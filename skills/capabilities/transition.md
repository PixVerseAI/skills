---
name: pixverse:transition
description: Create smooth transition animations between two or more keyframe images
---

# Transition

Animate between two or more keyframe images: face/object morphs, scene transitions, before/after reveals, or storyboard frames.

Relax flags are accepted; see the [execution contract](../references/execution-contract.md#relax-mode). For Seedance 480p Drafts and paid 1080p Final creation, read [Draft and Final](../references/seedance-draft-final.md).

## create transition

| Flag | Description | Values |
|:---|:---|:---|
| `--images <inputs...>` | Keyframes: local files, HTTPS URLs, image IDs, or media paths (2+ required) | -- |
| `--prompt <text>` | Prompt to guide transition | optional generally; required for `seedance-2.5`, `seedance-2.5-480draft`, `minimax-h3`, `minimax-h3-max`, and `wan-3.0` |
| `-m, --model <model>` | Video model | See the table below |
| `-q, --quality <q>` | Video quality | model-specific (see table) |
| `-d, --duration <sec>` | Duration | model-specific (default `5`; Veo `4`) |
| `--count <n>` | Generations | `1`–`4`; two-frame transitions only |
| `--seed <n>` | Random seed | -- |
| `--audio` / `--no-audio` | Enable or disable audio generation | model-dependent |
| `--off-peak` | Off-peak pricing | flag |
| `--idempotency-key <key>` | Stable safe-retry key; see execution contract | optional |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | -- |

Framing is derived from the input images; there is no `--aspect-ratio` flag. Query `pixverse capabilities create transition --model <id> --json` for the installed CLI; the table below is a fallback.

## Transition-capable models

Two-frame models accept exactly two images. Only `v5` accepts three or more.

| Model | `--model` value | Quality | Duration | Notes |
|:---|:---|:---|:---|:---|
| PixVerse V6 | `v6` (default) | `360p` `540p` `720p` `1080p` | `1`–`15` | Two frames only |
| PixVerse C1 | `pixverse-c1` | `360p` `540p` `720p` `1080p` | `1`–`15` | Two frames only |
| PixVerse v5.6 | `v5.6` | `360p` `480p` `540p` `720p` `1080p` | `1`–`10` | Two frames only |
| PixVerse v5 | `v5` | `360p` `540p` `720p` `1080p` | `1`–`10` | **3+ frames only** |
| Seedance 2.5 | `seedance-2.5` | `480p` `720p` (default) `1080p` | `4`–`30` | Prompt required; no audio/off-peak control |
| Seedance 2.5 Draft | `seedance-2.5-480draft` | `480p` | `4`–`30` | Prompt required; see [Draft and Final](../references/seedance-draft-final.md) |
| Seedance 2.0 Standard | `seedance-2.0-standard` | `480p` `720p` `1080p` `2160p` | `4`–`15` | No off-peak |
| Seedance 2.0 Fast / Mini | `seedance-2.0-fast`, `seedance-2.0-mini` | `480p` `720p` | `4`–`15` | No off-peak |
| MiniMax H3 | `minimax-h3` | `768p` `1440p` (default) | `5`–`15` | Prompt required; no audio/off-peak control |
| MiniMax H3 Max | `minimax-h3-max` | `480p` `768p` (default) `1080p` | `5`–`15` | Prompt required; no audio/off-peak control |
| Wan 3.0 | `wan-3.0` | `480p` `720p` (default) `1080p` | `2`–`30` | Prompt required; audio optional; no off-peak |
| Veo 3.1 Standard / Fast | `veo-3.1-standard`, `veo-3.1-fast` | `720p` `1080p` `2160p` | `4` `6` `8` | |
| Veo 3.1 Lite | `veo-3.1-lite` | `720p` `1080p` | `4` `6` `8` | |
| Kling 4.0 | `kling-4.0` | `720p` `1080p` (default) | `3`–`30` | No audio control, multi-shot, or off-peak |
| Kling O3 / 3.0 | `kling-o3-pro`, `kling-o3-standard`, `kling-o3-4k`, `kling-3.0-pro`, `kling-3.0-standard`, `kling-3.0-4k` | set by model ID (omit `--quality`) | `3`–`15` | No off-peak |

In `--region cn`, only V6, C1, v5.6, v5 and the Seedance models are available.

Kling O3/3.0 resolution is selected entirely by the model ID; an explicit `--quality` is ignored with a warning. Use the `-4k` IDs for the 4K tier.

### Three or more images

With 3+ images, omitting `--model` selects `v5`. An explicit model that does not support multi-frame transitions (including `v6`, `pixverse-c1`, and `v5.6`) fails validation with exit 6; pass `--model v5` or omit the flag. Multi-frame requests send no top-level count, so `--count` has no effect.

## Results

Follow the [execution contract](../references/execution-contract.md) for result shapes, waiting, and recovery.

## Examples

```bash
pixverse create transition --images ./a.jpg ./b.jpg --prompt "smooth morph" --quality 1080p --json
pixverse create transition --images ./f1.jpg ./f2.jpg ./f3.jpg --model v5 --duration 10 --json
pixverse create transition --model minimax-h3-max --images ./start.jpg ./end.jpg --prompt "A smooth orbiting camera move connects the scenes" --quality 768p --duration 10 --json
pixverse create transition --model seedance-2.5 --images ./start.jpg ./end.jpg --prompt "A seamless transformation" --quality 1080p --duration 20 --no-wait --json
```

## Related Skills

- `pixverse:create-video` -- create videos from text or images
- `pixverse:post-process-video` -- extend or upscale videos
- `pixverse:task-management` -- check status and wait for tasks
- `pixverse:asset-management` -- browse, download, and delete assets
