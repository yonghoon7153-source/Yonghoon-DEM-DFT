#!/usr/bin/env bash
# dd_eval.m 배관 e2e — Octave 전사본 vs Python 전사본. 합성 데이터.
# 사용: ./run_e2e.sh <작업디렉터리>
set -u
T="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK="${1:-$(mktemp -d)}"
mkdir -p "$WORK"
python3 "$T/gen_synth_data.py" "$WORK" >/dev/null || exit 1
cd "$WORK" || exit 1

fail=0; n=0
for spec in \
  "data/half_cell/GITT/:Li:pristine"      "data/half_cell/GITT/:Li:300_0009" \
  "data/half_cell/GITT/:Kunz:200"         "data/half_cell/GITT/:Kunz:300_0147" \
  "data/half_cell/step_005C/:Li:pristine" "data/half_cell/step_005C/:Kunz:100" \
  "data/half_cell/step_005C/:Li:300_0147"
do
  IFS=: read -r hcd si st <<< "$spec"
  tag="$(echo "${hcd}_${si}_${st}" | tr '/' '_')"
  octave-cli --no-init-file --eval "
    addpath('$T/../dd_shims'); addpath('$T/oct_stubs'); addpath('$T/synth'); addpath('$T/..');
    dd_eval('HalfCellDir','$hcd','SiSource','$si','State','$st','Out','o_$tag.csv');
  " > "oct_$tag.log" 2>&1
  python3 "$T/mirror_dd_eval.py" --root . --half-cell-dir "$hcd" --si-source "$si" \
    --state "$st" --out "p_$tag.csv" > "py_$tag.log" 2>&1
  n=$((n+1))
  if [ ! -f "o_$tag.csv" ]; then
    echo "FAIL $spec  (Octave 쪽 산출 없음 — oct_$tag.log)"; fail=$((fail+1)); continue
  fi
  if out=$(python3 "$T/check_e2e.py" "o_$tag.csv" "p_$tag.csv" 2>&1); then
    echo "OK   $spec   ${out}"
  else
    echo "FAIL $spec"; echo "$out" | sed 's/^/       /'; fail=$((fail+1))
  fi
done
echo "----"
echo "$((n-fail))/$n 통과   (작업디렉터리 $WORK)"
[ "$fail" -eq 0 ]
