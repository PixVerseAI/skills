---
name: pixverse:task-management
description: Check generation task or MiniApp project status and wait for completion
---

# Task Management

Check or wait for existing generation tasks (`video_id`, `image_id`, `audio_id`) and MiniApp projects (`project_id`). Use it after `--no-wait` submissions, for batches, and to resume after a polling timeout. Waiting, recovery and exit codes follow the [execution contract](../references/execution-contract.md#waiting-and-recovery). For Seedance Draft metadata and paid Final creation, read [Draft and Final](../references/seedance-draft-final.md).

## Commands

| Command | Use |
|:---|:---|
| `task status <id> [--type T] --json` | One task, single-object JSON |
| `task status <id1> <id2> ... [--type T] --json` | Batch; also `--ids id1,id2` (do not combine with positional IDs) |
| `task wait <id> [--type T] [--timeout 300] --json` | Block until completion, failure, or timeout |

`--type` is `video` (default), `image`, `audio` or `miniapps`; all IDs in one call must be the same type. `--type audio` is unavailable in `--region cn` (exit 6). Run task commands in the same region and workspace as the creation.

## task status

Exit 0 means the query succeeded, not that the task completed. Branch on `status_code`, not on `status`: `status` is a display label (`In queue`, `Generating`, `Completed`, `Failed`, `Not approved`).

```json
{"id": 123456, "type": "video", "status": "Generating", "status_code": 10, "prompt": "...", "model": "v6", "created_at": "...", "video_url": null, "cover_url": null, "duration": null}
```

Type-specific fields:

- Video: `video_url`, `cover_url`, `duration`; `seedance_draft` for Seedance Drafts.
- Image: `image_url`.
- Audio: `create_mode`, `voice_id`, `language_code`, `audio_url`, `duration`.
- MiniApps: `app_id`, `url`, `assets`.

Batch output is a map keyed by ID. Duplicate IDs are queried once, and a failed lookup appears as an entry with `error` (plus `code` / `trace_id`) without aborting the others:

```json
{"123456": {"id": 123456, "type": "video", "status": "Generating", "status_code": 10}, "123457": {"error": "Task not found", "code": 400001, "trace_id": "..."}}
```

| `status_code` | Meaning | Action |
|:---|:---|:---|
| 5, 9 | In queue | Keep waiting |
| 10 | Generating | Keep waiting |
| 1 | Completed | Use the result |
| 8 | Failed | Terminal |
| 7, 17 | Not approved (moderation) | Terminal; preserve the ID, report, do not resubmit automatically |

## task wait

On success `status` is lowercase `"completed"`, with the same type-specific result fields as above (audio returns `create_mode`, `audio_url`, `duration`, `model`, `created_at`). A failure or moderation rejection exits 5, and a timeout exits 2: resume with another `task wait` on the same ID instead of resubmitting.

When a batch `task status` query hits several typed errors, the exit code is chosen by priority: authentication (3) > insufficient credits (4) > concurrency (7) > timeout (2) > generation failure (5). Results for every ID are still printed first.

## Examples

```bash
pixverse task status 789012 --type image --json
pixverse task status 123456 123457 123458 --json
pixverse task wait 987654 --type miniapps --timeout 600 --json
```

For batch submission and result preservation, follow [batch creation](../workflows/batch-creation.md).

## Related

- [asset-management](asset-management.md): download, inspect and delete results
- [miniapps](miniapps.md): MiniApp projects
