---
name: pixverse:create-music
description: Generate music audio from a text prompt (optionally with lyrics) using MiniMax, ElevenLabs, or Google Lyria. Use when the user wants a soundtrack, background music, theme song, jingle, or instrumental. The output is a standalone audio asset — mux it onto a video with ffmpeg if needed.
---

# Create Music

Generate music from a prompt with `pixverse create music`. Every model can produce instrumental tracks or auto-generated lyrics; MiniMax and ElevenLabs can also sing supplied lyrics. The output is a **standalone audio asset**; mux it onto a video yourself. Music is **not available** in `--region cn` (exit 6 before any upload or API request).

Browse models and current credit costs first (no auth required):

```bash
pixverse music models --json
```

## create music -- Flags

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--prompt <text>` | Music prompt (required): literal, file path, or `-` for stdin | -- |
| `--lyrics <text>` | Explicit lyrics (MiniMax / ElevenLabs only): literal, file path, or `-` | rejected by Lyria |
| `-m, --model <id>` | Music model | `music-2.6` (default); see table below |
| `--instrumental` | Instrumental music (no vocals) | flag |
| `--auto-lyrics` | Let the model write lyrics | flag; all models |
| `--duration-seconds <sec>` | Target duration (sets `duration_auto=false`) | `10`–`240` |
| `--no-duration-auto` | Disable automatic duration (requires `--duration-seconds`) | flag |
| `--image <input...>` | Reference images, **Lyria only**: file paths, HTTPS URLs, image IDs, or media paths | up to 10 |
| `--output <path>` | Download the finished music to this file or directory | optional |
| `--client-request-id <id>` | Caller-side request id (tracing only, not deduplication) | optional |
| `--no-wait` / `--timeout <sec>` / `--json` | Standard flags | timeout `300` |

Vocal flag precedence, applied after model compatibility checks:

1. `--instrumental` wins: it sends `instrumental=true`, forces `auto_lyrics=false`, and omits lyrics.
2. Otherwise `--auto-lyrics` wins over `--lyrics`, which is omitted.
3. Otherwise explicit lyrics are sent. MiniMax and ElevenLabs require one of `--lyrics`, `--auto-lyrics`, or `--instrumental`.

Lyria rejects `--lyrics` even alongside the other flags; put lyric-style direction in `--prompt` or use `--auto-lyrics`.

| Model | `--model` value | Provider | Explicit lyrics | Image ref |
|:---|:---|:---|:---|:---|
| MiniMax Music 3.0 | `music-3.0` | MiniMax | Yes | No |
| MiniMax Music 2.6 *(default)* | `music-2.6` | MiniMax | Yes | No |
| ElevenLabs Music V2 | `music-v2` | ElevenLabs | Yes | No |
| ElevenLabs Music | `music-v1` | ElevenLabs | Yes | No |
| Google Lyria 3 Pro | `lyria-3-pro-preview` | Google | No | Up to 10 images |

All models support auto lyrics, instrumental output, and `10`–`240s`. The CLI imposes no local prompt or lyrics length cap; do not truncate input, and report backend validation errors.

## Results

A completed result contains `audio_id` and `audio_url`; with `--output` it also includes `local_path`. Pass `--type audio` to task and asset commands. Do not resubmit after an ambiguous failure; follow the [execution contract](../references/execution-contract.md) for waiting, recovery, and [local downloads](../references/execution-contract.md#local-downloads).

## Examples

```bash
pixverse create music --prompt "calm ambient forest score, soft strings" --instrumental --output ./score.mp3 --json
pixverse create music --prompt "an upbeat synth-pop anthem" --lyrics "[Verse]\nWalking through the neon light" --model music-2.6 --output ./song.mp3 --json
pixverse create music --model music-3.0 --prompt "modern cinematic pop with a soaring chorus" --auto-lyrics --duration-seconds 120 --json
pixverse create music --model lyria-3-pro-preview --prompt "an anthemic electronic song inspired by these scenes" --auto-lyrics --image ./scene1.jpg ./scene2.jpg --json
```

To combine music with a video, follow [video production](../workflows/video-production.md).

## Related Skills

- `pixverse:create-voice` -- generate speech/voiceover audio (TTS)
- `pixverse:asset-management` -- list, download, and delete audio assets (`--type audio`)
- `pixverse:task-management` -- poll audio tasks after `--no-wait` (`--type audio`)
