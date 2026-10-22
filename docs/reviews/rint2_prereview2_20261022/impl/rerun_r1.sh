#!/bin/bash
# 1 회차 탐침 재실행 (93d93bc02) — 출력 JSON 은 이 폴더
cd "$(dirname "$0")"
export PRE_REPO=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a388f740a6ce4524d
LIST="${*:-probe_gap_revisit probe_gap_revisit_prod probe_self_vs_distinct probe_ptfe_monotone probe_sdcp_relocate probe_sv_cf probe_k_boundary probe_k_boundary_prod probe_closed_loop probe_zero_binding probe_mut_cf}"
for p in $LIST; do
  echo "=== $p"; s=$(date +%s)
  timeout 900 python3 -I "$p.py" 2>&1 | tail -40
  echo "rc=${PIPESTATUS[0]} t=$(( $(date +%s) - s ))s"
done
