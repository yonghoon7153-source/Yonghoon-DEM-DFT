# Codex 리뷰 과제 — 다른 기계에서 이 워크벤치를 보게 하는 길

[codex-session-bootstrap.md](codex-session-bootstrap.md) 로 세션을 연 뒤, 아래
"붙여넣는 프롬프트" 를 그대로 붙여넣는다.

이 리뷰는 **주제 하나**다: `bml use` / `bml share` / 공유 암호 게이트. 도메인
수치(mAh/g, knee, dQ/dV)는 이 변경이 건드리지 않았으므로 범위 밖이다.

## 왜 이 리뷰가 필요한가

이 저장소가 지금까지 지켜 온 것 중 두 가지를 이 변경이 건드린다.

1. **로그인을 두지 않는다** (ADR 0012). 이 변경은 조건부로 문을 하나 단다
   (ADR 0014). 랩 안에서는 아무것도 바뀌지 않아야 하고, 바깥에 열었을 때만
   서야 한다. **이 저장소에서 인증 비슷한 것을 처음 만든 것이므로, 가장
   덜 검토된 코드다.**
2. **우리 것임을 증명한 뒤에만 프로세스를 죽인다** (CLAUDE.md §0.8). 터널을
   띄우고 죽이는 코드가 새로 생겼다.

거기에, 이 변경의 대부분은 **쉘 스크립트**(`tools/bml`, +594줄)다. 이 저장소에서
테스트가 가장 얇은 층이고, 실패가 사용자 화면에 "안 됩니다" 로만 나타난다.

## 범위

```bash
git log --oneline d41aec3e^..d37b4071
git diff --stat d41aec3e^..d37b4071
```

| 파일 | 무엇 |
|---|---|
| `apps/api/app/gate.py` (신규) | 공유 암호 — HMAC 쿠키, 로그인 한 장 |
| `apps/api/app/main.py` | 게이트 미들웨어, `POST /__login` |
| `apps/api/app/settings.py` | `WORKBENCH_PASSWORD` |
| `apps/web/src/lib/api.ts` | 401 → 화면 다시 읽기 |
| `tools/bml` | `use` `password` `share` `share stop`, 주소 판정, 대기 |
| `docs/adr/0014-...md` | 결정 |
| 테스트 | `apps/api/tests/test_gate.py` (11), `tools/tests/test_bml_client.sh` (70) |

## 지금 상태 — 리뷰어가 알아야 할 것

이 랩 망에서 7844/TCP 가 막혀 있어 Cloudflare 터널이 안 됐다 (로그: `dial tcp
198.41.200.43:7844: i/o timeout`, 엣지 IP 여러 개, 45초). 실측한 포트:

```
region1.v2.argotunnel.com:7844  막힘
localhost.run:22                열림
connect.ngrok-agent.com:443     열림
```

그래서 제공자를 둘로 두고 `bml share` 가 7844 를 찔러 보고 고르게 했다
(`WORKBENCH_TUNNEL=auto|cloudflare|ssh`). **SSH 쪽(localhost.run)은 이 컨테이너
에서 22 가 막혀 실제로 붙여 보지 못했다** — 문법과 소유 판정, 주소 파싱만
시험했다. 리뷰에서 가장 의심스러운 부분이다.

## 이 브랜치에서 이미 잡은 것 (다시 찾을 필요 없음)

리뷰 시간을 아끼기 위해 적는다. 커밋 메시지에 각각의 실패 시나리오가 있다.

- `833874e1` 경로를 `$(...)` 로 돌려주다 진행 표시가 변수에 섞였고, `die` 의
  `exit` 이 서브셸만 끝냈다.
- `88a0fc0e` "공개" 를 설정에서 읽어, 설정 전에 띄운 서버에도 접속 가능하다고 했다.
- `96ec4bfb` / `0f0523ed` 대기를 횟수로 세서, 붙는 중인 터널을 우리가 죽였다.
- `a68c3c15` 터널을 창에 매달아 두어, 창을 닫으면 남이 오류 1033 을 봤다.
- `d37b4071` `close_tunnel` 이 pid 소유를 확인하지 않고 그룹째 죽였다.

## 붙여넣는 프롬프트

```text
이 브랜치의 커밋 d41aec3e^..d37b4071 을 리뷰해줘. 주제는 하나다: 다른 기계에서
이 워크벤치를 보게 하는 길 (bml use / bml share / 공유 암호). 결과는
docs/reviews/2026-08-21-codex-remote-access-review.md 한 파일로 작성해서 이
브랜치에 커밋해줘 (push 는 내가 말하면).

먼저 읽을 것: docs/adr/0014-share-with-a-tunnel-and-one-password.md,
docs/adr/0012-attribution-not-authentication.md,
docs/adr/0011-central-instance-for-data.md, CLAUDE.md 0장.

우선순위 (위에서부터 중요):

1. 게이트 (apps/api/app/gate.py, main.py 의 _gate 미들웨어와 /__login)
   - 암호가 비어 있을 때 정말로 아무것도 바뀌지 않는가. 빈 암호가 "문이 없다"
     가 아니라 "빈 암호가 맞다" 로 읽히는 경로가 하나라도 있는가
   - 미들웨어가 실제로 가장 바깥인가. 게이트를 통과하지 않고 DB 를 읽거나
     actor 를 찍는 경로가 있는가 (등록 순서 vs Starlette 의 스택 구성)
   - OPEN_PATHS 가 맞는가. /api/health 는 data_dir 절대경로와 wrdkit 판, 업로드
     상한을 돌려준다 — 인터넷에 열린 주소에서 이것이 문 밖에 있어도 되는가.
     닫으면 bml use 가 주소를 확인할 방법이 없어지는데, 다른 방법이 있는가
   - 쿠키: HttpOnly/SameSite=Lax 이고 Secure 는 없다. 터널은 https 인데
     Secure 를 안 거는 것이 맞는가. SameSite=Lax 만으로 이 API 의 쓰기
     (POST/PATCH/DELETE, JSON) 에 대한 CSRF 가 실제로 막히는가
   - /__login 에 시도 제한이 없다. 주소가 무작위라는 것에 얼마나 기대도 되는가
   - 정적 자산(/assets/*)과 SPA 폴백이 전부 문 안에 있는가
   - 암호를 바꿨을 때 옛 쿠키가 확실히 무효가 되는가
   - 로그인 페이지 HTML 이 f-string 이다. 사용자 입력이 그 안에 들어가는
     경로가 있는가

2. tools/bml 의 프로세스·상태 판정 — 남의 프로세스를 건드리는 경로
   - owns_tunnel_pid / looks_like_our_tunnel: 명령줄 문자열 매치로 소유를
     판정한다. 우회하거나 오판하는 입력이 있는가. tools/tests/
     test_bml_ownership.sh 가 고정한 포트 쪽 원칙과 일치하는가
   - close_tunnel 이 "우리 것이 아니면 표식만 지운다" 로 끝나는데, 그 뒤
     bml share 가 하는 판단이 옳은가
   - nohup 으로 띄운 터널이 고아가 된 뒤 tunnel.pid 가 낡았을 때의 순열
   - bml stop 이 터널을 닫는 것이 항상 옳은가 (dev 서버만 내리는 경우 등)
   - tunnel_via_ssh: 실제로 붙여 보지 못했다. `nohup ssh -T ... </dev/null` 이
     stdin EOF 로 조용히 끝나지 않는가. StrictHostKeyChecking=accept-new 가
     없는 옛 OpenSSH 에서는 어떻게 되는가. ExitOnForwardFailure 가 걸렸을 때
     try_tunnel 이 그것을 실패로 읽는가. 키가 없는 기계에서 nokey@ 인증이
     비밀번호 프롬프트로 빠지면 nohup 안에서 무슨 일이 생기는가

3. tools/bml 의 "사실이 아닌 말" — 이 브랜치의 버그가 전부 이 종류였다
   - listening_scope: ss 출력을 문자열로 판정한다. 포트 번호가 다른 줄에
     섞여 오판하는 경우 (5003 vs 15003 vs 원격 주소 열)
   - reachable_addresses: 100.64/10 판정, 192.168.56/24 제외, 남겨야 하는데
     버리는 대역이 있는가 (172.16/12 사설망을 통째로 버린다 — 맞는가)
   - normalize_server_url: 스킴이 있으면 그대로 믿는다. 사용자가 실제로 칠
     법한 입력 중 조용히 틀린 주소가 되는 것이 있는가
   - wait_until_alive 가 SECONDS 를 쓴다. 서브셸·set -u·긴 curl 과의 상호작용
   - write_env_key: 값에 들어갈 수 있는 문자 중 load_env_file 이 다르게 읽는
     것이 남아 있는가 (= 와 줄바꿈은 막았다). 따옴표, 앞뒤 공백, `~`, `#`
   - count_chars 의 UTF-8 가정 (이어지는 바이트 제거)

4. 화면 (apps/web/src/lib/api.ts)
   - 401 → location.reload() 가 무한 새로고침이 되는 경로가 있는가
   - 진행 중인 SSE 스트림(live.ts)이 401 을 받으면 어떻게 되는가
   - 타이핑 중 401 로 화면을 다시 읽으면 입력하던 값이 사라진다 — ADR 0012 가
     막으려던 것과 같은 실패다. 실제로 일어나는가

5. 문서-코드 일치
   - ADR 0014 가 적은 것과 코드가 하는 것이 같은가
   - docs/guides/central-server.md 의 명령과 출력 예시가 실제와 같은가
   - CLAUDE.md / AGENTS.md parity

보고 형식 (2026-08-21-codex-remote-access-review.md):

## 요약
전체 평가 3~5문장, 발견 수(심각도별).

## 발견
심각도 내림차순 표:
| # | 심각도 | 파일:줄 | 제목 | 실패 시나리오 | 제안 수정 |
실패 시나리오는 "어떤 입력/상태 → 어떤 잘못된 출력" 형식의 구체적 경로.
"안전하지 않을 수 있다" 는 발견이 아니다 — 무엇이 어떻게 되는지 적어라.
스타일·취향은 싣지 않는다. 확신이 없으면 다음 절로.

## 질문 / 확신 없음
결함인지 판단이 안 서는 것들. 왜 애매한지 한 줄씩.

## 이상 없음을 확인한 것
검토했고 문제 없다고 판단한 영역 목록.

## 터널 제공자
7844/TCP 가 막힌 망에서 쓸 수 있는 대안이 있으면 적어라. 조건: 계정 없이
되면 가장 좋고, 밖으로 나가는 443 만 쓰며, 이 앱에 로그인이 없다는 전제를
바꾸지 않는 것. 없으면 없다고 적어라.
```

## 검사 상태 (리뷰 시작 시점)

```
make check           통과
pytest (api+wrdkit)  212 통과
vitest               15 파일 통과
tools/tests          test_bml_client.sh 70 통과 · test_bml_ownership.sh ·
                     test_bml_shutdown.sh · test_lint_gate.sh · wiki_lint · backup
```

실측 `.wrd` 검증(`WRDKIT_SAMPLE=... pytest`)은 이 변경이 수치 경로를 건드리지
않아 돌리지 않았다. 수치 before/after 도 없다 — 바뀐 숫자가 없다.
