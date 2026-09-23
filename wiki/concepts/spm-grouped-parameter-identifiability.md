---
title: "SPM 파라미터 묶음과 식별 집합 — 용량 스케일은 입력이고, LAM 과 입자 비연결은 같은 묶음에 든다"
description: "Bizeray et al. 2019 reduce the single particle model to six parameter groups and, after linearisation, to three identifiable ones (two diffusion time constants and a lumped charge-transfer resistance); electrode capacity and initial stoichiometry - the degradation-mode axes - are assumed known through measured OCV slopes, so in this model class whole-particle disconnection enters exactly like active material loss and partial contact loss disappears into a lumped resistance"
created: 2026-09-23
updated: 2026-09-23
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/chien2023_ici-rapid-solid-state-diffusion-coefficient.md, raw/papers/bizeray2019_spm-identifiability-parameter-estimation.md, raw/papers/park2024_asymmetric-kinetics-low-mass-loading-nmc111-latp-li-metal.md, raw/papers/iwakiri2024_new-ssb-model-parameter-estimation-sensitivity.md, raw/papers/sinzig2024_p2d-validity-ssb-global-sensitivity.md, raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode.md]
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
| 30호 Park 2024 (ASSB 실험, LATP 펠릿) | CV Randles–Ševčík `D` | 기울기 `I_p/ν^½ ∝ A·C·√D` ⇒ `D_app ∝ 1/(A·C)²` — 29호 GITT 와 **같은 `τ_d` 부류 묶음의 CV 판**. `A`·`C_Li` 미인쇄라 재현되는 것은 방향 간 비뿐(`[재현]` 기울기 비² 1.94 ↔ 인쇄 1.97). 액체 대비 10.9 배를 **전부 `D`** 에 배정 — 29호(면적에 배정)와 **반대 방향으로 같은 묶음을 쪼갰다** |
| 30호 | Dunn `k₁ν + k₂ν^½` | 용량성/확산 비 `∝ c_s/(C√D)` — **면적이 약분되는 조합**(이 표의 `R_ct·C_dl` 류). 묶음을 푸는 도구가 아니라 묶음 **밖**의 비교 축 후보 |
| 31호 Chien 2023 (⚠ 액체, ICI 방법 원전) | ICI `D` (식 19, `A` = BET 상수) | 관측 비 `k·I/(dE_OC/dt) ∝ (V/A)/√D` = **`1/√τ_d` 묶음 그 자체**(`L = V/A`). GITT 와 같은 묶음을 1–5 s 차단창에서 본다 — 묶음을 푸는 것은 **상수 입력**이고 저자가 그것을 고지(`[인쇄]` "BET … may differ from the electrochemically active surface area") |
| 31호 | 입자 통째 비연결 `u` · 표면 피복 `φ` | `[해석]` `u` 는 `V`·`A` 를 같이 줄여 **약분**(이 표의 "통째 비연결 → `Q_th`" 와 정합 — `τ_d` 묶음에는 안 들어간다) · `φ` 는 `D_app = φ²D` 로 `τ_d` 묶음에 들어간다. 이 표 "표면 일부 접촉 → `R_ct`" 행의 **확산 판** |
| 31호 | ICI `R` ↔ `k` | `R` = EIS `R0+R1+R2`(이 표 선형화 행의 `R_ct` + `R0` 합) · `k ∝ 1/(A√D)`. `[해석]` 표면형 `R ∝ 1/(A·j₀)` 라 **`R/k` 에서 면적 약분** — 묶음 밖 비교 축 후보(30호 Dunn 비와 같은 부류) |

## 한계 (이 페이지가 주장하지 않는 것)

- **비선형 SPM 의 식별성은 원전에 없다** — 모든 결론이 DoD 한 점 근방 선형화 위다(`[인쇄]` 비선형 동역학은 향후 과제).
- 원전의 실제적 식별성은 **등고선 그림**이다 — FIM · CI · 프로파일 수치 0. 정량 도구는 [[constrained-crb-identifiability]] · [[near-optimal-set-width-measurement]] 쪽에 있다.
- **ASSB 에 SPM 이 맞는다고 하지 않는다** — SPM 은 전해질 수송을 무시한다. ASSB 복합양극은 고체전해질 이온 수송이 지배 인자일 수 있다(27호).
- 입자 비연결 ≡ LAM 은 **묶음 대수**다. 비연결 입자가 느리게라도 방전되는 부분 연결은 이 표 밖이다.

## 관련

- [[assb-contact-loss-vs-lampe]] — Q4 의 도구 칸(28호).
- [[assb-sensitivity-sweep-vs-identifiability]] — 세 줄 표의 셋째 줄 원전.
- [[assb-lampe-contact-product-degeneracy]] — `A_eff·k` 곱의 액체 SPM 판 원형(식 18 · 26).
- [[fitting-degeneracy]] — flat valley 일반형. 원전 Fig. 2 가 그 2 차원 그림이다.
- [[constrained-crb-identifiability]] — 모드 축(`β`·`x⁰` 쪽)의 식별성을 수치로 재는 틀.
