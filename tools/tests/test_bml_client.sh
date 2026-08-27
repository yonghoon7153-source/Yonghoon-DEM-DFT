#!/usr/bin/env bash
#
# 노트북이 중추 서버를 보게 하는 길.
#
# 이것이 없을 때 실제로 일어난 일: 노트북에서 `bml` 을 치면 그 노트북에
# 서버가 뜨고, 그 서버는 자기 폴더의 빈 `data/` 를 본다.  화면은 아무 오류
# 없이 멀쩡하게 뜨고 셀만 0개다 — 데이터가 날아간 것으로 읽힌다.  주소도
# 똑같이 localhost:5003 이라 어느 쪽을 보고 있는지 화면으로는 알 수 없다.
#
# 그래서 지켜야 하는 것이 셋이다.
#   1. 중추 서버가 정해져 있으면 `bml` 은 자기 서버를 띄우지 않는다.
#   2. 못 닿는 주소는 저장하지 않는다.  저장되면 그 뒤로 매번 실패하는데,
#      사람은 방금 적은 주소가 아니라 서버를 의심한다.
#   3. `.bml/env` 의 다른 줄(WORKBENCH_DATA 등)을 건드리지 않는다.
#
# 사용: bash tools/tests/test_bml_client.sh     (실패 0 이면 exit 0)

set -uo pipefail

HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BML="$HERE/../bml"

pass=0
fail=0
check() {
  local what="$1" got="$2" want="$3"
  if [ "$got" = "$want" ]; then
    pass=$((pass + 1)); printf '  ok   %s\n' "$what"
  else
    fail=$((fail + 1)); printf '  FAIL %s\n           얻음: %s\n           기대: %s\n' "$what" "$got" "$want"
  fi
}

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"; [ -n "${SERVER_PID:-}" ] && kill "$SERVER_PID" 2>/dev/null' EXIT

# 함수만 불러온다 (명령은 실행되지 않는다).
BML_SOURCE_ONLY=1 . "$BML"
# 진짜 저장소의 .bml/env 를 건드리지 않도록 옮겨 둔다.
REPO="$TMP/repo"; RUN_DIR="$REPO/.bml"; mkdir -p "$RUN_DIR"
# RUN_DIR 에서 파생된 경로들도 함께 옮긴다.  안 그러면 아래 시험이 진짜
# 저장소의 상태 파일을 지우고, 돌고 있던 개발 서버를 죽인다.
TUNNEL_PID_FILE="$RUN_DIR/tunnel.pid"; TUNNEL_URL_FILE="$RUN_DIR/tunnel.url"

echo "주소 펴기"
check "맨 IP 에 우리 포트를 붙인다"      "$(normalize_server_url 192.168.0.7)"          "http://192.168.0.7:$PORT"
check "적어 준 포트를 존중한다"          "$(normalize_server_url 192.168.0.7:5010)"     "http://192.168.0.7:5010"
check "스킴까지 적었으면 그대로 둔다"    "$(normalize_server_url https://lab.example)"  "https://lab.example"
check "끝의 / 를 뗀다"                   "$(normalize_server_url http://10.0.0.2:5003/)" "http://10.0.0.2:5003"
check "경로가 있으면 포트를 넣지 않는다" "$(normalize_server_url lab.example/bml)"      "http://lab.example/bml"
check "빈 값은 빈 값이다"                "$(normalize_server_url '')"                   ""

echo
echo "다른 기계가 칠 수 있는 주소 고르기"
# 실제로 겪은 목록.  169.254.x 가 맨 앞이라 `hostname -I | awk '{print $1}'`
# 이 그것을 골랐고, 노트북에서는 끝내 안 열렸다.
check "169.254.x 를 고르지 않는다" \
  "$(reachable_addresses '169.254.83.107 192.168.0.40 192.168.56.1' | tr '\n' ' ')" "lan 192.168.0.40 "
check "VirtualBox 호스트 전용을 버린다" "$(reachable_addresses '192.168.56.1')" ""
check "루프백을 버린다"                 "$(reachable_addresses '127.0.0.1')"     ""
# 도커 브리지와 WSL NAT 이 같은 대역이다.  둘 다 그 PC 안에서만 통한다.
check "172.17.x 를 버린다"              "$(reachable_addresses '172.17.0.1')"    ""
check "172.28.x 를 버린다"              "$(reachable_addresses '172.28.144.1')"  ""
check "10.x 는 남긴다"                  "$(reachable_addresses '10.0.1.5')"      "lan 10.0.1.5"
check "하나도 없으면 빈 값"             "$(reachable_addresses '127.0.0.1 169.254.1.2')" ""
# 두 사람이 다른 공유기에 있으면 이것만 통한다.  LAN 만 찍으면 안 알려 주게 된다.
check "사설망 100.64/10 을 남긴다"      "$(reachable_addresses '100.118.47.60')" "vpn 100.118.47.60"
check "공인 100.x 는 사설망이 아니다"   "$(reachable_addresses '100.20.1.1')"    ""
check "100.127.x 까지가 사설망이다"     "$(reachable_addresses '100.127.0.1')"   "vpn 100.127.0.1"
check "100.128.x 는 아니다"             "$(reachable_addresses '100.128.0.1')"   ""

echo
echo "실제로 열려 있는 곳"
# `.bml/env` 를 나중에 넣고 서버를 안 내리면 설정과 실제가 어긋난다.
SS_ALL="LISTEN 0 2048 0.0.0.0:$PORT 0.0.0.0:*"
SS_LOCAL="LISTEN 0 2048 127.0.0.1:$PORT 0.0.0.0:*"
check "0.0.0.0 이면 전체"        "$(listening_scope "$SS_ALL")"                  "all"
check "127.0.0.1 이면 이 기계뿐" "$(listening_scope "$SS_LOCAL")"                "local"
check "[::] 도 전체다"           "$(listening_scope "LISTEN 0 128 [::]:$PORT")"  "all"
check "*:포트 도 전체다"         "$(listening_scope "LISTEN 0 128 *:$PORT")"     "all"
# ss 가 없거나 서버가 안 떠 있으면 모른다고 해야 한다 — 모르는 것을 '이 기계뿐'
# 으로 읽으면 멀쩡한 설정에 경고가 붙는다.
check "안 떠 있으면 모른다"      "$(listening_scope "")"                         "unknown"
check "다른 포트에 속지 않는다"  "$(listening_scope "LISTEN 0 128 0.0.0.0:22")"  "unknown"

echo
echo ".bml/env 고쳐 쓰기"
printf 'WORKBENCH_DATA=/mnt/d/bml-data\nWORKBENCH_HOST=0.0.0.0\n' > "$RUN_DIR/env"
write_env_key WORKBENCH_SERVER "http://10.0.0.9:5003"
check "적힌다" "$(grep -c '^WORKBENCH_SERVER=http://10.0.0.9:5003$' "$RUN_DIR/env")" "1"
# 데이터 경로를 날리면 중추 서버가 다음 실행에서 빈 data/ 를 새로 만든다.
check "다른 줄은 그대로다" "$(grep -c '^WORKBENCH_DATA=/mnt/d/bml-data$' "$RUN_DIR/env")" "1"

write_env_key WORKBENCH_SERVER "http://10.0.0.10:5003"
check "두 번 적어도 한 줄이다" "$(grep -c '^WORKBENCH_SERVER=' "$RUN_DIR/env")" "1"

write_env_key WORKBENCH_SERVER ""
check "빈 값이면 줄이 사라진다" "$(grep -c '^WORKBENCH_SERVER=' "$RUN_DIR/env")" "0"
check "지운 뒤에도 다른 줄은 남는다" "$(grep -c '^WORKBENCH_HOST=0.0.0.0$' "$RUN_DIR/env")" "1"

echo
echo ".bml/env 저장이 실패할 때"
# 예전에는 어느 단계가 실패해도 조용히 넘어가서, 부르는 쪽이 "저장했습니다" 를
# 출력하고 0 으로 끝났다.  사용자는 보호됐다고 믿는데 서버에는 옛 암호(또는
# 무암호)가 그대로 남았다.  실패 지점마다 하나씩 찔러 본다.
#
# 권한(chmod)으로 막지 않는다 -- 이 시험은 root 로도 돌기 때문이다.  함수를
# 갈아 끼워 그 단계만 실패시키면 누가 돌리든 같은 경로를 지난다.
ENV_GOOD='WORKBENCH_DATA=/mnt/d/bml-data
WORKBENCH_PASSWORD=옛날암호'

reset_env() { printf '%s\n' "$ENV_GOOD" > "$RUN_DIR/env"; }

reset_env
mv() { return 1; }
write_env_key WORKBENCH_PASSWORD "새암호1234" && rc=0 || rc=1
unset -f mv
check "mv 가 실패하면 실패를 돌려준다" "$rc" "1"
check "그때 원본은 그대로다" "$(grep -c '^WORKBENCH_PASSWORD=옛날암호$' "$RUN_DIR/env")" "1"
check "임시 파일을 남기지 않는다" "$(find "$RUN_DIR" -maxdepth 1 -name 'env.*' | wc -l | tr -d ' ')" "0"

reset_env
chmod() { return 1; }
write_env_key WORKBENCH_PASSWORD "새암호1234" && rc=0 || rc=1
unset -f chmod
# 누구나 읽을 수 있는 암호는 없는 암호보다 나쁘다 -- 있다고 믿게 되므로.
check "권한을 못 걸면 저장하지 않는다" "$rc" "1"
check "그때도 원본은 그대로다" "$(grep -c '^WORKBENCH_PASSWORD=옛날암호$' "$RUN_DIR/env")" "1"

reset_env
grep() { command grep "$@" >/dev/null 2>&1; return 2; }   # 읽기 오류
write_env_key WORKBENCH_SERVER "http://10.0.0.9:5003" && rc=0 || rc=1
unset -f grep
# 그냥 진행하면 새 key 하나만 든 파일이 원본을 갈아치워, WORKBENCH_DATA 와
# 기존 암호가 통째로 사라진다.
check "기존 파일을 못 읽으면 갈아치우지 않는다" "$rc" "1"
check "다른 설정이 살아 있다" "$(grep -c '^WORKBENCH_DATA=/mnt/d/bml-data$' "$RUN_DIR/env")" "1"

# grep 이 1 을 내는 것(남은 줄이 없음)은 실패가 아니다.  이것까지 실패로 읽으면
# 한 줄짜리 env 를 고칠 수 없다.
printf 'WORKBENCH_SERVER=http://old:5003\n' > "$RUN_DIR/env"
write_env_key WORKBENCH_SERVER "http://new:5003" && rc=0 || rc=1
check "남은 줄이 없는 것은 실패가 아니다" "$rc" "0"
check "그래도 새 값이 적힌다" "$(grep -c '^WORKBENCH_SERVER=http://new:5003$' "$RUN_DIR/env")" "1"

# 여기서는 함수를 갈아 끼우지 않는다.  `need_run_dir` 은 **우리 함수**라,
# 셰임을 씌운 뒤 `unset -f` 하면 원본까지 같이 사라진다 -- 그 뒤의 모든
# write_env_key 가 "command not found"(127) 로 실패한다.  실제로 그렇게
# 뒤쪽 시험 두 개가 엉뚱하게 깨졌다.  대신 만들 수 없는 경로를 준다.
reset_env
saved_run_dir="$RUN_DIR"; RUN_DIR=/dev/null/nope
write_env_key WORKBENCH_PASSWORD "새암호1234" && rc=0 || rc=1
RUN_DIR="$saved_run_dir"
check "설정 폴더를 못 만들면 실패를 돌려준다" "$rc" "1"
check "그 뒤에도 저장이 멀쩡하다" \
  "$(reset_env; write_env_key WORKBENCH_SERVER http://x:1 && echo ok || echo no)" "ok"

echo
echo "부르는 쪽이 그 실패를 본다"
# 조용히 넘어가면 "공유 암호를 저장했습니다" 를 출력하고 0 으로 끝난다.
reset_env
mv() { return 1; }
out="$( WORKBENCH_PASSWORD="" cmd_password "새암호1234" 2>&1 )" && rc=0 || rc=1
unset -f mv
check "cmd_password 가 0 으로 끝나지 않는다" "$rc" "1"
check "저장했다고 말하지 않는다" \
  "$(case "$out" in *"저장했습니다"*) echo yes ;; *) echo no ;; esac)" "no"
check "무엇이 잘못됐는지 말한다" \
  "$(case "$out" in *"저장하지 못했습니다"*) echo yes ;; *) echo no ;; esac)" "yes"

reset_env
mv() { return 1; }
out="$( WORKBENCH_HOST="" cmd_host local 2>&1 )" && rc=0 || rc=1
unset -f mv
check "cmd_host 도 0 으로 끝나지 않는다" "$rc" "1"
check "공개 범위를 바꿨다고 말하지 않는다" \
  "$(case "$out" in *"저장하지 못했습니다"*) echo yes ;; *) echo no ;; esac)" "yes"

# 실제 권한으로도 한 번 -- root 가 아니면.
if [ "$(id -u)" -ne 0 ]; then
  reset_env
  chmod 500 "$RUN_DIR"
  write_env_key WORKBENCH_PASSWORD "새암호1234" && rc=0 || rc=1
  chmod 700 "$RUN_DIR"
  check "읽기 전용 폴더에서도 실패를 돌려준다" "$rc" "1"
else
  printf '  skip 읽기 전용 폴더 시험 (root 로는 권한이 안 먹는다)\n'
fi

echo
echo "살아 있는 서버 판정"
# /api/health 가 200 을 주는 최소 서버.  파일 하나면 된다.
mkdir -p "$TMP/www/api" && printf 'ok' > "$TMP/www/api/health"
# 포트는 커널이 고르게 하고(0), 고른 값을 파일로 알려 준다.  기동 로그를
# 긁어서 알아내면 버퍼링에 따라 가끔 비어 있다 — 그러면 이 파일 전체가
# 아무 이유 없이 실패한 것처럼 보인다.
python3 - "$TMP/www" "$TMP/port" >/dev/null 2>&1 <<'PYSRV' &
import functools, http.server, sys
root, portfile = sys.argv[1], sys.argv[2]
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=root)
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
with open(portfile, "w") as fh:
    fh.write(str(srv.server_address[1]))
srv.serve_forever()
PYSRV
SERVER_PID=$!
LIVE=""
for _ in $(seq 1 50); do
  [ -s "$TMP/port" ] && LIVE="$(cat "$TMP/port")" && break
  sleep 0.1
done
if [ -n "$LIVE" ]; then
  check "응답하는 주소를 알아본다" "$(server_alive "http://127.0.0.1:$LIVE" && echo yes || echo no)" "yes"

  # 확인이 끝난 뒤에만 적는다.
  : > "$RUN_DIR/env"
  ( WORKBENCH_WAIT=1 BML_NO_OPEN=1 cmd_use "127.0.0.1:$LIVE" >/dev/null 2>&1 )
  check "닿는 주소는 저장된다" "$(grep -c "^WORKBENCH_SERVER=http://127.0.0.1:$LIVE$" "$RUN_DIR/env")" "1"
else
  fail=$((fail + 1)); printf '  FAIL 시험용 서버를 못 띄웠다\n'
fi

  check "살아 있으면 바로 통과한다" \
    "$(wait_until_alive "http://127.0.0.1:$LIVE" 10 && echo yes || echo no)" "yes"

# 닫힌 포트.  curl 은 기다리지 않고 바로 거절당한다.
check "안 닿는 주소는 거절한다" "$(server_alive 'http://127.0.0.1:1' && echo yes || echo no)" "no"

: > "$RUN_DIR/env"
( WORKBENCH_WAIT=1 BML_NO_OPEN=1 cmd_use "127.0.0.1:1" >/dev/null 2>&1 )
check "안 닿는 주소는 저장하지 않는다" "$(grep -c '^WORKBENCH_SERVER=' "$RUN_DIR/env")" "0"

echo
echo "안 닿을 때의 안내"
# 터널 주소에 방화벽·포트포워딩 안내를 주면, 아무 상관 없는 것을 확인하느라
# 시간을 쓴다.  실제로 그렇게 한참 돌았다.
# 터널 판정은 **도메인**으로 한다.  예전에는 아무 https 나 터널로 봐서, 오타
# 하나에도 "bml share stop 후 다시" 를 시켰다 (열지도 않은 터널을 닫으라는 말).
# 그래서 이 시험도 진짜 제공자 도메인을 쓴다.  코드는 000 으로 고정한다 —
# 여기서 보려는 것은 '어느 안내로 가는가' 이지 그 주소의 상태가 아니다.
help_lan="$(server_unreachable_help 'http://192.168.0.40:5003' 2>&1)"
help_tunnel="$( http_code_of() { printf '000'; }; server_unreachable_help 'https://a.lhr.life' 2>&1 )"
check "LAN 주소에는 방화벽을 말한다" \
  "$(case "$help_lan" in *"방화벽"*) echo yes ;; *) echo no ;; esac)" "yes"
check "터널 주소에는 bml share 를 말한다" \
  "$(case "$help_tunnel" in *"bml share"*) echo yes ;; *) echo no ;; esac)" "yes"
check "터널 주소에는 방화벽을 말하지 않는다" \
  "$(case "$help_tunnel" in *"New-NetFirewallRule"*) echo no ;; *) echo yes ;; esac)" "yes"
# "응답하지 않습니다" 만으로는 오타·터널 닫힘·방화벽·엉뚱한 서버를 구분할 수 없다.
check "curl 이 뭐라 했는지 보여 준다" \
  "$(case "$help_tunnel" in *"curl 이 말한 것"*) echo yes ;; *) echo no ;; esac)" "yes"

echo
echo "기다리는 것은 횟수가 아니라 시간이다"
# 아직 안 붙은 터널은 530 을 곧바로 돌려준다.  횟수로 세면 "다섯 번 해 봤다"
# 가 실제로는 7초고, 준비 중인 터널을 우리가 먼저 죽인다 — 실제로 그랬다.
started=$SECONDS
wait_until_alive "http://127.0.0.1:1" 6 && waited=-1 || waited=$((SECONDS - started))
check "포기하기 전에 준 시간만큼 기다린다" "$([ "$waited" -ge 6 ] && echo yes || echo no)" "yes"
check "영원히 붙잡고 있지는 않는다"       "$([ "$waited" -lt 20 ] && echo yes || echo no)" "yes"

echo
echo "터널 주소 꺼내기"
# 못 꺼내면 터널은 떠 있는데 아무도 못 들어온다 — 열려 있다고 믿고 안 끈다.
CF_LOG="2026-08-21T04:00:00Z INF +------------------------------+
2026-08-21T04:00:00Z INF |  https://odd-lamp-9k2.trycloudflare.com  |
2026-08-21T04:00:00Z INF +------------------------------+"
check "여러 줄에서 주소만 꺼낸다" "$(tunnel_url_from "$CF_LOG")" "https://odd-lamp-9k2.trycloudflare.com"
check "아직 안 나왔으면 빈 값"    "$(tunnel_url_from 'INF Starting tunnel')" ""
# 로그에는 문서 링크도 같이 나온다.  그걸 주소로 찍으면 상대는 클라우드플레어
# 문서를 열고 "안 열리는데요" 라고 한다.
check "다른 도메인은 안 집는다"   "$(tunnel_url_from 'see https://developers.cloudflare.com/x')" ""
# localhost.run 은 접속 안내에 관리 페이지 주소를 같이 찍는다.  그것을 알려
# 주면 상대는 남의 관리 화면을 연다.
LHR_LOG="Welcome to localhost.run!
To set up and manage custom domains go to https://admin.localhost.run/
6f8a1234.lhr.life tunneled with tls termination, https://6f8a1234.lhr.life"
check "localhost.run 주소를 꺼낸다"     "$(tunnel_url_from "$LHR_LOG")" "https://6f8a1234.lhr.life"
check "관리 페이지를 주소로 안 집는다"  "$(tunnel_url_from 'https://admin.localhost.run/')" ""

echo
echo "공유 암호"
: > "$RUN_DIR/env"
( WORKBENCH_PASSWORD="" cmd_password "$(printf 'abc\ndef')" >/dev/null 2>&1 )
check "줄바꿈이 든 암호는 저장하지 않는다" "$(grep -c '^WORKBENCH_PASSWORD=' "$RUN_DIR/env")" "0"
: > "$RUN_DIR/env"
( WORKBENCH_PASSWORD="" cmd_password "짧다" >/dev/null 2>&1 )
check "너무 짧으면 저장하지 않는다" "$(grep -c '^WORKBENCH_PASSWORD=' "$RUN_DIR/env")" "0"
# 한글 두 글자는 여섯 '바이트' 다.  ${#var} 로 세면 로케일에 따라 통과한다.
: > "$RUN_DIR/env"
( WORKBENCH_PASSWORD="" cmd_password "암호" >/dev/null 2>&1 )
check "한글도 글자 수로 센다"       "$(grep -c '^WORKBENCH_PASSWORD=' "$RUN_DIR/env")" "0"
# .bml/env 는 KEY=VALUE 다.  '=' 가 든 암호는 잘려서 저장되고, 그러면 사용자가
# 아는 암호로는 영영 안 열린다.
: > "$RUN_DIR/env"
( WORKBENCH_PASSWORD="" cmd_password "abc=defgh" >/dev/null 2>&1 )
check "'=' 가 들면 저장하지 않는다" "$(grep -c '^WORKBENCH_PASSWORD=' "$RUN_DIR/env")" "0"
: > "$RUN_DIR/env"
( WORKBENCH_PASSWORD="" cmd_password "건식전극2026" >/dev/null 2>&1 )
check "쓸 만한 암호는 저장된다"     "$(grep -c '^WORKBENCH_PASSWORD=건식전극2026$' "$RUN_DIR/env")" "1"
# 실험실 공용 PC 의 기본 umask 로는 누구나 읽을 수 있는 파일이 된다.
check "암호가 든 파일은 나만 읽는다" "$(stat -c '%a' "$RUN_DIR/env" 2>/dev/null)" "600"

echo
echo "터널 프로그램 찾기"
# 경로를 stdout 으로 돌려주면 진행 표시가 그 변수로 들어가 실행이 깨진다.
# 실제로 그렇게 됐고, 화면에는 "터널 주소를 받지 못했습니다" 만 떴다.
mkdir -p "$RUN_DIR/bin"
printf '#!/bin/sh\n' > "$RUN_DIR/bin/cloudflared"
chmod +x "$RUN_DIR/bin/cloudflared"
# PATH 를 비워 두고 부른다 — 이 기계에 cloudflared 가 이미 깔려 있으면
# 그쪽이 이겨서 받아 둔 것을 쓰는 경로를 시험하지 못한다.
mkdir -p "$TMP/emptybin"
SAVED_PATH="$PATH"; PATH="$TMP/emptybin"
CLOUDFLARED=""
# 여기서 `$(ensure_cloudflared)` 로 부르면 안 된다.  서브셸에서 값이 정해지고
# 부모는 빈 값을 들고 간다 — 지금 고치는 버그가 바로 그것이었다.
ensure_cloudflared >"$TMP/ensure.out" 2>/dev/null
PATH="$SAVED_PATH"
check "경로가 변수로 온다"     "$CLOUDFLARED" "$RUN_DIR/bin/cloudflared"
check "그 경로가 실행 가능하다" "$([ -x "$CLOUDFLARED" ] && echo yes || echo no)" "yes"
check "값을 찍지 않는다"       "$(cat "$TMP/ensure.out")" ""

echo
echo "터널은 창을 닫아도 살아 있어야 한다"
# 창에 매달아 두면 Ctrl-C 나 창 닫기로 터널이 죽고, 주소를 받은 사람은
# Cloudflare 오류 1033 을 본다 — "닫혔다" 가 아니라 "고장 났다" 로 읽힌다.
# 명령줄이 우리 터널처럼 보여야 소유로 친다.  PID 는 재사용되므로 살아 있다는
# 것만으로 죽이면 남의 프로세스를 그룹째 죽일 수 있다 (CLAUDE.md §0.8).
check "우리 터널의 명령줄을 알아본다" \
  "$(looks_like_our_tunnel "cloudflared tunnel --no-autoupdate --url $URL" && echo yes || echo no)" "yes"
check "SSH 터널도 우리 것이다" \
  "$(looks_like_our_tunnel "ssh -T -o StrictHostKeyChecking=accept-new -R 80:localhost:$PORT nokey@localhost.run" && echo yes || echo no)" "yes"
check "남의 포트를 넘기는 ssh 는 우리 것이 아니다" \
  "$(looks_like_our_tunnel "ssh -T -R 80:localhost:9999 nokey@localhost.run" && echo yes || echo no)" "no"
check "남의 cloudflared 는 우리 것이 아니다" \
  "$(looks_like_our_tunnel "cloudflared tunnel --url http://localhost:9999" && echo yes || echo no)" "no"
check "아무 프로세스나 우리 것이 아니다" \
  "$(looks_like_our_tunnel "python3 -m long_experiment" && echo yes || echo no)" "no"
check "빈 명령줄은 우리 것이 아니다" \
  "$(looks_like_our_tunnel "" && echo yes || echo no)" "no"

# 살아 있지만 우리 것이 아닌 pid — 죽이면 안 된다.
sleep 300 &
STRANGER=$!
echo "$STRANGER" > "$TUNNEL_PID_FILE"
printf 'https://someone-else.trycloudflare.com' > "$TUNNEL_URL_FILE"
check "남의 pid 는 열려 있는 것으로 안 친다" "$(tunnel_running && echo yes || echo no)" "no"
close_tunnel >/dev/null 2>&1
sleep 0.3
check "남의 pid 를 죽이지 않는다" "$(kill -0 "$STRANGER" 2>/dev/null && echo yes || echo no)" "yes"
kill "$STRANGER" 2>/dev/null

# 이제 진짜 우리 것처럼 보이는 프로세스로.
bash -c "exec -a \"cloudflared tunnel --no-autoupdate --url $URL\" sleep 300" &
FAKE_TUNNEL=$!
echo "$FAKE_TUNNEL" > "$TUNNEL_PID_FILE"
printf 'https://fake-tunnel.trycloudflare.com' > "$TUNNEL_URL_FILE"
check "열려 있는 것을 알아본다"  "$(tunnel_running && echo yes || echo no)" "yes"
check "주소를 기억한다"          "$(tunnel_url)" "https://fake-tunnel.trycloudflare.com"
check "닫으면 닫혔다고 한다"     "$(close_tunnel && echo yes || echo no)" "yes"
sleep 0.3
check "프로세스가 실제로 죽는다" "$(kill -0 "$FAKE_TUNNEL" 2>/dev/null && echo no || echo yes)" "yes"
check "주소 파일도 지운다"       "$([ -e "$TUNNEL_URL_FILE" ] && echo no || echo yes)" "yes"
check "두 번 닫으면 닫을 게 없다" "$(close_tunnel && echo yes || echo no)" "no"
# 7844 가 막힌 망에서는 cloudflared 가 어떤 --protocol 로도 못 붙는다.
# 그때 SSH 로 넘어가지 않으면 그 망에서는 공유 자체가 불가능해진다.
#
# **네 자리다.**  `bml share now` (설정을 둔 채 한 번만 랜덤으로), 자동
# 판별에서 7844 가 막혔을 때, Cloudflare 를 시도했는데 안 됐을 때, 그리고
# 2026-08-27 에 붙은 것: `bml share cf` 를 골라 뒀는데 **cloudflared 를 준비
# 못 한** 경우 (Codex #13).  예전에는 갈래를 고르기 전에 무조건 받고 실패하면
# 죽었으므로 이 자리가 아예 없었다.
check "cloudflare 가 안 되면 SSH 로 넘어간다" \
  "$(sed -n '/^cmd_share()/,/^}/p' "$BML" | grep -c 'tunnel_via_ssh')" "4"
# 주소는 받았는데 확인이 안 된 것을 실패로 치고 죽여 버리면, 사람이 그 주소를
# 손으로 찔러 볼 수도 없다 — 실제로 그래서 원인을 못 찾았다.
check "마지막 시도는 확인이 안 돼도 남긴다" \
  "$(sed -n '/^cmd_share()/,/^}/p' "$BML" | grep -c 'tunnel_via_ssh 1')" "4"
check "확인 실패(2)를 실패(1)와 구분한다" \
  "$(sed -n '/^cmd_share()/,/^}/p' "$BML" | grep -c 'rc" -eq 2')" "1"
# 서버 없이 남은 터널은 남에게 오류 화면을 띄우는 주소일 뿐이다.
check "bml stop 이 터널도 닫는다" \
  "$(sed -n '/^cmd_stop()/,/^}/p' "$BML" | grep -c close_tunnel)" "1"

echo
echo "암호 없이는 바깥에 열지 않는다"
# 로그인이 없는 앱을 인터넷에 올리는 일이라, 이 판정이 무너지면 되돌릴 수 없다.
out="$(WORKBENCH_PASSWORD= BML_NO_OPEN=1 "$BML" share 2>&1)"
check "share 가 거절한다"     "$(case "$out" in *"공유 암호가 없어서"*) echo yes ;; *) echo no ;; esac)" "yes"
check "무엇을 하라는지 말한다" "$(case "$out" in *"bml password"*) echo yes ;; *) echo no ;; esac)" "yes"

echo
echo "중추 서버가 정해져 있으면 자기 서버를 안 띄운다"
# 데이터 폴더가 없는 채로 부른다.  자기 서버를 띄우려 했다면 guard_data_dir 가
# "데이터 폴더가 없습니다" 로 죽는다 — 그 메시지가 나오면 분기를 안 탄 것이다.
out="$(WORKBENCH_SERVER=http://127.0.0.1:1 WORKBENCH_DATA="$TMP/없는폴더" \
       WORKBENCH_WAIT=1 BML_NO_OPEN=1 "$BML" 2>&1)"
check "중추 서버 이야기를 한다"      "$(case "$out" in *"중추 서버"*) echo yes ;; *) echo no ;; esac)" "yes"
check "자기 데이터 폴더를 안 찾는다" "$(case "$out" in *"데이터 폴더가 없습니다"*) echo no ;; *) echo yes ;; esac)" "yes"
check "빈 data/ 를 만들지 않는다"    "$([ -d "$TMP/없는폴더" ] && echo no || echo yes)" "yes"

echo
echo "중추 서버 주소가 이 기계 자신을 가리키는 경우"
# 실제로 막힌 자리 (2026-08-24): 이 설정이 걸려 있으면 bml 은 서버를 띄우지도
# 빌드하지도 않고 브라우저만 연다.  이미 떠 있던 옛 서버가 계속 응답하므로
# 화면은 멀쩡하고, git pull 을 받아도 화면이 그대로다 — "restart 했는데 안
# 바뀐다" 가 이렇게 나온다.  판정이 조용히 틀리면 안내도 같이 사라진다.
PORT=5003
check "localhost 는 이 기계다"  "$(server_is_this_machine http://localhost:5003 && echo yes || echo no)" "yes"
check "127.0.0.1 도 이 기계다"  "$(server_is_this_machine http://127.0.0.1:5003 && echo yes || echo no)" "yes"
# 포트가 다르면 다른 서비스다 — 같은 기계라도 우리 것이 아니다.
check "포트가 다르면 아니다"    "$(server_is_this_machine http://localhost:9999 && echo yes || echo no)" "no"
# 남의 기계는 당연히 아니다.  여기서 yes 가 나오면 멀쩡한 설정에 헛경고가 뜬다.
check "남의 LAN 주소는 아니다"  "$(server_is_this_machine http://192.0.2.7:5003 && echo yes || echo no)" "no"
check "빈 주소는 아니다"        "$(server_is_this_machine "" && echo yes || echo no)" "no"
# IPv6 리터럴이 대괄호째 들어와도 호스트와 포트를 갈라야 한다.
check "IPv6 루프백도 이 기계다" "$(server_is_this_machine 'http://[::1]:5003' && echo yes || echo no)" "yes"

echo
echo "NAT 뒤 WSL 주소 뽑기 (netsh connectaddress= 에 들어가는 값)"
# 이 값 하나를 사람이 손으로 옮겨 적어야 해서, 가이드가 경고해 둔 대로
# 자리표시자째 붙여넣는 사고가 실제로 난다.  bml 이 알고 있으니 대신 넣어 준다.
check "172.x 를 뽑는다"          "$(wsl_nat_address '172.28.144.1')" "172.28.144.1"
check "여러 개면 사설망 먼저"     "$(wsl_nat_address '172.28.144.1 10.0.0.5')" "172.28.144.1"
check "10.x 도 사설망이다"        "$(wsl_nat_address '10.0.0.5')" "10.0.0.5"
# 169.254 는 DHCP 를 못 받았다는 뜻이다.  이걸 넘겨 주면 포워딩은 걸리지만
# 아무것도 안 지나가고, 사람은 방화벽을 의심한다.
check "169.254 는 건너뛴다"       "$(wsl_nat_address '169.254.83.107 172.20.5.3')" "172.20.5.3"
# LAN 주소가 보이는 기계는 애초에 이 안내가 필요 없다 — 빈 값이어야 한다.
check "LAN 주소만 있으면 비운다"   "$(wsl_nat_address '192.168.0.40')" ""
check "빈 입력도 죽지 않는다"      "$(wsl_nat_address '')" ""

echo
echo "안내 화면 — 명령과 파일 내용을 섞지 않는다"
# 실제로 일어난 일: `bml status` 가 mirrored 안내에서 `.wslconfig` 의 두 줄을
# 붙여넣을 명령과 같은 초록으로 찍었다.  사람은 PowerShell 에 그대로
# 붙여넣었고 `'networkingMode=mirrored' 용어가 ... 인식되지 않습니다` 를 봤다.
# 오류 문구에 '파일' 이라는 말이 없어서, 화면을 준 우리 말고는 원인을 알 수 없다.
NAT_HINT="$(nat_hint '172.28.144.1')"

# 파일 내용은 반드시 │ 를 달고 나온다.  들여쓰기만 벗기면 명령과 똑같아지는
# 줄이 하나라도 있으면 같은 사고가 다시 난다.
check "파일 내용이 맨줄로 새지 않는다" \
  "$(printf '%s\n' "$NAT_HINT" | sed 's/^[[:space:]]*//' \
     | grep -c -x -e '\[wsl2\]' -e 'networkingMode=mirrored')" "0"
check "파일 내용에는 │ 가 붙는다" \
  "$(printf '%s\n' "$NAT_HINT" | grep -c '│ \[wsl2\]')" "1"

# 그리고 사람이 손으로 파일을 만들지 않도록, 그 일을 하는 명령을 준다.
# 이 화면을 읽는 사람은 WSL 터미널 앞에 앉아 있다 — 창을 옮기게 하지 않는다.
check "mirrored 를 켜는 명령이 화면에 있다" \
  "$(printf '%s\n' "$NAT_HINT" | grep -c 'bml mirrored')" "1"

# 붙여넣기는 한 번에 끝나야 한다.  줄이 갈리면 PowerShell 은 오류도 없이
# 다음 줄을 기다리기만 하고, 사람은 명령이 먹은 줄 안다.
check "그 명령은 한 줄이다" "$(wslconfig_mirror_command | wc -l | tr -d ' ')" "1"
check "그 명령이 넣는 값"   "$(wslconfig_mirror_command | grep -c 'networkingMode=mirrored')" "1"
# 이미 있는 .wslconfig 를 통째로 덮으면 memory·processors 설정이 사라진다.
# 읽고 → 있으면 그 자리를 고치고 → 없으면 넣는다, 이 순서가 깨지면 안 된다.
# 실제 PowerShell 7.4.6 으로 다섯 경우를 돌려 확인했다 (log.md 참고):
# 없던 파일 / [wsl2]+memory / 다른 절만 / networkingMode=NAT / 이미 mirrored.
# 인코딩을 명시하지 않으면 Windows PowerShell 5.1 의 Get-Content/Set-Content 가
# 기본 ANSI 로 읽고 써서, 한글이 든 .wslconfig 를 CP949 로 다시 쓴다.  cmdlet 을
# 피하고 .NET API 에 인코딩을 넘긴다.
check "인코딩을 명시한다"           "$(wslconfig_mirror_command | grep -cF 'UTF8Encoding($false)')" "1"
check "cmdlet 대신 .NET 으로 쓴다"  "$(wslconfig_mirror_command | grep -cF '[IO.File]::WriteAllText')" "1"
check "읽기도 .NET 으로"            "$(wslconfig_mirror_command | grep -cF '[IO.File]::ReadAllText')" "1"
# 링크면 멈춘다 — 무엇을 고치게 될지 알 수 없다.
check "링크면 멈춘다"               "$(wslconfig_mirror_command | grep -c 'LinkType')" "1"
# 백업은 없을 때만 만든다.  두 번째 실행이 첫 원본 백업을 덮으면 되돌릴 것이 사라진다.
check "기존 백업을 덮지 않는다"      "$(wslconfig_mirror_command | grep -cF 'not (Test-Path -LiteralPath "$f.bml-bak")')" "1"
# CRLF 파일에서 [ \t]*$ 는 \r 때문에 절대 안 맞는다 — 그러면 이미 mirrored 인
# 파일을 매번 다시 쓰고 백업까지 새로 만든다 (검증에서 실제로 걸렸다).
check "멱등 판정이 CR 을 본다"       "$(wslconfig_mirror_command | grep -cF 'mirrored[ \t]*\r?$')" "1"
check "NAT 이라고 적힌 줄을 바꾼다"   "$(wslconfig_mirror_command | grep -cF 'networkingMode[ \t]*=[^\r\n]*')" "1"
check "[wsl2] 절을 두 번 만들지 않는다" "$(wslconfig_mirror_command | grep -cF 'elseif($t -match')" "1"
# 줄바꿈을 CRLF 그대로 둔다.  `.*` 로 지우면 그 줄만 LF 가 되어 파일이 섞인다 —
# CRLF 가 섞인 파일이 어떤 얼굴로 나타나는지는 §0.5 가 이미 겪은 그대로다.
check "고친 줄의 CRLF 를 먹지 않는다"   "$(wslconfig_mirror_command | grep -cF '[^\r\n]*')" "1"

# B 안내는 우리가 아는 172.x 를 실제로 채워야 한다.  자리표시자가 남으면
# `구문이 올바르지 않습니다` 가 나고, 그 문구는 주소 얘기를 하지 않는다.
check "netsh 줄에 진짜 주소가 들어간다" \
  "$(printf '%s\n' "$NAT_HINT" | grep -c 'connectaddress=172.28.144.1')" "1"
# 주소를 모르면 아는 척하지 않는다 (§0.4).
check "모르면 자리표시자를 남긴다" \
  "$(nat_hint '' | grep -c 'connectaddress=<그 172.x>')" "1"
check "모를 때 빈 connectaddress 를 주지 않는다" \
  "$(nat_hint '' | grep -c 'connectaddress=$')" "0"

# 화면과 가이드가 서로 다른 한 줄을 주면, 둘 중 어느 것이 맞는지 아무도 모른다.
# 한쪽만 고치는 일이 실제로 잦아서 여기서 붙들어 둔다.
check "가이드에도 같은 한 줄이 있다" \
  "$(grep -cFx "$(wslconfig_mirror_command)" "$HERE/../../docs/guides/central-server.md")" "1"

# `bml feed` 도 같은 자리다 — docs/log.md 에 적을 줄은 명령이 아니다.
check "log.md 예시 줄도 파일 내용으로 찍는다" \
  "$(grep -c 'file_line "## \[' "$BML")" "1"


echo "WSL 쪽에서 .wslconfig 고치기 (bml mirrored)"
WSC="$TMP/wslconfig"; mkdir -p "$WSC"
# 파일 내용을 눈으로 보기 좋게 (CR 을 드러낸다).
seen() { sed -e 's/\r/<CR>/' "$1" | tr '\n' '|'; }

# 없던 파일: Windows 가 읽는 파일이니 CRLF 로 만든다.
f="$WSC/none"; wslconfig_set_mirrored "$f"
check "없던 파일을 CRLF 로 만든다" "$(seen "$f")" "[wsl2]<CR>|networkingMode=mirrored<CR>|"

# 이미 있는 설정을 지우면 그 기계의 메모리·CPU 설정이 조용히 사라진다.
f="$WSC/keep"; printf '[wsl2]\r\nmemory=8GB\r\nprocessors=4\r\n' > "$f"
wslconfig_set_mirrored "$f"
check "[wsl2] 절 안에 넣고 나머지를 살린다" "$(seen "$f")" \
  "[wsl2]<CR>|networkingMode=mirrored<CR>|memory=8GB<CR>|processors=4<CR>|"

# [wsl2] 가 없는 파일: 절째로 앞에 넣되 뒤에 있던 것은 그대로 둔다.
f="$WSC/other"; printf '[experimental]\r\nautoMemoryReclaim=gradual\r\n' > "$f"
wslconfig_set_mirrored "$f"
check "다른 절만 있으면 앞에 붙인다" "$(seen "$f")" \
  "[wsl2]<CR>|networkingMode=mirrored<CR>|[experimental]<CR>|autoMemoryReclaim=gradual<CR>|"

# NAT 이라고 적힌 파일에 두 줄을 더 얹고 끝나면, 사람은 켰다고 믿는데 안 켜져 있다.
f="$WSC/nat"; printf '[wsl2]\r\nnetworkingMode=NAT\r\nmemory=8GB\r\n' > "$f"
wslconfig_set_mirrored "$f"
check "NAT 이라고 적힌 줄을 바꾼다" "$(seen "$f")" \
  "[wsl2]<CR>|networkingMode=mirrored<CR>|memory=8GB<CR>|"

# 줄바꿈은 그 파일이 쓰던 것을 따른다.  Windows 가 읽는 파일에 LF 와 CRLF 를
# 섞어 놓는 것은 §0.5 로 이미 값을 치른 종류의 사고다.
f="$WSC/lf"; printf '[wsl2]\nmemory=8GB\n' > "$f"
wslconfig_set_mirrored "$f"
check "LF 파일에 CR 을 섞지 않는다" "$(seen "$f")" "[wsl2]|networkingMode=mirrored|memory=8GB|"

# 두 번 눌러도 안전해야 한다.  rc 1 은 "이미 되어 있어 손대지 않았다" 는 뜻이고,
# cmd_mirrored 는 그때 백업을 도로 지운다.
f="$WSC/twice"; wslconfig_set_mirrored "$f"
before="$(seen "$f")"; wslconfig_set_mirrored "$f"; rc=$?
check "이미 mirrored 면 손대지 않는다" "$rc" "1"
check "그때 내용도 그대로다"           "$(seen "$f")" "$before"

echo
echo "Windows 사용자 폴더 고르기 (짐작해서 남의 폴더에 쓰지 않는다)"
U="$TMP/Users"; mkdir -p "$U/Public" "$U/Default" "$U/윤홍" && : > "$U/desktop.ini"
check "시스템 폴더를 빼면 하나뿐" "$(windows_home_candidate "$U" nobody)" "$U/윤홍"
# 사람 폴더가 둘이면 이름이 맞는 쪽.  Windows 는 대소문자를 안 가린다.
mkdir -p "$U/Lab"
check "WSL 사용자 이름과 같은 폴더"  "$(windows_home_candidate "$U" lab)" "$U/Lab"
check "대소문자는 안 가린다"         "$(windows_home_candidate "$U" LAB)" "$U/Lab"
# 이름이 아무것도 안 맞으면 고르지 않는다 — 남의 폴더에 쓰는 것보다 낫다.
check "못 고르면 빈 값"              "$(windows_home_candidate "$U" nobody)" ""
# 다만 .wslconfig 가 이미 있는 폴더가 하나뿐이면 그것이 정답이다.
: > "$U/Lab/.wslconfig"
check ".wslconfig 가 있는 쪽을 고른다" "$(windows_home_candidate "$U" nobody)" "$U/Lab"
check "없는 폴더는 빈 값"              "$(windows_home_candidate "$TMP/nope" me)" ""


echo
echo "bml mirrored — 저장소 바깥 파일이라 증명된 것에만 손댄다"
FAKE="$TMP/winhome"; mkdir -p "$FAKE"
printf '[wsl2]\r\nnetworkingMode=NAT\r\nmemory=8GB\r\n' > "$FAKE/.wslconfig"
# 함수 재정의는 서브셸 안에만 남는다 — 뒤의 시험이 가짜를 물려받지 않는다.
# $1 은 재정의한 함수 안에서는 그 함수의 인자다 — 미리 잡아 둔다.
run_mirrored() { local h="$1"; ( is_wsl() { return 0; }; windows_home_verified() { printf '%s' "$h"; }; cmd_mirrored 2>&1 ); }
OUT="$(run_mirrored "$FAKE")"
check "고쳤다고 말한다"        "$(printf '%s\n' "$OUT" | grep -c '고쳤습니다')" "1"
check "어느 파일인지 먼저 밝힌다" "$(printf '%s\n' "$OUT" | grep -c "^대상.*$FAKE/.wslconfig")" "1"
check "실제로 mirrored 가 된다"  "$(grep -c '^networkingMode=mirrored' "$FAKE/.wslconfig")" "1"
check "고치기 전 파일을 남긴다"  "$(grep -c 'networkingMode=NAT' "$FAKE/.wslconfig.bml-bak")" "1"
check "다음 할 일을 준다"        "$(printf '%s\n' "$OUT" | grep -c -- '--shutdown')" "1"

# 두 번째 실행이 첫 실행의 백업을 없애면 되돌릴 것이 사라진다.  예전에는
# 백업을 먼저 뜨고 나중에 지워서, 두 번째 실행이 '이미 mirrored 인 파일' 로
# NAT 원본 백업을 덮었다.  이제 이미 되어 있으면 백업을 만들지도 지우지도 않는다.
OUT="$(run_mirrored "$FAKE")"
check "두 번째는 손대지 않는다"  "$(printf '%s\n' "$OUT" | grep -c '이미 mirrored')" "1"
check "첫 백업이 살아남는다"     "$(grep -c 'networkingMode=NAT' "$FAKE/.wslconfig.bml-bak")" "1"

# 지금 로그인한 Windows 사용자를 모르면 **아무것도 안 쓴다.**  '.wslconfig 가
# 하나뿐' 같은 짐작은 그 사용자라는 증거가 아니다 — 남의 파일을 고치게 된다.
BEFORE="$(cat "$FAKE/.wslconfig")"
OUT="$( is_wsl() { return 0; }; windows_home_verified() { printf ''; }; windows_home_candidate() { printf '%s' "$FAKE"; }; cmd_mirrored 2>&1 )"
check "사용자를 모르면 안 쓴다"   "$(printf '%s\n' "$OUT" | grep -c '짐작으로 파일을 고치지 않습니다')" "1"
check "그때 파일은 그대로다"      "$(cat "$FAKE/.wslconfig")" "$BEFORE"
check "짐작은 제안으로만 보여 준다" "$(printf '%s\n' "$OUT" | grep -c '아마 여기')" "1"
check "대신 PowerShell 한 줄을 준다" \
  "$(printf '%s\n' "$OUT" | grep -cF "$(wslconfig_mirror_command)")" "1"

# 심볼릭 링크를 따라가면 화면은 .wslconfig 를 고친다고 하면서 엉뚱한 파일을
# 덮어쓴다.  실제로 걸리는 모양: .wslconfig -> ~/.ssh/config
LINKHOME="$TMP/linkhome"; mkdir -p "$LINKHOME"
printf 'Host lab\n  User yonghoon\n' > "$TMP/ssh-config"
ln -s "$TMP/ssh-config" "$LINKHOME/.wslconfig"
SSHBEFORE="$(cat "$TMP/ssh-config")"
OUT="$(run_mirrored "$LINKHOME")"
check "링크면 손대지 않는다"      "$(printf '%s\n' "$OUT" | grep -c '심볼릭 링크')" "1"
check "링크가 가리킨 파일은 무사하다" "$(cat "$TMP/ssh-config")" "$SSHBEFORE"

# 백업 자리가 링크여도 마찬가지다 — 백업을 뜨는 순간 그쪽이 덮인다.
BAKHOME="$TMP/bakhome"; mkdir -p "$BAKHOME"
printf '[wsl2]\r\nmemory=8GB\r\n' > "$BAKHOME/.wslconfig"
printf 'keep me\n' > "$TMP/precious"
ln -s "$TMP/precious" "$BAKHOME/.wslconfig.bml-bak"
OUT="$(run_mirrored "$BAKHOME")"
check "백업 자리가 링크여도 멈춘다" "$(printf '%s\n' "$OUT" | grep -c '심볼릭 링크')" "1"
check "그 링크가 가리킨 파일도 무사" "$(cat "$TMP/precious")" "keep me"

# BOM 이 붙은 파일에 절을 앞에 붙이면 BOM 이 파일 한가운데로 간다.
BOMHOME="$TMP/bomhome"; mkdir -p "$BOMHOME"
printf '\xef\xbb\xbf[experimental]\r\nautoMemoryReclaim=gradual\r\n' > "$BOMHOME/.wslconfig"
BOMBEFORE="$(md5sum < "$BOMHOME/.wslconfig")"
OUT="$(run_mirrored "$BOMHOME")"
check "BOM 파일은 손대지 않는다"   "$(printf '%s\n' "$OUT" | grep -c 'BOM')" "1"
check "그 파일도 그대로다"        "$(md5sum < "$BOMHOME/.wslconfig")" "$BOMBEFORE"

echo
echo "모르는 명령 — 오타보다 '옛 bml' 이 흔하다"
# 실제로 일어난 일: 화면과 문서가 알려 준 `bml mirrored` 를 그대로 쳤는데
# `모르는 명령: mirrored` 가 났다.  그 기계의 bml 이 옛것이었을 뿐인데, 그
# 문구는 "네가 잘못 쳤다" 로 읽힌다.  이제 먼저 맞춰 보고, 그래도 없으면
# 가까운 이름을 짚는다.
check "목록을 case 라벨에서 뽑는다"   "$(known_commands | grep -c '^mirrored$')" "1"
check "안쪽 case 는 섞이지 않는다"    "$(known_commands | grep -c '^crlf$')" "0"
check "'*' 는 명령이 아니다"          "$(known_commands | grep -c '^\*$')" "0"

# 도움말에 적힌 명령이 실제로 붙어 있어야 한다.  한쪽만 고치는 일이 잦고,
# 그때 사람은 문서를 그대로 따라 하다 오늘과 같은 화면을 본다.
MISSING=""
while read -r c; do
  known_commands | grep -qx -- "$c" || MISSING="$MISSING $c"
done < <(sed -n '3,30p' "$BML" | grep -oE '^#   bml [a-z-]+' | awk '{print $3}' | sort -u)
check "도움말의 명령이 전부 붙어 있다" "$MISSING" ""

check "오타에 가까운 것을 짚는다"     "$(suggest_commands mirrorred)" "mirror"
check "앞이 같으면 그것"              "$(suggest_commands stat)"      "status"
check "아무것도 안 닮았으면 빈 값"    "$(suggest_commands zzzz)"      ""

echo
echo "지금 이 서버에 문이 있는가"
# 설정에 암호가 있는 것과 떠 있는 서버가 그것을 들고 있는 것은 다르다.
# 적어 두고 restart 를 안 하면 문이 없는 채로 열려 있다.
check "401 이면 잠긴 것"            "$(door_state 401 '')"        "locked"
check "적어는 뒀는데 안 물으면"      "$(door_state 200 '암호')"     "pending"
check "암호가 없으면 열린 것"        "$(door_state 200 '')"        "open"
check "대답이 없으면 모르는 것"      "$(door_state 000 '암호')"     "unknown"
check "빈 코드도 모르는 것"          "$(door_state '' '')"         "unknown"

echo
echo "Windows 쪽 LAN 주소 읽기 (사람이 ipconfig 에서 골라 적던 자리)"
KO='Windows IP 구성

이더넷 어댑터 vEthernet (WSL):
   IPv4 주소 . . . . . . . . . : 172.24.25.206
   서브넷 마스크 . . . . . . . : 255.255.240.0

무선 LAN 어댑터 Wi-Fi:
   IPv4 주소 . . . . . . . . . : 192.168.0.40
   서브넷 마스크 . . . . . . . : 255.255.255.0
   기본 게이트웨이 . . . . . . : 192.168.0.1'
# 172.x 는 WSL NAT 이라 밖에서 못 쓴다.  그것을 불러 주면 노트북에서 영영 안 열린다.
check "WSL 의 172.x 를 고르지 않는다" "$(windows_lan_address "$KO")" "192.168.0.40"

EN='Windows IP Configuration

Ethernet adapter vEthernet (WSL):
   IPv4 Address. . . . . . . . . . . : 172.24.25.206
   Subnet Mask . . . . . . . . . . . : 255.255.240.0

Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . . . . . . . : 10.0.1.5
   Default Gateway . . . . . . . . . : 10.0.1.1'
# 'IPv4' 는 어느 언어의 Windows 에서도 번역되지 않는다 — 그래서 이 낱말로 잡는다.
check "영문 Windows 도 같다" "$(windows_lan_address "$EN")" "10.0.1.5"

# 가장 위험한 오답: 기본 게이트웨이(공유기)를 사람에게 불러 주는 것.  IP 처럼
# 생긴 것을 다 긁으면 그렇게 된다.  IPv4 줄만 보므로 걸리지 않는다.
check "게이트웨이를 고르지 않는다" \
  "$(windows_lan_address 'Wi-Fi:
   IPv4 주소 . . . : 192.168.0.40
   기본 게이트웨이 . : 192.168.0.1')" "192.168.0.40"
# 서브넷 마스크도 IP 처럼 생겼다.
check "서브넷 마스크도 고르지 않는다" \
  "$(windows_lan_address 'Wi-Fi:
   서브넷 마스크 . . : 255.255.255.0
   IPv4 주소 . . . : 192.168.0.40')" "192.168.0.40"
# 쓸 만한 것이 하나도 없으면 짐작하지 않는다 (§0.4).
check "WSL 것뿐이면 빈 값" \
  "$(windows_lan_address 'vEthernet (WSL):
   IPv4 주소 . . . : 172.24.25.206')" ""
check "빈 출력도 죽지 않는다" "$(windows_lan_address '')" ""

# drvfs 는 /mnt/c 의 모든 파일에 실행 비트를 붙인다.  그래서 interop 이 꺼져
# 있어도 `[ -x ipconfig.exe ]` 는 참이고, 실행하면 한 줄도 안 나온다.  그것을
# "부를 수는 있는데 쓸 주소가 없다" 로 읽으면 사람을 랜선 뽑혔나 보러 보낸다.
# 출력이 비면 못 부른 것이다 — 종료 코드로 갈라야 화면이 옳은 말을 한다.
windows_ipconfig >/dev/null 2>&1; rc=$?
check "못 부르면 실패로 알린다"  "$([ "$rc" -ne 0 ] && echo yes || echo no)" "yes"
# 실제로 걸린 것: /etc/wsl.conf 의 systemd=true 가 부팅 때 binfmt 등록을
# 정리하면서 WSL 의 WSLInterop 까지 지운다.  그 뒤 모든 .exe 가
# "cannot execute binary file: Exec format error" 로 죽는데, 그 문구에는
# systemd 도 WSL 도 interop 도 안 나온다.  이 저장소는 이제 .exe 에 기댄다
# (bml mirrored, LAN 주소 읽기) — doctor 가 짚어야 한다.
check "등록이 살아 있으면 ok"     "$(interop_state 'status register WSLInterop' 'enabled')" "ok"
check "등록만 사라졌으면 wiped"   "$(interop_state 'status register' '')"                   "wiped"
check "꺼져 있으면 disabled"      "$(interop_state 'status register WSLInterop' 'disabled')" "disabled"
# binfmt_misc 가 안 보이면 단정하지 않는다 (§0.4) — 다른 이유일 수 있다.
check "목록이 없으면 unknown"     "$(interop_state '' '')"                                  "unknown"
# 처음엔 /usr/lib/binfmt.d 에 파일만 두라고 안내했다가 실측에서 틀렸다:
#   systemd-binfmt.service ... skipped (ConditionVirtualization=!wsl)
# systemd 는 WSL 안에서 그 서비스를 건너뛴다.  그래서 파일을 아무리 잘 써 놔도
# 적용해 줄 사람이 없다.  지금 살리는 길은 커널에 직접 쓰는 것뿐이다.
check "지금 살리기는 커널에 직접"   "$(interop_repair_now | grep -c '/proc/sys/fs/binfmt_misc/register')" "1"
check "그것도 한 줄이다"            "$(interop_repair_now | wc -l | tr -d ' ')" "1"
check "등록 줄은 WSL 의 것과 같다"  "$(interop_repair_now | grep -c ':WSLInterop:M::MZ::/init:PF')" "1"
# 다음 부팅에도 살리려면 그 조건을 비워야 서비스가 돈다.
check "조건을 비우는 드롭인"        "$(interop_repair_persist | grep -c 'ConditionVirtualization=')" "1"
check "드롭인 자리"                 "$(interop_repair_persist | grep -c '/etc/systemd/system/systemd-binfmt.service.d')" "2"
check "그때 쓰일 파일도 만든다"      "$(interop_repair_persist | grep -c '/usr/lib/binfmt.d/WSLInterop.conf')" "1"
# printf 안의 \n 이 두 개로 새면 파일에 글자 그대로 \n 이 들어가고 유닛이 안 읽힌다.
check "줄바꿈 escape 가 안 샌다"    "$(interop_repair_persist | grep -c '\\\\n')" "0"

check "받은 것이 있으면 그대로"  "$(windows_ipconfig 'Wi-Fi:
   IPv4 주소 . . . : 10.1.2.3' | tail -1 | tr -d ' ')" "IPv4주소...:10.1.2.3"

# 실제로 걸린 것: 이 랩 망이 172.16-31 사설 대역을 쓴다.  대역만 보고 거르면
# (hostname -I 처럼 이름이 없을 때 하던 대로) 진짜 LAN 주소를 WSL NAT 으로
# 오해해서 버리고 "쓸 만한 것이 없습니다" 로 끝난다.  이름이 있으면 그럴
# 이유가 없다 — WSL 것은 어댑터에 vEthernet (WSL) 이라고 적혀 있다.
LAB172='이더넷 어댑터 vEthernet (WSL):
   IPv4 주소 . . . : 172.24.25.206

이더넷 어댑터 이더넷:
   IPv4 주소 . . . : 172.20.30.40
   기본 게이트웨이 . : 172.20.0.1'
check "랩 망이 172.x 여도 고른다"   "$(windows_lan_address "$LAB172")" "172.20.30.40"
check "그때도 WSL 것은 뺀다"        "$(windows_lan_address "$LAB172" | grep -c '172.24')" "0"
# 가상 어댑터는 이름으로 뺀다 — 대역이 겹쳐도 안전하다.
check "VirtualBox 어댑터를 뺀다" \
  "$(windows_lan_address '이더넷 어댑터 VirtualBox Host-Only Network:
   IPv4 주소 . . . : 192.168.56.1

이더넷 어댑터 Wi-Fi:
   IPv4 주소 . . . : 192.168.0.40')" "192.168.0.40"
# 어댑터별 목록 자체도 고정한다 — 화면이 "본 것" 으로 이것을 그대로 찍는다.
check "어댑터 이름과 주소를 짝지어 낸다" \
  "$(windows_ipv4_by_adapter "$LAB172" | tr '\t' '=' | tr '\n' ' ')" \
  "이더넷 어댑터 vEthernet (WSL)=172.24.25.206 이더넷 어댑터 이더넷=172.20.30.40 "

# 한국어 Windows 의 ipconfig 는 CP949 로 찍는다.  UTF-8 로케일의 grep 은 그런
# 바이트가 섞인 줄에서 매칭을 조용히 놓친다 — 주소는 ASCII 인데 같은 줄의
# '주소' 두 글자 때문에 못 찾는다.  그래서 바이트로만 본다.
CP949="$(printf 'Wi-Fi:\n   IPv4 \xc1\xd6\xbc\xd2 . . . : 192.168.0.40\n   \xb1\xe2\xba\xbb . : 192.168.0.1\n')"
check "CP949 로 찍혀도 읽는다" "$(LC_ALL=C.UTF-8 windows_lan_address "$CP949")" "192.168.0.40"

# PATH 에 Windows 가 안 붙은 기계가 있다 (/etc/wsl.conf 의 appendWindowsPath=false).
# 그때 `command -v ipconfig.exe` 는 빈손이고, 화면은 이유 없이 "못 찾았습니다"
# 로만 끝난다.  System32 를 직접 본다.
check "PATH 에 있으면 이름 그대로"  "$(win_exe bash)" "bash"
check "없는 것은 거부한다"          "$(win_exe nope-nope.exe || echo REFUSED)" "REFUSED"
check "빈 이름도 거부한다"          "$(win_exe '' || echo REFUSED)" "REFUSED"
# PATH 에 없을 때 System32 를 실제로 보는지 — 예전 시험은 가짜 폴더를 만들기만
# 하고 쓰지 않아, 이 분기를 지워도 통과했다 (Codex 리뷰의 테스트 지적).
FAKE32="$TMP/System32"; mkdir -p "$FAKE32"; : > "$FAKE32/onlyhere.exe"; chmod +x "$FAKE32/onlyhere.exe"
check "PATH 에 없으면 System32 를 본다" \
  "$(WIN_SYSTEM32="$FAKE32" win_exe onlyhere.exe)" "$FAKE32/onlyhere.exe"
# 실행 비트가 없으면 부를 수 없다 — 있는 척하면 안 된다.
: > "$FAKE32/notexec.exe"; chmod -x "$FAKE32/notexec.exe"
check "실행할 수 없으면 거부한다" \
  "$(WIN_SYSTEM32="$FAKE32" win_exe notexec.exe || echo REFUSED)" "REFUSED"

echo
echo "mirrored 를 켠 뒤의 포트 충돌 — bml stop 으로는 안 되는 경우"
# mirrored 네트워크에서는 WSL 이 Windows 의 망을 그대로 쓴다.  그래서 Windows
# 쪽이 잡은 5003 도 WSL 안에서 보이는데, 그것은 WSL 안에서 끌 수 없다.
# 그때 "bml stop 후 다시" 라고 하면 사람은 영영 안 되는 일을 반복한다.
BINDLOG="$TMP/bind.log"
printf 'ERROR: [Errno 98] error while attempting to bind on address: address already in use\n' > "$BINDLOG"
MINE="$( is_wsl() { return 0; }; owns_port() { return 0; }; explain_log "$BINDLOG" 2>&1 )"
THEIRS="$( is_wsl() { return 0; }; owns_port() { return 1; }; explain_log "$BINDLOG" 2>&1 )"
check "우리 것이면 bml stop 을 준다"   "$(printf '%s\n' "$MINE"   | grep -c 'bml stop')" "1"
check "남의 것이면 bml stop 은 소용없다고 말한다" \
  "$(printf '%s\n' "$THEIRS" | grep -c '소용없습니다')" "1"
# mirrored 를 켠 기계에서 가장 흔한 범인은 예전에 걸어 둔 portproxy 다.
check "포워딩을 지우라고 짚는다" \
  "$(printf '%s\n' "$THEIRS" | grep -c 'portproxy reset')" "1"
# 그래도 남으면 무엇이 잡고 있는지 볼 길을 준다 — WSL 안에서 칠 수 있는 것으로.
check "누가 잡았는지 볼 명령을 준다" \
  "$(printf '%s\n' "$THEIRS" | grep -c 'netstat.exe -ano')" "1"

echo
echo "DB 오류 — 셀을 통째로 버리라고 시키지 않는다"
# 예전에는 `sqlite3.OperationalError` 하나로 묶고 "DB 를 옆으로 치우고 다시" 를
# 시켰다.  그 그물에는 잠김·권한·경로가 다 걸리는데 그 셋은 스키마와 상관이
# 없고, 시키는 일은 셀·그룹·피팅을 통째로 버리는 것이다 -- 이 도구에서 가장
# 위험한 한 줄이었다 (실측 2026-08-27: 방금 내린 서버가 파일을 쥐고 있었을
# 뿐인데 이 안내가 떴다).
dblog() { printf '%s\n' "$1" > "$TMP/db.log"; explain_log "$TMP/db.log" 2>&1; }

LOCKED="$(dblog 'sqlite3.OperationalError: database is locked')"
check "잠김은 스키마 문제가 아니라고 말한다" \
  "$(printf '%s\n' "$LOCKED" | grep -c '스키마 문제가 아닙니다')" "1"
check "잠김에서는 DB 를 지우라고 안 한다" \
  "$(printf '%s\n' "$LOCKED" | grep -cE 'rm data/workbench.db|mv data/workbench.db')" "0"

PERM="$(dblog 'sqlite3.OperationalError: unable to open database file')"
check "권한·경로도 스키마 문제가 아니라고 말한다" \
  "$(printf '%s\n' "$PERM" | grep -c '스키마 문제가 아닙니다')" "1"
check "권한·경로에서도 DB 를 지우라고 안 한다" \
  "$(printf '%s\n' "$PERM" | grep -cE 'rm data/workbench.db|mv data/workbench.db')" "0"

# 진짜 스키마 문제일 때도 **첫 처방은 지우기가 아니다.**  `init_db` 가 빠진
# 열을 자동으로 붙이므로 (apps/api/app/db.py: _add_missing_columns) 한 번 더
# 띄워 보는 것이 먼저고, 버리는 것은 그래도 안 될 때다.
SCHEMA="$(dblog 'sqlite3.OperationalError: no such column: run.superseded_by')"
S_BML="$(printf '%s\n' "$SCHEMA" | grep -n 'bml' | head -1 | cut -d: -f1)"
S_RM="$(printf '%s\n' "$SCHEMA" | grep -n 'rm data/workbench.db' | head -1 | cut -d: -f1)"
if [ -n "$S_BML" ] && [ -n "$S_RM" ] && [ "$S_BML" -lt "$S_RM" ]; then
  pass=$((pass + 1)); printf '  ok   스키마 문제도 다시 띄우기가 먼저다\n'
else
  fail=$((fail + 1)); printf '  FAIL 버리는 것을 먼저 시킨다 (bml %s, rm %s)\n' \
    "${S_BML:-없음}" "${S_RM:-없음}"
fi
check "지우기 전에 백업을 시킨다" \
  "$(printf '%s\n' "$SCHEMA" | grep -c 'cp data/workbench.db')" "1"
check "무엇이 사라지는지 말한다" \
  "$(printf '%s\n' "$SCHEMA" | grep -c '사라집니다')" "1"

# 모르는 OperationalError 는 처방을 지어내지 않고 sqlite 가 한 말을 보여 준다.
OTHER="$(dblog 'sqlite3.OperationalError: disk I/O error')"
check "모르는 것은 그 줄을 그대로 보여 준다" \
  "$(printf '%s\n' "$OTHER" | grep -c 'disk I/O error')" "1"
check "모르면서 DB 를 지우라고 하지 않는다" \
  "$(printf '%s\n' "$OTHER" | grep -cE 'rm data/workbench.db|mv data/workbench.db')" "0"

echo
echo "자리를 둘로 — bmlin / bmlout"
# 랩 주소는 한 번 정하면 안 바뀌고, 터널 주소는 열 때마다 달라질 수 있다.
# 하나만 저장하면 자리를 옮길 때마다 주소를 다시 쳐야 한다.
check "in 은 LAN 자리"     "$(slot_key in)"     "WORKBENCH_SERVER_LAN"
check "out 은 터널 자리"   "$(slot_key out)"    "WORKBENCH_SERVER_TUNNEL"
check "lan 도 같은 자리"   "$(slot_key lan)"    "WORKBENCH_SERVER_LAN"
check "모르는 자리는 거부" "$(slot_key nope || echo REFUSED)" "REFUSED"
# 별칭을 기계마다 손으로 관리하면 반드시 어긋난다.  세 이름이 같은 파일을
# 부르므로 bml 을 고치면 bmlin/bmlout 도 같이 따라온다.  (자세한 것은
# test_bml_install.sh — 여기서는 세 이름이 있다는 것만 본다.)
check "install 이 세 이름을 만든다" \
  "$(grep -c 'for name in bml bmlin bmlout' "$BML")" "1"
check "불린 이름으로 자리를 정한다" \
  "$(grep -c 'bmlin)  set -- in' "$BML")" "1"
# 'tunnel' 은 이미 share 의 별칭이다 — out 에 겹쳐 쓰면 share 가 먹힌다.
check "out 은 tunnel 을 뺏지 않는다" "$(grep -c 'out|wan)' "$BML")" "1"

echo
echo "충돌이 남았으면 그 트리를 실행하지 않는다"
# git pull --rebase --autostash 는 autostash 를 되돌리다 충돌해도 0 을 주는
# 경우가 있다.  그러면 <<<<<<< 가 든 tools/bml 이 남고, 재실행이 그것을
# 실행해서 셸 구문 오류로 죽는다 — 사람은 방금 친 명령을 의심한다.
check "unmerged 를 보고 멈춘다"    "$(grep -c -- '--diff-filter=U' "$BML")" "1"
check "멈출 때 stash 를 짚어 준다" "$(grep -c 'git stash list' "$BML")" "1"
# 그 검사는 재실행보다 **앞**에 있어야 한다.  뒤에 있으면 이미 실행된 뒤다.
check "재실행보다 앞에 있다" \
  "$(awk '/--diff-filter=U/{u=NR} /exec "\$SCRIPT"/{e=NR} END{print (u && e && u < e) ? "yes" : "no"}' "$BML")" "yes"

echo
echo "LAN 주소는 이름이 아니라 기본 경로로 고른다"
# 어댑터 이름은 정체성이 아니다.  VMware 가 192.168.x 를 들고 있으면 이름
# 규칙은 그것을 LAN 으로 보고 노트북에 그 주소를 쓰라고 한다.  반대로 사람이
# 어댑터 이름을 바꾸면(Windows 가 공식 지원) 진짜 LAN 을 버린다.
ROUTES='활성 경로:
네트워크 대상        네트워크 마스크          게이트웨이       인터페이스   메트릭
          0.0.0.0          0.0.0.0     172.20.0.1     172.20.30.40     35
          0.0.0.0          0.0.0.0   192.168.231.2    192.168.231.1    281
        127.0.0.0        255.0.0.0            연결됨        127.0.0.1    331'
check "기본 경로의 인터페이스를 고른다" "$(windows_default_route_ip "$ROUTES")" "172.20.30.40"
# 경로가 여럿이면 메트릭이 낮은 것이 이긴다 — Windows 자신이 고르는 규칙이다.
check "메트릭이 낮은 쪽이 이긴다" \
  "$(windows_default_route_ip '          0.0.0.0          0.0.0.0     10.0.0.1     10.0.0.5     99
          0.0.0.0          0.0.0.0   192.168.0.1  192.168.0.40     10')" "192.168.0.40"
# 기본 경로가 아닌 줄은 보지 않는다 (마스크 칸에도 0.0.0.0 이 나온다).
check "기본 경로가 아닌 줄은 무시"      "$(windows_default_route_ip '        127.0.0.0        255.0.0.0   연결됨   127.0.0.1   331')" ""
check "빈 출력도 죽지 않는다"           "$(windows_default_route_ip '')" ""

echo
echo "401 은 '지금 그 암호' 라는 증거가 아니다"
# bml password 새암호 를 적고 restart 를 안 하면 서버는 옛 암호를 들고 있는데
# 무인증 요청은 똑같이 401 이다.  화면이 잠겼다고만 하면 사람은 새 암호를
# 남에게 알려 주고, 그 사람은 못 들어온다.  문을 실제로 두드려야 안다.
check "303 이면 그 암호가 맞다" \
  "$( curl() { printf '303'; }; door_password_works http://x "암호" && echo yes || echo no )" "yes"
check "401 이면 아니다" \
  "$( curl() { printf '401'; }; door_password_works http://x "암호" && echo yes || echo no )" "no"
check "암호가 없으면 물어보지도 않는다" \
  "$( curl() { printf '303'; }; door_password_works http://x "" && echo yes || echo no )" "no"
# share 는 인터넷에 여는 자리라 이 확인을 반드시 거쳐야 한다.
check "share 가 그 확인을 한다" "$(grep -c 'door_password_works "\$URL"' "$BML")" "2"

echo
echo "화면에 명령으로 찍힐 주소는 애초에 안 받는다"
# 실패 화면이 `bml use $url`, `curl … $url/api/health`, `WORKBENCH_SERVER=$url bml`
# 을 인용 없이 찍는다.  주소에 `;touch …;#` 이 섞여 있으면 사람이 화면대로
# 붙여넣는 순간 그것이 실행된다.  들어올 때 막는 것이 유일하게 확실한 자리다.
check "세미콜론이 든 주소를 거부"   "$(normalize_server_url 'https://x.lhr.life/;touch /tmp/BML_PWN;#' || echo REFUSED)" "REFUSED"
check "명령 치환도 거부"           "$(normalize_server_url 'http://a$(id)b' || echo REFUSED)" "REFUSED"
check "역따옴표도 거부"            "$(normalize_server_url 'http://a`id`b' || echo REFUSED)" "REFUSED"
check "공백도 거부"                "$(normalize_server_url 'http://a b' || echo REFUSED)" "REFUSED"
check "멀쩡한 주소는 그대로"       "$(normalize_server_url 'https://x.lhr.life')" "https://x.lhr.life"
check "맨 IP 도 그대로 편다"       "$(normalize_server_url '192.168.0.40')" "http://192.168.0.40:5003"

echo
echo ".wslconfig — 갈아 끼우지 못하면 원본을 건드리지 않는다"
WT="$TMP/atomic"; mkdir -p "$WT"
printf '[wsl2]\r\nmemory=8GB\r\n' > "$WT/.wslconfig"
BEFORE="$(md5sum < "$WT/.wslconfig")"
# mv 를 실패시킨다.  예전에는 여기서 `cat "$tmp" > "$f"` 로 물러섰고, 그것은
# 원본을 먼저 비우므로 도중에 실패하면 설정이 조각난 채 남았다.
RC="$( mv() { return 1; }; wslconfig_set_mirrored "$WT/.wslconfig"; echo $? )"
check "옮기지 못하면 실패로 끝난다" "$RC" "2"
check "그때 원본은 그대로다"        "$(md5sum < "$WT/.wslconfig")" "$BEFORE"
check "임시 파일도 안 남긴다"       "$(ls "$WT" | grep -c 'bml-new')" "0"

echo
echo ".wslconfig — 알 수 없는 인코딩은 손대지 않는다"
printf '\xff\xfe[\x00w\x00s\x00l\x002\x00]\x00' > "$WT/u16"
check "UTF-16 BOM 을 거부한다"   "$(wslconfig_writable_reason "$WT/u16" | grep -c 'UTF-16')" "1"
printf 'a\x00b\n' > "$WT/nul"
check "NUL 이 있으면 거부한다"   "$(wslconfig_writable_reason "$WT/nul" | grep -c 'NUL')" "1"
# 그리고 멀쩡한 CRLF 파일은 통과해야 한다 — NUL 검사를 잘못 짜면 전부 거부한다
# (bash 는 문자열에 NUL 을 못 담아서 `grep $'\000'` 이 빈 패턴이 된다).
check "멀쩡한 CRLF 파일은 통과"  "$(wslconfig_writable_reason "$WT/.wslconfig" >/dev/null && echo OK)" "OK"

echo
echo ".wslconfig — [wsl2] 절 안에서만 본다"
# 엉뚱한 절의 networkingMode 를 고치고 "됐다" 고 하면, [wsl2] 에는 설정이
# 안 들어가고 사람은 켰다고 믿는다.
printf '[wsl2]\r\nmemory=8GB\r\n[experimental]\r\nnetworkingMode=NAT\r\n' > "$WT/sec"
wslconfig_set_mirrored "$WT/sec"
check "[wsl2] 안에 넣는다"        "$(wslconfig_value_in_wsl2 "$WT/sec" networkingMode)" "mirrored"
check "남의 절은 안 건드린다"      "$(grep -c 'networkingMode=NAT' "$WT/sec")" "1"
# 반대로 엉뚱한 절의 mirrored 를 보고 "이미 되어 있다" 고 해도 안 된다.
printf '[experimental]\r\nnetworkingMode=mirrored\r\n' > "$WT/wrong"
check "남의 절의 mirrored 는 아니다" "$(wslconfig_is_mirrored "$WT/wrong" && echo yes || echo no)" "no"
# 공식 값 virtioproxy → mirrored 는 파일이 짧아진다.  길이로 재면 멀쩡한
# 설정을 거부하고 화면은 권한 문제로 오진한다.
printf '[wsl2]\r\nnetworkingMode=virtioproxy\r\n' > "$WT/vp"
wslconfig_set_mirrored "$WT/vp"
check "짧아지는 값도 고친다"       "$(wslconfig_value_in_wsl2 "$WT/vp" networkingMode)" "mirrored"

echo
echo ".wslconfig — 되돌릴 수 없는 백업이면 고치지 않는다"
BK="$TMP/bakcheck"; mkdir -p "$BK"
printf '[wsl2]\r\nmemory=8GB\r\n' > "$BK/.wslconfig"
mkdir -p "$BK/.wslconfig.bml-bak"          # 백업 자리가 폴더다
BEFORE="$(md5sum < "$BK/.wslconfig")"
OUT="$(run_mirrored "$BK")"
check "쓸 수 없는 백업이면 멈춘다" "$(printf '%s\n' "$OUT" | grep -c '쓸 수 없는 것입니다')" "1"
check "그때 원본은 그대로다"       "$(md5sum < "$BK/.wslconfig")" "$BEFORE"

echo
echo "중추 서버를 봐도 저장소는 맞춘다"
# 이 분기가 sync_repo 를 건너뛰면, 그 기계의 bml·문서·스킬이 클론한 시점에
# 얼어붙는다.  중추 서버 자신에게 use 가 걸리면 아무도 코드를 갱신하지 않는다.
# serve 와 restart 두 분기 모두여야 한다.  하나만 고치면 나머지 하나로 들어온
# 사람에게 같은 증상이 그대로 남는다.
# 한 줄을 통째로 대조하지 않는다.  그러면 그 줄에 단어 하나만 늘어도
# (`cmd_stop --keep-tunnel` 이 그랬다) 규칙이 멀쩡한데 시험이 깨지고, 고치는
# 사람은 시험을 지우는 쪽으로 간다.  못 박을 것은 **순서**다: 중추 서버로
# 붙는 두 분기 모두에서 sync_repo 가 cmd_connect 보다 먼저 와야 한다.
# **순서를 문자열로 못 박지 않는다.**  한 줄로 쓰든 여러 줄로 쓰든 지켜야 하는
# 것은 "붙기 전에 최신화한다" 이고, 정규식은 줄바꿈 하나에 깨진다 -- 그러면
# 규칙이 멀쩡한데 시험이 깨지고, 고치는 사람은 시험을 지우는 쪽으로 간다.
# 실제로 불러 보고 순서를 본다.
sync_before_connect() {
  ( SERVER="https://x.example"
    PORT=59992
    sync_repo()   { printf 'sync '; }
    ensure_deps() { :; }
    cmd_stop()    { :; }
    cmd_connect() { printf 'connect '; }
    main "$1"
  ) 2>/dev/null
}
check "serve 는 붙기 전에 최신화한다"   "$(sync_before_connect serve)"   "sync connect "
check "restart 도 붙기 전에 최신화한다" "$(sync_before_connect restart)" "sync connect "

echo
echo "제자리에서 다시 띄우는 자리는 터널을 살려 둔다"
# 터널은 localhost:5003 을 가리키므로 그 뒤의 서버가 몇 초 내려갔다 올라오는
# 것은 견딘다.  그런데 닫으면 **주소가 바뀐다** (실측: 열 때마다 다른 이름).
# 그러면 코드를 고칠 때마다 기계마다 `bmlout <새 주소>` 를 다시 쳐야 하고,
# 그 사이 노트북은 HTTP 503 을 본다.
#
# 한때 `restart` 두 자리만 그랬다.  그런데 `bml` 이 낡은 서버를 발견해 갈아
# 끼우는 두 갈래도 똑같이 제자리 재시작인데 거기서는 닫고 있었다 -- 실측
# 2026-08-26: 새 커밋을 받은 `bml` 이 터널을 닫아 주소가 사라졌고, 그 뒤
# `bml status` 는 공유에 대해 한 마디도 안 했다.  넷 다 살려 둔다.
check "다시 띄우는 자리 넷이 --keep-tunnel 을 쓴다" \
  "$(grep -c 'cmd_stop --keep-tunnel' "$BML")" "4"
check "stop 은 그대로 닫는다" \
  "$(grep -cE '^\s+stop\|down\)\s+cmd_stop ;;' "$BML")" "1"
# 살려 두는 것은 "곧 돌아온다" 는 약속이다.  다시 띄우다 실패하면 그 약속이
# 깨졌으므로 닫는다 — 뒤에 서버가 없는 주소는 남에게 오류 화면만 띄운다.
check "서버가 안 뜨면 터널을 닫는다" \
  "$(sed -n '/^report_failure()/,/^}/p' "$BML" | grep -c 'close_tunnel')" "1"

# **문자열을 세는 것으로는 부족하다.**  나가는 길이 하나가 아니다 --
# guard_data_dir 은 그 자리에서 exit 하고, 빌드 실패는 die 로 나가고, Ctrl-C 는
# 아무 데서나 온다.  예전에는 report_failure 를 지나는 길에만 정리가 있어서,
# 데이터 폴더가 빠진 채 restart 하면 서버 없는 터널이 그대로 남았다.
# 실제로 restart 를 깨뜨려 본다.
restart_leaves_tunnel() {
  # $1: restart 를 깨뜨리는 방법 (함수 정의 문자열)
  bash -c "exec -a \"cloudflared tunnel --no-autoupdate --url $URL\" sleep 60" &
  local fake=$!
  echo "$fake" > "$TUNNEL_PID_FILE"
  printf 'https://fake-restart.trycloudflare.com' > "$TUNNEL_URL_FILE"
  (
    PORT=59991
    sync_repo() { :; }
    cmd_stop() { :; }
    open_browser() { :; }
    eval "$1"
    main restart
  ) >/dev/null 2>&1
  sleep 0.3
  if tunnel_running; then printf 'yes'; else printf 'no'; fi
  kill "$fake" 2>/dev/null
  rm -f "$TUNNEL_PID_FILE" "$TUNNEL_URL_FILE"
}

check "데이터 폴더가 빠지면 터널을 남기지 않는다" \
  "$(restart_leaves_tunnel 'ensure_deps() { :; }; guard_data_dir() { exit 1; }')" "no"
# build_web 은 start_serve 안, 즉 약속을 건 **뒤**에 돈다.  (ensure_deps 는 그
# 전이라 거기서 죽는 것은 문제가 아니다 -- 서버가 아직 살아 있다.)
check "빌드가 실패해도 터널을 남기지 않는다" \
  "$(restart_leaves_tunnel 'ensure_deps() { :; }; guard_data_dir() { :; }; build_web() { die "빌드 실패"; }')" "no"
# 사람이 Ctrl-C 를 눌러도 같다 -- 나가는 길이 하나가 아니라는 것이 요점이다.
# `$$` 가 아니라 `$BASHPID` 로 보낸다: 서브셸 안에서도 `$$` 는 **부모** pid 라,
# 시험을 돌리는 셸 자신이 INT 를 받고 통째로 죽는다 (한 번 그렇게 죽였다).
check "중간에 끊어도 터널을 남기지 않는다" \
  "$(restart_leaves_tunnel 'ensure_deps() { :; }; guard_data_dir() { kill -INT $BASHPID; sleep 1; }')" "no"
# 멈추기 전에 먼저 받는다 -- 내려가 있는 시간을 줄이고, sync_repo 가 자기 자신을
# 갱신해 exec 로 다시 시작할 때 아직 아무것도 안 멈춘 상태여야 한다.
check "restart 는 멈추기 전에 sync_repo 를 부른다" \
  "$(grep -cE 'sync_repo; (ensure_deps; )?cmd_stop --keep-tunnel' "$BML")" "2"

echo
echo "남의 서버만 보는 기계는 파이썬 환경이 필요 없다"
# 실제로 일어난 일: 다른 공유기의 노트북에서 `bml pull` 이 1~3분짜리 의존성
# 설치를 시작했고, python3-venv 가 없어 거기서 죽었다.  그 기계는 브라우저
# 노릇만 할 참이라 파서도 API 도 거기서 돌지 않는다 (ADR 0011).
# `serve` 분기는 이미 이 규칙을 지키고 있었는데 `pull` 만 빠져 있었다.
check "pull 도 중추 서버가 있으면 건너뛴다" \
  "$(grep -c '중추 서버 ${SERVER} 를 보는 기계라 의존성은 건너뜁니다' "$BML")" "1"
# 그리고 아직 아무 말도 안 한 기계(갓 클론)에서도 만들지 않는다.  그 기계가
# 서버가 될지 브라우저가 될지는 아무도 말한 적이 없고, 1~3분짜리 설치는
# "맞추기" 가 아니다.  실제로 그 설치가 python3-venv 없는 노트북을 두 번 죽였다.
check "환경이 없으면 pull 이 만들지 않는다" \
  "$(grep -c 'elif \[ -x "$REPO/.venv/bin/python" \]; then' "$BML")" "1"
check "대신 무엇을 치면 되는지 말한다" \
  "$(grep -c '파이썬 환경은 아직 없습니다 — 필요할 때 만듭니다' "$BML")" "1"

echo "만들다 만 가상환경은 살려 두지 않는다"
# `python3 -m venv` 가 도중에 죽어도 `.venv/bin/python` 은 남는다.  그러면
# 다음 실행이 "환경이 있다" 로 넘어가 pip 을 부르고, 매번 `No module named
# pip` 로 끝난다 -- 화면은 venv 가 아니라 wrdkit 을 탓한다.
check "pip 이 없으면 껍데기로 본다" \
  "$(grep -c '\-m pip --version >/dev/null 2>&1' "$BML")" "1"
check "그때는 지우고 다시 만든다" \
  "$(grep -c '가상환경이 만들다 말았습니다' "$BML")" "1"
# 두 곳이다: `ensure_deps` 와 `bml repair`.  둘 다 남은 조각이 새 환경에
# 섞이지 않게 --clear 를 쓴다 -- 한쪽만 쓰면 그쪽으로 들어온 사람만 낫는다.
check "다시 만들 때는 --clear 로 (ensure_deps · repair)" \
  "$(grep -c 'python3 -m venv --clear "$REPO/.venv"' "$BML")" "2"
check "그래도 저장소는 맞춘다" \
  "$(awk '/pull\|sync\|update\)/,/^      ;;/' "$BML" | grep -c 'sync_repo')" "1"

echo "venv 를 못 만들면 두 갈래를 다 말한다"
# 파이썬이 찍는 영어 안내는 "이 패키지를 까세요" 까지만 말하고, 이 기계에
# 그게 정말 필요한지는 말해 주지 않는다.  둘 다 없으면 사람은 필요도 없는
# 패키지를 설치하려고 sudo 를 찾아 헤맨다.
check "서버를 띄울 거면 깔 것을 짚는다" \
  "$(grep -c '이 기계에서 서버를 띄울 거라면' "$BML")" "1"
check "남의 서버만 볼 거면 필요 없다고 말한다" \
  "$(grep -c '남의 서버(중추 서버)만 볼 거라면' "$BML")" "1"
check "그때 칠 명령도 함께 준다" \
  "$(grep -c 'bmlout <터널 주소>' "$BML")" "1"

echo "끊기면 다시 붙는다 — 등록한 키가 있을 때만"
# nokey@ 는 붙을 때마다 새 이름을 받으므로, 되살아나면 주소가 바뀌어서 받는
# 쪽은 어차피 다시 쳐야 한다 -- "스스로 낫는다" 가 아니라 "조용히 딴 데를
# 가리킨다" 가 된다.  등록한 키라야 주소가 그대로다.
check "감독자는 키가 있을 때만" \
  "$(awk '/^tunnel_via_ssh\(\) \{/,/^}/' "$BML" | grep -c 'write_tunnel_keepalive')" "1"
# 감독자가 둘이다: localhost.run 쪽과 우리 VPS 쪽 (ADR 0034).  둘 다 같은
# 고리를 가져야 한다 — 한쪽만 다시 붙으면 그쪽만 살아남는다.
#
# **넷이다.**  고리마다 `wait` 가 둘이라서다: 하나는 자식이 끝날 때까지 기다리는
# 것이고, 하나는 TERM 을 받았을 때 죽인 자식을 **거두는** 것이다 (2026-08-27).
# 거두지 않으면 좀비로 남고, 좀비에게도 `kill -0` 은 성공해서 "아직 살아 있다"
# 로 읽힌다.
check "끊기면 다시 붙는 고리가 있다" \
  "$(grep -c 'wait "\\$child"' "$BML")" "4"
# 무한히 두드리지 않는다 -- 키가 지워졌거나 계정이 막힌 것은 고쳐지지 않는다.
check "곧바로 계속 끊기면 멈춘다" \
  "$(grep -c '계속 곧바로 끊겨서 멈춥니다' "$BML")" "2"
# 감독자를 우리 것으로 못 알아보면 status 가 못 보고, close_tunnel 이 안 닫는다.
check "감독자도 우리 것으로 알아본다" \
  "$(grep -c 'tunnel-keepalive.sh"\*) return 0' "$BML")" "1"
# **VPS 감독자도** (Codex #2).  이것이 빠져 있어서 `bml stop` 이 VPS 터널을
# 남겼다 — 닫았다고 말한 뒤에 고정 주소가 조용히 다시 열린다.
check "VPS 감독자도 우리 것으로 알아본다" \
  "$(grep -c 'vps-keepalive.sh"\*) return 0' "$BML")" "1"
# 신호를 받으면 자식 ssh 까지 데리고 죽는다 -- 안 그러면 감독자만 죽고 터널이
# 주인 없이 남는다.
check "닫으면 자식 ssh 도 죽는다" \
  "$(grep -c "trap 'kill" "$BML")" "2"

echo "맞추기가 먼저다 — 자기 갱신 재실행이 일을 두 번 시키지 않게"
# sync_repo 는 자기 자신이 갱신되면 원래 명령줄로 다시 실행한다(exec).  뒤에
# 두면 앞에서 이미 끝낸 접속이 통째로 한 번 더 돌고, 그 두 번째가 잠깐의
# 네트워크 사정으로 실패하면 성공한 뒤에 빨간 ✕ 가 찍힌다 (실측 2회).
check "in 은 sync 뒤에 붙는다" \
  "$(grep -c 'shift; sync_repo; cmd_slot in' "$BML")" "1"
check "out 도 sync 뒤에" \
  "$(grep -c 'shift; sync_repo; cmd_slot out' "$BML")" "1"
check "only 도 sync 뒤에" \
  "$(grep -c 'shift; sync_repo; cmd_only' "$BML")" "1"

echo "bmlonly — DNS 가 막힌 그 한 대에서만"
# `bmlout` 은 어느 기계에서나 같은 뜻이어야 한다: "밖 주소로 붙어라".  DNS 가
# 막힌 기계에서만 그것이 세 단계(공용 DNS → hosts → 접속)가 되는데, 그 셋을
# bmlout 에 섞으면 멀쩡한 기계에서도 sudo 를 묻고 hosts 를 건드리게 된다.
check "이름이 따로 있다"        "$(grep -c 'bmlonly) set -- only' "$BML")" "1"
check "분기도 따로 있다"        "$(grep -c '^    only)' "$BML")" "1"
check "설치가 별칭을 만든다"    "$(grep -c 'for name in bml bmlin bmlout bmlonly' "$BML")" "1"
check "도움말에 있다"           "$(grep -c '#   bmlonly \[주소\]' "$BML")" "1"
# 살아 있는 것을 못 봤으면 hosts 를 건드리지 않는다 -- 죽은 IP 를 박아 두면
# 그 뒤로 이 기계만 조용히 엉뚱한 곳을 본다 (§0.4).
check "확인 전에는 hosts 를 안 건드린다" \
  "$(grep -c '/etc/hosts 는 건드리지 않았습니다' "$BML")" "1"
check "옛 터널 이름을 먼저 지운다" \
  "$(grep -c "sudo sed -i '/\\\\.lhr\\\\.life\\\$/d;/\\\\.localhost\\\\.run\\\$/d" "$BML")" "1"
# 막히지도 않은 기계에서 쳤으면 그냥 넘겨 준다 -- 쓸데없이 sudo 를 묻지 않는다.
# 그리고 **이미 닿으면** 아무것도 안 한다: sync_repo 가 자기 갱신 뒤 원래
# 명령줄로 다시 실행하므로, 이 갈래가 없으면 성공한 뒤에 빨간 ✕ 가 찍힌다.
check "이미 닿으면 아무것도 안 한다" \
  "$(grep -c 'hosts 를 건드릴 것 없이 그대로 씁니다' "$BML")" "1"
# 이름이 잡히는가가 아니라 **워크벤치가 답하는가**를 본다 -- 우리가 알고 싶은
# 것이 그것이고, 이름 풀이는 대리 지표일 뿐이라 어긋날 수 있다.
check "이름이 아니라 응답으로 판정한다" \
  "$(awk '/^cmd_only\(\) \{/,/^cmd_reparse\(\) \{/' "$BML" | grep -c 'server_alive "\$url"')" "1"
# 4초로 재다가 두 번 헛짚었다.  이 왕복은 학교망 → 인터넷 → localhost.run →
# 다시 학교망 → WSL 이라 잘 되는 날에도 몇 초가 든다.
check "왕복 시간을 넉넉히 준다" \
  "$(grep -c 'server_alive "$url" 12' "$BML")" "1"
# 이름이 이미 잡히면 hosts 로 내려갈 이유가 없다.  거기서 공용 DNS 가 막히면
# "이 망이 막습니다" 라는 엉뚱한 결론으로 끝난다 -- 정작 막힌 건 없는데.
check "이름이 잡히면 평소 길로 보낸다" \
  "$(grep -c '이름은 이미 잡힙니다' "$BML")" "1"
# WSL 에서 이 명령이 고치는 것은 **WSL 의** /etc/hosts 인데, 브라우저는
# Windows 에 있고 그 파일을 안 본다.  그래서 bml 은 붙었다고 하는데 크롬은
# ERR_CONNECTION_CLOSED 를 낸다 -- 화면 둘이 정반대를 말한다 (실측).
check "브라우저는 Windows 것이라는 걸 말한다" \
  "$(grep -c '브라우저로 보려면 Windows 에도 같은 줄이 있어야 합니다' "$BML")" "1"
check "Windows 쪽 명령도 준다" \
  "$(grep -cF 'Add-Content' "$BML")" "1"
check "지우는 법까지" \
  "$(grep -c "notmatch 'lhr" "$BML")" "1"
# 세 갈래 모두 같은 곳으로 나간다: 이미 닿을 때, 이름이 잡힐 때, 이름표를
# 막 박았을 때.  `bmlonly` 가 따로 접속 절차를 갖지 않는 것이 요점이다 --
# 갖는 순간 `bmlout` 과 조용히 달라진다.
check "세 갈래 다 bmlout 과 같은 길로" \
  "$(awk '/^cmd_only\(\) \{/,/^cmd_use\(\) \{/' "$BML" | grep -c 'cmd_slot out "\$url"')" "3"

echo
echo "bml reparse — 계산이 바뀌면 올려 둔 것도 따라온다"
# 사이클 요약은 올릴 때 계산해 DB 에 넣는다 (ADR 0003: 시계열은 디스크, 요약만
# DB).  그래서 wrdkit 의 계산을 고쳐도 **이미 올린 파일은 옛 숫자를 그대로
# 들고 있다** -- 코드는 고쳤는데 화면은 안 바뀐다.  실측 2026-08-26: 방전 용량
# 0.18 % 오차를 고친 뒤에도 "아직 값 차이가 난다" 던 자리가 정확히 여기였다.
RE="$(awk '/^cmd_reparse\(\) \{/,/^\}/' "$BML")"
check "전체 재파싱 창구를 부른다" \
  "$(printf '%s' "$RE" | grep -c '\$url/api/runs/reparse')" "1"
check "POST 다"                  "$(printf '%s' "$RE" | grep -c -- '-X POST')" "1"
# 쌓인 것을 다 읽으면 몇 분이 든다.  기본 타임아웃으로 중간에 끊기면 절반만
# 새 값인 저장소가 남는다 -- 옛 값도 새 값도 아닌, 가장 나쁜 상태다.
check "오래 걸리는 것을 안다"    "$(printf '%s' "$RE" | grep -c -- '-m 3600')" "1"
# 서버가 없는데 조용히 넘어가면, 사람은 값이 안 바뀐 이유를 계산에서 찾는다.
check "서버가 없으면 멈춘다"     "$(printf '%s' "$RE" | grep -c 'server_alive')" "1"
# 실패는 세는 것이 아니라 **이름을 적는다** -- "1건 실패" 로는 어느 파일인지
# 알 수 없고, 그러면 고칠 수도 없다 (§0.4).
check "못 읽은 파일 이름을 적는다" "$(printf '%s' "$RE" | grep -c '"name"')" "1"
check "명령이 연결돼 있다"       "$(grep -c '^    reparse|재파싱)' "$BML")" "1"
# 상대가 이 명령의 존재를 알 길은 도움말뿐이다.  값을 고쳐 놓고 상대는 옛
# 숫자를 보는 상태가 이 저장소에서 제일 조용한 고장이다.
check "도움말에 있다" \
  "$(awk 'NR > 1 { if ($0 !~ /^#/) exit; sub(/^# ?/, ""); print }' "$BML" | grep -c '^  bml reparse')" "1"
# 바깥에 열려 있으면 문이 서 있다 (ADR 0014).  `/api/health` 만 문 밖이라
# **서버가 살아 있는 것과 이 POST 가 들어갈 수 있는 것은 다른 일**이다.
# 실측: server_alive 는 통과했는데 {"detail":"암호가 필요합니다."} 로 끝났다.
check "문이 있으면 먼저 들어간다"  "$(printf '%s' "$RE" | grep -c 'hold_gate_jar "$url"')" "1"
# 쿠키 값을 셸에서 흉내 내면(gate.py 의 HMAC) 저쪽이 계산을 바꾸는 날 조용히
# 401 이 되고, 증상은 이쪽에 뜨는데 원인은 저쪽에 있다.
GJ="$(awk '/^gate_jar\(\) \{/,/^\}/' "$BML")"
check "진짜 문으로 들어간다"      "$(printf '%s' "$GJ" | grep -c '__login')" "1"
check "HMAC 을 흉내 내지 않는다"  "$(printf '%s' "$GJ" | grep -c 'hmac\|sha256')" "0"
check "303 이 아니면 실패다"      "$(printf '%s' "$GJ" | grep -c '"303"')" "1"
# 이 쿠키는 암호와 같은 값이다.  저장소 폴더(.bml/)에 남기지 않는다.
check "쿠키를 저장소에 안 남긴다" "$(printf '%s' "$GJ" | grep -c 'RUN_DIR')" "0"
# 쓰고 나서 지운다 — 다만 **부르는 쪽에서 손으로** 지우지 않는다.  나가는 길이
# 넷이라 (curl 실패 · 답 못 읽음 · EIS 실패 · 정상) 손으로 붙이면 하나를
# 빠뜨리고, 실제로 빠뜨려서 EIS 호출이 쿠키 없이 나갔다.  trap 에 건다.
check "정리를 trap 에 건다" \
  "$(printf '%s' "$RE" | grep -c 'hold_gate_jar')" "1"
check "손으로 지우는 줄이 없다" \
  "$(printf '%s' "$RE" | grep -c 'rm -f "\$jar"')" "0"
HJ="$(awk '/^hold_gate_jar\(\) \{/,/^\}/' "$BML")"
check "trap 을 거는 곳은 hold 다"  "$(printf '%s' "$HJ" | grep -c "trap 'drop_gate_jar'")" "1"
check "경로를 표준출력으로 안 낸다" "$(printf '%s' "$HJ" | grep -c 'printf')" "0"
DJ="$(awk '/^drop_gate_jar\(\) \{/,/^\}/' "$BML")"
check "지우고 trap 을 푼다"        "$(printf '%s' "$DJ" | grep -c 'trap - EXIT')" "1"
# 401 을 "뜻 모를 답" 으로 뭉뚱그리면 고칠 방법이 안 보인다.  갈래가 둘이다:
# 암호가 **틀린** 것(문에서 303 이 안 나옴)과 아예 **안 적힌** 것(POST 가 401).
# 둘 다 같은 곳으로 안내한다.
check "고칠 방법을 두 갈래 다"    "$(printf '%s' "$RE" | grep -c 'bml password')" "2"
check "암호 401 을 알아본다"      "$(printf '%s' "$RE" | grep -c '\*암호\*)')" "1"

# 별칭 + 자기 갱신 재실행에서 인자가 밀리지 않는가.
#
# 실행기는 `BML_INVOKED_AS=bmlonly exec …/bml "$@"` 로 부르고, 그 값은 exec 를
# 타고 넘어간다.  별칭을 편 뒤에 BML_ARGV 를 잡으면 재실행 때 한 번 더 펴져
# 인자가 하나씩 밀린다 -- `bmlonly URL IP` 가 `cmd_only "only" "URL"` 이 됐다.
echo
echo "별칭을 편 뒤가 아니라 **앞에서** 원래 인자를 잡는다"

order() {
  # main() 안에서 BML_ARGV 대입이 case 보다 먼저 나오는지.
  awk '/^  BML_ARGV=\(\)/ { argv = NR }
       /bmlonly\) set -- only/ { alias = NR }
       END { print (argv && alias && argv < alias) ? "before" : "after" }' "$HERE/../bml"
}
check "원래 인자를 먼저 잡는다" "$(order)" "before"

# 그리고 실제로 밀리지 않는지 -- 별칭을 두 번 펴 본다.
replay() {
  set -- "$@"
  local kept=("$@")
  # main() 이 하는 그대로: 먼저 잡고, 그다음 편다.
  case "bmlonly" in bmlonly) set -- only "$@" ;; esac
  # 자기 갱신 재실행: 잡아 둔 것으로 다시 시작하고 별칭이 또 펴진다.
  set -- "${kept[@]}"
  case "bmlonly" in bmlonly) set -- only "$@" ;; esac
  shift
  printf '%s|%s' "${1:-}" "${2:-}"
}
check "재실행해도 URL·IP 가 제자리" \
  "$(replay https://x.lhr.life 1.2.3.4)" "https://x.lhr.life|1.2.3.4"
check "인자 없는 bmlout 도 그대로" "$(replay)" "|"

echo
echo "문 쿠키는 두 호출을 다 지나고 나서 지워진다"
# 실제로 있었던 결함: `bml reparse` 가 충방전 호출 **직후에** 쿠키 파일을
# 지워서, 바로 뒤 EIS 호출이 `-b <없는 파일>` 로 나가 401 을 받았다.
#   ! EIS 맞춤 결과를 읽지 못했습니다.
#     {"detail":"암호가 필요합니다."}
# 소스 훑기로는 못 잡는다 — 지우는 줄이 **있는 것** 자체는 맞기 때문이다.
# 그래서 함수를 진짜로 돌려 파일이 언제 사라지는지 본다.
JARTEST="$(mktemp -d)"
cat > "$JARTEST/run.sh" <<'INNER'
set -u
# `gate_jar` 만 흉내 낸다 — 로그인 대신 파일 하나를 만든다.
gate_jar() { local j; j="$(mktemp "${TMPDIR:-/tmp}/faux-jar.XXXXXX")"; printf '%s
' "$j"; }
GATE_JAR=""
drop_gate_jar() {
  [ -n "$GATE_JAR" ] || return 0
  rm -f "$GATE_JAR"; GATE_JAR=""; trap - EXIT INT TERM
}
hold_gate_jar() {
  local url="${1:-}" jar
  jar="$(gate_jar "$url")" || return 1
  [ -n "$jar" ] || return 0
  GATE_JAR="$jar"
  trap 'drop_gate_jar' EXIT INT TERM
}
hold_gate_jar http://x
printf 'held=%s
' "$GATE_JAR"                       # 전역이 부모에 남았나
[ -f "$GATE_JAR" ] && printf 'first=yes
'           # 첫 호출 때 있다
[ -f "$GATE_JAR" ] && printf 'second=yes
'          # 둘째 호출 때도 있다
printf '%s
' "$GATE_JAR" > "$1"                     # 경로를 밖으로 흘린다
exit 0                                               # 나가면 trap 이 지운다
INNER
OUTJ="$(bash "$JARTEST/run.sh" "$JARTEST/path" 2>&1)"
JARPATH="$(cat "$JARTEST/path" 2>/dev/null || true)"
check "쿠키 경로가 부모 셸에 남는다 (서브셸이면 빈다)" \
  "$(printf '%s' "$OUTJ" | grep -c '^held=/')" "1"
check "첫 호출 때 파일이 있다" \
  "$(printf '%s' "$OUTJ" | grep -c '^first=yes')" "1"
check "둘째 호출 때도 아직 있다" \
  "$(printf '%s' "$OUTJ" | grep -c '^second=yes')" "1"
check "나가면 지워진다" "$([ -e "$JARPATH" ] && echo left || echo gone)" "gone"
rm -rf "$JARTEST"

echo
echo "bml reparse 는 EIS 맞춤도 같이 다시 한다"
# 충방전 파싱은 결정적이라 다시 읽으면 끝이지만, EIS 는 판정 규칙이 맞춤 안에
# 들어 있다.  여기서 같이 안 돌리면 사람은 "왜 갑자기 미결정이지" 만 본다.
RE="$(sed -n '/^cmd_reparse()/,/^}/p' "$BML")"
check "충방전 재파싱을 부른다" \
  "$(printf '%s' "$RE" | grep -c '\$url/api/runs/reparse')" "1"
check "EIS 재맞춤도 부른다" \
  "$(printf '%s' "$RE" | grep -c '\$url/api/eis/refit')" "1"
check "수렴 안 한 개수를 읽는다" \
  "$(printf '%s' "$RE" | grep -c 'not_converged')" "1"
# EIS 가 실패해도 충방전 결과를 되돌리지 않는다 — 둘은 서로 다른 일이다.
check "EIS 실패는 경고로 끝난다" \
  "$(printf '%s' "$RE" | grep -c 'EIS 맞춤은 다시 하지 못했습니다')" "1"
# 두 호출 **사이에서** 쿠키를 지우면 안 된다.  그것이 바로 그 결함이었다.
BETWEEN="$(printf '%s' "$RE" | sed -n '/api\/runs\/reparse/,/api\/eis\/refit/p')"
check "두 호출 사이에서 쿠키를 안 지운다" \
  "$(printf '%s' "$BETWEEN" | grep -c 'rm -f "\$jar"')" "0"
check "끝에서 명시적으로도 한 번 정리한다" \
  "$(printf '%s' "$RE" | grep -c '^  drop_gate_jar$')" "1"

echo
if [ "$fail" -eq 0 ]; then
  printf '통과 %d건.\n' "$pass"
else
  printf '통과 %d건, 실패 %d건.\n' "$pass" "$fail"
fi
exit $([ "$fail" -eq 0 ] && echo 0 || echo 1)
