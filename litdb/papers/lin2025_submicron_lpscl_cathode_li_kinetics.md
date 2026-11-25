# Sub-micrometer Li6PS5Cl regulated cathodic Li kinetics in sulfide based all-solid-state batteries — Lin et al. (*Phys. Chem. Chem. Phys.* **2025**, 27, 3455–3462) · 습식 밀링 미립 LPSCl (D50 2.34 µm) vs 원 LPSCl (D50 11.88 µm) · NCM811/LPSC/VGCF 복합양극의 기공 · ion tortuosity · 동역학 · CAM 70–90 wt%

> slug `lin2025_submicron_lpscl_cathode_li_kinetics` · DOI `10.1039/d4cp03893b` · type `exp (습식 밀링 LPSCl 2 입도 · NCM811/LPSC/VGCF 복합양극 · EIS-τ · CV Randles–Sevcik · DRT · dQ/dV · FIB-SEM · XPS · 시뮬 없음)` · PDF `d697636f-2._Sub-micrometer_Li6PS5Cl_regulated_cathodic_Li_kinetics_in_sulfide_based_all-solid-state_batteries.pdf` (본문 8 pp) + `3eb1fa04-2._Sup_Sub-micrometer_Li6PS5Cl_regulated_cathodic_Li_kinetics_in_sulfide_based_all-solid-state_batteries.pdf` (ESI 9 pp — Fig. S1–S12 · Table S1–S8) · digested `2026-10-30` · status ✅

> topic: size_effect (SE 입도 효과)
> elements: Li, P, S, Cl, Ni, Co, Mn, O, C, In
> methods: EIS, arrhenius, Raman, XRD, CV, Randles-Sevcik, DRT, dQ/dV, XPS, FIB-SEM, SEM-EDS, laser diffraction

<!-- 실독 기록 (2026-10-30, litdb-curator)
     본문 8 쪽 + ESI 9 쪽 전부 읽었다 (pdftotext + 쪽 렌더).  크롭 25 장 = 본문 그림 5 + ESI 그림 12 + ESI 표 8
     (200 dpi pdftoppm → PIL, 임베디드 래스터 bbox 기준 + 흰 테두리 다듬기) — 전부 열어 확인했다.
     판독 근거로 Fig. 1c·1f · 2d · 3a·3b · 5a–d 는 500 dpi 로 따로 확대해 읽었다.
     ESI 의 Table S1 · S2 · S4 · S8 은 그림(래스터) 표라 텍스트로 안 나온다 → 크롭을 읽어 옮겼다.
     표기 규약: 논문에 적힌 값 = stated · 그림에서만 읽은 값 = 판독 ≈ · 논문에 없는 계산 = 우리 산수.
     쪽 표기: 본문 = 저널 쪽 p. 3455–3462 (PDF 1–8) · ESI = 인쇄 쪽 = PDF 쪽 (ESI p. 1–9).
     pdftotext 는 µ 를 'm' 로 뽑는다 ("10 mm" = 10 µm) — 그림·캡션으로 단위를 확인했다. -->

## 0. 이 digest 를 읽는 법 — 왜 지금 이 논문인가, 그리고 원문 판정

**계기 (2026-10-30)**: 50 kg 4차년도 DEM 보고 (SE D50 0.7 · 1 · 2 · 3 µm 단분산 대리 · NCM D6 µm · 85 wt% · 300 MPa) 의
문헌 지도 `docs/50kg/report_y4/lit_se_size_map_20261030.md` §6 이 이 논문을 **2순위** 로 올렸다 —
*"서브 µm LPSCl 복합양극 비교 — 우리 D0.7 자리 (p2 · p4)"*.  원문으로 확인한 판정:

| Q | 판정 (한 줄) | 근거 |
|---|---|---|
| **Q1 정말 서브 µm 인가** | **D50 기준으로는 아니다.** 레이저 회절 **D50 SU-LPSC 2.34 µm · IN-LPSC 11.88 µm** (stated). "sub-micrometer" 는 SEM 인상 (*"some particles around 2 µm and most reaching the nanoscale"*) 과 분포의 미분 꼬리 (≈0.1 µm 부터, 판독) 를 가리킨다. 가중 기준 (부피 / 개수) · 장비 미기재 | p. 3456 · `Fig. S2` · `Fig. 1a,b` · `Fig. S1` |
| **Q2 순수 SE σ** | **4.96 → 1.51 mS cm⁻¹ (×3.28 ↓)** · Ea **0.296 → 0.357 eV** · 결정성 (Table S3) ↓. SU 는 IN 을 **습식 볼밀 (800 rpm · 2 h · 시클로헥산) 한 뒤 재열처리 없이** 건조 (Table S2: 120 °C · 24 h) 한 것 ⇒ **입도와 밀링 손상이 함께 바뀐 시료** | p. 3456 · p. 3460 · `Fig. 1c,f` · `Table S1`–`S3` |
| **Q3 복합체 기공 · τ** | 기공 **21.12 → 18.68 %** (**450 MPa**, `Table S4` — 셀 성형압 640 MPa 와 다르다) · "ion tortuosity" **3.91 → 1.77** (식 τ² = σ_ion,SE·ε_SE/σ_ion,eff). **σ_ion,eff · ε_SE · 어느 σ_ion,SE 를 넣었는지 전부 미보고** → 재계산 불가 (§3h 2×2 표) | p. 3459 · `Table S4` · `Table S5` |
| **Q4 성능** | 10 mg cm⁻² · RT: 0.1C 첫 방전 **175.7 → 197.5 mAh g⁻¹** · ICE **80.0 → 82.4 %** · 0.5C 200 사이클 유지 **84.7 → 93.4 %** · 3C **≈38 (판독) → 62.9** | p. 3457 · `Fig. 2` |
| **Q5 높은 AM 분율** | SU 로만 70–80 wt% (`Table S8`): 80 wt% · 20 mg cm⁻² 에서 200 사이클 **74.6 %**. 85 · 90 wt% 셀은 ESI 그림만 (조성 미기재) | `Fig. 5` · `Table S8` · `Fig. S11`–`S12` |

⇒ **지도 §6 판정을 고친다**: 이 논문의 SU-LPSC 는 *"우리 D0.7 자리"* 가 아니라 **D50 기준 우리 D2–D3 대역** (IN-LPSC 는 D3 바깥) 이고,
성격은 **밀링 손상 교란형 미립화** 다 — 그래서 주 자리는 **p5 (구조 효과 ↔ 물성 가정 분리)** 이고 p2 · p4 는 보조다.
D0.7 대역에 해당하는 것은 SU 분포의 **미분 꼬리 (개수 기준)** 뿐이다.  NCM811 입도가 보고되지 않아 **D_AM/D_SE 도 정할 수 없다**.

---

## 1. 한 줄 요약

고상 합성한 Li₆PS₅Cl (IN-LPSC, D50 11.88 µm, 4.96 mS cm⁻¹) 을 **습식 볼밀로 잘게 만든** SU-LPSC (D50 2.34 µm, 1.51 mS cm⁻¹ — 펠릿 σ 가 3.3 배 낮다)
를 NCM811/LPSC/VGCF (70:27:3 wt%) 복합양극에 넣으면, 펠릿 σ 손해에도 불구하고 **기공 (21.12 → 18.68 %) 과 "ion tortuosity" (3.91 → 1.77) 가 줄고**,
CV 겉보기 확산계수 (+65.7 %) · 첫 사이클 용량 · 율특성 · 200 사이클 유지 (84.7 → 93.4 %) 가 모두 좋아진다는 실험 논문.
저자 서사는 *"미립 SE 가 빈틈을 메우고 NCM 을 코팅처럼 감싸 Li⁺ 경로를 늘리고, 부피 변화의 응력을 완충한다"* 이다.
⚠ 핵심 수송 수치 (τ) 는 **원 σ_eff 와 정규화 규약이 빠져** 있어 재현할 수 없고, 기공 차는 **두께 0.97 vs 1.00 mm 한 자리 차** 위에 서 있다 (§10).

## 2. 메타 / 동기 / 질문

| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Yuanyuan Lin**, Hanzhou Liu, Yaqi Hu, **Yang Lu\***, Zongliang Zhang, Yang Liu, Yongle Chen, Kun Zhang, Shuo Yin, **Fangyang Liu\*** (Central South University · Hunan Energy Frontiers New Materials Technology Co. · GEM Co. · CNGR Advanced Material Co.) | *Phys. Chem. Chem. Phys.* **27**, 3455–3462 (2025) · 접수 2024-10-10 · 수락 2025-01-21 · 게재 2025-01-27 | 10.1039/d4cp03893b | **Li₆PS₅Cl** 두 입도 (자체 합성 IN · 습식 밀링 SU) + **NCM811** (LiNi₀.₈Co₀.₁Mn₀.₁O₂, 출처 · 입도 · 코팅 미기재) + **VGCF 3 wt%** (Showa Denko) · 분리막 IN-LPSC · 대극 Li–In | 실험 (펠릿 EIS · 반쪽셀 사이클 · CV · EIS/DRT · FIB-SEM · XPS) — **시뮬 없음** |

- **동기 (p. 3455–3456)**: 복합양극 성능은 CAM–SSE 고체 접촉에 달려 있고, SSE 는 작은 기공에 스며들지 못한다 (ref 17 Bielefeld 2022). 시뮬 선행 (ref 18 Bielefeld 2019: CAM 3 µm 유리) · Shi (ref 19, *"conductor 입자를 2–3 배 줄이면 이용률 20 → 100 %"*) · Minnmann 2024 (ref 20, ISE D50 4.93 µm 가 균질 · 높은 계면 · 낮은 tortuosity) 가 있으나 *"실험 검증이 부족하다"* 는 문제 제기.
- **질문**: 서브 µm LPSC 가 복합양극의 Li 동역학 (확산 · 계면 저항 · tortuosity) 과 사이클 · 율 성능을 어떻게 바꾸나 + CAM 분율 70–80 wt% 에서 최적 배합은.
- **이해관계 (p. 3461)**: *"There are no conflicts to declare."* — 단 공저자 3 명이 소재 기업 (Hunan Energy Frontiers · GEM · CNGR) 소속이고, Li₂S · P₂S₅ 도 Hunan Energy Frontiers 제품 (p. 3460).
- **자금**: NSFC 22109084 · 52474338, 후난성 R&D 2024JK2093 · 2023GK2016, 후난성 자연과학기금 2022JJ40627, CSU 2023XQLH159 (p. 3461).

## 3. 핵심 수치 총정리 ★

### 3a. 재료 · 배합

| 항목 | 값 | 표기 | 출처 |
|---|---|---|---|
| IN-LPSC 합성 (본문) | Li₂S · P₂S₅ (Hunan Energy Frontiers) · LiCl (Aladdin) 화학양론 → ZrO₂ 볼밀 **500 rpm · 6 h** → **450 °C · 8 h** 소성 | stated | p. 3460 |
| ⚠ IN-LPSC 합성 (ESI) | `Table S1` "Our work" 행 = **800 rpm · 2 h · 500 °C · 8 h** → 4.96 × 10⁻³ S cm⁻¹ — **본문과 다르다** (SU 의 밀링 조건이 섞인 것으로 보임) | stated | ESI p. 6 |
| SU-LPSC 제조 | IN-LPSC 를 ZrO₂ 볼밀 **800 rpm · 2 h · 시클로헥산 (99.5 %) · 실온** → 손 분쇄 · 체가름. `Table S2` "Our work" = 800 rpm · 2 h · 건조 **120 °C · 24 h** → 1.5 × 10⁻³ S cm⁻¹. **재소성 없음** | stated | p. 3460 · ESI p. 6 |
| PSD (레이저) | **D50 SU 2.34 µm · IN 11.88 µm** — 장비 · 부피/개수 기준 미기재 | stated | `Fig. S2` 캡션 |
| PSD 모양 | 모드 SU ≈2.8 · IN ≈14 µm · 범위 SU ≈0.1–60 µm (꼬리 ≈200) · IN ≈0.5–250 µm · SU 에 0.2–0.5 µm 어깨 | 판독 ≈ | `Fig. S2` |
| SEM 인상 | IN *"typically around 10 µm"* · SU *"some particles around 2 µm and most reaching the nanoscale"* | stated | p. 3456 · `Fig. 1a,b` |
| NCM811 | LiNi₀.₈Co₀.₁Mn₀.₁O₂ — **공급사 · 입도 · 코팅 · 단결정/다결정 미기재** | — | p. 3460 |
| 복합양극 (SU 계열) | NCM811 : SU-LPSC : VGCF = **70:27:3 (70SU) · 72:25:3 · 74:23:3 · 76:21:3 · 78:19:3 · 80:17:3** wt% · 손 혼합 12 min | stated | p. 3460 |
| IN 복합양극 | 같은 70:27:3 로 읽힌다 (`Table S6` "70IN-cathode") — 본문 명시 없음 | 우리 판독 | ESI p. 7 |
| CAM 로딩 | **10.0 · 20.0 mg cm⁻²** (NCM811 기준) | stated | p. 3460 |
| 셀 | ∅10 mm 금형: 복합양극 + **IN-LPSC 분리막 130 mg** + In 박 100 µm → **640 MPa** 3층 압착 → In 위 Li 1.5 mg → 2032 코인 · 사이클 중 스테인리스 케이스 **50 MPa** | stated | p. 3460 |
| ⚠ 분리막 양 | `Table S8` "SE/mg" 열 = **120** (본문 130 과 다름) | stated | ESI p. 8 |
| CV 셀 | LPSC : VGCF = 9 : 1 (손 혼합 12 min) + LPSC + In 박 → 640 MPa | stated | p. 3460 |

### 3b. 순수 SE — 입도와 밀링 손상이 함께 움직인다

| 물성 | IN-LPSC | SU-LPSC | 조건 | 표기 · 출처 |
|---|---|---|---|---|
| σ (25 °C) | **4.96 mS cm⁻¹** | **1.51 mS cm⁻¹** | 강철‖LPSC‖강철 (PEEK), EIS 5 MHz–1 Hz · 10 mV, Gamry Ref 600+ | stated · p. 3456 · `Fig. 1c` 삽도 |
| Nyquist 저주파 절편 | ≈40 Ω cm² | ≈132 Ω cm² | 축 "Ω cm²" | 판독 ≈ · `Fig. 1c` |
| Ea | **0.296 eV** | **0.357 eV** | Arrhenius ln(σ·T) vs 1000/T (3.0–3.35 K⁻¹) | stated · `Fig. 1f` |
| Arrhenius 기울기 재판독 | ≈ −3.6 kK → ≈0.31 eV | ≈ −4.3 kK → ≈0.37 eV | 끝점 두 개로 | 판독 + 우리 산수 · `Fig. 1f` |
| Arrhenius 25 °C 수준 | ln(σT) ≈ 0.14 → σ ≈ **3.9 mS cm⁻¹** | ≈ −1.24 → σ ≈ **1.0 mS cm⁻¹** | 1000/T = 3.355 (298 K) | 판독 + 우리 산수 — 본문값보다 22 · 36 % 낮다 (§10-6) |
| XRD | 전 피크 LPSC (ref. 97-041-8490) | 넓은 피크 = 나노결정 | Cu Kα, 10–80° | stated · `Fig. 1d` |
| "main peak crystallinity" | 85.21 / 80.21 / 86.15 % | 84.66 / 76.41 / 85.99 % | Peak 1–3 · **정의 미기재** | stated · `Table S3` |
| Raman | PS₄³⁻ 단일 강 피크 | 같은 위치, 세기 약간 ↓ · 폭 ↑ | 532 nm | stated · `Fig. 1e` |
| 저자 해석 | 볼밀 파쇄로 표면 결함 · 원자 무질서 ↑ → 결정성 · σ ↓ · Ea ↑ | | | stated · p. 3456 |

- ⇒ **우리 산수**: σ 비 4.96/1.51 = **3.285**, 입도 비 11.88/2.34 = **5.08**. 절편 비 ≈132/40 = 3.3 이 σ 비와 같으므로 두 펠릿 두께가 같았다고 읽히고, "Ω cm²" 를 면적 저항으로 읽으면 L = σ·R_A ≈ **0.20 cm** (두 펠릿 모두; 논문은 두께 미보고).
- CV 안정성 (`Fig. S3`): *"consistent intensities, without any additional oxidation–reduction peaks … no parasitic reaction"* (p. 3456). ⚠ 곡선 모양은 §10-7.

### 3c. 복합체 미세구조 — 기공 · 단면

| 항목 | SU-LPSC 양극 | IN-LPSC 양극 | 표기 · 출처 |
|---|---|---|---|
| ε_void (**450 MPa**) | **18.68 %** | **21.12 %** | stated · `Table S4` |
| `Table S4` 원자료 | AM:SE 70:30 w% · m 0.20 g · d 10.00 mm · **h 0.97 mm** · "V_solid" 76.18 mm³ | 70:30 · 0.20 g · 10.00 mm · **h 1.00 mm** · 78.54 mm³ | stated |
| FIB-SEM 단면 (초기) | 기공 · 틈 적음, NCM 이 SU 에 고르게 둘러싸임 (*"similar to a cathode coating"*) | 기공 다수, **NCM811 끼리 직접 접촉** (파란 원) — 고르지 않은 분포 | stated · `Fig. 4a` · p. 3458 |
| FIB-SEM (200 사이클 뒤) | 틈 적고 밀착 유지 | NCM–LPSC 사이 큰 틈 (파란 사각) | stated · `Fig. 4a` |
| 평면 SEM (640 MPa) | 매끈 · 치밀 · 기공 · 균열 적음 | 상대적으로 거침 | stated · `Fig. 2b,c` · p. 3456 |
| 단면 SEM-EDS | 균일 분포 · 큰 기공 감소 | 큰 LPSC 입자 불균일 분산 | stated · `Fig. S7`–`S8` · p. 3458 |

- ⚠ **우리 산수 — `Table S4` 의 "V_solid" 는 고체 부피가 아니라 펠릿 전체 부피다**: π·(5.00 mm)²·0.97 mm = **76.18** · π·25·1.00 = **78.54 mm³** 로 정확히 같다.
  거꾸로 V·(1 − ε) 를 구하면 두 시료 모두 **61.95 mm³** = 같은 가정 고체 밀도 0.20 g / 61.95 mm³ = **3.23 g cm⁻³** (논문 미보고).
  ⇒ 두 기공값의 차 (2.44 %p) 는 **오직 두께 0.97 vs 1.00 mm (0.03 mm) 에서** 나오고, 두께 한 자리 (0.01 mm) 가 기공 **≈0.8 %p** 에 해당한다 (§10-2).

### 3d. 이온 수송 — "ion tortuosity" (원 σ_eff 없음)

| 항목 | 값 | 표기 · 출처 |
|---|---|---|
| 측정 셀 | 전자차단: **Li 금속 ‖ LPSC 층 ‖ 복합양극 ‖ LPSC 층 ‖ Li 금속**, EIS (ref 41) | stated · p. 3458–3459 |
| 식 | **τ² = (σ_ion,SE / σ_ion,eff) · ε_SE** (ref 42) — σ_ion,SE = LPSC 벌크 σ · ε_SE = LPSC 부피분율 | stated · p. 3459 |
| 보고값 | **SU 1.77 · IN 3.91** (*"ion tortuosity"*) | stated · p. 3459 · 결론 |
| 미보고 | σ_ion,eff (두 양극) · ε_SE · **어느 σ_ion,SE (4.96 · 1.51 · 다른 값) 를 썼는지** · 셀 두께 · 적합 회로 | — |
| `Table S5` 비교 | 액체 전해질 다공 전극의 tortuosity 와 나란히: 시뮬 0.35/2.6 · NMC 0.40/≈1.7 · LCO 0.40/≈1.85 · 흑연 0.40/≈1.8 · NCA 0.43/1.5–2.5 · LMO 0.63/2.9 · **"Our work" NCM811 0.19/1.77** (porosity / tortuosity) | stated · ESI p. 7 |

### 3e. 전기화학 성능 (10 mg cm⁻² · RT · 2.4–3.7 V vs Li⁺/Li–In · 1C = 170 mA g⁻¹ · 첫 3 사이클 0.1C 활성화 뒤 0.5C)

| 항목 | SU-LPSC | IN-LPSC | 표기 · 출처 |
|---|---|---|---|
| 율 0.1 / 0.2 / 0.3 / 0.4* / 1 / 2 / 3 C | **194.8 / 184.0 / 175.6 / 161.2 / 131.5 / 89.6 / 62.9** → 0.1C 회복 **190.9** | ≈178 / ≈162 / ≈150 / ≈133 / ≈103 / ≈63 / ≈38 → ≈168 | SU stated · IN 판독 ≈ · p. 3457 · `Fig. 2d` (*그림 단계 표지는 **0.5 C**) |
| 0.1C 첫 방전 · ICE | **197.5 mAh g⁻¹ · 82.4 %** | **175.7 · 80.0 %** | stated · `Fig. 2e` |
| 0.5C 200 사이클 | **169.0 mAh g⁻¹ · 93.4 %** | 유지 **84.7 %** | stated · `Fig. 2f` |
| 20 mg cm⁻² 첫 방전 (0.1C) · CE | **184.7 · 84.0 %** | — | stated · `Fig. 2g` |
| 20 mg cm⁻² 0.5C 200 사이클 | **135.5 · 93.8 %** | 유지 **83.4 %** | stated · `Fig. 2h` |
| 0.05C 첫 방전 · ICE | **209.2 · 84.0 %** | ICE **79.8 %** | stated · `Fig. 2i` |
| 1C 200 사이클 | **152.5 · 93.3 %** | 유지 **84.3 %** | stated · `Fig. 2j` |
| 반복성 n = 5 — 첫 방전 | ≈196.5–200 (평균 ≈198.5) | ≈180.8–188.3 (평균 ≈183) | 판독 ≈ · `Fig. S10a` |
| 반복성 — ICE | ≈82.5–83.4 % | ≈78.8–81.6 % | 판독 ≈ · `Fig. S10b` |
| 반복성 — 200 사이클 유지 (0.5C) | ≈92.3–95 % | ≈81.4–85.8 % | 판독 ≈ · `Fig. S10c` |

- 초록 · 결론의 *"ICE +2.4 %"* = 82.4 − 80.0, *"retention +8.7 %"* = 93.4 − 84.7 (%p, 우리 산수 — 상대 % 가 아니다).
- 우리 산수: 1C = 170 mA g⁻¹ × 10 mg cm⁻² = **1.70 mA cm⁻²** · `Table S8` 면적 용량 1.97 mAh cm⁻² = 197.5 × 0.010 ✓.

### 3f. 동역학 · 계면 (CV · dQ/dV · EIS · DRT · XPS)

| 항목 | SU-LPSC | IN-LPSC | 표기 · 출처 |
|---|---|---|---|
| Randles–Sevcik 겉보기 D | **1.38 × 10⁻⁸ cm² s⁻¹** | **8.33 × 10⁻⁹ cm² s⁻¹** (+65.7 %) | stated · p. 3457 |
| 식 | I_p = 2.69 × 10⁵ n^{3/2} A D^{1/2} C v^{1/2} — n · A · C 는 "상수" (값 미기재) | | stated · p. 3457 |
| I_p–v^{1/2} 기울기 (O1 · H1→M) | ≈1.21 | ≈0.99 (×10⁻³ A per 10⁻² (V s⁻¹)^{1/2}) → 비 ≈1.22 → **D 비 ≈1.49** | 판독 + 우리 산수 · `Fig. 3a` |
| 기울기 (R1 · M→H1) | ≈1.24 | ≈0.90 → 비 ≈1.38 → **D 비 ≈1.90** | 판독 + 우리 산수 · `Fig. 3b` |
| CV 0.1 mV s⁻¹ 피크 | 산화 0.052 · 환원 0.041 A g⁻¹ | 산화 0.055 · 환원 0.038 A g⁻¹; 1→3 사이클 산화 0.055 → 0.051 · 환원 0.039 → 0.037 | stated · p. 3457–3458 · `Fig. 3c` |
| dQ/dV ΔV (100 사이클) | **93.47 mV** | **137.94 mV** | stated · `Fig. 3d,e` |
| 셀 임피던스 | 초기 ≈30 Ω → 첫 충전 뒤 **56 Ω** | ≈30 Ω → **99 Ω** · 100 사이클 뒤 초기의 2 배 | stated · p. 3458 · `Fig. 3f,g` |
| 등가회로 | R_s – (R_gb‖CPE₁) – (R_ct‖CPE₂) – W_s | | stated · `Fig. S5` |
| DRT CEI 대역 | 본문 10⁻⁶–10⁻¹ s (그림 음영 ≈10^−5.6–10^−2 s, 판독) | | stated / 판독 · p. 3458 · `Fig. S6` |
| DRT CEI 피크 γ | ≈5–9 Ω (사이클 내내 낮음) | ≈15 → ≈20 → ≈29 Ω (1st-charge → 50th → 100th) | 판독 ≈ · `Fig. S6` |
| XPS P 2p "ScanB" (2p₃ / 2p₁) | 1st 0.07 / 0.04 · 200th 0.09 / 0.05 | 1st 0.29 / 0.15 · 200th 0.24 / 0.12 | stated · `Table S6`–`S7` |
| XPS S 2p "ScanB" | pristine 0.11 / 0.05 · 1st 0.39 / 0.20 · 200th 0.43 / 0.22 | 0.15 / 0.08 · 0.33 / 0.17 · 0.52 / 0.27 | stated |
| XPS S 2p "ScanC" | 1st 0.25 / 0.13 · 200th 0.14 / 0.07 | 0.15 / 0.07 · 0.12 / 0.06 | stated |

- XPS 해석 (본문): *"intensities of the sulfite and phosphate peaks are nearly identical … no oxidation"* (p. 3459). `Fig. S9` 는 P 2p 에 "Phosphates", S 2p 에 "Li₂S · Bridging S · CoS" 를 표지하지만 **Scan A/B/C ↔ 화학종 대응은 표에 없다** [미확인] (§10-8).

### 3g. CAM 분율 계열 (SU-LPSC · `Table S8` 전문 "Our work" 6 행 · `Fig. 5`)

| CAM wt% | 로딩 (mg cm⁻²) | 첫 방전 (mAh g⁻¹) | ICE (%) | 면적 용량 (mAh cm⁻²) | 0.5C 200 사이클 |
|---|---|---|---|---|---|
| 70 | 10 | **197.5** | 82.4 | 1.97 | 168.9 mAh g⁻¹ · **93.4 %** |
| 70 | 20 | **184.7** | 84.0 | 3.69 | 135.5 · **93.8 %** |
| 74 | 10 | **195.1** | 84.2 | 1.95 | 160.9 · **92.8 %** |
| 74 | 20 | **190.3** | 84.7 | 3.81 | 108.4 · **83.9 %** |
| 80 | 10 | **191.1** | 83.1 | 1.91 | 131.7 · **85.6 %** |
| 80 | 20 | **180.1** | 82.1 | 3.60 | 76.7 · **74.6 %** |

- 74SU 율 (stated, p. 3459): 0.1C **203.1** · 0.2C **194.3** · 0.3C **186.6** · 0.5C **175** · 1C **150.5** · 2C **100.3** · 회복 **201.5 mAh g⁻¹**.
- `Fig. 5c` 판독 (10 mg cm⁻², 1C / 2C / 3C): 70SU ≈131 / ≈91 / ≈63 · 72SU ≈143 / ≈100 / ≈67 · 74SU ≈146 / ≈100 / ≈69 · 76SU ≈130 / ≈84 / ≈55 · **78SU ≈108 / ≈57 / ≈32 · 80SU ≈56 / ≈25 / ≈12** — 76 → 80 wt% 에서 고율 용량이 무너진다.
- **85SU** (`Fig. S11`, 10 mg cm⁻² · 0.5C): 첫 충전 ≈222 · 방전 ≈183 mAh g⁻¹ · 0.5C ≈118 → 200 사이클 ≈104 (판독). **90SU** (`Fig. S12`): ≈211 · ≈168 · 0.5C ≈84 → ≈69 (판독). **두 배합의 SE : VGCF 비는 어디에도 없다** [미확인].
- 저자 결론: *"74 % … exhibits the best high-rate performance, excellent first-cycle … and long-term cycling retention"* (p. 3459). ⚠ 유지율 최고는 표에서 **70 wt%** 다 (§10-10).
- 문헌 비교 (`Fig. 5d` · `Table S8` 위 9 행): Ref [52] NCM811 0.5C 135 / 84 % · [53] NCM811 0.1C 192 / 86 % · [54] NCM622 0.3C 165 / 80 % · [50] NCM712 0.1C 153 / 92 % · [55] NCM712 0.1C 168 / 99 % · [56] NCM811 0.2C 160 / 95 % · "Our work" NCM811 **0.5C** 197 / 94 % (stated 그림 숫자).

### 3h. 우리 산수 (논문 미보고 — 입력은 stated 값 · 표지된 판독값)

**(1) "ion tortuosity" 의 두 모호성 → σ_eff 비의 2 × 2 표.**
논문은 식 τ² = σ_SE·ε_SE/σ_eff 를 적고 **"ion tortuosity" = 1.77 · 3.91** 을 준다. 두 가지가 불명이다 — ⓐ 보고값이 τ 인가 τ² 인가 ⓑ σ_SE 로 각 시료 자기 값 (IN 4.96 · SU 1.51) 을 썼나 공통 값을 썼나.
φ_SE 비 SU/IN ≈ **1.031** (고체 분율 비 (1 − 0.1868)/(1 − 0.2112), 고체 안 SE 비율이 같다고 가정) 로 두면:

| 읽기 | τ²_IN/τ²_SU | σ_eff,SU / σ_eff,IN | 자기 σ_SE 로 정규화한 f 의 비 (SU/IN) | σ_SE 손해 (×3.285) 를 넘나 |
|---|---|---|---|---|
| A-자기 σ_SE (보고값 = τ) | 4.880 | **1.53** | 5.03 | ✓ |
| A-공통 σ_SE | 4.880 | **5.03** | 16.5 | ✓ |
| B-자기 σ_SE (보고값이 실은 τ²) | 2.209 | **0.69** | 2.28 | ✗ |
| B-공통 σ_SE | 2.209 | **2.28** | 7.48 | ✓ |

⇒ **넷 중 셋에서 "구조 이득 > 펠릿 σ 손해"** (SU 복합체의 σ_eff 가 더 높다) 이고, B-자기 규약 하나에서만 거꾸로다. **원 σ_eff 가 없어 어느 칸인지 가를 수 없다.**

**(2) 우리 규약 (CLAUDE.md τ 명명) 으로 옮기면** — 식 그대로 (읽기 A) 보고값이 √ 값이면 우리 **수송 tortuosity (tau2 = φ_SE·σ₀/σ_eff)** = **SU 3.13 · IN 15.29** (1.77² · 3.91²). 읽기 B 면 1.77 · 3.91 그대로. ⚠ 어느 쪽이든 σ₀ 가 무엇인지 모른다.

**(3) 기타**: `Table S4` 공통 고체 부피 61.95 mm³ · 함의 고체 밀도 3.23 g cm⁻³ · 두께 0.01 mm ↔ 기공 ≈0.8 %p (§3c) · 펠릿 두께 ≈0.20 cm (§3b) · σ 비 3.285 · 입도 비 5.08 · 1C ≈1.70 mA cm⁻² (§3e).

---

## 4. 재료 & 방법 — 같은 축을 흉내 낼 때 필요한 조건 ★

### 4a. 합성 · 미립화 (p. 3460 · `Table S1`–`S2`)
- IN-LPSC: 고상 (볼밀 500 rpm · 6 h → 450 °C · 8 h). ⚠ ESI 표는 800 rpm · 2 h · 500 °C · 8 h.
- SU-LPSC: IN-LPSC → 습식 볼밀 800 rpm · 2 h · 시클로헥산 → (ESI) 120 °C · 24 h 건조 → 손 분쇄 · 체가름. **재소성 없음.** 전 공정 Ar 글러브박스 (O₂ · H₂O < 0.1 ppm).

### 4b. 복합양극 · 셀 (p. 3460)
- NCM811 : LPSC : VGCF = 70–80 : 27–17 : 3 wt% · 손 혼합 12 min · ∅10 mm · 640 MPa 3층 (양극 · IN-LPSC 130 mg · In 100 µm) · Li 1.5 mg · 2032 코인 · 사이클 50 MPa 케이스.
- ⚠ 기공 측정 (`Table S4`) 은 **450 MPa** · AM:SE **70:30** w% (VGCF 미표기) · 0.20 g 펠릿 — 셀 성형 조건 (640 MPa · 70:27:3) 과 같은 시료인지 불명.

### 4c. 측정 (p. 3460–3461)
- 펠릿 σ: 강철‖LPSC‖강철 PEEK 금형 · Gamry Reference 600+ · 5 MHz–1 Hz · 10 mV · 25 °C (성형압 미기재).
- 정전류: LAND CT2001A · 2.4–3.7 V (vs Li⁺/Li–In) · *"at various temperatures (25 °C/60 °C)"* — 실린 자료는 전부 RT.
- EIS (셀): 5 MHz–0.01 Hz · 10 mV · Gamry 600+. CV: Squidstat Prime · 2.0–4.0 V · 0.05–0.40 mV s⁻¹ (Randles–Sevcik 에는 0.10–0.40 의 7 점, `Fig. 3a`).
- τ: 전자차단 Li‖LPSC‖복합‖LPSC‖Li 대칭셀 EIS (두께 · 적합 미기재).
- 구조: XRD PANalytical Cu Kα 10–80° · 0.0263° · 1 s · 폴리이미드 10 µm 창 / Raman HORIBA LabRAM HR800 532 nm 100–2000 cm⁻¹ / FE-SEM JEOL 7900F (5 kV · BSE 10 kV) + EDS EDAX 15 kV / **FIB-SEM ZEISS Crossbeam 540** (진공 이송) / XPS Thermo Escalab 250Xi (전 스펙트럼 150 eV · 0.1 eV 스텝 단일 원소 60 eV · 5 회).
- DRT (ESI p. 3): MATLAB 2021b DRTtools · Gaussian process · 실부+허부 결합 · 인덕턴스 없이 · 1차 미분 벌칙 · λ = 10⁻³ · 표본 10,000.

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 SU-LPSC 의 준비와 성질 (`Fig. 1`, `Fig. S1`–`S3`, `Table S1`–`S3`)
SEM (`Fig. 1a,b`, 5 µm 눈금) 에서 IN 은 10 µm 급 덩어리, SU 는 2 µm 이하 조각이 대부분이다. EDS (`Fig. S1`) 로 SU 는 P · S · Cl 이 고르게, IN 은 큰 덩어리에 몰려 보인다.
레이저 PSD (`Fig. S2`) 는 SU 가 IN 보다 한 자릿수 왼쪽으로 옮겨 갔지만 **D50 = 2.34 µm** 이고 0.1 µm 부터 60 µm 너머까지 넓다.
σ 는 4.96 → 1.51 mS cm⁻¹, Ea 는 0.296 → 0.357 eV, XRD 피크가 넓어지고 Raman PS₄³⁻ 피크가 약해진다 — 저자는 이를 **볼밀이 만든 표면 결함 · 원자 무질서** 로 해석한다 (refs 24–27).
⇒ 이 비교의 SE 는 **작아졌고 동시에 손상됐다** (Cronau 2022 의 습식 밀링 손상 서사와 같은 부류).

### 5.2 복합양극 성능 (`Fig. 2`, `Fig. S10`)
70 wt% · 10 mg cm⁻² 에서 SU 양극이 모든 율에서 높고 (차이는 고율에서 커져 3C 에서 ≈1.65 배, 판독 기준 우리 산수), 첫 사이클 용량 · ICE · 200 사이클 유지가 모두 높다.
20 mg cm⁻² 와 0.05C/1C 조건에서도 유지율 차 (≈93 vs ≈84 %) 가 같은 크기로 남는다. n = 5 반복 (`Fig. S10`) 에서 두 군의 분포가 겹치지 않는다 (판독).

### 5.3 동역학 진화 (`Fig. 3`, `Fig. S4`–`S6`)
Randles–Sevcik 기울기가 SU 에서 크다 → 겉보기 D +65.7 %. 첫 충전 뒤 셀 임피던스가 SU 56 Ω · IN 99 Ω 으로 벌어지고, DRT 의 CEI 대역 (10⁻⁶–10⁻¹ s) 피크가 IN 에서만 사이클과 함께 커진다.
dQ/dV 의 100 사이클 분극 ΔV 는 SU 93.47 mV · IN 137.94 mV. 저자 해석: IN 은 기생 반응 산물이 더 많고 (CV 피크 감쇠), SU 의 밀착 접촉이 *"multiple lithium-ion migration path"* 를 만든다.

### 5.4 계면 접촉 (`Fig. 4`, `Fig. S7`–`S9`, `Table S4`–`S7`)
FIB-SEM 단면에서 IN 양극은 기공과 **NCM–NCM 점접촉** 이 보이고, SU 양극은 NCM 이 SU 에 감싸인다. 200 사이클 뒤 IN 은 NCM–LPSC 사이 틈이 커지고 SU 는 유지된다.
저자 기전 (`Fig. 4b,c`): IN 은 빈틈을 못 메우고 부피 변화의 응력을 못 받아 NCM 이 깨진다 / SU 는 *"soft SU-LPSC"* 가 NCM 을 감싸 **응력 완충** + 기공 감소 → τ 3.91 → 1.77.
기공 (`Table S4`) 21.12 → 18.68 %. XPS 는 *"화학 변화 없음"* 으로 결론 (단 §10-8).

### 5.5 CAM 분율 최적화 (`Fig. 5`, `Fig. S11`–`S12`, `Table S8`)
70–80 wt% 계열에서 첫 방전은 거의 같고 (180–198 mAh g⁻¹), **고율 (≥1C) 과 20 mg cm⁻² 장기 유지가 76 wt% 를 넘으면서 떨어진다** (80 wt% · 20 mg cm⁻²: 74.6 %).
저자는 74 wt% 를 최적으로 고르고, 문헌 6 편과 비교해 *"superior"* 라 한다. 85 · 90 wt% 는 ESI 그림 두 장뿐 (본문 언급 없음).

### 5.6 결론 (p. 3460, stated)
*"The reduction of particle size from 10 µm to submicron … facilitate effective gap filling, reduce ionic meandering (1.77 vs. 3.91), and accelerate ion transport kinetics (65.7 % improvement)"* · *"the sub-micrometer electrolyte mitigates internal stress on the electrode resulting from cathode volume expansion"*.

## 6. 우선 질문 — 50 kg 4차년도 보고 쪽 (p1–p7) 기준 원문 대조

| 쪽 | 묻는 것 | 이 논문이 주는 것 | 못 주는 것 |
|---|---|---|---|
| p1 비교 틀 (입도 · D_AM/D_SE) | 입도 표기 기준 | **D50 (레이저) 2.34 vs 11.88 µm + SEM "서브 µm" 인상의 괴리** = 우리 단분산 대리 입도를 부피/개수 기준과 함께 적어야 하는 이유 | **CAM 입도 → D_AM/D_SE 불가** · 분포 폭 수치 (D10/D90) 없음 |
| p2 공간 점유 · 압밀 | 복합체 기공 | 70 wt% 펠릿 기공 21.12 → 18.68 % (450 MPa) — 방향 | 압력 곡선 · 언로딩 전 상태 · 두께 분해능 (0.01 mm ↔ 0.8 %p) |
| p3 접촉 · 피복 | 피복 | FIB-SEM 정성 (*"coating 처럼"*, NCM–NCM 점접촉) | 피복률 · 접촉 수 수치 없음 |
| p4 연결성 · 병목 | 수송 tortuosity | "ion tortuosity" 3.91 → 1.77 | **σ_eff · σ₀ · ε_SE · τ/τ² 구분** 없음 → 우리 tau2 와 수치 대조 불가 (§3h) |
| p5 구조 ↔ 물성 분리 | 펠릿 σ 손해 vs 구조 이득 | **σ 비 3.285 (밀링 SE)** + 복합체 성능은 그래도 향상 · 2 × 2 읽기 중 3 칸이 손익분기 통과 | σ_eff 직접값 · 밀링 없는 같은 크기 대조군 |
| p6 두께 방향 | 분포 | 없음 (응력 완충은 정성 주장) | — |
| p7 경향 · 다음 검증 | 방향 · 고 AM | 작은 SE → 용량 · 율 · 유지 ↑ (70 wt%) · **CAM 76 → 80 wt% 에서 고율 붕괴** · 85/90 wt% 그림 | 85 wt% 조성 · 율 · 입도 대조 없음 |

## 7. 우리 DEM+MPM 대비 ★ (근거 = 작업 브랜치 CLAUDE.md · `docs/50kg/report_y4/storyline_draft1.md` · `lit_se_size_map_20261030.md` — 정본 `our_dem_baseline.md` 는 값 없는 자리표시)

### 7a. 항목별 대조

| 항목 | 이 논문 | 우리 (50 kg 4차년도 DEM) | 차이 / 이유 |
|---|---|---|---|
| SE | LPSCl 자체 합성 · **IN 11.88 / SU 2.34 µm (D50)** · 넓은 분포 · SU = 습식 밀링 손상 | LPSCl **단분산 구** D50 0.7 · 1 · 2 · 3 µm | SU 의 D50 은 **우리 D2–D3 사이** · IN 은 D3 바깥 · 분포 폭 · 미분 꼬리는 우리 침대에 없다 |
| CAM | NCM811 (입도 미보고) | NCM D6 µm 단일 | λ = D_AM/D_SE 대조 불가 |
| 조성 | **70 wt%** (주 비교) · 70–80 wt% (SU) · 85 · 90 wt% (ESI) · VGCF 3 wt% | **85 wt%** · 탄소 · 바인더 없음 | 주 비교가 우리 AM 분율보다 15 %p 낮다; 우리 85 wt% 와 같은 칸은 `Fig. S11` 한 장 (조성 미기재) |
| 압력 | 성형 640 MPa · 기공 측정 450 MPa · 사이클 50 MPa | 300 MPa (목표) · 판 고정 이완 · 언로딩 없음 | 압력 · 상태 (성형 후 vs 가압 중) 모두 다름 → 기공 절대값 같은 줄 비교 금지 (storyline 2쪽 C) |
| 기공 | 21.12 → 18.68 % (펠릿 · 두께법) | 판 고정 기공 D2 16.74 · D3 18.96 % (가압 상태 · 시드 1 · ε_sphere) | 정의 · 상태가 달라 **방향만** — 그리고 우리 두 점도 *"경향 아님"* (storyline 2쪽) |
| 순수 SE σ | 측정 4.96 / 1.51 mS cm⁻¹ (입도 + 손상) | 망 솔버 σ₀ 는 입력 (보고에서는 f 로 나눠 봄 · 손익분기선 = 1저자 펠릿 실측 1 µm 2.3 · 3 µm 5.1) | 이 논문의 σ 비 3.285 는 p5 의 펠릿 σ 비 목록에 새 상단 점 |
| 이온 수송 | τ² = σ_SE·ε/σ_eff (규약 불명) | **f = σ_eff/σ₀ · 수송 tortuosity tau2 = φ_SE·σ₀/σ_eff** (`scripts/network_conductivity.py` · `scripts/tau_flux.py`) | 같은 꼴의 정의 — 그러나 σ₀ · τ/τ² 가 불명이라 숫자는 못 맞댄다 |
| 접촉 형태 | *"NCM 을 코팅처럼 감싼다"* (FIB-SEM) | DEM = 강체 구 + 겹침 대리 (형상 소성 없음) | **등각 피복은 MPM 쪽 현상** (SE 형상 소성 · frame [5]) — DEM 은 겹침 접촉면적 · 피복 (`calc_coverage`) 까지 |
| 전기화학 | 용량 · 율 · DRT · XPS | 없음 (다음 = 3D 전기화학, p7) | 우리가 못 하는 칸 |

### 7b. 50 kg 4차년도 보고 쪽 대응 (문헌 지도 §3 에 넣을 문장 후보)
- **p5 (주 자리)**: 문헌 지도 §3 p5 의 [우리 산술] 밀링 SE σ 비 목록 (MIN24 1.25 · MIN21 1.33 · CRO 1.45 · SHI 2.3 · BAZ25 2.9) 에 **LIN 3.28** 이 들어간다 → 덱의 5.1/2.3 = **2.217 은 "범위 위쪽" 이 아니라 범위 안쪽** 이 된다. 그리고 이 논문은 *"펠릿 σ 가 3.3 배 낮은 밀링 SE 로도 복합양극 성능이 오른다"* 를 보이지만, σ_eff 를 주지 않아 *"손익분기선을 넘었다"* 는 **2 × 2 읽기 중 셋에서만** 성립한다 (§3h). ⇒ 덱 문장은 *"문헌 복합양극 (70 wt%) 은 밀링 SE 의 σ 손해에도 성능이 올랐다 — 단 σ_eff 와 정규화 규약 미보고"* 까지.
- **p4**: 수송 tortuosity 쪽 문헌 예로 쓸 때는 *"보고값 1.77 / 3.91 (τ 로 읽으면 tau2 3.13 / 15.3)"* 처럼 두 읽기를 함께 적는다. f 와 수송 tortuosity 를 독립 성공 둘로 세지 않는다 (`KG50B-03`).
- **p2**: 방향 (작은 SE → 복합체 기공 ↓) 의 문헌 점 하나 — 단 두께 한 자리 차 · 450 MPa 펠릿.
- **p3**: *"코팅처럼 감싼다"* 는 정성 — 우리 피복 지도 (기하 캡 합집합) 와 같은 양이라고 하지 않는다.
- **p7 (문헌 방향 열)**: "작은 SE → 용량 · 율 · 유지 ↑ (70 wt%)" + **"AM 76 → 80 wt% 에서 고율 붕괴"** (`Fig. 5c` 판독). 85 wt% 는 `Fig. S11` 한 장 (조성 미기재) 이라 우리 설계점 근거로는 약하다.
- **p1**: *"서브 µm"* 같은 표기는 부피 D50 이 2 µm 넘을 수 있다 — 우리 단분산 0.7 µm 는 이 논문 SU 보다 **D50 기준 3.3 배 작다** (우리 산수 2.34/0.7).

### 7c. 문헌 지도 속 위치 (표 · 빈도 칸)
- 지도 §1 표에 넣을 행 (안): `lin2025_submicron_lpscl_cathode_li_kinetics` | LPSCl D50 11.88 → 2.34 µm (습식 밀링 · 재소성 없음) | NCM811 (입도 미보고) · 70 wt% · VGCF 3 | 펠릿 σ 4.96 → 1.51 mS/cm · Ea 0.296 → 0.357 eV · 기공 21.12 → 18.68 % (450 MPa) · ion tortuosity 3.91 → 1.77 · 0.1C 175.7 → 197.5 mAh/g · 200 사이클 84.7 → 93.4 % · CAM 70–80 wt% | 기공 · f · tau2 · 피복 | 용량 · DRT · 밀링 σ.
- §2 빈도: T1 (PSD · SEM ✓) · T2 (순수 SE σ ✓) · T3 (기공 ✓) · T4 (FIB-SEM ✓) · T5 (정성) · T6 (✗ — σ_eff 없음) · T7 (✓ 규약 불명) · T9 (✗) · T10 (✓) · T11 (✗ CAM 입도 없음) · T14 (✓ XRD · Raman · Ea) · T15 (정성 주장).
- §2 단서 · 반례 줄에 더할 것: *"밀링 SE 의 σ 비가 3 배를 넘어도 복합체 (70 wt%) 성능은 올랐다 — 다만 σ_eff 미보고"*.

### 7d. frame [4]/[5] 판정
- **frame [5]**: 이 논문은 **실험 쪽 절반 (전기화학 + 영상)** 만 갖고, 구조 → 수송 사슬은 정성 영상과 하나의 τ 로만 말한다. 우리 DEM 이 주는 것 = 같은 입도 축에서 기공 · 접촉망 · f · tau2 · 연결성을 **입력 없이 창발** 시키는 것; 저자가 내세운 *"코팅처럼 감싼다 · 응력 완충"* 은 **SE 형상 소성 (MPM 쪽)** 의 주장이다 — 강체 구 DEM 은 그 형태를 만들지 못하고 겹침 대리로만 흉내 낸다.
- **frame [4]**: 이 논문 값으로 우리 모델을 맞추지 않는다 (교차적합 금지) — 특히 τ 는 규약이 불명이라 앵커 자격이 없다. 쓸 수 있는 것은 **방향** 과 **펠릿 σ 비 (p5 시나리오 입력의 문헌 범위)** 다.
- 이전 가능성 경계: LPSCl ↔ LPSCl (같은 재료) 이지만 **밀링 손상 시료** · NCM 입도 미상 · 70 wt% (우리 85) · 640 MPa 성형 (우리 300) — 숫자 이식 불가, 방향 · 범위만.

---

## 8. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | (a,b) IN · SU SEM (5 µm) · (c) 펠릿 Nyquist (Ω cm²) + σ 막대 4.96 / 1.51 mS cm⁻¹ · (d) XRD (ref 97-041-8490) · (e) Raman PS₄³⁻ · (f) Arrhenius 0.296 / 0.357 eV | **밀링 미립화 = σ ↓ · Ea ↑** 의 원자료 (p5 의 펠릿 σ 비 근거) |
| 2 | (a) 셀 모식 (양극 · LPSC · Li–In · 강철) · (b,c) 640 MPa 평면 SEM (20 µm) · (d) 율 0.1–3 C (10 mg cm⁻²) · (e–j) 0.1C / 0.05C 첫 곡선 + 0.5C · 1C 200 사이클 (10 · 20 mg cm⁻²) | 성능 방향 · 고율에서 차가 커지는 모양 (수송 제한 서명) |
| 3 | (a,b) O1 · R1 피크 전류 vs v^{1/2} · (c) CV 0.1 mV s⁻¹ 1–3 사이클 · (d,e) dQ/dV ΔV 137.94 / 93.47 mV · (f,g) 사이클별 Nyquist (25 Ω 이동) · (h,i) DRT 2D 지도 | 겉보기 D (+65.7 %) · 계면 저항 성장 — 전기화학 (우리 범위 밖) |
| 4 | (a) FIB-SEM 단면 IN · SU × 초기 · 200 사이클 (3 µm) · (b) 응력 완충 모식 · (c) Li⁺ 경로 모식 (ion tortuosity 3.91 / 1.77) | 접촉 형태 정성 · *"코팅처럼"* = MPM 형상 소성 쪽 그림 |
| 5 | (a,b) CAM 70–80 wt% 첫 방전 · ICE · 200 사이클 유지 (10 · 20 mg cm⁻²) · (c) 70SU–80SU 율 · (d) 문헌 6 편 대비 | **고 AM 분율에서 고율 붕괴** (p7 · 우리 85 wt% 맥락) |
| S1 | SU · IN 분말 SEM + P · S · Cl EDS (5 µm) | 분말 형태 |
| S2 | 레이저 PSD — **D50 SU 2.34 · IN 11.88 µm** | ★ "서브 µm" 표기 대 D50 의 괴리 (p1) |
| S3 | IN · SU CV 1 · 2 사이클 (2–4 V vs Li⁺/Li–In) | 밀링 무손상 주장 근거 (§10-7) |
| S4 | IN · SU 양극 CV 0.05–0.40 mV s⁻¹ · O1 / R1 | Randles–Sevcik 원자료 |
| S5 | Nyquist 적합 + 등가회로 R_s–(R_gb‖CPE₁)–(R_ct‖CPE₂)–W_s | 회로 형식 |
| S6 | DRT γ(τ) — IN · SU × 1st-charge · 1st/50th/100th-discharge · CEI 음영 | IN 의 CEI 성장 |
| S7 | IN-LPSC 양극 / LPSC 단면 SEM-EDS (P · S · Cl · O · Co · Ni · Mn) | 큰 LPSC 섬 |
| S8 | SU-LPSC 양극 / LPSC 단면 SEM-EDS | 균일 분포 (정성) |
| S9 | XPS S 2p · P 2p (pristine · 1st · 200th) — Li₂S · bridging S · CoS · phosphates 표지 | 계면 화학 — Table S6/S7 과 함께 (§10-8) |
| S10 | n = 5 반복: 첫 방전 · ICE · 200 사이클 유지 + 사이클 곡선 다발 | 반복성 · 대표 셀 불일치 (§10-9) |
| S11 | **85SU** 첫 곡선 + 0.5C 200 사이클 (10 mg cm⁻²) | ★ 우리 AM 분율 (85 wt%) 근방의 유일한 점 — 조성 미기재 |
| S12 | **90SU** 첫 곡선 + 0.5C 200 사이클 | 고 AM 쪽 끝점 |
| Table S1 | 고상 합성 문헌 6 + "Our work" (800 rpm · 2 h · 500 °C · 8 h · 4.96 × 10⁻³ S cm⁻¹) | 본문 합성 조건과 불일치 (§10-4) |
| Table S2 | 습식 합성 문헌 5 + "Our work" (800 rpm · 2 h · 120 °C · 24 h 건조 · 1.5 × 10⁻³ S cm⁻¹) | SU = 재소성 없는 습식 밀링 |
| Table S3 | 주 피크 결정성 (%) SU 84.66 / 76.41 / 85.99 · IN 85.21 / 80.21 / 86.15 | 손상 지표 (정의 미기재) |
| Table S4 | 70:30 w% · 0.20 g · ∅10.00 · h 0.97 / 1.00 mm · "V_solid" 76.18 / 78.54 mm³ · ε 18.68 / 21.12 % (450 MPa) | ★ 기공 원자료 — "V_solid" 오표기 · 두께 분해능 (§3c) |
| Table S5 | 액체 다공 전극 tortuosity 6 행 + "Our work" 0.19 / 1.77 | 비교 대상 범주 오류 (§10-3) |
| Table S6 | 70IN XPS 면적비 (pristine · 1 · 200) | phosphate (ScanB) 출현 |
| Table S7 | 70SU XPS 면적비 | IN 보다 P 2p ScanB 작음 |
| Table S8 | 문헌 9 행 + "Our work" 6 행 (70 · 74 · 80 wt% × 10 · 20 mg cm⁻²) | ★ CAM 분율 계열 정본 수치 (§3g) |

## 9. Post-processing ★
- **펠릿 σ**: Nyquist 저주파 절편 → σ (L · A 미기재) · Arrhenius ln(σT) vs 1000/T 선형 적합 → Ea.
- **결정성**: XRD 주 피크 3 개의 "crystallinity %" (산출법 미기재).
- **기공**: 질량 · 지름 · 두께 → 기하 부피 · 가정 고체 밀도 → ε_void (`Table S4`).
- **τ**: 전자차단 대칭셀 EIS → σ_ion,eff → τ² = σ_SE·ε_SE/σ_eff (적합 회로 · 두께 미기재).
- **겉보기 D**: CV 피크 전류 vs v^{1/2} 선형 적합 기울기 → Randles–Sevcik (n · A · C 미기재 · 비만 의미).
- **dQ/dV**: 1 vs 100 사이클 산화 · 환원 피크 간격 ΔV.
- **EIS · DRT**: 등가회로 적합 (`Fig. S5`) · DRTtools (Gaussian process · λ = 10⁻³) → γ(τ) 2D 지도 (사이클 축).
- **XPS**: 성분 피크 적합 → 2p₃/2p₁ 면적비 (ScanA 로 정규화).
- **반복성**: n = 5 반바이올린 + 상자 (`Fig. S10`).
- **기록 · 그림**: 용량 mAh g⁻¹ (NCM 기준) · 면적 용량 mAh cm⁻² · σ mS cm⁻¹ · 임피던스 Ω 또는 Ω cm² (그림마다 다름).

## 10. 비판 / 주의 / 한계 ★ (over-claim 방지)

1. **"서브 µm" 은 D50 이 아니다.** 레이저 D50 2.34 µm (`Fig. S2`) · 결론의 *"10 µm to submicron"* 은 SEM 인상. ⇒ 인용 시 *"wet-milled LPSCl with D50 2.34 µm (volume basis not stated)"* 로.
2. **기공 차는 두께 한 자리 차다.** `Table S4` 의 두 기공은 같은 가정 고체 부피 61.95 mm³ 에서 h 0.97 vs 1.00 mm 만 달라 나온 값 (§3c). 0.01 mm 분해능 ↔ ≈0.8 %p → **2.44 %p 차는 측정 분해능의 3 칸**. 반복 · 오차 없음. 측정압 450 MPa ≠ 셀 640 MPa. "V_solid" 열은 펠릿 전체 부피의 오표기.
3. **τ 는 재현 불가 · 비교 대상이 틀렸다.** σ_eff · ε_SE · σ_SE 선택 · τ/τ² 구분이 모두 없다 (§3h 2 × 2). `Table S5` 는 **액체 전해질 다공 전극** 의 tortuosity (전도상 = 기공) 와 나란히 놓고 SU 를 *"porosity 0.19"* 행으로 적는다 — 고체 복합체의 전도상은 기공이 아니라 SE 라 **범주가 다르다**.
4. **합성 조건이 본문 ↔ ESI 에서 다르다**: IN 은 본문 500 rpm · 6 h · 450 °C / `Table S1` 800 rpm · 2 h · 500 °C. 분리막 양도 130 (본문) ↔ 120 mg (`Table S8`).
5. **입도 효과와 밀링 손상이 분리되지 않는다.** SU 는 재소성 없는 습식 밀링 시료 (σ ×1/3.3 · Ea +0.061 eV · 결정성 ↓). 같은 크기의 손상 없는 대조군 (재소성 · 다른 합성) 이 없다 → *"입도가 성능을 올렸다"* 가 아니라 *"작고 손상된 SE 가 크고 손상 없는 SE 보다 나았다"*.
6. **Arrhenius 수준이 본문 σ 와 어긋난다**: `Fig. 1f` 를 25 °C 로 읽으면 ≈3.9 · ≈1.0 mS cm⁻¹ (판독 + 우리 산수) — 본문 4.96 · 1.51 보다 22 · 36 % 낮다. 다른 펠릿이거나 온도 보정 문제 [미확인]. 기울기 (Ea) 만 쓴다.
7. **`Fig. S3` 의 곡선 모양**: 3.2 · 3.6 V 산화 / 3.0 · 3.45 V 환원 피크와 ≈1 mA 세기는 NCM811 상전이 피크와 같은 모양으로 보인다 (우리 판독). 본문이 말한 *"LPSC:VGCF 9:1 CV 셀"* 의 그림인지 확인할 수 없다 [미확인] — *"밀링 뒤 기생 반응 없음"* 근거로 약하다.
8. **XPS 표가 본문 문장과 긴장한다**: 본문은 *"sulfite · phosphate 세기 거의 같음 = 산화 없음"* 이지만 `Table S6`–`S7` 은 사이클 뒤 P 2p "ScanB" 가 새로 생기고 IN 이 SU 보다 크다 (1 사이클 0.29 vs 0.07 = **≈4.1 배** · 200 사이클 0.24 vs 0.09 = **≈2.7 배**, 우리 산수). `Fig. S9` 의 "Phosphates" 표지가 ScanB 라면 *"IN 쪽 산화가 더 크다"* 로 읽힌다 — Scan ↔ 화학종 대응 미기재 [미확인].
9. **대표 셀과 반복 분포가 어긋난다**: IN 대표 첫 방전 175.7 mAh g⁻¹ (`Fig. 2e`) 은 n = 5 범위 ≈180.8–188.3 (`Fig. S10a`, 판독) 밖이다. `Fig. S10` 캡션의 (a)/(b) 이름도 그림과 뒤바뀌어 있다.
10. **"74 wt% 최적" 은 율 기준이다**: 200 사이클 유지율 최고는 `Table S8` 에서 70 wt% (93.4 · 93.8 %). 74 wt% · 20 mg cm⁻² 는 83.9 % 로 낮다. `Fig. 5a,b` 막대의 오른쪽 두 축 대응도 표 값과 완전히 맞지 않는다 (판독) → 수치는 `Table S8` 을 쓴다.
11. **표기 오류 소소**: 율 단계 *"0.4C"* (본문) ↔ *"0.5 C"* (`Fig. 2d`) · `Fig. 2` 캡션 (e) *"0.5C"* ↔ 패널 *"0.1 C"* · XRD *"peak width … slightly decreases, suggesting a reduction in particle size"* 는 Scherrer 방향과 반대 · `Fig. 5d` 의 "Our work 0.5 C 197" 은 0.1C 활성화 첫 방전.
12. **Randles–Sevcik D 는 복합전극의 겉보기 값**: A (기하 면적) · C 를 상수로 둔 비이고, 복합체에서는 이온 망 저항이 피크 전류에 섞인다 → *"NCM 확산계수가 65.7 % 올랐다"* 가 아니라 *"전극 수준 겉보기 수송이 올랐다"*. 어느 피크 (O1 ≈1.49× · R1 ≈1.90×, 판독) 의 값인지도 미기재.
13. **CAM 입도 · 출처 · 코팅 미기재** → λ 축 (p1 · 지도 T11) 에 못 올린다. 85 · 90 wt% 배합 미기재.
14. **이해관계**: 공저자 3 명이 소재 기업 소속 · 원료 공급사 겸 — *"no conflicts"* 선언.

## 11. 적용 인사이트
- ① **p5 의 문헌 범위가 넓어진다**: 밀링 SE 펠릿 σ 비 목록에 3.28 (LIN) 추가 → 덱 2.217 은 범위 안쪽. 손익분기선을 *"문헌이 넘는다/못 넘는다"* 로 쓰려면 **σ_eff 가 보고된 논문만** 써야 한다 — 이 논문은 τ 만 있어 조건부 (넷 중 셋).
- ② **"서브 µm" 라벨 검문**: 문헌의 미립 SE 가 부피 D50 2 µm 대인 경우가 있다 → 우리 D0.7 은 **실험 문헌보다 훨씬 고운 쪽** 일 수 있고, 그 대역의 LPSCl 복합양극 실측은 이 논문으로 채워지지 않는다.
- ③ **고 AM 분율에서 율 붕괴**: SU 로도 76 → 80 wt% 에서 1C 이상이 무너진다 (`Fig. 5c`, 판독). 85 wt% 를 다루는 우리 보고에서 *"연결성 · 협착이 율을 정한다"* 는 질문 (p4 · p7) 의 실험 쪽 근거 — 단 조성 · 입도 · 압력이 다르다.
- ④ **형태 주장 (등각 피복 · 응력 완충) 은 MPM 몫**: 비교하려면 DEM 피복 (기하 캡) 이 아니라 MPM 형상 소성 단면이 상대다 (frame [5]).
- ⑤ **기공 보고는 두께 분해능과 함께**: 우리 그림에 문헌 기공을 겹칠 때 *"두께 0.01 mm ↔ 0.8 %p"* 같은 측정 분해능을 각주로.

## 12. 인용 가능 문장 (영문 초안)
- *"Wet-milling a solid-state-synthesized Li₆PS₅Cl from D50 11.88 to 2.34 µm lowered its pellet conductivity from 4.96 to 1.51 mS cm⁻¹ and raised the activation energy from 0.296 to 0.357 eV, yet NCM811 composites (70 wt% CAM, 3 wt% VGCF) with the milled electrolyte showed lower porosity (18.68 vs 21.12 % at 450 MPa) and better first-cycle capacity and 200-cycle retention (93.4 vs 84.7 %) [Lin 2025]."*
- *"The reported ion tortuosity (1.77 vs 3.91) cannot be converted into an effective conductivity because the effective conductivity, the electrolyte volume fraction and the reference bulk conductivity were not reported [Lin 2025, p. 3459]."* (내부 메모용)
- ⚠ *"sub-micrometer"* 를 그대로 옮기지 말 것 — D50 2.34 µm 병기.

## 13. 기법 용어 미니사전
- **IN-LPSC / SU-LPSC**: 저자 표기 — *initial* (고상 합성 원 분말) / *sub-micrometer* (그것을 습식 밀링한 분말).
- **습식 볼밀 (wet milling)**: 용매 (여기선 시클로헥산) 속 볼밀 — 분쇄와 함께 표면 비정질화 · 결함을 만든다. 재소성 없으면 σ 가 떨어지는 것이 보통 (Cronau 2022 서사).
- **ion tortuosity (이 논문)**: τ² = σ_SE·ε_SE/σ_eff 의 τ. 우리 규약에서는 τ² 쪽이 **수송 tortuosity (tau2)** 이고 √ 값에는 그 이름을 안 쓴다.
- **전자차단 대칭셀**: Li‖SE 층‖복합체‖SE 층‖Li — 전자는 SE 층에서 막히고 Li⁺ 만 관통 → 복합체의 이온 저항.
- **Randles–Sevcik**: 확산 제어 CV 의 피크 전류 I_p ∝ D^{1/2} v^{1/2}. 복합전극에서는 겉보기 값.
- **dQ/dV ΔV**: 미분 용량 곡선의 산화 · 환원 피크 사이 전압 간격 — 분극의 지표.
- **DRT (distribution of relaxation times)**: 임피던스를 시정수 τ 분포 γ(τ) 로 풀어 과정 (벌크 · 계면 · CEI · 확산) 을 나누는 모형-자유 해석.
- **CEI (cathode–electrolyte interphase)**: 양극–전해질 계면에 생기는 분해 산물 층.
- **H1 → M**: NCM 의 육방정 (H1) → 단사정 (M) 상전이 — CV 의 O1/R1 피크.
- **ICE**: 첫 사이클 쿨롱 효율 (방전/충전).
- **D50 (레이저 회절)**: 누적 50 % 입경 — 보통 부피 가중. 넓은 분포에서는 개수 중앙값과 크게 다르다.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
