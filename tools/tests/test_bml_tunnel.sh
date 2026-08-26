#!/usr/bin/env bash
#
# `bml share` 가 터널을 어떻게 판정하는지에 대한 회귀 테스트.
#
# 여기서 지키는 것은 하나다: **확인이 안 됐다는 말이 세 가지를 한 덩어리로
# 만들면 안 된다.**  실제로 일어난 일 — 랩 망이 7844/TCP 를 막아 SSH 터널로
# 넘어갔고, 주소는 받았는데 이 기계에서 그 주소로 나가지도 못했다.  화면은
# "아직 응답하지 않습니다" 한 줄이었고, 그 문장은 (1) 터널이 아직 안 붙었다,
# (2) 이 기계만 못 나간다(상대는 열려 있다), (3) 터널 프로그램이 이미 죽었다
# 를 구분해 주지 못한다.  대처가 셋 다 다른데도.
#
# 사용: bash tools/tests/test_bml_tunnel.sh     (실패 0 이면 exit 0)

set -uo pipefail

HERE="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BML_SOURCE_ONLY=1 source "$HERE/../bml"

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

contains() {
  local what="$1" haystack="$2" needle="$3"
  case "$haystack" in
    *"$needle"*) pass=$((pass + 1)); printf '  ok   %s\n' "$what" ;;
    *) fail=$((fail + 1)); printf '  FAIL %s\n           얻음: %s\n           들어 있어야: %s\n' "$what" "$haystack" "$needle" ;;
  esac
}

echo "bml 터널 판정"

# --- 코드 하나가 사람 말이 되는가 -------------------------------------------

# 000 이 가장 중요하다.  이것만은 "터널이 안 됐다" 로 읽히면 안 된다 — 우리가
# 못 나간 것이고, 그 주소는 상대 쪽에서 멀쩡히 열려 있을 수 있다.  그런데도
# 여기서 주소를 버리면 열린 터널을 손으로 닫는 셈이 된다.
contains "000 은 '이 기계가 못 나갔다' 로 말한다" \
  "$(tunnel_code_meaning 000)" "이 기계가"
contains "000 은 상대 쪽 가능성을 남긴다" \
  "$(tunnel_code_meaning 000)" "상대"
contains "빈 코드도 000 과 같이 다룬다" \
  "$(tunnel_code_meaning "")" "이 기계가"

# 5xx 는 반대다 — 우리는 나갔고, 제공자가 뒤에서 응답을 못 받았다.
# Cloudflare 는 530, localhost.run 은 502·503 을 준다.
#
# 그런데 그 코드가 가르는 것은 거기까지다.  터널이 끊긴 것인지 그 뒤의 서버가
# 안 떠 있는 것인지는 **둘 다 503** 이라 구분되지 않는다.  한쪽으로 단정하면
# 나머지 절반의 사람에게 틀린 절차를 시킨다 (실측 2026-08-24: 방금 연 터널이
# 503 이었고, 끊긴 것은 터널이 아니라 서버였다).
for code in 502 503 530; do
  contains "$code 는 뒤에서 응답이 없다고 말한다" \
    "$(tunnel_code_meaning "$code")" "아무 응답도 못 받았습니다"
  case "$(tunnel_code_meaning "$code")" in
    *"터널이 끊겼거나"*) pass=$((pass + 1)); printf '  ok   %s 는 둘 다 가능하다고 말한다\n' "$code" ;;
    *) fail=$((fail + 1)); printf '  FAIL %s 가 한쪽으로 단정한다\n' "$code" ;;
  esac
done
contains "404 는 엉뚱한 서버라고 말한다"     "$(tunnel_code_meaning 404)" "우리 서버가 아닙니다"
contains "429 는 사용량 제한이라고 말한다"   "$(tunnel_code_meaning 429)" "제한"

# 200 말고는 무엇도 "열렸습니다" 라고 하지 않는다.  한 번 그렇게 말하면
# 사람은 그 주소를 상대에게 보내고, 되돌아오는 데 왕복 한 번이 든다.
for code in 000 404 429 502 530 999 ""; do
  case "$(tunnel_code_meaning "$code")" in
    *열렸습니다*) fail=$((fail + 1)); printf '  FAIL %s 인데 열렸다고 말한다\n' "${code:-빈값}" ;;
    *) pass=$((pass + 1)) ;;
  esac
done
check "200 만 열렸다고 말한다" "$(tunnel_code_meaning 200)" "HTTP 200 — 열렸습니다"

# --- 죽은 터널을 계속 기다리지 않는가 ---------------------------------------

# ssh 는 `remote port forwarding failed` 로 몇 초 만에 끝날 수 있다.  그
# 뒤로 남은 시간을 죽은 주소에 대고 물어보면, 화면에는 "느리다" 로만 보이고
# 사람은 망을 의심한다.  주소는 그 프로그램이 살아 있는 동안만 산다.
sleep 0.1 & dead_pid=$!
wait "$dead_pid" 2>/dev/null
started=$SECONDS
# 127.0.0.1:1 은 곧바로 연결이 거절된다 — curl 이 오래 잡고 있지 않는다.
wait_until_alive "http://127.0.0.1:1" 45 "$dead_pid"
rc=$?
elapsed=$((SECONDS - started))
check "죽은 pid 를 보고 있으면 실패로 끝난다" "$rc" "1"
if [ "$elapsed" -le 15 ]; then
  pass=$((pass + 1)); printf '  ok   죽은 터널을 45초까지 기다리지 않는다 (%d초)\n' "$elapsed"
else
  fail=$((fail + 1)); printf '  FAIL 죽은 터널을 %d초나 기다렸다\n' "$elapsed"
fi

# 그리고 좀비도 죽은 것으로 봐야 한다.  터널은 `disown` 한 자식이라 끝나도
# 우리가 거두지 않아 좀비로 남는데, 좀비에게 `kill -0` 은 성공한다 — 그 한
# 줄만 믿으면 이미 죽은 터널을 상한까지 기다린다.
zombie=""
if command -v python3 >/dev/null 2>&1; then
  # 파이썬은 자식을 자동으로 거두지 않는다 — sleep 이 끝나면 확실한 좀비가 된다.
  # (bash 로는 안 된다: bash 는 백그라운드 작업을 알아서 거둔다.)
  exec 4< <(python3 -c 'import subprocess,time
p = subprocess.Popen(["sleep", "0.2"])
print(p.pid, flush=True)
time.sleep(20)' 2>/dev/null)
  read -r zombie <&4
  parent_of_zombie=$!
fi
if [ -n "$zombie" ]; then
  # 좀비가 될 때까지 기다린다.
  for _ in 1 2 3 4 5 6 7 8 9 10; do
    state="$(sed 's/.*) //' "/proc/$zombie/stat" 2>/dev/null | cut -d' ' -f1)"
    [ "$state" = "Z" ] && break
    sleep 0.3
  done
  check "좀비 프로세스를 만들었다" "$state" "Z"
  if process_alive "$zombie"; then
    fail=$((fail + 1)); printf '  FAIL 좀비를 살아 있다고 봤다 (죽은 터널을 상한까지 기다린다)\n'
  else
    pass=$((pass + 1)); printf '  ok   좀비는 죽은 것으로 본다\n'
  fi
  started=$SECONDS
  wait_until_alive "http://127.0.0.1:1" 45 "$zombie"
  check "좀비를 보고 있으면 곧바로 접는다" "$((SECONDS - started))" "0"
  kill "${parent_of_zombie:-0}" 2>/dev/null
  exec 4<&-
else
  printf '  --   좀비 검사 건너뜀 (python3 없음)\n'
fi

# 살아 있는 것은 살아 있다고 봐야 한다 — 위 검사만 있으면 항상 거짓을 돌려도
# 통과한다.
sleep 20 & live_pid=$!
if process_alive "$live_pid"; then
  pass=$((pass + 1)); printf '  ok   돌고 있는 프로세스는 살아 있다고 본다\n'
else
  fail=$((fail + 1)); printf '  FAIL 돌고 있는 프로세스를 죽었다고 봤다 (멀쩡한 터널을 접는다)\n'
fi
kill "$live_pid" 2>/dev/null; wait "$live_pid" 2>/dev/null

# pid 없이 부르는 자리(bml use 등)가 그대로 돌아야 한다 — 인자를 하나 늘린
# 변경이 조용히 그쪽을 깨는 것이 이 종류의 흔한 사고다.
started=$SECONDS
wait_until_alive "http://127.0.0.1:1" 3
rc=$?
elapsed=$((SECONDS - started))
check "pid 를 안 주면 예전처럼 시간으로만 센다" "$rc" "1"
if [ "$elapsed" -ge 3 ] && [ "$elapsed" -le 20 ]; then
  pass=$((pass + 1)); printf '  ok   상한을 지킨다 (%d초)\n' "$elapsed"
else
  fail=$((fail + 1)); printf '  FAIL 상한 3초인데 %d초 걸렸다\n' "$elapsed"
fi

# --- 000 이 어느 층에서 끊긴 것인가 -----------------------------------------

# 실제로 일어난 일 (2026-08-22): `curl https://a1ef13c23c42c8.lhr.life/api/health`
# 가 `SSL_ERROR_SYSCALL` 과 000 을 냈다. 이름은 풀렸고 443 에도 붙었는데 TLS
# 손을 잡다가 끊긴 것 — 7844 를 막던 그 망의 장비가 SNI 의 도메인을 보고
# 끊었다. 터널은 멀쩡히 살아 있었다. 이것을 "터널이 안 됐다" 로 읽으면 사람은
# 멀쩡한 터널을 닫고 처음부터 다시 한다.

# 이름이 없는 주소는 dns 에서 걸려야 한다 — .invalid 는 절대 풀리지 않는다(RFC 2606).
check "풀리지 않는 이름은 dns 층" \
  "$(tunnel_block_layer https://bml-test.invalid)" "dns"

# 아무도 안 듣는 곳은 tcp 층 — 443 에 못 붙는다.
# (이 기계가 443 을 쓰고 있으면 이 검사는 뜻이 없다. 건너뛴다.)
if ss -ltn 2>/dev/null | grep -qE '[:.]443[[:space:]]'; then
  printf '  --   tcp 층 검사 건너뜀 (이 기계가 443 을 쓰고 있다)\n'
else
  check "443 이 안 열린 곳은 tcp 층" \
    "$(tunnel_block_layer https://127.0.0.1)" "tcp"
fi

# 주소에 이상한 글자가 섞이면 셸에 넘기지 않는다.  이 값은 우리가 로그에서
# 뽑아낸 것이라 원칙적으로 안전하지만, 셸 명령에 붙는 자리는 좁혀 둔다.
check "명령이 섞인 이름은 넘기지 않는다" \
  "$(tunnel_block_layer 'https://evil.example.com;touch /tmp/bml-pwned')" "unknown"
if [ -e /tmp/bml-pwned ]; then
  fail=$((fail + 1)); printf '  FAIL 주소에 섞인 명령이 실행됐다\n'; rm -f /tmp/bml-pwned
else
  pass=$((pass + 1)); printf '  ok   주소에 섞인 명령이 실행되지 않는다\n'
fi

# 그리고 층마다 다음에 할 일이 달라야 한다.
contains "dns 는 터널이 닫혔을 가능성을 말한다" "$(block_layer_meaning dns)" "닫혔"
contains "tcp 는 이 망이 막는다고 말한다"       "$(block_layer_meaning tcp)" "이 망이"
contains "tls 는 다른 망 가능성을 말한다"        "$(block_layer_meaning tls)" "다른 망에서는 열릴 수 있습니다"
contains "짚지 못하면 짚지 못했다고 말한다"      "$(block_layer_meaning unknown)" "짚지 못했습니다"

# tls·tcp 로 판정되면 "다시 열어 보라" 고 하면 안 된다 — 멀쩡한 터널을 닫는
# 안내다.  화면 분기가 실제로 갈라져 있는지 코드에서 확인한다.
if grep -q 'case "$tlayer" in tls|tcp)' "$HERE/../bml" \
   && grep -q 'case "$layer" in' "$HERE/../bml"; then
  pass=$((pass + 1)); printf '  ok   tls·tcp 는 다시 열라고 하지 않는 갈래로 간다\n'
else
  fail=$((fail + 1)); printf '  FAIL 층에 따라 안내가 갈리지 않는다\n'
fi

# --- 확인이 안 됐을 때 화면이 뭘 말하는가 -----------------------------------

# 1분을 이미 물어봤으면서 "curl 로 직접 확인해 보세요" 로 끝나면 안 된다.
# 우리가 본 코드를 남기고, 그것을 화면에 옮긴다.
if grep -q 'tunnel.last-code' "$HERE/../bml" \
   && grep -q 'tunnel_code_meaning "$code"' "$HERE/../bml"; then
  pass=$((pass + 1)); printf '  ok   확인 실패 시 본 코드를 남기고 화면에 옮긴다\n'
else
  fail=$((fail + 1)); printf '  FAIL 확인에 실패한 이유를 화면이 말하지 않는다\n'
fi

echo
echo "이름이 안 잡힐 때 — 터널이 닫힌 것과 이 기계의 DNS 는 다르다"
# 실제 화면: "터널은 살아 있는데, 여기서는 확인이 안 됐습니다" 바로 밑에
# "터널이 이미 닫혔거나" 가 찍혔다.  두 줄이 서로 부딪히고, 사람은 멀쩡한
# 터널을 닫고 처음부터 다시 한다.  살아 있는 줄 알면 앞쪽은 배제된다.
check "살아 있으면 '닫혔거나' 를 말하지 않는다" \
  "$(block_layer_meaning dns 1 | grep -c '이미 닫혔')" "0"
check "그때는 이 기계의 DNS 라고 짚는다" \
  "$(block_layer_meaning dns 1 | grep -c 'DNS 가 그 도메인을 거르는')" "1"
# 반대로 살아 있는지 모르면 두 가능성을 다 남긴다 (§0.4).
check "모르면 두 가능성을 다 남긴다" \
  "$(block_layer_meaning dns | grep -c '이미 닫혔거나')" "1"
# tls·tcp 는 터널과 무관하다는 판정이라 원래대로다.
# TLS 손잡기를 실제로 해 본 적이 없다 — /dev/tcp 로 붙어만 봤다.  그러니
# "SNI 를 보고 끊는다" 고 단정하면 안 된다 (Codex 리뷰 10번).
check "확인 못 한 것을 단정하지 않는다" \
  "$(block_layer_meaning tls | grep -c '확인한 것은 아닙니다')" "1"
check "그래도 다른 망 가능성은 말한다" \
  "$(block_layer_meaning tls | grep -c '다른 망에서는 열릴 수 있습니다')" "1"

# 그리고 그 단정과 아래 안내가 어긋나면 안 된다.  "터널은 붙어 있다" 고 적어
# 놓고 세 줄 밑에서 "이 기계의 망 문제일 수 있습니다" 로 물러서면, 사람은
# 약한 쪽을 믿고 멀쩡한 터널을 닫는다.  dns 도 tls·tcp 와 같은 취급이어야 한다.
check "dns 도 단정하는 분기에 있다" \
  "$(grep -c 'tls|tcp|dns)' "$HERE/../bml")" "1"

echo
echo "이름이 안 잡힐 때 — 터널이 죽은 것과 이 망의 DNS 는 대처가 정반대다"
# 노트북에서 `bml use <터널 주소>` 가 'Could not resolve host' 로 죽었다.
# 그 화면은 "터널이 닫혔나 보다" 로 읽히는데, 실제로는 이 랩 망의 DNS 가
# lhr.life 를 거르고 있었다.  둘을 안 가르면 멀쩡한 터널을 닫고 다시 열기를
# 반복하게 된다.  그래서 이 기계의 resolver 를 건너뛰고 공용 DNS 에 묻는다.
check "답이 실려 있으면 있는 것" \
  "$(dns_public_json_verdict '{"Status":0,"Answer":[{"data":"1.2.3.4"}]}')" "exists"
check "NXDOMAIN 이면 없는 것" \
  "$(dns_public_json_verdict '{"Status":3,"Question":[]}')" "missing"
check "빈 칸으로 띄운 것도 읽는다" \
  "$(dns_public_json_verdict '{"Status": 3}')" "missing"
# "Answer" 라는 글자만 보면 안 된다 — SERVFAIL 응답에도 빈 배열로 들어 있다.
check "Status 가 0 이 아니면 모른다" \
  "$(dns_public_json_verdict '{"Status":2,"Answer":[]}')" "unknown"
check "답이 비어 있으면 모른다" \
  "$(dns_public_json_verdict '{"Status":0,"Answer":[]}')" "unknown"
# 확실한 신호가 없으면 단정하지 않는다 (§0.4) — 틀리게 단정하면 살아 있는
# 터널을 닫거나, 죽은 터널을 기다리게 만든다.
check "대답이 없으면 모른다"       "$(dns_public_json_verdict '')"        "unknown"
check "모르는 모양이면 모른다"     "$(dns_public_json_verdict 'garbage')" "unknown"

echo
echo "이름이 막혔어도 IP 로 직접 물어본다 — 여기서 알 수 있는 것은 여기서 안다"
# 이름이 잡히는 것과 터널이 살아 있는 것은 다르다 (lhr.life 는 와일드카드라
# 아무 이름이나 같은 IP 로 잡힌다).  예전에는 거기서 멈추고 "휴대폰으로 열어
# 봐야 압니다" 로 끝났는데, 공용 DNS 가 IP 를 줬으면 `curl --resolve` 로
# resolver 를 건너뛰고 진짜 답을 받을 수 있다.
check "DoH 응답에서 A 레코드를 뽑는다" \
  "$(printf '%s' '{"Status":0,"Answer":[{"name":"a.lhr.life","type":1,"data":"64.227.135.145"}]}' \
     | tr ',{}' '\n\n\n' | sed -n 's/.*"data":"\([0-9][0-9.]*\)".*/\1/p' | head -n 1)" \
  "64.227.135.145"
# CNAME 이 먼저 실려 오는 응답에서 이름을 IP 로 착각하면 curl 이 죽는다.
check "IP 가 아닌 data 는 건너뛴다" \
  "$(printf '%s' '{"Status":0,"Answer":[{"type":5,"data":"tunnel.example.com."},{"type":1,"data":"10.0.0.9"}]}' \
     | tr ',{}' '\n\n\n' | sed -n 's/.*"data":"\([0-9][0-9.]*\)".*/\1/p' | head -n 1)" \
  "10.0.0.9"
check "IP 없이 부르면 조용히 빈 값" "$(dns_public_ip '')" ""
# 막힌 갈래가 실제로 그 길을 타는지 -- 함수만 있고 안 부르면 화면은 그대로다.
check "막힌 갈래에서 IP 로 찔러 본다" \
  "$(grep -c 'tunnel_probe_by_ip "$url" "$tip"' "$HERE/../bml")" "1"
check "살아 있으면 그렇게 말한다" \
  "$(grep -c '막는 것은 이 기계의 DNS 하나뿐입니다' "$HERE/../bml")" "1"
# 사람에게 다른 기계를 꺼내라고 하기 전에, 이 기계에서 쓸 수 있는 길을 준다.
# 절차를 여기 적지 않고 **명령 하나**를 준다 -- 세 단계를 순서대로 치게 하면
# 한 단계씩 빠뜨리고, 터널 주소가 바뀔 때마다 처음부터 다시다.
# `bmlonly ${url}` 만 세면 안 된다 -- 주소 뒤에 IP 를 붙이는 판이 두 군데 더
# 생겼고(share 의 안내, 모든 DNS 가 막혔을 때의 안내), 그것들도 같은 글자로
# 시작한다.  이 갈래가 주는 것은 **주소만 붙인** 판 하나다.
check "브라우저까지 열 길도 함께 준다" \
  "$(grep -c 'bmlonly ${url}${OFF}' "$HERE/../bml")" "1"
check "그 명령이 무엇을 하는지도 적는다" \
  "$(grep -c '공용 DNS 로 주소 → 살아 있는지 확인' "$HERE/../bml")" "1"
# hosts 를 실제로 고치는 곳은 `cmd_only` 한 곳뿐이어야 한다 -- 두 곳이면
# 한쪽만 고쳐지고, 그때 어느 쪽이 돌았는지는 화면으로 알 수 없다.
check "hosts 를 고치는 곳은 한 곳" \
  "$(grep -c 'sudo tee -a /etc/hosts' "$HERE/../bml")" "2"

echo
echo "주소에서 호스트만 (셸에 넘기기 전에 좁힌다)"
check "스킴과 경로를 뗀다"      "$(url_host https://a.lhr.life/api/health)" "a.lhr.life"
check "포트도 뗀다"             "$(url_host http://192.168.0.7:5003)"      "192.168.0.7"
# 이 값이 그대로 nslookup/curl 에 들어간다.  글자를 안 좁히면 주소 한 줄로
# 남의 명령을 실행시킬 수 있다.
check "이상한 글자는 거부한다"  "$(url_host 'https://a;rm -rf/' || echo REFUSED)" "REFUSED"
check "빈 값도 거부한다"        "$(url_host '' || echo REFUSED)"           "REFUSED"
# userinfo 를 안 떼면 curl 이 가는 곳과 우리가 진단하는 곳이 달라진다.
check "userinfo 를 뗀다"        "$(url_host 'https://u:p@real.example/path')"  "real.example"
# 앞이 '-' 인 이름은 nslookup·dig 의 옵션 인자로 먹힐 수 있다.
check "앞이 - 면 거부한다"      "$(url_host 'https://-debug' || echo REFUSED)" "REFUSED"
check "빈 라벨도 거부한다"      "$(url_host 'https://x..y' || echo REFUSED)"   "REFUSED"
# authority 를 먼저 끊지 않으면 fragment·query 안의 @ 를 userinfo 로 읽는다 —
# 그러면 남의 도메인을 우리 터널로 판정한다.
check "fragment 뒤의 @ 에 속지 않는다" "$(url_host 'https://custom.example#@x.lhr.life')" "custom.example"
check "query 뒤의 @ 도 마찬가지"       "$(url_host 'https://custom.example?a@x.lhr.life')" "custom.example"
check "그때 우리 터널로 보지 않는다" \
  "$(is_our_tunnel_url 'https://custom.example#@x.lhr.life' && echo yes || echo no)" "no"

echo
echo "같은 망에서는 '중추 서버에서 확인해 보라' 가 갈라 주지 못한다"
# 실제로 겪은 것: 데스크톱과 노트북이 같은 랩 망이라 둘 다 똑같이 실패했다.
# 그 화면의 확인 절차는 전부 같은 망 안에서 도는 것이라 아무것도 못 가른다.
# 망 밖(모바일 데이터)에서 한 번 찔러 보는 것만이 그 경우를 가른다.
#
# 바깥 세상을 재지 않는다.  예전에는 이 줄이 진짜로 lhr.life 에 나갔고, 그러면
# **거기가 뭐라 답하느냐가 어느 갈래를 타느냐를 정한다**.  lhr.life 는 와일드
# 카드라 없는 서브도메인에도 503 을 돌려주므로, 나갈 수 있는 기계(CI 러너)에서는
# 위의 502/503 갈래가 먼저 return 해 이 두 줄이 아예 안 찍혔다 -- 나갈 수 없는
# 기계에서는 000 이라 통과했다.  같은 코드가 망에 따라 갈렸다.
#
# 여기서 재려는 것은 "확정 코드가 없을 때 같은 망 안내가 나오는가" 하나다.
# 그러니 세 갈림길을 다 고정한다: 코드는 000(못 나감), 이름은 잡히는 것으로
# (DNS 갈래를 건너뛴다), curl 한 줄은 안 부른다.
HELP="$( http_code_of() { printf '000'; }
         getent() { return 0; }
         explain_unreachable() { :; }
         server_unreachable_help https://a1b2c3.lhr.life 2>&1 )"
check "망 밖에서 찔러 보라고 한다" "$(printf '%s\n' "$HELP" | grep -c '모바일 데이터로 그 주소를')" "1"
check "같은 망이면 안 갈린다고 말한다" "$(printf '%s\n' "$HELP" | grep -c '같은 망이면')" "1"

echo
echo "터널 주소인가 — 아무 https 나 터널로 보면 안 된다"
# 예전에는 https:// 면 전부 터널로 봤다.  그러면 오타 하나에도 "bml share stop
# 후 다시 bml share" 를 시킨다 — 열지도 않은 터널을 닫으라는 말이다.
check "lhr.life 는 우리 것"        "$(is_our_tunnel_url https://a.lhr.life && echo yes || echo no)" "yes"
check "trycloudflare 도 우리 것"   "$(is_our_tunnel_url https://x.trycloudflare.com/y && echo yes || echo no)" "yes"
check "localhost.run 도 우리 것"   "$(is_our_tunnel_url https://z.localhost.run && echo yes || echo no)" "yes"
check "남의 https 는 아니다"       "$(is_our_tunnel_url https://lab.example.org && echo yes || echo no)" "no"
check "오타 도메인도 아니다"       "$(is_our_tunnel_url https://typo.example.invalid && echo yes || echo no)" "no"
check "LAN 주소는 당연히 아니다"   "$(is_our_tunnel_url http://192.168.0.40:5003 && echo yes || echo no)" "no"
# 이름을 흉내 낸 것도 아니다 — 접미사로만 인정한다.
check "이름만 비슷한 것은 아니다"  "$(is_our_tunnel_url https://evil-lhr.life.example.com && echo yes || echo no)" "no"

echo
echo "503 은 확정 신호지만, 무엇이 끊겼는지까지는 아니다"
# 두 번 겪었고 원인이 서로 달랐다.
#   1차: 중추 서버의 터널이 정말 끊겨 있었다.
#   2차(2026-08-24): 방금 연 터널이 503 이었고, 끊긴 것은 **서버** 였다.
# 화면에서 둘은 똑같다.  그래서 단정하지 않고, **값싼 확인을 먼저** 시킨다 --
# status 는 아무것도 안 바꾸고, 터널을 다시 여는 것은 주소를 잃는다.
DEAD="$( http_code_of() { printf '503'; }; server_unreachable_help https://a.lhr.life 2>&1 )"
check "응답이 없다고 말한다"       "$(printf '%s\n' "$DEAD" | grep -c '뒤에서 응답이 없습니다')" "1"
check "둘 다 가능하다고 말한다"    "$(printf '%s\n' "$DEAD" | grep -c '구분되지 않습니다')" "1"
# 순서가 요점이다.  bml status 가 bml share stop 보다 먼저 나와야 한다.
STATUS_LINE="$(printf '%s\n' "$DEAD" | grep -n 'bml status' | head -1 | cut -d: -f1)"
SHARE_LINE="$(printf '%s\n' "$DEAD" | grep -n 'bml share stop' | head -1 | cut -d: -f1)"
if [ -n "$STATUS_LINE" ] && [ -n "$SHARE_LINE" ] && [ "$STATUS_LINE" -lt "$SHARE_LINE" ]; then
  pass=$((pass + 1)); printf '  ok   값싼 확인(status)을 먼저 시킨다\n'
else
  fail=$((fail + 1)); printf '  FAIL 주소를 잃는 절차를 먼저 시킨다 (status %s, share %s)\n' \
    "${STATUS_LINE:-없음}" "${SHARE_LINE:-없음}"
fi
# 서버가 내려간 경우에는 주소가 안 바뀐다는 것도 말해야 한다 -- 안 그러면
# 습관대로 터널부터 다시 연다.
check "서버만 띄우면 주소가 그대로임을 말한다" \
  "$(printf '%s\n' "$DEAD" | grep -c '주소도 그대로')" "1"
check "다시 여는 명령도 준다"      "$(printf '%s\n' "$DEAD" | grep -c 'bml share stop')" "1"
# 어느 줄을 보라고까지 말해야 한다.  '실행 중' 만 짚으면, 서버가 돌고 있는
# 경우에 화면은 다 맞는 말을 했는데도 사람이 엉뚱한 곳을 판다 (실측: 그렇게
# 됐다 — 답은 '공유 주소' 줄이 **없다** 는 것이었다).
check "실행 중 줄을 짚는다"        "$(printf '%s\n' "$DEAD" | grep -c "'실행 중' 이 없다")" "1"
check "공유 주소 줄도 짚는다"      "$(printf '%s\n' "$DEAD" | grep -c "'공유 주소' 가 없다")" "1"
check "점검표를 훑게 하지 않는다"  "$(printf '%s\n' "$DEAD" | grep -c '중추 서버 쪽에서 순서대로')" "0"
# 확정 코드가 있으면 curl 의 첫 대답은 안 찍는다.  두 번 물어보면 답이 다를 수
# 있어서, 실제 화면에 `HTTP 000` 바로 밑에 `(HTTP 503)` 이 나란히 찍혔다 —
# 화면이 스스로 모순되면 사람은 어느 쪽을 믿을지부터 정해야 한다.
check "모순되는 첫 대답을 안 찍는다" "$(printf '%s\n' "$DEAD" | grep -c 'curl 이 말한 것')" "0"
# 404 는 다른 뜻이다 — 주소는 닿는데 우리 서버가 아니다.
WRONG="$( http_code_of() { printf '404'; }; server_unreachable_help https://a.lhr.life 2>&1 )"
check "404 는 다르게 말한다"       "$(printf '%s\n' "$WRONG" | grep -c '우리 워크벤치가 아닙니다')" "1"

echo
echo "터널이 스스로 죽으면 status 가 그렇게 말한다"
# 주소 파일은 남고 프로세스만 없다 (SSH 가 끊기면 그렇게 된다).  예전에는 그때
# 공유 관련 줄이 통째로 사라졌고, 그러면 "터널이 죽었다" 와 "애초에 안 열었다"
# 가 같은 화면이 된다 -- 없는 줄은 근거가 아니다.
# cmd_status 를 통째로 돌리려면 git·포트·서버까지 다 세워야 한다.  여기서
# 못 박을 것은 그 화면에 **그 줄이 있는가** 이므로 소스에서 직접 본다.
if grep -q '터널이 죽어 있습니다' "$HERE/../bml"; then
  pass=$((pass + 1)); printf '  ok   죽었으면 죽었다고 적는다\n'
else
  fail=$((fail + 1)); printf '  FAIL 죽은 터널을 침묵으로 넘긴다\n'
fi
if sed -n "/! tunnel_running && \[ -n \"\$(tunnel_url)\" \]/,/^  fi/p" "$HERE/../bml" | grep -q 'bml share'; then
  pass=$((pass + 1)); printf '  ok   다시 여는 명령을 함께 준다\n'
else
  fail=$((fail + 1)); printf '  FAIL 죽었다고만 하고 무엇을 할지 안 준다\n'
fi

echo
echo "보여 준다고 해 놓고 침묵하지 않는다"
# 실제 화면: "tunnel.log 의 마지막 줄:" 뒤에 아무것도 안 나왔다.  빈 줄을
# 걸러 냈더니 남는 게 없었던 것인데(배너만 찍고 죽는 경우), 사람은 자기 화면이
# 잘린 줄 안다.  없으면 없다고 말하고, 그때 할 일까지 준다.
check "빈 로그면 없다고 말한다"   "$(grep -c '남은 말이 없습니다' "$HERE/../bml")" "1"
# 세 곳이다: nokey 로 여는 곳, 등록한 키로 여는 곳, 그리고 그 옵션이 왜
# 있는지 설명하는 안내 문구.  포워딩이 실패했는데 조용히 붙어 있으면 주소만
# 받고 아무것도 안 열린다.
check "그때 다시 열라고 안내한다" "$(grep -c 'ExitOnForwardFailure' "$HERE/../bml")" "3"

echo "등록한 키로 열면 주소가 안 바뀐다 (설정한 사람만)"
# localhost.run 은 등록하지 않은 키를 거부한다 (Permission denied (publickey) --
# 실측).  등록 전에 키를 강제하면 그때부터 bml share 가 죽으므로, 키를 적어 둔
# 사람만 그 길을 탄다.
check "키가 없으면 nokey 그대로" "$(WORKBENCH_TUNNEL_KEY= ; tunnel_ssh_key || echo none)" "none"
check "없는 파일은 안 쓴다" \
  "$(WORKBENCH_TUNNEL_KEY=/does/not/exist tunnel_ssh_key || echo none)" "none"
check "키가 있으면 그것으로" \
  "$(WORKBENCH_TUNNEL_KEY="$HERE/../bml" tunnel_ssh_key)" "$HERE/../bml"
# nokey@ 는 익명이라 붙을 때마다 새 이름을 받는다.  키 쪽은 사용자 이름 없이
# `-i` 로 붙는다 (지금은 되살리는 감독자 스크립트 안에 있다).
check "키 쪽은 nokey@ 를 안 쓴다" \
  "$(grep -c 'IdentitiesOnly=yes' "$HERE/../bml")" "1"
# 두 곳이다: nokey 경로와 감독자 안.  keepalive 가 빠지면 학교망이 유휴 TCP 를
# 끊어도 이쪽은 모르고, 살아 있는 것처럼 보이는데 엣지는 503 을 돌려준다.
check "양쪽 다 keepalive 를 건다" \
  "$(grep -c 'ServerAliveInterval=30' "$HERE/../bml")" "2"

echo
echo "주소가 왜 바뀌었는지 화면에서 갈린다"
# 등록한 키는 주소가 그대로여야 하는데 실제로 바뀐 적이 있다
# (653712d5fb509b -> d1c47a7b4af191).  "등록한 키" 라고만 하면 무엇을 확인해야
# 하는지가 안 보인다 -- 키를 다시 만들었는지, 다른 키를 보고 있는지, 등록을
# 안 한 키인지.  경로와 지문 한 줄이면 등록한 것과 눈으로 맞춰 볼 수 있다.
check "어느 키인지 적는다"        "$(grep -c 'say "  ${DIM}키: ${key}${OFF}"' "$HERE/../bml")" "1"
check "지문도 적는다"             "$(grep -c 'ssh-keygen -lf "${key}.pub"' "$HERE/../bml")" "1"
check "지문을 못 읽으면 넘어간다" "$(grep -c '\[ -n "$print_" \] &&' "$HERE/../bml")" "1"
# 키가 없으면 주소가 매번 바뀐다 -- 그 사실을 **여는 자리에서** 말한다.
# 나중에 "또 바뀌었는데" 를 듣고 나서 설명하면 그 사이 왕복이 전부 낭비다.
# `bml share key` 의 안내에도 같은 문장이 있다 -- 여는 자리의 것만 센다.
check "키 없이 열면 그렇다고 말한다" \
  "$(grep -c '등록한 키 없이 엽니다 — 주소가 열 때마다 바뀝니다' "$HERE/../bml")" "1"
check "고정하는 법도 함께"        "$(grep -c 'bml share key${OFF}${DIM} (한 번만)' "$HERE/../bml")" "1"

echo
echo "공용 DNS 도 막힌 망 — 한 곳만 물어보고 포기하지 않는다"
# 실측: 학교망에서 1.1.1.1 하나만 물어보다 셋(평문·DoH 포함)이 다 실패했다.
# 1.1.1.1 은 사설 게이트웨이 대역과 부딪히거나 통째로 차단되는 망이 있어서,
# "공용 DNS 가 막힌 망" 이 아니라 "이 한 곳이 막힌 망" 인 경우가 많다.
check "물어볼 곳이 셋이다"          "$(grep -c '^8\.8\.8\.8|' "$HERE/../bml")" "1"
check "9.9.9.9 도 있다"             "$(grep -c '^9\.9\.9\.9|' "$HERE/../bml")" "1"
check "이름이 아니라 IP 로 적는다"  "$(grep -c 'DNS_PROVIDERS="1\.1\.1\.1|' "$HERE/../bml")" "1"
# 세 곳을 다 물어보는지 -- 목록만 있고 안 돌면 화면은 그대로다.
# 단수형과 복수형 둘 다 이 목록을 돈다 (복수형은 A 레코드를 전부 낸다).
check "dns_public_ip 가 목록을 돈다"    "$(grep -c 'done <<EOF' "$HERE/../bml")" "3"

# 그마저 막히면 남는 길: 이름을 아는 기계가 IP 를 대신 읽어 준다.
check "bmlonly 가 IP 를 인자로 받는다" \
  "$(grep -c 'if \[ \$# -gt 1 \]; then shift; given_ip="\$\*"; fi' "$HERE/../bml")" "1"
check "받은 IP 면 DNS 를 안 탄다" \
  "$(grep -c '주소를 받아 왔습니다 — DNS 는 건너뜁니다' "$HERE/../bml")" "1"
# 이 문구는 주석에도 한 번 나온다 (인자 밀림 사고의 증상으로) -- 실제로
# 죽이는 자리만 센다.
check "IP 가 아닌 것은 거른다" \
  "$(grep -c 'die "IP 로 안 보입니다' "$HERE/../bml")" "1"
# 성공 갈래와 **실패 갈래 둘 다** 적어야 한다.  이 갈래로 오는 이유가 대개
# "이 기계의 DNS 가 그 도메인을 거른다" 이고, 그러면 받는 쪽도 같은 랩 망이라
# 같은 벽에 부딪힌다 -- 성공 갈래에만 있으면 정작 필요할 때 없다.
check "IP 안내가 한 곳에 모여 있다" \
  "$(grep -c 'bmlonly ${url} ${ip}' "$HERE/../bml")" "1"
# 셋이다: 확인 안 된 갈래, 우리 도메인으로 열린 갈래, 그냥 열린 갈래.
# 이 갈래로 오는 이유가 대개 "이 기계의 DNS 가 거른다" 이고 받는 쪽도 같은 벽에
# 부딪히므로, 어느 갈래에서도 IP 줄이 빠지면 안 된다.
check "세 갈래 모두에서 부른다" \
  "$(grep -c 'tunnel_ip_hint "$url"' "$HERE/../bml")" "3"
# **못 얻어도 조용하지 않다.**  한때는 덤인 줄로 보고 조용히 넘겼는데, 이
# 기계도 같은 랩 망이라 공용 DNS 가 막혀 있고 그러면 안내가 통째로 사라졌다 --
# 정작 그 줄이 받는 사람에게 줄 유일한 값인데.  받는 사람은 주소만 받고, 그
# 주소가 자기 기계에서 안 열리는 이유를 알 길이 없다.
check "IP 를 못 얻으면 그렇다고 말한다" \
  "$(grep -c '주소는 이것인데 IP 는 못 알아냈습니다' "$HERE/../bml")" "1"
check "그때 어디서 IP 를 얻는지도 적는다" \
  "$(grep -c 'nslookup ${host} 1.1.1.1' "$HERE/../bml")" "1"
# 두 곳이다: 보내는 쪽(IP 를 못 알아냈을 때)과 받는 쪽(공용 DNS 가 다 막혔을
# 때).  둘 다 "IP 를 어디서든 구해 와서 뒤에 붙여라" 로 끝나야 한다.
check "막혔을 때 그 길을 알려 준다" \
  "$(grep -c 'bmlonly ${url} <그 IP>' "$HERE/../bml")" "2"
# 자기 resolver 를 먼저 쓴다.  바로 위에서 이 주소로 curl 을 쳐서 200 을 봤으니
# 대개 답을 안다 -- 공용 DNS 부터 물어보면 그것이 막힌 망에서 헛되이 실패한다.
check "자기 resolver 를 먼저 쓴다" \
  "$(awk '/^tunnel_ips\(\) \{/,/^\}/' "$HERE/../bml" | grep -c "getent ahostsv4")" "1"
# 순서는 뒤집혔다 (아래 "DNS 가 거짓말을 하는 망" 을 보라) -- 공용 DNS 가 먼저고
# 자기 resolver 가 그다음이다.  그 두 줄은 거기서 고정한다.
# 조건문("못 찾는다고 하면")으로 두면 저쪽이 한 번 실패해 알려 주고 이쪽이
# 그제서야 보내는 왕복이 주소가 바뀔 때마다 되풀이된다.  그냥 늘 준다.
check "보낼 줄을 조건 없이 준다" \
  "$(grep -c '받는 사람에게 이 두 줄을 그대로 보내세요' "$HERE/../bml")" "1"
# `bml share` 를 친 창은 이미 닫혔을 수 있다.  그때 이 값을 다시 보려고 멀쩡한
# 터널을 닫았다 여는 일이 실제로 있었고, 그러면 주소가 바뀌어 문제가 하나 는다.
check "status 에서도 같은 줄을 낸다" \
  "$(grep -c 'tunnel_ip_hint "$(tunnel_url)"' "$HERE/../bml")" "1"
# 엣지가 회전 풀이다.  실측: 같은 이름이 3.208.46.244 와 3.234.18.192 로 갈렸다.
# 하나만 건네면 그 노드가 빠질 때 받는 기계가 다시 물어봐야 하는데, 그 기계는
# 물어볼 길이 없다 -- 그것이 이 명령이 있는 이유다.
check "A 레코드를 전부 뽑는 길이 있다" \
  "$(grep -c '^dns_public_ips() {' "$HERE/../bml")" "1"
check "받는 사람에게 IP 를 여럿 준다" \
  "$(grep -c 'ip="$(tunnel_ips "$host" | tr' "$HERE/../bml")" "1"
# 카톡으로 옮겨 적는 줄이라 길어지면 그 자체가 오타의 자리가 된다.
check "그래도 셋까지만" \
  "$(grep -c 'head -n 3' "$HERE/../bml")" "2"
check "중계기가 IP 를 여러 번 받는다" \
  "$(grep -c 'action="append"' "$HERE/../bml_relay.py")" "1"
check "붙다 실패하면 다음 IP 로 넘어간다" \
  "$(grep -c 'for ip in ips:' "$HERE/../bml_relay.py")" "1"
# 예전처럼 두 자리만 집으면 두 번째 IP 부터 조용히 버려진다.
check "별칭이 인자를 전부 넘긴다" \
  "$(grep -c 'cmd_only "\$@"; cmd_connect' "$HERE/../bml")" "1"
check "IP 마다 하나씩 검사한다" \
  "$(grep -c 'die "IP 로 안 보입니다: \$one"' "$HERE/../bml")" "1"

echo
echo "제자리에서 다시 띄우는 것은 터널을 무효로 만들지 않는다"
# 실측 2026-08-26: bml 이 새 커밋을 받아 낡은 서버를 갈아 끼우면서 터널을 닫았다.
# 주소가 사라지고, 그 뒤 bml status 는 공유에 대해 **한 마디도 안 했다** --
# 사람은 "안 뜨는뎅?" 으로 끝났다.  터널은 localhost:5003 을 가리키므로 같은
# 포트로 몇 초 뒤에 돌아오는 서버는 터널을 무효로 만들지 않는다.
check "다시 띄우는 자리는 모두 터널을 남긴다" \
  "$(grep -c 'cmd_stop --keep-tunnel' "$HERE/../bml")" "4"
# 진짜로 내리는 자리(bml stop)는 여전히 닫아야 한다 -- 서버 없는 터널은 남에게
# 오류 화면을 띄우는 주소일 뿐이다.
check "진짜로 내릴 때는 닫는다" \
  "$(grep -c 'stop|down)         cmd_stop ;;' "$HERE/../bml")" "1"
# 그리고 주소 기록조차 없을 때도 침묵하지 않는다.  두 갈래가 다
# `[ -n "$(tunnel_url)" ]` 로 막혀 있어서 세 번째 경우가 통째로 사라졌었다.
check "안 열려 있으면 그렇다고 적는다" \
  "$(grep -c '공유        \${DIM}안 열려 있습니다' "$HERE/../bml")" "1"
check "그 판정이 기록 없음까지 본다" \
  "$(grep -c '! tunnel_running && \[ -z "\$(tunnel_url)" \]' "$HERE/../bml")" "1"

echo
echo "주소가 정말 고정되는지는 저쪽이 안다 — 우리가 단정하지 않는다"
# "등록한 키를 쓰면 주소가 고정된다" 는 우리 가정이었고 실측에서 틀렸다:
# 같은 지문(SHA256:VOJgVgFM…)으로 주소가 셋이었다.
#   653712d5fb509b -> d1c47a7b4af191 -> 928ae9cbe83d4e
# 우리가 아는 것은 "어느 키를 쓰라고 적어 두었다" 까지다.  그 키가 계정에
# 실제로 올라가 있는지는 저쪽만 알고, 저쪽은 붙을 때마다 로그에 말해 준다.
check "여는 자리가 '등록한' 이라고 단정하지 않는다" \
  "$(grep -c 'localhost.run · 지정한 키' "$HERE/../bml")" "1"
check "keepalive 도 주소 고정을 단정하지 않는다" \
  "$(grep -c '등록한 키라 주소는 그대로입니다' "$HERE/../bml")" "0"
check "저쪽이 한 말을 그대로 옮기는 길이 있다" \
  "$(grep -c '^tunnel_account_note() {' "$HERE/../bml")" "1"
check "그 줄을 지어내지 않고 로그에서 고른다" \
  "$(grep -c "grep -iE 'authenticat|registered|your key" "$HERE/../bml")" "1"

echo
echo "연 사람이 자기 터널을 확인할 수 있어야 한다"
# 이 랩에서는 중추 서버 자신도 터널 도메인을 못 찾는다.  그러면 방금 연 터널이
# 정말 열렸는지를 **연 사람이 모르고**, 확인이 받는 사람이 열어 볼 때까지
# 미뤄진다 -- 그 왕복이 매번 든다.  이름만 막힌 것이면 IP 로 물어보면 된다.
check "IP 로 직접 확인하는 길이 있다" \
  "$(grep -c '^tunnel_verify_by_ip() {' "$HERE/../bml")" "1"
check "dns 갈래에서 실제로 부른다" \
  "$(grep -c 'vcode="$(tunnel_verify_by_ip "$url")"' "$HERE/../bml")" "1"
check "200 이면 열렸다고 단정한다" \
  "$(grep -c '터널이 정말 열렸습니다' "$HERE/../bml")" "1"
# 200 이 아니면 단정하지 않는다 -- 붙었는데 뒤가 조용한 것과 아예 못 나간 것은
# 대처가 다르다.
check "닿는데 응답이 없으면 그렇게 가른다" \
  "$(grep -c 'IP 로는 닿는데 그 뒤에서 응답이 없습니다' "$HERE/../bml")" "1"
check "IP 로도 못 나가면 그렇다고 한다" \
  "$(grep -c 'IP 로도 못 물어봤습니다' "$HERE/../bml")" "1"

echo
echo "이미 열려 있을 때도 보낼 줄을 준다"
# 터널이 서버 재시작을 살아남게 되면서 (제자리 재시작은 --keep-tunnel) 이
# 갈래가 제일 흔해졌다.  그런데 여기에는 보낼 줄도 저쪽이 한 말도 없었다 --
# 정작 그것을 보려고 치는 명령인데.  그러면 사람은 그것을 보려고 멀쩡한
# 터널을 닫았다 열고, 그때 주소가 바뀐다.
check "이미 열려 있어도 IP 줄을 낸다" \
  "$(grep -c 'tunnel_ip_hint "$open_url"' "$HERE/../bml")" "1"
check "저쪽이 한 말도 함께" \
  "$(grep -c 'tunnel_account_note' "$HERE/../bml")" "4"
# `bml use` 가 아니라 `bmlout` 이다 -- use 는 활성 주소를 통째로 바꾸고, 자리를
# 둘로 나눠 둔 뜻이 사라진다.
check "받는 쪽 명령을 bmlout 으로 준다" \
  "$(grep -c 'bmlout ${open_url}' "$HERE/../bml")" "1"

echo
echo "DNS 가 거짓말을 하는 망 — 건네기 전에 찔러 본다"
# 실측 2026-08-26: 이 랩의 resolver 가 터널 이름에 166.104.100.110 을 돌려줬다.
# 그것은 이 기계 자신과 같은 캠퍼스 대역이고 (접속 id 166.104.133.20), 진짜
# 엣지는 AWS 다 (공용 DNS: 3.234.18.192 · 3.208.46.244 · 54.172.225.3).
# 그 주소를 받는 사람에게 건네면 그 기계는 캠퍼스 안 엉뚱한 곳을 가리킨다.
check "공용 DNS 를 먼저 묻는다" \
  "$(grep -c 'out="$(dns_public_ips "$host")"' "$HERE/../bml")" "1"
# 자기 resolver 는 공용 DNS 가 다 막혔을 때만 (bmlonly 를 만든 그 상황).
check "자기 resolver 는 그다음일 때만" \
  "$(grep -c 'if \[ -z "$out" \] && command -v getent' "$HERE/../bml")" "1"
# DNS 를 믿지 않고 직접 확인한다 -- 인증서가 그 이름의 것이 아니면 떨어진다.
check "찔러 본 것만 고르는 길이 있다" \
  "$(grep -c '^tunnel_live_ips() {' "$HERE/../bml")" "1"
check "안내가 그것을 쓴다" \
  "$(grep -c 'live="$(tunnel_live_ips "$url"' "$HERE/../bml")" "1"
# 하나도 확인 못 했으면 확인된 값인 척하지 않는다 (0.4 -- 모르면 모른다고).
check "확인 못 했으면 그렇다고 적는다" \
  "$(grep -c '이 IP 는 여기서 확인하지 못했습니다' "$HERE/../bml")" "1"

echo
echo "우리 도메인 — 주소를 고정하는 유일한 길"
# 실측: 키를 등록해 인증까지 됐는데도 (authn: user … authenticated) 주소는 계속
# 랜덤이었다.  저쪽 배너가 스스로 답을 적어 준다 — custom domains.
check "도메인을 적어 두는 명령이 있다" \
  "$(grep -c '^cmd_share_domain() {' "$HERE/../bml")" "1"
check "share 가 그리로 보낸다" \
  "$(grep -c 'cmd_share_domain "${1:-}"' "$HERE/../bml")" "1"
# SSH 원격 전달의 bind 주소로 이름을 준다.
check "그 이름에 묶어서 연다" \
  "$(grep -c -- '-R \${bind}:localhost:\$PORT localhost.run' "$HERE/../bml")" "1"
check "도메인이 없으면 예전대로 80" \
  "$(grep -c 'local bind="80"' "$HERE/../bml")" "1"
# 키 없이 도메인만 적으면 그 도메인은 절대 안 나온다.  조용히 랜덤으로 열면
# 사람은 도메인이 되는 줄 알고 그 주소를 준다.
check "키 없이 도메인만 적은 것을 잡는다" \
  "$(grep -c '도메인이 적혀 있는데 키가 없습니다' "$HERE/../bml")" "1"
# **적어 둔 것과 저쪽이 준 것은 다른 일이다.**  DNS 가 안 돌았으면 저쪽은
# 조용히 랜덤 주소를 준다 -- 그것을 "됐다" 로 읽으면 고정하려고 도메인을 산
# 사람에게 제일 나쁜 결말이 된다.
check "그 이름이 정말 나왔는지 확인한다" \
  "$(grep -c '적어 둔 도메인(${want})이 아니라 다른 주소가 나왔습니다' "$HERE/../bml")" "1"
check "나왔으면 안 바뀐다고 말한다" \
  "$(grep -c '우리 도메인 · 이제 안 바뀝니다' "$HERE/../bml")" "1"
check "우리 도메인도 우리 터널로 본다" \
  "$(grep -c 'case "$h" in "$d"|\*.".$d") return 0 ;; esac' "$HERE/../bml")" "1"
# 고정 주소로 가는 길이 Cloudflare 로 바뀌었다 (ADR 0031).  localhost.run 의
# 커스텀 도메인은 $9/월(연납)이고 Cloudflare 터널은 무료다 -- 결과가 같은데
# 한쪽만 돈이 든다.  그래서 예전 CNAME(cd.localhost.run)·A 레코드 안내는
# **일부러 지웠다**: 두 길을 나란히 적어 두면 비싼 쪽을 고르는 사람이 나온다.
#
# 화면이 절차를 직접 말한다.  "문서를 보세요" 로 끝내면 그 문서가 이 망에서
# 안 열릴 수 있고, 정작 그 값이 필요한 사람이 못 본다.
check "옛 유료 길을 안 권한다" \
  "$(grep -c 'cd.localhost.run' "$HERE/../bml")" "0"
check "대시보드 두 곳을 적어 준다" \
  "$(grep -c 'one.dash.cloudflare.com' "$HERE/../bml")" "2"
# 세 자리 모두 같은 것을 가리켜야 한다.  터널이 우리 이름으로 안 나오는 이유는
# 거의 언제나 "대시보드에 그 이름이 없다" 이고, 그 셋이 사람이 여기 닿는 길의
# 전부다: 처음 설정할 때 · 이름을 적을 때 · 못 열렸을 때.  총 개수로 세면
# 한 자리를 지워도 다른 자리에 하나 늘리면 통과한다.
check "설정 절차가 어디를 가리킬지 말한다" \
  "$(awk '/^cf_setup_steps\(\) \{/,/^\}/' "$HERE/../bml" | grep -c 'Public Hostname')" "1"
check "이름을 적을 때도 말한다" \
  "$(awk '/^cmd_share_domain\(\) \{/,/^\}/' "$HERE/../bml" | grep -c 'Public Hostname')" "1"
check "못 열렸을 때 거기를 보라고 한다" \
  "$(awk '/^cmd_share\(\) \{/,/^\}/' "$HERE/../bml" | grep -c 'Public Hostname')" "1"
# 무료 요금제의 100 MB 상한.  우리 서버 상한은 512 MB 라, 랩 안에서 되던
# 파일이 밖에서만 안 되는 경우가 생긴다 -- 그때 화면은 우리 탓처럼 보인다.
check "100 MB 상한을 미리 말한다" \
  "$(grep -c '100 MB 를 넘으면 Cloudflare 가 막습니다' "$HERE/../bml")" "1"
# 이게 진짜 이득이다 -- 우리 도메인은 이 망의 차단 목록에 없다.
check "차단이 풀린다는 것도 말한다" \
  "$(grep -c '이 망의 DNS 차단 목록에 없습니다' "$HERE/../bml")" "1"
# 세 곳 이름을 화면에 적는다 -- "공용 DNS" 라고만 하면 어디를 물어본 것인지
# 모르고, 사내망 관리자에게 무엇을 열어 달라고 할지도 못 정한다.
check "어디에 물어봤는지 적는다" \
  "$(grep -c '1\.1\.1\.1 · 8\.8\.8\.8 · 9\.9\.9\.9' "$HERE/../bml")" "1"
check "휴대폰 갈래도 남긴다" \
  "$(grep -c '휴대폰(모바일 데이터)으로 그 주소를 열어 보면 갈립니다' "$HERE/../bml")" "2"

echo
echo "7844 이 막힌 것과 이름을 못 구한 것은 다르다"
BML0="$HERE/../bml"
# 이 망은 이름을 가로챈다 (ADR 0030).  이름이 엉뚱한 곳을 가리키면 붙을 리가
# 없는데, 예전 코드는 그때도 "7844/TCP 가 막혀 있습니다" 라고 단정했다.
# 대처가 정반대다: 포트가 막혔으면 Cloudflare 는 아예 못 쓰고 (quic 도 http2 도
# 같은 7844 를 쓴다), 이름만 못 구한 것이면 아직 아무것도 모르는 것이다.
check "이름부터 구한다"       "$(awk '/^edge_probe\(\) \{/,/^\}/' "$BML0" | grep -c 'dns_public_ips')" "1"
check "못 구하면 no-dns"      "$(awk '/^edge_probe\(\) \{/,/^\}/' "$BML0" | grep -c "printf 'no-dns'")" "1"
check "막혔으면 그 IP 도 낸다" "$(awk '/^edge_probe\(\) \{/,/^\}/' "$BML0" | grep -c "printf 'blocked %s'")" "1"
# 실제로 갈리는지.  .invalid 는 절대 안 풀린다 (RFC 2606).
probe_out="$( edge_probe() { local ip; ip=""; [ -z "$ip" ] && { printf 'no-dns'; return 1; }; }; edge_probe )"
check "이름이 없으면 포트를 탓하지 않는다" "$probe_out" "no-dns"
SH0="$(awk '/^cmd_share\(\) \{/,/^\}/' "$BML0")"
check "화면도 둘을 갈라 말한다"  "$(printf '%s' "$SH0" | grep -c '엣지 이름을 못 구했습니다')" "1"
# 두 자리에서 말한다: 길을 고를 때(SSH 로 넘어가며), 그리고 우리 이름으로 열려다
# 실패했을 때.  뒤쪽이 특히 중요하다 -- 거기서 7844 를 안 짚으면 사람은 대시보드
# 설정을 몇 번이고 다시 본다.  설정 문제가 아닌데.
check "막혔으면 어디에 못 붙었는지" "$(printf '%s' "$SH0" | grep -c '에 못 붙습니다')" "2"
check "설정 탓이 아니라고 말한다" \
  "$(printf '%s' "$SH0" | grep -c '설정 문제가 아니므로')" "1"
check "quic 도 http2 도 7844 임을 적는다" \
  "$(printf '%s' "$SH0" | grep -c 'quic 은 UDP, http2 는 TCP, 둘 다 7844')" "1"

echo
echo "모르는 말을 삼키지 않는다"
# 실측 2026-08-26: `bml share cf <토큰>` 을 옛 bml 에서 쳤더니 "cf" 를 그냥
# 무시하고 터널을 열었다 -- 화면은 "이미 열려 있습니다" 였고 토큰은 아무 데도
# 안 들어갔다.  **아무 일도 안 하고 성공처럼 보이는 것**이 최악이다.
check "모르는 하위 명령을 거절한다" \
  "$(printf '%s' "$SH0" | grep -c 'bml share 가 모르는 말입니다')" "1"
# 거절만 하고 끝내면 사람은 뭘 쳐야 할지 모른다.  주석 말고 **화면에 나오는
# 줄**을 본다 -- 주석까지 세면 설명을 지워도 시험이 통과한다.
check "쓸 수 있는 것을 나열한다" \
  "$(printf '%s' "$SH0" | grep '^ *say ' | grep -c 'bml share cf <토큰>')" "1"
# 그리고 애초에 그 기계가 옛 bml 을 들고 있으면 안 된다.  share 도 pull 한다.
check "share 도 최신으로 맞추고 간다" \
  "$(awk '/^    share\|tunnel\)/,/^      ;;/' "$BML0" | grep -c 'sync_repo')" "1"

echo
echo "우리 이름으로 여는 터널 (Cloudflare · ADR 0031)"
BMLF="$HERE/../bml"
# 토큰과 이름이 **둘 다** 있어야 한다.  하나만으로는 못 연다.
#
#   토큰만 → 어느 이름으로 나갔는지 이쪽이 모른다.  "열렸는가" 를 확인할
#            주소가 없으니 확인을 건너뛰게 되고, 그 순간 화면이 거짓말을 한다.
#   이름만 → 붙을 자격이 없다.  저쪽은 그 이름을 모르므로 아무 데도 안 나온다.
#
# 어느 쪽이든 조용히 랜덤 주소로 흘러가면 최악이다: 고정 주소를 설정한 사람은
# 열렸다는 말을 보고 `bml.<도메인>` 을 남에게 알려 주는데, 정작 열린 것은
# 랜덤 주소다.  화면은 성공이고 상대는 아무것도 못 연다.
( WORKBENCH_CF_TOKEN="" WORKBENCH_TUNNEL_DOMAIN="" ; tunnel_via_named 0 ) >/dev/null 2>&1
check "토큰도 이름도 없으면 안 연다" "$?" "1"
( WORKBENCH_CF_TOKEN="$(printf 'x%.0s' $(seq 1 60))" WORKBENCH_TUNNEL_DOMAIN="" ; tunnel_via_named 0 ) >/dev/null 2>&1
check "토큰만 있으면 안 연다"        "$?" "1"
( WORKBENCH_CF_TOKEN="" WORKBENCH_TUNNEL_DOMAIN="bml.example.kr" ; tunnel_via_named 0 ) >/dev/null 2>&1
check "이름만 있으면 안 연다"        "$?" "1"

# 이름 붙인 터널은 로그에 주소를 안 찍는다 -- 어느 이름으로 나갈지가 대시보드에
# 있고 cloudflared 는 그것을 모른 채 연결만 맺는다.  그래서 로그를 훑는
# `try_tunnel` 로는 영영 주소를 못 얻고 60번 세다 실패로 끝난다.
NAMED="$(awk '/^try_tunnel_named\(\) \{/,/^\}/' "$BMLF")"
check "로그에서 주소를 찾지 않는다"  "$(printf '%s' "$NAMED" | grep -c 'tunnel_url_from')" "0"
# 그래도 **열렸는지는 똑같이 확인한다.**  주소를 아는 것과 그 주소가 열린 것은
# 다른 일이고, 그 확인을 건너뛰는 순간 이 명령은 믿을 수 없는 것이 된다.
check "그래도 열렸는지는 확인한다"   "$(printf '%s' "$NAMED" | grep -c 'confirm_tunnel')" "1"
# 두 길이 같은 확인을 써야 한다.  갈라 두면 한쪽만 고치는 날이 온다.
check "확인은 한 군데서만 한다"      "$(grep -c '^confirm_tunnel() {' "$BMLF")" "1"
check "랜덤 쪽도 같은 확인을 쓴다"   "$(awk '/^try_tunnel\(\) \{/,/^\}/' "$BMLF" | grep -c 'confirm_tunnel')" "1"

# 이름 있는 터널은 `tunnel run --token`.  `--url` 은 랜덤 주소를 받는 쪽이다.
VIA="$(awk '/^tunnel_via_named\(\) \{/,/^\}/' "$BMLF")"
check "run --token 으로 붙는다"      "$(printf '%s' "$VIA" | grep -c -- 'tunnel --no-autoupdate run --token')" "1"
check "랜덤 주소를 받지 않는다"      "$(printf '%s' "$VIA" | grep -c -- '--url')" "0"
# QUIC(UDP)만 막힌 망이 있다.  http2 도 같은 7844 를 쓰지만 TCP 다 -- 랜덤 쪽과
# 같은 두 번째 시도가 여기에도 있어야 한다.
check "http2 로 한 번 더 시도한다"   "$(printf '%s' "$VIA" | grep -c -- '--protocol http2')" "1"

# 실패했다고 랜덤 주소로 흘러가지 않는다.  `cmd_share` 가 그 갈래를 아예 안 탄다.
SH="$(awk '/^cmd_share\(\) \{/,/^\}/' "$BMLF")"
check "우리 이름이 있으면 그 길뿐"   "$(printf '%s' "$SH" | grep -c '랜덤 주소로 대신 열지 않습니다')" "1"
check "그때 무엇을 볼지 말해 준다"   "$(printf '%s' "$SH" | grep -c 'one.dash.cloudflare.com')" "1"

# 토큰은 암호와 같은 급이다 -- 가진 사람은 그 터널로 붙을 수 있고, 사람들은 이
# 화면을 스크린샷으로 보낸다 (`bml password` 와 같은 이유).
CF="$(awk '/^cmd_share_cf\(\) \{/,/^\}/' "$BMLF")"
check "토큰 값을 다시 찍지 않는다"   "$(printf '%s' "$CF" | grep -c '값은 찍지 않습니다')" "1"
check "설정됨만 말한다"              "$(printf '%s' "$CF" | grep -cE '\$\{?(raw|token|WORKBENCH_CF_TOKEN)\}?\$?\{?OFF' )" "0"
# 잘려 붙은 토큰을 그대로 받으면, 다음 `bml share` 가 뜻 모를 오류로 죽는다.
check "짧으면 잘렸다고 말한다"       "$(printf '%s' "$CF" | grep -c '잘려서 붙은 것 같습니다')" "1"

# 우리 이름으로 연 터널에 localhost.run 계정 안내를 띄우면, 다 해 놓은 사람에게
# 아직 안 했다고 말하는 셈이 된다.
check "저쪽 계정 안내를 안 띄운다" \
  "$(awk '/^tunnel_account_note\(\) \{/,/^\}/' "$BMLF" | grep -c 'tunnel_cf_token >/dev/null && tunnel_domain >/dev/null && return 0')" "1"
# 열기 전에도 어긋남이 보여야 한다 -- 둘 중 하나만 적힌 상태는 열어 보기 전에는
# 티가 안 난다.
ST="$(awk '/^cmd_status\(\) \{/,/^\}/' "$BMLF")"
check "status 가 고정 이름을 적는다" "$(printf '%s' "$ST" | grep -c '고정 — 열어도 안 바뀝니다')" "1"
check "반쪽 설정을 status 가 잡는다" "$(printf '%s' "$ST" | grep -c '토큰만 있고 이름이 없습니다')" "1"

echo
echo "이름이 막힌 기계 — hosts 대신 중계기로"
# 예전 방식(/etc/hosts)이 이 랩에서 특히 나빴던 이유는 셋이다: 브라우저가
# Windows 에 있어서 WSL 의 hosts 를 안 보고(관리자 PowerShell 이 한 번 더),
# WSL 이 켤 때마다 hosts 를 다시 만들고(재부팅하면 사라짐), 터널 주소가 열
# 때마다 바뀐다(그래서 그 둘을 매번 처음부터).  중계기는 셋을 통째로 없앤다.
check "중계기를 hosts 보다 먼저 시도한다" \
  "$(grep -c 'if relay_python >/dev/null 2>&1 && \[ -f "\$RELAY_SCRIPT" \]; then' "$HERE/../bml")" "1"
# 5003 이면 이 기계가 나중에 제 서버를 띄울 때 다툰다 -- 그때 "왜 남의
# 데이터가 보이지" 가 된다.
check "중계기 포트는 서버 포트와 다르다" \
  "$(grep -c 'RELAY_PORT="\${WORKBENCH_RELAY_PORT:-5013}"' "$HERE/../bml")" "1"
# 127.0.0.1 에만 연다.  0.0.0.0 이면 같은 망의 아무나 암호 화면까지 온다.
check "바깥에 열지 않는다" \
  "$(grep -c 'ThreadingHTTPServer(("127.0.0.1", args.listen), Relay)' "$HERE/../bml_relay.py")" "1"
# 인증서를 끄면 IP 로 붙는 순간 중간자를 못 본다.  이름으로 검증해야 한다.
check "인증서를 터널 이름으로 검증한다" \
  "$(grep -c 'server_hostname=host' "$HERE/../bml_relay.py")" "1"
check "검증을 끄는 길이 없다" \
  "$(grep -c 'CERT_NONE\|check_hostname = False' "$HERE/../bml_relay.py")" "0"
# 안 닿는 대상으로 띄우면 브라우저에 502 만 뜨고, 사람은 중계기가 아니라
# 워크벤치를 의심한다.
check "띄우기 전에 한 번 물어본다" \
  "$(grep -c -- '--check >/dev/null 2>&1 || return 1' "$HERE/../bml")" "1"
# 낡은 pid 파일이 가리키는 남의 프로세스를 죽이지 않는다 (CLAUDE.md 0.8).
check "우리 중계기임을 확인하고 죽인다" \
  "$(grep -c 'case "$cmd" in \*bml_relay.py\*) return 0 ;; esac' "$HERE/../bml")" "1"
# 기계를 껐다 켜면 중계기는 죽고 주소는 남는다.  되살리지 않으면 그때부터
# "응답하지 않습니다" 인데, 할 일은 다시 띄우는 것 하나다.
check "다음 bml 이 중계기를 되살린다" \
  "$(grep -c 'relay_revive || true' "$HERE/../bml")" "1"
check "되살릴 대상을 적어 둔다" \
  "$(grep -c 'RELAY_TARGET_FILE"$' "$HERE/../bml")" "1"
# 중계기를 거쳐 볼 때 "그 주소" 는 127.0.0.1 이다.  터널 진단을 그대로 내면
# 죄 없는 로컬 포트를 두고 DNS 를 의심하게 된다.
check "중계기일 때는 터널 진단을 내지 않는다" \
  "$(grep -c '이 주소는 이 기계 안의 중계기입니다' "$HERE/../bml")" "1"
check "bml stop 이 중계기도 내린다" \
  "$(grep -c '중계기도 내렸습니다' "$HERE/../bml")" "1"
check "status 가 무엇을 통해 보는지 적는다" \
  "$(grep -c '중계기     \${B}\${RELAY_URL}' "$HERE/../bml")" "1"

echo
if [ "$fail" -eq 0 ]; then
  printf '결과: %d개 통과\n' "$pass"
  exit 0
fi
printf '결과: %d개 통과, %d개 실패\n' "$pass" "$fail"
exit 1
