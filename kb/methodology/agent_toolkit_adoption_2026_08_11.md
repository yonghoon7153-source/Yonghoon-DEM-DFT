---
title: 외부 에이전트 툴킷 3종(ponytail · caveman · superpowers) 검토와 선별 채택
date: 2026-08-11
updated: 2026-08-11
tags: [methodology, agent, tooling, code-discipline, adoption]
status: 확정
confidence: medium
verificationStatus: unverified
explored: false
authoredBy: agent
effort: medium
claimType: prescriptive
evidenceScope: multi-source-mixed
---

## 검토 대상

- **ponytail** (DietrichGebert) — "가장 게으른 시니어" 판단 사다리를 코드 생성 **전에** 태워
  안 쓴 코드를 늘린다. 주장: 코드 ~54% 감소.
- **caveman** (juliusbrussee) — 산문 출력 압축. 주장: 산문 65% 절감, **자체 실측으론
  실제 에이전틱 런에선 8.5%** (HONEST-NUMBERS.md 로 공개 — 이 정직성은 배울 점).
- **superpowers** (obra) — 브레인스토밍 → 설계 승인 → 2–5분 작업 분해 → 서브에이전트
  구현 + 2단 리뷰 → TDD(RED-GREEN-REFACTOR) → 코드 리뷰.

## 먼저 잰 것 — 우리한테 그 문제가 있나

| 지표 | 실측 (2026-08-11) |
|---|---|
| tools/ 규모 | py **305** · sh **106** · **62,410줄** |
| MSD 함수 자체 구현 | **8개 파일** |
| 아레니우스 적합 자체 구현 | **6개 파일** |
| watch_* / run_* 스크립트 | 26 / 56 |
| assert·selftest 보유 | 305 중 **30개 (~10%)** |

**그런데 규약은 아직 안 갈라졌다.** D 추출은 검사한 12개 파일 전부 자유절편
polyfit(정본 `MSD = c + 6Dt`), kB 는 `8.617333262e-5`(15) vs `8.617333e-5`(9)로
상대차 1e-7 — 물리적으로 무의미. 즉 **중복은 크지만 피해는 아직 0**이다.

이 측정이 채택 범위를 정했다: 지금 있는 문제를 고치는 도구가 아니라 **회귀 가드**만
필요하다. (ponytail 사다리 1번 "이게 존재할 필요가 있나" 를 우리 자신에게 적용한 결과)

## 채택

| 출처 | 채택한 것 | 형태 |
|---|---|---|
| ponytail | **재사용 사다리** — 새 스크립트 전 기존 도구 확인, 확장 > 신규 | CLAUDE.md §코드 규율 |
| ponytail | 규약 복사본 감시 | tools/convention_check.py (얇게 — 2검사 + 1경고) |
| superpowers | **selftest 에 음성 경로 필수** (틀린 입력을 잡는지) | CLAUDE.md §코드 규율 |
| caveman | **한계 공개 의무** (HONEST-NUMBERS 정신) — docstring 에 "못 하는 것" 절 | CLAUDE.md §코드 규율 |
| caveman | 선택적 압축 — 진행 보고는 짧게 | CLAUDE.md §코드 규율 |

`convention_check.py` 는 의도적으로 얇다: 검사는 ① 자유절편 D ② MSD 창 2–50 ps
두 개(틀리면 논문 숫자가 바뀜) + kB 자릿수 경고뿐. **아레니우스 온도 집합은 일부러
검사하지 않는다** — 타당한 변이가 많아 경고가 소음이 된다. 예외는 EXEMPT 에 사유와 함께.

## 기각

| 출처 | 기각한 것 | 사유 |
|---|---|---|
| ponytail | 강도 레벨(lite/full/ultra) · 부채 추적기 · 전체 감사 명령 | 우리 코드는 제품이 아니라 분석 도구. 위험 축은 "코드 양"이 아니라 **규약 일관성**이고, 그건 이미 2검사로 덮인다 |
| caveman | **전면 산문 압축** | CLAUDE.md 소통 규칙이 "새 개념은 한 단계씩 설명"을 명시 — 정면 충돌. 게다가 그들 자체 실측도 에이전틱 런 8.5% |
| superpowers | TDD RED-GREEN-REFACTOR 전면 도입 | 우리 도구의 정답은 단위테스트가 아니라 **물리 정합성**이다. 대신 selftest 음성 경로 + Codex/자체 교차검증이 같은 자리를 이미 채운다 |
| superpowers | 브레인스토밍→설계승인 단계 신설 | 이미 있다 — 붙여넣기 워크플로 + 리뷰 왕복 |
| 셋 다 | 플러그인/마켓플레이스 설치 | 외부 코드를 캠페인 repo 에 상주시키지 않는다. 필요한 규칙만 우리 문장으로 옮겨 적었다 |

## 한계

- 세 repo 의 성능 주장(54% · 65%)은 **재현하지 않았다** — 우리가 가져온 건 수치가 아니라 규율이다.
- `convention_check.py` 는 정규식 기반이라 AST 수준 우회(변수 경유 계산 등)는 못 잡는다.
  docstring 에 명시했다.
- 재사용 사다리의 효과는 미검증 — 다음에 새 스크립트를 만들 때가 첫 시험이다.
