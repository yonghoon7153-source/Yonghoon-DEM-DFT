# 🔬 문헌 ↔ 우리 DFT — 물성축별 분류 + 논문 reference

> 기준값: `our_dft_baseline.md`. **각 주장마다 [출처 논문] 명시.** digest 있는 논문은 `papers/<slug>.md` 링크.
> 사용법: 새 논문 digest 시 해당 축 표에 행 1개 추가(+출처). 산화 Q&A는 맨 아래 §Q&A 로그.

## 📑 Reference key (출처 약칭)
| 약칭 | 논문 (저자·년·저널) | digest/status | 유형 |
|---|---|---|---|
| **[Zuo]** | Zuo 2022 Angew — 양극 계면 chlorination | ✅ `papers/zuo2022_chlorination_cathode_interface.md` | exp |
| **[Ke]** | Ke 2025 ESM — MgClO 음극 혼성 도핑 | ✅ `papers/ke2025_orbital_hybridization_mgclo.md` | exp+DFT |
| **[GG]** | Gil-González 2022 ESM — constrained ESW (구속) | ✅ `papers/gilgonzalez2022_synergistic_cl_constricted_esw.md` | DFT+exp |
| [Wu] | Wu 2026 Nano Energy — calendar aging | 📄 db/properties/oxidation_stability.json | exp |
| [Banik] | Banik 2022 ACS AEM — HAXPES VBM=S | ⬜ PDF | exp |
| [Liu] | Liu 2022 AdvFM — Cl 결정화/계면 | ⬜ PDF | exp |
| **[Lu]** | Lu 2025 CEJ — 음극 4d-Cl 자기분해 → LiCl interphase (gap 1.88/LiCl 6.22) | ✅ `papers/lu2025_tailoring_cl_rich_anode_licl.md` | exp+DFT |
| **[Liu23]** | Liu 2023 Angew — MgF₂ 공도핑 electron redistribution (redox-resistible, σ_e 8×↓) ⚠[Liu]≠이것(=Liu 2022 AdvFM) | ✅ `papers/liu2023_electron_redistribution_redox_resistible_mgf2.md` | exp+DFT |
| [Ma] | Ma 2026 J.E.S. — In doping, PBE gap 2.10→2.62 | ⬜ PDF | DFT |
| [Semi] | "When Electrolytes Are Semiconductors" 2026 — HSE06 gap | ⬜ PDF | DFT |
| [Kaur] | Kaur 2016 JES — elastic SQS E22.1/B28.7/G8.1 | ⬜ PDF | DFT |
| [JPCC] | First-Principles Mech&Aniso 2025 — D3 E27.4/B34.7/G10.0 | 📄 Excel | DFT |
| **[Rupp]** | Kim/Balaish/Rupp 2021 AEM — oxide vs sulfide SE + 계면 landscape 리뷰 (63 pp) | ✅ `papers/kim2021_review_oxide_sulfide_se_interfaces.md` | review |

---

> 🗺️ **Landscape note [Rupp]** (digest `papers/kim2021_review_oxide_sulfide_se_interfaces.md`): 우리 LPSCl/LPSCl1.6의 좌표계 논문. **oxide(garnet LLZO: σ~1 mS/cm·환원 0.05 V·산화 2.9 V·E 140–160 GPa·취성) vs sulfide(argyrodite Li₆PS₅X: σ~10⁻³·환원 1.7 V·산화 2.0–2.2 V·E~10–37 GPa·연성)** 의 head-to-head + 양극/음극 계면 카탈로그(Table 1·2·3·4, SI Table 1). 우리 숫자(ESW band·환원산물·연성)를 *검증*이 아니라 *문헌 줄에 정렬*하는 용도. **Cl-rich(LPSCl1.5/1.6) 자체는 안 다룸** → 우리 비교는 리뷰 너머의 기여.

## A. 이온전도도 — *Cl-rich가 빠르다 (전원 일치)*
| 주장 | 출처 | 우리 (comp1→modelc) | 일치 |
|---|---|---|---|
| Cl↑ → σ 2.5→7–10 mS/cm, Ea 0.34→0.22 eV | [Zuo](2.9→7.0), [GG](AIMD peak 14.55 @Cl1.5), [Liu], Excel exp 다수 | D(600K) 3.09→7.90e-6, Ea 0.253→**0.224** | **✓✓** |
| σ 기전 = inter-cage Li jump (Cl 4c 무질서) | [GG] (Li 확률밀도, Fig 1e,f) | 우리 percolation/inter-cage 분석과 동일 물리 | ✓ |
| **Li₆PS₅Cl = S²⁻/Cl⁻ 완전 disordered → 가장 빠른 Li⁺** (Cl이 X=Cl,Br,I 중 disorder 최대) | **[Rupp]** p.9 | comp1→modelc D↑·Ea↓ (Cl-rich 빠름) | **✓ 구조적 근거** (Cl disorder = σ↑ 원인) |
| AIMD setup (300 eV/Γ/NVT) | [GG] | 동급 | ✓ 방법 정합 |
> 인사이트: 우리 AIMD가 실험·문헌 trend 재현 → 신뢰. 절대 σ는 RT 외삽이라 Arrhenius로 비교.

## B. 산화안정성 — **4축 분리 (축 명명 없이 말하면 틀림)**
| 축 | 우위 | 출처 | 우리 값 / 재현 |
|---|---|---|---|
| **B① intrinsic 0-pressure onset** | **무승부** (S²⁻-limited, 둘 다 2.256 V) | [GG] K_eff=0 = **1.70–2.40 V**; **[Rupp]** LPSCl DFT **2.01 V**(→Li₃PS₄+S+LiCl) / **2.2 V** vs LCO(→LiCl+Li₄P₂S₆+Li₂S) | 우리 grand-potential OCV 1.717 / **onset 2.256**(LiS4 제외, GG set; 포함 시 2.14) → **✓✓ 재현**, GG 2.40과 격차 0.14 V, [Rupp] 2.0–2.2 V band와 정합 |
| **B① 방법: indirect (de)lithiation** | (우리 못 봄) | **[Rupp]** §2.5.2: LPSCl→**Li₄PS₄Cl/Li₁₁PS₅Cl 중간상** 거쳐 분해 → 실험창 ~1.25–2.5 V로 넓어 보임 (Schwietert/Wagemaker) | 우리 onset이 실험보다 낮은 이유 = indirect/passivation/kinetics의 **방법 근거** |
| **B② 기계 구속 window** | **Cl-rich 승** | [GG] K_eff=20 LPSCl1.5 **0.80–4.30 V** (Cl 산물 고몰부피→strain) | 우리 `constrained_esw.py`가 trend 재현(modelc 더 넓어짐) → **✓** |
| **B③ cathode 계면 cycling** | **Cl-rich 승** | [Zuo] R_cat 8.9<13.2, CE 79>77% (산물 양호) | 우리 grand-potential이 [Zuo] Eq1/Eq2 분해 stoichiometry 재현 → **✓ 화학** |
| **B④ calendar/thermal/moisture** | **Cl-poor(LPSCl) 승** | [Wu] 90℃ retention L6 68%>L55 48% | 범위 밖(우리 못 봄) |
> - 우리 ESW는 **B①만** 봄(S-limited 구조적). 분해 *양*([Zuo] CV 2×)·metastability(DSC/TGA)·기체는 못 잡음.
> - **deck 결론**: "전도도 이득이 산화창 손해 없이(B①–③ 중립~유리), 비용은 shelf-life(B④)." 축 명명 필수.
> - **LiS4 단서**: 우리 onset 2.14 vs [GG] 2.40 차이 = LiS4(mp-995393) 포함 탓 → 제외 시 2.26 (정합↑).

## C. 기계적 물성 — *값이 functional·정의 의존*
| 주장 | 출처 | 우리 | 비고 |
|---|---|---|---|
| E=22.1/B=28.7/G=8.1 (SQS) | [Kaur] | E_VRH 22.06(comp1) | functional/SQS 차이 |
| E=27.4/B=34.7/G=10.0, B/G=3.46(연성) | [JPCC] (PBE-D3) | E_VRH 27.66(modelc), B0 26.23→21.71 | D3라 절대값↑ |
| E 21.3→21.6 (Cl0→1.5 거의 불변) | Excel calc#12 | 우리 E_VRH 22→27.7 (변동) | 무질서/protocol 차이 |
| **sulfide 연성(B/G 1.25–2.5, E~10–37 GPa, 냉간가압) vs oxide 취성(E 100–200 GPa, K_IC 0.8–1.6)** | **[Rupp]** SI Table 1·§2.4 | 우리 B/G·연성 결론 동일 | **✓ "왜 황화물" deck 1슬라이드** (연성=부피변화 수용·intimate contact) |
| ⚠ argyrodite **E 92–100 / G 38–43 GPa** (단일 ref) | **[Rupp]** SI Table 1 | 우리 E_VRH 22–28 | **✗ outlier — 인용 금지** (같은 표 glass 13–28·LGPS 37과도 어긋남) |
| Monroe-Newman: dendrite 억제 **G_SE > ~2 G_Li (≈6.8–8.5 GPa)**, 단 무기SE엔 불충분(K_IC·grain·σ_e가 변수) | **[Rupp]** §2.4/§4.2 | 우리 G_VRH·B/G → dendrite 다리 | 우리 elastic→dendrite 연결 시 **G 하나로 결론 금지** |
> 차이 원인: relaxed vs clamped-ion, PBE vs PBEsol/D3 → 절대 E/B ±수 GPa. **비교 전 functional·ion-relax 맞출 것.** B/G 연성 결론만 robust. **[Rupp] argyrodite E절대값(92–100)은 outlier — 무시.**

## D. 전자구조 / band gap — *방법 의존, 절대 비교 금지*
| 주장 | 출처 | 우리 | 비고 |
|---|---|---|---|
| PBE gap **LPSCl 1.88 / LiCl 6.22 eV** | [Lu] | comp1 2.066 / modelc 2.098 (PBE) | 무질서·Γ-only k ±0.2–0.3 scatter. LiCl 6.22 = 전자절연 interphase 기준 |
| PBE 2.10→2.62 (In 도핑) | [Ma] | — | In 0.52 eV↑인데 σ_e 1.2×만 변(=defect-controlled) |
| PBE 2.45 / **HSE06 3.30** | [Semi] | (우리 PBE 2.07) | PBE는 ~1 eV 과소 → "wide-gap insulator"만 |
| VBM = S 3p (HAXPES) | [Banik] | 우리 PDOS VBM=S 3p | **✓ 재현** |
| **산화 onset ≈ 음이온 p-band(VBM) 깊이**: S 3p(얕음)→LPSCl 2.256 V vs O 2p(깊음)→LLZO **2.88 V (+0.63)** | [Rupp] + **우리 LLZO grand-potential**(`papers/kim2021…md` §LLZO) | comp1 VBM=S 3p, onset 2.256 | **✓ VBM character가 onset 지배** (S²⁻→S⁰ vs O²⁻→peroxide) |
| PS₄ "gap" ~2.0 → MgS₄ ~4.2 eV (도핑이 gap 확대) | [Liu23] | comp1 2.066 ≈ 그들 LPSC ~2.0 (우연) | MP smear 0.2 + PDOS 분리 추정, 엄밀 gap 아님; **MgS₄ 구조 자체 부실(§12b)** |
| **bulk σ_e(실측) = 8.16×10⁻⁹ S/cm** (Mg/F 도핑 시 1.03×10⁻⁹, 8×↓) | [Liu23] (DC분극) | 우리 미측정 | **slide25 σ_e 논의 실측 기준값** |
| sulfide = "wide-band-gap" (구체 LPSCl gap 미제시; buffer LiI gap 6.4 eV) | **[Rupp]** | comp1 2.066 / modelc 2.098 (PBE) | 리뷰 gap 절대값 無 → "wide-gap insulator" 수준만 일치(비교대상 자체 없음) |
| **interphase는 전자절연이어야 self-limiting** (LPO ALD로 LLZO σ_e 10⁻⁸→10⁻⁹ → dendrite 억제) | **[Rupp]** Fig 13·17 | (우리 σ_e 논의 frame) | [Ke]Li₂O·[Lu]LiCl·[Liu23]LiF 절연 interphase 논리의 **landscape 근거** |
> 인사이트: ① **모델 간 gap scatter(1.88 vs 2.10)는 σ_e 차이를 설명 못 함** — [Ma]는 gap +0.52인데 σ_e 1.2×만(=defect/carrier 지배, slide25 틀). ② 단, **큰 전자구조 변화(도핑)는 σ_e를 바꿈** — [Liu23]는 Mg/F로 σ_e 8×↓(gap 확대 + LiF + carrier 변화 복합, gap만 분리 불가). → "작은 모델 scatter ≠ σ_e / 큰 도핑 변화 = σ_e 가능", 두 경우 구분.

## E. 환원 / 음극(Li 금속) 계면 — **⚠ Cl-rich 유불리 문헌 충돌 (자리 점유가 변수)**
| 주장 | 출처 | 우리 | 일치 |
|---|---|---|---|
| 분해창 환원 <1.7 V / 산화 >2.1 V | [Ke] (인용), [GG] | ESW 환원 **1.24 V** / 산화 **2.14 V** | 산화 ✓(2.1≈2.14); 환원 같은 결 |
| LPSCl(1.5) 환원 산물 = Li₂S+Li₃P **+LiCl** | [Ke], [GG], **[Lu]**, **[Liu23]** | comp1/modelc 0V → Li₃P+Li₂S+**LiCl** | **✓ 동일 chemistry** ([Liu23]도 PS₄→Li₂S+Li₃P) |
| **Li₆PS₅X 환원전위 1.7 V vs Li → Li₃P+Li₂S+LiX (passivation)** | **[Rupp]** Table 3 (in-situ XPS+EIS) | comp1/modelc 환원 1.24 V → Li₃P+Li₂S+LiCl | **✓ 동일 chemistry**, 전위 절대값은 방법차(우리 0-pressure vs 인용 indirect/실험). **LiX=LiCl이 passivation 산물** = modelc Cl-rich 이점 단서 |
| **도핑 route**: PS₄³⁻의 Li-유발 redox 분해를 **Mg(s-p 혼성, S 전자풍부→전자이동 차단)+F(in-situ LiF 절연층)** 로 억제 (MgS₄는 무분해) | **[Liu23]**(MgF₂), [Ke](MgClO) | modelc 환원산물 = 그들이 억제하려는 분해산물 | 별도 축(조성 아닌 *도핑*); cascade 동기 |
| interphase **LiCl = 전자절연(gap 6.22) + 저Li⁺장벽(0.05) + 연성(Poisson 0.23)** → 좋은 buffer | **[Lu]** Fig6 | modelc가 LiCl 생성 → Lu의 "good passivator"로 해석 | **✓ 우리 LiCl 산물에 의미 부여** |
| 계면E Li/LPSCl −2.68 ≪ LiCl/LPSCl −0.19 J cm⁻² (LiCl buffer가 Li-S 자발반응 차단) | **[Lu]** Fig6a | 우리 계면 slab 미계산(gap H) | 차용 가능 |
| **[Lu] 견해**: 4d-Cl 90 % 자기분해 → LiCl passivation → **Cl-rich가 음극 유리** (CCD 0.96, 800h) | **[Lu]** | modelc Cl-rich, 4d 점유↑ 추정 → 부합 | Cl-rich ✓(조건부) |
| **[GG] 견해**: 과안정 LPSCl1.5는 self-limiting ✗ → **moderate Cl(1.0)이 유리** (다층 전략) | [GG] | — | Cl-rich ✗ |
> **🔑 화해 (정직)**: 같은 LPSCl1.5인데 [Lu]는 "Cl-rich 유리", [GG]는 "moderate 유리"로 정반대. 둘 다 **"전자절연 passivation(LiCl) 형성 = dendrite 억제 관건"** 엔 동의. 차이는 **Cl '양'이 아니라 Cl '자리(4d)'**: [Lu]의 high-4d-Cl은 metastable(E_hull +15.2)이라 자기분해→LiCl, [GG]의 조성-평균 관점은 이 자리 불안정성을 못 봄. → **deck 결론: "음극엔 Cl-rich 무조건 유리 ✗ / 전자절연 LiCl interphase 형성되면 ✓, 형성 여부는 4d-Cl 점유가 좌우"**. (상세 = `papers/lu2025_tailoring_cl_rich_anode_licl.md` §13)

## F. 도핑 (계면 전자구조 엔지니어링)
| 주장 | 출처 | 우리 연결 |
|---|---|---|
| MgClO(Mg+Cl+O) 공도핑 → 계면 metallic→gapped (s-p/p-p 혼성) → 환원 분해 차단 | [Ke] | **우리 cascade(Mg/Cl/O/F 도판트 스크리닝)의 직접 문헌 동기 ①** |
| **MgF₂(Mg+F) 공도핑** → 음극 redox 억제(실험: CCD 0.6→1.4, σ_e 8×↓). ⚠메커니즘("MgS₄ 사면체 s-p 혼성, Mg@P자리")은 **구조모델 under-determined**(lab XRD로 Mg@P vs Mg@Li 구분 불가, 자기 ELF는 이온결합, 반경상 Mg→Li) → `papers/liu2023…md` §12b | **[Liu23]** | cascade 동기 ②는 **실험적 방향**(Mg 도핑이 음극 도움)만; *기전*은 미확정으로 인용 |
| SEI = 전자절연(Li₂O 8.37 eV)+친리튬(LiMg) | [Ke] | 우리 **Li₃N**(음극 interphase) 연구와 같은 패밀리 |
| 도판트 음극 호환성 descriptor: 계면 binding energy(J/m²), E_F metallic 여부 | [Ke] | 우리 cascade 평가에 차용 가능 |
| **음이온 자리(4d) Cl 점유 엔지니어링** → 자기분해 LiCl interphase (원소도핑 아닌 *자리* 레버) | **[Lu]** | modelc Cl-rich의 4a/4d 분포 명시하면 Lu와 직접 연결 |
| **interphase 품질 descriptor 3종**: 전자 gap 넓음 + Li⁺장벽 낮음 + Poisson 연성 | **[Lu]** Fig6d | Ke binding-E와 묶어 음극 interphase 평가셋 완성 |

## G. ✅ 우리 계산이 문헌을 *검증*하는 지점 (강점)
| 우리 결과 | = 문헌 | 출처 |
|---|---|---|
| **onset 반응 (LiS4 제외)** `Li6PS5Cl→Li3PS4+LiCl+S+2Li` | = **[Zuo] Eq1 정확히 일치** (2 e⁻, 원소 S) | [Zuo] |
| modelc onset `→Li3PS4+1.6LiCl+0.4S+0.8Li` | = [Zuo] Eq2 거동 (전자 적게·LiCl 많이) | [Zuo] |
| 0-pressure ESW (OCV 1.717, onset **2.256** LiS4 제외) | = K_eff=0 (1.70–2.40), 격차 0.14 V | [GG] |
| 구속 ESW Cl-rich 확대 trend | = K_eff=20 거동 | [GG] |
| AIMD Ea/D Cl-rich 빠름 | = 실험 σ trend | [GG][Zuo][Liu] |
| VBM = S 3p | = HAXPES | [Banik] |
| 환원 산물 Li₃P+Li₂S+**LiCl** (LiCl = 전자절연 passivator) | = LPSCl(1.5) 환원; LiCl이 음극 passivation | [Ke][GG][**Lu**][**Liu23**] |

## H. ⚠️ 우리가 아직 못 하는 것 (정직 목록 → 향후)
| gap | 누가 필요로 함 | 보강책 |
|---|---|---|
| 기체상(SO₂/O₂) 포함 계면 분해 | [Zuo] R_int 메커니즘 | 기체 chempot + NCM O-release |
| 무질서 E_above_hull (metastability) | [Zuo] DSC/TGA, [Wu] | SQS/enumerate E_hull |
| ~~LiS4 제외 ESW~~ ✅ **완료 (2026-06-23)** | [GG] phase set | onset 2.256 V, comp1 rxn=Zuo Eq1 정확 일치 (`our_dft_baseline.md` §ESW 상세) |
| 구속 ESW 절대값(full Lagrange) | [GG] K_eff=20 정량 | constrained_esw 2nd-order |
| defect/σ_e 정량 | slide25 틀 | Freysoldt defect calc |
| slab IP / absolute VBM | UPS 절대 기준 | slab+vacuum |

---

## 🗨️ Q&A 로그
> 슬라이드·결과를 보며 나온 질문/답 누적. "Q&A 작성해줘" 트리거.

### Q1 · 2026-06-23 · LPSCl vs LPSCl1.6 산화안정성 누가 더 좋나? "우리 동일"과 문헌이 다르면 이유? (slide 27 ESW)
**한 줄 답**: 단일 승자 없음 — **축을 명명**해야 함. 우리 "동일"은 intrinsic onset(B①) 한정 정답, 문헌의 "다름"은 우리 ESW가 안 보는 다른 축(B②③④).
- 우리 grand-potential ESW = **intrinsic 0-pressure onset**. 첫 산화 S²⁻→S₂²⁻(황)는 두 조성 공유 → 조성 무관 = 동일. [GG] K_eff=0이 검증.
- "Cl-rich 덜 안정"([Zuo] CV·DSC/TGA) = (a) 무질서 metastability(우리 ideal 밖), (b) kinetics/접근성(2×≈σ비 2.4×), (c) CV apparent onset. **열역학 onset은 동일**([Zuo] "same peak potentials").
- "Cl-rich 더 안정"([GG] 구속, [Zuo] 계면) = B②③, 우리 0-pressure가 구조적으로 제외.
- **결론**: intrinsic 무승부 / 계면 Cl-rich 우위([Zuo]) / shelf-life Cl-rich 열위([Wu]). 축 명명 필수.
연결: §B · `our_dft_baseline.md` · `papers/zuo2022_chlorination_cathode_interface.md` §11 · `papers/gilgonzalez2022_synergistic_cl_constricted_esw.md` §10.

### Q2 · 2026-06-23 · CDD 색이 직관과 반대로 보이는 이유 (Li 노랑 / S²⁻ 파랑 / Cl⁻ 무색)
**원리**: CDD `Δρ=ρ_SCF−ρ_atom` 기준은 **중성 자유원자**(이온 아님). 색 = "중성원자 대비 증감", **절대 전하 아님**.
- **Li⁺ → 노랑(축적)**: 2s를 내주면 남은 **1s 코어가 가림↓로 수축** → 핵 위 밀도↑ (PP가 1s 가전자 포함, zval=3). 데이터: 핵 위 +0.044.
- **free S²⁻ → 파랑(결핍)**: 2e⁻ 얻지만 **soft → 구름 바깥 팽창** → 중성 S(compact) 대비 안쪽 결핍. 얻은 전자는 diffuse 바깥(+0.001, 등치면 미달→안 보임). 데이터: 핵 −0.004 / 바깥 +0.001. (lone pair는 ELF에서 노랑, CDD에선 중성도 3p 있어 안 부각)
- **Cl⁻ → 무색(≈0)**: 중성 Cl(3p⁵)≈Cl⁻(3p⁶), 전자 1개 차 + **hard/compact 3p(고전기음성도)라 팽창 거의 없음** + P–Cl 공유결합 없음 → |Δρ|~0.001(최약) → 구름 없음.
- **P–S → 노랑(P쪽)+파랑(S쪽) 짝**: 공유결합 재배치(강한 신호).
**한 줄**: CDD = 절대 전하 아니라 **중성원자 대비 재배치** → Li 수축(노랑)·S²⁻ 팽창(파랑)·Cl⁻ 무변화(무색)·P–S 공유(짝).
연결: `our_dft_baseline.md` · slide 24(CDD) · `papers/zuo2022_chlorination_cathode_interface.md`(분해화학).
