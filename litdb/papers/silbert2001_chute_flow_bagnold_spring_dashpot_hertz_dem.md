<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 형식 이웃 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md (절 · 머리 상자 · 의도 대조) ·
     계산 (DEM) 방법 절 꼴 = cantor2020_compaction_model_highly_deformable_particles.md · 같은 접촉 법칙 계보 = luding2008_cohesive_frictional_contact_models.md (우리 hooke/hysteresis 정의서).
     쪽 표기: p.N = 논문 번호 쪽 051302-N (PDF 14 쪽 = 인쇄 14 쪽 · 본문 p.1–13 · 참고문헌 p.13–14 · 보충 자료 안내 없음).
     값 표지: [인쇄] = 본문 · 표 · 캡션 · 그림 안 글자 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 94 행 · 원 래스터 300 dpi · 눈금 직선 보정 ·
     방법은 각 행 note) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 추론] · [카드 관찰] = 이 카드의 해석 · [미확인] = 원문 14 쪽에 없음.
     원문은 텍스트 층 + 쪽 렌더로 읽었다 — 텍스트 층은 Symbol 글꼴이 깨져 (θ → u · μ → m · ε → e · = → 5 · × → 3 · ( ) → ~ ! 등) 기호 · 부등호 · 지수는 전부 렌더로 확인했다. -->
# 경사면 중력 흐름 (chute flow) 의 2D · 3D DEM — `gran/hooke/history` · `gran/hertz/history` 로 인용되는 접촉력 꼴의 원문 (법선 스프링–감쇠 × f(δ/d) = 1 · √(δ/d) · 접선 탄성 변위 이력 u_t · Coulomb 절단 · k_t/k_n 2/7 · δt = t_col/50) + Bagnold 척도 (v ∝ H^1.52) · φ_max 2D 0.815 / 3D 0.590 — ⚠ 단분산 단단한 구 · 겹침 ~10⁻⁴–10⁻³ d · 법선 이력 일부러 뺌 · 고압 압밀 아님 — Silbert · Ertaş · Grest · Halsey · Levine · Plimpton (Phys. Rev. E 2001)

> slug `silbert2001_chute_flow_bagnold_spring_dashpot_hertz_dem` · DOI `10.1103/PhysRevE.64.051302` · type `DEM (자체 MD 코드 · contact law 원문 · 2D 원판 + 3D 구 · 단분산 · Model L 선형 스프링–감쇠 · Model H Hertz · 접선 이력 + Coulomb 절단 · 중력 경사면 흐름 · 주기 경계 · N 200–24,000)` · PDF `ba72a247-71._Granular_flow_down_an_inclined_plane_Bagnold_scaling_and_rheology.pdf` · digested `2026-11-16` · status ✅
>
> **저자**: **Leonardo E. Silbert**¹ · **Deniz Ertaş**² · **Gary S. Grest**¹ · **Thomas C. Halsey**² · **Dov Levine**³ · **Steven J. Plimpton**¹ — ¹ Sandia National Laboratories (Albuquerque, NM 87185) · ² Corporate Strategic Research, ExxonMobil Research and Engineering (Annandale, NJ 08801) · ³ Department of Physics, Technion (Haifa 32000) · 교신 저자 표시 없음 · *Phys. Rev. E* **64**, 051302 (2001) · 14 쪽 (051302-1 – 051302-14) · Received 28 March 2001 · published 25 October 2001 · PACS 46.55.+d · 45.70.Cc · 46.25.−y · 자금 = Israel Science Foundation Grant No. 211/97 (D.L.) · Sandia = DOE Contract No. DE-AC04-94AL85000 (p.13).
> **이웃 카드 (링크만)**: 이 논문을 인용한 카드 — [`benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem`](benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem.md) (ref 34 · L222 · L445 = 고른 의도의 출처) · [`haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem`](haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem.md) (ref 30 · Δt 규칙) · [`shi2019_high_am_loading_particle_size_assb`](shi2019_high_am_loading_particle_size_assb.md) (본문 [22]) — 우리 압축 덱 접촉 법칙의 정의서 [`luding2008_cohesive_frictional_contact_models`](luding2008_cohesive_frictional_contact_models.md) · 강성 낮추기 [`lommen2014_dem_speedup_contact_stiffness_reduction_bulk_behavior`](lommen2014_dem_speedup_contact_stiffness_reduction_bulk_behavior.md).
> **판독 원자료**: `litdb/figures/silbert2001_chute_flow_bagnold_spring_dashpot_hertz_dem/digitized.csv` (94 행 — Fig. 2 · 5 · 9b · 11 · 12 · 15b · 16 · 18 · 19 · 20) · 크롭 63 장 (그림 20 = 전부 다시 자름 · 표 1 · 식 22 · 근거 문단 20) — `figures.json`.
>
> ⚠⚠ **먼저 읽을 것 — 다섯 겹의 전이 금지**: ① **중력으로 흐르는 정상 상태 (경사면 · chute)** 이지 판으로 누르는 준정적 고압 압밀이 아니다 (탈압 없음) · ② **단분산 단단한 구** (지름 d · 질량 m) — 겹침은 점접촉 근사가 맞는 아주 작은 영역 (바닥 최대 하중에서도 δ/d ≈ 3 × 10⁻⁴ (Model L) · 4 × 10⁻³ (Model H) [카드 산술 · 자릿수 · §3-5]) · ③ 모든 양이 **무차원** (d · √(d/g) · mg) — 재료 · 절대 압력이 없다 · ④ 법선 접촉의 **재하 / 제하 이력을 일부러 뺐다** (*"We ignore hysteretic effects between loading or unloading normal contacts"* p.4) — 우리 압축 덱 `hooke/hysteresis` 의 핵심 부분과 **다른 법칙** · ⑤ 2D 결과는 단분산 원판이 멈출 때 **결정화**해 이력 · 정지 거동이 3D 와 다르다 (p.3 · p.6).
> ⇒ **절대값 전이 0 건.**  가져오는 것 = (a) 접선 이력 (u_t) · Coulomb 절단 · 스프링–감쇠 · Hertz 배율 f(δ/d) 의 **원문 식과 매개변수 관례** (식 2–11 · 표 I) (b) 시간 간격 규칙 δt ≈ t_col/50 과 ε ↔ γ_n 의 닫힌 꼴 (식 10–11 — 단위 시험 U5 의 기대값) (c) "강성을 낮춰도 된다" 는 근거의 **조건** (중력 하중 · k_n 이 충분히 클 때 · 밀도는 둔감 · 속도는 민감) (d) 2D ↔ 3D 차이의 실증 목록.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 단분산 구 (3D) · 원판 (2D) 을 거친 바닥 위에 쌓고 중력을 θ 만큼 기울여 흐르게 한 대규모 DEM (자체 MD 코드 · N 200–24,000 · δt = 10⁻⁴ √(d/g)) 에서, **선형 스프링–감쇠 (Model L) 와 Hertz (Model H) 법선력 + 접선 탄성 변위 u_t 이력 + Coulomb 절단** 으로 정상 흐름을 만들고, 깊이에 무관한 일정 충전율 · Bagnold 척도 (σ_xz ∝ γ̇² · v ∝ H^1.52±0.05) · 접촉이 응력을 나른다는 것 (운동 몫 ≈1 %) 을 보인다 — 접촉 법칙의 세부 (k_t/k_n · γ_t · μ · ε · k_n) 에 **밀도는 둔감, 속도는 민감**하다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 접촉력 식 (원문) | 식 (2)–(7): δ_ij = d − r_ij · F_n = f(δ/d)(k_n δ n − γ_n m_eff v_n) · F_t = f(δ/d)(−k_t u_t − γ_t m_eff v_t) · du_t/dt = v_t − (u_t·v_ij) r_ij / r_ij² · f(x) = 1 (Model L) / √x (Model H) · ‖F_t‖ ≤ μ‖F_n‖ 가 되게 u_t 를 잘라 냄 ("proportional loading") | [인쇄] p.4–5 · `eq_02`–`eq_07` · `txt_p5_coulomb_*` |
| ② 매개변수 (표 I) | k_n = 2 × 10⁵ mg/d (세 모델 같음) · γ_n = 33.5 (L2) / 50.0 (L3 · H3) · k_t/k_n = 2/7 · γ_t/γ_n = 0 · μ = 0.50 · ε = 0.92 (L2) / 0.88 (L3) / 속도 의존 (H3) · δt = 10⁻⁴ t_o | [인쇄] p.4–5 · `tab_1` |
| ③ 시간 간격 · 반발 계수 규칙 | t_col = π(2k_n/m − γ_n²/4)^(−1/2) · ε_n,t = exp(−γ_n,t t_col/2) · *"an accurate simulation typically requires δt ~ t_col/50"* — 표 I 값으로 t_col = 4.97 × 10⁻³ t_o · ε 0.920 (L2) · 0.883 (L3) 재현 · t_col/δt = 49.7 | [인쇄] p.4 · [카드 산술] §3-5 |
| ④ 강성을 낮춘 이유와 근거 | 유리 d = 100 µm 이면 k_n^glass = O(10¹⁰) → 시간 간격이 너무 작아 대규모 계산 불가 → **k_n = O(10⁵)** (≈5 × 10⁴ 배 무름 [카드 산술]) · k_n 2 × 10⁴ – 2 × 10⁶ 시험: *"the effect of variations in k_n is minimal, provided k_n is sufficiently large"* | [인쇄] p.4 · p.8 · Fig. 11 |
| ⑤ 단단한 구 · 작은 겹침 가정 | *"large enough to avoid grain interpenetration"* (p.4) · *"pile of stiff objects … controlled by aspects of geometrical packing, rather than the specific form of the stiff force laws"* (p.12) — 겹침 크기는 원문에 없다 [미확인] · 카드 어림 δ/d ~10⁻⁴–10⁻³ (L) · ~10⁻³–10⁻² (H) | [인쇄] · [카드 산술] §3-5 |
| ⑥ 소성 · 큰 변형 | **없다** — 입자 형상 고정 · 법선 이력 (잔류 겹침) 없음 · '소성' 은 연속체 Coulomb 항복 (Mohr–Coulomb) 비교에만 나온다 (p.10–11) | [인쇄] |
| ⑦ 2D ↔ 3D | 둘 다 계산 · 같은 꼴 (일정 밀도 · Bagnold · α 1.52) 이지만 2D 는 정지 때 결정화 → 큰 이력 · A_Bag 불연속 · 표면 항복 거동 반대 · 충전율은 면적 ↔ 부피 분율이라 숫자 비교 불가 (0.815 ↔ 0.590) | [인쇄] p.3 · p.8 · p.11–12 · §4-10 |
| ⑧ 탈압 | **없다** (흐름 · 정지 · 재시작의 각도 이력만) | — |
| ⑨ 우리 덱과의 관계 | 압축 덱 `hooke/hysteresis` (Luding 2008 계열 이력 스프링) 의 **법선 부분은 이 논문 꼴이 아니다** (원문이 뺀 바로 그 이력) · `tangential history` 는 같은 부류 · 믹서 덱 `hertz tangential history` 는 Model H 계열 + 점착 · 구름 저항 (원문에 없음) | 정본 카드 표기 · §4-9 |

⛔ **한정어 (떼지 말 것)**: ① 정상 중력 흐름 (응력 = 자기 무게 · 바닥 σ_zz ≈ 40 mg/d² [카드 산술]) ② 단분산 · 단단한 구 · 점착 없음 ③ 무차원 (재료 없음 · 유리 예는 강성 설명용 한 줄) ④ 법선 이력 없음 (ε 는 감쇠로만) ⑤ 2D 는 '투영된 구' (원판 · xz 평면 운동).
⇒ **절대값 전이**: 없음.  **방법 · 규칙 전이**: 접촉 꼴 · 시간 간격 · ε–γ 관계 · 매개변수 민감도의 '방향' (밀도 둔감 · 속도 민감) — 단 그 둔감성은 **겹침 ~10⁻⁴ d 인 중력 영역에서** 확인된 것이고, 우리 압축 (⟨δ⟩/d ≈ 0.11) 은 그 25–400 배 겹친 영역이다 [카드 산술 · §8-4].

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-71 의 '왜' 칸)

의도 원문 (S8 N-71): *"후보 D0 (접촉 법칙 원전) — 'gran/hertz/history 꼴 원전'"* · 근거 = `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` L445 (*"카드 없음 — gran/hertz/history 꼴 원전"*).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "gran/hertz/history 꼴" — Hertz 법선 + 접선 이력 + 마찰 | **채움 (꼴)** | 식 (6)·(7) 에 f(x) = √x (Model H) · 접선력은 저장된 탄성 접선 변위 u_t (식 5 · 접촉 시작 때 0 · 접촉 수명 동안 추적) 에서 · ‖F_t‖ ≤ μ‖F_n‖ 이 되게 u_t 를 잘라 냄 (p.5) · 감쇠도 f(δ/d) 를 곱함 · Model H 의 ε 는 충돌 속도에 따라 다름 (p.4) [인쇄] · 조건 = 3D · 단분산 · 중력 흐름 · μ 0.50 |
| 같은 꼴의 선형판 (`gran/hooke/history`) | **채움** | Model L = f(x) = 1 (선형 스프링–감쇠) — 이 논문의 주 모델 (L2 · L3) [인쇄] p.4 |
| "원전" (그 접촉 법칙을 처음 세운 논문) | **일부** | 원문 스스로 *"essentially a reduced version of that employed by Walton and Braun [22], developed earlier by Cundall and Strack [28]. More recent versions of these models now exist [31–33]"* (p.4) — 처음 세운 논문이 아니라 **줄인 판의 기준 구현**이다.  LAMMPS 쌍 퍼텐셜 이름 (`gran/hertz/history`) 은 원문 14 쪽 어디에도 없다 (텍스트 검색 0 회) — 이름 대응은 인용하는 쪽 (benhadjali2026 · shi2019 카드) 의 것 |
| 후보 D0 = "지금의 DEM (구 · 탄성-이력 접촉 · 무르게 맞춘 영률)" 의 접촉 법칙 원전 | **일부 — 법선 이력은 없음** | 원문: *"We ignore hysteretic effects between loading or unloading normal contacts and we do not differentiate between frictional directions at the same contact point at different time steps as does Walton [23]."* (p.4) → 우리 압축 덱 `hooke/hysteresis` 의 법선 이력 (k₁ 재하 · k₂ 제하 · 잔류 겹침 δ₀ — `luding2008` 카드 L80–104) 은 이 논문에 **없다** (그 계보 = Walton–Braun 1986 [22] → Luding 2008 · `luding2008` 카드 머리 *"Walton–Braun 1986 … 을 대체하는 공개·완전판"*).  `tangential history` (접선 이력 + Coulomb) 는 같은 부류 |
| 매개변수 값 (D0 덱 감사용) | **채움** | 표 I (k_n · γ_n · k_t/k_n · γ_t/γ_n · μ · ε) · δt = 10⁻⁴ (k_n = 2 × 10⁵ 일 때) · δt ~ t_col/50 · 시험 범위 (k_n 2 × 10⁴–2 × 10⁶ · μ 0.15–1.0 · ε 0.58–0.98 · k_t/k_n 2/7 ↔ 2/3 · γ_t 0 ↔ γ_n) [인쇄] p.4–5 · p.8 |
| E · ν 로 강성을 세는 Hertz 매개변수화 | **없음** | k_n 은 무차원 스프링 상수 (mg/d 단위) · E · ν 는 원문 계산에 없다 — Poisson 비는 *"For Hertzian contacts [37], the ratio k_t/k_n depends on the Poisson ratio of the material, and is about 2/3 for most materials"* 한 문장뿐이고 실제로는 2/7 을 썼다 (p.5) |
| 다분산 배율 √(R_iR_j/(R_i+R_j)) | **없음** | 원문 배율은 단분산 지름 d 하나의 f(δ_ij/d) = √(δ_ij/d) — 크기가 다른 입자 쌍의 유효 반지름 식은 원문에 없다 |
| 가리킨 카드의 **2 차 인용 ①** — `benhadjali2026` L222: *"F^{GH} = √δ · √(R_iR_j/(R_i + R_j)) · [(K_n δ n_ij − m_eff γ_n v_n) − (K_t Δs_t + m_eff γ_t v_t)] … Hertz 는 겹칠 때만 · Silbert 2001 [34]"* | **꼴은 같음 · 배율 다름 (카드 문제 아님)** | 원문 식 (6)·(7) 과 같은 항 (탄성 · m_eff 감쇠 · 저장된 접선 변위 · 감쇠) — 같은 크기 구 (R_iR_j/(R_i+R_j) = d/4) 이면 √δ·√(d/4) = (d/2)√(δ/d) 라 **K_n = 2k_n/d 의 상수배** [카드 산술] · 다분산 R_eff 꼴은 원문에 없다 (그 논문 식 4–11 을 카드가 옮긴 것 — 귀속은 그 논문 몫) |
| 2 차 인용 ② — `benhadjali2026` L445 서지 | **같음** | "L.E. Silbert, D. Ertaş, G.S. Grest, T.C. Halsey, D. Levine, S.J. Plimpton, … Phys. Rev. E 64 (2001) 051302 · DOI" = 원문 첫 쪽과 같다 |
| 2 차 인용 ③ — `haervig2017` L141 · L298 *"시간 간격 지침은 Silbert [30] 의 Δt_col/δt ≈ 50"* | **같음** | 원문 p.4 *"δt ~ t_col/50"* · 표 I 로 t_col/δt = 49.7 [카드 산술].  ⚠ 그 카드 L298 서지 *"Phys. Rev. (2001) 051302"* 에 'E 64' 가 없다 — 그 카드가 haervig 원문 목록을 옮긴 것이라 적혀 있고 이 카드는 haervig PDF 를 대조하지 않았다 |
| 2 차 인용 ④ — `shi2019` L169–173: *"[22] = Silbert et al., Phys. Rev. E 2001, 64, 051302"* (*"normal and tangential interactions and damping forces"* 의 근거) · SI 식 *"F_ij = √δ·√(R_iR_j/(R_i+R_j))·[(k_n δ n_ij − γ_n (v·n_ij) n_ij) + (k_t δ t_ij − γ_t (v·t_ij) t_ij)]"* | **서지 · 귀속 같음 · 그 SI 식은 원문 꼴과 세 곳이 다름 (카드 문제 아님)** | 원문과 다른 점: (i) 감쇠에 m_eff 가 없다 (ii) 접선 스프링이 저장 변위 u_t 가 아니라 'δ t_ij' (iii) 접선 스프링 부호 + (원문 −k_t u_t) — shi2019 카드가 *"부호 규약·접선 변위를 δ 로 쓴 것 모두 인쇄 그대로"* 라 적었으므로 그 논문 SI 의 표기 문제 |

⇒ **의도 대조 결과: 일부** — Model H (f = √(δ/d)) + 저장 접선 변위 u_t + Coulomb 절단 = `gran/hertz/history` 꼴의 원문 식 · 매개변수 · 시간 간격 규칙은 **채움**; 그러나 원문은 스스로 Walton–Braun · Cundall–Strack 의 **줄인 판** 이라 하고, 우리 D0 압축 덱의 **법선 이력은 일부러 뺐으며**, LAMMPS 이름 · 다분산 R_eff 배율 · E · ν 매개변수화는 원문에 **없다**.

---

## 1. 한 줄 요약

**KR:** 거친 바닥 (3D = 무작위 구 한 겹 ≈1.2 d · 2D = 지름 2d 구의 규칙 배열) 위의 단분산 입자 더미 (3D N 1000–24,000 · 2D N 200–20,000 · x · y 주기) 를 중력 기울기 θ 로 흐르게 하는 자체 MD 코드 (3 차 Gear 예측–수정 또는 속도-Verlet · δt = 10⁻⁴ t_o · MPI 공간 분할) 로, 선형 스프링–감쇠 (Model L · 2D L2 · 3D L3) 와 Hertz (Model H · 3D H3) 접촉 + 저장 접선 변위의 Coulomb 절단을 써서 (θ, H) 상 그림 (흐름 없음 · 정상 · 불안정) 을 그리고, 정상 흐름에서 깊이에 무관한 충전율 (θ 가 안식각 θ_r 로 갈수록 φ_max 2D 0.815(5) · 3D 0.590(5)), Bagnold 속도 단면과 척도 v ∝ H^α (α = 1.52 ± 0.05), 응력의 99 % 가 지속 접촉에서 온다는 것, 3D 에서 σ_yy 가 15–20 % 작다는 것, 작고 부호가 바뀌는 법선 응력 이상 χ, 안식각에서 몸통은 Coulomb 항복에 가지 않고 3D 표면만 가까이 간다는 것을 보인다.  접촉 매개변수 (μ · ε · k_n · k_t/k_n · γ_t) 를 바꿔도 **밀도는 거의 안 바뀌고 속도는 바뀐다** — 저자는 이것을 *"geometrical packing"* 이 지배한다는 근거로 읽는다.

**EN:** Large-scale MD/DEM of monodisperse spheres (3D) and disks (2D) flowing down a rough incline under gravity, with linear spring-dashpot (Model L) or Hertzian (Model H) normal forces, a stored elastic tangential displacement truncated at the Coulomb limit, k_t/k_n = 2/7, γ_t = 0, δt = 10⁻⁴√(d/g) ≈ t_col/50; steady flow shows depth-independent packing fraction (φ_max 0.815 in 2D, 0.590 in 3D at the angle of repose), Bagnold rheology σ_xz ∝ γ̇² and v ∝ H^1.52±0.05, contact-dominated stress (kinetic part ≈1 %), and a weak, sign-changing normal-stress anomaly; bulk density is insensitive to interaction parameters while velocities are not.

**우리에게 왜 중요한가 (3 줄):** ① 우리 두 덱이 쓰는 **`tangential history` + Coulomb 절단 · Hertz 배율 · m_eff 감쇠의 원문 꼴** — D0 덱 감사의 기준 문서 (§4-9).  ② **"강성을 낮춰도 밀도는 둔감" 의 원문 근거와 그 조건** — 중력 하중 (겹침 ~10⁻⁴ d) 에서 k_n 2 × 10⁴–2 × 10⁶ 를 본 것이지 고압 압밀이 아니다 → 우리 18 배 연화의 근거로 옮기면 안 된다 (§8-4).  ③ **2D ↔ 3D 가 같은 꼴이어도 정지 · 이력 · 표면 거동은 다르다** 는 한 논문 안의 실증 (§4-10).

## 2. 메타

| 항목 | 내용 |
|---|---|
| 제목 | Granular flow down an inclined plane: Bagnold scaling and rheology |
| 저자 · 소속 | 위 머리 상자 (6 명 · Sandia 3 · ExxonMobil 2 · Technion 1) |
| 저널 | *Physical Review E* **64**, 051302 (2001) · 14 쪽 · ©2001 APS · 1063-651X/2001/64(5)/051302(14) |
| DOI | 10.1103/PhysRevE.64.051302 (첫 쪽 인쇄) |
| 날짜 | Received 28 March 2001 · published 25 October 2001 |
| 코드 | 자체 MD 코드 (이름 없음) · 직렬판 + MPI 병렬판 (공간을 3D 하위 블록으로 나눔 · 방법 = ref [40] Plimpton, J. Comput. Phys. 117, 1 (1995)) — 코드 이름 · 공개 여부 [미확인] |
| 계산 자원 | 500-MHz DEC Alpha (직렬) · Alpha/Myrinet 클러스터 8 프로세서 (병렬) |
| 그림 · 표 · 식 · 문헌 | 그림 **20** · 표 **1** (TABLE I) · 식 **(1)–(22)** · 참고문헌 **49** (주석형 [34] · [41] · [46] · [47] 포함) |
| SI | 없음 (본문 · 참고문헌에 보충 자료 안내 없음) |
| 소재 | **모델 입자** — 단분산 구 / 원판 · 점착 없음 · 재료 이름 없음 (유리 d = 100 µm 는 강성 설명의 예 한 줄) · ⛔ SE · CAM 아님 |
| 연구 유형 | 수치 (DEM/MD · 2D + 3D) + 연속체 해석 (Cauchy · Mohr–Coulomb · Bagnold) · 실험 없음 (실험과는 α 하나를 견줌 — ref [29] Pouliquen) |
| 1저자 메모 · 후보 표 서지 대조 | 저자 6 · 제목 · Phys. Rev. E 64 (2001) 051302 · DOI — **원문과 같다 (다른 점 없음)** |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 표 I — 표준 계산 세트 (p.4 · `tab_1`) + 이 카드의 재현 산술

| 모델 | D | f(x) | k_n [mg/d] | γ_n [1/t_o] | k_t/k_n | γ_t/γ_n | μ | ε | t_col [t_o] [카드 산술 · 식 11 · m = 1] | ε 재현 [카드 산술 · 식 10] |
|---|---|---|---|---|---|---|---|---|---|---|
| L2 | 2 | 1 | 2 × 10⁵ | 33.5 | 2/7 | 0 | 0.50 | **0.92** | 4.969 × 10⁻³ | **0.920** |
| L3 | 3 | 1 | 2 × 10⁵ | 50.0 | 2/7 | 0 | 0.50 | **0.88** | 4.971 × 10⁻³ | **0.883** |
| H3 | 3 | √x | 2 × 10⁵ | 50.0 | 2/7 | 0 | 0.50 | (속도 의존 · 값 미인쇄) | — | — |

- 단위 (p.4 · `txt_p4_units_*`): 길이 d · 시간 t_o = √(d/g) · 속도 v_o = √(gd) · 힘 F_o = mg · 탄성 상수 k_o = mg/d · 응력 σ_o = mg/d².  γ_n 의 단위는 원문에 없다 — γ_n m_eff v 가 힘이므로 1/t_o [카드 추론].
- **δt = 10⁻⁴ t_o (k_n = 2 × 10⁵)** [인쇄 p.5] → t_col/δt = **49.7** [카드 산술] = 원문 규칙 *"δt ~ t_col/50"* (p.4) 과 맞다.  표 I 의 ε 두 값을 식 (10)·(11) 로 그대로 재현한다 (m_eff = m/2 → ω² = 2k_n/m).
- γ_t = 0 이면 식 (10) 의 ε_t = 1 (접선 감쇠 없음) [카드 산술].  Model L 의 ε 는 충돌 속도에 무관 · Model H 는 속도 의존 (p.4).
- k_t/k_n = 2/7 의 이유: *"makes the period of normal and shear contact oscillations equal to each other for Model L [38]"* (p.5) · Hertz 이론값은 Poisson 비에 따라 ≈2/3 (p.5).

### 3-2. 그 밖의 계산 설정 (p.2–6)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 적분 | 3 차 Gear 예측–수정 **또는** 속도-Verlet [39] (어느 그림이 어느 적분기인지 [미확인]) | [인쇄] p.5 |
| 정상 상태 도달 | 정지에서 출발해 **1–2 × 10⁷ δt** (N < 10,000) · 2D 최대 (H = 200) **2–5 × 10⁸ δt** = 1,000–2,000 · 20,000–50,000 t_o [카드 산술] | [인쇄] p.5 |
| 비용 | 500-MHz DEC Alpha 에서 3D 8000 입자 10⁷ 걸음 ≈5 일 (≈1.9 × 10⁵ 입자·걸음/s [카드 산술]) · 8 프로세서에서 같은 계 1.5 × 10⁷ 걸음/일 (병렬 효율 ≈0.94 [카드 산술]) · 프로세서당 ≈1000 입자면 효율이 높다 | [인쇄] p.5 |
| 3D 기하 | x (흐름) · y (와도) 주기 · 고정된 거친 바닥 (이전 충전 상태에서 RCP 에 가까운 면적 분율의 조각 ≈1.2 d 두께 — *"glue … particles are then sprinkled"* 실험의 흉내) · 위는 자유면 · N 1000–20,000 (Fig. 1 은 N 24,000 · 바닥 20 × 20 d) · H ≡ Nd²/A (단순 입방 격자로 평면에 쌓은 높이) · 예: N 8000 · L_x 20d · L_y 10d → H 40 (실제 높이 ≈37) · 최대 H 100 | [인쇄] p.3 · p.5 |
| 2D 기하 | 운동이 xz 평면으로 제한된 '투영된 구' · 바닥 = 지름 2d 구의 규칙 배열 · 주기 x = 100d (큰 입자 50 개) · 2 ≤ H ≤ 200 (N 200–20,000) · H ≡ Nd/L | [인쇄] p.4 · p.5 |
| 기울이기 | 중력 벡터를 xz 평면에서 θ 만큼 돌림 (z = 자유면의 법선 · 흐름은 +x) | [인쇄] p.5 |
| 출발 상태 | 2D = 삼각 격자 → θ 를 올려 흐름이 시작될 때까지 (θ ≳ 23° 에서만) · 3D = 무작위로 비운 단순 입방 격자 → θ = 30° 로 무질서화 · 정착 → 원하는 θ 로 낮춤 | [인쇄] p.5 · `txt_p5_p6_*` |
| 정상 상태 정의 | *"the energy input from gravity balances that dissipated from friction and collisions, so that the total kinetic energy of the system reaches a macroscopically constant value"* · 24–30° 로 흐름을 일으켜 구성 이력을 지움 | [인쇄] p.2 · `txt_p2_*` |
| 응력 | 표본 부피 V 안 입자의 접촉 (virial) 항 + 운동 항 (식 12 · 시간 평균 속도를 뺌) | [인쇄] p.5 |

### 3-3. 결과 수치 — 본문 · 캡션에 인쇄된 값

| 양 | 값 | 조건 | 쪽 |
|---|---|---|---|
| 최대 충전율 (안식각에서) | **φ_2D^max = 0.815(5)** · **φ_3D^max = 0.590(5)** | θ_r,2D ≈ **17.8°** · θ_r,3D ≈ **19.4°** · 정상 흐름 · 선형 외삽 | p.8 |
| 3D 정지 충전율 | **0.595** | θ < θ_r 로 낮춰 멈춘 뒤 · 유동층 실험과 비슷 [44] | p.8 |
| 2D 정지 | 다결정 삼각 격자 · **φ_2D ≃ 0.9** | θ < θ_r | p.8 |
| 이상 미끄럼 층 | 2D 정사각 π/4 ≈ **0.79** · 3D π/(3√3) ≈ **0.60** | 자유면에 나란한 최밀 선 / 면의 흐름 가정 | p.9 |
| Bagnold 지수 | **α = 1.52 ± 0.05** (⟨v²⟩^1/2 ∝ H^α) | 2D 20° (μ 0.50 · 0.25) · 3D H3 24° · 실험 [29] 과 맞다 | p.12 · 초록 |
| 운동 (ballistic) 응력 몫 | **≈1 %** | 정상 흐름 | p.12 |
| σ_yy 결손 | xx · zz 보다 **15–20 %** 작음 | 3D | p.11 |
| 표면 유변 층 | **5d–8d** (지수 감쇠 길이 1.3–2.2d) | 3D H3 H40 (Fig. 13b) | p.10 |
| 일정 밀도 구간 | 3D **≈40 층** · 2D **100 층** | Fig. 4 | p.7 |
| Bagnold 꼴 성립 | 위 5–8 층 아래 · 바닥에서 떨어진 곳 · **H ≳ 20** (그보다 얇으면 비-Bagnold) | Fig. 7 · 8 · 17 | p.8 · p.11 |
| 2D 최대 안정 각 | ε 0.92 → 0.82 로 낮추면 **≈23° → 26°** | 2D | p.3 |
| 2D 처음 흐름 | 삼각 격자는 **θ ≳ 23°** 에서만 흐름 시작 | 2D 출발 | p.5 |
| 접선 절단 시험 | u_t 를 자르지 않으면 평균 KE 가 커짐 — 자른 쪽이 **≈18 %** 작다 | L2 | p.5 |
| k_t/k_n 시험 | 2/3 이면 평균 KE **+≈10 %** · 밀도 · 응력 그대로 | — | p.5 |
| γ_t 시험 | γ_t = γ_n 이면 KE **−≈8 %** · 정상 상태에 더 빨리 · 나머지 그대로 | — | p.5 |
| 불안정 조합 | μ ≈ 0.10 + ε ≈ 0.96 (2D) / 0.98 (3D) | — | p.8 |
| 동마찰만 (u_t = 0 · 접선 속도 감쇠만) | **정상 흐름이 한 번도 안 나옴** | 2D · ref [34] 주석 | p.13–14 |

### 3-4. ★ 그림 판독 (전부 [판독] · 방법 = digitized.csv note)

**Fig. 12 — 정상 흐름 몸통 충전율 φ(θ)** (`fig_12`)

| θ | 18° | 19° | 20° | 21° | 22° | 23° | 24° | 25° | 26° |
|---|---|---|---|---|---|---|---|---|---|
| L2 (2D · 면적 분율) | 0.814 | 0.802 | 0.789 | 0.771 | 0.747 | 0.709 | — | — | — |
| L3 (3D · 부피 분율) | — | — | 0.591 | 0.586 | 0.579 | 0.573 | 0.567 | 0.561 | 0.555 |
| H3 (3D · Hertz) | — | — | ≈L3 (겹침) | — | ≈L3 | — | ≈L3 | — | **0.531** |

- 3D 에서 Hertz (H3) 와 선형 (L3) 이 20–24° 에서 표지가 겹친다 (차 ≲ 0.005) · 26° 에서만 H3 가 0.024 낮다 (불안정 경계 근처 · Fig. 4b 의 H3 26° 속도도 L3 보다 크다).
- 2D 는 θ 1° 마다 φ 가 0.012–0.038 내려가고 23° 근처에서 빨라진다 · 3D 는 ≈0.006/° 로 거의 직선.

**Fig. 18 — Bagnold 진폭 A_Bag(θ)** (`fig_18`): L2 0.080 (18°) · 0.130 · 0.175 · 0.225 · 0.280 · 0.355 (23°) / L3 0.041 (20°) · 0.115 (22°) · 0.207 (24°) · 0.256 (26°) / H3 ≈0.024 · ≈0.105 · ≈0.201 · 0.370 (26°) — 3D 는 θ_r 에서 0 으로 이어지고 2D 는 18° 에서 0.08 에 끊긴다 (원문 *"finite jump"*).

**Fig. 20 — 평균 순간 배위수 Z_c(θ)** (`fig_20`): 3D L3 H40 = 3.23 (20°) · 2.52 · 1.93 · 1.66 · 1.23 · 1.09 · 0.91 · 0.66 · ≈0.51 (≈28°) / 2D L2 H100 = 0.90 (19°) · 0.70 · 0.53 · 0.41 · 0.31 (23°).  ⚠ 정규화 — 원문 *"for a static 2D triangular lattice … the value would be 3"* (= 입자당 접촉 수 N_c/N = Z/2) 와 *"for 3D static packings, one might expect a value between 4–6 [48]"* (= 보통의 Z) 가 같은 정규화로 읽히지 않는다 [카드 관찰 · §12-B].

**Fig. 16 — 법선 응력 이상 χ = (σ_zz − σ_xx)/σ_zz** (`fig_16`): L2 +0.034 (19°) · ≈+0.054 (20°) · ≈+0.057 (21°) · +0.040 (22°) · +0.004 (23°) / L2 (ε 0.82) +0.039 … −0.019 (26°) / L3 +0.015 (20°) → −0.031 (26°) / H3 +0.028 (20°) → −0.026 (26°) — 크기 ≤ 0.06 · 부호가 θ 에 따라 바뀜 (원문 *"neither monotonic in θ nor of a specific sign"*).

**Fig. 15b — 응력 성분 (L3 · H 40 · 22°)** (`fig_15`): σ_xx ≈ σ_zz = 35.2 (z 3) · 29.0 (z 10) · 19.5 (z 20) · 10.1 (z 30) mg/d² (직선 · 0 점 z ≈ 41) · σ_yy = 29.9 · 24.8 · 16.6 → **σ_yy/σ_xx ≈ 0.85** (원문 *"smaller … by 15–20%"* 의 아래 끝) · σ_xz/σ_zz = **0.40** = tan 22° (식 16 확인).

**Fig. 11 — k_n 민감도 (L2 · 20° · H 50)** (`fig_11`): 몸통 φ ≈ **0.782** (k_n 2 × 10⁴ · 선 모양으로 배정 · 낮은 신뢰) ↔ **0.789–0.794** (2 × 10⁵ · 2 × 10⁶) · 자유면 근처 v_x ≈ **29** (2 × 10⁴) ↔ **24** (2 × 10⁵ · 2 × 10⁶).  ⇒ 10 배 무르게 하면 밀도 −≈0.01 · 표면 속도 +≈20 % · 10 배 단단하게 하면 거의 그대로 [카드 산술].

**Fig. 9b — μ 민감도 (L3 · 22° · H 40)** (`fig_9`): z ≈ 40.6 에서 v_x = **≥28** (μ 0.15 · 패널 위 끝에 닿아 잘렸을 수 있음) · **17.5** (0.25) · **8.3** (0.50) · **4.4** (1.00) · 몸통 φ 0.573–0.581 — 마찰은 속도를 ≈6 배 바꾸고 밀도는 ≈0.01 안.

**Fig. 19 — Bagnold 척도** (`fig_19`): 3D 점 H 20 · 30 · 40 · 50 · 80 · 100 · 200 → ⟨v²⟩^1/2 3.63 · 7.01 · 9.99 · 14.3 · 29.9 · 43.3 · 128 · log–log 기울기 **1.55** [카드 산술] (원문 1.52 ± 0.05 안).

**Fig. 2 — 상 그림** (`fig_2`): 2D H 50 = 흐름 없음 17.0° · 정상 17.5–23.0° · 불안정 24°– / 3D H 40 = 흐름 없음 ≤ 19° · 정상 20–27° · 불안정 27.5° / 3D H 5 = 흐름 없음 ≤ 23° · 정상 24.5–29.5° · 불안정 30° — 얇을수록 안식각이 올라간다.

**Fig. 5 — 수직 확산**: ⟨z²⟩(t ≈ 19.8 t_o) = 3.55 (23°) · 2.82 (22°) · 1.96 (21°) d² → D_z = ⟨z²⟩/2t ≈ 0.090 · 0.071 · 0.049 d²/t_o [카드 산술 · 직선 확산 가정 = 원문 *"well-defined diffusive motion"*].

### 3-5. [카드 산술] 확인 계산

| 계산 | 식 · 입력 | 결과 |
|---|---|---|
| t_col · ε 재현 | 식 (11) · (10) · 표 I (m = 1) | 4.97 × 10⁻³ t_o · ε 0.920 / 0.883 = 표 I 의 0.92 / 0.88 · t_col/δt 49.7 |
| 강성을 낮춘 배수 | k_n^glass / k_n = O(10¹⁰) / (2 × 10⁵) | **≈5 × 10⁴** (우리 DEM 18 배의 ≈2,800 배) |
| 유리 강성이면 걸음 수 | δt ∝ k_n^(−1/2) (원문 *"increasing k_n by a factor of 100 requires a reduction in the time step by a factor of 10"*) | δt ÷ ≈220 → 걸음 수 × ≈220 |
| 3D 바닥 응력 | 식 (17) · ρ = 6φ/(πd³) (원문 φ = πρd^D/2D) · φ 0.58 · θ 22° · h ≈ 41 (Fig. 15b [판독] 직선의 0 점) | σ_zz(0) ≈ **42 mg/d²** ↔ Fig. 15b [판독] 35.2 (z 3) · 직선 외삽 ≈38 (z 0) — 판독 기울기 0.93 이 식 (17) 의 1.03 보다 ≈10 % 작다 (같은 자릿수) |
| 평균 접촉력 | ⟨F⟩ ≈ π d² p / (Z φ) (3D virial · 가지 길이 ≈ d) · p ≈ 40 · Z = 2 Z_c ≈ 3.9 (Fig. 20 · 22°) | ⟨F⟩ ≈ **56 mg** (Z = Z_c 로 읽으면 ≈110 mg) |
| 겹침 (바닥 · 최대 하중) | Model L: δ/d = F/(k_n d) · Model H: δ/d = (F/(k_n d))^(2/3) | **δ/d ≈ 3 × 10⁻⁴ (L)** · **≈4 × 10⁻³ (H)** (Z 정규화에 따라 ×2 · ×1.6) — 원문은 겹침을 적지 않았다 |
| Hertz 의 실효 강성 | k_n √(δ/d) | ≈1.3 × 10⁴ mg/d = Model L 의 1/15 — 그래도 Fig. 12 의 φ 는 L3 ≈ H3 |
| 계산 비용 | 8000 × 10⁷ / (5 × 86,400 s) · 8 프로세서 15 × 10⁶ 걸음/일 | 1.9 × 10⁵ 입자·걸음/s · 병렬 효율 ≈0.94 |
| Bagnold 식 정합 | 식 (18) + γ̇ = A_Bag √σ_xz (Fig. 18 캡션 정의) 를 z 로 적분 | 식 (22) 가 나온다 → 식 (21) 은 σ_xz = **A_Bag⁻²** γ̇² 이어야 하는데 **A_Bag²** 로 인쇄 (§12-B) |

### 3-6. 이 논문에 **없는** 값 (찾으러 갔다가 없다고 확인)
- 겹침 크기 (평균 · 최대 · 분포) · 접촉 면적 · 힘 분포 — 0 회 ('overlap' 낱말 0 회).
- 입자의 재료 상수 (E · ν · 밀도) · 실제 단위의 압력 — 없음 (유리 예 한 줄뿐).
- Model H 의 ε 값 (속도 의존 곡선) · H3 표의 ε 칸 = 빈칸.
- 압축 · 탈압 · 판 · 하중 단계 — 없음 ('compression' 0 회 · 'unload' 은 *"loading or unloading normal contacts"* 한 번).
- 코드 이름 · 공개 여부 · 각 그림의 적분기 · 반복 표본 수 · 오차 막대 정의 (Fig. 16 *"Errors are of order symbol size"* 뿐).

---

## 4. ★ 방법 — 접촉 법칙 · 계산 · 입자 처리

### 4-1. 틀 (p.3)
*"We use the methods of molecular dynamics to perform 2D and 3D simulations of granular particles."* — 연성 구 DEM (겹침에 비례하는 반발) 의 명시 적분.  계산의 모든 입력 = 표 I + 기하 (H · L) + θ.  맞춘 값 = **없음** (매개변수는 '실제 입자를 닮게' 고른 값 · 실험 대조는 α 하나).

### 4-2. ★ 접촉력 계산 순서 (식 2–7 · p.4 · 크롭 `eq_02`–`eq_07`)
1. 겹침 δ_ij = d − r_ij (식 2) · r_ij = r_i − r_j · n_ij = r_ij/r_ij · v_ij = v_i − v_j.
2. 상대 법선 속도 v_n,ij = (v_ij·n_ij) n_ij (식 3) · 상대 접선 속도 v_t,ij = v_ij − v_n,ij − ½(ω_i + ω_j) × r_ij (식 4 — 접촉점의 회전 몫 포함).
3. **탄성 접선 변위** u_t,ij: 접촉 시작 때 0 · du_t/dt = v_t − (u_t·v_ij) r_ij / r_ij² (식 5) — 둘째 항은 *"arises from the rigid body rotation around the contact point and insures that u_t,ij always lies in the local tangent plane of contact"* (p.4) = 접촉의 '이력 (history)'.
4. 법선력 F_n = f(δ_ij/d)(k_n δ_ij n_ij − γ_n m_eff v_n,ij) (식 6) · 접선력 F_t = f(δ_ij/d)(−k_t u_t,ij − γ_t m_eff v_t,ij) (식 7) · m_eff = m_i m_j/(m_i + m_j) (= m/2) · F_ji = −F_ij.
5. **Coulomb 절단**: *"The static yield criterion, characterized by a local particle friction coefficient μ [34], is modeled by truncating the magnitude of u_t,ij as necessary to satisfy |F_t,ij| < |μF_n,ij|. Thus the contact surfaces are treated as ‘‘stuck’’ while F_t,ij < μF_n,ij, and as ‘‘slipping’’ while the yield criterion is satisfied."* (p.5 · 부등호 기호는 렌더 기준).
6. 운동 방정식 F_i^tot = m_i g + Σ_j (F_n,ij + F_t,ij) (식 8) · τ_i^tot = −½ Σ_j r_ij × F_t,ij (식 9).
- **Hooke 꼴 ↔ Hertz 꼴** (*"f(x) = 1 for the linear spring-dashpot model, denoted henceforth as Model L, or f(x) = √x for Hertzian contacts with viscoelastic damping between spheres, denoted as Model H"*): Model H 에서는 법선 탄성 · 법선 감쇠 · 접선 탄성 · 접선 감쇠 **네 항 모두**에 √(δ/d) 가 곱해진다 — 그래서 ε 가 충돌 속도에 따라 달라진다.  k_n 숫자는 두 모델이 같다 (2 × 10⁵) → 같은 하중에서 Model H 가 훨씬 무르다 (§3-5).

### 4-3. 반발 계수 · 시간 간격 (식 10–11 · p.4)
- Model L: ε_n,t = exp(−γ_n,t t_col/2) · t_col = π(2k_n/m − γ_n²/4)^(−1/2).
- *"The value of the spring constant should be large enough to avoid grain interpenetration, yet not so large as to require an unreasonably small simulation time step δt, since an accurate simulation typically requires δt ~ t_col/50."* (`txt_p4_kn_interpenetration_*`)

### 4-4. 매개변수 선택의 근거와 민감도 (p.4–5 · p.8)

| 매개변수 | 선택 · 근거 (원문) | 바꿔 본 범위 → 결과 |
|---|---|---|
| k_n | 유리 O(10¹⁰) 는 시간 간격 때문에 불가 → O(10⁵) · *"we believe captures the general behavior of intermediate-to-high-k systems"* | 2 × 10⁴ · 2 × 10⁵ · 2 × 10⁶ (L2 · 20° · H 50 · ε 를 γ_n 으로 고정) → *"minimal, provided k_n is sufficiently large"* (Fig. 11 · 10 배 무른 쪽에서 φ −≈0.01 · 표면 속도 +≈20 % [판독]) |
| k_t/k_n | 2/7 (L 의 법선 · 접선 진동 주기를 같게) · Hertz 이론 ≈2/3 | 2/3 → KE +≈10 % · 밀도 · 응력 그대로 |
| γ_t/γ_n | 0 (회전 속도 감쇠 없음) | γ_t = γ_n → KE −≈8 % · 정상 상태에 더 빨리 · 나머지 그대로 |
| μ | 0.50 (*"Typical values … range between 0.4 and 0.6 for many materials"*) | 0.15 · 0.25 · 0.50 · 1.0 → 몸통 밀도 거의 그대로 · 속도 크게 (Fig. 9) |
| ε | *"chosen to reflect the properties of a realistic granular particle"* | 2D 0.72–0.96 · 3D 0.58–0.98 → 3D 는 거의 그대로 · 2D 0.96 은 φ ≈0.765 로 낮고 빠름 (Fig. 10 [판독]) |
| Coulomb 절단 | u_t 를 자름 ("proportional loading") | 자르지 않음 (*"we do not believe this to be a physically reasonable choice"*) → 비슷 · KE 18 % 차 |
| 마찰 꼴 | 정마찰 (저장 u_t) | 동마찰만 (u_t = 0) → 정상 흐름 없음 (ref [34]) |

### 4-5. 적분 · 비용 · 병렬 (p.5) — §3-2 표.  한 줄 요지: 2001 년 기준 3D 8000 입자 10⁷ 걸음 ≈5 일 → MPI 8 프로세서로 하루 1.5 × 10⁷ 걸음.

### 4-6. 응력 · 관측량 정의
- **응력 (식 12)**: σ_αβ = (1/V) Σ_i [Σ_{j≠i} r_ij^α F_ij^β/2 + m_i(v_i^α − v̄^α)(v_i^β − v̄^β)] — 시간 평균 속도를 빼야 하는 이유 *"the kinetic portion of the stress tensor is entirely due to fluctuations in the velocity field"* (p.5).
- **충전율**: φ = πρd^D/2D (ρ = 수 밀도 · p.9) · '일정 밀도 구간' 의 값 (위 · 아래 경계 층 제외).
- **높이**: H ≡ Nd²/A (단순 입방 격자로 평면에 쌓았을 때의 높이 — 측정 높이 ≈ 0.93 H) · h = 식 (17) 의 적분 상수 (유효 높이).
- **응력 각 2φ** (Mohr 원의 COA 각 · p.10) · **χ** (식 20) · **A_Bag** (Fig. 18 캡션 γ̇/√σ_xz) · **Z_c** (평균 순간 배위수 · 정규화 §3-4).
- **정상 상태**: 전체 KE 가 거시적으로 일정 (p.2).

### 4-7. Cauchy · Mohr–Coulomb · Bagnold (식 13–22 · p.9–11)
- 정상 · 일정 밀도 → σ_zz = gρ cosθ (h − z) · σ_xz = gρ sinθ (h − z) (식 17·18) · σ_xx 는 구성 관계 없이는 정해지지 않는다 → Mohr 원의 응력 각으로 표현.
- 경계: 유체처럼 σ_xx = σ_zz 이면 sin 2φ = tan θ · 전체가 항복 직전 (IYE · 균일 Coulomb) 이면 φ = 0.
- Bagnold: σ_xz = A_Bag² γ̇² (식 21 인쇄) + 무미끄럼 → 식 (22) 의 h^(3/2) 속도 단면 (⚠ 지수 부호 §12-B).

### 4-8. ★ 입자 처리 — **진짜 형상 변형인가?**

| 질문 | 이 논문 | 우리 DEM (D0) | 우리 MPM |
|---|---|---|---|
| 입자 형상이 바뀌나 | **아니오** — 단단한 구 · 겹침 δ 로 힘을 셈 | 아니오 — 단단한 구 + 겹침 | 예 (J2 소성 흐름) |
| 접촉 '소성' | **없음** — 법선 이력 일부러 뺌 | 있음 — hooke/hysteresis 의 잔류 겹침 δ₀ (`luding2008` 카드) · 형상은 그대로 | (연속체) |
| 겹침 크기 | ~10⁻⁴–10⁻³ d [카드 산술] | ⟨δ⟩/d ≈ 0.11 (순수 SE) · 0.0175 (복합) (`comparison_vs_ours_DEM.md` L371–372 표기) | — |
| 강성 | k_n 무차원 · 유리의 ≈1/(5 × 10⁴) [카드 산술] · 이유 = 계산 시간 | E_eff 1.35 GPa · 18 배 연화 · 이유 = 기공률 보정 (frame [2]) | E 1.53 GPa · ν 0.49 · σ_y 0.30 GPa |
| 크기 분포 | 단분산 | 다분산 (AM ⌀4–9 µm · SE ⌀≈1 µm) | DEM 씨앗 |
| 하중 | 중력 (바닥 ≈40 mg/d²) | 300 MPa 판 | 판 |
| 차원 | 2D (원판) + 3D (구) | 3D | 3D (2D 판도 있음) |
| 탈압 | 없음 | 언로딩 키트 (진행) | 부분 |

### 4-9. ★ 우리 LIGGGHTS 덱과의 식 꼴 대조 (덱 표기 = 정본 카드 표기 · 이 카드는 리포 덱을 열지 않았다)

우리 두 덱 (정본 `ai2011` 카드 §7-2 · `shenouda2020` 카드 L233–234 표기): 압축 = `pair_style gran model hooke/hysteresis tangential history rolling_friction cdt` · 믹서 = `pair_style gran model hertz tangential history cohesion sjkr rolling_friction cdt`.

| 항 | 이 논문 (Model L / H) | 우리 압축 덱 | 우리 믹서 덱 | 같음 / 다름 |
|---|---|---|---|---|
| 법선 탄성 | k_n δ (L) · k_n √(δ/d) δ (H) · k_n = 무차원 상수 | Luding 이력 스프링 — 처녀 재하 k₁ · 제하 / 재하 k₂ (≤ k̂₂) · 점착 k_c · 소성 깊이 φ_f (`luding2008` 카드 L80–104 · 덱 m6 · m7 · m8 대응 = 그 카드 L5) | Hertz | 압축 = **다름** (원문이 뺀 이력) · 믹서 = Model H 와 같은 부류 (강성을 E · ν · R\* 로 세는 방식 = [미확인]) |
| 법선 잔류 겹침 | 없음 | δ₀ = (1 − k₁/k₂) δ_max | 없음 [카드 추론] | 압축 = 다름 |
| 법선 감쇠 | γ_n m_eff v_n × f — ε 와 식 (10)·(11) 로 묶임 | COR 로 설정 · k₂/k₁ 과의 정합 미감사 (`comparison_vs_ours_DEM.md` F-P5) | [미확인] | 대조 전 |
| 점착 | 없음 (*cohesionless*) | k_c | SJKR | 다름 |
| 접선 | 저장 탄성 변위 u_t (회전 보정) · k_t = (2/7) k_n · γ_t = 0 · Coulomb 절단 | `tangential history` | `tangential history` | **같은 부류** — 회전 보정 · 절단 방식 · k_t/k_n · 접선 감쇠의 구현 세부 대조 = [미확인] |
| 구름 저항 | 없음 | `rolling_friction cdt` (A 부류 · `ai2011` 카드) | cdt μ_r 0.075 | 다름 |
| 강성을 낮춘 이유 | 계산 시간 · 둔감 시험 (중력) | 보정 (기공률) | 속도 · 보정 (믹서 ref 배수 — 정본 comparison 문서) | 이유가 다르다 |
| 시간 간격 | δt = t_col/50 | [미확인 — 덱 값은 이 카드에서 확인 안 함] | 같음 | — |

- ★ **계보 [카드 정리]**: Cundall–Strack 1979 [28] → Walton–Braun 1986 [22] (이력 법선) → { 이 논문 = 법선 이력을 **뺀** 줄인 판 (원문 p.4) · Luding 2008 = 이력 + 점착의 공개 완전판 (`luding2008` 카드 머리) = 우리 압축 덱 }.  ⇒ **우리 압축 덱의 접촉 법칙 원전을 이 논문으로 인용하면 틀린다** — 이 논문은 접선 이력 · Coulomb 절단 · 스프링–감쇠 · Hertz 배율의 원문으로만 인용한다.

### 4-10. ★ 2D ↔ 3D (질문 g) — 한 논문 안의 실증

| 항목 | 2D (L2 · 원판) | 3D (L3 · H3 · 구) | 원문 위치 |
|---|---|---|---|
| 정지 상태 | **다결정 삼각 격자로 결정화** (φ ≃ 0.9) | 무질서 정지 (φ 0.595) | p.6 · p.8 |
| 흐름 이력 | **크다** — *"Crystallization of the 2D monodisperse pile upon the arrest of flow was primarily responsible for the large hysteresis"* · 재시작에 훨씬 큰 각 필요 | 작다 — 얇은 더미 · 낮은 각에서만 · H 를 키우면 줄어듦 | p.3 · p.6 |
| A_Bag 의 안식각 거동 | **유한 도약** | 0 으로 연속 | p.12 · Fig. 18 |
| 흐름 정지가 시작되는 곳 | 바닥 근처 (표면은 안식각에서 IYE 에서 더 멀어짐) | **표면** (표면 층이 IYE 에 접근) | p.10–11 · Fig. 14 |
| 최대 충전율 | 0.815 (면적 분율) | 0.590 (부피 분율) — **숫자끼리 비교 불가** | p.8 |
| 안식각 | ≈17.8° | ≈19.4° | p.8 |
| 정상 범위 (H ≈ 40–50) | ≈17.5–23° (ε 0.92) | ≈20–27° | Fig. 2 [판독] |
| 배위수 Z_c | 0.3–0.9 | 0.5–3.2 | Fig. 20 [판독] |
| ε 민감도 | 있음 (0.96 → φ 낮고 빠름) | *"little effect … particularly in 3D"* | p.8 · Fig. 10 |
| σ_yy | (없음) | xx · zz 보다 15–20 % 작음 | p.11 |
| 같은 것 | 일정 밀도 · Bagnold 단면 · α = 1.52 ± 0.05 · 접촉 지배 응력 · 얇은 더미 (H ≲ 20) 의 비-Bagnold | | p.12 · p.13 |

⇒ **[카드 추론]**: 꼴 (일정 밀도 · 척도 지수) 은 2D 에서 3D 로 옮겨지지만 **정지 · 재시작 · 이력 · 파괴 위치**는 단분산 2D 결정화 때문에 옮겨지지 않는다 — 우리 단계 3 (2D 벤치마크) 에서 단분산 원판을 쓰면 같은 함정에 들어간다.

### 4-11. 탈압 — 다루지 않음
하중을 빼는 계산이 없다.  접촉 법칙에 재하 / 제하 이력이 없으므로 (p.4) 압력을 빼도 잔류 겹침 · 되돌아옴 비대칭이 원리적으로 생기지 않는다.  원문의 '이력' 은 흐름이 멈추는 각 (θ_r^stop) 과 다시 시작하는 각 (θ_r^flow) 의 차 (p.6) 이다.

### 4-12. 기법 미니 용어집
- **chute flow** = 거친 바닥의 경사면을 따라 중력으로 흐르는 입자 층 · **안식각 θ_r** = 그 아래에서 흐름이 유지되지 않는 각 · **θ_max** = 정상 흐름이 가능한 최대 각 (그 위는 바닥 층이 묽어져 전체가 가속).
- **spring-dashpot (Model L)** = 겹침에 비례하는 스프링 + 상대 속도에 비례하는 감쇠 · **Model H** = 같은 식에 √(δ/d) 를 곱한 Hertz 꼴.
- **u_t (탄성 접선 변위)** = 접촉이 붙어 있는 동안 쌓인 접선 미끄럼 · 그것이 접선 스프링을 늘려 정마찰을 만든다 = 접촉 '이력 (history)'.
- **proportional loading** = 접선력이 μF_n 을 넘으면 u_t 를 잘라 경계 위에 두는 근사 (실제 접촉의 Mindlin–Deresiewicz 이력의 단순화 [36]).
- **t_col** = 감쇠 스프링 한 번의 충돌 시간 · **ε (반발 계수)** = 충돌 뒤 / 앞 상대 속도 비.
- **Bagnold 척도** = 전단 응력이 변형률 속도의 제곱에 비례 (σ ∝ γ̇²) · 일정 밀도 더미에서 v ∝ h^(3/2).
- **Mohr 원 · 응력 각 2φ · IYE** = 응력 텐서를 회전시켜 본 그림 · 2φ = 0 이면 모든 곳이 Coulomb 항복 직전 (incipient yield everywhere).
- **χ (법선 응력 이상)** = (σ_zz − σ_xx)/σ_zz · 유체이면 0.
- **Z_c** = 평균 순간 배위수 (정규화 §3-4).

---

## 5. 결과 — 절별 상세

### 5-1. 상 그림 · 이력 (§I · II · Fig. 2 · p.2–3 · p.6)
흐름 없음 / 정상 / 불안정 세 영역 (2D · 3D 모두) · 두 경계각 θ_r · θ_max 는 μ · ε · H 에 따라 움직인다 (2D ε 0.92 → 0.82 에 θ_max ≈23° → 26° · μ 를 낮추면 정상 범위가 좁아짐).  경계 근처는 흐름 시작 절차에 민감하고 3D 는 얇은 더미에서 작은 이력 · 2D 는 결정화로 큰 이력.  θ > θ_max 에서는 *"the development of a shear thinning layer at the bottom of the pile results in lift-off and unstable acceleration of the entire pile"* (p.2).

### 5-2. 운동학 (§III A · Fig. 3–8 · p.6–8)
- Fig. 3 (2D 출발): 삼각 격자에서 바닥이 먼저 무너지고 팽창 앞면이 위로 올라가 더미가 *"fluffs up"*.
- Fig. 4: 일정 φ 구간 + 위쪽 팽창 층 · θ 가 커지면 φ 감소 · 팽창 층 증가 · 속도 단면은 위로 볼록 (concave) · KE 증가.
- Fig. 5: 수직 평균 제곱 변위가 시간에 선형 = 잘 섞이는 확산 · 바닥 근처가 더 빠름.
- Fig. 6: 속도 요동 ('granular temperature') 이 바닥 근처 (판에서 몇 d 위) 에서 최대 → 위로 감소 · *"a constant density is maintained through the increased particle velocity fluctuations"* (p.7) — 아래로 갈수록 무게가 커져도 밀도가 일정한 이유의 부분 설명.
- Fig. 7: 몸통 밀도 · 표면 근처 밀도와 변형률 단면이 전체 높이에 무관 → 국소 유변학 (단 식은 찾지 못했다).  Fig. 8: H 10 은 거의 직선 속도 단면 (비-Bagnold) · 그 경계 H ≳ 20.

### 5-3. 상호작용 매개변수 (§III B · Fig. 9–11 · p.8) — §4-4 표.  핵심 문장: *"while the density of the bulk material does not depend sensitively on these interaction parameters, the velocity profiles do."*

### 5-4. 기울기 의존 (§III C · Fig. 12 · p.8–9)
*"effects due to material properties and system size can be neglected in the steady-state regime"* · φ 가 θ 에 거의 선형 · φ_max (안식각) 2D 0.815 · 3D 0.590 · 정지 3D 0.595 · 2D 결정 ≃ 0.9 · 이상 미끄럼 층 π/4 · π/(3√3) 와 가깝다.

### 5-5. 응력 (§IV · Fig. 13–16 · p.9–11)
2φ 는 표면 값에서 몸통 값으로 지수 감쇠 (식 19 · 층 5–8d) · 몸통의 σ_xx ≈ σ_zz (χ 작음 · 부호 바뀜) · 3D σ_yy 15–20 % 작음 (*"consolidation and compaction normal to the shear plane is poorer"*) · 동차 · 다항 · 회전 불변 구성 관계로 χ 를 설명하지 못했다.  *"the normal stress anomalies … are quite small compared to what one would have attributed to a plastic material at incipient yield"* (p.11).

### 5-6. 유변학 (§IV D · Fig. 17–20 · p.11–12)
몸통에서 σ_xz ∝ γ̇² (위 5–8 층 아래 · 바닥에서 떨어진 곳) · A_Bag 은 3D 에서 θ_r 로 연속해 0 · 2D 도약 · α = 1.52 ± 0.05 · Bagnold 의 이진 충돌 기전이 아니라 지속 접촉이 응력을 나름 (운동 몫 ≈1 %) — *"the success of the Bagnold scaling is based on the dimensional structure of the problem"* · Z_c ≫ 1 (3D) · θ_r 로 갈수록 증가.

### 5-7. 결론 (§V · p.13)
일정 밀도 · Bagnold 척도 (≥ 20 입자 높이) · 법선 응력 이상은 *"a mystery"* · 접촉이 응력 전달을 지배 · 안식각에서 몸통은 Coulomb 항복 구조에 가지 않고 3D 표면만 접근 → 3D 표면 파괴의 특별한 역할.  후속 = 매끈한 바닥 [3] · 3D 평면 Couette.

---

## 6. Figure set ★

| 그림 | 내용 | 우리 활용 |
|---|---|---|
| Fig. 1 | 3D 스냅숏 (N 24,000 · 바닥 20 × 20 d · θ 24° · ε 0.88 · μ 0.50) | 계산 기하 (주기 x · y + 거친 바닥) |
| Fig. 2 (a · b) | (θ, H) 상 그림 — 2D L2 · 3D L3 · '+' = 3D 이력 흐름 | 안식각 · 정상 범위 · 얇은 더미 효과 [판독 §3-4] |
| Fig. 3 | 2D 삼각 격자가 24° 로 기울인 뒤 무너지는 시간 순서 (t 100 · 400 · 600 · 6000) | 2D 단분산 결정 출발의 함정 그림 |
| Fig. 4 (a · b) | φ(z) · v_x(z) — 2D H100 18–23° · 3D H40 20–26° (L3 기호 · H3 선) | 일정 밀도 구간 · Model L ↔ H |
| Fig. 5 | 수직 평균 제곱 변위 (L3 · 21–23°) | 혼합 확산 계수 D_z [카드 산술] (흐름 밖: 믹서) |
| Fig. 6 | 운동 응력 단면 (정규화) | 속도 요동이 바닥 근처 최대 |
| Fig. 7 (a · b) | 높이 H 에 따른 φ · v_x (2D 25–200 · 3D 40–100) | 크기 무관 국소 유변학 · ⚠ (b) 캡션 ↔ 범례 H 값 어긋남 |
| Fig. 8 | 얇은 더미 (H 10) — 비-Bagnold | H ≳ 20 경계 |
| Fig. 9 (a · b) | μ 0.15–1.0 의 φ · v_x · 변형률 속도 | ★ 밀도 둔감 · 속도 민감 [판독] |
| Fig. 10 (a · b) | ε 0.72–0.96 (2D) · 0.58–0.98 (3D) | 3D 는 ε 무관 · 2D 0.96 만 다름 |
| Fig. 11 | ★ k_n 2 × 10⁴ · 2 × 10⁵ · 2 × 10⁶ (L2 · 20° · H 50) | 강성 낮추기의 근거 그림 — 중력 영역 한정 |
| Fig. 12 | ★ 몸통 φ(θ) — L2 · L3 · H3 · 안식각 외삽 | φ_max · Model L ≈ H [판독 표] |
| Fig. 13 (a · b) | Mohr 원 정의 · 2φ(z) 지수 맞춤 (H3 H40) | 표면 층 5–8d |
| Fig. 14 (a · b) | 2φ^surf · 2φ^bulk (θ) · 2D vs 3D | 3D 표면이 IYE 에 접근 (2D ↔ 3D 차이) |
| Fig. 15 (a · b) | 응력 성분 단면 (2D H100 · 3D H40 · 22°) | 정수압형 직선 · σ_yy 결손 |
| Fig. 16 | χ(θ) — L2 · L2 ε 0.82 · L3 · H3 | 작고 부호가 바뀌는 이상 [판독] |
| Fig. 17 (a · b) | ∂v_x/∂z vs σ_xz + Bagnold 맞춤 | 몸통 σ ∝ γ̇² |
| Fig. 18 | A_Bag(θ) | 3D 연속 · 2D 도약 [판독] |
| Fig. 19 | ⟨v²⟩^1/2 vs H (log–log) | α = 1.52 · ⚠ 캡션은 (a)(b) 인데 한 패널 |
| Fig. 20 | Z_c(θ) 2D · 3D | 배위수 정규화 함정 |
| Table I | 표준 세 모델 매개변수 | D0 덱 감사 · U5 기대값 |
| 식 크롭 22 장 | `eq_01` (Bagnold) · `eq_02`–`eq_07` (★ 접촉 꼴: 겹침 · 상대 속도 · 접선 변위 이력 · 법선력 · 접선력) · `eq_08`–`eq_09` (운동 · 회전) · `eq_10`–`eq_11` (★ 반발 계수 · 충돌 시간) · `eq_12` (응력) · `eq_13`–`eq_18` (Cauchy) · `eq_19`–`eq_22` (응력 각 · χ · Bagnold) | 보고서 DEM 접촉 법칙 절에 그대로 |
| 근거 문단 20 장 | `txt_p4_contact_model_*` (Walton–Braun 축소판 · 이력 무시) · `txt_p4_fx_*` (Model L/H) · `txt_p4_units_kn_glass_*` (강성 낮춤 이유) · `txt_p4_kn_interpenetration_*` (t_col/50) · `txt_p5_coulomb_*` (절단 · proportional loading) · `txt_p5_kt_kn_*` · `txt_p5_gamma_t_mu_*` · `txt_p5_integration_*` (δt · 비용) · `txt_p5_geometry_*` · `txt_p5_p6_initial_state_*` · `txt_p2_protocol_*` · `txt_p3_hysteresis_*` · `txt_p3_p4_method_*` · `txt_p8_interaction_*` (k_n 둔감) · `txt_p8_p9_packing_*` (φ_max) · `txt_p11_bulk_*` (σ_yy) · `txt_p12_bagnold_*` (α) · `txt_p12_contacts_*` (접촉 지배 · Z_c · 기하 지배) · `txt_p13_conclusions_*` · `txt_p13_p14_ref34_*` (동마찰 → 정상 흐름 없음) | 원문 인용용 |

## 7. Post-processing ★
- **무엇을**: 일정 밀도 구간의 φ · 속도 · 응력 단면 (z 층별 시간 평균) · 응력 (식 12 · 시간 평균 속도를 뺀 운동 항) · Mohr 원 응력 각과 지수 맞춤 (식 19) · χ · A_Bag (몸통 맞춤) · ⟨v²⟩^1/2 vs H (log–log 기울기) · Z_c · 평균 제곱 변위.
- **안 한 것**: 겹침 · 힘 분포 · 접촉 면적 · 힘 사슬 · 접촉 수 정의 (Z ↔ N_c/N) 명시 · 오차 막대 정의 · 표본 수 · 적분기별 결과 구분 · 탈압.
- **이 카드의 후처리**: 원 래스터 (300 dpi) 10 그림 판독 94 행 (눈금 직선 보정 · 표지 중심 = 구멍 메움 + 9 × 9 열림 연산의 무게 중심 · 겹친 표지는 채운 표지만 따로 · 곡선은 열 안의 어두운 구간 가운데) · 표 I 재현 산술 · 겹침 · 접촉력 자릿수 어림 · 비용 산술 · 식 (21)–(22) 정합 점검.

---

## 8. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 지시서 · CLAUDE.md 의 고정 기준값과 정본 카드 표기를 병기)

### 8-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 방법 | 연성 구 DEM (자체 MD) | LIGGGHTS DEM (D0) + MPM | 같은 부류 (DEM) |
| 접촉 법칙 | 스프링–감쇠 / Hertz + 접선 이력 + Coulomb · 법선 이력 없음 | 압축 hooke/hysteresis (이력 · 점착) · 믹서 hertz + SJKR · 둘 다 tangential history + cdt | §4-9 — 접선 = 같은 부류 · 압축 법선 = 다름 |
| 하중 · 상태 | 중력 정상 흐름 · 무차원 | 300 MPa 압축 → 판 고정 이완 (→ 언로딩 진행) | 다름 — 흐름 ↔ 준정적 압밀 |
| 강성 | k_n = 유리의 ≈1/(5 × 10⁴) · 계산 시간 | E_eff 1.35 GPa = 실재 ≈24 GPa 의 1/18 · 기공률 보정 | 이유가 다르다 (속도형 ↔ 보정형 — `comparison_vs_ours_DEM.md` Lommen 블록의 (a) ↔ (b)) |
| 겹침 | ~10⁻⁴–10⁻³ d [카드 산술] | ⟨δ⟩/d ≈ 0.11 (순수 SE) · 0.0175 (복합) | **25–400 배** [카드 산술] |
| 입자 | 단분산 · 점착 없음 | 다분산 (AM 강 · SE 연) · 점착 (k_c) | 다름 |
| 충전율 | 3D 정지 0.595 (단분산 · μ 0.5 · 중력) | 순수 SE 300 MPa 기공 10–13 % (랩 표준) · DEM ε_union ≈10 % | 다른 상태 — 비교 금지 (§8-3) |
| 차원 | 2D + 3D | 3D (MPM 2D 판 있음) | 2D ↔ 3D 증거만 |
| 수송 | 없음 | 접촉망 σ 삼중항 | frame [5]: 이 논문 = 패킹 · 레올로지 쪽 반쪽 |

### 8-2. 같은 점
- 접선 이력 (`tangential history`) · Coulomb 절단 · m_eff 감쇠라는 **접선 꼴의 계보**가 같다 (구현 세부 [미확인]).
- 강성을 실재보다 낮춘다 — 둘 다 "DEM 강성은 물성이 아니라 계산 · 보정 손잡이" 라는 같은 인식 (원문 *"we believe captures the general behavior of intermediate-to-high-k systems"* ↔ 우리 frame [2]).
- 응력을 접촉 virial 로 센다 (식 12 ↔ 우리 Love–Weber 입자 응력 · LHS ④b) — 식 꼴 대조의 기준.

### 8-3. 다른 점 — 그리고 왜 (방법 인공물 vs 실제 차이)
1. **법선 이력**: 원문은 일부러 뺐다 · 우리 압축은 그것이 핵심 (잔류 겹침 = ε_sphere 규약의 물리 · `luding2008` 카드).  → 원문의 매개변수 둔감성 결과 (밀도 둔감) 를 우리 이력 법칙의 k₁ · k₂ · k_c 로 옮기지 않는다 (법칙이 다르다).
2. **하중 영역**: 원문 둔감성은 겹침 ~10⁻⁴ d 의 중력 흐름에서 · 우리는 ⟨δ⟩/d ≈ 0.11 — 원문이 말한 *"provided k_n is sufficiently large"* 의 '충분히' 를 우리 압밀에서는 만족하지 못한다 (실재 E 로도 δ/d ≈ 7.6 % — `comparison_vs_ours_DEM.md` F-P4 의 봉투 계산).  → **"Silbert 2001 이 강성을 낮춰도 밀도가 안 바뀐다고 했다" 로 우리 18 배를 방어하지 않는다** (방법 인공물 아님 · 영역 차이).
3. **충전율 숫자**: 0.590 / 0.595 는 단분산 · 마찰 0.5 · 무압력 (중력) 의 흐름 · 정지 상태 — 우리 300 MPa 압밀 침대와 다른 상태 · 다른 재료 · 다른 크기 분포 (실제 차이 · 비교 금지).
4. **2D 원판 결정화**: 원문의 2D 이력은 단분산 결정화의 산물 — 다분산 · 3D 계에는 없을 수 있다 (방법 인공물 쪽).

### 8-4. ★ 겹침 · 강성 영역을 나란히 (유비 · 산술 — 논문 주장 아님)
| 출처 | 하중 | 겹침 δ/d | 강성을 낮춘 배수 | 둔감성 확인 |
|---|---|---|---|---|
| 이 논문 Model L (3D 바닥) | ≈40 mg/d² (중력) | ≈3 × 10⁻⁴ [카드 산술] | ≈5 × 10⁴ (속도) | k_n 100 배 범위에서 밀도 ≲ 0.01 (2D) [판독] |
| 이 논문 Model H (3D 바닥) | 같음 | ≈4 × 10⁻³ [카드 산술] | 같음 (k_n 숫자 같음) | φ(H3) ≈ φ(L3) (20–24°) |
| 우리 DEM 순수 SE | 300 MPa | ≈0.11 (`comparison_vs_ours_DEM.md` L371) | 18 (보정) | 1.35 ↔ 1.5 GPa (11 %) 만 — 시드 산포 안 (같은 문서 F 절 'F-P1 · F-C2′ 의 근거 문장이 잘못됐다' 항목) |
| 우리 DEM 복합 | 300 MPa | ≈0.0175 (같은 문서 L372) | 18 | 같음 |
⇒ 우리 압축은 원문의 둔감성 확인 영역보다 겹침이 **25–400 배** 크다 — 원문의 결론 (기하가 지배 · 힘 법칙 세부는 덜 중요) 이 거기서도 성립하는지는 원문으로 알 수 없다 [카드 추론].

### 8-5. frame [5] — 어느 반쪽을 가졌나
- **가진 것**: DEM 쪽 — 접촉 법칙 (원문 꼴) · 패킹 (충전율) · 배위수 · 레올로지 (흐름).
- **없는 것**: 수송 · 압밀 · 탈압 · 형상 변화 · 소성 · 다분산 · 점착.  ⇒ D0 접촉 꼴의 기준 문서이자 '연화의 근거는 영역 한정' 의 반례 근거.  MPM 쪽에 주는 것 = 없음 (흐름 밖: 믹서 흐름 레올로지 · 혼합 확산).

---

## 9. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = 지시서 고정값: DEM 18 배 연화 · E_eff 1.35 GPa · Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준) | ★ (1) **명목 높이 ↔ 측정 높이를 따로 적는 꼴**: H ≡ Nd²/A (단순 입방 평면 높이) 와 측정 높이 ≈37 (H 40) 을 나란히 (p.5) — 우리 두께 연산자 (판 간격 · 질량 보존 두께) 등록에 '명목 / 측정' 칸 (2) **경계 층 제외 규칙**: φ 를 '일정 밀도 구간' 에서만 · 표면 유변 층 5–8d 는 팽창 층보다 두껍다 (p.11 (v)) — 관측 구간 경계를 결과 전에 (3) 정상 상태 = 전체 KE 평탄 — 우리 이완 · 언로딩 판정의 에너지 기준 후보 | 기공 연산자 자체 · 압밀 상태 |
| **단계 1** (3D 메모리 · 장 수) | 없음 (MPI 공간 분할 성능 1000 입자/프로세서 = 흐름 밖: DEM 병렬 규모 감각) | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | ★ **2D 단분산의 함정**: 멈출 때 결정화 → 큰 이력 · 재시작 각 상승 · A_Bag 도약 (p.3 · p.6 · p.12) — 2D 벤치마크 침대는 다분산으로 만들거나 결정화 여부를 결과 전에 점검 항목으로 | 압축 · 접촉 표현 비교 자체 없음 |
| **단계 4** (3D 순수 SE 붓고 누르기) | 출발 충전의 기준 숫자 (다른 재료): 단분산 · μ 0.5 마찰 구의 정지 충전 **0.595** (중력 · 흐름 정지) — 우리 '느슨하게 부은' 출발 상태의 충전율을 결과 전에 기록할 때 '단분산 마찰 구 문헌 값' 으로만 · 출발 무질서화 절차 (30° 로 기울여 흔들고 낮춤 · p.5) | 압축 · σ_y 맞춤 표적 아님 (랩 표준이 표적) |
| **단계 5** (3D 복합 압밀) | 없음 | — |
| **단계 6** (탈압 · 되돌아옴) | 없음 — 법선 이력 없음 (원문이 뺐다) · 압력을 빼는 계산 없음 | 되돌아옴 표적 · 이력 법칙 매개변수 |
| **단계 7** (형상 · 피복 · 수송) | 배위수 정규화 함정 (Z ↔ N_c/N — §3-4) → 우리 CN 열 정의에 '접촉 하나를 두 번 세나' 를 명시 · 응력 virial 식 (12) 의 ½ · 운동 항 = 우리 Love–Weber 열 정의 대조 (흐름 밖: LHS 인계 ④b) | 수송 · 피복 없음 |
| **후보 D0** (지금 DEM) | ★★ 접선 이력 · Coulomb 절단 · m_eff 감쇠 · Hertz 배율의 **원문 식** (식 2–7) · 매개변수 관례 (k_t/k_n 2/7 · γ_t 0 · μ 0.5) · δt = t_col/50 · ε–γ (식 10–11) · 민감도 표 (§4-4) → 덱 감사 항목: ① 시간 간격을 **가장 단단한 가지** (이력 법칙이면 k̂₂) 의 t_col 로 점검 ② k_t/k_n · 접선 감쇠 설정과 그 효과 (원문은 KE 만 ±10 %) ③ 우리 법선 이력은 이 논문 밖 (Luding) 이라는 인용 규칙 | 우리 압밀 영역의 둔감성 (영역 밖) · E · ν 매개변수화 · 다분산 R_eff |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 꼴만 — 붙음 / 미끄럼 판정을 **저장된 접선 변위를 잘라** 구현하는 Coulomb 규칙 (식 5 + 절단) = MPM 벽 마찰 규칙을 세울 때 견줄 이산 접촉판 | MPM 격자 접촉 자체 없음 |
| **후보 A · A′** (MPM 강체 AM / 입자별 속도장) | 없음 | — |
| **후보 B** (입자별 FE) | 없음 | — |
| **후보 C** (MDR 류) | 없음 — 작은 겹침 · 점접촉만 | — |
| **후보 C′** (항복 캡 · Thornton–Ning) | 반대 사례 — 이 논문은 C′ 의 정의 요소 (법선 이력 · 소성 분기) 를 **뺀** 판 · 그래도 흐름 밀도가 맞는다는 것 = 중력 흐름에서는 법선 이력이 필요 없다는 증거일 뿐 [카드 추론] | 압밀에서의 필요성 판단 근거 아님 |
| **후보 M0** (균질화 · Heckel · 캡) | 흐름 밖: Bagnold 구성식 σ_xz = A_Bag⁻² γ̇² (식 21–22 · 부호 §12-B) · Mohr–Coulomb 해석 · *"We have been unable to define a simple, local, dimensionally consistent and rotationally invariant constitutive relation"* (p.3) — 조밀 흐름 연속체 닫음이 불완전하다는 원문 진술 | 압밀 Heckel · 캡 없음 |
| **U0–U6** | ★ **U5** (같은 강성 입자끼리 충돌): 두 입자 정면 충돌 → ε · t_col 를 식 (10)·(11) 과 견줌 — 기대값 = 표 I 매개변수에서 t_col 4.97 × 10⁻³ t_o · ε 0.883 (γ_n 50) / 0.920 (33.5) [카드 산술] (Model H 는 속도 의존 · 값 없음) · **U2** (경사면 마찰): 다입자판 기대값 = 3D 단분산 μ 0.5 의 안식각 ≈19.4° · 정상 범위 ≈20–27° (H 40) [인쇄 · 판독] — 단일 물체 미끄럼 시험의 대체는 아님 | U1 · U3 · U4 · U6 없음 |
| **R1–R7** | **R2** (미끄럼 · 분리) — 붙음 / 미끄럼 (Coulomb 절단) · 분리 (δ ≤ 0 이면 힘 0) 의 이산 구현 · 동마찰만이면 정상 흐름이 안 나온다 (ref 34) = 정마찰 (저장 변위) 이 필요하다는 증거 | R1 · R3 · R4 · R5 · R6 · R7 없음 |
| **결과 전 대조 항목** | (i) U5 두 입자 충돌의 ε · t_col (식 10–11 · 우리 덱 매개변수로 다시 계산 — 이 논문 숫자 아님) (ii) 우리 덱으로 단분산 μ 0.5 구 chute 를 돌렸을 때 φ_3D^max ≈0.590 · θ_r ≈19.4° 근처인가 (코드 검증용 · 재료 무관) | 압밀 · 기공 절대값 비교 금지 |

- **랩 기준과 나란히 (판정 없이 · "랩 표준과 다른 문헌 값")**

| 출처 | 재료 · 상태 | 압력 | 기공 (= 1 − φ) |
|---|---|---|---|
| **랩 표준** | LPSCl 순수 SE · 누른 침대 | 300 MPa | **10–13 %** (진밀도 1.64 g/cm³ 기준 · 고정) |
| 이 논문 (3D 정지) | 단분산 마찰 구 (μ 0.5) · 흐름이 멈춘 상태 | 중력 (무차원) | 40.5 % [카드 산술 1 − 0.595] |
| 이 논문 (3D 흐름 · 안식각) | 같음 · 정상 흐름 | 중력 | 41.0 % [카드 산술 1 − 0.590] |
| 이 논문 (2D 정지) | 단분산 원판 · 결정화 | 중력 | ≈10 % (면적 · φ ≃ 0.9) — 2D 면적 분율 |

- **재료 · 차원 · 조건 차이**: 무재료 모델 구 ↔ LPSCl · NCM / 단분산 ↔ 다분산 / 중력 흐름 ↔ 300 MPa 압밀 / 무점착 ↔ 점착 / 2D + 3D ↔ 3D.

## 10. 적용 인사이트 (내 연구에 어떻게)
1. **우리 압축 덱의 접촉 법칙 원전을 이 논문으로 인용하지 않는다** — 이 논문은 법선 이력을 뺀 판이다 (p.4).  이 논문은 '접선 이력 · Coulomb 절단 · 스프링–감쇠 · Hertz 배율' 의 원문으로, 이력 법선은 Luding 2008 (← Walton–Braun 1986) 로 인용한다 (D0 · 보고서 방법 절).
2. **"강성을 낮춰도 된다" 는 근거는 하중 영역과 함께 적는다** — 원문의 둔감성은 겹침 ~10⁻⁴ d 의 중력 흐름에서 k_n 이 *"sufficiently large"* 일 때다 · 우리 압밀은 그 25–400 배 겹친다 (§8-4) → 18 배 연화의 방어는 이 논문이 아니라 우리 보정 · 교차 검증 (frame [2] · [4]) 으로.
3. **U5 단위 시험 기대값을 닫힌 꼴로 만든다** — 식 (10)·(11) 은 두 입자 충돌의 ε · t_col 를 바로 준다 · 우리 덱 (E · ν · COR → 강성 · 감쇠) 에서 같은 계산이 맞는지 (COR ↔ k₂/k₁ 정합 미감사 F-P5 와 같은 할 일).
4. **시간 간격 = 가장 단단한 가지의 t_col / 50** — 이력 법칙이면 k̂₂ 로 세야 한다 (`luding2008` 카드 L89–90 의 k̂₂ = 시간 간격 안정 상한) · 원문 규칙 (p.4) 을 덱 감사 한 줄로.
5. **2D 단분산 벤치마크 금지 · 배위수 정의 명시** — 단계 3 의 2D 침대는 결정화를 피하게 다분산으로 · CN 열에는 Z 와 N_c/N 중 무엇인지.

## 11. 인용 가능 문장 (deck/paper 용 — 표지 그대로)
- "The widely used DEM contact model with a stored elastic tangential displacement truncated at the Coulomb limit, a linear spring–dashpot (or Hertzian, f(δ/d) = √(δ/d)) normal force and k_t/k_n = 2/7 is documented in Silbert et al., Phys. Rev. E 64, 051302 (2001), Eqs. (2)–(7) and Table I; the authors describe it as a reduced version of Walton & Braun (1986) that ignores loading/unloading hysteresis of normal contacts."
- "Silbert et al. (2001) chose k_n = O(10⁵) mg/d instead of O(10¹⁰) for glass to keep the time step tractable (δt ~ t_col/50), and found the bulk density insensitive to k_n between 2×10⁴ and 2×10⁶ in gravity-driven chute flow — a low-stress regime (overlap ~10⁻⁴ d by our estimate), not high-pressure compaction."
- 국문: *"Silbert 2001 의 접촉 꼴 (식 6·7) 은 법선 이력이 없는 스프링–감쇠 / Hertz 판이다 — 우리 hooke/hysteresis 의 법선 이력 원전이 아니다."*
- 국문: *"강성을 낮춰도 밀도가 둔감하다는 Silbert 2001 의 결과는 중력 흐름 (작은 겹침) 에서의 것이다 — 300 MPa 압밀로 옮기지 않는다."*

## 12. 주의 / 한계 (over-claim 방지 · 원문 비판)

### 12-A. 우리에게 옮길 때의 한계
1. 중력 흐름 ↔ 준정적 고압 압밀 — 하중 · 겹침 영역이 2–3 자릿수 다르다 (§8-4).
2. 단분산 · 무점착 · 무재료 · 무차원 — 절대값 전이 0.
3. 법선 이력 없음 — 우리 압축 덱과 다른 법칙.
4. 2D 결과는 결정화로 이력이 부풀었다 — 2D 숫자를 3D 로 옮기지 않는다.
5. 겹침 · 접촉력 어림 (§3-5) 은 이 카드의 자릿수 산술 (Z 정규화 · 가지 길이 ≈ d 가정) — 원문 값 아님.

### 12-B. ★ 이 논문 자체의 약점 · 불일치 (비판적으로)
1. **식 (21) ↔ Fig. 18 · 식 (22)**: 식 (21) 은 σ_xz = **A_Bag²** γ̇² 로 인쇄 · Fig. 18 캡션은 A_Bag = γ̇/√σ_xz · 식 (18) 과 γ̇ = A_Bag √σ_xz 를 적분하면 식 (22) 가 그대로 나온다 → 식 (21) 은 A_Bag**⁻²** 이어야 맞는다 [카드 산술].
2. **Z_c 정규화**: 2D 삼각 격자 = 3 (N_c/N) ↔ 3D 정지 충전 '4–6' (보통 Z) — 같은 정규화로 읽히지 않는다 (p.12) · 그래서 Fig. 20 의 3D 값 (≤ 3.2) 을 어느 쪽과 견줘야 하는지 [미확인].
3. **Fig. 7 (b)**: 캡션 *"H=100, 60, 50, and 40"* ↔ 범례 H = 100 · 80 · 60 · 40 (곡선 끝 높이 ≈95 · 77 · 58 · 39 d 도 범례 쪽) [판독].
4. **Fig. 19**: 캡션은 (a) 2D · (b) H3 두 패널 · 인쇄는 한 패널 (범례 3D μ 0.50 · 2D μ 0.50 · 2D μ 0.25).
5. **Fig. 6**: 캡션의 선 모양 표지 (21° · 23° 둘 다 파선 · 25° 일점쇄선) 가 그림의 실선 · 일점쇄선 · 점선과 1:1 로 맞지 않는다.
6. **3D 불안정 각**: 본문 *"in 3D the unstable flow regime is observed above 26°"* (p.7 · H 40) ↔ Fig. 2b H 40 은 27° 정상 · 27.5° 불안정 [판독] — 1° 안팎 어긋남.
7. **2D 안식각**: φ 외삽 θ_r,2D ≈ 17.8° (p.8) ↔ Fig. 2a H 50 은 17.5° 에서 정상 흐름 [판독] (0.3° · 정의 차이일 수 있음).
8. **Z_c 문장**: *"In a system dominated by binary collisions, one would expect Z_c ≪ 1; this is clearly not the case"* — 2D 값은 0.3–0.9 로 1 보다 작다 (3D 만 1 을 넘는다).
9. **참고문헌 목록**: [20] (Kharkhar 외) 와 [25] (Zheng & Hill) 가 같은 *"Powder Technol. 86, 219 (1996)"* · [31] (Vu-Quoc & Zhang) 과 [32] (Vemuri 외) 가 같은 *"Mech. Mater. 31, 235 (1999)"* — 둘 중 하나씩은 틀렸다 (어느 쪽인지 원문으로 가를 수 없다) · [36] *"L. Appl. Mech."* · [2] *"Europhy. Lett."* ([19] 는 *"Europhys. Lett."*) · [39] *"Tilldesley"* — 인쇄 그대로.
10. **겹침 · 접촉력 미보고**: 작은 겹침 가정의 크기를 원문이 숫자로 주지 않는다 — '단단한 구' 근사의 정량 근거가 원문 안에 없다.
11. **적분기 둘**: Gear 와 속도-Verlet 중 어느 결과인지 그림별로 구분하지 않는다.

### 12-C. [미확인] 목록 (PDF 에 없음)
- 겹침 · 접촉력 · 접촉 면적의 크기 · 분포 · Model H 의 ε(v) 값.
- 코드 이름 · 공개 여부 · 그림별 적분기 · 반복 표본 수 · 오차 막대 정의 · 시간 평균 길이.
- 유리 k_n^glass = O(10¹⁰) 의 유도 (어느 하중 · 어느 식).
- Z_c 의 정확한 정의 (접촉을 한 번 / 두 번 세는지).
- 참고문헌 [20]/[25] · [31]/[32] 의 바른 서지.
- 2D 원판의 질량 · 회전 관성 (*"(projected) spheres"* — 구의 관성을 쓰는지).

## 13. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 22 | O. R. Walton and R. L. Braun, J. Rheol. 30, 949 (1986). | 법선 이력 (우리 hooke/hysteresis 계보) · 이 논문이 줄인 원판 | 없음 — ⛔ 후보 표 제외 (N-72 첫째 · 1저자 내려받기 불가) · 공개 대체판 = `luding2008` |
| 28 | P. A. Cundall and O. D. L. Strack, Geotechnique 29, 47 (1979). | DEM · 접선 스프링의 원전 (D0 · 질문 e · k) | 없음 (papers/ ls · grep) |
| 36 | R. D. Mindlin and H. Deresiewicz, L. Appl. Mech. 20, 327 (1953). | 실제 접촉의 접선 이력 — proportional loading 이 단순화한 대상 (질문 e · k) | 없음 |
| 38 | J. Schafer, S. Dippel, and D. E. Wolf, J. Phys. I 6, 5 (1996). | k_t/k_n = 2/7 의 근거 · 접촉 꼴 비교 (D0 · U5) | 없음 |
| 31 | L. Vu-Quoc and X. Zhang, Mech. Mater. 31, 235 (1999). | 탄소성 접촉 (C′ · 질문 e) · ⚠ [32] 와 권 · 쪽이 같음 | 없음 |
| 48 | H. A. Makse, D. L. Johnson, and L. M. Schwartz, Phys. Rev. Lett. 84, 4160 (2000). | 3D 정지 충전 배위수 4–6 의 근거 (질문 d · k) | 없음 |
| 23 | O. R. Walton, Mech. Mater. 16, 239 (1993). | 3D chute DEM · 마찰 방향 기억 (D0) | 없음 |
| 35 | T. C. Halsey and D. Ertaş, Phys. Rev. Lett. 83, 5007 (1999). | 'proportional loading' 근사의 출처 | 없음 |
| 40 | S. J. Plimpton, J. Comput. Phys. 117, 1 (1995). | 병렬 공간 분할 방법 (흐름 밖) | 없음 |
| 29 | O. Pouliquen, Phys. Fluids 11, 542 (1999). | α · 상 그림의 실험 대조 | 없음 |
- 같은 저자군의 짝 논문 [2] (Ertaş 외, *Europhy. Lett.* (unpublished)) · [3] (Silbert 외, unpublished) — 서지 미완 (원문 그대로).

---

## [미확인] 목록
- §12-C 와 같음 (겹침 · 접촉력 크기 · ε(v) · 코드 · 적분기 · 오차 정의 · 유리 k_n 유도 · Z_c 정의 · 참고문헌 둘 · 2D 관성).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-16)
- 서지: 1저자 메모 · 후보 표 N-71 서지 = 원문 첫 쪽 (저자 6 · 소속 · 접수 · 출판 날짜 · DOI · PACS) 과 같다.  PDF 메타데이터에는 제목 · DOI 가 없다 (creator 'XPP' 뿐) — 서지는 첫 쪽 인쇄로 확인.
- 기호 · 숫자: 텍스트 층이 Symbol 글꼴을 잃어 (θ · μ · ε · φ · ρ · χ · ψ · = · × · ≈ · ≲ · ≤ · ± · 괄호) 모든 식 · 표 · 기호 문장을 쪽 렌더 (250–400 dpi) 로 다시 읽었다 — 식 (1)–(22) · 표 I · 캡션 20 · δt = 10⁻⁴ · 1–2 × 10⁷ δt · 2–5 × 10⁸ δt · H ≳ 20 · θ ≳ 23° · 0.815(5) · 0.590(5) · ≈17.8° · ≈19.4° · 0.595 · ≃0.9 · π/4 ≈ 0.79 · π/(3√3) ≈ 0.60 · 15–20 % · 1.52 ± 0.05 · 4–6 · ≈1 % · 18 % · 10 % · 8 % · O(10¹⁰) · O(10⁵) · 2/7 · 2/3 · 5 days · 15 million · 1000 · 8000 · 24,000 · 20 × 20.
- 낱말 검색 (텍스트 층 14 쪽): 'LAMMPS' · 'Hooke' · 'overlap' · 'compression' · 'deform' 0 회 · 'plas' 1 회 (p.11 *"plastic material at incipient yield"*) · 'history' 4 회 (구성 이력 · 표본 이력 · 이력 효과 [30]) · 'unload' 1 회 (p.4).
- 판독 보정: 각 그림의 큰 눈금 (자동 검출 · 라벨 대조) 직선 보정 · Fig. 12 · 18 은 겹친 표지를 채운 표지 (구멍 메움 없이 9 × 9 열림) 로 따로 · Fig. 19 기울기 1.55 (원문 1.52 ± 0.05) 로 보정 점검.
- 정본 중복 확인: papers/ 파일 목록 (silbert · ertas · grest · bagnold · chute · plimpton · halsey) · '051302' · 'Bagnold scaling' · 'Silbert' grep — 카드 없음 (benhadjali2026 · haervig2017 · shi2019 = 이 논문 인용 · brodu2015 = Silbert 2002 PRE 65 031304 인용 · clemmer2024 = Santos · Silbert 다른 논문).

## 🔗 관련 카드
- 이 논문을 인용한 카드: `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` (ref 34 · 고른 의도) · `haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem` (ref 30 · Δt 규칙) · `shi2019_high_am_loading_particle_size_assb` (본문 [22]).
- 접촉 법칙 계보 · 우리 덱: `luding2008_cohesive_frictional_contact_models` (hooke/hysteresis 정의서 · Walton–Braun 대체판) · `ai2011_rolling_resistance_contact_models_dem` (우리 덱의 cdt 표기) · `shenouda2020_dem_metal_powder_am_liggghts_tutorial` (덱 줄) · `thorntonning1998_adhesive_elastoplastic_contact` (C′) · `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` (LAMMPS gran/hertz/history 를 쓰는 전지 DEM).
- 강성 낮추기 · 보정: `lommen2014_dem_speedup_contact_stiffness_reduction_bulk_behavior` · `morenoatanasio2007_contact_stiffness_surface_energy_fluidization_cohesive_dem` · `paulick2015_elastic_particle_properties_dem_review` · `coetzee2017_dem_calibration_review` · `haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem`.
- 조밀 · 다접촉: `brodu2015_multiple_contact_dem_dense_granular` (같은 그룹 Silbert 2002 인용) · `clemmer2024_bpm_elastic_grain_compaction_beyond_jamming`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
