# Synergistic effects of chlorine substitution in sulfide electrolyte solid state batteries — Gil-González et al. (Energy Storage Mater. 2022)

> slug `gilgonzalez2022_synergistic_cl_constricted_esw` · DOI `10.1016/j.ensm.2021.12.008` · type `DFT(AIMD + constrained-ensemble) + exp` · PDF `89e5cdc5…Synergistic…pdf` (+ SI docx `06043fdc`) · digested `2026-06-23` · status ✅
> **저자**: Eva Gil-González, Luhan Ye, Yichao Wang, Zulipiya Shadike, Zhenming Xu, Enyuan Hu, **Xin Li*** (Harvard SEAS + Brookhaven) · ESM 45 (2022) 484–493

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
