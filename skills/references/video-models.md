# Video model fallback reference

Read only when installed capability discovery is unavailable or mode-specific behavior needs clarification. Prefer `pixverse capabilities create video --model <id> --json` (or `create reference` / `create transition`) for flags, enums and defaults. This catalog describes CLI 1.4.20; reference-input limits are in [video reference](video-reference.md).

| Model | `--model` value | Modes | Quality | Duration | Aspect ratio (Video mode) |
|:---|:---|:---|:---|:---|:---|
| PixVerse V6 | `v6` (default) | Video, Reference, Extend, two-frame Transition | `360p` `540p` `720p` `1080p` | `1`–`15` | `16:9` `21:9` `4:3` `1:1` `3:4` `9:16` `3:2` `2:3` |
| PixVerse C1 | `pixverse-c1` | Video, Reference, two-frame Transition | `360p` `540p` `720p` `1080p` | `1`–`15` | V6 ratios except `21:9` |
| PixVerse v5.6 | `v5.6` | Video, Reference, two-frame Transition, Motion Control | `360p` `480p` `540p` `720p` `1080p` | `1`–`10` | `16:9` `9:16` `1:1` `4:3` `3:4` `3:2` `2:3` |
| Sora 2 / Sora 2 Pro | `sora-2`, `sora-2-pro` | Video | `720p` (Pro adds `1080p`) | `4` `8` `12` | `16:9` `9:16` |
| Veo 3.1 Standard / Fast | `veo-3.1-standard`, `veo-3.1-fast` | Video, Transition | `720p` `1080p` `2160p` | `4` `6` `8` | `16:9` `9:16` |
| Veo 3.1 Lite | `veo-3.1-lite` | Video, Transition | `720p` `1080p` | `4` `6` `8` | `16:9` `9:16` |
| Grok Imagine | `grok-imagine` | Video, Reference, Extend | `480p` `720p` | `1`–`15` | `16:9` `4:3` `1:1` `9:16` `3:4` `3:2` `2:3` |
| Grok Imagine 1.5 | `grok-imagine-1.5` | Video (I2V only) | `480p` `720p` `1080p` | `1`–`15` | derived from input image |
| Happy Horse 1.0 | `happyhorse-1.0` | Video | `720p` `1080p` | `3`–`15` | `16:9` `9:16` `1:1` `4:3` `3:4` |
| Seedance 2.5 | `seedance-2.5` | Video, Reference, two-frame Transition | `480p` `720p` (default) `1080p` | `4`–`30` | `auto` `21:9` `16:9` `4:3` `1:1` `3:4` `9:16` |
| Seedance 2.5 Draft | `seedance-2.5-480draft` (CLI 1.4.19+) | Video, Reference, two-frame Transition | `480p` | `4`–`30` | see [Draft and Final](seedance-draft-final.md) |
| Seedance 2.0 Standard | `seedance-2.0-standard` | Video, Reference, Transition | `480p` `720p` `1080p` `2160p` | `4`–`15` | `16:9` `4:3` `1:1` `3:4` `9:16` `21:9` |
| Seedance 2.0 Fast / Mini | `seedance-2.0-fast`, `seedance-2.0-mini` | Video, Reference, Transition | `480p` `720p` | `4`–`15` | `16:9` `4:3` `1:1` `3:4` `9:16` `21:9` |
| MiniMax H3 | `minimax-h3` | Video, Reference, two-frame Transition | `768p` `1440p` (default) | `5`–`15` | `21:9` `16:9` `4:3` `1:1` `3:4` `9:16` |
| MiniMax H3 Max | `minimax-h3-max` | Video, Reference, two-frame Transition | `480p` `768p` (default) `1080p` | `5`–`15` | `21:9` `16:9` `4:3` `1:1` `3:4` `9:16` |
| FLUX 3 | `flux-3.0` | Video | `720p` (default) `1080p` | `5`–`20` | `auto` `21:9` `2:1` `16:9` `4:3` `1:1` `3:4` `9:16` |
| Wan 3.0 | `wan-3.0` | Video, Reference, two-frame Transition | `480p` `720p` (default) `1080p` | `2`–`30` | `auto` (default) `16:9` `4:3` `1:1` `3:4` `9:16` |
| Kling 4.0 | `kling-4.0` | Video, Reference, two-frame Transition | `720p` `1080p` (default) | `3`–`30` | `16:9` `9:16` `1:1` `21:9` |
| Kling O3 Pro / Standard / 4K | `kling-o3-pro`, `kling-o3-standard`, `kling-o3-4k` | Video, Reference, Transition | set by model ID (omit `--quality`) | `3`–`15` | `16:9` `9:16` `1:1` |
| Kling 3.0 Pro / Standard / 4K | `kling-3.0-pro`, `kling-3.0-standard`, `kling-3.0-4k` | Video, Transition | set by model ID (omit `--quality`) | `3`–`15` | `16:9` `9:16` `1:1` |
| Google Gemini Omni | `gemini-omni-flash` | Video, Reference | `720p` | `3`–`10` | `16:9` `9:16` |

Default duration is `5` (Veo and Sora `4`). Multi-frame Transition (3+ keyframes) uses `v5`; Modify uses `v5.5`.

**Region:** `--region cn` allows only `v6`, `pixverse-c1`, `v5.6`, `v5.5`, `v5`, `seedance-2.5`, `seedance-2.5-480draft`, `seedance-2.0-standard`, `seedance-2.0-fast`, `seedance-2.0-mini`, and `happyhorse-1.0`. Every other model is global only, subject to upstream access.

## Behavior the registry does not express

- **Context-dependent framing:**
  - V6 Reference with image or video input also accepts `auto` and defaults to it; an explicit fixed ratio is kept.
  - MiniMax H3 and H3 Max image-to-video always send `auto`, ignoring `--aspect-ratio`.
  - H3 Reference with an image accepts `auto` but defaults to `16:9` (or a saved default); without images, `auto` is rejected.
  - H3 Max Reference defaults to `auto` and ignores a saved ratio.
  - Seedance 2.5 accepts `auto` in T2V and Reference, but image-to-video uses fixed ratios.
  - FLUX 3 image-to-video defaults to `auto`.
  - Kling 4.0 Reference also accepts `auto` but defaults to `16:9`; Kling 4.0 I2V and Transition derive framing from images.
  - Grok Imagine Reference with a video derives framing from the source.
- **Video-reference duration:** a reference video sets duration to `auto` for V6, Grok Imagine, Gemini Omni, Seedance 2.5, and Wan 3.0. For Seedance 2.5, choosing a fixed `4`–`30` duration restores the fixed ratio choices. For Wan 3.0, a fixed duration is capped at `floor(30 - reference video duration)`.
- **Prompt required:** Seedance 2.5 (and Draft), MiniMax H3 / H3 Max, FLUX 3, and Wan 3.0 require a prompt in every supported mode.
- **Unsupported CLI controls:**
  - Seedance 2.5, H3, H3 Max, and Kling 4.0 expose no audio, multi-shot, or off-peak control.
  - FLUX 3 and Wan 3.0 allow audio but not multi-shot or off-peak.
  - Seedance 2.0, Kling, and Gemini Omni have no off-peak.
  - C1 forces multi-shot off.
- **Quality selection:** Kling O3/3.0 select resolution by model ID, and an explicit `--quality` is ignored with a warning. Kling 4.0 sends quality, uses `1080p` ahead of a saved generic quality, and honors an explicit `720p`.
- **Seedance 2.5 task type:** `--task-type auto|reference|edit|extend` (default `auto`) applies to Seedance 2.5 and its Draft.
- **Grok Imagine 1.5** requires `--image`; there is no text-only generation.

## Examples

```bash
pixverse create video --model seedance-2.5 --prompt "A slow aerial orbit around an alpine lake" --quality 720p --duration 12 --aspect-ratio auto --json
pixverse create video --model minimax-h3-max --prompt "A sweeping aerial shot across a crystalline desert" --quality 768p --duration 10 --aspect-ratio 21:9 --json
pixverse create video --model flux-3.0 --prompt "A paper lantern drifting over a moonlit canal" --quality 1080p --duration 8 --aspect-ratio 21:9 --json
```
