---
title: "Zheng, Xie, Zhang, Yang, Zhou, Zhu 2026 — All-solid-state batteries for the grid: A realistic appraisal of challenges and opportunities (Energy 345, 140229)"
source_url: local-upload/12._All-solid-state_batteries_for_the_grid_A_realistic_appraisal_of_challenges_and_opportunities.pdf
source_url_note: "본문 10쪽 (텍스트 pp. 1-8 + 참고문헌 56편 pp. 8-10). **SI 없음** — 업로드 큐에 `12._Sup_*` 파일이 없고 본문에 supplement*/Supporting/Appendix 언급이 0회다 (Perspective 형식; `Data availability: No data was used`). 그림 Fig. 1-5 + Table 1-2 가 전부이고 크로퍼 누락 0. **1차 측정 0 · 그림 5장 전부 모식도/레이더(데이터 그림 0)** — 수치는 저자 1차 추정(σ 문턱·<5 MPa·20-80 % SOC)·재인용(BNEF·Schmaltz·자기 논문)·투영(Table 1 ASSB 열)의 셋이며 digest 에서 구분했다."
source_doi: 10.1016/j.energy.2026.140229
source_license: "(c) 2026 Elsevier Ltd. All rights reserved (text/data mining·AI training 유보) — CC 아님"
pdf_sha256: 496f3b4580a81b9b91322659ccd4b240c2d87a9e7ded6bdcfe9ce9af957b5c1d
ingested: 2026-09-22
sha256: 788302da97549b74ab56b2129e760bda0de4da834de7756b83a9efa365f2d4f3
---

# 수집 목적

`assb` 섹션 **13호**. 큐 **12번** (12호 = 큐 11 Sadegh Kouhestani 2022 PHM 종설). 닻은
`questions/assb-contact-loss-vs-lampe.md` 이고 큐 문서(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md`
§6-1)에는 축이 **Q3 (라벨 출처) · Q4 (분해 유일성)** 로 등록돼 있었으나, 지시대로 "실제 접점이
어디인가" 를 읽고 판정했다 → **실제 접점은 Q6 (압력 창) 과 Q8 (LFP 평탄 OCP + 부분 SOC 운전 창)**
이다. Q3·Q4 에는 칸이 없다 (아래 판정표).

> ⚠ **형식 — Perspective (appraisal). 1차 측정 0 · 데이터 0.** 논문 자신이 `[인쇄]` "Data
> availability: **No data was used for the research described in the article.**" 이라 적는다.
> 따라서 이 digest 의 `[인쇄]` 는 10호(Vadhva 2021)·12호(Kouhestani 2022)·8호(Li 2026) 와 같은
> 뜻 — **"이 지면에 이렇게 적혀 있다"** 이지 "실측됐다" 가 아니다. 수치는 세 종류다:
> ① **저자들의 1차 주장/추정** (예: `σ ≥ 0.15 mS cm⁻¹`, `<5 MPa`, `20–80 % SOC`) ② **재인용**
> (BNEF 가격, Schmaltz 로드맵, LLTeO 0.826 mS cm⁻¹ = 자기 논문 [29]) ③ **투영/목표**
> (Table 1 의 ASSB 열 전부). 셋을 구분해 적었다.
>
> 표기: `[인쇄]` 본문 명시 · `[도표]` 그림에서만 읽은 값 (`figure-read ≈`) · `[재현]` 우리가
> 지면의 숫자로 계산한 값 · `[해석]` 우리 해석. `[해석]` 표시 없는 문장은 원문이 실제로 말한 것.

# 서지

**Zhuoyuan Zheng**^{a,c,*}, Yurong Xie^b, Haizhen Zhang^b, Baofeng Yang^c, **Jie Zhou**^{a,**},
**Yusong Zhu**^{a,***} — "All-solid-state batteries for the grid: A realistic appraisal of
challenges and opportunities", ***Energy* 345 (2026) 140229**, doi `10.1016/j.energy.2026.140229`.
접수 2025-12-07 → 개정 2026-01-05 → 승인 **2026-01-27** → 온라인 2026-01-29 (접수→승인 **51 일**).
Elsevier © 2026 (text/data mining·AI training 유보 문구 있음 — CC 아님).
- a: Nanjing Tech University (School of Energy Science and Engineering + Jiangsu Key Lab)
- b: **Huadian Electric Power Research Institute Co., Ltd.** (Hangzhou — 전력회사 연구소)
- c: **Shuangdeng Group Co., Ltd.** (Taizhou — 전지 제조사; 제1저자 겸직)
- 교신 3 인 (Zheng · Zhou · Zhu). CRediT: Zhou = 초고, Zheng = 검토·개념화, Zhang = 시각화.
- 키워드 `[인쇄]`: ASSB · Energy storage system (ESS) · Grid-scale · **LCOS** · **Mechanical
  health management**.
- **큐 문서의 "Energy 2026" 표기는 지면과 일치** (권 345, 논문번호 140229).
- 분량: **10 쪽** = 본문 pp. 1–8 (절 6 개 + 표 2 + 그림 5) + 참고문헌 **56 편** pp. 8–10.
  **SI 없음** — 업로드 큐에 `12._Sup_*` 부재 + 본문 `supplement*`·`Supporting`·`Appendix`
  **0 회** (합자 정규화 후 집계; 이 PDF 는 NFKC 정규화 뒤 `ﬁ`/`ﬂ` 잔존 0).
- 자기 인용: **[28] [29] [33] [50]** 제1저자 Zheng, **[40] [43]** 공저 — 56 편 중 **6 편**.
  ★ §3 이 "가장 유망하다" 고 고른 **복합전해질의 유일한 수치 예(LLTeO/PMMA/PVDF, 0.826 mS cm⁻¹)
  가 자기 논문 [29]** 다.

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 걸리는 축 |
|---|---|---|
| G1 | **LCOS 식 (1) 의 입력값이 다 없다** — `r = 5 %`, `T = 20 y`, DoD 80 %, 2 cycle/day, RTE 는 있으나 **`P_charge`·`d`(연 열화율)·`C_degradation(t)`·`C_O&M(t)` 의 시계열이 없다** → Table 1 의 `$0.16–0.22` / `$0.08–0.12 /kWh` 는 **재현 불가**. "sensitivity analysis confirms" 라 쓰고 **민감도 표·그림이 없다** | Q3 (수치 출처) |
| G2 | **ASSB 수명 10000–15000+ cycles 의 출처가 없다** — Table 1 각주 e 는 인용 번호 없이 "intrinsic stability … suppresses side reactions and lithium dendrite growth" 로 정당화. LCOS 의 **최대 구동 변수가 무인용 투영**이다 | Q3 |
| G3 | **`<5 MPa` 문턱의 근거** — §3 은 [35](Li Menglin 2025, Si 파괴 크기 문턱 ↑ with 압력) 뒤에, §5 는 [45](Zhang 2025, 무외압 Si ASSB) 뒤에 나오지만 **어느 쪽도 "5" 를 준다고 적지 않는다** | **Q6** |
| G4 | **접촉 손실의 양·단위·모델 형태 0** — `contact loss` 1 회(M3 시뮬 대상 열거), `interfacial contact` 6 회, 전부 정성. 유일한 대리량 제안 = **"interfacial contact pressure" 의 감쇠**(센서로 잴 것) | Q1 |
| G5 | §5 exemplar workflow `[인쇄]` "These models **inversely estimate** the current state of interfacial contact and material properties" — **모델 형태·관측 벡터·예시·유일성 언급 전부 0** | **Q4** |
| G6 | §4 `[인쇄]` "profiles can be distorted by **voltage hysteresis arising from mechanical stresses**" — **인용 0 · 크기 0 · 어느 전극인지 0** | Q8 |
| G7 | §3 `j ≈ 5 mA cm⁻²` 가 "0.5P" 에 대응한다는 말 — **면적 용량 미기재**. `[재현]` 0.5P = 2 h 방전이면 **≈10 mAh cm⁻²** 가 함의된다 (상용 LFP 3–4 mAh cm⁻² 의 2.5–3 배) — 로딩 가정이 어디에도 없다 | 서술 정합 |
| G8 | Fig. 2 레이더 5 축의 **점수 산정 규칙·출처 0** (본문은 각 클래스를 한 문장씩 정성 서술) | [도표] |
| G9 | "EIS could be used as a proxy for contact integrity" — **주파수·특징량·인용 0** (`EIS` 1 회, `DRT` 0 회) | Q2 |
| G10 | **Si 음극을 권하면서 Si OCP 의 이력·비평탄을 한 번도 안 다룬다** — 같은 §4 가 "좁은 전압 창에서 SOC 를 추적해야 한다" 고 요구하는데, 권장 음극의 OCP 형상은 논의 0 | Q8 (음극 축) |
| G11 | Table 2 "Dominant Degradation Modes" 열의 **인용 0** — 세 용도별 지배 열화 기구가 전부 무근거 서술 | Q3 |
| G12 | 20-year × 2 cycle/day = `[재현]` **14,600 cycles**. ASSB 목표 10000–15000 의 **상단만** 이것을 넘는다 — 논문은 이 산술을 적지 않는다 (Table 1 각주 d 는 LFP 쪽 "mid-project replacements" 만 말한다) | 서술 정합 |

# 그림 — 크로핑 7 장 (Fig. 1–5 + Table 1–2), 실제로 본 것: **Fig. 1·2·3·4·5 전부** (표 2 장은 텍스트가 정확해 텍스트로 전사)

`wiki/raw/figures/zheng2026_assb-grid-realistic-appraisal/` · 누락 0. **5 장 전부 모식도/레이더**
이고 **데이터 그림 0 장** (축·오차막대·측정점이 있는 그림이 없다).

| 그림 | 무엇 | 실제로 본 것 `[도표]` | 본문과의 관계 |
|---|---|---|---|
| **Fig. 1** | "Requirement Triangle" — 왼쪽 삼각(그리드), 오른쪽 원(EV) | 왼쪽 삼각: **Cost**("Rely on expensive elements and energy-intensive manufacturing processes") · **Performance**("Electrochemical and mechanical properties and failures") · **Stability**("Electrode-electrolyte interface stability under long-term, realistic, slow grid-duty cycles"); 가운데 컨테이너 ESS + 풍력·태양광 사진. 오른쪽 원: **Power & Rate Capability "3C–5C discharge and charge rates"** · **Energy Density ">400 Wh/kg and >1000 Wh/L"** · **Lifetime & Durability ">1500 cycles and >99.98 % CE per cycle"** | ⚠ **그리드 쪽 삼각에는 숫자가 하나도 없다** — 본문의 그리드 문턱(>250 Wh/L · >180 Wh/kg · 0.5P · >10000 cycles)이 그림에 없다. ⚠⚠ EV 원의 "**>99.98 % CE**" 는 `[재현]` 1500 사이클에 0.9998^1500 ≈ **74 %**, 그리드 10000 사이클이면 ≈ **13.5 %** — 즉 그리드용 CE 문턱은 **>99.998 %** 급이어야 하는데 논문은 CE 문턱을 그리드 쪽에 주지 않는다 (D3) |
| **Fig. 2** | 전해질 5 클래스 레이더 (Oxides / Sulfides / Halides / Polymers / Composites) 5 축: Electrochemical Performances · Scalability Cost · Manufacturability · Operating Cost · Temp. Suitability | **전도도 라벨**: Oxides "0.1–1 mS/cm" · Sulfides "**>10**" · Halides "1–10" · Polymers "0.01–0.1" · Composites "~1". **★ 압력 라벨 (Operating Cost 축)**: Oxides "**High, stack pressure ≥ 30 MPa**" · Sulfides "**Moderate, stack pressure of 5–20 MPa**" · Halides "**Possibly low, 2–10 MPa**" · Polymers "**No or compliant pressure**" · Composites "**Low, tunable pressure of 1–10 MPa**". Temp: Oxides Good · Sulfides "Limited, at low T" · Halides Good · Polymers "Poor at low T" · Composites "Moderate, Tunable". 형상: Oxides = Temp·Manufacturability 만 큰 찌그러진 삼각, Sulfides = 전도도 축만 뾰족, **Halides·Composites = 거의 정오각형**, Polymers = 하단 두 축만 큼. 예시 물질: Li₇La₃Zr₂O₁₂ · Li₃PS₄ · Li₃YCl₆ · PEO/PVDF · **PVDF/PMMA-Li₁.₅La₁.₅TeO₆**(자기 논문 [29]) | ★★ **압력 창 5 개가 본문에 없다 — 그림에만 있다** (본문 `MPa` 는 `<5` 두 번뿐). ⚠ 본문이 권하는 두 클래스(Halides 2–10 · Composites 1–10)의 **상단이 본문의 `<5 MPa` 문턱의 2 배** 다 (D4). 캡션 `[인쇄]` "projected cycle life … comparable … not included as a differentiating axis" (D8) |
| **Fig. 3** | BMS 패러다임 전환 모식도 (위 LIB / 아래 SSB) | **위(LIB)**: 입력 **Pack/Cell Voltage · Current · Temperature** → BMS → "State Estimation SOC / SOH / RUL"; 출력 "Power Optimization / Balancing" + "Thermal Management". **아래(SSB)**: 입력 **Voltage · Current · Pressure(빨강) · Impedance(빨강)** → BMS → "State Estimation **Interfacial Integrity** / SOC / SOH / RUL"; 출력 "Power Optimization / Balancing" + **"Active Stress Management"(빨강 점선 상자)**. 온도 입력·Thermal Management 화살이 **아래 그림에는 없다** | ⚠ §4 마지막 문단은 `[인쇄]` "thermal management **remains a critical function** of the BMS … 30–50 °C" 라 적는데 **그림의 SSB BMS 에는 온도 입력이 없다** (D5). "Interfacial Integrity" 가 SOC 앞에 놓인 것이 이 논문의 주장 그대로 |
| **Fig. 4** | 지식 공백 피라미드 (4 단 + 왕관) | 아래→위: "Innovation of **SSE** Candidates"(Earth-abundant, stable materials) → "Advanced Holistic **Design** of ASSBs"(**Low-pressure architectures / microstructure to eliminate complex external systems**) → "Creation of **ALT** Protocols"(ALT protocols to replicate grid-specific duty cycles) → "**LCA** and **3Rs**"(end-of-life + LCA at design stage) → 왕관 "Sustainable ASSBs for the Grid" | §5 의 "four key directions" 와 1:1. 정보량 0 (본문 재서술) |
| **Fig. 5** | M³-ML 프레임워크 (5 스케일 + ML 도구) | Atomistic(Crystal Structures · Element Doping · Thermodynamic Stability · Ion Migration Barrier) → Micro(Ion Transfer Path · Ionic Conductivity · Parasitic Reactions) → Meso(**Dendrite Growth · Stress Concentration · Cracking/Fracture**) → Cell(**(Dis)charging Behavior · Temperature Change · Mechanical Response** — 셀 모식도가 "Solid particle / Electrolyte / Solid particle" + **"SEI growth" 화살**) → System(Power I/O · Cell Balancing · Thermal Management · Failure Diagnosis — Cold Plate 그림). 아래 ML: Supervised · Unsupervised · Reinforcement · **Physics-Informed**. 스케일별 ML 역할: High Throughput Screening / ML Force Field / Structure-Property Mapping / **Aging Mechanism Analysis + Reverse-Design** / SOC/SOH Estimation + Fault Prognosis | Cell-scale 모식도가 **액체셀 P2D 그림(SEI growth)** 이다 — ASSB 의 접촉 손실·균열이 Cell 칸에 없고 Meso 칸에만 있다. `[해석]` 이 그림에서 "접촉 손실 → 용량" 사상은 어느 칸에도 없다 |

**본문과 어긋난 그림**: Fig. 1 (D3, 그리드 숫자 부재 + CE 문턱 EV 급), Fig. 2 (D4 압력 상단 ↔
`<5 MPa`), Fig. 3 (D5 온도 입력 소실). Fig. 4·5 는 본문 재서술이라 어긋남 없음.

# 절별 해체

## §1 Introduction — 그리드가 EV 와 다른 요구

- `[인쇄]` IEA: net-zero 에 "**tens of terawatt-hours**" 저장 필요 [4]. 그리드 시장 규모가 EV 와
  "similar, if not larger" [3].
- `[인쇄]` 현행 = **LFP LIB**. 한계: 전해액 가연성 → MWh 급 열관리·소화 비용; **>10000 cycles**
  와 캘린더 수명이 "continuous electrolyte decomposition and interfacial degradation" 때문에
  어렵다 [6–8].
- **논지 문장** `[인쇄]`: "the prevailing development roadmap for lithium-based ASSBs is
  disproportionately influenced by the performance-driven requirements of EVs, particularly the
  pursuit of extreme energy density [13]. For stationary storage, the supreme metric is … the
  economic **LCOS**". 요구 3 가지: (i) 재료 우선순위 재평가 (ii) "**mechanical stability over
  energy density**" 중심의 시스템 재설계 (iii) 저비용 대량 제조.

## §2 ESS 대차대조표 — LCOS 모델과 Table 1·2

- 운전 환경 `[인쇄]`: "thousands of shallow discharge cycles (**1–2 per day**) over a **20-year**
  lifespan", "**−30 °C–50 °C**", 습기, "thousands of interconnected cells".
- ASSB 이점 3 가지 `[인쇄]`: 본질 안전(소화 설비·보험·조밀 배치) · 운전 온도 폭 · **수명**
  ("drastically reducing continuous electrolyte decomposition and transition metal
  dissolution … dramatically slower capacity fade and impedance growth, which is the **single
  most important factor**").
- **LCOS 식 (1)** `[인쇄]`:
  `LCOS = [C_capex + Σ_{t=1}^{T} (C_O&M(t) + C_degradation(t) + P_charge·E_discharged(t)/η)/(1+r)^t] / [Σ_{t=1}^{T} E_discharged(t)·(1−d)^t/(1+r)^t]` — 변수: capex, `T`, O&M, 열화·교체 비용, 전력 구입가, 연 방전량, RTE `η`, **열화율 `d`**, 할인율 `r`. 출처 [18] Schmidt 2019 *Joule*.
  ⚠ G1 — `d`·`P_charge`·`C_degradation(t)` 값 없음.
- **Table 1** (LFP LIB 2025 ↔ ASSB 2030 투영; 조건 `[인쇄]` 2 cycle/day · 80 % DoD · **0.5P** ·
  20 y · r = 5 %):

  | 항목 | LFP LIB (2025) | ASSB (2030 목표) | 출처 층위 |
  |---|---|---|---|
  | Capital ($/kWh) | **$75–90** (BNEF 2025 팩 ≈$70 + BOS) | **~$350 (2026)** → **~$140–160 (2030)** (각주 c 는 "~$155") | 재인용 [19]·[13] |
  | Cycle life (80 % DoD) | **4000–6000** | **10000–15000+ (projected)** | LFP: 서술 · ASSB: **무인용** (G2) |
  | Calendar life (y) | 15–20 | 25–30+ | 무인용 |
  | RTE | 92–94 % | 94–97 % | 무인용 |
  | O&M & Safety ($/kWh/yr) | Medium ($8–12) | Very Low ($2–4) | 무인용 |
  | Safety/Permitting premium | 10–20 % of capex | Negligible | 무인용 |
  | **Projected LCOS** | **$0.16–0.22/kWh** | **$0.08–0.12/kWh** | 식 (1), 입력 미공개 |

  `[인쇄]` "ASSB enables **~45–55 %** LCOS reduction". `[재현]` 끝점 짝으로는 (0.16→0.08) **50 %**,
  (0.22→0.12) **45.5 %** — "55" 는 표의 네 숫자에서 나오지 않는다 (D2). `[재현]` 수명비 = 10000–
  15000 / 4000–6000 = **1.67–3.75 ×** (표는 "2–3 times").
- **Table 2** (용도 3 종): Energy Arbitrage/PV shifting (1–2 deep cycles/day, ~80 % DoD, 0.2–0.5C,
  long dwell at full/empty) · Frequency Regulation (very high cycle count, 10–20 % DoD, partial SOC)
  · Capacity Firming/Backup (irregular deep discharge, long high-SOC dwell). "Dominant Degradation
  Modes" 열: `[인쇄]` "Cycle-life degradation (capacity fade), calendar aging at high/low voltage" /
  "Electrolyte/interface fatigue from micro-cycling, **possible Li plating** at high rates" /
  "Calendar aging (electrolyte decomposition), possible mechanical stress from infrequent large
  expansion". ⚠ D7 — **§4 가 ASSB 의 지배 실패 모드로 꼽는 접촉 손실·균열이 이 열에 없다**;
  어휘가 액체셀 것(Li plating, electrolyte decomposition).
- **도전 3 가지** `[인쇄]` (Fig. 1): ① 재료·제조 비용/규모 (Ge·La·Zr, ALD·스퍼터링은 "GWh yr⁻¹"
  과 비호환) ② **계면 장기 안정성 = "critical unknown"** — "chemo-mechanical evolution … under
  realistic, slow grid-duty cycles over **5–10 years** is poorly understood … major risk for
  **sudden failure**" ③ ★ **스택 압력** — "perhaps most critically for system integration …
  mechanical requirement for stack pressure … [23]. The necessity to maintain constant external
  load introduces immense complexity … new points of mechanical failure, such as **creep, fatigue,
  and fracture**". [23] = Li Qianya et al., *Nat. Energy* **2025**, 10, 1064 "The critical
  importance of stack pressure in batteries" (재인용 대상 — 후속 후보).
- 그리드 최소 성능 `[인쇄]`: "**>250 Wh/L and >180 Wh/kg** coupled with a peak current density of
  **0.5P** (comparable to contemporary LFP LIB systems)".

## §3 재료 요구의 재정의

- **"Good enough" 전도도** `[인쇄]`: "on the order of **0.1–1 mS cm⁻¹** … for a representative
  grid duty cycle (0.5P, equivalent to a current density j of **~5 mA cm⁻²**), the minimum required
  conductivity σ can be estimated as **σ ≥ L·j/ΔV = 0.15 mS cm⁻¹**, with an electrolyte thickness L
  of **30 μm** and acceptable IR drop ΔV of less than **100 mV** (RTE penalty <2 %)".
  `[재현]` 3×10⁻³ cm × 5×10⁻³ A cm⁻² / 0.1 V = 1.5×10⁻⁴ S cm⁻¹ = **0.15 mS cm⁻¹** ✓.
  ⚠ G7 — `j = 5 mA cm⁻²` 는 로딩 ≈10 mAh cm⁻² 를 함의.
- 저온 `[인쇄]`: "At **−10 °C**, conductivity can drop by an order of magnitude, necessitating
  impractically thin electrolytes (**<5 μm**)". `[재현]` ×10 감소 + 같은 ΔV 면 L ≤ 3 µm — "<5" 와
  자릿수 정합.
- 클래스별 `[인쇄]`: **Oxides** 고온 소결·취성·"often require significant stack pressure" ·
  **Sulfides** 공기 불안정(드라이룸)·"moderate stack pressure requirements" · **Halides** 중간,
  희토류/전이금속 공급망 위험 · **Polymers** "require **no stack pressure**", 실온 전도도
  ~10⁻⁵–10⁻⁴ S cm⁻¹, 영하 성능 열화 · **Composites** = "highest promise" — 예 **50 wt%
  Li₁.₅La₁.₅TeO₆ in PMMA/PVDF → 0.826 mS cm⁻¹**, 드라이룸 불필요 [29 = 자기 논문].
- **양극** `[인쇄]`: Ni-rich NCM 을 밀지 말고 "**LFP or LFMP** with lower operating voltages to
  minimize interfacial degradation [31]"; 목표는 "simple, scalable coating and processing
  techniques to **maximize interfacial contact** and prevent interdiffusion over decades".
- **음극** `[인쇄]`: "is lithium metal necessary or even desirable for ESS?" — "infinite relative
  volume change, stringent pressure requirements, and the perpetual risk of dendrite propagation".
  대안 = **Si 계** (SiOx-C, pure Si) — "finite, predictable alloying reaction", 부피팽창 **~280 %**
  는 pre-lithiation·바인더·기공률로 관리. ★ `[인쇄]` "this finite expansion drastically reduces the
  required stack pressure (**<5 MPa**), enabling simple, passive cell casing and facilitating the
  low-pressure module architectures [35]".
- 환경 `[인쇄]`: −30–50 °C, 습도, **air-stable processing = "major economic lever"** [36].
  §3 끝: "a robust system that **degrades predictably and gracefully**".

## §4 시스템 통합 — BMS 의 진화 (이 논문에서 우리 축에 가장 가까운 절)

- **역할 전환** `[인쇄]`: LIB BMS = "safety guardian" (열폭주 조기 검출) → ASSB BMS = "**sentinel
  of long-term mechanical and interfacial health**". 관리 대상 = "the dominant failure modes of
  ASSBs [38]: **the gradual loss of interfacial contact, the propagation of cracks within brittle
  solid electrolytes, and the chemo-mechanical evolution of electrode-electrolyte interfaces** over
  a targeted 20-year lifespan". ([38] = Gu 2023 *AEM* 종설 — 종설 인용 종설, D11.)
- ★★ **SOC 추정의 세 장애** `[인쇄]`: ① "grid batteries rarely perform full cycles … operate within
  a limited window (e.g., **20–80 % SOC**)" → "prevents regular full-range calibration, causing
  traditional coulomb counting to drift and making it **impossible to obtain a full open-circuit
  voltage (OCV) curve** for calibration" ② "the **flat voltage profiles** of common ASSB pairings
  (e.g., **LFP cathodes**) exhibit minimal voltage change over large SOC ranges" ③ "these profiles
  can be **distorted by voltage hysteresis arising from mechanical stresses**" (G6). 처방 = "adaptive
  model-based estimators that can accurately track SOC within a narrow voltage window".
- ★★★ **SOH 의 이분법** `[인쇄]`: "SOH estimation can no longer rely on periodic full-capacity
  checks [40]. The BMS must instead **distinguish between true active material loss and a reduction
  in 'useable capacity' caused by rising impedance or increasing overpotentials** that effectively
  shrink the operational voltage window at practical power rates. This requires … new,
  **multi-parameter SOH models** that fuse historical operational data with real-time diagnostics to
  provide a nuanced assessment of **degradation root causes**". ([40] = Kohtz·Xu·**Zheng**·Wang 2022,
  자기 공저 PIML SOH.)
  `[해석]` 이것은 닻 페이지의 3 항 분해(`Q_apparent = θ_AM·Q_material·η(i)`) 중 **`Q_material`
  ↔ `η(i)` 두 항만** 가른 것이다. 같은 절 첫 문단이 **접촉 손실을 지배 실패 모드 1 번**으로
  꼽아 놓고, 이 이분법에서 **접촉 손실이 어느 쪽인지 말하지 않는다** — "true active material
  loss" 인가 "rising impedance" 인가. **`θ_AM` 항이 문장에서 사라졌다.** (아래 판정 Q1·Q3.)
- **직접 기계 건강 감시** (Fig. 3) `[인쇄]`: "piezoelectric or thin-film pressure sensors within the
  cell stack to monitor the distribution and **decay of interfacial contact pressure** over time".
  비용 논리: 센서 = 1 회성 capex 증분 ↔ 수명·교체·가동중단 절감. 실무 난점 `[인쇄]`: 센서 수명·
  교정 안정성(수십 년), 모듈/팩 배선·데이터, 하드웨어 비용 정당화.
- **간접 방법** `[인쇄]`: "**EIS** could be used as a **proxy for contact integrity**, while in-situ
  **acoustic or ultrasonic** sensing could detect the formation of **voids or cracks** … [41]" →
  "hybrid diagnostic strategy" (드문 직접 센서 + 주기적 간접). (G9 — EIS 의 어느 특징인지 0.)
  ([41] = Lu 2024 *ESM* 저온 시험-분석 흐름 — 음향 논문이 아니다.)
- ★★ **능동 응력 관리** `[인쇄]`: "For cells that require stack pressure … **active stress
  management**. Here, the BMS would not merely monitor but act, controlling an external mechanism to
  modulate the applied pressure. An intelligent strategy could apply **higher pressure during
  high-rate cycling** to maintain electrical contact and then deliberately **reduce pressure during
  extended rest periods or as the cell ages** to minimize the creep of soft components and the
  mechanical fatigue of brittle electrolytes".
  `[해석]` 압력이 **상태변수 + 제어변수** — 8호(Li 2026) `[인쇄]` "coupled state/control variable"
  와 같은 명제이고, 13호는 거기에 **정책(율↑→P↑, 휴지/노화→P↓)** 까지 적었다. 인용 0.
- **열관리** `[인쇄]`: 목적이 "longevity rather than preventing catastrophe"; 창 "**30–50 °C** for
  many sulfide or polymer-based electrolytes [42]"; "operating continuously at a **mid-range SOC**
  may induce **different long-term degradation mechanisms** at the solid interfaces compared to deep
  cycling"; "passive or minimally active thermal management".

## §5 공백과 연구 방향

- 1 차 장애 `[인쇄]`: "lack of understanding of the dynamic interplay at solid-solid interfaces under
  the combined stresses of **decades of shallow, partial-state cycling**, wide temperature
  fluctuations, and continuous mechanical strain" + "**dearth of data on the 'mechanical fatigue'**
  of solid electrolytes; how do properties like **fracture toughness and creep resistance** degrade
  after thousands of expansion/contraction cycles? … a fundamental requirement for **predicting
  long-term contact loss** … Without it, we are designing in the dark."
- **네 방향** (Fig. 4) `[인쇄]`: ① earth-abundant 재료 ② "**pressure-less**" or low-pressure
  architectures — "compliant interlayers and engineered microstructures [45]. A low-pressure
  threshold of **<5 MPa** enables simplified, passive mechanical constraints, such as standard cell
  casing or lightweight module frames." ★★ 상한 논리: "**high, constant stack pressure can induce
  detrimental long-term effects: creep and stress relaxation in softer components (e.g., polymer
  binders) and fatigue-driven micro-crack initiation in brittle ceramics, gradually degrading
  interfacial contact, increase impedance, and accelerate overall cell degradation**" ③ **ALT**
  (20 년 그리드 duty cycle 재현 — "move beyond traditional metrics to capture the unique mechanical
  and interfacial degradation mechanisms") ④ 순환성 (EoL, LCA, 3Rs; 황화물은 불활성 분위기 회수,
  폴리머는 용매 분리, "debondable interfaces").
  `[해석]` ②의 상한은 5호(Doux 2020)의 상한(**단락**, 시간 ~h)과 **다른 축** — **피로/크리프**
  (시간 ~년). 압력 창의 위 벽이 **둘**이 된다.
- 구조 전지(load-bearing) [47] · 적층 제조 [48,49].
- **M³-ML** (Fig. 5) `[인쇄]`: multi-scale (DFT → phase-field 덴드라이트/균열 → continuum) ·
  multi-physics (전기화학·응력·열) · **multi-mode** ("simultaneously simulate various degradation
  modes — such as **interface decomposition, contact loss, and crack propagation** — to unravel
  their synergies and identify the dominant failure mechanisms"). ML: supervised/unsupervised/RL,
  **physics-informed** ("overcoming data scarcity without compromising predictive accuracy").
- **디지털 트윈** [54–56] `[인쇄]`: "material passport", RUL for second-use.
- ★★ **exemplar workflow** `[인쇄]` (p.7–8): "forecasting the **decay of interfacial contact
  pressure — a primary driver of impedance growth**. Here, short-term operational data and direct
  sensor readings calibrate high-fidelity, cell-level models of chemo-mechanical stress evolution.
  These models **inversely estimate the current state of interfacial contact and material
  properties**. Augmented by ML surrogates trained on vast libraries of simulated scenarios, they
  rapidly predict long-term pressure decay and remaining useful life." (G5 — 모델·관측·유일성 0.)
  `[해석]` 인과 방향이 명시됐다: **압력 감쇠 → 임피던스 성장**. 그리고 역추정 대상이 "접촉 상태
  **와** 재료 물성" 둘 — 9호(Huo 2025)의 `A_eff·ε_p/R_s` 곱 축퇴가 정확히 이 두 부류 사이에 있다.
  이 논문은 그 축퇴를 모른다 (`identifiab*` 0).

## §6 결론 — "manifesto"

`[인쇄]` 세 원칙: **i) Lifetime over energy density** (>10000 cycles, 0.1–1 mS cm⁻¹ 로 충분)
**ii) System cost over peak performance** (공기 안정 복합전해질 + **pressure-less** 아키텍처, Si
계 음극) **iii) Predictive over reactive management** (직접 기계 건강 감시, 수십 년 SOH). 판정
질문 `[인쇄]`: "Does this primarily enhance energy density for EV-like performance, or does it
directly improve lifetime, safety, and scalability to lower the LCOS for grid storage?"
`[인쇄]` "pursuing lithium metal anodes for grid storage **may be misguided**".

# 어휘 집계 (합자 NFKC 정규화 후, 본문 pp. 1–8, 참고문헌 제외; 약어는 대소문자 구분)

| 어휘 | 회 | 비고 |
|---|---|---|
| `identifiab*` / `identification` | **0 / 0** | `identify` 1 (M3 "identify the dominant failure mechanisms") |
| `uniqu*` | 3 | 전부 무관 ("unique cycling patterns" 등) |
| `ill-posed` · `regulariz*` · `uncertaint*` · `confidence` · `error bar` · `fitted` | **0** | |
| `inverse*` | 2 | "inverse design" 1 · "**inversely estimate** … interfacial contact" 1 |
| `LAM` · `LLI` · `SEI` · `GITT` · `dV/dQ` · `incremental` · `half-cell` · `DRT` | **0** | `active material loss` 1 (§4 이분법 문장) |
| `SOH` / `SOC` | 4 / 9 | |
| `OCV` | **1** (+`open-circuit` 같은 문장) | "impossible to obtain a full OCV curve" |
| `hysteresis` | 1 | "voltage hysteresis arising from mechanical stresses" |
| `EIS` / `impedance` / `acoustic` / `ultrason*` / `sensor*` | 1 / 6 / 1 / 1 / 5 | |
| `contact` / `interfacial contact` / `contact loss` / `contact pressure` | 10 / 6 / **1** / 1 | |
| `pressure` / `stack pressure` / `pressure-less` / `MPa` | **24 / 7 / 5 / 2** | `MPa` 본문 2 회 = 둘 다 "<5" (Fig. 2 라벨 5 개는 그림에만) |
| `creep` / `fatigue` / `crack*` / `void*` | 4 / 5 / 5 / 3 | |
| `dendrite` / `plating` / `dead li*` / `isolated` / `indium` / `In-Li` | 3 / 2 / **0 / 0 / 0 / 0** | |
| `LFP` / `silicon` / `lithium metal` | 7 / 5 / 1 | |
| `LCOS` / `BMS` / `digital twin` / `ML` / `physics-informed` | 26 / 13 / 4 / 5 / 1 | |
| `supplement*` · `Supporting` · `Appendix` | **0** | SI 없음 확정 |

# Q1~Q8 판정 (닻 페이지 수집 지침)

| Q | 판정 | 근거 |
|---|---|---|
| **Q1 접촉 손실 정량** | **없다 (정량 0).** | `contact loss` 1 회(시뮬 대상 열거) · `θ`·`percolat*`·`tortuos*` 0 · 단위·모델 형태 0. 유일한 제안 대리량 = **"interfacial contact pressure" 의 시간 감쇠**(압력 센서로 관측) + 인과 명제 `[인쇄]` "decay of interfacial contact pressure — a primary driver of impedance growth". ★ `[해석]` 이 계보에서 **접촉 손실의 대리량으로 압력 시계열을 지목한 첫 편** (9호는 힘 시계열을 **재고도** 모델에 안 넣었다) |
| **Q2 독립 관측** | **없다 — perspective.** 처방만 셋 | ① 압전/박막 **압력 센서** ② **EIS** "proxy for contact integrity" ③ **음향/초음파** (void·crack). 전부 인용 0 또는 무관 인용([41]). `LAM_PE` ↔ 접촉 손실을 가르는 관측으로 제시된 것은 **없다** |
| **Q3 라벨 층위** | **해당 없음 + 정의 하나.** `[인쇄]` "No data was used" | Table 1 은 투영(재인용 2 + 무인용 5), LCOS 입력 미공개(G1). ★ **라벨의 정의**는 인쇄됐다: SOH 가 갈라야 할 것 = "**true active material loss**" ↔ "**reduction in usable capacity caused by rising impedance or increasing overpotentials**" — **2 항 이분법**, 접촉 손실의 소속 미지정. 12호가 `LAM ⊃ 접촉 손실` 로 정의했다면, 13호는 **`LAM` ↔ `kinetic` 둘만 두고 접촉 손실을 지배 실패 모드로 따로 부른다** — 두 종설의 분류가 **서로 다르고 둘 다 우리 3 항과 다르다** |
| **Q4 유일성** | **0 (13/13 편).** | `identifiab*`·`uniqu*(유관)`·`ill-posed`·`regulariz*`·`uncertaint*`·`confidence` 전수 0. ★ 성질: **역추정을 워크플로로 처방한다** — `[인쇄]` "inversely estimate the current state of interfacial contact **and** material properties" — **유일성 경고 0**. 8호(2026)가 `identifiab*` 5 회로 이름을 붙였다면 **같은 해의 13호는 이름 없이 역문제를 처방**한다 ⇒ "2026 년 PHM 문헌이 식별 가능성을 안다" 는 일반화가 성립하지 않는다 (8호 하나의 일이다) |
| **Q5 Li-In** | **해당 없음.** `indium`·`In-Li` 0 | Li 금속 음극 자체를 "may be misguided" 로 배제 |
| **Q6 압력** | **★★ 있다 — 이 편의 본체(값은 적다).** `pressure` 24 · `MPa` 본문 2 | ① 1 차 주장 `[인쇄]` **`<5 MPa`** ×2 (Si 음극 / 저압 아키텍처 문턱; 근거 [35]·[45], G3) ② `[도표]` Fig. 2 클래스별 창: Oxides **≥30** · Sulfides **5–20** · Halides **2–10** · Polymers **0/compliant** · Composites **1–10 MPa** — **본문에 없는 다섯 값** ③ ★★ **상한의 두 번째 형태**: `[인쇄]` 고정 고압 → "creep and stress relaxation … fatigue-driven micro-crack initiation … gradually degrading interfacial contact" (5호의 단락 상한과 **시간 스케일이 다른** 위 벽) ④ ★★ **압력 = 제어변수 + 정책** (율↑→P↑, 휴지/노화→P↓) ⑤ 압력 센서 = 상태 관측 ⑥ 인과 `압력 감쇠 → 임피던스 성장`. ⚠ **압력 → 용량 곡선 0 · 스윕 0 · 이력 0** (perspective). ★ 요구치 계보: 8호 `<≈1`(Xu 2024, 산업) · 12호 `0.4–1`(Tian/Shao 모델 최적) · **13호 `<5`(Si 음극 근거)** — **세 원전이 다르고 자릿수는 같다**; 실험실 창 2–490 MPa 은 셋 다의 위 |
| **Q7 dead Li** | **해당 없음.** `dead li`·`isolated` 0 | Si 음극 권장. `plating` 2 회는 그리드 주파수조정 "resistance to lithium plating" · Table 2 |
| **Q8 화학·OCP** | **★ 부분 — 처방과 경고, 곡선 0.** | ① 양극 권장 = **LFP / LFMP** ② `[인쇄]` "**flat voltage profiles** … (e.g., LFP cathodes) exhibit minimal voltage change over large SOC ranges" ③ ★ **운전 창 절단**: `[인쇄]` "20–80 % SOC … **impossible to obtain a full OCV curve**" ④ `[인쇄]` "distorted by **voltage hysteresis arising from mechanical stresses**" (G6) ⑤ 음극 권장 = **Si 계** (비평탄·이력 OCP — 논문은 논의 0, G10). **V–Q·OCP·GITT 0 장**. `[해석]` 닻의 "모르는 것 5"(LFP 평탄 → `(X1, X3)` 축퇴)가 그리드 용도에서 **설계 권장(LFP) + 운전 창 절단(20–80 %) + 응력 이력** 세 겹으로 강화되고, 동시에 "전고체 음극 = 평탄" 전제는 **세 번째로**(9호 Li-Si · 11호 graphite 에 이어, 이번엔 **설계 처방으로서**) 깨진다 |

**채움표 판정 한 줄**: **새 칸 0 (누적 ≈8.5 / 8 유지, Q4 0/13).** Q6 와 Q8 의 **이미 채워진 칸에
층이 하나씩** 얹힌다 — Q6: 요구치 세 번째 독립 인쇄 + 피로형 상한 + 제어 정책; Q8: 그리드
운전 창(20–80 %)이 OCV 채널을 **설계상** 닫는다.

# 12호·10호·8호와의 대조

| 축 | 13호 Zheng 2026 (*Energy*) | 12호 Kouhestani 2022 (*Energies*) | 8호 Li 2026 (*Front. Chem.*) |
|---|---|---|---|
| 형식 | Perspective, 10 쪽, 56 refs, 1 차 측정 0, 그림 5 장 전부 모식도 | Review, 26 쪽, 131 refs, 그림 7 장 전부 재수록 | Mini Review, 12 쪽 |
| 접수→승인 | **51 일** | 9 일 | — |
| `identifiab*` | **0** | 0 | **5** |
| 열화 라벨 정의 | **2 항**: "true AM loss" ↔ "usable capacity ↓ by impedance/overpotential"; 접촉 손실 = 별도 "failure mode", 소속 미지정 | **`LAM ⊃ contact loss`** (§2.2) | SOH 스칼라, 모드 라벨 0 |
| 압력 요구치 | **`<5 MPa`** (1 차 주장, Si 근거) + Fig. 2 클래스 창 | `0.4–1 MPa` (재인용, 출처 미확정) | `<≈1 MPa` (재인용 Xu 2024) |
| 압력의 역할 | 상태 + **제어변수 + 정책** + 센서 관측 + 인과(감쇠→임피던스) | 재인용 1 문장 | "coupled state/control variable" |
| 상한 형태 | **피로/크리프** (년) | — | "pressure/contact failure" (목록) |
| 역문제 | "inversely estimate contact state and material properties" **처방**, 경고 0 | "difficult parameter identification" | "lose physical uniqueness" · "ill-posed inversion needs regularization" |
| 데이터 | "No data was used" | "Not applicable" | "no direct capacity labels" |

**공통 원전**: 12호 ↔ 13호 **0 건** (12호의 Tian·Shao·Hu·Fathiannasab·Cho 가 13호에 없고, 13호의
Schmaltz·Albertus·Huang/Ceder/Olivetti·Li Qianya·Gu·Pang 2021 이 12호에 없다). 10호 ↔ 13호:
**같은 그룹(Imperial, Offer/Marinescu) 의 다른 논문** (10호 Pang 2019 *PCCP* ↔ 13호 Pang 2021
*Mater. Today* [51]) — 공통 원전 아님. 8호 ↔ 13호: 압력 요구치 원전이 다르다 (Xu 2024 ↔ [23]
Li Qianya *Nat. Energy* 2025 / [35] / [45]). ⇒ 8호에서 했던 "같은 원전을 두 리뷰가 다르게
적었는가" 는 이 쌍에서도 **수행 불가**; 대신 **압력 요구치 자릿수(≈1–5 MPa)가 세 종설에서 세
원전으로 독립 수렴**한다는 것이 이번 실측이다.

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 약화되는 주장 |
|---|---|---|
| **D1** | Table 1 "~$140–160 (2030 target)" ↔ 각주 c "~$155/kWh by 2030" — 범위 안이라 편집급 | — |
| **D2** | "~45–55 % LCOS reduction" ↔ 표의 끝점 짝 `[재현]` **45.5 / 50 %** — 55 는 표에서 안 나온다 | LCOS 주장 (G1 과 합쳐 재현 불가) |
| **D3** | Fig. 1 그리드 삼각에 **숫자 0**, EV 원에는 ">1500 cycles · >99.98 % CE" — `[재현]` 그 CE 로 10000 사이클이면 잔존 ≈13.5 % | "lifetime over energy density" 를 그림이 수치로 못 받친다 |
| **D4** | 본문 `<5 MPa` 문턱 ↔ Fig. 2 권장 클래스 상단 **Halides 10 · Composites 10 · Sulfides 20 MPa** | "pressure-less" 경로의 실현 가능성 |
| **D5** | Fig. 3 SSB BMS 입력에 **온도 없음** ↔ §4 "thermal management remains a critical function … 30–50 °C" | — (그림 단순화) |
| **D6** | §3 `j ~5 mA cm⁻²` ⇔ 0.5P → `[재현]` 로딩 ≈10 mAh cm⁻² 함의, 미기재 | σ 문턱 0.15 mS cm⁻¹ 의 전제 |
| **D7** | Table 2 "Dominant Degradation Modes" = 액체셀 어휘(Li plating, electrolyte decomposition) ↔ §4 "dominant failure modes of ASSBs" = 접촉 손실·균열·계면 진화 | 용도별 열화 서술 |
| **D8** | Fig. 2 캡션 "cycle life … comparable … not included" ↔ 논지 전체가 "lifetime 이 LCOS 최대 구동" | 전해질 클래스 비교의 완결성 |
| **D9** | §4 간접 진단 인용 [41] = Lu 2024 저온 시험-분석 흐름 — 음향/초음파 논문이 아니다 | 인용 위생 |
| **D10** | §4 "dominant failure modes [38]" = Gu 2023 종설(응력 측정 리뷰) — 종설 인용 종설 | 인용 위생 |
| **D11** | Table 1 수명비 "2–3 times" ↔ `[재현]` 1.67–3.75 × | 편집급 |
| **D12** | Table 1 각주 e (10000–15000+ cycles) **무인용** ↔ 같은 표의 LFP 값은 서술 근거 | LCOS 의 핵심 입력 |

# 후속 후보 (원전 우선)

| 순위 | 원전 | 왜 |
|---|---|---|
| ★★★ 1 | **Li Qianya, Liu, Ye, Li, Wu, Li, Chen — "The critical importance of stack pressure in batteries", *Nat. Energy* 2025, 10, 1064** [23] | 13호가 "perhaps most critically" 라 부른 압력 문제의 인용 원전 — **Q6 요구 창의 정본 후보**(8호 Xu 2024 · 12호 Tian/Shao 와 삼각 대조) |
| ★★★ 2 | **Zhang et al. — "Silicon-based ASSBs operating free from external pressure", *Nat. Commun.* 2025, 16, 1013** [45] | "pressure-less" 의 실험 근거 — **압력 0 에서의 접촉 손실 시계열**이 있는지 (Q1·Q6 동시) |
| ★★ 3 | **Li Menglin et al. — "Stack Pressure Enhanced Size Threshold of Si Anode Fracture in ASSBs", *AFM* 2025, 35, 2415696** [35] | `<5 MPa` 의 근거 후보 — 압력 → 파괴 문턱 사상 |
| ★★ 4 | **Oh Jihoon et al. — "ASSBs with extremely low N/P ratio operating at low stack pressure", *AEM* 2025, 15, 2404817** [34] | 저압 운전의 실셀 데이터 |
| ★★ 5 | **Gu, Liang, Shi, Yang — "Electrochemo-Mechanical stresses and their measurements in sulfide-based ASSBs: a review", *AEM* 2023, 13, 2203153** [38] | 9호 힘 시계열의 측정법 계보 · "지배 실패 모드" 정의의 원전 |
| ★ 6 | **Pang, Yang, Brugge, … Marinescu, Wang, Offer — "Interactions are important: linking multi-physics mechanisms to the performance and degradation of SSBs", *Mater. Today* 2021, 49, 145** [51] | 10호 Pang 2019 의 자매 — multi-physics 결합에서 접촉 손실 항의 형태 |
| ★ 7 | **Kohtz, Xu, Zheng, Wang — PIML SOH from partial charging segments, *MSSP* 2022, 172, 109002** [40] | 13호 SOH 이분법 문장의 인용 원전(자기 공저) — 부분 충전 구간 라벨의 정의 |
| ★ 8 | **Schmidt, Melchior, Hawkes, Staffell — LCOS projection, *Joule* 2019, 3, 81** [18] | LCOS 식의 원전 — `d`(열화율) 취급법 (G1) |

큐 13~37 과의 겹침: 큐 문서를 위 8 편의 저자·제목으로 검색 — **겹침 0 건** (13 Maxwell Protocol
*Angew* · 14 IISE Smart BMS 와 무관).
