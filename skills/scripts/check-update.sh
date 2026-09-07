#!/usr/bin/env bash
# Optional manual check; never run automatically during skill loading.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SKILL_DIR/.." && pwd)"
REMOTE_URL="https://raw.githubusercontent.com/PixVerseAI/skills/main/VERSION"

if [ -f "$REPO_ROOT/VERSION" ]; then
  LOCAL_VERSION=$(tr -d '[:space:]' < "$REPO_ROOT/VERSION")
else
  LOCAL_VERSION=$(sed -n 's/^version: *//p' "$SKILL_DIR/SKILL.md" | head -n 1)
fi
REMOTE_VERSION=$(curl -sf --max-time 2 "$REMOTE_URL" 2>/dev/null | tr -d '[:space:]' || true)
# Ignore unavailable or non-release responses; never advertise a downgrade.
[[ $LOCAL_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ && $REMOTE_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || exit 0
IFS=. read -r -a LOCAL_PARTS <<< "$LOCAL_VERSION"
IFS=. read -r -a REMOTE_PARTS <<< "$REMOTE_VERSION"
for i in 0 1 2; do
  if (( 10#${REMOTE_PARTS[i]} > 10#${LOCAL_PARTS[i]} )); then
    printf 'PixVerse Skills update available: v%s -> v%s. Update through your installer, or use skills/scripts/update.sh in a clean source checkout.\n' "$LOCAL_VERSION" "$REMOTE_VERSION"
    exit 0
  fi
  (( 10#${REMOTE_PARTS[i]} < 10#${LOCAL_PARTS[i]} )) && exit 0
done
exit 0
