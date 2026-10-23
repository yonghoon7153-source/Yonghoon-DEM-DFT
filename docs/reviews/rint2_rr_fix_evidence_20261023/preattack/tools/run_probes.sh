#!/bin/bash
# usage: run_probes.sh <src_dir> <ev_dir> <tag>
SRC=$1; EV=$2; TAG=$3; LOG=${ATK_ROOT:?}/logs  # 리포 사본에서 바꾼 줄
export RINT_REVIEW_SOURCE=$SRC PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd $EV
for p in registration/probe_registration_current.py certificate/probe_certificate.py geometry/run_review.py; do
  n=$(basename $p .py)
  /usr/bin/time -v python3 -X importtime -c 1 >/dev/null 2>&1
  start=$(date +%s)
  python3 $p > $LOG/${TAG}_${n}.out 2> $LOG/${TAG}_${n}.err
  echo "$TAG $p rc=$? secs=$(( $(date +%s) - start ))" >> $LOG/${TAG}_summary.txt
done
