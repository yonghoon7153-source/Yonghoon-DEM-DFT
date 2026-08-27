# Codex 리뷰 과제 — 우리 VPS 한 대를 워크벤치의 대문으로

[codex-session-bootstrap.md](codex-session-bootstrap.md) 로 세션을 연 뒤 아래
"붙여넣는 프롬프트" 를 그대로 붙여넣는다.

이 리뷰는 **주제 하나**다: 랩 PC → 우리 VPS 로 `ssh -R` 을 걸고, 그 앞에 nginx
+ Let's Encrypt 를 세워 **주소가 안 바뀌게** 하는 길 (ADR 0034). 도메인 수치
(mAh/g, knee, dQ/dV, EIS 피팅)는 이 변경이 안 건드리므로 범위 밖이다.

## 왜 이 리뷰가 필요한가

1. **아직 한 번도 안 돌려 봤다.** VPS 를 아직 안 만들었다. `tools/vps-setup.sh`
   는 **실행된 적이 없는 107줄**이고, 이 저장소에서 유일하게 시험이 못 닿는
   코드다 (남의 기계에서 root 로 도는 셸).
2. **바깥에 여는 길이다.** 이 앞에 있는 것은 공유 암호 하나뿐이고 (ADR 0014),
   그마저 뚫리면 주소를 아는 사람이 전부 읽고 전부 지운다. 잘못 열면 조용히
   열린다 — 화면에는 아무 표시도 안 난다.
3. **셸이다.** 이 저장소에서 시험이 가장 얇은 층이고, 실패가 사용자 화면에
   "안 됩니다" 한 줄로만 나타난다.

## 범위

```bash
git log --oneline ce8adc94~1..HEAD -- tools/ docs/adr/0034-our-own-vps-in-front.md
git diff ce8adc94~1..HEAD -- tools/vps-setup.sh tools/bml
```

| 파일 | 무엇 |
|---|---|
| `tools/vps-setup.sh` (신규, 107줄) | VPS 에서 한 번 도는 설치 — nginx · certbot · sshd |
| `tools/bml` `tunnel_vps` · `write_vps_keepalive` · `tunnel_via_vps` · `cmd_share_vps` | 랩 PC 쪽. keepalive 스크립트를 만들어 띄운다 |
| `tools/bml` `share_stale` · `cmd_share` 의 "이미 열려 있습니다" 갈래 | 죽은 터널 판정 (2026-08-27 추가) |
| `docs/adr/0034-our-own-vps-in-front.md` | 왜 Cloudflare 가 아니라 우리 기계인가 |
| 시험 | `tools/tests/test_bml_tunnel.sh` (233건 — `cmd_share` 를 실제로 돌린다) |

## 실측 — 리뷰어가 알아야 할 것

이 랩 망에서 **7844 이 TCP·UDP 둘 다 막혀** Cloudflare 터널이 안 된다 (엣지
IPv4 `198.41.192.27` · `198.41.192.7` 에 직접 붙어 확인, ADR 0031). 그런데
SSH 는 나간다:

```
/dev/tcp/github.com/22       → OK
/dev/tcp/ssh.github.com/443  → OK
```

그래서 "남의 터널 서비스" 대신 우리 기계다. 지금 쓰는 localhost.run 은
**세션이 조용히 풀린다** (2026-08-27: ssh 는 살아 있는데 엣지가 503 —
`ServerAliveInterval=30` 이 걸려 있어도 전송은 멀쩡했으므로 ssh 가 못 잡는다).
그 경험이 `share_stale` 을 낳았고, 같은 일이 VPS 에서도 날 수 있는지가
아래 질문 4번이다.

## 우리가 이미 의심하는 것 (확인 부탁)

**A. `certbot` 이 돌기 전에 nginx 설정이 깨져 있다 — 거의 확실.**
`vps-setup.sh` 는 `listen 443 ssl;` 을 쓴 server 블록을 먼저 쓰고 심볼릭 링크를
걸어 둔 뒤에 `certbot --nginx` 를 부른다. 그런데 그 블록에는 `ssl_certificate`
가 없다 (아직 발급 전이라 없는 게 맞다). nginx 는 그 조합을 거절하므로
(`no "ssl_certificate" is defined for the "listen ... ssl" directive`) certbot 이
안에서 `nginx -t` 를 할 때 실패할 것으로 본다. 흔한 처방은 **:80 블록만 써 두고
443 은 certbot 이 붙이게 두는 것**인데, 그러면 우리가 적어 둔
`client_max_body_size 512m` · `proxy_buffering off` · `proxy_read_timeout 3600s`
가 어디로 가야 하는지가 문제다 (셋 다 없으면 안 된다 — 아래 질문 2번).
→ **맞는지, 그리고 셋을 잃지 않는 최소 수정이 무엇인지.**

**B. `Connection "upgrade"` 를 무조건 보낸다.** `map $http_upgrade
$connection_upgrade` 없이 `proxy_set_header Connection "upgrade";` 만 있다.
지금은 WebSocket 을 안 쓰고 SSE 만 쓰는데, 이 헤더가 SSE·평범한 요청에
해가 되는지.

**C. `rm -f /etc/nginx/sites-enabled/default`.** 전용 기계를 전제한 줄인데
스크립트 어디에도 그렇게 안 적혀 있다.

## 물어보고 싶은 것

1. **랩 PC 쪽 keepalive** (`write_vps_keepalive`). `ssh -N -R` 을 `while :` 로
   감싸고, 5초 안에 죽는 것이 20번 이어지면 멈춘다. `close_tunnel` 은
   `kill $pid` 뒤 `kill -- -$pid` 를 하는데, 스크립트에서 띄운 백그라운드
   프로세스는 제 프로세스 그룹의 리더가 아니므로 뒤엣것은 대개 실패하고
   `trap ... TERM INT` 에 기댄다. **랩 PC 를 재우거나 랜을 뽑았다 꽂았을 때,
   또는 `bml stop` 을 했을 때 ssh 가 확실히 죽는가?** 좀비 ssh 가 남아 저쪽
   5003 을 잡고 있으면 다음 연결이 `ExitOnForwardFailure=yes` 로 곧바로
   죽는다 — 그리고 그 모양은 "키가 안 올라갔다" 와 화면에서 구분되지 않는다.

2. **SSE 와 업로드.** 이 앱은 `/api/events` 로 SSE 를 20초 하트비트로 흘리고
   (`apps/api/app/routers/live.py`), 업로드 상한이 512 MB 다. nginx 쪽
   `proxy_buffering off` · `proxy_read_timeout 3600s` · `client_max_body_size
   512m` 로 충분한가? **`ssh -R` 한 단이 더 있다는 것**이 여기서 차이를
   만드는지 (버퍼·창 크기·긴 업로드 중 keepalive).

3. **`GatewayPorts`.** `^\s*GatewayPorts\s+yes` 만 `no` 로 바꾼다.
   `clientspecified` 이거나 줄이 아예 없을 때도 안전한가? 우리가 바라는 것은
   "전달된 5003 이 127.0.0.1 에만 붙는다" 하나다. 확인하는 값싼 방법도.

4. **끊김 판정.** localhost.run 에서 **전송은 살아 있는데 전달만 풀리는** 일이
   있었다. 우리 VPS + `ssh -R` 에서도 같은 일이 가능한가 (sshd 가 리스너를
   놓았는데 세션은 유지)? 가능하다면 랩 PC 가 그것을 **자기 쪽에서** 알 수 있는
   길이 있는지 — 지금은 `share_stale` 이 공개 주소를 HTTP 로 찔러서만 안다.

5. **Oracle Cloud 특유의 함정.** 이 기계는 Oracle Cloud Always Free (Tokyo)
   가 될 예정이다. Ubuntu 이미지가 기본 iptables 로 80/443 을 막아 두는 것으로
   아는데, `vps-setup.sh` 에 그 얘기가 없다. 보안 목록(security list)과 인스턴스
   방화벽 **둘 다** 여는 최소 절차를 적어 주면 좋겠다.

6. **우리가 안 본 구멍.** 위 다섯 개 말고, 이 설정으로 바깥에 열었을 때
   **조용히** 잘못될 수 있는 것.

## 범위 밖

- 공유 암호 게이트 자체 (ADR 0014) — 이미 리뷰받았다
  (`codex-review-remote-access.md`).
- 프런트엔드, 도메인 수치, EIS 피팅.
- "VPS 말고 다른 서비스를 쓰자" — ADR 0031·0034 에서 이미 재어 본 것이라,
  **그 재기가 틀렸다는 근거가 있을 때만** 다시 연다.

## 붙여넣는 프롬프트

```
이 저장소의 `tools/vps-setup.sh` 와 `tools/bml` 의 VPS 터널 갈래를 리뷰해 줘.
범위와 배경은 docs/reviews/codex-review-vps.md 에 있다. 그 파일의 "우리가 이미
의심하는 것" 세 개를 먼저 확인하고, "물어보고 싶은 것" 여섯 개에 답해 줘.

지켜야 하는 것:
- 이 스크립트는 **아직 한 번도 안 돌았다.** 처음 돌리는 사람이 root 로 남의
  기계에서 돌린다 — 되돌릴 수 없는 줄(`rm`, `sed -i`, certbot)을 특히 봐 줘.
- 바깥에 여는 길이다. 잘못 열리면 **조용히** 열린다.
- 랩 PC 쪽은 CLAUDE.md §0.8 을 지켜야 한다: 우리 것임을 증명한 뒤에만 죽인다.

낼 것: 심각도(높음/중간/낮음) · 파일:줄 · **재현 절차** · 최소 수정.
확실하지 않은 것은 "확실하지 않음" 이라고 적어 줘 — 추측을 실측처럼 쓰면
우리가 그것을 근거로 기계를 만든다.
```
