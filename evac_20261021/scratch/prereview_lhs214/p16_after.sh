#!/bin/bash
# P16 — p07b (변이 × 문서 짝) → p13 (묶음 §4 단계 1 · 3 · 4 · 이 컨테이너 범위) → p14 (회귀 · 단계 2 자체 시험 다섯) 를 한 자리에서 차례로
# 재실행: cd <worktree> && bash <SCRATCH>/heavy.sh bash p16_after.sh <worktree> <SCRATCH>/prereview_lhs214
WT=$1; D=$2
cd "$WT" || exit 9
echo "== p07b $(date +%T)"
python3 -I -B "$D/p07b_combos.py" "$WT" "$D/p07b_combos.json"
echo "== p13 $(date +%T) dirty=$(git status --porcelain --untracked-files=no | wc -l)"
bash "$D/p13_preflight.sh" "$D/p13_out" > "$D/p13.log" 2>&1; echo "p13 rc=$?"
echo "== p14 $(date +%T) dirty=$(git status --porcelain --untracked-files=no | wc -l)"
bash "$D/p14_regress.sh" "$D/p14_out" > "$D/p14.log" 2>&1; echo "p14 rc=$?"
echo "== end $(date +%T) dirty=$(git status --porcelain --untracked-files=no | wc -l)"
