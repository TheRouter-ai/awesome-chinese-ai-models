#!/usr/bin/env python3
"""Run the full maintainer pipeline for one day."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone, date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.maintainer import dedupe_candidates, score_candidate
from scripts.update_repo import append_news_items, render_newsletter_files


def read_jsonl(path: Path) -> list[dict]:
    items = []
    if not path.exists():
        return items
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def write_jsonl(path: Path, items: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")


def parse_item_date(item: dict) -> date | None:
    raw = str(item.get("published_at") or item.get("date") or "")[:10]
    try:
        return date.fromisoformat(raw)
    except ValueError:
        return None


def filter_fresh_candidates(items: list[dict], run_date: str, max_age_days: int) -> list[dict]:
    if max_age_days < 0:
        return items
    target = date.fromisoformat(run_date)
    fresh = []
    for item in items:
        item_date = parse_item_date(item)
        if item_date is None:
            continue
        age = (target - item_date).days
        if 0 <= age <= max_age_days:
            fresh.append(item)
    return fresh


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now(timezone.utc).date().isoformat())
    parser.add_argument("--fetch", action="store_true", help="fetch public sources")
    parser.add_argument("--include-static", action="store_true", help="include static source-tracking candidates for smoke tests")
    parser.add_argument("--fail-on-source-error", action="store_true")
    parser.add_argument("--limit-per-source", default=5, type=int)
    parser.add_argument("--min-accepted", default=10, type=int)
    parser.add_argument("--max-age-days", default=7, type=int, help="Only accept candidates published within this many days; -1 disables")
    parser.add_argument("--fail-under-target", action="store_true")
    parser.add_argument("--run-dir", default=None, type=Path)
    args = parser.parse_args()

    run_dir = args.run_dir or ROOT / "runs" / args.date / datetime.now(timezone.utc).strftime("%H%M%S")
    candidates_path = run_dir / "normalized-candidates.jsonl"
    health_path = run_dir / "source-health.jsonl"

    discover_cmd = [
        sys.executable,
        "scripts/discover_candidates.py",
        "--out",
        str(candidates_path),
        "--health",
        str(health_path),
        "--limit-per-source",
        str(args.limit_per_source),
    ]
    if args.fetch:
        discover_cmd.append("--fetch")
    if args.include_static:
        discover_cmd.append("--include-static")
    if args.fail_on_source_error:
        discover_cmd.append("--fail-on-source-error")
    run(discover_cmd)

    raw = read_jsonl(candidates_path)
    fresh_raw = filter_fresh_candidates(raw, args.date, args.max_age_days)
    scored = [score_candidate(item) for item in fresh_raw]
    eligible = [item for item in scored if item.get("decision") != "reject"]
    accepted, duplicates = dedupe_candidates(eligible)
    accepted = sorted(accepted, key=lambda item: (-int(item.get("score", 0)), item.get("title", "")))

    write_jsonl(run_dir / "scored-candidates.jsonl", scored)
    write_jsonl(run_dir / "accepted-candidates.jsonl", accepted)
    write_jsonl(run_dir / "duplicates.jsonl", duplicates)

    written = append_news_items(ROOT, accepted)
    daily_path = render_newsletter_files(ROOT, args.date, accepted)
    run([sys.executable, "scripts/generate_readme.py"])

    summary = {
        "date": args.date,
        "raw": len(raw),
        "fresh_raw": len(fresh_raw),
        "scored": len(scored),
        "accepted": len(accepted),
        "duplicates": len(duplicates),
        "news_items_written": written,
        "daily_digest": str(daily_path.relative_to(ROOT)),
        "run_dir": str(run_dir.relative_to(ROOT) if run_dir.is_relative_to(ROOT) else run_dir),
        "target_met": len(accepted) >= args.min_accepted,
    }
    (run_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if args.fail_under_target and len(accepted) < args.min_accepted:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
