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
  references/                       # Curated design knowledge
    mondo-poster/                   #   37 artist styles, composition, genre templates
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

## Supported Models

### Video Models

| Model | CLI value | Modes | Quality | Duration | Aspect Ratio |
|:---|:---|:---|:---|:---|:---|
| PixVerse V6 | `v6` (default) | Video, Transition (first/last frame), Extend, Reference | `360p` `540p` `720p` `1080p` | `1`-`15` (any integer; Reference video uses `auto`) | `auto` `16:9` `4:3` `1:1` `3:4` `9:16` `3:2` `2:3` `21:9` (Reference supports `auto`) |
| PixVerse C1 | `pixverse-c1` | Video, Transition (first/last frame), Reference | `360p` `540p` `720p` `1080p` | `1`-`15` (any integer) | `16:9` `4:3` `1:1` `3:4` `9:16` `3:2` `2:3` |
| PixVerse v5.6 | `v5.6` | Video, Transition, Reference, Motion Control | `360p` `480p` `540p` `720p` `1080p` | `1`-`10` (any integer) | `16:9` `4:3` `1:1` `3:4` `9:16` `3:2` `2:3` |
| Sora 2 | `sora-2` | Video | `720p` | `4` `8` `12` | `16:9` `9:16` |
| Sora 2 Pro | `sora-2-pro` | Video | `720p` `1080p` | `4` `8` `12` | `16:9` `9:16` |
| Veo 3.1 Standard | `veo-3.1-standard` | Video, Transition | `720p` `1080p` `2160p` | `4` `6` `8` | `16:9` `9:16` |
| Veo 3.1 Fast | `veo-3.1-fast` | Video, Transition | `720p` `1080p` `2160p` | `4` `6` `8` | `16:9` `9:16` |
| Veo 3.1 Lite | `veo-3.1-lite` | Video, Transition | `720p` `1080p` | `4` `6` `8` | `16:9` `9:16` |
| Grok Imagine | `grok-imagine` | Video, Extend, Reference | `480p` `720p` | `1`-`15` (Reference video uses `auto`) | fixed ratios normally; Reference video derives framing from source |
| Grok Imagine 1.5 | `grok-imagine-1.5` | Video (image-to-video only) | `480p` `720p` `1080p` | `1`-`15` | derived from input image |
| Happy Horse 1.0 | `happyhorse-1.0` | Video | `720p` `1080p` | `3`-`15` | `16:9` `9:16` `1:1` `4:3` `3:4` |
| Seedance 2.5 | `seedance-2.5` | Video, Reference, Transition (exactly 2 frames) | `480p` `720p` `1080p` | `4`-`30` (Reference video also `auto`) | `auto` `21:9` `16:9` `4:3` `1:1` `3:4` `9:16` (mode-dependent) |
| Seedance 2.0 Standard | `seedance-2.0-standard` | Video, Reference, Transition | `480p` `720p` `1080p` `2160p` | `4`-`15` | `16:9` `4:3` `1:1` `3:4` `9:16` `21:9` |
| Seedance 2.0 Fast | `seedance-2.0-fast` | Video, Reference, Transition | `480p` `720p` | `4`-`15` | `16:9` `4:3` `1:1` `3:4` `9:16` `21:9` |
| Seedance 2.0 Mini | `seedance-2.0-mini` | Video, Reference, Transition | `480p` `720p` | `4`-`15` | `16:9` `4:3` `1:1` `3:4` `9:16` `21:9` |
| MiniMax H3 | `minimax-h3` | Video, Reference, Transition (exactly 2 frames) | `768p` `1440p` | `5`-`15` | `auto` `21:9` `16:9` `4:3` `1:1` `3:4` `9:16` (mode-dependent) |
| FLUX 3 | `flux-3.0` | Video | `720p` `1080p` | `5`-`20` | `auto` `21:9` `2:1` `16:9` `4:3` `1:1` `3:4` `9:16` |
| Wan 3.0 | `wan-3.0` | Video, Reference, Transition (exactly 2 frames) | `480p` `720p` `1080p` | `2`-`30` (Reference video also `auto`) | `auto` `16:9` `4:3` `1:1` `3:4` `9:16` |
| Kling O3 Pro | `kling-o3-pro` | Video, Reference, Transition | model-selected (`--quality` omitted) | `3`-`15` | `16:9` `9:16` `1:1` |
| Kling O3 Standard | `kling-o3-standard` | Video, Reference, Transition | model-selected (`--quality` omitted) | `3`-`15` | `16:9` `9:16` `1:1` |
| Kling O3 4K | `kling-o3-4k` | Video, Reference, Transition | model-selected 4K tier (`--quality` omitted) | `3`-`15` | `16:9` `9:16` `1:1` |
| Kling 3.0 Pro | `kling-3.0-pro` | Video, Transition | model-selected (`--quality` omitted) | `3`-`15` | `16:9` `9:16` `1:1` |
| Kling 3.0 Standard | `kling-3.0-standard` | Video, Transition | model-selected (`--quality` omitted) | `3`-`15` | `16:9` `9:16` `1:1` |
| Kling 3.0 4K | `kling-3.0-4k` | Video, Transition | model-selected 4K tier (`--quality` omitted) | `3`-`15` | `16:9` `9:16` `1:1` |
| Google Gemini Omni | `gemini-omni-flash` | Video, Reference | `720p` | `3`-`10` | `16:9` `9:16` |

> MiniMax H3 defaults to `1440p`. Text-to-video defaults to `16:9` and rejects `auto`; image-to-video forces `auto`. Reference requests with images default to `auto` but preserve an explicit fixed ratio; reference requests without images default to `16:9` and reject `auto`.

> FLUX 3 is available only in `create video`. Text-to-video defaults to `16:9`; image-to-video defaults to `auto` while preserving an explicit fixed ratio. Generated audio is optional; multi-shot and off-peak are unsupported.

> Wan 3.0 defaults to `720p`, 5 seconds, and `auto`, and is available in video, two-frame transition, and reference creation. Reference accepts up to 10 images, 5 videos, and 5 audios (20 total), including audio-only input. Video and audio reference durations are each limited to 15 seconds in aggregate. With a video reference, duration defaults to `auto`; a fixed output duration is limited by `30 - reference video duration`. Transition requires exactly two images and a prompt and has no selectable aspect ratio.

> Seedance 2.5 supports `480p`, `720p`, and `1080p` and defaults to `720p`, 5 seconds, and `16:9` without a reference video. Text-to-video and Reference accept `--aspect-ratio auto`; Reference with a video defaults to `--duration auto`, which locks framing to `auto`, while an explicit `4`–`30s` duration allows either automatic or fixed framing. Reference also accepts `--task-type auto|reference|edit|extend` (`auto` by default). It accepts up to 50 mixed references (30 images, 10 videos, and 10 audios), with separate 30-second aggregate limits for video and audio. Transition requires exactly two images and a prompt and has no selectable aspect ratio. Generated audio, multi-shot, and off-peak generation are unsupported.

> Kling resolution is selected by the model ID. All Kling video requests omit `quality`; an explicit `--quality` value is ignored with a warning. The `kling-o3-4k` tier supports Video, Reference, and Transition, while `kling-3.0-4k` supports Video and Transition.

> Reference video editing is model-specific: V6 accepts up to 10 images / 2 videos; Gemini Omni up to 5 images / 1 video; Kling O3 (including the 4K tier) up to 7 images without video or 4 images with 1 video; Grok Imagine accepts either 1–7 images or exactly 1 video; Wan 3.0 accepts up to 10 images / 5 videos / 5 audios (20 total), including audio-only. V6, Gemini Omni, and Grok video inputs lock duration to `auto`; Grok video framing is source-derived and no aspect-ratio parameter is sent. See `skills/capabilities/create-video.md` for full media constraints.

### Image Models

| Model | CLI value | Resolution | Aspect Ratio |
|:---|:---|:---|:---|
| Qwen Image | `qwen-image` | `720p` `1080p` | `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| GPT Image 2 | `gpt-image-2.0` | `1080p` `1440p` `2160p` | `1:1` `16:9` `9:16` `4:3` `3:4` `3:2` `2:3` `2:1` `1:2` `21:9` |
| Seedream 5.0 Pro | `seedream-5.0-pro` | `1080p` `1440p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Seedream 5.0 Lite | `seedream-5.0-lite` | `1440p` `1800p` `2160p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Seedream 4.5 | `seedream-4.5` | `1440p` `2160p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Seedream 4.0 | `seedream-4.0` | `1080p` `1440p` `2160p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Gemini 2.5 Flash (aka Nanobanana) | `gemini-2.5-flash` | `1080p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Gemini 3.0 (aka Nano Banana Pro) | `gemini-3.0` | `1080p` `1440p` `2160p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Gemini 3.1 Flash (aka Nano Banana 2) | `gemini-3.1-flash` | `512p` `1080p` `1440p` `2160p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Gemini 3.1 Flash Lite (aka Nano Banana 2 Lite) | `gemini-3.1-flash-lite` | `1080p` | `auto` `1:1` `3:2` `2:3` `3:4` `4:3` `4:5` `5:4` `9:16` `16:9` `21:9` |
| Kling Image O3 | `kling-image-o3` | `1080p` `1440p` `2160p` | `16:9` `9:16` `1:1` `4:3` `3:4` `3:2` `2:3` `21:9` |
| Kling Image V3 | `kling-image-v3` | `1080p` `1440p` | `16:9` `9:16` `1:1` `4:3` `3:4` `3:2` `2:3` `21:9` |

### Voice / TTS Models

| Model | CLI value | Provider | Max characters |
|:---|:---|:---|---:|
| MiniMax Speech 2.8 HD | `speech-2.8-hd` (default) | MiniMax | 10,000 |
| MiniMax Speech 2.8 Turbo | `speech-2.8-turbo` | MiniMax | 10,000 |
| Eleven Multilingual v2 | `eleven-multilingual-v2` | ElevenLabs | 10,000 |
| Eleven v3 | `eleven-v3` | ElevenLabs | 5,000 |
| Eleven Turbo v2.5 | `eleven-turbo-v2.5` | ElevenLabs | 40,000 |

### Music Models

| Model | CLI value | Provider | Explicit lyrics | Auto lyrics | Instrumental | Image ref |
|:---|:---|:---|:---|:---|:---|:---|
| MiniMax Music 3.0 | `music-3.0` | MiniMax | Yes | Yes | Yes | No |
| MiniMax Music 2.6 | `music-2.6` (default) | MiniMax | Yes | Yes | Yes | No |
| ElevenLabs Music V2 | `music-v2` | ElevenLabs | Yes | Yes | Yes | No |
| ElevenLabs Music | `music-v1` | ElevenLabs | Yes | Yes | Yes | No |
| Google Lyria 3 Pro | `lyria-3-pro-preview` | Google | No | Yes | Yes | Up to 10 |

## For AI Agent Developers

These skills are designed to be loaded into agent context. Each skill file is self-contained with:

- **Decision trees** — help the agent choose the right command
- **Flag tables** — every parameter with allowed values and defaults
- **Model reference tables** — per-model parameter constraints
- **JSON output schemas** — exact response format for parsing
- **Exit codes** — deterministic error handling
- **Examples** — copy-paste-ready commands

Start by loading `skills/SKILL.md` as the entry point, then load specific capability or workflow skills as needed.

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
