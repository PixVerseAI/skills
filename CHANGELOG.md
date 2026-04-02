# Changelog

All notable changes to PixVerse Skills will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/).

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
