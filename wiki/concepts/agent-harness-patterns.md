---
title: Agent Harness Patterns (채택·각색·기각)
description: "What we took from ponytail, caveman and superpowers — and what we deliberately did not, with reasons"
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: [tooling, design, wiki]
sources: [raw/repositories/2026-08-11-agent-harness-repos.md]
confidence: medium
explored: false
verificationStatus: unverified
model: claude-opus-5
effort: high
claimType: prescriptive
evidenceScope: multi-source-mixed
---

# Agent Harness Patterns (채택·각색·기각)

에이전트 작업 규율을 파는 외부 하네스 3종을 조사해, 이 모노레포에 **각색**해
넣은 결과와 그 판단 근거. 결과물은 루트 `CLAUDE.md` + `/finding` `/lean-review`
`/self-review` `/gate-request` 커맨드.

## 판단 원칙

플러그인을 통째로 설치하지 않았다. 이유 셋:
1. 세 하네스 모두 **세션 시작 훅으로 전역 행동을 바꾼다.** 이 저장소는
   적대적 게이트 리뷰 중이고 산출물 identity 가 커밋에 묶여 있어
   ([[provenance-fail-closed-verification]]), 통제 못 하는 행동 변경은 위험 대비
   이득이 없다.
2. 세 하네스의 기본 가정이 우리와 부분적으로 **어긋난다** (아래 표).
3. 우리에게 필요한 건 범용 규율이 아니라 **13라운드에서 실측된 우리 실패 패턴**에
   맞춘 규율이다.

## 채택 결과

| 출처 | 원래 형태 | 우리 적용 | 판정 |
|---|---|---|---|
| superpowers | TDD RED-first: 실패를 못 봤으면 옳은 것을 재는지 모른다 | `/finding` — 리뷰 발견은 반드시 RED 테스트부터. **+ 우리 고유 확장**: 테스트가 처음부터 통과하면 fixture 가 진실을 가린 것 | **전면 채택** |
| superpowers | verification-before-completion: 신선한 증거 없이 완료 선언 금지 | `CLAUDE.md` 상시 규칙 + 증명 명령 명시 (pytest / smoke_e2e) | **전면 채택** |
| superpowers | dispatching-parallel-agents / requesting-code-review | `/self-review` — 6개 렌즈 병렬 탐색 → 선별 → 적대적 검증 | **채택 (이미 실적 있음)** |
| ponytail | decision ladder (YAGNI → 재사용 → stdlib → …) | `/lean-review` — 단 **검증 코드는 carve-out**, 겨냥 대상을 중복·재구현으로 한정 | **방향 좁혀 채택** |
| ponytail | 강도 모드 lite/full/ultra/off | 미채택 — 모드 전환이 아니라 carve-out 목록이 우리 안전장치 | 기각 |
| caveman | 전역 출력 압축 (~65%) | **기계용 문서만** 밀도 압축 (`/gate-request`). 사용자 보고서는 압축 안 함 | **부분 채택** |
| caveman | 세션 시작 자동 활성 + statusline | 미채택 | 기각 |

## 왜 그렇게 갈렸는가

### superpowers 의 TDD 가 우리와 정확히 겹친 이유
"테스트가 즉시 통과하면 기존 동작을 재고 있는 것" 이라는 규칙은, 우리가
validator 를 강화할 때마다 **fixture 가 먼저 깨져야 정상**이라는 교훈과 같은
구조다. 이 저장소에서 fixture 가 위조 통로였던 사례가 4회 이상 실측됐다
(가짜 digest fixture, 이름 규칙이 실제와 다른 half-cell meta, canonical 이 아닌
조건 ID 등). superpowers 는 이것을 일반 규칙으로 먼저 적어 둔 셈이다.

### ponytail 을 방향만 좁혀 받은 이유
ponytail 의 안전 carve-out 은 "trust-boundary validation … never on the chopping
block" 이다. 우리 저장소에서 **거의 모든 코드가 그 카테고리**다 — 13라운드 리뷰가
계속 검사를 **더** 요구했고, 줄이는 방향의 압력은 리뷰가 아니라 우리 피로에서
온다. 그래서 사다리는 검증 축이 아니라 중복·재구현에만 쓴다. 실제 후보:
env 결정축 비교가 두 파일에 중복, check 작성 보일러플레이트, smoke 의 heredoc 반복.

### caveman 을 전역으로 받지 않은 이유
이 프로젝트의 사용자용 산출물(리뷰 요청문 해설, 상태 보고, 판단 근거)은
**압축하면 근거가 사라진다.** caveman 자신도 에이전틱 실행에서 절감이 8.5%로
떨어진다고 정직하게 공개하는데, 우리 세션이 정확히 그 형태(도구 호출·diff 위주)다.
반면 게이트 리뷰 요청문은 **다른 LLM 이 읽는다** — 거기서는 밀도가 곧 품질이라
그 경계에만 적용했다.

## 한계·불확실성
- 세 저장소의 벤치마크 수치(LOC 54%↓, 토큰 65%↓)는 **저자 자기보고**이고 우리가
  재현하지 않았다. 채택 근거로 쓰지 않았다 — 채택 이유는 전부 우리 실측 실패
  패턴과의 부합 여부였다.
- raw 는 README 원문이 아니라 WebFetch 요약이다. 인용문은 요약에 포함된 직접
  인용이며, 원문 대조 검증(`/wiki-verify`)은 아직 하지 않았다.
- `/lean-review` 의 carve-out 목록은 지금까지의 리뷰 발견에 근거한다 — 새 축이
  생기면 갱신해야 한다.

## 첫 실행 결과
`/lean-review` 를 처음 돌린 결과는 [[lean-review-backlog]] — 실제 중복 3곳을
찾았고, carve-out 규칙("리뷰 라운드 중에는 source_digest 를 바꾸지 않는다")이
실행을 보류시켰다. 규율이 의도대로 작동한 첫 사례다.

## 관련
- [[provenance-fail-closed-verification]] — carve-out 이 지키려는 원칙 본체
- [[gate-review-loop]] — `/self-review` `/gate-request` 가 들어가는 루프
- [[degradation-degeneracy]] — 이 규율이 적용되는 대상 프로젝트
