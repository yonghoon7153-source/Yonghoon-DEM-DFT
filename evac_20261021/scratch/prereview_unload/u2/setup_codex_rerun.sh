#!/usr/bin/env bash
# U2 — Codex 수정 재확인 탐침 (10-15 증거 probes/ · support/) 을 주어진 커밋의 키트로 다시 돌릴 폴더 (scratch · 리포에 쓰지 않는다)
# 사전 리뷰 변형 둘 (10-21 증거 probes/) 도 같은 probes/ 에 둔다.
# 사용: bash setup_codex_rerun.sh <commit> <dest>
set -euo pipefail
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a948397637bfe9a76
C=${1:?commit}
D=${2:?dest}
EV=docs/reviews/codex_dem_unloading_kit_fix_recheck_evidence_20261015
EV2=docs/reviews/dem_unloading_kit_prereview_fix_evidence_20261021
rm -rf "$D"
mkdir -p "$D/src_tree" "$D/evidence"
git -C "$WT" archive "$C" "$EV/probes" "$EV/support" | tar -x -C "$D"
git -C "$WT" archive bbc2adefe "$EV2/probes" | tar -x -C "$D"   # 사전 리뷰 변형 둘 = 문서 커밋에서 반입 (핀 뒤 · 키트 무관)
mv "$D/$EV/probes" "$D/probes"
mv "$D/$EV/support" "$D/support"
cp "$D/$EV2/probes/"*.py "$D/probes/"
rm -rf "$D/docs"
git -C "$WT" archive "$C" \
  docs/data/ps45_unload_20261009 \
  docs/data/ps73_compaction_curve_20261006/raw/ps73_logs.tgz \
  docs/reviews/dem_unloading_history_test_20261014 \
  docs/reviews/codex_ps45_porosity_evidence_20261001/reference/dem_scripts/ps_sweep_6mah_20260914/in.ps_7_3_r45.liggghts \
  scripts/plane_load_share.py | tar -x -C "$D/src_tree"
mv "$D/src_tree" "$D/source"
ls "$D" "$D/probes"
( cd "$D/source/docs/data/ps45_unload_20261009" && sha256sum SHA256SUMS history_test/SHA256SUMS )
