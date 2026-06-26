# Kim 2024 (ACS Energy Letters, 동료심사 ORIGINAL) — Digital Twin Battery Modeling and Simulations ★ 우리 top-down/bottom-up POSITIONING의 PEER-REVIEWED 인용원 (= "Ref 127")

**인용(★ PDF에서 검증한 정확한 서지):** Suhwan Kim, **Hyobin Lee**, **Jaejin Lim**, Joonam Park, **Yong Min Lee**\* —
"Digital Twin Battery Modeling and Simulations: A New Analysis and Design Tool for Rechargeable Batteries,"
***ACS Energy Letters* 2024, _9_, 5225–5239.**  **DOI: 10.1021/acsenergylett.4c01931.**
Received **2024-07-16** · Revised **2024-09-09** · Accepted **2024-09-17** · Published **2024-10-03**.
© 2024 American Chemical Society.  Article type = **REVIEW (Focus Review)**.
소속: ¹DGIST(Daegu Gyeongbuk Institute of Science and Technology) 에너지공학과 · ²연세대 화공생명공학과(= **Digital
Twin Battery Lab, 이용민 LEAD**) · ³LG에너지솔루션 과천 R&D(박주남).  교신 **yongmin@yonsei.ac.kr** (ORCID
0000-0003-2002-2218).  ★ **저자 기여 각주: "S. Kim, H. Lee, and J. Lim contributed equally to this work."**
(= **이효빈·임재진 = DTBL 모델러** 공동 1저자 — 우리가 비교/이식하는 #271·#266·#262의 digital-twin 모델러 본인들.)

**★ 문서 성격 — 동료심사 저널 REVIEW(peer-reviewed):** 이건 **연세/DGIST DTBL 그룹의 방법론 도구논문(tool paper)**의
**정식 동료심사 원본**이다.  매거진(Choi 2024)과 달리 **peer-reviewed → 논문 인용에 review-safe**.  ⚠ 단
**#260-286 리스트(literature_yonsei_dtbl_2026.md)에는 번호가 없다**(리뷰/framework 자료 → 번호 부여 안 함);
**"보충/FRAMEWORK 리뷰 — peer-reviewed source"**로 파일링.  ⚠ **이 리뷰도 정량 수치 앵커가 아니다** — LPSCl
σ/porosity 절대 앵커는 **Bazzoun(`lit_bazzoun2026_dem_fem_rnm.md`)/Varkey/Minnmann/#266/#271** 그대로 유지.
**이 논문의 유일한 가치 = peer-reviewed TAXONOMY(top-down/bottom-up · multi-scale · 미세구조 descriptor · DTP/DTI)
= 우리 POSITIONING의 정식 인용원.**

**★★ 핵심 관계 — 이게 한국어 E.Chem 총설(`lit_choi2024_digital_twin_review_echem.md`)의 영문 PEER-REVIEWED 원본:**
한국어 총설(Choi 2024, E.Chem 매거진 Vol.16 No.1)의 **Fig 1b·2d·3·4e·5·6·7 전부 "[Ref 127의 허가 하에 재구성.
ⓒ 2024 ACS]"**로 표기돼 있었고, 그 **Ref 127 = 바로 이 논문(Kim 2024 ACS EL 9, 5225-5239)**이다.  즉
**E.Chem 총설 = 이 ACS EL 도구논문의 한국어 확장·대중화판**, **이 ACS EL = 그 원본**.  ⇒ **top-down/bottom-up
분류 + multi-scale 지도 + 미세구조 descriptor 어휘를 논문에 인용할 땐 — 매거진(번호 없음·非동료심사)이 아니라
이 ACS EL(vol 9, 5225-5239)을 인용**해야 안전.  **이 디제스트의 역할 = (a) 정확한 동료심사 서지 확정, (b)
매거진 대비 무엇이 더 rigorous/추가됐는지, (c) positioning 인용원 확정** — 매거진 디제스트와 중복 최소화(매거진
디제스트는 한국어 본문 인용·우리-출력 1:1 표를 이미 상세히 담음 → 여기선 "peer-reviewed에서 검증된 것 + 더한 것"에 집중).

DB 동반 파일: 없음(리뷰 = 수치 corpus 아님).  SI: 없음(Focus Review).  PDF 페이지: 본문 5225-5235(11p) + 참고문헌
5235-5239(118편).

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 왜 중요한가

**디지털 트윈(digital twin) = 물리 배터리의 가상 복제체로, 미세구조를 정량 분석해 실험으로 직접 못 보는 "숨겨진
파라미터(hidden parameters)"를 식별·예측하는 분석·설계 도구**라는 명제 아래, 동료심사 본문이 (1)
**atom/molecule → particle → electrode → cell → module/pack** multi-scale 지도(Fig 1a), (2) 미세구조 구성요소별
**구조 descriptor 분류**(Fig 1b: active material / conductive agent / binder / electrode / separator), (3)
**DTP(Digital Twin Prototype, 설계측) vs DTI(Digital Twin Instance, 물리시스템 연결측)** 구분, (4) ★ **3D 구조
형성의 두 방법론 — top-down(reconstruction) vs bottom-up(formation)**("STRUCTURE FORMATION METHODOLOGIES" §,
Fig 3), (5) 미세구조 해상(structure-resolved) 분석(Fig 4), (6) 전기화학·기계·열 **다중물리(Fig 5)**, (7) **AI 기반
multi-scale + 동적 시뮬레이션** 전망(Fig 6)을 종합한다.

**우리 hook(가장 중요):** 본문 §**"STRUCTURE FORMATION METHODOLOGIES"**가 정의하는 **Top-Down Method
(reconstruction) vs Bottom-Up Method(formation)**가 정확히 우리 positioning이다.  `positioning_vs_geodict.md`의
**"GeoDict = 구조-given 특성화(top-down/reconstruction) ↔ 우리 DEM+MPM = 공정에서 구조-예측(bottom-up/
formation)"**가 — 내가 발명한 구분이 아니라 **이 그룹(이용민 DTBL) 자신의 동료심사 ACS EL 논문이 명시적으로
NAMING한 필드 표준 taxonomy**다.  ⇒ **우리 DEM+MPM = 이 논문이 정의한 "bottom-up/formation" 범주**(본문이
**그 도구로 "discrete element method (DEM) and finite volume method (FVM)"를 명시**), GeoDict 사용 논문들
(#266/#271/#281/#284/#286/#275/#15/#16) = **"top-down/reconstruction" 범주**.  ★ **그리고 이젠 그 인용이
peer-reviewed(ACS EL 9, 5225-5239)** — significance에 넣어도 reviewer-safe.

---

## 0. 약어·핵심개념 (peer-reviewed 본문 정의)

- **Digital Twin:** "a virtual replica that accurately reflects the form and behavior of a physical object,
  system, or process."  초기 개념(Grieves, ref 5)은 **(i) 물리 시스템 · (ii) 가상 시스템 · (iii) 둘 간의
  양방향 정보흐름(bidirectional flow of information)** 3요소.
- **DTP (Digital Twin Prototype):** "DTP models contain essential information required to create physical
  objects, allowing **assessment and validation in the early design stage**."  ★ **우리 DEM+MPM = DTP**
  (설계측, 아직 특정 셀과 실시간 연결 X — 공정→구조→성능 설계 도구).  (ref 6, 8, 9.)
- **DTI (Digital Twin Instance):** "DTI models are continuously connected to physical objects throughout
  their life cycle, with **two-way data exchange**, enabling real-time monitoring and prediction of future
  behaviors."  (BMS측, physical-system-connected.)
- **★ Top-down method (reconstruction):** "involves acquiring **actual structural images** of electrodes or
  separators using advanced imaging techniques such as probe microscopy, electron microscopy, and X-ray
  computed tomography (XCT) ... **followed by structural reconstruction**."  = **측정된 구조에서 출발.**
- **★ Bottom-up method (formation):** "generates digital twin structures based on **design parameters, such
  as particle shape, composition, spatial distribution, and density** ... These parameters are input into a
  **stochastic model** for the 3D virtual microstructure."  = **설계 파라미터에서 구조 형성.**  ★ **우리
  DEM+MPM이 여기.**
- **Hidden parameters:** 실험으로 직접 측정 못 하나 셀 성능을 가르는 유효 구조물성(유효 전도도·tortuosity·접촉
  면적·percolation·dead particle).  Abstract 그래픽 제목 = **"Unraveling Hidden Parameters."**
- **Structure-resolved (microstructure-resolved) analysis:** voxel 해상 미세구조 정량.  SW: **Avizo, GeoDict,
  TauFactor, Fiji**(in-house / commercial / open-source).
- **Multiphysics:** 전기화학(electrochemical) + 기계(mechanical) + 열(thermal) 결합.
- **AM / CBD / SE:** active material / carbon-binder domain / solid electrolyte.

---

## 1. 서론·동기 (peer-reviewed, p.5225-5226)

- **Abstract(원문 요지):** "The intricate correlation between microstructural properties and performance in
  lithium rechargeable batteries necessitates advanced methods to elucidate their mechanisms.  ... digital
  twin simulations have been utilized by creating virtual replicas ... However, the relationship between
  microstructural parameters and battery performances is **still not fully understood**.  This focus review
  ... explore[s] microstructure formation and validation methods as **top-down and bottom-up simulation
  techniques** and provide[s] a comprehensive view of **multiphysics approaches** (electrochemical,
  mechanical, thermal) ... [and] **AI-driven multiscale modeling strategies and dynamic simulations**."
  → ★ **Abstract 자체가 top-down/bottom-up + 다중물리 + AI를 핵심 축으로 명시**(매거진 초록보다 더 명시적으로
  "as top-down and bottom-up simulation techniques"라는 문구를 씀).
- **동기(서론):** 전기차 시장 확대로 LIB가 **전기화학 성능 + 안전성**을 동시 요구.  전통 연구는 **소재 조성·제조
  공정의 실험적 최적화**에 집중 → 그러나 "these methods often encounter difficulties in predicting the
  **complex relationship between geometric microstructures and battery performances**.  This gap underscores
  the need for innovative approaches."  → 디지털 트윈의 필요성.
- **★ 리뷰의 차별점(서론, 본문 명시):** "There have been many existing review papers about digital twin
  battery simulations focusing on two-way connection ... (ref 6,12).  In contrast, several review papers deal
  with digital twin simulations for **microstructure formation and physics-based performance prediction**
  (ref 11,13,14).  **However, the identification of hidden parameters within the microstructure and their
  effect on battery performance have not been thoroughly discussed.  Furthermore, detailed discussions are
  needed on the digital twin structure formation and the verification process required for accurate
  structural analysis.**"  → ★ **본 리뷰의 4-차별점 = (a) hidden-parameter 식별 + (b) top-down/bottom-up 구조
  형성·검증을 전통 모델과 구별 + (c) 전기화학/기계/열 다중물리 + (d) AI multi-scale·동적 시뮬.**

---

## 2. ★ Multi-scale 지도 (Fig 1a, p.5226) — atom → pack

> **Fig 1a:** "A comprehensive overview of multiscale simulations from molecules to pack for analyzing
> material properties and battery performance."  5단계 스케일축(길이 스케일 명시) 각각에 (시뮬 대상)+(예측 물성).

| 스케일 | 길이(본문) | 시뮬 도구·대상 | 예측 물성(본문 원문) | **우리 위치** |
|---|---|---|---|---|
| **Atom / Molecule** | 10⁻¹⁰ m (Å) | **DFT / MD**(본문 명시) | **Thermodynamic Properties**: potential, Li diffusion behavior, activation energy, crystal/lattice stability | (우리 미사용) |
| **Particle** | 10⁻⁶ m (µm) | 입자 스케일 | **Material Properties**: physical/chemical properties, solid diffusion, phase transition, interfacial reaction, **volume expansion & crack** | ★ 우리 AM/SE 구(crack=fracture) |
| **Electrode** | 10⁻⁴ m (~mm) | **DEM, FVM**(본문 §bottom-up 명시) | **Electrode Performance**: effective structural properties, mass transport/charge transfer, **electronic/ionic conduction**, interfacial reaction, **mechanical stress** | ★★ **우리 DEM+MPM 스케일** |
| **Cell** | 10⁻² m (cm) | 셀 모델 | **Cell Performance**: capacity & power, current density distribution, cycle life, heat generation & transfer, mechanical stress | (Phase 4 PyBaMM 후보) |
| **Module & Pack** | ≥ 10⁰ m (m) | 시스템 | **BMS**: SOC estimation, power management, cycle life, thermal management, thermal runaway prediction | (우리 범위 밖) |

- **★ peer-reviewed 본문이 우리 E_eff softening을 정당화하는 정확한 문장(p.5226):** "Extending these
  atomic/molecular analyses to the particle and electrode scales reveals that **the intrinsic properties of
  the materials cannot be fully realized, and various performances and characteristics, such as physical and
  chemical properties, diffusion and conduction, charge transfer reaction and mechanical behavior, can be
  different depending on design parameters.**"  ★★ **이게 우리 E_eff 1.35(DEM)/1.53(MPM) softening의 동료심사
  레벨 근거** — 원자 스케일 bulk 단결정 **E_SE=24 GPa(=intrinsic property)가 전극 스케일에선 그대로 실현되지
  않고**(granular rearrangement/GB-slide 때문에) **softened proxy로 나타난다** = 논문이 말한 "intrinsic
  properties cannot be fully realized at the electrode scale"의 정확한 사례.  → 매거진은 같은 취지를 한국어로
  서술했지만, **이 동료심사 영문 문장("cannot be fully realized")이 인용에 더 강하다.**
- **본문(p.5226):** "In the electrodes, the particle-related parameters such as size, shape, and distribution
  vary depending on the composition of the materials.  Furthermore, the **contact area, porosity, and
  tortuosity**, resulting from the dispersion of these components, impact reaction kinetic and
  electron/ionic conductivity, thereby affecting battery performance (ref 18-20)."  ★ **= 우리 출력 축
  (contact area / porosity / tortuosity / σ_e / σ_ionic)을 동료심사 본문이 electrode 스케일의 핵심 결정자로 명시.**

---

## 3. ★ 미세구조 descriptor 분류 (Fig 1b, p.5226) — 우리 출력과 1:1

> **Fig 1b:** "Scheme for various components in the battery microstructure and their structural properties."
> Battery Microstructure(SEM-like 단면) → **5개 구성요소 + 각 descriptor(범례 텍스트, peer-reviewed 원문):**

| Fig 1b 구성요소 | **structural property (peer-reviewed 원문 범례)** | **우리 DEM+MPM metric** | DEM/MPM |
|---|---|---|---|
| **Active material** | **size, shape, orientation, coating, crack, …** | 입경분포(AM_P/AM_S)·scaffold 위치·MPM 소성 shape·**fracture(crack=Auerbach/Holm)** | DEM+MPM |
| **Conductive agent** | **shape, distribution, connection, …** | `additives.py` SuperP(점)/VGCF(섬유) morphology·**분산 CV**·**percolation(connection)** | DEM(voxel) |
| **Binder** | **shape, distribution, surface coverage, …** | PTFE fibril 형태·**surface coverage(cov_AM, Tabor/Hertz)** | DEM(StageE) |
| **Electrode** | **contact area, porosity, tortuosity, percolation pathway, …** | **contact area(StageE)·porosity·τ_Laplace,eff/τ_Dijkstra·percolation(f_p)·homogeneity** | DEM+MPM |
| **Separator** | **thickness, porosity, pore network, homogeneity, …** | (우리 범위 밖 — 양극 RVE) | — |

→ ★★ **이 표 = 우리 DEM+MPM이 이 논문(Ref 127)이 정의한 미세구조 descriptor를 정확히 출력한다는 증명, 이번엔
peer-reviewed 범례로 확정.**  특히 active material의 **"crack" = 우리 fracture**, binder의 **"surface coverage"
= 우리 coverage**, electrode의 **"contact area / porosity / tortuosity / percolation pathway" = 우리 StageE
coverage / porosity / τ / f_p** — descriptor 이름까지 일치.  ⚠ **매거진 Fig 1b 범례는 electrode를 "contact
area, porosity, tortuosity, **pore network**, homogeneity"로 옮겼는데, peer-reviewed 영문 원본은 electrode를
"contact area, porosity, tortuosity, **percolation pathway**"로, **separator를 "thickness, porosity, **pore
network**, homogeneity"**로 둔다** — "pore network"는 영문 원본에선 **separator** 항목, electrode 항목엔
**"percolation pathway"**.  → **descriptor 어휘를 논문에 쓸 땐 영문 원본 기준(electrode = percolation pathway)으로
정렬**(매거진의 미세 의역 교정).

---

## 4. ★★ 3D 구조 형성 방법론 — TOP-DOWN vs BOTTOM-UP (Fig 3, §"STRUCTURE FORMATION METHODOLOGIES", p.5229) ← 핵심

> ★★★ **peer-reviewed 본문의 독립 §제목 = "STRUCTURE FORMATION METHODOLOGIES"** → 그 아래 **"Top-Down Method."**
> + **"Bottom-Up Method."** 두 소제목.  **Fig 3** = "Schematic representation of the 3D digital twin structure
> formation methodologies": 위 = **Top-down approach**, 아래 = **Bottom-up approach**.  ★ **매거진엔 §제목이
> 한국어 의역이었으나, 동료심사 원본은 "STRUCTURE FORMATION METHODOLOGIES / Top-Down Method / Bottom-Up Method"라는
> 명시적 영문 소제목** → 인용 시 이 §명을 그대로 쓰면 됨.

### 4.0 도입(원문, p.5229)

> **"Because the quality of the 3D structure determines the accuracy of the derived simulation, it is
> critical to form highly realistic digital twin structures.  This is accomplished through **two primary
> methodologies: top-down and bottom-up methods.**"**

### 4.1 ★ Top-Down Method (= reconstruction) — p.5229

**정의(peer-reviewed 원문):** **"The top-down method involves acquiring actual structural images of
electrodes or separators using advanced imaging techniques such as probe microscopy, electron microscopy,
and X-ray computed tomography (XCT) (Figure 3, top).  These techniques provide high-resolution images that
capture the intricate nano and micro geometries ... including material morphology, heterogeneities, and pore
connectivity.  ... **followed by structural reconstruction.**"**

- **대표 기법(Fig 3 위 — domain volume vs voxel size 차트 + FIB-SEM·XCT 모식도):**
  - **FIB-SEM / TEM:** "resolution down to a few or tens of nanometers."  ★ **한계(원문): "the observable
    domain size is limited to tens of micrometers, and as a destructive analysis method, it cannot be free
    from sample damage and is difficult to conduct operando analysis."**
  - **XCT:** "use nanometer-scale wavelengths, which are relatively higher than electron beams, offering
    relatively lower resolution but expanding the observable area from micrometers to millimeters."  ★
    **장점(원문): "as a nondestructive method, it prevents specimen damage ... and allows for operando
    analysis to observe real-time structural changes."**  (차트엔 X-ray CT / Nano X-ray CT / FIB Tomography /
    Transmission Electron Tomography / Atom Probe Tomography 스펙트럼.)
  - "Recently, combined approaches have emerged to reflect and analyze complex microstructures more
    accurately"(multi-modal).
- ★ **= 측정된(measured) 실제 구조 → 재구성(reconstruct).**  본문이 곧장 잇는 응용: "active materials are
  observed at scales of tens to hundreds of micrometers, while **carbon binder domain (CBD) phases are
  observed locally at several micrometers using FIB-SEM or nano-CT** ... effective diffusion and conduction
  properties of the CBD phase are then calculated ... **compensating for the inability of the electrode
  microstructure-resolved model to explicitly reflect the CBD pores** (ref 45,55)."  ★ **= 우리 voxel CBD
  서브해상 처리(SuperP/VGCF를 voxel로)와 같은 문제·해법** (Lu et al. ref 56 = reconstructed electrode 유지한
  채 CBD porous phase 형성 → #266/#271 GeoDict workflow).

### 4.2 ★ Bottom-Up Method (= formation) — p.5229-5230  ← 우리 DEM+MPM이 여기

**정의(peer-reviewed 원문):** **"Conversely, the bottom-up method generates digital twin structures based on
**design parameters, such as particle shape, composition, spatial distribution, and density.**  Structural
parameters can be obtained through measurements such as **SEM, particle size analysis (PSA), and
Brunauer-Emmett-Teller (BET) surface area analysis** (ref 1,34,40).  ... efforts are being made to
incorporate detailed information, such as **particle shape, grain structure, CBD distribution, and the
morphology and distribution of fibers and pores** (ref 60,61,63,64).  These parameters are input into a
**stochastic model for the 3D virtual microstructure.  The generated models are validated against
experimental data** to enhance structural consistency and reliability, allowing for the comparison and
analysis of various design parameter modifications (Figure 3, bottom)."**

- ★★ **핵심 도구 명시(peer-reviewed 원문, p.5230):** **"To effectively simulate the internal distribution
  and morphology, computational techniques like the **discrete element method (DEM) and finite volume method
  (FVM)** are employed to model **particle interactions and the morphological changes under compression.**
  The bottom-up approach offers significant flexibility in exploring a wide range of design configurations
  and optimizing electrode or separator properties through virtual modeling (ref 39,73-75)."**  ⇒ ★★★
  **동료심사 본문이 bottom-up formation 도구로 DEM·FVM을 명시 호명, 그리고 "morphological changes under
  compression"을 그 역할로 명시** — **우리 DEM(=particle interactions) + MPM(=morphological changes under
  compression)이 정확히 이 문장의 구현.**  (매거진도 같은 문장을 한국어로 옮겼으나, **이 영문 원본이 인용에 더
  강하다.**)
- **검증(Fig 3 아래 — "Generation" → 3단계, peer-reviewed 그림):**
  - **Structural Information**: **Loading Level · Density · Composition**(실험 입력, ref 34/51).
  - **Modeling**: ★ **LPSCl + NCM 70 wt% 3D 가상구조 생성(색분리 voxel)** — **정확히 우리 소재계(LPSCl+NCM) +
    우리 조성대(NCM 70 wt%)!**  (Fig 3 캡션: "Reproduced with permission from ref 34. Copyright 2020 John
    Wiley ... ref 51 ... 2023 John Wiley" — ref 34 = Park et al. *Adv. Energy Mater.* 2020 Digital-Twin-Driven
    All-Solid-State Battery, ref 51 = Song et al. *Adv. Energy Mater.* 2023.)
  - **Validation**: Experiment(실선) vs Simulation(점) 방전곡선 **1C/2C/4C/8C (Voltage vs Time)** 일치도.
  - 본문(p.5230, "Microstructure-Resolved Characterization" §): "particle size and distribution within the
    electrode (ref 65,66) and specific surface area (ref 40) of 3D structures was validated against actual
    samples.  After confirming the structural consistency, further validations for predicting battery
    performance are required" → **단일입자 전압(ref 51) · in situ STXM Li 분포(ref 67) · 율속별 σ·전압 비교
    (ref 54,56,68) · 응력-변형 곡선(ref 63,69) · 열전도(ref 70).**  ★ **= 우리 bottom-up 구조의 검증 경로
    (porosity↔#266/Minnmann, σ↔Bazzoun/#271)의 필드 표준.**

### 4.3 ★ peer-reviewed 비교 요약표 (vs 매거진 — 무엇이 같고 무엇이 추가됐나)

| 축 | **Top-Down (reconstruction)** | **Bottom-Up (formation)** | 매거진 대비 |
|---|---|---|---|
| 출발점 | **측정된 실제 구조**(XCT/FIB-SEM/TEM 영상) | **설계 파라미터**(shape·composition·distribution·density) | = 동일 |
| 구조 생성 | 영상 → **structural reconstruction** | 파라미터 → **stochastic model** | ★ peer-reviewed가 "stochastic model" 명시 |
| 도구 | FIB-SEM, TEM, XCT(+APT/nano-CT) | **DEM, FVM**(+ stochastic) | ★ §명 "STRUCTURE FORMATION METHODOLOGIES" |
| 강점 | 실제 형상 충실(불균일·결함 그대로) | **설계 자유 탐색·최적화**(원문: "significant flexibility in exploring a wide range of design configurations") | ★ 영문 강점 문장 |
| 한계 | **분석영역 제한·시료손상·operando 불가**(FIB-SEM) | 생성구조의 **실험-검증 필요**(원문 명시) | ★ 영문 한계 문장 |
| **우리/상용** | GeoDict 논문(#266/#271/#281/#284/#286/#275/#15/#16) | **우리 DEM+MPM**(process-physics 하위유형) | = positioning |

→ ★★★ **이 표 = `positioning_vs_geodict.md`의 필드-표준 어휘 버전, 이젠 peer-reviewed로 확정.**  단 **정직한
정합 주의(매거진 디제스트와 동일):** 이 논문의 bottom-up은 **"설계 파라미터 → stochastic model"**까지 포함
(확률적 생성, 예: ref 63,64 stochastic reconstruction).  **우리 DEM+MPM은 bottom-up 중에서도 가장 강한 형태 —
"공정(압력) 물리에서 구조를 역학적으로 형성"**(확률적 배치가 아니라 압축 시뮬).  즉 **우리는 bottom-up/formation
범주에 속하되, 그 안에서 "process-physics-driven formation"이라는 가장 predictive한 하위유형**(stochastic
placement보다 한 단계 더 — 압력→구조 인과; 본문도 DEM을 "particle interactions and morphological changes under
compression"으로 호명해 우리 쪽 = process-physics임을 뒷받침).

---

## 5. 디지털 트윈 미세구조 해상 분석 (Fig 4, p.5230) — Microstructure-Resolved Characterization

> **Fig 4:** "Digital twin microstructure-resolved structural analysis" — 5개 분석축(a~e).  SW: **Avizo,
> GeoDict, TauFactor, Fiji**(in-house/commercial/open-source) 명시.

- **(a) Size & Morphology**: Won et al. STEM 기반 탄소 3D 호스트 재구성 + 그래핀 gap 분포(ref 76).  → 우리
  입경분포·morphology.
- **(b) Orientation**: 개별 NCM 입자 배향(XCT, ref 56); Ebner et al. NCM/LCO/graphite 입자 장축 수평 정렬(ref 41).
  → ★ 우리 **미모델**(구-입자 → 배향 없음, honest gap).
- **(c) Connectivity**: **Percolation(0.37 vol%) / Unconnected Phase(Inactive Objects) / Distribution
  (Ceramic in Hybrid Electrolyte)**(ref 77,78).  ★★ **= 우리 percolation(f_p) + dead-particle(σ=0 고립) +
  분산 = σ_e/σ_ionic 접촉망 분석과 동일축.**  (Jia et al. ref 77 = 입자 주입 시뮬로 ion flux homogeneity →
  separator pore network.)
- **(d) Contact Loss**: **Intergranular Crack / Void in Cathode(after 50 cycles) / Void in Solid Electrolyte
  (1.0 mAh/cm²)**(ref 78,79,80,81).  ★★ **= 우리 fracture(Auerbach/Holm σ↓) + MPM void + StageE 접촉면적
  감소.**  ★ 본문(p.5231): "Gao et al. revealed that the main degradation mechanism of sulfide-based
  solid-state batteries operating at low pressures is related to the **interparticle voids through volume
  changes of the cathode active materials** through plasma FIB-SEM-based microstructures (ref 80)" + "the
  **crack propagation of the sulfide electrolyte just before lithium penetration** was visualized through 3D
  rendering obtained from in situ XCT (ref 81)."  ★★★ **= 우리 LPSCl 양극의 interparticle void + 전해질 균열을
  동료심사 본문이 ASSB 열화의 주기작으로 명시 = 우리 fracture·void-fill·StageE가 푸는 정확한 문제.**
- **(e) Passivation Layer**: Müller et al. ptychographic XCT + 전송 X선으로 Si 입자 SEI 두께(ref 82).  → 우리
  **미모델**(SEI = 화학 부반응, 기계/transport 모델 밖).
- ★ **본문(p.5230, ASSB 직접 맥락):** "In the field of solid-state batteries (SSBs), **interparticle contact
  significantly affects battery performance, making it essential to control the design of the microstructure.
  Neumann et al. first performed microstructure-resolved electrochemical simulations depending on the
  composition and loading of sulfide-based solid-state electrodes (ref 91).**  Subsequently, digital twin
  electrochemical simulations were applied in solid-state battery research involving various types of solid
  electrolytes and electrode designs (ref 34,35,100-103) ... **Dynamic modeling techniques, such as DEM and
  coarse-grained molecular dynamics (CGMD), were used to create 3D electrode structures and perform
  microstructure-resolved performance predictions, thereby unveiling the influence of drying conditions and
  calendering degree** (ref 50,104)."  ★★ **= 우리 작업(황화물 ASSB + DEM + calendering/압축 + 미세구조-해상)의
  직접 선행 맥락을 동료심사 본문이 정리** — 우리는 그 위에 **σ triad(σ_ionic/σ_e/σ_thermal) + MPM 소성 morphology
  + fracture**를 추가한다.

---

## 6. 다중물리(Multiphysics) 시뮬레이션 (Fig 5, p.5231-5232)

> **Fig 5:** "Physics → Multiphysics" — 5개 패널(a~e).

- **개념(p.5231):** "Physical phenomena that occur in actual batteries are **intertwined**.  For example,
  heat is generated due to current flow, and volume changes of the active material occur due to the Li⁺
  (de)intercalation by electrochemical reaction.  Therefore, **by coupling and analyzing a greater number of
  physical phenomena together, the influence of the microstructure on battery performance can be understood
  with greater accuracy.**"  ★ **= frame[5] 다중물리 버전 + 우리 DEM(transport)+MPM(mechanics) 결합의
  동료심사 정당화.**
- **Fig 5 5개 패널(peer-reviewed):**
  - **(a) Electrochemical**: LIB Electrode(**CBD + CBD Clogging vs CBD + Full Clogging**) + SSB Electrode
    (Li⁺ Concentration, Electron Current Density) + 제조 파라미터 진화(**Slurry → Dried electrode →
    Calendered electrode → Discharged electrode**)(ref 50,68,91).  ★ **calendered = 우리 압축; CBD clogging =
    우리 CBD 이온채널 blocking(#284/#275 trade-off).**
  - **(b) Mechanical**: **10/20/30/40 MPa Compression** displacement field(ref 69, Lagadec et al. separator
    compression).  ★★ **= 우리 MPM 압축 변위장(다압력 wallP)과 동형.**
  - **(c) Fluid dynamics**: 3D full-cell microstructure → **Lattice Boltzmann model(LBM)** 전해질 침투
    saturation(35%/50%/80%, ref 92).  → 우리 **미모델**(ASSB는 SE 고체라 관련 낮음).
  - **(d) Electrochemo-mechanical**: 리튬화(Degree of Discharge)별 **von Mises stress (VMS 1.10 / 1.48 / 2.44
    / 4.19 MPa)** + Hydrostatic Stress + **Graphite/Silicon electrode (0.1C/1C von Mises)**(ref 51,94).  ★★
    **= 정확히 우리 MPM von Mises 응력장 + chemo-mechanical.**  본문(p.5232): "a reconstructed
    LiNi₀.₇Co₀.₁₅Mn₀.₁₅O₂ (NCM711) particle-resolved electrochemo-mechanical model was developed considering
    **volume expansion depending on lithiation using the hygroscopic swelling equation (ref 51)** ... enabled
    the prediction of the structures where **stress is concentrated and cracks are prone to occur** in
    advance ... **potential delamination points of the CBD and the current collector could be predicted.**"
    ★ **= 우리 MPM 응력집중·crack 예측(단 우리는 압축 응력장, 그들은 리튬화 swelling 응력장 — 결합 시 Phase 4).**
  - **(e) Thermo-electrochemical**: 작동 중 발열 분해 **Ionic / Electronic / Reaction / Entropic heat**
    (resistive heat in electrolyte; areal heat)(ref 95).  ★ **= 우리 σ_thermal triad의 발열 맥락**(우리 κ 유효
    열전도 ↔ 그들 발열원 분해 — 상보).
- ★ **본문(p.5232):** "In systems where interparticle contact is crucial for performance, such as
  **solid-state batteries, analyzing the distribution of heat generation within the microstructure can be
  useful for discovering the practical issues by charge inhomogeneity or local degradation where temperature
  or heat is high.**"  → 우리 σ_thermal + 접촉망 발열 정량의 동료심사 가치 진술.

---

## 7. AI 기반 디지털 트윈 + 동적 시뮬레이션 (Fig 6, p.5233-5234) — ★ 매거진 Fig 6+7을 ACS EL은 Fig 6 한 장으로

> ⚠ **매거진은 이 부분을 Fig 6(AI surrogate)+Fig 7(동적 시뮬) 두 장으로 나눴는데, 동료심사 원본은 Fig 6 한 장
> (a)+(b)로 합쳐 둔다.**  ACS EL **Fig 6(a) = AI multiscale upscaling(매거진 Fig 6a+7a)**, **Fig 6(b) =
> digital twin dynamic simulation(매거진 Fig 7b)**.  → 그림 번호 인용 시 **ACS EL 기준 Fig 6**.

> **Fig 6:** "Perspective on digital twin battery simulation.  (a) Schematic diagram of the advanced
> methodology for constructing digital twin structures for **multiscale upscaling modeling using the
> application of AI technologies.** (b) **Digital twin dynamic simulation** of various electrode and separator
> behaviors."

### 7.1 ★ peer-reviewed 본문이 명시한 3-소절(매거진엔 강조 텍스트 박스로만 있던 것)

동료심사 §은 **"1. AI-Based Techniques for Enhancing Multiscale Structural Property Characterization. /
2. Advancing Structure Measurements and Computational Power for Enhancing Precision and Reliability. /
3. Dynamic Digital Twin Simulation for Comprehensive and Predictive Analysis."** 세 번호 소절로 구조화 —
**매거진은 이걸 한국어 강조 박스로만 흩어 놨으나, 동료심사 본문은 명시 번호 소제목으로 정돈**(= 더 rigorous).

- **(소절 1) AI surrogate (Fig 6a 상단 — CNN vs marker-based watershed):** "Conventional methods for forming
  digital twin microstructures such as **watershed algorithm-based top-down or stochastic bottom-up
  approaches have limitations in precisely capturing the nanostructures.  These challenges can be overcome
  through the application of AI-based technologies.**"  ★ **AI-driven segmentation이 top-down(watershed) +
  bottom-up(stochastic) 둘 다의 nanostructure 한계를 보완** → **AI가 nanoscale 추출 → 더 큰 도메인으로 upscale.**
  본문 강조: "**AI-based techniques can extract critical structural parameters from nanoscale domains and
  utilize these data to generate additional structural regions, effectively expanding domain scales** (ref
  110)."  ★ **= 우리 scaling-law predictor의 개념(σ_ionic LOOCV 0.975 / σ_e 0.953 / σ_thermal 0.90 = design-knob
  →metric AI surrogate).**  (Finegan et al. ref 110 = ML로 3D 방전곡선 수초 재현·수천 변수 탐색.)
- **(Fig 6a 하단 — nano→electrode upscaling):** Nanostructure Properties(**Electron network / Ion network /
  Coverage**) → Electrode Properties(**Rate / Current / Overpotential / SOC**).  ★ **coverage가 nano→
  electrode upscaling의 입력으로 명시 = 우리 coverage metric의 역할.**
- **(소절 2) 측정·계산 하드웨어:** FIB-SEM cryo(ref 111,112)/PFIB(ref 50,114)/synchrotron XCT(ref 115,116) +
  **HPC/GPU/cloud/quantum computing**으로 정밀·확장성 확보.  → 우리 GPU MPM(Taichi)·predictor 가속의 필드 표준.
- ★ **(소절 3) 동적 시뮬 — Fig 6b 결함 휠(매거진 Fig 7b):** "Dynamic digital twin simulations enable a
  comprehensive analysis of structural changes ... including **deformations and degradations** ... such as
  **phase transitions and lithium plating** ... particularly evident in materials with high strain (e.g.,
  alloying or deposition mechanisms) or with low crystal stability."  **Fig 6b 휠 = Cathode(Crack
  propagation · Contact loss · Degradation: Layered/Rock salt) / Membrane(Membrane deformation) /
  Anode(Volume expansion · Delamination · Lithium plating).**  ★★ **= 우리가 하는 것(crack/contact loss/
  volume = 우리 fracture·StageE·MPM)과 안 하는 것(delamination/rock-salt/plating/membrane = 화학·계면·동적)을
  동료심사가 한 휠로 명명** → frame[5] 분업 + honest gap의 인용 근거.
- ★ **manufacturing/spring-back은 어디?** ⚠ **주의(매거진과 다름):** 매거진 Fig 6c "압연 DEM 학습 공정모델
  (압축-spring back-접촉/다공/굴곡; Galvez-Aranda)"은 **ACS EL Fig 6에는 별도 패널로 없다** — ACS EL은 manufacturing
  parameter(slurry/dried/calendered)를 **Fig 5a(다중물리 electrochemical)**에 두고, dynamic 변형을 Fig 6b에 둔다.
  → **spring-back/압연 공정모델을 우리 future-work 근거로 쓸 땐 매거진 Fig 6c가 아니라 본문 ref 50,104(drying/
  calendering DEM) + Fig 5a(calendered electrode) + Fig 6b(dynamic deformation)로 인용**(동료심사 안전).  우리
  MPM이 rate-independent J2라 spring-back 미구현이라는 #285 한계는 그대로.

### 7.2 요약·전망 (SUMMARY AND PERSPECTIVES, p.5232 + 5234)

- **§제목 = "SUMMARY AND PERSPECTIVES"**(peer-reviewed).  "3D digital twin battery modeling and simulations
  play a pivotal role ... particularly through microstructure-resolved analysis.  The methodologies for 3D
  digital twin structure formation, including **both top-down and bottom-up methodologies**, have enabled the
  **identification of hidden microstructural parameters affecting battery performance.**"
- ★ **제한사항(원문 3가지, 매거진과 동일하나 영문 확정):**
  1. **스케일·정확도:** "Most microstructural analyses are limited to **domains of tens of micrometers**, and
     nanoscale properties are often treated as effective properties due to computational constraints.  ...
     Accurately reflecting nanoscale morphologies within larger sample sizes requires advancements in both
     measurement and calculation methodologies."
  2. **동적 거동 추정 난이도:** "another limitation ... is the difficulty in estimating the dynamic behaviors
     ... materials ... are prone to **cracking, volume expansion, or contact loss** during operation ...
     **dynamic simulations are required** ... but they also further intensify computational demands."
  3. **AI 가속 필수:** "advancements in computational power, both hardware and software, combined with the
     development of dynamic simulation technologies, will broaden the applications."  + "**These advancements
     will not only enhance the prediction of first-life performance but also optimize battery reuse and
     application in second-life applications.**"  ★ (= 매거진엔 없던 **second-life/재사용** 명시 — peer-reviewed 추가.)
  ★ **우리 작업이 채우는 자리:** **DEM/MPM이 입자스케일 동적 거동(압축·균열·void-fill)을 직접 모사**(리뷰가
  어렵다 한 (2)) + **scaling law가 AI 가속**(리뷰의 (3)).

---

## 8. 그림 한 장씩 — 무엇을 보이고 우리가 쓸 것 (★ ACS EL 그림 번호 = 인용 기준)

| Fig (ACS EL) | 페이지 | 무엇을 보이는가 | ★ 우리가 쓸 것 | 매거진 대응 |
|---|---|---|---|---|
| **1a** | 5226 | atom→pack 5-스케일 + 스케일별 시뮬·물성 | ★ 우리 = **electrode 스케일**(DEM·FVM 명시); "intrinsic properties cannot be fully realized at electrode scale" = E softening 근거 | Fig 1a |
| **1b** | 5226 | 미세구조 5요소 descriptor(AM crack·도전재 connection·binder coverage·electrode contact area/porosity/tortuosity/**percolation pathway**·separator pore network) | ★★ **우리 출력 1:1**(peer-reviewed 범례; electrode="percolation pathway", pore network=separator 항목 — 매거진 의역 교정) | Fig 1b |
| **2a-d** | 5227 | DT 개념(a) + ASSB vs LIB Ragone+NCA95(b) + hidden-parameter 가시화(c) + 4-목표 반응표면(d) | ★★ (c) Contact Area·Active Surface Area(Binder Coverage)·Ion/Electron Pathway·Distribution Uniformity·Tortuosity·**Dead Particles**·Side Reaction = 우리 출력; (d) 4-목표 = 우리 Phase 1-5 | Fig 2a-d |
| **3** | 5228 | ★★ **Top-down(XCT/FIB-SEM→Reconstruction) vs Bottom-up(설계파라미터→stochastic→Generation; DEM/FVM; LPSCl+NCM 70wt% 예시 + 1C/2C/4C/8C 검증)** | ★★★ **positioning NAMING — 우리=bottom-up/formation, GeoDict=top-down/reconstruction; §명 "STRUCTURE FORMATION METHODOLOGIES"** | Fig 3 |
| **4a-e** | 5230 | 구조-해상 5축(Size/Orientation/**Connectivity**/**Contact Loss: SE void·intergranular crack**/Passivation); SW Avizo·GeoDict·TauFactor·Fiji | ★ Connectivity=우리 percolation·dead-particle; Contact Loss=우리 fracture·MPM void(Gao ref80 ASSB interparticle void; ref81 LPSCl 균열) | Fig 4a-e |
| **5a-e** | 5231 | 다중물리(Electrochemical+**calendered**/**Mechanical 10-40MPa 압축 변위**/Fluid LBM/**Electrochemo-mech von Mises 1.10-4.19MPa**/Thermo 발열분해) | ★★ (b) 압축 변위장 + (d) von Mises = 우리 MPM; (a) calendered = 우리 압축; frame[5] 다중물리 정당화 | Fig 5a-e |
| **6a-b** | 5233 | ★ **AI multiscale upscaling**(CNN vs watershed; nano network/ion network/**coverage**→rate/current/overpotential/SOC) + ★ **동적 시뮬 결함 휠**(crack/contact loss/volume vs delamination/plating/membrane) | ★★ (a)=우리 scaling-law predictor + coverage upscaling; (b)=우리 하는 것(crack/contact/volume) + honest gap(delamination/plating) | ★ 매거진 Fig 6+7을 ACS EL은 Fig 6 한 장으로 합침 |

---

## 9. ★★ 매거진(Choi 2024) 대비 — 무엇이 같고 무엇이 더 RIGOROUS/추가됐나 (이 디제스트의 핵심 차별)

> 매거진 디제스트(`lit_choi2024_digital_twin_review_echem.md`)는 **한국어 본문 인용 + 우리-출력 1:1 표**를 이미
> 상세히 담았다.  여기선 **동료심사 원본에서만 확정되는 것 + 매거진과 달라지는 것**만 정리(중복 회피).

### (A) ★ SAME — 동일한 골격(매거진 = 이 ACS EL의 한국어판이므로 당연)
- multi-scale 지도(atom→pack), top-down/bottom-up 분류, DTP/DTI, 미세구조 descriptor, 다중물리(전기화학·기계·열),
  AI surrogate·동적 시뮬 — **5축 골격 동일.**  매거진의 Fig 1b/2d/3/4e/5/6/7이 전부 이 논문에서 왔으므로 **핵심
  taxonomy·그림은 1:1.**  → **우리 positioning·descriptor 1:1 맵(매거진 디제스트 §3·§8·§11 (B) 표)은 그대로 유효**,
  단 **인용원만 매거진 → 이 ACS EL로 교체.**

### (B) ★★ MORE RIGOROUS / 추가 — 동료심사 원본에만 있는 것 (논문 인용에 이걸 써라)
1. **명시 §제목·소제목(영문):** **"STRUCTURE FORMATION METHODOLOGIES"** → **"Top-Down Method." / "Bottom-Up
   Method."**; **"MICROSTRUCTURE-RESOLVED CHARACTERIZATION"**; **"MULTIPHYSICS SIMULATION"**; **"SUMMARY AND
   PERSPECTIVES"** + AI §의 **번호 소절 1/2/3.**  → 매거진은 한국어 의역 §명이었으나, **인용 시 이 영문 §명을
   그대로 쓰면 reviewer가 원문 대조 가능**(rigor↑).
2. **핵심 정의 문구의 영문 원문(인용 가능):**
   - top-down = "acquiring **actual structural images** ... followed by **structural reconstruction**."
   - bottom-up = "generates ... based on **design parameters** ... input into a **stochastic model** ...
     **validated against experimental data**."
   - 도구 = "**discrete element method (DEM) and finite volume method (FVM)** ... model particle interactions
     and the **morphological changes under compression.**"
   - E softening 근거 = "**intrinsic properties of the materials cannot be fully realized** ... at the
     particle and electrode scales ... **can be different depending on design parameters.**"
   → **매거진 디제스트는 이걸 한국어로 옮겼으나, 이 영문 원문이 인용에 직접 쓸 수 있는 형태.**
3. **descriptor 범례 정밀화:** electrode = "contact area, porosity, tortuosity, **percolation pathway**"
   (매거진은 "pore network"로 의역); "pore network"는 **separator** 항목.  → **우리 descriptor 라벨 정렬 시
   영문 원본 기준**(electrode=percolation pathway).
4. **118편 참고문헌(완전):** 매거진엔 없던 **전체 ref 리스트** — 우리가 이미 디제스트한 그룹 논문들의 정확한 좌표:
   **ref 32 = Park et al. *Nano Energy* 2021(#266 계열 ASSB 3D DT), ref 34 = Park et al. *Adv. Energy Mater.*
   2020 Digital-Twin-Driven ASSB, ref 35 = Lim et al.(Synergistic Halide-Sulfide), ref 51 = Song et al.
   *Adv. Energy Mater.* 2023(NCM811 crack propagation, electrochemo-mech), ref 33/36 = Clausnitzer et al.
   (ASSB composite cathode structure-resolved).**  → **이 ref들이 우리 #266/#271/#262의 동료심사 좌표** →
   인용 그래프에서 우리 작업을 이 그룹 논문군에 정확히 연결.
5. **second-life/재사용 전망:** 매거진엔 없던 **"optimize battery reuse and application in second-life
   applications"** 명시(전망 §).  → 우리 predictor의 확장 서사(첫-수명 예측 → 재사용)에 동료심사 근거.
6. **저자 기여 각주:** "S. Kim, H. Lee, and J. Lim contributed equally" — **이효빈·임재진이 공동 1저자**임이
   명시(매거진엔 기여 표기 없음).  → 우리가 비교하는 #271/#266/#262의 모델러 본인들이 이 taxonomy의 저자임을 확정.

### (C) ⚠ 매거진과 달라지는 점(혼동 금지)
- **그림 번호:** 동적 시뮬 = **ACS EL Fig 6b**(매거진은 Fig 7b).  AI surrogate = **ACS EL Fig 6a**(매거진은
  Fig 6a+7a 분할).  **압연 DEM 공정모델(Galvez-Aranda) 별도 패널은 ACS EL Fig엔 없음**(매거진 Fig 6c) → 본문
  ref 50,104 + Fig 5a(calendered)로 인용.
- **§ 수:** ACS EL 본문 6 §(서론 / STRUCTURE FORMATION / MICROSTRUCTURE-RESOLVED CHAR / MULTIPHYSICS / AI-§ /
  SUMMARY) + Fig 6장; 매거진은 7 Fig.

---

## 10. 기술 미니용어집 (peer-reviewed 정의 기준)

- **Digital Twin / DTP / DTI:** 가상 복제체 / **early-design-stage assessment(우리 DEM+MPM=DTP)** / physical-
  system-connected two-way(BMS).
- **★ Top-Down (reconstruction):** "actual structural images ... followed by structural reconstruction"
  (XCT/FIB-SEM/TEM).  = GeoDict 논문(#266/#271/#281/#284/#286/#275/#15/#16)의 입력 방식(측정/CAD IN).
- **★ Bottom-Up (formation):** "design parameters ... input into a stochastic model ... validated against
  experimental data"; 도구 = **DEM·FVM**("particle interactions and morphological changes under
  compression").  ★ **우리 DEM+MPM = process-physics-driven 하위유형**(확률 배치가 아닌 압축역학).
- **Structure-resolved analysis:** voxel 해상 정량(Avizo/GeoDict/TauFactor/Fiji).
- **Hidden parameters:** "Unraveling Hidden Parameters"(Abstract 그래픽) — Contact Area·Active Surface Area·
  Ion/Electron Pathway·Distribution Uniformity·Tortuosity·Percolation·**Dead Particles**·Side Reaction.
  = 우리 σ triad·coverage·τ·f_p·dead-SE/AM.
- **Dead particle:** "electronically isolated active material and ionically disconnected electrolyte regions"
  (본문 p.5229, Fig 2c·4c).  = 우리 σ=0 비퍼콜레이션 클러스터.
- **Multiphysics:** 전기화학+기계+열 결합("intertwined ... coupling ... greater accuracy").  frame[5] 다중물리.
- **AI surrogate / multiscale upscaling:** "extract critical structural parameters from nanoscale domains ...
  expand domain scales"(ref 110).  = 우리 scaling-law predictor.
- **Calendering / Calendered electrode:** 압연 치밀화(Fig 5a: Slurry→Dried→Calendered→Discharged).  = 우리
  300 MPa 압축(#276 §3.4·#285와 동일).
- **Spring-back:** ⚠ **ACS EL Fig엔 별도 패널 없음**(매거진 Fig 6c) — 본문 ref 50,104(calendering DEM)로 대체
  인용.  ★ **우리 MPM 미구현**(rate-independent J2, #285 한계).
- **Delamination:** 전극↔집전체 박리(Fig 6b anode; 본문 "potential delamination points of the CBD and the
  current collector could be predicted" ref 51).  ★ **우리 미모델**(bulk RVE만 — honest gap, #276 §3.3 동일).

---

## ★★★ 11. 우리 DEM+MPM positioning — 이 ACS EL이 PEER-REVIEWED 인용원 (이 디제스트의 핵심)

> ⚠ **대전제:** 이건 **동료심사 framework REVIEW, 정량 수치 앵커가 아니다.**  LPSCl σ/porosity 절대 앵커 =
> Bazzoun(`lit_bazzoun2026_dem_fem_rnm.md`)/Varkey(`lit_varkey2026_multicontact_dem.md`)/Minnmann/#266/#271.
> **이 논문에서 가져오는 단 하나 = peer-reviewed TAXONOMY(top-down/bottom-up · multi-scale · descriptor ·
> DTP/DTI) = 우리 POSITIONING의 정식 인용원.**  매거진(번호 없음·非동료심사) 대신 **이 ACS EL(vol 9, 5225-5239)을
> 인용**.

### (A) ★★ THE KEY — top-down/bottom-up이 곧 우리 positioning, 이젠 peer-reviewed

| `positioning_vs_geodict.md` 내 표현 | **이 ACS EL(Kim 2024, peer-reviewed)의 필드 어휘** | 매핑 |
|---|---|---|
| GeoDict = "구조를 줘야 함"(측정/CAD IN) | **Top-Down Method (reconstruction)** = "actual structural images ... followed by structural reconstruction" | **= 동일** |
| 우리 DEM+MPM = "압력·조성에서 구조 예측" | **Bottom-Up Method (formation)** = "design parameters → stochastic model"; 도구 = **DEM·FVM** "morphological changes under compression" | **= 동일**(우리는 process-physics 하위유형) |
| GeoDict 논문 #266/#271/#281/#284/#286/#275/#15/#16 | 전부 **top-down/reconstruction**(토모/CAD → GeoDict 특성화) | **= 분류 일치** |
| 우리 입력측 예측 + voxel FV + 접촉망 | **bottom-up/formation** + structure-resolved(GeoDict류) + (리뷰 미강조) granular constriction | superset |

→ ★★★ **positioning이 "내가 만든 구분" → "필드(이 그룹 자신의 동료심사 논문)의 taxonomy 안에서 우리 위치"로
격상, 그리고 인용이 peer-reviewed(ACS Energy Lett. 2024, 9, 5225-5239).**  논문 significance 인용 문안(예):

> **"Digital twin microstructure formation is categorized into top-down (reconstruction) and bottom-up
> (formation) methods, with the bottom-up method employing the discrete element method (DEM) and finite
> volume method (FVM) to model particle interactions and morphological changes under compression (Kim et al.,
> *ACS Energy Lett.* 2024, 9, 5225-5239).  Prior solid-state-cathode digital-twin studies (#266/#271/#281/
> #284/#286/#275) characterize measured or reconstructed structures with commercial GeoDict — a top-down/
> reconstruction route.  Our DEM+MPM forms the structure from design parameters (compaction pressure,
> composition, particle size) — a bottom-up/formation route, and specifically the process-physics-driven
> subtype that derives the structure from compaction mechanics (DEM hooke/hysteresis + MPM J2) rather than
> stochastic placement, providing the process→structure prediction that top-down methods cannot."**

### (B) ★★ 미세구조 descriptor 1:1 맵 (peer-reviewed 범례 기준)
- 매거진 디제스트 §11 (B)의 descriptor 1:1 표(AM crack→fracture / 도전재 connection→percolation / binder
  surface coverage→coverage / 전극 contact area·porosity·tortuosity→StageE·porosity·τ / dead particle→dead-SE)
  는 **그대로 유효**, 단 **electrode descriptor를 "percolation pathway"로 정렬**(영문 원본; "pore network"는
  separator 항목).  → **우리 출력이 동료심사 descriptor를 예측한다는 증명을 이젠 ACS EL 범례로 확정.**

### (C) ★ WHERE WE ADD VALUE — DESCRIPTIVE 리뷰 ↔ PREDICTIVE 엔진 + frame[5]
- **이 ACS EL = DESCRIPTIVE 방법론 survey**(top-down/bottom-up·다중물리·AI 분류·서술; 미세구조→성능 정성 연결).
  **압력→미세구조→σ를 수치로 예측하는 솔버는 아님.**
- **우리 DEM+MPM = PREDICTIVE 엔진:** **압력→미세구조→σ triad(ionic/electronic/thermal)**를 explicit 접촉망
  (Kirchhoff/Holm) + 소성 morphology(MPM J2 void-fill) + fracture(Auerbach)로 **정량·예측** + scaling law
  (LOOCV 0.975/0.953/0.90).
- ★ **우리 고유 edge(리뷰의 bottom-up DEM·FVM 서술이 강조 안 하는 것) = granular 점접촉 constriction σ:** 리뷰의
  bottom-up DEM·FVM은 **유효물성(volume-averaged, GeoDict류 ConductoDict)** 중심.  **우리는 거기에 더해
  Kirchhoff/Holm 접촉망으로 granular 점접촉의 constriction σ_ionic을 직접 잡는다**(연속체 voxel FV는 σ_contact-free
  상한만 — frame[5]).  ⇒ **우리 = bottom-up/formation(구조 예측) + structure-resolved(유효물성) + granular
  constriction(연속체 미포착)** 셋을 하나로.
- ★ **frame[5] 분업이 이 리뷰의 다중물리(Fig 5) + 동적 휠(Fig 6b)과 겹침:** 리뷰가 **transport descriptor**
  (Ion/Electron Pathway·tortuosity·connectivity·coverage = DEM) + **mechanics descriptor**(compression 변위·
  von Mises·volume expansion·crack = MPM)를 둘 다 핵심으로 명명 → "DEM=transport, MPM=mechanics" 분업이 필드
  인정 축임을 재확인(Varkey/Bazzoun이 frame[1]/[2]/[4]를, 이 리뷰가 frame[5]의 어휘·방법론 정당화 — #276과 동일 역할).

### (D) ★ honest GAPS — 리뷰가 강조하나 우리 미모델
1. **Top-down(reconstruction) 자체 — 우리는 안 함(설계 선택):** 우리는 **bottom-up 전용**(공정→구조 예측).  측정
   구조 재구성(XCT/FIB-SEM)은 우리 파이프라인 밖 → ⚠ 정직하게: 우리 bottom-up 구조 검증은 리뷰가 말한 "validated
   against experimental data"가 필요(우리는 #266/Minnmann porosity·Bazzoun/#271 σ로 검증; full 3D 토모
   one-to-one은 미수행).  → top-down은 우리가 "못 하는" 게 아니라 "안 하는"(GeoDict/토모 담당) — frame[5].
2. **입자 Orientation(Fig 4b) + AM coating:** 우리 구-입자 모델은 배향·코팅 미반영(등방 구, gap).
3. **Spring-back + 동적 거동(Fig 6b):** 우리 MPM = rate-independent J2 → 시간의존 spring-back 미구현(#285 한계);
   동적 균열전파/plating/delamination도 우리 정적 스냅샷 밖.
4. **Delamination / 집전체 계면(Fig 6b anode; ref 51):** 우리 bulk RVE만 → 박리·집전체 접착 미모델(#276 §3.3 gap).
5. **Fluid dynamics(Fig 5c LBM) / SEI(Fig 4e) / rock-salt:** 전해질 유동·SEI·화학 부반응은 우리 기계/transport
   모델 밖(ASSB는 SE 고체라 LBM 관련 낮음).

### (E) ★ ACTION items
1. **★ 최우선 — positioning 인용을 ACS EL로:** 논문 intro/significance에서 top-down/bottom-up을 **Kim et al.
   *ACS Energy Lett.* 2024, 9, 5225-5239(DOI 10.1021/acsenergylett.4c01931)** 인용으로 명시(매거진 대신).
   문안은 위 (A).  `positioning_vs_geodict.md`는 유저가 이미 이 ACS EL Ref 127을 인용하도록 갱신함(본 디제스트는
   근거·정확 서지 제공만 — positioning 파일은 건드리지 않음).
2. **multi-scale 위치:** Fig 1a electrode 스케일(10⁻⁴ m, DEM·FVM)에 우리 배치 → E softening을 본문 "intrinsic
   properties cannot be fully realized at the electrode scale"로 정당화(영문 원문 인용).
3. **descriptor 어휘 정렬:** Fig 1b 영문 범례(electrode=contact area·porosity·tortuosity·**percolation
   pathway**; binder=**surface coverage**; AM=**crack**)를 우리 metric 라벨로 정렬.
4. **DTP 자리매김:** 우리 DEM+MPM = **DTP(early-design-stage)**로 명명; Phase 4(PyBaMM)·Phase 5(layered)가 cell
   스케일로 확장하는 경로.
5. **ref-그래프 연결:** 이 논문 ref 32/34/35/51/33/36(= 우리 #266/#271/#262 계열의 동료심사 좌표)으로 우리 작업을
   이 그룹 논문군에 정확히 연결.
6. **매거진·#276 교차인용:** 매거진(`lit_choi2024_digital_twin_review_echem.md`) = 한국어판(positioning 직관),
   이 ACS EL = peer-reviewed 인용원; **#276(Nam 2026 DPE 공정 taxonomy, calendering=압축) = 공정 축** →
   "공정(#276) × 방법론(이 ACS EL bottom-up) 교차점에 우리 작업."

### 비교 요약표

| 축 | 이 ACS EL (Kim 2024, peer-reviewed) | 우리 (LPSCl ASSB DEM+MPM) | 이식/교훈 |
|---|---|---|---|
| 성격 | **DESCRIPTIVE 방법론 REVIEW(peer-reviewed)** | **PREDICTIVE**(압력→미세구조→σ) | ★ 우리 = framework의 정량 엔진 |
| **구조 형성 분류** | ★ **top-down(reconstruction) vs bottom-up(formation)** §명시 | ★ **bottom-up/formation**(process-physics 하위유형) | ★★ **positioning의 peer-reviewed NAMING** |
| multi-scale | atom→pack(electrode=DEM·FVM) | electrode 스케일(DEM+MPM) | E softening 정당화("cannot be fully realized") |
| descriptor | Fig 1b 영문 범례(crack/coverage/τ/percolation pathway) | 우리 출력 1:1 | 영문 descriptor 어휘 정렬 |
| 다중물리 | 전기화학+기계+열(Fig 5; von Mises·압축 변위) | σ triad(DEM) + 응력장(MPM) | frame[5] 정당화 |
| AI surrogate | upscaling(coverage→성능, ref 110) | scaling law(LOOCV 0.975/0.953/0.90) | = 같은 개념 |
| 동적 시뮬 | Fig 6b 휠(crack/contact/volume vs delamination/plating) | 우리 하는 것 + honest gap | frame[5] 분업 |
| top-down 재구성 | ★ 한 축 | (안 함 — bottom-up 전용) | frame[5] 분업(GeoDict/토모 담당) |
| 우리 고유 | (없음 — 방법론 리뷰) | granular constriction σ + 소성 morphology + fracture 예측 | 그들엔 정량·예측 솔버 없음 |
| 인용 안전성 | ★ **peer-reviewed(ACS EL 9, 5225-5239)** | — | ★ **매거진 대신 이걸 인용** |

---

## ★ 12. 우리 작업에 넣을 가장 날카로운 인사이트 3가지

1) **★ top-down/bottom-up이 우리 positioning을 NAMING하고, 이젠 peer-reviewed로 인용 가능(ACS EL 9, 5225-5239).**
   `positioning_vs_geodict.md`의 "GeoDict=구조-given 특성화 / 우리=공정→구조 예측"이 — 이 동료심사 논문의 **§
   "STRUCTURE FORMATION METHODOLOGIES"의 Top-Down(reconstruction) / Bottom-Up(formation)** 분류와 정확히
   동일하고, **본문이 bottom-up 도구로 DEM·FVM을 명시**("morphological changes under compression").  ⇒
   positioning이 "내가 만든 구분"에서 **"필드(우리가 비교하는 바로 그 이용민 DTBL 그룹)의 동료심사 taxonomy 안에서
   우리 위치"로 격상** — significance에 매거진이 아니라 이 ACS EL을 인용(reviewer-safe).  단 정직하게: 우리
   bottom-up은 리뷰의 "stochastic model"보다 한 단계 더 — **압축역학(DEM/MPM)으로 구조를 형성하는 process-
   physics-driven 하위유형**(압력→구조 인과)으로 구체화하면 정확.

2) **매거진 대비 더 RIGOROUS한 인용 자산 4가지 — 영문 §명·정의 문구·descriptor 정밀화·118 ref.**  동료심사 원본은
   (a) 명시 영문 §/소절명("STRUCTURE FORMATION METHODOLOGIES / Top-Down / Bottom-Up", AI §의 번호 소절 1/2/3),
   (b) 인용 직결 가능한 정의 문장("actual structural images ... structural reconstruction" / "design parameters
   ... stochastic model ... validated against experimental data" / "DEM and FVM ... morphological changes
   under compression" / "intrinsic properties ... cannot be fully realized at the electrode scale"), (c)
   descriptor 범례 정밀화(electrode="percolation pathway", pore network=separator — 매거진 의역 교정), (d) 우리
   그룹-논문(#266/#271/#262)의 동료심사 좌표(ref 32/34/35/51/33/36)를 준다.  ⇒ **매거진 디제스트의 한국어 인용을
   이 영문 원문·§명·ref로 업그레이드** = reviewer가 원문 대조 가능한 rigor.

3) **frame[5] + E softening + honest gap이 이 동료심사 본문에 명시된다.**  (a) frame[5] 분업 = Fig 5 다중물리
   (transport descriptor=DEM ↔ 압축/von Mises=MPM) + Fig 6b 동적 휠(crack/contact/volume=우리 ↔ delamination/
   plating=gap); (b) E softening = "intrinsic properties cannot be fully realized at the electrode scale"
   (영문 동료심사 근거); (c) honest gap(orientation/coating/spring-back/delamination/SEI/LBM)이 Fig 4b·6b로
   필드 레벨 명명.  ★ 단 **spring-back/압연 공정모델은 ACS EL Fig엔 별도 패널 없음**(매거진 Fig 6c) → 본문
   ref 50,104 + Fig 5a(calendered)로 인용(동료심사 안전).

### 보너스 실행 항목
- **literature_yonsei_dtbl_2026.md 갱신(완료):** 보충/FRAMEWORK §에 **"(보충) Kim 2024 ACS Energy Letters
  (digital-twin taxonomy의 PEER-REVIEWED source = Ref 127)"** 추가, 매거진 항목 + `positioning_vs_geodict.md`
  교차링크.
- ⚠ **혼동 금지:** 이 ACS EL = **peer-reviewed framework/taxonomy/positioning** 공급원 — **수치 앵커 아님.**
  LPSCl σ/porosity 앵커는 Bazzoun/Varkey/Minnmann/#266/#271; z-구배 #286; CBD trade-off #284; spring-back #285.
- ⚠ **매거진과 역할 분담:** 매거진(`lit_choi2024_digital_twin_review_echem.md`) = 한국어 본문·우리-출력 1:1 표
  (positioning 직관·작업 메모); 이 ACS EL = **동료심사 인용원**(논문에 들어가는 citation).  중복 디제스트 회피 —
  매거진의 상세 본문 인용은 거기서, 정확 서지·영문 §·매거진 대비 차이는 여기서.
