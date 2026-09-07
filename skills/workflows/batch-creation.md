---
name: pixverse:batch-creation
description: Submit multiple creations efficiently and recover individual failures
---

Read [execution contract](../references/execution-contract.md) for result handling, retries, and defaults.

Choose the batch form:

- Same parameters: `create video --count <n> --no-wait --json` (or the relevant image/motion-control command).
- Different prompts or seeds: separate `--no-wait` requests. Bound submissions by available concurrency from `account slots --json`; avoid a barrier waiting for unrelated work when slots remain.

Check available credits and any known per-request cost before a large batch; a positive balance alone does not prove the whole batch is affordable. All requests use the active workspace; use `--workspace-id <id>` per command to target a different one without switching.

Assign a stable idempotency key to each logical submission before its first attempt. Check each command's exit status before parsing stdout. Retain IDs immediately; never collect only the last result or mask a failed background process with a bare shell `wait`. Use a unique temporary directory if saving responses.

For submitted video batches, retain `video_ids`; single requests return `video_id`. Query multiple IDs with `pixverse task status <id1> <id2> --type video --json`, or wait once per ID and save its completed result. Image tasks require `--type image`.

For default wait-mode batches, successful completed items are under `items` (single success may use the single-object shape). Partial results use this shape:

```json
{
  "status": "partial",
  "items": [{ "video_id": 111, "status": "completed", "video_url": "https://..." }],
  "failed_ids": [112],
  "trace_id": "..."
}
```

In the current CLI, exit `5` covers both complete generation failure and partial failure; exit `6` is validation failure. Inspect the structured result to identify successful items rather than inferring partial success from the exit code alone (older CLI versions may differ). Partial results can include `fail_count` when failures have no IDs. Preserve successful items and recover only failed work; reuse the key for an unconfirmed submission retry, but use a new key for an intentional replacement of a confirmed failed generation. Exit `7` means occupied generation slots, not insufficient credits; apply the bounded retry rules in the execution contract.

Download each confirmed successful item with the correct asset type. Details: [task-management](../capabilities/task-management.md), [asset-management](../capabilities/asset-management.md).
