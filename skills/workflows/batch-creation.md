---
name: pixverse:batch-creation
description: Create multiple videos or images in parallel for efficiency
---

### Strategies

**Strategy 1: Single command with --count**
```bash
RESULT=$(pixverse create video --prompt "A colorful parrot" --count 4 --no-wait --json)
# Returns: { "video_id": 111, "video_ids": [111, 112, 113, 114], ... }
# Wait for each
for ID in $(echo "$RESULT" | jq -r '.video_ids[]'); do
  pixverse task wait $ID --json
done
```

**Strategy 2: Parallel commands with different prompts**
```bash
# Launch in parallel
pixverse create video --prompt "A sunset over mountains" --no-wait --json > /tmp/v1.json &
pixverse create video --prompt "A sunrise over ocean" --no-wait --json > /tmp/v2.json &
pixverse create video --prompt "Northern lights over tundra" --no-wait --json > /tmp/v3.json &
wait

# Collect IDs and wait
for f in /tmp/v1.json /tmp/v2.json /tmp/v3.json; do
  ID=$(jq -r '.video_id' "$f")
  pixverse task wait $ID --json
  pixverse asset download $ID --json
done
```

**Strategy 3: Variations (same prompt, different seeds)**
```bash
for SEED in 42 123 999 2024; do
  pixverse create video --prompt "A cat playing piano" --seed $SEED --no-wait --json
done
```

### Credit Awareness
Always check balance before batch creation:
```bash
CREDITS=$(pixverse account info --json | jq -r '.credits.total')
echo "Available credits: $CREDITS"
# Each generation costs credits — verify you have enough for the batch
```

### Workspace Context
All creation commands run in the active workspace. To batch-create across multiple workspaces without switching, use the global `--workspace-id` flag:
```bash
pixverse --workspace-id 42 create video --prompt "Team content" --no-wait --json > /tmp/team.json &
pixverse --workspace-id 0 create video --prompt "Personal content" --no-wait --json > /tmp/personal.json &
wait
```

### Related Skills
`pixverse:create-video`, `pixverse:create-and-edit-image`, `pixverse:task-management`, `pixverse:auth-and-account`, `pixverse:workspace`
