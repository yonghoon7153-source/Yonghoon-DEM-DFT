#!/usr/bin/env bash
# Nudges after an edit, based on which invariant the file touches.
#
# Deliberately advisory (exit 0): a hook that blocks on a heuristic gets
# disabled, and then it protects nothing.
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
root="${CLAUDE_PROJECT_DIR:-$(pwd)}"

case "$path" in
  */CLAUDE.md|*/AGENTS.md)
    echo "참고: CLAUDE.md 와 AGENTS.md 는 미러입니다. 'make wiki-lint' 로 parity 를 확인하세요."
    ;;
  */packages/wrdkit/src/*)
    echo "참고: wrdkit 변경은 테스트가 따라야 합니다 — python3 -m pytest packages/wrdkit/tests"
    echo "      숫자가 바뀌었다면 WRDKIT_SAMPLE 로 실측 검증도 돌리세요."
    ;;
  */apps/api/app/models.py)
    echo "참고: 컬럼을 더했다면 init_db 의 자동 마이그레이션이 처리합니다."
    echo "      이름 변경·타입 변경은 처리되지 않으니 ADR 을 먼저 쓰세요."
    ;;
  */apps/api/app/schemas.py)
    echo "참고: 스키마를 바꿨다면 apps/web/src/lib/types.ts 도 함께 고치세요."
    ;;
esac

if [ -f "$root/docs/adr/0001-store-raw-capacity-only.md" ]; then
  case "$path" in
    */apps/api/app/*)
      if grep -qE "mah_g|per_gram|normalized_capacity" "$path" 2>/dev/null; then
        echo "주의: 정규화된 용량을 저장하려는 것처럼 보입니다. ADR 0001 — raw mAh 만 저장합니다."
      fi
      ;;
  esac
fi
exit 0
