#!/usr/bin/env bash
# ⑤ 다시 대조 이름 꼴 자기 점검 로그 — 쓰임: bash rerun_type_log.sh <작업 트리> <로그> <도구 폴더>
set -u
{
  echo '$ python3 probe_rerun_type.py <작업 트리>  # ⑤ 다시 대조가 요약 resume.rerun 이름을 run_dirs 에 넘김 — 글 아닌 이름 · 요청 칸 없는 기록에서 traceback 없음 (앞 검사가 먼저 사유)'
  timeout 600 python3 "$3/probe_rerun_type.py" "$1"
  echo "rc=$?"
} > "$2" 2>&1
echo "ok $(grep -c '"ok"' "$2") · exc $(grep -c '"exc"' "$2") · $(tail -1 "$2")"
