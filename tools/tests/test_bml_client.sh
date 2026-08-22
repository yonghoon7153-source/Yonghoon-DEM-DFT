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
help_lan="$(server_unreachable_help 'http://192.168.0.40:5003' 2>&1)"
help_tunnel="$(server_unreachable_help 'https://127.0.0.1:1' 2>&1)"
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
check "cloudflare 가 안 되면 SSH 로 넘어간다" \
  "$(sed -n '/^cmd_share()/,/^}/p' "$BML" | grep -c 'tunnel_via_ssh')" "2"
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
if [ "$fail" -eq 0 ]; then
  printf '통과 %d건.\n' "$pass"
else
  printf '통과 %d건, 실패 %d건.\n' "$pass" "$fail"
fi
exit $([ "$fail" -eq 0 ] && echo 0 || echo 1)
