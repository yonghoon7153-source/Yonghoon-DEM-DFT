#!/bin/bash
# PAI probe — -C on the real D2 pair (as received from ibb) and on the reconstructed D0.7 pair (make_d07_resume.py)
#   usage: bash c_real.sh <scratch dir holding d07/ from make_d07_resume.py>
WT=$(cd "$(dirname "$0")/../../../../.." && pwd)
SP=${1:?scratch}
T=$WT/scripts/resume_ckpt.sh
D2=$WT/docs/data/kg50_resume_tests_20261027/d2_main_1028_0942
D07=$WT/docs/data/kg50_decks_20261027_v3_b50/kg50_d07_b50
mkdir -p "$SP/w_d2" "$SP/w_d07"
echo "tool sha256 $(sha256sum < "$T" | cut -c1-64)"
bash "$T" -C "$D2/input_kg50_d2_b50.liggghts" "$D2/input_kg50_d2_b50_r4.liggghts" restart_kg50_d2_b50/restart_settling_20001.bin 20001 "$SP/w_d2"
echo "== D2 received pair rc=$?"
bash "$T" -C "$D07/input_kg50_d07_b50.liggghts" "$SP/d07/d07_tool_r56.liggghts" restart_kg50_d07_b50/restart_settling_20001.bin 20001 "$SP/w_d07"
echo "== D0.7 reconstructed pair rc=$?"
echo "files written into the -C work folders:"; ls -la "$SP/w_d2" "$SP/w_d07"
