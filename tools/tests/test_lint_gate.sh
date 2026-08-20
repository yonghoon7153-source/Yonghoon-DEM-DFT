#!/usr/bin/env bash
# `make lint-py` 회귀 테스트 — ruff 위반이 있으면 반드시 0 이 아닌 코드로 죽어야 한다.
#
# 예전 레시피는 `|| true` 로 실패를 삼켰다. 그러면 CLAUDE.md 가 '커밋 전 필수'로
# 지정한 `make check` 는 통과하는데 `bml check` 와 CI 는 같은 검사에서 빨간불이
# 되고, 공용 브랜치라 상대가 그 CI 를 물려받는다.
#
# 저장소를 건드리지 않으려고 임시 폴더에 Makefile 만 복사해서 돌린다.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
FAILURES=0

fail() { echo "  x  $*"; FAILURES=$((FAILURES + 1)); }
ok() { echo "  ok $*"; }

if [ ! -x "$ROOT/.venv/bin/python" ]; then
  echo "SKIP: .venv 가 없습니다 (make install-api 후 다시 돌리세요)"
  exit 0
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

cp "$ROOT/Makefile" "$TMP/Makefile"
ln -s "$ROOT/.venv" "$TMP/.venv"
mkdir -p "$TMP/packages" "$TMP/apps/api"

# 1. 깨끗한 트리는 통과해야 한다 (게이트가 늘 실패하기만 하면 쓸모없다).
if make -C "$TMP" lint-py >/dev/null 2>&1; then
  ok "clean tree passes lint-py"
else
  fail "위반이 없는데도 make lint-py 가 실패함"
fi

# 2. F401 을 심으면 실패해야 한다.
printf 'import os\n' > "$TMP/packages/lint_gate_probe.py"
if make -C "$TMP" lint-py >/dev/null 2>&1; then
  fail "ruff 위반이 있는데 make lint-py 가 exit 0 (|| true 로 삼키고 있음)"
else
  ok "ruff violation fails lint-py"
fi

echo
echo "=== LINT GATE REGRESSION === 실패 $FAILURES"
[ "$FAILURES" -eq 0 ]
