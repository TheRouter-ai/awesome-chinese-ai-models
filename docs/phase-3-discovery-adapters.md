# Phase 3 — Discovery Adapters

Phase 3 adds source adapters that turn public source signals into normalized maintainer candidates.

## Scripts

- `scripts/discovery.py` — pure normalization and adapter mapping helpers.
- `scripts/discover_candidates.py` — CLI for source catalog discovery.

## Supported adapters

- `static` — emits a source-tracking candidate without network access.
- `github_org` — reads a GitHub organization via public API and maps updated repositories/releases.
- `huggingface_org` — reads a Hugging Face organization via public API and maps model cards.
- `modelscope_org` — maps ModelScope-style model payloads when an API endpoint is configured.
- `therouter_catalog` — parses TheRouter's public model catalog for supported Chinese model-page discovery.
- `rss` — parses RSS/Atom feeds into community/media candidates.

## Output

Normalized candidate JSONL:

```json
{"id":"...","title":"...","summary":"...","source_type":"official_release","category":"model_update","provider_id":"qwen","source_url":"https://...","canonical_url":"https://...","entity_key":"qwen:qwen3:latest","signals":{"chinese_ai_relevance":20,"awesome_value":18,"freshness":10,"verifiability":10,"category_clarity":9,"community_signal":2},"risks":[]}
```

Run static/offline smoke discovery:

```bash
python3 scripts/discover_candidates.py --include-static --out /tmp/candidates.jsonl
```

Run no-network discovery without smoke candidates:

```bash
python3 scripts/discover_candidates.py --out /tmp/candidates.jsonl
# candidates=0 unless sources have non-network adapters
```

Run public-source discovery:

```bash
python3 scripts/discover_candidates.py --fetch --out /tmp/candidates.jsonl --health /tmp/source-health.jsonl
```

## Source health

The CLI can write source health JSONL. Failed sources do not fail the whole run; they are recorded for follow-up so one blocked site does not stop daily maintenance.
