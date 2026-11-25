<!-- digest 표준 양식 (paper-level STANDALONE). 이 파일이 깊이 기준 문서다.
     2026-09-11 전면 재작성: ① 크로핑 그림 12장을 **실제로 보고** figure-read 값 삽입,
     ② elements/methods 태그 수정(이 논문은 DFT 를 하지 않는다), ③ 전압기준 +0.62→+0.6 V 정정
     (논문 자신이 쓰는 환산), ④ Fig. 4 를 "100 사이클 후"로 잘못 적었던 것 → **3.7 V 60 h 홀드 후**로 정정,
     ⑤ 1저자 지정 읽기축(comp1 vs modelc 산화안정성) 기준으로 §7 재작성. -->

# Impact of the Chlorination of Lithium Argyrodites on the Electrolyte/Cathode Interface in Solid-State Batteries — Zuo et al. (*Angew. Chem. Int. Ed.* **2023**, 62, e202213228)

> slug `zuo2022_chlorination_cathode_interface` · DOI `10.1002/anie.202213228` (독일판 `10.1002/ange.202213228`) · type `exp 전용 (원자단위 계산 0 — 이론은 분해 반응식 3줄이 전부)` · PDF `litdb/inbox/105. Impact_of_the_Chlorination…pdf` (본문 8 pp) + `105. Sup) …pdf` (SI 11 pp, Fig S1–S12 · Table S1) · digested `2026-06-23` · **재작성 `2026-09-11`** (그림 실독 + 축 B 재정렬) · status ✅ · 태그 **[외부]**

> elements: Li, P, S, Cl, O, Ni, Co, Mn, In, C
> methods: ESW

> **저자**: Tong-Tong Zuo\*, Felix Walther, Jun Hao Teo, Raffael Rueß, Yubo Wang, Marcus Rohnke, Daniel Schröder, **Linda F. Nazar**, **Jürgen Janek\*** (JLU Giessen 물리화학·ZfM/LaMa · KIT INT · TU Braunschweig InES · **Univ. Waterloo**) · 투고 2022-09-07 · accepted 2022-11-23 · VoR 2023-01-10 · **OA CC BY-NC-ND** · BMBF FestBatt(03XP0177A/03XP0430A) + InCa/InCa2(BMBF–NEDO 독일–일본) + NSERC Canada Research Chair
>
> **계보**: [Adeli] 2019 Angew(같은 Nazar 그룹, Li₆₋ₓPS₅₋ₓCl₁₊ₓ 고용체 원전·이 논문 합성법 ref[1]) → **본 논문**(그 물질의 *양극 계면* 대가를 처음 물음) → [Qian25](LiPO₂F₂ CAM 코팅) → [Qian26](데칸산 SE 코팅). Waterloo/Nazar × Giessen/Janek 합작 라인의 2번째.

---

## 0. 이 digest 를 읽는 법 — 1저자 지정 읽기축

이 논문은 **우리 comp1(Li₆PS₅Cl)과 modelc(Li₅.₅PS₄.₅Cl₁.₅ ≈ LPSCl1.6 계열)를 정확히 그 두 조성으로 실험 비교한 유일한 대조군**이다. 우리가 grand-potential 로만 다뤄 온 **축 B(산화)** 에 실험 데이터를 대는 것이 이 digest 의 목적이다.

논문의 핵심은 **역설**이다 — *"Cl 을 더 넣으면 산화 분해는 더 심한데 셀 성능은 왜 더 좋아지나?"*
답: **분해의 "양"과 분해 산물의 "질"은 별개 축**이다. Cl-rich 는 더 많이 분해되지만, 고전압에서 NCM 격자산소와 만났을 때 **저항성 고체 산화물(phosphate)을 덜 만들고 기체(SO₂)·폴리설파이드로 더 빠진다** → 계면 저항 증가가 느리다.

> ⚠⚠ **전압 기준 — 이 논문은 +0.6 V 를 쓴다.**
> SI 가 세 군데서 명시한다: `3.7 V vs In/InLi = **4.3 V** vs Li⁺/Li` · `3.9 V vs In/InLi = **4.5 V**` · `2.0–3.9 V vs In/InLi = **2.6–4.5 V**`.
> 따라서 **환산은 +0.6 V**다 (In/InLi 평탄부의 통상값 0.62 V 가 아니라 논문 자신의 반올림).
> 본문의 "≥4.2 V" · ">4.2 V" 는 **Li⁺/Li 기준**, CV·GITT·EIS·DEMS 축은 전부 **In/InLi 기준**이다. 섞으면 0.6 V 가 통째로 날아간다.
> 🔑 **이 환산이 §7 의 핵심 논점을 만든다**: CV 창의 하한 2.0 V vs In/InLi = **2.6 V vs Li⁺/Li** 이고, 우리 계산 산화 onset 2.256 V vs Li⁺/Li = **1.656 V vs In/InLi** — 즉 **우리 onset 은 이 논문의 측정창 아래 0.34 V 지점에 있어서 CV 로는 원리적으로 볼 수 없다.**

> **본 digest 에서 실제로 본 그림 (2026-09-11)**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` `Fig. 6` `Fig. 7` `Fig. S1` `Fig. S2` `Fig. S3` `Fig. S4` `Fig. S11` — **12장**.
> 안 본 것: `Fig. S5` `Fig. S6`(EIS 피팅 결과) · `Fig. S7` `Fig. S8`(rate, 값은 `Table S1` 로 확보) · `Fig. S9`(SEM) · `Fig. S10`(폴리설파이드 박스플롯) · `Fig. S12`(CO₂/H₂) · `Table S1`(표는 PDF 텍스트가 정확).
> 그림에서만 읽은 값은 **`figure-read ≈`** 로 표시했다.

---

## 1. 한 줄 요약

Cl-rich(Li₅.₅PS₄.₅Cl₁.₅)는 LPSCl 보다 **더 쉽게·더 많이 전기화학 분해**되지만(CV 전류 `figure-read ≈`1.5×·GITT 3 V 이하 용량 1.45×·ToF-SIMS S⁻ 10.4 vs 6.7배·DSC/TGA 열역학 열세), NCM85 와 만나는 **고전압 산소관여 경로에서는 고체 phosphate 를 40 % 덜 만들고 SO₂ 기체로 더 빠져서** — 3.7 V 정전압 홀드 중 계면저항 증가율이 **8.9 < 13.2 Ω·h⁻⁰·⁵** 이고 50 사이클 방전용량이 **145 > 133 mAh/g** 이다.

⚠ 단 이 "Cl-rich 승" 은 **정전압 홀드(화학 열화 지배) 조건에서만** 성립한다 — 갈바노 사이클링(`Fig. 3d,e`)과 C/20·45 °C DEMS 셀(`Fig. 6`)에서는 우위가 사라지거나 뒤집힌다(§5.11·§10).

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 비교 쌍 | **Li₆PS₅Cl (Cl 1.0)** vs **Li₅.₅PS₄.₅Cl₁.₅ (Cl 1.5)** — "주요 구조변화 없이 할라이드 함량만 바꾼 모델계" |
| 양극 | **NCM851005 (NCM85, BASF SE)** = LiNi₀.₈₅Co₀.₁₀Mn₀.₀₅O₂ · H2–H3 전이에서 격자 O 를 내놓는 고-Ni 층상 |
| 던지는 질문 | halogenation 이 (a) SE **자체의 전기화학 분해**, (b) **CAM 계면의 화학 분해** 를 각각 어떻게 바꾸나 |
| 문헌 갭 | Kraft(2017)·Gautam(2021)·Adeli(2019)가 halide 로 σ 를 올리는 데까지는 갔는데, **그 대가(계면 안정성)는 미지** |
| 선행 축 (Dewald 2019 · Tan 2019) | LPSCl 산화 = **티오인산 폴리음이온의 S²⁻ → Sₓ⁰/Sₓ²⁻ 산화**(= Li 탈리)가 지배. CAM 접촉 시 **oxygenated S/P** 가 추가로 생김(Walther 2019) |
| 선행 축 (Strauss 2020 · Jung 2017/2018) | NCM 이 고SOC 에서 내놓는 O₂(아마 singlet ¹O₂)가 SE 와 반응해 **SO₂** |

---

## 3. 핵심 수치 총정리 ★

> 기준 전극을 **매 행에 명시**한다. `figure-read` = 그림에서 읽은 값(본문 미명시).

### 3a. 물질·수송

| 물성 | Li₆PS₅Cl | Li₅.₅PS₄.₅Cl₁.₅ | 조건/출처 |
|---|---|---|---|
| σ (25 °C) | **2.9 mS cm⁻¹** | **7.0 mS cm⁻¹** (2.4×) | 본문 p.2. intro 는 소결 시 **12 mS cm⁻¹** 인용([Adeli]) |
| XRD 2차상 | 없음 | **LiCl** (2θ ≈ 35°, 50°) | `Fig. S1`. `figure-read ≈` 최강선(30°) 대비 **≲2 %** — 아주 약함 |
| 합성 | Li₂S+P₂S₅+LiCl, 볼밀 380 rpm 17 h → 펠렛 → **550 °C 10 h 진공 봉입관** | 동일(단 `Fig. S3` DSC 용 상순수 시료는 **480 °C** 로 낮춰 LiCl 석출 회피) | SI p.2 |

### 3b. 전기화학 분해 (SE/C 전극 — CAM 없음, 순수 산화축)

| 물성 | Li₆PS₅Cl | Li₅.₅PS₄.₅Cl₁.₅ | 조건/출처 |
|---|---|---|---|
| CV 산화 피크 전류밀도 | `figure-read ≈` **32 nA cm⁻²** @ ≈2.85 V | `figure-read ≈` **47 nA cm⁻²** @ ≈2.75 V | `Fig. 1a,b`·`Fig. S2`. **vs In/InLi**. 0.05 mV s⁻¹, C65 20 wt% |
| 본문이 주장한 전류비 | 1× | **"approximately twofold"** | ⚠ `figure-read` 피크비는 **≈1.5×** — 2× 는 2.0–2.2 V 구간에서만(§10-①) |
| 피크 전위 | \_ | **동일** | `Fig. S2` 겹침 → **메커니즘 같다** (논문 주장) |
| 산화 개시(apparent) | `figure-read ≈` 2.05–2.1 V | `figure-read ≈` 1.95–2.0 V | `Fig. S2`, **vs In/InLi**. ⚠ 스캔 하한이 2.0 V라 **두 시료 모두 창 시작점에서 이미 산화 중** |
| 전류 정규화 기준 | \_ | \_ | C65 BET **59 m² g⁻¹** → 전극 표면적 **1180 cm²** 가정 ⇒ **1 µA ↔ 8.5×10⁻⁴ µA cm⁻²** (`Fig. S2` 캡션). *우리 산수*: 47 nA cm⁻² ≈ **55 µA**, 32 nA cm⁻² ≈ **38 µA** |
| 완전 산화 전자수 | **5 e⁻/f.u.** | **4 e⁻/f.u.** | 반응식 (1)+(3) / (2)+(3) |
| GITT 총 분해용량 (→3.9 V vs In/InLi) | `figure-read ≈` **305 µAh** | `figure-read ≈` **358 µAh** | `Fig. S4a`. 5 µA 1 h 분극 + 1 h 이완 반복 |
| ┗ 3 V vs In/InLi **이하** | `figure-read ≈` **112 µAh** | `figure-read ≈` **163 µAh** (**1.45×**) | `Fig. S4a` 점선. 저전압에서 Cl-rich 가 더 분해 |
| ┗ 3 V vs In/InLi **이상** | `figure-read ≈` **193 µAh** | `figure-read ≈` **195 µAh** (**동일**) | 본문 "similar decomposition capacity" 와 정확히 일치 |
| GITT IR drop @3.9 V vs In/InLi | `figure-read ≈` **0.53 V** | `figure-read ≈` **0.71 V** (1.34×) | `Fig. S4b`. 3.0 V 에서 교차 — **그 아래선 Cl-rich 가 오히려 낮다**(σ 우위) |
| *우리 산수* — 분해 심도 | ≈**38 mAh g⁻¹_SE** = 이론 499 의 **7.6 %** | ≈**45 mAh g⁻¹_SE** = 이론 402 의 **11.1 %** | 전극 10 mg 중 SE 8 mg(C:SE=2:8) 가정, 5 e⁻/4 e⁻ 완전분해 기준. **전체 SE 의 10 % 남짓만 분해** |

### 3c. ToF-SIMS — SE/C 전극 표면 (3.7 V vs In/InLi 60 h 홀드 후, `Fig. 1c,d`)

| fragment | Li₆PS₅Cl pristine → aged | Li₅.₅PS₄.₅Cl₁.₅ pristine → aged | 배수 |
|---|---|---|---|
| **S⁻** (I_S/I_total) | 484 → **3266** | 339 → **3535** | **6.7×** vs **10.4×** |
| **Cl⁻** (I_Cl/I_total) | 771 → **3935** | 947 → **6314** | **5.1×** vs **6.7×** |

### 3d. ToF-SIMS — SE/NCM85 복합양극 표면 (**3.7 V vs In/InLi 60 h 홀드 후**, `Fig. 4`) ★

> ⚠ **`Fig. 4` 는 "100 사이클 후"가 아니라 60 h 정전압 홀드 후다** (캡션·본문 확인). 100 사이클 후는 `Fig. 5`·`Fig. S11`.
> (a),(b) 는 **I_total 정규화**, (c),(d) 는 **I_NiO₂⁻ 정규화** — 정규화 기준이 다르다(NCM 2차입자 표면에서만 산소관여 분해가 일어난다는 가정).

| fragment | LPSCl before → after | Cl1.5 before → after | 판정 |
|---|---|---|---|
| **S⁻** | `fr≈` 0.20 → **1.6 ×10³** | `fr≈` 0.25 → **3.0 ×10³** | Cl-rich **1.9×** 더 많음 (분해 많음) |
| **Cl⁻** | `fr≈` 0.62 → **2.1 ×10³** | `fr≈` 0.63 → **3.55 ×10³** | Cl-rich **1.7×** |
| **PO₃⁻** (phosphate) | `fr≈` 2.2 → **8.1 ×10⁵** | `fr≈` 2.3 → **4.0 ×10⁵** | **LPSCl 이 2.0× 더 많음** ← 반전 핵심. pristine 이 2.2 vs 2.3 으로 **맞춰져 있어 비교가 깨끗** |
| **SO₃⁻** (sulfate/sulfite) | `fr≈` 1.1 → **3.55 ×10⁵** | `fr≈` 0.37 → **0.75 ×10⁵** | LPSCl 4.7× 더 많음. ⚠ **pristine 이 이미 3× 차이**(1.1 vs 0.37) — 배수로 보면 3.2× vs 2.0× 로 격차가 확 줄어든다(§10-③) |

> 🔑 **pristine Cl⁻ 이 두 시료에서 같다**(0.62 vs 0.63 ×10³) — Cl 이 50 % 더 많은데도. ToF-SIMS 2차이온 수율은 매트릭스 의존이라 **절대 정량이 아님**을 스스로 보여주는 자료. 배수(fold)로만 읽어야 한다.

### 3e. ToF-SIMS ROI 반정량 (**100 사이클 후**, 45° FIB crater 측벽, `Fig. S11`) ★

| 신호 | Li₆PS₅Cl | Li₅.₅PS₄.₅Cl₁.₅ | 비 |
|---|---|---|---|
| **(S₄⁻+S₅⁻+S₆⁻)** 폴리설파이드 | **9.1×10⁻³** | **1.3×10⁻²** | Cl-rich **+43 %** |
| **(PO₂⁻·PO₃⁻)** phosphate | **7.2×10⁻³** | **4.3×10⁻³** | Cl-rich **−40 %** |
| **(SO₂⁻·SO₃⁻)** sulfate/sulfite | **4.7×10⁻⁴** | **4.8×10⁻⁴** | **차이 없음 (+2 %)** |

> 🔑🔑 **장기 사이클 후에는 "산화된 S 가 적다"가 성립하지 않는다.** 견고한 것은 **phosphate −40 %** 와 **폴리설파이드 +43 %** 뿐이다. 논문 자신도 SOₓ 동일에 대해 "부분 가역 산화환원 + 질량간섭 + 낮은 신호세기" 로 변명한다. **초록의 "less solid oxygenated phosphorous *and sulfur* species" 중 sulfur 는 60 h 홀드(`Fig. 4d`)에서만이고 100 사이클(`Fig. S11c`)에선 무효** — 인용할 때 조건을 붙여야 한다.

### 3f. 계면 저항 — EIS + TLM (3.7 V vs In/InLi 정전압 홀드 30 h, `Fig. 2`)

| 항목 | Li₆PS₅Cl | Li₅.₅PS₄.₅Cl₁.₅ |
|---|---|---|
| **R_cat 증가율 (√t)** | **13.2 Ω h⁻⁰·⁵** | **8.9 Ω h⁻⁰·⁵** (0.67×) |
| R_cat 초기 (`figure-read`, t⁰·⁵≈1) | ≈ **36 Ω** | ≈ **19 Ω** |
| R_cat 최종 (`figure-read`, t⁰·⁵≈4.3 = 18.5 h) | ≈ **83 Ω** | ≈ **52 Ω** |
| Nyquist 특성 주파수 표시 | **~550 Hz** | **~550 Hz** (동일) |
| 정의 | **R_cat = √(R_ct(R_el + R_ion))** (식 4, Moškon 2020) — Gerischer 거동이라 **R_ct 와 수송을 분리 못 함(논문 자인)** | |

> ⚠⚠ **이 표가 이 논문에서 제일 조심할 자리다.** R_cat 은 Ω 단위 **절대 저항**이고 정의상 **R_ion 을 품고 있다**. Cl-rich 는 σ 가 2.4× 높아 R_ion 이 그만큼 작다. R_ct 만 시간에 선형으로 자란다고 보면 기울기 = √(k_ct·(R_el+R_ion)) 이므로 **기울기 비 1.48× 는 (R_el+R_ion) 비의 제곱근만으로도 상당 부분 설명된다** — 즉 "Cl-rich 계면 화학이 더 착하다" 가 아니라 **"Cl-rich 복합체가 이온적으로 덜 막힌다"** 일 수 있다(§10-②).

### 3g. 셀 성능

| 항목 | Li₆PS₅Cl | Li₅.₅PS₄.₅Cl₁.₅ | 조건 |
|---|---|---|---|
| 1st 충/방전 | **215 / 165 mAh g⁻¹** (CE **77 %**) | **215 / 170** (CE **79 %**) | `Fig. 3a,b`, 0.5 C = 0.96 mA cm⁻², 25 °C, ~3.7 V vs In/InLi 상한 |
| 50 사이클 | **133** | **145** | `Fig. 3c`. 유지율 *우리 산수* 80.6 % vs 85.3 % |
| 50th 충전 후 총 임피던스 (`figure-read`) | ≈ **135 Ω** | ≈ **132 Ω** (거의 같음) | `Fig. 3d,e` — 본문 "차이 미미" 와 일치 |
| ┗ 1st→50th 증가분 (`figure-read`, 오프셋 뺀 반원폭) | ≈ 32 → **103 Ω** (Δ≈71) | ≈ 22 → **112 Ω** (Δ≈**90**) | ⚠ **사이클링 중에는 Cl-rich 가 오히려 더 자란다** (§5.11) |
| rate (0.1/0.2/0.5/1/2 C) | 183.9 / 164.7 / 132.3 / 95.8 / **45.6** | 199.3 / 184.7 / 159.9 / 131.1 / **85.6** | `Table S1` (동종 분리막·양극 조합) |

**`Table S1` 4-셀 분해 (분리막 × 복합양극 교차, 단위 mAh g⁻¹)**

| 분리막 SE | 복합양극 SE | 0.1 C | 0.2 C | 0.5 C | 1 C | 2 C |
|---|---|---|---|---|---|---|
| LPSCl | LPSCl | 183.9 | 164.7 | 132.3 | 95.8 | 45.6 |
| LPSCl | **Cl1.5** | **201.6** | **180.9** | 136.6 | 89.2 | **36.6** |
| **Cl1.5** | LPSCl | 193.2 | 172.7 | 143.3 | 109.7 | 52.0 |
| **Cl1.5** | **Cl1.5** | 199.3 | 184.7 | **159.9** | **131.1** | **85.6** |

> 판정: **저율(0.1–0.2 C) 병목 = 복합양극** (Cl1.5 양극 두 셀이 위), **고율(1–2 C) 병목 = 분리막 σ** (Cl1.5 분리막 두 셀이 위).
> ⚠ 2 C 에서 `LPSCl 분리막 | Cl1.5 양극` **36.6 < 45.6** — Cl-rich 양극이 LPSCl 분리막과 조합되면 오히려 나쁘다. 논문은 언급 안 함.

### 3h. 기체 (DEMS, `Fig. 6`) ★

| 항목 | Li₆PS₅Cl 셀 | Li₅.₅PS₄.₅Cl₁.₅ 셀 |
|---|---|---|
| 1st 충/방전 | **243 / 201 mAh g⁻¹_NCM** | **239 / 176** |
| *우리 산수* — 1st CE | **82.7 %** | **73.6 %** ⚠ **9 %p 열세** (0.5 C 셀의 79 vs 77 과 방향 반대, §10-④) |
| SOC (O₂ 방출 조건 >80 %) | **84.3 %** | **82.5 %** |
| **O₂ 누적 (m/z 32)** | **6.7 µmol g⁻¹_NCM** | **6.8 µmol g⁻¹_NCM** — **동일** |
| O₂ 방출 속도 피크 (`figure-read`) | ≈ **140 nmol min⁻¹ g⁻¹** | ≈ **133 nmol min⁻¹ g⁻¹** |
| O₂ 방출 개시 전압 표기 (`figure-read`, 그림 주석) | **3.59 V** vs In/InLi (= 4.19 vs Li⁺/Li) | **3.46 V** vs In/InLi (= 4.06) |
| **SO₂ (m/z 64)** 정규화 이온전류 피크 (`figure-read`) | 1st ≈ **0.45** / 2nd ≈ **0.35** a.u. | 1st ≈ **2.55** / 2nd ≈ **2.3** a.u. → **≈5.7×** |
| 그 외 검출 기체 | **H₂ (m/z 2)** = 음극 미량수분 환원 · **CO₂ (m/z 44)** = 저전압 음극 부반응 + 고SOC **NCM 표면 Li₂CO₃ 분해** (복합양극에 카본 없음 → 탄소 산화 배제) | `Fig. S12` |

> 🔑 **"gas diversion"**: **같은 양의 O₂ (6.7 ≈ 6.8)** 가 나왔는데 **SO₂ 는 Cl-rich 가 5~6배**. 즉 O₂ 의 행선지가 조성에 따라 갈린다 — LPSCl 은 고체 산화물(phosphate)로, Cl-rich 는 기체(SO₂)로.
> ⚠ **단 SO₂ 는 a.u. 다.** SI 는 "측정 후 교정가스로 mol/g 로 환산" 한다고 적었는데 **정작 µmol/g 로 보고된 것은 O₂ 뿐**이다. 5.7× 는 **교정된 몰비가 아니다** — 방향만 인용하고 배수는 `figure-read` 라고 밝혀야 한다.

### 3i. 열적 안정성 (`Fig. S3`)

| 항목 | Li₆PS₅Cl | Li₅.₅PS₄.₅Cl₁.₅ |
|---|---|---|
| DSC 융해 / 결정화 | **535 / 532 °C** (뾰족) | **523 / 493 °C** (넓어지고 하강 → **incongruent melting** 시사) |
| TGA 질량감소 개시 | 유의미한 손실 없음 | **315 °C** |
| TGA 600 °C 잔량 (`figure-read`) | ≈ **95 %** (즉 ~5 % 손실 — "없음"은 과장) | ≈ **81 %** (~**19 %** 손실) |
| 공통 (`figure-read`) | 둘 다 100 °C 부근 ~1–2 % 감소 (이송 중 공기 노출 ≤1 min, SI 명시) | |

---

## 4. 재료 & 방법 — 우리가 같은 축을 흉내 낼 때 필요한 조건 전부 ★

### 4a. 합성
Li₂S(99.98 %) + P₂S₅(99 %) + LiCl(99.98 %) 화학량론 혼합 → 마노 유발 → **ZrO₂ 45 mL 용기, 5 mm 볼, Fritsch P7, 380 rpm 17 h**(10 min 가동 / 10 min 냉각) → 펠렛 성형 → **탄소코팅 석영 앰플**(800 °C 진공 예열로 수분 제거, 시료 ~1 g/앰플) 진공 봉입 → **550 °C 10 h, 승온 5 °C/min** → 유발 분쇄. 전 과정 Ar (O₂·H₂O < 0.1 ppm).
※ `Fig. S3` DSC/TGA 용 **상순수 Cl1.5 만 480 °C 합성** — LiCl 석출을 없애기 위해. 논문 주장: "미량 LiCl 불순물은 *열* 안정성에만 영향, σ 와 전기화학 안정성은 불변".

### 4b. 셀 (핵심 조건)
- **복합양극**: 아르지로다이트 : NCM85 = **3 : 7 질량비**, 유발 손혼합 30 min. **카본 첨가제 없음** (SI 가 CO₂ 논의에서 명시).
- **카본 전극(SE/C)**: C65(Timcal) : 아르지로다이트 = **2 : 8**, 유발 30 min. C65 BET **59 m² g⁻¹**.
- **셀 스택**: PEEK 다이. 분리막 **SE 80 mg** 손압 → 복합양극 **12 mg** 도포 → **3 ton 3 min 일축 압축**. SE/C 셀은 분리막 60 mg + 작동전극 10 mg.
- **음극**: In 박(8 mm ⌀) + Li 박(4 mm ⌀) + Cu 박(10 mm ⌀) → Al 프레임 **~28 MPa 1 h** 평형화 → 측정 중 **~100 MPa** 유지.
- *우리 산수*: 복합양극 12 mg × 0.7 = **8.4 mg NCM85**; 0.5 C = 0.96 mA cm⁻²·1 C=180 mA g⁻¹ 에서 역산하면 면적 ≈0.79 cm²(10 mm ⌀) → **로딩 ≈10.7 mg_NCM cm⁻², ≈2.3 mAh cm⁻²** (다이 지름 가정이 들어감 — 참고값).

### 4c. 전기화학
- **CV**: **2.0–3.7 V vs In/InLi** (= 2.6–4.3 vs Li⁺/Li), **0.05 mV s⁻¹**, 25 °C, 3 사이클. Biologic VMP300.
- **에이징**: 0.1 C 로 **3.7 V vs In/InLi (=4.3 vs Li⁺/Li)** 까지 충전 → **정전압 홀드**, **25 min 간격 EIS 30 h**. EIS **3 MHz–0.1 Hz**, 진폭 **10 mV**, RelaxIS 피팅.
- **사이클링**: 0.5 C(임피던스 추적) / 0.2 C 100 사이클(장기) / rate 0.1–2 C. Maccor.
- **GITT**: **5 µA 1 h 분극 + 1 h 이완** 반복, **3.9 V vs In/InLi (=4.5)** 까지.
- 온도 챔버 25 °C 고정 (DEMS 만 45 °C).

### 4d. ToF-SIMS
- **표면 분석**: IONTOF **Hybrid SIMS M6**, **Bi₃²⁺ 60 keV**, 조리개 1100 µm, cycle 100 µs, **bunched(고질량분해) 모드 FWHM m/Δm > 7000 @ m/z 31.97 (S⁻)**, **음이온 모드**. 저에너지 전자 + Ar 표면 flooding(5×10⁻⁶ mbar)으로 대전 보정. **시료당 서로 다른 10 군데 스펙트럼**, 분석면적 150×150 µm², 256×256 px, **static 조건 유지(1차이온 도즈 10¹² ions cm⁻²)**, 전류 ~0.4 pA.
- **crater 측벽**: TOF.SIMS 5-100. **FIB Ga 30 keV ~19.9 nA** 로 120×80 µm² **45° crater** → 고해상 폴리싱(1024×1024, dwell 70 ms) → 손상층 제거 클리닝 → ROI 125×125 µm² 내 분석(1024×1024 px, 70 frames, **이론 측방분해능 122 nm**, Bi₃⁺ fast imaging, ~0.13–0.14 pA).
- **정규화 규칙(중요)**: 2차이온 이미지는 **총이온신호로 정규화**(FIB crater 지형 보정). `Fig. 4c,d` 만 **NiO₂⁻ 로 정규화**. POₓ·SOₓ 이미지는 **곱셈 정규화**(PO₂⁻·PO₃⁻, SO₂⁻·SO₃⁻)로 질량간섭 억제, 폴리설파이드는 **S₄⁻+S₅⁻+S₆⁻ 합산**으로 신호 증폭. 소프트웨어 Surface Lab 7.1.
- **분석 위치**: 복합전극 중 **집전체를 향한 면**(pellet 바깥면).

### 4e. DEMS
- 셀: 복합양극(SE/NCM85) + SE 분리막 + In/InLi, **PEEK 링** 커스텀. SE 100 mg **~113 MPa** → 복합양극 + **Al 메시(8 mm, 통전+통기)** 얹고 **~440 MPa** 동시 압축. 양극 spacer 에 **1 mm 구멍**(기체 배출).
- 조건: **0.05 C(C/20), 45 °C, 2.0–3.9 V vs In/InLi (= 2.6–4.5 vs Li⁺/Li)**. 시작 전 **10 h OCV**(온도 평형 + MS 배경).
- 캐리어: **He 6.0, 2.5 mL min⁻¹** (Bronkhorst MFC). MS: Pfeiffer **Omnistar GSD 320**. **m/z 1–100** 스캔, 측정 후 **교정가스로 ion current → mol/g 환산**.

### 4f. 기타
DSC(TA Q2000, ~5 mg, Al 밀폐팬, N₂ 50 mL/min, → 550 °C → 40 °C, **20 °C/min**) · TGA(TA Q600, ~20 mg, Pt 도가니, → 600 °C, 20 °C/min, N₂ 40/60 mL/min, **이송 중 공기노출 ≤1 min**) · XRD(PANalytical Empyrean, Cu Kα, Bragg–Brentano, Si 홀더 + Kapton 밀봉, 10–90° step 0.026°) · SEM(Zeiss Merlin 5 kV, Leica EM VCT500 무노출 이송).

### 4g. 이론 (전부)
> **이 논문은 DFT 를 하지 않는다.** 이론은 아래 반응식 3줄이 전부이며, 저자들도 "highly simplified" 라고 명시한다.

```
(1)  Li6PS5Cl        →  LiCl     + Li3PS4 + S      + 2 Li⁺ + 2 e⁻
(2)  Li5.5PS4.5Cl1.5 →  1.5 LiCl + Li3PS4 + 0.5 S  + 1 Li⁺ + 1 e⁻
(3)  Li3PS4          →  0.5 P2S5 + 1.5 S           + 3 Li⁺ + 3 e⁻
```
⇒ 완전 분해 시 **LPSCl 5 e⁻/f.u.**, **Cl1.5 4 e⁻/f.u.**
저자 주석: 실제로는 **PS₄³⁻, P₂S₇⁴⁻, P₂S₆²⁻** 등 중간체가 다수 개입해 훨씬 복잡하다.

🔑 **핵심 비대칭**: Cl-rich 는 **첫 산화 단계에서 전자를 절반만 내놓고(1 vs 2 e⁻)** **불활성 LiCl 을 1.5배 만든다.** 이것이 뒤에 나오는 "산물이 덜 해롭다" 의 화학적 뿌리다.

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 합성·상순도 (`Fig. S1`)
σ 2.9 → 7.0 mS cm⁻¹. `Fig. S1` 을 실제로 보면: 두 패턴 모두 전형적 아르지로다이트(F-43m) 반사열이고, Cl1.5 쪽에만 **2θ ≈ 35°·50° 에 파란 원으로 표시된 LiCl 선**이 있다. `figure-read` 로 그 선의 세기는 **최강선(≈30°) 대비 ≲2 %** — 정말 미량이다. LPSCl 쪽엔 없다.
→ **Cl 고용한계**. [Adeli] 가 x ≤ 0.5(= Cl1.5)를 한계로 잡았는데 **그 한계점에서 이미 LiCl 이 나온다**. **우리 modelc 는 Cl 1.6 = 한계 너머**이므로 2차상 위험이 더 크다(§12-⑦).

### 5.2 CV — 전기화학 분해의 "양" (`Fig. 1a,b`, `Fig. S2`) ★
`Fig. 1a,b` 를 실제로 보면 y축은 **전류밀도 nA cm⁻²** (0–60), x축은 **V vs In/InLi** (≈1.9–3.7).
- LPSCl: 1차 스캔이 2.0 V 근처에서 출발해 **≈2.85 V 에서 ≈32 nA cm⁻²** 피크, 이후 완만히 감소하며 3.65 V 에서 ≈23.
- Cl1.5: **≈2.75 V 에서 ≈47 nA cm⁻²** 피크, 3.4 V 부근에 어깨, 3.65 V 에서 ≈25.
- **두 그림 모두 화살표 방향(1→3 사이클)으로 전류가 거의 0 까지 붕괴한다.** 2·3 사이클은 3.4 V 이상에서만 10 nA cm⁻² 안팎의 작은 고리로 남는다 → **강한 자기부동태화**. (이 대목은 본문이 전혀 논하지 않는다. [Wu26] 의 "self-passivating practical window" 와 같은 현상이다.)

`Fig. S2`(두 곡선 겹침, 1차 스캔)에서 `figure-read`:
| V vs In/InLi | LPSCl | Cl1.5 | 비 |
|---|---|---|---|
| 2.0–2.2 | ≈0.5–2 | ≈5–8 | **≳3×** |
| 2.4 | ≈18 | ≈28 | 1.6× |
| 피크 | ≈32 | ≈47 | **≈1.5×** |
| 3.65 | ≈23 | ≈25 | ≈1.1× |

→ 본문의 **"approximately twofold"** 는 **피크에서 성립하지 않는다**(§10-①). 성립하는 곳은 **개시 근처 저전압**뿐이고, 고전압으로 갈수록 둘이 수렴한다.
→ 피크 전위는 사실상 같고(2.85 vs 2.75, `figure-read` 0.1 V 차) 곡선 모양이 닮았다 ⇒ 논문 결론 **"메커니즘은 같고 양만 다르다"** 는 그림이 지지한다.
→ ⚠ **스캔 하한이 2.0 V vs In/InLi (= 2.6 vs Li⁺/Li)** 라서 두 시료 모두 **창 시작점에서 이미 전류가 흐른다**. 따라서 "Cl-rich 의 onset 이 더 낮다"는 **참 onset 이 아니라 창 경계에서의 전류 크기 차이**다.

### 5.3 분해 반응식이 말하는 것 (반응 1–3)
Cl-rich 는 (a) 첫 산화에 **전자 1개**만(LPSCl 2개), (b) **LiCl 1.5 당량**(LPSCl 1.0), (c) 원소 S 는 **0.5 당량**(LPSCl 1.0)만 만든다. 그래서 논문은 CV 전류가 큰 것을 두 갈래로 해석한다 — **"더 많은 SE 가 분해" 또는 "더 완전히(더 깊은 단계까지) 분해"**. 둘을 구분할 데이터는 제시되지 않는다.

### 5.4 DSC/TGA — 열역학적 준안정성 (`Fig. S3`) ★
`Fig. S3a` 실독: y = Heat Flow (mW/mg, −1.5~1.5), x = 0–600 °C, 위 두 곡선이 냉각·아래 두 곡선이 가열. LPSCl(검정)은 가열 **535 °C·냉각 532 °C 에 뾰족한 단일 피크**. Cl1.5(빨강)는 가열 쪽 피크가 **≈500 °C 부터 넓게 끌리고**, 냉각 결정화는 **493 °C 에 하나** — **넓어짐 + 하강 = incongruent melting** 이라는 저자 해석과 그림이 맞는다.
`Fig. S3b` 실독: y = Weight loss (%), 80–100. 둘 다 100 °C 근처에서 1–2 % 빠지고(이송 중 공기 노출), 300 °C 까지는 거의 겹친다(≈97 %). 그 뒤 **Cl1.5 만 315 °C 부터 급락 → 600 °C 에서 ≈81 %**. LPSCl 은 완만히 ≈95 %.
→ **Cl-rich 가 열역학적으로 덜 안정**하다는 독립 증거. 본문은 "TGA 에서 LPSCl 은 유의미한 손실 없음" 이라 했지만 `figure-read` 로는 **5 % 손실**이 있다 — 상대적 진술로만 읽어야 한다.
→ 이 축은 **우리 0 K grand-potential 이 구조적으로 못 잡는 축**이다(§7-D).

### 5.5 GITT — 분해의 전압 의존성 (`Fig. S4`) ★
`Fig. S4a` 실독(V vs In/InLi vs 누적용량 µAh): 두 곡선 모두 2.1–2.2 V 에서 출발해 단조 상승, 3.9 V 에서 LPSCl ≈305 µAh · Cl1.5 ≈358 µAh. **3 V 점선에서 각각 ≈112 / ≈163 µAh** ⇒ **3 V 이하에서 Cl-rich 가 1.45배 더 분해**, **3 V 이상에서는 193 vs 195 µAh 로 동일**.
`Fig. S4b` 실독(IR drop vs V): 2.2–2.9 V 구간에서 **검정이 오히려 살짝 위**(Cl-rich 가 σ 우위로 저항이 낮다). **3.0 V 에서 교차**한 뒤 빨강이 급상승 — 3.4 V 에서 0.42 vs 0.30, 3.9 V 에서 **0.71 vs 0.53 V**. 검정은 3.2–3.3 V 에 평탄부/딥이 있다.
🔑 **이 그림이 축을 가른다**: **카본만 있는 계(= 순수 전기화학 산화)에서는 고전압에서 Cl-rich 가 저항을 더 빨리 쌓는다.** 뒤의 `Fig. 2`(NCM 복합, 3.7 V 홀드)에서는 정반대다 → **차이를 만드는 것은 SE 자체가 아니라 CAM 의 산소**라는 논문 논지의 가장 깨끗한 근거.

### 5.6 임피던스 + TLM — 계면 열화 속도 (`Fig. 2`) ★
`Fig. 2a,b` 실독: Nyquist, 축 라벨이 **R_Re / −R_Im (Ω)** (통상 Z′/−Z″ 인데 R 로 적혀 있다), 0–180 Ω. 0/5/10/15 h 스펙트럼을 **35 Ω 씩 y-shift** 해 쌓았고, **~550 Hz 지점을 노란 점선**으로 이어 놓았다 — 두 시료 모두 550 Hz 로 같다(= 같은 종류의 과정).
- LPSCl 0 h: ≈29 → 97 Ω, 15 h: ≈30 → 150 Ω.
- Cl1.5 0 h: ≈20 → 70 Ω, 15 h: ≈18 → 112 Ω. (**Cl-rich 가 처음부터 낮다** = σ 효과.)

`Fig. 2c`: TLM 등가회로 — 분리막(직렬 R) + 양극(TLM 블록) + 음극(R∥CPE). TLM 내부는 전자 경로 **R_el**(초록), 이온 경로 **R_ion**(보라), 각 접점의 전하이동 **R_ct**(주황) + **W_diff**(입자 내 확산 Warburg) + **C_dc**(NCM 미분용량) + **CPE_int**(계면 용량).
`Fig. 2d`: R_cat vs t⁰·⁵ 가 **둘 다 직선** → 포물선 성장(확산율속 고체상 반응) 확정. 기울기 **13.2 vs 8.9 Ω h⁻⁰·⁵**. `figure-read` 로 절편도 다르다(≈25 vs ≈10 Ω).

메커니즘 제안(본문): ① NCM 표면에서 SE/C 계면과 같은 **전기화학 분해(Li 탈리 + S 산화, NCM 산소 무관)**, ② 추가로 **NCM–SE 화학반응**, 고전압(**>3.6 V vs In/InLi** = 4.2 vs Li⁺/Li)에서 **NCM85 격자 산소 방출** 동반. 포물선 = 둘의 합성.

### 5.7 사이클·rate (`Fig. 3`, `Table S1`)
`Fig. 3a` 실독: LPSCl 1차 충전 곡선이 **2.28 V 에서 출발**해 가파르게 3.0 V 로 올라간 뒤 완만한 기울기로 215 mAh/g 까지. `Fig. 3b` 의 Cl1.5 는 **≈2.95 V 에서 출발**. (셀별 초기 OCV 차 — 정량 비교엔 쓰지 말 것.) 10th·50th 충전은 둘 다 3.05–3.1 V 에서 시작.
`Fig. 3c`: 빨강이 전 구간 검정 위, 두 곡선이 **평행하게** 감쇠 — 즉 **감쇠 기전이 같고 오프셋만 다르다**.
율속 해석은 §3g 표 참조.

### 5.8 ToF-SIMS 표면 — 60 h 홀드 후 복합양극 (`Fig. 4`) ★ 반전의 핵심
`Fig. 4` 실독: 박스플롯 4장. (a) S⁻·(b) Cl⁻ 는 **I_total 정규화**, (c) PO₃⁻·(d) SO₃⁻ 는 **I_NiO₂⁻ 정규화**. 각 패널에 pristine(연한색) / aged(진한색) × 2조성 = 4 상자.
- (a)(b): 두 SE 모두 크게 증가, **Cl-rich 가 더 큼** → 분해 더 많음. (분산도 Cl-rich 가 크다 = 불균일.)
- (c) **PO₃⁻ 가 뒤집힌다**: pristine 이 2.2 vs 2.3 ×10⁵ 로 **맞춰져 있는데** aged 는 **8.1 vs 4.0 ×10⁵** — LPSCl 이 2배. 이 비교는 기준선이 같아 **깨끗하다**.
- (d) SO₃⁻: aged 3.55 vs 0.75 ×10⁵ 로 LPSCl 이 4.7배지만, **pristine 이 이미 1.1 vs 0.37 로 3배 차이** → 배수로는 3.2× vs 2.0× 로 줄어든다. **기준선 오염된 비교**다.
→ 요약: **"Cl-rich 는 고체 phosphate 를 덜 만든다"는 견고**, **"고체 sulfate 도 덜 만든다"는 약함.**

### 5.9 ToF-SIMS 공간분포 — 100 사이클 후 FIB 측벽 (`Fig. 5`, `Fig. S11`) ★
`Fig. 5` 실독: 6열 × 2행(위 LPSCl, 아래 Cl1.5) + RGB 확대. 스케일바 **20 µm**, 컬러맵은 I/I_total.
- **NiO₂⁻**(CAM): 5–10 µm 급 NCM 2차입자가 밝게. **Cl⁻**(SE): 정확히 그 보색 — 입자 사이가 밝다. 두 상이 잘 분리된다.
- **(PO₂⁻·PO₃⁻)**: LPSCl 행이 **눈에 띄게 밝고 연결망이 넓다**. Cl1.5 행은 훨씬 어둡다.
- **(SO₂⁻·SO₃⁻)**: **두 행 모두 거의 검다** — 신호가 정말 약하다. 논문의 "낮은 신호세기 + 질량간섭" 변명이 그림으로 확인된다.
- **(S₄⁻+S₅⁻+S₆⁻)**: 둘 다 SE/CAM 경계선을 따라 망상, Cl1.5 쪽이 조금 더 밝다.
- **RGB**(청 NiO₂⁻ / 적 POₓ / 녹 Sₓ): LPSCl 확대원에는 **청 입자를 감싸는 적색 띠**가 뚜렷하고 그 바깥에 녹색. Cl1.5 확대원은 **적색이 크게 줄고 녹색이 흩어져** 있다.
→ 논문 결론: **POₓ·SOₓ = NCM 쪽 "안쪽" 열화층**(O₂ 방출 + Li₂CO₃ 분해 + 확산율속 고체상 반응), **Sₓ = 전해질 쪽 "바깥" 열화층**(SE 의 전기화학적 탈리튬화).
→ ⚠ **그림이 "층"을 해상한 것은 아니다.** 시야 20 µm·실효분해능 ≳122 nm 이고, 보이는 것은 **입자 스케일 공간 상관**이다. nm 급 CEI 층구조를 이 그림으로 주장하면 과대해석(§10-⑤).
`Fig. S11` 실독(막대 3개, 오차막대 없음): §3e 표 그대로 — **Sₓ +43 % · POₓ −40 % · SOₓ ±0 %**.

### 5.10 DEMS — 기체 (`Fig. 6`) ★
`Fig. 6` 실독: 패널당 3단. 위 = Voltage (V vs In/InLi, 1.5–4.0), 중 = Rate O₂ (nmol min⁻¹ g⁻¹, 왼축 0–160) + **누적 Gas evolution (nmol g⁻¹, 오른축 0–8000)** 점선, 아래 = **정규화 이온전류 (a.u.)** m/z 64 (SO₂). x = 시간 0–100 h(2 사이클).
- 두 셀 모두 **1차 충전 말기에 O₂ 가 날카로운 단일 피크**로 터지고(LPSCl ≈140, Cl1.5 ≈133 nmol min⁻¹ g⁻¹), 누적은 그 계단에서 ≈5300 / ≈6000 nmol g⁻¹ 로 점프한 뒤 **2차 충전에서 한 번 더 작은 계단**(→ 6.7 / 6.8 µmol g⁻¹).
- **2차 사이클에도 O₂ 와 SO₂ 가 또 나온다** → 이 열화는 첫 충전으로 끝나지 않는다(자기제한적이지 않다).
- SO₂ 는 **O₂ 피크와 같은 시각에** 뜬다 → 산소 방출이 SO₂ 의 방아쇠. 피크 높이 **0.45 vs 2.55 a.u. ≈ 5.7×**.
- 그림 주석 전압 **3.59 V (LPSCl) vs 3.46 V (Cl1.5)** vs In/InLi — Cl-rich 셀이 **더 낮은 셀 전압에서** 같은 조건에 도달한다(과전압이 작아서. SOC 84.3 vs 82.5 % 와 정합).

### 5.11 ⚠ 논문이 스스로 그은 조건 경계 (본문 p.4)
저자들이 명시한다: *"`Fig. 2` 의 셀은 **3.7 V 에 홀드**된 것 — NCM85 산소 방출에 의한 **화학 열화**를 키우는 조건. 반면 **전기화학 분해**는 `Fig. 3` 처럼 **사이클링할 때** 더 두드러진다."*
그리고 실제로 `Fig. 3d,e` 에서 **두 셀의 저항 증가 차이는 "insignificant"** 라고 적었다. `figure-read` 로는 오히려 **Cl-rich 쪽 반원 성장이 더 크다**(Δ≈90 vs ≈71 Ω).
🔑 **따라서 "Cl-rich 가 계면에서 유리하다"는 결론은 *정전압 홀드(산소관여 화학 지배)* 조건에 붙은 결론이다.** 사이클링(전기화학 분해 지배)에서는 성립하지 않는다. 이 경계를 지우고 인용하면 안 된다.

---

## 6. 메커니즘 종합 (`Fig. 7`)

`Fig. 7` 실독: 4패널 + 범례(회색 LiCl · 빨강 P₂S₅ · 노랑 S/Sₓ²⁻ · 초록 sulfate/sulfite · 파랑 phosphate · O₂ 기체 · SO₂ 기체 · 빗금 **rock-salt transition metal oxide**).
- **왼쪽 2장 "Electrochemical decomposition"**(저전압, <4.2 V vs Li⁺/Li): NCM 위에 노랑(S/Sₓ)+회색(LiCl)+빨강(P₂S₅) 분해층. **Cl-rich 쪽 층이 더 두껍고 회색(LiCl)이 더 많다.**
- **오른쪽 2장 "Oxygen-involving degradation"**(≥4.2 V vs Li⁺/Li): NCM 표면에 **빗금 rock-salt 재구성층**이 생기고 그 위에 **초록(sulfate/sulfite) + 파랑(phosphate) 안쪽층**, 그 위로 노랑/회색 바깥층, 옆으로 O₂·SO₂ 가 빠져나간다. **LPSCl 쪽 초록+파랑 층이 두껍고, Cl-rich 쪽은 얇은 대신 SO₂ 분자가 훨씬 많이 그려져 있다.**

정리:
1. **< 4.2 V vs Li⁺/Li**: SE 의 **전기화학 산화**(탈리튬화 + S²⁻ 산화)가 지배. **Cl-rich 가 더 많이 분해**.
2. **≥ 4.2 V vs Li⁺/Li**: NCM85 격자 불안정화 → **표면 산소 활성화·방출**(+ Li₂CO₃ 분해) → **산소관여 열화**가 지배. 산물이 **기체(SO₂)** 와 **고체(phosphate, sulfate/sulfite)** 로 갈린다.
3. **조성이 바꾸는 것은 그 갈림의 비율**: Cl-rich = 기체·폴리설파이드 쪽 ↑, 고체 산화물(특히 phosphate) ↓.
4. 그 결과 **계면 저항 증가율 ↓ → 셀 성능 ↑** (단 §5.11 조건 한정).
5. 저자 자인: *"산소관여 열화의 메커니즘은 상당히 복잡하고, 기체/고체 산물이 갈리는 이유는 **여전히 불명확하며 추가 연구가 필요**하다."*

> ⚠ **이 그림 안에 논문의 내적 긴장이 있다**: 초록·결론은 *"thin and homogeneous phosphate/sulfate layer"* 가 성능을 올린다고 쓰는데, `Fig. 7` 은 Cl-rich 의 **전체 분해층을 더 두껍게** 그린다. 얇아진 것은 **산화물 안쪽층뿐**이다(§10-⑥).

---

## 7. 우리 DFT 와의 대조 ★★ (1저자 지정 축 — `../our_dft_baseline.md`, `db/properties/`)

> 규율: **문헌 수치는 소환값**이다. 아래 표는 *방향·순위·메커니즘*만 맞대고, 우리 절대값과 한 표에 섞지 않는다.

### 7a. 우리가 계산한 "Cl 증가의 방향" (먼저 확인한 것)

| 우리 축 | 원장 | 계산 결과 (Cl 0.5 → 1.0 → 1.5 → 1.6) |
|---|---|---|
| **B① 0압력 열역학 산화 onset** | `db/properties/constrained_esw_cl_scan.json`, `esw_lis4excluded.json` | **2.256 V 고정** — Cl 함량에 **완전 무감**. (Li₅PS₄Cl₂ = Cl 2.0 에 가서야 2.385 V 로 튀는데 그건 반응식 자체가 바뀜) |
| 그 onset 반응 | 동일 | comp1 `Li6PS5Cl → Li3PS4 + LiCl + S + 2 Li` · modelc `Li5.4PS4.4Cl1.6 → Li3PS4 + 1.6 LiCl + 0.4 S + 0.8 Li` |
| **B② 구속(strain-explicit) ESW** | 같은 파일, k_eff 10/20 GPa | 산화 onset이 **Cl 과 함께 단조 상승**: k_eff 10 GPa 에서 Cl0.5 **1.784** < Cl1.0 **1.969** < Cl1.5 **2.456** < Cl1.6 **2.685 V**. 이유는 산화 반응의 **ΔV 부호 전환**(Cl0.5 −22.7 Å³/3e⁻ → Cl1.5 **+3.2** Å³/1e⁻ → Cl1.6 **+5.5** Å³/0.8e⁻) |
| **B③ 양극 계면 반응성** | `db/properties/oxidation_stability.json` (`nd2o3_interface_reactivity`) | vs LiCoO₂ 최소 ΔE_rxn: comp1 **−0.3227** vs modelc **−0.3308 eV/atom** (modelc 가 0.008 만큼 더 반응성 — **noise 급**). **산물은 두 조성 동일**: Co₉S₈ + Li₃PO₄ + Li₂S + LiCl + Li₂SO₄ |

### 7b. 항목별 대조 — 같은가 다른가

| # | 항목 | Zuo (실험) | 우리 (DFT) | 판정 |
|---|---|---|---|---|
| **A** | **분해 stoichiometry** | Eq (1) 2 e⁻ + 1.0 LiCl / Eq (2) 1 e⁻ + 1.5 LiCl | comp1 **2 Li⁺/2 e⁻ + 1 LiCl + 1 S** (= Eq 1 **문자 그대로 일치**) / modelc **0.8 e⁻ + 1.6 LiCl + 0.4 S** (= Eq 2 거동) | **✓✓✓ 완전 일치.** Zuo 가 "highly simplified" 라고 단 반응식을 우리 grand-potential 이 **독립적으로 재생**했다. 이 논문의 이론부 전체가 우리 계산과 같은 것을 말한다 |
| **B** | **산화 onset (열역학)** | "**peak 전위 동일**"(`Fig. S2`) — 메커니즘 같음 | comp1 = modelc **2.256 V** 동일 (**S²⁻-limited**) | **✓✓ 일치.** Cl 은 onset 을 옮기지 않는다는 우리 결론의 **실험 확증**. 논문의 "lower onset for Cl1.5" 는 전류 크기 차이지 열역학 onset 이 아님 |
| **C** | **측정창 정렬** | CV **2.0–3.7 V vs In/InLi = 2.6–4.3 V vs Li⁺/Li** | 우리 onset 2.256 V vs Li⁺/Li = **1.656 V vs In/InLi** | 🔑 **비교 불가 — 우리 onset 은 이 논문 창 아래 0.34 V.** 두 시료 다 **창 하한에서 이미 산화 중**인 것이 우리 열역학 onset 이 더 아래에 있다는 것과 **정합**. ⛔ "실험 onset 2.0 V vs 우리 2.256 V" 식으로 나란히 쓰면 기준전극을 섞는 오류 |
| **D** | **분해 "양" (CV 1.5×·GITT 1.45×)** | Cl-rich 가 더 분해 | 우리는 **양을 계산하지 않는다**(0 K 열역학은 onset 과 산물만 준다) | **✗ 범위 밖 (모순 아님).** 양은 kinetics·접촉면적·전자전도·σ 의 함수. `figure-read` 전류비 **1.5× < σ 비 2.4×** 라 **"σ 만으로 설명 가능한 범위"** 안이다 → ⛔ Cl-rich 의 **intrinsic 반응성이 크다**고 주장 금지 |
| **E** | **열역학 준안정성 (DSC/TGA)** | Cl-rich 융점↓·315 °C 질량손실 | 우리 ESW 는 **조성간 metastability 를 못 본다**(E_above_hull 축 미구축) | **✗ 우리 공백.** [Wang22] Th′ 서술자로 *우리 산수* 한 comp1 ≈683 > modelc ≈656 kJ/mol 이 **같은 방향**이긴 하나 Eq5 에 Li–Cl 항이 없어 정량 금지 |
| **F** | **B② 구속 축** | **데이터 없음** (셀은 ~100 MPa 스택압이지만 k_eff 와 다른 양) | Cl↑ → 구속 하 onset **상승** (2.256 → 2.685 V @10 GPa) | **미검증.** Zuo 가 반증하지도 지지하지도 않는다. ⚠ 단 *정신적으로는 긴장*: 구속이 Cl-rich 를 보호한다면 100 MPa 펠렛에서 1.5× 더 분해되는 것은 설명이 필요 → **B② 는 [GG] 계열로 따로 검증해야 한다** |
| **G** | **양극 계면 산물 (종류)** | ToF-SIMS **PO₃⁻/PO₂⁻ · SO₃⁻/SO₂⁻ · Sₓ⁻ · Cl⁻** | interface_reactivity(vs LiCoO₂) **Li₃PO₄ · Li₂SO₄ · 폴리설파이드(0.25 LiS₄→S) · LiCl** (+Co₉S₈) | **✓✓ 4종 1:1 일치** (§11b 상세). 우리 hull 이 **독립적으로** Zuo 가 SIMS 로 본 계면 화학을 내놓는다 |
| **H** | **양극 계면 산물 (비율)** | Cl-rich 가 phosphate **−40 %**, 폴리설파이드 **+43 %** | comp1 −0.3227 ≈ modelc −0.3308 eV/atom (**Δ0.008 = noise**), **산물 목록 동일** | **✗ 못 가른다.** 우리는 "어떤 상" 까지, Zuo 는 "얼마나" 까지. 정적 hull 로 분율을 논하면 안 됨 |
| **I** | **기체 경로 (SO₂ diversion)** | O₂ 동일(6.7≈6.8) · SO₂ 5.7× | **구조적으로 못 봄** — 우리 hull 은 닫힌 고체계, 기체상 chempot 없음 | **✗ 우리 한계.** 향후 (a) 기체 chempot 을 연 계면, (b) NCM O-release 를 소스로 넣은 계산 필요 |
| **J** | **셀 성능 (R_cat·용량)** | Cl-rich 승 (홀드 조건) | 계산 밖 | **✗** — 인용만 |

### 7c. 🔑 층위를 갈라 쓴 결론 (원고·발표용)

> **"Cl 증가는 우리 계산에서도 실험에서도 *산화 onset 을 옮기지 않는다*(S²⁻ 가 한계를 고정). 실험이 보는 Cl-rich 의 열세는 onset 이 아니라 *분해의 양·속도*이고, 그 크기(CV 1.5×)는 이온전도도 비(2.4×)로 설명 가능한 범위 안이다. 실험이 보는 Cl-rich 의 우세는 *고전압 NCM 산소관여 경로의 산물 분배*(고체 phosphate ↓, 기체 SO₂ ↑)이며, 이는 우리 0 K 닫힌계 hull 이 원리적으로 못 보는 축이다."**

층위 표:
| 층위 | 누가 보는가 | Cl↑ 의 방향 |
|---|---|---|
| 0 K 열역학 **onset** | 우리 grand-potential · Zuo CV peak 전위 | **무변화** (양쪽 일치) |
| 0 K 열역학 **산물** | 우리 hull · Zuo Eq1/2 · Zuo ToF-SIMS 종 | **LiCl↑, 전자↓** (양쪽 일치) |
| **준안정성/합성 열역학** | Zuo DSC/TGA | **악화** (우리 공백) |
| **분해 kinetics/양** | Zuo CV·GITT·SIMS fold | **악화** (우리 범위 밖; σ 로 상당 부분 설명) |
| **구속 하 onset** | 우리 constrained ESW | **개선** (실험 미검증) |
| **CAM 산소관여 산물 분배** | Zuo SIMS·DEMS | **개선(phosphate↓)** (우리 범위 밖) |
| **셀 계면저항** | Zuo EIS/TLM | **개선(홀드 조건 한정)** — ⚠ σ 교락(§10-②) |

### 7d. LPSOCl(+O) 축과의 연결 ★
이 논문에서 **산소는 SE 안에 넣은 도펀트가 아니라 NCM 격자에서 나온 것**이다. 그런데 그 산소가 SE 와 만나 만드는 것이 정확히 **phosphate(Li₃PO₄)와 sulfate(Li₂SO₄)** — 우리 **LPSOCl(+O) 계에서 O 가 들어가 만드는 결합환경과 같은 종류**다. 두 가지 읽기:
1. **우리 interface_reactivity 가 comp1/modelc 모두에 Li₃PO₄ 를 산물로 내놓는데, 그 O 의 출처는 도펀트가 아니라 *양극*이다** (원장 주석: *"O for Li₃PO₄ comes from the CATHODE, so phosphate CEI forms regardless of doping"*). Zuo 의 ToF-SIMS PO₃⁻ 가 그 예측의 실측이다.
2. ⚠ **따라서 "O 를 SE 에 미리 넣으면 phosphate CEI 를 미리 만든 셈" 이라는 서사는 이 논문이 지지하지 않는다.** Zuo 에서 phosphate 가 **많은** 쪽(LPSCl)이 계면저항이 **더 빨리** 오른다. 즉 이 논문 프레임에서 **phosphate 는 좋은 CEI 가 아니라 저항원**이다 — 우리 LPSOCl 서사가 "Li₃PO₄ 형 결합이 유리" 쪽으로 갈 때 반드시 마주칠 반론이다.
   (⚠ 단 §10-⑥ 대로 그 인과는 이 논문에서 증명되지 않았다. 양쪽 다 약한 주장이다.)

---

## 8. DFT/계산 방법 ★
**없다.** code·functional·pseudo·k-point·supercell·DFT+U·AIMD·MLIP·무질서 처리 전부 **n/a** — 이 논문은 원자단위 계산을 수행하지 않는다. 이론적 내용은 §4g 의 반응식 (1)–(3) 뿐이며, 그 출처도 자체 계산이 아니라 선행 문헌(ref 7b, 12, 16)의 서술이다.
⇒ **우리 grand-potential 이 이 논문의 이론부를 *채우는* 관계**다. 반대 방향(이 논문에서 계산 수치를 가져오기)은 성립하지 않는다.

---

## 9. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| S1 | XRD 두 전해질, Cl1.5 에만 LiCl(2θ≈35°,50°, `figure-read` 최강선 대비 ≲2 %) | **Cl 고용한계의 실물 증거** — modelc Cl1.6 은 이 한계 *너머*라 2차상 명시 필요 |
| 1a,b | CV (SE/C, 0.05 mV/s, C65 20 wt%, 2.0–3.7 V vs In/InLi). 피크 `figure-read` **32 vs 47 nA cm⁻²**, 1→3 사이클에 전류 거의 0 으로 붕괴 | 분해 "양" 의 1차 증거 + **자기부동태화**([Wu26] practical window 와 같은 현상) |
| 1c,d | ToF-SIMS SE/C 표면 S⁻ 6.7→10.4배 · Cl⁻ 5.1→6.7배 (60 h @3.7 V) | 분해 정도의 정량 배수. 절대값 아닌 **fold 로만** |
| S2 | CV 겹침 — peak 전위 동일, Cl-rich 가 전 구간 위 | **"onset 동일 = 우리 2.256 V 조성 무감"의 실험 확증** + 창 하한(2.6 V vs Li⁺/Li)이 우리 onset 위라는 §7-C 논점 |
| S3 | DSC(535/532 vs 523/493 °C) · TGA(315 °C 부터, 600 °C 잔량 `figure-read` 95 vs 81 %) | **우리가 못 보는 metastability 축** — E_above_hull(SQS) 숙제의 근거 |
| S4 | GITT: 3 V 이하 용량 `figure-read` 112 vs 163 µAh, 3 V 이상 193 vs 195; IR drop 3.0 V 에서 교차 | **카본계에서는 Cl-rich 가 고전압 저항을 더 쌓는다** = `Fig. 2` 와 반대 → 축 분리의 핵심 근거 |
| 2a–d | EIS + TLM, R_cat=√(R_ct(R_el+R_ion)), √t 기울기 13.2 vs 8.9 Ω h⁻⁰·⁵ | 계면 열화 **속도**의 정량 틀 — ⚠ σ 교락 주의(§10-②). TLM 자체는 우리가 차용할 도구 |
| 3a–e | 0.5 C 사이클(215/165→133 vs 215/170→145) + 1/10/50th Nyquist | 성능 우위의 근거. ⚠ `figure-read` 로 **사이클링 중 저항 증가는 Cl-rich 가 더 큼** |
| 4a–d | ToF-SIMS 복합양극 (60 h 홀드): S⁻·Cl⁻ ↑(Cl-rich 큼), **PO₃⁻ 8.1 vs 4.0 ×10⁵**, SO₃⁻ 3.55 vs 0.75 ×10⁵ | **반전의 핵심.** phosphate 비교는 pristine 이 맞아 깨끗, sulfate 는 기준선 오염 |
| 5 | FIB 45° 측벽 SI 이미지 6종 + RGB (100 사이클, 20 µm 시야) | CEI **공간 상관**(POₓ=CAM 쪽, Sₓ=SE 쪽). ⚠ nm 층구조 주장 금지 |
| S10 | 폴리설파이드 Sₓ⁻(x=1–4) 박스플롯 — S₂⁻·S₃⁻ 는 Cl-rich 증가, S₄⁻ 는 집전체 간섭으로 차이 소멸 | (미독) 폴리설파이드 증가의 보강 |
| S11 | ROI 반정량 (100 사이클): Sₓ **9.1e−3 → 1.3e−2** · POₓ **7.2e−3 → 4.3e−3** · SOₓ **4.7e−4 ≈ 4.8e−4** | **장기에는 "sulfate 감소"가 무효** — 인용 조건 붙이기. 오차막대 없음 |
| 6a,b | DEMS: O₂ 6.7 vs 6.8 µmol/g_NCM(동일), SO₂ `figure-read` ≈5.7×, 2차 사이클에도 재발생 | **gas diversion** 의 유일한 정량 근거. SO₂ 는 a.u. — 배수 인용 시 명시 |
| S12 | CO₂·H₂ — H₂=음극 수분, CO₂=NCM 표면 Li₂CO₃(복합양극에 카본 없음) | (미독) 기체 귀속의 대조군 |
| 7 | 메커니즘 도식: 좌 전기화학분해(Cl-rich 층 더 두껍다) / 우 산소관여(Cl-rich 산화물층 얇고 SO₂ 많다) + **rock-salt 재구성층** | deck 용 산화 2단계 도식. ⚠ 초록의 "thin layer" 와 그림의 "두꺼운 총층"이 어긋남(§10-⑥) |
| Table S1 | 4-셀 교차(분리막×양극) 율속 표 | **저율=복합양극 병목 / 고율=분리막 σ 병목** 분해. ⚠ 2C 에서 `LPSCl 분리막|Cl1.5 양극` 이 최하 |

---

## 10. 비판 — 이 논문의 약한 곳 ★

① **"approximately twofold" 는 그림이 지지하지 않는다.** `Fig. S2` 를 실제로 보면 피크 전류비는 **≈1.5×**(47 vs 32 nA cm⁻²)이고, 3.65 V 에서는 **≈1.1×** 로 수렴한다. 2× 이상이 되는 곳은 **2.0–2.2 V 개시 구간**뿐이다. 정량 주장에 구간이 없다.

② **R_cat 은 σ 와 교락돼 있다 — 이 논문에서 제일 큰 구멍.** 식 (4) `R_cat=√(R_ct(R_el+R_ion))` 안에 **R_ion 이 들어 있고**, Cl-rich 는 σ 가 **2.4×** 높다. R_ct 만 t 에 선형이라면 √t 기울기 = √(k_ct·(R_el+R_ion)) 이므로 **기울기 비 13.2/8.9 = 1.48 은 (R_el+R_ion) 비가 ~2.2 이기만 해도 화학적 차이 없이 전부 설명된다.** 논문은 Gerischer 거동 때문에 **R_ct 와 수송을 분리 못 한다고 스스로 인정**하면서, 분리 못 한 양으로 **화학적 결론**을 낸다. 면적·로딩 정규화도 없다(단위가 Ω). ⇒ **"Cl-rich 계면 화학이 착하다" 는 이 데이터만으로는 확립되지 않는다.**

③ **`Fig. 4c,d` 는 처리가 일관되지 않다.** (a),(b) 는 I_total 정규화 + pristine 대비 **배수**로, (c),(d) 는 I_NiO₂⁻ 정규화 + **절대값**으로 비교한다. SO₃⁻ 는 **pristine 이 이미 3배 차이(1.1 vs 0.37)** 라 절대 비교가 기준선을 물려받는다. 배수로 환산하면 3.2× vs 2.0× 로 격차가 크게 준다. 그리고 100 사이클 후(`Fig. S11c`)에는 **차이가 완전히 사라진다**(4.7 vs 4.8 ×10⁻⁴). ⇒ **초록의 "less ... sulfur species" 는 조건부**로만 참.

④ **DEMS 셀의 쿨롱효율이 결론과 반대다.** *우리 산수*: LPSCl **201/243 = 82.7 %** vs Cl1.5 **176/239 = 73.6 %** — **Cl-rich 가 9 %p 열세**다. 같은 논문의 0.5 C 셀에서는 79 vs 77 % 로 Cl-rich 우세였다. 즉 **C/20·45 °C(고전압 체류시간 길고 뜨거움)에서는 Cl-rich 가 확실히 더 손해**인데, 논문은 이 숫자를 적어 놓고 **한 줄도 논하지 않는다**. SO₂ 5.7× 와 같은 방향이라 우연으로 보기 어렵다.

⑤ **`Fig. 5` 의 "내부층/외부층"은 해상된 층이 아니다.** 시야 20 µm, 실효 측방분해능 ≳122 nm(이론값이고 지형·거칠기로 더 나빠진다고 논문이 인정), FIB 45° 측벽. 보이는 것은 **입자 스케일 공간 상관**이다. 여기서 CEI **층서(stratigraphy)** 를 주장하는 것은 데이터를 넘어선다.

⑥ **"덜 저항성인 CEI" 의 물리가 논증되지 않았다.** 논문 논리는 *"Cl-rich 는 고체 phosphate/sulfate 를 덜 만든다 → 계면저항이 덜 오른다"* 인데, **왜 phosphate/sulfate 가 폴리설파이드·원소 S·LiCl 보다 더 저항성인지** 한 줄도 없다. 오히려 상식은 반대에 가깝다 — **Li₃PO₄ 는 코팅재로 쓰이는 Li⁺ 전도체**이고, **원소 S·폴리설파이드는 전자·이온 양쪽으로 절연**이며 LiCl 도 열등한 전도체다. 게다가 `Fig. 7` 은 Cl-rich 의 **총 분해층을 더 두껍게** 그려놓고 초록은 *"thin and homogeneous"* 라고 쓴다. **인과의 방향이 검증되지 않은 상태에서 서사가 먼저 있다.**

⑦ **상 순도가 비교군을 오염시킨다.** Cl1.5 에는 LiCl 2차상이 있고(`Fig. S1`), 저자들은 DSC/TGA 만 **480 °C 로 따로 합성한 상순수 시료**로 측정했다. 즉 **열 데이터와 전기화학 데이터의 시료가 다르다.** "미량 LiCl 은 열안정성에만 영향" 이라는 주장에 근거 제시가 없다(σ·CV 대조 데이터 미제시).

⑧ **n=1 급 통계.** ToF-SIMS 는 시료당 10 지점으로 박스플롯을 그려 좋지만, **셀은 조성당 1개**로 보이고 `Fig. S11` ROI 에는 **오차막대가 없다**. R_cat 기울기(13.2 vs 8.9)도 단일 셀 피팅이다. 셀-대-셀 산포를 모르면 1.48× 를 유의하다고 말할 수 없다.

⑨ **인용 오류 2건.** 본문 p.4 가 율속 데이터를 **`Fig. S5`** 라 지칭하는데 실제로는 **`Fig. S7`·`Fig. S8`** 이다(`Fig. S5` 는 EIS 피팅). SI 의 H₂ 논의도 **`Fig. S9`**(SEM)를 가리키는데 **`Fig. S12`** 여야 한다.

⑩ **`Fig. 1a,b` 의 자기부동태화를 논하지 않는다.** 1→3 사이클에 산화전류가 거의 0 으로 붕괴하는 것은 **분해층이 스스로를 막는다**는 뜻이고, 이게 실용 창을 만드는 기전인데 본문에 언급이 없다. 우리에겐 이 대목이 [Wu26]·[Qian25/26] 과 이어지는 중요한 자리다.

⑪ **"주요 구조변화 없이 halide 만"이라는 모델 전제가 느슨하다.** Cl 1.0 → 1.5 는 Li 공공 0.5 개 + Cl/S 자리무질서 대폭 증가([Adeli] 4c-Cl 점유 61 → 83 %) + 격자 수축(9.8598 → 9.8061 Å)을 동반한다. σ 가 2.4× 바뀐 것 자체가 "주요 변화 없음"과 어울리지 않는다.

---

## 11. 우리 원장 매핑 (요약표)

| 항목 | Zuo (exp, 소환값) | 우리 (DFT, canonical) | 판정 |
|---|---|---|---|
| 분해 stoichiometry | Eq1 / Eq2 | comp1/modelc grand-potential onset 반응 | **✓✓✓ 일치** |
| 산화 onset | peak 전위 동일 | **2.256 V** 동일 (LiS4 제외; 포함 2.14) | **✓✓ 일치** (S²⁻-limited) |
| Cl-rich 분해 "양" | CV `fr≈`1.5× · GITT(<3 V) 1.45× · SIMS 10.4/6.7 | 계산 축 없음 (interface ΔE 차이 0.008 eV/atom = noise) | **✗ 범위 밖** — σ 2.4× 로 설명 가능 |
| 구속 하 onset | 데이터 없음 | Cl↑ → 2.256 → 2.685 V (k_eff 10 GPa) | **미검증** |
| 계면 산물 **종류** | PO₃⁻ · SO₃⁻ · Sₓ⁻ · Cl⁻ | Li₃PO₄ · Li₂SO₄ · 폴리설파이드 · LiCl (+Co₉S₈) | **✓✓ 1:1** (§11b) |
| 계면 산물 **분율** | phosphate −40 %, Sₓ +43 % | 분율 계산 불가 | **✗** |
| 기체(SO₂/O₂) | 정량 | 닫힌 고체계 — 기체 없음 | **✗ 우리 한계** |
| metastability | DSC/TGA Cl-rich 열세 | E_above_hull 축 미구축 | **✗ 우리 공백** |

## 11b. Zuo ToF-SIMS 분해종 ↔ 우리 interface_reactivity + XPS anchor (2026-06-26 추가, 유지)

> Zuo 는 **ToF-SIMS 음이온 fragment** 로만 종을 본다. 우리는 같은 화학을 **grand-potential interface_reactivity**(`db/properties/oxidation_stability.json`)로 *어떤 상*인지 짚고, **XPS BE anchor**(`db/properties/xps_reference_sei.csv`)로 그 상을 *코어레벨로* 동정한다.

| Zuo ToF-SIMS fragment | = 우리 interface_reactivity 산물 (vs LiCoO₂) | = 우리 XPS anchor (BE_eV) | 정합 |
|---|---|---|---|
| **PO₃⁻ / PO₂⁻** (phosphate, 안쪽층) | **Li₃PO₄** (O 는 **CATHODE** 에서 옴 → 도핑 무관 형성) | Li₃PO₄ **P 2p₃/₂ 133.3** · O 1s 531.5 (thiophosphate 131.7 대비 **+1.6 eV**) | **✓✓** |
| **SO₃⁻ / SO₂⁻** (sulfate/sulfite, 안쪽층) | **Li₂SO₄** | Li₂SO₄ **S 2p₃/₂ 168.0** (thiophosphate 161.6 대비 **+6.4 eV**) | **✓✓** |
| **Sₓ⁻ (S₄+S₅+S₆, 바깥층)** | grand-potential staircase **0.25 LiS₄(2.14 V) → 원소 S(3.06 V)** | (폴리설파이드 단일 anchor 없음; Li₂S **S 2p 160.2** = 완전환원 끝점) | **✓ 같은 경로** |
| **Cl⁻ (LiCl)** | **LiCl** (comp1/modelc 분해 전구간 inert 산물) | LiCl **Cl 2p₃/₂ 198.6** | **✓✓** |

🔑 세 결론:
1. **Zuo 의 SIMS 4종 = 우리 interface_reactivity 산물 4종 (1:1)** — 우리 grand-potential 이 *독립적으로* 같은 상을 내놓는다.
2. **XPS anchor 도 동일 상을 지목** — 우리 `xps_reference_sei.csv` 가 Zuo 계면 화학을 BE 수준으로 커버.
3. **단 "양 vs 질" 은 SIMS 만 분리** — comp1 −0.3227 ≈ modelc −0.3308 eV/atom (**Δ0.008 = noise**) → "어떤 산물" 은 같고 "얼마나" 는 못 가른다.

---

## 12. 적용 인사이트 ★

1. **축 B 의 프레이밍이 이 논문으로 확정된다.** *"Cl 증가는 산화 onset 을 옮기지 않는다(우리 2.256 V·Zuo peak 동일). 바뀌는 것은 분해의 **양**(악화, σ 로 상당 설명)과 산물의 **분배**(고전압 CAM 계면에서 개선)다."* — onset/양/분배 **세 층을 섞지 않는 것**이 이 논문의 최대 소득.
2. **우리 grand-potential 이 Zuo 의 이론부를 문자 그대로 재생한다** (Eq1 ↔ comp1 onset 반응). 이 논문은 원자계산을 하지 않으므로, **"실험 논문의 반응식을 우리 계산이 독립 재현" 은 강한 검증 문장**이다.
3. **`figure-read` 전류비 1.5× < σ 비 2.4×** — 기존 digest 가 "2× ≈ σ 2.4× 이므로 접근성" 이라 했는데, 실제 그림은 **1.5×** 라 오히려 **단위 전도도당 반응성은 Cl-rich 가 낮다**. ⛔ 어느 방향으로도 intrinsic 반응성을 주장하지 말 것.
4. **"어디서 측정했나" 가 결론을 뒤집는다**: **카본계(`Fig. S4b`)** = Cl-rich 가 고전압 저항 더 쌓음 / **NCM 정전압 홀드(`Fig. 2d`)** = Cl-rich 유리 / **NCM 사이클링(`Fig. 3d,e`)** = 차이 없음(figure-read 로는 Cl-rich 열세) / **C20·45 °C DEMS** = Cl-rich CE 9 %p 열세. ⇒ 우리 4축 명명(B①②③④)이 문헌에서 실제로 필요하다는 실증.
5. **정량 틀 차용 2종**: (a) **R_cat = √(R_ct(R_el+R_ion)) 의 √t 기울기**를 "계면 열화 속도" 단일 수치로 쓰는 법, (b) **ToF-SIMS 종 분리**(고체 산화물 vs 폴리설파이드 vs 기체)로 "분해의 양 vs 질" 을 나누는 법. 단 (a) 는 **σ 정규화 없이는 못 쓴다**(§10-②) — 우리가 쓸 땐 R_ion 을 독립 측정/계산해 나눠야 한다.
6. **우리 공백 2개가 명확해졌다**: (i) **기체상을 연 계면 열역학**(SO₂/O₂ chempot + NCM O-release 소스), (ii) **무질서 E_above_hull(SQS)** 로 조성간 metastability. 둘 다 이 논문이 실험으로 보여주는데 우리 모델이 구조적으로 못 보는 것.
7. **modelc Cl1.6 경고**: Cl**1.5** 에서 이미 LiCl 2차상이 XRD 에 보인다(`Fig. S1`). [Adeli] 고용한계가 x=0.5(=Cl1.5)이고 **x=0.6(=우리 modelc 조성)은 LiCl 석출 + σ 3.3 mS/cm 로 꺾인다**. ⇒ modelc 를 "실현 가능한 단상" 으로 말할 때 **반드시 2차상 단서**를 붙인다.
8. **LPSOCl(+O) 서사에 대한 반론을 미리 알아둘 것** (§7d): 이 논문 프레임에서 **phosphate 는 저항원**이다. "O 를 넣어 phosphate 형 계면을 만든다" 가 자동으로 좋은 이야기가 아니다.

---

## 13. 인용 가능 문장 (영문 초안)

- "Our grand-potential decomposition reactions reproduce the simplified reaction scheme of Zuo et al. — two electrons and one LiCl for Li₆PS₅Cl versus fewer electrons and more inert LiCl for the Cl-rich composition — providing an independent, first-principles cross-check of the chemistry that their experiments presuppose."
- "Consistent with the identical CV peak potentials reported by Zuo et al., our calculated oxidation onset is unchanged between Li₆PS₅Cl and the Cl-rich composition (S²⁻-limited); chlorination alters the *extent* and the *product distribution* of oxidation, not its thermodynamic onset."
- "Because the CV window of Zuo et al. (2.0–3.7 V vs In/InLi ≡ 2.6–4.3 V vs Li⁺/Li) starts above our calculated thermodynamic oxidation onset, both electrolytes are already beyond their thermodynamic limit at the start of the scan — the reported onset difference is a current-magnitude, not a thermodynamic, observation."
- "Chlorination is a trade-off: more electrochemical decomposition (≈1.5× anodic peak current density, 1.45× decomposition capacity below 3 V vs In/InLi) but a product distribution shifted away from resistive solid phosphate (−40 % PO₂⁻·PO₃⁻ after 100 cycles) toward gaseous SO₂ and polysulfides."
- ⚠ (조건부) "Under a 3.7 V (vs In/InLi) potentiostatic hold, the cathode resistance of the Cl-rich cell grows more slowly (8.9 vs 13.2 Ω h⁻⁰·⁵); we note that this effective resistance contains the ionic transport term and is therefore not decoupled from the 2.4× higher ionic conductivity of the Cl-rich electrolyte."

## 14. 주의 / 한계 (인용 규율)

- ⛔ **Zuo 의 Cl-rich 는 Cl 1.5, 우리 modelc 는 Cl 1.6** — 동일시 금지. 1.6 은 [Adeli] 고용한계 밖이다.
- ⛔ **전압 기준 혼용 금지.** 이 논문은 **+0.6 V** 환산을 쓴다(In/InLi → Li⁺/Li). CV·GITT·EIS·DEMS 는 In/InLi, "≥4.2 V" 메커니즘 문장은 Li⁺/Li.
- ⛔ **우리 onset(2.256 V vs Li⁺/Li)과 이 논문의 CV 수치를 같은 표에 놓지 말 것** — 측정창이 우리 onset 위에서 시작한다(§7-C).
- ⛔ **R_cat 8.9/13.2 을 "계면 화학 우열" 로 단독 인용 금지** — σ 교락(§10-②). 쓸 거면 교락을 같은 문장에 적는다.
- ⛔ **SO₂ 5.7× 는 `figure-read` a.u. 비**다. 교정된 몰비가 아니다. O₂ 만 µmol/g 로 교정됐다.
- ⛔ **"less oxygenated sulfur" 는 60 h 홀드 한정** — 100 사이클(`Fig. S11c`)에서는 차이 없음(4.7 vs 4.8 ×10⁻⁴).
- ⚠ **"낮은 onset"** 은 `Fig. S2` 의 약한 주장이다. peak 전위는 동일하다고 논문 자신이 쓴다.
- ⚠ CV 는 **탄소 20 wt% 증폭계**다. 평판 CV([Adeli])는 **정반대 겉보기**(Cl-rich 전류가 더 작음)를 준다 — 측정계 명시 없이 "Cl-rich 가 더/덜 분해" 를 인용하면 안 된다.
- ⚠ **DSC/TGA 시료는 480 °C 로 따로 합성한 상순수품** — 전기화학 시료와 다르다.
- ⚠ NCM85 특정 결과다. 다른 CAM(저Ni·스피넬·인산염)이면 산소관여 축 자체가 달라진다.

## 15. 기법 용어 미니사전

- **CV (cyclic voltammetry)**: 전위를 일정 속도로 훑으며 전류를 본다. SE/카본 복합에서 흘리는 산화전류 = SE 분해 **속도**. 카본은 전자를 SE 표면 구석구석에 배달하는 **증폭기**라, 실제 셀보다 분해를 과장해서 보여준다(그게 목적).
- **In/InLi 기준전극**: In 에 Li 를 조금 넣으면 2상 공존(In + InLi)이 되어 전위가 **Li⁺/Li 대비 약 0.6 V** 에 고정된다. Li 금속보다 다루기 쉬워 전고체셀의 사실상 표준 음극이자 기준.
- **GITT**: 짧은 전류 펄스 + 긴 이완을 반복. 펄스 직후 전압 점프(**IR drop**)가 내부저항, 이완 후 전압이 준평형 전위. 여기서는 "전압대별로 얼마나 분해됐나 + 저항이 얼마나 쌓였나" 를 동시에 본다.
- **TLM (transmission line model)**: 다공성 복합전극을 "이온 사다리(R_ion) ∥ 전자 사다리(R_el) + 가로대(R_ct)" 로 모델링한 임피던스 등가회로. 세 저항을 분리하려는 도구인데, **Gerischer 거동**(화학반응과 확산이 결합돼 45° 꼬리가 생김)이면 분리가 안 되고 **곱 √(R_ct(R_el+R_ion))** 형태의 유효저항만 나온다.
- **ToF-SIMS**: 1차 이온빔(여기선 Bi₃⁺/Bi₃²⁺)으로 표면을 때려 튀어나온 **2차 이온**을 비행시간 질량분석. `static` 조건(도즈 <10¹³ ions cm⁻²)이면 표면 1층만 본다. **매트릭스 효과** 때문에 절대 정량이 아니고, 같은 물질끼리의 **상대 배수**로 읽어야 한다. FIB 로 45° crater 를 파면 **단면 2D 맵**을 얻는다.
- **DEMS**: 셀에 캐리어가스(He)를 흘리며 나오는 기체를 **실시간 질량분석**. 전기화학 곡선과 시간축을 공유해 "어느 전압에서 무슨 기체가 얼마나" 를 준다. 교정가스로 이온전류 → mol/g 환산.
- **CEI (cathode–electrolyte interphase)**: 양극/전해질 계면에 자라는 분해 생성층. 얇고 Li⁺ 를 통과시키며 전자를 막으면 좋고, 두껍거나 저항성이면 나쁘다.
- **singlet oxygen (¹O₂)**: 고SOC 층상 산화물 표면에서 나오는 들뜬 상태 산소. 삼중항 O₂ 보다 훨씬 반응성이 커서, 전해질 산화(여기선 SO₂ 생성)의 주범으로 지목된다.
- **incongruent melting**: 녹을 때 액상과 고상의 조성이 달라지는 융해. DSC 피크가 **넓어지고 과냉각(결정화 온도 하강)** 이 커지는 것이 신호 — Cl1.5 가 그렇다.
- **rock-salt reconstruction layer**: 고-Ni 층상 양극이 산소를 잃으면 표면이 층상(R-3m) → 암염(Fm-3m)으로 재구성된다. Li⁺ 통로가 막혀 저항원이 된다. `Fig. 7` 의 빗금 층.
