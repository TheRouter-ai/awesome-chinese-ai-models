# Awesome Chinese AI Models — Operations & Growth Plan

Version: V1 · Status: active

## Strategic positioning

This repository is **not** a model list, a ranking, or a generic "awesome list".

It is **the entry point for global developers to understand, compare, and
access China's AI model ecosystem**.

Tagline: *Global guide to China's AI model ecosystem.*

The real goal is not stars. It is to become **the first GitHub page an
overseas developer thinks of when they search for Chinese AI models**.

## Core narrative

The narrative is **global access to emerging AI ecosystems** — information
transparency, global access, developer-friendliness, multi-model choice, cost
optimization.

We provide an **access layer**, not an ideology. Keep all content:

- factual and source-driven
- vendor-neutral
- non-political, non-nationalistic, non-adversarial

Banned framing: "China AI #1", hype words (`最强`, `吊打`, `遥遥领先`,
`全球第一`). See `CONTRIBUTING.md`.

## Two-layer automation architecture

```
Layer 1 — GitHub Actions (deterministic data pipeline)
  daily-update.yml   : discover → score → dedupe → news.yaml → newsletter
                       → regenerate README → open bot PR
  validate.yml       : schema / tests / README consistency
  weekly-rollup.yml  : aggregate the week's news into a weekly draft

Layer 2 — OpenClaw agent `acam-curator` (LLM judgment, editorial, distribution)
  A. PR quality gate + auto-merge
  B. Stable curation (digest items → models.yaml / collections)
  C. Editorial sections (comparison / availability / best-for / access / faq)
  D. Weekly digest writing
  E. Multi-channel distribution (Telegram, X, Reddit/HN drafts)
  F. SEO operations
```

Division of labor: Actions move data deterministically; OpenClaw does the work
that needs judgment and writing. See `docs/operations/openclaw-agent.md`.

## Repository structure

The README is assembled from `data/*.yaml` through `scripts/generate_readme.py`.
Editorial sections are AUTO-GENERATED blocks backed by data files, so even
hand-curated content stays machine-validated:

| README section | Data file |
| --- | --- |
| Model Comparison | `data/comparison.yaml` |
| How to Access | `data/access_methods.yaml` |
| Best For | `data/best_for.yaml` |
| Global Availability | `data/availability.yaml` |
| Benchmarks | `data/benchmarks.yaml` |
| FAQ | `data/faq.yaml` |
| Latest Updates | `data/news.yaml` (auto) |
| Providers / Featured Models | `data/providers.yaml`, `data/models.yaml` |

Never edit AUTO-GENERATED blocks by hand. Edit the data file, then run
`python3 scripts/generate_readme.py`.

## SEO strategy

Target keywords (must appear naturally — no keyword stuffing):
`deepseek api`, `qwen api`, `glm api`, `kimi api`, `china ai models`,
`claude alternative`, `openrouter alternative`, `cheap ai api`.

- **GitHub SEO**: repo topics, commit frequency, issue/discussion activity,
  external links. Topics to set:
  `ai-models llm deepseek qwen glm kimi china-ai ai-api openrouter-alternative`
  (`gh repo edit --add-topic ...`).
- **Google SEO**: long README, comparison tables, FAQ, regular updates.

## Growth phases

| Phase | Stars | Goal | Key actions |
| --- | --- | --- | --- |
| 1 | 0–100 | Credibility | Daily updates, comparison/availability/FAQ sections, GitHub topics, Discussions |
| 2 | 100–1000 | Search traffic | Telegram channel, weekly digest, posts on Reddit / HN / X / Habr |
| 3 | 1000+ | Industry entry point | Automated benchmarks, provider comparison, model explorer, route to TheRouter |

## Distribution channels

- **Telegram** — `@ChineseAIModels` broadcast channel for new models, pricing
  changes, benchmark updates. Primary channel. See `openclaw-agent.md`.
- **Weekly digest** — `newsletters/weekly/YYYY-Www.md`, "This Week in China AI Models".
- **X / Reddit / Hacker News** — drafts prepared by the agent for human review.

## Long-term evolution

Repo → model database site → global access portal → routing/access layer.
The durable value is the **access and awareness layer**: models, vendors, and
prices change, but the entry point compounds.
