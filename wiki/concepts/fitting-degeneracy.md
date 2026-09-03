---
title: Fitting Degeneracy (LLI/LAM 분리가능성)
description: "full-cell 곡선 하나로 LLI·LAM_PE·LAM_NE 를 가를 수 있는가 — flat valley(데이터 한계)와 multimodal(최적화 난이도)의 구분"
created: 2026-08-11
updated: 2026-09-03
type: concept
tags: [battery, degradation, research]
sources: [raw/repositories/degradation-degeneracy-audit.md, raw/papers/lin2024_ocv-degradation-mode-identifiability.md, raw/papers/schaeffer2024_nullspace-regularization-interpretation.md]
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

## ★ 닫힌 형태로 알려진 null 방향 하나 (2026-09-03 추가)

지금까지 이 페이지의 flat valley 는 **수치로 발견되는 것**이었다. 그런데
[[np-lip-ocv-reparametrization]] (Lin & Khoo 2024, *J. Power Sources* 605,
234446) 이 그중 한 방향을 **해석적으로** 인쇄한다.

SOC 로 정규화한 full-cell OCV 곡선의 **형상**은 두 비(比)에만 의존한다
(`[인쇄]` "the shape of an OCV curve … is **only governed by two degrees of
freedom**"). 그 두 비는 세 모드의 **1 마이너스 값의 비**로만 결정되므로
(원전 식 16):

```
(1−LLI, 1−LAM_NE, 1−LAM_PE) → c·(1−LLI, 1−LAM_NE, 1−LAM_PE)   ⟹ 곡선 형상 불변
특히 pristine 에서:  LLI = LAM_PE = LAM_NE = x  ⟹ 곡선이 pristine 과 완전히 동일
```

즉 **세 모드가 같은 비율로 진행하면 SOC 정규화 곡선에는 아무 흔적도 남지 않고,
총용량만 `1−x` 배가 된다.** 이 방향은 노이즈·최적화와 무관한 모델 자체의 성질이라
국소가 아니라 **구조적**이며, 격자에 truth 쌍으로 **직접 심어 시험할 수 있다**
(수치로 찾은 방향과 검증력이 다르다). 원전 자신은 이것을 축퇴라고 부르지 않고
표기법상의 `[인쇄]` "redundancy" 라고 부른다.

**주의 — 완전한 축퇴는 아니다**: 총용량은 이 방향을 따라 변하므로
**형상 2 + 측정 총용량 1 = 3** 으로 원리적 복원은 가능하다. 남는 문제는
유일성이 아니라 **조건수**이고, 원전 Fig. 9 가 그 조건수가 대부분의 SOC 창과
대부분의 regime 에서 매우 나쁘다는 것을 CRLB 로 보여 준다.

## ★ 그 방향을 **그리는** 법 (2026-09-03 추가)

위 절이 "무엇을 그릴지" 를 주었다면, [[nullspace-coefficient-interpretation]]
(Schaeffer et al. 2024, *Comput. Chem. Eng.* 180, 108471) 이 **어떻게 그릴지**를
준다. 두 문헌은 짝이고, 서로를 인용하지 않는다 (어휘가 달라서 —
Lin 은 `nullspace` 0회, Schaeffer 는 `identifiability` 0회).

**동치 관계** (`[해석]`, 재료는 `[인쇄]`): 선형 최소제곱의 Hessian 은 정확히
`2XᵀX` 이고 `𝒩(X) = 𝒩(XᵀX)` 이며, 등분산 가우시안이면 Fisher 는 `XᵀX/σ²` 다.
즉 **Schaeffer 의 `𝒩(X)` 와 Lin 의 `C_θ⁻¹` 의 영/최소 고유공간은 같은 대상**
이다. 우리 비선형 문제에서는 `X` 자리에 **Jacobian `J(θ)`** 가 들어간다.

**절차 (미실행, 값이 싸다)** — 원전 식 (19)·(23) 을 그대로 옮긴 것:

```
1. 동작점 θ₀ 에서 J = ∂(모델 곡선)/∂θ 를 수치 미분으로 구한다
2. JᵀJ 를 고유분해 → 최소 고유벡터 u_min 과 고유값 스펙트럼
   ⟹ 예측: u_min 이 위 절의 (1−LLI, 1−LAM_NE, 1−LAM_PE) 방향과 정렬해야 한다
      (해석해의 수치 검증. 이 위키가 그 방향을 인쇄만 하고 확인한 적이 없다)
3. θ₀ ± t·u_min 을 따라 곡선을 그려 겹쳐 보인다 (원전 Fig. 1b 의 우리 판)
   대조군으로 θ₀ ± t·u_max 도 함께 그린다
4. t 를 로그로 쓸며 목적함수 증가량을 그린다 → flat valley 의 폭을 물리 단위로
5. 원전 식 (23) 의 허용 손실 c 를 우리 잡음 수준에서 잡으면
   "측정 잡음 안에서 구별 불가능한 열화 조합의 집합" 이 직접 나온다
```

**왜 정확 사영(원전 식 14)이 아니라 완화판(식 19)인가**: 원전은 `p ≫ n` 이라
`𝒩(X)` 가 **정확히** 959차원인 반면, 우리는 미지수 3~4개에 관측이 곡선 전체라
`𝒩(J)` 가 일반적으로 `{0}` 이다. 즉 **우리 축퇴는 정확 null 이 아니라 근사
null(작은 특이값)** 이고, 식 (19) `v_γ = −(γ JᵀJ + I)⁻¹ θ_Δ` 는 `JᵀJ` 가
정칙이어도 정의되며 특이값 크기에 따라 "데이터가 말이 없는 방향" 을 연속적으로
골라낸다. 덤으로 `XXᵀ` 역행렬을 피한다 (`[재현]` 원전 데이터에서 열 평균중심 후
`cond(XXᵀ) ≈ 2.1e17` — 원전 식 (14) 의 전제가 원전 자신의 전처리로 깨진다).

**★ 이 그림이 이 계보에 없다는 것도 확인됐다.** Schaeffer 저장소 노트북에
`scipy.linalg.null_space` 로 기저를 그려 본 셀이 있고, 바로 아래 저자 주석이
`[인쇄]` "It's **difficult to interpret when visualized this way** … orthogonal
unit vectors which can be difficult to visualize (and interpret)" 다. 실패
원인은 **차원(959)** 이지 발상이 아니다 — 우리 null 방향은 1차원이므로 그
장애가 없다.

## 판정 방법 (요약)
정답을 아는 합성 격자에서 복원 오차 |err| 와 tol(2%p) 기반 degenerate 판정,
clean 바이어스 보정, 복원가능군 한정 집계. PE·NE 가 같은 부호로 묶이는
flat 방향의 비율이 "LAM_PE ≈ LAM_NE 는 수학" 가설의 직접 증거 후보.

## 인접하지만 다른 분해 (혼동 주의)
- [[thermo-kinetic-loss-partition]] — 전압 손실을 **열역학 ΔE / 동역학 η** 로
  가르는 분해 (Tao 2025). 이름이 "degradation pattern decoupling" 이라 이 카드와
  같은 문제처럼 읽히지만 **미지수 정의가 다르다**: LLI·LAM_PE·LAM_NE 가 **전부
  ΔE 한 칸 안**에 들어간다. 즉 그 분해가 완벽해도 이 페이지의 질문은 그대로
  남는다. 원전 자신이 그 셋을 가르는 것을 "Hard to decouple" 이라고 인쇄한다.

## 한계
- 판정은 tol 임계와 guard-feasible 모집단에 조건부다.
- 위 "그리는 법" 은 **국소**다 (`J` 는 `θ₀` 에서만 정의된다). 멀리 떨어진 두
  해가 같은 곡선을 내는 **전역** 축퇴는 여전히 격자 스캔이 있어야 한다.
- 수치는 위키에 복사하지 않는다 — 정본은 artifact 와
  `degradation-degeneracy/docs/RESULTS*.md` ([[provenance-fail-closed-verification]]).
