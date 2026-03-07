---
name: pixverse:post-process-video
description: Enhance existing videos — extend duration, upscale resolution, add speech (lip sync), or add sound effects
---

# Post-Process Video

Enhance existing PixVerse videos with additional capabilities: extend duration, upscale resolution, add speech/lip sync, or add sound effects.

## Prerequisites

- PixVerse CLI installed and authenticated (`pixverse auth login`)
- An existing video (by ID or local file path)
- For speech: an audio file or TTS text
- For sound: a prompt describing the desired sound effect

## When to Use

```
Have an existing video?
├── Make it longer? → pixverse create extend --video <id-or-path> --json
├── Higher resolution? → pixverse create upscale --video <id-or-path> --json
├── Add voice/speech?
│   ├── From audio file? → pixverse create speech --video <id> --audio <path> --json
│   └── From text (TTS)? → pixverse create speech --video <id> --tts-text "..." --tts-speaker <id> --json
└── Add sound effects? → pixverse create sound --video <id> --prompt "..." --json
```

## Steps

1. Identify the source video (ID from a previous generation, or a local file path).
2. Choose the post-processing operation (extend, upscale, speech, or sound).
3. Run the appropriate `pixverse create` subcommand with `--json`.
4. Parse the JSON output to get the `video_id`.
5. If using `--no-wait`, poll with `pixverse task wait <video_id> --json`.
6. Download the result with `pixverse asset download <video_id> --json` if needed.

## Commands Reference

### create extend

Extend a video's duration.

| Flag | Description | Values |
|:---|:---|:---|
| `--video <id-or-path>` | Video ID or local file (required) | -- |
| `--prompt <text>` | Prompt for extension | optional |
| `-m, --model <model>` | Video model | `v5.6` (default), `v5`, `v4.5`, `v4`, `v3.5` |
| `-q, --quality <q>` | Video quality | `360p`, `540p`, `720p` (default), `1080p` |
| `-d, --duration <sec>` | Duration | `4`, `5`, `8`, `10` (NOTE: extend supports 4s, unlike standard creation) |
| `--count <n>` | Generations | `1`-`4` |
| `--seed <n>` | Random seed | any integer |
| `--off-peak` | Off-peak pricing | flag |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | -- |

### create upscale

Upscale a video to higher resolution.

| Flag | Description | Values |
|:---|:---|:---|
| `--video <id-or-path>` | Video ID or local file (required) | -- |
| `-q, --quality <q>` | Target quality | `1080p`, `1440p`, `2160p` (dedicated upscale set) |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | -- |

### create speech

Add speech or voice to a video via audio file or TTS.

| Flag | Description | Values |
|:---|:---|:---|
| `--video <id-or-path>` | Video ID or local file (required) | -- |
| `--audio <path>` | Audio file (alternative to --tts-text) | local file |
| `--tts-text <text>` | TTS text (alternative to --audio) | -- |
| `--tts-speaker <id>` | TTS speaker ID | -- |
| `-m, --model <model>` | Video model | same set |
| `--keep-original-sound` | Keep original sound | flag |
| `--count <n>` | Generations | `1`-`4` |
| `--off-peak` | Off-peak pricing | flag |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | -- |

### create sound

Add sound effects to a video.

| Flag | Description | Values |
|:---|:---|:---|
| `--video <id-or-path>` | Video ID or local file (required) | -- |
| `--prompt <text>` | Sound effect description (required) | -- |
| `-m, --model <model>` | Video model | same set |
| `--keep-original-sound` | Keep original sound | flag |
| `--count <n>` | Generations | `1`-`4` |
| `--off-peak` | Off-peak pricing | flag |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | -- |

## JSON Output

All post-processing commands produce the same video result format.

Submitted (with `--no-wait`):

```json
{ "video_id": 123, "trace_id": "...", "status": "submitted" }
```

Completed (default, waits for result):

```json
{ "video_id": 123, "trace_id": "...", "status": "completed", "video_url": "...", "cover_url": "...", "prompt": "...", "model": "...", "duration": 5, "width": 1280, "height": 720, "created_at": "..." }
```

## Examples

Extend a video:

```bash
pixverse create extend --video 123456 --prompt "continue the scene" --duration 5 --json
```

Upscale to 1080p:

```bash
pixverse create upscale --video 123456 --quality 1080p --json
```

Add TTS speech:

```bash
pixverse create speech --video 123456 --tts-text "Welcome to the future" --tts-speaker 1 --json
```

Add speech from audio file:

```bash
pixverse create speech --video 123456 --audio ./voiceover.mp3 --json
```

Add sound effects:

```bash
pixverse create sound --video 123456 --prompt "gentle rain and thunder" --json
```

Combined pipeline -- extend, add speech, then upscale:

```bash
VID=<original_video_id>
EXTENDED=$(pixverse create extend --video $VID --prompt "continue the scene" --json | jq -r '.video_id')
pixverse task wait $EXTENDED --json
WITH_SPEECH=$(pixverse create speech --video $EXTENDED --tts-text "Hello world" --json | jq -r '.video_id')
pixverse task wait $WITH_SPEECH --json
FINAL=$(pixverse create upscale --video $WITH_SPEECH --quality 1080p --json | jq -r '.video_id')
pixverse task wait $FINAL --json
pixverse asset download $FINAL --json
```

## Error Handling

| Exit Code | Meaning |
|:---|:---|
| 0 | Success |
| 2 | Timeout waiting for generation |
| 3 | Authentication error (token invalid/expired) |
| 4 | Credit/subscription limit reached |
| 5 | Generation failed or content policy violation |
| 6 | Validation error (invalid flags/arguments) |

## Related Skills

- `pixverse:create-video` -- create videos from text or images
- `pixverse:task-management` -- check status and wait for tasks
- `pixverse:asset-management` -- browse, download, and delete assets
