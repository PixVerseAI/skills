# Video reference generation and editing

Read for `create reference` image/video/audio inputs. On CLI 1.4.0+, query `pixverse capabilities create reference --model <id> --json`; older versions require `pixverse create reference --help` and the static constraints below. Keep supplied model and media choices.

## create reference -- Flags

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--images <inputs...>` | Image references; limits depend on model and whether video is also supplied (see matrix below) | file path, HTTPS URL, image ID, or media path |
| `--videos <inputs...>` | Video references for V6, Seedance, `minimax-h3`, `wan-3.0`, Gemini Omni, Kling O3, and Grok Imagine; model-specific limits apply | file path, HTTPS URL, video ID, or media path |
| `--audios <inputs...>` | Audio references for Seedance / `minimax-h3` / `wan-3.0`. Seedance and H3 require ≥1 image/video; Wan 3.0 also accepts audio-only. Seedance 2.5: max 10 and ≤30s total. Seedance 2.0: max 3, each 2–15s, ≤15s total, and known local files ≤15MB. Wan 3.0: max 5, each 1–15s, exact total ≤15s. H3 uses count-only model validation | file path, HTTPS URL, audio ID, or media path |
| `--prompt <text>` | Prompt text (required) | -- |
| `-m, --model <model>` | Video model | See the Reference media matrix below |
| `-q, --quality <q>` | Video quality | model-specific; up to `2160p` (see [video model reference](video-models.md)) |
| `--aspect-ratio <ratio>` | Aspect ratio | model-specific; `auto` is available or forced for selected media combinations (see matrix below) |
| `-d, --duration <seconds-or-auto>` | Duration | `auto` is locked for V6, Gemini Omni, and Grok Imagine video references; it is the default for Seedance 2.5 and Wan 3.0 video references, which may instead use a fixed duration |
| `--task-type <type>` | Seedance 2.5 task intent | `auto` (default), `reference`, `edit`, or `extend`; rejected for other models |
| `--audio` / `--no-audio` | Enable or disable audio generation | model-dependent boolean toggle |
| `--count <number>` | Number of generations | `1` (default), `2`, `3`, `4` |
| `--seed <number>` | Random seed | any integer |
| `--off-peak` | Use off-peak pricing | flag |
| `--idempotency-key <key>` | Stable safe-retry key; see execution contract | optional |
| `--no-wait` | Return immediately without polling | flag |
| `--timeout <sec>` | Polling timeout | `300` (default) |
| `--json` | JSON output | flag |

### Reference media matrix

| Model | Images | Videos | Audios | Video constraints and output behavior |
|:---|:---|:---|:---|:---|
| V6 (`v6`) | max 10 | max 2 | no | MP4/MOV, each `1`–`15s`, ceil-each total ≤ `15s`, width/height ≤ `3840`; video input locks `--duration auto`; Reference framing supports fixed ratios or `auto` (default `auto`) |
| PixVerse C1 / v5.6 | max 7 | no | no | image-only Reference |
| Seedance 2.5 | max 30 | max 10 | max 10 | max 50 inputs; known video total ≤ `30s`, known audio total ≤ `30s`; video input defaults to `--duration auto`, but explicit `4`–`30s` is allowed |
| Seedance 2.0 variants | max 9 | max 3 | max 3 | MP4/MOV videos, each `2`–`15s`, ceil-each total ≤ `15s`, each ≤ `50MB`; audio each `2`–`15s`, total ≤ `15s`, known local file ≤ `15MB` |
| MiniMax H3 | max 9 | max 3 | max 3 | model-level validation is count-only; remaining media validation is shared/backend-side |
| Wan 3.0 (`wan-3.0`) | max 10 | max 5 | max 5 | max 20 inputs; audio-only is valid; known video each `1`–`15s` and exact total ≤ `15s`; known audio each `1`–`15s` and exact total ≤ `15s`; video input defaults to `--duration auto`, while a fixed duration is capped at `floor(30 - known reference-video duration)` |
| Gemini Omni (`gemini-omni-flash`) | max 5 | max 1 | no | MP4/MOV `1`–`10s`; images and video may mix; video input locks `--duration auto` and rejects fixed values |
| Kling O3 Pro / Standard / 4K | max 7 without video; max 4 with video | max 1 | no | MP4/MOV `1`–`15s`, ≤ `200MB`, width/height ≤ `2048`; images and video may mix; omit `--quality` because the model ID selects resolution |
| Grok Imagine (`grok-imagine`) | `1`–`7` in image mode | exactly 1 in video mode | no | images and video are mutually exclusive; video must be MP4 `1`–`8.7s`, locks `--duration auto`, rejects fixed duration, and derives framing from the source video without sending aspect ratio |

At least one image or video is required except on Wan 3.0, which also accepts audio-only references. Count/combination checks happen before upload. Format, size, dimensions, and duration are validated locally when metadata is known; opaque media paths defer unknown metadata to the backend. Wan 3.0 enforces known duration totals locally and leaves remaining media constraints to the backend.

Seedance 2.5 Reference with video and automatic duration locks `--aspect-ratio auto`. Selecting a fixed duration from `4` through `30` unlocks `auto` plus all six fixed ratios and defaults to `16:9`. Without video, `--duration auto` is invalid. Wan 3.0 video and reference default framing to `auto`; with a video reference, duration also defaults to `auto`, while a selected fixed duration remains available up to `floor(30 - known reference-video duration)`. V6, Gemini Omni, and Grok Imagine video references use automatic duration when `--duration` is omitted or explicitly set to `auto`; any fixed duration is an error. Gemini image-only references keep their normal fixed-duration path. Grok image-only references also keep fixed duration and selectable fixed ratios, while video references derive framing from the source and omit the aspect-ratio parameter.

## Steps for Reference Generation / Video Editing

1. Choose the model from the Reference media matrix, then prepare a valid image/video combination. Seedance and MiniMax H3 also accept audio references when accompanied by a visual input. Wan 3.0 accepts mixed image/video/audio references and also allows audio-only input.
2. Write a prompt describing the output or edit. Assets keep flag order and use per-type labels such as `@image1`, `@video1`, and `@audio1`.
3. Run the command:
   ```bash
   pixverse create reference --images ./char1.jpg ./char2.jpg --prompt "Two characters meeting in a park" --json
   ```
4. Preserve the creation result and exit code; follow the [execution contract](execution-contract.md) for single/batch results, waiting, and partial failure.

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

### Wan 3.0 mixed references

```bash
pixverse create reference --model wan-3.0 \
  --videos ./motion.mp4 --audios ./voice.mp3 \
  --duration auto --prompt "Follow @video1 and @audio1" --json
```

Wan 3.0 defaults to `720p`, 5 seconds, and `auto`. Reference accepts up to 10 images / 5 videos / 5 audios (20 total), including audio-only input. Known video and audio durations are each `1`–`15s` with an exact 15-second aggregate. With a video reference, duration defaults to `auto`; a fixed duration is limited by `floor(30 - known reference-video duration)`. Generated audio is optional; multi-shot and off-peak are unsupported.

### Fusion (character reference)

```bash
pixverse create reference --images ./char1.jpg ./char2.jpg --prompt "Two characters meeting at a cafe" --json
```

Return to [create video](../capabilities/create-video.md).
