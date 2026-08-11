#!/usr/bin/env bash
# UserPromptSubmit 훅 — 컨텍스트 점유율이 임계를 넘으면 한 줄 알린다 (평소엔 조용).
#   임계/창 조정: CLAUDE_CONTEXT_THRESHOLD (기본 50) · CLAUDE_CONTEXT_WINDOW (기본 auto)
#   ⚠ 훅은 절대 세션을 막지 않는다 — 어떤 실패에도 exit 0.
#
# ⚠⚠ settings.json 에 **autoCompactWindow 를 넣지 말 것** (2026-08-11, 다른 브랜치 실사고:
#     압축이 계속 돌아 대화가 못 쓰게 됐다).  이 계기는 **알리기만** 한다 — 압축 여부는
#     사람이 정한다.  자동압축을 물리면 "압축 직후의 스테일 읽기"가 곧바로 다음 압축을
#     부르는 무한루프가 된다 (context_meter.py 가드 ① 참조).
exec python3 "$CLAUDE_PROJECT_DIR/scripts/context_meter.py" --hook 2>/dev/null || exit 0
