#!/usr/bin/env bash
CMD="$1"; shift 2>/dev/null; INPUT="$*"
case "$CMD" in
  create) cat << 'PROMPT'
You are an expert. Help with: 生成配置文件. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  plugin) cat << 'PROMPT'
You are an expert. Help with: 插件配置. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  loader) cat << 'PROMPT'
You are an expert. Help with: Loader配置. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  optimize) cat << 'PROMPT'
You are an expert. Help with: 性能优化. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  split) cat << 'PROMPT'
You are an expert. Help with: 代码分割. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  migrate) cat << 'PROMPT'
You are an expert. Help with: Webpack→Vite迁移. Provide detailed, practical output. Use Chinese.
User request:
PROMPT
    echo "$INPUT" ;;
  *) cat << 'EOF'
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Webpack Config — 使用指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  create          生成配置文件
  plugin          插件配置
  loader          Loader配置
  optimize        性能优化
  split           代码分割
  migrate         Webpack→Vite迁移

  Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
EOF
    ;;
esac
