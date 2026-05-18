#!/usr/bin/env python3
"""Discovery adapters for normalized maintainer candidates.

Adapters are split into two layers:
- pure mapping helpers that convert already-fetched payloads into candidates
- optional stdlib fetch helpers used by `discover_candidates.py`
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any
from urllib.request import Request, urlopen
from xml.etree import ElementTree

from scripts.maintainer import canonicalize_url


def slugify(value: str | None) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "unknown"


def today_iso() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def stable_id(*parts: str) -> str:
    joined = "|".join(part for part in parts if part)
    digest = hashlib.sha1(joined.encode("utf-8")).hexdigest()[:10]
    return f"{slugify(parts[0] if parts else 'candidate')}-{digest}"


def infer_category(title: str, source_type: str | None = None, tags: list[str] | None = None) -> str:
    text = f"{title} {' '.join(tags or [])}".lower()
    if source_type == "github_release":
        return "open_source"
    if source_type == "model_card":
        return "model_update"
    if source_type == "official_docs":
        return "api_update"
    if any(word in text for word in ["price", "pricing", "降价", "价格"]):
        return "pricing"
    if any(word in text for word in ["benchmark", "eval", "leaderboard", "评测", "榜单"]):
        return "benchmark"
    if any(word in text for word in ["paper", "arxiv", "论文"]):
        return "paper"
    if any(word in text for word in ["release", "发布", "model", "模型"]):
        return "model_update"
    return "community"


def infer_signals(source_type: str | None, provider_id: str | None, category: str | None) -> dict[str, int]:
    source_bonus = {
        "official_release": (20, 18, 10),
        "official_docs": (20, 14, 10),
        "github_release": (20, 16, 9),
        "model_card": (20, 16, 9),
        "benchmark": (18, 15, 8),
        "credible_media": (15, 10, 6),
        "community": (10, 8, 4),
    }.get(source_type or "", (10, 8, 4))
    relevance = source_bonus[0] if provider_id else max(source_bonus[0] - 4, 0)
    if category in {"model_release", "open_source", "benchmark", "api_update"}:
        awesome_value = min(source_bonus[1] + 2, 20)
    else:
        awesome_value = source_bonus[1]
    return {
        "chinese_ai_relevance": relevance,
        "awesome_value": awesome_value,
        "freshness": 10,
        "verifiability": source_bonus[2],
        "category_clarity": 9 if category else 6,
        "community_signal": 4 if source_type in {"credible_media", "community"} else 2,
    }


def normalize_raw_item(raw: dict[str, Any]) -> dict[str, Any]:
    title = (raw.get("title") or raw.get("name") or "Untitled").strip()
    source_url = raw.get("source_url") or raw.get("url") or ""
    canonical_url = canonicalize_url(source_url) if source_url else ""
    source_type = raw.get("source_type") or "community"
    provider_id = raw.get("provider_id")
    model_id = raw.get("model_id") or raw.get("model")
    version = raw.get("version") or raw.get("tag") or "latest"
    category = raw.get("category") or infer_category(title, source_type, raw.get("tags"))
    entity_key = raw.get("entity_key")
    if not entity_key and provider_id and model_id:
        entity_key = f"{provider_id}:{slugify(model_id)}:{slugify(version)}"
    item = {
        "id": raw.get("id") or stable_id(title, canonical_url),
        "title": title,
        "summary": (raw.get("summary") or raw.get("description") or "").strip(),
        "source_type": source_type,
        "category": category,
        "provider_id": provider_id,
        "model_id": slugify(model_id) if model_id else None,
        "version": version,
        "source_url": source_url,
        "canonical_url": canonical_url,
        "published_at": raw.get("published_at") or raw.get("date") or today_iso(),
        "entity_key": entity_key,
        "evidence_urls": raw.get("evidence_urls", []),
        "signals": raw.get("signals") or infer_signals(source_type, provider_id, category),
        "risks": raw.get("risks") or [],
    }
    return {key: value for key, value in item.items() if value is not None}


def discover_from_github_releases(releases: list[dict[str, Any]], source: dict[str, Any], repo: str) -> list[dict[str, Any]]:
    items = []
    for release in releases:
        tag = release.get("tag_name") or release.get("name") or "latest"
        title = release.get("name") or tag
        body = release.get("body") or ""
        items.append(
            normalize_raw_item(
                {
                    "id": stable_id(repo, tag, release.get("html_url", "")),
                    "title": f"{repo} release {title}",
                    "summary": body.strip().replace("\r", " ").replace("\n", " ")[:240],
                    "source_type": source.get("source_type", "github_release"),
                    "provider_id": source.get("provider_id"),
                    "source_url": release.get("html_url"),
                    "published_at": release.get("published_at"),
                    "version": tag,
                    "model_id": repo.split("/", 1)[-1],
                    "category": "open_source",
                    "tags": ["github", "release"],
                }
            )
        )
    return items


def discover_from_huggingface_models(models: list[dict[str, Any]], source: dict[str, Any]) -> list[dict[str, Any]]:
    items = []
    for model in models:
        model_id = model.get("modelId") or model.get("id")
        if not model_id:
            continue
        tags = model.get("tags") or []
        items.append(
            normalize_raw_item(
                {
                    "id": stable_id(model_id, model.get("lastModified", "")),
                    "title": f"Hugging Face model update: {model_id}",
                    "summary": f"Model card/update on Hugging Face. Tags: {', '.join(tags[:8])}",
                    "source_type": source.get("source_type", "model_card"),
                    "provider_id": source.get("provider_id"),
                    "source_url": f"https://huggingface.co/{model_id}",
                    "published_at": model.get("lastModified"),
                    "model_id": model_id.split("/", 1)[-1],
                    "category": "model_update",
                    "tags": tags,
                }
            )
        )
    return items


def discover_from_modelscope_models(models: list[dict[str, Any]], source: dict[str, Any]) -> list[dict[str, Any]]:
    """Map ModelScope-style model payloads to normalized candidates.

    ModelScope endpoints have changed over time, so this mapper accepts the common
    fields seen in public/search payloads and local fixtures rather than binding to
    one endpoint schema.
    """
    items = []
    for model in models:
        model_id = model.get("modelId") or model.get("model_id") or model.get("id") or model.get("name")
        if not model_id:
            continue
        owner = model.get("owner") or model.get("namespace") or source.get("provider_id")
        path = str(model_id).strip("/")
        if owner and "/" not in path:
            path = f"{owner}/{path}"
        url = model.get("url") or model.get("modelUrl") or f"https://modelscope.cn/models/{path}"
        tags = model.get("tags") or model.get("tasks") or []
        if isinstance(tags, str):
            tags = [tags]
        items.append(
            normalize_raw_item(
                {
                    "id": stable_id(path, model.get("lastUpdated") or model.get("updated_at") or ""),
                    "title": f"ModelScope model update: {path}",
                    "summary": (model.get("description") or model.get("summary") or "Model card/update on ModelScope.")[:240],
                    "source_type": source.get("source_type", "model_card"),
                    "provider_id": source.get("provider_id"),
                    "source_url": url,
                    "published_at": model.get("lastUpdated") or model.get("updated_at") or model.get("gmtModified"),
                    "model_id": path.split("/", 1)[-1],
                    "category": "model_update",
                    "tags": tags,
                }
            )
        )
    return items


def discover_from_therouter_catalog(html_text: str, source: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract Chinese-model catalog entries from TheRouter's public model page."""
    provider_allowlist = set(source.get("provider_allowlist") or [])
    items = []
    seen: set[str] = set()
    for href in re.findall(r"href=[\"'](/models/[^\"']+)[\"']", html_text):
        href = html.unescape(href)
        slug = href.strip("/").split("/")[-1]
        if "--" not in slug:
            continue
        provider_id, model_id = slug.split("--", 1)
        if provider_allowlist and provider_id not in provider_allowlist:
            continue
        url = "https://therouter.ai" + href
        if url in seen:
            continue
        seen.add(url)
        items.append(
            normalize_raw_item(
                {
                    "id": stable_id("therouter", provider_id, model_id),
                    "title": f"TheRouter supported model page: {provider_id}/{model_id}",
                    "summary": "TheRouter model page with model introduction and OpenAI-compatible access details.",
                    "source_type": source.get("source_type", "official_docs"),
                    "provider_id": provider_id,
                    "model_id": model_id,
                    "source_url": url,
                    "published_at": today_iso(),
                    "category": "api_update",
                    "tags": ["therouter", "model_page"],
                }
            )
        )
    return items


def discover_from_rss(xml_text: str, source: dict[str, Any]) -> list[dict[str, Any]]:
    root = ElementTree.fromstring(xml_text)
    items = []
    for node in root.findall(".//item") + root.findall(".//{http://www.w3.org/2005/Atom}entry"):
        title_node = node.find("title")
        if title_node is None:
            title_node = node.find("{http://www.w3.org/2005/Atom}title")
        link_node = node.find("link")
        if link_node is None:
            link_node = node.find("{http://www.w3.org/2005/Atom}link")
        desc_node = node.find("description")
        if desc_node is None:
            desc_node = node.find("summary")
        if desc_node is None:
            desc_node = node.find("{http://www.w3.org/2005/Atom}summary")
        date_node = node.find("pubDate")
        if date_node is None:
            date_node = node.find("published")
        if date_node is None:
            date_node = node.find("updated")
        link = ""
        if link_node is not None:
            link = link_node.get("href") or (link_node.text or "")
        published = date_node.text if date_node is not None and date_node.text else today_iso()
        try:
            if "," in published:
                published = parsedate_to_datetime(published).date().isoformat()
        except Exception:
            pass
        title = html.unescape(title_node.text if title_node is not None and title_node.text else "Untitled")
        summary = html.unescape(desc_node.text if desc_node is not None and desc_node.text else "")
        items.append(
            normalize_raw_item(
                {
                    "title": title,
                    "summary": re.sub(r"<[^>]+>", "", summary)[:240],
                    "source_type": source.get("source_type", "credible_media"),
                    "provider_id": source.get("provider_id"),
                    "source_url": link,
                    "published_at": published,
                    "category": infer_category(title, source.get("source_type")),
                }
            )
        )
    return items


def discover_from_static_source(source: dict[str, Any]) -> dict[str, Any]:
    return normalize_raw_item(
        {
            "id": f"source-{source['id']}",
            "title": f"Tracked source: {source['name']}",
            "summary": f"Official/trusted source tracked by maintainer agent: {source['name']}.",
            "source_type": source.get("source_type", "official_docs"),
            "provider_id": source.get("provider_id"),
            "source_url": source.get("url"),
            "category": "official_resource",
            "signals": {
                "chinese_ai_relevance": 20 if source.get("provider_id") else 12,
                "awesome_value": 12,
                "freshness": 3,
                "verifiability": 10,
                "category_clarity": 10,
                "community_signal": 0,
            },
        }
    )


def fetch_json(url: str, timeout: int = 20) -> Any:
    headers = {"User-Agent": "awesome-chinese-ai-models-maintainer/1.0"}
    token = os.environ.get("GITHUB_TOKEN")
    if token and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {token}"
        headers["Accept"] = "application/vnd.github+json"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_text(url: str, timeout: int = 20) -> str:
    request = Request(url, headers={"User-Agent": "awesome-chinese-ai-models-maintainer/1.0"})
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")
