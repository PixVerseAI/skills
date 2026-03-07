---
name: pixverse
description: PixVerse CLI — generate AI videos and images from the command line. Start here.
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
| `task status` | Check task status |
| `task wait` | Wait for task completion |
| `asset list` | List generated assets |
| `asset info` | Get asset details |
| `asset download` | Download a generated asset |
| `asset delete` | Delete an asset |
| `account info` | View account info and credits |
| `account usage` | View credit usage records |
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
