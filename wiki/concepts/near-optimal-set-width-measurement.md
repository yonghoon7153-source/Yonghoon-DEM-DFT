---
title: 근최적 집합의 폭을 재는 법 (표집·Hessian 이 못 답하는 것)
description: "유도량이 근최적 집합 위에서 훑는 범위를 직접 미는 방법 — 등방 표집이 참 폭 40 %p 를 0.00 %p 로 보고한 반례에서 나왔다"
created: 2026-09-14
updated: 2026-09-14
type: concept
tags: [research, degradation, design]
sources: [raw/transcripts/2026-09-14-bms-handoff-width-and-wiki-candidates.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: prescriptive
evidenceScope: user-original
---

# 근최적 집합의 폭을 재는 법 (표집·Hessian 이 못 답하는 것)

## 정의

**폭**은 근최적 집합 `S = {p : J(p) ≤ J* · (1 + tol)}` 위에서 **유도량**
(LLI · LAM_PE · LAM_NE) 이 훑는 범위다. 파라미터 공간의 흩어짐이 아니라
**읽어 낼 값**의 도달 범위이므로, 축퇴 질문("이 결론이 데이터로 정해졌는가")에
직접 답하는 단위다.

세 가지가 서로 다른 것을 잰다:

| 방법 | 답하는 질문 | 못 답하는 질문 |
|---|---|---|
| Hessian 고윳값 | 그 방향이 최적점에서 국소적으로 평평한가 | 그 방향으로 **얼마나 멀리** 갈 수 있나 · 골짜기가 **휘면** 어디로 가나 |
| 최적점 둘레 등방 표집 | 최적점 **근처**의 흩어짐 | 좁고 긴 골짜기의 **끝** |
| 근최적 집합 극값 밀기 | 유도량이 실제로 훑는 범위 (하한) | 정확한 폭 · 신뢰구간 (아래 한계) |

## 왜 중요한가 — 실측 반례

`bms-balancing/` 의 옛 `cmd_degeneracy` 는 최적점 둘레에 등방 Gaussian 400 점을
뿌리고 **관측된** min/max 를 '폭' 이라 불렀다. 참 폭 40 %p 가 알려진 **굽은**
골짜기를 넣으면 그 방식은 **0.00 %p** 를 보고한다. 원인은 표본 부족이 아니라
방법의 종류다 — 등방 구름은 골짜기를 따라가지 않는다.

**Hessian 도 같은 뿌리의 한계를 다른 형태로 갖는다.** 둘 다 최적점 **국소**
정보다. `degradation-degeneracy/src/hessian.py` 는 이 사실을 스스로 적어 두고
있다 (docstring: "이 지표는 결론 근거가 아니다 — 참고 진단으로만 쓴다", 17차
발견 7). 비매끄러운 목적함수에서 수치 Hessian 이 수렴하지 않는 실측
(조건수 중앙값이 eps 1e-3 / 1e-4 / 1e-5 에서 12.8 / 229 / 17381) 도 같은 자리에
적혀 있다.

이 교훈이 **두 프로젝트에 동시에** 걸린다: `bms-balancing/` 의 α·β 식별
가능성 질문과 `degradation-degeneracy/` 의 [[fitting-degeneracy]] 질문은 같은
모양이다.

## 방법 — 두 갈래의 합집합

사각지대가 서로 달라 **둘을 같이 쓰고 합집합을 취한다**.

1. **직접 제약 최적화** — `J(p) ≤ limit` 를 제약으로 걸고 유도량(mode)을
   최적화한다. 골짜기 바닥에서 제약의 기울기가 0 이 되어 LICQ 가 깨지면 더
   못 미끄러진다.
2. **mode 등식 프로파일** — mode 를 `= v` 로 묶고 `J` 를 최소화해 그 `v` 가
   도달 가능한지 본다. 1 이 막히는 자리를 메운다. 격자는 1 이 찾은 범위
   **둘레에 모은다** — 상자 전체에 깔면 근최적 집합 근처가 성기다 (실측:
   LLI 도달 격자점이 22 개 중 1 개).

합성 검증 (참 폭 40 %p 골짜기):

| 골짜기 두께 | 등방 구름 | 이 방법 |
|---|---:|---:|
| 부피 있음 (실제 목적함수급) | 1.01 %p | **40.00 %p** |
| 측도 0 (극단) | 0.00 %p | 24.24 %p |

구현과 반례 회귀 테스트는 `bms-balancing/bms_balancing/verify.py`
(`near_optimal_extrema()` · `mode_profile_extrema()`) 와
`bms-balancing/tests/test_review_findings.py` 에 있다. 이 위키는 지도이고
수치의 정본은 그쪽 산출물이다.

## 한계 — 인용할 때 반드시 같이 옮긴다

1. **여전히 하한이다.** SLSQP 는 국소 해법이고 격자는 유한하다. 산출에
   `is_lower_bound: True` 를 박아 둔 이유다. "정확한 폭" 도 "신뢰구간" 도 아니다.
2. **`tol` 은 통계가 아니다.** 목적함수가 likelihood 가 아니라 RMSE 합이라,
   같은 곡률의 `J(θ) = c + θ²` 도 `c` 가 0.01 / 1 / 100 이면 1 % 띠의 폭이
   0.02 / 0.2 / 2.0 으로 100 배 변한다. 잡음 모델이나 bootstrap 없이는
   **분석자가 고른 민감도 값**이다. 통계적 식별 가능성 쪽 언어는
   [[constrained-crb-identifiability]] 를 보라.
3. **비용.** `bms-balancing/` 데이터에서 4 분 (제약 최적화 + 격자 21 × mode 3).
   격자 규모에 곱하면 커진다.
4. **provenance.** `degradation-degeneracy/` 로 옮긴다면 `hessian.py` 처럼
   validator 밖에 두면 결론 근거로 못 쓴다. 봉인된 fits 에서 재계산 가능하게
   붙여야 한다 ([[provenance-fail-closed-verification]] 의 규율).

## 본체 적용 여부 — 미정 (2026-09-14)

`degradation-degeneracy/src/` 에는 이 계열 도구가 **없다**. 폭에 가장 가까운
것은 `hessian.py` 하나이고 그것은 위에 적은 대로 스스로 강등돼 있다. 옮길지는
아직 정하지 않았다. 옮긴다면 22p 질문
([[22p-physics-or-degeneracy]]: `LAM_PE ≈ LAM_NE ≈ 13 %` 가 물리냐 축퇴냐) 에
**유도량 단위로** 답할 수 있는 형태가 된다 — 지금 본체가 가진 어떤 지표도 그
형태로는 답하지 않는다.

## 관련
- [[fitting-degeneracy]] — 같은 질문의 본체 판본
- [[constrained-crb-identifiability]] — 통계적 식별 가능성 쪽 언어
- [[provenance-fail-closed-verification]] — 옮길 때 지켜야 할 규율
- [[22p-physics-or-degeneracy]] — 이 폭이 답하게 될 질문
