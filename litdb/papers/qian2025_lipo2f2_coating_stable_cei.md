# Engineering Stable Decomposition Products on Cathode Surfaces to Enable High Voltage All-Solid-State Batteries — Qian/Huang/Dean/Kochetkov/Singh/Nazar (Angew. Chem. Int. Ed. 2025)

> slug `qian2025_lipo2f2_coating_stable_cei` · DOI `10.1002/anie.202413591` (독일어판 typeset = *Angew. Chem.* **2025**, 137, e202413591, `10.1002/ange.202413591` — 내용 동일 영문) · type `DFT (convex-hull 열역학, MP 기반) + exp (코팅·전기화학·XPS/ToF-SIMS)` · PDF 본문 `99737a54-73._engineering_Stable_Decomposition_Products…pdf` (9 pp) + SI `08022c09-73._Sup_…pdf` (14 pp, Fig S1–S9 + Table S1) — **본문+SI 통합 digest** · digested `2026-09-08` · status ✅
> **저자**: **Lanting Qian⁺**, **Yangyang Huang⁺**, Cameron Dean, **Ivan Kochetkov**, **Baltej Singh**, **Linda F. Nazar\*** (lfnazar@uwaterloo.ca) — Department of Chemistry & Waterloo Institute of Nanotechnology, **University of Waterloo**, 200 University Ave, Waterloo ON, Canada. ⁺공동 1저자.
> Received **2024-07-18** / Accepted manuscript online **2024-11-12** / Version of record **2024-12-04**. **Open access (CC-BY)**. refs 48. Keywords: solid-state battery · cathode-electrolyte interface · argyrodite electrolyte · **DFT** · cathode coating by design.
> **연구비/재료 공급**: BASF + NSERC(L.Q.), **BASF-SE 가 다결정 NCM85 제공**, NSERC CRC·Discovery, Ontario Research Fund. XANES = Canadian Light Source(SGM). 이해상충 없음 선언. ⚠ **CAM 공급자가 연구비 지원자와 동일**(BASF) — 결론이 코팅 효과라 편향 여지는 작지만 기록.
> **그룹 계보**: **Waterloo/Nazar 라인 4번째 논문**. `[Adeli]`(조성축 Cl-rich) → `[Zuo]`(계면축, Nazar 공저) → **본 논문**(양극 입자 코팅축, 2025) → `[Qian26]`(SE 입자 유기코팅축, 2026). 1저자 Lanting Qian·공저 Kochetkov 는 `[Qian26]` 과 동일 인물, ref [43] = Kochetkov 2022 EES(TLM 원전, 본인 논문).


> elements: Li, P, O, F, S, Cl, Ni, Co, Mn
> methods: DFT, VASP, ESW, grand-potential, bandgap, XPS

---

## 0. 이 digest 를 읽는 법 (우리 캠페인에서의 위치)

이 논문의 질문은 한 줄이다 — **"코팅 물질을 고를 때, 그 물질 자체가 아니라 *그 물질이 깨져서 만들 산물*을 보고 골라야 하지 않나?"**

답: **LiPO₂F₂(=LiPOF)** 를 골랐고, 그 근거를 **convex hull 열역학 3종**(① 자체 전기화학창, ② SE 와의 혼합 반응, ③ 양극과의 혼합 반응)으로 세운 다음, 실험(코팅→셀→XPS/ToF-SIMS)으로 예측 산물(**LiF · LiPₓOᵧF_z**)이 실제로 생기는 것을 확인했다.

> **우리 관점에서 이 논문이 특별한 이유 — 방법이 우리 것과 *같은 기계*다.**
> 이 논문의 Fig 1 은 전부 **pymatgen** 의 `get_element_profile`(1a) + `InterfacialReactivity`(1b) +
> `GrandPotentialInterfacialReactivity`(1c–f)로 그린 것이다. 우리 `tools/oxidation/esw_grand_potential.py`,
> `tools/oxidation/interface_reactivity.py`, `tools/oxidation/interface_reactivity_v2.py` 가 **같은 클래스를
> 같은 순서로 호출**한다. 즉 이 논문은 우리에게 "새 물리"가 아니라 **우리 도구가 뱉는 그림의
> 외부 대조군이자, 그 그림을 논문에 어떻게 배치·해석하는가의 서식 견본**이다.
> → 그래서 §10 「우리가 활용할 수 있는 부분」을 convex hull 중심으로 따로 뺐다 (1저자 지정).

> ⚠ **축 명명 규율**: 이 논문의 이득은 **산화 4축 중 B③(계면 산물/CEI)** 이다.
> **B①(intrinsic 산화 onset)은 건드리지 않는다** — 저자들도 LPSCl 의 ~2.5 V 산화한계를
> 전제로 깔고 "그 위에서 어떻게 버티게 할까"만 묻는다. "Cl-rich 산화안정" 같은 말과 절대 섞지 말 것.

> ⚠ **전압 기준**: 본문·그림 전부 **vs Li⁺/Li**. 셀 대극은 Li–In 이므로 실측 셀 전압은 −0.62 V 이다
> (2.8–4.3 V vs Li⁺/Li ≡ 2.18–3.68 V vs Li–In). **단 Fig 4 캡션만 "OCV ~3.7 V vs Li−In"** 이라 기준이 섞여
> 있다(§13 ⑪).

---

## 1. 한 줄 요약

**LiPO₂F₂(LiPOF)** 를 DMC 용액으로 NCM85 에 1 wt% 코팅(**~25–35 nm 비정질 conformal, 100 °C 증발 건조, 소결 0**) 하면, DFT convex-hull 이 예측한 대로 **LiF + LiPₓOᵧF_z + LiPO₃** 계 CEI 가 만들어져 **Li₆PS₅Cl 의 산화분해를 막는다** → 2.8–4.3 V·0.2 C·200 cyc 에서 **유지율 81.4 %(bare 56.0 %)**, **R_cathode 90 Ω·cm²(bare 200)**, S 2p 의 산화-S 신호 소멸, ToF-SIMS SOₓ⁻ 대폭 감소. 고로딩(25.6 mg/cm²)에서도 **4.4 mAh/cm²·200 cyc 77 %**.

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| 문제 | 황화물 SE(Li₆PS₅Cl)의 산화한계 **~2.5 V** vs 고Ni NCM 작동 **4.3 V** → 계면에 POₓ·SOₓ 절연층 축적 → 저항↑·용량 급락 |
| 기존 해법 | 산화물 코팅(LiNbO₃·Li₂ZrO₃·Li₃BO₃–Li₂CO₃·HfO₂) — 대부분 **spray/sol-gel + >300 °C 소결** → 비싸다 |
| 이 논문의 착상 | **LiPON 선례**(ref [7]=Richards16): LiPON 자체가 아니라 그 *분해산물*(Li₄P₂O₇·LiPO₃·P₄O₁₀)이 고전압 안정해서 고전압 양극과 호환된다 → **"분해산물이 안정한 물질을 코팅으로 고르자"** |
| 후보 | **LiPO₂F₂ (LiPOF)** — 액체계 LIB 에서 CEI 형성 첨가제로 검증된 염(refs 12–14), **극성 용매에 녹고** 그 분해산물은 불용 → 용액 도포 후 증발만으로 코팅이 남는다 |
| 이상적 코팅의 4조건(본문 명시) | ① 적합한 전기화학창(**물질 자체 창** *또는* **속도론적으로 안정화된 산물의 창**) ② 낮은 전자전도 ③ 높은 이온전도 ④ 얇고 균일한 막 형성능 |
| 계 | CAM = **NCM85 = LiNi₀.₈₅Mn₀.₁Co₀.₀₅O₂**(BASF, D50 ~4 µm, 다결정) / SE = **상용 Li₆PS₅Cl**(Ampcera, D50 ~1 µm, **σ 2.2 mS/cm**) / 음극 = **In/LiIn** |
| 유형 | 계산 + 실험 (계산 = Fig 1 전부, SI Table S1; 나머지 전부 실험) |

## 3. 핵심 수치 총정리

### 3a. 계산 결과 (Fig 1 · SI Table S1 에서)

| 양 | 값 | 조건 / 출처 |
|---|---|---|
| **LiPO₂F₂ 자체 안정 전압창** | **2.6 – 4.9 V** vs Li⁺/Li | `Fig. 1a` grand-potential element profile (본문 명시값) |
| LiPOF 환원 시 Li 흡수량 | **~8 Li/f.u.** (0 V 에서 Li/f.u. = 9, 창 안에서 1) | `Fig. 1a` **figure-read ≈** |
| LiPOF 산화 시 | 4.9 V 위에서 Li/f.u. → **~0** (P₂O₃F₄, Li_xO) | `Fig. 1a` **figure-read ≈** |
| **LPSCl\|LiPOF 혼합 반응 최저점 (전위 무인가)** | **≈ −145 meV/atom @ x = 0.52** | `Fig. 1b` **figure-read ≈** (x 는 본문 명시) · 산물 **Li₃PO₄ + LiF + LiCl + P₂S₅** |
| 〃 (0.4 < x < 0.6 주변) | ≈ −130 meV/atom @ x ≈ 0.42 | `Fig. 1b` **figure-read ≈** · 산물 **Li₄P₂O₇ + LiF + LiPO₃ + LiCl + P₂S₅** |
| **Li₆PS₅Cl 자체 분해 구동력** | **≈ −83 meV/atom** (→ Li₃PS₄ + Li₂S + LiCl) | `Fig. 1b` x = 1.0 회색 점선 "Decomposition" **figure-read ≈** · = 그들 데이터셋에서 LPSCl 의 E_above_hull |
| **LPSCl\|LiPOF @ 2.8 V** | **≈ −43 meV/atom @ x ≈ 0.62** | `Fig. 1c` **figure-read ≈** · 산물 **LiPO₃ + LiF + LiCl + P₂S₇** (인접 kink: LiF+Li₄P₂O₇+LiCl+P₂S₇) |
| **LPSCl\|LiPOF @ 4.3 V** | **≈ −96 meV/atom @ x ≈ 0.08** | `Fig. 1d` **figure-read ≈** · 산물 **LiPO₃ + P₂O₃F₄ + SOCl₂** |
| **NCM\|LiPOF @ 2.8 V** | **≈ −395 meV/atom @ x ≈ 0.41** | `Fig. 1e` **figure-read ≈** · 산물 **CoO + NiO + Li₃PO₄ + LiF** |
| **NCM\|LiPOF @ 4.3 V** | **≈ −108 meV/atom @ x ≈ 0.61** | `Fig. 1f` **figure-read ≈** · 산물 **Li₂NiF₄ + CoO₂ + MnO₂ + Ni₃(PO₄)₂** |
| 저반응성 판정 문턱 | **\|ΔE_rxn\| < 100 meV/atom** | 본문, ref [7] 인용 (⚠ 귀속 주의 §13 ⑨) |
| DFT 에 넣은 NCM 조성 | **LiMn₀.₀₈₃Co₀.₀₈₃Ni₀.₈₃O₂** | `Fig. 1e,f` x축 **figure-read** — ⚠ 실험 CAM(LiNi₀.₈₅Mn₀.₁Co₀.₀₅O₂)과 **다르다** |

**Table S1 — 계면 산물의 전압창·밴드갭 (SI 원문 텍스트, 그림 아님)**

| 조성 | 전압창 (vs Li⁺/Li) | Band gap (eV) |
|---|---|---|
| LiF | 0 – 6.3 V ⁽¹⁾ | **8.7** |
| LiCl | 0 – 4.3 V ⁽¹⁾ | **6.3** |
| LiPO₃ | 2.5 – 4.9 V ⁽²⁾ | **2.5** |
| Li₃PO₄ | 0 – 5.0 V ⁽³⁾ | **5.8** |
| Li₄P₂O₇ | 2.3 – 4.3 V | 5.6 |
| Li₂NiF₄ | 2.8 – 5.6 V | 4.7 |
| P₂S₅ | 2.3 V – (상한 없음) | 2.6 |
| P₂O₃F₄ | 3.1 V – | 5.8 |
| SOCl₂ | 3.3 V – | 3.6 |
| P₂S₇ | 2.3 V – | **2.1** |
| CoO | 1.9 V – | 0.6 |
| CoO₂ | 4.1 V – | 0.6 |
| MnO₂ | 3.7 V – | 0.5 |
| Ni₃(PO₄)₂ | 2.8 V – | 3.4 |

> SI 주석: *"P₂S₅ 이하 항목은 Li 를 포함하지 않아 상한 전압이 없다."* 출처는 *"다른 연구[7,32,33] 에서 추출하거나 DFT 로 추정"* — 표의 ⁽¹⁾⁽²⁾⁽³⁾ 가 refs 7/32/33 중 무엇인지는 **SI 에 매핑이 없다**. ([7]=Richards 2016, [32]=Guo 2024 EES, [33]=**Xiao 2019 Joule = 우리 `xiao2019` digest**)

### 3b. 실험

| 항목 | bare NCM85 | **LiPOF-coated (1 wt%)** | 출처 |
|---|---|---|---|
| 코팅 두께 | — | **~25–35 nm** 비정질 conformal | 본문 · `Fig. 2c,e` 는 **~35 nm** 두 곳 표기 |
| 초기 방전용량 (0.2 C) | 170 mAh/g | **182 mAh/g** | 본문 |
| **ICE** | **64.6 %** | **81.6 %** | `Fig. 3a` 도면 주석 (본문은 65 / 82 로 반올림) |
| 첫 충전용량 | ≈ 270 mAh/g | ≈ 222 mAh/g | `Fig. 3a` **figure-read ≈** — 차이 ≈ 48 mAh/g 이 argyrodite 산화 몫 |
| 0.1 C / 1 C 방전 | 152 / 51 mAh/g | **180 / 85 mAh/g** | 본문 (`Fig. 3c` figure-read ≈ 152/52 vs 180/88 로 정합) |
| **200 cyc 유지율 (0.2 C, 9.9 mg/cm²)** | **56.0 %** (97 mAh/g) | **81.4 %** (147 mAh/g) | `Fig. 3d` 도면 주석 |
| 100 cyc 유지율 | — | 90 % | 본문 |
| 고로딩 (25.6 mg/cm²) | — | **4.4 mAh/cm²**, 초기 173 mAh/g, **200 cyc 77 %** | 본문 · `Fig. 3e` |
| **R_cathode (200 cyc 후, TLM fit)** | **200 Ω·cm²** | **90 Ω·cm²** (< 절반) | `Fig. 4a` |
| R_bulk (x절편) | ≈ 52 Ω·cm² | ≈ 43 Ω·cm² | `Fig. 4a` **figure-read ≈** (본문: "pre/post 유사") |
| S 2p 산화-S (163.2 eV) | **크다** | **무시 가능** | `Fig. 4b` |
| F 1s (200 cyc 후) | **신호 없음** | **LiPₓOᵧF_z(688.3) + LiF(684.9)** | `Fig. 4c` |
| ToF-SIMS SOₓ⁻ | 강함 (SO₂⁻>SO₃⁻>SO⁻) | 약함 (SO₂⁻>SO⁻>SO₃⁻) | `Fig. 5` |
| 2 wt% 코팅 | — | 80 cyc **92 %**, 초기 ≈167 mAh/g, ICE ≈ **78.6 %** | `Fig. S7` (92 % 는 도면 주석, 나머지 **figure-read ≈**) |
| 1 wt% 동일 구간 | — | 80 cyc 93 %, 초기 182 mAh/g | 본문 |
| 셀 조립 | SE 펠릿 120 mg @ **250 MPa 1 min** / 복합양극 **SE:CAM = 2:8 wt** 마노유발 15 min, **200 MPa 3 min** / In 포일 φ10 mm × 0.1 mm + Li ~1.5 mg → LiIn / **스택압 200 MPa** | | SI |
| 전기화학 | 1 C = **200 mA/g**, VMP3 or MACCOR, EIS **25 °C, 100 mHz–1 MHz**, RelaxIS 피팅 | | SI |
| ⚠ | **복합양극에 카본 도전재 없음** (SE:CAM 2:8 만) | | SI |

---

## 4. DFT / 계산 방법 ★ (SI "Computational Methods" 전문 + 그림에서 역추적)

- **code**: **VASP** (버전 미기재)
- **입력 규약**: *"All calculations used VASP input parameters that **matched those used by Materials Project** for energy minimization"*
  - **ENCUT = 520 eV**
  - **k-mesh = Monkhorst–Pack, 1000 per reciprocal atom** (= MP 의 `KPPRA=1000` 관례)
  - **수렴 = 0.0005 × (원자수) eV per cell** (= MP 의 `EDIFF_PER_ATOM` 관례)
- **functional**: ⛔ **명시 없음**. "MP 파라미터와 일치" 라는 서술로만 암시 → 실질적으로 **PBE(GGA) + GGA+U**(전이금속 산화물에 MP 의 Hubbard U) 로 읽어야 하지만 **논문은 PBE 도 U 값도 쓰지 않았다**. Ni/Co/Mn 이 들어가는 Fig 1e,f 판정에 직접 영향.
- **pseudo / PAW**: ⛔ **명시 없음** (MP 는 특정 POTCAR 세트 고정).
- **DFT+U**: ⛔ **명시 없음**.
- **에너지 보정**: ⛔ **명시 없음** — 황화물+산화물+불화물을 **한 hull 에 섞으므로** MP2020Compatibility(anion/음이온 보정)가 사실상 필수인데 언급이 전혀 없다 (§13 ②).
- **supercell / nat / 이완 조건**: ⛔ 명시 없음. LiPO₂F₂ 는 *"crystal structure of LiPO₂F₂ 로 0 K DFT 에너지를 계산"* 이라고만 씀 (어느 ICSD/공간군인지 미기재).
- **무질서 처리**: ⛔ **전혀 언급 없음**. Li₆PS₅Cl 의 **S²⁻/Cl⁻ 4a/4d 자리 무질서**를 어떤 배열로 대표했는지 안 적었고, NCM 고용체(Ni/Co/Mn 랜덤)를 어떤 셀로 대표했는지도 안 적었다. Fig 1e,f 의 x축이 **LiMn₀.₀₈₃Co₀.₀₈₃Ni₀.₈₃O₂** 인 것으로 보아 **12-포뮬라(1/12 = 0.0833) 정수 치환 셀**을 쓴 정황이지만 본문에 서술은 없다.
- **AIMD / MLIP / NEB / phonon**: **없음** (0 K 정적 열역학만).
- **데이터 출처 (hull 참조상 집합)**:
  1. **Materials Project DB** 에서 **Li–P–O–F 계** 전 화합물의 DFT 에너지 소환 (**DB 버전·API 버전 미기재**)
  2. + **ICSD** 에서 추가 구조를 가져와 **같은 파라미터로 자체 계산**해 보충
  3. + **LiPO₂F₂ 자체 계산**
  4. Fig 1b–d 는 여기에 **S·Cl** 이, Fig 1e,f 는 **Ni·Co·Mn** 이 더 필요 → 그 원소들의 참조상 집합은 **어디서 왔는지 SI 에 적혀 있지 않다** (MP 로 추정되나 미명시).
- **후처리 도구**: **pymatgen (Python Materials Genomics)** — *"Pymatgen 패키지로 LiPO₂F₂ 의 element profile 을 인가전위에 대해 생성"*.

### 4b. hull 을 실제로 어떻게 썼나 — 세 가지 다른 계산 (이게 이 논문의 핵심 기술)

| # | 그림 | 무엇 | 화학공간 | 열린 원소 | 반환값 |
|---|---|---|---|---|---|
| **①** | `Fig. 1a` | **element profile** — μ_Li 를 스캔하며 LiPO₂F₂ 가 hull 위에 있는 전압 구간 | Li–P–O–F | **Li 열림** (μ_Li = μ⁰ − eφ) | Li/f.u. 계단 + 각 구간의 평형상 → **창 2.6–4.9 V** |
| **②** | `Fig. 1b` | **닫힌 계 pseudo-binary 계면반응** — `x·LPSCl + (1−x)·LiPOF → P3`, x 를 0→1 스캔해 최소화 | Li–P–S–Cl–O–F | **없음 (닫힌 계)** | ΔE_rxn(x) 곡선 + 각 kink 의 산물 |
| **③** | `Fig. 1c–f` | **grand-potential 계면반응** — ②를 μ_Li 고정(=2.8 V / 4.3 V) 하에서 다시 | 〃 (+Ni,Co,Mn) | **Li 열림, μ_Li 고정** | 전압별 ΔE_rxn(x) + 산물 |

**세 계산의 관계** (이 논문이 명시하지 않은 것까지 우리가 정리):
- ①은 **코팅 혼자**의 창 → "본질적 안정성".
- ②는 *"이 창은 다른 상과 접촉하지 않은 벌크 정보라, 전해질/양극과의 반응은 못 본다"* (본문 원문 취지) → 임의 비율로 섞일 수 있으니 **x 를 자유변수로 두고 최악(최저)점을 찾는다**. 이것이 **pseudo-binary** 형식 = `[Rich16]`.
- ③은 ②에 **작동 전압**을 얹은 것 = `[Rich16]` eq 4. 셀이 도는 동안 μ_Li 는 Li 저장고가 정한다는 물리.
- **끝점 규약**: Fig 1c–f 는 **x = 0 과 x = 1 에서 ΔE_rxn = 0** 이다 → 각 끝점이 **자기 hull 로 이미 평형화된 상태**를 기준으로 잡는 규약(pymatgen `use_hull_energy=True`)이다. Fig 1b 만 x=1.0 끝점을 **−83 meV/atom** 에 두고, 회색 점선으로 "미분해 Li₆PS₅Cl(0) → 분해상태(−83)" 를 따로 그려 **LPSCl 자체가 이미 hull 위가 아님**을 보인다 (ref [30] Schwietert/Wagemaker, ref [31] Jain/MP 와 일치한다고 주장).

---

## 5. 결과 — 절별 상세

### 5.1 계산 ① — LiPOF 자체 창
`Fig. 1a`. Li/f.u. 를 y축(0–10), 인가전압을 x축(0–7 V)으로 그린 **계단 그림**. 0 V 에서 **9 Li/f.u.**(= LiPO₂F₂ 1 Li + 환원으로 8 Li 흡수) → ~0.7 V, ~1.1 V, ~2.0 V 에서 계단 하강 → **2.6 V 에서 Li/f.u. = 1 로 떨어져 4.9 V 까지 평평**(초록 영역, **LiP(OF)₂ = LiPO₂F₂ 자체가 hull 위**) → **4.9 V 에서 ~0 으로** 붕괴.
- 창 아래(주황): **LiF, Li_xP, LiP_yO_z**. 창 위(주황): **P₂O₃F₄, Li_xO**.
- 결론: **2.6–4.9 V** ⊃ NCM85 작동창 **2.8–4.3 V** → *"통상 작동조건에서 코팅은 본질적으로 안정"*.
- ⚠ 여백이 **아래쪽 0.2 V 뿐**이다. 방전 하한 2.8 V 에서 코팅 환원까지 0.2 V 밖에 안 남는다(§13 ③).

### 5.2 계산 ② — LPSCl 과 섞이면 (전위 무인가)
`Fig. 1b`. `x·Li₆PS₅Cl + (1−x)·LiP(OF)₂ → P3` 를 x=0→1 로 훑는다.
- **최저 x = 0.52**, ΔE_rxn **≈ −145 meV/atom** → **Li₃PO₄ + LiF + LiCl + P₂S₅**
- x ≈ 0.42 → **Li₄P₂O₇ + LiF + LiPO₃ + LiCl + P₂S₅** (본문: 0.4<x<0.6 에서 LiF·LiPO₃·Li₄P₂O₇ 같은 유리한 산물)
- x ≈ 0.81 → 같은 **Li₃PO₄ + LiF + LiCl + P₂S₅** 세트
- x = 1.0 (LPSCl 단독) → **Li₃PS₄ + Li₂S + LiCl**, **≈ −83 meV/atom**
- 저자 해석: 생기는 것들이 **Table S1 상 넓은 창·큰 gap** 이라 계면을 **부동태화**할 것이다. 코팅 재료로 이미 검증된 종들(refs 6, 34)이다.

### 5.3 계산 ③ — 전압을 걸면
- **2.8 V** (`Fig. 1c`): 최저 x ≈ 0.62, **≈ −43 meV/atom** → **LiPO₃ + LiF + LiCl + P₂S₇** (바로 옆 kink x≈0.68 은 **LiF + Li₄P₂O₇ + LiCl + P₂S₇**). 전부 *"NCM 에 대해 Li₆PS₅Cl 보다 훨씬 반응성이 낮다"*.
- **4.3 V** (`Fig. 1d`): 최저 **x ≈ 0.08**, **≈ −96 meV/atom** → **LiPO₃ + P₂O₃F₄ + SOCl₂**.
  - **P₂O₃F₄ 는 방전(2.8 V)에서 리튬화/환원되어 LiP₂O₃F₄ 또는 "비정질 LiPₓOᵧF_z" 가 될 것**으로 예상 — **이 예측이 곧 XPS 로 확인되는 항목**(`Fig. 4c`).
  - **SOCl₂ 는 액체 → 속도론적으로 막혀 실제로는 안 생길 것**이라고 스스로 배제.
- 두 경우 모두 **\|ΔE_rxn\| < 100 meV/atom** → *"낮은 화학반응성의 지표"* (ref [7]) → **LiPOF 는 넓은 창 + LPSCl 과 좋은 호환성**.
- ⚠ **Fig 1b 의 −145 는 이 문턱을 넘는다** — "<100" 주장은 **전압을 건 ③에만** 해당한다(§13 ④).

### 5.4 계산 ③′ — 양극과 섞이면
- **2.8 V**: 최저 x ≈ 0.41, **≈ −395 meV/atom** → **CoO + NiO + Li₃PO₄ + LiF**
- **4.3 V**: 최저 x ≈ 0.61, **≈ −108 meV/atom** → **Li₂NiF₄ + CoO₂ + MnO₂ + Ni₃(PO₄)₂**
- 저자 처리: *"이 산물들을 실험에서 유의미한 양으로 검출하지 못했다 → 큰 반응에너지에도 불구하고 **자기제한적**이고 분해 범위가 **속도론**에 묶여 있다고 본다"*, 그리고 *"argyrodite 결정립은 주로 LPSCl|LiPOF 산물과 접하므로 CAM|LiPOF 산물은 LPSCl 열화에 영향이 작다"*.
- 저자 스스로의 마무리: *"이 계산들은 열역학적으로 유리한 산물을 예측할 뿐 **반응 속도론을 무시**한다 … 그래서 계면에 생길 수 있는 화합물의 **저비용 예측**으로만 쓰고 실험으로 검증한다."*
- ⚠ **−395 meV/atom 은 자기 문턱의 4배**다. "속도론이 막는다"는 사후 해명이고 계산적 근거는 없다(§13 ⑤).

### 5.5 코팅 제조·구조 (`Fig. 2`, `Fig. S1–S6`)
- **공정**: Ar 하 LiPO₂F₂ 를 **DMC** 에 2 h 교반 용해 → NCM85 투입 2 h 교반 → **100 °C, N₂ 유동 하 증발** → **100 °C 6 h 진공 건조**(BUCHI). **소결 없음, 상압.**
- 코팅 중 **LiPOF 염이 부분적으로 이미 분해**되어 안정 산물로 NCM 표면에 남는다.
- **FTIR (`Fig. S1`)**: 코팅 시료에만 LiPOF 특성 밴드 — **P–O 비대칭/대칭 1273 / 1163 cm⁻¹**, **P–F 비대칭/대칭 934 / 887 cm⁻¹**.
- **F 1s XPS (`Fig. S2`)**: 순수 LiPO₂F₂ 는 **≈688.3 eV 단일 피크**. 코팅된 NCM 은 **≈690.2(Li_xP_yF_z) + ≈688.1(LiPₓOᵧF_z) + ≈684.9(LiF, 소량)** 3성분. (**figure-read** BE)
- **XANES Ni L-edge (`Fig. S3`) · XRD (`Fig. S4`)**: NCM85 벌크 **R3̄m** 층상 구조 코팅 전후 불변.
- **SEM (`Fig. 2a`, `Fig. S5`)**: 코팅/무코팅 모두 **~4 µm 구형 2차입자**(1차 결정립 응집).
- **HRTEM (`Fig. 2b,c,e,f`)**: **~35 nm 균일 비정질 층** (도면 주석 2회; 본문은 "25–35 nm"). `Fig. 2f` 는 격자무늬 없는 **amorphous compositions**.
- **STEM-EDX (`Fig. 2g`)**: P·O·F·Ni·Mn·Co 맵. 저자 주장 *"Li·P·O·F 가 표면에 균일 분포"*.
- `Fig. 2d` 는 캡션·본문 어디에도 없는 **모식도**(NCM85 + Coating Layer = LiF / Li_xP_yF_z / LiPₓOᵧF_z).

### 5.6 첫 사이클 — 코팅이 argyrodite 산화를 지운다 (`Fig. 3a,b`)
- **`Fig. 3a`**(0.2 C, 2.8–4.3 V, 9.9 mg/cm²): bare 첫 충전이 **≈270 mAh/g** 까지 부푸는데(정상 NCM85 는 ~220), 방전은 170 → **ICE 64.6 %**. 코팅은 충전 ≈222 / 방전 182 → **ICE 81.6 %**. **잉여 충전용량 ≈48 mAh/g 이 곧 LPSCl 산화 몫**.
- bare 충전곡선의 **3.5 V 이하 sloping 구간**(= Li₆PS₅Cl 산화, ref [36] Koerver 2017)이 코팅에서는 **사라진다**.
- **`Fig. 3b` dQ/dV**: bare 만 **~3.0–3.2 V 에 넓은 혹**(도면 라벨 **"Argyrodite decomposition"**). NCM 자체 전이 피크는 **H1+M(~3.65 V) · M+H2(~3.95 V) · H2+H3(~4.2 V)** 세 개(도면 라벨). 코팅 쪽이 특히 **H2+H3 피크가 더 크고 더 가역**(figure-read: 충전 피크 ≈1.8 vs bare ≈1.3 Ah g⁻¹ V⁻¹).
  - ⚠ 본문은 이 세 피크를 *"H1 to M, H2, H3 전이"* 로 쓰는데 **도면 라벨은 H1+M / M+H2 / H2+H3** 다. 도면 라벨을 따르는 게 맞다.
  - 저자 자인: *"이 현상을 완전히 이해하지는 못한다"*.

### 5.7 율속·수명 (`Fig. 3c,d,e`, `Fig. S7`)
- **율속(`Fig. 3c`)**: 0.1/0.2/0.5/1.0/2.0 C 후 0.1 C 복귀. 코팅 **180 / 85 mAh/g @ 0.1 / 1 C**, bare **152 / 51**. 2.0 C 에서 코팅 ≈40 vs bare ≈20 (**figure-read**). 복귀 0.1 C 에서 코팅 ≈177, bare ≈152 (**figure-read**) → bare 는 **회복도 안 된다**.
- **수명(`Fig. 3d`)**: 200 cyc @0.2 C — 코팅 **147 mAh/g, 81.4 %** vs bare **97 mAh/g, 56.0 %**. CE 는 둘 다 ~99–100 %.
- **고로딩(`Fig. 3e`)**: 25.6 mg/cm², **4.4 mAh/cm²**, 초기 173 mAh/g, **200 cyc 77 %**. (figure-read 로는 200 cyc 잔량 ≈140 mAh/g → 140/173 = 81 % 로 보여 본문 77 % 와 미세 불일치, §13 ⑧)
- **2 wt% (`Fig. S7`)**: 9.7 mg/cm², 80 cyc **92 %** — 1 wt% 의 93 % 와 사실상 같지만 **초기용량이 167 vs 182 mAh/g 로 낮고 ICE 도 ≈78.6 %(figure-read) vs 81.6 %** → **두꺼우면 임피던스 손해**. **1 wt% 가 최적.**
- 문헌 대비(본문): LiNbO₃ 코팅 **75 cyc 84 %**(ref 40, 같은 LPSCl·NCM85·0.2 C) / Li₂HfO₃·HfO₂ **200 cyc 81 %지만 45 °C**(ref 42) / LiDFOB-코팅 NCM622 **100 cyc 80 %**(ref 18) / 폴리머 코팅 **100 cyc 86 % @0.1 C**(ref 17).

### 5.8 임피던스 — TLM (`Fig. 4a`)
- 등가회로: **R_bulk(SE 펠릿) + TLM(blocking boundary)**. TLM 3요소 = **R_ion(양극 이온) / R_e(양극 전자) / R_int(CEI 저항, R‖CPE 가지)**, 그리고 도면에 **R_cathode = √(R_int·(R_ion + R_e))** 를 명시. 절차 출처 = **ref [43] = Kochetkov 2022 EES**(본 논문 공저자).
- Nyquist(ReZ 30–250, −ImZ 0–60 Ω·cm²): 사이클 전에는 두 셀 유사, 200 cyc 후 **bare 200 vs coated 90 Ω·cm²**.
- 본문 주의: 양극 반원이 **<10 Ω·cm² 로 작고 Li⁺ 확산 영역과 겹쳐 정확히 피팅 불가** — 그래서 **절대값보다 변화량 비교**로 읽으라고 스스로 단서.

### 5.9 XPS — 산화된 황이 없다 (`Fig. 4b,c`, `Fig. S8`)
- **S 2p (`Fig. 4b`, 200 cyc 후)**: 2p₃/₂ 기준 **160.2 eV = "free" S²⁻**, **~161.6 eV = PS₄³⁻**, **~163.2 eV = 산화로 생긴 S⁰**.
  - **coated**: S⁰ **거의 0**. **uncoated**: S⁰ 성분이 PS₄³⁻ 에 필적할 만큼 크고, 추가로 **thiosulfate(~167)·polythionate(~168–169)** 까지 뜬다(도면 라벨).
- **F 1s (`Fig. 4c`, 200 cyc 후)**: coated = **LiPₓOᵧF_z(≈688.3) + LiF(≈684.9)** 두 성분, **LiF 가 사이클 전보다 크게 성장**. uncoated = **F 신호 없음**(잡음).
  - `Fig. S2`(사이클 전) 대비: **690 eV 의 Li_xP_yF_z 가 사라지고 LiF 로 전환** → 본문 *"LiPOF 와 Li_xP_yF_z 의 상당량이 LiF 와 LiPₓOᵧF_z 로 전환"* = **DFT 예측(P₂O₃F₄ → 방전 시 LiPₓOᵧF_z, 그리고 LiF)의 실험 확증**.
- **P 2p (`Fig. S8`)**: 3단 비교. (상) 미사이클 코팅 입자 = **P–F(≈136.2) + P–(OF)(≈134.2)**. (중) 사이클 코팅 셀 = 작은 **P–F_x(≈135.8)** + **P–O_x(≈133.3)** + **PS₄³⁻(≈132.0, 지배적)**. (하) 사이클 무코팅 셀 = **P–O_x 가 PS₄³⁻ 에 필적/우세**.
  - 저자 논리: LiPO₃ 의 P 2p₃/₂ 는 **133 eV** 로 Li₃PO₄·산화된 LPSCl 의 POₓ 와 **구분 불가** → P 2p 로는 LiPO₃ 를 확정 못 한다. 다만 **S 2p 에 산화-S 가 없으니** 코팅 셀의 133 eV 는 **LiPO₃ 일 가능성이 높다**.
  - (우리 추가 판독) **P–Oₓ/PS₄³⁻ 면적비가 무코팅에서 확실히 크다** — 논문이 강조하지 않은 보조 증거다(**figure-read**).

### 5.10 ToF-SIMS (`Fig. 5`)
- ION-TOF ToF-SIMS 5, **음이온 모드**, 30 keV 클러스터 이온총, **200 × 200 µm²**, 256×256 px, 주 이온전류 ~0.3 pA, stop 5×10¹² ions/cm². **전 이온신호로 정규화**.
- **SO⁻ / SO₂⁻ / SO₃⁻** 6장 heat map. 컬러스케일은 bare/coated **동일**(SO⁻ 0.002–0.010, SO₂⁻ 0.002–0.014, SO₃⁻ 0.000–0.012).
- bare 가 전면적으로 훨씬 밝다 (SO₂⁻·SO₃⁻ 는 **스케일 상단에서 포화**). 순위: bare **SO₂⁻>SO₃⁻>SO⁻**, coated **SO₂⁻>SO⁻>SO₃⁻**. 무코팅/코팅 비율의 크기 순위는 **SO₃⁻ > SO₂⁻ > SO⁻** → *"코팅은 황 산화를 막는 데 매우 효과적"*.
- 근거: SOₓ⁻ 는 **탈리튬 NCM 과 LPSCl 의 확산 지배 반응** 산물(refs 46, 47 = Zuo 2023 Angew).
- 시야가 커서 **NCM85 입자(D50 5 µm) 다수 · SE–CAM 계면 다수**를 포함 → 편향 최소화 주장.

### 5.11 FIB-SEM (`Fig. S9`)
200 cyc 후 단면. **bare·coated 둘 다 CAM 입자 균열**(입자 중심에서 방사상, ref 48 과 정합)이지만 **coated 가 확연히 덜하다**. 저자 해석: **얇은 코팅이 부피변화를 기계적으로 흡수하는 건 아니고**, 계면 부반응·O₂ 방출을 줄인 결과로 균열이 완화된 것.

---

## 6. 메커니즘 종합

```
LiPO₂F₂ (용액 코팅, 100 °C)
   │ 코팅 중 이미 부분 분해  → 표면: LiPOF + Li_xP_yF_z + 소량 LiF     (Fig S2)
   │
   ├─ 사이클 중 4.3 V:  DFT ③ ⇒ LiPO₃ + P₂O₃F₄ (+SOCl₂ 는 속도론 배제)  (Fig 1d)
   ├─ 방전 2.8 V:      P₂O₃F₄ 리튬화 ⇒ "비정질 LiPₓOᵧF_z"              (Fig 1d 해석)
   └─ 200 cyc 후 실제: LiPₓOᵧF_z + LiF (690 eV Li_xP_yF_z 소멸)        (Fig 4c)
                          ↓
        전자 절연·고전압 안정 CEI (LiF 8.7 eV / LiCl 6.3 / Li₃PO₄ 5.8 eV gap)
                          ↓
        LPSCl 이 NCM 표면에서 산화될 경로 차단
                          ↓
   S 2p S⁰ 소멸(Fig 4b) · SOₓ⁻ 급감(Fig 5) · R_cathode 200→90(Fig 4a)
                          ↓
        용량·율속·수명 개선 (Fig 3) + 균열 완화 (Fig S9)
```

**논증 흐름**
1. 문제 = SE 산화(2.5 V) ↔ 고Ni 작동(4.3 V) 불일치.
2. 선례(LiPON)로부터의 착상 = **분해산물의 창**이 실효 창을 정한다.
3. 후보 LiPOF 를 hull 3종으로 심사 → 자체 창 2.6–4.9 V, SE 와의 산물이 LiF/LiPO₃/LiCl/Li₄P₂O₇ 로 좋고 \|ΔE_rxn\|<100 meV/atom.
4. 값싼 용액 코팅으로 구현(30 nm 비정질).
5. 첫 사이클에서 argyrodite 산화 신호(3.5 V 이하 sloping, dQ/dV 혹) **소멸**.
6. 200 cyc 후 XPS 로 **예측 산물(LiF·LiPₓOᵧF_z) 검출** + **산화-S 부재**, ToF-SIMS 로 **SOₓ⁻ 감소**, EIS 로 **R_cathode 반감**.
7. 결론 = "코팅은 그 자체가 아니라 **깨져서 무엇이 되는가**로 설계하라."

---

## 7. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1a | LiPO₂F₂ 의 **grand-potential element profile** — Li/f.u. vs 인가전압(0–7 V) 계단. 초록 = 창 **2.6–4.9 V**; 아래 LiF/Li_xP/LiP_yO_z, 위 P₂O₃F₄/Li_xO | 우리 `esw_grand_potential.py` 출력과 **동일 그림 문법**. 우리 staircase 플롯(`plot_esw_staircase.py`)의 외부 서식 견본 |
| 1b | **닫힌 계** pseudo-binary `x·LPSCl+(1−x)·LiPOF` ΔE_rxn(x) — 최저 −145 meV/atom @x=0.52 → Li₃PO₄+LiF+LiCl+P₂S₅. x=1.0 회색 점선 = **LPSCl 자체 분해 −83 meV/atom** | 우리 `interface_reactivity.py`(OCV) 출력과 1:1. **끝점 규약 비교** 대상 — 우리는 hull-energy 규약이라 x=1 이 0 |
| 1c | 같은 계 **@2.8 V** — 최저 −43 meV/atom @x≈0.62 → LiPO₃+LiF+LiCl+P₂S₇ | 우리 `interface_reactivity_v2.py`(전압분해)와 **완전 동형**. 우리가 아직 안 돌린 "코팅\|SE" 축의 견본 |
| 1d | 같은 계 **@4.3 V** — 최저 −96 meV/atom @**x≈0.08** → LiPO₃+P₂O₃F₄+SOCl₂ | ⚠ 최소점이 x≈0.08(코팅 92 %)라 **물리적 계면 화학량론과 거리가 멀다** — 우리 v2 결과 해석 시 같은 함정 경고 |
| 1e | **NCM\|LiPOF @2.8 V** — 최저 ≈−395 meV/atom @x≈0.41 → CoO+NiO+Li₃PO₄+LiF | 우리 cathode 축 값(LiCoO₂\|comp1 −323 meV/atom)과 **같은 자릿수**. 코팅도 양극과는 크게 반응한다는 기준선 |
| 1f | **NCM\|LiPOF @4.3 V** — 최저 ≈−108 meV/atom @x≈0.61 → Li₂NiF₄+CoO₂+MnO₂+Ni₃(PO₄)₂ | 고전압에서 **F 가 TM 으로 옮겨간다**(Li₂NiF₄) — 우리 F 함유 도판트 검토 시 경고 사례 |
| 2a–c,e–g | SEM(4 µm 구형) · HRTEM(**~35 nm 비정질 conformal**) · STEM-EDX(P/O/F/Ni/Mn/Co) | 코팅 두께 스케일 기준선. ⚠ EDX 는 **Li 를 못 본다** — "Li·P·O·F 균일" 주장의 한계 |
| 3a,b | 초기 충방전(**ICE 64.6→81.6 %**, bare 첫충전 ≈270 mAh/g) + dQ/dV(bare 만 **3.0–3.2 V "Argyrodite decomposition"** 혹) | ⭐ **"SE 산화량 = 첫 충전 잉여용량"** 의 깔끔한 실측. 우리 grand-potential onset 2.256 V 가 **실제로 셀에서 어떻게 보이는가**의 그림 |
| 3c–e | 율속(0.1–2 C) · 200 cyc 수명(**81.4 vs 56.0 %**) · 고로딩 25.6 mg/cm² **4.4 mAh/cm² 77 %** | 코팅 문헌 벤치마크 수치 |
| 4a | **TLM 등가회로 + `R_cathode = √(R_int·(R_ion+R_e))`** + Nyquist(**200 → 90 Ω·cm²**) | ⭐ 우리 `kim2025_impedance_decoupling_tlm_assb` 축의 실사용 예. 공식 자체가 인용 가치 |
| 4b | S 2p — coated 는 **163.2 eV S⁰ 거의 0**, bare 는 S⁰ + thiosulfate + polythionate | ⭐ 우리 `xps_reference_sei.csv` anchor 와 **160.2 / 161.6 / 163.2 eV 3점 일치**. thiosulfate·polythionate 는 추가 anchor 후보 |
| 4c | F 1s — coated 200 cyc 후 **LiPₓOᵧF_z(688.3) + LiF(684.9)**, bare 는 무신호 | DFT 예측 산물의 실험 확증 방식(예측→BE 앵커→검출) 견본 |
| 5 | ToF-SIMS **SO⁻/SO₂⁻/SO₃⁻** heat map 6장, 200×200 µm², 동일 컬러스케일 | ⭐ `[Zuo]`/`[Qian26]` 와 **3편째 동일 종(SOₓ⁻) 관측** — 우리 interface_reactivity 산물의 실험 대조축. ⚠ bare 맵은 **포화** |
| S1 | FTIR — P–O 1273/1163, P–F 934/887 cm⁻¹ | 코팅 존재 확인 분광 앵커 (우리 Raman/IR 대조용) |
| S2 | F 1s **사이클 전** — LiPOF 단독은 688.3 단일, 코팅 NCM 은 **690.2(Li_xP_yF_z)+688.1+684.9** | ⭐ **코팅은 도포 단계에서 이미 분해돼 있다**는 직접 증거 (본문 서술보다 강함, §13 ⑥) |
| S3, S4 | XANES Ni L-edge · XRD — 벌크 R3̄m 불변 | 코팅이 벌크를 안 건드린다는 표준 대조 |
| S5, S6 | 무코팅 SEM · 추가 HRTEM/STEM-EDX | — |
| S7 | **2 wt% 코팅** 80 cyc 92 %, 초기 ≈167 mAh/g, ICE ≈78.6 % | ⭐ **코팅 두께 최적점이 존재**한다는 실측 (1 wt% 승) |
| S8 | P 2p 3단 — 미사이클 코팅(P–F/P–(OF)) / 사이클 코팅(P–F_x·P–Oₓ·**PS₄³⁻ 지배**) / 사이클 무코팅(**P–Oₓ 우세**) | ⭐ POₓ/PS₄³⁻ 비 = 우리 O-도핑 서사의 **133.3 vs 131.7 eV** 전환 앵커와 같은 축 |
| S9 | FIB 단면 — 균열이 coated 에서 덜함 | 화학 억제가 기계적 열화를 줄인다는 연결고리 (우리 chemo-mech 축) |
| Table S1 | 계면 산물 14종의 **전압창 + band gap** | ⭐⭐ **§10-C 참조** — 우리 `sei_products.json` gap 표와 직접 대조 가능한 외부 표 |

## 8. Post-processing ★

- **무엇**: ① grand-potential **element profile**(ESW) ② **닫힌 계 pseudo-binary 계면반응** ③ **grand-potential 계면반응**(μ_Li 고정) ④ 산물의 **band gap 조회**(Table S1). NEB·Bader·COHP·DOS·ELF·phonon·MD **전부 없음**.
- **도구**: **VASP**(에너지) + **pymatgen**(상평형·element profile·계면반응) + **Materials Project DB**(참조상) + **ICSD**(보충 구조).
- **수치화·플롯 방식**: 계면반응은 전부 **ΔE_rxn(meV/atom) vs 혼합분율 x** 산점+선. **최소점에 금색 별**, 각 kink 에 **화살표+산물 텍스트**. 전압 케이스는 패널 안에 **"at 2.8 V" / "at 4.3 V"** 라고만 적는다. element profile 은 **Li/f.u. 계단 + 창 색칠 + 양끝 산물 라벨**.
- **기록 방식**: 수치를 **표로 주지 않는다** — 본문에 x=0.52 하나, "<100 meV/atom" 하나뿐. **나머지 ΔE_rxn 값은 전부 그림에서 읽어야 한다**(그래서 이 digest 의 §3a 는 대부분 `figure-read ≈`). 산물의 창·gap 만 Table S1 로 표화.
- 실험 후처리: **RelaxIS**(EIS 피팅, TLM blocking-boundary), **Athena**(XANES 정규화), **GMS Digital Micrograph**(FFT·d-spacing), ToF-SIMS **전 이온 정규화**.

---

## 9. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`

| 항목 | 이 논문 | 우리 | 같나/다르나 · 왜 |
|---|---|---|---|
| **계면반응 방법** | pymatgen `InterfacialReactivity` + `GrandPotentialInterfacialReactivity`, MP hull, meV/atom | `tools/oxidation/interface_reactivity.py`(OCV) + `interface_reactivity_v2.py`(전압분해), pymatgen, MP **GGA/GGA+U** hull, `use_hull_energy=True`, eV/atom | ✅ **완전 동일 기계**. 우리 v2 docstring 이 인용하는 원전(**Richards/Ong 2016**)이 이 논문 ref [7] 과 같다 |
| **ESW 방법** | `get_element_profile`, Li 열림, 창을 "hull 위에 남는 전압구간"으로 정의 | `esw_grand_potential.py` — 동일 함수·동일 정의, μ_Li ref −2.3867 eV, φ 0–5 V, dφ 0.02 V | ✅ 동일 |
| **LPSCl 자체 산화 onset** | 명시 계산 **없음** — 본문은 문헌값 *"~2.5 V"* 를 전제로만 씀 | **2.256 V**(LiS₄ 제외 GG set) / 2.14 V(포함) | ⚠ **비교 불가** — 저자가 자기 hull 로 LPSCl onset 을 안 냈다. "2.5 V" 는 그들의 계산이 아니라 인용 |
| **LPSCl E_above_hull** | **≈ −83 meV/atom**(figure-read, → Li₃PS₄+Li₂S+LiCl) | **0 by construction** — 우리는 `energy_mode: hull`(조성의 MP convex-hull 에너지 = ideal line phase)을 쓴다. 참고로 MP 실엔트리 `mp-985592-GGA` 는 e_above_hull **1.5663 eV/atom**(무질서 미보정 인공물) | ❌ **규약이 다르다.** 그들의 −83 은 "그들이 쓴 LPSCl 구조 1개"의 hull 위 높이. **어느 S/Cl 배열인지 안 적혀 있어 이식 불가** |
| **LPSCl 분해 산물** | Li₃PS₄ + **Li₂S** + LiCl (x=1) | `interface_reactivity_results.json` x=1.0 kink: `Li6PS5Cl -> Li3PS4 + Li2S + LiCl` | ✅ **완전 일치** (독립 재현) |
| **양극 계면 반응 크기** | NCM\|LiPOF @2.8 V **≈ −395 meV/atom** | LiCoO₂\|comp1 **−323 meV/atom**, LiCoO₂\|modelc **−331** | ≈ 같은 자릿수. ⚠ **양극도 계도 다르므로 값 대조 금지**, "수백 meV/atom 급"까지만 |
| **SE\|양극 산물** | (그들은 SE\|양극을 안 돌림) | comp1\|LiCoO₂ → Co₉S₈ + Li₂SO₄ + **Li₃PO₄** + Li₂S + **LiCl** | — |
| **공통 산물** | **Li₃PO₄ · LiCl** | 동일 2종 | ✅ 산물 어휘 겹침 |
| **산물 band gap 규약** | Table S1, MP 계열 GGA gap. LiCl **6.3** / Li₃PO₄ **5.8** / LiF **8.7** | `sei_products.json`(MP PBE/PBE+U 최저 e_above_hull 엔트리). LiCl **6.65** / Li₃PO₄ **5.73** / Li₂S 3.90 / Li₃P 0.70 | ⚠ **같은 방법 이름, 다른 값**(LiCl 6.65 vs 6.3 = 0.35 eV) → **MP 버전/엔트리 차이**. 절대값 혼용 금지, "wide-gap" 계급만 |
| **절연/전도 문턱** | 명시 없음 (그냥 "low electronic conductivity") | 우리 규약: **절연 ≥4 eV / marginal 2–4 / 전도 <2 eV** | ⚠ 우리 문턱으로 재면 그들의 **LiPO₃(2.5)·P₂S₅(2.6)·P₂S₇(2.1)** 은 **marginal**, CoO/CoO₂/MnO₂(0.5–0.6)는 **전도체** (§13 ①) |
| **무질서 처리** | ⛔ 서술 없음 | 우리도 argyrodite 는 배열 의존이 크다는 걸 안다(gap ±0.2–0.3 eV) | ⚠ 양쪽 다 약점. 그들은 **약점을 적지도 않았다** |
| **functional 명시** | ⛔ 없음 ("MP 파라미터와 일치") | 우리 hull 은 **MP GGA_GGA+U thermo_type 명시** | ❌ 그들이 못 적은 것 — 우리 쪽이 재현성 우위 |
| **실험 검증** | XPS·ToF-SIMS·EIS·TEM 다층 | 우리는 실험 0 (문헌 대조만) | 그들 우위 |

**판정 요약** — *진짜 차이 vs 방법 인공물*
- ✅ **진짜 일치**: LPSCl → Li₃PS₄+Li₂S+LiCl 분해식, 계면 산물 어휘(Li₃PO₄·LiCl), 방법 골격.
- ⚠ **방법 인공물 의심 (수치 이식 금지)**: LPSCl E_above_hull −83 meV/atom(구조·배열 미기재), Table S1 gap 값(MP 버전 드리프트), NCM 조성 불일치(0.83 vs 0.85).
- ❌ **비교 자체가 성립 안 함**: 이 논문의 산화 onset — **자기 계산이 없다**.

---

## 10. ★★ 우리가 활용할 수 있는 부분 (1저자 지정 절)

### A. convex hull — 이 논문이 실제로 한 것의 해부

**A-1. 어떤 화학공간에서, 어떤 참조상으로 hull 을 쳤나**

| 계산 | 화학공간(원소 축) | 참조상 집합 |
|---|---|---|
| `Fig. 1a` (LiPOF 창) | **Li–P–O–F** (4원) | MP 의 Li–P–O–F 전 화합물 + **ICSD 추가 구조 자체계산** + **LiPO₂F₂ 자체계산** |
| `Fig. 1b–d` (SE\|코팅) | **Li–P–S–Cl–O–F** (6원) | 위 + S·Cl 계 (⛔ **출처 미기재**, MP 추정) |
| `Fig. 1e,f` (양극\|코팅) | **Li–Mn–Co–Ni–O–P–F** (7원) | 위 + Ni·Co·Mn 계 (⛔ **출처 미기재**) |

- **참조상을 "다 넣었다"고만 하고 목록·개수·MP 버전을 안 준다.** 4원 → 6원 → 7원으로 공간을 키우면 hull 이 새 상에 의해 재구성되는데, 그 상들이 어디서 왔는지가 안 적혀 있다. **재현하려면 우리가 MP 를 다시 쿼리해야 한다.**

**A-2. E_hull / ΔE_rxn 의 정의·단위·기준**
- 단위는 전부 **meV per atom** (모든 그림 y축). f.u. 당이 아니다.
- **ΔE_rxn(x)** = `x·P1 + (1−x)·P2 → P3` 의 **원자당 반응에너지**, x 는 **혼합 분율**(그림 x축이 곧 x). 음수 = 발열 = 반응성 큼.
- **끝점 규약**: `Fig. 1c–f` 는 x=0, x=1 에서 0 → **각 끝점을 자기 hull 로 평형화한 상태 기준**(pymatgen `use_hull_energy=True` 와 동치). `Fig. 1b` 만 x=1 을 −83 에 두고 "미분해 LPSCl → 0" 을 회색 점선으로 따로 표기.
- **functional / U**: ⛔ **미기재**. "MP 파라미터 일치"만 → 사실상 PBE + MP 의 GGA/GGA+U 혼합 스킴으로 읽어야 하지만 **논문이 그렇게 쓰지 않았다.**
- **에너지 보정**: ⛔ 미기재 (MP2020Compatibility 언급 0). **황화물+산화물+불화물 혼합 hull 에서 이게 빠지면 값이 크게 흔들린다.**

**A-3. 분해생성물 후보를 어떻게 열거했나 / 무엇을 "안정" 으로 판정했나**
- **열거 = 열거하지 않았다.** hull 위 상들의 조합을 **pymatgen 이 자동으로 낸다**(사람이 후보 목록을 쓰지 않는다). x 를 훑으며 각 kink 의 평형상 세트를 읽는 방식.
- **"안정" 판정 3층**:
  1. **자체 창** — `Fig. 1a` 에서 화합물이 **hull 위에 남는 전압 구간**(LiPOF: 2.6–4.9 V). 여기엔 문턱이 없다(hull 위/아래 = 이진).
  2. **화학 반응성** — **\|ΔE_rxn\| < 100 meV/atom** 이면 *"낮은 화학반응성의 지표"*. 본문이 ref [7] 을 단다.
  3. **산물의 질** — Table S1 의 **전압창이 작동창을 덮고 band gap 이 크면** 부동태화 산물로 인정. **정량 문턱은 없다** (LiPO₃ 2.5 eV 도 통과시킨다).
- ⚠ **문턱 100 meV/atom 의 귀속**: 우리가 실물 검증한 digest 기준으로 **`[Rich16]` 의 100 meV/atom 은 "무시한 계면에너지의 상한"**(Δγ 0.5 J/m², 원자층 두께)이고, **반응성 게이트로서의 \|ΔE_rxt\|<100 meV/atom 은 `[Xiao19]` filter 4**(= 이 논문의 ref [33])다. 숫자와 계보는 맞지만 **인용이 한 편 어긋나 있다.**
  🔑 그리고 이 우연의 일치가 우리에게 주는 교훈: **100 meV/atom 은 동시에 "게이트"이자 "우리가 무시한 항의 크기"** 다 → **게이트 바로 위/아래 물질의 순위는 근사 안에 있다** (우리 `[Rich16]` digest §16 규율과 동일).

**A-4. 전압과 hull 을 어떻게 엮었나**
- **grand-potential hull 이다** (단순 반응 hull 아님). μ_Li 를 Li 저장고로 열고 **μ_Li = μ⁰_Li − eφ** 로 전압을 넣는다.
- 다만 **두 가지를 나눠 쓴다**:
  - `Fig. 1b` = **닫힌 계**(전위 무인가) — 저장고 없음, 조성 보존.
  - `Fig. 1c–f` = **grand-potential** — μ_Li 를 **2.8 V / 4.3 V 두 점에만** 고정. **연속 스캔이 아니다** (우리 v2 는 전압축을 훑는다 → 우리 쪽이 정보량 많음).
- `Fig. 1a` 는 계면반응이 아니라 **단일상 element profile** — 같은 grand-potential 이지만 혼합 축이 없다.

**A-5. 데이터 출처**
- **Materials Project** (Li–P–O–F 확정, 나머지 원소는 미기재) + **ICSD**(추가 구조를 자체 계산) + **LiPO₂F₂ 자체 계산**.
- **버전·API·pseudopotential·U 값 전부 미기재.** ⇒ **이 hull 은 논문 정보만으로 재현 불가**다.

### B. 🟢 우리 계에 **그대로 옮길 수 있는 것**

| # | 옮길 것 | 어디에 |
|---|---|---|
| B-1 | **"코팅은 자신이 아니라 분해산물로 심사한다"는 설계 원리** — 세 계산(자체 창 / SE 혼합 / 양극 혼합)을 한 세트로 돌리는 절차 | 우리 SE 도판트·코팅 cascade 의 **게이트 설계**. 우리는 이미 ESW+interface_reactivity 를 갖고 있으니 **"산물 창·gap 조회"만 붙이면 이 논문의 전 절차가 완성**된다 |
| B-2 | **두 전압점(하한 2.8 V / 상한 4.3 V)에서 계면반응을 각각 돌리는 관행** | 우리 `interface_reactivity_v2.py` 는 전압축을 훑는데, **논문 그림용으로는 2점 스냅샷이 훨씬 읽기 쉽다**. 우리 그림 서식에 채택 가능 |
| B-3 | **끝점 hull-평형 규약**(x=0,1 에서 ΔE_rxn=0)과 그것을 **회색 점선으로 따로 보여주기** | 우리 `plot_interface_reactivity_v2.py` 에 "미분해 상태 → 분해 상태" 화살표 추가 = 독자가 hull 규약을 오해하지 않게 하는 장치 |
| B-4 | **\|ΔE_rxn\| < 100 meV/atom 게이트** (단, 출처는 `[Xiao19]` 로 적을 것) + **"게이트 근처는 순위 금지"** 규율 | 우리 cascade 게이트 문서 |
| B-5 | **LPSCl → Li₃PS₄ + Li₂S + LiCl (닫힌 계, x=1)** 라는 분해식의 **외부 독립 재현** | `comparison_vs_ours.md` B③ — 우리 `interface_reactivity_results.json` 과 문자 그대로 일치 |
| B-6 | **XPS BE 앵커 5점**: S 2p₃/₂ **160.2(free S²⁻) / 161.6(PS₄³⁻) / 163.2(S⁰)**, F 1s **688.3(LiPₓOᵧF_z) / 684.9(LiF)**, + **690.2(Li_xP_yF_z)**, P 2p₃/₂ **133(LiPO₃≈Li₃PO₄) / 132.0(PS₄³⁻) / 134.2(P–(OF)) / 136.2(P–F)** | 우리 `db/properties/xps_reference_sei.csv` 에 **F 1s·P–F 계열 신규 anchor 추가** (S/P 3점은 이미 일치 → 교차검증) |
| B-7 | **`R_cathode = √(R_int·(R_ion + R_e))`** (TLM blocking-boundary) 와 그 출처 ref [43] Kochetkov 2022 EES | 우리 임피던스 축(`kim2025_impedance_decoupling_tlm_assb`) 문서의 공식 앵커 |
| B-8 | **셀 조건 세트**: SE:CAM **2:8 wt**(카본 없음), 펠릿 250 MPa, 양극 200 MPa, 스택압 200 MPa, 1 C = 200 mA/g, EIS 100 mHz–1 MHz @25 °C | 우리 DEM/디지털트윈 축의 **실셀 파라미터 기준값** |
| B-9 | **"첫 충전 잉여용량 = SE 산화량"** 판독법 (bare 270 vs coated 222 mAh/g ⇒ ≈48 mAh/g) | 우리 grand-potential onset(2.256 V)이 **셀에서 어떤 관측량으로 나타나는가**를 잇는 다리 |
| B-10 | **코팅 두께 최적점이 존재**(1 wt% > 2 wt%: 용량·ICE 손해) | 우리 `[BZOx]`/`[Cha]`/`[Kang25]` 코팅 라인의 공통 서사 보강 |

### C. 🔴 옮기면 **안 되는 것** (+ 왜)

| # | 금지 | 왜 |
|---|---|---|
| C-1 | **LPSCl E_above_hull ≈ −83 meV/atom 을 우리 값으로 쓰기** | 우리는 `energy_mode: hull`(조성의 hull 에너지, e_above_hull ≡ 0)을 쓴다. 그들은 **특정 LPSCl 구조 1개**의 에너지를 썼는데 **어느 S/Cl 배열인지 안 적었다**. argyrodite 는 배열 하나로 수십 meV/atom 이 움직인다 → **정의도 구조도 달라 이식 불가**. |
| C-2 | **Table S1 의 band gap 을 우리 `sei_products.json` 표에 섞기** | 같은 "MP GGA gap" 이름인데 **LiCl 6.3 vs 우리 6.65** 로 0.35 eV 어긋난다 = **MP DB 버전/엔트리 차이**. 절대값 혼용 금지, **"wide-gap(≥4 eV) 계급"** 수준까지만. |
| C-3 | **Table S1 의 전압창을 우리 ESW 표에 붙이기** | 출처가 **혼합**이다 — 일부는 refs 7/32/33 소환값, 일부는 자체 DFT 추정이고 **어느 것이 어느 것인지 SI 가 매핑을 안 준다**. 우리 `esw_*.json` 은 단일 규약(MP2020, LiS₄ 제외 GG set)이라 **섞으면 규약이 오염된다**. |
| C-4 | **ΔE_rxn 값을 우리 값과 직접 대소 비교** | ① functional·U·보정 미기재 ② MP 버전 미기재 ③ **끝점 규약이 Fig 1b 와 1c–f 사이에서도 다르다** ④ 우리 v2 는 GGA_GGA+U thermo_type 을 명시 고정. → **자릿수(수백 meV/atom vs 수십)까지만** 대조. |
| C-5 | **NCM 조성을 "NCM85" 로 인용** | DFT 입력은 `Fig. 1e,f` x축의 **LiMn₀.₀₈₃Co₀.₀₈₃Ni₀.₈₃O₂** 이고 실험 CAM 은 **LiNi₀.₈₅Mn₀.₁Co₀.₀₅O₂** 다. **Co 가 0.083 vs 0.05 로 1.7배 다르다** — Fig 1e 의 CoO 예측을 실험 NCM85 에 그대로 옮기면 과대. |
| C-6 | **"LiPOF 는 2.6–4.9 V 안정" 을 우리 SE 도판트/코팅 비교표에 넣기** | 그건 **Li–P–O–F 4원 hull 위 단일상 창**이다. 우리 표의 창들은 **각자 다른 화학공간**에서 나왔다. 창끼리 비교하려면 **같은 hull·같은 참조상 집합**이어야 한다. |
| C-7 | **"산물이 전자절연이라 부동태화" 를 이 논문 근거로 인용** | 그들 자신의 Table S1 이 **LiPO₃ 2.5 · P₂S₅ 2.6 · P₂S₇ 2.1 · CoO/CoO₂ 0.6 · MnO₂ 0.5 eV** 를 준다. 우리 문턱(절연 ≥4 eV)으로는 **절반이 절연체가 아니다**. 전자절연 주장을 떠받치는 건 **LiF(8.7)·LiCl(6.3)·Li₃PO₄(5.8)** 셋뿐. |
| C-8 | **SDCP 바인더 축으로 옮기기** | 유기 고분자는 **MP hull 밖**이다 (`[Qian26]` 에서 이미 같은 판정). 이 논문의 hull 도구는 **무기 결정상 전용** — SDCP 흡착·기계 축에는 아무 것도 못 준다. ⛔ 우리 `estimand_card` 규율상 "다른 보고량"이다. |
| C-9 | **LiNiO₂(104) 슬랩 축으로 옮기기** | 이 논문에 **슬랩·표면·흡착 계산이 0** 이다. 전부 **벌크 0 K 상평형**. 표면에너지·흡착에너지·표면 재구성 어느 것도 이 논문에서 나올 수 없다. 슬랩 대조군이 필요하면 `[Qian26]` Table S2(LPSCl 저지수 슬랩 표면E)로 가야 한다. |
| C-10 | **"코팅이 LPSCl 산화 onset 을 올렸다" 로 읽기** | 저자 주장은 **onset 이동이 아니라 접근 차단**이다. 우리 축 언어로는 **B①(intrinsic onset) 불변 · B③(계면 산물) 이득**. `[Qian26]`·`[Deng26PS]` 와 같은 결론. |

### D. 그 밖에 우리가 바로 쓸 수 있는 것 (실험 대조축)

- **계면 분해생성물 목록 (이 논문이 예측한 전부)** — 우리 산물 사전에 합칠 후보:
  - LPSCl\|LiPOF: **Li₃PO₄, LiF, LiCl, P₂S₅, Li₄P₂O₇, LiPO₃, P₂S₇, P₂O₃F₄, SOCl₂**
  - NCM\|LiPOF: **CoO, NiO, Li₃PO₄, LiF, Li₂NiF₄, CoO₂, MnO₂, Ni₃(PO₄)₂**
  - LPSCl 단독: **Li₃PS₄, Li₂S, LiCl** ← 우리와 1:1 일치
- **ToF-SIMS 종 (SO⁻/SO₂⁻/SO₃⁻)** — `[Zuo]`·`[Qian26]` 과 **3편 독립 관측**. 우리 interface_reactivity 산물(Li₂SO₄ 등)의 실험 대응.
- **셀 성능 벤치마크 표** (§3b) — 우리 코팅/도핑 제안의 "이 정도는 나와야" 기준선.
- **"자기제한 반응" 서술의 반례로서의 가치** — −395 meV/atom 을 "속도론이 막는다"로 넘기는 방식은 **우리가 하면 안 되는 논증**의 견본이다(§13 ⑤).

---

## 11. 적용 인사이트 (우리 연구에 어떻게)

1. **우리 cascade 에 "산물 심사" 층을 하나 더 붙일 수 있다.** 지금 우리 게이트는 (상안정 hull → ESW → 계면반응)인데, 이 논문은 거기에 **"나온 산물 각각의 창·gap 을 다시 조회"** 를 얹었다(Table S1). 우리는 `sei_products.json` 에 이미 그 조회 결과를 갖고 있으므로 **연결만 하면 된다** — 새 도구 불필요(코드 규율 사다리 ③ "기존 도구에 플래그").
2. **우리 v2(전압분해)가 이 논문보다 정보량이 많다.** 그들은 2.8/4.3 V **두 점**만 찍었다. 우리는 전압축을 훑는다 → **"어느 전압에서 산물 세트가 바뀌는가"(kink 전압)** 를 낼 수 있고, 그건 이 논문이 못 낸 값이다. **우리 그림의 차별점으로 쓸 수 있다.**
3. **B③ 축의 4번째 레버가 확정됐다.** 우리 `comparison_vs_ours.md` B③ 은 이미 [Zuo](조성) / [Kang25](SE 코팅) / [Cha](할라이드 코팅) / [BZOx](양극 산화물 코팅) / [Qian26](SE 유기코팅)을 갖고 있다. 여기에 **[Qian25] = 양극 입자 무기-염 코팅(용액·무소결)** 이 붙는다. **레버가 다섯 개인데 B① onset 은 다섯 편 모두 안 움직인다** — 이 관찰 자체가 우리 서사의 강한 문장이다.
4. **"F 를 계면에 넣는 것"의 양면**: LiF(8.7 eV gap)는 최고의 절연 CEI 지만, `Fig. 1f` 는 4.3 V 에서 **F 가 TM 으로 이동해 Li₂NiF₄** 를 만든다고 예측한다. 우리가 F 도판트를 검토할 때(cascade 의 F 계열) **"고전압에서 F 가 TM 불화물로 갈아탄다"** 를 반드시 게이트에 넣어야 한다.
5. **재현성 규율의 반면교사.** 이 논문의 계산 절은 **11줄**이고 functional·U·보정·구조·무질서가 전부 빠져 있다. 우리 `estimand_card` 규율(보고량 정의 → 상태 선택 규칙 → 게이트)로 보면 **"admissible state 가 여럿인데 선택 규칙이 없다"**(argyrodite S/Cl 배열, NCM 고용체 배열)에 정확히 해당한다. 우리 원고 SI 는 이 수준이면 안 된다.

## 12. 인용 가능 문장 (deck / 원고용)

- "Qian et al. (Angew. 2025) 은 코팅 물질을 **그 자체의 안정성이 아니라 분해산물의 안정성**으로 선별하는 절차를 제시했다 — LiPO₂F₂ 의 grand-potential 창(2.6–4.9 V vs Li⁺/Li)과 Li₆PS₅Cl 과의 계면반응(2.8 V 에서 −43, 4.3 V 에서 −96 meV/atom, 둘 다 100 meV/atom 미만)을 근거로 삼았다."
- "같은 pymatgen 계면반응 계산이 **Li₆PS₅Cl → Li₃PS₄ + Li₂S + LiCl** 를 독립적으로 재현했다 (우리 `interface_reactivity_results.json` x=1 kink 와 문자 그대로 일치)."
- "코팅은 argyrodite 의 **산화 개시 전압을 옮기지 않는다** — 첫 충전의 3.5 V 이하 sloping 구간과 dQ/dV 의 3.0–3.2 V 혹이 사라지는 것은 **분해 경로가 차단**된 결과이고, ICE 는 64.6 → 81.6 %, 200 사이클 유지율은 56.0 → 81.4 % 로 개선된다."
- "200 사이클 후 F 1s XPS 에서 **LiF(684.9 eV)와 LiPₓOᵧF_z(688.3 eV)** 가 검출되어, 4.3 V 계면반응이 예측한 P₂O₃F₄ 의 방전 시 리튬화 산물 가설을 지지한다."
- ⚠ 인용 금지: "LiPO₂F₂ 코팅이 황화물의 산화창을 넓힌다" — **저자도 그렇게 주장하지 않는다**.

## 13. 주의 / 한계 (비판 — over-claim 방지)

① **"분해산물이 전자절연" 주장을 자기 표가 절반만 지지한다.** Table S1 의 LiPO₃ **2.5** · P₂S₅ **2.6** · P₂S₇ **2.1** eV 는 우리 문턱(절연 ≥4 eV)으로 **marginal** 이고, NCM 쪽 산물 CoO/CoO₂ **0.6** · MnO₂ **0.5** eV 는 **전도체**다. 그런데 `Fig. 1c`(2.8 V) 의 대표 산물 세트에 **P₂S₇(2.1 eV)** 이 들어 있다. 전자절연 서사를 떠받치는 건 **LiF·LiCl·Li₃PO₄** 셋뿐이다. 인용 시 **"LiF/LiCl/Li₃PO₄ 가 절연"** 으로 좁혀 써야 한다.

② **계산 절이 재현 불가능하다.** functional·U·PAW·MP 버전·에너지 보정(MP2020Compatibility)·구조 출처·무질서 처리가 **전부 미기재**. 특히 **S/O/F 를 한 hull 에 섞으면서 음이온 보정 언급이 없는 것**은 이 방법론에서 무거운 누락이다.

③ **작동창의 하단 여유가 0.2 V 뿐이다.** LiPOF 안정창 하한 **2.6 V** vs 방전 하한 **2.8 V**. 그리고 `Fig. 1a` 는 창 아래에서 코팅이 **~8 Li/f.u. 를 흡수**한다고 예측한다 — 국소 과전압·불균일 전위분포에서 코팅이 Li 싱크가 될 위험을 논문이 논의하지 않는다.

④ **"<100 meV/atom" 은 전압 건 경우에만 성립한다.** `Fig. 1b`(무인가) 최저점은 **−145 meV/atom** 으로 자기 문턱을 넘는데, 본문은 "In both cases"(= 2.8/4.3 V) 로 범위를 좁혀 말하고 1b 의 초과는 언급하지 않는다.

⑤ **양극과의 −395 meV/atom 을 "속도론이 막는다"로 넘긴다.** 자기 게이트의 **4배**인데 계산적·실험적 근거 없이 *"검출 안 됐으니 자기제한적일 것"* 이라고만 쓴다. **검출 한계(XPS ~0.1–1 at%, 30 nm 층)** 를 제시하지 않았으므로 "없다"가 아니라 "못 봤다"다. 우리가 같은 논증을 하면 안 된다.

⑥ **본문 서술이 자기 그림보다 약하다(F 1s).** 본문은 *"코팅 전후 물질이 **대부분 LiPOF 와 LiPₓOᵧF_z**"* 라고 쓰는데, `Fig. S2` 에서 코팅 시료의 **가장 큰 단일 성분은 690.2 eV 의 Li_xP_yF_z** 이고 이건 순수 LiPO₂F₂ 기준시료에 **없는** 피크다. 즉 **코팅은 도포 단계에서 이미 상당히 분해돼 있다** — 논문 주제(분해산물 설계)에는 오히려 유리한 사실인데 본문이 축소해 썼다.

⑦ **Fig 3 캡션이 패널과 어긋난다 (인용 시 주의).** 캡션은 *"a) Rate performance, b) 초기 충방전, c) dQ/dV"* 라고 쓰지만, **실제 그림은 a) 초기 충방전, b) dQ/dV, c) rate** 다(본문 서술이 맞다). 또 `Fig. 1` 캡션은 *"e) … at e) 2.8 and f) 4.3 V"* 로 e 가 중복 인쇄돼 있고, `Fig. 2` 캡션은 **패널 d(모식도)를 아예 빠뜨렸다**. **캡션 그대로 인용하면 틀린다.**

⑧ **숫자 내부 불일치 3건.** (i) 초록 **82 %** vs 본문·`Fig. 3d` 주석 **81.4 %**(81 %). (ii) 코팅 두께 본문 **25–35 nm** vs 도면 주석 **~35 nm** 2회(25 nm 근거 미제시). (iii) `Fig. 3e` 고로딩 200 cyc 잔량이 **figure-read ≈ 140 mAh/g**(173 대비 81 %)인데 본문은 **77 %**.

⑨ **문턱 인용이 한 편 어긋난다.** *"<100 meV/atom 이 낮은 화학반응성의 지표로 쓰여 왔다"* 에 **ref [7] = Richards 2016** 을 달았다. 우리 실물 검증 digest 기준으로 Richards 의 100 meV/atom 은 **무시한 계면에너지의 상한**이고, **반응성 게이트 100 meV/atom 은 [Xiao19](이 논문 ref [33]) filter 4** 다. (부수 서지 오류: ref [7] 페이지를 **255–273** 으로 적었는데 실물은 **266–273**.)

⑩ **ToF-SIMS 의 "semi-quantify" 주장에 숫자가 없다.** `Fig. 5` 의 bare SO₂⁻·SO₃⁻ 맵은 **컬러스케일 상단에서 포화**돼 있어 이미지에서 비율을 읽을 수 없고, 본문이 말하는 순위(SO₃⁻>SO₂⁻>SO⁻ 비율)의 **수치 표가 없다**. 순위 주장은 스펙트럼 기반일 텐데 그 데이터가 제시되지 않았다.

⑪ **EIS 조건 서술이 모순이다.** `Fig. 4` 캡션: *"EIS 는 매 사이클 **OCV(~3.7 V vs Li−In)** 에서, 셀을 **2.8 V 로 방전한 뒤** 기록"*. 2.8 V vs Li⁺/Li 로 방전했다면 OCV 는 **~2.2 V vs Li−In** 이어야 한다(3.7 V vs Li−In ≈ **4.3 V vs Li⁺/Li** = 만충). **R_cathode 90/200 Ω·cm² 는 "OCV 에서, 정확한 SOC 는 캡션상 불명"** 으로 인용해야 한다.

⑫ **DFT NCM ≠ 실험 NCM.** 계산은 **LiMn₀.₀₈₃Co₀.₀₈₃Ni₀.₈₃O₂**, 실험은 **LiNi₀.₈₅Mn₀.₁Co₀.₀₅O₂**. Co 함량이 **1.7배** 다른데 `Fig. 1e` 의 대표 산물에 **CoO** 가 들어 있다. 조성 불일치를 본문이 언급조차 하지 않는다.

⑬ **복합양극에 카본이 없다.** SE:CAM = 2:8 만. 카본이 없으면 SE 로의 전자 접근이 제한돼 **산화분해가 과소평가**될 수 있다. 반대로 `[Zuo]` 는 CV 에 **20 wt% C65** 를 넣어 분해를 증폭시켰다. **두 논문의 분해 "양" 을 직접 비교하면 안 된다.**

⑭ **코팅의 이온전도를 재지 않았다.** 저자 스스로 든 "이상적 코팅 4조건" 중 **③ 높은 이온전도**에 대한 데이터가 **하나도 없다**. 2 wt% 에서 용량이 떨어지는 것(`Fig. S7`)이 그 대가를 간접적으로 보여줄 뿐이다.

⑮ **비교 코팅(LiNbO₃ 등)을 직접 만들지 않았다.** 전부 **문헌 인용 비교**이고, 셀 구성·온도·로딩이 제각각(예: HfO₂ 는 **45 °C**). *"state-of-the-art 코팅보다 우수"* 라는 초록 문장은 **동일 조건 비교가 아니다**.

---

## 14. 기법 용어 미니사전 (이 논문을 읽는 데 필요한 것만)

- **convex hull (볼록 껍질)**: 어떤 화학공간(예: Li–P–O–F)에서 모든 알려진 화합물의 형성에너지를 찍고 그 **아래쪽 껍질**을 잇는 면. 껍질 **위(=on the hull)** 에 있으면 그 조성에서 열역학적으로 안정, 껍질보다 위에 떠 있으면(**E_above_hull > 0**) 분해할 구동력이 있다.
- **E_above_hull**: 그 화합물이 hull 보다 **얼마나 높이 떠 있나**(meV/atom). 0 = 안정. 이 논문 `Fig. 1b` 의 −83 meV/atom 이 곧 그들 데이터셋에서의 Li₆PS₅Cl 값.
- **grand potential (대정준 퍼텐셜)**: 계를 **Li 저장고**에 연결해 Li 를 자유롭게 주고받게 한 뒤(μ_Li 고정) 계산하는 열역학 퍼텐셜 Φ = E − μ_Li·N_Li. 전지에서 **전압 = μ_Li 를 조절하는 손잡이**(μ_Li = μ⁰_Li − eφ)라서, 전압을 걸었을 때의 안정성을 이걸로 잰다.
- **element profile**: μ_Li 를 훑으며 "이 조성이 hull 위에 남는가 / 몇 개의 Li 를 흡수·방출하는가"를 계단으로 그린 것. `Fig. 1a` 가 그것이고, 계단이 평평한 구간이 **전기화학 안정창**.
- **pseudo-binary 계면반응**: 두 상 P1·P2 가 임의 비율로 섞일 수 있다고 보고 `x·P1 + (1−x)·P2 → P3` 의 반응에너지를 **x 에 대해 최소화**하는 방식. 계면에서는 화학량론이 정해져 있지 않기 때문에 최악의 x 를 찾는다. 원전 = **Richards 2016**.
- **ΔE_rxn (meV/atom)**: 그 반응의 원자당 에너지. **음수 = 발열 = 반응이 일어난다**. 절대값이 클수록 계면이 불안정.
- **kink (꺾임점)**: ΔE_rxn(x) 곡선이 꺾이는 x. 그 지점에서 **평형 산물 세트가 바뀐다**. 그림의 파란 점들이 kink 다.
- **CEI (cathode–electrolyte interphase)**: 양극 표면에 생기는 계면상. 좋은 CEI = **전자는 막고 Li⁺ 는 통과**시키는 얇고 안정한 층.
- **ICE (initial coulombic efficiency)**: 첫 방전용량 / 첫 충전용량. 첫 충전에 SE 산화 같은 비가역 반응이 있으면 ICE 가 떨어진다 — 그래서 **ICE 가 SE 산화량의 대리 지표**가 된다.
- **TLM (transmission line model)**: 다공성 복합전극의 임피던스를 **이온 경로 사다리 + 전자 경로 사다리 + 그 사이의 계면 임피던스**로 모델링한 등가회로. 여기서 `R_cathode = √(R_int·(R_ion+R_e))`.
- **dQ/dV**: 용량을 전압으로 미분한 곡선. 상전이·산화환원이 **피크**로 보인다. bare 에서만 3.0–3.2 V 에 나타나는 혹이 argyrodite 분해.
- **H1→M, H2, H3**: 층상 고Ni NCM 이 탈리튬되며 겪는 상전이 이름. **H2→H3** 가 부피변화가 가장 크고 입자 균열의 주범.
- **ToF-SIMS**: 1차 이온빔으로 표면을 때려 튀어나온 2차 이온을 비행시간으로 질량분석. XPS 보다 **감도가 몇 자릿수 높고** 분자 조각(SO₂⁻ 등)을 본다. 대신 정량이 어렵다.
- **XANES**: 흡수단 근처 X선 흡수 스펙트럼 — 여기서는 **Ni 산화상태·국소구조**가 코팅으로 안 변했는지 확인용.

---

## 15. 관련 digest (교차참조)

- `richards2016_interface_stability_pseudobinary.md` — `Fig. 1b–f` 방법의 **원전** (이 논문 ref [7])
- `xiao2019_cathode_coating_screening.md` — **\|ΔE_rxt\|<100 meV/atom 게이트의 실제 출처** (이 논문 ref [33]); 코팅 후보 HT 스크리닝
- `zhu2015_esw_grand_potential_origin.md` — `Fig. 1a` element-profile 방법의 원전; Table S1 의 LiF/LiCl 창 계보
- `qian2026_decanoate_coating_lpscl_moisture_interface.md` — **같은 1저자**, 레버가 SE 입자 유기코팅(이 논문은 양극 입자 무기코팅)
- `zuo2022_chlorination_cathode_interface.md` — 같은 Nazar 공저, SOₓ⁻ ToF-SIMS 계보; **카본 20 wt% CV 라 분해량 직접비교 금지**
- `cha2024_dualcompatible_halide_ncm_lpscl_interface.md` · `kang2025_highvoltage_parasitic_reaction_benefit_sulfide_assb.md` · `choi2026_bzox_dry_zro2x_nmc_shell_coating.md` · `sundar2025_oxide_coating_screening_lpscl.md` · `kim2026_hts_li3sc2po43_coating_midni_ncm.md` — 코팅 레버 형제들
- `banik2022_substitutions_oxidative_stability_argyrodite.md` — **B① 은 치환으로 안 움직인다**(S 3p pin) → 그래서 코팅이 필요하다는 이 논문의 전제
