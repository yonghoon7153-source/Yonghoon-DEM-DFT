---
title: Gate Review Loop
description: "Adversarial external-review loop: fix, verify, push, request review with target commit, only GO starts the expensive run"
created: 2026-08-11
updated: 2026-08-11
type: guide
tags: [gate-review, design, project]
sources: [raw/repositories/degradation-degeneracy-audit.md]
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
4. **리뷰 수신**: NO-GO 발견은 유효성만 빠르게 확인하고 다시 1로. 리뷰어 지적이
   맞으면 그대로 수용하고, 갈리면 근거를 들어 질문으로 되돌린다.
5. **GO 후에만** 본 실행. 실행 절차·보존 증거 목록도 리뷰 요청문에 미리 합의한다.

## 이 프로젝트의 참조 (living reference)
- 발견 원장: `degradation-degeneracy/docs/08_REVIEW_RESPONSE.md`, `degradation-degeneracy/CHANGELOG.md`
- 리뷰 원문: `degradation-degeneracy/docs/1x_CODEX_*.md`
- 요청문 예: 13차 (대상 `c9970ebc`) — 발견 8건 표 대응 + 질문 5개 형식

## 한계
- 리뷰어와 요청자가 같은 저장소를 보므로, 요청문의 "실측"은 리뷰어가 재실행해
  검증하는 것을 전제로 한다 — 요청문 자체는 증거가 아니다.
- 위키에는 발견 번호(F1~F89 등)의 상세를 복사하지 않는다 — 원장이 정본.
