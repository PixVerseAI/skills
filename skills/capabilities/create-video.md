---
name: pixverse:create-video
description: Create AI videos from text prompts (T2V), images (I2V), reference media, or source-video editing
---

# Create Video

Generate AI videos using PixVerse CLI. Supports text-to-video (T2V), image-to-video (I2V), reference-media generation, and prompt-driven source-video editing.

## Decision Tree

```
Want to create a video?
|-- From text only?            -> T2V:    pixverse create video --prompt "..." --json
|-- From an image?             -> I2V:       pixverse create video --prompt "..." --image <path> --json
|-- With image references?     -> Reference: pixverse create reference --images <img...> --prompt "..." --json
+-- Edit/source from videos?   -> Reference: pixverse create reference --videos <video...> --prompt "..." --json
```

---

## create video -- Flags

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--prompt <text>` | Prompt text (required) | -- |
| `--image <input>` | Image input (enables I2V): local file path, HTTPS URL, image ID, or media path | local files auto-upload; pass an existing asset's image ID or media path to skip upload |
| `-m, --model <model>` | Video model | `v6` (default), `pixverse-c1`, `v5.6`, `sora-2`, `sora-2-pro`, `veo-3.1-standard`, `veo-3.1-fast`, `veo-3.1-lite`, `grok-imagine`, `grok-imagine-1.5` (I2V only — requires `--image`), `seedance-2.5`, `seedance-2.0-standard`, `seedance-2.0-fast`, `seedance-2.0-mini`, `minimax-h3`, `gemini-omni-flash`, `kling-o3-pro`, `kling-o3-standard`, `kling-o3-4k`, `kling-3.0-pro`, `kling-3.0-standard`, `kling-3.0-4k`, `happyhorse-1.0` |
| `-d, --duration <sec>` | Duration in seconds | model-specific; `1`–`30` overall (default `5`; see Model Reference) |
| `-q, --quality <q>` | Video quality | model-specific; `360p`–`2160p` overall (see Model Reference) |
| `--aspect-ratio <ratio>` | Aspect ratio | model-specific; Seedance 2.5 T2V also accepts `auto`; H3 image-to-video forces `auto` (see Model Reference) |
| `--seed <number>` | Random seed | any integer |
| `--count <number>` | Number of generations | `1` (default), `2`, `3`, `4` |
| `--audio` / `--no-audio` | Enable or disable audio generation | boolean toggle (default: on for supported models) |
| `--multi-shot` / `--no-multi-shot` | Enable or disable multi-shot mode | boolean toggle (forced off for `pixverse-c1`) |
| `--off-peak` | Use off-peak pricing | flag |
| `--idempotency-key <key>` | Stable safe-retry key; repeated submissions return the original task without re-charging | optional |
| `--no-wait` | Return immediately without polling | flag |
| `--timeout <sec>` | Polling timeout | `300` (default) |
| `--json` | JSON output | flag |

---

## create reference -- Flags

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--images <inputs...>` | Image references; limits depend on model and whether video is also supplied (see matrix below) | file path, HTTPS URL, image ID, or media path |
| `--videos <inputs...>` | Video references for V6, Seedance, `minimax-h3`, Gemini Omni, Kling O3, and Grok Imagine; model-specific limits apply | file path, HTTPS URL, video ID, or media path |
| `--audios <inputs...>` | Audio references for Seedance / `minimax-h3`; requires ≥1 image/video. Seedance 2.5: max 10 and ≤30s total. Seedance 2.0: max 3, each 2–15s, ≤15s total, and known local files ≤15MB. H3 uses count-only model validation | file path, HTTPS URL, audio ID, or media path |
| `--prompt <text>` | Prompt text (required) | -- |
| `-m, --model <model>` | Video model | `v6` (default), `pixverse-c1`, `v5.6`, `seedance-2.5`, `seedance-2.0-standard`, `seedance-2.0-fast`, `seedance-2.0-mini`, `minimax-h3`, `gemini-omni-flash`, `kling-o3-pro`, `kling-o3-standard`, `kling-o3-4k`, `grok-imagine` |
| `-q, --quality <q>` | Video quality | model-specific; up to `2160p` (see Model Reference) |
| `--aspect-ratio <ratio>` | Aspect ratio | model-specific; `auto` is available or forced for selected media combinations (see matrix below) |
| `-d, --duration <seconds-or-auto>` | Duration | `auto` is locked for V6, Gemini Omni, and Grok Imagine video references; it is the default for Seedance 2.5 video references, which may instead use `4`–`30` seconds |
| `--task-type <type>` | Seedance 2.5 task intent | `auto` (default), `reference`, `edit`, or `extend`; rejected for other models |
| `--audio` / `--no-audio` | Enable or disable audio generation | model-dependent boolean toggle |
| `--count <number>` | Number of generations | `1` (default), `2`, `3`, `4` |
| `--seed <number>` | Random seed | any integer |
| `--off-peak` | Use off-peak pricing | flag |
| `--idempotency-key <key>` | Stable safe-retry key; repeated submissions return the original task without re-charging | optional |
| `--no-wait` | Return immediately without polling | flag |
| `--timeout <sec>` | Polling timeout | `300` (default) |
| `--json` | JSON output | flag |

> **Note:** Reference (fusion) supports `v6` (default), `pixverse-c1`, `v5.6`, `seedance-2.5`, `seedance-2.0-standard`, `seedance-2.0-fast`, `seedance-2.0-mini`, `minimax-h3`, `gemini-omni-flash`, `kling-o3-pro`, `kling-o3-standard`, `kling-o3-4k`, and `grok-imagine`.

### Reference media matrix

| Model | Images | Videos | Audios | Video constraints and output behavior |
|:---|:---|:---|:---|:---|
| V6 (`v6`) | max 10 | max 2 | no | MP4/MOV, each `1`–`15s`, ceil-each total ≤ `15s`, width/height ≤ `3840`; video input locks `--duration auto`; Reference framing supports fixed ratios or `auto` (default `auto`) |
| PixVerse C1 / v5.6 | max 7 | no | no | image-only Reference |
| Seedance 2.5 | max 30 | max 10 | max 10 | max 50 inputs; known video total ≤ `30s`, known audio total ≤ `30s`; video input defaults to `--duration auto`, but explicit `4`–`30s` is allowed |
| Seedance 2.0 variants | max 9 | max 3 | max 3 | MP4/MOV videos, each `2`–`15s`, ceil-each total ≤ `15s`, each ≤ `50MB`; audio each `2`–`15s`, total ≤ `15s`, known local file ≤ `15MB` |
| MiniMax H3 | max 9 | max 3 | max 3 | model-level validation is count-only; remaining media validation is shared/backend-side |
| Gemini Omni (`gemini-omni-flash`) | max 5 | max 1 | no | MP4/MOV `1`–`10s`; images and video may mix; video input locks `--duration auto` and rejects fixed values |
| Kling O3 Pro / Standard / 4K | max 7 without video; max 4 with video | max 1 | no | MP4/MOV `1`–`15s`, ≤ `200MB`, width/height ≤ `2048`; images and video may mix; omit `--quality` because the model ID selects resolution |
| Grok Imagine (`grok-imagine`) | `1`–`7` in image mode | exactly 1 in video mode | no | images and video are mutually exclusive; video must be MP4 `1`–`8.7s`, locks `--duration auto`, rejects fixed duration, and derives framing from the source video without sending aspect ratio |

At least one image or video is required; audio alone is invalid. Count/combination checks happen before upload. Format, size, dimensions, and duration are validated locally when metadata is known; opaque media paths defer unknown metadata to the backend.

Seedance 2.5 Reference with video and automatic duration locks `--aspect-ratio auto`. Selecting a fixed duration from `4` through `30` unlocks `auto` plus all six fixed ratios and defaults to `16:9`. Without video, `--duration auto` is invalid. V6, Gemini Omni, and Grok Imagine video references use automatic duration when `--duration` is omitted or explicitly set to `auto`; any fixed duration is an error. Gemini image-only references keep their normal fixed-duration path. Grok image-only references also keep fixed duration and selectable fixed ratios, while video references derive framing from the source and omit the aspect-ratio parameter.

---

## JSON Output

### With --no-wait (submitted)

```json
{
  "video_id": 123456,
  "trace_id": "abc-123",
  "status": "submitted"
}
```

When `--count > 1`, the submitted output includes a list of IDs:

```json
{
  "video_ids": [123456, 123457, 123458, 123459],
  "trace_id": "abc-123",
  "status": "submitted"
}
```

### With wait (completed)

```json
{
  "video_id": 123456,
  "trace_id": "abc-123",
  "status": "completed",
  "video_url": "https://...",
  "cover_url": "https://...",
  "prompt": "A cat astronaut floating in space",
  "model": "v5.6",
  "duration": 5,
  "width": 1280,
  "height": 720,
  "created_at": "2026-01-01T00:00:00Z"
}
```

---

## Steps for T2V

1. Compose your prompt describing the desired video.
2. Choose a model — see Model Reference table below for all available models and their constraints.
3. Set quality, aspect ratio, and duration based on the chosen model's supported values.
4. Optionally set: `--seed`, `--count`, `--audio`, `--multi-shot`, `--off-peak`.
5. Run the command:
   ```bash
   pixverse create video --prompt "A sunset over mountains" --model v6 --quality 720p --json
   ```
6. Parse `video_id` from JSON output:
   ```bash
   pixverse create video --prompt "A sunset over mountains" --json | jq '.video_id'
   ```
7. If `--no-wait` was used, poll later with `pixverse task wait <video_id> --json`.
8. If wait completed, result includes `video_url`. Download with `pixverse asset download <video_id> --json`.

## Steps for I2V

1. Same as T2V, plus provide `--image <local-path-or-url>`.
2. Local file paths are auto-uploaded to PixVerse cloud storage (OSS) by the CLI. **Do not pass files containing sensitive, private, or confidential content.**
3. URLs are passed directly to the API. Only `https://` URLs are accepted (`http://` is rejected for security).
4. Alternatively, pass an already-uploaded asset's **image ID** or **media path** directly to `--image` to skip the upload step.
5. Run the command:
   ```bash
   pixverse create video --prompt "Animate this scene" --image ./photo.jpg --json
   ```

## Steps for Reference Generation / Video Editing

1. Choose the model from the Reference media matrix, then prepare a valid image/video combination. Seedance and MiniMax H3 also accept audio references when accompanied by a visual input.
2. Write a prompt describing the output or edit. Assets keep flag order and use per-type labels such as `@image1`, `@video1`, and `@audio1`.
3. Run the command:
   ```bash
   pixverse create reference --images ./char1.jpg ./char2.jpg --prompt "Two characters meeting in a park" --json
   ```
4. Parse and wait the same as T2V.

---

## Examples

### Basic T2V

```bash
pixverse create video --prompt "A sunset over mountains" --json
```

### Full customization

```bash
pixverse create video \
  --prompt "A cinematic drone shot of a futuristic city at night" \
  --model v6 \
  --quality 1080p \
  --aspect-ratio 16:9 \
  --duration 10 \
  --audio \
  --json
```

### I2V from local file

```bash
pixverse create video --prompt "Animate this scene with gentle wind" --image ./photo.jpg --json
```

### I2V from URL

```bash
pixverse create video --prompt "Bring this painting to life" --image "https://example.com/photo.jpg" --json
```

### Seedance 2.5 text-to-video

```bash
pixverse create video --model seedance-2.5 \
  --prompt "A slow aerial orbit around an alpine lake" \
  --quality 720p --duration 12 --aspect-ratio auto --json
```

Without a reference video, Seedance 2.5 defaults to `720p`, 5 seconds, and `16:9`. Text-to-video accepts `auto` plus its six fixed aspect ratios; image-to-video retains fixed-ratio behavior. It does not support generated audio, multi-shot, or off-peak generation.

### Seedance 2.5 mixed references

```bash
pixverse create reference --model seedance-2.5 \
  --images ./character.png \
  --videos ./motion.mp4 \
  --audios ./dialogue.mp3 \
  --prompt "@image1 follows @video1 and speaks with @audio1" \
  --quality 1080p --duration auto --aspect-ratio auto --task-type edit --json
```

Reference mode allows up to 30 images, 10 videos, and 10 audios, with 50 inputs total. Known video durations may total at most 30 seconds, known audio durations may total at most 30 seconds, and audio cannot be the only reference type. With video, duration defaults to `auto` and locks aspect ratio to `auto`; explicitly select `--duration 4` through `30` to use either `auto` or a fixed ratio. Use `--task-type auto|reference|edit|extend` to state the task intent; this flag is Seedance 2.5-only and defaults to `auto`.

### Reference video editing

```bash
# V6: up to 10 images / 2 videos; video duration is locked to auto
pixverse create reference --model v6 --videos ./shot1.mp4 ./shot2.mov \
  --duration auto --prompt "Turn the scene into a rainy night" --json

# Gemini Omni: up to 5 images plus 1 video; video duration is locked to auto
pixverse create reference --model gemini-omni-flash \
  --images ./style.png --videos ./source.mp4 \
  --duration auto --prompt "Keep @video1's motion and apply @image1's style" --json

# Kling O3 4K: with video, up to 4 images; omit --quality
pixverse create reference --model kling-o3-4k \
  --images ./character.png --videos ./motion.mov \
  --prompt "Use @image1 as the subject in @video1" --json

# Grok Imagine: exactly 1 video with no images; duration is auto and framing is source-derived
pixverse create reference --model grok-imagine --videos ./source.mp4 \
  --duration auto --prompt "Replace the background with a desert" --json
```

### MiniMax H3 text-to-video

```bash
pixverse create video --model minimax-h3 --prompt "A sweeping aerial shot across a crystalline desert" --quality 1440p --duration 10 --aspect-ratio 21:9 --json
```

For H3 image-to-video, pass `--image`; the CLI uses aspect ratio `auto` regardless of an explicit `--aspect-ratio` value.

### MiniMax H3 mixed references

```bash
pixverse create reference --model minimax-h3 \
  --images ./character.png \
  --videos ./motion.mp4 \
  --audios ./dialogue.mp3 \
  --prompt "@image1 follows @video1 while speaking with the delivery in @audio1" \
  --quality 768p --duration 10 --aspect-ratio 16:9 --json
```

Because this reference request includes an image, omitting `--aspect-ratio` would default to `auto`; the explicit fixed `16:9` value is preserved. H3 reference requests without images default to `16:9` and do not accept `auto`.

### Fusion (character reference)

```bash
pixverse create reference --images ./char1.jpg ./char2.jpg --prompt "Two characters meeting at a cafe" --json
```

### No-wait + batch generation

```bash
VIDEO_IDS=$(pixverse create video --prompt "Ocean waves at sunset" --count 4 --no-wait --json | jq '.video_ids[]')
for id in $VIDEO_IDS; do
  pixverse task wait "$id" --json
done
```

---

## Input Handling

How the CLI processes `--image` / `--video` inputs before submitting to the API:

- **Local images** that exceed `1920×1920` pixels or `5 MB` are auto-resized and re-encoded (progressive JPEG/WebP, transparency preserved). Agents do **not** need to pre-compress images — pass them as-is. The original file on disk is not modified.
- **Local videos** are uploaded as-is.
- **Remote URLs** are streamed to a temp file and then uploaded. Only `https://` is accepted; `http://` URLs are rejected with a validation error (exit code 6).

---

## Model Reference

Each model has its own supported parameter combinations. **Always check this table before selecting flags.**

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
| Kling O3 Pro | `kling-o3-pro` | Video, Reference, Transition | not applicable (omit `--quality`) | `3`–`15` (any integer) | `16:9` `9:16` `1:1` |
| Kling O3 Standard | `kling-o3-standard` | Video, Reference, Transition | not applicable (omit `--quality`) | `3`–`15` (any integer) | `16:9` `9:16` `1:1` |
| Kling O3 4K | `kling-o3-4k` | Video, Reference, Transition | not applicable (4K model tier) | `3`–`15` (any integer) | `16:9` `9:16` `1:1` |
| Kling 3.0 Pro | `kling-3.0-pro` | Video, Transition | not applicable (omit `--quality`) | `3`–`15` (any integer) | `16:9` `9:16` `1:1` |
| Kling 3.0 Standard | `kling-3.0-standard` | Video, Transition | not applicable (omit `--quality`) | `3`–`15` (any integer) | `16:9` `9:16` `1:1` |
| Kling 3.0 4K | `kling-3.0-4k` | Video, Transition | not applicable (4K model tier) | `3`–`15` (any integer) | `16:9` `9:16` `1:1` |
| Google Gemini Omni | `gemini-omni-flash` | Video, Reference | `720p` | `3`–`10` (any integer, default `5`) | `16:9` `9:16` |

> **Recommended:** PixVerse V6 (`v6`) is the default — longest duration (up to 15s), widest aspect ratio support (including `21:9`), native audio and multi-shot, and multi-subject reference (fusion). Use `v5` when you need multi-frame transitions (3+ keyframes); `v5.6` is valid for first/last-frame transition only.

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
- **Kling O3 (Pro, Standard & 4K)**: External model tiers; resolution is selected entirely by model ID, so omit `--quality` (an explicit value is ignored with a warning). Duration starts at `3s` (minimum); aspect ratios are limited to `16:9` `9:16` `1:1`. Reference accepts up to 7 images without video or up to 4 images plus 1 MP4/MOV video (`1`–`15s`, ≤`200MB`, width/height ≤`2048`). All three tiers are available in Video, Reference, and Transition modes. No off-peak pricing.
- **Kling 3.0 (Pro, Standard & 4K)**: External model tiers; resolution is selected by model ID and `quality` is omitted. Duration starts at `3s` (minimum), with the same aspect ratios as Kling O3. All three tiers are available in Video and Transition modes only (no Reference). No off-peak pricing.
- **Google Gemini Omni** (`gemini-omni-flash`): External model; `720p` only; duration `3`–`10s` (default `5`); aspect ratios `16:9` `9:16` only. Available in Video and Reference modes (no Transition or Extend). Reference accepts up to 5 images plus 1 MP4/MOV video (`1`–`10s`); video input locks duration to `auto` and rejects fixed values, while image-only Reference retains fixed duration. No off-peak pricing. Added in CLI v1.2.7.

---

## Error Handling

| Exit Code | Meaning | Recovery |
|:---|:---|:---|
| 0 | Success | -- |
| 2 | Timeout waiting for completion | Increase `--timeout` or use `--no-wait` then poll with `pixverse task wait` |
| 3 | Auth token expired or invalid | Re-run `pixverse auth login` to refresh credentials |
| 4 | Insufficient credits | Check balance with `pixverse account info --json`, then top up |
| 5 | Generation failed | Check prompt for policy violations, try different parameters |
| 6 | Validation error | Review flag values against the tables above |
| 7 | Concurrent generation limit | Wait for a slot, then retry with the same `--idempotency-key` |

Example error handling in a script:

```bash
result=$(pixverse create video --prompt "A sunset" --json 2>/dev/null)
exit_code=$?
if [ $exit_code -eq 3 ]; then
  pixverse auth login
  result=$(pixverse create video --prompt "A sunset" --json 2>/dev/null)
elif [ $exit_code -eq 4 ]; then
  echo "Out of credits" >&2
  pixverse account info --json | jq '.credits'
  exit 1
elif [ $exit_code -eq 7 ]; then
  echo "Generation slots are busy; wait and safely retry" >&2
  pixverse account slots --json
  exit 7
elif [ $exit_code -ne 0 ]; then
  echo "Failed with exit code $exit_code" >&2
  exit $exit_code
fi
video_url=$(echo "$result" | jq -r '.video_url')
```

---

## Related Skills

- `pixverse:prompt-enhance` -- optimize your prompt for better V6 results (opt-in, user must request)
- `pixverse:modify-video` -- modify an existing video with a prompt at a keyframe
- `pixverse:motion-control` -- animate a character image with motion from a reference video
- `pixverse:task-management` -- poll and manage tasks after using `--no-wait`
- `pixverse:asset-management` -- download, list, and delete completed videos
- `pixverse:post-process-video` -- extend, upscale, or add audio to existing videos
