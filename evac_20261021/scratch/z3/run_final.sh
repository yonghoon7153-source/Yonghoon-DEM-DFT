#!/bin/bash
# Final regression re-run after the run_contract underflow fix (one at a time, nice 19).
Z3=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/z3
R="$Z3/run_one.sh"
rm -f "$Z3/final.done"
bash "$R" f_rcself python3 scripts/run_contract.py --selftest
bash "$R" f_runner python3 scripts/test_ca_ext_runner.py --old-runner "$Z3/base/scripts/sdcp_gain_vox015_8arm.sh"
bash "$R" f_b6 python3 scripts/test_ca_ext_b6.py --old-scripts "$Z3/base/scripts"
bash "$R" f_e2e python3 scripts/test_rint_r_chain_e2e.py
bash "$R" f_cmd python3 scripts/check_method_discipline.py
echo done > "$Z3/final.done"
