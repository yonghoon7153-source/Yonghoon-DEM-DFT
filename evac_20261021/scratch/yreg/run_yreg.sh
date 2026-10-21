#!/bin/bash
# merged main (X + Y + Y2) cross-check before the gate
cd /home/user/Yonghoon-DEM-DFT || exit 9
D=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/yreg
echo "HEAD $(git rev-parse --short HEAD) dirty=$(git status --porcelain | wc -l)"
run() { local name="$1"; shift; local t0=$(date +%s); timeout 3600 "$@" > $D/$name.log 2>&1; local rc=$?; echo "$name rc=$rc t=$(( $(date +%s)-t0 ))s :: $(tail -n 2 $D/$name.log | tr '\n' ' ' | cut -c1-200)"; }
run b6 python3 -B scripts/test_ca_ext_b6.py
run runner python3 -B scripts/test_ca_ext_runner.py
run verdict python3 -B scripts/test_ca_ext_verdict.py
run labels python3 -B webapp/test_ca_ext_labels.py
run cjunc python3 -B scripts/test_carbon_junction.py
run s0 python3 -B scripts/test_ca_s0_census.py
run ptfe_old python3 -B scripts/test_ptfe_face_alpha.py --old-scripts /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/s1/old/scripts
echo DONE
