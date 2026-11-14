# CLI execution contract

Read once when executing a creation chain or handling results. This describes CLI 1.4.20; use installed command help and version-specific behavior on older releases. Canvas, MiniApps and [schema-driven templates](../capabilities/template.md#schema-driven-templates) keep their own result contracts in their capabilities.

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

## Relax mode

`create image`, `video`, `transition`, `reference`, `modify`, and `motion-control` accept Relax flags. [Seedance Final](seedance-draft-final.md) also accepts them with separate regional behavior:

- `--relax-mode` or `--relax-mode true` sends true; `--relax-mode false` or `--no-relax-mode` sends false. The `--relax-mode=true/false` forms also work.
- Omission sends no Relax field; it is not an explicit false. Preserve the user's choice. If both positive/negative flags appear, the last wins; prefer a single unambiguous choice.
- Values are case-sensitive; invalid or empty values fail with exit 6 before media upload. Registry `supported: true` means CLI pass-through, not model support or account entitlement. The backend decides eligibility and pricing; do not promise free video or retry a rejected Relax request as paid generation automatically.
- Relax is separate from `--off-peak`; existing off-peak restrictions still apply. Other creation modes, templates and MiniApps do not accept these flags. Canvas fields still require live adapter discovery.

## Waiting and recovery

Creation waits by default. A completed response already contains the result; no second `task wait` or `asset info` is needed to retrieve the same ID/URL. For long-running or parallel jobs, submit with `--no-wait`, save all IDs immediately, and call `task wait` once per pending task. Save each wait response for later use.

The CLI uses a 60-second API request timeout, including creation submission and upload registration. This is separate from generation polling `--timeout` and storage-transfer deadlines; increasing polling timeout does not extend a submission request.

`task status` exit 0 means the query succeeded, not that generation completed. Its `status` is a display label (`In queue`, `Generating`, `Completed`, `Failed`, `Not approved`); branch on the numeric `status_code`: 1 completed, 5/9/10 pending, 8 failed, 7/17 moderation-rejected. Only creation results and `task wait` use lowercase `"completed"`. Batch status queries return an ID-keyed map and can contain individual `error` objects even when the command succeeds. `task wait` waits for completion and reports generation failure separately.

Status `7` and external moderation status `17` are terminal rejections for image/video/audio polling. `task status` still exits 0 for a successful query; waiting or creation polling exits 5 on rejection. Structured moderation errors include `error_type: "content_rejected"`, `status_code`, and `asset_id`. Preserve the ID, report the rejection, and stop polling; do not retry the same generation automatically or reinterpret it as a timeout.

| Exit | Meaning | Next action |
|:---|:---|:---|
| 0 | Command succeeded; task may only be submitted or queried | Inspect the command-specific status |
| 1 | General/API error | Inspect stderr and any available IDs before retrying |
| 2 | Polling timed out | Resume the existing task; do not assume submission failed |
| 3 | Authentication failure | Re-authenticate in the intended region |
| 4 | Insufficient credits | Inspect the intended account/workspace; stop until resolved |
| 5 | Generation failure, including partial image/video batches | Preserve successful items and submitted IDs; inspect `failed_ids` / `fail_count` |
| 6 | Invalid parameters | Correct flags/inputs; it is not proof of partial success |
| 7 | Concurrency limit | Query `account slots --json`, then bounded backoff |

Non-success HTTP responses keep the service business code and message. Inspect structured `code`, `error` and available `trace_id` instead of classifying solely by HTTP status. Authentication, credit, concurrency and workspace errors retain their typed handling; an HTTP error does not automatically mean a transient transport failure or authorize resubmission.

Never classify a partial batch from an exit code alone. On timeout, recover a known ID with `task wait`; if no ID was captured, inspect recent assets/request diagnostics before resubmitting. Prefer `--no-wait` up front when durable task IDs are needed.

Seedance Final has no idempotency key and every accepted submission creates a paid task. Never automatically resubmit; recover the returned or linked Final IDs using the [Draft/Final contract](seedance-draft-final.md).

Use a stable `--idempotency-key` **from the first submission** for image/video creation commands that support it. Reuse it only for the same logical request when retrying an unconfirmed submission. An intentional replacement of a confirmed failed generation needs a new key and may cost credits. For concurrency, retry at most three times with increasing delay (for example 5/10/20 seconds), then report pending work and retained IDs. Do not switch models or workspaces just to evade a failed request.

Voice/music `--client-request-id` is tracing, not deduplication. Do not automatically resubmit those commands after an ambiguous network error. Canvas patch keys and edit versions follow [Canvas-specific recovery](../capabilities/canvas.md).

## Media inputs and reuse

Uploads retry transient transport and TLS/connection failures automatically; let the CLI finish. Permission, signature, validation and local-file errors are not retried. Never disable certificate verification to bypass a failure. Video uploads are capped at 50 MiB (local files and URL downloads) unless a model/template sets its own limit, such as 200 MiB for Kling O3/4.0 reference videos.

Local files and external HTTPS image URLs are uploaded; URLs can be downloaded locally and re-uploaded. Reuse an existing compatible asset ID or media path to avoid that transfer. `http://` inputs are rejected. Image/video/audio acceptance and media limits depend on the command/model; query the installed capability before assembling mixed references.

Check generation status before consuming a URL. A missing or temporarily inaccessible download does not establish that generation failed: retry the download or inspect the existing asset before generating again. Download each confirmed result once and retain its local path for post-processing.

## Local downloads

`asset download --dest` selects a directory for video, image, and MiniApp assets. Audio downloads and `create voice/music --output` also accept an explicit filename: an existing directory or a missing extension-less path is treated as a directory; another path with an extension is an exact filename. `miniapps create --output` remains directory-only. Retain the returned path: asset downloads use `file`, while creation with `--output` uses `local_path`.

Downloads never overwrite or auto-rename an occupied target, including a file, directory, or symlink. Invalid filenames/IDs and collisions produce exit 6 with error JSON on stderr. Choose a fresh destination and download the existing asset again; a local output failure is not a reason to repeat paid generation. If creation failed while downloading, recover its task/asset ID from available diagnostics or asset history first.

The download layer accepts only positive safe-integer media IDs; malformed backend IDs are rejected even with an explicit audio filename. This media-ID restriction is separate from Canvas project IDs, which remain decimal strings and can exceed JavaScript's safe-integer range. Server-provided audio filenames are untrusted: unsafe names fall back to a generated filename inside the selected directory. Use the returned path instead of predicting it.

Completed files are published without replacement after transfer; failed transfers clean only their own staging files. Filesystems without hard-link support fail safely: use a compatible local destination rather than bypassing the no-overwrite behavior. Caller-selected directories may be symlinks resolved to their canonical directory; the destination is not restricted to the current working directory.
