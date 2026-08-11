#!/bin/bash
# 컨텍스트 사용률 게이지만 표시한다. 압축 관련 경고·안내는 넣지 않는다
# (2026-08-11 제거: 자동 압축 설정 자체를 `.claude/settings.json` 에서 뺐다).
# stdin 으로 세션 JSON 을 받는다 (`context_window.used_percentage` 등).
set -u

IN=$(cat)
PY=$(command -v python3 || command -v python)

if command -v jq >/dev/null 2>&1; then
  PCT=$(printf '%s' "$IN" | jq -r '.context_window.used_percentage // 0')
  MODEL=$(printf '%s' "$IN" | jq -r '.model.display_name // "?"')
  DIR=$(printf '%s' "$IN" | jq -r '.workspace.current_dir // .cwd // ""')
else
  read -r PCT MODEL DIR < <(printf '%s' "$IN" | "$PY" -c '
import json, sys
d = json.load(sys.stdin)
cw = d.get("context_window") or {}
w = d.get("workspace") or {}
print(round(float(cw.get("used_percentage") or 0)),
      (d.get("model") or {}).get("display_name", "?"),
      w.get("current_dir") or d.get("cwd") or "")
' 2>/dev/null)
fi

PCT_I=${PCT%.*}; PCT_I=${PCT_I:-0}
BRANCH=$(git -C "${DIR:-.}" rev-parse --abbrev-ref HEAD 2>/dev/null)

# 색만 바꾼다: <70% 초록 · 70~89% 노랑 · >=90% 빨강. 안내 문구 없음.
if   [ "$PCT_I" -ge 90 ]; then C=$'\033[31m'
elif [ "$PCT_I" -ge 70 ]; then C=$'\033[33m'
else                          C=$'\033[32m'
fi
R=$'\033[0m'; DIM=$'\033[2m'

FILL=$(( PCT_I / 5 )); [ "$FILL" -gt 20 ] && FILL=20
BAR=""; i=0
while [ "$i" -lt 20 ]; do
  if [ "$i" -lt "$FILL" ]; then BAR="${BAR}█"; else BAR="${BAR}░"; fi
  i=$((i+1))
done

printf '%s[%s]%s %s%s%s  %s%s %d%%%s\n' \
  "$DIM" "$MODEL" "$R" \
  "$DIM" "${BRANCH:-?}" "$R" \
  "$C" "$BAR" "$PCT_I" "$R"
