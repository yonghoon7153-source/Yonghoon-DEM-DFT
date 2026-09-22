<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-09-22 작성.
     ★ 이 편은 **`papers/wang2026_lirich_mn_cathode_solid_state_review.md` 의 ref 42 원문**이다.
       그 리뷰 digest 가 "원출처를 따로 digest 해야 센다"고 F4·⛔③ 에 두 번 적어 둔 바로 그 논문 —
       판정은 §0a 에 있고, 리뷰가 2차로 옮긴 수치 3건을 여기서 **원문으로 승격**한다.
     ⚠ 실험 논문이다. **자체 계산 0건** — 우리 DFT 와 *수치로* 맞댈 수 있는 자리는 좁고,
       그 좁은 자리를 §7 에서 "되는 곳 / 안 되는 곳"으로 갈라 적었다. -->

# High-Energy and Long-Cycling All-Solid-State Lithium-Ion Batteries with Li- and Mn-Rich Layered Oxide Cathodes and Sulfide Electrolytes — Wubin Du et al. (*ACS Energy Lett.* **2022**, 7, 3006−3014)

> slug `du2022_lmro_lpscl_reversible_redox_assb` · DOI `10.1021/acsenergylett.2c01637` · type `exp (자체 DFT 0 · 자체 MD 0 · 전편 실험)` · PDF `65beba50-19._High-energy…pdf` (본문 9 pp) + `e2319ab9-19._Sup_…pdf` (SI 24 pp) · digested `2026-09-22` · status ✅

> elements: Li, P, S, Cl, Mn, Ni, Co, O, Nb, In
> methods: XPS

> 🎤 **관련 발표**: 없음 (`litdb/talks/*.md` 인입 대기열 전수 확인 — `lee2026_skku_mlip_materials_design.md` 의 9건 어디에도 이 논문 없음)
> 🔗 **역링크**: 이 편은 **`papers/wang2026_lirich_mn_cathode_solid_state_review.md` 의 `ref 42` 원문**이다 — 그 리뷰 digest 의 §10-**F4** 와 §11-1 이 *"원출처를 직접 digest 해야 센다"* 고 두 번 적어 둔 논문이고, **2026-09-22 에 양쪽을 다 갱신했다**(그쪽 머리말 + F4 해소 + §11-1 1번 완료 표시). **⛔ 방향은 이 digest → 리뷰가 아니라, 리뷰의 2차 인용을 이 원문이 *대체* 하는 것이다** — 값이 충돌하면 **이 편이 정본이다**.

> **저자**: **Wubin Du**^a,b,⊥ · **Qinong Shao**^b,⊥ · Yiqi Wei^b · Chenhui Yan^b · Panyu Gao^c · Yue Lin^d · Yinzhu Jiang^b · Yongfeng Liu^b · Xuebin Yu^c · **Mingxia Gao\***^b · Wenping Sun^b · **Hongge Pan\***^{a,b}  (⊥ Du·Shao 공동 1저자)
> · ^a **西安工业大学 新能源科学技术研究院** (Xi'an Technological University, Institute of Science and Technology for New Energy), Xi'an 710021
> · ^b **浙江大学 硅材料国家重点实验室 + 材料科学与工程学院** (Zhejiang University, State Key Laboratory of Silicon Materials & School of MSE), Hangzhou 310027
> · ^c **复旦大学 材料科学系** (Fudan University), Shanghai 200433 — XPS·HRTEM 담당
> · ^d **中国科学技术大学 合肥微尺度物质科学国家研究中心** (USTC, Hefei National Research Center for Physical Sciences at the Microscale) — 구면수차보정 STEM 담당
> · 교신: `gaomx@zju.edu.cn` (Mingxia Gao) · `honggepan@zju.edu.cn` / `hgpan@zju.edu.cn` (Hongge Pan)
> · 지원: **NSFC 중점 51831009 · 51571178** + **国家杰出青年科学基金 52125104** + NSFC 52071285 · 51901168 · 이해상충 없음
> · 접수 **2022-07-18** / 수락 **2022-08-12** / 게재 **2022-08-17** · *ACS Energy Letters* **Letter**
> · 본문 9 pp (refs **48**) · SI 24 pp (`Fig. S1–S12` · `Table S1` 12행 + SI refs 12) · Fig 1–4

---

## 0. 이 digest 를 읽는 법

### 0a. ⭐⭐⭐ 첫 판정 — **이 논문이 Du 2022 = `[Wang26LRM]` 의 ref 42 가 맞다**

우리 litdb 는 이 논문을 **두 번 이름으로 지명해 두고 있었다**:

| 우리 기록 | 적혀 있던 것 |
|---|---|
| `papers/wang2026_lirich_mn_cathode_solid_state_review.md` **§0b-1 / F4** | *"`Li₆PS₅Cl` 은 **≈2.5 V 이상에서 가역적 산화분해**를 겪고 폴리설파이드를 만들며, 그 폴리설파이드는 **2.3 V 아래 방전에서 환원**된다"*(§3.2, **ref 42 = Du 2022 *ACS Energy Lett.***) — *"재인용 + 방법 미표기. **원출처 ref 42(Du 2022 ACS Energy Lett. 7, 3006)를 직접 digest 해야 한다**"* |
| `comparison_vs_ours.md` 줄 1643 (⛔ 인용금지 목록 ③) | *"**`Li₆PS₅Cl` ≈2.5 V 산화분해**(ref 42) 를 축 B① **5번째 kinetic 데이터점으로 세는 것** — 방법 미표기 재인용이다. **원출처 `Du 2022 ACS Energy Lett. 7, 3006` 을 별도 digest 해야 센다.**"* |

**세 갈래로 대조했고 셋 다 맞는다** ⇒ **동일 논문 확정**:
1. **서지** — `ACS Energy Lett.` **2022**, **7**, **3006−3014**, 1저자 **Wubin Du**. 세 항목 전부 일치 (PDF 메타 `nz2c01637`).
2. **문장** — 본문 p.3009 원문: *"LPSCl **starts to oxidize at approximately 2.5 V** during the first cycle, and it undergoes **partial reduction starting at around 2.3 V** (`Fig. 3a`)"* ⇒ 리뷰 §3.2 문장의 **직역 수준 출처**다.
3. **그림** — 리뷰의 `Fig. 7c`(리뷰 digest 가 figure-read 로 *"σ_ion 6×10⁻⁸→6×10⁻⁶ · σ_e 7×10⁻⁷→7×10⁻⁵ S/cm · C2/m 38→28 wt%"* 라고 적어 둔 그림)는 **이 논문의 `Fig. 2d` 를 재수록한 것**이다. 원문 `Fig. 2d` 를 실독한 결과 **σ·자릿수는 정확히 일치**하고 C2/m 만 `38 → ≈26 wt%`(우리 재판독)로 2 %p 차 ⇒ **리뷰 digest 의 figure-read 는 신뢰할 만했다**.

**⇒ 이 digest 의 가장 큰 값은 "2차 → 1차 승격" 이다.** 아래 §0b 표.

### 0b. ⭐ 리뷰가 2차로 옮긴 것 → **원문으로 승격 (3건)** + **승격 불가 (2건)**

| # | `[Wang26LRM]` 이 적은 것 (2차) | **이 논문의 원문 (1차)** | 판정 |
|---|---|---|---|
| **1** | *"`Li₆PS₅Cl` ≈2.5 V 이상 가역 산화분해 · 폴리설파이드는 2.3 V 아래 방전에서 환원"* (방법 0) | **CV, 0.1 mV s⁻¹, (LPSCl+VGCF 90:10 wt)/LPSCl/In–Li, 10 mg 로딩, 27 °C, 4사이클.** 산화 개시 ≈**2.5 V** vs Li/Li⁺, 환원 개시 ≈**2.3 V**. 반응식까지 명시: 산화 `PS₄³⁻ → −S⁰− + P₂S₇⁴⁻`(ref 18 Schwietert 2020), 환원 `−S⁰− → S²⁻`(ref 18, 36 Tan 2019) | ✅ **승격 — 축 B① kinetic onset 데이터점으로 셀 수 있다**(§7b). ⛔ 단 우리 2.256 V 와 같은 표에 넣지 않는다 |
| **2** | `Table 1` 이 **ref 66 행에** 넣어 둔 *"244.5 mAh g⁻¹ · 1000사이클 83 %"* (ref 42 는 표에 행이 아예 없었다 — 리뷰 digest §10 불일치 12건 중 1건) | **이 논문의 값이 맞다.** `LRCo10@5LN` **244.5 mAh g⁻¹**(10사이클 활성화 후, 0.1C) · `LRCo10@10LN` **1000사이클 83 %**(0.5C) | ✅ **승격 + 리뷰의 표 오배치 확정** |
| **3** | `Fig. 7c` (=이 논문 `Fig. 2d`) 의 σ·`C2/m` 자릿수 | **원문 본문값**: `LRCo0` σ_e **3.44×10⁻⁹** · σ_ion **2.65×10⁻¹⁰** S cm⁻¹ / `LRCo10@5LN` σ_e **1.82×10⁻⁵** / `LRCo10@10LN` σ_e **7.36×10⁻⁵** S cm⁻¹ = LRCo0 대비 **4 자릿수↑** | ✅ **승격** — ⛔ 단 σ 절대값 인용은 우리 규율상 여전히 금지, **자릿수 간격만** |
| **4** | *"`Li₂MnO₃`\|`Li₆PS₅Cl` 계면저항 **3722 Ω**"* (ref **93**) | **이 논문이 아니다.** 이 논문의 계면저항은 `R_cathode` **39 Ω(1사이클) → 262 Ω(1000사이클)**, 액체셀 **1989 Ω**. 3722 Ω 은 여전히 미추적 | ⛔ **승격 불가** — ref 93 을 따로 구해야 한다 |
| **5** | *"분해산물 `SO₄²⁻`·`SO₃²⁻`·`P₂Sₓ`, **>4.4 V 생성 · 2.0 V 방전 후에도 잔존 = 비가역**"* (ref **94**, `Fig. 13c`) | **이 논문이 아니다.** 다만 ⭐ **이 논문의 `Fig. 3c,d` 가 같은 것을 보여 주면서 본문이 그것을 안 쓴다** — 1000사이클 후 S 2p 에 **`SO₃²⁻` 168.5 eV**, P 2p 에 **`PSₓOᵧ³⁻` 133.9 eV 가 주성분**(§10-2) | ⛔ 승격 불가 (다른 ref) · ⭐ **그러나 ref 94 의 주장을 이 논문의 그림이 *독립적으로* 지지한다** |

### 0c. 본 그림 / 안 본 그림 (크로핑 **17장 중 10장 실독**)

- ✅ **본 것 (10)**: `Fig. 1`(XRD + σ 막대 + 1사이클 + 100사이클) · `Fig. 2`(8패널 — 이 편에서 수치가 제일 많다) · **`Fig. 3`(CV 2장 + S 2p/P 2p XPS 각 5단 — 우리 축에 제일 가까운 그림)** · `Fig. 4`(HAADF-STEM 8패널, 액체 vs 전고체 1000사이클) · **`Fig. S1`(LPSCl 자체 σ·Ea·σ_e — 축 A/D 앵커)** · `Fig. S7`(액체 vs 전고체 4패널) · `Fig. S8`(LCO 방전하한 대조) · **`Fig. S9`(LPSCl 자체 충방전 — §10-1 의 근거)** · `Fig. S10`(EIS 6패널) · `Fig. S12`(EELS 8패널, 산소방출 깊이)
- ⛔ **안 본 것 (6)**: `Fig. S2`(형태·TEM) · `Fig. S3`(STEM-EDS 매핑) · `Fig. S4`(Co 계열 σ 원시곡선) · `Fig. S5`(Co 계열 액체셀) · `Fig. S6`(yLN 계열 σ 원시곡선) · `Fig. S11`(복합양극 SEM 전/후).
  **이유**: `S4`·`S6` 은 `Fig. 1b`·`Fig. 2d` 막대의 **원시 I–V/Nyquist** 라 값이 이미 본문·막대에 있고, `S2`·`S3`·`S11` 은 **형태/원소분포 정성 이미지**(수치축 없음), `S5` 는 액체셀 Co 계열로 우리 축에 안 걸린다.
- 📄 **`Table S1`(tab_S1.png)은 이미지로 안 봤다** — 관례대로 **PDF 텍스트에서 12행 전 셀 복원**(§3g).
- 🔎 **그림에서만 읽은 값은 전부 `figure-read ≈`** 로 표시했다.
- ⚠⚠ **크로핑 도구 오탐 2건을 사람이 고쳤다** (`tools/litdb/extract_figures.py`):
  · **`Fig. S7` 이 "그래픽 없음(img0/draw0)"으로 제외**됐는데, SI p.15 에는 **벡터 경로가 6,212개** 있다 = **오탐(false negative)**. 캡션 위 영역을 자를 때 세로 경계가 너무 아래로 잡힌 것으로 보인다(패널 c,d 안의 축 라벨 텍스트를 본문 문단으로 오인).
  · **`Fig. S10` 은 자동 크롭이 패널 `e`·`f` 만** 잡았다 (같은 원인). **a–d 가 통째로 날아가 있었다** — 그런데 그 a–d 가 이 논문에서 우리에게 제일 쓸모 있는 EIS 분해다(§3f).
  · 둘 다 **SI 페이지를 캡션 위 전 영역으로 다시 렌더**해 `fig_S7.png`·`fig_S10.png` 로 교체하고 `figures.json` 에 `note_manual` 을 남겼다.

### 0d. 🟢 우리가 가져올 수 있는 것 / 🔴 가져오면 안 되는 것

| 🟢 전이 가능 | 왜 | 🔴 전이 금지 | 왜 |
|---|---|---|---|
| ⭐⭐⭐ **방전하한 2.0 V vs 2.5 V 의 갈림** — 2.0–4.8 V 에선 환원 피크가 있고 2.5–4.8 V 에선 없다 | **우리 산화 onset 2.256 V 가 정확히 그 둘 사이에 있다**(§7b-1). 절대값 일치를 요구하지 않는 **괄호(bracketing) 검증** | **σ(LPSCl) 4.73 mS cm⁻¹** | 우리 MLIP-MD σ 절대값 인용 금지 규율 + 측정은 냉간압축 펠릿 **총전도도**(입계 포함) |
| ⭐⭐ **4.8 V 충전 후 XPS 산물 = `P₂S₇⁴⁻` + `−S⁰−`** | 우리 `interface_reactivity` 가 **4.0/4.5 V 에서 `Li₆PS₅Cl → Li + P₂S₇ + SCl + 0.5 S`** 를 낸다 — **P₂S₇ 와 원소 S 가 같은 전압대에서 실측된다**(§7b-2) | **Ea(LPSCl) 0.335 eV** | 실험 EIS 총 Ea(입계 포함) vs 우리 MLIP-MD 단결정 tracer Ea — **다른 양**(§7a) |
| ⭐⭐ **P 가 S 보다 더 산화된다**(`PSₓOᵧ³⁻` 133.9 eV, ref 37 Janek 그룹과 일치) | **우리 §D 인산염 경로의 전제**(P 가 O 싱크다)에 대한 **실험 근거**. Nd 는 안 건드리지만 P–O 화학 자체를 앵커 | **`R_cathode` 262 Ω · `3722 Ω`류 저항 전부** | **면적 정규화(Ω cm²) 없음**. 셀 형상·압력 의존 |
| ⭐ **σ_e(LPSCl) = 4.11×10⁻⁹ S cm⁻¹** | `[Deng26PS]` 의 **5.69×10⁻⁹** 와 **같은 자릿수 독립 2번째 실측** ⇒ *"LPSCl σ_e ≈ 4–6×10⁻⁹ S cm⁻¹"* 의 문헌 합의 (⚠ 우리는 σ_e 를 계산한 적이 없다, §7d) | **영률 ≈20 GPa** | ⚠ 원출처가 ref 46 = **McGrogan 2017**(`Li₂S–P₂S₅` **유리**, 나노인덴테이션)로 추적된다 — **결정질 아지로다이트도 아니고 DFT 도 아니다**. 우리 `E_VRH` 22.06/27.66 GPa 옆에 놓지 않는다(§7c) |
| ⭐ **공정이 SE 를 망가뜨리는 정량**: σ 4.73 → 1.48(볼밀) → **0.21 mS cm⁻¹**(EtOH), Ea 0.335 → 0.368 → **0.424 eV** | 우리 §H "공정 축 없음" 공백의 **문헌 눈금**. 그리고 이 논문 복합양극의 SE 는 **BM+EtOH 등급**이다(§10-9) | **용량·에너지밀도·유지율 전부** | 조립압(510 MPa)·스택압(15 N·m)·면적용량·CC 모드 지배. **n=1** |
| ⭐ **"양극 쪽 산소가 SE 로 넘어온다"의 직접 증거** (`PSₓOᵧ³⁻`·`SO₃²⁻` 생성) | 우리 0-압력 grand-potential 이 **양극의 O 를 반응물로 쓰는 축**(`interface_reactivity`)과 **자기분해 축**(ESW) 중 어느 쪽인지 갈라 주는 실측(§7b-3) | **"LMRO+LPSCl 계면은 안정하다"** | **맨 계면을 한 번도 안 만들었다** — 전 시료가 `LiNbO₃` 2 wt% + `LPSCl` 15 wt% **이중코팅**(§10-4) |

---

## 1. 한 줄 요약

**Li·Mn 과잉 층상산화물(LMRO) 양극을 `Li₆PS₅Cl` 전고체 셀에 처음으로 실용 수준으로 올린 논문이고, 그 핵심 논리는 "LMRO 의 방전하한이 2.0 V 라서, 충전 중 `Li₆PS₅Cl` 이 산화돼 만든 폴리설파이드(`−S⁰−`)가 방전 때 `S²⁻` 로 되돌아간다 — 그래서 LCO·NCM(하한 2.5–3.0 V) 계에서 누적되던 절연성 `−S⁰−` 가 여기서는 안 쌓인다"** 는 것이다. 여기에 양극 쪽에서 **Co 함량 + 공칭 `LiNiO₂` 성분**을 조절해 LMRO 자체의 전자·이온전도도를 **4 자릿수** 끌어올려, **244.5 mAh g⁻¹ · 853 Wh kg⁻¹**(0.1C)와 **0.5C 1000사이클 83 % 유지**(액체셀 36 %)를 낸다.

⚠ **우리 입장에서의 한 줄**: 이 편은 *"황화물 SE 의 산화분해를 막지 말고, **되돌릴 수 있는 전압창 안에서 살게 하라**"* 는 **설계 전환**이다. 우리 캠페인(도핑으로 **분해 구동력 자체를 낮춘다**)과 **경쟁이 아니라 직교**한다 — 그리고 우리 산화 onset **2.256 V** 가 저쪽이 실험으로 찾아낸 갈림선(2.0 V 는 되고 2.5 V 는 안 된다) **정확히 안쪽에 있다**(§7b-1). 이 논문은 우리 숫자의 **가장 값싼 외부 검증**이다.

---

## 2. 메타 / 동기 / 질문

| 저자 | 저널/년 | DOI | 조성 | 연구유형 |
|---|---|---|---|---|
| **Wubin Du**·**Qinong Shao**(공동1) … **Mingxia Gao\***·**Hongge Pan\*** (西安工业大 + 浙江大 + 复旦大 + 中科大) | ***ACS Energy Lett.*** **2022**, **7**, 3006−3014 (접수 2022-07-18 / 수락 2022-08-12 / 게재 2022-08-17) | `10.1021/acsenergylett.2c01637` | **양극** `0.5LiNi₀.₃₃Co₀.₃₃₊ₓMn₀.₃₃₋ₓO₂–0.5Li₂MnO₃` (x=0→0.33, `LRCo0`…`LRCo33`) · `LRCo10–yLiNiO₂` (y=0.03→0.10, `@3LN`…`@10LN`) · **전해질 `Li₆PS₅Cl`** (3등급: `LPSCl`·`LPSCl-BM`·`LPSCl-EtOH`) · **코팅** `LiNbO₃`(2 wt%, 1–2 nm) + `LPSCl`(15 wt%) · **음극** In(100 μm)+Li(50 μm) · **도전재** VGCF · **대조** 액체셀 1 M `LiPF₆` EC:DMC:DEC 1:1:1 | **실험** — 자체 DFT·MD·NEB **0건**. 계산 인용도 ref 17(Zhu/Mo 2015)·ref 18(Schwietert 2020) **둘뿐** |

### 2a. 저자들이 던진 문제

1. LCO·NCM 은 작동전압 **4.3 V**, 실용용량 **≈200 mAh g⁻¹**, 에너지밀도 **≈760 Wh kg⁻¹** 에서 한계에 왔다.
2. LMRO(`xLi₂MnO₃·(1−x)LiTMO₂`)는 가역용량 **>280 mAh g⁻¹**, 에너지밀도 **>1000 Wh kg⁻¹** 이지만 — (i) 작동전압이 **4.8 V** 로 높고 (ii) 전자전도도 **≈10⁻⁹–10⁻⁸ S cm⁻¹**, 이온전도도 **≈10⁻¹¹ S cm⁻¹** 로 **절망적으로 낮다** ⇒ *"to the best of our knowledge, **there is no report on the application of LMROs in ASSLIBs**"*.
3. 황화물 SE 쪽: *"theoretical calculations and experimental results show that **elemental S in the sulfide electrolytes undergoes oxidative decomposition above 2.5 V**"*(ref 5 Cao 2020 · **ref 17 Zhu/He/Mo 2015** · **ref 18 Schwietert 2020**) ⇒ LCO·NCM 이 도는 **2.5–4.3 V** 창에서는 **절연성 `−S⁰−` 가 계속 쌓인다**(ref 19 Koerver 2017, ref 20 Wang 2021).
4. **저자들의 착상**: Li–S 전지 문헌에서 **`S⁰` 는 2.0–2.3 V 에서 환원된다**(ref 23, 24). 그런데 **LMRO 의 방전하한이 바로 2.0 V** 다. ⇒ *"we speculate that combining LMROs with sulfide electrolytes … might mitigate the deterioration of the cathode−electrolyte interface"*.

**⇒ 이 논문의 논리 구조 한 줄**: 「SE 가 2.5 V 위에서 산화된다」 + 「그 산물은 2.0–2.3 V 에서 환원된다」 + 「LMRO 의 창이 2.0–4.8 V 다」 = **창이 산물을 회수한다**.

---

## 3. 핵심 수치 총정리 ★

> ⚠ 전압은 전부 **vs Li⁺/Li**. 원 측정은 vs In/InLi 이고 **오프셋 정확히 +0.62 V** (SI: `1.38–4.18 V vs In/InLi` ≡ `2.0–4.8 V vs Li⁺/Li`). 온도는 전부 **27 °C**.

### 3a. `Li₆PS₅Cl` 자체 (`Fig. S1`, `Note S1`) — **우리 축 A/D 와 직접 닿는 유일한 표**

| 등급 | 입자크기 | σ_ion (27 °C) | **Ea** | 용도 | 비고 |
|---|---|---|---|---|---|
| **`LPSCl`** (볼밀 + 550 °C 5 h 소성) | **30–50 μm** | **4.73 mS cm⁻¹** | **0.335 eV** | **분리막/전해질층** | 회색 분말 |
| **`LPSCl-BM`** (p-xylene 중 400 rpm 6 h 재분쇄 → 200 °C 증발) | **2–5 μm** | **1.48 mS cm⁻¹** | **0.368 eV** | **복합양극의 이온전도재** | 흰색 |
| **`LPSCl-EtOH`** (무수에탄올 용해 → 180 °C 진공 5 h) | — | **0.21 mS cm⁻¹** | **0.424 eV** | **양극입자 표면 코팅층** | 용액공정 |

- **σ_e(`LPSCl`) = 4.11×10⁻⁹ S cm⁻¹** — DC 분극 `SS/LPSCl/SS`, 1 V, 정상전류 **32.3 nA** (`Fig. S1h`).
- Arrhenius 는 **0 / 10 / 20 / 27 / 40 / 50 / 60 °C 7점**, EIS 1 MHz–10 Hz, 펠릿 **510 MPa** 냉간압축, d = 1.0 mm (EtOH 만 0.78 mm).
- ⚠ **XRD 지시상이 `Li₇PS₆` PDF#34-0688** 이다(`Fig. S1c`) — 아지로다이트 계열이긴 하나 `Li₆PS₅Cl` 카드가 아니다. 흔한 관행이지만 상순도 논거로 쓰기엔 약하다.
- 🔎 **figure-read**: `LPSCl-EtOH` 의 XRD 피크는 **(331)·(531)·(620) 이 거의 사라질 정도로 약해지고 폭이 넓어진다** — 저자들은 *"입자크기 감소"* 로만 설명하지만, σ 가 **22배** 떨어진 것과 함께 보면 **에탄올 재석출로 결정성이 실제로 상한 것**으로 읽는 게 정직하다(§10-9).

### 3b. LMRO 양극의 전도도 — **두 레버**

**레버 ① Co 함량** (`Fig. 1b`, 본문 + figure-read)

| 시료 | x(Co 증분) | σ_e (S cm⁻¹) | σ_ion (S cm⁻¹) | `C2/m` wt% |
|---|---|---|---|---|
| `LRCo0` = `Li₁.₂Ni₀.₁₃Co₀.₁₃Mn₀.₅₄O₂` | 0 | **3.44×10⁻⁹** (본문) | **2.65×10⁻¹⁰** (본문) | figure-read ≈ **43** |
| `LRCo05` | 0.05 | figure-read ≈ 6.5×10⁻⁸ | ≈ 2.6×10⁻⁹ | ≈ 40 |
| **`LRCo10`** (최적) | 0.10 | ≈ 7×10⁻⁷ | ≈ 6×10⁻⁸ | ≈ 38 |
| `LRCo15` | 0.15 | ≈ 4×10⁻⁶ | ≈ 4×10⁻⁷ | ≈ 34 |
| `LRCo20` | 0.20 | ≈ 1.7×10⁻⁵ | ≈ 1.6×10⁻⁶ | ≈ 31 |
| `LRCo25` | 0.25 | ≈ 4×10⁻⁵ | ≈ 3×10⁻⁶ | ≈ 27 |
| `LRCo33` | 0.33 | ≈ 2×10⁻⁴ | ≈ 1.5×10⁻⁵ | ≈ 24 |

⇒ **Co 0→0.33 에서 σ_e·σ_ion 이 각각 ≈5 자릿수 오른다**(figure-read). 기전: `Li₂MnO₃`(`C2/m`) 분율이 **≈43 → ≈24 wt%** 로 줄어 절연상이 빠지는 것 (`Fig. 1a` 20–24° 초격자 hump 가 단조 감소).
⚠ **그런데 전도도 1등이 성능 1등이 아니다** — `LRCo33` 은 σ 가 제일 높은데 1사이클 방전은 낮다(`Fig. 1c`). 저자들은 *"trade-off between electrochemical performance and electrical conductivity"* 로 **`LRCo10` 을 선택**한다. 🔎 figure-read: `Fig. 1d` 100사이클에서 `LRCo10`(파랑)만 ≈213→≈116, 나머지는 전부 100 아래.

**레버 ② 공칭 `LiNiO₂` 성분** (`Fig. 2d`, 본문 + figure-read) — `LRCo10@yLN`

| 시료 | 화학식 (SI p.3) | σ_e (S cm⁻¹) | σ_ion (S cm⁻¹) | `C2/m` wt% |
|---|---|---|---|---|
| `LRCo10` (y=0) | `Li₁.₂Ni₀.₁₃Co₀.₁₇Mn₀.₄₉O₂` | figure-read ≈ 7×10⁻⁷ | ≈ 6×10⁻⁸ | figure-read ≈ 38 |
| `@3LN` (y=0.03) | `Li₁.₁₉Ni₀.₁₆Co₀.₁₇Mn₀.₄₈O₂` | ≈ 1×10⁻⁵ | ≈ 5×10⁻⁷ | ≈ 33 |
| **`@5LN`** (y=0.05) | `Li₁.₁₉Ni₀.₁₇Co₀.₁₆Mn₀.₄₇O₂` | **1.82×10⁻⁵** (본문) | ≈ 1.9×10⁻⁶ | ≈ 30 |
| `@7LN` (y=0.07) | `Li₁.₁₈Ni₀.₁₉Co₀.₁₆Mn₀.₄₆O₂` | ≈ 2.8×10⁻⁵ | ≈ 3.3×10⁻⁶ | ≈ 28 |
| **`@10LN`** (y=0.10) | `Li₁.₁₈Ni₀.₂₁Co₀.₁₅Mn₀.₄₅O₂` | **7.36×10⁻⁵** (본문) | ≈ 6.3×10⁻⁶ | ≈ 26 |

⇒ 본문: *"4 orders of magnitude higher than that of `LRCo0` and **reach the level of NCM cathodes**"* (ref 5, 33).
⭐ **구조적 기전은 벌크가 아니라 표면이다** — `Fig. 2b` 의 `LRCo10` 은 표면→벌크가 균일한 층상, `Fig. 2c` 의 `@10LN` 은 **표면에 스피넬상**이 생겼다. 🔎 **figure-read**: `Fig. 2c` 의 라벨이 벌크 `C2/m [103]` / 표면 **`Fd-3m [111]`** 로 **공간군까지 찍혀 있다**(본문은 *"a spinel-like phase"* 로만 씀).

### 3c. 전고체 셀 성능 (2.0–4.8 V vs Li⁺/Li, 27 °C, CC 모드)

| 시료 | 0.1C 1사이클 방전 | 0.1C 100사이클 | 0.5C 700사이클 | 0.5C 1000사이클 | 에너지밀도 |
|---|---|---|---|---|---|
| `LRCo0` | **130 mAh g⁻¹** | figure-read ≈ 35 | — | — | — |
| `LRCo10` | **213.4** | **116.2 (54 %)** | **25 %** | — | — |
| **`LRCo10@5LN`** | **244.5**(10사이클 활성화 후, **최고값**) | **85 %** | figure-read ≈ 122 mAh g⁻¹ | — | **853 Wh kg⁻¹** |
| `LRCo10@7LN` | figure-read ≈ 200 | figure-read ≈ 188 | figure-read ≈ 118 | — | — |
| **`LRCo10@10LN`** | **215** (활성화로 상승) | **감쇠 0** | **90 %** | **83 %** (액체 36 %) | **752 Wh kg⁻¹** |

- **평균 쿨롱효율** (`Fig. 2h`, 0.5C 1000사이클, `@10LN`): **전고체 99.96 % vs 액체 98.91 %**.
  (`Fig. S7c`, `@5LN` 0.5C 700사이클: 전고체 **99.90 %** vs 액체 **98.85 %**)
- **액체셀 1사이클 방전** (`Fig. S7b`): `LRCo10` **260.9** · `@3LN` **252.4** · `@5LN` **247.5** · `@7LN` **235.4** · `@10LN` **231.1 mAh g⁻¹** — **`LiNiO₂` 성분이 늘수록 단조 감소**(전고체에선 반대로 `@3LN`·`@5LN` 이 `LRCo10` 보다 **높다**).
- 🔎 **figure-read, 본문에 없는 것** (`Fig. S7d`): 0.5C 에서 `@10LN` 전고체는 **≈157 mAh g⁻¹ 로 시작**하고 액체는 **≈205** 로 시작한다. 1000사이클 뒤 전고체 **≈130**, 액체 **≈75**. ⇒ **절대값으로도 전고체가 이기지만, "83 % vs 36 %" 는 기준선이 다른 두 곡선을 각자 100 % 로 잡은 표현이다**(§10-6).
- 🔎 **figure-read** (`Fig. S7a` vs `Fig. 2e`): **액체셀의 4.5 V 평탄부가 전고체보다 훨씬 길다.** 액체는 ≈120→≈220 mAh g⁻¹ 구간이 거의 수평, 전고체는 4.4–4.6 V 구간이 짧다 ⇒ **전고체에서 산소 음이온 산화환원 활성화가 부분적으로 억제된다**. 본문은 이 비교를 하지 않는다.

### 3d. ⭐⭐ CV — `Li₆PS₅Cl` 의 산화·환원 전위 (`Fig. 3a,b`)

**셀**: `(LPSCl + VGCF 90:10 wt)` / `LPSCl` / `In–Li`, 복합 작용극 **10 mg**, **0.1 mV s⁻¹**, 27 °C, 각 4사이클. 두 셀을 따로 조립(하나는 2.0–4.8 V, 하나는 2.5–4.8 V).

| 창 | 1사이클 산화 | 1사이클 환원 | 2–4사이클 |
|---|---|---|---|
| **2.0–4.8 V** | **개시 ≈2.5 V**(본문). 🔎 figure-read: 넓은 피크 **≈3.5 V 에서 ≈3.8 mA g⁻¹**, 어깨 **≈4.2 V**, 4.8 V 까지 지속. 라벨 `PS₄³⁻ → S + P₂S₇⁴⁻` 화살표가 **≈3.1→4.6 V** 를 덮는다 | **개시 ≈2.3 V**(본문). 🔎 figure-read: 2.0 V 에서 **≈ −9.5 mA g⁻¹** 까지 급락. 라벨 `S → S²⁻` | 🔎 figure-read: 산화 피크가 **≈3.15 V, ≈1.6 mA g⁻¹** 로 이동·축소, 환원 **≈ −2 ~ −2.5 mA g⁻¹**. **작아지지만 사라지지 않는다** |
| **2.5–4.8 V** | 🔎 figure-read: 1사이클 피크 **≈3.5 V, ≈3.7 mA g⁻¹**(2.0–4.8 V 와 사실상 동일), 어깨 ≈4.25 V | **환원 피크 없음**(본문) | 🔎 figure-read: 거의 0, 4.5–4.8 V 에서만 약간 상승 |

- 본문 해석: 산화 = `PS₄³⁻ → −S⁰− + P₂S₇⁴⁻` (ref 18) · 환원 = `−S⁰− → S²⁻` (ref 18, 36).
- 본문: *"During the following cycles, the decomposition of LPSCl is **kinetically inhibited due to the passivated decomposition layer** formed at the surface during the first cycle (ref 5), **while the decomposition is still reversible**"*.
- ⚠⚠ **`Fig. 3b` 의 y축이 0 에서 시작한다**(0–4 mA g⁻¹). 즉 **작은 음전류가 있어도 그림에 안 나온다** ⇒ *"환원 피크가 없다"* 는 **그것을 보여줄 수 없는 축에서** 주장된다(§10-8).

### 3e. ⭐⭐⭐ XPS — 분해 산물 (`Fig. 3c,d`) · **이 논문에서 우리에게 제일 중요한 데이터**

**장비**: Thermo ESCALAB 250Xi, Al Kα 1486.6 eV, **자체제작 무대기 이송장치**. 시료는 `LRCo10@10LN` **복합양극**(= LPSCl-BM + VGCF 포함).

**S 2p (5단, 172→158 eV)**

| 상태 | 성분 (결합에너지) |
|---|---|
| **pristine `LPSCl`** | **161.4 eV `PS₄³⁻`**(아지로다이트 P–S–Li, 주) + **160.0 eV** 자유 `S²⁻`/`Li₂S` 불순물(부) |
| **복합양극, 사이클 전** | 160.0 eV **소멸** · **163.0 eV `P₂S₇⁴⁻`**(P–S–P) **신규** ⇒ *"slight oxidation of LPSCl **during the preparation of the composite cathode**"* |
| **4.8 V 충전** | **163.6 eV `−S⁰−`**(폴리설파이드) 신규 + `P₂S₇⁴⁻` 증가. 🔎 이 패널에 **`SO₃²⁻` 라벨**도 찍혀 있다(≈168–170 eV 영역) |
| **2.0 V 방전 (1사이클)** | **`−S⁰−` 완전 소멸** ⇒ 본문: *"the `−S⁰−` species can be **completely reduced** … the oxidative decomposition of LPSCl is indeed **reversible in one charge/discharge cycle**"* |
| **1000사이클 후** | 본문: *"main peaks … can still be assigned to `PS₄³⁻` and `P₂S₇⁴⁻`, and the **`−S⁰−` peak does not emerge**"*. 🔎🔎 **figure-read — 본문이 말하지 않는 것 2가지**: ① **`SO₃²⁻` 168.5 eV 피크가 뚜렷하게 새로 있다** ② **보라(`P₂S₇⁴⁻`)가 파랑(`PS₄³⁻`)보다 확실히 크다** = 계면 근처 SE 가 대부분 `P₂S₇⁴⁻` 로 바뀌었다 |

**P 2p (5단, 138→128 eV)**

| 상태 | 성분 |
|---|---|
| pristine `LPSCl` | **131.9 eV `PS₄³⁻`** |
| 복합양극, 사이클 전 | **132.5 eV `P₂S₇⁴⁻`** 신규 |
| 4.8 V 충전 | **133.9 eV `PSₓOᵧ³⁻`** 신규 (**산소가 붙은 P**) |
| 2.0 V 방전 | 본문: *"the oxidized phosphorus is **partially reduced back** after discharging"* — 🔎 figure-read: 133.9 eV 성분이 **줄지만 남는다** |
| **1000사이클 후** | 🔎🔎 **figure-read: `PSₓOᵧ³⁻` 133.9 eV 가 *주성분*이다** (본문은 P 2p 의 1000사이클 상태를 서술하지 않는다) |

- 본문의 결론 문장: *"**phosphorus exhibits a higher degree of oxidation than sulfur**, which is consistent with the results reported by **Janek et al.**(ref 37 = Walther 2019 *Chem. Mater.* ToF-SIMS)"*.
- 본문의 방어: *"the decomposition occurs **only on the surface** of LPSCl, and the `P₂S₇⁴⁻` ions are also **favorable for Li⁺ conduction** as it is an important component for the superionic conductor `Li₇P₃S₁₁`"*(ref 43, 45).
- ⭐⭐ **우리 판정**: **가역인 것은 `S⁰ ⇄ S²⁻` 채널뿐이고, `PSₓOᵧ³⁻`·`SO₃²⁻` 산소화 채널은 비가역이며 그쪽이 자란다**(§10-2). 산소의 출처는 **양극(LMRO)과 `LiNbO₃` 코팅** 말고는 없다.

### 3f. ⭐ EIS — 계면저항의 시간축 (`Fig. S10`) · **자동 크롭이 날려서 사람이 복구한 패널**

**등가회로**: `R_SE` + (`R_anode`‖CPE1) + (`R_cathode`‖CPE2) + CPE3.

**(a,b) 1사이클 안에서** — 🔎 figure-read (본문에 값 없음)

| 상태 | `R_SE` | `R_anode` | **`R_cathode`** |
|---|---|---|---|
| 사이클 전 | ≈25 Ω | ≈16 Ω | **≈78 Ω** |
| **4.8 V 충전** | ≈27 | ≈27 | **≈231 Ω** |
| **2.0 V 방전** | ≈26 | ≈32 | **≈40 Ω** |

⇒ **충전에 3배로 부풀고 방전에 원상보다도 아래로 내려온다.** 본문: *"indicating the **reversible decomposition** of the LPSCl electrolyte in the composite cathode"*. ⭐ **`R_SE`·`R_anode` 는 안 움직인다 — 변하는 것은 오직 양극 계면이다.**

**(c,d) 1000사이클에 걸쳐**

| 사이클 | **`R_cathode`** | `R_SE` | `R_anode` |
|---|---|---|---|
| 1 | **39 Ω** (본문) | ≈26 | ≈26 |
| 300 | figure-read ≈ **101 Ω** | ≈28 | ≈29 |
| 700 | figure-read ≈ **250 Ω** | ≈27 | ≈27 |
| 1000 | **262 Ω** (본문) | ≈29 | ≈30 |

⇒ 본문: *"the `R_cathode` is **only increased from 39 Ω to 262 Ω**, which is much smaller than the increase seen for the liquid battery (**1989 Ω**)"*.
⚠ **우리 판정**: **6.7 배**다. 그리고 🔎 figure-read 로 보면 **증가의 대부분이 300→700 사이클 구간(101→250 Ω)에 몰려 있다** — *"only increased"* 라는 서술이 가리는 부분이다(§10-3). `R_SE`·`R_anode` 가 1000사이클 내내 평평한 것과 대비하면, **열화는 전부 양극\|SE 계면 한 곳**이다 = **우리 §B 의 무대 그 자체**.
⛔ **면적 정규화(Ω cm²)가 없다.** 펠릿 지름 10 mm(면적 0.785 cm²)는 알지만 복합양극의 실접촉면적은 모른다 ⇒ **다른 논문의 Ω 와 직접 비교 금지**.

### 3g. ⭐ `Table S1` — 저자들의 벤치마크 표 (PDF 텍스트 전 셀 복원, 12행)

> "high-voltage oxide cathodes in sulfide-based ASSLIBs at room temperature"

| 양극 | 전해질 | 전압창 (V vs Li/Li⁺) | 방전용량 (mAh g⁻¹) | 에너지밀도 (Wh kg⁻¹) | 용량유지 | ref |
|---|---|---|---|---|---|---|
| **`LRCo10@5LN`** | **`Li₆PS₅Cl`** | **2.0–4.8** | **245** | **853** | 85 (0.1C 100) / 85 (0.5C 300) | **본 연구** |
| **`LRCo10@10LN`** | **`Li₆PS₅Cl`** | **2.0–4.8** | **215** | **752** | 100 (0.1C 100) / 100 (0.5C 300) / **83 (0.5C 1000)** | **본 연구** |
| `LiNi₀.₇₅Co₀.₁₀Mn₀.₁₅O₂` | `Li₆PS₅Cl` | 3.0–4.3 | 196 | 744 | 79 (0.5C 200) | 1 (Jung 2020 *AEM*) |
| `LiNi₀.₈Co₀.₁Mn₀.₁O₂` | `Li₁₀SnP₂S₁₂` | 2.85–4.35 | 187 | 711 | 64 (0.1C 100) | 2 (Liu 2021 *AEM*) |
| `LiNi₀.₅Co₀.₂Mn₀.₃O₂` | `Li₁₀GeP₂S₁₂` | 2.5–4.4 | 161 | 610 | 63 (C/3 500) | 3 (Wang 2021 *AEM*) |
| `LiNi₀.₅Co₀.₂Mn₀.₃O₂` | `Li₁₀GeP₂S₁₂` | 2.5–4.4 | 156 | 588 | 60 (0.1C 150) | 4 (Wang 2020 *ESM*) |
| `LiNi₀.₈Co₀.₁Mn₀.₁O₂` | `Li₁₀GeP₂S₁₂` | 2.7–4.5 | 171 | 633 | 59 (0.2C 300) | 5 (Deng 2020 *ESM*) |
| `LiNi₁/₃Co₁/₃Mn₁/₃O₂` | `Li₇P₃S₁₁` | 2.6–4.4 | 154 | 580 | 87 (0.1C 30) | 6 (Calpa 2019 *EA*) |
| `LiNiO₂` | `Li₆PS₅Cl` | 2.9–4.3 | 188 | 705 | 74 (0.2C 200) | 7 (Ma 2021 *ACS EL*) |
| `LiFePO₄` | `Li₁₀GeP₂S₁₂` | 2.5–4.1 | 148 | 500 | 91 (0.5C 120) | 8 (Wang 2019 *AFM*) |
| `LiCoO₂` | `Li₆PS₅Cl` | 2.6–4.5 | 143 | 552 | 95 (0.2C 100) | 9 (Wang 2021 *AEM*) |
| `LiCoO₂` | `Li₆PS₅Cl` | 2.5–4.2 | 134 | 523 | 72 (0.1C 100) | 10 (Zhao 2020 *ESM*) |
| `LiNi₀.₅Mn₁.₅O₄` | `Li₁₀GeP₂S₁₂` | 3.5–5.0 | 80 | 365 | 71 (0.1C 10) | 11 (Oh 2016 *CM*) |
| `LiNi₀.₅Mn₁.₅O₄` | `Li₆PS₅Cl` | 3.0–4.9 | 78 | 353 | 79 (0.1C 20) | 12 (Wang 2021 *NE*) |

⭐ **우리에게 쓸모 있는 읽기**: **표의 12개 대조군 중 방전하한이 2.5 V 아래인 것은 하나도 없다**(최저 2.5 V). 이 논문만 **2.0 V** 다. ⇒ 저자들의 주장("하한 2.0 V 가 열쇠")은 **표 자체가 방증**한다.
⛔ **하지만 이 표는 벤치마크로 못 쓴다** — 창·C-rate·양극·면적용량·조립압이 전부 다르다. `LiNi₀.₅Mn₁.₅O₄` 행(3.5–5.0 V, 80 mAh g⁻¹)을 이 논문(2.0–4.8 V, 245)과 나란히 놓는 것은 **창 폭이 다른 데서 오는 차이를 화학 차이로 읽게 만든다**(§10-7).
⚠ **표와 본문의 어긋남 2건**: ① 표는 `@5LN` 을 **"245"** 로 반올림(본문 244.5) ② 표의 *"85 (0.5C 300)"* 와 *"100 (0.5C 300)"* 은 **본문에 한 번도 안 나온다**.

### 3h. STEM — 1000사이클 후 구조 (`Fig. 4`)

| | **액체셀** (`Fig. 4a–c`) | **전고체셀** (`Fig. 4d–h`) |
|---|---|---|
| 입자 내부 | **격자무늬 심하게 파괴 + 나노보이드 다수** (🔎 `Fig. 4a` 에 `Void` 라벨 3개, 5 nm 스케일) | *"maintains good structural integrity **without any nanovoids**"* |
| 상 | 층상 → **스피넬형 `Li_xMn₂O₄`** 로 광범위 전환. 🔎 `Fig. 4c` FFT 에 `(3–11)`·`(–111)` 지수와 **끼인각 58.52°**, `Spinel-like [11̄2]` | 표면 **6 nm 스피넬층이 보존**되고 내부는 층상 유지 (`Fig. 4g,h`) |
| 계면 | — | *"the lattice of the cathode surface is well sustained, and **only about 2 unit cells are damaged**"*; **`LPSCl` 이 여전히 양극 표면을 덮고 있다** (`Fig. 4d`, 10 nm 스케일) |

⚠ **우리 판정**: `Fig. 4e` 에는 **계면상(interphase)이 보이지 않는다**. 하지만 같은 시료의 XPS(`Fig. 3c,d`)는 **산화된 P·S 종이 있다**고 말한다. 둘은 모순이 아니다 — **HAADF-STEM 은 ~1 nm 비정질 산황화물층을 SE 배경에서 못 가른다**. 문제는 이 논문이 `Fig. 4` 를 *"반응이 없었다"* 의 증거처럼 배치한다는 것이다(§10-13).

### 3i. EELS — 산소 방출 깊이 (`Fig. S12`, `Note S2`)

| | **액체셀 1000사이클** | **전고체셀 1000사이클** |
|---|---|---|
| O K-edge pre-peak 감소 깊이 | **50 nm** (`Oxygen loss (50 nm)` 라벨) | **4 nm** (`Preserved oxygen lattice` 라벨) |
| Mn L₃/L₂ 표면값 | 🔎 figure-read ≈ **2.8** (`Mn^2.67+` 라벨) | 🔎 figure-read ≈ **2.55** (`Mn³⁺`) |
| Mn⁴⁺ 회복 깊이 | **50–60 nm** 에서야 ≈1.95(Mn⁴⁺ 기준선) | 🔎 **≈6 nm** 에서 이미 ≈2.0, 이후 24 nm 까지 평평 |
| Mn³⁺ 매핑 분포 | 두꺼운 외각 전체 (50 nm 스케일바) | **가장자리 얇은 띠만** (10 nm 스케일바) |

⇒ 본문: *"the **stubborn oxygen release problem** of LMROs … can also be significantly **suppressed in sulfide-based ASSLIBs**"*.
⭐ 이 논문이 내세우는 전고체의 3대 이득: **TM 용출 억제 · 산소방출 억제(50→4 nm) · 층상→스피넬 전이 억제**.

### 3j. LCO 대조군 — *"그럼 LCO 도 2.0 V 로 내리면 되잖아"* (`Fig. S8`)

- 0.1C 1사이클: 충전 🔎 ≈178 mAh g⁻¹, 방전 🔎 **≈152**(2.0–4.3 V) vs **≈155**(3.0–4.3 V) mAh g⁻¹ — 거의 같다.
- **0.5C 700사이클 유지율: 3.0–4.3 V → 72 % · 2.0–4.3 V → 63 %** ⇒ **하한을 내리면 LCO 는 더 나빠진다.**
- 본문: *"it will lead to the **over-insertion of lithium in the LCO**, which is not conducive to the cycle performance"*.
- ⚠ **이 대조는 SE 환원 효과를 분리하지 못한다** — LCO 과리튬화라는 **양극 쪽 손상**과 SE 폴리설파이드 환원이라는 **전해질 쪽 이득**이 같은 실험 안에 섞여 있고, 순효과는 **음**이다. 그리고 정작 필요한 실험(**같은 LMRO 셀을 2.5–4.8 V 와 2.0–4.8 V 로 각각 사이클**)은 **안 했다**(§10-5).

### 3k. `Li₆PS₅Cl` 자체가 내는 용량 (`Fig. S9`) — ⭐ **§10-1 의 근거**

`(LPSCl + 10 wt% VGCF)` / `LPSCl` / `In–Li`, **20 mA g⁻¹**:

- 본문: *"it can **only provide a discharge capacity of about 3 mA h g⁻¹ within 2.3–2.0 V** … Therefore, the discharge capacity of LMRO-based ASSLIB **mainly comes from the LMRO cathode itself**"*.
- 🔎🔎 **figure-read — 본문이 안 쓴 두 값**:
  · **1사이클 충전 용량 ≈11.5 mAh g⁻¹** (4.8 V 까지). 방전은 ≈3.0 ⇒ **SE 산화환원의 1사이클 쿨롱효율 ≈26 %**.
  · **사이클 거동**: 2.95 → 1.17 → 0.9 → … → **≈0.2 mAh g⁻¹ 로 20사이클쯤에 정착**하고 100사이클까지 그대로.
- ⇒ **"가역"의 실체 = 작고, 자기제한적이며, 대부분 1사이클에서 끝난다.** 이건 셀 입장에선 **좋은 소식**(부동태화)이지만, 논문 초록의 *"can be reversibly oxidized and reduced"* 보다는 훨씬 약한 진술이다(§10-1).

---

## 4. 재료 & 방법 — 우리가 같은 축을 흉내 낼 때 필요한 조건 전부 ★

### 4a. 합성

- **LMRO (분무열분해)**: Li/Mn/Co/Ni **아세테이트** 를 화학량론비로 **5000 mL** 탈이온수에 **0.3 mol L⁻¹** → **시트르산 0.8 mol**(착화제, 금속염 침전 억제) → **80 °C 수욕, 500 rpm, 1 h** → **200 °C 고압가스**로 연동펌프 분무 → 전구체 분말 → **900 °C 10 h, 공기중** 소성.
- **`Li₆PS₅Cl`**: `Li₂S` 를 **LiH + S (2:1) 500 rpm 24 h 볼밀**로 자체합성 → `Li₂S : P₂S₅ : LiCl = 5 : 1 : 2` **500 rpm 24 h 볼밀** → **550 °C 5 h, 승온 5 °C min⁻¹** 소성 (회색 `LPSCl`) → p-xylene 중 **400 rpm 6 h** 재분쇄 → 200 °C 용매증발 (흰색 `LPSCl-BM`).
- **`LiNbO₃` 코팅 (2 wt%)**: Li 금속 + niobium ethoxide 를 무수에탄올 2 mL 에 용해, 30 min → 양극 1 g 투입 3 h 교반 → **120 °C 진공 10 h** → **400 °C, O₂ 기류, 1 h**. 두께 **1–2 nm** (`Fig. S3`).
- **`LPSCl` 코팅**: `LPSCl` **75 mg** 을 무수에탄올 2 mL 에 용해(노란 용액) → `LiNbO₃`-코팅 양극 **425 mg** 투입 3 h → **180 °C 진공 5 h**. ⇒ **양극 대비 LPSCl 약 15 wt%**.
- 전 공정 **Ar 글러브박스 (O₂ < 0.1 ppm, H₂O < 0.1 ppm)**.

### 4b. 셀 (핵심 조건)

- **PEEK 슬리브 Ø10 mm + SS 로드 2개** (자체제작).
- 분리막: `LPSCl` **100 mg**, **120 MPa 1 min** 냉간압축.
- 복합양극: `LPSCl-코팅 양극` : `LPSCl-BM` : `VGCF` = **60 : 35 : 5 wt**, **10 mg**, **510 MPa 3 min** 단축가압.
- 음극: **In 박 100 μm + Li 박 50 μm**.
- 스택압: SS 프레임 나사 **15 N·m 토크** (⛔ MPa 환산값 미기재).
- 시험: **1.38–4.18 V vs In/InLi ≡ 2.0–4.8 V vs Li⁺/Li**, **27 °C**, **CC 모드**(저자들이 *"in contrast to the **CC-CV** mode used in other ASSLIBs studies"* 라고 명시 — **정직한 조건 공개**).
- **1C = 200 mA g⁻¹**. 0.5C 시험은 **0.1C 10사이클 활성화 후** 시작.
- **액체 대조셀**: 85 wt% AM + 10 wt% Super P + 5 wt% **CMC**(수계 바인더), Al 집전체, Li 금속 상대극, **1 M `LiPF₆` in EC:DMC:DEC 1:1:1**, 로딩 **2.30 ± 0.03 mg cm⁻²**, **2025 코인셀**, 2.0–4.8 V, 27 °C.

### 4c. 전도도 측정 — **혼합전도체를 두 셀로 가른다** (우리가 배울 설계)

| 대상 | 셀 | 방법 |
|---|---|---|
| `LPSCl` **σ_ion** | `SS / LPSCl / SS` (510 MPa, Ø10 mm) | EIS **1 MHz–10 Hz**, **0→60 °C** 7점 → Arrhenius |
| `LPSCl` **σ_e** | 같은 셀 | **DC 분극 1 V** |
| 양극 **σ_e** | **이온차단셀** `SS / cathode / SS` (200 mg, 510 MPa, t = 1 mm) | **선형주사 0→1 V** → Ohm 법칙 **+ EIS 저주파 극한** → **두 값을 대조해 검증** |
| 양극 **σ_ion** | **전자차단셀** `Li-In / LPSCl / sample / LPSCl / Li-In` (5층) | **DC 분극**, 정상전류로 산출 |

⭐ **설계 포인트**: `LPSCl` 층을 **전자 차단막**으로 써서 혼합전도체의 이온 성분만 뽑는다. 그리고 σ_e 를 **두 독립 방법(LSV + EIS)으로 교차검증**한다 — *"The electronic conductivities obtained from linear scanning and EIS are **almost identical**"* (`Fig. S4`, `Fig. S6` 캡션).

### 4d. 분석

- **XRD**: Rigaku MiniFlex 600, Cu Kα, **40 kV / 15 mA**, 2θ **10–90°**, **1° min⁻¹**. `C2/m` 분율 = **GSAS Rietveld 정련**.
- **SEM** SU8010 · **HRTEM+EDS** FEI/Talos F200X · **HAADF-STEM + EELS** JEM-ARM200F (구면수차보정, USTC).
- **XPS** Thermo ESCALAB 250Xi, Al Kα **1486.6 eV**, **자체제작 무대기 이송장치**.
- ⛔ **미기재**: XPS 보정기준(C 1s?)·피팅 소프트웨어·구속조건(doublet Δ, FWHM) · EIS 피팅 소프트웨어 · 스퍼터 여부 · **반복 셀 수(n)** · 오차막대 — **논문 전체에 오차막대가 하나도 없다**.

### 4e. 이론 — **없다**

이 논문에는 **자체 DFT·MD·NEB·상평형 계산이 0건**이다. 계산은 **인용 2건**뿐:
- **ref 17 = Zhu, He, Mo (2015) *ACS AMI* 7, 23685** — *"Origin of Outstanding Stability in the Lithium Solid Electrolyte Materials: Insights from Thermodynamic Analyses Based on First-Principles Calculations"* ⭐ **= 우리 grand-potential ESW 계보의 직계 조상**(우리 litdb `[Zhu15]`).
- **ref 18 = Schwietert et al. (2020) *Nat. Mater.* 19, 428** — *"Clarifying the Relationship between Redox Activity and Electrochemical Stability in Solid Electrolytes"* ⇒ `PS₄³⁻ → −S⁰− + P₂S₇⁴⁻` 반응식의 출처.

⇒ **"above 2.5 V" 라는 문장의 계산 근거는 이 논문이 아니라 `[Zhu15]` 다.** 즉 이 논문의 CV 2.5 V 와 `[Zhu15]` 계열 계산창은 **독립이 아니다 — 저자들이 계산값을 먼저 알고 그 근처를 확인한 구조**다. 축 B① 데이터점으로 셀 때 이 점을 명시해야 한다(§7b-1 주의).

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 Co 스캔 — *"전도도를 올려야 전고체에서 산다"* (`Fig. 1`)

- Co 를 늘리면 20–24° 초격자 hump 가 약해지고(`Fig. 1a` 우측 확대) `C2/m` 분율이 줄며 σ_e·σ_ion 이 **각각 ≈5 자릿수** 오른다(`Fig. 1b`).
- `LRCo0` 은 σ 가 너무 낮아 **4.5 V 산소 redox 평탄부가 거의 안 나타나고** 방전이 **130 mAh g⁻¹** 에 그친다 — **같은 물질이 액체셀에선 274 mAh g⁻¹**(`Fig. S5b`). ⇒ **전고체에서의 손실은 물질이 아니라 수송이 원인**이라는 직접 증거.
- ⚠ **반전 1**: 액체셀에서는 Co 를 늘리면 **용량·수명이 나빠진다**(`Fig. S5`, ref 30·31 과 일치). **전고체에서는 반대다.** 저자들: *"the cathodes with increased Co content exhibit higher discharge capacities and capacity retention than those of `LRCo0` **in ASSLIBs**"*.
  ⇒ **같은 도펀트가 매질에 따라 부호가 뒤집힌다** — 우리 Cl-rich / Nd 도핑 서사에도 그대로 적용되는 경고다(§8-4).
- ⚠ **반전 2**: 그럼에도 **σ 최고인 `LRCo33` 이 아니라 `LRCo10` 이 최적**이다. 전도도는 필요조건이지 충분조건이 아니다.

### 5.2 `LiNiO₂` 성분 — *"표면에 스피넬을 깔아 전자·이온을 동시에 연다"* (`Fig. 2a–d`)

- 벌크는 전부 같은 **α-`NaFeO₂` 층상**(`Fig. 2a`)인데 **표면만 달라진다**: `LRCo10` 은 표면까지 층상(`Fig. 2b`), `@10LN` 은 표면에 **스피넬형**(`Fig. 2c`, 🔎 `Fd-3m [111]` / 벌크 `C2/m [103]`).
- σ_e 7.36×10⁻⁵ S cm⁻¹ = `LRCo0` 의 **4 자릿수 위**, *"NCM 수준"*.
- ⭐ **우리 관점**: 이건 *"양극 표면에 전자·이온 둘 다 통하는 상을 in-situ 로 만든다"* 는 전략이고, **우리 §D 의 "SE 안에 Nd 를 넣어 in-situ 로 인산염 싱크를 만든다"** 와 **문법이 같다**(레버 위치만 양극 ↔ 전해질). 경쟁이 아니라 **짝**이다.

### 5.3 셀 성능 — 왜 `@5LN` 과 `@10LN` 이 갈리나 (`Fig. 2e–h`)

- `@5LN` = **용량 챔피언**(244.5, 853 Wh kg⁻¹) · `@10LN` = **수명 챔피언**(1000사이클 83 %).
- `LiNiO₂` 성분이 늘수록 초기용량↓·수명↑ — 저자들 설명: **전도도 상승 + 스피넬/층상 이종구조**.
- 🔎 `Fig. 2f` figure-read: `@10LN` 은 100사이클 동안 **≈160 → ≈210 mAh g⁻¹ 로 *오른다*** (활성화). ⇒ `Table S1` 의 *"100 % 유지"* 는 **1사이클 기준 정규화**의 결과이지 감쇠가 0이라는 뜻이 아니다(§10-10).
- 🔎 `Fig. 2g` figure-read (0.5C 700사이클): `LRCo10` ≈130→≈33 · `@3LN` ≈185→≈105 · `@5LN` ≈200→≈122 · `@7LN` ≈172→≈118 · `@10LN` ≈152→≈143.

### 5.4 ⭐⭐ CV — 이 논문의 중심 주장 (`Fig. 3a,b`)

**주장**: 2.0–4.8 V 에서는 산화(≈2.5 V 개시)와 환원(≈2.3 V 개시)이 **둘 다** 나오고, 2.5–4.8 V 에서는 **산화만** 나온다. ⇒ **방전하한이 2.3 V 아래로 내려가야 `−S⁰−` 가 회수된다.**

**따라 붙는 논증**: *"the discharge cutoff voltages of the LCO and NCM cathodes are **generally above 2.5 V**. Therefore, the `−S⁰−` species in LCO- or NCM-based ASSLIBs **cannot be reduced**, and there is always a strong `−S⁰−` peak in the S 2p XPS spectra of cycled LCO or NCM in ASSLIBs (ref 37–40)"* — 여기서 드는 4개 ref 는 전부 **Janek/Zeier·Jung·Sun 그룹의 XPS/ToF-SIMS 실측**이라 논증이 단단하다.

**⛔ 그러나 약한 고리 두 개**:
1. `Fig. 3b` 의 **y축이 0 에서 시작**한다(§3d).
2. LCO 대조(`Fig. S8`)는 하한을 내리는 것이 **LCO 에겐 해롭다**는 결과를 준다 — 즉 *"2.0 V 가 좋다"* 는 **LMRO 에서만** 성립하는 조건부 주장인데, 그 조건부성을 직접 시험하는 실험(LMRO 를 2.5 V 하한으로 돌리기)이 없다(§10-5).

### 5.5 ⭐⭐⭐ XPS — 가역 채널과 비가역 채널이 갈린다 (`Fig. 3c,d`)

저자들의 서사는 **한 채널**이다: `PS₄³⁻` —(충전)→ `P₂S₇⁴⁻` + `−S⁰−` —(방전)→ `PS₄³⁻`·`P₂S₇⁴⁻`.

**그림을 실제로 보면 채널이 둘이다**:

| 채널 | 종 | 1사이클 | 1000사이클 | 가역? |
|---|---|---|---|---|
| **황 채널** | `−S⁰−` 163.6 eV | 충전 생성 → **방전 완전 소멸** | **없음** | ✅ **가역** |
| **골격 재편** | `P₂S₇⁴⁻` 163.0 / 132.5 eV | 조립 단계부터 존재, 충전에 증가 | 🔎 **`PS₄³⁻` 보다 커진다** | ⚠ **비가역(누적)** — 단 저자 말대로 `Li₇P₃S₁₁` 성분이라 Li⁺ 전도에 해롭진 않다 |
| **산소화 채널** | `PSₓOᵧ³⁻` 133.9 eV · `SO₃²⁻` 168.5 eV | 충전 생성 → 방전에 **부분만** 감소 | 🔎🔎 **`PSₓOᵧ³⁻` 가 P 2p 주성분** · **`SO₃²⁻` 신규 출현** | 🔴 **비가역, 그리고 자란다** |

⭐ **이게 이 논문에서 우리가 얻는 제일 값진 것이다**: 산소는 **SE 안에 없다**. `LiNbO₃`(NbO₃⁻) 와 **LMRO 격자산소**뿐이다. ⇒ **양극의 O 가 SE 의 P·S 로 넘어가 산화물계 음이온을 만든다** = **우리 `interface_reactivity` 가 모델링하는 바로 그 반응**(§7b-3). 그리고 `R_cathode` 가 1000사이클에 걸쳐 **6.7 배**로 자라는 것(§3f)과 **같은 채널**로 읽힌다.

### 5.6 구조·조성 무결성 (`Fig. 4`, `Fig. S11`, `Fig. S12`)

전고체셀의 이득 3종(§3h, §3i) + 기계적 근거: *"owing to the **lower Young's modulus (≈20 GPa)** of the sulfide electrolyte as compared to those of oxide materials (**100–200 GPa**)(ref 46), the sulfide electrolyte is capable of accommodating **volume expansion (≈2 %)** of the LMRO (ref 12, 47) during cycling. There are **no cracks** appearing after 1000 cycles"* (`Fig. S11`).

⚠ **ref 46 = McGrogan et al. 2017 *Adv. Energy Mater.* 7, 1602011** — *"Compliant Yet Brittle Mechanical Behavior of `Li₂S−P₂S₅` Lithium-Ion-Conducting Solid Electrolyte"*. ⇒ **≈20 GPa 의 출처는 `Li₂S–P₂S₅` *유리*의 나노인덴테이션이고, `Li₆PS₅Cl` 도 DFT 도 아니다**(§7c).

---

## 6. 메커니즘 종합 — 저자들이 그린 그림

```
충전 (→4.8 V)
  LMRO:  Li 탈리 (양이온 redox <4.4 V)  +  산소 음이온 redox (4.4–4.6 V 평탄부)
  LPSCl: PS₄³⁻  --(≈2.5 V 위)-->  P₂S₇⁴⁻  +  −S⁰−        [CV Fig. 3a · XPS Fig. 3c,d]
         P       --(양극의 O 유입)-->  PSₓOᵧ³⁻              [XPS Fig. 3d — 저자 서사 밖]
  ⇒ R_cathode 78 → 231 Ω                                  [EIS Fig. S10b]

방전 (→2.0 V)
  LMRO:  Li 재삽입
  LPSCl: −S⁰−  --(≈2.3 V 아래)-->  S²⁻                      [CV Fig. 3a · XPS Fig. 3c]
  ⇒ R_cathode 231 → 40 Ω  (원상보다 아래)                   [EIS Fig. S10b]

1000 사이클 후
  ✅ −S⁰− 없음 · LPSCl 이 여전히 양극을 덮고 있음 · 균열 없음 · 산소방출 4 nm
  🔴 그러나 PSₓOᵧ³⁻ 가 P 주성분 · SO₃²⁻ 신규 · R_cathode 39 → 262 Ω (6.7×)
```

**한 문장**: 저자들의 기전은 *"방전창이 SE 의 산화산물을 회수한다"* 이고 **황 채널에서는 실제로 그렇다**. 다만 **산소가 개입한 채널은 회수되지 않고, 그 채널이 계면저항 상승의 주범으로 보인다** — 논문은 이 두 번째 채널을 서술하지 않는다.

---

## 7. 우리 DFT 와의 대조 ★★ (`../our_dft_baseline.md`, `db/properties/`)

> ⛔ **대전제**: 이 논문은 **실험이고 자체 계산이 0건**이다. 우리 절대값과 **같은 표에 놓을 수 있는 칸이 거의 없다**. 아래는 **되는 곳 / 안 되는 곳**을 먼저 가른 표다.

### 7a. 🔴 **안 되는 곳** — 수치로 맞대면 안 되는 4칸

| 항목 | 이 논문 | 우리 | 왜 안 되나 |
|---|---|---|---|
| **σ(Li₆PS₅Cl)** | **4.73 mS cm⁻¹** (27 °C, EIS, 510 MPa 냉간압축 펠릿, SS 차단전극) | MLIP-MD Nernst–Einstein σ (**절대값 인용 금지** — CLAUDE.md §MLIP-MD) | **총전도도(입계 포함) vs 단결정 tracer**. 게다가 우리 규율이 σ 절대값 인용을 금한다 |
| **Ea** | **0.335 eV** (Arrhenius, 0–60 °C 7점, 펠릿) | comp1 **0.253** / modelc **0.224 eV** (UMA-s-1p1 MLIP-MD, 600/800/1000 K, MSD 2–50 ps, **단일궤적**) | **다른 양이다.** 실험 Ea 는 입계 저항을 포함해 **체계적으로 높다**. 온도창도 300–333 K vs 600–1000 K 로 겹치지 않는다. ⇒ *"0.335 vs 0.253 = 불일치"* 로 읽으면 틀린다 |
| **영률** | **≈20 GPa** (ref 46 McGrogan 2017, `Li₂S–P₂S₅` **유리**, 나노인덴테이션) | `E_VRH` comp1 **22.06** / modelc **27.66 GPa** (DFT 탄성 C_ij, relaxed-ion, VRH) | **다른 물질 + 다른 방법.** 값이 우연히 가깝다 ⇒ **우연 일치는 면제가 아니라 부인 선언 대상**(`[Wang26LRM]` 에서 이미 같은 함정을 등록했다 — 출처만 바뀌고 숫자는 같다) |
| **계면저항** | `R_cathode` 39 → 262 Ω | 없음 (우리는 Ω 축이 없다) | **면적 정규화 없음**. 우리 축에 대응물도 없다 |

### 7b. 🟢 **되는 곳** — 축 B 에서 실제로 맞물리는 3가지

#### 7b-1. ⭐⭐⭐ **우리 산화 onset 2.256 V 가 저쪽 실험의 갈림선을 *괄호로 감싼다***

**사실관계**

| | |
|---|---|
| **우리** (`our_dft_baseline.md`) | 산화 onset **2.256 V** (grand-potential, LiS₄·SCl₃·Li₅PS₄Cl₂ 제외 = GG set). 반응식 `Li₆PS₅Cl → Li₃PS₄ + LiCl + **S** + 2 Li⁺ + 2 e⁻`. modelc 도 **동일 2.256 V** (S²⁻-limited) |
| **이 논문** | 방전하한 **2.5 V** → 환원 피크 **없다** (`Fig. 3b`) · 방전하한 **2.0 V** → 환원 피크 **있다**, 개시 **≈2.3 V** (`Fig. 3a`) |

**⇒ 판정**: `2.0 V (된다) < **2.256 V (우리 onset)** < 2.5 V (안 된다)`.
우리 열역학 onset 은 **"S 가 안정한 전압"과 "S²⁻ 가 안정한 전압"의 경계**다. 하한이 그 경계를 **넘어가야만** 원소 S 가 다시 S²⁻ 로 환원될 수 있다. 저쪽 실험이 찾아낸 갈림선이 **정확히 우리 경계를 사이에 두고 있다**.

**왜 이게 값진가**: 이 검증은 **절대값 일치를 요구하지 않는다.** 필요한 것은 `2.0 < 2.256 < 2.5` 라는 **부등식 두 개**뿐이다. 우리가 PBE·hull 세대·상 제외 정책 때문에 절대값을 방어하기 어려운 상황에서, **부등식만으로 성립하는 검증**은 드물고 강하다.

**⚠ 이 주장에 붙일 단서 4개** (빼면 과주장이 된다):
1. **산화 개시(≈2.5 V)와 환원 개시(≈2.3 V)는 비대칭**이다. 우리 2.256 V 는 **환원 쪽(2.3 V)에 훨씬 가깝다**(차 0.044 V) — 그럴 만하다: 양극(산화) 방향은 **핵생성 과전압**을 치르지만, 이미 생긴 S 를 되돌리는 음극 방향은 그 장벽이 없다. ⇒ *"우리 2.256 V 는 CV 이력곡선의 **음극 가지 바로 아래**에 앉는다"* 가 제일 정확한 표현이다.
2. 저자들의 *"above 2.5 V"* 는 **`[Zhu15]` 계산에서 온 기대값**이다(§4e) — **독립 관측이 아니다**. 축 B① 데이터점으로 셀 때 *"계산을 알고 확인한 값"* 이라고 적는다.
3. **IR 보정·기준전극 오프셋 검증이 없다.** In/InLi → Li⁺/Li 변환은 **+0.62 V 일정**으로 가정됐다.
4. 우리 2.256 V 는 **LiS₄ 제외 phase set** 값이다. 포함하면 **2.14 V** 이고, 그래도 `2.0 < 2.14 < 2.5` 는 유지된다 ⇒ **괄호 판정은 phase set 선택에 robust 하다**. (이 robustness 를 명시하면 §H 의 "phase set 임의성" 비판을 이 건에 한해 무력화할 수 있다.)

#### 7b-2. ⭐⭐ **4.8 V 충전 산물이 우리 고전압 자기분해식과 겹친다**

| 우리 `cei_interface_V_2026_09_19.json` (`LiMnO₂` 계열, 끝점 퇴화 칸) | 이 논문 XPS (`Fig. 3c,d`, 4.8 V 충전) |
|---|---|
| **4.00 V**: `Li₆PS₅Cl → 6 Li + 0.5 **P₂S₇** + **SCl** + 0.5 **S**` | **`P₂S₇⁴⁻`** 163.0 / 132.5 eV ✅ · **`−S⁰−`** 163.6 eV ✅ |
| **4.50 V**: `Li₆PS₅Cl → 6 Li + **SCl** + 0.5 **P₂S₇** + 0.5 **S**` | 동일 ✅ |

⇒ **우리가 4.0–4.5 V 에서 예측하는 SE 자기분해 산물 3종 중 2종(`P₂S₇`·원소 `S`)이 4.8 V 실측 XPS 에 그대로 있다.** 결합에너지 귀속도 저자들이 **`Li₇P₃S₁₁`(=`P₂S₇⁴⁻` 함유 초이온전도체) 문헌**(ref 43 Busche 2016)으로 붙였다.
⛔ **`SCl` 은 확인 못 한다** — 이 논문은 **Cl 2p 스펙트럼을 안 찍었다**. 우리 census 에서 `SCl` 이 **98회**로 2위인 것을 감안하면 이건 **우리 쪽 미검증 항목**으로 남는다(§9-후속).
⚠ 우리 4.0/4.5 V 칸은 **`endpoint_degenerate`**(양극이 계산에 안 들어간 SE 자체분해)라, 이 대조는 **"복합양극 계면"이 아니라 "SE 자기분해"** 축의 대조다. 축 이름을 반드시 붙인다.

#### 7b-3. ⭐⭐ **산소화 산물 — 우리 census 의 *같은 사다리, 다른 칸***

| 우리 `product_census`(4 양극 × 6 전압 전수, 등장횟수) | 이 논문이 실제로 본 것 |
|---|---|
| **`Li₂SO₄` 109** (1위) · `SCl` 98 · `CoS₂` 95 · **`LiCl` 88** · `NiS₂` 78 · `Ni(PO₃)₂` 60 · `SO₂` 54 · **`NdPO₄` 48** · **`MnS₂` 46** · **`Mn(PO₃)₂` 45** · **`S` 42** · **`Li₃PO₄` 41** · `Li₄P₂O₇` 30 · `NdP₅O₁₄` 32 · `LiMnPO₄` … (고유 36종) | **`SO₃²⁻`** 168.5 eV (**황 + 산소, 아황산**) · **`PSₓOᵧ³⁻`** 133.9 eV (**인 + 황 + 산소**) · `−S⁰−` · `P₂S₇⁴⁻` |
| `LiMnO₂@2.5 V / comp1` 반응식: `0.7059 LiMnO₂ + 0.2941 Li₆PS₅Cl → 1.176 Li + 0.2941 **Li₃PO₄** + 0.0588 **Li₂SO₄** + 0.7059 **MnS₂** + 0.2941 **LiCl**` (**E_rxn = −0.4903 eV/atom**) | — |

**⇒ 판정**: **같은 산화 사다리의 서로 다른 칸이다.**
· 우리 0 K hull 은 **끝점**을 준다 — S 는 끝까지 산화돼 `SO₄²⁻`(S⁶⁺), P 는 `PO₄³⁻`(P⁵⁺).
· 27 °C 에서 1000사이클 돈 실험은 **중간 칸에서 멈춘다** — `SO₃²⁻`(S⁴⁺), `PSₓOᵧ³⁻`(S 가 아직 남은 부분산화 P).
· **방향이 같고 원소 조합이 같다** (S+O, P+O+S). **속도론이 끝점 도달을 막고 있을 뿐.**
· ⭐ 이건 우리 계산의 **약점이 아니라 정확히 알려진 경계**다 — `[Xiao20Rev]` 가 우리 grand-potential 을 *"**worst-case scenario** (no kinetic stabilization)"* 로 정의해 둔 것과 같은 말이다. **실험이 그 worst case 로 가는 길목에서 멈춘 모습을 처음으로 우리 계(`Li₆PS₅Cl` + Mn 계 양극)에서 찍어 준다.**

⛔ **단 하나 꼬인 점**: 우리 census 의 `Li₂SO₄`·`Li₃PO₄` 는 **양극 O 를 반응물로 쓴** `interface_reactivity` 산물이고, 이 논문의 산소원은 **LMRO + `LiNbO₃` 둘 다**다. `LiNbO₃` 는 우리 계산에 없다 ⇒ **산소 출처를 하나로 못 좁힌다.** 인용할 때 *"양극계 산소"* 라고 뭉뚱그리고, `LiNbO₃` 기여를 배제했다고 쓰지 않는다.

### 7c. 🟡 축 C(기계) — **번호가 같아서 더 위험하다**

우리 `E_VRH` 22.06 / 27.66 GPa ↔ 이 논문의 *"sulfide ≈20 GPa"*. **이미 `[Wang26LRM]` 에서 같은 함정을 등록했고**(그쪽 출처는 중문 ref 99), 이번에 **출처가 하나 더 추적됐다**:
- **ref 46 = McGrogan, Swamy, Bishop, Eggleton, Porz, Chen, Chiang, Van Vliet (2017) *Adv. Energy Mater.* 7, 1602011**, `Li₂S−P₂S₅` **유리**, **나노인덴테이션**.
⇒ **"황화물 ≈20 GPa" 는 문헌에서 이 McGrogan 측정을 돌려 쓰는 관용구일 가능성이 높다.** 우리 값 옆에 놓지 않되, **출처를 이름으로 댈 수 있게 됐다** — 이게 이번 digest 의 부수 소득이다.
· 부피변화 **≈2 %**(LMRO, ref 12·47) 는 우리 EOS/탄성 축과 **연결점이 없다**(우리는 사이클 중 부피변화를 계산하지 않는다).

### 7d. 🟡 축 D(전자구조) — **우리에게 없는 양을 두 번째로 재 준다**

- 이 논문: **σ_e(`Li₆PS₅Cl`) = 4.11×10⁻⁹ S cm⁻¹** (DC 분극, 1 V, 32.3 nA).
- `[Deng26PS]`: bare LPSC **5.69×10⁻⁹ S cm⁻¹** (DC 분극, Al\|SE\|Al, 0.1–0.5 V 5점 선형).
⇒ **독립 두 그룹, 같은 자릿수** ⇒ *"`Li₆PS₅Cl` σ_e ≈ 4–6 ×10⁻⁹ S cm⁻¹"* 를 **문헌 앵커로 세울 수 있다**.
⛔ **우리는 σ_e 를 계산한 적이 없다.** 우리 축 D 는 **band gap**(comp1 2.066 / modelc 2.099 / +B₂O₃ 1.9671 / LPSOCl 2.2309 eV)뿐이고, gap 과 σ_e 는 다른 양이다(gap = 캐리어 생성 문턱, σ_e = 농도 × 이동도). ⇒ **§H 공백 유지**, 단 이제 **목표값이 둘 있다**.

### 7e. 🟢 축 A 의 *다른* 칸 — **공정이 σ 를 22배 깎는다**

| 등급 | σ (mS cm⁻¹) | Ea (eV) | 우리 대응 |
|---|---|---|---|
| `LPSCl` (소성 그대로) | 4.73 | 0.335 | — |
| `LPSCl-BM` (p-xylene 재분쇄) | **1.48** (**3.2×↓**) | 0.368 (**+0.033**) | — |
| `LPSCl-EtOH` (에탄올 용해·재석출) | **0.21** (**22×↓**) | 0.424 (**+0.089**) | — |

⇒ **우리 계산에는 이 축이 통째로 없다.** 우리는 완벽한 주기결정만 본다. 그런데 **이 논문의 복합양극 안에 실제로 들어간 SE 는 BM 등급(1.48)과 EtOH 등급(0.21)** 이다. ⇒ *"σ 가 4.73 mS cm⁻¹ 인 전해질로 만든 셀"* 이라고 읽으면 틀린다(§10-9).
⭐ **우리 §H(정직 목록)에 한 줄 추가할 값**: *"문헌은 같은 `Li₆PS₅Cl` 을 공정만 바꿔 Ea 를 0.335→0.424 eV 로 움직인다(+0.089 eV). 우리 comp1→modelc 조성차(0.253→0.224, −0.029 eV)보다 **3배 크다**"* ⇒ **조성 효과를 주장할 때 공정 효과가 그보다 크다는 것을 알고 있어야 한다.**

### 7f. 🔎 선행연구 점검 — **우리 §B·§D·§2b·§E 가 여기 있나**

| 우리 절 | 이 논문에 있나 | 판정 |
|---|---|---|
| **§B** MP hull grand-potential 계면 반응성, 4 양극(LCO·LNO·**LiMnO₂**·NMC811) × 6 전압 2.5–4.5 V | ❌ **계산 0건.** 상평형·hull·grand-potential 어느 것도 없다 | 🟢 **선점 없음.** 오히려 우리 §B 가 이 논문의 기전을 **설명하는 쪽**이다(§7b-1) |
| **§D** Nd 가 Li 를 안 쓰는 인산염 경로를 연다 | ❌ Nd·희토류 **0회 언급**. 도펀트는 양극 쪽 Co·Ni 뿐 | 🟢 **선점 없음.** 단 *"P 가 S 보다 더 산화된다"*(`PSₓOᵧ³⁻`)는 **§D 전제의 실험 근거**로 쓸 수 있다 |
| **§2b** 보호율 `min(1, k·x/(1−x))` | ❌ 없음 | 🟢 **선점 없음** |
| **§E** 환원/음극(Li 금속) | ⚠ 음극이 **Li–In** 이고, `R_anode` 가 1000사이클 평평하다는 것만 | 🟡 **무관** — Li 금속 계면 축이 아니다 |
| **축 B 실험 무대 전체** | ✅ **여기가 강하다** — `Li₆PS₅Cl` × 고전압 산화물 × 1000사이클 × XPS/EIS/STEM/EELS | 🔴 **우리가 "황화물 SE 로 고전압 양극 장수명"을 말할 때, 이 논문이 실험 쪽 현직 챔피언**(83 %/1000 cyc)이다. **반드시 인용해야 하고, 우리 주장은 "이미 된 것"이 아니라 "다른 레버"로 서술해야 한다**(§8-3) |

---

## 8. 적용 인사이트 — 우리 연구에 어떻게 ★

1. ⭐⭐⭐ **§B 의 전압 사다리에 `2.0 V` 와 `4.8 V` 를 추가한다.**
   현재 우리 `cei_interface_V_*.json` 는 **`[2.5, 3.0, 3.5, 4.0, 4.3, 4.5]`** 여섯 칸이다.
   · **아래로 2.0 V**: 이 논문의 기전이 사는 칸이다. 2.0 V 는 우리 onset 2.256 V **아래**라 원소 S 가 불안정해야 하고, 그게 저쪽 CV 환원 피크의 열역학적 근거다. **계산 한 칸 추가로 §7b-1 의 괄호 판정이 그림으로 선다.**
   · **위로 4.8 V**: LMR 양극의 실제 상한이고, 4.6–4.8 V 는 LMRO·고전압 스피넬이 모두 쓰는 창이다. 지금 우리 상한 4.5 V 는 **LMR 계 논문과 겹치지 않는다**.
   · 비용은 거의 0이다(같은 스크립트에 전압 2개 추가).

2. ⭐⭐ **축 B① 의 "kinetic overshoot" 표에 *환원 가지*를 새로 만든다.**
   지금 우리 표는 **산화 개시**만 모은다([LiGaF] 2.5 · [Qian26] 2.5 · [Zuo] 2.5–2.7 · [Cronk26] 2.70 · [Deng26PS] 2.85–2.9 · [Ling26] ≈3.05 · **이 논문 ≈2.5**).
   이 논문은 **환원 개시 ≈2.3 V** 를 준다 — 우리 2.256 V 와 **0.044 V** 차. ⇒ *"열역학 onset 은 CV 이력곡선의 **음극 가지**에 붙고, 양극 가지와의 0.25–0.8 V 격차가 핵생성 과전압이다"* 라는 **정량적 프레임**을 처음 세울 수 있다. 우리 §H 의 "운동학 여유" 서술이 **한 단계 구체화**된다.

3. ⭐⭐ **우리 주장을 "경쟁"이 아니라 "직교하는 두 번째 레버"로 다시 쓴다.**
   이 논문의 처방 = **셀 운용창을 산물 회수가 가능한 곳에 둔다**(하한 2.0 V) + **버퍼층**(`LiNbO₃` 1–2 nm) + **양극 표면 스피넬**.
   우리 처방 = **SE 조성(Nd, +O)으로 분해 구동력 자체를 낮춘다**.
   ⇒ 원고 문장은 *"선행연구는 운용창과 버퍼층으로 계면을 살렸다(Du 2022, 1000사이클 83 %). 그러나 그 셀에서도 **양극 계면 저항은 6.7배 오르고 산소화 인·황 종이 누적된다**(같은 논문 `Fig. 3d`, `Fig. S10d`). 우리는 그 잔여 구동력을 SE 조성으로 줄이는 축을 본다"* 가 **정직하고 강하다**.
   ⛔ *"아무도 못 했다"* 는 못 쓴다.

4. ⭐ **"같은 도펀트가 매질에 따라 부호를 뒤집는다"를 우리 규율에 넣는다.**
   `Fig. 1d` vs `Fig. S5c,d`: **Co 증량은 액체셀에서 나쁘고 전고체에서 좋다.** 이유는 화학이 아니라 **수송 병목의 위치가 다르기 때문**이다.
   ⇒ 우리가 Cl-rich·Nd 도핑의 이득을 말할 때, **어느 무대(벌크 수송 / 계면 열역학 / 셀 수준)에서의 이득인지 명시**하지 않으면 같은 종류의 뒤집힘을 맞는다. `[Liang26IF]` 의 *"도핑이 σ 를 낮출 수 있다"* 와 같은 결의 경고다.

5. ⭐ **공정 축의 눈금을 얻었다** — Ea 를 **0.089 eV** 움직이는 공정 변수(에탄올 재석출)가 실재한다. 우리 조성 효과(comp1→modelc, **−0.029 eV**)의 **3배**다. ⇒ §H 에 *"우리 Ea 차는 문헌의 공정 편차보다 작다"* 를 적어 두면, 나중에 실험팀과 대조할 때 **우리가 먼저 말한 것**이 된다.

6. ⭐ **`SCl` 이 여전히 미검증이다.** 우리 census 2위(98회)인데, 이 논문은 **Cl 2p 를 안 찍었다**. `[Zuo]`·`[Deng26PS]` 도 S 2p/P 2p 중심이다. ⇒ **"Cl 함유 산화산물의 XPS/ToF-SIMS 증거"** 를 명시적으로 찾는 과제를 §9 후속에 올린다. (없다면 그것대로 §10 에 적을 우리 계산의 열린 항목이다.)

---

## 9. 인용 가능 문장 (deck / 원고용 영문 초안)

- "Du *et al.* showed that `Li₆PS₅Cl` oxidised from ≈2.5 V and that the resulting `−S⁰−` species were re-reduced only when the discharge cut-off was lowered to 2.0 V; no cathodic feature appeared for a 2.5–4.8 V window." *(CV, 0.1 mV s⁻¹, LPSCl+VGCF composite vs In–Li, 27 °C)*
- "Our computed 0 K grand-potential oxidation onset for `Li₆PS₅Cl` (2.256 V vs Li⁺/Li) lies **between** the two experimental cut-offs that Du *et al.* found to work (2.0 V) and to fail (2.5 V), consistent with elemental sulfur being thermodynamically re-reducible only below that onset."
  ⚠ 반드시 같이 쓸 단서: *worst-case, no kinetic stabilisation (`[Xiao20Rev]`)*; LiS₄ 포함 시 2.14 V 이나 **부등식은 유지**된다.
- "XPS after 1000 cycles shows that the polysulfide channel is reversible (`−S⁰−` absent) while oxygen-bearing species accumulate — `PSₓOᵧ³⁻` (133.9 eV) becomes the dominant P environment and a new `SO₃²⁻` component appears at 168.5 eV — in a cell whose cathode-side interfacial resistance grows 6.7-fold (39 → 262 Ω)." *(figure-read from `Fig. 3c,d` and `Fig. S10d`; the authors do not discuss these components.)*
- "The oxidation products predicted for `Li₆PS₅Cl` at 4.0–4.5 V (`P₂S₇`, elemental `S`) are both observed by XPS after charging to 4.8 V."
- "Reported `Li₆PS₅Cl` electronic conductivities cluster at 4–6 × 10⁻⁹ S cm⁻¹ (4.11 × 10⁻⁹, Du 2022; 5.69 × 10⁻⁹, Deng 2026)."

---

## 10. 비판 — 이 논문의 약한 곳 ★

**1. ⭐⭐ "가역"이 과주장이다 — 저자들 자신의 `Fig. S9` 가 반증한다.**
🔎 figure-read: `(LPSCl+VGCF)` 셀의 **1사이클 충전 ≈11.5 mAh g⁻¹ vs 방전 ≈3.0 mAh g⁻¹** ⇒ **SE 산화환원의 1사이클 쿨롱효율 ≈26 %**. 본문은 **방전값 3 만 쓰고 충전값 11.5 는 쓰지 않는다.** 게다가 가역용량은 **20사이클쯤에 ≈0.2 mAh g⁻¹ 로 정착**한다. ⇒ 정확한 서술은 *"가역이다"* 가 아니라 **"1사이클에 대부분 일어나고, 곧 부동태화되어 작아지는 부분가역 과정"** 이다.

**2. ⭐⭐⭐ 본문이 자기 그림의 비가역 성분을 서술하지 않는다.**
`Fig. 3c` 1000사이클 패널에 **`SO₃²⁻` 168.5 eV** 가 뚜렷하고, `Fig. 3d` 1000사이클 패널은 **`PSₓOᵧ³⁻` 133.9 eV 가 주성분**이다. 본문은 S 2p 에 대해 *"main peaks … still `PS₄³⁻` and `P₂S₇⁴⁻`, `−S⁰−` does not emerge"* 라고만 쓰고 **168.5 eV 를 언급하지 않으며**, P 2p 의 1000사이클 상태는 **아예 서술하지 않는다**. ⇒ **가역 채널(황)만 이야기하고 비가역 채널(산소화)은 그림에 두고 지나간다.** 우리 §B 관점에서는 후자가 더 중요하다.

**3. ⭐⭐ `R_cathode` 상승을 "only" 로 표현한다.**
39 → 262 Ω = **6.7 배**. 🔎 figure-read 로 보면 증가가 **300→700사이클(≈101→≈250 Ω)에 집중**돼 있다 — 선형이 아니고, 그 구간에 무언가 임계가 있다. `R_SE`·`R_anode` 는 평평하다 ⇒ **전 열화가 양극 계면 한 곳**인데, 본문은 액체셀(1989 Ω)과 비교해 *"much smaller"* 로 넘어간다.

**4. ⭐⭐ 맨 계면 대조군이 없다.**
모든 양극이 **`LiNbO₃` 2 wt%(1–2 nm) + `LPSCl-EtOH` 15 wt%** 이중코팅이다. 즉 실제 접촉은 `LMRO / LiNbO₃ / LPSCl-EtOH / LPSCl-BM` 4층이다. ⇒ *"LMRO 와 황화물이 잘 맞는다"* 는 **한 번도 시험되지 않았다.** 우리 `interface_reactivity` comp1\|`LiMnO₂` **−0.4903 eV/atom (2.5 V)** 는 바로 그 **만들어진 적 없는 맨 계면**을 기술한다 ⇒ 두 값이 서로를 검증하지 못한다.

**5. ⭐⭐ 중심 주장의 결정적 대조실험이 빠졌다.**
필요한 실험은 **같은 LMRO ASSLIB 를 `2.5–4.8 V` 와 `2.0–4.8 V` 로 각각 사이클**하는 것이다. 안 했다. 대신 **LCO 를 2.0 vs 3.0 V 로** 돌렸는데(`Fig. S8`), 결과는 **낮은 하한이 더 나쁘다(63 % vs 72 %)**. 저자들은 이를 *"LCO 과리튬화"* 로 설명하지만, 그 설명이 맞다면 **LMRO 에서도 과리튬화가 있는지**를 따로 보여야 한다. ⇒ *"2.0 V 하한이 이득이다"* 는 **CV + XPS 의 간접 증거로만** 선다.

**6. ⭐ "83 % vs 36 %" 가 기준선이 다른 두 곡선의 비교다.**
🔎 `Fig. S7d` figure-read: 0.5C 초기용량이 **전고체 ≈157 · 액체 ≈205 mAh g⁻¹**. 1000사이클 뒤 **≈130 vs ≈75**. **절대값으로도 전고체가 이기지만**, 각자 100 % 로 정규화한 유지율은 **초기값이 낮은 쪽에 유리**하다.

**7. ⭐ `Table S1` 벤치마크가 전압창을 통제하지 않는다.**
본 연구만 창이 **2.0–4.8 V (2.8 V 폭)**, 대조군은 **1.3–1.9 V 폭**이다. 용량·에너지밀도 우위의 상당 부분이 **창 폭에서 온다**. ⇒ *"highest energy density and best cycling performance by far"* 는 **동일 조건 비교가 아니다**.

**8. ⭐ `Fig. 3b` 의 y축이 0 에서 시작한다.**
*"there are **no reduction peaks**"* 를 **음전류를 표시할 수 없는 축**에서 주장한다. 같은 그림의 (a) 는 −10 mA g⁻¹ 까지 그린다 ⇒ **일관성 문제**.

**9. ⭐ 헤드라인 σ 와 셀에 들어간 σ 가 다르다.**
초록·본문은 `LPSCl` **4.73 mS cm⁻¹** 을 앞세우지만, **복합양극 안의 SE 는 `LPSCl-BM`(1.48) 과 `LPSCl-EtOH`(0.21)** 이다. **22배 차**를 논문은 SI 에 성실히 적어 놓고 본문에서 연결하지 않는다. (EtOH 재석출이 결정성을 해쳤을 가능성은 `Fig. S1c` XRD 의 피크 약화·광폭화로도 보인다.)

**10. ⭐ "100 % 유지" 는 정규화 산물이다.**
`Table S1` 의 `@10LN` *"100 (0.1C 100 cycles)"* 은, `Fig. 2f` 에서 그 시료가 **≈160 → ≈210 mAh g⁻¹ 로 *올라간* 것**을 1사이클 기준으로 잰 값이다. **활성화 상승을 "감쇠 0"으로 읽게 만든다.** (`@5LN` 의 85 % 는 반대로 **최대값 기준**이라고 본문이 밝힌다 — **두 시료의 기준이 다르다**.)

**11. 에너지밀도 853 / 752 Wh kg⁻¹ 의 기준이 명시되지 않는다.** 활물질 기준으로 보이지만 본문·SI 어디에도 *"based on active material"* 문구가 없다. 셀 수준 값과 섞으면 5–10배 과대평가가 된다.

**12. n = 1, 오차막대 0.** 반복 셀 수·표준편차가 **논문 전체에 한 번도 없다**. 1000사이클 셀은 특히 셀간 편차가 큰 측정이다.

**13. `Fig. 4` 를 "반응 없음"의 증거로 배치한다.** HAADF-STEM 은 **~1 nm 비정질 산황화물층**을 비정질에 가까운 SE 배경에서 못 가른다. 같은 시료의 XPS 는 산화종이 있다고 말한다. 두 데이터가 모순은 아니지만, **`Fig. 4` 는 "계면상이 없다"를 보일 수 있는 측정이 아니다**.

**14. `Fig. S1c` 의 XRD 지시상이 `Li₇PS₆`(PDF#34-0688)** 이다. `Li₆PS₅Cl` 표준카드가 아니다 — 상순도 논거로는 약하다.

---

## 11. 우리 원장 매핑 (요약표)

| 우리 원장 | 이 논문이 주는 것 | 취급 |
|---|---|---|
| `our_dft_baseline.md` **산화 onset 2.256 V** | **괄호 검증** `2.0 < 2.256 < 2.5` (§7b-1) | 🟢 **축 B① 외부 검증 추가.** 단 **부등식 형태로만** |
| `our_dft_baseline.md` **Ea 0.253 / 0.224 eV** | 실험 **0.335 eV** (EIS 총전도) | 🔴 **다른 양.** 같은 표 금지 |
| `our_dft_baseline.md` **E_VRH 22.06 / 27.66 GPa** | *"sulfide ≈20 GPa"* (ref 46 McGrogan, `Li₂S–P₂S₅` 유리, 나노인덴테이션) | 🔴 **부인 선언 대상**(우연 근접). ⭐ 단 **출처 추적 완료** |
| `db/properties/cei_interface_V_2026_09_19.json` **전압 6칸** | 저쪽 창은 **2.0–4.8 V** | ⭕ **2.0 V·4.8 V 칸 추가 제안**(§8-1) |
| 같은 파일 **`product_census` 36종** | `SO₃²⁻`·`PSₓOᵧ³⁻` 실측 = **같은 사다리 중간 칸** (§7b-3) | 🟢 **방향 검증**. ⛔ 종 이름을 1:1 로 대응시키지 않는다 |
| 같은 파일 **4.0/4.5 V 자기분해식 `P₂S₇`+`SCl`+`S`** | `P₂S₇⁴⁻`·`−S⁰−` **실측 2/3 일치**, `SCl` 미확인 | 🟢 **2종 검증 + 1종 열린 항목** (§8-6) |
| `interface_reactivity` comp1\|`LiMnO₂` **−0.4903 eV/atom (2.5 V)** | **대응 실험 없음** — 맨 계면을 안 만들었다 | 🔴 **검증 불가.** §10-4 |
| **σ_e** | 4.11×10⁻⁹ S cm⁻¹ (+`[Deng26PS]` 5.69×10⁻⁹) | 🟡 **우리에게 없는 양** — §H 공백 유지, 목표값 2개 확보 |
| **§D Nd 인산염 경로** | Nd 언급 0 · 단 *"P 가 S 보다 더 산화된다"* 실측 | 🟢 **전제 지지** (선점 없음) |
| **§2b 보호율** | 없음 | 🟢 **선점 없음** |

---

## 12. 주의 / 한계 (인용 규율)

1. ⛔ **산화 onset 을 우리 2.256 V 와 같은 표·같은 열에 놓지 않는다.** 이 논문의 2.5 V 는 **CV kinetic onset**(0.1 mV s⁻¹, 탄소 10 wt% 복합체, In-Li 기준, IR 미보정)이고 우리 것은 **0 K grand-potential** 이다. §7b-1 의 **괄호 판정**은 두 값을 *비교*하지 않고 **부등식으로만** 쓰기 때문에 허용된다.
2. ⛔ **σ·Ea·용량·에너지밀도·저항 절대값 전부 소환값**이다. 우리 `db/properties/*` 와 같은 표에 넣지 않는다.
3. ⛔ **"LMRO 와 `Li₆PS₅Cl` 은 화학적으로 양립한다"로 읽지 않는다** — 맨 계면은 시험된 적이 없다(§10-4).
4. ⛔ **"황화물 ≈20 GPa"** 를 우리 `E_VRH` 옆에 두지 않는다. 다른 물질(유리)·다른 방법(나노인덴테이션).
5. ⚠ **figure-read 와 본문값을 섞지 않는다.** 이 digest 에서 `🔎 figure-read ≈` 로 표시한 값은 전부 **우리가 그림에서 읽은 것**이고 본문에 없다: `Fig. 1b`·`Fig. 2d` 의 σ/`C2/m` 막대, `Fig. 3a,b` 의 전류밀도·피크위치, `Fig. 3c,d` 의 **1000사이클 `SO₃²⁻`·`PSₓOᵧ³⁻` 주성분 판정**, `Fig. 4c` 의 58.52°, `Fig. S7d` 의 초기·최종 용량, `Fig. S9` 의 **충전 11.5 mAh g⁻¹ 과 0.2 mAh g⁻¹ 정착**, `Fig. S10b,d` 의 저항값 4개, `Fig. S12c,f` 의 Mn L₃/L₂ 값.
6. ⚠ **저자들의 "above 2.5 V" 는 `[Zhu15]` 계산에서 온 기대값이다** — 독립 관측으로 세지 않는다(§4e).
7. ⚠ **`[Wang26LRM]` 의 ref 93(3722 Ω)·ref 94(SO₄²⁻/SO₃²⁻/P₂Sₓ 비가역)는 이 논문이 아니다.** 여전히 원출처 미확보.
8. ⚠ **크로핑 도구가 `Fig. S7` 을 오탐 제외하고 `Fig. S10` 을 반만 잘랐다**(§0c). 이 digest 의 두 그림은 **사람이 다시 렌더한 것**이고 `figures.json` 에 그 사실을 기록했다.

---

## 13. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| **1a,b** | Co 0→0.33 의 XRD(20–24° 초격자 hump 감소)와 σ_e·σ_ion·`C2/m` wt% 막대 | `C2/m`(=`Li₂MnO₃`) 분율이 절연성을 지배한다는 정량. 🔎 figure-read σ 5 자릿수 상승, `C2/m` ≈43→≈24 wt% |
| **1c,d** | Co 계열 ASSLIB 1사이클(2.0–4.8 V, 0.1C)과 100사이클 | `LRCo0` 130 mAh g⁻¹(액체 274) = **전고체 손실이 물질이 아니라 수송**. σ 1등(`LRCo33`)이 성능 1등이 아니다 |
| **2a–c** | `LRCo10@yLN` XRD + HAADF-STEM 2장 | 🔎 `Fig. 2c` 에 벌크 `C2/m [103]` / 표면 **`Fd-3m [111]`** 공간군이 찍혀 있다(본문은 "spinel-like"만). 표면상 설계 = 우리 §D in-situ 싱크와 같은 문법 |
| **2d** | `@yLN` σ_e·σ_ion·`C2/m` 막대 | **`[Wang26LRM]` `Fig. 7c` 의 원본**. 리뷰 digest 의 figure-read 를 원문으로 검증 |
| **2e–h** | 1사이클·100사이클(0.1C)·700사이클(0.5C)·1000사이클 유지율+CE | 244.5 / 853 Wh kg⁻¹ / 83 % / CE 99.96 % 의 출처. 🔎 `@10LN` 이 100사이클 동안 **오르는** 것(→ §10-10) |
| **3a** | **CV 2.0–4.8 V, 4사이클** — 산화 ≈2.5 V, 환원 ≈2.3 V, 2–4사이클 축소·잔존 | ⭐⭐⭐ **§7b-1 괄호 판정의 근거.** 🔎 1사이클 피크 ≈3.5 V/≈3.8 mA g⁻¹, 2.0 V 에서 ≈−9.5 mA g⁻¹ |
| **3b** | **CV 2.5–4.8 V** — 환원 피크 없음 | ⭐⭐ 같은 판정의 음성 대조. ⚠ **y축이 0 에서 시작**한다(§10-8) |
| **3c** | **S 2p XPS 5단**: pristine → 복합양극 → 4.8 V → 2.0 V → 1000사이클 | ⭐⭐⭐ `−S⁰−` 163.6 eV 의 생성·완전소멸. 🔎🔎 **1000사이클 패널의 `SO₃²⁻` 168.5 eV 는 본문에 없다**(§10-2) |
| **3d** | **P 2p XPS 5단** | ⭐⭐⭐ **`PSₓOᵧ³⁻` 133.9 eV** = 양극 O 가 SE 의 P 로 넘어온 직접 증거. 🔎 1000사이클에 **주성분**. 우리 §D(P 가 O 싱크) 전제의 실험 근거 |
| **4a–c** | 액체셀 1000사이클 후 STEM + FFT | 나노보이드 + 스피넬 `Li_xMn₂O₄`. 🔎 FFT 끼인각 **58.52°** |
| **4d–h** | 전고체 1000사이클 후 계면·벌크 STEM | 계면 손상 ≈2 단위격자, 표면 6 nm 스피넬 보존. ⚠ **계면상 부재의 증거로는 못 쓴다**(§10-13) |
| **S1a–c** | LPSCl 3등급 SEM(30–50 / 2–5 μm) + XRD | ⚠ 지시상이 **`Li₇PS₆` PDF#34-0688**. 🔎 EtOH 등급 피크 약화·광폭화 |
| **S1d–g** | Nyquist(0–60 °C) + **Arrhenius 3계열** | ⭐⭐ 축 A 앵커: **4.73 / 1.48 / 0.21 mS cm⁻¹**, **Ea 0.335 / 0.368 / 0.424 eV** = **공정이 Ea 를 0.089 eV 움직인다**(§7e) |
| **S1h** | DC 분극 `SS/LPSCl/SS` 1 V | ⭐ **σ_e = 4.11×10⁻⁹ S cm⁻¹** (32.3 nA). `[Deng26PS]` 5.69×10⁻⁹ 와 같은 자릿수(§7d) |
| **S7a–d** | 액체 vs 전고체 4패널 | 🔎 **전고체는 0.5C 초기 ≈157, 액체 ≈205 mAh g⁻¹** ⇒ "83 % vs 36 %" 기준선 문제(§10-6). 🔎 **액체의 4.5 V 평탄부가 더 길다** = 전고체에서 산소 redox 활성화 부분억제 |
| **S8a,b** | LCO ASSLIB 방전하한 2.0 vs 3.0 V | ⭐ **하한을 내리면 LCO 는 나빠진다(63 % vs 72 %)** — 저자 주장의 조건부성(§10-5) |
| **S9a,b** | `(LPSCl+VGCF)` 자체 충방전 + 100사이클 | ⭐⭐ **§10-1 의 근거**. 🔎 **충전 ≈11.5 vs 방전 ≈3.0 mAh g⁻¹(CE ≈26 %)**, 20사이클에 **≈0.2 로 정착** |
| **S10a,b** | 1사이클 Nyquist + 등가회로 + R 분해 | ⭐⭐ 🔎 **`R_cathode` 78 → 231 → 40 Ω**. `R_SE`·`R_anode` 불변 = **열화가 양극 계면 한 곳** |
| **S10c,d** | 1000사이클 Nyquist + R 분해 | ⭐⭐ 🔎 **39 → ≈101 → ≈250 → 262 Ω (6.7×), 증가가 300–700사이클에 집중**(§10-3) |
| **S10e,f** | 액체 vs 전고체 1000사이클 | 1989 vs 262 Ω. ⛔ 면적 미정규화 |
| **S12a–h** | EELS 라인스캔 + Mn³⁺/Mn⁴⁺ 매핑 | 산소방출 **50 nm(액체) vs 4 nm(전고체)**. 🔎 Mn L₃/L₂ 표면 ≈2.8 vs ≈2.55, Mn⁴⁺ 회복 50–60 nm vs ≈6 nm |
| **Table S1** | 황화물 ASSLIB 고전압 양극 12행 벤치마크 | ⭐ **12개 대조군 중 방전하한 2.5 V 미만이 하나도 없다** = 저자 주장의 방증. ⛔ 창 폭이 달라 벤치마크로는 못 쓴다(§10-7) |

---

## 14. Post-processing / 도구 ★

- **Rietveld 정련 (GSAS)** → `C2/m` 상 wt% (`Fig. 1b`·`Fig. 2d` 의 보라 막대).
- **Arrhenius 회귀** σ(T), 0–60 °C 7점 → Ea (`Fig. S1g`).
- **EIS 등가회로 피팅**: `R_SE` + (`R_anode`‖CPE1) + (`R_cathode`‖CPE2) + CPE3 (`Fig. S10a`) — ⛔ 소프트웨어·χ² 미기재.
- **Ohm 법칙 × 2 경로 교차검증**: 선형주사(0–1 V) 기울기 ↔ EIS 저주파 극한 — *"almost identical"*.
- **DC 분극 정상전류** → σ_e(SE) 및 σ_ion(양극, 전자차단셀).
- **XPS 피크 분해** S 2p / P 2p (doublet) — ⛔ 보정기준·구속조건·소프트웨어 미기재.
- **FFT / FFT 필터링** (HAADF-STEM) → 상 동정 + 면간각 (`Fig. 4b,c,f,h`).
- **EELS 백선비** Mn L₃/L₂ → Mn 가수; **O K-edge pre-peak 강도** → 격자산소 (`Fig. S12`).
- ⛔ **없는 것**: DFT · MD · NEB · Bader · COHP/ICOHP · DOS/PDOS · ELF · BVSE · grand-potential · phonon · 탄성 C_ij — **전부 0건**.

---

## 15. 기법 용어 미니사전

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **LMRO** | Li- and Mn-Rich layered Oxide, `xLi₂MnO₃·(1−x)LiTMO₂`. TM 층에 Li 가 과잉으로 들어가 `LiMn₆` 벌집 초격자를 만든다 | 양극 본체. `C2/m`(`Li₂MnO₃`) + `R3̄m`(`LiTMO₂`) 두 상 |
| **`C2/m` 분율** | `Li₂MnO₃` 유사 단사정 도메인의 무게분율. XRD 20–24° 초격자 hump 로 보이고 Rietveld 로 정량 | **절연성의 원인** — 클수록 σ_e·σ_ion 이 낮다 |
| **음이온(산소) 산화환원** | 4.4 V 위에서 TM 이 아니라 격자 O²⁻ 가 전하보상을 하는 기전. 고용량의 원천이자 O₂ 방출의 원인 | 4.4–4.6 V 평탄부 |
| **`−S⁰−` (폴리설파이드)** | S–S 가교를 가진 중성에 가까운 황. XPS S 2p **163.6 eV**. **전자·이온 둘 다 안 통한다** | 산화산물, 2.3 V 아래 방전에서 `S²⁻` 로 환원 |
| **`P₂S₇⁴⁻`** | 두 `PS₄` 사면체가 S 하나를 공유한 이사면체. XPS S 2p **163.0** / P 2p **132.5 eV** | 산화산물. **`Li₇P₃S₁₁` 의 구성단위라 Li⁺ 전도에 해롭지 않다**(저자 방어) |
| **`PSₓOᵧ³⁻`** | O 가 일부 S 를 대체한 티오인산 음이온. P 2p **133.9 eV** | 🔴 **비가역 누적.** 산소는 양극/`LiNbO₃` 에서 온다 |
| **`SO₃²⁻`** | 아황산(S⁴⁺). S 2p **168.5 eV** | 🔴 1000사이클 후 신규 — 본문 미언급 |
| **이온차단셀 / 전자차단셀** | 혼합전도체의 σ_e / σ_ion 을 따로 재기 위한 셀. 전자는 `SS/시료/SS`, 이온은 `Li-In/SE/시료/SE/Li-In` | `Fig. S4`·`Fig. S6`. **우리가 배울 설계** |
| **VGCF** | Vapor-Grown Carbon Fiber. 복합양극 전자경로 | 5 wt%(양극) / 10 wt%(CV 셀) |
| **`LiNbO₃` 버퍼** | 황화물 SE 와 산화물 양극 사이 표준 완충층. Li⁺ 전도성 산화물 | 2 wt%, **1–2 nm** — ⚠ **맨 계면이 없는 이유** |
| **HAADF-STEM** | 고각환상암시야 주사투과전자현미경. 밝기 ∝ Z^≈1.7 → 중원소 자리가 밝다 | `Fig. 2b,c`·`Fig. 4` |
| **EELS Mn L₃/L₂** | Mn 2p→3d 백선의 강도비. 비가 클수록 Mn 가수가 낮다 | `Fig. S12c,f` — 산소방출 깊이의 대리지표 |
| **grand-potential ESW** *(우리 쪽 용어)* | Li 저장소를 연 대퍼텐셜 `Φ = E − n_Li μ_Li` 의 convex hull. `μ_Li = μ⁰_Li − eV` | 이 논문에 **없다**. 우리 2.256 V 가 여기서 온다 |
