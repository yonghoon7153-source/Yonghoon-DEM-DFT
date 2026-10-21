#!/bin/bash
# Re-run the regressions that last ran before the run_contract underflow fix (one at a time).
Z3=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/z3
R="$Z3/run_one.sh"
rm -f "$Z3/final2.done"
bash "$R" f_verdict python3 scripts/test_ca_ext_verdict.py
bash "$R" f_labels python3 webapp/test_ca_ext_labels.py
bash "$R" f_cj python3 scripts/test_carbon_junction.py
bash "$R" f_s3self python3 scripts/step3_sigma.py --selftest
bash "$R" f_s3rint python3 scripts/step3_sigma.py --selftest-rint
bash "$R" f_z1 python3 scripts/test_ca_ext_z1.py
bash "$R" f_pfa python3 scripts/test_ptfe_face_alpha.py --old-scripts /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/s1/old/scripts
bash "$R" f_cmdself python3 scripts/check_method_discipline.py --selftest
echo done > "$Z3/final2.done"
