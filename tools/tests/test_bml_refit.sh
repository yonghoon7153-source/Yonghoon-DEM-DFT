#!/usr/bin/env bash
#
# `bml refit` — 검수가 권한 회로·하한으로 한꺼번에 다시 맞춘다 (ADR 0045).
#
# 가짜 서버를 띄워 명령을 **진짜로** 돌린다.  소스를 훑어서는 못 잡는 것이
# 요점이다:
#
#   1. 서버의 글을 **받는 대로** 찍는다.  십수 분 걸리는 묶음이 끝날 때까지
#      터미널이 조용하면 사람은 멈춘 줄 안다 — 서버가 마지막 줄을 보내기 전에
#      첫 줄이 화면에 있어야 한다.
#   2. 끝나면 데이터 폴더에 남긴다.  `--dry-run` 은 dry_run=true 로 부르고 이름도
#      따로 남긴다.
#   3. `--undo` 는 되돌리기 창구를 부르고 그 글을 찍는다.
#   4. 옛 서버(404)면 그렇다고 말하고, 404 본문을 결과처럼 흘리지 않는다.
#   5. 서버가 옛 커밋으로 떠 있으면 맞추지 않는다 — 옛 판정으로 맞추게 된다.
#   6. 모르는 선택은 막는다.
#
# 사용: bash tools/tests/test_bml_refit.sh     (실패 0 이면 exit 0)

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
has() {
  local what="$1" haystack="$2" needle="$3"
  case "$haystack" in
    *"$needle"*) pass=$((pass + 1)); printf '  ok   %s\n' "$what" ;;
    *) fail=$((fail + 1)); printf '  FAIL %s\n           "%s" 가 없습니다\n' "$what" "$needle" ;;
  esac
}
hasnt() {
  local what="$1" haystack="$2" needle="$3"
  case "$haystack" in
    *"$needle"*) fail=$((fail + 1)); printf '  FAIL %s\n           "%s" 가 있습니다\n' "$what" "$needle" ;;
    *) pass=$((pass + 1)); printf '  ok   %s\n' "$what" ;;
  esac
}

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"; [ -n "${SERVER_PID:-}" ] && kill "$SERVER_PID" 2>/dev/null' EXIT

BML_SOURCE_ONLY=1 . "$BML"
unset WORKBENCH_PASSWORD SERVER
REPO="$TMP/repo"; RUN_DIR="$REPO/.bml"; mkdir -p "$RUN_DIR"
HEAD_FILE="$RUN_DIR/server.head"      # 진짜 저장소의 표식을 건드리지 않는다

# POST 한 경로(쿼리 포함)를 `posted` 에 적고, `www/<경로>` 를 돌려준다.  파일이
# 없으면 404.  `www/<경로>.slow` 가 있으면 그 줄들을 **한 줄씩 사이를 두고**
# 보내고, 다 보낸 뒤에 `www/<경로>.sent` 를 만든다 — 흘려 받는지 보는 표식.
mkdir -p "$TMP/www/api/eis/audit"
printf 'ok' > "$TMP/www/api/health"
python3 - "$TMP/www" "$TMP/port" "$TMP/posted" >/dev/null 2>&1 <<'PYSRV' &
import http.server, os, sys, time
root, portfile, posted = sys.argv[1], sys.argv[2], sys.argv[3]

class Canned(http.server.BaseHTTPRequestHandler):
    def _answer(self):
        path = self.path.split("?", 1)[0].lstrip("/")
        target = os.path.join(root, path)
        if os.path.isfile(target + ".slow"):
            with open(target + ".slow", "rb") as fh:
                lines = fh.read().splitlines(keepends=True)
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            for index, line in enumerate(lines):
                self.wfile.write(line)
                self.wfile.flush()
                if index == 0:
                    time.sleep(3.0)
            open(target + ".sent", "w").close()
            return
        if not os.path.isfile(target):
            self.send_response(404); self.end_headers()
            self.wfile.write(b'{"detail":"Not Found"}')
            return
        with open(target, "rb") as fh:
            body = fh.read()
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._answer()

    def do_POST(self):
        with open(posted, "a") as fh:
            fh.write(self.path + "\n")
        self._answer()

    def log_message(self, *args):
        pass

srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Canned)
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
if [ -z "$LIVE" ]; then
  printf '  FAIL 시험용 서버를 못 띄웠다\n'
  exit 1
fi
URL="http://127.0.0.1:$LIVE"
ENDPOINT="$TMP/www/api/eis/audit/refit"

echo "bml refit — 받는 대로 찍고, 남긴다"
printf '%s\n' \
  'EIS 다시 맞추기 — 2026-09-23 16:03 UTC · 묶음 refit-20260923T160320' \
  '[1/2] #12  B15_pellet  바꿈  R0-p(R1,CPE1) → L1-R0-CPE1 · 문제 1 → 0' \
  '[2/2] #13  B14_arc  그대로  (L1-R0-CPE1 · 기본 시작점에서 — 맞춤이 평균 22.7 % 어긋납니다)' \
  '대상 2 · 바꾼 것 1 · 그대로 1 · 건너뜀 0' > "$ENDPOINT.slow"

( DATA_DIR="$TMP/data" cmd_refit > "$TMP/out" 2>&1; echo $? > "$TMP/rc" ) &
RUNNER=$!
streamed=no
for _ in $(seq 1 60); do
  if grep -q 'EIS 다시 맞추기' "$TMP/out" 2>/dev/null; then
    [ -e "$ENDPOINT.sent" ] || streamed=yes
    break
  fi
  sleep 0.1
done
wait "$RUNNER"
OUT="$(cat "$TMP/out")"
check "서버가 다 보내기 전에 첫 줄이 화면에 있다" "$streamed" "yes"
check "성공으로 끝난다" "$(cat "$TMP/rc")" "0"
has "스펙트럼마다의 줄을 찍는다" "$OUT" "[2/2] #13  B14_arc  그대로"
has "끝의 정리를 찍는다" "$OUT" "대상 2 · 바꾼 것 1 · 그대로 1 · 건너뜀 0"
check "한 줄을 두 번 찍지 않는다" "$(grep -c '^\[1/2\]' "$TMP/out")" "1"
SAVED="$(ls "$TMP/data/audit"/eis-refit-2*.txt 2>/dev/null | head -n 1)"
check "데이터 폴더에 파일로 남긴다" "$([ -n "$SAVED" ] && echo yes || echo no)" "yes"
check "남긴 파일이 받은 글과 같다" "$(cat "$SAVED" 2>/dev/null)" "$(cat "$ENDPOINT.slow")"
has "어디 남겼는지 말한다" "$OUT" "$SAVED"
check "글로 달라고 부른다 (저장한다)" "$(tail -n 1 "$TMP/posted")" "/api/eis/audit/refit?format=text"
rm -f "$ENDPOINT.slow" "$ENDPOINT.sent"

echo
echo "bml refit --dry-run — 맞춰 보기만"
printf 'EIS 다시 맞추기 — 2026-09-23 16:04 UTC · 묶음 refit-20260923T160400\n맞춰 보기만 했습니다 — 아무것도 저장하지 않았습니다.\n' \
  > "$ENDPOINT"
OUT="$( DATA_DIR="$TMP/data" cmd_refit --dry-run 2>&1 )"; rc=$?
check "성공으로 끝난다" "$rc" "0"
check "dry_run=true 로 부른다" "$(tail -n 1 "$TMP/posted")" \
  "/api/eis/audit/refit?format=text&dry_run=true"
has "서버의 글을 찍는다" "$OUT" "아무것도 저장하지 않았습니다"
check "따로 남긴다" "$(ls "$TMP/data/audit"/eis-refit-dry-*.txt 2>/dev/null | wc -l | tr -d ' ')" "1"

echo
echo "bml refit --undo — 마지막 묶음만 지운다"
# 같은 경로가 묶음(파일)과 되돌리기(`…/refit/undo`)의 앞이라 폴더로 바꾼다.
rm -f "$ENDPOINT"; mkdir -p "$ENDPOINT"
printf '묶음 refit-20260923T160320 의 맞춤 1개를 지웠습니다 — 그 스펙트럼들은 묶음 전의 맞춤으로 돌아갔습니다.\n    #12  B15_pellet — L1-R0-CPE1 → R0-p(R1,CPE1)\n' \
  > "$ENDPOINT/undo"
OUT="$( DATA_DIR="$TMP/data" cmd_refit --undo 2>&1 )"; rc=$?
check "성공으로 끝난다" "$rc" "0"
check "되돌리기 창구를 부른다" "$(tail -n 1 "$TMP/posted")" "/api/eis/audit/refit/undo?format=text"
has "지운 것을 찍는다" "$OUT" "#12  B15_pellet — L1-R0-CPE1 → R0-p(R1,CPE1)"
check "되돌리기는 파일로 남기지 않는다" \
  "$(ls "$TMP/data/audit"/eis-refit-*.txt 2>/dev/null | wc -l | tr -d ' ')" "2"

echo
echo "옛 서버 · 옛 커밋 · 모르는 선택"
rm -rf "$ENDPOINT"
OUT="$( DATA_DIR="$TMP/data" cmd_refit 2>&1 )"; rc=$?
check "옛 서버면 실패로 끝난다" "$rc" "1"
has "옛 코드라고 말한다" "$OUT" "옛 코드로 떠 있습니다"
has "고칠 명령을 가리킨다" "$OUT" "bml restart"
hasnt "404 본문을 결과처럼 찍지 않는다" "$OUT" "Not Found"

git -C "$REPO" init -q
git -C "$REPO" -c user.name=t -c user.email=t@example.com commit -q --allow-empty -m one
printf '0123456789abcdef0123456789abcdef01234567\n' > "$HEAD_FILE"
: > "$TMP/posted"
OUT="$( DATA_DIR="$TMP/data" cmd_refit 2>&1 )"; rc=$?
check "옛 커밋의 서버면 실패로 끝난다" "$rc" "1"
has "어느 커밋이 떠 있는지 말한다" "$OUT" "이전 커밋(01234567)"
check "아무것도 부르지 않는다" "$(wc -l < "$TMP/posted" | tr -d ' ')" "0"
rm -f "$HEAD_FILE"

OUT="$( DATA_DIR="$TMP/data" cmd_refit --force 2>&1 )"; rc=$?
check "모르는 선택이면 실패로 끝난다" "$rc" "1"
has "쓸 수 있는 선택을 말한다" "$OUT" "[--dry-run | --undo]"

OUT="$( URL="http://127.0.0.1:1" DATA_DIR="$TMP/data" cmd_refit 2>&1 )"; rc=$?
check "서버가 없으면 실패로 끝난다" "$rc" "1"
has "서버가 없다고 말한다" "$OUT" "서버가 응답하지 않습니다"

echo
echo "명령과 도움말"
check "명령이 연결돼 있다" "$(grep -c '^    refit|다시맞춤)' "$BML")" "1"
check "도움말에 있다" \
  "$(awk 'NR > 1 { if ($0 !~ /^#/) exit; sub(/^# ?/, ""); print }' "$BML" | grep -c '^  bml refit ')" "2"

echo
if [ "$fail" -eq 0 ]; then
  printf '통과 %d건.\n' "$pass"
else
  printf '통과 %d건, 실패 %d건.\n' "$pass" "$fail"
fi
exit $([ "$fail" -eq 0 ] && echo 0 || echo 1)
