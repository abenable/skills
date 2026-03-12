#!/usr/bin/env bash

# ==============================================================================
# SkillShield local shell pre-check wrapper
# This marketplace build is local-only, uses a small regex denylist,
# and does not contact remote services.
# It is a best-effort pre-check, not a sandbox or complete policy engine.
# ==============================================================================

COMMAND="$*"
if [ -z "$COMMAND" ]; then
    echo "[SkillShield] Refused: missing command argument."
    exit 1
fi

echo "[SkillShield] Running local pre-check."
echo "[SkillShield] Local-only mode. No remote upload. Best-effort regex filter."

DANGEROUS_PATTERNS=(
    "rm[[:space:]]+.*-r.*f[[:space:]]+/"
    "rm[[:space:]]+-rf[[:space:]]+~"
    "rm[[:space:]]+-rf[[:space:]]+/\\*"
    "chmod[[:space:]]+.*-R[[:space:]]+.*/"
    "chown[[:space:]]+.*-R[[:space:]]+.*/"
    "mkfs\\."
    "dd[[:space:]]+if=.*of=/dev/"
    "crontab[[:space:]]+"
    "\\.ssh/v?id_[a-z]+"
    ">[[:space:]]*/etc/.*"
    ">>[[:space:]]*/etc/.*"
    ">[[:space:]]*/boot/.*"
    ">>[[:space:]]*/boot/.*"
    "/dev/tcp/"
    "nc[[:space:]]+-e"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
    if printf '%s' "$COMMAND" | grep -Eq "$pattern"; then
        echo "[SkillShield] Blocked: matched deny pattern [$pattern]"
        exit 126
    fi
done

# Allowed to continue
echo "[SkillShield] Pre-check passed. Executing command."
bash -lc "$COMMAND"
exit $?
