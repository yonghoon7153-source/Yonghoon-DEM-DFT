#!/bin/bash
# run_legs.sh <leg...> — P2 다리를 순서대로 한 번씩. 각 다리 앞에서 디스크 (≥ 2 GB) · 시계 (23:24:56Z 상한) 를 본다.
# 다리가 rc≠0 이면 그 자리에서 멈춘다 (재실행 없음 — 시도 1 회).
S=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad
cd $S/p2/degradation-degeneracy || exit 9
G=results/_smoke/p2/grid_22p_seed_101
COMMON=(--in $G --objective pocv_dvdq,pocv_dvdq_dqdv --n-restarts 5 --nproc 4)
HC=(--reference halfcell)
DEADLINE=$(date -u -d 2026-10-06T23:24:56Z +%s)
for leg in "$@"; do
  free=$(df -B1 --output=avail . | tail -1)
  now=$(date -u +%s)
  echo "$(date -u +%FT%TZ) pre $leg disk_free=$free left_s=$((DEADLINE-now))" >> $S/p2run/legs_progress.txt
  [ "$free" -ge 2000000000 ] || { echo "STOP disk $free" >> $S/p2run/legs_progress.txt; exit 3; }
  [ "$now" -lt "$DEADLINE" ] || { echo "STOP time" >> $S/p2run/legs_progress.txt; exit 4; }
  case $leg in
    L0) A=("${COMMON[@]}" --out results/_smoke/p2/fit_L0_grid) ;;
    L1) A=("${COMMON[@]}" "${HC[@]}" --out results/_smoke/p2/fit_L1_ocp) ;;
    L2) A=("${COMMON[@]}" "${HC[@]}" --halfcell-method ocpbias --halfcell-arg pe_offset_mv=5 --out results/_smoke/p2/fit_L2_u5) ;;
    L3) A=("${COMMON[@]}" "${HC[@]}" --halfcell-method ocpbias --halfcell-arg pe_offset_mv=10 --out results/_smoke/p2/fit_L3_u10) ;;
    L4) A=("${COMMON[@]}" "${HC[@]}" --halfcell-method ocpbias --halfcell-arg pe_offset_mv=5 --halfcell-arg pe_tilt_mv=10 --out results/_smoke/p2/fit_L4_t5) ;;
    L5) A=("${COMMON[@]}" "${HC[@]}" --halfcell-method ocpbias --halfcell-arg pe_offset_mv=10 --halfcell-arg pe_tilt_mv=20 --out results/_smoke/p2/fit_L5_t10) ;;
    L6) A=("${COMMON[@]}" "${HC[@]}" --halfcell-method ocpbias --halfcell-arg pe_tilt_mv=10 --out results/_smoke/p2/fit_L6_tilt10) ;;
    *) echo "unknown $leg"; exit 8 ;;
  esac
  $S/p2run/rl.sh 2${leg#L}_fit_$leg 3600 ./run.sh --mode fit "${A[@]}" || { echo "STOP $leg rc=$?" >> $S/p2run/legs_progress.txt; exit 5; }
  echo "$(date -u +%FT%TZ) done $leg" >> $S/p2run/legs_progress.txt
done
echo "ALL_DONE $*" >> $S/p2run/legs_progress.txt
