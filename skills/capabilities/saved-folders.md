---
name: pixverse:saved-folders
description: Organize generated and uploaded assets into named folders — create, browse, rename, and manage folder contents
---

# Saved Folders

Organize generated and uploaded assets into named folders. Exit codes follow the [execution contract](../references/execution-contract.md#waiting-and-recovery).

- Every account has a **default** folder, referenced as `default`. It cannot be renamed or deleted.
- Folders hold references: removing an asset from a folder or deleting a folder does not delete the asset.
- Assets are identified by **type** (`video` or `image`) and **source** (`create` or `upload`).

## Commands

| Command | Flags | JSON |
|:---|:---|:---|
| `saved list` | — | `{"folders": [{"folder_id", "folder_label", "name", "asset_count", "created_at"}], "total"}` |
| `saved items [folder_id]` | folder defaults to `default`; `--type all\|video\|image` (default `all`), `--source create\|upload` (default `create`), `--limit 1-100`, `--page` | `{"items", "total", "page", "limit", "has_more"}` |
| `saved new <name>` | — | `{"folder_id", "folder_label", "name"}` |
| `saved rename <folder_id> <name>` | — | `{..., "renamed": true}` |
| `saved add <ids...>` | `--type video\|image` (**required**), `--folder` (default `default`), `--source` (default `create`) | `{"folder_id", "folder_label", "added": [...]}` |
| `saved remove <ids...>` | same as `add` | `{"folder_id", "folder_label", "removed": [...]}` |
| `saved delete <folder_id>` | — | `{..., "deleted": true}` |

A missing `--type`, an invalid folder ID, or renaming/deleting the default folder exits 6.

## Examples

```bash
pixverse saved items 12345 --type image --source upload --json

if FOLDER_JSON=$(pixverse saved new "Project Alpha" --json); then
  FOLDER=$(printf '%s\n' "$FOLDER_JSON" | jq -er '.folder_id') || exit 1
  pixverse saved add 111 222 333 --folder "$FOLDER" --type video --json
fi
```

## Related

- [asset-management](asset-management.md): browse, download, upload and delete individual assets
