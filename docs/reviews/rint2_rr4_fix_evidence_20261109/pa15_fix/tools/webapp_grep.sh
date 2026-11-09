#!/usr/bin/env bash
# 웹앱 grep — 재개 자격 · 원장 · 재개 출처 공통 검증 화면이 웹앱에 있나 (코드 → 웹앱 순차 반영 규칙 · 없으면 그 사실을 적는다).  쓰임: bash webapp_grep.sh <작업 트리>
set -u
cd "${1:?작업 트리}" || exit 9
P='resume_ok|RESUME_NOT_ALLOWED|RESUME_MISMATCH|rint_r_chain|재실행 자격|재개 출처|resume_provenance|attempt_entry_diff|ResultHeld|resume_disk_rerun|resume_recompare_run|ATTEMPT_OPEN'
echo "\$ grep -rIc -E '$P' webapp/ (0 아닌 파일만)"
hits=$(grep -rIc -E "$P" webapp/ | grep -v ':0$')
[ -n "$hits" ] && echo "$hits"
echo "0 아닌 파일 수 = $(printf '%s' "$hits" | grep -c .)"
