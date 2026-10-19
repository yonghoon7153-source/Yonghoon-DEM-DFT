#!/bin/bash
cd ~/wt_t50_1019 || exit 9
PY=/home/kgy/apps/miniforge3/envs/uma/bin/python; A=~/work/runs/lpscl_smallcell_2026_09_16/A; O=~/work/runs/lpscl_glass_t50_A_2026_10_19
echo "[$(date '+%F %T')] ▶ 대조 잡 A seed1 (09-21 표 21 창)"
$PY tools/ionic/quench_t50_scan.py --control_A1 --traj $A/seed1/traj.xyz --thermo $A/seed1/thermo.csv --py $PY --out $O/control_A1.json || { echo "⛔ 대조 잡 실패 — A seed2 를 내지 않는다"; exit 1; }
echo "[$(date '+%F %T')] ▶ A seed2"
$PY tools/ionic/quench_t50_scan.py --traj $A/seed2/traj.xyz --thermo $A/seed2/thermo.csv --label A_s2 --py $PY --out $O/t50_A_s2.json || { echo "⛔ A seed2 rc=$?"; exit 2; }
echo "[$(date '+%F %T')] ■ 끝"
