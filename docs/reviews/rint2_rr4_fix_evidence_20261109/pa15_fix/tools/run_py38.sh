#!/usr/bin/env bash
# kgy 판 3.8 묶음 (scripts/check_kgy_py38.sh 그대로 · 묶음 로그 = KGY_PY38_LOGDIR) — 쓰임: bash run_py38.sh <작업 트리> <요약 로그> <묶음 로그 폴더>
set -u
export KGY_PY38_LOGDIR=${3:?묶음 로그 폴더}
mkdir -p "$KGY_PY38_LOGDIR"
cd "${1:?작업 트리}" || exit 9
{
  echo "\$ KGY_PY38_LOGDIR=<로그> bash scripts/check_kgy_py38.sh"
  bash scripts/check_kgy_py38.sh
  echo "rc=$?"
} > "${2:?요약 로그}" 2>&1
tail -3 "$2"
