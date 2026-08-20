#!/usr/bin/env bash
#
# bml 의 포트 소유 판정 회귀 테스트.
#
# Every case below is a bug that actually shipped.  The rule the whole file
# defends: `bml` may replace its own server, and may never kill anyone else's.
# Getting that wrong in either direction has a real cost -- a refused launch
# wastes the user's time, a wrong kill destroys someone's running experiment.

set -uo pipefail

HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BML_SOURCE_ONLY=1 source "$HERE/../bml"

pass=0
fail=0

#: expect_ours <설명> <cmdline> [cwd]
expect_ours() {
  local what="$1" cmd="$2" cwd="${3:-}"
  if classify_process "$cmd" "$cwd"; then
    pass=$((pass + 1))
    printf '  ok   우리 것: %s\n' "$what"
  else
    fail=$((fail + 1))
    printf '  FAIL 우리 것인데 남의 것으로 봤다: %s\n       cmd=%s cwd=%s\n' "$what" "$cmd" "$cwd"
  fi
}

#: expect_stranger <설명> <cmdline> [cwd]
expect_stranger() {
  local what="$1" cmd="$2" cwd="${3:-}"
  if classify_process "$cmd" "$cwd"; then
    fail=$((fail + 1))
    printf '  FAIL 남의 것인데 우리 것으로 봤다 (죽일 뻔): %s\n       cmd=%s cwd=%s\n' "$what" "$cmd" "$cwd"
  else
    pass=$((pass + 1))
    printf '  ok   남의 것: %s\n' "$what"
  fi
}

echo "bml 포트 소유 판정"

# --- 우리 것으로 알아봐야 하는 것들 -----------------------------------------

# bml 이 직접 띄우는 형태. python_bin() 이 절대경로를 준다.
expect_ours "bml serve (절대경로 venv)" \
  "$REPO/.venv/bin/python -m uvicorn app.main:app --port 5003" "$REPO/apps/api"

# make serve 는 상대경로로 띄운다.  argv[0] 를 프로세스의 cwd 에 붙여야 보인다.
# 여기서 readlink -f 를 쓰면 venv 의 bin/python 심볼릭 링크를 따라가 시스템
# 인터프리터가 되어 버려서, 찾으려던 표식이 바로 그때 사라진다.
expect_ours "make serve (상대경로 venv)" \
  ".venv/bin/python -m uvicorn app.main:app --port 5003" "$REPO"

expect_ours "손으로 띄운 ./venv 상대경로" \
  "./.venv/bin/python -m uvicorn app.main:app" "$REPO"

# 개발 서버.
expect_ours "vite dev" "node $REPO/apps/web/node_modules/.bin/vite" "$REPO/apps/web"
expect_ours "npm run dev" "npm run dev" "$REPO/apps/web"

# 저장소 경로를 인자로 든 uvicorn 은 어디서 띄웠든 우리 것이다.
expect_ours "app-dir 로 우리 트리를 가리키는 uvicorn" \
  "/usr/bin/python3 -m uvicorn app.main:app --app-dir $REPO/apps/api" "/tmp"

# --- 절대로 죽이면 안 되는 것들 ---------------------------------------------

# 이게 실제로 죽었던 케이스다.  'app.main:app' 은 FastAPI 튜토리얼의 경로라
# 남의 곁다리 프로젝트도 똑같이 쓴다.  cwd 가 우리 apps/api 일 때만 우리 것.
expect_stranger "남의 FastAPI (같은 app.main:app, 다른 디렉터리)" \
  "/usr/bin/python3 -m uvicorn app.main:app --host 127.0.0.1 --port 5003" \
  "/home/someone/other-project"

# 저장소 디렉터리에서 띄웠다는 것만으로는 근거가 안 된다.  한때 cwd 만 보고
# 판단했다가 애먼 프로세스를 죽였다.
expect_stranger "우리 저장소 안에서 띄운 남의 프로그램" \
  "/usr/bin/python3 -m http.server 5003" "$REPO"

expect_stranger "다른 venv 의 파이썬" \
  "/home/someone/other/.venv/bin/python -m uvicorn app.main:app" "/home/someone/other"

expect_stranger "이름만 비슷한 경로" \
  "/home/someone/.venv-backup/bin/python server.py" "/home/someone"

expect_stranger "평범한 웹서버" "nginx: master process /usr/sbin/nginx" "/"

# vite 라도 우리 apps/web 에서 돈 게 아니면 남의 것이다.
expect_stranger "남의 vite" "node /home/someone/site/node_modules/.bin/vite" "/home/someone/site"

# 저장소 이름을 접두사로만 공유하는 이웃 디렉터리.
expect_stranger "이름이 겹치는 옆 디렉터리" \
  ".venv/bin/python -m uvicorn app.main:app" "${REPO}-backup"

echo
if [ "$fail" -eq 0 ]; then
  printf '결과: %d개 통과\n' "$pass"
  exit 0
fi
printf '결과: %d개 통과, %d개 실패\n' "$pass" "$fail"
exit 1
