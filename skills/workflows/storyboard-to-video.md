---
name: pixverse:storyboard-to-video
description: Generate a four-panel storyboard, animate each panel, and concatenate the clips
---

Read [execution contract](../references/execution-contract.md) for result handling, retries, and defaults.

This recipe uses a 2×2 grid and four clips. Adapt the shot count or layout if the user specifies a different structure.

1. Check `pixverse`, Python 3, ImageMagick (`magick`, or IM6 `convert` plus `identify`), and `ffmpeg`/`ffprobe` availability. Follow existing user authorization for missing dependency installation. Create a unique working directory; never share fixed `/tmp/shot1.png` names across runs.
2. Decompose the idea into four ordered visual shots, each with one camera angle and consistent recurring subjects/style. Present the shot plan; preserve requested dialogue separately for audio rather than silently dropping it.
3. Use [create-and-edit-image](../capabilities/create-and-edit-image.md) to generate a 2×2 grid. Prompt for four equally sized panels in reading order without gutters or text labels. Include the user's reference image with `--image` if supplied. Choose a model supported in the active region; use enough resolution for each cropped panel. Select the grid's aspect ratio to match the desired panel ratio (a 2×2 grid preserves that ratio).
4. Validate the completed image result and download its ID with `--type image` into the working directory. Inspect the layout before splitting; do not treat approximate AI layout as a guaranteed equal grid.
5. From the installed skill directory, split with the local helper (paths below are variables selected for this run):

   ```bash
   python3 scripts/storyboard-media.py split "$STORYBOARD_FILE" "$FRAMES_DIR"
   ```

   It accepts IM6 or IM7 and creates `shot1.png` through `shot4.png`, rejecting existing outputs. Inspect all four frames.
6. Generate each frame's I2V clip using [create-video](../capabilities/create-video.md), combining its shot description with the actual frame content. Use `--no-multi-shot` for supported models to preserve a continuous shot. Enable audio only as appropriate to the task. Apply [batch-creation](batch-creation.md): bounded submissions, stable per-shot keys, validate each response, retain IDs, and wait once per submitted task. Save the completed results; do not wait again merely to extract URLs. On a timeout continue tracking the same task. Retry only confirmed failed shots within the authorized scope.
7. Download each successful clip with `asset download --type video` and retain its returned `file`. Stop before composition if any required shot is missing. Concatenate in shot order:

   ```bash
   python3 scripts/storyboard-media.py concat "$FINAL_FILE" "$CLIP1" "$CLIP2" "$CLIP3" "$CLIP4" --width 1280 --height 720 --fps 30
   ```

   Choose width/height for the requested output. The helper normalizes dimensions, timestamps and frame rate; preserves existing audio, adds silence only to clips missing audio, and produces video-only output if all clips are silent. It fails rather than overwriting an existing final file. An arbitrary ffmpeg failure must not trigger a fallback that discards audio.
8. Inspect the resulting video and report its final path. Keep generated inputs available for selective recovery; cleanup only task-owned temporary files when no longer needed.

The helper performs local media operations only; generation, credentials, credits, and retry decisions remain with the agent. Details: [prompt-enhance](../capabilities/prompt-enhance.md), [asset-management](../capabilities/asset-management.md).
