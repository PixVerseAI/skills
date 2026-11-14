---
name: pixverse:miniapps
description: Discover PixVerse MiniApps, inspect their live parameter schemas, create projects, and manage the generated project assets
---

# PixVerse MiniApps

PixVerse MiniApps are preset, single-purpose generators. The CLI discovers available apps and their parameter schemas from the backend; there is no bundled catalog. Always call `miniapps info <id> --json` before constructing `--params`, because apps and schemas change independently of the CLI. Exit codes follow the [execution contract](../references/execution-contract.md#waiting-and-recovery).

## Discover

`pixverse miniapps list --json` returns `{"items": [{"app_id", "name", "description", "can_create"}]}`. Apps the user cannot create are omitted.

`pixverse miniapps info <id> --json` preserves the backend payload and adds a flat `params_schema`:

| Field | Meaning |
|:---|:---|
| `name` | Key to place in the `--params` JSON object |
| `component` | Renderer component, when different from `name` |
| `required` | Whether the field must be supplied |
| `type` | `enum`, `upload`, `text`, or `unknown` |
| `options` | Allowed values for an enum |
| `max_count` / `max_video_size_mb` / `max_length` | Declared limits |
| `note` | Explanation when the type cannot be inferred |

The normalizer reports fields it cannot infer as `unknown`; it does not invent types, defaults, or enum values. Ask the user rather than guessing an `unknown` field.

## Create a project

| Flag | Notes |
|:---|:---|
| `--id <app_id>` | Required |
| `--params <input>` | Required JSON object: literal JSON, a file path, or `-` for stdin. The CLI checks JSON syntax; the backend validates fields |
| `--output <dir>` | Download the completed project's primary asset (the first video, otherwise the first image); directory only, never overwrites |
| `--no-wait` / `--timeout 300` | Submit only / polling limit |

Upload fields need PixVerse media paths, not local paths or URLs. Upload first and use the returned `path`:

```bash
if UPLOAD=$(pixverse asset upload ./source.png --json); then
  MEDIA_PATH=$(printf '%s\n' "$UPLOAD" | jq -er '.path') || exit 1
else
  exit $?
fi

PARAMS=$(jq -nc --arg image "$MEDIA_PATH" '{image: $image, ratio: "16:9"}')
if RESULT=$(pixverse miniapps create --id magic_extend --params "$PARAMS" --no-wait --json); then
  PROJECT_ID=$(printf '%s\n' "$RESULT" | jq -er '.project_id') || exit 1
else
  RC=$?; printf '%s\n' "$RESULT" >&2; exit "$RC"
fi
pixverse task wait "$PROJECT_ID" --type miniapps --json
pixverse asset download "$PROJECT_ID" --type miniapps --dest ./output --json
```

Submitted (`--no-wait`): `{"id", "project_id", "app_id", "trace_id", "status": "submitted"}`.

Completed (waiting): `{"id", "project_id", "app_id", "status": "Completed", "status_code": 1, "url", "first_frame", "assets": [{"type", "id", "url"}], "created_at"}`, plus `trace_id` when available and `local_path` with `--output`. Here `status` is a display label; branch on `status_code`.

A download collision requires a fresh destination for the existing project's asset, not a new project submission.

## Manage a project

MiniApp projects use `project_id` and always need an explicit `--type miniapps` (they are excluded from type auto-detection):

```bash
pixverse task status 987654 --type miniapps --json
pixverse asset info 987654 --type miniapps --json
pixverse asset delete 987654 --type miniapps --json
```

See [task-management](task-management.md) and [asset-management](asset-management.md) for those commands.
