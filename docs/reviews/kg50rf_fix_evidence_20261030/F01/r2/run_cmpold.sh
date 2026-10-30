#!/bin/bash
# --compare-old against the base tool (77c24237 = bf8cf21c6) and F02 1 판 (5f4ffb46 = 2107f144f) — Python 3.11 · mawk · from the worktree root
W=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/f01r2
cd /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-ac3f433b81b4e211e || exit 1
export TMPDIR=$W/tmp
for t in base_77c24237 f02r1_5f4ffb46; do
  nice -n 10 python3 -I scripts/test_resume_ckpt.py --compare-old "$W/old/tool_$t.sh" > "$W/logs/compare_old_$t.log" 2>&1
  echo "$t rc=$? $(grep -E '^[0-9]+ PASS' "$W/logs/compare_old_$t.log" | tail -1) · ENOSPC $(grep -cE 'No space left|Errno 28' "$W/logs/compare_old_$t.log")"
done
echo DONE
