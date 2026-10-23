#!/bin/bash
# Codex rereview probes, unchanged, on the fixed tree (a32fcf32f copy) — outputs into work logs/
W=${ATK_ROOT:?ATK_ROOT = 리뷰어 작업 폴더 (README)}
export ATK_ROOT=$W RINT_REVIEW_SOURCE=$W/new_src PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd $W/ev_new
for p in registration/probe_registration_current.py certificate/probe_certificate.py geometry/run_review.py; do
  n=$(basename $p .py)
  start=$(date +%s)
  nice -n 19 python3 $p > $W/logs/r2_${n}.out 2> $W/logs/r2_${n}.err
  echo "r2 $p rc=$? secs=$(( $(date +%s) - start ))" >> $W/logs/r2_summary.txt
done
cd $W
nice -n 19 python3 -I -B $W/tools_r1/reg_each.py $W/ev_new > $W/logs/r2_reg_each.json 2>&1
echo "reg_each rc=$?" >> $W/logs/r2_summary.txt
