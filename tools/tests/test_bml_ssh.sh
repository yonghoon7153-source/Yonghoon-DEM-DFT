#!/usr/bin/env bash
#
# 노트북에서 이 WSL 로 들어오는 ssh 문 (`bml ssh`).
#
# 이 문이 잘못 열리면 눈에 안 띄는 방식으로 잘못된다.  여기서 잡는 것 넷:
#
#   1. **22 번을 쓰지 않는다.**  Windows 에도 OpenSSH 서버가 있고 켜져 있으면
#      22 번을 잡는다.  mirrored 에서는 접속이 **되긴 되는데** 들어간 곳이
#      Windows 다 — 저장소도 venv 도 없는 곳에서 "왜 파일이 없지" 가 된다.
#   2. **암호 로그인을 켜지 않는다.**  WSL 계정은 암호가 없거나 약하고, 랜에
#      열어 둔 문이라 한 번 뚫리면 데이터가 그대로 딸려 간다.
#   3. **`sshd_config` 을 건드리지 않는다.**  드롭인만 쓴다 — 통째로 지우면
#      원래대로 돌아가고, 무엇이 우리 것인지 헷갈릴 일이 없다.
#   4. **드롭인을 안 읽는 기계에 조용히 쓰지 않는다.**  `Include` 줄이 없으면
#      파일은 써지는데 아무 일도 안 난다 (그것이 제일 나쁜 실패다).
#
# 사용: bash tools/tests/test_bml_ssh.sh     (실패 0 이면 exit 0)

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
trap 'rm -rf "$TMP"' EXIT

BML_SOURCE_ONLY=1 . "$BML"

echo "포트"
check "기본은 2222 — 22 는 Windows 의 OpenSSH 서버 몫으로 비워 둔다" \
      "$(ssh_port)" "2222"
check "22 를 쓰겠다고 적으면 그대로 쓴다 (사람의 결정이다)" \
      "$(WORKBENCH_SSH_PORT=22 ssh_port)" "22"
check "숫자가 아니면 기본으로 — 포트 자리에 빈 값이 들어가면 sshd 가 안 뜬다" \
      "$(WORKBENCH_SSH_PORT=abc ssh_port)" "2222"
check "안 적었으면 기본" "$(WORKBENCH_SSH_PORT= ssh_port)" "2222"

echo
echo "설정 조각"
check "sshd_config 이 아니라 드롭인에 쓴다" \
      "$BML_SSHD_DROPIN" "/etc/ssh/sshd_config.d/bml.conf"

# 드롭인을 읽는지 보는 판정.  진짜 /etc 를 건드리지 않으려고 함수를 그대로
# 흉내낸다 — 여기서 보려는 것은 **어떤 줄을 Include 로 보느냐** 뿐이다.
reads() {
  printf '%s' "$1" | grep -qE '^[[:space:]]*Include[[:space:]]+/etc/ssh/sshd_config\.d/'
}
reads "Include /etc/ssh/sshd_config.d/*.conf" \
  && { pass=$((pass+1)); echo "  ok   Include 줄이 있으면 읽는다고 본다"; } \
  || { fail=$((fail+1)); echo "  FAIL Include 줄이 있는데 못 읽는다고 했다"; }
reads "#Include /etc/ssh/sshd_config.d/*.conf" \
  && { fail=$((fail+1)); echo "  FAIL 주석 처리된 Include 를 살아 있다고 봤다"; } \
  || { pass=$((pass+1)); echo "  ok   주석 처리된 Include 는 안 읽는 것으로 본다"; }

echo
echo "켤 때 나가는 말"
# 진짜로 apt 를 돌리지 않고 안내만 본다.  `ssh_next_steps` 가 그 안내 전부다.
out="$(windows_lan_address() { printf '192.168.0.40'; }
       windows_home_verified() { printf ''; }
       wsl_has_systemd() { return 1; }
       wsl_own_ip() { printf '172.20.1.2'; }
       ssh_next_steps 2222 2>&1)"

has   "접속 주소가 bmlin 과 같은 랩 안 주소다" "$out" "192.168.0.40"
has   "포트를 붙인 ssh 명령을 그대로 준다" "$out" "ssh -p 2222"
has   "방화벽은 Private 로만 연다 — 카페 와이파이에서까지 열리면 안 된다" \
      "$out" "-Profile Private"
has   "mirrored 가 아니면 포워딩 명령을 주소까지 채워서 준다" \
      "$out" "connectaddress=172.20.1.2"
has   "그 주소가 다시 뜰 때마다 바뀐다는 것을 말한다" "$out" "바뀝니다"
has   "systemd 가 아니면 다시 뜰 때 꺼진다는 것을 말한다" "$out" "systemd"
#: 제일 자주 걸리는 자리.  나머지를 다 해 놓고도 이것 때문에 "어제는 됐는데"
#: 가 된다 — 안내에 없으면 아무도 못 짚는다.
has   "WSL 이 떠 있어야 닿는다는 것을 말한다" "$out" "WSL 이 떠 있어야"

echo
echo "mirrored 이면 포워딩 얘기를 하지 않는다"
conf="$TMP/.wslconfig"
printf '[wsl2]\nnetworkingMode=mirrored\n' > "$conf"
out2="$(windows_lan_address() { printf '192.168.0.40'; }
        windows_home_verified() { printf '%s' "$TMP"; }
        wsl_has_systemd() { return 0; }
        ssh_next_steps 2222 2>&1)"
hasnt "mirrored 에서는 netsh 를 시키지 않는다" "$out2" "netsh interface portproxy"
has   "그 대신 필요 없다고 적는다" "$out2" "포워딩은 필요 없습니다"
hasnt "systemd 면 '다시 뜨면 꺼진다' 를 말하지 않는다" "$out2" "sshd 는 꺼져 있습니다"

echo
echo "모르는 인자"
out3="$(cmd_ssh nonsense 2>&1)"; rc=$?
check "모르는 대상은 거절한다" "$rc" "1"
has   "무엇을 쓸 수 있는지 적는다" "$out3" "on | off | status"

echo
printf '결과: %d개 통과' "$pass"
[ "$fail" -gt 0 ] && printf ', %d개 실패' "$fail"
printf '\n'
[ "$fail" -eq 0 ]
