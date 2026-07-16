<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md -->
# ASSB 양극을 *습식공정*(슬러리→건조→압연)으로 — *실제 형상(resolved, multisphere)* AM 입자를 nano-CT에서 추출해 DEM 제조 시뮬 + GeoDict로 σ_ionic·σ_e 산출 — Weitze / Franco (Energy Storage Materials 2024)

> slug `wet_processing_resolved_am_ssb_cathode_manufacturing` · DOI `10.1016/j.ensm.2024.103747` · type `DEM (LAMMPS, multisphere resolved-AM; wet-process slurry→dry→calender; exp 밀도/porosity 보정) + GeoDict 연속체 σ_ionic/σ_e` · PDF `WetProcessing_ResolvedAM_SSB_CathodeManufacturing_Simulation.pdf` · digested `2026-06-26` · status ✅

---

## 0. 이 논문이 우리에게 *왜 특별한가* (한눈 positioning)

이 논문은 **우리 프로젝트와 가장 직접적으로 겹치는 시뮬 peer 중 하나**다. 다섯 가지가 동시에 성립한다:
1. **소재계가 우리 것** — NMC(니켈리치) + **LPSCl(Li₆PS₅Cl)** ASSB 양극 (단 NMC**622** LiNi₀.₆Mn₀.₂Co₀.₂O₂, 우리는 NMC811 — Ni 함량만 다름).
2. **resolved(실제 형상) AM 입자** — nano-CT에서 *진짜 다결정 NMC 형상*을 추출해 **multisphere(여러 구 + harmonic bond로 강체 고정)** 로 표현. ★ **우리가 *안 가진* 것**(우리 DEM AM은 완전 구 + MPM scaffold로 형상 우회) → §B/§C의 핵심 대비축.
3. **transport를 *수치로* 산출** — GeoDict DiffuDict/ConductoDict 연속체로 **σ_ionic·σ_e**를 계산(σ_thermal 없음). Lyu(정성)·Bielefeld2019(percolation까지)보다 한 발 더, 우리·Bazzoun과 같은 transport-수치 레벨이되 **연속체**(점접촉 constriction 없음 = 상한).
4. **습식공정(wet-processing) 전체 사슬** — 슬러리 평형 → 건조(용매 제거) → 압연을 *한 LAMMPS DEM*에서 연속. **건조·CBD·용매 = 우리 미보유 wet-process 축**. ⚠ 단 우리 ASSB는 건식(dry-process) 지향이라 *셀-제조 경로가 다름*.
5. **Franco/ARTISTIC/LRCS 그룹** — Ngandjong(2021)·Bazzoun(2026)과 *같은 연구실*. 즉 **Ngandjong LIB resolved-shape(ref 37 Xu 2023) → 본 논문 ASSB resolved-shape**의 직계, 그리고 **Bazzoun(같은 그룹의 RNM constriction σ)** 과 자매. 우리 transport novelty의 정확한 위치를 *그룹 내부 진화*로 드러내는 peer.

⇒ **그들이 앞서는 칸 = resolved AM 형상 + 습식공정**(정직히 인정). **우리가 앞서는 칸 = 점접촉 constriction σ 삼중항(Holm/Kirchhoff) + Stage-E 소성면적 + 진짜 소성 morphology(MPM J2) + fracture-aware + dual-model + LOOCV 예측기.** 본 논문은 *형상은 resolved지만 transport는 연속체(constriction 없음)이고 σ_thermal·소성흐름·fracture가 없다* → 우리가 메우는 칸이 분명하다.

---

## 1. 한 줄 요약
**solid-state 양극(NMC622 + LPSCl + carbon C65 + PIB 바인더)의 *습식 제조*(tape-cast 슬러리 → 건조 → 압연)를 *실제 형상 AM 입자*로 DEM 시뮬한 proof-of-concept.** 핵심 novelty(저자 주장): **nano-CT 단층촬영에서 다결정 NMC의 *진짜 형상*을 Weka segmentation + watershed로 추출해 multisphere(겹친 구 + harmonic bond로 강체 유지)로 표현**하고, 그 resolved-shape AM을 **습식 제조 워크플로(LAMMPS: Langevin + LJ + JKR + harmonic bond, 슬러리 NPT 평형 → CBD 입자지름 축소로 건조 → 압연 roll)** 에 넣어, **Bayesian 다목적 최적화로 force field를 실험 밀도·porosity에 보정**한 뒤, **GeoDict(DiffuDict 이온/ConductoDict 전자)로 σ_ionic·σ_e의 압연도(calendering degree) 의존성**을 도출. 결과: ① **porosity 0.57 → 0.30**(0~45% 압연, 비선형 — springback 때문), ② **σ_ionic·σ_e 둘 다 압연도↑ → 단조 증가**(percolation 경로 짧아짐·접촉↑), ③ ★ **반직관적 발견**: 압연해도 *서로 다른 상 사이* 계면면적(AM-SE 등)은 *증가하지 않고 거의 일정* — **구형·강체 입자라 일단 접촉하면 면적이 더 안 늘기 때문**(저자가 *모델 한계로 명시*: spherical/rigid → 소성 변형으로 계면이 못 자람). 즉 **이 논문조차 "resolved 형상이어도 *입자 소성 변형*(계면 성장)은 못 잡는다"고 자인** → 우리 MPM 형상소성이 메우는 바로 그 칸.

**⚠ 핵심 주의 3가지**: (i) **σ는 *연속체*(GeoDict, 점접촉 constriction 없음)** → SE-SE granular 점접촉 좁힘저항(Holm)을 안 풀어 **σ_eff 상한**(우리·Bazzoun RNM이 그 아래로 깎음). (ii) **resolved 형상 ≠ 형상 *소성***: AM은 multisphere로 *형상은 실제*이되 **harmonic bond로 강체 고정 = 영원히 안 변함**(δ 겹침조차 인위적으로 억제) → 압밀 중 *형상 변화·void-fill·계면 성장 없음*(저자 명시 한계). (iii) **nano-CT 소재 ≠ 슬러리 소재**(데이터 가용성 때문에 다른 NMC nano-CT를 형상 추출용으로 차용) → 형상은 *대표적*이지 *그 슬러리의 실측 형상은 아님*.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (AM/SE/binder) | 연구유형 |
|---|---|---|---|---|
| **Dennis Weitze, Franco M. Zanotto, Diana Zapata Dominguez, Alejandro A. Franco**(교신, alejandro.franco@u-picardie.fr) — **Laboratoire de Réactivité et Chimie des Solides (LRCS), Université de Picardie Jules Verne, Amiens** + Réseau sur le Stockage Électrochimique de l'Énergie (RS2E) + ALISTORE-ERI + Institut Universitaire de France | **Energy Storage Materials 73 (2024) 103747** (접수 2024-06-11, 개정 2024-07-22, 게재 2024-08-24, online 2024-08-30, ©Elsevier; **NOT open access**) | 10.1016/j.ensm.2024.103747 | **AM = NMC622** LiNi₀.₆Mn₀.₂Co₀.₂O₂ **75 wt%**(resolved multisphere) + **SE = LPSCl** Li₆PS₅Cl **17.5 wt%**(구) + **carbon C65(Timcal) 5 wt%** + **PIB(polyisobutene) 바인더 2.5 wt%**(C65+binder = CBD 도메인, 구) + **용매 p-xylene**(건조로 제거); 슬러리 고체분율 **50 %**, PIB 9 wt% in p-xylene | **DEM**(LAMMPS [45]; 슬러리→건조→압연 습식 연속) + **resolved-AM multisphere 추출**(nano-CT [41,42] + Weka segmentation [43] + watershed) + **Bayesian 다목적 보정**(eq 2.12) + **GeoDict 연속체 σ**(DiffuDict 이온 + ConductoDict 전자) |

> ★ **그룹·계보 자리매김 (매우 중요)**: 본 논문은 **Franco 그룹(LRCS, ERC-ARTISTIC/SMARTISTIC) 의 ASSB 제조-시뮬 라인**이다. 본문 §1·§2가 직접 계보를 밝힌다:
> - **Alabdali / Ngandjong / Duquesnoy [16,24,25,33,40]** = 그룹의 **LIB 제조 디지털트윈**(슬러리→CGMD→건조→압연→echem). 본 논문 = 그 LIB 워크플로의 **ASSB 확장 + resolved-shape**.
> - **ref [37] Xu, Ngandjong, Franco 2023 (J. Power Sources)** = 같은 그룹의 ***LIB* resolved-shape**(3D 실제 입자 형상) 모델. 본 논문이 명시: *"realistic shapes의 포함은 *이전엔 Li-ion에서만* 됐다(ref [37]) — 본 논문이 *처음으로* ASSB에 적용."* ⇒ **본 논문 novelty = resolved-shape를 ASSB로 가져온 첫 사례.**
> - **ref [16] Alabdali 2022 (J. Power Sources)** = 그룹의 **첫 ASSB 물리모델**(단 *구형 AM*). 본 논문 = 그 위에 *realistic shape* 추가. *"Alabdali가 manufacturing을 microstructure에 처음 link(구형 AM); 본 논문이 realistic shape로 확장."*
> - **ref [38] Xu, Paredes-Goyes 2023 (Batteries & Supercaps)** = 같은 그룹의 **압연 중 입자 *fracture* 예측 모델**(LIB) — 본 논문은 *fracture는 안 넣음*(한계로 언급).
> - **자매(같은 ASSB-σ 솔버 그룹) Bazzoun 2026** = *RNM(Holm constriction)* σ. 본 논문은 *GeoDict 연속체* σ. ⇒ **같은 그룹이 ASSB σ를 *연속체(본 논문)*와 *constriction-RNM(Bazzoun)* 두 방식으로** 푼다 — 우리 transport 비교에서 *둘 다* 매핑 대상.
> ⇒ 본 논문의 셀링포인트 = **"resolved(실제) AM 형상 + 습식공정 전체사슬을 ASSB에 처음"**. 단 저자 스스로 **proof-of-concept / limited computational resources**라고 반복 명시(고해상 입자는 비용으로 *안 씀* — coarsened 사용).

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **슬러리 밀도 ρ** | **exp 1.353 ± 0.001 / sim 1.34 ± 0.02 g/cm³** | 슬러리(보정 타깃) | stated(eq 3.1) | Anton Paar densimeter DMA 4100 M. Bayesian 최적화로 sim→exp 밀도 맞춤 |
| **porosity (건조후, 압연 전)** | **exp 0.53 ± 0.03 / sim 0.57 ± 0.01** | 건조 전극, 압연 0 % | stated(eq 3.2) | sim이 exp 오차범위 내. ★ 이게 압연의 시작점 |
| **★ porosity (압연)** | **0.57 → 0.30** | 압연도 0 → 45 % | stated(본문) + Fig 6 | P_sim=0.30±0.02 @45 %. **비선형**(springback이 압연도 따라 달라서); ~25 % 압연 이후 급강하 |
| **★ σ_ionic (압연)** | **~0.05e-2 → ~1.35e-2** (정규화, SE bulk=1) | 압연도 0 → 45 % | digitized(Fig 8 우) | **단조 증가**, 무차원(SE 벌크 σ_ion=1로 정규화). 압연↑ → SE 접촉↑·τ↓ → σ_ion↑ (★ ASSB는 LIB와 반대로 압연이 이온도 좋게 함, 저자 명시) |
| **★ σ_electronic (압연)** | **~0.15e-3 → ~1.15e-3** (정규화, CBD bulk=1) | 압연도 0 → 45 % | digitized(Fig 8 좌) | **단조 증가**, 무차원(CBD 벌크 σ_e=1로 정규화). 0.3 압연 근처 계단형 상승. 압연↑ → 입자접촉↑·porosity↓ → σ_e↑ |
| **★ 정규화 계면면적 A_interface/A_base (압연)** | SE-Pore **~11.5→8.5**, CBD-Pore **~5.8→4.8**, AM-Pore **~5.7→4.0**, **AM-SE ~1(거의 일정)**, CBD-SE ~1.8, CBD-AM ~0.9 | 압연도 0.05 → 0.45 | digitized(Fig 7) | ★★ **반직관 핵심**: *상-Pore* 계면은 감소(공극 줄어듦), 그런데 ***상-상* 계면(AM-SE 등)은 거의 안 늘거나 감소** — 구형·강체라 접촉 후 면적 못 자람(저자 *모델 한계로 명시*) |
| **두께 (제조 사슬)** | **슬러리 box 폭 22 µm → 건조 110 µm → 압연 40 µm** | 공정 단계 | stated(Fig 4) | RVE 폭 22 µm, 건조 높이 110 µm, 압연 후 40 µm |
| **E_AM (NMC)** | **명시 단일값 없음** (JKR E* eq 2.8로 들어감, Bayesian 보정) | 소재 | — | ★ Table로 E 절대값 안 줌 — force field를 *밀도/porosity에 보정*(eq 2.12)해 결정. cf 우리 E_CAM 140, Lyu 142 |
| **E_SE / E_CBD** | **명시값 없음**(보정으로 결정) | — | — | 마찬가지로 JKR/LJ 파라미터를 Bayesian로 보정 — *재료 E를 직접 입력 안 함*(chemistry-neutral 지향, 본문 명시) |
| **AM PSD** | **target 입경분포로 추출**(명시 D10/D50/D90 없음) | nano-CT secondary particle | — | watershed로 secondary particle 분리, "targeted particle size distribution" 범위로 선택. ⚠ **nano-CT 소재 ≠ 슬러리 소재** |
| **coordination Z / Heckel P_y** | **n/a**(미보고) | — | — | ★ Z·Heckel 안 줌(porosity-vs-압연도만). Lyu/Sangrós와 달리 배위수 진화 없음 |
| **σ_thermal** | **n/a — 안 풂** | — | — | ★ 이온·전자만(우리 삼중항 중 열전도 없음) |
| **σ 절대 단위** | **무차원**(상 벌크 σ=1로 정규화) | — | stated(본문 §2.5) | ⚠ **절대 mS/cm 값 *없음*** → Bazzoun 0.137 / Minnmann 0.17 mS/cm 등과 *절대 비교 불가*, *압연도-추세*만 |

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
  - **RVE**: 슬러리 box 폭 **22 µm**(x·y·z 주기, 초기), 건조 후 높이 **110 µm**, 압연 후 **40 µm**. bottom = current collector(CC), top = 압연 roll.
  - **압연 BC**: **roll을 const 속도로 하강** → 목표 압연도(calendering degree, *두께 감소율*) 도달까지 → **roll 제거(retract) → springback 발생**(실험처럼). roll·CC 둘 다 JKR로 미세구조와 상호작용. ★ **압연도(% 두께감소)로 제어 = 변위/속도 제어**(우리 MPM "hold"·Lyu와 같은 결, servo 압력제어 아님).
  - **압력범위**: ★ **절대 압력(MPa) sweep 없음** — **압연도 0~45 %**(두께 감소율)로 sweep. Heckel·절대응력 미보고.
  - **seeds**: 시뮬 반복(Fig 6·8 error bar = "standard error of simulation repetitions") — 횟수 명시 안 됨(복수 반복).
  - **보정 프로토콜 (Bayesian, eq 2.12)**: **다목적 cost `C = Σα_i(1−β_i)²`** (β_i = 타깃 비, 본 논문은 *밀도* β=ρ_sim/ρ_exp 단일목적으로 단순화). **(1) 슬러리 평형 단계에서 force field를 ρ_sim→ρ_exp에 보정, (2) 건조 단계에서 force field를 *재보정*해 dry porosity→exp porosity.** Bayesian이 posterior로 다음 force-field 제안 → argmin(C) 수렴. ⇒ **실험 밀도·porosity *2점*에 force field 전체를 보정**(우리 Minnmann 단일 porosity 앵커와 같은 결, 단 *force field 자체*를 맞춤).
- **특이사항/튜닝**:
  (1) **resolved AM 형상(multisphere) = 본 논문 셀링포인트** — ASSB 처음(LIB는 ref [37]에서 먼저). 단 *coarsened*·*nano-CT 소재 차용*·*강체*.
  (2) **chemistry-neutral force field 보정** — E를 직접 안 주고 Bayesian로 밀도·porosity에 맞춤(*다른 chemistry로 일반화* 지향).
  (3) **건조 = CBD 입자축소(eq 2.11)** — 저건조속도 모델, 명시 모세관 없음.
  (4) **σ = GeoDict 연속체**(constriction 없음) → 상한.
  (5) **검증 = 밀도(1.353 vs 1.34) + 건조 porosity(0.53 vs 0.57)** 2점 + σ·계면은 *추세* 분석(절대 σ 실측 검증 없음 — 무차원이라).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | **nano-CT 단층 슬라이스**(2D): gray-scale로 3상 분해 — **거의 검정=Pore, 진회색=SE/binder/CB(CBD) 응집, 밝은 원형=AM**. 100 µm scale bar | **실측 nano-CT가 *3상*(AM/Pore/CBD)만 분해 가능**(SE와 CBD가 gray로 구별 안 됨 → SE 형상은 *구로 가정*, AM만 resolved). 우리 micro-CT 비교 시 같은 한계 |
| **2** | ★ **resolved-AM 추출 파이프라인**(3D): (좌)nano-CT 슬라이스 스택 → (중)**Material Segmentation**(Weka Fast-RF: AM=보라/Pore=빨강/CBD=노랑) → (우)**Active Material Extraction**(AM skeleton만 보라 다결정 형상) | ★ **"실측 형상 → segmentation → AM 추출"의 모범 워크플로** — 우리가 resolved AM을 *진짜로* 넣으려면 이 경로(우리는 대신 sphere+MPM scaffold로 우회) |
| **3** | ★ **particle coarsening**(3D): (좌)고해상 multisphere AM 입자(수백 구, 보라 매끈) → (우)**조대화 후**(파란 큰 구 ~십수 개, 거친 형상) | ★ **"resolved이되 coarse" = 계산비 절충** — 고해상 형상은 *안 씀*. 우리 sphere 가정과 그들 coarse-multisphere 사이의 *해상도 스펙트럼* 가시화 |
| **4** | ★ **습식제조 4단계 스냅샷**: (1)Initial(슬러리 random, AM 초록/CBD-with-solvent 파랑/SE 노랑/CBD 검정) → NPT평형 → (2)**Equilibrated Slurry**(폭 22 µm, CBD 파랑이 부피 지배) → 건조(CBD 축소+재평형) → (3)**Dry Electrode**(110 µm, SE 노랑+AM 초록 보임) → 압연(roll) → (4)**Calendered**(40 µm, roll 위) | ★★ **슬러리→건조→압연 *전체 사슬*의 시각화** — 우리는 *압밀부터* 시작(슬러리·건조 미보유). **건조로 110→압연 40 µm** 두께변화. SI에 springback 영상 |
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
| **소재계** | **NMC622 + LPSCl + C65 + PIB**(ASSB) | **NMC811 + LPSCl + VGCF/SuperP + PTFE**(ASSB) | ★ **거의 같은 셀화학**(둘 다 LPSCl ASSB; Ni 함량·바인더만 차이) — *드물게 같은 계열* peer |
| **★ AM 형상** | ★ **resolved multisphere**(nano-CT 실제 형상, 강체) | **완전 구**(DEM) + MPM scaffold로 형상 우회 | ★★ **그들이 앞섬**(실제 형상). 단 *강체*(소성흐름 없음) — 우리 MPM J2가 *형상변화*는 보유 |
| **★ 형상 *소성*** | **없음**(harmonic bond로 강체; JKR=탄성+점착, 캡 없음) | **MPM 진짜 J2 SHAPE 소성**(void-fill·계면성장) | ★★ **우리가 앞섬.** 저자 Fig 7에서 "계면 못 자람 = 한계" 자인 → 우리 MPM이 메움 |
| **★ 전달 σ** | **GeoDict *연속체*(DiffuDict/ConductoDict) σ_ionic·σ_e — *constriction 없음*(상한), σ_thermal 없음, *무차원***| **Kirchhoff + Holm 구속 + Stage-E** σ_ionic/e/thermal **삼중항(절대 mS/cm)** | ★★ **우리가 앞섬**(점접촉 constriction + 열전도 + 절대값). 그들은 연속체 상한·이온/전자만·무차원 |
| **접촉법칙** | **JKR**(Hertz+점착, 항복캡 없음) + LJ(콜로이드) | Luding hooke/hysteresis(캡 없음) + Stage-E 소성면적 | **같은 no-cap 층**, 그들은 *점착(JKR)·콜로이드(LJ)* 추가(슬러리라); 우리는 Stage-E 소성면적 |
| **공정 범위** | **슬러리→건조→압연**(습식 전체사슬) | **압밀(cold-press)부터** | ★ **그들이 앞섬**(건조·슬러리 보유) — 단 ASSB는 건식이라 *경로 다름* |
| **건조/용매** | **Langevin(Brownian+점성) 슬러리 + CBD 입자축소 건조**(eq 2.11) | **없음**(dry-process/cold-press) | ★ **그들이 앞섬**(습식). ⚠ ASSB는 본질 건식 → *우리가 뒤처진 게 아니라 셀화학상 단계 없음* |
| **CBD** | **균질 carbon+binder 구(LJ/JKR), 명시 bond 없음** | Stage-2 부피점유; 명시 bond 없음(backlog A3) | **둘 다 명시 bond 없음** — 그들은 *콜로이드 구*, 우리는 *부피점유*. Sangrós/Lyu가 명시 bond 보유 |
| **E_AM/E_SE** | **명시 안 함**(Bayesian로 밀도·porosity에 보정 — chemistry-neutral) | E_CAM 140 / E_SE real 24·eff 1.35(DEM)/1.53(MPM) | ★ **철학 정반대**: 그들=force field를 *거시 보정*; 우리=재료 E 명시 + 18× 연화 프록시 |
| **압밀 제어** | **압연도(% 두께)** roll const-속도, springback 有 | **cold-press 단축, 변위 hold**(압력 300 MPa) | 둘 다 변위/속도 제어. **그들은 springback 有**(우리 미보유 — MPM unload로 가능) |
| **압력/Heckel** | **절대 MPa 없음**(압연도만), Heckel 없음, Z 없음 | 300 MPa, Heckel P_y=138·R²=0.965, Z 보유 | ★ **우리가 더 정량**(절대압·Heckel·Z) — 그들은 압연도-추세 |
| **porosity** | **0.57→0.30**(압연 0~45 %), exp 0.53 | pure-SE ~10 % / real_14 15.6 % @300 | ⚠ **floor 다름**(그들 30 % vs 우리 10–15.6 %) — *압연도≠압력*, 슬러리-잔류공극, 강체-구 + 연속체 → §A에서 상술. *절대 비교 금지* |
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
- **그들**: σ_ionic = DiffuDict(확산 flux), σ_e = ConductoDict(Ohm) — **GeoDict voxel 연속체 솔버**. **(i) 점접촉 수렴저항(Holm/Greenwood) 없음** → SE-SE granular 점접촉의 좁힘을 *입자별로 안 풂* = **σ_eff *상한***. **(ii) σ_thermal 없음**(이온·전자만). **(iii) 무차원**(상 벌크 σ=1로 정규화) → 절대 mS/cm 없음.
- **우리**: **명시 Kirchhoff 망**(Σ(φi−φj)/R=0) + **Holm 구속저항**(R=1/(2σr_c), 1967) + **Stage-E 소성 접촉면적** → **σ_ionic·σ_e·σ_thermal 삼중항을 *절대값(mS/cm)*** 으로. 게다가 **LOOCV 스케일링 법칙**(0.975/0.953/0.903).
- **대비의 의미 (그룹-진화로 positioning)**: ★ **이건 우리 transport novelty가 *그룹 내부 궤적*으로 가장 선명하게 보이는 칸.** Franco/Janek-계열 ASSB-σ는 **Bielefeld2019(σ 안 풂, percolation만) → Bielefeld2020 & *본 논문 Weitze2024*(연속체 flux-PDE/GeoDict σ, *constriction 없음 = 상한*) → Bazzoun2026(RNM Holm constriction σ + 실험) → 우리(constriction 삼중항 + 열전도 + 절대값 + 예측기)** 로 *스스로* 정교화돼 왔다. **본 논문 = 그 궤적의 "연속체 상한" 단계** — 우리·Bazzoun은 그 constriction을 *되돌려* 넣어 σ를 아래로 깎는다. ⇒ **"공정→구조 + granular constriction σ 삼중항 + 소성 morphology"라는 우리 3대 portion은 이 그룹이 걸어온 길의 *자연스러운 끝*에 놓인다**(positioning 최강 근거). ⚠ 정직: 본 논문 *목적*은 resolved-shape 제조-구조이지 constriction-정밀 σ가 아님 → "그들이 못 했다"가 아니라 "연속체 상한까지가 그들 scope, constriction은 우리/Bazzoun scope".
- **단 그들이 우리보다 *나은* σ 측면**: ★ **resolved AM 형상 위에서 σ를 푼다** — 우리 σ는 *구 패킹* 위. 즉 그들 σ_eff는 *실제 AM 외형에 따른 tortuosity/계면*을 반영(우리 구-가정이 근사하는 부분). ⇒ **이상적 미래 = 우리 constriction-RNM을 *그들 resolved 형상 위에서*** (둘의 결합).

### A-3. ★ 이온위상 — 본 논문은 *우리와 같은 ASSB 위상*(드물게)
- **Lyu/Sangrós/Ngandjong(LIB)** 은 이온=공극(Bruggeman, porosity GOOD)이라 우리와 *정반대* 위상이었다. **본 논문은 ASSB** → **이온 전도체 = SE(LPSCl) 고체망**, σ_ionic = SE-SE 연결(DiffuDict는 *SE 상* 벌크=1로 정규화) → **압연(압밀)↑ → SE 접촉↑ → σ_ionic↑**(Fig 8, 저자 명시: "LIB와 *달리* ASSB는 압연이 이온수송도 향상[16,56]"). ⇒ ★ **우리 "압밀↑→σ_ionic↑(SE접촉↑), porosity BAD"와 *정확히 같은 위상*** — Lyu 같은 LIB peer와의 *위상역전* 대비가 *여기선 불필요*(같은 ASSB). 오히려 **본 논문이 "ASSB는 압연이 이온도 좋게 한다"를 *명시*** → 우리 frame의 ASSB-위상 정당화.
- **단 그들 σ는 연속체 상한·무차원** → "압연↑→σ_ion↑" *추세*는 우리와 일치(교차검증), *절대값*은 비교 불가(무차원).

### A-4. ★ 습식공정(슬러리·건조) — 우리 미보유 wet-process 축 (Lyu와 같은 칸, 단 ASSB)
- **그들**: **Langevin(Brownian + 점성 마찰) 슬러리 NPT 평형 → CBD 입자축소 건조(eq 2.11) → 압연** 전체 사슬. 결과: 두께 슬러리 22 µm → 건조 110 µm → 압연 40 µm, *graded-z 조성*(Fig 5, CC 근처 AM 결핍).
- **우리**: **건조·슬러리 없음.** ASSB **dry-process/cold-press** 지향(우리 소재계 = 건식 co-rolling, `papers/lee2025_corolling_dryprocess_lpscl_ptfe.md`).
- **대비의 의미**: ★ **습식 제조는 frame[5]의 우리 쪽에 *없는* 축** — Lyu와 같은 칸이되 *ASSB 버전*이라 더 직접적. 단 ⚠ **현재 ASSB 고에너지 셀은 *건식*이 주류**(slurry 용매가 SE를 적셔 계면 손상 → 본문 §1조차 "wet에서 SE가 AM을 못 적셔 계면 문제·sluggish kinetics[13,14]"라고 *습식의 단점* 인정!). ⇒ **우리가 뒤처진 게 아니라**, 본 논문은 *습식 ASSB라는 다른(덜 성숙한) 제조경로*를 다룸. **우리 dry-process가 오히려 *현재 주류 ASSB 경로***. 단 **습식 모델링 *방법*(Langevin 슬러리·CBD 축소 건조)** 은 만약 우리가 *습식 ASSB*나 *건조 동역학*을 다루면 청사진(우리 backlog D5와 약하게 연결).
- ★ **본 논문의 습식 단점 자인 = 우리 dry-process 정당화**: §1 — *"replacing the liquid electrolyte with a SE introduces disadvantages... the electrolyte is no longer able to wet the active material efficiently, interfaces are created between different materials, inducing capacity fade and mechanical instabilities[13,14]."* ⇒ **습식 ASSB의 계면 문제를 저자가 명시** → 우리 건식 경로(`Lee2025` co-rolling)가 *그 계면 문제를 회피*하는 이유.

### A-5. 압밀곡선·계면·검증 — *절대 비교 금지* 주의
- **압밀 P-vs-압연도**: 그들 Fig 6 = 0.57→0.30(압연 0~45 %, *비선형* — springback). 우리 Heckel = pure-SE 4압력 R²=0.965·**P_y=138 MPa**. ⚠ **x축이 *압연도(% 두께감소)*지 *압력(MPa)*** 가 아니다 → **그들 곡선을 우리 Heckel(P_y=138)/P-vs-porosity와 *직접 겹치기 불가*.** floor도 다름: **그들 30 %**(@45 % 압연) vs **우리 10–15.6 %**(@300 MPa). 왜 그들이 높나? (i) **압연도≠압력** — 45 % 압연이 우리 300 MPa에 해당하는지 *불명*(절대압 미보고); (ii) **습식 잔류공극**(슬러리 유래 + 저건조속도); (iii) **resolved 형상이나 *강체***(소성흐름 없어 우리 MPM처럼 void-fill로 floor 못 깸 — Fig 7 자인); (iv) **연속체 σ·구 SE**. ⇒ **floor 30 %는 LIB-DEM rigid floor ~20 %보다도 높음** — *강체-구 floor + 습식 잔류공극*. **우리 10–15.6 %는 소성흐름(MPM)·연화(DEM)로 그 아래** → 우리가 floor를 깬다는 논거의 *또 하나 대조점*(단 압력대 불명이라 *정성*으로만).
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
- **그들**: GeoDict DiffuDict(이온)·ConductoDict(전자) = **연속체 voxel** σ — **(i) 점접촉 수렴저항(Holm/Greenwood) 없음 → σ_eff *상한***, **(ii) σ_thermal 없음**, **(iii) 무차원**(상 벌크=1). ★ 그들조차 본문에서 "future work = constriction/contact 저항"을 시사(Bielefeld2019 Greenwood ref와 같은 그룹-계보).
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
- **그들**: σ가 **무차원**(SE 벌크=1) — **σ_grain 절대값·입계·crystallinity 인자 *없음***(정규화로 소거). 실험 σ 절대값과 *비교 불가*.
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
- ⑦ **데이터**: `docs/data/wet_processing_resolved_am.csv` — porosity(0.57→0.30, 압연도)·σ_ionic/σ_e(무차원, 압연도)·계면면적 6종(Fig 7)·슬러리밀도(1.353 vs 1.34)·건조 porosity(0.53 vs 0.57)·두께(22→110→40 µm)·조성(75/17.5/5/2.5 wt%). **⚠ σ 무차원(절대 mS/cm 없음); 압연도≠압력(MPa); resolved이되 강체; nano-CT 소재≠슬러리 소재 → 절대 σ·porosity·압력 ASSB-production 전이 금지, 추세·방법·형상-한계 대조용.**

## 9. 인용 가능 문장 (deck/paper용)
- "Weitze, Zanotto, Zapata Dominguez and Franco (2024, LRCS/ARTISTIC) presented the **first simulation of *wet-processed* solid-state-battery cathode manufacturing (NMC622 + LPSCl + carbon + PIB) with *resolved active-material geometries*** — realistic polycrystalline NMC shapes extracted from nano-CT by Weka segmentation and represented as **multisphere clusters held rigid by artificial harmonic bonds (eq 2.10)** — run through a slurry→drying→calendering DEM in LAMMPS (Langevin + Lennard-Jones + JKR), force-field-calibrated to experimental slurry density (1.353 vs 1.34 g/cm³) and dry porosity (0.53 vs 0.57) by Bayesian optimization, with **ionic and electronic conductivities computed by GeoDict continuum solvers (DiffuDict/ConductoDict)**."
- "Crucially, their AM particles are **resolved in shape but *rigid***: a key result (Fig 7) is the *counter-intuitive* finding that calendering does **not** grow the inter-phase (e.g. AM–SE) interfacial area, which the authors **explicitly attribute to a model limitation** — *'on account of the spherical [and rigid] nature of these particles, two phases will not be able to increase their contact area'*. This is the **strongest external evidence for frame [1]/[2]**: even a model that puts in the *real shape* cannot capture the plastic deformation and interfacial growth that our **MPM (true J2 shape flow) + Stage-E plastic contact area** supply."
- "Their conductivity is solved on a **continuum GeoDict grid (no point-contact constriction) and reported dimensionlessly** (phase bulk σ = 1), i.e. an **upper bound** of the rigid-contact granular network. Our **explicit Kirchhoff/Holm constriction-resistance triad (σ_ionic/σ_e/σ_thermal, absolute mS/cm)** narrows that bound and adds thermal transport — placing our work at the *end* of the Franco/Janek group trajectory (Bielefeld 2019 no-σ → Weitze 2024 / Bielefeld 2020 continuum-σ → Bazzoun 2026 RNM-constriction → ours constriction-triad)."
- "Both we and Weitze (2024) find ASSB **densification raises σ_ionic** (SE-network conductor, porosity detrimental) — the *opposite* of the Li-ion peers (Lyu/Sangrós, pore-conductor) — confirming our all-solid-state transport framing on the *same LPSCl chemistry*."

## 10. 주의/한계 (over-claim 방지)
- **★ resolved 형상 ≠ 형상 *소성***: AM은 multisphere로 *형상은 실제*이되 **harmonic bond로 *강체*(eq 2.10) = 영원히 안 변함.** **CONTACT 소성조차 없음**(JKR = 탄성+점착, 항복캡 없음; δ는 기하 프록시). *진짜 SHAPE flow·void-fill·계면성장 없음*(저자 Fig 7 자인). → "그들이 형상을 넣었으니 소성도 있다"고 *오독 금지*.
- **★ σ = *연속체*(GeoDict, constriction 없음) + *무차원***: SE-SE 점접촉 수렴저항(Holm/Greenwood) 안 풂 → **σ_eff *상한*.** 상 벌크 σ=1로 정규화 → **절대 mS/cm 없음** → Bazzoun 0.137·Minnmann 0.17·우리 0.04–0.18 등과 **절대 비교 *불가***, *압연도-추세*만. σ_thermal 없음.
- **★ 압연도(% 두께) ≠ 압력(MPa)**: Fig 6/8의 x축은 *압연도(두께 감소율)*지 *절대압*. **Heckel·P_y·절대응력 미보고** → 우리 Heckel(P_y=138)·P-vs-porosity와 *직접 겹치기 불가*. porosity floor 0.30(@45 % 압연)도 *압력 불명*이라 우리 10–15.6 %(@300 MPa)와 *절대 비교 금지*(압연도≠압력 + 강체-구 + 습식 잔류공극 + 연속체).
- **★ nano-CT 소재 ≠ 슬러리 소재**: 형상 추출용 nano-CT는 *데이터 가용성* 때문에 *다른 NMC*(슬러리의 NMC622가 아닌). → 형상은 *대표적*이지 *그 슬러리의 실측 형상은 아님*(저자 명시). SE 형상은 *구로 가정*(nano-CT gray로 SE/CBD 구별 불가, AM만 resolved).
- **★ 입자 coarsening**: 고해상 multisphere는 *계산비로 안 씀* → pixel-averaging 조대화(Fig 3). 형상은 "coarse한 resolved"(완전 구보다 실제적이되 고해상 형상 아님). **proof-of-concept / limited computational resources** 저자 반복 명시.
- **건조 = CBD 입자축소(eq 2.11), 저건조속도 모델**: 명시 모세관력·표면장력·convection-diffusion 없음(ref [29,30,31,32]가 그걸 함 — 본 논문 scope 밖). 고속건조 비균질·crack 미반영. AM·SE는 건조 중 안 변함, CBD만 축소.
- **CBD = 균질 carbon+binder 구**: 명시 입자-입자 bond 없음(Sangrós eq10–13/Lyu parallel-bond 아님). binder가 *접착 bond*가 아니라 *콜로이드 입자상*(LJ/JKR). PTFE fibril/SuperP 응집 *morphology 효과 없음*.
- **E_AM/E_SE/σ_y/ν 절대값 미보고**: Bayesian로 force field를 밀도·porosity에 *보정*(chemistry-neutral) → 재료 E가 *입력*이 아님. → 우리 E_eff·Sangrós 나노압입과 *방법 철학 정반대*(블랙박스 fit vs 물리적 연화/실측).
- **Z·Heckel·coverage(우리식)·fabric tensor·내부응력 없음**: Lyu/Sangrós보다 역학 후처리 *적음*(porosity·계면·σ-추세 중심). **검증 = 밀도·건조 porosity 2점**(절대 σ 실측 검증 없음 — 무차원).
- **NMC*622* + LPSCl**: CAM Ni 함량이 우리 NMC811과 다름(622 vs 811). 셀화학은 *거의 같으나*(LPSCl ASSB) AM·바인더·도전제 종류 차이 → 절대 porosity·σ 전이 시 주의.
- **Fig 6/7/8 값 일부 digitized**(그래프에서 읽음) → **추세만(±)**. **stated**: 슬러리밀도 1.353/1.34, 건조 porosity 0.53/0.57, porosity 압연 0.57→0.30, 두께 22/110/40 µm, 조성 75/17.5/5/2.5 wt%, 고체분율 50 %, PIB 9 wt%. **σ_ionic/σ_e/계면면적 절대값은 digitized + 무차원**(Fig 7/8).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
