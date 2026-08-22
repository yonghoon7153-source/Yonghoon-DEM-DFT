#!/usr/bin/env bash
# 커밋 **전에** 돌리는 것 — CI 가 돌릴 것을 그대로, 먼저.
#
# ★★ 왜 (2026-08-20, 같은 실수 두 번):
#   `--selftest` 는 **검사기가 맞나**를 보고, 인자 없는 실행은 **리포가 맞나**를 본다.
#   두 번 다 나는 selftest 만 돌리고 푸시했다:
#     ① CLAUDE.md 에 철회값을 인용 → ban-sweep 이 6건 (CI run 2 = failure)
#     ② CL-58 에 `kind: measurement` (유효값 아님) → 규율 J (CI run 11 = failure)
#   ②는 러너의 fail-closed 게이트라 **사용자의 GPU 런을 막았다** — CI 가 60 초 뒤 빨간불을
#   냈지만 그 사이에 pull 이 일어났다.  ⇒ 기억에 맡기지 말고 한 명령으로 묶는다.
#
#   bash scripts/check_all.sh
#
# ⚠ GPU·솔브 없음.  규칙 J 의 초소형 픽스처 스모크가 가장 오래 걸린다 (수 초).
set -uo pipefail
cd "$(dirname "$0")/.."

FAIL=0
run() {
  local label="$1"; shift
  if "$@" >/tmp/_ca.$$ 2>&1; then
    printf '  ✓ %s\n' "$label"
  else
    printf '  ✗ %s\n' "$label"
    sed 's/^/      /' /tmp/_ca.$$ | tail -25
    FAIL=1
  fi
  rm -f /tmp/_ca.$$
}

echo "── selftest (검사기가 맞나) ──"
run 'check_review_findings   --selftest' python3 scripts/check_review_findings.py --selftest
run 'check_method_discipline --selftest' python3 scripts/check_method_discipline.py --selftest
run 'sdcp_gain_verdict       --selftest' python3 scripts/sdcp_gain_verdict.py --selftest
run 'sdcp_phase_ledger_match --selftest' python3 scripts/sdcp_phase_ledger_match.py --selftest

echo "── 리포 실물 (리포가 맞나 — selftest 가 **대신해 주지 않는다**) ──"
run 'check_review_findings   (원장 + 철회값 스윕)' python3 scripts/check_review_findings.py
run 'check_method_discipline (규칙 A~J + claims 원장)' python3 scripts/check_method_discipline.py

echo
if [ "$FAIL" = 0 ]; then
  echo "✓ 전부 통과 — 커밋해도 된다 (CI 가 같은 것을 다시 돈다)"
else
  echo "✗ 실패가 있다 — 고치고 다시.  ⚠ 이대로 푸시하면 러너의 fail-closed 게이트가"
  echo "  사용자의 GPU 런을 막는다 (규율 검사는 런 시작 전에 걸린다)."
fi
exit "$FAIL"
