# OpenClaw Agent — `acam-curator`

`acam-curator` is the OpenClaw agent that operates this repository. It is the
judgment-and-writing layer on top of the deterministic GitHub Actions data
pipeline. See `growth-plan.md` for the two-layer architecture.

## Where the agent lives

The agent definition is **not** in this repo (it contains operational config
and is bound to a private OpenClaw install):

- Agent dir: `~/.openclaw/agents/acam-curator/agent/`
  - `CLAUDE.md` — system prompt (source of truth)
  - `AGENT_CARD.yaml` — capability contract
  - `models.json` — model routing
  - `sync-prompt.mjs` — syncs `CLAUDE.md` into `openclaw.json`
- State dir: `~/.openclaw/agents/acam-curator/state/`
- Registry: `openclaw.json` → `agents.list[id=acam-curator]`

This repo only documents the contract the agent operates against.

## Run modes

| Mode | Trigger | What it does |
| --- | --- | --- |
| A. PR gate | after daily bot PR | Review `bot/daily-awesome-update`: source quality, dedupe, neutral tone, CI green → auto-merge; else comment and skip |
| B. Stable curation | daily | Promote recurring digest items into `data/models.yaml`, `data/providers.yaml`, and `collections/*.md` |
| C. Editorial | daily / on events | Maintain `comparison`, `availability`, `best_for`, `access_methods`, `benchmarks`, `faq` data files; regenerate README; open a PR |
| D. Weekly digest | Monday | Turn the week's `news.yaml` into `newsletters/weekly/YYYY-Www.md` |
| E. Distribution | daily / weekly | Run `scripts/broadcast_telegram.py`; draft X / Reddit / HN posts to state |
| F. SEO | weekly | Check GitHub topics and natural keyword coverage |

## PR quality gate

The daily GitHub Action opens `bot/daily-awesome-update`. The agent reviews it
and, per the operator's decision, **auto-merges** when checks pass:

1. CI is green (`validate.yml`).
2. The diff scope is sane — `data/news.yaml`, `newsletters/`, regenerated
   README blocks; no unexpected files.
3. Sources are P0/P1 per `CONTRIBUTING.md`; no SEO spam or dead mirrors.
4. Tone is neutral — no hype words (`最强`, `吊打`, `遥遥领先`).

Pass → `gh pr merge --squash`. Fail → `gh pr comment` with the reason, skip
the merge, leave for human review. Every decision is logged to
`state/pr-reviews.jsonl`.

## State files

Kept outside the public repo:

- `pr-reviews.jsonl` — every PR gate decision
- `curated.jsonl` — items promoted to stable entries
- `broadcasts.jsonl` — what was sent to Telegram / drafted for X
- `weekly-runs.jsonl` — weekly digest runs

## Telegram setup

The broadcast channel is `@ChineseAIModels`.

1. In Telegram, create a public channel `@ChineseAIModels`.
2. Talk to `@BotFather`, create a bot, copy its token.
3. Add the bot as an **admin** of the channel (post-messages permission).
4. Store credentials in `~/.openclaw/.env` (never in this repo):
   ```
   ACAM_TELEGRAM_BOT_TOKEN=...
   ACAM_TELEGRAM_CHANNEL=@ChineseAIModels
   ```
5. Test: `python3 scripts/broadcast_telegram.py --dry-run` then a real send.

`scripts/broadcast_telegram.py` reads a daily or weekly digest, picks the
high-signal events (new models, pricing, benchmarks), and posts a compact
message. It uses only the Python standard library.

## Scheduling

Registered as cron jobs in the OpenClaw gateway (local time):

- `30 2 * * *` — PR gate (after the 01:10 UTC daily Action)
- `15 9 * * *` — editorial + stable curation sweep
- `45 9 * * 1` — weekly digest + distribution (Mondays)

## Troubleshooting

- **Bot PR not merging** — check `validate.yml` status and `pr-reviews.jsonl`
  for the recorded reason.
- **README check fails** — a data file changed without regenerating; run
  `python3 scripts/generate_readme.py`.
- **Telegram send fails** — verify the bot is a channel admin and the token in
  `~/.openclaw/.env` is current.
