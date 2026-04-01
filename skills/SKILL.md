---
name: pixverse-ai-image-and-video-generator
description: PixVerse CLI — generate AI videos and images from the command line. Supports PixVerse, Veo, Sora, Kling, Hailuo, Wan, and more video models; Nano Banana (Gemini), Seedream, Qwen image models; and PixVerse's rich effect template library. Start here.
version: 1.3.0
homepage: https://pixverse.ai
source: https://github.com/PixVerseAI/skills
---

# PixVerse CLI — Master Skill

## What is PixVerse CLI

PixVerse CLI is the official command-line interface for [PixVerse](https://pixverse.ai) — an AI-powered creative platform for generating videos and images. It is essentially **a UI-free version of the PixVerse website**: all features, models, and parameters are aligned with the web experience at [app.pixverse.ai](https://app.pixverse.ai).

It is designed for:
- **AI agents** (primary) — structured JSON output, deterministic exit codes, and pipeable commands for autonomous workflows (Claude Code, Cursor, Codex, custom agents)
- **Developers & power users** — scriptable video/image generation without leaving the terminal
- **Automation** — batch processing, CI/CD pipelines, content production workflows

Key facts:
- Generating content **consumes credits** from the user's PixVerse account (same pricing as the website)
- **Only subscribed users** can use the CLI — see [subscription plans](https://app.pixverse.ai/subscribe)
- All output can be returned as structured JSON via `--json` flag
- English only

---

## Installation

```bash
npm install -g pixverse
```

Or run without installing:
```bash
npx pixverse
```

Verify:
```bash
pixverse --version
```

**Requires Node.js >= 20.**

---

## Quick Start

```bash
# 1. Install
npm install -g pixverse

# 2. Authenticate (OAuth device flow — opens browser)
pixverse auth login --json

# 3. Create a video (waits for completion by default)
RESULT=$(pixverse create video --prompt "A cat astronaut floating in space" --json)
VIDEO_ID=$(echo "$RESULT" | jq -r '.video_id')

# 4. Download the result
pixverse asset download $VIDEO_ID --json
```

To skip waiting and poll later:
```bash
RESULT=$(pixverse create video --prompt "A cat astronaut floating in space" --no-wait --json)
VIDEO_ID=$(echo "$RESULT" | jq -r '.video_id')
pixverse task wait $VIDEO_ID --json
pixverse asset download $VIDEO_ID --json
```

> **Windows users**: For a full PowerShell pipeline example (T2I → I2V → sound → upscale → download), see `skills/examples/windows/powershell-text-to-video.ps1`.

---

## Authentication

PixVerse CLI uses **OAuth device flow** — no need to manually copy tokens:

1. Run `pixverse auth login --json`
2. The CLI prints an authorization URL
3. Open the URL in your browser and authorize
4. The token is stored automatically in `~/.pixverse/`

Details:
- Token is valid for 30 days
- CLI sessions are independent from your web/app sessions
- If token expires (exit code 3), re-run `pixverse auth login --json`
- Set `PIXVERSE_TOKEN` environment variable to override the stored token
- Run `pixverse auth status --json` to check login state and credits

---

## Capabilities Overview

| I want to... | Use skill |
|:---|:---|
| Create a video from text or image | `pixverse:create-video` |
| Create or edit an image | `pixverse:create-and-edit-image` |
| Extend, upscale, or add audio to a video | `pixverse:post-process-video` |
| Create transition animation between frames | `pixverse:transition` |
| Check generation progress | `pixverse:task-management` |
| Browse, download, or delete assets | `pixverse:asset-management` |
| Set up auth or check account | `pixverse:auth-and-account` |
| Browse and create from effect templates | `pixverse:template` |
| Manage workspaces (list, switch, status) | `pixverse:workspace` |
| Generate Mondo-style posters and covers | `pixverse:mondo-poster-design` |

> **Looking up models or parameters?** Don't wait until you're generating — read the relevant capabilities file directly:
> - Video models & constraints → `skills/capabilities/create-video.md` (Model Reference section)
> - Image models & constraints → `skills/capabilities/create-and-edit-image.md` (Model Reference section)

---

## Model Quick Reference

Use this to pick a model before diving into a sub-skill.

### Video Models (`pixverse create video --model <value>`)

| Model | `--model` value | Max Quality | Duration |
|:---|:---|:---|:---|
| PixVerse V6 *(default)* | `v6` | `1080p` | `1`–`15`s |
| PixVerse v5.6 | `v5.6` | `1080p` | `1`–`10`s |
| Sora 2 | `sora-2` | `720p` | `4` `8` `12`s |
| Sora 2 Pro | `sora-2-pro` | `1080p` | `4` `8` `12`s |
| Veo 3.1 Standard | `veo-3.1-standard` | `1080p` | `4` `6` `8`s |
| Veo 3.1 Fast | `veo-3.1-fast` | `1080p` | `4` `6` `8`s |
| Grok Imagine | `grok-imagine` | `720p` | `1`–`15`s |

### Image Models (`pixverse create image --model <value>`)

| Model | `--model` value | Max Quality |
|:---|:---|:---|
| Qwen Image *(default)* | `qwen-image` | `1080p` |
| Seedream 5.0 Lite | `seedream-5.0-lite` | `1800p` |
| Seedream 4.5 | `seedream-4.5` | `2160p` |
| Seedream 4.0 | `seedream-4.0` | `2160p` |
| Gemini 2.5 Flash (Nanobanana) | `gemini-2.5-flash` | `1080p` |
| Gemini 3.0 (Nano Banana Pro) | `gemini-3.0` | `2160p` |
| Gemini 3.1 Flash (Nano Banana 2) | `gemini-3.1-flash` | `2160p` |

For full parameter constraints (aspect ratios, quality per model, mode support), read the capabilities files listed above.

---

## Workflow Skills

| I want to... | Use skill |
|:---|:---|
| Generate video from text end-to-end | `pixverse:text-to-video-pipeline` |
| Animate an image into video | `pixverse:image-to-video-pipeline` |
| Generate image then animate it | `pixverse:text-to-image-to-video` |
| Iteratively edit an image | `pixverse:image-editing-pipeline` |
| Full video production (create + extend + audio + upscale) | `pixverse:video-production` |
| Create multiple items in parallel | `pixverse:batch-creation` |
| Generate a Mondo-style poster end-to-end | `pixverse:mondo-poster-pipeline` |
| Generate poster then animate into video | `pixverse:mondo-poster-to-video-pipeline` |

---

## Reference Materials

Located in `skills/references/`. These are read-only knowledge bases that capabilities and workflows draw from — no CLI commands, just curated design knowledge.

| Reference | Path | Content |
|:---|:---|:---|
| Mondo Artist Styles | `references/mondo-poster/artist-styles.md` | 37 artist styles with prompt keywords across 7 categories |
| Mondo Composition Patterns | `references/mondo-poster/composition-patterns.md` | 8 composition techniques (negative space, silhouette, geometric framing, etc.) |
| Mondo Genre Templates | `references/mondo-poster/genre-templates.md` | Genre-specific prompt templates for film, book covers, and album covers |

---

## All Commands

| Command | Description |
|:---|:---|
| `auth login` | Login via browser (OAuth device flow) |
| `auth status` | Check authentication status |
| `auth logout` | Remove stored token |
| `create video` | Text-to-video or image-to-video |
| `create image` | Text-to-image or image-to-image |
| `create transition` | Create transitions between keyframes |
| `create speech` | Add lip-sync speech to video |
| `create sound` | Add AI sound effects to video |
| `create extend` | Extend video duration |
| `create upscale` | Upscale video resolution |
| `create reference` | Generate video with character references |
| `create template` | Create video or image from an effect template |
| `template categories` | List template categories |
| `template list` | Browse templates (with optional category filter) |
| `template search` | Search templates by keyword |
| `template info` | Get template details |
| `task status` | Check task status |
| `task wait` | Wait for task completion |
| `asset list` | List generated assets |
| `asset info` | Get asset details |
| `asset download` | Download a generated asset |
| `asset delete` | Delete an asset |
| `account info` | View account info and credits |
| `account usage` | View credit usage records |
| `workspace list` | List all workspaces |
| `workspace status` | Show currently active workspace |
| `workspace switch` | Switch to a different workspace |
| `workspace manage` | Open workspace management in browser |
| `subscribe` | Open subscription page in browser |
| `config list` | List all config values |
| `config get` | Get a config value |
| `config set` | Set a config value |
| `config reset` | Reset config to defaults |
| `config path` | Show config file path |
| `config defaults` | Manage per-mode creation defaults |

---

## Global Flags

| Flag | Description |
|:---|:---|
| `--json` or `-p` | Pure JSON output to stdout (required for agent use) |
| `--workspace-id <id>` | Per-command workspace override (0 = personal). Not persisted — only affects the single invocation. |
| `-V, --version` | Show CLI version |
| `-h, --help` | Show help for any command |

Every command supports `--json`. All examples in skills use `--json` for machine-readable output.

**Interactive mode**: Run any creation command without arguments (and without `--json`) to enter the interactive wizard.

---

## Output Contract

### JSON mode (`--json`)

- **stdout**: Pure JSON only. No spinners, no progress text, no decorative output.
- **stderr**: All errors, warnings, and diagnostic messages.
- Parse stdout with `jq` or any JSON parser.

### Exit Codes

| Code | Name | Meaning | Recovery |
|:---|:---|:---|:---|
| 0 | SUCCESS | Completed | — |
| 1 | GENERAL_ERROR | Unexpected error | Check stderr for details |
| 2 | TIMEOUT | Polling timed out | Increase `--timeout` or use `--no-wait` then `pixverse task wait` |
| 3 | AUTH_EXPIRED | Token invalid/expired | Re-run `pixverse auth login --json` |
| 4 | CREDIT_INSUFFICIENT | Not enough credits | Check `pixverse account info --json`, wait for daily reset or upgrade |
| 5 | GENERATION_FAILED | Generation failed/rejected | Check prompt, try different parameters |
| 6 | VALIDATION_ERROR | Invalid parameters | Check flag values against enums in each skill |

### Workspace error auto-recovery

When a request fails because the active workspace is no longer accessible (e.g. user was removed from a team), the CLI automatically resets to personal workspace (ID=0) and asks you to retry. This does **not** trigger when `--workspace-id` override is active or the failing request is a workspace management command.

### Error handling pattern

```bash
RESULT=$(pixverse create video --prompt "A sunset over mountains" --json 2>/tmp/pv_err)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  VIDEO_ID=$(echo "$RESULT" | jq -r '.video_id')
  echo "Success: $VIDEO_ID"
  pixverse asset download $VIDEO_ID --json
elif [ $EXIT_CODE -eq 3 ]; then
  echo "Token expired, re-authenticating..."
  pixverse auth login --json
elif [ $EXIT_CODE -eq 4 ]; then
  echo "Not enough credits"
  pixverse account info --json | jq '.credits'
elif [ $EXIT_CODE -eq 5 ]; then
  echo "Generation failed — check prompt or parameters"
  cat /tmp/pv_err
else
  echo "Error (code $EXIT_CODE)"
  cat /tmp/pv_err
fi
```
