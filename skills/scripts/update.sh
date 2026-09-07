#!/usr/bin/env bash
# Update a clean source checkout without stashing, switching, or rebasing.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$REPO_ROOT"

if ! TOP_LEVEL=$(git rev-parse --show-toplevel 2>/dev/null) || [ "$(cd "$TOP_LEVEL" && pwd -P)" != "$(pwd -P)" ]; then
  echo "Error: this is not a PixVerse Skills source checkout. Update an installed skill through its installer."
  exit 1
fi
if [ "$(git branch --show-current)" != "main" ]; then
  echo "Error: updates require the main branch. No branch or file was changed."
  exit 1
fi
if [ -n "$(git status --porcelain --untracked-files=all)" ]; then
  echo "Error: the checkout has local changes or untracked files. Preserve them before updating."
  exit 1
fi
REMOTE=$(git remote get-url origin) || exit 1
OLD_VERSION=$(tr -d '[:space:]' < VERSION)
printf 'Fast-forward this checkout from %s (main)? [y/N] ' "$REMOTE"
if ! IFS= read -r REPLY || [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo "Aborted. No files changed."
  exit 0
fi
# --ff-only rejects divergent history; no automatic stash or rebase.
git pull --ff-only origin main
NEW_VERSION=$(tr -d '[:space:]' < VERSION)
if [ "$OLD_VERSION" = "$NEW_VERSION" ]; then
  echo "Already at version $NEW_VERSION."
else
  echo "Updated: v$OLD_VERSION -> v$NEW_VERSION"
fi
