# Computationally-Guided Development of Sulfide Solid Electrolyte Powder Coatings — Sundar et al. (Advanced Science 2025)

> slug `sundar2025_oxide_coating_screening_lpscl` · DOI `10.1002/advs.202513191` · type `DFT high-throughput screening + exp 검증(ALD·XPS·EIS·CCD)` · PDF `82ea256b-…15._Computteries.pdf` · digested `2026-06-26` · status ✅ · 태그 **[외부]**
> **저자**: Aditya Sundar, Taewoo Kim, Francisco Lagunas, Anil U. Mane, Udochukwu D. Eze, Colton Ginter, Rajesh Pathak, Sanja Tepavcevic, Jeffrey W. Elam, Zachary D. Hood, **Peter Zapol***, **Justin G. Connell*** (Argonne National Laboratory + University of Chicago) · Adv. Sci. 2025, 12, e13191 · Received 2025-07-14, Published 2025-10-15.

---

## 0. 이 digest를 읽는 법 (먼저 — 우리 연구와의 위치 정렬)
이 논문은 **우리 doping cascade(격자 치환)와는 *다른 레버***다. 우리는 **LPSCl *격자 안*을 도판트(Nd/Mg/O/F…)로 바꾼다**. 이 논문은 **LPSCl *입자 표면*에 바이너리 산화물(MgO/ZrO₂/ZnO/Al₂O₃)을 ALD로 ~1 nm 코팅**한다. 그래서:
- **연결 1순위 = 우리 `GrandPotentialInterfacialReactivity` / `interface_reactivity` / `sei_products`** (계면 분해반응 ΔE·산물·band gap). 이 논문의 *방법론 자체*가 우리 grand-potential 계면 도구의 **쌍둥이**다: "코팅║전해질, 코팅║양극, 코팅║음극 세 계면의 분해반응 ΔE를 0 K DFT로 전부 계산 → 가장 음의 driving force를 heatmap화 → 후보 선별".
- **연결 2순위 = He2019-류 DFT-방법론 / 우리 electronic.json·oxidation grand-potential**. HSE06 band gap(bulk+1 nm slab), CI-NEB Li migration barrier가 우리 electronic gap·li_transport와 *기법* 정렬.
- **❗ 연결 *아님* (force-fit 금지)**: 우리 47-dopant cascade의 descriptor/ranking(stability↔mobility trade-off, BVSE bottleneck)은 이 논문과 **직접 대응되지 않는다**. 이 논문엔 도판트도, BVSE도, Li-mobility descriptor도 없다. 유일하게 약한 개념 공명은 §2.5의 "**가장 예측력 있는 지표 = 코팅 그 자체가 아니라 *계면 분해산물*의 ionic/electronic conductivity**" ↔ 우리 cascade의 "도판트 자체가 아니라 *분해산물·SEI*의 전자절연성이 진짜 레버"라는 *철학*뿐. **랭킹·descriptor 대조는 하지 말 것.**

> ⚠ **우리 그룹 아님**: Argonne/UChicago. [Cha]/[Kang]/[KimICCF] 라인과 무관. 그러나 SE = **Li₆PS₅Cl(=우리 comp1)**, 동일 grand-potential 계면 방법론 → 우리 *방법*의 가장 직접적인 외부 거울.

## 1. 한 줄 요약
**DFT 2-단계 스크리닝**(① 계면 분해 ΔE + bulk/slab band gap → ② 분해산물의 Li migration barrier + band gap)으로 LPSCl 입자에 코팅할 바이너리 산화물을 추리고, **MgO·ZrO₂·ZnO**를 ALD로 실제 증착해 검증한다. 핵심 결론: **코팅의 (전기)화학 성능을 결정하는 가장 예측력 있는 지표는 코팅 산화물 *자체의 열역학 안정성*이 아니라, LPSCl·Li 금속과 만나 *형성되는 계면 분해산물의 이온/전자 전도도*** — 특히 **Li-conductive 산화물 + Li-alloy 형성이 음극서 좋고**, **MgO가 다면적(σ_ion↑·σ_e↓·Li-metal 안정·R_int↓·CCD↑)으로 최고**. (Al₂O₃ 재확인, ZnO는 σ_e가 예상과 반대로 *증가*.)

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 대상 SE | **Li₆PS₅Cl (LPSCl = 우리 comp1)** powder |
| 레버 | 입자 표면 **ALD 바이너리 산화물 코팅** (~1 nm), 격자 도핑 아님 |
| 코팅 후보 | 주기율표 첫 6주기 바이너리 산화물 광범위 스크린 → SiO₂·Al₂O₃·ZrO₂·MgO·TiO₂·Sc₂O₃·Y₂O₃·Nb₂O₅·MnO·Cr₂O₃·CaO·ZnO (Table 1) |
| 실험 검증 | **MgO·ZrO₂·ZnO** ALD 증착 (Al₂O₃는 선행연구[ref13]서 이미 검증) |
| 양극/음극 모델 | 양극 = **LiCoO₂(LCO)·LiMn₂O₄(LMO)**; 음극 = **Li metal** |
| 질문 | "Al₂O₃ 말고 *더 다면적 이득*을 주는 코팅을 DFT로 어떻게 찾나? 어떤 지표가 진짜 예측력 있나?" |
| 갭 | 기존 코팅 스크린은 (a) 양극에만 집중, (b) 반응 *에너지*만 봄 — 계면 *전역(전해질·양극·음극)* + *분해산물의 전도도*까지 본 종합 스크린은 부재 |
| 선행(같은 그룹) | [ref13] Hood/Connell: **Al₂O₃ ALD on LPSCl** → σ_ion 2× ↑, σ_e ↓, Li/oxidizing 안정 ↑ (이 논문의 출발점) |

## 3. 핵심 물성 / 수치 (총정리)

### 3.1 LPSCl 기준값 (이 논문 계산)
| 물성 | 값 | 방법 |
|---|---|---|
| **LPSCl band gap** | **3.92 eV** | **HSE06** (mixing 0.32) — Fig 3a 점선 기준 |
| LPSCl║SiO₂ 계면 ΔE | **0.000 eV/atom** (무반응) | Table 1 |

### 3.2 계면 분해 driving force ΔE (Table 1·2, eV/atom; 더 음수 = 더 반응)
| Oxide | **LPSCl║Oxide ΔE** | **Li║Oxide ΔE** | 주 분해산물 (LPSCl 계면) |
|---|---|---|---|
| SiO₂ | **0.000** (무반응) | −0.447 | — |
| Al₂O₃ | **−0.044** | −0.220 | Li₃PS₄ + LiCl + **LiAlS₂ + LiAl₅O₈** |
| ZrO₂ | **−0.097** | −0.185 | Li₃PS₄ + **Li₆Zr₂O₇ + Zr₃O** + LiCl |
| MgO | **−0.125** | **−0.040** (Li와 가장 안정) | Li₃PO₄ + Li₂S + LiCl + **MgS** |
| TiO₂ | −0.126 | −0.357 | Li₄TiS₄ + Li(TiS₂)₂ + TiS₂ … |
| Sc₂O₃ | −0.132 | −0.034 | Li₃Sc(PO₄)₂ + LiScS₂ … |
| Y₂O₃ | −0.176 | **0.000** (무반응) | LiYS₂ + YPO₄ … |
| Nb₂O₅ | −0.200 | −0.585 | NbS₂ + Li₃PO₄ … |
| MnO | −0.202 | −0.557 | Li₆MnS₄ + MnS … |
| Cr₂O₃ | −0.256 | −0.611 | LiCrS₂ + LiScS₂ 류 … |
| CaO | −0.304 | n/a (Table1 미기재) | Li₂S + CaS + LiCl |
| **ZnO** | **−0.372** (가장 반응성) | **−0.653** (가장 반응성) | Li₂S + ZnS + LiCl |
> 기준 반응 예 `0.2 Li₆PS₅Cl + 0.8 Li₂O → Li₂S + 0.2 Li₃PO₄ + 0.2 LiCl` (ΔE = **−0.278 eV/atom**, Eq 1). p-궤도 가전자 원소(In·Ga·Sn)는 ZnO보다 ΔE 낮으나 **Li 반응성 때문에 제외**.

### 3.3 HSE06 band gap (Fig 3, eV)
| Oxide | bulk gap | ~1 nm slab gap | 비고 |
|---|---|---|---|
| **LPSCl** | **3.92** | — | 기준선 |
| Al₂O₃ | **8.80** | >6 | 가장 큰 gap (σ_e 최소) |
| SiO₂ | **8.12** | >6 | |
| MgO | **7.16** | <5 (insulating) | |
| ZrO₂ | (>LPSCl) | >6 | |
| Sc₂O₃ / Y₂O₃ | >6 | >6 | |
| TiO₂ | ~5 (bulk) | **~2** (slab) | slab서 LPSCl보다 낮아짐 |
| MnO | (bulk) | **~2** (slab) | |
| **ZnO** | **3.40 (exp), ~3 (bulk calc)** | **0.4** (1 nm slab) | slab서 급감 — but ALD ZnO는 산소공공으로 실제 σ_e 높음 |
> 메시지: bulk gap이 커도 **나노 slab + 산소공공**이 σ_e를 지배 → ZnO 함정. monolayer ZnO 선행값 3.5 eV[ref49]와 본 계산 0.4 eV 차이 = ZnO defect 민감성.

### 3.4 분해산물의 Li migration barrier (CI-NEB, Fig 4, eV)
| 산물 | barrier | 전도 특성 |
|---|---|---|
| **Li₃PO₄** | **0.25** | Li⁺ conductor (LPSCl 분해 1차산물) |
| **Li₃PS₄** | **0.34–0.41** | Li⁺ conductor |
| **LiAlS₂** / LiAl₅O₈ | **0.28–0.33** | Li⁺ conductor (Al₂O₃ 산물) |
| **Li₂S, LiCl** | 빠름 (<100>/<110> 방향) | Li⁺ conductor |
| **Li₄TiS₄ / YPO₄** | 0.30 / 0.24 | 3D 빠름 |
| **MgS / YPO₄ 류** | (다양) | 층상 황화물 |
| **Zr₃O** | **1.4** | Li-insulating (ZrO₂ 산물 → σ_ion ↓ 설명) |
| Li₆Zr₂O₇ | 큼 | Li-insulating |
| MnS·NbS₂·TiS₂·Li(TiS₂)₂ | ~metallic | σ_e ↑ (ZnO/MnO/Nb₂O₅/TiO₂ 산물) |
> 산물 band gap(Table S5/S6): Li₃PO₄·Li₃PS₄·Li₂S·LiCl 모두 **bulk LPSCl보다 큰 gap** → σ_e 억제 산물. **LiAlS₂·LiAl₅O₈·MgS = 특히 큰 gap**(Al₂O₃·MgO 유리). Ga₂O₃·In₂O₃·ZnO → 금속성/소-gap 황화물(MnS/NbS₂/Zr₃O metallic) → σ_e ↑.

### 3.5 실험 (전도도 비, ALD-coated / uncoated; Fig 6, 25 °C 5 MPa)
| 코팅 | **σ_ion 비** | **σ_e 비** | 메시지 |
|---|---|---|---|
| **Al₂O₃** | **≈1.5** (↑) | **0.81** (↓) | 선행[ref13] 재확인 |
| **MgO** | **≈1.0** (불변~약↑, 본문 "up to 25% 높음") | **0.11** (1/9, 대폭↓) | **다면적 best** |
| **ZnO** | **≈1.2** (↑) | **0.17** (↓) | (단 ZnO는 1 nm Al₂O₃ seed 필요) |
| **ZrO₂** | **0.1× (1.26→0.12 mS/cm, 한 자릿수 ↓)** | **2× (↑)** | 예측대로 나쁨 (Zr₃O/Li₆Zr₂O₇ Li-insulating) |
> ⚠ **ZnO σ_e 역설**: ZnO는 transparent-conducting-oxide라 σ_e ↑ 예상인데 코팅 후 **σ_e 0.17로 ↓** — 본문 해석: ZnO 분해산물(ZnS, resistivity ALD ZnS ≈ 10⁸× ALD ZnO[ref61])이 σ_e를 떨어뜨림. **"산물이 코팅 자체보다 (전기)화학 물성을 지배"의 결정적 증거.**

### 3.6 실험 — MgO-coated LPSCl 다면 이득 (Fig 7·8)
| 지표 | uncoated | MgO-coated | 출처 |
|---|---|---|---|
| Li metal 안정성 (S 2p PS₄³⁻→Li₂S 환원) | 심함 | **약함** (Li₃₋ₓP 더 많음, Li₃P 적음) | Fig 7a,b |
| MgO 리튬화 산물 | — | **LiMgO·LiMg alloy + Li₂O** (DFT 예측 일치) | Fig 7c,d |
| 대칭셀 CCD | ~0.6 mA/cm²서 voltage decoupling (soft short) | **≤0.9 mA/cm²까지 안정**, decoupling ≈0.8서 미미 | Fig 8 |
| ASR (CCD 중) | 0.6 mA/cm²서 precipitous drop | **0.9까지 drop 없음** | Fig 8b,d |

## 4. DFT/계산 방법 ★ (우리 grand-potential 계면 도구의 거울 — 정밀 대조)
- **code / version**: **VASP**. ([ref72] Kresse)
- **functional (band gap)**: **HSE06** (Heyd-Scuseria-Ernzerhof, **mixing parameter = 0.32** — 표준 0.25 아님, LPSCl/산화물 gap 튜닝). [ref73]
- **functional (NEB / 반응에너지)**: **PBE** (GGA). [ref75]
  - ⚠ **반응 ΔE는 PBE 0 K**, gap만 HSE06. → 우리와 같은 분리(에너지=GGA, gap=정밀).
- **계면 반응에너지**: **Materials Project Interface Reactions app (legacy MP)** + **Materials Project DFT 에너지** retrieve (Selenium WebDriver 스크래핑). 각 (oxide+LPSCl), (oxide+Li), (oxide+cathode) 조합에 대해 **가능한 모든 반응 계산 → 가장 음의 ΔE(최대 driving force) 선택** → heatmap.
  - 🔑 **이것이 곧 pymatgen `InterfacialReactivity`** — 우리 `interface_reactivity`/`GrandPotentialInterfacialReactivity`와 **동일 알고리즘**. (우리는 grand-potential(전압분해)까지, 이들은 0 V 2상 반응 ΔE.)
- **band gap 계산 cell**: bulk + **~1 nm slab**(ALD 코팅 두께 모사, 진공 ~1 nm, 5×5×5 k-mesh region). monolayer 효과 명시.
- **NEB**: **CI-NEB** (climbing image), 중간 replica = 초기/최종 선형보간. [ref74]
- **수렴**: 에너지 10⁻⁶ eV, 힘 10⁻² eV/Å. plane-wave cutoff **500 eV**.
- **k-points / supercell / nat**: slab 5×5×5 영역; 자세한 supercell/nat은 본문 미기재(n/a — SI 추정).
- **DFT+U**: 명시 없음(n/a). LCO/LMO/TiO₂/MnO 등 전이금속 산화물 포함이나 U 언급 없음 — **방법 약점 가능성**(§10).
- **AIMD**: 없음. (Li migration은 CI-NEB만; 분해산물 barrier 일부는 *선행 AIMD 인용*[refs50–53].)
- **MLIP**: 없음.
- **무질서 처리**: 명시 없음(n/a). LPSCl의 S²⁻/Cl⁻ 4a/4c site disorder를 어떻게 다뤘는지 본문 불명 — **우리 SQS/single-config 고민과 동일 미해결**(§10).
- **반응 차원**: 주로 **2상 반응**(oxide+LPSCl). 3상(Li-Oxide-LPSCl)은 대표 Li-Al₂O₃-LPSCl만 SI서 체크 → "유의차 없음"(향후 과제로 남김).

## 5. 결과 — 섹션별 상세

### 5.1 §2.1 계면 열역학 안정성 (3 계면)
**1단계 스크린 = 반응 ΔE + band gap.** 세 계면(전해질║코팅·음극║코팅·양극║코팅) 각각 heatmap(Fig 2).
- **§2.1.1 전해질║Oxide (Table 1, Fig 2 LPSCl panel)**: SiO₂(ΔE=0, 무반응) > Al₂O₃(−0.044) > ZrO₂(−0.097) > MgO(−0.125) > … > ZnO(−0.372). **가전자 배치 s²/s²p¹/s²p²/d²/d¹⁰(완전점유) = 덜 반응 / s¹(Li,Na,K,Rb) + d-부분점유(Fe,Co,Ni,Cu,Zn,Pd,Ag,Cd) = 더 반응**. SiO₂가 가장 안정(무반응)이나, **In·Ga·Sn(p-궤도)은 ΔE 더 낮아도 Li 반응성으로 제외** → ZnO를 d-원소 중 가장 안정한 *추가* 후보로 채택(다른 이유 = σ_e 검증용).
- **§2.1.2 음극(Li)║Oxide (Table 2, Fig 2 Li-anode panel)**: Y₂O₃·CaO(무반응, ΔE=0) > Sc₂O₃(−0.034) > **MgO(−0.040)** > ZrO₂(−0.185) > Al₂O₃(−0.220) > … > **ZnO(−0.653, 최악)**. d-블록 산화물(부분점유)은 ZnO보다 Li와 훨씬 강하게 반응. Na₂O·K₂O·Rb₂O·SrO·BaO는 Li와는 덜 반응하나 **LPSCl과 ZnO보다 강반응 → 제외**. **MgO·ZrO₂·Al₂O₃ = Li·LPSCl 양쪽 모두 비교적 안정** → 핵심 후보.
- **§2.1.3 양극(LCO/LMO)║Oxide**: 양극 계면 ΔE는 **전해질·음극 계면보다 훨씬 작음**(거의 무반응). 예 `0.1525 LiMn₂O₄ + 0.8475 Al₂O₃ → 0.1017 Mn₃O₄ + 0.08475 Al₁₁O₁₈ + 0.1525 LiAl₅O₈`, ΔE = **−0.024 eV/atom** (Li 금속 반응의 1/10, kinetic 제약으로 사실상 무반응). → **결론: 양극 반응성은 코팅 성능의 신뢰할 지표가 아니다**(대부분 산화물이 양극엔 안정). **진짜 변별은 전해질·Li 계면**.

### 5.2 §2.2 전자구조 (Fig 3)
- LPSCl HSE06 gap = **3.92 eV**(기준선). 대부분 후보 산화물 bulk gap이 이보다 큼 → σ_e 억제 가능.
- Al₂O₃(8.80)·SiO₂(8.12)·MgO(7.16) = 최대 gap. **단 나노 slab는 다름**: TiO₂·MnO slab ~2 eV(LPSCl보다 작음), **ZnO 1 nm slab = 0.4 eV**(급감) → 산소공공·표면상태로 σ_e ↑ 위험. → **"코팅이 LPSCl보다 작은 gap(TiO₂/MnO/ZnO)이면 σ_e ↑, 큰 gap(Al₂O₃/SiO₂/MgO)이면 σ_e ↓"** + bulk gap 단독으론 부족, slab+defect 필수.

### 5.3 §2.3 분해산물의 이온/전자 전도 (Fig 4) — **이 논문의 핵심 논리축**
1단계 후보의 **분해산물**(Fig 2 반응이 만든 화합물)의 (a) Li migration barrier(Fig 4a LPSCl계면 / 4b Li계면) + (b) band gap(Table S5/S6) 평가 = 2단계 스크린.
- **LPSCl║Oxide 분해산물**: 주로 **Li₃PO₄(0.25)·Li₃PS₄(0.34–0.41)·Li₂S·LiCl** = Li⁺ conductor + 큰 gap → σ_ion 유지·σ_e 억제. **LiAlS₂·LiAl₅O₈(0.28–0.33)·MgS = 특히 큰 gap** → Al₂O₃·MgO 유리.
- **나쁜 산물**: **Zr₃O(barrier 1.4 eV, Li-insulating)·Li₆Zr₂O₇** = ZrO₂가 σ_ion 떨어뜨리는 이유. **MnS·NbS₂·TiS₂·Li(TiS₂)₂ ≈ metallic / Zr₃O metallic** → MnO·Nb₂O₅·TiO₂·ZrO₂ σ_e ↑.
- **Li║Oxide 분해산물(Fig 4b)**: Li₂O = 가장 흔한 산물, 빠른 Li 전도. Ga₂O₃·In₂O₃·ZnO → metal-sulfide + 소-gap 산물(σ_e↑). Zr₃O metallic.
- 🔑 **종합 결론**: **Al₂O₃·MgO 코팅** → (i) 낮은 분해 driving force, (ii) Li-conductive 산물로 σ_ion 채널 유지, (iii) 큰-gap 산물로 σ_e 억제 = **다면적 이득**. **ZrO₂** → Li-insulating + σ_e↑ 산물로 trade-off 나쁨.

### 5.4 §2.4 ALD 코팅 실증 (Fig 5)
MgO·ZrO₂·ZnO를 ALD 증착(~1 nm, conformal). XPS(S 2p·P 2p + Mg 2p/Zr 3d/Zn 2p) + STEM-EDS.
- **MgO**: S 2p PS₄³⁻(161.6/162.7) 유지(저반응) + minor oxysulfide(POₓSᵧ) + Mg 2p **49.9 eV = Mg(OH)₂/oxysulfide** + **49.2 eV = LiMgO**(DFT가 LPSCl║MgO 산물로 예측한 것과 일치). MgS도 minor 검출.
- **ZrO₂**: Zr 3d **182.0/184.4 = ZrO₂** + minor **Li₆Zr₂O₇·Zr₃O**(179.7/182.1/178.2/180.6) → DFT Li║ZrO₂ 예측 산물 일치.
- **ZnO**: LPSCl 위 직접 증착 실패(반응성↑/휘발) → **1 cycle Al₂O₃ seed 후** 증착 가능. 명확한 Zn 신호.
- STEM-EDS: Mg·Zr·Zn 균일 분포(우선 핵형성/편석 없음), 입자 표면 약간 농축.

### 5.5 §2.4 전도도 측정 (Fig 6) — DFT 검증
- **σ_ion 비**: Al₂O₃ 1.5↑ / MgO ~1.0(~25%↑) / ZnO 1.2↑ / **ZrO₂ 0.1× (한 자릿수 ↓)**. → ZrO₂는 Zr₃O/Li₆Zr₂O₇(Li-insulating) 산물 예측대로 σ_ion 급감.
- **σ_e 비**: Al₂O₃ 0.81 / **MgO 0.11(1/9)** / ZnO 0.17 / **ZrO₂ 2×(↑)**. → ZrO₂만 σ_e ↑(소-gap/금속성 산물), 나머지는 σ_e ↓.
- 🔑 **Fig 6 = "분해산물의 ionic/electronic 전도가 코팅 자체의 열역학 안정성보다 더 예측력 있다"의 정량 증거.** ZnO가 좋은 예: ZnO 자체는 conducting인데 ZnS 산물이 절연 → 코팅 후 σ_e↓.

### 5.6 §2.5 MgO-coated LPSCl의 Li 금속 안정성 (Fig 7) + CCD (Fig 8)
- **XPS before/after Li**: uncoated는 PS₄³⁻→Li₂S(160.3/161.4) + Li₃P(125.7/126.6) 강한 환원. **MgO-coated는 Li₂S 적고 Li₃₋ₓP(덜 환원) 많음** = Li 금속 안정성 ↑ (Al₂O₃ 선행결과와 동일).
- **Mg 2p/O 1s**: Li 증착 후 **LiMgO·LiMg alloy + Li₂O** 형성(DFT 예측 일치). MgO 리튬화 정도가 Al₂O₃보다 큼 → LiMg alloy가 더 형성.
- **CCD(대칭셀, Fig 8)**: uncoated는 0.6 mA/cm²서 voltage decoupling(ASR precipitous drop = soft short). **MgO-coated는 0.9 mA/cm²까지 largely stable**(decoupling ≈0.8서 미미, ASR drop 없음). → MgO가 CCD·ASR 개선(Al₂O₃와 유사 거동, full-cell은 본 논문 범위 밖).

## 6. 메커니즘 종합 (design rules)
**2-단계 스크린의 논리:**
1. **1단계 (선별)**: 코팅 후보 = **낮은 계면 분해 ΔE**(전해질·Li 양쪽) + **큰 band gap**(bulk+slab, σ_e↓). → SiO₂·Al₂O₃·ZrO₂·MgO·Sc₂O₃·Y₂O₃ 통과.
2. **2단계 (변별)**: 1단계 후보의 **분해산물**이 **Li-conductive(낮은 NEB barrier)** + **큰 gap(σ_e↓)**인지. → **Al₂O₃·MgO 통과**(LiAlS₂/LiAl₅O₈/MgS/Li₃PO₄ = Li-conductive·wide-gap), **ZrO₂ 탈락**(Zr₃O/Li₆Zr₂O₇ = Li-insulating + 금속성).
3. **🔑 핵심 design rule**: **"가장 예측력 있는 지표 = 계면 분해산물의 ionic/electronic conductivity (특히 음극서 Li-conductive oxide + Li-alloy 형성에 대한 열역학적 선호), *코팅 자체의 열역학 안정성이 아니다*."** (ZnO 역설이 증명: 안정성·bulk-gap 예측과 실제 σ_e가 어긋남 → 산물이 지배.)
4. **MgO = champion**: σ_ion↑(~25%)·σ_e↓(1/9)·Li-metal 안정·R_int↓·CCD↑(0.9 mA/cm²) 다면적. **Al₂O₃ 재확인**. ZnO도 일부 좋으나 ALD 처리성(Al₂O₃ seed 필요)·defect 민감으로 차순위. ZrO₂ = 안정해 보여도 산물 때문에 실패.

## 7. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`
> ⚠ **이 논문은 LPSCl *코팅* 연구 — 우리 *격자 도핑*과 다른 레버.** 직접 수치 1:1 대조 가능한 칸은 **band gap·계면 분해화학**뿐. 나머지는 *방법론* 정렬.

| 항목 | Sundar 2025 | 우리 (comp1/modelc) | 일치/차이 + 이유 |
|---|---|---|---|
| **LPSCl band gap** | **3.92 eV (HSE06, mix 0.32)** | comp1 **2.066** / modelc **2.098 eV (PBE)** | △ **방법차 (PBE vs HSE06)** — 우리 PBE가 ~1.85 eV 과소. [Semi]의 PBE 2.45/HSE06 3.30과 같은 ~1 eV gap. **절대 비교 금지, "wide-gap insulator"만.** Sundar 3.92는 mix 0.32(>표준 0.25)라 [Semi] 3.30보다도 높음 → mixing 의존성 노출 |
| **계면 분해 방법** | MP `InterfaceReactions` (2상, 0 V, PBE ΔE) | 우리 `interface_reactivity` / `GrandPotentialInterfacialReactivity` (voltage-resolved) | **✓✓ 동일 알고리즘(pymatgen)** — 우리는 grand-potential로 *전압별*까지 확장, 이들은 0 V 2상. **방법 거울** |
| **LPSCl 분해 1차산물 (계면)** | Li₃PO₄·Li₂S·LiCl·Li₃PS₄ (산화물과) | comp1 환원 0 V → Li₃P+Li₂S+**LiCl**; 산화 → Li₃PS₄+LiCl+S | **✓ 같은 산물 패밀리** (Li₂S·LiCl·Li₃PS₄·Li₃PO₄ 공통). 단 *상대(oxide) 다름* — 우리는 LPSCl 자체분해, 이들은 oxide와 반응 |
| **분해산물 band gap(σ_e 지표)** | Li₃PO₄·Li₃PS₄·Li₂S·LiCl·LiAlS₂·MgS = LPSCl보다 큰 gap (HSE06) | sei_products.json: **LiCl 6.65 / Li₂S 3.90** (MP) | **✓✓ 같은 논리** — "wide-gap 분해산물 = σ_e 억제 = 좋은 interphase". [Li25] LiCl 6.13/Li₂S 3.04, [Lu] LiCl 6.22와 한 줄. **단 우리 LiAlS₂/MgS 없음**(Al/Mg 우리 hull 밖) |
| **Li migration barrier(분해산물)** | CI-NEB: Li₃PO₄ 0.25 / Li₃PS₄ 0.34–0.41 / Zr₃O 1.4 eV | 우리 Ea(AIMD): comp1 0.253 / modelc 0.224 eV (LPSCl *자체*) | △ **대상 다름** — 이들은 *분해산물*의 NEB, 우리는 *LPSCl bulk*의 AIMD. 직접 비교 X. 단 Li₃PS₄ 0.34–0.41 ≈ 우리 LPSCl 0.22–0.25 같은 0.2–0.4 eV 줄 |
| **σ_e(전자전도) 측정** | ALD-coated 실측 비: MgO 0.11·ZnO 0.17·ZrO₂ 2× | 우리 미측정(bulk gap=wide insulator) | [Liu23] 8.16e-9, [Li25] 1.02e-8 S/cm 실측 anchor와 같은 줄 — **σ_e가 진짜 dendrite/안정성 레버** 재확인 |
| **환원/Li-metal 안정 산물** | MgO→LiMgO+LiMg alloy+Li₂O (Fig 7) | comp1/modelc 0 V → Li₃P+Li₂S+LiCl | △ **다른 화학**(이들=oxide 리튬화, 우리=LPSCl 환원). 단 **"Li-alloy/wide-gap oxide 형성이 음극서 좋다"** = [Ke] LiMg+Li₂O 8.37 eV와 같은 결 |

## 8. 적용 인사이트 (우리 연구에 어떻게, 깊게)
1. **방법론 거울 — 우리 grand-potential 계면 도구의 외부 정당화**: 이 논문은 우리 `GrandPotentialInterfacialReactivity`/`interface_reactivity`와 **같은 pymatgen `InterfaceReactions`**로 12개 산화물×3계면을 스크린한다. **우리 도구가 표준임을 외부 Argonne 그룹이 동일하게 사용** → deck "우리 계면 분해 분석은 분야 표준 방법" 근거. (단 우리는 *전압분해(grand-potential)*까지 확장 = 우리 우위.)
2. **"분해산물의 전도도가 진짜 지표" = 우리 sei_products/Nd cascade 철학과 정확히 같은 결**: Sundar의 핵심 design rule("코팅 안정성 < 분해산물 σ_ion/σ_e")은 우리 "도판트 자체 < *분해산물/SEI*의 전자절연성(NdPO₄/Li₃PO₄/Li₂O wide-gap)이 진짜 레버"와 **같은 사고**. **인용 가능**: "An independent high-throughput study reaches the same conclusion — the (electro)chemical viability is governed by the *interfacial reaction products' transport properties*, not the additive's own stability."
3. **wide-gap 분해산물 = σ_e 억제 = 좋은 interphase, 독립 재확인**: Sundar HSE06 gap(Li₂S<LiCl, LiAlS₂/MgS 큼) = 우리 sei_products.json(LiCl 6.65≫Li₂S 3.90) + [Li25](LiCl 6.13/Li₂S 3.04) + [Lu](LiCl 6.22) 줄에 **HSE06 산화물-계 산물(LiAlS₂/MgS)을 추가**. 우리 "wide-gap halide/phosphate = 전자절연 SEI" 패밀리의 또 다른 외부 증거.
4. **band gap은 PBE 과소 + slab/defect 민감, 절대 비교 금지 — Sundar가 직접 보여줌**: bulk ZnO 3.4 eV인데 1 nm slab 0.4 eV, monolayer 선행값 3.5 eV. → **우리 PBE gap 2.07(과소)·무질서 ±0.2–0.3 scatter를 "wide-gap insulator"로만 쓰는 우리 규율이 옳다는 외부 근거.** Sundar mix 0.32로 3.92, [Semi] 3.30 — HSE도 mixing 의존.
5. **❗ cascade(도핑)와는 force-fit 금지**: 이 논문엔 도판트·BVSE·Li-mobility descriptor·stability↔mobility trade-off가 *없다*. 우리 47-dopant 랭킹과 대조하면 안 됨. 연결은 **(a) 계면 방법론, (b) 분해산물-전도도 철학** 두 곳뿐.
6. **MgO가 우리 6원소 hull 밖이지만 — Mg 도판트 관점 단서**: 우리 cascade에 Mg 도판트가 있다면([Ke]/[Liu23] MgClO/MgF₂ 동기), Sundar는 "MgO 코팅 산물 = LiMgO·LiMg·Li₂O·MgS = wide-gap·Li-alloy·Li-conductive" → **Mg 도입이 (코팅이든 도핑이든) 음극 측에 wide-gap·alloy 산물을 줘 유리**라는 *화학적 일관성*. (단 코팅≠도핑, 산물 위치 다름 — 신중히.)
7. **양극 계면은 변별력 약하다(Sundar §2.1.3) = 우리 [Cha]/[Kang25] 정렬**: "대부분 산화물이 양극엔 안정, 진짜 변별은 전해질·Li 계면" → 우리 그룹 양극 코팅 논문들이 "양극은 *어떻게 차단/균일화*하느냐(σ 아닌 호환성)"로 간 것과 결이 같음. 양극 ΔE 절대값은 작아 ranking 신뢰도 낮음 = Sundar도 명시.

## 9. 인용 가능 문장 (deck/paper용)
- "Sundar et al. (Adv. Sci. 2025), using the same pymatgen `InterfaceReactions` framework we employ, screened binary-oxide coatings on Li₆PS₅Cl and concluded that **the interfacial decomposition products' ionic/electronic conductivity — not the coating's own thermodynamic stability — is the most predictive metric**, mirroring our SEI/Nd-cascade philosophy."
- "Their HSE06 band gaps of LPSCl-decomposition products (Li₂S < LiCl, with LiAlS₂/MgS especially wide) reproduce the same insulating-product ordering as our `sei_products.json` (LiCl 6.65 ≫ Li₂S 3.90 eV) and [Li25] (LiCl 6.13/Li₂S 3.04)."
- "The ZnO paradox (bulk gap 3.4 eV but 1 nm slab gap 0.4 eV, and σ_e *dropping* upon coating due to insulating ZnS products) confirms why we treat PBE gaps only as 'wide-gap insulator' and never compare absolute values across disorder/k-mesh/functional."
- "MgO coating gave a multifaceted benefit (σ_ion +~25%, σ_e ÷9, improved Li-metal stability via LiMg-alloy formation, CCD up to 0.9 mA cm⁻²), independently validating that Li-conductive + wide-gap decomposition products define a good interphase."

## 10. 주의 / 한계 (over-claim 방지 — 비판적)
- **❗ 코팅 ≠ 도핑 — 우리 cascade와 직접 비교 금지.** 이 논문은 LPSCl *표면 코팅*(별도 산화물 상). 우리 modelc/Nd는 *격자 치환*. 산물·메커니즘 위치가 다르다. "Sundar = 우리 cascade 검증"이라고 하면 **틀림** — 검증되는 건 *계면 방법론*과 *분해산물 철학*뿐.
- **반응 ΔE = PBE 0 K 2상**, gap만 HSE06. 우리 grand-potential(전압분해)·indirect lithiation을 안 봄 → 절대 ΔE는 우리 onset과 다른 스케일(0 V vs 전압별).
- **DFT+U 미명시**: LCO/LMO/TiO₂/MnO/Cr₂O₃ 등 강상관 전이금속 산화물 포함인데 +U 언급 없음 → 이들 산화물의 반응 ΔE·gap **신뢰도 의문**(특히 Mn/Cr/Ti 계). 본 논문 결론(MgO/Al₂O₃)은 비-상관 산화물이라 영향 적으나, 양극·전이금속 산화물 ranking은 주의.
- **무질서(LPSCl S²⁻/Cl⁻ disorder) 처리 미명시**: single-config로 보이나 불명. 우리와 같은 미해결.
- **HSE06 mixing 0.32 = 비표준(>0.25)**: gap을 높이는 방향으로 튜닝됨. LPSCl 3.92는 [Semi] HSE06 3.30보다 높음 → **mixing 선택이 gap 절대값을 좌우**(우리가 절대 gap 비교를 피하는 이유의 또 다른 예).
- **양극 계면 ΔE 절대값이 작음(−0.024 류)** → ranking noise 가능, 본문도 "신뢰할 지표 아님"으로 후퇴. 양극 결론은 약함.
- **3상 반응 미검토**(대표 1개만): 실제 ALD 계면은 3상(Li-Oxide-LPSCl) 가능 → 향후 과제로 본문이 인정.
- **ZnO 직접증착 실패** → Al₂O₃ seed 위 ZnO. 따라서 "ZnO 코팅" 실측은 엄밀히 ZnO/Al₂O₃ 이중층 → 순수 ZnO 효과 분리 불완전(본문 1 nm Al₂O₃는 σ_e에 영향 미미하다 주장하나 caveat).
- **full-cell 사이클 데이터 없음** — Li 대칭셀 CCD/ASR + XPS까지. 실제 배터리 성능은 미검증(향후).
- **σ_ion/σ_e 절대값 없이 *비(ratio)*만** — batch 변동 정규화 목적이나, uncoated 절대 σ가 batch마다 달라 절대 성능 비교는 불가.

## 11. 기법 용어 미니사전
- **ALD (Atomic Layer Deposition)**: 기체 전구체 self-limiting 반응으로 ~Å 단위 conformal 박막. 여기선 분말 LPSCl에 산화물 ~1 nm 코팅(TMA/MgCp₂/TDMAZr/DEZ 전구체, 150 °C).
- **InterfaceReactions (pymatgen / MP app)**: 두 상의 혼합비를 0→1로 스캔하며 convex hull 상 가능한 모든 분해반응의 ΔE를 계산, 가장 음수(최대 driving force)를 계면 반응성 지표로. **우리 `interface_reactivity`와 동일.**
- **CI-NEB (Climbing-Image Nudged Elastic Band)**: 초기·최종 구조 사이 image 띠를 최적화해 migration 안장점(barrier) 산출. 여기선 *분해산물*의 Li 이동도.
- **HSE06 (mixing α)**: 하이브리드 functional, exact-exchange α 비율(여기 0.32, 표준 0.25). PBE의 gap 과소를 보정. α 클수록 gap↑.
- **CCD (Critical Current Density)**: Li 대칭셀에서 단락(soft/hard short) 직전 최대 전류밀도. SE의 음극 측 안정성 지표.
- **ASR (Area-Specific Resistance)**: 단위면적 저항(Ω·cm²); CCD 중 precipitous drop = soft short 신호.
- **voltage decoupling**: 대칭셀 stripping/plating 전압이 비대칭/붕괴 = 부분 단락 시작.
- **LiMg alloy / LiMgO**: MgO가 Li과 만나 형성하는 lithiophilic alloy + 삼원 산화물(Mg 2p ~49.2 eV). 음극 안정·균일 Li flux에 유리.
- **transparent conducting oxide (TCO)**: ZnO처럼 wide-gap이나 산소공공/도핑으로 σ_e 높은 산화물 — coating으로 부적합한 함정(but 산물 ZnS가 절연이라 결과적 σ_e↓).
