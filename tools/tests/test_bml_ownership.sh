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

# --- 우리 안에 있는 남의 checkout ---------------------------------------------
#
# 다른 checkout 을 "$REPO/.worktrees/other" 처럼 우리 트리 안에 두는 것은 흔한
# 배치다.  그때 그 서버의 --app-dir 도 "$REPO/" 로 시작하므로, 경로 접두사만
# 보면 우리 것으로 판정돼 "다른 폴더의 워크벤치" 분기가 아예 실행되지 않는다 —
# 남의 data/ 를 가진 서버를 우리 것인 양 열어 주거나 죽인다.
OTHER_CHECKOUT=""
nested="$REPO/.worktrees/other"
mkdir -p "$nested/packages/wrdkit/src/wrdkit" "$nested/apps/api"
classify_process \
  "$nested/.venv/bin/python -m uvicorn app.main:app --app-dir $nested/apps/api" \
  "$nested"
verdict=$?
if [ "$verdict" -eq 3 ] && [ "$OTHER_CHECKOUT" = "$nested" ]; then
  pass=$((pass + 1))
  printf '  ok   우리 트리 안에 중첩된 다른 checkout 을 구분한다\n'
else
  fail=$((fail + 1))
  printf '  FAIL 중첩 checkout 을 우리 것으로 봤다 (verdict=%s)\n' "$verdict"
fi
rm -rf "$REPO/.worktrees"
OTHER_CHECKOUT=""

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

# --- 접두사만 겹치는 폴더가 명령줄 *안에* 있을 때 ---------------------------
#
# 위 케이스는 cwd 로만 이웃 폴더를 덮는다.  진짜 사고는 명령줄에 그 경로가
# 들어올 때 난다: "$REPO-old" 는 문자열로 "$REPO" 를 포함하므로, 경계 없는
# 부분일치는 --app-dir 분기(3)에 닿기도 전에 "우리 것"(0)이라고 답한다.
# 그러면 start_serve 는 남의 data/ 를 가진 서버를 "이미 돌고 있습니다" 로
# 열어 주고(올린 .wrd 가 사라진 것처럼 보이는 바로 그 사고), 비정상이면
# cmd_stop 으로 갈아끼운다.
OTHER_CHECKOUT=""
sibling="${REPO}-old"
classify_process \
  "$sibling/.venv/bin/python -m uvicorn app.main:app --app-dir $sibling/apps/api" \
  "$sibling"
verdict=$?
if [ "$verdict" -eq 3 ] && [ "$OTHER_CHECKOUT" = "$sibling" ]; then
  pass=$((pass + 1))
  printf '  ok   접두사만 겹치는 형제 체크아웃: 3 으로 구분한다\n'
else
  fail=$((fail + 1))
  printf '  FAIL 형제 체크아웃을 우리 것으로 봤다 (verdict=%s, folder=%s)\n' \
    "$verdict" "${OTHER_CHECKOUT:-없음}"
fi

# 같은 접두사를 쓰는 완전한 남 (모듈 경로부터 다르다).  1 이어야 한다 — 3 은
# "사용자에게 묻는다" 라서 남의 프로세스에 붙일 답이 아니다.
OTHER_CHECKOUT=""
classify_process \
  "/usr/bin/python3 -m uvicorn somebody.main:app --app-dir ${REPO}-backup/apps/api" \
  "/tmp"
verdict=$?
if [ "$verdict" -eq 1 ]; then
  pass=$((pass + 1))
  printf '  ok   남의 것: 접두사만 겹치는 폴더의 남의 uvicorn\n'
else
  fail=$((fail + 1))
  printf '  FAIL 접두사만 겹치는 폴더의 남을 %s 로 봤다 (죽일 뻔)\n' "$verdict"
fi

# 위를 조이다가 진짜 우리 것을 놓치면 안 된다: --app-dir 가 저장소 루트인 형태.
expect_ours "app-dir 가 저장소 루트인 uvicorn" \
  "/usr/bin/python3 -m uvicorn app.main:app --app-dir $REPO" "/tmp"

# --- PID 파일에 적힌 pid 를 죽여도 되는가 ------------------------------------
#
# PID 파일은 재부팅이나 강제 종료 뒤에도 남고, 커널은 pid 번호를 재사용한다.
# "살아 있다"(kill -0) 만 보고 죽이면 그 번호를 물려받은 남의 프로세스를,
# 그것도 프로세스 그룹째 죽인다.  포트 쪽과 같은 기준으로 신원을 확인해야 한다.
sleep 30 &
stranger_pid=$!
if owns_pid "$stranger_pid"; then
  fail=$((fail + 1))
  printf '  FAIL 낡은 PID 파일이 가리키는 남의 pid 를 우리 것으로 봤다 (pid=%s)\n' \
    "$stranger_pid"
else
  pass=$((pass + 1))
  printf '  ok   남의 pid: 살아 있다는 것만으로는 우리 것이 아니다\n'
fi

# 반대 방향도 고정한다.  실제 서버를 띄우지 않고 argv[0] 로 명령줄만 흉내 낸다.
bash -c "exec -a '$REPO/.venv/bin/python -m uvicorn app.main:app' sleep 30" &
ours_pid=$!
sleep 0.3   # exec 가 끝나 /proc/pid/cmdline 이 바뀔 때까지
if owns_pid "$ours_pid"; then
  pass=$((pass + 1))
  printf '  ok   우리 pid: 우리 venv 로 도는 프로세스는 알아본다\n'
else
  fail=$((fail + 1))
  printf '  FAIL 우리 프로세스를 남의 것으로 봤다 — bml stop 이 아무것도 못 내린다\n'
fi
kill "$ours_pid" 2>/dev/null

# cmd_stop 이 그 판정을 실제로 쓰는지.  낡은 PID 파일이 남을 가리키면 죽이지
# 않고 파일만 지워야 한다.
tmp_run="$(mktemp -d)"
save_pid_file="$PID_FILE"; save_dev_file="$DEV_PID_FILE"
save_port="$PORT"; save_api_port="$API_PORT"
PID_FILE="$tmp_run/server.pid"; DEV_PID_FILE="$tmp_run/dev.pid"
# 돌고 있을지도 모르는 진짜 서버를 건드리지 않도록 아무도 안 쓰는 포트로.
PORT=59997; API_PORT=59996
printf '%s' "$stranger_pid" > "$PID_FILE"
cmd_stop >/dev/null 2>&1
if kill -0 "$stranger_pid" 2>/dev/null; then
  pass=$((pass + 1))
  printf '  ok   cmd_stop: 낡은 PID 파일이 가리키는 남의 프로세스를 살려 둔다\n'
else
  fail=$((fail + 1))
  printf '  FAIL cmd_stop 이 PID 파일만 믿고 남의 프로세스를 죽였다\n'
fi
kill "$stranger_pid" 2>/dev/null
PID_FILE="$save_pid_file"; DEV_PID_FILE="$save_dev_file"
PORT="$save_port"; API_PORT="$save_api_port"
rm -rf "$tmp_run"

# --- 의존성만 바뀐 pull 뒤의 프론트엔드 빌드 ---------------------------------
#
# package-lock.json 만 바뀐 커밋(라이브러리 버그 픽스)을 받으면 src 는 그대로다.
# 그것을 빌드 대상에서 빼면 옛 라이브러리가 구워진 dist 를 계속 서빙하면서
# "빌드 최신" 이라고 말한다 — 고친 걸 받았는데 증상이 똑같은 그 경우다.
webtmp="$(mktemp -d)"
mkdir -p "$webtmp/apps/web/src" "$webtmp/apps/web/dist"
for f in index.html vite.config.ts tsconfig.json package.json package-lock.json \
         src/main.tsx; do
  : > "$webtmp/apps/web/$f"
done
touch -d '2020-01-01' "$webtmp/apps/web/src" "$webtmp/apps/web/src/main.tsx" \
  "$webtmp/apps/web/index.html" "$webtmp/apps/web/vite.config.ts" \
  "$webtmp/apps/web/tsconfig.json" "$webtmp/apps/web/package.json" \
  "$webtmp/apps/web/package-lock.json"
touch -d '2021-01-01' "$webtmp/apps/web/dist/index.html"

save_repo="$REPO"; REPO="$webtmp"
if web_needs_build; then
  fail=$((fail + 1))
  printf '  FAIL 아무것도 안 바뀌었는데 다시 빌드한다\n'
else
  pass=$((pass + 1))
  printf '  ok   빌드 최신: 소스가 dist 보다 오래됐으면 다시 빌드하지 않는다\n'
fi

touch -d '2022-01-01' "$webtmp/apps/web/package-lock.json"
if web_needs_build; then
  pass=$((pass + 1))
  printf '  ok   의존성만 바뀐 pull 뒤에도 다시 빌드한다\n'
else
  fail=$((fail + 1))
  printf '  FAIL package-lock.json 이 새로운데 낡은 dist 를 서빙한다\n'
fi
REPO="$save_repo"
rm -rf "$webtmp"

# --- 시작 직후 PID 파일 기록 --------------------------------------------------
#
# lsof·ss·fuser 가 하나도 없는 머신에서는 port_owner 가 빈 문자열을 낸다
# (port_busy 의 /dev/tcp 폴백이 그 환경을 위해 있다).  그때 파일로 바로
# 리다이렉트하면 파일이 먼저 잘려, 시작할 때 적어 둔 pid 까지 잃는다 —
# 그러면 bml stop 이 자기 서버를 남의 것으로 오인하고 영영 못 내린다.
#
# port_owner 를 여기서 갈아끼우므로, 이 아래에서는 원래 것을 쓰지 않는다.
pidfile="$(mktemp)"
printf '%s' 4242 > "$pidfile"
port_owner() { printf ''; }
record_port_owner 5003 "$pidfile"
if [ "$(cat "$pidfile")" = "4242" ]; then
  pass=$((pass + 1))
  printf '  ok   소유자를 알 수 없으면 적어 둔 pid 를 지우지 않는다\n'
else
  fail=$((fail + 1))
  printf '  FAIL PID 파일이 비었다 (내용=%s) — bml stop 이 자기 서버를 못 내린다\n' \
    "$(cat "$pidfile")"
fi

port_owner() { printf '%s' 777; }
record_port_owner 5003 "$pidfile"
if [ "$(cat "$pidfile")" = "777" ]; then
  pass=$((pass + 1))
  printf '  ok   소유자를 알아내면 실제 pid 로 갱신한다\n'
else
  fail=$((fail + 1))
  printf '  FAIL 실제 포트 소유자를 기록하지 못했다 (내용=%s)\n' "$(cat "$pidfile")"
fi
rm -f "$pidfile"

# start_serve/start_dev 가 그 함수를 실제로 쓰는지.  `port_owner … > "$PID_FILE"`
# 로 돌아가면 셸이 명령을 실행하기 전에 파일을 잘라 버리므로 위 회귀가 그대로
# 되살아난다 — 함수 하나만으로는 못 막는 형태라 소스에서 금지한다.
truncating="$(grep -nE 'port_owner[^)]*>[[:space:]]*"\$' "$HERE/../bml" \
              | grep -vE '^[0-9]+:[[:space:]]*#')"
record_calls="$(grep -c 'record_port_owner "' "$HERE/../bml")"
if [ -z "$truncating" ] && [ "$record_calls" -ge 3 ]; then
  pass=$((pass + 1))
  printf '  ok   구조: PID 파일 기록이 잘라 쓰는 리다이렉션이 아니다\n'
else
  fail=$((fail + 1))
  printf '  FAIL 구조: PID 파일을 잘라 쓴다 (호출 %s곳)\n       %s\n' \
    "$record_calls" "$truncating"
fi

# --- doctor 의 처방 -----------------------------------------------------------
#
# `bml doctor` 는 "안 되면 여기부터" 라, 사용자는 출력된 명령을 그대로
# 붙여넣는다.  그 안에 `git reset --hard` 가 한 줄 있으면 CRLF 파일 하나를
# 고치는 대가로 저장소 전체의 미커밋 작업이 말없이 사라진다 — 이 저장소는
# --autostash 로 "커밋 안 해도 잃지 않는다" 를 전제로 굴러가는데 정반대다.
#
# 그리고 tools/bml 만 검사하면 반쪽이다.  사람이 실제로 붙여넣는 처방은
# 가이드 문서에도 있고, 거기 남아 있으면 피해는 똑같다 — 실제로 bml 은
# 고쳤는데 wsl-setup.md 에 `git rm --cached -r . && git reset --hard` 가
# 그대로 남아 있었다.
destructive=""
for source in "$HERE/../bml" "$HERE/../../docs/guides/wsl-setup.md" \
              "$HERE/../../docs/guides/bml-command.md" "$HERE/../../README.md"; do
  [ -f "$source" ] || continue
  hit="$(grep -nE 'reset --hard|checkout -f|clean -[a-z]*f|rm --cached' "$source" \
         | grep -vE '^[0-9]+:[[:space:]]*(#|>)')"
  [ -n "$hit" ] && destructive="$destructive
${source##*/}: $hit"
done
if [ -z "$destructive" ]; then
  pass=$((pass + 1))
  printf '  ok   처방(코드·문서)에 미커밋 작업을 날리는 명령이 없다\n'
else
  fail=$((fail + 1))
  printf '  FAIL 파괴적 명령이 처방돼 있다%s\n' "$destructive"
fi

# 대신 안전한 대안이 실제로 존재해야 한다 — 문서가 없는 명령을 안내하면
# 사용자는 결국 옛 처방을 검색해서 쓴다.
if grep -q 'cmd_repair_crlf' "$HERE/../bml" \
   && grep -q 'repair crlf' "$HERE/../../docs/guides/wsl-setup.md"; then
  pass=$((pass + 1))
  printf '  ok   안전한 대안(bml repair crlf)이 코드와 문서 양쪽에 있다\n'
else
  fail=$((fail + 1))
  printf '  FAIL 문서가 안내하는 CRLF 복구 명령이 코드에 없다\n'
fi

echo
if [ "$fail" -eq 0 ]; then
  printf '결과: %d개 통과\n' "$pass"
  exit 0
fi
printf '결과: %d개 통과, %d개 실패\n' "$pass" "$fail"
exit 1
