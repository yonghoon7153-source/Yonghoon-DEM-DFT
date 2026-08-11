#!/usr/bin/env bash
# 로컬(WSL) 쪽 V100 접속 셋업 — `ssh v100` 한 단어로 붙게 만든다.
#
# ★ scripts/setup_v100.sh 와 다른 것: 저건 **V100 안에서** 도는 환경 재건이고,
#   이건 **내 WSL 에서** 도는 접속 설정이다.  둘 다 필요하다.
#
# 재대여마다 pem 파일명과 호스트가 바뀌므로 인자로 받는다:
#   bash scripts/setup_v100_local.sh /mnt/c/Users/안용훈/Downloads/Tesla_V100_20260811_092016.pem
#   bash scripts/setup_v100_local.sh <pem> [user@host] [port]
#
# 하는 일:
#   ① pem 을 ~/.ssh/ 로 복사 + chmod 600
#      (⚠ /mnt/c 는 drvfs 라 chmod 가 안 먹는다 → Windows 경로에 둔 채로는 SSH 가
#        "Permissions 0777 are too open" 으로 **거부**한다.  복사가 필수.)
#   ② ~/.ssh/config 에 Host v100 블록을 쓴다 (있으면 교체 = 멱등)
#   ③ 연결 스모크
#
# 그 뒤로는 이렇게 쓴다:
#   ssh v100                      # 접속
#   scp figure.png v100:~/        # 파일 전송 (alias 와 달리 config 는 scp/rsync 도 먹는다)
#   rsync -av v100:~/se_curve/ ./se_curve/
set -uo pipefail
PEM="${1:-}"
DEST="${2:-ubuntu@machine.runyour.ai}"
PORT="${3:-22}"
HOSTALIAS=v100
fail() { echo "★★ $*" >&2; exit 1; }

[ -n "$PEM" ] || fail "pem 경로가 필요하다.
  예: bash $0 '/mnt/c/Users/안용훈/Downloads/Tesla_V100_20260811_092016.pem'"
[ -f "$PEM" ] || fail "pem 을 못 찾았다: $PEM"

USERPART="${DEST%@*}"; HOSTPART="${DEST#*@}"
[ "$USERPART" != "$DEST" ] || { USERPART=ubuntu; HOSTPART="$DEST"; }

echo "═══ ① pem → ~/.ssh (chmod 600) ═══"
mkdir -p ~/.ssh && chmod 700 ~/.ssh
KEY="$HOME/.ssh/$(basename "$PEM")"
cp -f "$PEM" "$KEY" || fail "복사 실패"
chmod 600 "$KEY"
PERM=$(stat -c '%a' "$KEY" 2>/dev/null || echo '?')
[ "$PERM" = "600" ] || fail "chmod 600 이 안 먹었다 (perm=$PERM) — ~/.ssh 가 /mnt/c 밑인가?"
echo "  $KEY  (perm $PERM)"

echo "═══ ② ~/.ssh/config 의 Host $HOSTALIAS 블록 (멱등 교체) ═══"
CFG="$HOME/.ssh/config"; touch "$CFG"; chmod 600 "$CFG"
# 기존 블록 제거: 'Host v100' 부터 다음 'Host ' 직전까지
awk -v h="Host $HOSTALIAS" '
  $0 ~ "^"h"([ \t]|$)" { skip=1; next }
  skip && /^Host[ \t]/  { skip=0 }
  !skip
' "$CFG" > "$CFG.tmp" && mv "$CFG.tmp" "$CFG"
cat >> "$CFG" <<EOF
Host $HOSTALIAS
    HostName $HOSTPART
    User $USERPART
    Port $PORT
    IdentityFile $KEY
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 10
    # ⚠ 대여 머신은 **같은 호스트명에 매번 다른 호스트키**로 온다.  기본 known_hosts 를
    #   쓰면 재대여 때마다 REMOTE HOST IDENTIFICATION HAS CHANGED 로 접속이 막힌다.
    #   그래서 이 Host 전용 known_hosts 로 분리한다 — 전역 검사를 끄는 것이 아니라
    #   **이 별칭에 한정**해 완화하는 것이고, 다른 호스트의 보호는 그대로다.
    #   (교환은 대여업체가 준 주소를 신뢰하는 것 = pem 을 받은 것과 같은 신뢰 수준.)
    UserKnownHostsFile ~/.ssh/known_hosts_v100
    StrictHostKeyChecking accept-new
EOF
chmod 600 "$CFG"
echo "  $CFG 에 Host $HOSTALIAS → $USERPART@$HOSTPART:$PORT"

echo "═══ ③ 연결 스모크 ═══"
if ssh -o ConnectTimeout=15 -o BatchMode=yes "$HOSTALIAS" 'echo "  접속 OK — $(hostname)"; nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null || echo "  (nvidia-smi 없음)"' 2>&1; then
  cat <<EOF

═══ 준비 끝 ═══
  ssh v100                        # 접속
  scp <파일> v100:~/              # 올리기
  rsync -av v100:~/Yonghoon-DEM-DFT/se_curve/ ./se_curve/   # 결과 내려받기

  V100 안에서 (최초 1회):
    git clone --branch claude/stoic-knuth-NObVQ \\
      https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT.git ~/dem-stoic
    bash ~/dem-stoic/scripts/setup_v100.sh
EOF
else
  echo "
  ⚠ 스모크 실패.  흔한 원인:
    · 머신이 아직 부팅 중 (1~2분 뒤 재시도)
    · 호스트/포트가 다름 → bash $0 '$PEM' 'ubuntu@<주소>' <포트>
    · pem 이 이 머신 것이 아님 (재대여 때 새로 받은 것인지 확인)
  수동 확인:  ssh -v $HOSTALIAS"
  exit 1
fi
