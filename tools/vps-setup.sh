#!/usr/bin/env bash
#
# 우리 VPS 한 대를 워크벤치의 대문으로 만든다 (ADR 0034).
#
#   [랩 PC]  bml 서버 :5003
#      └─ ssh -R 5003:localhost:5003 ─→ [이 VPS]
#                                          nginx :443 (Let's Encrypt)
#                                             └→ 127.0.0.1:5003
#
# **VPS 에서 한 번만 돌립니다.**  랩 PC 에서 돌리는 것이 아닙니다.
#
#   curl -fsSL <이 파일> -o vps-setup.sh
#   sudo bash vps-setup.sh bml.bmlwork.kr you@example.com
#
# 왜 Cloudflare 프록시(주황 구름)를 안 쓰는가: 무료 요금제는 올리는 파일 하나가
# 100 MB 를 넘으면 막는다.  우리 서버 상한은 512 MB 라, 랩 안에서 되던 파일이
# 밖에서만 안 되는 일이 생긴다 -- 그때 413 은 우리가 준 것이 아닌데 화면은 우리
# 탓처럼 보인다.  DNS 만 Cloudflare 에 두고(회색 구름) TLS 는 여기서 끝낸다.

set -euo pipefail

DOMAIN="${1:-}"
EMAIL="${2:-}"
PORT="${3:-5003}"

if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
  echo "사용: sudo bash vps-setup.sh <도메인> <이메일> [포트]" >&2
  echo "  예:  sudo bash vps-setup.sh bml.bmlwork.kr you@hanyang.ac.kr" >&2
  exit 2
fi
[ "$(id -u)" = "0" ] || { echo "sudo 로 돌려 주세요." >&2; exit 2; }

echo "▸ 패키지"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq nginx certbot python3-certbot-nginx

echo "▸ sshd — 원격 전달을 127.0.0.1 에만 묶는다"
# GatewayPorts 를 켜지 **않는다.**  켜면 전달된 포트가 0.0.0.0 에 열려서, 인터넷
# 아무나 :5003 으로 nginx 를 건너뛰고 들어온다 -- TLS 도 없이.  nginx 가 같은
# 기계 안에서 127.0.0.1 로 붙으므로 켤 이유도 없다.
if grep -qE '^\s*GatewayPorts\s+yes' /etc/ssh/sshd_config; then
  sed -i 's/^\s*GatewayPorts\s\+yes/GatewayPorts no/' /etc/ssh/sshd_config
  systemctl reload ssh 2>/dev/null || systemctl reload sshd
fi

echo "▸ nginx"
cat > "/etc/nginx/sites-available/$DOMAIN" <<CONF
# bml — 랩 PC 가 ssh -R 로 넘겨 준 $PORT 를 그대로 넘긴다.
server {
    listen 80;
    listen [::]:80;
    server_name $DOMAIN;
    location / { return 301 https://\$host\$request_uri; }
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name $DOMAIN;

    # 20 MB .wrd 가 기본이고 긴 실험은 더 크다.  여기서 막으면 413 이 나는데
    # 그 413 은 워크벤치가 준 것이 아니라 화면이 엉뚱한 곳을 가리킨다.
    client_max_body_size 512m;

    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

        # 실시간 갱신은 SSE 다 (`/api/events`).  버퍼링을 끄지 않으면 nginx 가
        # 응답을 모아 두고, 화면은 남이 고친 것을 영영 못 받는다.
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;

        # 업그레이드 헤더를 넘겨 둔다 -- 지금은 WebSocket 을 안 쓰지만, 쓰게
        # 되는 날 여기를 다시 찾아오는 것보다 낫다.
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
CONF
ln -sf "/etc/nginx/sites-available/$DOMAIN" "/etc/nginx/sites-enabled/$DOMAIN"
rm -f /etc/nginx/sites-enabled/default

echo "▸ 인증서 (Let's Encrypt)"
# certbot 이 80 으로 확인하므로 **DNS 가 이미 이 기계를 가리켜야** 한다.
certbot --nginx -d "$DOMAIN" --agree-tos -m "$EMAIL" --non-interactive --redirect

nginx -t && systemctl reload nginx
systemctl enable nginx >/dev/null 2>&1 || true

echo
echo "✓ 됐습니다."
echo
echo "  이제 랩 PC 에서:"
echo "    bml share vps <이 기계의 사용자>@<이 기계의 IP 또는 이름>"
echo "    bml share domain $DOMAIN"
echo "    bml share stop && bml share"
echo
echo "  랩 PC 의 공개키가 이 기계의 ~/.ssh/authorized_keys 에 있어야 합니다."
echo "  랩 PC 에서:  ssh-copy-id <사용자>@<이 기계>"
