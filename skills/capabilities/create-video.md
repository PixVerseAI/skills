---
name: pixverse:create-video
description: Create AI videos from text prompts (T2V), images (I2V), reference media, or source-video editing
---

# Create Video

For text-to-video use `create video --prompt`; add `--image` for image-to-video. For `create reference` with image/video/audio references or source-video editing, read [reference generation](../references/video-reference.md) only; do not load it for a normal text/image-to-video request. For Seedance 480p Drafts and paid 1080p Final creation, read [Draft and Final](../references/seedance-draft-final.md).

Relax flags are accepted; see the [execution contract](../references/execution-contract.md#relax-mode).

## Parameter discovery

Query only the selected mode and model:

```bash
pixverse capabilities create video --model v6 --json
```

Use the installed result for supported flags, defaults, enums, and limits. Without it (CLI before 1.4.0), use `pixverse create video --help` and the [static video model reference](../references/video-models.md), which also covers mode- and region-specific behavior. Preserve the user's chosen model and parameters.

## create video -- Flags

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--prompt <text>` | Prompt text (required) | -- |
| `--image <input>` | Image input (enables I2V): local file, HTTPS URL, image ID, or media path | pass an existing image ID or media path to skip upload |
| `-m, --model <model>` | Video model | `v6` by default; see discovery above |
| `-d, --duration <sec>` | Duration in seconds | model-specific (default `5`) |
| `-q, --quality <q>` | Video quality | model-specific |
| `--aspect-ratio <ratio>` | Aspect ratio | model-specific; some models accept `auto` or force it for I2V |
| `--seed <number>` | Random seed | any integer |
| `--count <number>` | Number of generations | `1`–`4` |
| `--audio` / `--no-audio` | Enable or disable audio generation | default on for supported models |
| `--multi-shot` / `--no-multi-shot` | Enable or disable multi-shot mode | model-dependent; forced off for `pixverse-c1` |
| `--off-peak` | Use off-peak pricing | flag |
| `--idempotency-key <key>` | Stable safe-retry key; see execution contract | optional |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | timeout `300` |

## Create one video

Submit once and preserve the result; the [execution contract](../references/execution-contract.md) covers batch or partial results, waiting, retries, and media inputs.

```bash
if RESULT=$(pixverse create video --prompt "$PROMPT" --model v6 --count 1 --json); then
  VIDEO_ID=$(printf '%s\n' "$RESULT" | jq -er 'select(.status == "completed") | .video_id // empty') || exit 1
else
  RC=$?
  printf '%s\n' "$RESULT" >&2
  exit "$RC"
fi
```

To animate an image, add `--image "$IMAGE_INPUT"`. Oversized local images are resized to fit `1920×1920` and `5 MB`; the original file stays unchanged.

## Continue only when needed

- Download the result: [text-to-video workflow](../workflows/text-to-video-pipeline.md).
- Multiple outputs or parallel requests: [batch creation](../workflows/batch-creation.md).
- Extend, upscale, or add audio: [video production](../workflows/video-production.md).
- Edit at a keyframe: [modify video](modify-video.md).
- Transfer motion to a character: [motion control](motion-control.md).
