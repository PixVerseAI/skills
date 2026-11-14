---
name: pixverse:post-process-video
description: Enhance existing videos — extend duration or upscale resolution
---

# Post-Process Video

Extend the duration or upscale the resolution of an existing video supplied as a local file, HTTPS URL, PixVerse video ID, or media path. To change content, use [modify-video](modify-video.md). For a voiceover or soundtrack, generate audio with [create-voice](create-voice.md) or [create-music](create-music.md) and mux it yourself (for example with ffmpeg).

## create extend

| Flag | Description | Values |
|:---|:---|:---|
| `--video <input>` | Video file path, HTTPS URL, video ID, or media path (required) | -- |
| `--prompt <text>` | Prompt for extension | optional |
| `-m, --model <model>` | Video model | `v6` (default), `grok-imagine` (global only; in `cn` use `v6`) |
| `-q, --quality <q>` | Video quality | V6: `360p` `540p` `720p` `1080p`; Grok Imagine: `480p` `720p`; defaults to the source video's quality, else `720p` |
| `-d, --duration <sec>` | Duration | `1`–`15` (default `5`) |
| `--count <n>` | Generations | `1`–`4` |
| `--seed <n>` | Random seed | any integer |
| `--audio` / `--no-audio` | Enable or disable audio generation | V6 only; ignored with a warning for Grok Imagine |
| `--off-peak` | Off-peak pricing | flag |
| `--idempotency-key <key>` | Stable safe-retry key; see execution contract | optional |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | -- |

## create upscale

Upscales to `2160p`, the default and only accepted `--quality`, so the flag can be omitted.

| Flag | Description | Values |
|:---|:---|:---|
| `--video <input>` | Video file path, HTTPS URL, video ID, or media path (required) | -- |
| `-q, --quality <q>` | Target quality | `2160p` |
| `--idempotency-key <key>` | Stable safe-retry key; see execution contract | optional |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | -- |

## Results

Follow the [execution contract](../references/execution-contract.md) for result shapes, waiting, and recovery.

## Examples

```bash
pixverse create extend --video 123456 --prompt "continue the scene" --duration 5 --json
pixverse create upscale --video ./source.mp4 --json
```

For extension, upscaling, or audio composition in a deliverable, follow [video production](../workflows/video-production.md).

## Related Skills

- `pixverse:create-video` -- create videos from text or images
- `pixverse:create-voice` -- generate speech audio (TTS) to add as a voiceover
- `pixverse:create-music` -- generate a music track
- `pixverse:modify-video` -- modify video content with a prompt at a keyframe
- `pixverse:task-management` -- check status and wait for tasks
- `pixverse:asset-management` -- browse, download, and delete assets
