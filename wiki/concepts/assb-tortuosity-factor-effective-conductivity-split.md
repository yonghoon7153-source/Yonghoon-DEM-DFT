---
title: "ASSB 복합양극의 굴곡도 인자 — 측정되는 것은 σ_eff 하나이고 ε·τ² 분할은 가정이 정한다"
description: "In ASSB composite cathodes the tortuosity factor tau^2 = eps x sigma_bulk / sigma_eff is not measured but obtained by dividing a measured effective conductivity by an assumed phase fraction; the only operando-plus-EIS paper in the lineage shows the same measured conductivities giving opposite tau^2 trends under two eps conventions, reads the mismatch between its EIS and model-fitted values as tortuosity evolution, and by its own definition places point-contact loss inside tau^2"
created: 2026-09-23
updated: 2026-09-23
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/bielefeld2020_effective-ionic-conductivity-binder-composite-cathode.md, raw/papers/hlushkou2018_void-space-ion-transport-composite-cathode.md, raw/papers/neumann2021_garnet-3d-structure-grain-boundary-transport.md, raw/papers/stavola2023_lithiation-gradients-tortuosity-thick-nmc111-argyrodite.md, raw/papers/yanev2024_resistive-diffusive-limitations-thiophosphate-composite-cathode.md, raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md, raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md, raw/papers/strauss2018_cathode-particle-size-inactive-fraction-assb.md, raw/papers/zhou2025_tailored-cathode-microstructure-low-pressure-assb.md, raw/papers/sinzig2024_p2d-validity-ssb-global-sensitivity.md]
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

## 이 페이지가 주장하지 않는 것

- **"굴곡도가 진화하지 않았다" 고 하지 않는다** — `σ_eff` 로 보면 70 % 는 변화 없음, 80 % 는 ≈3 배이고, 그 3 배의 배정이 안 갈린다는 것까지다.
- **D1(ε 규약)을 저자의 의도된 다른 정의로 볼 가능성을 배제하지 않는다** — 다만 본문 식 (3)의 `ε_i`(재료 i)와 모순된다.
- **옴 강하 추정을 측정값으로 쓰지 않는다** — OCP 기울기는 우리 가정이고 1차원 균일 반응 근사다.
- 근거 편수: **수송 곱을 숫자로 준 편은 24호 하나**다. 9호는 같은 식을 모델에 두고 값을 적합했을 뿐 `σ_eff` 를 재지 않았다. 1호는 이 항을 뺐다.
- ★ **2026-09-23 (55호)**: 위 "근거 편수" 줄은 24호 시점의 기록이다 — 그 뒤 29호(측정 ÷ 공칭 `ε`) · 54호(구조 계산) · 55호(두 경로)가 수를 줬다. 55호 EIS 쪽 `ε` ≈0.65 는 **우리 역산**이고 저자 값이 아니다.

## 관련

- [[assb-lampe-contact-product-degeneracy]] — 동역학 곱(`A_eff·ε_p/R_s`)과 처방 표. 이 페이지는 그 ③ 채널(수송)의 본체. 24호가 **여덟 번째 적용**.
- [[assb-apparent-capacity-decomposition]] — `θ`·`η(i)` 에 더해 **`η(z)`** (깊이 방향 이용 지연)가 들어오는 자리.
- [[composite-cathode-percolation-utilization]] — 1호 `θ` 는 연결 여부만 본다; 연결된 경로의 폭은 이 페이지.
- [[assb-interphase-vs-contact-loss-attribution]] — 두 비-LAM 기구에 **세 번째 이름("굴곡도 진화")** 이 붙는 자리.
- [[assb-contact-loss-vs-lampe]] — 닻.
- [[near-optimal-set-width-measurement]] — `(ε, a)` 평면의 평탄 계곡을 잴 기계.
