---
title: 22p 결과는 물리인가 fitting degeneracy 인가
description: "Is the seminar 22p LLI/LAM decomposition (LAM_PE=LAM_NE=13%, LLI=17%) real physics or an artifact of non-identifiability"
created: 2026-08-11
updated: 2026-08-11
type: research-question
tags: [battery, degradation, research]
sources: [raw/repositories/degradation-degeneracy-audit.md]
confidence: medium
explored: false
verificationStatus: unverified
model: claude-fable-5
effort: high
claimType: empirical
evidenceScope: multi-source-primary
status: active
feedsInto: "세미나 재발표 결론 + degradation-degeneracy/docs/RESULTS.md 결론 1~3"
---

# 22p 결과는 물리인가 fitting degeneracy 인가

## 질문
2026-08-05 세미나 22p 의 열화 분해(LAM_PE ≈ LAM_NE ≈ 13%, LLI ≈ 17%)는 실제
물리인가, full-cell 곡선 하나로는 두 전극을 가를 수 없어 생긴
[[fitting-degeneracy]] 인가?

## 왜 중요한가
이 분해값이 세미나·후속 연구의 근거로 인용된다. degeneracy 라면 "PE 와 NE 가
같은 비율로 열화했다"는 서사 자체가 수학적 우연이고, 측정·목적함수를 바꿔야 한다.

## 가설
LAM_PE ≈ LAM_NE 는 물리가 아니라 **flat valley 방향에서 두 전극이 같은 부호로
묶이는 degeneracy** 의 산물이다 (귀무: 실제로 대칭 열화).

## Evidence For (가설 지지)
- (방향성 관측, 인용 금지 등급) 이전 coarse/이전-세대 실행에서 grid 기준 fitting
  의 상당 비율이 degenerate 로 판정되고, flat 방향에서 PE·NE 동부호 결합이
  관찰됨 — 정확한 비율은 clean 본 실행 후 확정.

## Evidence Against
- (방향성 관측, 인용 금지 등급) half-cell 기준(Case 1)과 dQ/dV 항 추가가 복원
  오차를 줄이는 방향 — 조건에 따라 분리가 가능할 수 있음.

## Status Log
- **[2026-08-05]** 세미나 22p 발표 — 질문 성립.
- **[2026-08-11]** 판별 파이프라인이 13차 게이트 리뷰 대기
  ([[degradation-degeneracy]], [[gate-review-loop]]). 본 실행(grid v4, 10h) 전 —
  위 Evidence 는 전부 잠정. GO 후 artifact 수치로 이 카드를 갱신한다.
