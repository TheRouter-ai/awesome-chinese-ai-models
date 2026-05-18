# Phase 2 — Maintainer Agent Skeleton

This phase adds the first executable layer for `awesome-chinese-ai-models-maintainer`.

## What exists now

- `agent/profile.yaml` — repo and automation policy.
- `agent/source-catalog.yaml` — initial trusted source list.
- `agent/scoring-policy.yaml` — scoring thresholds, source priority, hard blocks.
- `scripts/maintainer.py` — deterministic helper functions for URL canonicalization, scoring, dedupe, source catalog validation, and digest rendering.
- `scripts/run_maintainer.py` — offline runner for normalized JSONL candidates.
- `tests/test_maintainer.py` — unit tests for the core maintainer behavior.

## What this phase deliberately does not do

- It does not fetch web pages yet.
- It does not open PRs yet.
- It does not auto-merge.
- It does not store private state in the public repo.

## Candidate JSONL shape

```json
{"id":"qwen-update-1","title":"Qwen release","summary":"...","source_type":"official_release","category":"model_release","provider_id":"qwen","source_url":"https://...","entity_key":"qwen:qwen3:v1","signals":{"chinese_ai_relevance":20,"awesome_value":18,"freshness":10,"verifiability":10,"category_clarity":10,"community_signal":5},"risks":[]}
```

Run:

```bash
python3 scripts/run_maintainer.py --date 2026-05-18 --candidates path/to/candidates.jsonl --out-dir runs/2026-05-18/manual
```

`runs/` is gitignored. Future cron/agent runs should keep raw/private state outside the repo or under ignored paths.

## Next phase

Phase 3 should add discovery adapters:

- GitHub org/release adapter
- Hugging Face org/model-card adapter
- ModelScope adapter
- RSS/blog adapter
- benchmark adapter

Each adapter should output normalized candidate JSONL, then call this deterministic maintainer layer.
