#!/bin/bash
# Q5 selftests (kg50_q5_branches · kg50_q5_verdict) from the worktree root — they call scripts/resume_ckpt.sh -C by relative path
W=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/f01r2
cd /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-ac3f433b81b4e211e || exit 1
export TMPDIR=$W/tmp
mkdir -p "$TMPDIR" "$W/logs"
for s in branches verdict; do
  nice -n 10 python3 scripts/kg50_q5_$s.py --selftest > "$W/logs/q5_${s}_selftest.log" 2>&1
  echo "$s rc=$? $(tail -1 "$W/logs/q5_${s}_selftest.log")"
done
