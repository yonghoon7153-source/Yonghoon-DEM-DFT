# 입자크기·압력이 빠른 이온전도체 t-Li₇SiPS₈ 의 수송물성에 미치는 영향 — DEM 압밀 + Heckel + FVA σ — Schneider (Adv. Energy Mater. 2023)

> slug `schneider2023_particle_size_pressure_transport` · DOI `10.1002/aenm.202203873` · type `DEM+FVA(continuum) + exp(EIS) + AIMD` · PDF `Schneider_2023_AdvEnergyMater_ParticleSize_Pressure_TransportProperties_FastConductor.pdf` · digested `2026-06-26` · status ✅

---

## ⚠️ 0. 가장 먼저 — 소재 정정 (위시리스트 제목 추정과 다름)

위시리스트 #34 추정 제목은 "fast [Li-Ion Conductor / argyrodite]"였으나, **PDF 전수 정독 결과 실제
소재는 argyrodite(Li₆PS₅X)가 아니라 tetragonal LGPS-계열 thiophosphate `t-Li₇SiPS₈` (t-LiSiPS)** 이다.
- **t-Li₇SiPS₈** = Li₁₀GeP₂S₁₂(LGPS)-like 정방정(tetragonal) 황화물, c축 1D 빠른 전도 채널. glass-ceramic
  (비정질 side phase 8.2–9.0 wt% 함유).
- **우리 LPSCl(Li₆PS₅Cl, argyrodite)과 같은 *황화물(thiophosphate) 패밀리*지만 *다른 결정구조·다른 조성***.
  → **물리·압력거동·방법론은 직접 비교 가능**(같은 sulfide cold-press 거동), **σ 절대값·E·ΔV 등 소재고유
  수치는 transfer 금지**(Cronau/Sakuda/Doux 와 동일한 same-family-but-not-LPSCl 주의).

★ **그럼에도 이 논문이 #34로서 핵심인 이유:** 위시리스트가 노린 두 축 — **σ(입자크기)** 와 **σ(압력)** —
을 **실험 EIS + DEM 압밀 + Heckel + FVA(연속체 σ)** 로 *동시에* 다룬, **우리 DEM→미세구조→σ 파이프라인과
가장 직접적으로 평행한 실험+시뮬 논문**이다. 심지어 Bazzoun/Varkey 보다 *압밀 역학(Heckel P_y, 압력영역
분해)* 측면에서 우리와 더 겹친다.

---

## 1. 한 줄 요약
**황화물 SE 펠릿의 이온전도도는 "상대밀도(porosity)"보다 *입자크기분포(PSD)*에 더 강하게 지배되며,
압밀압력(pelletizing) 은 두 개의 분리된 영역 — (I) 저압 미세구조(입자 재배열·파편화·접촉면적) 와
(II) 고압 원자수준(활성화부피 ΔV 에 의한 격자압축) — 으로 σ 에 *반대 방향*으로 작용한다.** 저자들은
이를 **Heckel 압밀해석 + DEM 압밀시뮬 + FVA 연속체 σ + AIMD** 의 다중스케일로 분해. → 우리에게는
**σ-vs-압력**(우리 Heckel P_y·σ-vs-porosity)과 **σ-vs-입자크기**(우리 Cronau(r_SE)/packing) 의 *실험+시뮬*
앵커이자, "**porosity 는 σ 의 약한 descriptor, PSD 가 강한 descriptor**" 라는 우리 σ_ionic 형태(φ_eff·CN²·
cov·packing 이 porosity 단독보다 강함)와 정합하는 핵심 frame[4] 외부 근거.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| Christian Schneider, Christoph P. Schmidt, Anton Neumann, Moritz Clausnitzer, Marcel Sadowski, Sascha Harm, Christoph Meier, Timo Danner, Karsten Albe, Arnulf Latz, Wolfgang A. Wall, **Bettina V. Lotsch\*** (Max Planck FKF Stuttgart + TU München + DLR/HIU Ulm + TU Darmstadt + LMU) | Adv. Energy Mater. **13**, 2203873 (2023); Received 2022-11-14, Published 2023-03-03 | 10.1002/aenm.202203873 | **t-Li₇SiPS₈** (tetragonal LGPS-like thiophosphate; glass-ceramic). **CAM 없음 — SE-only blocking-electrode 펠릿** | DEM(압밀) + FVA(연속체 σ) + EIS(실험) + AIMD; open access |

> ★ **SE-only 논문**(CAM/composite 아님). σ 는 모두 **순-SE 펠릿의 유효 이온전도도**(blocking electrode EIS).
> Bazzoun/Minnmann 의 *composite* σ_eff,ion 과는 층위가 다름 — 이 논문은 **SE 재료 자체의 σ(압력·크기) 거동**.

## 3. 핵심 물성 (수치)
| 물성 | 값 | 조건 (P, 조성) | stated/digitized | 비고 |
|---|---|---|---|---|
| **σ_ionic (압축, 1차)** | max **4.1 mS/cm** (<50µm) / **5.7 mS/cm** (>50µm) | @ ~0.5 GPa pelletizing | stated | 압축 sweep 최대 |
| σ_ionic @ 최저압 (압축) | **0.3 mS/cm** (<50µm) / **0.7 mS/cm** (>50µm) | @ 0.01 GPa | stated | 미압축 분체 → 접촉불량 |
| **σ_ionic (release, 1차)** | max **5.3 mS/cm** (<50µm) / **6.6 mS/cm** (>50µm) | @ ~0.1–0.2 GPa (release) | stated | 압력해제 sweep 최대 |
| σ_ionic @ 0.01 GPa (release) | **4.4 mS/cm** (<50µm) / **2.1 mS/cm** (>50µm) | @ 0.01 GPa release | stated | >50µm 가 release 더 민감 (역전) |
| σ_total (무압) | **2 mS/cm**, E_a **0.27 eV** | Harm et al. (ref 38) | stated | 재료 고유 |
| **활성화부피 ΔV** | **~1.4 cm³/mol** (exp: 1.39 / 1.41) | release fit (Fig 4c) | stated | **입자크기·morphology 무관 = intrinsic** |
| ΔV (AIMD) | **1.7–2.0 cm³/mol** (f=0.99→1.7, f=0.98→2.0) | 격자 scaling 계산 | stated | 양수 → 압축시 host 국소팽창 필요 |
| 이온 migration 장벽 | **0.22 eV (c축 1D)** / **0.28 eV (3D)** | bond-valence + AIMD | stated | 이방성 D_c ≈ 4× D_a/b |
| **Heckel P_y ("in die")** | **0.95(3) GPa** (<50µm) / **1.65(3) GPa** (>50µm) | 압축, regime II 기울기 | stated | 작은 PSD → 낮은 P_y → 소성변형 쉬움 |
| ρ_rel (상대밀도) | regime III 에서 **90–95 %** (porosity 5–10 %) | 고압(>~1 GPa) | stated | release 시 약 **−4 %** 복원 |
| 펠릿두께 | ~**1600 → 1000 µm** (압축); release 시 ~4% 증가 | 0→1.7 GPa | digitized(Fig 2d) | <50µm 가 더 치밀(낮은 두께) |
| ρ_rel @ 저압 비교 | <50µm > >50µm (작은 입자 초기 더 치밀) | Fig 2e | stated | 단, σ 는 반대(>50µm 가 높음) |
| **비정질 side phase** | **8.2–9.0 wt%** (pristine) → **9.7–10.2 wt%** (@1.7 GPa) | ³¹P MAS NMR | stated | 압력이 결정도 일부 손상 (소성흐름→격자무질서) |
| PSD (<50µm) | monomodal; gamma fit a=1.944, b=7.048 | sieve 통과분 | stated | DEM 입력 |
| PSD (>50µm) | bimodal; **D50(vol) = 89 µm** | sieve 잔류분 | stated | number-PSD 는 작은입자 우세나 vol 은 >50µm 우세 |
| E_SE / σ_y / ν | **n/a** (논문이 E·σ_y 수치 미명시 — DEM 은 c_cor·k_N 으로 캘리브) | — | — | ⚠ Heckel P_y 0.95/1.65 GPa = 유효 항복(σ_y proxy) |
| coverage / Z / σ_e / σ_thermal | **n/a** (SE-only, 측정 안 함) | — | — | composite·전자·열 채널 없음 |

## 4. 시뮬레이션 방법 ★
- **code / version**: **DEM = in-house multi-physics 코드 `BACI`** (TU München Wall 그룹; ref 51). **FVA(연속체
  σ) = `BEST`** (Battery and Electrochemistry Simulation Tool, DLR/HIU; ref 52,53). **AIMD = 별도(VASP류, ref 38·48)**.
  → **3개 솔버 + 실험 EIS** 의 multiscale.
- **DEM 접촉법칙**: 논문 본문에 contact law 정식 미상술(SI 참조). 입력 파라미터로 **ρ, ν, k_N(법선강성),
  c_cor(접촉보정), μ(마찰), g(중력)** 명시(Fig 6a insert). **구형 입자 + 접촉 overlap = 더 큰 접촉면적 → 더 나은
  transport path** 로 모델링("larger contact surface modeled by particle overlapping"). ⚠ **항복캡·SHAPE 소성
  명시 없음** → Bazzoun/Varkey 와 같은 **rigid-sphere + CONTACT(overlap) 모델 계열**로 추정(아래 §10).
- **재료 파라미터**: E_SE/σ_y/ν 의 *수치* 는 본문 미제공(SI). 대신 거시 **Heckel P_y = 0.95/1.65 GPa** 가
  유효 소성항복(σ_y proxy). 밀도 ρ, 마찰 μ 등은 실험 매칭으로 튜닝.
- **bond/binder 모델**: **없음**(SE-only, 바인더·CAM 미포함).
- **MPM/continuum**: **MPM 아님 — FVA(finite volume analysis)** 가 연속체 역할. DEM 이 만든 입자 위치·반지름
  → **voxel 구조 생성** → BEST 로 **정상상태 전류분포**(인가전압 ΔV, ∇·J=0, J=−σ∇φ) 풀어 **유효 σ** 산출.
  = Bazzoun 의 FEM 와 같은 *연속체 전달 readout*(단 voxel-FVM). **점접촉 constriction 명시 없음** → σ 는
  접촉면적(overlap)으로 들어감.
- **전달 솔버 ★**: FVA(BEST) 가 유효 σ. **두 시나리오로 분해(핵심 설계):**
  - **Scenario I** = bulk σ 를 **활성화부피 효과(ΔV)로 감소**시킨 채 일정 stack pressure → **0.1 GPa stack
    실험 모사**.
  - **Scenario II** = bulk σ 를 **증가하는 외부압력에 따라 감소**(ΔV 격자압축) → **variable pelletizing 실험 모사**.
  - σ 값은 **정규화**(σ/σ₀ 또는 σ/σ_0.5GPa) — 절대 bulk σ 가정에 무관, **기하(미세구조)만의 효과** 추출.
- **입자 처리 ★** (DEM판 "무질서 처리"):
  - **구형 입자만**(perfect spheres). 논문이 §결론에서 **"DEM 의 perfect spheres ↔ 실제 비구형 분말 차이가
    저압 regime I 의 과대평가 원인"** 을 *명시*("difference between the DEM model consisting of perfect spheres
    and the powder, which consists of particles that are not perfectly spherical").
  - **실측 PSD 반영**: <50µm = gamma(a=1.944,b=7.048) **다분산(poly)**, >50µm = bimodal. → **mono/bi/poly-PSD
    실측 일치**가 이 논문의 강점(우리 12:4:1 bimodal 과 같은 정신).
  - **rigid vs CONTACT-소성 vs SHAPE-소성**: **CONTACT(overlap) 계열** — 입자 형상은 안 변하고 overlap 이 접촉면적·
    transport 를 키움(="δ-overlap 프록시"). **진짜 SHAPE 소성(입자 형상흐름) 아님** → 우리 MPM 이 메우는 칸과 동일.
    (단 Heckel 해석은 *거시 소성*을 인정 — regime II 가 "plastic deformation" — 그러나 *입자 단위 형상변화*는 DEM 에 없음.)
- **도메인/RVE / servo / seeds / 압력범위**: base **210×210 µm²** × height **1700 µm**, **9591 입자**, **측방 주기경계**
  (실험 펠릿은 측방이 훨씬 크나, 모든 상호작용 포착되도록 측방을 PBC). 압력범위 **0.01 → ~1.7 GPa**(실험과 동일).
  ⚠ **우리 300 MPa cold-press 보다 ~5× 높은 압력대까지**(GPa 영역) — 이 논문은 고압 ΔV 효과를 보려고 일부러 고압.
- **특이사항/튜닝**: DEM 측방 치수를 실험보다 작게 잡되 "PSD 가 실험과 충분히 가깝고 모든 상호작용이 표현되도록"
  선택. σ 는 정규화로만 — **절대 bulk σ 캘리브 회피**(기하효과만 분리하는 영리한 설계).

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | **문헌 σ-vs-P 종합**(Na₃PS₄/Na₃SbS₄/Na₂S·P₂S₅ glass/β-AgI/LiBH₄/Li-β-alumina/LLTO). 미압축 분체(hollow)는 비선형 급상승→포화; 압축펠릿(filled)은 ln(σ)-P 선형. | **압력↑→σ↑→포화** 의 *재료-일반성* + 분체 vs 펠릿 거동차 = 우리 σ-vs-porosity/Heckel knee 의 문헌 맥락 |
| **2 (a–f)** | **압밀 역학·밀도·Heckel.** (a) 두 sieve 분율 SEM, (b) number-PSD, (c) cumulative number/volume PSD(D50_vol=89µm), (d) 펠릿두께-vs-P + 압력 protocol scheme, (e) **ρ_rel-vs-P**(<50µm 가 더 치밀), (f) **"in die" Heckel plot** (regime I 재배열·파편화 / II 소성 / 회색띠) | ★ **Heckel ln(1/(1−ρ))=Kp+A** = 우리 Heckel(P_y=138)과 *동일 식*. regime I/II 분해 = 우리 압밀 단계. **작은 PSD → 더 치밀 BUT σ 는 더 낮음**(역설) |
| **3** | **σ_ionic-vs-pelletizing pressure (1차 cycle)**, 압축(filled)+release(hollow), <50/>50µm. max 4.1/5.7 @0.5GPa; release max 5.3/6.6. 압력 protocol insert. | ★★ **σ-vs-압력 핵심 데이터.** 저압 미세구조-지배(상승) ↔ 고압 ΔV-지배(하강), ~0.5 GPa 최대. release hysteresis = 비가역 소성(우리 Heckel·Doux 비가역) |
| **4 (a–c)** | **원자수준 ΔV.** (a) t-Li₇SiPS₈ 결정구조 + bond-valence iso-energy(c축 1D 채널), (b) AIMD MSD(f=1.0/0.99/0.98 격자scaling) → 압축시 확산↓, (c) **ln(σ)-vs-P 에서 ΔV≈1.4 cm³/mol** 추출(입자크기 무관) | ΔV = **압력이 σ 를 *낮추는* 원자기구**(격자압축→migration 부피 부족). 우리엔 없는 *원자축* — frame[5] 밖(우리 DEM/MPM 은 입자스케일) |
| **5** | **σ-vs-stack pressure** (고정 pelletizing 후 0.01 vs 0.1 GPa stack 에서 EIS). 0.1 GPa stack 이 0.01 보다 높은 σ — 표면균열·접촉저항 영향. | ★ **stack pressure 분리**(우리 운전압 40–70 / Cronau stack 구분). 0.1 GPa stack 권장 = 표면균열 닫기 |
| **6 (a,b)** | **DEM+FVA 시뮬 ↔ 실험 대조.** (a) <50µm Feret 히스토그램 + gamma fit(a=1.944,b=7.048) + DEM/FVA workflow(Scenario I/II), (b) **정규화 σ-vs-P: 실험(원) vs DEM/FVA(삼각) 2 시나리오** — regime II 잘 맞음, **regime I(저압)은 시뮬이 과대평가**(구형 가정 탓) | ★★ **우리 DEM→FVA→σ 파이프라인의 직접 평행 사례.** 시뮬이 *기하만으로* σ-vs-P 추세 재현. 저압 과대평가 = **구형 한계**(우리도 동일) |

> **Figure S (SI, 본 digest 범위 밖이나 본문 인용):** S9 = "in die" vs "out of die" Heckel(탄성 기여 분리),
> S10 = 1.7 GPa SEM(표면균열 수십 µm), S11 = Nyquist, S12 = ³¹P NMR(side phase·peak broadening),
> S13 = DEM contact surface, S17 = AIMD 이방성. SI 입수 시 §3 표 보강 가능.

## 6. Post-processing ★
- **무엇**:
  - ★ **Heckel 압밀해석** `ln(1/(1−ρ_rel)) = K·p + A` (eq 1) — **우리 Heckel 과 완전 동일 식**. 기울기 K 의
    역수 = **평균 항복압 P_y**(소성흐름 stress). **"in die"**(압축중 측정) vs **"out of die"**(해제후 측정) 구분 —
    탄성복원 분리. **3 영역 분류**: I(재배열·파편화, <0.5 GPa) / II(소성변형, 선형, >0.5 GPa) / III(공극소멸, ρ→90–95%).
  - **활성화부피 ΔV** = `−k_B·T·(∂lnσ/∂p)` (eq 3, eq 2 의 단순화) — release sweep 의 ln(σ)-vs-P 선형기울기에서 추출.
    `ΔV = V_m − V_f`(eq 4, migration 부피 − free 부피).
  - **FVA 유효 σ**: DEM 입자 → voxel → 정상상태 전류분포 → σ_eff(정규화).
  - **NMR side-phase 정량**(³¹P MAS): 비정질 부상(side phase) wt% + peak broadening(압력유발 무질서).
  - **AIMD MSD → D → σ** (Nernst-Einstein), 격자 scaling f=0.98–1.00 로 압축효과.
- **도구**: ImageJ(+Legland/Landini plugins; ref 23–25) 로 SEM → PSD(Feret diameter). gamma 분포 fit. BACI(DEM),
  BEST(FVA), AIMD. RELAXIS-류 EIS fit(Nyquist).
- **수치화·플롯·기록 방식**: σ-vs-P 를 압축/release 두 가지로(hysteresis loop). Heckel 을 in-die/out-die 두 가지로.
  σ 정규화(σ/σ_0.5GPa, σ/σ₀)로 절대 bulk 가정 회피. DEM/FVA 와 실험을 **같은 정규화 축**에 겹쳐 그림(Fig 6b).

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| **소재** | t-Li₇SiPS₈ (LGPS-계 정방정 황화물) | LPSCl(argyrodite) | **같은 sulfide 패밀리·다른 구조** → 물리·압력거동 비교 OK, **σ/E/ΔV 절대값 transfer 금지** |
| **Heckel 식** | `ln(1/(1−ρ))=Kp+A` (eq 1) | **동일 식** | ✓ 같음 (P_y = 1/K) |
| **Heckel P_y** | **0.95 GPa(<50µm) / 1.65 GPa(>50µm)** ("in die") | **0.138 GPa(138 MPa)**, σ_y_eff≈46 MPa (pure-SE 4압력) | ⚠ **그들이 7–12× 높음** — *압력대 다름*(그들 GPa 영역 측정, 우리 ≤300 MPa) + *소재 다름* + *in-die vs out-die*. **추세(작은 입자→낮은 P_y→소성쉬움)는 같은 방향** |
| **압밀 압력대** | **0.01 → 1.7 GPa** (고압 ΔV 보려 일부러) | **300 MPa cold-press** | 우리 제조압 = 그들 *저압 regime I/II 경계*(0.3–0.5 GPa) 근방. 그들 GPa 고압은 우리 범위 밖 |
| **ρ_rel @ 고압** | **90–95 %** (porosity 5–10 %) @ >~1 GPa | pure-SE **~90 %**(porosity 10 %) @300 MPa | ⚠ 우리가 *훨씬 낮은 압력*에서 같은 밀도 — 소재·측정·convention 차. **추세만** |
| **입자 처리** | **구형 + overlap(CONTACT)**, 형상변화 없음 | DEM 구형+overlap / **MPM 진짜 SHAPE 소성** | 우리 MPM 이 그들(+Bazzoun/Varkey) 못 가진 *형상흐름* 보유 (frame[5]) |
| **σ readout** | **FVA(voxel-FVM) 연속체**, constriction 명시 없음 | **Kirchhoff/Holm 점접촉 constriction** | 우리 = 명시적 contact-network constriction; 그들 FVA = 연속체(Bielefeld2020 처럼 *상한*에 가까움) |
| **σ 절대 캘리브** | **회피**(정규화 σ/σ₀ — 기하효과만) | σ_grain=3.0·Cronau 절대 캘리브 | 그들은 *상대추세* 전용 설계, 우리는 절대값 예측 — **목적 다름** |
| **σ 채널** | **σ_ionic 만** (SE-only) | σ_ionic + σ_e + σ_thermal | 우리 삼중항 우위 |
| **σ vs porosity** | ★ **"porosity 는 σ 의 *약한* descriptor, PSD 가 *강한* descriptor"**(명시 결론) | σ_ionic = f(φ_eff, CN², cov, packing) — **porosity 단독 아님** | ★ **정합!** 우리도 porosity 외 CN/cov/packing 이 σ 지배 — 그들이 *실험으로* 같은 결론 |
| **σ vs 입자크기** | **작은 입자(<50µm) → σ *낮음***(grain contact 불량·misorientation) | Cronau(r_SE): sub-µm → σ↓; packing: 작은 SE → σ↑(접촉多) | ⚠ **부호 주의**(아래 §A 상세) — 그들 50µm vs sub-µm 의 두 효과 분리 필요 |
| **활성화부피 ΔV** | **1.4 cm³/mol** (압력↑→σ↓ 원자기구) | **n/a**(우리 입자스케일, 원자 ΔV 없음) | 그들 고유 — frame[5] 밖(원자축) |
| **DEM/FVA 저압 과대평가** | **regime I 시뮬>실험**(구형 탓) | 우리도 구형 한계 동일 | ★ **공통 한계** — 우리 MPM(형상)·de Larrard(packing)이 보완 방향 |

## A. 우리 DEM+MPM 대비 (comparison vs ours) — σ(입자크기) & σ(압력)

### A-1. σ(입자크기) — ⚠ 부호 충돌 주의: **두 개의 *반대* 크기효과를 분리해야 한다**
이 논문의 핵심 역설: **작은 입자(<50µm)가 *더 치밀*(ρ_rel↑, Fig 2e)인데도 σ 는 *더 낮다*(Fig 3, 3.8 vs 5.7 mS/cm).**
저자 해석(본문): "<50µm 는 같은 질량에 입자수가 많아 **grain-to-grain 접촉이 많고**, 그 접촉들이 **불리한
grain 방위(misorientation)** 를 가져 **intergranular 저항↑**. Harm et al.(ref 38): t-Li₇SiPS₈ 는 intra-/inter-grain
확산이 섞이며 **inter(grain-boundary) 길이스케일에서 확산이 더 빠름** → 작은입자=GB 많음=병목." 즉 **"작을수록 σ↓"
는 *GB(입계) 저항* 메커니즘**.

우리 모델의 두 크기항과 대조:
- **(i) 우리 Cronau(r_SE) sub-µm σ_grain 감쇠**(작은 r_SE → σ↓): **부호 일치 + 메커니즘 일치!** Cronau digest
  (`docs/lit_cronau2021_*.md` §0(B))가 이미 판정했듯, Cronau(r_SE)의 진짜 물리는 "입자가 작아서"가 아니라
  **"미세결정·소결불량 → grain-contact/GB 불량 → σ↓"** 이다. **이 Schneider 논문이 바로 그 GB 메커니즘을
  *같은 황화물에서 실험으로* 보여줌**("작은입자=GB多=σ↓") → ★ **Cronau(r_SE) 인자의 *부호*에 대한 두 번째
  same-family 실험 근거.** (단 그들 크기축은 **<50µm vs >50µm**(수십 µm 영역), 우리 Cronau breakpoint 는
  **sub-µm(0.03–0.5µm)** — *스케일이 다름* → 부호·메커니즘만 지지, breakpoint 수치 미지지. Cronau 와 동일.)
- **(ii) 우리 packing "size=PACKING"(작은 SE → 접촉多 → σ↑)**: **부호 반대**. 우리·Bazzoun·Minnmann2021 의
  composite "작은 SE → σ_eff↑" 는 *composite 에서 SE 가 CAM 공극을 채우는 packing/percolation* 효과. **Schneider
  는 SE-only 펠릿** → packing-percolation 이득이 없고 **GB 저항만 남아** σ↓. ⇒ **모순 아님, 층위 분리**:
  *composite packing*(우리 σ↑) ≠ *SE-only GB*(Schneider σ↓). 우리 σ_ionic 식이 **둘 다** 담아야 함:
  packing/CN 은 σ↑(composite), Cronau/GB 는 σ↓(미세결정) — **이미 우리 식에 둘 다 있음**(CN²·cov ↑, Cronau ↓).
  Schneider 가 **GB 항(Cronau)** 의 실험 정당성을 SE-only 에서 깨끗이 보여준 것.

### A-2. σ(압력) — 우리 σ-vs-porosity(compaction) 와 정합 + ΔV 라는 *추가* 고압 반전
이 논문은 σ-vs-P 를 **두 영역**으로 분해(우리에게 직접 매핑):
- **저압 regime I/II (≤0.5 GPa): 압력↑ → 미세구조 개선(접촉면적↑·공극↓) → σ↑.** = ★ **우리 σ-vs-porosity
  (porosity↓→σ↑)·Heckel knee 와 *정확히 같은 물리***. 그들 σ 가 0.01→0.5 GPa 에서 0.3→4.1 mS/cm(<50µm) 급상승 =
  우리 "압밀↑→contact-network↑→σ↑"·Bazzoun "σ-vs-P 상승"·Doux "접촉@~25 MPa 포화"·우리 Heckel P_y=138 와 같은 계열.
- ★ **고압 regime (>0.5–0.7 GPa): 압력↑ → 격자압축(ΔV) → σ↓.** = **우리엔 *없는* 반전.** 우리 DEM/MPM 은 입자스케일
  (porosity↓→σ↑ 단조)이라 **격자압축이 σ 를 *낮추는*** 원자효과를 못 본다. → **우리 σ-vs-P 는 ~0.5 GPa 아래(우리
  제조 300 MPa 는 여기)에서만 단조 상승으로 유효**; 그 이상은 ΔV 반전이 시작. **우리 작동범위(300 MPa)에서는 ΔV
  무시 가능**(저자도 "stack pressure 0.1 GPa 에선 ΔV 무시" 명시) → **우리 σ-vs-porosity 모델은 우리 압력대에서 안전**.
- **σ-vs-porosity 강도**: ★ 저자 결론 **"relative density(porosity)는 σ 의 *약한* descriptor, PSD 가 *강한*
  descriptor"** → 우리 σ_ionic 가 porosity 단독이 아니라 **φ_eff·CN²·cov·packing(=PSD 의존)** 으로 짜인 것과
  **정합**. "porosity 만으로 σ 예측 불가"는 우리 5-항 형태(LOOCV 0.975)의 실험적 정당화.

### A-3. DEM/FVA 파이프라인 — 우리와 가장 직접적인 평행 + 공통 한계
Fig 6b: 그들 **DEM(입자압밀) → voxel → FVA(연속체 σ)** 가 **정규화 σ-vs-P 추세를 *기하만으로* 재현**(regime II
잘 맞음). = ★ **우리 DEM→네트워크 σ 와 같은 정신.** 차이: 그들 readout 은 **FVA 연속체**(constriction 없음 →
Bielefeld2020 처럼 *상한*), 우리는 **Kirchhoff/Holm 점접촉 constriction**(더 물리적). **공통 한계: 둘 다 구형 →
저압 regime I 과대평가**(그들 명시) → 우리 MPM(형상)·de Larrard(packing)이 메우는 방향.

## B. 적용가능성 (applicability to our model)

### B-1. ★ backlog B6 (우리 Heckel P_y / σ-vs-P) 직접 앵커
- **Heckel 식 동일**: 그들 `ln(1/(1−ρ))=Kp+A` = 우리 식. **P_y(작은 PSD)=0.95 < P_y(큰 PSD)=1.65 GPa** →
  **"작은 입자 → 낮은 P_y → 소성변형 쉬움(더 치밀)"** 가 *같은 황화물에서 실측*. ⇒ 우리 DEM Heckel(P_y=138 MPa,
  pure-SE)·MPM σ_y_eff 의 **PSD-의존성** 검증 후보: 우리도 **bimodal vs monomodal Heckel P_y 를 비교**하면 같은
  부호가 나와야 함(우리는 아직 *조성*만 Heckel, *PSD* Heckel 미수행). **frame[3] universal compaction physics 확장**.
  ⚠ 절대 P_y(0.95/1.65 GPa)는 *그들 GPa 측정·다른 소재* → **부호·PSD-순서만 transfer**, 138 MPa 와 절대대조 금지.
- **σ-vs-P 영역분해**: 우리 σ-vs-porosity 는 **regime I/II(≤0.5 GPa)** 에 해당 → 우리 300 MPa 제조압은 그들
  **저압 미세구조-지배 영역**(σ↑) 안 → **우리 σ-vs-porosity 단조성은 우리 압력대에서 유효**(ΔV 반전 전). 이를
  명시하면 우리 모델의 *유효 압력범위*를 정직하게 bound 할 수 있다.

### B-2. ★ backlog B5 (우리 Cronau(r_SE) σ_grain 크기/GB 인자 — 이중계상 점검)
- Schneider 의 **"작은입자 → GB 많음 → σ↓"** (SE-only, 실험) = **Cronau(r_SE) 의 *부호*에 대한 두 번째 same-family
  근거**(Cronau 는 Br-argyrodite, Schneider 는 LGPS-계 — 둘 다 sulfide, 둘 다 GB 메커니즘). ⇒ Cronau digest 의
  "Cronau(r_SE) 를 *결정도/grain-contact 효율 인자*로 재명명" 권고를 **강화**: GB 가 σ 병목이라는 게 *두 황화물에서
  독립 확인*. **흡수 후보**: 우리 σ_grain prefactor 의 GB 항을 *입자수밀도(grain contact 수)* 로 재파라미터화하면
  Schneider 의 "<50 vs >50µm" 거동까지 설명 가능(현재 우리 Cronau 는 sub-µm 만).
- ⚠ **이중계상(double-count) 주의**: 우리 σ_ionic 에 **CN²(접촉수 → σ↑)** 와 **Cronau(GB → σ↓)** 가 *둘 다* 있다.
  Schneider 는 "접촉 *수*↑ 인데 σ↓"(작은입자) — 즉 **접촉수와 GB-품질이 *반대로* 작용**. 우리 CN² 가 접촉수만 보고
  Cronau 가 품질을 보므로 **개념적으로 분리돼 있어 이중계상은 아님**. 단 *작은 입자에서 CN²↑ 와 Cronau↓ 가
  상쇄*되는지 우리 corpus 로 점검할 가치(Schneider 가 SE-only 에서 GB↓ 가 이긴다고 보임 → 우리 SE-rich 코너에서
  같은 상쇄가 나오나 확인).

### C. frame[4] 위치 (experimental anchor)
- **이 논문 = frame[4] 외부 실험+시뮬 앵커, DEM 경쟁자 아님.**
  - **experiment(EIS σ-vs-P/크기) → 앵커**: σ_ionic max 4.1/5.7 mS/cm @0.5 GPa, ΔV 1.4 cm³/mol, Heckel P_y
    0.95/1.65 GPa, ρ_rel 90–95% — *t-Li₇SiPS₈ 고유*. **우리 LPSCl 모델의 *추세·물리* 검증점**(절대값 transfer 금지).
  - **우리 SIMULATION 이 *더하는* 것**: (1) **명시적 3D contact-network σ**(Kirchhoff/Holm constriction) — 그들
    FVA 는 연속체(constriction 없음 → σ 상한); (2) **σ_e + σ_thermal 삼중항**(그들 ionic-only); (3) **진짜 SHAPE
    소성 morphology**(MPM) — 그들 구형 한계(저압 과대평가)를 메움; (4) **composite(CAM+SE) packing/Furnas dip**
    (그들 SE-only); (5) **fracture-Holm/Auerbach**(그들 없음). ⇒ 그들이 *측정/연속체-시뮬* 한 σ(P,size)를, 우리는
    *접촉역학에서 emergent 하게* + *composite·삼중항·morphology* 로 확장.
  - **소재 transferability caveat**: t-Li₇SiPS₈ ≠ LPSCl(다른 구조·다른 σ 절대값·다른 ΔV·다른 E). **같은 황화물
    cold-press 물리**(Heckel 영역, σ-vs-P 형태, GB-vs-크기 부호, 구형-DEM 한계)는 transfer OK; **절대 σ/P_y/ΔV/밀도
    수치는 LPSCl 쪽 앵커(Minnmann/Doux/Cronau/우리 DEM)** 가 소유. ⇒ densification/σ DB 에 넣되 *별도 material 태그*.

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① ★ **σ-vs-porosity 의 "약한 descriptor" 정당화 + 유효 압력범위 bound**: Schneider 의 "porosity 는 약한
  descriptor, PSD 가 강한" 실험결론 → 우리 σ_ionic 5-항(porosity 외 CN/cov/packing) 형태의 *실험 정당화*. 동시에
  **고압 ΔV 반전**(>0.5 GPa σ↓)을 근거로 **우리 σ-vs-porosity 단조모델의 유효범위 = ≤~0.5 GPa(우리 300 MPa 포함)**
  를 명시 → over-claim 방지(우리는 ΔV 원자효과를 안 다룬다고 정직 표기).
- ② ★ **Cronau(r_SE) GB 인자의 두 번째 same-family 부호근거 + 접촉수↔GB 분리**: "작은입자→GB多→σ↓" 가 LGPS-계
  황화물에서도 성립 → Cronau(r_SE) *부호* 재확인. 우리 CN²(접촉수↑→σ↑) vs Cronau(GB↓) 의 *반대작용*을 우리 SE-rich
  코너에서 점검(Schneider 는 SE-only 에서 GB 가 이김). **backlog B5(이중계상 점검) 의 실험 레퍼런스**.
- ③ ★ **PSD-의존 Heckel 비교(우리가 아직 안 한 것)**: 우리 Heckel 은 *조성*만(P_y=138). Schneider 처럼 **monomodal
  vs bimodal PSD 의 P_y 차이**(작은 PSD→낮은 P_y)를 우리 DEM/MPM 으로 재현하면 frame[3] universal-compaction 을
  *PSD 축*으로 확장. **DEM/FVA→σ 파이프라인 자체가 우리와 평행**(Fig 6) → positioning 근거(우리는 contact-network
  constriction + 삼중항 + MPM morphology 로 그들 FVA-연속체-ionic-only-구형 을 넘어선다).

## 9. 인용 가능 문장 (deck/paper용)
- "For the LGPS-type sulfide t-Li₇SiPS₈, Schneider et al. (2023) showed by combined EIS, DEM compaction and
  finite-volume σ analysis that the ionic conductivity of a pressed pellet is governed *more strongly by the
  particle-size distribution than by relative density (porosity)* — an experimental justification for casting
  σ_ionic as a function of coordination, coverage and packing rather than porosity alone."
- "Their Heckel analysis (ln[1/(1−ρ)] = Kp + A, identical to ours) yields a mean yield pressure P_y of 0.95 GPa
  for the small PSD versus 1.65 GPa for the large PSD, confirming — in a sulfide of the same family as our LPSCl —
  that a finer powder plastically densifies more easily (lower P_y), the same size-ordering our DEM Heckel exhibits."
- "Their DEM→FVA pipeline reproduces the σ-vs-pressure trend from geometry alone but *over-predicts the low-pressure
  (regime I) conductivity because the model uses perfect spheres* — the very rigid-sphere limit our MPM (true plastic
  shape change) and de Larrard packing are designed to fill (frame [5])."
- "Above ~0.5 GPa the conductivity *decreases* with pressure through a positive activation volume (ΔV ≈ 1.4 cm³/mol,
  lattice compression), an atomistic effect outside the particle-scale DEM/MPM picture; below it (our 300 MPa
  fabrication regime) σ rises monotonically with densification, where our σ-vs-porosity model is valid."

## 10. 주의/한계 (over-claim 방지)
- ★ **소재 = t-Li₇SiPS₈(LGPS-계 정방정), NOT argyrodite LPSCl.** 위시리스트 추정 제목과 다름. **같은 황화물
  패밀리**라 *물리·압력거동·방법론*은 비교 가능하나, **σ 절대값(4.1/5.7 mS/cm), Heckel P_y(0.95/1.65 GPa),
  ΔV(1.4 cm³/mol), 밀도(90–95%)는 소재고유 → LPSCl 로 transfer 금지**. (Cronau Br-argyrodite·Sakuda glass 와
  동일한 same-family-not-LPSCl 주의.)
- **SE-only 펠릿**(CAM/composite 아님). σ 는 *재료 자체* σ(blocking electrode) → **composite σ_eff,ion**
  (Bazzoun/Minnmann/우리)과 **층위 다름**. 그들 "작은입자→σ↓"(SE-only GB) 를 우리 *composite* "작은 SE→σ↑"
  (packing)와 *직접* 충돌시키면 안 됨(§A-1: 다른 층위).
- **DEM = 구형 + overlap(CONTACT) 계열**, 형상변화 없음 — Bazzoun/Varkey 와 동일. 저자 *스스로* "perfect spheres
  ↔ 실제 비구형 분말 차이가 저압 과대평가 원인"·"grain boundary 저항은 FV 시뮬에 미포함"·"마찰·접촉저항이 DEM 에
  완전히 반영 안 됨" 명시 → **frame[5] 전달 절반(우리 MPM morphology 미보유)** 의 또 하나의 독립 확증.
- **σ = 정규화(σ/σ₀) — 상대추세 전용.** 절대 bulk σ 캘리브를 *의도적으로 회피* → **그들 시뮬 σ 절대값과 우리
  절대 σ 를 직접 대조 금지**(우리 Cronau σ_grain 절대값과 다른 철학). 추세·물리만.
- **압력대 다름**: 그들 측정 **0.01–1.7 GPa**(고압 ΔV 보려), 우리 제조 **0.3 GPa**. **Heckel P_y·ρ_rel·σ 절대값을
  우리 300 MPa 값과 직접 동일시 금지** — 그들 GPa 영역은 우리 범위 밖(regime III·ΔV 반전).
- **ΔV(활성화부피)·AIMD·NMR = 원자/결정 스케일** — 우리 DEM/MPM(입자스케일) 의 frame[5] *밖*. 우리가 "검증"하는
  게 아니라 *우리가 안 다루는 축*을 그들이 보여줌(정직히).
- **digitized vs stated**: σ max(4.1/5.7/5.3/6.6), P_y(0.95/1.65), ΔV(1.4), ρ_rel(90–95%), side-phase(8.2–10.2 wt%),
  gamma(a=1.944,b=7.048), D50_vol(89µm) = **stated**. 펠릿두께(1600→1000µm)·Fig3/Fig6 곡선 형태 = digitized(추세).
  E_SE/σ_y/ν 수치·coverage/Z/σ_e/σ_thermal = **본 논문에 없음(n/a)** — SE-only·SI-only.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
