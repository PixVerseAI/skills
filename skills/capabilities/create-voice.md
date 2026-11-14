---
name: pixverse:create-voice
description: Generate speech audio from text (TTS) using MiniMax or ElevenLabs voices. Use when the user wants a voiceover, narration, spoken line, or any text-to-speech audio. The output is a standalone audio asset — mux it onto a video with ffmpeg if needed.
---

# Create Voice (Text-to-Speech)

Generate speech audio from text with `pixverse create voice`. The result is a **standalone audio asset**; to put a voiceover on a clip, mux it yourself (for example with ffmpeg). Voice is **not available** in `--region cn` (exit 6 before any upload or API request).

Browse models, languages, and preset voices first (no auth required):

```bash
pixverse voice models --json
pixverse voice presets --provider minimax --language en --json
```

## create voice -- Flags

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--text <str>` | Text to synthesize (required): literal, file path, or `-` for stdin | -- |
| `-m, --model <id>` | Voice/TTS model | `speech-2.8-hd` (default); see table below |
| `--voice-id <id>` | PixVerse preset voice ID (**recommended**) | from `pixverse voice presets` |
| `--provider-voice-id <id>` | Provider's raw voice ID (when not using a preset) | -- |
| `--language <code>` | Language code | `auto` (default) |
| `--speed <n>` | Speech speed | ElevenLabs `0.7`–`1.2`; MiniMax `0.5`–`2.0` (default `1.0`) |
| `--output <path>` | Download the finished audio to this file or directory | optional |
| `--client-request-id <id>` | Caller-side request id (tracing only, not deduplication) | optional |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | timeout `300` |

ElevenLabs-only:

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--stability <0..1>` | Voice stability | default `0.5` |
| `--similarity-boost <0..1>` | Similarity boost | default `0.75` |
| `--style <0..1>` | Style exaggeration (**`eleven-multilingual-v2` only**) | default `0` |
| `--use-speaker-boost` / `--no-use-speaker-boost` | Speaker boost (**`eleven-multilingual-v2` only**) | default on |

MiniMax-only:

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--volume <0..10>` | Output volume | default `1.0` |
| `--pitch <-12..12>` | Pitch shift | default `0` |
| `--emotion <enum>` | Emotion preset | `happy`, `sad`, `angry`, `fearful`, `disgusted`, `surprised`, `calm`, `fluent`, `whisper`; `auto` or omission sends no emotion |

Passing a flag for the other provider fails with exit 6 before submission.

| Model | `--model` value | Provider |
|:---|:---|:---|
| MiniMax Speech 2.8 HD *(default)* | `speech-2.8-hd` | MiniMax |
| MiniMax Speech 2.8 Turbo | `speech-2.8-turbo` | MiniMax |
| Eleven Multilingual v2 | `eleven-multilingual-v2` | ElevenLabs |
| Eleven v3 | `eleven-v3` | ElevenLabs |
| Eleven Turbo v2.5 | `eleven-turbo-v2.5` | ElevenLabs |

Underscore forms such as `eleven_v3` are rejected. The CLI imposes no local text length cap; do not truncate or split the user's text, and report backend validation errors.

## Results

A completed result contains `audio_id` and `audio_url`; with `--output` it also includes `local_path`. Pass `--type audio` to task and asset commands. Do not resubmit after an ambiguous failure; follow the [execution contract](../references/execution-contract.md) for waiting, recovery, and [local downloads](../references/execution-contract.md#local-downloads).

## Examples

```bash
pixverse create voice --text "Welcome to the future of creative tooling." --voice-id 12345 --output ./voiceover.mp3 --json
pixverse create voice --text "Once upon a time…" --model eleven-multilingual-v2 --voice-id 67890 --stability 0.4 --style 0.6 --json
pixverse create voice --text "We did it!" --voice-id 12345 --emotion happy --speed 1.1 --json
cat script.txt | pixverse create voice --text - --voice-id 12345 --output ./narration.mp3 --json
```

To combine voice audio with a video, follow [video production](../workflows/video-production.md).

## Related Skills

- `pixverse:create-music` -- generate a music track from a prompt
- `pixverse:asset-management` -- list, download, and delete audio assets (`--type audio`)
- `pixverse:task-management` -- poll audio tasks after `--no-wait` (`--type audio`)
- `pixverse:post-process-video` -- extend / upscale video (mux voice on externally)
