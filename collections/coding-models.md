# Chinese Coding Models

Models commonly used for code generation, completion, review, and software
engineering workloads. Several are evaluated as lower-cost alternatives to
closed coding models — benchmark on your own tasks before committing.

| Model | Provider | Open Weights | Notes |
| --- | --- | --- | --- |
| DeepSeek-V3 | DeepSeek | Yes | Widely used for low-cost coding workloads. |
| Qwen3 | Alibaba Qwen | Yes | Strong multilingual coding; Qwen-Coder variants available. |
| [Qwen-Code](https://github.com/QwenLM/qwen-code) | Alibaba Qwen | Yes (Apache-2.0) | Open-source terminal coding agent built on Qwen3. Runs in CLI; supports tool use. |
| GLM-4 | Zhipu AI | No | Coding with agent and tool-use support. |

## Related tooling

- [`QwenLM/qwen-code`](https://github.com/QwenLM/qwen-code) — open-source terminal coding agent (Apache-2.0). Install via `npm install -g @qwen-code/qwen-code`.

This collection is curated by the `acam-curator` agent. Submit additions
through `CONTRIBUTING.md`.
