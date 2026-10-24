#!/usr/bin/env bash
# Run R-path tests under the py3.8 venv on a given tree (unpatched or patched).  Usage: py38_runall.sh TREE OUTDIR
TREE=$1; OUT=$2; B=${PY38_BIN:?PY38_BIN = python3.8 가 든 bin 폴더 (numpy 1.24.4 · scipy 1.10.1 설치)}; PY=$B/python3.8; export PATH=$B:$PATH; unset VIRTUAL_ENV
mkdir -p "$OUT"; cd "$TREE"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
run() { local name=$1; shift; local t0=$(date +%s); timeout 2400 nice -n 19 "$PY" "$@" > "$OUT/$name.log" 2>&1; local rc=$?; echo "$name rc=$rc $(( $(date +%s) - t0 ))s :: $(tail -1 "$OUT/$name.log" | cut -c1-160)" >> "$OUT/summary.txt"; }
: > "$OUT/summary.txt"
run run_contract scripts/run_contract.py --selftest
run step3_rint scripts/step3_sigma.py --selftest-rint
run ptfe_face_alpha scripts/test_ptfe_face_alpha.py
run carbon_junction scripts/test_carbon_junction.py
run ca_ext_b6 scripts/test_ca_ext_b6.py
run ca_ext_runner scripts/test_ca_ext_runner.py
run rint_r_chain scripts/test_rint_r_chain.py
run rint_r_chain_e2e scripts/test_rint_r_chain_e2e.py
run step3_target_cert scripts/test_step3_target_cert.py
run step3_conv_cert scripts/test_step3_conv_cert.py
run ca_s0_census scripts/test_ca_s0_census.py
echo DONE >> "$OUT/summary.txt"
