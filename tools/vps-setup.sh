#!/usr/bin/env bash
#
# 우리 VPS 한 대를 워크벤치의 대문으로 만든다 (ADR 0034).
#
#   [랩 PC]  bml 서버 :5003
#      └─ ssh -R 127.0.0.1:5003:127.0.0.1:5003 ─→ [이 VPS]
#                                                    nginx :443 (Let's Encrypt)
#                                                       └→ 127.0.0.1:5003
#
# **VPS 에서 한 번만 돌립니다.**  랩 PC 에서 돌리는 것이 아닙니다.
#
#   sudo bash vps-setup.sh bml.bmlwork.kr you@example.com
#
# 먼저 할 것이 둘 있습니다 (안 하면 인증서 발급이 timeout 납니다):
#   1. DNS 의 A 레코드가 **이미** 이 기계를 가리켜야 합니다 (회색 구름).
#   2. 80·443 이 **두 층 다** 열려 있어야 합니다 — Oracle Cloud 는 VCN 의
#      Security List/NSG 와 인스턴스 안의 iptables 가 따로 놉니다.
#      `--check` 로 먼저 재 보세요:  sudo bash vps-setup.sh --check <도메인>
#
# 왜 Cloudflare 프록시(주황 구름)를 안 쓰는가: 무료 요금제는 올리는 파일 하나가
# 100 MB 를 넘으면 막는다.  우리 상한은 512 MB 라, 랩 안에서 되던 파일이
# 밖에서만 안 되는 일이 생긴다 — 그때 413 은 우리가 준 것이 아닌데 화면은 우리
# 탓처럼 보인다.  DNS 만 Cloudflare 에 두고(회색 구름) TLS 는 여기서 끝낸다.

set -euo pipefail

# --- 인자 -------------------------------------------------------------------

CHECK_ONLY=0
if [ "${1:-}" = "--check" ]; then CHECK_ONLY=1; shift; fi

DOMAIN="${1:-}"
EMAIL="${2:-}"
PORT="${3:-5003}"
TUNNEL_USER="${TUNNEL_USER:-bml-tunnel}"

usage() {
  echo "사용: sudo bash vps-setup.sh <도메인> <이메일> [포트]" >&2
  echo "      sudo bash vps-setup.sh --check <도메인>        (열렸는지만 봅니다)" >&2
  echo "  예:  sudo bash vps-setup.sh bml.bmlwork.kr you@hanyang.ac.kr" >&2
  exit 2
}

# **아무것도 바꾸기 전에 검증한다** (Codex #5).  예전에는 비어 있는지만 보고
# root 로 파일을 쓰고 nginx 설정에 그대로 끼워 넣었다.  `../../ssh/sshd_config`
# 같은 도메인은 `/etc/nginx/sites-available/` 를 벗어나 **다른 파일을 자른다**
# (`realpath -m` 으로 확인할 수 있다).  줄바꿈이 든 포트는 nginx 지시어가
# 하나 더 생기는 것과 같다.
valid_domain() {
  # 라벨은 영숫자로 시작·끝나고, 가운데만 하이픈.  마지막 라벨은 글자만.
  printf '%s' "$1" | grep -qE '^([A-Za-z0-9]([A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}$'
}
valid_port() {
  case "$1" in ''|*[!0-9]*) return 1 ;; esac
  [ "$1" -ge 1 ] && [ "$1" -le 65535 ]
}

[ -n "$DOMAIN" ] || usage
valid_domain "$DOMAIN" || { echo "도메인 모양이 아닙니다: $DOMAIN" >&2; exit 2; }
valid_port "$PORT" || { echo "포트가 1–65535 가 아닙니다: $PORT" >&2; exit 2; }
if [ "$CHECK_ONLY" = "0" ]; then
  [ -n "$EMAIL" ] || usage
  case "$EMAIL" in *@*.*) ;; *) echo "메일 주소 모양이 아닙니다: $EMAIL" >&2; exit 2 ;; esac
fi

SITE="/etc/nginx/sites-available/$DOMAIN"
LINK="/etc/nginx/sites-enabled/$DOMAIN"
# 값이 통과해도 **경로가 그 폴더 안인지** 다시 본다.  검증과 사용 사이에
# 우리가 놓친 표기가 있을 수 있고, 그때 지는 쪽이 `/etc` 여서는 안 된다.
case "$(dirname "$(realpath -m "$SITE")")" in
  /etc/nginx/sites-available) ;;
  *) echo "도메인이 설정 폴더를 벗어납니다: $DOMAIN" >&2; exit 2 ;;
esac

# --- 열렸는지부터 (Codex #16) ------------------------------------------------

#: 80·443 이 **밖에서** 열렸는지.  Oracle Cloud 는 두 층이라 한쪽만 열면
#: 조용히 timeout 난다 — 그 timeout 은 certbot 실패로 보이지 우리 방화벽
#: 문제로 보이지 않는다.
check_ports() {
  local ok=0 ip
  ip="$(curl -fsS --max-time 8 https://api.ipify.org 2>/dev/null || true)"
  echo "▸ 이 기계의 공인 IP: ${ip:-못 구했습니다}"
  echo "▸ DNS 가 가리키는 곳:  $(getent hosts "$DOMAIN" | awk '{print $1}' | tr '\n' ' ')"
  for p in 80 443; do
    if ss -H -ltn "sport = :$p" | grep -q .; then
      echo "  :$p  이 기계 안에서는 열려 있습니다"
    else
      echo "  :$p  이 기계 안에서 아무도 안 듣고 있습니다"
      ok=1
    fi
  done
  cat <<'HINT'

  밖에서 안 열리면 두 층을 **둘 다** 봐야 합니다 (Oracle Cloud):
    1. VCN → Security List 또는 NSG 에 ingress 두 개
       source 0.0.0.0/0 · TCP · 80 과 443.  5003 은 **열지 마세요.**
    2. 인스턴스 안의 iptables — Oracle Ubuntu 이미지는 기본으로 막습니다.
       기존 규칙을 지우지 말고 reject 앞에 끼워 넣습니다:
         sudo iptables -I INPUT 6 -p tcp --dport 80  -j ACCEPT
         sudo iptables -I INPUT 6 -p tcp --dport 443 -j ACCEPT
         sudo netfilter-persistent save
       줄 번호(6)는 이미지마다 다릅니다 — `sudo iptables -L INPUT --line-numbers`
       로 REJECT 줄 앞자리를 확인하고 그 번호를 쓰세요.  UFW 로 고치지
       마세요 (Oracle 이 이 이미지에서 권하지 않습니다).
HINT
  return $ok
}

if [ "$CHECK_ONLY" = "1" ]; then
  check_ports || true
  exit 0
fi

[ "$(id -u)" = "0" ] || { echo "sudo 로 돌려 주세요." >&2; exit 2; }

# --- 이미 있는 것을 말없이 덮지 않는다 (Codex #6) -----------------------------

if [ -e "$SITE" ] || [ -e "$LINK" ]; then
  if [ "${BML_REPLACE:-}" != "1" ]; then
    echo "이미 $DOMAIN 설정이 있습니다 — 덮지 않고 멈춥니다." >&2
    echo "  정말 바꾸려면:  sudo BML_REPLACE=1 bash vps-setup.sh $DOMAIN $EMAIL" >&2
    echo "  (바꾸기 전에 .bak 으로 복사해 둡니다)" >&2
    exit 3
  fi
  [ -f "$SITE" ] && cp -a "$SITE" "$SITE.bak.$(date +%s)"
fi

echo "▸ 패키지"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq nginx certbot python3-certbot-nginx

# --- sshd: 전달된 포트는 127.0.0.1 에만 (Codex #4 · #7 · #10) -----------------

# 전용 사용자를 만든다.  랩 PC 의 키가 이 계정에 올라가고, 이 계정은
# **reverse forwarding 하나**만 할 수 있다 — shell 도 sudo 도 없다.  예전에는
# 평범한 관리 계정에 `ssh-copy-id` 를 시켰고, 그 키가 새면 VPS 셸과 (관리
# 계정이면) sudo 까지 함께 샜다.
if ! id "$TUNNEL_USER" >/dev/null 2>&1; then
  echo "▸ 전용 사용자 $TUNNEL_USER"
  useradd --create-home --shell /usr/sbin/nologin "$TUNNEL_USER"
fi
install -d -m 700 -o "$TUNNEL_USER" -g "$TUNNEL_USER" "/home/$TUNNEL_USER/.ssh"
touch "/home/$TUNNEL_USER/.ssh/authorized_keys"
chown "$TUNNEL_USER:$TUNNEL_USER" "/home/$TUNNEL_USER/.ssh/authorized_keys"
chmod 600 "/home/$TUNNEL_USER/.ssh/authorized_keys"

echo "▸ sshd — 그 사용자만, 127.0.0.1:$PORT 만"
# 메인 파일을 sed 로 고치지 않는다 (Codex #4).  Ubuntu 는 include 를 쓰고
# `Match` 블록이 값을 덮으므로, 한 모양만 바꿔서는 **실효값**을 모른다.
# drop-in 을 하나 두고 아래에서 `sshd -T` 로 실효값을 확인한다.
install -d -m 755 /etc/ssh/sshd_config.d
cat > /etc/ssh/sshd_config.d/60-bml-tunnel.conf <<CONF
# bml 이 만든 파일입니다 (ADR 0034).
# 전달된 포트를 wildcard 에 붙이지 않는다 — 붙으면 인터넷 아무나 :$PORT 로
# nginx 와 TLS 를 건너뛰고 들어온다.
GatewayPorts no

Match User $TUNNEL_USER
    GatewayPorts no
    PermitListen 127.0.0.1:$PORT
    AllowTcpForwarding remote
    PermitTTY no
    X11Forwarding no
    AllowAgentForwarding no
    # 랩 PC 가 자거나 랜이 빠지면 저쪽 listener 가 포트를 계속 잡는다.
    # 그러면 깨어난 감독자의 새 연결이 ExitOnForwardFailure 로 죽는다.
    ClientAliveInterval 30
    ClientAliveCountMax 3
CONF
sshd -t
# **실효값을 확인하고서야 넘어간다.**  못 읽으면 멈춘다 — 모르면서 열지 않는다.
if ! sshd -T -C "user=$TUNNEL_USER,host=localhost,addr=127.0.0.1" \
     2>/dev/null | grep -qi '^gatewayports no$'; then
  echo "sshd 의 실효 GatewayPorts 가 no 가 아닙니다 — 멈춥니다." >&2
  echo "  sudo sshd -T -C user=$TUNNEL_USER,host=localhost,addr=127.0.0.1 | grep -i gatewayports" >&2
  exit 4
fi
systemctl reload ssh 2>/dev/null || systemctl reload sshd

# --- nginx: 먼저 80 만, 인증서를 받고서 443 (Codex #1) ------------------------

# 공용 proxy 설정.  최종 443 블록과 임시 80 블록이 **같은 것**을 include 하므로
# `client_max_body_size` 나 SSE timeout 이 인증서 단계에서 사라지지 않는다.
cat > /etc/nginx/snippets/bml-proxy.conf <<CONF
# bml 이 만든 파일입니다 (ADR 0034).

# 20 MB .wrd 가 기본이고 긴 실험은 더 크다.  여기서 막으면 413 이 나는데 그
# 413 은 워크벤치가 준 것이 아니라 화면이 엉뚱한 곳을 가리킨다.
# 파일 상한(512 MiB)에 multipart 머리말 몫을 더해 둔다 — 정확히 512 MiB 인
# 파일이 boundary 때문에 여기서 먼저 걸리면 앱은 받아 주는데 문 앞에서 막힌다.
client_max_body_size 520m;
# 요청을 다 받아 두고 넘기지 않는다.  기본값이면 암호를 모르는 사람도 512 MB
# 를 이 기계 디스크에 쌓을 수 있다 — 401 은 그 뒤에 나간다.
proxy_request_buffering off;
client_body_timeout 120s;

location / {
    proxy_pass http://127.0.0.1:$PORT;
    proxy_http_version 1.1;
    proxy_set_header Host \$host;
    proxy_set_header X-Real-IP \$remote_addr;
    proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto \$scheme;
    proxy_buffering off;
    proxy_cache off;
    # 업로드가 길어도 끊기지 않을 만큼.  이것은 **응답을 기다리는** 시간이다.
    proxy_read_timeout 600s;
    proxy_send_timeout 600s;
}

# 실시간 갱신은 SSE 다 (20초 하트비트).  여기만 짧게 잡는다 — 서버가 조용해진
# 것을 한 시간이나 열어 두면 브라우저의 재연결도 그만큼 늦고, 화면은 그동안
# 남이 고친 것을 못 받는다.
location = /api/events {
    proxy_pass http://127.0.0.1:$PORT;
    proxy_http_version 1.1;
    proxy_set_header Host \$host;
    proxy_set_header X-Forwarded-Proto \$scheme;
    proxy_buffering off;
    proxy_cache off;
    proxy_read_timeout 75s;
}
CONF

echo "▸ nginx — 먼저 80 만 (인증서를 아직 안 받았습니다)"
# `listen 443 ssl` 을 인증서보다 먼저 쓰면 nginx 가 그 설정을 거절하고
# (`no "ssl_certificate" is defined ...`) certbot 이 제 검사에서 멎는다.
cat > "$SITE" <<CONF
# bml — 랩 PC 가 ssh -R 로 넘겨 준 $PORT 를 그대로 넘긴다 (ADR 0034).
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN;
    include snippets/bml-proxy.conf;
}
CONF
ln -sfn "$SITE" "$LINK"

# **default 를 지우지 않는다** (Codex #6 · #22).  전용 기계라는 계약이 없고,
# 지우면 모르는 Host 로 온 요청이 이 사이트로 떨어져 `$host` 로 301 하는
# open redirect 가 된다.  대신 모르는 이름을 거절하는 기본 서버를 둔다.
cat > /etc/nginx/sites-available/000-bml-default <<'CONF'
# bml 이 만든 파일입니다.  모르는 Host 는 여기서 끝난다.
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    return 444;
}
CONF
ln -sfn /etc/nginx/sites-available/000-bml-default /etc/nginx/sites-enabled/000-bml-default

nginx -t
systemctl reload nginx

echo "▸ 인증서 (Let's Encrypt)"
certbot --nginx -d "$DOMAIN" --agree-tos -m "$EMAIL" --non-interactive --redirect

# certbot 이 443 블록을 붙였다.  그 블록도 같은 snippet 을 보게 한다 —
# 안 그러면 업로드 상한과 SSE timeout 이 HTTPS 에서만 사라진다.
if ! grep -q 'include snippets/bml-proxy.conf' "$SITE"; then
  echo "certbot 이 고친 설정에 우리 snippet 이 없습니다 — 손으로 확인하세요:" >&2
  echo "  $SITE" >&2
  exit 5
fi
nginx -t
systemctl reload nginx

# 재부팅 뒤에도 서야 한다.  실패를 숨기고 "됐습니다" 를 내면 그 화면이 거짓말이
# 된다 (Codex #21).
systemctl enable --now nginx
systemctl is-enabled nginx >/dev/null
systemctl is-active  nginx >/dev/null

echo
echo "✓ 됐습니다."
echo
echo "  랩 PC 의 공개키를 이 계정에 올리세요 — **shell 이 없는 전용 계정**입니다."
echo "  랩 PC 에서:"
echo "    ssh-keygen -y -f ~/.ssh/id_ed25519    # 없으면 ssh-keygen -t ed25519"
echo "  그 한 줄을 이 기계에서 (앞의 제한을 **그대로** 붙여 주세요):"
echo "    sudo -u $TUNNEL_USER tee -a /home/$TUNNEL_USER/.ssh/authorized_keys <<'KEY'"
echo "    restrict,port-forwarding,permitlisten=\"127.0.0.1:$PORT\" ssh-ed25519 AAAA... 랩PC"
echo "    KEY"
echo
echo "  그 다음 랩 PC 에서:"
echo "    bml share vps $TUNNEL_USER@<이 기계의 IP 또는 이름>"
echo "    bml share domain $DOMAIN"
echo "    bml share"
echo
echo "  확인:"
echo "    이 기계에서   ss -H -ltn 'sport = :$PORT'   → 127.0.0.1 하나여야 합니다"
echo "    밖에서        nc -vz <이 기계> $PORT         → 실패해야 합니다"
echo "    갱신          sudo certbot renew --dry-run"
