#!/bin/bash
# usage: bash run.sh <out-prefix> <command...>   — stdout → <prefix>.out · stderr → <prefix>.err · rc · seconds → <prefix>.rc
# 작업 트리 = 호출한 곳 (cwd) · BLAS 한 스레드 · nice 19
out=$1; shift
s=$(date +%s)
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 nice -n 19 "$@" > "$out.out" 2> "$out.err"
rc=$?
e=$(date +%s)
echo "rc=$rc secs=$((e - s)) cwd=$(pwd) cmd=$*" > "$out.rc"
cat "$out.rc"
exit $rc
