#!/usr/bin/env python3
"""Aggregate a week of news.yaml into a weekly digest draft.

This produces a raw aggregation only. The acam-curator agent rewrites the
draft into the polished "This Week in China AI Models" post.

Usage:
    python3 scripts/weekly_rollup.py --end 2026-05-22
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    print("PyYAML is required: python3 -m pip install pyyaml", file=sys.stderr)
    raise SystemExit(2) from exc

ROOT = Path(__file__).resolve().parents[1]
NEWS = ROOT / "data" / "news.yaml"
WEEKLY_DIR = ROOT / "newsletters" / "weekly"


def parse_date(value) -> date | None:
    try:
        return date.fromisoformat(str(value or "")[:10])
    except ValueError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--end", default=datetime.now(timezone.utc).date().isoformat())
    args = parser.parse_args()

    end = date.fromisoformat(args.end)
    start = end - timedelta(days=6)

    with NEWS.open("r", encoding="utf-8") as f:
        news = (yaml.safe_load(f) or {}).get("news", [])

    by_category: dict[str, list[dict]] = defaultdict(list)
    total = 0
    for item in news:
        item_date = parse_date(item.get("date"))
        if item_date is None or not (start <= item_date <= end):
            continue
        by_category[item.get("category", "update")].append(item)
        total += 1

    iso_year, iso_week, _ = end.isocalendar()
    out_path = WEEKLY_DIR / f"{iso_year}-W{iso_week:02d}.draft.md"
    WEEKLY_DIR.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# This Week in China AI Models — {iso_year}-W{iso_week:02d} (draft)",
        "",
        f"Window: {start.isoformat()} → {end.isoformat()} · {total} updates",
        "",
        "> Raw aggregation. The acam-curator agent rewrites this into the published digest.",
        "",
    ]
    for category in sorted(by_category):
        items = sorted(by_category[category], key=lambda x: int(x.get("score", 0)), reverse=True)
        lines.append(f"## {category} ({len(items)})")
        lines.append("")
        for item in items:
            title = item.get("title", "Untitled")
            url = (item.get("source") or {}).get("url", "")
            link = f"[{title}]({url})" if url else title
            lines.append(f"- {link} — {item.get('summary', '')}")
        lines.append("")

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Weekly rollup draft written: {out_path.relative_to(ROOT)} ({total} items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
