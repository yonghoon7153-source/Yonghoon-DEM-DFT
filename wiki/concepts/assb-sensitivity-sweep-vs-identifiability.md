---
title: "ASSB 모델 논문의 '민감도 분석' — OAT 스윕은 야코비안의 열이고, 겹쳐 보면 비식별 방향이 보인다"
description: "In the ASSB modelling literature 'sensitivity analysis' means one-at-a-time parameter sweeps of a forward model against design KPIs, not identifiability analysis; when a paper prints both a parameter fit and such sweeps, overlaying the sweep figures exposes parallel or null Jacobian columns, and the first such paper shows a fitted parameter that drifted ten orders of magnitude along a direction its own sweep had found flat"
created: 2026-09-23
updated: 2026-10-03
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/ansah2021_assb-fem-parametric-sweep-thickness-diffusivity.md, raw/papers/shao2022_thin-film-assb-mechano-electrochemical-stress-partial-molar-volume.md, raw/papers/xie2008_lco-thin-film-orientation-diffusion-gitt-pitt-eis.md, raw/papers/danilov2008_liquid-electrolyte-transport-electroneutrality-dissociation.md, raw/papers/deng2021_assb-reduced-order-model-pade-polynomial.md, raw/papers/kim2019_assb-ekf-soc-estimation-weak-observability.md, raw/papers/raijmakers2020_thin-film-assb-model-double-layer-dc-ac-joint-fit.md, raw/papers/lu2022_nondestructive-eis-lumped-dfne-parameter-estimation.md, raw/papers/khalik2021_dfn-grouping-sensitivity-parameter-estimation.md, raw/papers/bielefeld2023_useful-models-ssb-simplicity-perspective.md, raw/papers/firouz2020_hammerstein-wiener-multisine-bla-nonlinearity-assb.md, raw/papers/danilov2011_thin-film-assb-model-weak-electrolyte-parameter-fit.md, raw/papers/kim2023_argyrodite-coated-ncm-normal-pressure-assb.md, raw/papers/wang2024_fast-kinetics-hierarchical-catholyte-anode-design-ssb.md, raw/papers/jiao2023_electro-chemo-mechanical-se-modulus-conductivity-intergranular-czm.md, raw/papers/schlautmann2023_lpscl-particle-size-distribution-composite-transport.md, raw/papers/shi2020_particle-size-ratio-cathode-utilization-assb.md, raw/papers/davis2021_operando-microscopy-graphite-lpscl-composite-current-focusing.md, raw/papers/naik2022_kinetics-vs-transport-ssb-cathode-mesoscale-regime-map.md, raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode-si.md, raw/papers/asheri2023_data-driven-multiscale-ssb-delamination-surrogate.md, raw/papers/neumann2021_garnet-3d-structure-grain-boundary-transport.md, raw/papers/ren2023_oxide-ssb-composite-cathode-architecture-perspective.md, raw/papers/barai2018_measurement-timescale-internal-resistance-methods.md, raw/papers/li2024_assb-composite-cathode-model-contact-area-edl.md, raw/papers/thelen2024_probabilistic-ml-battery-health-review.md, raw/papers/roman2021_ml-pipeline-soh-estimation-uncertainty.md, raw/papers/liang2026_pulse-excitation-active-bms-comment.md, raw/papers/chien2023_ici-rapid-solid-state-diffusion-coefficient.md, raw/papers/park2024_asymmetric-kinetics-low-mass-loading-nmc111-latp-li-metal.md, raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode.md, raw/papers/bizeray2019_spm-identifiability-parameter-estimation.md, raw/papers/iwakiri2024_new-ssb-model-parameter-estimation-sensitivity.md, raw/papers/sinzig2024_p2d-validity-ssb-global-sensitivity.md, raw/papers/zhou2025_tailored-cathode-microstructure-low-pressure-assb.md, raw/papers/stavola2023_lithiation-gradients-tortuosity-thick-nmc111-argyrodite.md, raw/papers/vadhva2021_eis-for-assb-theory-methods.md]
confidence: low
explored: false
verificationStatus: unverified
claimType: interpretive
evidenceScope: multi-source-primary
---

# ASSB 모델 논문의 "민감도 분석" — 스윕 ≠ 식별성

> `assb` 축의 개념 페이지. 닻은 [[assb-contact-loss-vs-lampe]] 의 **Q4(유일성·식별성)**.
> 이론 쪽 정의는 [[constrained-crb-identifiability]] · [[fitting-degeneracy]] 에 있고, 이 페이지는 **ASSB 문헌에서 그 낱말이 실제로 무엇을 가리키는가**와
> **그 그림들을 공짜로 식별성 검사에 쓰는 법**을 다룬다. 수치의 정본은 원문 PDF 이고 여기 값은 **사본**이다.

## 정의 — 세 가지 "민감도"를 가른다

| 이름 | 무엇을 흔드나 | 출력 | 식별성을 말하나 |
|---|---|---|---|
| **설계 민감도** (design) | 물질 파라미터 한 개를 대역 배수(×0.1–×500)로 | 방전곡선 · KPI(용량 이용률 · 전압 효율) | **아니다** — "무엇을 올리면 좋아지나" |
| **추정 민감도** (estimation) | 적합점 근방에서 파라미터를 국소로 | **추정 데이터 위의** 잔차/출력의 야코비안 `J` | 절반 — `J` 의 열이 평행하거나 0 이면 비식별 **후보** |
| **식별성** | `J^T J`(FIM) · 조건수 · 프로파일 가능도 · 근최적 폭 | 추정 불확실성 · 조합의 null 방향 | **예** |
| ↳ 첫 줄의 **전역판** (27호) | 사전 상자 전체에서 입력 여럿을 동시에 (Sobol 1·2·전차 + CI, 대리모형) | 설계 KPI 의 분산 분해 | **아니다** — 대상이 데이터가 아니다. 단 전차 지수 ≈0 은 그 출력에 대한 비식별의 **충분조건** |
| **모델 불일치 민감도** (27호, 새 줄) | 두 모델(상위 충실도 ↔ 축약)에 같은 입력 | `d = Y_hi − Y_lo` 의 기울기 `|∇d|` | **아니다** — **모델 적합성**(model adequacy)의 도구. `|∇d| ≈ 0` 은 "차이가 상수라 보정이 흡수한다" 는 뜻 |
| ↳ 셋째 줄의 **입력 설계판** (34호, 새 줄 · ⚠ 처방만) | **입력 `u`**(펄스 진폭 · 폭 · 순서)를, 파라미터는 고정 | `det FIM(u)`(D-optimality) · PE 조건 | **절반** — **실제적** 비식별(FIM 정칙, 조건수 큼)만 줄인다. **구조적** 비식별(모든 `u` 에서 FIM 특이 — 곱 축퇴)에서는 D-optimality = 0. 그리고 FIM 은 국소라 설계 뒤 **전역 폭**을 다시 재야 한다 — 근최적 폭 측정이 사후 검증 |
| **예측 보정** (35호, 새 줄 · 표 밖) | 모델 출력 분포를 **보정 전용 셀**에 맞춰 재보정(isotonic) | 스칼라 예측의 적중률(`C_score` @90 %) · 날카로움 | **아니다** — 대상이 **예측**이지 파라미터가 아니다. 축퇴 방향에서 예측이 변하지 않으면 그 폭은 보정된 구간에 **안 보인다**. 모드 분해가 없는 목표(SOH 스칼라) 위에서만 정의된다 |
| **불확실성 분류** (36호, 새 줄 · 표 밖) | 총 예측 불확실성을 aleatory(비가역) ↔ epistemic(가역: model-form · parameter)으로 **분류**, 구간을 CI ⊂ PI ⊂ TI 로 정의 | 어휘와 정의 — 계산 대상은 예측 분포 · ML 가중치 사후 | **아니다** — 그리고 **자리를 막는다**: epistemic = "reducible" · CI 는 참값으로 붕괴로 정의되므로, 데이터량 불변인 **구조적 비식별**이 들어갈 칸이 없다 |
| **비선형 시스템 식별** (92호, 새 줄 · 표 밖) | **입력의 위상 실현 · 주기**(무작위 위상 다중정현 · M × P) — 진폭 · 상태는 한 점 | 비모수 FRF(BLA) + 선별 잡음 · 확률적 비선형 왜곡 분산 → 전달함수 + 정적 비선형 블록(H · W · H-W) | **아니다** — "identification" = 구조를 고르고 맞추기. BLA 의 "분산" 은 FRF 의 잡음 · 왜곡 분산(매개변수 분산 0). 그리고 블록 지향 구조 자체에 **블록 사이 이득 · 오프셋 교환**(입력으로 못 사는 구조적 비식별)이 있어 정규화 없이는 블록별 모양이 정해지지 않는다 |
| **측정 대체 · 안건형** (93호, 새 줄 · 표 밖 · 처방만) | 흔드는 것 없음 — **적합 단계를 지우고** 입력을 재료(조합)에서 따로 잰다(Berro 4단계 "Identify model parameters that fit the data" → "Measure reliable model input parameters") · 남은 "민감도" 는 입력 정확도 · 정밀도에 대한 국소 강건성(5단계 — 첫 줄 설계 스윕) · 못 재면 "결과에 영향 없을 정교한 추측" | forward 예측 + 정성 검증 | **아니다 — 옮긴다**: 비유일성이 측정 역모형(EIS `R_CT` → `j₀` 는 면적 `A` · GITT/EIS → `D̃` 는 확산 길이 · 면적 규약)으로 이동하고, 검증 곡선 일치는 입력 가족 사이 비유일성(56호 그림 7)을 가리지 않는다. "결과에 영향 없을 추측" 은 0 열의 실천판 — 둔감은 본 출력 · 본 조건의 성질이다 |
| ↳ 둘째 줄의 **직교화 순위 + 합성 다중 시작판** (95호, 새 줄 · ⚠ 액체 DFN 도구) | **사전 범위로 정규화한 β**(로그 14 · 선형 8)를 한 점에서 유한차분 — 추정 자료 위 감도 행렬 `S` 를 피벗 QR(Lund & Foss)로 직교화해 추정할 매개변수를 고르고 나머지는 β 0.5(범위 가운데) 고정 · 그 위에 합성 셀(범위 안 참값 하나 · 같은 모형 · 무잡음 · 다중 시작 50) | 순위 + `\|r_kk\|` 막대 · 다중 시작 상자 그림(합성은 참값 대비) · 출력 RMSE | **절반** — 평행 열은 순위 뒤로 밀리고 `\|r₁₁\|/\|r_kk\|` 가 **조건수 하한**을 공짜로 준다(`[재현]` 고른 12 개 ≥10^2.98). 그러나 순위는 한 점 · 범위 폭 의존이고 문턱 0 이며, 다중 시작 산포에는 잔차 문턱(`tol`)이 없어 **근최적 폭 ↔ 수렴 실패**가 섞인다 — 무잡음 · 같은 모형에서도 출력 RMSE 중앙값 0.13 mV ≠ 0 · 참값 IQR 밖 14/22 |
| ↳ 셋째 줄의 **선형화(소신호) 손 분석 + 단일 실행 합성판** (96호, 새 줄 · ⚠ 액체 EIS 도구) | 흔드는 것 없음 — **소신호 전달함수(TF) 식의 구조**를 손으로 읽어 비식별 조합을 적고(비 n̄e/ψ̄ · κ̄D/ψ̄ · 직렬 R_c ↔ 1/κ̄^s), 비선형 PDE 판의 구조적 식별성은 다른 편(Ref. 2 학회 판) 인용 · 그 위에 합성 셀(같은 TF 모형 · 참값 하나 · 잡음 0.5 % 실현 하나 · 실행 하나) | 비 · 합으로 줄인 추정 집합(열셋) + 정규화 궤적 그림(추정/참) · 출력 절대 오차 | **절반** — 선형 비식별 조합은 정확히 적는다(`[재현·대수]` 비 구조 ✅). 그러나 "nonlinearly identifiable" 은 인용이고 FIM · 공분산 · 다중 시작 0 · 합성 시험은 잡음 실현 하나 · 실행 하나라 산포가 없다 — 같은 모형에서도 전체 집합 다섯 19–64 % · 펄스 셋 29–66 % · 참값 경계 밖 둘 |
| ↳ **상태 관측성 논증 + 합성 추정기 실행** (99호, 새 줄 · 표 밖) | 흔드는 것 없음 — OCV 평탄(야코비안 ≈0)을 '약한 관측성' 으로 부르고, 같은 모형 계열 합성 플랜트에서 EKF 를 한 번 돌려 SOC 오차를 보인다 · 같은 편의 '민감도 분석'(표 2)은 **모델 불일치 민감도(27호 줄)의 OAT 판**(출력 = 전체 ↔ 축약 모형 전압 차의 Max · RMS) | SOC 오차 시계열(실행 하나) · 축약 오차 표 | **아니다** — 대상이 **상태**(SOC)이지 매개변수가 아니고 관측성 행렬 · Gramian · CRB 0 · 오차의 성격(분산 ↔ 편향)도 가르지 않는다 — 우리 재현으로는 편향(모형 불일치 ÷ OCV 기울기) |

`[해석]` 26호(Iwakiri 2024, `raw/papers/iwakiri2024_new-ssb-model-parameter-estimation-sensitivity.md`)의 제목 "sensitivity analysis" 는 **첫 줄**이다.
그 편의 Table 1(ASSB 모델 10 편 비교)에서 "Sensitivity Analysis" 열의 값이 **Several / Temperature / Current / Diffusion / Conductivity** — **무엇을 스윕했나의 목록**이다.
⇒ 이 문헌에서 "sensitivity analysis" 를 보면 **스윕**으로 읽고, 식별성의 증거로 세지 않는다. (근거 한 편의 표 하나 — `single-source`.)

`[해석]` 34호(Liang et al. 2026, `raw/papers/liang2026_pulse-excitation-active-bms-comment.md`, ⚠ Comment · 데이터 0 · ASSB 0)는 BMS 쪽에서 **입력 설계판**을 처방한다 — `[인쇄]` "FIM or D-optimality … ensures maximum parameter identifiability" · "observability is redefined as a controllable resource". 계산은 0 이고, **구조적 ↔ 실제적 비식별을 가르지 않는다**(`[인쇄]` "CRLB, which is the inverse of the FIM" — 특이 FIM 무언급). ⇒ "입력을 설계해 식별성을 높인다" 는 명제를 보면 **곱 축퇴처럼 모든 입력에서 null 인 방향이 있는지를 먼저** 묻는다. 그 방향은 입력이 아니라 모델 구조(곱과 다르게 반응하는 항)와 그 항의 대역 샘플링이 가른다([[assb-lampe-contact-product-degeneracy]] 열일곱 번째 적용).

## ★★★★ 그래도 스윕 그림은 공짜 야코비안이다 — 겹쳐 본다

대역 스윕 곡선은 국소 미분이 아니지만, **한 파라미터를 흔든 곡선족의 "모양"** 은 그 파라미터의 민감도 방향을 보여 준다. 그래서:

1. **같은 모양의 그림 쌍 = 평행한 열** — 두 파라미터를 데이터가 한 조합으로만 본다(후보).
2. **반응 없는 그림 = 0 열** — 그 파라미터는 그 출력으로 정해지지 않는다(적어도 그 영역에서).
3. **그 파라미터를 적합표에서 찾아 문헌값과의 비를 본다** — 0 열 파라미터의 적합값은 **아무 데나** 갈 수 있다.

### 26호에서 실제로 나온 것

| 겹친 그림 | 모양 | `[재현]` 구조 | 적합표 |
|---|---|---|---|
| Fig. 5a (`D_e⁻` ×0.1–500) | **0 열** — 네 곡선이 확대창에서도 일치 | 식 (30) `D_p = 2D_M⊕D_e⁻/(D_M⊕+D_e⁻)` 가 `D_e⁻ ≫ D_M⊕` 에서 포화 → **하한만 식별** | ★ `D_e⁻` 최적 **5.24×10⁻³** ↔ 문헌 5.06×10⁻¹³ (**10 자릿수**) |
| Fig. 12a ↔ 12b (`k₁` ↔ `k₂`) | **평행** — 두 판 판별 불가 | `α` = 0.5 두 계면 모두 `asinh(i/2i₀)`, `i₀⁻` SOC 무관 → 몸통에서 합만 | 둘 다 ≈×1.05 |
| Fig. 3 ↔ Fig. 15 (`D_M⊕` ↔ `a_max`, 전류 고정) | **동일 곡선족**(끝 `x` 11 개 일치) | `x` 좌표에서 양극 부분계가 `D_M⊕·a_max/I` 한 조합만 본다(`I⁺₀ ∝ a_max` 만 깬다) | 둘 다 ×1.05 |
| Fig. 6 · 8 · 14 · 16 (전해질 셋 · `a_max`@C 고정) + 12 | **평행 이동 일곱 개** | 몸통의 평탄한 과전압 — 율 사이 곡률(옴 ↔ asinh)만 가른다 | 7/10 이 정확히 문헌 ×1.0500 |

★★★★ **첫 줄이 이 페이지의 이유다**: 26호는 `D_e⁻` 가 곡선을 안 움직인다는 것을 **자기 그림으로 보였고**, 그 파라미터를 **10 자릿수 표류한 값으로 보고**했으며,
그 점에서 본 둔감을 **"느린 종이 지배한다" 는 물리**로 결론에 올렸다. `[재현]` 문헌값이었다면 `D_e⁻` ×0.1 은 `D_p` 를 ×0.365 로 떨어뜨려 곡선이 크게 움직였어야 한다 —
**그림은 적합점에서 그려졌고, 그 둔감은 적합점의 성질이다.**

## 왜 중요한가 — Q4 의 0 과 이 페이지의 관계

- 카드의 Q4 는 **"유일성·식별성을 쟀나"** 다. 스윕은 재지 않은 것이다 — **26호 이후에도 Q4 는 0/26**, 전역 Sobol 을 제대로 한 27호 이후에도 **0/27**. → **29호에서 처음 반 칸**(둘째 줄의 수치 진단, 아래 절).
- 그러나 26호는 **추정과 스윕이 같은 모델 · 같은 지면**에 있는 계보 첫 편이라, **원전 수치만으로 비식별을 재현할 수 있었다.** 24호(열일곱 번째 성질)의 재료가
  "측정 ÷ 가정"([[assb-tortuosity-factor-effective-conductivity-split]]), 25호(열여덟 번째)가 "손잡이의 폭" 이었다면 26호의 재료는 **저자 자신의 계산**이다.
- ~~큐 26(P2D 유효성)은 둘째 줄 너머(전역 분산 분해)를 할 것으로 보인다~~ → **2026-09-23 흡수(27호) 결과: 첫 줄의 전역판이었다** — 아래 절. Sobol 지수는 분산 기여이지 조합의 null 방향이 아니라는 예고는 맞았다.
  큐 27(Bizeray 2019, 액체셀 SPM)이 **셋째 줄**의 원전이다. → **2026-09-23 흡수(28호) 결과: 맞다 — 단 액체셀이고, 식별 집합에 용량 스케일이 없다** (아래 절).


## ★★★★ 27호 — 전역으로 제대로 해도 첫 줄이다, 그리고 **적합성 ≠ 식별성**

`raw/papers/sinzig2024_p2d-validity-ssb-global-sensitivity.md` (Sinzig, Schmidt, Wall 2024, *JES* 171, 120519). 3차원 입자 분해 모델(참값으로 **가정**) ↔ 균질화 P2D 를
4 입력(`σ` · `κ` · `D` · 전류) 150 표본 + GP 대리모형으로 비교해 Sobol 1·2·전차 지수를 **95 % CI 와 함께** 낸 편. 출력은 `SOC_end`(방전 끝 양극 SOC) 하나.

| 물음 | 27호 |
|---|---|
| 어느 줄인가 | **첫 줄의 전역판** — 사전 상자 × 설계 KPI, 데이터 · 적합점 0 |
| 새 줄 | `m_SOC = |∇(SOC_res − SOC_P2D)|` — **모델 불일치 민감도** |
| 식별성 재료 | ① `S_T(D │ P2D) ≈ 0` · ② 두 모델이 같은 값을 내는 영역 · ③ `[인쇄]` "a constant difference could still be corrected by an update of the homogenization parameters" |
| 저자가 읽은 틀 | 셋 다 **모델 적합성** — ① "P2D 가 `D` 의 영향을 과소평가" · ② "P2D may be easily used" · ③ 보정 가능 |

**두 질문을 가르는 한 줄**: 적합성은 "**같은 입력**에서 두 모델이 같은 출력을 내나", 식별성은 "**한 모델**에서 데이터가 파라미터를 하나로 정하나" 다.
**만나는 자리는 셋**(`[해석]`): (가) 두 모델의 일치 = 그 출력으로 **모델 구조를 못 가른다**(구조적 비식별) · (나) 보정이 흡수하는 상수 = **보정 파라미터가 구조 오차를 먹는다** · (다) 전차 지수 0 = 비식별의 충분조건.

★★★★ **(나) 의 상수를 벡터 좌표로 재면 접촉 손실이다.** `[재현]` resolved 모델의 비연결 입자(`[인쇄]` `u = 0.93`)는 초기 SOC 에 머물러 `SOC_end` 에 **`1 − u = 0.07` 바닥**을 깐다 —
큰 `κ` 오프셋 0.068 · 150 표본 평균 차 0.072 와 맞는다. 저자는 그 오프셋을 "insufficient homogenization strategy" 로 배정하고, `u` 를 넣는 처방은 `[인쇄]` "reducing the available capacity … by a modification of the specific interface area" 다.
⇒ **보정이 흡수하는 "상수 차이" 는 접촉 손실이 용량 손잡이로 들어가는 자리**다 — 카드 물음([[assb-contact-loss-vs-lampe]])의 모델 대 모델 판.

**Q4 는 0/27.** 데이터가 없고(두 모델의 무잡음 출력), ① 은 단일 파라미터 · 대리모형 · 저자가 적합성으로 읽음, ③ 은 명제이며 그 계산(Fig. 3b "dashed line")이 그림에서 빠졌다.

## ★★★★ 28호 — 셋째 줄의 원전, 그러나 **대상이 액체셀이고 용량은 입력이다**

`raw/papers/bizeray2019_spm-identifiability-parameter-estimation.md` (Bizeray, Kim, Duncan, Howey 2019, *IEEE TCST* 27(5), 1862). 묶음 표 전체는 [[spm-grouped-parameter-identifiability]].

| 물음 | 28호 |
|---|---|
| 어느 줄인가 | **셋째 줄 — 계보 첫 편.** 구조적 식별성(전달함수 유일성, Bellman–Åström 정의) + 실제적 식별성(합성·실험 EIS 의 손실 등고선) |
| 정량 도구 | **0** — FIM · CI · 프로파일 · 조건수 없음. 등고선 **그림**을 읽는다(= 2 차원 근최적 집합의 그림) |
| 식별 집합 | `θ̃ = (τ_d⁺, τ_d⁻, R_ct)` — **전극 용량 `Q_th` 와 초기 화학량론 `x⁰` 은 입력**(`β = dU/dQ` 를 기준극으로 잰다) |
| 비식별 조건 | `[인쇄]` 평탄 OCV(`β = 0`) → 그 전극 `τ_d` · `β₊ = −β₋` → 전극 맞바꿈 · 한 DoD 에서 두 전극 동역학은 `R_ct` 하나 |
| ASSB 인가 | **아니다** — 액체(LCO 합성 · Kokam NMC 740 mAh 실험). 26·27호 **둘 다 인용 0** |

**세 줄 표에 더하는 것**: 셋째 줄에도 **두 층**이 있다 — "무엇을 식별 집합에 넣었나". 28호는 동역학 축을 식별하고 **모드 축(용량 스케일 · 정렬)을 입력으로 뺐다**.
카드 Q4 가 묻는 것은 모드 축의 유일성이므로 **셋째 줄에 서 있어도 Q4 의 대상이 아닐 수 있다.** 논문을 읽을 때 "식별성을 했다" 다음에 **"식별 집합에 무엇이 있나"** 를 적는다(처방 7).

**Q4 는 ASSB 0/28** (스물한 번째 성질 "도구는 있고 대상이 없다"). 26호의 `k₁≡k₂` 는 28호 식 (50) 과 같은 구조, 26호 `D_e⁻` 0 열은 28호 예외 1(`β = 0`)과 같은 부류 · 다른 기구
(관측 이득 0 은 작동점으로 풀리고, 모델 구조의 포화는 안 풀린다), 27호의 오프셋 `1 − u` 는 28호 `Q_th` 손잡이와 같은 자리 — 전부 우리 `[해석]` 이다.

⚠ **합자 맹점이 IEEE 에도 있다** — 큐 지문의 `identifiab` 9 는 전부 대문자 쪽 머리글이었고 본문 출현은 합자 속에 있었다(NFKC 뒤 54). 처방 1 의 지문은 **NFKC 뒤에** 센다.

## ★★★★ 29호 — 둘째 줄에 처음 붙은 수치, 그리고 **대상에 용량 스케일이 있다**

`raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode.md` (Yanev et al. 2024, *JES* 171, 050530 — ASSB 실험, 14 복합체, 신품).

| 물음 | 29호 |
|---|---|
| 어느 줄인가 | **둘째 줄(추정 민감도)** — 추정 데이터(CA 율 곡선) 위의 적합에서 OriginPro **"dependency"**(파라미터 공분산에서 나오는 공선 지표, 1 에 가까우면 다른 파라미터와 독립으로 못 정함)를 계산 |
| 식별 집합 | `(Q_M, α, n)` — **`Q_M` = 무한 저율 용량(용량 스케일)** 이 들어 있다. 28호는 이 축을 입력으로 뺐다 |
| 비식별 명제 | `[인쇄]` sc90 "not enough information in the measured data to accurately fit the Q_M and α … high dependencies close to unity in Table S2. Only the fit parameter n can be reasonably interpreted" |
| 구조 | `[재현]` `Q(R) = Q_M/(1+2(Rα)ⁿ)` 의 고율 극한 `(Q_M/2)(Rα)⁻ⁿ` ⇒ 평탄이 창 밖이면 `Q_M·α⁻ⁿ` 한 조합 · `n` 은 기울기라 조합 밖 — 저자 판정과 정확히 맞다 |
| 약점 | 수치는 SI(미열람) · 국소 공분산 하나 · **진단을 해석에 전파 안 함**(sc90 무표시 작도, 같은 문제의 sc84 외삽값으로 "LIB 초과 이용률") |

**Q4 는 ASSB 첫 반 칸(0/28 → 0.5).** 이 페이지 표의 둘째 줄 정의("`J` 의 열이 평행하거나 0 이면 비식별 **후보** — 절반")와 같은 무게로 셌다.
⇒ **세 줄 표에 더하는 것**: 둘째 줄은 "후보" 로만 남는 것이 아니라 **적합 소프트웨어가 기본으로 내놓는 dependency/상관 행렬**로 수치가 된다 — 추정 논문이 그 표를 SI 에 싣는지 먼저 본다(처방 8).

### ↳ 29호 SI 보강 (2026-09-28) — 둘째 줄의 수치를 봤다

`raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode-si.md` (SI 6 쪽 — Tab. S2 · 그림 S1–S8).

| 물음 | SI 뒤 |
|---|---|
| 값 | `[인쇄]` 14 셀 × (`Q_M` · `α` · `n`) 값과 dependency. **0.95 를 넘는 셀은 셋** — sc90 0.998 / 0.998 / 0.885 · sc90-BM 0.976 / 0.962 / 0.830 · **sc84 0.973 / 0.957 / 0.832**(`Q_M` / `α` / `n`) — 본문이 경고한 것은 sc90 하나. 넷째 gran90 0.82 / 0.73 / 0.54, 나머지 `Q_M` 0.14–0.56. **표준오차 · CI 0** |
| 무엇을 쟀나 | `[재현]` 창 끝(0.02 C)에서 적합 곡선이 `Q_M` 에 닿은 정도(`Q(R_min)/Q_M`)와 `Q_M` dependency 의 Spearman **ρ = −0.991** — 진단은 **측정 창(설계)의 성질**을 잰다. 3-파라미터 야코비안 모사(설계 가정 넷)는 순위를 재현(0.965–0.991), 절대값은 못 한다(표본 배치 · 가중 미기재) |
| 진단이 옳았나 | `[도표]`+`[재현]` 경고 수준인데 본문이 경고하지 않은 두 셀의 `Q_M`(sc84 236 · sc90-BM 179–205)이 **자기 형성 첫 CCCV 충전(Fig. S6, ≈209 · ≈158 mAh g⁻¹)을 넘는다** — 방전이 돌려줄 수 있는 Li 의 상한 밖. dependency 가 낮은 11 셀은 상한 안 |
| 약점 | 국소 · 폭 0 · 축이 정적 ↔ 동적 — **그대로**. 그리고 같은 셀의 파라미터가 Tab. S2 · Fig. 4 · Fig. S7 에서 다르다(sc84-BM `α` ×1.9 · sc90-BM 세 값) |

⇒ **Q4 반 칸 확정**(반 칸 이유 ① 해소 · ④ 강화) — 누적 변화 0. 이 페이지 세 줄 표에 더하는 것: **둘째 줄 진단은 "창 끝에서 곡선이 얼마나 굽었나" 를 잰다** — 같은 곡선 모양이면 창을 더 낮은 율까지 넓히는 것이 진단을 바꾸는 손잡이다. 그리고 1 에 붙은 값은 **물리 상한(그 셀의 충전 전하 · 재고)** 으로 교차 검사할 수 있다(처방 8 덧붙임).

## ★★ 30호 — 세 줄 어디에도 없는 편: 교과서 선형화 추출

`raw/papers/park2024_asymmetric-kinetics-low-mass-loading-nmc111-latp-li-metal.md` (Park 2024, *Materials* 17, 5014 — LATP 펠릿 Li 금속 셀, 주사율 CV).

| 물음 | 30호 |
|---|---|
| 어느 줄인가 | **어느 줄도 아니다.** 파라미터를 흔들지도(첫 줄), 적합 근방 `J` 를 보지도(둘째 줄), 식별성을 재지도(셋째 줄) 않는다. 값은 **교과서 식의 선형화 회귀**(log–log 기울기 b · `I_p`–`ν^½` 기울기 · Dunn 전위별 회귀)에서 나온다 — `fit`·`regression` 낱말 0 |
| 무엇이 먼저 깨지나 | **모형 전제.** 같은 봉우리 전류에서 b ≠ 0.5(멱법칙)를 보인 뒤 b = 0.5 를 전제하는 Randles–Ševčík 로 `D` 를 뽑는다 · `[재현]` 회귀 절편 ≠ 0 |
| 그보다 먼저 깨지는 것 | ★ **라벨.** `[재현]` 그림에서 다시 구한 b 는 산화 ≈0.58 · 환원 ≈0.73, 인쇄는 0.76 · 0.58 |
| 묶음 | `D_app ∝ 1/(A·C)²` — 29호 GITT 와 같은 부류([[spm-grouped-parameter-identifiability]]) |

⇒ **처방 9**(아래)를 붙였다. 식별성 이전에 **전제와 라벨**을 검사하는 층이 있고, ASSB 실험 문헌의 상당수가 그 층에서 끝날 수 있다(표본 1 — 일반화하지 않는다).

## ★★ 31호 — 세 줄 밖의 네 번째 도구: **방법 간 일치 ≠ 인자 식별**

`raw/papers/chien2023_ici-rapid-solid-state-diffusion-coefficient.md` (Chien et al. 2023, ⚠ **액체셀**, ICI 방법 원전).
이 편의 검증은 **세 방법(GITT · ICI · EIS)이 같은 값을 낸다**는 것이다 — `k` 상대차 평균 0.013 · SD 0.26, OCP 기울기 SD 0.076, `D` 평균 0.15 · SD 0.56(SI Fig. 9 · 11 · 12). 이것은 위 표 어느 줄도 아니다: **스윕도, 추정 데이터 위 `J` 도, FIM 도 아니고 교차 방법 일치(cross-method agreement)** 다.
`[해석]` 세 방법이 **같은 묶음**(`D·(A/V)²`, EIS 도 `σ ∝ 1/(A√D)`)을 보면 일치는 **묶음 측정의 재현성**을 보이지 묶음 **안의 인자**(`D` ↔ 면적)를 식별하지 않는다. 저자는 이를 알고 비교를 `A` 약분 형태로 한정했다(`[인쇄]` "both of which are equally affected by this factor") — **교차 방법 일치가 무엇을 보증하지 않는지를 인쇄한** 계보 첫 문장이다. 그러나 그 한정은 논문 후반의 절대 주장(사이클 `D` 감소)으로 이어지지 않는다.
`[재현]` `D` 불일치 SD 는 `2·√(0.26² + 0.076²) = 0.54` 로 거의 전부 `k`(√t 기울기) 불일치에서 오고, 그림 오차막대(회귀 SD)는 그 1/2–1/5 이다 — **회귀 SD 는 분석창 · 프로토콜 · 상수 선택을 안 본다.** 상수 선택(BET ↔ D50 구) 하나가 `D` 를 ×2.5 움직인다.
⇒ 처방 목록에 한 줄: **"방법들이 일치한다" 를 보면 두 방법이 같은 묶음을 보는지부터 확인한다 — 같은 묶음이면 일치는 식별의 증거가 아니다.**

## ★★ 35호 — 표 밖의 다섯 번째 도구: **예측 보정 ≠ 식별성**

`raw/papers/roman2021_ml-pipeline-soh-estimation-uncertainty.md` (Roman et al. 2021, *Nat. Mach. Intell.* 3, 447, ⚠ **액체 상용 셀 · ML 방법 논문 · ASSB 0**).
이 편의 불확실성 도구는 이 계보에서 **가장 완비**돼 있다 — 예측 분포 `N(μ, σ²)`, 보정 전용 셀(5 · 10 · 1 개)에 isotonic 재보정, 시험 셀의 90 % 적중률 `C_score`,
날카로움 Sh, 예측 띠 안 확률 질량 β, 조기 예측 비율 PEP. 그러나 목표는 **용량 스칼라 하나**다(`LLI` · `LAM` · `degradation mode` 0).
`[해석]` 위 표의 어느 줄도 아니다: 스윕도 `J` 도 FIM 도 교차 방법 일치도 아니고, **예측이 측정 라벨을 얼마나 자주 덮는가**다. 곱 축퇴나 LLI ↔ LAM 축퇴는
**데이터(그리고 용량)가 같은 값을 내는 방향**이라, 그 방향으로 해가 아무리 넓게 퍼져도 용량 예측과 그 적중률은 **변하지 않는다**. ⇒ 보정이 완벽해도 식별성에 대해 0 을 말한다.
그리고 적중률은 **그룹 평균**이다 — `figure-read ≈` 한 시험 셀(Group II 셀 1)은 재보정 뒤 90 % 목표에서 ≈74 % 로 오히려 멀어졌다(Fig. 4b).
⇒ 처방 목록에 한 줄: **"calibrated uncertainty" 를 보면 대상이 예측인지 파라미터인지부터 적는다 — 예측이면 식별성의 증거로 세지 않는다.**

## ★★ 36호 — 표 밖의 여섯 번째 도구: **불확실성 분류 ≠ 식별성**

`raw/papers/thelen2024_probabilistic-ml-battery-health-review.md` (Thelen et al. 2024, *npj Mater. Sustain.* 2, 14, ⚠ **Review · 1차 측정 0 · ASSB 0**).
확률적 ML 종설 — `uncertaint` 180 · `posterior` 26 · `epistemic` 11 인데 `identifiab` 0. 불확실성은 첫 쪽에서 `[인쇄]` "the predictive uncertainty of an ML model … for a training/test sample point" 로 정의되고,
사후는 전부 **ML 가중치**의 사후다. 이 편이 보태는 것은 도구가 아니라 **분류**다: aleatory(`[인쇄]` "irreducible") ↔ epistemic(`[인쇄]` "reducible", model-form · parameter) · CI ⊂ PI ⊂ TI.
`[해석]` 식별성의 폭은 이 두 칸 어디에도 안 맞는다 — **데이터량에 따라 줄지 않는 파라미터 불확실성**이다. 그래서 이 분류는 식별성의 증거를 못 줄 뿐 아니라, 폭을 "데이터 부족" 으로 **오독하게 만든다**.
가장 가까운 것은 이 편이 재인용한 Gasper 2021(`[인쇄]` "model parameter uncertainty can be very large when … too many fittable parameters are included") — **부트스트랩 파라미터 분포**는 우리 폭과 같은 종류의 대상이다(원전 미열람, 액체 · 수명 모델 계수).
그리고 `[인쇄]` "This would require the probing … of posterior results (not just posterior-predictive results and not just looking at RMSE)" — 이 편에서 우리 입장에 가장 가까운 문장이지만 대상은 가중치다.
⇒ 처방 목록에 한 줄: **불확실성 문헌의 "parameter uncertainty" 를 보면 무엇의 파라미터인지(물리 ↔ ML 가중치)와 데이터를 늘리면 줄어드는지를 먼저 적는다.**

## ★★★ 37호 — 첫 줄 스윕이 **항등 쌍의 한쪽만** 흔든다, 그리고 "minimal" 이 무엇의 minimal 인가

`raw/papers/li2024_assb-composite-cathode-model-contact-area-edl.md` (Li et al. 2024, *eTransportation* 20, 100315 — 9호가 위임한 원형 모델).
`[인쇄]` "through a parameter sensitivity analysis, we offer strategic guidelines for optimizing battery performance" — Fig. 11, **0.4 C 한 율 · OAT 6 판**(`R_s` ×0.5/×1.5 · `A_eff` 1.0/0.3 · `L_SE` ×0.1 · `ε_p` 0.32). 첫 줄(설계)이다. `identifiab` 0.
`[해석]` 이 편에서 스윕 그림이 공짜 야코비안으로 주는 것은 둘이다:
1. **`A_eff` 판은 짝(`k_p`)을 흔들지 않았다** — 식 (8) · (5) 에서 `A_eff ↔ k_p` 는 정확한 스케일 대칭이라 두 열은 **정확히 평행**하다. 짝을 흔들지 않은 스윕은 그 평행을 보여 줄 수 없다(27호 처방 5 의 "보상은 교호작용 지수로 안 보인다" 와 같은 맹점, OAT 판).
2. **"minimal deviation" 은 용량 끝점의 말이다** — `[재현]` 인쇄 파라미터로 0.4 C 중간 SOC 전압은 `A_eff` 1.0 에서 +61 mV · 0.3 에서 −37 mV(`[도표]` Fig. 11b/e ≈60 · ≈35 mV) = 그 율 RMSE(11.5 mV)의 3–5 배. **데이터(전압)에 대한 열은 0 이 아니다** — 다만 `k_p` 열과 평행이다. 설계 KPI(용량)로 읽은 "둔감" 을 식별성의 0 열로 옮기면 틀린다.
그리고 이 편의 적합은 **율마다 다시 정하는 `D_p,ref(C-rate)`** 를 가진다 — 둘째 줄(추정 데이터 위 `J`)을 계산한다면 율 축의 정보가 먼저 그 파라미터 열로 간다.
⇒ 처방 목록에 한 줄: **OAT 스윕에서 "둔감" 을 보면 (i) 출력이 용량인지 전압인지 (ii) 그 파라미터와 곱으로만 들어가는 짝이 있는지를 식에서 먼저 찾는다.**

## ★★ 49호 — 31호 줄의 원전형: **총량이 한 곡선에 모인다 ≠ 성분이 식별된다**, 그리고 대역 끝이 파라미터 값을 정한다

`raw/papers/barai2018_measurement-timescale-internal-resistance-methods.md` (Barai et al. 2018, ⚠ **액체셀**, 상용 20 Ah LFP/흑연 파우치 한 상태).
이 편의 검증도 **교차 방법 일치**다 — DC 펄스 · 1 kHz · EIS · 펄스-다중사인의 저항이 "timescales match" 하면 한 곡선(EIS \|Z\|, 가로축 t = 1/f)에 모인다(`[재현]` 5 C: −6 … +11 %). 31호보다 5 년 이르고, 모이는 것은 **총량**이다.
`[해석]` 세 가지를 더한다.
1. **성분은 모이지 않는다** — 같은 이름이 방법마다 `R₀` ×2.0 · `R_CT` ×2.9 · `R_p` ×13, EIS 에서 경계만 0.1 → 0.01 Hz 로 옮겨 `R_p` ×3.9. 원문도 `R_p` 를 "pre-defined" 로 적었다. ⇒ 총량 일치는 **창 차분(성분)** 의 식별을 보증하지 않는다(31호: 같은 묶음을 보는 방법끼리의 일치는 인자 식별이 아니다 — 같은 범주).
2. **일치의 분해능** — 규약을 t = 1/(2πf) 로 옮기면 일치가 −13 … −23 % 로 벌어진다(그림 판독). 스펙트럼이 decade 당 ≈15–19 % 변하는 평탄한 셀에서 "timescales match" 는 시간 척도를 ≈1 decade 로만 가른다.
3. **대역 끝 흡수** — 다중사인 ECM 직렬 `R₀` 1.62 = \|Z\|(1 Hz)(여기 최고 1 Hz) · DC 0.1 s = \|Z\|(10 Hz)(장비 10 Hz). 적합된 직렬 파라미터는 **관측 대역 위쪽 끝의 임피던스**를 가져간다 — 스윕 · `J` · FIM 표 어느 줄도 아닌, **여기 설계가 파라미터의 뜻을 정하는** 경우다. 원문은 ECM 비유일성("not uniquely identifiable" · "ambiguities … Ro and RCT" · "judged solely on closeness of fit")을 인쇄하고, 결론에서는 "EIS can accurately provide separation and identification of all the individual resistance components" 로 지웠다.
⇒ 처방 목록에 한 줄(13).

## ★★ 53호 — 스파이더 그림: 묶음 OAT · **순서 의존을 인쇄** · 한 손잡이가 두 물리를 움직인다

`raw/papers/ren2023_oxide-ssb-composite-cathode-architecture-perspective.md` (Ren · Danner 2023, ⚠ Perspective — P2D 사례 계산 Fig. 9).
`[인쇄]` "we perform a **sensitivity analysis** of the virtual cells to determine the limiting processes" — 모든 파라미터를 improved 로 두고 **묶음 하나씩**(σ⁰·β_tort · σ⁰·β_SP·β_tort · `R_IP`·`R_CT` · `R_CT` · `D_Li`·`d50` · κ⁰) state-of-the-art 로 되돌린 비에너지 스파이더(1 · 10 mA × 50 · 100 µm), 그다음 누적 막대(Fig. 9D).
`[해석]` 세 가지:
1. **묶음이 겹친다** — "Resistive Interphases (`R_IP`, `R_CT`)" 와 "Charge Transfer (`R_CT`)" 가 `R_CT` 를 공유한다. `[도표]` `R_CT` 단독 가지는 두 두께 · 두 전류에서 손실 ≈0 이라, 앞 묶음의 손실은 사실상 `R_IP`(= 표의 `R_SP`) 몫이다 — 본문 "charge transfer kinetics … prominent effect" 와 어긋난다(53호 D10).
2. **비가법성을 인쇄하고 재지 않는다** — `[인쇄]` "the order of the improvements is also crucial and has a significant influence" — OAT 가 교호작용을 못 본다는 것을 저자가 알고, 누적 막대의 순서를 **전략**으로 제시한다. 순서를 바꾼 막대는 없다.
3. **"CAM Li Diffusion Length (`D_Li`, `d50`)"** — `a`(비계면 면적)가 SI 에 정의되지 않았지만 구 기하(`3ε/r`)라면 `d50` 은 확산 길이와 계면 면적을 **같이** 움직인다. 이름표는 확산인데 이득의 일부는 면적이다(곱 축퇴 페이지 서른여섯 번째 적용).
⇒ 처방 목록에 덧붙임: **스파이더 · 토네이도 그림은 (i) 묶음이 파라미터를 공유하는지 (ii) 한 손잡이가 식에서 몇 군데에 들어가는지 (iii) 순서 의존을 인쇄했는지** 먼저 본다.

## ★★ 54호 — 두 한-파라미터 스윕이 **같은 저주파 끝**에 닿는다: 저자가 "unfeasible" 을 인쇄한 그림 판

`raw/papers/neumann2021_garnet-3d-structure-grain-boundary-transport.md` (Neumann 2021). 다공 시편(42 · 56 %) 불일치를 두 OAT 스윕으로 본다 — Fig. 6 `σ_bulk` 7.69 → 2.0 × 10⁻⁴(최적 42 % 3.0 · 56 % 2.0) · SI Fig. S5 `i₀₀^GB` × 0.75 · × 0.50(최적 42 % × 0.50 · 56 % × 0.75). `[도표]` 두 스윕 모두 첫 호 끝을 실험 골(≈1270 · ≈5.4 kΩ cm²)에 맞출 수 있고, 다른 것은 **고주파 절편**(벌크만 옮김, `[인쇄]` "We do not observe a shift in the bulk polarization contribution along the x-axis") — 그 절편은 **측정 대역 밖**이다. 저자 판정 `[인쇄]` "an exact deconvolution of both contributions via EIS is unfeasible without additional information on the GB composition" · 결론 "bulk **and/or** GB".

- 이 페이지 처방 2("스윕 그림끼리 겹친다")를 **저자 자신이 문장으로 한** 표본 — 26호 · 53호와 달리 결론에서 지우지 않았다.
- ⚠ 그러나 두 스윕은 **공동 적합 · 상관 · 폭 0** 이고, 최적 보정량이 시편마다 비단조(`i₀₀` × 0.50 ↔ × 0.75) — 저자는 편석 경로로 설명하지만 검증 0. 본문은 SI 스윕을 "by 25%" 로 옮긴다(× 0.75 = 저항 +33 %).
- 교정 단계에서는 같은 벌크 ↔ 입계 분할을 **입력 `σ⁰`** 로 정했다 — 비식별 인쇄가 적용 단계에만 걸린다(카드 Q4 마흔여섯 번째 성질).

## ★★ 58호 — 대리모형 위의 OAT 두 줄(C-율 · `G_c`): **축을 바꾸면 효과가 사라지거나 뒤집힌다**

`raw/papers/asheri2023_data-driven-multiscale-ssb-delamination-surrogate.md` (Asheri 2023 — 신경망 대리 + FE² 두 단계, 실험 0). Fig. 10(1 · 2 · 5 C, `G_c` 5.97) · Fig. 11(`G_c` 13.92 · 9 · 5.97 · 5 · 4.21, 1 C) — 둘 다 **한 번에 한 손잡이**, 시간 축 그림.
`[해석]` 세 가지:
1. **축 선택이 결론을 정한다** — `[인쇄]` "At higher C-rates damage starts earlier and evolves faster" 는 시간 축 명제다. `[재현]` 학습 자료(미세 FE)에서 손상은 SOC 의 함수이고(`|j|` ≤ 0.03 에서 곡선 겹침 ≈1 %), 그림의 끝 `⟨d⟩` 도 세 율이 ≈0.19–0.205 로 같다. 전하 축으로 옮기면 효과는 대부분 시간 압축이다.
2. **그림이 서술의 순서를 어긴다** — `[도표]`+`[재현]` 전달 전하 2 C ≈3780 > 5 C ≈3575 > 1 C ≈3450(1 C·s) ↔ "the delivered capacity is smaller"; `G_c` 13.92 가 무손상보다 늦게 끝난다. 대리 위 OAT 에서는 **망 전환 · 학습 분포 밖** 이 스윕 축과 교락할 수 있다(세 율이 서로 다른 망에 걸린다, `[재현]` 추정).
3. **스윕한 손잡이의 식 속 자리를 먼저 본다** — `G_c` 는 `⟨d⟩` 를 거쳐 `a·(1−⟨d⟩)` 한 곳으로 들어가고 그 결합은 `ε_p` 와 같다 → `G_c` 스윕 곡선은 **초기 활물질 분율 스윕과 같은 모양 부류**다(곱 축퇴 페이지 마흔한 번째 적용).
⇒ 처방 목록에 덧붙임: **대리모형 위 스윕은 (i) 원 모델 기준해가 있는 점인지 (ii) 스윕 축이 학습 격자 · 망 경계를 가로지르는지 (iii) 효과를 시간 축이 아니라 전하 · 상태 축으로도 적었는지** 본다.

## ★★ 75호 — 첫 줄 한 칸, **판정 규칙이 24호와 반대 방향**이고 포화를 "다음 한계" 로 읽었다 — 그리고 판정 도구가 두 저항을 묶는다

`raw/papers/naik2022_kinetics-vs-transport-ssb-cathode-mesoscale-regime-map.md` (Naik · Vishnugopi · Mukherjee 2022, *ACS AMI* 14, 29754 — 모형 편, 실험 0 · 24호 ref 54 · 원장 "Q4 입구 후보").
`[인쇄]` "we conduct a performance sensitivity analysis … While maintaining other electrode properties (i.e., tortuosity, ionic conductivity, and active area) constant, only the intrinsic electronic conductivity of the AM is increased" — Fig. 6c, **무탄소 세 조성 · OAT · 출력 = 끝 용량**. 첫 줄(설계)이다. `identif` 4 = 전부 "identify".
`[해석]` 이 편에서 첫 줄 스윕과 판정 도구가 주는 것은 셋이다:
1. **포화를 원인 검사 없이 "다음 한계" 로 읽었다** — `[인쇄]` "this limit signifies a fundamental transition from an electron transport-limited to an ion transport-limited regime". `[재현]` 40 · 60 wt% 포화값을 AM 무게로 나누면 209.5 · 210.5 mAh g⁻¹_AM — 탄소 있는 셀에서 AM 을 다 쓴 값(≈207–209)과 같은 자리다. σ_AM 방향의 0 열(평탄)의 원인은 "이온 수송" 이 아니라 "더 쓸 AM 이 없음" 이다.
2. **판정 규칙이 24호와 반대 방향이다** — 24호: `i₀` 를 흔들어 평평 → "동역학 한계 아님"(스윕 평탄 → 부재). 75호: `k` · `c_e` 를 흔들지 않고, 세 저항 중 동역학 몫이 크면 "동역학 한계"(크기 → 한계). 이 편 안에서도 40 wt% 는 저항 순위로 "동역학 한계" 인데 AM 기준 끝 용량은 `a_s` ×2.0–3.4 에 ±1 % 로 평평하다(`[재현]` — 용량 축은 복합체 기준). 두 규칙은 같은 셀에 다른 답을 낸다.
3. **판정 도구가 두 저항을 묶는다** — 식 12 `η_kin = (1/L_c)∫η dx` 는 전류 가중이 아닌 두께 단순 평균이라, 반응이 몰리면(큰 `R_SE`) `R_kin` 이 희석된다. `[재현]` 표 S3 · S4 아홉 값을 한 θ 의 균질 BV 로 되돌리면 함축 `i₀` 가 7.6×10⁻⁴–3.2 A m⁻²(×4,200)로 흩어진다(한 `k` · 한 `c_e` 모형). 두 "저항" 은 독립 좌표가 아니다.
그리고 곱 `a_s·k·√c_e`(식 5 · 6 · 10)의 **`a_s` 만** 미세구조로 흔들었다 — 37호(`A_eff` 판은 짝 `k_p` 를 흔들지 않았다)의 균질판이다([[assb-lampe-contact-product-degeneracy]] 쉰여덟 번째 적용).
⇒ 처방 목록에 한 줄(15).

## ★★ 76호 — 첫 줄 두 칸(OAT 가상 실험 κ ×≈11 · `D` ×10), **셋째 후보(`i₀`)는 흔들지 않았고 옴 지배는 입력의 귀결** — 그리고 "두 무늬 = 두 원인" 배정이 자기 가상 실험에서 흔들린다

`raw/papers/davis2021_operando-microscopy-graphite-lpscl-composite-current-focusing.md` (Davis · Goel · … · Thornton · Dasgupta 2021, *ACS Energy Lett.* 6, 2993 — 실험 + 2D 해상 모형 · 흑연 \| Li₆PS₅Cl 복합 음극 · 24호 ref 39).
`[인쇄]` 서론 "there is a need to decouple the relative contributions of solid-state diffusion within the active material, interfacial kinetics, and electrostatic…" · 모형 "a hypothetical value of Li diffusivity in graphite that is 10 times higher than the actual value. No other model parameter was changed" — **40 % Gr · C/4 한 조건의 OAT 둘 · 출력 = SOC 지도(정성)**. 첫 줄(설계)이다. `sensitiv` 0(SI "air-sensitive" 1) · `identif` 2 = 전부 "identify".
`[해석]` 이 편에서 첫 줄이 주는 것은 셋이다:
1. **가를 대상으로 적은 셋 중 하나를 흔들지 않았다** — 계면 동역학(`i₀,ref` 232 A m⁻² — 액체 흑연 편 값 · 환산 미인쇄)은 고정. `[재현]` 인쇄 파라미터의 Wagner 형 비 `Wa = (R_ct/aL)/(L/κ_eff)` ≈0.008–0.1(x 0.5–0.99) — 어느 SOC 에서도 ≪ 1 이라 "옴 · 확산이 한계" 는 **입력에서 이미 정해진 영역**이다. 75호(면적만 흔듦)와 합치면 이 계보의 모형 편 둘 다 "kinetics" 를 계면 속도상수로 시험하지 않았다.
2. **"×10" 은 문헌값으로 되돌리기다** — `[인쇄]` SI "the diffusivity value used in the model was 1/10th of the literature value"(근거 "graphite grain boundaries" · 출처 0) ↔ 본문 "10 times higher than the actual value". 둘째 무늬(영역 안 구배)의 크기가 근거 없는 인자에 걸린다.
3. **배정이 일대일이 아니다** — `[도표]` S17(`D` ×10)에서 둘째 무늬와 함께 **두께 방향 대비도** 약해진다(φ_e 강하는 기본과 같음 — 76호 D7). 한 관측 무늬에 두 원인이 기여하는 **배정의 비식별**이고, 곱 축퇴가 아니라 "두 손잡이 → 두 무늬" 사상의 비대각 성분이다. OAT 두 칸으로는 그 비대각을 잴 수 없다.
⇒ 처방 목록에 한 줄(16).

## ★★ 77호 — 설계 스윕 두 축(λ · f_CAM)의 격자 지도와 실험 열 점: 첫 줄(설계)이고, "이온 퍼콜레이션이 한계" 는 다른 한계를 흔든 시험이 아니며 — 모형 ↔ 실험 "일치" 는 닻에 걸린 점을 빼야 셀 수 있다

`raw/papers/shi2020_particle-size-ratio-cathode-utilization-assb.md` (Shi · Tu · … · Ceder 2020, *Adv. Energy Mater.* 10, 1902881 — DEM + 입자 그래프 · 25호 ref 14 · 24호 ref 53).
`[인쇄]` "These results are consistent with ionic percolation being the limiting factor" · "The model-predicted specific capacities were calculated by multiplying the full capacity (largest experimental specific capacity observed, 155 mAh g−1) by the predicted θCAM" — λ(0.33–8) × f_CAM(60–90 wt%) 격자 지도(Fig. 3c) · 출력 = 정적 θ. 첫 줄(설계)이다. `identif` · `sensitiv` · `uncertain` · `fit` 0 회.
`[해석]` 이 편에서 첫 줄이 주는 것은 셋이다:
1. **"X 가 한계" 의 판정이 대안 한계를 흔들지 않았다** — 율 시험 0 · 휴지 0 · 전자 퍼콜레이션 계산 0(`[인쇄]` "our model applies to both electronic and ionic percolations" — 계산 없이) · 입자 안 확산 · 계면 동역학 0. 판정 = 모형 ↔ 첫 방전 대조 + "큰 CAM 이 이긴다" 는 방향 — (주) 다섯 칸 중 ①(순위 · 문턱) ④(저항 정의) ⑤(동역학 손잡이)가 비었다.
2. **"일치" 의 점 수** — 열 셀 중 넷은 모형 θ ≈1 이라 닻(155 = 실험 최대값)에 걸려 **자동으로** 맞는다. 남는 여섯에서 `[재현]` RMS 8.5 mAh g⁻¹ · 크게 빗나간 둘(70 wt%/λ 1.67 모형 0.99 ↔ 0.89 · 80 wt%/λ 3.33 0.72 ↔ 0.62) · 조건당 셀 1 이라 산포와 편향이 안 갈린다.
3. **관측이 하나다** — 첫 충전(5 h CV)에 대면 두 저 λ 셀에서 모형 θ 가 충전 비보다 낮다(0.56 < 0.71 · 0.48 < 0.64). 한 관측(방전)에서의 일치가 다른 관측(충전)에서는 반례가 된다 — 관측 선택이 결론을 정한다.
⇒ 처방 목록에 한 줄(17).

## ★★ 82호 — 실험 스윕 한 축(SE 입도 네 수준): **한 손잡이가 공극 · 면적 · σ_ion · σ_el 를 같이 움직이는데 "균형(σ_ion/σ_el → 1)" 한 축으로 귀속** — 비 > 1 표본이 없어 경쟁 설명과 갈리지 않고, 크기 검사를 거치지 않았다

`raw/papers/schlautmann2023_lpscl-particle-size-distribution-composite-transport.md` (Schlautmann · … · Bielefeld · Zeier 2023, *Adv. Energy Mater.* 13, 2302309 — 실험 네 수준 × 셀 셋 + GeoDict 모형).
`[인쇄]` "An increase in capacity can be observed when the conductivity is balanced and closer to unity. It becomes evident that for a high-performance electrode not only fast charge transport but also balanced charge transport is essential" — Fig. 6b 네 점(σ_ion/σ_el ↔ 용량). 첫 줄(실험 OAT — 손잡이 하나)이다. `identif` 1(ORCID) · `uniqu` 0.
`[해석]` 이 편에서 첫 줄이 주는 것은 셋이다:
1. **한 손잡이 · 다섯 양** — SE 입도가 void(14.1 → 24.3 %) · 모형 면적(×8.6) · 균질도 · σ_ion(×1.54) · σ_el(×0.74 AC)을 함께 움직인다. 네 점 위의 상관은 다섯 중 무엇이 용량을 정하는지 말하지 않는다 — 실험 스윕판의 "평행 열"(처방 2)이다.
2. **경쟁 설명이 같은 예측을 한다** — 네 비가 전부 1 아래(0.41–0.84)라 "균형(→ 1)" 과 "σ_ion 증가" 가 같은 순서를 준다. 둘이 갈리는 쌍(L ↔ XL)은 σ_ion 차가 오차 막대 안이고 면적 · void 도 같은 쪽이며, DC 로 비를 셈하면 순서가 뒤집힌다.
3. **크기 검사가 없다** — `[재현]` 측정 σ_eff 의 옴 강하(가정 두께)는 C/20 2–4 mV · 1C 차 ≤28 mV 로, 1C 전압 간격 0.33–0.92 V · C/20 결손 30 mAh g⁻¹ 의 작은 몫이다. 상관의 크기가 제안된 기구의 크기와 맞는지 보지 않고 귀속했다.
⇒ 처방 목록에 한 줄(18).

## ★★ 83호 — 모형 OAT 두 줄(E · σ)을 **서로의 고정값 없이** 따로 흔들고 조합을 설계 지침으로: 결론 셋이 스윕의 결과가 아니라 **모형 구조 · 기준 선택의 귀결**이다

`raw/papers/jiao2023_electro-chemo-mechanical-se-modulus-conductivity-intergranular-czm.md` (Jiao · … · Xu X. · Liu Y. 2023, *Energy Storage Mater.* 61, 102864 — 순수 모형: 3D 복합 양극 한 번 방전 + 2D 입계 CZM).
`[인쇄]` "high-adequate ionic conductivity of 5 × 10−4 S cm−1 and soft mechanical property of E=~2 GPa can be proposed as the guideline of SE" — SE E 아홉 값 · σ 열두 값의 두 OAT 줄과 CZM 2 × 2(첫 줄). `identif` · `uniqu` · `sensitiv` · `uncertain` · `valid` 0.
`[해석]` 이 편에서 첫 줄이 주는 것은 넷이다:
1. **조합 run 0 · 고정값 미인쇄** — E 스윕의 σ, σ 스윕의 E 가 지면에 없다. "E ≈2 GPa **와** σ 5×10⁻⁴" 는 두 줄을 글로 합친 것이다(서로 이어지지 않은 3D · 2D 두 모형의 결론까지).
2. **"둔감" 이 구조의 귀결** — E 스윕의 방전 곡선 · EIS 가 겹치는 것은 역학 → 전기화학 결합이 ϕ_mech 하나(`[재현]` 0.6–1.1 mV/100 MPa)이고 CAM\|SE 박리가 가정으로 빠졌기 때문이다 — 스윕이 "영향 없음" 을 보인 것이 아니라 모형이 그 경로를 두지 않았다(처방 12 의 확장 — 둔감의 원인이 짝의 보상이 아니라 식 구조 · 가정에 있다).
3. **문턱에 무차원 조건이 없다** — "σ 5×10⁻⁴ threshold" 는 전류 미인쇄 · 열두 값 중 여덟 미인쇄. `[재현]` 옴 강하가 RT/F 가 되는 전류 ≈1C(가정) — 문턱은 재료 상수가 아니라 영역 경계(처방 15 ④).
4. **기준을 바꿔 순위를 뒤집었다** — CZM 파괴 사이클은 두 SE 모두 fine > coarse(1545 > 1409 · 132 > 95)인데, 초록 "postponed by the coarse-primary" 는 총 균열 기준으로 고른 결론이다(처방 17 ②와 같은 모양 — 관측 선택이 결론을 정한다).
⇒ 처방 목록에 한 줄(19).

## ★★ 85호 — 스윕 0 · 대신 **온도 기울기(Ea)로 곱 R = ρl/A 의 한쪽을 배정**한 실험 편: 그 Ea 가 인쇄 표로 재현되지 않고, 앞인자 가정은 없으며, A 의 독립 관측도 없다

`raw/papers/wang2024_fast-kinetics-hierarchical-catholyte-anode-design-ssb.md` (Wang Y. · Li X. 2024, *Adv. Mater.* 36, 2309306 — 1차 측정 · 모형 0).
`[인쇄]` "This is because Ea here corresponds to resistivity ρ rather than to resistance R, where σ = 1/ρ ∝ exp(−Ea/kT). The much smaller interface resistance R3 but higher resistivity (ρ) for the mixed catholyte cell than the large catholyte-only cell thus suggests that although adding small LPSCl1.5 particles increases the resistivity at various interfaces, the overall interface contact area (A) is dramatically increased; thus, giving a much lower resistance (R = ρl/A)". `identif` 1(ORCID) · `uniqu` 1 · `sensitiv` 0.
`[해석]` 이 편이 주는 것은 넷이다:
1. **곱을 두 관측으로 풀었다고 인쇄** — R(25 °C)와 Ea(기울기)로 ρ · A 둘을 정했다. 두 미지수 · 두 관측이지만 Ea → ρ 는 **같은 앞인자** 가정 위에 있고 그 가정은 인쇄 0.
2. **수치가 재현되지 않는다** `[재현]` — 인쇄 Ea 8 중 7 = `k_B · d log₁₀(T/R)/d(1/T)`(ln 10 누락 · ±1 meV) · mixed/Si–Cl R3 284 는 55 °C 점을 표 S1 의 R2 값으로 두어야 나온다(그림 S1(b) 점 2.00) · 표대로 255 → 본문 "37 · 86 · 42 meV" 가 **7 · 57 · 13** · 4 ↔ 3 점 적합 차 ≤27 meV.
3. **면적 무관 관측이 지면에 있는데 안 썼다** — τ = RC = ρε(면적 · 두께 소거) `[재현]` mixed/large ×2.2 · small/large ×2.4(25 °C) → ρε ↑ 는 Ea 없이도 선다(단 R · C 둘로 A · ρ 둘을 정하는 동어반복이며 독립 A 는 여전히 0).
4. **배정 연산자가 구성 차 하나** — large ↔ small 두 구성의 R2 · R3 순서로 "수송 ↔ 접촉" 을 가르고(처방 15 ①), 그 회로의 셋째 저항(R1 — 저자 정의 "연결 전해질 망")이 같은 크기로 움직인 것(`[도표]` 68 ↔ 37 ↔ 27 Ω)은 판정에 들어가지 않았다.
⇒ 처방 목록에 한 줄(20).

## ★★ 86호 — 스윕 = 성형 압력 3 점(300–500 MPa) · 운전 0 · 대신 **GITT 식 (1) 의 곱 `D·S²` 를 `D` 고정으로 `S`("피복률")에 배정**한 실험 편: `D` 는 미인쇄이고, 같은 지면의 첫 충전 등가가 정적 면적 차 ≈0 을 주는데 대조하지 않았다

`raw/papers/kim2023_argyrodite-coated-ncm-normal-pressure-assb.md` (Kim J.T. … 2023 *J. Mater. Chem. A* 11, 20549 — 25호 ref 17 · 3차 묶음 파일 48).

- **첫 줄(설계 스윕)**: 성형 압력 300 / 400 / 500 MPa 첫 사이클(S13) — LP2 `[도표]` ≤5 % 차 · bare 300 MPa −6 % · 500 MPa 미세균열 → `[인쇄]` "the pressure of 410 MPa … seems to be appropriate" 는 bare 쪽 판정(라벨 400 ↔ 본문 410) · 셀 하나씩 · 운전 압력 축 0.
- **곱의 배정**: `D = (4/πτ)(m V_M/(M S))²(ΔEs/ΔEt)²` — 한 식에 두 미지수(`D` · `S`) · `D` 를 고정(값 · 출처 0)해 `S` 83.9 ↔ 19.7 % · (주) 기준: 무엇(피복률 비) · 시간 기준(GITT 방전 · 펄스 SOC 0) · 조건(0.5C 60 s · 2 h · 30 °C) · 정의(분모 BET?) · 손잡이(`D` 가정 미인쇄) — 85호(온도 기울기로 `ρ` ↔ `A`)의 GITT 판.
- **자기 데이터 교차**: 첫 충전 `[재현]` 202.1 ↔ 201.9 mAh g⁻¹ → 정적 면적(고립) 차 ≈0 · "×4.26" 은 분극 비 — 교차하지 않았다.
- **재현 결과**: SE Ea 는 σT 규약으로 ±0.015 eV 재현(85호와 반대 — 규약을 찾으면 맞는 편) · 그러나 S4 ↔ 1g RT 불일치(D2) · σ ↔ σₑ 두께 역산 ×1.7–4.3(D3).


## ★★★ 91호 — 스윕 0 · 추정 = "model optimization" 한 줄 · 그러나 **인쇄 표로 저자 그림을 다시 풀면 `k_r` 가 ×100 어긋나고**, 같은 모형의 국소 CRB 는 전해질 넷을 한 묶음으로 본다 — 26호 계보의 첫 표

`raw/papers/danilov2011_thin-film-assb-model-weak-electrolyte-parameter-fit.md` (Danilov · Niessen · Notten 2011 *J. Electrochem. Soc.* 158, A215 — 26호 [15] · 4차 묶음 파일 51).

- **위 표의 어느 줄인가**: 어느 줄도 아니다 — 스윕 · 민감도 · Fisher · 신뢰구간 · 식별성 어휘 **본문 전수 0**(NFKC 전후). 추정은 "The optimized parameters are listed in Table II" · 각주 "obtained from model optimization" 뿐(손실 · 알고리즘 · 잔차 0). 일치는 "agree" **9 회**.
- **재풀이(이 페이지 처방 2 · 3 의 원형 모형판 — 스윕 대신 인쇄 표 자체로)**: `[재현]` 표 II 값 그대로 전해질 부분계(식 18–20)를 풀면 그림 8a · 11 · 12 가 안 나온다(RMS 64 mV · 정상 한계 전류 ≈257 µA cm⁻² < 51.2C 512) · **`k_r` 하나만 ×100**(≈0.90×10⁻⁶)이면 RMS 0.8 mV — 26호 "문헌값" 8.00×10⁻⁷ 과 같은 자릿수. 26호의 "문헌과 5 % 이내" 가 기대는 계보에서 **첫 표의 인쇄 값부터 그림과 안 맞는다**.
- **국소 CRB(`[재현·가정]` 우리 재풀이 모형 · σ_V 1 mV · 여섯 율)**: 전해질 넷(`k_r` · `δ` · `D_Li⁺` · `D_n⁻`) \|ρ\| ≥ 0.98 · 조건수 9.5×10⁵ · 1σ ×1.4–1.9 ↔ `D_Li` ×1.005 · `α` ×1.03 · i₀ ×1.10 — 26호 §5-2 ④ "전해질 셋 — 전도도형 한 조합"(26호 `[추론]`)의 원형 모형 수치. 본문 "only about 18% of the Li atoms are mobile"(`δ`)은 골짜기 위의 한 점이다.
- **(주) 기준으로 본 결론** — "transport limitations in the solid-state electrolyte … at least half of the total overpotential": ① 과전압 몫 ② 시간 기준 = 51.2C 뒷 절반(본문) ↔ 초록은 뗌 ③ 0.512 mA cm⁻² · "or higher" 모의 0 ④ — ⑤ 몫이 `k_r` 자릿수 · 이원 SE 가정(`[재현·가정]` ≈71 %)에 매달림 · `[재현·벡터]` 시간 평균 45 · 46 %.
- **후보 처방(결정 대기 — 새 판단 거리)**: "추정 논문의 매개변수 표가 계보의 '문헌값' 으로 쓰이면, 인쇄 값으로 저자 그림 하나를 다시 풀어 폐합을 본다" — 처방 2 · 3(스윕 그림 겹치기 · 적합 ÷ 문헌 비)의 **스윕 없는 편 판**. 격상은 결정하지 않는다.


## ★★★ 92호 — 표 밖의 일곱 번째 도구: **비선형 시스템 식별(BLA · 블록 지향) ≠ 식별성**, 그리고 블록 모양은 정규화 · 구조가 정한다

`raw/papers/firouz2020_hammerstein-wiener-multisine-bla-nonlinearity-assb.md` (Firouz · Goutam · Cazorla Soult · Mohammadi · Van Mierlo · Van den Bossche 2020 *J. Energy Storage* 28, 101184 — 26호 [17] · 원장 구조적 공백 1번 후보 · 4차 묶음 파일 52).

- **위 표의 어느 줄인가**: 새 줄("비선형 시스템 식별") — 26호 Table 1 이 "Parameter Estimation Yes" 로 묶은 경험식 편. 무작위 위상 다중정현(33 선 · 4 mHz–1 Hz · M 4 × P 6)으로 BLA 를 내고 셀 2 에 H · W · H-W 를 맞췄다. 식별성 어휘(`identifiab*` · `confiden*` · `Fisher` · `D-optim*`) **0**(NFKC 전후) · `variance` 6 은 전부 BLA.
- **"분산" 의 정체**: 식 9–11 은 FRF 의 잡음 ↔ 확률적 비선형 왜곡 분산이다(매개변수 분산 0). `[재현]` 인쇄 식대로면 식 9 · 10 이 한 주기 FRF 의 분산이라 식 11 의 ×M 이 실현당 왜곡을 ×3.13(+5 dB) 키운다(Monte Carlo · 저자 코드 미대조).
- **구조적 비식별(셋째 줄의 블록 판)**: 선형 블록을 BLA 로 고정해도 `(k·f_h, f_w(·/k))` · `(f_h + c, f_w(· − G(1)c))` 가 같은 출력 — `[재현]` 수치 차 0 · 3×10⁻¹³. 정규화가 인쇄되지 않아 그림 13 의 "선형선 이탈" 과 f_w 꺾인점("−0.4", 선형 출력 좌표)은 정규화 의존이고, 같은 자료에서 입력 블록 곡률이 H 단독(확장) ↔ H-W(포화)로 뒤집힌다 — 26호 그림 겹치기(처방 2)의 **구조 판**: 같은 데이터가 두 블록 사이 몫을 정하지 않는다.
- **입력 설계판(34호 줄)과의 관계**: 입력 설계는 실재하나 목적은 분리(Schoukens 계보)이고 정보 기준 0 · 진폭 한 수준 · 선형 격자(0.04 Hz 아래 2 / 33 `[도표·화소]`) — 34호 줄의 "구조적 비식별에는 D-optimality = 0" 이 이 블록 교환에서 구체로 선다.
- **(주) 기준으로 본 결론** — "the Hammerstein function indicates the current saturation because of the charge-transfer limit and the Wiener function explains the severe voltage drops due to the mass-transfer limit": ① 순위 · 문턱 0 ② 시간 기준 0 ③ 60 ℃ · 50 % SoC · 진폭 하나 ④ — ⑤ 식 35 c_s → c_s,max(값 0) · 근거 모양이 정규화 · 구조 의존.
- **후보 처방(결정 대기 — 새 판단 거리)**: 처방 22(아래) — 격상은 결정하지 않는다.

## ★★★ 93호 — 표 밖의 여덟 번째 도구: **측정 대체(measure, don't fit) ≠ 식별성** — 비유일성 경고를 인쇄하고 적합 단계를 지웠다

`raw/papers/bielefeld2023_useful-models-ssb-simplicity-perspective.md` (Bielefeld 2023 *Batteries & Supercaps* 6, e202300180 — 26호 [6] · 27호 [2] · 1 · 57 · 56호 저자의 Perspective · 4차 묶음 파일 53).

- **위 표의 어느 줄인가**: 새 줄("측정 대체 · 안건형") — 1차 자료 · 계산 0 의 방법론 편. 식별성 어휘(`identifiab*` · `uniqu*` · `uncertaint*` · `Fisher` · `Bayes*`) **0**(NFKC 전후) · 비유일성은 Berro 경고를 옮긴 한 문장("a parameter set which produces a good fit is not necessarily the only parameter set that does")뿐.
- **5단계 "민감도 분석" = 첫 줄**: `[인쇄]` "all input data are limited by their accuracy and precision … If small changes in a parameter result in large deviations in the results, the particular parameter should be elaborated on" — 입력 정밀도에 대한 국소 강건성 · 자기 예(1호)는 void · 입도 · 두께 · 조성 설계 스윕. 처방은 입력 쪽(더 공들여 재라)이고 출력 구간 · 전파는 0.
- **측정 역모형** — 같은 저자 56호(digest 전사): `j₀` ← Rueß `R_CT`(면적 미정의 — 곱 축퇴가 측정 단계에) · `D̃` "may be underestimated significantly" · **그림 7: 측정 SOC 의존 입력 ↔ 상수 `{D₂, j₁}` 가 같은 곡선 가족(0.5 C 에서는 상수가 더 맞음)** — 이 페이지 처방 2 · 3 의 입력 가족판(서로 다른 입력 집합이 같은 출력). 이 편은 그 결과를 쓰지 않는다.
- **단순성의 근거와 식별성** — 과적합 회피(코끼리) · 작은 매개변수 공간 · "distinguishable" 예측 — 식별성 보장을 쓰지는 않는다; 자기 예는 적합 0 이라 첫째가 닿지 않고, 1호 출력은 그 자체로 비유일(`A_spec,a` 평탄 ±4 vol% — 1호 digest).
- **(주) 기준으로 본 결론** — "Conductive carbon is not required above a CAM fraction of 68 vol%": ① 문턱(이용률 판정 기준 — 1호 G5 · 40 % 임의) ② 시간 기준 = 신품 정적 ③ 조건 20 % 공극 · 균일 5 µm(그림 1 에만) ④ — ⑤ — · 검증 = 부피 기준이 다른 조성(전체 Φ · 14 % 가정) 위의 방향 일치.
- **후보 처방(결정 대기 — 새 판단 거리)**: 처방 23(아래) — 격상은 결정하지 않는다.

## ★★★ 95호 — 둘째 줄의 직교화판 + 묶음 + 합성 다중 시작: **출력이 맞는 매개변수 수 ≠ 식별되는 매개변수 수**, 그리고 모드 좌표(창)가 약한 쪽이다 (⚠ 액체 DFN 도구)

`raw/papers/khalik2021_dfn-grouping-sensitivity-parameter-estimation.md` (Khalik · Donkers · Sturm · Bergveld 2021 *J. Power Sources* 499, 229901 — 27호 [27] · 4차 묶음 파일 55 · ⚠ 액체셀 — 28호 선례로 도구 칸).

- **위 표의 어느 줄인가**: 둘째 줄의 새 판(위 표 "직교화 순위 + 합성 다중 시작판") — 추정 자료(동적 전류 · 전압) 위 유한차분 감도 행렬을 사전 범위로 정규화한 β 좌표에서 피벗 QR 로 직교화해 순위를 매긴다(26호식 OAT 스윕보다 한 단계 위 — 평행 열이 순위 뒤로 밀린다). 그 앞에 **셋째 줄의 구조적 조각**이 하나 있다: 정규화 · 묶음으로 원 DFN 35 → 24(출력 = 묶음 함수 — 구성 증명). FIM · 공분산 · 신뢰구간 · 프로파일 0 · `identifiab*` 7(NFKC 전후 같음).
- **묶음의 최소성**: 24 의 식별성은 증명되지 않았다 — `[재현·대수]` 인쇄 식 (9a) 는 `D̂_e p̂`, (11a) 는 `κ̂ p̂` 로만 써서 `(D̂_e, κ̂, p̂) → (D̂_e/λ, κ̂/λ, λp̂)` 가 정확한 대칭이다(식별 가능한 조합 ≤23) · `k̂₀` 묶음의 정확성은 본문이 적지 않은 `α_c = 1 − α_a`(표 1(b) 식 12a · b 에만)에 기댄다. 28호(SPM 14 → 6 → 3)와 같은 계보의 DFN 판 — 묶음 대수는 [[spm-grouped-parameter-identifiability]] "DFN 판" 절.
- **강조문 H2 "Estimating all DFN model parameters is not necessary to obtain an accurate model" 은 출력 기준이다**: 12 개 뒤 출력 RMSE 평탄(그림 5(a)) · 결론 문장도 "(with respect to the output voltage)" 를 단다 — 그리고 저자가 같은 지면에 H1 "Parameters obtained from input/output data are not necessarily physically meaningful" 을 따로 인쇄했다. 27호 절의 **"적합성 ≠ 식별성"** 의 추정 편 판: 출력이 맞는 수(12)와 식별되는 수(미증명)는 다른 물음이다.
- **공짜 조건수**: `[재현]` 피벗 QR 에서 `σ_max(S) ≥ |r₁₁|` · 앞 k 열 블록의 `σ_min ≤ |r_kk|` ⇒ `cond(S_k) ≥ |r₁₁|/|r_kk|` — 그림 4 막대 끝값(벡터 판독)으로 고른 12 개 ≥10^2.98(Cell 1) · 10^3.00(Cell 2) · 22 개 ≥10^6.20 · 10^6.46(β 좌표 · 하한). 저자는 이 값을 조건수로 읽지 않는다. 처방 2 · 3(스윕 겹치기)의 **순위 그림판**이다 — 순위 그림을 인쇄한 편이면 막대 끝값 비가 하한을 준다.
- **합성 참값 시험 — 일관성 ≠ 정확성**: 범위 안 무작위 참값 하나 · 같은 모형 · 무잡음(역범죄 — 28호와 같은 설계) · 다중 시작 50 → `[도표·벡터]` 참값이 IQR 밖 14/22 · `[재현]` 표 4 "Random parameters" 행 = 균등 무작위 β 의 기대 RMS(0.427 ↔ 인쇄 0.43) · 모형 오차 둘(출력 1.2 mV)을 넣으면 β RMSE 0.43–0.44 = 무작위 수준 · 세 수정 모두 `s_p,100%`(양극 창 끝) 중앙값이 범위 하한. 실셀 Cell 1 은 상자가 좁고 22 개 중 중앙값 10 개가 범위 끝 — `[해석]` **좁은 상자 + 범위 끝은 경계에 눌린 일관성**이다(저자도 원인 후보로 "unmodeled behavior … or … the ranges chosen for the parameters are too small" 을 인쇄).
- **모드 좌표(창 넷)가 식별 집합 안에 있다 — 28호와 반대쪽 끝**: 셀 EMF 만 아는 구성(경우 1)에서 창은 평형 채널에 정의상 무정보(`[인쇄]` "the same EMF-SOC relation can be reached with any choice between 0 and 1") · 0 % 끝 둘은 순위 15–21 위(12 개 밖 — β 0.5 고정) · Cell 1 다중 시작에서 창 넷 중 셋이 범위 끝 · 합성 모형 오차 1.2 mV 에서 `s_p,100%` 0.418 → 0.22(범위 하한) `[도표·벡터]`.
- **(주) 기준으로 본 결론** — "estimating 12 out of all 22 model parameters is sufficient to obtain an accurate model (with respect to the output voltage)"(결론 — 저자 스스로 출력 전압 기준을 괄호로 단다): ① 순위 = 한 점 국소 · 범위 폭 의존 · 문턱 0(12 는 출력 RMSE 평탄으로 고름) ② 시간 기준 = 신품 · 회차 하나 ③ 조건 = 셀 둘 · 동적 프로파일 · 온도 미인쇄 ④ 기준 = 출력 RMSE(검증 자료로 모형 선택 — Cell 2 검증은 추정 구간 포함) ⑤ 동역학 손잡이 = `k̂₀`(면적 · `k₀` 한 묶음 · `α_c` 가정 위).
- **후보 처방(결정 대기 — 새 판단 거리)**: 처방 24(아래) — 격상은 결정하지 않는다.

## ★★★ 96호 — 셋째 줄의 선형화판: **"nonlinearly identifiable but not linearly identifiable" 을 인쇄하고 소신호 비식별 조합을 손으로 적은 다음, 같은 모형 합성 한 번으로 "highly accurate" 를 냈다** (⚠ 액체 EIS 도구)

`raw/papers/lu2022_nondestructive-eis-lumped-dfne-parameter-estimation.md` (Lu · Trimboli · Fan · Wang · Plett 2022 *J. Electrochem. Soc.* 169, 080504 — 27호 [28] · 4차 묶음 파일 56 · ⚠ 액체셀 — 28 · 95호 선례로 도구 칸).

- **위 표의 어느 줄인가**: 셋째 줄(식별성)의 **구조적 조각 둘** — ① 비선형 PDE 판 LPM 의 식별성은 인용(`[인쇄]` "We know from Ref. 2 that all parameters of the PDE version of the LPM are identifiable" — 지면 증명 0) ② 소신호 TF 의 비식별은 손 분석 결론(ψ̄ · n̄e^r · κ̄D 는 비 둘로만 · R_c ↔ 1/κ̄^s "identical" — 도출은 "some detailed analysis" 로만) — 그리고 실제적 조각 하나(합성 참값 한 번). 감도 행렬 · FIM · 공분산 · 신뢰구간 · 프로파일 · 다중 시작 0 · `identifiab*` 19 · `sensitiv*` 15(Rabissi 인용 · 결과 없는 "A sensitivity study shows …" · 둔감 서술).
- **28호(선형화 SPM)와 같은 연산 · 같은 쪽 끝**: 둘 다 소신호 전달함수에서 식별 집합을 읽고 용량 스케일 · 창(Q · θ0 · θ100)을 **입력**으로 뺀다(이 편은 연재 [4 · 5] 의 OCV · 방전 시험 값). 28호 식 50(두 전극 동역학 → R_ct 하나)과 이 편의 비 둘 · 직렬 합은 같은 부류 — **곱 · 합으로만 들어가는 조합**이다. 95호(창을 식별 집합 안에 넣음)와 셋이 액체 도구 칸을 이룬다.
- **실제적 조각 — 합성 참값 시험의 설계가 폭을 지운다**: 가상 셀 하나 · 같은 TF 모형(역범죄) · 잡음 0.5 % 실현 하나 · particleswarm + fmincon 실행 하나(기본 시드 · 48 h) → `[도표·화소]` 부분 집합(펄스 참값 고정) 열셋 중 열둘 ±5 % · n̄e^s/ψ̄ 1.48 / 전체 집합 n̄e^n/ψ̄ 1.20 · n̄e^s/ψ̄ 0.48 · n̄e^p/ψ̄ 1.25 · κ̄D/ψ̄ 1.19 · R_c 1.64(초기 X = 참값 1.0 에서 출발) · σ̄^p ≈1.66 · κ̄^p ≈1.44 · κ̄^n ≈1.29 · `[재현]` k̄0,6/7 참값이 경계("one order of magnitude around their initial values") 하한의 1/1,287 · 1/411(도달 불가) · 출력 절대 오차 ≲0.04 mΩ. 참값이 경계 **위**(n_f = n_dl = 1 · 경계 0.9–1)인 매개변수도 있다. 본문은 "We see some degradation in the quality of parameter estimates" · R_c "lack of convergence" 를 인쇄하나 초록 · 결론은 단서 없이 "highly accurate" · "very good accuracies". ⇒ 출력 ≲0.04 mΩ 에서 매개변수가 19–66 % 움직인다는 것은 **근최적 폭의 하한 표본**이다(산포 0 인 한 번의 실행이 그것을 보여 줌).
- **실셀 쪽 — 같은 지면이 폭의 둘째 하한을 준다**: SOC 무관 전해질 상수 κ̄D/ψ̄ 를 SOC 별로 따로 맞추면(Strategy 2) 19 점이 −0.031 … −0.36(×12 `[도표·화소]`) · 전 SOC 동시(Strategy 1) −0.040 · 가상 셀 참 −492 · 그리고 `[재현]` 표 VI 최종값이 같은 편 부록의 경계 · 물리 범위 넷 밖 · 둘 경계 위(n̄e^n ×5.1 > 3Q/14 · κ̄D ×1/5,900 · κ̄^p/κ̄^s < 2⁻³·⁵ · R̄dl^n 10⁻¹⁰ < 10⁻⁶ · K_n̄e 2.000 · n_dl^p 0.90).
- **(주) 기준으로 본 결론** — "able to find all parameter values of interest with very good accuracies"(결론): ① 근거 = 같은 모형 합성 한 번(부분 집합) ② 시간 기준 = 신품 · 실셀 이력 미인쇄 ③ 조건 = 25 °C · 셀 하나 · 소신호(C/50) ④ 기준 = 정규화 궤적 그림(추정/참) · 출력 절대 오차 — 불확실성 0 ⑤ 동역학 손잡이 = k̄0,j(면적 · k₀ 한 묶음 — 전극 전체 교환율).
- **후보 처방(결정 대기 — 새 판단 거리)**: 처방 25(아래) — 격상은 결정하지 않는다.

## ★★★ 98호 — 스윕 = "a small sensitivity study"(D 둘 바꾸기 — 설계 KPI) · 추정 = DC + AC 한 벌 동시 적합(방법 0) · **그 적합값이 26호의 '문헌값'** — 그리고 인쇄 식 묶음 그대로의 방향 문제가 그림 셋에 정량으로 남았다

`raw/papers/raijmakers2020_thin-film-assb-model-double-layer-dc-ac-joint-fit.md` (Raijmakers · Danilov · Eichel · Notten 2020 *Electrochim. Acta* 330, 135147 — 26호 [10] · 37호 [14] · 4차 묶음 파일 58).

- **위 표의 어느 줄인가**: 첫 줄 하나 — "a small sensitivity study"(그림 10 — D_Li⊕ = D_e⁻ · 뒤집기 두 경우 · 출력 = 1C 방전 곡선 · 농도 단면 · 설계 결론 "the battery performance increases significantly if the ionic and electronic diffusion coefficients are identical"). 둘째 · 셋째 줄 0 — 식별성 어휘는 ρ_Pt · ρ_Li 직렬 합 한 문장(올바른 구조적 묶음)뿐 · `uniqu*` · `uncertain*` · `±` · `residu*` · `correlat*` 0 · 추정은 "optimized" 뿐(목적 함수 · 알고리즘 · 잔차 0).
- **26호의 '문헌값' 이 무엇이었나**: 이 페이지 처방 3("적합값 ÷ 문헌값이 같은 비율이면 시작점 근방 정지")이 26호에서 본 ×1.0500 의 분모 = **이 편 표 3 의 무각주 적합 9 + EMF 유도 1** — 같은 셀 · 같은 곡선 묶음(+ EIS)의 적합. 26호 "converge into values in agreement with results reported in the literature" 는 **같은 자료 두 적합의 일치**다. 그리고 `[재현·대수]` 이름 ×1.05 뒤에서 모형이 보는 조합(D⁰_p ×1.30 · 경계 분배 0.81 → 1.00 · σ ×1.10)은 움직였다.
- **"관측 추가" 를 처방으로 인쇄**: "when only the DC simulations are used for parameter optimization, the impedance simulations do not agree with the impedance measurements" · "Performing impedance simulations in addition to DC simulations results in much more accurate parameter estimation since more measurement information has been made available" — 비유일성 증상과 처방 선언(값 · 폭 0). `[재현]` 더한 관측이 실제로 닻을 내린 것: 벌크 옴(EIS 호 지름 326.2 ↔ ≈327 Ω cm²) / 못 내린 것: 음극 계면(τ_n/τ_LiPON 0.72 — 같은 대역).
- **재풀이(처방 2 · 3 의 스윕 없는 판 — 91호 절과 같은 연산)**: 표 3 그대로 전해질 · 양극 계면 · 호 지름 ✅ · k_r 인쇄 = 그림(91호 ×100 과 반대) / 음극 계면은 인쇄 식 (12) · (16) 글자 그대로의 반대 방향 계산과 그림 9e · 9f 삽도 · 11c 가 정량 일치 — **크기 폐합(1C)으로는 안 보이고 부호 · 저주파 위상에서 보인다**.
- **(주) 기준으로 본 결론** — "the overpotential across the LiPON electrolyte is most dominant": ① 과전압 몫(η_bat 의 66–67 % `[도표·화소]`) ② 시간 기준 = 방전 중간 ③ 1C · 4C · 셀 한 종 ④ — ⑤ `[재현·가정]` 이원 가정 몫 ≈8 % — 벌크 옴이 EIS 로 닻을 내려 91호(≈71 %)보다 단단하다.
- **후보 처방(결정 대기 — 새 판단 거리)**: 처방 26(아래) — 격상은 결정하지 않는다.

## ★★★ 99호 — '민감도 분석' = 축약 오차의 OAT(동기는 식별성 [19, 20]) · '관측성' = 평탄 논증 + 합성 EKF 한 번 — **9 % 는 편향이었고, 비교 기준(전체 모형)은 인쇄 식의 항 하나를 빼고 계산됐다**

`raw/papers/kim2019_assb-ekf-soc-estimation-weak-observability.md` (Kim · Lin · Abbasalinejad · Kim · Chung 2019 *Electrochim. Acta* 317, 663 — 12호 [62] · 37호 [21] · 4차 묶음 파일 59 · 원장 §2 공백 1번 후보).

- **위 표의 어느 줄인가**: 표 2 = **모델 불일치 민감도(27호 줄)의 OAT 판** — 출력 = 전체(모형 1) ↔ 축약(2 · 3 · 4) 전압 차의 Max · RMS · 흔든 것 = 매개변수 다섯 ×1/100 · ×100(L 만 ±27 %) · 동기 문장은 "it has been widely used in studies on assessing parameter identifiability or estimability [19,20]" — 식별성 계산 0. 관측성은 새 줄(상태 관측성 논증 + 합성 추정기 실행).
- **OAT 표의 '같은 값' 은 첫 순간일 수 있다**: 펄스 모형 3 최대 0.0027 V 가 열 행 중 일곱 행에 같다 — `[재현]` SOC 0.99 · 10C 켜는 순간 α 0.6 ↔ 0.5 의 η_ct 차 2.68 mV(그림 6 첫 점 t = 0.009 s +2.68). 매개변수를 흔들어도 안 변하는 최대는 그 매개변수가 그 순간에 안 보인다는 뜻이지 견고하다는 뜻이 아니다.
- **흔들지 않은 매개변수가 단순화를 정한다**: 단순화 (1)(SE 안 생성 · 재결합 무시)의 오차는 k_r 에 매달린다 — `[재현]` 10C M1 − M2 0.49 / 0.19 mV(인쇄 k_r — 표 2 ✅) → ×100(91호 그림 일치 값) 15.33 / 6.77 mV · 표 2 에 k_r · δ 행 0. 그리고 단순화 (2) 가 깨지는 k_pos ×1/100(86.9 mV)은 "not physically realistic" 로 배제 — 열화로 A·k_pos 가 줄어드는 방향이다.
- **비교 기준의 항 누락**: 그림 3 η_mt 는 식 (14) 둘째 항(−∫E)만이다(그림 4 단면으로 ±0.3 mV · Nernst 항 −1.0 … −18.4 mV 없음) — 식 (14) 그대로면 모형 4 오차 RMS 13.0 → 27.6 mV(우리 재풀이 · 표 2 인쇄 14.3). 축약 오차 표는 기준 모형이 인쇄 식대로인지 먼저 본 뒤 옮긴다(98호 재풀이 처방의 항판).
- **관측성 — 계산 대신 증폭 지도**: `[재현]` 식 (22) \|dE/dSOC\| 최소 0.072 V/SOC(SOC 0.28) · SOC 0.1–0.4 중앙 0.126 ↔ 0.4–0.99 0.658 · 그림 9 Δη_total ÷ 기울기 = 그림 7 SOC 오차(EKF4 800 s −0.084 ↔ −0.087) — '약한 관측성' 은 오차의 원천이 아니라 모형 불일치의 증폭기였다. 셋째 줄의 입력 설계판(34호)과 달리 이 편의 처방은 모형을 키우는 것(EKF3)이었고, 미래 과제(궤적 창)는 분산만 줄인다([[data-window-identifiability]] 99호 절).
- **(주) 기준으로 본 결론** — "the simplified models have sufficient accuracy in the voltage prediction": ① 무엇의 순위 = 축약 오차 Max ② 시간 기준 = 방전 끝 · 켜는 순간(펄스 M3) ③ 조건 = 10C · 신품 · 매개변수 다섯 OAT ④ — ⑤ 동역학 손잡이 = F·A·k_pos 한 곱(×1/100 배제).
- **후보 처방(결정 대기 — 새 판단 거리)**: 처방 27(아래) — 격상은 결정하지 않는다.

## ★★★ 100호 — 스윕 0 · 묶음은 세웠고 식별은 0: 축약 모형(ROM)의 'less than 2.6 mV' = 같은 매개변수 한 벌의 원 PDE 대비 UDDS RMSE — **전압이 4.6 mV 로 맞을 때 성분(η_d)은 76.3 mV 어긋났고, 차수 선택 근거 그림의 '원 모형' 곡선은 해석식의 응답이 아니었다**

`raw/papers/deng2021_assb-reduced-order-model-pade-polynomial.md` (Deng · Hu · Lin · Xu · Li · Guo 2021 *IEEE Trans. Transp. Electrif.* 7(2), 464 — 26호 [16] · 37호 [29] · 4차 묶음 파일 60 · 원장 §2 공백 1번 후보의 마지막 ASSB 편).

- **위 표의 어느 줄인가**: 흔드는 것 0 — 원 PDE(COMSOL 5.4a) ↔ ROM(Laplace → 3차 Padé → 포물선 · 삼차식)의 출력 차(RMSE · MaxAE — 표 IV · V)를 **한 매개변수 점(표 I)** 에서만 잰다 = **모델 불일치 민감도(27호 줄)의 한 점판**(기울기 · 매개변수 흔들기 0). `sensitiv*` 0 · `identif*` 1(Fabre 소개 "to identify some model parameters") · 매개변수 추정 0.
- **묶음은 지면이 세웠다 — 목록 · 식별은 0**: `[인쇄]` "The coefficients of the transfer functions can be explicitly derived from the electrochemical parameters." · "which makes it a lumped-parameter model" — `[재현·대수]` 계수는 묶음 다섯(1/(A·F·L_p) · L_p²/D_Lis · L_e/(4A·F·D_Li⁺) · L_e²/D · A·k_pos)으로만 쓰이고, 양극 묶음 셋은 (A, L_p, D_Lis, k_pos) → (λA, L_p/λ, D_Lis/λ², k_pos/λ) 에서 그대로다([[spm-grouped-parameter-identifiability]] 100호 행). 26호가 본 "식별 대상이 되는 형태" 는 맞고, 그 꼴로 식별한 것은 0 이다.
- **출력 불일치 ≠ 성분 불일치**: 표 IV 10C V MaxAE 4.6 ↔ η_d 76.3 mV — V = Eeq(θ_s) + η(식 16 둘째 줄)라 η_d 오차가 Eeq(θ̄) 의 같은 크기 반대 부호 오차와 상쇄된다(`[재현·대수]`). 27호 줄의 `d = Y_hi − Y_lo` 를 출력 하나로 재면 성분의 불일치가 사라진다 — 축약 모형을 성분 라벨 · truth 로 쓸 때는 성분별 d 를 따로 잰다.
- **'less than 2.6 mV' 의 지표 · 위치 · 조건**: 초록 ↔ 표 IV UDDS RMSE 2.60 · MaxAE 40.5 mV(방전 끝 — `[도표·벡터]` 그림 8 36.7 mV @2,722 s) · 조건 = 축척 UDDS 두 번(2,742 s · −3.88 … +8.65C — 축척 방법 미인쇄) · Δt 1 s · α_pos 0.5 · r 무시 · 같은 매개변수 한 벌 · 신품.
- **흔들지 않은 매개변수가 축약을 정한다(처방 27 ③ 의 상속판)**: r 무시의 근거 = "The results of [9] suggest that ignoring the r term will not cause a large voltage error in the considered models"(99호 표 2 — 인쇄 k_r · 10C 에서의 결론) · `[재현]` 10C r 무시 오차 RMS 0.40 · 최대 0.75 mV(인쇄 k_r) → 14.85 · 23.94 mV(k_r ×100 — 91호 그림 일치 값). 앞 편 OAT 가 흔들지 않은 매개변수가 뒤 편 축약의 정당화로 넘어갔다.
- **차수 근거 그림의 기준 곡선**: `[재현]` 그림 2 의 PDE 곡선은 정확한 coth 응답(±0.13 dB · ±0.06°)이지만 그림 3 의 'PDE' 곡선은 식 (22) 의 정확한 응답이 아니다(632 rad/s 499 ↔ 99 dB · 위상 진동 ↔ −45° 수렴 — 원인 미확정) — 본문은 그것을 PDE 의 성질("diverges … oscillates")로 읽고 3차를 골랐다 · 3차 유효 대역(1 dB · 5°) 양극 0.19 · 전해질 0.056 Hz ↔ 인용 기준 "less than 2.5 Hz [19]".
- **비교 기준의 항 — 99호와 반대로 들어 있다**: 원 PDE 는 식 (9) 그대로 Nernst 항 포함(그림 7(a) 재풀이 ±0.05 mV · 빼면 최대 19.3 mV) — 같은 계열 · 같은 표의 99호 그림(둘째 항만)과 다른 구현이다(처방 27 ① 의 반대 방향 표본).
- **(주) 기준으로 본 결론** — "Compared with the original PDE-based model, the voltage errors of the proposed ROM are less than 2.6 mV": ① 무엇의 순위 = 출력(V) 오차 RMSE(최대 · 성분 오차는 표에만) ② 시간 기준 = 전 구간 평균(최대는 방전 끝) ③ 조건 = 같은 매개변수 한 벌 · 10C · 축척 UDDS · 신품 ④ 기준 = COMSOL 원 PDE(인쇄 식 그대로) ⑤ 동역학 손잡이 = F·A·k_pos 한 곱(α 0.5 asinh).
- **후보 처방(결정 대기 — 새 판단 거리)**: 처방 28(아래) — 격상은 결정하지 않는다.

## ★★ 101호 — 스윕 = 해리도 δ 한 축(그림 11 · 12 — 선택 값 위) · 처방 = 닫힌 꼴 비 하나(식 42): **'t₊ 를 실험으로 얻는 도구' 는 완전 해리 · 정상 조건의 구조 명제이고 같은 지면의 해리 판에서 깨진다 — 그리고 지면의 그림들은 한 매개변수 표로 닫히지 않는데, 그 차이를 가르는 것은 정상 값이 아니라 시간 경과다**

`raw/papers/danilov2008_liquid-electrolyte-transport-electroneutrality-dissociation.md` (Danilov · Notten 2008 *Electrochim. Acta* 53, 5569 — ⚠ 액체 전해질 모형 원전 · ASSB 아님 · 26 · 91 · 98 · 100호 SE 수송 식의 유도처 · 4차 묶음 파일 61).

- **위 표의 어느 줄인가**: 흔드는 것 = 해리도 δ 하나(1 · 0.85 · 0.70 · 0.6569 — 그림 11 · δ 0.65–1.00 — 그림 12) · k_a · D_LiPF₆ 는 "have to be chosen" 선택 값 고정 = **OAT 한 줄(26호 줄)의 모형판** · `sensitiv*` · `identif*` · `estimat*` · `fit` 0 · 매개변수 추정 0.
- **구조 명제 둘은 지면에 있다 — 그러나 식별성이라 부르지 않는다**: `[인쇄]` 식 (37) "ηss … only depends on DLi+ and is independent on DPF6−"(정상 관측의 구조적 비식별 방향) · 식 (42) "delivers a nice tool to obtain this value experimentally"(닫힌 꼴 역문제). `[재현]` 식 (42) 는 해리 판에서 깨진다 — δ 0.8 · 50 min 낙차/정상 0.445 ↔ t₊ 0.4 · 자기 측정(그림 9)에는 적용 0(선 낙차/정상 ≈0.48–0.50 ≈ t₊ 0.5).
- **스윕 결론은 고정한 선택 값에 매달린다**: "migration is of major importance in poorly dissociated electrolytes" · 한계 δ 0.6569 — `[재현]` 중성 LiPF₆ 를 고정(D_LiPF₆ → 0)하면 같은 50 min 한계 δ 가 0.6576 → 0.923 — 스윕이 흔들지 않은 매개변수(D_LiPF₆)가 결론의 자리(한계 해리도)를 정한다(처방 27 ③ 과 같은 축).
- **스윕 그림의 매개변수 상태**: `[재현]` 그림 11(B)–(D) · 12 · 인쇄 x 0.9017 · '61 %' · 한계 δ 는 L 2.9×10⁻⁴ 로만 닫히고(±1–3 mV · 0.6576), 같은 그림 11 의 (A) · 그림 8 은 표 1 L 2.8×10⁻⁴ 로 닫힌다 — 스윕 축(δ) 밖의 매개변수가 그림 사이에서 바뀌었다(인쇄 0). 같은 x 의 한 매개변수 변경 넷 중 그림 11(C) 시간 경과는 L 만 0.83 mV 로 닫는다 — 완전 해리라면 정상 값은 x 하나라 넷이 같다(그림 11(A) 조건 49.5 min 152.1–152.2 mV).
- **(주) 기준으로 본 결론** — "the transference number of Li-ions only determines the instantaneous voltage drop and this facilitates the way to perform simple experiments to determining the transference numbers": ① 무엇 = 비 η_down/η_ss(낙차 자체는 t₊ 와 농도 비에 같이 매임) ② 시간 기준 = 정상 도달 뒤 끊는 순간 ③ 조건 = 완전 해리 · 이상 묽은 용액 · 일정 D ④ 기준 = 이 편 모형 ⑤ 손잡이 = t₊ = D₊/(D₊ + D₋)(Nernst–Einstein 형).
- **후보 처방(결정 대기 — 새 판단 거리)**: 처방 29(아래) — 격상은 결정하지 않는다.

## ★★ 102호 — 스윕 = 막 셋(두께 = 배향) · 방법 넷 · 조성 · 추정 0 · 판정 = '어느 방법이 맞는가' 를 σ 대조 하나로: **측정 D̃ 가 방법 · 역모형 · 미인쇄 기하 가정의 라벨이고(같은 막 시간 상수 ×≈50–430), 방법 순위를 정한 환산은 종 기준이 어긋나 1/δ 배다**

`raw/papers/xie2008_lco-thin-film-orientation-diffusion-gitt-pitt-eis.md` (Xie · Imanishi · Matsumura · Hirano · Takeda · Yamamoto 2008 *Solid State Ionics* 179, 362 — ⚠ 액체 셀 LCO 박막 측정 · ASSB 아님 · 26호 [23] · 98호 [31] · 4차 묶음 파일 62).

- **위 표의 어느 줄인가**: 매개변수 추정 0 · `sensitiv*` 1(이력 민감) · `identif*` 1(D̃ 를 'identify' 하는 방법) — 이 편의 '스윕' 은 **실험 설계 축 셋**(막 두께 = 배향 · 방법 · 조성)이고, 출력은 각 방법 역모형의 D̃ 다. 표 밖의 도구 — **'측정 대체' 의 측정 쪽**(93호 줄 — 측정 입력의 역모형)과 같은 축.
- **역모형 선택이 측정값을 정한다**: `[재현]` 네 닫힌 꼴은 미인쇄 상수 한 벌(S 0.64 · Vm 19.34 · C 1/Vm · 298 K · 그림 5 dE/dδ)로 저자 그림을 다시 내지만(±0.03–0.07 dex · CV 1.4 %), 선택 둘이 같은 그림에서 값을 움직인다 — Warburg σ 를 Z′(3.43) ↔ −Z″(6.01 Ω s^-½)로 ×3.1 · PITT 창 100–500 ↔ 1500–2000 s 로 ×2.7. 방법 사이는 ×10²–10³ · 같은 막 · 같은 전위의 전 막 τ 가 EIS 8–30 s ↔ GITT · PITT 1400–3400 s(`[재현·가정]`).
- **판정 처방의 자기 일관성**: '가장 믿을 만한 방법' = σ(Nernst–Einstein 환산) ≈ σ(정제 DC) — `[재현]` 환산의 ϕ(δ 기준) × C(Li 상수) → 1/δ 배(고치면 Li0.65 세 칸이 같이 맞고 Li1.0 둘 다 안 맞음) · 기준 DC 정제는 자기 σ 로 환산한 이완(≈14–18 일)을 관측(≈30 s)이 닫지 못함 · 조성마다 시료 하나.
- **(주) 기준으로 본 결론** — "PITT is the most reliable technique for the determination of the Li–ion chemical diffusion coefficient in LiCoO2 thin film": ① 무엇 = 액체 셀 · 세 막 · 두 조성의 σ 일치 ② 시간 기준 = PITT '직선 구간'(미인쇄 — 창에 따라 ×2.7) ③ 조건 = room temperature(미인쇄) · 정제 50–80 °C 외삽 ④ 기준 = 정제 DC 하나 ⑤ 손잡이 = σ 환산 규약(1/δ).
- **후보 처방(결정 대기 — 새 판단 거리)**: 처방 30(아래) — 격상은 결정하지 않는다.

## ★★ 103호 — 스윕 = 대칭 인자 넷 OAT(0.3–0.7 · 여덟 값 · M = RMS(G/X)) + 설계 스윕 Ω · E_sp · l_sp · 추정 0: **'Sensitive · Not sensitive' 의 기준점에서 응력 → i₀ 결합이 꺼져 있고(γ = β), 지표(충전 끝 용량)는 평형 항(V_str)만 보며, 인쇄 γ 민감도는 인쇄 식으로 재현되지 않는다**

`raw/papers/shao2022_thin-film-assb-mechano-electrochemical-stress-partial-molar-volume.md` (Shao · Shao · Sang · Liu 2022 *J. Electrochem. Soc.* 169, 080529 — 무공극 박막 ASSB 역학–전기화학 결합 모형 · 실험 0 · 26호 [14] · 4차 묶음 파일 63).

- **위 표의 어느 줄인가**: OAT 한 줄(26호 줄)의 모형판 — 흔드는 것 = β^s1 · β^s2 · γ^s1 · γ^s2 하나씩(0.3–0.7 · 여덟 값 미인쇄) · 지표 g = "the capacity of the cell"(충전 끝 SOC) · M = √((1/k)Σ(G/X)²)(식 68–70 · Jiang [46]) · 분류 'Sensitive · Very sensitive · Not sensitive' 문턱 0 · `identif*` · `estimat*` · `fit*` 0.
- **기준점에서 결합이 꺼져 있다**: `[재현·대수]` 식 (24)–(25) 의 응력 인자 exp((γ − β)(Ωσ^h − Ω_Li⁺σ^h_SE)/RT) 는 표 I γ = β = 0.5 에서 ≡ 1 — 기준 그림 전부에서 '응력이 계면 동역학을 바꾼다' 는 결합은 0 이고, γ 스윕은 그 결합을 처음 켜는 시험이다.
- **인쇄 민감도의 재현**: `[재현·가정]`(층 평균 닫힌 꼴 · T 298 K · i₀ mol L⁻¹ · x_n 0.30–0.70 · 0.5 제외) β^s1 2.763 × 10⁻² · β^s2 1.452 × 10⁻¹(인쇄 2.77 × 10⁻² · 1.43 × 10⁻¹ ✅) · **γ^s1 2.02 × 10⁻² · γ^s2 1.52 × 10⁻² ↔ 인쇄 6.91 × 10⁻³ · 1.99 × 10⁻¹¹** — 식 그대로면 γ 는 β^s1 과 같은 자릿수('Sensitive' 쪽) · 인쇄 'Not sensitive' 는 구현(특히 s2 응력 항)이 지면과 다를 때만 나온다.
- **설계 스윕의 결론은 고정한 가정에 매달린다**(처방 27 ③ 과 같은 축): Ω 스윕의 용량 효과(−39 % · +1.72 %)는 면내 강체 구속(식 37)이 만든 V_str 에서 오고 — `[재현]` 면내 자유면이면 Ωc 0.834–5 모두 SOC_cut 0.9899 — 스페이서 스윕은 σxx(SE 강성 99.87 %)만 움직이고 V · 용량은 그대로다.
- **(주) 기준으로 본 결론** — "The most sensitive parameter is the symmetry factor of the anode/SE interface … capacity is less sensitive to the two mechanical symmetry factors": ① 무엇 = 충전 끝 용량의 상대 변화 ② 시간 기준 = 4.03 V 도달 ③ 조건 = 0.1 mA cm⁻² · 박막 · T(인쇄 333 ↔ 계산 298 K) ④ 기준 = 이 편 모형(기준점 γ = β) ⑤ 손잡이 = 대칭 인자 하나씩.
- **후보 처방(결정 대기 — 새 판단 거리)**: 처방 31(아래) — 격상은 결정하지 않는다.

## ★★ 104호 — 스윕 = 네 손잡이 OAT(L_c · L_e · C_max · D_Lis) + 율 셋 · 추정 0 · `sensitiv*` 0: **26호가 'sensitivity = sweep' 관행의 표본으로 지목한 편 — 관행 ✅ · 낱말 ❌(이 편은 'parametric study' 라 부른다). 그리고 '검증' 은 사이클마다 다른 모형 상태(바꾼 것 인쇄 0)이고, 쓸기 그림은 인쇄 기하로 나오지 않는다(그림 8 = 확산 길이 ≈1 µm)**

`raw/papers/ansah2021_assb-fem-parametric-sweep-thickness-diffusivity.md` (Ansah · Shin · Lee J.-S. · Cho 2021 *Electron. Mater. Lett.* 17, 532 — InLi \| Li₆PS₅Cl \| LiCoO₂ 1D FEM(COMSOL 5.4) · 실험 = 다른 연구실 제공 미출판 자료 · 26호 [9] · 4차 묶음 파일 64).

- **위 표의 어느 줄인가**: **첫 줄(설계 민감도 — OAT 대역 쓸기)** — 흔드는 것 = L_c 100–600 µm(여섯 값 · 그림 3) · L_c × 율 0.1 · 0.5 · 1 C(그림 4 · 5) · L_e 200–900 µm(다섯 · 그림 6) · C_max 2130–2530 mol m⁻³(일곱 · 그림 7) · D_Lis 10⁻¹⁸–10⁻¹¹ m² s⁻¹(십년 여덟 × 율 둘 · 그림 8) · 다른 손잡이는 표 1 · 기준점 고정 · 조합 실행 0(L_c × 율 만 격자) · 출력 = 2.5 V 차단 용량(mAh g⁻¹) · 본문 `sensitiv*` · `identif*` · `fit*` · `estimat*` 0 · `valid*` 10 · `Pearson` 1. 26호 원장 행 '같은 sensitivity = sweep 관행의 표본' 은 **관행 ✅ · 낱말 ❌** — 이 편은 쓸기를 'comprehensive parametric study' 로만 부르고, 'Sensitivity Analysis' 라는 이름표는 26호 표 1 이 붙인 것이다(26호 digest 전사에 [9] 행의 칸 값은 없다).
- **쓸기 그림을 겹쳐 본 것(처방 2 — 공짜 야코비안)**: `[도표·화소]` 그림 7(C_max)은 처음 ≈10 mAh g⁻¹ 의 전압을 안 움직이고 끝 용량만 움직인다(직선 0.04357·C_max − 9.48 — 원점 비례 아님) = **용량 스케일 열** · 그림 8(D_Lis)은 0.1 C 에서 10⁻¹⁵ 위로 **0 열**(91.60 고정)이고 아래로 용량 ∝ D · 그림 3(L_c)은 용량 ∝ L_c(오목 — 600 µm 가 100–300 µm 직선 외삽의 −14.7 %). 평면 판이면 D 와 L² 는 한 묶음(τ = D·t/L²)의 두 축인데, 그림 8 이 주는 길이(≈1 µm)와 그림 3 의 L_c(100–600 µm)가 다르다 — **두 쓸기는 같은 묶음 위에 있지 않다**(구현 미인쇄).
- **인쇄 식 · 표의 재풀이**: `[재현·가정]`(평면 판 · 한쪽 정전류 유입 · 표면 최대 농도에서 차단 — 용량 상한) 인쇄 기하 L_c 200 µm · D 1.76×10⁻¹⁵ 이면 L²/D = 2.27×10⁷ s(263 일) · 0.1 C 이용률 0.124 % · 용량 ∝ 1/L(그림 3 은 ∝ L) · 1 C/0.1 C 0.10(그림 4(a) 0.957) — 그림 8 을 역산하면 평면 등가 확산 길이 0.96–1.04 µm(0.1 C 네 점). 그림 8 의 기준 점선은 log D −14.28(5.2×10⁻¹⁵ — 표 1 값의 ×3.0).
- **'검증' 의 층**: 모형에 열화 항 0 · 그림 2 모형 곡선 넷(1 · 5 · 10 · 20 사이클 · 끝 91.9 · 81.1 · 65.8 · 52.45 mAh g⁻¹) ⇒ 사이클마다 다른 매개변수 상태(무엇을 · 몇 개를 — 인쇄 0)이고, 처음 전압이 60–130 mV 낮아지는 꼴은 C_max(용량 스케일) 하나로 안 나온다(`[해석]` — 저항형 손잡이가 같이 움직였다) · 실험 = 다른 연구실(사사)의 미출판 자료 · 지표 = 평균 R²(Pearson) 0.96 — 상관은 상수 이동 · 척도에 불변이라 기준 전위(InLi ↔ Li ≈0.62 V) · 질량 정규화의 차를 못 본다. 쓸기 세 그림(3 · 4 · 7)의 기준점 끝 용량 91.9–92.05 = '1 cycle' 상태 하나.
- **같은 조건 값 · 기준**(`[도표·화소]`): 100 µm · 0.1 C 가 그림 3 · 5 48.4 ↔ 그림 4(a) · 본문 46.13(−4.7 %) · SE 두께 '22.67 %' = (92.02 − 75.01)/75.01 — 기준이 바꾼 뒤(900 µm) 값이다(바꾸기 전 92.02 기준이면 −18.49 %) · '+41.30 %' 는 바꾸기 전 기준 · 비용량(mAh g⁻¹)의 분모(고정 질량 ↔ 두께에 비례하는 질량) 미인쇄.
- **(주) 기준으로 본 결론** — "the cathode diffusivity is a performance-limiting factor of the SSB": ① 무엇 = 차단 용량의 변화(0.1 C 10⁻¹⁵ 위 포화 · 1 C 10⁻¹⁴ 위 +1.6 %) ② 시간 기준 = 2.5 V 차단 ③ 조건 = L_c 200 µm(표 1 — 그림이 요구하는 길이는 ≈1 µm) · 0.1 · 1 C ④ 정의 = "the factor(s) that constrains the performance of the cell"([7] — 문턱 0) ⑤ 손잡이 = D 하나(같은 묶음의 길이 · 율은 따로 흔들지 않음) — 1 C 기준점(점선)에서 용량이 포화값의 ≈95 %(86/90.4)라 '한계' 판정은 기준점 선택에 매달린다.
- **후보 처방(결정 대기 — 새 판단 거리)**: 처방 32(아래) — 격상은 결정하지 않는다.

## 우리 쪽 연결

- `degradation-degeneracy/` 는 **"곡선이 맞는다 ≠ 파라미터가 맞다"** 를 합성 truth 로 채점하는 프로젝트다. 26호의 "RMSD 0.11 → 0.06 V + 문헌과 5 % 이내" 는 그 실패 모드를
  검사하지 않은 검증의 **야생 표본**이고, `D_e⁻` 가 그 실패의 실례다. (우리 쪽 수치는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본 — 여기 옮기지 않는다.)
- 폭 측정기([[near-optimal-set-width-measurement]])를 26호 모델에 걸면 `D_e⁻` 는 **한쪽이 열린 구간**으로 나와야 한다(`[추론]`, 코드 비공개라 미실행).

## 처방 (논문을 읽을 때)

1. 제목·표의 "sensitivity analysis" 를 보면 **위 표의 어느 줄인지** 먼저 적는다(`Fisher`·`Hessian`·`profile`·`confidence`·`identifiab` 지문).
2. 추정 논문이 스윕도 인쇄했으면 **스윕 그림끼리 겹친다** — 평행 · 0 열을 찾는다.
3. 0 열 · 평행 열 파라미터의 **적합값 ÷ 문헌값**을 본다. 여러 좌표가 **같은 비율**이면 시작점 근방 정지 신호(26호 7/10 이 ×1.0500)다.
4. 스윕이 **추정 데이터의 조건**(율 · 온도)에서 돌았는지 본다 — 26호는 1C(추정 데이터에 없음)에서 돌렸다.
5. (27호) **Sobol 을 보면 출력이 데이터인지 설계 KPI 인지 먼저 적는다.** 전차 지수 ≈0 은 그 출력에 대한 비식별의 충분조건으로 쓰되, 대리모형 검증 · CI 출처를 확인한다.
   그리고 **Sobol 의 교호작용 지수는 보상(compensation)을 재지 않는다** — 곱 쌍의 짝을 흔들지 않았으면 곱은 아예 나타나지 않는다(27호는 `κ` 만 흔들고 `ε/τ` 는 고정).
6. (27호) **모델 비교 논문의 "상수 차이 = 보정 가능" 은 구조 오차가 파라미터로 흡수되는 자리다.** 그 상수의 크기를 **알려진 구조량**(연결 분율 `1 − u` 등)과 대조한다.
7. (28호) **식별성을 한 논문이면 식별 집합의 목록을 먼저 적는다.** 용량 스케일(`Q_th`) · 정렬(`x⁰`) · OCV 곡선이 **입력**이면 그 논문은 모드 분해의 유일성을 말하지 않는다.
   그리고 사후 보정 손잡이(28호 ×0.78)가 **어느 묶음**에 걸리는지 본다 — 식별 집합에서 뺀 축이면 그 보정이 그 축의 추정이다.
8. (29호) **적합 논문이면 파라미터 dependency/상관 행렬을 SI 에서 찾는다** — 둘째 줄의 수치다. 찾았으면 **진단이 경고한 셀이 결론에 쓰였는지** 추적한다(29호는 sc90 을 빼고 같은 문제의 sc84 로 결론을 냈다). (29호 SI 보강) 찾으면 ① 전 셀을 전사해 **본문이 경고한 셀 수와 대조**하고 ② 1 에 붙은 파라미터를 **그 셀의 물리 상한**(충전 전하 · Li 재고)과 대조하고 ③ **표 ↔ 그림 값**이 같은지 본다 — 29호는 ① 1 ↔ 3 ② 두 셀 상한 밖 ③ 두 셀 불일치.
9. (30호) **교과서 선형화 추출(b 값 · Randles–Ševčík · Dunn)이면 식별성 이전에 두 가지를 본다** — ① 같은 데이터가 식의 전제(b = 0.5 · 원점 통과)를 만족하는가 ② 인쇄된 값과 **라벨**(산화/환원 · 계)이 그 논문 자기 그림에서 다시 구한 값과 맞는가. 30호는 ② 에서 뒤집혀 있었다.
10. (35호) **"calibrated uncertainty" · "confidence interval" 을 보면 대상이 예측(스칼라 목표의 오차)인지 파라미터(해 집합)인지 먼저 적는다.** 예측이면 Q4 근거가 아니다. 그리고 적중률 점수(`C_score`)는 **목표와의 거리**로 읽는다 — 90 % 목표에서 100 은 과소 확신이다. 이름도 대조한다: "α-accuracy · β"(예측 지표) ≠ 우리 α·β(전극 스케일 · 오프셋).
11. (36호) **"posterior" · "parameter uncertainty" · "epistemic" 을 보면 ① 무엇의 파라미터인지(물리 ↔ ML 가중치) ② 데이터를 늘리면 줄어드는 폭인지(실제적) 아닌지(구조적) ③ 공분산을 보고했는지(평균장 근사면 상관이 지워진다)를 적는다.** 셋 다 아니면 Q4 근거가 아니다.
12. (37호) **OAT 스윕의 "둔감 · minimal" 을 보면 ① 출력이 용량(설계 KPI)인지 전압(데이터)인지 ② 그 파라미터와 곱으로만 들어가는 짝이 식에 있는지 ③ 짝이 적합에서 풀렸는지를 적는다.** 짝이 풀렸고 스윕 대상이 출처 없이 고정됐으면 그 값은 데이터가 정한 것이 아니다(37호 `A_eff` 0.4938 ↔ `k_p`).
13. (49호) **"방법들이 시간 척도를 맞추면 일치한다" 를 보면 ① 일치하는 것이 총량인지 성분인지 ② 시간 ↔ 주파수 대응 규약과 그 대역의 \|Z\| 기울기(분해능) ③ 진폭이 같은지 ④ 적합된 직렬 파라미터가 여기 대역 위쪽 끝의 \|Z\| 와 같은지를 적는다.** 같으면 그 파라미터는 물리 성분이 아니라 대역 끝의 이름이다.
14. (54호) **"unfeasible · not separable" 을 인쇄한 모델 편이면 ① 가르는 채널이 모델 안에 있는지(절편 · 온도 · 진폭) ② 그 채널이 측정 대역 · 조건 안에 있는지 ③ 교정 단계에서 같은 분할을 입력으로 정하지 않았는지를 적는다.** 54호: ① 있다(고주파 절편) ② 없다(`f_C,B` ≈ 장비 상한) ③ 정했다(`σ⁰` 문헌 윗끝).
15. (75호) **"X-limited" · 영역 지도를 보면 ① 판정 규칙(스윕 평탄 → 부재 ↔ 저항 크기 → 한계) ② 무엇의 순위 · 문턱인지 ③ 값의 시간 기준 ④ 조건(두께 · 전류 · 방향) ⑤ 저항 정의의 가중(전류 가중 ↔ 두께 단순 평균) ⑥ 동역학 손잡이가 곱의 어느 쪽인지(면적 ↔ `k` · `c_e`)를 적는다.** 그리고 스윕 포화를 "다음 한계로의 전이" 로 읽은 곳에서는 포화값이 **이용 가능 재고의 상한**(AM 기준 용량)에 닿았는지 본다 — 75호 40 · 60 wt% 는 닿았다.
16. (76호) **"A 무늬는 B 원인" 배정을 보면 ① 가를 대상으로 적은 후보를 전부 흔들었는지(76호 `i₀` 0 회) ② 흔든 배수가 문헌값 복귀인지(76호 `D` ×10 = 문헌값) ③ 한 손잡이가 다른 무늬도 움직였는지(비대각 — 76호 S17) ④ 입력 파라미터의 무차원 영역(Wa 등)이 결론을 미리 정하지 않았는지를 적는다.** ④ 가 정했으면 "X 가 한계가 아니다" 는 시험이 아니라 입력이다.
17. (77호) **모형 ↔ 실험 "good agreement" 를 보면 ① 정규화 척도(완전 용량 · 닻)의 출처 — 실험 최대값이면 그 근처 점은 자동으로 맞는다 ② 관측의 수(충전 · 방전 · 율 · 사이클) ③ 닻에 걸린 점을 뺀 나머지 점 수와 차 ④ 대안 한계(전자 · 수송 · 동역학)를 흔든 시험이 있는지를 적는다.** 77호: ① 실험 최대값 155 ② 첫 방전 하나 ③ 여섯 점 RMS 8.5 mAh g⁻¹ ④ 0 — 그리고 첫 충전에 대면 두 점이 반례다.
18. (82호) **실험 스윕(한 손잡이 여러 수준)에서 "Y 가 성능을 정한다" 상관을 보면 ① 손잡이가 같이 움직인 양의 목록(공극 · 면적 · 균질도 · 두 σ) ② 경쟁 설명이 다른 예측을 하는 표본이 있는지(비 > 1 등) ③ 측정 방법을 바꿔도 순서가 유지되는지 ④ 제안 기구의 크기 검사(옴 강하 ↔ 관측 간격)를 적는다.** 82호: ① 다섯 ② 0 개 ③ 아니다(AC ↔ DC 로 L ↔ XL 뒤집힘) ④ 없다 — `[재현]` 작은 몫.
19. (83호) **모형 편이 두 손잡이의 OAT 결과를 "설계 지침" 으로 합쳤으면 ① 각 스윕의 다른 손잡이 고정값 ② 조합 run 유무 ③ "둔감" 한 손잡이가 전기화학에 닿는 경로가 식에 몇 개인지(가정으로 뺀 기구 포함) ④ 문턱의 무차원 조건(전류 · 두께) ⑤ 결론이 쓴 기준(수명 ↔ 총 균열 등)이 자기 다른 기준과 순위가 같은지를 적는다.** 83호: ① 미인쇄 ② 0 ③ 하나(ϕ_mech — CAM\|SE 박리는 가정으로 제외) ④ 전류 미인쇄 ⑤ 다르다(파괴 사이클 fine > coarse ↔ 총 균열 coarse < fine).
20. (85호) **온도 기울기(Ea)로 곱(R = ρl/A · `j₀·A_eff`)의 한쪽을 배정한 편이면 ① 인쇄 Ea 를 인쇄 표로 재적합(log 밑 · 형식 · 점 수 · 신뢰 낮은 점) ② "Ea ↑ ⇒ ρ ↑" 에 필요한 앞인자 동일 가정의 인쇄 여부 ③ R·C 곱(τ = ρε · 면적 무관)이 같은 방향을 주는지 ④ A 의 독립 관측 유무 ⑤ 배정 차이의 크기 ↔ 적합 폭을 적는다.** 85호: ① 7/8 ln 10 누락 · 1/8 점 뒤바뀜 ② 0 ③ τ ×2.2 같은 방향 ④ 0 ⑤ 7 meV ↔ ≤27 meV.
21. (86호) **GITT 로 "피복률 · 접촉 면적 · 활성 면적" 을 뽑은 편이면 ① `D` 의 값 · 출처(액체셀 · 문헌 · 같은 지면) ② 펄스 SOC · ΔEs · ΔEt 판독(IR 계단 제외 여부) ③ 기준 면적(BET · 기하)을 찾고 ④ 같은 지면의 첫 충전 상한(코팅 · 공정 쌍의 첫 충전이 같으면 정적 면적 차 ≈0)과 교차한다 — ①–③ 중 하나라도 없으면 그 값은 분극 비의 이름표로 옮긴다(65 · 29 · 86호).**
22. (92호) **"system identification · BLA · 블록 지향" 을 보면 ① 식별된 값 · 불확실도가 인쇄됐는지 ② "분산" 이 무엇의 분산인지(FRF 잡음 · 왜곡 ↔ 매개변수) ③ 블록 사이 정규화(이득 · 오프셋)를 적었는지 — 없으면 블록별 모양 · 출력 좌표 꺾인점은 정규화 의존 ④ 구조를 바꿔도 블록 모양이 유지되는지 ⑤ 진폭 수준 수 · 학습 ↔ 검증 신호 구분 · 적합도 백분율의 정의를 적는다.** 92호: ① 0 ② 잡음 · 왜곡(인쇄 식대로면 ×3.13) ③ 0 ④ 뒤집힘(H 단독 확장 ↔ H-W 포화) ⑤ 진폭 하나 · 비선형 검증 신호 미인쇄 · 정의 0.
23. (93호) **"적합하지 않았다 · 입력을 쟀다(none fitted · measure reliable inputs)" 나 "단순 · 입력이 적다" 를 신뢰 근거로 쓴 편이면 ① 측정 입력마다 역모형과 그것이 요구한 다른 입력(면적 · 확산 길이 · ε 규약 · 문헌 OCV)을 적고 ② 이산 선택(PSD 절단 · 입력 세트 · 수작업 연결)을 실험 일치로 했는지 ③ 같은 지면 · 같은 저자 앞 편에서 다른 입력 가족이 같은 곡선을 냈는지 ④ 대안 가설 단계가 실제로 수행됐는지 ⑤ "단순" 의 척도(물리 입력 · 모형 선택 · 적합 매개변수 · 계산비)를 적는다.** 93호: ① 0(처방만) ② 56호 D2 ③ 56호 그림 7(상수 `{D₂, j₁}` 가 0.5 C 에서 더 맞음) ④ 그림 1 "(not done)" ⑤ 물리 입력만 셈(1호 모형 선택 다섯은 안 셈).
24. (95호) **재매개화 · 묶음 · 감도 순위 편("원 N 개 → M 개 → 추정 K 개")이면 ① 남은 묶음이 식에 단독으로 나오는지(곱으로만 나오는 쌍 = 남은 정확한 대칭) ② 가정으로 줄인 것(`α_c = 1 − α_a` 등)과 항등으로 줄인 것 ③ 범위 [0, 0] · 측정 고정을 갈라 적고 ④ 순위의 계산점 · 좌표(범위 정규화 · 로그/선형) · 문턱과 `|r₁₁|/|r_kk|` 조건수 하한을 적고 ⑤ 다중 시작 · 합성 참값 시험이면 회차별 잔차 문턱 · 범위 끝 몫 · 참값 IQR 안 몫 · 무작위 기준 · 잡음 · 참값 개수를 적는다.** 95호: ① 척도 대칭 하나(`D̂_e p̂` · `κ̂ p̂` — ≤23 `[재현·대수]`) ② `α_c = 1 − α_a` 하나(본문 0) ③ `R̂_f,p` [0, 0] · Q 측정 ④ 계산점 미인쇄 · 로그 14 / 선형 8 · 문턱 0 · ≥10^2.98(12 개) ⑤ 문턱 0 · Cell 1 범위 끝 10/22 · 참값 IQR 밖 14/22 · 무작위 0.43 · 무잡음 · 참값 하나.
26. (98호) **"문헌값과 일치 · 문헌 범위 안" 을 식별 근거로 쓴 추정 편이면 ① 그 문헌값이 같은 자료(같은 셀 · 같은 곡선)의 적합인지 · 측정인지를 원 편 각주로 확인하고 ② 같은 이름의 비(÷ 문헌)뿐 아니라 모형이 실제로 보는 조합(쌍극 확산 · 경계 분배 · 전도도 · i₀)의 비를 계산하고 ③ 원 편이 '관측 추가(DC + AC)' 를 처방으로 썼으면 더한 관측이 닻을 내린 항(대역이 따로 선 것)과 못 내린 항(같은 대역에 겹친 것)을 가르고 ④ 재풀이 대조를 크기뿐 아니라 계면 반응 방향(이완 부호 · 저주파 위상)까지 한다.** 98호: ① 적합 9 + EMF 유도 1 ② D⁰_p ×1.30 · t_e 0.81 → 1.00 · σ ×1.10 ③ 벌크 옴 ↔ 음극 계면(τ 비 0.72) ④ 음극 방향이 인쇄 식 글자 그대로.
25. (96호) **"identifiable" 을 쓴 추정 편이면 ① 그 주장의 층(구조적 비선형 · 선형 소신호 · 실제적 잡음)과 증명 위치(지면 · 인용)를 적고 ② 실제로 쓴 관측(소신호 EIS · 펄스 · OCV)에서 남는 비 · 합 조합을 적고 ③ 합성 참값 시험이면 시험 집합(부분 ↔ 전체) · 같은 모형 여부 · 잡음 실현 · 실행 수 · 참값이 경계 위 · 밖인지 · 초기값 = 참값인 매개변수를 적고 ④ 실셀 최종 표를 같은 지면의 초기화 · 경계 · 물리 범위와 대조하고(공통 인자로 묶인 값들이 함께 범위에 들 수 있는지) ⑤ SOC 무관 매개변수를 SOC 별로 맞춘 산포가 있으면 폭의 하한 표본으로 적는다.** 96호: ① 구조적 = 인용(Ref. 2) · 선형 = 손 분석 · 실제적 = 합성 한 번 ② 비 n̄e/ψ̄ · κ̄D/ψ̄ · R_c ↔ 1/κ̄^s(`[해석]` + R̄f^n) ③ 부분 집합만 정확 · 같은 모형 · 실현 하나 · 실행 하나 · n = 1 경계 위 · k̄0,6/7 경계 밖 · R_c 초기 = 참 ④ 넷 밖 · 둘 경계 위 · ψ̄ 화해 불가 ×3×10⁴ ⑤ κ̄D/ψ̄ ×12.
27. (99호) **'민감도 분석' 표가 축약 모형 검증(전체 ↔ 축약 오차의 OAT)이면 ① 기준 모형이 인쇄 식대로 계산됐는지 그림 값으로 항별 재풀이하고(99호 Nernst 항) ② 매개변수를 흔들어도 같은 최대값이 그 매개변수가 안 보이는 순간(켜는 순간 · 끝)인지 보고 ③ 단순화가 기대는 매개변수(단순화 (1) 이면 k_r · δ)를 흔들었는지 · '비현실' 배제 영역이 열화로 도달 가능한지 적고 ④ '관측성 · 관측 불가' 를 함께 쓴 편이면 대상(상태 ↔ 매개변수) · 근거 층(논증 · 계산 · 합성 실행) · 오차 성격(분산 ↔ 편향 — 모형 불일치 ÷ 출력 기울기)을 가른다.** 99호: ① Nernst 항 없음(모형 4 오차 ≈절반) ② 펄스 M3 0.0027 = t = 0⁺ ③ k_r · δ 행 0 · k_r ×100 이면 M2 15.3 / 6.8 mV · k_pos ×1/100 배제 ④ 상태 · 논증 + EKF 한 번 · 편향(9 % ≈ Δη ÷ 기울기).
28. (100호) **축약 · 근사 모형의 '오차 < X' 를 검증 근거로 옮길 때 ① 지표(RMSE ↔ 최대)와 최대의 자리(방전 끝 · 켜는 순간) ② 프로파일(축척 · 반복 · 끝 SOC) ③ 비교 대상이 같은 매개변수 한 벌의 원 모형인지(그러면 축약 오차일 뿐 매개변수 검증이 아니다) ④ 성분별 오차(출력 사상에서 상쇄되는 쌍 — 출력에 안 보이는 성분) ⑤ 축약이 기댄 단순화 근거가 앞 편 OAT 의 흔들지 않은 매개변수인지 ⑥ 차수 근거 그림의 '원 모형' 곡선이 해석식의 정확한 응답인지와 고른 차수의 유효 대역 ↔ 인용 기준 · 표본 주기를 적는다.** 100호: ① UDDS RMSE 2.6 · MaxAE 40.5 mV(방전 끝) ② 축척 UDDS 두 번 · 끝 SOC 0.021(`[재현]`) ③ 같은 표 I 의 PDE ④ 10C V 4.6 ↔ η_d 76.3 mV ⑤ r 무시 = 99호 표 2(인쇄 k_r — ×100 이면 10C RMS 14.85 mV) ⑥ 그림 3 PDE ≠ 식 (22) · 3차 대역 0.19 · 0.056 Hz ↔ 2.5 Hz.
29. (101호) **닫힌 꼴 '측정 비 → 매개변수' 처방(예: η_down/η_ss = t₊)이나 '정상 관측은 X 에 무관' 같은 구조 명제를 식별 근거로 옮길 때 ① 성립 조건(완전 해리 · 정상 도달 · 이상 · 일정 D) ② 같은 지면 확장(해리 등)에서 성립하는지 ③ 자기 자료에 적용했는지 ④ 그 지면 그림들이 한 매개변수 표로 닫히는지(정상 값이 같은 묶음 안의 차이는 시간 경과로 가린다)를 같이 적는다.** 101호: 해리 판 0.445 ↔ t₊ 0.4 · 그림 9 적용 0 · 표 1 ↔ x 0.9017 두 상태(그림 11(C) 시간 경과가 L 만 닫음).
30. (102호) **측정 확산계수(D̃)를 적합값의 '독립 대조' · '문헌값' · 하네스 입력으로 옮길 때 ① 방법과 역모형(가역 · 반무한 · 장시간 · Warburg 성분)과 맞춤 창 ② 가정 기하(S · L · Vm)와 dE/dδ · 조성 축 출처 ③ 셀(액체 ↔ 고체) · 막 두께 · 배향 ④ 같은 막 다른 방법의 시간 상수 폐합(EIS 무릎 · 저주파 용량 ↔ L²/D)을 같이 적고, 방법 순위를 정한 편이면 ⑤ 그 환산(Nernst–Einstein · Darken)의 종 기준과 기준 측정의 자기 일관성(이완 시간 · 시료 · 외삽)을 확인한다.** 102호: 한 물질 4.97 dex · 시간 상수 ×≈50–430 · σ 1/δ · DC 이완 ×≈5×10⁴ — 26 · 98호의 적합값은 이 범위 안이되 방법 칸에 따라 일치 ↔ ×25–146.
31. (103호) **결합 모형의 '민감도 둔감 · 영향 작음' 결론을 옮길 때 ① 기준점에서 그 결합 항이 켜져 있는지(103호: γ = β 이면 i₀ 응력 인자 ≡ 1) ② 지표가 그 항을 볼 수 있는지(충전 끝 용량은 평형 항 V_str 은 보고 σxx 는 못 본다 — 전압 몫 0.01 mV) ③ 결론이 기대는 구속 · 경계 가정(면내 강체 · 양끝 변위 0 — 풀면 Ω 의 용량 효과 0)과 짝인지 ④ 인쇄 민감도가 같은 지면 식으로 재현되는지(β ✅ · γ ✗)를 적는다** — ①–④ 가 없으면 '둔감' 은 구성의 결과일 수 있다.
32. (104호) **'parametric study · 설계 지침' 쓸기 편을 옮길 때 ① 쓸기 경향이 인쇄 기하 · 매개변수의 무차원 수(확산 시간 L²/D ↔ 방전 시간 · 이용률 상한)로 가능한지 ② '검증된 모형' 이 다사이클 · 다조건 실험에 사이클 · 조건마다 다른 상태로 맞춰졌는지(바꾼 손잡이 · 수) ③ 같은 조건 값이 그림 사이 같은지(기준점 · 점선 · 표) ④ 백분율의 기준(바꾸기 전 ↔ 뒤)과 비용량의 분모(고정 ↔ 비례 질량) ⑤ '일치' 지표가 상수 이동 · 척도에 불변인지(상관)를 적는다.** 104호: ① 평면 200 µm 이용률 0.12 % ↔ 그림 ∝ L(그림 8 = L_eff ≈1 µm) ② 곡선 넷 · 인쇄 0 ③ 100 µm · 0.1 C 48.4 ↔ 46.13 · 점선 5.2×10⁻¹⁵ ↔ 표 1.76×10⁻¹⁵ ④ −22.67 %(기준 900 µm) · mAh g⁻¹ 분모 미인쇄 ⑤ Pearson R² 0.96.

## 이 페이지가 주장하지 않는 것

- **대역 스윕이 국소 야코비안이라고 하지 않는다** — 모양 판독은 방향의 **후보**를 주고, 폭·조건수는 주지 않는다.
- **26호의 세 방향이 4 율 동시 적합에서도 전부 비식별이라고 하지 않는다** — 고율 곡선의 asinh 곡률(`[재현]` `i/2i₀` 1.9–2.3 @6C)이 `k` 쪽을 부분적으로 가를 수 있다. 확정된 것은 `D_e⁻` 의 한쪽 비식별(식 30의 극한) 하나다.
- **"sensitivity = sweep" 이 ASSB 문헌 전체의 관행이라고 하지 않는다** — 26호 Table 1 한 표 근거다. 27호는 반례(전역 Sobol)이지만 역시 첫 줄이다.
- **27호의 큰 `κ` 오프셋이 전부 접촉 손실이라고 단정하지 않는다** — 0.068 ↔ 0.07 일치와 바닥을 뺀 연결 입자 SOC 0.044 ↔ P2D 0.043 까지가 사실이고, `u` 가 부피 분율인지 · P2D 면적 과대(≈1.5 배)가 같은 자리에서 상쇄되는지는 모른다.
- **35호의 보정된 구간이 쓸모없다고 하지 않는다** — 스칼라 SOH 를 운용하는 데는 이 계보에서 가장 정직한 불확실성 보고다. 주장은 **그것이 파라미터 식별성과 다른 물음에 답한다**는 것까지다.
- **36호의 분류가 틀렸다고 하지 않는다** — aleatory/epistemic 은 예측 불확실성을 나누는 표준 분류이고 그 목적에는 맞다. 주장은 **그 분류에 데이터량 불변의 파라미터 폭이 들어갈 칸이 없다**는 것까지이며, 분류 원전(Der Kiureghian 2009)이 그 자리를 어떻게 두는지는 미확인이다.
- **49호의 "대역 끝 흡수" 를 일반 정리로 주장하지 않는다** — 한 셀(평탄한 스펙트럼)에서 두 사례가 맞은 것이다. 가파른 호가 대역 끝에 걸리면 적합 직렬 R 과 끝점 \|Z\| 는 다를 수 있다.
- **29호 SI 의 dependency 절대값을 재현했다고 하지 않는다** — 순위만 재현했다(표본 배치 · 가중 미기재, OriginPro 정의식은 이 세션에서 원문 미확인). 그리고 **"창 끝 도달률이 dependency 를 정한다" 를 일반 법칙으로 주장하지 않는다** — 식 (2) 한 모형 · 14 셀의 순위 일치다.
- **75호의 영역 지도가 틀렸다고 하지 않는다** — 기준 미인쇄 · 단순 평균 희석 · 40 · 60 wt% 포화 해석까지다. 함축 `i₀` 흩어짐은 한 θ 균질 BV 로 재현되지 않는다는 `[재현]` 이고, 원인(시간 기준 · 국소화 · θ → 1 소멸)은 가르지 않았다. 용량 축이 복합체 기준이라는 것도 지도 판독 위의 `[재현]` 이다(분모 미정).
- **76호의 원인 배정이 틀렸다고 하지 않는다** — `i₀` 미시험 · ×10 = 문헌값 · S17 비대각까지다. Wa 는 인쇄 파라미터(선형 극한 `R_ct` · 영상 계면 길이 판독 12–15 · τ 정의 두 가지)로 만든 `[재현]` 범위이고, 실제 황화물 계면의 `j₀` 는 이 위키에 없다.
- **77호의 "ionic percolation being the limiting factor" 가 틀렸다고 하지 않는다** — 대안 한계를 흔든 시험이 없고 관측이 방전 하나라는 것까지다. 첫 충전 반례 둘은 `[도표]` · 조건당 셀 1 위의 검사다.
- **82호의 "balanced transport" 가 틀렸다고 하지 않는다** — 네 점 표본으로 σ_ion 증가 · 면적 · 공극과 가를 수 없다는 것까지다. 옴 강하 크기 검사는 가정 두께(밀도 · void) 위의 `[재현]` 이고, 반응 분포를 통한 수송 한계는 배제되지 않는다.
- **83호의 설계 지침(E ≈2 GPa · σ 5×10⁻⁴ · coarse)이 틀렸다고 하지 않는다** — 조합 run · 고정값 · 전류가 없고, 결론 하나는 자기 다른 기준과 순위가 반대라는 것까지다. ϕ_mech 규모와 옴 문턱 전류는 인쇄 밀도 · 단면 분율(화소) · 가정 부피 변화 위의 `[재현]` 이다.
- **85호의 "작은 입자가 ρ 를 올린다" 가 틀렸다고 하지 않는다** — τ 비(×2.2)는 같은 방향이다; 틀린 것은 Ea 산술과 그 위의 정량("37 meV")이고, A 의 독립 관측이 없다는 것까지다.
- **86호의 "코팅이 접촉을 늘린다" 가 틀렸다고 하지 않는다** — 첫 충전 등가는 정적 고립 차의 상한(CV 몫 · 기생 · 산포 위)이고, 코팅 셀의 분극이 작다는 관측은 단단하다; 걸린 것은 `D` 없는 피복률의 재현 불가와 자기 데이터 미교차다.
- **92호의 블록 지향 모형이 틀렸다고 하지 않는다** — H-W 는 낙하 구간을 따라간다(그림 12c · 정의 미인쇄 86.5 %); 주장은 "블록 모양의 물리 배정이 정규화 · 구조 의존이고, BLA 분산은 식별성이 아니다" 까지다. 블록 교환은 일반 대수 성질이고 ×3.13 은 인쇄 식 그대로의 기대값이다(저자 코드 미대조).
- **93호의 "입력을 재라" 가 틀렸다고 하지 않는다** — 측정 입력이 적합보다 나은 출발점일 수 있다; 주장은 "측정 대체" 가 유일성 진단을 대신하지 않는다(측정 역모형이 가정을 요구 · 같은 저자 56호 그림 7)는 것까지다. 1호 예측 문장의 원문 존재는 1호 digest 전사 기준이고, 56호 그림 7 의 판독은 56호 digest 의 `[도표]` 다.
- **95호의 "12 개면 충분" 이 틀렸다고 하지 않는다** — 출력 RMSE 기준으로는 그림에 선다(셀 둘 · 회차 하나); 주장은 그것이 식별성 명제가 아니라는 것(저자 H1 이 같은 말을 한다)과 24 에 남은 척도 대칭 · `α_c` 가정까지다. 대칭은 인쇄 식 (9a) · (11a) 위의 대수이고 저자 툴박스 이산화는 미확인이며, 조건수 하한은 그림 4 막대 끝값(벡터 판독) 위의 `[재현]` 이지 참 조건수(SVD)가 아니다.
- **96호의 "highly accurate" 가 틀렸다고 하지 않는다** — 부분 집합(펄스 참값 고정)에서는 열셋 중 열둘이 ±5 % 안이다(그림 11 `[도표·화소]`); 주장은 그 문장이 단서 없이 전체 집합 · 실셀로 넘어간다는 것과 합성 시험이 산포를 낼 수 없는 설계(실현 하나 · 실행 하나)라는 것까지다. 비 구조의 척도 불변은 부록 계수 위의 `[재현·대수]` 이고, R_c ↔ R̄f^n 교환은 그림 13(b) 판독 폭 ±0.3 위의 `[해석]` 이다.
- **98호의 모형 · "LiPON 지배" 결론이 틀렸다고 하지 않는다** — 재풀이가 전해질 · 양극 · 호 지름에서 닫힌다; 주장은 그 적합값이 하류에서 '문헌값' 으로 쓰일 때 독립 근거가 아니라는 것과, 음극 계면이 인쇄 식 묶음 그대로의 반대 방향으로 계산된 서명이 그림 셋에 있다는 것(`[재현·대수]` · `[도표·화소]` — 코드 미공개라 구현 확정 아님)까지다. 조합 비는 인쇄 식 위의 대수다.
- **99호의 EKF 결론 · 단순화 판단이 틀렸다고 하지 않는다** — 재풀이가 그림 2 · 3 을 ±0.5 mV 로 닫는다(D_n⁻ 5.1 · 91호 c_max · T 가정); 주장은 그 기준 모형이 인쇄 식 (14) 의 Nernst 항 없이 계산됐다는 서명(`[재현]` — 코드 미공개라 구현 확정 아님)과, 표 2 가 단순화 (1) 이 기대는 k_r 을 흔들지 않았다는 것, '관측성' 이 계산 없이 쓰였고 9 % 가 편향의 크기와 같다는 것(화소 판독 ×0.7–1.5)까지다.
- **100호의 ROM 이 쓸모없다고 하지 않는다** — 계수는 정확한 Padé 이고 그림 5–8 이 우리 재현과 닫히며 정전류 축약 오차는 작다(RMSE ≤0.54 mV); 주장은 초록 '2.6 mV' 가 RMSE 라는 것(최대 40.5 mV) · 같은 10C 실행에서 출력 최대 4.6 ↔ 성분(η_d) 최대 76.3 mV 라는 것 · 그림 3 의 기준 곡선이 식 (22) 의 응답이 아니라는 것(원인 미확정) · r 무시 근거가 인쇄 k_r 에 매달린다는 것(`[재현]`)까지다.
- **101호의 닫힌 꼴 · 해리 결론이 틀렸다고 하지 않는다** — 완전 해리 · 정상 조건에서 식 (31)–(42) 는 우리 대수와 맞고 그림 8 · 11 · 12 는 재풀이와 ±1–3 mV 로 닫힌다; 주장은 그 처방 · 결론의 성립 조건이 지면 문장에 붙어 있지 않다는 것과, 그림들의 매개변수 상태가 표 하나로 닫히지 않는다는 것까지다(저자가 무엇을 바꿨는지는 인쇄 0).
- **102호의 측정 · 'PITT 가 가장 믿을 만하다' 가 틀렸다고 하지 않는다** — 네 닫힌 꼴은 저자 그림을 다시 내고 배향 효과의 방향은 원시 시간 상수도 지지한다; 주장은 측정 D̃ 가 방법 · 역모형 · 미인쇄 가정의 라벨이라는 것(같은 막 시간 상수 불일치 — 반사 경계 · L = 두께 가정 위의 `[재현·가정]`)과, 방법 순위를 정한 σ 환산의 종 기준(1/δ)과 기준 측정(이완)의 자기 일관성이 지면에서 확인되지 않는다는 것까지다.
- **103호의 모형 · 민감도 표가 틀렸다고 하지 않는다** — β 둘은 재현되고 인쇄 식은 한 매개변수 상태로 저자 그림을 다시 낸다(T 298 K · i₀ mol L⁻¹); 주장은 'Not sensitive' 가 기준점(γ = β) · 지표 · 구속 가정 위에 있다는 것과 γ 둘이 인쇄 식으로 재현되지 않는다는 것까지다(x_n 미인쇄 — 가정한 여덟 값 위).
- **104호를 'sensitivity = sweep' 낱말 관행의 둘째 근거로 세지 않는다** — 이 편은 'sensitivity' 를 한 번도 쓰지 않는다(0 회); 26호 표가 붙인 이름표의 대상일 뿐이다. 그리고 **이 편의 결론 방향이 틀렸다고 하지 않는다** — 인쇄 기하로 그림이 안 난다는 것(평면 확산 상한 위의 `[재현·가정]`) · 같은 지면 값 · 기준 · 사이클별 상태까지다; 저자 구현의 길이(≈1 µm)는 역산이지 확정이 아니다.

## 관련

- [[assb-contact-loss-vs-lampe]] — 닻(Q4).
- [[spm-grouped-parameter-identifiability]] — 셋째 줄 원전(28호, 액체셀)의 묶음 표. 26·27호 방향 대조.
- [[constrained-crb-identifiability]] — 셋째 줄의 이론. "민감도 ≠ 식별성" 의 원래 자리.
- [[fitting-degeneracy]] — flat valley 의 일반형.
- [[near-optimal-set-width-measurement]] — 폭을 재는 기계.
- [[assb-lampe-contact-product-degeneracy]] — 곱 축퇴 처방 표. 26호가 **열 번째 적용**이고, 이 페이지의 처방 2·3 이 그 표의 "`J^T J` 최소 고유벡터" 줄의 **공짜판**이다.
- [[assb-tortuosity-factor-effective-conductivity-split]] — 24호, Q4 열일곱 번째 성질의 재료. 27호의 `τ` 는 24호의 `τ²` 와 같은 양(이름 충돌).
