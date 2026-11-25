#!/usr/bin/env bash
# watch_umascan.sh — SDCP UMA re-screen (tall-vacuum, image-clean) status on gabia.
#   watch -n 30 'bash ~/Yonghoon-DEM-DFT/tools/sdcp/watch_umascan.sh'
# Reads the umascan launcher log; shows wait-state -> refs -> per-pose E_bind -> ranking.
set +H
BASE=${BASE:-/data/work/runs/sdcp_linio2_binding}
LOG=$BASE/phaseA_tallvac.log
echo "══ SDCP UMA re-screen (c40 image-clean, neutral+doped 24 pose)  $(date '+%m-%d %H:%M:%S') ══"

sess=$(tmux ls 2>/dev/null | grep -oE 'umascan|pbvert' | tr '\n' ' ')
gpu=$(nvidia-smi --query-gpu=memory.used,memory.free,utilization.gpu --format=csv,noheader,nounits 2>/dev/null | head -1)
echo "  세션: ${sess:-없음} | GPU ${gpu} (used,free,util%)"
[ -f "$LOG" ] || { echo "  로그 아직 없음 ($LOG)"; exit 0; }

# --- phase: still waiting for pw.x, or scanning? ---
if ! grep -aq "E_slab" "$LOG"; then
  echo "  단계: ⏳ pw.x(vertical) 대기중 — UMA 스캔 미시작"
  tail -2 "$LOG" | sed 's/^/    /'
  exit 0
fi

# --- references ---
echo "── 레퍼런스 ──"
grep -aE "c-axis ->|E_slab =|E_mol =" "$LOG" | sed 's/^/  /'

# --- poses done + current top (negative = stronger binding) ---
done=$(grep -ac "E_bind =" "$LOG")
echo "── 포즈 ${done}/24  (상위 6, 음수=강결합) ──"
grep -aE "E_bind =" "$LOG" \
  | awk '{v=""; for(i=1;i<=NF;i++) if($i=="=") v=$(i+1); if(v!="") print v, $1}' \
  | sort -n | head -6 | awk '{printf "  %9s eV  %s\n", $1, $2}'

# --- final ranking (image-clean preferred pose) ---
if grep -aq "=== ranking" "$LOG"; then
  echo "── ✅ 스캔 완료 · 최종 랭킹 (image-clean preferred) ──"
  sed -n '/=== ranking/,/saved:/p' "$LOG" | sed 's/^/  /'
  echo "  >> 상위 자세를 DFT refine (같은 c40 셀, neutral+doped) 걸면 진짜 결합 판정"
fi
