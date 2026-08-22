---
title: Codex 원격 접근 독립 리뷰
created: 2026-08-21
updated: 2026-08-22
type: review
tags: [review, audit, crosscheck, remote-access, security]
sources:
  - docs/adr/0011-central-instance-for-data.md
  - docs/adr/0012-attribution-not-authentication.md
  - docs/adr/0014-share-with-a-tunnel-and-one-password.md
confidence: high
explored: true
verificationStatus: verified
---

# Codex 원격 접근 독립 리뷰

검토 범위: `d41aec3e^..14dff93c` (`bml use`, `bml share`, 공유 암호 게이트)

> **이 문서는 받은 리뷰 원문이다.** 대응 상태는 아래 "대응 현황" 표에서만
> 갱신한다. 원문 표는 고치지 않는다 — 무엇을 지적받았는지가 남아야 한다.

## 요약

공유 암호의 기본 게이트 자체는 바깥 미들웨어로 배치되어 있지만, 터널 수명과
게이트 수명이 결합되지 않아 이미 열린 터널이 나중에 무암호 서버를 공개할 수
있다. 프로세스 소유 판정과 종료 확인도 CLAUDE.md §0.8 수준에 못 미쳐, 남의
프로세스를 죽이거나 살아 있는 공개 터널을 "닫힘"으로 보고하는 경로가
재현됐다. Cloudflare Quick Tunnel은 공식적으로 SSE를 지원하지 않고
localhost.run 경로도 HTTP 노출·provider 선택·수명 검증에 문제가 있어, 현재
상태를 중앙 워크벤치의 안전한 공유 경로로 승인하기 어렵다. 확정 발견은
**높음 8건, 중간 13건**이다.

## 대응 현황

이 표만 갱신한다. `열림` 은 아직 아무도 손대지 않은 것이다.

| # | 심각도 | 상태 | 어디서 | 비고 |
|---|---|---|---|---|
| 1 | 높음 | 열림 | `tools/bml` | 터널 수명과 게이트 수명이 안 묶인다 |
| 2 | 높음 | 열림 | `tools/bml` | 부분 문자열 소유 판정 — starttime·argv 토큰 필요 |
| 3 | 높음 | 열림 | `tools/bml` | `close_tunnel` 이 사망 확인 없이 성공 보고 |
| 4 | 높음 | 열림 | `tools/bml` | provider 전환이 PID·URL 을 섞는다 |
| 5 | 높음 | 열림 | `tools/bml`, `apps/api` | localhost.run 평문 HTTP 로그인 |
| 6 | 높음 | 열림 | `apps/api`, `tools/bml` | 1자 암호 허용 + 로그인 rate limit 없음 |
| 7 | 높음 | 열림 | `apps/web`, `tools/bml` | Quick Tunnel 에서 SSE 안 됨 → polling 전환 필요 |
| 8 | 높음 | 열림 | `tools/bml:1270` | `.localhost.run` 형식을 정상 주소로 안 본다 |
| 9 | 중간 | 열림 | `apps/api`, `tools/bml` | `share stop` 후에도 랩 안 문이 남는다 |
| 10 | 중간 | 열림 | `tools/bml` | 명시적 SSH 도 cloudflared 설치에 종속 |
| 11 | 중간 | 열림 | `tools/bml` | TCP 만 찔러 QUIC 경로를 버린다 |
| 12 | 중간 | 열림 | `tools/bml` | SSH 가 비대화식·IPv4 로 고정되지 않았다 |
| 13 | 중간 | 열림 | `tools/bml`, `apps/api` | health 가 내부 경로를 인증 없이 노출 |
| 14 | 중간 | 열림 | `tools/bml` | 떠 있는 서버가 현재 암호를 쓰는지 확인 안 함 |
| 15 | 중간 | 열림 | `apps/web` | 401 → 무한 reload, 편집값 소실 |
| 16 | 중간 | 열림 | `apps/web` | 내보내기 링크가 401 처리를 우회 |
| 17 | 중간 | 열림 | `tools/bml` | status 의 LAN 주소 판정이 틀린다 |
| 18 | 중간 | 열림 | `tools/bml` | 주소 입력 정규화 (IPv6·대소문자·공백) |
| 19 | 중간 | 열림 | `tools/bml` | 저장한 암호를 재시작하면 다르게 읽는다 |
| 20 | 중간 | 열림 | `tools/bml` | `WORKBENCH_WAIT` 검증 없음 → 무한 루프 |
| 21 | 중간 | **닫음** | `bml check`, CI | 2026-08-22. client·shutdown·tunnel·worklog 를 `bml check` 와 CI tools job 이 함께 돌린다. 표 아래 "남은 절반" 참고 |

**#21 의 남은 절반은 아직 열려 있다.** 실행 등록만 고쳤고, "fallback 테스트가
`cmd_share` 본문의 문자열 개수만 센다" 는 지적은 그대로다. fake ssh/cloudflared
로 provider 강제·child 사망·TERM 무시·fallback·URL 파싱을 end-to-end 로
검사해야 닫힌다.

## 발견

| # | 심각도 | 파일:줄 | 제목 | 실패 시나리오 | 제안 수정 |
|---|---|---|---|---|---|
| 1 | 높음 | `tools/bml:1423-1426, 1490-1500` | 살아남은 터널이 무암호 재기동 서버를 공개한다 | 암호가 걸린 서버에서 `bml share` → uvicorn만 비정상 종료 → 암호를 끄거나 빈 값으로 서버 재기동 → 분리 실행 중인 기존 터널이 새 무암호 서버에 즉시 연결된다. 이후 `bml share`도 기존 터널 분기에서 게이트를 재검사하지 않고 "이미 열려 있습니다"로 끝난다. | 서버 시작·재시작 때 살아 있는 터널과 게이트 상태를 함께 검증하고, 무암호 서버를 띄우기 전 터널 종료를 확인한다. 기존 터널 조기 반환 전에도 보호 API의 401을 다시 확인한다. 장기적으로는 LAN 서버가 아니라 터널 전용 로컬 게이트 프록시를 공개한다. |
| 2 | 높음 | `tools/bml:1366-1382, 1395-1401` | 명령줄 부분 문자열이 남의 프로세스를 우리 터널로 만든다 | 낡은 PID가 `python worker.py --note ssh -R 80:localhost:5003 nokey@localhost.run` 또는 `notssh-helper -Rgarbage80:localhost:5003 suffix-localhost.run` 같은 프로세스에 재사용됨 → `looks_like_our_tunnel`이 참 → `close_tunnel`이 그 프로세스 그룹을 종료한다. 다른 worktree나 수동 터널이 같은 기본 URL을 쓰는 경우도 구별하지 못한다. | PID와 `/proc/$pid/stat` starttime, 실제 executable, NUL 구분 argv의 정확 토큰, repo별 launch nonce/provider를 함께 저장·검증한다. 어느 하나라도 설명하지 못하면 죽이지 않는다. |
| 3 | 높음 | `tools/bml:1395-1407` | 종료하지 못한 터널도 닫았다고 보고하고 소유 증거를 지운다 | 정확한 cloudflared argv를 가진 프로세스가 TERM을 무시함 → `close_tunnel`은 두 번 `kill`한 뒤 생존 확인 없이 PID/URL 파일을 삭제하고 성공 반환 → 사용자는 공개 URL이 닫힌 줄 알지만 터널은 살아 있고, 다음 명령은 더 이상 그 PID를 관리하지 못한다. | TERM 뒤 동일 PID/starttime의 종료를 제한 시간 동안 확인한다. 확인된 우리 프로세스에만 최종 KILL을 허용하고, 사망 확인 전에는 상태 파일을 보존하며 실패를 사용자에게 알린다. |
| 4 | 높음 | `tools/bml:1415-1445, 1538-1545` | provider 전환이 서로 다른 PID와 URL을 한 상태로 섞는다 | 첫 Cloudflare 프로세스가 URL을 쓴 뒤 TERM을 무시하고 health 실패 → 같은 `tunnel.log`를 비운 뒤 SSH fallback 시작 → 고아 Cloudflare가 다시 쓴 URL을 SSH URL로 읽어 SSH PID와 저장 → `share stop`은 SSH만 죽이고 Cloudflare 공개 URL은 관리 불능으로 남는다. URL 출력 직후 죽은 child도 health가 우연히 200이면 성공 상태로 남는다. | provider별 임시 로그·상태를 사용하고 이전 provider 종료를 확인한 뒤에만 fallback한다. PID, starttime, provider, URL을 하나의 원자 상태로 커밋하고 URL 획득 직후와 health 성공 직후 child 생존을 재검사한다. |
| 5 | 높음 | `tools/bml:1468-1473`; `apps/api/app/main.py:145-156` | localhost.run이 평문 HTTP 로그인도 함께 연다 | `ssh -R 80:...`로 free HTTP tunnel을 열면 HTTPS와 함께 HTTP endpoint도 생긴다. 사용자가 `http://같은-host`로 접속 → 공유 암호 POST와 `Secure` 없는 gate cookie가 방문자와 localhost.run edge 사이에서 평문으로 흐른다. localhost.run도 HTTP 앱은 HTTPS를 강제하라고 명시한다. | HTTP를 HTTPS로 강제할 수 있는 provider/edge 옵션을 사용하고, 신뢰한 forwarded scheme에서 tunnel 응답 cookie에 `Secure`를 건다. LAN HTTP와 터널 HTTPS를 같은 listener가 구분하지 못하는 현 구조는 터널 전용 프록시로 분리한다. 근거: [localhost.run Security](https://localhost.run/docs/security/). |
| 6 | 높음 | `apps/api/app/settings.py:37`; `apps/api/app/main.py:145-156`; `tools/bml:64-65, 1500-1525` | 공식 환경변수 경로는 1자 암호와 무제한 대입을 허용한다 | `WORKBENCH_PASSWORD=x bml` 후 같은 환경에서 `bml share` → 서버는 1자를 정상 secret으로 쓰고 share는 nonempty와 "API가 401인가"만 확인해 공개 터널을 연다. 인터넷의 `/__login`에는 시도 제한이 없어 `x`를 즉시 대입할 수 있다. 6자 검사는 `bml password`에만 있다. | 서버 시작과 `share`가 같은 trim·길이·허용문자·강도 검증을 사용하게 한다. 암호 입력은 argv 대신 hidden prompt/stdin을 기본으로 하고, 로그인에는 IP/세션별 rate limit, 지연, 429와 감사 로그를 둔다. |
| 7 | 높음 | `apps/web/src/lib/live.ts:78-99`; `tools/bml:1535-1544` | 기본 Cloudflare 공유에서는 실시간 갱신이 동작하지 않는다 | `auto`가 Cloudflare Quick Tunnel을 선택 → 다른 사용자가 질량·그룹을 수정 → Quick Tunnel은 공식적으로 SSE를 지원하지 않지만 브라우저는 EventSource가 있다는 이유로 SSE만 재접속하고 polling으로 전환하지 않는다 → 공유 화면이 오래된 값을 계속 표시한다. | SSE 오류/무이벤트 watchdog 뒤 revision polling으로 전환하거나 SSE를 지원하는 provider를 선택한다. 중앙 서버의 "모든 화면이 따라온다" 계약을 provider acceptance test로 고정한다. 근거: [Cloudflare Quick Tunnel 제한](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/). |
| 8 | 높음 | `tools/bml:1270-1275` | 공식 localhost.run 주소 형식을 정상 터널로 인정하지 않는다 | SSH가 `tunneled with tls termination, https://yourapp.localhost.run`을 출력 → 정규식은 `*.lhr.life`만 허용 → 30초 뒤 URL 없음으로 정상 SSH를 종료한다. | 관리 페이지 `admin.localhost.run`은 계속 배제하되, provider의 구조화 출력 문맥에서 단일 서브도메인 `.localhost.run`과 `.lhr.life`를 모두 파싱한다. 실제 fake-ssh 출력으로 회귀 테스트한다. 근거: [localhost.run 공식 문서](https://localhost.run/). |
| 9 | 중간 | `apps/api/app/gate.py:1-5`; `tools/bml:1319-1356, 1395-1407`; `docs/adr/0014-share-with-a-tunnel-and-one-password.md:62-79` | `share stop` 후에도 랩 안 서버의 문이 계속 남는다 | 암호 설정·restart·share 후 `bml share stop` → 터널만 종료되고 서버와 `.bml/env`의 암호는 유지 → localhost와 LAN 사용자도 계속 로그인해야 한다. LAN 주소는 HTTP인데 같은 공유 암호 cookie는 `Secure`가 없다. 이는 "주소가 인터넷에 있는 동안에만 문이 선다"는 코드 주석과 ADR의 "랩 안 아무 변화 없음"과 다르다. | 터널 전용 gate listener/proxy로 수명을 결합하거나, 정책을 "암호 설정 시 LAN도 잠김"으로 명시 변경하고 LAN HTTPS를 제공한다. `share stop` 후 LAN 동작을 테스트한다. |
| 10 | 중간 | `tools/bml:1527-1533` | 명시적 SSH fallback도 cloudflared 설치에 종속된다 | `WORKBENCH_TUNNEL=ssh bml share`, ssh는 정상이고 cloudflared 다운로드는 차단됨 → provider 분기 전에 `ensure_cloudflared`가 종료 → SSH를 한 번도 실행하지 않는다. | 선행 `ensure_cloudflared`를 제거하고 Cloudflare 분기 안에서만 준비한다. auto에서는 설치 실패를 fatal exit가 아니라 SSH fallback 사유로 전달한다. |
| 11 | 중간 | `tools/bml:1180-1187, 1535-1544`; `docs/adr/0014-share-with-a-tunnel-and-one-password.md:39-58` | TCP 하나만 찌르면 가능한 QUIC 경로를 버린다 | UDP 7844는 열리고 TCP 7844와 SSH 22는 닫힌 망 → cloudflared 기본 QUIC은 가능하지만 TCP preflight가 실패해 localhost.run을 선택 → 공유 실패. 문서의 "QUIC도 7844/TCP"도 사실과 다르다. | UDP/TCP를 따로 진단하거나 Cloudflare의 실제 QUIC→HTTP/2 시도를 수행한 뒤 SSH로 넘어간다. 근거: [Cloudflare 방화벽 사양](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/configure-tunnels/tunnel-with-firewall/). |
| 12 | 중간 | `tools/bml:1463-1473` | SSH 실행이 비대화식·로컬 주소에 대해 결정적이지 않다 | 사용자 ssh 설정에 password/kbd-interactive 또는 ControlMaster가 있음 → nohup child가 `/dev/tty`/askpass를 기다리거나 저장한 PID와 실제 연결 소유가 달라진다. 또 `localhost`가 `::1` 우선이고 서버는 `127.0.0.1`만 listen → 공개 URL은 생겨도 origin 연결이 실패한다. | `BatchMode=yes`, password/kbd-interactive off, `ControlMaster=no`, 유한 `ConnectTimeout`을 명시하고 local target은 `127.0.0.1:$PORT`로 고정한다. 공식 문서도 IPv4-only 앱에는 `127.0.0.1`을 권한다. |
| 13 | 중간 | `tools/bml:1155-1163`; `apps/api/app/main.py:169-176` | 임의의 health 200을 워크벤치로 저장하며 내부 경로도 공개한다 | 사용자가 `bml use`에 `/api/health`가 단순 200인 다른 서버를 입력 → 주소가 Workbench로 저장된다. 실제 Workbench health는 인증 없이 절대 `data_dir`, wrdkit 판, 업로드 한도를 인터넷에 노출한다. | 공개 readiness body를 안정된 service marker와 status만으로 축소하고 `bml use`는 JSON content-type, marker, schema를 검증한다. 상세 진단은 gate 안 별도 endpoint로 옮긴다. |
| 14 | 중간 | `tools/bml:1513-1525` | 떠 있는 서버가 현재 공유 암호를 쓰는지 확인하지 않는다 | 서버는 옛 암호 A로 실행 중인데 환경/.bml은 새 암호 B → `/api/samples`는 어쨌든 401이라 share가 성공 → 운영자는 B를 알려 주지만 로그인되지 않고, A를 아는 사람은 계속 접속한다. | 별도 cookie jar로 현재 암호 B의 `/__login` 성공과 보호 API 접근을 검증하고 임시 cookie를 폐기한다. 또는 암호 설정 변경을 서버 restart/health fingerprint와 원자적으로 결합한다. |
| 15 | 중간 | `apps/web/src/lib/api.ts:45-72`; `apps/web/vite.config.ts:12-27` | 401 처리로 개발 화면은 무한 reload되고 편집값은 사라진다 | 암호가 남은 `bml dev`에서 `/api`가 401 → Vite SPA reload → `/__login`은 proxy되지 않아 다시 SPA → 같은 fetch 401을 반복한다. 일반 화면에서도 cookie가 만료된 채 질량/조성을 입력 중 저장 → 즉시 reload되어 draft와 deep link가 사라지고 로그인 성공 후 항상 `/`로 간다. | 401 시 backend 로그인 URL로 return path와 함께 명시 이동하거나 modal을 연다. draft를 보존하고 로그인 뒤 원래 route로 복귀한다. Vite는 `/__login`도 proxy하고 통합 테스트로 reload loop를 막는다. |
| 16 | 중간 | `apps/web/src/lib/api.ts:176-189`; `apps/web/src/pages/SampleDetail.tsx:391-417, 857-862` | 내보내기는 공통 401 처리를 우회한다 | cookie 만료 후 원본/CSV/XLSX 링크 클릭 → raw `<a href>`가 JSON 401을 새 페이지에 표시하거나 그 내용을 파일처럼 받음 → 암호 화면으로 가지 않는다. | 인증된 `fetch` 후 blob 다운로드를 사용하거나 navigation 요청의 401은 return URL을 가진 로그인 HTML redirect로 처리한다. |
| 17 | 중간 | `tools/bml:1108-1145, 1698-1723` | status가 실제로 닿는 LAN 주소를 숨기거나 잘못 공개라고 말한다 | `ss`에 `192.168.1.40:5003`처럼 특정 LAN NIC만 listen → `local`로 판정해 접속 주소를 숨긴다. `0.0.0.0:50030` 같은 텍스트도 포트 경계 없이 5003으로 오인할 수 있다. 172.16/12는 모두 WSL/도커라 가정해 실제 LAN도 버리고, 임의 100.64/10을 모두 "VPN — 다른 공유기에서도"라고 표시하며 IPv6는 전부 버린다. | `ss`를 열 단위로 파싱해 exact local port와 bind address를 판정한다. 실제 interface/route 정보를 이용해 loopback, LAN, WSL NAT, VPN을 구분하고 CGNAT은 VPN이라고 단정하지 않는다. IPv6 URL도 지원한다. |
| 18 | 중간 | `tools/bml:99-113` | 흔한 서버 주소 입력이 조용히 잘못된 URL이 된다 | `2001:db8::1` → 대괄호 없는 `http://2001:db8::1`, `[fd12::7]` → 기본 port 누락, `HTTP://lab.example` → `http://HTTP://lab.example`, 양끝 공백과 여러 trailing slash도 남음 → `bml use`가 엉뚱한 주소를 검사하거나 저장한다. | 입력을 trim하고 URL parser로 scheme/host/port를 검증·정규화한다. IPv6 literal은 bracket과 기본 port를 명시하고 scheme은 대소문자 무관 처리한다. |
| 19 | 중간 | `tools/bml:66-83, 1202-1214, 1319-1354` | 저장한 암호를 재시작하면 다른 암호로 읽는다 | `bml password ' abcdef '` 또는 `~/abcde`, 감싼 따옴표를 포함한 값 → 파일에는 입력값을 저장하지만 다음 실행의 공통 env loader가 trim, quote 제거, `~` 확장 → 사용자가 알려 준 암호로 로그인할 수 없다. 여섯 공백도 길이 검사를 통과한 뒤 빈 secret이 된다. | secret은 경로 설정과 다른 lossless 직렬화/loader를 사용한다. 허용 가능한 모든 암호에 대해 write→load 동일성 테스트를 추가한다. |
| 20 | 중간 | `tools/bml:1171-1177, 1593-1621` | 잘못된 대기 설정이 무한 루프거나 예산보다 오래 기다린다 | `WORKBENCH_WAIT=abc`이고 서버가 안 닿음 → 산술 비교가 매번 오류가 되어 종료 조건이 영원히 참이 되지 않는다. `WORKBENCH_WAIT=0`도 먼저 최대 8초 curl을 실행해 표시한 전체 예산을 넘긴다. | 시작 전에 nonnegative integer 범위를 검증하고, 매 반복에서 남은 시간으로 curl timeout을 제한하며 호출 전에 예산 소진을 확인한다. |
| 21 | 중간 | `tools/tests/test_bml_client.sh:231-279`; `tools/bml:1734-1744`; `.github/workflows/ci.yml:87-95` | 가장 위험한 터널 회귀 테스트가 실행도, 동작 검증도 되지 않는다 | fallback 테스트는 `cmd_share` 본문에 `tunnel_via_ssh` 문자열이 두 번 있는지만 세어 provider 실행·실패를 전혀 검증하지 않는다. 더구나 `test_bml_client.sh`는 `make test-tools`에는 있지만 `bml check`와 CI tools job에는 없음 → 위 소유·종료·provider 결함이 모두 green으로 합쳐진다. | fake ssh/cloudflared/curl로 forced provider, child death, TERM-ignore, fallback, URL parsing, gate rotation을 end-to-end 검사한다. client·shutdown·ownership 스위트를 `bml check`와 CI에서 동일하게 실행한다. |

## 질문 / 확신 없음

- localhost.run과 Pinggy의 HTTP 모드는 edge에서 TLS를 종료하므로 제공자가
  미공개 실험 데이터와 공유 암호의 평문을 처리한다. 이 신뢰 경계를 연구실
  정책이 허용하는지 결정이 필요하다.
- 운영자 한 명의 Tailscale 계정·tailnet 설정은 허용되지만 앱 사용자별 계정은
  금지인지가 불명확하다. 전자만 허용되면 장기 공유에는 Funnel이 더 안정적인
  후보가 된다.
- localhost.run 무료 tier 문서는 20 MB request body와 SSE 지원을 보장하지
  않는다. 실제 랩 망에서 성공했다고 간주하려면 아래 acceptance test가 필요하다.

## 이상 없음을 확인한 것

- 암호가 빈 정상 설정에서는 게이트가 요청을 그대로 통과하고, 빈 암호를 올바른
  로그인으로 받아들이는 경로는 없었다.
- `_gate`는 write announcement 미들웨어보다 바깥에 구성되어 보호된 401 요청은
  actor 설정, router, DB에 도달하지 않는다.
- `/assets/*`, SPA fallback, API router는 모두 게이트 안에 있고 문 밖 경로는
  exact `/api/health`, `/__login`뿐이다.
- 암호 변경 뒤 이전 HMAC cookie는 새 암호와 일치하지 않는다.
- 로그인 HTML에는 제출한 암호나 다른 사용자 입력이 반사되지 않아 f-string 기반
  HTML injection 경로는 확인되지 않았다.
- `SameSite=Lax`, JSON API, 상태 변경 GET 부재를 함께 볼 때 일반적인
  cross-site form/fetch CSRF 우회는 확인되지 않았다.
- SSH 명령에는 `StrictHostKeyChecking=accept-new`, `ExitOnForwardFailure=yes`,
  keepalive가 있고 `nohup ... </dev/null`의 stdin EOF도 mock에서 확인했다.
  다만 비대화식 보장은 발견 #12처럼 불완전하다.
- `.bml/env`는 같은 디렉터리 임시 파일로 교체하고 mode 0600을 시도하며, 다른
  정상 key를 보존한다.
- `bml use`는 health 확인이 성공한 뒤에만 주소를 저장한다. 다만 그 health의
  신원성이 발견 #13처럼 부족하다.
- `git diff --check d41aec3e^..14dff93c`는 깨끗했고, `apps/api/tests/test_gate.py -q`는
  11건 통과했다. 전체 WSL shell suite는 이 실행기의 시간 제한 안에 끝나지 않아
  통과로 주장하지 않는다.

## 터널 제공자

### 결론

localhost.run은 **이번에 실측한 망에서 TCP 22가 열려 있고 계정이 필요 없다는
점에서는 합리적인 임시 fallback**이다. 다만 현재 구현은 공식 hostname을 놓칠 수
있고, free HTTP tunnel이 평문 HTTP endpoint도 제공하며, SSE·20 MB body·수 시간
유지 계약이 문서화되어 있지 않다. 따라서 "health 200 한 번"만으로 채택하지 말고
아래 검증을 통과할 때만 실험용 provider로 남기는 것이 맞다.

- 정확히 20 MB인 `.wrd` 업로드 후 보존 원본 SHA-256 일치
- 같은 크기 원본 및 CSV/XLSX 다운로드의 byte/행 검증
- 두 브라우저의 SSE revision을 최소 1시간 유지하고 재연결 후 누락 없음 확인
- 서버 restart, SSH 단절, 무료 주소 변경 뒤 URL·PID 상태 갱신 확인
- `http://공유-host`가 HTTPS로 강제되고 gate cookie가 Secure인지 확인

localhost.run 무료 tier는 가입 없이 쓸 수 있지만 주소가 정기적으로 바뀌고 속도
제한이 있으며, FAQ는 무료 주소가 몇 시간 뒤 바뀐다고 설명한다. 또한 HTTP
tunnel은 provider가 TLS를 복호화한다.
[무료 tier 제한](https://localhost.run/docs/forever-free/),
[주소 수명 FAQ](https://localhost.run/docs/faq/),
[보안 모델](https://localhost.run/docs/security/).

### 대안

1. **계정 없는 443 임시 경로: Pinggy.** 공식 SSH endpoint가 TCP 443이고 토큰
   없이 시작할 수 있으며 HTTPS 강제 옵션 `x:https`와 SSE 지원 사례가 문서화되어
   있어 현재 망 요구에 더 가깝다.

   ```sh
   ssh -p 443 \
     -o BatchMode=yes \
     -o ExitOnForwardFailure=yes \
     -o ServerAliveInterval=30 \
     -o ServerAliveCountMax=3 \
     -R0:127.0.0.1:5003 \
     -t free.pinggy.io x:https
   ```

   다만 무료 세션은 60분이고 재연결 때 URL이 바뀌며 HTTP tunnel은 provider가
   내용을 읽을 수 있다. 20 MB 제한은 공식 보장이 없으므로 동일 acceptance test가
   필요하다. [Pinggy SSH/443와 무인증 사용](https://pinggy.io/docs/usages/),
   [HTTPS 강제](https://pinggy.io/docs/http_tunnels/),
   [60분 제한](https://pinggy.io/help/),
   [SSE 사례](https://pinggy.io/docs/guides/pocketbase/).

2. **장기 공유: Tailscale Funnel.** 호스트 운영자는 계정·tailnet·MagicDNS·HTTPS·policy
   설정이 필요하지만 방문자는 Tailscale 계정 없이 공개 URL을 쓸 수 있고, 어려운
   망에서는 coordination/DERP가 TCP 443을 사용한다. 앱의 사람별 로그인은 새로
   만들지 않아도 된다. 단, Funnel은 beta이고 비설정 bandwidth limit이 있으므로
   운영자 계정을 허용할 때만 후보로 삼는다.
   [Funnel 개요와 방문자 조건](https://tailscale.com/docs/features/tailscale-funnel),
   [요구사항과 제한](https://tailscale.com/docs/features/tailscale-funnel#requirements-and-limitations),
   [443 relay](https://tailscale.com/docs/reference/faq/firewall-ports).

3. **Cloudflare Quick Tunnel은 현재 기본값으로 부적합.** 7844가 막힌 실측
   망에서는 연결되지 않고, 열린 망에서도 공식적으로 SLA가 없으며 SSE를 지원하지
   않는다. HTTP/2는 TCP 7844, QUIC은 UDP 7844이므로 현재 문서와 preflight도
   바로잡아야 한다.

LocalTunnel은 설치는 간단하지만 public service의 data plane이 443-only라는
계약이 없고, 자체 server 문서도 client 연결에 임의의 non-root TCP port를
사용한다고 설명하므로 이번 방화벽 조건의 우선 대안으로 삼기 어렵다.
[LocalTunnel client](https://github.com/localtunnel/localtunnel),
[server 연결 모델](https://github.com/localtunnel/server).
