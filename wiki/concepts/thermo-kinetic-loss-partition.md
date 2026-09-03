---
title: 열역학·동역학 손실 분해 (ΔE / η) — 전류를 관측 축으로 쓰는 분해
created: 2026-09-03
updated: 2026-09-03
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/tao2025_nondestructive-degradation-decoupling.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: single-source
---

# 열역학·동역학 손실 분해 (ΔE / η)

## 정의

전압 손실을 **인가 전류에 의존하지 않는 성분**과 **전류가 만드는 성분**으로
가르는 분해다. Tao et al. 2025 (`raw/papers/tao2025_nondestructive-degradation-decoupling.md`,
*Energy Environ. Sci.* 18, 1544) 의 식 (1)(2):

```
|U_actual − U_theoretical(*)| = ΔE(SOC, SOH, T) + η(I, SOC, SOH, T)
η = η_act + η_ohm + η_con
```

- **ΔE (열역학 손실)** — `[인쇄]` "attributed to the intrinsic material change
  due to aging". 전류가 0 일 때 남는 오프셋.
- **η (동역학 손실)** — 전류가 만드는 분극. 활성화·옴·농도 세 성분.

**작동 방식**: 전류를 바꾸면 두 성분의 비중이 바뀐다. 따라서 **다단 충전에서
저전류 단과 고전류 단을 비교**하면 두 성분을 (근사적으로) 나눌 수 있다.
Tao 2025 의 구현은 9단 충전에서 **0.33C 인 두 단(Q1, Q9)을 열역학 대표**,
**1.4–3C 인 일곱 단(Q2–Q8)을 동역학 대표**로 배정하는 것이다.

## 우리 축(LLI / LAM_PE / LAM_NE)과의 관계 ★

**같은 것이 아니다. 직교하지도, 포함하지도 않는다 — 한쪽이 다른 쪽을 삼킨다.**

| | ΔE / η 분해 | [[fitting-degeneracy]] 가 다루는 모드 분해 |
|---|---|---|
| 미지수 | 2 (ΔE, η) | 3 (LLI, LAM_PE, LAM_NE) |
| LLI 의 자리 | **ΔE 안** | 독립 미지수 |
| LAM_PE / LAM_NE | **둘 다 ΔE 안** | 각각 독립 미지수 |
| 임피던스 증가 | η (독립) | 목적함수 밖 |
| 가르는 수단 | 인가 **전류 크기** | 곡선 **형상** 적합 |

Tao 2025 자신의 Fig. 5b 가 이 관계를 그림으로 인쇄한다 — LAM 과 LLI 두 상자가
화살표 하나로 합쳐져 "Thermodynamics ΔE" 로 가고, 그 옆에 굵은 글씨로
`[인쇄]` **"Hard to decouple"** 이 붙어 있다. SI Fig. 25 캡션이 같은 말을 글로
적는다: "Thermodynamic loss can be related to loss of active material (LAM),
such as **LAM at the cathode, LAM at the anode, and loss of lithium inventory
(LLI)**."

**따라서 우리 프로젝트의 degeneracy 문제는 이 분해의 "열역학" 한 칸 안에
통째로 들어 있다.** 이 축으로 아무리 잘 분해해도 LLI ↔ LAM_PE 방향은 건드리지
않는다. 반대로 이 축은 우리가 지금 쓰지 않는 정보(임피던스)를 분리해 준다.

## 왜 중요한가 — 관측 채널로서의 가능성

[[pvs-sev-lli-lampe-separability]] 의 질문은 "관측을 늘리면 갈리는가" 다.
지금까지 후보는 (a) ICA/DVA 기하량(PVS), (b) 임피던스 유래량(SEV), (c) Birkl
식 제약 추가였다. 이 개념은 **네 번째 후보**를 준다:

> **같은 셀을 서로 다른 전류에서 관측하면 채널이 하나 늘어난다.**

우리 파이프라인은 현재 준평형 곡선 하나만 쓴다. 전류를 바꿔 얻는 두 번째 곡선이
LLI–LAM_PE 방향에 새 정보를 주는지는 **합성 truth 에서 값싸게 판정할 수 있다**
(모드를 고정한 채 두 전류에서 곡선을 뽑고 2×3 Jacobian 의 특이값을 본다).

**주의**: Tao 2025 는 이 채널로 "열역학 대 동역학" 만 갈랐지 "열역학 안" 을 가른
적이 없다. 따라서 위 판정은 **이 논문의 결과가 아니라 우리가 새로 물어야 할
질문**이다.

## 이 분해를 쓸 때의 함정 (Tao 2025 에서 실측된 것)

1. **ΔE 는 I = 0 에서 정의되는데 측정은 0.33C 에서 한다.** 0.33C 에도 분극이
   있으므로 "열역학 대표" 는 근사다. 논문은 이 간극을 다루지 않는다.
2. **`U_theoretical(*)`(이론 OCV)를 얻는 절차가 논문에 없다.** 식 (1)은 정의로만
   쓰이고, ΔE·η 가 **수치로 산출되는 곳이 논문 전체에 없다.** 실제로 쓰이는 것은
   통계 feature 52개이며, 식 (1)은 그것들을 두 상자에 담는 근거로만 기능한다.
3. **"열역학 79 %" 같은 수치는 손실의 크기가 아니라 feature 중요도 점유율이다.**
   Tao 2025 의 79 % = `Σ|SAGE(Q1,Q9)| / Σ|SAGE(Q1..Q9)|`, 검증 기준으로 제시된
   85 % = 같은 9개 feature 의 800 사이클간 변화량 비. **같은 아홉 숫자에서 나온
   두 요약**이므로 서로에 대한 독립 검증이 아니다.
4. **중요도가 음수인 feature 를 절댓값으로 집계한다.** Tao 2025 Fig. 4h 에서
   RL 계열 SAGE 가 여러 단에서 음수인데 (손실을 키운다는 뜻), 배분식은 절댓값을
   쓴다.

## 관련
- [[fitting-degeneracy]] — 이 분해가 **닿지 않는** 축. ΔE 한 칸 안의 문제다.
- [[pvs-sev-lli-lampe-separability]] — "관측을 늘리면 갈리는가" 의 네 번째 후보로
  전류 축이 추가된다.
- [[dubarry-mechanistic-mode-synthesis]] · [[birkl-ocv-degradation-diagnostic]] —
  LLI/LAM 좌표계 쪽 계보. 이 개념과 미지수 정의가 다르다.
- [[interpretable-ml-battery-prognosis-taxonomy]] — physics-inspired feature
  분류에서 Tao 2025 가 앉는 자리 (손실항이 아니라 feature·구조·사후해석).
