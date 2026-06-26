# Density Functional Theory for Battery Materials — He et al. (Energy & Environmental Materials 2019)

> slug `he2019_dft_for_battery_materials_review` · DOI `10.1002/eem.12056` · type `review (DFT methods, NOT argyrodite-specific)` · PDF `82ea256b-…13._Energy_Environ_Materials_2019_He….pdf` (16 pp) · digested `2026-06-26` · status ✅
> **저자**: Qiu He, Bin Yu, Zhaohuai Li, **Yan Zhao\*** (State Key Lab of Silicate Materials for Architectures / Advanced Tech for Materials Synthesis & Processing, **Wuhan University of Technology**; Y. Zhao also at Inst. of Technological Sciences, **Wuhan University**), *Energy Environ. Mater.* **2019**, *2*, 264–279. Received 2019-08-09, published 2019-10-15.
> **태그**: `[외부]` `methods-review`. **argyrodite 논문 아님 — DFT-for-batteries 방법론 백본 리뷰.** [우리 그룹] 아님(중국 Wuhan). 물성 4축 직접 수치비교 대상 아님(=우리 *방법*의 표준 정당화 문헌). comparison_vs_ours에는 "methods-provenance" 1줄로만.

---

## 0. 이 digest를 읽는 법 (왜 이 논문이 우리에게 특별한가)
이건 특정 재료 논문이 아니라, **"배터리 재료에 DFT를 어떻게 쓰나"의 표준 교과서형 리뷰**다. 우리 레포의 *거의 모든 계산 도구*(밴드갭/DOS, OCV·formation·convex-hull, NEB·AIMD 확산, grand-potential ESW, EOS·elastic, phonon)가 이 리뷰의 한 절(節)씩에 대응한다. 따라서 이 MD는 **"우리 방법이 표준 DFT-for-batteries 관행을 따른다"를 인용할 단일 출처**로 만든다 — 각 절마다 *(a) 리뷰가 권하는 표준* → *(b) 우리가 실제로 한 것(JSON 수치)* → *(c) 우리가 best-practice를 따르는지 / 알려진 caveat은 무엇인지* 를 정직하게 매핑한다.

> ⚠ **이 리뷰의 위상**: 2019년 리뷰라 **r²SCAN(2020) 이후**·**foundation MLIP(2023+, 우리 UMA-s-1p1)**·**최신 grand-potential 계면 도구**는 안 다룬다. SCAN(meta-GGA)·HSE06·GGA+U·NEB·AIMD-MSD·convex-hull voltage·VBM/CBM band-alignment·EOS/phonon은 전부 다룬다. 즉 우리 *정적 DFT 백본*은 완전히 커버, 우리 *MLIP surrogate*는 리뷰가 세운 "DFT 정확도 기준"을 만족해야 하는 대상으로만 연결된다.

> ⚠ **이 리뷰의 한계(우리에게 중요)**: 리뷰는 *electrode/anode/2D 재료* 예시가 대부분(NaₓMnO₂, Mg₃N₂, Mg₃Bi₂, V₂O₅, 폴리설파이드 anchoring 등). **고체전해질 ESW(grand-potential)·argyrodite·황화물 SE는 직접 예시가 없다.** 전기화학창은 **HOMO/LUMO(Goodenough) band-edge 그림(Fig 7)** 으로만 다루고 — 즉 우리가 쓰는 **grand-potential 분해창은 이 리뷰에 *없다*(Mo/Ong/Ceder 계열이 빠짐).** 이게 §7에서 가장 중요한 정직한 포인트다(우리는 리뷰가 권하는 band-edge보다 *더 엄밀한* 방법을 쓴다).

## 1. 한 줄 요약
He et al.은 배터리 재료에 적용되는 DFT를 **5개 축**으로 종설한다 — ① 구조안정성(cohesive/formation/Gibbs/phonon), ② 반응전압 OCV·이론용량(Nernst+convex-hull), ③ 전자구조(MO·band·DOS·charge), ④ 이온수송(NEB·AIMD-MSD), ⑤ 흡착(폴리설파이드 anchoring·이온저장) — 그리고 **§7에서 functional(LDA/GGA/GGA+U/HSE06/SCAN)을 벤치마크**해 "production run 전에 functional을 반드시 검증하라"고 결론한다. 핵심 정량 결론: **SCAN이 band gap·전압·DOS·구조를 PBE/PBE+U보다 균형있게 잘 주고, HSE06은 PBE+U급 정확도지만 비용이 크며, PBE는 전압을 수 십 분의 1 V 과소평가하고 gap을 ~1 eV 과소평가한다.**

## 2. 메타 / 구조
| 항목 | 내용 |
|---|---|
| 유형 | DFT 방법론 리뷰 (배터리 재료 일반: LIB·SIB·PIB·ZIB·AIB·CIB·MIB·Li-S·금속공기) |
| 범위 | electrode(양극/음극)·전해질·2D 재료·anchoring host — **고체전해질 ESW는 band-edge 그림만, grand-potential은 없음** |
| 구성 | §1 서론 → §2 구조안정성 → §3 전압·용량 → §4 전자구조 → §5 이온수송 → §6 흡착 → **§7 functional 벤치마크/권고** → §8 결론 |
| 우리 관련도 | **★★★★★** — 우리 정적 DFT 파이프라인 거의 전부의 표준 정당화. 단 우리 grand-potential ESW·MLIP은 리뷰 범위 밖(더 신·엄밀) |

---

## 3. 섹션별 상세 (DFT-for-batteries 핸드북으로서 정독)

### §1 서론 — XC functional의 세대와 "왜 functional이 핵심인가"
- DFT 정확도는 **exchange-correlation(XC) functional 품질에 좌우**된다(Kohn–Sham). 3세대 발전:
  1. **LSDA**(local spin density) — 밀도(스핀밀도)만의 함수. **lattice constant 예측은 의외로 좋으나**, 화학반응엔 부적합: **장벽(barrier)을 심하게 과소평가**하고 **화학결합을 과결합(overbind)**.
  2. **GGA**(밀도+그 gradient; **PBE**가 대표) — 화학결합에너지엔 LSDA보다 훨씬 유용. 단 여전히 **band gap·barrier height·비국소(noncovalent) 상호작용을 과소평가**.
  3. **meta-GGA**(kinetic energy density / spin Laplacian; **SCAN**) — 그리고 **HF exchange를 섞은 hybrid(HSE)** = band gap엔 더 정확하나 고체물리선 비용 때문에 덜 흔함.
- **배터리 재료의 주류 = GGA, 특히 PBE.** DFT는 열역학·전자구조·반응·수송경로를 계산하며, 실험 대비 **원자 수준 메커니즘 규명 + 가상 스크리닝**의 강점.
- 문헌 분포: 다수는 실험 중심+DFT 보조검증, 일부는 순수 이론, 일부는 동등 비중.
> **우리 매핑**: 우리 백본 = **PBE(QE) + GGA/GGA+U(MP hull)**. 리뷰의 "배터리 = PBE 주류" 서술이 우리 functional 선택의 표준 근거. (단 우리는 gap엔 PBE의 ~1 eV 과소를 명시; §7-D.)

### §2 구조안정성 (4가지 에너지 지표)
리뷰가 구조안정성을 보는 4지표를 *언제 무엇에 쓰나*까지 정리:

**§2.1 Cohesive energy** `E_co = [m·E(A) + n·E(B) − E(AₘBₙ)] / (m+n)` (Eq 1)
- 고립 *원자* 기준. 클수록 안정. 예: COF(NUS-2) anode가 Li 14개 흡착 후에도 cohesive E 4.6 eV/atom 유지 = 높은 열역학 안정성+큰 Li 저장.
- **0 K 안정성 평가용.**

**§2.2 Formation energy** `E_f = [m·E(A) + n·E(B) − E(AₘBₙ)] / (m+n)` (Eq 2), 단 E(A),E(B)는 **원소의 표준상태**(고립원자 아님)
- 더 양(+)일수록 안정. **cohesive보다 실용적**(화합물은 고립원자가 아니라 원소상태서 합성되므로). 예: 2D SiGe formation E = 1.51 eV/unit cell → 양호한 열역학 안정성.
- **포인트**: 0 K 안정성엔 formation E가 cohesive보다 나은 descriptor.

**§2.3 Gibbs free energy** `G = H − TS`, `H = E + PV` (Eq 3,4)
- isomer/polymorph를 **유한 T·P에서** 비교. 예: Na₂FeSiO₄ 14개 구조모델 → P_b phase가 저T·저P 최저, ~700 °C/8 GPa서 Pca2₁로 전이(Fig 1).

**§2.4 Phonon frequency**
- n원자 셀 → 3 acoustic + 3n−3 optical 분지. **허수(음의) frequency = 동역학 불안정.** 예: Pmma-XO(X=C,Si,Ge,Sn) monolayer 중 CO/SiO/GeO는 허수 없음(안정), SnO는 G점 근처 음의 frequency(불안정)(Fig 2). 최고 optical frequency(CO 1200·GeO 775 cm⁻¹)가 phosphorene(~450)·MoS₂(~500)보다 높음 → 더 강한 결합.
- **계산비용 큼** → 작은 계나 큰 계의 일부만.
> **우리 매핑**: 우리는 **phonon을 *현재* 안 돌림**(EOS·elastic eigenvalue 양수로 기계적 안정성 확인; 동역학 phonon 안정성은 미실시). cohesive/formation E도 우리 메인 라인 아님(우리 0K 안정성 = MP convex-hull E_above_hull + grand-potential). **→ §H "우리가 아직 안 하는 것"에 phonon 추가 후보.** (리뷰: phonon 비용 커 일부만 — 우리가 안 한 게 비표준은 아님.)

### §3 반응전압·이론용량 (Ceder식 평균전압 — 우리 OCV/ESW의 뿌리)
**§3.1 원리.** 일반 전기화학반응 `αA + βB → γC + δD` (Eq 5)의 Gibbs 변화 `Δ_rG = γΔ_fG_C + δΔ_fG_D − αΔ_fG_A − βΔ_fG_B` (Eq 6). 평형(Nernst) `Δ_rG = −nFE` (Eq 7) → **전압 = −Δ_rG/nF**.
- 고체상은 PV·TS 항 무시 가능 → **Δ_rG⊖ ≈ ΔE_r**(DFT total energy 차) (Eq 8). 즉 **평균전압을 DFT 총에너지만으로** 얻음(=Ceder/Aydinol 1997 average-voltage).
- 이론용량 등: 질량/부피 에너지밀도 ε_m=Δ_rG/ΣM, ε_v=Δ_rG/ΣV (Eq 9,10), 비용량 **C = nF/3.6m** (Eq 11).

**§3.2 위상(phase) & convex hull.** OCV는 **formation-energy convex hull**과 직결:
- 고용체(solid-solution) 단상 → 자유도 1 → 전압 **연속 감소**(Fig 3a,d).
- 1차 상전이(Li-poor↔Li-rich 2상 공존) → 자유도 0 → 전압 **평탄(plateau)**(Fig 3b,e).
- 중간 안정상 존재 → **다단 plateau**(Fig 3c,f). (Fig 3 = Goodenough/Kim 2010 식 자유에너지-전압 짝.)
- 예: **Na₀.₄₄MnO₂** SIB — 7개 안정상 + GGA+U 전압이 실험 plateau와 일치, Na 추출자리까지 식별; 용량열화 = Na 확산장벽 큼(Fig 5). **CaₓSn₁₋ₓ**(CIB) — Sn-Ca convex hull → calciation 전압·부피팽창·중간상(Ca₇Sn₆ 527 mAh/g) (Fig 6).
> **우리 매핑 (핵심)**: 우리 **grand-potential ESW = 이 §3 convex-hull voltage의 "open-system(μ_Li 가변)" 확장**이다.
> - 우리 OCV 1.717 V·환원 1.24 V·산화 onset 2.14 V(또는 LiS4 제외 2.256 V)는 **MP GGA/GGA+U hull 위에서 `get_element_profile`(Li chempot scan)** 로 — 즉 리뷰 §3가 *닫힌* 반응(Eq 6,7)으로 평균전압을 주는 것을, 우리는 *열린* 계(Li 저장소를 열어 μ_Li 스캔)로 **분해창**까지 확장. 리뷰 §3가 우리 전압계산의 *열역학 근간*(Δ_rG=−nFE)을 정당화.
> - **단 정직한 갭**: 리뷰는 SE 분해창 = **HOMO/LUMO band-edge 그림(Fig 7, §4.1)** 으로만 본다. **Mo/Ong/Ceder grand-potential은 이 리뷰에 없다.** 우리 ESW 방법의 1차 출처는 이 리뷰가 아니라 Ong2008/Mo2012/Schwietert2020(별도, `oxidation_stability_VBM_vs_grandpotential_report` §7·11). → 리뷰는 *Nernst 근간*만, *grand-potential 절차*는 아님. 인용 시 "average-voltage 근간 = He review §3" + "grand-potential 절차 = Mo2012" 둘 다 명시.
> - GGA+U 전압이 NaₓMnO₂ 실험과 일치(Fig 5)·우리 MP hull도 GGA/GGA+U pinned → **우리가 TM-free 황화물이라 U 불필요**한 점(§7-A)이 오히려 우리 전압이 U 모호성에서 자유로움을 의미.

### §4 전자구조 (MO·band·DOS·charge — 우리 electronic.json 직접 대응)
**§4.1 Molecular orbitals & 전기화학창(Goodenough 그림, Fig 7).**
- 좋은 전해질: **HOMO < cathode μ_C** *그리고* **LUMO > anode μ_A** (안 그러면 산화/환원). E_g(전해질 gap)가 V_oc 상한을 가르며, **SEI가 형성되면 이 조건을 완화**(전자전달 차단). DFT HOMO/LUMO로 전해질-전극 호환성 검사.
> **우리 매핑 (가장 중요한 정직 포인트)**: Fig 7은 **band-edge(VBM/CBM·HOMO/LUMO) 기반 안정창**이다. **우리는 일부러 이 방법을 *주력으로 쓰지 않는다.** 우리 `oxidation_stability_VBM_vs_grandpotential_report`가 정확히 이 점을 다룸: 고체 SE에서 산화 = "전자 1개 제거(HOMO)"가 아니라 **상 분해** → **band-edge 창은 실제 분해창을 2–3배 과대평가**(Schwietert 2020). 우리 직접 증거: **comp1·modelc는 절대 VBM이 +0.32 eV 다른데 산화 onset은 둘 다 2.14 V로 동일**(S²⁻-limited). → 즉 **리뷰의 Fig 7 band-edge 그림은 "band alignment/전자적 계면 안정성"에만 쓰고, "분해 전압"엔 grand-potential을 쓴다**가 우리 입장. 리뷰가 옛 표준(band-edge)을, 우리가 신 표준(grand-potential)을 대표 — *우리가 리뷰보다 엄밀.*

**§4.2 Band structures.** gap이 전도성·전기저항을 가른다. 예: **Mg₃N₂**(LIB anode) PBE gap 0.91 eV(반도체)→리튬화 후 Li₂Mg₃N₂ metallic(전도성↑); **PBE가 gap 과소** → **HSE06로 재계산해 1.92 eV(PBE보다 ~1 eV↑)**(Fig 8). **pg-CN**(2.0 eV)에 a-CB 코팅 → 구조안정+전도성 유지.
> **우리 매핑**: 이게 우리 밴드갭 caveat의 *교과서 근거*다 — **"PBE가 gap을 ~1 eV 과소, hybrid가 보정"**. 우리 comp1 PBE gap = **2.066 eV**(eigenvalue), modelc **2.099 eV**(`electronic.json eigenvalue_gaps_v100`); 문헌 PAW-PBE는 ~2.15–2.45, HSE06는 3.30(Semi 논문). 우리도 같은 "PBE 과소" 사실을 안고 있어 **절대 gap 직접비교 금지, "wide-gap insulator"로만**. comp1↔modelc Δ=+0.033 eV는 일관된 PBE라 *상대비교는 valid*. (리뷰가 "PBE 과소→HSE 보정"을 명시하므로 우리 caveat은 비표준 변명이 아니라 표준 인지.)

**§4.3 Density of states.** DOS = 단위에너지·부피당 상태수. PDOS로 원소·궤도 기여. 예: NCM523 Mo 도핑 → Ni²⁺ PDOS↑/Ni³⁺↓(charge compensation), Mo⁶⁺ 전도대가 E_F 근처서 전도성↑(Fig 9). **Mg₃Bi₂**: VB top이 Bi 6p에서 시작, Bi 6s–6p 큰 gap = 화학적 불활성(Fig 10). **DFT+U/HSE/SCAN 비교(Fig 11, LiNiO₂/LiCoO₂/LiMnO₂)**: TM-O 강한 혼성; **PBE는 metal-d를 E_F 근처서 과소, SCAN이 더 정확, PBE+U는 O 2p를 과대**. 저스핀(LiNiO₂ Ni³⁺ t₂g⁶eg⁰)·고스핀(LiMnO₂ Mn³⁺) 구분.
> **우리 매핑**: 우리 **PDOS로 VBM=S 3p(91–93%), CBM=S 3p(42–45%)+P 3s(25–27%)+Li 2p(13–14%)** 식별(`electronic.json comp1_v3/modelc_v3`) — 정확히 §4.3의 PDOS 용법. **HAXPES VBM=S 3p**(Banik)와 일치 = 실험검증. Nd 도핑 PDOS 분석(VBM 여전히 S 3p host, Nd 4f gap 밖 −7.4/+1.9, Nd 5d/6s가 CBM을 끌어내림 0.55 eV)도 §4.3 PDOS 추적과 동형. **Bader charge**(우리 `bader_full_matrix`: Li +0.877, P +4.686, S −1.807, Cl −0.914)·**ELF**(P–S bridge 0.946 vs Li basin 0.07 = ~13× 대비)·**charge distribution**(CDD)도 §4.4에 대응.

**§4.4 Electronic/charge distribution.** charge density difference(CDD)로 결합형성·전자이동 시각화. 예: MoSe₂-SnO₂ 계면서 Se→O 전자이동(Fig 12), V₂O₅·nH₂O서 Zn²⁺ 삽입 시 Zn→V/O 이동(Fig 13).
> **우리 매핑**: 우리 CDD(slide 24)·ELF(slide)가 정확히 이것. 우리 Q&A 로그(comparison §Q&A Q2)가 CDD를 "중성원자 대비 재배치"로 해석 = §4.4 표준 용법.

### §5 이온수송 (NEB·AIMD — 우리 li_transport.json 직접 대응)
- 이온확산이 rate·cycle·구조안정성 지배. **NEB(+CI-NEB)** 로 확산경로 따라 **활성화장벽 E_a** 계산.
- 예: **LiMn₂O₄(LMO)** 나노입자(<5 nm)서 오히려 성능 악화 — DFT+NEB로 bulk E_a 0.33 eV → 14→1.4 nm 나노입자서 **0.59 / 0.72 eV로 상승**(Fig 14) = 작은 입자가 확산 방해. **N-doped CNT**(Li-S host) Li 통과장벽(Fig 15). **Nb₂O₅**: path A/B E_a 0.33 / 0.25 eV → 이방성 초이온전도 설명(Fig 16).
- **AIMD**: NEB는 *한 경로 장벽*만 주지만, **AIMD는 확산계수 D·이온전도도 σ까지** 줌(실험 검증가능). 단 **계산비용 큼**(수백 원자, ~수십~수백 ps), 보통 고온서 통계.
> **우리 매핑 (best-practice 일치)**: 우리 수송 = **AIMD(foundation MLIP UMA-s-1p1) + MSD→D + Arrhenius→Ea + Nernst-Einstein σ** (`li_transport.json`). 정확히 §5의 AIMD 노선:
> - **MSD=6Dt**(diffusive regime), **ln D = ln D₀ − Ea/kT**, **σ_NE = n_Li z²e²D\*/kT**(H_R=1) — 리뷰 §5의 "AIMD가 D·σ 준다"의 표준 구현.
> - 결과: comp1 **Ea=0.2532 eV**(Schlem 2020 실험 ~0.25와 0.003 eV 일치★), modelc **Ea=0.2235 eV**, D(600K) 3.09→7.90×10⁻⁶ cm²/s. Cl-rich가 Ea↓·D↑(무질서+vacancy) = 리뷰가 강조하는 "구조가 장벽을 가른다"(LMO 나노입자 0.33→0.59 eV와 동형의 *구조-장벽 커플링*).
> - **우리가 리뷰보다 *나아간* 점**: 우리는 NEB(단일경로) 대신 **AIMD로 D·σ 직접**(리뷰가 "AIMD가 더 정보 많다"고 명시한 노선). 추가로 **BVSE**(bond-valence site energy, 빠른 bottleneck/경로 스크리너)를 cascade 전처리로 — 이건 리뷰 범위 밖(2019 이후 보편화)이나 NEB 정신의 경량판.
> - **우리 caveat(정직)**: ① **foundation MLIP은 DFT가 아니라 surrogate** — UMA가 LPSCl에서 Li 확산을 **실험 대비 3–5× 과대**(`li_transport.json caveats`). 그래서 **절대 σ(~14 mS/cm)는 인용 금지, Ea·ratio만 robust.** ② 600–1000 K Arrhenius의 300 K 외삽 불확실. ③ Nd 도핑은 **UMA 4f 전이성 미검증** → ratio(nd/modelc D 0.62×)만, 절대 σ 금지. → **리뷰의 "AIMD는 정확하나 비용 크다"가, 우리에겐 "MLIP로 비용은 줄였으나 *DFT 정확도를 만족하는지*가 새 부담"으로 치환됨**(§5-MLIP 항).

### §6 흡착 (폴리설파이드 anchoring·이온저장 — 우리엔 *간접* 관련)
- Li-S "shuttle effect" 억제 = 폴리설파이드를 host에 강하게 **anchoring**. DFT 흡착에너지로 정량. 예: 2D anchor(V₂O₅·MoO₃ 최강; ZnCl₂ 약)와 폴리설파이드 결합(Fig 17); **vdW 보정 필수**(리튬화 진행 시 물리흡착→화학결합)(Fig 17b). ZnFe₂O₄·CoTe₂·N-doped graphene·Si 클러스터 흡착(Fig 18,19,20). DFT+U(ZnFe₂O₄), Δ 정의(Eq 12).
> **우리 매핑(약함, 정직)**: 우리는 Li-S 양극 호스트가 아니라 **SE bulk**라 §6 anchoring은 *직접* 대상 아님. **단 두 접점**: (a) 우리 **interface_reactivity**(SE/cathode 분해산물 Co₉S₈+Li₃PO₄+Li₂S+LiCl)는 §6보다 §2/§3(formation·hull) 계열이지 흡착이 아님. (b) 리뷰의 **"vdW 필수"** 경고는 우리 elastic/EOS에서 **PBE vs PBE-D3** 절대값 차이(문헌 JPCC D3가 E 27.4 vs 우리 PBE relaxed-ion 22.06)를 설명하는 표준 근거(§7-C). → §6 자체는 우리 인용대상 거의 아님; vdW 경고만 차용.

### §7 ★ functional 벤치마크/권고 (이 리뷰의 클라이맥스 — 우리 functional 선택의 정당화)
리뷰의 결론절. **"production run 전에 functional을 반드시 검증하라. popular하다고 맹목 사용 금지."** 정량 벤치마크:

**(1) LDA/GGA의 한계 — 전압 과소.** 전자상관 부실. **전기화학 반응전압을 수 십 분의 1 V 과소평가**(Cococcioni). delocalized 전자의 self-interaction이 redox E를 낮춤. 금속 Li는 self-interaction 작으나 **TM의 localized d 전자는 큼** → 전압 과소.

**(2) DFT+U.** Kohn-Sham 궤도의 분수점유를 낮춰 self-interaction 교정. **GGA+U가 GGA보다 리튬화 전압 훨씬 정확**(Fig 21a, LiₓMPO₄). **단 U는 semi-empirical·system-dependent**, 그리고 **TM의 원소상태(metal)엔 U 적용 불가** → **산화물 formation E엔 GGA+U보다 GGA가 나음**(Wang). (Fig 21b: LiCoO₂·LiNiO₂·LiTiS₂… GGA(과소 ~−0.6~−1.2 V) vs GGA+U(±0.3 V) vs HSE06.)

**(3) HSE06(hybrid).** screened HF exchange로 self-interaction 교정. **formation E·부피·Li 삽입전압 정확도 GGA+U급**(Chevrier; LiMO₂·LiMPO₄·LiMn₂O₄). 산화물선 HSE06가 GGA+U보다 O에 더 많은 charge·더 높은 전압. polyanion(LiFePO₄)선 P 참여로 HF 효과 약화 → GGA+U와 유사. **비용은 GGA+U보다 훨씬 큼**(특히 대형계).

**(4) SCAN(meta-GGA) — 리뷰의 추천.** Chakraborty가 PBE/PBE+U/SCAN을 LiNiO₂·LiCoO₂·LiMnO₂서 비교(Fig 11): **SCAN이 band gap·절대전압을 PBE보다, DOS·반응전압을 PBE+U보다 잘 줌. 전자밀도·in-operando 격자상수도 SCAN 우월.** 이유: 향상된 functional form + 중거리 분산 기술. 단 **Isaacs: SCAN은 약결합 화합물(intermetallic)의 formation E 오차가 PBE보다 큼.**

**(5) 종합 권고.** 일반적으로 **에너지 관련(전압 등) 계산엔 LDA/GGA보다 SCAN/HSE06.** Li 폴리설파이드(Li₂Sₙ) atomization E 벤치(LiSAE38, WMS법): **PW6B95·B97-1·B3LYP-D3·TPSS·DSD-PBEP86가 가장 정확**; 절대 atomization엔 mPW2-PLYP-D·DSD-PBEP86·PBEQIDH; 상대안정성엔 MN15-L·revM06-L.

> **우리 매핑 (§7 전체 = 우리 functional 선택의 정당화 + 정직한 caveat)**:
> - **우리 백본 = PBE(QE, USPP/RRKJUS 또는 ONCV) + MP GGA/GGA+U hull.** 리뷰는 "배터리 = GGA 주류"라 **표준 범위 안**. 우리는 **r²SCAN/HSE를 *gap 절대값*엔 안 씀** → 그래서 gap을 "wide-gap insulator"로만 보고 절대비교를 피함(리뷰 §4.2가 정확히 그 이유=PBE 과소 제시).
> - **GGA+U**: 우리 주재료(LPSCl/modelc)는 **TM-free 황화물 → U 불필요**(S 3p·P 3s·Li 2s, localized d 없음). 리뷰의 "U는 TM-localized-d 교정용"에 비춰 **우리가 U를 안 쓰는 게 옳다**(억지로 넣으면 오히려 오류). **예외: Nd 도핑** — 우리는 **DFT+U(Nd 4f, U=8 eV)+nspin2 AFM**(`electronic.json Nd2O3_doped`) — 정확히 리뷰가 권하는 "localized f/d엔 +U". 단 우리 스스로 **"4f-U 민감, gap 절대값 ±, trend robust"** 라 caveat(리뷰의 "U는 semi-empirical"과 일치).
> - **MP hull은 GGA_GGA+U로 pinned**(`oxidation_stability.json method`: "avoids R2SCAN mixing noise, matches Mo/Ong literature numbers"). → 리뷰의 "전압엔 GGA+U" + Wang의 "산화물 formation엔 GGA"의 *혼합 문제*를 MP의 mixing scheme이 처리; 우리가 R²SCAN mixing을 *피한* 것은 리뷰 §7-(4)의 "SCAN intermetallic formation 오차(Isaacs)"와 같은 결의 보수적 선택.
> - **정직한 caveat(우리가 best-practice를 *완전히는* 안 따르는 지점)**: 리뷰의 *추천*은 "에너지엔 SCAN/HSE06". 우리 hull은 **GGA/GGA+U**(SCAN 아님). 이유는 (a) MP literature 정합·Mo/Ong 수치 재현, (b) R²SCAN mixing noise 회피 — 즉 *정당한 trade-off*이나, "리뷰의 1순위 추천(SCAN)을 따르지 않았다"는 점은 명시해야 정직. 우리 ESW 절대 onset의 ±0.x V 불확실(GGA 한계)은 이 선택의 알려진 비용(상대비교·실험창 정합은 robust로 방어).

---

## 4. Figure set ★ (방법 그림으로서 — 우리가 *방법론적으로* 참고할 점)
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 (방법론) |
|---|---|---|
| 1 | Na₂FeSiO₄ 자유에너지 vs T(a)·P(b) — polymorph 상전이 | Gibbs G(T,P)로 polymorph 비교 = 우리 modelc Li-basin/Cl-자리 다형 비교의 표준틀(우리는 0K E + MLIP anneal로 대용) |
| 2 | Pmma-XO phonon 분산 — 허수 frequency=불안정 | **동역학 안정성 phonon 판정**. 우리는 미실시(elastic eigenvalue 양수로 *기계*안정만) → §H 후보 |
| 3 | 자유에너지 vs Li 농도 → 전압 프로파일(단상 연속/2상 plateau/다단) | **convex-hull↔전압 짝의 교과서 그림**. 우리 grand-potential staircase(2.14/2.36/3.06 V…)가 바로 이 다단 plateau의 open-system판 |
| 4 | 2D AlN Li/Na 흡착E·OCV (PBE) | OCV=흡착E≈Δ_rG (Eq 8) 구현 예. SIB가 LIB보다 OCV↑ |
| 5 | NaₓMnO₂ formation E convex hull + 전압(계산 vs 실험, GGA+U) | **GGA+U 전압이 실험 plateau·추출자리 재현**. 우리 MP GGA+U hull 정합의 외부 근거 |
| 6 | CaₓSn₁₋ₓ convex hull·전압·부피팽창·중간상 | convex-hull로 중간상·부피팽창 추적 = 우리 분해 staircase 산물추적과 동형 |
| **7** | **Goodenough HOMO/LUMO 전기화학창**(E_g·μ_C·μ_A·SEI) | **★ band-edge ESW 그림 — 우리가 *대체*하는 방법.** 우리 grand-potential이 이걸 2–3× 과대 문제 없이 대체(report §3–8). 인용 시 "band alignment용으로만" |
| 8 | Mg₃N₂ DOS·band (PBE vs HSE06, gap 0.91→1.92) | **★ PBE gap ~1 eV 과소 → HSE 보정**의 직접 수치. 우리 gap caveat 근거 |
| 9 | NCM523 Mo 도핑 DOS(charge compensation) | 도핑 PDOS 추적 = 우리 Nd 도핑 PDOS(host-band shift) 분석틀 |
| 10 | Mg₃Bi₂ DOS·band(PBE vs HSE06, SOC) | 중원자 SOC 효과·hybrid gap. 우리 Nd(중원자) 계산 시 SOC 고려 단서(현재 미적용) |
| **11** | **LiNiO₂/LiCoO₂/LiMnO₂ DOS — PBE vs PBE+U vs SCAN** | **★ functional별 d/O 위치 차이의 결정적 그림.** SCAN 추천 근거. 우리 TM-free라 U 불필요 판단의 대조군 |
| 12–13 | MoSe₂-SnO₂·V₂O₅ CDD(전자이동) | CDD 표준 용법 = 우리 slide24 CDD |
| 14 | LMO 나노입자 NEB E_a(0.33→0.59/0.72) | NEB 장벽·구조-장벽 커플링 = 우리 AIMD Ea(Cl/무질서가 장벽 가름) |
| 15–16 | N-CNT·Nb₂O₅ NEB(이방성 0.33/0.25) | NEB 다경로 = 우리 BVSE/AIMD 경로 |
| 17–20 | 폴리설파이드/이온 흡착(vdW 필수) | **vdW 보정 필수** 경고만 차용(우리 PBE vs D3 elastic 절대값차 설명) |
| **21** | **LiₓMPO₄ 전압오차 GGA vs GGA+U vs HSE06** | **★ GGA 전압 과소(−0.6~−1.2 V)·+U/HSE 보정**의 정량. 우리 GGA+U hull 전압 신뢰의 근거 + "GGA 절대 onset ±0.x V" caveat 근거 |

## 5. DFT/계산 방법 ★ (리뷰가 *권하는* 표준 — 우리 설정과 대조용)
이 리뷰엔 *고정 production 설정*이 없다(방법 종설이라). 대신 리뷰가 명시·암시하는 표준:
- **code/functional**: VASP/QE류 평면파+PAW, **GGA-PBE 주류**; gap/redox 정밀엔 **HSE06**, TM-d엔 **GGA+U**, 균형엔 **SCAN**.
- **pseudo**: PAW 또는 norm-conserving(예: 2D AlN OCV에 Troullier-Martins NC).
- **k-points/ecut**: 리뷰가 수치 권고는 안 함(케이스별). 단 §7이 *functional* 수렴/검증을 강조.
- **DFT+U**: TM/f-전자 localized에만. U는 system-dependent → 검증 필수.
- **AIMD**: 수송(D·σ)용, 고온·수백원자·~수십~수백 ps. NEB는 단일경로 장벽.
- **vdW(D3 등)**: 흡착·층상·약결합에 필수.
- **무질서 처리**: 리뷰는 SQS를 명시하진 않으나(electrode 예시 중심), polymorph는 다중 구조모델 비교(Na₂FeSiO₄ 14개).
> **우리 실제 설정(대조)**: QE 7.4.1 PBE(USPP/RRKJUS 52/520 Ry, k=6×6×6 또는 8×8×8 nscf; ONCV 80/320 Ry for ELF) / MP GGA_GGA+U hull / **UMA-s-1p1 MLIP**(AIMD surrogate, Langevin NVT 600-1000 K, 2 fs, 100 ps) / Nd엔 DFT+U(4f, U=8) AFM / **무질서 = anti-site Cl/S decorate + Li-vacancy 단일 또는 ensemble**(SQS 아님, enumerate/decorate). → 리뷰 표준과 **정합**; 차이는 (a) 우리가 **MLIP surrogate**를 씀(리뷰엔 없음, 2019 이후), (b) gap엔 SCAN/HSE 대신 PBE+명시적 caveat.

## 6. Post-processing ★ (리뷰가 다루는 후처리 ↔ 우리 도구)
| 리뷰 후처리 | 우리 도구(repo) | 우리 기록 |
|---|---|---|
| convex hull·전압(Δ_rG=−nFE) | pymatgen PhaseDiagram + **`get_element_profile`**(grand-potential 확장) | `oxidation_stability.json` OCV/onset·반응식 staircase |
| DOS/PDOS·band·gap | QE **dos.x + projwfc.x**, eigenvalue gap(literature convention) | `electronic.json` gap·VBM/CBM 성분·EF |
| charge(CDD)·Bader·ELF | QE **pp.x**(plot_num 0/8) + Bader(Henkelman) | `electronic.json` bader_full_matrix·elf_comparison_v3 |
| NEB E_a | (우리 NEB 미사용) **BVSE**(경량) + **AIMD MSD→D→Ea** | `li_transport.json` Ea·D·σ_NE |
| AIMD D·σ | **UMA-s-1p1 MLIP-MD** + Nernst-Einstein | `li_transport.json` Arrhenius·σ_NE(H_R=1) |
| phonon(동역학 안정) | **미실시** | — (§H 후보) |
| elastic/EOS(리뷰 §2 안정성의 일부 아님 — 별도이나 우리 핵심) | QE 유한변형 stress-strain Cij + BM3 EOS | `elastic.json`·`eos.json` |
> 우리 ELF/COHP(LOBSTER ICOHP)·constrained-ESW(Fitzhugh)·interface_reactivity는 **리뷰 범위 밖의 신·심화 후처리**(리뷰는 CDD까지). → 우리 post-processing이 리뷰를 *상회*.

---

## 7. 우리 DFT 대비 — 절별 best-practice 체크 (→ `our_dft_baseline.md`)
> "이 논문 값 vs 우리 값"이 아니라(방법 리뷰라 비교할 단일 수치 없음), **"리뷰의 권고 ↔ 우리 실제 계산이 따르나 / caveat은?"** 의 체크리스트.

| 축 | 리뷰의 표준/권고 | 우리 실제 (JSON 수치) | 따르나? / caveat |
|---|---|---|---|
| **functional 일반** | 배터리=GGA-PBE 주류; 에너지엔 SCAN/HSE06 권장 | PBE(QE) + MP GGA/GGA+U hull | **부분 ✓** — PBE 백본은 표준; **gap·전압 정밀의 1순위(SCAN)는 미채택**(GGA+U hull, MP 정합·R²SCAN noise 회피 trade-off). 정직히 "리뷰 1순위 미사용" |
| **band gap (D)** | PBE gap ~1 eV 과소 → HSE06 보정(Fig 8: 0.91→1.92) | comp1 2.066 / modelc 2.099 eV (PBE eigenvalue); HSE 미실시 | **✓ caveat 인지** — "PBE 과소"는 리뷰가 보증. 절대 gap 비교 금지·"wide-gap"만; Δ(comp1↔modelc)=+0.033은 일관 PBE라 *상대* valid. **Nd 4f-U 민감**(gap 절대 ±, trend robust) = 리뷰 "U semi-empirical"과 일치 |
| **전압/ESW (B)** | 닫힌계 average-voltage(Δ_rG=−nFE, Eq 7); SE 창은 band-edge(Fig 7) | grand-potential `get_element_profile`(열린계 μ_Li scan): OCV 1.72·환원 1.24·산화 onset 2.14(LiS4제외 2.256) V | **✓✓ 우리가 *더 엄밀*** — 리뷰의 band-edge(Fig 7)는 분해창 2–3× 과대(Schwietert); 우리 grand-potential이 실험 CV 창 재현(GG K_eff=0 1.70–2.40 정합). 단 **grand-potential 절차는 이 리뷰가 아니라 Mo2012 출처**(리뷰는 Nernst 근간만). **GGA hull → 절대 onset ±0.x V**(Fig 21 GGA 전압 과소와 같은 결) |
| **migration (A)** | NEB(단경로 E_a) + AIMD(D·σ, 비용 큼) | UMA-MLIP AIMD: Ea comp1 0.2532/modelc 0.2235 eV·D(600K) 3.09→7.90e-6·σ_NE | **✓ best-practice(AIMD 노선)** — 리뷰가 "AIMD가 D·σ까지" 권한 그대로. Ea가 Schlem 실험 0.25와 0.003 eV 일치★. **caveat: MLIP≠DFT** — UMA가 σ 3–5× 과대 → **절대 σ 금지, Ea·ratio만**; Nd는 4f 전이성 미검증(ratio만) |
| **mechanical (C)** | vdW 필수(약결합); functional/ion-relax로 절대값 변동 | EOS B0 comp1 26.23/modelc 21.71 GPa; relaxed-ion E_VRH 22.06→27.66 GPa; clamped 52.31(vacancy paradox) | **✓ 정직 노출** — 리뷰 §2엔 elastic 직접 없으나 vdW 경고가 우리 PBE(22.06) vs 문헌 D3(27.4) 차이 설명. **relaxed vs clamped-ion이 2.4×**(우리 vacancy paradox) = 리뷰 "ion-relax 중요"의 극단 사례 |
| **phonon(동역학)** | 허수 frequency=불안정(비용 커 일부만) | 미실시(elastic eigenvalue 양수=기계안정만) | **△ 미실시이나 비표준 아님** — 리뷰도 "비용 커 일부만". 동역학 안정성 원하면 phonon 추가(§H) |
| **무질서** | polymorph 다중모델 비교(SQS 명시 없음) | anti-site decorate + Li-vac (enumerate/ensemble), SQS 아님 | **✓ 합리적** — 리뷰가 SQS를 요구하진 않음; 우리 disorder ensemble(Ea 0.177±0.027 @disorder 0.5)이 다중모델 정신 |
| **MLIP surrogate** | (리뷰 범위 밖 — 2019 이전) | UMA-s-1p1을 DFT 대용으로 AIMD·elastic·EOS | **신영역** — 리뷰가 세운 **DFT 정확도 기준이 우리 MLIP이 넘어야 할 바**. 교차검증: **Nd₂O₃ B0 UMA 18.9 vs cascade DFT-pending 19.9**(≈1 GPa) = MLIP가 EOS선 DFT급; 단 **σ는 3–5× 과대**(Ea만 신뢰) → "MLIP는 EOS/Ea OK, 절대 D/σ는 DFT 기준 미달" |

## 8. 적용 인사이트 (우리 연구·deck에 어떻게)
1. **"우리 방법이 표준 DFT-for-batteries 관행을 따른다"의 단일 인용처.** Methods 섹션·deck에서 밴드갭(PBE)·DOS/PDOS·OCV(Nernst·hull)·AIMD 확산·elastic 각각에 He2019를 표준 근거로. 절별 매핑(§7)이 그대로 Methods 정당화.
2. **gap caveat의 교과서 방패(slide 21/24/25).** "PBE가 gap을 ~1 eV 과소, hybrid가 보정"(Fig 8, Mg₃N₂ 0.91→1.92)을 인용해 우리 comp1 2.066 eV를 "wide-gap insulator, 절대비교 아님"으로 방어. 리뷰가 보증하므로 변명이 아니라 표준 인지.
3. **ESW에서 우리가 리뷰를 *상회*함을 명시.** 리뷰는 SE 창을 Fig 7 band-edge로만 본다 → 우리 grand-potential(+Schwietert 2–3× 과대 논증)이 *더 엄밀*. deck "우리 방법의 엄밀성" 슬라이드: "표준 리뷰조차 band-edge인데 우리는 grand-potential". 단 grand-potential *출처*는 Mo2012(리뷰 아님)로 정확히.
4. **TM-free라 U-모호성에서 자유.** 리뷰 §7의 "U는 semi-empirical·TM-d 전용·산화물 formation엔 GGA가 나음"의 *난맥*을 우리 황화물(localized d 없음)은 회피 — 우리 hull 전압이 U 선택 논쟁에서 깨끗함. **Nd만 +U(4f) 정당**.
5. **MLIP은 "리뷰의 DFT 기준을 넘는지"로 검증.** 우리 UMA가 (a) EOS/Ea는 DFT급(Nd B0 18.9≈19.9, Ea 0.25 실험일치)이나 (b) **절대 σ 3–5× 과대** → "에너지·장벽은 신뢰, 절대 수송계수는 DFT/실험 보정"이라는 우리 운용규칙이 리뷰의 "AIMD 정확도 기대"에 비춰 정당화. deck에서 MLIP 한계를 *선제적으로* 명시.
6. **SCAN 미채택의 정직한 trade-off 문서화.** 리뷰 1순위(SCAN)를 안 쓴 이유(MP 정합·R²SCAN mixing noise·Isaacs intermetallic 오차)를 §7에 적어둠 → reviewer "왜 SCAN 안 썼나"에 즉답.

## 9. 인용 가능 문장 (deck/paper용)
- "Our DFT pipeline follows standard practice for battery materials (He et al., *Energy Environ. Mater.* 2019): PBE for ground-state energetics, DOS/PDOS + Bader for electronic structure, Nernst/convex-hull thermodynamics for redox energetics, and AIMD-MSD for Li⁺ transport."
- "Consistent with the well-documented PBE band-gap underestimation (~1 eV; He et al. 2019, Fig 8), we report our argyrodite gaps (2.07 eV, PBE) only as 'wide-gap insulator' and compare compositions on a consistent-functional basis rather than against hybrid/experimental absolutes."
- "Whereas the standard review represents the solid-electrolyte stability window through the Goodenough HOMO/LUMO band-edge picture, we use the grand-potential decomposition window (Mo–Ong–Ceder), which avoids the 2–3× overestimation of band-edge windows for solid electrolytes — our LPSCl/LPSCl1.6 share an identical S²⁻-limited oxidation onset despite differing band edges."
- "Our AIMD activation energy for ordered LPSCl (0.253 eV) matches the experimental value (Schlem 2020, ~0.25 eV) within 0.003 eV, validating the transport protocol; absolute conductivities from the foundation MLIP carry a known 3–5× overshoot and are cited as Ea/ratios."

## 10. 주의/한계 (over-claim 방지)
- **이건 *방법* 리뷰지 argyrodite/SE 데이터 소스 아님.** 우리 4축(A/B/C/D)에 *수치*로 넣지 말 것 — comparison엔 "methods-provenance" 1줄로만. argyrodite·황화물 SE·grand-potential ESW는 리뷰에 **직접 예시 없음**.
- **2019 리뷰 = r²SCAN(2020)·foundation MLIP(2023+)·최신 grand-potential 계면 도구 누락.** 우리 UMA-MLIP·constrained-ESW·interface_reactivity의 표준성은 *이 리뷰가 아닌 후속 문헌*으로. 리뷰는 우리 *정적 DFT 백본*만 커버.
- **리뷰의 ESW = Fig 7 band-edge.** "He2019가 우리 grand-potential ESW를 정당화한다"고 하면 **부정확** — 리뷰는 band-edge 그림이고, 우리 grand-potential 출처는 Mo2012/Schwietert2020(별도). 리뷰는 *average-voltage(Δ_rG=−nFE) 근간*만 제공.
- **리뷰 1순위 추천(SCAN)을 우리는 안 씀**(GGA+U hull). 정당한 trade-off지만 "우리가 리뷰 best-practice를 *전부* 따른다"는 과장. 정확히는 "PBE 백본은 표준, gap/전압 정밀의 SCAN 권고는 MP-정합·noise 이유로 미채택".
- **우리 MLIP은 DFT가 아니다.** 리뷰의 DFT 정확도 기대는 우리 *DFT* 부분엔 직접 적용되나, *UMA surrogate*엔 "기준을 넘는지 검증해야 할 대상"으로만 — 절대 σ는 그 기준 미달(3–5× 과대).
- **저자 소속(Wuhan)·[외부]** — [우리 그룹] 태그 금지. self-cite/그룹 관계 없음(순수 외부 표준 리뷰).

## 11. 기법 용어 미니사전 (리뷰가 쓰는 용어 ↔ 우리 용법)
- **LSDA/LDA**: local (spin) density approx. 밀도만. lattice 좋고 barrier 과소·overbind. (우리 미사용)
- **GGA/PBE**: 밀도+gradient. 배터리 주류. gap·barrier·vdW 과소. **우리 백본.**
- **meta-GGA/SCAN**: +kinetic energy density. gap·전압·DOS 균형(리뷰 추천). intermetallic formation은 PBE보다 나쁠 수도. **우리 미채택(trade-off).**
- **hybrid/HSE06**: +screened HF exchange. gap·전압 정확(GGA+U급), 비용 큼. **우리 미실시(gap은 PBE+caveat).**
- **DFT+U**: Hubbard U로 self-interaction 교정. TM-d/f localized 전용·system-dependent. **우리 Nd 4f(U=8)만.**
- **cohesive E / formation E**: 0K 안정성. 고립원자 / 원소표준상태 기준. (우리 메인 = MP hull E_above_hull)
- **Gibbs G=H−TS**: 유한 T·P polymorph 비교. (우리 = 0K E + MLIP anneal 대용)
- **phonon dispersion**: 동역학 안정성(허수=불안정). **우리 미실시**(elastic eigenvalue로 기계안정만).
- **average voltage(Ceder)**: V=−Δ_rG/nF, 고체상 Δ_rG≈ΔE_DFT. **우리 grand-potential의 근간.**
- **convex hull**: formation E 하한포락 → 전압 plateau·중간상. **우리 분해 staircase의 닫힌계판.**
- **HOMO/LUMO 전기화학창(Fig 7)**: band-edge 기반 SE 안정창. **우리는 grand-potential로 대체**(band-edge는 2–3× 과대).
- **NEB/CI-NEB**: 확산 단일경로 E_a. (우리 = BVSE 경량 + AIMD)
- **AIMD-MSD**: MSD=6Dt→D, Arrhenius→Ea, NE→σ. **우리 수송 표준**(MLIP로 구현).
- **CDD(charge density difference)**: 결합형성·전자이동 시각화. **우리 slide24.**
- **vdW(D3)**: 분산보정. 흡착·약결합 필수. **우리 PBE vs D3 elastic 절대값차 설명용.**
- **grand-potential ESW**(리뷰엔 *없음*): μ_Li 열고 분해창. **우리 핵심**, 출처 Mo2012(리뷰 §3 Nernst의 open-system 확장).
- **foundation MLIP(UMA-s-1p1)**(리뷰엔 *없음*): DFT surrogate. EOS/Ea는 DFT급, 절대 σ 3–5× 과대.
