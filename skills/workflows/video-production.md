---
name: pixverse:video-production
description: Extend or upscale a video and optionally add voiceover or music
---

Read [execution contract](../references/execution-contract.md) for result handling, retries, and defaults.

Reuse an existing video file or completed video ID when provided; do not regenerate it. Only when the task needs a new source video, generate using [create-video](../capabilities/create-video.md), [motion-control](../capabilities/motion-control.md), or [modify-video](../capabilities/modify-video.md).

1. If requested and supported by the source/model, extend via [post-process-video](../capabilities/post-process-video.md). Validate success and replace the working video ID.
2. If requested, upscale to a supported final resolution. Validate success and replace the ID again. Default create calls already wait.
3. Reuse a supplied local video file. For a generated or remote asset ID, download once with `pixverse asset download <id> --type video --dest <directory> --json`; retain the returned `file` path.
4. Reuse supplied voiceover/music files directly. Generate new audio only when requested and no suitable supplied audio is available, using [create-voice](../capabilities/create-voice.md) or [create-music](../capabilities/create-music.md). Voice requires selecting a preset and passing `--voice-id <preset-id>` (or `--provider-voice-id`). Both audio modes are unavailable in region `cn`.

For example, after choosing a compatible voice:

```bash
pixverse create voice --text "Welcome to the forest" --voice-id "$VOICE_ID" --output "$AUDIO_FILE" --json
```

After confirming both files exist and the preceding commands succeeded, replace the original audio explicitly:

```bash
ffmpeg -n -i "$VIDEO_FILE" -i "$AUDIO_FILE" -map 0:v:0 -map 1:a:0 -c:v copy -af apad -c:a aac -shortest "$FINAL_FILE"
```

Here audio is padded with silence or trimmed to the video duration, preserving the whole video. If the user wants original audio retained under music/voice, mix the tracks with an explicit `amix` filter instead of replacing them; inspect whether the video has an audio stream first. Choose distinct input/output paths in a task-specific directory. Check ffmpeg availability before local post-processing; follow existing user authorization for dependency installation.
