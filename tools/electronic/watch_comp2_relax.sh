#!/usr/bin/env bash
# =============================================================================
# watch_comp2_relax.sh — comp2 champion 고정셀 DFT relax 감시 (gabia).
#   watch -n 60 'bash ~/Yonghoon-DEM-DFT/tools/electronic/watch_comp2_relax.sh'
# 이온스텝(BFGS)·에너지·총힘(→1e-3 목표)·SCF acc + 완료 시 argyrodite PS4 골격판정.
# =============================================================================
set +H
WORK=${WORK:-/data/work/runs/comp2_relax}
OUT=$WORK/relax.out
LOG=${LOG:-$HOME/comp2_relax.log}
echo "══ comp2 relax (Li6PS5Cl0.5Br0.5 · 고정셀 · argyrodite guard)  $(date '+%m-%d %H:%M:%S') ══"

# 실행상태
if pgrep -f run_comp2_relax_gabia >/dev/null 2>&1; then echo "  러너 실행중 ✔"
else echo "  (러너 안 보임 — 완료됐거나 미시작)"; fi
gpu=$(nvidia-smi --query-gpu=memory.used,memory.free,utilization.gpu --format=csv,noheader 2>/dev/null)
echo "  GPU: ${gpu:-N/A}"

[ -s "$OUT" ] || { echo "  relax.out 아직 없음 (pseudo fetch / 입력생성 중)"; \
  tail -3 "$LOG" 2>/dev/null | sed 's/^/    /'; exit 0; }

# 진행 지표
nstep=$(grep -ac "^!" "$OUT")
elast=$(grep -a "^!" "$OUT" | tail -1 | sed 's/^ *//')
fmax=$(grep -a "Total force" "$OUT" | tail -1 | sed 's/^ *//')
scfacc=$(grep -a "estimated scf accuracy" "$OUT" | tail -1 | sed 's/^ *//')
bfgs=$(grep -a "number of bfgs steps" "$OUT" | tail -1 | sed 's/^ *//')
echo "── relax 진행 (forc_conv_thr = 1e-3 Ry/Bohr) ──"
echo "  수렴 이온스텝(^! 개수) = ${nstep:-0}   ${bfgs:+| $bfgs}"
echo "  최신 에너지 : ${elast:-대기}"
echo "  최신 총힘   : ${fmax:-대기}"
echo "  최신 SCF acc: ${scfacc:-대기}"

# 종료/경고
grep -aq "bfgs converged" "$OUT" && echo "  ✅ $(grep -a 'bfgs converged' "$OUT" | tail -1 | sed 's/^ *//')"
grep -aq "JOB DONE"      "$OUT" && echo "  ✅ JOB DONE"
grep -aqiE "convergence NOT achieved|%%%%%%|Error in routine|stopping" "$OUT" \
  && echo "  ⚠ 경고/에러 감지 — tail 확인"

echo "── relax.out tail ──"; tail -4 "$OUT" | sed 's/^/    /'

# argyrodite 골격판정 (relax 완료 후 러너가 로그에 찍음)
echo "── argyrodite PS4 골격판정 (완료 시) ──"
if grep -aq "골격 검증" "$LOG" 2>/dev/null; then
  grep -aA10 "골격 검증" "$LOG" | tail -13 | sed 's/^/  /'
else
  echo "  (relax 끝나면 자동 표시: PS4 배위 / 변위 / min-dist / 저장여부)"
fi
