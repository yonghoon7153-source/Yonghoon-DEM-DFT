# MLS-MPM 의 원전 — 형상함수 기울기 없이 APIC 의 C_p 로 힘 · 변형구배 (전달 2 배) + CPIC: 색칠 거리장으로 격자 한 장에서 변위 불연속 · 강체 양방향 결합 ★★★ 우리 Taichi MPM 의 뿌리 · 후보 A / A′-0 부품 — Hu, Fang 외 5 인 (ACM TOG 2018)

> slug `hu2018_mls_mpm_cpic_two_way_rigid_coupling` · DOI `10.1145/3197517.3201293` · type `MPM (명시적 MLS-MPM · APIC/PolyPIC 전달의 MLS 유도 + CPIC 색칠 거리장 · 강체 양방향 결합 — 컴퓨터 그래픽스 · 3D 시연 12 + 2D 1 · 에너지 곡선 2 · 로봇 영상 대조)` · PDF `51bd9be0-13._A_moving_least_squares_material_point_method_with_displacement_discontinuity_and_two-way_rigid_body_coupling.pdf` + 보충 `13._Sup_mlsmpm-supp.pdf` (5 쪽 · 식 10 개 · 그림 · 표 없음) · digested `2026-11-10` · status ✅
>
> ⚠ **먼저 읽을 것** — ① **컴퓨터 그래픽스 논문이다.**  검증은 *"visually comparable"* + 에너지 곡선 두 개 (MLS-MPM ↔ 전통 MPM **끼리** 비교) + 로봇 보행 영상 대조 (정성) 가 전부다.  해석해 · 수렴 차수 · 오차 노름 · 실험 수치 대조는 **0 건**.
> ② 재료는 젤 · 치즈 · 바나나 · 모래 · 물 (탄성계수 1.5 × 10³ – 1.8 × 10⁶ · 단위 미인쇄) — **LPSCl · NCM 이 아니다.  절대값 전이 0 건**, 가져오는 것은 이산화 식 · 알고리즘 · 비용 **비율** 뿐.
> ③ **압밀 · 기공 · 탈압 계산이 없다.**  하중은 중력과 지정 운동 (자르기 · 젓기 · 쓸기) 뿐이다.  **DEM 언급 0 건** (본문 + 보충 전문 검색).
> ④ CPIC 의 불연속은 **강체 (또는 운동이 지정된) 표면 메시의 양쪽**에서만 선다.  변형체끼리 (우리 SE–SE) 의 미끄럼 · 분리는 이 논문에 없다 — 그쪽은 여전히 단일 속도장 (붙음) 이다.
> ⑤ Table 3 의 Δx · Δt · 밀도 · 탄성계수는 **단위가 인쇄돼 있지 않다** — 이 카드의 파속 · Courant 수는 "한 단위계로 적혔다" 는 가정의 산술이다.
> ⑥ 표지: `인쇄` = 본문 · 표 · 캡션에 인쇄된 값 · `[카드 산술]` = 인쇄값에서 산술로만 유도 (식 병기) · `[판독]` = 그림에서 읽은 값 · `[미확인]` = 원문 (본문 + 보충) 에 없음 · `[우리 코드 판독]` · `[카드 추론]` = 논문 밖 판단.
>
> 짝 카드: `bardenhagen2000_mpm_granular_multibody_frictional_contact` · `bardenhagen2001_mpm_improved_contact_granular_stress_waves` — 변형체끼리의 접촉 (물체별 격자 속도장) 은 그쪽이 원전이다.  이 논문의 경계 투영 식 (25) 는 그 접촉 보정 (2000 판 식 23) 과 **같은 꼴** (법선 제거 + Coulomb 절단 + 자유 분리) 이고, 상대가 '질량중심 속도장' 대신 '강체 속도' 라는 점만 다르다 [카드 산술 · §4-7].  ⚠ 이 논문의 참고문헌 86 건에 Bardenhagen 은 **없다** [카드 확인].

---

## 0. 이 논문이 우리에게 왜 중요한가 (한눈 positioning)

우리 MPM (`scripts/mpm3d_compaction.py` · Taichi) 의 한 걸음 `substep()` 은 이 논문 §4 가 적은 **MLS-MPM 여섯 단계 그대로**다.  이 논문이 그 이산화의 원전이다.

> *"The main difference between traditional MPM and MLS-MPM is the choice of this function space.  Traditional MPM uses B-spline basis functions while MLS-MPM uses MLS shape functions (Φ_i(x) in §3.1).  This choice is the key contribution of MLS-MPM"* (p.150:5–150:6, §3.3.2)

> *"The only differences between MLS-MPM and traditional MPM are the force expression in step (2) and the F update in step (4)."* (p.150:8, §4)

| 논문 §4 의 단계 (p.150:7–150:8) | 논문의 식 | 우리 코드 [우리 코드 판독 · `scripts/mpm3d_compaction.py` · 가지 `claude/stoic-knuth-NObVQ` · 파일 마지막 커밋 `cb5a6a445`] |
|---|---|---|
| (1) 입자 → 격자 (APIC) | 보충 §1.2 의 전달식 · 본문 식 (24) 의 CPIC 없는 꼴 | 2952–2976 행 — 2차 B-spline 가중치 `w`, `grid_v[node] += wt * (pm * v[p] + affine @ dpos)`, `grid_m[node] += wt * pm` |
| (2) 격자 운동량 갱신 — **MLS-MPM 힘** | 식 (18) · (26) + §6 의 융합 행렬 Q_p | 2967 행 — `st = (-dt * pm * 4 * inv_dx * inv_dx) * P; affine = st + pm * C[p]`  (`4 * inv_dx * inv_dx` = M_p⁻¹ = 4/Δx² · `P` = Kirchhoff 응력 (∂Ψ/∂F)Fᵀ · `pm` = V_p⁰ (밀도 1 로 둔 부피 = 질량)) |
| (3) 격자 → 입자 (APIC) | 보충 식 (2)(3) | 3004–3017 행 — `nv += wt * gv; nc += 4 * inv_dx * wt * gv.outer_product(dpos)` |
| (4) 변형구배 갱신 — **C_p 재사용** | 식 (17) | 3017 행 — `F[p] = (I + dt * nc) @ F[p]` |
| (5) 소성 사상 | *"Project particle deformation gradient for plasticity (if there is any)"* | 3019–3029 행 — SVD → 로그 변형률 → J2 반환 사상 |
| (6) 입자 이류 | x_p ← x_p + Δt v_p | 3030 행 — `x[p] += dt * v[p]` |

그리고 이 논문의 **둘째 절반 — CPIC (§5)** — 은 우리 코드에 **한 줄도 없다**.  우리 경계 (AM 마스크 · 판 · 바닥 · 옆벽) 는 이 논문이 *"Normally for level set-based collision objects, boundary conditions are applied at grid nodes inside the level set"* (p.150:10, §5.5) 라고 부르는 **옛 방식** — 격자 노드에 직접 건 조건 — 이고, 강체로 돌아가는 힘은 재기만 하고 버린다 (§8-2).

| 우리가 필요한 것 | 이 논문이 주는 것 |
|---|---|
| 우리 MPM 이산화의 **인용할 원전 · 유도** | §3 식 (1)–(19) + 보충 §1–2 — 이 카드 §4-1 ~ §4-5 에 전부 옮김 |
| "단일 속도장 = 못 가른다" 는 우리 진단의 **제3자 진술** | §1 *"traditional MPM fails to model sharp separation of material points and cannot represent discontinuous velocities"* · §2.3 *"Due to the adoption of a single velocity field, it remains challenging to separate continuum materials in MPM"* |
| [DEM 우선 (수영)] 후보 **A′-0** (판 · 벽 · AM 자리에만 미끄럼 · 분리) 의 식 | 경계 투영 연산자 식 (25): sticky / slip / separate + 동마찰 μ |
| 후보 **A** (AM = 움직이는 강체 · SE 는 한 속도장) 의 부품 | 강체 속도 V_r(x) · 비호환 노드 임펄스 · 유령 속도 · 벌칙력 · 한 걸음 7 단계 (Fig. 10) — §4-6 ~ §4-9 |
| 후보 **A′** (입자마다 속도장) 의 근거 | **없음** — 변형체끼리의 접촉은 다루지 않는다 (그쪽은 Bardenhagen 2000 · 2001, Nezamabadi 2022 카드) |
| 해상도 · 안정 조건 규칙 | 한 줄뿐 — CPIC 는 *"only resolves features at a scale of grid Δx"* (§8).  CFL · 시간 간격 규칙은 **인쇄 없음** |
| 비용 근거 | Table 2 (전달 연산 ms) · Table 3 (예제별 입자 수 · sec/frame) · CPIC 덧비용 6 % — CPU 4 코어 기준, GPU 없음 |
| 정량 검증 | **없음에 가깝다** — Fig. 17 (두 이산화끼리) 뿐.  우리 정량 사용 (판 반력 · 기공률) 은 우리 단위 시험이 져야 한다 |

### 0-2. 이 묶음의 네 질문 (DEM 한계 · 소성 · 2D/3D · 탈압)

| 질문 | 이 논문의 답 (원문 위치) |
|---|---|
| (i) DEM (단단한 구 · 점접촉) 의 한계를 말한 문장 | **말 없음.**  본문 14 쪽 + 보충 5 쪽에 'discrete element' · 'DEM' 이 한 번도 안 나오고, 'contact' 는 참고문헌 제목 한 곳뿐이다 [카드 확인: 텍스트 층 전문 검색].  대신 **MPM 단일 속도장의 한계**를 말한다: *"Despite its high efficacy in many situations, traditional MPM fails to model sharp separation of material points and cannot represent discontinuous velocities."* (p.150:2, §1) · *"The main issue is that particle kernels in MPM are nonconforming to boundaries.  Each particle exchanges data with grid nodes in its entire kernel support across the boundary which naturally causes velocity field smoothing."* (p.150:2, §1) · *"Due to the adoption of a single velocity field, it remains challenging to separate continuum materials in MPM."* (p.150:3, §2.3) |
| (ii) 입자의 소성 · 큰 변형이 왜 어려운가 · 우회 · 비용 | 어렵다는 설명은 **없다** — 소성은 입자마다 변형구배를 항복면으로 사상하는 한 단계 (§4 단계 5) 이고 재료 모델은 다른 논문에 맡긴다 (von Mises = [Gao et al. 2017] · Drucker–Prager = [Klár et al. 2016], Table 3 캡션).  소성이 문제로 나오는 곳은 하나 — 재료 **분리**를 소성 연화 · 손상으로 흉내 내면 *"results in too many debris particles"* (p.150:2, Fig. 2b) · *"causes mesh dependent volume loss as well as undesirable debris"* (p.150:3, §2.3).  우회 = 분리를 구성식이 아니라 **운동학 (CPIC)** 으로.  비용 (소성 예제 3 건 · Table 3): 입자 1.2–1.8 M · 105.3–227.1 sec/frame · Intel i7-7700K 4 코어.  맞춘 값 · 맞춘 대상 **없음** (재료값은 보기 좋게 고른 값 — 근거 미인쇄) |
| (iii) 2D 인가 3D 인가 · 2D → 3D 전이 | 유도는 d = 2 또는 3 (식 7 아래) · 시연은 3D 12 건 + **2D 1 건** (Fig. 5 모래 바퀴 · 입자 4.1K · 0.3 sec/frame) · 2D 설명 그림 (Fig. 2 · 11 · 12 · 13).  2D 결과를 3D 로 옮기는 것에 대한 말은 **없다**.  차원에 따라 달라지는 것은 구현 수뿐: 강체 요소 (2D 선분 / 3D 삼각형) · 뿌림 범위 (Fig. 11 의 9 노드 / 3 × 3 × 3 = 27 노드) · 병렬 색 (4 / 8 묶음) · 비용 — *"Our discussion is focused on 3D cases, which are significantly more computationally expensive than 2D ones."* (보충 p.4) |
| (iv) 압력을 뺄 때의 거동 | **다루지 않는다** ('unload' · 'rebound' · 'springback' 0 회 [카드 확인]).  닿는 것은 둘 — 경계 유형 `separate` (멀어지면 구속 없음, 식 25) 와, 늘려 둔 탄성체를 자르면 되튀는 Fig. 7 (정성) |

---

## 1. 한 줄 요약

**KR:** MPM 을 "배경 격자를 이웃 탐색 도우미로 쓰는 EFG (요소 없는 Galerkin) 법" 으로 다시 읽어, 약형의 시험 함수 · 속도를 B-spline 대신 **MLS 형상함수**로 이산화한다.  선형 다항 기저 + 2차/3차 B-spline 가중이면 모멘트 행렬이 상수 (M_p = Δx²/4 또는 Δx²/3) 가 되어, 격자 → 입자 전달이 곧 APIC 이고 (C_p = 재구성한 속도 기울기), 노드 힘은 f_i = −Σ_p N_i(x_p) V_p⁰ M_p⁻¹ (∂Ψ/∂F) F_pᵀ (x_i − x_p), 변형구배는 F_p ← (I + Δt C_p) F_p 가 된다 — **형상함수 기울기 ∇N_i 를 한 번도 안 쓴다** (전달 연산이 2 배 빨라짐).  그 위에 **CPIC**: 강체 표면에서 뿌린 색칠 거리장 (노드마다 부호 없는 거리 + 표면별 '가까움 · 어느 쪽' 2 비트) 으로 입자와 노드의 **호환** 을 정하고, 입자는 호환 노드와만 질량 · 운동량을 주고받으며, 비호환 노드 몫은 경계 투영 (sticky / slip / separate + 마찰) 을 거쳐 **강체에 임펄스**로 간다.  격자는 한 장 그대로인데 표면 양쪽 재료가 따로 움직인다 — 절단, 두께 0 의 경계, 강체와의 양방향 결합.  단 Δx 규모까지만 해상하고, 변형체끼리의 접촉은 그대로 단일 속도장이다.

**EN:** MLS-MPM re-derives MPM as a modified element-free Galerkin method in which the background grid only accelerates moving-least-squares interpolation: with a linear polynomial basis and quadratic/cubic B-spline weights the moment matrix is constant, the grid-to-particle transfer is exactly APIC, the nodal force becomes f_i = −Σ_p N_i(x_p) V_p⁰ M_p⁻¹ (∂Ψ/∂F) F_pᵀ (x_i − x_p) and the deformation gradient update F_p ← (I + Δt C_p) F_p reuses the APIC matrix, so no kernel gradient is ever evaluated (≈ 2× faster transfers; "almost identical" energy curves to traditional MPM in two tests).  CPIC adds a colored distance field splatted from rigid surfaces and a particle–node compatibility test: particles exchange mass and momentum only with compatible nodes, the blocked contribution is projected (sticky / slip / separate with dynamic friction) and applied to the closest rigid body as an impulse, and incompatible nodes return a per-particle ghost velocity.  This gives cutting, infinitely thin boundaries and two-way rigid coupling on a single shared grid, at Δx resolution; deformable–deformable contact is not addressed.  Validation is visual plus two energy curves and one qualitative robot-footage comparison.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 제목 | **A Moving Least Squares Material Point Method with Displacement Discontinuity and Two-Way Rigid Body Coupling** |
| 저자 | **Yuanming Hu**† · **Yu Fang**† · **Ziheng Ge**† · **Ziyin Qu** · **Yixin Zhu**† · **Andre Pradhana** · **Chenfanfu Jiang**  († = *"visiting students at the University of Pennsylvania during this work"*, p.150:1 각주) |
| 소속 | Hu: MIT CSAIL · Fang: Tsinghua University · Ge: University of Science and Technology of China · Qu · Pradhana · Jiang: University of Pennsylvania · Zhu: University of California, Los Angeles |
| 저널 | **ACM Trans. Graph. 37, 4, Article 150 (August 2018), 14 pages** (쪽 표기 150:1–150:14 · © 2018 Association for Computing Machinery · `0730-0301/2018/8-ART150 $15.00`) |
| DOI | **10.1145/3197517.3201293** (p.150:1 인쇄 — 1저자 메모와 같음) |
| 분류 · 키워드 | CCS: Computing methodologies → Physical simulation · Additional Key Words: *Material Point Method (MPM), moving least squares, cutting, discontinuity, distance field, rigid coupling* |
| 접수 · 게재일 | **[미확인]** (인쇄 없음 · "Publication date: August 2018" 만) |
| 분량 | 본문 14 쪽 · Fig. 1–17 · Table 1–3 · 식 (1)–(28) · 참고문헌 86 건 [카드 계수] / 보충 문서 5 쪽 · 식 (1)–(10) · 참고문헌 6 건 · 그림 · 표 없음 |
| 연구 유형 | 수치 방법 (MPM 이산화 + 경계 · 강체 결합 알고리즘) + 고성능 구현 + 시연 (그래픽스) · 실험은 로봇 영상 한 건 (정성 대조) |
| 구현 기반 | *"We developed our system based on Taichi [Hu 2018]"* (p.150:12) — [Hu 2018] = *"Taichi: An Open-Source Computer Graphics Library.  arXiv preprint arXiv:1804.09293"*.  *"Our high-performance code will be open-sourced with the publication of this work"* — URL **[미확인]** (인쇄 없음).  ⚠ 그 라이브러리와 우리가 쓰는 파이썬 `taichi` 패키지의 관계, 그리고 흔히 말하는 "88 줄 MLS-MPM" 은 **이 논문 · 보충 문서에 없다** [미확인 — 원문 밖] |
| 자금 | Jiang 의 StartUp Grant (University of Pennsylvania) · NSF IIS-1755544 · National Key Technology R&D Program of China (2017YFB1002701) · Awowd Inc. · NVIDIA Corporation · SideFX 의 기부 |
| 감사의 글 | Christopher Long (Los Alamos National Laboratory) *"for useful discussions"* · Hannah Bollar (영상 해설) · Hangxin Liu (UCLA · 로봇 실험 보조) |
| PDF 상태 | LaTeX (acmart) 원본 · 텍스트 층 온전 · 그림은 렌더 래스터 + 벡터 (Fig. 2 · 5 · 10–13 · 17) |

**자기 위치 (저자 원문)**
> *"Interestingly, our derivation shows that MPM, although seemingly quite different from purely Lagrangian meshless methods, can be treated as a modified element-free Galerkin (EFG) method [Belytschko et al. 1994], where the background Eulerian grid merely acts as a helper structure for accelerating MLS interpolation from particle neighbor regions."* (p.150:4, §3)

> *"Compared to traditional MPM, the resulting Moving Least Squares Material Point Method (MLS-MPM) provides almost identical visual results and enables an effortless 2× speed up with easier implementation."* (p.150:2, §1.1)

---

## 3. 핵심 수치

> **라벨 규약** · `인쇄` = 본문 · 표 · 캡션에 적힌 값 · `[카드 산술]` = 인쇄값에서 산술로만 유도 (논문에 없는 수) · `[판독]` = 그림에서 읽은 값 (Fig. 17 은 PDF 벡터 경로 좌표를 눈금 글자 위치로 환산 — 두 곡선의 **차**는 축 환산 오차와 무관, 절대값은 ±0.01 정도) · `[미확인]` = 원문에 없음

### 3-1. 전달 연산 벤치마크 (Table 2 · §6.1 · 보충 §3)

| 항목 | 값 | 라벨 |
|---|---|---|
| 장비 | Intel Core i7-7700K · 4 코어 4.2 GHz · DDR4 4 × 8 GB 2400 MHz · Turbo Boost 끔 · gcc 5.4.1 | 인쇄 (Table 2 캡션 · §6.1) |
| 문제 | 영역 [0.1, 0.9]³ · Δx = 8 × 10⁻³ · 셀당 입자 8 개 균일 → **100³ 격자 · 입자 8 M** · APIC 전달 · 선형 탄성 | 인쇄 (보충 p.3) · 산술 확인 0.8 / 0.008 = 100 · 8 × 100³ = 8 × 10⁶ [카드 산술] |
| 정밀도 · 핵 | 32 비트 부동소수 · **2차 B-spline** (*"the smallest kernel that makes all constitutive models stable"*) | 인쇄 (보충 p.4) |
| "P2G" 에 넣은 것 | 변형구배에서 힘 계산 + 질량 · 탄성력 · APIC 아핀 운동량 산란 + 격자 속도 정규화 · 중력 | 인쇄 (보충 p.3) |
| "G2P" 에 넣은 것 | 격자 속도 · (필요하면) 속도 기울기 · 아핀 속도장 수집 + 변형구배 갱신 + 입자 이류 | 인쇄 (보충 p.3) |
| 전달이 차지하는 시간 | 전통 MPM 에서 P2G + G2P 가 *"usually takes more than 85% of time based on our experience"* | 인쇄 (p.150:11, §6) |

| 시간 (ms) | Reference ([Tampubolon et al. 2017] · OpenVDB) | Ours (MPM) | Ours\* (MPM · 최적화) | Ours\* (MLS-MPM · 최적화) | 라벨 |
|---|---|---|---|---|---|
| P2G · 1 스레드 | 4760 (1×) | 5744 (0.83×) | 2685 (1.77×) | **1283 (3.71×)** | 인쇄 (Table 2) |
| P2G · 4 스레드 | 1220 (1×) | 1525 (0.80×) | 688 (1.77×) | **328 (3.72×)** | 인쇄 |
| G2P · 1 스레드 | 8255 (1×) | 7476 (1.10×) | 1144 (7.21×) | **589 (14.01×)** | 인쇄 |
| G2P · 4 스레드 | 2070 (1×) | 2011 (1.03×) | 313 (6.61×) | **163 (12.70×)** | 인쇄 |
| ⇒ 알고리즘 몫만 (최적화 MPM → MLS-MPM) | — | — | 기준 | P2G 2.09× · 2.10× · G2P 1.94× · 1.92× (1 · 4 스레드) | [카드 산술] 2685/1283 · 688/328 · 1144/589 · 313/163 |
| ⇒ P2G + G2P 한 걸음 | 13,015 / 3,290 (1 / 4 스레드) | — | 3,829 / 1,001 | **1,872 / 491** | [카드 산술] 합 |
| ⇒ 입자 · 걸음당 | — | — | — | **234 ns (1 스레드) · 61 ns (4 스레드)** | [카드 산술] 1.872 s / 8 × 10⁶ · 0.491 s / 8 × 10⁶ |
| ⇒ 4 스레드 확장 (MLS-MPM) | — | — | — | P2G 3.91× · G2P 3.61× | [카드 산술] 1283/328 · 589/163 |

- 저자 진술: *"MLS-MPM halves the number of FLOPs needed for each particle"* · *"the usage of MLS-MPM directly enhances MPM performance by 2× in the case of explicit time integration, regardless of whether low-level performance engineering is performed"* (p.150:11).  암시 적분에서는 이득이 *"less significant"* (명시 적분에서만 아핀 운동량과 힘 산란이 한 번으로 합쳐지므로).
- FPU 이용률 (Intel VTune): 저자들의 최적화 MLS-MPM 의 P2G · G2P 가 [Tampubolon et al. 2017] 대비 **1.93× · 7.38×** (인쇄, p.150:11) — 최적화 전통 MPM 의 속도 이득 (1.77× · 7.21×) 이 이 비율과 비례한다고 저자가 적는다.
- ⚠ 이 수치는 **CPU (gcc 5.4.1 · intrinsics 직접 작성) · SPGrid** 구현의 것이다.  GPU · Taichi 커널 (우리 환경) 의 시간은 이 논문에 없다 [미확인].

### 3-2. 예제 13 건 (Table 3) + 카드 산술

Table 3 캡션 (인쇄): 입자 수 · 프레임 시간은 평균값 · 전부 Intel Core i7-7700K 4 코어 4.2 GHz · **모든 예제 Poisson 비 ν = 0.3** · 탄성 = fixed corotated [Stomakhin et al. 2013] · 약압축성 물 = [Tampubolon et al. 2017] · 소성 = St. Venant–Kirchhoff 탄성 + von Mises [Gao et al. 2017] · 입상 = St. Venant–Kirchhoff 탄성 + Drucker–Prager [Klár et al. 2016].  **단위는 인쇄돼 있지 않다.**

| 예제 (그림) | sec/frame | Δx | Δt | 입자 수 | 밀도 | 영률 | 체적계수 | 항복응력 | 마찰각 | c_P · C = c_P Δt/Δx [카드 산술] |
|---|---|---|---|---|---|---|---|---|---|---|
| Cutting armadillo (Fig. 7) | 107.0 | 5.0 × 10⁻³ | 5 × 10⁻⁶ | 1.3 M | 400 | 1 × 10⁵ | – | – | – | 18.3 · **0.018** |
| Bunny split (Fig. 4) | 16.7 | 3.3 × 10⁻³ | 3 × 10⁻⁴ | 2.0 M | 400 | 1.5 × 10³ | – | – | – | 2.25 · 0.20 |
| Water wheel (Fig. 1) | 120.3 | 2.5 × 10⁻³ | 5 × 10⁻⁵ | 1.4 M | 1000 | – | 1 × 10⁴ | – | – | 3.16 · 0.063 |
| Buoyancy (Fig. 6) | 122.9 | 3.1 × 10⁻³ | 1 × 10⁻⁴ | 5.3 M | 1000 | – | 1 × 10⁴ | – | – | 3.16 · 0.10 |
| Cheese (Fig. 3) | 227.1 | 3.3 × 10⁻³ | 2 × 10⁻⁵ | 1.8 M | 400 | 4 × 10⁵ | – | 10 | – | 36.7 · 0.22 |
| Goo blocks (Fig. 8) | 105.3 | 4.2 × 10⁻³ | 1 × 10⁻⁴ | 1.8 M | 400 | 5 × 10⁴ | – | 10 | – | 13.0 · 0.31 |
| Banana (Fig. 1) | 140.5 | 4.2 × 10⁻³ | 5 × 10⁻⁵ | 1.2 M | 400 | 4 × 10⁵ | – | 5 | – | 36.7 · 0.44 |
| Sand wheel (2D) (Fig. 5) | 0.3 | 2.5 × 10⁻³ | 1 × 10⁻⁴ | 4.1 K | 1000 | 3.5 × 10⁵ | – | – | 45 | 21.7 · 0.87 |
| Sand sweep (Fig. 15) | 288.3 | 2.0 × 10⁻³ | 2 × 10⁻⁵ | 2.6 M | 400 | 3.5 × 10⁵ | – | – | 35 | 34.3 · 0.34 |
| Sand stir (Fig. 9) | 158.3 | 3.1 × 10⁻³ | 1 × 10⁻⁴ | 5.2 M | 400 | 3.5 × 10⁵ | – | – | 10 | 34.3 · **1.11** |
| Sand paddles (Fig. 14) | 20.0 | 2 × 10⁻³ | 1 × 10⁻⁴ | 1.0 M | 400 | 3.5 × 10⁵ | – | – | 30 | 34.3 · **1.72** |
| Robot (Fig. 16) | 112.4 | 3.3 × 10⁻³ | 1 × 10⁻⁴ | 3.4 M | 2000 | 1.8 × 10⁶ | – | – | 45 | 34.8 · **1.06** |
| Robot (reverse) (Fig. 16) | 116.8 | 3.3 × 10⁻³ | 1 × 10⁻⁴ | 3.4 M | 2000 | 1.8 × 10⁶ | – | – | 45 | 34.8 · **1.06** |

- 앞 열 열 개는 전부 **인쇄 (Table 3)**.  마지막 열만 [카드 산술]: 탄성 종파 속도 c_P = √(E (1 − ν) / ((1 + ν)(1 − 2ν) ρ)) (ν 0.3 → 1.3462 E/ρ 의 제곱근) · 물은 c = √(K/ρ) · C = c_P Δt/Δx.  ⚠ **가정**: Table 3 의 수가 한 단위계 (예: SI) 로 적혔다.  단위가 인쇄돼 있지 않아 이 가정은 확인되지 않았다.
- ⚠ 그 가정에서 **C 가 1 을 넘는 예제가 넷** (Sand stir 1.11 · Sand paddles 1.72 · Robot 두 건 1.06) 이다.  논문은 단계 (2) 에서 symplectic Euler (식 18) 와 backward Euler (식 19) 를 **둘 다** 허용한다고만 적고, **어느 예제가 어느 적분인지 · 안정 조건이 무엇인지는 적지 않는다** [미확인].
- 소성 예제의 E/σ_y [카드 산술 · 같은 단위 가정]: Cheese 4 × 10⁴ · Goo blocks 5 × 10³ · Banana 8 × 10⁴ — 항복 변형률이 10⁻⁴–10⁻⁵ 급인 "거의 강소성" 재료다 (우리 생산 설정 E/σ_y ≈ 5.1 과 자릿수가 다르다 — §9-⑧).
- 프레임 길이 (초당 프레임 수) 가 **인쇄돼 있지 않아** sec/frame 을 걸음당 비용으로 바꿀 수 없다 [미확인].  영역 크기 · 격자 수 · 셀당 입자 수도 예제별로는 없다 [미확인].
- 강체 쪽 값 (경계 유형 B_r · 마찰계수 μ_r · 벌칙 강성 k_h · 강체 질량 · 관성) 은 **어느 예제에도 없다** [미확인].  그림 안 글자로만: Fig. 8 강체 블록 밀도 400 · 2000 · 5000 (젤 400) · Fig. 1 물레방아 "Inflow speed 0.5 / 1.0 / 0.5 · Wheel density 1.0 / 4.0 / 4.0" [판독 — 그림 안 표지].  Table 3 의 '마찰각' 은 모래의 Drucker–Prager **내부** 마찰각이지 강체 경계 마찰이 아니다.

### 3-3. 에너지 곡선 — 이 논문의 유일한 정량 검증 (Fig. 17 · §7)

*"We also perform two standard hyperelasticity tests: initially stretched oscillating cube and colliding balls.  The total energy evolution curves for MLS-MPM and MPM are plotted in Fig. 17 showing almost identical numerical dissipation."* (p.150:12)

| 시험 | 곡선 | t = 0 | 중간 | 끝 | 두 방법의 최대 차 | 라벨 |
|---|---|---|---|---|---|---|
| 진동하는 젤 (좌) | MLS-MPM | 2.125 | t 0.5: 0.959 · t 1.0: 0.609 | t 2.0: **0.329** | 0.018 (끝 · 전통 MPM 값의 5.8 %) · 평균 0.015 | [판독 · 벡터 경로] |
| | 전통 MPM | 2.119 | t 0.5: 0.945 · t 1.0: 0.591 | t 2.0: **0.311** | | [판독 · 벡터 경로] |
| 충돌하는 공 (우) | MLS-MPM | 0.692 | t 0.2: 0.629 · t 0.3: 0.532 | t 0.6: **0.508** | 0.010 (끝 · 1.9 %) · 평균 0.006 | [판독 · 벡터 경로] |
| | 전통 MPM | 0.692 | t 0.2: 0.630 · t 0.3: 0.541 | t 0.6: **0.517** | | [판독 · 벡터 경로] |

- ⇒ 끝/처음 에너지 비 [카드 산술]: 젤 0.155 (MLS) · 0.147 (전통) — **두 방법 모두 t = 2 까지 전체 에너지의 ≈ 85 % 를 잃는다**; 공 0.733 · 0.747 (≈ 26 % 손실 · 충돌 구간 t ≈ 0.13–0.3 에 집중).  저자는 이 감소를 *"numerical dissipation"* 이라 부른다 (캡션).
- 부호가 시험마다 다르다: 젤에서는 MLS-MPM 이 덜 잃고 (+5.8 %), 공에서는 더 잃는다 (−1.9 %) [판독].
- ⚠ 이 그림이 보이는 것은 **두 이산화가 서로 비슷하다**는 것뿐이다 — 초탄성 문제의 기준 (에너지 보존) 과의 거리, 격자 수렴은 보이지 않는다.  시험의 재료값 · 격자 · Δt · 에너지에 넣은 항 (운동 · 변형 · 중력 퍼텐셜) · 축 단위는 **[미확인]** (축 라벨 `E` · `t` 뿐).

### 3-4. CPIC 의 비용 · 저장

| 항목 | 값 | 라벨 |
|---|---|---|
| CPIC 덧비용 | 바나나 예제: 칼 없이 131.9 sec/frame → 자르면 140.5 sec/frame, *"with only 6% CPIC overhead"* | 인쇄 (p.150:12) · 140.5/131.9 − 1 = 6.5 % [카드 산술] |
| CPIC 가 필요한 범위 | *"only a narrow band near the rigid boundaries needs CPIC"* · *"Typically, around 90% blocks use regular MLS-MPM transfers"* | 인쇄 (p.150:12 · 보충 p.5) |
| 격자 CDF 저장 | 부호 없는 거리 32 비트 float + A_ir · T_ir 의 32 비트 부호화 (강체마다 2 비트) = **노드당 64 비트** | 인쇄 (p.150:9, §5.2.3) |
| ⇒ 한 장면의 강체 수 상한 | 32 / 2 = **16 개** (이 부호화 그대로일 때) | [카드 산술] — 논문에 '16' 은 인쇄돼 있지 않다 |
| 강체 입자 간격 | 삼각형마다 격자 꼴로 뿌리되 *"the minimum particle distance is smaller than grid spacing Δx"* | 인쇄 (p.150:9) |
| 거리 뿌림 범위 | 강체 입자마다 가장 가까운 노드 + 주변 3 × 3 × 3 노드 (3D · 27 개) — 2D 그림은 9 개 | 인쇄 (p.150:9 · Fig. 11 캡션) |
| SPGrid 블록 | 블록 4 × 4 × 8 노드 · 전달용 덧댄 지역 격자 6 × 6 × 10 노드 · 병렬 색 묶음 2D 4 · 3D 8 | 인쇄 (보충 p.4–5) |

### 3-5. ★ 이 논문에 **없는** 값 (정직 목록)

| 찾은 것 | 상태 |
|---|---|
| 압밀 · 치밀화 · 기공률 · 탈압 | **없음** |
| DEM · 입자 접촉 법칙 | **없음** (언급 0 회) |
| 시간 간격 규칙 · CFL 수 · 안정 조건 | **없음** — Table 3 에 Δt 값만 |
| 격자 수렴 · 수렴 차수 · 오차 노름 · 해석해 대조 | **없음** |
| 강체로 가는 힘 · 토크의 정확도 (부력 · 침강 · 회전 속도의 수치 대조) | **없음** — Fig. 6 · 8 · 14 는 그림뿐 |
| 운동량 · 각운동량 보존의 수치 확인 | **없음** — 벌칙 임펄스에 대해서만 *"the reverse impulse to the rigid body for conservation of momentum"* 라는 서술 |
| 강체 토크 식 · 임펄스를 속도로 바꾸는 식 | **없음** — *"applied to the closest rigid body … at x_j"* · *"advected in a standard way"* 뿐 |
| 강체–강체 충돌 해법 | **없음** — *"any external rigid body dynamics package can be used.  We will skip the details"* (§5.1) |
| k_h (벌칙 강성) · c (밀어내기 항) · 예제별 B_r · μ_r | **없음** |
| 로봇 대조의 수치 (이동 거리 · 속도 · 침하) | **없음** — *"match real world footage"* (영상) |
| 프레임 길이 · 영역 크기 · 격자 수 · 셀당 입자 수 (예제) | **없음** |
| GPU 성능 | **없음** (CPU 4 코어만) |
| 변형체끼리의 접촉 · 물체별 속도장 | **없음** |
| Table 3 의 단위 | **없음** |

---

## 4. 방법 ★

### 4-1. MLS 재구성 (§3.1, 식 1–4 · 그림 `eq_01_04_mls_reconstruction.png`)

표본 u_i = u(x_i) 가 주어졌을 때, 고정점 x 근처의 임의 위치 z 에서
> u(z) = Pᵀ(z − x) c(x)    (1)   — P = 다항 기저 (m 차 · l 차원), c = 기저 계수, 기저를 x 로 옮겨 모멘트 행렬의 큰 항을 피함 [Liu et al. 1995]

c(x) 는 가중 최소제곱 J_x(c) = Σ_{i∈B_x} ξ_i(x) (Pᵀ(x_i − x) c(x) − u_i)² 를 최소로 하는 값 (ξ_i = x_i 에 중심을 둔 국소 가중 함수 · B_x = ξ_i(x) ≠ 0 인 표본 집합):
> c(x) = M⁻¹(x) b(x)    (2)   — b(x) = Σ ξ_i(x) P(x_i − x) u_i · **모멘트 행렬** M(x) = Σ ξ_i(x) P(x_i − x) Pᵀ(x_i − x)

> u(z) = Σ_{i∈B_x} ξ_i(x) Pᵀ(z − x) M⁻¹(x) P(x_i − x) u_i = Σ Φ_i(z) u_i    (3)

Φ_i(z) = ξ_i(x) Pᵀ(z − x) M⁻¹(x) P(x_i − x) 가 EFG 의 노드 형상함수이고 *"exactly the shape function used in the Reproducing Kernel Particle Method (RKPM)"*.  상수 기저가 늘 들어 있으므로 Σ_i Φ_i = 1 (단위 분할) · 완전한 m 차 기저면 m 차 일관 (m 차 이하 다항식을 정확히 재현) · ξ_i 가 Cᵏ 면 Φ_i 는 C^min(k, m).

**선형 기저 (m = l = 1)** — P(x_i − x) = [1, (x_i − x)ᵀ]ᵀ 이면 함수값과 기울기가 한꺼번에 나온다:
> [û ; ∇û] = M⁻¹(x) Qᵀ Ξ(x) [u_1 ; … ; u_N]    (4)   — Ξ_ii = ξ_i(x) · Q(x) = [P(x_1 − x), …, P(x_N − x)]ᵀ · M = QᵀΞQ

### 4-2. APIC = 속도에 건 MLS (§3.2 · 보충 §1 · 그림 `eq_S01_S03_apic_as_mls.png` · `eq_S04_moment_matrix_Dp.png`)

- 논문의 주장: *"APIC [Jiang et al. 2015] and PolyPIC [Fu et al. 2017] are equivalent to applying MLS to velocity v(x) with B-splines as the weighting function ξ_i(x)."* (p.150:5).  EFG · RKPM 은 재구성 위치와 표본 위치가 같지만 MPM 은 **표본을 직교 격자 노드에 두므로 입자 이웃 탐색이 필요 없다** — 격자는 *"scratch pad"* 다.
- APIC 전달 (보충 p.1):
  > 입자 → 격자: m_iⁿ v_iⁿ = Σ_p m_p N_i(x_pⁿ) (v_pⁿ + C_pⁿ (x_i − x_pⁿ))
  > 격자 → 입자: v_p^{n+1} = Σ_i N_i(x_pⁿ) v̂_i^{n+1}    (보충 2)
  > C_p^{n+1} = (Σ_i N_i(x_pⁿ) v̂_i^{n+1} (x_i − x_pⁿ)ᵀ) D_p⁻¹    (보충 3)   — D_p = Σ_i N_i(x_pⁿ)(x_i − x_pⁿ)(x_i − x_pⁿ)ᵀ
- MLS 로 읽으면: 표본 {u_1 … u_N} = 입자 p 의 핵이 닿는 노드들의 속도, 재구성 함수값 û = v_p^{n+1}, 재구성 기울기 ∇û = C_p^{n+1}.  모멘트 행렬은
  > M(x_pⁿ) = Σ_i ξ_i(x_p) [[1, (x_i − x_pⁿ)ᵀ], [(x_i − x_pⁿ), (x_i − x_pⁿ)(x_i − x_pⁿ)ᵀ]]    (보충 4)

  이고 ξ_i 를 N_i 로 바꾸면 식 (4) 가 블록별로 보충 식 (2)(3) 이 된다.
- **왜 B-spline 인가** (보충 p.2): 다른 무격자법에서는 이웃 표본이 한 평면 · 한 직선에 놓이거나 모자라면 M 이 특이해져 의사 역행렬이 필요하다.  3D 선형 기저의 M 은 일반 4 × 4 행렬이지만 Σ_i ξ_i = 1 · Σ_i ξ_i (x_i − x) = 0 이면 블록 대각이고, **2차 / 3차 B-spline 이면 대각**이다 — 왼쪽 위 1, 오른쪽 아래 블록 D_p = **¼ Δx² I (2차) · ⅓ Δx² I (3차)**.  *"The simple form for D_p comes from the properties of B-splines, and is not generally true for other interpolation functions."*
- PolyPIC = 더 높은 차수의 기저 P (다중선형 · 2차 항) — 입자마다 계수 벡터 c(x_p) 를 싣고, 선형만 쓰면 APIC 로 줄어든다.  [Fu et al. 2017] 은 Gram–Schmidt 로 질량 직교 기저를 만들어 M 을 대각으로 둔다 (보충 p.2).

### 4-3. 약형에서 MLS-MPM 힘 식까지 (§3.3, 식 5–16 · 그림 `eq_05_07_…` · `eq_08_11_…` · `eq_12_…` · `eq_13_16_…`)

**지배식** (Euler 꼴): Dρ/Dt + ρ ∇·v = 0 (5) · ρ Dv/Dt = ∇·σ + ρ g (6), g = (0, −9.8, 0)ᵀ.

**약형** (updated Lagrangian 시간 이산화 · [Jiang et al. 2016] 을 따름 · g 생략):
> (1/Δt) ∫_{Ω^{tⁿ}} ρ (v̂_α^{n+1} − v_αⁿ) q_α dx = ∫_{∂Ω^{tⁿ}} q_α T_α ds − ∫_{Ω^{tⁿ}} q_{α,β} σ_{αβ} dx    (7)

q = Dirichlet 경계에서 0 인 임의 시험 함수, d = 2 또는 3, T = 경계 견인력.  v̂^{n+1} = 힘을 준 뒤의 속도장 (아직 시각 n 의 영역 위에서 정의).

**전통 MPM** (§3.3.3): 모든 공간 항을 B-spline 으로 — q_α = N_i q_{iα}ⁿ · v_αⁿ = N_j v_{jα}ⁿ · 집중 질량 m_iⁿ = Σ_p N_i(x_pⁿ) m_p.

**MLS-MPM 운동량 항** (§3.3.4): 영역을 입자 구획 Ω_p 로 나누고, 각 구획 안 (x 가 x_pⁿ 근처) 에서
> v_αⁿ(x) = Σ_j Φ_j(x) v_{jα}ⁿ    (8)        q_α(x, tⁿ) = Σ_i Φ_i(x) q_{iα}ⁿ    (9)
> Φ_i(x) = ξ_i(x_pⁿ) Pᵀ(x − x_pⁿ) M⁻¹(x_pⁿ) P(x_i − x_pⁿ)    (10)

→ Σ_p ∫_{Ω_p} ρ v_αⁿ q_α dx = Σ_{p,i,j} q_{iα}ⁿ v_{jα}ⁿ m_ij (11), m_ij = ∫_{Ω_p} ρ Φ_i Φ_j dx.  행별 합으로 집중하면
> m_iⁿ = Σ_p ∫_{Ω_p} ρ Φ_i dx ≈ Σ_p m_p Φ_i(x_pⁿ) = Σ_p m_p N_i(x_pⁿ)   — 전통 MPM 과 같다.

격자 속도를 v_iⁿ → v̂_i^{n+1} 로 전진시킨 뒤 입자 위치에서 v̂_α^{n+1}(x) = Pᵀ(x − x_pⁿ) c(x_pⁿ) 를 다시 맞추는 것 = APIC / PolyPIC 의 격자 → 입자 전달 (§3.2).

**MLS-MPM 응력 항 — 핵심 기여** (§3.3.5): 경계 견인력 항은 0 (zero Neumann).
> −∫ q_{α,β} σ_{αβ} dx = −Σ_p ∫_{Ω_p} q_{α,β} σ_{αβ} dx    (12)

자유도 (노드 î, 성분 α̂) 하나만 1 인 시험 함수 q_{iα}ⁿ = δ_{iî} δ_{αα̂} 를 식 (9)(10) 에 넣으면
> q_α(x, tⁿ) = Pᵀ(x − x_pⁿ) M⁻¹(x_pⁿ) ξ_î(x_pⁿ) P(x_î − x_pⁿ) δ_{αα̂}    (13)
> q_{α,β}(x, tⁿ) = (∂Pᵀ(x − x_pⁿ)/∂x_β) M⁻¹(x_pⁿ) ξ_î(x_pⁿ) P(x_î − x_pⁿ) δ_{αα̂}    (14)

**두 가지 선택** — ① 선형 다항 공간 Pᵀ(x − x_pⁿ) = [1, x_1 − x_{p1}ⁿ, x_2 − x_{p2}ⁿ, x_3 − x_{p3}ⁿ] (*"it is possible to generalize this choice to a higher order polynomial space, and we leave such an extension to future work"*) ② 가중 ξ_î = N_î 를 2차 / 3차 B-spline 으로 (M⁻¹ 이 상수).  그러면
> q_{α,β}(x, tⁿ) = M_p⁻¹ N_î(x_pⁿ) (x_{îβ} − x_{pβ}) δ_{αα̂}    (15)   — **M_p = ¼ Δx² (2차) · ⅓ Δx² (3차)**  (인쇄는 N_i 에 모자가 빠져 있다 — 식 16 은 N_î)

> **f_{îα̂} = −Σ_p ∫_{Ω_p} q_{α,β} σ_{αβ} dx ≈ −Σ_p V_pⁿ M_p⁻¹ σ_{p α̂β}ⁿ N_î(x_pⁿ) (x_{îβ}ⁿ − x_{pβ}ⁿ)**    (16)

V_pⁿ = 입자의 현재 부피.  근사 = 입자 구획 안 응력을 σ_pⁿ 하나로 두는 **한 점 구적**.  대조 (같은 쪽): 전통 MPM 은 f_{îα̂} = −Σ_p V_pⁿ σ_{p α̂β}ⁿ N_{î,β}(x_pⁿ) 로 *"requires explicitly differentiating the interpolation function"*.

★ **두 힘 식은 같은 식이 아니다** [카드 산술]: 전통 MPM 의 ∇N_î(x_p) 자리에 MLS-MPM 은 M_p⁻¹ N_î(x_p)(x_î − x_p) 를 쓴다.  1D 2차 B-spline (s = (x_p − x_i)/Δx) 로 풀면 |s| < ½ 에서 ∂N/∂x_p = −2s/Δx 인데 MLS 쪽은 −(3 − 4s²) s/Δx — 노드 바로 옆에서 **1.5 배**, s = ½ · 1 에서 같고, s = 1.25 에서 0.625 배다.  둘이 공유하는 것은 ① 합이 0 (Σ_i = 0 → 운동량 보존) ② 선형장을 정확히 재현 (Σ_i (대용 기울기)_i (x_i − x_p)ᵀ = I ← D_p M_p⁻¹ = I) 두 가지뿐이다 (세 노드 수치 확인).  ⇒ "MLS-MPM = 전통 MPM 의 빠른 구현" 이 아니라 **1차 일관성이 같은 다른 이산화**이고, 둘의 가까움은 논문에서 Fig. 17 과 눈 비교로만 확인됐다.

### 4-4. 변형구배 · 초탄성 힘 · 암시 적분 (§3.4–3.5, 식 17–19 · 보충 §2 · 그림 `eq_17_…` · `eq_18_19_…` · `eq_S05_S06_…` · `eq_S07_S10_…`)

- ∂F/∂t = (∂v/∂x) F.  전통 MPM: ∂v̂^{n+1}/∂x (x_pⁿ) = Σ_i v̂_i^{n+1} ∇N_i(x_pⁿ)ᵀ.  MLS 에서는 식 (8) 을 미분해 (선형 다항)
  > ∂v̂^{n+1}/∂x = C_p^{n+1}   그리고   **F_p^{n+1} = (I + Δt C_p^{n+1}) F_pⁿ**    (17)   — C_p^{n+1} 은 *"exactly the affine velocity matrix from APIC"*
- 초탄성 (전체 퍼텐셜 E = Σ_p V_p⁰ Ψ_p(F_p) · V_p⁰ = 초기 부피) 이면
  > **f_i = −∂E/∂x_i = −Σ_p N_i(x_pⁿ) V_p⁰ M_p⁻¹ (∂Ψ/∂F)(F_pⁿ) F_pⁿᵀ (x_iⁿ − x_pⁿ)**    (18)

  σ = (1/det F)(∂Ψ/∂F) Fᵀ · det(F) V_p⁰ = V_pⁿ 이므로 식 (16) 과 같다.
- 저자 결론: *"the MLS-MPM deformation gradient update and force computation directly re-use quantities from APIC and do not require any evaluation of the interpolation function gradient throughout the algorithm."* (p.150:7)
- **암시 적분** (Newton · [Gast et al. 2015]): 에너지 Hessian 의 작용
  > −δf_i = Σ_p V_p⁰ A_p F_pⁿᵀ M_p⁻¹ N_i(x_pⁿ)(x_iⁿ − x_pⁿ)    (19)   — A_p = ∂²Ψ/∂F∂F : Σ_j M_p⁻¹ N_j(x_pⁿ) δu_j (x_jⁿ − x_pⁿ)ᵀ F_pⁿ

  유도 (보충 §2): 힘을 가상으로 움직인 노드 위치 x_i = x_iⁿ + Δt v̂_i 의 함수로 두고 (보충 식 5), F_p(x_i) = (I + Δt C_p(x_i)) F_pⁿ (보충 6), C_p(x_i) = (Σ_i N_i(x_pⁿ) ((x_i − x_iⁿ)/Δt)(x_iⁿ − x_pⁿ)ᵀ) M_p⁻¹ (보충 7) 을 연쇄 법칙으로 미분 (보충 8 → 9 · 10).  실제로는 격자 → 입자 수집 (A_p) + 입자 → 격자 산란 (δf_i) 한 번씩.  (보충은 같은 상수를 D_p⁻¹ 로, 본문은 M_p⁻¹ 로 적는다.)

### 4-5. MLS-MPM 한 걸음 = 여섯 단계 (§4) + 융합 산란 Q_p (§6 · 그림 `eq_Qp_fused_p2g_scatter.png`)

1. **입자 → 격자** — APIC 또는 PolyPIC 로 질량 · 운동량.
2. **격자 운동량 갱신** — symplectic Euler (힘 = 식 18) 또는 backward Euler (힘 미분 = 식 19).
3. **격자 → 입자** — 속도와 아핀 (다항) 계수.
4. **입자 변형구배** — 식 (17).
5. **입자 소성** — 변형구배를 항복면으로 사상 (있으면).
6. **입자 이류** — 새 속도로 위치 갱신.

전통 MPM 과 다른 곳은 (2) 의 힘 식과 (4) 의 F 갱신뿐 (저자).  명시 적분에서는 (1) 과 (2) 가 한 번의 산란으로 합쳐진다:
> 노드 i 로 가는 기여 = N_i(x_pⁿ) Q_p (x_i − x_pⁿ),   Q_p = Δt V_p⁰ M_p⁻¹ (∂Ψ/∂F)(F_pⁿ) F_pⁿᵀ + m_p C_p    (인쇄 그대로 — p.150:11 · 보충 p.4)

안쪽 반복 (3D 2차 B-spline 이면 27 번) 마다 행렬–벡터 곱 하나.
⚠ **부호 [카드 산술]**: 식 (26) (m v̂)_i = (mv)_i + Δt (m_i g + f_i) 에 식 (18) 과 식 (24) 를 넣으면 (x_i − x_p) 에 걸리는 행렬은 **m_p C_p − Δt V_p⁰ M_p⁻¹ (∂Ψ/∂F) Fᵀ** 다.  인쇄된 Q_p 는 첫 항이 `+` 라 식 (18) · (26) 과 부호가 맞지 않는다 (본문 · 보충 두 곳 모두 `+`).  우리 코드는 `−` 다 (`st = (-dt * pm * 4 * inv_dx * inv_dx) * P`) [우리 코드 판독] — 인용할 때는 식 (18) · (26) 을 쓴다.

### 4-6. CPIC ① 색칠 거리장 (§5.2–5.3, 식 20–22 · 그림 `eq_20_…` · `eq_21_…` · Fig. 11–13)

*"rigid body"* = 동역학 강체 **또는** 운동이 지정된 강체 경계 (§5).  표기: p, q = MPM 입자 · r, s = 강체 · i, j = 노드.

**왜 부호 거리장 (SDF) 이 아닌가**: SDF 는 닫힌 표면의 안팎 · 법선에 편하지만 **교차하는 열린 경계**는 못 나타낸다.  그래서 *"unsigned distance d(x_i) and color information"* — 색이 '가까운 표면들의 집합' 과 '그 각각의 어느 쪽' 을 담아, 격자 한 장으로 여러 영역을 이산적으로 나타낸다 (p.150:8).  (더 정밀한 대안으로 저자가 든 것: [Xu and Barbič 2014] 의 거리장 · [Mitchell et al. 2015] 의 non-manifold level set.)

**격자 거리** (§5.2.1):
- 강체 표면 r 위에 보조 **강체 입자** r_1 … r_R 를 뿌린다 (요소 E(r_η) = 2D 선분 / 3D 삼각형 · 삼각형마다 간격 < Δx).
- 강체 입자마다 가장 가까운 노드와 주변 3 × 3 × 3 노드를 그 요소의 평면에 투영해 **점–평면 부호 거리** u_{i,r_η} 를 구한다.  투영점이 **요소 안**에 떨어질 때만 '유효' 로 저장 (점–평면 거리 = 점–요소 거리인 경우) (Fig. 11).
- d_i = min_{r,η} |u_{i,r_η}|.  함께 기록: 가장 가까운 강체 r\*(x_i) (임펄스를 줄 대상) · 강체 r 마다 가장 가까운 강체 입자 r_η\*(x_i) (어느 쪽인지 정할 때).
- 절충 (저자): 모서리 근처에 값이 빠지는 노드가 생기지만 점–메시 정확 거리보다 훨씬 싸다.

**격자 색** (§5.2.2): 친화 (가까움) 와 꼬리표 (쪽).
> A_ir = 1 (유효한 u_{i,r_η} 가 하나라도 있으면) · 0 (아니면)    (20)        T_ir = sign(u_{i, r_η\*(x_i)})

**입자 색 · 거리 · 법선** (§5.3):
- 친화 A_pr = 입자 핵 안 노드의 A_ir 를 물려받음.  꼬리표는 거리 가중 평균
  > T_pr = sign(Σ_i N_i(x_p) d_i T_ir)    (21)   — d_i 를 곱해, 표면에 바짝 붙어 부호가 애매한 노드의 영향을 줄인다
- 입자가 표면에 다가가면 핵 전체에 CDF 가 있다는 보장이 없고 뿌림도 모서리 노드를 놓치므로 d_i 를 그냥 보간하지 않는다 — 입자 · 노드의 꼬리표로 **부호를 맞춘 뒤** 식 (4) (MLS) 로 입자 거리 d_p 와 기울기 ∇d_p 를 재구성하고 **n_p = ∇d_p / |∇d_p|** (Fig. 12 e · f).
- **색 지속 + 벌칙력** (§5.3.3 · Fig. 13): 한번 얻은 (A_pr, T_pr) 은 핵 안 모든 노드가 r 과의 친화를 잃을 때까지 유지한다 — 입자가 이류 수치 오차로 표면을 살짝 넘어도 꼬리표를 뒤집지 않기 위해서다.  그러면 d_p 가 음수로 나오고, 그런 입자에
  > f_p^{P,n} = −k_h d_p n_p    (22)   — k_h = 벌칙 강성 (값 [미확인]) · *"weak penalty force"*
- **호환** (§5.3.4): S_i · S_p = 노드 · 입자가 친화를 가진 표면 집합.  *"A grid node i and a particle p are compatible if and only if for all surfaces shared by the particle and the grid node, all tags are the same (T_ir = T_pr, ∀r ∈ S_i ∩ S_p)."*

### 4-7. CPIC ② 호환 전달 · 경계 투영 · 임펄스 (§5.4–5.5, 식 23–28 · 그림 `eq_22_25_…` · `eq_26_28_…` · `eq_28b_…`)

i^{p+} / i^{p−} = 입자 p 와 호환 / 비호환인 노드 · p^{i+} / p^{i−} = 노드 i 와 호환 / 비호환인 입자.

**입자 → 격자 — 호환 노드에만**:
> m_iⁿ = Σ_{q∈{p^{i+}}} N_i(x_qⁿ) m_q    (23)        (mv)_iⁿ = Σ_{q∈{p^{i+}}} N_i(x_qⁿ) m_q (v_qⁿ + C_qⁿ (x_i − x_qⁿ))    (24)

**경계 투영 연산자** — 강체의 그 자리 속도 V_rⁿ(x) = v_rⁿ + ω_rⁿ × (x − x_rⁿ), 그리고 입력 속도 v · 법선 n · 경계 유형 B · 마찰 μ 에 대해
> Proj(v, n, B, μ) = 0 (B = sticky) · v_t (B = slip) · ζ v̂_t (B = separate 이고 v·n ≤ 0) · v (B = separate 이고 v·n > 0)    (25)
> ζ = max(0, |v_t| + μ v·n) · v_t = v − (v·n) n · v̂_t = v_t / |v_t| · μ ≥ 0 = *"the dynamic friction coefficient"*

| 유형 | 강체 기준 상대 속도에 하는 일 | 뜻 [카드 판독] |
|---|---|---|
| sticky | 전부 0 | 붙음 (강체와 같이 움직임) |
| slip | 법선 성분 제거 (부호와 무관) · 접선 그대로 | 마찰 없는 미끄럼 · **떨어지지 못함** |
| separate, 다가옴 (v·n ≤ 0) | 법선 제거 · 접선 크기를 μ‖v_n‖ 만큼 줄임 (0 아래로는 안 감) | Coulomb 동마찰 미끄럼 / 붙음 |
| separate, 멀어짐 (v·n > 0) | 그대로 | **자유 분리** |

- n_p 는 표면에서 입자 쪽을 향한다 (d_p < 0 일 때 식 22 가 입자를 +n_p 로 민다) [카드 판독] — 그래서 v·n ≤ 0 이 '다가옴'.
- 대조 [카드 산술]: separate 의 두 줄은 Bardenhagen 2000 식 (23) ṽ = v − [(v − v_cm)·n](n + μ′ n × ω̂), μ′ = min(μ, 붙임 비) 와 **같은 보정**이다 — ζ v̂_t = v_t − min(μ‖v_n‖, ‖v_t‖) v̂_t.  기준 속도만 질량중심 속도장 → 강체 속도 V_r 로 바뀌었다.  분리 판정은 **속도만** 본다 (2001 개정판의 견인력 판정은 없다).
- |v_t| = 0 일 때의 v̂_t 처리는 인쇄 없음 [미확인].

**강체로 가는 임펄스**: 입자 p · 강체 r 에 대해 비호환 노드로 갈 속도 기여를
> Proj_r(v_pⁿ, n_p, x_i) = V_rⁿ(x_i) + Proj(v_pⁿ − V_rⁿ(x_i), n_p, B_r, μ_r)

로 투영하고, *"each incompatible grid node j ∈ i^{p−} results in an impulse m_p (v_pⁿ − Proj_{r\*}(v_pⁿ, n_p, x_j)) N_j(x_pⁿ) applied to the closest rigid body r\*(x_j) (tracked in §5.2.1) at x_j."* (p.150:10)
- 힘이 넘어가는 길은 이것 하나 (+ 벌칙 임펄스) 다 — 견인력을 표면에서 적분하지 않고 **막힌 운동량**을 임펄스로 준다.  토크는 "x_j 에 건다" 는 말로만 있고 식은 없다 — 강체 동역학의 통상 처리로 (x_j − x_r) × J 가 되리라는 것은 [카드 추론].
- 입자의 아핀 항 C_p (x_j − x_p) 는 임펄스 식에 없다 (v_pⁿ 만) [카드 판독].
- 접촉은 표면이 실제로 닿을 때가 아니라 **입자 핵이 표면 건너편 노드에 닿는 순간** (2차 B-spline 이면 표면에서 ≈ 1.5 Δx 안) 부터 걸린다 [카드 추론] — §8 의 *"only resolves features at a scale of grid Δx"* 와 같은 뜻.

**격자 갱신** (symplectic Euler):
> (m v̂)_i^{n+1} = (mv)_iⁿ + Δt (m_iⁿ g + f_iⁿ)    (26)   → v̂_i^{n+1} = (m v̂)_i^{n+1} / m_iⁿ   — f_iⁿ = 식 (18)

(식 18 의 합이 호환 입자로 제한되는지는 따로 적혀 있지 않다 — Q_p 로 융합해 산란하면 호환 노드에만 간다 [카드 추론].)

**격자 → 입자 — 유령 속도**: 비호환 노드의 속도는 그 입자와 무관하므로 입자 자신에서 상수로 외삽한 값을 쓴다.
> v_p^{n+1} = Σ_{j∈i^{p−}} N_j(x_pⁿ) ṽ_p + Σ_{j∈i^{p+}} N_j(x_pⁿ) v̂_j^{n+1}    (27)
> C_p^{n+1} = D_p⁻¹ (Σ_{j∈i^{p−}} N_j(x_pⁿ) ṽ_p z_{jp}ⁿᵀ + Σ_{j∈i^{p+}} N_j(x_pⁿ) v̂_j^{n+1} z_{jp}ⁿᵀ)    (28)   — z_{jp}ⁿ = x_j − x_pⁿ

- *"Here we include ghost velocities on incompatible nodes to prevent potential singularity of D_p."*
- **충돌한 입자 속도** ṽ_p = Proj_r(v_pⁿ, n_pⁿ, x_j) + Δt c n_p — r = 입자에 가장 가까운 강체 경계, c = *"non-zero when there is need to push the particle away from the boundary"* (값 · 기준 [미확인]).  (본문 문장은 "v_j = v_pⁿ 로 상수 외삽" 이라 쓰고 식 27 · 28 은 ṽ_p 를 쓴다 — 식을 따른다 [카드 판독].)
- 이어서 x_p^{n+1} = x_pⁿ + Δt v_p^{n+1} · F_p^{n+1} = (I + Δt C_p^{n+1}) F_pⁿ · 벌칙 임펄스 Δt f_p^{P,n} 을 입자에, 반대 임펄스를 강체에 (*"for conservation of momentum"*).

### 4-8. 강체 쪽 (§5.1 · §5.6)

- **강체–강체 충돌 · 관절** (§5.1): *"It is independent from our MPM algorithm, and any external rigid body dynamics package can be used.  We will skip the details"* — 걸음 처음에 v_rⁿ → v_r\*, ω_rⁿ → ω_r\* (중간값).
- **강체 갱신** (§5.6): §5.4 의 임펄스로 v_r^{n+1} ← v_r\*, ω_r^{n+1} ← ω_r\* 를 갱신하고 *"the rigid bodies are advected in a standard way"*.
- 결합은 **한 걸음 안에서 번갈아 푸는 약결합**이다: *"Fully implicit rigid-MPM strong coupling is not formulated in this work and we leave that as future work."* (§8)

### 4-9. 의사코드 — CPIC 한 걸음 (우리 전사 · Fig. 10 의 1–7 · 논문에 이 꼴로는 없음)

```
# (논문 식 번호) · [카드 판독/추론] 표시
1  강체–강체 충돌 · 관절 → v_r*, ω_r*                         (§5.1 · 외부 강체 해법)
2  강체 표면 → 강체 입자 r_η (간격 < Δx)
   r_η 마다: 가장 가까운 노드 + 주변 3×3×3 노드에 점–평면 부호 거리 u (투영이 요소 안일 때만 유효)
   노드: d_i = min|u| · r*(x_i) · A_ir (20) · T_ir = sign(u_{i,r_η*})
3  입자: A_pr ← 핵 안 노드의 A_ir · T_pr = sign(Σ N_i d_i T_ir) (21)  — 한번 얻으면 유지 (§5.3.3)
        부호를 맞춘 격자 거리 → MLS (4) → d_p, n_p = ∇d_p/|∇d_p|
        d_p < 0 이면 벌칙력 f_p^P = −k_h d_p n_p (22)
4  입자 → 격자:
     호환 노드 i ∈ i^{p+}: 질량 · 운동량 (23)(24) [+ 힘: Q_p 융합 — 카드 추론]
     비호환 노드 j ∈ i^{p−}: J = m_p (v_p − Proj_{r*}(v_p, n_p, x_j)) N_j(x_p) 를 강체 r*(x_j) 의 x_j 에
   격자: (m v̂)_i = (mv)_i + Δt (m_i g + f_i) (26) · v̂_i = (m v̂)_i / m_i
5  격자 → 입자: 호환 노드는 v̂_j, 비호환 노드는 유령 속도 ṽ_p = Proj_r(v_p, n_p, x_j) + Δt c n_p  (27)(28)
        F_p ← (I + Δt C_p) F_p (17) → 소성 사상
        벌칙 임펄스 Δt f_p^P → 입자, 반대 임펄스 → 강체
6  x_p ← x_p + Δt v_p
7  강체: 받은 임펄스로 v_r, ω_r 갱신 → 강체 이류                 (§5.6)
```

### 4-10. 고성능 구현 (§6 · 보충 §3)

- 목표 셋 (보충 p.4): ① 메모리 대역폭 소비 줄이기 ② FPU 이용률 올리기 ③ 구현을 단순하게.
- **SPGrid** [Setaluri et al. 2014] 희소 격자 (Morton 부호 + TLB) · 블록 4 × 4 × 8 · 블록마다 덧댄 지역 격자 (6 × 6 × 10) 를 L1 캐시에 올려 전달 (**blocked transfer**) · P2G 뒤에만 되써 넣음.
- **강체 경계 입자가 있는 블록과 없는 블록에 다른 커널** — 분기를 입자 수준에서 블록 수준으로 올린다.  CPIC 는 경계 근처 좁은 띠에만 필요하고 블록의 ≈ 90 % 는 보통 MLS-MPM 전달 (보충 p.5).
- **잠금 없는 다중 스레드**: 블록 좌표의 홀짝으로 묶음을 나눠 (2D 4 · 3D 8 묶음) 같은 묶음 안에서는 두 블록이 같은 전역 노드에 쓰지 않게 한다 (*"eight-colored P2G"*).
- 저수준: CPU intrinsics 를 직접 씀 (정렬 문제로 컴파일러 자동 벡터화에 기대지 않음) · FMA (a × b + c) · 4 개 float 벡터의 남는 한 칸에 질량 · 27 번 반복을 손으로 풀어 씀.

### 4-11. ★ 입자 처리 (DEM 의 "무질서 처리" 대응)

| 축 | 이 논문 |
|---|---|
| 재료 표현 | **연속체** — 물질점은 알갱이가 아니라 구적점이다.  모래도 Drucker–Prager 연속체 (알갱이 없음) |
| 형상 | 메시에서 채운 임의 형상 (토끼 · 아르마딜로 · 바나나 …) — 입자 크기 분포 개념 없음 |
| 소성 표현 | **진짜 형상 소성** (von Mises · Drucker–Prager 반환 사상 — 식은 인용 논문에) |
| 변형체–변형체 접촉 | **없음** — 닿으면 한 속도장 (붙음 · 합쳐짐).  저자: MPM 은 *"automatically supports … material split and merge"* |
| 변형체–강체 접촉 | CPIC — sticky / slip / separate + μ · 양방향 임펄스 · Δx 해상 |
| 강체 | 표면 메시 (얇은 껍질 · 열린 면 · 교차 면 가능) · 강체끼리는 외부 해법 |
| 파괴 · 절단 | 강체 표면이 지나간 자리의 **운동학적 분리** (재료 파괴 기준 없음 · 미리 정한 절단면) |
| 무작위성 | 벤치마크는 셀당 8 개 균일 · 예제의 입자 배치 · 시드 [미확인] |

---

## 5. 결과 — 절별

### 5-1. MLS-MPM ↔ 전통 MPM (§6–§7 · Table 2 · Fig. 17)

- 눈으로: *"MLS-MPM produces visually comparable dynamics with traditional MPM."*
- 에너지: 두 초탄성 시험에서 곡선이 거의 겹친다 (§3-3 — 최대 차 0.018 · 0.010 [판독]).  두 방법 모두 에너지가 준다 (젤 ≈ 85 % · 공 ≈ 26 % [카드 산술]).
- 속도: 전달 연산이 알고리즘만으로 ≈ 2 배 (§3-1), 저수준 최적화까지 합치면 참조 구현 대비 P2G 3.71× · G2P 14.01×.
- 구현: *"MLS-MPM can be easily imported to any existing MPM solvers with APIC/PolyPIC transfers."*

### 5-2. 절단 — 변위 불연속 (Fig. 1 · 2 · 3 · 4 · 7)

- **Fig. 2 (2D · 왜 필요한가)**: (a) 수준집합 충돌체를 노드 한 층 두께 (1 Δx) 로 넣어도 탄성체가 안 잘린다 — 그림에서 sticky 는 블록이 충돌체에 끌려 한쪽으로 기울고, slip 은 충돌체가 블록 속에 들어가 있는데도 갈라지지 않는다 [판독].  (b) 소성 연화 (2 Δx 띠) 는 분리는 되나 잔해 입자가 흩어진다.  (c) 입자 삭제 (1 Δx · 1.5 Δx) 는 안 잘리거나 부피를 잃는다.  (d) CPIC 는 점진 절단 · 즉시 절단 모두 깨끗하다.  저자 진단: 입자 핵이 경계와 맞지 않아 (*nonconforming*) 경계 너머 노드와 자료를 주고받고, 고체에 필요한 2차 · 3차 B-spline 의 넓은 핵 때문에 FLIP 유체보다 더 심하다.
- **Fig. 7 아르마딜로**: 늘려 둔 탄성체를 두 번 차례로 자른다 (1.3 M · Δt 5 × 10⁻⁶ — 표에서 가장 작은 걸음).  **Fig. 4 토끼**: 교차하는 얇은 판 두 장으로 넷으로.  **Fig. 1 바나나 · Fig. 3 치즈**: von Mises 소성체 절단 — 치즈는 물결 칼에서 *"appealing peeling behavior"*.
- 한계 (저자): *"it is hard to reconstruct sharp cutting surfaces from particles"* (§8).

### 5-3. 얇은 경계 (Fig. 5 · 9 · 15)

- **Fig. 9 모래 젓기** (5.2 M): 얇은 판 두 장 — *"Materials from opposite sides experience independent dynamics even with the use of a single shared background grid."*
- **Fig. 15 모래 쓸기** (2.6 M · Δx 2.0 × 10⁻³ = Sand paddles 와 함께 표에서 가장 고운 격자 · 288.3 sec/frame = 가장 느림): 운동이 지정된 얇은 껍질.
- **Fig. 5 모래 바퀴 (2D)**: 교차하는 얇은 경계로 만든 바퀴 — 칸마다 재료가 깨끗이 갈리고, 두 시점의 그림에서 바퀴가 모래에 밀려 돌아가 있다 [판독].

### 5-4. 강체 양방향 결합 (Fig. 1 · 6 · 8 · 14)

- **Fig. 8 젤 + 강체 블록**: 밀도 400 · 2000 · 5000 블록 (그림 안 표지) 을 von Mises 젤 (ρ 400 · E 5 × 10⁴ · 항복 10) 에 떨어뜨림 — 그림에서는 무거운 블록일수록 깊이 박혀 있다 [판독 · 정성].
- **Fig. 6 부력**: 밀도 다른 강체 블록과 튀는 물 (5.3 M).  **Fig. 14 모래 패들**: 수직 모래 흐름이 강체 패들 넷을 돌린다.  **Fig. 1 물레방아**: 유입 속도 · 바퀴 밀도 세 조합.
- 어느 것도 힘 · 토크 · 침강 깊이 · 회전 속도의 **수치 대조가 없다** — *"Two-way coupling with rigid bodies is naturally supported, and shown by …"* 가 전부다.

### 5-5. 로봇 — 유일한 실험 대조 (Fig. 16 · 보충 §4)

- *"we simulate and validate locomotion for robot navigating in granular media"* · 캡션 *"our simulation results (top) match real world footage (bottom) on different motion patterns"*.
- 실험 (보충 p.5): [Li et al. 2013] 의 로봇 (RoboXplorer, Smart Lab) 몸체 + ABS 3D 프린트 다리 6 개 (길이 2R = 4.1 cm · 폭 1.0 cm · 두께 0.3 cm · 곡률 1/r = [−1, 1]/R 두 가지) · 번갈아 세 다리 걸음 (1 자유도 회전) · 모터 4.5 V · 배 면적 13 × 2 cm² · 전체 85 g · 트랙 180 × 40 cm · 고운 모래 깊이 8 cm · 카메라 2 대 (앞 · 위) 30 FPS.
- 시뮬 (Table 3): 3.4 M 입자 · ρ 2000 · E 1.8 × 10⁶ · 마찰각 45 · 112.4 / 116.8 sec/frame.
- ⚠ 대조는 **영상의 운동 양상** (다리 곡률 두 가지 = Table 3 의 Robot · Robot (reverse) 두 줄) 이고, 이동 거리 · 속도 · 침하 깊이 · 힘의 수치 비교는 없다.  모래의 재료값을 어떻게 정했는지도 없다 [미확인].

### 5-6. 한계와 향후 (§8)

저자 원문은 §11 표에.  향후로 든 것: 고차 다항 공간 (고차 MPM) · 다중선형 핵의 cell-crossing 오차 줄이기 (*"While traditional MPM readily goes unstable in this case, MLS-MPM provides possible solutions due to its freedom in choosing the function space and weighting functions"*) · 공간 적응 [Gao et al. 2017] (MLS 는 규칙 격자가 필요 없다) · power diagram · 메시 기반 해법 (천) 과의 CPIC 결합.

---

## 6. 그림별 (원 캡션 요지 + MPM 관점)

> 파일 = `litdb/figures/hu2018_mls_mpm_cpic_two_way_rigid_coupling/` · 300 dpi · 그림 17 + 표 3 = 도구 자동 크롭 (Fig. 8 한 장만 다시 자름) · 식 그림 17 장은 손 크롭.  MPM 관점의 [카드 추론] · [우리 코드 판독] 표지는 논문 밖 판단이다.

| 그림 | 파일 | 원 캡션 요지 | MPM 관점 (우리 MPM · 재설계 후보) |
|---|---|---|---|
| 1 | `fig_1.png` | 방법이 가능하게 한 것 — 세계 좌표에서의 절단 (바나나) · 복잡한 얇은 경계 · 강체 양방향 결합 (물레방아 셋) | 강체 (칼 · 바퀴) 는 표면 메시로 들어가고 재료가 그 양쪽에서 따로 움직인다.  바퀴가 유체 힘으로 **돌아가는** 것이 후보 A (AM 이 SE 에 밀려 움직임) 의 시연 원형 — 단 수치 대조 없음.  그림 안 표지: Inflow speed 0.5 / 1.0 / 0.5 · Wheel density 1.0 / 4.0 / 4.0 [판독] |
| 2 | `fig_2.png` | 2D 절단 비교 — (a) 1 Δx 두께 수준집합 충돌체 (sticky · slip) 는 못 자른다 (b) 2 Δx 소성 연화 = 잔해 (c) 1 · 1.5 Δx 입자 삭제 = 안 잘리거나 부피 손실 (d) 제안 방법 | ★ (a) 가 우리 AM 마스크 · 판과 **같은 종류의 경계 처리** (격자 노드에 조건) 다.  입자 핵 (2차 B-spline · 3 셀) 이 경계 너머 노드와 자료를 주고받아 속도장이 뭉개진다는 저자 진단은, AM 표면에서 핵 반폭 ≈ 1.5 dx ≈ 0.21 µm (dx 0.141 µm) 안의 SE 가 AM 속도 (0) 에 끌린다는 뜻 — SE 지름 1 µm 의 ≈ 21 % [카드 산술 · 카드 추론] |
| 3 | `fig_3.png` | 물결 칼로 치즈 자르기 — 벗겨지는 거동 | von Mises 소성체 + 강체 표면의 미끄럼 · 분리 (정성).  E/σ_y = 4 × 10⁴ [카드 산술] 인 거의 강소성 영역 — 우리 생산 설정 (≈ 5.1) 과 다른 영역이라 소성 거동의 닮음을 기대할 근거가 못 된다 |
| 4 | `fig_4.png` | 교차하는 얇은 판 두 장으로 탄성 토끼를 가름 | 교차 표면 = 강체 (표면) 마다 2 비트인 색의 조합으로 네 영역.  '한 노드 가까이에 강체가 둘' 인 경우 (우리 AM–AM 근접) 의 색 조합 선례 — 단 판은 얇고 열린 면, AM 은 닫힌 두꺼운 구 |
| 5 | `fig_5.png` | 2D 모래 유입이 바퀴와 양방향 결합 — 교차하는 얇은 경계로 만든 바퀴가 면 · 모서리 양쪽 재료를 깨끗이 가름 | 4.1K 입자 · 0.3 sec/frame — 2D 에서 빨리 도는 회귀 시험 꼴 (계획의 단계 2).  입자 색 = 어느 칸에 속하는지 |
| 6 | `fig_6.png` | 튀는 물과 밀도 다른 강체 블록의 양방향 결합 | 힘 전달의 시연이지만 부력 · 침강의 수치 대조가 **없다** → 후보 A 의 힘 전달 정확도는 이 논문으로 보증되지 않는다.  해석해가 있는 단위 시험 (정지 부력 = 배제 부피 × ρ g 등) 으로 직접 확인할 것 [카드 추론] |
| 7 | `fig_7.png` | 처음에 늘려 둔 탄성 아르마딜로를 두 번 차례로 절단 | 예응력 상태에서 자르면 되튄다 — 불연속이 응력 전달을 실제로 끊는다는 정성 증거.  '하중이 풀리며 떨어지는' 장면이 나오는 유일한 그림이나 되돌아온 양의 수치는 없다 |
| 8 | `fig_8.png` | 탄소성 von Mises 젤 블록이 밀도 비가 다른 강체 블록과 양방향 결합 | ★ 후보 A 에 가장 가까운 시연 = 소성 연속체에 무거운 강체가 눌러 박힘 (그림 안 표지: 블록 400 · 2000 · 5000 · 젤 400 [판독]).  그러나 하중은 중력이고 우리처럼 판이 미는 준정적 고압 압축이 아니며, 박힌 깊이의 수치 · 해석 대조가 없다.  (자동 크롭이 위 문단의 식 8–9 를 삼켜 다시 자름) |
| 9 | `fig_9.png` | 얇은 판 두 장으로 마른 모래 그릇 젓기 — 한 장의 공유 배경 격자로도 양쪽 재료가 독립 운동 | ★ "격자 한 칸 = 속도 하나" 를 넘는 방식의 시연 — 장을 늘리지 않고 **노드를 면의 한쪽에만 배정**한다.  단 면은 강체 메시다; SE–SE 처럼 변형체끼리의 경계에는 쓸 수 없다 |
| 10 | `fig_10.png` | MLS-MPM + CPIC 의 한 걸음 — (1) 강체–강체 (2) 강체 → 격자 CDF (3) 격자 → 입자 CDF (4) CPIC 입자 → 격자 + 강체 임펄스 (5) CPIC 격자 → 입자 (6) 입자 이류 (7) 강체 이류 | 우리 `substep()` 에 없는 단계 = 1 · 2 · 3 · 4 의 임펄스 · 7.  후보 A 구현의 점검표 |
| 11 | `fig_11.png` | 선분 위 강체 입자 하나가 노드 9 개에 부호 없는 거리장을 뿌림 — 투영이 요소 **안**일 때만 유효 | 얇고 열린 표면을 위한 장치.  구형 AM 은 해석적 부호 거리 (‖x − c‖ − R) 로 대신할 수 있어 이 뿌림 · 색이 필요 없다 [카드 추론] |
| 12 | `fig_12.png` | 교차하는 얇은 강체 경계 셋 (2D): (a) 표면 (b) 격자 거리 (c) 격자 색 (d) 입자 색 (e)(f) MLS 로 재구성한 입자 거리 · 법선 | 색 · 거리가 경계 ±1–2 셀의 좁은 띠에만 있다 = CPIC 비용이 띠에만 든다.  조밀한 복합 양극에서는 AM 표면 띠가 SE 영역의 큰 몫을 차지할 수 있다 — 비용 · 정확도 모두 '좁은 띠' 가정이 약해진다 [카드 추론] |
| 13 | `fig_13.png` | 이류 수치 오차로 경계를 살짝 넘은 입자 — 색 (A_pr, T_pr) 과 법선 n_p 를 유지하고 재구성 거리가 음수 → 약한 벌칙력 | 속도 투영만으로는 침투가 0 이 되지 않는다는 저자 스스로의 기록.  k_h 값은 미인쇄.  A′-0 · A 에서도 침투량 (d_p 분포) 을 재서 보고해야 한다 [카드 추론] |
| 14 | `fig_14.png` | 수직 Drucker–Prager 모래 흐름이 강체 패들 넷과 양방향 결합 | 강체가 재료 흐름에서 토크를 받아 돈다 — "임펄스를 x_j 에 건다" 의 시연 (토크 식은 미인쇄 · 회전 속도 수치 없음) |
| 15 | `fig_15.png` | 운동이 지정된 얇은 껍질로 모래 더미 쓸기 | '운동 지정 강체' = 우리 판 (플래튼) 과 같은 종류.  판을 이 틀의 강체로 두면 분리 (separate) 와 마찰 μ 가 같은 식 (25) 에서 나온다 — A′-0 |
| 16 | `fig_16.png` | 강체–MPM 결합으로 모래 위 다리 로봇 보행 예측 — 위 = 시뮬 · 아래 = 실제 영상 · [Li et al. 2013] 모델을 3D 프린트 | 이 논문의 **유일한 실험 대조** — '운동 양상이 맞는다' 는 영상 비교이고 거리 · 속도 · 힘의 수치가 없다.  정량 검증으로 인용 금지 |
| 17 | `fig_17.png` | 진동하는 젤 (좌) · 충돌하는 공 (우) 의 전체 에너지 — MLS-MPM 과 전통 MPM 의 수치 소산이 거의 같다 | ★ 유일한 정량 검증이고 **두 이산화끼리의 비교**다 (끝값 0.329 ↔ 0.311 · 0.508 ↔ 0.517 [판독]).  두 방법 모두 에너지를 크게 잃는다 (젤 ≈ 85 %) = 전달의 수치 소산 — 준정적 가압에는 감쇠로 작용하나 되튐 · 응력파에는 영향을 준다 [카드 추론] |
| Table 1 | `tab_1.png` | MLS-MPM 유도 (§3) 의 기호표 | 기호 대조용.  ρ(x, t) 의 '형' 이 vector 로, v̂ 의 위첨자가 n 으로 인쇄돼 있다 (본문은 스칼라 · n + 1) [카드 판독] |
| Table 2 | `tab_2.png` | MPM 전달 연산 벤치마크 (ms) — 참조 구현 ↔ 저자 MPM ↔ 저자 최적화 MPM ↔ 저자 최적화 MLS-MPM | 알고리즘 몫 ≈ 2 배 (2.09× · 1.94× [카드 산술]) 가 우리 코드가 물려받은 이득.  CPU · SPGrid 수치라 GPU 커널 시간과는 무관 |
| Table 3 | `tab_3.png` | 예제별 sec/frame · Δx · Δt · 입자 수 · 밀도 · 영률 · 체적계수 · 항복응력 · 마찰각 (ν 0.3 공통) | 단위 미인쇄 · 프레임 길이 미인쇄.  1.0–5.3 M 입자가 4 코어 CPU 에서 16.7–288.3 sec/frame — 우리 GPU 런 (10⁷–10⁸ 물질점 [우리 기록]) 과 규모가 다르다 |

**식 그림 (손 크롭 · 텍스트 층이 온전하므로 전사 확인용)**: `eq_01_04_mls_reconstruction.png` · `eq_05_07_governing_weak_form.png` · `eq_08_11_momentum_term_lumped_mass.png` · `eq_12_stress_term_test_function.png` · `eq_13_16_mlsmpm_nodal_force.png` · `eq_17_deformation_gradient_update.png` · `eq_18_19_hyperelastic_force_differential.png` · `eq_20_grid_affinity.png` · `eq_21_tag_storage_particle_color.png` · `eq_22_25_penalty_compatibility_cpic_p2g_projection.png` · `eq_26_28_impulse_grid_update_cpic_g2p.png` · `eq_28b_collided_velocity_penalty_impulse_rigid_advection.png` · `eq_Qp_fused_p2g_scatter.png` · 보충: `eq_S01_S03_apic_as_mls.png` · `eq_S04_moment_matrix_Dp.png` · `eq_S05_S06_force_on_fictitious_positions.png` · `eq_S07_S10_force_differential_derivation.png`.

---

## 7. Post-processing

| 무엇 | 어떻게 | 우리에게 |
|---|---|---|
| 전체 에너지 – 시간 | 두 이산화의 곡선을 한 축에 겹침 (Fig. 17) | 이산화를 바꿀 때 (전달 방식 · 접촉 규칙) 의 회귀 시험 꼴 — 단 기준 (해석해 · 에너지 보존) 도 같이 그려야 한다 [카드 추론] |
| 전달 연산 시간 | P2G · G2P 를 1 · 4 스레드로 따로 재고 참조 구현 대비 배수로 표 (Table 2) | 우리 커널 프로파일의 보고 꼴 |
| FPU 이용률 | Intel VTune | — |
| 예제 통계 | sec/frame · Δx · Δt · 입자 수 · 재료값을 한 표로 (Table 3) | 런 표의 최소 열 — 여기에 **단위 · 프레임 길이 · 적분 방식**을 더해야 재현된다 (이 논문에 빠진 것) |
| CDF 시각화 | 격자 거리 · 격자 색 · 입자 색 · 입자 거리 · 법선을 나란히 (Fig. 12) | 강체 결합을 넣으면 같은 진단 그림 |
| 실험 대조 | 시뮬 렌더와 실제 영상을 위아래로 (Fig. 16) | 정성 대조의 꼴 — 우리는 SEM 단면 대조에 수치 (기공 · 두께) 를 같이 둔다 |
| 도구 | Taichi [Hu 2018] · SPGrid · gcc 5.4.1 · Intel VTune · 렌더러 [미확인] | — |

---

## 8. 우리 DEM + MPM 대비

### 8-1. 정면 비교

| 축 | Hu 2018 | 우리 DEM (LIGGGHTS) | 우리 MPM (Taichi scaffold) |
|---|---|---|---|
| 이산화 | MLS-MPM · APIC/PolyPIC · 2차 B-spline (3차도 유도) · 명시 / 암시 | 구 입자 · 접촉 법칙 | **같은 MLS-MPM** — APIC · 2차 B-spline · 명시 · f32 [우리 코드 판독] |
| 재료 | fixed corotated 탄성 · StVK + von Mises · StVK + Drucker–Prager · 약압축성 물 | hooke/hysteresis (탄성 + 이력) | fixed corotated 응력 + Hencky 변형률 J2 반환 [우리 코드 판독] |
| 변형체–변형체 접촉 | 없음 (한 속도장 — 붙음 · 합쳐짐) | 있음 (마찰 · 분리) | 없음 (한 속도장 — 붙음) |
| 변형체–강체 경계 | CPIC — 표면 메시 · sticky / slip / separate + μ · **양방향** 임펄스 · 유령 속도 · 벌칙 | 판 · 벽 메시 | 격자 노드 조건 — AM 0 (붙음) · 판 양방향 고정 · 바닥 / 옆벽 한쪽 · 마찰 0 · **일방** (반력은 재기만) |
| 불연속 | 강체 표면 양쪽 (Δx 해상) | 입자마다 | 없음 |
| 강체 운동 | 임펄스로 병진 · 회전 (강체끼리는 외부 해법) | 판은 지정 운동 | AM 고정 · 판 지정 / 서보 |
| 차원 · 규모 | 3D 1.0–5.3 M 입자 (CPU 4 코어) · 2D 4.1K | 3D 10⁴–10⁵ 입자 | 3D 10⁷–10⁸ 물질점 (GPU) [우리 기록] |
| 하중 | 중력 · 지정 운동 | 300 MPa 압축 | 300 MPa 급 압축 |
| E/σ_y | 5 × 10³ – 8 × 10⁴ [카드 산술] | — | ≈ 5.1 (E 1.53 · σ_y 0.30 GPa) [우리 기록] |
| 검증 | 에너지 곡선 2 (이산화끼리) · 로봇 영상 1 (정성) | 실험 기공 · 접촉 겹침 | 실험 기공 (보정) · DEM 두께 대조 |
| 탈압 | 없음 | 있음 | 부분 |
| 수송 (σ) | 없음 | 접촉망 | 복셀 (STEP3) |

### 8-2. 우리 경계를 식 (25) 로 읽으면 [우리 코드 판독 · `scripts/mpm3d_compaction.py` 2980–3003 행]

| 우리 경계 | 코드 | 식 (25) 의 유형으로는 | 빠진 것 |
|---|---|---|---|
| AM 마스크 노드 | `grid_v[I] = 0` (2990) | **sticky** (정지 강체) — 격자 노드에 건 옛 방식 | 미끄럼 · 분리 · AM 운동 |
| 판 (플래튼) | `if k * dx > wall_z: grid_v[I][2] = wall_vel` (2996–2998) | **slip** (법선 상대 속도를 양방향으로 0 · 접선 자유) | **분리** — 판이 물러날 때도 판 위 노드가 판 속도를 받는다 · 마찰 |
| 바닥 | `if k * dx < FLOOR and grid_v[I][2] < 0: grid_v[I][2] = 0` (2995) | **separate, μ = 0** | 마찰 |
| 옆벽 (주기 경계가 아닐 때) | 3000–3003 | **separate, μ = 0** | 다이 벽 마찰 |
| (선택) `SE_AM_DRAG` | `grid_v[I] *= max(0, 1 − SE_AM_DRAG * am_near[I])` (2992–2993) | 식 (25) 에 없는 임의 감쇠 | — |

- 우리 코드는 **강체에 줄 임펄스를 이미 센다**: 판 반력 `wallf += grid_m[I] * (grid_v[I][2] − wall_vel)` (2997) = 판이 막은 운동량 Σ m_i (v_i − V_판) 이고, 얼린 AM 이 받아낸 운동량도 `amf_dn` · `amf_up` 으로 잰다 (2983–2989 — 주석 "측정 전용").  이 논문의 임펄스 (비호환 노드로 갈 운동량 − 투영된 운동량) 의 **격자 노드판**이다.  ⇒ 후보 A 는 새 물리를 지어내는 것이 아니라 **지금 버리는 그 임펄스를 AM 강체 운동에 돌려주는 것**이다 [카드 추론].
- 차이: 이 논문은 조건을 노드가 아니라 **입자–노드 쌍** (호환 여부) 에 걸고 비호환 노드에 유령 속도를 쓴다.  우리처럼 강체 안쪽 노드에 조건을 걸면 Fig. 2 (a) 가 보이는 뭉개짐 (핵이 경계를 넘어 섞임) 이 남는다 — AM 은 두꺼워서 '안 잘림' 문제는 없지만 **표면에서 핵 반폭 안의 SE 는 AM 속도에 묶인다** [카드 추론].

### 8-3. 전이되는 것 / 안 되는 것

- ✅ **이산화 식 전부** (식 1–19 · 보충 1–10) — 재료 무관.  우리 코드의 줄 단위 대응 (§0 표).
- ✅ **경계 투영 연산자** (식 25) 와 임펄스 · 유령 속도의 틀 — A′-0 · A 의 부품.
- ✅ **비용 비율**: MLS-MPM ≈ 전통 MPM 의 ½ (전달 연산) · CPIC 덧비용 ≈ 6 % (강체 띠가 좁을 때).
- ✅ **저자가 스스로 그은 선**: Δx 규모까지만 해상 · 좁은 틈 · 뾰족한 모서리 불가 · 약결합 · 선형 기저.
- ❌ 재료값 · sec/frame · 에너지 곡선의 수치 — 그래픽스 재료 · CPU · 단위 미인쇄.
- ❌ "검증됨" 이라는 지위 — 이 논문은 MLS-MPM 의 정량 정확도 (응력 · 반력 · 수렴) 를 보이지 않는다.  우리 판 반력 (wallP) · 기공률의 수치 신뢰는 이 논문에서 빌려올 수 없다.
- ❌ 변형체끼리의 접촉 (A′) — 다루지 않는다.
- ⚠ CPIC 덧비용 6 % · "블록 90 % 는 보통 전달" 은 강체가 몇 개뿐인 장면의 값이다.  AM 수백 개가 부피의 절반 가까이를 차지하는 침대에서는 띠가 좁지 않다 [카드 추론].

### 8-4. frame 판정

- **frame [5] (분업)**: 이 논문은 MPM 쪽 (형상 소성) 에 **강체와의 접촉 자유도**를 더한다 — DEM 고유로 둔 "AM 이 움직이며 하중을 나눠 짐 (R1)" 의 일부를 MPM 틀로 가져올 길.  그러나 AM–AM 접촉은 *"any external rigid body dynamics package"* 로 밀려나 있어, 후보 A 는 결국 **SE = MPM · AM–AM = 강체 접촉 해법 (DEM 접촉 법칙) · AM–SE = 이 논문의 투영 / 임펄스** 세 조각의 결합이 된다 [카드 추론].  수송 (접촉망 · 복셀) 분업은 그대로.
- **frame [4] (교차 맞춤 금지)**: 이 논문에는 맞춘 값 자체가 없다.  A′-0 · A 를 만들면 실험 (기공 · 두께) 에 따로 보정하고 DEM 과 맞추지 않는다.
- **frame [1]/[2] (연화)**: 이 논문은 연화 · 재배열을 말하지 않는다 (중립).  다만 §1 · §2.3 의 진술은 "단일 속도장은 못 가른다" 를 우리 계보의 원전이 직접 적은 것이다.

---

## 9. 깊은 통찰

① **계보의 원전이 정량 검증을 주지 않는다.**  우리 `substep()` 은 이 논문 §4 그대로인데, 이 논문이 그 이산화에 대해 보인 것은 "눈으로 비슷" 과 에너지 곡선 두 개 (이산화끼리) 뿐이다.  수렴 차수 · 응력 정확도 · 반력 정확도는 **인용할 곳이 없다** — 우리 단위 시험 (계획의 U1 입자 하나 압축 · U6 조밀 충전 해상도 수렴) 이 그 자리를 채워야 하고, 원고에서 MLS-MPM 의 정확도를 이 논문에 기대는 문장을 쓰면 안 된다.

② **MLS-MPM 힘은 전통 MPM 힘과 같은 식이 아니다** (§4-3 [카드 산술]).  ∇N 대신 M_p⁻¹ N (x_i − x_p) — 선형장 재현과 운동량 보존만 같고 점별로는 최대 1.5 배 다르다.  접촉 문헌 (Bardenhagen 2000 은 1차 B-spline + ∇N — 그 카드 §4-1) 의 해상도 규칙 (지름당 8 요소 등) 을 우리 2차 B-spline MLS-MPM 에 옮길 때 **수치가 그대로 옮겨진다는 보장이 없다** — 같은 시험을 우리 이산화로 다시 재야 한다 [카드 추론].

③ **"한 칸에 속도 하나" 를 넘는 두 길.**  Bardenhagen 은 물체마다 속도장을 **늘리고**, CPIC 는 장은 하나로 두고 **노드를 표면의 한쪽에만 배정** (비호환 쌍은 전달을 끊고 유령 값) 한다.  CPIC 는 메모리가 싸지만 (노드당 64 비트) **표면이 주어져야** 한다 — 강체 메시는 되고 변형체끼리의 경계는 안 된다.  ⇒ AM (강체) 에는 CPIC 식, SE–SE 에는 다중 속도장 — 두 길은 겨루는 것이 아니라 **맡는 계면이 다르다** [카드 추론].

④ **후보 A 의 부품은 있고 검증은 없다.**  V_r(x) · 투영 · 임펄스 · 유령 속도 · 벌칙 · 7 단계는 그대로 쓸 수 있다.  없는 것: (a) 힘 · 토크 전달의 수치 확인 (b) 고압 준정적 영역의 시연 (전 예제가 중력 구동) (c) AM–AM 접촉 (외부 해법) (d) 강결합 (e) 강체 16 개를 넘는 저장 (2 비트 × 16 = 32 비트 [카드 산술] — real_14 의 AM 457 개에는 '가장 가까운 강체 번호' 같은 다른 부호화가 필요 [카드 추론]).  ⇒ A 의 신뢰는 단위 시험 (U3 단단한 구를 소성 블록에 눌렀다 떼기 · U5) 에서 나와야 한다.

⑤ **좁은 틈은 저자가 못 한다고 적은 바로 그 자리다.**  *"we cannot handle sub-grid level boundary configurations such as sharp corners and narrow gaps"* (§8).  복합 양극의 압밀은 단단한 AM 사이에 SE 를 끼워 누르는 일이라, 하중을 지는 AM–SE–AM 다리가 곧 좁은 틈이다.  2차 B-spline 핵은 3 셀 — 틈이 ≈ 3 Δx (dx 0.141 µm 이면 ≈ 0.42 µm · SE 지름 1 µm 의 절반 이하 [카드 산술]) 아래로 내려가면 그 안의 SE 입자는 온전한 호환 노드 집합을 갖지 못한다 [카드 추론].  A 를 만들면 **두 강체 구 사이에 낀 소성 막** 을 틈 / Δx 사다리로 재는 시험이 먼저다.

⑥ **분리 판정이 속도뿐이다.**  식 (25) 의 separate 는 Bardenhagen 2000 과 같은 운동학 판정이고, 2001 개정판이 고친 이유 (압축이 남아 있는데 멀어지는 속도만으로 놓아 버림 → 되튈 때 에너지가 약간 늚 — `bardenhagen2001…` 카드 §3) 가 그대로 남는다.  이 논문은 대신 '색 지속 + 약한 벌칙력' 으로 침투를 막는다.  탈압 (판 분리 · AM–SE 계면 열림) 을 이 틀로 재려면 **견인력 판정을 더할지** 를 시험 (U3 · U4) 전에 정해 둔다 [카드 추론].

⑦ **우리 판에는 분리 규칙이 없다 — 식 (25) 로 읽으면 'slip' 꼴이다** (§8-2).  탈압 계산에서 판이 물러나는 동안에도 판 위 노드가 판 속도를 받으므로, 핵 폭 안의 SE 는 그 속도를 일부 물려받아 끌려 올라간다 (접착 같은 인공물 · 크기 미측정) [우리 코드 판독 · 카드 추론].  식 (25) 의 separate 한 줄 (멀어지면 그대로) 이 가장 작은 고침이고, 마찰 μ 를 같이 얻는다 — A′-0 의 첫 항목.

⑧ **이 논문의 소성 예제와 우리 설정은 다른 영역이다.**  E/σ_y 가 5 × 10³ – 8 × 10⁴ (거의 강소성) ↔ 우리 ≈ 5.1 (항복에서 탄성 편차 변형률 σ_y/(2μ) ≈ 0.29 [카드 산술: 0.30 / (2 × 0.5134)]).  Table 3 캡션은 소성 재료에 "St. Venant–Kirchhoff 탄성 + von Mises [Gao et al. 2017]" 를 한 쌍으로 쓴다고 적는데, 우리 코드는 응력은 fixed corotated · 반환 사상은 Hencky 변형률이다 (이미 `comparison_vs_ours_DEM.md` §C 의 11-09 정정 메모에 있음).  변형률이 작으면 두 탄성 법칙이 같아지지만 우리 영역에서는 차이가 작지 않을 수 있다 — 이 논문은 그 영역을 보증하지 않는다.  [Gao et al. 2017] 의 정확한 식은 이 논문에 없다 [미확인].

⑨ **수치 소산이 크다 — 그리고 이산화를 바꿔도 같다.**  젤 시험에서 두 방법 모두 에너지의 ≈ 85 % 를 잃는다 (Fig. 17 [판독 · 카드 산술]).  준정적 가압에서는 이 소산이 감쇠 노릇 (정착을 도움) 을 하지만, 그 크기가 격자 · 걸음 · 속도에 어떻게 달리는지는 이 논문에 없다 [미확인] — 우리 쪽에서는 판 속도 사다리가 유일한 확인 수단이다.  탈압의 되돌아온 **양**은 평형량이라 소산에 덜 민감할 것이나, 되튐 **과정** (넘침 · 진동 · 응력파) 은 이 이산화로 믿지 않는다 [카드 추론].

⑩ **안정 조건은 원전에 없다.**  Δt 는 표에 값만 있고, 일관 단위 가정으로는 Courant 수가 0.018 – 1.72 로 100 배 퍼진다 (§3-2 [카드 산술]).  우리 `--platen-mach` · CFL 규칙은 이 논문에서 온 것이 아니라 우리가 세운 것이다 — Methods 에서 시간 간격의 근거를 이 논문으로 돌리지 않는다.

⑪ **Q_p 의 부호** (§4-5).  인쇄된 융합 행렬은 응력 항이 `+` 인데 식 (18) · (26) 과 맞추면 `−` 다 (우리 코드도 `−`).  원고 · SI 에 식을 옮길 때 Q_p 가 아니라 식 (18) · (26) 을 옮긴다.

---

## 10. [DEM 우선 (수영)] — 후보별 함의 + 구체 행동

| 후보 | 이 논문의 함의 | 판정 |
|---|---|---|
| **A′-0** (판 · 벽 · AM 자리에만 미끄럼 · 분리) | 식 (25) 가 그대로 부품 — sticky / slip / separate + μ.  우리 경계를 이 유형으로 다시 쓰면 판 = separate + μ_w · 바닥 / 옆벽 = separate + μ_w · AM = slip 또는 separate + μ.  노드에 건 조건으로도 넣을 수 있고 (옛 방식), 입자–노드 호환 + 유령 속도까지 넣으면 핵 뭉개짐이 준다 | ✅ 직접 지지 · ⚠ 수치 검증은 우리 몫 (U2 · U4) |
| **A** (AM = 움직이는 강체 · SE 한 속도장) | 한 걸음 7 단계 · 임펄스 · 유령 속도 · 벌칙의 **알고리즘 원전**.  그러나 고압 준정적 · 강체 수백 개 · 좁은 틈 · AM–AM 접촉 · 강결합은 이 논문 밖 | ✅ 부품 · ⚠ 성능 · 정확도 근거 0 · ⚠ 좁은 틈은 저자 명시 한계 |
| **A′** (입자마다 속도장) | 근거 없음 — 변형체끼리의 접촉은 단일 속도장 그대로.  §1 · §2.3 의 "단일 속도장은 못 가른다" 진술이 A′ 가 필요한 이유의 인용처일 뿐 | 중립 (필요성의 진술만) |
| **B** (입자마다 유한요소 + 접촉) | §1 이 메시 기반 절단 (재메시 · VNA · XFEM) 의 어려움을 적는다 — 품질 유지 · 퇴화 경우의 부동소수 · 자기 충돌.  입자별 FE 접촉과는 다른 문제 | 중립 |
| **C / C′** (접촉 법칙 DEM) | 관련 없음 (DEM 언급 0) | — |
| **D0** (지금 DEM) | 관련 없음 | — |
| **M0** (균질화 압밀) | 관련 없음.  모래를 Drucker–Prager 연속체로 푸는 것은 입상체 균질화의 한 예이나 압밀이 아니다 | — |

**구체 행동 (순서 = 싼 것 → 비싼 것; 전부 [카드 추론] · 결과 전 등록 대상)**
1. **인용 정리** — 원고 · SI 의 MPM 이산화 인용을 이 논문으로 (식 16 · 17 · 18 · 26).  함께 적을 한정: "정량 정확도는 이 문헌이 아니라 우리 단위 시험이 보인다".  Q_p 는 옮기지 않는다 (부호).
2. **A′-0 의 식 고정** — 판 · 바닥 · 옆벽 · AM 노드에 식 (25) 를 넣는 변형 (유형과 μ 를 인자로).  기본값은 지금 거동과 비트 같게 (AM = sticky · 판 = slip · 벽 = separate μ 0) 두고, 바꾼 팔만 새 거동.  시험: U2 = Bardenhagen 2000 식 (25) 경사면 해석해 · U4 = 판 분리 (separate 에서 판이 물러날 때 반력이 0 으로 떨어지고 인장이 안 생기는가).
3. **핵 뭉개짐 재기 (GPU 불요 · 작은 2D)** — 정지한 강체 평면 옆 소성 띠의 전단 흐름을 (i) 노드 조건 (ii) 호환 + 유령 속도로 풀어 표면에서 1.5 Δx 안의 속도 분포를 견준다 — 우리 AM 표면 '붙음 층' 의 크기를 숫자로.
4. **A 의 저장 설계** — AM 457 개 > 16 이므로 2 비트 색 대신 노드당 '가장 가까운 AM 번호 (int32) + 해석적 부호 거리'.  구는 닫힌 볼록체라 색 (어느 쪽) 이 거리의 부호와 같다.  메모리: 384³ 노드 × 8 B ≈ 0.45 GB [카드 산술] — 지금 `grid_v` + `grid_m` (≈ 0.91 GB) 의 절반.
5. **A 의 단위 시험을 이 논문 밖에서 가져온다** — U3 (단단한 구를 J2 블록에 눌렀다 떼기: 평균 접촉 압력 · 잔류 압흔 · 되돌아옴 ↔ 접촉역학 카드의 해석 · FE 값) · 좁은 틈 시험 (두 강체 구 사이 소성 막, 틈 / Δx = 6 · 4 · 3 · 2) · 정지 부력 (힘 전달의 해석해).  이 논문은 표적값을 하나도 주지 않는다.
6. **AM–AM 접촉 법칙 결정** — 후보 A 에서 AM–AM 은 DEM 접촉 (지금 LIGGGHTS 의 법칙을 그대로 쓸지) 이 된다.  그 선택과 보정 대상 (실험) 을 A 등록 문서에 미리 적는다.
7. **분리 판정 선택** — 속도 판정 (이 논문 · Bardenhagen 2000) ↔ 견인력 판정 (Bardenhagen 2001) 을 탈압 단위 시험 (U3 · U4) 의 두 팔로 등록.

---

## 11. 논문이 스스로 적은 한계 (원문 근거)

| # | 한계 | 근거 |
|---|---|---|
| 1 | CPIC 는 **Δx 규모**까지만 해상 — 격자보다 작은 뾰족한 모서리 · 좁은 틈 불가 | §8 *"While CPIC tackles infinitely thin boundaries, it only resolves features at a scale of grid Δx.  Thus we cannot handle sub-grid level boundary configurations such as sharp corners and narrow gaps as done by Azevedo et al. [2016] with cut-cells."* |
| 2 | 호환 판정이 이진 · 격자 정렬 | §8 *"Our compatibility condition between particles and grids nodes is a binary decision and essentially grid-aligned."* |
| 3 | 입자에서 날카로운 절단면을 복원하기 어려움 | §8 *"it is hard to reconstruct sharp cutting surfaces from particles"* |
| 4 | 강체–MPM **강결합 (완전 암시)** 미정식 | §8 *"Fully implicit rigid-MPM strong coupling is not formulated in this work and we leave that as future work."* |
| 5 | 힘 식은 **선형 다항 공간**에서만 유도 | §3.3.5 *"it is possible to generalize this choice to a higher order polynomial space, and we leave such an extension to future work"* |
| 6 | 거리 뿌림이 모서리 근처 노드를 놓침 | §5.2.1 *"there will be missing values at certain corners"* · §5.3.2 *"tends to miss a small number of nodes near mesh corners"* |
| 7 | 입자가 이류 수치 오차로 표면을 살짝 넘음 → 벌칙력 필요 | §5.3.3 *"a particle may slightly penetrate a surface due to numerical advection error"* |
| 8 | 격자 이하 정확도 · 복잡한 위상 (non-manifold 분기) 에는 다른 거리장이 낫다 | §5.2 *"for sub-grid accuracy and more non-trivial topology such as non-manifold bifurcation, it is a better choice to construct the distance field using the algorithm by Xu and Barbič [2014]"* |
| 9 | 강체마다 CDF 하나는 비싸다 → 노드당 64 비트로 압축 (강체당 2 비트) | §5.2.3 *"Ideally one would like to have one CDF for each rigid body, but this is expensive in both computation and storage."* |
| 10 | 암시 적분에서는 속도 이득이 작다 | §6.1 *"The gain is however less significant, because only in explicit time integration it benefits from unifying affine momentum and particle force contribution."* |
| 11 | 전통 MPM 과의 일치는 '시각적' · 에너지 곡선 수준 | §1.1 *"almost identical visual results"* · §7 *"visually comparable dynamics"* |
| 12 | 강체–강체는 다루지 않음 | §5.1 *"We will skip the details"* |

## 12. 불확실 · PDF 에 없는 것

- Table 3 의 **단위** · 프레임 길이 · 예제별 적분 방식 (명시 / 암시) · 영역 크기 · 격자 수 · 셀당 입자 수: 미인쇄 → 이 카드의 c_P · Courant 수는 가정 산술.
- **안정 조건 · CFL 규칙 · 수렴 연구**: 없음.
- CPIC 의 값: k_h · c · 예제별 B_r · μ_r · 강체 질량 / 관성 · 강체 입자 수: 없음.  토크 식 · 임펄스 → 강체 속도 식: 없음.  |v_t| = 0 처리: 없음.
- 식 (18) 의 합이 호환 입자로 제한되는지 · 임펄스에 아핀 항이 들어가는지: 명시 없음 (이 카드의 읽기는 [카드 판독 / 추론]).
- Fig. 17 의 시험 조건 (재료 · 격자 · Δt · 에너지 정의 · 축 단위): 없음.  로봇 대조의 수치: 없음.
- 인쇄 어긋남 [카드 판독]: Q_p 첫 항 부호 (`+` ↔ 식 18 · 26 의 `−`) · 식 (15) 의 N_i (모자 빠짐) · §5.5 본문 "v_j = v_pⁿ" ↔ 식 (27)(28) 의 ṽ_p · Table 1 의 ρ 형 'vector' · v̂ 위첨자 n · 본문 M_p⁻¹ ↔ 보충 D_p⁻¹ (같은 상수의 두 이름).
- Taichi [Hu 2018] 와 우리가 쓰는 파이썬 `taichi` 패키지의 관계 · 코드 공개 위치: 이 논문에 없음 [미확인 — 원문 밖].
- **이 방법이 고밀도 압밀 · 탈압에서 어떻게 행동하는지는 이 논문으로 알 수 없다.**

## 13. 인용 가능 문장 (덱 · 원고용)

- "MLS-MPM 은 약형의 시험 함수와 속도를 B-spline 대신 이동 최소제곱 형상함수로 이산화한 MPM 이며, 선형 기저와 2차 B-spline 가중에서 노드 힘이 f_i = −Σ_p N_i V_p⁰ M_p⁻¹ (∂Ψ/∂F) F_pᵀ (x_i − x_p), M_p = Δx²/4 가 되어 형상함수 기울기를 계산하지 않는다 (Hu et al., ACM Trans. Graph. 37(4), 150, 2018, 식 15–18)."
- "기존 MPM 은 물질점의 날카로운 분리와 불연속 속도를 나타내지 못한다 — 단일 속도장을 쓰기 때문이다 (같은 문헌 §1 · §2.3)."  — ⚠ 이 문헌은 그 한계를 **강체 표면에 대해서만** 푼다는 것을 함께 적을 것.
- "MLS-MPM 과 전통 MPM 은 두 초탄성 시험에서 거의 같은 에너지 곡선을 냈다 (같은 문헌 Fig. 17)."  — ⚠ 정확도 검증으로 쓰지 말 것 (이산화끼리의 비교 · 해석해 없음).
- ⛔ 쓰지 않을 문장: "MLS-MPM 은 검증된 방법이다" (정량 검증 없음) · "강체 결합이 실험으로 검증됐다" (로봇 영상의 정성 대조뿐).

## 14. 기법 미니 용어집

- **MLS (moving least squares)** — 흩어진 표본에서 위치마다 가중 최소제곱으로 다항식을 맞추는 국소 재구성.  함수값과 기울기가 같이 나온다 (식 4).
- **EFG / RKPM** — MLS 형상함수로 약형을 이산화하는 무격자법.  이 논문은 MPM 을 "격자를 이웃 탐색 도우미로 쓰는 EFG" 로 읽는다.
- **모멘트 행렬 M (M_p · D_p)** — MLS 정규방정식의 행렬.  2차 / 3차 B-spline 가중 + 선형 기저면 상수 Δx²/4 · Δx²/3.
- **APIC (affine particle-in-cell)** — 입자가 속도 v_p 와 아핀 행렬 C_p (국소 속도 기울기) 를 싣는 전달.  MLS 로 읽으면 C_p = 재구성한 ∇v.
- **PolyPIC** — 더 높은 차수의 다항 계수를 싣는 전달.  선형만 쓰면 APIC.
- **MLS-MPM** — 힘과 F 갱신까지 MLS 형상함수로 이산화한 MPM (식 16 · 17 · 18).  ∇N 을 쓰지 않는다.
- **한 점 구적** — 입자 구획 안 응력을 입자 값 하나로 대표하는 근사 (식 16 의 ≈).
- **CPIC (compatible particle-in-cell)** — 입자와 노드의 호환 (같은 쪽) 여부로 전달을 끊는 전달 방식.
- **CDF (colored distance field)** — 노드마다 부호 없는 거리 + 색 (표면별 친화 A · 꼬리표 T).  교차하는 열린 표면을 격자 한 장으로 나타낸다.
- **강체 입자 (rigid particle)** — 강체 표면에 뿌린 보조 표본점.  거리장을 격자에 뿌리는 데만 쓴다.
- **호환 (compatible)** — 입자와 노드가 함께 아는 모든 표면에 대해 같은 쪽.
- **유령 속도 (ghost velocity)** — 비호환 노드 대신 쓰는, 입자 자신의 (투영된) 속도.
- **sticky / slip / separate** — 경계 유형: 붙음 / 마찰 없는 미끄럼 (분리 없음) / 마찰 미끄럼 + 자유 분리.
- **약결합 (weak coupling)** — 한 걸음 안에서 MPM 과 강체를 번갈아 푸는 것 (동시에 풀지 않음).
- **SPGrid** — Morton 순서의 희소 블록 격자 자료구조.

## 15. 관련 카드

- **변형체끼리의 접촉 (이 논문에 없는 절반)**: `bardenhagen2000_mpm_granular_multibody_frictional_contact` (물체별 속도장 · 식 23 = 이 논문 식 25 의 separate 와 같은 보정) · `bardenhagen2001_mpm_improved_contact_granular_stress_waves` (견인력 분리 판정 — 이 논문에는 없음) · `nezamabadi2022_mpm_cd_plastic_particle_compaction` · `nguyen2017_mpm_bpm_deformable_particle_compaction` (입자별 격자 + contact dynamics 로 압밀).
- **같은 그래픽스 MPM 계보**: `stomakhin2013_mpm_snow_elastoplastic` (fixed corotated · 수준집합 충돌체 = 이 논문이 "옛 방식" 이라 부르는 경계) · `klar2016_dp_sand_animation` (Drucker–Prager · APIC — 이 논문의 모래 재료 모델) · `devaucorbeil2020_mpm_after_25_years_review` (MPM 리뷰 · MLS 계열의 위치).
- **입자별 FE (후보 B)**: `cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd` (강체 + 무른 입자 혼합 압밀 — 후보 A 가 못 주는 입자 경계 관측량) · `demirtas2021_mpfem_hollow_sphere_die_compaction` · `pycompact2025_dem_mpfem_workflow`.
- **단위 시험의 표적 (이 논문이 주지 않는 것)**: `kogutetsion2002_ep_sphere_rigid_flat` (탄소성 구–평면 접촉).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
