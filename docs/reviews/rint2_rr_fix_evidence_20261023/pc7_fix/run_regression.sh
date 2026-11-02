#!/usr/bin/env bash
# Rint ② PC7 고침 회귀 (11-02 · author 11-02 approved PC7 fix) — 사슬 전체 · 끝-끝 · kgy 판 (Python 3.8) 을 차례로 · 로그 = <로그 폴더>.
#   bash run_regression.sh <작업 트리> <로그 폴더>
# 메인 게이트 (scripts/check_all.sh) 가 도는 동안에는 돌리지 않는다 (같은 시험 · 자원) — 부르는 쪽이 먼저 확인한다.
set -uo pipefail
WT="$1"; LOG="$2"
mkdir -p "$LOG"
cd "$WT"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
echo "HEAD ${HEAD_SHA:-?} · $(python3 --version 2>&1) · $(date -u +%FT%TZ)" > "$LOG/regression_env.txt"
python3 scripts/test_rint_r_chain.py > "$LOG/full_after.log" 2>&1; echo "full rc=$?" >> "$LOG/regression_env.txt"
python3 scripts/test_rint_r_chain_e2e.py > "$LOG/e2e_after.log" 2>&1; echo "e2e rc=$?" >> "$LOG/regression_env.txt"
KGY_PY38_LOGDIR="$LOG/py38" bash scripts/check_kgy_py38.sh > "$LOG/py38_check.out" 2>&1; echo "py38 rc=$?" >> "$LOG/regression_env.txt"
echo "done $(date -u +%FT%TZ)" >> "$LOG/regression_env.txt"
