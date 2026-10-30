#!/bin/bash
# run_one.sh <tag> <env> [extra args to test_resume_ckpt.py ...]
#   env = py311_mawk | py311_gawk | py38_mawk | py38all_mawk
#   log = $SP/logs/<tag>_<env>.log ; one-line summary appended to $SP/logs/<tag>_summary.txt
#   reruns (max 3) if the log has an ENOSPC line
SP=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad
W=$SP/f01r2
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-ac3f433b81b4e211e
P38=/root/.local/share/uv/python/cpython-3.8.20-linux-x86_64-gnu/bin/python3.8
T=$1; ENV=$2; shift 2
mkdir -p "$W/logs" "$W/tmp"
cd "$WT" || exit 1
export TMPDIR="$W/tmp"
case $ENV in
  py311_mawk) CMD=(python3 -I scripts/test_resume_ckpt.py);;
  py311_gawk) CMD=(env PATH="$SP/gawk_bin:$PATH" python3 -I scripts/test_resume_ckpt.py);;
  py38_mawk) CMD=("$P38" -I scripts/test_resume_ckpt.py);;
  py38all_mawk) CMD=(env PATH="$SP/f01_work/py38_bin:$PATH" "$P38" -I scripts/test_resume_ckpt.py);;
  *) echo "unknown env $ENV"; exit 2;;
esac
n=0
while :; do
  t0=$(date +%s)
  nice -n 10 "${CMD[@]}" "$@" > "$W/logs/${T}_${ENV}.log" 2>&1; rc=$?
  t1=$(date +%s)
  grep -qE 'No space left|Errno 28' "$W/logs/${T}_${ENV}.log" || break
  n=$((n+1)); [ $n -ge 3 ] && break
  sleep 30
done
echo "$ENV rc=$rc $(tail -1 "$W/logs/${T}_${ENV}.log") · $((t1-t0)) s · ENOSPC 다시 $n 번 · 남은 ENOSPC 줄 $(grep -cE 'No space left|Errno 28' "$W/logs/${T}_${ENV}.log")" >> "$W/logs/${T}_summary.txt"
tail -1 "$W/logs/${T}_summary.txt"
