#!/usr/bin/env bash
W=/home/kgy/wt_hj_md1; R=/home/kgy/work/runs/hj_md1_1120; PY=/home/kgy/apps/miniforge3/envs/uma/bin/python; ST=$W/db/structures/hyeokju_md1_2026_11_20
ts(){ date '+%m-%d %H:%M:%S'; }
echo "[$(ts)] 시작 · commit $(cat $R/SOURCE_COMMIT) · 세 시드 동시"
for k in 1 2 3; do
  s=$((20261120 + k))
  mkdir -p $R/s$k
  "$PY" -u $W/tools/oxidation/run_li_interface_md.py --interface $ST/I142_liouter_aLZO16_md1s${k}_init.xyz --label md1s$k --out_dir $R/s$k \
    --freeze_idx $ST/I142_liouter_aLZO16_md1s${k}_init_freeze.json --schedule "hold:2500:10,ramp:2500:600:19" --schedule_dt_fs 1 --release \
    --relax_fmax 1.0 --relax_steps 300 --temperature 600 --equilib_ps 1 --prod_ps 1000 --dt_fs 2 --friction 0.02 --save_fs 100 \
    --seed $s --msd_elements Zr O Li --device cuda --stream_traj > $R/s$k.log 2>&1 &
  echo "[$(ts)] ▶ s$k (seed $s) PID $!"
  echo $! > $R/s$k.pid
  sleep 20
done
rc=0
for k in 1 2 3; do wait $(cat $R/s$k.pid); r=$?; echo "[$(ts)] s$k rc $r"; [ $r = 0 ] || rc=1; done
echo "[$(ts)] 끝 · rc $rc"
