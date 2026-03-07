---
name: pixverse:task-management
description: Check generation task status and wait for completion
---

# Task Management

Check the status of generation tasks and wait for them to complete.

## Prerequisites

- PixVerse CLI installed and authenticated (`pixverse auth login`)
- A task ID (video or image) from a previous `pixverse create` command

## When to Use

```
Check on a generation?
├── Just check status? → pixverse task status <id> --json
└── Wait until done? → pixverse task wait <id> --json --timeout 300
```

Use task management when:

- You submitted a creation with `--no-wait` and need to check on it later
- You want to poll a previously submitted task
- You are running batch workflows and need to track multiple tasks

## Steps

1. Note the `video_id` or `image_id` from the creation command output.
2. Use `pixverse task status <id> --json` to check current state.
3. If not yet complete, use `pixverse task wait <id> --json` to block until done.
4. Parse the JSON output to get the final result (URL, metadata).

## Commands Reference

### task status <id>

Check the current status of a generation task without waiting.

| Flag | Description | Values |
|:---|:---|:---|
| `--type <video\|image>` | Asset type | `video` (default), `image` |
| `--json` | Output as JSON | flag |

JSON output (video):

```json
{
  "id": 123456,
  "type": "video",
  "status": "processing",
  "status_code": 10,
  "prompt": "...",
  "model": "v5.6",
  "created_at": "...",
  "video_url": null,
  "cover_url": null,
  "duration": null
}
```

JSON output (image):

```json
{
  "id": 789012,
  "type": "image",
  "status": "completed",
  "status_code": 1,
  "prompt": "...",
  "model": "qwen-image",
  "created_at": "...",
  "image_url": "https://..."
}
```

### task wait <id>

Block until a generation task completes or times out.

| Flag | Description | Values |
|:---|:---|:---|
| `--type <video\|image>` | Asset type | `video` (default), `image` |
| `--timeout <seconds>` | Max wait time | default `300` |
| `--json` | Output as JSON | flag |

JSON output (video completed):

```json
{
  "id": 123456,
  "type": "video",
  "status": "completed",
  "video_url": "https://...",
  "cover_url": "https://...",
  "prompt": "...",
  "model": "v5.6",
  "duration": 5,
  "created_at": "..."
}
```

JSON output (image completed):

```json
{
  "id": 789012,
  "type": "image",
  "status": "completed",
  "image_url": "https://...",
  "prompt": "...",
  "model": "qwen-image",
  "created_at": "..."
}
```

## Status Codes

| Code | Label | Meaning | Action |
|:---|:---|:---|:---|
| 5 | WAITING | Queued | Keep polling |
| 9 | QUEUE | In queue | Keep polling |
| 10 | PROCESSING | Generating | Keep polling |
| 1 | NORMAL | Done -- success | Use result |
| 8 | FAILED | Generation failed | Exit code 5 |
| 7 | NOT_APPROVED | Content policy violation | Exit code 5 |

## Examples

Check video status:

```bash
pixverse task status 123456 --json
```

Check image status:

```bash
pixverse task status 789012 --type image --json
```

Wait for video completion:

```bash
pixverse task wait 123456 --json
```

Wait with extended timeout:

```bash
pixverse task wait 123456 --timeout 600 --json
```

Wait for image completion:

```bash
pixverse task wait 789012 --type image --json
```

Batch workflow -- submit multiple, then wait:

```bash
VID1=$(pixverse create video --prompt "ocean waves" --no-wait --json | jq -r '.video_id')
VID2=$(pixverse create video --prompt "mountain sunset" --no-wait --json | jq -r '.video_id')
pixverse task wait $VID1 --json
pixverse task wait $VID2 --json
```

## Error Handling

| Exit Code | Meaning |
|:---|:---|
| 0 | Success -- task completed |
| 2 | Timeout -- task did not complete within the specified time. Increase `--timeout` or accept partial result |
| 3 | Authentication error (token invalid/expired) |
| 5 | Generation failed or content policy violation |

Exit code 2 (TIMEOUT) is the most common error for task management. If a task consistently times out, consider:

- Increasing the `--timeout` value
- Checking system status or trying again later
- Using `task status` to inspect the current state without blocking

## Related Skills

- `pixverse:create-video` -- create videos from text or images
- `pixverse:create-and-edit-image` -- create and edit images
- `pixverse:asset-management` -- browse, download, and delete assets
