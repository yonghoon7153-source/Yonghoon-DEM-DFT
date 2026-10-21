#!/usr/bin/env bash
# U2 — Codex 탐침 둘째 차례 (receipt_ids_recheck 는 history_actual 의 evidence/history_reread* 를 읽는다 → 그 뒤에) · kitreader 는 다른 run-id
set -u
D=${1:?dir}
mkdir -p "$D/logs" "$D/tmp"
export TMPDIR=$D/tmp OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$D" || exit 9
for spec in "receipt_ids_recheck:" "receipt_ids_recheck_q4tolerant:" "grammar_provenance_kitreader:--run-id u2k"; do
  p=${spec%%:*}; a=${spec#*:}
  t0=$(date +%s)
  # shellcheck disable=SC2086
  nice -n 19 python3 -I -X utf8 -B "probes/$p.py" $a > "logs/$p.log" 2>&1
  rc=$?
  echo "$p rc=$rc secs=$(( $(date +%s) - t0 )) last=$(tail -1 "logs/$p.log" | cut -c1-200)"
done
