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


def _flag(value) -> str:
    return "✅" if value else "—"


def render_comparison(rows):
    if not rows:
        return "No comparison data yet."
    lines = [
        "| Model | Best For | Context | Vision | Reasoning | API | Open Weights |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row.get('name', '')} | {row.get('best_for', '')} | {row.get('context', '')} "
            f"| {_flag(row.get('vision'))} | {_flag(row.get('reasoning'))} "
            f"| {_flag(row.get('api'))} | {_flag(row.get('open_source'))} |"
        )
    return "\n".join(lines)


def render_access_methods(methods):
    if not methods:
        return "No access methods documented yet."
    lines = []
    for m in methods:
        name = m.get("name", m.get("id", ""))
        url = m.get("url")
        heading = f"**[{name}]({url})**" if url else f"**{name}**"
        lines.append(f"- {heading} — {m.get('summary', '')}")
        if m.get("best_for"):
            lines.append(f"  - Best for: {m['best_for']}")
        if m.get("notes"):
            lines.append(f"  - {m['notes']}")
    return "\n".join(lines)


def render_availability(availability):
    regions = availability.get("regions", [])
    rows = availability.get("providers", [])
    if not rows:
        return "No availability data yet."
    headers = ["Provider"] + [r.get("label", r.get("id", "")) for r in regions] + ["Crypto Payment"]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    symbol = {"yes": "✅", "no": "—", "partial": "◐", "unknown": "?"}
    for row in rows:
        cells = [row.get("name", row.get("provider_id", ""))]
        for region in regions:
            cells.append(symbol.get(str(row.get(region.get("id"), "unknown")), "?"))
        cells.append(_flag(row.get("crypto_payment")))
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("Legend: ✅ available · ◐ partial · — not available · ? unverified.")
    lines.append("Availability changes often. Always verify with the provider.")
    return "\n".join(lines)


def render_best_for(rows):
    if not rows:
        return "No best-for mapping yet."
    lines = []
    for row in rows:
        lines.append(f"- **{row.get('name', row.get('provider_id', ''))}**")
        for case in row.get("use_cases", []):
            lines.append(f"  - {case}")
    return "\n".join(lines)


def render_benchmarks(benchmarks):
    if not benchmarks:
        return "No benchmark sources yet."
    lines = []
    for bm in benchmarks:
        name = bm.get("name", bm.get("id", ""))
        url = bm.get("url", "")
        link = f"[{name}]({url})" if url else name
        lines.append(f"- {link} — {bm.get('coverage', '')}")
        if bm.get("note"):
            lines.append(f"  - {bm['note']}")
    return "\n".join(lines)


def render_faq(faq):
    if not faq:
        return "No FAQ entries yet."
    lines = []
    for entry in faq:
        lines.append(f"### {entry.get('question', '')}")
        lines.append("")
        lines.append(" ".join((entry.get("answer", "") or "").split()))
        lines.append("")
    return "\n".join(lines).rstrip()


def generate() -> str:
    text = README.read_text(encoding="utf-8")
    providers = load_yaml("data/providers.yaml").get("providers", [])
    models = load_yaml("data/models.yaml").get("models", [])
    news = load_yaml("data/news.yaml").get("news", [])
    comparison = load_yaml("data/comparison.yaml").get("comparison", [])
    access_methods = load_yaml("data/access_methods.yaml").get("access_methods", [])
    availability = load_yaml("data/availability.yaml").get("availability", {})
    best_for = load_yaml("data/best_for.yaml").get("best_for", [])
    benchmarks = load_yaml("data/benchmarks.yaml").get("benchmarks", [])
    faq = load_yaml("data/faq.yaml").get("faq", [])
    providers_by_id = {p.get("id"): p for p in providers}
    text = replace_block(text, "comparison-table", render_comparison(comparison))
    text = replace_block(text, "how-to-access", render_access_methods(access_methods))
    text = replace_block(text, "best-for", render_best_for(best_for))
    text = replace_block(text, "global-availability", render_availability(availability))
    text = replace_block(text, "benchmarks", render_benchmarks(benchmarks))
    text = replace_block(text, "latest-news", render_latest_news(news))
    text = replace_block(text, "featured-models", render_models(models, providers_by_id))
    text = replace_block(text, "providers", render_providers(providers))
    text = replace_block(text, "faq", render_faq(faq))
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
