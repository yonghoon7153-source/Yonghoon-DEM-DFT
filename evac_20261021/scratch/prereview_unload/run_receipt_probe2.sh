#!/usr/bin/env bash
# Codex receipt_ids_recheck.py 의 Q4 내성 사본 (정밀도 블록만 빈 행 허용) — 리뷰 핀 사본에서 · 화면 = logs/receipt_ids_recheck_q4tolerant.log
D=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_unload/codex_rerun_pin
cd "$D" || exit 9
mkdir -p tmp logs
export TMPDIR=$D/tmp
t0=$(date +%s)
python3 -I -X utf8 -B probes/receipt_ids_recheck_q4tolerant.py > logs/receipt_ids_recheck_q4tolerant.log 2>&1
rc=$?
echo "receipt_ids_recheck_q4tolerant rc=$rc secs=$(( $(date +%s) - t0 ))"
tail -3 logs/receipt_ids_recheck_q4tolerant.log | cut -c1-600
