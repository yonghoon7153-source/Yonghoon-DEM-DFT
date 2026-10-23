#!/bin/bash
# usage: r.sh <src_tree> <out_file> <python script> [args...]  (cwd = work folder)
W=${ATK_ROOT:?ATK_ROOT = 리뷰어 작업 폴더 (README)}
SRC=$1; OUT=$2; shift 2
export RINT_REVIEW_SOURCE=$SRC PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 ATK_ROOT=$W
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd $W
start=$(date +%s)
nice -n 19 python3 -I -B "$@" > "$OUT" 2>&1
rc=$?
echo "rc=$rc secs=$(( $(date +%s) - start ))"
