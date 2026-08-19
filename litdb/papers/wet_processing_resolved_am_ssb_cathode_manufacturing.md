<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md -->
# ASSB 양극을 *습식공정*(슬러리→건조→압연)으로 — *실제 형상(resolved, multisphere)* AM 입자를 nano-CT에서 추출해 DEM 제조 시뮬 + GeoDict로 σ_ionic·σ_e 산출 — Weitze / Franco (Energy Storage Materials 2024)

> slug `wet_processing_resolved_am_ssb_cathode_manufacturing` · DOI `10.1016/j.ensm.2024.103747` · type `DEM (LAMMPS, multisphere resolved-AM; wet-process slurry→dry→calender; exp 밀도/porosity 보정) + GeoDict 연속체 σ_ionic/σ_e` · PDF `WetProcessing_ResolvedAM_SSB_CathodeManufacturing_Simulation.pdf` · digested `2026-06-26` · status ✅

> ⚠ **rev 2026-08-19** — 출판본 PDF 전문 + **SI(force-field·JKR·PSD 표)** 재판독으로 **정정 6건**이 있다.
> **§ ★★ 2026-08-19 심화** 절이 정본이며, 아래 본문 중 정정된 자리에는 `⚠정정2026-08-19` 표식을 달았다.
> 특히 **① AM 소재(NMC622 는 형상 공여체일 뿐)**, **② 두께 110/40 µm 의 귀속**, **③ "σ 는 상한" 프레이밍**,
> **④ "무차원이라 절대 비교 불가"** 는 **뒤집혔거나 갈라졌다** — 그 4건은 심화 절 §0 표를 먼저 볼 것.



> elements: Li
> methods: elastic

---

## 0. 이 논문이 우리에게 *왜 특별한가* (한눈 positioning)

이 논문은 **우리 프로젝트와 가장 직접적으로 겹치는 시뮬 peer 중 하나**다. 다섯 가지가 동시에 성립한다:
1. **소재계가 우리 것** — NMC(니켈리치) + **LPSCl(Li₆PS₅Cl)** ASSB 양극. `⚠정정2026-08-19` 슬러리 AM 은 **`LiNi₉Mn₀.₅Co₀.₅O₂`(인쇄 그대로 = Ni-rich, 첨자 오식 의심)** 이고 **NMC622 는 nano-CT *형상 공여체*** 다(§2.2 가 "슬러리 소재와 다르다"고 명시) — 초판의 "AM = NMC622" 는 반전 오독.  Ni 함량은 오히려 우리 NMC811 에 **가까울 수 있다**(단정 불가).
2. **resolved(실제 형상) AM 입자** — nano-CT에서 *진짜 다결정 NMC 형상*을 추출해 **multisphere(여러 구 + harmonic bond로 강체 고정)** 로 표현. ★ **우리가 *안 가진* 것**(우리 DEM AM은 완전 구 + MPM scaffold로 형상 우회) → §B/§C의 핵심 대비축.
3. **transport를 *수치로* 산출** — GeoDict DiffuDict/ConductoDict 연속체로 **σ_ionic·σ_e**를 계산(σ_thermal 없음). Lyu(정성)·Bielefeld2019(percolation까지)보다 한 발 더, 우리·Bazzoun과 같은 transport-수치 레벨이되 **연속체**(점접촉 constriction 없음 = 상한).
4. **습식공정(wet-processing) 전체 사슬** — 슬러리 평형 → 건조(용매 제거) → 압연을 *한 LAMMPS DEM*에서 연속. **건조·CBD·용매 = 우리 미보유 wet-process 축**. ⚠ 단 우리 ASSB는 건식(dry-process) 지향이라 *셀-제조 경로가 다름*.
5. **Franco/ARTISTIC/LRCS 그룹** — Ngandjong(2021)·Bazzoun(2026)과 *같은 연구실*. 즉 **Ngandjong LIB resolved-shape(ref 37 Xu 2023) → 본 논문 ASSB resolved-shape**의 직계, 그리고 **Bazzoun(같은 그룹의 RNM constriction σ)** 과 자매. 우리 transport novelty의 정확한 위치를 *그룹 내부 진화*로 드러내는 peer.

⇒ **그들이 앞서는 칸 = resolved AM 형상 + 습식공정**(정직히 인정). **우리가 앞서는 칸 = 점접촉 constriction σ 삼중항(Holm/Kirchhoff) + Stage-E 소성면적 + 진짜 소성 morphology(MPM J2) + fracture-aware + dual-model + LOOCV 예측기.** 본 논문은 *형상은 resolved지만 transport는 연속체(constriction 없음)이고 σ_thermal·소성흐름·fracture가 없다* → 우리가 메우는 칸이 분명하다.

---

## 1. 한 줄 요약
**solid-state 양극(NMC[Ni-rich, `LiNi₉Mn₀.₅Co₀.₅O₂` 인쇄 그대로 — `⚠정정2026-08-19` NMC622 는 nano-CT 형상 공여체일 뿐] + LPSCl + carbon C65 + PIB 바인더)의 *습식 제조*(tape-cast 슬러리 → 건조 → 압연)를 *실제 형상 AM 입자*로 DEM 시뮬한 proof-of-concept.** 핵심 novelty(저자 주장): **nano-CT 단층촬영에서 다결정 NMC의 *진짜 형상*을 Weka segmentation + watershed로 추출해 multisphere(겹친 구 + harmonic bond로 강체 유지)로 표현**하고, 그 resolved-shape AM을 **습식 제조 워크플로(LAMMPS: Langevin + LJ + JKR + harmonic bond, 슬러리 NPT 평형 → CBD 입자지름 축소로 건조 → 압연 roll)** 에 넣어, **Bayesian 다목적 최적화로 force field를 실험 밀도·porosity에 보정**한 뒤, **GeoDict(DiffuDict 이온/ConductoDict 전자)로 σ_ionic·σ_e의 압연도(calendering degree) 의존성**을 도출. 결과: ① **porosity 0.57 → 0.30**(0~45% 압연, 비선형 — springback 때문), ② **σ_ionic·σ_e 둘 다 압연도↑ → 단조 증가**(percolation 경로 짧아짐·접촉↑), ③ ★ **반직관적 발견**: 압연해도 *서로 다른 상 사이* 계면면적(AM-SE 등)은 *증가하지 않고 거의 일정* — **구형·강체 입자라 일단 접촉하면 면적이 더 안 늘기 때문**(저자가 *모델 한계로 명시*: spherical/rigid → 소성 변형으로 계면이 못 자람). 즉 **이 논문조차 "resolved 형상이어도 *입자 소성 변형*(계면 성장)은 못 잡는다"고 자인** → 우리 MPM 형상소성이 메우는 바로 그 칸.

**⚠ 핵심 주의 3가지**: (i) **σ는 *연속체*(GeoDict, 점접촉 constriction 없음)** → SE-SE granular 점접촉 좁힘저항(Holm)을 안 풀어 **σ_eff 상한**(우리·Bazzoun RNM이 그 아래로 깎음). **`⚠정정2026-08-19` — 이 '상한' 서술은 *방법 수준*(접촉·계면 저항 항이 없다)에서만 유효하다.  *결과 수준*에서는 반대다: 그들 F_ion = 1.35×10⁻² 은 같은 소재계 실험(Bazzoun 0.134)의 **1/10**, Bruggeman 유효매질의 **1/5.6** 이다 — 얼어붙은 접촉면적(Fig 7)과 φ_SE ≈ 0.18(percolation 문턱 아래)이 σ 를 **아래로** 끌어내린다.  심화 §②-4/②-보론.** (ii) **resolved 형상 ≠ 형상 *소성***: AM은 multisphere로 *형상은 실제*이되 **harmonic bond로 강체 고정 = 영원히 안 변함**(δ 겹침조차 인위적으로 억제) → 압밀 중 *형상 변화·void-fill·계면 성장 없음*(저자 명시 한계). (iii) **nano-CT 소재 ≠ 슬러리 소재**(데이터 가용성 때문에 다른 NMC nano-CT를 형상 추출용으로 차용) → 형상은 *대표적*이지 *그 슬러리의 실측 형상은 아님*.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (AM/SE/binder) | 연구유형 |
|---|---|---|---|---|
| **Dennis Weitze, Franco M. Zanotto, Diana Zapata Dominguez, Alejandro A. Franco**(교신, alejandro.franco@u-picardie.fr) — **Laboratoire de Réactivité et Chimie des Solides (LRCS), Université de Picardie Jules Verne, Amiens** + Réseau sur le Stockage Électrochimique de l'Énergie (RS2E) + ALISTORE-ERI + Institut Universitaire de France | **Energy Storage Materials 73 (2024) 103747** (접수 2024-06-11, 개정 2024-07-22, 게재 2024-08-24, online 2024-08-30, ©Elsevier; **NOT open access**) | 10.1016/j.ensm.2024.103747 | **AM = NMC622** LiNi₀.₆Mn₀.₂Co₀.₂O₂ **75 wt%**(resolved multisphere) + **SE = LPSCl** Li₆PS₅Cl **17.5 wt%**(구) + **carbon C65(Timcal) 5 wt%** + **PIB(polyisobutene) 바인더 2.5 wt%**(C65+binder = CBD 도메인, 구) + **용매 p-xylene**(건조로 제거); 슬러리 고체분율 **50 %**, PIB 9 wt% in p-xylene | **DEM**(LAMMPS [45]; 슬러리→건조→압연 습식 연속) + **resolved-AM multisphere 추출**(nano-CT [41,42] + Weka segmentation [43] + watershed) + **Bayesian 다목적 보정**(eq 2.12) + **GeoDict 연속체 σ**(DiffuDict 이온 + ConductoDict 전자) |

> ★ **그룹·계보 자리매김 (매우 중요)**: 본 논문은 **Franco 그룹(LRCS, ERC-ARTISTIC/SMARTISTIC) 의 ASSB 제조-시뮬 라인**이다. 본문 §1·§2가 직접 계보를 밝힌다:
> - **Alabdali / Ngandjong / Duquesnoy [16,24,25,33,40]** = 그룹의 **LIB 제조 디지털트윈**(슬러리→CGMD→건조→압연→echem). 본 논문 = 그 LIB 워크플로의 **ASSB 확장 + resolved-shape**.
> - **ref [37] Xu, Ngandjong, Franco 2023 (J. Power Sources)** = 같은 그룹의 ***LIB* resolved-shape**(3D 실제 입자 형상) 모델. 본 논문이 명시: *"realistic shapes의 포함은 *이전엔 Li-ion에서만* 됐다(ref [37]) — 본 논문이 *처음으로* ASSB에 적용."* ⇒ **본 논문 novelty = resolved-shape를 ASSB로 가져온 첫 사례.**
> - **ref [16] Alabdali 2023 (J. Power Sources 580, 233427)** `⚠정정2026-08-19: 연도 2022→**2023**` = 그룹의 **첫 ASSB 물리모델**(단 *구형 AM*). 본 논문 = 그 위에 *realistic shape* 추가. Weitze 원문 §1: *"Alabdali et al. [16], from our group, developed the **first model linking the microstructure of a solid-state battery to its manufacturing process**, by taking into account **spherical shapes** for the active material"* + *"a further development of the existing simulation method … developed by Alabdali et al. [16]"*. ⇒ **정본 카드 `papers/alabdali2023_cgmd_wet_manufacturing_ssb_cathode.md`** (2026-08-19 신설 — 슬러리 유변학 보정·CBD 입자축소 건조·δ_e/τ_g 원본 수치는 **전부 그 카드**로).
> - **ref [38] Xu, Paredes-Goyes 2023 (Batteries & Supercaps)** = 같은 그룹의 **압연 중 입자 *fracture* 예측 모델**(LIB) — 본 논문은 *fracture는 안 넣음*(한계로 언급).
> - **자매(같은 ASSB-σ 솔버 그룹) Bazzoun 2026** = *RNM(Holm constriction)* σ. 본 논문은 *GeoDict 연속체* σ. ⇒ **같은 그룹이 ASSB σ를 *연속체(본 논문)*와 *constriction-RNM(Bazzoun)* 두 방식으로** 푼다 — 우리 transport 비교에서 *둘 다* 매핑 대상.
> ⇒ 본 논문의 셀링포인트 = **"resolved(실제) AM 형상 + 습식공정 전체사슬을 ASSB에 처음"**. 단 저자 스스로 **proof-of-concept / limited computational resources**라고 반복 명시(고해상 입자는 비용으로 *안 씀* — coarsened 사용).

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **슬러리 밀도 ρ** | **exp 1.353 ± 0.001 / sim 1.34 ± 0.02 g/cm³** | 슬러리(보정 타깃) | stated(eq 3.1) | Anton Paar densimeter DMA 4100 M. Bayesian 최적화로 sim→exp 밀도 맞춤 |
| **porosity (건조후, 압연 전)** | **exp 0.53 ± 0.03 / sim 0.57 ± 0.01** | 건조 전극, 압연 0 % | stated(eq 3.2) | sim이 exp 오차범위 내. ★ 이게 압연의 시작점 |
| **★ porosity (압연)** | **0.57 → 0.30** | 압연도 0 → 45 % | stated(본문) + Fig 6 | P_sim=0.30±0.02 @45 %. **비선형**(springback이 압연도 따라 달라서); ~25 % 압연 이후 급강하 |
| **★ σ_ionic (압연)** `⚠정정2026-08-19` | **0.04e-2 → 1.35e-2** (= **형성인자 F = σ_eff/σ_SE,bulk**, 9점: 0.04/0.14/0.31/0.43/0.50/0.66/0.85/0.94/1.35 ×10⁻²) | 압연도 0.05 → 0.45 | digitized(Fig 8 우) | **단조 증가**, 무차원(SE 벌크 σ_ion=1로 정규화). 압연↑ → SE 접촉↑·τ↓ → σ_ion↑ (★ ASSB는 LIB와 반대로 압연이 이온도 좋게 함, 저자 명시) |
| **★ σ_electronic (압연)** `⚠정정2026-08-19` | **0.12e-3 → 1.13e-3** (= **F = σ_eff/σ_CBD,bulk**, 9점: 0.12/0.16/0.30/0.29/0.33/0.64/0.57/0.96/1.13 ×10⁻³) | 압연도 0.05 → 0.45 | digitized(Fig 8 좌) | **단조 증가**, 무차원(CBD 벌크 σ_e=1로 정규화). 0.3 압연 근처 계단형 상승. 압연↑ → 입자접촉↑·porosity↓ → σ_e↑ |
| **★ 정규화 계면면적 A_interface/A_base (압연)** | SE-Pore **~11.5→8.5**, CBD-Pore **~5.8→4.8**, AM-Pore **~5.7→4.0**, **AM-SE ~1(거의 일정)**, CBD-SE ~1.8, CBD-AM ~0.9 | 압연도 0.05 → 0.45 | digitized(Fig 7) | ★★ **반직관 핵심**: *상-Pore* 계면은 감소(공극 줄어듦), 그런데 ***상-상* 계면(AM-SE 등)은 거의 안 늘거나 감소** — 구형·강체라 접촉 후 면적 못 자람(저자 *모델 한계로 명시*) |
| **두께 (제조 사슬)** `⚠정정2026-08-19` | **평형 슬러리 22 µm 폭 × 110 µm 높이 → 건조 전극 22 × 40 µm**(압연 박스도 40 µm) | 공정 단계 | digitized(Fig 4 라벨) | **110 µm 은 *슬러리 기둥*, 40 µm 이 *건조 전극*** — 즉 110→40 은 **건조 수축(2.75×)** 이고 압연은 그 40 µm 안에서 일어난다.  초판의 "건조 110 → 압연 40" 은 오독 |
| **E_AM (NMC)** | **명시 단일값 없음** (JKR E* eq 2.8로 들어감, Bayesian 보정) | 소재 | — | ★ Table로 E 절대값 안 줌 — force field를 *밀도/porosity에 보정*(eq 2.12)해 결정. cf 우리 E_CAM 140, Lyu 142 |
| **E_SE / E_CBD** | **명시값 없음**(보정으로 결정) | — | — | 마찬가지로 JKR/LJ 파라미터를 Bayesian로 보정 — *재료 E를 직접 입력 안 함*(chemistry-neutral 지향, 본문 명시) |
| **AM PSD** `⚠정정2026-08-19` | **Gaussian µ = 4.5 µm, sd = 0.79 µm, [3, 6] µm 밖 제외**; **SE = 단분산 Ø1.0 µm**(LPSCl fine, NEI Corp.) | SI "Particle Size Distribution" | **stated(SI)** | watershed로 secondary particle 분리, "targeted particle size distribution" 범위로 선택. ⚠ **nano-CT 소재 ≠ 슬러리 소재** |
| **coordination Z / Heckel P_y** | **n/a**(미보고) | — | — | ★ Z·Heckel 안 줌(porosity-vs-압연도만). Lyu/Sangrós와 달리 배위수 진화 없음 |
| **σ_thermal** | **n/a — 안 풂** | — | — | ★ 이온·전자만(우리 삼중항 중 열전도 없음) |
| **σ 절대 단위** `⚠정정2026-08-19` | **무차원 = 형성인자 F**(이온은 SE 벌크, 전자는 CBD 벌크를 1.0) | — | stated(본문 §2.5) | ⚠ **절대 mS/cm 는 없다.**  그러나 **F 축에서는 직접 비교된다** — 그들 F_ion = 1.35×10⁻² (**N_M = 74**) vs **Bazzoun 실험 0.134 (N_M = 7.5)** = **10배 저항적**.  전자 축만 **CBD 벌크 σ 미보고(n/a)** 라 환산 불가.  심화 §③-C/③-D |

## 4. 시뮬레이션 방법 ★
- **code / version**: **LAMMPS** [45] (open-source MD/DEM; 슬러리·건조·압연 모두). 형상 추출 = **ImageJ [41,42] + Weka segmentation plugin(Fast Random Forest 분류기) [43] + watershed [41,42]**. **transport σ = GeoDict (Math2Market) — DiffuDict(이온) + ConductoDict(전자)** [16]. **보정 = Bayesian 다목적 최적화** [49].
- **지배 운동방정식 (Langevin DEM; eq 2.1–2.2)**: 회전 `I_i dω_i/dt = M_i` (eq 2.1, M_i=접촉토크). 병진 = **Langevin** `m_i d²r_i/dt² = −λ·(dr_i/dt) + f_i^ext + η_i(t)` (eq 2.2) = **속도의존 마찰 −λv(감쇠)** + **외력 f^ext** + **시간의존 stochastic force η(t) (Gaussian = Brownian 운동)**. ★ **이게 핵심 차별점 1**: 슬러리(분산매 속 입자)라 **Brownian/점성 Langevin 동역학** — Lyu의 fluid-substitution(부력+점성)과 같은 *목적*(용매 환경)이되 *방식이 다름*(Langevin 마찰+stochastic). 중력 무시(µm 입자).
- **외력 f^ext = 세 항의 합 (eq 2.3, cutoff r_c 내에서만)**: `f_i^ext = −∇U_pot = −∇U_LJ − ∇F_JKR(의 퍼텐셜) − ∇U_harm`. 즉 **(A) Lennard-Jones + (B) JKR 접촉 + (C) harmonic bond** 세 가지.
  - **(A) Lennard-Jones (eq 2.4)**: `U_LJ(r_ij) = 4ε[(σ/r_ij)¹² − (σ/r_ij)⁶]` if r_ij < r_c. **ε = 퍼텐셜 깊이(상호작용 세기), σ = 입자 근접거리** = **van-der-Waals/반발 — 큰 거리 인력 + 가까이서 반발**. 이종입자 간: **ε = √(ε_i·ε_j) (기하평균, eq 2.5), σ = (σ_i+σ_j)/2 (산술평균, eq 2.6)** [47]. ⇒ LJ = 슬러리 분산/응집의 콜로이드 상호작용.
  - **(B) JKR 접촉 (eq 2.7)**: `F_JKR = (4Ea³/3R − 2πa²√(4γE/πa))·n̂` (Johnson-Kendall-Roberts — **점착성 탄성 접촉**). 유효반경 `R = R_iR_j/(R_i+R_j)` (eq 2.7), **유효 Young's modulus E (eq 2.8)** `E = [(1−ν_i²)/E_i + (1−ν_j²)/E_j]⁻¹`, **표면장력 에너지밀도 γ**(점착). 접촉반경 a, 겹침 `δ = a²/R − 2√(πγa/E)` (eq 2.9, δ>0일 때만). ★ **JKR = Hertz + 점착(adhesion)** — *항복압 캡 없음*(탄성 + 표면에너지). 즉 우리 **접촉모델 층위지도의 *no-cap* 층**(Hertz류, 소성 없음)에 *점착*만 더한 것. δ는 *기하 겹침 프록시*.
  - **(C) harmonic bond (eq 2.10) ★★ — resolved 형상을 강체로 유지하는 핵심**: `U_harm(r_ij) = Σ_{i=1}^N (κ/2)(r_ij − r_0)²` — **같은 secondary AM 입자에 속한 primary(구성) 구들끼리 최근접·차근접 이웃 사이에 인공 harmonic bond**. **bond 강성 κ를 *인위적으로 매우 크게*** → primary 구들이 거의 안 움직임 → **secondary 입자가 *실제 형상을 유지한 채 강체*처럼 거동**. ★ **이게 "resolved 형상"의 메커니즘이자 동시에 한계**: 형상은 *진짜*(multisphere로 NMC 다결정 외형 재현)이되, **그 형상은 *영원히 안 변함*(강체)** — 압밀 중 소성변형·계면 성장 *불가*(저자가 Fig 7 반직관 결과의 원인으로 명시).
- **재료 파라미터**: ★ **E_AM/E_SE/E_CBD·σ_y·ν를 *직접 표로 안 줌*.** 본문 §2.4: *"chemistry-neutral을 지향 — 상-상 상호작용(eq 2.3)을 *실험 물성을 모사하도록 보정*."* **모든 force field(LJ ε·σ, JKR γ·E, bond κ)를 Bayesian 최적화로 *슬러리 밀도(eq 2.12) → 건조 porosity*에 맞춤.** ⇒ **재료 E는 *입력*이 아니라 *보정 결과*** — Sangrós(나노압입으로 E 직접)·Lyu(Table 1 E 명시)와 *정반대 철학*. ν는 JKR E*(eq 2.8)에 들어가나 값 미명시.
- **bond/binder 모델**: **carbon C65 + PIB binder = CBD(Carbon Binder Domain) 도메인** — **균질 혼합 구(sphere)로 표현**(본문: "carbon과 binder가 *완전 혼합·균질 분포*라 가정 = CBD morphology 분석 시 통상 가정 [44]"). ⚠ **명시 입자-입자 *bond*(Sangrós eq10–13/Lyu parallel-bond) 아님** — CBD는 *구 + LJ/JKR 상호작용*으로만(binder가 *접착 bond*가 아니라 *콜로이드 입자상*). 건조 시 CBD-with-solvent 구가 dry-CBD 구로 *지름 축소*(아래).
- **★ 용매/건조 모델 (eq 2.11) — "particle shrinking" 건조**: 슬러리에서 **CBD 입자는 용매를 머금은 큰 지름 d_CBD^slurry**. 건조 = **CBD 입자 지름을 *제거된 용매 부피만큼* 축소** `d_CBD^slurry → d_CBD^electrode` (eq 2.11, dry CBD = slurry CBD − 용매부피). 그 뒤 NPT 재평형 → 건조 전극. ★ **이건 *저(低)건조속도* 모델**(저자 명시: "low drying rates"; 고속 건조의 비균질·crack은 ref [29] Lombardo로 *scope 밖*). ⚠ **명시 모세관력·표면장력·convection-diffusion 없음**(ref [30] Zihrul이 그걸 함 — 본 논문은 *입자축소*로 coarse). AM·SE 구는 건조 중 안 변함, CBD만 축소.
- **MPM/continuum**: **없음**(역학은 전부 DEM). **입자 형상 *소성* 없음** — AM은 multisphere로 *형상은 resolved*이되 harmonic bond로 *강체*. void-fill flow·계면성장 없음(저자 자인).
- **★ 전달 솔버 (GeoDict 연속체 — constriction 없음)**: **이온 σ = DiffuDict** (확산 flux: 양 끝 면에 1 mM 농도차 고정, steady-state 확산 → flux·두께/농도차 = 유효확산도 = σ_ion). **전자 σ = ConductoDict** (Ohm 법칙: z방향 1 V 전위차, Poisson steady-state). **둘 다 무차원**(관련 상 벌크 σ를 1로 정규화 — 이온=SE, 전자=CBD). xz·yz 외면 주기. ★★ **연속체 voxel 솔버 = SE/SE 점접촉 *수렴저항(Holm/Greenwood)* 을 *입자별로 안 풂*** → **σ_eff는 강체-접촉 granular망의 *상한***. ⇒ **우리 Kirchhoff+Holm·Bazzoun RNM이 그 constriction을 *되돌려* 넣어 σ를 아래로 깎는다**(우리가 *더하는* 핵심). 같은 Janek/Franco-계열 진화: Bielefeld2019(σ 없음)→Bielefeld2020(연속체 flux-PDE σ, *본 논문과 같은 방식*)→Bazzoun2026(RNM constriction σ)→우리(constriction 삼중항).
- **입자 처리** ★ (DEM판 "무질서 처리") — **★★ 이 논문의 가장 중요한 대비축**:
  - **AM = resolved(실제 형상) multisphere** — nano-CT에서 추출한 *진짜 다결정 NMC 외형*을 **여러 겹친 구 + harmonic bond(eq 2.10)로 강체 고정**해 표현. ★ **"sphere vs shape"에서 *shape* 쪽** = **Lyu·Sangrós·Bazzoun·Varkey(전부 완전 구)와 *유일하게 다른* 점**, 그리고 **우리(완전 구 DEM + MPM scaffold)와도 다른 점**.
  - **단 "rigid vs CONTACT-소성 vs SHAPE-소성"에서는 *rigid***: 형상은 실제지만 **harmonic bond로 강체 = 형상 *안 변함*** → **CONTACT 소성조차 없음**(JKR = 탄성+점착, 항복캡 없음; δ는 기하 프록시). ⇒ **resolved 형상 ≠ 형상 소성** — *진짜 SHAPE flow(우리 MPM J2)*는 여전히 없음. ★ **저자가 Fig 7에서 이 한계를 *직접 자인***: "구형·강체라 접촉 후 *계면이 못 자란다* → 압밀해도 상-상 계면면적이 안 늘어 *반직관적*."
  - **SE = 구**, **CBD = 구**(균질 carbon+binder).
  - **PSD**: AM은 nano-CT 추출(target 분포), SE·CBD는 구. **bimodal/Furnas dip *안 다룸*** — 압연도 sweep만(조성·크기비 sweep 없음).
  - **입자 coarsening (eq 본문, Fig 3)**: 고해상 multisphere(수백 구/입자)는 *계산비로 안 씀* → **pixel-averaging(3×3×3 슬라이딩, 평균>0.5면 입자 중심)으로 *조대화*** → 입자당 구 수 대폭 감소. ⇒ **형상은 "coarse한 resolved"**(완전 구보다 실제적이되 고해상 형상은 아님).
  - **초기구조 = 슬러리 random placement** → NPT 평형(슬러리) → 건조(CBD 축소 + 재평형) → 압연. ★ **Ngandjong식 "공정으로 구조 형성"**(랜덤 배치 후 그대로 안 씀).
- **도메인/RVE / servo / seeds / 압력범위**:
  - **RVE** `⚠정정2026-08-19`: **평형 슬러리 22 × 22 × 110 µm**(x·y·z 주기) → **건조 전극 22 × 22 × 40 µm**(압연도 이 박스 안).  110 µm 은 슬러리 기둥 높이다. bottom = current collector(CC), top = 압연 roll.
  - **압연 BC**: **roll을 const 속도로 하강** → 목표 압연도(calendering degree, *두께 감소율*) 도달까지 → **roll 제거(retract) → springback 발생**(실험처럼). roll·CC 둘 다 JKR로 미세구조와 상호작용. ★ **압연도(% 두께감소)로 제어 = 변위/속도 제어**(우리 MPM "hold"·Lyu와 같은 결, servo 압력제어 아님).
  - **압력범위**: ★ **절대 압력(MPa) sweep 없음** — **압연도 0~45 %**(두께 감소율)로 sweep. Heckel·절대응력 미보고.
  - **seeds**: 시뮬 반복(Fig 6·8 error bar = "standard error of simulation repetitions") — 횟수 명시 안 됨(복수 반복).
  - **보정 프로토콜 (Bayesian, eq 2.12)**: **다목적 cost `C = Σα_i(1−β_i)²`** (β_i = 타깃 비, 본 논문은 *밀도* β=ρ_sim/ρ_exp 단일목적으로 단순화). **(1) 슬러리 평형 단계에서 force field를 ρ_sim→ρ_exp에 보정, (2) 건조 단계에서 force field를 *재보정*해 dry porosity→exp porosity.** Bayesian이 posterior로 다음 force-field 제안 → argmin(C) 수렴. ⇒ **실험 밀도·porosity *2점*에 force field 전체를 보정**(우리 Minnmann 단일 porosity 앵커와 같은 결, 단 *force field 자체*를 맞춤).
- **특이사항/튜닝**:
  (1) **resolved AM 형상(multisphere) = 본 논문 셀링포인트** — ASSB 처음(LIB는 ref [37]에서 먼저). 단 *coarsened*·*nano-CT 소재 차용*·*강체*.
  (2) **chemistry-neutral force field 보정** — E를 직접 안 주고 Bayesian로 밀도·porosity에 맞춤(*다른 chemistry로 일반화* 지향).
  (3) **건조 = CBD 입자축소(eq 2.11)** — 저건조속도 모델, 명시 모세관 없음.
  (4) **σ = GeoDict 연속체**(접촉·계면 저항 항 없음; **voxel 크기 미보고 → 감사 불가**) → *방법 수준* 상한, **결과 수준은 실험의 1/10** `⚠정정2026-08-19`.
  (5) **검증 = 밀도(1.353 vs 1.34) + 건조 porosity(0.53 vs 0.57)** 2점 + σ·계면은 *추세* 분석(절대 σ 실측 검증 없음 — 무차원이라).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | **nano-CT 단층 슬라이스**(2D): gray-scale로 3상 분해 — **거의 검정=Pore, 진회색=SE/binder/CB(CBD) 응집, 밝은 원형=AM**. 100 µm scale bar | **실측 nano-CT가 *3상*(AM/Pore/CBD)만 분해 가능**(SE와 CBD가 gray로 구별 안 됨 → SE 형상은 *구로 가정*, AM만 resolved). 우리 micro-CT 비교 시 같은 한계 |
| **2** | ★ **resolved-AM 추출 파이프라인**(3D): (좌)nano-CT 슬라이스 스택 → (중)**Material Segmentation**(Weka Fast-RF: AM=보라/Pore=빨강/CBD=노랑) → (우)**Active Material Extraction**(AM skeleton만 보라 다결정 형상) | ★ **"실측 형상 → segmentation → AM 추출"의 모범 워크플로** — 우리가 resolved AM을 *진짜로* 넣으려면 이 경로(우리는 대신 sphere+MPM scaffold로 우회) |
| **3** | ★ **particle coarsening**(3D): (좌)고해상 multisphere AM 입자(수백 구, 보라 매끈) → (우)**조대화 후**(파란 큰 구 ~십수 개, 거친 형상) | ★ **"resolved이되 coarse" = 계산비 절충** — 고해상 형상은 *안 씀*. 우리 sphere 가정과 그들 coarse-multisphere 사이의 *해상도 스펙트럼* 가시화 |
| **4** | ★ **습식제조 4단계 스냅샷**: (1)Initial(슬러리 random, AM 초록/CBD-with-solvent 파랑/SE 노랑/CBD 검정) → NPT평형 → (2)**Equilibrated Slurry**(22 µm 폭 × **110 µm 높이**, CBD 파랑이 부피 지배) → 건조(CBD 축소+재평형) → (3)**Dry Electrode**(`⚠정정2026-08-19` **40 µm**, SE 노랑+AM 초록) → 압연(roll) → (4)**Calendered**(박스 40 µm, roll 위) | ★★ **슬러리→건조→압연 *전체 사슬*의 시각화** — 우리는 *압밀부터* 시작(슬러리·건조 미보유). **건조로 110→압연 40 µm** 두께변화. SI에 springback 영상 |
| **5** | ★ **상별 부피분율 vs CC로부터 거리**(z-프로파일, 압연도 0.05~0.45 색코딩): (좌상)AM·(우상)CBD·(좌하)Pore·(우하)SE. **압연↑(파랑→빨강)** → AM 부피분율↑(중앙 ~0.4), Pore↓, CBD·SE도 압연도 따라 z-피크 이동. **CC 근처는 AM 적음**(큰 AM 입자가 CC에 *모서리만* 접촉 → 중앙으로 갈수록 AM↑) | ★ **graded-z(두께방향 조성 구배)를 *공정에서* 얻음** — 우리 Phase-5 layered/graded-z의 *제조-유래* 버전. resolved 형상이라 *CC 근처 AM 결핍*이 자연 발생(작은 SE·CBD가 CC를 채움) — 우리 graded 모델 근거 |
| **6** | ★ **porosity vs 압연도**(0~0.45): **0.57 → 0.30**, error bar 有, **비선형 곡선**(~0.25 이후 급강하). 저자: springback이 압연압 따라 달라 *선형 아님* | ★ **압밀곡선 형태**(우리 P-vs-porosity·Heckel과 *형태만* 대조) — 단 **x축이 압연도(% 두께)지 압력(MPa) 아님** → 우리 Heckel(P_y=138)과 *직접 겹치기 불가*. 우리 floor ~10–15.6 %보다 훨씬 높은 30 %(LIB식 잔류공극? — 아래 §A 주의) |
| **7** | ★★ **정규화 계면면적 A_interface/A_base vs 압연도**(6종 계면): **SE-Pore(파랑 ~11.5→8.5) > CBD-Pore(주황 ~5.8→4.8) ≈ AM-Pore(초록 ~5.7→4.0) > CBD-SE(보라 ~1.8) > AM-SE(빨강 ~1, *거의 일정*) > CBD-AM(~0.9)**. **모든 *상-Pore* 계면은 감소**(공극 줄어듦), **AM-SE 등 *상-상* 계면은 안 늚** | ★★ **반직관 핵심 + 저자의 *모델 한계 자인***: "구형·강체라 접촉 후 *두 상이 면적을 못 늘림*(소성 변형 불가) → 압밀해도 AM-SE 계면(=충방전 활성)이 안 자라는 건 *비현실적, 우리 모델 한계*." ⇒ **우리 MPM 형상소성(계면 성장·coverage↑)이 메우는 *정확한 칸***. 우리 coverage(Tabor 소성면적)가 바로 이 *상-상 계면 성장*을 정량 |
| **8** | ★ **σ_e(좌)·σ_ionic(우) vs 압연도**(정규화, error bar): **σ_e ~0.15e-3→1.15e-3**(0.3 근처 계단 상승), **σ_ion ~0.05e-2→1.35e-2**(완만 단조). 둘 다 **압연↑→σ↑** | ★★ **압연(압밀)이 σ_ionic·σ_e *둘 다* 올림 — ASSB는 LIB와 반대**(저자 명시: "LIB와 달리 ASSB는 압연이 이온수송도 향상[16,56]"). = 우리 "압밀↑→σ_ionic↑(SE접촉↑)" 정확 일치. ⚠ 무차원이라 절대 σ는 우리/Bazzoun과 비교 불가, *추세*만 |

## 6. Post-processing ★
- **무엇**:
  - **porosity (eq 3.2)**: `P = V_pore/V_electrode`. 압연도 함수(Fig 6). 실험(densimeter + mass loading)과 2점 대조.
  - **상별 부피분율 z-프로파일**: CC로부터 거리 z의 함수로 AM/CBD/Pore/SE 부피분율(Fig 5) — *두께방향 비균질·graded* 정량.
  - **정규화 계면면적 A_interface/A_base (Fig 7)**: 6종 상-상/상-Pore 계면면적 / 양극 base 면적. ★ *충방전 활성 계면(AM-SE)* 추적이 목적이나 *반직관 결과*로 한계 노출.
  - **σ_ionic (DiffuDict)·σ_e (ConductoDict)**: GeoDict 연속체, 무차원(상 벌크=1 정규화). 압연도 함수(Fig 8).
  - **Bayesian cost C (eq 2.12)**: force field 보정 목적함수(밀도·porosity 비).
  - ⚠ **Z·Heckel·coverage(우리식)·fabric tensor·내부응력 *없음*** — Lyu/Sangrós보다 역학 후처리 *적음*(transport·계면·porosity 중심).
- **도구**: **LAMMPS**(DEM) + **ImageJ/Weka**(segmentation) + **watershed**(입자분리) + **GeoDict DiffuDict/ConductoDict**(σ) + **Bayesian 다목적 최적화**(force field 보정) [49]. 실험: **nano-CT**(형상 [41,42]), **Anton Paar DMA 4100 M**(슬러리 밀도), porosity(mass loading).
- **수치화·플롯·기록 방식**: 모든 결과를 **압연도(calendering degree, % 두께감소)의 함수**로(Fig 6·7·8). z-프로파일은 CC-거리 함수(Fig 5). **σ는 무차원**(절대값 없음). **압력(MPa)·Heckel·Z 없음.**

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 (Weitze 2024, ASSB 습식) | 우리 (ASSB cold-press) | 차이 / 이유 |
|---|---|---|---|
| **소재계** | **NMC(Ni-rich, `LiNi₉Mn₀.₅Co₀.₅O₂` 인쇄 그대로) + LPSCl + C65 + PIB**(ASSB) `⚠정정2026-08-19` NMC622 는 형상 공여체 | **NMC811 + LPSCl + VGCF/SuperP + PTFE**(ASSB) | ★ **거의 같은 셀화학**(둘 다 LPSCl ASSB; Ni 함량·바인더만 차이) — *드물게 같은 계열* peer |
| **★ AM 형상** | ★ **resolved multisphere**(nano-CT 실제 형상, 강체) | **완전 구**(DEM) + MPM scaffold로 형상 우회 | ★★ **그들이 앞섬**(실제 형상). 단 *강체*(소성흐름 없음) — 우리 MPM J2가 *형상변화*는 보유 |
| **★ 형상 *소성*** | **없음**(harmonic bond로 강체; JKR=탄성+점착, 캡 없음) | **MPM 진짜 J2 SHAPE 소성**(void-fill·계면성장) | ★★ **우리가 앞섬.** 저자 Fig 7에서 "계면 못 자람 = 한계" 자인 → 우리 MPM이 메움 |
| **★ 전달 σ** | **GeoDict *연속체*(DiffuDict/ConductoDict) σ_ionic·σ_e — *constriction 없음*(방법 수준 상한 — **결과는 실험의 1/10** `⚠정정2026-08-19`), σ_thermal 없음, *무차원(=형성인자)***| **Kirchhoff + Holm 구속 + Stage-E** σ_ionic/e/thermal **삼중항(절대 mS/cm)** | ★★ **우리가 앞섬**(점접촉 constriction + 열전도 + 절대값). 그들은 연속체 상한·이온/전자만·무차원 |
| **접촉법칙** | **JKR**(Hertz+점착, 항복캡 없음) + LJ(콜로이드) | Luding hooke/hysteresis(캡 없음) + Stage-E 소성면적 | **같은 no-cap 층**, 그들은 *점착(JKR)·콜로이드(LJ)* 추가(슬러리라); 우리는 Stage-E 소성면적 |
| **공정 범위** | **슬러리→건조→압연**(습식 전체사슬) | **압밀(cold-press)부터** | ★ **그들이 앞섬**(건조·슬러리 보유) — 단 ASSB는 건식이라 *경로 다름* |
| **건조/용매** | **Langevin(Brownian+점성) 슬러리 + CBD 입자축소 건조**(eq 2.11) | **없음**(dry-process/cold-press) | ★ **그들이 앞섬**(습식). ⚠ ASSB는 본질 건식 → *우리가 뒤처진 게 아니라 셀화학상 단계 없음* |
| **CBD** | **균질 carbon+binder 구(LJ/JKR), 명시 bond 없음** | Stage-2 부피점유; 명시 bond 없음(backlog A3) | **둘 다 명시 bond 없음** — 그들은 *콜로이드 구*, 우리는 *부피점유*. Sangrós/Lyu가 명시 bond 보유 |
| **E_AM/E_SE** | **명시 안 함**(Bayesian로 밀도·porosity에 보정 — chemistry-neutral) | E_CAM 140 / E_SE real 24·eff 1.35(DEM)/1.53(MPM) | ★ **철학 정반대**: 그들=force field를 *거시 보정*; 우리=재료 E 명시 + 18× 연화 프록시 |
| **압밀 제어** | **압연도(% 두께)** roll const-속도, springback 有 | **cold-press 단축, 변위 hold**(압력 300 MPa) | 둘 다 변위/속도 제어. **그들은 springback 有**(우리 미보유 — MPM unload로 가능) |
| **압력/Heckel** | **절대 MPa 없음**(압연도만), Heckel 없음, Z 없음 | 300 MPa, Heckel P_y=138·R²=0.965, Z 보유 | ★ **우리가 더 정량**(절대압·Heckel·Z) — 그들은 압연도-추세 |
| **porosity** | **0.578→0.291**(압연 0→0.45, digitized 10점), exp 0.53 | pure-SE ~10 % / real_14 15.6 % @300 | ⚠ **floor 다름**(그들 29 % vs 우리 10–15.6 %) — *압연도≠압력*(절대압 **미보고**), 습식 잔류공극, 소성 부재.  `⚠정정2026-08-19` **강성만으로 귀속하지 말 것** — 그들 침대엔 **E ≈ 5 kPa 의 초연질 CBD 상이 ~10 vol%** 있어 E→floor 사다리에 그대로 얹히지 않는다(심화 §③-B). *절대 비교 금지* |
| **PSD/dip** | **resolved AM(target 분포) + SE 구**, **dip 안 다룸**(압연도 sweep만) | **bimodal 12:4:1** + Furnas dip 정량 | ★ **우리가 dip 보유** — 그들은 조성·크기비 sweep 없음 |
| **검증** | **밀도(1.353 vs 1.34) + 건조 porosity(0.53 vs 0.57)** 2점 | solver=ground truth + Minnmann·Cronau·Bazzoun 외부앵커 | 그들 2점 보정; **절대 σ 실측 검증 없음**(무차원) |
| **예측기** | **없음**(case-by-case 시뮬) | scaling-law LOOCV(σ_ionic 0.975/σ_e 0.953/σ_thermal 0.903) | ★ **우리가 앞섬** — 솔버를 예측법칙으로 압축 |

> ★★★ **위 표는 §A에서 모두 풀어 씀 — 아래 "## 우리 DEM+MPM 대비"가 정식 비교 섹션**(사용자 mandatory). §7은 요약표.

### frame[5] 위치
- **이 논문 = 전달/패킹 측 + ASSB 습식공정 + *resolved 형상***: resolved multisphere AM(강체) + SE/CBD 구 + JKR/LJ → DEM 제조(슬러리·건조·압연) + GeoDict 연속체 σ. ★ **형상은 resolved이되 *소성*은 없음** — 우리 MPM이 메우는 *형상-소성/계면성장 절반*이 *여기서도* 빠짐(저자 Fig 7 자인). ⇒ **resolved 형상이어도 *소성흐름*은 별개**라는 강력한 frame[1]/[2] 증거 — *형상을 실제로 넣은 논문조차* "계면이 못 자란다"고 한계 인정.
- **그들 σ = *연속체 상한*(constriction 없음)** → 우리 Kirchhoff/Holm constriction 삼중항이 *수치로* 깎아 넣는 칸. Bielefeld2020(연속체)→Bazzoun2026(RNM)→우리(constriction 삼중항) 그룹-진화의 끝.
- **그들 습식(슬러리·건조) = 우리 미보유 wet-process 절반** → 단 ASSB 건식이라 *셀화학상 단계 없음*(보완 관계).

---

## 우리 DEM+MPM 대비 (comparison vs ours)

> 사용자 mandatory 섹션 A. 그들 **resolved multisphere AM(강체) + JKR/LJ 슬러리 + GeoDict 연속체 σ** vs 우리 **완전 구 DEM(Luding hooke/hysteresis + Stage-E) + MPM J2 형상소성 + Kirchhoff/Holm constriction 삼중항**; 그들 *습식*(슬러리→건조→압연) vs 우리 *건식 cold-press*; **그들이 *실제 AM 형상*을 갖고 transport도 *수치*로 푼다 — 단 *연속체 상한*이고 *형상 소성*은 없다.**

### A-1. ★★ AM 형상: 그들 resolved-multisphere(강체) vs 우리 완전-구-DEM + MPM-scaffold — *형상은 그들이, 형상-소성은 우리가*
- **그들**: nano-CT에서 **다결정 NMC의 진짜 외형을 추출 → multisphere(겹친 구 + harmonic bond로 강체)** 로 표현(Fig 2·3). ASSB에서 *처음*(LIB는 그룹 선행 ref [37]). ⇒ **"sphere vs shape"에서 *shape* 쪽** — Lyu·Sangrós·Bazzoun·Varkey(전부 완전 구)와 *유일하게 다르고*, **우리(완전 구 + MPM scaffold)와도 다르다.** ★ **이게 그들이 *명확히 앞서는* 칸.**
- **우리**: DEM AM = **완전 구**(AM_P/AM_S). 비구형 형상을 *직접* 안 넣음 — 대신 **(i) DEM은 구로 패킹**(Furnas dip·접촉망·transport를 구로 풀고), **(ii) MPM은 SE만 소성변형**(scaffold: DEM AM 위치 고정 + SE만 J2로 형상변화). 즉 **우리는 *형상 자체*는 구로 두되 *SE의 소성 형상변화*는 보유**.
- **★ 결정적 구분 — resolved 형상 ≠ 형상 *소성***: 그들 AM은 *형상은 실제*이되 **harmonic bond κ를 크게 잡아 *강체* = 영원히 안 변함**(eq 2.10). 압밀해도 *형상 변화·void-fill·계면 성장 없음*. ⇒ **그들은 "정지된 실제 형상"**, 우리 MPM은 **"변하는 형상(J2 흐름)"**. 두 강점이 *직교*:
  - **그들 강점**: 정적 미세구조의 *기하적 사실성*(실제 AM 외형 → 실제 packing·계면 위치·CC-근처 AM결핍 Fig 5). 우리 구-가정이 놓치는 *형상-유발 packing 비등방*을 그들은 잡음.
  - **우리 강점**: *압밀 중 형상이 변하는 과정*(SEM 코어보존+경계평탄화 ✓, 계면 성장, void-fill). **그들 Fig 7 반직관 결과의 원인**("구형·강체라 접촉 후 계면 못 자람")을 우리 MPM이 *정확히* 메움.
- **★★ 저자 자인 = frame[1]/[2]의 가장 강한 외부 증거**: Fig 7에서 저자가 직접 — *"as the material is compressed more and more, we would expect particularly the binder and solid electrolyte phase to deform and increase its interfacial contact... In our simulations, we do not observe this trend on account of the spherical [and rigid] nature of these particles."* ⇒ **형상을 *실제로 넣은* 논문조차 "소성 변형(계면 성장)을 못 잡는 게 한계"라고 명시** = "강체-구/형상 DEM은 소성흐름 절반이 빠진다, MPM이 필요하다"(frame[5])는 우리 논거를 *resolved-shape peer가 자기 입으로 확증*. (Varkey "구=타협"·Sangrós "고압 파쇄 고려필요"와 같은 계보, 단 *형상까지 넣고도 소성은 안 됨*이라 더 강력.)

### A-2. ★★ 전달 σ: 그들 GeoDict *연속체*(constriction 없음, 무차원, 이온·전자) vs 우리 Kirchhoff+Holm *constriction 삼중항*(절대 mS/cm, 이온·전자·열)
- **그들**: σ_ionic = DiffuDict(확산 flux), σ_e = ConductoDict(Ohm) — **GeoDict voxel 연속체 솔버**. **(i) 점접촉 수렴저항(Holm/Greenwood) 없음** → SE-SE granular 점접촉의 좁힘을 *입자별로 안 풂* = **σ_eff *상한***. **`⚠정정2026-08-19` — 이 '상한' 서술은 *방법 수준*(접촉·계면 저항 항이 없다)에서만 유효하다.  *결과 수준*에서는 반대다: 그들 F_ion = 1.35×10⁻² 은 같은 소재계 실험(Bazzoun 0.134)의 **1/10**, Bruggeman 유효매질의 **1/5.6** 이다 — 얼어붙은 접촉면적(Fig 7)과 φ_SE ≈ 0.18(percolation 문턱 아래)이 σ 를 **아래로** 끌어내린다.  심화 §②-4/②-보론.** **(ii) σ_thermal 없음**(이온·전자만). **(iii) 무차원**(상 벌크 σ=1로 정규화) → 절대 mS/cm 없음.
- **우리**: **명시 Kirchhoff 망**(Σ(φi−φj)/R=0) + **Holm 구속저항**(R=1/(2σr_c), 1967) + **Stage-E 소성 접촉면적** → **σ_ionic·σ_e·σ_thermal 삼중항을 *절대값(mS/cm)*** 으로. 게다가 **LOOCV 스케일링 법칙**(0.975/0.953/0.903).
- **대비의 의미 (그룹-진화로 positioning)**: ★ **이건 우리 transport novelty가 *그룹 내부 궤적*으로 가장 선명하게 보이는 칸.** Franco/Janek-계열 ASSB-σ는 **Bielefeld2019(σ 안 풂, percolation만) → Bielefeld2020 & *본 논문 Weitze2024*(연속체 flux-PDE/GeoDict σ, *constriction 없음 = 상한*) → Bazzoun2026(RNM Holm constriction σ + 실험) → 우리(constriction 삼중항 + 열전도 + 절대값 + 예측기)** 로 *스스로* 정교화돼 왔다. **본 논문 = 그 궤적의 "연속체 상한" 단계** — 우리·Bazzoun은 그 constriction을 *되돌려* 넣어 σ를 아래로 깎는다. ⇒ **"공정→구조 + granular constriction σ 삼중항 + 소성 morphology"라는 우리 3대 portion은 이 그룹이 걸어온 길의 *자연스러운 끝*에 놓인다**(positioning 최강 근거). ⚠ 정직: 본 논문 *목적*은 resolved-shape 제조-구조이지 constriction-정밀 σ가 아님 → "그들이 못 했다"가 아니라 "연속체 상한까지가 그들 scope, constriction은 우리/Bazzoun scope".
- **단 그들이 우리보다 *나은* σ 측면**: ★ **resolved AM 형상 위에서 σ를 푼다** — 우리 σ는 *구 패킹* 위. 즉 그들 σ_eff는 *실제 AM 외형에 따른 tortuosity/계면*을 반영(우리 구-가정이 근사하는 부분). ⇒ **이상적 미래 = 우리 constriction-RNM을 *그들 resolved 형상 위에서*** (둘의 결합).

### A-3. ★ 이온위상 — 본 논문은 *우리와 같은 ASSB 위상*(드물게)
- **Lyu/Sangrós/Ngandjong(LIB)** 은 이온=공극(Bruggeman, porosity GOOD)이라 우리와 *정반대* 위상이었다. **본 논문은 ASSB** → **이온 전도체 = SE(LPSCl) 고체망**, σ_ionic = SE-SE 연결(DiffuDict는 *SE 상* 벌크=1로 정규화) → **압연(압밀)↑ → SE 접촉↑ → σ_ionic↑**(Fig 8, 저자 명시: "LIB와 *달리* ASSB는 압연이 이온수송도 향상[16,56]"). ⇒ ★ **우리 "압밀↑→σ_ionic↑(SE접촉↑), porosity BAD"와 *정확히 같은 위상*** — Lyu 같은 LIB peer와의 *위상역전* 대비가 *여기선 불필요*(같은 ASSB). 오히려 **본 논문이 "ASSB는 압연이 이온도 좋게 한다"를 *명시*** → 우리 frame의 ASSB-위상 정당화.
- **단 그들 σ는 연속체·무차원** → "압연↑→σ_ion↑" *추세*는 우리와 일치(교차검증), *절대값*은 비교 불가(무차원). `⚠정정2026-08-19` **단, 무차원 값은 정의상 *형성인자* F = σ_eff/σ_bulk 이므로 F·MacMullin 축에서는 직접 비교된다** — 그들 F_ion = 1.35×10⁻²(N_M 74) vs Bazzoun 실험 0.134(N_M 7.5) vs 우리 STEP3 0.052–0.166(N_M 6–19).  전자 축만 CBD 벌크 σ 미보고라 불가.  심화 §③-C.

### A-4. ★ 습식공정(슬러리·건조) — 우리 미보유 wet-process 축 (Lyu와 같은 칸, 단 ASSB)
- **그들**: **Langevin(Brownian + 점성 마찰) 슬러리 NPT 평형 → CBD 입자축소 건조(eq 2.11) → 압연** 전체 사슬. 결과 `⚠정정2026-08-19`: 슬러리 기둥 22 µm 폭 × **110 µm** → **건조 전극 40 µm**(건조 수축 2.75×) → 압연은 그 40 µm 안, *graded-z 조성*(Fig 5, CC 근처 AM 결핍).
- **우리**: **건조·슬러리 없음.** ASSB **dry-process/cold-press** 지향(우리 소재계 = 건식 co-rolling, `papers/lee2025_corolling_dryprocess_lpscl_ptfe.md`).
- **대비의 의미**: ★ **습식 제조는 frame[5]의 우리 쪽에 *없는* 축** — Lyu와 같은 칸이되 *ASSB 버전*이라 더 직접적. 단 ⚠ **현재 ASSB 고에너지 셀은 *건식*이 주류**(slurry 용매가 SE를 적셔 계면 손상 → 본문 §1조차 "wet에서 SE가 AM을 못 적셔 계면 문제·sluggish kinetics[13,14]"라고 *습식의 단점* 인정!). ⇒ **우리가 뒤처진 게 아니라**, 본 논문은 *습식 ASSB라는 다른(덜 성숙한) 제조경로*를 다룸. **우리 dry-process가 오히려 *현재 주류 ASSB 경로***. 단 **습식 모델링 *방법*(Langevin 슬러리·CBD 축소 건조)** 은 만약 우리가 *습식 ASSB*나 *건조 동역학*을 다루면 청사진(우리 backlog D5와 약하게 연결).
- ★ **본 논문의 습식 단점 자인 = 우리 dry-process 정당화**: §1 — *"replacing the liquid electrolyte with a SE introduces disadvantages... the electrolyte is no longer able to wet the active material efficiently, interfaces are created between different materials, inducing capacity fade and mechanical instabilities[13,14]."* ⇒ **습식 ASSB의 계면 문제를 저자가 명시** → 우리 건식 경로(`Lee2025` co-rolling)가 *그 계면 문제를 회피*하는 이유.

### A-5. 압밀곡선·계면·검증 — *절대 비교 금지* 주의
- **압밀 P-vs-압연도**: 그들 Fig 6 = 0.57→0.30(압연 0~45 %, *비선형* — springback). 우리 Heckel = pure-SE 4압력 R²=0.965·**P_y=138 MPa**. ⚠ **x축이 *압연도(% 두께감소)*지 *압력(MPa)*** 가 아니다 → **그들 곡선을 우리 Heckel(P_y=138)/P-vs-porosity와 *직접 겹치기 불가*.** floor도 다름: **그들 30 %**(@45 % 압연) vs **우리 10–15.6 %**(@300 MPa). 왜 그들이 높나? (i) **압연도≠압력** — 45 % 압연이 우리 300 MPa에 해당하는지 *불명*(절대압 미보고); (ii) **습식 잔류공극**(슬러리 유래 + 저건조속도); (iii) **resolved 형상이나 *강체***(소성흐름 없어 우리 MPM처럼 void-fill로 floor 못 깸 — Fig 7 자인); (iv) **연속체 σ·구 SE**. ⇒ **floor 30 %는 LIB-DEM rigid floor ~20 %보다도 높음** — *강체-구 floor + 습식 잔류공극*. **우리 10–15.6 %는 소성흐름(MPM)·연화(DEM)로 그 아래** → 우리가 floor를 깬다는 논거의 *또 하나 대조점*(단 압력대 불명이라 *정성*으로만).
  - `⚠정정2026-08-19` **보강·완화 (심화 §①-B/③-B)**: SI 가 그들 AM/SE 쌍-유효 영률을 **135 GPa**(우리 환산)로 못박아 "강체-구" 진단은 **확인**됐다.  그러나 floor 30 % 를 **강성으로 귀속하는 것은 과하다** — 같은 SI 가 CBD 쌍 E 를 **1–20 kPa** 로 주고 그 CBD 가 ~10 vol% 를 차지한다(가장 무른 상이 압축을 흡수).  게다가 **압력 축이 아예 없다**.  ⇒ 이 대비는 **정성**으로만.  ★ 대신 그들에게서 **정량으로 가져올 것은 springback**: 우리 산출 회복률 = **압축량의 10–15 %**(심화 §③-C ④).
- **★ 계면 성장(Fig 7) = 우리 coverage가 메우는 칸**: 그들 AM-SE 계면이 압연해도 *안 자람*(강체-구) = *비현실적, 저자 한계 자인*. 우리 **coverage(Tabor 소성 접촉면적, Stage-E)** 가 바로 *압밀 중 AM-SE 계면 성장*을 정량(real_14 Tabor AM_P/S 49.6/48.2 %, 압밀↑→coverage↑). ⇒ **그들이 "못 잡는다"고 한 그 계면-성장을 우리가 *수치로* 보유** — §C의 강력한 차별점.
- **검증 깊이**: 그들 = 밀도(1.353 vs 1.34) + 건조 porosity(0.53 vs 0.57) **2점** + σ·계면 *추세*(절대 σ 실측 없음 — 무차원). 우리 = Minnmann porosity·Cronau overlap·Bazzoun σ_ionic·SEM morphology 다중앵커. ⚠ 둘 다 절대값 직접 전이 시 *소재·공정·무차원* 주의.

---

## 적용가능성 (applicability to our LIGGGHTS DEM + MPM model)

> 사용자 mandatory 섹션 B. 그들 **resolved-multisphere AM** vs 우리 sphere+MPM-scaffold로 비구형 AM 다루기; 습식공정 관련성(ASSB 건식 대비); 흡수 가능한 것. 우리 파이프라인/scripts에 매핑.

### B-1. ★★ resolved-AM-shape: 그들 multisphere vs 우리 sphere+MPM-scaffold — *둘을 결합*이 이상적
- **현재 우리**: DEM AM = **완전 구**(`input_*.liggghts`), 비구형 형상은 *직접* 안 넣음. MPM은 SE만 소성변형(scaffold = DEM AM 위치 고정). 즉 **AM 형상 자체는 구 가정**.
- **그들이 주는 것**: **multisphere(겹친 구 + harmonic bond로 강체)로 nano-CT 실제 AM 외형 표현**(eq 2.10, Fig 2·3). ★ LIGGGHTS도 **`multisphere` fix**(겹친 구 강체) 보유 → **우리가 *원하면* 그들 방식으로 비구형 AM을 LIGGGHTS에 *직접* 넣을 수 있음**(nano-CT/SEM → segmentation → multisphere).
- **★ 우리 전략 선택지(3가지) 비교**:
  | 방식 | 형상 | 소성 | 비용 | 우리 적용 |
  |---|---|---|---|---|
  | **현재 우리** = 완전 구 DEM + MPM scaffold(SE만 소성) | 구(AM) | SE만 J2 흐름 | 낮음 | production. *AM 형상* 근사 |
  | **그들(Weitze)** = resolved multisphere AM(강체) | 실제(coarse) | **없음**(강체) | 높음(multisphere) | 형상↑·소성×. *정적 packing* 사실성 |
  | **이상(미래)** = resolved multisphere AM + MPM SE 소성 | 실제 + 흐름 | SE J2 | 가장 높음 | 둘의 장점 결합 |
- **→ 매핑/판단**: ★ **그들 방식(강체 multisphere)을 *그대로* 채택하면 형상은 얻되 *소성을 잃는다*** — 우리 MPM 강점(SE 형상흐름)을 버리게 됨. 따라서 **무비판 흡수 금지.** 대신: **(i) AM *packing*의 형상효과가 중요한 케이스**(예: 매우 비구형 다결정 NMC의 CC-근처 결핍, Fig 5)만 **DEM AM을 multisphere로** 올리고(나머지는 구 유지 — 비용), **(ii) SE 소성·계면성장은 *계속 MPM*** 로. ⇒ **"비구형 AM packing은 그들 multisphere, SE 소성 morphology는 우리 MPM"**가 우리 frame[5]에 맞는 결합. ⚠ 단 *비용*(multisphere = 입자당 수~수십 구 → 접촉수 폭증) + *그들도 coarsening 강제*(고해상 안 씀)라 **production 전면 도입은 비현실적** — *대표 케이스 검증*용으로.

### B-2. ★ 그들 Fig 7 "계면 못 자람" = 우리 MPM coverage가 *이미* 메우는 칸 → 차별점 강화(흡수 불요)
- 그들이 *못 한* AM-SE 계면 성장(강체-구)을 **우리 MPM(J2 SE 소성)·Stage-E coverage가 *이미 보유*** → **흡수가 아니라 *우리 우위 강화*** (§C-3). ★ **흡수할 것은 *그들의 한계 진술 자체*** = paper/deck에서 "resolved-shape ASSB peer조차 소성 계면성장을 못 잡는다(Weitze 2024, Fig 7 자인) → 우리 MPM이 그 칸을 채운다"로 인용.

### B-3. ★ 습식공정·건조 — ASSB 건식이라 *우선순위 낮음*, 단 graded-z·Langevin은 방법론
- **건조(CBD 입자축소, eq 2.11)·Langevin 슬러리**: LAMMPS/LIGGGHTS에 `fix langevin`(마찰+stochastic) + 입자지름 ramp로 *구현 가능*하나 — ⚠ **우리 ASSB는 건식**(Lee2025 co-rolling)이라 *습식 건조 단계 원천 무관*. *우선순위 낮음.*
- **★ 흡수 가능 *방법론* 2가지**:
  - **(가) graded-z 조성(Fig 5)**: 그들은 *공정에서* CC-근처 AM 결핍·두께방향 조성구배를 얻음. 우리 **Phase-5 layered/graded-z**의 *제조-유래* 근거 — 우리 synth(`scripts/extract_2d_microstructure.py`, z-band)가 *임의로* graded를 넣는데, 그들은 *제조 물리로* 자연발생 → **graded-z가 인위적이 아니라 제조-실재**임을 인용.
  - **(나) Langevin 분산 동역학**: 만약 우리가 *SE-dispersion*(SE 응집/분산이 σ에 미치는 영향, backlog A5)을 모델하면 그들 Langevin(Brownian+점성)이 *분산 동역학* 청사진(Lyu fluid-sub보다 콜로이드에 적합).

### B-4. ★ Bayesian force-field 보정 — 우리 E_eff 연화의 *대안 방법론* (단 철학 차이 인지)
- 그들은 **재료 E를 직접 안 주고** Bayesian 다목적 최적화(eq 2.12)로 **force field 전체를 실험 밀도·porosity에 보정**(chemistry-neutral). 우리는 **재료 E 명시(24) + 18× 연화(→1.35)** 로 거시 porosity(Minnmann)에 맞춤.
- **→ 매핑**: ★ **두 방법은 *같은 목표(거시 보정), 다른 수단*.** 그들 Bayesian = *force field를 데이터에 fit*; 우리 = *물리적 연화 인자*. **우리 18× 연화가 *물리적 의미*(granular 재배열 프록시)를 갖는 반면, 그들 Bayesian-fit force field는 *블랙박스*** — ⇒ **우리 방식이 *더 해석가능*** (frame[2] 연화의 물리적 정당화 = 우리 강점). 단 **Bayesian 다목적 보정 *틀* 자체**는 우리가 *여러* 앵커(porosity + Cronau overlap + SEM)에 *동시* 보정할 때 참고(현재 우리는 순차 보정). ⚠ 흡수 시 *해석가능성 유지* — 블랙박스 fit로 가지 말 것.

### B-5. 종합 정리 — 우리가 가져갈 것 / 안 가져갈 것
- **가져갈 것**: ① **resolved-multisphere AM을 *대표 케이스*에 (B-1)** — 비구형 packing 사실성(production 전면 X, 비용); ② **그들 Fig 7 한계 진술 *인용* (B-2)** — 우리 MPM coverage 우위 강화; ③ **graded-z 제조-유래 근거 (B-3가)** — Phase-5; ④ **Bayesian 다중앵커 보정 *틀* (B-4)** — 단 해석가능성 유지.
- **안 가져갈 것**: ① **강체 multisphere를 production 전면** — 비용 + 소성 상실(우리 MPM 강점 버림); ② **습식 건조 동역학** — ASSB 건식이라 원천 무관(D5 약연결만); ③ **연속체 GeoDict σ** — 우리 constriction-RNM이 더 정밀; ④ **무차원 σ** — 우리 절대 mS/cm가 더 유용; ⑤ **Bayesian *블랙박스* fit** — 우리 물리적 연화가 더 해석가능.
- **결론**: ★ **본 논문에서 우리가 *실제로 흡수*할 핵심 = (i) resolved AM 형상 *방법*(multisphere, 대표 케이스용) + (ii) 그들이 자인한 "강체-구는 계면 못 자람" 한계 진술(우리 MPM 정당화) + (iii) graded-z 제조-유래 근거.** 나머지(연속체 σ·습식·블랙박스 보정)는 우리가 *이미 더 낫거나* 셀화학상 무관.

---

## ★ 우리 novelty — 왜 우리가 state-of-the-art인가 (our novelty vs this DEM model)

> 사용자 mandatory 섹션 C. 사용자가 firm한 DEM novelty를 원함 — **우리가 SOTA임을 분명히 주장.** 7개 차별점을 Weitze 2024 대비 매핑. ★ **이 논문은 가장 까다로운 비교상대** — *resolved AM 형상*(우리 미보유)을 갖고 transport도 *수치*로 풀기 때문. 그러나 **형상이 *강체*(소성 없음)이고 σ가 *연속체 상한*(constriction 없음)이며 σ_thermal·fracture·예측기가 없다** → 핵심 transport·소성·예측 축에서 *여전히* 우리가 SOTA. 정직하게 그들이 앞서는 칸(resolved 형상·습식)도 명시. evidence-based.

**총평: Weitze 2024는 "resolved(실제 형상) AM + 습식 ASSB 제조 + 수치 σ"를 *처음* 결합한 야심찬 논문이고, *AM 형상 사실성·습식 전체사슬*에서 우리보다 앞선다. 그러나 (i) 형상이 *강체*라 *소성 변형·계면 성장*을 못 잡고(저자 Fig 7 자인), (ii) σ가 *연속체*라 *점접촉 constriction*을 빼서 *상한*만 주며, (iii) σ_thermal·fracture·Heckel·Z·dip·예측기가 없다. 우리는 (i) MPM J2로 *진짜 소성 형상변화*(저자가 못 한 그 계면성장), (ii) Kirchhoff/Holm constriction *삼중항*(절대 mS/cm), (iii) fracture·literature σ_grain·dual-model·LOOCV 예측기를 보유 → *transport·소성·예측* 축에서 명백히 SOTA. 그들 우위(resolved 형상·습식)는 *직교하는 강점*이지 우리 핵심을 잠식하지 않으며, 둘의 이상적 결합 = '우리 constriction-RNM을 그들 resolved 형상 위에서'.**

**(1) 전달 TRIAD σ_ionic + σ_e + σ_thermal — 명시 Kirchhoff/Holm *constriction* 솔버, 절대 mS/cm (★ 가장 강한 우위)**
- **그들**: GeoDict DiffuDict(이온)·ConductoDict(전자) = **연속체 voxel** σ — **(i) 점접촉 수렴저항(Holm/Greenwood) 없음 → σ_eff *상한***, **(ii) σ_thermal 없음**, **(iii) 무차원**(상 벌크=1). ★ `⚠정정2026-08-19` **초판의 "그들조차 future work 로 constriction/contact 저항을 시사" 는 근거가 없다** — 본문·SI 에 "constriction"·"Greenwood" 는 **0회**이고, 그들이 적은 향후과제는 *"porosity as a function of calendering pressure, conductivities, and cracking of secondary particles"* 뿐이다.  ⇒ **그 문장을 인용하지 말 것**(대신 쓸 수 있는 자인 = "겹침을 허용하지 않는 force field 는 setback").
- **우리**: **3채널 모두**(σ_ionic LOOCV 0.975 / σ_e 0.953 / σ_thermal 0.903), **명시 접촉망 Kirchhoff + Holm R=1/(2σr_c) 구속저항 + Stage-E 소성면적**, **절대 mS/cm**. ⇒ **constriction·열전도·절대값 = 명백한 우리 SOTA.** ★ **그룹-진화 논거**: Franco/Janek-계열이 Bielefeld2019(σ 없음)→**Weitze2024/Bielefeld2020(연속체 상한 σ)**→Bazzoun2026(RNM constriction)→우리(constriction 삼중항)로 정교화 — 우리가 *그 끝*.

**(2) Stage-E 소성 접촉 AREA 재유도**
- **그들**: 계면면적 = **GeoDict voxel 기하면적**(Fig 7) — 그런데 *강체-구라 접촉 후 안 자람*(Fig 7 반직관). 소성 pile-up·Tabor 면적 재유도 *없음*.
- **우리**: **Stage-E(Tabor F/H + volume V/h 소성 접촉면적)** 로 *압밀 중 계면 성장*을 정량(real_14 Tabor coverage AM_P/S 49.6/48.2 %, 압밀↑→coverage↑). ⇒ ★ **그들 Fig 7이 "못 잡는다"고 한 *바로 그 상-상 계면 성장*을 우리가 *수치로 보유*** — 가장 직접적인 차별점.

**(3) DEM↔MPM scaffold 커플링 + 진짜 소성 MORPHOLOGY (J2) ★ — 그들 resolved-형상의 *결정적 빈칸*을 메움**
- **그들**: AM 형상은 **resolved(실제)이되 *강체*(harmonic bond)** — 압밀 중 **형상 변화·void-fill·계면성장 *없음*.** ★ **저자 Fig 7에서 *직접 자인***: "spherical [and rigid] nature → 압축해도 binder·SE가 *deform·계면증가를 안 함* = 비현실적." **즉 *형상을 실제로 넣고도* 소성을 못 잡음** — frame[1]/[2]의 *가장 강력한* 외부 증거(Varkey "구=타협"보다 강함, *형상까지 넣었는데도* 소성 부재).
- **우리**: **MPM 진짜 J2 소성 형상변화**(SEM 코어보존+경계평탄화 ✓), **부피보존 void-fill flow**(porosity를 rigid floor 아래로), **DEM AM 골격 + SE만 MPM(scaffold)** 커플링. ⇒ ★ **그들이 "resolved 형상으로도 못 한" 소성 계면성장·void-fill을 우리 MPM이 *정확히* 메움.** **형상-소성 = 우리 고유** — 그들 resolved *정적* 형상과 *직교*(이상적 결합 = 우리 MPM SE 소성 + 그들 multisphere AM).

**(4) fracture-aware transport (Auerbach + Lawn)**
- **그들**: 입자 fracture **안 넣음**(그룹 선행 ref [38] Xu가 *LIB* 압연 fracture를 했으나 본 논문은 *제외*). 본문이 "future = cracking of secondary particles" + "압연압 무한↑ 못함(AM 균열 유발)[53,56]"으로 *한계·향후만*.
- **우리**: **Auerbach 임계 + Lawn 미세균열 → fracture-aware Holm**(f_intact로 σ 부분전도 보정; 깨진 접촉도 ~60 % 미세접촉 유지). ⇒ ★ **그들 "AM 균열 고려필요"를 우리는 *fracture 솔버로 정량*** + *transport에 연결*(그들은 미보유).

**(5) 문헌-근거 σ_grain (Cronau) + 절대 σ 앵커**
- **그들**: σ가 **무차원**(SE 벌크=1) — **σ_grain 절대값·입계·crystallinity 인자 *없음***(정규화로 소거). 실험 σ 절대값과 *비교 불가*. `⚠정정2026-08-19` **단, 무차원 값은 정의상 *형성인자* F = σ_eff/σ_bulk 이므로 F·MacMullin 축에서는 직접 비교된다** — 그들 F_ion = 1.35×10⁻²(N_M 74) vs Bazzoun 실험 0.134(N_M 7.5) vs 우리 STEP3 0.052–0.166(N_M 6–19).  전자 축만 CBD 벌크 σ 미보고라 불가.  심화 §③-C.
- **우리**: **σ_grain=3.0 mS/cm × Cronau(r_SE)** — Cronau 단결정 문헌값 + sub-µm amorphization 입계 인자, **절대 mS/cm** → Bazzoun 0.137·Minnmann 0.17 등 실험과 *직접 앵커*. ⇒ ★ **절대 σ·재료-근거 σ_grain = 우리 보유, 그들 무차원이라 미보유.**

**(6) 실험-anchored INDEPENDENT dual-model frame[4]/[5]**
- **그들**: **단일 DEM 모델**(Bayesian로 밀도·porosity 2점 보정 + GeoDict σ). 독립 2모델 교차검증 없음. MPM 없음.
- **우리**: **DEM(전달) + MPM(역학/형상)** 을 *각각 독립적으로 실험에 보정*(Minnmann·Cronau·Bazzoun) — *서로 cross-fit 안 함*(frame[4]). 수렴=교차검증(예: real_14 DEM 15.6 ↔ MPM 16.7 % ↔ Minnmann anchor), 발산=정량화된 모델한계. ⇒ ★ **이중모델 메타-검증 = 우리 고유**(그들 단일 모델).

**(7) 솔버→스케일링 법칙 LOOCV 압축**
- **그들**: **case-by-case 시뮬**(압연도마다 GeoDict 재계산). 예측 법칙·ML 압축 *없음*.
- **우리**: 네트워크 솔버 출력 → **스케일링 법칙(LOOCV 0.90–0.98) + grade_engine** + (Phase 3–5) design-knob→metric 예측기 → 2D synth → layered. ⇒ ★ **솔버를 *예측 가능한 법칙으로 압축* = 우리 고유**(그들 시뮬-마다).

**⚖️ 정직하게 — 그들이 우리보다 앞선 곳 (over-claim 방지):**
- **(가) ★ resolved(실제 형상) AM** — nano-CT multisphere로 *진짜 다결정 NMC 외형*. **우리는 완전 구**(MPM scaffold로 형상 우회). ★ **이건 그들이 *명확히* 앞서는 칸** — *정적 미세구조의 기하 사실성*(실제 packing·계면 위치·CC-근처 AM결핍). 우리 구-가정이 근사하는 부분을 그들은 직접. (단 *강체*라 *소성*은 없음 — 형상↔소성 직교.)
- **(나) 습식공정 전체사슬(슬러리→건조→압연)** — Langevin 슬러리 + CBD 축소 건조. **우리 미보유.** ⚠ 단 ASSB는 *건식*이 주류(저자도 §1에서 습식 SE-wetting 단점 인정) → *셀화학상 경로가 다름*(우리 dry-process가 현 주류). "뒤처졌다" 아니라 *다른 경로*.
- **(다) 같은 소재계(LPSCl ASSB) + transport 수치** — Lyu(LIB·σ정성)·Sangrós(LIB)보다 *우리에 가까운*(ASSB·수치 σ) peer. 단 *연속체 상한·무차원*이라 우리 constriction·절대값보다 *덜 정밀*.
- ⚠ **(가)(나)(다) 모두**: 형상은 *강체*(소성 X), σ는 *연속체 상한·무차원*(constriction X, 절대값 X), 그리고 **σ_thermal·fracture·Heckel·Z·dip·예측기 전부 없음** → **transport(constriction 삼중항)·소성 morphology·예측 축에서 우리가 SOTA**라는 결론은 *확고히* 유지. 그들 우위 = *형상 사실성·습식*(직교 강점), 우리 우위 = *constriction σ·형상소성·fracture·dual-model·예측*.

### ★ 종합 positioning (한 문단, deck용)
"Weitze·Zanotto·Zapata·Franco (2024, LRCS/ARTISTIC) 는 **실제 형상(nano-CT multisphere) AM + 습식(슬러리→건조→압연) ASSB 양극 제조**를 *처음* DEM(LAMMPS)으로 시뮬하고 **GeoDict 연속체로 σ_ionic·σ_e**를 산출해, *AM 형상 사실성*에서 우리(완전 구)를 앞선다. 그러나 그 형상은 **harmonic bond로 *강체*** 라 — 저자 스스로 Fig 7에서 *'구형·강체라 압축해도 binder·SE 계면이 못 자란다 = 우리 모델 한계'*라고 자인하듯 — **소성 변형·계면 성장·void-fill을 못 잡고**, σ는 **연속체(점접촉 constriction 없음 = 상한)·무차원**이며 **σ_thermal·fracture·Heckel·dip·예측기가 없다.** 우리 ASSB DEM+MPM 은 *같은 LPSCl 소재계*에서 그 빈칸을 정면으로 메운다: ① **Kirchhoff/Holm *constriction* σ 삼중항(절대 mS/cm)** — 그들 연속체 상한을 아래로 깎고 열전도까지(Franco/Janek-계열 Bielefeld2019→Weitze2024/Bielefeld2020 연속체→Bazzoun2026 RNM→우리 constriction 삼중항 궤적의 *끝*); ② **MPM J2 *진짜 소성* morphology** — 그들이 *형상까지 넣고도 못 한* 바로 그 계면성장·void-fill(SEM ✓); ③ **fracture·literature σ_grain·dual-model·LOOCV 예측기.** 정직히 **resolved 형상·습식은 그들이 앞서지만**(직교 강점 — ASSB 건식엔 습식이 비주류), 그건 *정적 기하 사실성*이지 우리 핵심(*동적 소성* + *constriction transport* + *예측*)을 잠식하지 않는다. **이상적 미래 = 우리 constriction-RNM·MPM 소성을 그들 resolved 형상 위에 결합.**"

---

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① ★ **paper 대조축 — "resolved-shape ASSB peer(Weitze 2024)조차 *강체-구*라 소성 계면성장을 못 잡는다(Fig 7 자인) → 우리 MPM이 그 칸"**: frame[1]/[2]의 *가장 강력한* 외부 증거(Varkey "구=타협"보다 강함 — *형상까지 넣었는데도* 소성 부재). 우리 MPM 형상소성·Stage-E coverage 정당화에 1순위 인용.
- ② ★ **transport positioning — Franco/Janek 그룹-진화의 끝**: Bielefeld2019(σ 없음)→Weitze2024/Bielefeld2020(연속체 상한 σ)→Bazzoun2026(RNM constriction)→우리(constriction 삼중항+열+절대값+예측기). **본 논문 = "연속체 상한" 단계** — 우리·Bazzoun이 constriction을 되돌려 넣음. *같은 그룹이 우리 방향으로 진화*한다는 positioning 최강 근거.
- ③ ★ **resolved-AM *방법* 흡수(대표 케이스용, B-1)**: LIGGGHTS `multisphere` fix로 비구형 AM packing을 *검증 케이스*에 (production 전면 X — 비용 + 소성 상실). **SE 소성은 계속 MPM** → "비구형 AM packing = 그들 multisphere, SE 소성 = 우리 MPM" 결합.
- ④ **graded-z 제조-유래 근거(Fig 5, B-3가)**: CC-근처 AM 결핍·두께방향 조성구배가 *제조 물리로 자연발생* → 우리 Phase-5 layered/graded-z synth가 *인위적이 아니라 제조-실재*임을 인용.
- ⑤ **Bayesian 다중앵커 보정 *틀*(B-4)**: 우리가 여러 앵커(porosity+Cronau+SEM)에 *동시* 보정할 때 참고 — 단 *해석가능성 유지*(우리 18× 연화의 물리적 의미 vs 그들 블랙박스 fit).
- ⑥ ★ **ASSB 습식 단점 = 우리 dry-process 정당화(A-4)**: 저자 §1이 "습식은 SE가 AM을 못 적셔 계면 문제·capacity fade[13,14]" 자인 → 우리 건식 경로(Lee2025 co-rolling)가 *그 문제를 회피*하는 이유.
- ⑦ **데이터** `⚠정정2026-08-19` **(심화 §③-C 가 10항목 앵커표로 확장)**: `docs/data/wet_processing_resolved_am.csv` — porosity(0.578→0.291 10점, 압연도)·σ_ionic/σ_e(무차원, 압연도)·계면면적 6종(Fig 7)·슬러리밀도(1.353 vs 1.34)·건조 porosity(0.53 vs 0.57)·두께(22→110→40 µm)·조성(75/17.5/5/2.5 wt%). **⚠ σ 무차원(절대 mS/cm 없음); 압연도≠압력(MPa); resolved이되 강체; nano-CT 소재≠슬러리 소재 → 절대 σ·porosity·압력 ASSB-production 전이 금지, 추세·방법·형상-한계 대조용.**

## 9. 인용 가능 문장 (deck/paper용)
- "Weitze, Zanotto, Zapata Dominguez and Franco (2024, LRCS/ARTISTIC) presented the **first simulation of *wet-processed* solid-state-battery cathode manufacturing (a Ni-rich NMC printed as LiNi₉Mn₀.₅Co₀.₅O₂ + LPSCl + carbon + PIB; **NMC622 is only the nano-CT shape donor**) with *resolved active-material geometries*** — realistic polycrystalline NMC shapes extracted from nano-CT by Weka segmentation and represented as **multisphere clusters held rigid by artificial harmonic bonds (eq 2.10)** — run through a slurry→drying→calendering DEM in LAMMPS (Langevin + Lennard-Jones + JKR), force-field-calibrated to experimental slurry density (1.353 vs 1.34 g/cm³) and dry porosity (0.53 vs 0.57) by Bayesian optimization, with **ionic and electronic conductivities computed by GeoDict continuum solvers (DiffuDict/ConductoDict)**."
- "Crucially, their AM particles are **resolved in shape but *rigid***: a key result (Fig 7) is the *counter-intuitive* finding that calendering does **not** grow the inter-phase (e.g. AM–SE) interfacial area, which the authors **explicitly attribute to a model limitation** — *'on account of the spherical [and rigid] nature of these particles, two phases will not be able to increase their contact area'*. This is the **strongest external evidence for frame [1]/[2]**: even a model that puts in the *real shape* cannot capture the plastic deformation and interfacial growth that our **MPM (true J2 shape flow) + Stage-E plastic contact area** supply."
- "Their conductivity is solved on a **continuum GeoDict grid (no point-contact constriction) and reported dimensionlessly** (phase bulk σ = 1), i.e. an **upper bound** of the rigid-contact granular network. Our **explicit Kirchhoff/Holm constriction-resistance triad (σ_ionic/σ_e/σ_thermal, absolute mS/cm)** narrows that bound and adds thermal transport — placing our work at the *end* of the Franco/Janek group trajectory (Bielefeld 2019 no-σ → Weitze 2024 / Bielefeld 2020 continuum-σ → Bazzoun 2026 RNM-constriction → ours constriction-triad)."
- "Both we and Weitze (2024) find ASSB **densification raises σ_ionic** (SE-network conductor, porosity detrimental) — the *opposite* of the Li-ion peers (Lyu/Sangrós, pore-conductor) — confirming our all-solid-state transport framing on the *same LPSCl chemistry*."

## 10. 주의/한계 (over-claim 방지)
- **★ resolved 형상 ≠ 형상 *소성***: AM은 multisphere로 *형상은 실제*이되 **harmonic bond로 *강체*(eq 2.10) = 영원히 안 변함.** **CONTACT 소성조차 없음**(JKR = 탄성+점착, 항복캡 없음; δ는 기하 프록시). *진짜 SHAPE flow·void-fill·계면성장 없음*(저자 Fig 7 자인). → "그들이 형상을 넣었으니 소성도 있다"고 *오독 금지*.
- **★ σ = *연속체*(GeoDict, constriction 없음) + *무차원***: SE-SE 점접촉 수렴저항(Holm/Greenwood) 안 풂 → *방법 수준* **σ_eff 상한** `⚠정정2026-08-19`(**결과 수준은 실험의 1/10** — 심화 §②-4). 상 벌크 σ=1로 정규화 → **절대 mS/cm 없음** → Bazzoun 0.137·Minnmann 0.17·우리 0.04–0.18 등과 **절대 비교 *불가***, *압연도-추세*만. `⚠정정2026-08-19` **단, 무차원 값은 정의상 *형성인자* F = σ_eff/σ_bulk 이므로 F·MacMullin 축에서는 직접 비교된다** — 그들 F_ion = 1.35×10⁻²(N_M 74) vs Bazzoun 실험 0.134(N_M 7.5) vs 우리 STEP3 0.052–0.166(N_M 6–19).  전자 축만 CBD 벌크 σ 미보고라 불가.  심화 §③-C. σ_thermal 없음.
- **★ 압연도(% 두께) ≠ 압력(MPa)**: Fig 6/8의 x축은 *압연도(두께 감소율)*지 *절대압*. **Heckel·P_y·절대응력 미보고** → 우리 Heckel(P_y=138)·P-vs-porosity와 *직접 겹치기 불가*. porosity floor 0.30(@45 % 압연)도 *압력 불명*이라 우리 10–15.6 %(@300 MPa)와 *절대 비교 금지*(압연도≠압력 + 강체-구 + 습식 잔류공극 + 연속체).
- **★ nano-CT 소재 ≠ 슬러리 소재** `⚠정정2026-08-19`: 형상 추출용 nano-CT 가 **NMC622**(LiNi₀.₆Mn₀.₂Co₀.₂O₂)이고 **슬러리 AM 이 다른 (Ni-rich) 소재**다 — 초판은 방향을 반대로 적었다. → 형상은 *대표적*이지 *그 슬러리의 실측 형상은 아님*(저자 명시). SE 형상은 *구로 가정*(nano-CT gray로 SE/CBD 구별 불가, AM만 resolved).
- **★ 입자 coarsening**: 고해상 multisphere는 *계산비로 안 씀* → pixel-averaging 조대화(Fig 3). 형상은 "coarse한 resolved"(완전 구보다 실제적이되 고해상 형상 아님). **proof-of-concept / limited computational resources** 저자 반복 명시.
- **건조 = CBD 입자축소(eq 2.11), 저건조속도 모델**: 명시 모세관력·표면장력·convection-diffusion 없음(ref [29,30,31,32]가 그걸 함 — 본 논문 scope 밖). 고속건조 비균질·crack 미반영. AM·SE는 건조 중 안 변함, CBD만 축소.
- **CBD = 균질 carbon+binder 구**: 명시 입자-입자 bond 없음(Sangrós eq10–13/Lyu parallel-bond 아님). binder가 *접착 bond*가 아니라 *콜로이드 입자상*(LJ/JKR). PTFE fibril/SuperP 응집 *morphology 효과 없음*.
- **E_AM/E_SE/σ_y/ν 절대값 미보고**: Bayesian로 force field를 밀도·porosity에 *보정*(chemistry-neutral) → 재료 E가 *입력*이 아님. → 우리 E_eff·Sangrós 나노압입과 *방법 철학 정반대*(블랙박스 fit vs 물리적 연화/실측).
- **Z·Heckel·coverage(우리식)·fabric tensor·내부응력 없음**: Lyu/Sangrós보다 역학 후처리 *적음*(porosity·계면·σ-추세 중심). **검증 = 밀도·건조 porosity 2점**(절대 σ 실측 검증 없음 — 무차원).
- **CAM = Ni-rich NMC(`LiNi₉Mn₀.₅Co₀.₅O₂` 인쇄 그대로) + LPSCl** `⚠정정2026-08-19`: 인쇄된 첨자는 화학량론이 안 맞아 **오식으로 보이나 단정 불가** → CAM 조성을 정량 인용하지 말 것.  NMC622 는 **형상 공여체**의 조성이다. 셀화학은 *거의 같으나*(LPSCl ASSB) AM·바인더·도전제 종류 차이 → 절대 porosity·σ 전이 시 주의.
- **Fig 6/7/8 값 일부 digitized**(그래프에서 읽음) → **추세만(±)**. **stated**: 슬러리밀도 1.353/1.34, 건조 porosity 0.53/0.57, porosity 압연 0.57→0.30; **두께 22/110/40 µm 는 digitized(Fig 4 라벨)** `⚠정정2026-08-19`, 조성 75/17.5/5/2.5 wt%, 고체분율 50 %, PIB 9 wt%. **σ_ionic/σ_e/계면면적 절대값은 digitized + 무차원**(Fig 7/8).

## ★★ 2026-08-19 심화 — 원문 PDF + SI 재판독

> 2026-06-26 초판 digest 는 본문만 봤다.  이번에 **출판본 PDF 전문(10 pp) + SI 본문(mmc1, force-field·JKR·PSD 표)**
> 을 재판독했다.  SI 영상 3건(`mmc2/3/4.mp4`, 압연·springback 진화)은 **존재만 기록**하고 열지 않았다.
> 아래는 (0) 초판 정정, (①) solid-state 구현의 기계적 해부, (②) 축별 우열 판정, (③) 우리 차별점·앵커 목록 순.
> **stated = 논문/SI 에 적힌 값 · digitized = 그림에서 읽은 값(±, TREND only) · 우리 산출 = 이 카드의 산술**.
> 논문·SI 에 없는 것은 **n/a — 미보고**로 명시했다 (§F1).

### 0. 초판 digest 정정 6건 + 신규 소득

| # | 초판 서술 | 재판독 결과 | 근거 |
|---|---|---|---|
| **C1** | AM = **NMC622** LiNi₀.₆Mn₀.₂Co₀.₂O₂ 75 wt% | **반대다.** 슬러리 AM 은 초록·§2.1 에 **`LiNi₉Mn₀.₅Co₀.₅O₂`(인쇄 그대로)** = **Ni-rich**(첨자 그대로면 화학량론 불성립 → **논문 오식**, NMC-90/05/05 의 오식일 가능성이 크나 **단정 불가**).  **NMC622 는 nano-CT *형상 공여체*일 뿐**이고 §2.2 가 *"this is not the same material as used in the slurry formulation"* 라고 **명시**한다 | PDF 초록·§2.1(이미지로 확인: `LiNi₉Mn₀.₅Co₀.₅O₂`) vs §2.2 |
| **C2** | 두께 = 슬러리 22 µm → **건조 110 µm** → 압연 40 µm | **오독.** Fig 4 라벨: 평형 **슬러리 기둥 = 22 µm 폭 × 110 µm 높이** → **건조 전극 = 22 × 40 µm** → 압연 박스도 40 µm.  즉 **110 → 40 µm 은 *건조 수축*** (2.75×), 압연은 그 40 µm 안에서 일어난다 | Fig 4 (digitized 라벨) |
| **C3** | "GeoDict 연속체 = constriction 없음 → σ_eff **상한**" | **결과 수준에서는 상한이 아니다.** 그들의 이온 형성인자 F=σ_eff/σ_bulk 는 **1.35×10⁻²** 로 같은 소재계 실험(Bazzoun 0.137/1.02 = **0.134**)의 **1/10**, Bruggeman 유효매질 추정의 **1/5.6** 이다.  ⇒ **방법 수준의 상한 논거**(접촉저항 항 부재)와 **결과 수준의 값**(실험보다 훨씬 낮다)을 **분리해 써야 한다**.  §심화 ②-4 참조 | §2.5 + Fig 8 digitized + Bazzoun 카드 |
| **C4** | "σ 무차원 → 절대 비교 **불가**" | **절반만 맞다.** 무차원 값은 정의상 **형성인자(formation factor) F = σ_eff/σ_bulk** 이므로 **F·MacMullin 축에서는 직접 비교된다**(이온 축 대조 완료).  **전자 축만** CBD bulk σ 미보고 → 환산 불가 | §2.5 정규화 정의 |
| **C5** | AM PSD "명시 D10/D50/D90 없음" | **SI 에 명시**: AM = **Gaussian µ = 4.5 µm, sd = 0.79 µm, [3, 6] µm 밖은 제외**; **SE = 단분산 Ø 1.0 µm** (LPSCl fine, NEI Corp.) | SI "Particle Size Distribution" |
| **C6** | Fig 7 "AM-SE ~1, **거의 일정**" | 값은 맞으나 추세는 **미증가(+16 %)**: AM–SE 는 1.08 → 1.25 로 **유일하게 오르는 상-상 계면**이다(오차막대 안팎).  CBD–SE 1.95→1.82, CBD–AM 0.72→0.68 은 **평/하락** | Fig 7 digitized(9점) |

**신규 소득(초판에 없던 것)**: SI JKR/LJ/harmonic 전 표 + 단위환산 · **E_pair = 135 GPa** · **γ = 1000 J/m²** · CBD 건조 수축 **Ø2.438 → 0.7 µm** · **압연도별 porosity 10점** · **springback 회복률(우리 산출) 10–15 %** · **F_ion / F_e 9점** · **φ_SE ≈ 0.15→0.18(Fig 5)** → **τ_SE ≈ 375 → 13** · **저자 자인 3건**("energy was unable to reach full equilibrium" / "we would expect even higher values for larger interfacial areas" / "force field parameters that do not allow for a high degree of overlap ... a setback").

---

### ① solid-state 를 어떻게 구현했나 — 기계적으로 정확히

#### ①-A 상(phase) 표현 — **resolved 된 것은 AM 하나뿐이다**

| 상 | 표현 | 입경 | 개수 | 부피분율 |
|---|---|---|---|---|
| **AM** (`LiNi₉Mn₀.₅Co₀.₅O₂` 인쇄 그대로) | **multisphere** — nano-CT(다른 소재 **NMC622**)에서 뽑은 2차입자 외형을 **겹친 1차 구 + harmonic bond 로 강체 고정** | **2차입자 Gaussian 4.5 ± 0.79 µm, [3,6] 절단**(SI) · 1차 구 ≈ **Ø0.97 µm**(LJ σ_NMC, SI) | **n/a**.  우리 산출 자릿수: 4.5 µm 2차입자 ÷ pitch 0.98 µm ⇒ **1차 구 ~50개/입자** | digitized(Fig 5) 중앙 plateau **0.27 (압연 5 %) → 0.35 (45 %)** |
| **SE** (LPSCl fine, NEI Corp.) | ★ **완전 구, 단분산** | **Ø 1.0 µm**(SI, stated) | n/a | digitized **0.15 → 0.18** (CC 근처 첨두 0.20 → 0.39) |
| **CBD** (C65 + PIB 균질 혼합 1상) | **완전 구** | 슬러리 **Ø 2.438 µm** → 건조 **Ø 0.7 µm** (LJ σ_CBD, SI — eq 2.11 의 지름축소를 정량화한 유일한 수치) | n/a | digitized **0.075 → 0.10** (CC 근처 0.15–0.175) |
| **Pore** | 나머지 | — | — | **0.578 → 0.291** (Fig 6, digitized 10점) |

★★ **가장 중요한 정정성 관찰**: nano-CT 의 gray scale 이 **SE·carbon·binder 를 서로 구별하지 못해서**(§2.2 명시) **SE 형상은 resolved 되지 않았다** — 논문 자신의 문장: *"Carbon additives, binder and solid electrolyte were indistinguishable to nano-CT imaging from one another, **which limits the use of realistic SE particle shapes in our simulations**."*
⇒ **ASSB 이온수송을 지배하는 상(SE)은 그들도 우리와 똑같은 단분산 구다.**  "이 논문은 형상이 resolved 다"는 서술을 **이온 축에 그대로 옮기면 틀린다** (초판 카드의 §0·A-1 이 이 구분을 흐리게 썼다 — ②-1/②-2 에서 축을 갈라 고쳤다).

#### ①-B 접촉모델 — SI 전 표 + 단위환산 + 물리 해설

**단위 규약**(SI 표 각주, LAMMPS pg·µm·µs 계): ε [pg µm² µs⁻²] · σ, r_c [µm] · γ, κ [pg µs⁻²] · k_t [pg µm⁻¹ µs⁻²].
**우리 환산**(SI 로 곱): 에너지 1 pg µm²/µs² = **1×10⁻¹⁵ J** · 응력 1 pg µm⁻¹ µs⁻² = **1 kPa** · 표면에너지밀도 1 pg µs⁻² = **1 mJ/m²** · 스프링상수 1 pg µs⁻² = **1×10⁻³ N/m**.
⚠ **SI 는 E 의 단위를 `pg µs⁻²`(=표면에너지 단위)로 적었다 — 차원이 맞지 않는다.**  k_t 와 같은 응력 단위 `pg µm⁻¹ µs⁻²` 의 오식으로 읽어야 물리적이며, 아래 GPa 환산은 **그 가정 위의 우리 환산**이다.

**(1) Lennard-Jones (eq 2.4–2.6) — 단계마다 통째로 바뀌는 fit 노브**

| 단계 | ε_NMC | σ_NMC | r_c,NMC | ε_SE | σ_SE | r_c,SE | ε_CBD | σ_CBD | r_c,CBD |
|---|---|---|---|---|---|---|---|---|---|
| **슬러리** (SI T1) | **15.1** | 0.97 | 2.5 | **10.5** | 1.0 | 2.5 | **55.1** | **2.438** | 7.5 |
| **건조** (SI T4) | **150 000** | 0.97 | 2.5 | **150 000** | 1.0 | 2.5 | **150 000** | **0.7** | 2.5 |
| **압연** (SI T6) | **75 000** | 0.97 | 2.5 | **75 000** | 1.0 | 2.5 | **100 000** | 0.7 | 2.5 |

- ε = 퍼텐셜 우물 깊이(인력 세기), σ = U=0 이 되는 거리(≈ 입자 지름 — **σ_SE = 1.0 이 SI 의 SE 지름 1 µm 와 정확히 일치**해 이 읽기가 확인된다), r_c = 절단반경.  이종쌍은 ε 기하평균 · σ 산술평균(eq 2.5/2.6); **r_c 의 혼합규칙은 미보고(n/a)**.
- ★★ **ε 가 단계 사이에서 10⁴ 배 뛴다** (NMC 15.1 → 150 000 → 75 000).  ⇒ **LJ 는 재료 상수가 아니라 *단계별 fit 노브*** 이고, 본문의 *"The force field parameters between all particles are recalibrated in order to attain experimental porosities"* 가 SI 수치로 확인된다.
- **우리 환산**: ε_슬러리 = 1.51×10⁻¹⁴ J, ε_건조 = 1.5×10⁻¹⁰ J.  참고로 kT(300 K) = 4.14×10⁻²¹ J (**Langevin 온도는 논문·SI 모두 미보고 n/a** — 300 K 는 눈금용).  ⇒ 어느 단계에서도 LJ 우물이 열에너지보다 **10³–10¹⁰ 배** 깊다 = **eq 2.2 의 Brownian 항 η(t) 는 구조를 결정하지 못한다**(CG 입자라 ε≫kT 자체는 정상이나, "슬러리 = Brownian 분산" 이라는 서술의 실효는 그만큼 약하다).
- ★ **σ_CBD 2.438 → 0.7 µm 이 eq 2.11 "particle shrinking" 건조의 유일한 정량치** — 지름비 3.48× = **부피비 42×**(우리 산출).

**(2) JKR 접촉 (eq 2.7–2.9)** — 표의 E·γ 는 위 단위 가정 하의 우리 환산을 괄호로 병기

| 단계 | 쌍 | **E** | η_n0 | ν | **γ** | k_t | x_γ,t | µ_s |
|---|---|---|---|---|---|---|---|---|
| **슬러리** (SI T2) | CBD–CBD | 1 **(1 kPa)** | 10 | 0.3 | 82 **(0.082 J/m²)** | 5.0 | 1.0 | 0.5 |
| | **NMC–NMC · NMC–SE · SE–SE** | **135×10⁶ (≈ 135 GPa)** | 500 | 0.3 | **1×10⁶ (≈ 1000 J/m²)** | 800 | 1.0 | 0.5 |
| | CBD–NMC · CBD–SE | 20 **(20 kPa)** | 10 | 0.3 | 52 **(0.052 J/m²)** | 5.0 | 1.0 | 0.5 |
| **건조** (SI T5) | CBD–CBD | 5 **(5 kPa)** | 1 | 0.3 | 2 **(0.002 J/m²)** | 5.0 | 1.0 | 0.5 |
| | **NMC/SE 3쌍** | **135×10⁶** | **50** | 0.3 | **1×10⁶** | 800 | 1.0 | 0.5 |
| | CBD–NMC · CBD–SE | 5 | 1 | 0.3 | 2 | 5.0 | 1.0 | 0.5 |
| **압연** (SI T7) | — | **건조 단계와 완전히 동일** | | | | | | |

물리 해설(항별):
- **E** = eq 2.8 의 *쌍-유효* 영률.  ★★ **AM–AM · AM–SE · SE–SE 가 전부 135 GPa 한 값**이다 = **AM 도 SE 도 벌크 산화물급 강성**.  실제 LPSCl 은 E ≈ 22–24 GPa(우리 DFT E_VRH 22.06 / Sakuda 24), 우리 DEM 유효값은 **1.35 GPa** — ⇒ **그들 SE 접촉은 실물의 ~6배, 우리 규약의 ~100배 뻣뻣하다.**  저자도 Fig 6 논의에서 *"the pores begin to close, **on account of the high Young's modulus of the material phases**"* 라고 이 사실을 스스로 쓴다 (= 입자는 안 변하고 공극만 닫힌다).
- **γ** = JKR 표면에너지밀도(점착).  AM/SE 쌍 **≈ 1000 J/m²** 는 물리적 vdW 표면에너지(0.05–1 J/m²)나 Bucci LPSCl G_c 2.8 J/m² 보다 **10²–10⁴ 배** 크다 ⇒ **재료 상수가 아니라 수치 응집항**.  우리 산출 pull-off 력 F_c = (3/2)πγR_eff = **≈ 1.1 mN/접촉** (R_eff = 0.2425 µm 기준).  반대로 **CBD 쌍의 γ(0.05–0.08 J/m²)는 물리적 vdW 범위** — 즉 같은 SI 안에서 CBD 는 물리값, AM/SE 는 수치값이라 **범주가 섞여 있다**.
- **ν = 0.3 · µ_s = 0.5 · x_γ,t = 1.0** 이 모든 쌍·모든 단계에서 동일.  ν = 0.3 은 **우리 DEM 접촉모델 입력과 같은 선택**이다(우리 CLAUDE.md: ν 0.3 은 E* 에만 들어가는 2차 인자).  µ_s = 0.5 는 우리 값과 대조 시 확인 필요.
- **η_n0**(법선 감쇠)만 슬러리 500 → 건조/압연 50 으로 10× 낮췄고, **AM/SE 의 E·γ·k_t 는 세 단계 내내 불변**이다.  ⇒ Bayesian 재보정이 실제로 움직인 것은 **LJ ε 과 CBD 의 E·γ** 이지 AM/SE 접촉이 아니다.

**(3) Harmonic bond (eq 2.10) — 형상을 강체로 고정하는 장치** (SI T3, 건조·압연에도 동일)

| 이웃 껍질 | κ | r₀ [µm] |
|---|---|---|
| 최근접 | 1×10⁶ | **0.980** |
| 차근접 | 1×10⁶ | **0.848** |
| further | 1×10⁶ | **1.386** |
| further | 1×10⁶ | **1.700** |
| further | 1×10⁶ | **1.960** |

- **우리 읽기**: 1.386 = √2 × 0.98, 1.700 ≈ √3 × 0.98, 1.960 = 2 × 0.98 ⇒ 1차 구가 **pitch 0.98 µm 의 단순입방 복셀 격자**에 놓였음을 뜻한다(= 코어스닝 3×3×3 픽셀 평균의 결과).  ⚠ **0.848 은 이 읽기와 맞지 않는다**(0.848 ≈ (√3/2)·0.98) — "차근접" 이라면서 최근접보다 짧다.  **SI 인쇄 그대로 남기고 해석하지 않는다.**
- **우리 환산**: κ = 1×10⁶ pg µs⁻² = **≈ 1000 N/m**.  저자는 *"artificially high bond strengths allow only for minimal deformation"* 이라 쓰지만, 같은 SI 의 JKR 인력(우리 산출 1.1 mN)과 나란히 놓으면 **강체성이 자동 보장되지는 않는다** — 실제 2차입자 변형량은 **미보고(n/a)**.

#### ①-C 3단계 경계조건·구동

| 단계 | 앙상블/구동 | 정지 조건 | 비고 |
|---|---|---|---|
| **슬러리** | 전 방향 주기 상자에 **무작위 배치** → **NPT**(heat-bath + barostat) 평형 → 이후 "time-stopping condition" 까지 추가 진화 | **시간**(값 미보고 n/a) | **점도 보정은 안 했다** — 본문 자인: *"such simulations also require a calibration of the viscosity [16], however ... this was not considered in this proof-of-concept work."* ⇒ 슬러리 유변학은 **구속되지 않았다** |
| **건조** | CBD 지름을 용매부피만큼 축소(eq 2.11, Ø2.438→0.7) → **NPT 재평형** | 미보고 | **저건조속도 극한 모델**.  모세관력·표면장력·convection-diffusion **없음**(고속건조는 ref [29] scope 밖이라 명시) |
| **압연** | 위 = calendering roll, 아래 = CC.  **둘 다 JKR 로 미세구조와 상호작용**.  roll 을 **등속 하강** → 목표 **압연도(두께 감소율)** 도달 → **같은 속도로 후퇴** → **springback** | **압연도 = 변위 목표**(0.05–0.45, 0.05 간격 9점 + CD 0) | ★ **응력 서보 없음 · 압력 판독 없음**.  본문 전체에 **절대압(MPa) 이 한 번도 안 나온다**(우리 grep: 본문 "MPa" 실질 0회, "plastic/plasticity" **0회**, "yield" 1회는 *"yielding dimensionless values"*).  주기 경계를 걸쳐 CC 위로 나온 AM 은 **그 자리에서 잘라낸다**(*"it is simply cut at that point"*) · roll 속도값 **미보고(n/a)** |

★ **압연 단계는 실험 앵커가 하나도 없다** — 실험 대조 2점은 슬러리(밀도)와 건조(porosity)에만 걸려 있고, 압연 단계 force field(SI T6/T7)는 **보정 대상이 아니었다**.  저자 자신이 결론에서 이것을 요구한다: *"one way to improve the realism ... would be to better parametrize the force field parameters used during the drying and calendering stages according to experimental data, considering macroscopic properties such as **porosity as a function of calendering pressure**, conductivities, and cracking of secondary particles."*

#### ①-D ★★ 압밀에서 소성을 어떻게 다뤘나 — **전혀 안 다뤘고, 정당화도 안 했다**

- **JKR = 탄성 + 점착이고 항복 캡이 없다.**  Thornton–Ning(Varkey 2026)·Storakers·Luding hysteresis 같은 **소성 분기가 없다.**  논문 본문에서 **"plastic/plasticity" 는 0회**, 항복응력·경도·소성 접촉면적 **전무**.
- **정당화 시도 자체가 없다.**  ASSB 압밀이 왜 탄성-점착만으로 되는지에 대한 논증이 본문에 없고, 대신 **결함으로 자인**한다 — 결론: *"**A setback is also the use of force field parameters that do not allow for a high degree of overlap, as this effect is important for the appropriate description of the mechanical properties of the electrode.**"*  그리고 Fig 7 논의: *"once contact has been established between two or more spheres, no matter how much the microstructure is compressed, two phases will not be able to increase their contact area, **since we do not allow for much overlap between the different spheres during the calendering stage in the first place**."*
- ★ **우리 산출 — 그 강성에서 LPSCl 접촉은 사실상 "닿자마자 소성"이다.**  Hertz 평균접촉압 p̄ = (4/3π)·E*·√(δ/R).  E* = 135 GPa, R_eff = 0.2425 µm(Ø0.97 1차구 쌍) 이면:
  - 겹침 δ = 10 nm 에서 이미 **p̄ ≈ 11.6 GPa** — LPSCl 항복응력(우리 MPM champion σ_y = 0.15 GPa, 문헌대 0.05–0.30)의 **40–200배**.
  - 항복 개시(p̄ ≈ 1.1 σ_y ≈ 0.165 GPa)에 대응하는 겹침은 **δ ≈ 2 pm** (원자 간격 이하).
  ⇒ **그들 SE 접촉은 물리적으로 첫 접촉 순간부터 소성 영역인데, 모델에는 그것을 표현할 자유도가 없다.**  같은 산술을 우리 DEM(E_eff = 1.35 GPa)에 하면 항복 개시가 **δ/R_eff ≈ 8.3 %** 이고, 우리 **pure-SE 실측 ⟨δ⟩ ≈ 지름의 11 %**(Cronau 대조, CLAUDE.md) ⇒ **δ/R_eff ≈ 0.44 = 항복 개시의 약 5배** — 우리 접촉은 **확실히 소성 영역 안**에 있다.  ⇒ **18× 연화가 접촉을 "소성 스케일" 에 올려놓는 장치**임이 이 대비로 다시 확인된다(frame[2]).
  ⚠ σ_y = 0.15 GPa 는 **우리 값**이고 논문 값이 아니다.  E* 환산은 ①-B 의 단위 가정에 의존한다.

#### ①-E 실험 대조를 어디에 어떻게 걸었나 — **2점, 둘 다 *보정 타깃* → 독립 검증 0**

| 앵커 | 실험 | 시뮬 | 어떻게 썼나 |
|---|---|---|---|
| 슬러리 밀도 | **1.353 ± 0.001 g/cm³** (Anton Paar DMA 4100 M, 제조 직후) | **1.34 ± 0.02** | **슬러리 단계 force field 를 여기에 Bayesian 보정** (eq 2.12, β = ρ_sim/ρ_exp 단일 목적) |
| 건조 porosity | **0.53 ± 0.03** | **0.57 ± 0.01** | **건조 단계 force field 를 여기에 재보정** |

⇒ **두 실험값 모두 보정에 소비됐다 = 남겨둔(held-out) 검증점이 없다.**  σ_ionic·σ_e·계면면적·graded-z·springback 은 **어떤 실험 대조도 없다**(무차원이라 원리적으로도 불가).  ⚠ 정직: 우리 E_eff = 1.35 GPa 도 porosity 에 보정된 값이라 **그 축에서는 우리도 동급**이다 — 우리 우위는 *앵커 개수*와 *남겨둔 앵커*(Cronau overlap · Bazzoun σ · SEM · Lee/Kim σ_e 밴드)에 있다.
그리고 압연 결과 전체가 **"For this proof-of-concept work, the energy was unable to reach full equilibrium"** 라는 자인 위에 있다 (본문 §3).

#### ①-F GeoDict 로 σ 를 어떤 설정에서 냈나

| 항목 | 이온 (DiffuDict) | 전자 (ConductoDict) |
|---|---|---|
| 지배식 | 정상상태 확산 | Ohm + Poisson 정상상태 |
| 구동 BC | **양쪽 면에 Δc = 1 mM 고정**(z) | **Δφ = 1 V**(z) |
| 측면 BC | **xz·yz 주기** (DEM 과 동일) | 동일 |
| 산출 | D_eff = \|flux\|·두께/Δc; *"In normalized units, diffusivity and ionic conductivity are the same, as they are proportional"* | σ_eff |
| 정규화 | **SE 벌크 = 1.0** | **CBD 벌크 = 1.0** |
| **상별 σ 입력값** | **n/a — 미보고** (AM 이 이온을 전도하는지, SE 가 전자를 전도하는지, pore 처리 전부 미기술) | **n/a** |
| **voxel 크기/해상도** | **n/a — 미보고** (본문에 "voxel" 은 nano-CT 세그멘테이션 맥락 1회뿐; 방법 상세는 ref [16] Alabdali 2023 로 위임) | **n/a** |
| **접촉/계면 저항 항** | **없음**(기술 자체가 없다) — 상별 벌크 σ + 기하만 | **없음** |
| **τ 규약** | ★ **τ 를 산출하지 않는다.**  본문의 "decrease in tortuosity factor of the SE phase" 는 refs [51,52] 를 인용한 *기대*이지 그들의 계산값이 아니다 | — |

⇒ **정규화가 SE(이온)/CBD(전자) 벌크라는 사실만으로 F = σ_eff/σ_bulk 는 순수 기하량**이 되고(선형 문제), 그래서 **F 는 그들이 어떤 절대 σ 를 넣었든 무관하게 우리·Bazzoun 과 비교 가능**하다 (C4 정정의 근거).

---

### ② 이 방법이 실제로 더 유효한가 — **축별 판정** (뭉뚱그리지 않는다)

| # | 축 | (a) 그들 | (b) 우리 | (c) 판정 + 근거 |
|---|---|---|---|---|
| **1** | **AM 형상 표현** | nano-CT → Weka RF → watershed → **multisphere(1차 구 Ø0.97, ~50개/입자, 강체)**.  ASSB 최초 | **완전 구**(AM_P/AM_S) + MPM scaffold(AM 위치 고정) | ★ **그들 우세, 단 3중 감쇄**: ① 형상 공여체가 **다른 소재**(NMC622 ≠ 슬러리 AM, 저자 명시) ② **조대화**(고해상 입자는 "계산비로 안 씀") ③ **강체**(κ=1e6 harmonic).  ⇒ "정적 기하 사실성" 축에서만 우세 |
| **2** | **SE 형상 표현** ★ | **단분산 Ø1.0 µm 완전 구** — nano-CT 가 SE/CBD/carbon 을 구별 못 해 **원리적으로 resolved 불가**(저자 명시) | **구**이되 **bimodal 12:4:1** + **Cronau(r_SE) 물성 인자** + **MPM 에서 SE 만 J2 로 실제 변형** | ★ **우리 우세.**  ASSB 이온수송의 주역인 SE 상에서 그들의 "resolved" 는 **적용되지 않는다**.  게다가 그들 SE 는 **크기 자유도조차 0**(단분산) → Furnas·크기효과 불가 |
| **3** | **압밀 물리** ★★ | JKR(탄성+점착), **E_pair 135 GPa**, **γ 1000 J/m²**, 항복·소성 **0**, 압력 판독 **0**, "겹침 허용 안 함"을 **저자가 결함으로 자인** | hooke/hysteresis + **E_eff 1.35 GPa**(18× 연화, pure-SE Cronau overlap 11–12 % 로 독립 확인) + **Stage-E Tabor/volume 소성면적** + **MPM J2 진짜 형상소성** + **Heckel P_y = 138 MPa, R² 0.965** | ★★ **우리 압도적 우세.**  결정적 근거 = **우리 산출 δ_y ≈ 2 pm** (①-D): 그들 강성에서는 LPSCl 이 항복하기 시작하는 겹침조차 표현 불가.  그들 결론이 요구하는 **"porosity as a function of applied pressure 로 보정"** 이 **정확히 우리가 이미 하는 것** |
| **4** | **transport 이산화** ★ | **GeoDict 연속체 voxel 1종** · 채널 2개(이온·전자) · 접촉저항 항 없음 · **voxel 크기 미보고** · 무차원 | **이중 이산화**: DEM **접촉망**(접촉당 Holm 1/(2σr_c) + Kirchhoff) **＋** MPM **복셀 FV**(STEP3 ∇·σ∇φ=0) · 채널 **3개**(+열) · **절대 mS/cm** · **격자수렴 원장 보유**(CL-25 표현부피 18× 변동 실측 · CL-39 구-스탬프 수렴 0.2 %) | ★ **우리 우세 — 단 이유를 바꾼다.**  "연속체라서 constriction 을 못 본다"는 **반쯤만 맞다**(잘 해상하면 연속체도 목 기하를 푼다).  실제 결정적 결함은 ⓐ **voxel 크기 미보고 → 감사 불가**(우리 자신이 CL-25 로 이 노브가 σ 를 크게 흔든다는 것을 **실측**했다) ⓑ **접촉면적이 압밀에 반응하지 않음**(Fig 7) → 목이 얼어붙은 기하 위의 해 ⓒ **접촉·계면 저항 항 부재** ⓓ **σ_thermal 없음** |
| **5** | **σ 의 실제 값** ★★ | **F_ion = 1.35×10⁻²** (압연 45 %), **F_e = 1.13×10⁻³** | 우리 STEP3 SBE: **F_ion = 0.052 / 0.131 / 0.166**(vox 0.4/0.3/0.25, σ_SE,in = 3.0 기준) | ★ **우리 우세**, 그리고 **C3 정정의 근거**: 같은 소재계 실험(Bazzoun **F = 0.134**, 400 MPa) 대비 그들은 **1/10**, 우리 최조밀 격자 대비 **1/12** 다.  **N_M(=1/F): 그들 74 vs Bazzoun 실험 7.4 = 정확히 10배** |
| **6** | **공정 사슬** | **슬러리(Langevin NPT) → 건조(Ø2.438→0.7) → 압연(등속 하강·등속 후퇴 + springback)** | **cold-press 압밀만**(건식 지향) | ★ **그들 우세(축 보유)** — 단 3가지 감쇄: ① 단계마다 **force field 가 다른 fit 값**(ε 10⁴ 변동)이라 "사슬"의 물리적 연속성이 약함 ② **점도 미보정**(슬러리 유변학 무구속) ③ 같은 그룹이 **무용매 압출 DEM [9]** 도 갖고 있어 "습식 = 그들 정체성" 은 이 논문 한정 |
| **7** | **springback / 제하** ★ | **보유**(roll 후퇴 → 탄성회복; Fig 5 의 45 % 곡선이 ≈24 µm 에서 끝난다) | **미보유**(DEM hold, MPM hold/servo — 탄성회복을 산출로 안 냄) | ★ **그들 우세.**  ★ 우리 산출 회복률(고체부피 보존 + Fig 6 digitized): **압축량의 10–15 %**, 압연도 0.45 에서 relaxed 두께 ≈ **23.8–24.6 µm**(digitized 0.578→0.291 이면 23.8, stated 0.57→0.30 이면 24.6; 초기 40 µm, 눌린 22 µm) — **Fig 5 의 45 % 곡선 종단 ≈24 µm 와 자기일관** ✓.  Sangrós 2019 LIB 점탄성 회복 ~17 % 와 같은 자릿수 |
| **8** | **실험 앵커 개수·직접성** | **2점, 둘 다 보정 타깃**(밀도·건조 porosity) → **held-out 0**.  압연 단계는 앵커 **0**(저자 자인).  σ·계면 실험 대조 **0** | Minnmann porosity(보정) + **Cronau overlap(독립)** + **Bazzoun σ(독립)** + **SEM morphology(독립)** + **Lee2025/Kim2024 σ_e 밴드(독립)** + **DEM↔MPM frame[4] 교차** | ★ **우리 우세** — 단 정직히 **보정-앵커 축(E_eff↔porosity)에서는 동급**.  차이는 남겨둔 앵커의 수 |
| **9** | **계산 비용·확장성** | RVE **22×22×40 µm**(건조) · 입자수 **미보고** · "limited computational resources" 반복 · 고해상 형상 **포기** · 점도 보정 **포기** · **"energy was unable to reach full equilibrium"** | DEM 3만+ 입자 · MPM 최대 **115 M 점**(512³) · STEP3 최대 **86.8 M dof** · 코퍼스 132–291 케이스 · 8팔 factorial 앙상블 | ★ **우리 우세**(규모·앙상블·수렴 판정).  단 multisphere 는 접촉수가 본질적으로 폭증하는 표현이라 비용 축은 **방법 선택의 대가**이기도 하다 |
| **10** | **예측/압축** | **case-by-case**(압연도마다 GeoDict 재계산).  단 그룹은 ML 다목적 최적화 [49] 보유 | 스케일링 법칙 **LOOCV 0.975 / 0.953 / 0.903** + 설계→구조 예측기(nested CV) | ★ **우리 우세**(이 논문 한정으로는 압도적).  ⚠ "그룹이 ML 을 못 한다" 로 읽지 말 것 |

#### ②-보론 ★★ 왜 그들의 σ 가 실험의 1/10 인가 — **SE 가 percolation 문턱 아래에 있다**

- F = σ_eff/σ_bulk = **φ/τ** (선형 정상상태, SE 만 이온 전도).  Fig 5 digitized φ_SE 를 넣으면 **우리 산출 τ_SE**:
  - 압연 5 %: φ_SE ≈ 0.15, F = 4×10⁻⁴ → **τ_SE ≈ 375**
  - 압연 45 %: φ_SE ≈ 0.18, F = 1.35×10⁻² → **τ_SE ≈ 13**
  (참고: Bazzoun 실험 φ_SE = 0.53, F = 0.134 → **τ ≈ 4.0**; Bruggeman τ = φ^-0.5 는 φ=0.18 에서 2.4 → F_B = 0.076 ⇒ 그들은 유효매질보다 **5.6배 나쁘다**, 압연 5 % 에서는 **145배**)
- **φ_SE ≈ 0.15–0.18 은 문헌이 인용하는 이온 percolation 문턱 φ_SE ≳ 25 %**(Bielefeld 2019, Famprikis 2019 리뷰 경유) **아래**다.  ⇒ **그들의 "압연하면 σ_ion 이 34배 오른다" 는 문턱을 향해 기어오르는 곡선**이지, 실제 셀이 운전되는 문턱 위 영역의 "치밀화 → 수송 개선" 곡선이 아니다.
- ★ **우리 쪽 함의**: 이것은 우리 **G4 가드**(Stage 22.5 를 φ_AM < 0.3 에서 외삽 금지 — 멱함수는 문턱 붕괴를 표현 못 함)와 **같은 물리를 다른 상에서** 본 사례다.  문헌 카드로 인용 가치가 있다.
- ⚠ φ_SE 는 **digitized(±0.02–0.03)**, 문턱 25 % 는 **다른 논문 값**, τ 는 **우리 산출**이다.  ⇒ 방향과 자릿수만 인용할 것.

#### ②-보론 2 ★ 논문 자체의 오류 1건 (우리 판단)

Fig 7 의 크기 서열(SE–Pore 11.5 ≫ AM–Pore 5.7)을 저자는 **부피**로 설명한다 — *"since **SE has the highest volume**, it also has the largest value in the beginning."*  그러나 **자기 Fig 5 가 φ_AM(0.27–0.35) > φ_SE(0.15–0.18)** 을 보여준다.  올바른 설명은 **비표면적**이다: S/V = 6/d 이므로 Ø1.0 µm SE 는 Ø4.5 µm AM 2차입자의 4.5배 비표면을 갖고, φ×6/d 로 계산하면 SE:AM ≈ **2.5** — 관측 **2.0** 과 정합(multisphere 표면이 매끈 구보다 커서 비가 더 줄어드는 방향).  ⇒ **부피가 아니라 입경이 서열을 만든다.**  ⚠ 결과 수치는 영향 없음, **설명만 틀렸다**.

---

### ③ 우리와의 차별점 + 우리 이점 — 원고에 쓸 수 있는 형태

#### ③-A 우리가 **원리적으로 못 하는 것** (정직)

1. **비구형 AM 형상** — 우리 DEM AM 은 완전 구다.  LIGGGHTS `multisphere` 로 원리상 가능하지만 production 에 없다.  (⚠ 단 ②-2: 그들의 resolved 는 **AM 한 상뿐**이라 이 결손의 사정거리는 *패킹·기하*이지 *이온 수송*이 아니다.)
2. **nano-CT → segmentation → 입자 추출 자산** — 실측 형상 파이프라인 자체가 없다.
3. **슬러리·용매·건조** — 원천 없음(우리는 건식 지향이라 셀-제조 경로가 다르다).
4. **springback / 제하 탄성회복** — 산출로 내지 않는다.  ★ 이건 **흡수 가치가 실재**한다(③-C ④번 앵커).
5. **상용 GeoDict 급 voxel 재료-연구소 성숙도** — 우리 STEP3 는 자작이다.

#### ③-B 우리가 **원리적으로 더 하는 것** — 그리고 왜 중요한가

| 우리 고유 | 그들 상태 | 왜 중요한가 |
|---|---|---|
| **접촉당 Holm 협착 + Stage-E 소성면적** | 접촉저항 항 없음 + **면적이 압밀에 반응 안 함**(Fig 7) | **"압밀이 계면을 키운다"** 는 ASSB 의 핵심 물리를 그들은 수치로 못 낸다.  저자 자신이 *"we would **expect even higher values** for larger interfacial areas between materials"* 라고 결손을 말한다 |
| **MPM J2 진짜 형상 소성** | 소성 0(단어조차 0회), E 135 GPa | 그들 porosity 하한 29 % vs 우리 15.6 %.  ⚠ 단 압력 축이 없어 **정량 대조 금지**, 그리고 그들 침대엔 **E ≈ 5 kPa 의 초연질 CBD 상**이 10 vol% 있어 강성만으로 floor 를 설명할 수 없다(초판 A-5 의 강성 귀속을 여기서 **완화**한다) |
| **σ_thermal** | 없음 | 열 채널은 이 문헌 계보 전체에 없다 |
| **절대 mS/cm + 문헌 밴드 대조** | 무차원 | 실험 밴드(Lee 34 · Kim 38.6–65.2)에 앉힐 수 있는가의 차이 |
| **fracture-aware transport** | 없음(future work; 그룹의 LIB fracture 모델 [38] 은 이 논문에 안 들어옴) | 저자가 *"large pressures can induce AM particle cracking [53]"* 로 한계만 언급 |
| **이중모델 frame[4] + 격자수렴 원장** | 단일 모델, **voxel 크기 미보고**, "energy not fully equilibrated" | 우리는 같은 함정(격자·수렴)을 **계량해서 원장에 남긴다** — 이게 방법론적 우위의 실체 |
| **솔버 → 스케일링 법칙 LOOCV 압축** | case-by-case | 설계 스윕 비용 |

#### ③-C ★ 그들 수치 중 **우리가 당장 앵커/대조로 쓸 수 있는 것** (조건 명시)

| # | 값 | 조건 | 출처 등급 | 우리 용도 |
|---|---|---|---|---|
| 1 | **슬러리 밀도 1.353 ± 0.001 g/cm³** | 75/17.5/5/2.5 wt%, 고체분율 50 wt%, PIB 9 wt% in p-xylene, Anton Paar DMA 4100 M, 제조 직후 | **stated·실험** | 습식 조성→밀도 sanity check (건식 우리 파이프라인엔 간접) |
| 2 | **건조(미압연) porosity 0.53 ± 0.03** | 저건조속도 tape-cast, 압연 전 | **stated·실험** | ★ **"압연 전 습식 ASSB 양극"의 실험 porosity 앵커** — 우리 300 MPa 15.6 % 와의 격차가 *공정 경로 차*임을 보이는 대조점 |
| 3 | **porosity vs 압연도 10점**: 0.578 / 0.559 / 0.539 / 0.517 / 0.492 / 0.464 / 0.428 / 0.390 / 0.341 / **0.291** (CD 0→0.45, 0.05 간격) | 압력 축 **없음** | **digitized** | 압밀곡선 *형상* 대조만.  ⚠ **Heckel 과 직접 겹치기 금지**(x축이 압력이 아님).  ★ 이 곡선은 **가속형**(고압연에서 더 가파름) = 실제 분체 압밀의 감속형과 **반대** — 소성 부재의 서명 |
| 4 | **springback = 압축량의 10–15 %** (CD 0.1→0.45 에서 15 → 10 %); CD 0.45 에서 relaxed 두께 ≈ **23.8–24.6 µm**(초기 40, 눌림 22) | **우리 산출**: 고체부피 보존 + 압연도 = 적용 두께감소율 가정.  Fig 5 종단 ≈24 µm 와 자기일관 ✓ | **derived** | ★ **우리 MPM 제하(unload) 검증 타깃** — 우리가 없는 산출물.  Sangrós 2019 LIB ~17 % 와 같은 자릿수 |
| 5 | **F_ion 9점**(SE 벌크 기준, ×10⁻²): 0.04 / 0.14 / 0.31 / 0.43 / 0.50 / 0.66 / 0.85 / 0.94 / **1.35** (CD 0.05→0.45) | 무차원 = **형성인자** | **digitized** | ★★ **N_M = 74 (그들) vs 7.4 (Bazzoun 실험 400 MPa) vs 6–19 (우리 3격자)** 3자 대조.  아래 표 참조 |
| 6 | **F_e 9점**(CBD 벌크 기준, ×10⁻³): 0.12 / 0.16 / 0.30 / 0.29 / 0.33 / 0.64 / 0.57 / 0.96 / **1.13** | 무차원 | **digitized** | ⚠ **CBD 벌크 σ 미보고 → 절대 mS/cm 환산 불가**(③-D) |
| 7 | **계면면적 6종**(A/A_base, CD 0.05→0.45): SE–Pore 11.5→8.6 · CBD–Pore 5.9→4.8 · AM–Pore 5.7→4.05 · CBD–SE 1.95→1.82 · **AM–SE 1.08→1.25** · CBD–AM 0.72→0.68 | 복셀 기하 면적 | **digitized** | ★ **우리 유도 AM 표면 SE-피복률 = 1.08/(1.08+0.72+5.7) = 14.4 % → 20.9 %** — 우리 **Hertz coverage 16–18 %** · **MPM 기하 ground-truth 16 %(gap≤0)** 와 **같은 밴드**, 우리 **Tabor 48–52 %** 와는 다른 밴드.  ⇒ "탄성-접촉 피복 vs 소성-확산 피복" 두 밴드의 **외부 대조점**.  ⚠ 그들 porosity 30–57 % vs 우리 15.6 % |
| 8 | **PSD**: AM Gaussian **4.5 ± 0.79 µm**, [3,6] 절단 · **SE 단분산 Ø1.0 µm** | SI | **stated** | ★ **SE 지름이 우리 r_SE = 0.5 µm(Ø1.0)와 정확히 같다** → SE 크기 축은 직접 비교 가능.  AM:SE = **4.5:1 단봉** vs 우리 **12:4:1 이봉** → 그들에게 Furnas dip 이 없는 이유가 조성이 아니라 **PSD 설계** |
| 9 | **RVE**: 슬러리 22×22×110 µm → 건조 22×22×40 µm | Fig 4 라벨 | **digitized** | 우리 real_14(≈30 µm 두께)와 같은 자릿수 |
| 10 | **JKR/LJ/bond 전 표**(①-B) | SI | **stated**(단위 환산은 우리 것) | 접촉모델 층위지도에서 **"항복캡 없음 + 벌크 강성 + 초강 점착"** 좌표를 채우는 외부 사례 |

**형성인자 3자 대조표** (F = σ_eff/σ_bulk, N_M = 1/F):

| 출처 | σ_eff | σ_bulk 기준 | **F** | **N_M** | 조건 |
|---|---|---|---|---|---|
| **Weitze 2024** (이 논문) | — (무차원) | SE 벌크 | **0.0135** | **74** | 압연 45 %, porosity 0.291, φ_SE ≈ 0.18, **압력 미보고** |
| **Bazzoun 2026 실험** | 0.137 mS/cm | 펠릿 1.02 mS/cm | **0.134** | **7.5** | f_CAM 70 wt%, **400 MPa**, full-blocking EIS |
| **우리 STEP3 SBE** | 0.156 / 0.394 / 0.498 mS/cm | 입력 3.0 mS/cm | **0.052 / 0.131 / 0.166** | **19 / 7.6 / 6.0** | vox 0.4 / 0.3 / 0.25 µm, **격자 미수렴**(SR-01) |

⚠ **읽는 법**: ① Weitze 의 F 는 **순수 기하량**이라 그가 어떤 절대 σ 를 썼든 무관하다(선형 문제 + SE 만 이온 전도) — 그래서 이 표는 성립한다.  ② 우리 F 는 **σ_bulk 기준을 3.0(단결정)으로 잡은 값**이라 Bazzoun 의 펠릿(1.02) 기준과 **규약이 다르다**(우리 CLAUDE.md 가 이미 표시한 σ_grain 이중계산 위험 — 펠릿 기준으로 바꾸면 우리 F 는 3배 커진다).  ③ 우리 값은 **격자 미수렴**(3.2배 폭)이다.  ⇒ **"Weitze 가 실험보다 10배 낮다"** 만이 규약에 둔감한 강건한 문장이고, 우리↔Bazzoun 비교는 규약을 붙여야 한다.

#### ③-D ★ 우리 σ_e 밴드(73 / 54.6 mS/cm)에 그들 값이 앉는가 — **이온은 앉힐 수 있고 전자는 못 앉힌다**

- **전자 축**: 그들 σ_e = **1.13×10⁻³ × σ_CBD,bulk** 인데 **σ_CBD,bulk 가 논문·SI 어디에도 없다(n/a)**.  ⇒ **밴드 위치 결정 불가.**
  역산만 가능하다(**우리 산술, 조건부**): 우리 밴드(Lee 2025 **34** · Kim 2024 **38.6–65.2** · 우리 SBE **73**(PTFE 미차단) / **54.6**(PTFE 차단, CL-49))에 앉으려면 **σ_CBD,bulk = 30–65 S/cm** 여야 한다.  이 값 자체는 불합리하지 않다 — 우리 σ_VGCF 규약 100 S/cm, CL-47 이 확정한 **분말 카본 83 S/cm** 와 같은 자릿수다.  만약 σ_CBD = 100 S/cm 를 가정하면 그들 σ_e ≈ **113 mS/cm** = 우리 SBE 73 의 1.5배 자리.
  ⚠ 그러나 이건 **가정 위의 숫자**다 (§F1): 그들 porosity 30 % vs 우리 15.6 %, 그들 CBD 7.5 wt%(C65+PIB) vs 우리 VGCF 3 wt% + PTFE, 그리고 **AM 을 전자전도체로 셌는지조차 미보고**.  ⇒ **원고에 "그들 σ_e 는 우리 밴드 안" 이라고 쓰지 말 것.**  쓸 수 있는 문장은 *"그들의 전자 형성인자 1.13×10⁻³ 은 CBD 벌크 σ 를 우리 탄소 규약(≈10²  S/cm)으로 놓을 때에만 우리 밴드 자릿수가 된다 — 그 상수를 논문이 보고하지 않아 검증 불가"* 뿐이다.
- **이온 축**: 위 3자 대조표대로 **그들 N_M = 74 는 실험(7.5)의 10배, 우리(6–19)의 4–12배** — **밴드 밖(더 저항적)** 에 명확히 앉는다.  ★ 원인은 조성이 아니다: 그들 **SE/solid ≈ 0.18/0.65 = 28 %** 로 **우리 real_14 의 26–27 % 와 거의 같고**, φ_SE(전체 기준)도 0.18 vs 우리 0.23 으로 비슷하다.  ⇒ **거의 같은 SE 함량에서 형성인자만 한 자릿수 낮다** = 차이는 **조성이 아니라 접촉망 연결성(=압밀 물리)** 에 있다.  이것이 우리 압밀 물리 우위의 **가장 깔끔한 정량 근거**다.

#### ③-E 원고용 3문장 (그대로 쓸 수 있는 형태)

1. *"Weitze et al. (2024) put **real, nano-CT-derived AM shapes** into an ASSB manufacturing DEM for the first time, but their supporting information shows the contact model is JKR **elastic + adhesion with a pair modulus of 135 GPa and no yield branch**; the authors themselves list *'force field parameters that do not allow for a high degree of overlap'* as **a setback** and report that calendering does **not** grow the inter-material interfaces.  At that stiffness an LPSCl contact would already be **above its yield stress at ~2 pm of overlap** (our estimate), which is precisely the regime our **18×-softened DEM contact + MPM J2 shape plasticity** are built to represent."*
2. *"Because their conductivities are normalized to the bulk conductivity of the conducting phase, they are **formation factors**, and can therefore be compared directly with experiment: their most-calendered cathode reaches **F_ion = 1.35×10⁻² (MacMullin number 74)**, an order of magnitude below the **F_ion = 0.134 (N_M = 7.5)** measured by Bazzoun et al. on the same LPSCl/NMC chemistry at 400 MPa — at an essentially identical SE-of-solids fraction (~28 % vs ~27 %).  The gap is therefore **not compositional but a connectivity/compaction gap**."*
3. *"Their simulated SE volume fraction (φ_SE ≈ 0.15–0.18, digitized from Fig. 5) sits **below the ~25 % ionic-percolation threshold** quoted in the literature, so their 34× rise of σ_ionic with calendering is a **climb toward percolation**, not the densification-transport response of an operating cathode — the same failure mode our σ_e scaling law is explicitly guarded against below φ_AM = 0.3."*

---

### ④ 이 논문이 **보고하지 않은 것** (n/a 대장 — 인용 시 요구 금지 목록)

절대압(MPa)·응력 판독 · Heckel / P_y · 배위수 Z · roll 속도 · Langevin 온도 · 시뮬 시간·타임스텝 · **입자 개수** · AM 2차입자 개수/1차 구 개수 · 슬러리 점도(보정 **안 함**, 자인) · **GeoDict voxel 크기** · **상별 σ 절대값**(AM 이온? SE 전자? pore?) · **τ 계산값** · σ_thermal · 재료 E/σ_y/ν 의 *재료* 값(쌍-유효 E 만 SI) · 반복 횟수(오차막대는 "standard error", Fig 8 만 *"simulation repetitions"* 라고 명시) · fracture · 전기화학 사이클링.

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
