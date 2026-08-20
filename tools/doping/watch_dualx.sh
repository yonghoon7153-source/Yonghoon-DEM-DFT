#!/usr/bin/env bash
# Watch a dual-x sweep (high-x or low-x). Auto-detects the driver process, the
# current dopant + its stage, per-dopant done count (STAGE_04.DONE), liveness,
# and GPU (shared with the main cascade).
# Usage:  bash tools/doping/watch_dualx.sh [highx|lowx]   (default highx)
set +H
SUF="${1:-highx}"
DX=/data/work/runs/dualx_v23
DOPANTS=(Sc2O3 Gd2O3 Cr2O3 Y2O3 La2O3 HfO2 Ta2O5 Nb2O5 V2O5 TiF4)

echo "════════════ $(date '+%Y-%m-%d %H:%M:%S')  dual-x ${SUF} watch ════════════"

# ---- 1. driver process ----
if [ "$SUF" = lowx ]; then DPID=$(pgrep -f "run_dualx.sh" | head -1)
else DPID=$(pgrep -f "run_dualx_${SUF}.sh" | head -1); fi
if [ -n "$DPID" ]; then
  echo "driver ✅ 실행중   PID=$DPID   가동 $(ps -o etime= -p "$DPID" 2>/dev/null | tr -d ' ')"
else
  echo "driver ⛔ 프로세스 없음 (완료했거나 중단 — 아래 진행도로 판단)"
fi
pgrep -af "tier_cascade|run_anneal|run_screen|run_eos|run_bvse" 2>/dev/null \
  | grep -i "${SUF}" | head -2 | sed 's/^/  child: /'

# ---- 2. per-dopant progress (STAGE_04.DONE = mobility pipeline done) ----
done=0; cur=""
echo "── 도펀트별 (mobility = STAGE_04.DONE) ──"
for c in "${DOPANTS[@]}"; do
  O=$DX/${c}_${SUF}
  if [ -f "$O/STAGE_04.DONE" ]; then
    st="✅ done (stage04)"; done=$((done+1))
  elif [ -d "$O" ]; then
    last=$(ls -d "$O"/[0-9]*_* 2>/dev/null | sed 's#.*/##' | tail -1)
    st="⏳ ${last:-시작중}"; [ -z "$cur" ] && cur=$c
  else
    st="·  대기"
  fi
  printf "  %-7s %s\n" "$c" "$st"
done
echo "진행: ${done}/10 완료   현재 처리: ${cur:-(없음 — 모두 끝났을 수 있음)}"

# ---- 3. current dopant latest log ----
if [ -n "$cur" ]; then
  L=$DX/${cur}_${SUF}.log
  echo "── $cur 최근 로그 (${L##*/}) ──"
  tail -3 "$L" 2>/dev/null | sed 's/^/    /'
fi

# ---- 4. liveness (any *_SUF log touched in last 5 min) ----
R=$(find "$DX" -path "*_${SUF}*" -name "*.log" -newermt "-5 min" 2>/dev/null | head -1)
if [ -n "$R" ]; then echo "🟢 진행중 (5분내 갱신: ${R##*/})"
else echo "🔴 5분내 갱신 없음 — 정체/완료 의심"; fi

# ---- 5. GPU (shared with main cascade) ----
echo "── GPU (메인 cascade와 공유) ──"
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null \
  | sed 's/^/  /' || echo "  (nvidia-smi 없음)"
