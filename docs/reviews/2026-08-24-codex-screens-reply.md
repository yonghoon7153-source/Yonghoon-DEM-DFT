---
title: Codex 화면 리뷰 회답
created: 2026-08-24
updated: 2026-08-24
type: review
tags: [review, audit, crosscheck, wsl, tooling]
sources: [docs/reviews/codex-review-screens-and-wsl.md, tools/bml]
confidence: high
explored: true
verificationStatus: verified
verifiedAt: 2026-08-24
---

# Codex 화면 리뷰 회답 — 15건 전부 대응

받은 리뷰: 높음 4 · 중간 9 · 낮음 2 (범위 `a7efba10..284a4582`).
**승인 보류가 맞았다.** 15건 중 반박한 것은 없다 — 전부 실제로 사고가 되는
것이었고, 특히 1·2·3 은 노트북에서 `bml mirrored` 를 돌리기 전에 막아야 했다.

> 이 표만 갱신한다. 원문 지적은 고치지 않는다 — 무엇을 지적받았는지가 남아야
> 한다. 원문은 상대 세션의 출력이고, 요청서는
> [codex-review-screens-and-wsl](codex-review-screens-and-wsl.md) 이다.

| # | 심각도 | 상태 | 커밋 | 무엇을 했나 |
|---|---|---|---|---|
| 1 | 높음 | **닫음** | `5aca3651` | 짐작한 경로에 안 쓴다. `windows_home_verified` (interop 이 말한 `%USERPROFILE%`) 일 때만 고치고, 못 물어보면 짐작을 "아마 여기" 로만 보여 준다 |
| 2 | 높음 | **닫음** | `5aca3651` | `wslconfig_writable_reason` 이 원본·백업의 심볼릭 링크, 비정규 파일, 권한, BOM 을 보고 하나라도 걸리면 손대지 않는다 |
| 3 | 높음 | **닫음** | `5aca3651` | 단계마다 실패를 확인하고, 완성본을 검사(넣은 줄이 있는가·원본보다 짧지 않은가)한 뒤에야 원본에 손댄다. 임시 파일은 같은 폴더에 만들고 `mv` 로 갈아 끼운다 |
| 4 | 높음 | **닫음** | `e8fc9e0a` | PowerShell 한 줄이 cmdlet 대신 `[IO.File]::Read/WriteAllText` + `UTF8Encoding($false)` 를 쓴다. 링크면 `throw`, 멱등, 백업은 없을 때만 |
| 5 | 중간 | **닫음** | `5aca3651` | 멱등 판정을 백업보다 **먼저** 한다. 이미 있는 백업은 안 덮고, 백업을 못 뜨면 고치지 않는다 |
| 6 | 중간 | **닫음** | `e8fc9e0a` | `sync_repo` 가 재실행 **전에** unmerged 를 보고, 있으면 멈추고 `git stash list` 와 복구 절차를 짚는다 |
| 7 | 중간 | **닫음** | `fb9d2b07` | 어댑터 이름 대신 **기본 경로**(`route print -4 0.0.0.0`, 메트릭 최소)를 본다. 못 읽으면 이름 규칙으로 물러선다 |
| 8 | 중간 | **닫음** | `e8fc9e0a` | "172. 는 WSL 것" 을 지우고 "`vEthernet (WSL)` 어댑터에 붙은 것만 빼라" 로 바꿨다 |
| 9 | 중간 | **닫음** | `fb9d2b07` | `door_password_works` 가 `/__login` 을 두드려 303 을 확인한다. `status` 가 갈라 말하고, `share` 는 그 확인을 통과해야 연다 |
| 10 | 중간 | **닫음** | `fb9d2b07` | `tls` 는 "손잡기 자체를 확인한 것은 아닙니다 … 열릴 수 있습니다" 로, `dns`+살아있음은 "터널 프로그램은 살아 있으니 … 쪽이 유력합니다" 로 물렸다 |
| 11 | 중간 | **닫음** | `fb9d2b07` | `Status` 가 0 이고 `Answer` 가 비어 있지 않을 때만 `exists`. "DNS 를 1.1.1.1 로 두라" 제안은 뺐다 |
| 12 | 중간 | **닫음** | `248248c5` | `is_our_tunnel_url` — 제공자 도메인만 접미사로 인정한다. 502·503·504·530 은 "터널이 끊겼다" 로 곧장 말한다 |
| 13 | 중간 | **닫음** | `5aca3651` | `wsl.exe` 를 `win_exe` 로 찾아 **절대 경로로** 준다. 못 찾으면 "Windows PowerShell 에서 `wsl --shutdown`" 으로 분기 |
| 14 | 낮음 | **닫음** | `e8fc9e0a` | `unknown` 이면 "확인하지 못했습니다 (HTTP …)" 로 찍는다 — 줄이 사라지면 "문이 없구나" 로 읽힌다 |
| 15 | 낮음 | **닫음** | `e8fc9e0a` | userinfo 를 떼고, 앞이 `-` 이거나 빈 라벨이면 거부한다 |

## 테스트 지적에 대해

리뷰가 "최종 화면이 어떤 행동을 시키는가는 대부분 빠져 있다" 고 한 것이 맞았다.
그 지적대로 고친 것:

- `cmd_mirrored` 를 **끝까지** 돌린다 (고침 → 백업 → 두 번째엔 무동작 → 백업
  보존 → 사용자 미확인 시 무동작 → 링크 두 종류에서 가리킨 파일 바이트 불변 →
  BOM 파일 불변).
- `win_exe` 의 System32 갈래를 `WIN_SYSTEM32` 로 갈아 끼워 **실제로** 탄다
  (예전에는 가짜 폴더를 만들기만 하고 안 써서 분기를 지워도 통과했다).
- `door_password_works` 를 303/401/빈 암호로 본다. `share` 가 그 확인을
  부르는지도 코드에서 센다.
- `server_unreachable_help` 를 코드별로(503·404) 돌려 **어느 안내로 가는지**를 본다.
- `sync_repo` 의 unmerged 검사가 재실행보다 **앞에** 있는지를 줄 번호로 본다.

**옛 시험 셋이 틀린 것을 정답으로 고정하고 있었다** — 잘못된 사용자 추정,
백업 삭제, 그리고 `https://127.0.0.1:1` 을 '터널 주소' 로 보던 전제. 전부
바꿨다. 89 → **201건** (+ 터널 33 → 66건).

## 여전히 확인 못 한 것

- **Windows PowerShell 5.1 자체로는 못 돌렸다.** 4번 수정은 PowerShell 7.4.6
  (Linux)으로 여덟 경우 — 다섯 상태 + 한글 UTF-8 왕복 + 링크 + 기존 백업 —
  을 돌려 확인했다. 5.1 에서 같게 도는 근거는 **cmdlet 을 아예 안 쓰고
  `[IO.File]` + 명시 인코딩만 쓴다**는 것이다. 그 검증 중에 멱등 판정이 CRLF
  에서 안 먹는 것을 잡았다 (`[ \t]*$` 가 `\r` 을 못 넘음).
- **`route print` 실물 출력으로는 안 돌렸다.** 픽스처(한국어 열 이름, 메트릭
  두 개, 마스크 칸의 `0.0.0.0`)로만 고정했다.
- **`appendWindowsPath=false` 기계는 못 만들었다.** `WIN_SYSTEM32` 를 갈아
  끼운 가짜로만 확인했다.
- **DoH 실제 전송은 여전히 못 했다** (컨테이너 프록시가 1.1.1.1 을 막는다).
  JSON 판정만 픽스처로 고정했다.
- mirrored 적용과 interop 복구는 이 사이에 **사용자 기계에서 실측됐다** —
  `docs/log.md` 의 같은 날짜 항목에 있다.

## 관련

- [codex-review-screens-and-wsl](codex-review-screens-and-wsl.md) — 보낸 요청서
