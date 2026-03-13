#!/usr/bin/env bash
set -euo pipefail
# ─────────────────────────────────────────────
# clip-note.sh — 网页剪藏入口（env 解析 + 转发 clip-note.mjs）
#
# 读取环境变量后通过 argv 传给 clip-note.mjs，使 .mjs 无需访问 process.env。
# 用法：bash clip-note.sh [所有原 clip-note.mjs 参数]
# ─────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

ENV_ARGS=()

if [ -n "${YOUDAONOTE_API_KEY:-}" ]; then
  ENV_ARGS+=(--api-key "$YOUDAONOTE_API_KEY")
fi

if [ -n "${YOUDAONOTE_MCP_URL:-}" ]; then
  ENV_ARGS+=(--sse-url "$YOUDAONOTE_MCP_URL")
fi

if [ -n "${YOUDAONOTE_MCP_TIMEOUT:-}" ]; then
  ENV_ARGS+=(--mcp-timeout "$YOUDAONOTE_MCP_TIMEOUT")
fi

if [ -n "${YOUDAONOTE_CLIP_DEBUG:-}" ]; then
  ENV_ARGS+=(--debug-dir "$YOUDAONOTE_CLIP_DEBUG")
fi

exec node "$SCRIPT_DIR/clip-note.mjs" ${ENV_ARGS[@]+"${ENV_ARGS[@]}"} "$@"
