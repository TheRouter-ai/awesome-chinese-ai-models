# Multimodal Chinese AI Models

Vision-language, image, video, audio, speech, OCR, and 3D models from Chinese
AI labs.

| Area | Model / Provider | Notes |
| --- | --- | --- |
| Vision-language | Qwen, GLM, Hunyuan, ERNIE, Doubao | VLM input across most major providers. |
| On-device VLM | [MiniCPM-V 4](https://huggingface.co/openbmb/MiniCPM-V-4.6) (OpenBMB) | Apache-2.0; quantized variants (GGUF/AWQ/GPTQ) available; thinking variant released 2026-05. |
| Scientific multimodal | [Intern-S1](https://github.com/InternLM/Intern-S1) (InternLM / Shanghai AI Lab) | Scientific Multimodal Foundation Model; Apache-2.0; open weights. |
| OCR | [HunyuanOCR](https://github.com/Tencent-Hunyuan/HunyuanOCR) (Tencent Hunyuan) | Dedicated OCR model; open weights; verify license with provider. |
| Translation | [Hy-MT2](https://github.com/Tencent-Hunyuan/Hy-MT2) (Tencent Hunyuan) | Machine-translation family (1.8B / 7B / 30B-A3B); zh/en/fr; open weights; arxiv:2512.24092. |
| Image generation | Zhipu (CogView), others | See `data/therouter_model_links.yaml` for tracked models. |
| Video generation | Zhipu (CogVideoX), MiniMax | Video generation APIs. |
| Audio / speech | MiniMax, Alibaba (CosyVoice) | TTS and speech models. |
| 3D world model | [HY-World 2.0](https://github.com/Tencent-Hunyuan/HY-World-2.0) (Tencent Hunyuan) | Multi-modal world model for 3D reconstruction, generation, and simulation; open weights. |
| 3D asset generation | Tencent Hunyuan | Hunyuan 3D asset generation via Tencent Cloud API. |

This collection is curated by the `acam-curator` agent. Submit additions
through `CONTRIBUTING.md`.
