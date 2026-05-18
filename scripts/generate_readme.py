#!/usr/bin/env python3
"""Generate guarded README sections from data/*.yaml."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError as exc:
    print("PyYAML is required: python3 -m pip install pyyaml", file=sys.stderr)
    raise SystemExit(2) from exc

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


def load_yaml(rel: str):
    with (ROOT / rel).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def replace_block(text: str, block: str, body: str) -> str:
    start = f"<!-- AUTO-GENERATED:START {block} -->"
    end = f"<!-- AUTO-GENERATED:END {block} -->"
    before, sep, rest = text.partition(start)
    if not sep:
        raise ValueError(f"missing start marker for {block}")
    current, sep, after = rest.partition(end)
    if not sep:
        raise ValueError(f"missing end marker for {block}")
    return before + start + "\n" + body.rstrip() + "\n" + end + after


def render_latest_news(news):
    items = sorted(news, key=lambda x: (x.get("date") or "", x.get("id") or ""), reverse=True)[:10]
    if not items:
        return "No daily updates have been published yet. See `docs/agent-workflow.md` for the planned 10+ updates/day maintainer workflow."
    lines = []
    for item in items:
        date = item.get("date", "unknown-date")
        title = item.get("title", "Untitled")
        url = (item.get("source") or {}).get("url", "")
        category = item.get("category", "update")
        summary = item.get("summary", "")
        link = f"[{title}]({url})" if url else title
        lines.append(f"- {date} `{category}` {link} — {summary}")
    return "\n".join(lines)


def render_models(models, providers_by_id):
    featured = models[:12]
    if not featured:
        return "No featured models yet."
    lines = ["| Model | Provider | Type | Access | Open Weights | Official |", "| --- | --- | --- | --- | --- | --- |"]
    for model in featured:
        provider = providers_by_id.get(model.get("provider_id"), {}).get("name", model.get("provider_id", ""))
        caps = model.get("capabilities", [])
        typ = ", ".join(caps[:3]) if caps else "model"
        access = model.get("access", {})
        modes = [label for label, value in access.items() if value for _ in [0]]
        access_text = " / ".join(modes) if modes else "Unknown"
        open_weights = "Yes" if access.get("weights") else "No"
        official = model.get("official", {})
        url = official.get("website") or official.get("github") or official.get("docs") or ""
        name = model.get("name", model.get("id"))
        link = f"[{name}]({url})" if url else name
        lines.append(f"| {link} | {provider} | {typ} | {access_text} | {open_weights} | [Source]({url}) |")
    return "\n".join(lines)


def render_providers(providers):
    if not providers:
        return "No providers yet."
    lines = []
    for p in providers:
        name = p.get("name", p.get("id"))
        name_zh = p.get("name_zh")
        label = f"{name} / {name_zh}" if name_zh and name_zh != name else name
        website = p.get("website", "")
        tags = ", ".join(p.get("tags", [])[:4])
        lines.append(f"- [{label}]({website}) — {tags}.")
    return "\n".join(lines)


def generate() -> str:
    text = README.read_text(encoding="utf-8")
    providers = load_yaml("data/providers.yaml").get("providers", [])
    models = load_yaml("data/models.yaml").get("models", [])
    news = load_yaml("data/news.yaml").get("news", [])
    providers_by_id = {p.get("id"): p for p in providers}
    text = replace_block(text, "latest-news", render_latest_news(news))
    text = replace_block(text, "featured-models", render_models(models, providers_by_id))
    text = replace_block(text, "providers", render_providers(providers))
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if README is not up to date")
    args = parser.parse_args()
    new_text = generate()
    old_text = README.read_text(encoding="utf-8")
    if args.check:
        if new_text != old_text:
            print("README.md is not up to date. Run: python3 scripts/generate_readme.py")
            return 1
        print("README.md is up to date.")
        return 0
    README.write_text(new_text, encoding="utf-8")
    print("README.md updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
