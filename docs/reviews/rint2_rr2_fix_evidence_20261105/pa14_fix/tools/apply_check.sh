#!/bin/bash
# code.diff 점검 — 바탕 (379e85856) 두 파일 사본 + code.diff (patch -p1) = 고친 판 바이트 (sha256 대조)
set -eu
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/pa14fix
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a271b07eec3fe5332
D=$H/applycheck
rm -rf "$D"
mkdir -p "$D/scripts"
cp "$H/base/rint_r_chain.py" "$H/base/test_rint_r_chain.py" "$D/scripts/"
cd "$D"
patch -p1 --quiet < "$WT/docs/reviews/rint2_rr2_fix_evidence_20261105/pa14_fix/code.diff"
sha256sum scripts/rint_r_chain.py scripts/test_rint_r_chain.py
cd "$WT"
sha256sum scripts/rint_r_chain.py scripts/test_rint_r_chain.py
cmp "$D/scripts/rint_r_chain.py" "$WT/scripts/rint_r_chain.py" && cmp "$D/scripts/test_rint_r_chain.py" "$WT/scripts/test_rint_r_chain.py" && echo "바탕 + code.diff = 고친 판 바이트 같음"
