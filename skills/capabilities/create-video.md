---
name: pixverse:create-video
description: Create AI videos from text prompts (T2V), images (I2V), reference media, or source-video editing
---

# Create Video

For text-to-video use `create video --prompt`; add `--image` for image-to-video.
For `create reference` with image/video/audio references or source-video editing, read [reference generation](../references/video-reference.md) only. Do not load the reference matrix for a normal text/image-to-video request.

## Parameter discovery

Check the CLI version once per session. On **1.4.0+**, query only the selected mode and model:

```bash
pixverse capabilities create video --model v6 --json
```

Use the installed result for supported flags, defaults, enums, and limits. On older releases, inspect `pixverse create video --help` and read the [static video model reference](../references/video-models.md) as needed; a static entry does not establish support in an older install. Preserve the user's chosen model and parameters.

## create video -- Flags

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--prompt <text>` | Prompt text (required) | -- |
| `--image <input>` | Image input (enables I2V): local file path, HTTPS URL, image ID, or media path | local files auto-upload; pass an existing asset's image ID or media path to skip upload |
| `-m, --model <model>` | Video model | Installed registry; static fallback linked above |
| `-d, --duration <sec>` | Duration in seconds | model-specific; `1`–`30` overall (default `5`; see Parameter discovery above) |
| `-q, --quality <q>` | Video quality | model-specific; `360p`–`2160p` overall (see Parameter discovery above) |
| `--aspect-ratio <ratio>` | Aspect ratio | model-specific; Seedance 2.5 T2V, FLUX 3, and Wan 3.0 also accept `auto`; H3 image-to-video forces `auto` (see Parameter discovery above) |
| `--seed <number>` | Random seed | any integer |
| `--count <number>` | Number of generations | `1` (default), `2`, `3`, `4` |
| `--audio` / `--no-audio` | Enable or disable audio generation | boolean toggle (default: on for supported models) |
| `--multi-shot` / `--no-multi-shot` | Enable or disable multi-shot mode | boolean toggle (forced off for `pixverse-c1`) |
| `--off-peak` | Use off-peak pricing | flag |
| `--idempotency-key <key>` | Stable safe-retry key; see execution contract | optional |
| `--no-wait` | Return immediately without polling | flag |
| `--timeout <sec>` | Polling timeout | `300` (default) |
| `--json` | JSON output | flag |

## Create one video

After authentication and parameter selection, submit once and preserve the result. This example requests one output explicitly; use the [execution contract](../references/execution-contract.md) for batch or partial results, retries, and asynchronous submission.

```bash
if RESULT=$(pixverse create video --prompt "$PROMPT" --model v6 --count 1 --json); then
  VIDEO_ID=$(printf '%s\n' "$RESULT" | jq -er 'select(.status == "completed") | .video_id // empty') || exit 1
else
  RC=$?
  printf '%s\n' "$RESULT" >&2
  exit "$RC"
fi
```

To animate an image, add `--image "$IMAGE_INPUT"` to the same invocation. An input may be a local file, HTTPS URL, compatible image ID, or media path. Existing IDs/media paths avoid repeated transfer. HTTPS URLs are downloaded and uploaded; HTTP is rejected. Oversized local images are resized to fit `1920×1920` and `5 MB`; the original file stays unchanged. Local videos are uploaded as-is.

Create waits by default; do not wait again after a completed result. To return before completion, pass `--no-wait`, retain submitted IDs, and follow [task management](task-management.md).

## Continue only when needed

- Download the result: [text-to-video workflow](../workflows/text-to-video-pipeline.md).
- Multiple outputs or parallel requests: [batch creation](../workflows/batch-creation.md).
- Extend, upscale, or add audio: [video production](../workflows/video-production.md).
- Edit at a keyframe: [modify video](modify-video.md).
- Transfer motion to a character: [motion control](motion-control.md).
