# Image model fallback reference

Read when installed capability discovery is unavailable or to compare model-specific limits. This static reference describes CLI 1.4.1, not necessarily the installed version.

### Model Reference

On CLI v1.4.0 or later, query `pixverse capabilities create image [--model <id>] --json` for installed flags and constraints. Check `pixverse --version` once per session. On older versions, use `pixverse create image --help` with the table below as a fallback; newer models or flags may be unavailable.

| Model | `--model` value | Resolution | Aspect Ratio | Max I2I refs |
|:---|:---|:---|:---|---:|
| GPT Image 2.5 Flare | `gpt-image-2.5-flare` (global default, CLI 1.4.1+) | `1080p` `1440p` `2160p` | Quality-dependent; see table below | 16 |
| GPT Image 2.5 Sunburst | `gpt-image-2.5-sunburst` (CLI 1.4.1+) | `1080p` `1440p` `2160p` | Quality-dependent; see table below | 16 |
| GPT Image 2 | `gpt-image-2.0` | `1080p` `1440p` `2160p` | `1:1` `16:9` `9:16` `4:3` `3:4` `3:2` `2:3` `2:1` `1:2` `21:9` | 9 |
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

### GPT Image 2.5 quality-dependent framing

Flare and Sunburst share the same limits. Select quality first, then a ratio from that quality's row; the union of ratios in the base capability is not a valid combination matrix.

| Quality flag | Allowed ratios | Omitted ratio with built-in defaults |
|:---|:---|:---|
| `1080p` | `1:1`, `3:2`, `2:3` | `1:1` |
| `1440p` | `1:1`, `16:9`, `9:16` | `16:9` |
| `2160p` | `16:9`, `9:16` | `16:9` |

`1K` is an interactive label for `1080p`, not a quality flag value. A supported saved aspect-ratio default is preserved. An explicitly unsupported ratio warns and falls back to `1:1` at 1080p/1440p or `16:9` at 2160p; this differs from omitting the ratio at 1440p. Choose explicit valid pairs when framing matters. For a 2160p square or 2:3 poster, choose another compatible model rather than assuming GPT Image 2.5 supports it.

Both 2.5 models accept detail levels `low` (default), `medium`, `high`, `xhigh`, and `max`. GPT Image 2.0 retains only `low`, `medium`, and `high`; other image models reject `--detail-level`. The 16-reference limit is validated before upload and is separate from the 1–4 output `--count` limit.

The global built-in default in CLI 1.4.1 is `gpt-image-2.5-flare`, `1080p`, `1:1`, detail `low`; explicit flags and saved creation defaults can override it. GPT Image 2.0 remains available explicitly. For wider ratio choices at high resolution, check Gemini or Seedream's rows above. In `--region cn`, the default remains `qwen-image`; only `qwen-image`, `seedream-5.0-lite`, `seedream-4.5`, and `seedream-4.0` are available. Neither GPT Image 2.5 variant is available in CN.

Unsupported quality/ratio values are adjusted with a warning on stderr. Unsupported models or detail levels are validation errors; do not retry them as transient generation failures.
