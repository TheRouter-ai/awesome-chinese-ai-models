#!/usr/bin/env python3
"""Offline maintainer runner for normalized candidate JSONL files.

This command does not fetch the web. It consumes normalized candidates produced by
future discovery jobs, applies canonicalization/scoring/dedupe, and writes a daily
digest markdown file for review.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.maintainer import canonicalize_url, dedupe_candidates, render_daily_digest, score_candidate


def read_jsonl(path: Path) -> list[dict]:
    items = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            if "source_url" in item and "canonical_url" not in item:
                item["canonical_url"] = canonicalize_url(item["source_url"])
            if "id" not in item:
                item["id"] = f"{path.stem}-{line_no}"
            items.append(item)
    return items


def write_jsonl(path: Path, items: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Digest date, YYYY-MM-DD")
    parser.add_argument("--candidates", required=True, type=Path, help="Normalized candidate JSONL")
    parser.add_argument("--out-dir", default=Path("runs/manual"), type=Path)
    parser.add_argument("--digest", default=None, type=Path, help="Digest output path")
    args = parser.parse_args()

    raw = read_jsonl(args.candidates)
    scored = [score_candidate(item) for item in raw]
    eligible = [item for item in scored if item["decision"] != "reject"]
    accepted, duplicates = dedupe_candidates(eligible)
    digest = render_daily_digest(args.date, accepted)

    out_dir = args.out_dir
    write_jsonl(out_dir / "scored-candidates.jsonl", scored)
    write_jsonl(out_dir / "accepted-candidates.jsonl", accepted)
    write_jsonl(out_dir / "duplicates.jsonl", duplicates)

    digest_path = args.digest or out_dir / f"{args.date}.md"
    digest_path.parent.mkdir(parents=True, exist_ok=True)
    digest_path.write_text(digest, encoding="utf-8")

    print(f"raw={len(raw)} scored={len(scored)} accepted={len(accepted)} duplicates={len(duplicates)} digest={digest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
