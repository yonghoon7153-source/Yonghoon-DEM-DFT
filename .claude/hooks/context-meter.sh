#!/usr/bin/env bash
# UserPromptSubmit 훅 — 컨텍스트 점유율이 임계를 넘으면 한 줄 알린다 (평소엔 조용).
#   임계/창 조정: CLAUDE_CONTEXT_THRESHOLD (기본 50) · CLAUDE_CONTEXT_WINDOW (기본 auto)
#   ⚠ 훅은 절대 세션을 막지 않는다 — 어떤 실패에도 exit 0.
exec python3 "$CLAUDE_PROJECT_DIR/scripts/context_meter.py" --hook 2>/dev/null || exit 0
