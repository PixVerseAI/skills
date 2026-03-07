---
name: pixverse:asset-management
description: Browse, inspect, download, and delete generated videos and images
---

# Asset Management

Browse, inspect, download, and delete generated videos and images from your PixVerse account.

## Prerequisites

- PixVerse CLI installed and authenticated (`pixverse auth login`)
- For download: write access to the destination directory

## When to Use

```
Manage assets?
├── Browse history? → pixverse asset list --type video --json
├── Get details? → pixverse asset info <id> --json
├── Download? → pixverse asset download <id> --json
└── Delete? → pixverse asset delete <id> --json
```

## Steps

1. Use `pixverse asset list --json` to browse your generation history.
2. Use `pixverse asset info <id> --json` to inspect a specific asset.
3. Use `pixverse asset download <id> --json` to save an asset locally.
4. Use `pixverse asset delete <id> --json` to remove an asset.

## Commands Reference

### asset list

Browse generation history with pagination.

| Flag | Description | Values |
|:---|:---|:---|
| `--type <video\|image>` | Asset type | `video` (default), `image` |
| `--limit <n>` | Items per page | default `20` |
| `--page <n>` | Page number | default `1` |
| `--json` | Output as JSON | flag |

JSON output:

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "limit": 20,
  "has_more": true
}
```

### asset info <id>

Get full details of a specific asset.

| Flag | Description | Values |
|:---|:---|:---|
| `--type <video\|image>` | Asset type (auto-detected if omitted) | `video`, `image` |
| `--json` | Output as JSON | flag |

JSON output: full VideoDetail or ImageDetail object from the API.

### asset download <id>

Download an asset to the local filesystem.

| Flag | Description | Values |
|:---|:---|:---|
| `--type <video\|image>` | Asset type (auto-detected if omitted) | `video`, `image` |
| `--dest <path>` | Destination directory | default: current directory |
| `--json` | Output as JSON | flag |

JSON output:

```json
{
  "id": 123456,
  "type": "video",
  "file": "/path/to/downloaded/file.mp4"
}
```

### asset delete <id>

Delete an asset from your account.

| Flag | Description | Values |
|:---|:---|:---|
| `--type <video\|image>` | Asset type (auto-detected if omitted) | `video`, `image` |
| `--json` | Output as JSON | flag |

JSON output:

```json
{
  "id": 123456,
  "type": "video",
  "deleted": true
}
```

## Examples

List recent videos:

```bash
pixverse asset list --json
```

List images, page 2:

```bash
pixverse asset list --type image --page 2 --json
```

List with custom page size:

```bash
pixverse asset list --type video --limit 50 --json
```

Get video details:

```bash
pixverse asset info 123456 --json
```

Get image details:

```bash
pixverse asset info 789012 --type image --json
```

Download a video to current directory:

```bash
pixverse asset download 123456 --json
```

Download to a specific directory:

```bash
pixverse asset download 123456 --dest ./output --json
```

Download an image:

```bash
pixverse asset download 789012 --type image --json
```

Delete an asset:

```bash
pixverse asset delete 123456 --json
```

Pipeline -- create, wait, download:

```bash
VID=$(pixverse create video --prompt "a sunset over the ocean" --json | jq -r '.video_id')
pixverse task wait $VID --json
pixverse asset download $VID --dest ./renders --json
```

## Error Handling

| Exit Code | Meaning |
|:---|:---|
| 0 | Success |
| 1 | Generic API error (e.g., asset not found) |
| 3 | Authentication error (token invalid/expired) |
| 6 | Validation error (invalid flags/arguments) |

## Related Skills

- `pixverse:create-video` -- create videos from text or images
- `pixverse:create-and-edit-image` -- create and edit images
- `pixverse:task-management` -- check status and wait for tasks
