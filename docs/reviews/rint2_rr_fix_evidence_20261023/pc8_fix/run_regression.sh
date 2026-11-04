#!/usr/bin/env bash
# Rint ② PC8 고침 회귀 (11-04 · 1저자 11-04 "다 권고대로") — 묶음을 하나씩 차례로 · Python 3.11 (기본 python3) 뒤 kgy 판 3.8.20 · 로그 = <로그 폴더>/<판>/.
#   bash run_regression.sh <작업 트리> <로그 폴더> <HEAD sha> [py311|py38|both]
# 메인 게이트 (scripts/check_all.sh) 와 같은 시험 · 자원 — 부르는 쪽이 먼저 확인한다 · 묶음 = 사슬 · 끝-끝 · 탄소 접합 · ca_ext (b6 · runner · z3) · 목표 증서.
set -uo pipefail
WT="$1"; LOG="$2"; HEAD_SHA="$3"; WHICH="${4:-both}"
PY38_BIN=/root/.local/share/uv/python/cpython-3.8.20-linux-x86_64-gnu/bin
mkdir -p "$LOG"
cd "$WT"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
SUITES="${SUITES:-test_rint_r_chain test_rint_r_chain_e2e test_carbon_junction test_ca_ext_b6 test_ca_ext_runner test_ca_ext_z3 test_step3_target_cert}"
SUFFIX="${SUFFIX:-}"                                       # 같은 판을 다시 돌릴 때 로그 폴더 꼬리 (예 _r2)
run_set() {
  local tag=$1$SUFFIX
  mkdir -p "$LOG/$tag"
  echo "[$tag] HEAD ${HEAD_SHA} · $(python3 --version 2>&1) · $(python3 -c 'import numpy, scipy; print("numpy", numpy.__version__, "scipy", scipy.__version__)' 2>&1) · $(date -u +%FT%TZ)" >> "$LOG/regression_env.txt"
  for s in $SUITES; do
    local t0; t0=$(date +%s)
    python3 "scripts/$s.py" > "$LOG/$tag/$s.log" 2>&1
    local rc=$?
    echo "[$tag] $s rc=$rc $(( $(date +%s) - t0 )) s · $(tail -1 "$LOG/$tag/$s.log" | cut -c1-140)" >> "$LOG/regression_env.txt"
  done
}
if [ "$WHICH" = "py311" ] || [ "$WHICH" = "both" ]; then
  run_set py311
fi
if [ "$WHICH" = "py38" ] || [ "$WHICH" = "both" ]; then
  export PATH="$PY38_BIN:$PATH"
  unset VIRTUAL_ENV
  run_set py38
fi
echo "done $(date -u +%FT%TZ)" >> "$LOG/regression_env.txt"
