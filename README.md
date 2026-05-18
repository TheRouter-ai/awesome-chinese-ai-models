# Awesome Chinese AI Models

A curated, machine-readable index of Chinese AI models, capabilities, official resources, and ecosystem updates.

中文：一个持续更新的中国 AI 模型、能力、玩法、新闻和官方资源索引。Maintained by TheRouter.ai for developers and the Chinese AI community.

> Scope: Chinese AI models, Chinese-capable model infrastructure, official resources, open-source releases, benchmarks, APIs, product capabilities, and reproducible playbooks.

## Quick Links

- [Latest Updates](#latest-updates)
- [Featured Models](#featured-models)
- [Model Providers](#model-providers)
- [Capabilities](#capabilities)
- [Collections](#collections)
- [Machine-readable Data](#machine-readable-data)
- [Contributing](#contributing)

## Latest Updates

<!-- AUTO-GENERATED:START latest-news -->
- 2026-05-18 `api_update` [TheRouter supported model page: zhipu/cogvideox-3](https://therouter.ai/models/zhipu--cogvideox-3) — TheRouter model page with model introduction and OpenAI-compatible access details.
- 2026-05-18 `api_update` [TheRouter supported model page: alibaba/cosyvoice2-0.5b](https://therouter.ai/models/alibaba--cosyvoice2-0.5b) — TheRouter model page with model introduction and OpenAI-compatible access details.
- 2026-05-18 `api_update` [TheRouter supported model page: zhipu/cogvideox-flash](https://therouter.ai/models/zhipu--cogvideox-flash) — TheRouter model page with model introduction and OpenAI-compatible access details.
- 2026-05-18 `api_update` [TheRouter supported model page: zhipu/cogview-4](https://therouter.ai/models/zhipu--cogview-4) — TheRouter model page with model introduction and OpenAI-compatible access details.
- 2026-05-18 `api_update` [TheRouter supported model page: zhipu/cogview-3-flash](https://therouter.ai/models/zhipu--cogview-3-flash) — TheRouter model page with model introduction and OpenAI-compatible access details.
- 2026-05-18 `open_source` [QwenLM/qwen-code release Release v0.15.11-nightly.20260518.f44ed0941](https://github.com/QwenLM/qwen-code/releases/tag/v0.15.11-nightly.20260518.f44ed0941) — ## What's Changed * feat(cli): wrap markdown links in OSC 8 so wrapped URLs stay clickable by @BZ-D in https://github.com/QwenLM/qwen-code/pull/4037 * fix(core): normalize cumulative OpenAI stream deltas to suffixes by @chiga0 in https://gi
- 2026-05-18 `model_update` [Hugging Face model update: openbmb/BitCPM4-CANN-8B-unquantized](https://huggingface.co/openbmb/BitCPM4-CANN-8B-unquantized) — Model card/update on Hugging Face. Tags: transformers, pytorch, minicpm, text-generation, conversational, custom_code, zh, en
- 2026-05-18 `model_update` [Hugging Face model update: openbmb/BitCPM4-CANN-3B-unquantized](https://huggingface.co/openbmb/BitCPM4-CANN-3B-unquantized) — Model card/update on Hugging Face. Tags: transformers, pytorch, llama, text-generation, conversational, custom_code, zh, en
- 2026-05-18 `model_update` [Hugging Face model update: openbmb/BitCPM4-CANN-3B](https://huggingface.co/openbmb/BitCPM4-CANN-3B) — Model card/update on Hugging Face. Tags: transformers, pytorch, llama, text-generation, conversational, zh, en, license:apache-2.0
- 2026-05-18 `model_update` [Hugging Face model update: openbmb/BitCPM4-CANN-1B-unquantized](https://huggingface.co/openbmb/BitCPM4-CANN-1B-unquantized) — Model card/update on Hugging Face. Tags: transformers, pytorch, llama, text-generation, conversational, custom_code, zh, en
<!-- AUTO-GENERATED:END latest-news -->

## Featured Models

<!-- AUTO-GENERATED:START featured-models -->
| Model | Provider | Type | Access | Open Weights | Official |
| --- | --- | --- | --- | --- | --- |
| [DeepSeek-V3](https://www.deepseek.com/) | DeepSeek | chat, reasoning, coding | api / web / weights / local-deploy / openai_compatible | Yes | [Source](https://www.deepseek.com/) |
| [Qwen3](https://qwenlm.github.io/) | Alibaba Qwen | chat, reasoning, coding | api / web / weights / local-deploy / openai_compatible | Yes | [Source](https://qwenlm.github.io/) |
| [GLM-4](https://www.bigmodel.cn/) | Zhipu AI | chat, reasoning, coding | api / web / openai_compatible | No | [Source](https://www.bigmodel.cn/) |
| [Kimi](https://www.moonshot.cn/) | Moonshot AI | chat, long-context | api / web / openai_compatible | No | [Source](https://www.moonshot.cn/) |
<!-- AUTO-GENERATED:END featured-models -->

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
<!-- AUTO-GENERATED:END providers -->

## Capabilities

- Text LLMs and reasoning models
- Coding models
- Vision-language models
- Image / video / 3D generation
- Audio, speech recognition, and TTS
- Embedding and reranking models
- Agent and tool-use capabilities
- Long-context and retrieval workflows
- Local deployment, quantization, and inference stacks
- API routing, fallback, evaluation, and cost optimization

## Collections

- `collections/open-source-models.md` — open-weight Chinese AI models.
- `collections/api-accessible-models.md` — models available through APIs.
- `collections/multimodal-models.md` — VLM, image, video, audio, and 3D models.
- `collections/coding-models.md` — code generation and software engineering models.
- `collections/agent-models.md` — tool-use, agent, browser, and workflow models.
- `collections/embedding-rerank.md` — embedding and reranker models.
- `collections/therouter-supported.md` — Chinese models available or tracked for TheRouter access.
- `newsletters/latest.md` — latest daily digest.

## Machine-readable Data

The canonical registry lives in `data/`:

- `data/models.yaml` — model index
- `data/providers.yaml` — provider index
- `data/news.yaml` — daily updates and news events
- `data/resources.yaml` — official resources, docs, model cards, tutorials
- `data/capabilities.yaml` — normalized capability taxonomy
- `data/benchmarks.yaml` — benchmark claims and sources
- `data/use_cases.yaml` — reproducible playbooks and workflows

Schemas and validation live in `schema/` and `scripts/`.

Run local validation:

```bash
python3 scripts/validate_data.py
python3 scripts/generate_readme.py --check
```

## Contributing

Please read `CONTRIBUTING.md` before opening an issue or PR.

Minimum requirements:

- Prefer official sources: websites, docs, GitHub, Hugging Face, ModelScope, papers, or changelogs.
- Include source URL, category, date, and why the entry belongs here.
- Keep descriptions factual and neutral. Avoid unverified claims such as “最强”, “吊打”, or “全球第一”.
- Do not submit random mirrors, SEO spam, unverifiable screenshots, cracked products, or gray-market workflows.

## TheRouter

TheRouter.ai provides an OpenAI-compatible access layer for multiple AI models, with routing, fallback, and cost-control workflows. This repo may include TheRouter-specific collections when they help developers compare and use Chinese AI models, but entries should remain source-driven and community-useful.

## Disclaimer

This is a community-maintained index. Always verify model availability, pricing, licensing, and benchmark claims with the official provider.
