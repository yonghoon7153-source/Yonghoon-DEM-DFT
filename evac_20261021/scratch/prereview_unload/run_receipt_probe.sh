#!/usr/bin/env bash
# Codex receipt_ids_recheck.py 를 리뷰 핀 사본 (codex_rerun_pin) 에서 다시 — 화면 = logs/receipt_ids_recheck.log
D=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_unload/codex_rerun_pin
cd "$D" || exit 9
mkdir -p tmp logs
export TMPDIR=$D/tmp
python3 -I -X utf8 -B probes/receipt_ids_recheck.py > logs/receipt_ids_recheck.log 2>&1
rc=$?
echo "receipt_ids_recheck rc=$rc"
tail -3 logs/receipt_ids_recheck.log | cut -c1-400
