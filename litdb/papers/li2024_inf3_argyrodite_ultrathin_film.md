# A Versatile InF₃ Substituted Argyrodite Sulfide Electrolyte Toward Ultrathin Films for All-Solid-State Lithium Batteries — Dabing Li et al. (USTB, Li-Zhen Fan 그룹) · **본문+SI 통합 digest**

> slug `li2024_inf3_argyrodite_ultrathin_film` · **Adv. Energy Mater. 2024, 14(47), 2402929** · DOI **10.1002/aenm.202402929** (Wiley-VCH; Received **2024-07-04** · Revised **2024-09-22** · Published online **2024-10-10**) · type `exp (도핑·전기화학·필름·풀셀) + DFT 보조 (자리 형성E · 슬랩 CI-NEB · Li 금속 슬랩 CI-NEB · H₂O/유기용매 흡착E · PDOS)` · PDF **본문 12 pp** + **SI docx**(Methods + Fig S1–S34 + Table S1–S4) · digested `2026-08-05` · 태그 **[외부]** · status ✅**(본문+SI 완결)**
> **재투입 검증 `2026-08-06`** — 같은 논문이 `litdb/inbox/55. A Versatile InF 3 Substituted Argyrodite Sulﬁde ElectrolyteToward Ultrathin Films for All-Solid-State Lithium Batteries.pdf` (**inbox #55 · 사용자 분류 폴더 `DFT`**) 로 재투입돼 **본문 12 pp 전문(PyMuPDF 59.8 k자) 재추출 + `Fig. 1`–`Fig. 6` 전 6 장 이미지 재판독**. → **§14** (교정 **1**(⑥ 철회) · 신규 적발 **4**(⑯–⑲) · 출처 정밀화 **1** · 신규 판독 그림 **2**(`Fig. 5`·`Fig. 6`)). ⚠ **SI 는 이번 재투입에 없다**(원 digest 의 docx SI 가 유일 출처 — Fig S1–S34·Table S1–S4 항목은 재검증 대상 아님).
> elements: Li, P, S, Cl, F, In, O, Co, Fe, Si
> methods: DFT, NEB, DOS, PDOS, XPS, Raman
> **저자**: **Dabing Li**†, **Xinyu Liu**†, **Yang Li**, Xiaoxue Zhao, Meng Wu, Xiang Qi, Lei Gao, **Li-Zhen Fan\*** (fanlizhen@ustb.edu.cn) — Beijing Advanced Innovation Center for Materials Genome Engineering / Beijing Key Lab for Advanced Energy Materials and Technologies, **University of Science and Technology Beijing (USTB)**. (†공동 1저자)
> **자금**: National Key R&D Program of China (2023YFB2503902) · NSFC (U21A2080) · Beijing NSF (Z200011)
> **데이터 공개**: *"available on request … not publicly available due to **privacy or ethical restrictions**"* ⚠ 순수 재료 논문에 privacy/ethical 사유는 부적절한 상투구 — **[GaF₃] 후속편에 그대로 복사돼 있다**

---

## 0. 이 digest를 읽는 법 (⚠ 먼저 읽을 것)

### 0a. **왜 지금 이 논문을 불렀나 — 리뷰어 노트 A13 을 실물로 판정하려고**

1저자가 심사 중인 리뷰 원고(**ECER-D-26-00097**, `papers/fan2026_sulfide_assb_stability_review_ECERD2600097.md`)가 §3.2 에서 **이 논문을 ref [97] 로** 인용하며 이렇게 쓴다:

> *"For instance, incorporating stabilizing components like **InF₃** enhances **lattice bond energy** and **reduces polarizability**, which enables modified sulfide SEs to maintain high ionic conductivity even after organic solvent immersion (Figure 4c)."*

우리 리뷰어 노트 **A13** 이 여기 걸어 둔 지적: *"InF₃ 의 효과가 **In(양이온) 때문인지 F(음이온) 때문인지 원고가 안 가른다**."*
**§4 가 그 판정 전용 절**이다. 결론만 먼저:

| 질문 | 판정 | 근거 |
|---|---|---|
| ① **논문이 In/F 를 갈랐나?** | **축마다 다르다 — "반쯤 갈랐다"** | **이온전도 ✅ 완전 분리**(실험 단일도펀트 대조군 2종, dose-matched, Fig S8) · **수분 ✅ 계산으로 분리**(pristine/In-only/F-only/co-doped 4종 슬랩, Fig S22) · **유기용매 ❌ 미분리**(pristine vs co-doped 2점만, Fig 4a·S24) · **Li 금속·CCD ❌ 미분리** |
| ② **논문의 기전 주장** | **축마다 담당 원소가 다르다** — 수분은 *F(0.15) > In(0.12 eV)*, 용매는 **In 중심 서사**(HSAB soft In³⁺–soft S²⁻ + InS₄ 무분해 만화 `Fig. 4f`), Li 금속은 **F(LiF SEI) + In(Li–In 합금) 분업** | §4c |
| ③ **"lattice bond energy / polarizability" 가 이 논문에 있나?** | **❌ 둘 다 없다.** 원문 전체 검색: `polarizability` **0회**, `bond energy` **0회**, `lattice energy` **0회**. **"polariz-" 5회는 전부 다른 뜻**이고, 그중 물성 서술 1회는 *"F⁻–Li⁺ 정전인력이 강해 **lower polarization rate**"* = **F 가 σ 를 깎는 이유**(이득이 아니라 손해!) | §4d — **리뷰의 인과 사슬이 뒤집혀 있다** |
| ④ **용매 침지 조건** | SE:용매 **1:1 질량**, 슬러리로 섞어 **말린 뒤**, **1 h**, **25 °C**. 용매 3종(polar index 2.4/3.4/4.3). σ 보존율 **co-doped 91.3/82.5/71.2 %** vs **pristine 62.5/43.7/20.8 %** | §4e — 리뷰 Fig 4c ≈ 이 논문 **`Fig. 4b,c` + `Fig. 4f`**(σ 데이터는 **`Fig. 4a`**) |

### 0b. litdb 안에서의 위치 — **"한 염 두 도펀트" 계열의 원조 격**

| 논문 | 염 | 양이온 자리 | 음이온 자리 | 우리 digest |
|---|---|---|---|---|
| [Taklu] 2021 | **CuCl** | Cu→4b(P) | Cl→4a/4c | ✅ |
| [Liu23] 2023 | **MgF₂** | Mg→4b(P) 주장 | F→Cl 자리 | ✅ |
| **본편 2024** | **InF₃** | **In→4b(P)** | **F→4a(Cl)** | **본 digest** |
| [Li25] 2025 | **CuBr₂** | Cu→4b(P) | Br→4a/4d | ✅ |
| [Yang25] 2025 | **La₂O₃** | La→4b(P) 가정 | O→PS₄ 코너 | ✅ |
| [GaF₃] 2026 | **GaF₃** | Ga→4b(P) | F→4a/4d | ✅ |

**🔑 계보**: [GaF₃](*Energy Mater. Adv.* 2026;7:0227)가 **자리 배정(F→Cl 4a, M→P 4b)을 본편에서 그대로 인용**한다("According to previous reports…[34]"). 즉 **본편이 그 그룹의 자리 배정 원본**이고, GaF₃ 는 **3가 금속만 In→Ga 로 갈아 끼운 후속편**이다. 1저자 **Dabing Li** 는 GaF₃ 논문의 2저자이고, 공저 **Yang Li** 는 [Fan26] 리뷰의 제1저자이자 [Li25] CuBr₂ 의 제1저자, 교신 **Li-Zhen Fan** 은 [Fan26] 리뷰 교신저자다. **한 연구실의 네 번째 digest.**

### 0c. 우리 캠페인 관점 3줄

1. **In³⁺ 선택의 근거가 [Zhu20] = 우리가 SI 엑셀까지 전수 전사한 바로 그 논문이다** (본문 ref [20] = P. Zhu, Y. Mo, *Angew* **2020**, 59, 17472). 우리 `db/properties/zhu2020_si_hydrolysis_energies.csv` 로 검산하면 **In₂S₃ +0.599 eV (46종 중 9위)** > Li₂S +0.225 > **P₂S₅ −0.156** — 즉 **P→In 치환은 이성분 프록시에서 +0.755 eV 개선**이다. 논문 주장과 **방향 완전 일치**(§8c). ⚠ 단 이성분 프록시 (`kb/open_items.md` #11).
2. **우리 `+B₂O₃` 와는 축이 반대다.** 같은 [Zhu20] 표에서 **B₂S₃ = −0.901 eV (44/46위)** — B 는 가수분해 축 최하위군. 우리 B–S 안정화(free-S ⟨3p⟩ −1.14 → B–S −2.15 eV)는 **산화(전자구조) 축**의 성과지, 대기 축이 아니다 → **"동형 기전"은 절반만 맞다**(§8d).
3. **In/F 기여 분리를 우리가 완성해 줄 수 있다.** 이 논문은 **수분 축은 계산으로, 전도 축은 실험으로** 갈랐지만 **용매·Li 금속 축은 못 갈랐다**. 우리 cascade 는 **양이온 단독 투입**이라 In-only 를 자연히 만든다 → §8e 에 필요한 계산 3개를 적어 뒀다.

---

## 1. 한 줄 요약

Cl-rich argyrodite **Li₅.₇PS₄.₇Cl₁.₃** 에 **InF₃ 를 격자 공도핑**(`Li₅.₇₊₂ₓP₁₋ₓInₓS₄.₇Cl₁.₃₋₃ₓF₃ₓ`)하면 **In³⁺→P⁵⁺(4b, InS₄⁵⁻ 형성)** 과 **F⁻→Cl⁻(4a)** 가 서로 다른 축을 맡아, **x = 0.02 에서 σ 최고 5.6 mS cm⁻¹**(pristine 4.8), **x = 0.06 에서 σ_e 최저 2.94×10⁻⁹ S cm⁻¹ · CCD 최고 2.5 mA cm⁻² · 대칭셀 2000 h@0.5 / 1000 h@1 mA cm⁻²** 를 낸다. 대기(30 % RH 60 min H₂S **3.82 → 1.16 cm³ g⁻¹**)와 **유기용매 내성**(toluene/DCM/EtOAc 1 h 침지 후 σ 보존 **91/83/71 %** vs pristine **63/44/21 %**)이 함께 개선되고, DFT 는 이를 **H₂O 흡착E ↓0.32 eV**(In 0.12 + F 0.15, 초가법적)와 **toluene 흡착E −0.41 → −0.12 eV** 로 뒷받침한다. 이 SE 와 PIB 바인더로 **35 µm 필름**(σ 1.4 mS cm⁻¹, 면저항 2.9 Ω cm²)을 슬러리 캐스팅·열압으로 만들어 **LCO/Li 500 cyc 83.2 %** 와 **FeS₂/Li 410 Wh kg⁻¹** 를 시연했다.

---

## 2. 메타 / 동기 / 설계 계보

| 항목 | 내용 |
|---|---|
| Host | **Li₅.₇PS₄.₇Cl₁.₃** (Cl-rich; 우리 modelc Li₅.₄PS₄.₄Cl₁.₆ 와 근접, [GaF₃]/[Yang25] host Li₅.₅PS₄.₅Cl₁.₅ 와도 이웃) |
| 도핑식 | **`Li₅.₇₊₂ₓP₁₋ₓInₓS₄.₇Cl₁.₃₋₃ₓF₃ₓ`**, x = 0 / 0.02 / 0.04 / 0.06 / 0.08 / 0.10 (+ SI 0.15) |
| 전하균형 | ✓ 자기정합: In³⁺→P⁵⁺ ⇒ **+2 Li/In** (5.7+2x); F⁻↔Cl⁻ 등가 ⇒ Li 불변. **In:F = 1:3 = InF₃ 화학량론 그대로** |
| 조성 두 개를 쓴다 ⚠ | **x = 0.02** = `Li₅.₇₄P₀.₉₈In₀.₀₂S₄.₇Cl₁.₂₄F₀.₀₆` (**σ 챔피언 5.6**) / **x = 0.06** = `Li₅.₈₂P₀.₉₄In₀.₀₆S₄.₇Cl₁.₁₂F₀.₁₈` (**"LPSCInF" = 모든 안정성·셀 시험의 주인공**, σ 4.0). **헤드라인 σ 와 헤드라인 안정성이 서로 다른 시료**다 → §11-③ |
| 전구체·합성 | Li₂S(Alfa 99.9) · P₂S₅(Macklin 99) · LiCl(Sigma 99.9) · **InF₃(Aladdin)** → 볼밀 **500 rpm 10 h** → 밀봉 석영관 **480 °C 6 h** → 마노 유발 30 min. 필름용 정제: heptane 중 300 rpm 4 h + 진공 80 °C 8 h |
| 연구유형 | 실험 주 + **DFT 보조 5종**(자리 형성E · SE 슬랩 CI-NEB · Li/Li–In 슬랩 CI-NEB · H₂O·유기용매 흡착E · PDOS) |
| 설계 근거 (In) | 본문 ref **[20] = P. Zhu, Y. Mo, *Angew* 2020, 59, 17472 = 우리 [Zhu20] digest**. 원문: *"Based on the calculation results of Mo et al.,[20] **In³⁺ is the most promising cationic dopant** … because it has the **highest stability against moisture and reduction**"* |
| 설계 근거 (HSAB) | ref **[11] = R. G. Pearson, *JACS* 1963, 85, 3533** (HSAB 원전). 논문의 논리축: 극성용매(N·O 고립전자쌍) = 강 Lewis base ↔ **hard acid P⁵⁺** 가 표적 ⇒ **soft acid In³⁺** 로 바꾸면 공격이 약해진다 |
| 후속편 | [GaF₃] *Energy Mater. Adv.* **2026**;7:0227 — 본편을 ref [34] 로 인용해 **자리 배정을 그대로 승계** |
| 질문 | Cl-rich argyrodite 를 **한 염(InF₃)** 으로 공도핑해 **(a) σ 유지 (b) Li 금속 내성 (c) 대기·유기용매 내성** 을 동시에 얻고, 그 결과로 **슬러리 캐스팅 가능한 35 µm 박막**까지 갈 수 있나 |

---

## 3. 핵심 수치 총정리

> **판독 규율** — **[본문]** = 본문 인쇄값 · **[SI]** = SI 인쇄값 · **[figure-read ≈]** = 우리가 잘라낸 PNG 에서 직접 읽은 값(±0.02–0.05, **순위만 인용 권장**). 문헌 수치는 **소환값**이다 — 우리 db 절대값과 같은 표에 넣지 않는다.

### 3a. 구조 · 자리 (`Fig. 1`, `Fig. S1`–`S6`, `Table S1`)

| 항목 | 값 | 출처 |
|---|---|---|
| 공간군 | **F-43m** (cubic argyrodite), 참조 카드 **Li₇PS₆ PDF#34-0688** | [본문] `Fig. 1a` |
| 격자상수 a | **9.825 Å (x=0) → 9.856 Å (x=0.1)**, 단조 증가 (+0.32 %) | [본문] `Fig. S1` |
| 팽창 근거 | P⁵⁺ **38 pm** → In³⁺ **81 pm** (팽창) vs Cl⁻ **181 pm** → F⁻ **136 pm** (수축) ⇒ *"In³⁺ substitution plays a more significant role in crystal lattice than F⁻ doping"* | [본문] |
| ⚠ F⁻ 반경 불일치 | 구조 절 **136 pm** ↔ 수송 절 **119 pm** — **같은 논문 안에서 두 값** | [본문] §11-⑫ |
| 29–32.5° 확대 | 두 주피크가 x 증가에 따라 **저각으로 연속 이동** (Bragg 팽창) | [figure-read ≈ 0.1–0.15°] `Fig. 1a` 우측 |
| 2차상 (x > 0.08) | **LiCl · LiInS₂ · Li₈P₂S₉ · LiF** (용해도 한계) ⚠ `Fig. 1a` 에는 **LiInS₂(\*)·LiCl(♣) 만 실제로 표시**됨 — Li₈P₂S₉·LiF 는 본문 주장뿐 | [본문] + `Fig. 1a` 판독 |
| Rietveld (x=0.06) | **R_wp 4.61 % · R_p 1.18 %**, F-43m; ≈17° 할로는 **폴리이미드 테이프** | [본문] `Fig. 1b` |
| Raman PS₄³⁻ 주peak | **422.6 cm⁻¹ (x=0) → 417.3 cm⁻¹** (x↑, red-shift = 격자 팽창) | [본문] `Fig. S5a,b` |
| Raman 보조 밴드 | **187 cm⁻¹ = Li–S**, **310 cm⁻¹ = InS₄** | [본문] `Fig. S5c` |
| XPS S 2p | PS₄³⁻ **2p₁/₂ 162.5 · 2p₃/₂ 161.2 eV** / InS₄⁵⁻ **2p₁/₂ 163.9 · 2p₃/₂ 161.6 eV** ⚠ **후자는 스핀궤도 분리 2.3 eV = S 2p 로 불가능**(정상 1.18 eV) → §11-⑨ | [본문] `Fig. 1d` |
| XPS In 3d | In³⁺ **3d₅/₂ 444.4 · 3d₃/₂ 451.9 eV** | [본문] `Fig. S6b` |
| XPS F 1s | **684.5 eV** ("F-SEs" = 격자 F) | [본문] `Fig. 1e` |
| XPS P 2p | **131.8 / 132.7 eV** (PS₄³⁻) | [본문] `Fig. S6c` |
| 입도 | 볼밀 후 **≈3–5 µm**; EDS 로 P·S·In·F 균일 분포 | [본문] `Fig. 1f` |

**`Table S1` (x = 0.06 Rietveld) — 전수 기록 + 우리 검산**

| Atom | Wyckoff | x/a | y/b | z/c | Occ. |
|---|---|---|---|---|---|
| Li1 | **48h** | 0.3202 | 0.0183 | 0.6798 | 0.5050 |
| Cl1 | 4a | 0.0 | 0.0 | 1.0 | 0.4310 |
| Cl2 | 4d | 0.25 | 0.25 | 0.75 | 0.6880 |
| **F1** | **4a** | 0.0 | 0.0 | 1.0 | 0.0693 |
| **F2** | **4d** | 0.25 | 0.25 | 0.75 | 0.1107 |
| P1 | 4b | 0.0 | 0.0 | 0.5 | 0.942 |
| **In1** | **4b** | 0.0 | 0.0 | 0.5 | **0.058** |
| S1 | 4d | 0.25 | 0.25 | 0.75 | 0.3619 |
| S2 | 16e | 0.12 | −0.12 | 0.62 | 0.94 |
| S3 | 4a | 0.0 | 0.0 | 1.0 | 0.5781 |

**⚠⚠ 우리가 직접 검산한 것 (SI 엔 없다) — 이 표는 결정학적으로 성립하지 않는다**
- **조성은 명목값과 정확히 일치**: In **0.058**≈0.06 ✓ · F (4×0.0693+4×0.1107)/4 = **0.180** = 명목 F₀.₁₈ **정확** ✓ · Cl (4×0.4310+4×0.6880)/4 = **1.119** ≈ 1.12 ✓ · S (4×0.5781+4×0.3619+16×0.94)/4 = **4.700** = 명목 4.7 **정확** ✓ → **너무 정확해서 정련이 아니라 명목 고정(fixed)** 으로 보인다.
- **그 대가로 자리 점유 합이 1 을 넘는다**:
  - **4a**: Cl1 0.4310 + F1 0.0693 + S3 0.5781 = **1.0784 (+7.8 %)** ❌
  - **4d**: Cl2 0.6880 + F2 0.1107 + S1 0.3619 = **1.1606 (+16.1 %)** ❌
  - 4b: P 0.942 + In 0.058 = **1.000** ✓ (여기만 맞다)
- **Li 총량 초과**: 48 × 0.5050 / 4 = **6.06 Li/f.u.** vs 명목 **5.82** (**+4.1 %**). 게다가 **Li 가 전부 48h 뿐 — 24g 자리가 표에 아예 없다**(Cl-rich argyrodite 정련에서 24g 를 완전히 비우는 것은 이례적).
- ⇒ **`Table S1` 의 4a/4d S/Cl/F 분할은 인용하지 말 것.** 근본 원인은 [GaF₃] 편과 같다 — **lab XRD 는 S(Z=16)와 Cl(Z=17)을 사실상 구분 못 하고**, F(Z=9)·Li(Z=3)는 X-선 산란인자가 너무 작아 결정되지 않는다. 자리 정보의 실질 출처는 **XPS + DFT 형성에너지**이지 Rietveld 가 아니다.

### 3b. 이온전도 — **★ In/F 기여가 갈리는 축** (`Fig. 2a,b`, `Fig. S7`, `Fig. S8`)

| 시료 | 조성 | σ (25 °C) | 출처 |
|---|---|---|---|
| pristine LPSC | Li₅.₇PS₄.₇Cl₁.₃ | **4.8 mS cm⁻¹** | [본문] |
| **In-only** | **Li₅.₇₄P₀.₉₈In₀.₀₂S₄.₇Cl₁.₃** | **7 mS cm⁻¹** | ⭐ **[본문 인쇄]** *"the high ionic conductivity of **7 mS cm⁻¹** in the LPSC with only In substitution (`Fig. S8b`)"* (2026-08-06 정밀화 — 조성식만 SI) |
| **F-only** | **Li₅.₇PS₄.₇Cl₁.₂₄F₀.₀₆** | **4.3 mS cm⁻¹** | ⭐ **[본문 인쇄]** *"the ionic conductivity of F-only doped LPSC is **4.3 mS cm⁻¹**, which is slightly lower than that of pristine LPSC (`Fig. S8a`)"* (2026-08-06 정밀화) |
| co-doped x=0.02 | Li₅.₇₄P₀.₉₈In₀.₀₂S₄.₇Cl₁.₂₄F₀.₀₆ | **5.6 mS cm⁻¹** (최고) | [본문] |
| co-doped x=0.04 | — | ≈ 4.9 | [figure-read ≈] `Fig. 2b` |
| co-doped x=0.06 (**LPSCInF**) | Li₅.₈₂P₀.₉₄In₀.₀₆S₄.₇Cl₁.₁₂F₀.₁₈ | **4.0** | [본문] `Fig. 4a` "Before" |
| co-doped x=0.08 | — | ≈ 2.95 | [figure-read ≈] `Fig. 2b` |
| co-doped x=0.10 | — | ≈ 1.9 | [figure-read ≈] `Fig. 2b` |

> **⭐ `Fig. S8` 의 두 대조군은 dose-matched 다** — In-only 의 In 량(0.02)과 F-only 의 F 량(0.06)이 **co-doped x=0.02 의 In·F 량과 정확히 같다**. 즉 이 논문은 (의도했든 아니든) **2² 요인설계**를 갖고 있다. 정량 분해는 **§4b**.

**활성화에너지 (EIS Arrhenius, 25–80 °C)**

| x | Ea | 출처 |
|---|---|---|
| 0 | ≈ **0.303 eV** | [figure-read ≈] `Fig. 2b` |
| **0.02** | **0.29 eV** (전 시료 중 최저) | **[본문]** |
| 0.04 | ≈ 0.303 | [figure-read ≈] |
| 0.06 | ≈ 0.307 | [figure-read ≈] |
| 0.08 | ≈ 0.325 | [figure-read ≈] |
| 0.10 | ≈ 0.337 | [figure-read ≈] |

**논문이 대는 이유 (원문 그대로)**
- **F 는 σ 를 깎는다**: *"the substitution of F in SE **impairs the ionic conductivity** mainly due to the smaller ionic size of F⁻ (r(F⁻) = 119 pm, r(Cl⁻) = 181 pm) and the **stronger electrostatic attraction between F⁻ and Li⁺**, resulting in a **lower polarization rate**. The shorter and stronger chemical bond of strong F⁻ with Li⁺ leads to local distortion in the Li⁺ coordination environment, which **increases the energy barrier for Li⁺ migration**."*
- **In 은 σ 를 올린다**: *"doping In³⁺ with the lower valence in place of P⁵⁺ … increases the Li⁺ carrier concentration and generates **more vacancies to transport ions**"* + NEB 로 *"In doping significantly reduces the migration energy barrier from **0.662 to 0.236 eV**"*.

### 3c. 전자전도 σ_e · CCD — **역상관의 4번째 표** (`Fig. 2c`, `Fig. S10`, `Fig. S11`)

| x | σ_e (25 °C) | CCD (mA cm⁻²) |
|---|---|---|
| 0 | ≈ **1.77×10⁻⁸ S cm⁻¹** [figure-read ≈] | **1.0** [본문] |
| 0.02 | ≈ 6.9×10⁻⁹ [figure-read ≈] | ≈ 1.4 [figure-read ≈] |
| 0.04 | ≈ 5.6×10⁻⁹ [figure-read ≈] | ≈ 2.0 [figure-read ≈] |
| **0.06** | **2.94×10⁻⁹ (최소)** [본문] | **2.5 (최대)** [본문] |
| 0.08 | ≈ 6.3×10⁻⁹ [figure-read ≈] | ≈ 1.9 [figure-read ≈] |
| 0.10 | ≈ 8.7×10⁻⁹ [figure-read ≈] | ≈ 1.7 [figure-read ≈] |
| 0.15 | ≈ 9.0×10⁻⁹ [figure-read ≈] | ≈ 1.5 [figure-read ≈] |

**`Fig. S11` 은 두 축이 완벽한 거울상**이다 — σ_e 최소와 CCD 최대가 **둘 다 x = 0.06** 에서, 그리고 전 구간 단조 반대. **σ_e ↓ → CCD ↑ 역상관의 litdb 내 4번째 독립 재현**([Taklu] CuCl · [Li25] CuBr₂ · [GaF₃] 에 이어; 유일 반례는 [Yang25]).
- σ_e 개선폭 **≈6× 감소**, CCD 개선폭 **2.5×**.
- 필름 상태에서는 **σ_e = 8.31×10⁻¹⁰ S cm⁻¹** 로 더 낮다 [본문, `Fig. S30`].

### 3d. 전기화학 창 · 전자구조 (`Fig. 2d,e,f`, `Fig. S18`)

| 항목 | LPSC | LPSCInF | 조건 |
|---|---|---|---|
| CV 산화 피크 | **≈2.6 V** vs Li⁺/Li | 같은 위치, **전류 크게 감소** | Li/SE/SE+C(7:3), **0.1 mV s⁻¹**, 0→5 V [본문] `Fig. 2d` |
| CV 환원 피크 | **1.2 V** | 같은 위치, 전류 감소 | 동상 |
| **PDOS 밴드갭** | **1.78 eV** | **2.75 eV** | DFT PBE, **DOS 문턱 판독** [본문] `Fig. 2e,f` |
| SEI 산물 갭 | **LiF 7.4 eV** ("electronic insulator") | — | [본문] `Fig. S18` (Li₂S·Li₃P·LiCl 은 값 미인쇄) |

⚠ **CV 는 onset 이 아니라 진폭 논증이다.** `Fig. 2d` 를 실제로 보면 두 곡선의 산화/환원 **밴드 위치가 같고**, 달라지는 것은 **전류 크기**뿐이다. 본문이 이를 *"wide-voltage window stability"* 로 표현하지만 **창이 넓어졌다는 증거는 그림에 없다** → §11-⑤. (그림 라벨 *"Reduce to PS₄³⁻" / "Oxidize to PS₄³⁻"* 도 오기 — PS₄³⁻ **를** 환원/산화한다는 뜻이어야 한다.)

### 3e. 대기 안정성 (`Fig. S20`–`S22`)

| 시료 | H₂S @ 60 min (30 % RH, 25 °C) | 출처 |
|---|---|---|
| x = 0 (pristine) | **3.82 cm³ g⁻¹** | [본문] |
| x = 0.02 | **1.73** (−55 %) | [본문] |
| x = 0.06 | **1.16** (−70 %) | [본문] |
| x = 0.15 | **1.10** ("slightly lower than x=0.06") | [본문] |

- **10 min 대기 노출 후 σ**: LPSCInF **2.5 mS cm⁻¹** vs LPSC **0.24 mS cm⁻¹** (**10.4× 차이**) [본문, `Fig. S21`]
- **H₂O 흡착 자유에너지 ΔE_ads** (규약: `E_surf + E_H₂O − E_복합체`, **양수 = 발열 = 흡습 강함**, 값이 **작을수록 좋다**):

| 표면 | Li1 (24g) | Li2 (48h) | 평균 감소 |
|---|---|---|---|
| pristine LPSC (001) | ≈ **0.64 eV** | ≈ **0.52 eV** | — |
| **In-only** | ≈ 0.52 | ≈ 0.40 | **−0.12 eV** [본문] |
| **F-only** | ≈ 0.49 | ≈ 0.365 | **−0.15 eV** [본문] |
| **In–F co-doped** | ≈ **0.32** | ≈ **0.20** | **−0.32 eV** [본문] |

값은 [figure-read ≈] (`Fig. S22`), 감소량은 [본문] 인쇄값. **두 소스가 정확히 일치**한다(0.64−0.52=0.12, 0.64−0.49=0.15, 0.64−0.32=0.32) → 판독 신뢰도 높다.
⚠ **모든 값이 여전히 양수** = 여전히 흡습성이다. "소수성이 됐다"가 아니라 "덜 끌어당긴다"이다.
⚠ **규약이 [Fan26] 리뷰(−1.63 eV)·[Li25](0.29→2.42)와 부호·정의가 다르다 — 절대값 교차인용 금지.**

### 3f. 유기용매 안정성 — **리뷰가 인용한 그 데이터** (`Fig. 4`, `Fig. S23`, `Fig. S24`)

**프로토콜** [SI Methods]: SE 와 용매를 **1:1 질량비 슬러리로 섞고 → 말린 뒤** σ 변화 측정. 노출 **1 h**, **25 °C** (`Fig. S23` 캡션). XRD·Raman 은 **toluene 1 h** 침지 전후.

| 용매 (polar index) | LPSC σ (mS cm⁻¹) | 보존율 | LPSCInF σ | 보존율 |
|---|---|---|---|---|
| **Before** | **4.8** | 100 % | **4.0** | 100 % |
| **Toluene (2.4)** | **3.0** | **62.5 %** (본문 −37.5 %) | **3.65** | **91.3 %** (본문 −8.75 %) |
| **Dichloromethane (3.4)** | **2.1** | **43.7 %** (본문 −56.3 %) | **3.3** | **82.5 %** (본문 −17.5 %) |
| **Ethyl acetate (4.3)** | **1.0** | **20.8 %** (본문 −79.2 %) | **2.85** | **71.2 %** (본문 −28.8 %) |

값은 `Fig. 4a` 에 **숫자로 인쇄**돼 있고 본문 % 와 완전 정합. ⚠ **출발점이 다르다**(4.8 vs 4.0) — 공도핑 시료는 **초기 σ 를 17 % 팔아** 내성을 산다. 교차점은 toluene 부터.

**DFT 흡착에너지 E_ad** (규약: `E_복합체 − E_SE − E_용매`, **음수 = 결합, 더 음수 = 강한 상호작용**)

| 계 | LPSC | LPSCInF | 출처 |
|---|---|---|---|
| **Toluene @ (001)** | **−0.41 eV** | **−0.12 eV** | [본문] `Fig. 4b,c` ← **리뷰가 인용한 값** |
| Dichloromethane @ P-site | ≈ **−0.82** [figure-read ≈] | **−0.30 eV** [본문] | `Fig. S24b` |
| Ethyl acetate @ P-site | ≈ **−1.85** [figure-read ≈] | **−0.69 eV** [본문] | `Fig. S24b` |

**LPSC 자리별 흡착 스캔 (ethyl acetate 의 O 원자 기준)** [figure-read ≈] `Fig. S24a`:
**P −1.85 ≪ S −1.31 < Li −1.04 < Cl −0.66 eV** ⇒ *"the maximum adsorption energy is found between the **P site** … the site with the largest adsorption energy is the best adsorption site"* → **P 가 공격 표적**이라는 것이 이 논문의 정량 근거다.

**구조 증거 (toluene 1 h 후)**
- **Raman `Fig. 4d`**: pristine 의 PS₄³⁻ 422.6 cm⁻¹ **세기 급감 + 고파수 이동** ↔ LPSCInF **거의 불변**.
- **XRD `Fig. 4e`**: pristine → **Li₄P₂S₆ · Li₃P · LiCl** 새 피크 출현 ↔ LPSCInF → **변화 없음**(Li₇PS₆ PDF#34-0688 유지).
- **만화 `Fig. 4f`**: `PS₄ + C₇H₈ → P₂S₆ + Li₃P` (attack) vs `InS₄ + C₇H₈ → ✗ No decomposition Product`.

### 3g. Li 금속 계면 (`Fig. 3`, `Fig. S12`–`S19`)

| 항목 | LPSC (x=0) | LPSCInF (x=0.06) |
|---|---|---|
| CCD | **1.0 mA cm⁻²** | **2.5 mA cm⁻²** |
| 대칭셀 @ 0.5 mA cm⁻² | **75 h 에 단락** (`Fig. S12`) | **2000 h 안정** (`Fig. 3d`) ✅ **본문·그림·`Table S2` 3자 일치**(2026-08-06 재검증 — 이전 "본문 800 h" 지적은 **철회**, §14a) |
| 대칭셀 @ 1 mA cm⁻², 1 mAh cm⁻² | — | **>1000 h** (`Fig. S14`) |
| x=0.02 대칭셀 | — | >750 h (`Fig. S13`) |
| 분극 전압 | **23 → 101 mV** (증가) | **22 mV 평탄** |
| Li/SE/Li EIS | 163 → **312 Ω** (48 h, 계속 증가) | 24 h 증가 후 **≈175 Ω 로 안정**(72 h) (`Fig. S15`) |
| 순환 후 Li 표면 SEM | **mossy 덴드라이트** (`Fig. S16c`) | **덴드라이트·균열 없음** (`Fig. S16b`) |

**순환 50 h 후 XPS** [본문] `Fig. 3e,f`
- **F 1s**: pristine "F-SEs" **684.5** → cycled **"LiF" 684.8 eV**
- **In 3d**: In³⁺ 444.4/451.9 (유지) + **In⁰ 443.0/450.7** + **Li–In alloy 441.3/448.1 eV** (신규)
- ⇒ 서사: **F → in-situ LiF (전자 절연 SEI, gap 7.4 eV)** + **In → Li–In 합금 (빠른 Li 표면확산)**

**Li 금속/합금 슬랩 NEB** [본문] `Fig. 3g,h` · `Fig. S19`
- 순수 **Li (100) 표면 확산 장벽 0.38 eV** → **Li–In 합금 (110) 0.17 eV** (`Fig. S19b`: Li–In (100) 0.23 eV)
- Li–In 합금 표면에너지: **(100) 0.50 / (110) 0.40 / (111) 0.51 eV Å⁻²** ⇒ (110) 채택
- 인용값: Li–In 합금상 D_Li ≈ **10⁻⁸–10⁻⁶ cm² s⁻¹** vs Li 금속 벌크 **5.69×10⁻¹¹** (refs [30][31])

### 3h. 필름 · 풀셀 (`Fig. 5`, `Fig. 6`, `Fig. S25`–`S34`, `Table S3`, `Table S4`)

| 항목 | 값 |
|---|---|
| 바인더 | **PIB (polyisobutylene, Mw ≈ 800,000)**, anhydrous toluene 5 wt% 용액, SE:용액 **1:1 질량** |
| 공정 | doctor blade on **50 µm PET** → 캘린더 **35 µm** → 진공 100 °C overnight → **냉간 100 MPa 5 min** → ⌀10 mm |
| FTIR | **2950.6 · 1468.5 cm⁻¹ = PIB 의 C–H** / **569.8 cm⁻¹ = P–S** (`Fig. S25b`) |
| 필름 σ | **1.4 mS cm⁻¹** @ 25 °C (분말 4.0 대비 **−65 %**) · **Ea 0.33 eV** |
| 면적 지표 | 면전도 **274 mS** · **면저항 2.9 Ω cm²** |
| 필름 σ_e | **8.31×10⁻¹⁰ S cm⁻¹** |
| 필름 대칭셀 | **>400 h** @ 0.5 mA cm⁻², 0.5 mAh cm⁻² (`Fig. S29`) |
| **LCO/필름/Li** | 8.9 mg cm⁻², 2.8–4.3 V, 0.1 C, 25 °C: **135.7 mAh g⁻¹**, ICE **86.2 %**, **500 cyc 83.2 %** · EIS 223.5 → 330.6 Ω (100th → 500th) |
| 율속 (1.8 mg cm⁻²) | **139.2 / 136.6 / 133.3 / 125.7 / 111.6 mAh g⁻¹** @ 0.1/0.2/0.3/0.5/1 C, 0.3 C 복귀 **131.5** |
| 대기내성 실증 | **80 °C 1 h 노출 후** 134.7 → **127.8 mAh g⁻¹** (−5 %만) |
| µSi 음극 셀 | N/P 1.2, 0.5 C: **105.1 mAh g⁻¹**, ICE **70.2 %**, **100 cyc 95.8 %** (`Fig. S32`) |
| **FeS₂/필름/Li** | 5.0 mg cm⁻², 1–3 V, 60 °C, 0.1 C: **834.1 mAh g⁻¹**, ICE **96.9 %**, **100 cyc 91.3 %**; 평탄부 **2.2 · 1.5 V** |
| FeS₂ 율속 (1.27 mg cm⁻²) | 819.7 / 785.2 / 779.7 / **763.0 mAh g⁻¹** @ 0.1–0.5 C (0.5 C 에서 **93.1 %** 유지) |
| **에너지밀도** (`Table S3`) | **410 Wh kg⁻¹** · **526.7 Wh L⁻¹** · 면용량 **4.17 mAh cm⁻²** · N/P **4.84** · 평균 2.1 V · 총질량 16.78 mg · 총부피 0.0131 cm³ |

**`Table S2` — 문헌 벤치마크 (전수 기록)** ⚠ **σ·CCD 비교표이므로 우리 db 와 같은 표에 넣지 않는다**

| 전해질 | σ (mS cm⁻¹) | CCD (mA cm⁻²) | 도금 전류 | 사이클 | 우리 litdb |
|---|---|---|---|---|---|
| Li₅.₆P₀.₈Si₀.₂S₄.₄Cl₁.₆ | 4.0 | 1.9 | 1 | 1000 | — |
| Li₆.₅In₀.₂₅P₀.₇₅S₅I | 1.06 | – | 0.2 | 1000 | **In-치환 선행** |
| Li₆.₂₅PS₄Cl₀.₇₅O₁.₂₅ | 2.8 | 1 | 2 | 100 | — |
| Li₅.₆Cu₀.₂PS₄.₈Br₁.₂ | 3.65 | 1.2 | 0.2 | 1200 | **= [Li25] CuBr₂** ✅ |
| Li₃.₂P₀.₈Sn₀.₂S₄ | 1.21 | – | 0.1 | 600 | — |
| Li₇P₃S₁₁-0.05Mo | 2.5 | 0.96 | 0.5 | 50 | — |
| Li₂.₉₆P₀.₉₈S₃.₉₂O₀.₀₆-Li₃N | 1.58 | 1 | 0.5 | 1000 | — |
| Li₆.₂₅PS₄.₇₅N₀.₂₅Cl | 1.3 | 1.52 | 0.5 | 1000 | — |
| **Li₆PS₅Cl₀.₃F₀.₇** | **0.71** | – | 1.27 / 6.37 | 636 / 159 | ⭐ **F-only 순수 치환 = σ 붕괴 외부 증거** (§4b) |
| Li₆.₃P₀.₉Mg₀.₁S₅Cl₀.₈F₀.₂ | 1.70 | 1.4 | 0.1 | 1800 | **= [Liu23] MgF₂** ✅ |
| LiF@Li₁₀GeP₂S₁₂ | 2.54 | 3 | 0.1 | 1000 | — |
| 0.7(0.75Li₂S-0.25P₂S₅)−0.3LiI | 1.8 | 3.9 (100 °C) | 1.5 | 200 | — |
| **This work** Li₅.₈₂P₀.₉₄In₀.₀₆S₄.₇Cl₁.₁₂F₀.₁₈ | **4.0** | **2.5** | 0.5 / 1 | **2000 / 1000** | — |

⚠ `Fig. 3c` 의 산점도는 **CCD vs "capacity"** 인데, capacity = CCD × (스텝 시간)이라 **거의 같은 양을 두 축에 그린 것**이고, 스텝 시간이 논문마다 달라 **직접 비교가 성립하지 않는다** → §11-⑧. 그 그림에 **Li₅.₄PS₄.₄Cl₁.₆ (= 우리 modelc 조성)이 CCD ≈0.55 mA cm⁻² 로 최하점**에 찍혀 있다.

---

## 4. ★★ In 기여 vs F 기여 — **전용 절** (리뷰어 노트 A13 판정)

### 4a. ① **논문이 In 과 F 를 분리했나 — 대조군 대장**

| 축 | 대조군 구성 | 분리 가능? | 어디 |
|---|---|---|---|
| **이온전도 σ** | pristine · **In-only(In₀.₀₂)** · **F-only(F₀.₀₆)** · co-doped(x=0.02) — **dose-matched 2² 요인설계** | **✅ 완전 분리 (실험)** | `Fig. S8a,b` + 본문 |
| **수분 (H₂O 흡착E)** | pristine · **In-doped** · **F-doped** · **In–F co-doped** (001) 슬랩 4종 | **✅ 완전 분리 (계산)** | `Fig. S22` + 본문 |
| **유기용매 (σ 보존·E_ad)** | **pristine · co-doped 2점뿐** | **❌ 분리 불가** | `Fig. 4a`, `Fig. S24b` |
| **H₂S 발생량** | x = 0 / 0.02 / 0.06 / 0.10 / 0.15 — **x 를 바꾸는 시리즈뿐** | **❌ 분리 불가** | `Fig. S20` |
| **CCD · σ_e** | x 시리즈뿐 | **❌ 분리 불가** | `Fig. S11` |
| **Li 금속 계면** | pristine · co-doped 2점뿐 (XPS 도 co-doped 만) | **❌ 분리 불가** | `Fig. 3`, `Fig. S12`–`S17` |
| **자리 배정 (E_f)** | In 3자리 / F 4자리 각각 스캔 | ✅ (자리 선택 문제라 원래 분리돼 있음) | `Fig. S4a,b` |

> **⇒ 정답: "조성 시리즈뿐이라 분리 불가"는 틀렸다. 이 논문은 σ 와 수분 두 축은 갈랐다.**
> **그러나 리뷰가 실제로 인용한 축(= 유기용매 침지 후 σ 유지)에는 단일 도펀트 대조군이 없다.**
> 이것이 A13 의 정확한 사정거리다 — **"이 계열은 전부 못 갈랐다"가 아니라 "이 논문조차 가장 중요한 축에서만 안 갈랐다"** 가 더 강하고 정확한 지적이다.

### 4b. **In/F 정량 분해 — 우리가 직접 계산한 것**

**(i) 이온전도 (2² 요인, `Fig. S8` + 본문, 전부 x=0.02 수준으로 dose-matched)**

| 인자 | σ (mS cm⁻¹) | pristine 대비 |
|---|---|---|
| — (pristine) | 4.8 | — |
| **In only** | **7.0** | **+2.2 (+46 %)** |
| **F only** | **4.3** | **−0.5 (−10 %)** |
| In + F (실측) | **5.6** | **+0.8 (+17 %)** |
| In + F (**가법 예측**) | 4.8 + 2.2 − 0.5 = **6.5** | — |
| **상호작용항** | **5.6 − 6.5 = −0.9 mS cm⁻¹** | **하가법(sub-additive)** |

**⇒ σ 축의 부호 귀속은 명확하다: In 이 올리고, F 가 깎는다. 그리고 둘을 같이 넣으면 In 의 이득이 절반 이상 잠식된다.**
- **외부 교차검증**: `Table S2` 의 **Li₆PS₅Cl₀.₃F₀.₇ = 0.71 mS cm⁻¹** (F 를 대량 넣은 순수 F 치환 argyrodite) — F 가 σ 를 무너뜨린다는 독립 증거.
- **litdb 내 교차검증**: [GaF₃] 편 σ = pristine 5.6 / **Ga-only 6.4** / **F-only 2.3** / co 4.5 → **완전히 같은 부호 구조**. [Liu23] Mg-only 3.51 → MgF 1.70 도 같다.
- ⚠ 단일 시료·단일 측정, 오차막대 없음 → **부호와 순위만** 인용하고 상호작용항 −0.9 는 "하가법 경향" 수준으로만.

**(ii) 수분 흡착 (`Fig. S22`, ΔE_ads 감소량, 값이 작을수록 좋다)**

| 인자 | Δ(감소량) |
|---|---|
| **In only** | **0.12 eV** |
| **F only** | **0.15 eV** |
| 가법 예측 | 0.27 eV |
| **In + F (실측)** | **0.32 eV** |
| **상호작용항** | **+0.05 eV (초가법, super-additive)** |

**⇒ 수분 축에서는 F 기여(0.15)가 In 기여(0.12)보다 크다.** 논문 자신이 이렇게 쓴다: *"Compared to F atoms, **In atom doping has a lower effect on ΔE_ads**, probably due to the four surrounding S atoms inhibiting the direct interaction between In and Li atoms."*
- ⚠ 즉 **"InF₃ = In 덕분"이라는 통념은 적어도 대기 축에서는 논문 자신의 데이터와 어긋난다.**
- ⚠ 두 축의 담당자가 반대다: **σ 는 In 이 이득·F 가 손해**, **수분은 F 가 In 보다 이득**. **한 문장으로 "InF₃ 가 좋다"고 말하면 이 반전이 지워진다.**

**(iii) 유기용매 — 분해 불가, 그러나 논문 서사는 100 % In 쪽이다** → §4c

### 4c. ② **논문이 주장하는 기전 — 축별로 담당이 다르다**

| 축 | 논문의 기전 | 담당 원소 | 증거 |
|---|---|---|---|
| **σ ↑** | In³⁺(3가) 이 P⁵⁺(5가) 자리에 → Li 캐리어·공공 증가; NEB 장벽 0.662 → 0.236 eV | **In** | NEB `Fig. S9b` + Fig S8b |
| **σ ↓ (부작용)** | F⁻ 가 작고(119 pm) Li⁺ 와 정전인력 강 → 국소 왜곡 → 이동 장벽↑, **"lower polarization rate"** | **F** | `Fig. S8a` + ref [24] |
| **수분 ①** | H₂O 흡착 시 Li–S 의 전자가 O 로 넘어가 Li–O 공유결합 형성 → H₂S. **Li–F 결합이 강해 그 전자를 덜 내준다** | **F** | ΔE_ads −0.15 eV |
| **수분 ②** | **HSAB: soft acid In³⁺ 와 soft base S²⁻ 의 tight binding** ⇒ S 가 안 떨어진다 | **In** | ΔE_ads −0.12 eV + ref [11][34] |
| **유기용매** | 극성용매의 고립전자쌍(N·O)이 **hard acid P⁵⁺** 를 친핵 공격 → P–S 절단. **soft acid In³⁺ 로 바꾸면 그 공격이 약해진다** ⇒ `PS₄ → P₂S₆ + Li₃P` vs `InS₄ → 무분해` | **In (100 %)** | E_ad −0.41 → −0.12 eV; 자리 스캔에서 **P 자리가 최강 흡착점**; `Fig. 4f` 만화 |
| **Li 금속 ①** | 순환 중 **in-situ LiF** 생성(gap 7.4 eV) → 전자 절연 SEI → 덴드라이트 억제 | **F** | XPS `Fig. 3e` + `Fig. S18` |
| **Li 금속 ②** | 순환 중 **Li–In 합금** 생성 → 표면 Li 확산 0.38 → 0.17 eV → 균일 도금 | **In** | XPS `Fig. 3f` + NEB `Fig. 3g,h` |

**⚠ 여기 논리적 구멍이 하나 있다 (§11-⑦ 과 연결).**
`Fig. 4f` 만화는 "PS₄ 는 공격받고 InS₄ 는 안 받는다"로 읽히는데, **x = 0.06 에서 사면체의 94 % 는 여전히 PS₄ 다.** 그리고 `Fig. S24b` 는 co-doped 계에서도 **"P-site"** 흡착에너지를 계산해 −1.85 → −0.69 eV 로 줄었다고 보고한다 — 즉 **개선의 실체는 "In 이 취약한 P 를 대체했다"가 아니라 "In 이 이웃 P 의 전자 환경을 바꿨다"**(2차 근접 효과)여야 한다. 논문은 이 구분을 하지 않는다.

### 4d. ③ **"lattice bond energy / reduces polarizability" — 원문 대조 결과**

**원문 전수 검색 (본문 12 pp + SI):**

| 검색어 | 본문 | SI |
|---|---|---|
| `polarizability` | **0회** | 0회 |
| `bond energy` / `bond strength` | **0회** | 0회 |
| `lattice energy` | **0회** | 0회 |
| `polariz-` (전체) | 5회 — ① 그림 캡션 "Direct-current **polarization** curves" ② 방법 "direct current **polarization** measurements" ③ **"lower polarization rate"** ④ "**polarization** voltage 23 → 101 mV"(과전압) ⑤ "calculated from the **polarization** curves" | 2회 (모두 DC 분극 측정법) |

> ### 판정
> **리뷰 문장의 *"enhances lattice bond energy and reduces polarizability"* 는 이 논문에 없는 표현이다.** 리뷰가 붙인 **해석/의역**이고, 그것도 **원문의 인과를 뒤집었다**:
> - 이 논문에서 **"polarization rate 가 낮아진다"** 는 것은 **F⁻ 가 Li⁺ 를 세게 붙들어 σ 를 깎는 이유**로 등장한다 — **불이익**이다.
> - 리뷰는 그것을 **"분극률을 낮춰서 용매 침지 후에도 σ 를 유지한다"** 는 **이익**으로 옮겨 붙였다. **같은 물성이 두 문장에서 반대 부호로 쓰인 셈**이다.
> - **"lattice bond energy"** 에 대응할 정량량은 이 논문에 **존재하지 않는다**. 가장 가까운 것은 (a) 정성적 HSAB 서술("tight binding between soft acid In³⁺ and soft base S²⁻"), (b) **자리 형성에너지 E_f** (`Fig. S4`, 도핑 열역학이지 결합에너지가 아님), (c) **분자–표면 흡착에너지 E_ad / ΔE_ads** (격자 결합에너지가 **아니다**). 셋 중 어느 것도 "lattice bond energy" 가 아니다.
>
> **⇒ 리뷰어 노트 A12("어떻게 쟀는지 없다")는 실물로 확정된다. 답은 "재지 않았다 — 원 논문에 그 양이 없다"이다.**

### 4e. ④ **용매 침지 조건 전수 + 리뷰 Figure 4c 매핑**

| 항목 | 값 |
|---|---|
| 시료 | pristine **Li₅.₇PS₄.₇Cl₁.₃** vs **Li₅.₈₂P₀.₉₄In₀.₀₆S₄.₇Cl₁.₁₂F₀.₁₈** (x = 0.06) |
| 용매 | **toluene** (polar index 2.4) · **dichloromethane** (3.4) · **ethyl acetate** (4.3) |
| 비율 | **SE : 용매 = 1:1 질량** 슬러리 |
| 절차 | 혼합 → **건조** → σ 재측정 (즉 "침지 후 회수" 조건이지 in-situ 아님) |
| 시간 | **1 h** |
| 온도 | **25 °C** (`Fig. S23` 캡션) |
| σ 보존율 | **co-doped 91.3 / 82.5 / 71.2 %** vs **pristine 62.5 / 43.7 / 20.8 %** |
| 구조 증거 | Raman·XRD **toluene 1 h** 만 |
| ⚠ 미실시 | NMP·THF 등 **고 donor-number 용매 없음** (리뷰 §3.2 의 주 논증 대상인 NMP 는 시험 안 됨) · 다른 온도·시간 없음 · **In-only/F-only 대조 없음** |

**리뷰 Figure 4c 매핑** — [Fan26] digest 는 그 패널을 *"InF₃-LPSCl 용매내성(E_ad −0.12 eV; PS₄→P₂S₆+Li₃P vs InS₄ 무분해)"* 로 기록한다. 그 두 요소는 이 논문의
- **E_ad −0.12 eV** = **`Fig. 4c`** (LPSCInF 슬랩 + toluene; 짝은 `Fig. 4b` LPSC −0.41 eV)
- **PS₄→P₂S₆+Li₃P vs InS₄ 무분해 만화** = **`Fig. 4f`**
- (리뷰 문장의 *"maintain high ionic conductivity"* 근거 데이터는 **`Fig. 4a`**)

⇒ **리뷰 Fig 4c 는 이 논문 `Fig. 4b,c,f` 의 재구성**이다. 리뷰가 σ 보존 데이터(`Fig. 4a`)를 실제로 실었는지는 원고 실물로 확인 필요.

### 4f. **그래서 A13 을 어떻게 쓸 것인가 (§13 에서 다시)**

- **"기여 분리를 요구"만 하면 반박당한다** — 저자들은 `Fig. S8`(σ)과 `Fig. S22`(수분)를 들어 "우리는 갈랐다"고 답할 수 있다. 게다가 이 논문은 **리뷰 교신저자 본인의 논문**이다.
- **강한 형태**: *"인용된 축(유기용매 내성)에는 단일 도펀트 대조군이 없고, 같은 논문의 다른 두 축에서는 **In 과 F 의 부호가 서로 반대**(σ: In↑/F↓, 수분: F>In)다. 통합 문장은 그 반전을 지운다."* → **정확하고, 저자 자신의 데이터로만 구성돼 있어 반박 불가**.

---

## 5. DFT / 계산 방법 ★ (SI Computational Section 전문 + 우리 감사)

### 5a. 인쇄된 것 전부

- **code**: **VASP** (ref [1] Kresse & Furthmüller PRB 1996 54, 11169). 버전 미기재
- **functional**: **PBE (GGA)** (ref [2]). **vdW/분산 보정 언급 없음** ⚠
- **pseudo**: **PAW** (ref [3] Blöchl 1994). POTCAR 버전·valence 미기재
- **ecut**: **450 eV** (파동함수)
- **supercell / nat**: **Li₅.₇PS₄.₇Cl₁.₃ 의 1×1×1 셀**. 만드는 법: *"Li₆PS₅Cl 구조에서 Li 1 개와 S 1 개를 지우고, Li₆PS₅Cl 안에서 가장 에너지가 낮은 자리에 Cl 1 개를 더했다. 여러 구조를 만들어 본 결과 최저에너지 구조는 **4a 자리 S 를 Cl 로 치환**한 것이었다."* ⇒ 우리 검산: Li₆PS₅Cl 관용셀 52 원자(Z=4) → −1 Li −1 S +1 Cl = **51 원자, Li₂₃P₄S₁₉Cl₅ = Li₅.₇₅PS₄.₇₅Cl₁.₂₅** (명목 Li₅.₇PS₄.₇Cl₁.₃ 의 반올림판)
- **수렴**: 벌크 이완 힘 **< 0.01 eV/Å**; 슬랩은 **상위 4 층만 이완, 힘 < 0.03 eV/Å**; **진공 15 Å**
- **NEB**: **CI-NEB** (ref [4] Henkelman & Jónsson 2000), ecut 450 eV, 에너지 **10⁻⁵ eV** · 힘 **0.03 eV/Å**
- **형성에너지** (부호 규약 주의):
  - `E_f = E_base − E_In-doped + E_In − E_P/Li` (Eq S1) — ***"A larger positive E_f value indicates a more stable doping site"***
  - `E_f = E_In-doped − E_In-F-doped + E_F − E_S/Cl` (Eq S2)
- **H₂O 흡착**: `ΔE_ads = E_surf + E_H₂O − E_복합체` (Eq S3) — **양수 = 발열 = 흡습 강함**
- **유기용매 흡착**: `E_ad = E_복합체 − E_SE − E_용매` (Eq S4) — **음수 = 결합**
- **Li 금속 슬랩**: 순수 Li = **4 층 4×4×1 Li(100)**; Li–In 합금 = **1×1×1 Li(110) + 최상층 In 1 개**
- **무질서 처리**: **단일 최저에너지 배열** (수동 소규모 탐색). SQS·enumerate·앙상블 평균 **없음**

### 5b. **없는 것** (⚠ 재현 불가 항목 — [GaF₃] 편과 거의 동일한 구멍)

| 미기재 | 왜 중요한가 |
|---|---|
| **k-mesh** | 51 원자 셀에서 Γ-only 인지 아닌지에 따라 **PDOS 갭이 0.2–0.3 eV 흔들린다**. 우리 규율(fixed-occ nscf) 과 대조 불가의 1차 원인 |
| **vdW/분산 보정** | ⚠⚠ **가장 치명적.** toluene 은 **비극성 방향족** — 표면 흡착이 사실상 **분산력 지배**다. **순수 PBE 는 분산을 거의 못 잡아** E_ad 를 크게 과소평가한다. **−0.41 / −0.12 eV 라는 절대값과 그 차이가 함수형 인공물일 가능성**을 배제할 수 없다 → §11-① |
| **표면 종단(termination)** | (001) 슬랩을 Li-종단으로 잘랐는지 S/Cl-종단인지에 따라 흡착에너지가 eV 단위로 바뀐다 |
| **dipole correction** | 비대칭 슬랩(상위 4 층만 이완)에서 필수 |
| **원자 수·NEB 이미지 수** | `Fig. S9b` 프로파일이 9 점처럼 보이는데 명시 없음 |
| **spin / smearing / DFT+U** | 전부 미기재 (In 5s·F 2p 계는 U 불필요하나 명시가 원칙) |
| **(001)/(010)/(100) 표기** | `Fig. S3` 캡션은 **(100)**, 흡착은 **(001)**, NEB 는 **(010)** — F-43m 에서는 동등하지만 논문이 서로 다르게 부른다 |
| **DFT 도핑 농도 vs 실험** | 1×1×1 셀에 P 는 **4 개**뿐 → In 1 개 = **In 25 %**. 실험 x = 0.02–0.06 (**2–6 %**) 대비 **4–12× 과도핑**. F 는 Cl 5 개 중 1 개 = 20 % vs 실험 14 % (이쪽은 근접) → §11-④ |

### 5c. 후처리 / 도구

- **CI-NEB** — SE 슬랩 Li 48h→48h 1 경로 · Li(100) 1 경로 · Li–In(110) 1 경로 · Li–In(100) 1 경로 (도구 미기재, VTST 추정)
- **PDOS** — LPSC / LPSCInF (`Fig. 2e,f`) + 이성분 Li₂S·Li₃P·LiCl·LiF (`Fig. S18`). **갭은 DOS 문턱 판독**(우리 규율 위반 방식) — 도구 미기재(VASPKIT 추정)
- **표면에너지** — Li–In 합금 (100)/(110)/(111)
- **흡착에너지** — H₂O(2 자리 × 4 표면) + toluene/DCM/EtOAc(자리 4 × 표면 2)
- **형성에너지** — In 3 자리 + F 4 자리
- **구조 시각화** — VESTA 계열로 보임 (`Fig. 1c`, `Fig. 4b,c`, `Fig. S9a`)
- **하지 않은 것**: Bader · COHP/ICOHP · ELF · BVSE · phonon · elastic · EOS · AIMD · MLIP · **grand-potential ESW** — **전부 없음**

---

## 6. Figure set ★ — 그림별 전수 해설

> ⚠ **아래 표는 "우리가 실제로 본 그림"과 "캡션·본문으로만 정리한 그림"이 섞여 있다.**
> **실제 PNG 를 Read 로 본 것 (12 장)**: `Fig. 1` · `Fig. 2` · `Fig. 3` · `Fig. 4` · **`Fig. 5` · `Fig. 6`**(2026-08-06 재투입 때 추가 판독) · `Fig. S4` · `Fig. S8` · `Fig. S9` · `Fig. S11` · `Fig. S22` · `Fig. S24`.
> **안 본 것 (28 장)**: SI 그림 전부(`Fig. S1`–`S3`·`S5`–`S7`·`S10`·`S12`–`S21`·`S23`·`S25`–`S34`).
> ⇒ **본문 그림(`Fig. 1`–`6`)은 이제 전수 판독 완료**, SI 그림은 위 6 장만 봤다.
> 그림에서만 읽은 값은 본문 곳곳에 **[figure-read ≈]** 로 표기했다.

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| **1a,b** | x = 0–0.10 XRD (F-43m, Li₇PS₆ PDF#34-0688) + 29–32.5° 확대(저각 이동 = 팽창) + x=0.06 Rietveld (R_wp 4.61 / R_p 1.18 %) | ✅ **본 그림.** 2차상 표시는 **LiInS₂·LiCl 뿐** — 본문이 말한 Li₈P₂S₉·LiF 는 그림에 없다. 고용한계 x ≈ 0.08 |
| **1c** | 결정구조 도해: Li(48h) · **P/In(4b)** · S(16e) · **S/Cl/F(4a,4d)** | 자리 배정 시각 요약 — **In→4b, F→4a/4d** 라는 이 그룹 표준 그림 |
| **1d,e** | XPS S 2p (PS₄³⁻ + **InS₄⁵⁻** + 미량 metal sulfide) · F 1s (**684.5 eV "F-SEs"**) | ⚠ InS₄ 이중선 분리 2.3 eV = **S 2p 로 물리적으로 불가** → 자리 증거로 약함 (§11-⑨) |
| **1f** | SEM + EDS (P·S·In·F 균일, 입도 3–5 µm) | ⚠ In 0.5 at%·F 1 at% 수준을 EDS 맵으로 "균일"이라 하는 것은 과해석 |
| **2a,b** | Arrhenius(25–80 °C, 6 조성) · σ/Ea vs x (**σ 정점 x=0.02 5.6 · Ea 최저 0.29 eV**) | ✅ **본 그림.** Ea 는 x 와 함께 **단조 증가**([figure-read ≈] 0.303 → 0.337) — F 가 늘수록 나빠진다 |
| **2c** | DC 분극(0.4 V) 6 조성 — x=0.06 전류 최소 | ✅ **본 그림.** σ_e 최소 = x=0.06 확인 |
| **2d** | CV 0.1 mV s⁻¹ Li/SE/SE+C — LPSC 산화 2.6 V·환원 1.2 V, LPSCInF 전류 급감 | ✅ **본 그림.** ⚠ **onset 위치는 두 시료가 같다** — "창이 넓어졌다"는 그림으로 지지되지 않는다(§11-⑤). 우리 grand-potential 창(환원 1.242 / 산화 2.256 V)과 **비교 가능한 유일한 칸** |
| **2e,f** | PDOS: **LPSC 1.78 eV / LPSCInF 2.75 eV** | ✅ **본 그림.** ⚠ **DOS 문턱 판독** — 우리 규율(fixed-occ nscf 고유값) 위반 방식. E_F 가 VBM 에 붙어 있다. 절대 갭 직접 비교 금지(§8b) |
| **3a,b** | CCD 계단 시험 — x=0 **1.0** / x=0.06 **2.5 mA cm⁻²** 에서 단락 | ✅ **본 그림** |
| **3c** | CCD vs "capacity" 문헌 산점도 | ✅ **본 그림.** ⚠ 두 축이 거의 같은 양(capacity = CCD × 스텝시간)이라 **비교 성립 안 함**(§11-⑧). **Li₅.₄PS₄.₄Cl₁.₆ = 우리 modelc 조성이 최하점(CCD ≈0.55)** |
| **3d** | x=0.06 대칭셀 **2000 h @ 0.5 mA cm⁻², η ≈ ±22 mV** | ✅ **본 그림.** 본문·`Table S2` 와 **일치**(이전 "본문 800 h" 지적 철회, §14a) |
| **3e,f** | 순환 50 h 후 XPS: F 1s **LiF 684.8** · In 3d **In⁰ + Li–In alloy** 신규 | ✅ **본 그림.** ⚠ F 1s 이동이 본문상 **0.3 eV** 뿐(전하보정 오차 수준) · In⁰/Li–In 성분은 **In³⁺ 대비 매우 작다** — SEI 서사가 소수성분에 얹혀 있다 |
| **3g,h** | Li(100) **0.38 eV** vs Li–In alloy(110) **0.17 eV** 표면 확산 장벽 | ✅ **본 그림.** 두 프로파일 모두 **대칭·매끄러움**(수렴 양호) — `Fig. S9b` 와 대조된다 |
| **4a** | ★ **용매 침지 전후 σ**: LPSC 4.8→3.0/2.1/1.0 · LPSCInF 4.0→3.65/3.3/2.85 | ✅ **본 그림.** **리뷰 "maintain σ after immersion" 의 근거 데이터.** ⚠ 출발점이 4.8 vs 4.0 — **초기 σ 17 % 를 팔았다** |
| **4b,c** | ★ toluene 흡착 모델: **LPSC E_ad −0.41 / LPSCInF −0.12 eV** | ✅ **본 그림.** **리뷰 Fig 4c 의 원본.** ⚠ **vdW 보정 없는 PBE 로 방향족 흡착** — 절대값 신뢰 불가(§11-①) |
| **4d,e** | toluene 1 h 후 Raman(pristine PS₄ 422.6 급감/이동, co-doped 불변) · XRD(pristine → **Li₄P₂S₆·Li₃P·LiCl**) | ✅ **본 그림.** **구조 분해의 직접 증거 — 이 논문에서 가장 설득력 있는 데이터.** 분해산물이 우리 0 V 분해식(Li₃P + Li₂S + LiCl)과 겹친다 |
| **4f** | ★ 만화: `PS₄ + C₇H₈ → P₂S₆ + Li₃P` vs `InS₄ + C₇H₈ → ✗` | ✅ **본 그림.** **리뷰 Fig 4c 의 나머지 절반.** ⚠ x=0.06 에서 사면체의 **94 % 가 여전히 PS₄** — 만화가 실제 조성을 반영하지 않는다(§11-⑦) |
| **5a–g** | LPSCInF 필름 제조 개요 · LCO/필름/Li 충방전·율속·500 cyc 83.2 %·EIS | ✅ **본 그림(2026-08-06 추가).** 율속·500 cyc·EIS(223.5→330.6 Ω)·80 °C 노출(134.7→127.8) 전부 본문값과 일치. ⚠ **`Fig. 5a` 도식은 "유발 분쇄 → 복합체 → 캘린더 롤"만 그린다** — SI Methods 의 **doctor blade on PET** 단계가 도식에서 빠져 있어, 본문의 *"slurry casting"* 과 그림의 인상이 어긋난다(§14b-신규④는 아님, 서술 수준 지적). 35 µm·2.9 Ω cm² 는 우리 dry-electrode 축 참고 |
| **6a–e** | FeS₂/필름/Li 60 °C: 834.1 mAh g⁻¹·ICE 96.9 %·100 cyc 91.3 %·**410 Wh kg⁻¹** | ✅ **본 그림(2026-08-06 추가).** `6e` 의 "This work" 별점 [figure-read ≈] **4.1 mAh cm⁻² / ≈400 Wh kg⁻¹** = `Table S3` (4.17 / 410) 와 정합 ✓. ⚠ `6a` 2nd 방전의 **상부 평탄부가 [figure-read ≈] 2.0 V** 로 보여 본문 *"2.2 and 1.5 V"* 와 0.1–0.2 V 어긋난다(판독 불확실 ±0.1 — **저확신 관찰**, 본문 인쇄값을 우선) |
| **S1** | 격자상수 vs x (9.825 → 9.856 Å) | 안 봄 — 본문 인쇄값 사용 |
| **S2** | x = 0.15 XRD (2차상 다수) | 안 봄 |
| **S3** | DFT 도핑 자리 모델 (In: P-4b/Li-24g/Li-48h · F: Cl-4a/Cl-4d/PS₄-S/InS₄-S) | 안 봄 — 캡션이 자리 목록을 다 준다 |
| **S4a,b** | ★ **자리 형성에너지**: In **P4b +0.32** / Li48h −0.49 / Li24g −0.79 · F **Cl4a +0.81** / Cl4d +0.64 / PS₄-S −1.56 / InS₄-S −1.24 eV | ✅ **본 그림.** 본문 인쇄값과 완전 일치. **우리 cascade 의 M³⁺@Li_24g 규칙과 정면 충돌**(§8a) |
| **S5** | Raman x 시리즈 + **In–S 310 cm⁻¹** 밴드 | 안 봄 ⚠ [GaF₃] 편에서 유사 밴드가 "불순물상 신호"로 정정된 전례 있음 — 이 논문의 310 cm⁻¹ 도 같은 검증 필요 |
| **S6** | XPS Li 1s / In 3d / P 2p / Cl 2p | 안 봄 — 본문 인쇄값 사용 |
| **S7** | Nyquist x = 0.02–0.15 | 안 봄 |
| **S8a,b** | ★★ **F-only Li₅.₇PS₄.₇Cl₁.₂₄F₀.₀₆ σ = 4.3** · **In-only Li₅.₇₄P₀.₉₈In₀.₀₂S₄.₇Cl₁.₃ σ = 7.0 mS cm⁻¹** | ✅ **본 그림 — A13 의 핵심 증거.** 두 대조군이 **dose-matched**. 둘 다 반원 없이 차단 꼬리만(R = x-절편 ≈42 / 26 Ω) |
| **S9a,b** | ★ SE 슬랩 48h→48h CI-NEB: **pristine 0.662 → In-doped 0.236 eV** | ✅ **본 그림.** ⚠⚠ 프로파일이 **비대칭·톱니** — 한 이미지에서 0.195 → 0.662 → 0.39 로 튄다(**미수렴 saddle 징후**). 게다가 캡션은 "(010) 표면"인데 **그림에는 진공층이 보이지 않는다**(§11-②). **0.662 eV 는 [GaF₃] 논문이 재사용한 값과 동일** |
| **S10** | x = 0.02/0.04/0.08/0.1/0.15 CCD 시험 (0.1 mA cm⁻², 2 h 스텝) | 안 봄 — `Fig. S11` 요약으로 대체 |
| **S11** | ★ **σ_e ↔ CCD 역상관** (둘 다 x = 0.06 이 극값) | ✅ **본 그림.** **litdb 역상관 진영의 4번째 표**(§8f) |
| **S12–S14** | 대칭셀: x=0 75 h 단락 / x=0.02 750 h / x=0.06 1000 h @1 mA cm⁻² | 안 봄 — 본문 인쇄값 사용 |
| **S15** | Li/SE/Li 휴지 EIS 시간전개 (LPSC 163→312 Ω / LPSCInF →175 Ω 안정) | 안 봄 |
| **S16** | 순환 후 Li 표면 SEM (co-doped 평탄 / pristine mossy) | 안 봄 |
| **S17** | 순환 후 XPS Li 1s / P 2p / S 2p / Cl 2p | 안 봄 |
| **S18** | 이성분 PDOS: Li₂S · Li₃P · LiCl · **LiF (7.4 eV)** | 안 봄 ⚠ **우리 `sei_products.json` 과 대조 가능한 칸** — [GaF₃] 편이 같은 4종을 7.4/6.2/4.2/1.1 eV 로 인쇄했으므로 **먼저 [GaF₃] 값을 쓰고, 필요하면 이 그림을 다시 볼 것** |
| **S19** | Li–In 합금 표면에너지 (100) 0.50 / (110) 0.40 / (111) 0.51 eV Å⁻² + (100) 확산 0.23 eV | 안 봄 — 본문 인쇄값 사용 |
| **S20** | H₂S 발생량 vs 시간 (x = 0/0.02/0.06/0.10/0.15) | 안 봄 — 60 min 값이 본문에 인쇄 |
| **S21** | 대기 10 min 노출 전후 Arrhenius | 안 봄 |
| **S22** | ★★ **H₂O 흡착에너지 4 표면 × 2 자리** (pristine / In-only / F-only / co-doped) | ✅ **본 그림 — A13 의 두 번째 핵심 증거.** 판독값이 본문 감소량(0.12/0.15/0.32)과 **정확히 정합** |
| **S23** | 용매 침지 전후 Nyquist (25 °C 명시) | 안 봄 — 온도 조건만 캡션에서 회수 |
| **S24a,b** | ★ 자리별 E_ad (**P −1.85 ≪ S −1.31 < Li −1.04 < Cl −0.66**) · P-site DCM/EtOAc **LPSC vs LPSCInF** | ✅ **본 그림.** **"P 가 표적"의 정량 근거.** ⚠ co-doped 계에서도 **"P-site"** 를 계산했다 = 개선의 실체는 2차 근접 전자효과(§4c 각주) |
| **S25–S27** | 필름 XRD/FTIR · 광학사진 · 단면 SEM(35 µm) + In·F EDS | 안 봄 |
| **S28** | 필름 Nyquist + Arrhenius (σ 1.4 mS cm⁻¹, Ea 0.33 eV) | 안 봄 — 본문 인쇄값 사용 |
| **S29** | 필름 대칭셀 >400 h | 안 봄 |
| **S30** | 필름 DC 분극 (σ_e 8.31×10⁻¹⁰ S cm⁻¹) | 안 봄 |
| **S31–S34** | LCO 입자 SEM/EDS · Si 음극 셀 · FeS₂ 입자 · FeS₂ 셀 EIS | 안 봄 |
| **Table S1** | x=0.06 Rietveld 좌표·점유 | ⚠ **우리 검산 결과 4a 합 1.078 · 4d 합 1.161 로 1 을 초과** — 인용 금지(§3a) |
| **Table S2** | 문헌 σ/CCD 벤치마크 15 행 | ⭐ **Li₆PS₅Cl₀.₃F₀.₇ σ 0.71** = F-only 가 σ 를 무너뜨린다는 외부 증거. [Li25]·[Liu23] 도 이 표 안에 있다 |
| **Table S3** | FeS₂ 셀 에너지밀도 계산 (410 Wh kg⁻¹ / 526.7 Wh L⁻¹) | 셀 수준 목표치 참고 |
| **Table S4** | SE 막 두께별 파우치셀 에너지밀도 비교 9 행 | 35 µm·410 Wh kg⁻¹ 가 최상단 |

---

## 7. 기법 미니 용어집 (이 논문을 읽는 데 필요한 것만)

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **HSAB** (hard/soft acid–base) | Pearson 1963. **hard acid ↔ hard base**, **soft acid ↔ soft base** 가 안정한 짝. 전하밀도가 크고 분극 안 되는 쪽이 hard | P⁵⁺ = hard acid(표적), In³⁺ = soft acid, S²⁻ = soft base ⇒ In–S 가 P–S 보다 튼튼하다는 논증. ⚠ [Fan26] 리뷰는 §3.2 에서 P⁵⁺ 를 **soft** 라고 써서 이 논문과 어긋난다(리뷰어 노트 **A7**) |
| **polar index (극성지수)** | Snyder 극성 척도. toluene 2.4 < DCM 3.4 < ethyl acetate 4.3 | 침지 시험의 x 축. ⚠ 리뷰 §3.2 는 **donor number** 를 쓴다 — **다른 척도**다 |
| **CCD (critical current density)** | 대칭셀 전류를 계단으로 올려 단락되는 지점. 덴드라이트 내성 지표 | 1.0 → 2.5 mA cm⁻². ⚠ 스텝 크기·시간에 강하게 의존해 **논문 간 비교 위험** |
| **CI-NEB** | climbing-image NEB. 이미지 사슬 중 최고점을 saddle 로 끌어올려 장벽을 정확히 잡는 법 | SE 슬랩·Li 금속 슬랩 4 경로 |
| **ΔE_ads vs E_ad** | 이 논문은 **부호 규약이 반대인 두 양**을 쓴다: H₂O 는 `E_surf+E_H₂O−E_복합체`(**양수=강함**), 유기용매는 `E_복합체−E_SE−E_용매`(**음수=강함**) | 혼동 주의 — 두 값을 같은 표에 넣지 말 것 |
| **DOS-threshold 갭** | PDOS 곡선이 0 을 벗어나는 지점으로 갭을 읽는 방식 | `Fig. 2e,f` (1.78 / 2.75 eV). **우리 규율은 이것을 금지**하고 fixed-occ nscf VBM/CBM 고유값만 인정 |
| **PIB (polyisobutylene)** | 포화 탄화수소 사슬 바인더. 극성기가 없어 황화물과 반응 안 함 | toluene 용해 → 슬러리 캐스팅. **toluene 내성이 있어야 이 공정이 성립** = 논문의 실용 논리 |

---

## 8. 우리 DFT / db 대비 ★ (`our_dft_baseline.md`)

> ⚠ **문헌 수치는 소환값**이다. 아래 표는 **축 정렬**용이고, 절대값을 우리 db 로 이식하지 않는다.

### 8a. 🔑 **자리(site) 충돌 — [Yang25]·[GaF₃] 에 이어 세 번째**

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| M³⁺ 선호 자리 | **In → P(4b)**, E_f +0.32 vs Li24g −0.79 eV (**Δ 1.11 eV 로 4b 압승**) | `doping_cascade_trivalent_M3.json` — **3가 champion 26 종 전원 Li_24g, P_4b 0 건** | **정면 충돌.** 단 (i) 우리 cascade 는 **산화물 전구체(M₂O₃)** 를 넣고 이들은 **불화물(InF₃)**, (ii) 우리 판정 기준은 **총에너지 최저 배열**, 이들은 **Eq S1 형성에너지**(기준상태가 원소 In·P 금속/원소상)로 **비교 기준이 다르다**, (iii) 이들은 In 25 % 과도핑 셀에서 1 자리만 비교 |
| F 선호 자리 | **Cl 4a (+0.81)** > Cl 4d (+0.64) ≫ PS₄-S (−1.56) | 우리 F 도핑 데이터 없음 | **우리에게 없는 칸** — F 를 넣는다면 4a 부터 시험 |

**⇒ 후속 계산 필요 (§8e-①).** 같은 host·같은 코드 계열에서 **In@P_4b vs In@Li_24g 총에너지**를 우리 규율로 직접 재는 것이 세 번째 요청이다.

### 8b. 전자구조 — **비교하되 절대값은 금지**

| 항목 | 이 논문 | 우리 (canonical) | 판정 |
|---|---|---|---|
| 밴드갭 (pristine) | **1.78 eV** (PBE, **DOS 문턱**) | comp1 **2.066** / modelc **2.099** eV (PBE, **fixed-occ nscf 고유값**) | **방법 인공물이 지배.** 판독법(DOS 문턱은 통상 ~0.3 eV 과소) + k-mesh 미기재 + 무질서 단일 배열 + 조성 차이(Li₅.₇PS₄.₇Cl₁.₃ vs Li₆PS₅Cl) — **실질 차이라 부를 수 없다** |
| 밴드갭 (doped) | **2.75 eV** | +B₂O₃ **1.9671** / LPSOCl(+O) **2.2309** eV | ⚠ **PBE argyrodite 에서 2.75 eV 는 이례적으로 크다.** In³⁺→P⁵⁺ 는 Li 를 2 개 더 넣어 **부분 점유/E_F 배치 문제**를 낳는데 그림에서 E_F 가 VBM 에 붙어 있다. **"넓은 갭 절연체"라는 정성 진술까지만** 공유 |
| VBM character | 논문이 안 밝힘 | comp1/modelc **둘 다 S 3p** (89.5 %) | 이 논문에는 **원소분해 PDOS 가 없다** — 우리 site-PDOS 가 갖는 정보 우위 |
| σ_e (실측) | pristine ≈1.77×10⁻⁸ → **2.94×10⁻⁹ S cm⁻¹** | 우리는 N(E_F)=0 (완전 절연체) | 실험 σ_e 는 입계·불순물 지배 — **DFT 값과 같은 축이 아니다**. 다만 **"도핑이 σ_e 를 낮춘다"는 방향은 우리 gap 결과와 모순 없음** |

### 8c. ✅ **In 선택의 근거가 우리 [Zhu20] db 로 직접 검산된다** (가장 값어치 있는 칸)

논문 본문 ref [20] = **P. Zhu, Y. Mo, *Angew* 2020, 59, 17472 = 우리 [Zhu20] digest** 이고, 우리는 그 **SI 엑셀을 전수 전사**해 두었다(`db/properties/zhu2020_si_hydrolysis_energies.csv`, 이성분 황화물 **46 종**, ΔE_hyd per H₂O, **양수 = 흡열 = 가수분해 불리 = 공기 안정**):

| 화합물 | ΔE_hyd (eV) | 46 종 중 순위 | 뜻 |
|---|---|---|---|
| **In₂S₃** | **+0.599** | **9 위** | In–S 가 물에 잘 안 뜯긴다 |
| Sb₂S₃ | +0.535 | 12 위 | (이 그룹의 다른 도펀트 계열) |
| SnS₂ | +0.441 | 13 위 | |
| **Ga₂S₃** | **+0.362** | 18 위 | **In > Ga** — 그룹이 InF₃(2024) 를 먼저 하고 GaF₃(2026) 로 간 순서와 정합 |
| **Li₂S** (host 기준선) | **+0.225** | 22 위 | |
| **P₂S₅** (치환 대상) | **−0.156** | 25 위 | **P 가 취약점** |
| **B₂S₃** (우리 +B₂O₃) | **−0.901** | **44 위** | ⚠ §8d |

**⇒ `P₂S₅ (−0.156) → In₂S₃ (+0.599)` = 이성분 프록시에서 +0.755 eV 개선.** 논문의 HSAB 서사("soft In³⁺–soft S²⁻ tight binding")와 **방향 완전 일치**하고, 그 근거가 **우리가 이미 갖고 있는 표**다.
⚠ **단 이것은 이성분 프록시이지 도핑된 SE 값이 아니다** (`kb/open_items.md` #11). 그리고 논문이 쓴 *"In³⁺ is the most promising … **highest** stability against moisture"* 는 **[Zhu20] 표에서 In₂S₃ 가 1 위가 아니라 9 위**라는 점에서 부정확하다 — 상위 8 개(Au₂S·Cu₂S·ZnS 등)는 **환원 안정성이 나빠 탈락**하는 것이므로 "**습기·환원 두 축을 동시에 만족하는 것 중** 최선"이라 썼어야 한다.

### 8d. ⚠ **우리 +B₂O₃ 와 "동형 기전"인가 — 절반만 맞다 (판정)**

리뷰 digest 는 이 계열을 우리 B–S 안정화와 **"✓ 동형 기전"** 으로 적어 두었다. 실물 대조 결과:

| | 이 논문 (InF₃) | 우리 (+B₂O₃) | 판정 |
|---|---|---|---|
| **논리 형태** | "취약 단위(PS₄)를 강결합 단위(InS₄)로 바꾸면 공격에 면역" | "free-S 를 B–S 결합으로 묶으면 산화 취약성 완화" | **✓ 논리는 동형** |
| **취약점의 정체** | **P⁵⁺ (친핵 공격 표적)** — 흡착 스캔에서 P 자리 −1.85 eV 최강 | **free-S²⁻ (산화 취약)** — site mean-3p **−1.14 eV 로 가장 얕음** | **✗ 다른 원자, 다른 축** |
| **관측량** | **분자–표면 흡착에너지** (화학적 공격) | **자리분해 PDOS ⟨3p⟩ + 산화 onset** (전자적 산화) | **✗ 다른 물리량** |
| **안정화 폭** | E_ad −0.41 → −0.12 eV (toluene) | free-S −1.14 → **B–S −2.15 eV** (mean-3p 기준) | **부호는 같으나 단위·정의가 달라 직접 비교 불가** |
| **[Zhu20] 대기 축** | **In₂S₃ +0.599 (9/46위)** — 우수 | **B₂S₃ −0.901 (44/46위)** — 최하위군 | **✗✗ 정반대** |

> **판정: "동형 기전"이라 부를 수 있는 것은 *논리 형태*(취약 단위를 강결합으로 묶는다)까지다.**
> **B 와 In 은 축이 다르다** — B 는 **산화(전자구조) 축**을 고치고 **대기 축은 오히려 최하위군**이며, In 은 **대기·용매(화학적 공격) 축**을 고친다. 우리 원고에서 이 둘을 나란히 놓을 때 **반드시 축을 명시**해야 한다. (리뷰 digest 의 "✓ 동형 기전" 항목에 이 단서를 달아 두었다 → `comparison_vs_ours.md`)

### 8e. ★ **우리가 이 계열보다 잘할 수 있는 것 — In/F 기여 분리 (구체 계산 3개)**

우리 cascade 는 **양이온 도펀트를 단독으로** 넣으므로 **In-only 계산이 자연히 존재**한다. 필요한 것을 명세로 적는다:

| # | 계산 | 목적 | 규율 |
|---|---|---|---|
| **①** | **In@P_4b vs In@Li_24g 총에너지** (comp1/modelc host, 우리 표준 relax) | §8a 의 자리 충돌 판정. **[Yang25](La)·[GaF₃](Ga) 에 이어 세 번째 요청 — 한 번에 처리** | 우리 k-mesh·ecut 규율, 같은 셀에서 배열만 바꿔 비교 |
| **②** | **자리분해 PDOS/ICOHP 로 In–S vs P–S 비교** (In-doped modelc 단독) | 논문이 정성적으로만 말한 *"tight binding In³⁺–S²⁻"* 를 **ICOHP 로 정량화** — 우리가 이미 Li–Cl(−1.86/−2.10)에서 쓰는 관측량. **리뷰어 A12("어느 정의로 쟀나")에 우리 답을 붙이는 자리** | mean-3p 는 **−8..0 eV 창** 고정 |
| **③** | **F-only modelc** (Cl 4a 하나를 F 로) 의 (a) gap (b) Li–F ICOHP (c) MLIP-MD Ea | **F 단독이 σ 를 깎는 기전**을 우리 축에서 재현. 실험(4.8→4.3, Li₆PS₅Cl₀.₃F₀.₇ 0.71)과 **방향 일치 여부**만 판정 | **σ 절대값 인용 금지**, Ea 는 **멀티시드**로만, MSD 창 2–50 ps |

**①+②+③ 이 다 나오면 우리는 "In 기여 / F 기여 / 상호작용"을 계산 축에서 분해한 첫 사례가 된다** — 이 문헌 계열(InF₃·GaF₃·MgF₂·CuBr₂·CuCl·La₂O₃) 전체가 못 한 것이다.

### 8f. ✓ σ_e ↔ CCD 역상관 — 진영 판정 4번째 표

| 논문 | σ_e 변화 | CCD 변화 | 역상관? |
|---|---|---|---|
| [Taklu] CuCl | ↓ | ↑ | ✓ |
| [Liu23] MgF₂ | ↓ | ↑ | ✓ |
| **본편 InF₃** | **1.77×10⁻⁸ → 2.94×10⁻⁹ (6×↓)** | **1.0 → 2.5 (2.5×↑)** | **✓ (전 구간 단조 거울상, `Fig. S11`)** |
| [Li25] CuBr₂ | ↓ | ↑ | ✓ |
| [GaF₃] | 1.68×10⁻⁸ → 5.0×10⁻⁹ | 0.4 → 1.8 | ✓ |
| [Yang25] La₂O₃ | — | — | ✗ (유일 반례) |

**5:1 로 역상관 진영이 압도적.** 그리고 **[GaF₃] 의 DC 분극 대조(F-only·co-doped 만 전류 0, Ga-only 는 pristine 과 동일)로부터, 이 계열에서 σ_e 를 낮추는 것은 F 라는 강한 추론이 가능**하다 — 본편은 그 대조를 안 했지만 같은 그룹·같은 설계이므로 이식 가능한 가설이다(**추론임을 명시할 것**).

### 8g. ✗ 우리에게 없는 것 / 그들에게 없는 것

| 그들이 한 것 (우리에게 없음) | 우리가 한 것 (그들에게 없음) |
|---|---|
| 유기용매 흡착에너지 (자리별 스캔) | **grand-potential ESW** (환원 1.242 / 산화 2.256 V, 반응식까지) |
| H₂O 흡착에너지 (4 표면 × 2 자리) | **ICOHP** (LOBSTER), **Bader**, **ELF** |
| Li–In 합금 표면에너지·표면 확산 NEB | **BVSE 채널 정량**, **탄성 C_ij / EOS B₀** |
| PIB 필름·풀셀 실증 (35 µm, 410 Wh kg⁻¹) | **MLIP-MD 아레니우스(멀티시드)**, **자리분해 PDOS ⟨3p⟩** |
| 실험 Ea (EIS Arrhenius, **0.29–0.34 eV**) | — |

⭐ **실험 Ea 0.29 eV (x=0.02) / ≈0.303 eV (pristine Li₅.₇PS₄.₇Cl₁.₃)** 는 우리 MLIP-MD Ea(comp1 0.253 / modelc 0.224, 3-seed 0.197±0.032)의 **외부 실험 앵커**다. 우리 값이 더 낮은 것은 **입계 없는 벌크량**이기 때문이라 방향 정합 — [GaF₃] 편의 0.28 eV 와 같은 자리에 놓인다.

---

## 9. 메커니즘 흐름 (논문이 주장하는 대로 + 우리 주석)

```
 InF₃ 한 염 투입
        │
        ├── In³⁺ → P⁵⁺ (4b)        [E_f +0.32 eV, XPS InS₄⁵⁻, Raman 310 cm⁻¹]
        │     ├── +2 Li/In → 캐리어·공공 ↑ ────────────► σ ↑ (4.8 → 7.0 In-only)
        │     ├── HSAB soft-soft (In³⁺–S²⁻) ──────────► H₂O 흡착E −0.12 eV
        │     ├── hard acid P⁵⁺ 표적 제거/희석 ───────► 용매 E_ad −0.41 → −0.12 eV
        │     │        ⚠ 우리 주석: x=0.06 에서 PS₄ 가 94 % — 실체는 2차 근접 전자효과
        │     └── 순환 중 Li–In 합금 ─────────────────► Li 표면 확산 0.38 → 0.17 eV
        │              ⚠ 우리 주석: XPS 에서 In⁰/Li–In 성분은 In³⁺ 대비 소수
        │
        └── F⁻ → Cl⁻ (4a)          [E_f +0.81 eV, XPS F 1s 684.5 eV]
              ├── Li–F 정전인력 강 → Li⁺ 국소 왜곡 ────► σ ↓ (4.8 → 4.3 F-only) ★부작용
              ├── Li–F 가 전자를 덜 내줌 ──────────────► H₂O 흡착E −0.15 eV (In 보다 큼!)
              └── 순환 중 LiF SEI (gap 7.4 eV) ────────► 전자 절연 → σ_e ↓ → CCD ↑
                       ⚠ 우리 주석: F 1s 이동이 0.3 eV 뿐 — 전하보정 오차 수준

 순 결과 (x=0.06): σ 4.0 (−17 %) · σ_e 6×↓ · CCD 2.5×↑ · H₂S 70 %↓ · 용매 σ 보존 3.4×↑
        ⇒ "σ 를 조금 팔아 3 개 축(대기·용매·Li 금속)을 산다" — [Yang25]/[GaF₃]와 같은 트레이드
```

---

## 10. 인용 가능 문장 (deck / 원고용 — 사실만)

- "InF₃ 공도핑 argyrodite(Li₅.₈₂P₀.₉₄In₀.₀₆S₄.₇Cl₁.₁₂F₀.₁₈)는 toluene·dichloromethane·ethyl acetate 에 1 h 침지한 뒤에도 이온전도도의 **91 / 83 / 71 %** 를 유지하며, 무치환 Li₅.₇PS₄.₇Cl₁.₃ 의 **63 / 44 / 21 %** 와 대비된다 (Li *et al.*, *Adv. Energy Mater.* **2024**, 14, 2402929)."
- "같은 연구는 toluene 의 argyrodite (001) 표면 흡착에너지가 InF₃ 공도핑으로 **−0.41 → −0.12 eV** 로 약해진다고 보고한다 (PBE, vdW 보정 미기재)."
- "그 논문 자신의 단일 도펀트 대조군에서 **In 단독은 σ 를 4.8 → 7.0 mS cm⁻¹ 로 올리고, F 단독은 4.8 → 4.3 mS cm⁻¹ 로 낮춘다** — 공도핑 시료의 5.6 mS cm⁻¹ 는 두 효과의 절충이다."
- "H₂O 흡착에너지 감소분은 **In 0.12 eV, F 0.15 eV, 공도핑 0.32 eV** 로, **대기 안정성 기여는 F 가 In 보다 크다**."
- "In³⁺ 를 고른 근거는 Zhu & Mo (*Angew* 2020)의 설계지도이며, 그 SI 의 이성분 가수분해 에너지에서 **In₂S₃ +0.599 eV** 는 기준선 **Li₂S +0.225 eV** 와 치환 대상 **P₂S₅ −0.156 eV** 를 모두 웃돈다."
- ⚠ **쓰면 안 되는 문장**: *"InF₃ 가 격자 결합에너지를 높이고 분극률을 낮춘다"* — **원 논문에 그 표현도, 그 물리량도 없다**(§4d).

---

## 11. 비판 (방법 의존성 · 주장 vs 증거)

**① ⚠⚠ vdW 보정 없는 PBE 로 방향족 분자 흡착을 계산했다 — 이 논문 최대 약점**
`Fig. 4b,c` 의 **toluene** 은 비극성 방향족이라 표면 결합이 **분산력 지배**다. 순수 PBE 는 분산을 거의 못 잡아 흡착에너지를 크게 과소평가한다. SI Computational Section 어디에도 **D2/D3/TS/vdW-DF 언급이 없다**. ⇒ **−0.41 / −0.12 eV 라는 절대값은 물론, 두 값의 차(0.29 eV)조차 함수형 인공물일 수 있다.** 이 값이 [Fan26] 리뷰의 핵심 인용값이라는 점에서 특히 문제다.

**② ⚠⚠ SE 의 NEB 가 미수렴으로 보이고, 벌크인지 표면인지도 불명확하다**
`Fig. S9b` 의 pristine 프로파일은 한 이미지에서 **0.195 → 0.662 → 0.39 eV** 로 튄다 — 대칭 hop 인데 프로파일이 **비대칭·톱니**다. 이미지 수 부족·saddle 미해상의 전형적 징후다(같은 논문의 `Fig. 3g,h` Li 금속 프로파일은 매끄럽고 대칭이라 대조가 뚜렷하다). 게다가 **캡션은 "(010) 표면"인데 `Fig. S9a` 에 진공층이 보이지 않는다**. **그리고 0.662 eV 는 실험 Ea(0.29–0.30 eV)의 2.2 배**인데 논문이 이 격차를 전혀 언급하지 않는다. ⇒ **이 NEB 값을 우리 벌크 Ea 와 같은 표에 넣지 말 것.**

**③ ⚠ 헤드라인 σ 와 헤드라인 안정성이 다른 시료다**
σ 챔피언은 **x = 0.02 (5.6 mS cm⁻¹)** 인데, 모든 안정성·CCD·필름·풀셀은 **x = 0.06 (σ 4.0)** 로 한다. 초록은 두 값을 나란히 제시해 **한 시료가 둘 다 갖는 것처럼 읽힌다**. `Table S2` 벤치마크 행도 σ 를 **4.0** 으로 정직하게 적었으나 초록·결론은 5.6 을 앞세운다.

**④ ⚠ DFT 도핑 농도가 실험의 4–12 배다**
1×1×1 셀에 P 는 **4 개**뿐 → In 1 개 = **In 25 %**. 실험 x = 0.02–0.06 (**2–6 %**). 자리 선호(E_f)와 PDOS 갭 2.75 eV 는 **이 과도핑 셀의 값**이다. [GaF₃] 편과 완전히 같은 결함.

**⑤ ⚠ CV 로 "창이 넓어졌다"를 주장하지만 그림은 진폭만 보여준다**
`Fig. 2d` 에서 두 시료의 산화/환원 **밴드 위치는 같다**. 달라지는 것은 전류 크기다. *"suggesting a wide-voltage window stability"* 는 **onset 이동이 아니라 반응량 감소**로 다시 써야 한다. (그림 라벨 *"Reduce/Oxidize **to** PS₄³⁻"* 도 오기.)

**⑥ ~~본문과 그림이 어긋난다 — 대칭셀 수명~~ → ❌ 철회 (2026-08-06 재검증)**
~~본문이 "800 h"라 쓰는데 `Fig. 3d` 는 2000 h 다~~ — **오지적이었다.** 재투입 PDF 본문 전문에서 해당 문장은 *"the Li/LPSCInF (x = 0.06)/Li symmetric cell can be operated stably over **2000 h** at a flat overpotential of 22 mV"* (p.5) 이고, 논문 전체에서 `800` 이 나오는 곳은 **PIB 분자량 "Mw ≈800000" 단 한 군데**다. **본문·`Fig. 3d`·`Table S2` 가 모두 2000 h 로 일치**한다 → §14a.

**⑦ ⚠ `Fig. 4f` 만화가 실제 조성을 반영하지 않는다**
x = 0.06 에서 사면체의 **94 % 가 여전히 PS₄** 인데, 만화는 "PS₄ 는 분해, InS₄ 는 무분해"로 그려 **6 % 의 InS₄ 가 전체를 지키는 것처럼** 읽힌다. 정작 `Fig. S24b` 는 co-doped 계에서도 **"P-site"** 흡착을 계산했다 — 즉 논문 자신의 계산이 말하는 것은 **"In 이 이웃 P 의 전자환경을 바꿨다"**(2차 근접 효과)인데, 만화·본문 서사는 **"In 이 P 를 대체했다"** 로 읽히게 만든다. 이 구분이 없으면 **필요한 In 량의 스케일링(왜 6 %면 되는가)** 을 설명할 수 없다.

**⑧ ⚠ `Fig. 3c` 벤치마크 산점도의 두 축이 사실상 같은 양이다**
CCD 시험에서 capacity = CCD × (스텝 시간)이므로 두 축은 종속이다. 스텝 시간이 논문마다 달라(본편은 `Fig. S10` 기준 2 h 스텝) **점들 사이의 상대 위치가 프로토콜 차이를 반영한다**. "우리가 오른쪽 위"라는 주장의 근거로 약하다.

**⑨ ⚠ XPS 귀속 두 건이 물리적으로 성립하지 않거나 분해능 이하다**
- S 2p 의 **InS₄⁵⁻ 이중선을 2p₁/₂ 163.9 / 2p₃/₂ 161.6 eV** 로 잡았는데 **분리 2.3 eV** 다. S 2p 스핀궤도 분리는 **1.18 eV** 로 고정이므로 이 조합은 하나의 화학종일 수 없다(같은 문단의 PS₄³⁻ 는 1.3 eV 로 정상). ⇒ **XPS 를 In 자리 증거로 쓰기 어렵다.**
- F 1s: pristine **684.5** → cycled **684.8 eV** 를 "F-SEs → LiF" 로 읽는데 **Δ 0.3 eV** 는 전하 보정·시료 대전 드리프트와 구분되지 않는다. (우리가 `Fig. 3e` 를 직접 보면 이동폭은 그보다 커 보이나, 본문 인쇄값이 0.3 eV 다 — **본문과 그림이 또 어긋난다**.)

**⑩ ⚠ `Table S1` 은 결정학적으로 성립하지 않는다**
4a 점유 합 **1.078**, 4d 점유 합 **1.161**, Li 총량 **6.06 vs 명목 5.82**. 조성(F 0.180 / Cl 1.119 / S 4.700)이 명목과 **소수 셋째 자리까지 일치**하는 것으로 보아 **점유를 정련한 것이 아니라 명목값으로 고정**한 결과다. 근본 원인은 lab XRD 가 S(Z=16)/Cl(Z=17)을 구분 못 하고 F·Li 는 거의 안 보인다는 것. **4a/4d 분할 수치 인용 금지.**

**⑪ ⚠ "In³⁺ is the most promising … highest stability" 는 근거 논문의 표와 정확히 맞지 않는다**
인용한 [Zhu20] 표에서 **In₂S₃ 는 46 종 중 9 위**다(1–8 위는 Au₂S·Cu₂S·ZnS 등). 상위 화합물들이 **환원 안정성에서 탈락**하는 것이 맥락이므로 *"습기·환원 두 축을 동시에 만족하는 것 중 최선"* 이라 썼어야 한다.

**⑫ ⚠ F⁻ 이온반경이 같은 논문 안에서 두 값이다**: 구조 절 **136 pm**, 수송 절 **119 pm**. 격자 팽창/수축 논증과 σ 저하 논증이 **서로 다른 반경**에 기대고 있다. ([GaF₃] 편도 133/119 로 같은 실수를 한다 — 그룹 차원의 복붙.)

**⑬ ⚠ (001)/(010)/(100) 표기가 절마다 다르다** (`Fig. S3` 캡션 (100) / 흡착 (001) / NEB (010)). F-43m 에서는 대칭 동등이지만 **논문 내부 일관성 문제**이고, 슬랩 종단이 미기재라 독자가 확인할 수 없다.

**⑭ ⚠ 극성 척도가 리뷰와 다르다**: 이 논문은 **polar index**(2.4/3.4/4.3), [Fan26] 리뷰 §3.2 는 **donor number**. **NMP·THF 같은 고-DN 용매는 이 논문에서 시험되지 않았다** — 리뷰가 이 논문을 §3.2 의 DN 논증 옆에 놓을 때 **척도가 바뀐다**는 점을 밝혀야 한다.

**⑯ ⚠⚠ [신규 2026-08-06] "양이온의 *환원*이 *산화* 한계를 정한다" — 두 문장 안에서 산화/환원이 뒤집힌다**
p.5 원문: *"Based on previous reports, **the reduction of cations largely determines the oxidative limit** of sulfide SEs.[20] Compared with high valence ions such as Ge⁴⁺, P⁵⁺, and Sb⁵⁺, In³⁺ has relatively good **reduction stability** and can be electrochemically stabilized **under reducing conditions**."* — 앞 문장은 "산화 한계", 바로 뒤 문장은 전부 **환원** 이야기다. 물리적으로도 **양이온 환원은 환원(음극쪽) 한계**를 정하지 산화 한계를 정하지 않는다(**황화물의 산화 한계는 S²⁻ 가 잡는다** = 우리 ESW 축 ①, `our_dft_baseline.md` onset 2.256 V S-limited). 게다가 인용한 **[20] = [Zhu20] 은 가수분해·환원 안정성 논문**이라 "oxidative limit" 의 근거가 될 수 없다. ⇒ **이 논문이 CV `Fig. 2d` 의 산화쪽 개선을 In³⁺ 로 설명하는 사슬 전체가 이 오기 위에 얹혀 있다.** 우리 축으로 옮길 때 **"In 은 환원(음극) 축, 산화 축은 여전히 S²⁻"** 로 바로잡아 인용할 것.

**⑰ ⚠ [신규 2026-08-06] Li–In 합금 표면에너지 단위가 물리적으로 성립하지 않는다**
p.5: *"the surface energies of Li–In alloy (100), (110), and (111) are **0.50, 0.40, and 0.51 eV Å⁻²**"*. **1 eV Å⁻² = 16.02 J m⁻²** 이므로 이 값들은 **6.4–8.2 J m⁻²** 다 — **Li 금속 실측 표면에너지 ≈0.5 J m⁻²(≈0.03 eV Å⁻²)의 10–20 배**이고 텅스텐(~3 J m⁻²)보다도 크다. **단위 오기**(eV/표면원자 또는 J m⁻² 를 eV Å⁻² 로 잘못 적었을 가능성)로 보인다. 순위((110) 최저)는 살릴 수 있어도 **절대값은 인용 금지**. ⇒ `Fig. S19a` 를 우리 슬랩 표면에너지와 같은 표에 넣지 말 것.

**⑱ ⚠ [신규 2026-08-06] "Li 캐리어 농도↑" 와 "vacancy 더 생성" 을 한 문장에서 동시에 주장한다**
p.4: *"doping In³⁺ with the lower valence in place of P⁵⁺ … **increases the Li⁺ carrier concentration** and **generates more vacancies** to transport ions"*. In³⁺→P⁵⁺ 는 전하보상으로 **Li 를 +2/In 넣는다**(5.7 → 5.82). argyrodite 의 Li 자리(48h)는 부분점유이므로 **Li 가 늘면 vacancy 는 줄어든다** — 두 주장은 같은 방향일 수 없다. (Cl-rich 계열의 표준 서사는 그 반대다: **Cl↑ → Li↓ → vacancy↑**. 우리 comp1→modelc 가 정확히 그 경로다.) ⇒ **σ 상승의 기전을 "vacancy 증가"로 옮겨 쓰지 말 것.** 이 논문 자신의 NEB(장벽 0.662→0.236)는 **병목 확장(구조)** 서사이지 캐리어/vacancy 서사가 아니다.

**⑲ ⚠ [신규 2026-08-06] 본문이 자기 그림을 오지칭한다** — p.5: *"As shown in **Figure 4e**, the presence of LiF is verified by the characteristic peak observed at 684.8 eV in the **F 1s** spectrum"*. `Fig. 4e` 는 **toluene 침지 전후 XRD** 이고, 순환 후 F 1s 는 **`Fig. 3e`** 다(바로 두 문장 앞에서 "depicted in Figure 3e,f" 라고 옳게 쓴다). 단순 오식이지만 **LiF-SEI 서사의 유일한 직접 증거를 가리키는 문장**이라 인용 시 `Fig. 3e` 로 고쳐 적을 것.

**⑮ ⚠ 데이터 공개 문구가 [GaF₃] 편과 글자 그대로 같다** (*"privacy or ethical restrictions"*). 재료 논문에 부적절한 상투구가 그룹 템플릿으로 재사용되고 있다.

---

## 12. 우리 원고에 바로 쓸 수 있는 것

1. **[Zhu20] 표를 우리 도펀트 선택의 정량 근거로 승격.** 이 논문이 In 을 고른 이유가 **우리가 이미 전수 전사한 표**라는 것은 곧 **우리 cascade 의 3가 도펀트 선정에도 같은 표를 쓸 수 있다**는 뜻이다. In₂S₃ +0.599 / Ga₂S₃ +0.362 / B₂S₃ −0.901 의 순위는 그대로 **"대기 축 사전 스크리닝"** 이 된다.
2. **"σ 를 팔아 안정성을 산다" 트레이드의 세 번째 정량 사례.** [Yang25] · [GaF₃] · 본편이 모두 같은 구조다(본편: 4.8 → 4.0, −17 %). 우리 `+B₂O₃`(σ 축 1등)가 **반대 방향의 사례**라는 점을 대비 축으로 쓸 수 있다.
3. **σ_e ↔ CCD 역상관 5:1** — 우리 gap/N(E_F) 결과를 "왜 절연이 중요한가"의 계산 근거로 연결하는 문헌 진영이 이제 충분히 두껍다.
4. **A12/A13 리뷰어 코멘트의 실물 근거** — §4d 의 원문 검색 결과(polarizability 0회, bond energy 0회)는 그대로 코멘트에 넣을 수 있다.

---

## 13. ★ 1저자 보고용 — A13 을 어떻게 쓸 것인가

**사실관계 (반박 불가)**
1. 이 논문은 **σ 축에서 In-only(7)·F-only(4.3) dose-matched 실험 대조군**을 갖고 있다 (`Fig. S8`). **★ 두 수치는 SI 가 아니라 본문 p.4 에 인쇄돼 있다**(2026-08-06 확인) — 즉 **리뷰 교신저자가 자기 본문에서 이미 In/F 를 갈라 놨다**. A13 을 "갈라라"가 아니라 **"당신 ref [97] 본문이 이미 갈랐고, 그 결과가 축마다 부호가 반대다"** 로 쓸 근거가 더 단단해진다.
2. 이 논문은 **수분 축에서 pristine/In-only/F-only/co-doped 4 종 계산 대조군**을 갖고 있다 (`Fig. S22`, 감소량 In 0.12 / F 0.15 / co 0.32 eV).
3. **리뷰가 실제로 인용한 축(유기용매 침지 후 σ 유지)에는 단일 도펀트 대조군이 없다** (`Fig. 4a`, `Fig. S24b` 는 pristine vs co-doped 2 점).
4. **두 축에서 In 과 F 의 부호가 반대다**: σ 는 **In↑ / F↓**, 수분은 **F(0.15) > In(0.12)**.
5. 리뷰 문장의 *"lattice bond energy"* · *"polarizability"* 는 **원 논문에 없다**. 원 논문의 "polarization rate" 는 **F 가 σ 를 깎는 이유**로 쓰인다.

**⇒ 권고: A13 을 "기여 분리를 요구"로 쓰지 말고, 아래 형태로 바꿀 것**

> **못 쓸 형태** (저자가 반박 가능): *"InF₃ 의 In/F 기여가 분리되지 않았으니 분리하라."*
> → 저자는 `Fig. S8`·`Fig. S22` 를 들어 "우리는 갈랐다"고 답할 수 있고, **그 논문은 리뷰 교신저자 본인의 것**이다.
>
> **쓸 형태 (권장)**:
> *"§3.2 가 인용한 ref [97] 은 실제로 단일 도펀트 대조군을 갖고 있다 — 이온전도에서는 In 단독(4.8→7.0 mS cm⁻¹)과 F 단독(4.8→4.3 mS cm⁻¹)이, 수분 흡착에서는 In(−0.12 eV)과 F(−0.15 eV)가 각각 보고된다. **그런데 두 축에서 두 원소의 부호가 반대다.** 반면 §3.2 가 인용한 축(유기용매 침지 후 σ 유지)에는 단일 도펀트 대조군이 없다. 통합된 'stabilizing component' 서술은 이 반전과 미분리를 모두 지운다. **어느 축에서 어느 원소가 무엇을 담당하는지**를 한 문장이라도 갈라 주면 §5.2.2 의 in-situ 불화물층 논의와도 정합해진다."*
>
> **동시에 A12 를 확정 지적으로 승급**: *"'enhances lattice bond energy and reduces polarizability' 는 인용 논문에 나오지 않는 표현이다. 그 논문에서 'lower polarization rate' 는 F⁻ 치환이 **이온전도도를 낮추는** 이유로 등장한다 — 즉 인용 문장은 원 논문의 인과를 반대 방향으로 옮겼다. 표현을 원 논문 근거(H₂O·유기용매 흡착에너지 저하, HSAB soft–soft 결합)로 바꾸거나, 어느 계산량으로 'lattice bond energy' 를 정의하는지 밝혀야 한다."*

**한 문단 총평**
공정(35 µm 슬러리 캐스팅 필름 → 410 Wh kg⁻¹ FeS₂ 셀)까지 밀고 간 점에서 이 계열 중 **가장 완성도 높은 실증 논문**이다. 그리고 σ·수분 두 축에서 **단일 도펀트 대조군을 실제로 갖춘 드문 사례**이기도 하다. 그러나 **정작 리뷰가 인용한 용매 축은 pristine vs co-doped 2 점뿐**이고, 그 축의 계산 근거(toluene 흡착 −0.41 → −0.12 eV)는 **vdW 보정 없는 PBE** 로 얻은 값이라 절대값 신뢰도가 낮다. DFT 파트 전반이 **k-mesh·vdW·종단·이미지 수 미기재 + 실험의 4–12 배 과도핑 + 미수렴으로 보이는 NEB + 성립하지 않는 Rietveld 점유** 로 재현 불가에 가깝다. **실험은 강하고 계산은 삽화에 가깝다** — 우리가 In/F 기여를 계산 축에서 제대로 분해하면(§8e) 이 계열 전체가 못 한 자리를 채울 수 있다.

---

## 14. ★ 재투입 실물 재검증 (`2026-08-06`) — inbox #55 본문 PDF

> **왜 다시 봤나**: 같은 논문이 `litdb/inbox/55. A Versatile InF 3 Substituted Argyrodite Sulﬁde
> ElectrolyteToward Ultrathin Films for All-Solid-State Lithium Batteries.pdf` (**사용자 분류 폴더 `DFT`**)
> 로 재투입됐다. 원 digest(2026-08-05)는 **업로드본 본문 + SI docx** 로 썼으므로, 이번엔 **inbox 실물 본문**
> 으로 대조했다.
> **범위**: 본문 12 pp **전문 재추출**(PyMuPDF, 59,789 자 → `litdb/inbox/_55_text.txt`) + **`Fig. 1`–`Fig. 6`
> 전 6 장 이미지 재판독**(그중 `Fig. 5`·`Fig. 6` 은 **이번이 첫 판독**).
> ⚠ **SI 는 이번 재투입에 없다** — inbox #55 에 Sup) 파일이 없고 원 digest 의 SI 는 docx 였다.
> 따라서 **`Fig. S*`·`Table S*` 항목은 이번 검증 대상이 아니다**(원 digest 기록 그대로 유지).
> ⚠ **주의(도구)**: `extract_figures.py --slug … --clean` 을 이 slug 에 돌리면 **SI 크롭 34 장이 지워진다**
> (본문 PDF 만으로는 fig_S* 를 다시 못 만든다). 이번에 실제로 지워졌다가 `git checkout` 으로 복구했다.
> **이 slug 에는 `--clean` 금지** — SI docx 를 다시 넣기 전까지.

### 14a. 교정 1 건 — **§11-⑥ 철회**

| 항목 | 원 digest | 실물 | 판정 |
|---|---|---|---|
| 대칭셀 수명 본문값 | *"본문은 **800 h**, `Fig. 3d` 는 2000 h — 2.5 배 불일치"* | 본문 p.5: *"can be operated stably over **2000 h** at a flat overpotential of 22 mV"*. 논문 전체에서 `800` 은 **PIB "Mw ≈800000"** 한 곳뿐 | ❌ **오지적 — 철회.** 본문·`Fig. 3d`·`Table S2` **3자 일치** |

### 14b. 신규 적발 4 건 (전부 §11 에 ⑯–⑲ 로 편입)

| # | 내용 | 심각도 |
|---|---|---|
| **⑯** | *"the **reduction** of cations largely determines the **oxidative** limit"* (p.5) — 산화/환원 뒤바뀜. 뒤 문장은 전부 환원 이야기이고, 인용한 [Zhu20] 도 가수분해·환원 논문. **황화물 산화 한계는 S²⁻**(우리 ESW 축 ①) | ⚠⚠ **높음** — CV 산화쪽 개선을 In³⁺ 로 설명하는 사슬 전체가 이 위에 얹혀 있다 |
| **⑰** | Li–In 합금 표면에너지 **0.50/0.40/0.51 eV Å⁻² = 6.4–8.2 J m⁻²** → Li 실측(≈0.5 J m⁻²)의 **10–20 배**. 단위 오기 | ⚠ 중간 — 순위만 사용, 절대값 인용 금지 |
| **⑱** | *"increases the Li⁺ carrier concentration **and generates more vacancies**"* (p.4) — In³⁺→P⁵⁺ 는 Li 를 **늘리므로**(5.7→5.82) vacancy 는 **줄어든다**. 두 주장이 동시 성립 불가 | ⚠ 중간 — σ 상승 기전을 "vacancy 증가"로 옮겨 쓰지 말 것 |
| **⑲** | p.5 *"As shown in **Figure 4e** … F 1s"* → 실제로는 **`Fig. 3e`**(`Fig. 4e` 는 XRD). 두 문장 앞에서는 옳게 "Figure 3e,f" 라고 쓴다 | 낮음 — 인용 시 `Fig. 3e` 로 고쳐 적기 |

### 14c. 출처 정밀화 1 건

- **In-only 7 mS cm⁻¹ · F-only 4.3 mS cm⁻¹ 은 `[SI 인쇄]` 가 아니라 `[본문 인쇄]`** 다 (p.4 두 문장에 그대로 있다;
  SI `Fig. S8` 은 Nyquist 그림과 조성식). → **§3b 표 수정 + §13-1 강화**. **A13 논증이 더 세진다** —
  단일도펀트 분리 결과가 **리뷰 교신저자 본인 논문의 본문에** 인쇄돼 있다.

### 14d. 재판독으로 **확인된**(불일치 0) 본문 수치 — 이번에 실물로 다시 맞춘 것

`Fig. 1b` R_wp **4.61 %** / R_p **1.18 %** · a **9.825 → 9.856 Å** · Raman **422.6 → 417.3 cm⁻¹** ·
XPS S 2p **162.5/161.2**(PS₄) **163.9/161.6**(InS₄) · F 1s **684.5**(pristine) **684.8**(cycled) ·
In 3d **444.4/451.9** · σ **4.8(x=0) / 5.6(x=0.02) / 4.0(x=0.06)** · Ea **0.29 eV**(x=0.02) ·
σ_e **2.94×10⁻⁹** · CCD **1.0 → 2.5 mA cm⁻²** · NEB **0.662 → 0.236 eV** ·
Li(100) **0.38** → Li–In(110) **0.17** · Li–In(100) **0.23 eV** · PDOS **1.78 → 2.75 eV** · LiF gap **7.4 eV** ·
H₂S **3.82 / 1.73 / 1.16 / 1.10 cm³ g⁻¹** · 대기 10 min 후 σ **2.5 vs 0.24** ·
ΔE_ads 감소 **In 0.12 / F 0.15 / co 0.32 eV** · toluene E_ad **−0.41 → −0.12 eV** · DCM **−0.30** · EtOAc **−0.69 eV** ·
용매 σ 감소율 **37.5/56.3/79.2 %(pristine) vs 8.75/17.5/28.8 %(co)** — **`Fig. 4a` 인쇄 절대값
(4.8→3.0/2.1/1.0 · 4.0→3.65/3.3/2.85)으로 재검산해 소수점까지 정합** ✓ ·
필름 **35 µm · 1.4 mS cm⁻¹ · Ea 0.33 eV · 274 mS · 2.9 Ω cm² · σ_e 8.31×10⁻¹⁰** ·
LCO **135.7 mAh g⁻¹ · ICE 86.2 % · 500 cyc 83.2 % · EIS 223.5→330.6 Ω · 80 °C 후 134.7→127.8** ·
FeS₂ **834.1 · ICE 96.9 % · 100 cyc 91.3 % · 410 Wh kg⁻¹** · µSi **105.1 · ICE 70.2 % · 95.8 %**.
→ **원 digest 의 본문 수치는 위 전 항목에서 실물과 일치**(교정은 §14a 1 건뿐).

### 14e. 새로 본 그림 2 장에서만 읽은 것 (`figure-read ≈`)

- **`Fig. 5a`**: 도식이 **유발 분쇄 → LPSC-InF@PIB 복합체 → 캘린더 롤(35 µm)** 순서만 그린다.
  SI Methods 의 **doctor blade on 50 µm PET** 단계가 도식에 없어, 본문 *"slurry casting"* 과 인상이 어긋난다(서술 수준).
- **`Fig. 6a`**: 2nd 방전 상부 평탄부가 **≈2.0 V** 로 보인다(본문 *"2.2 and 1.5 V"*). 판독 불확실 **±0.1 V** —
  **저확신 관찰**이므로 본문 인쇄값을 우선한다. (100th 는 실제로 더 높은 쪽으로 이동 = 본문 서술과 정합 ✓)
- **`Fig. 6e`**: "This work" 별점 **≈4.1 mAh cm⁻² / ≈400 Wh kg⁻¹** = `Table S3`(4.17 / 410) 와 정합 ✓.
- **`Fig. 5d`·`5f`·`5g`·`6b`·`6d`**: 율속·500 cyc·EIS 곡선 전부 본문 인쇄값과 일치, 새 정보 없음.
