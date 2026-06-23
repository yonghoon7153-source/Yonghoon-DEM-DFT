# Tailoring argyrodite electrolyte for enhanced interface compatibility with lithium anode — Lu et al. (Chem. Eng. J. 2025)

> slug `lu2025_tailoring_cl_rich_anode_licl` · DOI `10.1016/j.cej.2025.160455` · type `exp + DFT(VASP/PBE)` · PDF `2e34de4d…Tailoring…anode.pdf` (+ SI `ea9b5cb6…Sup…`) · digested `2026-06-23` · status ✅
> **저자**: Shijie Lu, Yuxiang Zhang, Xinyu Zhang, Tianwen Yang, Haijian Lv, Zihan Li, **Daobin Mu*** (School of Materials Science & Engineering, **Beijing Institute of Technology**) · Chem. Eng. J. **507** (2025) 160455 · Received 7 Nov 2024 / Accepted 8 Feb 2025

---

## 0. 이 digest를 읽는 법 (핵심 + 우리 비교의 긴장점)
이 논문의 핵심 주장: **음극(Li metal) 쪽에서는 Cl-rich가 *오히려 유리*하다.** Cl을 음이온 자리(4a/4d)에 90.01 %까지 채운 **Cl15 (Li₅.₅PS₄.₅Cl₁.₅)** 는, 충방전 중 **4d 자리의 Cl을 내주며 표면에서 스스로 분해(self-decomposition)** → **LiCl이 풍부한 in-situ interphase**를 만든다. LiCl은 **전자 절연체(gap 6.22 eV)이면서 Li⁺ 확산장벽이 낮아(0.05 eV)** → 전자 누설(=계속 분해)을 막고 Li⁺은 통과시켜 **dendrite를 억제**한다.

> ⚠ **우리 comparison §E와의 긴장점 (정직하게 기록).** 우리는 지금까지 [GG](Gil-González)를 근거로 "**과안정 LPSCl1.5는 self-limiting이 안 돼서 moderate Cl(1.0)이 음극엔 유리**"라고 적어놨다. Lu는 **같은 조성 LPSCl1.5**를 두고 정반대("자기분해→LiCl passivation→음극 우수")를 말한다. → **§13에서 화해**: 둘 다 "전자절연 passivation이 생기느냐"가 관건이라는 데는 동의. 차이는 (a) GG는 조성-평균 관점에서 "LPSCl1.5 너무 안정", Lu는 **자리(4d) 분해능 관점**에서 "high-4d-Cl은 metastable(E_hull>0)이라 자기분해" — 즉 **Cl '양'이 아니라 Cl '자리(4d 점유)'가 변수**라는 것. (b) 성능도 다름(Lu CCD 0.96 vs GG 0.25서 short) → 자리 설계·압력·공정 차이.

## 1. 한 줄 요약
음이온 자리 Cl 점유율을 4d 90.01 %까지 끌어올린 **Cl15(LPSCl1.5)** 는 Li 음극과 만나면 **4d Cl을 내주며 자기분해 → LiCl-rich interphase**를 형성하고, 이 LiCl층의 **전자 절연 + 낮은 Li⁺ 장벽** 덕에 **대칭셀 800 h @0.5 mA cm⁻²(무단락), LCO‖Li 550 cyc @0.5C, LCO‖Li-In 10,000 cyc @5C**를 달성. **음극 호환성은 Cl-rich가 유리** (단, 자리 점유가 핵심).

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 조성 | Cl-added argyrodite **Cl10~Cl20** (Cl10 = Li₆PS₅Cl, **Cl15 = Li₅.₅PS₄.₅Cl₁.₅**, Cl18/Cl20 = 과량) |
| 주제 | **음극(Li metal) 계면 호환성** (≠ Zuo의 양극 계면) |
| 핵심 레버 | **음이온 자리(4a/4d) Cl 점유율** — 단순 조성이 아니라 *어느 자리*에 Cl이 들어가나 |
| 핵심 메커니즘 | 4d Cl → 표면 자기분해 → **LiCl-rich interphase** (전자절연 + 저 Li⁺장벽 + 연성) |
| 동기 | 황화물 SE는 Li 환원 시 전자전도성 interphase(Li₂S/Li₃P) 형성 → no-passivation → 계속 분해 → dendrite. 이를 **LiCl(전자절연)** 로 바꾸자 |
| 선행 모순 인용 | Janek 등 [14]: Li₆PS₅X(X=Cl,Br,I) 계면 임피던스 큰 차이 — 음이온 자리 역할 미규명. LiX 이온전도 순서 Li₂S < LiCl < LiBr < LiI [15]. **Li₆PS₅I는 I/S가 4a/4d 완전점유 → 주 interphase가 LiI 아닌 Li₂S**(4d S 고반응성) |

## 3. 핵심 물성 (수치 총정리)
| 물성 | Cl15 (LPSCl1.5) | Cl10 (LPSCl) | 조건 / 출처 |
|---|---|---|---|
| **이온전도도 σ** | **9.3 mS cm⁻¹** | 3.2 mS cm⁻¹ (3× 낮음) | RT, Fig 2/S2 |
| 활성화E Ea | **0.29 eV** | 0.34 eV | Fig S2 |
| **Cl 점유율 4a / 4d** | **56.32 % / 90.01 %** | (낮음) | NPD Rietveld, Fig 1b |
| Rw (Rietveld) | **2.19 %** | — | Fig 1a, ICSD 142464, F-43m |
| LiCl 잔존 무게분율 | **< 3 %** (완전 고용) | — | NPD |
| ⁷Li NMR δ (pristine) | **1.83 ppm** (더 shielded) | 2.21 ppm | Fig 1c (Cl ↑→ Li 더 가려짐) |
| ³¹P 주배위 (pristine) | **PCl₄ 41 % > PSCl₃ 38 %** | 1 broad peak | Fig 1d,e,g |
| **CCD (임계전류밀도)** | **0.96 mA cm⁻²** | 0.32 mA cm⁻² | 대칭셀, 0.9까지 작동 |
| 대칭셀 수명 | **800 h @0.5 (2000 h @0.2)** 무단락 | 수 사이클 후 실패 @0.2 | Fig 2a |
| 1st Li 도금용량 | **0.765 mAh cm⁻²** | 0.639 (Cl15 +0.126) | Fig 2b,c |
| ICE (asym. SS) | **76.5 %** | 63.9 % | Fig 2b,c |
| CV 1st-cycle 통과전하 (Red/Ox) | **7.36 / 4.92 µAh** | 12.78 / 8.17 µAh (≈2×) | Fig 3a,b (Cl15 ≈ 절반) |
| 24h 계면저항 변화 ΔR_total | **+3.5 Ω cm²** | +9.4 Ω cm² | Fig 3c–f (Cl10은 GB +8.4) |
| 풀셀 LCO‖Li | **550 cyc @0.5C** (115.5 mAh g⁻¹, CE 92.55 %) | 양극 ~100cyc 후 급락(비호환) | Fig 2f, S5 |
| 풀셀 LCO‖Li-In | **10,000 cyc @5C, 51.3 % 유지** | — | Fig S5c, S6 |
| 사이클 후 Li 표면 Cl 면적% | **15.18 → 82.57 %** (LiCl-rich) | 불균형 Cl, dendrite 침투 | Fig 5d, S12 |
| **DFT band gap** | **LPSCl 1.88 eV** / **LiCl 6.22 eV** | — | PBE PDOS, Fig 6c |
| DFT 계면에너지 | Li/LPSCl **−2.68**, LiCl/LPSCl **−0.19**, Li/LiCl **−0.89** J cm⁻² | — | Fig 6a |
| DFT Li⁺ 장벽 (interphase) | **LiCl 0.05 eV** (최저), Poisson 0.23 | Li₂S Poisson 0.17 | Fig 6d |

## 4. DFT/계산 방법 ★
- **code**: VASP (Vienna Ab initio Simulation Package)
- **functional**: **GGA-PBE** (Perdew–Burke–Ernzerhof). vdW(D3) **언급 없음**.
- **pseudo**: PAW (명시 안 됨, VASP 기본)
- **k-points**: **1×1×1 Monkhorst-Pack (Γ only)** — supercell/slab가 커서 단일 k. (우리 bulk k-mesh보다 성김 → gap scatter 요인)
- **ecut**: **520 eV**
- **수렴**: 에너지 **10⁻⁵ eV**, 힘 **0.015 eV/Å**
- **vacuum**: **15 Å** (slab/monolayer 표면 상호작용 차단)
- **slab/계면 모델**: 3종 — **Li(100)/LPSCl(2 2 0)**, **LiCl(0 0 1)/LPSCl(2 2 0)**, **Li(100)/LiCl(1 1 1)**. 격자 mismatch **0.98 % / 4.11 % / 4.7 %**. (결정면 선택 근거 = SI Note 1)
- **E_above_hull**: 자리(4a/4d) Cl 점유에 따른 안정성. **양쪽 자리 Cl = −192.1 eV(최안정)**, 4a 100 %만 = −8.4 eV, **4d 완전점유 = +15.2 eV(metastable, 분해 구동력)** (Fig S7).
- **무질서 처리**: 명시적 SQS/enumerate 아님 — **실험 NPD 점유율(4a 56 %, 4d 90 %)을 반영한 단일 배열** 수준으로 추정 + 계면 slab.

> 방법 한계(정직): **Γ-only k + PBE + slab** → band gap 절대값은 우리(2.066) 대비 낮게(1.88) — **model scatter**이지 물리적 차이 아님. interface energy/Bader는 우리가 안 하는 **계면 slab 계산**.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1a** | NPD Rietveld (Cl15), Rw 2.19 %, LiCl<3 % | F-43m·ICSD142464, Cl 완전 고용 확인 |
| **1b** | **Cl10→Cl20 4a/4d 점유율** (Cl15서 4d=90.01 % 최대, Cl18/20 반전) | **음이온 자리 점유 = 핵심 변수** (조성≠자리) |
| 1c | ⁷Li NMR: Cl10 2.21 → Cl15 1.83 ppm | Cl↑ → Li 더 shielded (Li-T2 displacement) |
| 1d,e | ³¹P NMR: Cl10 1피크 vs Cl15 PCl₄/PSCl₃ 우세 | Cl이 4d P 배위로 들어감(PClₙ) 직접 증거 |
| 1f,g | P 배위환경 + 국소 Li cluster (jump distance ↓) | σ 기전: cluster 팽창 → cage간 점프거리↓ |
| 2a | 대칭셀 Li‖Cl15‖Li 800h/2000h, CCD 0.96 | **음극 안정성 핵심 데이터** |
| 2b,c | 1st 도금용량·ICE (Cl15 76.5 % > Cl10 63.9 %) | Cl15 가역성 우수 |
| 2d,e | 비대칭 Pre-SS (Cl15 200h vs Cl10 단락) | dendrite 억제 |
| 2f | **풀셀 LCO‖Li 550cyc**, "Li/SE incompat → stable LiCl interphase" | Cl15 음극호환 → 풀셀 수명 |
| 3a,b | **CV 통과전하 (Cl15 절반)**, P/S redox 귀속 | Cl15 분해 억제 정량 |
| 3c–f | 임피던스 vs 방치시간 (Cl15 ΔR +3.5 vs Cl10 +9.4) | 계면 안정성 정량 |
| **4a** | 사이클 후 단면 SEM/EDS: **Cl 계면 집적**, P/S 반대거동 | LiCl이 계면에 모임 |
| 4b–d | depth-XPS: LiCl 55.8 eV 주성분, **Li₂S/Li₃P <5 %** | 분해 거의 안 함(LiCl만) |
| **5a–c** | **SIMS: LiCl 우세 / Li₂Sₓ 희박** (3D) | SEI 주성분 = LiCl(전자절연) ≠ Li₂S(전자전도) |
| 5d | 사이클 후 Li 표면 "LiCl-rich interphase" (Cl 15→82 %) | in-situ LiCl층 형성 시각화 |
| 5e | ⁷Li NMR pristine 2.13 → cycled 1.83 ppm | 사이클 후 Li 환경 비대칭화 |
| 5f,g | ³¹P: cycled서 **PCl₄ 41→36 %↓, PS₂Cl₂ 17→24 %↑** | **4d Cl이 방출됨** 직접 증거 |
| **6a** | **계면에너지 3모델** (Li/LPSCl −2.68 최저=가장 불안정) | Li/LPSCl 자발반응(Li-S 결합) → LiCl buffer 필요 |
| **6b** | **Bader 평균전하**: LiCl/LPSCl(P+2.05,S+0.47,Cl−0.57) vs Li/LPSCl(P+0.12,S−0.41,Cl−0.43) | LiCl계면은 [PS₄]³⁻ 보존, Li계면은 [PS₄]³⁻ 해체 |
| **6c** | **PDOS gap**: LPSCl 1.88(VB=S 지배), LiCl 6.22 eV | LiCl=전자절연체; LPSCl gap=S의 "전자전도" |
| **6d** | **band gap + Li⁺장벽** 비교 (LiCl/LiF/LiI/LiBr/LiOH/Li₂CO₃/Li₂S) | LiCl: 넓은 gap + 최저장벽(0.05) = 최적 buffer |
| 7 | 계면진화 모식도 (연속분해 vs 자기분해-LiCl) | **deck 음극 슬라이드 모델 그림** |

## 6. 결과 — 섹션별 상세

### 6.1 구조: Cl이 4d 자리를 채운다 (Fig 1)
- NPD/Rietveld(Rw 2.19 %): Cl15는 **F-43m(ICSD 142464)** cubic argyrodite. LiCl 별도상 무게분율 **<3 %** → Cl이 격자에 거의 완전 고용.
- **Cl 점유 (Fig 1b)**: Cl10→Cl15로 가며 **4a 56.32 %, 4d 90.01 %** 까지 증가. **Cl15서 4d 점유 최대**. Cl18/Cl20은 반전(added LiCl 미고용).
- ⁷Li NMR(1c): Cl10 2.21 → Cl15 **1.83 ppm** (저주파 이동 = Li 핵 더 shielded). S(4a/4d)가 Cl로 치환될수록 Li-T2 displacement ↑.
- ³¹P NMR(1d,e): Cl10은 1개 broad peak, Cl15는 두 주공명 + shoulder. **PCl₄(41 %) > PSCl₃(38 %)** 우세 → Cl이 4d로 들어가 P 배위가 PClₙ형으로. (배위: PS₄/PS₃Cl/PS₂Cl₂/PSCl₃/PCl₄)
- **σ 기전 (1g)**: 4d/4a Cl↑ → 48h/4d와 Coulomb 인력↑ + 4a Li⁺ 반발↓ → 4a 평균전하↓ → **Li 재분포·cluster R_mean↑(Li-T2)** → cluster 팽창이 **cluster간 점프거리(48h↔4d)를 줄여** 장거리 전도↑ → σ **9.3 mS cm⁻¹**.

### 6.2 음극 안정성: 대칭셀·풀셀 (Fig 2)
- **대칭셀**: Cl15 **2000 h@0.2 / 800 h@0.5 mA cm⁻²** 무단락. Cl10은 0.2서 수 사이클 후 실패.
- **CCD**: Cl15 **0.96 mA cm⁻²** ≫ Cl10 0.32. Cl15는 0.9서도 작동.
- 1st Li 도금: Cl15 **0.765 mAh cm⁻²**(Cl10 0.639, +0.126), **ICE 76.5 %**(Cl10 63.9 %).
- 비대칭 Pre-SS(prelith. 0.3 mAh cm⁻²): Cl15 200 h@0.1 안정 / Cl10 수 사이클 후 단락.
- **풀셀**: LCO‖Cl15‖Li **550 cyc@0.5C(0.49 mA)**, 0.1C 첫용량 115.5 mAh g⁻¹·CE 92.55 %. LCO‖Cl15‖Li-In **10,000 cyc@5C, 51.3 % 유지**. Cl10은 양극 비호환으로 급락.

### 6.3 분해 억제 정량: CV·임피던스 (Fig 3)
- CV(0.1–6 V): 환원 큰 peak ~−0.3 V (P⁵⁺→P⁰/P³⁻), 산화 peak ~1.2 V(P³⁻/P⁰)·~2.0 V(S²⁻/S⁰). **Cl15 통과전하 = Cl10의 ≈절반** (Red 7.36/12.78, Ox 4.92/8.17 µAh) → Cl15가 redox에 덜 참여.
- 임피던스(방치 24h): Cl15 **R_inter +4.8, R_ct −1.3 → ΔR_total +3.5 Ω cm²** (R_bulk·R_gb 불변). Cl10 **R_ct −2.9, GB +8.4 → +9.4 Ω cm²**. → Cl15가 분해를 억제하며 낮은 계면저항 유지.

### 6.4 interphase 정체: LiCl이다 (Fig 4·5)
- **단면 SEM/EDS(4a)**: 사이클 후 **Cl이 계면에 집적**(점선), P·S는 반대(계면서 감소). (Cl10은 Fig S9: Li dendrite 침투 + Cl 불균형)
- **depth-XPS(4b–d)**: Li1s **LiCl 55.8 eV가 주성분**(전 깊이). S2p/P2p 분해(PS₄³⁻/P-Sₙ-P/Li₂S/Li₃P). **분해부산물 Li₂S·Li₃P/P 합쳐 전 종의 <5 %** → Cl15는 Li 상대로 안정. (Cl10은 S10: 강한 분해, Li₂S·황산염 다량 + dendrite)
- **SIMS(5a–c)**: 계면 SEI는 **LiCl이 지배**, Li₂Sₓ는 희박(전 깊이). → SEI 주성분이 **전자절연 LiCl**(≠ 전자전도 Li₂S) → passivation.
- **Li 표면(5d)**: 사이클 후 Li에 **"LiCl-rich interphase"** 막. Cl 면적% **15.18 → 82.57 %**.
- ⁷Li NMR(5e): pristine 2.13 → cycled 1.83 ppm + 광폭화 → Li 환경 비대칭·이동도↓.
- **³¹P NMR(5f,g)**: cycled서 **PCl₄ 41→36 %↓, PS₂Cl₂ 17→24 %↑** → **4d 자리에서 Cl이 방출**되어 LiCl interphase로 감 (자기분해의 직접 분광 증거).

### 6.5 DFT: 왜 LiCl interphase가 좋은가 (Fig 6)
- **E_hull(Fig S7)**: 4d 완전 Cl점유 = **+15.2 eV(metastable)** → **LiCl로 분해할 열역학 구동력**. 분해식:
  - **Eq1: Li₅.₅PS₄.₅Cl₁.₅ → Li₃PS₄ + 1.5 LiCl + 0.5 Li₂S**
  - **Eq2: Li₆PS₅Cl → Li₃PS₄ + LiCl + Li₂S**
  - → Cl15가 **LiCl을 더 많이(1.5 vs 1.0)** 내놓음 → 표면 LiCl enrich → 전자 차폐 → 추가 분해 억제.
- **계면에너지(6a)**: Li/LPSCl **−2.68**(가장 음=가장 불안정, 자발 Li-S 결합·구결합 파괴), LiCl/LPSCl **−0.19**, Li/LiCl **−0.89** J cm⁻². → **LiCl이 Li와 LPSCl 사이 buffer**로 들어가면 Li/LPSCl 직접접촉의 격렬반응을 회피.
- **Bader(6b)**: LiCl/LPSCl 계면 — P **+2.05**, S **+0.47**, Cl **−0.57** (P·S 잃는 전자 ≈ bulk [PS₄]³⁻ → LiCl 무해). Li/LPSCl 계면 — P **+0.12**, S **−0.41**, Cl **−0.43** → Li-S/Li-P 형성으로 **[PS₄]³⁻ 해체**(비호환).
- **PDOS(6c)**: **LPSCl gap 1.88 eV**(VB는 음이온 **S 지배**), **LiCl gap 6.22 eV**(우수 전자절연). LPSCl의 좁은 gap = "S의 전자전도성".
- **band gap + Li⁺장벽(6d)**: LiCl/LiF/LiI/LiBr/LiOH/Li₂CO₃/Li₂S 비교. **LiCl = 넓은 gap + 최저 Li⁺장벽 0.05 eV** → 빠른 Li 수송 buffer. + **LiCl Poisson 0.23 vs Li₂S 0.17** → 연성 LiCl-rich가 도금/탈리 부피변화 수용.

### 6.6 메커니즘 종합 (Fig 7)
- **Cl10 (비호환)**: Li 음극과 **연속 분해**(전자/이온 모두 전도하는 interphase) → 계속 진행 → dendrite.
- **Cl15 (호환)**: 4d Cl 자기분해 → **LiCl-rich interphase**(이온전도 + **전자절연**) → 추가분해 차단 + Li⁺ 통과 + 연성으로 부피변화 수용 → **낮은 R_inter, dendrite 억제**.

## 7. 전체 논증 흐름
Fig1(Cl이 4d 점유→σ↑·구조) → Fig2(음극 대칭/풀셀 우수) → Fig3(분해 통과전하 절반·저저항) → Fig4·5(interphase = LiCl, 4d Cl 방출 증거) → Fig6(DFT: 왜 LiCl이 좋은 buffer인가) → Fig7(연속분해 vs 자기분해-LiCl 모델).

## 8. Post-processing ★
- **NPD Rietveld** (GSAS/EXPGUI) → 4a/4d 자리별 Cl 점유율(핵심).
- **depth-XPS** (PHI Genesis, Cr Kα **5414.8 eV** = 준-HAXPES) → 계면 화학종 깊이분포.
- **ToF-SIMS** (PHI nano TOF II) → LiCl vs Li₂Sₓ 3D 분포.
- **MAS-NMR** (Bruker AVANCE NEO 400; ⁷Li 194.4, ³¹P 202.4 MHz; 25 kHz) → Li shielding, P 배위 분율(자기분해 추적).
- **DFT**: 계면 slab energy, **Bader 전하**(donor/acceptor), **PDOS gap**, **NEB(추정) Li⁺ 장벽**, **E_hull**(자리 점유별).
- 전기화학: CV 통과전하 적분, EIS 등가회로(ZView 4), 대칭/풀셀.

## 9. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`
| 항목 | Lu 2025 | 우리 | 차이 / 이유 |
|---|---|---|---|
| **band gap (PBE)** | LPSCl **1.88 eV** | comp1 2.066 / modelc 2.098 | 무질서·**Γ-only k**·slab → ~0.2 eV scatter. **σ_e와 무관** |
| LiCl gap | **6.22 eV** | (우리 미계산) | 전자절연 interphase 기준값 — 차용 가능 |
| **0V 환원 산물** | Eq1/Eq2 → Li₃PS₄+**LiCl**+Li₂S (표면 자기분해) | modelc 0V → **Li₃P+Li₂S+LiCl** | 우리 건 *완전*환원(Li₃P), Lu Eq1은 *부분*(Li₃PS₄ 잔존). **LiCl 생성은 공통** |
| 계면에너지 | Li/LPSCl −2.68 등 (slab) | 미계산(우리 bulk만) | 우리가 **못 하는 계면 slab** — gap H |
| Bader | 계면 P+2.05/S+0.47/Cl−0.57 | 우리 bulk Bader/CDD | 우리 CDD(중성기준)와 부호규약 다름 — 직접비교 주의 |
| Li⁺ 장벽 (LiCl) | **0.05 eV** | 우리 AIMD는 *SE bulk* Ea(0.224) | interphase NEB는 별개 — 향후 |
| 방법 | VASP/PBE, Γ-only, slab | VASP/PBE, denser k, bulk+AIMD | 큰 틀 동일 |

## 10. 적용 인사이트 (내 연구에 어떻게)
1. **음극 축(§E)의 Cl-rich '유리' 근거**: Lu는 "Cl-rich가 음극에 *유리*"의 강한 실험+DFT 패키지(LiCl passivation). 우리 deck의 음극 슬라이드에서 **modelc(Cl-rich)의 0V 환원이 LiCl을 내놓는다**는 우리 결과를, "LiCl=전자절연 passivation(Lu Fig6c, 6.22 eV)"으로 **해석**할 수 있게 됨.
2. **"Cl 양 vs Cl 자리" 프레임**: Lu의 진짜 메시지는 조성이 아니라 **4d 점유**. 우리 modelc(Li5.4PS4.4Cl1.6)도 Cl-rich라 4d 점유가 높을 것 → Lu의 LiCl-passivation 시나리오에 부합. (우리 구조의 4a/4d Cl 분포를 명시하면 Lu와 직접 연결)
3. **interphase descriptor 차용**: "interphase 품질 = (전자 gap 넓음) + (Li⁺장벽 낮음) + (연성 Poisson)" 3지표(Fig 6d). 우리 cascade(도판트/interphase 스크리닝) 평가지표로 그대로 사용 가능 — Ke의 binding-energy descriptor와 묶어 음극 interphase 평가 셋 완성.
4. **GG와의 화해를 deck에 명시**(§13): "음극엔 Cl-rich 무조건 유리"가 아니라 "**전자절연 passivation(LiCl)이 형성되면** 유리; 형성 여부는 **Cl 자리(4d)**가 좌우" — 축 명명 정신과 일치.
5. **slide 25(전자전도) 보강**: Lu의 LPSCl gap 1.88 = 우리가 slide 25에서 쓴 [Lu] 값의 *출처*. "1.88 vs Ma 2.10은 model scatter, σ_e와 무관"(comparison §D) 결론 유지.

## 11. 인용 가능 문장 (deck/paper용)
- "On the **anode side**, Cl-rich argyrodite is *beneficial*: high 4d-Cl occupancy (90.01 %, Cl15) self-decomposes into a **LiCl-rich interphase** that is electronically insulating (gap 6.22 eV) yet Li⁺-permeable (0.05 eV barrier), suppressing dendrites (Lu 2025, CEJ)."
- "Our Cl-rich (modelc) 0 V reduction yields **LiCl + Li₂S + Li₃P** — the LiCl component is exactly the electron-insulating passivator Lu et al. identify (DFT gap 6.22 eV) as the origin of anode compatibility."
- "The operative variable for anode compatibility is **anion-site (4d) occupancy, not Cl stoichiometry alone**: ³¹P NMR shows 4d-Cl (PCl₄) is released on cycling (41 → 36 %) to build the LiCl interphase (Lu 2025)."
- "DFT interface energies (Li/LPSCl −2.68 vs LiCl/LPSCl −0.19 J cm⁻²) explain why a LiCl buffer prevents the spontaneous Li–S bond formation that dissociates [PS₄]³⁻ at a bare Li/LPSCl contact."

## 12. 주의/한계 (over-claim 방지)
- **GG와 정면 긴장**: 같은 LPSCl1.5인데 Lu는 "자기분해 passivation→우수", GG는 "과안정→self-limiting 실패→moderate Cl이 나음". → 단정 금지, **§13 화해 프레임으로만** 인용.
- band gap **1.88 eV는 Γ-only+PBE+slab** → 절대 비교 금지(우리 2.07과 scatter 내).
- Eq1/Eq2는 **가정된 분해식**(E_hull 기반) — 실측 stoichiometry 아님. 우리 grand-potential과는 환원 조건(완전 vs 부분)이 달라 산물식 직접 일치 아님(LiCl 공통만).
- Li⁺ 장벽 0.05 eV(LiCl)는 **interphase 결정상 NEB** — 실제 비정질 SEI·입계 포함 안 함.
- 성능(CCD 0.96 등)은 **스택압(~10 MPa)·Li 두께(~100 µm)·공정 의존** → 절대치 인용 주의.

## 13. 🔑 GG ↔ Lu 화해 (음극 Cl-rich 논쟁) — 정직한 종합
| 관점 | [GG] Gil-González 2022 | [Lu] Lu 2025 | 화해 |
|---|---|---|---|
| 대상 | LPSCl1.5 (조성-평균) | **Cl15=LPSCl1.5 (4d 90 %)** | **같은 조성, 다른 자리설계** |
| 주장 | 과안정 → self-limiting ✗ → moderate Cl(1.0) 유리 | 4d-Cl 자기분해 → LiCl passivation → Cl-rich 유리 | — |
| 안정성 진단 | LPSCl1.5 "너무 안정" | high-4d-Cl **metastable(E_hull +15.2)** | **자리 분해능**이 GG의 평균관점이 놓친 불안정성 드러냄 |
| 공통 합의 | **전자절연 passivation 형성 = dendrite 억제 관건** | 동일(LiCl이 그 passivation) | ✅ **둘 다 "passivation이 관건"엔 동의** |
| 성능 | 0.25 mA cm²서 short | **CCD 0.96** | 자리설계·압력·공정 차이로 Lu가 우수 |
| **우리 결론** | "음극엔 Cl-rich 무조건 좋다 ✗" | "**4d-Cl로 LiCl passivation 되면** 좋다 ✓" | **조건부**: 전자절연 interphase(LiCl) 형성 여부가 핵심, 그건 **Cl 자리(4d)** 가 좌우 |

## 14. 기법 용어 미니사전
- **self-decomposition-induced interphase**: SE가 음극에서 *스스로* 분해해 보호막을 만드는 것. Lu의 핵심 — 분해를 막는 게 아니라 **좋은 산물(LiCl)로 분해**시켜 passivation.
- **electron shielding (전자 차폐)**: interphase가 전자절연이라 전자가 SE로 못 들어가 추가 분해를 막음.
- **4a / 4d Wyckoff site**: argyrodite F-43m의 음이온 자리. S²⁻/Cl⁻이 나눠 점유. Lu는 **4d Cl 점유**가 LiCl 방출원.
- **CCD (critical current density)**: dendrite로 단락되기 직전 전류밀도. 높을수록 음극 안정.
- **interface energy (J cm⁻²)**: 계면 형성 자유에너지. 매우 음수면 자발반응(=불안정 계면).
- **PClₙ 배위 (³¹P NMR)**: PS₄ → PS₃Cl → PS₂Cl₂ → PSCl₃ → PCl₄. Cl이 4d로 들어갈수록 PClₙ 우세.
