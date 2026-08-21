#!/usr/bin/env bash
#
# 서버가 내려갈 수 있는가.
#
# 실시간 갱신(SSE)을 붙인 날 이것이 깨졌다.  이벤트 스트림은 스스로 끝나는
# 응답이 아니라서, uvicorn 의 graceful shutdown 이 "하던 요청" 이 끝나기를
# 영원히 기다린다.  브라우저 탭이 하나라도 열려 있으면 SIGTERM 으로는 죽지
# 않고 포트를 계속 붙잡는다 — 측정해 보니 10초 뒤에도 살아 있었다.
#
# 증상은 엉뚱한 곳에서 나온다: `bml` 이 "포트 5003 가 아직 잡혀 있습니다.
# WORKBENCH_PORT=6001 로 옮기세요" 로 죽는다.  옮길 이유가 전혀 없는데도.
#
# 두 가지가 함께 막는다.  uvicorn 쪽 상한과, bml 쪽에서 그래도 남아 있으면
# 확실히 내리는 것.  둘 중 하나만 있어도 대부분 되지만, 하나가 빠지면 남는
# 실패가 "가끔 안 뜬다" 라 원인을 찾기 어렵다.
#
# 사용: bash tools/tests/test_bml_shutdown.sh     (실패 0 이면 exit 0)

set -uo pipefail

HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BML="$HERE/../bml"
MAKEFILE="$HERE/../../Makefile"

pass=0
fail=0

check() {
  local what="$1" condition="$2"
  if [ "$condition" = "yes" ]; then
    pass=$((pass + 1))
    printf '  ok   %s\n' "$what"
  else
    fail=$((fail + 1))
    printf '  FAIL %s\n' "$what"
  fi
}

has() {
  if grep -q -- "$2" "$1"; then echo yes; else echo no; fi
}

# uvicorn 을 띄우는 곳마다 상한이 걸려 있어야 한다.  한 곳만 빠지면 그 경로로
# 띄운 서버만 안 죽는데, 사용자는 어느 경로로 떴는지 모른다.
# 주석에도 `-m uvicorn` 이 나온다 (make serve 를 설명하는 대목).  실제로
# 띄우는 줄만 센다.
launches="$(grep -c -- '-m uvicorn app.main:app' "$BML")"
timeouts="$(grep -c -- '--timeout-graceful-shutdown' "$BML")"
check "bml 의 uvicorn 실행이 모두 종료 상한을 건다 (${timeouts}/${launches})" \
  "$([ "$launches" -gt 0 ] && [ "$timeouts" -eq "$launches" ] && echo yes || echo no)"

check "make serve 도 같은 상한을 건다" \
  "$(has "$MAKEFILE" '--timeout-graceful-shutdown')"

# SIGTERM 이 안 통했을 때 물러서면 안 된다.  포트 소유 판정은 이미 끝난
# 뒤이므로(test_bml_ownership.sh 가 그것을 지킨다) 세게 죽여도 우리 것이다.
check "bml stop 이 안 죽는 프로세스를 확실히 내린다" "$(has "$BML" 'kill -9')"

# 1초만 기다렸다 포기하면, 탭 몇 개 열어 둔 것만으로 "포트를 옮기세요" 가 뜬다.
check "다시 뜨기 전에 포트가 풀릴 시간을 준다" \
  "$(grep -A 6 'local freed=0' "$BML" | grep -q 'port_busy' && echo yes || echo no)"

printf '\n=== BML SHUTDOWN === 실패 %s\n' "$fail"
[ "$fail" -eq 0 ]
