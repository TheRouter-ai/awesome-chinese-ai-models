#!/usr/bin/env python3
"""Discover normalized candidates from configured sources.

The command is safe for CI/manual use:
- by default it performs no network calls and emits no static placeholder updates
- with `--include-static`, it emits source-tracking candidates for smoke tests
- with `--fetch`, it calls public APIs/RSS endpoints and records per-source health
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.discovery import (
    discover_from_github_releases,
    discover_from_huggingface_models,
    discover_from_modelscope_models,
    discover_from_rss,
    discover_from_static_source,
    discover_from_therouter_catalog,
    fetch_json,
    fetch_text,
    normalize_raw_item,
)
from scripts.maintainer import load_source_catalog


def github_org_from_url(url: str) -> str | None:
    marker = "github.com/"
    if marker not in url:
        return None
    rest = url.split(marker, 1)[1].strip("/")
    return rest.split("/", 1)[0] if rest else None


def huggingface_author_from_url(url: str) -> str | None:
    marker = "huggingface.co/"
    if marker not in url:
        return None
    rest = url.split(marker, 1)[1].strip("/")
    return rest.split("/", 1)[0] if rest else None


def discover_github_org(source: dict, limit: int) -> list[dict]:
    org = github_org_from_url(source["url"])
    if not org:
        return [discover_from_static_source(source)]
    repos = fetch_json(f"https://api.github.com/orgs/{org}/repos?sort=updated&per_page={min(limit, 20)}")
    candidates = []
    for repo in repos[:limit]:
        repo_name = repo.get("full_name")
        if not repo_name:
            continue
        candidates.append(
            normalize_raw_item(
                {
                    "title": f"GitHub repository update: {repo_name}",
                    "summary": repo.get("description") or "Repository tracked from an official GitHub organization.",
                    "source_type": source.get("source_type", "github_release"),
                    "provider_id": source.get("provider_id"),
                    "source_url": repo.get("html_url"),
                    "published_at": repo.get("pushed_at") or repo.get("updated_at"),
                    "model_id": repo_name.split("/", 1)[-1],
                    "version": repo.get("pushed_at") or "latest",
                    "category": "open_source",
                    "tags": ["github", "repository"],
                }
            )
        )
        releases_url = repo.get("releases_url", "").replace("{/id}", "")
        if releases_url:
            try:
                releases = fetch_json(f"{releases_url}?per_page=3")
                candidates.extend(discover_from_github_releases(releases[:3], source, repo_name))
            except Exception:
                pass
    return candidates


def discover_huggingface_org(source: dict, limit: int) -> list[dict]:
    author = huggingface_author_from_url(source["url"])
    if not author:
        return [discover_from_static_source(source)]
    models = fetch_json(f"https://huggingface.co/api/models?author={author}&sort=lastModified&direction=-1&limit={min(limit, 20)}")
    return discover_from_huggingface_models(models[:limit], source)


def discover_modelscope_org(source: dict, limit: int) -> list[dict]:
    api_url = source.get("api_url")
    if api_url:
        payload = fetch_json(api_url.format(limit=min(limit, 20)))
        if isinstance(payload, dict):
            models = payload.get("Data") or payload.get("data") or payload.get("models") or payload.get("items") or []
        else:
            models = payload
        return discover_from_modelscope_models(models[:limit], source)
    return []


def discover_therouter_catalog(source: dict, limit: int) -> list[dict]:
    return discover_from_therouter_catalog(fetch_text(source["url"]), source)[:limit]


def discover_source(source: dict, fetch: bool, limit: int, include_static: bool = False) -> tuple[list[dict], dict]:
    health = {"source_id": source.get("id"), "ok": True, "error": None, "count": 0}
    try:
        if not source.get("enabled", True):
            return [], {**health, "ok": True, "skipped": True}
        adapter = source.get("adapter") or "static"
        if adapter == "static" or not fetch:
            items = [discover_from_static_source(source)] if include_static else []
        elif adapter == "github_org":
            items = discover_github_org(source, limit)
        elif adapter == "huggingface_org":
            items = discover_huggingface_org(source, limit)
        elif adapter == "modelscope_org":
            items = discover_modelscope_org(source, limit)
        elif adapter == "therouter_catalog":
            items = discover_therouter_catalog(source, limit)
        elif adapter == "rss":
            items = discover_from_rss(fetch_text(source["url"]), source)
        else:
            items = [discover_from_static_source(source)]
        health["count"] = len(items)
        return items, health
    except Exception as exc:
        health.update({"ok": False, "error": str(exc), "count": 0})
        return [], health


def write_jsonl(path: Path, items: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", default=Path("agent/source-catalog.yaml"), type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--health", default=None, type=Path)
    parser.add_argument("--fetch", action="store_true", help="fetch public web/API sources")
    parser.add_argument("--include-static", action="store_true", help="emit static source-tracking candidates for smoke tests")
    parser.add_argument("--fail-on-source-error", action="store_true", help="return non-zero if any enabled source fails")
    parser.add_argument("--limit-per-source", default=5, type=int)
    args = parser.parse_args()

    sources = load_source_catalog(args.catalog)
    all_items: list[dict] = []
    health: list[dict] = []
    for source in sources:
        items, source_health = discover_source(source, fetch=args.fetch, limit=args.limit_per_source, include_static=args.include_static)
        all_items.extend(items)
        health.append(source_health)
    write_jsonl(args.out, all_items)
    if args.health:
        write_jsonl(args.health, health)
    print(f"sources={len(sources)} candidates={len(all_items)} out={args.out}")
    failures = [item for item in health if not item.get("ok")]
    if failures:
        print(f"source_failures={len(failures)}", file=sys.stderr)
        if args.fail_on_source_error:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
