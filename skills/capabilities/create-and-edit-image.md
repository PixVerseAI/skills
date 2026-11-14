---
name: pixverse:create-and-edit-image
description: Create images from text (T2I) or edit existing images (I2I) using AI
---

# Create and Edit Image

Use `create image --prompt` for text-to-image. Add `--image` for one reference or `--images` for several references to edit or combine existing images.

Relax flags are accepted; see the [execution contract](../references/execution-contract.md#relax-mode).

## Parameter discovery

Query `pixverse capabilities create image --model <id> --json` for the chosen model, or `pixverse capabilities create image --json` to find the installed default. Without it (CLI before 1.4.0), use `pixverse create image --help` with the [static image model reference](../references/image-models.md), which also covers model-specific defaults, region availability, and reference limits.

Preserve the requested model and quality; otherwise use defaults or select by requested resolution, reference count, and speed. The global default is `gpt-image-2.5-flare`; in `cn` it is `qwen-image` and fewer models are available.

## Flags

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--prompt <text>` | Prompt text (required) | -- |
| `--image <input>` | Single image input (enables I2I): local file, HTTPS URL, image ID, or media path | pass an image ID or media path to skip upload |
| `--images <inputs...>` | Multiple image inputs (enables I2I) | per-model reference cap |
| `-m, --model <model>` | Image model | see discovery above |
| `-q, --quality <q>` | Image quality | model-specific (default `1080p` for most); aliases `1K`/`1.5K`/`2K`/`3K`/`4K` |
| `--aspect-ratio <ratio>` | Aspect ratio | model-specific (default `16:9`); some models accept `auto` |
| `--detail-level <level>` | Rendering detail | GPT Image and Nano Banana 2.1 only; see [model-specific flags](../references/image-models.md#model-specific-flags) |
| `--background <value>` | `auto`, `transparent`, `opaque` | GPT Image 2.5 and Seedream 5.5 only |
| `--output-format <format>` | `png`, `jpeg`, `webp` | MiniMax H3 Image only (CLI 1.4.20+) |
| `--count <number>` | Number of generations | `1`–`4` |
| `--seed <number>` | Random seed | ignored by Nano Banana 2.1 and MiniMax H3 Image |
| `--idempotency-key <key>` | Stable safe-retry key; see execution contract | optional |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | timeout `300` |

Models that do not support `--detail-level`, `--background`, or `--output-format` reject them with exit 6 before upload.

## Create or edit one image

Submit once and capture both result and exit status; for batches, partial results, and media inputs read the [execution contract](../references/execution-contract.md).

```bash
if RESULT=$(pixverse create image --prompt "$PROMPT" --count 1 --json); then
  IMAGE_ID=$(printf '%s\n' "$RESULT" | jq -er 'select(.status == "completed") | .image_id // empty') || exit 1
else
  RC=$?
  printf '%s\n' "$RESULT" >&2
  exit "$RC"
fi
```

For editing, add `--image "$SOURCE_IMAGE"` or `--images "$IMAGE_1" "$IMAGE_2"` to that invocation. Check the chosen model's reference limit. Pass `--type image` to `task wait` and `asset download` for images.

## Continue only when needed

- Repeated edits: [image editing workflow](../workflows/image-editing-pipeline.md).
- Generate then animate: [image-to-video chain](../workflows/text-to-image-to-video.md), passing the generated image ID directly.
- Multiple images: [batch creation](../workflows/batch-creation.md).
- Browse or download: [asset management](asset-management.md).
