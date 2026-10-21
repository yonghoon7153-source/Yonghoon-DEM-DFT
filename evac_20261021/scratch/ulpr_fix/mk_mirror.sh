#!/usr/bin/env bash
# Read-only mirror of the kit (+ the repo files the kit reads) at a commit of THIS worktree's repository — git archive → scratch.
# Usage: bash mk_mirror.sh <commit> <dest>
set -euo pipefail
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-aa282bca507003e72
C=${1:?commit}
D=${2:?dest}
rm -rf "$D"
mkdir -p "$D"
git -C "$WT" archive "$C" \
  docs/data/ps45_unload_20261009 \
  docs/data/ps73_compaction_curve_20261006/raw/ps73_logs.tgz \
  docs/reviews/dem_unloading_history_test_20261014/hist_20261014_094731.report.tgz \
  docs/reviews/codex_ps45_porosity_evidence_20261001/reference/dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts \
  scripts/plane_load_share.py | tar -x -C "$D"
echo "mirror $C -> $D"
( cd "$D/docs/data/ps45_unload_20261009" && sha256sum SHA256SUMS history_test/SHA256SUMS )
