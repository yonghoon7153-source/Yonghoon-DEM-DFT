# Mechanical instability of electrode-electrolyte interfaces in solid-state batteries — Bucci, Talamini, Renuka Balakrishna, Chiang, Carter (Phys. Rev. Materials 2018)

> slug `bucci2018_mechanical_instability_interface_delamination` · DOI `10.1103/PhysRevMaterials.2.105407` · type `continuum (1D radially-symmetric analytical, cohesive-zone fracture) + random-walk FPT transport` · PDF `Bucci_2018_PRM_MechanicalInstability_ElectrodeElectrolyteInterface.pdf` · digested `2026-06-26` · status ✅ · WISHLIST #22 (fracture/interface / frame[5])
>
> ⚠ **소재 한정**: 이 논문은 **소재-무관 *해석 모델*** (LPSCl도 NMC811도 *지정 안 함*) — E_SE 20–200 GPa **파라미터 스윕**으로 모든 무기 SE 를 포괄.  우리 LPSCl(E≈22–24)·NMC811은 그 스윕의 *한 점*으로만 매핑.  porosity·σ·Heckel·PSD·coordination = **전부 n/a** (압밀 논문 아님 — 사이클-구동 *계면 박리* 역학 논문).  정량 앵커는 **부피변화 임계(7.5 %/25 %) · E_SE<25 GPa compliant 기준 · 임계입자반경 50–500 nm · σ_yield<0.5·F_c · 박리→ASR(FPT) 비**.

---

## 1. 한 줄 요약 (TL;DR)
**Cohesive 파괴이론에 기반한 1D 방사대칭 *해석* 모델** — 구형 AM 입자가 SE 껍질에 박혀 있는 단위 셀에서, **충방전 중 AM 부피변화(de/intercalation)가 만드는 변위-제어 하중**이 AM↔SE 계면을 **박리(delamination)** 시키는 *임계조건*과 *안정조건*을 유도한다.  핵심 결론: **대부분의 인터칼레이션 화합물은 반경 ~2.5 %(부피 ~7.5 %)만 변해도 박리가 *시작*** 되며, **compliant(무른) SE (E < 25 GPa) + 큰 계면 cohesive 에너지(γ > 5 J/m²)** 라야 부피변화 25 %까지 박리를 *지연*시킨다.  파괴의 *안정/불안정(ductile/brittle)* 은 **damage-zone 크기 대 입자반경 비**로 갈리고(임계반경 50–500 nm), **고전도 SE 일수록 박리가 총 충방전 시간을 *크게* 늘린다**(FPT random-walk).  → 우리 frame[5]에서 ***사이클 중* AM-SE 계면 decohesion** 이라는, 우리가 *압밀-시점 접촉만* 다루느라 **비워둔 시간축**을 채우는 해석 레퍼런스.

이 논문이 우리에게 주는 정확한 자리: 우리 **Stage-E(Tabor) 가 *압밀 순간* 계산하는 그 AM-SE 접촉면적**이, **사이클이 돌면 박리로 *깎이고*, 그 면적 손실이 곧 ASR(면적비 임피던스) 증가**라는 *time-axis* 인과를 해석식으로 준다 (우리 backlog **B6 time-axis** 의 문헌 근거).

---

## 2. 메타
| 항목 | 값 |
|---|---|
| 저자 | **Giovanna Bucci**¹·², **Brandon Talamini**³·(now Sandia), **Ananya Renuka Balakrishna**¹, **Yet-Ming Chiang**¹, **W. Craig Carter**¹ |
| 소속 | ¹ **MIT** Dept. Materials Science & Engineering · ² **Robert Bosch LLC**, Research and Technology Center, Sunnyvale CA · ³ **MIT** Dept. Mechanical Engineering (now **Sandia National Laboratories**, Livermore CA) |
| 교신 | **bucci@mit.edu** (Giovanna Bucci) |
| 저널/년 | **Physical Review Materials 2, 105407 (2018)** (Received 2018-07-05, revised 2018-09-10, published 2018-10-30) |
| DOI | **10.1103/PhysRevMaterials.2.105407** |
| Funding | **DOE Office of Science Grant DE-SC0002633** |
| 소재 (SE/CAM) | ⚠ **소재-무관 해석 모델** — SE: **E_se 20–200 GPa 스윕**(무기 ceramic/polymer SE 일반), ν 0.10–0.45; CAM: 일반 "polycrystalline intercalation compound", 부피변화 0–25 % 스윕 (양극 delithiation 시 *수축*) |
| 연구유형 | **해석(analytical) 1D 방사대칭 cohesive-zone 모델** (Del Piero 변분 파괴이론 기반) + **random-walk first-passage-time** 박리→ASR 추정.  ⚠ **DEM 없음, MPM 없음, FEM 없음** (닫힌형 해석 + 몬테카를로 random walk) |

---

## 3. 핵심 물성 / 정량 결과 (수치)

> ★ 모든 값은 **본문 stated**(식·수치) 또는 **Fig contour digitized**(TREND only)로 구분 표기.  이 논문은 단일 소재의 측정값이 아니라 *파라미터 스윕의 임계선*을 준다 → "값"이 아니라 "**임계조건**"이 앵커.

### 3.1 ★★ 박리 임계 — 부피변화 (이 논문의 대표 숫자)
| 항목 | 값 | 조건 | src | 비고 |
|---|---|---|---|---|
| **박리 개시 반경변화 (전형)** | **~2.5 %** (반경) | E_se·γ_am-se 대부분 조합, ‖u‖_R=1 nm | stated | = 우리가 인용할 대표 숫자 |
| **박리 개시 부피변화 (전형)** | **~7.5 %** (부피) | 위와 동일 (반경 2.5 % ⇒ 부피 ≈3×2.5) | stated (abstract+§II) | "encompasses many intercalation compounds" |
| **박리 지연 한계 (compliant SE)** | **25 %** (부피)까지 수용 | **E_se < 25 GPa** AND **γ_am-se > 5 J/m²** | stated (Fig 3a) | compliant + 큰 cohesive E 라야 |
| Fig 3a contour 수준 | 7.5 % / 15 % / 25 % / 50 % 부피수축 등고선 | E_se 20–200 GPa × γ 1–10 J/m² | digitized | 무를수록·γ 클수록 더 큰 변화 견딤 |

### 3.2 ★ 안정/불안정(ductile/brittle) 기하 임계 — 입자반경 vs damage-zone
| 항목 | 값 | 조건 | src | 비고 |
|---|---|---|---|---|
| **임계 입자반경 A_critical** | **~50–500 nm** (예측 bound) | cohesive length ‖u‖_R ~1 nm, ν up to 0.3 | stated (§Stability) | 이보다 작으면 안정-쪽으로 |
| **cohesive length ‖u‖_R (균열공정영역 크기)** | **~1 nm** (대표; 클수록 안정) | linear traction-separation | stated (Fig 3a 고정값) | rough 계면 → ‖u‖_R↑ → 더 안정 |
| **interfacial fracture energy γ_am-se** | **1–10 J/m²** (스윕) | Fig 3a 가로축 | stated | sulfide SE 알려진 값 계열(yun2023 G_c 2.93) |
| **adhesive strength F_c** | **2–20 GPa** (‖u‖_R=1 nm 일 때 역산) | γ=1–10, ‖u‖=1 nm | stated | F_c = 2γ/‖u‖_R |
| **소성-억제(no-delamination) 설계 기준** | **σ_yield < 0.5·F_c** | elasto-plastic SE, ν·φ_AM 약의존 | stated (Eq 14, Fig 7) | "rule of thumb" — 항복강도가 접착강도 절반보다 작으면 소성이 박리를 막음 |

### 3.3 ★ 박리 → ASR(면적비 임피던스) — random-walk FPT
| 항목 | 값 | 조건 | src | 비고 |
|---|---|---|---|---|
| **평균 FPT 증가 (연속 박리 50 %)** | **×2.75** (mean FPT) | contiguous(연속) 박리 patch, 50 % 면적 | stated (Fig 8) | "연속" 박리가 최악 |
| **FPT 표준편차 증가** | **×5** (std dev) | contiguous 50 % | stated (Fig 8) | 불균일 Li 분포 시사 |
| **불연속(discontinuous) 박리 효과** | **훨씬 작음** (mean·std 둘 다) | 같은 50 % 면적이라도 patch 가 흩어지면 | stated (Fig 8a,b) | ★ 면적뿐 아니라 *연결성*이 중요 |
| **총 충방전시간 영향 (고전도 SE)** | t_P 2배 → 셀 시간 2t_P→3t_P (**+150 %**의 t_P 기여) | d_particle = (1/10)·d_electrode, Li mobility SE 10× | stated (worked example) | **t_P≫t_S 면 박리가 율속** |
| **총 충방전시간 영향 (저전도 SE)** | **작음** | t_S ≫ t_P (SE 가 율속) | stated | 저전도 SE 면 박리 영향 미미 |

### 3.4 SE 응력장 (Fig 6, 부피수축 중 SE 껍질)
| 항목 | 값 | 조건 | src |
|---|---|---|---|
| 방사응력 σ_RR (내경, ν=0.15) | **~+4 GPa** (인장) → 외경서 감쇠 | E_se=50 GPa, φ_AM=0.55, full charge | digitized (Fig 6a) |
| hoop 응력 σ_θθ (ν=0.15) | 계면서 **압축**, 두께 따라 부호변화 | 동일 | digitized (Fig 6a) |
| von Mises σ (ν=0.15) | **~−4 GPa → −2 GPa** (스칼라 음부호 표기) | 동일 | digitized (Fig 6a) |
| ν=0.35 일 때 | hoop 이 *인장*으로 바뀜, Mises 절대값 약간↓ | E_se=50, φ_AM=0.55 | digitized (Fig 6b) |
> ★ 응력 *수 GPa* = Kang2025/yun2023 의 "확산-유발 응력 최대 GPa ≫ 가압 수백 MPa"와 같은 계열 — **사이클 응력이 압밀 응력보다 훨씬 큼**.

### 3.5 기하인자 f = R_B/R_A (Fig 1 우측)
| φ_AM (AM vol%) | f = R_B/R_A | src |
|---|---|---|
| 30 % | ~1.70 | digitized (Fig 1) |
| 50 % | ~1.45 | digitized (Fig 1) |
| 70 % | ~1.28 | digitized (Fig 1) |
> f(φ_AM) = (1/φ_AM)^(1/3) 계열 (space-filling truncated-octahedron 단위셀); 상용 셀 전형 φ_AM 50–60 %.

### 3.6 미측정/n/a (우리 압밀·전달 앵커와 직접대조 금지)
| 항목 | 상태 |
|---|---|
| porosity / 상대밀도 / Heckel / P_y / coordination Z | **n/a** (압밀 논문 아님) |
| σ_ionic / σ_e / σ_thermal 절대값 (mS/cm) | **n/a** (FPT *비*만 — random-walk로 *상대* ASR) |
| coverage % / 접촉면적 (정량) | **n/a** (계면을 *연속체 cohesive 면*으로 — 입자별 접촉면적 없음) |
| PSD (D10/D50/D90) | **n/a** (단일 대표입자 + 반경 스윕) |
| LPSCl·NMC811 *지정* 물성 | **n/a** (소재-무관 스윕; E_se 20–200 의 한 점으로만) |

---

## 4. 모델 ★ — 1D 방사대칭 cohesive-zone 박리 해석 (모든 수식)

> ★ **방법 핵심**: 미세구조를 **공간충전 truncated-octahedron 집합**으로 이상화(Fig 1) → 단위셀 = **구형 AM 입자 + 그를 감싸는 구형 SE 껍질**(내경 R_A, 외경 R_B) → **1D 방사대칭**으로 환원.  AM 입자는 *명시적으로 모델 안 함* — 그 반경변화를 **계면 안쪽에 *부과된 변위* u(R_A)=αc·R_A** 로 대체 (변위-제어 파괴시험).  SE 껍질 = **선형탄성(또는 elasto-plastic)**, 계면 = **cohesive traction-separation 법칙**.  ⇒ **변위-제어 1D 균열문제**로 닫힌형 풀이.

### 4.1 경계조건 + 탄성해 (Eqs 1–6)
- **AM 반경변화 = Vegard 변형**: AM 반경은 SOC c 의 함수로 strain-free R_A 에서 변함.  반경변화 ∝ **Vegard 파라미터 α** (Li 수용에 따른 격자 strain).  계면 안쪽에 부과되는 전 변위:
  ```
  u(R_A) = α c R_A          (충전 시 양극 delithiation → AM 수축 → 음의 변위)   ... Eq (1) BC
  u(R_B) = 0                (외경 고정 = 인접 입자가 받쳐줌)
  ```
- **부과변위의 분해**: 전 변위 u 는 (i) SE 껍질의 *탄성 stretching* u(R) + (ii) 계면의 *비가역 열림* ‖u‖(변위점프, displacement jump)로 나뉜다.  파괴 *전*엔 ‖u‖=0, SE 변형만.
- **중공 구 탄성 일반해** (구대칭):
  ```
  u(R) = C₁ R + c₂ / R²                                                        ... Eq (2)
  ```
- BC (Eq 1) 적용 →
  ```
  u(R) = [R_A³ α c / (R_A³ − R_B³)] · (R − R_B³/R²)                            ... Eq (3)
  ```
- **외경 R_B = f·R_A** (f = 기하 scaling factor, φ_AM 의 함수, Fig 1):
  ```
  u(R) = α c (R_A³ f³ − R³) / [(f³−1) R²]                                       ... Eq (4)
  ```
- **방사·hoop 변형**: ε_RR=∂u/∂R, ε_θθ=u/R.  **응력**(λ=1st Lamé, ν=Poisson):
  ```
  σ_RR(R) = (λ/ν)[(1−ν)ε_RR + 2ν ε_θθ]
          = α c λ [2 R_A³ f³ (2ν−1) − (ν+1) R³] / [(f³−1) ν R³]                ... Eq (5)
  σ_θθ(R) = (λ/ν)(ν ε_RR + ε_θθ)
          = −α c λ [R_A³ f³ (2ν−1) + (ν+1) R³] / [(f³−1) ν R³]                 ... Eq (6)
  ```
  (Eq 5/6 는 E·ν 로도 표기 가능: λ = Eν/[(1−2ν)(1+ν)].)

### 4.2 ★ 박리 *개시* 임계 (Criterion for delamination, Eqs 7–10)
- **총 에너지 = 탄성(벌크) + cohesive(계면 단위면적당)**:
  ```
  E(u, ‖u‖) = ∫_{R_A}^{R_B} k_el (u'(R))² dR  +  G(‖u‖)                          ... Eq (7)
  ```
  (1항=SE 껍질 탄성에너지(강성 k_el·방사변형²), 2항=cohesive 에너지.)
- **cohesive 에너지 (이차형 traction-separation)**:
  ```
  G(‖u‖) = F_c ( ‖u‖ − F_c/(4 γ_am-se) (‖u‖)² )                                 ... Eq (8)
  ```
  두 핵심 파라미터: **γ_am-se = interfacial energy release rate** (=lim G at ‖u‖→‖u‖_R, 임계열림서 방출되는 계면에너지) + **F_c = adhesive strength**(접착강도, first-principles로 계산 가능, ref Hong/Qi).
- **선형 traction-separation 법칙** G'(‖u‖) (Fig 2 의 감쇠직선):
  ```
  G'(‖u‖)|_R = F_c ( 1 − F_c/(2γ_am-se) (‖u‖)|_R ) = 0
  ⇒ 임계열림 ‖u‖_R = 2 γ_am-se / F_c                                            ... Eq (9)
  ```
  (계면이 완전 박리되는 임계 열림 = cohesive length.)
- **박리 핵생성 = 계면 응력이 접착강도 도달**: σ_RR(A)=F_c.  Eq 5 로부터 박리 유발 *인터칼레이션 strain* (αc):
  ```
  (αc)_fracture = − F_c (f³−1) ν / [λ (f³(4ν−2) − ν − 1)]                        ... Eq (10)
  ```
  ⇒ **박리 개시 strain 은 (i) SE 탄성물성(λ,ν), (ii) 계면 접착강도 F_c, (iii) AM 부피분율(f) 의 함수**.  → **Fig 3a contour** (E_se × γ_am-se → 임계 부피수축 %): 대부분 조합서 **2.5 % 반경(7.5 % 부피)**, **compliant(E<25)+큰 γ(>5)** 만 25 %.
  - ★ "fracture cannot be alleviated by simply choosing a smaller particle size" — **Eq 10 에 입자크기 없음** → 박리 *개시*는 입자크기 *무관*.

### 4.3 ★ 파괴 *안정성* (ductile vs brittle, Eqs 11–12) + 임계반경
- 박리 핵생성 후, 계면은 **혼합 Robin BC**(force balance σ_RR=F_c + compatibility u+‖u‖=αcR_A 동시)로 진화.  **u(R_A) vs ‖u‖ 평면**(Fig 4)에서:
  - **빨강 평형곡선(equilibrium)**: SE 방사력 = cohesive traction; 기울기 = 전변위의 벌크↔계면 분배 = SE·계면 *상대강성*으로 결정(음의 기울기).
  - **검정 적합곡선(compatible loading)**: u(R_A)+‖u‖=αcR_A; SOC 증가로 위로 평행이동.
  - **안정(ductile, Fig 4b)**: 적합곡선 기울기 < 평형곡선 기울기 → 매 SOC 마다 교차 → **균열이 *점진적으로* 열림**(gradual).
  - **불안정(brittle, Fig 4a)**: 적합곡선이 더 가팔라 kinking point 너머서 교차 *없음* → **coherent→fully-debonded *급격 비평형 전이***(snap).
- **임계 입자반경 A_critical** (안정↔불안정 경계; 에너지함수 Eq 7 의 minimizer 조건):
  ```
  A_critical = λ[f³(2+4ν)+ν+1] / [(f³−1)ν] · ‖u‖_R/F_c
             = E[f³(2+4ν)+ν+1] / [(f³−1)(1−2ν)(ν+1)] · ‖u‖_R/F_c                ... Eq (11)
  ```
  **무차원형**:
  ```
  A_critical/‖u‖_R = (E/F_c) · [f³(2−4ν)+ν+1] / [(f³−1)(1−2ν)(ν+1)]              ... Eq (12)
  ```
  - 좌변 = **임계입자반경 / 임계열림**(미세구조 길이 / 균열공정영역 길이).  우변 = **E/F_c**(SE 영률 / 접착강도) × ν·φ_AM 함수.
  - ★ **Fig 5** (A_critical/‖u‖_R 등고선): 안정조건 = **큰 E_se(뻣뻣) + 작은 γ(낮은 계면파괴에너지) + 큰 cohesive length ‖u‖_R**.  ⇒ ‖u‖_R~1 nm 이면 **임계반경 50–500 nm**.
  - ★ **모순적 설계 긴장 (이 논문의 미묘점)**: *핵생성 방지*엔 **compliant(무른) SE** 가 좋다(Eq 10, 4.2) — *그러나* 일단 핵생성하면 무른 SE 에선 *전파가 불안정*(Eq 11/12) → **nanostructured AM(50–500 nm)** 과 결합해야 더 넓은 SE 물성 사용 가능.

### 4.4 ★ 소성으로 박리 *방지* (elasto-plastic SE, Eqs 13–14, Fig 2 하단·Fig 7)
- SE 가 **소성으로 흐르면** dislocation 발달이 계면 응력을 *완화* → 접착강도 도달 *전*에 막음 (Fig 2 하단: "elasto-plastic → no fracture").
- 항복(von Mises≡Tresca, 구대칭서 σ_θθ−σ_RR=σ_yield):
  ```
  (αc)_plastic = − (f³−1) ν σ_yield / [3 f³ λ (2ν−1)]                            ... Eq (13)
  ```
- **소성-우선 조건** |(αc)_plastic| < |(αc)_fracture| (Eq 13 vs Eq 10):
  ```
  (σ_yield/F_c)(f³(2−4ν)+ν+1) / [3 f³ (1−2ν)] < 1                                ... Eq (14)
  ```
  - ★ **Fig 7** (σ_yield/F_c × ν 평면, φ_AM 0.4–0.7 등고선 4개): 회색=소성흐름(박리 방지), 흰색=취성.  **모든 실용 조합서 σ_yield < 0.5·F_c 면 박리 방지** → **"rule of thumb": 항복강도가 접착강도의 절반보다 작은 ductile SE 가 bulk-type 배터리에 유리.**
  - Eq 14 는 입자크기·E_se 무관, F_c·ν·σ_yield 에 강의존.

### 4.5 ★ 박리 → 면적비 임피던스 (ASR) — random-walk FPT (Fig 8)
- **박리 = AM 입자의 Li-전도 접촉면적 감소** → Li 인터칼레이션·디인터칼레이션 시간 ↑ → **유효 ASR ↑**.  이를 **random-walk first-passage-time(FPT)** 으로 추정.
- **방법**: AM 입자 표면을 **2160 삼각형**으로 이산화; 박리부 = **반사경계(reflective)**.  **1000 random walker** 가 중심서 출발, step=반경의 1 %, 무작위방향; 박리부에 부딪히면 step 기각; **온전한 표면 통과까지의 step 수 = FPT**.
- **두 경계조건**: (a) **contiguous(연속)** 박리 patch (불안정/brittle 계열) vs (b) **discontinuous(불연속, 흩어진)** patch (안정/ductile 계열) → FPT 의 하한·상한 bound.
- **결과 (Fig 8a,b)**: 박리면적 0→50 % 스윕 →
  - **연속 박리 50 %**: 평균 FPT **×2.75**, std **×5** (노란 마커).
  - **불연속 박리 50 %**: 효과 *훨씬 작음* (파란 마커).
  - ⇒ ★ **계면 kinetics 는 *접촉면적*뿐 아니라 그 *연결성(connectivity)* 에 의존** — rough/흩어진 박리는 평균저항을 낮게 유지 (안정계면 설계의 transport 이득).
- **셀 시간축 (Fig 8c)**: 두 시간척도 — t_P(입자 탈리시간) + t_S(separator 도달시간).  입자가 전극두께의 1/10, SE Li-mobility 10× 면 t_P=t_S → 박리로 t_P 2배 → 셀 시간 **2t_P→3t_P (+150 % of t_P 기여)**.  **고전도 SE(t_P≫t_S)** 면 박리가 *율속*; **저전도 SE(t_S≫t_P)** 면 박리영향 *미미*.

### 4.6 입자 처리 ★ (DEM판 "무질서 처리" 관점에서)
- **AM 입자**: *명시적으로 모델 안 함* — 단일 대표 구의 **반경변화를 부과변위 u=αcR_A 로 추상화** (개별 입자 형상·PSD·접촉망 *전부 없음*).  → 우리 DEM 의 *명시적 다입자 접촉망*과 정반대 추상화 레벨 (1-particle 단위셀).
- **SE 껍질**: **연속체** — 선형탄성(Eqs 1–12) 또는 **elasto-plastic(J2/Tresca, Eqs 13–14)**.  ★ **이 소성 = 우리 MPM J2 와 *같은 계열*** (von Mises≡Tresca 구대칭) — *단* 여기선 *박리를 막는 응력완화* 용도, 우리 MPM 은 *void-fill 형상흐름* 용도.
- **계면**: **cohesive traction-separation 면**(연속체 박리) — 입자별 접촉면적이 아니라 *연속 계면*이 ‖u‖ 만큼 열림.  → 우리 Stage-E 의 *입자별 Tabor 접촉면적*과 추상화가 다름 (그들=연속 면 cohesive, 우리=이산 접촉 area).
- ⇒ ★ **rigid/CONTACT-소성/SHAPE-소성 분류 밖**: 이 논문은 입자를 *안 깬다*(SE 형상 안 변함), 대신 **계면을 *벌린다*(cohesive decohesion)** — **우리 DEM(구·접촉)·MPM(소성형상) 둘 다에 *없는* 4번째 메커니즘 = 계면 박리**.

---

## 5. 결과 상세 — section-by-section (모든 수치·논리)

### 5.1 §I 서론 — 문제 설정
- ASSB 의 율속이 *계면*에 있음(bulk σ 좋아도 rate 나쁨, refs 1,5,6).  **SE-탄소 매트릭스에 박힌 다결정 AM 의 사이클 부피변화(양극 delithiation 시 *수축*, ref 21,22) → de-bonding → 셀 임피던스 증가 + (입자 완전고립 시) 용량감소.**
- 두 설계전략의 trade-off: (1) **SE scaffold 에 AM 채움** = 변형 수용하나 *접촉면적↓*; (2) **저공극 가압/소결 복합** = 내부저항↓이나 *역학열화 취약*.  → "어느 (E_se, F_c, γ) 조합서 박리하나?" 가 질문.
- 파괴양식 분류 예고: 일부 조합 = **brittle(급격)**, 일부 = **ductile(연속)**; 더 복잡한 경쟁(벌크/SE 분해→신상, refs 23–25)은 *향후과제*.

### 5.2 §II 모델 유도
- §4.1–4.4 의 식 전개.  핵심 가정(stated): **sharp interface**, 계면 toughness < 두 인접물질 toughness(계면이 약한 고리), **chemical expansion isotropic + Li 함량의 linear 함수**(Vegard), **bulk·interface 구성거동 rate-independent**(∴ 해가 *충전율 무관*).
- ★ **각주1**: 이 불안정성은 **박막 코팅 buckling 과 *다른* 현상** — 두 인접물질 두께가 비슷(껍질 vs 입자).  → 박막 delamination 문헌(refs 27–32)과 *공유 물리*(구조크기 vs cohesive length 비)이나 좌굴은 아님.

### 5.3 §II Criterion for delamination (Fig 3)
- §4.2.  **Fig 3a** = E_se(20–200) × γ_am-se(1–10 J/m²) → 임계 부피수축 등고선 (7.5/15/25/50 %).  ‖u‖_R=1 nm 고정 → F_c=2–20 GPa.
- **Fig 3b** = 무차원화: 세로 = 인터칼레이션 strain / cohesive length, 가로 = **cohesive over bulk stiffness 2γ/‖u‖_R·E** (ν=0.25, φ=0.55) → **선형관계** (주어진 γ 서 F_c 는 ‖u‖_R 와 함께 감쇠).
- ★ 결론문: "**particle delamination is a likely event** in solid-state-electrode microstructures; fracture **cannot be alleviated by simply choosing a smaller particle size**" (개시는 크기무관).

### 5.4 §II Stability of fracture (Figs 4,5)
- §4.3.  **Fig 4** = u(R_A) vs ‖u‖ 평면; (a) 불안정(교차없음, snap) vs (b) 안정(교차, gradual).  **Fig 5** = A_critical/‖u‖_R 등고선 (E/F_c × ν, φ_AM).
- 결론: **안정 = 큰 E_se + 낮은 γ + 큰 ‖u‖_R(rough 계면)**; 나노입자(50–500 nm)는 안정쪽이나 *핵생성 자체는 못 막음*.  **densely-packed 미세구조 + 큰 damage-zone = 안정 선호**.  ⚠ 단 dense-pack 은 *tortuous diminishing pore* 로 이온수송 제약 — **역학안정 ↔ 이온수송 trade-off** 명시.

### 5.5 §II.A Exploit electrolyte ductility (Fig 7) + 응력장 (Fig 6)
- §4.4.  **Fig 6** = SE 껍질 응력장(σ_RR/σ_θθ/Mises vs R/R_A; ν=0.15 vs 0.35; E_se=50, φ_AM=0.55).  방사 ~수 GPa 인장, hoop 부호변화, Mises 압축.  **Fig 7** = σ_yield/F_c × ν, 소성흐름(회색)/취성(흰색) 경계, φ_AM 0.4–0.7.
- 결론: **σ_yield < 0.5·F_c 인 ductile SE 가 박리 방지** → "ceramic/polymer SE 를 *ductile* 하게 engineering 하면 좋다" (우리 frame[2] "LPSCl 소성으로 압밀" 과 결이 같으나 *여기선 사이클-박리 방지* 목적).

### 5.6 §II.A Effect on area-specific impedance (Fig 8)
- §4.5.  random-walk FPT.  연속 50 % → mean ×2.75/std ×5; 불연속 ≪.  셀 시간 2t_P→3t_P(고전도 SE).  → **"고전도 SE 쓸수록 박리가 셀 power 를 *더* 깎는다"** (역설: 좋은 SE 가 박리에 더 민감).

### 5.7 §III 결론 (저자 요약)
1. 고려한 탄성물성·계면 toughness·팽창계수 범위서 **양극 입자는 박리하기 쉽다** — 대부분서 반경 2.5 %(부피 7.5 %)면 개시.
2. **compliant SE + 큰 cohesive E** 면 25 % 부피변화까지 견딤.
3. **박리 개시는 입자크기 무관**; 핵생성 후 *전파*의 안정/불안정은 **벌크/계면 상대강성**에 의존.
4. 안정 = **큰 E_se + 낮은 γ + 큰 damage-zone**; nanostructured AM(<~100 nm 계열)과 결합 시 더 넓은 SE 물성 사용.
5. **소성 SE(σ_yield<0.5F_c)가 박리 방지** — ductile SE 가 유리.
6. **고전도 SE 면 박리가 power density 율속**; 두 시간척도(t_P 입자·t_S separator) 중 큰 쪽이 충방전능력 결정.

---

## 6. Figure set ★ (모든 그림 + 우리가 쓸 점)
| Fig | 내용 (무엇을 보여주나) | 핵심 수치 | 우리가 참고할 점 |
|---|---|---|---|
| **1 (좌)** | 미세구조 이상화 = space-filling truncated-octahedron 단위셀 (AM 입자 + SE 껍질 R_A/R_B) | φ_AM 50–60 % 전형 | 우리 RVE 의 *해석적* 단위셀 대응 |
| **1 (우)** | 기하인자 f=R_B/R_A vs φ_AM | 30 %→1.70, 50 %→1.45, 70 %→1.28 | f(φ_AM)=(1/φ_AM)^⅓; 우리 φ_AM↔껍질두께 |
| **2** | 1D 모델 모식: SE=탄성스프링, 계면=cohesive traction-separation; 탄성(파괴) vs 탄소성(무파괴) | — | ★ 박리 vs 소성-억제 두 시나리오 한 그림 |
| **3a** | E_se × γ_am-se → 임계 부피수축 등고선 (7.5/15/25/50 %) | **7.5 % 전형, 25 % @ E<25·γ>5** | ★★ **대표 숫자** + compliant 기준 |
| **3b** | 무차원화 (intercalation strain/‖u‖ vs cohesive/bulk stiffness) | ν=0.25, φ=0.55, 선형 | cohesive length 일반화 |
| **4a,b** | u(R_A) vs ‖u‖ 평면: (a) 불안정(snap) vs (b) 안정(gradual) | 평형·적합곡선 기울기 비교 | ★ 안정/불안정 판별 기하 |
| **5a,b** | A_critical/‖u‖_R 등고선 (E/F_c × φ_AM / × ν) | **임계반경 50–500 nm** | ★ 입자크기-안정성 regime |
| **6a,b** | SE 껍질 응력장 σ_RR/σ_θθ/Mises vs R/R_A (ν=0.15 / 0.35) | 방사 ~+4 GPa, Mises ~−4→−2 | 사이클 응력 수 GPa ≫ 압밀 수백 MPa |
| **7** | σ_yield/F_c × ν, 소성흐름/취성 경계 (φ_AM 0.4–0.7) | **σ_yield<0.5F_c → 박리방지** | ★ ductile SE 설계기준 |
| **8a,b** | FPT(평균·std) vs 박리면적 %, 연속 vs 불연속 | 연속 50 %→mean×2.75/std×5 | ★★ **박리→ASR** 우리 coverage→ASR 의 시간축 |
| **8c** | random-walk 모식 (박리구 + t_P/t_S) | d_p=d_e/10, mob 10× → 2t_P→3t_P | ★ 박리 connectivity 가 ASR 결정 |

---

## 7. Post-processing ★
- **무엇:**
  - **닫힌형 해석** — cohesive 에너지 Eq 8 → 임계열림 Eq 9 → 박리개시 strain Eq 10 → 임계반경 Eq 11/12 → 소성억제 Eq 14.  (수치근 없음, 전부 대수.)
  - **contour 플롯** — Eq 10 을 (E_se, γ) 평면에 (Fig 3a), Eq 12 를 (E/F_c, ν, φ_AM) 평면에 (Fig 5), Eq 14 를 (σ_yield/F_c, ν) 평면에 (Fig 7) 매핑.
  - **random-walk FPT 몬테카를로** — 1000 walker, 2160-삼각형 입자표면, 박리=반사경계, step=1 % 반경 → 평균·std FPT vs 박리 % (Fig 8).
- **도구**: 명시 안 함 (해석식 + 자체 random-walk; Mathematica류 플롯 추정 — Fig 3b "0.0–1.0" 축 스타일).
- **수치화·기록**: 임계조건을 *무차원군*(A_crit/‖u‖_R, E/F_c, σ_yield/F_c, 2γ/‖u‖_R·E)으로 정규화 → 소재-무관 설계맵.

---

## 8. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`
| 항목 | 이 논문 (Bucci 2018) | 우리 (DEM+MPM) | 차이 / 이유 |
|---|---|---|---|
| 대상 물리 | **사이클-구동 AM↔SE 계면 *박리*** (cohesive decohesion) | **압밀-시점 AM-SE *접촉면적*** (Stage-E Tabor) + 압밀 porosity | ★ **시간축이 다름** — 그들=*사이클 후*, 우리=*제조 순간*.  같은 계면의 *형성*(우리) vs *파괴*(그들) |
| 계면 모델 | 연속체 **cohesive traction-separation 면** (‖u‖ 열림) | 이산 입자별 **Tabor/Hertz 접촉 area** + Holm 구속저항 | 연속-면 cohesive ↔ 이산-접촉 area (추상화 다름) |
| SE 거동 | 선형탄성 또는 **elasto-plastic(J2/Tresca, *박리억제* 용도)** | DEM hooke/hysteresis(연화 1.35) + **MPM J2(void-fill 형상흐름)** | ★ *같은 J2 계열*이나 용도 다름: 그들=응력완화·박리방지, 우리=형상흐름·압밀 |
| AM 입자 | *명시 안 함* — 단일 구 반경변화를 부과변위로 | **명시적 다입자 + PSD(12:4:1) + 접촉망** | 1-particle 해석 ↔ 다입자 수치 (정반대 추상화) |
| 부피변화 driver | **Li de/intercalation(사이클)** → AM 수축 → 계면 응력 | **가압(300 MPa 제조)** → 접촉/overlap | ★ driver 다름: 사이클 화학팽창 ↔ 제조 압력 |
| 임피던스/ASR | **박리→FPT→ASR↑** (random-walk, *상대*) | σ_ionic 솔버(Kirchhoff/Holm) + ASR_ionic(validation_flags) | 그들=*박리에 의한* ASR 증가(시간축); 우리=*구조에 의한* 절대 ASR(정적) |
| 파괴 | **AM-SE *계면* 박리** (cohesive, 사이클) | **Auerbach AM-AM 입자균열** (접촉응력, 압밀) | ★ 균열 *위치* 다름: 그들=*계면*, 우리=*AM 입자*; 둘 다 AM-SE 계면 박리는 *우리 미보유* |
| 입자크기 효과 | 박리 *개시* 무관, *안정성*은 의존(임계 50–500 nm) | size=PACKING(Furnas), overlap 거의 무관 | 다른 축 (그들=파괴안정성 크기, 우리=패킹 크기) |
| 검증 | 해석(실험·수치 검증 *없음* — 설계맵) | solver=ground truth + 외부 실험앵커(Minnmann/Bazzoun) | 그들=순수 이론 → 우리 *압밀/전달* 과 직접 수치비교 불가, *개념* 보완 |
| 소재 | **소재-무관 스윕**(E 20–200) | LPSCl(E 22–24) + NMC811 | 우리는 그 스윕의 *한 점* — LPSCl E≈22 ⇒ "compliant 경계(25)" 근처 |

---

## A. ## 우리 DEM+MPM 대비 (comparison vs ours) — 계면 *형성*(우리) ↔ 계면 *파괴*(그들)

> ★ 이 절이 이 논문의 frame[5] 핵심: **그들의 "박리 → 면적비 임피던스↑" 는 *바로 우리 Stage-E 가 압밀시점에 계산하는 그 AM-SE 접촉면적*의 *사이클 열화*다.**  같은 물리량(AM-SE 계면 접촉/면적)을 우리는 *형성*(제조 순간), 그들은 *파괴*(사이클 후) 의 두 시점에서 본다.

### A.1 같은 계면, 다른 시점 — 우리 Stage-E coverage ↔ 그들 박리
- **우리 Stage-E (Tabor)**: 압밀 300 MPa 순간 AM-SE *접촉면적*(coverage)을 plastic Tabor 로 계산 — real_14 에서 **AM_P/AM_S coverage 49.6/48.2 % (Tabor) vs Hertz 18 %** (CLAUDE.md DEM↔MPM scaffold cross-validation).  이게 **Li⁺ 가 AM↔SE 로 건너가는 *면적***.
- **그들 박리**: 사이클이 돌면 AM 부피변화(7.5 %)가 그 계면을 *벌려*(‖u‖_R=2γ/F_c), **접촉면적이 *줄고*** → FPT(=Li 인터칼레이션 시간) **×2.75**(연속 50 %) → **ASR↑**.
- ⇒ ★ **인과 사슬 완성**: *우리* coverage(압밀) → *그들* 박리(사이클) → *그들* FPT/ASR(열화).  우리가 압밀시점 coverage 를 안다면, 그들 식(Eq 10 박리개시 + Fig 8 FPT)이 그 coverage 가 *사이클로 얼마나 깎이는지*를 준다.

### A.2 우리 ASR_ionic ↔ 그들 FPT-ASR
- 우리 `validation_flags.asr_ionic_Ohm_cm2` = 구조에서 푼 *정적* 면적비 이온저항 (σ_thermal Ridge 의 feature 로도 사용).
- 그들 ASR = *박리에 의한* 증가분 (random-walk FPT 비, *상대*).  → ★ **우리 정적 ASR 에 그들 박리-FPT 배수(×2.75 연속/더 작은 불연속)를 곱하면 *사이클 후* ASR 추정** = 우리 ASR 의 *시간축 확장* 골격.
- ⚠ 단 그들 FPT 는 *비*(상대)지 절대 Ω·cm² 아님 → 우리 절대 ASR 에 *배수*로만 적용, 절대값 전사 금지.

### A.3 우리 MPM J2 는 계면 박리를 *못* 한다 (frame[5] 공백 명시)
- 우리 MPM = **연성 J2 *형상흐름*** (void-fill, SEM morphology) — *연속체*라 **계면 decohesion(균열·박리) *불가***.  그들 cohesive-zone 은 *바로 그 박리*를 모델.
- → ★ **우리 MPM 으로 박리 못 함**: SE 가 갈라지는 게 아니라 *흐르므로*.  계면 박리는 (a) 그들 해석식, 또는 (b) devaucorbeil2020 리뷰가 가리킨 **continuous-damage/cohesive MPM**(Homel-Herbold mixed)로만 — 우리 J2 에 *별도 damage 변수* 추가 필요.
- 우리 **Auerbach 는 AM-AM 입자균열**(접촉응력), **AM-SE *계면* 박리 아님** → 이 논문이 그 칸을 비춤.

### A.4 응력 스케일 — 사이클(수 GPa) ≫ 압밀(수백 MPa)
- 그들 Fig 6: SE 껍질 사이클 응력 **방사 ~+4 GPa, Mises ~−4 GPa**.  우리 압밀 = 300 MPa 제조.
- = Kang2025/yun2023 의 "확산-유발 응력 최대 GPa ≫ 가압 수백 MPa" 와 **같은 계열** → **사이클 역학이 압밀 역학보다 훨씬 가혹** → 우리가 압밀만 보면 *과소평가*하는 영역.  ⚠ 단 우리 *압밀* porosity/Heckel 결론(압력이 주역)에 이 "사이클 응력 큼"을 전이 금지 (맥락 분리).

---

## B. ## 적용가능성 (applicability to our model) — 우리 coverage/ASR 채널의 *사이클 열화* 경로

> ★ 구체적으로 우리 *어느 채널*에 *무엇*을 넣을지.  대부분 **backlog B6 (time-axis / 사이클 열화)** 로 귀속.

### B.1 박리→ASR 관계식 = 우리 coverage/ASR_ionic 의 *사이클* 열화 모듈 (backlog B6)
- **무엇**: 그들 **Eq 10**(박리개시 strain (αc)_fracture) + **Fig 8**(박리% → FPT 배수) 두 식.
- **어디에**: 우리 coverage(Stage-E AM-SE area) + `asr_ionic_Ohm_cm2` 채널.
- **어떻게**:
  1. AM 부피변화(인터칼레이션 strain)를 입력 (NMC811 = **~5.9 % 부피** stated in yun2023/Kang2025; 이 논문 전형 7.5 %).
  2. 우리 SE 물성(E_eff vs real, ν, 추정 F_c·γ)으로 **(αc)_fracture** 계산 → AM 변화가 이를 넘으면 박리 개시.
  3. 박리면적 % → **Fig 8 FPT 배수**(연속 ×2.75 / 불연속 더 작음) → 우리 정적 coverage·ASR 에 곱해 **사이클-N 후 coverage/ASR** 추정.
- **산출물**: `coverage(N cycles)` 와 `ASR_ionic(N)` 의 *time-axis* — 우리가 지금 *못 주는* 사이클 의존 transport 열화.

### B.2 입자크기 vs damage-zone → 우리 coverage 가 *사이클-안정*한 영역
- **무엇**: 그들 **Eq 12 / Fig 5**(임계반경 A_critical = f(E/F_c, ν, φ_AM, ‖u‖_R)).
- **어디에**: 우리 AM PSD(12:4:1) + coverage 채널.
- **어떻게**: 우리 AM_P(큰, ~6 µm)·AM_S(작은) 각각이 A_critical(50–500 nm) 대비 *훨씬 큼* → **둘 다 불안정-전파 쪽**(brittle snap).  ⇒ ★ **우리 AM 은 사이클 박리 시 *급격*(gradual 아님)** → coverage 가 사이클로 *계단식*으로 깎일 수 있음 (점진 아님).  + Kang2025 "큰 입자 사이클 균열"·우리 Auerbach AM_P 균열과 합쳐 **"큰 다결정 AM = 사이클 박리·균열 둘 다 취약"** 의 정량 근거.
- ⚠ Eq 12 는 ‖u‖_R(계면 cohesive length, ~1 nm)·F_c(접착강도) 입력 필요 — 우리가 *모르는* 값 → first-principles(ref Hong/Qi) 또는 yun2023 G_c 2.93 J/m² 로 추정해야 (불확실 밴드로).

### B.3 compliant-E-accommodates-more = 인용 가능한 문헌값
- **무엇**: "**E_se < 25 GPa + γ > 5 J/m² 면 부피변화 25 %까지 박리 지연**"; "**σ_yield < 0.5·F_c 면 소성이 박리 방지**".
- **어디에**: 우리 deck/paper 의 frame[2] "softened E / ductile SE" 논거.
- **어떻게**: 우리 E_eff 1.35(DEM)/1.53(MPM)·real 22–24.  ★ **LPSCl real E≈22 < 25 = 그들 "compliant 경계" 바로 아래** → **LPSCl 은 *마침* compliant-쪽**(박리 지연에 유리한 SE) — 우리 "LPSCl 이 무르고 소성으로 압밀"(frame[2]) 과 *독립적으로 일관*.  → 인용: "LPSCl 의 E≈22 GPa 는 Bucci 2018 의 compliant 임계(25 GPa) 근방 → 사이클 박리를 *지연*시키는 쪽; 우리 frame[2]의 ductile-LPSCl 가정과 정합."  ⚠ 그들 25 = *해석 임계*(소재 측정 아님) → "근방" 으로만, 정밀 동일시 금지.

### B.4 ductile-SE 설계기준 ↔ 우리 frame[2]
- 그들 **σ_yield < 0.5·F_c → 박리방지** = 우리 "LPSCl 소성이 압밀·계면접촉 유지" 와 *같은 방향의 다른 목적*(그들=사이클 박리방지, 우리=압밀 densify).  → 우리 MPM 소성-SE 가 *압밀*뿐 아니라 *사이클 계면유지*에도 유리하다는 **추가 정당화**(단 우리 MPM 은 박리 자체는 못 모델 — A.3).

---

## C. ## frame[5] 위치 (our division) — 사이클 계면 박리 = 우리가 *비워둔* 시간축

> ★ softer novelty framing: 이 논문은 **해석 모델**(DEM 경쟁자 아님) → "그들이 owns / 우리가 owns" 를 *상보적*으로.

### C.1 우리가 OWNS (compaction-state)
- **압밀-시점 AM-SE *접촉면적 형성*** (Stage-E Tabor coverage, real_14 49.6/48.2 %).
- **명시적 접촉망 transport** σ_ionic/σ_e/σ_thermal (Kirchhoff/Holm) — *정적* ASR_ionic.
- **압밀 porosity/Heckel/coordination/percolation** + **Furnas dip**(패킹).
- **SE 소성 *형상* morphology + void-fill** (MPM J2, SEM 일치).
- **AM-AM 입자균열** (Auerbach, 압밀 접촉응력).

### C.2 그들이 OWNS (cycling interface stability) — 우리 *미보유*
- **사이클-구동 AM↔SE *계면 decohesion*** (cohesive 박리) — 부피변화 7.5 % 개시.
- **박리 *안정/불안정*** (ductile/brittle, 임계반경 50–500 nm).
- **소성-SE 의 *박리 억제*** 설계기준 (σ_yield<0.5F_c).
- **박리 → FPT → ASR** 의 *시간축* 인과 (고전도 SE 율속).

### C.3 division 한 줄
- **우리 = 계면의 *형성*(제조 순간 접촉면적·transport·morphology)**; **그들 = 계면의 *파괴*(사이클 박리·ASR 열화)**.
- 같은 AM-SE 계면의 **τ=0(압밀, 우리) ↔ τ=N cycles(열화, 그들)** 두 시점 → ★ **frame[5] 시간축 분업** (devaucorbeil2020 가 "SE 취성균열은 cohesive-MPM 으로" 가리킨 것과 같은 공백; yun2023/Kang2025 가 *SE/CAM* 균열의 *실험·FEM* 판이라면 Bucci 는 *AM-SE 계면 박리*의 *해석* 판).
- ⚠ **over-claim 금지**: 이 논문은 *해석*(실험·수치 검증 없음, 소재-무관 스윕) → 우리 압밀/전달 *수치*와 직접 비교 불가; *개념·설계맵·time-axis 골격*으로만.  DEM 경쟁자 아님 → "우리가 못 하는 걸 *해석으로* 보여줌" 의 보완 레퍼런스.

---

## 9. 인용 가능 문장 (deck/paper용)
- "An analytical 1D radially-symmetric cohesive-zone model (Bucci et al., PRM 2018) shows that AM-SE interfacial **delamination initiates once electrode particles change radius by only ~2.5 % (volume ~7.5 %)** during (de)intercalation — a strain encompassing most intercalation compounds — and that **only compliant electrolytes (E < 25 GPa) with large cohesive energy (γ > 5 J/m²) tolerate up to 25 % volume change**; LPSCl's E ≈ 22 GPa places it near this compliant threshold."
- "Delamination raises the area-specific impedance: a random-walk first-passage analysis gives a **2.75× mean (5× std) increase in Li intercalation time at 50 % contiguous delamination**, and the impedance penalty is governed by the *connectivity* of the delaminated patches, not only their area — directly the cycling degradation of the AM-SE contact area our Stage-E computes at compaction."
- "Delamination *initiation* is **independent of particle size** (the criterion contains no length scale), whereas *stability* of propagation is set by the particle radius relative to the cohesive length (critical radius ~50–500 nm); a **ductile electrolyte with σ_yield < 0.5·F_c prevents delamination** — the cycling-stability counterpart of our frame[2] ductile-LPSCl compaction argument."

## 10. 주의/한계 (over-claim 방지)
- **순수 해석 모델** — 실험·수치(FEM/DEM/MPM) 검증 *없음*.  contour 는 *설계맵*이지 측정값 아님 → 우리 압밀 porosity·전달 σ 절대값과 **직접 비교 불가**.
- **소재-무관 스윕** (LPSCl/NMC811 *지정 안 함*) — E_se 20–200 GPa 의 *한 점*으로만 우리계 매핑.  "compliant 25 GPa"·"7.5 %" 는 *해석 임계*지 LPSCl 측정 아님 → 근방·추세로만 cite.
- **1-particle 단위셀** (truncated-octahedron, φ_AM 균일) — 우리 다입자 PSD(12:4:1)·패킹·dip *전부 없음*.  기하인자 f(φ_AM) 만 공유.
- **Vegard linear + isotropic 가정** — 실제 NMC 의 비등방·비선형 팽창, 입계, c-축 붕괴 등 미반영.
- **cohesive 입력(F_c, γ, ‖u‖_R) 미지** — 우리계 적용 시 first-principles(Hong/Qi) 또는 yun2023 G_c 2.93 으로 *추정*해야 (불확실 밴드).
- **FPT 는 *상대* 비** — 절대 ASR(Ω·cm²) 아님 → 우리 절대 ASR 에 *배수*로만, 절대값 전사 금지.
- **rate-independent** — 충전율 의존(빠른 충전서 농도구배·국부 박리) 미반영 (저자 명시 향후과제).
- **계면 박리 ≠ 입자 균열 ≠ 좌굴** — 우리 Auerbach(AM-AM), yun2023/Kang(SE/CAM 균열), 박막 좌굴 과 *다른* 메커니즘(AM-SE *계면* cohesive 박리).  혼동 금지.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
