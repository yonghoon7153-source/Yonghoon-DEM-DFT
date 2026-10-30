#!/bin/bash
# PAI probe — the current cutter (deckcheck --cut-trial · heredoc lines 64–1566 of 2dc7f693) on the D2 r4 deck as received:
#   output must be byte-identical to the received r4t (Codex §5 checked this on 77c24237) · then the D0.7 r56t from the
#   reconstructed D0.7 deck (make_d07_resume.py) and its run budget (--trial-steps).
#   usage: bash cut_d2.sh <scratch with d07/>
WT=$(cd "$(dirname "$0")/../../../../.." && pwd)
SP=${1:?scratch}
D2=$WT/docs/data/kg50_resume_tests_20261027/d2_main_1028_0942
sed -n '64,1566p' "$WT/scripts/resume_ckpt.sh" > "$SP/deckcheck_2dc7.py"
head -c 0 /dev/null
python3 "$SP/deckcheck_2dc7.py" --cut-trial "$D2/input_kg50_d2_b50_r4.liggghts" 2000 "$SP/d2_r4t_regen.liggghts"; echo "cut rc=$?"
cmp "$SP/d2_r4t_regen.liggghts" "$D2/input_kg50_d2_b50_r4t.liggghts" && echo "D2 r4t regenerated == received (byte-identical)"
sha256sum "$SP/d2_r4t_regen.liggghts" "$D2/input_kg50_d2_b50_r4t.liggghts" | cut -c1-16
python3 "$SP/deckcheck_2dc7.py" --cut-trial "$SP/d07/d07_tool_r56.liggghts" 2000 "$SP/d07_r56t.liggghts"; echo "cut rc=$?"
python3 "$SP/deckcheck_2dc7.py" --trial-steps "$SP/d07_r56t.liggghts"; echo "trial-steps rc=$?"
wc -l "$SP/d07_r56t.liggghts" "$D2/input_kg50_d2_b50_r4t.liggghts"
tail -1 "$SP/d07_r56t.liggghts"
