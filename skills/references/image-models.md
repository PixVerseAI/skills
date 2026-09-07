# Image model fallback reference

Read when installed capability discovery is unavailable or to compare model-specific limits. This static reference describes CLI 1.4.0, not necessarily the installed version.

### Model Reference

On CLI v1.4.0 or later, query `pixverse capabilities create image [--model <id>] --json` for installed flags and constraints. Check `pixverse --version` once per session. On older versions, use `pixverse create image --help` with the table below as a fallback; newer models or flags may be unavailable.

| Model | `--model` value | Resolution | Aspect Ratio | Max I2I refs |
|:---|:---|:---|:---|---:|
| GPT Image 2 | `gpt-image-2.0` (default) | `1080p` `1440p` `2160p` | `1:1` `16:9` `9:16` `4:3` `3:4` `3:2` `2:3` `2:1` `1:2` `21:9` | 9 |
| Qwen Image | `qwen-image` | `720p` `1080p` | `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 3 |
| Seedream 5.0 Pro | `seedream-5.0-pro` | `1080p` `1440p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 10 |
| Seedream 5.0 Lite | `seedream-5.0-lite` | `1440p` `1800p` `2160p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 6 |
| Seedream 4.5 | `seedream-4.5` | `1440p` `2160p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 6 |
| Seedream 4.0 | `seedream-4.0` | `1080p` `1440p` `2160p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 6 |
| Gemini 2.5 Flash (aka Nanobanana) | `gemini-2.5-flash` | `1080p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 3 |
| Gemini 3.0 (aka Nano Banana Pro) | `gemini-3.0` | `1080p` `1440p` `2160p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 9 |
| Gemini 3.1 Flash (aka Nano Banana 2) | `gemini-3.1-flash` | `512p` `1080p` `1440p` `2160p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 9 |
| Gemini 3.1 Flash Lite (aka Nano Banana 2 Lite) | `gemini-3.1-flash-lite` | `1080p` | `auto` `1:1` `3:2` `2:3` `3:4` `4:3` `4:5` `5:4` `9:16` `16:9` `21:9` | 14 |
| Kling Image O3 | `kling-image-o3` | `1080p` `1440p` `2160p` | `16:9` `9:16` `1:1` `4:3` `3:4` `3:2` `2:3` `21:9` | 10 |
| Kling Image V3 | `kling-image-v3` | `1080p` `1440p` | `16:9` `9:16` `1:1` `4:3` `3:4` `3:2` `2:3` `21:9` | 1 |

> **Recommended:** The default is `gpt-image-2.0` (up to `2160p`; `--detail-level` defaults to `low`). For the widest resolution/aspect-ratio range prefer `gemini-3.1-flash` (up to `2160p`) or `seedream-5.0-lite` (up to `2160p`). Use `seedream-5.0-pro` when you need up to 10 I2I references at `1080p` / `1440p`, and `qwen-image` when you want a fast, lighter model (capped at `1080p`). In `--region cn`, the default is `qwen-image` and only `qwen-image`, `seedream-5.0-lite`, `seedream-4.5`, and `seedream-4.0` are available.

> **Important:** Each model only accepts specific quality and aspect-ratio values. The CLI adjusts unsupported values to a model-valid fallback and writes a warning to stderr; choose from the table to avoid silent parameter changes.
