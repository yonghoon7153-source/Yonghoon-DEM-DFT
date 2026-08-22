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

# 5xx 는 반대다 — 우리는 나갔고, 터널 쪽이 아직 우리 서버에 못 붙었다.
# Cloudflare 는 530, localhost.run 은 502 를 준다.
contains "530 은 터널이 못 붙었다고 말한다" "$(tunnel_code_meaning 530)" "붙지 못했습니다"
contains "502 도 같은 갈래다"               "$(tunnel_code_meaning 502)" "붙지 못했습니다"
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
if [ "$fail" -eq 0 ]; then
  printf '결과: %d개 통과\n' "$pass"
  exit 0
fi
printf '결과: %d개 통과, %d개 실패\n' "$pass" "$fail"
exit 1
