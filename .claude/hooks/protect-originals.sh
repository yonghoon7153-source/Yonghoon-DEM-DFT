#!/usr/bin/env bash
# Refuse edits to the immutable layers.
#
# `data/uploads/` holds the original .wrd files: everything downstream can be
# rebuilt from them, and nothing can rebuild them.  `docs/raw/` is the record
# of what was established by decoding those files.  Neither is ever edited in
# place -- new findings are appended, and a bad parse is fixed by re-parsing.
set -euo pipefail

payload=$(cat)
path=$(printf '%s' "$payload" | python3 -c '
import json, sys
try:
    data = json.load(sys.stdin)
except Exception:
    print(""); raise SystemExit
print(data.get("tool_input", {}).get("file_path", "") or "")
')

[ -z "$path" ] && exit 0

case "$path" in
  */data/uploads/*)
    echo "차단: data/uploads/ 의 원본 .wrd 는 불변입니다. 파싱 결과를 고치려면 파서를 고치고 재파싱하세요." >&2
    exit 2
    ;;
  */docs/raw/*)
    if [ -e "$path" ]; then
      echo "차단: docs/raw/ 는 불변 레이어입니다. 새 발견은 문서 끝에 추가하거나 새 파일로 만드세요." >&2
      exit 2
    fi
    ;;
esac
exit 0
