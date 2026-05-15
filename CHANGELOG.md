# Changelog

All notable changes to PixVerse Skills will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/).

## [1.9.0] - 2026-05-15

Sync with PixVerse CLI **v1.1.8**, which offlined the `create sound` command and dropped deprecated models from several creation modes.

### Removed
- **`create sound` command** — the sound effect reference was offlined upstream on 2026-04-17 and the CLI removed the subcommand in v1.1.8. Master `SKILL.md` "All Commands" table, `pixverse:post-process-video` (frontmatter, decision tree, dedicated `### create sound` section, and example), and the decision-tree branches in `pixverse:modify-video` have all been cleaned up.
- Sound-effect steps in workflow examples: `pixverse:video-production`, `pixverse:motion-control-pipeline`, `pixverse:modify-video-pipeline`, `pixverse:mondo-poster-to-video-pipeline`, plus the motion-control capability example and `examples/windows/powershell-text-to-video.ps1`. Pipelines now flow create → (extend / modify / motion-control) → upscale → download, with optional speech as the only audio post-process.

### Changed
- **Per-mode model whitelists tightened** to match CLI v1.1.8 validation:
  - `pixverse:create-video` (`create video` flags): dropped `v5.5`, `v5`, `v5-fast` from `--model`.
  - `pixverse:create-video` (`create reference` flags): dropped `v5`; default model is now `pixverse-c1`; added `grok-imagine` to the supported list.
  - `pixverse:post-process-video` (`create extend` flags): dropped `v5.5`, `v5`; remaining set is `v6` (default) and `grok-imagine`.
  - `pixverse:transition` (`create transition` flags): dropped `v5.5` and `v4.5` from the model list; the `v5.5` row was removed from the Transition-capable models table; added a dedicated `v5` row tagged **Multi-frame only**.
- `pixverse:transition` 3+ image constraint rewritten: only `v5` supports multi-frame transitions now (previously `v5` and `v4.5`). The V6/C1 multi-frame note now points to `v5` only, and the "use a specific model" example was switched to a valid 3-frame `v5` call (the old 2-frame `--model v5` example is no longer valid under the new whitelist).

### Added
- `seedream-5.0-lite` now supports `2160p` quality (CLI v1.1.8). Updated quality columns and "up to" phrasing in top-level `README.md`, master `SKILL.md` Model Quick Reference, `pixverse:create-and-edit-image` Model Reference + recommendation lines, and `pixverse:mondo-poster-design` Model Selection Guide.

### Fixed
- `pixverse:transition` Transition-capable models table and `--model` value list now include **Veo 3.1 Lite** (`veo-3.1-lite`, `720p` / `1080p`, durations `4` / `5` / `6`, `16:9` / `9:16`, first/last frame only). The model has been a valid transition target upstream for some time but the skill docs never reflected it. `pixverse:create-video` Model Reference table and `Veo 3.1 Lite` constraint note updated accordingly.

## [1.8.1] - 2026-05-06

### Added
- **`pixverse:seedance-prompt-optimize` skill** — Seedance 2.0-specific prompt optimizer for `seedance-2.0-standard` and `seedance-2.0-fast`. Model-gated with smart auto-detection: runs an 8-flag triage on every Seedance prompt and only invokes when meaningful headroom exists (missing core elements; raw paths, URLs, or `video_id` numbers in body; ambiguous multi-asset roles; camera-move conflicts; vague verbs; tokenizer-disambiguation violations; hollow filler dominance; multi-character action without position lock). Skips silently when the prompt is already clean. Produces a three-section structured rewrite (Setup → Time-Sliced Shot Script → Edit Instructions → Quality/Style/Constraint pad), grounded in the eight core elements from Volcengine's Seedance 2.0 prompt guide. Codifies canonical principles: Positional Reference Binding, Tokenizer Disambiguation, Single-Camera-Move-Per-Slice, Verb Precision Over Adjective Stacking, First-Last-Frame Anchoring, Common-Glyph Rule. For non-Seedance models, the existing `pixverse:prompt-enhance` continues to apply.
- Master `SKILL.md` capabilities table updated to register the new skill alongside `pixverse:prompt-enhance`, with the auto-trigger / skip behavior surfaced inline.

### Notes
- PixVerse's Seedance 2.0 integration does **not** accept audio as an input reference — the skill explicitly drops audio assets and avoids audio-output cues in the optimized prompt body, to stay aligned with the current pipeline surface.
- Asset references in optimized prompts bind to **positional `@imageN` / `@videoN` labels matching the CLI flag order** (`--images <p1> <p2> ...`, source video order, or `video_id`), instead of any fabricated opaque ID format.

## [1.8.0] - 2026-04-30

### Added
- **`pixverse:item-design` skill** — sister skill to `pixverse:character-design` for creating and reusing persistent key items, props, and objects across stories. Cloud-first (PixVerse `image_id` as source of truth), FS + session persistence modes, v2 registry schema, hybrid field collection (`category`, `material`, `color_palette`, `size_scale`, `era_style`, `distinctive_features`, `condition`, `style_tags`), model fallback chain (`gpt-image-2.0` → `gemini-3.1-flash` → `gemini-3.0` → `seedream-5.0-lite`). Generates a 1:1 four-panel orthographic grid (front / left / top-down / right) with a pure-white #FFFFFF background. Includes panel-sizing guidance for tall items (sword, staff, rifle), long-horizontal items (motorcycle, car, boat), flat items (book, plate, phone), and cubic / spherical items. Documents the canonical "compose with character" pattern (`pixverse create image --images <character_id> <item_id> ...`).
- README capabilities/skills tree gains `character-design.md` and `item-design.md` under `capabilities/`.
- README image models table now lists **GPT Image 2** (`gpt-image-2.0`, `1080p` / `1440p` / `2160p`, per-quality aspect-ratio map). The model was added to the CLI in v1.1.4 and to SKILL.md in v1.7.2 but the README table was never synced — fixed here.
- README video models table now lists **Veo 3.1 Lite** (`veo-3.1-lite`, `720p` / `1080p`, durations `4` `5` `6`, `16:9` / `9:16`). The model was added in v1.7.0 but the README table was never synced — fixed here.

### Changed
- **`pixverse:character-design`** — prompt-template layout instruction now requires a **pure solid white (#FFFFFF) background filling the entire canvas** (no gradient, no texture, no colored tint, no studio backdrop curve). Replaces the previous "neutral light-gray studio background" wording. The same requirement is codified in `pixverse:item-design`, so a future reader can spot the contract identically in either file. Only the soft drop shadow directly under the character's feet (or under each item view) is allowed on the background.

## [1.7.3] - 2026-04-29

### Added
- `happyhorse-1.0` video model (CLI v1.1.5) — added to SKILL.md Model Quick Reference (max `1080p`, `3`–`15`s), create-video Model Reference table and constraints (Video mode only; aspect ratios `16:9` `9:16` `1:1` `4:3` `3:4`), and README video models table.
- `grok-imagine` Extend and Reference modes (CLI v1.1.6) — updated in create-video Model Reference table, constraints note, and README; also added `grok-imagine` to `create extend --model` options in post-process-video.
- `pixverse:character-design` skill — generates a three-view character sheet (front/side/back + head detail) and persists it locally for reuse across image/video generations; registered in SKILL.md skill directory table.

### Changed
- SKILL.md frontmatter description now mentions Happy Horse alongside other video model families.

## [1.7.2] - 2026-04-24

### Added
- `gpt-image-2.0` image model (CLI v1.1.4) — added to SKILL.md Model Quick Reference (max `2160p`) and create-and-edit-image Model Reference with per-quality aspect ratio map (`1080p`: `1:1` `3:2` `2:3` · `1440p`: `1:1` `16:9` `9:16` · `2160p`: `16:9` `9:16`), max `--count 9`, plus a dedicated example.
- `--detail-level` flag on `create image` (CLI v1.1.4) — values `low` (default) / `medium` / `high`; only valid with `--model gpt-image-2.0`. Passing it with any other model or an invalid value fails with exit code 6 (validation).
- SKILL.md Output Contract: new **Universal JSON fields** section documenting that `trace_id` is auto-injected on every `--json` object payload (success on stdout, errors on stderr) from the backend `Ai-Trace-Id` header, and that error payloads additionally carry `code` (backend `ApiError` code) and `error` (message).
- SKILL.md Output Contract and create-and-edit-image: documented the new `cost_credits` field on `create …` success payloads — present **only when the API returns a positive integer** (absent for `0` / `null` / missing); in text mode it surfaces as `Cost: N credits` after `Submitted!`.
- auth-and-account: new step 8 documenting the `PIXVERSE_ACCESS_KEY` server-to-server access key env var, including auth priority order (explicit `Token` header → stored token → `PIXVERSE_ACCESS_KEY`).

### Changed
- SKILL.md Output Contract clarifies that in `--json` mode, `pixverse task …` and `pixverse template …` error payloads now correctly route to **stderr** (CLI v1.1.4 fix), preserving the stdout-is-success contract for all commands.
- SKILL.md frontmatter description now mentions GPT Image family alongside Nano Banana / Seedream / Qwen / Kling.

### Fixed
- auth-and-account: removed stale reference to `PIXVERSE_TOKEN` env var — current CLI versions ignore it; use `PIXVERSE_ACCESS_KEY` instead.

## [1.7.1] - 2026-04-20

### Added
- `veo-3.1-lite` video model (CLI v1.1.1) — added to SKILL.md Model Quick Reference and create-video Model Reference (720p / 1080p, durations 4 / 5 / 6, `16:9` and `9:16` only, Video mode only)
- `seedance-2.0-standard` now supports `1080p` quality (CLI v1.1.2) — updated quality column in SKILL.md and create-video Model Reference

### Changed
- create-video, asset-management, motion-control: documented new auto-compression behavior (CLI v1.1.3) — local images exceeding `1920×1920` or `5 MB` are auto-resized and re-encoded before upload; agents no longer need to pre-compress
- create-video, asset-management: clarified that remote inputs accept only `https://` URLs (`http://` is rejected)
- auth-and-account: documented browser auto-open behavior — interactive mode opens the authorization URL in the system default browser; `--json` / `-p` modes suppress browser opening to keep automation side-effect-free

## [1.7.0] - 2026-04-13

### Added
- 6 new video models: Seedance 2.0 Standard/Fast, Kling O3 Pro/Standard, Kling 3.0 Pro/Standard — with full parameter constraints documented in create-video, transition, and master SKILL.md
- 2 new image models: Kling Image O3, Kling Image V3 — added to create-and-edit-image with reference image limits
- Saved folders capability (`pixverse:saved-folders`) — organize assets into named folders with list, items, new, rename, add, remove, delete commands
- `asset upload` command in asset-management — upload local files or HTTPS URLs to the asset library
- `--source` filter (create/upload) and `--off-peak` filter on `asset list`

### Changed
- Updated SKILL.md frontmatter description to include Seedance and Kling model families
- Updated Model Quick Reference tables in SKILL.md with all new video and image models
- Updated All Commands table with `asset upload` and all `saved` subcommands
- Capabilities Overview table now includes saved-folders skill
- Reference (fusion) mode model list expanded with Seedance 2.0 and Kling O3 models

## [1.6.0] - 2026-04-10

### Added
- Motion control capability (`pixverse:motion-control`) — generate camera motion-controlled videos via `create motion-control` command (CLI v1.0.10)
- `motion-control-pipeline` workflow skill for end-to-end motion control video production
- Storyboard-to-video workflow (`pixverse:storyboard-to-video`) — decompose prompt into multi-shot storyboard, generate frames, run parallel I2V generations, and concatenate with ffmpeg
- `pixverse-c1` model added to create-video, transition, and master SKILL.md model references (CLI v1.0.12)
- Batch partial failure (exit code 6) documented in `batch-creation` workflow

### Changed
- Improved modify-video skill trigger conditions — clarified AI content modification vs traditional editing, added concrete trigger examples
- Clarified audio and multi-shot toggle flags in create-video capability
- Updated README with all new skills and pixverse-c1 model

### Fixed
- Removed undocumented `PIXVERSE_TOKEN` env var reference from SKILL.md and auth-and-account docs

## [1.5.0] - 2026-04-03

### Added
- Prompt enhancement capability (`pixverse:prompt-enhance`) — optimize user prompts for V6 video generation with improved structure, verb precision, and multi-shot sequencing

### Changed
- All skill examples aligned with V6 as default model (commands updated from `--model v5.6` to `--model v6`)
- Removed phantom models (Kling, Hailuo, Wan) from SKILL.md frontmatter that were never shipped
- Config defaults examples updated to use V6

## [1.4.0] - 2026-04-02

### Added
- Video modification capability (`pixverse:modify-video`) — AI-powered content modification: replace subjects, swap outfits, change backgrounds in existing videos (CLI v1.0.9)
- `modify-video-pipeline` workflow skill for end-to-end video modification

### Changed
- `create-video` capability updated with cross-reference to modify-video
- `post-process-video` updated with modify-video context

## [1.3.0] - 2026-04-01

### Added
- Workspace management capability (`pixverse:workspace`) — list, switch, check status, and open management page for personal and team workspaces
- Global `--workspace-id` flag documented in master SKILL.md for per-command workspace override
- Workspace error auto-recovery documented in exit codes section

### Changed
- `account info` JSON output now includes `workspace` object and team credits (`credits.used`, `workspace.seats`)
- `account usage` behavior documented for team workspaces (different item fields, `--type` filter restriction)
- `auth login` / `auth status` / `auth logout` JSON output schemas updated to match CLI v1.0.7
- `subscribe` command now documented with team workspace guard (exits code 6 in team context)
- `batch-creation` workflow updated with workspace context and cross-workspace example

## [1.2.0] - 2026-03-30

### Changed
- PixVerse V6 is now the default video model across all skills
- Updated model lists to match CLI source: video (`v6, v5.6, v5.5, v5, v5-fast`), extend (`v6, v5.5, v5`), reference (`v5, v5.6`), transition (`v6, v5.6, v5.5, v5, v4.5, veo-3.1-*`)
- V6 supports duration 1–15s, aspect ratio includes `21:9`, native audio and multi-shot
- V6 transition limited to first/last frame only — documented in transition and create-video skills
- V6 does not support multi-subject reference (fusion) — documented with fallback guidance
- Removed deprecated models (`v4, v3.5`) from video mode model lists

## [1.1.0] - 2026-03-30

### Added
- Mondo poster design capability (`pixverse:mondo-poster-design`) — generate Mondo-style posters, book covers, and album covers with 37 artist styles, composition patterns, and genre templates
- 2 workflow skills: `pixverse:mondo-poster-pipeline` (end-to-end poster generation), `pixverse:mondo-poster-to-video-pipeline` (animate poster into cinematic video)
- `references/` directory for curated design knowledge, starting with `references/mondo-poster/` (artist-styles, composition-patterns, genre-templates)
- Reference Materials section in master SKILL.md

### Credits
- Mondo poster design adapted from [qiaomu-mondo-poster-design](https://github.com/joeseesun/qiaomu-mondo-poster-design) by [@vista8](https://x.com/vista8), with image generation replaced by PixVerse CLI

## [1.0.0] - 2026-03-24

### Added
- Master skill (`SKILL.md`) with full CLI reference, model tables, and output contract
- 8 capability skills: auth-and-account, create-video, create-and-edit-image, post-process-video, transition, template, task-management, asset-management
- 6 workflow skills: text-to-video-pipeline, image-to-video-pipeline, text-to-image-to-video, image-editing-pipeline, video-production, batch-creation
- PowerShell example script for Windows users (`skills/examples/windows/`)
- Version checking mechanism (`skills/scripts/check-update.sh`, `skills/scripts/update.sh`)
- VERSION file and CHANGELOG
