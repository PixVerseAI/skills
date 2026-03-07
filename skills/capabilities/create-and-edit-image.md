---
name: pixverse:create-and-edit-image
description: Create images from text (T2I) or edit existing images (I2I) using AI
---

# Create and Edit Image

Generate images from text prompts (T2I) or transform existing images (I2I) using PixVerse CLI.

## Decision Tree

```
Want an image?
|-- From text only?           -> T2I: pixverse create image --prompt "..." --json
|-- Edit with single image?   -> I2I: pixverse create image --prompt "..." --image <path> --json
+-- Edit with multiple images? -> I2I: pixverse create image --prompt "..." --images <p1> <p2> --json
```

---

## Flags

| Flag | Description | Values / Default |
|:---|:---|:---|
| `--prompt <text>` | Prompt text (required) | -- |
| `--image <pathOrUrl>` | Single image input (enables I2I) | local file or URL |
| `--images <paths...>` | Multiple image inputs (enables I2I) | local files or URLs |
| `--asset-image <path>` | OSS asset path (skips upload) | -- |
| `-m, --model <model>` | Image model | `qwen-image` (default), `seedream-5.0-lite`, `seedream-4.5`, `seedream-4.0`, `nanobanana`, `nano-banana-pro`, `nano-banana-2` |
| `-q, --quality <q>` | Image quality | `720p`, `1080p` (default), `1440p`, `2160p` |
| `--aspect-ratio <ratio>` | Aspect ratio | `1:1` (default), `16:9`, `9:16`, `4:3`, `3:4`, `3:2`, `2:3`, `5:4`, `4:5`, `21:9`, `auto` |
| `--count <number>` | Number of generations | `1` (default), `2`, `3`, `4` |
| `--seed <number>` | Random seed | any integer |
| `--no-wait` | Return immediately without polling | flag |
| `--timeout <sec>` | Polling timeout | `300` (default) |
| `--json` | JSON output | flag |

### Model Reference

Each model has its own supported parameter combinations. **Always check this table before selecting flags.**

| Model | `--model` value | Resolution | Aspect Ratio |
|:---|:---|:---|:---|
| Qwen Image | `qwen-image` (default) | `720p` `1080p` | `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Seedream 5.0 Lite | `seedream-5.0-lite` | `2k` `3k` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Seedream 4.5 | `seedream-4.5` | `2k` `4k` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Seedream 4.0 | `seedream-4.0` | `1080p` `2k` `4k` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Nanobanana | `nanobanana` | `1080p` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Nano Banana Pro | `nano-banana-pro` | `1080p` `2k` `4k` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |
| Nano Banana 2 | `nano-banana-2` | `512p` `1080p` `2k` `4k` | `auto` `1:1` `16:9` `9:16` `4:3` `3:4` `5:4` `4:5` `3:2` `2:3` `21:9` |

> Models marked with "—" have not yet been documented; use default values until confirmed.

---

## JSON Output

### Submitted (--no-wait)

```json
{
  "image_id": 789012,
  "trace_id": "def-456",
  "status": "submitted"
}
```

When `--count > 1`:

```json
{
  "image_ids": [789012, 789013, 789014, 789015],
  "trace_id": "def-456",
  "status": "submitted"
}
```

### Completed

```json
{
  "image_id": 789012,
  "trace_id": "def-456",
  "status": "completed",
  "image_url": "https://...",
  "prompt": "A beautiful landscape",
  "model": "qwen-image",
  "width": 1024,
  "height": 1024,
  "created_at": "2026-01-01T00:00:00Z"
}
```

---

## Steps for T2I

1. Compose your prompt describing the desired image.
2. Choose a model from: `qwen-image`, `seedream-5.0-lite`, `seedream-4.5`, `gpt-image-1.5`.
3. Set quality (`720p`, `1080p`, `1440p`, `2160p`) and aspect ratio.
4. Optionally set: `--seed`, `--count`.
5. Run the command:
   ```bash
   pixverse create image --prompt "A serene lake at dawn" --json
   ```
6. Parse `image_id` from JSON output:
   ```bash
   pixverse create image --prompt "A serene lake at dawn" --json | jq '.image_id'
   ```
7. If `--no-wait` was used, poll later with `pixverse task wait <image_id> --type image --json`.
8. If wait completed, result includes `image_url`.

## Steps for I2I (Single Image)

1. Provide a source image with `--image <local-path-or-url>`.
2. Write a prompt describing how to transform the image.
3. Local files are auto-uploaded to OSS by the CLI.
4. URLs are passed directly to the API.
5. Alternatively, use `--asset-image <oss-path>` to skip the upload step.
6. Run the command:
   ```bash
   pixverse create image --prompt "Make it look like watercolor" --image ./photo.jpg --json
   ```

## Steps for I2I (Multiple Images)

1. Provide multiple source images with `--images <path1> <path2> ...`.
2. Write a prompt describing how to combine or transform the images.
3. Run the command:
   ```bash
   pixverse create image --prompt "Combine these into one scene" --images ./img1.jpg ./img2.jpg --json
   ```

---

## Examples

### T2I basic

```bash
pixverse create image --prompt "A serene lake at dawn with mist rising" --json
```

### T2I with full options

```bash
pixverse create image \
  --prompt "A photorealistic portrait of a medieval knight in golden armor" \
  --model seedream-5.0-lite \
  --quality 2160p \
  --aspect-ratio 16:9 \
  --json
```

### I2I with single image

```bash
pixverse create image \
  --prompt "Transform into a watercolor painting style" \
  --image ./photo.jpg \
  --json
```

### I2I with multiple images

```bash
pixverse create image \
  --prompt "Combine these characters into a single scene in a garden" \
  --images ./img1.jpg ./img2.jpg \
  --json
```

### Batch generation

```bash
pixverse create image --prompt "A cyberpunk cityscape" --count 4 --json
```

### Parse output and use in pipeline

```bash
# Generate an image, then use it for I2V
IMAGE_RESULT=$(pixverse create image --prompt "A beautiful sunset landscape" --json)
IMAGE_URL=$(echo "$IMAGE_RESULT" | jq -r '.image_url')

pixverse create video \
  --prompt "Animate this sunset with gentle clouds moving" \
  --image "$IMAGE_URL" \
  --json
```

### No-wait with later polling

```bash
RESULT=$(pixverse create image --prompt "A forest path" --no-wait --json)
IMAGE_ID=$(echo "$RESULT" | jq '.image_id')
# ... do other work ...
pixverse task wait "$IMAGE_ID" --type image --json
```

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
result=$(pixverse create image --prompt "A landscape" --json 2>/dev/null)
exit_code=$?
if [ $exit_code -eq 3 ]; then
  pixverse auth login
  result=$(pixverse create image --prompt "A landscape" --json 2>/dev/null)
elif [ $exit_code -eq 4 ]; then
  echo "Out of credits" >&2
  pixverse account info --json | jq '.credits'
  exit 1
elif [ $exit_code -ne 0 ]; then
  echo "Failed with exit code $exit_code" >&2
  exit $exit_code
fi
image_url=$(echo "$result" | jq -r '.image_url')
```

---

## Related Skills

- `pixverse:task-management` -- poll and manage tasks after using `--no-wait`
- `pixverse:asset-management` -- download, list, and delete completed images
- `pixverse:create-video` -- use generated images as input for I2V video creation
