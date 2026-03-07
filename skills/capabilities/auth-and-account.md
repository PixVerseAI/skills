---
name: pixverse:auth-and-account
description: Authenticate with PixVerse, check account info, manage credits, and configure CLI defaults
---

# Auth and Account Management

Covers: `auth login`, `auth logout`, `auth status`, `account info`, `account usage`, `config set/get/list/reset/path/defaults`

---

## auth login

OAuth device flow — the CLI prints an authorization URL, the user opens it in a browser and authorizes, and the token is stored automatically.

```bash
pixverse auth login --json
```

JSON output on success:
```json
{
  "message": "Login successful",
  "user": {
    "accountId": 12345,
    "email": "user@example.com",
    "nickname": "user",
    "username": "user",
    "memberType": 2,
    "memberLabel": "Pro"
  }
}
```

Decision tree:
- If exit code 0 -> login succeeded, token is stored in `~/.pixverse/`
- If exit code 1 -> unexpected error, check stderr
- If the user does not complete the browser authorization within the timeout, the command will fail

---

## auth status

Check whether the CLI is currently authenticated and display user info.

```bash
pixverse auth status --json
```

JSON output when logged in:
```json
{
  "authenticated": true,
  "user": {
    "accountId": 12345,
    "email": "user@example.com",
    "nickname": "user",
    "username": "user",
    "memberType": 2,
    "memberLabel": "Pro"
  }
}
```

JSON output when not logged in:
```json
{
  "authenticated": false
}
```

Decision tree:
- If `authenticated` is `true` -> proceed with CLI commands
- If `authenticated` is `false` -> run `pixverse auth login --json` first

---

## auth logout

Remove the stored token.

```bash
pixverse auth logout --json
```

JSON output:
```json
{
  "message": "Logged out successfully"
}
```

---

## account info

Display account details and credit balance.

```bash
pixverse account info --json
```

JSON output:
```json
{
  "accountId": 12345,
  "email": "user@example.com",
  "nickname": "user",
  "username": "user",
  "memberType": 2,
  "memberLabel": "Pro",
  "isCreator": false,
  "credits": {
    "daily": 100,
    "membership": 500,
    "bonus": 50,
    "total": 650,
    "highQualityTimes": 10,
    "renewalCredits": 500
  }
}
```

Key fields:
- `credits.total` — total available credits across all types
- `credits.daily` — credits that reset daily
- `credits.membership` — credits from subscription tier
- `credits.bonus` — bonus credits (promotions, etc.)
- `credits.highQualityTimes` — remaining high-quality generation slots
- `memberType` — subscription tier (0 = free, 1 = Basic, 2 = Pro, 3 = Team)
- `memberLabel` — human-readable subscription name

Decision tree:
- If `credits.total` > 0 -> user can create content
- If `credits.total` == 0 -> wait for daily reset or upgrade subscription at https://app.pixverse.ai/subscribe
- If exit code 3 -> token expired, re-run `pixverse auth login --json`

---

## account usage

View credit usage history.

```bash
pixverse account usage --json --type used --limit 10
```

Options:
| Flag | Values | Default | Description |
|:---|:---|:---|:---|
| `--type` | `all`, `earned`, `used` | `all` | Filter by transaction type |
| `--limit` | any positive integer | `20` | Number of items per page |
| `--page` | any positive integer | `1` | Page number |

JSON output:
```json
{
  "total": 100,
  "page": 1,
  "limit": 10,
  "items": [
    {
      "id": 1,
      "type": "used",
      "amount": -10,
      "description": "Video generation",
      "createdAt": "2026-03-01T12:00:00Z"
    }
  ]
}
```

---

## config commands

### List all config values

```bash
pixverse config list --json
```

### Get a specific config value

```bash
pixverse config get <key> --json
```

Example:
```bash
pixverse config get output-dir --json
```

### Set a config value

```bash
pixverse config set <key> <value> --json
```

Example:
```bash
pixverse config set output-dir /tmp/pixverse-output --json
```

### Reset all config to defaults

```bash
pixverse config reset --json
```

### Show config file path

```bash
pixverse config path --json
```

JSON output:
```json
{
  "path": "/Users/you/.pixverse/config.json"
}
```

### View per-mode creation defaults

```bash
pixverse config defaults show --json
```

JSON output:
```json
{
  "video": {
    "model": "v5.6",
    "quality": "1080p",
    "duration": "5",
    "aspectRatio": "16:9"
  },
  "image": {
    "model": "v5.6",
    "quality": "1080p",
    "aspectRatio": "16:9"
  }
}
```

### Set per-mode creation defaults

```bash
pixverse config defaults set --mode video --model v5.6 --quality 1080p --json
```

This sets default values that apply when you run `pixverse create video` without specifying those flags explicitly. Command-line flags always override defaults.

### Reset per-mode creation defaults

```bash
pixverse config defaults reset --json
```

---

## Steps: First-Time Setup Recipe

1. **Install the CLI**
   ```bash
   npm install -g pixverse
   pixverse --version
   ```

2. **Authenticate**
   ```bash
   pixverse auth login --json
   ```
   The CLI will print a URL. Open it in a browser and authorize. On success, the token is stored in `~/.pixverse/`.

3. **Verify authentication**
   ```bash
   pixverse auth status --json
   ```
   Confirm `authenticated` is `true`.

4. **Check credits**
   ```bash
   pixverse account info --json
   ```
   Parse `credits.total` to confirm the user has credits available.

5. **Check usage history** (optional)
   ```bash
   pixverse account usage --json --type used --limit 10
   ```

6. **Configure defaults** (optional)
   ```bash
   pixverse config defaults set --mode video --model v5.6 --quality 1080p --json
   ```

7. **Token refresh**: If any command exits with code 3, re-run `pixverse auth login --json`. The environment variable `PIXVERSE_TOKEN` overrides the stored token if set.

---

## Error Handling

| Exit Code | Cause | Recovery |
|:---|:---|:---|
| 0 | Success | -- |
| 1 | Unexpected error | Check stderr for details |
| 3 | Token expired or invalid | Re-run `pixverse auth login --json` |
| Network error | No internet or API unreachable | Check internet connection, retry |

Example error handling:
```bash
pixverse account info --json 2>/tmp/pixverse_err
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  CREDITS=$(cat /dev/stdin | jq -r '.credits.total')
  echo "Available credits: $CREDITS"
elif [ $EXIT_CODE -eq 3 ]; then
  echo "Token expired, re-authenticating..."
  pixverse auth login --json
else
  echo "Error (code $EXIT_CODE):"
  cat /tmp/pixverse_err
fi
```

---

## Related Skills

- `pixverse:create-video` — create videos from text or image
- `pixverse:create-and-edit-image` — create or edit images
- `pixverse:task-management` — check generation progress and wait for completion
- `pixverse:asset-management` — browse, download, or delete generated assets
