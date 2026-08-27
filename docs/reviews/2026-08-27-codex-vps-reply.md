---
title: 2026-08-27 VPS 리뷰 회답 — 22건 전부
created: 2026-08-27
updated: 2026-08-27
type: guide
tags: [review, response, vps, ssh, nginx]
sources: [docs/reviews/2026-08-27-codex-vps-result.md, docs/adr/0034-our-own-vps-in-front.md]
confidence: high
explored: true
verificationStatus: partial
verifiedAt: 2026-08-27
---

# 2026-08-27 VPS 리뷰 회답 — 22건 전부

- 원문: [2026-08-27-codex-vps-result](2026-08-27-codex-vps-result.md) (승인 보류)
- 범위: `tools/bml` 의 VPS·stale 갈래, `tools/vps-setup.sh`, ADR 0034, 해당 시험
- 결과: **22건 전부 고침.** 되받아친 것 없음. 결론을 바꾼 것도 없음.
- 커밋 셋: `a43acc55`(랩 PC 8건) · `9a09baf6`(VPS 13건) · `b8322940`(#8)

> **"고쳤다" 의 경계를 먼저 밝힌다.** 이 컨테이너에는 nginx·sshd·certbot·OCI 가
> 없다. 그래서 `tools/vps-setup.sh` 는 **한 줄도 돌려 보지 못했다.** 랩 PC 쪽
> (`tools/bml`) 은 함수를 실제로 실행해서 확인했고, 저쪽 설치본은 소스와 공식
> 문서 대조까지다 — Codex 도 같은 조건이었고 스스로 그렇게 밝혔다.
> **그 경계가 지워지면 이 표가 실측처럼 읽힌다.** 실검사는 일회용 VPS 에서
> 열 단계(ADR 0034 '올리기 전에')이고, 그 전에는 실제 이름으로 안 올린다.

## 표

| # | 심각도 | 상태 | 커밋 | 어떻게 확인했나 |
|---:|:---:|:---:|---|---|
| 1 | 높음 | 닫음 | `9a09baf6` | 문자열 — `listen 443` 0건, `listen 80` 2건, snippet 3곳 |
| 2 | 높음 | 닫음 | `a43acc55` | **실행** — 진짜 감독자+자식 ssh 를 띄우고 `close_tunnel` 뒤 `process_alive` 로 둘 다 확인 |
| 3 | 높음 | 닫음 | `a43acc55` | **생성** — 감독자 파일을 만들어 `-R` 줄을 직접 읽는다 |
| 4 | 높음 | 닫음 | `9a09baf6` | 문자열 — drop-in 1건, `sshd -T -C` 2건, `sed -i …sshd_config` 0건 |
| 5 | 높음 | 닫음 | `9a09baf6` | 문자열 — `valid_domain` 2건, `realpath -m` 2건 |
| 6 | 높음 | 닫음 | `9a09baf6` | 문자열 — `BML_REPLACE` 2건, `rm -f …sites-enabled/default` 0건 |
| 7 | 높음 | 닫음 | `9a09baf6` | 문자열 — `useradd …nologin` 1건, `PermitListen 127.0.0.1` 1건, `permitlisten` 1건 |
| 8 | 높음 | 닫음 | `b8322940` | **실행** — 진짜 HTTP 서버 넷(우리·같은·다른·옛). 고치기 전 코드에서 17건 실패 |
| 9 | 중간 | 닫음 | `9a09baf6` | 문자열 — `proxy_request_buffering off` 1건 |
| 10 | 중간 | 닫음 | `9a09baf6` | 문자열 — `ClientAliveInterval` 1건 |
| 11 | 중간 | 닫음 | `a43acc55` | **실행** — 링크 자리에 `write_vps_keepalive` → 거절 |
| 12 | 중간 | 닫음 | `a43acc55` | **실행** — 502/503/504 만 닫고 DNS·TLS·404·429 는 안 건드림 |
| 13 | 중간 | 닫음 | `a43acc55` | 갈래 안으로 옮김 (`ensure_cloudflared_or_warn`) |
| 14 | 중간 | 닫음 | `a43acc55` | **생성** — `WORKBENCH_PORT=6001` 에서 `-R 127.0.0.1:5003:127.0.0.1:6001` |
| 15 | 중간 | 닫음 | `a43acc55` | **생성** — 감독자 파일에 `BatchMode=yes` 1건 |
| 16 | 중간 | 닫음 | `9a09baf6` | `--check` 모드 + OCI 두 층 안내 2건 |
| 17 | 중간 | 닫음 | `9a09baf6` | 문자열 — `proxy_read_timeout 75s` 1건, `3600s` 0건 |
| 18 | 낮음 | 닫음 | `9a09baf6` | ADR 0034 문구 — "평생인 것은 요금이지 이 인스턴스가 아니다" |
| 19 | 낮음 | 닫음 | `9a09baf6` | 문자열 — `client_max_body_size 520m` 1건 |
| 20 | 낮음 | 닫음 | `a43acc55` | **실행** — `u@h:` · `u@h:abc` · `u@@h` 등 8가지가 저장 전에 거절 |
| 21 | 낮음 | 닫음 | `9a09baf6` | 문자열 — `enable … || true` 0건, `is-active` 1건 |
| 22 | 낮음 | 닫음 | `9a09baf6` | 문자열 — `return 444` 1건 (default 는 안 지움) |

**"문자열" 과 "실행"·"생성" 을 표에서 갈라 적는다.** Codex 의 지적 중 가장
아픈 것이 "VPS 부분은 대부분 구현 문자열을 센다" 였다. 랩 PC 쪽은 그 지적대로
돌리는 시험으로 바꿨고 (그 시험이 곧바로 좀비 한 건을 더 잡았다), 저쪽 설치본은
**아직 문자열이다.** 그것을 표에서 숨기지 않는다.

## 결함으로 세지 않은 셋 — 우리가 한 것

Codex 가 확정 22건에 넣지 않고 따로 적어 둔 것들이다.

- **`Connection "upgrade"`** (물음 B). "지금 WebSocket 이 없으므로 두 Upgrade
  header 를 지우는 것이 가장 작다" 는 권고를 그대로 따랐다 — 새 설치본에
  `Upgrade` 는 한 줄도 없다. 나중에 필요하면 공식 `map $http_upgrade` 를 쓴다.
- **PID 재사용 TERM** (물음 1). 재현은 못 했다고 했지만 최소 수정이 한 줄이라
  넣었다: `wait "$child"` 다음에 `child=""`. 끝난 PID 를 손에 들고 있지 않으면
  그 번호가 재사용돼도 trap 이 남의 프로세스를 못 죽인다.
- **좀비** (물음 1). "zombie 는 fd 가 닫혀 VPS 포트를 잡지 못한다" 가 맞다.
  그래서 좀비는 위험이 아니었지만 **시험이 좀비에게 속았다** — `kill -0` 이
  좀비에게도 성공해서, 우리 시험이 죽은 자식을 "살아 있다" 로 셌다. 시험을
  `process_alive` 로 바꾸고, 그러다 trap 이 자식을 **거두지 않는** 것을 찾아
  `wait` 를 붙였다. 지적이 아닌 데서 한 건이 나왔다.

## 늘린 시험 여섯 중 우리가 한 것

Codex 가 "늘릴 시험의 모양" 으로 여섯을 적었다. 다섯을 넣었고, 하나는 못 넣는다.

1. **`-R 127.0.0.1:5003:127.0.0.1:6001` 을 생성해서 검사** — 넣음.
2. **가짜 감독자와 자식 ssh 를 실제로 띄워 stop 뒤 둘 다 사라지는지** — 넣음.
3. **새 ssh 는 bind 실패, 옛 endpoint 는 200 → nonce 불일치로 실패** — 넣음
   (`confirm_tunnel` 이 4 를 내고 닫는지까지).
4. **cloudflared 가 전혀 없어도 VPS `cmd_share` 가 끝까지** — 갈래 안으로 옮겨
   구조적으로 못 막게 했다. 전체 `cmd_share` 실행 시험은 아직 없다.
5. **DNS·TLS·404·429·502 를 각각 넣어 유지/재시작을 가른다** — 넣음.
6. **일회용 Ubuntu 에서 `nginx -t` · `sshd -T` · IPv4 선점 bind** — **못 넣는다.**
   이 컨테이너에도 CI 에도 그 셋이 없다. ADR 0034 의 열 단계가 이것을 사람이
   한 번 하는 절차로 대신한다.

## 승인 보류에 대한 우리 답

**보류가 맞다.** 22건을 다 고쳤어도 "VPS 를 세워도 된다" 가 되지는 않는다 —
고친 것의 절반을 우리가 못 돌려 봤기 때문이다. ADR 0034 의 상태를
`채택 — 다만 아직 세우지 않았다` 로 바꾸고, 승격 조건 열 단계를 거기 적었다.
일회용 VPS 에서 그 열 단계를 통과하기 전에는 실제 이름을 걸지 않는다.
