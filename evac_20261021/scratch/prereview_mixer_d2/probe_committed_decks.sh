#!/bin/bash
# recheck 10-21: fixed readback / deck diff on the COMMITTED DEV decks (default path consumers — no false refusal?)
W=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a876633abb3bfa519
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2
V=$W/docs/data/mixer_highbo_dev_decks_20260930_v26/decks
U=$W/docs/data/mixer_highbo_dev_decks_20261005_u/decks
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1
cd "$H" || exit 9
python3 -I -B "$W/scripts/mixer_deck_readback.py" \
  --table U "$V/LC_ref_r2_s32452843/in.mixer" "$U/LU212_ref_r2_s32452843/in.mixer" \
  --table U "$V/LC_ref_r2_s32452843/in.mixer" "$U/LU637_ref_r2_s32452843/in.mixer" \
  --table U "$U/LU212_ref_r2_s32452843/in.mixer" "$U/LU637_ref_r2_s32452843/in.mixer" \
  --table B "$V/LC_ref_r2_s32452843/in.mixer" "$V/LH_ref_r2_s32452843/in.mixer" \
  --table E0 "$V/E0_ref_s32452843/in.mixer" "$V/E0_ref2_s32452843/in.mixer" \
  --table DT "$V/E0_ref_s32452843/in.mixer" "$V/E0_ref_dthalf_s32452843/in.mixer" > "$H/committed_readback.out" 2>&1
echo "readback rc=$?"; grep -E "^── 표|표 PASS|⛔" "$H/committed_readback.out" | head -12
python3 -I -B "$W/scripts/mixer_deck_diff.py" "$V/LC_ref_r2_s32452843/in.mixer" "$V/LH_ref_r2_s32452843/in.mixer" --allow B > "$H/committed_diff_B.out" 2>&1
echo "diff B rc=$? :: $(tail -1 "$H/committed_diff_B.out")"
python3 -I -B "$W/scripts/mixer_deck_diff.py" "$V/LC_ref_r2_s32452843/in.mixer" "$U/LU637_ref_r2_s32452843/in.mixer" --allow U > "$H/committed_diff_U.out" 2>&1
echo "diff U rc=$? :: $(tail -1 "$H/committed_diff_U.out")"
python3 -I -B "$W/scripts/mixer_deck_diff.py" --runs "$V" --cohort dev-e0 > "$H/committed_cohort_e0.out" 2>&1
echo "diff --cohort dev-e0 rc=$? :: $(tail -1 "$H/committed_cohort_e0.out")"
python3 -I -B "$W/scripts/mixer_deck_diff.py" --runs "$V" --cohort dev-rot > "$H/committed_cohort_rot.out" 2>&1
echo "diff --cohort dev-rot rc=$? :: $(tail -1 "$H/committed_cohort_rot.out")"
