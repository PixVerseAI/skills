# CLI execution contract

Read once when executing a creation chain or handling results. This describes CLI 1.4.2; use installed command help and version-specific behavior on older releases. Canvas and MiniApps keep their own result and concurrency contracts in their capabilities.

## Streams and task identity

Use `--json`: stdout contains JSON results; stderr contains errors, warnings, and diagnostics. Inspect both the exit code and any stdout result. Partial batches may return usable stdout with a nonzero exit. Error objects can contain `error`, backend `code`, and `trace_id`; preserve them for diagnosis. `cost_credits` is optional and may be absent, so absence does not mean free generation.

| Operation | Identity / result |
|:---|:---|
| Image/video creation | `image_id` / `video_id`; see shapes below |
| Voice/music | `audio_id`; see the selected audio capability for output |
| MiniApps | `project_id`; task/asset commands require `--type miniapps` |
| `task status` / `task wait` | `id` and `type`, not necessarily the creation field name |
| Uploaded input | `id` from `asset upload`; do not treat it as a pending generation |
| Canvas | Project/node identifiers and graph versions; follow the Canvas contract |

Pass `--type image` or `--type audio` to task commands for those media; video is the default. Retain workspace/region with task IDs. An ID from another account or workspace is not an interchangeable input.

## Image/video result shapes

These examples show only the fields needed to control a workflow. Extra metadata can be present.

Submitted with `--no-wait`:

```json
{"status":"submitted","video_id":111,"video_ids":[111,112],"trace_id":"..."}
```

The singular ID is the first task; the plural array is included when multiple tasks were accepted. Image requests use `image_id` / `image_ids`. Retain the entire array. Submission failures may also produce `fail_count`, including with usable IDs.

Single completion:

```json
{"status":"completed","video_id":111,"video_url":"https://...","trace_id":"..."}
```

Multiple completions:

```json
{"status":"completed","items":[{"video_id":111,"status":"completed","video_url":"https://..."},{"video_id":112,"status":"completed","video_url":"https://..."}],"trace_id":"..."}
```

Partial completion:

```json
{"status":"partial","items":[{"video_id":111,"status":"completed","video_url":"https://..."}],"failed_ids":[112],"fail_count":1,"trace_id":"..."}
```

Images substitute `image_id` / `image_url`. A batch with only one success and no reported failures can collapse to the single-object shape. `items` contains completed successes; `failed_ids` may be absent when submission failed before IDs existed. Do not assume top-level IDs exist for a completed batch. Extract completed video IDs with `jq -r '(.items // [.])[] | select(.status == "completed") | .video_id // empty'` (substitute `image_id` for images). Use `jq -er '.video_ids // [.video_id] | .[] | select(. != null)'` for submitted video IDs.

## Save once, parse once

This Bash example is for one default-wait video. It stops on failure without losing partial stdout; batch callers should process the successful `items` before deciding whether to replace failures.

```bash
if RESULT=$(pixverse create video --prompt "A sunset over mountains" --json); then
  VIDEO_ID=$(printf '%s\n' "$RESULT" | jq -er 'select(.status == "completed") | .video_id // empty') || exit 1
else
  RC=$?
  printf '%s\n' "$RESULT" >&2
  exit "$RC"
fi
pixverse asset download "$VIDEO_ID" --type video --json
```

Do not run create a second time to parse an ID. Do not pipe create straight into `jq` without preserving its failure status: empty input can make the parser exit successfully. For scripted pipelines use explicit checks (as above) or appropriate shell failure propagation, and validate required fields. Store concurrent workflow files in a unique temporary directory, not shared fixed `/tmp` names.

## Waiting and recovery

Creation waits by default. A completed response already contains the result; no second `task wait` or `asset info` is needed to retrieve the same ID/URL. For long-running or parallel jobs, submit with `--no-wait`, save all IDs immediately, and call `task wait` once per pending task. Save each wait response for later use.

`task status` exit 0 means the query succeeded, not that generation completed. Check `status` / `status_code`: 1 completed, 5/9/10 pending, 7/8 failed. Batch status queries return an ID-keyed map and can contain individual `error` objects even when the command succeeds. `task wait` waits for completion and reports generation failure separately.

| Exit | Meaning | Next action |
|:---|:---|:---|
| 0 | Command succeeded; task may only be submitted or queried | Inspect the command-specific status |
| 1 | General/API error | Inspect stderr and any available IDs before retrying |
| 2 | Polling timed out | Resume the existing task; do not assume submission failed |
| 3 | Authentication failure | Re-authenticate in the intended region |
| 4 | Insufficient credits | Inspect the intended account/workspace; stop until resolved |
| 5 | Generation failure, including partial image/video batches in CLI 1.4.0 | Preserve successful items and submitted IDs; inspect `failed_ids` / `fail_count` |
| 6 | Invalid parameters | Correct flags/inputs; it is not proof of partial success |
| 7 | Concurrency limit | Query `account slots --json`, then bounded backoff |

Older CLI output can differ; never classify a partial batch from an exit code alone. On timeout, recover a known ID with `task wait`; if no ID was captured, inspect recent assets/request diagnostics before resubmitting. Prefer `--no-wait` up front when durable task IDs are needed.

Use a stable `--idempotency-key` **from the first submission** for image/video creation commands that support it. Reuse it only for the same logical request when retrying an unconfirmed submission. An intentional replacement of a confirmed failed generation needs a new key and may cost credits. For concurrency, retry at most three times with increasing delay (for example 5/10/20 seconds), then report pending work and retained IDs. Do not switch models or workspaces just to evade a failed request.

Voice/music `--client-request-id` is tracing, not deduplication. Do not automatically resubmit those commands after an ambiguous network error. Canvas patch keys and edit versions follow [Canvas-specific recovery](../capabilities/canvas.md).

## Media inputs and reuse

Local files and external HTTPS image URLs are uploaded; URLs can be downloaded locally and re-uploaded. Reuse an existing compatible asset ID or media path to avoid that transfer. `http://` inputs are rejected. Image/video/audio acceptance and media limits depend on the command/model; query the installed capability before assembling mixed references.

Check generation status before consuming a URL. A missing or temporarily inaccessible download does not establish that generation failed: retry the download or inspect the existing asset before generating again. Download each confirmed result once and retain its local path for post-processing.
