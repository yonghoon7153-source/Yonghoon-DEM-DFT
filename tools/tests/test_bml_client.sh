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
  "$(lan_addresses '169.254.83.107 192.168.0.40 192.168.56.1' | tr '\n' ' ')" "192.168.0.40 "
check "VirtualBox 호스트 전용을 버린다" "$(lan_addresses '192.168.56.1')" ""
check "루프백을 버린다"                 "$(lan_addresses '127.0.0.1')"     ""
# 도커 브리지와 WSL NAT 이 같은 대역이다.  둘 다 그 PC 안에서만 통한다.
check "172.17.x 를 버린다"              "$(lan_addresses '172.17.0.1')"    ""
check "172.28.x 를 버린다"              "$(lan_addresses '172.28.144.1')"  ""
check "10.x 는 남긴다"                  "$(lan_addresses '10.0.1.5')"      "10.0.1.5"
check "하나도 없으면 빈 값"             "$(lan_addresses '127.0.0.1 169.254.1.2')" ""

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
  ( BML_NO_OPEN=1 cmd_use "127.0.0.1:$LIVE" >/dev/null 2>&1 )
  check "닿는 주소는 저장된다" "$(grep -c "^WORKBENCH_SERVER=http://127.0.0.1:$LIVE$" "$RUN_DIR/env")" "1"
else
  fail=$((fail + 1)); printf '  FAIL 시험용 서버를 못 띄웠다\n'
fi

# 닫힌 포트.  curl 은 기다리지 않고 바로 거절당한다.
check "안 닿는 주소는 거절한다" "$(server_alive 'http://127.0.0.1:1' && echo yes || echo no)" "no"

: > "$RUN_DIR/env"
( BML_NO_OPEN=1 cmd_use "127.0.0.1:1" >/dev/null 2>&1 )
check "안 닿는 주소는 저장하지 않는다" "$(grep -c '^WORKBENCH_SERVER=' "$RUN_DIR/env")" "0"

echo
echo "중추 서버가 정해져 있으면 자기 서버를 안 띄운다"
# 데이터 폴더가 없는 채로 부른다.  자기 서버를 띄우려 했다면 guard_data_dir 가
# "데이터 폴더가 없습니다" 로 죽는다 — 그 메시지가 나오면 분기를 안 탄 것이다.
out="$(WORKBENCH_SERVER=http://127.0.0.1:1 WORKBENCH_DATA="$TMP/없는폴더" \
       BML_NO_OPEN=1 "$BML" 2>&1)"
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
