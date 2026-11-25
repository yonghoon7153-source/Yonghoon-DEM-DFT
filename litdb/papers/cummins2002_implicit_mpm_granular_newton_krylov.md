<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 후보 표 N-39) 에서 꼭 뽑으라고 한 항목.
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표) ·
     MPM 이웃 = guilkey2003_implicit_mpm_newton_quasistatic_fem_comparison.md (같은 자리 · 암시 MPM 의 다른 갈래 · 그 카드가 이 논문을 [13] 으로 가리킴) ·
     bardenhagen2000_mpm_granular_multibody_frictional_contact.md (이 논문 ref [38] = 접촉 알고리즘의 원전) · bardenhagen2001_mpm_improved_contact_granular_stress_waves.md (ref [50] · 같은 광탄성 원판의 명시 MPM).
     원문 = J. Comput. Phys. 180, 506–548 (2002) · PDF 43 쪽 · 보충 자료 (SI) 없음 (본문 · 참고문헌 전수).
     쪽 표기 = 학술지 쪽 p.506–548 (PDF 쪽 = 학술지 쪽 − 505).  크롭 이름의 pN 과 figures.json 의 page 는 PDF 쪽이다 (예: txt_p25_… = p.530).
     값 표지: [인쇄] = 본문 · 식 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 83 행 — 그림 6 · 10 · 14 · 15 는 벡터 경로라
     PDF 그리기 명령에서 틀 + 큰 눈금으로 축을 맞추고 '+' 표지 = 암시 · 꺾은선 = 명시로 읽음 · 묶음이 섞인 곳은 600 dpi 래스터의 맨 위 잉크) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] · [카드 추론] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드에 적힌 값 (slug 병기) ·
     [우리 · CLAUDE.md] = 우리 쪽 값 · [미확인] = 원문 43 쪽 전수에 없음.
     원문 43 쪽은 글자 층 추출 전수 + 식 · 표 · 그림 크롭 렌더 (식 400 dpi · 나머지 300 dpi) 로 읽었다 (글자 층은 Δ · θ · 위아래 첨자가 빠지거나 흩어져 식은 전부 렌더로 대조).  DEM 계산 · 준정적 압밀 · 기공 · 탈압 · 3D 계산은 없다. -->

# 입상체 MPM 의 암시적 판 — 알갱이마다 격자 속도장 (다물체 접촉) + θ = ½ 시간 적분 + 행렬 없는 inexact Newton–Krylov (GMRES · 유한차분 야코비 곱 · 가중 Jacobi 전처리) · 1 차 부피 가중 접촉 (침투 금지 · Coulomb 마찰 · 결합 / 떨어짐) · J2 반경 귀환 탄소성 알갱이 · 에너지법으로 암시 = L2 안정 (걸음 크기 무관) ↔ 명시 도약 = 아님 · 유한 격자 (ringing) 불안정 제거 · 2D 예 셋: 탄성 알갱이 벽 충돌 (명시 총에너지 2 µs 에 ×14.5 [판독] ↔ 암시 '≈7 %') · 광탄성 원판 5 개 응력파 (암시 에너지 1 % 안) · HMX 370 알갱이 전단 330 % (평균 주응력차 명시 46.02 ↔ 암시 25.55 MPa) · 걸음 ≤ 10 Δt_exp (조건수 벽) · 걸음당 변형 < 1 % (= µ·1 % ≈ 0.25 σ_y) · 준정적 압밀 · 기공 · 하중 몫 · 탈압 · 3D · CPU 시간 없음 — Cummins · Brackbill (J. Comput. Phys. 2002)

> slug `cummins2002_implicit_mpm_granular_newton_krylov` · DOI `10.1006/jcph.2002.7101` · type `MPM (방법 논문 — 알갱이마다 격자 속도장을 둔 입상체 MPM (Bardenhagen 외 [38] 의 다물체 접촉) 의 암시적 θ 판 · 행렬 없는 inexact Newton–Krylov (GMRES · 유한차분 야코비 곱 · 가중 Jacobi 한 층 / 여러 층 V-cycle 전처리) · 1 차 부피 가중 접촉 · J2 반경 귀환 선형 경화 · Neumann · 유한 격자 불안정 · 에너지법 안정 분석 · 2D 동역학 예 셋 (탄성 알갱이 벽 충돌 · 광탄성 원판 5 개 응력파 · HMX 결정 370 알갱이 전단) — 준정적 압밀 · 기공 · 하중 몫 · 탈압 · 3D · DEM 계산 없음)` · PDF `58d437e1-39._An_implicit_particle-in-cell_method_for_granular_materials.pdf` · digested `2026-11-12` · status ✅

> **저자**: **S. J. Cummins** · **J. U. Brackbill** — Theoretical Division, Los Alamos National Laboratory, Los Alamos, New Mexico 87545 (E-mail scummins@lanl.gov · jub@lanl.gov · 교신 표지 없음) · *J. Comput. Phys.* **180**, 506–548 (2002) (43 쪽 · 호 미인쇄) · 접수 2001-08-15 (수정 · 게재일 미인쇄) · © 2002 Elsevier Science (USA) · 연구비 U.S. DOE Contract W-7405-ENG-36 · 감사 Scott Bardenhagen · Deborah Sulsky · Dana Knoll · Bryan Lally · Doug Kothe (p.546) · 키워드 *granular flow; finite-difference methods; implicit methods, quadratic conserving; nonlinear stability; Newton–Krylov*.  SI 없음.
> **이웃 카드 (링크만)**: [`bardenhagen2005_mpm_foam_densification_simulation`](bardenhagen2005_mpm_foam_densification_simulation.md) (이 논문을 *"expensive … area of algorithm research"* 로 가리킨 카드 · L253 · L299 · L519 · L53) · [`guilkey2003_implicit_mpm_newton_quasistatic_fem_comparison`](guilkey2003_implicit_mpm_newton_quasistatic_fem_comparison.md) (같은 자리 · 일관 접선 + 강성 행렬 갈래 · 그 카드 L127 · L274 · L350 이 이 논문을 인용 · 이 논문의 ref [55] 는 그 방법의 2001 학회 판) · [`bardenhagen2000_mpm_granular_multibody_frictional_contact`](bardenhagen2000_mpm_granular_multibody_frictional_contact.md) (ref [38] · 이 논문 접촉 식 (7)–(12) · (52)–(54) 의 원전 · 같은 HMX 근사) · [`bardenhagen2001_mpm_improved_contact_granular_stress_waves`](bardenhagen2001_mpm_improved_contact_granular_stress_waves.md) (ref [50] 'private communication' 의 출판본 · 같은 광탄성 원판 명시 MPM) · [`nezamabadi2022_mpm_cd_plastic_particle_compaction`](nezamabadi2022_mpm_cd_plastic_particle_compaction.md) · [`nguyen2017_mpm_bpm_deformable_particle_compaction`](nguyen2017_mpm_bpm_deformable_particle_compaction.md) (암시 MPM + contact dynamics 로 변형 입자 침대를 실제로 압밀한 뒤 선례) · [`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`](homel2017_mpm_field_gradient_partitioning_fracture_self_contact.md) (속도장을 알갱이 수만큼 늘리지 않는 다른 갈래) · [`hu2018_mls_mpm_cpic_two_way_rigid_coupling`](hu2018_mls_mpm_cpic_two_way_rigid_coupling.md) (우리 명시 MLS-MPM 의 원전) · [`steffen2008_mpm_implementation_choices_gimp_bspline_boundary`](steffen2008_mpm_implementation_choices_gimp_bspline_boundary.md) · [`steffen2010_mpm_space_time_error_balance_moving_mesh`](steffen2010_mpm_space_time_error_balance_moving_mesh.md) · [`bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing`](bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing.md) (명시 MPM 의 오차 · 셀 넘김) · [`devaucorbeil2020_mpm_after_25_years_review`](devaucorbeil2020_mpm_after_25_years_review.md).
> **판독 원자료**: `litdb/figures/cummins2002_implicit_mpm_granular_newton_krylov/digitized.csv` (83 행 — 그림 6 세 판 (총 · 탄성 에너지 · x 운동량) · 그림 10 · 그림 14 두 판 · 그림 15 (범례의 인쇄 평균 둘 + 봉우리 · 꼬리)) · 그림 크롭 **168 장** (그림 15 = 도구 13 + 손 2 (그림 3 · 11 도식) · 표 7 = 손 (로마 숫자 번호라 도구 밖) · 식 126 (식 (1)–(126) 번호마다 한 장 · 400 dpi · 다시 자름 19) · 근거 문단 20 (다시 자름 13)) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 알갱이를 탄소성 연속체 (물질점 묶음) 로 풀고 알갱이마다 격자 속도장을 두는 입상체 MPM (Bardenhagen 외 [38]) 을, 명시 도약 (leapfrog) 대신 **θ 시간 적분 (θ = ½)** 으로 바꾸고 그 비선형 · 비해석 (마찰 · 소성) 연립식을 **행렬 없는 inexact Newton–Krylov** 로 푼다 — 에너지법으로 암시 판은 **걸음 크기와 무관하게 L2 안정** 이고 명시 도약은 그렇지 않음을 보이고 (p.516 · p.522), 2D 동역학 예 셋에서 명시 도약의 **에너지 증가 · 거짓 잔류 응력 · 거짓 운동량 · 알갱이 가장자리 떨어져 나감 (spallation)** 이 암시에서는 사라진다 (탄성 알갱이 벽 충돌: 명시 총에너지 2 µs 에 **×14.5** [판독] ↔ 암시 *"maximum variation of ≈7%"* · 원판 5 개: 암시 *"conserved to within 1%"* · 370 알갱이 전단: 평균 주응력차 **46.02 ↔ 25.55 MPa** [그림 15 범례 인쇄]).  대가 = 걸음이 **≤ 10 Δt_exp** (그 위로는 선형 연립식 조건수가 나빠지고 전처리가 수렴 반경을 못 넓힌다 · p.531) 와 **걸음당 변형 < 1 %** (소성 정확도 · p.530) 에 묶이고, CPU 시간은 **한 번도 적지 않았다**.  예는 모두 **2D 동역학** — 준정적 압밀 · 기공 · 하중 몫 · 탈압은 없다.

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 무엇을 했나 | 알갱이 = 등방 선형 탄소성 연속체 (e = e_e + e_pl · 반경 귀환 · 일치 조건 · 변형 경화 · 식 1–6) · 알갱이마다 격자 속도장 (다물체) · 운동량식에 접촉 비력 f_gg′ (식 4) · MPM 의 첫 (Lagrange) 단계를 **θ 판** 으로 (식 38–41 · ½ ≤ θ ≤ 1) · 비선형 잔차 (식 105) 를 **행렬 없는 inexact NK** 로 (식 96–104 · 허용치 10⁻⁶ · ε = 10⁻³ · γ = 10⁻³) · 전처리 = 가중 Jacobi (w 0.67 · 두 번) 한 층 / V-cycle 여러 층 | [인쇄] p.508–529 · 식 (1)–(118) |
| ② ★ 접촉 · 다물체 (f) | 침투 금지 n̂_g · (v_g − v_g′) ≤ 0 (식 7) 은 알갱이 수의 **제곱** 비용 → 질량 가중 평균 속도 v (*"Fabre-averaged"* · 식 9) 와 비교하는 식 (8) 로 **알갱이 수에 선형** · *"We will assume no more than two grains are in contact at any given time"* · 접촉 판정 = 노드에서 알갱이 속도 ≠ 질량중심 속도 · 법선 = −∇ρ_g (식 48) · 공통 법선 가정 n̂_g · n̂_g′ = −1 (식 10) · Coulomb 마찰 (식 52–54 · 접선 속도가 뒤집히지 않게 µ′ = min(µ, …)) · 결합 = 상대 운동 전부 막음 · 떨어짐 = 법선 견인력 ≥ σ_bond (식 12) · **부피 가중** (식 55): 알갱이가 **한 셀** 떨어지면 무게 0 · 닿으면 각 ½ · 파고들면 > 1 로 밀어냄 → *"first-order accurate"* 이지만 *"smaller effective grain size"* · 벽 = 경계에서 v 를 지정한 같은 접촉 제약 | [인쇄] p.509 · p.514–515 · 식 (7)–(12) · (48)–(55) |
| ③ ★ 소성 · 큰 변형 (l) | 어려움 (원문): *"the frictional component of the contact model and the plastic constitutive model are both governed by nonlinear functions …; in addition the plastic constitutive model is also nonanalytic [8]. The Jacobian matrix for this system will therefore be difficult to invert."* (p.523) · Coulomb 의 불연속 = *"unconventional mathematics"* (p.507) · 우회 = 야코비를 만들지 않는 **행렬 없는 NK** (야코비 × 벡터 = 잔차 차분 · 식 101) + 소성 정확도를 위한 걸음 제한 (< 1 % · *"to ensure the stress is close to the yield surface immediately before the onset of plasticity"*) · 값 = HMX 결정 σ_y **300 MPa** · 경화 H **10 MPa** (표 VI · 원전 [38]) · 맞춘 값 **0** (원판 λ · µ 는 실험 [49] 의 P · S 파속 두 값에서 계산) · 비용 = 표 I 반복 수뿐 (CPU · 걸음 수 · 기계 [미확인]) | [인쇄] p.507 · p.523 · p.530 · 표 VI |
| ④ 암시의 이득 | Neumann: 암시는 Courant 한계를 없앤다 · θ = ½ 이면 해가 실수 · Nyquist 안 (식 58–60) · θ > ½ 는 감쇠 (식 61) / **유한 격자 불안정** (ringing) 은 명시 · 암시 **둘 다** 선형 분석으로는 Δt = 0 에서도 불안정 (U₀/√(λ/ρ₀) < 0.4 · 선형 b-spline · 식 68) / **에너지법**: 암시 θ 판의 운동 · 변형 에너지는 E⁰ 로 묶임 → *"stable in the L2 norm independent of the time step"* (식 88–90) · 명시 도약은 에너지를 O(Δt³) 로 지켜도 L2 안정을 보일 수 없음 (단진동 예 식 86–87) · 에너지 감소 몫을 식 (85) 로 분해 (θ 항 · 마찰 F ≤ 0 · 소성 P ≤ 0 · 질량 몰아주기 L ≤ 0) | [인쇄] p.515–522 |
| ⑤ 걸음 크기 · 비용 | 암시: 걸음당 최대 변형 **< 1 %** (식 119–120 · 탄성 재료에도 적용 · *"For materials with different yield properties the maximum strain limit will need to alter"*) · 명시: Courant α = **0.25** (보수적 · 에너지 보존이 낫다) 와 1 % 중 작은 쪽 (식 123) · *"The linear systems … become poorly conditioned for time steps Δt > 10 × Δt_exp … does not increase the radius of convergence. The reason for this is currently unclear."* · Newton 이 최대 반복에 못 맞추면 **걸음을 반으로** · 쓴 최대 걸음 = 2.5 Δt_exp (탄성 알갱이) · **10 Δt_exp** (원판 · 전단) = P파 Courant 수 2.5 [카드 산술] · 표 I (64 × 64 · t = 0.5): 전처리 없음 Newton 4249 · 선형 42490 → 한 층 WJ 1724 · 6727 → 여러 층 1691–1717 · 4442–4596 · **CPU 시간 · 메모리 · 걸음 수 미인쇄** | [인쇄] p.529–531 · 표 I–VII |
| ⑥ 해상도 · 오차 추정 (f) | 해상도 규칙 **없음** — 쓴 값: 알갱이 지름당 **12.3 칸** (탄성 알갱이 · R 50 µm · Δx 8.118 µm) · **32 칸** (원판 R 5 mm · Δx 0.3125 mm) · **8.0 칸** (전단 R 32.6 µm [카드 해석 · 그림 11 단위]) · 셀당 물질점 최대 **4** [카드 산술 · 인쇄] · 격자 수렴 시험 없음 · 오차 추정 = 에너지 · 운동량 장부 (그림 6 · 10 · 14) · 직사각 블록 충돌 파속의 해석해 대조 *"a 3% error was incurred for both implicit and explicit"* · 측정 P파 ≈2.5 × 10³ m/s (설정 2.133 × 10³ — 차이 설명 없음) · 응력 상한 2/√3 σ_y = 346 MPa 아래 | [인쇄] p.532–545 · 표 II · IV · VI |
| ⑦ 하중 몫 · 재밍 (d) | **없음** — 한 재료 (HMX 근사) · 결합재는 *"viscoplastic material [36, 39]"* 한 줄 · 앞 연구 [39] 인용: *"static loading results in stress bridging in polydisperse samples … with a stiff viscoelastic binder, stress fingering is suppressed"* | [인쇄] p.507 · p.509 |
| ⑧ 2D / 3D (g) | 계산은 전부 **2D** (17 × 17 · 36 × 176 · 156 × 150 격자 · 잔차 F = [F_x, F_y] · 대각 추출 '두 성분 × 아홉 셀 = 18 번') · 식은 d 차원 (*"bilinear (trilinear) mapping"*) · 평면변형률 / 평면응력 [미확인] · 2D → 3D 전이에 대한 말 **없음** | [인쇄] p.510 · p.522 · p.528 |
| ⑨ 탈압 · 되돌아옴 (b) | 압밀 탈압 **없음**.  가까운 것 = 탄성 알갱이 **벽 충돌 뒤 반발** — 명시는 *"An inelastic deformation is occurring after each wall contact and residual stresses remain"* + 거짓 운동량 증가 · 암시는 탄성 에너지 쌓임이 *"approximately two orders of magnitude less"* · 접촉은 *"allows them to move apart freely"* (자유 분리) | [인쇄] p.509 · p.534 |
| ⑩ DEM 한계 (k) | **직접 한계 문장 없음** — 대조 문장 둘: *"Contact dynamics' simulations assume that the individual grains are perfectly rigid and interact through exact Coulombian friction, which introduces a nonlocal character to momentum transfers that requires that all kinematic constraints be simultaneously accounted for in the solution of the dynamics [40]."* · DEM 힘 법칙 = *"a hard core potential [29], or a contact law derived from Hertz–Mindlin theory [16]"* ↔ *"methods which seek to model the material properties of the grains realistically [38, 44, 45]. These models resolve grain scale lengths, allow grains to deform, and solve continuum equations in which contact and friction have been regularized."* | [인쇄] p.506–507 |
| ⑪ 저자가 적은 한계 | 조건수 벽의 원인 *"currently unclear"* (p.531) · 여러 층 전처리 *"somewhat disappointing"* — 접촉 표현이 격자 간격과 자기 닮음이라 굵은 층에서 접촉 거리가 커진다 (p.530) · FLIP 내부력 판은 조건수가 낫지만 (탄성 알갱이 선형 반복 절반) 넓은 스텐실이 알갱이 가장자리 전단 오차 → 쓰지 않음 (p.525) · 걸음 제한이 실제 재료의 항복을 넘지 않게 최대 걸음을 묶음 (p.545) · 한 노드 두 알갱이 가정 (p.509) | [인쇄] |

⛔ **한정어 (떼지 말 것)**: ① 재료 = **HMX 근사** (탄성 알갱이 *"Bulk modulus λ"* 11.36 GPa · µ 7.48 GPa · ρ 1900 kg/m³ · *"infinite yield stress"* / 전단 = HMX 결정 J2 σ_y 300 MPa · H 10 MPa · 표 VI 의 λ 는 **1.136 × 10⁸** 으로 인쇄) · 원판 = 광탄성 재료 [49] 의 파속에 맞춘 λ 4.786 · µ 2.893 GPa — LPSCl · NCM 이 아니다 ② 예 셋 모두 **동역학** (벽 충돌 100 m/s · 속도 계단 10 m/s 0.12 µs · 오른쪽 벽 100 m/s 전단 330 %) — **준정적 압밀 · 기공 · 밀도 · 압력 곡선 없음** (준정적은 동기 문장뿐 · p.507) ③ **2D 계산뿐** ④ **한 재료** (단단한 + 무른 섞임 · 하중 몫 없음) ⑤ **탈압 없음** ⑥ **비용 숫자 없음** (CPU · 메모리 · 걸음 수 · 기계) ⑦ 원문 안 어긋남 (표 VI λ · ν · 그림 11 단위 · 측정 P파 +17 % · '≈7 %' 의 기준 — §3-11).
⇒ **절대값 전이: 0 건.**  옮길 수 있는 것 = **방법** (알갱이별 잔차 목록을 이어 붙인 행렬 없는 NK · 부피 가중 접촉 · 질량 가중 잔차 · 에너지 감소 분해 식 (85)) · **규칙** (걸음당 변형 한계 = µ·Δε ≈ 0.25 σ_y 로 재료마다 다시 정함 · ≤ 10 Δt_exp 조건수 벽 · Newton 실패 = 걸음 반) · **함정** (접촉 거리 ∝ Δx · 한 노드 두 알갱이 · 공통 법선 · 명시 도약의 에너지 증가 · 다층 전처리 무익 · 가장자리 작은 노드 질량) · 저자 문장.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-39 의 '왜' 칸)

의도 원문 (`S8_candidates.md` N-39): *"f · l · d — 입자 재료의 암시적 PIC (같은 자리 · 카드 §3-9) → 가루 침대의 준정적 압축을 MPM 계열로 푼 선례 후보"* (가리킨 카드 = `bardenhagen2005_mpm_foam_densification_simulation` §3-9 · 정본 L253 · 출처 = b41 findings n 절)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "입자 재료의 암시적 PIC" | **채움** | 제목 · 초록 (p.506) · §3.3 θ 판 (식 35–43) · §5–7 행렬 없는 inexact NK · 전처리 — 알갱이 = 탄소성 연속체 · 알갱이마다 격자 속도장 · *"In our application, a multivalued velocity field is required since relative motion between the grains must be simulated"* (p.523) |
| (f) MPM 의 접촉 · 다물체 · 강체 결합 · 해상도 규칙 · 수치 오차 추정 | **일부** | **접촉 · 다물체 = 채움** (식 7–12 · 48–55 · 부피 가중 1 차 · 질량중심 속도 비교 · 밀도 기울기 법선 · Coulomb µ′ · 결합/떨어짐 · 한 노드 두 알갱이 가정 · 벽 = v 지정 접촉) · **강체 결합 = 없음** (강체 물체 없음 · 전단의 양옆 알갱이는 움직이는 벽에 *"attaching"*) · **해상도 규칙 = 없음** (쓴 값만: 지름당 12.3 · 32 · 8.0 칸 · 셀당 최대 4 [카드 산술]) · **오차 추정 = 일부** (에너지 · 운동량 장부 · 블록 파속 해석해 3 % · P파 측정 · 346 MPa 상한 · 명시 ↔ 암시 · 격자 수렴 · 오차 노름 없음) |
| (l) 소성이 왜 어려운가 · 우회 · 비용 | **일부** | 어려움 = 마찰 · 소성의 비선형 + 소성의 **비해석성** → 야코비 역행렬 어려움 (p.523) · Coulomb 불연속 (p.507) · 항복 직전 응력 정확도 (p.530) · 우회 = 행렬 없는 NK + 걸음당 변형 < 1 % · 검증 = 에너지 장부 (소성 소산 P ≤ 0 · 식 83) · 전단 응력 분포 (그림 15) · **비용 숫자 없음** (표 I 반복 수뿐) · 소성 알갱이 계산은 전단 예 하나 (2D · 동역학) |
| (d) 단단한 + 무른 섞임 · 하중 몫 · 재밍 | **없음** | 한 재료 · 결합재 *"viscoplastic"* 한 줄 (p.509) · 앞 연구 [39] (Bardenhagen & Brackbill 1998 · 정적 재하 → 다분산 침대의 응력 다리 · 단단한 점탄성 결합재 → 응력 손가락 억제 · p.507) 인용만 — 정본 카드 없음 (wishlist L278) |
| "(같은 자리 · 카드 §3-9)" | **채움** | `bardenhagen2005_…` L253 이 인용한 바로 그 논문 — 아래 2 차 인용 표 |
| "→ 가루 침대의 준정적 압축을 MPM 계열로 푼 선례 후보" | **없음** | 준정적은 **동기 문장뿐**: *"for quasi-static granular problems implicit methods are potentially more efficient [12]. A robust and efficient MPM has many applications in the study of the response of granular materials to low strain rates, such as experiments on nonlinear stiffening [13] or shear cell experiments [19]"* (p.507) · 예 셋 모두 동역학 (§8.3 벽 충돌 100 m/s · §8.4 *"Compressed Grains"* = *"the dynamic loading of an assembly of grains"* — 원판 5 개 기둥 위 판에 속도 계단 10 m/s · 0.12 µs · 응력파 · §8.5 전단 100 m/s) · 압력 · 기공 · 밀도 없음.  **정본에서 실제로 가루 침대를 MPM 계열로 준정적 압밀한 선례** = `nezamabadi2022_…` · `nguyen2017_…` (암시 MPM + contact dynamics · 2D 변형 원판 300 개) — 이 논문이 아니다.  정적 압축 MPM 의 더 이른 선례 = 이 논문의 [39] (카드 없음) |
| (꼭 뽑을 것) 측정 조건 — 누른 채 / 뺀 뒤 · 압력 · 온도 · 조성 · 진밀도 | **해당 없음** | 계산 논문 · HMX 근사 · 광탄성 재료 · 압력 · 기공 · 진밀도 개념 없음 · 탈압 없음 |
| 후보 표 서지 (*"Cummins, S.J., Brackbill, J.U., 2002. An implicit particle-in-cell method for granular materials. J. Comp. Phys. 180, 506–548."*) | **같음** | 원문 첫 쪽: *Journal of Computational Physics* **180**, 506–548 (2002) · doi:10.1006/jcph.2002.7101 · 제목 *"An Implicit Particle-in-Cell Method for Granular Materials"* — 대소문자 · 학술지 약어만 다름 · 호 · 출판일 미인쇄 |

**가리킨 카드 · 같은 논문을 쓴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `bardenhagen2005_…` L253 (§3-9) | *"Currently these algorithms are expensive, and remain an area of algorithm research for GIMP methods Cummins and Brackbill (2002), Guilkey and Weiss (2003)."* (Bardenhagen 2005 원문 문장 그대로) | 이 논문 = **선형 b-spline 표준 MPM** (p.510 *"MPM typically uses linear b-splines"*) — GIMP 아님 · 비용을 숫자로 적지 않았다 · *"provides strong incentives for the development of more effective preconditioners in the future"* (p.546) · 조건수 벽 (p.531) = '연구 중' 과 같은 방향 | **맞음 (일부)** — 카드는 원 논문 문장을 그대로 옮겼다 · 'for GIMP methods' 는 Bardenhagen 2005 의 범위 표현 · 'expensive' 의 숫자 근거는 이 원문에 없다 (카드 문제 아님) |
| `bardenhagen2005_…` L299 · L519 · L53 | *"준정적에는 암시적 풀이가 낫지만 비싸고 연구 중"* · *"암시적 풀이는 비싸고 연구 중"* · *"To simulate quasi-static deformations an implicit numerical solution strategy is generally preferred"* | 이 원문 p.507 *"for quasi-static granular problems implicit methods are potentially more efficient [12]"* (Benson 2000 근거) · 효율은 **주장 ('potentially')** 이고 이 논문 안에서 재지 않았다 | **맞음** (방향) — 단 이 논문도 준정적 계산은 하지 않았다 |
| `guilkey2003_…` L127 | Guilkey 원문 *"that of Cummins and Brackbill is limited to 1% strain per time step"* · *"명시 dt (CFL 0.25) 의 10 배를 넘으면 해 없음"* · 차이 원인 = *"our approach employs a consistent tangent"* | 1 % = **스스로 둔 정확도 규칙** (소성 직전 응력이 항복면 근처 · 탄성에도 적용 · *"will need to alter"* · p.530–531) — 풀이기의 한계가 아니다 · 10 배 = *"become poorly conditioned … does not increase the radius of convergence"* + GMRES 상한 + 걸음 반 (p.531) · 이 논문은 바로 그 **10 Δt_exp 로 원판 · 전단을 끝까지 풀었다** (표 IV · VI) · α 0.25 ✓ | **일부** — 카드는 Guilkey 원문을 옮겼다 (카드 문제 아님) · Guilkey 의 요약이 이 원문보다 강하다 ('해 없음' ↔ '조건수 나쁨 · 반으로') |
| `guilkey2003_…` L274 (§7-3) | *"행렬 없는 Newton–Krylov (Cummins–Brackbill) 은 이 논문 보고로 'time steps greater than 10 times the explicit time step' 에서 해가 없었다"* | 위와 같음 | **일부** (같은 이유) |
| `guilkey2003_…` L350 (참고 [13]) | *"Cummins SJ, Brackbill JU. An implicit particle-in-cell method for granular materials. Journal of Computational Physics 2002; 180:506–548."* | ✓ | **같음** |

⇒ **의도 대조 결과: 일부** — '입자 재료의 암시적 PIC' **채움** · 접촉 · 다물체 (f) **채움** (강체 결합 · 해상도 규칙 없음) · 소성 (l) **일부** (어려움 · 우회는 있고 비용 숫자 없음) · 하중 몫 (d) **없음** · **'가루 침대 준정적 압축 MPM 선례' 없음** (예 셋 모두 2D 동역학 — 선례는 [39] · 정본 `nezamabadi2022_…` · `nguyen2017_…`) · 2 차 인용 값은 맞고, 'GIMP' 귀속 · '해 없음' 은 인용한 원 논문들 (Bardenhagen 2005 · Guilkey 2003) 의 표현이다.

---

## 1. 한 줄 요약
입상체를 '알갱이마다 격자 속도장을 둔 MPM' 으로 푸는 Bardenhagen · Brackbill · Sulsky [38] 의 모형을 명시 도약에서 **θ 암시 판** 으로 옮기고, 마찰 · 소성 때문에 야코비를 만들 수 없는 연립식을 **행렬 없는 inexact Newton–Krylov** (알갱이별 잔차 목록을 이어 붙인 한 벡터 · GMRES · 유한차분 야코비 곱 · 가중 Jacobi 전처리) 로 풀며, 접촉 비력에 **부피 가중** 을 넣어 1 차 정확도로 만든다 — 에너지법 · Neumann 분석으로 암시 θ = ½ 이 **걸음 크기와 무관하게 L2 안정** 이고 유한 격자 불안정을 누른다는 것을 보이고, 2D 탄성 알갱이 벽 충돌 · 광탄성 원판 5 개 응력파 · HMX 370 알갱이 전단에서 명시 도약의 에너지 증가 · 거짓 잔류 응력 · 떨어져 나감이 암시에서 사라짐을 그림으로 보인다 (걸음은 ≤ 10 Δt_exp · 변형 < 1 % 에 묶이고 CPU 비용은 적지 않았다).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (알갱이) | 연구유형 |
|---|---|---|---|---|
| S. J. Cummins · J. U. Brackbill (LANL Theoretical Division) | J. Comput. Phys. 180, 506–548 (2002) | 10.1006/jcph.2002.7101 | **HMX 근사** (PBX 의 폭약 결정 · 탄성 / J2 탄소성) · 광탄성 원판 (파속 맞춤) — **LPSCl · NCM 아님** | 방법 + 수치 분석 (MPM 암시 판 · NK 풀이기 · 안정 분석) + 2D 수치 예 셋 (실험 대조는 정성 · 남의 실험) |

- **1저자 메모 (후보 표) 와의 대조**: 저자 · 제목 · 학술지 · 권 180 · 쪽 506–548 · 2002 — **같다**.  덧붙임: DOI 10.1006/jcph.2002.7101 · 접수 2001-08-15 · 호 미인쇄.
- **글의 꼴**: 1 서론 → 2 변형 알갱이 입상체 모형 (식 1–12) → 3 암시 MPM (3.1 해 공간 · 3.2 공간 차분 · 3.3 암시 / 명시 판 · 3.4 접촉 힘 · 식 13–55) → 4 안정성 (4.1 Neumann · 4.2 유한 격자 불안정 · 4.3 에너지 보존 · 4.4 에너지법 · 식 56–90) → 5 행렬 없는 NK (식 91–104) → 6 비선형 잔차 (식 105–106) → 7 전처리 (7.1 WJ · 7.2 여러 층 · 7.3 결과 · 식 107–118 · 표 I) → 8 결과 (8.1 걸음 제한 · 8.2 NK 반복 끝내기 · 8.3 탄성 알갱이 · 8.4 눌린 알갱이 · 8.5 단분산 전단 · 식 119–126 · 표 II–VII · 그림 1–15) → 9 결론 → 참고문헌 60.  그림 15 · 표 7 (로마 숫자 I–VII) · 번호 식 126.
- 계보 (원문 서술): PIC → FLIP (Brackbill · Ruppel [35] · 암시 차분) ↔ MPM (Sulsky 외 [1, 8] · 명시 도약) — 둘의 차이: FLIP 은 입자 자료를 격자로 보간한 뒤 미분 · MPM 은 형상 함수를 미분한 뒤 보간 → MPM 은 모든 보간식이 켤레 관계를 만족해야 해서 *"MPM typically uses linear b-splines"* (p.510).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 알갱이 모형 (§2 · p.508–509 · `eq_001`–`eq_012` · `txt_p3_elastic_plastic_strain_split_radial_return.png` · `txt_p4_consistency_binder_contact_constraint_two_grains.png`)
- 알갱이 g 마다 연속체 방정식: 질량 dρ_g/dt = −ρ_g ∇·v_g (식 1) · 응력 dσ_g/dt = T_g : de_g/dt (식 2 · T = 접선 계수) · 변형률 속도 (식 3) · 운동량 ρ_g dv_g/dt = ∇·σ_g + Σ_g′ ρ_g f_gg′ (식 4 · f_gg′ = g′ 이 g 에 주는 비접촉력).
- *"The grains are modeled as isotropic, linearly elastic-plastic materials"* · e = e_e + e_pl (식 5) · *"for computational convenience the plastic strain is computed using a radial return rule"* (Sulsky 외 [8]) · de_pl/dt = (dλ/dt) σ_g/|σ_g| (식 6) · λ 는 단조 증가 · 일치 조건 |σ_g| = |σ_yield| (변형 경화 모형).
- 결합재: *"When the grains are held together by a binder, the binder is modeled as viscoplastic material [36, 39]"* (p.509 · 이 논문 예에는 없다).

### 3-2. 접촉 (§2 · §3.4 · p.509 · p.514–515 · `eq_007`–`eq_012` · `eq_048`–`eq_055` · `txt_p9_contact_detection_com_velocity_density_normal.png` · `txt_p10_volume_weighted_contact_first_order_effective_size.png`)
- 침투 금지 n̂_g · (v_g − v_g′) ≤ 0 (식 7): *"In general, this is a very expensive constraint to satisfy, because the computational effort scales as the square of the number of grains."* → ρ_g′ 를 곱해 g′ 로 더하면 n̂_g · (v_g − v) ≤ 0 (식 8) · v = Σρ_g v_g / Σρ_g (식 9 · 원문 철자 *"Fabre-averaged"* = 질량 가중 평균 [카드 해석]) → *"A constraint whose cost scales as the number of grains"*.  두 알갱이일 때만 (7) ≡ (8) — *"We will assume no more than two grains are in contact at any given time"*.
- 경계: *"Imposed strain boundary conditions are imposed through the contact force by specifying v on the boundary."* (p.509) — 벽 = 질량중심 속도를 지정한 같은 제약.
- 공통 법선 가정 n̂_g · n̂_g′ = −1 (식 10) · 운동량 보존 ρ_g f_gg′ + ρ_g′ f_g′g = 0 (식 11) · 결합 = 상대 운동 전부 막음 · 떨어짐 = n̂_g · σ_g · n̂_g ≥ σ_bond 이고 식 (7) 만족 (식 12).
- 판정: *"Points of contact between grains are detected by comparing the grain and center of mass velocities … every point where this condition holds is a contact point where two grains overlap."* · 법선 n_g = −∇ρ_g (식 48 · 내부 노드는 접촉점이 될 수 없어 밀도가 특성 함수로 충분).
- 힘: 시험 속도 ṽ (f = 0 으로 푼 해) 로 n̂_g · (ṽ_g − ṽ) ≤ 0 를 검사 (식 49 · φ = 1 도약 / θ 암시) · 질량중심 속도는 접촉 힘과 무관 (식 50) · 어기면 등식으로 법선 힘 (식 51) · Coulomb 마찰 (식 52) · 마찰 축 단위 벡터 (식 53) · **µ′ = min_g[µ, |ω̂_g × Δṽ| / |ω̂_g · Δṽ|]** (식 54 인쇄 그대로 — 뜻 = 접선 속도가 뒤집히지 않는 상한 · 인쇄 분모는 식 (53) 의 정의로 0 → §3-11) · 원전 = [38].
- **부피 가중** (식 55): V_f,i = Σ_p V_p s(ξ_i − ξ_p) / V_i — 알갱이 안 1 · 밖 0 · *"As grains separate by a full cell, V_f,i decreases to 0. As two grains approach, V_f,i increases through 1 as mass points defining the edge of the grain touch, at which point each grain contributes 1/2 to the weight. When material points interpenetrate, the volume fraction increases to more than 1 causing the grains to repel one another. Volume weighting results in a first-order accurate interaction force [47]. However, it also results in a smaller effective grain size with the same distribution of material points as with the previous version of the contact force without volume weighting [38]."* (p.515).

### 3-3. MPM 이산화 · 암시 / 명시 판 (§3 · p.510–514 · `eq_013`–`eq_047`)
- 두 단계: Lagrange 단계 (격자 · 물질점이 함께 움직임) → 새 격자에 물질점 재배치 · 형상 함수 = **선형 b-spline 의 텐서곱** (식 13–15 · *"bilinear (trilinear) mapping"*) · 격자 → 점 보간 (식 16–18) · 점 변형률 속도 (식 19–20) · 질량 · 응력 = 점의 델타 합 (식 21–23).
- 약형 (Burgess 외 [48] 의 전개): 운동 에너지 변화율 = Σ m_ij v_i · dv_j/dt (식 25) · 일관 질량 행렬 m_ij = Σ_p m_p s_i s_j (식 26 · 양의 대칭) · 격자 속도 = 질량 행렬 역으로 (식 27) · 격자 KE K ≤ 점 KE k 이지만 dK/dt = dk/dt · 격자 운동량식 (식 33) · 점 응력 갱신 (식 34).
- 암시 θ 판 (식 35–43): 걸음 처음 자연 좌표 (35) → 격자 속도 (36 · 보통 **몰아준 질량** m_i = Σ_j m_ij (37) — *"This introduces dissipation so that k¹ − k⁰ < K¹ − K⁰, but eliminates the need to invert a mass matrix"*) → 변형률 증분 · 부피 · 응력 · 격자 운동량을 v^θ 로 (38–41 · ½ ≤ θ ≤ 1) → 점 위치 · 속도 갱신 (42–43) · *"An implicit solution requires that Eqs. (38) through (41) be solved self-consistently."*
- 명시 도약 (식 44–47): 부피 · 응력 · 변형률을 반 걸음 (−½ → ½) · 운동량은 σ^{1/2} 와 f⁰ 로.

### 3-4. ★ 안정성 (§4 · p.515–522 · `eq_056`–`eq_090` · `txt_p11_courant_removed_finite_grid_unstable_l2_stable.png` · `txt_p12_finite_grid_instability_u0_04.png`)
- 요약 (원문): *"standard linear stability analysis shows that implicit differencing in time eliminates the usual Courant stability limit, but that both explicit and implicit MPM are linearly unstable to the finite grid instability, even for Δt = 0. Nonlinear stability analysis shows that implicit MPM is stable in the L2 norm, but that explicit MPM is not."*
- Neumann (1D): 도약 = k s Δt ≥ 1 이면 복소 근 (불안정 · 식 56–57 · s = √(T/ρ₀) 전단파속) · θ 판 = θ = ½ 이면 실수 · Nyquist 안 (식 58–60) · θ > ½ 이면 Im < 0 → 감쇠 (식 61) → *"unconditionally stable, and dissipative for θ > ½"*.
- 유한 격자 불안정 (§4.2): 균일 속도 U₀ 로 움직이는 입자 빔 · 전단파 (식 62–67) → 분산식 (68) = FLIP [34] 과 같은 꼴 → *"The finite-grid instability will occur at all wave numbers in the principal interval for values of U₀/√(λ/ρ₀) < 0.4 (when s is a linear b-spline)."* · Δt 는 공명을 옮길 뿐 · 암시 플라스마 계산에서도 일정 걸음 범위에서만 사라짐 [5].
- 에너지 (§4.3): K = ∫½ρv² (69) · S = ∫½ e:T:e (70) · θ 판 에너지 등식 (74 — 마지막 항 = v^θ 를 v^{1/2} 대신 쓴 오차) · 변형 에너지 오차 (77 — 걸음마다 줄이는 쪽) · 법선 접촉 일 = 0 (79) · 마찰 일 ≤ 0 (82) · 소성 일 P ≤ 0 (83 · λ 단조) · 몰아준 질량 감소 L (84 · 음의 정부호 [35]) → **E^n = E^{n−1} − (θ − ½)Σ[m_p |Δv_p|² + Δe_p : T : Δe_p] + F + P + L** (식 85 · θ ≥ ½) · *"exact energy conservation could be achieved in the usual way by storing an internal energy"*.
- 에너지법 (§4.4): 도약은 에너지를 적어도 O(Δt³) 로 지키지만 (Mazur [30]) 단진동의 두 에너지 적분 (86 · 87) 에서 운동 · 변형 에너지가 각각 묶이지 않는다 → *"the leapfrog algorithm cannot be shown to be stable in the L2 norm"* · 비선형 파국 불안정은 해가 0 근처에서 진동할 때 잦다 (Fornberg [11] · aliasing) · 암시: k^n, s^n ≥ 0 (88) · E^n ≤ E⁰ (89) → k^n, s^n ≤ E⁰ (90) → *"the implicit θ scheme is stable in the L2 norm independent of the time step"*.

### 3-5. 행렬 없는 inexact Newton–Krylov (§5–6 · p.522–525 · `eq_091`–`eq_106` · `txt_p17_inexact_matrix_free_nk_vs_benson_guilkey.png` · `txt_p18_friction_plasticity_nonanalytic_jacobian.png`)
- 다른 갈래와의 차이 (원문): *"This implicit integration algorithm is in contrast to that of Benson [12], who implemented an implicit Eulerian formulation based on mixture theory by solving a quasi-Newton problem. It is also in contrast to the work of Guilkey and Weiss [55], who solved a linearized implicit form of the MPM equations (with intergranular contact neglected) by inverting a stiffness matrix."* (p.522).
- ★ **미지수 = 알갱이별 노드 목록을 이어 붙인 속도** — F = [F_x, F_y] · F_x = [F¹_x, …, F^N_x] (N = 알갱이 수) · 알갱이 g 의 목록은 *"all nodes i belonging to g"* (N_g 개 · 식 91–95) · *"When grains come into close contact, a node i can be shared between more than one grain … the contact force couples the grains, and one must solve for a full multivalued velocity field"* (p.523).
- 수렴 ‖F(v^{k+1})‖₂ / F_scale < tol = **10⁻⁶** (식 96 · F_scale = V_char Σ m_p · 식 106) · Newton (97–99) · GMRES (Krylov 기저 · 식 100) · **J r ≈ [F(v + εr) − F(v)]/ε** (식 101) · ε = 0.001 × (1/N)‖r‖₂ Σ|v^k| (식 102 · 인쇄 그대로 — 흔한 행렬 없는 꼴은 ‖r‖₂ 를 분모에 두므로 조판으로 보임 [카드 해석] · *"The choice of perturbation parameter ε is heuristic and affects convergence considerably"*) · inexact: 선형 허용치 ∝ 비선형 잔차 · **γ = 0.001** (식 103–104).
- 잔차 (식 105 · θ 중심): m_i (v^{n+θ} − v^n)/(θΔt) − Σ_p ∇_pi · σ_p V_p + m_i f_i.  **질량 가중**: *"At grain edges, the nodal mass can be orders of magnitude smaller than in the interior … The internal force and nodal mass do not scale here."* → 가중하지 않으면 강성 (stiff) 잔차 · 큰 걸음에서 대각 우세가 깨져 *"the linear problem is poorly conditioned and the linear iteration converges slowly"* (p.524).
- FLIP 내부력 판 (셀 중심 2 차 기울기 · 2 차 보간): 조건수가 나아 *"the total number of linear iterations was halved"* (탄성 알갱이) · 명시에서도 더 튼튼 — 그러나 *"The stencil is broader, however, and produces errors in shearing near the grain edges. Therefore the MPM implementation is consistently used in this work."* (p.525).

### 3-6. 전처리 (§7 · p.525–530 · `eq_107`–`eq_118` · 표 I · 그림 1 · 2 · `txt_p25_multilevel_contact_scales_with_mesh.png`)
- 오른쪽 전처리 (식 107–110) · 가중 Jacobi y^s = y^{s−1} + (w/D)(V − M y^{s−1}) · **w = 0.67** · **두 번** (식 112) · M y 도 잔차 차분 (식 113) · 전처리 안에서는 질량중심 속도를 고정 (단순 잔차 F̃ · 식 114 — 내부력 · 접촉력을 격자 한 번 훑기로).
- 대각 D: 단위 벡터마다 하면 2n 번 → 2D MPM 잔차의 영향 범위 = **9 셀** → *"The diagonal D can therefore be calculated using 18 rather than 2n calls to the matrix-free approximation."* (p.528) · [카드 산술] 같은 묶음 탐침이면 3D 선형 b-spline = 27 × 3 = **81 번** · 3D 2차 B-spline (5³ 노드 영향) = 125 × 3 = **375 번**.
- 여러 층 (V-cycle · 식 116–118): 굵은 물질점 = 한 셀 안 질량 · 부피 합 · 질량중심 위치 · 속도 · 부피 가중 응력 (총질량 · 총운동량 불변) · 제한 = 질량 가중 2 차 보간 · 연장 = 이선형 · 그림 2 = 32 × 32 → 4 × 4 네 층의 노드 질량 등고.
- **표 I** (탄성 알갱이 · **64 × 64** · t = 0.5 · GMRES 최대 10) [인쇄]: 전처리 없음 Newton **4249** · 선형 **42490** (Newton 당 10.00 = 상한) / 1 층 **1724** · **6727** (3.900) / 2 층 1711 · 4590 (2.683) / 3 층 1695 · 4587 (2.706) / 4 층 1717 · 4596 (2.677) / 5 층 1691 · 4442 (2.627) / 6 층 1696 · 4452 (2.625).  [카드 산술] 한 층 WJ = Newton ÷2.46 · 선형 ÷6.3 · 층을 더하면 선형만 −32 ~ −34 % · Newton 그대로.
- 원문 판정: *"For multilevel preconditioners, the results are somewhat disappointing … the representation of the contact force is self-similar with mesh spacing. Therefore as the mesh coarsens the distance over which the contact force act increases (it scales with the mesh size) and hence the proportion of the grain under contact increases. Indeed for a coarse enough grid (i.e., 1 × 1 grid), the single grain will always be in contact with the boundaries."* (p.530).

### 3-7. ★ 걸음 크기 · NK 끝내기 (§8.1–8.2 · p.530–531 · `eq_119`–`eq_123` · `txt_p25_time_step_strain_1pct_025_sigma_y.png` · `txt_p26_poor_conditioning_10x_explicit_halving.png`)
- 암시: Δt_imp < 0.01 / |de/dt|_max (식 119) · |de/dt|_max = √(¼[∇v + ∇vᵀ] : [∇v + ∇vᵀ]) (식 120) — *"The idea behind the constraint is to ensure that an undisturbed stress state will not evolve to a plastic yielded state in one time step"* · *"For the plastic granular materials in this paper, a strain of 1% will result in a stress increment of ≈0.25 × σ_y"* · [카드 산술] µ × 1 % = 7.48 GPa × 0.01 = 74.8 MPa = **0.249 σ_y** (σ_y 300 MPa) — 0.25 σ_y 는 **전단 계수 × 변형** 으로 읽힌다 · *"While this strain restriction is relevant only to plastic materials, we apply it to simulations of purely elastic materials as well. For materials with different yield properties the maximum strain limit will need to alter."*
- 명시: s = √((λ + 4/3 µ)/ρ) (식 121) · Δt_exp < α Δx / s (식 122) · *"A conservative CFL stability limit of α = 0.25 gives better energy conservation with the explicit leapfrog method"* · Δt_exp < min(1 % 변형 · αΔx/s) (식 123).
- 끝내기: *"The linear systems solved in this study become poorly conditioned for time steps Δt > 10 × Δt_exp. The use of the preconditioner aids in the efficiency of the solution for Δt < 10 × Δt_exp but does not increase the radius of convergence. The reason for this is currently unclear."* → GMRES Krylov 수 상한 · 못 맞추면 잔차를 다시 계산 · *"If convergence of the nonlinear problem has not been achieved after a maximum number of Newton iterations, the time step is halved and the Newton–Krylov iteration started again."*
- [카드 산술 · Δt_exp 에 α 0.25 가 들어 있다고 읽음] 10 Δt_exp = 2.5 Δx/s = **P파 Courant 수 2.5** · 2.5 Δt_exp = Courant 0.625.

### 3-8. ★ 탄성 알갱이 벽 충돌 (§8.3 · p.531–535 · 표 II · III · 그림 3–6 · `txt_p29_energy_explicit_order_magnitude_implicit_7pct.png` · `txt_p29_elastic_energy_accumulation_wave_speed_3pct.png` · digitized.csv fig6_*)
- **표 II** [인쇄]: 격자 **17 × 17** · Δx = Δy = **8.118 × 10⁻⁶ m** · 셀당 물질점 최대 **4** · 계산 시간 **2.00** · Δt_MAX = **2.5 × Δt_exp** · *"Bulk modulus λ"* **11.36 × 10⁹ Pa** · µ **7.48 × 10⁹ Pa** · ρ **1.9 × 10³ kg/m³** · U₀ **−1.0 × 10² m/s** · V₀ 0 · *"representative of the material high melting explosive (HMX) used in plastic bonded explosives (PBX) … assumed to have an infinite yield stress"*.
- **표 III** [인쇄]: Newton 허용치 10⁻⁶ · ε 10⁻³ · γ 10⁻³ · F_scale = U₀ × Σm_p · Newton 최대 **20** · 선형 최대 **5** · 전처리 **없음** · θ **0.5**.
- **그림 3** [인쇄]: 상자 X_max = Y_max = 1.38 × 10⁻⁴ m · 중심 (0.73, 0.73) × 10⁻⁴ m · R = 0.50 × 10⁻⁴ m · U = −1.00 × 10² m/s (왼쪽 벽으로).
- [카드 산술] 지름 = 12.3 칸 · 물질점 ≈ 4 × π × 6.16² ≈ **480** · 식 (121) 그대로 s = √((11.36 + 9.97) × 10⁹ / 1900) = **3351 m/s** · U₀/s = **0.030** · Δt_exp (α 0.25) = 6.06 × 10⁻¹⁰ s · 유한 격자 기준 U₀/√(λ/ρ) = 100/2445 = **0.041 < 0.4** (불안정 구간) · 첫 벽 접촉 ≈ (73 − 50 µm)/100 m/s = 0.23 µs ↔ 그림 6 첫 봉우리 t ≈ 0.24 [판독] → **그림 시간 단위 = µs**.
- [카드 산술 · 단위 확인] 처음 운동 에너지 ½ρπR²U₀² = 7.46 × 10⁻⁹ g·cm²/µs² (깊이 1 cm 당) ↔ 그림 6 처음 총에너지 **7.33 × 10⁻⁹** [판독] (−1.8 %) · 운동량 ρπR²U₀ = 1.49 × 10⁻⁶ ↔ 암시 판 평평한 구간 **1.41 × 10⁻⁶** [판독] → 그림의 에너지 · 운동량은 **g · cm · µs 단위 (깊이 cm 당)** [카드 해석].
- **명시 (그림 5 · α 0.25 · 1.0)**: *"the edges of the grain separate from the main body. The grain spallation is more catastrophic when the CFL limit is increased to α = 1.0. Spallation is completely absent in the implicit results"* · *"For the explicit leapfrog, the total energy grows by an order of magnitude"* — [판독] 7.33 × 10⁻⁹ (t 0) → 1.35 × 10⁻⁸ (0.5) → 3.82 × 10⁻⁸ (1.0) → 1.06 × 10⁻⁷ (2.0) = **×14.5** · 탄성 에너지 국소 최대 1.6 × 10⁻⁸ (0.6) → 8.6 × 10⁻⁸ (1.85) · x 운동량 판 |p| 1.37 → 1.51 → 1.82 → 2.07 (× 10⁻⁶) · 마지막 −2.16 × 10⁻⁶ (*"a spurious increase in momentum after each interaction"*) · 원인 (원문): 걸음 처음 속도만으로 내부력 · 셀 경계를 넘는 작은 질량 노드의 큰 가속 (*"Using the velocity at the start of the time step is clearly in error"*) · 단순 이류 중 에너지 증가 = 유한 격자 불안정.
- **암시**: *"the total energy grows to a maximum variation of ≈7% in the implicit scheme"* — [판독] 7.33 × 10⁻⁹ → 8.50 × 10⁻⁹ (t 2.0) = 처음→끝 **+16 %** · 평균 둘레 ±7.4 % [카드 산술 = (최대 − 최소)/(최대 + 최소)] → 원문 '≈7 %' 는 평균 둘레 반폭으로 읽으면 맞는다 [카드 해석] · 탄성 에너지 접촉 사이 바닥 0.81 → 2.61 (× 10⁻⁹ · t 0.35 → 1.8) · 접촉 봉우리 ≈7 × 10⁻⁹ [판독 · 래스터] · *"approximately two orders of magnitude less than that seen in the explicit case"* — [카드 산술] 쌓인 양 ≈8 × 10⁻⁸ ↔ ≈1.8 × 10⁻⁹ = ≈44 배 (≈1.6 자릿수) · *"Reducing the Newton tolerance in the nonlinear solution reduces this growth"* · 운동량 판 |p| 1.41 → 1.35 → 1.30 → 1.28 (× 10⁻⁶) [판독] = 몰아준 질량의 소산.
- 원문 주장: *"In [34] it is speculated that large time steps compared with the CFL limit are required to dampen the instability growth. This appears to be incorrect. Our calculations with the stability time step constraint in Eq. (123) with α = 0.25 and α = 0.10 are stable and energy conserving and show that a large time step is unnecessary for stability."* (p.534).
- 정확도: *"there is no analytical solution for the propagation speed of elastic waves in an impacting circular grain"* → 직사각 블록 충돌로 대신 · *"After the first wall interaction a 3% error was incurred for both implicit and explicit formulations."*

### 3-9. 원판 5 개 응력파 — *"Compressed Grains"* (§8.4 · p.535–540 · 표 IV · V · 그림 7–10 · `eq_124`–`eq_126` · `txt_p32_pwave_noise_energy_1pct.png` · digitized.csv fig10)
- 동기: Rossmanith · Shukla [49] 의 광탄성 동적 재하 실험 (뇌관) · Bardenhagen 외 [50] 의 명시 MPM 재현 (홉킨슨 봉 · 속도 계단) — *"The explicit MPM formulation was found to reproduce the character of the stress wave propagation closely although some calibration was required due to the uncertainty of the experimental material properties."* · 이 예의 목적: *"to highlight the extended range of applicability and robustness of the implicit formulation over the explicit formulation due to the suppression of the finite-grid instability"*.
- **표 IV** [인쇄]: **36 × 176** · Δx = Δy = **3.125 × 10⁻⁴ m** · 셀당 최대 4 · 계산 시간 **60.00** · Δt_MAX = **10.0 × Δt_exp** · λ **4.786 × 10⁹** · µ **2.893 × 10⁹ Pa** · ρ 1.9 × 10³ · U₀ 0 · V₀ **−1.00 × 10¹ m/s** · 재하 시간 **0.12 µs**.  **표 V**: Newton 최대 **5** · 선형 최대 **10** · 전처리 **WJ 1 층 · 2 번** · θ 0.5.
- **그림 7** [인쇄]: 원판 5 개 (R = 0.50 × 10⁻² m) 를 세로로 쌓고 맨 위 판 ((X_g, Y_g) = (1.12, 5.00) × 10⁻² m → (X_p, Y_p) = (1.12, 5.25) × 10⁻² m) 에 V₀ · *"The disks are separated from the left and right boundaries by a distance of 2Δx"*.
- 파속: λ · µ 는 [49] 의 P · S 파속을 내도록 정함 — P = √((λ + 4/3 µ)/ρ) = **2.133 × 10³ m/s** (식 124) · S = √(µ/ρ) = **1.234 × 10³ m/s** (식 125) · 무늬 Fr = cos[2π f_no (σ₁ − σ₂)/max(σ₁ − σ₂)] (식 126 · **f_no 값 미인쇄**).
- 결과: *"The explicit and implicit calculations display similar average propagation speeds, with the P-wave speed ≈2.5 × 10³ m/s. However, as the explicit calculation proceeds, the fringe patterns are dominated by high frequency noise … In contrast, the implicit formulation does not exhibit this high frequency noise and total energy is conserved to within 1%."* · [판독 그림 10] 암시 5.379 × 10⁻⁷ (t 1) → 5.349 × 10⁻⁷ (t 50) = **−0.56 %** · 명시 5.44 × 10⁻⁷ (2.5) → 5.62 × 10⁻⁷ (9) → 5.51 (16) → 5.87 × 10⁻⁷ (60) = **+7.9 %** (2.5 → 60) [카드 산술].
- [카드 산술] 원판 지름 = **32 칸** · 물질점 ≈ 4 × 5 × π × 16² ≈ 16,000 (+ 위 판 ≈1,150) · Δt_exp (α 0.25) = 3.66 × 10⁻⁸ s · Δt_MAX = 0.366 µs · V₀/P = 0.0047 · 기둥 5 cm 를 P파가 지나는 시간 ≈ 23 µs · 재하 = 계산 시간의 0.2 % (원문: *"the same fractional component of the simulation time as in [49]"*) · 측정 P파 2.5 × 10³ 는 설정 2.133 × 10³ 보다 **+17 %** (원문 설명 없음 · λ 를 라메 상수로 읽어 √((λ + 2µ)/ρ) 로 셈해도 2.36 × 10³).

### 3-10. ★ HMX 370 알갱이 단분산 전단 (§8.5 · p.540–545 · 표 VI · VII · 그림 11–15 · `txt_p35_shear_volume_weighting_critical_density_hmx.png` · `txt_p40_stress_histogram_mean_twice_346.png` · digitized.csv fig14_* · fig15)
- 동기 · 설정: [37] (Bardenhagen 외 2000 · 2D 전단 응력 분포) 의 문제를 다시 · *"The motivation behind this problem is the accurate numerical simulation of plastic bonded explosives"* · *"The constitutive equation is elastic-plastic and the contact algorithm incorporates Coulomb friction. The material constants chosen model the crystal HMX."* · 육방 충전 **370 알갱이** · 양옆 알갱이를 벽에 붙이고 오른쪽 벽을 V 로 (그림 11 의 화살표 = 위쪽 → 벽과 나란한 전단 [카드 해석]) · 위아래 주기 · t = 40.0 µs (*"the average shear strain exceeds 300%"*).
- **표 VI** [인쇄]: **156 × 150** · Δx = Δy = **8.118 × 10⁻⁶ m** · 셀당 최대 4 · 계산 시간 **40.00** · Δt_MAX **10.0 × Δt_exp** · λ **1.136 × 10⁸ Pa** (⚠ 표 II 는 같은 HMX 에 11.36 × 10⁹) · µ **7.48 × 10⁹** · ρ 1.9 × 10³ · V **1.00 × 10² m/s** · σ_y **3 × 10⁸ Pa** · 경화 H **1 × 10⁷ Pa** · **ν 0.3** (이름 없는 줄 — 마찰 계수로 읽힌다: 원전 [38] 의 같은 HMX 전단 문제 마찰 µ = 0.3 [다른 카드 · `bardenhagen2000_…` L110] · 이 논문은 µ 를 전단 계수 기호로 쓴다 [카드 해석]) · 그 밖의 마찰 · 결합 값 미인쇄.  **표 VII**: Newton 최대 **5** · 선형 최대 **5** · WJ 1 층 2 번 · θ 0.5.
- **그림 11** [인쇄]: X_max 1.27 × 10⁻³ m · Y_max 1.22 × 10⁻³ m · *"R = 3.26x10⁻³ m"* · *"V = 1.00x10⁻² m/s"* — [카드 해석] 그림 12 축이 0–0.127 (cm) 라 코드 단위 = cm · µs → R = 3.26 × 10⁻³ cm = **32.6 µm** · V = 10⁻² cm/µs = 100 m/s (표 VI 와 맞음) · [카드 산술] 지름 = **8.0 칸** · 물질점 ≈ 370 × 4 × π × 4.02² ≈ **75,000** · 면적 분율 370πR²/(X_max Y_max) = **0.797** (2D 육방 최조밀 0.907) · 줄 수 1.22 mm/(√3 R) ≈ 21.6 · 줄당 1.27 mm/2R ≈ 19.5 (≈ 370 알갱이 재현).
- 부피 가중의 효과 (명시끼리): *"Without the volume weighting, the overall packing order is lost by time t = 35 µs (which corresponds to an average shear strain of 284%)"* ↔ 부피 가중이면 *"By time t = 40 µs (… 330%), approximately one third of the structure is still regular near the center"* · *"The volume-weighted contact force allows a denser row packing before the onset of row buckling"* · *"the effective size of the grains is smaller with a volume-weighted contact function, and the density of the grains falls just below the critical density"* ('임계 밀도' 정의 · 값 [미확인]).
- 암시 ↔ 명시: *"In the implicit results, the disorder propagates even more slowly than the explicit calculation"* (원인 = 명시의 에너지 비보존이라고 *"postulated"*) · *"the total energy grows by two orders of magnitude more for the explicit calculation than the implicit calculation"* — [판독 그림 14] 명시 총에너지 6.1 × 10⁻⁷ (t 1) → 7.0 × 10⁻⁶ (t 39) · 암시 2.2 × 10⁻⁷ (t 1) · 0.67–2.3 × 10⁻⁷ 사이에서 오르내림 · 1.99 × 10⁻⁷ (t 40) → 끝 값 비 **≈35 배 (≈1.5 자릿수)** [카드 산술 — 원문 '두 자릿수' 보다 작다] · 명시 탄성 에너지 2.3 × 10⁻⁷ → 4.5 × 10⁻⁶ (단조 증가 = *"spurious residual grain stresses after collisions"*) · 암시 탄성 에너지 1.2 × 10⁻⁹ – 2.6 × 10⁻⁸ 에서 오르내림 · *"The energy dissipated by plasticity ensures the explicit calculation remains robust without grain spallation."*
- **그림 15** (t > 10.0 µs · 면적 분율 히스토그램): *"the explicit algorithm consistently produces more grains with principal stress differences > 30 MPa. As a result, the mean principal stress difference is nearly twice that produced from the implicit calculation"* · 범례 [인쇄] **암시 평균 25.55 · 명시 평균 46.02 (MPa)** → 비 1.80 [카드 산술] · 명시 분포 = 평균 위에서 지수 꼴 ([37] 과 같음) · 암시는 작은 응력에서 벗어남 (왼쪽 알갱이가 아직 변형 전 · 정상 상태 아님) · [판독] 암시 봉우리 ≈12 MPa (면적 분율 3.1 × 10⁻²) · 100 MPa 에서 6.5 × 10⁻⁴ ↔ 명시 2.3 × 10⁻³ · 마지막 표지 342 MPa · 명시 끝 331 MPa · *"Both distributions are bounded by Δσ ≤ 2/√3 σ_y = 346 MPa"* (평면변형률 J2 의 최대 주응력차 [카드 해석]).
- [카드 산술] 평균 전단 변형: V t / L — 330 % @ 40 µs 이면 L = 1.21 mm · 284 % @ 35 µs 이면 L = 1.23 mm (기준 길이 미인쇄) · s (표 II λ) = 3351 m/s → V/s = 0.030 · Δt_MAX = 6.06 × 10⁻⁹ s → 40 µs 에 **≥ 6,600 걸음** (모두 최대 걸음이라 가정).

### 3-11. 원문 안 어긋남 · 원문에 **없는** 값 (정직 목록)
- **λ 의 뜻 · 값**: 표 II · IV 는 λ 를 *"Bulk modulus"* 로 부르고 식 (121) · (124) 는 P파 계수를 **λ + 4/3 µ** 로 쓴다 (λ = 체적계수 K 로 읽어야 맞는 꼴) · 원전 [38] 의 같은 HMX 근사 = 체적계수 11.4 GPa [다른 카드 · `bardenhagen2000_…` L101] → 11.36 GPa = K 로 읽힌다 (그러면 푸아송비 = (3K − 2µ)/(2(3K + µ)) = **0.23** [카드 산술] · 11.36 GPa 를 라메 상수로 읽으면 0.30) · [38] 의 HMX 값 (전단 7.5 · 체적 11.4 · 항복 0.3 · 경화 0.01 GPa · 1900 kg/m³) 이 이 논문 표 II · VI 와 같다 → 표 VI 의 λ **1.136 × 10⁸** 은 1/100 로 찍힌 오기로 보인다 [카드 해석] · 표 VI 의 이름 없는 **ν 0.3** 은 푸아송비가 아니라 마찰 계수 ([38] 의 µ 0.3 [다른 카드 · `bardenhagen2000_…` L110]) 로 읽힌다 [카드 해석] · 코드 안 λ 의 뜻 [미확인].
- **식 (54) 의 분모**: ω̂_g = n̂_g × Δṽ / |n̂_g × Δṽ| (식 53) 는 Δṽ 에 수직이라 인쇄된 분모 ω̂_g · Δṽ 는 늘 0 이고 분자 |ω̂_g × Δṽ| 는 |Δṽ| 다 → 본문의 뜻 (*"so that the velocity does not reverse sign under the action of friction"* p.520) 에 맞는 꼴은 '접선 상대 속도 / 법선 상대 속도' 상한 (|n̂_g × Δṽ| / |n̂_g · Δṽ|) 로 읽힌다 — 원전 [38] 의 같은 식 (21) 은 실제로 n̂ 으로 적는다 (μ′ = min(μ, ‖Δv × n‖ / (Δv · n)) [다른 카드 · `bardenhagen2000_…` L169]) → 이 논문 식 (54) 는 n̂ 를 ω̂ 로 잘못 찍은 것으로 보인다 [카드 해석].
- **그림 11 단위**: R · V 가 'm' · 'm/s' 로 인쇄 — 코드 단위 (cm · cm/µs) 값 [카드 해석 · 위 §3-10].
- **측정 P파 ≈2.5 × 10³ ↔ 설정 2.133 × 10³ m/s (+17 %)** — 원문 설명 없음.
- **'≈7 %'** (암시 탄성 알갱이 총에너지) — 판독 처음→끝 +16 % · 평균 둘레 ±7.4 % → 반폭 뜻으로 읽힘 · **'두 자릿수'** (전단 총에너지) — 판독 끝 값 비 ≈35 배.
- 표 I 은 **64 × 64** 에서 (탄성 알갱이 예의 표 II 는 17 × 17) · 그 실행의 Δt · 걸음 수 미인쇄.
- 철자 *"Fabre-averaged"* (질량 가중 평균) · *"0(Δt³)"* (= O(Δt³)) · ref [50] *"private communication"* = 출판본 `bardenhagen2001_…` (CMES 2001).
- **없는 값**: CPU · 벽시계 시간 · 메모리 · 기계 · 걸음 수 · 실제 Newton/Krylov 반복 수 (표 I 외) · 마찰 계수의 이름 (표 VI 의 'ν 0.3' 으로 읽힘) · σ_bond · f_no · 평면변형률/평면응력 · 3D 계산 · 격자 · 물질점 수렴 · 압력 · 기공 · 밀도 · 탈압.

---

## 4. ★ 방법 — 모형 → 이산화 → 접촉 → 안정 → 풀이기 → 예

### 4-1. 모형 사슬
알갱이마다 연속체 (탄소성 J2 · 반경 귀환 · 선형 경화) + 알갱이마다 격자 속도장 → 접촉 비력 (질량중심 속도와 비교 · 부피 가중) → MPM 두 단계 (Lagrange 단계 = θ 암시 · 재배치) → 잔차를 알갱이별 노드 목록으로 이어 붙여 행렬 없는 NK.  **명시 도약 판은 같은 코드의 비교 판** (α 0.25 · 1.0).

### 4-2. 접촉의 작동 (원문 식만으로)
① 각 알갱이를 f = 0 으로 푼 시험 속도 ṽ_g 와 질량중심 속도 ṽ (접촉 힘과 무관) ② 노드마다 n̂_g · (ṽ_g − ṽ) > 0 이면 (다가옴) 그 차를 지우는 법선 힘 ③ 마찰은 접선 속도 차를 µ′ 만큼 (뒤집히지 않게) ④ 결합이면 상대 운동 전부 · 법선 견인력 ≥ σ_bond 이면 떨어짐 ⑤ 힘에 부피 분율 V_f 를 곱함 (한 셀 떨어지면 0 · 닿으면 ½ 씩 · 파고들면 > 1) ⑥ 벽 = ṽ 를 지정한 같은 규칙.  암시 판에서는 이 힘이 Newton 반복마다 다시 계산된다 (*"The contact force responds to this internal force which will then alter the estimate of the time-averaged velocity. The process continues until the solution relaxes to an equilibrium"* · p.534).

### 4-3. 입자 처리 ★
- 알갱이 = **물질점 묶음 (연속체)** — 모양이 변하고 (탄성 · 소성) 이력 (소성 변형) 을 싣는다: *"The material points resolve edges, support a multiple valued velocity so that sliding can be modeled, eliminate the numerical diffusion that would ordinarily occur as a grain moves, and allow history-dependent effects such as plastic strain to be recorded."* (p.507).
- 알갱이 정체성 = 속도장의 번호 (알갱이 경계를 기억 — 우리 조건 R3 의 꼴).
- DEM 처럼 강체 구 · 점접촉으로 두는 부분은 **없다**.

### 4-4. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **직접 한계 문장 없음**.  대조 문장 둘 (p.506–507 · `txt_p2_dem_force_laws_grain_scale_deformable_models.png`): contact dynamics = *"assume that the individual grains are perfectly rigid … nonlocal character to momentum transfers that requires that all kinematic constraints be simultaneously accounted for"* · DEM 힘 법칙 = *"hard core potential [29], or a contact law derived from Hertz–Mindlin theory [16]"* ↔ *"methods which seek to model the material properties of the grains realistically [38, 44, 45]. These models resolve grain scale lengths, allow grains to deform, and solve continuum equations in which contact and friction have been regularized."* — DEM 이 알갱이 변형 · 크기 척도를 풀지 않는다는 것은 **대조로만** 읽힌다 [카드 해석].
2. **소성 · 큰 변형을 넣기 어려운 이유 · 우회 · 비용** — 이유: 마찰 · 소성의 비선형 + 소성의 비해석성 → 야코비를 역으로 풀기 어려움 (p.523 · `txt_p18_friction_plasticity_nonanalytic_jacobian.png`) · Coulomb 의 불연속 (p.507 · `txt_p2_quasistatic_motivation_implicit_challenges.png`) · 항복 직전 응력 정확도 → 걸음 제한 (p.530) · 자료가 수많은 물질점에 흩어짐 (p.508).  우회: 행렬 없는 NK (야코비 × 벡터 = 잔차 차분) · 질량 가중 잔차 · 걸음 < 1 % · 조건수 벽 앞에서 걸음 반.  값: HMX J2 σ_y 300 MPa · H 10 MPa (맞춘 값 0 · 원전 [38]).  검증: 에너지 장부 (소성 소산 P ≤ 0) · 응력 분포 · 346 MPa 상한.  비용: 표 I 반복 수 · CPU [미확인].  저자 결론: *"The algorithm is ideally suited to the nonlinear and nonanalytic characteristics of MPM that result from grain plasticity and intergranular contact and will easily accommodate improved physics, such as grain fracture and intergranular binding."* (p.545).
3. **2D / 3D** — 계산 전부 2D · 식은 d 차원 (*"bilinear (trilinear)"*) · 잔차 · 대각 추출은 2D 로 적힘 · 전이 진술 없음.
4. **압력을 뺄 때의 거동** — 압밀 탈압 **없음**.  벽 충돌 뒤 반발 (동역학 분리) 에서 명시의 거짓 잔류 응력 · 운동량 · 암시의 탄성 에너지 쌓임 ≈1/100 (원문) — 수치 방식이 '되돌아온 뒤 남는 응력' 을 만들 수 있다는 증거 [카드 해석].

### 4-5. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| PIC · FLIP · MPM | 입자-격자 혼합법 · 격자에서 운동을 풀고 입자가 상태를 싣는다 · FLIP 은 보간 뒤 미분 (암시 차분) · MPM 은 형상 함수 미분 뒤 보간 (선형 b-spline · 명시 도약) |
| 도약 (leapfrog) | 속도와 위치 (응력) 를 반 걸음 엇갈려 명시로 갱신 · 에너지를 O(Δt³) 로 지키지만 L2 안정은 아님 |
| θ 판 | 걸음 처음 · 끝 값을 θ 로 섞어 평가 (θ = ½ 이면 2 차 · 에너지 보존 · θ > ½ 감쇠) |
| 유한 격자 불안정 (ringing) | 입자 밀도 변조가 격자 위에서 구분되지 않아 (aliasing) 생기는 불안정 · 느린 흐름 (U₀/√(λ/ρ) < 0.4) 에서 · 에너지 증가가 표지 |
| L2 안정 (에너지법) | 해의 크기 (여기선 운동 + 변형 에너지) 가 처음 값으로 묶임 |
| 몰아준 질량 (lumped mass) | 질량 행렬을 대각 합으로 바꿈 · 역행렬이 필요 없고 운동 에너지를 조금 소산 |
| 행렬 없는 NK | Newton 의 선형식 J δv = −F 를 GMRES 로 풀되 J 를 만들지 않고 J r ≈ [F(v + εr) − F(v)]/ε 로 곱만 |
| inexact | 선형식을 비선형 잔차에 비례한 허용치 (γ = 10⁻³) 까지만 풂 |
| 오른쪽 전처리 · 가중 Jacobi | J M⁻¹ (Mδv) = −F 꼴 · M⁻¹ 를 대각 D 로 두 번 완화 (w 0.67) |
| V-cycle 여러 층 | 굵은 격자 · 굵은 물질점에서 오차를 고쳐 되돌림 (이 논문에서는 이득 작음) |
| 부피 가중 접촉 | 노드의 물질 부피 분율로 접촉 힘을 가중 → 1 차 정확 · 효과 알갱이 크기 작아짐 |
| 질량중심 (Fabre) 속도 | 노드에 걸친 알갱이 속도들의 질량 가중 평균 · 접촉 판정 기준 |

---

## 5. Figure set ★
| 그림 · 표 | 내용 | 우리 활용 |
|---|---|---|
| 그림 1 (`fig_1.png`) | 굵은 층 물질점 · 격자를 고운 층에서 만드는 도식 | 여러 층 전처리 (이득 작음 — 접촉 거리 ∝ Δx) |
| 그림 2 (`fig_2.png`) | 32 × 32 탄성 알갱이 · t = 0.5 · 네 층 (32 × 32 → 4 × 4) 물질점 위치 · 노드 질량 등고 | 굵은 층에서 지지가 넓어지는 모습 |
| 그림 3 (`fig_3.png` · 손 크롭) | 탄성 알갱이 처음 배치 (상자 1.38 × 10⁻⁴ m · R 0.50 × 10⁻⁴ m · U −100 m/s) | ★ 단위 시험 (U1 · U5) 의 기하 |
| 그림 4 (`fig_4.png`) | 암시 판 알갱이 위치 (여러 시각) | 떨어져 나감 없음 |
| 그림 5 (`fig_5.png`) | 명시 판 t = 2.00 · α 0.25 · 1.0 | ★ 명시 도약의 가장자리 떨어져 나감 (α 1.0 이 더 심함) |
| 그림 6 (`fig_6.png`) | 총에너지 (로그) · 탄성 에너지 · x 운동량 — 암시 (+) ↔ 명시 (선) | ★ 에너지 장부 결과 전 대조 (×14.5 · +16 % [판독]) |
| 그림 7 (`fig_7.png`) | 원판 5 개 기둥 + 위 판 · V₀ −10 m/s · 0.12 µs | 다물체 응력파 단위 시험 (U5) |
| 그림 8 · 9 (`fig_8.png` · `fig_9.png`) | 주응력차 무늬 — 암시 / 명시 (α 0.25) · 여러 시각 | 명시의 고주파 잡음 (유한 격자 불안정) |
| 그림 10 (`fig_10.png`) | 원판 총에너지 — 암시 −0.56 % · 명시 +7.9 % [판독] | 에너지 장부 |
| 그림 11 (`fig_11.png` · 손 크롭) | 전단 처음 배치 (370 알갱이 · 육방 · 단위 표기 어긋남) | — |
| 그림 12 · 13 (`fig_12.png` · `fig_13.png`) | 전단 알갱이 위치 + 주응력차 (t 10 · 20 · 30 · 40 µs) — 암시 / 명시 | 응력 사슬 · 무질서 전파 |
| 그림 14 (`fig_14.png`) | 전단 총 · 탄성 에너지 (로그) — 명시 7.0 × 10⁻⁶ ↔ 암시 1.99 × 10⁻⁷ (t 40) [판독] | 거짓 잔류 응력 = 탄성 에너지 단조 증가 |
| 그림 15 (`fig_15.png`) | 주응력차 면적 분율 (로그) — 평균 25.55 ↔ 46.02 MPa (범례) · 상한 346 MPa | ★ 응력 통계가 시간 적분 방식에 1.8 배 흔들림 |
| 표 I–VII (`tab_I.png`–`tab_VII.png` · 손 크롭) | 전처리 반복 수 · 세 문제의 물성 · 격자 · 풀이기 설정 | 단위 시험 입력 그대로 |
| 식 크롭 126 (`eq_001_…`–`eq_126_…`) | 번호 식마다 한 장 (모형 1–12 · 이산화 13–47 · 접촉 48–55 · 안정 56–90 · NK 91–106 · 전처리 107–118 · 걸음 119–123 · 파속 · 무늬 124–126) | 보고서 MPM 절에 붙일 식 |
| 근거 문단 20 (`txt_p*`) | 카드가 인용한 문장 (숫자 · 정의 · 단정의 근거) | 원문 인용용 |

## 6. Post-processing ★
- **원문이 낸 양**: 총 · 탄성 에너지 · x 운동량 시계열 (그림 6 · 10 · 14 · 단위 미인쇄 = g · cm · µs [카드 해석]) · 주응력차 무늬 (식 126 · f_no 미인쇄) · 주응력차 면적 분율 히스토그램 (t > 10 µs · 평균) · 평균 전파 속도 (P파 ≈2.5 × 10³) · 블록 충돌 파속 오차 3 % · 반복 수 (표 I) · 알갱이 위치 그림.
- **안 한 것**: 격자 · 물질점 수렴 · 오차 노름 · 실험 무늬와의 정량 대조 · 압력 · 기공 · 접촉 면적 · 배위수 · CPU 시간.
- **이 카드의 후처리**: 그림 6 · 10 · 14 · 15 를 PDF 벡터 경로에서 읽음 (틀 + 큰 눈금 보정 · '+' 표지 중심 · 꺾은선 꼭짓점 · 구간 중앙값 / 최댓값 · 그림 15 는 세로 · 가로 획 교차로 '+' 를 찾음) → digitized.csv 83 행 · 파속 · Courant · Mach · 물질점 수 · 지름당 칸 · 단위 확인 · 에너지 비 — 전부 [카드 산술] 로 표지.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 가지에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · 다른 카드의 우리 코드 판독 출처를 병기)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 시간 적분 | **암시 θ = ½** (행렬 없는 NK) · 비교 판 = 명시 도약 (α 0.25 · 1.0) | **명시** MLS-MPM (Taichi) · dt = 0.4 dx/√M · 판 Mach 0.01–0.03 (`--platen-mach`) [다른 카드의 우리 코드 판독 · `gritton2017_…` L538 · M 의 뜻 [미확인]] | 우리는 이 논문의 '명시 판' 쪽 · 준정적을 느린 판으로 흉내 |
| 형상 함수 · 셀당 점 | 선형 b-spline · 셀당 최대 4 (2D) | 2차 B-spline (MLS · APIC) [`hu2018_…`] · 방향당 2 (셀당 8) [`homel2017_…` L499 우리 코드 판독] | 유한 격자 불안정 기준 (0.4) · 가장자리 작은 질량 문제는 선형 b-spline 판 — 그대로 옮기지 않는다 [카드 추론] |
| 속도장 | **알갱이마다** (다물체 · 미끄럼 · 분리 · 결합) | SE **한 속도장** · AM = 고정 격자 장애물 (scaffold · v = 0) [우리 · CLAUDE.md] | 우리 SE–SE 는 접촉 규칙 없이 붙어 흐른다 (= no slip · [`bardenhagen2000_…`]) · 후보 A′ 가 이 논문의 꼴 |
| 알갱이 재료 | HMX 근사 µ 7.48 · K(λ) 11.36 GPa (연화 없음) · 전단 J2 σ_y 300 MPa · H 10 MPa | MPM SE: E 1.53 · ν 0.49 → K 25.5 · µ 0.513 GPa (전단만 연화) · σ_y 0.30 GPa (Hencky 문턱 — 일축 압축 0.318 · 인장 0.454 GPa) / DEM: E_eff 1.35 GPa (18 배 연화) [우리 · CLAUDE.md] | 우리 SE 전단 계수는 HMX 의 1/15 · σ_y 는 같은 300 MPa 이지만 정의가 다르다 |
| 하중 | 벽 충돌 100 m/s · 속도 계단 10 m/s · 벽 전단 100 m/s (전부 동역학) | 판 압축 → 300 MPa (hold · servo) · 준정적 흉내 | 이 논문에 준정적 압밀이 없다 — 하중 꼴이 다르다 |
| 비교 기준 | 에너지 · 운동량 장부 · 블록 파속 해석해 · 남의 실험 (정성) | 랩 표준 순수 SE 기공 10–13 % (300 MPa · 진밀도 1.64) · DEM ↔ MPM (frame [4]) [우리 · CLAUDE.md] | 우리 MPM 은 **에너지 장부를 적지 않는다** [카드 추론] — 이 논문의 대조 꼴이 빠진 칸 |
| 차원 | 2D 계산 | 3D (n_grid 192–512) | 3D 비용 · 메모리는 따로 어림 (§7-4) |
| 탈압 | 없음 (충돌 반발만) | MPM 탈압 없음 · DEM 언로딩 키트 | 둘 다 압밀 탈압 없음 |

### 7-2. ★ 랩 기준과 나란히 (판정 없이)
| 출처 | 재료 | 조건 | 진밀도 분모 | 기공 |
|---|---|---|---|---|
| **랩 표준** | LPSCl (순수 SE) | 300 MPa | **1.64 g/cm³** (고정) | **10–13 %** |
| 이 논문 | HMX 근사 · 광탄성 원판 (2D) | 동역학 (충돌 · 응력파 · 전단) | 해당 없음 | **해당 없음** (전단 침대 면적 분율 0.797 [카드 산술] 은 처음 배치 · 2D) |
| 우리 DEM 순수 SE | LPSCl · E_eff 1.35 GPa (18 배 연화) · Heckel P_y 138 MPa | 300 MPa · 가압 중 | 구 부피 합 | ε_union ≈10 % · 겹침 11–12 % [우리 · CLAUDE.md 2026-06-06] |
| 우리 MPM 순수 SE | LPSCl · E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 | 300 MPa · 가압 중 | MPM 관례 | 10.0 % — 보정 표적 · 외부 앵커 아님 (`CL-94`) |
- 이 논문은 이 표에 **값을 넣지 못한다** — 주는 것은 수치가 아니라 **방법 · 규칙 · 함정** (§7-3 – §7-5 · §8).

### 7-3. ★ 같은 Mach 대의 명시 도약 — 에너지 장부 경고 [카드 산술 · 카드 추론]
- 이 논문 탄성 알갱이: U₀/s = **0.030** (식 121 그대로) — 우리 판 Mach 0.01–0.03 [우리 · CLAUDE.md] 와 **같은 자릿수**.  그 조건에서 명시 도약 (α 0.25 · 선형 b-spline) 의 총에너지가 2 µs (벽 충돌 ≈5 번 [판독]) 에 **×14.5** · 탄성 에너지 · 거짓 운동량이 충돌마다 쌓였다 [판독 그림 6].
- 유한 격자 불안정 기준 U₀/√(λ/ρ) < 0.4: 우리 SE (ν 0.49 → √(λ/ρ) ≈ 0.98 c_P) 의 물질 속도는 판 속도 이하 → 비 ≈ 0.01–0.03 = 이 기준으로는 **불안정 구간** [카드 산술].  ⚠ 기준은 선형 b-spline · 1D 빔 · FLIP 꼴 분석이다 — 우리 2차 B-spline · APIC/MLS 에서 같은 일이 있는지는 이 원문이 말하지 않는다 → **측정 항목** (우리 코드의 운동 + 탄성 + 소성 소산 + 판 일 장부).
- 우리 CLAUDE.md 의 Mach 사다리 (real_14 Mach 0.0306 → 0.01: σ +4.8 % · Lee 침대 0.03 → 0.01: 정착/목표 +9.0 %) 를 '관성' 으로 읽기 전에, 이 논문의 장부 (식 85 의 항별) 로 **수치 에너지 증가 · 거짓 잔류 응력 몫** 을 먼저 잰다 — 이 논문에서 명시 판은 같은 문제의 평균 주응력차를 **1.8 배** 키웠다 (그림 15).

### 7-4. ★ 알갱이별 장의 3D 저장 — 우리 크기 어림 [카드 산술 · 우리 값 = CLAUDE.md]
- 이 논문의 미지수 = **알갱이별 노드 목록** (알갱이가 닿는 노드만) — 알갱이 수 × 전체 격자가 아니다.
- real_14 (SE 32,832 개 · 지름 1 µm · n_grid 384 · dx 0.141 µm [우리 · CLAUDE.md]): 지름 = 7.09 칸 → 2차 B-spline 지지 (반경 1.5 칸) 를 더한 구 반경 5.05 칸 → 알갱이당 노드 ≈ **540** (선형 b-spline 이면 반경 4.55 칸 → ≈ 394) → 미지수 32,832 × 540 × 3 = **5.3 × 10⁷** (선형 3.9 × 10⁷).  GMRES (Krylov 10 + 작업 3 벡터 · 8 B) ≈ **5.5 GB** (선형 · Krylov 5 이면 ≈ 2.5 GB) → GPU 32–48 GB 에 들어간다.  비교: 강성 행렬 갈래 (Guilkey) = 3D 단일 장 1.7 × 10⁸ 자유도에서 행렬만 ≈165–760 GB [다른 카드 · `guilkey2003_…` §7-3].
- 대각 전처리 비용: 2D 선형 '18 번' → 3D 2차 B-spline 묶음 탐침이면 **375 번** 의 잔차 계산 (D 를 얼마나 자주 다시 구했는지 [미확인]).
- ⚠ *"no more than two grains are in contact at any given time"* — 3D 조밀 SE 충전에서는 세 알갱이 이상이 한 노드를 나누는 곳 (삼중 접점) 이 생긴다 · 식 (7) ≡ (8) 이 깨진다 [카드 추론] → A′ 설계의 첫 검사 항목.
- ⚠ 알갱이마다 장을 두는 대신 장 수를 늘리지 않는 갈래 = [`homel2017_…`] (손상장 기울기로 노드마다 두 장).

### 7-5. ★ 걸음 규칙을 우리 SE 로 옮기면 [카드 산술]
- **1 % 규칙의 뜻** = µ × Δε ≈ 0.25 σ_y (HMX: 7.48 GPa × 1 % = 74.8 MPa ≈ 0.249 × 300 MPa).  우리 MPM SE (µ 0.513 GPa · σ_y 0.30 GPa): µ × 1 % = 5.1 MPa = **0.017 σ_y** · 0.25 σ_y 에 해당하는 걸음 변형 = **14.6 %** → 우리 연화 SE 에는 1 % 가 정확도 근거로 너무 엄하다 — 원문도 *"will need to alter"*.
- **조건수 벽 10 Δt_exp** = P파 Courant 2.5 (α 0.25 라 읽을 때) ↔ 우리 명시 Courant 0.4 (M = P파 계수라면 · [미확인]) → 암시 최대 걸음 ≈ 우리 걸음의 **6.25 배**.  우리 판 압축의 걸음당 전체 변형 ≈ Mach × C × dx/H = 0.03 × 0.4 × 0.141/30.3 = **5.6 × 10⁻⁵** (real_14 · n_grid 384) → 1 % 규칙보다 조건수 벽이 먼저 묶는다.
- **걸음당 비용 감각** (잔차 1 회 ≈ 명시 1 걸음 · 표 I 한 층 = Newton 당 선형 3.9 · Krylov 벡터마다 WJ 2 번): Newton 1 회 ≈ 1 + 3.9 × 3 ≈ 13 잔차 (+ 대각) → 암시 1 걸음 (Newton 1–5 회) ≈ 13–64 잔차 ↔ 같은 시간 명시 ≈ 6 걸음 → **2–10 배 비쌈** [카드 산술 · 가정 다수].  ⇒ 우리 Mach 에서 '암시로 바꾸면 빨라진다' 는 이 논문 자료로 서지 않는다 · 값을 하는 자리 = **에너지 보존 · 유한 격자 불안정 제거 · 거짓 잔류 응력 제거** (정확도) 쪽.

### 7-6. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: MPM (역학) 쪽 다물체 입상체 계산의 **풀이 방법** (암시 · 행렬 없는 NK) · 수치 안정 이론 · 접촉 규칙 (미끄럼 · 분리 · 결합) · 에너지 장부.
- **없는 것**: 수송 (접촉망 · 복셀 σ) · 압밀 · 기공 · 하중 몫 · 실험 정량 대조 · 3D.  ⇒ 후보 A′ (입자마다 속도장) 의 **풀이기 · 접촉 설계서** 한 권.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = HMX 근사 · 광탄성 원판 · 2D · 동역학.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ① **접촉 거리 ∝ Δx**: 부피 가중이면 알갱이가 **한 셀** 떨어질 때 힘 0 (p.515) · 접촉 표현이 격자 간격과 자기 닮음 (p.530) → 알갱이마다 장을 두는 MPM 에서 물질점으로 센 기공에는 **해상도 몫 (≤ Δx 틈)** 이 섞인다 — 우리 dx 0.141 µm = SE 지름의 **14 %** [카드 산술] → 연산자 등록에 '접촉 알고리즘 판 · dx' 칸 ② 같은 물질점 배치라도 접촉 규칙 (부피 가중 유무) 이 **효과 알갱이 크기 · 충전 밀도** 를 바꿨다 (전단: 무질서 35 µs ↔ 40 µs 에 1/3 질서 · *"denser row packing"*) → '접촉 규칙 바꿈' 은 결과 전 대조 축 | 기공 · 밀도 값 없음 · 2D |
| **단계 1** (3D 메모리 · 장 수) | ★ 미지수 = **알갱이별 노드 목록** 을 이어 붙인 한 벡터 (식 91–95) → 우리 real_14 어림 5.3 × 10⁷ (2차 B-spline) · GMRES ≈5.5 GB [카드 산술 · §7-4] · 행렬 없음 → 강성 행렬 (≈165–760 GB · `guilkey2003_…`) 의 벽을 피함 · 대각 전처리 2D '18 번' → 3D 375 번 · ⚠ 한 노드 두 알갱이 가정 (3D 조밀 충전에서 깨짐) | 3D 계산 · 실측 메모리 · 시간 없음 |
| **단계 2** (2D MPM 코드 · 단위 시험) | ★ **표 II 탄성 알갱이 벽 충돌 = 2D 단위 시험 후보** (17 × 17 · Δx 8.118 µm · R 50 µm · U₀ −100 m/s (Mach 0.030) · K(λ) 11.36 · µ 7.48 GPa · ρ 1900 · 셀당 4 · 2 µs) → 우리 명시 코드의 총 · 탄성 에너지 · x 운동량 시계열을 그림 6 (명시 ×14.5 · 암시 처음→끝 +16 % [판독] · 첫 접촉 t ≈ 0.24 µs) 과 견줌 · **직사각 블록 충돌 파속** (해석해 대비 3 %) = 파속 단위 시험 · 식 (85) 의 항별 에너지 장부 = 코드 QC | 블록 시험의 크기 · 조건 미인쇄 · 평면변형률/응력 [미확인] · 소성 없는 탄성 |
| **단계 3** (2D 접촉 표현 비교) | ★ 이 논문 자체가 **접촉 표현 둘 (부피 가중 유무) 의 같은 문제 대조** — 무질서 시작 · 충전 밀도가 바뀜 (35 µs · 284 % ↔ 40 µs · 330 % 에 1/3 질서) · 시간 적분 둘 (명시 · 암시) 의 응력 통계 1.8 배 차 → 우리 단계 3 (한 속도장 ↔ 입자별 장) 에 '접촉 규칙 판 · 시간 적분' 을 고정 변수로 적어야 함 | **한 속도장 ↔ 입자별 장** 대조 없음 · 누르는 힘 비교 없음 |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 걸음 규칙 (µ·Δε ≤ 0.25 σ_y → 우리 SE 14.6 %) · J2 상한 검사 (평면변형률 최대 주응력차 = 2/√3 σ_y · HMX 346 MPa) — 우리 σ_y 는 Hencky 문턱이라 우리 코드의 실제 항복면으로 다시 계산해 상한 검사에 쓴다 | 순수 SE · 기공 · 실험 앵커 · 3D 없음 |
| **단계 5** (3D 복합 압밀) | 없음 — 단단한 + 무른 섞임 · 하중 몫 없음 · 앞 연구 [39] (정적 재하 → 응력 다리 · 단단한 결합재 → 응력 손가락 억제) 의 인용만 | — |
| **단계 6** (탈압 · 되돌아옴) | ★ 벽 충돌 뒤 반발에서 **명시 판이 거짓 잔류 응력 · 운동량을 남김** (탄성 에너지 충돌마다 쌓임 · 그림 6 · 14) ↔ 암시는 ≈1/100 (원문) → 우리 탈압 계산에서 '되돌아온 뒤 남는 응력' 을 물리로 읽기 전에 에너지 장부로 수치 몫을 뺀다 [카드 추론] · 자유 분리 (식 7) · 떨어짐 (식 12) = 탈압 접촉 규칙 | 압밀 탈압 · 잔류 변형 정량 없음 |
| **단계 7** (형상 · 피복 · 수송) | 주응력차 지도 · 히스토그램 (응력 사슬) — 시간 적분 방식에 평균이 1.8 배 흔들림 (그림 15) → MPM 응력 사슬 통계를 우리 결과로 낼 때 방식 표지 필수 | 피복 · 접촉 면적 · 수송 없음 |
| **후보 D0** (지금 DEM) | 없음 — DEM 힘 법칙 (hard core · Hertz–Mindlin) 을 이름으로만 · 알갱이 변형을 푸는 모형과 대조 (§4-4) | 수치 없음 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | ★ *"Imposed strain boundary conditions are imposed through the contact force by specifying v on the boundary"* (p.509) — 벽 = 질량중심 속도를 지정한 같은 침투 금지 · 마찰 · 분리 규칙 · 전단에서는 알갱이를 움직이는 벽에 '붙임' (결합) → 우리 판 (`k·dx > wall_z` 노드의 법선 속도를 양방향으로 처방 = **분리 없음** · 접선 자유 · 마찰 없음) · AM 마스크 (v = 0 · 붙음) [다른 카드 · `hu2018_…` L515–L516 의 우리 코드 판독] 를 '떨어질 수 있는 · 마찰 있는 벽' 으로 바꾸는 식 그대로 | 판 반력 · 미끄럼 값 없음 |
| **후보 A** (MPM 강체 AM + SE 한 속도장) | 없음 (강체 물체 없음) — 벽 규칙을 강체 AM 에 넓히는 길은 원문 밖 [카드 추론] | — |
| **후보 A′** (입자마다 속도장 · 다물체 마찰 접촉) | ★ **이 후보의 암시 판 설계서**: 식 (7)–(12) · (48)–(55) · 알갱이별 잔차 목록 · 행렬 없는 NK (허용치 10⁻⁶ · ε 10⁻³ · γ 10⁻³ · Newton 5–20 · Krylov 5–10 · WJ w 0.67 × 2) · 질량 가중 잔차 (가장자리 작은 질량) · 에너지 성질 (법선 접촉 일 0 · 마찰 · 소성 · 몰아주기 ≤ 0) · 함정 넷 (한 노드 두 알갱이 · 공통 법선 가정 — [38] 은 *"not along a common normal … small errors in momentum conservation"* [다른 카드 · `bardenhagen2000_…` L182] · 접촉 거리 ∝ Δx · 여러 층 전처리 무익) · 걸음 벽 (≤ 10 Δt_exp · < 1 %) | 2D · ≤ 370 알갱이 · 동역학 · 압밀 · 비용 숫자 없음 |
| **후보 B** (입자마다 FE + 접촉 · NSCD) | 대안 지도만: Euler 쪽 (혼합 이론 · 변형률 또는 응력 연속 가정 [46]) · Benson [12] 암시 Euler (준-Newton) · 입자 수준 분말 압밀 [44 Williamson 1990] · 구리 분말 충격 압밀 [45 Benson 외 1994] · contact dynamics = 강체 · 비국소 (p.506) | 계산 · 비교 없음 (정본 카드 없음 · 정독 n) |
| **후보 C · C′** (MDR · 항복 캡 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀) | 없음 | — |
| **U0–U6** | **U0** — 알갱이 하나면 접촉 힘 0 (질량중심 속도 = 알갱이 속도) · 명시 판은 **단순 이류 중에도** 에너지가 늘었다 (유한 격자 불안정) → U0 에 '접촉 없는 이류의 에너지 불변' 을 넣는다 · **U1** — 탄성 알갱이 벽 충돌 (지름 12.3 칸) + 블록 파속 3 % · **U4** — 자유 분리 · 떨어짐 규칙 (식 7 · 12) · **U5** — 원판 5 개 응력파 (지름 32 칸 · P파 측정 2.5 × 10³ ↔ 설정 2.133 × 10³) · 370 알갱이 전단 (지름 8 칸) · 그림 6 · 10 · 14 에너지 · **U2** — Coulomb µ′ 상한 식 (54) (경사면 시험 자체는 없음) | U3 (단단한 구 → 소성 블록 누르고 떼기) · U6 (조밀 충전 해상도 수렴) 없음 |
| **R1–R7** | **R2** (미끄럼 · 분리) — Coulomb + 자유 분리 + 결합/떨어짐 (식 7–12 · 52–54) · **R3** (SE 입자 경계 기억) — 알갱이마다 장 = 알갱이 정체성 · 소성 변형 이력을 물질점이 실음 (p.507) · **R4** (탈압) — 반발의 거짓 잔류 응력 (명시) · **R5** (맞추는 값 하나) — 원판 λ · µ 는 실험 파속 두 값에서 (맞춤 아님) · 명시 [50] 은 *"some calibration was required"* · **R6** (형상 변형) — 탄소성 알갱이가 전단에서 찌그러짐 (그림 12 · 13 · 정량 없음) · **R7** (파괴) — *"will easily accommodate … grain fracture"* (하지 않음) | R1 (하중 몫) 없음 |
| **결과 전 대조 항목** | ① 탄성 알갱이 (표 II · 2D): 명시 α 0.25 총에너지 **×14.5 / 2 µs** · 암시 처음→끝 **+16 %** (원문 '≈7 %') · 첫 접촉 t ≈ 0.24 µs · 운동량 판 1.41 × 10⁻⁶ [판독] ② 원판 5 개: 암시 에너지 **1 % 안** (판독 −0.56 %) · 명시 +7.9 % · P파 ≈2.5 × 10³ m/s ③ 전단: 평균 주응력차 **25.55 ↔ 46.02 MPa** · 상한 346 MPa · 무질서 시점 — 전부 2D · HMX · 맞추는 데 쓰지 않음 | 우리 재료 · 압밀 양과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: HMX 근사 (µ 7.48 GPa · 연화 없음) · 광탄성 원판 ↔ 우리 LPSCl (MPM µ 0.513 GPa · DEM 18 배 연화) · NCM · 2D ↔ 3D · 동역학 (충돌 · 응력파 · 전단 330 %) ↔ 판 압축 300 MPa · 한 재료 ↔ AM + SE · 탈압 없음.

## 9. 적용 인사이트 (행동)
1. **에너지 장부를 우리 MPM 산출물에 넣는다 (단계 2 · U0 · U5)** — 운동 + 탄성 (+ 소성 소산 · 판 일) 의 시계열과 식 (85) 꼴의 항별 분해.  첫 시험 = 표 II 탄성 알갱이 벽 충돌 (Mach 0.030 = 우리 판 Mach 대) — 그림 6 의 명시 ×14.5 · 암시 +16 % 를 결과 전 기준선으로.  접촉 없는 이류에서도 에너지가 늘면 유한 격자 불안정 쪽.
2. **Mach 사다리의 σ 변화를 '관성' 으로 부르기 전에 수치 몫을 잰다 (단계 4 · 단계 6)** — 이 논문에서 같은 Mach 대의 명시 도약이 거짓 잔류 응력으로 평균 주응력차를 1.8 배 키웠다 (그림 15).  우리 real_14 σ +4.8 % · Lee 침대 +9 % (CLAUDE.md) 에 장부를 붙인다.
3. **후보 A′ 를 고르면 이 논문을 풀이기 설계서로 (단계 1 · 3)** — 알갱이별 노드 목록 · 행렬 없는 NK · 질량 가중 잔차 · WJ 한 층 (여러 층은 이득 없음) · 3D 메모리 ≈5 GB 어림 (§7-4) · 첫 검사 = 한 노드 세 알갱이 이상 빈도 · 공통 법선 오차 · 접촉 시작 거리 (÷ dx).
4. **걸음 규칙은 재료로 다시 정한다** — '변형 1 %' 는 HMX 의 µ·Δε ≈ 0.25 σ_y · 우리 연화 SE 면 14.6 % 에 해당 · 암시를 쓰면 조건수 벽 (≤ 10 Δt_exp ≈ 우리 걸음의 6 배) 이 먼저 묶는다 → 암시의 이득은 속도가 아니라 정확도 (§7-5).
5. **판을 '떨어질 수 있는 벽' 으로 (후보 A′-0 · 단계 6)** — 벽 = v 지정 접촉 제약 (침투 금지 · 마찰 · 자유 분리) — 탈압에서 판이 침대에서 떨어지는 순간을 계산할 수 있다.
6. **접촉 규칙 · 시간 적분을 결과 표의 고정 칸으로 (단계 0 · 3 · 7)** — 같은 배치에서 부피 가중 하나로 충전 밀도 · 무질서 시점이, 시간 적분 하나로 응력 통계가 바뀌었다.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In a multi-velocity-field material point method for deformable grains, an implicit (θ = ½) Newton–Krylov formulation is stable in the L2 norm independent of the time step, whereas the explicit leapfrog scheme is not; in a 2D elastic-grain wall-impact test the explicit total energy grew by an order of magnitude (×14.5 in 2 µs, read from the figure) while the implicit variation stayed ≈7% (Cummins & Brackbill, *J. Comput. Phys.* 180 (2002) 506–548)."
- "The implicit linear systems became poorly conditioned beyond ten explicit time steps, and preconditioning did not enlarge the radius of convergence; the time step was also limited to <1% strain per step so that the stress stays near the yield surface (Cummins & Brackbill, 2002)."
- 국문 (한정어와 함께): *"입상체를 알갱이마다 속도장을 둔 MPM 으로 풀 때, 명시 도약은 같은 Mach 대 (≈0.03) 에서도 충돌마다 거짓 탄성 에너지 · 잔류 응력을 쌓고 (2D 탄성 알갱이 2 µs 에 총에너지 ×14.5 [판독]) 암시 θ = ½ 판은 이를 없앤다 — 단 이 결과는 2D · HMX 근사 · 동역학이고 준정적 압밀 · 계산 비용은 다루지 않았다 (Cummins & Brackbill 2002)."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
**원문이 스스로 적은 한계**: 조건수 벽의 원인 미상 · 여러 층 전처리 이득 없음 · FLIP 내부력 판의 가장자리 전단 오차 · 걸음이 항복 정확도에 묶임 · 한 노드 두 알갱이 가정 (§0 ⑪).
**카드가 본 한계**
1. **준정적이 없다** — 동기는 준정적 (p.507) 인데 예 셋 모두 동역학 · '암시가 준정적에 효율적' 은 이 논문 안에서 재지 않은 주장 (*"potentially more efficient [12]"*).
2. **비용이 없다** — CPU · 걸음 수 · 기계가 없어 암시 ↔ 명시 손익을 이 논문으로 셀 수 없다 (표 I 반복 수뿐 · 그것도 64 × 64 · 걸음 수 미인쇄).
3. **2D · 작은 규모** — ≤ 370 알갱이 · 지름 8–32 칸 · 격자 수렴 없음.
4. **접촉 1 차 정확 + 효과 크기 변화** — 부피 가중은 정확도를 높였다고 하지만 알갱이를 '작게' 만들어 충전 밀도 · 결과를 바꿨다 (원문 인정) · 어느 쪽이 물리에 가까운지 실험 대조 없음.
5. **에너지 주장의 판독 · 표현 차** — '≈7 %' (판독 처음→끝 +16 %) · '두 자릿수' (판독 ≈35 배) · '≈two orders' (판독 ≈44 배) — 방향은 같고 크기 표현이 느슨하다.
6. **물성 표기 어긋남** — 표 VI λ 1.136 × 10⁸ ↔ 표 II 11.36 × 10⁹ · λ 를 'Bulk modulus' 로 부르면서 식은 K 꼴 (뜻 [미확인]) · 이름 없는 'ν 0.3' (마찰 계수로 읽힘) · 그림 11 단위 (§3-11).
7. **측정 P파 +17 %** 를 설명하지 않았다.
8. **전이 한계**: HMX (폭약 결정) · 광탄성 고분자 · 2D · 동역학 · 한 재료 — LPSCl · NCM · 3D · 준정적 압밀로 값을 옮기지 않는다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| [39] | S. G. Bardenhagen and J. U. Brackbill, Dynamic stress bridging in granular material, J. Appl. Phys. 83, 5732 (1998). | ★ 입상체 MPM 의 **정적 · 동적 압축** (다분산 응력 다리 · 결합재) — '가루 침대 압축 MPM 선례' 의 실제 후보 · 정본 카드 없음 (wishlist L278) |
| [13] | W. L. Elban and M. A. Chiarito, Quasi-static compaction study of coarse HMX explosive, Powder Tech. 46, 191 (1986). | 이 논문이 동기로 든 **준정적 압밀 실험** (*"nonlinear stiffening"*) — 카드 없음 |
| [44] | R. L. Williamson, Parametric studies of dynamic powder consolidation using a particle-level numerical model, J. Appl. Phys. 68, 1287 (1990). | 알갱이를 변형체로 푼 분말 압밀 계산의 이른 선례 (*"resolve grain scale lengths, allow grains to deform"*) — 카드 없음 |
| [45] | D. J. Benson, W. Tong, and G. Ravichandran, An analysis by direct numerical simulation of the effects of particle morphology on the shock compaction of copper powder, Model. Sim. Mat. Sci. Eng. 2, 535 (1994). | Euler 쪽 입자 수준 분말 압밀 (입자 형상 효과) — 후보 B 계열 · 카드 없음 |
| [12] | David J. Benson, An implicit multi-material Eulerian formulation, Int. J. Numer. Meth. Eng. 48, 475 (2000). | 준정적 입상체에 암시가 낫다는 근거 · 혼합 이론 + 준-Newton — 카드 없음 |
| [46] | D. J. Benson, A mixture theory for contact in multi-material Eulerian formulations, Comput. Meth. Appl. Mech. Eng. 140, 59 (1997). | Euler 접촉 (변형률 / 응력 연속 가정) — 카드 없음 |
| [37] | S. G. Bardenhagen, J. U. Brackbill, and D. Sulsky, Numerical study of stress distribution in sheared granular material in two dimensions, Phys. Rev. E 62, 3882 (2000). | 전단 예의 원 문제 (부피 가중 없는 명시) — wishlist L197 |
| [34] | J. U. Brackbill, The ringing instability in particle-in-cell calculations of low-speed flow, J. Comput. Phys. 75, 469 (1988). | 유한 격자 불안정의 원전 — wishlist L193 |
| [8] · [1] · [32] | Sulsky 외 1995 · 1994 · 1996 | MPM 원전 · 반경 귀환 — wishlist L195 · 후보 표 N-40 · wishlist L196 |
| [38] · [50] · [55] | Bardenhagen 외 2000 (CMAME 187) · Bardenhagen 외 'private communication' · Guilkey & Weiss 2001 (MIT 학회) | 정본 `bardenhagen2000_…` · `bardenhagen2001_…` (출판본) · `guilkey2003_…` (같은 방법의 2003 저널 판) |
| [49] | H. P. Rossmanith and A. Shukla, Photoelastic investigation of dynamic load transfer in granular media, Acta Mech. 42, 211 (1982). | 원판 응력파 실험 원전 (U5 실험 대조) — 카드 없음 |

## 13. [미확인] 목록 (본문 43 쪽 전수에 없음)
1. CPU · 벽시계 시간 · 메모리 · 기계 · 코드 언어 · 걸음 수 (세 예 모두).
2. 2D 가 평면변형률인지 평면응력인지.
3. 코드 안 λ 의 뜻 (체적계수 ↔ 라메 상수) · 표 VI λ 의 바른 값.
4. 전단 예의 마찰 계수 (표 VI 의 이름 없는 'ν 0.3' 이 그것인지) · 원판 예의 마찰 유무 · σ_bond 값.
5. 무늬 식 (126) 의 f_no.
6. 직사각 블록 충돌 시험의 크기 · 격자 · 물성.
7. '임계 밀도' (critical density) 의 정의 · 값.
8. 평균 전단 변형의 기준 길이.
9. 측정 P파 +17 % 의 원인.
10. 3D 판 · 2D → 3D 전이 · 한 노드 세 알갱이 이상 처리.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 본문 43 쪽 글자 층 전수 추출 + 식 126 개 · 표 7 개 · 그림 15 개 · 근거 문단 20 개 렌더로 읽음.  서지 = 첫 쪽 (학술지 · 권 · 쪽 · DOI · 제목 · 저자 · 소속 · 접수일) · p.546 감사 (W-7405-ENG-36).  원문 낱말 (본문): DEM 2 회 (p.506 *"distinct element method (DEM) [3]"* · p.507 힘 법칙) · quasi-static 1 회 (p.507 동기 · 참고 [13] 제목에 1 회 더) · compaction 1 회 (p.507 [39] 인용 문장 · 참고 제목 둘) · unload · springback · porosity · CPU 0 회 · 3D · three-dimensional 0 회 (참고 [47] 제목뿐).
- 크롭 **168 장** = 그림 15 (도구 13 + 손 2 — 그림 3 · 11 은 글자 + 선 몇 개라 도구가 뺌) · 표 7 (로마 숫자 번호라 도구 정규식 밖 → 전부 손) · 식 126 (번호마다 한 장 · 400 dpi · **다시 자름 19** = 앞 문단 끝줄 15 · 이웃 줄 글자 4) · 근거 문단 20 (300 dpi · **다시 자름 13** = 이웃 줄과의 여백을 틈의 절반으로 · 그중 2 장은 이웃 줄에 닿았던 것).  168 장 전부 Read 로 열어 확인 (식 · 문단은 쌓은 확인 판으로).  `figures.json` 의 `manual_crop` · `note_manual`.
- 판독: digitized.csv 83 행 — 그림 6 (세 판) · 10 · 14 (두 판) · 15 를 PDF 그리기 명령에서 (축 = 틀 + 큰 눈금 최소 제곱 · '+' 표지 = 2.4 pt 세로 획 중점 · 꺾은선 = 꼭짓점 · 구간 중앙값 / 최댓값 · 그림 10 명시와 그림 6 탄성 에너지 봉우리는 600 dpi 래스터 맨 위 잉크 · 그림 15 는 세로 · 가로 획 교차로 '+' 를 찾고 꺾은선은 표지에서 1.45 pt 밖 꼭짓점만).  단위 확인: 처음 운동 에너지 7.46 × 10⁻⁹ ↔ 판독 7.33 × 10⁻⁹ (§3-8).
- 2 차 인용 대조: 정본 `bardenhagen2005_…` (L53 · L253 · L299 · L519) · `guilkey2003_…` (L127 · L274 · L350) — 고치지 않았다 (정독 출력 batch_80 의 "카드 문제" 절).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 + DOI (`jcph.2002.7101`) · 제목 낱말 (*"implicit particle-in-cell method for granular"*) · 저자 (Cummins) grep — 카드 없음 (인용만: `bardenhagen2005_…` · `guilkey2003_…` · `yano2023_…` / `yano2024_…` 의 Thornton–Cummins–Cleary 2017 은 다른 논문) (2026-11-12).

## 🔗 관련 카드
- 같은 자리 (명시를 천천히 돌리는 것의 대안 · 암시 MPM): `guilkey2003_implicit_mpm_newton_quasistatic_fem_comparison` (강성 행렬 + 일관 접선 · 이 논문 ref [55] 의 저널 판) · 가리킨 카드 `bardenhagen2005_mpm_foam_densification_simulation`.
- 다물체 접촉 원전 · 같은 문제: `bardenhagen2000_mpm_granular_multibody_frictional_contact` (ref [38]) · `bardenhagen2001_mpm_improved_contact_granular_stress_waves` (ref [50] · 광탄성 원판).
- 입자별 장 MPM 으로 실제 압밀: `nezamabadi2022_mpm_cd_plastic_particle_compaction` · `nguyen2017_mpm_bpm_deformable_particle_compaction` · 장 수를 늘리지 않는 갈래 `homel2017_mpm_field_gradient_partitioning_fracture_self_contact`.
- 명시 MPM 의 오차 · 안정: `bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing` · `steffen2008_mpm_implementation_choices_gimp_bspline_boundary` · `steffen2010_mpm_space_time_error_balance_moving_mesh` · `sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability`.
- 우리 MPM 계보 · 리뷰: `hu2018_mls_mpm_cpic_two_way_rigid_coupling` · `stomakhin2013_mpm_snow_elastoplastic` · `devaucorbeil2020_mpm_after_25_years_review`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
