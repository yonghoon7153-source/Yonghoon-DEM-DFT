---
title: Nullspace 관점의 계수 해석 (Schaeffer 2024)
description: "The data leaves a whole subspace of the coefficient vector free; only regularization picks a point in it — so coefficient shape and magnitude are not readable as physics"
created: 2026-09-03
updated: 2026-09-03
type: concept
tags: [battery, degradation, research, methodology]
sources: [raw/papers/schaeffer2024_nullspace-regularization-interpretation.md, raw/papers/lin2024_ocv-degradation-mode-identifiability.md, raw/papers/rhyu2025_systematic-feature-design-formation.md]
confidence: high
explored: false
verificationStatus: unverified
claimType: theoretical
evidenceScope: multi-source-primary
---

# Nullspace 관점의 계수 해석 (Schaeffer 2024)

## 정의

선형 모형 `y = Xβ` 에서 **설계행렬 `X` 의 nullspace**

```
𝒩(X) = { w : X w = 0 }        dim 𝒩(X) = p − rank(X) ≥ p − n
```

에 속한 벡터를 계수에 더해도 예측이 변하지 않는다 (`X(β + w) = Xβ`).
따라서 **데이터는 계수 벡터를 부분공간 하나만큼 결정하지 못하고, 그 안의
어느 점을 고를지는 오직 정칙화가 정한다.**

원전 `[인쇄]`: "The data's nullspace contains all coefficients that satisfy
**𝐗𝐰 = 𝟎**, thus allowing **very different coefficients to yield identical
predictions**."

## ★ 우리 문제로의 사전(辭典) — 이 페이지의 존재 이유

원전은 선형 회귀이고 우리는 비선형(모드 → 곡선)이다. 그러나 다리는 짧다.

| 원전 | 우리 |
|---|---|
| `X ∈ R^{n×p}` 설계행렬 | Jacobian `J(θ) = ∂(모델 곡선)/∂θ ∈ R^{n_점×3}` |
| `XᵀX` | `JᵀJ` = Gauss–Newton Hessian ≈ Fisher = [[np-lip-ocv-reparametrization]] 의 `C_θ⁻¹` |
| `𝒩(X)` (LFP 사례 **959차원**, 전역) | `J` 의 **최소 특이값 방향** (1차원, `θ` 국소) |
| 식 (19) `v_γ = −(γXᵀX + I)⁻¹ β_Δ` | **그대로 쓴다** |
| NRMSE 제약 식 (23) | 우리 목적함수의 허용 증가폭 (잡음 수준에서 유도 가능) |

`[해석]` **핵심 동치**: 선형 최소제곱의 Hessian 은 정확히 `2XᵀX` 이고
`𝒩(X) = 𝒩(XᵀX)` 이며, 등분산 가우시안이면 Fisher 는 `XᵀX/σ²` 다. 즉
**"설계행렬의 nullspace" 와 "Fisher/Hessian 의 영고유공간" 은 이 모형에서 같은
것의 두 이름**이다. 원전은 `Hessian`·`Fisher` 를 **0회** 쓰므로 이 연결을
말하지 않지만, 수학적으로는 동치다.

**차원이 반대이고, 그것이 우리에게 유리하다.** 원전은 `p ≫ n` 이라 nullspace
가 959차원이고 저자 자신이 그 기저를 그려 보다 포기했다 (저장소 노트북 주석
`[인쇄]`: "It's **difficult to interpret when visualized this way** … orthogonal
unit vectors which can be difficult to visualize (and interpret)"). 우리는
미지수가 3~4개이므로 **null 방향이 1차원이고 유일하게 결정되며 그릴 수 있다.**

## 두 부류의 정칙화 — 어느 점을 고르는가

| 부류 | 방법 | nullspace 성분 | 근거 |
|---|---|---|---|
| **직교** | RR · PCR · PLS · 최소노름해 | 정확히 `0` | 원전 SI §S2 증명 3건 |
| **비직교** | lasso · Elastic Net · **fused lasso** | 일반적으로 `≠ 0` | `[인쇄]` "not orthogonal to 𝒩(𝐗) **because of the L1-norm**" |

`[해석]` RR/PCR/PLS 를 쓰는 순간 "null 성분 = 0" 이라는 답이 데이터가 아니라
**L2 노름의 편의**로 미리 정해진다. 그 0 은 물리적 선택이 아니다.

## ★ 금지되는 독법 세 가지 (원전이 인쇄한 것)

1. **모양을 물리로 읽지 말라** — `[인쇄]` 계수를 "in terms of shape (e.g.,
   peaks, plateaus, slopes)" 로 기대와 대조하는 것은 "often done implicitly by
   engineers" 이지만 "**such an interpretation can lead to misleading
   conclusions**".
2. **크기를 중요도로 읽지 말라** (그림판 반례) — 원전 Fig. 4a: 참계수가 전
   구간 **상수 0.001** 인데 PLS 계수는 `[도표]` **3.2 V 위에서 ≈ 0 으로 붕괴**
   한다. nullspace 보정하면 `[도표]` **≈ 0.0009 로 되돌아온다.** 즉 "계수가
   작다 ⇒ 그 구간은 중요하지 않다" 가 **직접 반증**된다.
3. **학습 오차가 낮은 계수가 참에 가깝다고 읽지 말라** — 같은 그림의 범례
   `[도표]`: PLS 0.108 % < PLS+v_γ 0.118 % < **참계수 β\* 0.127 %**.
   참계수가 **가장 나쁘다.**

그리고 원전이 **금지하지 않는** 것도 적는다: "해석하지 말라" 가 아니다.
처방은 `[인쇄]` "regularization and z-scoring are design choices that, **if
chosen corresponding to prior physical knowledge**, lead to interpretable
regression results" 이고, 그 사전지식이 맞는지는 데이터로 확인 불가라고
스스로 못 박는다 — `[인쇄]` "**From the data alone, it is not possible to state
whether 𝐲 was constructed from constant or parabolic coefficients.**"

`[해석]` 즉 **"넣은 사전지식만큼만 나온다" 는 항등식**이며, 이것은
[[fitting-degeneracy]] 의 flat valley 위에서 fitting 이 내놓는 값이
암묵적 정칙화(초기값·경계·optimizer 경로)의 산물이라는 우리 진술의 선형판이다.

## 우리가 그대로 쓸 도구 (파일·함수)

저자 공개 저장소 `HDRegAnalytics` (AGPL-3.0; 읽기 전용으로 참조, 이 저장소에
복사하지 않는다):

- `src/nullspace.py:390 nullspace_calc` — 식 (19) 구현. 핵심 한 줄이 `:429`
  `v_[i,:] = -linalg.inv(g*self.XtX + I_) @ self.w`. **`XtX → JᵀJ`,
  `w → θ_A − θ_B` 로 바꾸면 끝.** `XXᵀ` 역행렬이 필요 없어 조건수를 우회한다.
- `src/plotting_utils.py:298 plot_nullspace_analysis` — 세 곡선(`β_A` /
  `β_A + v_γ` / `β_B`)을 겹쳐 그리고 NRMSE 를 범례에 박는 그림. 원전
  Fig. 1b·2·4·5 의 생성기.
- `src/nullspace.py:199 objective_function_trajectory` — `γ` 를 로그 스윕해
  **ΔNRMSE 와 ‖Xv‖ 를 로그-로그 이중축**으로 그린다. `[해석]` **flat valley
  의 폭을 재는 곡선**이며 원전 본문에는 실리지 않았다 (코드에만 있다).
- `src/utils.py:517/523` — 정확 사영자와 기저 기반 사영자. 노트북 주석
  `[인쇄]` "The scipy implementation is better".
- `src/hd_data.py:144 analyze_snr_by_splines` — 스플라인 잔차로 **좌표별 SNR**.
  "우리 곡선의 어느 전압 구간이 정보를 싣는가" 에 그대로 쓴다.

**주의 (`[재현]`)**: 원전 식 (14) 는 `XXᵀ` 가역을 전제하는데, 논문 자신의
전처리(열 평균중심)가 그 전제를 깬다 — 평균중심 후 `cond(XXᵀ) ≈ 2.1e17`.
식 (14) 가 아니라 **식 (19) 가 실용 도구**다.

## 우리 쪽 재현 수치 (`[재현]`, 인용 금지 등급)

원전 공개 데이터로 직접 계산 (정본은 원전 저장소이며 이 값들은 원문에 인쇄돼
있지 않다): fused lasso 계수 노름의 **36.5 %** 가 `𝒩(X)` 안에 있고, 그 성분을
지워도 학습 예측 차이는 **1.3e−15**(기계 정밀도)다. 점별로는 계수가 **2.09**
만큼 움직여도 예측이 변하지 않는다 (그 지점 최대 계수 3.18 — 크기의 2/3).
그 자유도는 **3.0–3.3 V 에 집중**되는데, 원전이 상전이 물리로 가장 조밀하게
해석한 구간이 바로 거기다. 상세는 raw digest §12.

## 이 위키에서의 적용

- **[[fitting-degeneracy]]** — flat valley 를 **그리는** 절차를 공급한다
  (그 페이지의 "축퇴 방향을 그리는 법" 절).
- **[[np-lip-ocv-reparametrization]]** — 그릴 **대상**(닫힌 형태 null 방향)을
  준 문헌. 두 페이지가 짝이다: 하나는 무엇을 그릴지, 하나는 어떻게 그릴지.
- **[[22p-physics-or-degeneracy]]** — "축퇴 방향 위의 값은 데이터가 아니라
  추정기가 정한다" 는 일반 명제가 Evidence For 에 붙는다.
- **[[pvs-sev-lli-lampe-separability]]** — 낮은 permutation importance 를
  "정보 없음" 으로 읽던 논거에 제동을 건다 (금지되는 독법 2번).
- **[[fused-lasso-feature-design-framework]]** — 그 논문의 참고문헌 `[13]` 이
  이 논문이다. 그쪽은 "β 가 해석을 준다" 는 **긍정 근거로만** 인용한다.

## 한계 (이 개념을 과대 적용하지 않기 위해)

- 원전은 **전부 선형 정적 모형**이다. 비선형 확장은 우리가 놓는 다리이며
  `𝒩(J)` 는 **국소**다 ([[np-lip-ocv-reparametrization]] 의 Lin 이 자기 감도에
  붙인 것과 같은 한계).
- 원전은 **LLI/LAM/half-cell 을 0회** 쓴다. 열화 모드를 재지 않으므로
  이 개념은 **증거가 아니라 도구**로만 인용한다.
- `γ` 선택이 휴리스틱이고 원전은 일부를 손으로 골랐다 (`[인쇄]` "We
  **hand-selected** γ = 10"). 결론의 진폭이 그 선택에 의존한다.
- 원전 자신이 §4.2.2 에서 **참계수를 모르는 실측 응답**의 계수 봉우리에
  물리(철 반사이트 결함 0.55 eV)를 붙인다 — 자기 경고와 긴장 관계다.

## 관련
- [[fitting-degeneracy]]
- [[np-lip-ocv-reparametrization]]
- [[22p-physics-or-degeneracy]]
- [[pvs-sev-lli-lampe-separability]]
- [[fused-lasso-feature-design-framework]]
