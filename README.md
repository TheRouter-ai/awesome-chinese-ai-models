# Awesome Chinese AI Models

> **A global guide to China's AI model ecosystem.**
> Discover, compare, and access leading AI models developed in China.

Chinese AI labs — DeepSeek, Qwen, GLM, Kimi, MiniMax, ERNIE, Hunyuan — now ship
some of the most capable and cost-efficient models available, and many are
open-weight. But for developers outside China, the ecosystem is hard to
navigate: scattered docs, unclear pricing, uncertain global availability.

This repository is a curated, continuously updated entry point. It covers:

- **Model comparison** — capabilities, context windows, open weights
- **How to access** — official APIs, routing gateways, and self-hosting
- **Best-for guidance** — which model fits which workload
- **Global availability** — where these models can be reached, and how to pay
- **Benchmarks** — aggregated from established leaderboards
- **Daily updates** — releases, API changes, and ecosystem news

中文：一个持续更新的中国 AI 模型索引——对比、接入方式、全球可用性、benchmark 和每日生态新闻。
Maintained by [TheRouter.ai](https://therouter.ai/?_tk=Z30eO1Ub) for the global developer community.

## Contents

- [Model Comparison](#model-comparison)
- [How to Access](#how-to-access)
- [Best For](#best-for)
- [Global Availability](#global-availability)
- [Benchmarks](#benchmarks)
- [Latest Updates](#latest-updates)
- [Model Providers](#model-providers)
- [Featured Models](#featured-models)
- [Collections](#collections)
- [Machine-readable Data](#machine-readable-data)
- [Contributing](#contributing)

## Model Comparison

A quick map of the major Chinese AI model families. DeepSeek is a popular
low-cost alternative for coding workloads; Qwen ships strong multilingual
open-weight models; GLM and Kimi focus on reasoning and long context.

<!-- AUTO-GENERATED:START comparison-table -->
| Model | Best For | Context | Vision | Reasoning | API | Open Weights |
| --- | --- | --- | --- | --- | --- | --- |
| DeepSeek | Low-cost coding and reasoning | 128K | — | ✅ | ✅ | ✅ |
| Qwen | Multilingual and open-weight deployment | 256K | ✅ | ✅ | ✅ | ✅ |
| GLM | Chinese reasoning and agent workflows | 128K | ✅ | ✅ | ✅ | ✅ |
| Kimi | Long-context document workloads | 256K | — | ✅ | ✅ | — |
| MiniMax | Long-context, audio, and video generation | 1M | ✅ | ✅ | ✅ | ✅ |
| ERNIE | Enterprise deployment on Baidu Cloud | 128K | ✅ | ✅ | ✅ | ✅ |
| Hunyuan | Multimodal generation including 3D world models | 256K | ✅ | ✅ | ✅ | ✅ |
| Doubao | Multimodal agents on Volcengine Ark | 256K | ✅ | ✅ | ✅ | — |
<!-- AUTO-GENERATED:END comparison-table -->

Context windows and capabilities are best-effort and change often. Always
verify with the official provider.

## How to Access

There are several ways to use Chinese AI models. This section stays
vendor-neutral — official APIs, third-party aggregators, and self-hosting are
listed side by side so you can choose what fits your project.

<!-- AUTO-GENERATED:START how-to-access -->
- **Official API** — Call the provider's own API directly.
  - Best for: Production workloads that need first-party SLAs, billing, and the newest model versions.
  - Each provider has its own endpoint, pricing, and regional availability. Most expose an OpenAI-compatible mode.
- **[TheRouter](https://therouter.ai/)** — An OpenAI-compatible routing gateway with fallback and cost controls.
  - Best for: Teams that want one endpoint across multiple Chinese and global models, with routing and accounting.
  - Maintained by TheRouter.ai, the maintainer of this repository. Listed as one option among several.
- **[OpenRouter](https://openrouter.ai/)** — A third-party aggregator that exposes many models behind one API.
  - Best for: Quick experimentation across providers without separate accounts.
  - Independent third party. Coverage and pricing of Chinese models varies.
- **Self-host** — Run open-weight models on your own infrastructure.
  - Best for: Data residency requirements, offline use, and full control over inference.
  - Only available for models that release open weights. Inference stacks include vLLM, SGLang, and llama.cpp.
<!-- AUTO-GENERATED:END how-to-access -->

## Best For

Developers new to Chinese AI models often ask which one to start with. This
mapping is a starting point, not a ranking — benchmark on your own workload
before committing.

<!-- AUTO-GENERATED:START best-for -->
- **DeepSeek**
  - Low-cost coding workloads
  - A cost-efficient alternative for reasoning tasks
- **Qwen**
  - Multilingual applications
  - Open-weight self-hosting and fine-tuning
  - Terminal coding agents (Qwen-Code)
- **GLM**
  - Chinese-language reasoning
  - Agent and tool-use workflows
- **Kimi**
  - Long-context document analysis
  - Retrieval-heavy workflows
- **MiniMax**
  - Very long context windows
  - Audio and video generation
- **ERNIE**
  - Enterprise integration on Baidu Cloud
  - PaddlePaddle-based deployment
- **Hunyuan**
  - Multimodal generation, including 3D assets
  - Integration with Tencent Cloud
- **Doubao**
  - Multimodal agents via Volcengine Ark
  - High-throughput production workloads
<!-- AUTO-GENERATED:END best-for -->

## Global Availability

Where can developers outside China actually reach these models, and how can
they pay? This is one of the hardest things to find out — and one of the most
useful.

<!-- AUTO-GENERATED:START global-availability -->
| Provider | Global API | Russia | Middle East | Southeast Asia | Crypto Payment |
| --- | --- | --- | --- | --- | --- |
| DeepSeek | ? | ? | ? | ? | — |
| Qwen | ? | ? | ? | ? | — |
| GLM | ? | ◐ | ◐ | ? | — |
| Kimi | ◐ | ? | ? | ◐ | — |
| MiniMax | ? | ◐ | ◐ | ? | — |
| ERNIE | ◐ | ? | ? | ◐ | — |
| Hunyuan | ◐ | ? | ? | ◐ | — |
| Doubao | ◐ | ? | ◐ | ? | — |

Legend: ✅ available · ◐ partial · — not available · ? unverified.
Availability changes often. Always verify with the provider.
<!-- AUTO-GENERATED:END global-availability -->

## Benchmarks

This repo does not invent benchmarks. It points to established leaderboards
and reports, with notes on how each covers Chinese AI models.

<!-- AUTO-GENERATED:START benchmarks -->
- [LMArena (Chatbot Arena)](https://lmarena.ai/) — Human-preference Elo rankings; includes major Chinese models.
  - Crowd-voted; useful for general quality signal, not task-specific performance.
- [Artificial Analysis](https://artificialanalysis.ai/) — Quality, speed, and price comparisons across providers.
  - Good for cost and latency trade-offs; tracks Chinese models alongside global ones.
- [OpenCompass](https://opencompass.org.cn/) — Open-source evaluation suite with strong Chinese-language task coverage.
  - Maintained by Shanghai AI Lab; broad academic benchmark coverage.
- [SuperCLUE](https://www.superclueai.com/) — Chinese-language general benchmark.
  - Chinese-language focus; verify test version and date.
- [Hugging Face Leaderboards](https://huggingface.co/collections) — Task-specific community leaderboards (coding, reasoning, embeddings).
  - Coverage varies by leaderboard; check maintainer and methodology.
<!-- AUTO-GENERATED:END benchmarks -->

## Latest Updates

<!-- AUTO-GENERATED:START latest-news -->
- 2026-07-06 `model_update` [Hugging Face model update: tencent/HunyuanOCR](https://huggingface.co/tencent/HunyuanOCR) — Model card/update on Hugging Face. Tags: transformers, safetensors, hunyuan_vl, image-text-to-text, ocr, vision-language-model, document-parsing, text-spotting
- 2026-07-06 `open_source` [QwenLM/qwen-code release Release v0.19.6-nightly.20260706.47f62a466](https://github.com/QwenLM/qwen-code/releases/tag/v0.19.6-nightly.20260706.47f62a466) — <!-- Release notes generated using configuration in .github/release.yml at release/v0.19.6-nightly.20260706.47f62a466 -->  ## What's Changed * fix(triage): strengthen PR gate with batch detection, problem existence check, and red flag patte
- 2026-07-05 `open_source` [QwenLM/qwen-code release Release v0.19.6-nightly.20260705.015ee4248](https://github.com/QwenLM/qwen-code/releases/tag/v0.19.6-nightly.20260705.015ee4248) — <!-- Release notes generated using configuration in .github/release.yml at release/v0.19.6-nightly.20260705.015ee4248 -->  ## What's Changed * fix(triage): strengthen PR gate with batch detection, problem existence check, and red flag patte
- 2026-07-04 `model_update` [Hugging Face model update: tencent/Ex-Omni](https://huggingface.co/tencent/Ex-Omni) — Model card/update on Hugging Face. Tags: safetensors, qwen3, arxiv:2602.07106, region:us
- 2026-07-04 `open_source` [QwenLM/qwen-code release Release v0.19.6-nightly.20260704.5dc2e1501](https://github.com/QwenLM/qwen-code/releases/tag/v0.19.6-nightly.20260704.5dc2e1501) — <!-- Release notes generated using configuration in .github/release.yml at release/v0.19.6-nightly.20260704.5dc2e1501 -->  ## What's Changed * fix(triage): strengthen PR gate with batch detection, problem existence check, and red flag patte
- 2026-07-03 `open_source` [QwenLM/qwen-code release Release v0.19.6](https://github.com/QwenLM/qwen-code/releases/tag/v0.19.6) — <!-- Release notes generated using configuration in .github/release.yml at release/v0.19.6 -->  ## What's Changed * fix(web-shell): cut mobile session-switch jank (memoized timeline signature, replay-first dispatch) by @qqqys in https://git
- 2026-07-03 `open_source` [QwenLM/qwen-code release Release v0.19.5-nightly.20260703.b16baf1ff](https://github.com/QwenLM/qwen-code/releases/tag/v0.19.5-nightly.20260703.b16baf1ff) — <!-- Release notes generated using configuration in .github/release.yml at release/v0.19.5-nightly.20260703.b16baf1ff -->  ## What's Changed * fix(web-shell): cut mobile session-switch jank (memoized timeline signature, replay-first dispatc
- 2026-07-02 `open_source` [QwenLM/qwen-code release Release v0.19.4-nightly.20260702.46814e4f1](https://github.com/QwenLM/qwen-code/releases/tag/v0.19.4-nightly.20260702.46814e4f1) — <!-- Release notes generated using configuration in .github/release.yml at release/v0.19.4-nightly.20260702.46814e4f1 -->  ## What's Changed * feat(cli): Harden daemon-managed channel worker by @doudouOUC in https://github.com/QwenLM/qwen-c
- 2026-07-02 `open_source` [QwenLM/qwen-code release Release v0.19.5](https://github.com/QwenLM/qwen-code/releases/tag/v0.19.5) — <!-- Release notes generated using configuration in .github/release.yml at release/v0.19.5 -->  ## What's Changed * feat(cli): Harden daemon-managed channel worker by @doudouOUC in https://github.com/QwenLM/qwen-code/pull/6098 * fix(web-she
- 2026-07-01 `open_source` [QwenLM/qwen-code release Release v0.19.3-nightly.20260701.a974594d7](https://github.com/QwenLM/qwen-code/releases/tag/v0.19.3-nightly.20260701.a974594d7) — <!-- Release notes generated using configuration in .github/release.yml at release/v0.19.3-nightly.20260701.a974594d7 -->  ## What's Changed * docs(daemon): refresh daemon docs for recent PRs (wave 2) by @doudouOUC in https://github.com/Qwe
<!-- AUTO-GENERATED:END latest-news -->

See [`newsletters/latest.md`](newsletters/latest.md) for the full daily digest.

## Model Providers

<!-- AUTO-GENERATED:START providers -->
- [DeepSeek / 深度求索](https://www.deepseek.com/) — llm, reasoning, coding, open-weights.
- [Alibaba Qwen / 通义千问](https://qwenlm.github.io/) — llm, multimodal, coding, open-weights.
- [Zhipu AI / 智谱 AI](https://www.zhipuai.cn/) — llm, multimodal, coding.
- [Moonshot AI / 月之暗面](https://www.moonshot.cn/) — llm, long-context.
- [MiniMax](https://www.minimaxi.com/) — llm, audio, video, agent.
- [Baidu ERNIE / 百度文心](https://yiyan.baidu.com/) — llm, enterprise, paddlepaddle.
- [Tencent Hunyuan / 腾讯混元](https://hunyuan.tencent.com/) — llm, multimodal, 3d.
- [ByteDance Doubao / Volcengine Ark / 字节豆包 / 火山方舟](https://www.doubao.com/) — llm, multimodal, agent.
- [OpenBMB (MiniCPM) / 清华 & 面壁智能](https://www.openbmb.cn/) — llm, multimodal, on-device, open-weights.
- [InternLM (Shanghai AI Lab) / 书生·浦语 / 上海人工智能实验室](https://internlm.intern-ai.org.cn/) — llm, multimodal, science, open-weights.
<!-- AUTO-GENERATED:END providers -->

## Featured Models

Entries from the machine-readable registry in `data/models.yaml`:

<!-- AUTO-GENERATED:START featured-models -->
| Model | Provider | Type | Access | Open Weights | Official |
| --- | --- | --- | --- | --- | --- |
| [DeepSeek-V3](https://www.deepseek.com/) | DeepSeek | chat, reasoning, coding | api / web / weights / local-deploy / openai_compatible | Yes | [Source](https://www.deepseek.com/) |
| [Qwen3](https://qwenlm.github.io/) | Alibaba Qwen | chat, reasoning, coding | api / web / weights / local-deploy / openai_compatible | Yes | [Source](https://qwenlm.github.io/) |
| [GLM-4](https://www.bigmodel.cn/) | Zhipu AI | chat, reasoning, coding | api / web / openai_compatible | No | [Source](https://www.bigmodel.cn/) |
| [Kimi](https://www.moonshot.cn/) | Moonshot AI | chat, long-context | api / web / openai_compatible | No | [Source](https://www.moonshot.cn/) |
| [Qwen-Code](https://github.com/QwenLM/qwen-code) | Alibaba Qwen | coding, agent-tool-use | weights / local-deploy | Yes | [Source](https://github.com/QwenLM/qwen-code) |
| [HY-World 2.0](https://github.com/Tencent-Hunyuan/HY-World-2.0) | Tencent Hunyuan | image-generation, video-generation | weights / local-deploy | Yes | [Source](https://github.com/Tencent-Hunyuan/HY-World-2.0) |
| [MiniCPM-V 4](https://github.com/OpenBMB/MiniCPM-V) | OpenBMB (MiniCPM) | chat, vision-language, reasoning | weights / local-deploy | Yes | [Source](https://github.com/OpenBMB/MiniCPM-V) |
| [Intern-S2-Preview](https://github.com/InternLM/Intern-S1) | InternLM (Shanghai AI Lab) | chat, vision-language, reasoning | weights / local-deploy | Yes | [Source](https://github.com/InternLM/Intern-S1) |
| [Qwen3.6](https://qwenlm.github.io/) | Alibaba Qwen | chat, reasoning, coding | weights / local-deploy | Yes | [Source](https://qwenlm.github.io/) |
| [VoxCPM](https://github.com/OpenBMB/VoxCPM) | OpenBMB (MiniCPM) | audio-speech | weights / local-deploy | Yes | [Source](https://github.com/OpenBMB/VoxCPM) |
| [Hy-MT2](https://github.com/Tencent-Hunyuan/Hy-MT2) | Tencent Hunyuan | translation | weights / local-deploy | Yes | [Source](https://github.com/Tencent-Hunyuan/Hy-MT2) |
| [HunyuanOCR](https://github.com/Tencent-Hunyuan/HunyuanOCR) | Tencent Hunyuan | ocr | weights / local-deploy | Yes | [Source](https://github.com/Tencent-Hunyuan/HunyuanOCR) |
<!-- AUTO-GENERATED:END featured-models -->

## Collections

- [`collections/open-source-models.md`](collections/open-source-models.md) — open-weight Chinese AI models.
- [`collections/api-accessible-models.md`](collections/api-accessible-models.md) — models available through APIs.
- [`collections/multimodal-models.md`](collections/multimodal-models.md) — VLM, image, video, audio, and 3D models.
- [`collections/coding-models.md`](collections/coding-models.md) — code generation and software engineering models.
- [`collections/agent-models.md`](collections/agent-models.md) — tool-use, agent, browser, and workflow models.
- [`collections/embedding-rerank.md`](collections/embedding-rerank.md) — embedding and reranker models.
- [`collections/therouter-supported.md`](collections/therouter-supported.md) — Chinese models available or tracked for TheRouter access.

## Machine-readable Data

The canonical registry lives in `data/`:

- `data/models.yaml` — model index
- `data/providers.yaml` — provider index
- `data/comparison.yaml` — model comparison matrix
- `data/access_methods.yaml` — how-to-access options
- `data/best_for.yaml` — best-for mapping
- `data/availability.yaml` — global availability matrix
- `data/benchmarks.yaml` — aggregated benchmark sources
- `data/faq.yaml` — frequently asked questions
- `data/news.yaml` — daily updates and news events
- `data/resources.yaml` — official resources, docs, model cards, tutorials
- `data/capabilities.yaml` — normalized capability taxonomy
- `data/use_cases.yaml` — reproducible playbooks and workflows

Run local validation:

```bash
python3 scripts/validate_data.py
python3 scripts/generate_readme.py --check
```

## FAQ

<!-- AUTO-GENERATED:START faq -->
### What are Chinese AI models?

AI models developed by organizations based in China, such as DeepSeek, Qwen (Alibaba), GLM (Zhipu AI), Kimi (Moonshot AI), MiniMax, ERNIE (Baidu), and Hunyuan (Tencent). Many are released with open weights and expose OpenAI-compatible APIs.

### Which Chinese AI model is best for coding?

DeepSeek and Qwen are commonly used for coding workloads, often as a lower-cost alternative to closed models. Compare them on a coding benchmark and on your own tasks before committing.

### Are Chinese AI models open source?

Many are open-weight: DeepSeek, Qwen, GLM, and MiniMax publish weights on Hugging Face and ModelScope. Some, such as Kimi and Doubao, are API-only. Check the license of each specific model before deployment.

### How can I access Chinese AI models from outside China?

Three common paths: call the provider's official API, use an OpenAI-compatible aggregator such as TheRouter or OpenRouter, or self-host open-weight models. See the "How to Access" section.

### Are Chinese AI models OpenAI-compatible?

Most major providers expose an OpenAI-compatible API mode, so existing OpenAI SDK code usually works with a changed base URL and API key. Confirm supported parameters in each provider's documentation.

### Are Chinese AI models cheaper than GPT or Claude?

Several Chinese models are priced below comparable closed models, which is why developers evaluate them as cost-efficient alternatives. Pricing changes frequently — verify current rates on the provider's pricing page.
<!-- AUTO-GENERATED:END faq -->

## Contributing

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening an issue or PR.

Minimum requirements:

- Prefer official sources: websites, docs, GitHub, Hugging Face, ModelScope, papers, or changelogs.
- Include source URL, category, date, and why the entry belongs here.
- Keep descriptions factual and neutral. Avoid unverified claims such as “最强”, “吊打”, or “全球第一”.
- Do not submit random mirrors, SEO spam, unverifiable screenshots, cracked products, or gray-market workflows.

## TheRouter

TheRouter.ai provides an OpenAI-compatible access layer for multiple AI models,
with routing, fallback, and cost-control workflows. It is listed in
[How to Access](#how-to-access) as one option among several. This repo stays
source-driven and vendor-neutral; entries must remain community-useful.

## Disclaimer

This is a community-maintained index. Always verify model availability,
pricing, licensing, and benchmark claims with the official provider.
