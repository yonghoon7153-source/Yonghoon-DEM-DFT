#!/usr/bin/env bash
# Codex re-check probes (repo copy, docs/reviews/codex_dem_unloading_kit_fix_recheck_evidence_20261015/) against a commit of THIS worktree —
# folder layout the probes expect: <D>/probes · <D>/support · <D>/source/<repo paths> · <D>/evidence.  Plus the pre-review variants (U).
# Usage: bash setup_codex_rerun.sh <commit> <dest>
set -euo pipefail
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-aa282bca507003e72
U=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_unload/codex_rerun_pin/probes
C=${1:?commit}
D=${2:?dest}
EV=docs/reviews/codex_dem_unloading_kit_fix_recheck_evidence_20261015
rm -rf "$D"
mkdir -p "$D/source" "$D/evidence"
git -C "$WT" archive "$C" "$EV/probes" "$EV/support" | tar -x -C "$D"
mv "$D/$EV/probes" "$D/probes"
mv "$D/$EV/support" "$D/support"
rm -rf "$D/docs"
cp "$U/grammar_provenance_kitreader.py" "$U/receipt_ids_recheck_q4tolerant.py" "$D/probes/"
git -C "$WT" archive "$C" \
  docs/data/ps45_unload_20261009 \
  docs/data/ps73_compaction_curve_20261006/raw/ps73_logs.tgz \
  docs/reviews/dem_unloading_history_test_20261014 \
  docs/reviews/codex_ps45_porosity_evidence_20261001/reference/dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts \
  scripts/plane_load_share.py | tar -x -C "$D/source"
( cd "$D/probes" && diff grammar_provenance.py grammar_provenance_kitreader.py ; diff receipt_ids_recheck.py receipt_ids_recheck_q4tolerant.py ) | grep -c '^[<>]' || true
( cd "$D/source/docs/data/ps45_unload_20261009" && sha256sum SHA256SUMS history_test/SHA256SUMS )
