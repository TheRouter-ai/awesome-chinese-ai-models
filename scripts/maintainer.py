#!/usr/bin/env python3
"""Core helpers for the awesome-chinese-ai-models maintainer agent.

These helpers are intentionally deterministic and network-free. Discovery agents can
fetch raw candidates elsewhere; this module normalizes, scores, dedupes, and renders
reviewable output for the repository.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import yaml

SOURCE_PRIORITY = {
    "official_release": 100,
    "official_docs": 95,
    "model_card": 95,
    "github_release": 95,
    "paper": 85,
    "benchmark": 80,
    "credible_media": 65,
    "community": 45,
}

TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "spm",
    "from",
    "ref",
}

RISK_PENALTIES = {
    "hype": -5,
    "unclear_license": -3,
    "unstable_link": -5,
    "duplicate": -10,
    "rumor_only": -20,
    "spam": -20,
}

REQUIRED_SOURCE_FIELDS = {"id", "name", "source_type", "url", "priority", "enabled"}


def canonicalize_url(url: str) -> str:
    """Return a stable URL for dedupe by stripping fragments/tracking params."""
    parsed = urlsplit(url.strip())
    query = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
        if key.lower() not in TRACKING_PARAMS and not key.lower().startswith("utm_")
    ]
    path = parsed.path.rstrip("/") if parsed.path != "/" else parsed.path
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower() if "github.com" not in parsed.netloc.lower() else parsed.netloc, path, urlencode(query), ""))


def source_rank(source_type: str | None) -> int:
    return SOURCE_PRIORITY.get(source_type or "", 0)


def score_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    """Score one normalized candidate and return score + routing decision."""
    signals = candidate.get("signals") or {}
    score = 0
    score += min(int(signals.get("chinese_ai_relevance", 0)), 20)
    score += min(source_rank(candidate.get("source_type")), 100) * 15 // 100
    score += min(int(signals.get("awesome_value", 0)), 20)
    score += min(int(signals.get("freshness", 0)), 10)
    score += min(int(signals.get("verifiability", 0)), 10)
    score += min(int(signals.get("category_clarity", 0)), 10)
    score += min(int(signals.get("community_signal", 0)), 10)

    risks = candidate.get("risks") or []
    for risk in risks:
        score += RISK_PENALTIES.get(risk, 0)

    hard_blocks = {"spam", "rumor_only", "not_chinese_ai_related", "unreachable_primary_url"}
    if hard_blocks.intersection(risks):
        decision = "reject"
    elif score >= 65:
        decision = "stable_entry"
    elif score >= 55:
        decision = "update_existing"
    elif score >= 45:
        decision = "daily_digest"
    else:
        decision = "reject"

    enriched = dict(candidate)
    enriched["score"] = score
    enriched["decision"] = decision
    return enriched


def dedupe_candidates(
    candidates: list[dict[str, Any]],
    seen_urls: set[str] | None = None,
    seen_entities: set[str] | None = None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Dedupe candidates, preferring higher-priority primary sources."""
    initial_seen_urls = set(seen_urls or set())
    initial_seen_entities = set(seen_entities or set())
    seen_urls = set(initial_seen_urls)
    seen_entities = set(initial_seen_entities)
    duplicates: list[dict[str, Any]] = []
    accepted_by_entity: dict[str, dict[str, Any]] = {}
    accepted_without_entity: list[dict[str, Any]] = []

    for item in candidates:
        candidate = dict(item)
        url = candidate.get("canonical_url") or canonicalize_url(candidate.get("source_url", ""))
        candidate["canonical_url"] = url
        entity = candidate.get("entity_key")

        if url in seen_urls:
            candidate["duplicate_reason"] = "seen_url" if url in initial_seen_urls else "duplicate_url_same_batch"
            duplicates.append(candidate)
            continue
        if entity and entity in seen_entities:
            candidate["duplicate_reason"] = "seen_entity" if entity in initial_seen_entities else "duplicate_entity_same_batch"
            duplicates.append(candidate)
            continue

        if entity:
            current = accepted_by_entity.get(entity)
            if current is None:
                accepted_by_entity[entity] = candidate
                seen_urls.add(url)
                continue
            if source_rank(candidate.get("source_type")) > source_rank(current.get("source_type")):
                current["duplicate_reason"] = "lower_priority_same_entity"
                duplicates.append(current)
                accepted_by_entity[entity] = candidate
                seen_urls.add(url)
            else:
                candidate["duplicate_reason"] = "lower_priority_same_entity"
                duplicates.append(candidate)
        else:
            accepted_without_entity.append(candidate)
            seen_urls.add(url)

    accepted = list(accepted_by_entity.values()) + accepted_without_entity
    accepted.sort(key=lambda item: (-source_rank(item.get("source_type")), item.get("id", "")))
    duplicates.sort(key=lambda item: item.get("id", ""))
    return accepted, duplicates


def select_supported_model_links(
    candidates: list[dict[str, Any]],
    model_links: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Return TheRouter model links relevant to the day's accepted candidates."""
    if not model_links:
        return []
    providers = {item.get("provider_id") or item.get("provider") for item in candidates}
    model_ids = {item.get("model_id") for item in candidates}
    providers.discard(None)
    model_ids.discard(None)
    selected: list[dict[str, Any]] = []
    seen_urls: set[str] = set()
    for link in model_links:
        url = link.get("url")
        if not url or url in seen_urls:
            continue
        if link.get("provider_id") in providers or link.get("model_id") in model_ids:
            selected.append(link)
            seen_urls.add(url)
    return selected


def render_daily_digest(date: str, candidates: list[dict[str, Any]], model_links: list[dict[str, Any]] | None = None) -> str:
    """Render a Markdown daily digest from accepted candidates."""
    ordered = sorted(candidates, key=lambda item: (-int(item.get("score", 0)), item.get("title", "")))
    lines = [
        f"# Chinese AI Models Digest — {date}",
        "",
        f"Accepted updates: {len(ordered)}",
        "",
        "## Updates",
        "",
    ]
    if not ordered:
        lines.append("No accepted updates today.")
    for item in ordered:
        title = item.get("title", "Untitled")
        url = item.get("canonical_url") or item.get("source_url") or ""
        category = item.get("category", "update")
        provider = item.get("provider_id") or item.get("provider") or "unknown"
        summary = item.get("summary", "")
        score = item.get("score")
        link = f"[{title}]({url})" if url else title
        score_part = f" score={score}" if score is not None else ""
        lines.append(f"- `{category}` `{provider}` {link} — {summary}{score_part}")
    lines.append("")
    supported_links = select_supported_model_links(ordered, model_links)
    if supported_links:
        lines.append("## TheRouter model pages")
        lines.append("")
        lines.append("相关模型可通过 TheRouter 查看模型介绍、API 兼容信息与接入方式：")
        lines.append("")
        for link in supported_links:
            lines.append(f"- [{link.get('title')}]({link.get('url')})")
        lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("Generated by the maintainer pipeline. Verify claims with primary sources before promoting items to stable collections.")
    return "\n".join(lines) + "\n"


def load_source_catalog(path: str | Path) -> list[dict[str, Any]]:
    """Load and validate a source catalog."""
    with Path(path).open("r", encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    sources = doc.get("sources")
    if not isinstance(sources, list):
        raise ValueError("source catalog must contain a sources list")
    for idx, source in enumerate(sources):
        missing = REQUIRED_SOURCE_FIELDS - set(source.keys())
        if missing:
            raise ValueError(f"source #{idx} missing required fields: {', '.join(sorted(missing))}")
    return sources
