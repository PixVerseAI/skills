---
name: pixverse:create-and-edit-image
description: Create images from text (T2I) or edit existing images (I2I) using AI
---

# Create and Edit Image

Use `create image --prompt` for text-to-image. Add `--image` for one reference or `--images` for several references to edit or combine existing images.

## Parameter discovery

Check the CLI version once per session. On **1.4.0+**, query `pixverse capabilities create image --model <id> --json` for the chosen model. If none was specified, query `pixverse capabilities create image --json` to find the installed default. On older releases, use `pixverse create image --help` with the [static image model reference](../references/image-models.md); newer model entries may not be supported by that installation.

Preserve the requested model and quality. Otherwise use defaults or select based on the requested resolution, reference count, and speed. CLI **1.4.1** changes the global built-in default to `gpt-image-2.5-flare` and adds `gpt-image-2.5-sunburst`; saved defaults or explicit flags still take precedence. In region `cn`, the default is `qwen-image` and the supported models differ; confirm availability before submission. Unsupported quality/ratio values can be adjusted with a warning on stderr, so choose model-valid values.

## Flags

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--prompt <text>` | Prompt text (required) | -- |
| `--image <input>` | Single image input (enables I2I): local file path, HTTPS URL, image ID, or media path | local files auto-upload; pass an image ID or media path to skip upload |
| `--images <inputs...>` | Multiple image inputs (enables I2I): file paths, HTTPS URLs, image IDs, or media paths | -- |
| `-m, --model <model>` | Image model | Installed registry; static fallback linked above |
| `-q, --quality <q>` | Image quality | `512p`, `720p`, `1080p` (default), `1440p`, `1800p`, `2160p` (availability varies by model — see Parameter discovery above) |
| `--aspect-ratio <ratio>` | Aspect ratio | `1:1`, `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `5:4`, `4:5`, `2:1`, `1:2`, `21:9`, `auto` (availability and default vary by model and installed CLI version) |
| `--detail-level <level>` | GPT Image rendering detail | 2.5 Flare/Sunburst: `low`, `medium`, `high`, `xhigh`, `max`; 2.0: `low`, `medium`, `high`. Default `low`; other models or unsupported values fail with exit 6. |
| `--count <number>` | Number of generations | `1` (default), `2`, `3`, `4` |
| `--seed <number>` | Random seed | any integer |
| `--idempotency-key <key>` | Stable safe-retry key; see execution contract | optional |
| `--no-wait` | Return immediately without polling | flag |
| `--timeout <sec>` | Polling timeout | `300` (default) |
| `--json` | JSON output | flag |

On CLI **1.4.2+**, GPT Image 2.5 supports `1:1`, `16:9`, `9:16`, `3:2`, and `2:3` at every supported quality, with built-in default `16:9`. Quality no longer filters framing: `1080p + 9:16` is valid. Both variants support up to 16 references, independently of output count. See [framing and version compatibility](../references/image-models.md#gpt-image-25-framing) for the older 1.4.1 restrictions and fallback behavior.

## Create or edit one image

Submit once and capture both result and exit status. This example explicitly requests one output; for batches and partial results read the [execution contract](../references/execution-contract.md).

```bash
if RESULT=$(pixverse create image --prompt "$PROMPT" --count 1 --json); then
  IMAGE_ID=$(printf '%s\n' "$RESULT" | jq -er 'select(.status == "completed") | .image_id // empty') || exit 1
else
  RC=$?
  printf '%s\n' "$RESULT" >&2
  exit "$RC"
fi
```

For editing, add `--image "$SOURCE_IMAGE"`, or `--images "$IMAGE_1" "$IMAGE_2"`, to that invocation. Local files and HTTPS URLs are uploaded; compatible image IDs or media paths reuse existing assets. Check the chosen model's input-reference limit. Local oversized images are automatically resized; do not pre-compress solely for upload.

Create waits by default and a single completion includes `image_url`. For `--no-wait`, retain submitted IDs and use `task wait <id> --type image --json`. Download a completed image with `asset download <id> --type image --json`. For result shape, retries, and partial batches use the execution contract.

## Continue only when needed

- Repeated edits: [image editing workflow](../workflows/image-editing-pipeline.md).
- Generate then animate: [image-to-video chain](../workflows/text-to-image-to-video.md), passing the generated image ID directly.
- Multiple images: [batch creation](../workflows/batch-creation.md).
- Browse or download: [asset management](asset-management.md).
