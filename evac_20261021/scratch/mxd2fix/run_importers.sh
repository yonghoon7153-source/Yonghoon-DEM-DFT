#!/bin/bash
# Selftests of the scripts that import the changed mixer tools (run from the worktree root).
W=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a09115c89f930642a
S=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/mxd2fix
cd "$W" || exit 9
for t in check_contact_validity make_mixer_resume measure_mixing_index mixer_exact_frames mixer_gate_reader_diff mixer_restart_phase_test mixer_stage_gate; do
  t0=$(date +%s)
  python3 -B "scripts/$t.py" --selftest > "$S/imp_$t.log" 2>&1
  rc=$?
  echo "$t rc=$rc $(( $(date +%s) - t0 ))s | $(grep -E 'selftest|PASS|FAIL|통과|실패' "$S/imp_$t.log" | tail -n 1 | cut -c1-160)"
done
