---
title: findings.json — 리뷰 발견 원장 (SR/RC 시리즈)
created: 2026-08-11
updated: 2026-08-11
type: entity
tags: [review, pipeline]
sources: [docs/reviews/findings.json, docs/reviews/codex_review_verdict_20260811.md, docs/reviews/selfreview_synthesis_vgcf_ptfe_se_grad_20260811.md]
confidence: high
explored: false
verificationStatus: unverified
author: agent
claimType: definition
evidenceScope: multi-source-primary
anchored: n-a
scope: n-a
---

# findings.json — 리뷰 발견 원장

## 개요
`docs/reviews/findings.json` — Codex 리뷰(RC 시리즈)와 자체 적대리뷰(SR 시리즈)의
발견을 **한 원장**에서 추적한다.  존재 이유 = RC6-Q8 교훈 "발견을 큐에서 잃지
않는다": 발견이 세션 로그에만 있으면 컨텍스트 압축과 함께 사라진다.

## 핵심 사실
- 항목 필드: id · severity(P1/P2…) · status(open / claimed_fixed /
  harness_ready_measurement_pending / verified…) · note(경위·수치·남은 것).
- `claimed_fixed` 는 **Codex 재검증 전** 상태 — 자칭 수정을 검증과 구분한다.
- 대표 항목: SR-01 (점-스탬프 조각남 — [[sr01-stamp-fragmentation]],
  측정 대기는 [[sr01-delta-sigma-sign]]) · SR-02 (서브에이전트 수치의 raw 미커밋
  = 증거등급 C 교훈 — 수치는 하네스와 함께 커밋).
- 앵커가 없어 배선을 멈춘 항목들은 별도로 [[anchor-waitlist]] 가 추적한다 (§F1).

## 관련 페이지·경로
- 원장을 채우는 절차: [[adversarial-review-protocol]]
- 위키 RQ 카드와의 관계: 겹치면 RQ 페이지가 ledger 항목을 sources 로 가리킨다
  (이중 기입 아님 — ledger 가 정본, RQ 는 근거 축적 층).
