# Image model fallback reference

Read when installed capability discovery is unavailable or to compare model-specific limits. This static reference describes CLI 1.4.8, not necessarily the installed version.

### Model Reference

On CLI v1.4.0 or later, query `pixverse capabilities create image [--model <id>] --json` for installed flags and constraints. Check `pixverse --version` once per session. On older versions, use `pixverse create image --help` with the table below as a fallback; newer models or flags may be unavailable.

| Model | `--model` value | Resolution | Aspect Ratio | Max I2I refs |
|:---|:---|:---|:---|---:|
| GPT Image 2.5 Flare | `gpt-image-2.5-flare` (global default, CLI 1.4.1+) | `1080p` `1440p` `2160p` | `1:1` `16:9` `9:16` `4:3` `3:4` `3:2` `2:3` `2:1` `1:2` `21:9` (CLI 1.4.3+) | 16 |
| GPT Image 2.5 Sunburst | `gpt-image-2.5-sunburst` (CLI 1.4.1+) | `1080p` `1440p` `2160p` | `1:1` `16:9` `9:16` `4:3` `3:4` `3:2` `2:3` `2:1` `1:2` `21:9` (CLI 1.4.3+) | 16 |
| GPT Image 2 | `gpt-image-2.0` | `1080p` `1440p` `2160p` | `1:1` `16:9` `9:16` `4:3` `3:4` `3:2` `2:3` `2:1` `1:2` `21:9` | 9 |
| Qwen Image | `qwen-image` | `720p` `1080p` | `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 3 |
| Seedream 5.0 Pro | `seedream-5.0-pro` | `1080p` `1440p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 10 |
| Seedream 5.0 Lite | `seedream-5.0-lite` | `1440p` `1800p` `2160p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 6 |
| Seedream 4.5 | `seedream-4.5` | `1440p` `2160p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 6 |
| Seedream 4.0 | `seedream-4.0` | `1080p` `1440p` `2160p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 6 |
| Gemini 2.5 Flash (aka Nanobanana) | `gemini-2.5-flash` | `1080p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 3 |
| Gemini 3.0 (aka Nano Banana Pro) | `gemini-3.0` | `1080p` `1440p` `2160p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 9 |
| Nano Banana 2.1 | `gemini-nano-banana-2.1` (CLI 1.4.8+, global only) | `1080p` `1440p` `2160p` | `auto` `1:1` `3:2` `2:3` `3:4` `4:3` `4:5` `5:4` `9:16` `16:9` `21:9` `1:4` `4:1` `1:8` `8:1` | 14 |
| Gemini 3.1 Flash (aka Nano Banana 2) | `gemini-3.1-flash` | `512p` `1080p` `1440p` `2160p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 9 |
| Gemini 3.1 Flash Lite (aka Nano Banana 2 Lite) | `gemini-3.1-flash-lite` | `1080p` | `auto` `1:1` `3:2` `2:3` `3:4` `4:3` `4:5` `5:4` `9:16` `16:9` `21:9` | 14 |
| Kling Image O3 | `kling-image-o3` | `1080p` `1440p` `2160p` | `16:9` `9:16` `1:1` `4:3` `3:4` `3:2` `2:3` `21:9` | 10 |
| Kling Image V3 | `kling-image-v3` | `1080p` `1440p` | `16:9` `9:16` `1:1` `4:3` `3:4` `3:2` `2:3` `21:9` | 1 |

### GPT Image 2.5 framing

On CLI **1.4.3+**, Flare and Sunburst accept all ten ratios (`1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `2:1`, `1:2`, `21:9`) at every supported quality (`1080p`, `1440p`, `2160p`). There are no quality-specific aspect-ratio rules. Both `1080p + 9:16` and `2160p + 1:1` are valid; do not upgrade quality or switch models merely to obtain those ratios.

The built-in omitted ratio is `16:9`. Supported explicit or saved ratios are preserved. A ratio outside the model's supported list warns and falls back to `1:1`; unsupported quality still follows the ordinary image-quality fallback. `1K` is an interactive label for `1080p`, not a quality flag value.

**CLI 1.4.2 compatibility:** all qualities accept only `1:1`, `16:9`, `9:16`, `3:2`, and `2:3`; the other five ratios were added in 1.4.3. Do not apply the expanded list to 1.4.2.

**CLI 1.4.1 compatibility:** that version restricted ratios by quality and used a `1:1` built-in default at `1080p`. Use its installed `capability.rules` rather than applying the expanded 1.4.2 combinations. The reference-sheet and Windows examples keep explicit `1440p` framing that works on both versions.

Both 2.5 models accept detail levels `low` (default), `medium`, `high`, `xhigh`, and `max`. GPT Image 2.0 retains only `low`, `medium`, and `high`; Nano Banana 2.1 has its own levels below; remaining image models reject `--detail-level`. The 16-reference limit is validated before upload and is separate from the 1–4 output `--count` limit.

The global built-in default in CLI 1.4.8 is `gpt-image-2.5-flare`, `1080p`, `16:9`, detail `low`; explicit flags and saved creation defaults can override it. GPT Image 2.0 remains available explicitly. For `auto`, `5:4`, or `4:5` framing, check Gemini or Seedream's rows above; these ratios are not supported by GPT Image 2.5. In `--region cn`, the default remains `qwen-image`; only `qwen-image`, `seedream-5.0-lite`, `seedream-4.5`, and `seedream-4.0` are available. Neither GPT Image 2.5 variant is available in CN.

Unsupported quality/ratio values are adjusted with a warning on stderr. Unsupported models or detail levels are validation errors; do not retry them as transient generation failures.

### Nano Banana 2.1

Use `gemini-nano-banana-2.1` for T2I or I2I on CLI **1.4.8+**, in the global region only. Query the installed model capability: builds without its `detail_level` parameter need an upgrade to use that flag.

- `--detail-level` accepts `minimal`, `medium` (default), or `high`. GPT Image's `low`, `xhigh`, and `max` are invalid here; invalid or empty detail values fail before reference upload.
- Shared built-in defaults are `1080p`, `16:9`, and one output for both T2I and I2I. Explicit flags and saved quality/framing/count defaults take precedence; adding an image does not automatically select `auto`. `512p` is unsupported.
- At most 14 references; overflow is rejected before resolving or uploading inputs. Output `--count` is independently 1–4. On CLI 1.4.8+, all image models use that output cap, independently of their reference cap.
- `--seed` is silently ignored for this model, including the implicit default; do not promise seed-based reproducibility.

```bash
pixverse create image --model gemini-nano-banana-2.1 --prompt "A panoramic botanical illustration" --quality 2160p --aspect-ratio 8:1 --detail-level high --json
```
