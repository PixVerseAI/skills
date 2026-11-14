---
name: pixverse:modify-video
description: Edit video content with AI — replace subjects, swap outfits, add accessories, change backgrounds, or transform scenes using a text prompt. Use when the user wants to modify, change, alter, or edit what appears IN a video (not trim/cut/splice). Examples — "replace the cat with a dog", "change her dress to red", "add sunglasses", "swap the background to a beach".
---

# Modify Video

Edit the visual content of an existing video with a text prompt: replace subjects, swap clothing or accessories, transform the background, or change visual style. This is AI re-generation anchored on one keyframe, not timeline editing; for trimming, cutting, or splicing use external tools such as ffmpeg. To make a video longer or sharper, use [post-process-video](post-process-video.md).

Relax flags are accepted; see the [execution contract](../references/execution-contract.md#relax-mode).

## create modify

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--video <input>` | Video file path, HTTPS URL, video ID, or media path (required) | -- |
| `--prompt <text>` | Desired change; bind optional reference images as `@image1`, `@image2`, ... | required |
| `--images <inputs...>` | Optional reference images: file paths, HTTPS URLs, image IDs, or media paths | max 5; labels follow flag order |
| `--keyframe-time <ms>` | Keyframe anchoring the change, in milliseconds; must not exceed the video duration | `0` (first frame) |
| `-m, --model <model>` | Video model | `v5.5` (only supported model; others exit 6) |
| `-q, --quality <quality>` | Video quality | `360p`, `540p`, `720p`; defaults to the source video's quality, else `720p`; an unsupported value falls back to `720p` with a warning |
| `--count <number>` | Number of generations | `1`–`4` |
| `--seed <number>` | Random seed | any integer |
| `--off-peak` | Use off-peak pricing | flag |
| `--idempotency-key <key>` | Stable safe-retry key; see execution contract | optional |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | timeout `300` |

## Results

Follow the [execution contract](../references/execution-contract.md) for result shapes, waiting, and recovery.

## Examples

```bash
pixverse create modify --video 123456 --prompt "Add fireworks exploding in the sky" --keyframe-time 3000 --json

pixverse create modify \
  --video ./my-video.mp4 \
  --images ./red-jacket.jpg ./city-at-night.jpg \
  --prompt "Replace the character's outfit with @image1 and use @image2 as the background" \
  --json
```

For modification followed by upscaling, use the [modify-video workflow](../workflows/modify-video-pipeline.md). For multiple variations, use [batch creation](../workflows/batch-creation.md).

## Related Skills

- `pixverse:create-video` -- create new videos from text or images
- `pixverse:post-process-video` -- extend or upscale existing videos
- `pixverse:task-management` -- poll and manage tasks after using `--no-wait`
- `pixverse:asset-management` -- download, list, and delete completed videos
