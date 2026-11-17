#!/usr/bin/env bash
W=/home/kgy/wt_hj_md0; R=/home/kgy/work/runs/hj_md0_1117
ts(){ date '+%m-%d %H:%M:%S'; }
echo "[$(ts)] DFT 시작 · commit $(git -C $W rev-parse --short HEAD)"
for spec in "bulk:9000" "bulk_k:16000" "iface:14000"; do
  sub=${spec%%:*}; mf=${spec#*:}
  echo "[$(ts)] ▶ $sub (MIN_FREE_MIB $mf)"
  MIN_FREE_MIB=$mf bash "$W/tools/doping/run_force_check_scf.sh" "$R/dft/$sub"; echo "[$(ts)] $sub 러너 rc $?"
done
echo "[$(ts)] 끝"
