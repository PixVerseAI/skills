---
name: pixverse:workspace
description: Manage workspaces — list, switch, check status, and open management page. Covers personal vs team context, roles, credits, and the global --workspace-id override.
---

# Workspace Management

Covers: `workspace list`, `workspace status`, `workspace switch`, `workspace manage`, and the global `--workspace-id` override.

Delegated (paired) sessions on CLI 1.4.19+ select Team workspaces account-wide, with different JSON and failure behavior. Use [delegated workspace selection](../references/auth-pairing.md#delegated-workspace-selection-cli-1419); the ordinary-profile override and personal fallback below do not apply to them.

## Concepts

- Personal workspace ID is `0`; team workspaces are `> 0` and share a team credit pool.
- The server is the source of truth for the active workspace; the CLI syncs it on login and on `workspace list` / `status`. The active workspace is stored per region.
- All creation, task, asset and account commands run in the active workspace. Switching changes which credits are consumed and which assets are visible.
- Roles: `owner`, `admin`, `member`, `guest`; `null` in personal.

## Commands

| Command | JSON output |
|:---|:---|
| `workspace list --json` | `{"activeWorkspaceId": 42, "workspaces": [{"workspace_id", "name", "role", "member_count"}]}` |
| `workspace status --json` | Personal: `{"workspaceId": 0, "name": "Personal"}`. Team: `{"workspaceId", "name", "role", "memberCount"}`. An inaccessible workspace returns `name: null` |
| `workspace switch <id> --json` | `{"workspaceId", "name", "role"}`; persisted. `0` switches to personal |
| `workspace manage --json` | Opens the region's team management page and returns `{"success": true, "url": "..."}`; use it for members, team plan and billing |

`workspace switch` without an ID is an interactive menu and is unavailable with `--json`. IDs must be non-negative integers; invalid IDs exit 6.

## One-invocation override: `--workspace-id`

```bash
pixverse --workspace-id 42 create video --prompt "Team content" --json
pixverse --workspace-id 0 account info --json
```

The global flag goes before the subcommand, is not persisted, and must be a non-negative integer (otherwise exit 6). Prefer it over repeated `switch` calls when one workflow touches several workspaces, and pass the same value to the later `task` / `asset` commands for those jobs.

## Inaccessible active workspace

If the persisted team workspace becomes inaccessible (for example, the user was removed), a failing command exits 1. The CLI resets the active workspace to personal and appends "switched to personal workspace. Please retry your command." This does not happen with an explicit `--workspace-id` or for workspace-management requests.

Do not simply retry: a retry now runs in **personal** and spends personal credits. Confirm the intended destination with the user, then `workspace switch` to it or pass `--workspace-id` before resubmitting. A `name: null` in `workspace status` means the same thing.

Other errors follow the [execution contract](../references/execution-contract.md).

## Related

- [auth-and-account](auth-and-account.md): `account info` shows workspace context and team credits
- [batch-creation](../workflows/batch-creation.md): batch work with `--workspace-id`
