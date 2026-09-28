---
title: "층상 NCM 격자 ↔ x(Li) 교정 — 구조 SOC 눈금의 축 규약 · 단조 채널 · 교정 간 이송"
description: "The lattice-parameter to Li-content calibration used to read x from diffraction is itself a charge-counted axis measured in a liquid reference cell — it assumes every particle is active, no parasitic charge and a first-cycle loss convention; c peaks near x≈0.45 for six NCM compositions so only a and V are monotone, Rietveld esd understates scatter 14–37x, and two same-group NCM622 calibrations differ by a near-constant ≈0.07 in x"
created: 2026-09-28
updated: 2026-09-28
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/debiasi2017_ncm-ni-content-operando-xrd-lattice-volume-energy-density.md, raw/papers/strauss2018_cathode-particle-size-inactive-fraction-assb.md, raw/papers/stavola2023_lithiation-gradients-tortuosity-thick-nmc111-argyrodite.md, raw/papers/koerver2017_capacity-fade-interphase-chemomechanical-ncm811-lps.md, raw/papers/zhang2017_in-situ-pressure-electrochemical-expansion-assb.md]
confidence: low
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: multi-source-primary
---

# 층상 NCM 격자 ↔ `x(Li)` 교정 — 구조 SOC 눈금의 축 규약 · 단조 채널 · 교정 간 이송

> `assb` 축 **구조 SOC 눈금** 페이지. 닻은 [[assb-contact-loss-vs-lampe]].
> 회절로 양극의 `x(Li)` 를 읽는 방법(22 · 24호)이 기대는 **교정 곡선 자체**를 다룬다. 원자료는 66호(de Biasi 2017 *J. Phys. Chem. C* 121, 26163 — 조성 여섯 × δ, 101 행).
> ⚠ 교정은 전부 **액체 LIB** 에서 잰 것이다 — ASSB 로 옮기는 부분은 `[해석]` 이다.

## 정의 — 교정과 읽기를 한 식으로 (`[해석]`)

```
교정(기준 셀, 액체 LIB):  δ(t) = δ₀ − ∫ I dt / (m · q),   q = F/(3.6 M) ≈ 275–278 mAh g⁻¹ per δ
                          g : δ ↦ (a, c, V)      (단상 Rietveld — 전극 속 모든 입자의 평균 격자)
읽기(다른 셀 · 시편):      x̂ = g⁻¹(a) 또는 g⁻¹(V)  (c 는 꼭짓점 근처에서 두 가지)
```

| 요소 | 무엇 | 66호에서 | 22호 · 24호에서 |
|---|---|---|---|
| **δ₀ 과 결손 배정(축 규약)** | 출발 조성 · 몇째 사이클 · 전처리 CE 결손을 어디에 두나 | `[인쇄]` "around 1.02"(공칭) · 넷째 충전 · "Coulombic efficiencies of less than 100% are a result of Li loss from the cathode material only" → NCM622 0.93 부터 | 22호: 첫 사이클 · x 1.02 부터 · `[인쇄]`(22호 Fig. S4 캡션) "The lithium content was calculated from the electrochemical data" · 24호: Buchberger 2015 식(액체 NMC111/흑연, 원전 미열람) |
| **θ_ref = 1 · 부반응 0** | 전극의 모든 입자가 같은 δ 로 움직이고 통과 전하가 전부 탈리튬 | 암묵 — 두 상 정련 0 · 4.6 V 정전압 1 h 전하 포함 | 같은 가정(교정 셀) |
| **단조 채널** | 역함수가 하나인 격자량 | `V` 거의 전 구간 · `a` 는 δ ≳0.15–0.40(조성별) · `c` 는 δ ≈0.45 꼭짓점(여섯 조성 모두) | 22호: `a` · `c` + 음영(`a` ↔ `c` 편차) · 24호: c/a 선형(0 < x < 0.5) |
| **분해능** | 기울기 × 오차 | `[재현]` NCM622 `a` 0.071 Å · `V` 3.29 Å³ per δ · 매끈한 곡선 잔차 → δ ±0.004 · esd 는 잔차의 1/14–1/37(`V`) | 22호 esd(`a` 0.001 Å · `V` 0.01 Å³)로 δ ±0.014 · ±0.003 · 같은 로트 원형 두 시편 차 → 0.024–0.028 |
| **이송(다른 로트 · 기하 · 사이클)** | 교정 곡선을 다른 시편에 옮길 때의 오프셋 | `[재현]` 22호 곡선과 **x ≈0.067 가로 이동**(0.057–0.082, x 0.90–0.35 에서 거의 일정) | 24호: 초기값 > 1.0 → 교정 오프셋 ≥0.02–0.05 |

## 왜 중요한가 — 구조 채널을 쓸 때의 함정 여섯

1. ★★★ **교정 축은 전하다.** 격자로 읽은 `x` 는 기준 셀의 통과 전하를 θ_ref = 1 · 부반응 0 · 결손 배정 규약과 함께 빌린다. 22호의 불활성 분율(상 분율)은 교정 없이 서지만 `x_active` · `η` · 용량 닫힘은 교정 위다
   (66호 `[재현]`: 같은 연구망 NCM622 곡선으로 바꾸면 22호 닫힘 ±7 % → L · M +11…+16 %).
2. ★★★ **`c` 는 꼭짓점 근처에서 두 가지.** 여섯 조성 모두 δ ≈0.45(NCM622 포물선 꼭짓점 ≈0.456) — δ 0.40–0.50 에서 `c` 는 ±0.005 Å 안이다. 22호 활성 상이 정확히 그 위에 앉는다. `a` · `V` 로 읽고 `c` 는 가지 판정에만 쓴다.
3. ★★★ **교정 간 이송 오차가 교정 안 분해능보다 크다.** 같은 연구망 · 같은 장치 계열 · 같은 정련의 두 NCM622 교정이 x 로 ≈0.067 어긋난다(가로 이동) — 한 곡선 안의 분해능(±0.004)의 ×15 이상, 22호 인쇄 오차(±0.02)의 ×3.
4. ★★ **esd 는 산포가 아니다.** 66호 표 S1 의 매끈한 곡선 잔차가 esd 의 14–37 배(`V`) · 1–14 배(`a`). 같은 로트 원형 두 시편의 격자 차(22호 L ↔ M)가 실제 바닥이다.
5. ★★ **조성 특이 · 지연.** Buchberger 선형 c/a 식은 66호 NCM111 에 δ 0.94–0.50 에서 −0.028…+0.007 로 맞고, NCM523 · 622 에는 +0.02…+0.14 · +0.03…+0.07 로 벗어난다(`[재현]`). NCM523 · 721 은 충전 초반
   δ 0.93/0.91 → 0.75 에서 `a` 가 거의 안 움직인다 — 전하로 센 δ 와 격자 평균의 지연이 조성마다 다르다.
6. ★★ **`V(x)` 는 선형이 아니다 — 두께 · 압력 채널의 양극 몫.** NCM811 dV/dδ 가 3.99–4.05 V −4 → 4.24–4.32 V −30 Å³ per δ(×7). [[assb-operando-pressure-signal-attribution]] 의 "Δx 당 몰부피 변화" 는 상수가 아니라
   이 곡선의 기울기이고, 같은 용량에서 활성 입자의 수축(과 23호 틈 요구치)은 θ 에 걸린다(θ = 1 이면 23호 첫 충전 176 mAh g⁻¹ → δ ≈0.38 → −1.3…−1.7 % · θ = 0.8 이면 −4.2…−4.6 %).

## 표본 표 — 이 위키에 들어온 교정

| 편 | 재료 · 셀 | 축 규약 | 채널 | 인쇄 형태 | 이 위키가 확인한 것 |
|---|---|---|---|---|---|
| **66호** de Biasi 2017 | NCM 여섯(111 … 851005) · 파우치 LIB · LP47 · Mo Kα 투과 · 넷째 충전 C/10 3.0–4.6 V | 공칭 1.02 · 전처리 결손 = 양극 Li 손실 · 전하 계수 | `a` · `c` · `V` · `z` · TM–O · Li–O · U | 수치 표(101 행) · 충전만 | `c` 꼭짓점 δ ≈0.45(여섯) · `V` 잔차 esd ×14–37 · 인쇄 오기 셋 · 원형(표 2)과 첫 점의 `V` 부호 섞임 |
| **22호** Strauss 2018 | NCM622(NCM-M) · 파우치 LIB · LP57 · 첫 사이클 C/10 4.4–2.9 V | x 1.02 부터 · 전하 계수 | `a` · `c`(+ `V`, Fig. S4) | 그림만 | 66호 곡선과 x ≈0.067 가로 이동 · L ↔ M 은 바닥 아래 |
| **24호** Stavola 2023 | NMC111 · Buchberger 2015 식(액체 NMC111/흑연) · 투과 EDXRD | 원전 미열람 | c/a 선형(0 < x < 0.5) | 식 하나 | 초기값 > 1.0 → 오프셋 ≥0.02–0.05(24호 D5) · 66호 NCM111 과 ±0.03 안 |

⚠ 3차 묶음 파일 29(Kondrakov 2017 *JPCC* 121, 24381 — 66호 [19], `c` 붕괴 위임처) · 31(Kondrakov 2017 *JPCC* 121, 3286 — 66호 [15]) · 40(Buchberger 2015 — 24호 교정 원전)이 같은 축의 편이다(미흡수).

## 이 위키에서의 적용

- **카드 [[assb-contact-loss-vs-lampe]] Q1 · Q2** — 구조 채널을 "`θ` 의 측정" 으로 셀 때 상 분율(교정 비의존)과 `x_active`(교정 의존)를 따로 적고, 교정 규약(δ₀ · 사이클 · 결손 배정 · 교정 셀 θ_ref)을 값 옆에 적는다.
- **[[assb-lampe-contact-product-degeneracy]]** — "SOC 추종 상 분율" 줄(22호)에 붙는 경고 행(66호) — 교정 조건.
- **[[assb-apparent-capacity-decomposition]]** — 22호 3항 분해의 `η` 는 교정 곡선의 축을 빌린다(66호 절).
- **[[assb-operando-pressure-signal-attribution]]** — 양극 몫 `Δh_ca` 의 둘째 인자 = `dV/dx`(66호 표 S1 원자료).
- **합성 truth([[assb-synthetic-truth-contact-loss-requirements]])** — 구조 관측을 truth 에 넣는다면 `V(x)` 곡선 전체와 교정 규약(δ₀ 오프셋)을 파라미터로 두는 후보(결정은 사용자 몫 · 코드 0).

## 이 페이지가 주장하지 않는 것

- **어느 교정의 축이 참 Li 함량인지 안다고 하지 않는다** — 세 편 모두 화학 분석(ICP · 적정)이 없다. x ≈0.067 이동은 두 곡선의 상대 이동이다.
- **이동의 원인이 결손 배정 규약이라고 단정하지 않는다** — 크기가 66호 전처리 보정(0.09)과 같은 자릿수라는 것까지이고, 로트 · 전해질 · 22호 그림 판독(±0.01–0.02)이 섞인다.
- **액체 교정의 θ_ref = 1 이 틀렸다고 하지 않는다** — 66호 S3 · Fig. 6 에 둘째 상은 안 보인다(우리 판독). 검사되지 않은 가정이라는 것까지다.
- **ASSB 셀의 격자가 액체 교정 곡선을 따른다고 전제하지 않는다** — 구속 · 응력 · 전해질이 다르다(ASSB 에서 잰 교정 곡선은 이 위키에 0).
- **`evidenceScope: multi-source-primary` · `confidence: low`** — 교정 원자료는 66호 하나이고, 22호 곡선은 그림 판독, 24호 식은 전사(원전 미열람)다.

## 관련
- [[assb-contact-loss-vs-lampe]] — 닻. Q1 · Q2 의 구조 채널 항목.
- [[assb-apparent-capacity-decomposition]] — 22호 `θ` · `η` 분리 · 66호 절.
- [[assb-lampe-contact-product-degeneracy]] — 처방 표 "SOC 추종 상 분율" 줄과 그 경고 행.
- [[assb-operando-pressure-signal-attribution]] — 두께 · 압력 신호의 양극 몫(`dV/dx`).
- [[composite-cathode-percolation-utilization]] — `θ_AM` 의 정의(교정 셀이 1 로 두는 양).
- [[fitting-degeneracy]] — 화학량 오프셋(δ₀)이 적합에서 다른 파라미터와 섞이는 자리(액체셀 축).
