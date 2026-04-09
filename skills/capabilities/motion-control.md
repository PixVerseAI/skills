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
| `--image <pathOrUrl>` | Character image file path or URL (required) | local file or URL |
| `--asset-image <path>` | Character image OSS path (skips upload) | -- |
| `--video <idOrPath>` | Motion reference video ID or file path (required) | -- |
| `-m, --model <model>` | Video model | `v5.6` (only supported model) |
| `-q, --quality <q>` | Video quality | `360p`, `480p`, `540p`, `720p` (default), `1080p` |
| `--count <number>` | Number of generations | `1` (default), `2`, `3`, `4` |
| `--off-peak` | Use off-peak pricing | flag |
| `--no-wait` | Return immediately without polling | flag |
| `--timeout <sec>` | Polling timeout | `300` (default) |
| `--json` | JSON output | flag |

### Model constraint

Motion control currently supports **v5.6 only**. Other models will fail with a validation error (exit code 6).

### Character image requirements

The CLI validates the character image before submission. The image must be a **clear half-body or full-body image of a character**. Cropped faces, group photos, or abstract images will be rejected with a validation error.

---

## How It Works

1. **Resolve character image** -- If `--image` is a local file, the CLI uploads it to PixVerse cloud storage. If `--asset-image` is provided, the OSS path is used directly.
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

## JSON Output

### With --no-wait (submitted)

```json
{
  "video_id": 123456,
  "trace_id": "abc-123",
  "status": "submitted"
}
```

When `--count > 1`:

```json
{
  "video_ids": [123456, 123457, 123458, 123459],
  "trace_id": "abc-123",
  "status": "submitted"
}
```

### With wait (completed)

```json
{
  "video_id": 123456,
  "trace_id": "abc-123",
  "status": "completed",
  "video_url": "https://...",
  "cover_url": "https://...",
  "prompt": "",
  "model": "v5.6",
  "duration": 5,
  "width": 1280,
  "height": 720,
  "created_at": "2026-01-01T00:00:00Z"
}
```

---

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

### Submit without waiting

```bash
RESULT=$(pixverse create motion-control \
  --image ./character.jpg \
  --video 123456 \
  --no-wait --json)
VIDEO_ID=$(echo "$RESULT" | jq -r '.video_id')
pixverse task wait $VIDEO_ID --json
pixverse asset download $VIDEO_ID --json
```

### Motion control + post-process pipeline

```bash
# Step 1: Generate motion-controlled video
VID=$(pixverse create motion-control \
  --image ./character.jpg \
  --video 123456 \
  --quality 720p --json | jq -r '.video_id')

# Step 2: Add sound effects
WITH_SOUND=$(pixverse create sound \
  --video $VID \
  --prompt "upbeat dance music" \
  --json | jq -r '.video_id')
pixverse task wait $WITH_SOUND --json

# Step 3: Upscale
FINAL=$(pixverse create upscale \
  --video $WITH_SOUND \
  --quality 1080p --json | jq -r '.video_id')
pixverse task wait $FINAL --json

# Step 4: Download
pixverse asset download $FINAL --json
```

---

## Error Handling

| Exit Code | Meaning | Recovery |
|:---|:---|:---|
| 0 | Success | -- |
| 2 | Timeout waiting for completion | Increase `--timeout` or use `--no-wait` then poll with `pixverse task wait` |
| 3 | Auth token expired or invalid | Re-run `pixverse auth login` to refresh credentials |
| 4 | Insufficient credits | Check balance with `pixverse account info --json`, then top up |
| 5 | Generation failed | Check character image quality, try a different reference video |
| 6 | Validation error | Character image must be a clear half-body or full-body shot; model must be `v5.6` |

---

## Related Skills

- `pixverse:create-video` -- create videos from text or images
- `pixverse:post-process-video` -- extend, upscale, or add audio to existing videos
- `pixverse:task-management` -- poll and manage tasks after using `--no-wait`
- `pixverse:asset-management` -- download, list, and delete completed videos
