#!/usr/bin/env bash
# C1 단계 실행 기록기 — P3 run_step.sh 형식 그대로 (argv · cwd · 시각 · HEAD · 디스크 · rc · 경과).
# 5 차 (§8-11 ③): 순서 스크립트 밖에서 (C1_TREE_ROOT 없음) 돌면 이 셸을 뿌리로 메모리 감시자를 붙인다 · 상한 초과면 rc 5.
# 사용: run_step.sh <이름> <명령...>   (cwd = 사본 루트 · 기록은 $C1_RUN/<이름>.{meta.txt,stdout.log,stderr.log,mem.jsonl,memtrip.json})
set -u
name="$1"; shift
: "${C1_RUN:?}" "${C1_COPY:?}" "${C1_REPO:?}"
meta="$C1_RUN/$name.meta.txt"
here="$(cd "$(dirname "$0")" && pwd)"
cd "$C1_COPY" || exit 99
export C1_STEP="$name"
{
  echo "argv: $*"
  echo "cwd: $(pwd)"
  echo "start_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "copy_head: $(git -C "$C1_COPY" rev-parse HEAD)"
  echo "repo_head: $(git -C "$C1_REPO" rev-parse HEAD)"
  echo "copy_dirty: $(git -C "$C1_COPY" status --porcelain | wc -l)"
  echo "disk_free_start: $(df -B1 --output=avail "$C1_COPY" | tail -1 | tr -d ' ')"
} > "$meta"
gpid=""
if [ -z "${C1_TREE_ROOT:-}" ] && [ -n "${PY:-}" ]; then
  "$PY" -I "$here/c1_memguard.py" watch --root $$ --log "$C1_RUN/$name.mem.jsonl" --trip "$C1_RUN/$name.memtrip.json" &
  gpid=$!
fi
t0=$(date +%s.%N)
"$@" > "$C1_RUN/$name.stdout.log" 2> "$C1_RUN/$name.stderr.log"
rc=$?
t1=$(date +%s.%N)
if [ -n "$gpid" ]; then kill -TERM "$gpid" 2>/dev/null; wait "$gpid" 2>/dev/null; fi
if [ -f "$C1_RUN/$name.memtrip.json" ]; then rc=5; fi
{
  echo "end_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "rc: $rc"
  echo "elapsed_s: $(python3 -c "print(round($t1-$t0,2))")"
  echo "disk_free_end: $(df -B1 --output=avail "$C1_COPY" | tail -1 | tr -d ' ')"
  [ -n "$gpid" ] && echo "mem_peak_B: $(grep '"summary"' "$C1_RUN/$name.mem.jsonl" | tail -1 | python3 -c 'import sys,json; print(json.loads(sys.stdin.read())["peak_B"])' 2>/dev/null)"
} >> "$meta"
exit $rc
