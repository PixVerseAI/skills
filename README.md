# PixVerse Skills

Agent skill library for [PixVerse CLI](https://www.npmjs.com/package/pixverse) — helps AI agents (Claude Code, Cursor, Codex, etc.) generate videos and images through structured, composable workflows.

## What is this?

PixVerse CLI is a **UI-free version of [pixverse.ai](https://pixverse.ai)** — all models, parameters, and capabilities from the website are available as CLI commands with structured JSON output.

This repository provides **skill files** that teach AI agents how to use those commands correctly: which flags to pass, which models support which parameters, how to chain commands into pipelines, and how to handle errors.

## Quick Start

```bash
# Install the CLI
npm install -g pixverse

# Authenticate
pixverse auth login

# Create a video
pixverse create video --prompt "A cat astronaut floating in space" --json
```

> PixVerse CLI uses the same credit system as the website. **Only subscribed users** can use it. See [subscription plans](https://app.pixverse.ai/subscribe).

## Skill Structure

```
skills/
  SKILL.md                          # Entry point — start here
  capabilities/                     # Individual command skills
    auth-and-account.md             #   Authentication & account management
    create-video.md                 #   Text-to-video, image-to-video, fusion
    create-and-edit-image.md        #   Text-to-image, image-to-image
    transition.md                   #   Keyframe transition animations
    post-process-video.md           #   Extend, upscale, speech, sound
    task-management.md              #   Poll and wait for generation tasks
    asset-management.md             #   List, download, delete assets
  workflows/                        # Multi-step pipeline skills
    text-to-video-pipeline.md       #   End-to-end text-to-video
    image-to-video-pipeline.md      #   Animate an image into video
    text-to-image-to-video.md       #   Generate image then animate it
    image-editing-pipeline.md       #   Iterative image editing
    video-production.md             #   Full production (create + extend + audio + upscale)
    batch-creation.md               #   Parallel batch generation
```

### Capabilities vs Workflows

- **Capabilities** document a single command or command group — flags, models, parameter constraints, JSON output format, error codes.
- **Workflows** compose multiple capabilities into end-to-end pipelines with step-by-step instructions.

## Supported Models

### Video Models

| Model | CLI value | Modes | Quality | Duration | Aspect Ratio |
|:---|:---|:---|:---|:---|:---|
| PixVerse v5.6 | `v5.6` | Video | `360p` `540p` `720p` `1080p` | `1`-`10` (any integer) | `16:9` `4:3` `1:1` `3:4` `9:16` `3:2` `2:3` |
| Sora 2 | `sora-2` | Video | `720p` | `4` `8` `12` | `16:9` `9:16` |
| Sora 2 Pro | `sora-2-pro` | Video | `720p` `1080p` | `4` `8` `12` | `16:9` `9:16` |
| Veo 3.1 Standard | `veo-3.1-standard` | Video, Transition | `720p` `1080p` | `4` `6` `8` | `16:9` `9:16` |
| Veo 3.1 Fast | `veo-3.1-fast` | Video, Transition | `720p` `1080p` | `4` `6` `8` | `16:9` `9:16` |
| Grok Imagine | `grok-imagine` | Video | `480p` `720p` | `1`-`15` | `16:9` `4:3` `1:1` `9:16` `3:4` `3:2` `2:3` |

### Image Models

| Model | CLI value | Resolution | Aspect Ratio |
|:---|:---|:---|:---|
| Qwen Image | `qwen-image` | `720p` `1080p` | `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Seedream 5.0 Lite | `seedream-5.0-lite` | `2k` `3k` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Seedream 4.5 | `seedream-4.5` | `2k` `4k` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Seedream 4.0 | `seedream-4.0` | `1080p` `2k` `4k` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Nanobanana | `nanobanana` | `1080p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Nano Banana Pro | `nano-banana-pro` | `1080p` `2k` `4k` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Nano Banana 2 | `nano-banana-2` | `512p` `1080p` `2k` `4k` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |

## For AI Agent Developers

These skills are designed to be loaded into agent context. Each skill file is self-contained with:

- **Decision trees** — help the agent choose the right command
- **Flag tables** — every parameter with allowed values and defaults
- **Model reference tables** — per-model parameter constraints
- **JSON output schemas** — exact response format for parsing
- **Exit codes** — deterministic error handling
- **Examples** — copy-paste-ready commands

Start by loading `skills/SKILL.md` as the entry point, then load specific capability or workflow skills as needed.

## Links

- [PixVerse Website](https://pixverse.ai)
- [PixVerse CLI on npm](https://www.npmjs.com/package/pixverse)
- [Subscription Plans](https://app.pixverse.ai/subscribe)
