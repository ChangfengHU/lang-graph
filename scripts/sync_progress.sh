#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: scripts/sync_progress.sh \"commit message\""
  echo "Example: scripts/sync_progress.sh \"Sync progress after lesson 2\""
  exit 1
fi

commit_message="$1"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Error: not inside a git repository."
  exit 1
fi

echo "[check] Running tests..."
uv run pytest

echo "[check] Current changes:"
git status --short

if git diff --quiet && git diff --cached --quiet; then
  echo "[done] No changes to sync."
  exit 0
fi

echo "[git] Staging progress files..."
git add \
  AGENTS.md \
  README.md \
  STUDY_GUIDE.md \
  docs \
  examples \
  lessons \
  scripts \
  tests \
  pyproject.toml \
  uv.lock \
  .gitignore

if git diff --cached --quiet; then
  echo "[done] No staged changes to commit."
  exit 0
fi

echo "[git] Committing..."
git commit -m "$commit_message"

echo "[git] Pushing..."
git push

echo "[done] Progress synced to remote."
