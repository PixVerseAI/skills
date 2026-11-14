# PixVerse Skills

Agent skill library for [PixVerse CLI](https://www.npmjs.com/package/pixverse) — helps AI agents (Claude Code, Cursor, Codex, etc.) generate videos, images, audio (speech & music), MiniApp projects, and Canvas workflows through structured, composable workflows.

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

Start at [`skills/SKILL.md`](skills/SKILL.md): it routes each task to the one file it needs. Supporting Markdown files are instructions, not separate CLI commands.

- `skills/capabilities/` — one command or command group each: flags, constraints, output, recovery.
- `skills/workflows/` — multi-step deliverables that chain capabilities.
- `skills/references/` — shared contracts ([execution](skills/references/execution-contract.md), [prompt editing](skills/references/prompt-contract.md), [persistent assets](skills/references/persistent-assets.md)) and on-demand model and design references.
- `skills/scripts/` — skill update helpers and the storyboard media helper (needs ImageMagick and ffmpeg).
- `skills/examples/` — shell-specific examples, such as Windows PowerShell.

## Models and parameters

This skill documents CLI 1.4.20. Query the installed CLI instead of relying on a static catalog; these queries are offline and need no login:

```bash
pixverse capabilities create --json
pixverse capabilities create video --model v6 --json
```

Canvas nodes and MiniApp schemas are live and must be discovered separately (`pixverse capabilities canvas --node-type <type> --json`, `pixverse miniapps info <id> --json`).

## Development

Run the offline regression suite with `python3 -m unittest discover -s tests -v`. It checks source-checkout updates, documented shell recipes, result parsing, links, and storyboard command behavior without generating media or consuming credits.

## Community Skills

Projects built on top of PixVerse CLI by the community:

| Project | Author | Description |
|:---|:---|:---|
| [pixverse-character-pipeline](https://github.com/Takamasa045/pixverse-character-pipeline) | [@takamasa045](https://x.com/takamasa045) | Character-driven video production — one speaker image + YAML config → multi-language, multi-ratio talking-head videos with lip-sync, BGM, and Remotion rendering |
| [pixverse-shotpack](https://github.com/Takamasa045/pixverse-shotpack) | [@takamasa045](https://x.com/takamasa045) | Creative brief → video shot pipeline — transforms markdown briefs or YAML storyboards into organized, editor-ready AI-generated video assets |

> Have a project built on PixVerse CLI? Open a PR to add it here.

## Credits

Thanks to the creators whose work has contributed to the PixVerse ecosystem:

- [@takamasa045](https://x.com/takamasa045) — for building character pipeline and shotpack production tools on PixVerse CLI
- [@vista8](https://x.com/vista8) — for the Mondo poster design system whose prompt engineering and artist style library are adapted in the Mondo poster design capability

## Links

- [PixVerse Website](https://pixverse.ai)
- [PixVerse CLI on npm](https://www.npmjs.com/package/pixverse)
- [Subscription Plans](https://app.pixverse.ai/subscribe)
