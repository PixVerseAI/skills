---
name: pixverse:motion-control
description: Generate video by combining a character image with a motion reference video — transfer motion from one video onto a character
---

# Motion Control

Transfer motion from a reference video onto a character image: the pose and movement follow the video while the character's appearance is preserved. Use it for dance moves, gestures, or reproducing an action with a different character. To create a video from scratch, use [create-video](create-video.md).

Relax flags are accepted; see the [execution contract](../references/execution-contract.md#relax-mode).

## create motion-control

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--image <input>` | Character image: local file, HTTPS URL, image ID, or media path (required) | pass an ID or media path to skip upload |
| `--video <input>` | Motion reference video: file path, HTTPS URL, video ID, or media path (required) | -- |
| `-m, --model <model>` | Video model | `v5.6` (only supported model; others exit 6) |
| `-q, --quality <q>` | Video quality | `360p`, `480p`, `540p`, `720p` (default), `1080p` |
| `--count <number>` | Number of generations | `1`–`4` |
| `--off-peak` | Use off-peak pricing | flag |
| `--idempotency-key <key>` | Stable safe-retry key; see execution contract | optional |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | timeout `300` |

The CLI checks the character image before submission. It must be a **clear half-body or full-body image of one character**; cropped faces, group photos, or abstract images are rejected with a validation error. Oversized local images are resized automatically; pass the source file as-is.

## Results

Follow the [execution contract](../references/execution-contract.md) for result shapes, waiting, and recovery.

## Examples

```bash
pixverse create motion-control --image ./character.png --video ./dance-reference.mp4 --json
pixverse create motion-control --image ./character.jpg --video 123456 --quality 1080p --count 4 --json
```

For asynchronous creation and optional upscaling, follow the [motion-control workflow](../workflows/motion-control-pipeline.md).

## Related Skills

- `pixverse:create-video` -- create videos from text or images
- `pixverse:post-process-video` -- extend or upscale existing videos
- `pixverse:task-management` -- poll and manage tasks after using `--no-wait`
- `pixverse:asset-management` -- download, list, and delete completed videos
