---
title: 제약 Cramér–Rao 하한으로 재는 식별 가능성
created: 2026-09-04
updated: 2026-09-04
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/mohtat2019_electrode-soh-estimability-expansion.md, raw/papers/lin2024_ocv-degradation-mode-identifiability.md, raw/papers/lee2020_estimation-error-bound-limited-data-window.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: theoretical
evidenceScope: multi-source-primary
---

# 제약 Cramér–Rao 하한으로 재는 식별 가능성

## 정의

파라미터 벡터 `θ` 를 관측 `Ŷ = Y(θ) + ε` 에서 추정할 때, **등식 제약
`f(θ*) = 0` 이 걸린 상태의** 추정 오차 하한. Mohtat et al. 2019 (§5.2, 식
28–34) 가 Stoica & Ng 1998 을 따라 이 문제에 도입한 형태:

```
𝓘_f = Sᵀ E⁻¹ S                       (Fisher 정보행렬, S = ∂Y/∂θ|_θ*)
(∂f/∂θ)|_θ*  𝒪 = 0                   (𝒪 = 제약 gradient 의 nullspace 정규직교기저)
Σ  ≥  𝒪 (𝒪ᵀ 𝓘_f 𝒪)⁻¹ 𝒪ᵀ              (제약 CRB)
σ_θ = sqrt(diag[Σ]) ,  Error(%) = σ_θi/θi × 100
```

**판정 규칙 두 층**:
1. **이분법 (구조)** — `[인쇄, Mohtat p.7]` "If 𝒪ᵀ 𝓘_f 𝒪 is nonsingular, then
   the constrained problem is **identifiable**." 특이하면 식별 불가.
2. **정도 (연속)** — `σ_θ` 의 크기. Mohtat 은 여기에 임의의 판정선(5 %)을 긋는다.

**제약이 하는 일**: 자유도를 `dim θ − rank(∂f/∂θ)` 로 줄이면서, 남은
부분공간 안에서만 Fisher 를 본다. 제약이 없을 때보다 `Σ` 는 **작아진다**
(정보가 늘어난 것이 아니라 모르는 방향이 줄어든 것).

## 왜 중요한가

이 위키의 반쪽전지 창 매개화 계보([[np-lip-ocv-reparametrization]],
`comparisons/halfcell-window-parametrization-lineage.md`)는 **컷오프 전압
등식으로 여분 자유도를 죽이는** 처방을 반복해서 만난다. 그 처방을 쓰면
"제약 하에서 무엇을 얼마나 잴 수 있나" 가 곧바로 문제가 되는데, 제약 CRB 가
그 질문의 표준 기계다. 우리 `mode-observability` Phase 1e/1h 는 제약
gradient 를 특이벡터와 각도로 대조했는데, **그것은 이 기계의 한 단면**이다 —
`𝒪` 로 사영해 다시 쓰면 같은 계보의 언어가 된다.

**★ 그리고 이 계보 전체가 공유하는 습관이 하나 있다: `Σ` 를 구한 뒤 즉시
`diag` 만 취한다.**

| 문헌 | `Σ` 를 구하나 | 무엇을 보고하나 | 축퇴 **방향**을 보고하나 |
|---|---|---|---|
| Mohtat 2019 | 예 (식 32) | `sqrt(diag Σ)` 4개 (Fig. 8) | **아니오** (파라미터 `correlat*` 0회) |
| Lin & Khoo 2024 | 예 (`C_θ`) | `sqrt(diag C_θ)` (Fig. 8·9) | **아니오** |
| **Lee et al. 2020** | 예 (식 16·24, 스스로 "the error **covariance** matrix" 라 부름) | 헤드라인은 `sqrt(diag Σ')` (Table II–IV, Fig. 4·5·6·9) | **그림으로만 예** — Fig. 7 이 6개 쌍 전부에 **95 % 오차 타원**(제약 유/무)을 그린다. 단 **수치 ρ 0회**, 창은 DW-deep **하나뿐**, 모드 좌표 전파 없음 |

`[해석]` **2026-09-04 정정**: "이 계보는 `Σ` 를 구해 놓고 대각선만 인쇄한다"
는 일반화는 Lee 2020 앞에서 예외를 하나 인정해야 한다. 정확한 진술은
**"비대각을 그림으로 한 번 보였으나 수치로 인쇄한 적이 없고, 모드 좌표로
전파한 적이 없다"** 이다. Lee 2020 은 산문으로도 상관을 말한다
(`[인쇄, p.8]` "a **strong correlation** … among the parameters from the same
electrode … the parameters from the different electrodes do not show any
correlation") — 그런데 자기 Fig. 7 의 `(e_Cp, e_x₁₀₀)` 패널(다른 전극 쌍)은
타원이 기울어 있다(`[도표]`, 부호 −). **본문이 그림보다 강하게 말한 자리**다.

그리고 Lee 2020 은 이 계보에서 **비대각을 요구하는 사상을 명시적으로
인쇄해 놓고 안 쓴** 첫 사례다: 식 (10) `LLI = 1 − (y^a₁₀₀C^a_p + x^a₁₀₀C^a_n) /
(y^f₁₀₀C^f_p + x^f₁₀₀C^f_n)` 는 네 성분을 섞으므로 **`Σ` 의 비대각 없이는
분산 계산 자체가 불가능**한데, 식 (10)–(12) 는 §III-A 이후 논문에 다시
등장하지 않는다. 즉 축퇴의 **크기는 재고 방향은 버린다**는 진단은
세 편 모두에 대해 여전히 유효하고, 이것이 [[fitting-degeneracy]] 를 다루는
우리 작업이 이 계보에 공급할 수 있는 정확한 빈칸이다.

**제약이 무엇을 못 하는지의 깨끗한 수치** (Lee 2020, `[인쇄, Table II↔III]`,
DW-deep·σ = 10 mV·95 %): `V_max` 등식 하나를 걸면 `y₁₀₀` 2.5 → **0.030 %**
(약 83배), `C_p` 1.3 → 0.9 % 인데 **`x₁₀₀` 3.0 → 3.0, `C_n` 3.9 → 3.9 로
변화가 없다.** 제약은 `y₁₀₀`·`x₁₀₀` 를 묶지만 `β ≪ α`(식 26
`σ_y α = σ_x β`) 이므로 이득이 뾰족한 전극 쪽으로만 흐른다 — **제약은 정보를
만들지 않는다**의 교과서적 사례.

## 두 가지 처방의 구분 (자주 헷갈린다)

`[해석]` "식별 가능성을 개선한다" 는 말 아래에 **성질이 다른 두 조작**이 있다.

| 조작 | 무엇을 바꾸나 | 예 | 우리 실측 |
|---|---|---|---|
| **제약 추가** | `𝒪` 를 좁힌다. 정보는 안 늘고 **모르는 방향이 준다**. 대신 제약이 참값에서 성립해야 하고, 안 성립하면 **모델 오차**가 된다 | 컷오프 전압 등식 (Birkl 2017, Mohtat 2019 식 (P)) | Phase 1e/1h — 우리 자료에서는 **손해**. 등식이 참값에서 127 mV/54 mV 폭으로 깨지고, σ_min 은 3~6 % 오를 뿐 (정본: `mode-observability/results/phase1e/`, `.../phase1h/`) |
| **관측 추가** | `S` 에 **행을 더한다**. 새 행이 기존 행과 선형독립이면 정보가 실제로 는다 | 셀 팽창 `Δt_c` (Mohtat 2019) | **미측정** — 우리가 아직 안 해 본 축 |
| **창 이동** | `S` 의 **행을 갈아 끼운다**. 개수가 같아도 다른 정보 | 데이터 창 `DW = [Q_s, Q_e]` (Lee 2020) | **미측정** — 상세는 [[data-window-identifiability]] |

**관측 추가가 이득이 되는 조건은 기계적으로 검사할 수 있다** (Mohtat 식 39):
새 관측 `g(θ)` 의 감도 열이 **0 이 아니어야** 한다. Mohtat 의 팽창은
`∂Δt_c/∂θ_j ∝ [ΔV'(·_i) − ΔV'(·₁₀₀)]` 이므로, **부피변화가 선형인 전극에
대해서는 그 열이 정확히 0** 이다 (LFP 양극). 그래서 팽창은 graphite 음극
파라미터만 살린다 — 논문의 정성 설명("LFP expands at a constant rate")을
식으로 옮기면 그렇다.

`[해석]` 반대 방향의 사례도 이 위키에 있다: Marongiu 2016 은 **상관된 관측을
더하면 오히려 나빠질 수 있다**는 것을 실측으로 보인다
([[pvs-sev-lli-lampe-separability]] Evidence For). 즉 관측 추가는 자동 이득이
아니고, **새 행의 독립성**이 조건이다.

## 한계 (이 도구가 못 하는 것)

1. **국소적이다.** `S` 를 참값 `θ*` 에서 평가하므로, 멀리 떨어진 두 해가 같은
   곡선을 내는 **전역 축퇴**는 보이지 않는다. Lin & Khoo 는 이 한정을 세 번
   인쇄하고 Bayesian inversion 을 미룬다. **Mohtat 은 그 한정을 인쇄하지 않는다**
   (어휘 전수: `global` 0회).
2. **불편(unbiased) 추정을 전제한다.** 비선형 문제의 최대우도 추정은 일반적으로
   불편이 아니다. Lin 은 이를 인정하고 "semi-heuristic" 이라 부르며 그냥 쓴다;
   Mohtat 은 교과서 정의만 인용하고 자기 문제에서 성립하는지 묻지 않는다.
3. **하한이지 추정 결과가 아니다.** 두 편 모두 **추정기를 노이즈 아래서 돌리지
   않는다.** CRB 가 낮다고 최적화가 그 해를 찾는다는 보장은 없다.
4. **모형 인공물에 민감하다.** 구간선형 OCP 근사는 평탄역을 **완전 평탄**으로
   만들어 rank 결손을 깨끗하게 만든다. Mohtat 자신이 `[인쇄, p.10]` "in
   practice … more non-linearities near the low DODs which results in
   **better-conditioned** sensitivity matrices" 라고 적는다.

## 이 위키에서의 적용

- **채택**: 제약 gradient 의 nullspace 사영(`𝒪`)은 우리 Phase 1e 의 각도
  대조와 같은 대상을 다른 좌표에서 본 것이다. 두 표기를 대사표로 붙여 두면
  이 계보와 직접 비교가 된다.
- **점검 (미실행)**: `Σ` 를 LLI/LAM 사상(Mohtat 식 16·20)으로 전파한
  `σ(LLI)`·`σ(LAM_pe)`·`σ(LAM_ne)`. **`LLI` 는 비대각 성분을 요구**하므로 이
  계산 하나가 "대각선만 보고하는 관습" 을 정면으로 깬다.
- **주의**: 우리 연구 수치의 정본은 artifact + `degradation-degeneracy/docs/`
  이며, 이 페이지의 수치 언급은 참조다.

## 관련
- [[fitting-degeneracy]] — 이 도구가 재려는 대상(축퇴)의 개념 페이지
- [[np-lip-ocv-reparametrization]] — 제약을 **애초에 안 만드는** 반대 처방
- [[pvs-sev-lli-lampe-separability]] — "관측을 더하면 갈리는가" 를 추적하는 열린 질문
- [[birkl-ocv-degradation-diagnostic]] — 컷오프 등식 처방의 앞선 사례
- [[dubarry-mechanistic-mode-synthesis]] — Mohtat 의 LLI/LAM 어휘 출처
- [[data-window-identifiability]] — 같은 기계를 **관측 창** 축에서 돌린 자매편(Lee 2020)
