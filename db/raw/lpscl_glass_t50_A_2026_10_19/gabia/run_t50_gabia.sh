#!/bin/bash
cd /data/work/wt_read_1019 || exit 9
PY=/data/apps/miniforge3/envs/uma/bin/python; AG=/data/work/runs/lpscl_smallcell_gabia/A; O=/data/work/runs/lpscl_glass_t50_A_2026_10_19
echo "[$(date '+%F %T')] ▶ 대조 잡 — B 다섯 (저장소 궤적) 재현"
$PY tools/ionic/quench_t50_scan.py --control_B --py $PY --out $O/control_B.json || { echo "⛔ 대조 잡 실패 — A 를 내지 않는다"; exit 1; }
for s in 3 4 5; do
  echo "[$(date '+%F %T')] ▶ A seed$s"
  $PY tools/ionic/quench_t50_scan.py --traj $AG/seed$s/traj.xyz --thermo $AG/seed$s/thermo.csv --label A_s$s --py $PY --out $O/t50_A_s$s.json || { echo "⛔ A seed$s rc=$?"; exit 2; }
done
echo "[$(date '+%F %T')] ■ 끝"
