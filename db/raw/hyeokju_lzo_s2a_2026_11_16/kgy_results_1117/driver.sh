#!/usr/bin/env bash
set -uo pipefail
cd "/home/kgy/work/runs/hj_s2a_1116" || exit 2
echo "[$(date '+%m-%d %H:%M:%S')] 시작 · commit $(cat SOURCE_COMMIT)"
export QE_FROM_LDD=1 PW="/home/kgy/apps/qe-7.4.1-gpu/bin/pw.x" QE="/home/kgy/apps/qe-7.4.1-gpu/bin/pw.x" DOSX="/home/kgy/apps/qe-7.4.1-gpu/bin/dos.x" PROJ="/home/kgy/apps/qe-7.4.1-gpu/bin/projwfc.x" SEI_MIN_FREE_MIB="8000"
WORK="/home/kgy/work/runs/hj_s2a_1116/main" bash "/home/kgy/wt_hj2a/tools/sei/run_sei_dft.sh" P2O5_mp-aaaaadqi
python3 "/home/kgy/wt_hj2a/tools/sei/extract_gap.py" --control_gate "/home/kgy/wt_hj2a/db/properties/cei_product_gap_card_2026_10_27.json" --work "/home/kgy/work/runs/hj_s2a_1116/main" \
  || { echo "⛔ 대조 잡 실패 — Li2ZrO3 를 돌리지 않는다 (main/control_gate.json)"; exit 3; }
WORK="/home/kgy/work/runs/hj_s2a_1116/main" bash "/home/kgy/wt_hj2a/tools/sei/run_sei_dft.sh" Li2ZrO3_mp-aaaaagdw
WORK="/home/kgy/work/runs/hj_s2a_1116/ecut90" bash "/home/kgy/wt_hj2a/tools/sei/run_sei_dft.sh" Li2ZrO3_mp-aaaaagdw
echo "[$(date '+%m-%d %H:%M:%S')] 끝"
