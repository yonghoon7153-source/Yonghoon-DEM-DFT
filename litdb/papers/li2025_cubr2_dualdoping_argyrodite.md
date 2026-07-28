# Engineering High-Performance Argyrodite Sulfide Electrolytes via Metal Halide Doping for All-Solid-State Lithium Metal Batteries — Li et al. (Energy Storage Mater. 2025)

> slug `li2025_cubr2_dualdoping_argyrodite` · DOI `10.1016/j.ensm.2025.104221` · type `exp (+ DFT 보조: PDOS·ELF·H₂O 흡착 ΔE·Br 자리 thermo)` · PDF `82ea256b-398d7029-09._Engineteries.pdf` · digested `2026-06-26` · status ✅
> **저자**: Yang Li, Gang Wu (공동 1저자), Xiaomeng Fan, Dabing Li, Hong Liu, Xiaoxue Zhao, Wanqing Ren, Peng Lei, Xianyi Zhao, Xun Wang, **Guoxu Wang** (교신, Heze Univ.), Lei Gao, **Ce-Wen Nan** (Tsinghua), **Li-Zhen Fan** (교신, USTB) · ESM 77 (2025) 104221
> **소속**: USTB(北京科技大学) Inst. Adv. Materials & Tech. + Guilin Univ. Tech. + **Tsinghua** State Key Lab New Ceramics + **Heze Univ.** · **외부 그룹 (≠ 우리 한양/Jong-Won Lee/Y.M.Lee/Cho/Cha/Kang)**

---

## 0. 이 digest를 읽는 법 (그리고 stray-파일 검증 결과)
**검증 통과**: 파일명 "09._Engineteries"는 generic이지만 **내용은 정확히 argyrodite 황화물 SE 논문** — Li argyrodite에 **CuBr₂(=Cu+Br) 이원(dual) 도핑**으로 σ·Li 금속 호환성·대기안정성을 동시에 끌어올리는 연구. (지난 hydrate 오파일 같은 off-topic 아님.)

이 논문은 **"halide 한 종(Cl)만 늘리는 대신, Cu(연산·soft acid)+Br(연음이온)을 동시에 격자에 박으면 어떻게 되나?"** 를 푼다. 핵심 통찰 3개: (a) **Cu²⁺→P⁵⁺ 자리 치환 = Li⁺ 추가 생성**(전하중성) + S²⁻ 주변 전하밀도↓ → **Li 확산장벽↓**, **Br→4a/4d 자리 = 음이온 무질서↑** → **σ 10.3 mS/cm**(LPSC-P 대비 1.9×); (b) Cu+Br이 **밴드갭을 1.82→2.41 eV로 넓혀** 전자전도 σ_e↓ + Li 금속 계면에 **wide-gap LiCl·LiBr 절연층** 형성 → dendrite 억제(CCD 1.9 mA/cm², 3000 h); (c) **Cu–S 결합이 P–S보다 강해** PS₄가 H₂O 공격에 더 견딤(물 흡착 ΔE 0.29→2.42 eV) → **대기안정성↑**(H₂S 방출↓).

> ⚠ **전압 기준**: 본문 전부 **Li/Li⁺ 기준** (In/InLi 아님). CV·CCD·full-cell 전압 모두 vs Li⁺/Li.
> ⚠ **명명**: LPSC-P = **Li₅.₅PS₄.₅Cl₁.₅** (도핑 안 한 모체, x=0) / LPSC-CB = **Li₅.₈P₀.₉Cu₀.₁S₄.₅Cl₁.₃Br₀.₂** (최적 도핑, x=0.1). 일반식 = **Li₅.₅₊₃ₓP₁₋ₓCuₓS₄.₅Cl₁.₅₋₂ₓBr₂ₓ**.

## 1. 한 줄 요약
Li argyrodite(Li₅.₅PS₄.₅Cl₁.₅)에 **CuBr₂를 도핑**(Cu가 P 자리 일부 치환 → Li⁺ 추가 + S²⁻ 전하밀도↓; Br이 4a/4d 음이온자리 → 무질서↑)하면 **σ=10.3 mS/cm(RT, 1.9×)·Ea 0.295→0.239 eV·밴드갭 1.82→2.41 eV·σ_e 3×↓** 가 되고, Li 금속과는 **wide-gap LiCl/LiBr 절연 계면층**(CCD 1.9 mA/cm²·3000 h 안정)을, 대기 중에는 **강한 Cu–S 결합으로 PS₄ 보호**(물 흡착 ΔE 0.29→2.42 eV·H₂S↓)를 만들어 → LCO 전셀 112.6 mAh/g·400 cyc 86.7 %, **FeS₂ 전셀 788.9 mAh/g·>4.02 mAh/cm²·200 cyc 80.1 %** 달성.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 비교 | **LPSC-P (Li₅.₅PS₄.₅Cl₁.₅, x=0)** vs **LPSC-CB (Li₅.₈P₀.₉Cu₀.₁S₄.₅Cl₁.₃Br₀.₂, x=0.1)** + 중간 조성 (x=0.05/0.1/0.15/0.2) |
| 일반식 | **Li₅.₅₊₃ₓP₁₋ₓCuₓS₄.₅Cl₁.₅₋₂ₓBr₂ₓ** (CuBr₂가 LiCl과 Li₂S 일부 치환) |
| 양극 | **LiCoO₂(LCO)** 안정성 검증용 + **FeS₂**(고용량 894 mAh/g 이론, earth-abundant) |
| 질문 | 단일원소(Cl) 도핑 대신 **양이온(Cu)+음이온(Br) 동시 도핑**이 σ·Li호환·대기안정을 *동시에* 개선하는가 |
| 동기/전략 | HSAB: **soft acid Cu²⁺**가 **soft base S²⁻**와 강한 Cu–S → P–S 가수분해 억제(대기안정) + Cu²⁺/P⁵⁺ 헤테로치환으로 Li⁺ 추가 + Br 무질서로 σ↑. **CuBr₂ 하나로 Cu·Br 둘 다 공급** |
| 선행 | Cu(Zhang ref33 Cu+S in LGPS), ZnO(ref24 EN), MgF₂(ref32 Liu23=우리 [Liu23]), Sn/F(ref33), HSAB(ref13/17) |

## 3. 핵심 물성 (수치 총정리)
| 물성 | LPSC-P (x=0) | **LPSC-CB (x=0.1)** | 출처/조건 |
|---|---|---|---|
| **σ (RT)** | **5.3 mS/cm** | **10.3 mS/cm** (1.9×) | Fig 2a,b (Arrhenius); intro/abstract |
| **Ea** | **0.295 eV** | **0.239 eV** | Fig 2b (slope) |
| **σ_e (전자전도)** | **1.02×10⁻⁸ S/cm** | **3.35×10⁻⁹ S/cm** (~3×↓) | Fig 2c (DC polarization, 0.2–1 V) |
| **밴드갭 (PDOS)** | **1.82 eV** | **2.41 eV** | Fig 2d (non-spin PDOS) |
| **CCD (대칭 Li)** | **0.6 mA/cm²** | **1.9 mA/cm²** (+216 %) | Fig 3a (galvanostatic step) |
| 격자상수 a | 9.8278 Å | **9.8378 Å** (팽창) | Table S1 (Rietveld), 큰 이온 치환 |
| 공간군 | F-43m | F-43m (cubic argyrodite) | Fig 1b,c (GSAS-II Rietveld, R_wp 5.31 %·R_p 1.88 %) |
| 대칭 Li 수명 | short (<수십 h) | **>3000 h @0.2 mA/cm²·0.2 mAh/cm²** | Fig 3c |
| | | **400 h @1 mA/cm²·1 mAh/cm²** | Fig S18 |
| **탄성계수 E (DFT)** | **28.2 GPa** | **28.8 GPa** (소폭↑) | 본문 §2.5 (DFT, dendrite 억제 근거) |
| **물 흡착 ΔE** | **0.29 eV** (PS₃O+H₂S) | **2.42 eV** (CuS₃O+H₂S) | Fig 6e (DFT, ΔE=U_생성−U_반응) |
| H₂S 방출 (20 % RH) | **~0.9 cm³/g** (100 min) | **~0.3 cm³/g** | Fig 6a |

### XPS / Raman / 분해산물 (정성·정량)
| 항목 | 값 | 비고 |
|---|---|---|
| Cu 2p XPS | **932.1 eV** (distinct peak) | Fig 1e, Cu²⁺ 격자 진입 확인 |
| Br 3d XPS | **68.1 / 69.1 eV** (deconvoluted doublet) | Fig 1f, Br 성공 도핑 |
| S 2p (PS₄³⁻) | **2p₁/₂ 162.0 / 2p₃/₂ 160.9 eV** | Fig 1 본문, thiophosphate |
| S 2p (CuS₄³⁻=Cu–S) | **162.6 / 162.6 eV** | Fig S7, Cu–S 결합 형성 |
| Raman PS₄³⁻ | **424 cm⁻¹** (primary) | Fig 6/S6, Cu 도핑 시 red-shift(격자팽창) |
| Raman Cu–S | **475 cm⁻¹** (신규) | Fig S6, P→Cu 치환 |
| LiCl (cycled XPS) | Cl 2p **56.3 eV** | Fig S19, Li/LPSC-CB 계면 SEI |
| LiBr (cycled XPS) | **56.9 eV** | Fig S19 |
| **Li₂S (LPSC-P 분해)** | S 2p **160.2 eV** 신규 / Raman **490.2 cm⁻¹** | Fig 4a,c, LPSC-P/Li 계면 심한 분해 (LPSC-CB엔 약함) |
| **Li₃P (LPSC-P 분해)** | P 2p 신규 peak | Fig 4b, LPSC-P/Li 계면 (LPSC-CB엔 미검출) |

### 분해산물 밴드갭 (DFT PDOS, Fig 5f–h) — **계면 절연성 핵심**
| 산물 | 밴드갭 (이 논문 DFT) | 우리 sei_products.json (MP) | 역할 |
|---|---|---|---|
| **Li₂S** | **3.04 eV** | 3.90 (marginal) | semi-insulating |
| **LiBr** | **5.07 eV** | (우리 없음) | insulator |
| **LiCl** | **6.13 eV** | 6.65 (insulator) | insulator |

### 전셀 성능
| 셀 | 값 | 조건 |
|---|---|---|
| **LCO/LPSC-CB/Li** | **112.6 mAh/g, CE 90.6 %(1st)·평균 99.8 %, 400 cyc 86.7 % 유지** | 0.2C·RT·2.8–4.2 V·8.9 mg/cm² (Fig 7b,c) |
| LCO/LPSC-P/Li (대조) | 큰 분극·**100 cyc 34.3 % 유지** (열위) | 동일 (Fig S31) |
| LCO rate | 0.1C→1C에서 **89.6 mAh/g** 회복; 0.5C 100 cyc 87.5 % | Fig 7d, S34 |
| **FeS₂/LPSC-CB/Li** | **788.9 mAh/g(1st, 0.1C), CE 93.9 %, >4.02 mAh/cm², 200 cyc 80.1 % 유지** | 6.37 mg/cm²·RT·1.0–3.0 V (Fig 7e,f) |

## 4. 재료 & 방법 (실험)
- **합성**: 통상 **고상반응(solid-phase reaction)** — 전구체 Li₂S + P₂S₅ + LiCl + **CuBr₂** 혼합 → ball-milling → 소결(Fig 1a 모식도: furnace). CuBr₂가 LiCl·Li₂S 일부 치환.
- **도핑 한계**: x>0.1(=CuBr₂ 10 % 초과) 시 **불순물 상**(Li₂S, LiCl, CuCl₂, LiBr, 미동정 상) 석출 → **용해한계** (Fig S3). σ도 x>0.1서 감소(불순물이 Li⁺ 경로 방해, Fig S11).
- **구조분석**: 싱크로트론 XRD + **GSAS-II Rietveld**(F-43m 확정, R_wp 5.31 %), ⁷Li MAS NMR(단일 공명 = 균질 화학환경; Gaussian 정적 + Lorentzian 이동성 Li 분리), Cu 2p/Br 3d XPS, S 2p(CuS₄ 확인), Raman(Cu–S 475 cm⁻¹), SEM/EDS(2–4 µm 입자, Cu·Br 균일).
- **전기화학**: EIS Arrhenius(σ·Ea), **DC polarization**(σ_e, 0.2–1 V), **CV**(Li/SE/SE+VGCF, 산화·환원 분해), **CCD**(대칭 Li, step galvanostatic), 대칭 Li plating/stripping(3000 h), **operando/time-resolved EIS**(Fig S16, 계면 진화).
- **대기/용매 안정**: **H₂S 발생량**(20 % RH 노출, Fig 6a), 노출 후 XRD(Fig 6b)·**P K-edge XANES**(Fig 6c, P 환경 불변)·노출 후 σ(Fig 6d); 용매(클로로벤젠) 침지 후 σ(Fig S29).
- **계면산물**: cycled cell XPS(LiCl 56.3·LiBr 56.9·Li₂S 160.2)·ex-situ Raman(Li₂S 490.2)·cycled XRD(LiCl@LiBr)·SEM(Li anode 단면).

## 5. DFT/계산 방법 ★
> ⚠ **본문에 DFT 파라미터 디테일이 거의 없음** — code·functional·k-points·ecut·supercell·무질서 처리 **전부 미명시**(SI에도 명시적 셋업 없는 듯). 아래는 본문에서 *수행했다고 밝힌* 계산 목록. **방어적 인용 시 "DFT (functional 미상)" 로 표기 필수.**

- **code / functional**: **명시 안 됨** (argyrodite 계 관례상 VASP/PBE 추정이나 **본문 근거 없음** → "n/a" 처리)
- **pseudo / PAW / k-points / ecut / supercell / nat**: **전부 n/a** (본문 미제공)
- **무질서 처리(SQS/enumerate/single-config)**: **n/a** — Br 자리 점유는 "structural optimization으로 여러 도핑 모델 생성 후 비교"(Fig S2)라고만 서술. 단일 배열 decorate로 보이나 명시 없음.
- **수행한 계산 4종**:
  1. **Br 자리 thermodynamics** (Fig S2): Br이 Cl을 4a·4d·16e 자리에서 치환할 때 에너지 비교 → **4a/4d 치환 에너지 비슷·낮음 → 무질서 통합**; 16e는 S와 치환 시 강한 왜곡·Li⁺ 경로 파괴 → 불리. 결론: **Br은 4a/4d 우선 점유 → 무질서·conformational entropy↑ → σ↑** (XRD와 일치).
  2. **PDOS** (Fig 2d non-spin / Fig S13 spin-resolved): Cu+Br 도핑이 **밴드갭 1.82→2.41 eV 확대** → 전자 점프 어려워짐 → σ_e↓ (DC polarization과 일치). spin-resolved도 수행.
  3. **분해산물 PDOS** (Fig 5e–h): Li-s, Cl-p, Br-p PDOS + Li₂S(3.04)·LiBr(5.07)·LiCl(6.13 eV) 밴드갭 계산 → **LiCl·LiBr이 Li₂S보다 wide-gap → 전자절연 우수 → 계면 분해 차단**.
  4. **ELF** (Fig 5c,d): Li/LPSC-P vs Li/LPSC-CB 계면 전자국재 → LPSC-P는 P·S 주위 국재(P–S 공유), **LPSC-CB는 Cu/Br EN 차로 전자가 Cl/Br 주위 재분포** → S 원자로 전자이동 차단 → LiCl@LiBr 층 생성. (s-p 혼성으로 Cl/Br 주위 전자 풍부 = [Liu23]/[Ke] 류 논리)
  5. **물 흡착 ΔE** (Fig 6e): PS₄(CuS₄) 사면체 + H₂O → PS₃O(CuS₃O) + H₂S 반응의 ΔE = U(PS₃O/CuS₃O)+U(O atom)−U(PS₃O/CuS₃O 생성)−U(S atom). **LPSC-P 0.29 / LPSC-CB 2.42 eV** → Cu–S 결합이 P–S보다 강해 가수분해 저항.

> 우리 대비: PDOS·ELF·계면 슬랩·산물 밴드갭은 **우리 전자구조 도구와 동급 분석**이나, **파라미터 미명시**라 절대값(특히 gap)의 직접 정량 비교는 부적절. 우리 PBE gap(comp1 2.066/modelc 2.099)과 이들 LPSC-P 1.82·LPSC-CB 2.41은 **둘 다 PBE류 과소평가 영역의 "wide-gap insulator"** 수준으로만 정렬 (functional·k·무질서 미상 → §10).

## 6. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1a | 합성 모식도 (Li₂S+P₂S₅+LiCl+CuBr₂ → furnace) | dual-dopant 단일전구체(CuBr₂) 전략 |
| 1b,c | LPSC-CB XRD Rietveld(F-43m, R_wp 5.31 %) + 결정구조도(4a/4d=S/Cl/Br, 4b=P/Cu, 16e=S, 48h=Li) | **자리귀속**: Br·Cl→4a/4d, Cu→4b(P자리), Li→48h |
| 1d | x=0–0.2 XRD + 확대 (피크 저각 이동=격자팽창) + 불순물(x>0.1) | 도핑 용해한계 (Cl-rich LiCl 불순물과 같은 결) |
| **1e,f** | **Cu 2p 932.1 eV / Br 3d 68.1·69.1 eV** | 도펀트 화학상태(Cu²⁺·Br⁻) 확인 |
| **2a,b** | Arrhenius σ + Ea (x별); **σ 10.3·Ea 0.239 @x=0.1** | σ-x 화산형(x=0.1 최적), Ea 최소 |
| **2c** | DC polarization σ_e (LPSC-P 1.02×10⁻⁸ / LPSC-CB 3.35×10⁻⁹) | **σ_e 직접 측정**(우리 미측정)·CCD와 역상관 |
| **2d** | non-spin PDOS, **밴드갭 2.41 eV** | gap 확대=σ_e↓ 논리 (우리 gap 비교축) |
| 2e | CV Li/LPSC-P+VGCF vs Li/LPSC-CB+VGCF; 산화 2.3 V·환원 0.8 V peak | LPSC-CB는 redox 전류 작음(계면 안정) |
| 2f | CV 확대: **산화 PS₄³⁻→S/P₂S₅, 환원 →Li₃P/Li₃P** 영역 | 분해 onset/산물 영역 (우리 ESW staircase와 대조) |
| **3a** | CCD step (LPSC-P 0.6 / **LPSC-CB 1.9 mA/cm²**) | dendrite 억제 정량(+216 %) |
| **3b** | x별 σ_e vs CCD (역상관) | "σ_e↓ → CCD↑" 직접 증거 |
| **3c** | 대칭 Li 3000 h @0.2 (LPSC-CB 안정 / LPSC-P 발산) | 장수명 음극 계면 |
| 3d | 대칭 Li 1000 h @0.5 | 고전류 안정 |
| **4a,b** | cycled XPS S 2p·P 2p — **LPSC-P: Li₂S(160.2)·Li₃P 신규 / LPSC-CB: 약함** | 계면 분해 정량(음극) |
| 4c,d | ex-situ Raman 전압별 — LPSC-P Li₂S(490.2 cm⁻¹) 출현 / LPSC-CB PS₄³⁻ 유지 | 구조 무결성(분해 억제) |
| **4e,f** | 계면 모식도 — LPSC-P=Li⁰ 박힘·균열 / LPSC-CB=균질층 | 음극 계면 도식 |
| **5a,b** | Li/LPSC-P vs Li/LPSC-CB 원자구조(반응 전후) — LPSC-P Li₂S·LiCl / LPSC-CB LiCl·LiBr | 계면 슬랩 모델 |
| **5c,d** | ELF 계면 (전자 재분포: Cl/Br 주위) | 우리 ELF/CDD와 같은 도구 |
| **5e** | PDOS Li-s·Cl-p·Br-p (LPSC-CB) | s-p 혼성·gap 판정 |
| **5f,g,h** | **Li₂S 3.04 / LiBr 5.07 / LiCl 6.13 eV** 밴드갭 | **= 우리 sei_products.json 절연산물 직접 평행** |
| **6a** | H₂S 발생 (LPSC-P 0.9 / 도핑 0.3 cm³/g) | 대기안정 정량 |
| 6b,c | 노출후 XRD·P K-edge XANES (구조·P 환경 유지) | 대기내성 구조 증거 |
| 6d | 노출후 σ (LPSC-P 3.72×10⁻⁴로 급락 / LPSC-CB 유지) | 대기노출 후 성능 보존 |
| **6e** | **물 흡착 ΔE 0.29 vs 2.42 eV** (CuS₃O vs PS₃O) | Cu–S>P–S 결합강도=대기안정 기전 |
| 7a | mould full cell 모식도(VGCF 도전재) | 셀 구성 |
| **7b,c** | LCO 사이클·충방전 (112.6 mAh/g·400 cyc 86.7 %) | 양극 안정성(LCO=4 V급) |
| 7d | LCO rate (0.1–1C, 89.6 mAh/g 회복) | 율속 |
| **7e,f** | **FeS₂ 788.9 mAh/g·200 cyc 80.1 %·>4.02 mAh/cm²** | 고용량 변환형 양극 |
| 7g | FeS₂ rate | 율속 |
| S2 | Br 자리 thermo (4a/4d vs 16e) | **자리 점유 DFT**(무질서 근거) |
| S3 | x>0.1 불순물(Li₂S/LiCl/CuCl₂/LiBr) | 용해한계 |
| S7 | S 2p CuS₄³⁻(162.6) | Cu–S 결합 |
| S13 | spin-resolved PDOS | 전자구조 상세 |
| S19 | cycled XPS LiCl(56.3)·LiBr(56.9) | 계면 SEI 종 |
| S21 | cycled XRD LiCl@LiBr | 계면 결정상 |

## 7. Post-processing ★
- **CV** (Li/SE/SE+VGCF): 산화(PS₄³⁻→S/P₂S₅, ~2.3 V)·환원(→Li₃P, ~0.8 V) 전류로 분해 취약성. 기록=peak 전위·전류크기. (LPSC-CB가 둘 다 작음=안정)
- **DC polarization → σ_e**: 0.2–1 V 정전압 plateau 전류 → 전자전도도. 기록=S/cm 절대값. **(우리 미측정 — 차용 가능 지표)**
- **CCD step**: 대칭 Li에 전류 단계 증가, short 직전 = CCD. 기록=mA/cm².
- **PDOS (spin/non-spin)**: 밴드갭·E_F 상태 → σ_e·절연성. 기록=gap(eV).
- **분해산물 PDOS**: 산물(Li₂S/LiBr/LiCl) 단독 밴드갭 → 계면 절연성. 기록=gap.
- **ELF**: 계면 전자국재 → 전자재분포(Cl/Br 주위)·결합성격(s-p 혼성).
- **물 흡착 ΔE**: PS₄+H₂O→PS₃O+H₂S 반응에너지 → 가수분해 저항. 기록=eV.
- **Rietveld(GSAS-II)**: 격자상수·자리점유. **⁷Li MAS NMR**(Gaussian 정적+Lorentzian 이동 Li 분리) → 이동성 Li 비율.
- **operando/time-resolved EIS**(Fig S16): 셀 과전압 진화와 동기 → 계면 안정/불안정 판정.
> 우리 적용: **σ_e DC-polarization 측정값**(LPSC-P 1.02×10⁻⁸ / LPSC-CB 3.35×10⁻⁹ S/cm)은 우리가 못 가진 **실측 전자전도 anchor** ([Liu23] 8.16×10⁻⁹과 같은 줄). **분해산물 밴드갭 PDOS**(LiCl 6.13/LiBr 5.07/Li₂S 3.04)은 **우리 sei_products.json(LiCl 6.65/Li₂S 3.90)의 독립 문헌 검증**.

## 8. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`
| 항목 | 이 논문 (LPSC-P / LPSC-CB) | 우리 (comp1 / modelc) | 일치 / 차이 + 이유 |
|---|---|---|---|
| **σ Cl-rich/도핑 빠름** | LPSC-P 5.3 → LPSC-CB 10.3 mS/cm | D(600K) 3.09→7.90e-6, Ea 0.253→0.224 | **✓ trend 일치** (도핑이 σ↑) — 단 이들 변수=Cu+Br(양/음 동시), 우리=Cl만. **메커니즘 동일 결**(무질서·vacancy↑) |
| **Ea↓** | 0.295 → 0.239 eV | 0.253 → **0.224 eV** | **✓ 일치**(도핑 시 Ea↓). 절대값 LPSC-P 0.295 vs 우리 comp1 0.253 = 실험 EIS vs AIMD 방법차 |
| **밴드갭 (PBE류)** | LPSC-P **1.82** → LPSC-CB **2.41 eV** | comp1 2.066 / modelc 2.099 (PBE) | △ **"wide-gap"수준만 정렬** — 이들 LPSC-P 1.82 < 우리 2.066이나 functional·k·무질서 미상 → **절대 gap 비교 금지**. 단 **도핑이 gap을 *넓힘*** 은 공통 방향 |
| **σ_e 절대값** | LPSC-P 1.02×10⁻⁸ / LPSC-CB 3.35×10⁻⁹ S/cm | 우리 **미측정** (gap=wide insulator로만 추론) | ✗ 우리 못 봄 → **이들이 실측 anchor 제공**(slide25 σ_e 논의 보강) |
| **계면 절연산물 gap** | LiCl 6.13 / LiBr 5.07 / Li₂S 3.04 eV | sei_products.json: LiCl 6.65 / Li₂S 3.90 (LiBr 없음) | **✓✓ 독립 검증** — 둘 다 LiCl≫Li₂S, "wide-gap halide가 절연 SEI" 일치. LiBr(5.07)은 우리 db에 추가 가치 |
| **환원 산물** | LPSC-P→Li₂S+Li₃P (XPS 160.2·Li₃P) | comp1/modelc 0V→Li₃P+Li₂S+LiCl | **✓ 동일 chemistry** (Li₂S+Li₃P). 도핑하면 LiCl/LiBr이 이 분해를 절연층으로 덮음 |
| **산화 분해 영역** | CV: PS₄³⁻→S/P₂S₅ (~2.3 V) | grand-potential onset 2.256 V → P₂S₇+S | **✓ 일치** (S²⁻ 산화 onset ~2.3 V, 산물 P₂Sₓ+S) |
| **기계 E** | LPSC-P 28.2 / LPSC-CB 28.8 GPa (DFT) | E_VRH comp1 22.06 / modelc 27.66; DFT 0K E 76.9(comp1) | △ **functional/정의 미상** — 28 GPa는 우리 E_VRH(22–28)와 같은 범위지만 clamped/relaxed·PBE류 미상 → 절대비교 금지. 도핑 시 E 소폭↑(우리 comp1→modelc E_VRH↑와 같은 방향) |
| **대기안정 (물 흡착)** | ΔE 0.29→2.42 eV (Cu–S 보호) | 우리 **범위 밖**(0K closed hull·기체 X) | ✗ 우리 못 봄 → 정성 인용. 단 우리 oxophilicity descriptor와 결이 같은 "결합강도→안정" 논리 |

## 9. 적용 인사이트 (깊게)
1. **σ 축 = 전원 일치 보강 + dual-doping 변종**: LPSC-P 5.3→LPSC-CB 10.3 mS/cm, Ea 0.295→0.239 = 우리 comp1→modelc(Ea 0.253→0.224)와 **같은 방향**. 단 변수가 **Cl이 아니라 Cu+Br** → 우리 "Cl이 σ↑" + 이 논문 "Cu/Br도 σ↑" = **무질서·Li⁺ 추가가 공통 레버**라는 더 일반적 결론. (Excel exp#9 mixed-halide Cl/Br 24 mS/cm와 같은 줄.)
2. **σ_e 실측 anchor 획득**: 우리는 bulk σ_e를 못 쟀고 gap(2.07)으로 "wide insulator"라고만 했는데, 이 논문이 **σ_e=1.02×10⁻⁸(LPSC-P)·3.35×10⁻⁹(LPSC-CB) S/cm** 를 DC polarization으로 실측 + **CCD와 역상관(σ_e↓→CCD↑, Fig 3b)** 을 직접 보임. → slide25 "σ_e가 dendrite 레버" 논의의 **외부 실측 근거**([Liu23] 8.16×10⁻⁹와 함께 두 번째 anchor). ⚠ 단 이들 σ_e 차이(3×)는 **gap 차이(1.82→2.41)+Cu/Br carrier 변화 복합** → gap만 분리 불가(§D 인사이트①과 같은 주의).
3. **분해산물 밴드갭 = 우리 sei_products.json 독립 검증 + LiBr 추가**: 이 논문 DFT가 **LiCl 6.13·LiBr 5.07·Li₂S 3.04 eV** → 우리 MP값(LiCl 6.65·Li₂S 3.90)과 **둘 다 LiCl≫Li₂S**, "wide-gap halide=전자절연 passivation·conductive Li₂S/Li₃P 대체"라는 **우리 cascade 중심논리를 외부 그룹 DFT가 재현**. **LiBr(5.07)은 우리 db에 없던 값** → Br계 도핑 고려 시 추가 가치.
4. **음극 계면 = wide-gap halide 절연층 (우리 'electron-blocking interphase' 패밀리)**: LPSC-CB/Li 계면이 **LiCl@LiBr 절연층**으로 Li₂S/Li₃P 전도성 분해를 막음 = 우리 Nd cascade("conductive Li₃P 0.70을 wide-gap Li₂O 5.24/Li₃PO₄ 5.73으로 대체")·[Ke] Li₂O·[Lu] LiCl·[Liu23] LiF·[KimICCF] LiF-rich SEI와 **정확히 같은 메커니즘 패밀리**(wide-gap 절연 SEI가 e⁻ leak·dendrite 차단). 단 **이들 절연층은 도핑이 만든 *native* 분해산물**(LiCl/LiBr), 우리 Nd는 *능동적 O-derived 산물* → 위치 다름(둘 다 "절연 SEI"엔 동의).
5. **대기안정 = 결합강도 descriptor의 실증**: Cu–S>P–S(물 흡착 ΔE 0.29→2.42 eV·HSAB)로 PS₄ 가수분해 억제 = 우리 **oxophilicity/ICOHP "강한 결합→안정"** 논리와 같은 결(다른 화학). 우리 O-doping이 **P–O(ICOHP −8.43, +41 % vs P–S)** 로 host를 bonding-lock하는 것과 평행 — "강한 음이온-host 결합이 분해(가수분해/산화) 저항"이라는 공통 원리. (단 우리는 대기안정 직접 계산 못 함 → §H 기체상 gap.)
6. **양극도 안정(LCO 4 V·FeS₂ 변환형)**: 우리 산화 onset 2.256 V(thermo)는 LCO 4 V와 큰 격차지만 이 논문이 **LCO 400 cyc 86.7 %·FeS₂ 788.9 mAh/g** 실증 → "실험창이 thermo onset보다 넓다"([Kang] thermo vs kinetic ECW)의 또 다른 사례. Cu–S 안정+VGCF 균질화가 kinetic passivation 제공.

## 10. 인용 가능 문장 (deck/paper용)
- "Li et al. (ESM 2025) achieve σ = 10.3 mS/cm (Ea 0.239 eV) by CuBr₂ dual doping of Li₅.₅PS₄.₅Cl₁.₅ (vs 5.3 mS/cm, 0.295 eV undoped) — the same disorder/extra-Li⁺ lever that drives our comp1→modelc Ea drop (0.253→0.224 eV), here via Cu²⁺/P⁵⁺ + Br⁻ instead of Cl⁻."
- "Their DFT decomposition-product band gaps (LiCl 6.13, LiBr 5.07, Li₂S 3.04 eV) independently reproduce our sei_products.json ordering (LiCl 6.65 ≫ Li₂S 3.90), supporting the 'wide-gap halide interphase = electronic insulation' basis of our Nd cascade."
- "Their measured electronic conductivities (LPSC-P 1.02×10⁻⁸, doped 3.35×10⁻⁹ S/cm, inversely correlated with CCD) give an external experimental anchor for our otherwise gap-only σ_e argument."
- "CuBr₂ doping widens the band gap 1.82→2.41 eV and raises the water-adsorption ΔE 0.29→2.42 eV (Cu–S stronger than P–S, HSAB) — a bond-strength-driven stability that parallels our P–O bonding-lock (ICOHP −8.43 eV) in the O-doping route."

## 11. 주의 / 한계 (over-claim 방지 — **비판적**)
- ⚠ **DFT 파라미터 전면 미명시**: code·functional·k·ecut·supercell·무질서 처리 **전부 본문 없음**. → 밴드갭(1.82/2.41)·E(28.2/28.8 GPa)·산물 gap·물 흡착 ΔE 절대값은 **방법 불명**이라 우리 값과 **직접 정량 비교 금지**(방향·순서만 정렬). "DFT (functional 미상)"로 인용.
- ⚠ **변수가 다중(Cu+Br 동시)**: σ↑·gap↑·CCD↑·대기안정↑이 **Cu 효과인지 Br 효과인지 분리 안 됨**(Cu만/Br만 대조군 부분적). → "CuBr₂ 도핑이 ~"로만, "Cu가 σ를 올린다" 식 단일귀속 금지.
- ⚠ **σ_e 3× 차이 ≠ gap만**: gap 1.82→2.41(+0.59 eV)와 σ_e 3×↓는 **carrier 농도·Cu/Br defect 동시 변화** 포함 → gap 단독 효과 분리 불가([Ma] In 도핑 gap+0.52인데 σ_e 1.2×만 = gap만으론 σ_e 설명 부족과 같은 주의).
- ⚠ **밴드갭 절대값 의심**: LPSC-P 1.82 eV는 우리 comp1 PBE 2.066보다 *낮음* + 실험 HSE(~3.3)·우리 PBE와 어긋남 → **무질서 배열/k-mesh/functional 차이**(전부 미상). "wide-gap insulator" 수준 정렬만.
- ⚠ **자리귀속 모델 의존**: Cu→4b(P자리)·Br→4a/4d는 Rietveld+DFT 추론이나, lab 분해능 한계로 Cu@P vs Cu@Li 등 완전 확정 어려움(우리 [Liu23] Mg@P 비판과 같은 류).
- ⚠ **대칭 Li 3000 h·CCD 1.9**는 **0.2/1 mA/cm²의 낮은 면적용량**(0.2 mAh/cm²) — full-cell 면적용량(>4 mAh/cm² FeS₂)과 조건 다름.
- ⚠ **LCO/LPSC-P 100 cyc 34 % vs LPSC-CB 400 cyc 87 %**: 대조군 cyc 수가 달라(100 vs 400) 직접 retention 비교는 주의.
- **외부 그룹** (USTB/Tsinghua/Heze) — 우리 그룹 논문 아님. **INDEX 우리그룹 태그 금지**.

## 12. 기법 용어 미니사전
- **HSAB (Hard-Soft Acid-Base)**: soft acid(Cu²⁺)는 soft base(S²⁻)와 강결합 선호 → Cu–S>P–S → 가수분해 저항. 도펀트 선택 원리.
- **DC polarization (σ_e)**: 정전압 인가 후 정상상태 전류 = 전자(만의) 전도도(이온 차단). dendrite 레버.
- **CCD (critical current density)**: dendrite/short 없이 견디는 최대 전류밀도.
- **헤테로치환 (heterovalent substitution)**: Cu²⁺→P⁵⁺(가수 다름) → 전하중성 위해 Li⁺ 추가 생성 → carrier↑.
- **conformational entropy**: 음이온(Cl/Br/S) 자리 무질서 배열 가짓수 → 높으면 Li⁺ sublattice 무질서·확산↑.
- **ELF**: electron localization function, 계면 전자국재(결합/lone-pair)·전자재분포 시각화.
- **물 흡착 ΔE**: PS₄+H₂O→PS₃O+H₂S 반응에너지; 클수록 가수분해 저항(대기안정).
- **P K-edge XANES**: P 흡수단 미세구조 → P 국소환경(사면체 유지 여부) 노출 전후 비교.
- **GSAS-II Rietveld**: 분말 XRD 전곡선 피팅으로 격자상수·자리점유 정밀화.
- **VGCF**: vapor-grown carbon fiber, 1D 도전재(이 논문 셀 도전재; 우리 [KimCA] 1D VGCF와 동일 물질).
