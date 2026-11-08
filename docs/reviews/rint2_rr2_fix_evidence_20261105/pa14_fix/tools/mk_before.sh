#!/bin/bash
# 고치기 전 뿌리 (사슬 = 바탕 379e85856 rint_r_chain.py · 시험 = 시험 먼저 판) — before_tree/scripts
set -eu
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/pa14fix
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a271b07eec3fe5332
mkdir -p "$H/test_first"
cp "$WT/scripts/test_rint_r_chain.py" "$H/test_first/test_rint_r_chain.py"
python3 "$H/tools/mktree.py" "$WT" "$H/before_tree" "$H/base/rint_r_chain.py" "$H/test_first/test_rint_r_chain.py"
sha256sum "$H/before_tree/scripts/rint_r_chain.py" "$H/before_tree/scripts/test_rint_r_chain.py"
