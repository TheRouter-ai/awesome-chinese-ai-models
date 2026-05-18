#!/usr/bin/env python3
"""Validate repository data files without requiring network access."""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    print("PyYAML is required: python3 -m pip install pyyaml", file=sys.stderr)
    raise SystemExit(2) from exc

ROOT = Path(__file__).resolve().parents[1]
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
URL_RE = re.compile(r"^https?://")


def load_yaml(rel: str):
    path = ROOT / rel
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def require(cond: bool, msg: str, errors: list[str]) -> None:
    if not cond:
        errors.append(msg)


def check_unique(items, key, label, errors):
    seen = {}
    for item in items:
        value = item.get(key)
        if value in seen:
            errors.append(f"duplicate {label}.{key}: {value}")
        seen[value] = item
    return set(seen)


def main() -> int:
    errors: list[str] = []

    providers_doc = load_yaml("data/providers.yaml") or {}
    models_doc = load_yaml("data/models.yaml") or {}
    caps_doc = load_yaml("data/capabilities.yaml") or {}
    news_doc = load_yaml("data/news.yaml") or {}
    resources_doc = load_yaml("data/resources.yaml") or {}
    benchmarks_doc = load_yaml("data/benchmarks.yaml") or {}
    use_cases_doc = load_yaml("data/use_cases.yaml") or {}

    providers = providers_doc.get("providers", [])
    models = models_doc.get("models", [])
    capabilities = caps_doc.get("capabilities", [])
    news = news_doc.get("news", [])
    resources = resources_doc.get("resources", [])
    benchmarks = benchmarks_doc.get("benchmarks", [])
    use_cases = use_cases_doc.get("use_cases", [])

    provider_ids = check_unique(providers, "id", "providers", errors)
    model_ids = check_unique(models, "id", "models", errors)
    capability_ids = check_unique(capabilities, "id", "capabilities", errors)
    check_unique(news, "id", "news", errors)
    check_unique(resources, "id", "resources", errors)
    check_unique(benchmarks, "id", "benchmarks", errors)
    check_unique(use_cases, "id", "use_cases", errors)

    for provider in providers:
        pid = provider.get("id")
        require(bool(pid and ID_RE.match(pid)), f"invalid provider id: {pid}", errors)
        require(bool(provider.get("name")), f"provider {pid} missing name", errors)
        website = provider.get("website")
        require(bool(website and URL_RE.match(website)), f"provider {pid} missing valid website", errors)
        require(isinstance(provider.get("tags"), list), f"provider {pid} tags must be list", errors)

    for cap in capabilities:
        cid = cap.get("id")
        require(bool(cid and ID_RE.match(cid)), f"invalid capability id: {cid}", errors)
        require(bool(cap.get("name")), f"capability {cid} missing name", errors)

    for model in models:
        mid = model.get("id")
        require(bool(mid and ID_RE.match(mid)), f"invalid model id: {mid}", errors)
        provider_id = model.get("provider_id")
        require(provider_id in provider_ids, f"model {mid} references unknown provider_id {provider_id}", errors)
        for cap in model.get("capabilities", []):
            require(cap in capability_ids, f"model {mid} references unknown capability {cap}", errors)
        access = model.get("access") or {}
        require(any(bool(v) for v in access.values()), f"model {mid} has no access mode", errors)
        official = model.get("official") or {}
        require(any(v for v in official.values()), f"model {mid} has no official source", errors)
        require(isinstance(model.get("tags"), list), f"model {mid} tags must be list", errors)
        status = model.get("status") or {}
        require("verified" in status, f"model {mid} missing status.verified", errors)

    for item in news:
        nid = item.get("id")
        require(bool(nid), "news item missing id", errors)
        require(bool(item.get("date")), f"news {nid} missing date", errors)
        source = item.get("source") or {}
        require(bool(source.get("url") and URL_RE.match(source.get("url"))), f"news {nid} missing valid source.url", errors)
        require(bool(item.get("verification", {}).get("status")), f"news {nid} missing verification.status", errors)

    for res in resources:
        rid = res.get("id")
        require(bool(rid), "resource missing id", errors)
        provider_id = res.get("provider_id")
        if provider_id is not None:
            require(provider_id in provider_ids, f"resource {rid} references unknown provider_id {provider_id}", errors)
        require(bool(res.get("url") and URL_RE.match(res.get("url"))), f"resource {rid} missing valid url", errors)
        require(isinstance(res.get("tags"), list), f"resource {rid} tags must be list", errors)

    for uc in use_cases:
        uid = uc.get("id")
        require(bool(uid), "use case missing id", errors)
        require(bool(uc.get("summary")), f"use case {uid} missing summary", errors)
        links = uc.get("links", [])
        require(isinstance(links, list) and links, f"use case {uid} missing links", errors)

    if errors:
        print("Validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print("Validation passed.")
    print(f"Providers: {len(providers)} | Models: {len(models)} | Resources: {len(resources)} | News: {len(news)} | Use cases: {len(use_cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
