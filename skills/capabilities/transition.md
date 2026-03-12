---
name: pixverse:transition
description: Create smooth transition animations between two or more keyframe images
---

# Transition

Create smooth transition animations between two or more keyframe images using PixVerse's transition generation.

## Prerequisites

- PixVerse CLI installed and authenticated (`pixverse auth login`)
- Two or more images (local file paths or URLs) to use as keyframes

## When to Use

```
Want to animate between images?
├── Two images → pixverse create transition --images ./a.jpg ./b.jpg --json
├── Multiple frames → pixverse create transition --images ./f1.jpg ./f2.jpg ./f3.jpg --json
└── With guidance → pixverse create transition --images ./a.jpg ./b.jpg --prompt "smooth morph" --json
```

Use transitions when you need to:

- Morph between faces or objects
- Create scene transitions
- Build before/after reveals
- Animate a storyboard into a video

## Steps

1. Prepare two or more keyframe images (local files or URLs).
2. Run `pixverse create transition` with `--images` and `--json`.
3. Parse the JSON output to get the `video_id`.
4. If using `--no-wait`, poll with `pixverse task wait <video_id> --json`.
5. Download the result with `pixverse asset download <video_id> --json` if needed.

## Commands Reference

### create transition

| Flag | Description | Values |
|:---|:---|:---|
| `--images <paths...>` | Image paths or URLs (2+ required) | -- |
| `--prompt <text>` | Optional prompt to guide transition | -- |
| `-m, --model <model>` | Video model | `v5.6` (default), `v5`, `v4.5`, `v4`, `v3.5`, `veo-3.1-standard`, `veo-3.1-fast` |
| `-q, --quality <q>` | Video quality | `360p`, `540p`, `720p` (default), `1080p` |
| `-d, --duration <sec>` | Duration | `5` (default), `8`, `10` |
| `--count <n>` | Generations | `1`-`4` |
| `--seed <n>` | Random seed | -- |
| `--off-peak` | Off-peak pricing | flag |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | -- |

### Transition-capable models

Only specific models support Transition mode. Using other models will result in a validation error.

| Model | `--model` value | Quality | Duration | Aspect Ratio |
|:---|:---|:---|:---|:---|
| PixVerse v5.6 | `v5.6` (default) | `360p` `540p` `720p` `1080p` | `1`–`10` (any integer) | `16:9` `4:3` `1:1` `3:4` `9:16` `3:2` `2:3` |
| Veo 3.1 Standard | `veo-3.1-standard` | `720p` `1080p` | `4` `6` `8` | `16:9` `9:16` |
| Veo 3.1 Fast | `veo-3.1-fast` | `720p` `1080p` | `4` `6` `8` | `16:9` `9:16` |

> **Veo 3.1 constraint:** `1080p` only supports `8s` duration; `720p` supports `4` / `6` / `8`.

### 3+ image constraint: automatic model fallback

When **3 or more images** are provided, models `v5.5` and `v5.6` do **not** support multi-frame transitions. The CLI automatically falls back to `v5` and prints a warning:

```
--model v5.6 does not support 3+ image transitions, using v5
```

To avoid the fallback, explicitly pass `--model v5` when supplying 3+ images.

Additionally, with 3+ images the `--count` flag has no effect — multi-frame transitions always produce one output per transition pair.

## JSON Output

Same video result format as create-video.

Submitted (with `--no-wait`):

```json
{ "video_id": 123, "trace_id": "...", "status": "submitted" }
```

Completed (default, waits for result):

```json
{ "video_id": 123, "trace_id": "...", "status": "completed", "video_url": "...", "cover_url": "...", "prompt": "...", "model": "...", "duration": 5, "width": 1280, "height": 720, "created_at": "..." }
```

## Use Cases

- **Morphing between faces** -- provide two portraits and let the model interpolate
- **Scene transitions** -- smoothly blend from one environment to another
- **Before/after reveals** -- transition between two states of an object or scene
- **Storyboard-to-animation** -- supply sequential storyboard frames to produce a cohesive animation

## Examples

Basic two-image transition:

```bash
pixverse create transition --images ./frame1.jpg ./frame2.jpg --json
```

With prompt and higher quality:

```bash
pixverse create transition --images ./a.jpg ./b.jpg --prompt "smooth morph" --quality 1080p --json
```

Multiple frames with longer duration:

```bash
pixverse create transition --images ./f1.jpg ./f2.jpg ./f3.jpg --duration 10 --json
```

Using a specific model:

```bash
pixverse create transition --images ./before.png ./after.png --model v5 --json
```

Submit without waiting:

```bash
pixverse create transition --images ./a.jpg ./b.jpg --no-wait --json
```

## Error Handling

| Exit Code | Meaning |
|:---|:---|
| 0 | Success |
| 2 | Timeout waiting for generation |
| 3 | Authentication error (token invalid/expired) |
| 4 | Credit/subscription limit reached |
| 5 | Generation failed or content policy violation |
| 6 | Validation error (e.g., fewer than 2 images provided) |

## Related Skills

- `pixverse:create-video` -- create videos from text or images
- `pixverse:post-process-video` -- extend, upscale, add speech/sound to videos
- `pixverse:task-management` -- check status and wait for tasks
- `pixverse:asset-management` -- browse, download, and delete assets
