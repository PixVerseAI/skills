---
name: pixverse:asset-management
description: Browse, inspect, download, upload, and delete generated media assets and MiniApp projects
---

# Asset Management

Browse, inspect, download, upload, and delete video, image and audio assets or MiniApp projects. Download destinations, collisions and media-input rules follow the [execution contract](../references/execution-contract.md#local-downloads); exit codes follow its [recovery table](../references/execution-contract.md#waiting-and-recovery).

For MiniApp projects, pass the `project_id` and `--type miniapps` explicitly to every asset command. Projects are created-only, so `--source upload` and `--off-peak` are invalid with them.

## Commands

| Command | Key flags | JSON |
|:---|:---|:---|
| `asset list` | `--type video\|image\|audio\|miniapps` (default `video`), `--source create\|upload` (default `create`), `--off-peak` (only with video + create), `--limit 1-100` (default 20), `--page` | `{"items", "total", "page", "limit", "has_more"}` |
| `asset info <id>` | `--type` (auto-detected if omitted; `miniapps` must be explicit), `--source create\|upload` for audio | Full asset detail. MiniApps add `id`, `project_id`, `app_id`, `status`, `status_code`, `url`, `first_frame`, `assets`, `created_at` |
| `asset download <id>` | `--type`, `--dest <dir>` (audio also accepts an exact filename) | `{"id", "type", "file"}`; MiniApps add `asset_id`, `asset_type` |
| `asset upload <input>` | local file or HTTPS URL | `{"id", "type", "name", "path", "url", "created_at"}` |
| `asset delete <id>` | `--type`, `--source create\|upload` (default `create`) | `{"id", "type", "deleted": true}`, plus `asset_id` / `source` where applicable |

`--type audio` is unavailable in `--region cn` (exit 6).

## Notes

- **Status labels:** the `status` field in `asset info` (including MiniApps) is a display label such as `Completed` or `Generating`. Branch on `status_code`.
- **Uploads:** accepted formats are jpg, png, webp, mp4 and mov, plus mp3, wav, m4a, aac and ogg in `global` (audio uploads are unavailable in `cn`). Local images larger than 1920×1920 or 5 MB are compressed before upload; the original file is not modified. Only `https://` URLs are accepted.
- **Uploaded assets are not downloadable.** `asset download` only accepts created assets. Uploaded audio is inspected with `asset info <id> --type audio --source upload`. Deleting an upload needs `--source upload` and an explicit `--type`.
- **MiniApp download:** downloads the project's primary child asset (the first video, otherwise the first image) and reports it as `asset_id` / `asset_type`.
- **Collisions:** downloads never overwrite. On exit 6, choose a fresh destination and download the same asset again; never regenerate.
- **Delete is irreversible.** Delete only what the user asked to remove.

## Examples

```bash
pixverse asset list --type image --page 2 --json
pixverse asset list --source upload --json
pixverse asset info 123456 --json
pixverse asset download 123456 --dest ./output --json
pixverse asset download 987654 --type miniapps --dest ./output --json
pixverse asset upload ./clip.mp4 --json
pixverse asset delete 555 --type image --source upload --json
```

## Related

- [saved-folders](saved-folders.md): organize assets into named folders
- [task-management](task-management.md): check status and wait for tasks
- [miniapps](miniapps.md): MiniApp projects
