#!/bin/bash
# usage: run_selftest.sh <generator.py> <out.txt>
# Runs a generator's --selftest with one BLAS thread at lowest priority; prints rc and elapsed seconds.
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
gen="$1"; out="$2"
t0=$(date +%s.%N)
nice -n 19 python3 -I -B "$gen" --selftest > "$out" 2>&1
rc=$?
t1=$(date +%s.%N)
echo "rc=$rc elapsed=$(python3 -c "print(round($t1-$t0,1))")s"
tail -2 "$out"
