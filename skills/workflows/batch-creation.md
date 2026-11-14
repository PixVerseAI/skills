---
name: pixverse:batch-creation
description: Submit multiple creations efficiently and recover individual failures
---

Choose the batch form:

- Same parameters: `create video --count <n> --no-wait --json` (or the relevant image/motion-control command); `--count` is 1–4 per request.
- Different prompts or seeds: separate `--no-wait` requests. Bound submissions by available concurrency from `account slots --json`; avoid a barrier waiting for unrelated work when slots remain.

Check available credits and any known per-request cost before a large batch; a positive balance alone does not prove the whole batch is affordable. All requests use the active workspace; use `--workspace-id <id>` per command to target a different one without switching.

For commands supporting idempotency keys, assign a stable key to each logical submission before its first attempt. Seedance Final does not support keys or automatic submission retry; follow its [dedicated contract](../references/seedance-draft-final.md). Check each command's exit status before parsing stdout. Retain IDs immediately; never collect only the last result or mask a failed background process with a bare shell `wait`. Use a unique temporary directory if saving responses.

For submitted video batches, retain `video_ids`; single requests return `video_id`. Query multiple IDs with `pixverse task status <id1> <id2> --type video --json`, or wait once per ID and save its completed result. Image tasks require `--type image`.

For default wait-mode batches, result shapes (`items`, `failed_ids`, `fail_count`) and exit codes follow the [execution contract](../references/execution-contract.md#imagevideo-result-shapes). Exit `5` covers both complete and partial failure, so inspect the structured result rather than the exit code. Preserve successful items and recover only failed work: reuse the key for an unconfirmed submission retry, use a new key for an intentional replacement of a confirmed failed generation. Exit `7` means occupied generation slots, not insufficient credits; apply the contract's bounded retry rules.

Download each confirmed successful item with the correct asset type. Details: [task-management](../capabilities/task-management.md), [asset-management](../capabilities/asset-management.md).
