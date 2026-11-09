#!/usr/bin/env bash
# 명령 하나를 로그로 — 머리 "$ 명령" · 끝 "rc=…" (회귀 로그 꼴).  쓰임: bash run_logged.sh <작업 폴더> <로그> <명령 …>
set -u
D=${1:?작업 폴더}
L=${2:?로그}
shift 2
cd "$D" || exit 9
{
  echo "\$ $*"
  "$@"
  echo "rc=$?"
} > "$L" 2>&1
tail -3 "$L"
