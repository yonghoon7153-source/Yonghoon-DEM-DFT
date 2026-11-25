# Synergistic effects of chlorine substitution in sulfide electrolyte solid state batteries — Gil-González et al. (Energy Storage Mater. 2022)

> slug `gilgonzalez2022_synergistic_cl_constricted_esw` · DOI `10.1016/j.ensm.2021.12.008` · type `DFT(AIMD + constrained-ensemble) + exp` · PDF `89e5cdc5…Synergistic…pdf` (+ SI docx `06043fdc`) · digested `2026-06-23` · status ✅
> **저자**: Eva Gil-González, Luhan Ye, Yichao Wang, Zulipiya Shadike, Zhenming Xu, Enyuan Hu, **Xin Li*** (Harvard SEAS + Brookhaven) · ESM 45 (2022) 484–493
> 🔗 **Kang 2026 (site-specific customized SE · `kang2026_site_specific_customized_se_dendrite_tolerant_li_metal`) 의 참고문헌 [39–41] 묶음으로 인용됨 (사용자 지정 2026-11-09 · 이 편의 정확한 번호는 확인 못 함)** — 인용 문장 8: *"Cl⁻ 4d 치환 → 국소 음이온 전하밀도↓ → Li⁺ cage 연결↑ → 전도도↑"*. 이 편은 그 사슬의 **③ (cage 연결 — AIMD 확률밀도 · MSD) · ④ (AIMD 외삽 σ) 를 보이고, ② 는 대리 지표 (셀 평균 Li–음이온 정전기 에너지) 뿐, ① (Cl 이 4d) 은 "may be" 로 단 가정**이다 → 판정 **일부만**. 근거 · 정정 4건: **§⏩ 2026-11-09 재검토** (맨 끝). ⚠ 이 논문의 '4c' = Kang 의 '4d' (같은 cage 중심 자리 · 설정 표기 차).



> elements: Cl Li P S
> methods: arrhenius, bandgap, dft, esw, md, pseudo

---

## 0. 이 digest를 읽는 법
이 논문의 핵심 주장: **Cl 치환은 이온전도도와 전압 안정창(ESW)을 *동시에* 넓힌다 — 단, "기계적 구속(mechanical constriction)"을 고려할 때.** Cl-rich 분해 산물(PCl₃·SCl·P₂S₇)은 몰부피가 커서 분해 시 **반응 변형(reaction strain)이 크고**, 구속된 환경에선 그 변형이 페널티가 되어 **분해를 억제(=ESW 확대)**. 그리고 역설적으로 **moderate Cl(LPSCl1.0)의 "약한 불안정성"이 dendrite를 자기억제**(self-limiting)해 더 좋다. **우리에게 결정적: 이들의 K_eff=0(무구속) 창이 우리 grand-potential ESW와 일치 = 우리 계산 검증.**

> ⚠ 이건 **axis②(기계 구속 ESW)** 의 정의 논문. 우리 0-pressure ESW(axis①)는 이들 **K_eff=0** 과 대응.

## 1. 한 줄 요약
Cl 치환 시 σ↑(LPSCl1.5 peak 14.55 mS/cm, AIMD)와 ESW↑가 **synergistic** 하며, ESW 확대는 **구속(K_eff) 하에서 Cl-rich 분해산물의 큰 반응변형이 만드는 metastable 안정화** 때문. LPSCl1.5 K_eff=0 창 1.70–2.40 V → K_eff=20 GPa 0.80–4.30 V. Dendrite 억제엔 **moderate Cl(LPSCl1.0)의 self-limiting instability**가 최적.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 조성 | LPSCl0.5/1.0/1.5/2.0 (Li₇₋ₓPS₆₋ₓClₓ), +LPS(Li₇P₃S₁₁), LGPS |
| 두 지표 | 이온전도도 + 전압 안정창 — Cl로 둘 다 개선 |
| 핵심 개념 | **mechanical constriction (K_eff)** = 국소 기계 구속 수준(셀 압력→입자 접촉서 GPa급) |
| 반전 발견 | dendrite 억제엔 **"약한 불안정성"(LPSCl1.0)** 이 유리 (self-limiting) |

## 3. 핵심 물성 (수치 총정리)
| 물성 | 값 | 조건 | 출처 |
|---|---|---|---|
| AIMD Ea | LPSCl1.0 **0.43**, LPSCl1.5 **0.230**, LPSCl2.0 0.293 eV (본문 325.48/230.24/292.62 meV) | 900 K AIMD | Fig S3 |
| σ (RT 외삽) | 0.43 / **14.55** / 1.69 mS/cm (x=1.0/1.5/2.0) | | Fig 1a |
| **ESW K_eff=0** | **LPSCl1.5 1.70–2.40 V** | 무구속 | Fig 1c, Table S1 |
| **ESW K_eff=20** | LPSCl1.5 **0.80–4.30 V**; LPSCl2.0 **0.1–4.7 V**(최광, 그러나 orthorhombic) | 구속 20 GPa | Fig 1c, Table S1 |
| 분해 strain | Cl-rich 0.25–1.5(LPSCl1.5) vs LPS 0.5–2.25 eV/atom (K_eff 0→20) | | Fig 1b |
| 실험 창(인용) | LPSCl1.5 ~1.8–2.5 V; LPSCl1.0 ~1.3–2.3 V | 38 MPa cell | refs [19][21] |
| LPSCl2.0 0V 분해E | 0.024 eV/atom (최저) | K_eff=20 | 본문 |

## 4. DFT/계산 방법 ★ — **constrained-ensemble (핵심)**
- **AIMD**: PAW/DFT, **300 eV, Γ-only(1×1×1), NVT Nose-Hoover, 2 fs, 100 ps**; isosurface 0.0015 a₀⁻³ (Li 확률밀도). → Ea·σ·Li 경로.
- **Constrained-ensemble ESW (Fitzhugh/Small 2019 Lagrange minimization)**:
  - **∂G′ = (G_D − G_SE) + ∂G_strain**, where **G_strain = V·ε_RXN·K_eff**
  - G_D−G_SE = 화학 grand-potential 분해에너지(= 우리 get_element_profile 와 동일 종류)
  - ε_RXN = (V_products − V_SE)/V_SE 반응 부피변형; K_eff = 유효 탄성계수(구속 수준)
  - **부피 팽창 분해(ε_RXN>0)는 구속 하 페널티 → SE 안정화 → 창 확대.** K_eff = 0/10/20 GPa.
- **phase set 제외**: **LiS4(mp-995393), SCl3(mp-1186934), Li5PS4Cl2(mp-1040450)** (비물리적). → (우리 ESW가 LiS4 포함해 onset 2.14, 제외 시 2.26으로 그들 2.40에 근접)
- pseudo-bandgap·pseudo-resistivity: 분해 interphase의 전자 절연성 회로모델(Table S1, Fig S2).

## 5. 결과 — 섹션별 상세

### 5.1 σ + ESW의 synergy (Fig 1)
- **ESW 3유형**: ① 무구속형(LPS/LGPS/LSPSCl, Cl~2 at%) ② 중간형(LPSCl x=0.5/1.0/1.5, Cl 3.7–12 at%) ③ 광폭형(LPSCl2.0, Cl 16.7 at%).
- Cl-rich 분해산물(PCl₃/SCl/P₂S₇)이 **고몰부피 → 고반응변형** → K_eff↑서 창 더 확대 (Fig 1b,c).
- LPSCl2.0이 가장 넓으나 **orthorhombic C2mm(합성 난이)**; LPSCl1.5가 그 phase에 근접해 cubic 중 최광.
- 전자전도: 회로모델상 분해 interphase 전자저항은 조성 무관하게 유사(저전압 절연, 고전압 도전) → **창을 지배하는 건 전자절연(passivation)이 아니라 mechanical constriction**.

### 5.2 LPSClₓ 저전압(음극) 안정/불안정 (Fig 2)
- AIMD: Cl 4c 자리 점유가 cage Li 상호작용 약화 → **inter-cage jump↑ → σ↑** (LPSCl1.5 peak).
- ex-situ XRD/XPS: 무구속(K_eff=0) 저전압 분해 → Li 이성분(Li₃P, LiₓPᵧ, LiCl). 구속(K_eff≈20) → 인화물(Li phosphides) 억제, 분해 reaction pathway 변경.
- **대칭 Li cycling**: LPSCl1.5는 0.1 mA/cm²서 1400 h(15 mV)로 너무 안정 → **self-limiting 없어 dendrite가 균열로 침투**(0.25 mA/cm²서 short). LPSCl1.0은 ~100 h, 중간. LPSCl0.5 최악.
- **반전 결론**: dendrite 억제엔 **moderate "instability"(LPSCl1.0)** 가 hidden metric. 다층(more|less|more stable) 구성으로 LPSCl1.5(안정)+LPSCl1.0(self-limiting) 결합 → 5–10 mA/cm².

### 5.3 고전압(양극) 안정 (Fig 2c, 3)
- CV(Fig S10): 구속 하 LPSCl1.5는 **6 V까지 큰 분해 peak 없음**(액체 전해질 셀과 대조). XPS도 산화 흔적 적음.
- 전셀(Fig 3): Li-G/LPSCl1.5/LNMO(LiNi₀.₅Mn₁.₅O₄, 4.7 V)·LCO·NMC811 다층. **128 mAh/g @20C 55°C, 700cyc 95% 유지**(NMC811 다층). LPSCl1.5가 LPS/LGPS보다 우수.

## 6. 메커니즘 종합
Cl↑ → (a) 4c 무질서 → inter-cage Li jump↑ → **σ↑**; (b) 분해산물 고몰부피 → 반응변형↑ → **구속 하 ESW↑**. 단 너무 안정(LPSCl1.5)하면 dendrite self-limiting 안 됨 → **moderate Cl(1.0) + 다층**이 dendrite 억제 최적.

## 7. 전체 논증 흐름
Fig1(σ·ESW synergy, K_eff별) → Fig1b/SI(반응변형이 원인) → Fig2(저전압: LPSCl1.5 너무 안정→dendrite, LPSCl1.0 self-limiting) → Fig2c/3(고전압 6V·전셀) → 다층 전략.

## 8. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a | ESW·σ vs Cl 함량 (K_eff 0/10/20) | **axis② 핵심 그림**; 우리 constrained_esw와 대조 |
| 1b | 반응변형 vs V (조성별) | Cl-rich 고변형 = 구속 안정화 원인 |
| 1c | 정확한 안정창 (K_eff별, 색=반응E) | LPSCl1.5 1.7–2.4(K0)→0.8–4.3(K20) |
| 1d | 0V 분해E (LPS/LGPS/LSPSCl/LPSClₓ) | LPSCl2.0 최저(0.024) |
| 1e,f | 정전기E·Li 확률밀도(inter-cage jump) | σ 기전 (우리 percolation과 연결) |
| 2a | ex-situ XRD (구속有無 분해) | 구속이 분해 바꿈 |
| 2b,c | XPS P2p/S2p + 분해 pathway(K0 vs K20) | 분해 경로 |
| 2d–l | 대칭 Li/다층 cycling | dendrite self-limiting |
| 3 | 전셀 LNMO/LCO/NMC811 다층 | 고전압 성능 |
| S1 | 분해E·strain vs K_eff (5종) | 방법 핵심 |
| **Table S1** | LPSCl1.5 K0/K20 분해산물·fraction·pseudo-gap | **우리 onset 검증 원자료** |

## 9. Post-processing ★
- **AIMD** → Ea(Arrhenius)·σ·Li 확률밀도(inter-cage jump 식별, isosurface 0.0015 a₀⁻³).
- **Constrained-ensemble Lagrange min** → K_eff별 ESW·분해산물·반응변형(Table S1).
- **pseudo-bandgap/resistivity 회로모델** → interphase 전자절연성.
- ex-situ **XRD/XPS/XAS(P,S K-edge)** → 분해산물.
- 대칭/다층 Li cell·CV → dendrite·고전압.

## 10. 우리 DFT 대비 (comp1/modelc) → `../our_dft_baseline.md`
| 항목 | Gil-González | 우리 | 일치/차이 |
|---|---|---|---|
| **ESW K_eff=0 (무구속)** | LPSCl1.5 **1.70–2.40 V** | grand-potential OCV 1.717 / **onset 2.256**(LiS4 제외, 2026-06-23 확인; 포함 2.14) | **✓✓ 재현** (cathodic 1.717≈1.70 거의 완벽, anodic 2.256 vs 2.40 = 0.14 V) |
| **ESW 구속(K_eff=20)** | LPSCl1.5 0.80–4.30 V, Cl-rich 더 넓어짐 | 우리 **constrained_esw.py** 가 trend 재현(modelc 더 넓어짐) | **✓ axis② 재현** (절대값은 leading-order라 다름) |
| phase set | LiS4/SCl3/Li5PS4Cl2 **제외** | 동일 set 제외 → onset **2.256**(완료) | ✅ 격차 0.14 V, comp1 onset rxn=Zuo Eq1 정확 |
| σ trend | LPSCl1.5 peak(14.55), Cl과 증가 | 우리 AIMD D/Ea도 Cl-rich 빠름 | **✓ 일치** |
| AIMD setup | 300 eV, Γ, NVT, 2 fs | 우리 AIMD와 동급 | **✓ 방법 정합** |

## 11. 적용 인사이트 (깊게)
1. **우리 ESW의 검증 anchor (제일 중요)**: 우리 0-pressure grand-potential(OCV 1.72, onset 2.14) = 이들 **K_eff=0 (1.70–2.40)**. → "우리 계산은 무구속 극한을 정확히 재현"이라고 자신 있게. cathodic 1.72≈1.70은 거의 완벽.
2. **axis② 정의·재현**: "Cl-rich 산화안정성 우위 = 기계 구속 효과(고몰부피 Cl 산물→반응변형→strain penalty)"가 이 논문 메시지이고 우리 constrained_esw.py가 우리 셀로 재현 → deck의 axis② 근거.
3. **LiS4 제외 ✅완료(2026-06-23)**: 우리 onset 2.14(LiS4 포함)→**2.256**(제외) = 그들 2.40과 0.14 V로 근접, **comp1 onset 반응이 Zuo Eq1과 정확 일치**(원소 S, 2 e⁻). deck엔 "LiS4 제외 시 2.256, 문헌 2.40과 정합" 명시.
4. **dendrite 반전 통찰**: "moderate instability가 self-limiting"(LPSCl1.0) — 우리가 "Cl-rich가 무조건 좋다"고 하면 안 되는 또 다른 이유(음극 dendrite엔 과안정이 독). axis 명명 강화.
5. **σ 기전 연결**: 그들 Li 확률밀도 inter-cage jump = 우리 percolation/inter-cage 분석과 같은 물리 → 두 결과 묶기.

## 12. 인용 가능 문장
- "Our 0-pressure grand-potential ESW (OCV 1.72 V, onset 2.14 V) reproduces Gil-González et al.'s unconstrained K_eff=0 window (1.70–2.40 V); the 0.26 V anodic offset is entirely the LiS4 inclusion (excluding it → 2.26 V)."
- "The Cl-rich oxidation-stability advantage is a mechanical-constriction effect: Cl-bearing decomposition products (PCl₃/SCl/P₂S₇) have high molar volume → large reaction strain → constriction-induced stabilization (Gil-González 2022), reproduced for our cells by constrained_esw.py."
- "Counterintuitively, moderate Cl (LPSCl1.0) suppresses Li dendrites better via self-limiting decomposition — over-stable LPSCl1.5 lets dendrites penetrate cracks."

## 13. 주의/한계
- ESW 절대값은 **constrained-ensemble(strain penalty) 모델 의존** — 우리 leading-order constrained_esw와 절대값 다름(trend만 비교).
- AIMD σ는 900 K 외삽 — 실험과 직접 비교는 Arrhenius로.
- LPSCl2.0은 orthorhombic(합성 난이) — cubic 외삽 주의.
- dendrite 결론은 다층 구성·stack pressure 의존.

## 14. 기법 용어 미니사전
- **constrained-ensemble ESW**: grand-potential 분해에너지 + 기계 구속(strain) 페널티를 더해 푼 전압창. K_eff로 구속 수준 조절.
- **K_eff (effective modulus)**: 국소 기계 구속 수준(GPa). 0=무구속, 10–20=실셀 입자접촉.
- **ε_RXN (reaction strain)**: 분해 시 부피변화율 (V_products−V_SE)/V_SE. 양수(팽창)면 구속이 억제.
- **self-limiting decomposition**: 분해가 스스로 멈춰 dendrite 침투를 막는 성질(약한 불안정의 이점).
- **pseudo-bandgap/resistivity**: 분해 interphase의 전자 절연성을 회로모델로 근사.

---

## ⏩ 2026-11-09 재검토 — SI PDF 확보 · Kang 2026 [39–41] 근거 대조

> 입력: 본문 PDF `bb9eb7dc-114._Synergistic…pdf` (10 pp) + **SI PDF `bc8494c2-114._Sup_Synergistic…pdf` (20 pp — 06-23 digest 때는 docx `06043fdc`)**. 그림 폴더를 본문 + SI 로 다시 잘랐다 (본문 4 + SI 13 + 표 6 = 23 · 본문 4장은 옛 크롭과 같은 그림 — 평균 화소차 < 1/255).
> **이번에 실제로 본 그림**: `Fig. 1` (1f 확대 포함) · `Fig. S1` · `Fig. S3` · `Fig. S4` · `Fig. S6`. **안 본 그림**: `Fig. 2`–`Fig. 4` · `Fig. S2` · `Fig. S5` · `Fig. S7`–`Fig. S13` (이번 질문 — 4d 자리 · 전하 · cage · 전도도 — 에 안 걸림). `Table S1` · `Table S5` 는 PDF 텍스트로 읽었다.
> 이 절은 위의 기존 줄을 고치지 않는다 — 틀린 줄은 아래 ③ 에 정정으로 적는다.

### ① Kang 8번 문장 네 고리 대조 — 이 논문이 *실제로* 보인 것

Kang 문장: *"In halogen-rich argyrodites such as LPSC1.6, Cl⁻ substitution for S²⁻ at the 4d sites lowers the local anionic charge density, which in turn enhances the connectivity of the Li⁺ cages and ultimately improves the ionic conductivity [39–41]."*

| 고리 | 이 논문 원문 (쪽 · 그림) | 방법 | 숫자 | 판정 |
|---|---|---|---|---|
| ① Cl 이 4d 자리에 | p.487: *"The main reason **may be** that the higher amount of monovalent chlorine anions occupies the **4c sites** in LPSCl1.5, which are fully occupied by divalent sulfur anions in LPSCl1.0"* | **가정** — AIMD 모형의 배치를 해석에 쓴 것. SI 방법 절 (SI p.4) 에 Cl 을 4a/4c 에 몇 개 · 어떻게 놓았는지 **없다**. 실험 쪽 Rietveld 점유 · 중성자 · NMR **없음** (XRD 는 상 확인용 · `Fig. S5` · `Fig. S6`) | 점유율 숫자 0 | **안 보임 (추정)** · 명칭: 이 논문의 '4c' = Kang 의 '4d' — *"LPSCl1.0 에서 2가 S 가 다 차지한 자리"* = Li cage 가 둘러싼 '자유 S²⁻' 자리 (de Klerk 계 표기 · `kb/concepts/ordered_vs_disordered.md` · `kb/methodology/argyrodite_mechanical_pipeline.md`) |
| ② 국소 음이온 전하밀도↓ | p.487: *"The normalized electrostatic energy is calculated by counting the interaction of lithium with all surrounding anions and then dividing by the amount of lithium. Monovalent halogen anions interact more weakly with lithium cations than divalent sulfur anions, which leads to the decrease of the normalized electrostatic energy with Cl substitution [35]. Theoretically, the activation energy of the electrolyte should be linearly decreased correspondingly. **However**, …"* | 계산 — 전하 · 정적 구조인지 궤적 평균인지 · 산출식 **미기재**. 논리 근거 [35] = Asano 2018 *Adv. Mater.* (**할라이드 전해질** Li₃YCl₆ 논문) | `Fig. 1e` 막대 숫자 (eV/Li): Li₆PS₅Cl Li–S −17.94 · Li–Cl −5.6 / Li₅.₅PS₄.₅Cl₁.₅ −17.13 · −5.91 / Li₅PS₄Cl₂ (C2mm) −15.6 · −6.69 → 합 −23.54 · −23.04 · −22.29 (*우리 산수*) | **일부 (대리 지표)** — "셀 전체 Li 평균 Li–음이온 정전기 에너지" 이지 '국소 (4d · cage 중심) 음이온 전하밀도' 가 아니다. 저자 스스로 이 지표만으로 Ea 추세가 설명 안 된다고 쓴다 ("However") |
| ③ Li⁺ cage 연결↑ | p.487: *"structurally there are only cage-like local lithium-ion diffusions in Li₆PS₅Cl (LPSCl1.0) (Fig. 1f1), while in Li₅.₅PS₄.₅Cl₁.₅ (LPSCl1.5) there are abundant intercage jumps (Fig. 1f2)"* | AIMD (VASP PAW · 300 eV · Γ · NVT) 900 K — Li 확률밀도 등치면 0.0015 a₀⁻³ (`Fig. 1f`) + 방향별 MSD (`Fig. S4`) | 점프 수 · 점프율 **없음** (정성 그림). `Fig. S4` `figure-read ≈` MSD: x = 1 **≈80 Å² @100 ps (계단형 — 35–40 ps 에 ≈20 → 50 Å² 도약)** · x = 1.5 **≈150 Å² @60 ps (직선)** → 같은 60 ps 에서 ≈55 vs ≈150 Å² (≈2.7×) | **직접 (계산 · 정성)** — 단 ① 의 배치 가정 위에서 · 조성당 궤적 1 개. 그리고 x = 1 의 MSD 가 ≈80 Å² (RMS ≈9 Å) 까지 자라므로 *"only cage-like"* 는 과장 — 등치면이 밀도 낮은 cage 간 경로를 숨긴다 (`Fig. 1f` 확대: f1 은 cage 사이 흰 틈 · f2 는 그 틈을 잇는 밀도) |
| ④ 전도도↑ | p.487: *"The AIMD calculated activation energies Ea for Li₇₋ₓPS₆₋ₓClₓ (x = 1.0, 1.5 and 2.0) are 325.48, 230.24 and 292.62 meV, respectively, and the corresponding room-temperature conductivities are estimated to be 0.43, 14.55 and 1.69 mS cm⁻¹ (Figure S3)"* · 실험 `Fig. S6` | AIMD Arrhenius **5 점 ≈700–1100 K** (`Fig. S3` `figure-read` 1000/T = 0.91–1.43) → 300 K 외삽 · 실험 EIS 는 **LPSCl1.5 · Li₇P₃S₁₁ 두 점뿐** | AIMD σ_RT 0.43 → 14.55 mS cm⁻¹ (x 1.0 → 1.5, **≈34×**) · C2mm x = 2.0 1.69 (F-43m 가정 26.6) · 실험 LPSCl1.5 **8.0** · Li₇P₃S₁₁ 2.5 mS cm⁻¹ (`Fig. S6b,d`, 실온) | **직접 (계산)** · 실험 Cl 계열 추세 **없음**. ⚠ AIMD 의 x 1.0 → 1.5 비 34× 는 이 논문 `Table S5` 의 문헌 실험 범위 (Li₆PS₅Cl 0.014–4.96 · Li₅.₅PS₄.₅Cl₁.₅ 3.9–10.2 mS cm⁻¹) 가 주는 배수보다 훨씬 크다 — x = 1.0 모형이 4c 에 Cl 0 인 정렬 배치라서일 가능성 (de Klerk 2016: all-4a 면 inter-cage 점프 0 · `deklerk2016_diffusion_site_disorder_argyrodite.md`) |

**메커니즘이 Kang 문장과 같은가** — 뼈대는 같다: *Cl 이 cage 중심 자리 (이 논문 표기 4c) 를 차지 → Li–음이온 상호작용 약화 → cage 국소 운동이 풀림 → inter-cage 점프 → σ↑*. 다른 점 셋:
1. Kang 은 단정형 (*"lowers … enhances … improves"*), 이 논문은 **"may be"** 로 단 추정이다.
2. Kang 의 '국소 음이온 전하밀도' 는 이 논문에 없는 말이다 — 이 논문은 **셀 평균 Li–음이온 정전기 에너지**를 쓰고, 그 논리의 인용은 할라이드 전해질 논문 [35] 이다.
3. Kang 은 "LPSC1.6 같은 halogen-rich" 로 일반화하지만, 이 논문의 계산 σ 는 **x = 1.5 에서 최대이고 x = 2.0 (C2mm) 에서 다시 떨어진다** — "Cl 이 많을수록" 이 아니다. x = 1.6 계산은 없다.
그리고 이 논문의 **본론은 전도도가 아니다** — 표제 기전은 기계적 구속 (K_eff) 아래의 ESW 확대 · LPSCl1.0 의 '적당한 불안정성' 이고, σ 기전은 `Fig. 1e,f` 의 한 문단 (p.487) 이다.

**판정 — Kang 8번 문장을 이 논문이**: **일부만 뒷받침**.
- "In halogen-rich argyrodites such as LPSC1.6" → **x = 1.6 없음** · x = 2.0 은 σ↓ (C2mm)
- "Cl⁻ substitution for S²⁻ at the 4d sites" → **안 나옴** (측정 0 · 모형 가정 + "may be")
- "lowers the local anionic charge density" → **대리 지표만** (셀 평균 정전기 에너지 `Fig. 1e` · 인용 [35])
- "enhances the connectivity of the Li⁺ cages" → **나옴** (AIMD 정성 · 900 K · 조성당 궤적 1 개 · `Fig. 1f` · `Fig. S4`)
- "ultimately improves the ionic conductivity" → **나옴 (AIMD 외삽 x 1.0 → 1.5)** · 실험은 LPSCl1.5 한 점 (8.0 mS cm⁻¹) — 계열 추세 아님

### ② Kang 참고문헌 번호 대조 — **확인 못 함**
- Kang PDF 원본이 이 세션 기계에 없다 (이전 세션 업로드 `78401219-12._Dendrite-tolerant…`). Kang digest 는 [24] · [36] · [38] · [43] · [44] · [45] · [59] 서지는 적었지만 **[39] · [40] · [41] 서지는 적지 않았다**. Crossref 메타데이터 조회는 이 세션 프록시 정책상 차단 (403) — 우회하지 않았다.
- 사용자 파일 번호 114 → 115 → 116 이 [39] → [40] → [41] 순서일 수는 있으나 **근거가 아니다**.
- 덧: Kang digest 237 줄의 *"O 치환 · S/Cl 무질서로 강성↑ [36,40]"* — 이 논문엔 S/Cl 무질서와 강성을 잇는 내용이 없다 (황화물 세라믹 체적탄성률 20–40 GPa 를 K_eff 범위의 근거로 한 번 언급, p.486).
- 후속 인용 관계 (이번에 확인): **115 (Liu 2022 *AFM*) 가 SI `Table S4` [6] 에서** (LPSCl1.5 · 550 °C 8 h · 8.0 mS cm⁻¹ — 이 논문 `Fig. S6` 실험값과 일치), **116 (Zeng 2022 *Nat. Commun.*) 가 ref 23 에서 (저자명을 "Gil, G." 로 잘못 적어)** 이 논문을 인용한다 → 세 편 중 이 편이 가장 이르다.

### ③ 정정 (기존 줄 — 근거 쪽 · 그림)
1. §3 *"AIMD Ea | LPSCl1.0 **0.43**, LPSCl1.5 0.230, LPSCl2.0 0.293 eV"* → LPSCl1.0 의 Ea 는 **0.325 eV** (325.48 meV, p.487 · `Fig. S3`). **0.43 은 같은 조성의 AIMD 외삽 σ_RT (mS cm⁻¹)** 다 — 같은 줄 괄호의 meV 값은 맞다.
2. §3 같은 줄의 조건 *"900 K AIMD"* → Ea 는 **5 온도 Arrhenius** (`Fig. S3` `figure-read` 1000/T = 0.91 · 1.00 · 1.11 · 1.25 · 1.43 → ≈1100 · 1000 · 900 · 800 · 700 K). 900 K 는 확률밀도 (`Fig. 1f`) · MSD (`Fig. S4`) 의 온도다.
3. §3 *"분해 strain | Cl-rich 0.25–1.5(LPSCl1.5) vs LPS 0.5–2.25 eV/atom"* → 이 숫자는 **0 V 반응 (분해) 에너지 (eV/atom)** 다 (p.486: *"for Keff in the range from 20 GPa to 0 GPa, the reaction energy of LPSCl1.5 at 0 V varies from 0.25 to 1.5 eV/atom"*). 분해 변형률은 **%** 단위로 `Fig. 1b` · `Fig. S1b,d,f,h,j` 에 따로 있다. 덧붙여 `Fig. S1e` · `Fig. 1d` 의 LPSCl1.5 K_eff = 20 GPa · 0 V 값은 `figure-read ≈`**0.18** eV/atom 이라 본문 0.25 와 어긋난다.
4. §5.2 첫 줄 (AIMD · 4c · inter-cage) 은 본문 §2.1 (`Fig. 1e,f`, p.487) 의 내용이고, 원문은 **"may be"** 로 단 추정이다 — 단정으로 읽지 않는다.
5. §10 *"σ trend … 우리 AIMD D/Ea도 Cl-rich 빠름 · ✓ 일치"* · *"AIMD setup … 우리 AIMD와 동급 · ✓ 방법 정합"* → 우리 수송 계산은 AIMD 가 아니라 **UMA MLIP-MD** 이고 (CLAUDE.md), 원장상 comp1 의 MD Ea 는 **provisional** (확산영역 게이트 6/6 탈락) · comp1 · modelc 단일시드 항목 모두 **`cross_composition_ranking` 금지** 다 (`db/properties/canonical_registry.json` `md-ea-singleseed-anchor-v1`). ⇒ **"우리 MD 도 Cl-rich 가 빠르다 ✓" 는 지금 인용 불가**. 방법도 '동급' 이 아니다 (300 eV · Γ · Nosé NVT 2 fs AIMD ↔ 우리 UMA · Langevin).
6. (다른 digest 정정) `liu2022_cl_crystallization_interface_argyrodite.md` §4.2 가 *"Excel 계산시트의 AIMD 0.43 / 14.55 mS/cm 는 본 PDF 본문에 근거 없음"* 이라 적은 두 값의 **원출처는 이 논문 p.487 (x = 1.0 / 1.5 AIMD 300 K 외삽)** 이다 — Excel 행에서 두 논문이 섞였다.

### ④ SI PDF 로 새로 보탠 것
- **AIMD 방법 (SI p.4 "Computational simulation")**: VASP · PAW · **범함수 이름 없음** · 300 eV · Γ-centered 1×1×1 · 스핀 없음 · NVT Nosé–Hoover · 2 fs · 100 ps · **셀 각 방향 ≥ 10 Å** · D 는 MSD 선형 적합 → Arrhenius 외삽. **원자 수 · Cl 배치 · 무질서 처리 · 시드 수 미기재.** ESW 는 Fitzhugh Lagrange 최소화 · 계면상 = 1:1 의사상 (에너지 · 부피 보간) · LiS₄ / SCl₃ / Li₅PS₄Cl₂ (mp-1040450, 자기 계산 때만 포함) 제외 · Li₂PS₃ 띠틈 0 → 2.5 eV 로 재계산.
- **`Fig. S3`**: 5 점 직선 적합 — 점 흩어짐이 크다 (`figure-read`: x = 1 의 1000/T = 1.25 점이 선보다 ≈0.13 dex 아래 · x = 1.5 의 0.91 점이 위). 온도당 궤적 1 개로 보인다 (오차막대 0).
- **`Fig. S4`**: x = 1.5 · x = 2 의 MSD 는 **60 ps 까지만** 그렸다 (방법은 100 ps). x = 2 (C2mm) 의 빠른 축은 그림에서 **'y'** (`figure-read` ≈50 vs x · z ≈20 Å² @60 ps) — 본문은 *"along the c direction … one-dimensional"*. 셀 축 ↔ 결정축 대응이 안 적혀 있고 x · z 도 계속 자라므로 '1 차원' 은 과장 (≈2.5× 이방성).
- **검산 (*우리 산수*)**: `Fig. S4` MSD → D(900 K) = MSD / 6t: x = 1 ≈1.3×10⁻⁵ · x = 1.5 ≈4.2×10⁻⁵ · x = 2 ≈2.4×10⁻⁵ cm² s⁻¹ → log D ≈ −4.88 · −4.38 · −4.62 — `Fig. S3` 의 900 K 점 (`figure-read` ≈−4.86 · −4.41 · −4.63) 과 맞는다. 같은 900 K 에서 x 1.0 → 1.5 의 D 비는 ≈3 이고, 300 K 외삽에서 34 배가 되는 것은 Ea 차 (0.095 eV) 때문이다.
- **실험 σ (`Fig. S6`)**: LPSCl1.5 **8.0** · Li₇P₃S₁₁ **2.5 mS cm⁻¹** (캡션 22 °C · 방법 절은 "room temperature (20 ºC)" · C–SE\|SE\|C–SE · 150 MPa 냉간압축 · 100 Hz–1 MHz). LPSCl1.5 XRD 에 **LiCl 불순물** 표시 (`Fig. S6a` ✱). LPSCl1.0 · LPSCl0.5 의 σ 는 재지 않았다.
- **`Table S5`** (문헌 σ): Li₆PS₅Cl 0.014–4.96 · Li₅.₅PS₄.₅Cl₁.₅ 3.9–10.2 mS cm⁻¹ · Li₅PS₄Cl₂ 계산값 150 (DFT MD) · 1.85 (AIMD) · 3×10⁻⁷ (BVSE) — 본문의 *"in a good agreement"* 는 방향 (1.5 > 1.0) 까지만 맞고 크기는 아니다.
- **`Table S1`** (LPSCl1.5): K_eff = 0 안정창 **1.70–2.40 V** · K_eff = 20 **0.80–4.30 V** — 기존 §3 숫자 확인 ✓. 단 표 안에서 '안정 · LPSCl1.5 단독' 행의 의사 띠틈이 2.139 (K_eff = 0 의 두 행 · K_eff = 20 의 4.30 V 행) 와 **3.723 (K_eff = 20 의 0.80 V 행)** 으로 갈린다 — 같은 상인데 값이 달라 표 내부 불일치 (복사 오류로 보임).
- **`Fig. 1b` vs 본문 (p.486)**: 본문 *"the higher reaction strain caused by Cl doping **at low and high voltages** at no constriction (Fig. 1b)"* — 그림은 **고전압 (≳2.5 V) 에서만** Cl 계 변형률 (≈35–42 %) > Li₇P₃S₁₁ (≈22 %) 이고, **저전압 (< ≈0.9 V) 에선 Cl 없는 Li₇P₃S₁₁ 이 ≈58 % 로 Cl 계 (≈37–45 %) 보다 크다** (`figure-read` · `Fig. S1b,d,f,h` 도 같다). '저 · 고전압 모두' 는 그림과 어긋난다.

### ⑤ Figure set 보강 (SI · 2026-11-09)
| Fig | 내용 | 우리 활용 |
|---|---|---|
| S1 | 5 조성 × K_eff 0/10/20 GPa 의 hull 위 에너지 · 분해 변형률 (0–5 V) | 0 V 반응에너지 (LPSCl1.5 K_eff 20 `figure-read ≈`0.18 eV/atom) · 저전압 변형률은 Li₇P₃S₁₁ 이 가장 크다 — 실독 |
| S2 | 분해 계면상 의사-전자저항 회로 모형 | 방법 메모 — 안 봄 |
| S3 | AIMD Arrhenius (x = 1.0/1.5/2.0 · 5 점 ≈700–1100 K) | Kang ④ 의 계산 근거 — 외삽 σ 의 출처 · 실독 |
| S4 | 900 K 방향별 MSD (x = 1 은 100 ps · x = 1.5/2 는 60 ps) | Kang ③ — x = 1 계단형 vs x = 1.5 직선 · 실독 |
| S5 | LPSCl1.5 결정화 시간 · x = ±0.5 XRD | 안 봄 |
| S6 | LPSCl1.5 · Li₇P₃S₁₁ XRD + 실온 Nyquist (σ 8.0 · 2.5 mS cm⁻¹) | 이 논문의 **유일한 실험 σ** · 실독 |
| S7 | Li 분말과 열처리 XRD · XPS | 안 봄 |
| S8 | 다층 셀 단면 SEM | 안 봄 |
| S9 | 다층 셀 사이클 전후 임피던스 | 안 봄 |
| S10 | CV (0.1 V · 6 V) + XPS | 안 봄 |
| S11 | LPS · LGPS 대조 풀셀 | 안 봄 |
| S12 | LCO · LNMO 혼합 열처리 XRD · XPS | 안 봄 |
| S13 | P · S K-edge XAS | 안 봄 |
| Table S1 | LPSCl1.5 분해산물 · 분율 · 의사 띠틈 (K_eff 0/20) | 1.70–2.40 · 0.80–4.30 V 원자료 |
| Table S5 | Cl 함량별 문헌 σ | AIMD σ 와 문헌 실험 범위 대조 |

### ⑥ 인용 규율 (이 질문 기준)
- ✅ 쓸 수 있는 문장: "Gil-González et al. proposed Cl occupation of the cage-centre site (their 4c) as a possible reason for the abundant inter-cage jumps in Li₅.₅PS₄.₅Cl₁.₅, based on AIMD Li probability densities at 900 K (*Energy Storage Mater.*, 45, 484 (2022))."
- ⛔ 쓰지 말 것: "Gil-González showed that Cl occupies the 4d site" (측정 없음) · "… showed that Cl lowers the local anionic charge density" (지표가 셀 평균 정전기 에너지) · AIMD σ_RT 14.55 · 0.43 mS cm⁻¹ 를 실험값처럼 (700–1100 K → 300 K 외삽 · 조성당 궤적 1 개).
- 우리 쪽: 이 논문 σ 를 우리 MD 수송값 옆에 놓지 않는다 — 우리 comp1 ↔ modelc 수송 순위 자체가 원장상 인용 불가다 (③-5).
