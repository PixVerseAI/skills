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

```
skills/
  SKILL.md                          # Entry point — start here
  capabilities/                     # Individual command skills
    auth-and-account.md             #   Authentication & account management
    create-video.md                 #   Text-to-video, image-to-video, fusion
    create-and-edit-image.md        #   Text-to-image, image-to-image
    create-voice.md                 #   Text-to-speech (TTS) — MiniMax, ElevenLabs voices
    create-music.md                 #   Prompt-to-music — MiniMax, ElevenLabs, Google Lyria
    modify-video.md                 #   AI content editing (replace subjects, swap outfits, change backgrounds)
    motion-control.md               #   Character animation with motion reference video
    transition.md                   #   Keyframe transition animations
    post-process-video.md           #   Extend duration, upscale resolution
    prompting-guide.md              #   Model-agnostic prompt advice (advice only — never auto-edits)
    prompt-enhance.md               #   Prompt optimization for V6 video generation
    seedance-prompt-optimize.md     #   Prompt optimization for Seedance 2.0 / 2.5
    seedance-vibe-creating.md       #   Vibe Creating — distill emotional / atmospheric ideas into Seedance prompts
    task-management.md              #   Poll and wait for generation tasks
    asset-management.md             #   List, download, upload, delete assets
    saved-folders.md                #   Organize assets into named folders
    template.md                     #   Browse and create from effect templates
    miniapps.md                     #   Discover and run PixVerse MiniApps
    capabilities.md                 #   Offline Create registry + live Canvas capability queries
    canvas.md                       #   Connected Canvas generation graphs
    workspace.md                    #   Team workspace management
    mondo-poster-design.md          #   Mondo-style poster, book cover, album art design
    character-design.md             #   Persistent characters — three-view sheet + cloud asset id reuse
    item-design.md                  #   Persistent items / props — four-panel orthographic sheet + cloud asset id reuse
  workflows/                        # Multi-step pipeline skills
    text-to-video-pipeline.md       #   End-to-end text-to-video
    image-to-video-pipeline.md      #   Animate an image into video
    text-to-image-to-video.md       #   Generate image then animate it
    image-editing-pipeline.md       #   Iterative image editing
    modify-video-pipeline.md        #   Modify video content then enhance
    motion-control-pipeline.md      #   Character animation end-to-end
    video-production.md             #   Full production (create + extend + audio + upscale)
    storyboard-to-video.md          #   Multi-shot storyboard → concatenated video
    batch-creation.md               #   Parallel batch generation
    mondo-poster-pipeline.md        #   End-to-end Mondo poster generation
    mondo-poster-to-video-pipeline.md #  Animate poster into cinematic video
  scripts/                          # Update helpers and local storyboard media processing
  references/                       # Shared contracts and on-demand model/design knowledge
    execution-contract.md           #   Results, waiting, task IDs, and retries
    prompt-contract.md              #   Rewrite scope and user constraints
    persistent-assets.md            #   Shared character/item registry protocol
    video-models.md                 #   Static video model fallback
    video-reference.md              #   Mixed reference media rules
    image-models.md                 #   Static image model fallback
    mondo-poster/                   #   33 artist styles, composition, genre templates
```

### Capabilities vs Workflows

- **Capabilities** document a single command or command group — flags, models, parameter constraints, JSON output format, error codes.
- **Workflows** compose multiple capabilities into end-to-end pipelines with step-by-step instructions.

## MiniApps

PixVerse CLI v1.3.0 adds a top-level `miniapps` group for preset generators. Discover the live catalog and schema before submitting a project:

```bash
pixverse miniapps list --json
pixverse miniapps info magic_extend --json
pixverse miniapps create \
  --id magic_extend \
  --params '{"image":"<media-path>","ratio":"16:9"}' \
  --no-wait \
  --json
```

Creation returns a `project_id`. Use it with `task` and `asset`, always passing `--type miniapps`:

```bash
pixverse task wait <project_id> --type miniapps --json
pixverse asset download <project_id> --type miniapps --json
```

See `skills/capabilities/miniapps.md` for normalized `params_schema` fields, media-path handling, output contracts, and the full project lifecycle.

## Capabilities and Canvas

PixVerse CLI v1.4.0 adds offline Create discovery and a top-level `canvas` group. Query the installed CLI instead of copying a static catalog:

```bash
pixverse capabilities --json
pixverse capabilities create video --model v6 --json
pixverse capabilities canvas --node-type image_generate --json
```

`capabilities` / `capabilities create` need no login. `capabilities canvas` is live and merges Canvas routes with the installed Create registry. Do not invent Canvas `node_type` mappings.

Typical Canvas automation:

```bash
pixverse canvas project create --json
pixverse canvas graph get --project-id "$PROJECT_ID" --json
pixverse canvas patch dry-run --project-id "$PROJECT_ID" --patch patch.json --json
pixverse canvas patch apply --project-id "$PROJECT_ID" --patch patch.json --json
pixverse canvas dispatch --project-id "$PROJECT_ID" --node-ids image_01 --edit-version 13 --json
```

See `skills/capabilities/capabilities.md` and `skills/capabilities/canvas.md`.

## Models and parameters

For CLI 1.4.0+, query the installed registry rather than maintaining another model catalog here:

```bash
pixverse capabilities create --json
pixverse capabilities create video --model v6 --json
pixverse capabilities create image --model gpt-image-2.5-flare --json
```

Queries are offline. Older CLI versions need their installed command help and version-compatible references; this skill documents CLI 1.4.1. Static model tables remain in the relevant [capabilities](skills/SKILL.md#select-an-operation) as an on-demand reference. Canvas and MiniApp schemas are live and must be discovered separately.

## For AI Agent Developers

Load [skills/SKILL.md](skills/SKILL.md) first, then only the capability or workflow needed for the request. Supporting Markdown files are not separate CLI commands.

Shared contracts keep execution and creative rules consistent:

- [Execution](skills/references/execution-contract.md): result shapes, task identity, waiting, and retries.
- [Prompt editing](skills/references/prompt-contract.md): advice versus authorized rewriting, model strategy, and user constraints.
- [Persistent assets](skills/references/persistent-assets.md): character/item registries, imports, caching, and region-aware fallback.

Workflows retain their original paths. The storyboard workflow uses a local Python helper for crop/concat operations; ImageMagick and ffmpeg are needed only for those media operations.

Run the offline regression suite with `python3 -m unittest discover -s tests -v`. It checks source-checkout updates, documented shell recipes, result parsing, and storyboard command behavior without generating media or consuming credits. Real ffmpeg/ImageMagick and PowerShell integration require those tools separately.

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
- [@vista8](https://x.com/vista8) — for the Mondo poster design system whose prompt engineering and artist style library are adapted in `pixverse:mondo-poster-design`

## Links

- [PixVerse Website](https://pixverse.ai)
- [PixVerse CLI on npm](https://www.npmjs.com/package/pixverse)
- [Subscription Plans](https://app.pixverse.ai/subscribe)
