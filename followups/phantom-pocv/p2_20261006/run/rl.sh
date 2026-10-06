#!/bin/bash
# rl.sh <name> <timeout_s> <cmd...> — P2 명령 기록: argv · cwd · 시각 · 사본 HEAD · 저장소 HEAD · rc · 소요 · 디스크
L=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad/p2run; n=$1; to=$2; shift 2
{ echo "argv: $*"; echo "cwd: $(pwd)"; echo "start_utc: $(date -u +%FT%TZ)"; echo "copy_head: $(git rev-parse HEAD 2>/dev/null)"; echo "repo_head: $(git -C /home/user/Yonghoon-DEM-DFT rev-parse HEAD)"; echo "copy_dirty: $(git status --porcelain 2>/dev/null | wc -l)"; df -B1 . | tail -1 | awk '{print "disk_free_start: "$4}'; } > "$L/$n.meta.txt"
s=$(date +%s.%N); timeout "$to" "$@" > "$L/$n.stdout.log" 2> "$L/$n.stderr.log"; rc=$?; e=$(date +%s.%N)
{ echo "end_utc: $(date -u +%FT%TZ)"; echo "rc: $rc"; echo "elapsed_s: $(python3 -c "print(round($e-$s,2))")"; df -B1 . | tail -1 | awk '{print "disk_free_end: "$4}'; } >> "$L/$n.meta.txt"
echo "$n rc=$rc elapsed=$(python3 -c "print(round($e-$s,1))")"; exit $rc
