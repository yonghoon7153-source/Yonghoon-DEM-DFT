<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 같은 축 = hu2018_mls_mpm_cpic_two_way_rigid_coupling.md (강체–MPM 결합) · bardenhagen2000_mpm_granular_multibody_frictional_contact.md -->
# MPM (연속체) 과 DEM (구 · 구 다발) 을 **블랙박스 두 개로 나눠** 공유 경계에서만 주고받는 분할 결합 (KRATOS) — DEM 이 먼저 접촉력을 내고 (벽 조건 = MPM 외곽) → 그 힘을 MPM 경계 입자에 점하중으로 (보존 사상 Hᵀ) → MPM (암시 Newmark) 이 움직인 경계를 다시 DEM 벽으로 (H) · Gauss–Seidel 약결합 · 빔 + 구 충격 (2D · 3D 해석해 대조) · 모래 흐름이 나무 블록을 넘기는 실험 대조 ★★ [DEM 우선 (수영)] 메모 3.2 **후보 A (강체 AM + SE 연속체)** 와 *물리 짝은 같고 결합 알고리즘은 다른* 공개 선례 — Singer, Sautter, Larese, Wüchner, Bletzinger (Adv. Model. Simul. Eng. Sci. 2022)

> slug `singer2022_partitioned_mpm_dem_coupling_kratos` · DOI `10.1186/s40323-022-00229-5` · type `MPM–DEM 분할 결합 (KRATOS · MPM = 암시 Newmark 갱신 라그랑주 + 경계 입자 점하중 · DEM = Hertz–Mindlin 스프링–감쇠 + Velocity-Verlet + 쿼터니언 회전 · Dirichlet–Neumann · 보존 사상 · 최근접 사상 · Gauss–Seidel 약결합) — 2D/3D 빔 충격 해석해 · 2D 모래 흐름 실험 대조 · 분말 압축 없음` · PDF `singer2022.pdf` · digested `2026-11-25` · status ✅

> 표지: **[인쇄]** = 본문 · 표 · 캡션 · 그림 안 글자 · **[판독]** = 그림에서 읽은 값 (그림 11 = PDF 벡터 표식 · `litdb/figures/singer2022_partitioned_mpm_dem_coupling_kratos/digitized.csv` · 그림 7 · 8 = 격자선으로 눈 판독) · **[카드 산술]** · **[추정]** · **[미확인]**.

---

## 0. 이 논문이 우리에게 *왜* 필요한가 (한눈 positioning)

[DEM 우선 (수영)] 재설계 메모 3.2 (`docs/reviews/dem_redesign_direction_20261109/memo_v3_2.md`) 의 **후보 A** = *"A′-0 + AM 을 강체로 움직인다.  격자에서 받는 힘 · 토크로 적분하고, AM–AM · AM–벽은 DEM 식 법칙.  SE 는 한 속도장"* 이다.  1저자 11-25 공부 (MPFEM · Kratos) 에서 Kratos 의 MPM–DEM 결합을 그 꼴로 읽었고, 그 근거 논문이 이 카드다.

**결론부터** — 물리 짝 (단단한 이산 물체 = DEM · 무른 연속체 = MPM) 은 후보 A 와 같다.  **결합 알고리즘은 다르다**: 후보 A 는 한 격자 안에서 강체를 움직이는 단일 코드 결합 (선례 = `hu2018_mls_mpm_cpic_two_way_rigid_coupling`) 이고, 이 논문은 두 풀이기를 블랙박스로 두고 **MPM 몸의 외곽 (경계 입자) ↔ DEM 벽 조건** 으로만 힘 · 변위를 주고받는 분할 결합이다.

| 우리가 필요한 것 | 이 논문이 주는 것 | 주지 않는 것 |
|---|---|---|
| 강체 (AM) + 연속체 (SE) 결합의 공개 구현 | KRATOS (C++ · Python 인터페이스) 에서 MPM · DEM 을 분할 결합 · GitHub [73] [인쇄] | 응용 이름 · 버전 고정 (참고문헌 [41] = KratosMultiphysics Version 8.0 · Zenodo 2020) · 입력 파일 [미확인] |
| 결합 꼴 | Dirichlet (DEM 벽) – Neumann (MPM 경계 입자 점하중) · 보존 사상 Hᵀ · Gauss–Seidel 약결합 (Algorithm 1) [인쇄] | 강결합 (반복) · 수렴 · 안정 분석 |
| 큰 강체 ↔ 고운 격자의 함정 | DEM 구 하나는 합력 **하나**를 낸다 → 몇 노드에만 힘 → 연속체가 구로 스민다 → **구 다발 (cluster)** 로 푼다 (그림 5) [인쇄] | 다발 크기 · 수렴 기준 |
| 검증 | 빔 + 구 충격 (해석해 · DEM–FEM 대조 · 2D · 3D) · 모래 흐름 + 블록 (실험 대조 · 그림 10–12) | **분말 압축 · 고압 준정적 · 조밀 충전 · 많은 DEM 입자** 선례 0 |
| 우리 계 규모 | 2D 블록 다발 2 개 (구 64 개씩) | real_14: AM 457 + SE 32,832 · 300 MPa |

---

## 1. 한 줄 요약

MPM 과 DEM 을 각자의 풀이기 (블랙박스) 로 두고 공유 경계 Γ_SP 에서 운동학 조건 (변위 · 속도 같음) 과 동역학 조건 (견인력 평형) 만 맞추는 분할 결합을 KRATOS 에 만들었다.  DEM 은 MPM 외곽을 **벽 조건** (2D 선분 · 3D 삼각형) 으로 보고 접촉력을 계산하며, 그 힘은 보존 사상 Hᵀ 로 MPM 의 **경계 입자** (질량 없는 점 · 물질점처럼 움직여 외곽을 따라감) 에 점하중으로 들어간다.  MPM 이 풀리면 경계 입자 변위 · 속도가 H 로 DEM 벽에 돌아간다 (Gauss–Seidel · 약결합 · 같은 시간 간격).  2D · 3D 단순 지지 빔에 구가 한 번 · 세 번 부딪히는 문제에서 해석해 · DEM–FEM 결합해와 맞았고, 모래 흐름 (MPM · Mohr–Coulomb) 이 쌓인 나무 블록 셋 (DEM 구 다발) 을 넘기는 실험에서 블록의 회전 · 멈춘 자리 (34.5 ↔ 34.6 cm · 39.7 ↔ 40.1 cm) 를 맞췄다.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Veronika Singer** (교신, veronika.singer@tum.de) · **Klaus B. Sautter · Antonia Larese · Roland Wüchner · Kai-Uwe Bletzinger** |
| 소속 | Chair of Structural Analysis, Technical University of Munich (Singer · Sautter · Larese · Bletzinger) · Department of Mathematics "Tullio Levi Civita", Università degli Studi di Padova (Larese) · Institute for Advanced Study, TUM, Garching (Larese) · Institute of Structural Analysis, Technische Universität Braunschweig (Wüchner) |
| 저널 | **Advanced Modeling and Simulation in Engineering Sciences (2022) 9:16** (24 쪽) · Research Article · Open Access |
| DOI | **10.1186/s40323-022-00229-5** |
| 이력 | Received 2022-03-21 · Accepted 2022-07-02 |
| 라이선스 | Creative Commons Attribution 4.0 [인쇄] |
| 연구비 | Hans Fischer Fellowship program (Institute of Advanced Studies, TUM) · INdAM 지원 · Open Access = Projekt DEAL |
| 자료 · 코드 | *"The software used is [39–41]. The current developers' version is available at [73] as a GitHub repository."* — [73] = github.com/KratosMultiphysics/Kratos (1저자가 준 링크와 같다) [인쇄] |
| 키워드 | Material point method · Discrete element method · Partitioned coupling · Natural hazards · Granular flow |
| 연구유형 | 수치 방법 (분할 결합) + 해석해 · 문헌 수치해 · 문헌 실험 대조 |

---

## 3. 방법 ★ (식 · 알고리즘)

### 3-1. MPM (Kratos MPM 쪽)

- 지배식: 질량 · 운동량 보존 Eq. (1)–(2) · Dirichlet / Neumann 경계 Eq. (3)–(4) · 약형 Eq. (5)–(6) [인쇄].
- 이산화: 물질점 n_p 개 (질량 일정 · 이력 변수 운반) + 고정 배경 격자 (Eq. 7–11).  **기하 · 재료 비선형 → Newton–Raphson** · 접선 강성 K_IJ (Eq. 10) 에 관성 항 N_I ρ α N_J · **α = 1/(0.25 Δt²) = 암시 Newmark** [인쇄].
- 한 걸음의 세 단계 (그림 1): (I) 초기화 = 물질점 → 노드 질량 · 운동량 · 힘 · 속도 · 가속도 (II) 라그랑주 = 지배식 풀이 · 격자가 변형 (갱신 라그랑주 FEM 걸음과 같음) (III) 대류 = 노드 해 → 물질점 위치 · 가속도 · 속도 (사다리꼴) 갱신 · 격자 되돌림 [인쇄].
- 암시 Newmark MPM 은 Guilkey & Weiss [46] 의 변위 기반 판을 넓힌 것 (`guilkey2003_implicit_mpm_newton_quasistatic_fem_comparison` 카드와 같은 계보) [인쇄 · 카드 대조].
- **경계 입자** (boundary particles · Eq. 12–13): Neumann 경계를 질량 없는 점 n_bp 개로 나누고 점하중 F_S 를 준다.  초기화 단계에서 연결 요소를 찾아 기저 함수로 노드에 싣고, 물질점처럼 움직여 **외곽을 따라간다** [인쇄].
- 물질점이 없는 요소에 경계 입자가 있으면 질량 있는 노드에만 싣도록 기저 함수를 고친다 (Eq. 14 · m_I ≤ ε 인 노드는 0 · 나머지 정규화) [인쇄].

### 3-2. DEM (Kratos DEM 쪽)

- 구 또는 **구 다발** (cluster · [52] · 다발 만들기 도구 [53–55]).  접촉 판정 = 대상 (구 · 꼭짓점 · 선분 · 면) 까지의 최단 거리 d_i < R_i · Double Hierarchy Method [33,34] [인쇄].
- 접촉력: **Hertz–Mindlin 스프링–감쇠 (HM+D) [56]** · k_n · k_t · c_n · c_t · µ (Coulomb 한계) (그림 2) [인쇄].
- 운동: F = mü · T = Iω̇ (Eq. 15–18) · 병진 = **2 차 Velocity-Verlet** · 회전 = 쿼터니언 적분 [62,63] [인쇄].

### 3-3. 분할 결합 (Algorithm 1 · 그림 3 · 4)

| 식 | 내용 | 표지 |
|---|---|---|
| Eq. (19) | 공유 경계 Γ_SP = Γ_S ∩ Γ_P | [인쇄] |
| Eq. (20) | 운동학: u_P = u_S · u̇_P = u̇_S (Γ_SP 위) | [인쇄] |
| Eq. (21) | 동역학: p_P = −p_S (견인력 평형) | [인쇄] |
| Eq. (22) | 이산: u_P = H_PS u_S · u̇_P = H_PS u̇_S (H = 직접 사상 행렬 · 맞지 않는 이산화) | [인쇄] |
| Eq. (23) | F_S = H_PSᵀ F_P — **보존 사상** (에너지 보존 Eq. 24) | [인쇄] |
| Eq. (25) | F_P = DEM(u_P, u̇_P) — DEM 쪽 **Dirichlet = 벽 조건** (Santasusana [33] 의 DEM–FEM 분할 결합에서 온 것) · 2D 선분 · 3D 삼각형 | [인쇄] |
| Eq. (26) | ⟨u_S, u̇_S⟩ = MPM(F_S) — MPM 쪽 **Neumann = 경계 입자 점하중** | [인쇄] |
| 사상 | **최근접 이웃** 보간 → 경계 입자를 DEM 벽 절점 자리에 두면 거의 복사 | [인쇄] |
| 걸음 | (1) DEM → (2) Hᵀ → (3) MPM → (4) H · **두 풀이기가 같은 Δt** 로 나간다고 가정 · 반복 없음 (약결합 · explicit coupling) | [인쇄] |

**Algorithm 1** — *Partitioned Weak MPM-DEM Coupling Scheme* [인쇄 · `tab_algorithm_1.png`]

| 단계 | 내용 | 식 |
|---|---|---|
| while time < t_end do | | |
| (1) | DEM Solver: F_P = DEM(u_P, u̇_P) | (25) |
| (2) | Mapper: F_S = H_PSᵀ F_P | (23) |
| (3) | MPM Solver: ⟨u_S, u̇_S⟩ = MPM(F_S) | (26) |
| (4) | Mapper: u_P = H_PS u_S and u̇_P = H_PS u̇_S | (22) |

### 3-4. ★ 큰 DEM 입자의 함정과 다발 (그림 5)

- *"a DEM particle i calculates one resulting contact force F_i,Contact, depending on the shortest distance between the interacting object and the center of the particle."* → 선분 하나에 닿으면 그 두 절점에만 힘 → 경계 입자 두 개 → 격자 몇 노드만 받는다.  *"Especially for granular material or solids within the MPM domain, together with a relatively larger particle size compared to the element size of the computational background grid in the MPM domain, this could lead to an insufficient representation of the shared interface, possibly resulting in penetration of the MPM material into the DEM particle"* [인쇄].
- 처방: **DEM 구 다발** — 다발 안 구마다 접촉력을 내어 경계에 힘이 퍼진다.  *"the clustering method should be applied if the shape of the particle should be accurately considered and a detailed interface representation is necessary in the MPM model"* [인쇄].

---

## 4. 검증 예제 ★ (모든 숫자)

### 4-1. 한 번 충격 — 단순 지지 빔 (MPM) + 구 (DEM) (그림 6 · 7)

| 항목 | 값 | 표지 |
|---|---|---|
| 빔 | 길이 15.35 cm · 단면 1 × 1 cm² · E 215.82 GPa · 밀도 7960 kg/m³ · ν 0.289 (그림 6) | [인쇄 · 그림 글자] |
| 구 | 반지름 1.0 cm · 처음 속도 **본문 −0.01 cm/s ↔ 그림 6 "u̇₀ = 1 cm/s"** (100 배 차 · 어느 쪽이 맞는지 원문으로 못 가린다) | [인쇄] — ⚠ 불일치 |
| 2D MPM | 배경 격자 = 사각형 62 × 13 (길이 15.87 cm · 높이 = 빔의 3 배) · 몸 메시 120 × 8 · 요소마다 물질점 16 개 (가우스점 자리) → 물질점 15,360 개 [카드 산술] · 경계 = DEM 벽 선분 60 · 경계 입자 61 (벽 절점과 같은 자리) | [인쇄] |
| 3D MPM | 벽 = 구조 삼각형 77 × 10 · 육면체 배경 격자 (폭 1.52 cm 를 7 요소) · 몸 메시 폭 10 요소 · 요소마다 물질점 16 | [인쇄] |
| 접촉 | Hertz · 반발 계수 1.0 · **DEM–MPM 마찰 0** | [인쇄] |
| Δt | **5 × 10⁻⁸** (단위 미기재 · 초로 읽음) | [인쇄] |
| 결과 (그림 7) | 접촉력 정점 ≈4.9 N (≈0.07 ms) · 접촉 끝 ≈0.15 ms · 빔 가운데 처짐 정점 ≈1.1 µm (≈0.32 ms) · 최저 ≈−1.1 µm (≈0.83 ms) · 2D · 3D · 기준해가 겹친다 — *"excellent agreement with the solution obtained by [70] and [33]"* | [판독 · 대략] + [인쇄] |

### 4-2. 세 번 충격 — 긴 빔 + 큰 구 (그림 8)

| 항목 | 값 | 표지 |
|---|---|---|
| 빔 · 구 | 길이 30.70 cm · 구 반지름 2.0 cm | [인쇄] |
| MPM | 배경 격자 124 × 13 (길이 30.96 cm) · 몸 메시 "24 × 8" (선분 240 개와 맞추면 240 × 8 의 인쇄 오류로 의심) · 요소마다 물질점 16 · DEM 벽 선분 240 | [인쇄] · 오기 의심 [카드 추론] |
| 결과 | 충격 세 번 · 접촉력 정점 ≈9 N (≈0.1 ms) · ≈12 N (≈1.65 ms) · ≈5–6 N (≈2.9–3.1 ms) · 빔 처짐 정점 ≈8.6 µm (≈2.15 ms) [판독 · 대략] · 둘째 · 셋째 충격에서 해석해와 작은 차 — 선형 고체 요소 FEM (DEM–FEM [33]) 도 같은 차를 보였다 (높은 진동 모드를 못 잡음) · DEM–FEM 해와는 *"nearly perfect agreement"* | [판독] + [인쇄] |
| 저자의 차이 설명 | MPM 은 배경 격자 노드가 빔 경계와 맞지 않아 변위장을 FEM 보다 거칠게 근사하고 접촉력을 약하게 부과한다 | [인쇄] |

### 4-3. 모래 흐름이 쌓인 블록을 넘김 (Liu 외 [36] 실험 · 그림 9–12 · Table 1)

**Table 1** — *Material properties for the granular flow and the wooden blocks* [인쇄 · `tab_1.png`]

| Material properties | Granular material (MPM) | Wooden blocks (DEM) |
|---|---|---|
| Density | 1300 kg/m³ | 500 kg/m³ |
| Young's modulus | 50 kPa | 50 MPa |
| Poisson's ratio | 0.4 | 0.5 |
| Cohesion | 0 Pa | 0 Pa |
| Friction angle | 22° | – |
| Dilation angle | 0° | – |
| Restitution coeff. | – | 0.05 |

| 항목 | 값 | 표지 |
|---|---|---|
| 실험 · 모형 | 모래 10 × 20 × 20 cm³ 를 풀어 중력으로 흘림 · 30 cm 떨어진 곳에 같은 나무 블록 셋을 쌓음 · 맨 아래 블록은 바닥에 붙임 · **2D 모형** | [인쇄] |
| MPM | **Mohr–Coulomb 평면변형** · 비구조 삼각형 배경 격자 0.5 cm · 몸 메시 = 그 반 크기 구조 삼각형 · 요소마다 물질점 3 · 바닥 고정 · 세로 벽 미끄럼 | [인쇄] |
| 경계 입자 | 처음 외곽 둘레에 0.005 cm 간격 · **몸 안쪽으로 δ = 몸 메시 크기의 1/3 만큼 옮겨 둠** — 바깥 줄 요소에 물질점이 몇 개 없으면 점하중이 비물리적 운동을 낳아서 (불안정 회피) | [인쇄] |
| DEM 블록 | 블록 2 × 1.8 × 19.8 cm³ · **구 8 × 8 = 64 개를 다진 다발** · 맨 아래 블록 = 고정 경계 · 위 두 블록만 다발 · Hertz | [인쇄] |
| 마찰 · 점착 | 나무 다발끼리 µ 0.6 · c 30 Pa · 강체 경계와 µ 0.3 · c 60 Pa | [인쇄] · DEM–MPM 경계의 µ [미확인] |
| Δt | **5 × 10⁻⁵** (초로 읽음) | [인쇄] |
| 사건 시각 | 흐름이 블록에 닿음 0.25 s (실험과 같음) · 0.30 s 에 두 블록이 아직 전폭으로 맞닿음 · 둘째 블록이 0.36–0.37 s 에 모서리로 바닥에 닿고 0.40 s 에 90° · 맨 위 블록이 0.38–0.39 s 에 모서리로 닿고 0.45 s 까지 180° | [인쇄] |
| 멈춘 자리 | 둘째 블록 왼쪽 끝 ↔ 상자 왼쪽 벽: 실험 **34.6 cm** ↔ 모의 **34.5 cm** · 맨 위 블록: **40.1 ↔ 39.7 cm** | [인쇄] |
| 둘째 블록 회전각 β (그림 11) | 실험 0.30 s 76.5° · 0.35 s 32.4° · 0.40 s 5.5° ↔ 이 논문 84.1° · 47.3° · −1.0° ↔ Liu 외 78.1° · 42.8° · 23.0° ↔ Jiang 외 63.6° · 41.0° · 3.3° | [판독 — PDF 벡터 표식 ±0.5°] |
| β 오차 (0.25–0.45 s 다섯 점 평균 절대 오차) | 이 논문 **6.3°** · Liu 외 7.4° · Jiang 외 **5.0°** | [카드 산술] |
| 저자 평가 | 둘째 블록 β *"in good agreement for the entire simulation time"* · 맨 위 블록 회전은 *"was not captured correctly in previous solutions but is reproduced very well by the novel approach"* (그림 12 · 정성) · 블록끼리 점착을 Hertz 법칙에 넣을 수 있어 0.30 s 에 두 블록이 붙어 있는 모습이 실험과 같다 | [인쇄] |
| 남은 문제 | 끝 무렵 물질점이 DEM 입자로 스민다 → 더 고운 경계 · 작은 배경 요소 필요 · DEM 매개변수 보정 필요 | [인쇄] |

---

## 5. Figure set ★ (12 개 전부 + Table 1 · Algorithm 1 — 모두 렌더해서 열어 봤다)

| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| **1** | MPM 한 걸음의 세 단계 (초기화 · 라그랑주 · 대류) | 우리 Taichi MLS-MPM 과 같은 꼴 (우리는 명시 · 이 논문은 암시) |
| **2** | HM+D 접촉 모형 (구–구 · 구–벽) | DEM 쪽 법칙 (k_n · k_t · c_n · c_t · µ) |
| **3** ★ | Gauss–Seidel 약결합 시간 그림 (1)–(4) | ★ 한 걸음에 한 번만 주고받는다 (반복 없음) |
| **4** ★★ | 결합 전체 그림 — DEM 벽 조건 Γ_P · 사상기 · MPM 경계 입자 Γ_S | ★★ 후보 A 와 다른 점이 한눈에: 힘이 **외곽의 경계 입자**로만 들어간다 |
| **5** ★★★ | (a) 큰 DEM 구 하나 = 합력 하나 → 경계 표현 부족 (b) 구 다발 → 힘이 퍼짐 | ★★★ 우리 AM (≈85 칸 폭 [카드 산술 §7-B]) 에 그대로 걸리는 함정 |
| **6** | 빔 + 구 설정 (E 215.82 GPa · 7960 kg/m³ · ν 0.289 · R 1 cm · u̇₀ 1 cm/s) | 그림 속도 ↔ 본문 속도 100 배 차 |
| **7** ★ | 한 번 충격: 처짐 · 접촉력 vs 시간 (2D · 3D · 기준해) | 결합의 기본 검증 — 동역학 |
| **8** | 세 번 충격: 처짐 · 접촉력 (기준해 · DEM–FEM) | 둘째 · 셋째 충격 차 = 격자 ↔ 경계 불일치 |
| **9** ★ | 모래 (MPM) + 블록 (DEM 다발) 설정 · 경계 입자 δ 이동 확대 | 경계 입자를 몸 안쪽으로 옮긴 처리 |
| **10** ★ | 실험 ↔ 모의 스냅숏 0–0.55 s | 흐름 · 블록 거동 정성 대조 |
| **11** ★★ | 둘째 블록 회전각 β(t) — 실험 · Liu · Jiang · 이 논문 | ★★ 벡터 판독 §4-3 · 이 논문이 가장 정확하지는 않다 (Jiang 5.0° ↔ 6.3°) |
| **12** | 충격 중 스냅숏 — 실험 · Liu · Jiang · 이 논문 | 맨 위 블록 회전의 정성 비교 |
| Table 1 | 모래 · 나무 물성 | §4-3 |
| Algorithm 1 | 결합 반복 | §3-3 |

---

## 6. Post-processing ★

| 무엇 | 어떻게 | 우리 대응물 |
|---|---|---|
| 처짐 · 접촉력 이력 | 빔 가운데 · 구 변위 · 총 접촉력 vs 시간 | 없음 (우리는 판 압력 · 충전율 판독) |
| 블록 회전각 β(t) | 둘째 블록의 각을 문헌 실험 · 두 수치해와 시간마다 비교 | 없음 |
| 멈춘 자리 | 블록 왼쪽 끝 ↔ 상자 벽 거리 | 없음 |
| 스냅숏 | 실험 사진 ↔ 모의 물질점 그림 | 침대 보기 (`/mixer` · 웹앱) |
| 도구 | KRATOS (MPM · DEM 응용) · 응용 이름 · 후처리 도구 [미확인] | Taichi MPM · LIGGGHTS |

---

## 7. 우리 DEM+MPM 대비  →  `comparison_vs_ours_DEM.md` · `our_dem_baseline.md` (⛔ 자리표시 — 우리 값은 CLAUDE.md · 리포 기록에서 직접)

### ★ 7-A. 이 논문 ↔ 메모 3.2 후보 A — 같은 것 · 다른 것

| 항목 | Singer 2022 (분할 결합) | 우리 후보 A (메모 3.2) | 판정 |
|---|---|---|---|
| 물리 짝 | 이산 물체 (DEM 구 · 다발) + 연속체 (MPM) | 강체 AM + SE 연속체 (한 속도장) | **같다** |
| 결합 위치 | **MPM 몸의 외곽** (경계 입자 ↔ DEM 벽 조건) | 격자 노드 (강체가 격자에서 힘 · 토크를 받음 · HU18 CPIC 선례) | **다르다** |
| 결합 세기 | Gauss–Seidel **약결합** · 반복 없음 · 같은 Δt | 한 코드 안 (한 걸음 안에서 일관) [추정] | 다르다 |
| 연속체 풀이 | 암시 Newmark · Newton–Raphson (Kratos MPM) | 명시 MLS-MPM (Taichi) | 다르다 — 이 논문 쪽이 준정적에 유리할 수 있다 [추정] (`guilkey2003_…` 카드) |
| 강체–강체 | DEM (HM+D · Velocity-Verlet · 쿼터니언) | DEM 식 법칙 (AM–AM · AM–벽) | 같은 꼴 |
| 연속체 재료 | Mohr–Coulomb (모래) · 선형 탄성 (빔) | J2 (SE · E 1.53 · ν 0.49 · σ_y 0.30) | 다르다 |
| 하중 | 충격 · 중력 흐름 (동역학 · 낮은 응력) | 300 MPa 준정적 압축 | **선례 밖** |
| 규모 | 구 1 개 · 다발 2 개 (64 구씩) | AM 457 · SE 32,832 (MPM 10⁷–10⁸ 점) | **선례 밖** |
| 연속체 안 접촉 | 한 몸 (모래) · 몸 안 미끄럼 · 분리 없음 | SE 한 속도장 (붙음) | 같다 — 둘 다 SE–SE 분리는 못 한다 |

⇒ 이 논문은 후보 A 의 *"강체 + 연속체를 공개 도구로 결합할 수 있다"* 는 **존재 증명**이다.  후보 A 가 우리 압밀 (수백 AM · 300 MPa · 준정적) 에서 돈다는 증거는 **아니다**.

### ★ 7-B. 우리 압밀에 그대로 쓸 때 걸리는 것 [추정 · 검증 전]

1. **큰 강체 ↔ 고운 격자 (그림 5 의 함정)** — real_14 의 AM_P 반지름 ≈6 µm · 3D MPM 384 격자의 dx ≈141 nm (CLAUDE.md "격자 판정" · real_14 384) → AM_P 지름 ≈85 칸 [카드 산술].  구 하나가 합력 하나를 내는 이 결합에서는 AM 한 알의 넓은 SE 접촉면이 몇 노드에만 실린다 → 다발 (작은 구 수백 개 / AM) 이 필요하다 → AM 457 알이면 다발 구가 수만–수십만 개 [추정].
2. **외곽 추적** — 경계 입자는 처음 외곽에 두고 물질점을 따라 움직인다.  압밀 침대의 SE 는 공극 둘레 자유 표면이 무수히 많고 압축 중 닫힌다 (위상 변화).  처음 외곽 밖에서 새로 생기는 SE–AM 접촉면을 이 방식이 담는지 원문에 근거가 없다.
3. **약결합 안정** — 중력 흐름에서도 경계 입자를 몸 안쪽으로 δ 옮겨야 했다 (§4-3).  단단한 AM 과 무른 SE 가 300 MPa 로 맞붙는 준정적 압축에서 반복 없는 약결합의 안정 · 정확도는 시험된 적이 없다.
4. **얻는 것** — 암시 MPM (준정적) · DEM 쪽 AM–AM 접촉망 (우리 DEM 판독기와 같은 꼴) · 오픈소스.  후보 A 를 우리 코드로 짤 때 **"DEM 이 먼저 → 힘을 연속체로 → 연속체가 움직인 경계를 DEM 으로"** 라는 걸음 순서와 보존 사상 (Hᵀ) 을 설계 비교 기준으로 쓴다.

### 7-C. [DEM 우선 (수영)] 2D 49 원판 벤치마크와의 관계

- 49 원판 문제는 **무른 원판끼리** 다 (E 10 MPa · σ_y 0.4 MPa · `docs/reviews/suyoung_u6_first_development_20261118/README.md`).  이 논문의 DEM 쪽은 **단단한** 구라서 그 문제의 바깥 기준 (MPFEM) 이 될 수 없다 — 그 자리는 `zhou2019_…` · `huang2017_…` · `li2022_…` 카드의 MPFEM 몫이다.
- 1저자 11-25 MPFEM · Kratos 공부 메모 (리포 밖 · 1저자 결정 전) 의 권고 *"Kratos MPM–DEM 은 이번 시험에서는 뺀다 · 단단 + 무른 혼합을 볼 때 후보 A 와 견주는 자리로 둔다"* 와 이 카드 판정이 같다.

### 7-D. 판정 (frame [4] · [5])

- frame [5]: 역학 결합 방법 논문 · 전달 0.
- frame [4]: 검증이 해석해 · 문헌 수치해 · 문헌 실험 (모래 흐름) 이라 우리 계의 앵커가 아니다.  방법 선례로만 쓴다.

---

## 8. 적용 인사이트 (실행 가능한 순서)

1. **후보 A 설계 문서에 '결합 꼴 비교표' 를 둔다** — 단일 격자 결합 (HU18 꼴) ↔ 분할 결합 (이 논문 꼴) · 각 꼴의 힘 전달 자리 (노드 ↔ 외곽 경계 입자) · 반복 유무 · 같은 Δt 가정 (§7-A 표 재사용).
2. **큰 AM 의 '합력 하나' 문제를 단위 시험으로** — 강체 원판 하나를 무른 연속체에 눌러 박는 2D 시험에서 접촉 노드 수 · 스밈 깊이를 격자 크기 (지름당 칸 수) 로 잰다 (후보 A 의 U 시험 꼴) [제안].
3. **Kratos 를 쓸 때는 버전 · 응용 이름 · 입력을 먼저 고정** — 이 논문은 Version 8.0 (Zenodo 2020) 을 인용하고 응용 이름은 적지 않았다.  이 카드는 저장소를 열지 않았다 (이 세션에서 GitHub 저장소 접근 불가 · [미확인]).
4. **'모래 흐름' 검증을 압밀 근거로 옮기지 않는다** — 동역학 · 낮은 응력 (E 50 kPa) · 다발 2 개.

---

## 9. 인용 가능 문장 (deck/paper 용)

- *"in case of substantial stiffness differences between adjacent material points, … this approach suffers from significant loss of accuracy and, more importantly, this approach leads to a sticking and therefore unphysical contact behaviour without the consideration of expensive contact detection algorithms."* (p.2) — MPM 한 속도장 다재료의 붙음 (우리 MPM SE–AM 붙음과 같은 지적).
- *"a DEM particle i calculates one resulting contact force F_i,Contact … this could lead to an insufficient representation of the shared interface, possibly resulting in penetration of the MPM material into the DEM particle"* (p.12–13).
- 우리 문장 (한정어 포함): "단단한 이산 물체 (DEM) 와 무른 연속체 (MPM) 의 분할 결합은 KRATOS 에서 충격 · 중력 흐름 문제로 검증됐다 (Singer 외 2022).  고압 준정적 압밀 · 조밀 다입자 계의 선례는 아니다."

---

## 10. 주의 / 한계 (over-claim 방지 + **이 논문에 대한 비판**)

### 10-A. 우리가 전이할 때의 한계

- 동역학 · 낮은 응력 · 적은 DEM 물체 — 우리 300 MPa 준정적 · AM 수백 알과 다르다 (§7-B).
- 2D 모래 흐름 · 평면변형 Mohr–Coulomb — SE 의 J2 · 3D 와 다르다.
- DEM–MPM 경계 마찰 (모래 예제) 이 적혀 있지 않다.

### 10-B. ★ 이 논문 자체의 약점 (비판적으로)

1. **속도 숫자 불일치** — 빔 예제 처음 속도 본문 −0.01 cm/s ↔ 그림 6 의 1 cm/s.
2. **"24 × 8" 몸 메시** — 둘째 예제의 선분 240 개 · 첫째 예제의 120 × 8 과 견주면 인쇄 오류로 의심된다.
3. **수렴 · 민감도 시험이 없다** — 격자 · 몸 메시 · 경계 입자 간격 · δ · Δt 를 바꾼 시험이 없다.  약결합의 안정 조건 · 에너지 보존 (Eq. 24) 의 실측도 없다.
4. **β 정확도 주장** — 둘째 블록 β 의 평균 절대 오차는 이 논문 6.3° 로 Jiang 외 (5.0°) 보다 크다 [판독 + 카드 산술].  *"good agreement"* 는 맞지만 기존 해보다 낫다는 근거는 맨 위 블록 회전의 정성 그림 (그림 12) 뿐이다.
5. **안정화 손질** — 경계 입자를 몸 안쪽으로 δ 옮기는 것은 저자도 *"future research could investigate alternative solutions"* 라 적은 임시 처리다.
6. **Δt 단위 미기재** — 5e−8 · 5e−5 (초로 읽힘).

### 10-C. frame 규율 재확인

- 이 논문으로 후보 A 의 성능 · 정확도를 주장하지 않는다.  우리 쪽 시험 (단위 시험 → 2D → 3D) 은 각자 실험 · 해석해에 대고 한다 (frame [4]).

---

## 11. 관련 카드 (중복 서술 금지 — 겹치면 넘김)

- `hu2018_mls_mpm_cpic_two_way_rigid_coupling` — MLS-MPM 의 원전 + CPIC 강체 양방향 결합 (후보 A 의 단일 격자 꼴 선례).
- `bardenhagen2000_mpm_granular_multibody_frictional_contact` · `bardenhagen2001_mpm_improved_contact_granular_stress_waves` — MPM 다물체 마찰 접촉 (후보 A′-0 · A′ 부품).
- `guilkey2003_implicit_mpm_newton_quasistatic_fem_comparison` — 이 논문이 넓힌 암시 MPM [46] 의 계보.
- `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` — 장 2 개로 MPM 접촉 · 분리.
- `zhou2019_mpfem_2d_copper_powder_die_compaction_release` · `huang2017_mpfem_2d_binary_al_sic_hard_soft_compaction` · `li2022_mpfem_3d_soft_hard_composite_compaction_vibration_unloading` — 같은 날 묶음의 MPFEM 세 편 (2D 49 원판 바깥 기준 · 단단 + 무른 짝).

---

## 12. 용어 (technique mini-glossary)

- **분할 결합 (partitioned coupling)** — 풀이기 둘을 따로 두고 공유 경계에서만 자료를 주고받는 결합.  반대말 = 단일 (monolithic) 결합.
- **블랙박스 풀이기** — 속을 고치지 않고 입력 (경계 조건) · 출력 (경계 힘 · 변위) 만 쓰는 풀이기.
- **Dirichlet–Neumann 분할** — 한쪽 (DEM) 에는 변위 · 속도를, 다른 쪽 (MPM) 에는 힘을 경계 조건으로 주는 분할.
- **벽 조건 (wall condition)** — DEM 쪽에서 MPM 외곽을 나타내는 움직이는 벽 (2D 선분 · 3D 삼각형).
- **경계 입자 (boundary particles)** — MPM 에서 Neumann 경계를 나누는 질량 없는 점.  점하중을 받고 물질점처럼 움직인다.
- **보존 사상 (conservative mapping)** — 힘을 Hᵀ 로 옮겨 경계 위 일 (에너지) 을 보존하는 사상.
- **Gauss–Seidel 약결합** — 한 걸음에 DEM → MPM 순서로 한 번씩만 풀고 반복하지 않는 결합 (explicit coupling).
- **구 다발 (cluster)** — 여러 구를 붙여 한 강체를 만드는 DEM 표현.
- **HM+D** — Hertz–Mindlin 스프링 + 감쇠 접촉 모형.

---

## 🗨️ Q&A 로그

- (2026-11-25 · litdb-curator) 그림 11 의 축 눈금 글자는 글리프 경로라 텍스트로 안 읽혀, 모든 계열이 90° 에서 출발 · 실험이 0° 에서 끝난다는 점과 점선 보조 격자 간격 (17.2 pt = 10°) 으로 축을 맞췄다.  Kratos 저장소 · PyPI 는 이 카드가 열지 않았다.
