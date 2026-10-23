#!/bin/bash
# usage: py.sh <src_tree> <out_file> <python script> [args...]   (cwd = scratch atk1023)
A=${ATK_ROOT:?}  # 리뷰어 작업 폴더 — 리포 사본에서 바꾼 줄
SRC=$1; OUT=$2; shift 2
export RINT_REVIEW_SOURCE=$SRC PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
cd $A
nice -n 19 python3 -I -B "$@" > "$OUT" 2>&1
echo "rc=$?"
