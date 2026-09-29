---
title: "ASSB 복합양극의 굴곡도 인자 — 측정되는 것은 σ_eff 하나이고 ε·τ² 분할은 가정이 정한다"
description: "In ASSB composite cathodes the tortuosity factor tau^2 = eps x sigma_bulk / sigma_eff is not measured but obtained by dividing a measured effective conductivity by an assumed phase fraction; the only operando-plus-EIS paper in the lineage shows the same measured conductivities giving opposite tau^2 trends under two eps conventions, reads the mismatch between its EIS and model-fitted values as tortuosity evolution, and by its own definition places point-contact loss inside tau^2"
created: 2026-09-23
updated: 2026-09-29
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/wang2024_fast-kinetics-hierarchical-catholyte-anode-design-ssb.md, raw/papers/jiao2023_electro-chemo-mechanical-se-modulus-conductivity-intergranular-czm.md, raw/papers/schlautmann2023_lpscl-particle-size-distribution-composite-transport.md, raw/papers/shi2020_particle-size-ratio-cathode-utilization-assb.md, raw/papers/davis2021_operando-microscopy-graphite-lpscl-composite-current-focusing.md, raw/papers/naik2022_kinetics-vs-transport-ssb-cathode-mesoscale-regime-map.md, raw/papers/minnmann2021_charge-transport-bottlenecks-tlm-ncm622-lpscl.md, raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode-si.md, raw/papers/bielefeld2020_effective-ionic-conductivity-binder-composite-cathode.md, raw/papers/hlushkou2018_void-space-ion-transport-composite-cathode.md, raw/papers/neumann2021_garnet-3d-structure-grain-boundary-transport.md, raw/papers/stavola2023_lithiation-gradients-tortuosity-thick-nmc111-argyrodite.md, raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode.md, raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md, raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md, raw/papers/strauss2018_cathode-particle-size-inactive-fraction-assb.md, raw/papers/zhou2025_tailored-cathode-microstructure-low-pressure-assb.md, raw/papers/sinzig2024_p2d-validity-ssb-global-sensitivity.md]
confidence: low
explored: false
verificationStatus: unverified
claimType: interpretive
evidenceScope: multi-source-primary
---

# ASSB 복합양극의 굴곡도 인자 — `σ_eff` 는 재고, `ε·τ²` 는 나눈다

> `assb` 축의 개념 페이지. 닻은 [[assb-contact-loss-vs-lampe]].
> [[assb-lampe-contact-product-degeneracy]] 가 **동역학 항**(`A_eff·ε_p/R_s`)의 곱 축퇴를 다뤘다면, 이 페이지는 **수송 항**(`σ_bulk·ε/τ²`)의
> 곱 축퇴를 다룬다 — 그 페이지 ③ 채널(9호 `κ_eff = κ_se·ε_se^brug`)의 본체다.
> 수치의 정본은 원문 PDF 이고, 이 페이지의 값은 **사본**이다.

## 정의 — 인쇄된 식과 데이터가 보는 것

24호(Stavola 2023, `raw/papers/stavola2023_lithiation-gradients-tortuosity-thick-nmc111-argyrodite.md`)의 `[인쇄]` 식:

```
(2)  σ_i,eff = L / (R_i · A)                    ← 차단 셀 EIS(TLM) 의 R_i 에서
(3)  τ_i²   = (σ_i,bulk / σ_i,eff) · ε_i         ← 굴곡도 인자의 정의
(4)  τ_i²   = ε_i^(−a_i)                          ← 멱법칙 (a = 0.5 가 Bruggeman)
S6·S7 σ_eff = σ_bulk · ε^(1+a)                   ← 모델 입력 (= (3)+(4))
```

`[해석]` 데이터가 보는 것은 **`σ_eff` 하나**다. `τ²` 는 그것을 **`ε`(와 `σ_bulk`)로 나눈 이름표**이고, `a` 는 그 이름표를 `ε` 의 함수로 적합한 것이다.
`ε` 를 재지 않으면(24호: `[인쇄]` "assuming 14% of the cathode is void") **`τ²` 와 `ε` 는 곱으로만 식별된다.**

`[인쇄]` 24호 SI p3 는 이 양의 뜻을 스스로 넓힌다: "the empirical tortuosity factor accounts not only for the length of conduction paths, but also their width,
including cross-sectional areas and **point contacts**." ⇒ **부분 접촉 손실은 정의상 `τ²` 안에 들어간다.**

## ★★★★ 같은 측정, 반대 추세 — `ε` 규약 하나로 (24호 Table S8, `[재현]`)

| CAM wt% | σ_ion,eff `[인쇄]` (S cm⁻¹) | τ²_LPSC `[인쇄]` | ε_CAM 로 계산 | **ε_LPSC 로 계산** |
|---|---|---|---|---|
| 95 | 3.785e-6 | 392.44 | 391.6 | **40.2** |
| 80 | 6.758e-5 | 15.62 | 15.74 | **8.43** |
| 70 | 8.682e-5 | 9.63 | 9.63 | **9.19** |
| 40 | 1.495e-4 | 2.49 | 2.54 | **8.39** |

(σ_bulk = 1.9e-3, `[인쇄]` 0 % CAM 펠릿.) 인쇄값은 **4/4 가 CAM 분율로 ≤2 % 재현**되고, 식 (3) 이 요구하는 LPSC 분율로는 1.05–10 배 어긋난다.
- 인쇄값으로는 70 → 80 % 에서 **×1.6 — `[인쇄]` "tipping point"**. 바른 `ε` 로는 **×0.92 — 40–80 % 에서 평탄(≈8.4–9.2)**, 95 % 에서만 급등.
- 멱법칙 `ε^(−a)` 도 인쇄값으로는 a ≈2.2–2.6(95 % 점이 2.365 를 정함), 바른 `ε` 로는 점별 a = **1.46 / 1.77 / 2.56 / 5.12** — **형태 자체가 안 선다.**
- ⇒ **측정(`σ_eff`)은 하나이고 결론(추세)은 가정이 정했다.** 이것이 이 페이지의 요지다.

## ★★★ 두 경로의 불일치를 "진화" 로 읽는 자리

24호는 `τ²` 를 **EIS(신품 차단 셀)** 와 **COMSOL 역적합(operando EDXRD 리튬화 구배)** 두 경로로 내고, 차이를 `[인쇄]` "the tortuosity factor **evolved** …
Because NMC shrinks during delithiation, rearrangement of particle contacts is expected" 로 배정한다. `[재현]` `τ²` 가 아니라 **`σ_eff` 로** 비교하면:

| | COMSOL / EIS 직접 | COMSOL / EIS 멱법칙 |
|---|---|---|
| LPSC 70 % | **0.93** | 0.75 |
| LPSC 80 % | **0.34** | 0.67 |
| NMC 70 % | 0.46 | **1.08** |
| NMC 80 % | 0.29 | **0.95** |

⇒ "두 조성 모두에서 SE 굴곡도 증가" 는 **80 % 셀 이온 전도도의 ≈3 배 저하 하나**로 줄어든다. 그 3 배의 후보:
1. **제조 압력** — EIS 셀 50 MPa(이온 차단) · 150 MPa(전자 차단) ↔ operando 양극 100 MPa.
2. **가정 `ε`** — `[재현]` 인쇄 두께가 함의하는 void ≈21–38 % ↔ 가정 14 %.
3. **모델 구조** — 2열 단분산 입자 · NMC 연속상(입자 간 Li 확산 허용) · **OCP 없음** · 10 h 강제 충전.
4. **접촉 손실** — 저자가 쓴 기구 그대로. 정의상 `τ²` 안.
5. (그리고) 80 % 집전체 쪽 조각의 **거의 반응 안 하는 모집단**(`θ` 형 — [[assb-apparent-capacity-decomposition]] §24호).

**24호는 1–5 를 가를 입력이 없고 4 를 골랐다.** 독립 경로 하나가 같은 셀을 가리킨다: `[재현]` 옴 강하 `i·L/(2σ_eff)` 와 (우리가 가정한) NMC111 OCP 기울기로
구배 크기를 추정하면 70·40 % 는 차수가 맞고 **80 % 만 ≈3–5 배 모자란다**.

## 왜 중요한가 — 접촉 손실의 **연속판**이 수송 인자의 이름으로 들어온다

[[assb-apparent-capacity-decomposition]] 의 3항 분해에서:

| 접촉 변화의 크기 | 어디로 가나 | 이름 |
|---|---|---|
| 입자가 **완전히** 끊김 | `θ` (쓰이지 않는 부피) | 불활성 · isolated (22호) |
| 경로가 **좁아짐**(점 접촉 감소, 연결은 유지) | `σ_eff ↓` → `η(z)` (깊이 방향 이용 지연) | **"굴곡도 증가"** (24호) |
| 계면 **면적**이 줄어듦 | `A_eff ↓` → `η(i)` (분극) | 접촉 손실 · `A_eff` (9·16호) |

⇒ 14호(Oh 2025)가 보인 **"접촉 손실 → 용량 사상은 문턱형"** 과 짝이다(`[추론]`): 문턱 아래 몫은 용량(`θ`)으로 가지 않고 **`σ_eff`·`A_eff` 를 거쳐 율 의존 손실로** 간다.
OCV 적합은 셋 중 첫째만 용량 축 스케일로 보고, 둘째·셋째는 **컷오프에 걸린 만큼만 겉보기 `LAM_PE`** 로 본다.

그리고 1호(Bielefeld 2019)가 `[인쇄]` "tortuosity, and resulting effective conductivities … are **not explicitly treated**" 로 뺀 항이 바로 이것이다 — 1호의 `θ` 는
첫째 줄만 계산한다([[composite-cathode-percolation-utilization]]).

## 무엇을 재면 갈리나 (처방)

1. **`ε` 를 잰다** — 단층촬영·밀도 · 적어도 인쇄 두께와 질량의 폐합. 못 재면 `τ²` 대신 **`σ_eff` 를 보고**한다.
2. **두 경로(EIS ↔ operando 역적합)의 시편은 같은 제조 압력·같은 두께**로 — 아니면 차이가 압력 이력에 배정된다(곱 축퇴 처방 4단계의 조건).
3. **같은 셀에서 첫 충전 전·후 차단 측정** — "진화" 는 두 시점의 측정으로만 주장할 수 있다.
4. **역적합에서 `ε` 를 자유로 두고 `a` 와의 프로파일을 그린다** — `ε^(1+a) = const` 곡선이 평탄 계곡으로 나오면 분할은 비식별이다([[near-optimal-set-width-measurement]]).
5. **모델에 OCP 를 넣는다** — 구배 크기는 `Δφ/(dU/dx)` 로 정해진다. OCP 없는 역적합은 무엇과 무엇이 교환됐는지 재현할 수 없다.

## ★★ 세 번째 종류의 "굴곡도" — 계산만 있고 `σ_eff` 는 없다 (2026-09-23, `assb` 25호)

`raw/papers/zhou2025_tailored-cathode-microstructure-low-pressure-assb.md` (Zhou 2025) 는 DEM 입자 그래프에서 **기하 굴곡도 τ = 경로 길이 / 직선 거리**를 계산한다 — `[인쇄]` 중앙값 fine **1.21** ↔ coarse **1.84**.

| | 24호 | 25호 |
|---|---|---|
| 양 | 굴곡도 **인자** `τ² = ε·σ_bulk/σ_eff` | **기하** τ (경로 길이비, 무차원) |
| 측정 | `σ_eff` 를 **잰다**(차단 셀 TLM) | `σ_eff` 를 **안 잰다**(차단 셀 0) |
| 가정 | `ε` 14 % | DEM 입도·연결 기준 |
| 함정 | 측정 ÷ 가정 | **계산만** — 그리고 SI Fig. S15 히스토그램 **제목이 본문 중앙값과 반대**(`[도표]` "Coarse" 판 ≈1.19, "Fine" 판 1.35–2.45) |

⇒ 25호의 "굴곡도 감소로 이온 수송 향상" 은 **계산 하나 + 제목 반전** 위에 있고, 같은 지면의 관측은 오히려 반대다 — `[도표]` 신품 고주파 절편 fine ≈54 > coarse ≈49.5 Ω, SE 벌크 σ `[도표]` ×0.66.
이 페이지의 처방 1("못 재면 `σ_eff` 를 보고")이 한 단계 앞에서 걸린다: **`σ_eff` 를 재지 않으면 굴곡도는 수송 주장의 근거가 되지 않는다.**

## ★★ 이름 충돌 — 27호의 `τ` 는 24호의 `τ²` 다 (2026-09-23, `assb` 27호)

`raw/papers/sinzig2024_p2d-validity-ssb-global-sensitivity.md` (Sinzig 외 2024, *JES* 171, 120519 — 3D 입자 분해 ↔ P2D 비교 모델 편).
`[인쇄]` 균질화 유속 `N̄ = N/τ`, `τ = ε^b`, `b = −0.5` ⇒ `σ_eff = (ε/τ)σ = ε^1.5 σ`. `[재현]` `τ_el = 0.424^−0.5 = 1.54` ✓ · `τ_c = 0.376^−0.5 = 1.63` ✓.
⇒ 이 편이 `τ` 라 부르는 것은 **굴곡도 인자**(24호 식 (3) 의 `τ²`)다. 두 편을 나란히 읽을 때 **`τ` 값을 그대로 비교하면 제곱만큼 틀린다.**

- **측정 0 · 전부 Bruggeman** — 24호(측정 ÷ 가정) · 25호(기하 계산만)보다 한 단계 더 가정 쪽이다.
- **P2D 에서 `κ` 는 `(ε_el/τ_el)κ` 로만 들어간다**(`[인쇄]` 식 10 · Table III). 이 편의 Sobol "ion. cond." 지수는 **`κ_eff` 의 지수**이고 `κ` ×1000 은 `ε/τ` ×1000 과 같다 — 곱의 짝을 흔들지 않아 곱이 드러나지 않는다.
- `[인쇄]` "While a constant difference could still be corrected by an update of the homogenization parameters" — 저자는 **`ε/τ` 재보정이 모델 구조 오차를 흡수할 수 있다**고 쓴다. 이 페이지의 요지(분할은 가정이 정한다)의 모델 판: **보정된 `τ` 는 물성이 아니라 "구조 오차 + 물성" 이 될 수 있다.**
  ⚠ 단 `[재현]` 이 편에서 그 "상수 차이" 의 크기는 수송이 아니라 **비연결 입자 몫 `1 − u` = 0.07** 과 맞는다 — [[assb-sensitivity-sweep-vs-identifiability]] §27호.

## ★★ 네 번째 표본 — 측정 `σ_eff` ÷ **공칭** `ε`, 공극은 `τ` 로 (2026-09-23, `assb` 29호)

`raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode.md` (Yanev 외 2024, *JES* 171, 050530 — 14 복합체).
`[인쇄]` 식 (4) `τ = (σ₀/σ_eff)·ε` (ref 22 Kaiser 2018) — 이름은 `τ` 지만 **굴곡도 인자**(24호의 `τ²`, 27호의 `τ` 와 같은 양). `σ_eff` 는 대칭 셀 EIS 의 **TLM 적합**, `σ₀` 는 SE 펠릿 차단 EIS(3.13 · BM 1.62 mS cm⁻¹).
- `[재현]` `ε = τ·σ_eff/σ₀` 로 역산하면 조성마다 하나(**0.57 / 0.37 / 0.234 / 0.153**)이고 gran·sc·BM 에 공통 ⇒ **공칭 catholyte 분율**이다. 공극은 측정되지 않았고 **`τ` 로 들어간다** — 저자도 `τ` 를 "geometric and porosity-related effects" 로 부른다(24호 D1 과 달리 규약이 서술과 맞는다).
- ⚠ sc73-BM 행만 `ε` 0.326 — `τ` 2.6 ↔ 정합값 2.9(같은 행 `φ` 도 불일치, 29호 D4).
- `τ` 1.5 → 54.2 (한 자릿수 반). 29호는 `τ` 를 결론에 쓰지 않는다(SI Fig. S8 로만) — 병목 판정은 `σ_eff`·`D` 로 한다.
- ↳ **2026-09-28 29호 SI 보강**(`raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode-si.md`): 공칭 `ε` 의 정체가 인쇄됐다 — Tab. S1 SE 부피비(66.20 / 43.50 / 27.80 / 18.10 %) × **(1 − 0.15)**, `[인쇄]` 두께도 "calculated … assuming 15% porosity"(얇아서 못 쟀다고 적었다). `[재현]` 역산 `ε` 가 12/13 셀에서 ±2.2 % 안(sc73-BM −11.9 % = 29호 D4 그대로). ⇒ `σ_eff ∝ L ∝ 1/(1−p)` · `ε ∝ (1−p)` 라 **`τ ∝ (1−p)²`** — 공극을 5 · 25 % 로 바꾸면 `τ` ×1.25 · ×0.78. 이 표본의 `τ` 는 **공극 가정의 제곱**을 품는다(측정 `σ_eff` 에 가정 두께 — 24호 · 25호 · 27호와 다른 규약). SI Fig. S8 의 `τ` · `φ` 는 Table I 값 그대로다.

## ★★★ 다섯 번째 표본 — 굴곡도를 **구조로 계산**해 곱을 풀고, 남은 합은 입력으로 닫았다 (2026-09-23, `assb` 54호)

`raw/papers/neumann2021_garnet-3d-structure-grain-boundary-transport.md` (Neumann … Latz 2021, LLCZNO 다공층 56 · 42 · 25 %, 공극 = 공기). 앞 네 표본(24 · 25 · 27 · 29호)은 `σ_eff` 를 재고 `ε·τ²` 를 **나눴다**. 이 편은 반대 방향 — FIB-SEM 3D 재구성 위에서 수송을 풀어 `τ` 를 **계산**하고, `σ_eff` 는 모델이 낸다.

- **이름**: Table 1 `τ` x/y/z(56 % 1.75/1.68/1.78 · 42 % 1.45/1.34/1.26 · 25 % 1.21/1.15/1.20)의 정의는 미인쇄. `[재현]` 구조-만 `σ_eff/σ⁰`(Fig. 8 판독) ≈ `ε/τ_x²` — 56 % 0.139 ↔ 0.139 · 42 % 0.273 ↔ 0.266 · 25 % 0.481 ↔ 0.512 ⇒ 표의 `τ` 는 **기하 굴곡도**이고 이 페이지의 `τ²` 가 그 제곱이다(27호 이름 충돌의 반대 짝).
- **곱은 풀렸다, 합이 남는다**: 입계(`i₀₀^GB` · `C_DL^GB`)를 넣으면 56 % 에서 `σ_eff` 가 1.1e-4 → 8.6e-6(`[인쇄]`). 이 **추가 인자**는 벌크 `σ⁰` 저하와 같은 모양으로 스펙트럼을 움직이고(`[인쇄]` "an exact deconvolution of both contributions via EIS is unfeasible"), `σ⁰` 는 벌크 절편이 대역 밖이라 **입력**이다(문헌 범위 2.4–7.69e-4 의 윗끝).
- **하류에서 지수가 된다**: 53호(Ren 2023)가 `σ_eff = σ⁰·ε^(β_GB+β_tort)`, `β_tort` 2.31 · `β_GB` 1.39 를 이 편 출처로 적었는데 이 편에 지수는 없다. `[재현]` 점별 구조-만 지수 2.54 · 2.23 · **2.31**(56 % 한 점) · 치밀 전 모형 정규화 입계 초과 지수 1.36 · 0.70 · 1.46 — **단일 멱법칙이 서지 않는다**(24호 "형태 자체가 안 선다" 와 같은 결론을 다른 경로로). 그 정규화면 곱하는 `σ⁰` 는 치밀 전 모형 2.1e-4 여야 하는데 53호는 8e-4 를 썼다(`[재현]` ×≈0.27 차 — 우리 재구성).
- ⇒ 이 페이지 요지의 네 번째 판: **`σ_eff` 는 재거나 계산하고, `ε·τ²` 분할은 가정(24호)이거나 구조(54호)이며, 그 위에 얹히는 입계 · 2차상 인자는 EIS 로 벌크와 갈리지 않는다.** 펠릿 지수를 복합양극으로 옮길 때 `ε` 범위(0.43–0.75 → 0.25) · 입도(공극률과 교락) · `σ⁰` 의 뜻을 같이 옮긴다.

## ★★★ 여섯 번째 표본 — 한 편이 두 경로(EIS · 구조)를 다 냈고, 비교는 `τ` 로 했다 (2026-09-23, `assb` 55호)

`raw/papers/hlushkou2018_void-space-ion-transport-composite-cathode.md` (Hlushkou · … · Roling · Tallarek 2018, *JPS* 396, 363 — LCO/비정질 LPSI, 탄소 없음 · 01호 ref 16).
앞 다섯 표본은 한 경로씩이었다(24 · 29호 측정 ÷ `ε`, 25 · 27호 계산 · 가정, 54호 구조 계산 + 재사용 EIS). 이 편은 **같은 연구에서 두 경로를 다 낸다** — 대칭셀 EIS(`τ_cond`)와 FIB-SEM 재구성 위 추적자 확산(`τ_diff`).

- **이름**: `[인쇄]` 식 (3) `τ_cond = (σ⁰/σ_comp)·ε` · 식 (9) `τ_diff = D⁰/D_eff` · Bruggeman `τ_B = ε^−0.5` ⇒ 이 편의 `τ` 는 **굴곡도 인자**(이 페이지의 `τ²`, 27 · 29호의 `τ`). 54호의 기하 `τ` 와 섞지 않는다.
- **경로 B 안에서는 곱이 풀린다**: 영상 `ε`(SE 53.7 %) · 모의 `τ` 1.74 각각. 같은 구조의 void 를 SE 로 채운 가상 구조에서 `τ` 1.27 · `ε` 66.9 % — `[재현]` `ε/τ` 0.309 → 0.527(×1.71), 로그 몫 `ε` 41 · `τ` **59 %**. 공극은 `ε` 만이 아니라 기하를 바꾼다: `[인쇄]` Bruggeman 은 무공극에서만 맞는다(1.22 ↔ 1.27), 실제는 `[재현]` 1.365 ↔ 1.74(인쇄 1.34, 55호 D3). 함의 지수 `ε^a`: a 1.59 → **1.89**.
- **두 경로 사이에서는 안 풀린다**: EIS 쪽 `ε` **미인쇄** — `[재현]`(관 내경 9.8 mm · σ⁰ 0.7 mS cm⁻¹) 관측 곱 **0.406 ± 0.013**, `τ_cond` 1.6 은 `ε` ≈0.65 에서 나온다(공칭 0.62 → 1.53 · 영상 0.537 → 1.32). **곱으로 비교하면** EIS 0.406 ↔ 모의 0.309(×1.31) · 무공극 0.527. EIS 시편의 void 는 재지 않았고 두 시편은 수지 · 충전 상태 · 압착 · 두께가 다르다 — 원문은 차를 "수지" 하나에 배정(24호가 "진화" 에 배정한 것과 같은 구조).
- ⇒ 이 페이지 요지의 다섯 번째 판: **구조가 곱을 푸는 것은 그 구조의 시편에 대해서다.** 측정과 구조를 대조할 때는 `τ` 가 아니라 `σ_eff/σ⁰` 를, 같은 시편 · 같은 `ε` 로 비교한다(처방 1 의 강화). 측정 0.406 은 "void 13 % + Bruggeman"(`[재현]` 0.394)과도 맞아 분할이 서지 않는다.
- **표의 둘째 줄에 수가 붙었다**: 위 "왜 중요한가" 표의 "경로가 좁아짐 → `σ_eff` ↓" — 이 편은 void 13.2 %(수지 포함)의 경로 효과를 ×0.59 로 계산했다. 셋째 줄(면적 `A_eff`/`φ`)은 모의에 계면이 없어 **구성상 0** 이다.

## ★★★ 일곱 번째 표본 — 구조 계산이 곱을 풀고, `τ²` 는 그 몫을 다시 쓴 것이며, 검증은 가정 `ε` 위의 한 점이다 (2026-09-23, `assb` 57호)

`raw/papers/bielefeld2020_effective-ionic-conductivity-binder-composite-cathode.md` (Bielefeld · Weber · Janek 2020, *ACS AMI* 12, 12821 — 01호 저자 셋의 속편, GeoDict 합성 구조 + EJ-heat 정상 전도). 24호가 `τ²` 정의를 가져왔다고 인용한 편이다(24호 ref 41).

- **정의**: `[인쇄]` 식 (3) `σ_eff = ε_SE/τ² · σ⁰` · 식 (11) `τ² = σ⁰·ε_SE/σ_eff` · `ε_SE = (1 − φ_void)·v_SE`(void 포함 전체 부피 기준) — 이 페이지의 `τ²` 와 같은 양, **24호 D1(CAM 분율로 나눔)과 다른 규약**. ⇒ 24호가 이 정의를 가져왔다면 따르지 않은 것이다.
- **경로 B(구조) 한 가지만, 그러나 스윕으로**: `σ⁰` 2.7 입력 · 구조 `ε` · 계산 `σ_eff` → `τ²` 는 이름표(`[재현]` Fig. 4 `τ²` 가 재현된다). 조성(40–68 vol%) · AM 크기(3–15 µm) · 다봉 분포 · **void 5 · 10 · 20 %** · 바인더 0 · 0.05 · 0.10 을 돌렸다 — 계보에서 `τ²` 의 **구조 의존을 스윕으로 준 첫 편**.
- **void 의 로그 분할**(`[재현]`, 50:50 · d 5 µm): `σ_eff` 5 → 20 % 비 1.81 = `ε` ×1.19 · `τ²` ×1.52 → `τ²` 몫 **70 %**(55호 실측 구조의 가상 치환 59 %와 같은 방향). **void 축 문턱 0** — 세 점 단조, 급변은 AM 분율 축(60 → 66 vol% 한 칸 보간)과 바인더에서만.
- **Bruggeman**: `[인쇄]` "significantly underestimates … 4-fold" · 수정식 α 2.02–1.21 · γ 0.32–0.67 — `[재현]` 전도도 지수(`σ_eff/σ⁰ ∝ ε^(1+α)`) **3.02 · 2.21**(55호 함의 1.89 · 고전 1.5). 저자 "these parameters do not offer any further scientific insight".
- **바인더**: `τ²` 는 **순수 SE `ε`** 로 나눈다(`[재현]` ε_AM 68 · 0.10: 835 ↔ SE+바인더 1391, `[도표]` ≈800) ⇒ 바인더 `τ²` 증가(70:30 에서 4.2 → 10)는 SE 부피 손실이 아니라 **경로 차단** 몫. 그러나 같은 편 전류 추정은 SE+바인더 `v_SE` 로 곱해 ×1.15–1.30 과대(D4) — 규약이 한 지면 안에서 바뀐다.
- **경로 A(측정)와의 대조는 한 점, 가정 `ε` 로**: Kato 2018 `σ_eff` 0.73 ↔ 모의 0.68(void **15 % 가정** — 시편 void 미보고); `τ²` 2.29 ↔ 2.47 의 차는 `ε` 규약(`[재현]` 2.28 · 2.50). ⇒ 여섯 번째 표본(55호)의 교훈 "같은 시편 · 같은 `ε`" 의 **실패형**: 시편 `ε` 를 모르면 구조 계산은 곱을 예측하지 않고 맞춘다 — 같은 지면의 void 손잡이(×2)가 일치 폭(7 %)보다 크다.

## ★★★ 여덟 번째 표본 — 계보가 식 (2)(4)를 빌려 온 방법 편: 차단 셀 두 종 · T형 TLM · 규약은 57호와 같고, 14 % 는 여기서도 가정이다 (2026-09-28, `assb` 73호)

`raw/papers/minnmann2021_charge-transport-bottlenecks-tlm-ncm622-lpscl.md` (Minnmann · Quillman · Burkhardt · Richter · Janek 2021, *JES* 168, 040537 — 무탄소 · 무바인더 NCM-622(3 µm) \| Li₆PS₅Cl, Φ 25–61 vol%). 24호 ref 42 · 50호 SI 4 · 56호 ref 27 이 "차단 셀 + TLM 방법" · "void 14 %" 의 근거로 단 편이고, 02호 Fig. 3 의 실험 점이 이 편 Fig. 2(a) 에서 왔다. SI 미수령.

- **정의 · 규약**: `[인쇄]` 식 2 `σ_i,eff = L/(R_i A)` · 식 3 `τ_i = l_i/l_0`(기하 굴곡도) · 식 4 `τ_i² = σ_i,0 φ_i/σ_i,eff`(ref 6 = 57호) — 이 편의 τ² 는 이 페이지의 `τ²` 와 같은 양이다. `[재현]` Fig. 2(b) τ² 가 (a) σ 에서 **이온 φ_SE = 1 − Φ − 0.14**(4/4 −2.9…+0.9 %) · **전자 φ_CAM = Φ**(5/5 −2.5…−0.9 %)로 재현된다(σ_ion,0 1.6 · σ_el,0 10 mS cm⁻¹) — 공극 포함 전체 부피 기준, 57호 식 (11) 과 같은 규약. ⇒ **24호 D1(이온 τ² 를 CAM 분율로)은 57호 · 이 편 어느 원전의 규약도 아니다.** 42 vol% 에서는 두 규약이 4.00 ↔ 4.27 로 가까워 이 편의 42 % 예시 한 점으로는 차가 안 보인다.
- **14 % 의 인쇄 자리**: `[인쇄]` "an average porosity of 14 % is assumed"(도출 SI Section 3) · 측정 범위 "13 %–17 % (Table SIII)" — 24호 "assuming 14% of the cathode is void (refs 7, 41, 42, 48, 49)" 의 ref 42 가 이 편이다(57호 = ref 41 은 15 %). `[재현]` 두께를 인쇄한 유일한 시편(42 vol% · 100 mg · 470 µm)은 15.8 %. **조성마다 같은 가정 값**이 모든 τ² 의 φ 와 Φ 축에 들어간다.
- **두 운반자 · 두 셀 · 뺀 합**: 전자 σ 는 이온 차단 셀(SS \| 복합체 \| SS)의 직류 끝 `R_el = L(r_el,1 + r_el,2)`, 이온 σ 는 전자 차단 셀(In/(InLi)ₓ \| LPSCl \| 복합체 \| LPSCl \| In/(InLi)ₓ)의 직류 끝에서 분리막 `2R_SE`(고주파 오프셋 귀속) · In 계면 `2R_In`(대칭셀 "considered")을 뺀 `R_ion` 이다. `[재현]` 뺀 합(42 vol% 역산 ≈100 Ω)은 조성 따라 `R_ion` 의 ≈59 %(25 vol%) → ≈1 %(61 vol%) — **저 CAM 의 τ²_ion 이 빼는 방법에 가장 민감**하고, 고 CAM 의 τ²_el 은 회로에 없는 강철 접촉 몇 Ω 에 ≈10 % 로 걸린다.
- **점 접촉이 τ²_el 안에 — 수 한 개**: `[인쇄]` 이 편도 식 4 가 "current constriction, cathode-electrolyte-interphase (CEI) formation, interface polarization, and space charge layers" 를 무시한다고 적는다("the determined tortuosity factor might deviate from the 'true' geometrical tortuosity factor"). `[재현]` 42 vol% 에서 `R_el` 107 Ω 의 ≈76 %(`r_el,2` ≈81.5 Ω)가 입자 간 전자 계면("interfacial charge transfer") 몫 — τ²_el 7.4 는 NCM 벌크 경로보다 **접촉 저항**을 주로 적은 수다(고주파 절편이 7 MHz 에서 닫혔다는 가정 위). 위 "왜 중요한가" 표의 둘째 줄(경로가 좁아짐 → `σ_eff` ↓)이 전자 쪽에서 수를 얻었다.
- **기준값도 가정이다**: 두 순수 기준점이 다른 공극 처리로만 τ² ≈1 에 앉는다 — LPSCl 점 1.006(σ₀ 1.6 · φ = 1) · NCM 점 0.99(`[도표]` σ 8.37e-3 ↔ 캡션 σ_el,0 10 mS cm⁻¹ — `[해석]` 8.37/0.86 = 9.7 로 읽힌다). LPSCl 에도 같은 보정을 하면 모든 τ²_ion 이 ×1.19(판정 아님 — 기준값의 시편 조건은 SI Table S2).
- **막대**: τ² 에만 정의 없는 ≈±20 % 막대(12/12 · 기준점 τ² = 1 둘에도 같은 크기) · σ 막대 0 — 통계 산포로 읽을 수 없다.
- ⇒ 이 페이지 요지의 방법 편 판: **계보가 식을 빌려 온 편에서도 측정은 `σ_eff`(두 셀의 직류 끝)이고, `τ²` 는 가정 공극 · 가정 기준 · 뺀 합 위의 이름표다.** 처방에 붙는 것(`[해석]`): `τ²` 를 옮길 때 **어느 셀에서 무엇을 뺐는지(분리막 · 상대극 계면 · 집전체 접촉)** 와 **기준 σ₀ 시편의 공극 처리**를 값 옆에 적는다. 한 셀 스펙트럼에서 호 배정이 안 갈린다는 것(두 차단 셀 교차 대입)은 [[assb-lampe-contact-product-degeneracy]] 쉰여섯 번째 적용.

## ★★ 아홉 번째 표본 — 확률 미세구조 DNS 로 계산한 `τ`(인자) · 이름표는 기하 단위 · 실측(73호)의 1/1.9–1/5.9 (2026-09-28, `assb` 75호)

`raw/papers/naik2022_kinetics-vs-transport-ssb-cathode-mesoscale-regime-map.md` (Naik · Vishnugopi · Mukherjee 2022, *ACS AMI* 14, 29754 — GeoDict 확률 미세구조 · NMC622 10 µm · β-Li₃PS₄ 3 µm · CBD · 공극 5 % · 모형 편).

- **정의 · 규약**: `[인쇄]` 식 3 `ε_SE/τ = −j_x L_c/(D(φ_right − φ_left))` · 식 4 `κ_eff = κ·ε_SE/τ_SE,i` · x · y · z 산술 평균 — **`τ` 는 굴곡도 인자(이 페이지의 `τ²` 와 같은 자리)** 인데 Fig. 2a 색막대 이름표는 "τ [m/m]"(기하 굴곡도의 단위). ⚠ 이름 충돌(27호 줄)의 셋째 형태.
- **`[재현]`**: Fig. S1 κ_eff(표지 20)와 표 S1 밀도 + 공극 5 % 로 `τ = κε/κ_eff` — CBD 4 에서 1.32 · 1.69 · 3.79(40 · 60 · 80 wt%; 본문 1.3 · 1.5 · "up to 4") · 80/6 에서 5.53 · Bruggeman(`ε^1.5`) 대비 `κ_eff/κ_Brugg` 0.96(40/0) → **0.36(80/6)**.
- **실측과 대조(방향만)**: 73호 τ²_ion(차단 셀) 2.43 · 3.27 · 4.33 · 15.3(50 · 60 · 70 · 80 wt%) ↔ 이 편 DNS τ(CBD 0) 1.29 · 1.46 · 1.75 · 2.59 — **×1.9 · 2.2 · 2.5 · 5.9**. 입도(73호 NCM 3 µm) · 공극(14 ↔ 5 %) · SE(LPSCl ↔ β-Li₃PS₄)가 달라 같은 계의 차가 아니다 — 방향은 "DNS 확률 구조가 고 AM 병목을 과소평가" 다.
- **곱의 자리**: 이 편은 `ε/τ` 를 DNS 로 **계산해 입력으로 고정**한다 — 수송 곱을 적합하지 않으니 이 페이지의 `(ε, a)` 평탄 계곡은 생기지 않는다. 대신 검증(73호 네 점)에서 조성 이름표가 10 wt% 씩 밀렸다(75호 D1) — τ 를 조성의 함수로 옮길 때 **조성 기준(Φ ↔ wt%)** 이 사고 자리다.
- ⇒ 처방에 붙는 것(`[해석]`): DNS · 모형 편의 "τ" 는 ① 인자인지 기하인지(식으로 확인) ② 공극 · 입도 가정 ③ 실측 대조가 있으면 그 조성 기준을 값 옆에 적는다.

## ★★ 열 번째 표본 — 영상 2D 미세구조의 flux `τ`(정의식 미인쇄) · 측정 κ_eff 와 모형 κ_eff 가 ×5–9.5 어긋나고, TLM 두 그림의 단위가 ×10³ 어긋난다 (2026-09-29, `assb` 76호)

`raw/papers/davis2021_operando-microscopy-graphite-lpscl-composite-current-focusing.md` (Davis · … · Thornton · Dasgupta 2021, *ACS Energy Lett.* 6, 2993 — 흑연 \| Li₆PS₅Cl 복합 음극 · 차단 대칭 셀 TLM · 광학 영상 2D 모형).

- **정의 · 규약**: `[인쇄]` 모형 τ 1.91(원 미세구조) → 1.38(수축부 넓힘 · S14) — "average steady-state flux method"(SI ref 16 Tjaden 2018) · **식 미인쇄**(인자인지 기하인지 · ε 를 어떻게 넣는지 지면에 없다). 모형 κ_eff 는 `κ·ε/τ`(τ 를 인자로) 0.27 또는 `κ·ε/τ²` 0.14 S m⁻¹(`[재현]` ε_SE,2D 0.595 · κ 0.88 S m⁻¹) — τ 규약에 따라 ×2.
- **측정**: 이온 σ 는 이온 차단 대칭 셀 + TLM(교점 = R_ion/3 · SI refs 4–6 — Höltschi 2020 · Ogihara 2012 · Siroma 2016) — 73호와 같은 계열 · 다른 판. ⚠ **S1 "Conductivity (mS/cm)" ↔ S2 축 "Z (Ω cm)"** — `[재현]` 여섯 패널에서 S1 ≈ (0.86–0.97) × 1/R_ion(S2 축 수치) → 축이 저항률이면 S1 은 S cm⁻¹(벌크의 ×34 — 불가) · 두께 · 면적 환산식 미인쇄(76호 D5).
- **`[재현]` 측정 ↔ 모형**: S1(40 % · 60 °C) κ_eff **0.029 S m⁻¹** ↔ 모형 0.14–0.27 — **모형 SE 망이 ×5–9.5 잘 통한다**(실측 `ε·κ/κ_eff` ≈20 ↔ 모형 τ 1.91 또는 τ² 3.65). 조성별 `ε·κ/κ_eff` ≈20 · 85–90 · 63–69(40 · 60 · 80 % — 밀도 가정 ε · 73호 τ² 규약과 같은 식으로 읽은 우리 산술).
- **곱의 자리**: 모형은 κ 를 한 값으로 두고 기하(영상)로 τ 를 넣는다 — S16 "κ ×≈11" 은 수송 곱 전체를 ×11 한 것이고, S14 수축부 넓히기는 τ −28 % 와 함께 계면 모양도 바꿨다(한 손잡이 두 곱 — 57호 줄).
- ⇒ 처방에 붙는 것(`[해석]`): 한 편이 측정 κ_eff 와 모형 τ 를 다 냈으면 **둘을 같은 규약으로 나란히 적는다** — 76호처럼 모형이 자기 측정에 묶이지 않은 채 "qualitative" 로 남으면 크기(옴 강하)가 과소인 방향이 지면에서 안 보인다. 보충 그림 두 장이 같은 양을 다른 단위로 적었으면 환산식을 찾기 전에 값을 옮기지 않는다.

## ★ 열한 번째 표본 — 굴곡도 인쇄 0 · 최단 경로를 뽑고도 τ 로 쓰지 않았다: 24호 "굴곡도 진화" 의 원전 자리에는 연결(θ)만 있다 (2026-09-29, `assb` 77호)

`raw/papers/shi2020_particle-size-ratio-cathode-utilization-assb.md` (Shi · Tu · … · Ceder 2020, *Adv. Energy Mater.* 10, 1902881 — 24호 ref 53 "CAM/SE 입도비 → 이온 수송 — '수축 → 입도비 변화 → τ↑' 논거의 원전").

- **정의 · 규약**: `tortuos` **0 회**(본문 · SI) · `[인쇄]` "we extracted the shortest percolating pathway of each active CAM particle to a SE target particle" — 경로 길이 · 곧은 거리 비(기하 τ) · 분포는 **인쇄 0**. 출력은 이진 연결 부피 분율 `θ_CAM` 하나.
- **측정**: 복합체 유효 이온 전도도 0 · SE 펠릿 σ 만(표 S3 — 입도가 작을수록 0.32 → 0.14 mS cm⁻¹ · `[인쇄]` "likely because of the increased grain boundary (or particle boundary) resistance, which can be worsened by any residual solvent") — 곱 `κ_eff = κ·ε/τ²` 의 κ 가 λ 손잡이와 함께 움직인다는 것만 인쇄.
- **곱의 자리**: 이 편에서는 곱이 **연결(θ) 한 인자로 줄었다** — `ε`(SE 분율)과 λ 가 θ 를 정하고, τ · κ 는 결과에 들어가지 않는다. 논의의 "a smaller percolation channel width and an increased number of particle/grain boundaries that may increase the impedance within the SE network" 가 τ · κ 쪽 이야기이고 계산 0.
- ⇒ 처방에 붙는 것(`[해석]`): 24호가 이 편을 "τ↑ 논거의 원전" 으로 매단 자리는 **연결(θ)과 굴곡도(τ)를 한 이름으로 묶은 것**이다 — 같은 λ 손잡이가 둘을 함께 움직이지만(작은 SE → 연결 ↑ · 입계 ↑ · 채널 폭 ↓) 이 편이 계산한 것은 연결뿐이다. "굴곡도 진화" 를 옮길 때 그 출처가 τ 를 인쇄했는지 먼저 본다.

## ★★ 열두 번째 표본 — 측정 κ(차단 셀 두 종 · AC · DC)와 모형 κ(GeoDict)가 한 편에: 규약은 57 · 73호와 같고 같은 70 : 30 wt% 에서 73호와 같은 크기 — 그러나 모형 입력 PSD 는 측정이 아니고 상 분율 표기가 뒤바뀌었다 (2026-09-29, `assb` 82호)

`raw/papers/schlautmann2023_lpscl-particle-size-distribution-composite-transport.md` (Schlautmann · … · Bielefeld · Zeier 2023, *Adv. Energy Mater.* 13, 2302309 — 시판 Li₆PS₅Cl 네 입도 × NCM811 70 : 30 · 무탄소 · 차단 대칭 셀 + GeoDict).

- **정의 · 규약**: `[인쇄]` "κ = volume fraction · bulk conductivity / effective conductivity" — 이 페이지의 `τ²`(굴곡도 인자) · 27 · 29호의 `τ` 와 같은 양. `[재현]` ST4 κ_sim 8/8 · S15 관측 κ 8/8 이 `ε_SE = 0.48(1 − void)` · `ε_CAM = 0.52(1 − void)`(전체 부피 기준 — 57 · 73호 규약)로 ±0.4 % 안. ⚠ ST1 의 48/52 vol% 는 같은 행 밀도로 `[재현]` 52.3/47.7 — **뒤바뀐 분율 위의 κ**(밀도 분율이면 κ_ion ×1.089 · κ_el ×0.918).
- **측정**: 이온 차단(steel) · 전자 차단(In/LiIn \| SE) 대칭 셀 · T형 TLM(73호와 같은 회로) + DC 분극 · 셀 셋(DC 이온 둘). κ_ion 관측 **3.57 · 4.35 · 5.43 · 4.85**(S → XL) · κ_el 관측 **7.72 · 8.62 · 6.83 · 5.04** · DC/AC −21.6 … +26.3 %.
- **`[재현]` 같은 정의 · 같은 조성 대조**: 73호 42 vol% 점(= 70 : 30 wt% · NCM622 · void 14 % 가정) `τ²_ion` 4.27 · `τ²_el` 7.40 ↔ 이 편 3.57–5.43 · 5.04–8.62 — **같은 크기**. 등가 Bruggeman 지수(이온) **2.44–2.73**(ST1 분율 · 밀도 분율 2.70–3.00) — 37호의 가정 3.67 은 이 `ε` 에서 κ 10.7–14.9(×3).
- **모형 ↔ 측정**: κ_sim 이온 4.70 · 6.65 · 8.56 · 7.50 — 측정의 ×1.3–1.6(모의 σ 가 측정의 0.63–0.76) · 전자 3.04 · 2.89 · 3.35 · 4.75 — 측정의 ×0.34–0.94. ⚠ 모형 입력 PSD 는 측정 PSD 가 아니다(S17b — span 을 µm 표준편차로 넣은 거의 단분산 · fines 0 — 82호 D4) · S15b 의 모의 κ_el 은 이온 모의 값 복제(D5).
- **곱의 자리**: SE 입도 한 손잡이가 `ε`(공극 14.1 → 24.3 %)와 κ 를 **같이** 움직인다 — σ_ion,eff 변화 ×1.54(AC) 중 `ε` 몫 `[재현]` ×1.13(0.4123/0.3634) · κ 몫 ×1.36. 전자 쪽은 σ_eff 가 거꾸로 간다(×0.74 AC · ×1.03 DC).
- ⇒ 처방에 붙는 것(`[해석]`): 같은 편에서 측정 κ 와 모형 κ 가 어긋나면(이온 모형이 ×1.3–1.6 더 굴곡) **모형 입력이 측정인지부터** 본다 — 82호의 격차는 입력 PSD(단분산 큰 SE · fines 0)와 뒤바뀐 분율 표기 위에 있어, 모형 오차로도 미세구조 기구로도 읽을 수 없다.

## ★ 25호가 SI ref 3 으로 가리킨 "굴곡도 후처리 원전" — 굴곡도 0, `σ_eff` 0 (2026-09-29, `assb` 83호)

`raw/papers/jiao2023_electro-chemo-mechanical-se-modulus-conductivity-intergranular-czm.md` (Jiao · … · Liu Y. 2023, *Energy Storage Mater.* 61, 102864 — 순수 모형: 3D 복합 양극(COMSOL) + 2D 입계 CZM). 25호 digest 후속 표가 이 편을 "DEM 입자 데이터 → 연결성 · 굴곡도 후처리 방법 원전" 으로 매달았는데, 지면에 **굴곡도가 없다** — `tortuos` 0 · `path` 0 · Bruggeman 0 · `σ_eff` 계산 0. SE 는 3D 형상 안에서 이원 농축 용액 수송(`[도표]` 초기 ≈1 mol L⁻¹ · t_Li+ · D_SE 미인쇄)으로 풀렸고, 수송 결론은 σ 스윕의 농도 CoV · 정규화 용량 · 중간 전압으로만 나온다(굴곡도 인자로 요약되지 않음). ⇒ 이 페이지 25호 절의 "기하 τ(경로 길이비)" 는 **원전이 아직 없다** — 25호 SI 의 ref 3 문장을 원문으로 다시 봐야 한다(83호 G1). 수치 표본이 아니므로 표본 번호를 매기지 않는다.

## ★★ 열세 번째 표본 — 굴곡도 낱말 9 · 값 0: "계층형 SE → 낮은 굴곡도" 의 원전(25호 ref 16)은 EIS 두 호의 순서에 붙인 이름표이고, 저자 정의의 "연결 전해질 망" 저항(R1)은 논의되지 않았다 (2026-09-29, `assb` 85호)

`raw/papers/wang2024_fast-kinetics-hierarchical-catholyte-anode-design-ssb.md` (Wang Y. · Li X. 2024, *Adv. Mater.* 36, 2309306 — 단결정 NMC83 70 : LPSCl1.5 30 wt% 무탄소 · SE 세 판(≈20 µm · ≈300 nm–4 µm · 혼합) · Si–Cl\|G\|Li · 50 MPa · 1차 측정).

- **정의 · 규약**: 없다 — `tortuos` 9 회(서론 2 · 모식 2 · §2.2 3 · CNF 2) · τ · τ² · Bruggeman · σ_eff · 두께 · 면적 **0**. "low/high tortuosity" 는 큰/작은 SE 판의 이름표.
- **근거의 실체**: `[인쇄]` "R2 is decided by the Li ion conduction in the catholyte network; while, R3 is decided by the cathode–electrolyte interface contact" — large ↔ small 두 구성에서 R2 · R3 순서가 뒤집힌다는 것(표 S1 · Ω · 면적 미인쇄) + 그림 1c 모식. 적합 특성 주파수 `[재현]` R2 1.9–3.9 kHz · R3 136–462 Hz(본문 "10 kHz · 500 Hz" 는 데이터 점 라벨).
- **R1 의 침묵**: 저자 정의 R1 = "connected electrolyte network including separator layers, catholyte, and anolyte" — `[도표]` small-only **68** ↔ large 37 ↔ mixed 27 Ω(25 °C · ±3) · −5 °C ≈360 ↔ ≈150 ↔ ≈130. 차(+31 Ω)가 R2 차(+29 Ω)와 같은 크기인데 본문에 R1 값 · 비교 0(`R1` 1 회 = 정의). 분리막이 같다면(가정) 굴곡도가 있을 자리는 여기다.
- **25호 귀속**: 25호 :104 `[인쇄]` "계층형 SE(≈300 nm–4 µm + ≈20 µm) → 낮은 굴곡도(ref 16)" — 전사 ✅ 정확 · 이 편에 굴곡도 양 0 → 25호의 기하 τ(DEM 경로 길이비 1.21 ↔ 1.84)와 정의 공유 0 · 25호 :481 자기 판정("σ_eff 를 한 번도 재지 않았다")과 같은 자리 — **계보 두 편 연속 측정 없는 명제**. 혼합비(20 : 10)는 그림 1b ↔ 실험 절이 반대(85호 D3).
- **옴 강하 크기 검사(82호식)**: 면적 미인쇄 → Ω·cm² 불가 · 비만 — 총 EIS 저항 중 (R1+R2) 몫 large 41 · small 78 · mixed/Si–Cl 52 · mixed/Si–G 51 % · `[재현]` 5 C 분극(그림 3b 왕복 ≈0.7 V − 0.3 C 0.15 V)에서 A·R_dc ≈22 Ω·cm².
- ⇒ 처방에 붙는 것(`[해석]`): "저 굴곡도" 를 인용하는 편을 만나면 ① 굴곡도 양(τ · τ² · σ_eff)이 인쇄됐는지 ② 아니면 어느 회로 호의 순서인지 ③ 그 회로에 "망" 저항 자리(R1)가 따로 있고 그 값이 어떻게 움직였는지를 적는다 — 85호는 ① 0 ② R2 ③ R1 이 R2 만큼 움직였는데 미논의.

## 이 페이지가 주장하지 않는 것

- **"굴곡도가 진화하지 않았다" 고 하지 않는다** — `σ_eff` 로 보면 70 % 는 변화 없음, 80 % 는 ≈3 배이고, 그 3 배의 배정이 안 갈린다는 것까지다.
- **D1(ε 규약)을 저자의 의도된 다른 정의로 볼 가능성을 배제하지 않는다** — 다만 본문 식 (3)의 `ε_i`(재료 i)와 모순된다.
- **옴 강하 추정을 측정값으로 쓰지 않는다** — OCP 기울기는 우리 가정이고 1차원 균일 반응 근사다.
- 근거 편수: **수송 곱을 숫자로 준 편은 24호 하나**다. 9호는 같은 식을 모델에 두고 값을 적합했을 뿐 `σ_eff` 를 재지 않았다. 1호는 이 항을 뺐다.
- ★ **2026-09-23 (55호)**: 위 "근거 편수" 줄은 24호 시점의 기록이다 — 그 뒤 29호(측정 ÷ 공칭 `ε`) · 54호(구조 계산) · 55호(두 경로)가 수를 줬다. 55호 EIS 쪽 `ε` ≈0.65 는 **우리 역산**이고 저자 값이 아니다.
- ★ **2026-09-28 (73호)**: 규약 재현(이온 φ_SE · 전자 φ_CAM)은 **래스터 판독값 위의 우리 산술**이다(9/9 ≤3 %) — 저자가 φ 를 표로 인쇄한 것은 아니다(SI Table SII 미수령). `R_el` 의 ≈76 % 가 접촉 몫이라는 것도 한 조성 · 한 스펙트럼 · 고주파 절편 폐합 가정 위의 `[재현]` 이고, σ_el,0 10 mS cm⁻¹ 이 공극 보정값이라고 단정하지 않는다.
- ★ **2026-09-28 (75호)**: **DNS τ ↔ 73호 τ² 비(×1.9–5.9)를 같은 계의 모형 오차로 쓰지 않는다** — 입도 · 공극 · SE 가 다르다(방향 대조). 이 편의 τ 는 Fig. S1 래스터 판독 위의 우리 역산(표 S1 밀도 · 공극 5 %)이다 — 저자는 τ 를 표로 인쇄하지 않았다(Fig. 2a 색 지도뿐).
- ★ **2026-09-29 (76호)**: **S1 ↔ S2 중 어느 단위가 틀렸는지 확정하지 않는다** — S1 ≈ (0.86–0.97)/R_ion 은 별표 픽셀 판독 · 교점 공식 가정 위의 `[재현]` 이다. 모형 ↔ 측정 κ_eff ×5–9.5 도 밀도 가정 ε 와 2D 영상 ε_SE 위의 산술이고, 모형 τ 의 정의식은 미인쇄다.
- ★ **2026-09-29 (77호)**: **24호의 "굴곡도 진화" 가 틀렸다고 하지 않는다** — 원전 자리(이 편)에 τ 가 인쇄되지 않았다는 것까지이고, 24호 자신의 σ_eff 대조(24호 digest §4-2d)는 이 편과 무관하다.
- ★ **2026-09-29 (82호)**: **82호 κ 와 73호 `τ²` 의 "같은 크기" 를 같은 계의 재현으로 쓰지 않는다** — NCM622 ↔ 811 · SE 입도 · 공극(가정 14 % ↔ 밀도 14.1–24.3 %)이 다르다. 규약 재현(8/8)은 인쇄 분율(뒤바뀐 48/52) 위의 우리 산술이고, 등가 Bruggeman 지수도 같은 산술이다.
- ★ **2026-09-29 (83호)**: **25호의 기하 τ(1.21 ↔ 1.84)가 틀렸다고 하지 않는다** — 25호가 가리킨 원전(83호) 지면에 경로 계산이 없다는 것까지이고, 25호 SI 문장은 다시 보지 못했다.
- ★ **2026-09-29 (85호)**: **85호 R1 차(+31 Ω)를 굴곡도로 배정하지 않는다** — 분리막 · 음극 동일성이 가정이고 면적이 없다; "저 굴곡도" 주장이 틀렸다고도 하지 않는다 — 양이 인쇄되지 않았다는 것까지다.

## 관련

- [[assb-lampe-contact-product-degeneracy]] — 동역학 곱(`A_eff·ε_p/R_s`)과 처방 표. 이 페이지는 그 ③ 채널(수송)의 본체. 24호가 **여덟 번째 적용**.
- [[assb-apparent-capacity-decomposition]] — `θ`·`η(i)` 에 더해 **`η(z)`** (깊이 방향 이용 지연)가 들어오는 자리.
- [[composite-cathode-percolation-utilization]] — 1호 `θ` 는 연결 여부만 본다; 연결된 경로의 폭은 이 페이지.
- [[assb-interphase-vs-contact-loss-attribution]] — 두 비-LAM 기구에 **세 번째 이름("굴곡도 진화")** 이 붙는 자리.
- [[assb-contact-loss-vs-lampe]] — 닻.
- [[near-optimal-set-width-measurement]] — `(ε, a)` 평면의 평탄 계곡을 잴 기계.
