#!/usr/bin/env bash
# OpenClaw Backup Script ☺️🌸
# Purpose: Syncs .openclaw configuration and workspace to a Git-managed directory and pushes to remote.

set -e

# Fetch repository URL from OpenClaw config
REPO_URL=$(openclaw config get skills.entries.openclaw-backup-restore.env.OPENCLAW_BACKUP_REPO 2>/dev/null | tr -d '"')

if [ -z "$REPO_URL" ] || [ "$REPO_URL" == "null" ]; then
    echo "Error: OPENCLAW_BACKUP_REPO is not set in openclaw.json."
    echo "Please set it via: openclaw config set skills.entries.openclaw-backup-restore.env.OPENCLAW_BACKUP_REPO "your-git-repo-url""
    exit 1
fi

SOURCE="${HOME}/.openclaw/"
BACKUP_DIR="${HOME}/openclaw-backup/"
LOG_FILE="/tmp/openclaw-backup.log"

echo "[$(date)] Starting OpenClaw backup to ${REPO_URL}..." | tee -a "$LOG_FILE"

# Ensure the backup directory exists and initialize git if necessary
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Initializing backup directory at $BACKUP_DIR..."
    mkdir -p "$BACKUP_DIR"
    cd "$BACKUP_DIR"
    git init
    git remote add origin "$REPO_URL"
else
    # Update remote URL if changed in config
    cd "$BACKUP_DIR"
    git remote set-url origin "$REPO_URL" || true
fi

# Sync files using .gitignore rules from the backup directory
# Logic: Even if the source lacks .gitignore, rsync uses the one in the backup folder
rsync -av --delete \
  --exclude-from="${BACKUP_DIR}.gitignore" \
  --exclude=".git/" \
  --exclude=".gitignore" \
  "$SOURCE" "$BACKUP_DIR"

# Commit and Push changes
cd "$BACKUP_DIR"
if [[ -n $(git status -s) ]]; then
    git add .
    git commit -m "Backup: $(date +'%Y-%m-%d %H:%M:%S')"
    git push origin main
    echo "[$(date)] Changes committed and pushed successfully." | tee -a "$LOG_FILE"
else
    # Attempt a push anyway to ensure remote is synced
    git push origin main || true
    echo "[$(date)] No changes detected, ensuring remote is synced." | tee -a "$LOG_FILE"
fi

echo "[$(date)] Backup complete! ☺️🌸" | tee -a "$LOG_FILE"
