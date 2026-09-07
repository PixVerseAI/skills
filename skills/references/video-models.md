# Video model fallback reference

Read only when installed capability discovery is unavailable, or when mode-specific behavior needs clarification. This static catalog describes CLI 1.4.0; older installations may support fewer models. Reference-input details are in [video reference](video-reference.md).

## Model Reference

On CLI v1.4.0 or later, query `pixverse capabilities create video [--model <id>] --json` (or `create reference` for reference mode) for installed flags and constraints. Check `pixverse --version` once per session. On older versions, use `pixverse create <mode> --help` with the table below as a fallback; do not assume newer models or flags are installed.

| Model | `--model` value | Modes | Quality | Duration | Aspect Ratio |
|:---|:---|:---|:---|:---|:---|
| PixVerse V6 | `v6` (default) | Video, Transition (first/last frame), Extend, Reference | `360p` `540p` `720p` `1080p` | `1`–`15` (any integer; Reference video uses `auto`) | `auto` `16:9` `4:3` `1:1` `3:4` `9:16` `3:2` `2:3` `21:9` (Reference supports `auto`) |
| PixVerse C1 | `pixverse-c1` | Video, Transition (first/last frame), Reference | `360p` `540p` `720p` `1080p` | `1`–`15` (any integer) | `16:9` `4:3` `1:1` `3:4` `9:16` `3:2` `2:3` |
| PixVerse v5.6 | `v5.6` | Video, Transition, Reference, Motion Control | `360p` `480p` `540p` `720p` `1080p` | `1`–`10` (any integer) | `16:9` `4:3` `1:1` `3:4` `9:16` `3:2` `2:3` |
| Sora 2 | `sora-2` | Video | `720p` | `4` `8` `12` | `16:9` `9:16` |
| Sora 2 Pro | `sora-2-pro` | Video | `720p` `1080p` | `4` `8` `12` | `16:9` `9:16` |
| Veo 3.1 Standard | `veo-3.1-standard` | Video, Transition | `720p` `1080p` `2160p` | `4` `6` `8` | `16:9` `9:16` |
| Veo 3.1 Fast | `veo-3.1-fast` | Video, Transition | `720p` `1080p` `2160p` | `4` `6` `8` | `16:9` `9:16` |
| Veo 3.1 Lite | `veo-3.1-lite` | Video, Transition | `720p` `1080p` | `4` `6` `8` | `16:9` `9:16` |
| Grok Imagine | `grok-imagine` | Video, Extend, Reference | `480p` `720p` | `1`–`15` (any integer; Reference video uses `auto`) | fixed ratios for normal/image Reference; Reference video derives framing from source |
| Grok Imagine 1.5 | `grok-imagine-1.5` | Video (I2V only) | `480p` `720p` `1080p` | `1`–`15` (any integer) | derived from input image |
| Happy Horse 1.0 | `happyhorse-1.0` | Video | `720p` `1080p` | `3`–`15` (any integer) | `16:9` `9:16` `1:1` `4:3` `3:4` |
| Seedance 2.5 | `seedance-2.5` | Video, Reference, Transition (exactly 2 frames) | `480p` `720p` `1080p` | `4`–`30` (Reference video also `auto`) | `auto` `21:9` `16:9` `4:3` `1:1` `3:4` `9:16` (T2V / Reference; transition has no selectable ratio) |
| Seedance 2.0 Standard | `seedance-2.0-standard` | Video, Reference, Transition | `480p` `720p` `1080p` `2160p` | `4`–`15` (any integer) | `16:9` `4:3` `1:1` `3:4` `9:16` `21:9` |
| Seedance 2.0 Fast | `seedance-2.0-fast` | Video, Reference, Transition | `480p` `720p` | `4`–`15` (any integer) | `16:9` `4:3` `1:1` `3:4` `9:16` `21:9` |
| Seedance 2.0 Mini | `seedance-2.0-mini` | Video, Reference, Transition | `480p` `720p` | `4`–`15` (any integer) | `16:9` `4:3` `1:1` `3:4` `9:16` `21:9` |
| MiniMax H3 | `minimax-h3` | Video, Reference, Transition (exactly 2 frames) | `768p` `1440p` (default) | `5`–`15` (any integer) | `auto` `21:9` `16:9` `4:3` `1:1` `3:4` `9:16` (mode-dependent) |
| FLUX 3 | `flux-3.0` | Video | `720p` `1080p` (default `720p`) | `5`–`20` (any integer) | `auto` `21:9` `2:1` `16:9` `4:3` `1:1` `3:4` `9:16` (T2V default `16:9`; I2V default `auto`) |
| Wan 3.0 | `wan-3.0` | Video, Reference, Transition (exactly 2 frames) | `480p` `720p` (default) `1080p` | `2`–`30` (Reference video also `auto`) | `auto` `16:9` `4:3` `1:1` `3:4` `9:16` (video/reference default `auto`; transition has no selectable ratio) |
| Kling O3 Pro | `kling-o3-pro` | Video, Reference, Transition | not applicable (omit `--quality`) | `3`–`15` (any integer) | `16:9` `9:16` `1:1` |
| Kling O3 Standard | `kling-o3-standard` | Video, Reference, Transition | not applicable (omit `--quality`) | `3`–`15` (any integer) | `16:9` `9:16` `1:1` |
| Kling O3 4K | `kling-o3-4k` | Video, Reference, Transition | not applicable (4K model tier) | `3`–`15` (any integer) | `16:9` `9:16` `1:1` |
| Kling 3.0 Pro | `kling-3.0-pro` | Video, Transition | not applicable (omit `--quality`) | `3`–`15` (any integer) | `16:9` `9:16` `1:1` |
| Kling 3.0 Standard | `kling-3.0-standard` | Video, Transition | not applicable (omit `--quality`) | `3`–`15` (any integer) | `16:9` `9:16` `1:1` |
| Kling 3.0 4K | `kling-3.0-4k` | Video, Transition | not applicable (4K model tier) | `3`–`15` (any integer) | `16:9` `9:16` `1:1` |
| Google Gemini Omni | `gemini-omni-flash` | Video, Reference | `720p` | `3`–`10` (any integer, default `5`) | `16:9` `9:16` |

> **Recommended:** PixVerse V6 (`v6`) is the default — longest duration (up to 15s), widest aspect ratio support (including `21:9`), native audio and multi-shot, and multi-subject reference (fusion). Use `v5` when you need multi-frame transitions (3+ keyframes); `v5.6` is valid for first/last-frame transition only. In `--region cn`, only `v6`, `pixverse-c1`, `seedance-2.5`, `seedance-2.0-standard`, `seedance-2.0-fast`, `seedance-2.0-mini`, `happyhorse-1.0`, and `v5.6` are available for Video (plus `v5.5` for modify and `v5` for 3+ frame transition).

### Model-specific constraints

- **V6**: Duration up to 15s; supports `21:9`; native audio and multi-shot (on by default). Supports Video, Extend, Reference, and Transition (**first/last frame only**). Reference accepts up to 10 images / 2 videos; video input locks duration to `auto`, and Reference defaults framing to `auto` while preserving an explicit valid fixed ratio. For multi-frame transitions (3+ keyframes), use `v5`.
- **C1** (`pixverse-c1`): Same duration and quality as V6 but **no `21:9` aspect ratio** and **multi-shot is forced off**. Supports Video, Transition (first/last frame), and Reference (fusion). Does not support Extend or Motion Control.
- **v5.6**: Supports Video, first/last-frame Transition, Reference (fusion), and Motion Control. It does not support Extend or 3+ frame transitions. Duration is capped at 10s; no `21:9`.
- **Sora 2**: Fixed at `720p`; only `16:9` / `9:16`.
- **Sora 2 Pro**: Adds `1080p` over Sora 2; same aspect ratio limits.
- **Veo 3.1 (Standard & Fast)**: Supports `720p` / `1080p` / `2160p`, durations `4` / `6` / `8`, and aspect ratios `16:9` / `9:16`. Available in Video and Transition modes.
- **Veo 3.1 Lite**: Cheaper Veo tier; supports `720p` / `1080p`, durations `4` / `6` / `8`, and aspect ratios `16:9` / `9:16`. Available in Video and Transition modes.
- **Grok Imagine**: Supports `480p` and `720p`; normal generation duration is any integer from `1` to `15`; widest fixed aspect-ratio selection among third-party models but no `21:9`. Reference accepts either 1–7 images or exactly 1 MP4 video (never both); video must be `1`–`8.7s`, locks duration to `auto`, rejects fixed duration, and derives framing from the source without sending aspect ratio. Also supports **Extend**.
- **Grok Imagine 1.5** (`grok-imagine-1.5`): **Image-to-video only** — `--image` is required (no text-only generation); aspect ratio is derived from the input image. Supports `480p` / `720p` / `1080p`; duration any integer `1`–`15`. Added in CLI v1.2.0.
- **Happy Horse 1.0** (`happyhorse-1.0`): External model; `720p` / `1080p`; duration starts at `3s` (minimum); aspect ratios `16:9` `9:16` `1:1` `4:3` `3:4`. Video (T2V/I2V) only — no Extend, Transition, or Reference modes.
- **Seedance 2.5** (`seedance-2.5`): External model; `480p` / `720p` / `1080p` (default `720p`); fixed durations `4`–`30s` (default `5s` without reference video). T2V and Reference support `auto` plus `21:9` `16:9` `4:3` `1:1` `3:4` `9:16` (default `16:9`); I2V retains fixed ratios. Reference accepts up to 30 images / 10 videos / 10 audios, 50 inputs total, with separate 30-second aggregate video and audio limits; audio requires a visual reference. With video, duration defaults to `auto` and locks the ratio to `auto`; choosing a fixed `4`–`30s` duration restores automatic and fixed ratio choices. `--task-type auto|reference|edit|extend` is available only for this model and defaults to `auto`. Exactly-two-frame Transition is supported with a required prompt and no selectable ratio. Generated audio, multi-shot, and off-peak are unsupported. Prompts are required in every supported mode.
- **Seedance 2.0 Standard**: External model; supports `480p` / `720p` / `1080p` / `2160p` (4K); duration starts at `4s` (minimum); supports `21:9`; available in Video, Reference, and Transition modes. No off-peak pricing.
- **Seedance 2.0 Fast**: External model; `480p` / `720p` only; duration starts at `4s` (minimum); supports `21:9`; available in Video, Reference, and Transition modes. No off-peak pricing.
- **Seedance 2.0 Mini**: External model; same capabilities as Seedance 2.0 Fast — `480p` / `720p` only; duration starts at `4s` (minimum); supports `21:9`; available in Video, Reference, and Transition modes. No off-peak pricing.
- **MiniMax H3** (`minimax-h3`): External model supporting `768p` / `1440p` (default `1440p`) and duration `5`–`15s`. T2V defaults to `16:9` and rejects `auto`; I2V always sends `auto` even if another ratio is supplied. Reference with at least one image defaults to `auto` but preserves an explicit fixed ratio; reference without images defaults to `16:9` and rejects `auto`. Reference accepts up to 9 images / 3 videos / 3 audios, and audio needs a visual reference. H3 reference validation is count-only at the model layer, unlike Seedance's clip-duration and local-audio-size checks. Prompts are required in Video, Reference, and exactly-two-frame Transition. Generated audio, multi-shot, and off-peak are unsupported.
- **FLUX 3** (`flux-3.0`): External model; Video (T2V/I2V) only — no Reference, Transition, Extend, or Motion Control. `720p` / `1080p` (default `720p`); duration `5`–`20s` (default `5`). Aspect ratios include `auto` and `2:1` in addition to `21:9` `16:9` `4:3` `1:1` `3:4` `9:16`. T2V defaults to `16:9`; I2V defaults to `auto` while preserving an explicit fixed ratio. Generated audio can be enabled or disabled; multi-shot and off-peak are unsupported. Prompts are required.
- **Wan 3.0** (`wan-3.0`): External model; `480p` / `720p` / `1080p` (default `720p`); duration `2`–`30s` (default `5` without a reference video). Video and Reference default framing to `auto` and also accept `16:9` `4:3` `1:1` `3:4` `9:16`. Reference accepts up to 10 images / 5 videos / 5 audios (20 total); audio-only is valid. Known video and audio clips are each `1`–`15s` with an exact 15-second aggregate. With a video reference, duration defaults to `auto`; a selected fixed duration is limited by `floor(30 - known reference-video duration)`. Exactly-two-frame Transition requires a prompt and does not expose an aspect-ratio flag. Generated audio is optional; multi-shot and off-peak are unsupported. Prompts are required in every supported mode.
- **Kling O3 (Pro, Standard & 4K)**: External model tiers; resolution is selected entirely by model ID, so omit `--quality` (an explicit value is ignored with a warning). Duration starts at `3s` (minimum); aspect ratios are limited to `16:9` `9:16` `1:1`. Reference accepts up to 7 images without video or up to 4 images plus 1 MP4/MOV video (`1`–`15s`, ≤`200MB`, width/height ≤`2048`). All three tiers are available in Video, Reference, and Transition modes. No off-peak pricing.
- **Kling 3.0 (Pro, Standard & 4K)**: External model tiers; resolution is selected by model ID and `quality` is omitted. Duration starts at `3s` (minimum), with the same aspect ratios as Kling O3. All three tiers are available in Video and Transition modes only (no Reference). No off-peak pricing.
- **Google Gemini Omni** (`gemini-omni-flash`): External model; `720p` only; duration `3`–`10s` (default `5`); aspect ratios `16:9` `9:16` only. Available in Video and Reference modes (no Transition or Extend). Reference accepts up to 5 images plus 1 MP4/MOV video (`1`–`10s`); video input locks duration to `auto` and rejects fixed values, while image-only Reference retains fixed duration. No off-peak pricing. Added in CLI v1.2.7.

### Seedance 2.5 text-to-video

```bash
pixverse create video --model seedance-2.5 \
  --prompt "A slow aerial orbit around an alpine lake" \
  --quality 720p --duration 12 --aspect-ratio auto --json
```

Without a reference video, Seedance 2.5 defaults to `720p`, 5 seconds, and `16:9`. Text-to-video accepts `auto` plus its six fixed aspect ratios; image-to-video retains fixed-ratio behavior. It does not support generated audio, multi-shot, or off-peak generation.

### MiniMax H3 text-to-video

```bash
pixverse create video --model minimax-h3 --prompt "A sweeping aerial shot across a crystalline desert" --quality 1440p --duration 10 --aspect-ratio 21:9 --json
```

For H3 image-to-video, pass `--image`; the CLI uses aspect ratio `auto` regardless of an explicit `--aspect-ratio` value.

### FLUX 3 text-to-video

```bash
pixverse create video --model flux-3.0 \
  --prompt "A paper lantern drifting over a moonlit canal" \
  --quality 1080p --duration 8 --aspect-ratio 21:9 --json
```

FLUX 3 is video-only (T2V and I2V). Text-to-video defaults to `16:9`; image-to-video defaults to `auto` while preserving an explicit fixed ratio. Supported qualities are `720p` / `1080p` (default `720p`); duration is any integer from `5` through `20` seconds (default `5`). Generated audio is optional; multi-shot and off-peak are unsupported.
