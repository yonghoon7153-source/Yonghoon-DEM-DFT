---
title: Gate Review Loop
description: "Adversarial external-review loop: fix, verify, push, request review with target commit, only GO starts the expensive run; since 2026-11-26 one prompt goes to two rebuttal windows (Codex, agy) and the replies are reconciled item by item"
created: 2026-08-11
updated: 2026-11-26
type: guide
tags: [gate-review, design, project]
sources: [raw/repositories/degradation-degeneracy-audit.md, raw/transcripts/2026-11-26-dual-rebuttal-rule.md]
confidence: high
explored: false
verificationStatus: unverified
model: claude-fable-5
effort: high
claimType: prescriptive
evidenceScope: multi-source-primary
---

# Gate Review Loop

비싼 본 실행(예: 10시간 fitting) 전에 외부 리뷰어(Codex)와 도는 적대적 게이트
루프. [[degradation-degeneracy]] 에서 13 라운드 운영하며 정련된 절차.
2026-11-26 부터는 같은 프롬프트를 Codex 와 agy (Antigravity) 두 반박창에 준다 — 아래 '반박 두 곳'.

## 루프
0. **자체 리뷰(선택)**: 요청 전 `/self-review` 로 다각 렌즈 적대적 탐색.
   CONFIRMED 는 아래 1로 보낸다 ([[agent-harness-patterns]] 의 채택 항목).
1. **수정**: 직전 리뷰의 발견을 **코드로** 닫는다 — `/finding` 절차(RED 테스트
   먼저, fixture 감사) (절차적 우회는 최후수단 —
   리뷰어가 "코드 우선"을 권고했고 실제로 재실행 폐기를 줄였다). 원칙은
   [[provenance-fail-closed-verification]].
2. **검증**: 전체 테스트 + strict smoke (dirty 완화 없음, clean 커밋에서) 통과.
   리뷰가 재현한 반례는 그대로 회귀 테스트로 고정한다.
3. **push** 후 **리뷰 요청문** 작성 (`/gate-request`):
   - 대상 커밋 SHA 명시 (리뷰어는 exact HEAD 를 fetch 해 검증한다)
   - 발견별 대응 위치(파일·검사 이름)와 회귀 테스트 이름
   - 판단이 갈릴 수 있는 지점은 명시적 질문으로 (예: 자기치유 vs 명시적 거부)
   - 실측 출력(validator 검사 목록 등)을 첨부해 재현 가능하게
   - 반박 창이 둘이면 같은 본문 하나를 두 창에 그대로 준다 (아래 '반박 두 곳' 1)
4. **리뷰 수신**: NO-GO 발견은 유효성만 빠르게 확인하고 다시 1로. 리뷰어 지적이
   맞으면 그대로 수용하고, 갈리면 근거를 들어 질문으로 되돌린다.
   반박 창이 둘이면 두 회신을 함께 반입해 대조표 하나로 정리한다 (아래 2–5).
5. **GO 후에만** 본 실행. 실행 절차·보존 증거 목록도 리뷰 요청문에 미리 합의한다.
   반박 창이 둘이면 두 판정이 다 GO 일 때만 GO 다 (아래 6).

## 반박 두 곳 — Codex · agy (2026-11-26 · 1저자 지시)

지시 원문은 `raw/transcripts/2026-11-26-dual-rebuttal-rule.md`, 상시 규칙은 루트 `CLAUDE.md` 작업 규율 8 이다.
여기는 그 절차다.

1. **발송** — 요청서 하나 · 발송 본문 하나 (`/gate-request`). 같은 본문을 Codex 반박창과 agy (Antigravity) 반박창에 그대로 준다.
   본문은 받는 쪽을 가리지 않게 쓰고, 같은 회차의 다른 쪽 판정문은 요청서 · 첨부에 넣지 않는다 (서로의 판정문은 보지 않게 —
   앞 회차 회신은 이미 저장소에 있으므로 같은 회차 기준이다).
2. **반입 순서** — 두 결과 (인계 ZIP) 가 다 온 뒤 **함께** 반입한다. 먼저 온 쪽은 스크래치에만 두고 저장소에 넣지 않는다.
   두 창 다 저장소를 읽을 수 있어서, 먼저 넣으면 늦은 쪽이 그 판정문을 볼 수 있다.
3. **반입 꼴** — 지금 관례 그대로 (ZIP 원본 · 안전하게 푼 사본 · 받은 원본 · 매니페스트 · 비밀값 검사 · 검토자 도구는 실행하지 않음) 를
   검토자마다 따로 둔다 (`codex/` · `agy/`). 보존 규칙 (`-text`) 은 바이트보다 먼저 커밋한다.
4. **대조표** — 그 흐름의 원장 반입 절에 하나로 둔다 (게이트 = `degradation-degeneracy/docs/08_REVIEW_RESPONSE.md` ·
   REIL = `bms-balancing/docs/REIL_PREREQUISITES_STATUS_20261004.md` 등).

   | 항목 | Codex 판정 | agy 판정 `[agy · 대조 중]` | 일치 · 엇갈림 | 우리 재현 | 처분 |
   |---|---|---|---|---|---|

   - **일치** = 두 판정이 같다 (지적 · 심각도 · 수용 여부). **엇갈림** = 판정이 다르거나 한쪽만 지적했다.
   - **우리 재현** = 허용된 범위 (읽기 · 합성 시험 · 재현 시험 먼저 — `/finding`) 에서 우리가 직접 본 결과. 검토자가 준 코드는 실행하지 않는다.
   - **처분** — 일치 칸은 평소 절차대로. 엇갈림 칸은 한쪽을 조용히 고르지 않고 **1저자 질문** 으로 남긴다 (권고 한 줄).
5. **agy 표지** — agy 판정은 `[agy · 대조 중]` 을 달고, Codex 판정과 같은 무게로 '확인됨' 처리하지 않는다. agy 만 낸 지적은 우리가
   재현해도 '우리 재현 (agy 제기)' 로 적는다. 가중은 몇 번 대조한 뒤 1저자가 정한다 — 회차마다 남는 대조표가 그 근거다.
6. **GO** (이 루프의 실행 문턱) — 두 판정이 다 GO 면 GO. 엇갈리면 (한쪽만 GO 포함) 실행하지 않고 1저자에게 묻는다.

## 이 프로젝트의 참조 (living reference)
- 발견 원장: `degradation-degeneracy/docs/08_REVIEW_RESPONSE.md`, `degradation-degeneracy/CHANGELOG.md`
- 리뷰 원문: `degradation-degeneracy/docs/1x_CODEX_*.md`
- 요청문 예: 13차 (대상 `c9970ebc`) — 발견 8건 표 대응 + 질문 5개 형식

## 한계
- 리뷰어와 요청자가 같은 저장소를 보므로, 요청문의 "실측"은 리뷰어가 재실행해
  검증하는 것을 전제로 한다 — 요청문 자체는 증거가 아니다.
- 위키에는 발견 번호(F1~F89 등)의 상세를 복사하지 않는다 — 원장이 정본.
