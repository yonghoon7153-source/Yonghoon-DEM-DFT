#!/usr/bin/env bash
# U2 읽기 전용 거울 — 주어진 커밋의 키트 + 키트가 리포에서 읽는 파일만 (git archive → scratch) · 리포에 쓰지 않는다
# 사용: bash mk_mirror.sh <commit> <dest>   (작업 트리 = U2 격리 작업 트리)
set -euo pipefail
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a948397637bfe9a76
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
