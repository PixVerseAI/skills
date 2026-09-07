---
name: pixverse:post-process-video
description: Enhance existing videos — extend duration or upscale resolution
---

# Post-Process Video

Enhance existing PixVerse videos: extend duration or upscale resolution.

> **Looking to add a voiceover or music track?** Speech and music are now standalone audio generations, not video post-processing. Generate audio with `pixverse:create-voice` (TTS) or `pixverse:create-music`, then mux it onto the video yourself (e.g. `ffmpeg`). The old `create speech` / lip-sync command was removed in CLI v1.2.0.

## Prerequisites

- PixVerse CLI installed and authenticated (`pixverse auth login`)
- An existing video supplied as a local file, HTTPS URL, PixVerse video ID, or media path

## When to Use

```
Have an existing video?
├── Change content/scene? → pixverse create modify --video <id-or-path> --prompt "..." --json
│                           (see pixverse:modify-video)
├── Make it longer? → pixverse create extend --video <id-or-path> --json
└── Higher resolution? → pixverse create upscale --video <id-or-path> --json
```

## Steps

1. Identify the source video (local file, HTTPS URL, PixVerse video ID, or media path).
2. Choose the post-processing operation (extend or upscale).
3. Run the appropriate `pixverse create` subcommand with `--json`.
4. Parse the JSON output to get the `video_id`.
5. If using `--no-wait`, poll with `pixverse task wait <video_id> --json`.
6. Download the result with `pixverse asset download <video_id> --json` if needed.

## Commands Reference

### create extend

Extend a video's duration.

| Flag | Description | Values |
|:---|:---|:---|
| `--video <input>` | Video file path, HTTPS URL, video ID, or media path (required) | -- |
| `--prompt <text>` | Prompt for extension | optional |
| `-m, --model <model>` | Video model | `v6` (default), `grok-imagine` |
| `-q, --quality <q>` | Video quality | V6: `360p` `540p` `720p` `1080p`; Grok Imagine: `480p` `720p` |
| `-d, --duration <sec>` | Duration | `1`–`15` (any integer; default `4`) |
| `--count <n>` | Generations | `1`-`4` |
| `--seed <n>` | Random seed | any integer |
| `--audio` / `--no-audio` | Enable or disable audio generation | V6 only; ignored with a warning for Grok Imagine |
| `--off-peak` | Off-peak pricing | flag |
| `--idempotency-key <key>` | Stable safe-retry key; see execution contract | optional |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | -- |

### create upscale

Upscale a video to the fixed `2160p` target. `--quality` may be omitted because `2160p` is the default and only accepted value.

| Flag | Description | Values |
|:---|:---|:---|
| `--video <input>` | Video file path, HTTPS URL, video ID, or media path (required) | -- |
| `-q, --quality <q>` | Target quality | `2160p` (default; only accepted value) |
| `--idempotency-key <key>` | Stable safe-retry key; see execution contract | optional |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | -- |

## Results and recovery

Use the shared [execution contract](../references/execution-contract.md) for submitted, completed, batch, and partial results, polling, and recovery. A single completed result contains `video_id` and `video_url`. Batch completions use `items[]`; do not parse a top-level ID from a batch result.

## Examples

Extend a video:

```bash
pixverse create extend --video 123456 --prompt "continue the scene" --duration 5 --json
```

Upscale to 2160p using the default:

```bash
pixverse create upscale --video 123456 --json

# The same command also accepts other video input forms:
pixverse create upscale --video ./source.mp4 --json
pixverse create upscale --video https://example.com/source.mp4 --json
pixverse create upscale --video upload/source.mp4 --json
```

For extension, upscaling, or audio composition in a deliverable, follow [video production](../workflows/video-production.md).

## Related Skills

- `pixverse:create-video` -- create videos from text or images
- `pixverse:create-voice` -- generate speech audio (TTS) to add as a voiceover
- `pixverse:create-music` -- generate a music track
- `pixverse:modify-video` -- modify video content with a prompt at a keyframe
- `pixverse:task-management` -- check status and wait for tasks
- `pixverse:asset-management` -- browse, download, and delete assets
