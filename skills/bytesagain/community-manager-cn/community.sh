#!/usr/bin/env bash
CMD="$1"; shift 2>/dev/null; INPUT="$*"
case "$CMD" in
  build) cat << 'PROMPT'
You are an expert. Help with: 社群搭建方案. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  engage) cat << 'PROMPT'
You are an expert. Help with: 活跃度提升. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  content) cat << 'PROMPT'
You are an expert. Help with: 内容规划. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  grow) cat << 'PROMPT'
You are an expert. Help with: 用户增长策略. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  monetize) cat << 'PROMPT'
You are an expert. Help with: 变现策略. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  crisis) cat << 'PROMPT'
You are an expert. Help with: 危机处理. Provide detailed, practical output in Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  *) cat << 'EOF'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Community Manager — 使用指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  build           社群搭建方案
  engage          活跃度提升
  content         内容规划
  grow            用户增长策略
  monetize        变现策略
  crisis          危机处理

  Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
EOF
    ;;
esac
