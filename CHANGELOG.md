# Changelog

All notable changes to PixVerse Skills will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/).

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
