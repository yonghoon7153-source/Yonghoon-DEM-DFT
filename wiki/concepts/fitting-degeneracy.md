---
title: Fitting Degeneracy (LLI/LAM 분리가능성)
description: "Can one full-cell curve separate LLI, LAM_PE and LAM_NE — flat valley vs multimodal distinction"
created: 2026-08-11
updated: 2026-08-11
type: concept
tags: [battery, degradation, research]
sources: [raw/repositories/degradation-degeneracy-audit.md]
confidence: high
explored: false
verificationStatus: unverified
model: claude-fable-5
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

# Fitting Degeneracy (LLI/LAM 분리가능성)

## 정의
full-cell 전압 곡선 하나를 alpha-beta 반쪽셀 재구성으로 fitting 할 때, 서로 다른
열화 조합 (LLI, LAM_PE, LAM_NE) 이 **구분 불가능하게 같은 곡선**을 만드는 현상.
degeneracy 가 있으면 fitting 이 낸 분해값은 물리가 아니라 최적화 우연이다 —
[[22p-physics-or-degeneracy]] 의 핵심 전제.

## 두 실패 모드 (처방이 정반대)
- **flat valley** — 같은 목적함수 값(J)인데 해가 서로 멀다. 데이터가 그 조합을
  구분하지 못한다는 **직접 증거**. 초기값을 잘 줘도 사라지지 않고, 측정 방식을
  바꿔야 줄어든다.
- **multimodal** — J 가 다른 국소최소가 여럿. degeneracy 가 아니라 **최적화
  난이도**. 좋은 초기값(warm start)으로 사라진다.
- 이 구분을 위해 multi-start 진단은 무작위 restart 끼리만, 공정 비교는 같은
  restart 예산·index 집합으로 한다 ([[degradation-degeneracy]] 의 paired 설계).

## 판정 방법 (요약)
정답을 아는 합성 격자에서 복원 오차 |err| 와 tol(2%p) 기반 degenerate 판정,
clean 바이어스 보정, 복원가능군 한정 집계. PE·NE 가 같은 부호로 묶이는
flat 방향의 비율이 "LAM_PE ≈ LAM_NE 는 수학" 가설의 직접 증거 후보.

## 한계
- 판정은 tol 임계와 guard-feasible 모집단에 조건부다.
- 수치는 위키에 복사하지 않는다 — 정본은 artifact 와
  `degradation-degeneracy/docs/RESULTS*.md` ([[provenance-fail-closed-verification]]).
