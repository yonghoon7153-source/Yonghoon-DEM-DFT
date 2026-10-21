#!/bin/bash
# Gate batch 2 + 3 (main 7f99be67c) holding gate.lock AND both heavy slots, so agent heavy runs wait
# (10-21 09:22 run failed only because mixer_smoke_blind --selftest hit 180 s under a 9-agent load; alone = 57 s rc 0).
S=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad
cd /home/user/Yonghoon-DEM-DFT || exit 9
LOG=$S/refaudit/gate_7f99.log
H=$(git rev-parse HEAD)
echo "gate start $(date -Iseconds) HEAD $H" > "$LOG"
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  flock -w 21600 $S/gate.lock flock -w 21600 $S/heavy.lock flock -w 21600 $S/heavy2.lock \
  nice -n 19 bash scripts/check_all.sh >> "$LOG" 2>&1
rc=$?
echo "gate rc $rc $(date -Iseconds)" >> "$LOG"
if [ $rc -ne 0 ] || ! tail -5 "$LOG" | grep -q "✓ 전부 통과"; then echo "GATE FAILED (rc $rc)"; tail -25 "$LOG"; exit 1; fi
[ "$(git rev-parse HEAD)" = "$H" ] || { echo "HEAD moved during gate — not pushing"; exit 2; }
for d in 0 2 4 8 16; do sleep $d; if git push -u origin claude/stoic-knuth-NObVQ >> "$LOG" 2>&1; then echo "PUSHED $H"; git fetch -q origin claude/stoic-knuth-NObVQ; echo "origin $(git rev-parse --short FETCH_HEAD)"; exit 0; fi; done
echo "PUSH FAILED"; tail -10 "$LOG"; exit 3
