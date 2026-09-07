---
name: pixverse:canvas
description: Build and manage connected Canvas generation workflows from the CLI. Create projects, inspect graphs, query node schemas, dry-run and apply patches, dispatch generation, rebind confirmation plans, recover nodes, manage versions, rerun, and extract audio. Query live capabilities instead of assuming node types or model mappings.
---

# Canvas

Canvas is a graph of connected generation nodes. A project holds prompts, reference media, generation tasks, and composed outputs. Dependencies decide when a node can run.

The CLI reuses the existing login, `--json` / `-p` stdout contract, and standard exit codes. Canvas has no separate auth path or API base.

**Do not** hard-code Canvas node types, adapter routes, or CLI field mappings. Query them:

```bash
pixverse capabilities canvas --json
pixverse capabilities canvas --node-type <type> --json
pixverse canvas node schema --node-type <type> --json
```

See `pixverse:capabilities`. `capability_ref` does not authorize calling `create.*` instead of Canvas Graph.

Requires PixVerse CLI v1.4.0 or later and authentication.

## Terms

| Term | Meaning |
|:---|:---|
| Canvas project | One workspace of nodes and connections |
| Node | One input, generated asset, text artifact, or composition step |
| Dependency | A connection that requires one node before another can run |
| Patch | A validated set of node and dependency changes |
| Dispatch | Starting generation for specific ready nodes |
| Dispatch plan | A confirmation record authorizing one exact node batch |
| Version | One saved generation result for a node |
| `edit_version` | Optimistic lock for writes; read it from the latest graph or successful apply |

Keep `project_id`, `node_id`, `history_id`, `session_id`, `run_id`, and plan IDs as **strings**. Never coerce them to JavaScript numbers.

## Agent workflow

```text
Create project → query capabilities → graph get → patch dry-run → patch apply → dispatch exact executable nodes → graph status
```

```bash
# 1. Empty project; keep project_id
PROJECT_ID=$(pixverse canvas project create \
  --name "Campaign workspace" \
  --description "Connected image and video workflow" \
  --json | jq -r '.project_id')

# 2. Confirm the node/route/model before writing a patch
pixverse capabilities canvas \
  --node-type image_generate \
  --selector text_to_image \
  --model qwen-image \
  --json

# 3. Read the graph; keep edit_version
pixverse canvas graph get --project-id "$PROJECT_ID" --json

# 4. Validate, then apply the same patch input
pixverse canvas patch dry-run --project-id "$PROJECT_ID" --patch patch.json --json
pixverse canvas patch apply --project-id "$PROJECT_ID" --patch patch.json --json

# 5. Dispatch only diff.executable_node_ids from apply
pixverse canvas dispatch \
  --project-id "$PROJECT_ID" \
  --node-ids image_01,video_01 \
  --edit-version 13 \
  --json

# 6. Poll only the involved nodes
pixverse canvas graph status \
  --project-id "$PROJECT_ID" \
  --node-ids image_01,video_01 \
  --json
```

## canvas project create

Creates an empty project in the active workspace. Name and description are optional; the CLI does not invent field limits.

```bash
pixverse canvas project create --json
pixverse canvas project create --name "Campaign workspace" --description "Connected workflow" --json
```

Success JSON includes a non-empty `project_id` plus `trace_id`. Creation does not lock the editor or fetch the graph. There is no caller idempotency key: if the request times out, inspect existing projects before retrying to avoid duplicates.

## Graph reads

### canvas graph get

```bash
pixverse canvas graph get --project-id "$PROJECT_ID" --json
```

Returns the full snapshot. Preserve at least `project_id`, `edit_version`, `nodes`, and `edges`. Use `edit_version` on later writes.

Resolve `node_type` in this order: `node.data.extra.node_type` → `node.info.node_type` → lossy `action_type + content_type` fallback. Commands that need an exact type fail when metadata is missing. Agent-created ownership is `source === "agent"` or a non-empty `agent_patch_id` in `data.extra` or `info`. `source_type` (`asset` / `generate` / `group`) is not an ownership marker.

### canvas graph status

```bash
pixverse canvas graph status --project-id "$PROJECT_ID" --json
pixverse canvas graph status --project-id "$PROJECT_ID" --node-ids image_01,video_01 --json
```

`--node-ids` is optional and comma-separated with no duplicates. The CLI filters `Resp.nodes` client-side and still preserves `project_id`, `edit_version`, `summary`, and `invalid`.

`derived_state` values: `METADATA`, `READY`, `PENDING`, `RUNNING`, `SUCCEEDED`, `FAILED`, `BLOCKED`, `INVALID`.

Polling:

- 2 seconds for the first 30 seconds, then exponential backoff up to 10 seconds
- Terminal: `SUCCEEDED`, `FAILED`, `INVALID`
- `BLOCKED`: inspect dependencies; do not rerun the blocked node
- `FAILED` with `retryable === true`: offer `canvas node rerun`

### canvas graph invalid-nodes

```bash
pixverse canvas graph invalid-nodes --project-id "$PROJECT_ID" --json
```

Surface `invalid`, `error_code`, and `error_message`, not only node IDs.

### canvas graph reconcile

Recovery for worker restarts, missed callbacks, or state repair. **Not** a normal post-dispatch step and never a substitute for Patch → Dispatch.

```bash
pixverse canvas graph reconcile \
  --project-id "$PROJECT_ID" \
  --node-ids image_01,video_01 \
  --edit-version 13 \
  --json
```

Requires explicit `--node-ids` and current `--edit-version`. Optional `--session-id`, `--run-id`, `--dispatch-plan-id`, `--require-dispatch`. Exit policy matches dispatch after stripping the `reconciled_` prefix from `dispatch_status`.

## Node inspection and lifecycle

### canvas node get / schema

```bash
pixverse canvas node get --project-id "$PROJECT_ID" --node-id image_01 --json
pixverse canvas node schema --node-type image_generate --json
```

`node schema` is the live structure for one type. Do not snapshot it into this skill.

### canvas node versions / version / version apply

```bash
pixverse canvas node versions --project-id "$PROJECT_ID" --node-id video_01 --page 1 --page-size 20 --json
pixverse canvas node version --project-id "$PROJECT_ID" --node-id video_01 --history-id "$HISTORY_ID" --json
pixverse canvas node version apply --project-id "$PROJECT_ID" --node-id video_01 --history-id "$HISTORY_ID" --json
```

`--page` defaults to 1; `--page-size` is 1–100 (default 20). Apply accepts optional `--session-id` / `--run-id` and does **not** take `--edit-version`. `applied=false` means the version is already current — a successful no-op. A successful switch advances the graph version but does not return it; read the graph again before another write. Downstream nodes are not invalidated or redispatched automatically.

### canvas node rerun

```bash
pixverse canvas node rerun \
  --project-id "$PROJECT_ID" \
  --node-id video_01 \
  --edit-version 13 \
  --json
```

`--edit-version` is required. Optional `--session-id` / `--run-id`. Reuses the node's current parameters. Do not simulate rerun by creating a new node with the same ID. Success statuses: `rerun_dispatched`, `skipped`. `failed` is non-zero even when the envelope has `ErrCode=0`.

### canvas node extract-audio

Extracts the **complete** audio track from a trusted source video node into a Canvas audio node. The CLI may create the target if it is missing.

```bash
pixverse canvas node extract-audio \
  --project-id "$PROJECT_ID" \
  --node-id audio_extract_01 \
  --source-node-id video_01 \
  --json
```

Rules:

- `--node-id` is the empty target; `--source-node-id` is the source video
- The two IDs must differ
- Source must have `content_type=video` and a trusted `file_path` from the current graph — never pass a raw media path
- An existing target must be an agent-created `audio_reference` with `action_type=upload`, `content_type=audio`, `status=normal`, and empty `task_id` / `history_id` / `file_path`
- Poll the target with `canvas graph status`; there is no separate Canvas task-lookup command

## Patches

`--patch` is the `graph_patch` object only (literal JSON, file path, or `-` for stdin). The CLI wraps it with `idempotency_key` and optional session/run IDs.

```json
{
  "schema_version": "canvas_agent_graph.v1",
  "base_edit_version": 12,
  "nodes": [
    {
      "node_id": "script_01",
      "node_type": "script",
      "title": "Opening scene",
      "artifact": { "text": "A wide establishing shot at sunrise." }
    }
  ]
}
```

Identify the project with `--project-id`. Omitting `project_id` inside the patch is preferred; a matching value is accepted, a mismatch is rejected locally.

```bash
pixverse canvas patch dry-run --project-id "$PROJECT_ID" --patch patch.json --json
pixverse canvas patch apply --project-id "$PROJECT_ID" --patch patch.json --json
printf '%s' '{"schema_version":"canvas_agent_graph.v1","base_edit_version":12,"nodes":[]}' | \
  pixverse canvas patch dry-run --project-id "$PROJECT_ID" --patch - --json
```

| Flag | Meaning |
|:---|:---|
| `--project-id <id>` | Required |
| `--patch <input>` | Required graph_patch JSON (literal, file, or `-`) |
| `--idempotency-key <key>` | Optional; derived automatically from `project_id` + canonical `graph_patch` |
| `--session-id <id>` / `--run-id <id>` | Optional positive decimal strings |

For the same project and unchanged patch, dry-run and apply reuse the same derived key. Supply `--idempotency-key` only when the workflow must own the retry key. After the graph changes, rebuild the patch and use a **new** key. Do not replay an old patch with only `base_edit_version` replaced (backend `800044`).

### Local validation (exit 6 before HTTP)

- `schema_version` is exactly `canvas_agent_graph.v1`
- `base_edit_version` is a non-negative integer
- `nodes` and `deleted_node_ids` are not both empty
- node IDs unique; no ID in both `nodes` and `deleted_node_ids`
- `script` / `shot_plan` text lives in `artifact.text`
- image/video reference nodes provide a non-empty `file_path`
- `audio_reference` normally has `file_path`, except an empty extraction target that depends on the source video
- payload node references also appear in `depends_on`, except `video_compose`
- mapped nodes are prechecked against the live v2 adapter + current CLI Create registry

Backend still owns DAG validation, deleted-node ownership, and concurrent graph state. Unknown selector, unavailable model, missing route condition, unknown CLI parameter, or illegal value is rejected locally with exit 6. Local precheck does **not** write CLI defaults back into the user's patch.

### Updates and dependencies

Updates are not JSON Merge Patch and not full-node replacement:

- omitted `title` / `position` / `style` are preserved
- `content_type` cannot change
- `payload` and agent metadata are replaced wholesale — submit complete objects
- existing dependencies **cannot** be cleared or replaced in place; omitted and empty `depends_on` do not remove edges

To change dependencies on an agent-created node:

1. Delete it in one patch
2. Read the latest graph and `edit_version` (do not guess the version)
3. Create a replacement with a **new** project-unique `node_id` and the complete `depends_on` in a second patch
4. Retarget every downstream dependency and payload reference, then read the graph again

Never put delete + recreate in one patch. Soft-deleted IDs stay reserved (`400017 node_id conflict` if reused). Nodes not created by the agent workflow cannot use this workaround.

`video_compose` references completed source media **only** through `payload.tracks`. Omit `depends_on` entirely so the composition node stays edge-free.

### Success checks

- Dry-run succeeds only when `ErrCode === 0` and `Resp.valid === true`
- Apply succeeds only when `valid === true` and `applied === true`
- Preserve apply `Resp.diff`, especially `executable_node_ids`, `metadata_node_ids`, and the new `edit_version`

## Dispatch

Dispatch only after a successful apply, and only the intended subset of `diff.executable_node_ids`. Do not dispatch metadata nodes.

```bash
pixverse canvas dispatch \
  --project-id "$PROJECT_ID" \
  --node-ids image_01,video_01 \
  --edit-version 13 \
  --json
```

| Flag | Meaning |
|:---|:---|
| `--project-id <id>` | Required |
| `--node-ids <a,b,c>` | Required exact batch |
| `--edit-version <n>` | Required; from successful apply or latest graph |
| `--dispatch-plan-id <id>` | Required for nodes awaiting confirmation |
| `--session-id` / `--run-id` | Optional positive decimal strings |
| `--require-dispatch` | Also fail on `skipped` / `no_ready_nodes` |

`dispatch_status` values: `no_ready_nodes`, `partial`, `failed`, `queued`, `dispatched`, `skipped`.

Exit codes:

- `dispatched`, `queued`, `skipped`, `no_ready_nodes` → 0
- `partial`, `failed` → non-zero (1)
- `--require-dispatch` also makes `skipped` and `no_ready_nodes` non-zero

`partial` is not whole-request success — inspect dispatched, deferred, skipped IDs, and errors. A repeat dispatch returning `skipped` means already processed; do not recreate nodes.

For nodes whose `semantic.dispatch_state` is `awaiting_confirmation`, use the matching `semantic.dispatch_plan_id`. Never strip semantic metadata to bypass consent.

### canvas dispatch rebind

Binds existing agent-created **READY** nodes to a caller-created opaque plan ID. It does not create nodes or start generation. All-or-nothing: succeeds only when `Resp.rebound === true`. Do **not** pass `--edit-version`.

```bash
pixverse canvas dispatch rebind \
  --project-id "$PROJECT_ID" \
  --dispatch-plan-id plan-20260817-001 \
  --node-ids image_01,video_01 \
  --json

pixverse canvas dispatch \
  --project-id "$PROJECT_ID" \
  --dispatch-plan-id plan-20260817-001 \
  --node-ids image_01,video_01 \
  --edit-version "$REBIND_EDIT_VERSION" \
  --json
```

After rebind, dispatch with the response `edit_version`, the **same** `node_ids`, and the same plan ID. A plan ID authorizes one exact batch and must not be reused for a different batch.

## Common API errors

| Code | Recovery |
|:---|:---|
| `400012` | Re-authenticate |
| `400017` | Fix the rejected parameter; a reused deleted `node_id` is a conflict |
| `500329` | Check project access and the authenticated account |
| `800000` | Check `--project-id` and read the graph again |
| `800001` | Read the graph again before locating the node |
| `800002` | Refresh the node version list |
| `800044` | Read the graph, rebuild the patch, use a new idempotency key |

## Error Handling

| Exit Code | Meaning |
|:---|:---|
| 0 | Success (including dispatch `skipped` / `no_ready_nodes` without `--require-dispatch`) |
| 1 | API error, invalid/unapplied patch, or dispatch `partial`/`failed` |
| 2 | Request timed out. If `patch apply` is unknown, retry the **same** patch with the **same** idempotency key. If `project create` timed out, inspect the project list before retrying |
| 3 | Authentication expired |
| 6 | Validation error (missing IDs, bad JSON, illegal patch, unsupported model/selector) |

## Related Skills

- `pixverse:capabilities` — offline Create registry and live Canvas+CLI capability queries
- `pixverse:auth-and-account` — login and workspace
- `pixverse:create-video` / `pixverse:create-and-edit-image` — direct Create commands; Canvas generation still goes through `canvas dispatch`
