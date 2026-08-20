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

# --- 같은 프로젝트의 다른 폴더 ----------------------------------------------
#
# 자동으로 갈아끼우면 안 된다.  폴더가 다르면 data/ 도 다르므로, 조용히 바꾸면
# 올려 둔 .wrd 가 사라진 것처럼 보인다.  0(우리 것)도 1(남의 것)도 아닌 3 으로
# 따로 답하고, 부르는 쪽이 폴더 이름을 보여 주며 사용자에게 고르게 한다.
other="$(mktemp -d)"
mkdir -p "$other/packages/wrdkit/src/wrdkit" "$other/apps/api"
classify_process \
  "$other/.venv/bin/python -m uvicorn app.main:app --app-dir $other/apps/api" \
  "$other"
verdict=$?
if [ "$verdict" -eq 3 ] && [ "$OTHER_CHECKOUT" = "$other" ]; then
  pass=$((pass + 1))
  printf '  ok   다른 폴더의 워크벤치: 3 으로 구분하고 폴더를 알려준다\n'
else
  fail=$((fail + 1))
  printf '  FAIL 다른 폴더의 워크벤치를 구분하지 못했다 (verdict=%s, folder=%s)\n' \
    "$verdict" "${OTHER_CHECKOUT:-없음}"
fi

# 그 폴더가 이미 다른 브랜치로 넘어갔어도 프로세스는 살아서 포트를 문다 —
# 오히려 그때가 원인을 찾기 가장 어렵다.  실행 파일이 그 폴더의 venv 면
# 우리 실행기가 띄운 것으로 본다.  (실제로 그렇게 옛 폴더의 서버가 5003 을
# 잡고 있었다.)
OTHER_CHECKOUT=""
gone="$(mktemp -d)"          # 워크벤치 파일은 없다 (브랜치가 바뀌었다)
classify_process \
  "$gone/.venv/bin/python -m uvicorn app.main:app --app-dir $gone/apps/api" "$gone"
verdict=$?
if [ "$verdict" -eq 3 ] && [ "$OTHER_CHECKOUT" = "$gone" ]; then
  pass=$((pass + 1))
  printf '  ok   폴더는 넘어갔지만 살아 있는 워크벤치 서버를 알아본다\n'
else
  fail=$((fail + 1))
  printf '  FAIL 폴더가 넘어간 워크벤치 서버를 놓쳤다 (verdict=%s)\n' "$verdict"
fi

# 워크벤치 표식도 없고 그 폴더의 venv 도 아니면 그냥 남의 것이다.
OTHER_CHECKOUT=""
notrepo="$(mktemp -d)"
mkdir -p "$notrepo/apps/api"
expect_stranger "app-dir 는 있지만 워크벤치가 아닌 폴더" \
  "/usr/bin/python3 -m uvicorn app.main:app --app-dir $notrepo/apps/api" "$notrepo"
rm -rf "$other" "$notrepo" "$gone"

# --- 구조 불변식 -------------------------------------------------------------
#
# bml 은 pull 로 자기 자신을 갈아치운다.  bash 는 파일 오프셋을 기억했다가
# 되돌아가 읽으므로, 마지막 줄 뒤에 코드가 남아 있으면 새 파일의 엉뚱한
# 바이트에 착지해 옛 코드와 새 코드가 섞여 돈다.  실제로 그렇게 이미 고친
# 버그가 되살아났다.  마지막 줄을 고정한다.
last="$(grep -v '^[[:space:]]*$' "$HERE/../bml" | tail -1)"
if [ "$last" = '{ main "$@"; exit $?; }' ]; then
  pass=$((pass + 1))
  printf '  ok   구조: bml 의 마지막 줄이 main+exit 묶음이다\n'
else
  fail=$((fail + 1))
  printf '  FAIL 구조: bml 의 마지막 줄이 바뀌었다 — 자기 갱신 중 깨진다\n       %s\n' "$last"
fi

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
