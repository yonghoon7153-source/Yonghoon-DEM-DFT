# COMSOL63_LATE_CAP_A_HANDOFF — 원문 보존 기록 (2026-09-14)

`.gitattributes` 의 `reviews/r14_repros/codex63/late_cap_a/** -text` 로 bytes 그대로 저장된다. 판정은
`docs/COMSOL_REBUILD_SPEC.md` §17. 보존은 `scripts/preserve_handoff.sh` 로 했다 (묶음 여덟 번째, 첫 스크립트 사용).

| 검사 | 결과 |
|---|---|
| ZIP 크기 | **780,744,308 bytes** — 전달값과 일치 |
| ZIP SHA-256 | `63bdb39c2956e1865441e26ffff344017b6c884519a7e94cf7c8acbf717e60b7` — 일치 |
| manifest 자체 SHA-256 | `d7c19bb00a90fe42fa647d70adc5d5b98549b60750d4cfc0f2d7bc0c4de8ccc2` — 일치 |
| 명세 | **201** payload (+ manifest 1) |
| ZIP 안 전수 대조 | **201 / 201 sha 일치** · 불일치 0 · 없음 0 |
| 보존한 항목 | **140** 개 — 복사 뒤 sha 일치 140, 불일치 0 |
| 제외한 항목 | **61** 개 (mph·로그·java·py·그림·중첩 ZIP·8 MiB 초과 profile CSV) |
| **커밋 안 bytes** | **140 / 140 일치** — 줄끝 정규화 없음 (`-text` 규칙이 묶기 **전에** 들어갔다) |
| 재계산 | 여덟 비교 전부 + 성분 분해 + 간격 수, 원시 CSV 에서 일치 (§17-2) |

## 이 묶음의 함정 둘 — 실측으로 걸렸다

**(1) manifest 가 둘이다.** 이번 것(`outputs/late_cap_a/package_manifest.json`, `d7c19bb0…`)과 **이전
R320_TIMECAP 것**(`outputs/radial320_timecap/package_manifest.json`, `964b6817…`)이 같이 들어 있다.
`rglob("package_manifest.json")` 로 아무거나 집으면 엉뚱한 것과 대조하고 "일치 21 · 불일치 1" 같은 값이 나온다.
**이번 것을 경로로 명시해야 한다.**

**(2) `git show HEAD:<경로>` 는 저장소 루트 기준이다.** `bms-balancing/` 안에서 치면서 접두사를 빼면 전부
"미보존" 으로 나온다 (실측: `일치 0 · 불일치 0 · 미보존 201`). 보존 실패로 착각하기 쉽다.

둘 다 `scripts/preserve_handoff.sh` 가 찍어 주는 재대조 명령에 반영했다.

## 확인하지 않은 것

COMSOL 재실행 · ZIP 안의 스크립트 실행(하지 않았다) · java 소스 해시(보존 제외) · mph 해시(보존 제외) ·
현지 명부 1,099 개 중 나머지 1,042 개의 현재 바이트 · 물성·OCP 의 물리적 정확성 · 이전 TIME_CAPS raw ZIP
차이 원인(계속 **미확인**). 현지 승인 대화 · 중복 실행 부재 · 20 코어 요청 거부 과정은 **전달된 기록의 주장**이지
우리가 직접 관측한 사실이 아니다.
