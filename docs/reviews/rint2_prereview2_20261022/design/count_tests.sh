#!/bin/bash
# Count PASS/FAIL of the test files cited by the ledger evidence_tests (RCA-01..13) at 93d93bc02.
# Run:  bash heavy.sh bash count_tests.sh <worktree> <outdir>
WT=$1
OUT=$2
mkdir -p "$OUT"
cd "$WT" || exit 1
for t in test_rint_r_chain.py test_ca_s0_census.py test_step3_conv_cert.py test_step3_target_cert.py test_carbon_junction.py \
         test_ca_ext_runner.py test_rint_r_chain_e2e.py test_ca_ext_b6.py; do
  s=$(date +%s)
  timeout 3000 python3 "scripts/$t" > "$OUT/$t.log" 2>&1
  rc=$?
  e=$(date +%s)
  echo "$t rc=$rc seconds=$((e - s)) tail: $(tail -n 2 "$OUT/$t.log" | tr '\n' ' ' | cut -c1-300)" >> "$OUT/summary.txt"
done
echo DONE >> "$OUT/summary.txt"
