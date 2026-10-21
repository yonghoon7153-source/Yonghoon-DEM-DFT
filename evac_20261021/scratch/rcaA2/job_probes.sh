#!/bin/bash
# pre-review probes rerun on the fixed tree (copies in rcaA2/probes · outputs there) + off-path bit identity vs a76f59d0d
D=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee
mkdir -p $D/probes/logs
cd $D/probes || exit 9
export PRE_REPO=$WT
for p in probe_gap_revisit probe_gap_revisit_prod probe_closed_loop probe_self_vs_distinct probe_ptfe_monotone probe_sdcp_relocate probe_sv_cf probe_k_boundary_prod probe_mut_cf; do
  python3 -I $p.py > logs/$p.log 2>&1; echo "rc=$?" >> logs/$p.log
done
python3 -I probe_stage2_gate.py $WT > logs/probe_stage2_gate.log 2>&1; echo "rc=$?" >> logs/probe_stage2_gate.log
rm -rf $D/probes/stage2_gate_repo
python3 $D/probe_off_bitid_a2.py > $D/logs/off_bitid.log 2>&1; echo "rc=$?" >> $D/logs/off_bitid.log
date > $D/logs/probes_done.txt
