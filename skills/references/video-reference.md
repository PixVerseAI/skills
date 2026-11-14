# Video reference generation and editing

Read for `create reference` image/video/audio inputs. Query `pixverse capabilities create reference --model <id> --json` first; the constraints below are a fallback. Keep supplied model and media choices. Relax flags are accepted ([execution contract](execution-contract.md#relax-mode)); for `seedance-2.5-480draft`, read [Draft and Final](seedance-draft-final.md).

## create reference -- Flags

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--images <inputs...>` | Image references | file path, HTTPS URL, image ID, or media path |
| `--videos <inputs...>` | Video references (models with a video column in the matrix) | file path, HTTPS URL, video ID, or media path |
| `--audios <inputs...>` | Audio references (Seedance, MiniMax H3 / H3 Max, Wan 3.0) | file path, HTTPS URL, audio ID, or media path |
| `--prompt <text>` | Prompt text (required) | -- |
| `-m, --model <model>` | Video model | see matrix |
| `-q, --quality <q>` | Video quality | model-specific; see [video model reference](video-models.md) |
| `--aspect-ratio <ratio>` | Aspect ratio | model-specific; see framing notes below |
| `-d, --duration <seconds-or-auto>` | Duration | `auto` only with a video reference, on the models noted below |
| `--task-type <type>` | Seedance 2.5 / Draft task intent | `auto` (default), `reference`, `edit`, `extend`; rejected for other models |
| `--audio` / `--no-audio` | Enable or disable audio generation | model-dependent |
| `--count <number>` | Number of generations | `1`–`4` |
| `--seed <number>` | Random seed | any integer |
| `--off-peak` | Use off-peak pricing | flag |
| `--idempotency-key <key>` | Stable safe-retry key; see execution contract | optional |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | timeout `300` |

Assets keep flag order and are labeled per type in the prompt: `@image1`, `@video1`, `@audio1`, and so on.

## Reference media matrix

| Model | Images | Videos | Audios | Constraints and behavior |
|:---|:---|:---|:---|:---|
| V6 (`v6`) | max 10 | max 2 | no | MP4/MOV, each `1`–`15s`, ceil-each total ≤ `15s`, width/height ≤ `3840`; video locks `--duration auto` |
| PixVerse C1 / v5.6 | max 7 | no | no | image-only |
| Seedance 2.5 (and Draft) | max 30 | max 10 | max 10 | max 50 inputs; known video total ≤ `30s`, known audio total ≤ `30s`; video defaults to `--duration auto`, explicit `4`–`30s` allowed |
| Seedance 2.0 variants | max 9 | max 3 | max 3 | MP4/MOV videos each `2`–`15s`, ceil-each total ≤ `15s`, each ≤ `50MB`; audio each `2`–`15s`, total ≤ `15s`, known local file ≤ `15MB` |
| MiniMax H3 | max 9 | max 3 | max 3 | count-only model validation; other checks are shared/backend-side |
| MiniMax H3 Max | max 9 | max 3 | max 3 | max **12 total**; fixed `5`–`15s` duration even with video; count-only model validation |
| Wan 3.0 (`wan-3.0`) | max 10 | max 5 | max 5 | max 20 inputs; audio-only is valid; known videos and audios each `1`–`15s` with exact totals ≤ `15s`; video defaults to `--duration auto`, a fixed duration is capped at `floor(30 - known reference-video duration)` |
| Gemini Omni (`gemini-omni-flash`) | max 5 | max 1 | no | MP4/MOV `1`–`10s`; video locks `--duration auto` |
| Kling 4.0 | max 10 | max 5 | no | MP4/MOV each `3`–`30s`, ≤ `30s` total, ≤ `200MB` each, width/height ≤ `2048`; video does not change output duration (`3`–`30s`) |
| Kling O3 Pro / Standard / 4K | max 7 without video; max 4 with video | max 1 | no | MP4/MOV `1`–`15s`, ≤ `200MB`, width/height ≤ `2048`; omit `--quality` |
| Grok Imagine (`grok-imagine`) | `1`–`7` in image mode | exactly 1 in video mode | no | images and video are mutually exclusive; MP4 `1`–`8.7s`; video locks `--duration auto` |

At least one image or video is required, except on Wan 3.0. Audio always needs a visual reference on Seedance and both H3 models. Count and combination checks run before upload. Format, size, dimension, and duration checks run locally when metadata is known; opaque media paths defer to the backend. Where `--duration auto` is locked, a fixed duration is an error; without a video reference, `auto` is invalid.

## Framing

- V6 with image or video references: `auto` (default) or a fixed ratio.
- Seedance 2.5 with video and automatic duration: locked to `auto`. A fixed `4`–`30s` duration allows `auto` or a fixed ratio (default `16:9`).
- MiniMax H3 with an image: `auto` or a fixed ratio, default `16:9`. Without images, `auto` is rejected.
- MiniMax H3 Max: `auto` (default, ignoring a saved ratio) or a fixed ratio.
- Wan 3.0: default `auto`.
- Kling 4.0: also accepts `auto`; default `16:9`.
- Grok Imagine with video: framing comes from the source, and no ratio is sent.

## Examples

```bash
# Fusion (character reference)
pixverse create reference --images ./char1.jpg ./char2.jpg --prompt "Two characters meeting at a cafe" --json

# Seedance 2.5 mixed references
pixverse create reference --model seedance-2.5 \
  --images ./character.png --videos ./motion.mp4 --audios ./dialogue.mp3 \
  --prompt "@image1 follows @video1 and speaks with @audio1" \
  --quality 1080p --duration auto --aspect-ratio auto --task-type edit --json

# V6 video editing; duration locked to auto
pixverse create reference --model v6 --videos ./shot1.mp4 ./shot2.mov \
  --duration auto --prompt "Turn the scene into a rainy night" --json

# Kling O3 4K: with video, up to 4 images; omit --quality
pixverse create reference --model kling-o3-4k \
  --images ./character.png --videos ./motion.mov \
  --prompt "Use @image1 as the subject in @video1" --json

# MiniMax H3 Max video + audio
pixverse create reference --model minimax-h3-max \
  --videos ./motion.mp4 --audios ./dialogue.mp3 \
  --prompt "Follow @video1 with the delivery reference in @audio1" \
  --quality 768p --duration 10 --json

# Wan 3.0 audio-capable reference
pixverse create reference --model wan-3.0 \
  --videos ./motion.mp4 --audios ./voice.mp3 \
  --duration auto --prompt "Follow @video1 and @audio1" --json
```

Follow the [execution contract](execution-contract.md) for results, waiting, and partial failure. Return to [create video](../capabilities/create-video.md).
