#!/usr/bin/env bash
#
# `bml audit` 와, `bml reparse` 가 EIS 원본도 다시 읽는 것 (ADR 0040).
#
# 가짜 서버를 띄워 명령을 **진짜로** 돌린다.  소스를 훑어서는 못 잡는 것이
# 이 둘의 요점이다:
#
#   1. 검수 글을 찍고 **파일로도 남긴다** — 그 글을 붙여 넣어 받는 쪽이 있다.
#      파일을 못 남겨도 멈추지 않는다: 화면의 글이 본체다.
#   2. 서버가 옛 코드면(404) 그렇다고 말하고 `bml restart` 를 가리킨다 —
#      "뜻 모를 답" 으로 끝나면 사람은 검수가 고장 난 줄 안다.
#   3. `bml reparse` 는 EIS 원본을 **맞춤보다 먼저** 다시 읽는다.  순서가
#      바뀌면 옛 점으로 다시 맞추고, 고친 파서가 소용없다.
#   4. 옛 서버에 EIS 재파싱 창구가 없어도 맞춤은 하던 대로 한다.
#
# 사용: bash tools/tests/test_bml_audit.sh     (실패 0 이면 exit 0)

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

# GET 도 POST 도 파일 하나로 답하는 서버.  경로 → `www/<경로>`, 쿼리는 떼고,
# 파일이 없으면 404.  POST 로 부른 경로는 `posted` 에 적는다 (순서 확인용).
mkdir -p "$TMP/www/api/eis" "$TMP/www/api/runs"
printf 'ok' > "$TMP/www/api/health"
python3 - "$TMP/www" "$TMP/port" "$TMP/posted" >/dev/null 2>&1 <<'PYSRV' &
import http.server, os, sys
root, portfile, posted = sys.argv[1], sys.argv[2], sys.argv[3]

class Canned(http.server.BaseHTTPRequestHandler):
    def _answer(self):
        path = self.path.split("?", 1)[0].lstrip("/")
        target = os.path.join(root, path)
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
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            self.rfile.read(length)
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

echo "bml audit — 글을 찍고, 남긴다"
REPORT='EIS 검수 — 2026-09-23 01:19 UTC · 스펙트럼 8개 · 스캔 1개
문제 1 · 확인 0 · 참고만 6 · 깨끗 1
    [문제] R1 (벌크 저항) 의 커패시턴스 4.66e-07 F 는 벌크일 수 없습니다'
printf '%s\n' "$REPORT" > "$TMP/www/api/eis/audit"

OUT="$( DATA_DIR="$TMP/data" cmd_audit 2>&1 )"; rc=$?
check "성공으로 끝난다" "$rc" "0"
has "서버가 만든 글을 그대로 찍는다" "$OUT" "[문제] R1 (벌크 저항) 의 커패시턴스"
SAVED="$(ls "$TMP/data/audit"/eis-audit-*.txt 2>/dev/null | head -n 1)"
check "데이터 폴더에 파일로 남긴다" "$([ -n "$SAVED" ] && echo yes || echo no)" "yes"
check "남긴 파일이 찍은 글과 같다" "$(cat "$SAVED" 2>/dev/null)" "$REPORT"
has "어디 남겼는지 말한다" "$OUT" "$SAVED"
# 검수는 **읽기만** 한다 — POST 가 하나라도 나가면 약속이 깨진 것이다.
check "아무것도 POST 하지 않는다" "$(cat "$TMP/posted" 2>/dev/null | wc -l | tr -d ' ')" "0"

# 파일을 못 남겨도 멈추지 않는다 — 화면의 글이 본체다.
touch "$TMP/not-a-dir"
OUT="$( DATA_DIR="$TMP/not-a-dir" cmd_audit 2>&1 )"; rc=$?
check "못 남겨도 성공으로 끝난다" "$rc" "0"
has "글은 그대로 찍는다" "$OUT" "스펙트럼 8개"
has "못 남겼다고 말한다" "$OUT" "파일로는 못 남겼습니다"

# 옛 코드로 떠 있는 서버 — 창구가 없다.
rm -f "$TMP/www/api/eis/audit"
OUT="$( DATA_DIR="$TMP/data" cmd_audit 2>&1 )"; rc=$?
check "옛 서버면 실패로 끝난다" "$rc" "1"
has "옛 코드라고 말한다" "$OUT" "옛 코드로 떠 있습니다"
has "고칠 명령을 가리킨다" "$OUT" "bml restart"

OUT="$( URL="http://127.0.0.1:1" DATA_DIR="$TMP/data" cmd_audit 2>&1 )"; rc=$?
check "서버가 없으면 실패로 끝난다" "$rc" "1"
has "서버가 없다고 말한다" "$OUT" "서버가 응답하지 않습니다"

echo
echo "bml reparse — EIS 원본을 맞춤보다 먼저 다시 읽는다"
printf '{"total":2,"reparsed":2,"failed":[]}' > "$TMP/www/api/runs/reparse"
printf 'EIS 원본 3/3 개를 다시 읽었습니다.\n점이 달라진 스펙트럼 1개 — 그 맞춤은 옛 점으로 한 것입니다:\n    #5 B12_activationE #2 — 점 59 → 57개\n' \
  > "$TMP/www/api/eis/reparse"
printf '{"total":3,"refitted":3,"not_converged":0,"failed":[]}' > "$TMP/www/api/eis/refit"
: > "$TMP/posted"
OUT="$( cmd_reparse 2>&1 )"; rc=$?
check "성공으로 끝난다" "$rc" "0"
has "EIS 재파싱의 글을 찍는다" "$OUT" "EIS 원본 3/3 개를 다시 읽었습니다."
has "달라진 스펙트럼을 이름으로 찍는다" "$OUT" "#5 B12_activationE #2 — 점 59 → 57개"
hasnt "HTTP 코드를 글에 섞지 않는다" "$OUT" "57개
200"
ORDER="$(sed 's/?.*//' "$TMP/posted" | tr '\n' ' ')"
check "충방전 → EIS 원본 → EIS 맞춤 순서" "$ORDER" "/api/runs/reparse /api/eis/reparse /api/eis/refit "
has "맞춤도 한다" "$OUT" "EIS 3/3 개를 다시 맞췄습니다."

# 옛 서버: EIS 재파싱 창구가 없다.  맞춤은 하던 대로.
rm -f "$TMP/www/api/eis/reparse"
: > "$TMP/posted"
OUT="$( cmd_reparse 2>&1 )"; rc=$?
check "옛 서버에서도 성공으로 끝난다" "$rc" "0"
has "옛 코드라고 말한다" "$OUT" "서버가 EIS 재파싱을 모릅니다"
has "맞춤은 그대로 한다" "$OUT" "EIS 3/3 개를 다시 맞췄습니다."
hasnt "404 본문을 결과처럼 찍지 않는다" "$OUT" "Not Found"

echo
echo "명령과 도움말"
check "명령이 연결돼 있다" "$(grep -c '^    audit|검수)' "$BML")" "1"
check "도움말에 있다" \
  "$(awk 'NR > 1 { if ($0 !~ /^#/) exit; sub(/^# ?/, ""); print }' "$BML" | grep -c '^  bml audit')" "1"

echo
if [ "$fail" -eq 0 ]; then
  printf '통과 %d건.\n' "$pass"
else
  printf '통과 %d건, 실패 %d건.\n' "$pass" "$fail"
fi
exit $([ "$fail" -eq 0 ] && echo 0 || echo 1)
