---
title: "복합양극 동역학 항의 곱 축퇴 — LAM_PE 와 접촉 손실이 A_eff·ε_p/R_s 한 조합으로만 들어간다"
description: "In a published composite-cathode ASSB P2D model the Butler-Volmer denominator sees only the product A_eff x eps_p / R_s, so active-material loss, contact-area loss and particle radius are not separately identifiable from a discharge curve; a second, experimental paper (three-electrode EIS + transmission-line model) stands on the same product and assigns all of it to the exchange current density; a third one prints both the resistance and the capacitance and so lets the product be broken - by us, not by its authors"
created: 2026-09-22
updated: 2026-09-23
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/bielefeld2022_voids-kinetics-morphology-composite-cathode-fem.md, raw/papers/hlushkou2018_void-space-ion-transport-composite-cathode.md, raw/papers/neumann2021_garnet-3d-structure-grain-boundary-transport.md, raw/papers/ren2023_oxide-ssb-composite-cathode-architecture-perspective.md, raw/papers/oh2025_mgsigr-overcharge-low-np-ratio-low-pressure-assb.md, raw/papers/illig2012_charge-transfer-contact-resistance-lfp-drt-ecm.md, raw/papers/miss2022_exchange-current-density-tlm-thickness-lco-nmc-assb.md, raw/papers/barai2018_measurement-timescale-internal-resistance-methods.md, raw/papers/dugas2021_engineered-three-electrode-cell-assb-li-in-reference-layer.md, raw/papers/solchenbach2016_gold-wire-micro-reference-electrode-liquid-t-cell.md, raw/papers/schlenker2020_li6ps5cl-li-metal-lifetime-three-electrode.md, raw/papers/hertle2023_micro-reference-electrode-lithiated-gold-wire-assb.md, raw/papers/jin2015_lithium-silicide-anode-electrode-design-assb.md, raw/papers/fukunishi2023_graphite-three-electrode-impedance-cyclability.md, raw/papers/santhosha2019_indium-lithium-electrode-phase-formation-redox-potential.md, raw/papers/nam2018_three-electrode-assb-failure-modes-li-in-depletion.md, raw/papers/ikezawa2020_lto-reference-electrode-assb-three-electrode-eis.md, raw/papers/sakka2022_pressure-3d-structure-composite-cathode-xct.md, raw/papers/conforto2021_chemo-mechanical-ncm-active-mass-eis-psd.md, raw/papers/li2024_assb-composite-cathode-model-contact-area-edl.md, raw/papers/thelen2024_probabilistic-ml-battery-health-review.md, raw/papers/roman2021_ml-pipeline-soh-estimation-uncertainty.md, raw/papers/liang2026_pulse-excitation-active-bms-comment.md, raw/papers/zhang2025_low-pressure-assb-challenges-strategies-review.md, raw/papers/bicer2025_ssb-chemistry-bms-thermal-assembly-critical-review.md, raw/papers/chien2023_ici-rapid-solid-state-diffusion-coefficient.md, raw/papers/park2024_asymmetric-kinetics-low-mass-loading-nmc111-latp-li-metal.md, raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode.md, raw/papers/bizeray2019_spm-identifiability-parameter-estimation.md, raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md, raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md, raw/papers/vadhva2021_eis-for-assb-theory-methods.md, raw/papers/kouhestani2022_phm-solid-state-batteries-perspective.md, raw/papers/yanev2024_li-in-alloy-anode-kinetic-limitations.md, raw/papers/fukunishi2023_ncm523-three-electrode-impedance-degradation.md, raw/papers/yoshida2024_four-electrode-assb-cell-li-transport.md, raw/papers/chang2020_embedded-in-reference-electrode-assb-limiting-factors.md, raw/papers/sedlmeier2023_micro-reference-electrode-assb-pouch-inli-anode.md, raw/papers/strauss2018_cathode-particle-size-inactive-fraction-assb.md, raw/papers/koerver2017_capacity-fade-interphase-chemomechanical-ncm811-lps.md, raw/papers/stavola2023_lithiation-gradients-tortuosity-thick-nmc111-argyrodite.md, raw/papers/zhou2025_tailored-cathode-microstructure-low-pressure-assb.md, raw/papers/iwakiri2024_new-ssb-model-parameter-estimation-sensitivity.md, raw/papers/sinzig2024_p2d-validity-ssb-global-sensitivity.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: theoretical
evidenceScope: multi-source-primary
---

# 복합양극 동역학 항의 곱 축퇴 (`A_eff · ε_p / R_s`)

> `assb` 축의 **다섯 번째** 개념 페이지다. 닻은 [[assb-contact-loss-vs-lampe]].
> 앞의 넷: [[composite-cathode-percolation-utilization]] (`θ_AM`) ·
> [[assb-apparent-capacity-decomposition]] (3 항 분해) ·
> [[assb-pressure-reapplication-separation-test]] (압력 되돌림) ·
> [[assb-stack-pressure-operating-window]] (압력 창).
>
> ★ **이 페이지가 앞 넷과 다른 점**: 앞 넷은 *현상*(접촉 손실이 존재한다)을 다룬다.
> 이 페이지는 *역문제*(그 존재량이 유일하게 정해지는가)를 다루고,
> **그 답이 "아니다" 라는 것을 출판된 모델의 인쇄된 식에서 손으로 보인다.**

## 어디서 왔나

Huo et al. 2025 (*J. Power Sources* **627**, 235830, raw:
`raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md`) 는 이 계보에서
**실험과 파라미터 식별을 한 논문 안에서 잇는 첫 편**이고, 그래서 처음으로
**열화 모드의 지분 자체를 적합으로 정한다** (`ε_p` 하나를 푼다).
그 논문의 Table 1 · Table 3 만으로 아래가 나온다.

> ★ **2026-09-23 정정 (37호 — 9호가 위임한 원전)**: 9호의 모델 · PSO · `A_eff` 정의는 Li et al. 2024 (*eTransportation* 20, 100315,
> `raw/papers/li2024_assb-composite-cathode-model-contact-area-edl.md`) 에서 왔다. 그 편 Table 1 의 `A^p_eff` 0.4938 · `A^n_eff` 0.4095 는 **출처 각주가 없고**
> 복합양극 조성이 다른(38 ↔ 56 wt%) 9호 값과 **네 자리 같다** — 아래 "`A^p_eff` 는 적합값" 은 **"출처 없는 상속값"** 으로 읽는다.
> 그리고 아래 "9 배" 의 `R_s` ≈9.4 µm 도 두 편에 공통이다(37호 SI SEM 도 입자 반경 ≈0.5–1.5 µm). 원형 모델의 식으로는 곱이 **`A_eff · k_p · ε_p / R_s`** 이고 그중 `A_eff ↔ k_p` 는 정확한 항등이다(아래 §스무 번째 적용).

## 정의 — 데이터가 보는 조합

원전 Table 1 의 **인쇄된 식**을 그대로 옮기면 (`[인쇄]`):

```
BV 전류밀도    j^p_ct = (I − I^p_dl) / ( A^p_eff · a_{s,p} · A · L_p )
비표면적       a_{s,p} = 3 · ε_p / R_s
```

따라서 (`[해석]`, 이 조합은 원전이 쓰지 않는다):

```
            ★  과전압 η^p_ct 가 보는 것은   A^p_eff · ε_p / R_s   한 조합뿐이다  ★
```

`A^p_eff`(유효 접촉 면적비) · `ε_p`(활물질 부피분율) · `R_s`(입자 반경)
**셋이 동역학 항에서 완전히 축퇴한다.** 세 값을 각각 `c`·`c`·`1` 배 해도,
또는 `1`·`k`·`k` 배 해도 계면 동역학은 **정확히 같다**.

## 축퇴를 깨는 채널은 셋뿐이고, 하나만 강하다

| # | 채널 | `ε_p` 가 들어가는 방식 | 세기 |
|---|---|---|---|
| ① | **용량** `Q_max = ε_p·A·L_p·c^p_max·F·Δθ_p` | `ε_p` 단독 (× `c^p_max`·`Δθ_p`) | **압도적** — 방전곡선의 길이 |
| ② | 고체확산 BC `D_p·∂c_p/∂r|_{R_s} = −I/(a_{s,p}·A·L_p·F)` | `ε_p / R_s` (**`A_eff` 없음**) | 약함 — 농도 분극에만 |
| ③ | `κ_eff = κ_se · ε_se^brug`, `ε_se = 1 − ε_p` | `ε_p` 단독 | 약함 + **정의가 모호**(아래 ⚠) |

`[해석]` **그러므로 방전 V–Q 곡선 하나를 맞추는 절차에서 식별되는 것은 사실상
"용량 ÷ 신품 용량" 이다.** `ε_p` 에 붙은 "positive active material 의 부피분율"
이라는 물리 이름은 **모델이 붙여 준 것**이지 데이터가 가른 것이 아니다.
용량을 같은 만큼 줄이는 어떤 기구든 — 접촉 손실, 균열에 의한 고립, 구조 열화,
코팅 열화, 리튬 재고 손실 — **같은 `ε_p` 를 낸다.**

이것은 [[fitting-degeneracy]] 의 **flat valley** 를 1 차원에서 본 형태다.
액체셀의 `(α_PE, β_PE)` 축퇴와는 **자리가 다르다**: 저쪽은 *용량축 좌표끼리*,
여기는 **용량축 스케일 ↔ 동역학 면적**이다.

## ★ 원전 안에서 이미 9 배로 흔들린다 (`[재현]`)

원전이 인쇄한 값과 원전의 SEM 이 서로를 배반한다.

| | 값 | 출처 |
|---|---:|---|
| `A^p_eff` | **0.4938** | `[인쇄]` Table 3 |
| `ε_p` (fresh) | **0.321** | `[인쇄]` Table 3 · Eq. (2) |
| `R_s` | **9.466 µm** | `[인쇄]` Table 3 |
| `a_{s,p} = 3ε_p/R_s` | **1.017e5 m⁻¹** | `[인쇄]` Table 3 (✓ `[재현]` 검산 일치) |
| **SEM 의 NCM 입자 반경** | **≈1.05 µm** | `[재현]` Fig. 5a 픽셀 계측, 스케일바 0.8 µm = 40 px |

```
표의 조합            A_eff · a_{s,p} = 0.4938 × 1.017e5 = 5.02e4 m⁻¹
SEM 의 R_s 를 쓰면   a_{s,p} = 3×0.321/1.05e-6       = 9.17e5 m⁻¹
같은 곱을 맞추려면   A_eff = 5.02e4 / 9.17e5         = ★ 0.055
```

→ **"유효 접촉 면적비" 가 `0.055` 와 `0.494` 사이를 9 배로 움직인다.**
어느 쪽도 데이터가 배제하지 않는다. 원전은 `[인쇄]` "retaining the **actual
physical significance** of the parameters" 라고 쓴다.

⚠ **한계**: 입자 경계는 저자가 그린 초록 원으로 잡았고 SEM 은 표면 투영이라
최대 단면이 아닐 수 있다. 9 배를 뒤집으려면 원이 실제 입자의 1/9 이어야 한다.
단결정 NCM811 의 통상 크기(2–5 µm)도 SEM 쪽과 일치한다.

## ★ 두 번째 결과 — 열화를 한 노브로 돌리면 LAM 과 율 손실이 섞인다

원전은 노화 단계마다 **`ε_p` 하나만** 다시 적합한다. 그런데 `ε_p` 가 줄면
`a_{s,p} = 3ε_p/R_s` 도 같이 줄어 **분극이 커지고 컷오프에 더 일찍 닿는다.**

`[재현]` (원전 Eq. (2) + Fig. 7c/8c 판독):

| 셀 | `Δε_p/ε_p` | `ΔSOH` | **증폭** |
|---|---:|---:|---:|
| A (125 cyc) | 14.28 % | `[도표]` 22.9 % | **1.60** |
| B (140 cyc) | 7.44 % | `[도표]` 9.8 % | **1.32** |

`[해석]` **원전이 "활물질 손실" 이라 부르는 용량 감소의 ≈37 %(A 기준)는
모델 안에서조차 활물질 손실이 아니라 같은 노브가 만든 율 특성 저하다.**
그리고 증폭이 상수가 아니다(1.60 vs 1.32) — 동작점에 의존한다.

이것은 [[assb-apparent-capacity-decomposition]] 의 3 항 분해
(`Q_apparent = θ_AM · η(i) · Q_material`) 에서 **`θ_AM` 과 `η(i)` 가 한 파라미터에
묶여 버린** 경우다. 2호(Clausnitzer)에서 세운 **율 스윕 분리 시험**이 그대로
처방이 된다: **같은 데이터를 `i → 0` 으로 한 번 더 돌리면 `η` 성분이 사라진다.**

## ⚠ 세 번째 — `ε_se` 의 처리가 어느 쪽이든 모델이 깨진다

원전 신품에서 `ε_p + ε_se = 0.321 + 0.679 = 1.000` (정확). 노화 중 `ε_p` 가 줄 때:

- **`ε_se = 1 − ε_p` 를 유지하면**: `[재현]` `ε_p = 0.2752` → `κ_eff` 가
  `0.3985 × 0.7248^3.67 = 0.1223 S/m` → **신품 0.0963 대비 +27 %**.
  **모델이 "늙을수록 복합양극 이온전도가 좋아진다" 고 말한다** — 원전 자신의
  `[인쇄]` "cracking … **increases the tortuosity** … and **reduces the effective
  conductivity**" 와 정반대다.
- **`ε_se` 를 고정하면**: `ε_p + ε_se = 0.954` → **9.5 vol% 의 유령 공극**.

**원전은 어느 쪽을 택했는지 적지 않는다.** 그리고 어느 쪽이든 ③ 채널이
축퇴를 깨는 데 쓸 수 없게 된다.

## 무엇을 재면 깨지는가 (처방)

축퇴는 **여기(excitation) 부족**에서 온다. 곱을 가르려면 `A_eff` 와 `ε_p` 가
**다르게 반응하는** 자극이 필요하다.

| 처방 | 무엇을 가르나 | 값 |
|---|---|---|
| **율 스윕** (최소 2 율, `i → 0` 포함) | `η(i)` 를 지워 `θ_AM·Q_material` 만 남긴다 | ★ 2호 논지의 재사용 |
| **HPPC / 펄스** | 과전압을 용량과 독립으로 읽는다 → `A_eff·ε_p/R_s` 를 직접 | ★★ **원전이 수집하고 버렸다** |
| **다중 SOC EIS** | 같은 곱의 주파수 분해 | ★ 원전이 100/50/0 % 를 재고 100 % 만 썼다. ⚠⚠ **단독으로는 못 쓴다 — 아래 §"EIS 는 대가를 받는다"** |
| **압력 되돌림** | `θ_AM` 만 (부분) 복원 → 진짜 재료 손실과 분리 | [[assb-pressure-reapplication-separation-test]] |
| **`J^T J` 최소 고유벡터** | 이 곱이 실제로 null 방향인지 수치 확인 | [[fitting-degeneracy]] 의 "그리는 법" |
| ★★★ **`R_CT · C_dl` 짝** (2026-09-22 신설, 16호에서) | **`R_CT·C` 는 접촉 면적이 소거되는 조합**(고유 시상수), **`C` 단독은 접촉 면적에 비례** ⇒ **둘을 같이 보면 `θ` 와 `j₀` 가 갈린다** | ★★ **16호가 두 값을 다 인쇄해 놓고 조합을 안 만든다** (아래 §16호) · ★★★★ **18호에서 실제로 갈렸다 — 단, 전제 `C∝θ` 를 먼저 검증해야 한다** (아래 §18호) · ❌ **19호에서 전제가 두 번째로 깨졌다** (아래 §19호) |
| ★★★★ **`Ea`(노화 전후) — 면적-불변 채널** (2026-09-22 신설, **19호에서**) | `R(T) = A(θ)·exp(Ea/RT)` 에서 **`Ea` 는 접촉 면적과 직교한다** ⇒ **`Ea` 불변 + `R` 증가 = 면적 쪽과 양립 · `Ea` 증가 = 화학/장벽 쪽**. ★ **`C_dl ∝ θ` 라는 (두 번 깨진) 전제를 쓰지 않는다** | ★★★★ **19호가 실측으로 준다**: `[도표]` 압력 560→840 kPa 에서 `R₂` **−26 %** 인데 `[인쇄]` "the **physical state of the interface does not affect the Ea** but the resistance values … **Ea as the essential parameter**". ⚠ **충분조건은 아니다**(`A` 에 면적 외 항) — 19호 자신이 반례다(아래 §19호 검사 B). ★ **18호가 `Ea(노화 전후)` 를 쟀다면 검사 B 가 `C` 없이 독립 확인됐을 것이다** |
| ★★★ **SOC 추종 상 분율** (2026-09-23 신설, **22호에서**) | 회절 2상 정련으로 **쓰이지 않은 부피(`θ·ε_p`)를 구조로** 잰다 ⇒ 곱에서 `ε_p·θ` 를 떼고 `A_eff·j₀` 만 남긴다 | ★★★ **22호가 신품에서 준다**: `[인쇄]` 불활성 2 / 27 / 31 %, 용량 독립 대조 ±7 %. ⚠ 반사 기하 = 한쪽 면 표층(`[재현]` ≈3–15 µm) · 열화 판은 **두 SOC** 가 필요 · `A_eff` ↔ `j₀` 는 여전히 안 갈린다 (아래 §22호) |
| ★★★ **무전류 이완 = 전제 양성 대조** (2026-09-23 신설, **23호에서**) | 같은 셀·같은 복합체에서 **전류 없이** 기계 이완만 일어날 때(화학 불변을 XPS 로 확인) `R·C` 가 보존되는지 본다 ⇒ 보존되면 **그 호에 대해서는 `C ∝ 면적` 이 이 복합체에서 작동**한다 | ★★★ **23호 SI Fig. S3**: `[도표]` (`R₂`,`C₂`) ×1.6 ↔ ×0.65, `R₂·C₂` **+5 %** (면적 서명 통과) · (`R₃`,`C₃`) ×2.4 ↔ ×1.35 (실패). ⚠ 호 정체·셀 조건 미상, 판 a↔c 크기 ≈8 배 불일치 (아래 §23호) |
| ★★ **상대극 교체 대조의 조건** (2026-09-23, **23호에서**) | In ↔ LTO 처럼 상대극을 바꿔 호의 전극 배정을 검사할 때 **두 상대극이 같은 결함(무 Li 조립 · 방전 끝 평탄 이탈)을 공유하지 않아야** 용량 배정까지 대조가 된다 | ⚠ **23호는 저항 배정만 검사** — 두 상대극 모두 방전 끝 `C_anode` 두 자릿수 붕괴 |
| ★★★ **코팅 유무 쌍 = 화학 대조** (2026-09-23 신설, **24호에서**) | 계면 **화학만** 바꾸고(코팅이 계면층 경로를 막는다) 수축·접촉·수송은 그대로 둔 쌍 ⇒ 코팅으로 **안 변하는 몫**이 면적·수송·상대극 쪽의 상한 — **면적 대조(2단계)의 여집합** | ★★★ **24호**(70 %, LLSTO 15–20 nm): 첫 사이클 비가역 `[도표]` **−14 %** 만 · 충전 1 구배 `[인쇄]` "did not change the nature" · 이봉 약화. ⚠ n = 1 씩, 코팅 행이 표끼리 안 맞는다(24호 D17) — 코팅이 접촉 형태를 안 바꾼다는 전제 위 |
| ★★ **두 영역 대조(4단계)의 시편 조건** (2026-09-23, **24호에서**) | 주파수 영역(EIS) 값과 시간 영역(operando/DC) 값을 비교할 때 두 시편은 **같은 제조 압력·같은 두께**여야 한다 | ⚠ **24호**: EIS 차단 셀 50 / 150 MPa ↔ operando 100 MPa — "굴곡도 진화" 가 압력 이력과 교락 |
| ★★★ **SE 입도 쌍 + 분말 BET = 한쪽 상의 면적 대조** (2026-09-23 신설, **25호에서**) | 계면의 **SE 쪽 비표면적만** 바꾼 쌍(CAM·조성·공정 고정)에 **독립 면적 측정(BET)** 을 붙인다 ⇒ 면적 가설의 예측(`C` 비 = 1/`R` 비 ≈ BET 비)을 **자기 데이터 밖에서** 검사 | ★★★ **25호 신품 P4**: `R_ct` ×0.57 · τ ×1.41 ⇒ `C` ×1.7–2.5 ↔ 1/`R` 1.75 · BET 1.53 — **방향·자릿수 통과**(18호 검사 A 의 **CAM** 입도 쌍은 실패). ⚠ BET 는 SE **분말** 면적이지 CAM\|SE 접촉 면적이 아니다 · 25호는 SE 벌크 σ ×0.66 · 밀도 0.77 → 0.90 가 같이 변했다(고주파 호 교락) |
| ★★ **추정 논문의 스윕 그림 겹치기 = 공짜 `J^T J`** (2026-09-23 신설, **26호에서**) | 적합과 OAT 스윕을 같이 인쇄한 모델 편에서 **같은 모양의 스윕 그림 쌍(평행 열) · 반응 없는 그림(0 열)** 을 찾고, 그 파라미터의 **적합값 ÷ 문헌값**을 본다 — 위 "`J^T J` 최소 고유벡터" 줄의 비용 0 판 | ★★★ **26호**: Fig. 5a `D_e⁻` 0 열 → 적합값 **10 자릿수** 표류 · Fig. 12a≡b `k₁`↔`k₂` · Fig. 3≡15 `D_M⊕`↔`a_max`. ⚠ 대역·단일 율 스윕이라 방향 **후보**일 뿐 폭은 안 준다 ([[assb-sensitivity-sweep-vs-identifiability]]) |
| ★★★ **외부 액체 기준 수입** (2026-09-23 신설, **29호에서**) | 곱의 한 인자를 **같은 분말의 액체 반쪽전지**로 고정한다 — GITT `D·(A_eff/V)²` 에서 `D_LIB` 를 들여와 나머지를 접촉 면적(피복률 `φ = √(D/D_LIB)`)으로 | ★★★ **29호**: `φ` 53.3 → 18.0 %(gran) · 85.2 → 3.1 %(sc). ⚠ **기준도 곱을 진다** — 같은 조성인데 `D_LIB` gran/sc **2.7 배**(액체가 균열 내면을 적신다, 저자 서술). 22호의 "LIB 대조" 와 같은 부류 |
| ↳ **율 스윕 줄의 실패 조건** (2026-09-23, **29호에서**) | 첫 줄("`i → 0` 포함")은 **종료 율에서 곡선이 평탄할 때만** `θ·Q` 를 `η` 에서 뗀다. 평탄이 창 밖이면 외삽 용량 `Q_M` 과 동역학 시간척도 `α` 가 한 조합(`Q_M·α⁻ⁿ`) | ★★★★ **29호 저자 진단**: `[인쇄]` sc90 dependency ≈1. ⚠ 같은 문제의 sc84 는 외삽 ≈236 ↔ 실측 177 로 해석에 쓰였다 |
| ↳ **율 스윕 줄의 두 번째 실패 조건** (2026-09-23, **30호에서**) | 외삽 용량은 **스윕 시간 동안 정적 용량이 움직이지 않을 때만** 정적이다 — 블록당 수십 사이클의 율 시험은 표류와 율을 섞는다. 29호 조건(종료 율 평탄)과 **별개** | ★★★ **30호**: `[재현]` 29호 식을 Fig. 2a 에 걸면 평탄이 창 안이라 `Q_M` ≈63 이 식별(`Q_M`–`α` 상관 0.24–0.34)되지만, 그 값은 0.1 C 블록에서만 85 → 63(−26 %) 표류한 **뒤**의 용량 · `n` ≈2.5(29호 해석 범위 밖) |
| ↳ **외부 액체 기준 줄의 경고** (2026-09-23, **30호에서**) | 액체 기준은 곱의 **어느 인자를 고정할지 정하지 않는다** — 저자가 고른다 | ⚠ **30호**: CV Randles–Ševčík `D_app ∝ 1/(A·C)²` 의 고체/액체 10.9 배를 **전부 `D` 에** 배정(29호는 같은 구조를 **면적**에). 30호의 액체 대조는 다공 전극 전체가 젖고 고체는 펠릿 한 면만 닿는 **면적이 정의상 다른 대조** — `[재현]` 유효 면적 ≈3.3 배면 `D` 가 같아도 된다 |
| ★★ **Dunn 비 `k₁/k₂` — CV 의 면적 소거 조합** (2026-09-23 후보, **30호에서**) | `k₁ = A·c_s` · `k₂ ∝ A·C·√D` ⇒ 용량성/확산 비 `∝ c_s/(C√D)` — **`A` 약분**. 16호 `R·C` 의 CV 판 | ⚠ **30호**: 1.0 mV s⁻¹ 비 액체 1.78 ↔ 고체 1.38 ⇒ 저자 `D` 배정이 맞으려면 면적당 표면 용량이 액체에서 **≈4.3 배**여야 한다(`[재현]`). 전제(두 성분이 같은 면적을 본다 · 면적당 `c_s` 비교 가능)가 약해 **후보**만 |
| ↳ **외부 기준 줄의 세 번째 배정 — 상수 입력** (2026-09-23, **31호에서**) | 기준 없이 `A` 를 **BET 상수**로 넣어 곱 전체를 `D` 에 준다. ★ 저자가 **고지**하고 비교 주장(두 방법 일치)을 `A` 약분 형태로 한정한 첫 표본 | ⚠ **31호**: 봉인은 사이클 추적 · operando 의 절대 주장에서 풀린다. `[재현]` BET ↔ D50 구 선택만으로 `D` ×2.52 — 방법 간 불일치 SD 0.56 보다 크다. 29호 `D_LIB` 가 바로 이런 액체 측정이다 ⇒ 29호 `φ` 는 **두 유효 면적의 비** |
| ★★ **ICI `R/k` — 한 차단의 면적 소거 조합** (2026-09-23 후보, **31호에서**) | 정전류 중 짧은 차단의 절편 `R`(표면형 `∝ 1/A`) 과 √t 기울기 `k`(`∝ 1/(A√D)`) ⇒ `R/k ∝ √D/j₀` — **`A` 약분**. 면적 손실 = `R`·`k` 동배수(`R/k` 불변) · `D` 손실 = `k` 만 · `j₀` 손실 = `R` 만. 16호 `R·C` 의 **시간 영역 · 확산 판**, 처방 1단계를 `C` 없이 | ⚠ **31호는 비를 만들지 않았고 사이클 추적(Fig. 7·8)에 `k` 를 인쇄하지 않았다** — 지면에서 계산 불가(zenodo 원자료에는 있음). 조건: `R` 에서 면적 무관 `R0` 제거(31호 액체 ≈4–5 Ω ≪ 50 Ω; ASSB 는 SE 벌크 + 상대극이라 크다 → 3전극 전제) · 반무한 창 유효(31호 `[재현]` 창이 경계). **후보** |
| ↳ **온보드 번역 — 한 펄스 이완이 1·4단계 + `R/k` 의 공통 입력** (2026-09-23, **34호에서**, `[해석]`) | 전류 계단 한 번의 응답 `R₀ + R_p(1−e^{−t/τ}) + k√t` 에서 `τ ∝ c_dl/j₀`(면적 약분) · `C = τ/R_p ∝ A`(면적 서명, 1단계 τ 형 = 21호) · `C` 상한 검사(4단계 = 20호) · `R_p/k ∝ √D/j₀`(31호). 능동 펄스 BMS 는 이 처방의 **자연 하드웨어** | ⚠ **34호(Comment)는 이것을 쓰지 않는다** — 대역 이름표 셋만, `C`·시상수 0, 등가 EIS 는 신경망 재구성. 조건 넷: τ ≫ 샘플 간격(계면 대역 τ ≈0.16 ms–0.16 s → kHz 급) · 단자 = 양극 + 상대극 합(17·20·25호) · `C ∝ A` 전제(18·19호에서 깨짐) · √t 창 분리(31호). **재구성 · 온도 불변 학습은 1단계 `C` 와 3-a `Ea` 를 지우는 방향** |
| ↳ ⚠ **경고 — 목표 주도 특징 선택은 처방 입력을 버린다** (2026-09-23, **35호에서**, `[해석]`) | 용량(SOH)을 목표로 한 특징 선택(RFE · 중요도)은 **용량과 직교하는 채널**(저항 · 용량성 · 시상수)을 먼저 버린다 — 곱의 두 인자를 가르는 정보가 바로 그 방향이다 | 35호: 30 특징 중 유일한 저항 채널 `Lagged Pseudo Resistance`(`ΔV/I`)가 세 그룹 **모두** 탈락(`[인쇄]` SI Tables 3–5). 데이터 기반 BMS 에서 처방 입력을 찾을 때는 **선택 전 특징 목록**을 본다. 34호(사상이 지운다)에 이은 두 번째 경로 |
| ↳ **율 스윕 줄의 세 번째 실패 조건** (2026-09-23, **37호에서**) | 모델이 **율마다 다시 정하는 파라미터**를 가지면(37호 `D_p = D_p,ref(C-rate)·trD_p(x)`), 율에 따른 잔여 손실 — 계면 · 접촉 · SE 수송 — 이 그 파라미터로 먼저 들어간다. 29호(종료 율 평탄) · 30호(스윕 중 표류)와 **별개** | ⚠ **37호**: `[도표]` `D_p,ref` 0.4 → 2 C ≈4.3 배, 검증 율(0.6 · 1.6 C)에도 꺾임 — 7 율이 있는데도 곱을 가를 정보가 `D_p,ref` 에 쓰였다. 율 스윕을 처방으로 쓸 때 **모델의 율 무관 파라미터 목록**을 먼저 확인한다 |
| ★★★ **`A_eff ↔ k` 항등 — 표면 접촉 손실의 쌍둥이는 `LAM` 이 아니라 반응 상수** (2026-09-23, **37호 — 원형 모델의 식에서**) | 원형 모델에서 `A_eff` 는 BV 분모에만 있다(`[인쇄]` 균일 표면 전류 가정 — 용량 · 확산에 없다) ⇒ `η_ct` 는 `A_eff·k·ε_p/R_s` 로만 보고 `A_eff → cA_eff, k → k/c` 가 **모든 출력에서** 같다. 1단계(`R·C`)가 가르려는 쌍이 바로 이것이다 | ⚠ **37호 모델은 `c_dl` 을 F(전극 전체)로 고정해 면적과 떼어 놓았다** — 이 모델로 truth 를 만들면 `A_eff` 변화가 `R·C` 를 바꾸고 `C` 는 그대로다(처방 전제의 반대). 처방을 채점할 truth 에는 **면적에 비례하는 이중층**이 먼저 필요하다 |
| ★★★ **이완 OCP 두 점 = 연결 질량 (`ΔQ/Δx`)** (2026-09-23 신설, **38호에서**) | 평탄 상대극 셀에서 방전 전후 **이완 OCP** 를 기준 OCP–x 에 대 `Δx` 를 얻고 `m_act = Q/q(Δx)` — 곱에서 **`η` 를 율과 무관하게** 뗀다(율 스윕 줄의 대체). **`θ` 와 `ε_p` 는 한 칸으로 남는다** | ★★★ **38호**: 40 사이클 × 4 조건, `[도표]` PC N = 40 ≈0.63 · SC ≈0.91. ⚠ 조건 셋 — (i) 이완 ≥ `L²/D̃`(38호 1 h ↔ `[재현]` PC 후반 ≈13–17 h ✗, 편향 방향 `[추론]` 질량 손실 과대) (ii) 상대극 평탄 폭 ≪ 분해능(±10 mV ≈ ±4 %) (iii) 기준 곡선이 같은 계면계(38호는 액체셀에서 수입) |
| ↳ ⚠ **저주파 꼬리의 반무한 곱 `L/(C_diff·√D̃)`** (2026-09-23, **38호에서**, `[해석]`) | 유한공간 Warburg 가 용량성 극한에 닿지 않으면(`ωτ ≫ 1`) 꼬리가 정하는 것은 `L/(C_diff√D̃)` 하나 — `C_diff/L ∝` 접촉 면적이므로 **면적 × √D̃** 이다. `C_diff` 를 다른 채널(OCP 질량)에서 고정하면 두 채널이 곱으로 거래한다. 용량성 극한에 닿으면 `C_diff` 단독 = **OCV 독립 활성 질량** | ⚠ **38호**: 저자 신뢰 한계 `√(D̃/f_min)` = 1.8 µm(25 °C) ↔ `[도표]` PC `L_diff,50` 4.8–5.6 µm · `C_diff` 를 OCP 질량으로 **고정**. 37호 `A_eff ↔ k` 의 확산 판, 30호 Randles–Ševčík · 31호 ICI 와 같은 부류의 **사이클 해상판** |
| ★★★ **영상 면적 → `R·φ` 검사 — 면적을 재고도 곱이 남는가** (2026-09-23 신설, **39호에서**) | 압력 · 공정 등으로 면적이 바뀐 상태들에서 **영상으로 잰 피복 `φ`** 와 **`R_ct`** 를 같이 얻으면 `R_ct·φ` 를 본다 ⇒ 일정하면 면적 채널, 변하면 **곱의 나머지**(`k_p` · 영상 해상도 아래 실접촉 · 상대극)가 그만큼을 가져간다. **영상의 길이 척도(화소)를 같이 적는다** — `A_eff = φ_영상 × (해상도 아래 실접촉 몫)` | ★★★★ **39호**(CT 0.5 µm, 신품, 압력 4 점): `[도표]` `φ` ×1.10 ↔ `R_ct` ×14 ⇒ `[재현]` `R_ct·φ` **×13** — **2단계를 측정된 면적으로 건 첫 표본이고, 면적 가설이 CT 척도에서 기각된다**(로그 변화의 ≈4 % 만 면적). ⚠ 2전극 · n = 1 · 분할 질량수지 ×2 · 고압 `R_ct` 가 Nyquist 호와 ×2–3 |
| ★★ **3전극 옴 몫은 기준극 위치가 정한다 — 분리막 질량비 검사** (2026-09-23 신설, **40호에서**) | 3전극으로 나눈 전극 저항 · DC 과전압에는 **기준극 위치가 정한 분리막 몫**이 들어 있다. 양 전극 스펙트럼의 고주파 끝 비를 **기준극 양쪽 SE 의 질량(두께) 비**와 대조하고, `R·C` · `Ea` 는 R1 을 뗀 호에, **DC 과전압 비교는 그 몫을 뺀 뒤에** 한다. 그리고 **2전극 "양극 호" 의 상대극 몫**을 같은 셀에서 잰다 | ★★ **40호**(LCO\|LGPS\|Li-In, 신품, 210 MPa): `[도표]` 고주파 끝 LCO ≈12–13 : Li-In ≈33–35 Ω ↔ LGPS 50 : 160 mg — `[재현]` 1 : 2.7 ↔ 1 : 3.2 ✓ · 2전극 적합이 LCO R2 ×2.7 · R3 ×1.67 과대(1 kHz 이상 호의 ≈절반이 상대극). ⚠ 21호가 이 편의 Li-In 과전압을 인용하며 분리막 몫(≈26–27 Ω cm²)과 충–방 폭(×2)을 함께 넣었다 — 이 줄이 없으면 생기는 오류의 실례 |
| ★★★ **면적 서명 ↔ 저율 용량 비 대조 — 반쪽전지 음극** (2026-09-23 신설, **43호에서**) | 1단계가 어떤 호에 면적 서명(`C` 비 ≈ 1/`R` 비, τ 불변)을 주면 그 면적 비를 **같은 셀 저율 용량 비**와 댄다. 반쪽전지(Li 저장소 상대극)는 `LLI` 를 지워 WE 용량을 `(1−LAM)(1−u)` 한 곱으로 만든다 ⇒ **면적 비 < 용량 비 이면 면적 손실의 일부는 연결된 입자의 피복(`A_eff`, 37호 `k` 쌍둥이)이지 통째 고립(`u`)이 아니다.** `LAM` ↔ `u` 는 여전히 한 곱 | ★★★ **43호**(흑연\|LPSI, 333 K 가속): `[재현]` `R_CT` `C_eff` ×0.43 ± 0.2 ≈ 1/`R` ×0.47 · τ ×0.92 ↔ 0.05 C 용량 `[도표]` ×0.75–0.78. ⚠ 같은 호의 `C_eff`(20–46 mF)가 이중층 상한의 ×270–3,200 라 `C ∝ A` 전제가 약하고, 3-a(`Ea` 22 → 27.5)는 반대 방향 · n = 1 |
| ↳ **외부 기준 줄의 네 번째 배정 — 같은 계의 "면적 기지" 대조 셀 (GITT Weppner–Huggins)** (2026-09-23, **44호에서**) | GITT 식이 주는 것은 `√D · S / θ` 한 조합이다(θ = 참여 분율, 식의 `m_B` 에 숨어 있다). 한 셀에서 `S`(또는 `D`)를 고정하는 **근거를 적고, 그 근거가 비교 셀에도 참인지** 본다 — 참이면 쪼개기는 결과가 아니라 선택이다. 그리고 (i) **계단별 값**을 다 적고 (ii) 참여 용량 비로 **`θ` 민감도**를 적고 (iii) 입자 `r²/D` 를 펄스 길이와 댄다 | ⚠ **44호**(Li₄.₄Si 단층, 신품, 2015 — 29 · 30 · 31호보다 이르다): Case 1 "전해질 없음 → `S` 기하" 로 `D` 를 뽑고 Case 2 차이를 전부 `S` 에 — Case 2 도 전해질 없음. `[재현]` 인쇄 `S` 3.19 = 셋째 계단(4.13 / 3.67 / 3.18) · BET ×8.7 ↔ ×2.07 · `θ` 를 GITT 참여 비(≈×2.75)로 두면 ×4.7–5.7 · r²/D ≈9 s ≪ 600 s |
| ★★ **합 일치는 분배를 검증하지 않는다 — 반쪽에만 있는 고주파 호는 3-b(`C` 상한)로 먼저 거른다** (2026-09-23 신설, **45호에서**) | 3전극 반쪽 합 = 완전지(`Z_CR + Z_RA = Z_CA`)는 같은 셀이면 항등식이라 **기준극 위치 artifact(재분배)가 상쇄**되고 DC 전위도 안 보인다. 그러므로 곱을 가르기 전에 (i) **두 반쪽의 분배**는 합이 아니라 기준극 위치 · 분리막 질량비(40호 줄)로 검사하고 (ii) **반쪽 하나에만 있는 호**는 `C = τ/R` 를 분리막 기하 용량과 대 넘치면 물리 성분으로 적합하지 않는다. 부수: **2전극 적합의 전극 간 비유일성은 같은 셀 3전극 반쪽이 고른다** — 곱 앞에 분배를 고정하는 순서 | ★★ **45호**(NCM851005\|Li₆PS₅Cl\|In/InLi, μ-RE ∅10 µm, 신품): `[인쇄]` 합 잔차 Re <1 % · Im <10 % 로 "validating … concept and construction" · 양극 반쪽 호 #1("SE separator") `[재현]` τ ≈0.6 µs · R ≈57 Ω(가정) ⇒ **C ≈10 nF ↔ 기하 10–100 pF(×100–1000)** · 2E 두 적합(`R_Anode` 14 ↔ 3.9 Ω cm², `[인쇄]` "equally well") ↔ S7 음극 반쪽 호 ≈12–13 ⇒ Fit 1(우리 판독). ⚠ 반쪽 · 전체 주파수 끝점 미인쇄 · 검증 셀 ≠ 분석 셀 |
| ↳ **외부 기준 줄의 다섯 번째 배정 — 연구 간 비교: 남의 논문의 로딩 · BET 추정으로 면적을 고정** (2026-09-23, **47호에서**, ⚠ 액체) | 다른 연구실 셀과 `R_CT` 를 비교할 때 면적(거칠기 인자 = 로딩 × BET)을 **그쪽 다른 논문에서 추정**해 넣고, `R` 비를 면적 비로 설명한다. **여러 점(첨가제 량 · SOC 등)에서 비가 일정한지** 먼저 본다 — 일정하지 않으면 면적 하나로 안 닫힌다 | ⚠ **47호**: `[재현]` 거칠기 비 295/70 = 4.2(인쇄 "∼5") ↔ Burns/자기 `R_CT` 비 6.0 · 3.75 · 3.2(×1.9 퍼짐). 저자는 "only an estimate" 로 고지하고 BET 규격화 축을 병기 |
| ★★ **호 제거 검정 + 2전극 합 재구성 — 적합 품질이 귀속을 알리지 않는다는 것의 같은 셀 시연** (2026-09-23 신설, **48호에서**) | 곱을 가르기 전에 두 검사: (i) **한 호를 빼도 적합 품질이 같으면** 그 호의 `R` 은 지표로만 쓴다(값을 곱의 입력으로 쓰지 않는다) (ii) 3전극 반쪽 합(상대극 쪽 분리막 몫 제거)을 **한 전극 모형으로 적합해 '만족' 이 나오면** 2전극의 그 호는 전극 귀속이 불가하다 — 2전극 셀에서 곱을 가르려는 시도는 거기서 멈춘다 | ★★★ **48호**(LTFS\|β-LPS\|Li₀.₅In 전면 기준층\|β-LPS\|Li₀.₅In): `[인쇄]` 재구성 2전극을 WE 3 요소 회로로 적합 "satisfactory" · 중간 호 **139 → 307 Ω cm²(×2.2)** · Warburg 표지 14 → 16 · "cannot be decorrelated" · "no way to identify which electrode" · TiS₂ `R_CT` "only indicative … fit is not altered upon removal". ⚠ 폭(근최적 집합) 0 · 상태 하나 · n 산포 0 |
| ★★ **역방향 반쪽 짝 — 한 셀 두 반쪽에서 박리 · 도금(양극이면 충 · 방)을 동시에** (2026-09-23 후보, **46호에서**, `[해석]`) | 면적(형태) 가설은 두 반쪽 계면 저항의 **부호가 반대**, 단조 계면층 성장은 **같은 부호**를 예측한다 — 곱 `A_geom × f_pass` 의 두 인자를 방향으로 가른다 | ⚠ **46호**: 박리 쪽 R3 ↑(`[도표]` ≈1.5 → 8.8 Ω) · 도금 쪽 전체 ↓ — 그러나 도금 쪽은 유도성으로 성분 분리 실패(`[인쇄]` "separation … impossible"), 짝이 반쪽만 남았다. 한 반쪽에만 이상 특징이 있으면 45호 3-b 거름망부터 |
| ↳ **창 규약 줄 — 시간 영역 성분은 창 경계 · 대역 끝 · 대응 규약 · 진폭과 함께 적는다** (2026-09-23, **49호에서**, ⚠ 액체) | 4단계(시간 ↔ 주파수) · 20호 번역 · 34호 온보드 펄스에서 `R₀`/`R_CT`/`R_p` 를 쓸 때 (i) **각 성분이 몇 초(몇 Hz)에서 몇 초까지의 차분인지** (ii) **대역 위쪽 끝**(샘플 간격 · 여기 최고 주파수 — 직렬 R 이 그보다 빠른 모든 과정을 흡수한다) (iii) **대응 규약**(t = 1/f · 1/(2πf))과 그 대역의 \|Z\| 기울기(일치 판정의 분해능) (iv) **전류 진폭** (v) ECM 총량이면 최저 여기 주파수 밖 **외삽**인지를 값 옆에 적는다. 1단계(`R·C`) · 3-b(`C = τ/R`)의 τ 도 이 창에서 나온다 | ★★ **49호**(상용 20 Ah LFP/흑연, 한 상태): `[재현]` 총량 5 C `ΔV/ΔI(t)` ↔ EIS \|Z\|(1/t) −6 … +11 % · 규약을 1/(2πf) 로 옮기면 −13 … −23 % · 같은 이름 `R₀` ×2.0 · `R_CT` ×2.9 · `R_p` ×13 · EIS `R_p` 경계만 ×3.9 · 0.1 s `R₀` = \|Z\|(10 Hz) +43 % · 다중사인 `R₀` = \|Z\|(1 Hz) · 10 s 창 진폭 ×1.46 · 다중사인 총 2.83 = ω→0 외삽(최저 여기 ≈1.98). ⚠ 액체 · 셀 수 미인쇄 · 그림 판독 |
| ★★★ **면적 정규화 규약 — 모형 수정 하나가 곱을 정확히 재척도한다** (2026-09-23 신설, **50호에서**) | TLM 계면 항은 `Z_loc/(a_v·ℓ)` 로만 들어가므로 `ℓ = τd ↔ d` 같은 교체는 `(j₀, Q_DL, dU/dc) → (j₀/s, Q_DL/s, s·dU/dc)` 와 **같은 스펙트럼**이다. 보고 `j₀` 옆에 (i) 면적 규약(구 기하 `3ε/r` · BET · τ 포함 여부) (ii) 비교 대상 편의 규약 (iii) **적합 `dU/dc` ÷ OCV 기울기**(저주파 화학 용량 `F·ε·d/\|dU/dc\|` 이 모형 안 면적 척도의 유일한 닻 — **용량성 극한에 닿을 때만**, 반무한이면 38호 줄의 `s·√D/\|dU/dc\|` 로 약해진다)를 적는다. 규약이 다른 편끼리의 `j₀` 비교는 방향까지만. ★ **1단계를 편 사이로 걸 때**(같은 분말 · 같은 규약 · 다른 SE) `C ∝ θ` 전제가 SE 교체로 약해진다는 것을 같이 적는다 | ★★★ **50호**(LCO · NMC83 \| LPSI \| In, 389 MPa, 두께 4 점): `[인쇄]` 수정 (ii) "should be better described by `a_v d`" — `[재현]` 식 (1)이면 `j₀` LCO 25.8 → 4.2 · NMC 0.11 → 0.016 A m⁻², "almost 2 orders" 의 ×6.1 이 이 줄 · `dU/dc` 적합/시작 ×1.31 · ×1.07 · 같은 지면 LCO ↔ NMC τ_CT ×106(면적 아님) ↔ 16호 ↔ 50호 NMC τ ×1.28(`1/R` ×12.1 · `C_eff` ×15.4 — **면적 서명**). ⚠ n 미인쇄 · Brug 근사 · NMC 비교 창 0.01 Hz 는 반무한(ωτ ≈10³) |
| ★★ **`C` 의 자리 — 저항과 같은 계면인가, 여집합인가 · 그리고 `Ea` 판별값은 계 고유** (2026-09-23 신설, **51호에서**, ⚠ 액체) | 1단계의 "τ 보존 = 면적" 은 `C` 가 **저항과 같은 계면**(접촉 면의 이중층)에 있을 때만 선다. 전자 접촉 호(집전체 \| 전극층)처럼 `C` 가 **비접촉 면(여집합)** 에 있으면 접촉 증가는 `R` ↓ · `C` ↓ 로 τ 를 두 인자로 줄인다 — 같은 규칙이 면적 변화를 면적 아님으로 판정한다. 호에 1단계를 걸기 전 (i) **`C` 가 어느 면에 있는지** 적고 (ii) 3-a 로 호에 정체를 붙일 때는 판별 문턱을 **같은 계의 대조**(18호 Al\|복합체\|Al 대칭셀 같은)로 잰다 — 액체의 "`Ea` ≈ 0 = 접촉" 을 옮기지 않는다 | ★★ **51호**(LFP\|LiPF₆\|Li, 한 셀): `[인쇄]` P1C 0.45 · P2C 0.06 eV · 식 (9) 한 줄 · `[재현]` Table I → `C` P2C ≈1 µF · P1C ≈3 mF cm⁻²(두 호 ×≈3,000, 각 호 온도 불변 — 표 주파수 열을 뒤집어야) · `[도표]` 캘린더링 τ P1C ×≈3.5 · P2C ×≈1/6 · Fig. 15 도식 P2C CPE → 비접촉 집전체. ↔ 18호 ASSB R2(전자 계면) `Ea` 41–70 kJ mol⁻¹ 가 R3(전하이동) 49–63 과 겹침. ⚠ 이상 RC · `n` 미인쇄 · 도식은 문장 아님 · 캘린더링은 네 원인 동시 |
| ★★ **누적 충–방 결손 ↔ Li 재고 상한 — 2전극 CE 를 `LLI` 로 쓰기 전의 검사** (2026-09-23 신설, **52호에서**, `[재현]`) | 곱을 가르기 **전 단계**: 2전극 용량 손실을 `LAM_PE` · `θ` · `LLI` 로 나눌 때 흔히 CE 결손을 `LLI` 로 고정한다. Σ(Q_ch − Q_dis) 를 양극 이론 Li 재고 · 형성 때 음극에 남은 저장소 · 관측 용량 손실과 대조하면 **CE 결손 중 재고 손실일 수 없는 몫**(누설 · 부반응)의 하한이 나온다. 조건 간 비교는 **면적당 결손**으로, 끝 전극 모드(양극이 방전 끝을 내면 `LLI` 는 CE 에 안 보인다)를 먼저 | ★★★ **52호**(Oh 2025 *AEM*, NCM811 \| LPSCl \| MgSiGr 과충전, N/P < 1): 20 MPa 평균 CE 99.2 %(`[인쇄]`) ↔ 유지율 83.7 % — 결손 ≈95 ↔ 손실 ≈27 mAh g⁻¹ · **3 MPa `[도표]` CE ≈85–97 %, 누적 결손 ≈575 mAh g⁻¹ > NCM811 재고 ≈275** · 면적당 ×≈1.8(CE ×≈7 은 적재 20 ↔ 6 mg). 44호 "Li 재고 수지"(한 사이클, 방전 > 충전)의 **다중 사이클 · 반대 부호 판**. ⚠ 셀 1 · 화소 판독 |
| ★★ **전류 진폭(선형 ↔ 로그) — 직렬 `R_SP` ↔ `R_CT` 를 가르고, 면적은 둘 다에 남는다** (2026-09-23 신설, **53호에서**, 식 + `[재현]`) | 계면 과전압이 `f_BV(i/(a·i₀))` + `(i/a)·R_SP` 로 들어가는 모델 · 셀에서 소신호 EIS 는 두 칸을 **합**으로만 본다(선형화 영역에서 둘 다 옴). 전류 진폭(펄스 여러 크기 · 대진폭 EIS)에 대한 과전압의 **선형 ↔ 로그** 의존이 두 칸을 가른다 — 49호 진폭 줄의 계면 판. 면적 `a`(접촉)는 두 칸 **모두의 분모**라 이 채널로는 안 떨어진다(1 · 2단계가 여전히 필요). 그리고 **입경 손잡이 경고**: `a = 3ε/r` 규약이면 `d50` 스윕은 확산 길이와 면적을 같이 움직인다 | ⚠ **53호**(Ren · Danner 2023, P2D 사례 계산): `[인쇄]` "close to linear dependence of the overpotential on the current density … in this case the overpotential depends logarithmically on the current" 를 적고도 "Deconvolution … is challenging … we assume" 로 한쪽에 몰았다(표는 `R_CT` = `R_SP` = 2600 두 칸). `[재현]` `a·L` ≈22.5(구 기하 가정) · 10 mA: 옴 ≈1.2 V ↔ BV ≈0.20 V; improved(`a·L` ≈2250)에서는 `a` 반감에도 ≈0.7 mV — **면적형 접촉 손실이 전압에 안 보이는 체제가 있다** |
| ★★ **벌크 특성 주파수 ↔ 측정 대역 상한 — SE 벌크 · 입계(또는 SE · 계면) 합을 나누기 전의 검사** (2026-09-23 신설, **54호에서**, `[인쇄]` + `[재현]`) | 직렬 두 저항(벌크 옴 + 입계 · 계면 호)의 합을 나눈 값을 쓰기 전에 `f_C,B = σ/(2πε₀ε_r)` 를 장비 상한과 비교한다. `f_C,B` ≳ 상한이면 **고주파 절편(벌크 저항)은 관측되지 않고**, 벌크 몫은 추정이 아니라 **입력**이다 — 모델 안에서는 벌크 `σ` 가 절편을 옮기고 입계 `i₀₀` 는 안 옮겨 두 파라미터가 갈리지만, 그 채널이 대역 밖이다. 곱 `σ⁰·ε/τ²` 은 **구조 계산**(3D 재구성 굴곡도)으로 뗄 수 있어도 이 합은 안 떨어진다. 대안 채널: 온도(`Ea`) · 입도만 바꾼 시리즈 · 대진폭(벌크 옴 ↔ 입계 sinh). 49호 "창 규약" 줄의 **위쪽 끝**을 SE 에 적용한 판 | ⚠ **54호**(Neumann 2021, LLCZNO 다공층 + BEST): `[인쇄]` 25 % `f_C,B` 1.40 × 10⁷ ↔ 상한 "around 1.5 × 10⁷ Hz" · "the bulk polarization process is not fully resolved" · "an exact deconvolution of both contributions via EIS is unfeasible"; `[도표]` 교정 펠릿 실험 호 시작 Re ≈12 ↔ 모델 벌크 절편 ≈28 Ω cm²; `[재현]` 치밀 `f_C,B` ≈1.8 × 10⁷. 입력 `σ⁰` = 문헌 범위 윗끝(7.69e-4). ★ 1단계 `C` 판독 전제 추가 — 교정된 `C_DL^GB` 9.75e-9 의 벽돌층 등가 두께 `[재현]` ≈6.8 µm(물리 입계의 10²–10³ 배) ⇒ **호 위치 맞춤값은 두께 · 면적 서명이 아니다** |
| ★★ **두 경로(측정 ↔ 구조 계산) 대조는 관측 곱 `σ_eff/σ⁰` 로, 같은 시편 · 같은 `ε` 로** (2026-09-23 신설, **55호에서**, `[재현]`) | 측정(EIS `σ_eff`)과 구조 계산(영상 `ε` + 모의 `τ`)을 비교할 때 **`τ` 끼리 비교하면 각 경로가 고른 `ε` 가 판정을 정한다** — 관측 곱 `ε/τ` 로, 구조가 측정 시편의 것일 때만 곱이 풀린다. 24호 "두 영역 대조의 시편 조건" 줄의 구조 판 | ⚠ **55호**: `τ` 1.6 ↔ 1.74(9 %, "close") · `[재현]` 곱 0.406 ↔ 0.309(31 %) · EIS `ε` 미인쇄(역산 ≈0.65) · 두 시편 수지 · 충전 상태 · 압착 · 두께 차 — 차를 "수지" 하나에 배정 |
| ★★ **`φ` 고정 분포 스윕 — 3D 모델에서 `A_eff ↔ k` 항등의 파괴 검사** (2026-09-23 신설, **56호에서**, 모델 명제 + `[재현]`) | 표면 피복을 넣은 해상 모델에서 (i) 피복률 스윕 (ii) **같은 피복률에서 피복 크기 · 분포 스윕** (iii) **`j₀` 균일 축소(같은 `A·j₀`)** 를 나란히 돌린다. (ii) 가 과전압을 움직이고 (iii) 이 (i) 과 어긋나면 그 계에서 접촉 손실은 `j₀` 의 쌍둥이가 아니다 — 곡선에 **분포의 서명**(입자 내부 확산의 공간 불균일)이 남는다. 37호 줄(식 항등)의 해상판 검사 | ⚠ **56호**: (i) · (ii) 만 — `[도표]` `φ` 70 % 고정에서 크기 비 1.2 → 10 이 0.2 C @50 ≈50 → ≈19 mV(×2.6) · @100 ≈65 → ≈14.5(×4.5); `[재현]` BV 면적 몫은 `A` ≈53 % 에서 ≈21 ↔ 47 mV(≈44 %). (iii) 은 입자형 모델에서만(상수 `j₀` 두 값) — 같은 모델 안 대조 0. 그리고 **"비적합" 선언 옆 이산 선택**(PSD 절단이 면적 0.113–0.173 m² g⁻¹ 를 정함)이 곱의 면적 인자를 실험 일치로 골랐다 |

★ **`R_CT·C_dl` 줄이 우리가 바로 할 수 있는 것이다.** 필요한 입력은 두 가지뿐:
반쪽전지 OCP 두 곡선(원전이 출처를 안 적었다)과 비공개 6 개 파라미터.

★★★ **2026-09-22 정련 (19호)**: 처방이 **세 단계로 자랐다.**
**16호** "두 값을 같이 보고하라" → **18호** "두 값 **+ 면적을 아는 대조군**" →
**19호** "두 값 + 면적을 아는 대조군 **+ `C` 의 절대 크기가 물리 상한 안인지**
**+ 면적-불변 채널 `Ea` 를 같이 재라**".
그리고 **대조군의 형태**도 19호가 보여 준다 — **"같은 재료 · 같은 공정 · 계면 하나만
추가"**(SE 펠릿 한 장 ↔ 두 장 적층). 복합양극 판으로 옮기면 **같은 활물질·SE·공정에서
계면 수/면적만 바꾼 전극 쌍**이다.

## ⚠⚠ EIS 는 대가를 받는다 — 두 번째 축퇴가 따라 들어온다 (2026-09-22, `assb` 10호)

위 처방표의 "다중 SOC EIS" 는 **곱을 주파수로 가르자**는 것이었다. 그런데
`assb` 10호(Vadhva et al. 2021, *ChemElectroChem* 8, 1930 — 이 분야 **유일한 EIS
방법론 리뷰**)를 넣고 보면 **그 통로에 다른 축퇴가 이미 앉아 있다.**

**(가) 같은 저항에 두 기구가 귀속된다.** In|LGPS|LCO 완전지의 SoC 분해 EIS 에서
중주파 **양극 계면 저항**의 증가를 원전이 이렇게 설명하고 리뷰가 그대로 옮긴다:

> `[인쇄]` "attributed to **loss of interfacial contact in the composite cathode
> due to volumetric expansion** **and** the **formation of a decomposition layer
> on exposed LCO**"

`[해석]` **접촉 손실**(우리의 `θ_AM`)과 **계면상 성장**(진짜 화학 열화)이
**하나의 `R_MF` 안에서 합쳐진다.** 가르는 관측은 원전에도 리뷰에도 없다.

**(나) 그리고 EIS 의 역문제도 유일하지 않다.** 같은 리뷰 §2.3 (`[인쇄]`):
- "**As no solution to an EIS spectrum is unique**"
- "**the inclusion of more elements will tend to improve the fit** of the
  equivalent circuit model" → **적합 잔차는 모델 선택의 근거가 못 된다**
- "it is often challenging to **decipher how many time constants are present** …
  their assignment can be **highly subjective**"
- DRT 로 개수를 정하려 해도 `[인쇄]` "data inversion is **mathematically
  ill-posed, requiring regularization methods**" 이고 "**very sensitive to
  experimental errors**"

**(다) 분해 가능한 원소의 개수 자체가 조건의 함수다.** 같은 리뷰가 다섯 곳에서
따로 보인다 — `[도표]` 황화물 5 종 중 **3 종만** 입계가 분해되고(같은 −130 °C),
LGPS 는 **실온에서 원호가 0 개**이며, Li|LLZO|Li 는 **400 MPa 에서 `R_int` 가
사라져야 `GB` 가 보이고**, 폴리머는 **60 °C 위에서 상경계 임피던스가 소멸**하며,
`[인쇄]` LiPON 박막은 **노화가 RQ 를 3 → 4 개로 바꾼다**(새 RQ 의 귀속은
`[인쇄]` "Li|LiPON interface **and/or** in the LCO bulk").

```
        시간·용량 영역 축퇴  ×  주파수 영역 축퇴  =  실제로 풀어야 할 문제
        (A_eff·ε_p/R_s)         (R_MF = 접촉 + 계면상)
```

★ **그러므로 처방표의 EIS 항목은 이렇게 고쳐 읽는다**: **EIS 단독으로는 안 되고,
"한 기구만 되돌리는 개입" 과 짝지어야 한다** — [[assb-pressure-reapplication-separation-test]]
의 `P↑`(접촉만 복원) 또는 상보 **대칭셀 쌍**(전극별 분리). 10호가 드는 유일한
"전극 귀속을 실제로 확정한" 사례도 주파수 추론이 아니라 **대칭셀 둘을 같은 조건으로
잰 것**이다(He 2017, LFP|PEM|LFP ↔ Li|PEM|Li).

★★ **보너스 — `P↑` 는 분해능 연산자이기도 하다.** `[도표]` 400 MPa 에서 `R_int` 가
사라지자 그 뒤에 숨어 있던 `GB` 원호가 드러난다. **압력은 `θ_AM` 을 되돌릴 뿐
아니라 관측 가능한 시상수의 개수를 바꾼다** → [[assb-stack-pressure-operating-window]].

⚠ **10호는 리뷰다** — 1차 측정 0, `contact loss` 0 회(위 인용구가 전부),
`identifiab*`·`uncertaint*` 전수 0 회. **재지 않았다.** 위에서 쓰는 것은 수치가
아니라 **방법론적 주장**이다.

## ★ 이 모델 형태는 9호 고유가 아닐 수 있다 — `A_eff` 의 계보 입구 (2026-09-22, `assb` 12호)

`assb` 12호(Sadegh Kouhestani et al. 2022, *Energies* 15, 6599 — ⚠ **PHM 종설, 1차 측정 0**,
`raw/papers/kouhestani2022_phm-solid-state-batteries-perspective.md`) §3.1.1 이 한 문장으로
같은 형태를 소개한다:

> `[인쇄]` "Tian et al. [60] and Shao et al. [60] introduced **a parameter to describe the
> contact area, which adjusts the current density in the 1-D Newman model**. They found
> that **the capacity drop was correlated with the loss of contact area**, and the optimal
> charging performance could be obtained under medium compressive pressures (0.4–1 MPa)."

`[해석]` "접촉 면적을 기술하는 파라미터가 1D Newman 모델의 **전류밀도를 조정**한다" 는
위 §정의의 `j^p_ct = (I − I^p_dl) / (A^p_eff · a_{s,p} · A · L_p)` 와 **자리가 같다** —
BV 분모의 유효 면적 인자. 즉 이 페이지가 손으로 보인 `A_eff · ε_p / R_s` 곱 축퇴는
**Huo 2025 가 만든 형태가 아니라 2017 년(Tian & Qi, *JES* 164, E3512)부터 있던 형태**일
가능성이 높고, Shao 2022 (*Energy* 239, 121929) 가 거기에 **압력 의존**을 얹었다.

**이것이 이 페이지에 뜻하는 것 둘**:
1. `evidenceScope: single-source` 는 **이때는 유지했다** — 12호는 식을 인쇄하지 않았고,
   원전 둘을 우리가 읽지 않았다. 다만 §"주장하지 않는 것" 의 "P2D 계열에 널리 반복될
   가능성" 이 **한 문장의 문헌 근거**를 얻었다.
   → **2026-09-22 늦게 `multi-source-primary` 로 승격**했다. 근거는 12호가 아니라
   **16호(식을 인쇄한 두 번째 1차 문헌)** 다 — 아래 §"두 번째 출처".
2. ★ Shao 2022 가 정말 `A_eff = A_eff(P)` 를 넣었다면, **압력 되돌림 연산자**
   ([[assb-pressure-reapplication-separation-test]])가 **모델 안에 이미 들어 있는** 첫 사례다
   — 그러면 곱 축퇴를 깨는 "다른 반응을 하는 자극" 이 그 모델에서는 **압력**이 된다.
   확인 전이다.

⚠ **단서**: 12호는 두 저자에 **같은 인용번호 [60]** 을 붙였다(Shao 는 [63] 이어야 한다).
그래서 `0.4–1 MPa` 가 어느 쪽 결과인지 **그 지면으로는 확정되지 않는다.** 이 절의 수치는
쓰지 않고 **형태**만 쓴다. 9호(Huo 2025)가 Tian & Qi 를 인용하는지도 **확인하지 않았다**.

## ★★★ 두 번째 출처, 그리고 **실측 판** — 16호가 같은 곱 위에 서서 한쪽 끝을 고른다 (2026-09-22)

`assb` 16호 (Ramanayagam, Miß, Leier, Duncker, Kirczek, Roling 2026, *Batteries & Supercaps*
**9**, e70315, `raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md`)
는 **3전극 실측 + TLM 적합**이다. 9호가 **모델 논문**이었다면 16호는 **실험 논문**이고,
**같은 구조가 EIS 쪽에서도 나타난다**는 것을 보인다.

### 정의 — 같은 자리, 다른 이름

원전의 **인쇄된 식** (`[인쇄]`):

```
식 (4)   a_V = 3·ε_CAM / r_CAM        캡션: "The area of the CAM particles in CONTACT with the SE
                                       normalized to the cathode volume"   ← 접촉 분율 인자가 없다
식 (5)   R_CT = R·T / (F · j₀)
극한 (i) 얇은 전극:  R_semicircle = R_CT / (a_V · d)
```

`[해석]` 합치면:

```
      ★  측정량이 보는 것 =  R·T·r_CAM / ( 3·F · j₀ · ε_CAM · d )
         ⇒ 식별되는 조합은   j₀ · ε_CAM / r_CAM   하나  ★
```

**9호의 `A_eff · ε_p / R_s` 와 같은 자리다.** 다른 점은 **`A_eff` 가 아예 없다는 것** —
16호는 접촉 분율을 **변수로 두지 않고 1 로 못 박는다.** 그러면서 **그 양에 "접촉 면적"
이라는 이름을 붙인다.**

### ★★★ 배정의 자유 — 같은 데이터, 반대 결론

논문의 배정(`ε_CAM`·`r_CAM` 고정): **`j₀` 0.74 → 1.33 A m⁻² (1.80 배 증가)**
(97 → 389 MPa). 그런데 **같은 Table 2 가 이중층 CPE 계수도 준다**:
**`Q_DL` 0.18 → 0.54 (3.0 배)**, `β` 0.81 → 0.89.

접촉 분율 `θ` 를 넣으면 — **두 양이 같은 가정 면적 `a_V` 로 정규화되므로**:

```
R_CT^meas = R_CT^true / θ         C^meas = θ · C^true
⇒ R_CT^meas · C^meas = R_CT^true · C^true      (★ θ 가 소거된다)
⇒ C^meas 단독은 θ 에 비례                        (★ θ 를 직접 준다)
```

| 배정 | `θ(389)/θ(97)` | `j₀^true(389)/j₀^true(97)` | 원전의 **말**과 |
|---|---:|---:|---|
| **논문 (`θ ≡ 1`)** | 1.0 | **1.80 (증가)** | 수치 결론 |
| **`Q_DL` 을 면적으로 읽음** | **3.0** | `[재현]` **0.60 (감소)** | `[인쇄]` "pressure improves the **interfacial contacts** between SE particles and CAM particles **considerably**" 와 정합 |

`[재현]` 둘째 행: `j₀^true ∝ 1/(θ · R_CT^meas)` ⇒ `(1/3.0) × 1.797 = 0.60`.

★★★ `[해석]` **같은 데이터가 `j₀` 의 증가와 감소를 둘 다 허용한다.** 그리고 원전의
**문장은 둘째 배정을 말하고 숫자는 첫째 배정을 쓴다.** 이것이 이 페이지가 9호에서
**식으로** 보인 것의 **실물**이다.

★ **단서 셋 (전부 우리가 붙인다)**:
1. `β` 가 0.89 ↔ 0.81 로 달라 **두 `Q` 는 엄밀히 차원이 다르다**(F sᵝ⁻¹ m⁻²).
   `[재현]` Brug 류 유효용량(`C = Q^{1/β}·R^{(1−β)/β}`)으로 고치면 비가 **3.0 → ≈5.6** —
   **방향은 그대로이고 세진다.**
2. 이중층 **비용량**이 압력에 무관하다는 가정이 필요하다.
3. `[재현]` **`R_CT·Q` 가 두 압력에서 같지 않다**(1.67 배; 유효용량으로는 3.1 배)
   ⇒ **순수 면적 효과만으로도 설명되지 않는다.** 즉 **세 번째 배정**(면적도 변하고
   고유 동역학도 변한다)이 가장 그럴듯하고, **원전은 세 배정 중 어느 것도 고를 관측을
   갖고 있지 않다.**

### ★★ 그래서 나오는 처방 — `R_CT · C_dl` 채널

> **`R_CT·C_dl` 은 접촉 면적이 소거된 고유 시상수이고, `C_dl` 단독은 접촉 면적에 비례한다.
> 둘을 같이 보고하면 `θ` 와 `j₀` 가 갈린다.**

이것이 위 §처방표의 새 행이다. **원전은 두 값을 다 갖고 있으면서 그 조합을 만들지 않는다.**
⚠ 우리도 **아직 재지 않았다** — 여기 적는 것은 **설계**다. 그리고 CPE(β<1)가 개입하면
변환이 **모형 의존적**이어서, 이 채널을 쓰려면 **`β` 를 압력 간에 고정하거나 유효용량
변환을 명시**해야 한다. 원전 데이터는 `[인쇄]` "available **on request**" 라 재적합 불가.

### ★ 같은 논문 안에서 서사가 전극마다 바뀐다

`[도표]` 16호 **Figure 5**(음극 모식도)는 압력이 바꾸는 것을 **"interphase 를 통하는 칸의
개수"** 로 **그림으로 명시**한다 (저압 통함 3/8 ↔ 고압 5/8). 즉 **음극에서는 면적 서사**다.
그런데 같은 논문의 **양극 TLM 은 면적을 고정**하고 `j₀` 를 움직인다 — **동역학 서사**.
`[해석]` **전극이 바뀌면 같은 현상의 이름이 바뀐다.** 이것은 저자의 실수라기보다
**두 배정이 관측상 구별되지 않기 때문에 생기는 자유**다 — 이 페이지의 논지 그 자체.

### 이 절이 페이지의 `evidenceScope` 에 하는 일

`single-source` → **`multi-source-primary`**. 근거 둘:
① 9호 Huo 2025 — **P2D 모델의 인쇄된 식**(`A_eff·ε_p/R_s`, 방전곡선 적합)
② 16호 Ramanayagam 2026 — **TLM/EIS 의 인쇄된 식**(`j₀·ε_CAM/r_CAM`, 임피던스 적합)
**다른 모델족 · 다른 관측 · 다른 그룹 · 다른 나라**인데 **같은 자리에서 축퇴한다.**
⚠ `confidence` 는 **medium 유지**다 — **두 편 다 축퇴를 재지 않았고**(`identifiab*` 0/0),
우리도 아직 폭을 재지 않았다. 근거 폭이 늘었을 뿐 **측정은 여전히 0 편**이다.

## ★★ 처방의 첫 적용 (2026-09-22, `assb` 17호) — **적용 불가, 그리고 그 이유가 정보다**

`raw/papers/yanev2024_li-in-alloy-anode-kinetic-limitations.md`
(Yanev et al. 2024, *JES* 171, 020512, Editors' Choice — 3전극 Li-In/NCM811).

### 판정: 입력이 없다

| 처방 입력 | 17호에 있나 |
|---|---|
| `R_CT` | **없다** (`fit*` **0 회**) |
| `C_dl` / `Q_DL` / `CPE` | **없다** (`capacitance`·`CPE` **0 회**) |
| 등가회로 | **없다** (`equivalent circuit`·`ECM`·`DRT` **0 회**) |
| 면적 인자 `a_V` / `θ` | **없다** (기하 계산 0) |

> `[인쇄]` "Detailed quantitative analyses and **modelling of the impedance spectra are
> beyond the scope of this study**."

⇒ **세 편의 실패 양식이 전부 다르다**:
**9호 = 곱을 적합했다** · **16호 = 곱 위에 서서 한쪽 끝을 골랐다(`θ ≡ 1`)** ·
**17호 = 곱을 만들지 않았다.**
`[해석]` **역설적으로 17호가 가장 안전하다** — 배정하지 않았으므로 잘못 배정할 수 없고,
그 편의 결론은 적합이 아니라 **세 번째 전극의 전압계 판독**에서 나온다.
대신 **정량이 0 이라 이 페이지가 가져갈 숫자도 없다.**

### ★★ 그래도 17호에 곱 축퇴가 있다 — 다른 자리에서, 문장으로

논문의 인과 주장이 **같은 조작을 두 이름으로** 부른다:

> ① `[인쇄]` "the Li depletion is primarily a function of the **contact surface between
>    the SE and LiIn**"
> ② `[인쇄]` "a … well-percolated composite anode with **high effective contact area**
>    to the separator"
> ③ `[인쇄]` "By increasing the sulfide content from 20 wt% to 40 wt% a further slight
>    performance increase is observed, which **confirms that the effective ionic
>    conductivity of the Li-In anode plays an important role**"

**SE 분말을 넣는 조작 하나가 (i) LiIn↔SE 접촉 면적과 (ii) 음극 유효 이온전도도를 동시에
올린다.** 둘을 따로 움직인 실험이 **없다.** 곱은 아니지만 **공변(co-varying) 두 인자**이고
데이터는 그 둘의 어떤 조합만 본다 — **이 페이지의 구조와 같다.**

★★★ **그리고 그 배정이 숫자로도 안 받쳐진다** `[재현]`:
- 2전극 총 임피던스 `[도표]` SE **20 % ≈36 Ω → 40 % ≈27 Ω**, **Δ ≈9 Ω (−25 %)**
- 그런데 `[도표]` Fig. 5b 에서 **40 % SE 복합 음극의 임피던스 전체가 ≈6 Ω** 이다
⇒ **Δ 9 Ω 을 음극에 다 줄 수 없고, 3전극은 40 % 쪽만 쟀다.**
남는 통로는 **양극/분리막의 셀 간 산포**인데, 같은 논문의 두 3전극 셀에서
`[재현]` **분리막 저항 배분이 30.5 : 69.5 ↔ 69.4 : 30.6 으로 뒤집힌다**
(총합은 41–43 Ω 로 5 % 안에서 같다 — RE 를 `[인쇄]` "roughly through the middle" 에
두었다는 진술의 실측값이다). ⇒ ③의 "confirms" 는 **전극 분해 근거가 0 이다.**

### ★★★ 17호가 이 페이지에 더하는 항 — **음극 오염**

> `[인쇄]` "**the deconvolution of half-cell impedance spectra** e.g., when
> characterizing **cathodic charge transfer phenomena**, could be **severely
> complicated by overlapping anode impedance**."

★★★ `[해석]` **이것은 9호·16호의 양극 적합이 딛는 자리에 대한 직접 경고다.**
16호가 `j₀ · ε_CAM / r_CAM` 를 **양극의 것**으로 읽을 때, 그 스펙트럼에 음극이 얼마나
섞였는지는 **16호도 우리도 모른다.** 17호가 보여 주는 크기는 작지 않다 —
`[재현]` **foil 셀에서 음극의 실축 기여가 ≥58 Ω 이고 양극 전체(≈31 Ω)의 2 배 가까이**이며,
**2전극 스펙트럼에서 그 둘은 한 곡선이다.**
⇒ **처방표에 한 줄 더**: **다중 SOC EIS 를 쓰려면 3전극(또는 상보 대칭셀)으로 음극
기여를 먼저 빼야 한다.** 16호는 3전극이었고(✔), **9호는 2전극이었다**(✗).
⚠ 단 3전극에도 값이 있다 — 17호 `[재현]` 합산 검사가 **2 Hz 에서 1 % 안**으로 맞지만
**고주파 절편은 foil 셀에서 7 % 어긋난다**(음극 임피던스가 거대할수록 아티팩트가 크다).

★ **그리고 그 음극이 얼마나 움직이는가는 이제 별도 페이지가 있다** —
[[assb-li-in-reference-potential-window]] (같은 공칭 조성의 두 Li-In 음극이 전류 ≈0 에서
`E_CE` 0.61 ↔ 1.35 V). **음극 임피던스뿐 아니라 음극 전위도 배정을 오염시킨다.**

## ★★★★ 처방의 두 번째 적용 (2026-09-22, `assb` 18호) — **첫 성공, 그리고 전제의 발견**

`raw/papers/fukunishi2023_ncm523-three-electrode-impedance-degradation.md`
(Fukunishi et al. 2023, *J. Power Sources* **564**, 232864 — 3전극 NCM523/Li-In,
LPSI·LPSCl 두 전해질, **1.0 C × 50 사이클 열화**).

### 입력이 처음으로 다 있다

| 처방 입력 | 9호 | 16호 | 17호 | **18호** |
|---|---|---|---|---|
| `R_CT` | 적합 1 개 | Table 2 | **없다** | ✅ **Table S1(신품 3 온도 × 2 입경) + Fig. 5(노화 전후 × 2 계)** |
| `C_dl`/`Q`/CPE | **없다** | Table 2 | **없다** | ✅ **Table S1 `CPE2-C` + Fig. 5 의 `τ`** |
| CPE 지수 `p` | — | β 0.89/0.81 | — | ✅ Table S1 (⚠ **노화 후는 없다**) |
| 면적을 바꾼 조작 | **없다** | 압력 2 점 | **없다** | ✅ **입자 크기 2 점** + ✅ **노화 전후** |
| **판정** | 곱을 적합했다 | 한쪽 끝을 골랐다(`θ≡1`) | 곱을 만들지 않았다 | ★ **우리가 곱을 만들었다** |

### ★★★★ 검사 B (열화 축) — 저자가 인쇄한 "or" 가 갈린다

18호는 우리 물음을 **문장으로 인쇄하고 가르지 않는다**:

> `[인쇄]` "R3 drastically increased (6 times larger) … These results suggest that the
> **chemical composition at the interface or the contact area** between the NCM523 and
> electrolyte particles changed."

**면적만 잃으면** `R ∝ 1/θ` · `C ∝ θ` ⇒ **`C` 비 = 1/(R 비)**.
**고유 동역학만 나빠지면** `C` 비 = **1.00**.
`[재현]` (`C ≡ τ/R`, Fig. 5 로그 막대 판독 ±0.04 ⇒ `C` 비 상대오차 ≈±18 %):

| 계 · 항 | `R` 비 | `τ` 비 | **`C` 비** | 순수 면적 | 순수 동역학 | 판정 |
|---|---:|---:|---:|---:|---:|---|
| **LPSI · R3** | 6.5 | 2.4 | **0.37 ± 0.07** | 0.15 | 1.00 | **둘 다** — 유효 면적 ≈2.7 배 감소 + 고유 `R_ct` ≈2.4 배 증가 |
| **LPSCl · R3** | 7.4 | 7.9 | **1.07 ± 0.19** | 0.13 | 1.00 | ★ **면적 손실 없음 — 전부 고유 동역학** |
| LPSI · R4 | 9.3 | 5.3 | 0.56 ± 0.10 | 0.11 | 1.00 | 둘 다 |
| LPSCl · R4 | 3.4 | 21 | **6.3** | 0.30 | 1.00 | ⚠ 비물리 — `R4` 가 2.8 Ω 로 작아 안 정해진다 |

★★★★ **그리고 이 분해가 같은 논문의 독립 관측과 일치한다**: `[인쇄]` **LPSI 에만**
2차 입자를 두르는 **O·P 퇴적층(2 µm)**이 생겼고 LPSCl 에는 `[인쇄]` "**not apparent**".
**덮으면 면적이 준다** ⇒ LPSI 0.37 ✔ · LPSCl 1.07 ✔.
⇒ **처방이 실제로 무언가를 갈랐다 — 그리고 두 번째 관측이 그 결과를 지지한다.**
★ 요점은 **새 실험이 아니라 같은 표의 두 열을 곱한 것**이라는 데 있다.

### ⚠⚠ 검사 A (신품, 입자 크기 축) — **처방의 전제가 흔들린다**

18호의 신품 논증: `R3` 비 0.5 = 접촉 면적 비 2.0–2.4 의 역수 ⇒ `[인쇄]` "uniform
physical contact". **면적이 유일한 차이라면 `C_dl` 도 2.0–2.4 배여야 한다.**
`[재현]` (`C_eff = Q^{1/p} R^{(1-p)/p}`):

| T | `R3(11.2)/R3(5.0)` | **`C_eff(5.0)/C_eff(11.2)`** | `p` 가 같나 |
|---|---:|---:|---|
| 283 K | 1.88 | **2.26** | ❌ 0.57 ↔ 0.76 |
| **293 K** | 2.10 | **0.68** | ✅ |
| **303 K** | 2.05 | **1.10** | ✅ |
| 면적 설명의 예측 | 2.0–2.4 | **2.0–2.4** | |

⇒ **`p` 가 같은 두 온도에서 2–3 배 어긋난다.** 맞는 유일한 온도는 **`p` 가 달라 두 `Q` 의
차원이 애초에 다른** 온도다.
⚠ **"반증" 으로 적지 않는 이유**: `[재현]` **같은 계면의 `C_eff` 가 283/293/303 K 에서
5.82 / 1.32 / 1.49 µF 로 4.4 배 움직인다.** 이중층 용량이 20 K 에 4 배 변하는 물리는 없다
⇒ **`Q` 는 이 적합에서 잘 안 정해지는 파라미터**이고, **Table S1 에서 ± 가 빠진 유일한
열이 `CPE2-C`·`τ3`** 다.

★★★ **그래서 처방이 한 단계 정련된다**:

> **`R_CT·C_dl` 채널을 쓰려면 `C_dl ∝ 접촉 면적` 을 먼저 검증해야 한다.**
> 검증 수단은 **면적을 아는 조작**(입자 크기·로딩)이고, 18호는 그것을 갖고 있으면서
> **우리 계산으로는 통과하지 못한다**. 즉 **처방은 "두 값을 보고하라" 가 아니라
> "두 값 + 면적을 아는 대조군을 같이 보고하라" 여야 한다.**

⚠ **세 가지 대안을 18호는 검토하지 않는다**: (ㄱ) 두 입경 시료의 **고유 전하이동 속도가
다르다**(코팅 두께·표면 상태), (ㄴ) `C_dl` 이 접촉 면적의 대리가 아니다(**LiNbO₃ 유전층**이
용량을 지배), (ㄷ) **적합이 `R`–`Q` 를 교환한다**.

### 부수 결과 — 절대 스케일 (⚠ 가정 위, 인용하지 않는다)

`[재현]` 이중층 비용량을 **10 µF cm⁻²** 로 놓으면 293/303 K 의 `C_eff` 는 **실면적
0.13–0.15 cm²** 에 해당하고, 같은 전극의 NCM 기하 표면적은 18호 자신의 식 (4)
`S_w = 3M/(dr)` 로 **7.5 cm²** 다 ⇒ **활성 접촉이 입자 표면의 ≈2 %.**
⚠⚠ **이 숫자를 쓰지 않는다** — 비용량은 우리 가정이고 `C_eff` 가 4 배 흔들린다.
**다만 방향은 분명하다**: `[인쇄]` "completely immersed" · "uniform physical contact" 와
자기 용량 데이터가 맞지 않는다. ⇒ [[composite-cathode-percolation-utilization]] 의
`θ_AM` 이 **1 에 가깝다는 가정이 실측 지면 안에서 근거를 잃는 첫 자리**다.

## ★★★★ 처방의 세 번째 적용 (2026-09-22, `assb` 19호) — **부분 적용 + 전제 반증 + 대체 채널 획득**

`raw/papers/yoshida2024_four-electrode-assb-cell-li-transport.md`
(Yoshida, Ikezawa, Okajima, Arai, *Electrochim. Acta* **497** (2024) 144523, **CC BY**).
★ **18호와 같은 연구실**이고, **4전극 셀로 SE\|SE 계면 하나만** 잰다 — **전극이 없다.**

### 입력이 처음으로 완비된다

| 처방 입력 | 9호 | 16호 | 17호 | 18호 | **19호** |
|---|---|---|---|---|---|
| `R` | 적합 | Table 2 | 없다 | Table S1 + Fig. 5 | ✅ **Table 2**(3 셀 × 2–3 성분) |
| `C` / CPE `Q` | 없다 | Table 2 | 없다 | Table S1(± 없음) | ✅ **Table 2 — 저자가 Brug 식 [27]로 직접 계산해 인쇄** |
| CPE 지수 `p` | — | 0.89/0.81 | — | Table S1 | ✅ **0.55 – 0.96** |
| 면적을 바꾼 조작 | 없다 | 압력 2 점 | 없다 | 입자 크기 2 점 + 노화 | ✅ **압력 2 점 · 단면적 3 점 · 계면 유무 대조** |
| **면적을 아는 대조군** | 없다 | 없다 | 없다 | ⚠ **실패** | ⚠ **있다(`S` 3 점 · 계면 유무) — `C` 가 그 축에 안 붙어 있다** |
| **판정** | 곱을 적합 | 곱 위에서 골랐다 | 곱을 안 만들었다 | ★ 갈랐다 | ★ **부분 + 전제 반증 + 대체 채널** |

`[재현]` **식 검산**: 저자의 식 (1) `C = (Q·R)^{1/p}/R` 로 (a) P1 → **2.35×10⁻¹⁰ F**
(인쇄 2.3×10⁻¹⁰), (a) P2 → **3.6×10⁻³ F**(인쇄 3.8×10⁻³). **`C` 열은 재현된다.**

### ❌ 검사 A — **절대 크기**: 전제 `C_dl ∝ 접촉 면적` 이 두 번째로 깨진다

`[재현]` 계면 반원 `P2` 의 용량 = **1.6 – 3.8 mF**. 기하 단면(φ10 mm = 0.785 cm²)으로
나누면 **2.0 – 4.8 mF cm⁻² = 2000 – 4800 µF cm⁻²**.
이중층 비용량을 **10 µF cm⁻²** 로 놓으면 실면적/기하면적 = **200 – 480 배**.

★★★★ **접촉 면적은 기하 면적을 넘을 수 없다.**
⇒ **`P2` 의 `C` 는 접촉 면적의 대리가 될 수 없다.** 남는 해석 셋을 논문은 검토하지 않는다:
(ㄱ) 화학용량/공간전하 (ㄴ) 거칠기가 아니라 **분포형 요소**(`p` = 0.55–0.61 은 극단적으로
눌린 CPE) (ㄷ) **Brug 변환이 이 `p` 에서 물리 용량을 주지 않는다.**

⇒ ★★★ **전제가 같은 방향으로 두 번 연속 깨졌다.**
**18호 검사 A** = "예측(면적 비 2.0–2.4)보다 **2–3 배 빗나감**" →
**19호 검사 A** = "**물리 상한을 2–3 자릿수 초과**".
`[해석]` **`C_dl` 채널은 "쓰려면 검증하라" 가 아니라 "기본값은 실패" 로 내려간다.**

### ⚠ 검사 B — **셀 간 축**: `C` 채널과 `Ea` 채널이 **70 배 충돌**한다

`[재현]` `P2` 세 셀:

| 셀 | `R₂`/Ω | `C₂`/mF | `τ₂ = R·C`/ms | `Ea(R₂)`/kJ mol⁻¹ |
|---|---:|---:|---:|---:|
| LGPS \| LPSI | **12** | **3.8** | 46 | **27 ± 3** |
| LPSI \| LPSCl | **21.5** | **1.7** | 36 | **41 ± 3** |
| LGPS \| LPSCl | **29.3** | **1.6** | 46 | **42 ± 1** |

- **`C` 채널이 말하는 것**: `τ` 가 **36–46 ms, ±13 % 안**. `R` 비 2.44 ↔ `C` 비 2.375
  (**3 % 안에서 일치**) ⇒ **"세 계면은 유효 면적만 다르다"**(면적 차 **2.4 배**).
  ★ 논문도 같은 관찰을 `[인쇄]` "similar fitting parameters … including the time
  constant … **not different among the three cells**" 로 적는다.
- **`Ea` 채널이 말하는 것**: 장벽이 **15 kJ mol⁻¹** 갈린다.
  `[재현]` 298 K 에서 `A = R·exp(−Ea/RT)` ⇒ **2.21×10⁻⁴ / 1.40×10⁻⁶ / 1.27×10⁻⁶**
  ⇒ **전지수 인자 비 158 – 174 배.**

★★★★ **면적 차 2.4 배 ↔ 158 배 — 두 진단이 70 배 어긋난다.**
⚠ **단서(중요)**: 이것은 **노화 축이 아니라 재료 축**이다. 세 계면은 **물리적으로 다른
계면**이라 "면적만 다르다" 가 애초에 성립할 이유가 없고, **동일 계면의 두 상태**를
비교한 18호 검사 B 와 성질이 다르다. 그래도 **검사 A 가 `C` 쪽을 의심할 이유를 준다.**

### ⚠ 검사 C — **압력 축**: 적용 불가, **18호와 정반대의 결손**

`[도표]` Fig. 8(b) 560 → 840 kPa: `R₁` **−6.5 %**, `R₂` **−26 %**.
**그런데 `C`·`Q`·`p` 가 두 압력에서 인쇄되지 않는다.**
⇒ **면적을 바꾼 조작이 있는데 `C` 가 그 축에 없다.**
(18호는 반대였다 — `C` 는 있고 면적을 아는 조작이 실패했다.)
⚠ 그리고 `[재현]` **조립 기본값 420 kPa 의 `R₂`(21.5 Ω, Table 2)가 560 kPa 의
`R₂`(≈24.7 Ω, Fig. 8b)보다 작다 — 압력 추세와 반대** ⇒ **셀 간 산포가 압력 효과보다
크거나 같은 셀이 아니다. 논문은 둘 다 확인하지 않는다.**

### ★★★★ 대신 얻은 것 — **면적-불변 채널 `Ea`**

> `[인쇄]` "the Ea values of both R1 and R2 **do not show pressure dependence** …
> These results strongly suggest that **the physical state of the interface does not
> affect the Ea but the resistance values**. It is thus proposed **Ea as the essential
> parameter** to describe the nature of the ion transport in this measurement system."

⇒ **`R(T) = A(θ) · exp(Ea/RT)` 에서 `Ea` 는 `θ` 와 직교하고 `A` 만 `θ` 를 탄다.**

| 관측 | 해석 |
|---|---|
| `Ea` 불변 + `R` 증가 | **면적/기하 쪽**과 양립 |
| `Ea` 증가 | **화학/장벽 쪽** — 면적만으로 설명 불가 |

★★ **이 채널의 장점**: `C_dl ∝ θ` 라는 (두 번 깨진) 전제를 **쓰지 않는다.**
⚠ **충분조건은 아니다** — `A` 에 면적 외의 항(시도 빈도·엔트로피)이 있고,
**검사 B 의 158 배 보상이 그 반례다.**
⚠⚠ **그리고 19호의 `Ea` 불변 근거 자체가 약하다**: **2 점 · n = 1 · 범위 1.5 배**,
그리고 같은 편이 드러낸 `Ea` 산포(아래)를 쓰면 **3 kJ mol⁻¹ 변화는 못 본다.**

★★★ **처방으로서의 값은 18호로 되돌아갈 때 나온다**: 18호는 `Ea` 를 **신품 축에서만**
쟀다(입자 크기 × SoC). **18호가 `Ea(노화 전후)` 를 쟀다면 검사 B 의 결론
(LPSI = 면적 ≈1/2.7 + 화학 ≈2.4 배, LPSCl = 화학만)이 `C` 없이 독립 확인됐을 것이다.**

### ★★★★ 그리고 **대조군의 형태**를 보여 준다 — 18호 검사 A 의 대안

`[도표]` Fig. 7: **LPSCl 펠릿 한 장 안에 RE 둘을 함께 성형한 셀에는 `P2` 가 없고**
(Z′ 72→162 Ω, P1 + P3 만), **같은 LPSCl 펠릿 두 장을 포갠 셀에는 `P2` 가 생긴다**(≈8 Ω).
⇒ **같은 재료 · 같은 공정 · 계면 하나만 다른 두 셀.**
`[해석]` **접촉 손실 연구가 원하는 "접촉을 아는 대조군" 의 교과서적 모양**이고,
복합양극 판으로 옮기면 **같은 활물질·SE·공정에서 계면 수/면적만 바꾼 전극 쌍**이다.
⚠ 단서 셋: 두 셀의 `R₁` 이 **162 ↔ 291 Ω** 로 1.8 배 달라 `d`·`S` 가 다르고(값 미인쇄),
`P3` 가 양쪽에 다 있으며 크기가 다르고, **n = 1**.
⚠⚠ **그리고 논문은 이것을 1 차 근거로 쓰지 않는다** — 1 차 근거는 4 점 중 하나가
4.5 배 이상치인 `R₂`–`d` 그림이다(닻 카드 §19호 절 7).

### ★★★ 부수 — 이 편이 주는 **적합 파라미터 산포의 하한**

`[도표]` LPSCl\|LPSCl 셀의 `Ea(R₁)` = **45.5 ± 0.1** kJ mol⁻¹. `R₁` 은 정의상
**LPSCl 벌크뿐**인데 같은 물질의 Table 1 값은 **40.5 ± 0.3** 이다.
⇒ **5.0 kJ mol⁻¹ = 인쇄된 ± 의 12–50 배. 논문 무언급.**
★ 저자 스스로 `[인쇄]` **성형법(냉간↔열간)이 `Ea` 를 11 kJ mol⁻¹ 움직인다**고 적는다.
다른 둘: **Li-In 전극 임피던스 39 ↔ 172 Ω (4.4 배, n = 3)** ·
`[인쇄]` **`P3` 가 셀마다** — `[도표]` **4.8 Ω ↔ ≈35 Ω (7 배)**.
⇒ `[해석]` **등가회로 파라미터를 점추정으로 보고하는 관행의 야생 눈금**이고,
**18호 검사 B 의 단서 (ㄹ)(셀 간 산포 ±20 % 추정)에 붙는 실측 상한**이다.

## ★★★★ 처방의 네 번째 적용 (2026-09-22, `assb` 20호) — **주파수 영역이 없는 편, 그리고 처방이 시간 영역으로 번역된다**

`raw/papers/chang2020_embedded-in-reference-electrode-assb-limiting-factors.md`
(Chang 외 2020, *Ionics* 26, 1555–1561). **2019년 접수 — 이 계보에서 시간이 가장 이르다.**

### 입력 점검 — 1·2단계는 적용 불가

| 처방 단계 | 필요한 입력 | 20호 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R_CT` **와** `C_dl` 을 같이 | `equivalent circuit`·`capacitance`·`C_dl` **0회**, 본문 `impedance` **0회**(5회 전부 참고문헌), `EIS`·`Nyquist`·`DRT` **0회** | ❌ **주파수 영역이 통째로 없다** |
| **2단계** (18호) | + 면적을 아는 대조군 | 셀 **1 개**, 면적 축 없음 | ❌ |
| **3단계-a** (19호) | `Ea` 를 면적-불변 채널로 | 본문 `Ea`·`Arrhenius`·`temperature` **0회** (정규식 2건은 참고문헌 저자 이니셜 "Suslov EA" 오검출, 확인함) | ❌ |
| **3단계-b** (19호) | `C` 가 물리 상한 안인가 | ★ **시간 영역으로 번역하면 있다** | ✅ **적용** |

### ★★★★ 3단계-b 의 번역 — `C = τ / R`, 그리고 즉시 실패한다

20호는 EIS 대신 **단일 정전류 스텝의 3시상수 분해**를 쓴다:
`[인쇄]` `R₀` = 순간 강하 / I · `R_ct` = 이어지는 **비선형** 강하 / I ·
`R_p` = 그 뒤 **~1 h 의 선형** 강하 / I.
⇒ **비선형 구간의 지속이 곧 그 성분의 시상수다.** 따라서 19호의 상한 검사가
그대로 걸린다:

| 양 | 값 | 근거 |
|---|---|---|
| `R_ct`(Cell, 방전) | **670 Ω** | `[인쇄]` Table 1 |
| 비선형 구간 지속 | **≈0.8–1.2 h** (합류 ≈3–5 τ 로 보면 τ ≳ 300 s) | `[도표]` Fig. 4a |
| ⇒ `C = τ / R_ct` | **≈1.5 F = ≈1 F cm⁻²** (A = 1.539 cm²) | `[재현]` |
| 이중층 상한 | **≈10⁻² F cm⁻²** | 19호 절 기준 |
| **초과 배수** | **10² – 10³ 배** | `[재현]` |

⇒ **`R_ct` 라 이름 붙은 성분은 전하이동이 아니다.** 19호가 `P2` 에서 찾은
**200–480 배** 초과보다 **한 자릿수 더 크다** — 그리고 이번에는 그 위에
**기구 서사**가 얹혀 있다(`[인쇄]` *"the de-alloying reaction is known to be
faster than the alloying reaction"*). **서사는 이름표를 잃는다.**

### ⇒ 처방에 **4단계**를 더한다

> **4단계**: *"**시간 영역 분해에도 같은 검사를 건다.** 성분의 시상수 τ 와
> 저항 R 로 `C = τ/R` 을 만들어 물리 상한 안인지 본다. 주파수 영역 분해가
> 없다고 해서 이 검사를 면제받지 않는다."*

계보: "두 값을 같이"(16호) → "+ 면적을 아는 대조군"(18호) →
"+ `C` 가 물리 상한 안인지 + `Ea` 를 면적-불변 채널로"(19호) →
**"+ 시간 영역에도 같은 상한 검사"(20호)**.

### ★★★ 그리고 이 편에 곱 축퇴가 있다 — **음극에서, 방정식 없이**

20호는 식을 한 줄도 쓰지 않는데도 곱에 걸린다. **진단 → 처방 사이**가 그 자리다:

| | 20호가 말한 것 | 어느 인자 |
|---|---|---|
| 진단 | `[인쇄]` *"the relatively **sluggish kinetics** of the alloying process"* (근거: 음극 `R_ct` 135→340, `R_p` 60→170) | **`j₀`** |
| 처방 | `[인쇄]` *"refine the particle size and optimize the morphology **for larger interface areas**"* | **`A`** |

`[재현]` 그리고 두 인자가 실제로 갈리지 않는다: 음극은 **8.4배 과잉**
(Li₄.₄Si 2011 mAh g⁻¹ × 0.06 g = 120.7 mAh vs 양극 14.34 mAh)이고 사이클된
DOD 는 **11.2 %** 인데, 그 11 % 에서 음극 전위가 **0.29 V** 움직여 충전을 끊는다.
설명은 둘 중 하나다 — **(a) 극심한 분극** 또는 **(b) 접근 가능한 음극 분율
≈1/9 이하**. **`R₀`·`R_ct`·`R_p` 세 수로는 가를 수 없다.**
⇒ **이 페이지의 곱이 양극(`A_eff·ε_p/R_s`)뿐 아니라 음극에도 같은 모양으로
있다**는 첫 표본이고, **모델 없이 문장만으로도 걸린다**는 것을 보인다.

### ⚠ 부수 — 뺄셈으로 만든 "접촉 저항" 의 이름표

`[인쇄]` σ = 1.8×10⁻⁴ S cm⁻¹ ⇒ SE **448 Ω**, 측정 `R₀`(Cell) **810 Ω**, 차
**362 Ω** 을 *"layer-to-layer contact resistance"* 로 배정한다.
`[재현]` 448 Ω 은 **정확히 재현된다**(L = 1240 µm, A = 1.539 cm²). 그러나 뺀 것은
**분리막 SE 슬래브뿐**이고, 남은 값에 `[도표]` **388 µm 양극 · 438 µm 음극
복합체 내부의 이온 경로**가 통째로 들어 있다 — ε_SE = 0.4 · 굴곡도 2 · 평균 경로
가정에서 **양극 복합체만 ≈350 Ω** 이다.
⇒ **뺄셈 잔차에 물리 이름을 붙이려면 뺀 항의 완전성을 먼저 보여야 한다.**
이 페이지의 곱 축퇴와 **같은 병**의 옴 판이다.

## ★★★★ 처방의 다섯 번째 적용 (2026-09-23, `assb` 21호) — **`C` 없이 τ 로: 한 쌍 통과 · 한 쌍 기각, 그리고 "전하이동" 이 세 번째로 상한을 넘는다**

`raw/papers/sedlmeier2023_micro-reference-electrode-assb-pouch-inli-anode.md`
(Sedlmeier 외 2023, *J. Electrochem. Soc.* 170, 030536, CC BY). 리튬화 금선 미세 기준극으로 **Li|Li** 와
**InLi|InLi** 대칭형 파우치의 두 전극 임피던스를 따로 잰다. **양극이 없다** — 곱의 자리는 **음극 계면**이다.

### 입력 점검

| 처방 단계 | 필요한 입력 | 21호 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | `capacitan*`·`equivalent circuit`·`fit*` **0 회** — `C` 는 없다. **그러나 꼭짓점 주파수가 인쇄되고(712 Hz · 0.5 Hz · 720 Hz · 1 Hz) 그림에 같은 주파수 마커가 있다** | ✅ **τ 형으로 적용** |
| **2단계** (18호) | + 면적을 아는 대조군 | 4.0 cm² 공칭, 정렬 어긋남은 `[인쇄]` "cannot be excluded" | ❌ |
| **3단계-a** (19호) | `Ea` | 25 °C 한 점 | ❌ |
| **3단계-b** (19호) | `C` 가 물리 상한 안인가 | `C = 1/(2π f_apex R)` | ✅ **반원마다 판정이 갈린다** |
| **4단계** (20호) | 시간 영역에도 같은 검사 | 6단계 소전하의 "이중층 충전" 설명 | ✅ **실패** |

### ★★★ 1단계를 τ 로 — `C` 가 없어도 된다

면적만 바뀌면 `R ∝ 1/A`, `C ∝ A` 라 **τ = RC 가 보존**되고, 동역학만 바뀌면 `C` 는 두고 `R` 만 움직여
**τ 가 바뀐다.** ⇒ **같은 주파수 마커가 두 스펙트럼의 같은 자리(꼭짓점)에 있는가** 만 보면 된다.

| 쌍 | `R` | τ | ⇒ `C` 비 | 면적 가설 | 판정 |
|---|---|---|---|---|---|
| **Li\|Li 계면 반원 WE ↔ CE** | `[도표]` ≈5.5 ↔ ≈2.5 kΩ cm² | `[인쇄]` 공통 **712 Hz** | 1/2.2 | 1/2.2 | ✅ **면적 서명** |
| **InLi-(Li) CE ↔ InLi-(In) WE 저주파 호**(8단계) | `[인쇄]` ≈320 ↔ ≈90 Ω cm² | CE `[인쇄]` **1 Hz** · WE `[도표]` **1 Hz 에서 이미 Im ≈ 0** ⇒ 꼭짓점 **≳5 Hz**(이상 RC) | `[재현]` **≳1.4** | **0.28** | ❌ **정렬 어긋남 기각(≥5배)** |

- 쌍 ①: 저자의 두 설명 — 스트리핑 **거칠어짐** · **정렬 어긋남** — 은 **둘 다 면적**이라 처방과 맞는다.
  ⚠ **처방은 면적 ↔ 동역학을 가르지, 면적의 두 원인은 못 가른다.** `[재현]` 스트리핑 3 µAh 는 4 cm² 에
  균일 **3.6 nm** — 거칠어짐으로 2.2배는 크기가 모자라 보인다(`[추론]`).
- 쌍 ②: 저자는 경쟁 설명 셋(① 정렬 어긋남 ② SEI ③ 계면 Li 고갈)을 **인쇄하고 가르지 않는다.**
  τ 가 **면적 가설을 지운다** — **18호 검사 B 에 이어, 논문 안에 가를 입력이 있었던 두 번째 사례**다.
  ⚠ CPE 형 분포 호면 꼭짓점 하한 ≈5 Hz 가 흔들린다.

### ★★★ 3단계-b — "전하이동" 이 세 번째로 상한을 넘는다

| 반원 | `[인쇄]` 배정 | `[재현]` `C` | 10 µF cm⁻² 대비 | 판정 |
|---|---|---:|---|---|
| Li\|Li 712 Hz | SEI + 물리 접촉 | 0.04 / 0.09 µF cm⁻² | 10⁻² | 막·수축형과 **양립** |
| InLi-(Li) 720 Hz | 물리 접촉 + SEI | ≈1 µF cm⁻²(R ≈235 추정) | 10⁻¹ | **양립** |
| **InLi-(Li) 1 Hz** | **전하이동** | **≈0.50 mF cm⁻²** | **≈50배** | ❌ |
| **Li\|Li 0.5 Hz** | **전하이동** | **≳0.64 mF cm⁻²** | **≳64배** | ❌ |

⇒ 계보: **19호 `P2`(200–480배) → 20호 `R_ct`(시간 영역) → 21호 저주파 호(50–64배)**. 금속 박이라 실면적 ≈
기하면적 — 거칠기로 50배를 채울 수 없다. `[추론]` **2상 평탄(In/In₁Li₁)의 dQ/dE 가 커서 화학용량이
크다** ⇒ 이 호는 **Li 저장과 결합된 과정**이고, 저자의 ③(계면 Li 고갈)과 같은 쪽이다.

⚠⚠ **기준값 정리(이 페이지의 부채)**: 19호 절은 이중층 **비용량 10 µF cm⁻²** 로 200–480배를 냈고, 20호 절의 표는
**"이중층 상한 ≈10⁻² F cm⁻²"** 로 적고 1 F cm⁻² 를 **10²–10³배**라 했다 — **두 값은 10³ 배 다르다**(10 µF 기준이면
20호는 10⁵배). **결론(20호 `R_ct` 는 전하이동이 아니다)은 어느 기준으로도 안 바뀐다.** 그러나 **21호의 0.5 mF cm⁻²
는 관대한 상한(10⁻² F cm⁻²)으로는 통과한다** ⇒ **판정이 기준에 걸린다.** 이 절은 **비용량 10 µF cm⁻² × 거칠기
(금속 박 ≲ 수 배)** 를 기준으로 쓴다.

### 4단계 — "이중층 충전" 설명이 실패한다

`[인쇄]` 6단계에서 InLi-(In) 0.39 µAh cm⁻²(ΔV 1.38 V) · 순수 In 0.32 µAh cm⁻²(ΔV ≈0.1 V) 의 출처 후보로
"simple capacitive currents (i.e., double-layer charging)". `[재현]` `C = Q/ΔV` = **≈1.0 mF cm⁻²** · **≈11.5–23 mF cm⁻²**
(분리막 IR 49 mV 를 빼면 뒤쪽) = **10²–10³배** ⇒ **실패.** 남는 것은 저자의 다른 둘(Li 불순물 · 고용체 Li).

### 부수 — AC = DC 일치는 값이지 배정이 아니다

`[인쇄]` 과전압 75 mV ↔ 375 Ω cm² vs 임피던스 365 · 150 mV ↔ 750 vs 800 ⇒ `[재현]` **3 % / 6 %** — 계보 최초의
시간↔주파수 영역 **값** 일치(19호는 CV 114 ↔ Nyquist 183 Ω 로 어긋났다). 저자는 이것으로 *"reliable values"* 를
말하지만 **경쟁 설명 셋은 그대로 남긴다** — Q4 열네 번째 성질. ⚠ `[재현]` 두 값 모두 **분리막 절반 ≈245 Ω cm²**
(33–65 %)를 품는다.

### 음극 판 곱 축퇴(20호)와의 연결

20호는 진단(동역학) ↔ 처방(면적)이 어긋났다. 21호는 **높은 절대 저항**을 `[인쇄]` *"the low fabrication (∼70 MPa)
and the low applied stack pressure (∼20 MPa)"* — **접촉 면적 쪽** — 으로 돌리고, **CE ↔ WE 의 차이**는 SEI · 고갈
(**화학·농도 쪽**)으로 돌린다. **τ 처방은 뒤쪽(차이)에서 면적을 기각했고, 앞쪽(절대 크기)은 대조군이 없어 시험되지
않는다.** ⇒ 같은 논문 안에서 **"면적" 과 "동역학" 이 다른 비교에 각각 배정**된다 — 처방이 걸 수 있는 곳은 **비교가
있는 곳뿐**이다.

## ★★★★ 처방의 여섯 번째 적용 (2026-09-23, `assb` 22호) — **주파수 영역 없음 · 대신 구조 채널이 곱의 한 인자를 뗀다**

`raw/papers/strauss2018_cathode-particle-size-inactive-fraction-assb.md` (Strauss 외 2018, *ACS Energy Lett.* 3, 992−996).
입자 크기(d₅₀ 4.0 / 8.3 / 15.6 µm)를 바꾸면 **면적(∝1/d)·접촉 분율·확산 길이가 같이** 움직인다 — 곱 축퇴의 교과서 설계다.

### 입력 점검

| 처방 단계 | 필요한 입력 | 22호 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` | `impedan*`·`capacitan*` **본문·SI 0 회** | ❌ |
| **2단계** (18호) | + 면적을 아는 대조군 | LIB 대조(같은 CAM, 크기 효과 없음) + **M ↔ L 같은 로트 체 분리 쌍**. ⚠ BET·밀링 후 입도 0; 액체는 2차 입자 기공을 적셔 SE 접촉 면적의 대조가 아니다 | ⚠ 부분 |
| **3단계-a** (19호) | `Ea` | 25 °C 한 점 | ❌ |
| **3단계-b** (19호) | `C` 물리 상한 | `C` 없음 | ❌ |
| **4단계** (20호) | 시간 영역 상한 검사 | 전자 차단 DC 분극(Fig. S6b): `[도표]` τ ≈5–10 h · `[재현]` R ≈60 kΩ ⇒ **C ≈0.4–0.8 F cm⁻²** | ✅ **계면 아님** — 혼합전도체의 화학량 분극; `[도표]` 60 h 에도 전류 감소 ⇒ **σ_ion 은 상한** |

### ★★★ 처방 표에 없던 채널 — "SOC 추종 상 분율"

ex situ XRD 2상 Rietveld 가 **`ε_p` 쪽(쓰이는 부피)을 구조로 직접** 잰다(`[인쇄]` 불활성 2 / 27 / 31 %).
곱 `A_eff · ε_p / R_s` 에서 `ε_p·θ` 가 떨어져 나가고, `R_s` 는 d₅₀ 로 알려져 있으므로 **남는 것은 `A_eff · j₀`** 다.
그 나머지는 갈리지 않는다: `[도표]` 분극(dQ/dU 봉우리, LIB 대비) **+80 / +130 / +190 mV** ↔ `[재현]` 활성 CAM
면적당 전류 비(∝ d/θ) **1 / 2.2 / 5.5** — 선형 동역학이면 면적 설명이 과잉, Tafel 영역이면 부족하지 않다.
저자는 `[인쇄]` "deterioration of kinetics" + "insulating layer increases the kinetic barrier" 로 **`j₀` 쪽 끝**을 고른다
(16·20호와 같은 한쪽 끝 선택, 식 없이).

⇒ **처방 표에 한 줄을 더한다**: *"SOC 추종 상 분율(ex situ/operando 회절) — `θ·ε_p` 를 뗀다. 열화 판에서는 **두 SOC 에서**
찍어 **SOC 를 따라가지 않는 상**의 분율을 쓴다(고립 당시 SOC 에 얼어붙은 상은 pristine 이 아닐 수 있다). 반사 기하의
정보 깊이(수–수십 µm)와 측정 면(집전체/분리막)을 함께 적는다."*

### 원인 배정도 곱 위에 있다

`[인쇄]` 불활성의 원인 = "lack of **electronic** contact", 근거 = 별도 펠릿의 벌크 부분 전도도(Fig. 4). `[도표]`
σ_e/σ_ion ≈550 / ≈50 / ≈1.5 인데 불활성은 M ≈ L; L 에서 σ_e ≈ σ_ion. ⇒ **전자 ↔ 이온 고립도 이 자료로 갈리지 않는다** —
그리고 Fig. 4 의 두 y 축 자릿수 간격이 달라(5 ↔ 3) **그림 인상이 값과 반대**다.

## ★★★★ 처방의 일곱 번째 적용 (2026-09-23, `assb` 23호) — **1단계가 상태축 위 연속 곡선으로 완전 적용된다 · 결과는 화학 형**

`raw/papers/koerver2017_capacity-fade-interphase-chemomechanical-ncm811-lps.md` (Koerver 외 2017, *Chem. Mater.* 29, 5574−5582 — "접촉 손실의
실험 원전"). 원전은 **계면층(CEI)** 과 **탈리튬 수축 접촉 손실**을 둘 다 주장하고 **가르지 않는다** — 그런데 SI 가 양극 호의 `R` 과 `C` 를
**두 셀(In · LTO 상대극) × 네 구간(1·2 차 충·방전)** 으로 인쇄한다. 이 곱의 두 인자(`A_eff` ↔ `j₀`)가 바로 두 기구다
([[assb-interphase-vs-contact-loss-attribution]]).

### 입력 점검

| 처방 단계 | 필요한 입력 | 23호 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | Fig. 4 + **S2**(In) · S6 + **S7**(LTO) — OCV 위 연속 | ✅ **계보 첫 연속 곡선** |
| **2단계** (18호) | + 면적을 아는 대조군 | 면적 대조 없음. **S3 무전류 기계 이완**(S4 XPS 로 화학 불변) | ⚠ **전제 양성 대조 — 한 호 통과, 한 호 실패** |
| **3단계-a** (19호) | `Ea` | 25 °C 한 점 | ❌ |
| **3단계-b** (19호) | `C` 물리 상한 | 양극 호 기하 2.3–3.3 µF cm⁻² · `[추론]` 실면적(입자 ∅6–9 µm `[도표]`) ≈0.10–0.15 µF cm⁻² | ✅ **양극 호 통과(DL 의 ≈1–2 %)** — 19·20·21호 연속 실패와 다르다 |
| 〃 | 〃 | 음극 호 0.5–6.4 mF cm⁻² | ❌ **DL 의 50–640 배** — "R_SE/Anode" 는 합금 화학 용량 (`[추론]`) |
| **4단계** (20호) | 시간 영역 | DC 과전압 ~100 mV ↔ EIS 25 mV | ⚠ 4 배 불일치, 그리고 **충전만 이동**(S1a) ⇒ DC 쪽은 옴이 아니라 **창 이동** (`[추론]`) |

### ★★★★ 1단계 결과 — 여섯 비교 중 다섯이 동역학 끝

| 셀 · 구간 | `R` 비 | 면적 예측 `C` 비 | 관측 `C` 비 `[도표]` |
|---|---|---|---|
| In · 첫 충전 3.25 → 3.53 V | ×2.45 | ×0.41 | **×1.05** |
| In · 둘째 충전 | ×1.5 | ×0.66 | **×1.0** |
| LTO · 첫 충전 | ×1.7 | ×0.59 | **×1.0** |
| LTO · 첫 방전 | ×1.8 | ×0.54 | **×0.96** |
| In · 첫 충전 전체 3.00 → 3.53 V | ×3.0 | ×0.33 | ×1.7 (면적과 반대 방향) |
| In · 첫 방전 끝 | ×1.65 | ×0.61 | ×3.0 — ⚠ **호 혼합**(같은 구간 `C_anode` ≈20 µF 로 붕괴, 두 호 주파수 비 ≈6 배) |

⇒ **EIS 창 안의 양극 저항 증가는 `j₀`(화학) 형**이다. 원전 **본문**의 CEI 배정은 원전 SI 로 지지되고, **초록**의 "contact loss … further
increasing the interfacial resistance" 는 지지되지 않는다. 16호(한쪽 끝을 골랐다) · 18호(`or` 를 남겼다)와 달리 23호는 **양쪽을 다 주장했고,
SI 가 한쪽만 남긴다.**

### ⚠ 이것이 곱을 푼 것은 아니다

- 푼 것은 **`R` 의 변화분**이다. **용량**의 분할(`θ` ↔ `η` ↔ `Q_material` ↔ 상대극)은 **0** 이다 — `[재현]` 원전 숫자로 계면층의 패러데이 몫 ≈4 %,
  옴 몫 ≲3 % 이고 나머지 ≳85 % 는 미배정([[assb-apparent-capacity-decomposition]] §23호).
- **완전히 고립된 입자는 호에서 빠진다.** 고립 분율 `f` 는 `R/(1−f)`, `C(1−f)` 로 역시 면적 서명을 내야 하므로 `C` 평탄은 **첫 충전 중 새 고립이
  ≲10–20 %** 라는 **약한 상한**이다(`[추론]`, 판독 분해능).
- 전제 `C ∝ 면적` 은 **18·19호에서 깨졌고** 23호 양성 대조는 **한 호**뿐이다. 그리고 CPE → C 환산식이 인쇄되지 않았다.

## ★★★★ 처방의 여덟 번째 적용 (2026-09-23, `assb` 24호) — **수송 곱 `σ_bulk·ε/τ²` 에서 4단계가 적용되고, 상태축 R·C 는 없다**

`raw/papers/stavola2023_lithiation-gradients-tortuosity-thick-nmc111-argyrodite.md` (Stavola 외 2023, *ACS Energy Lett.* 8, 1273−1280). 이 편의 곱은 **두 층**이다 —
전극 척도 **수송** `σ_eff = σ_bulk·ε/τ²`(이 페이지 ③ 채널의 본체, 상세 [[assb-tortuosity-factor-effective-conductivity-split]]) · 입자 척도 **동역학** `A_eff·j₀`(봉우리 이봉 해석).

### 입력 점검

| 처방 단계 | 필요한 입력 | 24호 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | TLM `R1`·`Q1,a1`(+`Q2` / `Qp`) — **조성축**(40–95 %), 신품 차단 셀만. CPE 지수 `[인쇄]` 0.02–0.89 · Q 단위 "ohm cm" | ❌ **상태축 0** — 23호의 "같은 상태축 위 R·C" 를 적용할 궤적이 없다 |
| **2단계** (18호) | + 면적을 아는 대조군 | 면적 대조 없음 · ★ **코팅 쌍 = 화학 대조**(계보 첫 통제 쌍) · 두께 쌍 50 ↔ 110 µm(한 셀, 정량 0) | ⚠ 여집합만 |
| **3단계-a** (19호) | `Ea` | 실온 한 점 | ❌ |
| **3단계-b** (19호) | `C` 물리 상한 | C 환산 불가 | ❌ |
| **4단계** (20호) | 시간 영역 | ★ **같은 `σ_eff` 를 두 영역에서** — EIS(주파수, 신품 펠릿) ↔ operando 리튬화 구배 역적합(시간, DC) | ✅ `[재현]` LPSC **70 % 0.93(통과) · 80 % 0.34(실패)**; 옴 강하 차수로도 80 % 만 ≈3–5 배 부족 |

### ★★★ 4단계 실패분의 배정 — 곱의 모든 인자 + 처방 표 밖의 하나

80 % 셀의 ≈3 배는 `ε`(가정 14 % ↔ `[재현]` 두께 함의 21–38 %) · `τ²`(저자 선택 — "evolved") · 접촉(`[인쇄]` 정의상 `τ²` 안의 "point contacts") · **제조 압력(50/150 ↔ 100 MPa)**
어느 쪽에도 들어간다. 원전은 **`τ²` 끝**을 고르고 기구로는 **접촉**("NMC shrinks … rearrangement of particle contacts")을 댄다 — **16·20·22호의 "한쪽 끝 선택" 이 수송 곱에서 반복된다.**
⇒ 처방 표에 **"두 영역 대조의 시편 조건"** 줄을 더했다.

### ★★ 23호 원칙("R·C 를 같은 상태축에서")의 자리 — 다른 채널로 나타난 같은 문제

상태축 EIS 가 없어 R·C 분류는 못 한다. 그러나 **봉우리 이봉**(입자 모집단 이질성)의 원인이 `j₀`(계면층, `[인쇄]` 저자 배정) ↔ `A_eff`(접촉) ↔ 자촉매 동역학(원전 ref 51)으로
같은 곱 위에 있고, **코팅 쌍이 첫째를 떼는 대조군**이다: `[인쇄]` 코팅에서 이봉이 약하다 ⇒ **이봉의 코팅 의존분은 화학 형** — 23호 SI 판정("양극 저항 증가는 화학 형")과 같은 방향.
⚠ n = 1 씩, 코팅 행 내부 불일치(24호 D17).

### ⚠ 이것이 곱을 푼 것은 아니다

- 수송 곱의 **분할**(`ε` ↔ `τ²` ↔ 접촉)은 0 이다 — 원전 Table S8 이 **같은 `σ_eff` 에서 `ε` 규약만으로 반대 추세**를 낸다(24호 D1).
- 동역학 곱(`A_eff·j₀`)은 이봉 해석에서 **코팅 의존분만** 화학으로 가고, 나머지는 안 갈린다.
- 용량의 분할(`θ` ↔ `η` ↔ `Q_material` ↔ 상대극)도 0 — 첫 사이클 비가역 ≈0.2 Δx 는 깊이 균일이라 `η(z)` 는 아니라는 것까지다.

## ★★★★ 처방의 아홉 번째 적용 (2026-09-23, `assb` 25호) — **신품 쌍의 2단계가 처음 통과하고, 열화 쪽 1단계는 그림 자료 때문에 막힌다**

`raw/papers/zhou2025_tailored-cathode-microstructure-low-pressure-assb.md` (Zhou 외 2025, *ACS Energy Lett.* 10, 966−974). NCM811–Li₆PS₅Cl–VGCF 복합양극에서 **SE 입도만** 바꾼 쌍(coarse ↔ fine)을
운전 압력 30 · 10 · 2 MPa 에서 100 사이클 — 2전극, Li 금속.

### 입력 점검

| 처방 단계 | 필요한 입력 | 25호 | 판정 |
|---|---|---|---|
| **1단계** (16호 · 23호) | 같은 상태축 위 `R`·`C` | `R` 은 1·100 사이클 × 3 압력 × 2 조성(S19 막대) · **`C`(CPE) 미인쇄** · τ 대리(DRT 회색 창)는 **12 곡선 중 5 개가 2 개의 곡선**(`[재현]` ≤0.21 Ω) | ❌ 깨끗한 1↔100 짝은 10 MPa 하나이고, 그 짝의 조성 배정이 범례 모순에 걸려 `C` ×**0.77**(면적 형) ↔ ×**1.20**(화학 형)으로 **판정이 뒤집힌다** |
| **2단계** (18호) | + 면적을 아는 대조군 | ★ **SE 입도 쌍 + BET**(6.02 → 9.24 m² g⁻¹) | ✅(부분) — 아래 |
| **3단계-a** (19호) | `Ea` | 온도 한 점 | ❌ |
| **3단계-b** (19호) | `C` 물리 상한 | 신품 P4 `C` = τ/`R` | ✅ CAM 면적당 ≈2–27 µF cm⁻² (입도 1–5 µm 가정) |
| **4단계** (20호) | 시간 영역 | GITT(100 뒤) — 펄스·휴지 미기재 | ❌ |

### ★★★ 2단계 — 신품 쌍에서 면적 서명이 통과한다

`[인쇄]` `R_ct` 17.3 → 9.9 Ω(×0.572), `[도표]` Fig. 1f P4 τ ≈2.9 → ≈4.1 ms(×1.41) ⇒ `[재현]` `C` ×**2.47**(DRT 높이 비 0.84 를 `R` 비로 쓰면 ×**1.68**).
면적만 바뀌었다면 `C` 비 = 1/`R` 비 = **1.75**, 독립 측정 BET 비 = **1.53**. ⇒ **방향과 자릿수가 맞는다.** 18호 검사 A(**CAM** 입도 쌍)에서는 `C` 가 면적 설명을 따르지 않았다 —
`[추론]` **어느 상의 입도를 바꾸느냐**가 전제 `C ∝ 면적` 의 성립을 가른다(CAM 을 바꾸면 2차 입자 내부 호가 같이 바뀐다 — 18호 R4).
⚠ ECM 과 DRT 가 `R` 비를 다르게 준다(0.57 ↔ 0.84) · BET 는 SE 분말 면적 · SE 벌크 σ(×0.66)·밀도가 같이 변했다.

### ★★★ 저자가 `C ∝ 면적` 을 스스로 인쇄했다 — 그러나 다른 봉우리에

`[인쇄]` P1(입계) "the increase in time constant indicates a rise in the capacitance … **capacitance is positively correlated with the electrochemical surface area** … attributed to the increased
interfacial area". **계보 첫 저자 자신의 `C ∝ 면적` 추론**이다. ⚠ `[추론]` 직렬 입계(벽돌층 모형)의 용량은 **결정립 크기에 비례**(`C_gb ∝ D/δ`)해 입자가 작아지면 **줄어야** 한다 —
P1 에서는 방향이 반대다. 같은 추론을 **P4(양극 전하이동)** 에 걸면 위처럼 양립한다 ⇒ **맞는 추론을 틀린 봉우리에 걸었다.**

### ⚠ 열화 쪽 — 원전이 스스로 "못 가른다" 고 적는다

`[인쇄]` "`R_SSE/NCM` contains both the charge transfer resistance … and the CEI resistance … **indistinguishable because there is only one semicircle**". 우리도 가를 입력(`C(N)`)이 없다.
그리고 그 위에 **17호 함정**이 얹힌다 — `[도표]` S19 에서 `ΔR_anode` 가 `ΔR_NCM` 의 ≈4 배(2 MPa coarse 2020 ↔ 535 Ω), `[재현]` 방전 전압 하강 ≈0.30–0.37 V 의 ≈80 % 가 Li 계면.
⇒ **양극 곱을 풀기 전에 상대극 몫을 빼야 한다** — 2전극에서는 뺄 수 없다.

### 처방 표에 한 줄

**"SE 입도 쌍 + 분말 BET"**(위 표). 조건: SE 벌크 전도도·밀도가 같이 변하면 고주파 호가 교락된다 — 25호는 둘 다 변했다.

## ★★★ 처방의 열 번째 적용 (2026-09-23, `assb` 26호) — **모델 편 · 빌린 데이터: 1–4단계 전부 막히고, 곱은 다른 모양으로 나타난다**

`raw/papers/iwakiri2024_new-ssb-model-parameter-estimation-sensitivity.md` (Iwakiri 외 2024, *Electrochim. Acta* 508, 145202). 박막 Li/LiPON/LCO 1차원 모델을
**남의 4 율 방전곡선**(Raijmakers 2020)에 Nelder–Mead 로 맞춘 편. 실험 데이터가 있으므로(빌린 것) 처방을 적용한다.

### 입력 점검

| 처방 단계 | 필요한 입력 | 26호 | 판정 |
|---|---|---|---|
| **1단계** (16호 · 23호) | 같은 상태축 위 `R`·`C` | EIS 0 · **모델이 이중층을 가정으로 배제**(`[인쇄]` 가정 2) | ❌ 모델 수준 봉쇄 |
| **2단계** (18호) | + 면적 대조군 | 셀 1 개 | ❌ |
| **3단계-a** (19호) | `Ea` | 293 K | ❌ |
| **3단계-b** (19호) | `C` 물리 상한 | `C` 없음 | ❌ |
| **4단계** (20호) | 시간 영역 | CC 방전만 | ❌ |
| 표 "율 스윕" | 여러 율 | **0.2 · 2 · 4 · 6 C** | ⚠ 데이터는 있고 손실 하나에 합쳤다 |
| 표 "`J^T J`" | 적합점 야코비안 | 스윕 곡선(열)은 인쇄 — 대역 · 1C | ⚠ 곱은 안 만들었다 → 위 표 새 줄 |

### ★★★ 이 모델에서 곱이 서는 자리 — `A_eff·ε_p/R_s` 가 아니라

박막이라 `ε_p`·`R_s`·`a_s` 가 **없다**(확산 길이 = 측정된 막 두께). 그래도 같은 두 자리에 조합이 선다(`[재현]`/`[추론]`, 상세 digest §5-2):
- **동역학 면적**: 식 (3)–(6) 의 전류는 기하 `A`(고정)로 나눈 밀도 ⇒ **실제 계면 면적 비는 `k¹_s` 에 흡수** — `A_eff·j₀` 의 박막판. `[도표]` Fig. 12a≡b 로 `k₁`·`k₂` 는 몸통에서 합만 보인다.
- **용량 스케일 ↔ 수송**: `x` 좌표에서 양극 부분계가 `D_M⊕·a_max/I` 한 조합만 본다 — `[도표]` Fig. 3(확산 ×K) ≡ Fig. 15(`a_max` ×K, 전류 고정). 9호의 ① 채널(용량이 `ε_p` 를 단독으로 고정)이
  **정규화 용량 축에서는 사라진다** — 절대 용량 축과 `I⁺₀ ∝ a_max` 만 남는다.

### ⚠ 이것이 곱을 푼 것은 아니다

26호는 열화 · 접촉을 다루지 않는다. 기여는 **처방 표의 새 줄 하나**와 **"모델 편에서도 같은 두 자리에 조합이 선다"** 는 두 번째 모델 표본(9호 P2D 다음)이다.

## ★★★ 27호 — **처방 적용 대상 아님(모델 편, 데이터 0)** · 그러나 곱의 모델 쪽 세 번째 표본: **`A_el-c` 한 손잡이가 면적 · 용량 · 연결 분율을 함께 진다** (2026-09-23, `assb` 27호)

`raw/papers/sinzig2024_p2d-validity-ssb-global-sensitivity.md` (Sinzig, Schmidt, Wall 2024, *JES* 171, 120519). 3차원 입자 분해 모델 ↔ 균질화 P2D, NMC622/LPS/Li. **실험 · 빌린 데이터 모두 0** ⇒ 1–4단계를 걸 입력이 없다.

**이 편이 주는 것** (`[인쇄]` + `[재현]`):
- P2D 반응원 `A_el-c N̄_q`(식 10–11) + BV `i₀` 상수 ⇒ **`A·i₀` 는 정확한 곱**(9호 `A_eff·j₀` 의 같은 자리).
- 그런데 `A` 가 **세 겹 짐**을 진다: 면적 `6ε_c/d̄` = 0.329 → **용량을 맞추려** 0.344(`[인쇄]` "such that the capacity … is exactly the same") → **연결 분율 `u` = 0.93 을 넣으려** 0.320(`[재현]` 0.320/0.344 = 0.930).
  `[인쇄]` "The utilization could be included within the P2D model by artificially reducing the available capacity of the cathode by a modification of the specific interface area".
- ⇒ **P2D 에서 접촉(연결) 손실이 들어갈 곳은 용량(= `LAM_PE` 의 자리)과 면적을 함께 깎는 손잡이 하나뿐**이다 — 이 페이지의 곱이 모델 설계 수준에서 **처방으로 인쇄**된 첫 편.
- `[재현]` 로그정규 구의 실제 비표면적 `6ε_c/d₃₂` = 0.216 ⇒ P2D 의 `A` 는 그 ≈1.5 배(개수 평균 `d̄` 를 썼기 때문). 면적 과대가 곱 안에 숨어 있다.

### ⚠ 이것이 곱을 푼 것은 아니다

데이터가 없고 `i₀` 를 흔들지 않았다. 기여는 **"축약 모델에는 `θ` 의 독립된 자리가 없다"** 는 구조 사실과, 그것을 `[재현]` 한 크기(비연결 7 % → `SOC_end` 바닥 0.07 ↔ 큰 `κ` 오프셋 0.068)다.
**ASSB 판 합성 truth 를 P2D 로 만들면 접촉 손실과 `LAM_PE` 가 truth 단계에서 같은 파라미터가 된다** — 시험이 동어반복이 된다(`[추론]`, 27호 digest §7).

## ★★★ 처방의 열한 번째 적용 (2026-09-23, `assb` 28호) — **액체셀 식별성 원전: 1–4단계가 파이프라인 입구에서 막히고, 대신 곱의 구조적 원형이 식으로 있다**

`raw/papers/bizeray2019_spm-identifiability-parameter-estimation.md` (Bizeray, Kim, Duncan, Howey 2019, *IEEE TCST* 27(5) 1862 — **액체셀 SPM**, ASSB 아님). 묶음 표는 [[spm-grouped-parameter-identifiability]].

### 입력 점검 — 데이터는 있다, 채널은 버렸다

실험 EIS(Kokam NMC 740 mAh, 9 DoD, 5 kHz–200 µHz) · 기준극 전극 OCV · 시간 영역 한 구간이 있다. 그러나:
- **1단계** ❌ — `[인쇄]` 고주파 반원(`R_ct ∥ C_dl`)은 "ignored", 이중층은 "beyond the scope". **`C` 가 설계로 없다.** `R0(DoD)` 9 점(`[도표]` ≈62 → ≈123 mΩ, 신품)은 있으나 `R_ct` · 옴 · **접촉** · 피막의 합이다.
- **2단계** ❌ 셀 하나 · 면적 변화 없음 · **3단계** ❌ 20 °C 한 온도(`Ea` 없음) · **4단계** ❌ 시간 영역 성분 분해 없음.

### ★★★ 곱의 원형 — `a = 3ε/R` 과 `k` 는 한 묶음 안에서만 만난다

`[인쇄]` 식 (4) `j = I/(aδFA)`, `a = 3ε/R` · 식 (18) `τ_k = R/(2k√c_e)` · 식 (26) `θ₃ = τ_k⁺/(3Q_th⁺)`. `[해석]` 표면 일부 접촉 손실을 `a_eff = A_eff·a` 로 넣으면 `θ₃ ∝ 1/(k·A_eff·ε δ c_max A)` —
**`k·A_eff` 가 이 페이지의 곱(`A_eff·ε_p/R_s` 의 동역학 쪽)과 같은 모양**이다. 그리고 `θ₃` 는 선형화에서 `θ₆`(음극)와 `R_ct` 하나로 합쳐지고(`[인쇄]` "infinite number of pairs"), `R_ct` 는 다시 `R0` 로 합쳐진다.
**입자 통째 비연결은 `ε` 에만 곱해져 `Q_th` 로 가고, 그것은 LAM 과 같은 묶음이다**(`[해석]`).

### ⇒ 이 적용이 처방에 더하는 것

`[해석]` **식별성 원전의 파이프라인을 그대로 ASSB 에 옮기면 1단계가 설계로 막힌다** — 이 처방이 가장 많이 쓴 채널(`R_CT · C_dl`, 16·18·19·21·23·25호)을 원전은 입구에서 버린다.
ASSB 에 식별성 도구를 들여올 때 **반원을 버리지 않는 판**(이중층을 모델에 넣은 SPM/P2D 임피던스)이 필요하다. 원전 참고문헌의 [33] Alavi 2016(Randles 회로 식별성)이 그 방향의 후보다.

## ★★★★ 처방의 열두 번째 적용 (2026-09-23, `assb` 29호) — **율 스윕 줄의 첫 실적용 · GITT 가 곱 자체 · 2단계 부분 통과**

`raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode.md` (Yanev et al. 2024, *JES* 171, 050530 — NCM811 gran/sc × LPSCl/BM × AM 51–90 wt%, 14 복합체, 신품, 2전극 Li-In).

### 입력 점검

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | 대칭 셀 EIS 를 TLM 으로 적합했으나 **인쇄는 `σ_eff` 뿐**(계면 요소 · `C` 는 SI Fig. S1, 미열람) | ❌ |
| **2단계** (18호·25호) | + 면적을 아는 대조군 | SE 입도 쌍(BET 2.25 ↔ 8.36 m² g⁻¹, ×3.7) · CAM 형상 쌍(0.570 ↔ 0.696) · 같은 분말 LIB | ✅ **부분** — `[재현]` BM/비BM `φ` 비 **1.02–2.29** < BET 비 3.7: 방향 통과 · 크기는 상한 안. 25호 "SE 입도 쌍 + BET" 줄의 **두 번째 표본** |
| **3단계-a/b** (19호) | `Ea` · `C` 상한 | 30 °C 한 점 · `C` 없음 | ❌ |
| **4단계** (20호) | 시간 영역에도 같은 검사 | CA `α`(h) ↔ GITT `L²/D`(`L = V/A_BET`) | ✅ **자릿수 양립**(`[재현]` gran51 0.06 ↔ 0.05 h · 나머지 ×1.6–16) — 단 둘이 **같은 곱**을 보므로 검사가 아니라 일관성 |

### ★★★★ 이 편의 GITT 가 곱 자체다

`[인쇄]` 식 (3) `D = (4/π)(m·V_M/(M·A))²·(ΔE_S/(t·dE/d√t))²` — `A` 가 **제곱**. 진짜 활성 면적이 `φ·A_BET` 이면 `D_app = D·φ²`. `[인쇄]` "The knowledge or assumption of A is necessary when quantifying diffusive phenomena."
⇒ 이 페이지의 곱 `A_eff·ε_p/R_s` 와 **같은 부류의 곱**(면적 × 수송)이 **확산 쪽**에 선다. 저자는 `D_LIB` 수입(위 새 줄)으로 풀고, 남는 차이를 전부 면적(`φ`)으로 배정한다 — 이 편의 결론 "확산성 한계는 작은 접촉 면적에서 온다" 는 **그 배정의 다른 이름**이다(`φ ≡ √(D_app/D_LIB)`).

### ★★★★ 처방 첫 줄의 실적용 — 그리고 그 줄이 언제 실패하는지

이 페이지 처방 표 첫 줄("율 스윕, `i → 0` 포함 — `η(i)` 를 지워 `θ_AM·Q_material` 만 남긴다")을 **계보에서 처음 실제로 한 편**이다: CA 한 번을 `Q(R) = Q_M/(1+2(Rα)ⁿ)` 로 적합해 `Q_M`(= `θ·Q`) 을 외삽한다.
`[재현]` 고율 극한 `(Q_M/2)(Rα)⁻ⁿ` ⇒ 저율 평탄이 창 밖이면 `Q_M·α⁻ⁿ` 한 조합 — `[인쇄]` sc90 dependency ≈1 과 정합. `[도표]` 그런데 **어느 셀도 0.02 C 에서 평탄하지 않고**, `Q_M` 은 평탄이 보이면 과소(gran51 ≈185 ↔ 194) · 안 보이면 과대(sc84 ≈236 ↔ 177)다.
⇒ 첫 줄에 조건을 붙였다(위 표 "↳ 율 스윕 줄의 실패 조건").

### 원인 배정도 곱 위에 있다
균열이 **두 칸에 동시에** 배정된다 — `[인쇄]` "detach from the electronic percolation network and remain unutilized" (→ `Q_M`, 용량) · "particle delamination and contact loss, which is purely detrimental to the AM-SE surface area and diffusive kinetics" (→ `φ`, 동역학). 몫을 가르는 관측은 없다.

## ★★★ 처방의 열세 번째 적용 (2026-09-23, `assb` 30호) — **SE 없는 슬러리 양극: 1–3단계가 막히고, 대조군이 곱을 가르지 않고 한 인자를 바꾼다**

`raw/papers/park2024_asymmetric-kinetics-low-mass-loading-nmc111-latp-li-metal.md` (Park 2024, *Materials* 17, 5014 — Li \| 소결 LATP 펠릿 \| NMC111 슬러리 전극, 2전극, 셀 1 개씩).
⚠ **이 셀에는 복합양극이 없다** — 양극 안 SE 0, 이온 경로는 펠릿 한 면. 곱 `A_eff·ε_p/R_s` 의 `A_eff` 는 **평면 계면 한 장의 점접촉 면적**이 된다.

### 입력 점검

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | 양극 셀 EIS **0**. Li/LATP/Li 대칭셀 Nyquist 한 장(적합 · 회로 · 주파수 표지 0) | ❌ |
| **2단계** (18호·25호) | + 면적을 아는 대조군 | 액체 대조 — **면적이 정의상 다른 대조**, 면적 측정 0 | ❌ — 대조가 곱을 가르지 않고 **곱의 한 인자를 바꾼다** |
| **3단계-a/b** (19호) | `Ea` · `C` 상한 | 온도 0 · `C` 0 | ❌ |
| **4단계** (20호) | 시간 영역에도 같은 검사 | Dunn `k₁/k₂`(면적 소거 조합)가 Table 1 에 있다 | ⚠ **부분** — 저자 `D` 배정은 면적당 표면 용량 ≈4.3 배를 요구(`[재현]`). 판정이 아니라 긴장 |

### ★★★ 같은 곱, 반대 배정 — 29호와 30호

29호 GITT 식 (3) `D_app ∝ 1/A²` 과 30호 Randles–Ševčík `D_app ∝ 1/(A·C)²` 는 **같은 구조**다. 둘 다 액체 반쪽전지를 기준으로 들여온다. 그리고 **정반대로 배정한다**: 29호는 "`D_true` 는 액체와 같다" 를 가정하고 차이를 면적(피복률 `φ`)에 넣고, 30호는 면적이 같다고 암묵 가정하고 차이(10.9 배)를 `D` 에 넣는다. 두 편 모두 고른 쪽을 측정하지 않았다 ⇒ 위 표의 "외부 액체 기준 수입" 줄에 경고 행을 붙였다.

### ★★★ 율 스윕 줄의 두 번째 실패 조건

29호가 준 조건은 "종료 율에서 곡선이 평탄할 것" 이었다. 30호는 그 조건을 **통과**한다(0.1–1 C 가 63 → 58, `[재현]` `Q_M`–`α` 상관 0.24–0.34 — 29호의 dependency ≈1 과 대조). 그런데 그 `Q_M` ≈63 은 0.1 C 첫 블록이 85 → 63 으로 떨어진 **뒤**의 값이고, 0.5 · 1 C 블록 안에서도 사이클당 ≈−0.09 mAh g⁻¹ 표류가 이어진다. ⇒ **율 스윕이 길면 "`i → 0` 극한" 이 시간에 따라 움직이는 양의 한 시점 값이 된다.** 처방 표에 두 번째 조건 행을 붙였다.
`n` ≈2.5 는 29호의 해석 범위 [0.5, 1] 밖이다 — `[해석]` 정전류 + 전압 창에서 옴 강하(`[재현]` 직렬 ≈0.6 kΩ, 1 C 를 150 mA g⁻¹ 로 가정하면 10 C 에서 ≈0.9 V)가 창을 넘는 **절벽형 손실**의 모양이다. CA 용 식의 `n` 을 여기로 옮기지 않는다.

### 원인 배정도 곱 위에 있다
"율 한계" 는 `[인쇄]` 낮은 `D` 에, "비대칭" 은 LATP/NMC111 공간전하층에 배정된다. 둘 다 **상대극 Li\|LATP 계면 + SE 직렬 저항**(`[재현]` 대칭셀 호 기반 ≈0.5–0.86 kΩ ↔ CV 봉우리 이동 ≈0.54–0.65 kΩ)과 양립하고, 이를 가를 관측은 없다.

## ★★★ 처방의 열네 번째 적용 (2026-09-23, `assb` 31호) — **액체셀 방법 원전: 곱을 가르지 않고, 가를 재료 반쪽을 같은 차단에서 이미 뽑는다**

`raw/papers/chien2023_ici-rapid-solid-state-diffusion-coefficient.md` (Chien et al. 2023, *Nat. Commun.* 14, 2289 — NMC811 | Li 링 기준극 | Li, 1 M LiPF₆ 3전극 파우치 ×2, ⚠ **액체셀**).
⚠ **이 셀에는 접촉 손실의 자리가 없다**(액체가 적신다). 곱은 `A_eff·ε_p/R_s` 가 아니라 **확산 쪽 곱 `D·(A/V)²`**(29호 GITT 와 같은 자리)로 선다.

### 입력 점검

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | EIS 등가회로(R0 · R1‖CPE1 · R2‖CPE2 · W0) 적합 — **값 미인쇄**. ICI 는 `R` · `k` | ❌ (`C`) · ★ 대체 후보 `R/k` (위 표 새 줄) |
| **2단계** (18·25호) | + 면적을 아는 대조군 | BET 한 값(공급사), 면적을 바꾼 쌍 0 | ❌ |
| **3단계-a/b** (19호) | `Ea` · `C` 상한 | 온도 미통제 한 점 · `C` 없음 | ❌ |
| **4단계** (20호) | 시간 영역에도 같은 검사 | ICI(시간) ↔ EIS(주파수): `k = σ√(8/π)` · `R_ICI ≈ R0+R1+R2` 가 3.8 V 위에서 일치 | ✅ **양립** — `σ ∝ 1/(A√D)` 도 같은 곱이라 **일관성**이지 검사가 아니다(29호와 같은 성질) |

### ★★★ 같은 곱, 세 번째 배정 — 그리고 첫 고지

`[인쇄]` 식 (19) `D = (4/π)(V/A)²((ΔE_OC/Δt_I)/(Ik))²` · `A` = BET 1.5 m² g⁻¹ · `[인쇄]` "The BET-surface area may differ from the electrochemically active surface area. However, … both of which are equally affected by this factor."
29호(차이 → 면적) · 30호(차이 → `D`) 에 이어 31호는 **상수 입력 → 전부 `D`**. 셋 중 유일하게 저자가 **자기 주장의 어느 부분이 배정에 기대는지를 적었다** — "ICI ≈ GITT" 는 `A` 가 약분되는 비라 배정과 무관하다. ⚠ 그러나 같은 논문의 **사이클 `D` 감소(Fig. 7) · operando "한 자릿수 급락"(Fig. 8) · 결론**은 절대값이고 신품 BET 를 55 사이클 뒤에도 쓴다 — 거기서는 29·30호와 같은 무고지 배정이다.

### ★★★ `[해석]` 확산 곱은 LAM 형 손실에 눈멀었다

식 19 의 관측 비는 `(V/A)/√D` 이다. 입자 통째 비연결(활성 분율 `u`)은 `V`·`A` 를 같이 줄여 **약분**되고, 표면 피복 `φ` 는 `A` 만 줄여 `D_app = φ²D`. ⇒ **이 페이지의 곱이 확산 쪽에 설 때, 그 곱은 `ε_p`(LAM 형)를 보지 않고 `A_eff`(피복형)만 본다** — 용량 축과 `D_app` 축이 두 접촉 손실을 **나눠 받는다**(29호 `Q_M` ↔ `φ`). 곱 안에서 `A_eff` ↔ `D` 는 여전히 한 조합이다.

### 원인 배정도 곱 위에 있다

사이클 `D` 감소 · `R` 증가를 저자는 c 격자 비가역성 · 두 상(fatigued) 분리에 배정한다. `[재현]` operando 극값에서 한 면적 인자는 충전 끝(`R` ×3.3 ↔ `D` ×≈0.17, 예측 ×0.09)에서만 자릿수 양립하고 방전 4.1 h(`R` ×1.7 ↔ `D` ×0.075)에서는 어긋난다. 그리고 그 구간은 `[인쇄]` 상속 가정 "single-phase solid solution" 이 자기 XRD(두 상)로 깨진 곳이다. 가를 `k` 는 인쇄되지 않았다.

## ★★ 처방의 열다섯 번째 적용 (2026-09-23, `assb` 32호) — **적용 불가, 대상 없음 · 대신 BMS 센서 목록이 처방 단계의 입력 채널과 겹친다**

`raw/papers/bicer2025_ssb-chemistry-bms-thermal-assembly-critical-review.md` (Biçer et al. 2025, *Batteries* 11, 212 — ⚠ **Review 49 쪽, 1차 측정 0, 식 0 개**).
곱이 설 모델도, 가를 데이터도 없다. 기록하는 이유는 둘이다: 계보에서 **"대상 없음" 도 한 번의 적용으로 센다**는 원칙, 그리고 이 편이 **SSB BMS 에 요구하는 센서 목록**이 처방의 입력 채널과 겹친다는 관찰.

### 입력 점검

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | EIS 를 `[인쇄]` "tracking dynamic internal resistance changes" 로만 권고 — **`C` 는 낱말로도 없다** | ❌ |
| **2단계** (18·25호) | + 면적을 아는 대조군 | 0 | ❌ |
| **3단계-a/b** (19호) | `Ea` · `C` 상한 | `Arrhenius` 0 · 열화 `Ea` 0 — 온도는 안전 감시(DSC/ARC) 와 BMS 입력뿐 | ❌ |
| **4단계** (20호) | 시간 영역에도 같은 검사 | 0 | ❌ |

### ★★ `[해석]` BMS 센서 ↔ 처방 단계 — 채널은 있고 물음이 없다

| 이 편이 SSB BMS 에 요구하는 것 (`[인쇄]`) | 처방의 자리 | 빠진 것 |
|---|---|---|
| "impedance-based diagnostics (e.g., EIS)" | 1단계 | `R` 만 추적 — **`C` 를 같이 보고**해야 면적 서명이 선다 |
| "thermal sensors" · "localized temperature sensing" | 3단계-a | 운전 온도 분포 위의 `R(T)` 를 모으면 `Ea` — **안전 감시가 아니라 진단으로** 써야 |
| "pressure sensors and feedback control ... maintain optimal stack pressure" | [[assb-pressure-reapplication-separation-test]] 의 `P` 축 | 압력을 **일정하게 유지**하면 그 축은 닫힌다 — 되돌림 시험은 **압력을 바꿔야** 한다 |
| "high-resolution current ... monitoring at the cell and sub-cell levels" | (처방 표 밖) | 면적 분포의 대리량 후보 — 확인 안 됨 |

처방 네 단계 중 두 단계(1 · 3-a)와 압력 축의 **센서는 BMS 요구 목록에 이미 있다.** 빠진 것은 "그 채널로 무엇을 가를지" 의 물음이고, 셋째 줄(압력)은 **유지 제어가 진단 채널을 닫는 방향**으로 설계돼 있다. 번역은 우리가 한 것이다 — 이 편은 곱도, 모드도, 면적도 말하지 않는다.

## ★★ 처방의 열여섯 번째 적용 (2026-09-23, `assb` 33호) — **적용 불가, 대상 없음 · 대신 압력 축에 상대극 교란의 크기가 붙는다**

`raw/papers/zhang2025_low-pressure-assb-challenges-strategies-review.md` (Zhang et al. 2025, *Adv. Mater.* 37, 2413499 — ⚠ **Review 22 쪽, 1차 측정 0**, 식 1 개 = Li/Cu 계면 응력).
곱이 설 모델도, 가를 데이터도 없다. 32호처럼 **"대상 없음" 도 한 번으로 센다.** 기록하는 이유는 이 편이 **압력 축**(처방이 아니라 [[assb-pressure-reapplication-separation-test]] 의 조작 변수)에 붙는 교란의 크기를 재수록 원자료로 준다는 것이다.

### 입력 점검

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | `EIS` 0 회 · 무음극 `R_tot`(Fig. 5A 재수록)는 저항만 | ❌ |
| **2단계** (18·25호) | + 면적을 아는 대조군 | Sakka 2022 [120] 를 인용하되 "3D 접촉 · 압력 방향" 명제로, 면적값 0 | ❌ |
| **3단계-a/b** (19호) | `Ea` · `C` 상한 | `Arrhenius` 0 — 온도는 "80 °C 면 2 MPa" 한 문장(출처 번호 둘로 갈림) | ❌ |
| **4단계** (20호) | 시간 영역 동일 검사 | 0 | ❌ |

### ★★ `[해석]` 압력 축의 교란 — 상대극 ΔP 가 조작 변수와 같은 크기

| 재수록 원자료 (33호 그림, `[도표]`) | 사이클당 ΔP | 기저 |
|---|---|---|
| [58] LCO · NCM · 혼합 양극 (Fig. 7A) | ≈0.05–0.07 MPa | 미기재 |
| [59] 흑연 ± LGPS (Fig. 3D) | ≈0.7–0.8 MPa | 미기재 |
| [88] μ-Si ‖ LTO (Fig. 4D) | ≈0.5–1.0 MPa | ≈45 MPa |
| [90] Sb ‖ Li (Fig. 4G) | ≈1.2–2.3 MPa | ≈20 MPa |

곱 `A_eff·ε_p/R_s` 의 `A_eff` 를 **압력으로 흔들어** 가르려면(되돌림 시험), 양극 `A_eff(P)` 에 들어가는 압력은 **지그 압력 + 상대극 ΔP(SOC)** 다. 산업 운전 압력(이 편 `[인쇄]` ≤2 MPa)에서 상대극 ΔP 는 **조작 변수와 같은 자릿수**이고, 양극 자신의 ΔP 는 두 자릿수 작다. ⇒ 되돌림 시험의 설계 입력에 **"상대극 ΔP(SOC) 를 먼저 재거나 정압 지그로 누른다"** 가 붙는다. ⚠ 진동은 고압 기저 · 정변위 지그에서 잰 것이다(저압 기저에서 크기 미상). 이 편은 곱도 분리도 말하지 않는다 — 번역은 우리 것.

## ★★★ 처방의 열일곱 번째 적용 (2026-09-23, `assb` 34호) — **적용 불가(데이터 0) · 대신 처방이 온보드로 번역된다: 한 펄스의 이완이 1·4단계와 `R/k` 의 공통 입력이다**

`raw/papers/liang2026_pulse-excitation-active-bms-comment.md` (Liang et al. 2026, *npj Clean Energy* 2, 16 — ⚠ **Comment 5 쪽, 1차 측정 0, 데이터 0, ASSB 0** — 도구 칸).
32 · 33호의 "대상 없음" 과 성질이 다르다: 이 편은 처방이 서는 **입력 채널(능동 펄스)** 을 BMS 에 넣자고 제안한다. 그러나 처방 단계를 명제로 쓰지는 않는다.

### 입력 점검

| 단계 | 요구 | 이 편 (`[인쇄]`) | 판정 |
|---|---|---|---|
| **1단계** (16호; τ 형 21호) | `R` 과 `C`(또는 τ) | 대역 이름 "interfacial polarization (10⁰ − 10³ Hz)" · Fig. 1c 모식도의 휘어진 상승 — `capacitan*` · `time constant` · `relaxation` **0** | ❌ 명제 없음 · `[해석]` 입력은 선다 |
| **2단계** (18·25호) | + 면적을 아는 대조군 | 0 | ❌ |
| **3단계-a** (19호 `Ea`) | 여러 온도의 `R` | **반대** — 온도 의존을 "transient, condition-dependent signals (e.g., temperature-sensitive voltage or resistance)" 로 불변 학습이 **지울 대상**에 둔다 | ❌ (채널 폐기 방향) |
| **3단계-b · 4단계** (19 · 20호) | `C = τ/R` 상한 | 0 | ❌ 명제 없음 · `[해석]` 펄스는 4단계의 본래 영역 |
| **31호 `R/k`** | 같은 차단의 `R` · √t `k` | "onset of transient diffusion (< 10⁻¹ Hz)" — 대역을 **자기 창("ms–s") 밖**에 적는다(D2) | ❌ 명제 없음 |

### ★★★ `[해석]` 한 펄스의 대수

```
V(t) − V₀ ≈ I·[R₀ + R_p(1 − e^{−t/τ})] + I·k·√t
R_p ∝ 1/(A·j₀) · C = c_dl·A · k ∝ 1/(A·√D)
⇒ τ ∝ c_dl/j₀ (A 약분) · C = τ/R_p ∝ A · R_p/k ∝ √D/j₀ (A 약분)
```

면적 손실은 `R_p` · `k` 를 같은 배수로 올리고 τ · `R_p/k` 를 두며 `C` 를 줄인다 · `j₀` 손실은 `R_p` 와 τ 를 올리고 `C` 를 둔다 · `D` 손실은 `k` 만. **세 서명이 한 펄스에 동시에 있다.**

### ★★★ OED 는 이 곱을 입력으로 풀지 못한다

이 편은 `[인쇄]` "FIM or D-optimality … ensures maximum parameter identifiability" 를 처방한다. `[해석]` 출력이 `A·j₀` 로만 의존하는 모델(이중층 · √t 항 없는 BV)에서는 **모든 입력에서 FIM 이 특이**해 D-optimality 가 0 이다. 곱을 가르는 것은 입력의 풍부함이 아니라 **(ⅰ) 곱과 다르게 반응하는 항이 모델에 있고 (ⅱ) 그 항의 대역이 샘플링된다**는 두 조건이다. 그 둘이 서면 OED 는 **실제적** 비식별(조건수)을 줄이는 도구로 쓸모가 있다 — 구조적 비식별은 위 약분표가 먼저 가른다.

### ⚠ 이 편의 두 권고가 입력을 지운다

① **재구성 경로**(펄스 → 신경망 → 등가 EIS, refs 21·22) — 처방은 적합된 `R_p` · τ 를 요구한다. ref 21 제목 "10 Hz sampling" 이면 나이퀴스트 5 Hz 위 계면 대역은 **사전이 채운다**. ② **불변 학습** — 온도(→ 3단계-a `Ea`) · 열화(→ α·β 화학량론 한계)를 지우는 사상이다.

## ★★ 처방의 열여덟 번째 적용 (2026-09-23, `assb` 35호) — **적용 불가(물리 모델 0) · 대신 데이터 기반 BMS 가 처방 채널을 잃는 두 번째 경로: 선택**

`raw/papers/roman2021_ml-pipeline-soh-estimation-uncertainty.md` (Roman et al. 2021, *Nat. Mach. Intell.* 3, 447 — ⚠ **ML 방법 논문, 1차 실험 0, 액체 상용 셀 179 개(공개 데이터), ASSB 0** — 도구 칸).
목표는 용량(Ah) 스칼라 하나이고, `A_eff·ε_p/R_s` 가 들어갈 식이 없다. 입력 채널만 점검한다.

### 입력 점검

| 단계 | 요구 | 이 편 (`[인쇄]`) | 판정 |
|---|---|---|---|
| **1단계** (16호; τ 형 21호) | `R` 과 `C`(또는 τ) | `Lagged Pseudo Resistance [Ω]` = 방전 개시 `ΔV/I`(합) — `C` · τ 0. **그리고 세 그룹 모두 특징 선택에서 탈락** | ❌ |
| **2단계** (18 · 25호) | 면적을 아는 대조군 | 0 | ❌ |
| **3단계-a** (19호 `Ea`) | 여러 온도의 `R` | 온도 입력 0(`[인쇄]` 향후 과제) | ❌ |
| **3단계-b · 4단계** | `C = τ/R` | 0 | ❌ |
| **31호 `R/k`** | 같은 차단의 `R` · √t `k` | CV 전류 꼬리의 **모양 통계**(왜도 · 첨도 · 엔트로피 · Fréchet)는 있으나 √t 해석 0 | ❌ |

### ★★ `[해석]` 선택이 지우는 이유

RF-RFE-CV 의 점수는 **용량 예측 MSE** 다. 곱의 두 인자(면적 ↔ 활물질)가 **같은 용량 감소**를 낼 때 그 둘을 가르는 정보는 용량을 예측하는 데 쓸모가 없다 —
정의상 목표와 직교하는 방향이다. 그러니 용량 목표의 특징 선택은 **분리 채널을 가장 먼저 버리도록** 설계돼 있다. 34호가 "재구성 · 불변 학습이 입력을
**지운다**(사상)" 였다면, 35호는 "선택이 입력을 **버린다**" 다. 두 경로 모두 BMS 의 **정확도를 올리는 방향**으로 작동한다는 점이 같다.

### 그리고 불확실성도 곱을 못 본다

이 편은 계보에서 불확실성을 가장 제대로 다룬다(보정 전용 셀 · isotonic 재보정 · 90 % 적중률). 그러나 곱 축퇴 방향에서 **용량 예측은 변하지 않으므로**
예측 구간은 그 방향의 폭을 볼 수 없다. **"보정된 SOH 구간이 좁다" 는 곱이 갈렸다는 근거가 되지 않는다** — 근최적 집합의 폭은 따로 잰다
([[near-optimal-set-width-measurement]]).

## ★★ 처방의 열아홉 번째 적용 (2026-09-23, `assb` 36호) — **적용 불가 · 대상 없음(종설) · 대신 확률 도구가 곱 방향의 폭을 지우는 두 경로**

`raw/papers/thelen2024_probabilistic-ml-battery-health-review.md` (Thelen et al. 2024, *npj Mater. Sustain.* 2, 14 — ⚠ **Review 33 쪽, 1차 측정 0, 액체셀 중심, ASSB 0** — 도구 칸).
확률적 ML(GPR · RVM · BNN · 앙상블 · 배깅) 종설이고 `A_eff·ε_p/R_s` 가 들어갈 식이 없다. 입력 채널은 전부 ❌(EIS 특징은 입력으로만 · `C` · τ 0 · 면적 대조군 0 · 온도는 조건 인식 입력 · `R/k` 0).

### ★★ `[해석]` 곱 방향의 폭은 이 편의 분류에 없다

이 편은 불확실성을 aleatory(비가역) ↔ epistemic(`[인쇄]` "reducible" — 데이터를 더 모으면 준다)으로 가르고, CI 는 `[인쇄]` "collapses to the true value" 로 정의한다.
곱 축퇴에서는 FIM 이 **모든 데이터량에서** 특이하므로 곱 방향의 폭은 데이터를 늘려도 줄지 않는다 — 사후가 점이 아니라 **능선**으로 수렴한다. 이 폭을 이 편의 분류로 읽으면
"데이터 부족(epistemic)" 으로 오독되고, 처방은 "더 모아라" 가 된다. 처방 표의 답은 **다른 종류의 관측**(1–4단계)이다.

### ★★ 확률적 추정이 곱을 가리는 두 경로

| 경로 | 이 편의 `[인쇄]` | 곱에 미치는 것 (`[해석]`) |
|---|---|---|
| **평균장 VI** | "a mean-field approach cannot capture parameter correlations and tends to under-predict the uncertainty" (BNN 맥락) | 곱 축퇴는 사후의 **음의 상관(능선)**으로 나타난다. 평균장은 그 상관을 지우고 좁은 주변분포 둘을 낸다 — 곱이 갈린 것처럼 보인다 |
| **상관된 학습 사전** | Ruan 2022 재인용: "the degradation modes are inherently correlated, and these correlations can be exploited to improve diagnostic accuracy" | 데이터가 못 가르는 방향을 사전의 상관이 정한다 — 같은 분포의 시험 셀에서는 정확도가 오르고, 다른 노화 경로에서는 그 몫이 사전이었음이 드러난다 |

→ 처방 표에 더하는 경고 한 줄: **"확률적 추정 결과를 처방의 입력으로 받을 때는 공분산(또는 능선)을 먼저 요구한다 — 주변분포만 좁으면 곱이 갈렸다는 근거가 아니다."** 34호(사상이 지운다) · 35호(선택이 버린다)에 이어 **세 번째 경로(추론 근사 · 사전이 가린다)** 다.

## ★★★★ 처방의 스무 번째 적용 (2026-09-23, `assb` 37호) — **처방의 원천 모델에 처방을 건다: 곱은 `A_eff·k_p·ε_p/R_s` 이고, 모델 구조가 1단계를 막는다**

`raw/papers/li2024_assb-composite-cathode-model-contact-area-edl.md` (Li, Fan, Zhang et al. 2024, *eTransportation* 20, 100315 — 9호가 해법을 위임한 [27]). NCM811/LPSCl/Li₄.₄Si, 신품만, 7 율 + 동적 사이클, PSO.

### 입력 점검

- **1단계 `R_CT·C_dl`** — ⚠ **모델 구조가 막는다.** `[인쇄]` `c^p_dl` = 5.1×10⁻⁶ **F**(각주 없음, 면적 무관 상수). `R_ct` 미인쇄 — `[재현]` 인쇄 파라미터로 중간 SOC **285 Ω**, `τ` = **1.5 ms**(x 0.99 에서 7 ms). 이 모델에서 `A_eff` 를 바꾸면 `R_ct ∝ 1/A_eff`, `C` 불변 ⇒ `τ` 가 **움직인다** — 처방 전제(면적 변화 ⇒ `R·C` 불변)의 반대가 모델에 박혀 있다. 실측 EIS 0(차단 셀만).
- **2단계 면적 대조군** — 모델 안에서만: `[도표]` Fig. 11b/e(`A_eff` 1.0 ↔ 0.3) = "면적만 바꾼 쌍" 의 모델판 ⇒ **용량 끝점 불변 · 전압 평행 이동**(`[재현]` +61 / −37 mV, 0.4 C). 실측 대조군 0.
- **3단계 `Ea`** ❌ 301.15 K 한 점.
- **4단계 `C` 상한** — `[재현]` `c^p_dl` ÷ 모델 접촉 면적(1.81 cm²) = **2.8 µF cm⁻²** ✓ 통과. ⚠ 그러나 `[도표]` Fig. 9c/f 의 `η^p_ct` 이완은 ≈**10² s** — 이 `C` 로 나올 수 없는 시상수(4–5 자릿수). **4단계를 거꾸로 건 첫 표본**: 파라미터는 상한 안인데 그 파라미터가 만들었다는 그림이 상한 밖이다(원인 미상 — `Ts` 1 s 이산화 · 다른 파라미터 · 다른 정의).
- **율 스윕 줄** — 7 율(0.4–2 C)이 있다. 그러나 `D_p,ref(C-rate)` 가 율마다 다시 정해진다 ⇒ **세 번째 실패 조건**(위 표).
- **외부 기준 줄** — GITT 식 (51) `D_p ∝ (V/S)²` 의 `S` = `[인쇄]` "total contact area between the electrolyte and the electrode"(값 미인쇄) — 31호 "상수 입력" 부류. ★ 모델은 `A_eff` 를 확산에서 빼는데 모델에 넣을 `D_p` 는 접촉 면적의 **제곱**을 품은 측정에서 온다 — 곱의 면적 인자가 **측정(확산)과 모델(BV)에서 다른 자리**에 있다.

### ★★★★ 원형 모델의 곱 — `A_eff` 는 `LAM` 이 아니라 `k` 의 쌍둥이

`[인쇄]` 식 (8) `j^p_ct = (I − I^p_dl)/(A^p_eff·a_{s,p}·A·L_p)` · (9) `a_{s,p} = 3ε_p/R_s` · (15) 표면 플럭스에 `A_eff` 없음 · (5) `j^p_0 = k_p F √c_SE √(c_max − c_sur) √c_sur`.
`[해석]` ⇒ `η^p_ct` 가 보는 것은 **`A^p_eff · k_p · ε_p / R_s`**. 9호 절(위 §정의)의 곱에 `k_p` 가 붙은 형이고, **`A_eff ↔ k_p` 는 정확한 스케일 대칭**이다(용량 · 확산 · 전해질 · 이중층 어디에도 `A_eff` 가 없다).
`ε_p` 는 용량(식 18 의 적분 극 `1/(ε_pAL_pF)`)과 확산에서 따로 붙잡힌다 — 그래서 **표면 피복형 접촉 손실은 이 모델에서 `LAM_PE` 와 구별되는 손잡이이지만, 계면 화학(`k_p`)과는 구별되지 않는다.** 18호가 `[인쇄]` "the chemical composition at the interface **or** the contact area" 로 남긴 선택지가 **식의 항등**이다.
그리고 **입자 통째 비연결에는 `ε_p` 말고 자리가 없다** — 27호(`A_el-c` 세 겹 짐) · 28호(`ε` 는 `Q_th` 에만)의 결론을 원형 모델이 그대로 갖는다.
`[재현]` 부수: 인쇄된 `k_p` 2.263×10⁻¹² 는 `[도표]` Fig. 5d 측정 11 점(≈0.7–7.2×10⁻¹¹) **밖**이다 — 항등 쌍의 한쪽(`A_eff`)을 출처 없이 고정하고 다른 쪽(`k_p`)을 PSO 로 풀면, `k_p` 가 측정과 어긋나는 만큼을 `A_eff` 의 선택이 정한다.

### ⇒ 이 적용이 처방에 더하는 것

1. **`A_eff ↔ k` 항등** (위 표 새 줄) — 처방 1단계가 가르려는 쌍이 원형 모델에서 정확한 항등이고, 그 모델은 `C` 를 면적과 떼어 놓아 1단계의 신호를 truth 에서 지운다.
2. **율 스윕 줄의 세 번째 실패 조건** (위 표 새 줄) — 율별 재적합 파라미터.
3. `[추론]` **ASSB 합성 truth 의 요구** — 이 모델로 truth 를 만들면 접촉 손실은 `A_eff(N)`(OCV 에 안 보이고 `k_p(N)` 와 같다) 또는 `ε_p(N)`(정의상 `LAM_PE`) 둘 중 하나다. 어느 쪽이든 카드 물음을 **시험하지 못하고 미리 답한다** — 27호 경고의 원형이 이 편이다. 요구 목록은 [[assb-contact-loss-vs-lampe]] §새 제약(37호).

### ⚠ 이것이 곱을 푼 것은 아니다

신품 데이터뿐이고 `A_eff` 도 `k_p` 도 흔들어 적합하지 않았다. 기여는 **곱의 원형 식**(`A_eff·k_p·ε_p/R_s`)과 **그 곱의 한쪽이 출처 없이 운반되었다는 사실**(9호와 네 자리 일치)이다.

## ★★★ 처방의 스물한 번째 적용 (2026-09-23, `assb` 38호) — **사이클마다 두 채널로 잰 첫 편: 곱을 `θ·ε_p` ↔ `η_diff` 로 가르고, 카드의 곱은 한 채널 안에 남긴다**

`raw/papers/conforto2021_chemo-mechanical-ncm-active-mass-eis-psd.md` (Conforto, Ruess, … Janek 2021, *JES* 168, 070546 — 9호 ref [30], 큐의 마지막 편). NCM811 PC/SC | Li₆PS₅Cl | In/InLi, ≈70 MPa, 40 사이클 × 4 조건, 조건당 셀 1 개.

### 입력 점검

- **1단계 `R_CT·C_dl`** — ⚠ 재료는 있고 값이 없다: 회로(Fig. 7a)에 `R_int ∥ C_int` 가 있고 매 사이클 적합됐으나 **인쇄 0**.
- **2단계 면적 대조군** — SC ↔ PC 가 입도(면적)를 바꾸지만 BET 는 PC 만(0.2 m² g⁻¹), SC 는 재소성(750 °C O₂) 시편 ❌.
- **3단계 `Ea`** — 25 · 60 °C 가 **신품 `D̃`** 에만(10⁻¹¹ ↔ 6 × 10⁻¹¹ cm² s⁻¹) ❌.
- **4단계 `C` 상한** — `C_diff/m` 520 mAh V⁻¹ g⁻¹(`[재현]` 자기 정의로는 725, ×0.72), `C_dl` 0 ❌.
- **율 스윕 줄** — 0.1 C ↔ 0.3 C 가 컷오프(4.25 ↔ 4.5 V)와 교락 ❌. 대신 **이완 OCP 두 점** 이 율 무관 게이지(위 표 새 줄).
- **SOC 추종 상 분율(22호 줄)** — `[인쇄]` 대안으로 **언급만**(ref 47 operando XRD, "requires expensive … equipment") ❌.
- **외부 액체 기준 줄** — 곱의 인자가 아니라 **게이지의 눈금**(OCP–x 기준 곡선)을 액체셀에서 수입 — 29호(`D_LIB`) · 30호(액체 대비 `D`) 와 다른 자리의 수입.

### ★★★ 두 채널이 가르는 것과 못 가르는 것

`[인쇄]` 식 (7) `m_act = Q_meas/q_act` + "disconnected … cannot contribute to the OCP any longer and can be considered inactive" · EIS-PSD `L_diff`(식 5, GA) · Fig. 9 "loss of active mass" + "increased length of the pathway".
`[해석]` ⇒ 채널 ① 은 `θ·ε_p`(카드의 곱 **그 자체**), 채널 ② 는 `L²/D̃`(유한공간) 또는 `L/(C_diff√D̃)`(반무한). 이 편은 곱을 **`θ·ε_p` ↔ `η_diff`** 로 가르고 — 그것이 채움표 Q2 반 칸이다 — **`θ` ↔ `ε_p` 는 채널 ① 안에 그대로 둔다.**
그리고 두 채널은 독립이 아니다: EIS 적합이 `C_diff ∝ m_act` 를 **고정 입력**으로 받고, 반무한 영역에서 `L ∝ C_diff` 이므로 질량 손실을 과대로 읽으면 `L` 이 작게 맞는다(§위 표 경고 줄).

### ⇒ 이 적용이 처방에 더하는 것

1. **이완 OCP 두 점 줄**(위 표) — 율 스윕 없이 `η` 를 떼는 두 번째 싼 채널(첫째는 29호 율 외삽 `Q_M`). 둘 다 `θ`+LAM 한 칸을 준다.
2. **반무한 꼬리 곱 경고**(위 표) — 저주파 EIS 로 면적 · 경로를 읽는 모든 편에 거는 전제 검사: 용량성 극한 도달 여부.
3. `[해석]` **평탄 상대극 설계의 의미** — 이 설계는 우리 degeneracy(음극 곡선 · 오프셋)를 지워 `α_PE` 를 두 점으로 식별하게 하지만, **카드의 곱은 `α_PE` 안**이라 그대로 남는다. "우리 축퇴가 없는 셀에서도 카드의 축퇴는 있다" 의 첫 실측 표본이다.

### ⚠ 이것이 곱을 푼 것은 아니다

조건당 셀 1 개 · SI 미열람 · 닫힘이 두 패널에서 15–30 % 어긋난다(`[도표]` Fig. 9a +12…+27 · 9d −14…−28 mAh g⁻¹). 기여는 **두 채널의 설계**와 **그 설계의 조건(이완 시간 · 용량성 극한)** 이다.

## ★★★★ 처방의 스물두 번째 적용 (2026-09-23, `assb` 39호) — **곱의 한 인자를 영상으로 직접 쟀다: 면적은 ×1.10, `R_ct` 는 ×14 — 곱의 나머지가 ×13 을 가져간다**

`raw/papers/sakka2022_pressure-3d-structure-composite-cathode-xct.md` (Sakka, Yamashige, … Orikasa 2022, *J. Mater. Chem. A* 10, 16602 — 원장 최상위, 25호 ref 12 · 33호 ref [120]). NCM111(LiNbO₃) | LGPS | In–Li, 신품, **제조 가압 0 → 단조 가압 0 · 6 · 12 · 50 · 100 MPa**, SPring-8 CT(화소 0.5 µm) + 동시 EIS, 2전극.

### 입력 점검

- **1단계 `R_CT·C_dl`** — 회로(SI Fig. S16)에 C 둘, **값 인쇄 0**, Nyquist 주파수 표지 0 ❌.
- **2단계 면적 대조군** — ★ **측정된 면적을 가진 첫 대조군.** `[인쇄]` "contact area fraction … with respect to the surface area of the NCM particles" = **표면 피복 `φ`**(37호 기준 `A_eff` 쪽 손잡이). `[도표]` `φ` 0.749 / 0.779 / 0.843 / 0.827 ↔ `R_ct` 8.7 / 4.1 / 1.6 / 0.62 ×10⁵ Ω (6 / 12 / 50 / 100 MPa).
- **3단계 `Ea`** ❌ 298 K. **4단계 `C` 상한** ❌. **율 스윕 줄** ❌ 0.01 C 한 율.

### ★★★★ 면적 가설의 실측 기각 — CT 척도에서

`[재현]` `R_ct·φ` = 6.5 → 3.2 → 1.4 → 0.51 ×10⁵ Ω ⇒ 면적당 전도도 **×13**. `ln 1.10 / ln 14` ≈ 0.04 — **CT 로 잰 접촉 면적은 `R_ct` 로그 변화의 ≈4 % 만 설명한다.**
원문은 `[인쇄]` "This corresponds to the increase of the contact area fraction" · "The enhanced contact area fraction … led to an order of magnitude reduction in charge transfer resistance" 로 **상관을 귀속으로 읽는다**.
`[해석]` ⇒ 37호 항등(`A_eff ↔ k_p`)에 **세 번째 인자가 붙는다**: `A_eff = φ_CT × (0.5 µm 아래 실접촉 몫)`. `R_ct` 가 보는 것은 `φ_CT × (실접촉 몫) × k_p` (+ 2전극이라 상대극 In–Li 계면). 이 편은 뒤의 셋을 가르지 않는다.

### ⇒ 이 적용이 처방에 더하는 것

1. **"영상 면적 → `R·φ` 검사" 줄**(위 표 새 줄) — 면적을 **재고도** 곱이 안 풀릴 수 있고, 그 크기가 `R·φ` 의 변화로 바로 보인다.
2. **2단계의 전제 조건** — 면적 대조군의 "면적" 은 측정 방법의 **길이 척도**를 달고 있어야 한다. 18 · 25호의 BET · 입자 기하 면적, 39호의 CT 피복은 서로 다른 척도의 면적이다.
3. `[해석]` **압력 연산자는 곱의 여러 인자를 같이 움직인다** — 공극률(→ 겉보기 전도도 +24 %) · `φ_CT`(+10 %) · 나머지(×13) · 상대극. 압력 되돌림 분리 시험([[assb-pressure-reapplication-separation-test]])의 비직교성(11호)에 실측 하나.

### ⚠ 이것이 곱을 푼 것은 아니다

점당 n = 1 · 오차 0 · 분할 문턱 미인쇄 · **분할이 질량을 보존하지 않는다**(`[재현]` NCM/LGPS 부피비 0.47 → 0.97, 고정 혼합물) · 고압 두 `R_ct` 가 Nyquist 호 지름과 ×2–3 어긋남 · 2전극. 기여는 **"면적을 영상으로 재도 안 풀린다" 는 형태와 그 크기(×13)** 다.

## ★★★ 처방의 스물세 번째 적용 (2026-09-23, `assb` 40호) — **R-LTO 원전: 3-a 와 4단계가 서고, 3-b 가 R2 귀속과 긴장하며, 1단계는 꼭짓점 낱말뿐이다**

`raw/papers/ikezawa2020_lto-reference-electrode-assb-three-electrode-eis.md` (Ikezawa … Arai 2020, *Electrochem. Commun.* 116, 106743). LiNbO₃-LCO | LGPS | R-LTO 메시 | LGPS | Li-In, 신품, 210 MPa, 3전극 EIS(7 MHz–10 mHz) + 5 율 충방전.

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | CPE 값 0 · `[인쇄]` 꼭짓점 "around 10 kHz"(R3) · "around 1 MHz"(R2) · 그림 주파수 표지 | ⚠ τ 형만 — `[재현]` `C₃` ≈0.35–0.52 µF(기하 0.45–0.66 µF cm⁻²) · `C₂` ≈22–23 nF(기하 ≈0.03 µF cm⁻²). R3 는 SOC 5 점이 있으나 `C` 가 없어 궤적 불가 |
| **2단계** 면적 대조군 | 없음 | ❌ |
| **3단계-a** `Ea` | R2 · R3, 298 · 288 · 273 K, SOC 100 % | ✅ **재료만** — `[재현]` 화소 판독 재적합 55.4 · 37.2 kJ mol⁻¹(인쇄 55 ± 1 · 37 ± 2 ✓). 노화 전후 없음 |
| **3단계-b** `C` 물리 상한 | `C₂` | ⚠ `[추론]` R2 = "LiNbO₃ 층 · LiNbO₃\|LGPS 계면" 이면 CAM 표면 전체의 nm 급 층이라 µF cm⁻² 급이어야 하는데 **기하 면적당으로도 두 자릿수 작다**(`ε_r` · `d` 가정). 꼭짓점 ≈1 MHz 는 저자가 기준극 artifact 를 의심한 대역("deviation observed above 1 MHz")의 문턱 |
| **4단계** 시간 영역 | Li-In: DC(Fig. 1d) ↔ EIS(Fig. 2a) | ✅ `[재현]` C/2 탈리튬 21–23 mV ↔ `Z′(1 Hz)` ≈82.6 Ω × 0.288 mA = 24 mV |

### ★★ 같은 상태의 R3 가 세 값이다

`[도표]` 명목상 같은 상태(LCO 만충, 298 K)의 R3 = **30.6**(Fig. 2d) · **37.7**(Fig. 3b) · **45.5 Ω**(Fig. 3d), Nyquist 호 끝 ≈50 · ≈65 · ≈70 Ω — 회로 차가 아니라 **스펙트럼이 다르다**. 원문 설명 0. ⇒ 1단계를 SOC 축으로 걸 때 **축의 효과(R3 25 → 100 %: −7 %)가 미설명 상태 간 산포(×1.49)보다 작으면 그 궤적은 읽을 수 없다** — 처방 입력의 전제 조건 하나("같은 셀 · 순서 기록 · 반복 상태의 재측정")가 여기서 나온다.

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 "3전극 옴 몫은 기준극 위치가 정한다"**(위 표). 3전극은 곱을 가르기 전에 **분리막을 두 전극에 나눠 싣는다** — 그 비율이 기준극 위치(여기 SE 질량 1 : 3.2)다.
2. **2전극 양극 호의 상대극 오염 크기**: 1 kHz 이상 호 합 ×1.86(신품 LCO\|Li-In). 2전극 셀에 1단계를 걸면 `R` 의 ≈절반이 다른 계면의 것이다 — 16 · 17호의 "overlapping anode impedance" 에 첫 직접 수.
3. **3-a 재료 + 4단계 통과가 같은 지면에 있는 두 번째 표본**(19호 뒤) — 노화 셀 한 쌍만 있으면 "`Ea` 불변 + `R` 증가" 검사가 된다. 이 그룹의 후속(18호)은 `Ea` 를 노화 전후로 재지 않았다.

### ⚠ 이것이 곱을 푼 것은 아니다

신품 · 열화 0 · 면적 대조 0 · CPE 미인쇄 · n 미기재 · R3 세 값. 기여는 **3전극 분해 자체가 곱 앞에 두 가지(기준극 위치 몫 · 상대극 오염)를 끼워 넣는다는 크기 둘**이다.

## ★★★ 처방의 스물네 번째 적용 (2026-09-23, `assb` 41호) — **적용 불가(EIS 0) · 대신 3전극 옴 배정의 극단 표본: 배면형 기준극은 분리막 옴 전부를 상대극 채널에 싣는다**

`raw/papers/nam2018_three-electrode-assb-failure-modes-li-in-depletion.md` (Nam … Jung 2018, *J. Mater. Chem. A* 6, 14867). Sn | Li₆PS₅Cl | Li₀.₅In 반쪽전지 · NCM622 | Li₆PS₅Cl(50–60 / 730 µm) | Gr · Si–C 완전지, RE 는 **WE 뒷면**에 추가 SE 층, 3전극 DC 곡선만(EIS 0), 74 MPa 운전.

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | **EIS 0**(`impedance` 는 서론 인용뿐) | ❌ |
| **2단계** 면적 대조군 | 없음(양극 건전성은 SEM 정성 부정 한 줄) | ❌ |
| **3단계-a** `Ea` | 30 °C 한 점 | ❌ |
| **3단계-b** `C` 물리 상한 | 없음 | ❌ |
| **4단계** 시간 영역 | 3전극 DC — 전류 반전 계단(Fig. 5b · S10b) · 컷오프 항등식(Fig. 2d · 3c) | ⚠ 옴 몫의 **상한**만, 보상 0 |

### ★★★ 파생 채널에 옴이 몰린다

`[인쇄]` "applying the current between the WE and CE while the open-circuit voltage of the WE/RE was measured" — RE 가 WE 뒷면이라 **WE/RE 에는 분리막 옴이 안 들어가고**, CE 전위(= WE/RE − WE/CE 파생)에 **분리막 전부 + WE 층 이온 경로**가 들어간다. 20호 `[인쇄]` "ohmic resistances were not incorporated into the voltage measurements"(이 배치를 두고)는 **WE 채널에서만 참**이다.
`[도표]`/`[재현]` 전류 반전 계단 절반(옴 + 빠른 분극의 상한): **1 C · 50–60 µm SE ≈0.10 V**(Gr 최저 ≈−0.02 V) · **2 C · 730 µm SE ≈0.20 V**(Gr 최저 ≈−0.15 V) ⇒ 원전의 "Gr 이 0 V 아래로 간다" 는 **파생 채널의 부호 판정이 계단 안에 있다** — 도금 자체는 ⁷Li NMR · Ni-NW 감지극이 따로 세운다.

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 "배면형 기준극은 분리막 옴 전부를 상대극 채널에 싣는다 — 파생 채널의 부호 판정은 전류 반전 계단 절반과 먼저 비교한다."** 40호 "3전극 옴 몫은 기준극 위치가 정한다"(1 : 3.2)의 **극단(0 : 1)** 이다. 우리 α · β 이식판이 3전극 자료를 받을 때 **어느 채널이 측정이고 어느 채널이 파생인지**를 입력 명세에 넣는다.
2. **컷오프 항등식**: 컷오프가 WE/CE 에 걸리면 상대극 "종단 전위" = WE 종단 + 오프셋이다 — 상대극의 `R` 이나 과전압으로 쓰지 않는다.
3. **2전극 두 서명이 다른 이름의 것**: 적재 의존 용량 부족(`LAM` 서명 → 상대극 표면 접근성) · 쿨롱 효율 저하(`LLI` 서명 → 연성 단락 누설). 곱을 가르기 **전에** 두 오염을 배제하는 3전극 한 번이 필요하다.

### ⚠ 이것이 곱을 푼 것은 아니다

양극 용량 손실 분석 0 · EIS 0 · 면적 0 · n 0. 기여는 **3전극 분해가 곱 앞에 끼워 넣는 배정 오염의 크기 둘**(≈0.10 · ≈0.20 V 계단 절반)과 항등식 하나다.

## ★★ 처방의 스물다섯 번째 적용 (2026-09-23, `assb` 42호) — **상대극 쪽 표본: 액체 EIS 의 R·C 가 저자의 면적 설명을 20 % 만 받치고, 고체 대칭셀의 4단계가 SE 옴 하한에서 먼저 떨어진다**

`raw/papers/santhosha2019_indium-lithium-electrode-phase-formation-redox-potential.md` (Santhosha … Adelhelm 2019, *Batteries & Supercaps* 2, 524). In 원판 | LiTFSI DOL/DME | Li 액체 3전극(적정 + EIS 0 · 45 · 52 at%) · In–Li | β-Li₃PS₄ | In–Li 대칭 2전극(DC 만) · 양극 없음(CuS 2전극 곡선 둘).

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | **액체** In 전극 R_CT · CPE_CT 세 조성(SI 표 1–3, CPE 지수 미인쇄 · 단위 µF) | ⚠ **부분** — 저자가 `[인쇄]` "the low remaining amount of In might be responsible for higher charge transfer resistance"(면적 설명). 0 → 45 at%: R_CT ×4.61 · CPE_CT ×0.73 ⇒ `[재현]` R·C ×3.38, **면적 몫 ≈20 %** · 45 → 52 at%: R ×0.153 · C ×3.87 ⇒ 면적 방향 몫 ≈72 % |
| **2단계** 면적 대조군 | XRD 잔류 In(정성, "minor amount") | ❌ |
| **3단계-a** `Ea` | 실온 한 점(Arrhenius 는 SE 벌크뿐) | ❌ |
| **3단계-b** `C` 물리 상한 | CPE_CT ≈14–54 µF cm⁻²(이중층 대역) · CPE_SL ≈6.4 µF cm⁻²(`[재현]` ε_r 5–10 이면 ≈0.7–1.4 nm) | ✅ 자릿수만 — ⚠ CPE_SL 이 두 표에서 7.2 ± 0.6 µF 로 동일 |
| **4단계** 시간 영역 | 액체: 펄스 분극 ↔ EIS 합 · 고체: 대칭셀 DC ↔ SE 벌크 옴 | 액체 ✅(45 at% `[재현]` 361.7 Ω × ≈0.28 mA ≈101 mV ↔ 인쇄 "about 0.10 V") · **고체 ❌** — 셀 12 Ω cm² ↔ SE ≈400–570 Ω cm²(`[재현]`, SI 자기 격자 · 전도도) |

### ★★★ 4단계의 하한 — SE 벌크 옴

2전극 셀의 전압을 전극 · 계면 몫으로 가르기 전에 **SE 벌크 옴(두께 ÷ 전도도)이 하한**이다. 42호 대칭셀은 그 하한의 **1/25–1/47** 이다 — 곱(`A_eff·k`)의 어느 인자를 말하기 전에 **전류가 이온 경로로 흘렀는지**가 서지 않는다(`[추론]` 전자 경로 · 전도도 오기 · SE 양 오기). 이 편의 "In–Li 조성이 계면 저항을 ×15 바꾼다" 는 그 위에 있다.

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 "4단계를 SE 벌크 옴 하한과 먼저 대조한다 — 2전극 · 대칭셀 저항이 그보다 작으면 곱을 가르기 전에 전자 경로를 의심한다."** 41호 "배면형 기준극 → 분리막 옴 전부 상대극 채널" 과 짝: 옴을 **어느 채널에 싣는가**(40 · 41호) 앞에 **옴이 있는가**(42호).
2. **면적 설명 → R·C 검사의 둘째 표본**(39호 `R_ct·φ` ×13 다음): 저자가 "남은 In 양"(면적)으로 설명한 R 증가를 C 가 ≈20 % 만 받친다 — **상대극 쪽**, 액체, CPE 지수 미상.
3. **상대극 조성이 계면 저항 인자를 움직인다** — 44 ↔ ≈75 at% 에서 대칭셀 저항 ×15 이상(Li-rich 셀은 ±0.2 V 한계에 눌려 하한). 2전극 완전지 적합에서 이 몫은 양극 `R` 로 들어간다(40호 "2전극 양극 호의 ≈절반이 상대극" 과 같은 방향).

### ⚠ 이것이 곱을 푼 것은 아니다

양극 없음 · 액체 EIS · 셀 1 개 · CPE 지수 미상 · 고체 EIS 0. 기여는 **검사 순서 하나(SE 옴 하한)** 와 **상대극 쪽 R·C 표본 하나**다.

## ★★★★ 처방의 스물여섯 번째 적용 (2026-09-23, `assb` 43호) — **음극 첫 적용: 1단계가 완비돼 면적 서명을 주고, 3-a 가 같은 호에서 반대로 말하며, 반쪽전지가 곱을 `LAM_NE` ↔ 고립 두 항으로 순수하게 남긴다**

`raw/papers/fukunishi2023_graphite-three-electrode-impedance-cyclability.md` (Fukunishi … Arai 2023, *ACS Appl. Energy Mater.* 6, 10908 — **18호와 다른 논문**). 흑연 : LPSI 20 : 80 wt% | LPSI | R-LTO 메시 | LPSI | Li-In, 110 MPa, 3전극 EIS(7 MHz–5 mHz) · RT 1 C × 500 → 같은 셀 333 K 1 C × 50, 전후 0.05 C 곡선 + 만리튬 EIS + 5 온도 Arrhenius.

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | Table 3 — `R_X` · `R_CT` 의 `R` · CPE-T · CPE-P, **노화 전후 모두 ±** | ✅ **계보 첫 완비**(18호는 후 상태 P 없음 · `C` ± 없음). `[재현]` `C_eff = (R·Q)^{1/P}/R`: `R_CT` 46 → 20 mF(×0.43 ± 0.2) ↔ 1/`R` ×0.47, τ 1.06 → 0.97 s ⇒ **면적 서명**. `R_X` 0.17 → 0.028 µF, τ ×1.45 — 전 상태 P ±0.04 가 τ 에 ×2.1 ⇒ **미정** |
| **2단계** 면적 대조군 | 입도 D50 5.0 / 11.2 / 30.0 µm | ⚠ 2전극 · 다른 공급처 분말 · **첫 리튬화 비가역 용량만**(`[인쇄]` (B) 96 / 52 / 21 mAh g⁻¹, `[재현]` (B)·D 480–630) — 면적 비례는 보이나 `R·C` 대조군은 아니다 |
| **3단계-a** `Ea` | 세 성분 × 5 온도 × 전후 | ✅ 입력(40호 절이 바란 "노화 셀 한 쌍"). ❌ **결과가 1단계와 충돌**: `R_CT` 22(1) → 27.5(3) kJ mol⁻¹ — 면적만이면 불변. `[재현]` 전지수 불변이면 293 K ×9.6 인데 관측 ×2.15 ⇒ 3-a 로는 면적이 ×≈4.5 **늘어야** 한다 |
| **3단계-b** `C` 물리 상한 | `C_eff` ↔ `[추론]` 기하 표면 1.46 cm²(흑연 0.6 mg · 2.2 g cm⁻³ 가정) × 10–50 µF cm⁻² | ❌ `R_CT` 호 20–46 mF = **×270–3,200** — "전하이동" 이 **네 번째로** 상한을 넘는다(19호 `P2` → 20호 → 21호 → 43호). 흑연 단계 2상 평탄의 화학용량(21호 In 과 같은 부류) 후보 · `R_X` 0.17 µF 는 막 자릿수(ε_r 10 이면 ≈75 nm) |
| **4단계** 시간 영역 | 0.05 C dQ/dV 봉우리 간격 증가 ↔ EIS `ΔR` 79 Ω | ✅ 복합체 질량 읽기(흑연 0.6 mg, 11.2 µA): 예측 1.8 ↔ `[도표]` ≈+1.5 mV. 흑연 3.0 mg 읽기면 8.8 mV ❌ — **지면의 질량 모호성("graphite composite (3.0 mg)")을 4단계가 푼다** |

### ★★★★ 반쪽전지는 음극 곱을 순수하게 남긴다

상대극 Li-In 이 Li 저장소(`[재현]` ≈18 배)라 **WE 용량 손실에 `LLI` 가 없다** — 0.05 C 에서 추가 옴 강하 ≈1 mV 라 동역학도 작다 ⇒ 용량 채널 = `(1−LAM_NE)(1−u)` 한 곱. 원전은 이 곱에 `[인쇄]` "loss of the active material"(dQ/dV **높이** 감소)이라는 이름 하나를 붙인다. 그런데 `[도표]` 봉우리 높이 비가 0.53–0.70(주 봉우리) · 1.03(0.21 V) 로 **용량 비 0.76 의 균일 비례가 아니다** — 높이는 넓어짐에도 준다.

`[재현]` 1단계 면적 비(×0.43–0.47)를 용량 비(×0.75–0.78)와 대면 **면적 손실 > 용량 손실** ⇒ `(1−u)·φ ≈ 0.45` · `(1−u)(1−LAM) ≈ 0.76`: 면적 손실의 대부분은 **연결된 입자의 피복 감소**(`φ` — 39호가 CT 로 잰 그 양, 37호의 `A_eff ↔ k` 쌍)이고, **`u` 와 `LAM_NE` 는 한 곱에 남는다.** 카드 물음의 양극 구조(`LAM_PE` ↔ 접촉)가 **음극에서 `LAM_NE` ↔ 고립**으로 그대로 선다 — 액체셀 `LAM_NE` 결론과 섞지 않는다(음극 축이 흑연 반쪽전지다).

### ★★★ 두 면적-불변 채널이 같은 호에서 충돌한다

19호 검사 B 는 **서로 다른 세 계면**에서 `C` 채널과 `Ea` 채널이 70 배 충돌했다. 43호는 **동일 계면 · 동일 셀 · 노화 전후**에서 1단계(면적 ×0.43)와 3-a(면적 ×≈4.5 필요)가 반대로 간다. 그리고 노화 뒤 **세 성분의 `Ea` 가 27.6(3) · 27(3) · 27.5(3) 으로 모인다**(원문: 둘은 "nearly unchanged", 하나는 "considerably decreased"). 신품에서도 `R_CT` `Ea` 22(1) 은 `R_SE` 22.9(7) · LPSI 벌크와 구별되지 않고 `CPE_CT-P` 0.45 는 전송선 45° 자리다 — 10호 §"EIS 는 대가를 받는다"(전하이동 ↔ 기공 이온 저항)의 **음극 실측 표본**.

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 "면적 서명 ↔ 저율 용량 비 대조 — 반쪽전지 음극"**(위 표). 곱을 가르지는 못해도 **면적 손실의 종류(피복 ↔ 고립)의 하한**을 준다.
2. **3-b 를 1단계 앞에**: 이 호처럼 `C` 가 이중층 상한을 수백 배 넘으면 1단계의 "면적 서명" 은 `C ∝ A` 전제 없이 읽힌 것이다 — 3-a 와의 충돌은 그 전제 쪽이 약하다는 신호로 먼저 읽는다.
3. **노화 뒤 `Ea` 수렴 = 호 분리 경고등**: 여러 호의 `Ea` 가 한 값으로 모이면 성분별 배정 전에 **근최적 폭**([[near-optimal-set-width-measurement]])부터 — 원전의 "`R_X` = most serious cause" 가 그 수렴 위에 있다.

### ⚠ 이것이 곱을 푼 것은 아니다

n = 1 · RT 500 → HT 50 누적 이력 · 용량은 그림 판독 · 봉우리 넓이 없음 · `C ∝ A` 전제가 3-b 에서 약함 · 흑연 밀도 · BET 미인쇄. 기여는 **음극 판 곱의 형태**, **두 채널 크기 대조의 첫 표본**, **1단계 ↔ 3-a 의 동일 계면 충돌**이다.

## ★★★ 처방의 스물일곱 번째 적용 (2026-09-23, `assb` 44호) — **GITT 식 한 줄 안의 곱: 대조 셀 가정으로 쪼갰고, 그 가정의 근거가 처리 셀에도 성립한다 — 계보에서 가장 이른(2015) 면적 대조군은 BET 로 반증된다**

`raw/papers/jin2015_lithium-silicide-anode-electrode-design-assb.md` (Jin, Park, Park, Lim 2015, *Electrochim. Acta* 185, 242 — **20호 셀의 원전**). Li₄.₄Si 단층 작업전극 \| 70Li₂S·30P₂S₅ 유리 \| In 박 상대극(반쪽 Case 1 · 2 — 2차 밀링 유무만 다름), 30 MPa 제조, GITT ~600 µA × 10 min / 20 min, 실온. 완전지 Case 3–7(TiS₂ 50 : SE 50 wt%, N/P 8.4).

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | EIS 는 Case 5/6 신품 2전극 두 장, 적합 · `C` 0 | ❌ |
| **2단계** 면적 대조군 | ★ **2차 밀링 쌍 + BET**(2.7 → 23.4 m² g⁻¹, ×8.7), 작업전극 조성 동일(전해질 0) | ✅(부분) — **계보에서 가장 이른 면적 대조군 + 독립 면적 측정**. 면적 가설 예측 ×8.7 ↔ GITT `S` 비 ×2.07 — 로그로 ≈34 %. 25호(SE 입도 쌍, 통과)와 반대 · 18호 검사 A(CAM 입도 쌍, 실패)와 같은 쪽 |
| **3단계-a** `Ea` | 실온 한 점 | ❌ |
| **3단계-b** `C` 상한 | `C` 없음 | ❌ |
| **4단계** 시간 영역 | GITT 자체. `C = τ/R` 불가(성분 분리 0). 42호 줄 "SE 옴 하한 먼저": `[재현]` 분리막 0.36 mm → 130 Ω ↔ Fig. 9B 고주파 절편 `[도표]` ≈100–120 Ω | ⚠ 옴 하한만 ✓ |

### ★★★★ 곱이 식 안에 있다 — `√D · S / θ`

Weppner–Huggins 단시간 해의 `m_B V_M / M_B` 는 **참여 부피를 전 질량으로** 둔 것이다. 참여 분율 `θ` 를 살리면 `ΔE_s/ΔE_t ∝ √D · S / θ` — 카드의 세 손잡이(동역학 `D` · 면적 `S` · 고립/`LAM` 의 `θ`)가 **측정량 하나**에 곱으로 들어간다. 원전은 Case 1 에서 `S` = 기하(`[인쇄]` "there was no addition of electrolyte to the working electrode") · 두 셀 `θ` = 1 · `D` 공통으로 두고 Case 2 차이를 **전부 `S`** 에 준다. ⚠ **Case 2 작업전극에도 전해질이 없다** — 같은 근거를 Case 2 에 쓰면 차이는 `D`(×≈3.4–4.3) 또는 `θ` 로 간다. `[재현]` 참여 용량 비(`[도표]` GITT 길이 ≈×2.75)를 `θ` 로 넣으면 `S` 비 ≈×4.7–5.7 — **이름표가 가정 하나에 ×2.3–2.8 움직인다.** 인쇄값(`D` 1.0 × 10⁻⁸ · `S` 3.19 cm² · "2 배")은 세 계단 중 **셋째** 것이고(계단별 `D` ×2.5 폭), Table 2 `ΔE_t` 는 저자 표지 펄스 그림값의 ×≈2 다(`D` 로 ×≈4).

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 "외부 기준 줄의 네 번째 배정 — 같은 계의 '면적 기지' 대조 셀"**(위 표). 29호(액체 `D_LIB` 수입) · 30호(전부 `D`) · 31호(BET 상수 `A`)에 이어 **네 번째 쪼개기 방식**이고 시간상 가장 이르다. 검사는 **가정 근거의 대칭성**: 대조 셀을 고른 이유가 비교 셀에도 참이면 그 쪼개기는 데이터가 아니라 선택이다.
2. **`θ` 는 GITT 식의 `m_B` 에 숨는다** — 반쪽전지 GITT 로 뽑은 `D` · 면적은 **참여 분율 = 1** 을 조건으로 한다. 38호 "이완 OCP 두 점 = 연결 질량" 과 짝: 그쪽이 `θ·ε_p` 를 재면 이쪽의 `√D·S` 를 뗄 수 있다.
3. **적용 조건 `r²/D ≫ τ`** — 입도를 줄이는 처리의 효과를 반무한 식으로 읽으면(`[재현]` r ≈3 µm → 9 s ≪ 600 s) 식 밖이다.

### ⚠ 이것이 곱을 푼 것은 아니다

n = 1 · 신품 · 표–그림 `ΔE_t` ×2 · 상대극(비리튬화 In 박, 질량 미인쇄) 평탄 가정이 `ΔE_s²` 로 들어간다(계단당 1 mV → `D` ×0.72–1.35). 기여는 **곱의 세 인자가 GITT 식 한 줄에 있다는 원형 표본**과 **대조 셀 가정의 대칭성 검사**다.

## ★★ 처방의 스물여덟 번째 적용 (2026-09-23, `assb` 45호) — **곱 앞의 분배: 합 일치는 두 반쪽의 나눔을 검증하지 못하고, 3-b 가 반쪽 하나에만 있는 호를 거른다 — 2전극 적합의 비유일성은 같은 셀 3전극 반쪽이 고른다**

`raw/papers/hertle2023_micro-reference-electrode-lithiated-gold-wire-assb.md` (Hertle … Janek 2023, *JES* 170, 040519 — "0 V 리튬화 금선" 원전). NCM851005 \| Li₆PS₅Cl(3E 분리막 200 mg) \| Au 도금 W μ-RE(분리막 가운데) \| In/InLi, 374 MPa 제조 · 63.7 MPa 운전, 신품, EIS 300 kHz–100 mHz.

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | 3E 양극 TLM: σ_ion(eff) 0.145 mS cm⁻¹ · R_CT 17.8 Ω cm² 두 값 · CPE 미인쇄(본문이 가리킨 Table S1 은 2E 적합) · 한 상태 | ❌ |
| **2단계** 면적 대조군 | 없음 | ❌ |
| **3단계-a** `Ea` | 25 °C 한 점 | ❌ |
| **3단계-b** `C` 상한 | ★ 양극 반쪽 호 #1(원문 "caused by the SE separator"): `[재현]` Fig. 12 −Im(100 kHz)/R ≈0.33 → ωτ ≈0.38 → τ ≈0.6 µs · R ≈57 Ω(고주파 Re 전부를 #1 로 둔 가정) ⇒ **C ≈10 nF** ↔ 분리막 반쪽(≈0.68 mm) 기하 용량 ≈10–100 pF(ε_r 10–100) | ✅ **배정 실패 ×100–1000** — SE 벌크 호가 아니다(입계 · 기준극 채널 후보). 같은 셀 2E 회로(Fig. 5 = SI Fig. S4)는 분리막을 저항 하나로 둔다 |
| **4단계** 시간 영역 | LTO 1 C 과전압 ≈300 mV ↔ LTO 임피던스 미인쇄 · In/InLi TSRE ±40 mV 는 다른(무가압) 셀 | ❌ |

### ★★★ 합 일치는 분배를 보지 않는다

`[재현]` 셀 A(Fig. 5 · 11 · S7): 반쪽 고주파 45 + 51.5 = 96.5 ↔ 전체 98 · 저주파 100 + 65 = 165 ↔ 165 — 합은 맞는다. 그러나 **같은 셀이면 이것은 키르히호프 항등식**이고, 기준극 위치가 분리막 · 전극 임피던스를 두 반쪽에 **어떻게 나눴든** 성립한다. 분배의 검사는 40호 줄(분리막 질량비: 여기 100 : 100 mg ↔ 45 : 51.5 Ω cm² ✓)이 하고, **반쪽 하나에만 있는 호**는 3-b 가 거른다. 검증 그림(Fig. 10)은 `[재현]` 다른 셀(고주파 ≈49 Ω cm²)이다.

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 "합 일치는 분배를 검증하지 않는다 — 반쪽에만 있는 고주파 호는 3-b 로 먼저 거른다"**(위 표). 40호(분배의 크기) · 41호(분배의 극단) 에 이은 **분배의 검증 불가성**.
2. **3-b 의 두 번째 용도** — 물리 배정(`LAM`/면적)의 거름망만이 아니라 **기준극 채널 artifact 의 거름망**이다.
3. **순서**: 2전극 적합의 전극 간 비유일성(`[인쇄]` 두 적합 "equally well", `R_Anode` ×3.6)을 **같은 셀 3전극 반쪽으로 먼저 고정**하고(S7 → Fit 1, 우리 판독), 그 다음에 전극 안 곱을 가른다. 3전극도 전극 안 **모델 구조**(TLM ↔ 직렬)는 못 고른다 — 원전은 "physically meaningful" 로 골랐다.

### ⚠ 이것이 곱을 푼 것은 아니다

신품 · 한 상태 · `C` 미인쇄 · 열화 0 · n 미기재. 3-b 판정은 R · ε_r · 호 모양 가정 위다. 기여는 **곱 앞 단계(전극 간 분배)의 검증 한계**와 그 거름망이다.

## ★★ 처방의 스물아홉 번째 적용 (2026-09-23, `assb` 46호) — **Li 음극 계면: 저자가 "면적 또는 절연 SEI" 를 인쇄하고 두 갈래를 "활성 접촉 면적 감소" 로 합쳤다 — 4단계만 부분 적용, 판별 설계(역방향 반쪽 짝)는 반쪽이 막혔다**

`raw/papers/schlenker2020_li6ps5cl-li-metal-lifetime-three-electrode.md` (Schlenker … Ehrenberg 2020, *ACS AMI* 12, 20012). Li\|Li₆PS₅Cl\|Li 대칭셀 · Au 도금 W 매립 기준극 · 0.30 mA cm⁻² 박리 중 EIS 10⁶–10⁻¹ Hz · 운전 "about 6 MPa" · 온도 미인쇄. 양극 없음 — **곱의 Li 음극 판**.

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | R3(계면) 5 상태 `[도표]` ≈1.5 · 4.1 · 5.9 · 7.8 · 8.8 Ω · C3 는 대표값 하나(10⁻⁷ F cm⁻²) | ❌ |
| **2단계** 면적 대조군 | 면적 비대칭 셀(Fig. 7 — 크기 · 전류 미인쇄, 전압만) · 압력 스윕(Fig. 6 — **다른 SE**, R_Ws · α 만 적합) | ⚠ 손잡이 둘, 판독이 R·C 가 아니다 |
| **3단계-a** `Ea` | 온도 미인쇄 | ❌ |
| **3단계-b** `C` 상한 | C3 10⁻⁷ · C2 "10^10"(부호 오기) — **규격화 면적 미인쇄** | ⚠ 판정 불가 |
| **4단계** 시간 영역 | `[재현]` DC 면적저항 77–117 Ω cm²(Fig. 1a,b, 캡션 J) ↔ 3E 반쪽 합(0.1 Hz 끝, 다른 셀) ≈24 Ω cm²(면적 ≈0.16 cm²) | ✅ 부분 — **≥2/3 가 0.1 Hz 아래**(저자 공공 확산 서사와 방향 일치, 저자는 대조하지 않음) |

### ★★★ 곱이 저자 문장 안에서 한 이름이 된다

`[인쇄]` "either with a decreasing interface area … as R ∼1/A or an ionically insulating SEI formation at the interface, leading to a decreasing active contact area" — 두 갈래의 끝이 같은 말이다. `[해석]` 계면 저항은 `A_geom × f_pass`(기하 접촉 × 화학적 통과 분율)의 역수만 본다 — 37호 `A_eff ↔ k` 항등의 음극 판. 저자의 배정(면적 쪽)은 **XPS 음성**(S 2p ≤6 at%) · **가역성 논증**(반주기마다 되풀이되는 상승) · **도금 쪽 반대 부호** 세 논증이고, 스스로 "open question" 이라 적었다.

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 후보 "역방향 반쪽 짝"**(위 표). 면적 ↔ 계면층을 **방향**으로 가르는 설계 — 이 편이 반쪽만 실행했다.
2. **4단계의 대역 밖 몫** — DC 와 EIS 대역(여기 0.1 Hz 하한)의 차는 곱의 어느 인자가 아니라 **대역 밖 과정**(여기 공공 확산 후보)의 크기다. 4단계를 쓰기 전에 EIS 하한 주파수와 DC 시간 척도를 맞춘다.

### ⚠ 이것이 곱을 푼 것은 아니다

양극 없음 · 상태별 `C` 없음 · 셀 수 미인쇄 · DC ↔ EIS 는 다른 셀. 기여는 **곱이 저자 문장 안에서 한 이름으로 합쳐지는 표본**과 **역방향 짝**이라는 판별 설계다.

## ★★ 처방의 서른 번째 적용 (2026-09-23, `assb` 47호 — ⚠ **액체셀**, 도구 칸) — **1단계가 Li\|Li 에서 면적 서명을 주고, 3-b 가 "전하이동" 을 다섯 번째로 떨어뜨리며, 연구 간 비교가 남의 논문 면적 추정으로 곱을 고정한다**

`raw/papers/solchenbach2016_gold-wire-micro-reference-electrode-liquid-t-cell.md` (Solchenbach … Gasteiger 2016, *JES* 163, A2265 — GWRE 원전). LP57 액체 · Swagelok T-셀 · Li\|Li(∅11 mm) 와 LFP\|흑연 · PEIS 5 mV 100 kHz–0.1 Hz. 카드의 곱(`A_eff·ε_p/R_s`)은 대상이 없다 — 처방의 **전제 · 이름표 검사**만 선다.

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C`(τ 형) | Li\|Li WE ↔ CE: 두 호 모두 꼭짓점 마커 공통(1.3 kHz · 1 Hz) · `[도표]` 고주파 호 폭 ≈81 ↔ ≈131 Ω | ✅ **τ 보존 → `C` 비 ≈1.6 = 면적 서명.** 저자 "거칠어짐"(`[인쇄]` "We believe") 과 양립 — 면적의 원인(박리 핏팅 ↔ 원판 간 차)은 못 가름. `[재현]` 뺀 Li 균일 두께 ≈0.77 nm |
| **2단계** 면적 대조군 | 흑연 BET 5 m² g⁻¹ × 5.9 mg cm⁻²(자기) ↔ Burns 셀 로딩 · BET(**다른 논문에서 추정**, 저자 "only an estimate") | ⚠ 아래 새 줄 — `[재현]` 거칠기 비 4.2(인쇄 "∼5") ↔ `R_CT` 비 6.0 · 3.75 · 3.2(VC 세 점) |
| **3단계-a** `Ea` | 25 · 10 °C 가 다른 셀 · 다른 절 | ❌ |
| **3단계-b** `C` 상한 | Li\|Li `[재현]` "SEI" ≈1.6 / 1.0 µF cm⁻² · "charge transfer" ≈10 / 7 mF cm⁻² | ✅ **"전하이동" 이름표 ×700–1000 실패 — 다섯 번째**(19 · 20 · 21 · 43호), **계보 첫 액체 표본** — ASSB 고유 현상이 아니다 |
| **4단계** 시간 영역 | Fig. 6 `[인쇄]` "overpotentials … do not change" — 수 0 | ❌ |

### ⇒ 이 적용이 처방에 더하는 것

1. **외부 기준 줄의 다섯 번째 배정**(위 표 새 줄): 연구 간 비교에서 면적을 **다른 연구실 논문의 로딩 · BET 추정**으로 고정하고 `R` 차를 면적에 돌린다. 저자는 고지했고 BET 규격화 축을 **병기**했다(곱 `R·A` 를 축으로 올린 사례). `[재현]` 세 점의 비가 ×1.9 퍼져 **단일 면적 인자로 닫히지 않는다** — 저자 단서("A different BET … would also affect the amount of additive per unit surface")와 같은 방향.
2. **3-b 의 대조군**: "전하이동" 이름표 실패가 액체 Li 금속에서도 같은 자릿수(10⁻² F cm⁻² 급)로 나온다 — 21호 ASSB Li\|Li(≳0.64 mF cm⁻²)와 같은 부류. 실패를 ASSB 계면 탓으로 돌리기 전에 이 대조를 댄다.

### ⚠ 이것이 곱을 푼 것은 아니다

액체 · 양극 곱 대상 없음 · 셀 1 개(Li\|Li) · n = 2(VC). 1단계 · 3-b 는 미폐 호 R 하한 · 이상 RC 가정 위다.

## ★★ 처방의 서른한 번째 적용 (2026-09-23, `assb` 48호) — **상태축 `R_CT` 는 있고 `C` 는 없다: 곱은 소거법으로 호를 고르고 원인을 `k` 쪽으로 읽었다 — 대신 "적합 품질이 귀속을 알리지 않는다" 를 같은 셀에서 두 번 인쇄**

`raw/papers/dugas2021_engineered-three-electrode-cell-assb-li-in-reference-layer.md` (Dugas … Tarascon 2021, *JES* 168, 090508). WE(LTFS · NMC622 · TiS₂ : SE 70 : 30, 탄소 0) \| SE \| Li₀.₅In : SE 전면 기준층 \| SE \| CE, ∅8 mm, 1 t cm⁻² 운전, 실온, EIS 200 kHz–1 mHz(2 h 마다 · 1 h 휴지 뒤).

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | LTFS · TiS₂ `R_CT`(SOC, N) 연속(Fig. 8b · d) — `Q` · α 미인쇄, 꼭짓점 주파수는 Fig. 6 · 7 네 상태뿐 | ❌ 상태축 `C` 없음 |
| **2단계** 면적 대조군 | 손 분쇄 ↔ 볼밀(같은 NMC · SE) — 볼밀이 계면 반응성도 키운다(`[인쇄]` 초기 경사 27 ↔ 2.3 mA h g⁻¹) | ⚠ 면적 · 화학 교락 |
| **3단계-a** `Ea` | 실온 한 점 | ❌ |
| **3단계-b** `C` 상한 | `[재현]` 이상 RC: LTFS 139 Ω cm² · 35 mHz → **≈33 mF cm⁻²** · 볼밀 NMC 1750 · 12 Hz → **≈7.6 µF cm⁻²** · argyrodite NMC `[도표]` ≈10–15 · 54 mHz → **≈0.2–0.3 F cm⁻²**(기하 면적당) | ✅ **느린 두 "전하이동" 호가 이중층 자릿수를 넘는다**(거칠기 ≳10³ · ≳10⁴ 필요 — 전극 질량 미인쇄라 범위만) · 볼밀 NMC 는 통과 — **여섯 번째 실패 계열**, 확산 · 화학 용량 대역과 겹친 호 |
| **4단계** 시간 영역 | Li 금속 CE: `[도표]` 가지 ↔ 휴지 끝 과전압 0.06–0.15 V at 27 µA cm⁻² → DC ≈2–6 kΩ cm² ↔ EIS 폭 ≈0.5–1.2 kΩ cm² | ✅ 부분(음극 판) — ×≈2–10 이 1 mHz 밖 또는 전류 중 상태(46호와 같은 방향) |

### ★★ 곱이 선 자리 — 소거법 배정

`[인쇄]` "Since the ion conductivity of β-LPS in the cathode composite is not expected to be dependent on the state of charge, variations in resistance of this loop can be attributed to the charge transfer to the active material, RCT." — 호의 정체는 **다른 후보(복합체 이온 전도)를 기대로 소거**해 정했고, `R_CT` 최대값의 사이클 증가(→ 1500 Ω cm², 5 사이클)의 원인은 충방 비대칭 → 음이온 산화환원 경로(`k` 쪽)로 읽었다. `R_CT ∝ 1/(A_eff·k)` 의 `A_eff` 쪽(LTFS 부피 변화에 따른 접촉 변화)은 검사되지 않았다. 같은 지면의 반대 방향 가설 — 손 분쇄 용량의 초기 증가를 `[인쇄]` "could slightly improve the double percolation"(접근 분율 증가) — 도 측정 0.

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 "호 제거 검정 + 2전극 합 재구성"**(위 표). 곱을 가르기 전 단계 — **그 호의 값이 입력으로 쓸 만한가**(제거 검정)와 **그 호가 어느 전극의 것인가**(합 재구성 적합). 45호 줄(합 일치는 분배를 검증하지 않는다)의 반대편: 같은 합을 **검증이 아니라 비식별성 시연**에 썼다 — 범주가 맞는 사용.
2. **3-b 실패의 여섯 번째 표본이 양극 복합체에서 나온다** — 느린 호(수십 mHz)가 확산 대역과 겹치면 "전하이동" 이름표가 화학 용량을 입는다. 3-b 를 적용할 때 꼭짓점 주파수가 Warburg 대역과 몇 decade 떨어졌는지 같이 적는다.

### ⚠ 이것이 곱을 푼 것은 아니다

`C` 미인쇄 · 전극 질량 미인쇄 · 셀 산포 0 · 최대 5 사이클. 3-b 는 이상 RC · 그림 판독 R(argyrodite) 위이고, 4단계는 휴지 EIS ↔ 전류 중 DC 의 대조다. 기여는 **곱 앞 단계(값의 쓸모 · 전극 귀속)의 두 검정**이다.

## ★★ 처방의 서른두 번째 적용 (2026-09-23, `assb` 49호 — ⚠ **액체셀**, 도구 칸) — **4단계의 원전형: 총량은 시간 ↔ 주파수로 한 곡선에 모이고, 성분 이름은 창 경계의 규약이다 — 적합된 직렬 R 은 대역 위쪽 끝의 \|Z\| 다**

`raw/papers/barai2018_measurement-timescale-internal-resistance-methods.md` (Barai … Jennings 2018, *Sci. Rep.* 8, 21 — 20호 ref [24]). 상용 20 Ah LFP/흑연 파우치 · 50 % SoC · 25 °C · DC 펄스(1–15 C) · 1 kHz · EIS(10 mHz–100 kHz) · 펄스-다중사인 2차 ECM. 카드의 곱(`A_eff·ε_p/R_s`)은 대상이 없다 — 처방 **4단계 자체의 원전 표본**이다.

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C`(τ 형) | EIS 적합 0(Nyquist 판독만) · 다중사인 τ₁ · τ₂ 미인쇄 | ❌ |
| **2단계** 면적 대조군 | 셀 한 종 · 면적 축 0 | ❌ |
| **3단계-a** `Ea` | 25 °C 한 점 | ❌ |
| **3단계-b** `C` 상한 | DC `R_CT` 0.41 mΩ · τ ≲ 2 s ⇒ `[재현]` 셀 단위 `C` ≲ 5 × 10³ F — 면적 · 질량 · BET 미인쇄 | ⚠ 판정 불가 |
| **4단계** 시간 ↔ 주파수 | Fig. 7b — 5 C 펄스 6 점 · 1 kHz · 다중사인을 EIS \|Z\|(t = 1/f) 위에 | ✅ **총량 ±11 %** · 성분은 원문이 "not meaningful" · `[재현]` 규약 1/(2πf) 면 −13 … −23 %(분해능 ≈1 decade) · 진폭 의존(10 s 창 ×1.46) |

### ★★ 곱이 선 자리 — 곱은 없고, "창 끝 흡수" 가 있다

`[인쇄]` 다중사인 ECM 직렬 `R₀` 1.62 mΩ 은 "employs a maximum frequency of 1 Hz, and thus cannot be labelled as a pure Ohmic resistance" 이고 EIS \|Z\|(1 Hz) 1.62 와 같다. DC 0.1 s `R₀` 1.33 ≈ \|Z\|(10 Hz) 1.41(장비 10 Hz). `[해석]` **적합 · 판독된 직렬 저항 = 관측 대역 위쪽 끝의 임피던스** — 곱 축퇴와 다른 종류의 비식별이다: 곱은 두 인자가 한 조합으로만 보이는 것이고, 이것은 **대역보다 빠른 모든 과정이 한 파라미터로 합쳐지는 것**이다. 다중사인 "RCT" 1.10 은 두 RC 가 모두 1 Hz 보다 느리므로 EIS `R_CT` 대역(2–251 Hz)과 겹치지 않는 과정에 같은 이름이 붙었다.

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 "창 규약"**(위 표). 4단계 · 20호 시간 영역 번역 · 34호 온보드 번역은 모두 창에서 읽은 성분을 쓴다 — 그 값은 **창 경계 · 대역 끝 · 진폭**이 정한다. 1단계 τ · 3-b `C = τ/R` 의 τ 도 같은 창에서 나오므로 이 줄이 두 단계의 전제다.
2. **20호 번역의 사후 근거**: 20호 `R_CT` 창(≈0.8–1.2 h)은 원전 창(0.1–2 s)의 ×10³ 이고 원전 규약으로 ≈0.28 mHz — 원전이 "diffusion dominated" 라 부른 대역이다. 20호 3-b 의 10²–10³ 배 실패는 원전의 틀이 예측하는 방향이다. 그리고 20호 "접촉 저항" 은 순간 `R₀` 의 대역 끝(샘플 간격 미인쇄)이 정한다.

### ⚠ 이것이 곱을 푼 것은 아니다

액체 · 한 상태 · 열화 0 · 셀 수 미인쇄 · `C` 0. 기여는 **처방 단계들이 입력으로 쓰는 "창에서 읽은 성분" 의 보고 규약**이다.

## ★★★★ 처방의 서른세 번째 적용 (2026-09-23, `assb` 50호) — **16호 방법의 원본: `a_v = 3ε/r` "in contact to SE" 의 출생지 · 두께 가변은 `a_v` 와 `j₀` 를 가르지 않는다 · 같은 지면 비교는 R·C 를 견디고 편 간 비교(16호)는 면적 서명이다**

`raw/papers/miss2022_exchange-current-density-tlm-thickness-lco-nmc-assb.md` (Miß · Ramanayagam · Roling 2022, *ACS AMI* 14, 38246 — 16호 ref [30]). 단결정 LCO(LiNbO₃ ≈12 nm 구입) · 단결정 NMC 83\|6\|11(LiNbO₃ 1 wt% 졸–겔) \| 0.67 Li₃PS₄·0.33 LiI(σ 0.8 mS cm⁻¹) \| In, 70 : 30, 탄소 0, 389 MPa 제조 = 운전, 두께 4 점(LCO 32–219 · NMC 31–221 µm, 계산값), SOC50 · 2 사이클째 EIS, 음극은 In–Li 대칭셀(40 at% · 125 MPa)의 절반을 빼서 제거.

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | `j₀` · `Q_DL` · β 두 재료(Table 2), 같은 `a_v` 규약 | ✅ **완비** — `[재현]` Brug `C_eff` LCO 4.4 · NMC 2.0 µF cm⁻²(CAM 기하 면적당), τ_CT 4.4 × 10⁻⁵ ↔ 4.6 × 10⁻³ s ⇒ LCO ↔ NMC **τ ×106 — 면적 서명 아님**(면적 몫 ≤ `C` 비 ×2.2, `Q` 원값 ×10 / `1/R` ×235) · **16호(389 MPa) ↔ 이 편 NMC**: `1/R` ×12.1 · `Q` ×13.5 · `C_eff` ×15.4 ⇒ **τ ×1.28 — 면적 서명** |
| **2단계** 면적 대조군 | 두께 4 점 = 공칭 면적당 계면 면적 ∝ d 의 척도 대조 | ⚠ 척도 법칙만 — NMC 통과(`R_ion/(R_CT/a_v d)` 0.45 → 23 전이 통과) · LCO 는 네 두께 전부 두꺼운 극한(92 → 4,300), `[인쇄]` 모형 두께 추세 불일치 "unclear". θ 는 안 건드린다 |
| **3단계-a** `Ea` | 실온 한 점 | ❌ |
| **3단계-b** `C` 상한 | 위 `C_eff` | ✅ **통과** — 두 재료 모두 이중층 자릿수(≲10 µF cm⁻²) 안. 16호 389 MPa 는 30.7(기하 면적당 이미 ×3) ⚠ |
| **4단계** 시간 영역 | 0.1 C · 1/30 C 곡선뿐 | ❌ |

### ★★★★ 곱이 선 자리 — 이름이 붙은 출생지, 그리고 규약 재척도

`[인쇄]` "The active area of the CAM particles **in contact to SE** normalized by the cathode volume is given by `a_v = (3ε_CAM)/r_CAM`" · `R_CT = RT/(F j₀)` · 초록 "These contacts determine the Li⁺ exchange current density" — 16호 절의 "`θ ≡ 1` 을 이름 붙여 가정" 은 **이 편에서 태어나 16호로 옮겨졌다**. 저자의 틀에서 `j₀` 는 정의상 접촉을 품는다(압력이 `j₀` 를 바꾼다는 결론 문장). 두께 가변은 `R_ion ∝ d` 와 `R_CT/(a_v d) ∝ 1/d` 를 가르지만 **`a_v` 와 `j₀` 는 둘 다 d 무관**이라 가르지 못한다.
★ 그리고 `[인쇄]` 수정 (ii) — `a_v·τd → a_v·d`("for improving the agreement", 기하 논증) — 는 `[재현]` **`j₀` 를 정확히 ×τ(6.1 · 6.8) 옮기는 규약 선택**이다(식 (1)의 계면 항이 `Z_loc/(a_v ℓ)` 한 조합). 비교한 액체 문헌의 규약은 지면에 없다.

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 "면적 정규화 규약"**(위 표). 곱 축퇴가 "측정이 한 조합만 본다" 라면, 이 줄은 **"보고자가 조합을 어떻게 쪼갤지 정하는 규약이 모형 수정 한 줄에 숨어 있다"** — 편 간 `j₀` 비교의 전제.
2. **1단계를 편 사이로 건 첫 표본** — 같은 분말 · 같은 규약 · 같은 압력에서 R·C 가 면적 서명을 준다: 16호의 "`j₀` 는 SE 이온전도도와 함께 오른다(≈한 자릿수)" 는 **접촉 면적 ×12–15 와 구별되지 않는다**. 반대로 같은 지면 LCO ↔ NMC 는 R·C 를 견딘다 — **같은 곱에서 한 비교는 서고 다른 비교는 안 선다**.
3. **3-b 통과 표본**(양극 복합체 · CAM 기하 면적당 2–4 µF cm⁻²) — 25 · 23호에 이어 "전하이동" 이 크기 검사를 통과한 자리.

### ⚠ 이것이 곱을 푼 것은 아니다

θ 를 잰 관측은 0(FIB-SEM/EDX 단면은 반경 확인에만). 1단계 판정은 `C ∝ θ` 전제 · Brug 근사 위이고, 편 간 판정은 **SE 가 달라 전제가 약하다**. 규약 대수는 식에서 읽은 것이고 저자는 인쇄하지 않았다. n 미인쇄 · `j₀` 는 "simulation … compared"(목적함수 · ± 0).

## ★★ 처방의 서른네 번째 적용 (2026-09-23, `assb` 51호 — ⚠ **액체셀**, 도구 칸) — **제목의 "전하이동 ↔ 접촉 저항 분리" 는 직렬 두 호의 이름 짓기다: 주 판별자는 `Ea`, 실체는 `C` 세 자릿수, 그리고 전자 접촉 호의 `C` 는 여집합에 있다**

`raw/papers/illig2012_charge-transfer-contact-resistance-lfp-drt-ecm.md` (Illig … Ivers-Tiffée 2012, *JES* 159, A952 — 18호 [29] · 11호 [9] · 47호 [35]). LFP : 카본블랙 : PVDF 70 : 24 : 6 \| 1 M LiPF₆ EC:EMC \| Li 금속 · 반쪽전지 + LFP\|LFP · Li\|Li 대칭셀 · EIS 10 mV 1 MHz–10 mHz(평가 100 kHz–10 mHz) · 0–30 °C × SOC 100–10 % · 캘린더링 한 쌍. "접촉" = **양극층 \| Al 집전체** — 카드의 곱(`A_eff·ε_p/R_s`, CAM\|SE `θ`)은 대상이 없다.

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | `C` · `Q` · `n` 미인쇄, 식 (9) `τ = R·C` 한 줄 · `[재현]` Table I → P2C ≈0.9–1.2 µF · P1C ≈2.8–3.5 mF cm⁻² · `[도표]` 캘린더링 봉우리 이동 | ⚠ **부분** — 두 호 분리는 `C` ×≈3,000 로 강하다(저자 미사용). 캘린더링: 두 호 모두 τ 이동 → 같은 계면 전제로는 면적 서명 아님 · **여집합 전제(P2C)로는 접촉 증가와 양립** |
| **2단계** 면적 대조군 | 캘린더링 한 쌍 — 두께 20 → 10 µm · 공극률 64.7 → 41.5 % · 두 면적(도식만) · 음극도 변함 · `[재현]` 고체량 ×0.83 | ⚠ 단일 원인 조작 아님 · 크기 0 |
| **3단계-a** `Ea` | 다섯 과정 · 5 온도 · 한 셀 | ✅ **이 편의 주 판별자**(0.45 ↔ 0.06 eV) — 이름은 "always temperature activated" 가정. ⚠ 판별값이 ASSB 에서 안 선다(18호 R2 ↔ R3 겹침) |
| **3단계-b** `C` 상한 | 위 `[재현]` | ✅ 둘 다 통과 — P1C 는 카본블랙 24 wt% 의 이중층 몫이 커 `C ∝ LFP 면적` 전제가 약하다 |
| **4단계** 시간 영역 | 없음 | ❌ |

### ★★ 곱이 선 자리 — 곱은 없고, 1단계 전제의 부호가 있다

P1C 한 호 안의 `A·j₀` 는 가르지 않았다 — 저자는 캘린더링 증가를 **면적**("electrolyte accessible surface area … should change the charge transfer resistance")에, SOC 증가를 **`j₀`**("charge transfer is facilitated when few lithium-ions are present in the host lattice")에 돌렸다: 같은 곱의 두 변화를 **다른 인자에 배정**했을 뿐이다. `[도표]` 캘린더링 P1C τ ×≈3.5 는 순수 면적(τ 보존)과 맞지 않는다.
P2C 쪽은 `[해석]` Fig. 15 도식이 CPE 를 **비접촉(전해질 접면) 집전체**에, 저항을 접촉(빨강)에 그렸다 — 그 배치면 `C ∝ (A_geo − A_c)` 이고 "C ∝ 접촉 면적" 전제의 **반대**다. 관측(τ ×≈1/6)은 이 배치와 방향이 맞는다.

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 "`C` 의 자리 · `Ea` 판별값은 계 고유"**(위 표). ASSB 에서도 집전체 \| 복합체 · CAM \| 탄소 같은 **전자 접촉 호**가 있고(18호 R2), 그 호에 CAM\|SE 용 1단계 규칙을 그대로 걸면 부호가 틀린다.
2. **곱 앞 단계(분배)의 채널 목록**: 대역 + 대칭셀 + `Ea` + SOC + 단일 원인 조작 — 45호(합 일치는 분배를 검증하지 않는다) · 48호(호 제거 검정) 줄의 앞. 이 편은 **넷째 과정을 빼서 적합을 안정시켰고 그 몫이 P2C 로 간다**고 스스로 인쇄했다 — 48호 제거 검정의 반대 방향(빼도 되는가를 묻지 않고 뺐다).
3. **대역은 정체가 아니다** — 원전 안에서 P2C 주파수가 캘린더링 ×≈6 · 반쪽 ↔ 대칭셀 ×≈2–3 움직인다. 11호가 "slightly above 10³ Hz" 로 옮긴 것은 이 셀의 R·C 다.

### ⚠ 이것이 곱을 푼 것은 아니다

액체 · 전자 접촉 · 셀 1 · 캘린더링 1 쌍. `C` 는 이상 RC 재현(`n` 미인쇄 · 표 순서 뒤집음), 캘린더링 τ 는 봉우리 위치 판독, 여집합 `C` 는 도식 판독(문장 0). 기여는 **1단계 전제의 적용 범위**와 **3-a 판별값의 이식 조건**이다.

## ★★ 처방의 서른다섯 번째 적용 (2026-09-23, `assb` 52호) — **적용 불가(양극 채널 0) · 대신 곱 앞 단계의 구멍: 2전극 용량 손실을 나눌 때 `LLI` 칸에 넣는 쿨롱 효율이 Li 재고를 넘는 결손을 낸다**

`raw/papers/oh2025_mgsigr-overcharge-low-np-ratio-low-pressure-assb.md` (Oh … Choi 2025, *Adv. Energy Mater.* 15, 2404817 — 13호 [34] · 14호 [10], 14호와 같은 연구실). LiNbO₃-NCM811 : LPSCl : VGCF 68 : 30 : 2 \| LPSCl \| MgSiGr(Mg 200 nm 위 SiGr 0.8 mg cm⁻², 과충전 Li 도금) · 펠릿 20 MPa(N/P 0.15 · 양극 20 mg cm⁻²) · 3 MPa(N/P 0.66 · 6 mg cm⁻²) · 파우치 3 MPa(N/P 0.6) · 25 °C · 2전극만.

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | 반쪽전지(음극) `R_B` · `R_CT` 두 값 · `C` 미인쇄 · 양극 0 | ❌ |
| **2단계** 면적 대조군 | 음극 교체(SiGr ↔ MgSiGr ↔ Li 10 µm) — 음극 쪽 | ❌(양극 곱 대상 아님) |
| **3단계-a** `Ea` | 25 °C 한 온도 | ❌ |
| **3단계-b** `C` 상한 | 없음 | ❌ |
| **4단계** 시간 영역 | 없음 | ❌ |

### ★★ 곱이 선 자리 — 곱 앞에서 `LLI` 칸이 잘못 채워진다

N/P < 1 과충전 셀의 충전은 대부분 **음극이 Li 금속(평탄)인 구간**이라 2전극 곡선은 사실상 양극 반쪽 곡선이다(`[도표]` 반쪽 도금 −15 … −22 mV vs Li). 그러면 `LLI` 는 곡선 모양이 아니라 **끝점**으로만 나타나고, 끝을 누가 내는지가 정해지지 않으면 `LLI` 와 `LAM_PE`(와 `θ`)는 같은 "용량 축 절단" 이다. 이때 흔한 처리는 CE 결손을 `LLI` 로 고정하고 나머지를 양극에 배정하는 것인데, 이 지면에서는 `[재현]` 3 MPa 누적 결손 ≈575 mAh g⁻¹ 가 NCM811 이론 Li 재고 ≈275 의 ≈2 배다 — **`LLI` 칸이 물리적으로 불가능한 크기로 채워진다.** 20 MPa 도 결손 ≈95 ↔ 관측 손실 ≈27.

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 "누적 충–방 결손 ↔ Li 재고 상한"**(위 표). 곱을 가르는 1–4단계의 **앞**에 둔다 — 45호(합 일치는 분배를 검증하지 않는다) · 48호(호 제거 검정)가 임피던스 쪽 분배 단계라면 이것은 **용량 쪽 분배 단계**다.
2. **조건 간 CE 는 면적당으로** — 52호 두 압력은 CE 로 ×≈7, 면적당 ×≈1.8(양극 적재 20 ↔ 6 mg cm⁻²). 압력 · 적재가 같이 바뀐 비교에서 CE 차를 압력 효과로 읽지 않는다.
3. **끝 전극 모드가 CE 의 뜻을 정한다** — 양극이 방전 끝을 내면 음극 저장소가 Li 손실을 흡수해 CE ≈1 이 된다(`LLI` 비가시), 음극이 끝을 내면 `LLI` 가 곧 용량이다. 41호의 요구("어느 전극이 끝을 내는가")가 CE 해석의 전제이기도 하다.

### ⚠ 이것이 곱을 푼 것은 아니다

양극 채널 0 · 셀 1 · CE · 용량은 화소 판독(±1 %p · ±2 mAh g⁻¹). 결손의 정체(연성 단락 누설 · 부반응 · SE 분해 보충)는 지면으로 못 가른다 — 주장은 "CE 결손 ≠ `LLI`" 까지다.

## ★★ 처방의 서른여섯 번째 적용 (2026-09-23, `assb` 53호 — ⚠ **Perspective**, 1차 기여는 P2D 사례 계산 하나) — **적용 불가(`C` 0 · 온도 하나) · 대신 모델 식이 곱의 세 번째 자리를 보인다: 면적 `a` 는 BV 칸(`a·i₀₀`)과 직렬 옴 칸(`a/R_SP`)의 공통 분모이고, 두 칸은 전류 진폭으로만 갈린다**

`raw/papers/ren2023_oxide-ssb-composite-cathode-architecture-perspective.md` (Ren · Danner … Latz … Janek … Fattakhova-Rohlfing 2023, *Adv. Energy Mater.* 13, 2201939 — 02호 ref 17). NMC811/LLZO 75 vol% 공소결 복합양극 50 · 100 µm \| LLZO 10 µm \| Li · 1 · 10 mA cm⁻² · 실온 · 문헌 파라미터(`R_CT` · `R_SP` 2600 / 150 · 0 Ω cm² ← Kato 2014 LCO/LLZO).

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | `R_CT` · `R_SP` 문헌값, `C` 0 | ❌ |
| **2단계** 면적 대조군 | `d50` 10 → 0.1 µm — `a` 미정의(구 기하면 면적 ×100 + 확산 길이 ×1/100 한 손잡이) | ❌(교락) |
| **3단계-a** `Ea` | 실온 하나 | ❌ |
| **3단계-b** `C` 상한 | 없음 | ❌ |
| **4단계** 시간 영역 | 없음 | ❌ |

### ★★ 곱이 선 자리 — 세 번째 곱 `a/R_SP`

SI Table 1 `[인쇄]`: `i_se = 2·i₀₀·√c_S·sinh(Fη/2RT)` · `η = Φ_S − Φ_E − U₀ − i_se·R_SP` · `i₀₀ = (1/R_CT)(RT/F)c_max^−0.5` · 전하 보존 `a·i_se`. ⇒ 전극 수준에서 `a·i₀₀`(37호 `A_eff ↔ k` 항등)와 **`a/R_SP`** 두 조합만 보인다. `ε_CAM` 은 75 vol% 고정 · 열화 무시 — 37호 ① `ε_p` 동어반복 자리는 이 모델에 없다. 서술은 "active surface area"([32] — 면적 자리)와 "isolation of particles"([122] — 고립 자리)를 섞어 쓴다.

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 "전류 진폭 — 직렬 `R_SP` ↔ `R_CT`"**(위 표). 저자가 선형 ↔ 로그를 인쇄하고 "Deconvolution … is challenging" 으로 가정에 넘긴 바로 그 분할이다.
2. **입경 손잡이 = 곱** — 50호 면적 규약(`3ε/r`)을 쓰는 모델의 `d50` 민감도("CAM Li Diffusion Length")는 확산과 면적의 곱이다.
3. `[재현]` **체제 의존 가시성** — state-of-the-art(옴 지배)에서는 `a` 변화가 크게 보이고, improved(`R_SP` 0 · 작은 입자)에서는 안 보인다. 합성 truth 를 만들 때 계면 체제가 면적형 접촉 손실의 가시성을 미리 정한다.

### ⚠ 이것이 곱을 푼 것은 아니다

식에서 읽은 구조 + `a` 구 기하 가정 위의 우리 계산. 저자는 진폭 채널을 쓰지 않았고, 모델에 열화가 없다.

## ★★ 처방의 서른일곱 번째 적용 (2026-09-23, `assb` 54호 — ⚠ **양극 없음**, SE 자체 수송 모델 + 재사용 자료) — **수송 곱 `σ⁰·ε/τ²` 은 구조 계산으로 떼어지고, 남은 직렬 합(벌크 ↔ 입계)은 가르는 채널이 측정 대역 밖이다 · `C` 는 호 위치 맞춤값이라 두께를 말하지 않는다**

`raw/papers/neumann2021_garnet-3d-structure-grain-boundary-transport.md` (Neumann · Hamann · Danner · Hein · Becker-Steinberger · Wachsman · Latz 2021, *ACS Appl. Energy Mater.* 4, 4786 — 02호 ref 38 · 27호 ref 14 · 53호 [27]). LLCZNO 다공층 56 · 42 · 25 % FIB-SEM 재구성 + 워터셰드 입자 분할 + BEST(입계 BV `i₀₀^GB` + 공간전하층 `C_DL^GB`) · 차단 Au EIS 모의 · 300 K.

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | 입계 `R` ≈3.74 Ω cm²/계면(`[재현]` `RT/F·i₀₀^GB`) · `C_DL^GB` 9.75e-9 F cm⁻² — 둘 다 재사용 치밀 펠릿 한 스펙트럼에 손 보정 | ❌ `C` 가 두께를 정하지 않는다(`[재현]` 등가 ≈6.8 µm) |
| **2단계** 면적 대조군 | 공극률 세 시편 — `τ` · `A_Spec,SE` · `A_Spec,GB` 를 **구조로 계산** | ⚠ 부분 — 입도(3.1 ↔ 4.6 µm) · 2차상이 같이 움직인다 |
| **3단계-a** `Ea` | 300 K 하나 | ❌ |
| **3단계-b** `C` 상한 | — | 해당 없음 |
| **4단계** 시간 영역 / 진폭 | 모델 ASR 시나리오 1: 0.1 → 10 mA cm⁻² 에서 1064 → 655 Ω cm²(입계 sinh) — 실험은 소신호 EIS 뿐 | ❌(데이터) · 모델에만 |

### ★★ 곱이 선 자리 — 곱은 풀리고 합과 곱 하나가 남는다

`[재현]` 구조-만 전도도 ÷ `σ⁰` ≈ `ε/τ_x²`(56 % 0.139 ↔ 0.139) — 굴곡도는 복셀 위에서 풀려 파라미터 벡터 밖에 있다. 남는 것: (i) 직렬 합 `R_bulk(σ⁰) + R_GB` — `[인쇄]` "exact deconvolution … unfeasible"(본문 · SI), Fig. 6(`σ_bulk` 스윕) ↔ Fig. S5(`i₀₀^GB` 스윕)가 **같은 저주파 끝**에 닿고 다른 것은 대역 밖 고주파 절편뿐; (ii) 입계 호 ∝ `L·τ/(d·i₀₀^GB)` 인데 교정 시편의 `d` 는 **가정**(GeoDict 다면체 15 ± 6 µm) ⇒ `d_dense·i₀₀^GB` 한 조합(`[해석]`).

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 "벌크 특성 주파수 ↔ 측정 대역 상한"**(위 표).
2. **구조 계산은 곱을 가른다 — 카드 곱에서의 대응은 영상 면적(39호)** · 그러나 구조 계산이 가를 수 있는 것은 **기하 인자**뿐이고, 같은 경로 위 직렬 저항의 합은 여전히 전기 채널(주파수 · 온도 · 진폭)이 필요하다.
3. **`C` 의 두 번째 경고**(51호 "여집합" 에 이어) — 교정 `C` 가 물리 두께와 10² 배 이상 어긋나면 그 `C` 는 호를 원하는 대역에 두려는 **위치 맞춤값**이고, 1단계 면적 서명으로 쓰지 않는다.
4. **진폭 줄의 SE 판** — 53호 "직렬 `R_SP` ↔ `R_CT`" 와 같은 구조가 SE 안(벌크 옴 ↔ 입계 sinh)에 있고, 이 편 모델 표가 그 차를 보였다.

### ⚠ 이것이 곱을 푼 것은 아니다

구조 계산이 뗀 것은 기하 인자 하나이고 벌크 ↔ 입계는 원문이 비식별을 인쇄했다. 등가 두께 · ASR 해석 · `d·i₀₀` 조합은 인쇄값 · 그림 판독 위의 우리 계산이다. 이 편은 양극이 없다 — 카드의 `A_eff·ε_p` 곱에 대한 직접 근거가 아니다.

## ★★ 처방의 서른여덟 번째 적용 (2026-09-23, `assb` 55호 — 수송 곱 · 신품) — **구조 계산은 그 구조의 시편에서만 곱을 푼다: 두 경로를 `τ` 로 비교하면 각자 고른 `ε` 가 일치를 만든다 · 디지털 치환은 2단계 대조군의 계산판이다**

`raw/papers/hlushkou2018_void-space-ion-transport-composite-cathode.md` (Hlushkou · Reising · Kaiser · Spannenberger · Schlabach · Kato · Roling · Tallarek 2018, *J. Power Sources* 396, 363 — 01호 ref 16). LCO(LiNbO₃)/비정질 LPSI, 탄소 없음 · 대칭셀 EIS 1(Li₀.₇₁CoO₂) + 별도 수지 함침 시편 FIB-SEM(35.6 nm × 100 nm) + 추적자 확산 모의 + 가상 void → SE 치환.

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | EIS 1 장 — `R_ion` 97 ± 2 Ω 만 인쇄, Warburg-short `α` · `β` · 계면 호 미인쇄 | ❌ `C` 0 |
| **2단계** 면적 대조군 | **디지털 치환 — 같은 재구성에서 void 만 SE 로, LCO 고정** | ⚠ 부분 — 수송만(계산), 접촉 면적 0 |
| **3단계-a** `Ea` | SE 펠릿만 −120 → 160 °C(`Ea` 미인쇄) · 복합체 온도 0 | ❌ |
| **3단계-b** `C` 상한 | — | 해당 없음 |
| **4단계** 두 영역 / 두 경로 | EIS ↔ 구조 모의 — 시편 넷이 다르다(수지 · 충전 상태 · 압착 · 두께) | ❌ 24호 시편 조건 위반 |

### ★★ 곱이 선 자리 — 경로 안에서는 풀리고, 경로 사이에서는 선다

경로 B(영상 `ε` + 모의 `τ`)는 FIB 시편의 `ε/τ` 를 각각 준다 ✅. 경로 A 는 `σ_eff/σ⁰` 하나이고(`[재현]` 0.406 ± 0.013) 그 시편의 `ε` 는 재지도 인쇄하지도 않았다. 원문은 `τ` 1.6 ↔ 1.74 를 "close" 로 읽었고, `[재현]` 1.6 은 `ε` ≈0.65 를 전제한다. 곱으로는 ×1.31 — 측정은 "void 13 % + Bruggeman"(0.394)과 "void 적음 + 구조 `τ`" 둘 다와 양립한다.

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 "두 경로 대조는 관측 곱으로, 같은 시편 · 같은 `ε` 로"**(위 표). 54호 "구조가 곱을 푼다" 의 조건문 — **같은 시편**.
2. **디지털 치환(재구성 위 한 상 바꾸기)은 2단계 면적 대조군의 계산판이다** — 실험으로는 한 상만 바꾼 쌍을 만들 수 없는데 재구성에서는 된다. 이 편은 수송에만 썼다(`[재현]` void 경로 효과 `ε/τ` ×0.59, 로그 몫 `τ` 59 %). `[해석]` 같은 치환에 **CAM 표면 분할(CAM–SE ↔ CAM–void)** 을 붙이면 void 의 접촉 효과(`φ`)와 경로 효과를 한 구조에서 가를 수 있다 — 카드 곱의 `A_eff` 쪽 입력.
3. **영상 상 이름 검사** — "void" 상에 안정화 수지가 섞였다(분리 0). 곱의 인자로 쓰기 전에 상의 내용물을 확인한다(39호 AB 분류와 같은 부류).

### ⚠ 이것이 곱을 푼 것은 아니다

경로 B 가 푼 것은 FIB 시편의 수송 곱이고, EIS 시편의 곱 · 카드의 동역학 곱(`A_eff·ε_p`)은 건드리지 않았다. `ε` ≈0.65 · ×1.31 · 로그 몫은 인쇄값과 관 내경 가정 위의 우리 계산이다. 신품 한 상태라 `LAM_PE` 가 없다.

## ★★ 처방의 서른아홉 번째 적용 (2026-09-23, `assb` 56호 — FEM 모델 · 새 측정 0) — **void 를 접촉 자리에만 넣은 3D 모델: 피복은 저율에 안 보이고, 같은 피복률에서도 분포가 과전압을 바꾼다 · `j₀` 는 면적 규약 없이 입력됐다**

`raw/papers/bielefeld2022_voids-kinetics-morphology-composite-cathode-fem.md` (Bielefeld · Weber · Rueß · Glavas · Janek 2022, *J. Electrochem. Soc.* 169, 020539 — 01호 저자들의 후속). NCM811/Li₆PS₅Cl, COMSOL FEM — 입자형 재구성(검증) · 1-입자-void(void 연구) · 원뿔(구조화). 입력은 Rueß 2020(GITT · EIS) · Conforto 2021(38호, PSD).

### 입력 점검

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | 모의 EIS 0 · `C_dl` 0 · `R_CT`(Rueß)는 식 (12) `R_CT = RT/(zFAj₀)` 로 `j₀` 가 되어 들어간다 — `A` 미정의 | ❌ |
| **2단계** 면적 대조군 | **모델 안 둘**: 피복률 스윕(Fig. 8, 100 → ≈52 %) · `φ` 고정 분포 스윕(Fig. 9) | ⚠ 모델판 — 실측 0 |
| **3단계-a** `Ea` | `T` 한 점(`[인쇄]` 273.15 K) | ❌ |
| **3단계-b** `C` 상한 | — | 해당 없음 |
| **4단계** 두 영역 | 없음 | ❌ |
| 율 스윕 줄 | 모의 4 율 — `[도표]` 0.02 C 피복 손실 48 % 에 ≤ ≈7 mV · 용량 −3 % ↔ 0.5 C −25 % | ✅ 모델판 — **저율이 `φ` 를 지운다** |
| `A_eff ↔ k` 줄(37호) | `[재현]` BV 면적 몫 ≈44 % · 나머지는 분포 · 확산 | ⚠ 해상 모델에서 부분 파괴 |
| 면적 정규화 규약 줄(50호) | 50호가 대조한 "10⁻⁵ A cm⁻²" 는 이 편의 **입력**(Rueß EIS) | ⚠ 한쪽 규약 없음 — `[재현]` 차 ≈×13.6 |

### ★★ 곱이 선 자리 — 입력 단계에서 한 규약으로 고정되고, 면적은 실험 일치로 골라졌다

모델의 BV 식은 모델 CAM/SE 면적 × `j₀` 를 본다. `j₀` 는 외부(Rueß `R_CT`)에서 `A` 미상으로 환산해 고정했고, 면적은 PSD 로 정해지는데 **PSD 는 세 절단 중 실험에 맞는 것(S, 0.17 m² g⁻¹)을 골랐다** — `[인쇄]` "none of the simulation input has been fitted" 와 공존한다. 곱은 풀린 것이 아니라 **`j₀` 를 고정하고 면적을 고른** 것이다(31호 "상수 입력" + 이산 선택). 그리고 이 편 Fig. 7 은 입력 가족 둘(SOC 의존 곡선 ↔ 상수 `{D̃₂, j₀,₁}`)이 비슷한 곡선을 주는 것을 보여 준다 — 저자는 "Achilles heel" 로 경고하고 물리적 정당성으로 골랐다.

### ⇒ 이 적용이 처방에 더하는 것

1. **새 줄 "`φ` 고정 분포 스윕 — 3D 모델에서 `A_eff ↔ k` 항등의 파괴 검사"**(위 표). 37호가 식에서 보인 항등(`A_eff → cA_eff, k → k/c` 가 모든 출력에서 같다)은 **균일 표면 전류 가정의 산물**이다. 피복을 공간적으로 해상하면 입자 내부 확산이 불균일해져 곡선에 분포의 서명이 남는다 — 56호에서 그 몫이 `[재현]` 과전압의 절반을 넘는다. `[해석]` 이 서명은 **`D̃` 가 느릴수록 크다**(빠르면 내부 확산이 불균일을 메운다) — 곱을 가를 신호가 확산 계수와 교락한다는 뜻이기도 하다.
2. **"비적합" 선언의 층위 검사** — 이산 선택(PSD 절단 · 입력 세트 · 수작업 연결)을 실험 일치로 했으면 곱의 한 인자가 맞춰진 것이다.
3. **검증 모델의 공극 처리 검사** — 56호 입자형 모델은 실험 void 14 % 를 SE 로 채웠다. 곡선 일치가 그 차(경로 · 접촉 둘 다)를 흡수했다 — 원뿔(void · 굴곡도 없음)이 0.5 C 에서 입자형보다 실험에 더 가깝다(`[도표]` ≈114 · ≈104 ↔ ≈115).

### ⚠ 이것이 곱을 푼 것은 아니다

전부 모델 명제다. 실측 `R·C` · `Ea` · 면적 대조군 0, 신품 · 첫 충전, `LAM_PE` 없음. `[재현]` BV 몫은 C-율 정의 · 국소 `j₀` · 대칭 BV 가정 위의 어림이다. `j₀` 균일 축소 대조(같은 모델)는 원문이 하지 않았다.

## 이 페이지가 주장하지 않는 것

- ★ **2026-09-22 (18호)**: **`C` 비 분해를 측정값으로 쓰지 않는다.** 로그 막대 판독 ·
  노화 후 `p` 미공개 · `C ∝ θ` 가정(검사 A 가 흔든다) · 조건당 셀 1 개 위에 있다.
  주장은 **"같은 지면의 두 열을 곱하면 저자가 남긴 'or' 가 갈린다"** 와
  **"그 전제를 먼저 검증해야 한다"** 까지다.
- **원전의 결론(양극 활물질 손실이 지배적)이 틀렸다고 주장하지 않는다.**
  주장하는 것은 **그 절차가 그것을 가려낸 절차가 아니라는 것**이다.
- **`A^p_eff = 0.4938` 이 틀렸다고 주장하지 않는다.** 단독으로 해석될 수 없다고
  주장한다.
- **축퇴를 수치로 재지 않았다.** 위 관계는 **인쇄된 식에서 손으로 읽은 구조**이고,
  근최적 집합의 **폭**은 아직 재지 않았다 ([[near-optimal-set-width-measurement]]).
- ★ **2026-09-22 (19호)**: **`C` 와 `Ea` 의 70 배 충돌을 "면적이 안 변했다" 로 옮기지
  않는다.** 19호의 세 계면은 **물리적으로 다른 계면**이라 "면적만 다르다" 가 애초에
  성립할 이유가 없다 — 18호 검사 B(**동일 계면의 두 상태**)와 성질이 다르다.
  주장하는 것은 **두 진단 채널이 같은 표에서 양립하지 않는다**는 것까지다.
  그리고 **`Ea` 채널을 충분조건으로 쓰지 않는다** — `A` 에 면적 외 항이 있고,
  19호의 `Ea` 불변 근거 자체가 **2 점 · n=1 · 범위 1.5 배**다.
- **이 관계가 다른 ASSB 모델에도 있다고 주장하지 않는다.** 근거는 **4 편**이다
  (`evidenceScope: multi-source-primary` — 9호 P2D + 16호 TLM/EIS + **18호 ECM/EIS + 열화**
  + **19호 ECM/EIS + SE\|SE 계면**). ⚠ **19호에는 활물질이 없어 `A_eff·ε_p/R_s` 자체가
  없다** — 기여하는 것은 **처방의 전제 검사와 대체 채널**이지 곱의 존재가 아니다.
  다만 `a_s = 3ε/R` 과 `j = i/(a_s·A·L)` 은
  P2D 계열의 표준형이라 **같은 구조가 널리 반복될 가능성이 높다** — 확인 안 됨.
- ★ **2026-09-22 추가**: 위 §"EIS 는 대가를 받는다" 는 **10호가 이 곱 축퇴를
  확인했다는 뜻이 아니다.** 10호는 `A_eff`·`ε_p`·`R_s` 를 언급조차 하지 않는다.
  주장하는 것은 **"주파수 영역에 별개의 축퇴가 하나 더 있고, 그것이 이 페이지의
  처방 중 한 줄을 약화시킨다"** 는 것뿐이다. 두 축퇴는 **독립이다.**
- ★ **2026-09-22 (20호)**: **`C ≈ 1 F cm⁻²` 를 측정값으로 쓰지 않는다.** τ 는
  **그림에서 읽은 합류 시간**이고 합류는 3–5 τ 라 τ 자체에 3–5 배 불확실이 있다.
  주장은 **"자릿수가 이중층과 맞지 않는다"** 까지이고, 그 결론은 τ 를 5배 줄여도
  바뀌지 않는다. 그리고 **`R_ct` 가 무엇인지 우리가 안다고 주장하지 않는다** —
  **전하이동이 아니라는 것**까지다.
- ★ **2026-09-22 (20호)**: **"접촉 저항 362 Ω 이 틀렸다" 고 주장하지 않는다.**
  복합전극 내부 저항 추정은 **ε·τ 를 우리가 가정**한 것이고, 원전은 복합체
  조성을 인쇄하지 않았다(ref [12] 에 있다). 주장은 **잔차가 유일 해석을 갖지
  않는다**는 것까지다.
- ★ **2026-09-23 (21호)**: **τ 형 1단계의 "≳1.4" 를 측정값으로 쓰지 않는다** — WE 꼭짓점 하한 ≈5 Hz 는 **이상 RC
  가정 + 그림 판독(1 Hz 에서 Im ≈ 0)** 이다. 주장은 **"면적 가설이 예측하는 0.28 과 방향이 반대다"** 까지다.
  그리고 **3단계-b 의 21호 판정이 기준값에 걸린다**는 것을 숨기지 않는다 — 20호 절 표의 "≈10⁻² F cm⁻²" 는 이 절에서
  정리했고, **고치지 않고 남겨 둔다**(그 절의 결론은 어느 기준으로도 같다).
- ★ **2026-09-23 (23호)**: **23호의 `C` 비를 측정값으로 쓰지 않는다** — 로그 축 판독 · CPE 환산식 미상 · 호가 위상 ≤4° 에서 겹친다. 주장은
  **"여섯 비교 중 다섯에서 `C` 가 `R` 을 따라가지 않는다"** 까지이고, **"접촉 손실이 용량에 없었다"** 가 아니다.
- ★ **2026-09-23 (24호)**: **σ_eff 비 0.93 / 0.34 를 측정값으로 쓰지 않는다** — COMSOL 쪽은 `ε` 14 % · `σ_bulk` 2e-3 가정 위의 모델 입력값이고 EIS 쪽은 다른 제조 압력의
  펠릿이다. 주장은 **"`τ²` 대신 `σ_eff` 로 비교하면 '두 조성 모두 증가' 가 '80 % 셀 하나의 ≈3 배' 로 줄어든다"** 까지다.
- ★ **2026-09-23 (25호)**: **2단계 통과를 "`R_ct` 차는 면적이다" 로 옮기지 않는다** — P4 τ 는 래스터 판독(×1.41), ECM ↔ DRT 의 `R` 비가 0.57 ↔ 0.84 로 다르고, BET 는 SE 분말 면적이다.
  주장은 **"면적 설명이 같은 지면의 독립 면적 측정과 방향·자릿수에서 양립한다"** 까지다. 그리고 **P1 벽돌층 반론은 모형 위의 추론**이다(P1 이 분리막 입계인지 미기재).
- ★ **2026-09-23 (26호)**: **박막 모델의 `D_M⊕·a_max` 대칭을 복합양극 P2D 로 옮기지 않는다** — 입자 차원이 없는 1차원 평판의 `x` 좌표 안의 구조다. 주장은 "같은 두 자리(동역학 면적 · 용량 스케일)에 조합이 선다" 까지다.
- ★ **2026-09-23 (27호)**: **`A` 의 세 겹 짐을 "접촉 손실은 원리적으로 못 가른다" 로 일반화하지 않는다** — 균질화 P2D 한 형식의 구조다. 연결 분율을 `A` 와 독립된 자리로 가진 축약 모델이 있을 수 있다(확인 안 됨).
- ★ **2026-09-23 (29호)**: **`φ` 를 측정된 피복률로 쓰지 않는다** — `D_true` 공통 · LIB 100 % 두 가정 위의 비이고, 기준(`D_LIB`) 자체가 형상에 따라 2.7 배 다르다. 그리고 **"`n` ≈0.5 는 고체 확산이 아니다" 라고 주장하지 않는다** — TLM √t 가 같은 지수를 줄 수 있다는 **대안**까지이고, 판별하지 않았다(CA 원자료 · TLM 파라미터 없음).
- ★ **2026-09-23 (30호)**: **"30호의 `D` 차는 면적이다" 라고 주장하지 않는다** — 유효 면적 ≈3.3 배는 **같은 `D` 가 가능하다**는 크기 검산이고, 측정이 아니다. Dunn 비의 4.3 배도 면적당 표면 용량을 계 사이에서 비교할 수 있다는 약한 전제 위다. 주장은 **"이 대조로는 `D` 와 면적이 안 갈린다"** 까지다. 그리고 `Q_M` ≈63 · `n` ≈2.5 는 **그림 판독 블록 평균에 우리가 건 적합**이지 원전 명제가 아니다.
- ★ **2026-09-23 (31호)**: **"ICI `R/k` 가 면적을 가른다" 고 주장하지 않는다** — 식에서 읽은 후보이고, 31호 지면에는 계산 재료(사이클별 `k`)가 없으며 `R` 에는 면적 무관 항이 섞인다. 그리고 **"`D_app` 은 LAM 에 불변" 은 식 19 위의 대수**(반무한 · 균질 모집단 · 액체 쪽 확산 무시)이지 원문 명제가 아니다.
- ★ **2026-09-23 (32호)**: **"BMS 센서만 있으면 곱이 갈린다" 고 주장하지 않는다** — 위 대응표는 32호가 요구한 센서 이름과 처방 단계의 입력을 **나란히 놓은 것**이다. 32호는 그 채널로 무엇도 가르지 않았고, 실셀 BMS 가 `C` 를 보고할 만큼 EIS 대역·정밀도를 갖는지는 확인되지 않았다.
- ★ **2026-09-23 (33호)**: **"상대극 ΔP 가 `A_eff(P)` 를 오염시킨다" 를 측정으로 주장하지 않는다** — 표의 ΔP 는 33호에 재수록된 네 원전의 그림 판독이고, 기저 20–45 MPa · 정변위 지그다. 주장은 **"재수록 원자료에서 상대극 ΔP 가 이 편 자신의 산업 운전 압력과 같은 자릿수다"** 까지다.
- ★ **2026-09-23 (34호)**: **"능동 펄스 BMS 가 곱을 가른다" 고 주장하지 않는다** — 한 펄스의 약분표는 단일 RC + 반무한 확산 근사 위의 **우리 대수**이고, 34호는 `C` · 시상수 · 조합을 쓰지 않았다. 실셀 단자 펄스는 양극 + 상대극(+ SE) 호의 합이고, `C ∝ A` 전제는 18·19호에서 깨졌다. "OED 가 구조적 곱을 못 푼다" 는 FIM 의 정의에서 나오는 일반 명제이지 34호가 인쇄한 것이 아니다.
- ★ **2026-09-23 (35호)**: **"용량 목표 특징 선택이 언제나 분리 채널을 버린다" 를 정리로 주장하지 않는다** — 근거는 35호 한 편에서 저항 채널 하나가 세 그룹 모두 탈락한 것과, 목표와 직교하는 정보는 목표 점수에 기여하지 않는다는 **일반 논리**다. 저항이 용량과 상관된 데이터(예: 같은 기구가 둘 다 움직이는 셀)에서는 선택될 수 있다. 그리고 35호는 액체 셀이라 접촉 손실 채널은 애초에 대상이 아니다.
- ★ **2026-09-23 (36호)**: **"평균장 VI 나 상관된 사전이 실제 모드 진단 문헌에서 곱을 가렸다" 고 주장하지 않는다** — 36호는 종설이고 두 문장 모두 재인용이다(평균장 경고는 BNN 가중치 맥락, Ruan 문장은 원전 미열람). 주장은 **두 경로가 구조상 곱 방향의 폭을 지울 수 있다**는 것까지이고, 확인은 원전(Ruan 2022 · Thelen 2022)에서 한다.
- ★ **2026-09-23 (37호)**: **"`A_eff` 는 원리적으로 `k` 와 못 가른다" 고 일반화하지 않는다** — 37호 · 9호의 식(균일 표면 전류 가정, `c_dl` 면적 무관)에서의 항등이다. 이중층을 면적에 비례시키거나 `A_eff` 를 확산에도 넣는 모델에서는 갈라질 수 있다. 그리고 **37호의 `k_p` · `R_s` 가 틀렸다고 단정하지 않는다** — `k_p` 는 LSV 환산 면적이 미인쇄라 측정과 "같은 양" 인지 모르고, `R_s` ↔ SEM 은 분말 투영 사진 한 장과의 대조다. 이완 시상수 불일치(4–5 자릿수)도 코드 없이 원인을 가르지 않는다.
- ★ **2026-09-23 (39호)**: **"`R_ct` 의 ×13 이 `k_p` 다" 라고 주장하지 않는다** — 후보는 셋(0.5 µm 아래 실접촉 · 계면 화학 `k_p` · 2전극의 상대극 In–Li 계면)이고 39호는 아무것도 가르지 않았다. 그리고 **`φ(P)` 추세 자체를 확정값으로 쓰지 않는다** — 같은 분할이 고정 혼합물의 부피비를 ×2 흔든다. 주장은 **"CT 로 잰 면적이 `R_ct` 변화의 작은 몫만 설명한다 — 그 분할을 믿는 한"** 까지다.
- ★ **2026-09-23 (40호)**: **R2 가 기준극 artifact 라고 주장하지 않는다** — `C₂` 가 표면 산화물 층 귀속과 두 자릿수 긴장한다는 것은 `ε_r` · `d` 가정 위이고, 꼭짓점 주파수는 인쇄된 "around" 다. **R3 세 값의 원인을 안다고 주장하지 않는다**(셀 · 시점 · 회로 중 무엇인지 지면이 말하지 않는다). 옴 몫 1 : 2.7 ↔ 1 : 3.2 는 LGPS 밀도 · 균질 분리막 가정 없이 질량비만 쓴 대조다.
- ★ **2026-09-23 (43호)**: **"`R_CT` 배증은 면적 손실이다" 도 "면적 손실이 아니다" 도 주장하지 않는다** — 1단계는 면적 서명, 3-a 는 반대, 3-b 는 1단계의 전제를 약화한다. 주장은 **"같은 호의 두 면적-불변 채널이 충돌하고, 1단계를 믿는 한 면적 손실이 용량 손실보다 크다"** 까지다. 그리고 **`(1−u)·φ` · `(1−u)(1−LAM)` 두 식은 우리 대수**이고 원전 명제가 아니다(원전은 두 채널을 대조하지 않았다). 흑연 0.6 mg 읽기는 4단계 일치(판독 한계 근처)로 고른 것이다.
- ★ **2026-09-23 (47호)**: **"리튬화한 쪽 Li 전극의 호가 작은 것은 거칠어짐이다" 도 "아니다" 도 주장하지 않는다** — τ 형 1단계는 면적 서명까지이고, 0.77 nm 는 균일 박리만 기각한다. 3-b 의 ×700–1000 은 0.1 Hz 에서 닫히지 않은 호의 `R` 하한 · 이상 RC 위다. 외부 기준 줄의 ×1.9 퍼짐은 Burns 쪽 값이 이 편에 재인쇄된 근사("∼30 · ∼60 · ∼150") 위다.
- ★ **2026-09-23 (48호)**: **"LTFS `R_CT` 증가는 `k` 쪽이다" 도 "접촉 손실이다" 도 주장하지 않는다** — 원문은 소거법으로 호를 고르고 비대칭으로 원인을 읽었을 뿐 곱을 가르지 않았다. 3-b 의 `C` 는 이상 RC · 기하 면적 · 그림 판독(argyrodite R) 위이고, 거칠기 범위는 전극 질량 미인쇄라 자릿수 판정까지다. **"2전극 호는 언제나 귀속 불가" 로 일반화하지 않는다** — 두 전극 호의 시상수가 겹친 이 셀 · 이 상태의 시연이다.
- ★ **2026-09-23 (46호)**: **"Li 금속 계면 저항 증가는 면적 손실이다" 도 "SEI 다" 도 주장하지 않는다** — 원전이 논증으로 배정했고 가르지 않았다는 것까지다. 4단계의 "≥2/3 가 0.1 Hz 아래" 는 **다른 셀 사이** 비교이고, 면적 ≈0.16 cm² 는 지면의 세 수를 맞추는 우리 추정이다. 역방향 짝은 후보 설계이고 이 편에서 판별에 성공하지 않았다.
- ★ **2026-09-23 (49호)**: **"적합된 직렬 R = 대역 위쪽 끝의 \|Z\|" 를 일반 정리로 주장하지 않는다** — 49호 한 셀에서 두 사례(다중사인 1 Hz · DC 10 Hz)가 맞은 것이고, 스펙트럼이 평탄(0.1–100 Hz 위상 ≤≈12°)해서 쉽게 맞는 조건이다. 가파른 호가 대역 끝에 걸린 셀에서는 적합 R 이 끝점 \|Z\| 와 다를 수 있다. 그리고 **t = 1/f 규약이 틀렸다고 하지 않는다** — 다른 규약이면 일치가 벌어진다는 그림 판독 위의 대조까지다.
- ★ **2026-09-23 (50호)**: **"16호의 SE 전도도 서사가 틀렸다" 고 주장하지 않는다** — 편 간 R·C 면적 서명은 **다른 SE 사이에서 면적당 이중층 용량이 같다는 약한 전제**와 Brug 근사 위의 우리 계산이다. 주장은 "그 비교가 곱을 가르지 않았다" 까지. 그리고 **수정 (ii)가 틀렸다고 하지 않는다** — 기하 논증은 합당하다. 주장은 "그 한 줄이 `j₀` 의 ×τ 를 정하고, 규약을 맞추지 않은 편 간 비교는 방향까지만 선다" 는 것이다. `dU/dc` 닻은 모형이 확산과 전하이동을 같은 `a_v` 로 통과시키는 **구조의 산물**이라 실접촉 θ 를 재는 채널이 아니다.
