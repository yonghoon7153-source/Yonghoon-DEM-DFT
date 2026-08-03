# A review of band structure and material properties of transparent conducting and semiconducting oxides: Ga₂O₃, Al₂O₃, In₂O₃, ZnO, SnO₂, CdO, NiO, CuO, and Sc₂O₃ — Joseph A. Spencer (Appl. Phys. Rev. 2022)

> slug `spencer2022_review_tco_band_structure_oxides` · DOI `10.1063/5.0078037` · type `review (문헌 메타집계; 자체 실험·계산 0)` ·
> 본문 **100 pp** (011315-1 ~ -100) + Appendix A/B + refs (~1085) · digested 2026-07-28 · **본문 실물 재검증 2026-08-03 (§15)** · status ✅
> elements: Ga, Al, In, Zn, Sn, Cd, Ni, Cu, Sc, O
> methods: DFT, DOS, PDOS, phonon, Raman, XPS, elastic
> PDF 5분할(초판, 스캔): `b4d89393`(1-24) / `4f8681ba`(25-49) / `e92d9cf6`(50-74) / `665907c1`(75-99) / `925cc792`(100-126)
> **⚠ 초판은 스캔 PDF — pdftotext/pypdf 추출 0 bytes, 전부 이미지 판독.**
> **✅ 2026-08-03: 같은 논문의 네이티브 텍스트 PDF(`inbox/46. …pdf`, 127 pp) 재판독 완료 → §13 판독불가 11/12 해소 · 신규 오류 9건 · 신규 관찰 4건 · 초판 자체교정 1건. §15 참조.**
>
> **저자** Joseph A. Spencer¹'²*, Alyssa L. Mock³'⁶, Alan G. Jacobs², Mathias Schubert⁵'⁶, Yuhao Zhang¹, Marko J. Tadjer⁷
> ¹Virginia Tech CPES · ²U.S. Naval Research Laboratory · ³NRC Research Associateship · ⁴Weber State Univ · ⁵Univ. Nebraska-Lincoln · ⁶Linköping Univ (IFM)
> 투고 2021-11-09 · 수리 2022-01-05 · 온라인 2022-03-04
>
> 🔑 **왜 이게 우리 근간인가**: 리뷰가 다루는 9개 산화물 중 **8개가 우리 cascade 도펀트 로스터**에 있다 —
> **Sc₂O₃(1위)·In₂O₃(4위)·Ga₂O₃(8위)·Al₂O₃(9위)·ZnO(29)·SnO₂(30)·NiO(46)·CuO↔Cu₂O(47)**.
> 우리가 `gap_lit_eV`라는 **출처 미상 큐레이션 값**으로 들고 있던 칸의 **실험 원전 모음**이다.
> 추출표 → `db/properties/oxide_literature_properties_spencer2022.json`

---

## ⚠️ 0. 먼저 읽을 것 — 이 리뷰를 전고체전지 문맥으로 옮길 때의 한계

**이 리뷰는 전고체전지 논문이 아니다.** 문맥은 **투명전도막(TCO)·전력반도체·게이트 유전체**다.

| 리뷰가 말하는 것 | 리뷰가 **전혀** 말하지 않는 것 |
|---|---|
| bandgap, 유전상수, 유효질량, mobility, 절연파괴장 | **전기화학 안정성 창(ESW), 산화/환원 onset** |
| CTE, Debye 온도, 비열, 열전도도, 열확산도 | **Li 이온 전도도 σ, 활성화에너지 Ea, 확산계수** |
| bulk modulus (9종), Young/Poisson (Sc₂O₃만) | **황화물 SE·양극과의 계면 반응성 ΔE_rxn** |
| IR/Raman 조사, 포논 주파수 | **탄성 텐서 C_ij, 전단탄성률 G, Pugh ratio** |
| 도핑·결함의 **전자적** 역할 | 형성에너지, hull 위 거리, 표면·계면에너지 |

→ **이 리뷰는 우리 cascade 의 산화안정 축(①)과 수송 축을 대체하지도, 보조하지도 못한다.**
닿는 곳은 딱 두 군데다: **(a) 전자절연 진단 축**(`cascade_screening_funnel.json` → `electronic_insulation_diagnostic`),
**(b) 역학 참고 축**(bulk modulus, Sc₂O₃의 E/ν).

그리고 **닿는 그 두 곳에서조차 리뷰는 우리를 편들지 않는다** — 오히려 §10에서 보듯
"gap 이 크면 절연이 안전하다"는 추론을 **자기 데이터로 두 번 반박**한다.

추가 규율:
- 리뷰 수치 = **소환값**. 우리 UMA/QE 절대값과 같은 표·플롯 금지 (CLAUDE.md litdb 규율).
- 리뷰는 **재인용(secondary)**. Ref 번호를 병기했지만, 인용 시엔 원논문 PDF 확보 후.
- 여기 실린 탄성/밀도/융점은 **순수 산화물 벌크**. 우리 cascade 의 `E_VRH`(예: Sc₂O₃ x=0.02 → 18.7 GPa)는
  **도핑된 LPSCl 호스트**다. 물리적 대상이 달라서 나란히 놓으면 오독이다.

---

## 1. 한 줄 요약

9개 이원 산화물(Ga₂O₃·Al₂O₃·In₂O₃·ZnO·SnO₂·CdO·NiO·CuO·Sc₂O₃)의 **결정구조·다형·밴드구조·bandgap·
유전상수·유효질량·mobility·절연파괴장·포논·열물성**을 문헌에서 긁어모아 **물질별 요약표 9개 + 교차비교표 5개**로
정리한 100쪽짜리 데이터 리뷰. 자체 실험·계산은 없고, **"같은 물질의 같은 물성이 방법·시료·정의에 따라
얼마나 갈리는가"를 보여주는 것**이 사실상의 기여다.

---

## 2. 리뷰의 구조 (어디에 무엇이 있나)

| § | 물질 | article pp | 물질별 요약표 | 우리 로스터 |
|---|---|---|---|---|
| I | Introduction | 2-4 | Fig 1 (주기율표) | — |
| II | **Ga₂O₃** | 4-29 | **Table XI**(구조·열), **Table XII**(전기·광학) | 8위 |
| II G | 합금 (AlGaO/InGaO/AlInGaO/ZnGa₂O₄) | 24-29 | Table X | ★ co-doping |
| III | **Al₂O₃** | 30-39 | **Table XVII** | 9위 |
| IV | **In₂O₃** | 39-50 | **Table XXIII**(구조·열), **XXIV**(전기·광학) | 4위 |
| V | **ZnO** | 50-59 | **Table XXX** | 29위 |
| VI | **SnO₂** | 59-66 | **Table XXXIV**, **XXXV** | 30위 |
| VII | CdO | 66-73 | Table XLVII(추정) | ✗ |
| VIII | **NiO** | 73-78 | **Table XLII** | 46위 |
| IX | **CuO**(+Cu₂O, Cu₄O₃) | 78-86 | **Table XLVIII** | Cu₂O 47위 |
| X | **Sc₂O₃** | **86-92** | **Table XLIX**(구조), **Table L**(요약) | **1위** |
| XI | **비교 요약** | 92-100 | **Tables LI–LV** | 전 물질 |
| XII | Conclusion | 100 | — | — |
| App A | **물성 정의** | 100-101 | — | ★ 용어 |
| App B | 성장법 정의 | 101- | — | — |

**교차비교표 5개** (§XI, 9종 전체를 한 표에):
- **Table LI** 기본물성 — 안정구조/공간군, 밀도, bulk modulus, 융점
- **Table LII** 열물성 — Debye 온도, 비열, 열전도도, 열확산도, CTE
- **Table LIII** 전기물성 — electron affinity, 절연파괴장, 유효질량(e/h), mobility(e/h)
- **Table LIV** 광학물성 — gap type, bandgap, ε₀, ε_∞, IR/Raman 활성 모드
- **Table LV** β-Ga₂O₃ 방향별 평균 실험 bandgap (SE vs Absorption)

---

## 3. ★ Sc₂O₃ — 리뷰가 말하는 전부 (§X, pp. 86-92)

우리 cascade 1위이자, 이상욱 랩 코팅 스크리닝 최종 후보 Li₃Sc₂(PO₄)₃ 와 같은 Sc 계
(`litdb/papers/kim2026_hts_li3sc2po43_coating_midni_ncm.md` §10-6). 그래서 이 절이 최우선이다.

### 3-a. 리뷰가 Sc₂O₃ 를 어떻게 규정하는가

> *"Sc₂O₃ (scandia or scandium sesquioxide) is **not as widely studied** of a material as the other oxides highlighted in this review."*
> *"Sc₂O₃ has the **fewest reported material properties** throughout literature."*
> *"A lack of reported values, as was the case of Sc₂O₃ where **thermal data are essentially nonexistent** in the literature, highlights the possibility for future research."* (§XII Conclusion)

**즉 리뷰의 Sc₂O₃ 절은 "데이터가 없다"는 보고서다.** 이건 나쁜 소식이 아니라 **좌표**다 —
우리가 UMA/QE 로 Sc₂O₃ 를 계산하면 **문헌 공백에 직접 들어가는** 위치다.

**용도 문맥** (배터리 아님): 고굴절률 **반사방지 코팅**(1029), 광학소자(1030), superluminescent LED 코팅(1031),
그리고 **MOSFET 게이트 유전체**(1032-1034). 리뷰는 Sc₂O₃ 를 Ta₂O₅(1039)·ZrO₂(1040)·**HfO₂**(1041) 와 같은
high-k 게이트 후보군에 놓고, **"Sc₂O₃ 가 HfO₂ 보다 gap 이 크다"**, 그리고 **"금속이 과잉일수록 굴절률이 오른다"**
는 성질을 HfO₂ 와 공유한다고 적는다.

### 3-b. 결정구조 (p. 88, Table XLIX, Fig 35)

**안정상 = cubic bixbyite (C-type), Ia-3 (No. 206).**

bixbyite 는 Fe₂O₃·Mn₂O₃ 의 광물명이다. 구조 서술(리뷰 원문 요약):
- 양이온이 **거의 FCC 격자**를 이루고, 그 안 8개 사면체 자리 중 **6개를 산소가 점유**.
- 비등가 양이온 자리 **2종(C site, D site)**, 둘 다 **O(6) 배위**.
- **C site** = C₂ 대칭의 왜곡된 큐브, **면대각선 위에 자유 코너 2개**.
- **D site** = 축대칭, 양이온 하나를 산소 6개가 둘러싸고 **한 대각선 위에 자유 코너 2개**.
- 내부 파라미터 u, x, y, z 는 Richard et al.(1044)에 있다.
- Ubaldini(1048): bixbyite 와 일치하는 **body-centered cubic**.

> 🔑 **두 자리(C/D)가 비등가**라는 것이 뒤의 전자구조·포논에 계속 나온다.
> Sc 3d 전도대의 결정장 분열이 **두 자리에서 다르게** 일어난다(p.90).
> 우리 argyrodite 의 4a/4c(4d) 비등가 자리 서사와 문법이 같다.

**격자상수** (Table XLIX):

| 종류 | 값 (Å) | Ref |
|---|---|---|
| 실험 | 9.8459 | 1045 |
| 실험 | 9.810 | 1046 |
| 실험 | 9.845 | 1030 |
| 실험 | 9.848 | 1053 |
| 이론 | 9.708 | 1044 (LDA/GGA) |
| 이론 | 9.90 | 1044 |

본문: 계산 9.7-9.9 Å, XRD 실험 **~9.84 Å**.
⚠ Table L(요약표)은 `a = 9.708-9.90` 으로 **이론과 실험을 섞은 range** 를 헤드라인으로 쓴다.
실험만 쓰면 **9.810-9.8459 Å**.
Belosludtsev(1043): **격자상수가 격자 내 산소량에 따라 증가**한다.

**준안정 다형**:

| 상 | 구조 | 공간군 | 격자 (Å) | 조건 |
|---|---|---|---|---|
| **Monoclinic (B-type)** | 단사 | C2/m (No.12, *가정*) | a 13.173 / b 3.194 / c 7.976 / β 100.40° | **1000 °C + 13 GPa** (1051) |
| Monoclinic | — | — | — | 1273 K + 13 GPa 하소 (1047) |
| Hexagonal (A-type) | — | — | — | potential (1044) |
| Hexagonal (H-type) | — | — | — | potential, 고온형 (1044) |
| Cubic (X-type) | — | — | — | potential, 고온형 (1044) |

- **압력 반응**: 3-8 GPa → 변화 없음. **11 GPa → 매우 나쁜 B-type 결정화.** 13 GPa → 단사정 전이.
- **밀도**: cubic **3.838** → monoclinic **4.16 g/cm³**.
- **배위수 증가**: 단사정에서 **Sc 의 2/3 가 6배위 → 7배위**.
- 리뷰: 단사정이 stable 인지 metastable 인지 **명시되지 않았으나**, 밀도 변화와 요구 압력으로 보아
  **상온상압에서는 metastable** 로 시사됨.

> 🔑 우리에게: Sc₂O₃ 는 **상온상압에서 사실상 단상(cubic bixbyite)** 이다. 다형 문제로 골치 썩을 필요가 없다.
> Li₃Sc₂(PO₄)₃ 가 α/γ 상에 따라 σ 가 30배 갈렸던 것(`kim2026` §5)과 **정반대로 편한 상황**.

### 3-c. 성장 (p. 88)

- **단결정**: 전기화학(전해) 법으로 **1223 K**. 통상법은 **>2800 K** 필요 → 극적인 저온화. 결정 크기는 전해 수율로 조절 (1049).
- **박막**: MOCVD(1037) · ion beam sputtering(1035) · solution process(1054) · MBE(1034) · ALD(1055) ·
  electron beam evaporation(1030,1056) · reactive magnetron sputtering / reactive evaporation(1029,1043) ·
  water-inducement → IZO/ScOₓ TFT(1033).
- **결정성 vs 기판온도**: e-beam 증착 기판 **>150 °C → 다결정**(굴절률↑, 밀도↑); **50 °C → 비정질**.

**증착법이 물성을 바꾼다** — 리뷰가 이걸 표로 보여준다:

| 증착법 | 굴절률 @355 nm | indirect gap (eV) | direct gap (eV) | Ref |
|---|---|---|---|---|
| pulsed DC magnetron sputtering | 2.07-2.08 | **5.7** | **6.1** | 1043 |
| ion beam sputtering | 2.07 | **5.8** | — | 1035 |
| electron beam evaporation | 1.82-1.92 | **5.84** | **6.04** | 1030,1056 |

> 🔑 리뷰 원문: *"The varying results across multiple deposition methods highlight how the stoichiometry
> and deposition characteristics play a significant role in the parameters and properties of Sc₂O₃ films."*

### 3-d. 전자구조 & bandgap (p. 89-90, Figs 36-37)

**역사적 전개**(리뷰가 연대순으로 서술):
1. 1960년대: 인접 3d TM 산화물 trend(TiO₂ 3.23/3.26/3.00, V₂O₅ 2.1, CrO₃ 1.4 eV)로부터
   Companion et al.(1057)이 **5.4 eV 예측**.
   > ⚠ 이 TiO₂/V₂O₅/CrO₃ 값들은 **소환의 소환**(1960년대 trend 인용). 우리 db 의
   > TiO₂ 3.2 / V₂O₅ 2.3 / CrO₃ 2.0 과 비교하지 말 것 — 신뢰도가 두 단계 낮다.
2. 1966: **Tippins(1052)** 단결정 측정 → **6.0 eV (RT), 6.2 eV (80 K)**.
3. 2000년대 초: **indirect gap 5.7-6.0 eV** (1030,1050,1056).
4. Herrero(1032): **6.3 eV** (⚠ **방법 미기재**) + dielectric constant 14 (⚠ 정적/고주파 미구분).
5. **DFT (Richard et al. 2010, PRB 82, 035206; LDA & GGA)**: **4.0 eV @ Γ** — 실험 5.7 대비 대폭 과소.

**Table L 헤드라인**: gap type = **Indirect**, E_g = **5.7-5.84 eV (박막 실험)**.

**밴드구조 (Fig 36)**: R-A-Γ-A-X-Z-M-Σ-Γ 경로. VBM = 0 eV(E_F), CBM ≈ 4.0 eV.
**DOS/PDOS (Fig 37)** — 가전자 밴드 3덩어리:

| 위치 | 성분 |
|---|---|
| **−26 eV** | **Sc 3p** 좁은 밴드 (+ O 2s 아주 희미한 기여) |
| **−15 eV** | **O 2s** 좁은 밴드 |
| **−4.5 eV ~ E_F** | **O 2p 주도** + Sc 3d 극소량 |

> 🔑🔑 **VBM = O 2p, CBM = 빈 Sc 3d.** Sc³⁺ 는 **3d⁰** 배치라, 흡수단은
> **O(2p) → 빈 Sc 3d¹** 전이다. 3d 파동함수 겹침이 만든 전도대이고, 결정장으로 sub-band 분열하며
> **bixbyite 두 자리(C/D)에서 분열 양상이 다르다**(1052).
> 상태 혼합은 **Sc–O 결합이 이온성 + 일부 공유성**임을 뜻한다(1044,1059,1060).
>
> 우리 언어로: **Sc₂O₃ 는 d⁰ 전이금속 산화물** — 산화된 상태에서 더 이상 뺏길 d 전자가 없다.
> 이건 우리 산화안정 축과 **개념적으로** 통하지만(리뷰가 산화안정을 말하진 않는다),
> 우리 cascade 가 Sc₂O₃ 를 1위로 올린 이유(ox_V 2.356)와 **독립적으로 같은 방향을 가리킨다.**

**온도 의존성** (p. 90, Fig 38):

| 계수 | 값 | 시료 | Ref |
|---|---|---|---|
| dE_g/dT | **−3 × 10⁻⁴ eV/K** | 박막 (e-beam, 기판 50-350 °C) | 1030 |
| 관계식 | **E₀(T) = 5.9369 − 3×10⁻⁴·T(K)** | 박막 | 1030 |
| dE_g/dT | **−9.6 × 10⁻⁴ eV/K** | **단결정** | 1052 (Tippins) |

- 단결정 계수가 박막의 **3배 이상**. 리뷰는 **결정 품질 차이**를 원인으로 추정.
- indirect 흡수단 **212 → 215 nm**, direct 흡수단 **205 → 206 nm** (기판 50→350 °C). 둘 다 redshift.
- 메커니즘: **부피 변화 + 전자-포논 상호작용**(1062,1063).
- 박막 계수 −3×10⁻⁴ eV/K 는 "다른 흔한 반도체와 잘 맞는다".
- Fig 38: 기판온도↑ → **굴절률↑(1.82→1.92), indirect gap↓(5.845→5.75)**. Herve(1061)도 "n↑ ↔ gap↓" 확인.
  (⚠ 리뷰 캡션 자체가 "Note typo in legend" — 원 그림 범례에 "Ractive index" 오타)

### 3-e. 물성 (p. 90-91) — ★ 우리 EOS/역학 대조용

**밀도**

| 값 (g/cm³) | 종류 | 비고 |
|---|---|---|
| **3.79-4.1** | 실험 | Table L (1038,1043,1051,1064) |
| 4.16 | 계산 | Table L (1047) |
| 3.838 → 4.16 | 실험 | cubic → monoclinic 전이 (1051) |
| 3.9, 4.1 | 실험 | 박막 vs 벌크 — ⚠ **리뷰 문장이 모순**("thin film ... slightly higher than bulk, 3.9 and 4.1, respectively")이라 귀속 불명 |

**융점**: **2753-2823 K** = 2479.85 / 2485 / 2549.85 °C (1049,1050,1065,118).
> 🔑 **리뷰 9종 중 최고 융점**(§XI, p.92). 열적으로 가장 단단한 산화물.

**역학** — 여기가 우리에게 가장 값어치 있다:

| 물성 | 값 | 종류 | 출처 |
|---|---|---|---|
| **Young's modulus E** | **214.3-227.6 GPa** | **실험** | Dole et al. (1066) |
| Young's modulus E | 218 & 251 GPa | 계산 | Gogotsi (1064) — 두 값 차이 이유 미기재 |
| **Bulk modulus B** | **168 GPa** | 계산 (**Materials Project + LBNL**) | 1067 |
| **Poisson ratio ν** | **0.30** | 계산 (MP, B 와 함께) | 1067 |
| B (유도) | 178.6-189.7 GPa | 리뷰가 직접 유도 | Dole 의 E + MP 의 ν |

- 리뷰 원문: ***"The bulk modulus was not found in the literature"*** → **실험 B 는 없다.** 168 은 MP 계산값.
- 리뷰가 직접 유도: E = 214.3-227.6, ν = 0.30 → B = E/(3(1−2ν)) = **178.6-189.7 GPa**,
  MP 의 168 과 "relatively good agreement".
- **범위 밖으로 남겨진 것**: Gogotsi(1064)는 Sc₂O₃ 세라믹의 **brittleness measure, modulus of rupture,
  bending strength, static modulus of elasticity, ultimate strain** 도 보고했는데
  리뷰가 "outside the scope" 로 생략. → **우리가 Sc₂O₃ 역학을 더 파려면 Ref 1064 가 다음 표적.**
- ⚠ **C_ij 전탄성텐서는 리뷰 전체에 없다** — 9종 어디에도. bulk modulus(9종) + Young/Poisson(Sc₂O₃만)이 전부.

**열물성** — 거의 전멸:

| 물성 | 값 |
|---|---|
| 비열 | **94.2 J/(mol K)** → 리뷰가 M = 137.91 g/mol 로 환산 → **0.683 J/(g K)** (Ref 118) |
| Debye 온도 | **미보고** |
| 열전도도 | **미보고** |
| 열확산도 | **미보고** |
| CTE | **미보고** |

> 리뷰 원문: *"The thermal properties included in this review such as the thermal conductivity, Debye
> temperature, thermal diffusivity, CTE were not readily found highlighting the need for additional basic research."*

### 3-f. 포논 (p. 91)

BCC 라 **primitive cell 이 unit cell 안에 2번** 등장 → 진동모드 결정에 **8개 이론 단위식** 필요.
Y₂O₃(같은 C-type sesquioxide)의 진동분광(1068)을 참조해 Ubaldini(1048)가 계산:

```
Γ_op = 4A_g + 4E_g + 14F_g + 5A_2u + 5E_u + 16F_u
Γ_ac = F_u
```

| 종류 | 개수 | 조사 |
|---|---|---|
| **Raman 활성** | **22** | 4A_g + 4E_g + 14F_g |
| **IR 활성** | **16** | 16F_u |
| silent | 10 | 5A_2u + 5E_u |

- **가장 강한 Raman peak ≈ 420 cm⁻¹**, A_g + F_g **조합**.
- ⚠ **개별 모드 주파수는 Sc₂O₃ 에 대해 표로 제시되지 않는다** (In₂O₃·Al₂O₃·SnO₂ 는 전 모드 표가 있는데).

### 3-g. 전기물성 (p. 91) — 절연파괴장이 핵심

| 물성 | 값 | 종류 | 출처 |
|---|---|---|---|
| electron affinity | **0.85 eV** | **예측** (일함수 4 eV 로부터) | 1069 |
| **절연파괴장 (실험)** | **3.5 MV/cm** | **실험** (ALD 후막 평균) | 1055 (Rouffignac) |
| **절연파괴장 (예측)** | **11 MV/cm** | 예측 (Higashiwaki gap-vs-field plot) | 147 |
| 유효질량 (e/h) | **미보고** | — | 1070 이 "no known values" 명시 |
| mobility (e/h) | **미보고** | — | bulk·박막 모두 |
| 정적 유전상수 ε₀ | **미보고** | — | — |
| 고주파 유전상수 ε_∞ | **미보고** | — | **9종 중 유일**(§XI, p.100) |

> 🔑🔑 **리뷰 원문**: 예측 11 vs 실험 3.5 = ***"a stark difference"***.
> **gap 으로 절연내압을 예측하는 관행이 Sc₂O₃ 에서 3배 넘게 틀린다**는 자백이다. §10에서 다시 다룬다.

애매한 단일 보고: Herrero(1032)의 "dielectric constant of 14" — **정적인지 고주파인지 리뷰도 특정 못 함**.
그대로 쓰면 안 된다.

### 3-h. 도핑·결함 (p. 91)

> *"Dopants for Sc₂O₃ are not readily seen throughout literature. **However, Sc was seen as the dopant
> for many materials.**"* (1071-1075, 상세는 범위 밖)

**→ Sc₂O₃ 를 도핑한 연구는 거의 없고, Sc 를 남에게 넣는 연구만 많다.**
(참고: 리뷰 ZnO 절은 **Sc 를 ZnO 의 shallow donor** 로 명시한다 — Zn²⁺ 를 치환. p.57)

**결함** — 둘 다 ion beam sputtering 박막 연구:

| 결함 | 발견 | Ref |
|---|---|---|
| **산소 침입형(O interstitial)** | 비정질 Sc₂O₃ 박막에서 관측. 밀도↑ → **박막 흡수↑**. 흡수 원인은 **bandgap 내 trap state** | 1035 (Langston) |
| **산소 결함** | O₂ flow = 0 sccm 이면 결함 다량 → **박막에 큰 변형(strain)**. flow rate 제어·제한이 필수 | 1076 (Kong) |

리뷰 결론: *"Much more research is needed on the defects of Sc₂O₃ and their origins."*

### 3-i. Sc 합금 (p. 91-92) — ★ 우리 co-doping 관심사와 직결

> *"Alloys for Sc₂O₃ are even rarer than Sc₂O₃ itself."*

**① ScGaO (Sc₂O₃-Ga₂O₃)** — **우리 cascade 1위 × 8위의 이원계**

- **이온반경**: Ga³⁺ **0.62 Å** vs Sc³⁺ **0.745 Å** → **차이 ~20%**.
  리뷰: *"This difference makes some of the possible solid solutions unlikely."*
- **4가지 가능한 상** (Sc₂O₃ 함량 **증가 순서**로 나열, Ref 1078):
  1. Ga₂O₃ 기반 **치환형 고용체**
  2. Ga₂O₃ 기반 **부분 규칙화** 고용체
  3. Ga·Sc 가 **서로 다른 자리 규칙**을 갖는 규칙 고용체
  4. Ga₂O₃ 와 **구조가 다른 완전히 새로운 화합물**
  > 🔑🔑 **"용질 농도가 늘면 치환형 → 부분규칙 → 규칙 → 신상" 4단계 도식.**
  > 우리 cascade 의 x = 0.02/0.05/0.10 sweep 이 **어느 단계에 있는지** 물어야 한다는 뜻이다.
- **Czochralski 성장**: 융점 **~1770 °C**. 격자상수 **a 12.496 / b 3.101 / c 5.873 Å, β 103.26°**
  (β-Ga₂O₃ 의 12.214/3.037/5.998/103.83° 와 매우 가깝다 → Ga₂O₃ 기반 고용체 쪽).
  seed/central/tail 세 절단면의 격자는 크게 다르지 않았으나 **tail → seed 로 갈수록 Sc 함량 증가**(성장 중 분배).
- **Zhu et al.(1078)**: Sc₂O₃-Ga₂O₃ 합금의 구조·전자물성 DFT.
  ***"identify a method of altering the conduction band and valence band offsets by incorporating more Sc into the alloy."***
  → **Sc 를 더 넣어 밴드 오프셋을 조절한다.** 상세는 원논문으로 넘김.
  > 🔑 **Action item: Ref 1078 원논문 확보.** Sc 밴드정렬의 1차 출처다.

**② CuScO₂ (CSO)** — PLD on α-Al₂O₃

- rhombohedral + hexagonal 두 구조. (0001) 면에 3회·6회 대칭, **a축 격자상수가 ZnO 와 유사**.
- **p-type**. 2가 양이온이 Sc 를 치환하면 정공 생성.
- **gap 3.7 eV** (optical transmission, c축 배향, direct allowed transition).
- **CSO/ZnO p-n 이종접합** 가능. (1079, Kakehi)

**③ YScO — (Y_xSc_{1-x})₂O₃ 삼원 박막**

- **절연파괴장 4.0-4.8 MV/cm** — **Sc₂O₃ 단독 실험값 3.5 MV/cm 보다 높다.** (1054, Hu)
> 🔑 **Sc₂O₃ 에 Y 를 섞으면 절연내압이 오른다** = 리뷰 안에서 **Sc 계 co-doping 이 전자적 물성을
> 개선한 유일한 정량 사례**. 우리 co-doping 서사에 쓸 수 있는 한 줄.
> (참고: 우리 cascade 에 Y₂O₃ 는 5위로 이미 있다. Sc+Y 페어는 리뷰가 지지하는 조합이다.)

**④ LLP 인광체 Sr₂Sc□O₅** ⚠ **화학식 판독 불가**

- 인쇄가 "Sr₂ScAcO₅" 로 보이나 중간 원소를 확정 못 했다(Al 추정, **단정 금지**).
- long lasting phosphorescence(LLP) 물질. ZnGa₂O₄·LiGa₅O₈·Zn₃Ga₂Ge₂O₁₀ 등 다른 LLP 산화물과 비교 목적.
- **orthorhombic, a 5.908 / b 15.180 / c 5.709 Å**.
- **DFT indirect gap 4.24 eV** (VBM = X point, CBM = G point), **optical gap 4.75 eV**
  (extrapolation + UV diffuse reflectance). 리뷰: 광학 gap 이 큰 이유는 **LDA 의 비광학 gap 과소평가** 때문.
- Sm³⁺ 를 Sr 자리에 첨가 (1080, Li).

**⑤ SrGaScO 페로브스카이트군** (1081, Chernov)

- **Sr₂GaScO₅** (Brownmillerite) / **Sr₁₀Ga₆Sc₄O₂₅** (신규 산소결핍 페로브스카이트) / **SrGa₀.₇₅Sc₀.₂₅O₂.₅** (cubic perovskite)
- 발견: **산소 함량을 고정한 채 Sc/Ga 비만 바꾸면 페로브스카이트 상과 구조가 바뀐다** —
  Sc³⁺ 와 Ga³⁺ 의 결정화학 차이 때문.
> 🔑 **같은 원소쌍의 "비율"만 바꿔도 상이 갈린다.** 우리 dual-x co-doping 에서 비율 자체가
> 설계변수라는 문헌 근거.

**리뷰의 Sc 합금 총평**:
> *"While this report deviates from the scope of the oxide review, it was included to highlight the
> **rarity and complexity of alloys containing Sc₂O₃** in the literature."*
> 반면 **ScAlN(scandium aluminum nitride)** 은 훨씬 잘 이해되어 있고 AlGaN/InAlN 보다 **압전성이 훨씬 커서**
> nitride 이종구조 배리어층으로 집중 개발 중 (1082-1085).

### 3-j. Sc₂O₃ 한 장 요약 (Table L 전사)

| 항목 | 값 | 종류 | Ref |
|---|---|---|---|
| 안정상 | Bixbyite (C-type) | — | 1052 |
| 안정구조 | Cubic **Ia-3 (No. 206)**, a = 9.708-9.90 Å | 이론+실험 혼합 | 36,1030,1044,1053 |
| 준안정상 | Monoclinic (B-type) | — | 1051 |
| 가능상 | Hexagonal A/H-type, Cubic X-type | — | 1044 |
| 밀도 | **3.79-4.1** g/cm³ / 4.16 | 실험 / 계산 | 1038,1043,1051,1064 / 1047 |
| **bulk modulus** | **168 GPa** | **계산(MP)** | 1067 |
| 융점 | 2479.85 / 2485 / 2549.85 °C | — | 1050 / 118 / 1049,1065 |
| 비열 | **0.683 J/(gK)** | — | 118 |
| electron affinity | **0.85 eV** | **예측** | 1069 |
| **절연파괴장** | **11** (예측) / **3.5** (실험) MV/cm | 예측 / 실험 | 147 / 1055 |
| gap type | **Indirect** | — | 1030 |
| **E_g** | **5.7-5.84 eV** | **박막 실험** | 1030,1050 |
| IR 활성 | **16F_u** | 예측 | 1048 |
| Raman 활성 | **4A_g, 4E_g, 14F_g** | 예측 | 1048 |

**Table L 에 없는 것** (리뷰가 "not found in the literature" 라고 명시): Young's modulus(본문엔 있음),
ε₀, ε_∞, 굴절률(본문엔 있음), 유효질량, mobility, CTE, Debye 온도, 열전도도, 열확산도.

---

## 4. Al₂O₃ (§III, pp. 30-39) — 우리 9위

**리뷰의 위치 설정**: Al₂O₃ 는 **반도체 산화물로 취급되지 않는다**. 리뷰가 넣은 이유는
(a) 다른 8종의 **baseline**, (b) **Ga₂O₃ 와 합금(AlGaO)을 만드는 파트너**.

### 4-a. 구조 — 다형이 9개다

**안정상 = α-Al₂O₃ (corundum), R-3c (No. 167), unit cell 10 atoms.**
나머지 **전부 metastable**: γ, η, θ, δ, κ, χ (+ θ′, θ″, λ 존재 근거).
분류: γ/η/θ/δ = **FCC 산소 배열**, κ/χ/α = **hexagonal 산소 배열**.

| 격자 표현 | 값 (Å) |
|---|---|
| Trigonal (hexagonal 파라미터) | a 4.75, c 12.97 |
| Hexagonal (RT) | **a 4.762, c 12.896** |
| Trigonal 단위셀 파라미터 | a 5.128 |

2000 °C 로 올리면 a 는 **+1.83%**, c 는 **+1.86%**, 삼방 a 는 **+1.35%**.

**준안정 다형 격자상수** (Table XIII):

| 상 | 구조 | 공간군 | 격자 (Å) |
|---|---|---|---|
| δ | Tetragonal | P-4m2 (#115) | a 5.599, c 23.657 |
| δ | Orthorhombic | P2₁2₁2₁ (#19) | a 16.4, b 12.2, c 8.2 |
| η | Cubic | Fd-3m (#227) | a ≈ 7.9 / 7.94 |
| γ | Cubic | Fd-3m (#227) | a ≈ 7.9 |
| κ | Orthorhombic | Pna2₁ (#33) | a 4.6, b 8.18, c 8.87 |
| χ | Hexagonal | P6₃/mcm (#193) | a 5.56 c 13.44 / a 5.57 c 8.64 |
| χ | Cubic (non-spinel) | — | a 7.94 |
| θ | Monoclinic | C2/m (#12) | a 11.813 b 2.906 c 5.625 β 104.1° / a 11.795 b 2.91 c 5.6212 β 103.79° |

> 🔑 **γ 와 η 는 파라미터가 사실상 동일**(둘 다 Fd-3m, a ≈ 7.9-7.94)한데도 **별개 상**이다.
> 이유: *"This is a result of the chemical ordering within the cations of the fcc anion structure."*
> → **격자상수가 같아도 양이온 배열(화학적 질서)이 다르면 다른 상.**
> 우리 disorder ensemble 서사(`kb/concepts/ordered_vs_disordered.md`)와 정확히 같은 명제다.

- γ-Al₂O₃ bandgap: 벌크 **8.7 eV**(292,293) → 박막에선 **2.5 eV** 로 급락(294, Ealet).
  이유는 α-Al₂O₃ 의 감소와 같은 **gap 안의 결함 준위**.
- δ 상은 전구체 열산화 또는 용융 quench 시 출현; 원래 boehmite(AlOOH) 에서 유래(289).

### 4-b. 전자구조 & bandgap

**gap type = Direct** (VBM/CBM 모두 Γ, Ref 285).
⚠ 단 Ching(284) OLCAO 는 direct 6.31 / **진짜 최소는 indirect 6.29 eV** — 차이가 작아 "검출 불가" 수준.

**밴드 성격** (Fig 18: GGA-PBE + tight-binding):
- **VB 최상단 = O 2p_x, 2p_y, 2p_z 거의 단독**
- 중간 = Al 3s + O 2p
- 최하단 = O s + Al 소량
- **CBM = Al 3s**, 상위 CB = Al 3p 반결합
- **강한 이온성** → valence band 가 깊이 끌려가지 않는다(α-quartz 의 공유결합 대비).
  가전자대 그룹 사이의 넓은 간극이 "ionicity gap" 으로 불리며 전자 상태가 없다 = 이온결합의 추가 증거.
- **VBM 은 Γ-A 방향 빼면 분산이 거의 없다** → **정공 유효질량 이방성 극대**.
  CB 는 Γ에서 포물선 → **전자 유효질량 등방**.
- CBM DOS 가 매우 작다(~1 electron/eV), 2차 전도대는 ~6 electron/eV 로 훨씬 크다.

**bandgap — bulk 와 film 이 2 eV 넘게 갈린다** (Table XIV):

| E_g (eV) | 방법 | 시료 | Ref |
|---|---|---|---|
| 8.8 | VUV transmission, ∥c | bulk | 271 |
| 9 | reflectance, ∥c | bulk | 271 |
| 9.2 | VUV-ref., ∥c (KK 모델) | bulk | 326 |
| 9.25 | VUV-ref., ⊥c (KK 모델) | bulk | 326 |
| 9.9 | polarized ref/trans | bulk | 319 |
| **6.2** | photoconductivity | **film** | 320 |
| **6.52** | energy loss spectra | **film** | 321 |
| **6.7** | XPS | **film** | 322 |
| **6.7** | X-ray absorption | **film** | 323 |
| **6.8** | XPS (ALD 250 °C, PE-ALD) | **film** | 307 |
| 6.29 | OLCAO | calc | 318 |
| 6.3 | HSE03 | calc | 324 |
| 8.0 | HSE03 | calc | 324 |

> 🔑🔑 **bulk 단결정 8-9 eV vs 비정질 박막 6.2-6.8 eV.**
> 리뷰: *"There appears a wide range of results spanning several eV depending on whether the sample
> is bulk or thin film."*
> **우리 문맥에서 Al₂O₃ 는 대개 비정질 ALD 코팅으로 존재한다** → `gap_lit_eV` 8.8 을 그대로 쓰면
> 절연성을 **2 eV 과대평가**한다.

**온도 의존성** (French 271):
- RT 8.8 eV → **1763 K 에서 7.2 eV** (총 **1.6 eV 감소**), 300-1573 K 선형.
- **γ = −1.1 meV/K** (실험). exciton peak(9 eV) −1.0, 12-13 eV peak −0.7 meV/K.
- 분해: **열팽창 −0.31 + 포논 −0.62 = 계산 −0.93 meV/K** (실험 −1.1 과 비교).
- 비교: Si −0.22, Ge −0.44 meV/K → **Al₂O₃ 가 훨씬 크다** (이온-전자 혼합 성격 때문).

### 4-c. 유전상수·유효질량·mobility·절연파괴장

| 물성 | ⊥c | ∥c |
|---|---|---|
| **ε₀ (정적)** | **9.385** | **11.614** |
| **ε_∞ (고주파)** | **3.077** | **3.072** |

> 🔑 **정적은 이방성이 뚜렷(9.4 vs 11.6), 고주파는 사실상 등방(3.077 vs 3.072).**
> 리뷰: *"There is clear anisotropy for the static dielectric constant due to the uniaxial nature of the
> material; however, anisotropy does not appear as strongly for the high-frequency constants."*
> **우리 ε_∞ 체인(전자 분극성)** 논의([kraft2017] digest 참조)에 쓸 수 있는 관찰:
> 전자 분극성은 격자 이방성에 둔감하고, 이온 기여가 이방성을 만든다.

- **유효질량**: 전자 **0.38-0.40 m_e**(계산), 등방 (0.40 ⊥c = 0.40 ∥c).
  정공 **6.3 m_h (⊥c) vs 0.36 m_h (∥c)** — **리뷰 9종 중 예측 정공 유효질량 최대**.
  실험 터널링 유효질량은 0.05-0.42 m_e 로 넓다.
- **mobility**: 실험 Hall 0.8-100 cm²/(V s). 계산(900 °C): **∥c 24 vs ⊥c 7.3 cm²/(V s)** —
  c축 방향이 원자충전이 성겨 산란중심이 적다.
- **절연파괴장**: 실험 **5.2-8 MV/cm**, 예측 **>20 (최대 25) MV/cm**.
  > 🔑🔑 리뷰 원문: ***"Al₂O₃ has a bandgap of almost double β-Ga₂O₃, but that value does not
  > correlate to a superior electrical breakdown field."***
  > **gap 이 2배라고 절연내압이 2배가 아니다.**
- **electron affinity 1.58 eV** (Pollack 358, J-V 로부터). 범위 1-2.58 eV.

### 4-d. 포논 (Table XV — 전 모드 수치)

```
Γ = 2A_1g + 2A_1u + 3A_2g + 2A_2u + 5E_g + 4E_u
```
10 atoms(4 Al + 6 O) → 30 Γ 모드 = 3 acoustic + 27 optical.
반전중심 존재 → **IR 활성은 Raman 금지, Raman 활성은 IR 금지**(상호배타).
Raman 활성 **2A_1g + 5E_g**, IR 활성 **2A_2u + 4E_u**, silent **2A_1u + 3A_2g**.

| Raman (cm⁻¹) | | IR TO/LO (cm⁻¹) | |
|---|---|---|---|
| A_1g(1) | 417.4 | A_2u(1) | 397.52 / 510.87 |
| A_1g(2) | 644.6 | A_2u(2) | 582.41 / 881.10 |
| E_g(1) | 378.7 | E_u(1) | 384.99 / 387.60 |
| E_g(2) | 430.2 | E_u(2) | 439.10 / 481.68 |
| E_g(3) | 448.7 | E_u(3) | 569.00 / 629.50 |
| E_g(4) | 576.7 | E_u(4) | 633.63 / 906.60 |
| E_g(5) | 750.0 | | |

**포논 변형 퍼텐셜(PDP)** (Table XVI, Zhu 355, 단위 10³ cm⁻²) — 굽힘 캘리브레이션으로 실측:
A_1g: K₁ −396±19, K₂ −406±6, K₃ −777±18 · E_g: K₁ −293±22, K₂ −227±24, K₃ −3.2±0.5, K₄ −8.5±1.
> 🔑 **"변형이 포논 주파수를 얼마나 옮기는가"를 정량화한 표.** 우리 phonon/strain 연결에 참고.

### 4-e. 열·역학

| 물성 | 값 |
|---|---|
| Debye 온도 | 계산 **1045 K**, 실험 965-1044 K (**9종 중 최고**) |
| 비열 | 0.750-0.785 J/(gK) @RT (소결체는 20→1500 °C 에서 0.755 → 1.33) |
| 열전도도 | 30 / 33 / 30-40 W/(mK); 단결정 35-54; **박막 0.25-0.8**; 소결체 20→1500 °C 에서 33 → 6.23 |
| 열확산도 | RT ~1.0-1.1×10⁻⁵ m²/s → 1000 K 에서 ~0.2×10⁻⁵ |
| CTE | 4.5-5.5 ×10⁻⁶/K @RT (1000-1600 °C 평균 7.5±0.4) |
| 밀도 | 3.92-3.984 g/cm³ (99.8% 순도 3.97-3.99) |
| **bulk modulus** | **257 GPa @20 °C** (실험), 225-252 (계산); **300→1500 °C 에서 257 → 227** |
| Vickers 경도 | **RT 15 GPa → 1500 °C 2.5 GPa** |
| 융점 | 2050-2071.85 °C |

### 4-f. 도핑·결함

- 도판트: Ti, Co, Fe, Mg, Y, Cr, Ca, Si, V.
  - **Ti**: Al 자리, 3가/4가 공존. Ti⁴⁺ 는 전하보상용 native defect 를 만들어 **이온결함 증가로 전도도 상승**.
  - **Mg**: acceptor. native 이온결함 증가, 정공은 소수 종. **이온전도는 이방성, 전자전도는 등방.**
  - **Y**: 고온 creep 억제. **Y 도핑 시 입계 확산도가 10배 감소.**
- 결함: 산소공공이 지배. **Al 이온이 5가지 원자가 상태(2+ ~ 2−)** 를 가질 수 있게 하고,
  이 vacancy state 들이 **Poole–Frenkel hopping** 전도를 만든다.
  > 🔑🔑 리뷰 원문: *"The vacancy states of α-Al₂O₃ allow charge carriers to 'slowly' make their way up
  > through the energy bandgap by stopping at the localized traps of the vacancies... explains how an
  > oxide with such a large bandgap as that of α-Al₂O₃ **can be considered a semiconducting oxide at times**."*
  > → **큰 gap 이 전자절연을 보장하지 않는다**는 두 번째 반증.
- 밴드정렬: α-/θ-Al₂O₃ 의 **+/0 vacancy level 이 HfO₂ 보다 gap 안쪽 아래**에 있고,
  Fermi 를 올려도 안정 형태를 유지(HfO₂ 는 아님) → HfO₂ 대체 게이트 유전체 후보.

---

## 5. In₂O₃ (§IV, pp. 39-50) — 우리 4위

### 5-a. 구조

**안정상 = bcc-In₂O₃ (bixbyite, C-type rare-earth sesquioxide), Ia-3 (No. 206), a = 10.117-10.118 Å.**
Unit cell **80 atoms**: In 32(24는 d 자리, 8은 b 자리) + O 48(특별한 위치 없음).
In-O 2.12-2.21 Å, In-In 3.35-3.36 Å. In 은 O 6개와 팔면체 배위.
b 자리는 축대칭, d 자리는 배위 비대칭.

> 🔑 **Sc₂O₃ 와 같은 bixbyite Ia-3 구조**다 (a 9.84 vs 10.12 Å). 심지어 δ-Ga₂O₃ 도 Ia-3 로 보고된다.
> **Sc/In/Ga(δ) 세 도펀트가 같은 구조족**이라는 것은 co-doping 을 생각할 때 실질적 정보다.

**다형** (Table XVIII):

| 상 | 구조 | 공간군 | 격자 (Å) | 비고 |
|---|---|---|---|---|
| bcc-In₂O₃-I | Cubic | I2₁3 (#199) | a 10.120 | 이론; Fuchs(428) **불안정 판정** |
| **rh-In₂O₃** | Rhombohedral | R-3c (#167) | a 5.478, c 14.51 | **고압 안정화**; f.u.당 부피 62.85 < bcc 64.72 Å³ |
| o′-In₂O₃ | Orthorhombic | Pbcn (#60) | 7.929/5.482/5.589 (9 GPa,600°C) 등 3세트 | |
| α-Gd₂S₃ type | Orthorhombic | Pnma (#62)/Pn2₁a (#33) | 5.473/3.003/11.618 | modeled |

### 5-b. ★ bandgap — 우리 `gap_lit_eV` 2.9 의 정체

**gap type = "Debated"** (Table XXIV). 이유가 물리적이다:
- bcc(bixbyite) 는 VBM/CBM 모두 Γ → **형식상 direct**.
- 그러나 **VBM → CBM 광학전이가 dipole 금지**. 하위 가전자대 → CBM 전이도 금지이거나 행렬요소가 작다.
- → 흡수계수는 **fundamental gap 보다 0.5-1.0 eV 높은 곳에서야** 크게 증가.
- rh 상은 CBM Γ / VBM L → **indirect**.

**King et al.(455) 의 결정적 한 쌍** (p.43):

| | fundamental | optical |
|---|---|---|
| 이론 (cubic) | 3.10 eV | 3.72 eV |
| **실험 (cubic)** | **2.93 eV** | **3.55 eV** |

> 🔑🔑 **우리 `gap_lit_eV` = 2.9 는 fundamental gap 2.93 eV 와 사실상 같다.**
> 반면 문헌·DB 다수가 인용하는 **3.6-3.7 eV 는 optical gap**이다.
> → **우리 값은 틀리지 않았다. 다만 정의가 다르다.**
> 이 라벨 없이 다른 산화물의 optical gap 과 나란히 순위를 매기면 **In₂O₃ 만 부당하게 낮게 평가**된다.

**보조 증거**: Weiher(237) — 흡수 onset 2.6 eV 시작 → 2.94 eV 까지 이어짐.
모델 결론: **Γ에서 direct allowed 3.7 eV** + **indirect forbidden 2.6 eV**. ARPES(87)와 일치.

**계산 스펙트럼** (Table XIX) — functional 사다리가 그대로 보인다:

| 방법 | E_g (eV) |
|---|---|
| LDA | **1.11-1.21** |
| GGA+U | 1.82 |
| LDA+U | 2.18-2.21 |
| HSE03 | 2.20-2.45 |
| **HSE03+G₀W₀/Δ** | **3.10** |

> 🔑 **LDA 가 1.1 eV, 실험이 2.93 eV** — PBE/LDA gap 과소평가가 **2.6배**다.
> 우리 "PBE gap 은 과소" 규율의 극단 사례.

**온도 의존성** (Irmscher 458):
- 300 K 2.76 eV → 9 K **2.94 eV**. 0 K 외삽 **2.884 eV**.
- **1200 K 에서 ~1.5 eV** — 저온 대비 **절반**. 다른 반도체 대비 극단적.
- 원인: **전자-포논 결합 상수가 6.73 → 8.24 로 증가**.
- γ = −1.1×10⁻³ (438) / −1.0×10⁻³ eV/K (237). Bose-Einstein: α_B 16 meV, θ 30.1 meV (460).

**두께 의존**: 420 → 35 nm 박막에서 optical gap 3.57 → 3.49 eV.
**변형 의존**: deformation potential −4.2 ~ −3.66 eV (ZnO 보다 크고 GaAs/GaN 보다 작음).
**cubic vs rh**: Wang(429) cubic 3.7 > rh 3.0 eV. King(455) rh 가 fundamental 은 크고 optical 은 작다
→ **문헌 간 부호가 갈린다.**

### 5-c. 유전상수·유효질량·mobility

- **ε₀**: 계산 9.0-10.74, 실험 8.9, **LST 10.55±0.07** (DFT 10.74 와 일치).
  ⚠ "9.5" 라는 값이 관행적으로 계산에 쓰였는데 **근거 불명**(Hamberg 406).
- **ε_∞**: 계산 3.82-4.128, 실험 4.0-4.05 (**4.05±0.05**, DFT 4.128·4.08 과 일치).
- **이방성 없음** (cubic bixbyite; rh 도 거의 없음, Walsh 463).

**유효질량 (Table XXII)** — 여기가 In₂O₃ 의 하이라이트다:

| 값 (m_e) | 방법 | 종류 |
|---|---|---|
| 0.14 | Hall-Seebeck | 실험 |
| 0.18 | plasma frequency | 실험 |
| **0.208±0.006** | **optical Hall effect** | 실험 |
| 0.30±0.03 | Hall-Seebeck | 실험 |
| 0.40 | plasma frequency | 실험 |
| 0.55 | Hall-thermoelectric power | 실험 |
| 0.16 / 0.18 / 0.22 | LDA / LDA / HSE03 | 계산 |

> 🔑🔑 **산포의 이유가 밝혀져 있다: 전도대가 비포물선이라 캐리어 농도가 오르면 유효질량이 커진다.**
> n ≤ 5×10¹⁹ cm⁻³ → 0.18 · n ~ 10²⁰ → 0.30 · n = 10²¹ cm⁻³ → **0.40 m_e** (487).
> → **"In₂O₃ 의 유효질량"은 단일 숫자가 아니다.**
> 이건 우리가 `gap_lit_eV` 를 다룰 때와 같은 병이다 — **물질상수처럼 보이는 값이 사실 상태변수**다.

- **mobility**: 이론 한계 270 / 274 cm²/(V s). 실험 7.81(박막) ~ **226**(벌크 RT 최고).
  배향 의존: UID 박막 (111) 110 vs (001) 55. 100 K 로 냉각 시 **1290** 까지.
  RT 는 **polar optical phonon scattering** 지배, 100 K 이하는 dislocation/impurity.
- **절연파괴장 3-4 MV/cm** (예측만). 리뷰: *"not a parameter of great interest, making it hard to find."*
- **electron affinity**: 3.3(계산, **9종 중 최저 인용값**) / 3.7 / 4.3 / 4.45 eV.

### 5-d. 포논 (Tables XX, XXI — 전 모드 수치표)

primitive cell **40 atoms → 117 optical modes**:
```
Γ_opt = 4A_g + 5A_u + 4E_g + 5E_u + 14T_g + 16T_u
```
A_g/E_g/T_g = Raman, **T_u = IR**, A_u/E_u = silent.
16개 IR 모드 중 **오래도록 11개만 검출**됐고, T_u(12)-T_u(16)은 세기가 약해 Stokey(484)가 처음 관측.
대표: T_u(1) TO 588.61(calc)/594.9(exp), LO 611.35/624 → T_u(16) TO 100.86/99.0 cm⁻¹.
Raman: F_2g(1) 106-112 → F_2g(14) 600-636 cm⁻¹ (22개 전부 계산·실험 대조).

**In₂O₃ vs SnO₂ 포논 비교** (p.47) — 리뷰가 직접 대조:
> In₂O₃ 는 SnO₂ 대비 **포논 매개 간접흡수가 50% 적다**. SnO₂ 가 전자-포논 결합이 더 강하고,
> ε₀-ε_∞ 차이도 더 크다(이온성이 더 강함). LO 포논 주파수도 SnO₂ 가 높다.
> → In₂O₃ 의 약한 간접흡수는 **작은 전자-포논 결합 + 낮은 LO 주파수** 때문.

### 5-e. 열·역학

| 물성 | 값 |
|---|---|
| Debye 온도 | 계산 700-811 K, 실험 **420±20 K** (⚠ 순수/Sn 도핑 미명시) |
| 비열 | 0.356 J/(gK)(몰비열 환산) / 0.837(가정값 환산 — **측정 아님**) |
| 열전도도 | RT 10-15 W/(mK); **어닐 후 (111) 20 K 에서 5000 W/(mK)** (다이아몬드/Si 급) |
| 열확산도 | ITO 박막 1.2 mm²/s, 벌크 계산 7.0 (**9종 중 최고**) |
| CTE | 6.15-10.2 ×10⁻⁶/K |
| 밀도 | 7.12(실험)/7.2(계산); ⚠ Wheeler 6.3 은 이상치 |
| **bulk modulus** | 실험 **194.24 GPa**, 계산 174-192.66 |
| 융점 | 1949-1950 °C |

> 🔑 **rh 상이 모든 압력에서 cubic 보다 bulk modulus 가 크다**(463) — 고압상이 더 단단.
> 열전도: Ge 도핑으로 3 → 0.6 W/(mK), ZT 0.1 → 0.45 (In₁.₈Ge₀.₂O₃, Ref 483).

### 5-f. 도핑·결함 (+ ITO)

- **O vacancy = double donor**, **In vacancy = triple acceptor**(n-type 보상중심).
  In vacancy 형성에너지가 높아 **p-type In₂O₃ 는 사실상 불가**(528).
- **Sn(ITO)**: In 치환, n-type. 캐리어 5×10²⁰ cm⁻³ @1 wt% Sn. 그러나 **mobility 는 UID(160-170)보다 낮다** —
  자유캐리어 산란 증가. 그리고 **Sn 일부가 전기적으로 비활성**.
- **Ti**: PLD, 표면거칠기 2 nm(Sn 의 절반), mobility 최대 **154 cm²/(V s)**. 상용 TCO 대비 우수(511).
- **Mo**: Mo(4d)가 In(5s)와 거의 혼성하지 않아 **도너를 전도대에서 분리** → 이온화 불순물 산란 감소,
  mobility 65.3 / 80-130 cm²/(V s). 같은 농도 Sn 대비 산란 훨씬 적음. **rh 상 형성도 억제**(517,518).
  > 🔑 **"도너를 전도대에서 떼어놓아 산란을 줄인다"** — 궤도 혼성으로 수송을 설계하는 사례.
  > 우리 [ke2025] MgClO s-p/p-p 혼성 서사와 같은 문법(다른 물리).
- 기타 도판트: H, W, Fe, Zn, Ta.
- ITO 의 보상 acceptor 는 In vacancy 가 아니라 **침입형 산소**(positron annihilation, 506).

---

## 6. Ga₂O₃ (§II, pp. 4-29) — 우리 8위 · 리뷰의 주인공

리뷰 100쪽 중 26쪽. **이방성이 물성 전반을 지배**하는 사례 연구다.

### 6-a. 구조 & 다형

**안정상 = β-Ga₂O₃, C2/m (#12), monoclinic.**
a 12.214 / b 3.037 / c 5.998 Å, **β 103.83°** (Ref 32).
**Ga(I) = 사면체 배위, Ga(II) = 팔면체 배위.** 산소는 O(I)/O(II)/O(III) 세 자리로 "distorted cubic" 충전.

| 다형 | 구조 | 공간군 | 격자 (Å) |
|---|---|---|---|
| **α** | Trigonal/rhomb. (corundum) | R-3c (#167) | a 4.97-4.983, c 13.433-13.457 |
| **γ** | Cubic (defective spinel) | Fd-3m (#227) | a 8.22-8.35 |
| **δ** | **Body-centered cubic** | **Ia-3 (#206)** | a 9.52(예측)/10.00 |
| **ε** | Hexagonal | P6₃mc (#186) | a 2.907, c 9.255 |
| **κ** | Orthorhombic | Pna2₁ (#33) | a 5.0463, b 8.7020, c 9.2833 |

- **α 는 corundum** = Al₂O₃ 안정상과 동형 → AlGaO 합금의 α 쪽 종점.
- **δ 는 Ia-3 (C-type rare earth)** = **Sc₂O₃·In₂O₃ 와 같은 bixbyite 구조족.**
- **ε 는 반전대칭이 깨져 압전성 예측**. κ 는 ε 의 subgroup.
- **Fig 10**: 다형별 실험/계산 bandgap 산점도. **δ 상은 gap 보고 자체가 없고, γ 상은 실험 보고가 없다.**
- α/ε/κ 는 β보다 gap 이 약간 크다 → bandgap engineering 여지.

### 6-b. ★ bandgap — 우리 4.8 eV 가 왜 낮은가

**gap type = Direct.** 그런데 **편광 방향별로 0.5 eV 이상 다르다** (Table LV):

| 방법 | E∥c | E∥a | E∥b |
|---|---|---|---|
| **SE (ellipsometry)** | **5.095** | **5.385** | **5.66** |
| **Absorption onset** | **4.50** | **4.57** | **4.73** |

> 🔑🔑 **리뷰의 명시적 판정** (p.12):
> *"Reported values from absorption measurements **fail to include excitonic effects**, effectively
> shifting the reported bandgap **down** by the neglected binding energy value. Ellipsometry
> investigations were able to fully account for anisotropy, excitonic effects, and dipole orientations
> thus we conclude that **these values best represent the true fundamental bandgap values of β-Ga₂O₃**."*
>
> → **우리 `gap_lit_eV` = 4.8 은 absorption 관행값**이고, 리뷰 기준으로는 **계통적 과소**다.
> 더 근본적으로, **이방성 물질에 스칼라 gap 하나를 붙이는 것 자체가 물리적으로 불완전**하다
> (b > a > c 순서는 방법 무관하게 성립).

**온도 의존성** (p.12) — 리뷰가 5개 연구를 모아놓았다:

| γ (meV/K) | 방향/조건 | Ref |
|---|---|---|
| −0.769 | [-201] 박막, 77-298 K (4.82→4.65 eV) | 109 |
| −0.98 / −0.18 | E∥c / E∥b, 77 & 300 K 2점 | 44 |
| −0.83 / −1.03 / −0.60 | a / c / b 근처 전이, 고온 SE (RT-550 °C) | 110 |
| −0.90 / −0.90 / −0.47 | a / c / b 근처 전이, 저온 SE (10-300 K) | 111 |

- **0 K gap**: E∥a **5.069**, E∥c **5.41**, E∥b **5.7 eV**.
- **포논 bath 온도 θ_B = 0.067 eV (537.7 cm⁻¹)**; 대칭독립 광학포논 산술평균 **507.5 cm⁻¹** 과 일치
  → **Bose-Einstein 근사의 타당성 확인**.
- 저온(Sturm)과 고온(Mock) 계수가 "excellent agreement" → effective phonon bath 근사 유효.

### 6-c. ★★ 캐리어 농도가 gap 을 바꾼다 (p.20)

이것이 이 리뷰에서 **우리 db 규율에 가장 직접 타격**을 주는 관찰이다 (Rafique 109):

| 조건 | gap 변화 | 메커니즘 |
|---|---|---|
| n = 1×10¹⁶ → 2.52×10¹⁸ cm⁻³ | **4.69 → 4.716 eV (증가)** | **Burstein–Moss band filling** |
| n = 6.23×10¹⁸ → 3.05×10¹⁹ cm⁻³ | **4.7 → 4.68 eV (감소)** | **Mott 반도체-금속 전이**(이론상 4×10¹⁸ cm⁻³) + 불순물 분포에 의한 정전 퍼텐셜 요동 band narrowing |
| n > 7.23×10¹⁹ cm⁻³ | **다시 증가** | Burstein–Moss 가 renormalization 을 재차 압도 |

> 🔑🔑🔑 **같은 물질의 gap 이 도핑 농도에 따라 올랐다 → 내렸다 → 다시 오른다.**
> **단일 `gap_lit_eV` 스칼라는 도핑된 실물질에서 성립하지 않는다.**
> 우리가 전자절연 축을 **"게이트가 아니라 진단"** 으로 둔 판단
> (`cascade_screening_funnel.json` → `electronic_insulation_diagnostic`)이 문헌으로 지지된다.
> SnO₂·In₂O₃ 도 Burstein–Moss shift 를 보인다(SnO₂ 는 0.02 eV 규모).

### 6-d. 물성 요약 (Tables XI, XII)

| 물성 | 값 |
|---|---|
| 밀도 | 5.88-5.95 g/cm³ |
| **bulk modulus** | 계산 **174**, 실험 **184-255 GPa** |
| Vickers 경도 | **656.5-1029.6 kg/mm² (방향 의존)** |
| 융점 | 1725 / 1740±15 / 1795 / 1806 °C |
| Debye 온도 | 실험 738 K, 계산 872 K |
| 비열 | 0.47-0.56 J/(gK) |
| **열전도도** | **a\* 15 · b 28 · c\* 18 W/(mK)**; [100] 10.9-13.6, [010] 22.8, [001] 14.7, [-201] 13.3, [110] 27.0 |
| 열확산도 | a\* 5.23 · b 9.76 · c\* 6.26 mm²/s |
| CTE | [100] 4.7-5.3, [010] 5.45-8.9, [001] 5.35-8.2 ×10⁻⁶/K |
| **electron affinity** | **4.00±0.05 eV** (실험) |
| 절연파괴장 | **8.0 MV/cm** (예측) — 리뷰 전체 예측의 **기준점** |
| 전자 유효질량 | m*_a 0.288, m*_b 0.283, m*_c 0.286 (실험) — **거의 등방** |
| 정공 유효질량 | m*_a 1.769, m*_c 0.409 (계산) — 강한 이방성 |
| mobility | 계산 220-300, 실험 112-176 cm²/(V s) |
| ε₀ | ε_a 10.9/10.19, ε_b 11.2/10.6, ε_c 12.6/12.4 |
| ε_∞ | ε_a 3.89, ε_b 3.87, ε_c* 2.9 (실험); 3.85/3.81/4.08 (계산) |
| IR 활성 | 4A_u, 8B_u |
| Raman 활성 | 10A_g, 5B_g |

> 🔑 **bulk modulus 가 174-255 GPa 로 65 GPa 넘게 갈린다.** 리뷰의 진단:
> *"The variation in values stems from using different theoretical equations of state, overall
> experimental method, and the crystal quality of the sample."*
> 그리고 명시: ***"Since bulk modulus is the change in volume vs applied pressure it is not a
> vector/tensor quantity and therefore cannot be anisotropic."***
> → 우리 EOS B₀ 논의에서 **"EOS 종류가 B₀ 를 바꾼다"** 는 것의 외부 확인.
>
> 🔑 **열전도도는 b축이 최대, a*/[100] 이 최소로 약 2배 이방성.** 리뷰는 Ga₂O₃ 의 낮은 열전도도를
> 소자 패키징의 핵심 난제로 지목한다(§II H).
>
> 🔑 **전자 유효질량이 단사정임에도 거의 등방(0.283-0.288)** — 대칭성이 낮다고 모든 물성이
> 이방적인 건 아니다. 실측 mobility 이방성은 **내재적 성질이 아니라 twin boundary 등 확장결함** 탓
> (Kang et al., HSE 계산은 방향 간 30% 미만 차이).

### 6-e. ★ 도핑·결함 (p.20-21) — 우리 도판트 논의와 가장 가까운 절

**n-type 은 자유자재, p-type 은 불가.** 이 비대칭이 Ga₂O₃ 절의 핵심이다.

- **치환형 shallow donor 로 1×10¹³ ~ 1×10²⁰ cm⁻³** 제어 가능 (상한은 Sn 도핑 박막).
- **자리 선호가 이온반경으로 설명된다** (p.20):
  | 도너 | 자리 | Ga 대비 원자반경 차 |
  |---|---|---|
  | Si | **사면체 Ga(I)** | **−40%** |
  | Ge | 사면체 Ga(I) | **−16%** |
  | Sn | **팔면체 Ga(II)** | **+14%** |
  | Cl, F | **3배위 O(I)** | — |
  > 🔑🔑 리뷰 원문: *"**germanium and tin offer good spatial fits for the gallium cationic site**."*
  > **"이온반경 mismatch → 자리 선호"를 숫자로 못박은 문장.**
  > 우리 47-dopant cascade 의 site-preference 판정(`champion_site_all_x`)에 인용할 수 있는 외부 근거.
- **산소공공은 도너지만 준위가 너무 깊어 전도에 기여하지 못한다**(Varley 66).
  → 언도프 n-type 은 **성장 중 유입된 불순물(주로 Si)** 탓.
  실증: SiO₂+Ga₂O₃ 혼합 feed rod float-zone 으로 Si 농도 10¹⁶-10¹⁸ cm⁻³ 제어,
  Si 증가에 따라 전도도가 **최대 50 Ω⁻¹cm⁻¹** 까지 계속 상승 (120).
- **Ga vacancy = 산소 dangling bond 3개 = triple acceptor** → 도너 보상, 자유전자 감소(178).
- 어닐: **O₂ → 자유전자 감소 / N₂·H₂ → n-type 전도 증가** (24,179).
- **p-type 불가**: 정공이 산소 자리 주변에 강하게 국재화 → 전기장을 걸어도 drift 불가 → **정공 mobility ≈ 0** (181,182).
- **★ co-doping 우회로 2가지** (p.20-21):
  1. **metal–nitrogen co-doping** (183, Yan): Mg 또는 Zn 을 **도너**, N 을 **acceptor** 로 **동시 도핑**하면
     N 의 준위가 각각 **0.16 / 0.01 eV** 로 크게 낮아진다(DFT). 게다가 **전자결핍 금속 co-doping 은
     보상 vacancy 결함 생성도 억제**한다.
  2. **Bi alloying** (184, Cai): (Bi_xGa_{1-x})₂O₃ 희박합금이 **중간 valence band** 를 만들어 acceptor 에너지를 낮춤.
  > 🔑🔑 **donor + acceptor 동시 투입으로 준위를 끌어내린다** = 우리 co-doping cascade 와 같은 문법
  > (우리 [ke2025] MgClO, [liu2023] MgF₂, [li2025] CuBr₂ 의 "이원 도핑" 서사와 개념적 평행선).
- **deep acceptor 의 반전**: Fe 도핑 → deep acceptor 이지만 결정은 여전히 약한 n-type;
  **Fe acceptor 준위 = 전도대 기준 860 meV** (186). Peelaers(185) 제1원리:
  β-Ga₂O₃ 도판트는 **VBM 위 1.3 eV 이상의 deep acceptor** 가 되는 일이 잦다.
  > 🔑 리뷰의 반전: ***"deep acceptors are beneficial for creating highly insulating layers within devices."***
  > **"전도를 못 만드는 결함이 절연층을 만드는 데는 유익하다"** — 우리 전자절연 축의 소자 언어판.
- 부수: 도핑이 **LO-phonon plasmon coupled mode** 의 주파수·편광방향을 이동시킨다(140).
  Sn/Fe 도핑 → 포논산란 증가 → **열전도도 감소**(14,187).
  Seebeck 계수 **−341 μV/K** @RT (계산) — 전자 유효질량이 커서 DOS 가 높은 탓(189).
  지배적 O-H 센터 = Ga(1) vacancy-2H, [V_Ga(1)]-2D center (188).

---

## 7. ZnO · SnO₂ · NiO · CuO (우리 29·30·46·47위)

### 7-a. ZnO (§V, pp. 50-59)

**구조**: wurtzite **P6₃mc (#186)**, a 3.2459-3.2501 / c 5.2069-5.2075 Å.
**c/a = 1.595-1.604 vs 이상값 1.633** — ZnO 의 이온성과 격자 안정성 탓에 약간 작다.
격자상수 편차 원인: 산소공공·Zn antisite·threading dislocation. 그리고
**자유전하가 전도대 minimum 의 deformation potential 을 통해 격자를 팽창시킨다**(p.51).
준안정: zinc blende **F-43m (#216)** a 4.463-4.619 Å · rocksalt **Fm-3m (#225)** a 4.271-4.30 Å.

**bandgap = Direct.** 이방성이 작다(대개 <100 meV):

| | E_g(ε⊥) | E_g(ε∥) | E_xb(⊥) | E_xb(∥) | 방법 |
|---|---|---|---|---|---|
| 벌크 평균 | **3.409** | **3.447** | 50-90 meV | 50-90 meV | SE/Trans |
| 박막 | 3.08-3.37 (이방성 미고려) | | 60 meV | | SE/Abs |
| 계산 | 2.97(sX) · 3.03(PBE0) · 3.20(GW) · 3.4(LDA+GW) · **3.6(LDA+U+GW)** · 3.77(SIC-PP) | | | | |

- **exciton 결합에너지 50-90 meV** = GaN 의 약 3배 → RT 에서도 exciton 발광이 뚜렷.
- 우리 `gap_lit_eV` 3.3 은 박막/이방성 미고려 범위(3.08-3.37)의 중앙. 벌크 단결정이면 3.41-3.45.
  → **실질 차이 없음, 라벨만 필요.**
- ⚠ **리뷰 내부 불일치**: 본문은 Yoshikawa(588)를 "3.54 eV" 로, Table XXVI 는 "3.45/3.45" 로 적는다. 표를 쓸 것.

**다형 gap 이 방법에 따라 5 eV 넘게 갈린다** (Table XXVIII):

| 상 | 계산 | 실험 |
|---|---|---|
| zinc blende | **LDA 0.79** · LDA+GW 1.00 · 1.36 · LDA-PP 1.77 · **SIC-PP 3.27** | **3.27** (PL) |
| rocksalt | LDA 1.16(indir)/2.54/3.08 · LDA+GW 3.72 · GW 4.51(indir)/4.74 · **HF 5.54(indir)/6.54** | 2.45(indir, avg abs edge) / 4.5 |

> 🔑 **zinc blende ZnO: LDA 0.79 eV vs 실험 3.27 eV = 4배 과소.** SIC-PP 만 맞춘다.
> **rocksalt 는 HF 가 6.54 로 과대**, LDA 는 1.16 으로 과소 — **같은 상에서 5 eV 넘게 갈린다.**
> 우리 "PBE gap 은 과소, 절대값 인용 금지" 규율의 교과서적 사례.
>
> 🔑 **rocksalt 가 indirect 인 이유가 대칭성으로 설명된다**: rocksalt(점군 O_h)는 반전중심이 있어
> 음이온 p 와 양이온 d 상태가 **섞이지 못한다** → valence band 가 분산되며 VBM 이 Γ에서 벗어남.
> zinc blende(T_d)는 반전중심이 없어 혼합이 일어나 direct 유지.
> **압축 시 Zn(3d) 밴드가 분열하고 상부 가전자대가 넓어지며 gap 이 커진다.**

**기타 물성**: 밀도 5.605 g/cm³ · bulk modulus 계산 154.4-173 / 실험 140-183 GPa
(**rocksalt 는 203-228 GPa 로 훨씬 단단**) · 융점 1975 °C · Debye 온도 **305-700 K(9종 중 산포 최대)** ·
비열 0.495-0.504 J/(gK) · 열전도도 **46-147 W/(mK)** (Zn face 102-116, O face 98-110;
**시료 간 최대 101 W/(mK) 차이 = 9종 중 산포 최대**) · CTE a축 4.31-4.75, c축 2.49-4.9 ×10⁻⁶/K ·
electron affinity 4.1/4.5 eV · 절연파괴장 2-3 MV/cm(예측) · m_e* 0.23-0.34, m_h* 0.79 ·
mobility 계산 260-300, 실험 120-440 cm²/(V s) ·
ε₀ ⊥c 7.46-7.77 / ∥c 8.50-8.91 (**9종 중 정적 유전상수 최저**) · ε_∞ 3.61-3.78 ·
IR 활성 A₁,E₁ / Raman 활성 A₁,E₁,2E₂.

**압전**: P(ZnO) = −0.032 / −0.05 / −0.057 C/m²(계산), **−0.07±0.015 C/m²**(SHG 실험),
−0.041 ~ −0.004 C/m²(ZnO/BaTiO₃ 다이오드 커패시턴스).
**압전전하는 c축 평행 변형에서 발생하고 인장/압축에 따라 부호가 바뀐다.**

**도핑/결함**:
- **shallow donor: Ga, Al, In, 그리고 Sc** — 모두 Zn²⁺ 치환(647,648).
  > 🔑 **리뷰가 Sc 를 ZnO 의 shallow donor 로 명시.** Sc₂O₃ 절 바깥에서 Sc 화학이 나오는 유일한 자리.
- 그 외 shallow donor: Zn interstitial, H interstitial, Zn 자리의 P.
- acceptor: Li·Na(Zn 자리) / N·P·As(O 자리). **p-type 은 여전히 어렵다** — O 2p VBM 탓.
- **H 가 ZnO 에서는 amphoteric 이 아니라 shallow donor** (Van de Walle 650) → 의도치 않은 n-type 의 원인.
  hydrothermal/MOCVD/VPT 대부분에 H 존재; H₂O 잔류가스에서도 유입.
- 결함 이동도 순서(DFT): **Zn interstitial > O interstitial > Zn vacancy > O vacancy**.
  n-type ZnO 의 자기확산은 **vacancy 매개**(654).

### 7-b. SnO₂ (§VI, pp. 59-66)

**구조**: rutile **P4₂/mnm (#136)**, a 4.673-4.776 / c 3.149-3.212 Å.
고압 다형 6종: CaCl₂(Pnnm) · α-PbO₂(Pbcn) · pyrite(Pa-3) · ZrO₂(Pbca) · fluorite(Fm-3m) · cotunnite(Pnma).

**다형 gap** (계산, Gracia 686): CaCl₂ 3.58 · α-PbO₂ **3.80(최대)** · pyrite 3.55 · ZrO₂ 3.44 ·
fluorite 3.01 · **cotunnite 2.84(최소, 유일한 indirect)** vs rutile 3.50 eV.
→ **α-PbO₂ 쪽으로 갈수록 gap 증가, cotunnite 쪽으로 갈수록 감소.**
전도대 = Sn s,p / 상부 가전자대 = Sn p + O p.

**bandgap = Direct.** 우리 `gap_lit_eV` 3.6 은 **리뷰가 §XI 에서 직접 계산한 벌크 실험 평균 3.614 eV** 와
사실상 동일 → **8종 중 가장 정확히 일치하는 항목.**

**⚠ 그런데 SnO₂ gap 은 두 계열이 공존한다** (Table XXXII):

| 계열 | 값 | 근거 |
|---|---|---|
| **전통 계열** | 3.37-4.00 eV (bulk), 3.64-4.38 (film) | photoconductivity, absorption edge, two-photon |
| **Feneberg SE 계열** | **E⊥c 4.35(excitonic onset)/4.52(fundamental)**, **E∥c 5.59/5.67** | SE + exciton 보정 (726) |

- exciton 결합에너지: E⊥c **0.17 eV**, E∥c **0.08 eV**.
- 흡수 onset: E⊥c 4.28, E∥c 5.42 eV → **강한 광학 이방성**.
- Feneberg 는 진짜 fundamental gap 이 **dipole-forbidden 3.59 eV** 에 있다고 본다.
  ε₂ 모델 피팅으로는 3.77(⊥c) / 3.41(∥c) eV.
> 🔑 **리뷰 자신이 "왜 그렇게 큰지 설명이 없다"고 적는다** (*"there is no explanation given for the large
> bandgap in the reported bandgap energies"*). **E∥c 와 E⊥c 의 fundamental gap 이 1 eV 이상 차이**난다.

**온도**: 벌크 **−6.0×10⁻⁴ eV/K** (8-415 K), 0 K 외삽 3.7 eV; 박막 **−2.0×10⁻⁴ ± 4×10⁻⁵ eV/K**.
**Burstein–Moss shift 로 캐리어 증가 시 gap 증가(0.02 eV 규모)**, 동시에 electron-electron·
electron-impurity 산란에 의한 narrowing 도 존재.

**포논** (Table XXXIII): `Γ = A_1g + A_2g + B_1g + B_2g + E_g + 2A_2u + 2B_1u + 4E_u`.
Raman: A_1g **638**, B_2g **782**, B_1g 100(calc), A_2g 398(calc), E_g **476** cm⁻¹.
IR TO/LO: A_2u 477/705, E_u1 244/276, E_u2 293/366, E_u3 618/710 cm⁻¹.

**기타**: 밀도 6.975-7.02 g/cm³ · bulk modulus 계산 221-245(rutile 221-228) / 실험 205
(**나노결정 270 GPa**) · 융점 **>1900(계산)/>2100 °C(실험)** — ⚠ **분해 때문에 미확정**(9종 중 유일한 특수 사례) ·
Debye 570/550 K · 비열 0.398/0.366 J/(gK) ·
열전도도 51.4, **⊥c 55.0 / ∥c 98.0 W/(mK)** (c축 평행이 2배) ·
열확산도 **1.45-1.7 mm²/s (9종 중 평균 최저)** ·
electron affinity 4.3-4.85 eV · 절연파괴장 3.5 MV/cm(예측) ·
m_e* 0.12-0.30(등방성이 저농도에서 크고 고농도에서 이방성 증가 = **비포물선 전도대**) ·
m_h* 1.21(Γ-X)/1.47(Γ-Z) · mobility 실험 35-260 cm²/(V s)
(**최고품질 결정 RT 260, 77 K 에서 8800**) · ε₀ ⊥c 14±2 / ∥c 9±0.5 · ε_∞ 3.70/3.90.

**도핑**: n-type 도판트 Pd, Sb, Pt, In(저농도에선 grain size 불변, Pt 만 Fermi level 미이동).
그 외 Co, Zn, CuO, Ni, Nb, Ta.
> 🔑 **Pb 도핑으로 gap 3.17 → 3.67 eV 조절**(Ganose 769, DFT). 메커니즘이 중요하다:
> ***"The bandgap modulation happens through the lowering of the conduction band maximum from the
> vacuum level. This lowering increases the electron affinity, which enables changing the work function
> and achieving improved alignment of the work function to cathodes and formation of Ohmic contacts."***
> → **도핑으로 gap 이 아니라 "밴드 엣지의 절대 위치"를 옮긴다.** 우리 밴드정렬 언어와 동형.

**p-type 실패**: Ga 도핑 시도 → Seebeck 은 p-type 을 가리키나 저항이 매우 높고 결정이 제대로 형성되지 않았다(758).
**내재 결함**: DFT — **비화학량론 결함이 화학량론 결함보다 형성이 쉽다** → SnO₂ 의 비화학량론성.
n-type 은 산소공공 탓(770).

### 7-c. NiO (§VIII, pp. 73-78) — ★ 우리에게 red flag 가 있다

**구조**: **distorted rhombohedral R-3m (#166)**, a 2.95 Å (안정상).
준안정 cubic rocksalt **Fm-3m (#225)**, a 4.08-4.26 Å.
Néel 온도 아래에서 약한 rhombohedral 왜곡 → **원래 금지된 1차 Raman 모드가 활성화**된다.

**bandgap = Indirect.** 계산 2.54-4.8 / 벌크 실험 3.60-4.30 / 박막 실험 3.25-4.5 eV.
우리 `gap_lit_eV` 4.0 은 벌크 실험 범위 중앙 → **범위 안**.
§XI: **9종 중 두 번째로 큰 실험 gap**(1위 Al₂O₃).
> ⚠ 그러나 산포가 2 eV 넘는다 — **상관전자계(Mott/charge-transfer)라 방법 의존이 극심**하다.

**★★ 우리 전자절연 축에 걸리는 red flag** (p.78):
> 리뷰 원문: *"Pure stoichiometric crystals of NiO make excellent insulators and contain a high room
> temperature resistivity of around 10¹³ Ohm cm."*
> *"**Lithium is a very common dopant of NiO** and acts as a substitute for the nickel ions. The p-type
> conductivity occurs in undoped samples as well as in lithium doped samples. **Often the lithium doped
> samples will exhibit higher conductivity values.**"*
> Li 는 격자 안에서 **Li⁺** 로 존재(Li 의 2차 이온화 퍼텐셜 > Ni 의 3차 이온화 퍼텐셜).
> Li⁺ 마다 전하중성을 위해 **Ni³⁺(= Ni²⁺ + 정공)** 가 생겨야 하고, 흔히 O²⁻ vacancy 가 대신 보상한다.
> **Li⁺ 는 acceptor** 다.

> 🔑🔑 **우리 문맥으로 번역하면**: Li-rich 계에 NiO 를 넣으면 **Li_xNi₁₋ₓO 형 p-type 전자(정공) 전도체**가
> 생길 수 있다. 리뷰는 전고체전지를 한 마디도 말하지 않지만, 이 문장은 **우리 전자절연 축에 직접 걸린다.**
> 우리 cascade 에서 NiO 가 46위인 것은 산화안정·역학 때문이었는데, 이 리뷰는 **독립적인 탈락 사유**를 준다.
> (⚠ 단, 이건 리뷰의 서술을 우리 문맥으로 **옮긴 해석**이지 리뷰의 주장이 아니다.)

**다른 도판트**: Cu(gap 3.73 → **3.69 eV**), O(산소공공 형성 억제), Fe(OER 과전압 감소),
**Co(gap 3.44 → 3.26 eV; Co 양이 cation vacancy 를 제어해 optical gap 을 바꾼다)**.
n-type 도 가능 — 산소공공 또는 금속 불순물이 결함을 지배할 때(925).

**mobility 가 리뷰 9종 중 최악**:
- 전자 실험 **0.14-3.3**, 계산 0.64 cm²/(V s) · 정공 계산 0.43-0.53, 실험 0.3-2.8 cm²/(V s).
- **정공 drift mobility(0.3)가 전자(0.14)의 2배.**
- 원인(Goodenough 919): **전자 밴드가 대부분 양이온 오비탈로 구성** → 양이온 vacancy 와 국재 스핀이 산란.
- 기판온도 200 → 500 °C 에서 정공 mobility 0.3 → 3.5 (결정성 개선).
- 정공 농도/mobility 쌍: (1.16e18, 0.86) · (6.0e18, 0.1) · (5.0e19, 0.7).
- **전자 유효질량은 "Not Applicable"** (p-type 이라). 정공만: 0.8-1.0 m_h(계산);
  Γ-Γ 0.86(상·하 VB 모두), Γ-K 0.55(상 VB)/1.66(하 VB).

**기타**: 밀도 6.8/6.8279 g/cm³ · bulk modulus 실험 199-205 / 계산 137.3 GPa ·
융점 실험 1955-1983 °C (**계산 3127 °C — 1100 °C 이상 차이**) ·
Debye 495-595 K (⚠ **저온 비열 Debye 와 고온 탄성 Debye 가 불일치**, White 906 명시) ·
비열 0.5903/0.5807 J/(gK) · 열전도도 20.2-50 W/(mK) (**45 K 에서 401 피크**;
나노결정립은 ~20 = 입계 포논산란) · 열확산도 **8.8 mm²/s (9종 중 평균 최고)** ·
CTE **12.28 ×10⁻⁶/K @305 K** (105-813 K 에서 11.23 → 14.93) ·
electron affinity 1.4(계산)/1.46-1.47 eV(실험) · 절연파괴장 2-5 MV/cm(예측) ·
ε₀ 11.75-12 · ε_∞ 5.4/5.7 (⚠ IR 모델은 4.93-4.97 — **모델 의존**).

**포논**: cubic rocksalt 에서 1차 TO/LO 는 **Raman 비활성**. Néel 온도 아래 rhombohedral 왜곡에서만 활성.
TO 350-410, LO 520-580 cm⁻¹(약함). 2차 Raman: 2TO 738, 2LO 1142, TO+LO 913 cm⁻¹.
IR ellipsometry: TO 393, TA+TO 548, LO 549 cm⁻¹.
> 🔑 **반강자성 결합·자기 단위셀 배가는 zone-center 포논에 영향을 주지 않는다**(912).

### 7-d. CuO / Cu₂O / Cu₄O₃ (§IX, pp. 78-86) — ⚠ 로스터 불일치

> ⚠⚠ **리뷰의 주역은 CuO(cupric oxide)이고 우리 로스터는 Cu₂O(cuprous oxide)다.**
> Table XLVIII 캡션: *"All values listed for CuO unless otherwise noted."*
> → **Cu₂O 의 bandgap 수치는 리뷰에 없다.** 우리 `gap_lit_eV` 2.1 은 이 리뷰로 **검증도 반박도 안 된다.**

**3상**:

| 상 | 구조 | 공간군 | 격자 (Å) | gap type |
|---|---|---|---|---|
| **CuO** (tenorite) | monoclinic | **C2/c (#15)** | a 4.5130-4.6837, b 3.3544-3.6121, c 5.0354-5.1408, β 97.06-99.54° | **indirect** |
| **Cu₂O** (cuprite) | cubic | **Pn-3m (#224)** | a **4.1656-4.27** | **direct** |
| Cu₄O₃ (paramelaconite) | tetragonal | I4₁/amd (#141) | a 5.6544-5.8392, c 9.7728-9.8966 | indirect |

- CuO: primitive cell 에 CuO 2단위, unit cell 에 4단위. O 4개 = 4e 자리, Cu 4개 = 4c 자리.
  **Cu-O 정사각 평면 배위**. **Néel 온도 ~230 K, 그 아래 반강자성**.
- Cu₂O: unit cell 6 atoms (Cu 4 + O 2), Cu 가 면심 위치.

**CuO bandgap**: 계산 **0.9-2.74** / 벌크 실험 **1.35-1.7** / 박막 실험 **1.4-2.03 eV**.
→ **리뷰 9종 중 실험 gap 최소.**

**Cu₂O 에서 쓸 수 있는 것** (p.86):
- **전자 유효질량 0.66 m_e, 등방** (Γ-X, Γ-M, Γ-R 세 방향 동일) — Cu₂O 가 cubic 이라 예상되는 결과.
- **정공은 강한 이방성 + 삼중축퇴**: heavy hole 2.83(Γ-X)/0.91(Γ-M)/0.72(Γ-R);
  최상단 VB 는 +3.16[100]/+3.14[110]/+2.74[111] m_h; [100]에서 최하단 VB 는 +0.34 m_h.
- **light hole 은 전자 유효질량의 약 절반** — Γ7⁺(light)와 Γ8⁺(heavy) 결합에 의한 가전자대 분열 탓.
- **정공 mobility 10-100 cm²/(V s)** (성장온도 1070 K → RT 62, 333 K 43);
  다결정이 단결정과 비슷(250 K 미만에서만 단결정 우위); **박막 최고 256 cm²/(V s)**(1021).
- 참고 Cu₄O₃ 정공 Hall mobility **0.04 cm²/(V s)** (van der Pauw, RT).

**CuO 기타**: 밀도 6.545 g/cm³ · bulk modulus 95.58/99.16/114.25 GPa(계산)
— **9종 중 절대값 최소이자 산포도 최소(~19 GPa)** · 융점 **1201 °C (9종 중 최저)** ·
Debye 640/575 K · 비열 0.526 J/(gK) · 열전도도 33/76.5 W/(mK) ·
**CTE 1.6 ×10⁻⁶/K (9종 중 최저)** · electron affinity **1.77 eV (9종 중 실험 최저)** ·
**절연파괴장 0.2-0.5 MV/cm (9종 중 최소)** · ε₀ 12.26-13.0(계산),
ε_DC 9.64/10.59/11.94(단사정 3성분) · ε_∞ 7.29-7.84 ·
IR 활성 3A_u,3B_u / Raman 활성 A_g,2B_g ·
전자 유효질량 0.78(longitudinal)/**3.52(transverse — 9종 중 최대, 다른 값보다 3.0 m_e 가까이 큰 outlier)**/0.16-0.46 ·
정공 1.87 / 0.54-3.01 · **정공 mobility 0.1 cm²/(V s)**.

> 🔑 CuO 의 극저 mobility(0.1) → **hopping 전도** 가설(937). 큰 정공 유효질량 = 강한 포논결합 및/또는
> 좁은 3d 가전자대. 리뷰: *"CuO shares some properties with another p-type oxide, NiO. Both materials
> have very low mobility owing to the **narrow valence 3d band** for both materials."*
> → **후기 3d TM 산화물(NiO, CuO)의 공통 병증**. 우리 cascade 에서 이 둘이 46·47위로 바닥인 것과 정합.

**CuO 도핑/결함**:
- **acceptor: Li, Na (Group IA)** → p-type 전도 증가. **여기서도 Li 가 등장한다.**
- donor: Al/Ga/In(IIIA), **Ti/Hf/Zr(IVB)**. **Zr·Hf 는 shallow donor 로 예측되어 n-type CuO 가능.**
  IVB 는 O-poor 조건에서 고용도 최대; Ti 가 형성에너지 최저. gap 안에 0/+1/+2 세 전하상태.
  단 형성에너지가 높아 **캐리어 농도를 오히려 낮출 수 있다.**
- 내재결함(Zivkovic 1025): **Cu-rich → V_O + Cu_i 지배**(형성에너지 ~1.0 eV; V_O 는 **deep donor** 로
  n-type CuO 의 낮은 mobility 원인 가능; Cu_i 는 중성). **O-rich → V_Cu, O_Cu, O_i 지배**
  (O_i 가 최저 형성에너지 acceptor; **V_Cu = shallow acceptor, O_Cu = deep acceptor**).
  이들이 보상되지 않아 CuO 의 p-type 성이 나온다.
- > 🔑 **두 성장조건 사이 에너지 차가 매우 커서, 성장분위기만으로 언도프 CuO 의 전도형을 결정할 수 있다.**

### 7-e. CdO (§VII, pp. 66-73) — 우리 로스터 밖, 최소만

rocksalt **Fm-3m (#225)**, a ~4.6-4.7 Å. gap type **direct**(단 더 작은 indirect gap 존재).
bandgap 계산 0.8-1.2 / 벌크 실험 1.11-2.28 / 박막 1.2-2.4 eV.
§XI 에서 CdO 가 차지하는 극단들: **밀도 최고(8.0-8.218) · Debye 온도 최저 · 열전도도 최저(8.1 W/(mK)) ·
CTE 평균 최고 · 정적 유전상수 최고 · electron affinity 최고(5.94 eV) · 실험 mobility 최고 ·
정공 유효질량이 전자보다 작은 유일한 예외.**
> 리뷰: **저전도도 + 고CTE 조합이라 열적 영향이 9종 중 가장 클 수 있다.**

---

## 8. ★ 합금/고용체 — 우리 co-doping 관심사와 직결 (§II G, §V G, §X F)

리뷰는 "고용체에서 물성이 어떻게 연속 변하는가"에 **4가지 서로 다른 대답**을 준다.
이게 이 리뷰가 우리에게 주는 **두 번째로 큰 값어치**다(첫째는 Sc₂O₃ 데이터).

### 8-a. 대답 ① — bowing 식으로 매끄럽게 (AlGaO 의 ε_∞)

α-(Al_xGa₁₋ₓ)₂O₃ 박막의 고주파 유전상수 (Hilfiker 228, Fig 14, Eq 5):

```
ε_∞,j[x] = (1−x)·ε_∞,j[0] + x·ε_∞,j[1] − b_j·x·(1−x)
```
**bowing parameter: b_⊥ = 0.386, b_∥ = 0.307.**
x = 0 → 1 에서 ε_∞ 가 **약 25% 감소**하고, ordinary/extraordinary 차이도 줄어든다.

> 🔑🔑 **고용체 물성을 "선형 + bowing 항" 으로 쓰는 표준 함수형.**
> **bowing = 0 이면 단순 가법성, ≠ 0 이면 상호작용.**
> 우리 co-doping 시너지(`cascade_v23_synergy_pairs.csv`)를 **정량 판정**하는 데 그대로 쓸 수 있다.

### 8-b. 대답 ② — Vegard 선형 (InGaO 의 격자, AlGaO 의 격자)

β-(In_xGa₁₋ₓ)₂O₃ (Kranert 240, Vegard):
`a = 12.295 + 1.43x` · `b = 3.035 + 0.35x` · `c = 5.795 + 0.39x` (Å)
In 증가 시 1-2% 팽창. 임계점 넘으면 고압 InGaO₃ 상 검출.

β-(Al_xGa₁₋ₓ)₂O₃ (Kranert 231): `a = 12.21 − 0.42x` · `b = 3.04 − 0.13x`
(⚠ c 파라미터는 인쇄가 "2.81 − 0.17x" 로 보이는데 β-Ga₂O₃ c = 5.80 Å 와 안 맞아 **판독 불가로 남김**).

**밴드도 선형**: β-(In_xGa₁₋ₓ)₂O₃ 는 In 18.75% 까지 **indirect·direct gap 모두 선형 감소**하고,
**VBM/CBM 의 BZ 내 위치는 바뀌지 않는다**(CBM Γ, VBM Γ-Y 방향 off-Γ). 3.125% In 에서 4.769 eV.
검출 파장 256 → 280 nm 확장. **In > 20% 에서 상분리 위험.**

> 🔑 **같은 모물질(Ga₂O₃)에서도 어떤 물성은 선형(격자·gap), 어떤 물성은 bowing 필요(ε_∞).**
> 물성마다 조성 의존 함수형이 다르다.

### 8-c. 대답 ③ — ★★ 구조전이에서 불연속으로 점프 (MgZnO)

**이 리뷰에서 우리 co-doping 에 가장 중요한 한 절이다.**

Mg_xZn₁₋ₓO (§V G, p.58):
- **wurtzite 영역** (x < 0.53): E₀^A **3.369 → 4.101 eV** (x = 0 → 0.29).
  exciton 결합에너지는 **bowing** — 61 → **50(x=0.17 최소)** → 58 meV.
  ZnO/Mg_xZn₁₋ₓO 이종구조 밴드 오프셋 최대 1 eV.
  **E₁·E₂ 고에너지 전이는 Mg 분율에 무의존, E₀ 만 강하게 의존**
  → **Mg 합금화는 주로 Γ점 전도대·가전자대만 바꾼다**(662).
- **x = 0.53 에서 hexagonal wurtzite → cubic rocksalt 구조 전이.**
- **rocksalt 영역**: E₀ x=0.70 에서 ~6.0 → x=1 에서 **7.674 eV**.
  exciton 결합 ~60 → **85.3 meV**.
- **★ 두 영역 사이에 bandgap 파라미터 E₀ 의 ~1 eV 불연속.**
  원인: **wurtzite(4배위) 와 rocksalt(6배위)의 Zn/Mg 배위수 차이**(590,663).

> 🔑🔑🔑 **한 구조 안에서는 매끄럽게(bowing 포함) 변하지만, 구조전이 조성을 넘는 순간 ~1 eV 로 점프한다.**
> → **우리 cascade 의 x sweep(0.02/0.05/0.10)이 구조를 유지하는지부터 확인해야 한다.**
> 우리는 이미 `dV_anneal_pct` 로 부피 변화를 추적하지만, **"상이 바뀌었는가"는 별개 질문**이다.

**포논도 조성으로 변한다** (Table XXIX, x = 0.10-0.52):
x 증가 시 **A₁(TO) 주파수 증가**, multiphonon 구조와 E₂^S 모드는 증가하지 않음.
그리고 **x = 0.23, 0.37, 0.52 에서 원래 없던 mixed mode(MM, 517→527 cm⁻¹)가 새로 나타난다.**
> 🔑 **고용 조성이 늘면 새 진동모드가 생긴다** — 우리 phonon/ICOHP 에서 "새 피크 = 새 국소환경" 을
> 읽는 방식과 같다.

**CdZnO 는 반대 방향**: Cd 증가로 gap **3.26 → 2.31 eV**(673) 또는 **3.3 → 1.8 eV**(674).
**거의 2 eV 튜닝** → 파장가변 LED. 부작용: grain size 증가.

### 8-d. 대답 ④ — 모상 구조가 다르면 애초에 제한된다

**AlGaO 상평형** (Hill/Roy/Osborn, Fig 11):
- **고온에서 β 상 Al 고용도 70%까지.**
- **저온으로 quench 하면 AlGaO₃ line compound 가 석출 → 저온 고용도 <10%.**
- DFT: Al 71%까지 monoclinic β 선호, 그 이상은 α.
- Al³⁺ 의 Ga₂O₃ 내 고용 상한 보고는 78%(226).
- α 상은 **m-plane sapphire 위 에피성장으로 전 조성 범위 상안정화** 가능 → gap **5.4 → 8.6 eV**,
  nitride 합금(AlGaN)보다 우수한 UWBG 재료(199).

> 🔑🔑 **"고온에서 섞인다"와 "상온에서 섞여 있다"는 다르다.**
> **우리 도핑 cascade 의 0 K 형성에너지가 실제 합성 가능성을 보장하지 않는다**는 문헌 사례.

**4원 합금의 경고** (Liu & Tan 246, GGA-PBE, β-(Al_xIn_yGa₁₋ₓ₋ᵧ)₂O₃):
- Al x, In y 각각 0-18.75% 에서 **indirect gap 5.171 → 4.432 eV**.
  유효질량은 등방이며 **In 증가 시 감소, Al 증가 시 증가**.
- **저자들의 경고**: wurtzite 4원 (Al,Ga,In)N 과 평행한 거동을 가정하지 말 것 —
  **열역학적 안정 이원상의 구조가 서로 다르기 때문**
  (Al₂O₃ rhombohedral corundum / In₂O₃ cubic bixbyite / Ga₂O₃ monoclinic).
> 🔑 **모물질 결정구조가 서로 다르면 "조성으로 매끄럽게 잇는다"는 가정 자체가 위험하다.**
> 우리 co-doping 페어를 논할 때 인용할 경고.

**계산 비용 자백** (p.28):
> β-Ga₂O₃ 는 1×2×2 supercell 에 **Ga 32 + O 48 atoms**. 여기서 Ga 하나를 Al/In 으로 치환.
> 자리가 여러 종이라 원자배열(ordering) 종류가 많고 더 큰 supercell 이 필요.
> 균일 무작위 양이온 분포 vs 양이온 클러스터링 효과도 조사 대상.
> ***"As of date of writing, no such investigations have been reported for β-(AlGaIn)₂O₃."***
>
> 🔑🔑 **우리 disorder ensemble / SQS 문제와 정확히 같은 진술이다.**
> "다원 합금 밴드구조는 supercell 이 커서 아직 안 됐다"는 2022년 리뷰의 자백.

### 8-e. ZnGa₂O₄ — 대칭성을 올려 공정성을 얻는 설계

**cubic spinel Fd-3m (#227), a = 8.3342 Å.** Zn²⁺ 사면체, Ga³⁺ 팔면체.
gap: 확산반사 ~5 eV(**ZnO 보다 크다 — 둘 다 Zn²⁺ 인데도**) · CL 5.25 eV(이론 5.2) ·
흡수계수 direct **4.570** / indirect **4.325** · SE+DFT **5.27(3) eV**.
ε_DC 10.5±0.06(LST) / 11.3±0.7(RF 커패시턴스), ε_∞ 3.78±0.02 —
**ε_DC/ε_∞ 비가 β-Ga₂O₃ 와 유사** → 포논산란 한계 mobility 도 비슷할 것으로 추정.
유효질량: 전자 0.24 m_e, 최상단 VB 정공도 0.24 m_e, **등방**. Wannier–Mott exciton Rydberg 14.8 meV.
Hall mobility 벌크 107 cm²/(V s); MOCVD 박막 5.6(30 sccm) → 1.4(60 sccm, 격자왜곡).
포논: primitive cell 14 atoms → 42 modes,
`Γ_opt = A_1g + 2A_2u + 2E_u + E_g + 4T_1u + 2T_2u + T_1g + 3T_2g`.

**Table X — ZnGa₂O₄ vs β-Ga₂O₃ 정면 비교** (Galazka 254):

| | ZnGa₂O₄ | β-Ga₂O₃ |
|---|---|---|
| 성장법 / 상태 | VGF, CZ / 개발 초기 | CZ / 성숙 |
| 최대 부피 | 8 cm³ | 160 cm³ |
| 융점 | 1900 °C | 1800 °C |
| **대칭** | **Cubic** | **Monoclinic** |
| **연마·절단** | **쉬움** | **어려움** |
| 벽개면 | 없음 | {100}, {001} |
| gap | 4.570 dir / 4.325 ind | 4.56∥[001] / 4.59∥[100] / 4.85∥[010] |
| UID n | 3e18-9e19 cm⁻³ | 5e16-2e18 cm⁻³ |
| UID μ | 40-100 cm²/(V s) | 100-150 |
| 최대 캐리어 | 1e20 (UID) | 1e19 (Si/Sn 도핑) |
| RT 열전도도 | **22.1 W/(mK)** | (방향별 — 판독 실패, Table XI 사용) |

> 🔑 **입방 스피넬로 바꾸면 이방성이 사라지고(연마·절단 쉬움, 벽개 없음) 유전상수는 유지된다.**
> "대칭성을 올려 공정성을 얻는" 설계 사례.
> 성장조건이 절연/n-type 을 결정하고, **700 °C 이상 산소 어닐 수 시간이면 절연체로 전환**된다.

### 8-f. ITO — 도핑이 캐리어를 늘리며 mobility 를 깎는다

리뷰는 ITO 를 별도 주제로 넘기고 In₂O₃ 절에서 비교만 한다.
캐리어 5×10²⁰ cm⁻³ @1 wt% Sn. **그러나 mobility 는 UID In₂O₃(160-170)보다 낮다.**
Sn 일부는 **전기적으로 비활성**. ITO 박막 열전도도는 bulk In₂O₃ 의 1/3, CTE 10.2(유리와 유사).
보상 acceptor 는 In vacancy 가 아니라 **침입형 산소**.
> 🔑 **"농도를 올리면 좋다"가 아니라 n × μ 곱의 최적점이 존재한다.**
> 우리 Nd σ-drop(D₀ 0.65×, Ea 불변 = prefactor 지배) 서사와 **어휘가 통한다** (물리는 다르다).

---

## 9. Appendix A — 물성 정의 (리뷰가 직접 정의한 것)

리뷰 §Appendix A (p.100-101)는 각 물성을 정의한다. 우리가 라벨링할 때 그대로 쓸 수 있다.
가장 중요한 두 개:

> **Fundamental bandgap** — *"Often referred to as the lowest direct band-to-band transition. The
> fundamental bandgap usually requires a variety of methods and techniques to be measured in order to
> determine since **the excitonic contributions alter the results**."*
>
> **Optical bandgap** — *"Photons of a selected frequency are used to help excite electrons from the
> valence band to the conduction band. **The energy of the exciton determines the onset of the transition**
> between vertical intrabands."*

그 외:
- **Bandgap**: VBM 과 CBM 의 차이. 같은 k 면 direct(운동량 이동 불필요), 다른 k 면 indirect.
- **Bulk modulus**: 균일 압축에 대한 저항. GPa.
- **Debye temperature**: 결정에서 **가장 높은 정규 진동 모드가 일어나는 온도**. K.
- **Effective mass**: 준입자의 관성질량. **텐서이며 운동량·에너지·밴드 지수에 의존하고,
  개별 텐서 성분은 실수이며 양수일 수도 음수일 수도 있다.**
- **Electrical breakdown field**: 전하가 흐르기 전까지 물질이 견디는 최대 전기장 = **peak electric field**. MV/cm.
- **Electron affinity**: 전자를 CBM 에서 진공준위로 올리는 데 필요한 에너지(또는 그 역과정에서 방출되는 에너지). eV.
- **High frequency dielectric constant**: **포논 모드 밴드보다 훨씬 위, 밴드간 흡수 onset 보다 훨씬 아래**
  주파수에서 측정 — 두 분산(포논 흡수, 밴드간 전이)을 모두 무시할 수 있는 영역.
  **대부분의 산화물에서 near-IR(0.2-1 eV) 영역.**
- **Static dielectric constant**: 저주파 또는 정전기장 조건에서의 유전상수.
- **Mobility**: 주어진 전기장에서 전하운반체의 포화속도 척도. 불순물·포논 산란으로 결정.

> 🔑 **ε_∞ 의 정의가 우리 ε∞ 체인([kraft2017] digest §7)에 그대로 쓸 수 있다** —
> "포논 위, 밴드간 흡수 아래" 라는 창(window)의 정의가 명확하다.

---

## 10. ★ 비판 / 한계 — 리뷰가 자기 데이터로 자기를 반박하는 지점

이 리뷰의 진짜 값어치는 표가 아니라, **표들 사이의 불일치**다. 우리가 인용할 때 반드시 함께 갈 것.

### 10-1. "gap 이 크면 전자적으로 안전하다"는 두 번 반박된다

| 반박 | 내용 | 출처 |
|---|---|---|
| **①** | *"Al₂O₃ has a bandgap of almost double β-Ga₂O₃, **but that value does not correlate to a superior electrical breakdown field**."* Al₂O₃ 실험 5.2-8 vs Ga₂O₃ 예측 8 MV/cm | p.38 |
| **②** | Sc₂O₃: gap 기반 예측 **11 MV/cm** vs 실측 **3.5 MV/cm** = *"a stark difference"* | p.91 |
| **③(보강)** | α-Al₂O₃ 는 vacancy state 를 통한 **Poole–Frenkel hopping** 으로 *"can be considered a **semiconducting oxide** at times"* | p.39 |
| **④(보강)** | NiO: gap 3.6-4.3 eV 인데 **Li 도핑으로 p-type 전도체**가 된다 | p.78 |

> **→ 우리 `electronic_insulation_diagnostic` 의 "게이트가 아니라 진단" 판단은 옳았다.
> 다만 이유를 하나 더 추가해야 한다: 큰 gap 이 절연을 보장하지 않는다(결함 준위·도핑).**

### 10-2. bandgap 은 물질상수가 아니다 — 4가지 이유

1. **정의 의존**: In₂O₃ fundamental 2.93 vs optical 3.55 eV (dipole-forbidden 탓).
   SnO₂ 3.6 vs 4.52/5.67(exciton 보정). Ga₂O₃ absorption 4.5 vs SE 5.1-5.7.
2. **시료 의존**: Al₂O₃ bulk 8.8-9.9 vs 비정질 박막 6.2-6.8 eV.
3. **방향 의존**: β-Ga₂O₃ b > a > c 로 0.5 eV 이상. SnO₂ E∥c − E⊥c > 1 eV.
4. **★ 캐리어 농도 의존**: β-Ga₂O₃ 가 4.69 → 4.716 → 4.68 → 다시 증가(비단조).
   SnO₂·In₂O₃ 도 Burstein–Moss.

> **→ 우리 `gap_lit_eV` 에 `definition`(fundamental/optical/absorption/SE)과
> `sample`(bulk single crystal/film/amorphous) 두 필드를 추가하지 않으면 값이 의미를 못 갖는다.**

### 10-3. 리뷰 자체의 약점

1. **자체 실험·계산이 0.** 전부 재인용(secondary). 원논문 대조 없이 인용하면 우리 규율 위반.
2. **요약표가 종종 이론과 실험을 한 range 로 섞는다.** 예: Sc₂O₃ Table L 의 `a = 9.708-9.90 Å`
   (9.708/9.90 은 이론, 실험은 9.810-9.8459).
3. **리뷰 내부 불일치가 있다.** ZnO Yoshikawa gap: 본문 3.54 vs Table XXVI 3.45.
   Al₂O₃ bulk modulus: Table LI 는 239 를 calc·225.9 를 expt 로, Table XVII 는 225-252 를 전부 calc 로.
4. **절연파괴장의 대부분이 실측이 아니라 "gap 으로부터의 예측"**(Higashiwaki plot, Ref 147).
   실측이 있는 것은 Al₂O₃(5.2-8), Sc₂O₃(3.5) 둘뿐이고 **둘 다 예측보다 훨씬 낮다.**
5. **C_ij 전탄성텐서가 9종 어디에도 없다.** bulk modulus 만 있고, Young/Poisson 은 Sc₂O₃ 뿐.
   → **우리 UMA/QE 탄성 계산이 이 공백을 채울 수 있다.**
6. **9종 전부에 대해 "누가 어떤 방법으로" 가 표에 압축돼 있어, 방법 세부(functional, k-mesh, 시료 순도)를
   추적하려면 매번 원논문으로 가야 한다.**

### 10-4. 우리 문맥으로 옮길 때의 위험 (재확인)

1. **전기화학이 없다.** ESW·산화 onset·Li 수송·계면 반응성 — 전부 부재. 우리 축을 대체 못 한다.
2. **"코팅"이라는 단어의 의미가 다르다.** 리뷰의 코팅은 **반사방지/게이트 유전체**다.
   우리의 코팅은 **전기화학 계면 보호막**이다. Sc₂O₃ 가 "좋은 코팅"이라는 문장을 옮겨오면 안 된다.
3. **벌크 vs 도핑 호스트.** Sc₂O₃ E 214-228 GPa 는 **순수 벌크**, 우리 `E_VRH` 18.7 GPa 는
   **Sc₂O₃ 를 x=0.02 넣은 LPSCl 호스트**. 나란히 놓으면 오독이다.
4. **CuO ≠ Cu₂O.** 우리 로스터는 Cu₂O 인데 리뷰 수치는 CuO 다. gap type 조차 다르다(direct vs indirect).
5. **다형·시료·측정법이 값을 지배한다.** 리뷰가 이걸 100쪽으로 증명한다.
   우리 db 에 이식할 땐 **반드시 라벨과 함께.**

---

## 11. 인용 가능 문장 (deck/manuscript 용)

- "Sc₂O₃ 는 리뷰된 9개 산화물 중 **융점이 가장 높고**(2753-2823 K), **보고된 물성이 가장 적은**
  물질이다 — 열물성(Debye 온도·열전도도·열확산도·CTE)과 유전상수·유효질량·mobility 가
  문헌에 사실상 존재하지 않는다[Spencer 2022]."
- "Sc₂O₃ 의 VBM 은 O 2p, CBM 은 **빈 Sc 3d** 이며(Sc³⁺ = 3d⁰), Sc–O 결합은 이온성에 일부 공유성이
  섞여 있다[Spencer 2022]."
- "Sc₂O₃ 의 Young's modulus 는 실험 **214.3-227.6 GPa**, Poisson ratio 0.30, bulk modulus는
  Materials Project 계산 **168 GPa** 이며 **실험 bulk modulus 는 문헌에 없다**[Spencer 2022]."
- "**gap 이 크다고 절연내압이 크지 않다** — Al₂O₃ 는 β-Ga₂O₃ 의 거의 두 배 bandgap 을 갖지만
  절연파괴장은 더 우수하지 않고[Spencer 2022 p.38], Sc₂O₃ 는 gap 기반 예측 11 MV/cm 대비
  실측이 3.5 MV/cm 에 그친다[동, p.91]."
- "β-Ga₂O₃ 의 bandgap 은 캐리어 농도에 따라 **4.69 → 4.716 → 4.68 eV 로 비단조 변화**한다
  (Burstein–Moss → Mott 전이 → 재확대)[Spencer 2022] — 단일 bandgap 값을 물질상수로 쓰는 것의 한계."
- "고용체의 물성은 한 구조 안에서는 bowing 을 포함해 매끄럽게 변하지만,
  **구조전이 조성을 넘으면 불연속으로 점프한다** — Mg_xZn₁₋ₓO 는 x = 0.53 의 wurtzite→rocksalt
  전이에서 bandgap 이 ~1 eV 도약한다[Spencer 2022]."
- "합금 물성의 조성 의존은 **ε(x) = (1−x)ε[0] + xε[1] − b·x(1−x)** 형태의 bowing 파라미터로 기술된다
  (α-(Al_xGa₁₋ₓ)₂O₃ 의 ε_∞ 에서 b_⊥ = 0.386, b_∥ = 0.307)[Spencer 2022]."
- "β-Ga₂O₃ 에서 도너의 자리 선호는 이온반경 정합으로 설명된다 — Si 는 Ga 대비 −40%, Ge −16%,
  Sn +14% 이며, **Ge 와 Sn 이 Ga 양이온 자리에 공간적으로 잘 맞는다**[Spencer 2022]."
- "β-Ga₂O₃ 의 p-type 화는 단일 치환으로는 불가능하고, **금속-질소 공도핑**(Mg 또는 Zn + N)이
  acceptor 준위를 0.16 / 0.01 eV 로 끌어내리는 것이 유망한 우회로로 제시된다[Spencer 2022]."
- "NiO 는 순수 화학량론에서 10¹³ Ω·cm 의 우수한 절연체이나, **Li 이 NiO 의 가장 흔한 도판트로
  Ni 자리를 치환해 p-type 전도도를 높인다**[Spencer 2022]."
- "In₂O₃ 는 VBM→CBM 광학전이가 dipole 금지라 **fundamental gap(실험 2.93 eV)과
  optical gap(3.55 eV)이 구조적으로 갈린다**[Spencer 2022]."

---

## 12. 우리 작업 항목 (json `action_items_for_us` 와 동기)

| id | 항목 | 우선 |
|---|---|---|
| **A1** | **Sc₂O₃ 순수 벌크를 UMA/QE 로 계산** → 리뷰의 E 214.3-227.6 GPa(exp) / B 168 GPa · ν 0.30(MP) 와 직접 벤치마크. 도핑 호스트 값과 무관한 **깨끗한 대조**가 가능한 드문 기회. | **high** |
| **A2** | **Ref 1078 (Zhu et al., Sc₂O₃–Ga₂O₃ alloy 구조·전자물성 DFT, 밴드 오프셋 조절) 원논문 확보** — Sc 밴드정렬의 1차 출처 | **high** |
| **A3** | Ref 1064 (Gogotsi, Sc₂O₃ 세라믹: brittleness, modulus of rupture, bending strength, ultimate strain) 확보 — 리뷰가 범위 밖이라 생략한 역학 데이터 | medium |
| **A4** | **우리 `gap_lit_eV` 에 `definition`(fundamental/optical/absorption/SE) + `sample`(bulk/film/amorphous) 필드 추가.** 리뷰가 보여준 대로 이 두 라벨 없이는 값이 의미를 못 갖는다 | **high** |
| **A5** | NiO 를 논할 때 "Li 가 NiO 의 표준 도판트이며 p-type 정공전도를 만든다"(p.78)를 **전자절연 축의 독립 탈락 사유**로 기록 | medium |
| **A6** | co-doping 서사에 **MgZnO x=0.53 구조전이 gap 1 eV 불연속** + **AlGaO ε_∞ bowing 식** 두 개 인용. 전자 = 연속성 가정의 붕괴, 후자 = 연속 변화의 표준 함수형 | **high** |
| **A7** | **Cu₂O 의 우리 `gap_lit_eV` 2.1 출처 확인** — 이 리뷰로는 검증 불가(리뷰는 CuO 만 수치화) | medium |

---

## 13. 판독 불가로 남긴 것 (12건) — 추정·보간 하지 않음

전체 목록은 json `unreadable_or_uncertain` 참조. 요약:

1. SnO₂ Table XXXV bulk expt gap 하한 (인쇄 "3.3.7-4.00")
2. Kranert AlGaO 의 c 파라미터 (인쇄 "2.81 − 0.17x", β-Ga₂O₃ c=5.80 Å 와 불일치)
3. Table X 의 β-Ga₂O₃ 방향별 RT 열전도도 (값과 참고문헌 위첨자 구분 불가)
4. Table LII(열물성 비교)의 CTE·비열 일부 칸 (9열 회전 조판)
5. Table XLI(NiO 포논) Lowndes 모델 ω/γ 열
6. Sc₂O₃ 절의 LLP 인광체 화학식 (인쇄 "Sr₂ScAcO₅", 중간 원소 확정 불가)
7. Sc₂O₃ 박막 vs 벌크 밀도 귀속 (리뷰 문장 자체가 모순)
8. Ga₂O₃ CTE 계산값의 세 번째 방향 라벨 ([100] 이 두 번)
9. SnO₂ 고농도 캐리어의 m*_⊥ (인쇄 "4.0 m_e", 0.40 의 오식 가능성)
10. ZnO Yoshikawa gap (본문 3.54 vs 표 3.45 = **리뷰 내부 불일치**)
11. ZnO bandgap 온도계수 γ (§V C 2 pp.54-55 끝까지 미판독)
12. Sc₂O₃ 절이 인용한 인접 TM 산화물 gap (TiO₂/V₂O₅/CrO₃ — 1960년대 trend 재인용이라 **소환의 소환**,
    우리 db 값과 비교 금지)

---

## 14. 연결

- **`db/properties/oxide_literature_properties_spencer2022.json`** — 8종 물성 추출표 (본 digest 의 정량 짝)
- `db/properties/cascade_v23_themes.json` — 우리 `gap_lit_eV` 원본 (§10-2 라벨링 대상)
- `db/properties/cascade_screening_funnel.json` → `electronic_insulation_diagnostic` — §10-1 이 지지하는 판단
- `db/properties/doping_cascade_verified.json` — 우리 E_VRH/B0 (⚠ **도핑 호스트**, 리뷰의 순수 벌크와 대상 다름)
- `litdb/papers/kim2026_hts_li3sc2po43_coating_midni_ncm.md` — Sc 수렴(§10-6); 이 리뷰가 **Sc₂O₃ 쪽 물성 배경**을 채운다
- `litdb/papers/kraft2017_lattice_polarizability_argyrodite_Li6PS5X.md` — ε_∞/분극성 체인; Appendix A 의 ε_∞ 정의가 유용
- `litdb/papers/sundar2025_oxide_coating_screening_lpscl.md` — LPSCl 위 산화물 ALD 코팅 스크리닝
  (Al₂O₃·ZnO·MgO·ZrO₂ 등장; **이 리뷰가 그 산화물들의 벌크 물성 배경**)
- `litdb/papers/he2019_dft_for_battery_materials_review.md` — PBE gap 과소평가 규율 (§5-b, §7-a 가 극단 사례 제공)

---

## 15. 🔬 본문 실물 독립 검증 (2026-08-03) — **네이티브 텍스트 PDF** 재판독

> **왜 다시 봤나**: 초판 digest(2026-07-28)는 **스캔 이미지 PDF 5분할**을 눈으로 읽어 만들었고, §13에 **판독 불가 12건**을 남겼다.
> 2026-08-03 `litdb/inbox/46. …pdf` 로 **같은 논문의 네이티브(텍스트 레이어 보유) PDF** 가 들어왔다.
> pypdf 전문 추출(800,623자) + PyMuPDF **단어 좌표 단위** 재구성으로 **본문 100 pp + Table I–LV + Fig 1–38 캡션 전수** 재판독.
> **결과: §13의 12건 중 11건 해소, 신규 오류 9건 적발, 신규 관찰 4건, 초판 자체 교정 1건.**
> (⚠ 이 절은 *텍스트 레이어* 판독이다. 랜드스케이프 조판 표는 좌표로 열 위치를 확인했으나, 대외 인용 전에는 렌더링된 페이지로 한 번 더 확인 권장.)

### 15-a. §13 판독 불가 12건 → **11건 해소**

| §13 # | 항목 | 판정 |
|---|---|---|
| **6** | LLP 인광체 화학식 (인쇄 "Sr₂ScAcO₅", 초판 추정 "Al") | **✅ 해소 + 초판 추정 기각.** 본문 p.93 인쇄는 **`Sr2ScCaO5`**. 그런데 **참고문헌 1080 = G. Li, W. Chen, Y. Wang, B. Duhan, "Electronic structure, photoluminescence and phosphorescence properties in **Sr₂ScGaO₅:Sm³⁺**," *Dyes Pigments* **157**, 259–266 (2018)** → **정답은 Sr₂ScGaO₅, 본문의 "Ca"가 Ga 오식**. 바로 뒤 Chernov 계열이 **Sr₂GaScO₅**(Brownmillerite)인 것과도 정합. 초판의 "Al 추정"은 틀렸다 |
| **2** | AlGaO 격자 c 파라미터 (인쇄 "2.81 − 0.17x") | **✅ 해소.** 네이티브 텍스트도 **`c = (2.81 – 0.17x) Å`** 그대로 → **스캔 아티팩트가 아니라 논문 인쇄 그대로**. β-Ga₂O₃ c=5.80 Å 및 같은 문장의 a=(12.21−0.42x)·b=(3.04−0.13x)와 안 맞으므로 **논문 오타(5.81→2.81)로 확정**. 인용 시 c 절편은 쓰지 말 것 |
| **1** | SnO₂ Table XXXV bulk expt gap 하한 (인쇄 "3.3.7-4.00") | **✅ 해소.** 네이티브도 `3.3.7–4.00` → **인쇄 오타 확정**. 올바른 값은 **3.37**(Table XXXII의 Nagasawa 광전도 3.37 eV) |
| **3** | Table X β-Ga₂O₃ 방향별 RT 열전도도 | **✅ 해소.** ZnGa₂O₄ **22.1** W/mK vs β-Ga₂O₃ **[100] 11 / [010] 29 / [001] 21** W/mK |
| **4** | Table LII CTE·비열 칸 (9열 회전 조판) | **✅ 전수 해소** → §15-c 교차표에 전사 |
| **5** | Table XLI NiO 포논 Lowndes 모델 열 | **✅ 해소.** One Lorentz ε∞ 4.96 / ω(TO) 390.5 / A 6.26 / γ 28.8 / MSE 4.78 · Two Lorentz 4.96 / 393.9 / 5.86 / 17.6 (+565 / 0.081 / 81) / MSE 3.81 · One Lowndes 4.93 / 391.1 / 18.2 / 585.9 / 35.1 / MSE 4.28 · Two Lowndes 4.97 / 392.9 / 17.2 / 593.9 / 42 (+548 / 55 / 542 / 38) / MSE 3.55. ⚠ **표 헤더가 `x(TO) c(TO)`를 두 번 반복** — 뒤쪽은 LO여야 함(인쇄 오류) |
| **7** | Sc₂O₃ 박막 vs 벌크 밀도 귀속 | **✅ 해소 = 논문 문장 자체가 모순 확정.** 원문: *"the density of thin film samples was slightly **higher** than bulk, **3.9 and 4.1** g/cm³, respectively"* — 값의 순서(film 3.9, bulk 4.1)와 "film이 더 높다"는 서술이 **정반대**. 인용 금지 |
| **8** | Ga₂O₃ CTE 계산값 세 번째 방향 라벨 | **✅ 해소 = 논문 오타 확정.** Table XI·LII 모두 `1.54 [100] / 3.37 [010] / **3.15 [100]**` — **[100]이 두 번**. 세 번째는 [001]이어야 함 |
| **9** | SnO₂ 고농도 캐리어 m*_⊥ (인쇄 "4.0 mₑ") | **✅ 해소(인쇄 확인).** 본문: *"at a carrier concentration of around 2×10²⁰ cm⁻³ values were about **4.0 mₑ for m*⊥** and **0.26 mₑ for m*∥**"* → 인쇄는 4.0이 맞다. 0.40 오식 가능성은 여전히 열려 있으나 **논문이 그렇게 썼다**(비포물선성 강조 맥락) |
| **10** | ZnO Yoshikawa gap 본문 3.54 vs 표 3.45 | **✅ 해소 = 리뷰 내부 불일치 확정.** 본문: *"Yoshikawa et al. carried out SE experiments to account for anisotropy but ultimately found the same bandgap energy (**3.54 eV**) for both directions"* / Table XXVI 해당 행: **`3.45 3.45 59 59 SE 588`**. 같은 Ref 588에서 두 값 |
| **11** | ZnO bandgap 온도계수 γ | **✅ 해소.** **Varshni 식 Eq.(6)** `Eg(T)=Eg(0)−αT²/(T+β)`, 자유엑시톤 결합에너지가 4.8–300 K에서 거의 온도 무관이므로 **E_XA 로 Eg 대체(Eq. 7)**; **T > 200 K 에서 dE_XA/dT = γ = −0.35 meV/K** |
| 12 | TiO₂/V₂O₅/CrO₃ 소환의 소환 | ❌ 미해소(판독 문제가 아니라 **출처 계보 문제**). 1960년대 trend 재인용 — 우리 db 값과 비교 금지 규율 유지 |

### 15-b. 🆕 신규 적발 (9건) — 초판이 놓친 논문 오류·불일치

| # | 위치 | 문제 | 우리 영향 |
|---|---|---|---|
| **N1 🔴최중대** | **Table LIV, In₂O₃ 밴드갭 칸** | **In₂O₃ 열의 밴드갭 값이 SnO₂ 열로 통째 복제됐다.** 값(calc 1.70/2.76/2.86/2.89/3.50/3.65/3.7; bulk expt 3.37/3.54/3.56/4.0; 3.57 ⊥c / 3.93 ∥c; film 3.7/3.71/3.64–3.94/4.38; 4.35·4.52 ⊥c / 5.59·5.67 ∥c)과 **참고문헌 번호(735, 687, 717, 686, 715, 718, 723, 719, 727, 720, 724, 722, 721, 725, 711, 709, 726)가 SnO₂ 열과 글자 단위로 동일**. PyMuPDF 좌표로 열 위치 확인(In₂O₃ 열 y≈471–513, SnO₂ 열 y≈282–330; **같은 표의 다른 물성 행 — 밀도·B·ε₀ 9.0/9.05/8.9·ε∞ 3.82–4.128 — 은 정상적으로 In₂O₃ 값**). **In₂O₃ 자신의 갭(Table XIX: bulk expt 2.72–3.55, 막 간접 2.62·직접 3.71–3.75, LDA 1.11 → HSE03+G₀W₀ 3.10)은 Table LIV에 아예 없다.** | **`gap_lit_eV` In₂O₃ 값을 Table LIV에서 뽑았다면 SnO₂ 값이다.** 반드시 **Table XIX**로 재확인. json `oxide_literature_properties_spencer2022.json` 의 In₂O₃ gap 출처 필드 점검 필요 |
| **N2** | Table LI vs Table XLII (NiO 안정상) | Table LI = **Fm3̄m (#225)**, Table XLII = **"안정상 = 왜곡 능면체 R3̄m(#166) a=2.95 Å, *준안정* = 입방 Fm3̄m"** — 정반대 귀속. 본문은 "왜곡각 4.2 arc-min로 무시 가능"이라 실용상 입방 취급 | NiO 구조를 인용할 땐 "실온에서 미세 능면체 왜곡, 실용상 입방"으로 서술 |
| **N3** | 본문 §IX A + Fig 32 캡션 (CuO 공간군) | **"C2/c (#12)"** 로 인쇄 — C2/c는 **#15**, #12는 C2/m. Tables XLIII·XLVIII·LI 는 **#15**로 올바름. 초판 digest는 표만 봐서 #15로 정확했으나, **본문/그림 캡션 쪽 오기를 기록해 둘 것** | — |
| **N4 🔑** | **Table VII vs XII vs LIV (β-Ga₂O₃ ε∞)** | **같은 출처(Ref. 44 = Schubert 2016)에서 세 가지 다른 값 세트**: <br>· Table VII: `SE 3.7(5) / 3.7(1) / 3.2(1)` (ε∞,a / ε∞,b / ε∞,c*) <br>· Table XII: `3.89 εa / 3.87 εb / 2.9 εc*` — **Expt.44** <br>· Table LIV: `3.8 εxx / 2.9 εyy / 3.8 εzz` — **Calc.44** <br>세 표가 값도 축라벨도 expt/calc 라벨도 다르다 | **🔑 우리 ε∞ 체인 직접 영향** — β-Ga₂O₃ ε∞ 를 이 리뷰에서 인용하면 안 되고 **Schubert, APL 2016(Ref 44) 원문**에서 가져와야 한다. [kraft2017] digest의 ε∞ 규율에 이 사례를 캐비앳으로 추가 |
| **N5** | Table XVII (Al₂O₃ 요약표) | 실험 XPS·에너지손실 박막값(Refs 307/321/322 — Table XIV에선 전부 **Expt**)을 **"Film calc."** 로 오분류; 반대로 계산 Ref 324(HSE03)를 **"Bulk expt. 8.8–9.9"** 목록에도 포함 | 물질별 요약표(XI–L)의 expt/calc 라벨을 신뢰하지 말 것 — **항상 물성별 원표(XIV 등)로 갈 것** |
| **N6** | Table XLIII 표제 / §IX A 본문 | 표제가 **"Cu₃O₄"**(→Cu₄O₃), 본문에 **"Cu₄O43"** 오타 | — |
| **N7** | §XI 본문 | *"**Table LI** highlights the anisotropic bandgap energies of β-Ga₂O"* → 실제로는 **Table LV**; 같은 문단에 **"b-Ga₂o₃"** 소문자 오타 | — |
| **N8** | §IV A / Table XVIII (In₂O₃) | **`o′-In₂O₃` 라벨을 Pbcn(#60) 상과 α-Gd₂S₃형 Pnma(#62)/Pn2₁a 상 양쪽에 사용** — 같은 기호가 두 상 | In₂O₃ 고압상 인용 시 공간군 병기 필수 |
| **N9** | (초판 §10-3 #3 자체 교정) | 초판은 *"Table LI 는 239 를 calc·**225.9 를 expt** 로, Table XVII 는 225-252 를 전부 calc 로"* 라고 적었으나, **네이티브 판독 결과 Table LI 도 `257 (20 °C) Expt / 239 Calc / 225.9 Calc / 252 Calc`** — 225.9는 **calc**다. **Table LI 와 XVII 는 실제로 일치**하며, 초판이 지적한 이 불일치는 **스캔 오독**이었다 | §10-3 #3 항목은 **삭제 대상**(대신 N5의 Al₂O₃ 라벨 오류로 대체) |

### 15-c. 🆕 신규 관찰 (초판에 없던 정량·방법)

**O1. CuO 의 GGA+U — "갭은 자유 파라미터의 단조함수"의 가장 노골적 사례 (Table XLIV)**

| U (eV) | 5 | 7 | 9 |
|---|---|---|---|
| CuO gap (eV) | **0.91** | **1.48** | **2.11** |

같은 코드·같은 구조에서 U만 5→9로 올리면 갭이 **2.3배**. 리뷰 원문: *"As U is increased there is an improvement in the electronic structure description used for the calculations, resulting in a theoretical value that is more comparable to experimental values."* — 즉 **실험값에 맞을 때까지 U를 올린다**는 절차를 그대로 기술한다. 같은 물질에서 HSE는 **2.74 eV**(최고 실험값 2.03보다 ~0.7 eV 과대), LDA·LDA+U 없이는 **금속으로 예측**.
> **→ `comparison_vs_ours.md` §D 의 "hybrid mixing 의존이라 gap 절대값 비교 금지"([Sundar] HSE06 mix 0.32 / [Semi] HSE 3.30 줄)에 붙일 최강 각주.** 우리 PBE 2.066/2.099 를 어떤 하이브리드 값과도 나란히 놓지 않는 규율의 외부 근거.

**O2. β-Ga₂O₃ 세 근본전이 — 편광각 + 전이별 결합에너지 (Tables II, III)**

| 전이 | Mock 각도(a축 기준) | Mock 엑시톤피크 / 결합E / Eg | Sturm 각도 | Sturm 피크 / 결합E / Eg |
|---|---|---|---|---|
| Γ1⁻¹ | **115.1°** | 4.92 / **120 meV** / **5.04** | 110° | 4.88 / 270 / 5.15 |
| Γ1⁻² | **25.2°** | 5.17 / **230 meV** / **5.40** | 17° | 5.10 / 270 / 5.37 |
| Γ1⁻⁴ | E∥b | 5.46 / **180 meV** / **5.64** | E∥b | 5.41 / 270 / 5.68 |

두 그룹의 차이는 데이터가 아니라 **모델 선택**이다 — Mock 은 결합에너지를 **이방적·전이별로 자유롭게** 뒀고, Sturm 은 **270 meV 하나로 고정**해 피팅했다. Furthmüller 계산은 s–pₓ / s–p_z 0.4 eV, s–p_y ≈0.1 eV.
> **→ "같은 시료·같은 기법에서도 *피팅 모델의 자유도 배분*이 갭을 0.1 eV 단위로 움직인다"** — 초판 §10-2의 "정의 의존"에 다섯 번째 층(모델 의존)을 추가.

**O3. Table LV 의 SE − Abs 차이를 방향별로 정량화**

| 방향 | SE 평균 | Abs 평균 | **차** |
|---|---|---|---|
| E∥c | 5.095 | 4.50 | **+0.595** |
| E∥a | 5.385 | 4.57 | **+0.815** |
| E∥b | 5.66 | 4.73 | **+0.93** |

> **🔑 우리 CLAUDE.md 규율 — "fixed-occ nscf VBM/CBM 고유값만, DOS-threshold 판독 금지(~0.3 eV 과소)" — 의 동형(isomorphic) 외부 선례.** 물질도 방법도 다르지만 구조가 같다: **동일 시료에서 추출 규칙만 바꿔도 갭이 0.3–0.93 eV 계통 이동한다.** peer-reviewed 100 pp 리뷰가 문헌 전체를 이 논리로 재정렬했다는 점에서, 우리 규율을 설명할 때 인용 1순위.

**O4. PDP(포논 변형퍼텐셜)의 미측정 규모 + 리뷰가 원문헌을 반박한 3건**

- β-Ga₂O₃: 모드당 **변형 4 + 응력 4** 파라미터 → 10Ag+4Aᵤ+5Bg+8Bᵤ = **총 216개**, **실험 결정값 0개**; LO 모드용 추가 48개는 아예 미보고(Korlacki 2020).
- **리뷰가 원논문 오류를 직접 반박한 3건**(리뷰 신뢰도 요소): ①SnO₂ CTE — Hassan의 `3.8×10⁻⁵ K⁻¹`을 "11.7×10⁻⁶보다 작다"고 쓴 데 대해 *"we believe this to be an error by Hassan et al."* ②CdO 열전도도 — CRC의 0.7 W/mK를 "이진 산화물치고 비현실적으로 낮다"며 ab initio 5.6–9.3으로 대체 ③β-Ga₂O₃ IR 모드 — Dohy(1980s)의 등방 모델 배정을 "틀렸다"며 Table V에 *"역사적 기록용, 실제 포논 주파수로 보지 말 것"* 각주.

### 15-d. 교차비교표 전사 (Tables LI–LV) — 텍스트 레이어 판독의 최대 수확

초판은 §2에서 표 목록만 나열했다. 아래는 **9종 × 전 물성**을 텍스트 레이어에서 복원한 것.

**Table LI 기본물성** (밀도 g/cm³ / B GPa / Tm °C)

| | Al₂O₃ | Ga₂O₃ | In₂O₃ | ZnO | CdO | SnO₂ | NiO | CuO | Sc₂O₃ |
|---|---|---|---|---|---|---|---|---|---|
| ρ | 3.92–3.984 | 5.88–5.95 | 7.12–7.2 (6.3 이상치) | 5.605 | 7.0–8.218 ↑ | 6.975–7.02 | 6.8–6.83 | 6.545 | 3.79–4.16 ↓ |
| B | **257(20 °C)** ↑ / 225.9–252 calc | 174 calc / 184–255 expt | 194.24 expt / 174–192.7 calc | 140–183 expt / 154–173 calc | 108–150 expt / 128–164 calc | 205 expt / 221–245 calc (270 나노) | 199–205 expt / 137.3 calc | **95.6–114.3** ↓ | 168 (MP) |
| Tm | 2050–2071.85 | 1725–1806 | 1912–1950 | 1974–1975 | >1500 (1559 승화) | >1900–>2100 (미결정) | 1955–1983 | **1201–1446** ↓ | **2479.85–2549.85** ↑ |

**Table LII 열물성** (Debye K / 비열 J·g⁻¹K⁻¹ / κ W·m⁻¹K⁻¹ / 열확산 mm²s⁻¹ / CTE 10⁻⁶K⁻¹)

| | Al₂O₃ | Ga₂O₃ | In₂O₃ | ZnO | CdO | SnO₂ | NiO | CuO | Sc₂O₃ |
|---|---|---|---|---|---|---|---|---|---|
| θ_D | **965–1045** ↑ | 738 expt / 872 calc | 420 expt / 700–811 calc | 305–>800 (편차 ~500) | **255** ↓ | 550–570 | 495–595 | 575–640 | **미보고** |
| c_p | **0.750–0.785** ↑ | 0.47–0.56 | 0.356 / 0.837 | 0.495–0.504 | **0.339** ↓ | 0.366–0.398 | 0.581–0.590 | 0.526 | 0.683 |
| κ | 30–40 | 10.9 [100]–28 [010] | 10–15.0 | **46–147** ↑ | **5.6–9.3** ↓ | 51.4 / 55 ⊥c / 98 ∥c | 20.2–50 | 33–76.5 | **미보고** |
| α_D | 미보고 | 5.23/9.76/6.26 (a*/b/c*) | 1.2(ITO막)/7.0 calc | 미보고 | 미보고 | 1.45–1.7 ↓ | **8.8** ↑ | 미보고 | 미보고 |
| CTE | 4.5–5.5 | 4.7–8.9 expt / 1.54–3.37 calc | 6.15–10.2 | 4.31–4.75(a)/2.49–2.9(c) | **13.31–14.33** ↑ | 4.0 ∥a / 3.7 ∥c | 12.28 | **1.6** ↓ | **미보고** |

> §XI 총평: **CdO = 열적 최악**(κ 최저 + CTE 최고), **Al₂O₃·NiO·CuO = 최선**, Ga₂O₃ = "middle of the pack". Ga₂O₃ κ 는 GaN(~130)·SiC(~360–490)보다 **한 자릿수 낮다.**

**Table LIII 전기물성** (χ eV / E_br MV·cm⁻¹ / m* mₑ / μ cm²V⁻¹s⁻¹)

| | Al₂O₃ | Ga₂O₃ | In₂O₃ | ZnO | CdO | SnO₂ | NiO | CuO | Sc₂O₃ |
|---|---|---|---|---|---|---|---|---|---|
| χ | 1.58 | 4.00±0.05 | 3.3 calc–4.45 expt | 4.1–4.5 | **5.94** ↑ | 4.3–4.85 | 1.4–1.47 | 1.77 | **0.85 pred** ↓ |
| E_br **pred** | **>20 (~25)** | 8 | 3–4 | 2–3 | 0.5–0.8 | 3.5 | 2–5 | **0.2–0.5** | 11 |
| E_br **exp** | **5.2–7** | 0.46–7.6 | — | — | — | — | — | — | **3.5** |
| m*ₑ | 0.16–0.45 | 0.224–0.41 calc / 0.276–0.311 expt | 0.14–0.55 expt / 0.16–0.22 calc | 0.23–0.34 | 0.09–0.24 | 0.12–0.30 (0.234∥/0.299⊥) | N/A (p형) | 0.78 종 / 3.52 횡 | 미보고 |
| m*ₕ | **6.3 ⊥c / 0.36 ∥c** | 0.409–1.769 | 0.27–0.28 | 0.79 | **0.05** ↓ | 1.21–1.47 | 0.55–1.66 | 0.54–3.01 (평균 1.87) | 미보고 |
| μₑ | **0.8** ↓ | 112–176 expt / 220–300 calc | 7.81–190 expt / 270–274 calc | 120–440 expt / 260–300 calc | **2–609** ↑ (광학 209–1116) | 35–260 | 0.14–3.3 | N/A | 미보고 |
| μₕ | — | — | — | — | — | — | 0.3–2.8 expt / 0.43–0.53 calc | 0.1 expt | — |

**Table LIV 광학/유전** — ⚠ **In₂O₃ 밴드갭 칸은 오류(N1)이므로 Table XIX 값으로 대체 표기**

| | Al₂O₃ | Ga₂O₃ | In₂O₃ ※XIX | ZnO | CdO | SnO₂ | NiO | CuO | Sc₂O₃ |
|---|---|---|---|---|---|---|---|---|---|
| 갭 유형 | 직접 | 직접(실질) | 논쟁 | 직접 | 직접(더 낮은 간접 존재) | 직접 | 간접 | 간접 | 간접 |
| Eg exp | 8.8–9.9 벌크 / 6.2–6.8 막 | 4.48–4.79 흡수 / **5.04–5.68 SE** | 2.72–3.55 벌크; 막 간접 2.62 / 직접 3.71–3.75 | 3.372–3.45 ⊥ / 3.405–3.492 ∥ | 직접 2.07–2.86 / 간접 1.09–1.47 | 3.37–4.00; **SE 4.52 ⊥c / 5.67 ∥c** | 3.60–4.30 벌크 / 3.25–4.5 막 | 1.35–1.7 벌크 / 1.4–2.03 막 | 5.7–5.84 간접 / 6.02–6.1 직접 |
| Eg calc | 6.29–8.0 | LDA 2.19 / PBE 2.356 / B3LYP 4.66 / HSE06 4.83–4.88 / Gau-PBE 4.74–5.35 | LDA 1.11 → LDA+U 2.18 → HSE03 2.44 → **HSE03+G₀W₀/Δ 3.10** | **LDA 0.23** / PBE 0.67 / HSE03 2.11 / SIC-PP 3.77 / **HF 11.07** | 0.61–2.18 | GGA 0.832 / LDA 0.94–1.38 / B3LYP 3.50 / HSE03+G₀W₀ 3.65 | **PBE 1.13** / LSDA+U 3.00 / ACBN0 4.04 / **HF 14.2** | **GGA+U 0.91→2.11 (U 5→9)** / HSE 2.74 | — |
| ε₀ | 9.385 ⊥c / 11.614 ∥c | 10.05–12.7 | 8.9–10.74 | **7.46–8.91** ↓ | **18.1±2.5** ↑ | 14±2 ⊥c / 9±0.5 ∥c | 11.9–12 | 12.26–13.0 calc; 9.64–11.94 expt | **미보고** |
| ε∞ | 3.038–3.077 | 2.9–4.08 ⚠**N4** | 3.82–4.128 | 3.61–3.78 | 5.4 | 3.70 ⊥c / 3.90 ∥c | 5.4–5.7 | **7.29–7.84** ↑ | **미보고** |

### 15-e. 이 검증이 우리 액션에 주는 변화

| id | 내용 | 상태 |
|---|---|---|
| **A8 🆕** | `db/properties/oxide_literature_properties_spencer2022.json` 의 In₂O₃ `gap` 항목이 Table LIV 출처인지 점검(N1 오염 여부) | **✅ 점검 완료 2026-08-03 — 오염 없음.** 해당 json 의 In₂O₃ gap 은 `bulk_expt_eV`·`film_expt_eV`·`calc_eV_bcc`·`calc_eV_rh` 전부 `src: "Table XIX"` 로 **올바른 출처**를 쓴다. Table LIV 를 출처로 삼은 In₂O₃ gap 값 없음 |
| **A9 🆕** | 같은 json 의 **β-Ga₂O₃ ε∞** 항목에 "리뷰 3표 불일치, Schubert 2016 원문 확인 필요" 플래그(N4) — [kraft2017] ε∞ 체인과 직결 | **high** |
| **A10 🆕** | §12 A4(`gap_lit_eV` 에 definition/sample 필드 추가)에 **세 번째 필드 `model_freedom`** 추가 검토 — CuO U-스캔(O1)·β-Ga₂O₃ 결합에너지 고정 여부(O2)가 보여주듯 *피팅 모델 자유도*도 갭을 움직인다 | medium |
| **A2 갱신** | Ref 1078(Zhu, ScGaO DFT) 외에 **Ref 1080 = Li et al., *Dyes Pigments* 157, 259 (2018), Sr₂ScGaO₅:Sm³⁺** 서지 확정(§15-a #6) | — |
| **§10-3 #3 폐기** | Al₂O₃ bulk modulus 표간 불일치 주장은 **스캔 오독**이었다(N9). 대신 **N5(Table XVII 의 expt/calc 라벨 오분류)** 를 그 자리에 | — |

> **검증 총평**: 초판 digest의 **정량 내용은 대체로 정확**했다(Sc₂O₃ 절, Table L 전사, bowing 식, MgZnO 불연속, NiO Li 도핑 red flag 등 핵심 판단 전부 유지). 스캔 판독의 한계는 **① 랜드스케이프 교차표(LI–LV) ② 표 간 라벨 대조** 두 군데에 몰려 있었고, 그 두 군데에서 **논문 자체의 제작 오류 1건(N1)과 표간 불일치 3건(N2·N4·N5)** 이 새로 드러났다. **N1(Table LIV In₂O₃ 갭 = SnO₂ 복제)는 이 리뷰를 데이터소스로 쓰는 누구에게나 영향을 주는 실질 오류다.**

*(검증 2026-08-03 · 네이티브 텍스트 PDF `inbox/46. …pdf` 127 pp / 본문 100 pp 전문 + Table I–LV + Fig 1–38 캡션 전수 · pypdf 800,623자 추출 + PyMuPDF 좌표 재구성 · 사용자 분류 `DFT`)*

