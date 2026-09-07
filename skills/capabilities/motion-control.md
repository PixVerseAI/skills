---
name: pixverse:motion-control
description: Generate video by combining a character image with a motion reference video — transfer motion from one video onto a character
---

# Motion Control

Generate videos by transferring motion from a reference video onto a character image. The character's pose and movement follow the reference video while preserving the character's appearance.

## Prerequisites

- PixVerse CLI installed and authenticated (`pixverse auth login`)
- A character image (clear half-body or full-body shot)
- A motion reference video (by ID or local file path)

## When to Use

```
Want to animate a character with specific motion?
├── Have a character image + motion reference video? → pixverse create motion-control --image <path> --video <id-or-path> --json
└── Want to create a video from scratch?             → pixverse create video (see pixverse:create-video)
```

Use motion control when you need to:

- Animate a character image with motion from a reference video
- Transfer dance moves, gestures, or actions onto a character
- Reproduce a specific motion sequence with a different character

---

## create motion-control -- Flags

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--image <input>` | Character image: local file path, HTTPS URL, image ID, or media path (required) | local files auto-upload; pass an image ID or media path to skip upload |
| `--video <input>` | Motion reference video: file path, HTTPS URL, video ID, or media path (required) | -- |
| `-m, --model <model>` | Video model | `v5.6` (only supported model) |
| `-q, --quality <q>` | Video quality | `360p`, `480p`, `540p`, `720p` (default), `1080p` |
| `--count <number>` | Number of generations | `1` (default), `2`, `3`, `4` |
| `--off-peak` | Use off-peak pricing | flag |
| `--idempotency-key <key>` | Stable safe-retry key; see execution contract | optional |
| `--no-wait` | Return immediately without polling | flag |
| `--timeout <sec>` | Polling timeout | `300` (default) |
| `--json` | JSON output | flag |

### Model constraint

Motion control currently supports **v5.6 only**. Other models will fail with a validation error (exit code 6).

### Character image requirements

The CLI validates the character image before submission. The image must be a **clear half-body or full-body image of a character**. Cropped faces, group photos, or abstract images will be rejected with a validation error.

Images exceeding `1920×1920` pixels or `5 MB` are auto-resized and re-encoded before upload — pass the source file as-is, no pre-compression needed. Remote URLs (`--image https://...`) must use `https://`.

---

## How It Works

1. **Resolve character image** -- If `--image` is a local file, the CLI uploads it to PixVerse cloud storage. If it's an image ID or media path, the already-uploaded asset is used directly.
2. **Validate character image** -- The CLI calls a precheck endpoint to verify the image contains a suitable character (half-body or full-body).
3. **Resolve motion reference** -- If `--video` is a numeric ID, the CLI fetches the video detail. If it's a local file, the CLI uploads it.
4. **Submit motion control** -- The character image, motion reference, and parameters are sent to `POST /video/mimic`.
5. **Poll** -- Unless `--no-wait` is set, the CLI polls until the new video is ready.

---

## Steps

1. Prepare a clear half-body or full-body character image.
2. Identify the motion reference video -- a video ID from a previous generation, or a local file path.
3. Run the command:
   ```bash
   pixverse create motion-control --image ./character.jpg --video 123456 --json
   ```
4. Parse `video_id` from the JSON output.
5. If `--no-wait` was used, poll with `pixverse task wait <video_id> --json`.
6. Download the result with `pixverse asset download <video_id> --json`.

---

## Results and recovery

Use the shared [execution contract](../references/execution-contract.md) for submitted, completed, batch, and partial results, polling, and recovery. A single completed result contains `video_id` and `video_url`. Batch completions use `items[]`; do not parse a top-level ID from a batch result.

## Examples

### Basic motion control

```bash
pixverse create motion-control \
  --image ./character.jpg \
  --video 123456 \
  --json
```

### With a local motion reference video

```bash
pixverse create motion-control \
  --image ./character.png \
  --video ./dance-reference.mp4 \
  --json
```

### Higher quality with multiple variations

```bash
pixverse create motion-control \
  --image ./character.jpg \
  --video 123456 \
  --quality 1080p \
  --count 4 \
  --json
```

For asynchronous creation and optional upscaling, follow the [motion-control workflow](../workflows/motion-control-pipeline.md) and [execution contract](../references/execution-contract.md).

## Related Skills

- `pixverse:create-video` -- create videos from text or images
- `pixverse:post-process-video` -- extend or upscale existing videos
- `pixverse:task-management` -- poll and manage tasks after using `--no-wait`
- `pixverse:asset-management` -- download, list, and delete completed videos
