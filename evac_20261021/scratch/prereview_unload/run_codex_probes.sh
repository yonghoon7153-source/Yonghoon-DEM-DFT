#!/usr/bin/env bash
# Codex 탐침 (리포 반입본 사본) 을 주어진 폴더에서 차례로 돌린다 — nice 19 · BLAS 1 · python -I -X utf8 -B · 화면 = <폴더>/logs/<탐침>.log
# 사용: bash run_codex_probes.sh <폴더> [탐침 이름 …]
set -u
D=${1:?dir}
shift
mkdir -p "$D/logs" "$D/tmp"
export TMPDIR=$D/tmp OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$D" || exit 9
for p in "$@"; do
  args=()
  [ "$p" = grammar_provenance ] && args=(--run-id prereview1)
  t0=$(date +%s)
  nice -n 19 python3 -I -X utf8 -B "probes/$p.py" "${args[@]}" > "logs/$p.log" 2>&1
  rc=$?
  echo "$p rc=$rc secs=$(( $(date +%s) - t0 )) last=$(tail -1 "logs/$p.log" | cut -c1-200)"
done
