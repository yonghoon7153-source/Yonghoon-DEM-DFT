#!/usr/bin/env bash
# P3 단계 실행 기록기 — P2 의 meta 형식 그대로 (argv · cwd · 시각 · HEAD · 디스크 · rc · 경과).
# 사용: run_step.sh <이름> <명령...>   (cwd = 사본 루트 · 기록은 $P3_RUN/<이름>.{meta.txt,stdout.log,stderr.log})
set -u
name="$1"; shift
: "${P3_RUN:?}" "${P3_COPY:?}" "${P3_REPO:?}"
meta="$P3_RUN/$name.meta.txt"
cd "$P3_COPY" || exit 99
{
  echo "argv: $*"
  echo "cwd: $(pwd)"
  echo "start_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "copy_head: $(git -C "$P3_COPY" rev-parse HEAD)"
  echo "repo_head: $(git -C "$P3_REPO" rev-parse HEAD)"
  echo "copy_dirty: $(git -C "$P3_COPY" status --porcelain | wc -l)"
  echo "disk_free_start: $(df -B1 --output=avail "$P3_COPY" | tail -1 | tr -d ' ')"
} > "$meta"
t0=$(date +%s.%N)
"$@" > "$P3_RUN/$name.stdout.log" 2> "$P3_RUN/$name.stderr.log"
rc=$?
t1=$(date +%s.%N)
{
  echo "end_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "rc: $rc"
  echo "elapsed_s: $(python3 -c "print(round($t1-$t0,2))")"
  echo "disk_free_end: $(df -B1 --output=avail "$P3_COPY" | tail -1 | tr -d ' ')"
} >> "$meta"
exit $rc
