#!/usr/bin/env python3
"""Apply accepted maintainer candidates to repository data and newsletters."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from scripts.maintainer import render_daily_digest


def candidate_to_news_item(candidate: dict[str, Any]) -> dict[str, Any]:
    published = str(candidate.get("published_at") or candidate.get("date") or "")
    date = published[:10] if published else "unknown-date"
    source_url = candidate.get("canonical_url") or candidate.get("source_url")
    return {
        "id": candidate.get("id"),
        "date": date,
        "title": candidate.get("title"),
        "summary": candidate.get("summary", ""),
        "category": candidate.get("category", "community"),
        "importance": "medium" if int(candidate.get("score", 0)) >= 65 else "low",
        "entities": {
            "providers": [candidate["provider_id"]] if candidate.get("provider_id") else [],
            "models": [candidate["model_id"]] if candidate.get("model_id") else [],
        },
        "source": {
            "type": candidate.get("source_type", "community"),
            "name": candidate.get("source_name") or candidate.get("provider_id") or "source",
            "url": source_url,
            "published_at": candidate.get("published_at") or date,
        },
        "verification": {
            "status": "verified" if candidate.get("source_type") in {"official_release", "official_docs", "github_release", "model_card", "benchmark"} else "unverified",
            "checked_by": "awesome-chinese-ai-models-maintainer",
        },
        "tags": [candidate.get("category", "community"), candidate.get("provider_id") or "chinese-ai"],
        "include_in_newsletter": True,
        "include_in_readme": int(candidate.get("score", 0)) >= 55,
        "score": candidate.get("score"),
        "decision": candidate.get("decision"),
    }


def append_news_items(root: str | Path, candidates: list[dict[str, Any]]) -> int:
    root = Path(root)
    path = root / "data" / "news.yaml"
    if path.exists():
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    else:
        doc = {"news": []}
    existing = doc.get("news") or []
    existing_ids = {item.get("id") for item in existing}
    existing_urls = {(item.get("source") or {}).get("url") for item in existing}
    new_items = []
    for candidate in candidates:
        item = candidate_to_news_item(candidate)
        if not item.get("id") or item["id"] in existing_ids or item["source"]["url"] in existing_urls:
            continue
        new_items.append(item)
        existing_ids.add(item["id"])
        existing_urls.add(item["source"]["url"])
    doc["news"] = new_items + existing
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=120), encoding="utf-8")
    return len(new_items)


def render_newsletter_files(root: str | Path, date: str, candidates: list[dict[str, Any]]) -> Path:
    root = Path(root)
    digest = render_daily_digest(date, candidates)
    year, month, _day = date.split("-", 2)
    daily_path = root / "newsletters" / year / month / f"{date}.md"
    latest_path = root / "newsletters" / "latest.md"
    daily_path.parent.mkdir(parents=True, exist_ok=True)
    latest_path.parent.mkdir(parents=True, exist_ok=True)
    daily_path.write_text(digest, encoding="utf-8")
    latest_path.write_text(digest, encoding="utf-8")
    return daily_path
