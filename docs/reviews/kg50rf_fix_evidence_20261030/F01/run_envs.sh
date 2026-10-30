#!/bin/bash
# 시험 환경 차례로 — 인자: <꼬리표> <환경 목록 (쉼표)> [--script <도구>]  · 로그 = f01_work/<꼬리표>_<환경>.log · 요약 = <꼬리표>_summary.txt
#   디스크 가득 (No space left · Errno 28) 이 로그에 있으면 그 판은 버리고 다시 (최대 3 번 · 다시 한 횟수를 요약에 적는다)
S=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad
W=$S/f01_work; T=$1; ENVS=$2; shift 2
cd /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a9a7305d1b862d610 || exit 1
P38=/root/.local/share/uv/python/cpython-3.8.20-linux-x86_64-gnu/bin/python3.8
cmd(){ case $1 in
  py311_mawk) echo python3 -I scripts/test_resume_ckpt.py;;
  py311_gawk) echo env PATH=$S/gawk_bin:$PATH python3 -I scripts/test_resume_ckpt.py;;
  py38_mawk) echo $P38 -I scripts/test_resume_ckpt.py;;
  py38all_mawk) echo env PATH=$W/py38_bin:$PATH $P38 -I scripts/test_resume_ckpt.py;;
esac; }
for env in ${ENVS//,/ }; do
  n=0
  while :; do
    $(cmd $env) "$@" > $W/${T}_$env.log 2>&1; rc=$?
    grep -qE 'No space left|Errno 28' $W/${T}_$env.log || break
    n=$((n+1)); [ $n -ge 3 ] && break
    sleep 30
  done
  echo "$env rc=$rc $(tail -1 $W/${T}_$env.log) · ENOSPC 다시 $n 번 · 남은 ENOSPC 줄 $(grep -cE 'No space left|Errno 28' $W/${T}_$env.log)" >> $W/${T}_summary.txt
done
cat $W/${T}_summary.txt
