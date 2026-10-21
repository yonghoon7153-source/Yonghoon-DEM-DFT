#!/usr/bin/env bash
# Run the Codex probes one after another in <dir> — python3 -I -X utf8 -B · BLAS 1 thread · screen = <dir>/logs/<probe>.log
# Usage: bash run_codex_probes.sh <dir> <probe ...>
set -u
D=${1:?dir}
shift
mkdir -p "$D/logs" "$D/tmp"
export TMPDIR=$D/tmp OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$D" || exit 9
for p in "$@"; do
  args=()
  case "$p" in grammar_provenance) args=(--run-id ulprfix_orig) ;; grammar_provenance_kitreader) args=(--run-id ulprfix_kitreader) ;; esac
  t0=$(date +%s)
  python3 -I -X utf8 -B "probes/$p.py" "${args[@]}" > "logs/$p.log" 2>&1
  rc=$?
  echo "$p rc=$rc secs=$(( $(date +%s) - t0 )) last=$(tail -1 "logs/$p.log" | cut -c1-240)"
done
