---
title: "ASSB 모델 논문의 '민감도 분석' — OAT 스윕은 야코비안의 열이고, 겹쳐 보면 비식별 방향이 보인다"
description: "In the ASSB modelling literature 'sensitivity analysis' means one-at-a-time parameter sweeps of a forward model against design KPIs, not identifiability analysis; when a paper prints both a parameter fit and such sweeps, overlaying the sweep figures exposes parallel or null Jacobian columns, and the first such paper shows a fitted parameter that drifted ten orders of magnitude along a direction its own sweep had found flat"
created: 2026-09-23
updated: 2026-09-23
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/thelen2024_probabilistic-ml-battery-health-review.md, raw/papers/roman2021_ml-pipeline-soh-estimation-uncertainty.md, raw/papers/liang2026_pulse-excitation-active-bms-comment.md, raw/papers/chien2023_ici-rapid-solid-state-diffusion-coefficient.md, raw/papers/park2024_asymmetric-kinetics-low-mass-loading-nmc111-latp-li-metal.md, raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode.md, raw/papers/bizeray2019_spm-identifiability-parameter-estimation.md, raw/papers/iwakiri2024_new-ssb-model-parameter-estimation-sensitivity.md, raw/papers/sinzig2024_p2d-validity-ssb-global-sensitivity.md, raw/papers/zhou2025_tailored-cathode-microstructure-low-pressure-assb.md, raw/papers/stavola2023_lithiation-gradients-tortuosity-thick-nmc111-argyrodite.md, raw/papers/vadhva2021_eis-for-assb-theory-methods.md]
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
8. (29호) **적합 논문이면 파라미터 dependency/상관 행렬을 SI 에서 찾는다** — 둘째 줄의 수치다. 찾았으면 **진단이 경고한 셀이 결론에 쓰였는지** 추적한다(29호는 sc90 을 빼고 같은 문제의 sc84 로 결론을 냈다).
9. (30호) **교과서 선형화 추출(b 값 · Randles–Ševčík · Dunn)이면 식별성 이전에 두 가지를 본다** — ① 같은 데이터가 식의 전제(b = 0.5 · 원점 통과)를 만족하는가 ② 인쇄된 값과 **라벨**(산화/환원 · 계)이 그 논문 자기 그림에서 다시 구한 값과 맞는가. 30호는 ② 에서 뒤집혀 있었다.
10. (35호) **"calibrated uncertainty" · "confidence interval" 을 보면 대상이 예측(스칼라 목표의 오차)인지 파라미터(해 집합)인지 먼저 적는다.** 예측이면 Q4 근거가 아니다. 그리고 적중률 점수(`C_score`)는 **목표와의 거리**로 읽는다 — 90 % 목표에서 100 은 과소 확신이다. 이름도 대조한다: "α-accuracy · β"(예측 지표) ≠ 우리 α·β(전극 스케일 · 오프셋).
11. (36호) **"posterior" · "parameter uncertainty" · "epistemic" 을 보면 ① 무엇의 파라미터인지(물리 ↔ ML 가중치) ② 데이터를 늘리면 줄어드는 폭인지(실제적) 아닌지(구조적) ③ 공분산을 보고했는지(평균장 근사면 상관이 지워진다)를 적는다.** 셋 다 아니면 Q4 근거가 아니다.

## 이 페이지가 주장하지 않는 것

- **대역 스윕이 국소 야코비안이라고 하지 않는다** — 모양 판독은 방향의 **후보**를 주고, 폭·조건수는 주지 않는다.
- **26호의 세 방향이 4 율 동시 적합에서도 전부 비식별이라고 하지 않는다** — 고율 곡선의 asinh 곡률(`[재현]` `i/2i₀` 1.9–2.3 @6C)이 `k` 쪽을 부분적으로 가를 수 있다. 확정된 것은 `D_e⁻` 의 한쪽 비식별(식 30의 극한) 하나다.
- **"sensitivity = sweep" 이 ASSB 문헌 전체의 관행이라고 하지 않는다** — 26호 Table 1 한 표 근거다. 27호는 반례(전역 Sobol)이지만 역시 첫 줄이다.
- **27호의 큰 `κ` 오프셋이 전부 접촉 손실이라고 단정하지 않는다** — 0.068 ↔ 0.07 일치와 바닥을 뺀 연결 입자 SOC 0.044 ↔ P2D 0.043 까지가 사실이고, `u` 가 부피 분율인지 · P2D 면적 과대(≈1.5 배)가 같은 자리에서 상쇄되는지는 모른다.
- **35호의 보정된 구간이 쓸모없다고 하지 않는다** — 스칼라 SOH 를 운용하는 데는 이 계보에서 가장 정직한 불확실성 보고다. 주장은 **그것이 파라미터 식별성과 다른 물음에 답한다**는 것까지다.
- **36호의 분류가 틀렸다고 하지 않는다** — aleatory/epistemic 은 예측 불확실성을 나누는 표준 분류이고 그 목적에는 맞다. 주장은 **그 분류에 데이터량 불변의 파라미터 폭이 들어갈 칸이 없다**는 것까지이며, 분류 원전(Der Kiureghian 2009)이 그 자리를 어떻게 두는지는 미확인이다.

## 관련

- [[assb-contact-loss-vs-lampe]] — 닻(Q4).
- [[spm-grouped-parameter-identifiability]] — 셋째 줄 원전(28호, 액체셀)의 묶음 표. 26·27호 방향 대조.
- [[constrained-crb-identifiability]] — 셋째 줄의 이론. "민감도 ≠ 식별성" 의 원래 자리.
- [[fitting-degeneracy]] — flat valley 의 일반형.
- [[near-optimal-set-width-measurement]] — 폭을 재는 기계.
- [[assb-lampe-contact-product-degeneracy]] — 곱 축퇴 처방 표. 26호가 **열 번째 적용**이고, 이 페이지의 처방 2·3 이 그 표의 "`J^T J` 최소 고유벡터" 줄의 **공짜판**이다.
- [[assb-tortuosity-factor-effective-conductivity-split]] — 24호, Q4 열일곱 번째 성질의 재료. 27호의 `τ` 는 24호의 `τ²` 와 같은 양(이름 충돌).
