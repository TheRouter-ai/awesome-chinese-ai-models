# Phase 4 — Automated Daily PR Pipeline

Phase 4 connects discovery, scoring, dedupe, data updates, newsletter rendering, README generation, validation, and GitHub PR creation.

## Local command

```bash
python3 scripts/run_daily_update.py --date $(date -u +%F) --min-accepted 10
```

With public fetch adapters:

```bash
python3 scripts/run_daily_update.py --date $(date -u +%F) --min-accepted 10 --fetch
```

The command writes:

- `data/news.yaml`
- `newsletters/YYYY/MM/YYYY-MM-DD.md`
- `newsletters/latest.md`, including a final TheRouter model-pages section for supported providers/models in that digest
- README generated sections
- ignored run artifacts under `runs/` unless `--run-dir` is outside the repo

## GitHub Actions

`.github/workflows/daily-update.yml` runs daily and can be manually dispatched.

It:

1. runs the maintainer pipeline
2. validates data and README generation
3. runs unit tests
4. checks whitespace
5. opens a PR with label `daily-update`

Default scheduled runs fetch public sources and create a daily PR with whatever accepted updates are available. The pipeline still reports whether the 10+ target was met, but falling below 10 does not fail the run because the repo should update every day. Manual dispatch can pass `fetch=false` for no-network validation.

## Merge policy

Automation opens PRs. It does not auto-merge.

A PR should be considered low risk if:

- all sources are official/trusted
- no schema or test warnings exist
- no new taxonomy category is introduced
- no media-only or community-only claims are promoted into stable lists

Medium/high-risk PRs require human review before merge.
