#!/usr/bin/env bash
# U2 탐침 실행 — nice 19 · BLAS 한 스레드 · TMPDIR = scratch · python -I -B (리포에 쓰지 않는다)
# 사용: bash run_probe.sh <탐침.py> [인자 ...]
set -u
HERE=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_unload/u2
mkdir -p "$HERE/tmp" "$HERE/out"
export TMPDIR=$HERE/tmp OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$HERE" || exit 9
nice -n 19 python3 -I -B "$@"
