#!/bin/bash
cd /home/user/Yonghoon-DEM-DFT || exit 9
LOG=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/refaudit/gate_10173a053.log
H=$(git rev-parse HEAD); echo "gate start $(date -Iseconds) HEAD $H" > "$LOG"
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 bash scripts/check_all.sh >> "$LOG" 2>&1
rc=$?; echo "gate rc $rc $(date -Iseconds)" >> "$LOG"; echo "EXIT=$rc"
if [ $rc -ne 0 ] || ! tail -5 "$LOG" | grep -q "✓ 전부 통과"; then echo "GATE FAILED (rc $rc)"; tail -25 "$LOG"; exit 1; fi
[ "$(git rev-parse HEAD)" = "$H" ] || { echo "HEAD moved during gate"; exit 2; }
echo "GATE PASSED $H"
