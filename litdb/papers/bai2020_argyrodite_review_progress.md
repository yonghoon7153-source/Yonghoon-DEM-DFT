# Research progress in Li-argyrodite-based solid-state electrolytes — Bai et al. (J. Mater. Chem. A 2020, REVIEW)

> slug `bai2020_argyrodite_review_progress` · DOI `10.1039/d0ta08472g` · type `review (exp+DFT 문헌 메타분석; 자체 신규 계산/실험 없음)` · PDF `054c2fbf-…Research_progress…argyrodite….pdf` (24 pp) · digested `2026-06-26` · status ✅
> **저자**: **Xiangtao Bai**, Yi Duan, Weidong Zhuang, Rong Yang, Jiantao Wang (**China Automotive Battery Research Institute Co., Ltd., Beijing** + **General Research Institute for Nonferrous Metals, Beijing**) · J. Mater. Chem. A **8** (2020) 25663–25686 · Received 29 Aug 2020 / Accepted 17 Nov 2020 · © RSC
> **태그: [외부]** — 한양대(Hanyang) 우리 연구실 아님(중국 자동차배터리연구원/유색금속연구원, Beijing). **kim2021(Rupp AEM, oxide vs sulfide 일반) ≠ 본 리뷰**(argyrodite 전용). 우리 litdb의 **두 번째 리뷰 digest**이자 **유일한 argyrodite-전용 field-map**.

---

## 0. 이 digest를 읽는 법 (리뷰의 thesis + litdb 내 위치)

**이 논문은 우리 litdb의 "argyrodite 전용 지도(field-map)" 논문이다.** kim2021(Rupp)이 *산화물 vs 황화물 SE 전체*를 펼친 광역 지도라면, 본 Bai 2020 리뷰는 **Li-argyrodite Li₆PS₅X(X=Cl/Br/I) 한 패밀리만**을 (1)결정구조 → (2)구조튜닝(치환·도핑) → (3)합성공정 → (4)양극/음극 계면 → (5)대기안정 → (6)셀 통합의 **6개 토픽 축**으로 종설한다. 즉 **우리 모재(comp1=Li₆PS₅Cl, modelc=Li₅.₄PS₄.₄Cl₁.₆)가 정확히 이 리뷰의 한복판에 놓이는** 가장 직접적인 좌표계다.

**리뷰의 핵심 주장(thesis) 3가지**:
1. **Argyrodite Li₆PS₅X는 황화물 SE 중 가장 유망**하다 — σ ~10⁻³–10⁻² S/cm·연성(낮은 Young's modulus로 냉간가압 가능)·전기화학 안정성의 균형. 단 **세 약점**(① 대기/수분 취약 → H₂S 발생, ② 양극 고전압 산화 분해, ③ 합성 공정의 큰 편차)이 상용화를 막는다.
2. **구조 변형(structural modification)이 만능 레버**: aliovalent 치환·도핑으로 **이온전도도와 안정성을 *동시에*** 끌어올릴 수 있다 — 특히 **anion site disorder(S²⁻/X⁻ 4a·4d 자리 섞임)** 가 inter-cage 점프 장벽을 낮춰 superionic을 켜고, **HSAB(연-경 산염기) 기반 양이온 치환(Sn/Sb)·O 공도핑**이 대기안정을 준다.
3. **단일 원소 치환 = 한 측면만; 다중/공도핑 = 종합 개선**: "double or multiple substitutions provide the possibility to achieve overall improvement"(p.25669) — 이것이 리뷰가 미래방향으로 못 박는 핵심 처방이며, **우리 cascade co-doping 서사의 *리뷰 차원 정당화***다.

> 🔗 **litdb 내 위치**: **리뷰·argyrodite-전용·field-map 축**. 이 digest는 다른 모든 argyrodite digest의 "토픽 좌표계"다. 특히:
> - **§2 결정구조 + Fig 1**(48h–24g–48h·intra-cage·inter-cage 3종 점프) → 우리 AIMD inter-cage 율속 서사(Ea·D)의 *교과서 출처*.
> - **§3.1 치환 site/trend + §5 대기안정(HSAB·O-doping)** → 우리 cascade(Nd/Mg/O/F)·comp1→modelc Cl-rich가 리뷰의 *어느 토픽 칸*에 들어가는지.
> - **§4 계면(음극 환원 1.7 V·양극 산화 2.0–2.2 V·passivation interphase)** → 우리 grand-potential ESW(환원 1.24·산화 2.14/2.256 V)의 *문헌 reference 줄*.
> - reference key `[Bai]` 로 `comparison_vs_ours.md`에 등록(리뷰 landscape note + 토픽 매핑).

> ⚠ **연도 주의**: 2020년 리뷰 = **Cl-rich 4축 미정립**(2022 Zuo·GG 이전), **grand-potential 산화창 미언급**(Mo2012 인용은 §4 "theoretical analysis ... up to 7 V"로 *간접*만), **foundation MLIP·constrained-ESW 부재**. 리뷰가 다루는 σ·구조·HSAB는 우리와 정렬되나, **우리 4축(intrinsic onset·기계구속·계면·calendar)·cascade ranking·Nd passivation은 리뷰 *너머***다(= 우리 기여 여지).

---

## 1. 한 줄 요약

Li-argyrodite Li₆PS₅X(X=Cl/Br/I) SE 한 패밀리를 **결정구조·구조튜닝(치환/도핑)·합성·계면(양극+음극)·대기안정·셀통합** 6토픽으로 펼친 24쪽 종설. 결론: **argyrodite는 σ(~10⁻²)·연성·전기화학안정의 균형으로 황화물 중 최유망이나, (1) 수분취약(H₂S), (2) 양극 고전압 산화분해, (3) 합성편차가 병목이고, 이를 *aliovalent 다중치환/공도핑*(Si/Ge로 σ↑·anion disorder↑; Sn/Sb·O로 HSAB 대기안정↑; LiBH₄로 음극호환↑)과 *고상↔용액 공정 최적화*로 동시 공략해야 한다.** 컴파일된 핵심 수치: **σ Li₆PS₅Cl 10⁻³→Cl-rich Li₅.₅PS₄.₅Cl₁.₅ ~10 mS/cm; halide trend σ Br≈Cl≫I(I는 10⁻⁷, ion 반경 過大로 disorder 소멸); E(Young) sulfide 18–37 GPa ≪ oxide 200 GPa; 양극 산화 ~2.0–2.2 V(이론) / 음극 환원 ~1.7 V(Li/SE 계면).**

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자/소속 | **Bai**·Duan·Zhuang·Yang·Wang (China Automotive Battery Research Institute + General Research Inst. for Nonferrous Metals, **Beijing**) |
| 저널/년 | J. Mater. Chem. A **8**, 25663–25686 (2020), **review, 24 pp, 181 refs** |
| DOI | 10.1039/d0ta08472g |
| 대상 | **Li-argyrodite Li₆PS₅X (X=Cl,Br,I) 전용** + 치환계 Li₆₊ₓM(M=Si/Ge/Sn/Sb)·Li₇₋ₓPS₆₋ₓX·oxysulfide·LiBH₄ argyrodite. 비교군으로 oxide(LLZO/LLTO/LATP)·기타 황화물(LGPS·Li₂S–P₂S₅) 표만. |
| 우리 관심 조성 | **Li₆PS₅Cl = comp1** (리뷰 전체의 reference 조성), **Li₅.₅PS₄.₅Cl₁.₅ ≈ modelc(Cl 1.6) 인접** (리뷰의 "Cl-rich σ ~10 mS/cm" 예시) |
| 연구유형 | 종합 리뷰 (실험·DFT 문헌 메타분석; **자체 신규 계산/실험 없음**) |
| 핵심 표 | **Table 1**(SE 기계물성 E/H/K_c — oxide/sulfide/organic), **Table 2**(ASSLB full cell·Li 대칭셀 성능), **Table 3**(고상 vs 용액 공정 비교), **Table 4**(황화물 SE 용액합성 σ), **Table 5**(LCO/NCM/LMO–Li₆PS₅Cl half-cell) |
| 핵심 그림 | **Fig 1**(결정구조+3종 Li 점프), Fig 2(LPSI-20Sn 대기안정), Fig 3·4(Si/Sb 치환 lattice·disorder), **Fig 5**(점프거리 vs annealing T·σ), **Fig 6**(UMA+RTA 합성), Fig 7(용액합성 결정화), Fig 8(NCM111 침투 양극) |

---

## 3. 리뷰의 조직 틀 (6 토픽 축) — 한눈에

리뷰 전체를 관통하는 6개 토픽. 우리 프로그램을 이 칸에 정렬하는 데 쓴다.

| § | 토픽 | 리뷰 핵심 메시지 | 우리 work이 앉는 칸 |
|---|---|---|---|
| **2** | 결정구조 | F-43m 입방; S²⁻(4d) + X⁻(4a) octahedral; PS₄(4b 16e tetra); Li 24g/48h cage; **3종 점프(doublet 48h–24g–48h / intra-cage 48h–48h / inter-cage 48h–48h)**; anion disorder(Cl/Br/I)가 inter-cage 활성화 | comp1/modelc **구조 baseline** + AIMD inter-cage 율속 서사 |
| **3** | 구조튜닝(치환·도핑) | 3 자리(halide 4a / PS₄ / free 4d) 치환; **Cl↑→σ↑(Cl/S 비)**; **Si/Ge로 lattice 팽창·anion disorder↑·σ↑**; Se로 polarizability↑; **단일치환=한 측면, 다중치환=종합** | **comp1→modelc(Cl-rich) + cascade co-doping(Nd/Mg/O/F)** ← 리뷰 핵심 처방의 *실행* |
| **4** | 합성공정 | 고상(>500 ℃·8–50 h·고σ) vs 용액(<300 ℃·scalable·저σ); **UMA+RTA**(one-pot, Li₅.₅PS₄.₅Cl₁.₅ 10.2 mS/cm) | (우리 DFT는 합성 무관 — 단 modelc Cl 1.6 용해한계 주의 = 리뷰 "Cl 용해한도·annealing window") |
| **(4 내)** | 양극/음극 계면 | 음극: Li/SE 환원 ~1.7 V·dendrite·LiI/O-doping passivation; 양극: 고전압 산화 ~2.0–2.6 V·LNO 코팅·실효 ESW는 passivation으로 확장 | 우리 **grand-potential ESW(환원 1.24·산화 2.14/2.256)·interface_reactivity·Nd passivation** |
| **5(=3.2 일부)** | 대기안정 | P⁵⁺ oxophilicity→H₂S; **HSAB: Sn/Sb(soft acid)→S 선호→대기안정**; **O 공도핑→대기안정 (σ 희생 없이)**; Zn/O 공도핑 | 우리 **O-doping/Nd₂O₃ cascade**(대기·계면) ← HSAB·O-doping 직접 정렬 |
| **5(outlook)** | 셀통합·미래방향 | sheet-type(<100 µm)·composite cathode·실패기전·in-situ 특성화 필요; **다중치환/공도핑이 종합개선 열쇠** | 우리 DFT는 atomistic 닻; 셀/공정은 그룹 실험(KimICCF/KimCA/Cha/Kang) |

---

## 4. §2 결정구조 — 상세 (Fig 1)

리뷰의 구조 서술(p.25664)은 우리 comp1/modelc 구조 baseline의 *교과서 출처*다.

- **일반식**: Li₁₂₋ₘ₋ₓ(MᵐY₄)Y₂₋ₓXₓ (M=Si,Ge,Sn,P,As; Y=O,S,Se,Te; X=Cl,Br,I; 0≤x≤2). Li₆PS₅X가 대표.
- **공간군 F-43m(입방)**. 완전 ordered 배열에서:
  - **X⁻(halide) → octahedral void, Wyckoff 4a** (FCC halide 부격자).
  - **PS₄³⁻ → P가 Wyckoff 4b** (P 중심 사면체).
  - **S²⁻ 두 종류**: tetrahedral site **16e**(PS₄의 S) + **Wyckoff 4d = "free S site"**(자유 S²⁻).
  - **Li⁺ → 24g + 48h** (free S²⁻ 주위 cage-like polyhedra).
- **3종 Li 점프**(Fig 1b, 우리 inter-cage 서사의 핵심):
  1. **doublet jump**: 인접 Li 위치 간 **48h–24g–48h**.
  2. **intra-cage jump**: cage 내부 **48h–48h**.
  3. **inter-cage jump**: cage 사이 **48h–48h** ← **율속(rate-limiting)**.
- **HT/LT 상전이**: Li₇PS₆(prototype)는 **~200 ℃**서 cubic-HT↔pseudo-cubic-LT 전이(LT는 저σ). **halide(Cl/Br/I) 치환이 RT서 cubic-HT 상을 안정화** → LiPSX가 RT 고σ.
- **anion site disorder가 σ 지배**(p.25664, **우리 modelc Cl-rich·disorder 서사의 핵심**):
  - **Li₆PS₅Cl·Li₆PS₅Br: Cl⁻/Br⁻ ↔ free S²⁻(4d) 자리 무질서가 큼 → σ 10⁻³–10⁻² S/cm**.
  - **Li₆PS₅I: σ ~10⁻⁷ S/cm (3–4 자릿수 낮음)** — **I⁻ 이온반경(2.20 Å)이 S²⁻(1.84 Å) 대비 過大**해 자리 교환이 안 일어남 → disorder 소멸 → 저σ. (Cl 1.81 Å·Br 1.96 Å은 S²⁻에 가까워 disorder OK.)
  - **site disorder가 inter-cage jump 활성화에너지를 낮춰 superionic을 켠다** → 이것이 리뷰가 명시하는 σ의 *구조적 뿌리*.

🔑 **우리 정렬**: 리뷰의 "**inter-cage jump = 율속 + anion disorder가 그 장벽을 낮춤**"은 우리 AIMD 서사(comp1 Ea 0.253·modelc 0.224 eV; Cl-rich disorder가 D↑·Ea↓)와 **메커니즘이 정확히 같다**. [Rao11](BVSE inter-cage 위계)·[Perc](site-percolation 망)·[Dyre](percolation 병목)가 같은 결론을 각자 방법으로 줌 = 리뷰가 이 합의의 *교과서 진술*.

---

## 5. §2.2 기계적 물성 — Table 1 (우리 elastic·vacancy paradox의 reference 줄)

리뷰는 **"황화물 = 낮은 Young's modulus → 냉간가압·intimate contact → ASSLB에 가장 경쟁력"**(p.25665)을 명시하고 Table 1로 정량.

| 물질군 | 대표 | E (GPa) | 비고 |
|---|---|---|---|
| **Oxide** | LLZO(Li₇La₃Zr₂O₁₂) | **150** | garnet, 취성·고온소결 |
| Oxide | LLTO(Li₀.₃₃La₀.₅₇TiO₃) | **200** | perovskite (최강) |
| Oxide | LATP | 115 | NASICON |
| **Sulfide** | **LPSX (argyrodite)** | **22.1–30.0** | ref 70; **= 우리 comp1 영역** |
| Sulfide | Li₂S–P₂S₅ glass | 18.5 | |
| Sulfide | LGPS | 37.2 | |
| Organic | PEO+LiClO₄ | 0.69×10⁻³ | 최저 |

- 리뷰 명시: **"sulfide … Young's modulus 18–25 GPa (e.g. Li₂S·P₂S₅), shear modulus as high as 6 GPa expected"**(p.25665) — dendrite 억제엔 충분하다고 봄(Monroe-Newman 기준).
- **"moderate modulus가 부피변화 응력 완화에 유리; 너무 높지도 낮지도 않게"**(p.25666) — Li₂S↑→E↑, LiX(LiI)↑→E↓로 조절 가능.

🔑 **우리 정렬·차별화**: 리뷰의 **LPSX E 22.1–30.0 GPa**는 우리 결과(comp1 E_VRH **relaxed-ion 22.06**·EOS B0 26.23; modelc 27.66)와 *같은 줄*. **그러나 리뷰는 relaxed vs clamped-ion 구분도, vacancy paradox도 다루지 않는다** — 우리 clamped(52.31) vs relaxed(22.06) 2.4× 격차, 그리고 [Torii](PBE-D3 relaxed E 27.4)가 우리 relaxed를 외부 확증한 *판정*은 **리뷰 너머**(2020엔 미존재). 즉 리뷰 Table 1은 우리 숫자를 *문헌 줄에 정렬*하는 용도이지, vacancy paradox를 *해결*하진 않는다.

---

## 6. §3 구조튜닝 (치환·도핑) — 가장 두꺼운 토픽

리뷰의 핵심 토픽. **우리 comp1→modelc(Cl-rich)·cascade co-doping이 정확히 여기 들어간다.**

### 6.1 치환 자리 3종 (p.25666)
1. **halide 자리(4a) 치환** — Cl/Br/I 단일 또는 혼합(Cl/Br, Br/I).
2. **PS₄³⁻ 단위 치환** — P→Si/Ge/Sn/Sb/As (aliovalent → Li 함량·lattice 변화).
3. **free S²⁻ 자리(4d) 치환** — S→Se/O.

### 6.2 Cl/S 비 → σ (DFT 예측+실험 확증, **우리 Cl-rich 직접 정렬**)
- **DFT-MD 예측**: "increase in the halogen content and corresponding increase in Li content can significantly enhance Li⁺ conductivity"(ref 1, de Klerk/Wagemaker) → **실험 확증: Cl 계수 1.5서 Li₅.₅PS₄.₅Cl₁.₅ σ = 10 mS/cm**(ref 30).
- **Feng et al.(ref 76)**: Li 결손 + Cl/S(4d) 치환 → **dominant 1S3Cl(4d) 단위** 형성 → Li⁺ 재분포(high mobility). **Ea가 x=0.7(Li₅.₃PS₄.₃Cl₁.₇)서 최저, σ 10 mS/cm.**
- **Yu & co-workers(ref 77)**: Li₇₋ₓPS₆₋ₓClₓ (x=1.1–1.9) → **Li₅.₇PS₄.₇Cl₁.₃이 σ ~6.4 mS/cm 최고**(낮은 합성온도 350 ℃ 장점). **x↑(1.7–1.9)일수록 순상 위해 합성온도↑(500 ℃) 필요** = Cl 용해/결정화 trade-off.
- **Br 계**: 최적 Li₅.₅PS₄.₅Br₁.₅ @350 ℃ σ **4.17 mS/cm**(ref 78).
- ⚠ **리뷰 경고(p.25667)**: "halides usually cause **current collector (Al) corrosion** in high-voltage systems" — Cl-rich의 *대가*를 명시.

### 6.3 Si/Ge 치환 → lattice 팽창·disorder·σ (Fig 3, 4)
- **Si⁴⁺ 치환(Li₆₊ₓP₁₋ₓSiₓS₅Br)**: lattice parameter 선형↑, **x=0.3서 saturation**(Si 용해한계, Fig 3a). MS₄ polyhedral volume↑(Fig 3b) = Si⁴⁺ 성공 incorporation. **σ 0.7→2.4 mS/cm**(x↑). 단 **x>0.3서 σ↓(용해한계 초과·상분리)**.
- **Nazar's group Li₆₊ₓMₓSb₁₋ₓS₅I(M=Si,Ge,Sn)(ref 85, Fig 4)**: Sb/Si로 anion disorder + **Li⁺ cation site disorder 동시 제어** → delocalized Li density가 new high-energy site 차지 → intermediate interstitial(local minima)이 **concerted ion migration** 활성화. **최적 Li₆.₆Sb₀.₆Si₀.₄S₅I σ = 14.8 mS/cm**(RT), **−78 ℃서도 0.25 mS/cm 유지**.
- **Se 치환**: S→Se는 electronegativity↓·lattice↑·polarizability↑ → Li 확산경로 boarding·Li-framework 상호작용 약화 → σ↑(단 Li vacancy 변화도 관여, Epp/Zeier ref 88–90).
- **Al³⁺ 치환(Li₆PS₅Br, Zhang ref 91)**: Li⁺ 자리 소량 Al → **vacancy 변화 + inter-cage jump 단축** → σ↑(주원인 = vacancy/jump, lattice 아님).

🔑 **우리 cascade 정렬**: 리뷰 §6.3의 **"aliovalent 양이온 치환이 lattice·vacancy·anion disorder를 *동시에* 조절해 σ를 켠다"** + **"Nazar Sb/Si concerted migration"** + **"Al→vacancy/jump"** = 우리 cascade co-doping의 *메커니즘 모음*. 우리 [Perc] site-percolation 백본·`migration_volume_fraction`·`dopant_blocking_fraction`이 바로 이 "vacancy/disorder/concerted" 물리의 정량화. ⚠ **단 리뷰의 치환은 전부 *σ를 켜는* 방향**(Si/Ge/Sb/Al). **우리 Nd는 σ를 *0.52× 낮추되* 대기·계면 passivation을 얻는 trade-off** → 리뷰의 "다중치환=종합개선" 정신엔 맞으나, 리뷰가 든 예시(전부 σ↑)와는 *목적 방향이 다름*(우리는 stability-leaning dopant).

---

## 7. §5(=3.2 후반) 대기안정 — HSAB + O-doping (우리 O-doping/Nd 대기축 핵심)

리뷰가 argyrodite 3대 약점 중 하나로 든 **수분취약(H₂S)**의 해법 토픽. **우리 O-doping/Nd₂O₃ cascade의 *직접 reference*.**

- **H₂S 발생 기원**: P⁵⁺의 **높은 oxygen affinity(oxophilicity)** → H₂O와 반응 → P–S 가수분해 → **toxic H₂S**(p.25666). "vacuum/inert atmosphere 필요 → 제조비용↑."
- **HSAB(hard-soft acid-base) 처방(p.25666, Fig 2)**:
  - **Sn은 P보다 soft·larger acid → soft base S 선호(hard base O 아님)** → **Sn 치환 argyrodite가 대기안정**.
  - 실증 **Li₆PS₅I–20Sn(ref 84, Fig 2)**: O₂ 10 h 노출 후 질량증가 pure Li₆PS₅I **1.12%** vs **20Sn 0.28%(10h)/0.35%(20h)**. 10% 습도 후 σ 0.22→재가열 0.31 mS/cm 회복(불순물상 사라짐). **DFT(Fig 2e): PS₄ vs (P/Sn)S₄의 H₂O 산화 난이도 = (P/Sn)S₄가 H₂O 접근 어려움**(2.04 Å vs 1.84 Å 결합).
  - 유사: Li₄SnS₄·Li₂SnS₃가 humid air서 우수 안정(ref 80–83).
- **O 공도핑(p.25666–25669)**:
  - **Zhang(ref 91) Li₆PS₅₋ₓOₓBr**: O가 가수분해 억제. **x<0.2는 무시할 영향, x=0.3서 불순물비 최소** → "**oxygen substitution obviously improved air stability**". chalcogen 중 **O·S가 Se 대비 수분안정 우수**(DFT).
  - **Zn/O 공도핑 Li₆₊₃ₓP₁₋ₓZnₓS₅₋ₓOₓ(ref 96)**: Li·S를 Zn·O로 부분치환 → **O가 σ 희생 없이 대기안정↑** + **Zn/O가 Li dendrite 억제·계면안정↑**(장기 plating/stripping). Raman: ZnO가 P–S bond 변형(local structure PS₄³⁻ 유지).
- **핵심 일반화(p.25669, 우리 cascade 정신)**: **"replacement of a single element can offer only improve a certain aspect; double or multiple substitutions provide the possibility to achieve overall improvement"** + **"in codoping, metal ions partially replace P or Li, while O partially replaces S; metal ions and oxygen cooperate with each other, improving humidity stability and other properties while retaining high ionic conductivity."**

🔑🔑 **우리 정렬**: 이 문단이 **우리 O-doping/Nd₂O₃ cascade의 *리뷰 차원 정당화*다.** 리뷰가 일반론으로 "metal+O 공도핑이 대기안정+σ유지+계면안정을 *동시에*"라고 부르고, 우리 DFT가 그 일반론을 **Nd(metal)+O 구체 시스템으로 atomistic 실현**(sei_products: O-derived Li₃PO₄/Li₂O/NdPO₄ wide-gap interphase). ⚠ **단 리뷰의 O-doping 예시(Zhang/Zn-O)는 *대기안정 측정(질량증가·H₂S)*이 중심**이고, **우리 Nd 핵심은 *전자절연 SEI/CEI(grand-potential·전자누출 차단)***. 둘 다 "metal+O 공도핑"이나 *관측량이 다름*(대기 질량 vs 전자절연 interphase) → "리뷰가 우리 Nd를 검증"이 아니라 "리뷰의 *처방 틀*에 우리가 들어맞음."

---

## 8. §4 계면 — 음극(환원) + 양극(산화) (우리 grand-potential ESW reference 줄)

리뷰의 가장 우리 산화/환원 축과 직접 닿는 토픽.

### 8.1 양극(cathode)/SE 계면 — 산화 (p.25669)
- **CV 실측**: "Li₆PS₅Cl exhibits **unstable electrochemical reactions above 2.2 V vs Li/Li⁺**"(ref 99).
- **이론 ESW(grand-potential, *간접 인용*)**: "oxidation/reduction reactants are **Li₄P₅Cl (S/S²⁻ redox, at 2.24 V)** and **Li₁₁P₅Cl (P/P⁵⁺ redox, at 1.08 V)**"(ref 100, Schwietert/Wagemaker). 활성화 장벽 낮아 빠른 분해 → 산화 시 **Li₃PS₄ + S + LiCl**, 환원 시 **P·Li₂S·LiCl**. 더 산화하면 **P₂S₅+S @2.9 V·~4.0 V**.
- **실효 ESW 확장(passivation)**: "electrochemical stability of Li₆PS₅Cl can be up to **7 V vs Li**(ref 37)"이나 실측 **practical window ~1.25 V**(ref 100). **Schwietert(ref 100): 분해경로가 direct 아니라 *(de)lithiated 준안정상 경유 indirect* → 실효 ESW가 direct 예측보다 넓다.** Li₂S·LiX·P₂S₅가 **protective interphase** 형성(ref 97, 98).
- **양극별 차이(Table 5, ref 116)**: LCO(2.6–4.3 V)·NCM(2.8–3.4)·LMO(2.4–4.0). **화학 반응성 LCO < NCM ≪ LMO**(OCV LCO 1.78·NCM 1.75·LMO 2.32 V vs In/InLi). >2.8 V서 PSₓ/phosphate/고가-sulfate로 산화.
- **LNO(LiNbO₃) 코팅**: NCM 71→147 mAh/g(반응성 1자릿수↓). LZO도 부분효과.

### 8.2 음극(anode)/SE 계면 — 환원 (p.25669–25670)
- **Li/SE 환원**: "argyrodite-type sulfides are **incompatible with Li metal**, exhibit a **reduction potential at around 1.7 V vs Li/Li⁺**"(ref 101). → Li₂S·Li₃P·LiCl interphase.
- **High electronic conductivity = dendrite 기원**(ref 108, Han): σ_e가 높으면 SE 내부 Li dendrite 핵생성. → **LiI incorporation이 dendrite 억제**(ref 109).
- **O-doping이 음극도 개선**: Li₆PS₄O₀.₃Br의 CCD 0.014→**0.9 mA/cm²**(O-doped, ref 95) ≫ pristine. O가 **shear modulus↑ + 계면안정↑**.
- **stack pressure**: 3→7 MPa로 CCD 0.2→1.0 mA/cm²(Li creep). 최적 ~5 MPa(>1000 h).
- **hybrid anode**: Li-In(0.6 V)·Li₄Ti₅O₁₂(1.5 V)로 환원 회피.

🔑 **우리 정렬·차별화**: 리뷰의 **음극 환원 ~1.7 V·양극 산화 ~2.2 V(CV)/2.24 V(이론 S/S²⁻)·Li₃PS₄+S+LiCl 분해산물**은 우리 grand-potential과 *정렬되는 줄*:
- 우리 **산화 onset 2.14(LiS4 포함)/2.256 V(제외) = 리뷰 "S/S²⁻ 2.24 V"·CV ">2.2 V"와 0.1 V 내 정합** (S²⁻-limited 동일).
- 우리 **comp1 분해 `Li₆PS₅Cl→Li₃PS₄+LiCl+S+2Li⁺+2e⁻` = 리뷰가 인용한 Schwietert 산화산물(Li₃PS₄+S+LiCl)과 정확 일치**.
- 우리 **환원 한계 1.24 V** vs 리뷰 **1.7 V** — 격차는 **Schwietert P/P⁵⁺ 1.08 V**(리뷰가 같이 인용)에 우리가 더 가까움; "1.7 V"는 *Li/SE 계면 환원전위*(다른 정의)라 직접 등치 금지.
- ⚠⚠ **그러나 리뷰엔 grand-potential 방법 *자체*가 없다** — Schwietert/Wagemaker 결과를 *문장으로 인용*만. 우리는 **get_element_profile로 직접 staircase 계산**(GG phase set). 또 리뷰는 **Cl-rich(modelc) vs comp1 산화창 비교 없음** → 우리 "Cl이 onset이 아니라 분해양/산물에 작용(S²⁻-limited 동일 onset)" 결론은 **리뷰 너머**(2020엔 [Zuo]·[Banik] 미존재).

---

## 9. §4 합성공정 — Table 3·4, Fig 5·6·7 (우리 DFT 무관 — modelc Cl 용해한계만 닿음)

우리 DFT는 합성 독립이나, **modelc Cl 1.6 용해한계** 주의가 여기서 나온다.

- **고상 vs 용액(Table 3)**: 고상 = >500 ℃·8–50 h·**고σ(0.1–10 mS/cm)**·closed system; 용액 = <300 ℃·scalable·sheet/coating 용이·**저σ(대부분 <1 mS/cm)**. argyrodite는 **PS₄³⁻ 단위라 용액합성 가능**(P₂S₇⁴⁻와 달리).
- **Fig 5(ref 134)**: Li₆PS₅Br annealing T별 **3종 점프거리 + σ**. **550 ℃서 doublet/intra/inter-cage 점프거리가 서로 가까워질 때 σ 최대(2.58×10⁻³)**. → "jump distance가 lattice·σ와 직결" (우리 inter-cage 서사의 실험 데이터).
- **Fig 6(ref 135) UMA+RTA**: one-pot ultimate-energy mechanical alloying + rapid thermal annealing → 결정화도 ~70%→82%(25분). **Li₅.₅PS₄.₅Cl₁.₅ σ = 10.2 mS/cm**. UMA가 CMA보다 σ↑.
- **Fig 7(ref 156)**: 용액합성 결정화 T별 상·불순물(LiBr·Li₂S) — 80→550 ℃ 진행.
- **Cl 용해한계 명시**(§6.2 재언급): x=1.7–1.9 Cl-rich는 **순상 위해 합성온도↑(500 ℃)** 필요 = LiCl/thio-LISICON 불순물 위험.

🔑 **우리 정렬**: 리뷰의 **"Cl-rich(x≥1.5)는 용해한계·annealing window 좁음"**은 [Zuo](Cl1.5 LiCl 불순물)·[Liu](Cl1.5 450 ℃만 순상)와 일치 → **우리 modelc(Cl 1.6)는 더 위험**(2차상). 우리 DFT는 *이상 결정*만 계산하므로 이 합성 현실은 §10 한계로 명시.

---

## 10. §5 셀통합·미래방향 (outlook) — 우리 프로그램 위치잡기 핵심

리뷰의 결론부(p.25677–25678). **우리 DFT가 어느 칸에서 닻을 내리고, 무엇이 비는지**를 가른다.

- **composite cathode(Fig 8)**: NCM111 다공전극에 Li₆PS₅Br 용액 침투 → 154 mAh/g. SE를 CAM에 코팅(PLD·용액)해 계면 favorable화.
- **sheet-type SSE membrane**: <100 µm(이상 <20–25 µm) 필요. 용액·slurry·infiltration·PI nonwoven(40–70 µm) 등.
- **3대 미해결(outlook)**:
  1. **대기안정**: codoping(metal+O)으로 더 개선해야 — "singular rather than comprehensive" 현 상태 극복.
  2. **계면**: Li/SE·cathode/SE 모두 surface treatment·microstructure로 — **in-situ 특성화(operando) 부족**.
  3. **실패기전(failure mechanism) 연구 강화** + 저가·산업화 공정.
- **미래방향 명문(p.25678)**: "component substitution should continue to be investigated … in codoping, metal ions and oxygen cooperate … improving humidity stability and other properties while retaining higher ionic conductivity. … research on the **failure mechanism** of ASSLBs needs to be further strengthened."

🔑🔑 **우리 프로그램 위치(deck용)**:
- 우리 work은 리뷰의 **§3(구조튜닝)·§5(대기안정 codoping)·§4(계면)** 세 칸에 *동시에* 앉는다 — **comp1→modelc(Cl-rich σ↑) + cascade(Nd/Mg/O/F co-doping) + grand-potential ESW/interface_reactivity + Nd passivation interphase**.
- 리뷰가 미래방향으로 부른 **"metal+O codoping으로 종합개선"**을 우리가 **atomistic in-silico로 *선행 실행***(47-dopant cascade screening) = 리뷰 outlook의 *계산적 응답*.
- **리뷰가 다루지만 우리가 안 하는 칸**: (a) **합성공정**(고상/용액·UMA·sheet — 그룹 실험 KimICCF/KimCA가 채움), (b) **operando/실패기전 동역학**(그룹 phase-field·리뷰 [Kang]가 채움), (c) **셀 통합 성능**(Table 2·5 — 우리 DFT 밖).
- **우리가 다루지만 리뷰가 (2020이라) 안 하는 것**: **Cl-rich 4축 분해(intrinsic onset·기계구속·계면·calendar) + vacancy paradox(relaxed vs clamped) + grand-potential staircase 직접계산 + foundation MLIP**.

---

## 11. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | (a) Li₆PS₅X ordered 결정구조(halide 4a octa·PS₄·free S 4d·Li 24g/48h) (b) **3종 Li 점프(doublet 48h–24g–48h / intra-cage / inter-cage)** | **comp1/modelc 구조 baseline + inter-cage 율속의 교과서 그림**(deck 구조 슬라이드) |
| Table 1 | SE 기계물성 E/H/K_c (oxide 150–200 vs **sulfide LPSX 22.1–30.0** vs organic) | 우리 E_VRH(22.06/27.66)의 *문헌 reference 줄*; "sulfide 연성=냉간가압" 근거 |
| **2** | Li₆PS₅I–20Sn 대기안정: (a)질량증가 1.12 vs 0.28% (b,c)XRD/XANES (d)Arrhenius (e)**DFT PS₄ vs (P/Sn)S₄ H₂O 산화난이도** | **HSAB·우리 O-doping/Nd 대기축의 직접 예시**; DFT로 H₂O 접근성 본 방법 |
| **3** | Si 치환 Li₆₊ₓP₁₋ₓSiₓS₅Br: (a)lattice x=0.3 saturation (b)MS₄ volume↑ (c)site disorder | aliovalent 치환의 lattice·용해한계·disorder 정량(우리 cascade lattice 효과) |
| **4** | Nazar Li₆.₇Sb₀.₃Si₀.₃S₅I 구조 + Li 점프(doublet/intra/**new inter-cage Li3 48h–48h**) | **concerted migration·new high-energy site = σ 14.8 mS/cm**; 우리 disorder/percolation 정렬 |
| **5** | (a)annealing T별 3종 점프거리 (b)Li₆PS₅Br σ vs T(550 ℃ 2.58 mS/cm 최대) | **점프거리↔σ 실험 데이터**(우리 inter-cage 서사 실증) |
| **6** | UMA+RTA one-pot 합성: (b)σ vs x(Cl) UMA>CMA (c)milling time | Cl-rich σ 10.2 mS/cm 합성; 우리 DFT 무관(공정) |
| 7 | 용액합성 결정화 T별 상·불순물(80→550 ℃) | modelc Cl-rich 용해한계·불순물 주의 |
| 8 | (a)NCM111 다공전극 Li₆PS₅Br 침투+pressing FE-SEM (b)충방전 (c)rate | composite cathode 계면(그룹 실험 KimCA/Cha 연결) |
| Table 2 | ASSLB full cell·Li 대칭셀 성능 총람(CCD·cycle) | 셀 성능 문헌 줄(우리 DFT 밖) |
| Table 5 | LCO/NCM/LMO–Li₆PS₅Cl half-cell(반응성 LCO<NCM≪LMO) | 양극별 산화반응성 trend(우리 interface_reactivity 정렬) |

---

## 12. DFT/계산 방법 ★ (리뷰 = 문헌 메타분석, 자체 계산 없음)

리뷰 자체는 **신규 DFT/실험 없음** — 인용 문헌의 방법을 종설할 뿐. 우리와 관련된 *인용된 방법*만:
- **DFT-MD(AIMD) σ/Ea 예측**(ref 1 de Klerk/Wagemaker, ref 6 Chevrier?, ref 52 Pecher): "Cl/halide·Li 함량↑→Li⁺ σ↑" 예측 → 실험 확증. = **우리 AIMD 노선의 문헌 근거**.
- **grand-potential ESW**(ref 100 Schwietert, ref 37 Mo/Ong 계열): *결과만 인용*(Li₄P₅Cl 2.24 V·실효 ESW 확장). **방법 절차·코드 미기술** → 우리 get_element_profile이 이를 *직접 재현*.
- **DFT H₂O 산화난이도**(ref 84, Fig 2e): PS₄ vs (P/Sn)S₄의 H₂O 결합/접근(2.04 vs 1.84 Å) — 대기안정 DFT.
- **DFT vacancy/jump**(ref 91 Zhang Al-doping): Al→vacancy·inter-cage jump 단축.
- **functional/k/supercell/무질서 처리**: 리뷰가 **개별 인용문헌의 DFT 디테일을 제공하지 않음** → 전부 **n/a**(원전 봐야 함).

> ⚠ 리뷰라 §4 템플릿의 code/functional/PAW/k/ecut/U/AIMD/MLIP/무질서는 **모두 n/a**(자체 계산 없음). 우리 baseline 대비는 *인용된 결과*와만 가능.

---

## 13. Post-processing ★ (인용된 기법)

리뷰가 종설한, 우리와 닿는 분석기법:
- **XRD/neutron + Rietveld**: anion site disorder(S²⁻/X⁻ 4a·4d 점유율)·lattice parameter·jump distance(ref 49, 51, 134). = 우리 disorder 모델의 실험 짝.
- **XANES(P K-edge)**: 대기노출 전후 P 환경(Fig 2c). 
- **CV(SE/C)**: 산화 onset(>2.2 V, ref 99) = 우리 산화축 실험 관측.
- **XPS/ToF-SIMS**: SEI 종(phosphate/sulfate, TM-free)·계면 성장(ref 98, 116, 117). = [Zuo]·우리 interface_reactivity 종분리.
- **DFT 도구**: grand-potential phase diagram(ref 37, 100)·AIMD MSD(σ/Ea)·H₂O 흡착(ref 84). 
> 우리 적용: 리뷰는 **"방법 카탈로그"**일 뿐 수치화/플롯 절차는 원전에. 우리가 차용할 건 **"anion disorder를 Rietveld 4a/4d 점유율로 + σ를 jump distance로 + 산화를 grand-potential staircase로"** 라는 *분석 축의 조합*.

---

## 14. 우리 DFT 대비 (comp1/modelc) → `../our_dft_baseline.md`

> ⚠ 리뷰 = **컴파일된 문헌값**(자체 계산 아님) → 아래는 "리뷰가 종설한 문헌 컨센서스" vs 우리. "일치/차이"는 *방법 의존성* 먼저 따짐.

| 항목 | 본 리뷰(문헌 컴파일) | 우리 (comp1→modelc) | 일치/차이 + 이유 |
|---|---|---|---|
| **σ (Li₆PS₅Cl)** | ~10⁻³ S/cm (고상; 용액 0.014–1.1) | (우리 DFT는 절대 σ 미보고; AIMD D만) | △ 우리 UMA σ는 3–5× 과대라 *절대 비교 금지*; Ea·ratio만 |
| **σ (Cl-rich)** | **Li₅.₅PS₄.₅Cl₁.₅ ~10 mS/cm**(ref 30) | modelc D(600K) 7.90 ≫ comp1 3.09 e-6(2.6×) | **✓ 방향 일치** (Cl-rich 빠름·disorder); 절대 σ는 미대조 |
| **Ea** | Cl-rich x=0.7서 최저(ref 76)·~0.2–0.3 eV대 | comp1 **0.253** / modelc **0.224 eV** | **✓ Cl-rich Ea↓ 방향 일치**; comp1 0.253=Schlem 실험 0.25와 정합(리뷰 ref 49 polarizability 계열) |
| **halide trend** | **σ Br≈Cl≫I(10⁻⁷)**; I는 반경 過大로 disorder 소멸 | (우리는 Cl만; [Rao11]/[Rao]가 Cl/Br/I) | **✓ 리뷰 trend = [Rao11](Cl1.9/Br6.8/I 4.6e-7)·[Rao]와 일치**; 우리 comp1=Cl 줄 |
| **anion disorder→σ** | **inter-cage jump 율속 + disorder가 장벽↓→superionic**(p.25664) | AIMD inter-cage 율속·Cl-rich disorder D↑ | **✓✓ 메커니즘 정확 일치**(리뷰=교과서 진술; [Perc]/[Dyre]/[Rao11] 백본) |
| **E (Young)** | **LPSX 22.1–30.0 GPa**(Table 1, ref 70) | E_VRH **relaxed 22.06**→27.66 (clamped 52.31) | **✓ relaxed-ion이 리뷰 줄**; clamped는 ×2 벗어남 = vacancy paradox(리뷰는 relaxed/clamped 미구분) |
| **양극 산화 onset** | CV >2.2 V; 이론 **S/S²⁻ 2.24 V**(ref 100) | **2.14(LiS4 포함)/2.256 V**(grand-potential) | **✓ 0.1 V 내 정합**(S²⁻-limited 동일); 단 리뷰는 *결과 인용*만, 방법 없음 |
| **산화 분해산물** | **Li₃PS₄ + S + LiCl**(ref 100 인용) | comp1 `→Li₃PS₄+LiCl+S+2Li⁺+2e⁻` | **✓✓ 정확 일치**(=[Zuo] Eq1·[Banik]도 동일) |
| **음극 환원** | Li/SE 계면 **~1.7 V**(ref 101); 이론 P/P⁵⁺ **1.08 V**(ref 100) | 환원 한계 **1.242 V** / OCV 1.717 V | △ 우리 1.24 ≈ P/P⁵⁺ 1.08(같은 grand-potential); "1.7 V"=Li/SE 계면전위(다른 정의)라 직접 등치 금지 |
| **band gap** | (리뷰 미보고; 반도체성 언급 없음) | comp1 2.066 / modelc 2.099 eV (PBE) | n/a — 리뷰는 gap 안 다룸; 우리 "wide-gap·PBE 과소"만 |
| **대기안정(H₂S/O-doping)** | **HSAB Sn/Sb·O codoping이 대기안정**(σ유지)(p.25666–69) | O-derived Li₃PO₄/Li₂O/NdPO₄ wide-gap interphase | **✓ 처방틀 일치**(metal+O codoping); 단 관측량 다름(질량/H₂S vs 전자절연 SEI) |

---

## 15. 적용 인사이트 (우리 프로그램 위치잡기 — deck용)

1. **field-map 좌표 확정**: Bai 2020 = **argyrodite 전용 6토픽 지도**. 우리 work은 그 중 **§3(구조튜닝)·§5(대기안정 codoping)·§4(계면)** 칸에 *동시에* 앉는다. deck "우리 연구 위치" 슬라이드에서 **"리뷰의 6토픽 중 구조튜닝·대기 codoping·계면 세 칸에 atomistic 닻"** 한 줄로.
2. **리뷰 outlook의 *계산적 응답***: 리뷰가 미래방향으로 못 박은 **"single substitution = 한 측면; multiple/co-doping = 종합개선; metal+O cooperate"**(p.25669, 25678)를 우리가 **47-dopant cascade screening으로 *선행 in-silico 실행***. = 리뷰가 부른 처방을 우리가 계산으로 답함.
3. **inter-cage 율속 = 분야 컨센서스**: 리뷰의 교과서 진술(anion disorder→inter-cage 장벽↓→superionic)이 우리 AIMD·[Rao11]·[Perc]·[Dyre]와 한 줄 → 우리 σ 서사는 *분야 표준 메커니즘*에 정확히 올라타 있다(deck 안전).
4. **Cl-rich 정렬 + 차별화**: 리뷰는 **Cl-rich σ↑(10 mS/cm)·용해한계·Al 부식**까지만. 우리 **Cl-rich 4축 분해(intrinsic onset S²⁻-limited·기계구속·계면·calendar)는 리뷰 너머**(2020 = [Zuo]/[GG]/[Banik] 이전) = **우리 명확한 기여**.
5. **대기 codoping = 우리 O/Nd의 정당화 틀**: 리뷰 §5(HSAB Sn/Sb·O codoping)가 우리 O-doping/Nd₂O₃의 *처방 정당화*. 단 "리뷰가 우리 Nd를 검증"이 아니라 "**우리 Nd가 리뷰의 metal+O codoping 틀의 한 구체 실현**"(관측량 다름 — 대기 질량 vs 전자절연 SEI)으로 정확히 표현.
6. **vacancy paradox는 리뷰 너머**: Table 1(E 22.1–30.0)은 우리 relaxed-ion 줄과 같으나, relaxed vs clamped 2.4× 격차·[Torii] 외부확증은 2020 리뷰가 모름 → 우리 elastic 기여의 독립성.
7. **정직한 비는 칸**: 합성공정(§4)·operando 실패기전(outlook)·셀성능(Table 2·5)은 우리 DFT 밖 → 그룹 실험(KimICCF/KimCA/Cha)·그룹 리뷰([Kang])가 채움. deck에서 "우리 DFT(bulk atomistic) + 그룹 실험(공정·계면·셀) = 리뷰 6토픽 풀커버"로 프레이밍.

## 16. 인용 가능 문장 (deck/paper용)

- "Bai et al.'s argyrodite review (JMCA 2020) frames the field in six topics — structure, substitution/doping, synthesis, anode/cathode interfaces, air stability, cell integration — and our DFT program plants atomistic anchors in exactly three: structural tuning (Cl-rich, cascade co-doping), air-stability co-doping (metal + O), and interfaces (grand-potential ESW)."
- "The review's central prescription — 'single substitution improves only one aspect; double/multiple co-doping enables overall improvement, with metal ions and oxygen cooperating' — is precisely what our 47-dopant cascade screening executes in silico."
- "Our grand-potential oxidation onset (2.14–2.256 V, S²⁻-limited, products Li₃PS₄ + S + LiCl) matches the review's cited values (S/S²⁻ redox at 2.24 V; CV instability > 2.2 V) within 0.1 V — the same sulfur-limited chemistry the field converges on."
- "The review reports sulfide LPSX Young's modulus 22.1–30.0 GPa; our relaxed-ion E_VRH (22.06–27.66 GPa) sits on that line, while our clamped-ion value (52.31 GPa) does not — a relaxed/clamped distinction the 2020 review does not make."

## 17. 주의/한계 (over-claim 방지)

- **리뷰 = 문헌 컴파일**(자체 계산/실험 0) → §4 DFT 디테일 전부 **n/a**; "리뷰가 X를 계산했다"는 금지(원전 인용일 뿐).
- **2020년 시점**: **Cl-rich 4축([Zuo]2022·[GG]2022·[Banik]2022·[Wu] calendar) 미존재**; **grand-potential 방법 *절차* 미기술**(결과만 ref 100/37 인용); **foundation MLIP·constrained-ESW·vacancy paradox 부재** → 리뷰를 "우리 신·심화 도구의 근거"로 쓰면 시대착오.
- **Cl-rich 조성**: 리뷰 예시 = **Cl 1.5**(Li₅.₅PS₄.₅Cl₁.₅); 우리 modelc = **Cl 1.6** → 동일시 금지(용해한계상 1.6이 더 위험).
- **σ 절대값**: 리뷰는 *실측 σ*(10⁻³–10⁻²); 우리 UMA σ는 3–5× 과대 → **절대 σ 직접 비교 금지, Ea·ratio·방향만**.
- **환원전위 1.7 V**: 리뷰의 "1.7 V"는 *Li/SE 계면 환원전위*(ref 101)이고 우리 1.24 V는 *grand-potential 환원한계*(≈Schwietert P/P⁵⁺ 1.08) — **정의가 달라 직접 등치 금지**.
- **대기 codoping 정렬**: 리뷰 O-doping 예시는 *대기 질량/H₂S 측정*이 중심, 우리 Nd는 *전자절연 SEI* — "처방틀 일치"는 맞으나 "리뷰가 우리 Nd 메커니즘을 검증"은 부정확(관측량 다름).
- **band gap·semiconductor**: 리뷰는 gap·반도체성을 안 다룸 → 우리 전자구조(VBM=S 3p·PBE 과소)와 대조 불가(n/a).
- **kim2021(Rupp)와 역할 구분**: kim2021 = oxide vs sulfide *광역* 지도(우리 좌표계 A); Bai2020 = argyrodite *전용* 6토픽 지도(우리 좌표계 B). 둘 다 리뷰지만 *스코프가 다름* — 혼동 금지.

## 18. 기법 용어 미니사전

- **anion site disorder (4a/4d)**: halide(X⁻, Wyckoff 4a) ↔ free S²⁻(Wyckoff 4d) 자리가 서로 섞여 점유되는 무질서. Cl/Br은 S²⁻와 반경 가까워 disorder 큼(고σ), I는 過大라 disorder 소멸(저σ). σ의 *구조적 뿌리*.
- **inter-cage / intra-cage / doublet jump**: argyrodite Li⁺ 3종 이동 — cage 내부(intra, 빠름)·인접위치(doublet)·cage 사이(inter, **율속**). disorder가 inter-cage 장벽을 낮춰 superionic.
- **HSAB (hard-soft acid-base)**: 연-경 산염기 원리. P⁵⁺=hard acid→O(hard base) 선호→oxophilic→H₂S; Sn/Sb=soft acid→S(soft base) 선호→대기안정.
- **oxophilicity (oxophilic)**: O와 결합하려는 경향. P⁵⁺이 높아 H₂O와 반응→가수분해→H₂S.
- **aliovalent substitution**: 모원소와 *다른 원자가*로 치환(예: P⁵⁺→Si⁴⁺/Sn⁴⁺) → Li 함량·vacancy 변화 유발.
- **concerted (cooperative) migration**: 여러 Li가 연쇄적으로 동시 이동(knock-on). new high-energy site·interstitial이 활성화. ([Perc] cooperative knock-on과 동일 개념.)
- **HT/LT phase**: argyrodite의 고온(cubic, 고σ) vs 저온(pseudo-cubic, 저σ) 상. halide 치환이 RT서 HT 상 안정화.
- **UMA + RTA**: ultimate-energy mechanical alloying(one-pot 고에너지 볼밀) + rapid thermal annealing(적외선 급속결정화) — 고결정·고σ 빠른 합성.
- **passivation interphase**: 분해산물(Li₂S·Li₃P·LiCl·LiX)이 계면에 형성돼 추가 분해를 막는 보호층 → 실효 ESW를 thermodynamic 예측보다 넓힘.
- **CCD (critical current density)**: dendrite/단락 없이 흘릴 수 있는 임계 전류밀도(음극 안정성 지표).
