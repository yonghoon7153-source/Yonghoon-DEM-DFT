#!/usr/bin/env bash
set -uo pipefail
W=/home/kgy/wt_hj_md0; R=/home/kgy/work/runs/hj_md0_1117; PY=/home/kgy/apps/miniforge3/envs/uma/bin/python; S=$W/db/structures
ts(){ date '+%m-%d %H:%M:%S'; }
echo "[$(ts)] 시작 · commit $(cat $R/SOURCE_COMMIT)"
echo "[$(ts)] ① 벌크 B144 — 600 K · 평형 1 ps + 생산 5 ps"
"$PY" -u "$W/tools/oxidation/run_li_interface_md.py" --interface "$S/hyeokju_Li2ZrO3_sc144_mp-aaaaagdw.vasp" --label bulk_B144 --out_dir "$R/bulk" --temperature 600 --equilib_ps 1 --prod_ps 5 --dt_fs 2 --friction 0.02 --save_fs 100 --relax_steps 0 --fix_bottom 0 --seed 20261117 --device cuda || { echo "[$(ts)] ⛔ 벌크 실패"; exit 3; }
echo "[$(ts)] ② 계면 I142 — LPSCl 고정 · 2500 K 10 ps → 600 K 19 ps → 풀고 600 K 평형 1 + 생산 5 ps"
"$PY" -u "$W/tools/oxidation/run_li_interface_md.py" --interface "$S/hyeokju_md0_2026_11_17/I142_liouter_aLZO16_init.xyz" --label interface_I142 --out_dir "$R/interface" --freeze_idx "$S/hyeokju_md0_2026_11_17/I142_liouter_aLZO16_init_freeze.json" --schedule "hold:2500:10,ramp:2500:600:19" --schedule_dt_fs 1 --release --relax_fmax 1.0 --relax_steps 300 --temperature 600 --equilib_ps 1 --prod_ps 5 --dt_fs 2 --friction 0.02 --save_fs 100 --seed 20261117 --msd_elements Zr O Li --device cuda || { echo "[$(ts)] ⛔ 계면 실패"; exit 4; }
echo "[$(ts)] 끝"
