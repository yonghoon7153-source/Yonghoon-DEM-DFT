---
title: "SPM 파라미터 묶음과 식별 집합 — 용량 스케일은 입력이고, LAM 과 입자 비연결은 같은 묶음에 든다"
description: "Bizeray et al. 2019 reduce the single particle model to six parameter groups and, after linearisation, to three identifiable ones (two diffusion time constants and a lumped charge-transfer resistance); electrode capacity and initial stoichiometry - the degradation-mode axes - are assumed known through measured OCV slopes, so in this model class whole-particle disconnection enters exactly like active material loss and partial contact loss disappears into a lumped resistance"
created: 2026-09-23
updated: 2026-10-02
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/khalik2021_dfn-grouping-sensitivity-parameter-estimation.md, raw/papers/danilov2011_thin-film-assb-model-weak-electrolyte-parameter-fit.md, raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode-si.md, raw/papers/conforto2021_chemo-mechanical-ncm-active-mass-eis-psd-si.md, raw/papers/miss2022_exchange-current-density-tlm-thickness-lco-nmc-assb.md, raw/papers/conforto2021_chemo-mechanical-ncm-active-mass-eis-psd.md, raw/papers/li2024_assb-composite-cathode-model-contact-area-edl.md, raw/papers/chien2023_ici-rapid-solid-state-diffusion-coefficient.md, raw/papers/bizeray2019_spm-identifiability-parameter-estimation.md, raw/papers/park2024_asymmetric-kinetics-low-mass-loading-nmc111-latp-li-metal.md, raw/papers/iwakiri2024_new-ssb-model-parameter-estimation-sensitivity.md, raw/papers/sinzig2024_p2d-validity-ssb-global-sensitivity.md, raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode.md]
confidence: low
explored: false
verificationStatus: unverified
claimType: theoretical
evidenceScope: multi-source-primary
---

# SPM 파라미터 묶음과 식별 집합

> **도구 페이지다 — ASSB 근거가 아니다.** 원전은 액체셀(Bizeray, Kim, Duncan, Howey 2019, *IEEE TCST* 27(5) 1862,
> `raw/papers/bizeray2019_spm-identifiability-parameter-estimation.md`). SCHEMA 규칙대로 `assb` 태그를 달지 않는다.
> ASSB 쪽 쓰임은 [[assb-contact-loss-vs-lampe]] Q4 와 [[assb-sensitivity-sweep-vs-identifiability]] 의 셋째 줄에서 한다.
> 수치의 정본은 원문 PDF 이고 여기 값은 사본이다.

## 정의 — 14 → 6 → 5 → 3

| 단계 | 남는 것 | 무엇이 사라지나 | 근거 |
|---|---|---|---|
| 물리 파라미터 | 전극마다 `R · D · k · ε · δ · c_max` + 공통 `A · c_e` (14) | — | 원문 식 1–9 |
| **묶음** | 전극마다 `τ_d = R²/D` · `τ_k = R/(2k√c_e)` · `Q_th = ±ε δ c_max F A` (**6**) | 곱으로만 들어가는 조합 | `[인쇄]` 식 17–19 · 26–27, 전제 `x⁰` · `U(x)` 를 안다 |
| **선형화(한 DoD)** | `τ_d⁺ · τ_d⁻ ·` `R_ct` (5 → 합쳐서) | 두 전극 동역학 `θ₃`·`θ₆` 가 `R_ct` 하나로 — `[인쇄]` "infinite number of pairs" | 식 50 |
| **OCV 를 용량으로 재면** | **`θ̃ = (τ_d⁺, τ_d⁻, R_ct)` (3)** | `Q_th` 가 `β = dU/dQ = α/Q_th` 안으로 들어가 따로 안 남는다 — `β` 는 기준극/반쪽전지로 **입력** | 식 53–58 |

구조적 식별성(전달함수 유일성)은 일반적으로 성립하고, 예외 둘: **`β_i = 0`(평탄 OCV) → 그 전극 `τ_d` 비식별** · **`β₊ = −β₋` → 두 전극 맞바꿈**. `[인쇄]` 처방 = 각 전극이 번갈아 기울기를 갖는 **상보적 DoD** 를 합친다.

## 왜 중요한가 — 식별 집합에 모드 축이 없다

`[해석]` 열화 모드 언어로 옮기면 `Q_th,i` 는 **전극 용량 스케일(LAM)**, `x_i⁰` 은 **전극 정렬(LLI)** 이다. 원전은 둘 다 **입력으로 가정**하고 동역학 축만 식별했다.
⇒ "식별성을 잰 원전" 이 있다는 것과 "모드 분해의 유일성을 잰 편" 이 있다는 것은 **다른 문장**이다 ([[mode-identifiability-unmeasured-lineage]] 의 논지와 충돌하지 않는다).

### 카드 물음을 묶음에 올리면 (`[해석]` — 대수, 원문 명제 아님)

| 기구 | 묶음에서 | 선형화 EIS 파이프라인에서 |
|---|---|---|
| 진짜 LAM (`ε ↓`) | `Q_th ↓` | `β ↑` — 입력 |
| **입자 통째 비연결** (`ε_eff = uε`) | `Q_th ↓` — **LAM 과 항등** (`ε` 는 `Q_th` 에만 있다) | 같음 |
| 표면 일부 접촉 손실 (`a_eff = A_eff·3ε/R`) | `τ_k/(3Q_th)` 안의 `k·A_eff` 곱 | `R_ct` → `R0`(옴·접촉·피막과 합침) — 파라미터로 안 남는다 |
| 크기 선택적 비연결 | 유효 `R` 이동 → `τ_d` | 식별 집합 안 — 후보 채널 `[추론]`, 판별력 미정 |

⇒ SPM 판에서 "접촉 손실 ↔ LAM" 은 **근사적 축퇴가 아니라 같은 파라미터**다(입자 통째의 경우). 가를 정보는 모델 밖 관측(DEM `θ` · 회절 상 분율 · 기준극)이 줘야 한다.

## 이 위키에서의 적용 — 다른 논문의 비식별 방향을 이 표에 맞춰 본다

| 논문 | 방향 | 이 페이지의 대응 |
|---|---|---|
| 26호 Iwakiri 2024 | `k₁ ≡ k₂` | 식 50 — **같은 구조**(두 계면 동역학의 한 소신호 저항). 치료도 같다: 전극별 SOC 의존 차이 |
| 26호 | `D_e⁻` 0 열 | 예외 1(`β = 0`)과 **같은 부류, 다른 기구** — 관측 이득 0(작동점으로 풀림) ↔ 모델 구조 포화(안 풀림) |
| 26호 | `D·a_max` 한 조합 | `θ₂ = τ_d/(3Q_th)` — 용량 스케일이 동역학만으로는 안 보인다(짝은 다름) |
| 27호 Sinzig 2024 | P2D 오프셋 `1 − u` ≈ 0.07 | `Q_th` 손잡이 — 27호 처방 `A_el-c` 용량 깎기와 같은 자리 |
| 원전 자신 | 시간 영역 사후 보정 ×0.78 | `β₊` ×0.78 ≡ `Q_th⁺` ×1.28 — 식별 집합에서 뺀 용량 스케일을 검증 데이터로 돌렸다 |
| 29호 Yanev 2024 (ASSB 실험) | GITT `D_app` (식 3, `A` = BET) | `D_app ∝ 1/A²` 라 데이터가 보는 것은 `D·(A_eff/V)²` = **`1/τ_d`**(`L = V/A`). 29호는 **`D_LIB` 수입**으로 `D` 와 면적을 쪼개 "피복률 `φ`" 를 만든다 — 묶음을 푸는 것은 가정이다 |
| 29호 | 율 곡선 `Q_M` ↔ `α` | `Q_M` 은 `Q_th` 자리(용량 스케일)를 **적합**했다. 저율 평탄이 창 밖이면 `Q_M·α⁻ⁿ` 한 조합 — `[인쇄]` dependency ≈1. 28호의 비식별 조건(`β = 0`)과 같은 부류: **여기(excitation)가 그 방향을 안 건드린다** |
| 29호 | 표면 피복 `φ` | 이 표의 "표면 일부 접촉 → `R_ct`" 를 29호는 **확산 묶음의 면적**으로 읽는다 — 같은 물리량이 모델에 따라 다른 묶음에 배정된다 |
| 29호 SI 보강 (2026-09-28) | Tab. S2 dependency · S3 입도 · S6 형성 | `[인쇄]` `Q_M`–`α` dependency ≥0.95 는 sc90 · sc84 · sc90-BM — `[재현]` 순위는 창 끝 평탄 도달률과 ρ −0.991: 위 행 **"여기(excitation)가 그 방향을 안 건드린다" 의 실측 수치판**. 1 에 붙은 두 `Q_M`(sc84 · sc90-BM)은 자기 형성 첫 충전을 넘는다(용량 스케일 칸의 **물리 상한 검사**). `τ_d` 묶음을 쪼갠 면적 입력은 BET ↔ 구 면적(S3, ×1.65–4.3) 선택만으로 `D` 를 ×2.7–18 움직인다 |
| 30호 Park 2024 (ASSB 실험, LATP 펠릿) | CV Randles–Ševčík `D` | 기울기 `I_p/ν^½ ∝ A·C·√D` ⇒ `D_app ∝ 1/(A·C)²` — 29호 GITT 와 **같은 `τ_d` 부류 묶음의 CV 판**. `A`·`C_Li` 미인쇄라 재현되는 것은 방향 간 비뿐(`[재현]` 기울기 비² 1.94 ↔ 인쇄 1.97). 액체 대비 10.9 배를 **전부 `D`** 에 배정 — 29호(면적에 배정)와 **반대 방향으로 같은 묶음을 쪼갰다** |
| 30호 | Dunn `k₁ν + k₂ν^½` | 용량성/확산 비 `∝ c_s/(C√D)` — **면적이 약분되는 조합**(이 표의 `R_ct·C_dl` 류). 묶음을 푸는 도구가 아니라 묶음 **밖**의 비교 축 후보 |
| 31호 Chien 2023 (⚠ 액체, ICI 방법 원전) | ICI `D` (식 19, `A` = BET 상수) | 관측 비 `k·I/(dE_OC/dt) ∝ (V/A)/√D` = **`1/√τ_d` 묶음 그 자체**(`L = V/A`). GITT 와 같은 묶음을 1–5 s 차단창에서 본다 — 묶음을 푸는 것은 **상수 입력**이고 저자가 그것을 고지(`[인쇄]` "BET … may differ from the electrochemically active surface area") |
| 31호 | 입자 통째 비연결 `u` · 표면 피복 `φ` | `[해석]` `u` 는 `V`·`A` 를 같이 줄여 **약분**(이 표의 "통째 비연결 → `Q_th`" 와 정합 — `τ_d` 묶음에는 안 들어간다) · `φ` 는 `D_app = φ²D` 로 `τ_d` 묶음에 들어간다. 이 표 "표면 일부 접촉 → `R_ct`" 행의 **확산 판** |
| 31호 | ICI `R` ↔ `k` | `R` = EIS `R0+R1+R2`(이 표 선형화 행의 `R_ct` + `R0` 합) · `k ∝ 1/(A√D)`. `[해석]` 표면형 `R ∝ 1/(A·j₀)` 라 **`R/k` 에서 면적 약분** — 묶음 밖 비교 축 후보(30호 Dunn 비와 같은 부류) |
| 37호 Li 2024 (ASSB 복합양극 P2D/SPM 혼성, 9호의 원형) | `A_eff ↔ k_p` | `[해석]` 원형 모델 식 (8) 에서 `A_eff` 는 BV 분모에만 있어 **`k·A_eff` 가 이 표 `τ_k`(`R_ct`) 묶음의 한 인자**로만 산다 — 이 표 "표면 일부 접촉 → `R_ct`" 행이 ASSB 모델에 **정확한 항등**으로 선다. 이 모델은 확산 BC(식 15)에 `A_eff` 를 넣지 않는다(29 · 31호 "확산 판" 과 다른 배정) |
| 37호 | `R_s` ("Measured with SEM" 9.315 µm ↔ SI SEM ≈0.5–1.5 µm) | 확산에서는 `τ_d = R_s²/D_p`, 동역학에서는 `k·ε/R_s` 로만 보인다 ⇒ `D_p` · `k_p` 를 PSO 로 풀면 **틀린 `R_s` 를 둘이 흡수**하고 적합은 안 깨진다. 이 표의 묶음이 "반경 오기 검출 불가" 를 예측한다 |
| 38호 Conforto 2021 (ASSB 실험, NCM811 PC/SC · In/InLi, 40 사이클) | 이완 OCP 두 점 활성 질량 `m_act = ΔQ/(Δx·q)` | 이 표의 **용량 스케일(`Q_th` 자리)을 측정**했다 — 평탄 상대극이라 음극 곡선 · 오프셋이 없어 두 점으로 정해진다. 그러나 `[인쇄]` "disconnected … cannot contribute to the OCP … inactive" ⇒ 이 표 "입자 통째 비연결 → `Q_th`" 행 그대로 **`ε`·`θ` 한 묶음**. 이완 1 h 가 `τ_d` 보다 짧으면(`[재현]` PC 후반 ≈13–17 h) `τ_d` 묶음이 이 값으로 샌다(`[추론]`) |
| 38호 | EIS-PSD 유한공간 꼬리 `L_diff`(원통 앙상블, 빈 16 개) | 빈마다 `τ_d = L²/D̃` 묶음 — `L` 은 `D̃`(신품 Warburg + BET 면적) 고정으로만 나온다. 반무한 영역(`ωτ ≫ 1`, 저자 한계 `√(D̃/f_min)` = 1.8 µm @ 25 °C 밖)에서는 `L/(C_diff√D̃)` 하나 — `C_diff` 를 위 행(OCP 질량)에서 **고정 입력**으로 받아 두 행이 곱으로 묶인다. 용량성 극한에 닿으면 `C_diff` 단독이 위 행의 **독립 교차 검사**(이 편은 안 닿았다) |
| 38호 SI 보강 (2026-09-28) | S3 기준 곡선 · S8 다중 시작 · S2 | 용량 스케일 행의 게이지 눈금(액체 PC-NCM · 충전 가지 · 2 h 휴지)은 **4.19 V 에서 끝** — high-V 초기 사이클은 외삽이고, S3 재료로 Fig. 6 은 N ≥ 20 만 재현된다. 기준 곡선의 3.77 V 기울기(≈0.53 V)가 `C_diff/m` 520 을 준다(`[재현]`). `τ_d` 묶음 행의 폭: SC low-V N40 `L_diff,50` 1.70–3.84 µm(25 적합, PC 0). S2 — **SC 셀도** 0.6 mHz 에서 용량성 극한 밖 ⇒ 위 행의 독립 교차 검사는 SC 에서도 없다 |
| 50호 Miß 2022 (ASSB 실험, LCO · NMC83 \| LPSI \| In, TLM 두께 4 점) | TLM 두 극한 | `[해석]` 계면은 `Z_loc/(a_v d)` 로만 보인다 ⇒ 얇은 쪽 `j₀·a_v`(= `k·A_eff` 자리, 이 표 `τ_k` 묶음) · 두꺼운 극한 `j₀·a_v/τ`(수송 τ 와 한 묶음). NMC 는 두께가 전이를 가로질러 두 묶음이 갈리고, LCO 는 네 두께 전부 두꺼운 극한이라 한 묶음만 — 두께 스윕이 이 표의 "여기(excitation)" 역할을 할 때와 못 할 때 |
| 50호 | 면적 규약 `a_v·τd → a_v·d` | `[재현]` `(j₀, Q_DL, dU/dc) → (j₀/s, Q_DL/s, s·dU/dc)` 정확한 재척도 — 저주파 화학 용량 `F·ε·d/\|dU/dc\|` 는 이 표 `β = dU/dQ` 입력 자리(원전처럼 OCV 기울기로 고정하면 s 가 선다). 50호는 `dU/dc` 를 가변으로 두어(시작 대비 ×1.31 · ×1.07) 닻을 반쯤 풀었다. 용량성 극한 밖(반무한)이면 위 38호 행과 같은 `√D` 곱으로 약해진다 |
| 91호 Danilov 2011 (ASSB 박막 원형 모형 · 26호 계보 첫 표) | 전해질 넷 `k_r` · `δ` · `D_Li⁺` · `D_n⁻` | `[재현·가정]` 우리 국소 CRB(재풀이 모형 · σ_V 1 mV · 여섯 율) — \|ρ\| ≥ 0.98 · 가장 약한 방향(`δ` ↑ · `D_Li⁺` · `D_n⁻` · `k_r` ↓) · 조건수 9.5×10⁵. SPM 은 전해질을 버리므로 이 표에 대응 묶음이 없다(한계 셋째 줄) — 박막 모형에서 26호 §5-2 ④ "전도도형 한 조합" 의 수치판 |
| 91호 | `a_max` = 측정 용량 ÷ (F·Δx·M·A) | 이 표 `Q_th` 자리(용량 스케일)를 **측정 용량으로 고정**했다(각주 c · `[재현]` 23.32 kmol m⁻³) — 원전(Bizeray)과 같은 "용량 스케일은 입력" 선택이고, 그래서 26호 `D·a_max` 한 조합(위 26호 행 · `θ₂`)이 이 편에서는 깨져 `D_Li` 가 국소적으로 선다(CRB ×1.005). 대가: 활성 분율 · 접촉 몫이 이 입력 하나에 섞인다 |
| 95호 Khalik 2021 (⚠ 액체 DFN · 정규화 · 묶음 35 → 24) | `D̂_s = D_s/R_s²` · `k̂₀ = k₀c_e,o^α_a/(R_sF)` · `3Q = ĉ^max(s_100% − s_0%)` | 이 표 `τ_d` · `τ_k` · `Q_th` 묶음의 **DFN 판** — `[인쇄]` "by decreasing the diffusion coefficient D_s and increasing the particle size R_s accordingly, the diffusion dynamics in the solid phase remain unchanged … one of these parameters is redundant". `k̂₀` 는 반응 면적 `3ε_s/R_s` · `A` · `δ` 가 정규화에서 약분된 꼴인데, 그 약분은 `α_c = 1 − α_a`(표 1(b) 식 12a · b 에만 · 본문 0)가 있어야 정확하다(`[재현·대수]`). 용량 스케일은 Q(측정) + 창 폭으로 갈라 들어간다(식 14) — 원전과 달리 **창(정렬 · 이용 범위)이 식별 집합 안**에 있다 |
| 95호 | 창 넷 `s_n,0%` · `s_n,100%` · `s_p,0%` · `s_p,100%`(경우 1 — 셀 EMF 만 앎) | `[인쇄]` "the same EMF-SOC relation can be reached with any choice between 0 and 1" — 한 전극 곡선을 빌리고 다른 쪽을 `U_EMF + U_n` 으로 **정의**하면 평형 채널이 창에 무정보다. 이 표 예외 1(`β = 0`)의 **구성판** — 관측 이득이 아니라 정의가 0 을 만든다. 남은 인쇄 경로는 (12b) 교환 전류의 SOC 모양 하나 · 0 % 끝 둘은 감도 순위 15–21 위(10^−3.6 … 10^−4.4 `[도표·벡터]`) · Cell 1 다중 시작에서 셋이 범위 끝 · 합성 모형 오차 1.2 mV 에서 `s_p,100%` 가 범위 하한 |
| 95호 | `D̂_e` · `κ̂` · `p̂_n` · `p̂_p` · `p̂_sep` | `[재현·대수]` (9a) `D̂_e p̂` · (11a) `κ̂ p̂` 로만 쓰여 `(D̂_e/λ, κ̂/λ, λp̂)` 가 정확한 척도 대칭 — 이 표 식 50(두 전극 동역학 → `R_ct` 하나)과 같은 "곱으로만 들어가는 조합" 이 묶은 뒤에도 하나 남았다(식별 가능한 조합 ≤23) · 사전 상자(`κ̂` ×2.86)가 자를 뿐 없애지 않는다 |

## ★ DFN 판 (2026-10-02, 95호 Khalik 2021 — ⚠ 액체 · 도구)

`raw/papers/khalik2021_dfn-grouping-sensitivity-parameter-estimation.md` (Khalik · Donkers · Sturm · Bergveld 2021 *J. Power Sources* 499, 229901 — 27호 [27] · 4차 묶음 파일 55).
원전(28호 SPM)과 같은 계보의 **DFN 묶음**이다 — 원 35(표 2 "a" 표시 34 + `A`) → 24(Q + 창 4 + 19) `[인쇄]` · `[재현]`.
출력은 24 묶음의 함수다(구성 증명). 24 의 식별성은 증명되지 않았다(위 적용 표 95호 셋째 행의 척도 대칭 · `α_c = 1 − α_a` 가정).

### 카드 물음을 DFN 묶음에 올리면 (`[해석·대수]` — 원문 명제 아님 · 이 편은 열화 · 접촉 0)

| 기구 | 정규화 DFN 묶음에서 | 위 SPM 표와 |
|---|---|---|
| 표면 접촉 손실 `A_eff` | `k̂₀ × A_eff` · `R̂_f ÷ A_eff`(막 저항은 국소 플럭스에 걸림) — **`k̂₀R̂_f` 불변** | SPM 은 `τ_k` 하나 · DFN 은 두 묶음에 같이 — 원리상 "곱 일정으로 같이 움직임" 이 둘째 서명 |
| 순수 `k₀` 손실 · 막 성장 | `k̂₀` 하나 · `R̂_f` 하나 | — |
| 입자 통째 비연결 `u`(= `ε_s` 형 LAM) | 창 폭(전극 용량 `3Q/Δs`) · `R̂_f`(÷u) · `σ̂`(×u) | SPM 은 `Q_th` 와 항등 · DFN 은 `R̂_f` · `σ̂` 가 붙는다 |
| `c^max` 형 LAM(입자는 남고 자리만 줄어듦) | 창 폭 하나 | `ε_s` 형과 `R̂_f` · `σ̂` 두 서명만큼 다르다 |
| **양극**(이 편 `R̂_f,p` 범위 [0, 0]) | `A_eff` 는 `k̂₀,p` 하나 · `u` 는 창 폭 + `σ̂_p`(감도 Cell 1 17 위 · 10^−3.79 `[도표·벡터]`) | **`u` ≈ `LAM_PE`** — SPM 판 항등이 범위 선택 덕에 거의 그대로(음극은 `R̂_f,n` 이 자유라 근사 축퇴) |

⇒ 묶음은 곱을 **선언**한다: 곱을 한 매개변수로 바꾸면 그 묶음은 식별 대상이 되지만 곱의 두 인자(`D ↔ R²` · `k₀ ↔ A_eff`)는 입력 쪽으로 넘어간다 — 카드 물음(`A_eff` · `u` ↔ `LAM_PE`)은 그 넘어간 쪽에 있다([[assb-lampe-contact-product-degeneracy]] 일흔여덟 번째 적용).

### 원전(28호)과 반대쪽 끝 — 식별 집합에 모드 좌표가 있다

28호는 용량 스케일 · 정렬을 입력으로 뺐다(위 "왜 중요한가"). 95호는 창 네 끝점을 식별 집합 안에 넣었고, 그 좌표가 약한 쪽이었다 — 경우 1(셀 EMF 만) 평형 채널 무정보(인쇄) · 0 % 끝 둘은 감도 순위 12 개 밖 · Cell 1 범위 끝 셋 · 합성 모형 오차에서 `s_p,100%` 0.418 → 0.22(범위 하한) `[도표·벡터]`.
경우 2(분해 OCP 고정 + 창 맞춤)는 우리 α·β 와 같은 연산이다 — [[halfcell-ocp-shape-invariance]] · [[halfcell-window-parametrization-lineage]] 여덟 번째 축.

## 한계 (이 페이지가 주장하지 않는 것)

- **비선형 SPM 의 식별성은 원전에 없다** — 모든 결론이 DoD 한 점 근방 선형화 위다(`[인쇄]` 비선형 동역학은 향후 과제).
- 원전의 실제적 식별성은 **등고선 그림**이다 — FIM · CI · 프로파일 수치 0. 정량 도구는 [[constrained-crb-identifiability]] · [[near-optimal-set-width-measurement]] 쪽에 있다.
- **ASSB 에 SPM 이 맞는다고 하지 않는다** — SPM 은 전해질 수송을 무시한다. ASSB 복합양극은 고체전해질 이온 수송이 지배 인자일 수 있다(27호).
- 입자 비연결 ≡ LAM 은 **묶음 대수**다. 비연결 입자가 느리게라도 방전되는 부분 연결은 이 표 밖이다.
- **DFN 판(95호)의 `u` ≈ `LAM_PE` 는 범위 선택(`R̂_f,p` [0, 0]) 위의 묶음 대수다** — 이 편은 열화 · 접촉을 다루지 않고, 남은 척도 대칭 · `α_c` 가정은 인쇄 식 위의 `[재현·대수]` 이다(저자 툴박스 이산화 미확인).

## 관련

- [[assb-contact-loss-vs-lampe]] — Q4 의 도구 칸(28호).
- [[assb-sensitivity-sweep-vs-identifiability]] — 세 줄 표의 셋째 줄 원전.
- [[assb-lampe-contact-product-degeneracy]] — `A_eff·k` 곱의 액체 SPM 판 원형(식 18 · 26).
- [[fitting-degeneracy]] — flat valley 일반형. 원전 Fig. 2 가 그 2 차원 그림이다.
- [[constrained-crb-identifiability]] — 모드 축(`β`·`x⁰` 쪽)의 식별성을 수치로 재는 틀.
