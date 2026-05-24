# Open-source Chinese AI Models

Chinese AI models that publish open weights, downloadable worldwide from
Hugging Face or ModelScope. Verify the license of each specific model before
deployment — "open weights" does not always mean a permissive license.

| Model | Provider | Capabilities | License |
| --- | --- | --- | --- |
| [DeepSeek-V3](https://huggingface.co/deepseek-ai/DeepSeek-V3) | DeepSeek | chat, reasoning, coding | DeepSeek License |
| [Qwen3](https://huggingface.co/Qwen) | Alibaba Qwen | chat, reasoning, coding, long-context | Apache-2.0 / model-specific |
| [Qwen-Code](https://github.com/QwenLM/qwen-code) | Alibaba Qwen | coding CLI agent | Apache-2.0 |
| [MiniCPM-V 4](https://huggingface.co/openbmb/MiniCPM-V-4.6) | OpenBMB | vision-language, on-device | Apache-2.0 |
| [HY-World 2.0](https://huggingface.co/tencent/HY-World-2.0) | Tencent Hunyuan | 3D world model, generation | verify with provider |

## How to run

- **vLLM** / **SGLang** — high-throughput GPU inference servers.
- **llama.cpp** — quantized CPU/GPU inference for smaller models.
- **ModelScope** — mirror of weights with China-region download speed.

This collection is curated by the `acam-curator` agent from `data/models.yaml`.
Submit additions through `CONTRIBUTING.md`.
