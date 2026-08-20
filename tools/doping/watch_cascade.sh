#!/usr/bin/env bash
# Accurate v23 cascade watch. Auto-detects the LIVE master PID, its active log,
# progress, recent pace, ETA, current cascade stage, liveness, and GPU.
# No hardcoded/stale PID (the old watch_v23.sh tracked a dead PID and false-alarmed).
# Usage:  bash tools/doping/watch_cascade.sh [BATCH_DIR]
set +H
D="${1:-/data/work/runs/multi_category_2026_05_26_v23}"
TOTAL=273

echo "════════════ $(date '+%Y-%m-%d %H:%M:%S')  cascade watch ════════════"
echo "BATCH_DIR: $D"

# ---- 1. live master (auto-detect, not hardcoded) ----
MPID=$(pgrep -f "master_batch_273.sh" | head -1)
if [ -n "$MPID" ]; then
  ET=$(ps -o etime= -p "$MPID" 2>/dev/null | tr -d ' ')
  echo "마스터 ✅ 실행중   PID=$MPID   가동 $ET"
else
  echo "마스터 ⛔ 실행중인 master_batch_273.sh 없음 (끝났거나 중단)"
fi

# ---- 2. active log (what master writes to; fallback newest master_*.log) ----
LOG=""
[ -n "$MPID" ] && LOG=$(readlink -f /proc/$MPID/fd/1 2>/dev/null | grep -E '\.log$')
[ -z "$LOG" ] && LOG=$(ls -t "$D"/master_*.log 2>/dev/null | head -1)
echo "활성 로그: ${LOG:-(없음)}"

NAME=""
if [ -n "$LOG" ] && [ -f "$LOG" ]; then
  # ---- 3. progress ----
  CURLINE=$(grep -E "Step [0-9]+/$TOTAL.*START" "$LOG" | tail -1)
  CURN=$(echo "$CURLINE" | grep -oE "Step [0-9]+" | grep -oE "[0-9]+" | head -1)
  NAME=$(echo "$CURLINE" | sed -E "s#.*Step [0-9]+/$TOTAL: ([A-Za-z0-9_]+).*#\1#")
  DONE_RUN=$(grep -c "✓ DONE" "$LOG")
  echo "진행: Step ${CURN:-?}/$TOTAL   현재 cascade: ${NAME:-?}   (이번 런 완료 $DONE_RUN개)"

  # ---- 4. recent pace + ETA (last 6 DONE timestamps) ----
  mapfile -t TS < <(grep -E "Step [0-9]+/$TOTAL.* DONE" "$LOG" | tail -6 \
                    | grep -oE "^\[[0-9-]+ [0-9:]+\]" | tr -d '[]')
  if [ "${#TS[@]}" -ge 2 ]; then
    t0=$(date -d "${TS[0]}" +%s 2>/dev/null)
    t1=$(date -d "${TS[$(( ${#TS[@]}-1 ))]}" +%s 2>/dev/null)
    n=$(( ${#TS[@]} - 1 ))
    if [ -n "$t0" ] && [ -n "$t1" ] && [ "$n" -gt 0 ] && [ -n "$CURN" ]; then
      pace=$(( (t1 - t0) / n ))                 # sec/cascade (recent, compute-bound)
      rem=$(( TOTAL - CURN ))
      eta_h=$(( rem * pace / 3600 ))
      echo "최근 pace ~$(( pace/60 ))분/cascade  |  남은 ~${rem}개  →  ETA ~$(( eta_h/24 ))일 $(( eta_h%24 ))시간"
      echo "  (현재 pace 기준 상한 — 남은 중 이미 done인 건 SKIP되어 더 빠를 수 있음)"
    fi
  fi
fi

# ---- 5. current cascade stage detail ----
if [ -n "$NAME" ] && [ -d "$D/$NAME" ]; then
  echo "── $NAME ──"
  echo "  존재 stage: $(ls -d "$D/$NAME"/[0-9]*_* 2>/dev/null | sed 's#.*/##' | tr '\n' ' ')"
  LL=$(find "$D/$NAME" -name "*.log" -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)
  if [ -n "$LL" ]; then echo "  최근 로그(${LL##*/}):"; tail -2 "$LL" 2>/dev/null | sed 's/^/    /'; fi
fi

# ---- 6. liveness (any log touched in last 5 min?) ----
RECENT=$(find "$D" -name "*.log" -newermt "-5 min" 2>/dev/null | head -1)
if [ -n "$RECENT" ]; then echo "🟢 진행중 (5분내 갱신: ${RECENT##*/})"
else echo "🔴 5분내 갱신 없음 — 정체/종료 의심"; fi

# ---- 7. GPU ----
echo "── GPU ──"
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null | sed 's/^/  /' \
  || echo "  (nvidia-smi 없음)"
