# Changelog

All notable changes to PixVerse Skills will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/).

## [1.26.0] - 2026-09-07

### Changed
- Reduce the entrypoint to task routing, version-aware discovery, and execution essentials; replace duplicate README model catalogs with installed-registry queries.
- Share execution, prompt-editing, and persistent-asset contracts across capabilities; preserve model-specific constraints and design references on demand.
- Shorten workflows while preserving their paths; reuse completed results and shared production steps.
- Move storyboard cropping and concatenation into a local helper with ImageMagick 6/7 support and missing-audio handling.

### Fixed
- Prevent duplicate generation in result-parsing recipes; document single, batch, partial, and task-query outputs accurately.
- Correct Seedance extension routing, required voice selection, stdin parsing, and failure propagation.
- Preserve explicit prompt constraints, align character/item region fallback, and reconcile multi-view references with Seedance input preparation.
- Make source updates clean-main and fast-forward only; cancellation never stashes changes, and update checks do not suggest downgrades.
- Update the Windows example's runtime requirement and result checks; add offline regression coverage.

## [1.25.0] - 2026-09-07

Sync the skill docs to PixVerse CLI **v1.4.0**.

### Added
- Add `pixverse:capabilities` for offline Create discovery (`capabilities`, `capabilities create [mode] [--model]`) and live Canvas+CLI queries (`capabilities canvas`, including `--raw`, `--node-type`, `--selector`, and `--model`).
- Add `pixverse:canvas` for the top-level Canvas command group: project create, graph inspect/status/reconcile, node schema/versions/rerun/extract-audio, patch dry-run/apply, dispatch, and dispatch rebind.
- Document the agent Canvas workflow (capabilities → graph get → dry-run → apply → dispatch exact `executable_node_ids` → status) and the invariants that matter at the CLI surface: string IDs, `edit_version` locking, fail-closed adapter merges, dependency replace-via-delete, and `video_compose` remaining edge-free.

### Changed
- Point model and parameter lookup at `pixverse capabilities create` as the installed-CLI source of truth, and tell agents not to copy a static Canvas node catalog.
- Extend the master command index, README skill map, and idempotency-key guidance to cover Canvas patches.

## [1.24.0] - 2026-09-06

Sync the skill docs to PixVerse CLI **v1.3.10**, covering CLI v1.3.6–v1.3.10.

### Added
- Add FLUX 3 (`flux-3.0`) for text-to-video and image-to-video: `720p` / `1080p`, integer durations from `5` through `20` seconds, Auto plus fixed aspect ratios including `2:1`, and optional generated audio. Text-to-video defaults to `16:9`; image-to-video defaults to `auto`.
- Add Wan 3.0 (`wan-3.0`) for video, two-frame transition, and mixed-media reference: `480p` / `720p` / `1080p`, integer durations from `2` through `30` seconds, Auto plus fixed aspect ratios, and optional generated audio. Reference accepts up to 10 images / 5 videos / 5 audios (20 total), including audio-only input.
- Document the global `--region global|cn` flag (default `global`; `PIXVERSE_REGION` overrides) and CN-region capability differences: isolated login state, blocked standalone audio commands, and the CN model allowlist.

### Changed
- Extend the master model lists, create-video reference matrix, transition tables, and character-design mixed-input guidance with FLUX 3 and Wan 3.0.

### Fixed
- Document that an invalid `PIXVERSE_ACCESS_KEY` (backend code `10004`) is treated as an authentication error (exit code 3), matching an expired token.

## [1.23.0] - 2026-08-19

Sync the skill docs to PixVerse CLI **v1.3.5**, covering CLI v1.3.3–v1.3.5.

### Added
- Add Seedance 2.5 `create reference --task-type auto|reference|edit|extend` guidance; `auto` remains the default and the flag is rejected for other models.
- Add the `kling-o3-4k` Video / Reference / Transition model tier and the `kling-3.0-4k` Video / Transition model tier.
- Add MiniMax Music 3.0 (`music-3.0`) and ElevenLabs Music V2 (`music-v2`), both with explicit lyrics, auto lyrics, instrumental generation, and 10–240-second durations; `music-2.6` remains the default.
- Add `1080p` support for Seedance 2.5 across Video, Reference, and exactly-two-frame Transition, and for Grok Imagine 1.5 image-to-video.

### Changed
- Raise the documented PixVerse CLI runtime requirement from Node.js 20 to Node.js 22.12.
- Document that Kling resolution is selected by model ID: all Kling video requests omit `quality`, and an explicit `--quality` is ignored with a warning.

### Fixed
- Correct Gemini Omni and Grok Imagine reference-video guidance: video inputs lock duration to `auto` and reject fixed values; Grok omits the aspect-ratio parameter and derives framing from the source video.

## [1.22.0] - 2026-08-11

Sync the skill docs to PixVerse CLI **v1.3.2**.

### Added
- Expand `create reference` video editing guidance with a model-specific media matrix: V6 supports up to 10 images / 2 videos, Gemini Omni up to 5 images / 1 video, Kling O3 up to 7 images or 4 images plus 1 video, and Grok Imagine either 1–7 images or exactly 1 video.
- Document known-media validation for reference videos, including model-specific format, duration, total-duration, file-size, and dimension limits.
- Add `--duration auto` guidance for V6 and Seedance 2.5 video references, and `--aspect-ratio auto` guidance for Seedance 2.5 text-to-video and reference generation.

### Changed
- Document duration/aspect-ratio derivation: V6 video references lock duration to `auto`; Seedance 2.5 video references default to `auto` but allow fixed `4`–`30s`; Gemini Omni and Grok derive duration from known source metadata; Grok video references force `auto` framing.
- Update Kling O3 quality guidance to `720p` / `1080p` across video, reference, and transition tables.

## [1.21.0] - 2026-08-07

Sync the skill docs to PixVerse CLI **v1.3.1**.

### Added
- Add Seedance 2.5 (`seedance-2.5`) to video, reference, and exactly-two-frame transition guidance, with `480p` / `720p`, integer durations from `4` through `30` seconds, and its six fixed aspect ratios.
- Document Seedance 2.5 mixed-reference limits: up to 30 images, 10 videos, and 10 audios, capped at 50 total inputs, with separate 30-second aggregate limits for video and audio.

### Changed
- Make the Seedance prompt optimizer, Vibe Creating, character-design, and prompting-guide routing recognize both Seedance 2.0 and Seedance 2.5 while preserving model-specific CLI limits.
- Clarify that Seedance 2.5 defaults to `720p`, 5 seconds, and `16:9`, and does not support generated audio, multi-shot, or off-peak generation.

### Fixed
- Document that Seedance 2.5 transitions require exactly two images and a non-empty prompt, and do not accept a user-selected aspect ratio.

## [1.20.0] - 2026-08-05

Sync the skill docs to PixVerse CLI **v1.3.0**, including the image-template fix released in CLI v1.2.13.

### Added
- Add the `pixverse:miniapps` capability for discovering live MiniApps, reading the normalized `params_schema`, constructing required JSON arguments, creating projects, and managing their outputs.
- Document the top-level `miniapps list`, `miniapps info <id>`, and `miniapps create --id <app_id> --params <json>` commands, including literal, file, and stdin parameter inputs.
- Document `--type miniapps` across `task status`, `task wait`, and MiniApp-aware asset list, info, download, and delete operations using `project_id`.

### Changed
- Extend the master command index, README, task guidance, and asset guidance with the MiniApp project lifecycle and machine-readable output contracts.
- Clarify that MiniApp upload parameters take PixVerse media paths returned by `asset upload`, and that project asset operations require explicit `--type miniapps`.

### Fixed
- Document that `create template` now supplies a random seed for image templates when `--seed` is omitted, preventing backend `invalid param` failures.

## [1.19.0] - 2026-08-03

Sync the skill docs to PixVerse CLI **v1.2.12**.

### Added
- Add `768p` as a supported MiniMax H3 (`minimax-h3`) video quality alongside `1440p`; the default remains `1440p`.

### Fixed
- Clarify MiniMax H3 aspect-ratio handling by mode: image-to-video still forces `auto`; reference requests with images default to `auto` but preserve an explicit fixed `--aspect-ratio`; reference requests without images default to `16:9` and reject `auto`.

## [1.18.0] - 2026-07-31

Sync the skill docs to PixVerse CLI **v1.2.11**.

### Added
- **MiniMax H3 (`minimax-h3`)** video model — available in text/image-to-video, reference, and exactly-two-frame transition modes; fixed `1440p`, duration `5`–`15s`, and H3-specific aspect-ratio behavior.
- Document MiniMax H3 mixed references: up to 9 images, 3 videos, and 3 audios, with audio requiring at least one visual reference.

### Changed
- Distinguish MiniMax H3 mixed-reference validation from Seedance 2.0: H3 enforces reference counts but defers reference-media format, file-size, dimensions/aspect-ratio, and clip-duration constraints to shared upload/backend rules.
- Clarify that H3 does not generate audio, does not support multi-shot or off-peak mode, and requires prompts in every supported creation mode.

## [1.17.0] - 2026-07-14

Sync the skill docs to PixVerse CLI **v1.2.10**.

### Added
- Document parallel `task status` queries with space-separated positional IDs while retaining the comma-separated `--ids` syntax, including de-duplication, per-ID result maps, and deterministic mixed-error precedence.
- Add exit code `7` (`CONCURRENCY_LIMIT`) to the master contract and generation capabilities, with agent guidance to wait for a slot and safely retry instead of treating it as insufficient credits.

### Changed
- Update `create upscale` guidance to its fixed `2160p` target/default and all four supported video inputs: local file, HTTPS URL, video ID, and media path.
- Update every upscale workflow and PowerShell example from the now-invalid `1080p` target to `2160p`.

## [1.16.1] - 2026-07-13

Sync the music guidance to PixVerse CLI **v1.2.9**.

### Fixed
- Document that every music model, including Google Lyria 3 Pro (`lyria-3-pro-preview`), supports `--auto-lyrics`; Lyria still rejects the separate `--lyrics` flag.
- Document Web-aligned music flag precedence: `--instrumental` forces `auto_lyrics=false` and omits lyrics; otherwise `--auto-lyrics` omits explicitly supplied lyrics.
- Split the music model tables into explicit-lyrics, auto-lyrics, and instrumental support so Lyria's capabilities are unambiguous.

## [1.16.0] - 2026-07-10

Sync the skill docs to PixVerse CLI **v1.2.8** and reconcile the command/model tables with the CLI's generated capability manifest and validation rules.

### Added
- **Seedream 5.0 Pro (`seedream-5.0-pro`)** image model — `1080p` / `1440p`, the standard Seedream aspect-ratio set, and up to 10 reference images for I2I.
- `create modify --images <inputs...>` — up to 5 reference images, addressable from the prompt as `@image1`, `@image2`, and so on.
- Audio toggles for `create extend`, `create reference`, and `create transition`, plus the missing per-command safe-retry (`--idempotency-key`) entries.

### Fixed
- Correct Veo 3.1 Standard/Fast maximum quality to `2160p`, and Veo 3.1 Lite durations to `4` / `6` / `8`.
- Correct GPT Image 2 guidance: `--detail-level` is optional and defaults to `low`; `--count` remains `1`–`4`; 9 is the I2I reference-image limit; aspect ratios follow the CLI's model-level list.
- Correct Extend's model-specific quality/duration/audio behavior, remove the stale claim that `v5.6` supports Extend, and document the direct `config defaults` shorthand.
- Replace invalid `asset download --output` examples with `--dest` and consume the returned local file path when muxing audio.

## [1.15.0] - 2026-07-06

Sync the skill docs to PixVerse CLI **v1.2.7** — add the new Gemini Omni and Nano Banana 2 Lite models.

### Added
- **Gemini Omni Flash (`gemini-omni-flash`)** video model — available in `create video` and `create reference`; `720p`, duration `3`–`10s` (default `5`), aspect ratios `16:9`/`9:16`, max 5 reference images in `create reference`.
- **Nano Banana 2 Lite (`gemini-3.1-flash-lite`)** image model — `1080p` resolution, full aspect-ratio range including `auto`/`21:9`, up to 14 reference images for I2I.

## [1.14.0] - 2026-06-29

A new `prompting-guide` skill — a model-agnostic, advice-only layer that reviews a generation prompt, shows the user a stronger alternative side by side with their original, and explains why, but **never edits the prompt without explicit consent**. Where `prompt-enhance` and `seedance-prompt-optimize` produce a model-specific rewrite, `prompting-guide` is the universal front door: it diagnoses, suggests, and waits.

### Added
- **`pixverse:prompting-guide` capability** — model-agnostic prompt advisory built on seven cross-model principles for how transformer video models read a prompt: shorter-beats-longer (front-loaded ~50–80-word, 3-sentence structure), "cinematic" / generic-quality words sample too broad a distribution (name a director / lighting / lens spec instead), camera moves are sequential vectors so stacking them causes jitter, there are no negative prompts (convert to positive constraints), "fast" degrades complex motion (describe the physics of speed instead), and re-describing an uploaded reference image causes subject drift (image-to-video prompts should carry motion + camera only). Enforces a Cardinal Rule — the prompt sent to generation is the user's verbatim original unless the user *explicitly* accepts a suggestion — backed by a consent table and a red-flags list against silent rewriting. Emits a single Current / Suggested / Why advisory card and hands off to `prompt-enhance` (V6) / `seedance-prompt-optimize` / `seedance-vibe-creating` for model-specific rewrites. Registered in the master `SKILL.md` capabilities table and the `README.md` skill tree.

## [1.13.0] - 2026-06-28

A new `seedance-vibe-creating` skill — the experiential counterpart to `seedance-prompt-optimize`. Where the optimizer engineers precise multi-modal / multi-shot control, Vibe Creating decides whether a Seedance 2.0 idea suits creative distillation and purifies emotional, atmospheric, memory, or mixed-expression inputs into experience-first prompts, while preserving user-specified dialogue, voiceover, music, sound effects, and other hard constraints.

### Added
- **`pixverse:seedance-vibe-creating` capability** — Vibe Creating (VC) for Seedance 2.0 (`seedance-2.0-standard` / `seedance-2.0-fast` / `seedance-2.0-mini`). Routes inputs on a scene-fit (S) × expression (E) matrix into one of six actions (Pass through / Light purify / Rewrite / Ask first / Keep original / Optional VC version); runs a four-layer information-density check (visual anchor / action / local tone / video theme) before rewriting; and selects among six rewrite modes (narrative, emotional, memory, stream-of-consciousness, multi-shot experience, hybrid purification). Downweights low-value camera/technical parameters while preserving camera *intent*, keeps user-specified sound verbatim and maps it to Seedance's `()` `<>` `{}` `[]` audio markup, and emits a four-part output (Judgment / Action / Result / Notes). Registered in the master `SKILL.md` capabilities table and the `README.md` skill tree.

## [1.12.0] - 2026-06-28

Major rewrite of the `seedance-prompt-optimize` skill into a fuller multi-modal directing model — task classification, complexity-based output routing, subject tags, an audio channel, ASCII audio/text markup, and conditional constraint packs.

### Added
- **Task classification** for `seedance-prompt-optimize` — every prompt is first sorted into multi-modal reference / edit / extend / combination, each with its own recommended sentence pattern, plus a guard against writing "reference @videoN" on edit/extend tasks (which would misclassify them).
- **Path A / Path B output routing** — simple single-scene prompts now assemble into one paragraph instead of being forced into sections; only ≥ 2-shot / multi-subject / cinematic *reference* prompts use the strict three-part structure. Complexity is judged on temporal + spatial event density, not asset count.
- **Subject-tag binding** — `<subjectN>@imageN`, or "define [2–3 stable features] as `<subjectN>`" for reuse across shots, layered on top of the existing positional `@imageN` binding.
- **Audio channel** — timbre reference, single-language consistency (with non-default-language tagging), homophone pronunciation fallback, and a tail-noise fade-out suggestion.
- **ASCII audio/text markup** — `()` background music, `<>` sound effect, `{}` dialogue, `[]` subtitle/title — plus three text-generation templates (ad copy / subtitle / speech bubble).
- **Conditional constraint packs** — quality, stability, subtitle guard, watermark/logo guard, twin/clone guard (multi-person), style anchor (anime/non-photoreal), and strong-position lock (multi-person frontal dynamic).
- **Asset best-practice guidance** — split multi-view sheets into headshot + full-body, group > 4 people before image-to-video, place precision-critical assets first, and target ~4–5 assets rather than the cap.
- Two new triage red flags — absolute-second timing, and unanchored anime / non-photoreal style.

### Changed
- **Shot timing now uses `Shot 1 / Shot 2 / …` ordering; absolute seconds (`0–3s`) are forbidden.** Seedance 2.0's precise-timing support is unstable, so the shot script is ordered, not wall-clock-timed. All examples were rewritten accordingly. (Supersedes the previous time-sliced shot script.)
- **Interruption policy reversed** in `seedance-prompt-optimize`. The skill no longer blocks on every missing element; it now stops only for four critical ambiguities (position / frame mapping, task-type misjudgment, camera-move conflict, contradictory subject features) and auto-fills non-critical gaps with transparent disclosure under "Issues Found".

## [1.11.2] - 2026-06-28

Sync the skill docs to PixVerse CLI **v1.2.5** (add `seedance-2.0-mini`), and correct stale Seedance 2.0 guidance now that audio references and real human faces are accepted.

### Added
- **Seedance 2.0 Mini (`seedance-2.0-mini`)** video model — same capabilities as `seedance-2.0-fast` (`480p` / `720p`; duration `4`–`15s`; aspect ratios `16:9` `4:3` `1:1` `3:4` `9:16` `21:9`; supports the Seedance-only `--videos` / `--audios` reference inputs and up to 9 reference images), available everywhere `seedance-2.0-fast` is (`create video`, `create reference`, `create transition`). Updated the master video-model table in `SKILL.md`, the model lists and reference tables in `create-video` and `transition`, the Seedance reference-inputs note in `character-design`, and the variant enumerations in `seedance-prompt-optimize`.

### Fixed
- **Seedance 2.0 audio input is supported.** `seedance-prompt-optimize` previously claimed PixVerse's Seedance integration does **not** accept audio references — this contradicted the skill's own Step 2 mapping. Audio is now documented as a first-class reference modality (`create reference --audios`, max 3 clips, each 2–15s, total ≤ 15s; requires ≥1 image/video reference): the pipeline note and the multi-modal-reference description now read image / video / audio and point to the `@audioN` binding flow.
- **Real human faces are accepted on Seedance 2.0.** Removed the `character-design` moderation tip that warned real human faces cause frequent Seedance rejections; most face inputs now pass moderation and are no longer blocked.

## [1.11.1] - 2026-06-23

Sync the skill docs to PixVerse CLI **v1.2.3** — add 4K (`2160p`) quality for the `seedance-2.0-standard` model.

### Added
- **Seedance 2.0 Standard 4K (`2160p`) quality** — `seedance-2.0-standard` now accepts `--quality 2160p`, available everywhere the model is supported (`create video`, `create reference`, `create transition`). Updated the master video-model table in `SKILL.md` (Max Quality `1080p` → `2160p`) and the per-mode quality lists in `create-video` and `transition`.

## [1.11.0] - 2026-06-23

Sync the skill docs to PixVerse CLI **v1.2.3** — the CLI's audio overhaul (standalone voice/music, removed lip-sync), the OSS→media-path rename, and several model/flag changes. (Versions 1.10.x are reserved for the in-progress screenplay/storyboard pipeline on a separate branch, so this release jumps 1.9.0 → 1.11.0.)

### Added
- **`pixverse:create-voice` capability** — text-to-speech (TTS) with MiniMax and ElevenLabs voices. Documents `create voice`, the read-only `voice models` / `voice presets` groups, provider-specific flags (stability/similarity/style/speaker-boost for ElevenLabs; volume/pitch/emotion for MiniMax), the 5-model registry, and `--output` download.
- **`pixverse:create-music` capability** — prompt-to-music with MiniMax (`music-2.6`), ElevenLabs (`music-v1`), and Google Lyria (`lyria-3-pro-preview`). Documents `create music`, the `music models` group, lyrics/instrumental/auto-lyrics options, Lyria image references, and duration controls.
- **Seedance 2.0 extra reference inputs** — `create reference --videos` (video references) and `--audios` (audio references), seedance-2.0 only, with the count/duration limits. Documented in `create-video`, `character-design`, and `seedance-prompt-optimize`.
- **`grok-imagine-1.5`** video model (image-to-video only) added to the master and `create-video` model tables.
- **New master commands** — `voice models`, `voice presets`, `music models`, `account slots`, `update`, and the `config defaults show|set|reset` subcommands added to the All Commands table.
- **Global `--trace-id`** flag and the common `-` (stdin) / `--idempotency-key` creation conventions documented in `SKILL.md`.
- `--type audio` documented for `asset list|info|download|delete` and `task status|wait`.

### Changed
- **Default image model is now `gpt-image-2.0`** (was incorrectly documented as `qwen-image`). Updated the master Image Models table and `create-and-edit-image`.
- **PixVerse `v6` now supports Reference (fusion)** and is the default reference model (was `pixverse-c1`). Corrected the stale "V6 does not support multi-subject reference" notes in `create-video`.
- **OSS path → media path.** Removed the deprecated `--asset-image` flag everywhere; `--image` / `--images` / `--video` now accept a file path, HTTPS URL, asset ID, or media path. Updated `create-video`, `create-and-edit-image`, `motion-control`, `seedance-prompt-optimize`, `image-to-video-pipeline`, and `motion-control-pipeline`.
- `create reference` image cap is now model-aware: 7 by default, up to 9 on seedance-2.0.
- `pixverse:post-process-video` and `pixverse:video-production` reframed around extend/upscale; voiceover and music are now generated as standalone audio assets and muxed on with `ffmpeg`.

### Removed
- **`create speech` (Lip Sync)** — removed from all docs (the command was dropped in CLI v1.2.0). The `post-process-video` "add speech" section, the `SKILL.md` command-table row, the `modify-video` / `video-production` references, and the `tts-text` / `tts-speaker` flag examples are gone. Remaining mentions are explicit "removed in v1.2.0" migration notes only.
- The stale "audio references are not supported by Seedance 2.0" note (audio references are now supported — see Added).

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
