---
name: pixverse:auth-and-account
description: Authenticate with PixVerse, check account info, manage credits, configure CLI defaults, and understand workspace-aware behavior
---

# Auth and Account Management

Covers: `auth login/status/logout`, `account info/usage/slots`, `subscribe`, `config`, `update`, and global options. Exit codes and error handling follow the [execution contract](../references/execution-contract.md); workspace behavior lives in [workspace](workspace.md).

If the host integration runs the CLI under an isolated delegated (paired) profile, use [MCP pairing](../references/auth-pairing.md) instead of the login/logout and access-key instructions below.

## Global options

| Option | Use |
|:---|:---|
| `--json` / `-p` | JSON on stdout only; errors and diagnostics on stderr |
| `--region global\|cn` | Default `global`; `PIXVERSE_REGION` overrides it. Tokens, active workspace and creation defaults are stored per region |
| `--workspace-id <id>` | One-invocation workspace override (`0` = personal); see [workspace](workspace.md) |
| `--trace-id <uuid>` | Attach a caller-chosen trace ID to every API request in this invocation; must be a UUIDv4. Useful for correlating a failure report |

## auth login

OAuth device flow. With `--json` / `-p` the CLI does **not** open a browser: read the `Authorize at: <url> (code: <code>)` line from stderr while the command runs and show that URL to the user. It can be opened in any browser on any device. Stdout receives JSON only after authorization:

```json
{"success": true, "email": "user@example.com", "nickname": "user", "memberType": 2, "tokenExpiresIn": 2592000}
```

`phone` is included when the account has one. After login the CLI syncs the active workspace from the server.

On failure (including the user not authorizing before the session expires), stderr gets `{"success": false, "error": "...", "code": ...}` and the process exits with the typed exit code (for example 3 for authentication), not always 1.

## auth status

```bash
pixverse auth status --json
```

Logged in (stdout): `{"authenticated": true, "email": "...", "nickname": "...", "memberType": "Pro", "credits": 650}`. Here `memberType` is the label, not the number.

Not logged in or token invalid: `{"authenticated": false, ...}` on **stderr**, exit 3. Run `pixverse auth login --json` in the intended region.

## auth logout

`pixverse auth logout --json` → `{"success": true, "message": "Token removed"}`. It also resets the active workspace to personal (`0`).

## Access key (non-interactive automation)

Set `PIXVERSE_ACCESS_KEY` in the environment. It is used only when no stored login token exists and applies to the selected region only. An invalid key exits 3 like an expired token. `PIXVERSE_TOKEN` is not supported.

## account info

```bash
pixverse account info --json
```

Key fields:

- `memberType` / `memberLabel`: subscription tier. 0 Free, 1 Standard, 2 Pro, 3 Premium, 6 Elite, 8 Ultra.
- `credits.total`: available credits (personal balance, or the team pool in a team workspace).
- `credits.daily` / `membership` / `bonus`: personal breakdown; `null` in a team workspace.
- `credits.used`: team consumption; `null` in personal.
- `workspace`: `workspaceId` (`0` = personal), `name`, `role`, `memberCount`, `seats`. Field meanings: [workspace](workspace.md).
- `phone` appears when present.

Example error handling:

```bash
if INFO=$(pixverse account info --json); then
  printf 'Available credits: %s\n' "$(printf '%s\n' "$INFO" | jq -r '.credits.total')"
else
  RC=$?
  [ "$RC" -eq 3 ] && echo "Not authenticated: run pixverse auth login --json in this region" >&2
  exit "$RC"
fi
```

If `credits.total` is 0, stop and report. The user can upgrade at https://app.pixverse.ai/subscribe, or a team admin can manage the team plan with `pixverse workspace manage`.

## account usage

```bash
pixverse account usage --json --type used --limit 10
```

| Flag | Values | Default |
|:---|:---|:---|
| `--type` | `all`, `earned`, `used` (personal only) | `all` |
| `--limit` | items per page | `20` |
| `--page` | page number | `1` |

Output: `{"total", "page", "limit", "items": [...]}`. Item fields differ by workspace:

- Personal: `create_time`, `credits`, `acquired_type` (1 generation, 2 refund for failed generation, 3 membership renewal, 4 expired, 5 task reward, 6 bonus, 7 gift code, 8 referral), optional `video_id`, plus `type` / `sub_type` / `source`.
- Team: your own usage in the team (last 30 days): `created_at`, `email`, `creation_mode`, `model`, `credit_cost`. A `--type` other than `all` exits 6.

## account slots

```bash
pixverse account slots --json
```

```json
{"image": {"limit": 3, "used": 1, "remaining": 2, "unlimited": false}, "video": {"limit": 3, "used": 1, "remaining": 2, "unlimited": false}, "shared_pool": true}
```

Check before parallel submission and after exit 7 (concurrency limit). `shared_pool: true` means image and video draw from one pool. Do not submit more concurrent jobs than `remaining` unless `unlimited` is true.

## subscribe

`pixverse subscribe --json` opens the subscription page and returns `{"success": true, "url": "..."}`. If no browser can be opened, it exits 1 with `success: false` and the `url` to show the user. In a team workspace it exits 6; team billing goes through `pixverse workspace manage`, or switch to personal first.

## config

| Command | Notes |
|:---|:---|
| `config list --json` | `{"outputDir": ..., "_paths": {"dir", "config"}}` |
| `config get <key>` / `config set <key> <value>` | The only settable key is `output-dir` (alias `outputDir`); unknown keys exit 6 |
| `config reset` | Resets configuration |
| `config path --json` | `{"dir": "...", "config": "..."}` |
| `config defaults show [mode]` | All modes, or `{"mode", "defaults"}` for one |
| `config defaults set <mode> <key> <value>` | One key per call |
| `config defaults reset [mode]` | All modes, or one mode back to built-in values |

Creation defaults apply when a flag is omitted; explicit flags always win. They are stored per region. Modes: `video`, `image`, `transition`, `extend`, `modify`, `upscale`, `reference`, `template`, `motion_control`. Keys are snake_case and mode-specific: `model`, `quality`, `duration`, `aspect_ratio`, `count`, `audio`, `multi_shot`, `off_peak` (`upscale` accepts only `quality`). Models are validated against the mode; invalid values exit 6.

```bash
pixverse config defaults set video model v6 --json
pixverse config defaults set video quality 1080p --json
```

Do not change a user's saved defaults unless asked; pass flags per command instead.

## update

`pixverse update --json` runs `npm i -g pixverse@latest` and returns `{"success": true, "from": "<old version>", "command": "..."}`; failures exit 1. It changes the user's global installation, so ask the user first. It updates the CLI, not this skill; the skill checkout has its own `scripts/update.sh`.

## Related

- [workspace](workspace.md): list, switch, and override workspaces
- [task-management](task-management.md) and [asset-management](asset-management.md)
