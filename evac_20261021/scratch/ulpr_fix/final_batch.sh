#!/usr/bin/env bash
# Final verification on a mirror of the review pin: all kit suites · pre-review probes · mutation run.
# Usage: bash final_batch.sh <commit>
set -u
S=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/ulpr_fix
C=${1:?commit}
M=$S/m_pin
EV=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-aa282bca507003e72/docs/reviews/dem_unloading_kit_prereview_fix_evidence_20261021
bash $S/mk_mirror.sh "$C" "$M"
echo "== suites"
bash $S/run_mirror.sh "$M" pin ul_lib ul_s3 ul_observers ul_gates ul_reader seal_selftest seal_check decks_selftest decks_check hist_decks_selftest hist_decks_check hist_read_selftest ul_runner_test
echo "== pre-review probes"
mkdir -p $S/results_pin
export TMPDIR=$S/tmp OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
( cd $S && python3 -I -B $EV/probe_resume_unfinished.py $M/docs/data/ps45_unload_20261009 $S/results_pin/pre_ul01_final.json > $S/results_pin/pre_ul01_final.log 2>&1; echo "probe_resume_unfinished rc=$?"; tail -3 $S/results_pin/pre_ul01_final.log )
( cd $S && python3 -I -B $EV/probe_misc.py $M/docs/data/ps45_unload_20261009 $S/results_pin/probe_misc_final.json > $S/results_pin/probe_misc_final.log 2>&1; echo "probe_misc rc=$?"; tail -3 $S/results_pin/probe_misc_final.log )
echo "== mutations"
python3 -I -B $S/mutate.py "$M" $S/mut_work_pin $S/results_pin/mutations_final.json
echo "== seal hashes"
( cd $M/docs/data/ps45_unload_20261009 && sha256sum SHA256SUMS active_rules.json ul_reader.py ul_gates.py seal_kit.py history_test/SHA256SUMS history_test/read_history.py history_test/history_params.json unload_params.json )
