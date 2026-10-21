#!/usr/bin/env bash
# 읽기 전용 — 커밋별 파일 sha256 (리포 작업 트리 = 이 에이전트 worktree · git show 만)
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a93377624c009ba18
K=docs/data/ps45_unload_20261009
cd "$WT" || exit 9
for c in "$@"; do
  rh=$(git -C "$WT" show "$c:$K/history_test/read_history.py" 2>/dev/null | sha256sum | cut -c1-16)
  hp=$(git -C "$WT" show "$c:$K/history_test/history_params.json" 2>/dev/null | sha256sum | cut -c1-16)
  hs=$(git -C "$WT" show "$c:$K/history_test/SHA256SUMS" 2>/dev/null | sha256sum | cut -c1-16)
  ks=$(git -C "$WT" show "$c:$K/SHA256SUMS" 2>/dev/null | sha256sum | cut -c1-16)
  gd=$(git -C "$WT" show "$c:$K/history_test/in.hist_grammar.liggghts" 2>/dev/null | sha256sum | cut -c1-16)
  pd=$(git -C "$WT" show "$c:$K/history_test/in.hist_producer.liggghts" 2>/dev/null | sha256sum | cut -c1-16)
  st=$(git -C "$WT" show "$c:$K/history_test/plate_hist.stl" 2>/dev/null | sha256sum | cut -c1-16)
  kt=$(git -C "$WT" rev-parse "$c:$K" 2>/dev/null | cut -c1-12)
  echo "$c kit_tree=$kt read_history=$rh params=$hp hist_SUMS=$hs kit_SUMS=$ks gram_deck=$gd prod_deck=$pd stl=$st"
done
