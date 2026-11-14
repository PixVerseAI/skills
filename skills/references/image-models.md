# Image model fallback reference

Read when installed capability discovery is unavailable or to compare model-specific limits. Prefer `pixverse capabilities create image --model <id> --json`. This static reference describes CLI 1.4.20.

| Model | `--model` value | Resolution | Aspect ratio | Max I2I refs |
|:---|:---|:---|:---|---:|
| GPT Image 2.5 Flare | `gpt-image-2.5-flare` (global default) | `1080p` `1440p` `2160p` | `1:1` `16:9` `9:16` `4:3` `3:4` `3:2` `2:3` `2:1` `1:2` `21:9` | 16 |
| GPT Image 2.5 Sunburst | `gpt-image-2.5-sunburst` | `1080p` `1440p` `2160p` | same as Flare | 16 |
| GPT Image 2 | `gpt-image-2.0` | `1080p` `1440p` `2160p` | same as Flare | 9 |
| Qwen Image | `qwen-image` (CN default) | `720p` `1080p` | `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 3 |
| MiniMax H3 Image | `minimax-h3-image` (CLI 1.4.20+) | `1080p` `1440p` `2160p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 16 |
| Seedream 5.5 | `seedream-5.5` | `1080p` `1.5k` `1440p` `1800p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` | 10 |
| Seedream 5.0 Pro | `seedream-5.0-pro` | `1080p` `1440p` | same as Seedream 5.5 | 10 |
| Seedream 5.0 Lite | `seedream-5.0-lite` | `1440p` `1800p` `2160p` | same as Seedream 5.5 | 6 |
| Seedream 4.5 | `seedream-4.5` | `1440p` `2160p` | same as Seedream 5.5 | 6 |
| Seedream 4.0 | `seedream-4.0` | `1080p` `1440p` `2160p` | same as Seedream 5.5 | 6 |
| Gemini 2.5 Flash (aka Nanobanana) | `gemini-2.5-flash` | `1080p` | same as Seedream 5.5 | 3 |
| Gemini 3.0 (aka Nano Banana Pro) | `gemini-3.0` | `1080p` `1440p` `2160p` | same as Seedream 5.5 | 9 |
| Nano Banana 2.1 | `gemini-nano-banana-2.1` | `1080p` `1440p` `2160p` | Seedream 5.5 ratios plus `1:4` `4:1` `1:8` `8:1` | 14 |
| Gemini 3.1 Flash (aka Nano Banana 2) | `gemini-3.1-flash` | `512p` `1080p` `1440p` `2160p` | same as Seedream 5.5 | 9 |
| Gemini 3.1 Flash Lite (aka Nano Banana 2 Lite) | `gemini-3.1-flash-lite` | `1080p` | same as Seedream 5.5 | 14 |
| Kling Image O3 | `kling-image-o3` | `1080p` `1440p` `2160p` | `16:9` `9:16` `1:1` `4:3` `3:4` `3:2` `2:3` `21:9` | 10 |
| Kling Image V3 | `kling-image-v3` | `1080p` `1440p` | same as Kling Image O3 | 1 |

**Region:** `--region cn` defaults to `qwen-image` and allows only `qwen-image`, `seedream-5.0-lite`, `seedream-4.5`, and `seedream-4.0`. All other models are global only.

## Shared defaults and validation

- The global built-in default is `gpt-image-2.5-flare`. Built-in quality is `1080p` (Seedream 5.0 Lite and 4.5: `1440p`), and framing is `16:9`. Explicit flags and saved creation defaults take precedence. Adding an image does not select `auto`; pass it explicitly where supported.
- Quality aliases are case-insensitive: `1K`=`1080p`, `1.5K`=`1.5k`, `2K`=`1440p`, `3K`=`1800p`, `4K`=`2160p`. They still require model support.
- An unsupported quality or ratio is adjusted with a warning on stderr. Unsupported models, detail levels, or backgrounds are validation errors (exit 6) raised before upload; do not retry them as transient failures.
- Reference caps (above) are validated before upload and are independent of the 1–4 output `--count`.

## Model-specific flags

| Flag | Models | Values |
|:---|:---|:---|
| `--detail-level` | GPT Image 2.5 Flare/Sunburst | `low` (default), `medium`, `high`, `xhigh`, `max` |
| | GPT Image 2.0 | `low`, `medium`, `high` |
| | Nano Banana 2.1 | `minimal`, `medium` (default), `high` |
| `--background` | GPT Image 2.5 Flare/Sunburst, Seedream 5.5 | `auto` (default), `transparent`, `opaque`. The backend chooses the file format, so a transparent background does not guarantee PNG; `--output-format` is rejected. |
| `--output-format` | MiniMax H3 Image only | `png` (default), `jpeg` (`jpg` alias), `webp`; case-insensitive; invalid values fall back to `png` |

Other models reject these flags. GPT Image 2.5 has no quality-specific ratio rules: `1080p + 9:16` is valid; do not upgrade quality or switch models to obtain a ratio. For `auto`, `5:4`, or `4:5`, choose a Gemini, Seedream, Qwen or H3 Image model.

## Model notes

- **Nano Banana 2.1:** `512p` is unsupported, and `--seed` is silently ignored, so seed-based reproducibility cannot be promised.
- **Seedream 5.5:** 4K is unsupported. `--detail-level` is unsupported, and prompts are passed through without a local length cap.
- **MiniMax H3 Image (CLI 1.4.20+):**
  - Framing defaults to `16:9` like other models; pass `--aspect-ratio auto` explicitly to get automatic framing.
  - Prompts must be nonblank and at most 20,000 Unicode code points; invalid prompts fail locally without truncation.
  - `--seed` is accepted but not sent. `--background` and `--detail-level` are unsupported.
  - References must be JPEG/PNG/WebP, at most 64 MiB, with edges of 128–8192 px and a longest/shortest edge ratio of at most 4. Originals are checked before upload compression and again after it. Existing asset IDs are checked against available metadata only.

```bash
pixverse create image --model gemini-nano-banana-2.1 --prompt "A panoramic botanical illustration" --quality 2160p --aspect-ratio 8:1 --detail-level high --json
pixverse create image --model minimax-h3-image --prompt "$PROMPT" --quality 2K --aspect-ratio auto --output-format webp --json
```
