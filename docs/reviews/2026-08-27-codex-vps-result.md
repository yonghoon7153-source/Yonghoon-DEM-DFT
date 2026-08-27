---
title: Codex 적대 리뷰 결과 — 우리 VPS 고정 대문
created: 2026-08-27
updated: 2026-08-27
type: review
tags: [review, audit, crosscheck, vps, ssh, nginx]
sources: [docs/reviews/codex-review-vps.md, docs/adr/0034-our-own-vps-in-front.md]
confidence: high
explored: false
verificationStatus: verified
---

# Codex 적대 리뷰 결과 — 우리 VPS 고정 대문 (승인 보류)

> Codex 가 작성한 독립 리뷰 원문이다. 소스는 고치지 않았고, Claude 쪽 자체
> 리뷰는 읽지 않았다. 실제 VPS 는 아직 없으므로 실행하지 못한 항목은 아래에
> 따로 밝혔다.  **원문 그대로 옮긴다 — 우리가 고른 대로 줄이지 않는다.**
>
> 우리 답은 [2026-08-27-codex-vps-reply.md](2026-08-27-codex-vps-reply.md).

- 과제: [codex-review-vps](codex-review-vps.md)
- 범위: `ce8adc94~1..HEAD` 중 `tools/vps-setup.sh`, `tools/bml` 의 VPS·stale
  갈래, ADR 0034 와 해당 시험
- 결론: **승인 보류.** 22건 — 높음 8 · 중간 9 · 낮음 5
- 먼저 막을 것: #1–#8. 지금 VPS 를 만들면 설치가 인증서 전에 멎고, 설령 손으로
  살려도 `bml stop` 이 VPS 터널을 못 닫으며, 원격 포트가 다른 IPv4 프로세스를
  조용히 공개할 수 있다.

## 검증 환경

- 코드보다 먼저 `CLAUDE.md` §0, ADR 0034와 과제 문서를 읽었다. 특히 §0.4의
  “모르면 None+이유”와 §0.8의 “우리 것임을 증명한 뒤에만 죽인다”를 판정
  기준으로 썼다.
- `tools/bml`과 `tools/vps-setup.sh`는 `bash -n`을 통과했다.
- `tools/tests/test_bml_tunnel.sh`의 논리적 233개 중 **229 passed, 1 failed,
  3 skipped**였다. skip은 이 Git Bash에 `python3`가 없어 못 만든 좀비 세 경우다.
  실패 하나는 `getent`가 없는 호스트에서 `.invalid`를 DNS가 아니라 TCP 층으로
  분류한 환경 차이다. VPS 지적의 재현 실패는 아니지만 시험은 완전 통과가 아니다.
- 추가로 `test_bml_client.sh`는 289 passed, 13 failed였다. 실패는 Windows Git
  Bash의 권한·심볼릭 링크·CRLF·interop 및 시험용 서버 제약에 모여 있어 이 범위의
  판정 근거로 세지 않았다.
- 집중 반례로 생성된 VPS 감독자 명령은 `WORKBENCH_PORT=6001`에서 실제로
  `-R 6001:localhost:6001`이었고, `looks_like_our_tunnel`은
  `.../vps-keepalive.sh`를 `no`로 판정했다.
- Ubuntu/nginx/sshd/Certbot/OCI VPS 실물은 없었다. 서버 쪽 항목은 소스와 공식
  매뉴얼 대조 및 아래의 재현 절차로 판정했으며, 실제 기계 실행으로 가장한 것은
  없다.

## 확인된 결함

| # | 심각도 | 파일:줄 | 증상 | 재현 또는 깨지는 입력 | 최소 수정 |
| ---: | :---: | --- | --- | --- | --- |
| 1 | 높음 | `tools/vps-setup.sh:48-95` | 인증서가 없는데 먼저 `listen 443 ssl` 사이트를 활성화한다. 첫 실행의 Certbot nginx 설정 검사가 실패하고, 깨진 사이트와 제거된 default가 디스크에 남는다. | 빈 Ubuntu에서 88–89행까지 적용한 뒤 `nginx -t`. `ssl_certificate`가 없다는 오류가 난다. 실제 VPS에서는 미실행했지만 [nginx HTTPS 설정](https://nginx.org/en/docs/http/configuring_https_servers.html)의 필수 쌍과 정면으로 어긋난다. | 유효한 HTTP-only 설정을 임시 설치하고 `nginx -t`·reload 후 Certbot을 실행한다. 그 다음 인증서 경로와 proxy 지시어가 함께 든 최종 443 설정을 원자적으로 설치하고 다시 검사한다. |
| 2 | 높음 | `tools/bml:3122-3131,3155-3167,3334-3358,3534-3581`; `tools/tests/test_bml_client.sh:1098-1104` | 소유 판정이 옛 `tunnel-keepalive.sh`만 인정하고 새 `vps-keepalive.sh`는 빠뜨렸다. `bml stop`은 감독자·자식 ssh를 남기고 PID·URL 표식만 지운다. 확인 실패 화면 뒤에도 orphan 감독자가 재시도하다 나중에 고정 도메인을 조용히 열 수 있다. | harmless `bash $RUN_DIR/vps-keepalive.sh` PID를 표식에 넣고 `close_tunnel`: 소유 판정 `no`, 반환 1, PID는 생존, 표식은 삭제됐다. 이 세션에서도 명령줄 판정 `vps-owned=no`를 재현했다. | 정확한 VPS 감독자 경로를 소유 판정에 넣고 시작시각/nonce도 표식에 둔다. 실제 감독자와 자식 ssh를 띄운 기능 시험에서 stop 뒤 둘 다 죽고, 확인된 경우에만 표식이 지워지는지 본다. |
| 3 | 높음 | `tools/bml:3531-3552`; `tools/vps-setup.sh:67`; `tools/tests/test_bml_tunnel.sh:734-738` | `-R`의 원격 listen 주소를 생략한다. OpenSSH는 loopback IPv4·IPv6를 시도하고 하나만 bind돼도 성공으로 답한다. `127.0.0.1:5003`을 다른 프로세스가 잡고 ssh가 `[::1]:5003`만 잡으면, nginx는 계속 IPv4의 **다른 프로세스**를 공개한다. | 일회용 VPS에서 `python3 -m http.server 5003 --bind 127.0.0.1` 뒤 현재와 같은 `ssh -N -o ExitOnForwardFailure=yes -R 5003:localhost:5003 ...`. ssh는 IPv6 하나로 성공할 수 있고 공개 URL은 선점 서버로 간다. [OpenSSH listener 구현](https://github.com/openssh/openssh-portable/blob/master/channels.c)도 주소 하나 성공을 전체 성공으로 센다. | `-R 127.0.0.1:${remote_port}:127.0.0.1:$PORT`로 양쪽 주소를 명시한다. `PermitListen 127.0.0.1:5003`을 걸고, IPv4 선점 시 연결이 반드시 실패하는 통합 시험을 둔다. |
| 4 | 높음 | `tools/vps-setup.sh:38-45`; `docs/adr/0034-our-own-vps-in-front.md:50-55` | 메인 파일의 `GatewayPorts yes` 한 모양만 고친다. Ubuntu의 include/drop-in, 대소문자, `Match User`의 유효값을 못 본다. effective 값이 `yes`면 5003이 wildcard에 붙어 nginx·TLS를 우회한다. | 일회용 VPS의 `/etc/ssh/sshd_config.d/`에 `GatewayPorts yes`를 둔 뒤 스크립트 실행. `sshd -T -C user=...,host=...,addr=...`와 터널 뒤 `ss -ltnp`에서 여전히 `yes`/wildcard인지 확인한다. | 전용 tunnel user 설정을 쓰고 `sshd -t` 뒤 그 사용자 조건의 `sshd -T -C`가 정확히 `gatewayports no`인지 확인하지 못하면 중단한다. 런타임에도 5003이 `127.0.0.1` 한 곳이며 외부 `nc VPS 5003`은 실패해야 한다. |
| 5 | 높음 | `tools/vps-setup.sh:22-36,48-93` | `DOMAIN`·`PORT`를 비어 있는지만 보고 root 쓰기와 nginx 보간에 쓴다. 경로 이동으로 `/etc`의 다른 파일을 truncate할 수 있고, PORT 개행은 nginx 지시어가 된다. 검증 전에 `apt-get`부터 바꾼다. | 실행하지 말고 `realpath -m /etc/nginx/sites-available/../../ssh/sshd_config`를 보면 `/etc/ssh/sshd_config`다. 즉 `DOMAIN=../../ssh/sshd_config`가 48행의 대상이 된다. `$'5003;\n...'` PORT도 설정 줄을 늘린다. | 어떤 변경보다 먼저 정규 FQDN, 기본 이메일, 숫자 1–65535를 검증하고 `/`, 제어문자, 빈·하이픈 경계 label을 거부한다. 최종 부모 경로가 정확히 `sites-available`인지 확인하고 링크·비정규 파일은 건드리지 않는다. |
| 6 | 높음 | `tools/vps-setup.sh:48,88-96` | 정상 도메인을 줘도 기존 site를 직접 truncate하고 `ln -sf`로 링크를 바꾸며 default를 삭제한다. 백업·원자 교체·실패 rollback이 없다. **재실행도** 기존 인증서 지시어를 먼저 지워 #1로 멎는다. | 일회용 컨테이너에 같은 이름의 기존 파일·enabled 링크·default를 만든 뒤 스크립트를 Certbot 실패까지 실행하고 `cmp`/`readlink`: 원본과 default가 돌아오지 않는다. | 기존 대상이면 기본 중단. 명시적 교체만 `cp -a` 백업과 같은 폴더 temp를 쓴다. temp 후보를 include한 임시 전체 설정으로 먼저 검사하거나, 원자 교체 직후 `nginx -t`가 실패하면 reload 전에 즉시 rollback한다. default는 지울 필요가 없다. Certbot도 [백업·rollback](https://eff-certbot.readthedocs.io/en/stable/using.html)을 전제로 쓴다. |
| 7 | 높음 | `tools/vps-setup.sh:101-107`; `tools/bml:3627-3628,3646-3656` | 보통 계정에 평범한 `ssh-copy-id`를 시킨다. 랩 PC 키가 유출되면 reverse tunnel 한 개가 아니라 VPS shell·임의 forwarding, OCI 기본 관리 계정이면 sudo까지 얻는다. | 안내대로 올린 키로 `ssh user@vps id`, 관리 계정이면 `ssh user@vps sudo -n id`. 둘 중 성공하는 권한은 이 앱에 필요 없다. | 비-sudo 전용 사용자를 만들고 authorized_keys를 `restrict,port-forwarding,permitlisten="127.0.0.1:5003"`로 제한한다. `Match User`에서 remote forwarding만, `PermitListen`, no PTY/agent/X11, `MaxSessions 0`을 적용하고 유효 설정을 검사한다. [sshd authorized_keys 제한](https://man.openbsd.org/sshd) 참고. |
| 8 | 높음 | `tools/bml:3334-3344,3396-3407`; `apps/api/app/main.py:197-204` | 공개 `/api/health`의 HTTP 200만 “이번 터널”로 인정한다. DNS가 옛 VPS B를 가리키거나 A의 5003에 옛 tunnel이 남은 상태에서 새 A 연결이 실패해도 B/옛 앱의 200을 성공으로 읽어 사용자를 다른 데이터로 보낸다. | 도메인은 건강한 B, `WORKBENCH_VPS`는 A로 두고 A의 새 reverse bind를 실패시킨다. B의 `/api/health`가 200이면 `confirm_tunnel`은 새 ssh 상태를 확인하기 전에 성공한다. 현재 시험은 임의 200을 진실로 mock한다. | 서버 시작마다 공개 가능하지만 예측할 필요 없는 instance nonce를 health 응답에 넣고 로컬 값과 공개 값을 비교한다. 이번 ssh의 forward-failure 로그/상태가 있으면 옛 endpoint의 200을 받지 않는다. |
| 9 | 중간 | `tools/vps-setup.sh:64,66-79`; `apps/api/app/main.py:125-147` | `proxy_buffering off`는 **응답**만 끈다. 요청은 기본 `proxy_request_buffering on`이라 nginx가 최대 512 MB를 임시 디스크에 다 받은 뒤에야 암호 gate로 보낸다. 암호 없는 공격자도 병렬 POST로 VPS 디스크·회선을 채울 수 있다. | 쿠키 없이 여러 `curl --data-binary @large.bin https://domain/api/not-found`를 보내며 nginx temp 경로와 `df`를 본다. 401은 각 body를 다 받은 뒤 온다. [nginx 요청 버퍼 문서](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_request_buffering)의 기본 동작이다. | `proxy_request_buffering off`로 gate까지 스트리밍하고, `client_body_timeout`·연결/요청 rate 제한을 명시한다. 이미 upstream HTTP/1.1이므로 chunked도 스트리밍할 수 있다. |
| 10 | 중간 | `tools/vps-setup.sh:38-45`; `tools/bml:3548-3552` | 클라이언트 `ServerAlive*`만 있고 서버 `ClientAlive*`는 없다. 랩 PC 절전·강제 종료·망 blackhole에서 VPS의 옛 sshd/listener가 OS TCP keepalive까지 5003을 잡으면 새 연결이 `ExitOnForwardFailure`로 계속 죽는다. | 터널 성립 뒤 FIN/RST 없이 랩→VPS 패킷을 DROP하거나 랩 PC를 강제 종료한다. VPS의 `ss`에서 5003 잔존, 새 `-R`의 bind failure를 확인한다. 실제 랩 절전 실측은 못 했다. | 전용 사용자에 `ClientAliveInterval 30`, `ClientAliveCountMax 3`을 두고 유효값을 검사한다. 약 90초 뒤 sleeping client가 정리되는 대가를 문서화하고, 깨어난 감독자가 재접속하게 한다. |
| 11 | 중간 | `tools/bml:3534-3567` | 감독자 파일을 직접 덮고 `cat`·`chmod` 실패를 검사하지 않는다. 링크를 따라 쓰거나, 쓰기 실패 뒤 옛 스크립트 경로를 성공으로 돌려 **옛 VPS/포트**를 실행할 수 있다. | temp `RUN_DIR`에서 `vps-keepalive.sh`를 다른 파일의 symlink로 만들거나 디렉터리를 읽기 전용으로 만든 뒤 `write_vps_keepalive`. 가리킨 파일 변경 또는 오류 뒤 성공 경로/낡은 내용 실행을 확인한다. | 링크·비정규 파일을 거부하고 같은 폴더 temp에 완성·검사·chmod한 뒤 원자 교체한다. 어느 단계든 실패하면 경로를 출력하지 말고 nonzero로 끝낸다. |
| 12 | 중간 | `tools/bml:3297-3310,3934-3955`; `tools/tests/test_bml_tunnel.sh:918-973` | 공개 probe 실패와 로컬 200만으로 “터널만 죽었다”고 단정해 닫는다. DNS/TLS/랩 인터넷 장애, 404, 429에서도 건강한 터널을 버린다. VPS 주소에는 “주소가 바뀝니다”도 거짓이다. | `server_alive(){ return 0; }`, 공개 probe 실패, `close_tunnel` 표식을 둔 현재 시험은 **닫힘을 정답**으로 통과한다. `.invalid`, TLS 차단, HTTP 429를 각각 넣어도 같은 행동이다. | VPS nginx의 502/504와 remote-loopback 실패처럼 backend 단절을 증명한 경우만 자기 자식을 재시작한다. DNS/TLS/404/429/unknown은 유지하고 판정 불가 이유를 낸다. 고정 VPS 주소와 랜덤 제공자 주소 안내를 분리한다. |
| 13 | 중간 | `tools/bml:3995-4005`; `tools/tests/test_bml_tunnel.sh:835-841` | VPS 갈래를 고르기 **전에** `ensure_cloudflared`를 무조건 실행한다. SSH만 쓸 새 PC도 불필요한 cloudflared 다운로드가 실패하거나 CPU가 미지원이면 정상 VPS를 시도조차 못 한다. | VPS·도메인은 설정하고 cloudflared 실행 파일/다운로드를 실패시킨 채 `cmd_share` 전체 실행. 4004행에 닿기 전 죽는다. 현재 시험은 소스에서 “VPS가 먼저 나온다”는 순서만 센다. | `ensure_cloudflared`와 실행 파일 검사를 Cloudflare 갈래 안으로 옮긴다. cloudflared가 전혀 없는 상태에서 VPS `cmd_share`를 끝까지 실행하는 회귀를 둔다. |
| 14 | 중간 | `tools/bml:102,3534-3552`; `tools/vps-setup.sh:24,49,67` | remote 포트와 로컬 앱 포트를 둘 다 `$PORT`로 묶는다. 도구가 직접 권하는 `WORKBENCH_PORT=6001 bml`을 쓰면 VPS nginx는 5003을 보는데 ssh는 6001에 remote listener를 만든다. | 이 세션에서 생성 함수를 실행해 `-R 6001:localhost:6001`을 확인했다. 기본 nginx는 `127.0.0.1:5003`이므로 공개 응답은 502다. | remote 기본은 5003, local target만 `$PORT`로 분리해 `-R 127.0.0.1:5003:127.0.0.1:6001`로 만든다. 설치 포트를 바꾸면 그 값을 별도 설정으로 명시 저장한다. |
| 15 | 중간 | `tools/bml:3548-3552,3617-3629` | 사전 probe는 `BatchMode=yes`지만 실패해도 설정을 저장하고, 실제 백그라운드 ssh에는 BatchMode가 없다. 키가 없고 password auth가 켜진 VPS에서는 `/dev/tty`/askpass를 기다려 quick-failure 상한도 작동하지 않을 수 있다. | 키 없는 password-enabled 시험 서버에 설정을 저장하고 nohup 감독자를 실행. ssh가 즉시 실패하지 않고 prompt/정지 상태에 남는지 본다. | 감독자에도 `BatchMode=yes`, `ConnectTimeout`을 넣는다. 사전 probe 실패를 저장 성공과 분리해 “아직 쓸 수 없음” 상태로 낸다. |
| 16 | 중간 | `tools/vps-setup.sh:33-36,91-95`; `docs/reviews/codex-review-vps.md:100-103` | OCI의 VCN Security List/NSG와 Ubuntu 인스턴스 iptables 두 층을 하나도 안내·검사하지 않는다. 기본 이미지에서는 80/443이 막혀 #1을 고쳐도 Certbot HTTP-01과 외부 접속이 timeout난다. | 새 OCI Ubuntu에서 두 방화벽을 그대로 둔 채 유효한 80 server와 Certbot 실행; 외부 80 timeout. 실제 인스턴스 실측은 못 했고 [OCI 이미지 방화벽](https://docs.oracle.com/en-us/iaas/Content/Compute/References/images.htm#Firewall_Rules)과 [웹 포트 절차](https://docs.oracle.com/en/learn/publish-webserver-using-oci/index.html)로 대조했다. | 아래 “Oracle 최소 절차”를 설치 전 필수 단계로 둔다. 80/443만 두 층에서 열고 5003은 둘 다 닫는다. |
| 17 | 중간 | `tools/vps-setup.sh:74-79`; `docs/adr/0034-our-own-vps-in-front.md:57-64`; `apps/api/app/live.py:74-101`; `apps/web/src/lib/live.ts:83-99` | `proxy_read_timeout 3600s`를 느린 **업로드** 보호라고 설명하지만 이는 upstream **응답 read 사이** 시간이다. SSE task가 첫 event 뒤 멎고 TCP만 열리면 브라우저 `onerror`·재연결도 최대 1시간 늦어져 화면이 stale하다. | **합성 재현 절차이며 실물에서는 미실행:** fault proxy나 시험 route로 `/api/events` 첫 yield 뒤 byte를 멈추고 다른 요청으로 revision을 올린다. 탭은 열린 EventSource로 남고 nginx가 약 1시간 뒤 끊을 때까지 갱신하지 않는다. [nginx 정의](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_read_timeout) 참고. | `/api/events` 전용 location에 `proxy_buffering off`, heartbeat 20초의 3회 정도인 `proxy_read_timeout 60s` 또는 75s를 둔다. 업로드는 `client_body_timeout`·request buffering으로 별도 설명한다. |
| 18 | 낮음 | `docs/adr/0034-our-own-vps-in-front.md:73-83`; `tools/bml:3642-3648` | 무료 자격과 동일 인스턴스의 존속을 섞어 “영영/평생”으로 읽히게 한다. Oracle은 7일 CPU·network 사용률 기준 아래인 Always Free 인스턴스를 idle로 회수할 수 있고, 조용한 relay가 후보가 될 수 있다. 도메인 이름은 유지돼도 재생성 전까지 대문은 죽는다. | OCI Monitoring에서 7일 지표를 본다. 실제 회수는 Oracle 재량이라 재현하지 못했다. 공식 [Always Free idle 회수 조건](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm#Idle_Compute_Instances)에 명시돼 있다. | ADR과 화면을 “주소는 DNS로 고정되지만 인스턴스는 회수될 수 있음”으로 고친다. reserved public IP, 외부 health 경보, 재생성·DNS 복구 절차를 둔다. 정책 회피용 가짜 부하는 권하지 않는다. |
| 19 | 낮음 | `tools/vps-setup.sh:62-64`; `apps/api/app/settings.py:31`; `apps/api/app/routers/runs.py:97-111`; `apps/api/app/routers/eis.py:872-874`; `apps/api/app/routers/gitt.py:222-224` | nginx의 512m은 파일이 아니라 multipart **전체 요청** 상한이다. API가 허용하는 정확히 512 MiB 파일도 boundary/header 때문에 nginx에서 413이 된다. 여러 EIS 부속 파일이면 더 일찍 넘는다. | `truncate -s 512M x.wrd` 후 `curl -F file=@x.wrd ...`. 앱 조건은 `>`라 파일 자체를 허용하지만 nginx request가 먼저 512m을 넘는다. | 파일 상한보다 multipart 여유가 있는 513–520m 정도로 request 상한을 두거나, 앱과 proxy가 같은 “요청 전체” 정의를 쓰게 한다. |
| 20 | 낮음 | `tools/bml:3535-3539,3584-3629` | 지원한다고 쓴 `사용자@호스트[:포트]`의 포트를 실제 keepalive는 쓰지만 사전 probe와 `ssh-copy-id` 안내는 무시한다. `u@h:`, `u@h:abc`, `u@@h`도 저장된다. | fake ssh로 `bml share vps ubuntu@host:443` 인자를 캡처하면 probe는 `-p 443` 없이 `ubuntu@host true`다. 위 세 깨진 문자열도 3611–3615행 검사를 통과한다. | parser 하나에서 user/host 비어 있음, `@` 한 개, 숫자 포트 1–65535를 검증하고 probe·안내·감독자가 같은 파싱 결과와 `-p`를 쓴다. |
| 21 | 낮음 | `tools/vps-setup.sh:95-99` | `systemctl enable nginx` 실패를 `|| true`로 숨긴 뒤 “됐습니다”를 낸다. 지금은 보여도 재부팅 뒤 대문이 사라지는 화면의 거짓이다. | 일회용 환경에서 `systemctl enable nginx`를 실패시키면 스크립트는 99행 성공 메시지까지 간다. | `enable --now` 실패를 전파하고 `is-enabled`·`is-active`를 확인한 뒤에만 성공을 말한다. |
| 22 | 낮음 | `tools/vps-setup.sh:50-55,88-89` | default를 없앤 뒤 이 site가 기본이 되며 redirect에 `$host`를 쓴다. 알 수 없는 Host도 공격자가 준 이름으로 301하는 open redirect가 된다. | `curl -I -H 'Host: evil.example' http://VPS-IP/x` → `Location: https://evil.example/x`. | redirect는 검증된 literal `$DOMAIN`으로 고정하고, 알 수 없는 Host는 별도 default server에서 거부한다. |

## 먼저 물은 세 가지

### A. Certbot 전에 nginx가 깨지는가

**맞다.** #1의 순서로 첫 실행이 막힌다. 최소 수정은 “80만 있는 유효 설정 →
`nginx -t`·reload → 인증서 발급 → 인증서 경로가 있는 최종 443 설정 → 다시
검사·reload”다. `client_max_body_size`, proxy headers, request/response buffering,
SSE timeout은 공용 snippet이나 최종 proxy location에 두면 잃지 않는다. Certbot에
최종 블록 생성을 맡기려면 먼저 HTTP proxy location에 그 지시어를 둬야 한다.

### B. 무조건 `Connection "upgrade"`

설정은 불필요하지만 **현재 SSE·일반 HTTP를 깨뜨리는 반례는 찾지 못했다.** nginx의
[WebSocket 공식 예시](https://nginx.org/en/docs/http/websocket.html)에도 단순형은
고정 `Connection "upgrade"`가 있고, 실제 전환은 client Upgrade와 upstream 101이
함께 있어야 한다. 지금 WebSocket이 없으므로 두 Upgrade header를 지우는 것이 가장
작다. 나중에 필요할 때 공식 `map $http_upgrade $connection_upgrade`나 WebSocket
전용 location을 넣는다. 이것은 확인된 22건에 세지 않았다.

### C. default site 삭제

전용 기계라는 계약도, 삭제 전 백업도 없으므로 안전하지 않다. 더구나 #1 실패와
결합하면 첫 실행이 기존 default를 끊고 깨진 site만 남긴다. `server_name`이 맞는
요청은 default를 남겨도 이 site로 오므로 삭제할 필요가 없다. 모르는 Host를 거부할
default를 따로 두는 편이 #22도 막는다.

## 여섯 질문에 대한 답

### 1. 절전·LAN 단절·`bml stop`에서 ssh가 죽는가

현재 답은 **보장되지 않는다.** `bml stop`은 #2 때문에 VPS 감독자를 아예 우리
것으로 인정하지 못해 확정적으로 남긴다. 여기서 위험한 것은 이미 exit한 zombie가
아니라 살아 있는 orphan 또는 멈춘 ssh다. zombie는 fd가 닫혀 VPS 포트를 잡지
못한다.

랩 PC가 깨어 있는 상태에서 망만 끊기면 `ServerAliveInterval=30`과
`ServerAliveCountMax=3`이 약 90초 뒤 client ssh를 끝내고 감독자가 다시 붙는다.
PC 자체가 잠들거나 전원이 빠지면 client 타이머도 멈추므로 VPS의 #10
`ClientAlive*`가 필요하다. 소유 누락을 고친 뒤에도 `kill -- -$pid`는 감독자가
그 프로세스 그룹 리더가 아니라 대개 실패하므로, trap으로 **자기 직계 child**를
죽이고 종료를 기다리는 기능 시험이 필요하다. 가장 단순한 구현은 supervisor를
별도 session/process group으로 띄우고 그 식별자를 저장해 확인된 그룹만 종료한 뒤
자식까지 사라졌는지 기다리는 것이다.

낮은 확률의 별도 §0.8 위험도 있다. `wait "$child"` 뒤 5초 sleep 동안 `child`에
끝난 PID가 남아 있고, 그 번호가 재사용된 순간 TERM을 받으면 trap이 남의 프로세스를
죽일 수 있다 (`tools/bml:3543-3564`). 작은 `pid_max` namespace의 PID churn으로는
만들 수 있지만 이 호스트에서는 재현하지 못해 본표에 세지 않았다. 최소한 wait
직후 `child=""`로 지우고 trap도 현재 직계 자식인지 확인해야 한다.

### 2. SSE·512 MB 업로드와 `ssh -R`

- SSE의 20초 heartbeat, 앱의 `X-Accel-Buffering: no`, nginx의
  `proxy_buffering off` 조합은 정상 경로에 충분하다. `ssh -R`은 HTTP buffer를
  한 층 더 만들지 않고 암호화된 TCP channel의 흐름제어·backpressure만 더한다.
- 3600초 read timeout은 업로드를 보호하지 않는다. 오히려 #17처럼 멎은 SSE를
  오래 열린 것으로 보이게 한다. `/api/events`는 60–75초로 분리하는 편이 맞다.
- 업로드는 기본 request buffering 때문에 먼저 VPS 디스크에 전부 쌓인다(#9).
  client가 계속 byte를 보내는 한 총 업로드 시간이 길다는 이유만으로 끊기지는
  않지만, byte 사이가 기본 `client_body_timeout`보다 길면 408이다. 터널이 중간에
  끊기면 이 앱에는 resume가 없어 처음부터 다시 올린다.
- 정확히 512 MiB 파일은 multipart overhead 때문에 #19의 413이 난다.

### 3. `GatewayPorts`

- 줄이 없으면 OpenSSH 기본값 `no`라 안전하다.
- `clientspecified`이고 현재처럼 bind 주소를 생략하면 client 요청 자체는 localhost라
  loopback이다. 다만 앞으로 `*`를 요청할 수 있고 “반드시 no”라는 서버 불변식은
  증명하지 못한다.
- `yes`는 client 요청을 wildcard로 덮어쓴다. 현재 grep은 include·Match를 못 봐
  #4가 된다. 공식 의미는 [sshd_config](https://man.openbsd.org/sshd_config)의
  `GatewayPorts`·`PermitListen`과 같다.

값싼 확인은 설정과 런타임 두 번이다.

```bash
sudo sshd -t
# 아래 문서용 IP·host를 실제 접속 조건으로 바꾼다.
sudo sshd -T -C user=bml-tunnel,host=lab-pc.example,addr=203.0.113.10,laddr=192.0.2.10,lport=22 | grep '^gatewayports no$'
sudo ss -H -ltnp 'sport = :5003'
```

마지막 출력은 sshd 소유의 `127.0.0.1:5003` **하나**여야 한다. `0.0.0.0`,
`[::]`, 또는 nginx가 안 쓰는 `[::1]`만 성공한 것도 실패다. 외부에서 `nc VPS 5003`은
실패해야 한다.

### 4. 전송은 살고 전달만 풀릴 수 있는가

raw OpenSSH `-R`에는 localhost.run 같은 별도 이름→session lease가 없다. listener는
sshd connection의 forwarding channel이라, 정상 모델에서 “SSH transport는 건강한데
listener만 시간 만료로 사라지는 것”은 흔한 경로가 아니며 재현하지 못했다.
`ExitOnForwardFailure`도 [공식 설명](https://man.openbsd.org/ssh_config#ExitOnForwardFailure)상
**최초 bind**까지만 보며, 이후 local `localhost:5003` 연결 실패나 HTTP 응답은
감시하지 않는다.

랩 PC에서 싼 전체 검사는 지금처럼 공개 HTTPS health다. 층을 가르려면 별도 관리
키로 VPS의 loopback을 찌른다.

```bash
ssh <관리계정>@<VPS> 'curl -fsS --max-time 5 http://127.0.0.1:5003/api/health'
```

로컬 앱은 건강한데 이것이 실패하면 reverse listener/forward 문제다. 이것은 되고
공개 HTTPS만 실패하면 nginx·인증서·DNS·두 방화벽 문제다. 둘 다 200이어도 #8 때문에
**같은 instance nonce**인지 비교해야 한다. `ssh -O check`나 ServerAlive는 SSH
transport만 증명하고 listener는 증명하지 않는다.

### 5. Oracle Cloud 최소 절차

1. public subnet, Internet Gateway route, 공인 IP를 확인한다.
2. 해당 VNIC의 NSG 또는 subnet Security List에 stateful ingress를 두 개만 둔다:
   source `0.0.0.0/0`, TCP, destination 80과 443. AAAA를 둘 때만 `::/0`도 별도로
   연다. SSH 22는 가능하면 랩·관리자 공인 IP 범위로 좁힌다.
3. **5003은 NSG/Security List에 열지 않는다.** GatewayPorts가 잘못돼도 이 층이
   nginx 우회를 막아야 한다.
4. 인스턴스 안에서도 기존 OCI link-local/iSCSI 규칙을 보존하며 terminal reject
   앞에 TCP 80·443 ACCEPT를 넣고 저장한다. Oracle은 Ubuntu 이미지에서 UFW로
   고치지 말라고 한다. [OCI UFW 주의](https://docs.oracle.com/en-us/iaas/Content/Compute/known-issues.htm#ufw)에
   따라 `/etc/iptables/rules.v4`와 `iptables-restore`/`netfilter-persistent`를 쓴다.
   이미지마다 줄 번호가 다르므로 인터넷 예제의 “6번 줄”을 그대로 베끼지 않는다.
5. 외부에서 80·443 성공, 5003 실패를 확인한 뒤 Certbot을 실행한다. 자동 갱신은
   `systemctl list-timers`와 `certbot renew --dry-run`으로 확인한다.

### 6. 처음 질문에 없던 구멍

가장 큰 것은 평범한 관리 SSH 키(#7), root 입력·덮어쓰기(#5·#6), 다른 Workbench의
200을 이번 터널로 믿는 것(#8), 암호 gate 앞의 512 MB request buffering(#9)이다.
랩 PC 쪽에는 cloudflared가 VPS를 가로막는 순서(#13), 로컬 포트 변경이 remote
포트까지 바꾸는 결합(#14), 감독자 파일의 비원자 쓰기(#11)가 있다. 모두 “화면은
한 일을 말하지만 실제로는 다른 곳/옛 파일/아무 곳에도 안 간다”는 같은 부류다.

## 시험이 실제 회귀를 잡는가

VPS 부분은 대부분 구현 문자열을 센다.

- `test_bml_tunnel.sh:734-752`는 `0.0.0.0` 문자열이 없고 `GatewayPorts no`,
  `proxy_buffering off`, `512m`이 한 번 있는지만 본다. 그래서 #1, #3, #4, #9,
  #19를 모두 정답으로 통과시킨다.
- `test_bml_client.sh:1098-1104`는 감독자가 둘이라고 설명하면서도 옛
  `tunnel-keepalive.sh` 패턴 기대값을 1로 둬 #2를 통과시킨다. 실제 stop을 실행하지
  않는다.
- stale 시험은 공개 응답을 yes/no 하나로 줄이고 “공개 실패+로컬 성공이면 close”를
  정답으로 고정해 #12를 잡는 대신 고정한다.
- full `cmd_share`에서 cloudflared 부재, wrong-instance 200, 키 거절, remote bind
  충돌, custom SSH port, local/remote 포트 분리, read-only·symlink 감독자 파일을
  실행하지 않는다.
- `vps-setup.sh`는 시험이 파일 존재와 문자열 세 개를 세는 데서 끝난다. nginx
  config test, sshd effective config, Certbot 순서, idempotence·rollback은 하나도
  실행하지 않는다.

따라서 늘릴 시험의 모양도 구체적이다.

1. 생성 함수를 실행해 exact `-R 127.0.0.1:5003:127.0.0.1:6001`을 검사한다.
2. fake supervisor와 child ssh를 실제로 띄워 stop 뒤 둘 다 사라지는지 본다.
3. 새 ssh는 bind 실패, 옛 endpoint는 200인 경우 nonce 불일치로 실패해야 한다.
4. cloudflared가 전혀 없어도 VPS `cmd_share`를 끝까지 통과시킨다.
5. DNS·TLS·404·429·502를 각각 넣어 어떤 경우에 유지/재시작하는지 화면까지 본다.
6. 일회용 Ubuntu/nginx·OpenSSH 환경에서 HTTP-only→인증서 fixture→최종 config의
   `nginx -t`, `sshd -T`, IPv4 선점 bind를 실행한다. 실제 ACME 전송은 fixture로
   대체해도 순서와 원자성은 잡을 수 있다.

## 확실하지 않은 것과 리뷰가 못 본 곳

- 실제 OCI 인스턴스, nginx, sshd, Certbot, DNS, Let's Encrypt 발급·갱신을 한 번도
  돌리지 못했다. #1·#3·#4·#10·#16은 공식 동작과 재현 절차까지 확인했지만 이
  특정 이미지의 실측은 아니다.
- `Connection "upgrade"`가 현재 FastAPI SSE를 깨뜨리는 반례는 없었다. 제거 권고를
  확정 결함으로 세지 않았다.
- Certbot 패키지가 이 이미지에서 자동 갱신 timer를 만드는지, OCI iptables의 정확한
  reject 줄 번호가 무엇인지는 모른다. 첫 설치 체크리스트에서 실측해야 한다.
- OpenSSH listener가 건강한 SSH transport에서 독립적으로 사라지는 사례와 절전 후
  정확한 회복 시간은 실측하지 못했다. 대신 확정된 orphan·부분 bind·server-side
  keepalive 공백을 보고했다.
- 512 MB 실업로드, SSE fault proxy, 외부 망에서의 TLS/HTTP와 Oracle idle 회수는
  실행하지 못했다.

이 상태에서는 첫 VPS를 만들지 않는 것이 맞다. 최소한 #1–#8과 OCI 80/443 절차를
닫고, 일회용 VPS에서 설치→터널→절전/망 단절→stop→재부팅→갱신 dry-run까지 한 번
통과한 뒤에 실제 워크벤치 주소로 승격해야 한다.