#!/usr/bin/env bash
# 지정 변이의 행 단위 확인 로그 — 쓰임: bash run_mutant_rows.sh <fixc 폴더> <mutate15.py> <고친 판 사슬> <변이 목록 쉼표>
set -u
FX=${1:?fixc}
cd "$FX" || exit 9
{
  echo '$ python3 mutant_rows.py <mutate15.py> <고친 판 사슬> <변이 행 트리 = 바탕 링크 + 고친 판 scripts (최종 시험)> <도구> <출력> <변이 목록>  # 지정 변이마다 기대와 다른 시험 행 (RR5A–F · RR4D)'
  timeout 1800 python3 tools/mutant_rows.py "$2" "$3" mut_rows tools logs/mutant_rows.json "$4"
  echo "rc=$?"
} > logs/mutant_rows.log 2>&1
cut -c1-250 logs/mutant_rows.log
sha256sum mut_rows/scripts/rint_r_chain.py
