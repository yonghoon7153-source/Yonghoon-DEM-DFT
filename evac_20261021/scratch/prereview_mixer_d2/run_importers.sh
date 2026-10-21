#!/bin/bash
# recheck 10-21: selftests of the tools that import make_mixer_deck / mixer_deck_diff (now also mixer_deck_readback) at 9412f384a
W=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a876633abb3bfa519
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2
L="$H/selftests_importers"
mkdir -p "$L" "$H/tmp_launcher"
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 TMPDIR="$H/tmp_launcher"
cd "$H" || exit 9
for t in check_contact_validity make_mixer_resume measure_mixing_index mixer_exact_frames mixer_gate_reader_diff mixer_restart_phase_test mixer_stage_gate; do
  s=$(date +%s)
  python3 -I -B "$W/scripts/$t.py" --selftest > "$L/$t.log" 2>&1
  rc=$?
  e=$(date +%s)
  np=$(grep -c "PASS\|✓" "$L/$t.log")
  nf=$(grep -c "^  FAIL\|  ✗\|^FAIL" "$L/$t.log")
  echo "$t rc=$rc $((e - s))s pass_lines=$np fail_lines=$nf :: $(tail -1 "$L/$t.log" | cut -c1-160)"
done
