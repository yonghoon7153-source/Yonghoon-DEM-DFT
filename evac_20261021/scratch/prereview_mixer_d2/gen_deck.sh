#!/bin/bash
# usage: gen_deck.sh <generator.py> <outdir> [generator args...]
# Runs the generator CLI (one BLAS thread, nice 19, python -I) writing into <outdir>; stdout/stderr -> <outdir>.log
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
gen="$1"; out="$2"; shift 2
mkdir -p "$(dirname "$out")"
nice -n 19 python3 -I -B "$gen" --out "$out" "$@" > "$out.log" 2>&1
echo "rc=$?"
