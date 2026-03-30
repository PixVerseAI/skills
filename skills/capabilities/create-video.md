---
name: pixverse:create-video
description: Create AI videos from text prompts (T2V), from images (I2V), or with character references (fusion)
---

# Create Video

Generate AI videos using PixVerse CLI. Supports text-to-video (T2V), image-to-video (I2V), and character-reference fusion.

## Decision Tree

```
Want to create a video?
|-- From text only?            -> T2V:    pixverse create video --prompt "..." --json
|-- From an image?             -> I2V:    pixverse create video --prompt "..." --image <path> --json
+-- With character references? -> Fusion: pixverse create reference --images <img1> [img2...] --prompt "..." --json
```

---

## create video -- Flags

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--prompt <text>` | Prompt text (required) | -- |
| `--image <pathOrUrl>` | Image path or URL (enables I2V) | local file or URL |
| `--asset-image <path>` | OSS asset path (skips upload) | -- |
| `-m, --model <model>` | Video model | `v6` (default), `v5.6`, `v5.5`, `v5`, `v5-fast`, `sora-2`, `sora-2-pro`, `veo-3.1-standard`, `veo-3.1-fast`, `grok-imagine` |
| `-d, --duration <sec>` | Duration in seconds | `1`–`15` (any integer, default `5`; varies by model — see Model Reference) |
| `-q, --quality <q>` | Video quality | `360p`, `480p`, `540p`, `720p` (default), `1080p` (availability varies by model — see Model Reference) |
| `--aspect-ratio <ratio>` | Aspect ratio | `16:9`, `4:3`, `1:1`, `3:4`, `9:16`, `3:2`, `2:3`, `21:9` |
| `--seed <number>` | Random seed | any integer |
| `--count <number>` | Number of generations | `1` (default), `2`, `3`, `4` |
| `--audio` | Enable audio generation | flag |
| `--multi-shot` | Enable multi-shot mode | flag |
| `--off-peak` | Use off-peak pricing | flag |
| `--no-wait` | Return immediately without polling | flag |
| `--timeout <sec>` | Polling timeout | `300` (default) |
| `--json` | JSON output | flag |

---

## create reference -- Flags

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--images <paths...>` | Image paths or URLs (1–7 required) | -- |
| `--prompt <text>` | Prompt text (required) | -- |
| `-m, --model <model>` | Video model | `v5` (default), `v5.6` |
| `-q, --quality <q>` | Video quality | `360p`, `480p`, `540p`, `720p` (default), `1080p` (availability varies by model) |
| `--aspect-ratio <ratio>` | Aspect ratio | `16:9`, `4:3`, `1:1`, `3:4`, `9:16`, `3:2`, `2:3` |
| `-d, --duration <sec>` | Duration in seconds | `1`–`10` (any integer, default `5`) |

> **Note:** Reference (fusion) only supports `v5` and `v5.6`. PixVerse V6 does **not** support multi-subject reference.
| `--count <number>` | Number of generations | `1` (default), `2`, `3`, `4` |
| `--seed <number>` | Random seed | any integer |
| `--off-peak` | Use off-peak pricing | flag |
| `--no-wait` | Return immediately without polling | flag |
| `--timeout <sec>` | Polling timeout | `300` (default) |
| `--json` | JSON output | flag |

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
   pixverse create video --prompt "A sunset over mountains" --model v5.6 --quality 720p --json
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
3. URLs are passed directly to the API.
4. Alternatively, use `--asset-image <oss-path>` to skip the upload step.
5. Run the command:
   ```bash
   pixverse create video --prompt "Animate this scene" --image ./photo.jpg --json
   ```

## Steps for Fusion (Character Reference)

1. Prepare 1–7 character reference images.
2. Write a prompt describing the desired scene with those characters.
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

## Model Reference

Each model has its own supported parameter combinations. **Always check this table before selecting flags.**

| Model | `--model` value | Modes | Quality | Duration | Aspect Ratio |
|:---|:---|:---|:---|:---|:---|
| PixVerse V6 | `v6` (default) | Video, Transition (first/last frame), Extend | `360p` `540p` `720p` `1080p` | `1`–`15` (any integer) | `16:9` `4:3` `1:1` `3:4` `9:16` `3:2` `2:3` `21:9` |
| PixVerse v5.6 | `v5.6` | Video, Transition, Reference, Extend | `360p` `540p` `720p` `1080p` | `1`–`10` (any integer) | `16:9` `4:3` `1:1` `3:4` `9:16` `3:2` `2:3` |
| Sora 2 | `sora-2` | Video | `720p` | `4` `8` `12` | `16:9` `9:16` |
| Sora 2 Pro | `sora-2-pro` | Video | `720p` `1080p` | `4` `8` `12` | `16:9` `9:16` |
| Veo 3.1 Standard | `veo-3.1-standard` | Video, Transition | `720p` `1080p` | `4` `6` `8` | `16:9` `9:16` |
| Veo 3.1 Fast | `veo-3.1-fast` | Video, Transition | `720p` `1080p` | `4` `6` `8` | `16:9` `9:16` |
| Grok Imagine | `grok-imagine` | Video | `480p` `720p` | `1`–`15` (any integer) | `16:9` `4:3` `1:1` `9:16` `3:4` `3:2` `2:3` |

> **Recommended:** PixVerse V6 (`v6`) is the new default — longest duration (up to 15s), widest aspect ratio support (including `21:9`), native audio and multi-shot. Use `v5.6` when you need multi-frame transitions or multi-subject reference (fusion).

### Model-specific constraints

- **V6**: Duration up to 15s; supports `21:9`; native audio and multi-shot (on by default). Transition supports **first/last frame only** — no multi-frame transitions and no multi-subject reference. Use `v5.6` for those modes.
- **v5.6**: Full mode support including multi-frame transitions and multi-subject reference (fusion). Duration capped at 10s; no `21:9`.
- **Sora 2**: Fixed at `720p`; only `16:9` / `9:16`.
- **Sora 2 Pro**: Adds `1080p` over Sora 2; same aspect ratio limits.
- **Veo 3.1 (Standard & Fast)**: `1080p` only supports `8s` duration; `720p` supports `4` / `6` / `8`. These are the only third-party models that support `Transition` mode.
- **Grok Imagine**: Supports `480p` and `720p`; duration is any integer from `1` to `15`; widest aspect ratio selection among third-party models but no `21:9`.

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
elif [ $exit_code -ne 0 ]; then
  echo "Failed with exit code $exit_code" >&2
  exit $exit_code
fi
video_url=$(echo "$result" | jq -r '.video_url')
```

---

## Related Skills

- `pixverse:task-management` -- poll and manage tasks after using `--no-wait`
- `pixverse:asset-management` -- download, list, and delete completed videos
- `pixverse:post-process-video` -- extend, upscale, or add audio to existing videos
