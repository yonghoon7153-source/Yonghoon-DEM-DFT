#!/bin/bash
# B 묶음 (끔 비트 동일) — 새 판 (93d93bc02 작업 트리) ↔ 기반 a76f59d0d scripts 사본
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a388f740a6ce4524d
D=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview2_impl
cd "$WT" || exit 9
python3 -I scripts/test_ca_ext_b6.py --only "${1:-B}" --old-scripts "$D/base_a76/scripts" ${2:+$2}
