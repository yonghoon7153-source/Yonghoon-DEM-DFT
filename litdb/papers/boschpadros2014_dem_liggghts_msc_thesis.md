<!-- digest 표준 양식 확장 (paper-level standalone). ★ = 사용자가 특히 원한 항목 -->
# Discrete element simulations with LIGGGHTS — Carles Bosch Padrós (Swansea MSc Thesis, 2014)

> slug `boschpadros2014_dem_liggghts_msc_thesis` · DOI `n/a` (MSc thesis, 비출판) · type `DEM (LIGGGHTS — methods/validation thesis)` · PDF `BoschPadros_2014_Swansea_MSc_DEM_LIGGGHTS.pdf` · digested `2026-06-26` · status ✅
> ★ **우리 코드(LIGGGHTS) 자체를 다룬 유일한 thesis** — Swansea ZC2E(Zienkiewicz Centre), 지도 Prof. Y. T. Feng, MSc in Computational Mechanics, 2014년 6월. ★★ **단, 이것은 *학습/방법론 입문* thesis** (DEM 이론 정리 + LIGGGHTS 사용법 + 단순 데모 3종)이지 정량 검증·소재 연구가 아니다. → **가치 = (a) 우리 LIGGGHTS input 명령어/Hertz-history 거버닝식의 *교과서 수준 참조*, (b) LPSCl/NMC811·전달·소성 *전무*를 확인해 우리 novelty를 또렷이 대비.**

---

## 0. 왜 이 thesis를 읽는가 (먼저 읽을 것 — 기대 조정)

이 thesis는 **우리 DEM 엔진(LIGGGHTS)을 정면으로 다룬 유일한 문헌**이라 끌렸지만, **읽고 나면 우리에게 직접적 가치는 두 가지로 한정**된다:

1. **LIGGGHTS 사용법·Hertz/history 거버닝식의 교과서 참조** (§4.3 eq 4.1–4.10 = LIGGGHTS가 `pair_style gran model hertz tangential history`로 *실제 푸는* 법선/접선 force·damping·stiffness 식). 우리 input 스크립트의 `fix m1..m6`·`pair_style`·insertion·dump 명령 구조와 **1:1로 대조**할 수 있는 *주석 달린 예시 input*을 제공.
2. **우리 novelty의 *바닥 대비선(baseline)***: 2014 MSc thesis가 **순수 역학 DEM(transport 0, 진짜 소성 0, 정량 검증 0, 소재 LPSCl/NMC811 0)**임을 보임으로써, 우리의 (1) 전달 삼중항(Kirchhoff+Holm) (2) Stage-E 소성면적 (3) DEM↔MPM scaffold + J2 morphology (4) fracture-aware (5) literature σ_grain (6) 실험-앵커 독립보정 (7) solver→scaling-law LOOCV 예측기가 *무엇에 비해* state-of-the-art인지를 또렷하게 함.

⚠ **기대 조정 — 이 thesis가 *주지 않는 것*** (over-expect 방지):
- **정량 검증 수치 0**: 모든 결과가 Paraview 스냅샷의 *정성* 관찰(shock width 넓다/좁다, 입자가 붙는다/안 붙는다). porosity·σ·coordination·Heckel·강도 **숫자 없음**.
- **소재 데이터 0**: 모래(sand)·알루미늄·고무(rubber) — 임의 데모 재료. LPSCl/NMC811 **전혀 없음** → 절대값 전이 불가.
- **전달 0**: σ_ionic/e/thermal 전무 (frame[5] 역학 절반만, 그것도 *데모*).
- **진짜 소성 0**: 입자는 영원한 rigid 구; "elasto-plastic models can also be obtained" 한 줄 언급뿐 구현 안 함.
- **저자 스스로의 솔직한 한계**(§6): "objectives changed due to the unexpected slow pace to the understanding of the code" — 원래 목표(DEM/FEM coupling)에 *도달 못 함*. Janssen effect 압력 출력도 "post-processing 이해 부족"으로 미완.

→ 따라서 이 digest는 luding2008(우리 LAW *정의서*)이나 bazzoun2026(같은 소재·코드 *교차검증*) 같은 *물리 앵커*가 아니라, **"우리 코드의 사용법 참조 + 우리 work이 뛰어넘는 출발선"**으로 읽는다.

---

## 1. 한 줄 요약

**LIGGGHTS(오픈소스 DEM, LAMMPS 파생)로 단순 입상-역학 문제를 배우고 데모하는 2014 Swansea MSc 입문 thesis**: (Ch2) DEM 접촉모델 이론 — Hertz·soft-contact·JKR·DMT·van der Waals·liquid-bridge·damping·Coulomb/Mindlin/rolling 마찰 — 을 *교과서식*으로 정리하고, (Ch3) LIGGGHTS 설치·input 파일·명령·Paraview 후처리를 *튜토리얼식*으로 안내한 뒤, (Ch4) **모래 기둥의 표면 충돌**(restitution/friction/2-크기/2-재료 sweep + Janssen effect), (Ch5) **회전 드럼 내 점착(cohesion)** 데모를 *정성적*으로 보인다. **순수 역학, 전달 없음, 진짜 소성 없음, 정량 검증 없음** — 우리에겐 **LIGGGHTS 사용법·Hertz/history 식의 참조서이자 우리 novelty의 바닥 대비선**.

## 2. 메타

| 저자 | 기관/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Carles Bosch Padrós** (저자), 지도 **Prof. Y. T. Feng** | **Swansea University, Zienkiewicz Centre for Computational Engineering (ZC2E), College of Engineering. MSc in Computational Mechanics (Erasmus Mundus; CIMNE/UPC Barcelona 연계). 2014년 6월** | n/a (비출판 MSc thesis) | **소재 무관** — 데모는 모래(sand ρ=2700)·알루미늄 벽·고무(rubber, E=0.01 GPa). **LPSCl/NMC811 전무.** | **DEM 방법론·LIGGGHTS 사용법 입문 + 단순 데모 3종** (정성). 표지·선언·감사·초록 보일러플레이트, 본문 ~60쪽. |

> 인용 정보: 자유 인용 가능한 출판물 아님(MSc thesis). deck/paper 인용 시 "Bosch Padrós, C. *Discrete element simulations with LIGGGHTS*, MSc thesis, Swansea University (2014)"로. ⚠ peer-reviewed 아님 → *권위 있는 출처로 인용 금지*, "LIGGGHTS 사용법 예시" 수준으로만.

## 3. 핵심 물성 (수치)

> ⚠ **이 thesis는 소재·정량 검증 논문이 아니다.** 아래 "수치"는 전부 (a) 식의 기호, (b) 데모 input의 *임의 예시 파라미터*뿐. **검증된 물성·porosity·σ·강도 절대값은 0**. LPSCl/NMC811 전이 절대 금지.

| 물성/파라미터 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| porosity / 상대밀도 | **n/a** (전혀 측정 안 함) | — | — | 압밀 연구 아님 (충돌·드럼 데모) |
| σ_ionic / σ_e / σ_thermal | **n/a** | — | — | **전달 전무** — frame[5] 역학 절반 (그것도 정성 데모) |
| coverage / 접촉면적% | **n/a** | — | — | 접촉면적 출력 없음 |
| coordination Z | **n/a** | — | — | 배위수 분석 없음 |
| Heckel P_y / knee | **n/a** | — | — | Heckel 없음 (압밀 안 함) |
| E (데모 재료) | sand **66.3 GPa**, alu wall **69 GPa**, rubber **0.01 GPa**, cohesion-demo **5 MPa** | input 예시 | stated | 임의 데모값 (소재 무관) |
| ν (데모) | sand **0.15**, alu **0.334**, rubber **0.49** | input 예시 | stated | |
| COR e (데모) | **0.1–0.9** sweep (sand-sand), rubber-rubber **0.1** | sweep | stated | Fig 4.4 e=0.1/0.3/0.6/0.9 |
| μ 마찰 (데모) | **0.1–0.9** sweep; sand-alu 0.6–0.7 | sweep | stated | Fig 4.5/4.6 f=0.1/0.3/0.6/0.9 |
| ρ 밀도 (데모) | sand **2700**, rubber **1200**, ch3 예시 **2500** kg/m³ | input | stated | |
| 입자 반경 (데모) | **0.015 / 0.02 / 0.03 m** (cm급, 모래 *아님* — 큰 데모 구) | input | stated | bi-크기 0.015&0.03 |
| timestep Δt | **1e-5 s** (Ch4), **3e-6 s** (Ch3) | input | stated | |
| 점착 K (cohesion energy density) | **1e5 / 1e6** (SJKR), `Densitycohesion` pairpair **1000/2000/6000** | Ch5 데모 | stated | F=K·A (eq 5.1) |
| 압력 출력 | **정량 실패** (Janssen 정성만) | — | stated | §4.4: 압력이 0~3×기댓값 사이 요동, "post-proc 이해 부족" |

## 4. 시뮬레이션 방법 ★ — **DEM 이론 + LIGGGHTS 사용법의 교과서 정리**

이 thesis의 *실질적* 가치는 §4(Ch2 이론) + §4(Ch3 LIGGGHTS) + §4(Ch4 거버닝식)에 집중. 아래는 **모든 식을 그대로 옮긴 것** (우리 코드 대조용).

### 4.1 code / version
- **LIGGGHTS-dev 3.0.1** (2014-04-11 빌드), Sandia(원전 LAMMPS) 파생. Ubuntu 12.04, 8GB RAM, 쿼드코어 3.3 GHz. 병렬 가능(`--dev`). 후처리 = **pizza.py(`dump` → VTK 변환) + Paraview**. ★ **우리 production 스택과 동일 계보**(LIGGGHTS + 자체 후처리). 약어: LIGGGHTS = *LAMMPS Improved General Granular and Granular Heat-Transfer Simulations*.

### 4.2 ★ DEM 접촉모델 이론 (Ch2 §2.1–2.2.5) — **모든 식**

- **Newton 2법칙 (eq 2.1)**: `m·a = F`. 입자 = 병진+회전 결합운동.
- **두 물체 충돌의 4모델** (§2.1.1):
  1. **Molecular dynamics**: 입자 완전 rigid, 충돌 전후 속도비 = COR(0–1, e=1이면 에너지 완전보존).
  2. **Continuum deformable (FEM)**: 입자를 유한요소로 이산화 → 변형·응력 정밀하나 계산비용 막대 (입자 多 → 요소 폭증).
  3. **Soft contact model** ★: 각 입자 = single rigid element + **작은 overlap 허용**. force는 contact law, 운동은 dynamics 식. **= DEM의 출발점.** (⚠ 'soft'는 *overlap 허용*이지 입자 형상변형 아님 — 우리 rigid-구 한계와 동일.)
  4. **Hierarchical**: FEM 이산화 표현.
- **★★ Hertz 접촉모델 (eq 2.2–2.5, §2.1.1.4 + 재게재 eq 2.6–2.9 §2.2.5.1)** — *우리 transport 측 Hertz coverage·f_AM 재구성의 기준식*:
  ```
  P = (4·E*·√R* / 3) · δ^(3/2)            (2.2 = 2.6)   ← 법선 force-overlap (δ^1.5 비선형)
  δ = R₁ + R₂ − d                          (2.3 = 2.7)   ← overlap (중심거리 d)
  1/R* = 1/R₁ + 1/R₂                       (2.4 = 2.8)   ← 환산반경
  1/E* = (1−ν₁²)/E₁ + (1−ν₂²)/E₂           (2.5 = 2.9)   ← 환산 모듈러스
  ```
  Hertz 가정: **인장력 없음, 마찰 없음, overlap ≤ 반경**. "elasto-plastic models can also be obtained with experiments"라고만 언급(구현 안 함). 속도 작을 때(준정적)만 유효.
- **JKR 접착탄성 (eq 2.10, §2.2.5.2)** — 저장탄성E ↔ 표면E 손실 균형, *무른* 입자용:
  ```
  F = 4·E*·a³/(3·R*) − √(8π·Δγ·E*·a³)      (2.10)
  ```
  a=임계 접촉반경, Δγ=표면에너지. 접착력이 **Hertz 프로파일을 변형**.
- **DMT (eq 2.11, §2.2.5.3)** — 접착력을 Hertz force에 *더함*(프로파일 변형 안 함), *단단한* 입자용:
  ```
  F = 4·E*·a³/(3·R*) − 2π·Δγ·R*            (2.11)
  ```
  ★ 우리 SE-SE 점착 layer-map: **SE = 작고 단단 → DMT 체제**(dmt1975 digest와 일치). pull-off ≈ 2πRγ.
- **van der Waals (eq 2.12–2.13, §2.2.5.4)** — 장거리 인력(같은 물질, 근접만으로):
  ```
  Hamaker:        F_n = A·R*/(6·s²)                      (2.12)   A=Hamaker 상수, s=간극
  Lennard-Jones:  V(s) = 4l·[(s_min/s)^12 − (s_min/s)^6]  (2.13)   l=우물깊이
  ```
- **Liquid bridge (eq 2.14, §2.2.5.5)** — 젖은 입자 모세관+점성:
  ```
  F_n = 2π·γ·R·sinφ·sin(φ+θ) + π·R²·Δp·sin²φ            (2.14)
  ```
  (우리 무관 — 건식 LPSCl. 점착은 cold-weld/vdW이지 액교 아님.)
- **★★ 에너지소산·이력 (eq 2.15–2.17, §2.2.5.6)** — *우리 hooke/hysteresis와 직결*:
  ```
  F'_n = F_n(δ) + c_n·δ̇                                  (2.15)   법선 force + 점성댐핑
  1/m* = 1/m₁ + 1/m₂                                     (2.16)   환산질량
  d_n = 2·√(m*/(k_n·ξ·δ))                                (2.17)   점성댐핑 (ξ=댐핑계수)
  ```
  ★★★ **Fig 2.34 = "coefficient of restitution" 그래프 = 우리 hooke/hysteresis의 핵심**: loading 기울기 **k₁**, unloading 기울기 **k₂(>k₁)**, δ_max에서 unload 시 0이 되는 잔류 overlap. **이것이 LIGGGHTS `hooke/hysteresis`의 k₁/k₂ 이력**(= Walton–Braun/Luding eq 6). ⚠ 단 **이 thesis 본문은 이 이력모델을 *데모로 쓰지 않는다*** — Fig 2.34에 *그림만* 있고, Ch4/Ch5의 모든 시뮬은 `pair_style ... hertz`(순수 탄성 Hertz, k₁=k₂ 가역)를 쓴다. → **우리 hooke/hysteresis의 실제 *사용*은 luding2008 digest가 정의서**; 이 thesis는 Fig 2.34에서 *개념 그림*만 제공.
- **Coulomb 마찰 (eq 2.18, §2.2.5.6)**:
  ```
  F_t = μ·F_n·δ_T / ‖δ_T‖                                (2.18)   δ_T=sliding velocity
  ```
  slip = 복원탄성 + 영구소성 합. (⚠ 여기 "permanent plastic part"는 *접선 slip*이지 입자 형상소성 아님.)
- **Mindlin–Deresiewicz (eq 2.19–2.20)** — 한 쌍 구의 접선력이 접촉반경 줄이고 ring slip:
  ```
  loading  (Fn 일정, Ft↑):  δ_t = 3(2−ν)μFn/(16Ga) · [1 − (1 − Ft/(μFn))^(2/3)]            (2.19)
  unloading(Fn 일정, Ft↓):  δ_t = 3(2−ν)μFn/(16Ga) · [2(1 − (Ft*−Ft)/(2μFn))^(2/3) − (1 − Ft/(μFn))^(1/3) − 1]  (2.20)
  ```
- **Rolling 마찰 (eq 2.21)**: `μ_r = e_r/R` (e_r=구름저항팔). **Spinning/torsion 마찰**: "usually not taken into account in DEM."

### 4.3 ★ 동역학·시간적분 (Ch2 §2.2.6) — **모든 식**
```
F(U, Ü, t) = M·Ü + C·U̇                                 (2.22)   거버닝 (질량+댐핑)
중심차분 (central difference, 명시적):
  U̇(n+½) = (U(n+1) − U(n)) / Δt_n                       (2.23)
  U̇(n−½) = (U(n) − U(n−1)) / Δt(n−1)                    (2.24)
  Δt̄_n   = (Δt_n + Δt(n−1)) / 2                          (2.25)
  Ü_n    = (U̇(n+½) − U̇(n−½)) / Δt_n                     (2.26)   2nd order
  U̇_n    = (U̇(n+½) + U̇(n−½)) / 2                        (2.27)
임계 timestep:
  Δt_cr = 2·√(m/k)·(√(1+ξ²) − ξ)                         (2.28)   ← 접촉쌍별, ×factor 0.1–0.9
  Courant-Friedrichs-Lewy:  c = √(E/(ρ(1−ν²)))            (2.29)   대안 임계 timestep
```
★ **우리 `fix ts all check/timestep/gran` (Rayleigh time 체크)의 이론 배경 = eq 2.28/2.29**. timestep factor 0.1–0.9 = 우리 안정성 마진과 동일 관행.

### 4.4 ★★ 객체표현·접촉탐색 (Ch2 §2.2.2–2.2.4) — *방법론 정리*
- **4 객체표현**: ① 구·타원(가장 흔함·단순) ② 다각형·다면체(overlap 영역=다각형, corner-to-corner 문제 → 라운딩 근사, 신뢰성↓) ③ 복합형(구 합성, 예: 캡슐) ④ FEM 이산화. **이 thesis는 데모를 전부 *구*로만** (우리와 동일 한계 명시).
- **접촉탐색 3단계**(계산비용의 **최대 90%**): ① global search(bounding box: 원형/AABB/OBB) ② locating(Brutal / Cell-grid / NBS / D-cell / Dgrid — 각 알고리즘 Fig 2.17–2.20 도해) ③ local resolution(실제 형상 접촉 확인, 법선·접선·접촉점·overlap 결정). **temporal coherence**: Δt 작아 직전 스텝 접촉형상이 다음 스텝 초기추정으로 good. ★ 우리 `neighbor`·`neigh_modify`·linked-cell 이웃탐색의 이론 배경.

### 4.5 ★★ LIGGGHTS 사용법 (Ch3) — **우리 input 스크립트의 주석 달린 예시**
input 파일 논리 순서(엄격하진 않으나 권장): **일반설정 → 도메인 → 재료물성 → pair_style → 시간/중력 → 벽/geometry → 입자 분포·삽입 → 적분 → 출력(dump)**. 주석 달린 예시(Ch3 §3.1.2.1):
```
atom_style granular         # 입자 = diameter+density+angular velocity
atom_modify map array
boundary m m m              # m=non-periodic fixed
newton off                  # 3rd Newton law off
communicate single vel yes
units si
region reg block -1 1 -1 1 -1 1 units box
create_box 1 reg
neighbor 0.001 bin
neigh_modify delay 0
fix m1 all property/global youngsModulus peratomtype 200.e9      # ★ 재료물성 시작
fix m2 all property/global poissonsRatio peratomtype 0.45
fix m3 all property/global coefficientRestitution peratomtypepair 1 0.1
fix m4 all property/global coefficientFriction peratomtypepair 1 0.5
pair_style gran model hertz tangential history    # ★ Hertzian without cohesion
pair_coeff * *
timestep 0.000003
fix gravi all gravity 9.81 vector 0.0 0.0 -1.0
fix cv all mesh/surface file meshes/conveyor.stl type 1 surface_vel 2. 0. 0.   # CAD geometry
fix wall all wall/gran model hertz tangential history mesh n_meshes 4 meshes cv wall1 wall2 wall3
fix pts1 all particletemplate/sphere 1 atom_type 1 density constant 2500 radius constant 0.015
fix pdd1 all particledistribution/discrete 1. 1 pts1 1
fix ins nve_group insert/stream seed 1 distributiontemplate pdd1 maxattempt 300 nparticles 15 ...
fix integr nve_group nve/sphere
fix ts all check/timestep/gran 1000 0.1 0.1            # Rayleigh-time 안정성 체크
dump dmp all custom 400 post/dump*.conveyor id type type x y z ... vx vy vz fx fy fz omegax ... radius
dump dumpmesh all mesh/gran/VTK 400 post/dump*.vtk id cv inface wall1 wall2 wall3
run 4000000 upto
```
**주요 명령 사전**(§3.1.2.2): `atom_style`·`boundary`·`newton`·`region`·`create_box`·`neighbor`·**`fix property/global`**(재료물성; peratomtype=단일재료 scalar, **peratomtypepair=2재료 관계 → 행렬형**)·**`pair_style`**(hertz/hooke, ±cohesion — *가장 중요*)·`pair_coeff`·`timestep`·`fix gravity`·`fix mesh/surface`(STL CAD 삽입)·`fix wall/gran`·`fix particletemplate/sphere`·`fix particledistribution/discrete`·`fix insert/stream`·`fix nve/sphere`·`fix check/timestep/gran`·`dump`·`dump mesh/gran/VTK`.

### 4.6 ★★ Hertz/history 거버닝식 (Ch4 §4.3) — **LIGGGHTS가 *실제 푸는* 식 (eq 4.1–4.10)**
이것이 이 thesis의 **가장 load-bearing한 부분** — `pair_style gran model hertz tangential history`가 푸는 법선/접선 force·damping·stiffness의 *완전한 LIGGGHTS 식*:
```
주 접촉식:
  F = (k_n·δn_(ij) − γ_n·vn_(ij)) + (k_t·δt_(ij) − γ_t·vt_(ij))            (4.1)
      └─────── 법선 ───────┘   └─────── 접선 ───────┘
Hertz/history pair-style이 주는 변수값:
  k_n = (4/3)·Y*·√(R*·δn)                                                  (4.2)   법선 elastic 상수
  1/Y* = (1−ν₁²)/Y₁ + (1−ν₂²)/Y₂                                          (4.3)
  γ_n = −2·√(5/6)·β·√(S_n·m*) > 0                                          (4.4)   법선 점탄성 댐핑
  β = ln(e) / √(ln²(e) + π²)                                               (4.5)   ← COR e로부터
  k_t = 8·G*·√(R*·δn)                                                      (4.6)   접선 elastic 상수
  1/G* = 2(2+ν₁)(1−ν₁)/Y₁ + 2(2+ν₂)(1−ν₂)/Y₂                              (4.7)
  γ_t = −2·√(5/6)·β·√(S_t·m*) > 0                                          (4.8)   접선 점탄성 댐핑
  S_n = 2·Y*·√(R*·δn)                                                      (4.9)
  S_t = 8·G*·√(R*·δn)                                                      (4.10)
```
⚠ δt = 마찰항복기준으로 truncate된 접선변위. β(eq 4.5) = COR→댐핑 변환(우리 `coefficientRestitution`이 γ_n/γ_t를 통해 들어가는 정확한 경로). ★ **우리 input의 COR/E/ν가 LIGGGHTS 내부에서 *어떻게* k_n·k_t·γ_n·γ_t로 변환되는지의 명시식** — Hertz pair-style을 쓸 때의 참조. (우리 production은 `hooke/hysteresis`라 식이 *다르나*, Hertz coverage·f_AM 재구성·So2021 경로 비교 시 이 eq 4.2–4.10이 정확한 Hertz baseline.)

### 4.7 ★ 점착(cohesion) 모델 (Ch5) — *우리 SE-SE 점착·MPM `--coh`의 LIGGGHTS 구현*
```
선형 점착(SJKR): F = K·A                                                   (5.1)
```
F=점착력, A=접촉면적, **K=cohesion energy density**. Hertz 법선력에 *더해* 접촉 유지. input:
```
fix m6 all property/global Densitycohesion peratomtypepair 2 1000 2000 2000 6000
pair_style gran model hertz tangential history cohesion skjr      # ★ 'cohesion skjr' 키워드
```
★ **= 우리 MPM `--coh`(backlog A3)·SE-SE adhesion의 LIGGGHTS *직접 구현*** (SJKR = simplified JKR). 데모에서 K(=surface energy density) 1e5→1e6으로 키우면 입상물질이 **"두꺼운 유체"처럼** 벽에 붙어 더 높이 올라감(Fig 5.2 vs 5.1). → k_c↔K↔`--coh` 매핑의 정성 기준. ⚠ 단 SJKR `F=K·A`(면적의존)는 luding eq6의 `−k_c·δ`(overlap의존)와 *형태 다름* (둘 다 점착이나 함수형 상이).

### 4.8 bond/binder / MPM / 전달
- **bond/binder 모델**: **없음** (바인더 미모델). 점착은 SJKR로만.
- **MPM / continuum**: **없음** (순수 이산 DEM). ⚠ 단 §6에서 "long-term goal was DEM/FEM coupling" — *원했으나 미도달*. → **우리 DEM↔MPM scaffold 커플링이 바로 그가 도달 못 한 지점**(아래 §C).
- **전달 솔버**: **없음** (σ 전무).

### 4.9 ★ 입자 처리 (DEM판 "무질서 처리")
- **구(sphere)만** (데모 전부). 비구형(다각형/타원/복합)은 *이론으로 도해*하나 데모엔 안 씀.
- **PSD**: mono(Ch4 case1·Ch3) 또는 **bi-크기**(Ch4 case2 0.015&0.03, Ch5 2크기) — bi-disperse까지, poly-PSD 아님, **Furnas/패킹-dip 분석 없음**(충돌·드럼 데모지 압밀 아님).
- **rigid 구 + 순수탄성 Hertz CONTACT** — *진짜 SHAPE 소성 아님*, *심지어 이력(hooke/hysteresis)도 데모엔 안 씀*. Fig 2.34 k₁/k₂ 이력은 그림만. ⇒ `contact_models_layer_map.md` 층위(1) CONTACT-LAW의 *가장 단순판*(순수 Hertz, cap·점착·이력 다 빠진 baseline). 우리는 그보다 *위*(hooke/hysteresis 이력 + adhesion + Stage-E).

### 4.10 도메인/케이스/seeds
- **Ch4 sand impact**: 0.4×0.4×1.5 m 박스(알루미늄 벽), 모래를 위에서 -8 m/s로 삽입, 바닥 STL mesh 표면에 압력 출력 시도. 2000 입자, massrate 300, insert_every 5000 step, run 100000. **Janssen effect**(높이↑여도 벽마찰로 바닥압력 포화)를 *정성* 시연. seed: `insert/stream seed 5330` 등 단일 seed.
- **Ch5 cohesion drum**: 회전 드럼(cylinder/ring STL) 내 2크기 동일재료 입자, 점착 sweep(0/1e5/1e6) + 드럼 속도(14 rad/s) + 벽-점착 sweep. 정성 관찰만.

### 4.11 특이사항/한계 (저자 명시)
- **압력 출력 실패**(§4.4): "the pressure shown during the insertion does not follow a reasonable evolution. The values fluctuate ... 0 to three times the expected maximum pressure." 원인 = surface mesh 요소 少 or 충돌순간 momentum 급변 + "post-processing 이해 부족"(§6). → **LIGGGHTS granular-wall 압력 출력은 transient에 신뢰 못 함**이 교훈(우리 wallP readout 설계 시 참고: 우리도 *transient* wallP를 arm-guard로 무시 → 같은 함정을 독립적으로 만남).
- **friction은 restitution보다 영향 작음**(§4.4): COR sweep은 shock width 뚜렷이 바꾸나 friction sweep은 미미 → "friction does not have the same influence as restitution."
- **2재료 평균화**(§4.6, case3): COR 매우 다른 두 재료 섞어도 거동 거의 불변 — "a particle has the same probabilities of impacts with both materials" → 평균화.

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1.1 | 모래더미 사진 | (장식) |
| 2.1–2.8 | 물체운동·2체충돌·이산화·soft-contact 모식 | DEM 기초 도해 (교과서) |
| **2.8/2.30** | **soft particle Hertz 접촉**(δ, d, P) | **우리 Hertz coverage·overlap 정의 그림** (δ=R₁+R₂−d) |
| 2.9–2.11 | 객체표현(구·타원/다각형·다면체/복합) | 우리도 구만 — 비구형 한계 공유 |
| 2.13–2.20 | 접촉탐색(bounding box·Brutal·Cell·NBS·D-cell) | 우리 neighbor/linked-cell 이론 배경 |
| 2.23–2.29 | 접촉쌍(disk-disk·segment·ellipse) 법선 결정 | (우리 구-구만 사용) |
| **2.33** | **damping 모델**(loading/unloading 이력 면적 = 소산E) | F'_n=F_n(δ)+c_n·δ̇ 의 이력 면적 = 소산 |
| **2.34 (★)** | **coefficient of restitution: k₁(loading)·k₂(>k₁, unloading)·δ_max** | ★ **우리 hooke/hysteresis k₁/k₂ 이력의 개념 그림** — 단 이 thesis는 데모에 *안 씀*(Hertz만). 실제 정의는 luding2008 |
| 2.35–2.38 | rheological(spring-mass-dashpot)·friction·rolling·spinning 도해 | γ_n 댐핑·μ_r 구름저항 도해 |
| 3.* | (LIGGGHTS 텍스트 — 그림 거의 없음) | input 예시(§4.5) |
| 4.1–4.3 | sand impact 도메인·과정·바닥 mesh | 데모 셋업 |
| **4.4** | **COR sweep(e=0.1/0.3/0.6/0.9) vZ 분포** | COR↑→shock width↑(덜 안정, 더 튐). COR이 거동 *주도* |
| **4.5/4.6** | **friction sweep(f=0.1/0.3/0.6/0.9)** mono(4.5)·bi(4.6) | friction은 영향 *미미*(COR보다 약함) |
| 4.7/4.8 | 2재료(sand+rubber) ts 진화 | 2재료 평균화(거동 불변) |
| **5.1 vs 5.2** | **점착 OFF(5.1) vs ON(K=1e5, 5.2)** 드럼 | ★ 점착↑→"두꺼운 유체"·벽에 더 붙음 = 우리 `--coh`/SE-SE adhesion 정성거동 |
| 5.3 | 점착+빠른 드럼(14 rad/s) | 속도↑→점착 효과↑ |
| 5.4 | 高점착 입자 + 低 벽-점착 | 입자끼리 뭉쳐 한 덩어리, 벽 안 붙음 |

## 6. Post-processing ★

- **무엇**: **정성 Paraview 스냅샷만**. vZ(법선속도) 색칠로 shock width·packing 관찰. **Heckel·percolation·coordination·coverage·tortuosity·porosity·강도 — 전부 없음.** 유일한 *정량* 시도 = 바닥 granular-wall **압력 출력**인데 **실패**(transient 비물리, §4.4).
- **도구**: pizza.py(`dump` text → VTK) + **Paraview**(전 결과 = Paraview 스크린샷). 자체 분석 스크립트 없음.
- **수치화·플롯·기록**: 거의 없음 — *그림 관찰* 위주. input 파라미터만 표기. ★ 우리와 *극명히 대조*: 우리는 network 솔버 + Stage-E + LOOCV scaling-law + grade_engine 30+ 지표.

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`

> ★ **이 절의 핵심: Bosch Padrós 2014는 *순수 역학 LIGGGHTS 데모*다.** 우리 transport·소성·정량 측을 *전혀* 안 다루므로, "대비"는 (a) **우리 input ↔ 그의 Hertz/history 식·명령 대조**(우리 코드 사용법 sanity), (b) **그가 *비운 칸*이 곧 우리 novelty**임을 확인.

### 7.1 ★ pair_style 측 — 그는 순수 Hertz, 우리는 hooke/hysteresis + 점착 + Stage-E

| 항목 | 이 thesis (Bosch 2014) | 우리 | 차이 / 관계 |
|---|---|---|---|
| 법선 pair_style | **`hertz tangential history`** (eq 4.1–4.10, 순수탄성 Hertz, k_n∝δ^0.5) | **`hooke/hysteresis`** (Luding eq6, k₁→k₂ 이력 + δ₀ 잔류겹침) | **다른 LAW** — 그는 *가역 Hertz*, 우리는 *비가역 이력*. Fig 2.34에 이력 *그림*만 있고 데모엔 Hertz만 씀 → 우리가 *한 단계 위* LAW |
| 점착 | **SJKR `cohesion skjr`, F=K·A**(면적의존, eq 5.1) | `adhesionStiffness`(overlap의존 −k_c·δ) + MPM `--coh` | **둘 다 점착이나 함수형 다름**(면적 vs overlap). SJKR = 우리 `--coh`의 LIGGGHTS 사촌 |
| 항복/소성 캡 | **없음** ("elasto-plastic ... can be obtained" 한 줄, 미구현) | 없음 → 18× 연화로 보상 (+ Stage-E 소성면적, + So2021 H-cap 경로) | 그는 *언급만*; 우리는 *연화로 실제 압밀* + Stage-E로 소성면적 보정 |
| Hertz 식 변수 | **eq 4.2–4.10 명시**(k_n·γ_n·β·G* 등) | LIGGGHTS 내부 동일 계열 | ★ **우리 Hertz coverage·f_AM 재구성·So2021 비교의 baseline 식** = 이 thesis가 깔끔히 정리 |
| 입자 형상 | rigid 구 (CONTACT만) | DEM도 rigid 구; SHAPE 소성은 MPM | **같은 한계**(SHAPE 없음) — 우리 MPM이 보강(frame[5]) |
| timestep 안정성 | eq 2.28/2.29 + factor 0.1–0.9, `check/timestep/gran` | 동일 관행 | **사용법 일치**(우리 setup sanity) |

### 7.2 ★★ 그가 *비운 칸* = 우리 novelty (frame[5] + 7대 차별점)

| 축 | 이 thesis | 우리 | → 우리 novelty |
|---|---|---|---|
| **전달 σ** | **전무**(역학 데모만) | **σ_ionic+σ_e+σ_thermal 삼중항** (Kirchhoff + Holm R=1/(2σr_c)) | ★ (1) transport TRIAD — *완전히 그가 비운 칸* |
| **소성 접촉면적** | 없음(접촉면적 출력조차 없음) | **Stage-E** (Tabor + volume 소성면적, coverage Hertz/Tabor) | ★ (2) Stage-E |
| **소성 morphology** | 없음(rigid 구) | **MPM J2 진짜 형상변화** + DEM↔MPM **scaffold** 커플링 | ★ (3) — 그가 §6에서 *원했으나 도달 못 한* DEM/FEM coupling |
| **균열** | 없음 | **fracture-aware** (Auerbach·Lawn, f_intact, frac_severe) | ★ (4) |
| **σ_grain 근거** | 없음 | **Cronau 2022 단결정 + Cronau(r_SE) sub-µm 인자** | ★ (5) literature-grounded |
| **보정 철학** | 임의 데모값(검증 없음) | **실험-앵커 독립보정** (Minnmann porosity, EIS σ) + frame[4] | ★ (6) — 그는 검증 0; 우리는 다중 실험 앵커 |
| **예측기** | 없음(정성 관찰) | **solver→scaling-law LOOCV 0.90–0.98** 예측기 | ★ (7) |
| 정량 검증 | **0** (Paraview 스냅샷) | network 솔버 + Heckel R²0.965 + LOOCV + grade 30+지표 | 우리가 *정량* 전부 소유 |

### 7.3 비교 요약 한 줄
**Bosch 2014 = LIGGGHTS로 "공이 떨어지고 드럼이 돈다"를 *정성적으로* 배운 thesis** ↔ **우리 = LIGGGHTS(+MPM)로 LPSCl-NMC811 복합양극의 *압밀·전달·소성·균열·예측*을 *정량적으로 실험에 앵커해* 푸는 work**. 공유점은 **코드(LIGGGHTS)와 rigid-구·Hertz/history 접촉식**뿐.

---

## 8. 적용 인사이트 (내 연구에 어떻게)

- ① **LIGGGHTS 사용법·Hertz/history 식의 참조서로**: eq 4.1–4.10(`pair_style hertz tangential history`가 푸는 정확한 k_n·k_t·γ_n·γ_t·β 식) + §4.5 주석 input을 **우리 코드 setup sanity / Hertz coverage·f_AM 재구성 baseline / So2021 H-cap 비교의 기준식**으로 인용. (단 우리 production은 `hooke/hysteresis` → 실제 LAW는 luding2008.)
- ② **SJKR `cohesion skjr` F=K·A**(eq 5.1)를 **우리 `--coh`(backlog A3)·SE-SE adhesion의 LIGGGHTS 구현 참조**로. Fig 5.1↔5.2 정성거동(점착↑→벽에 붙음·"두꺼운 유체")을 `--coh` 도입 sanity 기준 삼기. ⚠ SJKR(면적의존) ≠ luding `−k_c·δ`(overlap의존) — 함수형 차이 유의.
- ③ **압력 출력 transient 함정**(§4.4 "0~3×기댓값 요동"): LIGGGHTS granular-wall 압력은 *충돌 transient*에 비물리 → 우리 **wallP readout의 arm-after-compaction guard가 같은 함정의 독립적 해결**임을 보강(우리는 transient를 *무시*하고 정상상태만). 그가 *못 푼* 것을 우리가 푼 사례.
- ④ **우리 novelty deck의 "바닥 대비선"으로**: "2014 MSc thesis조차 LIGGGHTS로 *역학 데모*에 머물고 transport·소성·DEM/FEM coupling에 도달 못 했다 — 우리는 그 셋을 모두 LPSCl-NMC811에 정량 구현"이라는 *positioning* 문장의 근거.
- ⑤ **frame[5] 분업의 또 다른 독립 확인**: 그가 §6에서 "long-term goal was DEM/FEM coupling"이라 *명시*하고 도달 못 함 → **역학 DEM에 변형장/형상이 빠진다는 인식이 2014부터 있었고**, 우리 DEM(transport)↔MPM(소성 SHAPE) scaffold가 그 미충족 coupling의 *실현*임을 보임.

## 적용가능성 (applicability to our LIGGGHTS DEM model) — 우리 input 스크립트/knob 매핑

> 이 thesis에서 **구체적으로 우리 LIGGGHTS setup을 anchor/sanity-check하는 데 쓸 수 있는 것**을 우리 input(`dem_scripts/*.liggghts`)·knob에 1:1로 매핑.

| 이 thesis 내용 | 우리 LIGGGHTS input/knob | 어떻게 쓰나 (concrete) |
|---|---|---|
| **eq 4.2–4.10** (Hertz/history k_n·k_t·γ_n·γ_t·β 식) | `pair_style gran model hertz ...`(우리 *비교용* Hertz 분기) + `fix m1 youngsModulus`·`m2 poissonsRatio`·`m3 coefficientRestitution` | **Hertz coverage·f_AM 재구성·So2021 H-cap 경로의 baseline 식**. 우리 `scripts/dem_am_load_fraction.py`의 Hertz 재구성(δ^1.5)이 eq 4.2/4.4와 일치하는지 sanity. β=ln e/√(ln²e+π²)(eq4.5)로 우리 COR→댐핑 변환 검증. |
| **`pair_style ... hooke/hysteresis`**(Fig 2.34 k₁/k₂ 개념) | 우리 production `pair_style gran model hooke/hysteresis` + `m6 maxElasticStiffness`·`m7 adhesionStiffness`·`m8 plasticityDepth` | Fig 2.34는 *개념 그림*만 → **실제 파라미터 정의는 luding2008 digest §7.1**(우리 m6/m7/m8↔k̂₂/k_c/φ_f)로. 이 thesis는 "Hertz≠우리 LAW"를 재확인하는 용도. |
| **SJKR `cohesion skjr`, F=K·A**(eq5.1) + `Densitycohesion` | (도입 후보) SE-SE `adhesionStiffness` ↔ MPM `--coh`(backlog A3) | `--coh` 도입·k_c 캘리브레이션 시 **SJKR(면적의존) 형태를 LIGGGHTS 측 cross-check**. 정성 sanity = Fig5.1↔5.2(점착↑→벽 점착·"두꺼운 유체"). ⚠ F=K·A ≠ −k_c·δ(함수형 차이) 유의. |
| **eq 2.28/2.29 + factor 0.1–0.9** (임계 timestep) | 우리 `timestep` + `fix ts all check/timestep/gran` (Rayleigh-time) | 우리 timestep 안정마진(factor)·`check/timestep/gran` 사용이 표준 관행임을 확인 — setup sanity. |
| **§4.5 주석 input 골격**(general→domain→material→pair→insertion→dump 순) | 우리 input 파일 구조 | 우리 스크립트의 명령 *순서·문법*(fix property/global peratomtype vs peratomtypepair 행렬형, insert/stream, dump custom/VTK)이 정석임을 대조. |
| **§4.4 압력 출력 transient 실패**("0~3×기댓값") | 우리 MPM/DEM **wallP readout + arm-after-compaction guard** | LIGGGHTS granular-wall 압력이 *충돌 transient*에 비물리 → 우리 wallP가 transient 무시·정상상태만 읽는 설계가 *옳음*을 보강(독립적 같은 함정). |
| **접촉탐색(§2.2.4) / 객체표현 구만(§2.2.2)** | 우리 `neighbor`·`neigh_modify` + 구-입자 가정 | 이론 배경 참조(우리도 구만 → 비구형 한계 공유, MPM이 SHAPE 보강). |

⚠ **핵심 caveat**: 이 thesis 데모는 전부 `hertz`(가역 순수탄성). **우리 production은 `hooke/hysteresis`(비가역 이력)** → eq 4.1–4.10은 *우리 실제 LAW 식이 아님*, Hertz baseline/비교용으로만. 우리 LAW의 *정의서*는 luding2008.

## ★ 우리 novelty — 왜 우리가 state-of-the-art인가 (our novelty vs this work)

> **명확히 주장한다.** Bosch Padrós 2014는 *2014년 학습/방법론 MSc thesis*로 **순수 역학 LIGGGHTS 데모**(정량 검증·전달·진짜 소성·소재 0)에 머문다. 동일 코드(LIGGGHTS) 위에서 우리는 **7대 차별점**으로 그 위에 선다 — *증거 기반*으로:

1. **transport TRIAD (Kirchhoff + Holm)** — 그는 σ *전무*. 우리는 명시적 접촉망 위 σ_ionic+σ_e+σ_thermal 삼중항(R=1/(2σr_c), Σ(φi−φj)/R=0). **frame[5]의 transport 절반 전체가 그가 비운 칸.**
2. **Stage-E 소성 접촉면적** — 그는 접촉면적 출력조차 없음. 우리는 Tabor+volume 소성면적으로 coverage(Hertz/Tabor)·σ를 보정.
3. **DEM↔MPM scaffold + J2 morphology** — 그는 rigid 구 + *순수 Hertz*; §6에서 long-term 목표였던 **DEM/FEM coupling에 *도달 못 함*을 스스로 명시**. 우리 scaffold(실제 DEM AM 골격 + MPM J2 SE 소성)가 *바로 그 미충족 coupling*을 SEM-검증된 morphology로 실현.
4. **fracture-aware** (Auerbach·Lawn, f_intact, frac_severe) — 그는 균열 0.
5. **literature-grounded σ_grain** (Cronau 단결정 + Cronau(r_SE) sub-µm) — 그는 임의 데모값, 물성 근거 0.
6. **실험-앵커 독립보정** (Minnmann porosity, EIS σ, frame[4] DEM↔MPM 비-cross-fit) — 그는 **정량 검증 0**(Paraview 정성 스냅샷). 우리는 다중 실험 앵커.
7. **solver→scaling-law LOOCV 예측기** (σ_ionic 0.975 / σ_e 0.953 / σ_thermal 0.903) — 그는 예측기 0(정성 관찰).

**증거**: 이 thesis 본문(~68쪽)에 porosity·σ·coordination·coverage·Heckel·강도 *숫자가 단 하나도 없고*(§3), 압력이라는 유일한 정량 시도마저 transient 비물리로 실패(§4.4), 저자가 직접 DEM/FEM coupling 미달을 적었다(§6). ⇒ 우리 7대 차별점은 *과장이 아니라* 그가 *명시적으로 비운/도달 못 한* 칸들과 1:1 대응.

**genuinely useful foundational content (정직)**: 그렇다고 무가치한 것은 아니다 — (a) **eq 4.1–4.10**(LIGGGHTS Hertz/history가 푸는 정확한 k_n·k_t·γ_n·γ_t·β 식)은 우리 Hertz coverage·f_AM 재구성·So2021 비교의 *깔끔한 baseline*이고, (b) **§4.5 주석 input**은 우리 코드 setup의 *문법·순서 sanity*이며, (c) **SJKR `cohesion skjr` F=K·A + 정성 점착거동**(Fig5.1↔5.2)은 우리 `--coh` 도입의 *LIGGGHTS 측 cross-check*다. = "방법론 참조서"로서의 제한적·실질적 가치.

## 9. 인용 가능 문장 (deck/paper용)

- "LIGGGHTS의 Hertz/history pair-style이 푸는 법선·접선 접촉식(k_n=(4/3)Y*√(R*δ), γ_n=−2√(5/6)·β√(S_n m*), β=ln e/√(ln²e+π²))은 Bosch Padrós(2014, Swansea MSc thesis)가 명시적으로 정리하며, 우리 Hertz coverage·AM 하중분담 재구성의 baseline 식이다." (단 우리 production LAW = hooke/hysteresis, luding2008.)
- "우리 SE-SE 점착·MPM `--coh`는 LIGGGHTS의 `cohesion skjr`(SJKR) 선형 점착 F=K·A에 대응하며, 점착세기↑가 입상물질을 '두꺼운 유체'화한다는 정성거동(Bosch 2014, 회전드럼 데모)이 그 도입 sanity의 기준이다."
- "2014년 Swansea MSc thesis(Bosch Padrós)는 LIGGGHTS로 모래 충돌·회전드럼 점착을 *정성적으로* 데모하는 데 그쳤고 long-term 목표였던 DEM/FEM coupling·정량 검증·transport는 도달하지 못했다 — 우리 work은 동일 코드(LIGGGHTS) 위에서 LPSCl-NMC811 복합양극의 압밀·전달 삼중항(Kirchhoff+Holm)·소성 morphology(DEM↔MPM scaffold)·균열·LOOCV 예측을 실험에 앵커해 정량 구현함으로써 그 미충족 지점들을 모두 채운다."
- "LIGGGHTS granular-wall 압력 출력은 충돌 transient 구간에서 기댓값의 0~3배로 요동해 신뢰할 수 없다(Bosch 2014, §4.4) — 우리 wallP readout의 arm-after-compaction guard는 이 transient를 무시하고 정상상태만 읽음으로써 같은 함정을 해결한다."

## 10. 주의/한계 (over-claim 방지)

- **비출판 MSc thesis** — peer-reviewed 아님. *권위 있는 물리 출처로 인용 금지*; "LIGGGHTS 사용법·Hertz 식 정리 예시" 수준으로만. (luding2008/bazzoun2026 같은 앵커와 *격이 다름*.)
- **정량 검증 0** — 모든 결과가 Paraview 정성 스냅샷. porosity·σ·강도·Heckel·coordination *숫자 없음* → 어떤 절대값도 우리와 비교 불가.
- **소재 무관**(모래·알루미늄·고무, 임의 데모값) — LPSCl/NMC811 전이 절대 금지.
- **전달 0**(역학 데모만) → frame[5] 역학 절반, 그것도 *데모*. σ 비교점 0.
- **진짜 소성 0** — rigid 구 + *순수 Hertz*(데모). Fig 2.34 k₁/k₂ 이력은 *그림만*, 데모에 미사용 → 우리 hooke/hysteresis 이력의 실제 정의는 luding2008(이 thesis 아님).
- **저자 스스로 목표 미달 명시**(§6): 원래 DEM/FEM coupling 목표 → "code 이해 pace 느려" 단순 데모로 축소. 압력 출력·Janssen·conveyor(Karim&Corwin "erasing friction with friction") 전부 *미완*. → 이 thesis는 *완결된 연구*가 아니라 *학습 기록*.
- **bi-disperse까지**(0.015&0.03), **Furnas-dip·패킹 분석 없음**(압밀 아님) — 우리 dip 작업과 무관.
- **`hertz` vs `hooke/hysteresis` 혼동 주의**: 이 thesis 데모는 전부 `hertz`(가역). 우리 production은 `hooke/hysteresis`(비가역). eq 4.1–4.10은 *Hertz* 식이지 우리 *실제* LAW 식이 아님 — Hertz baseline/비교용으로만.

## Supplementary Information

**없음** (MSc thesis, SI 없음). 본문 ~68쪽 자체가 완결. 부록(Abbreviations/Physical Constants/Symbols)은 §3 표·§4 기호 정의에 흡수.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
