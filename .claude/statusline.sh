#!/bin/bash
# 컨텍스트 사용률을 항상 눈에 보이게 — 50% 를 넘으면 /compact 하라고 경고한다.
# stdin 으로 세션 JSON 을 받는다 (`context_window.used_percentage` 등).
#
# 왜 50%인가: 이 저장소의 세션은 긴 리뷰 원문·테스트 출력·diff 를 계속 싣는다.
# 자동 압축이 걸리는 지점까지 채우면 그 시점의 세부(반례 출력·검사 이름)가
# 요약에 눌려 사라진다. 절반에서 미리 접으면 압축이 남길 여유가 크다.
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

# <35% 초록 · 35~49% 노랑 · >=50% 빨강 + /compact 안내
if   [ "$PCT_I" -ge 50 ]; then C=$'\033[31m'; TAG="  ← /compact 하세요 (50% 초과)"
elif [ "$PCT_I" -ge 35 ]; then C=$'\033[33m'; TAG="  (50% 접근)"
else                          C=$'\033[32m'; TAG=""
fi
R=$'\033[0m'; DIM=$'\033[2m'

FILL=$(( PCT_I / 5 )); [ "$FILL" -gt 20 ] && FILL=20
BAR=""; i=0
while [ "$i" -lt 20 ]; do
  if [ "$i" -lt "$FILL" ]; then BAR="${BAR}█"; else BAR="${BAR}░"; fi
  i=$((i+1))
done

printf '%s[%s]%s %s%s%s  %s%s %d%%%s%s\n' \
  "$DIM" "$MODEL" "$R" \
  "$DIM" "${BRANCH:-?}" "$R" \
  "$C" "$BAR" "$PCT_I" "$R" "$TAG"
