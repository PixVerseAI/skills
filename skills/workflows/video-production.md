---
name: pixverse:video-production
description: Full video production pipeline — create, extend, add audio, upscale, and download
---

### Pipeline
1. Create base video (T2V, I2V, or Motion Control)
2. Optionally extend duration
3. Add speech (lip sync) or sound effects
4. Upscale to final resolution
5. Download

### Full Example
```bash
# Step 1: Create base video
RESULT=$(pixverse create video --prompt "A person walking through a forest" --model v6 --quality 720p --duration 5 --json)
VID=$(echo "$RESULT" | jq -r '.video_id')

# Step 2: Extend to make it longer
EXTENDED=$(pixverse create extend --video $VID --prompt "Continue walking deeper into the forest" --duration 5 --json | jq -r '.video_id')
pixverse task wait $EXTENDED --json

# Step 3: Add sound effects
WITH_SOUND=$(pixverse create sound --video $EXTENDED --prompt "Forest ambience, birds chirping, footsteps on leaves" --json | jq -r '.video_id')
pixverse task wait $WITH_SOUND --json

# Step 4: Upscale to 1080p
FINAL=$(pixverse create upscale --video $WITH_SOUND --quality 1080p --json | jq -r '.video_id')
pixverse task wait $FINAL --json

# Step 5: Download
pixverse asset download $FINAL --json
```

### Variations
- **Motion control start**: Replace Step 1 with `pixverse create motion-control --image ./char.jpg --video <ref-id> --json` to animate a character with reference motion, then continue with extend/sound/upscale
- Add speech instead of sound: `pixverse create speech --video $VID --tts-text "..." --json`
- Skip extend if original duration is sufficient
- Use `--audio <file>` for custom audio instead of TTS

### Related Skills
`pixverse:create-video`, `pixverse:motion-control`, `pixverse:post-process-video`, `pixverse:task-management`, `pixverse:asset-management`
