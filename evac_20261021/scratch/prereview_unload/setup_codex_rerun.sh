#!/usr/bin/env bash
# Codex 수정 재확인 탐침을 리뷰 핀 (92e6cda4d) 의 키트로 다시 돌릴 폴더 (scratch · 리포에 쓰지 않는다)
# 사용: bash setup_codex_rerun.sh <commit> <dest>
set -euo pipefail
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a93377624c009ba18
C=${1:?commit}
D=${2:?dest}
EV=docs/reviews/codex_dem_unloading_kit_fix_recheck_evidence_20261015
rm -rf "$D"
mkdir -p "$D/source" "$D/evidence"
git -C "$WT" archive "$C" "$EV/probes" "$EV/support" | tar -x -C "$D"
mv "$D/$EV/probes" "$D/probes"
mv "$D/$EV/support" "$D/support"
rm -rf "$D/docs"
git -C "$WT" archive "$C" \
  docs/data/ps45_unload_20261009 \
  docs/data/ps73_compaction_curve_20261006/raw/ps73_logs.tgz \
  docs/reviews/dem_unloading_history_test_20261014 \
  docs/reviews/codex_ps45_porosity_evidence_20261001/reference/dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts \
  scripts/plane_load_share.py | tar -x -C "$D/source"
ls "$D" "$D/probes" "$D/source/docs/data/ps45_unload_20261009" | head -40
