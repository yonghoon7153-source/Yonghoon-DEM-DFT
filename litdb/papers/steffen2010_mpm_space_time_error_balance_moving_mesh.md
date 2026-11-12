<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 후보 표 N-37 · 정독 78 · 11-12 대피 세션이 본 세션에서 넘겨받은 1 순위 후보) 에서 꼭 뽑으라고 한 항목.
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 상자 · §0-1 고른 의도 대조 · §8 자세한 분석) · steffen2008_mpm_implementation_choices_gimp_bspline_boundary.md (같은 Utah 무리 · 같은 1D 주기 막대 제조해 · MPM 수치 카드의 꼴 · 우리 MPM 값의 [다른 카드] 출처).
     원문 = 출판본 (Int. J. Numer. Meth. Engng 2010; 82:1207–1243 · 37 쪽 · SI 없음).
     쪽 표기 = "p.NNNN" 은 학술지 인쇄 쪽 (1207–1243).  크롭 파일 이름의 pN 과 figures.json 의 page 는 PDF 쪽 = 인쇄 쪽 − 1206.
     값 표지: [인쇄] = 본문 · 식 · 표 · 캡션에 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 250 행 — 그림이 PDF 벡터라 화소가 아니라 그리기 명령의 경로 좌표에서 읽었다:
     틀 사각형 모서리 ↔ 틀 끝에 인쇄된 축 한계 (로그 축은 자릿수에 선형) · 표지 중심 (+ · x = 짧은 두 획 · o = 곡선 넷의 닫힌 고리 · 시작 · 끝 이어짐으로 묶음) · 범례 상자 제외 · 그림 12 가로축은 눈금 9 개로 보정) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [카드 추론] = 우리 계획으로 옮긴 추론 · [다른 카드] = 정본의 다른 카드에 적힌 값 (slug · 줄) ·
     [우리 기록] = 우리 쪽 값 (CLAUDE.md · comparison_vs_ours_DEM.md) · [미확인] = 원문 37 쪽 전수에 없음.
     원문 37 쪽은 글자 층 추출 + 전 쪽 렌더로 전부 읽었다 (식 (1)–(138) 은 수식 글꼴이라 렌더에서 옮겼다).  DEM · 접촉 · 소성 · 압밀 · 알갱이 계산은 없다 — 1D 탄성 MPM 의 수치 오차 분석 + 수치 시연. -->
# MPM 의 공간 · 시간 오차를 떼어 내 균형 맞추기 — moving-mesh MPM (참조 배치 고정 · 격자 넘김 없음) 으로 시간 오차를 드러내고, 격자 넘김의 시간 도약 오차 O(Δt²) · 노드 적분 (quadrature) 오차의 누적 (전역 ∝ α^k · α = 1/셀당 물질점 · 선형 기저 k = 1 · 2차 B-spline k = 2 · Δt 와 무관한 바닥) · 한 걸음 국소 절단 오차로 상수 c₁ · c₂ 를 재어 균형 시간 간격 Δt = C·h (2 차 공간 오차) / C·√h (선형 기저 standard MPM) 를 예측 — 1D 주기 탄성 막대 제조해 · 균형 Δt 가 안정 한계 (CFL 1) 위라 '시간 0 차 수렴' 이 설명된다 — Steffen · Kirby · Berzins (Int. J. Numer. Meth. Engng 2010)

> slug `steffen2010_mpm_space_time_error_balance_moving_mesh` · DOI `10.1002/nme.2787` · type `MPM numerical error analysis (1D · explicit Forward-Euler / staggered centered difference · piecewise-linear vs quadratic B-spline (open knot vector) · standard (grid reset each step) vs moving-mesh (fully Lagrangian, reference configuration) MPM · simplified non-physical problems (fixed piecewise-linear velocity field · discontinuous integrand g(x)) + 1D periodic neo-Hookean bar manufactured solution · single-step local truncation errors — 알갱이 · 접촉 · 소성 · 압밀 · 2D/3D 계산 없음)` · PDF `f66711ce-37._Decoupling_and_balancing_of_space_and_time_errors_in_the_material_point_method_MPM.pdf` · SI 없음 · digested `2026-11-12` · status ✅
>
> **저자**: **Michael Steffen** · **Robert M. Kirby\*** · **Martin Berzins** — School of Computing and Scientific Computing and Imaging Institute, University of Utah, Salt Lake City, UT 84112, U.S.A. — \* 교신 (kirby@cs.utah.edu) · *Int. J. Numer. Meth. Engng* **2010**; **82**:1207–1243 (37 쪽 · 호 = 10 — 쪽 옆 내려받기 배너 "10970207, 2010, 10" 에서만 읽힘 · 첫 쪽 머리에는 호 없음) · 접수 2009-07-10 · 수정 2009-09-27 · 수락 2009-09-30 · 온라인 2009-12-09 (Wiley InterScience) · 키워드 *material point method; meshfree methods; meshless methods; particle methods; smoothed particle hydrodynamics; quadrature; time stepping; nodal quadrature* · 연구비 = U.S. DOE C-SAFE (W-7405-ENG-48) · 감사 = Utah MPM Group (Guilkey · Wallstedt · Brannon).
> **이웃 카드 (링크만)**: [`gritton2017_mpm_chemomechanical_coupling_silicon_anode`](gritton2017_mpm_chemomechanical_coupling_silicon_anode.md) (가리킨 카드 · 이 논문 = 그 ref. [36] · L91 의 "[32–37]" 묶음) · [`steffen2008_mpm_implementation_choices_gimp_bspline_boundary`](steffen2008_mpm_implementation_choices_gimp_bspline_boundary.md) (같은 무리의 앞 논문 = 이 논문 ref. [12] · 같은 1D 주기 막대 제조해 · 후보 표 N-36) · [`guilkey2003_implicit_mpm_newton_quasistatic_fem_comparison`](guilkey2003_implicit_mpm_newton_quasistatic_fem_comparison.md) (ref. [21] · 암시 MPM) · [`bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing`](bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing.md) (ref. [10] · GIMP) · [`hu2018_mls_mpm_cpic_two_way_rigid_coupling`](hu2018_mls_mpm_cpic_two_way_rigid_coupling.md) (우리 MLS-MPM · 2차 B-spline 의 원전) · [`sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability`](sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability.md) (Δt = 0.4h/C · MMS 노름 함정) · [`bardenhagen2005_mpm_foam_densification_simulation`](bardenhagen2005_mpm_foam_densification_simulation.md) (⚠ 이 논문 ref. [3] Brydon 외 2005 와 **다른 논문** · 같은 학술지 같은 권 53).
> **판독 원자료**: `litdb/figures/steffen2010_mpm_space_time_error_balance_moving_mesh/digitized.csv` (250 행 — 그림 5 점 · 6a/6b 도약 앞뒤 · 9a/9b 끝값 · 11 최대 · 계단 · 12 도약 앞뒤 + B-spline + 정해 (실선 · 3 차 Bézier 4 조각) · 13a/13b 전 점 · 14–19 전 점 + 기준선 끝점) · 그림 크롭 **179 장** (도구 17 중 다시 자름 10 + 그대로 7 · 손 크롭 162 = 그림 2 (Fig. 2 · 6) · 표 2 (I · II) · 식 138 (식 번호마다 하나 · 400 dpi) · 근거 문단 20) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 명시적 MPM 의 "시간 2 차" 라는 형식적 주장 [5] 과 실제 "시간 0 차 수렴" 관측 [7] 의 어긋남을, 공간 오차가 가속도에 섞여 시간 갱신식에 c₁h^p·Δt 로 붙는다는 Lawson 외 [18] 의 모형 **v^{k+1} = v^k + (a^k + c₁h^p)Δt + c₂Δt^q** (식 1 · p.1210) 으로 설명한다 — 격자 넘김이 없는 **moving-mesh MPM** 과 **비물리 단순 문제 둘**로 오차를 갈라 (시간 도약 오차 = O(Δt²) · 식 82 · 표 I / 노드 적분 오차 = 걸음마다 ε = Cαγ(t) 가 쌓여 전역 E_q = ½TCα^kΔt + ½T²Cα^k · 식 112–113 · 둘째 항은 Δt 와 무관한 바닥), 1D 주기 막대 제조해에서 **한 걸음 국소 절단 오차**로 c₁ (1024 셀 격자 가속도 L2 오차 ÷ h²) · c₂ (Δt = 10⁻⁴ 한 걸음 격자 속도 오차 ÷ Δt³) 를 재고, 균형 Δt = √(c₁/c₂)·h (2 차 공간 · 식 124) · √(c₁/c₂)·√h (선형 기저 standard MPM · 식 128) 를 예측해 2048 셀에서 **1.9917×10⁻⁵ · 5.1196×10⁻⁵** 를 얻는다 (p.1236 · p.1238 · 원문 *"precisely"* — 이 카드의 점근선 교차 판독 −2.3 % · **+38 %**).  균형 Δt 는 안정 한계 (CFL 1) 의 **4–10 배** [카드 산술 · CFL 식 미인쇄] 라 안정한 Δt 에서는 늘 공간 오차가 지배하고, 그래서 권고가 **"안정 한계 근처 Δt 면 충분 · 그보다 줄여도 소용없다"** 와 **"선형 기저에서 셀당 물질점 (PPC) 을 고정하면 격자를 조여도 오차가 줄지 않는다 — PPC 를 격자와 함께 늘리거나 매끈한 기저 (2차 B-spline) 를 쓴다"** 이다 (§7 · §8).

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 공간 · 시간 오차를 가르는 법 | ① **moving-mesh MPM** (참조 배치에서 기저 Φ_i(X_p) · F_p = I + Σ_i∇₀Φ_i(X_p)u_i (44) · 1st Piola–Kirchhoff 내부력 (45)) — 물질점이 늘 '이상적 자리' 라 노드 적분 오차가 시간에 따라 안 변하고 격자 넘김 오차 0 ② 단순 문제 둘 (고정 조각 선형 속도장 → 도약 오차만 · 불연속 g(x) 의 중점 적분 → 노드 적분 오차만) ③ **한 걸음 국소 절단 오차** — 누적 · 안정 조건 없이 잰다 | [인쇄] §3.3 · §5 · p.1235 |
| ② ★ 균형 Δt 의 식 · 상수 측정 | (122) → c₁h² = c₂Δt² → **Δt = C h** (124) / (126) → c₁h = c₂Δt² → **Δt = C√h** (128) · C = √(c₁/c₂) · moving-mesh 선형: c₁ = 1.7895×10⁻²/h² = **1.8764×10⁴** (135) · c₂ = 1.1277×10⁻⁵/Δt³ = **1.1277×10⁷** (136) · standard 선형: c₁ = 5.9119×10⁻²/h = **6.0538×10¹** (137) · c₂ = **1.1278×10⁷** (138) · 2048 셀 예측 **1.9917 · 2.3908 · 5.1196 · 2.6507 ×10⁻⁵** (moving-mesh 선형 · B-spline · standard 선형 · B-spline) | [인쇄] p.1231–1232 · p.1236 · p.1238 |
| ③ 시간 도약 오차 (격자 넘김) | 한 걸음 ↔ 두 걸음 (마디까지 · 나머지) 차 ≤ **¼[(∂v/∂x)v_p + a_p]Δt²** (82) · 표 I 추정 2.34 · 9.36 · 28.1 ×10⁻⁸ ↔ 계산 1.81 · 7.60 · 18.4 ×10⁻⁸ · 전체 MPM (64 셀 · 100 PPC) 에서 쌓인 도약 오차 = 변위 오차의 ≈9 % [판독] | [인쇄] p.1224–1225 · p.1233 · [판독] Fig. 11 |
| ④ ★ 노드 적분 오차 · 셀당 물질점 | 노드 힘 오차 상한 선형 **2σΔx/h** (94 · C₁ ½) · 2차 B-spline **σΔx²/h²** (95 · C₂ ⅛) → 걸음당 ε = Cαγ(t) (96 · α = Δx/h = 1/PPC · γ ∈ [−1, 1]) → 전역 **½TCα^kΔt + ½T²Cα^k** (112 · 113) · *"If the number of PPC remains constant, α also remains constant, and the global displacement error will not be reduced as grid resolution is increased"* (p.1240) · 그림 13a: 선형 고정 PPC 는 최소 뒤 128 → 1024 셀에서 **3.0–9.5 배 커진다** [판독] | [인쇄] p.1227–1229 · p.1240 · [판독] Fig. 13 |
| ⑤ 기저 (선형 ↔ 2차 B-spline) | B-spline = 조각 상수의 합성곱 (30) · 열린 매듭 + Cox–de Boor (32–34) · 노드에서 C¹ → 입자 가속도가 격자 넘김에서 연속 (그림 12) · 적분 오차 α → α² · standard 에서도 공간 2 차 (원문) — 판독은 고운 끝 1.6–1.7 | [인쇄] p.1214–1215 · p.1233 · p.1237 · [판독] Fig. 17 |
| ⑥ ★ 안정 한계 · '시간 0 차 수렴' | *"the time-step Δt, where spatial and temporal errors are balanced, is much higher than the stability limit … This explains why previous researchers [7] were not able to demonstrate the second-order temporal convergence"* (p.1240) · [카드 산술] 균형점 CFL (= cΔt/h · c = 100) **4.08 · 4.90 · 10.5 · 5.43** | [인쇄] p.1240 · [카드 산술] |
| ⑦ 실전 권고 (표 II) | 선형 · 128 셀 · 4 PPC · CFL 0.1 → RMS **2.21×10⁻²** · **9.62 s** / 2차 B-spline · 64 셀 · 4 PPC · CFL 0.9 → **8.39×10⁻⁵** · **0.50 s** (오차 263 배 · 시간 19 배 [카드 산술]) | [인쇄] p.1240–1241 |
| ⑧ 오차 목록 | 보간 (O(h^k) · *"rarely the limiting"*) · 덩어리 질량 (O(h²) · *"rarely the limiting error"*) · 시간 적분 · 시간 도약 · 노드 적분 — 공간 차수는 노드 적분 · 덩어리 질량 때문에 **2 차가 끝** | [인쇄] p.1209 · p.1239–1241 |
| ⑨ 저자 한계 · 원문 안 어긋남 | moving-mesh 는 *"not well suited for large deformation problems"* (p.1219) · 그림 9 의 단조 증가는 설계된 것 (실제는 해 둘레 진동 · p.1230) · 어긋남: Δt₀ = 0.01 ↔ 맞는 값 10⁻³ · 't = 0.2122·C' ↔ '/C' · '∫g dx = 0' ↔ 식 (87) 값 J/12 · 참고 [22] DOI = [11] 의 DOI · 참고 [12] 권 32 ↔ 원문 31 (§3-8) | [인쇄] · [카드 산술] |

⛔ **한정어 (떼지 말 것)**: ① **1D · 탄성 neo-Hookean (ν 0) · 매끈한 제조해 (체적력으로 만든 해) · 주기 경계** — 알갱이 · 접촉 · 소성 · 거의 비압축 · 압밀 · 판 · 벽 · 탈압 · 2D/3D 계산이 없다 ② 상수 c₁ · c₂ · 균형 Δt · 균형 CFL 은 **이 문제의 값** — 저자: *"Constants c1 and c2 are problem dependent"* (p.1210) · §6.4 의 A · E 는 인쇄되지 않았다 (c₂ 해석값으로 A 0.05 · C 100 이 맞는다 [카드 산술]) ③ 시간 적분 = 명시 Forward-Euler (18–22) · 엇갈린 중심차분 (23–27) 만 ④ *"precisely"* (p.1236 · p.1238) 는 그림 눈 대조 — 판독 교차는 −2.3 · −9.8 · **+38** · +7.7 % (§3-6) ⑤ 원문 안 어긋남 다섯 (§3-8) · CFL · 노름 식 미인쇄 ⑥ 이 논문의 'particle' = **물질점 (적분점)** — 알갱이가 아니다.
⇒ **절대값 전이: 0 건.**  전이되는 것은 **오차 모형의 꼴 (Δt_bal ∝ h^{p/2}) · 시험 절차 (한 시각 공간 오차 · 한 걸음 시간 오차 · 상수 · 균형 예측) · 기저 · PPC · Δt 규칙의 방향 · 보고할 칸** 뿐이다.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-37 의 '왜' 칸)

의도 원문: *"f — 공간 · 시간 오차를 갈라 균형 맞추는 법 → 격자 간격 · 시간 간격 규칙 (U1 · U6 의 수렴 판정)"* (가리킨 카드 = `gritton2017_mpm_chemomechanical_coupling_silicon_anode` ref. [36] · b40 findings n 절)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "공간 · 시간 오차를 갈라" | **채움** | 세 장치: ① moving-mesh MPM (§3.3 · 식 39–61 · p.1215–1217) — *"Moving-mesh MPM is a fully Lagrangian method that helps to control some of the more complicated sources of errors within MPM—quadrature and grid crossing errors"* (p.1208) ② 단순 문제 둘 (§5.2 고정 속도장 · §5.3 불연속 g(x) · p.1220–1230) ③ 한 걸음 국소 절단 오차 (§5.4 · §6.4 · *"As overall stability of the simulation is not required when looking at a single time-step, we are free to operate in regimes we could not previously test"* p.1235).  조건 = 1D · 탄성 · 동역학 (압력 · 누름 · 뺌 없음) |
| "균형 맞추는 법" | **채움** | 식 (1) (Lawson 외 [18] 의 꼴 · p.1210) → (122) · (126) → Δt = Ch (124) · C√h (128) · C = √(c₁/c₂) · 상수는 수렴 구간 한 점에서 **측정** (135–138) · 예측 2048 셀 1.9917×10⁻⁵ (moving-mesh 선형) · 2.3908×10⁻⁵ (B-spline) · 5.1196×10⁻⁵ (standard 선형) · 2.6507×10⁻⁵ (standard B-spline) — 원문 *"the transition occurs precisely where we expect"* (p.1236) · [판독] 점근선 교차 1.945 · 2.156 · 7.06 · 2.86 ×10⁻⁵ (−2.3 · −9.8 · **+38** · +7.7 %) · [카드 산술] c₂ 해석값 (1/24)A(Cπ)⁴\|cos(Cπt)\|/√2 = 1.1277×10⁷ (A 0.05 · C 100 · t = 0.2122/C) = 인쇄값 |
| "→ 격자 간격 규칙" | **일부** | 규칙은 **h 의 절대 크기가 아니라 기저 · PPC** 쪽: 선형 기저 + 고정 PPC 면 *"convergence is lost"* (p.1233 · 그림 13a) · PPC 를 N 과 함께 늘리면 1 차 (그림 13b 기울기 0.96 [판독]) 이나 입자 O(N²) *"may be prohibitive in practice"* (p.1235) · 2차 B-spline 이 적분 오차를 α → α² (113 · p.1240) · 공간 차수는 노드 적분 · 덩어리 질량 때문에 2 차가 끝 (p.1209 · p.1241).  **h 를 문제의 길이 (알갱이 지름 · 틈) 에 견주는 규칙 · 지름당 셀 수 = 없음** |
| "→ 시간 간격 규칙" | **채움 (그 1D 탄성 문제 안)** | *"time-steps near the stability limit are sufficient in most cases"* (p.1241) · *"running with a time-step significantly lower than the stability limit has no effect on reducing the temporal errors further"* (p.1240) · [카드 산술] 균형점 CFL 4.08 · 4.90 · 10.5 · 5.43 (CFL = cΔt/h · c = √(E/ρ₀) = 100 · CFL 식 미인쇄) · 표 II CFL 0.9 + B-spline 이 CFL 0.1 + 선형보다 오차 263 배 작고 19 배 빠름.  조건: 명시 중심차분 · 1D 탄성 · 매끈한 해 |
| "(U1 · U6 의 수렴 판정)" | **일부** | 판정 **절차**는 옮겨진다 — 한 시각의 격자 가속도 L2 오차 (식 133) h 사다리 (그림 14 · 17) + 한 걸음 국소 오차 Δt 사다리 (그림 15 · 18) → 상수 → 균형 Δt 예측 → 다른 해상도에서 교차 확인 (그림 16 · 19) + 격자 × PPC 엇갈림 (그림 13).  U1 (입자 하나 압축 · 지름당 셀) · U6 (작은 조밀 충전 압축) 의 **내용 = 없음** — 알갱이 · 접촉 · 소성 · 압밀 0 회 |

**가리킨 카드 · 이 논문을 다룬 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `gritton2017_…` L91 | *"MPM along with the multiple variants of the method are well described in the literature [32–37]"* — 이 논문 = [36] (값 인용 없음) | §3 이 standard · moving-mesh MPM 을 Galerkin 에서 유도해 설명 (식 2–61) | **채움** — 묶음 인용으로 맞다 (이 논문의 본 몫은 설명보다 오차 분석) |
| 후보 표 `S8_candidates.md` L61 (N-37 서지 칸) | "Steffen M, Kirby R M and Berzins M 2010 Decoupling and balancing of space and time errors in the material point method (mpm) Int. J. Numer. Methods Eng. 82 1207–43" | 첫 쪽: "(MPM)" · *Int. J. Numer. Meth. Engng* 2010; 82:1207–1243 · DOI 10.1002/nme.2787 | **채움** — 저자 · 연도 · 권 · 쪽 같음 · 제목 괄호 '(mpm)' 소문자 · 학술지 약어 꼴만 다름 · DOI 없음 |
| `steffen2008_…` L131 | 앞 논문 [11] 의 결과 "도약 오차 C[[f^(p+1)]]Δx^(p+2) · 선형 기저 ∇φ → O(Δx)" | 이 논문 p.1227–1228: 선형 E_jump = C₁[[φ′(0)]]Δx · C₁ = ½ · 2차 B-spline E_jump = C₂[[φ″(0)]]Δx² · C₂ = ⅛ (식 93–95) | **채움** (같은 꼴 · 이 논문이 상수 C₁ · C₂ 를 더한다) |
| `steffen2008_…` L411 ([미확인] 8) | stomakhin2013 L64 의 'Steffen et al. 2008' 3차 B-spline 식의 원전 | 이 논문에도 3차 식 없음 (2차 B-spline 만 · 식 30–34 · *"also detailed in [12]"* p.1209) | **해소 못 함** — [미확인] 그대로 |

⇒ **의도 대조 결과: 일부** — 공간 · 시간 오차를 가르는 법과 균형 Δt 식 (c₁ · c₂ 측정법) 은 **채움**, 시간 간격 규칙 (안정 한계 근처면 충분) 은 **그 1D 탄성 문제 안에서 채움**, 격자 간격 규칙은 **기저 · PPC 쪽만 일부** (h 의 절대 크기 · 지름당 셀 없음), U1 · U6 은 **절차만 일부 · 내용 없음** (접촉 · 다물체 · 압밀 0 회).  2 차 인용 (gritton2017 L91 · S8 서지 칸) 은 원문과 맞다.

---

## 1. 한 줄 요약
MPM 의 시간 수렴이 '형식적 2 차' 와 달리 0 차로 보이는 이유를, 공간 오차 (노드 적분 · 격자 넘김) 가 가속도에 섞여 시간 갱신식에 붙는다는 모형 (식 1) 과 그 모형을 시험할 수 있게 공간 오차를 떼어 내는 장치 (moving-mesh MPM · 단순 문제 둘 · 한 걸음 국소 오차) 로 풀고, 1D 주기 막대에서 균형 Δt 를 미리 계산해 맞힌 뒤 실무 권고 (매끈한 기저 · 안정 한계 근처 Δt · PPC 를 격자와 함께 늘림) 를 낸다 (`txt_p1_summary_balance_guidelines.png` · `txt_p2_motivation_formally_second_order_vs_zero_order.png`).
저자의 결론: *"time-steps near the stability limit are sufficient in most cases as time-steps near the stability limit already lead to solutions which are dominated by spatial errors"* (p.1241).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| M. Steffen · R. M. Kirby\* · M. Berzins (U. Utah · School of Computing · SCI Institute) | Int. J. Numer. Meth. Engng 82, 1207–1243 (2010) · 호 10 (배너) | 10.1002/nme.2787 | **재료 없음** — 무차원 1D neo-Hookean 주기 막대 (E 10⁴ · ρ₀ 1 · ν 0) + 비물리 단순 문제 둘 | MPM 수치 해석 (오차 분석 + 수치 시연) |

- **1저자 메모 (후보 표 행) 와의 대조**: 저자 · 제목 · 권 82 · 쪽 1207–1243 · 2010 — **같다**.  다른 점: 제목 괄호 '(MPM)' (행은 '(mpm)') · 학술지 약어 꼴 ('Int. J. Numer. Meth. Engng') · 호 10 (배너에서만) · DOI 10.1002/nme.2787 (행에 없음).
- **글의 꼴**: 1 서론 → 2 배경 → 3 MPM 개요 (3.1 Galerkin · 3.2 standard MPM · 3.3 moving-mesh MPM) → 4 Lagrangian–Eulerian 결합 해석 → 5 단순 문제 연구 (5.1 분리 전략 · 5.2 공간 불연속 → 시간 도약 · 5.3 노드 적분 오차 → 시간 · 5.4 공간 · 시간 오차 균형) → 6 전체 MPM 결과 (6.1 1D 주기 막대 · 6.2 도약 · 6.3 노드 적분 · 6.4 균형 · 6.4.1 standard) → 7 권고 (GUIDELINES) → 8 요약 · 결론 → 참고문헌 23.  그림 19 · 표 2 · 번호 식 138 · 각주 2 (‡ 선형계 표기 · § 그림 2 의 문제).
- 무리 맥락: Utah MPM Group (C-SAFE · Uintah 계열) — 앞 논문 [11] (노드 적분 오차 분석 · IJNME 2008 · 카드 없음) · [12] (구현 선택 · CMES 2008 = 정본 `steffen2008_…`).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. MPM 알고리즘 · moving-mesh MPM (§3 · 식 2–61 · `eq_002_…` – `eq_061_…` · `fig_1.png` · `txt_p3_p4_moving_mesh_small_deformation_no_grid_crossing.png`)
- Galerkin 약형 (3) → Ma = f^int + f^ext (4) · 덩어리 질량 = **행 합 (row-sum)** m_i = Σ_j M_ij = ∫ρφ_i dΩ (9 · 분할의 합이 전제) — *"the most prevalently used method employed in practice within the MPM community"* (p.1211).
- **노드 적분 = 준-중점 규칙 (quasi-midpoint rule · p.1213)**: v_i ≈ Σ_p m_p v_p φ_ip / Σ_p m_p φ_ip (15) · f_i^int ≈ −Σ_p σ_p·∇φ_ip V_p (16) · f_i^ext ≈ Σ_p m_p b_p φ_ip (17) · V_p = det(F_p)V_p⁰ (14).
- standard MPM 한 걸음 = **Forward-Euler** (18–22): v_i^{k+1} = v_i^k + a_iΔt → ∇v_p = Σ_i∇φ_ip v_i^{k+1} → F_p^{k+1} = (I + ∇v_pΔt)F_p^k → v_p += Σ_iφ_ip a_iΔt → u_p += Σ_iφ_ip v_i^{k+1}Δt.  ★ **입자 속도를 반 걸음 앞 (v_p^{−1/2}) 으로 초기화하면 같은 절차가 엇갈린 중심차분** (23–27) 이 된다 (*"a simple change of initializing particle velocities a half time-step earlier"* p.1214) — Sulsky 외 [5] 의 방식 · 장점 검토는 Wallstedt · Guilkey [7].
- 기저: 선형 φ(x) = 1 − \|x\|/h (28) · 분리형 3D 곱 (29) · 2차 B-spline = 조각 상수의 합성곱 φ = χ∗χ∗χ/\|χ\|² (30–31) · 열린 매듭 벡터 + Cox–de Boor 재귀 (32–34 · k 차면 함수 n + k − 2 개) — 분할의 합 유지 · 노드에서 C¹ (p.1215).
- **moving-mesh MPM (§3.3)**: 격자 질량 m_i = Σ_p m_p Φ_ip (39–43 — standard 와 같은 합이고 기저만 참조 배치 X_p 에서) · **F_p = I + Σ_i∇₀Φ_i(X_p)u_i** (44 · 시간 적분 아님 · 격자 변위에서 바로) · 내부력 = −Σ_p P_p·∇₀Φ_ip V_p⁰ (45 · 1st Piola–Kirchhoff · 처음 부피) · 초기 격자 변위 = 덩어리 L2 투영 (46–50) · 한 걸음 11 단계 (51–61).  *"Particles should be equally spaced and aligned with the grid cell boundaries as the major benefits of moving-mesh MPM are only obtained when particles are in these 'ideal' positions"* (p.1216) · 앞 논문들 [11, 12] 은 *"fixed background grid—a grid that 'resets' back to the starting position after each time-step"* 를 가정했고 *"It is this overlap that leads to the largest quadrature errors"* (p.1209).

### 3-2. 오차 모형 · 균형 (§2 · §4 · §5.4 · 식 1 · 62–65 · 116–128 · `eq_001_…` · `eq_116_…` – `eq_128_…` · `txt_p4_cd_zero_order_and_lawson_error_model.png` · `txt_p12_formally_second_order_unrealizable_jump.png`)
- 동기 (p.1210): USF · USL · CD 비교 [17, 7] 에서 CD 가 오차는 가장 작지만 *"the method showed no temporal error convergence in the regions of time-step selection where their simulations were stable"*.
- 식 (1) v^{k+1} = v^k + (a^k + c₁h^p)Δt + c₂Δt^q — *"Constants c1 and c2 are problem dependent, but once determined can be used to find the location where spatial and temporal errors are balanced (i.e. where c1h^pΔt = c2Δt^q)"* (p.1210).
- 중심차분은 형식상 2 차 (116–119) · 한 걸음 국소 오차 O(Δt³) (120) — 그러나 *"this formal analysis carries with it assumptions regarding the smoothness and accuracy of a, assumptions that do not hold within the MPM framework … significant quadrature errors in space and discontinuities in time [22], both of which make second-order temporal convergence unrealizable to the MPM practitioner"* (p.1218).
- 2 차 공간 (moving-mesh · B-spline): a^k = ã^k + c₁h² (121) → v^{k+1/2} = v^{k−1/2} + Δt(ã^k + c₁h²) + c₂Δt³ (122) → c₁h² = c₂Δt² (123) → **Δt = Ch** (124).  선형 기저 standard: a^k = ã^k + c₁h (125) → (126) → c₁h = c₂Δt² (127) → **Δt = C√h** (128) · B-spline 은 standard 에서도 Δt = Ch (p.1232).
- [카드 산술] 같은 h 에서 국소 오차 비 (시간 ÷ 공간) = c₂Δt³/(c₁h^pΔt) = (Δt/Δt_bal)² — 균형 Δt 의 1/10 이면 시간 몫 1 %.

### 3-3. 시간 도약 오차 (§5.2 · §6.2 · 식 70–86 · 표 I · 그림 3–6 · 11 · `fig_3.png` – `fig_6.png` · `tab_1.png` · `fig_11.png` · `txt_p18_dt0_001_jump_errors_tight_bounds.png` · `txt_p27_jump_error_64cells_100ppc_small.png`)
- 단순 문제: 입자 하나가 x = 0 에서 출발 · 고정 속도장 v = 3x+1 · 6x · 12x−4 · 18x−9 (구간 [0, 1/3] · [1/3, 2/3] · [2/3, 5/6] · [5/6, 1] · 식 70) — 연속 · 기울기만 불연속 → 정확해 = 구간별 지수 (72–74).  [카드 산술] 마디를 넘는 시각 = (1/3)ln2 = **0.2310** · +(1/6)ln2 = **0.3466** · +(1/12)ln(3/2) = **0.3804** = 그림 6 의 세 도약 자리 0.231 · 0.347 · 0.381 [판독].
- 한 걸음 ↔ 두 걸음 (마디까지 Δt₁ · 나머지 Δt₂ — Tran 외 [22] 의 식 76) 차 = [(∂v/∂x)v_p + a_p]Δt₁Δt₂ (80) · Δt₁Δt₂ = α(1 − α)Δt² (81 · ⚠ 여기 α = 걸음 비율 — 식 96 의 α = Δx/h 와 다른 뜻) → **≤ ¼[(∂v/∂x)v_p + a_p]Δt² = O(Δt²)** (82 · `eq_082_jump_error_bound_quarter.png`).
- 그림 5 (마디가 한 걸음 가운데 · 83–84): 기울기 **2.00** (Δt 4.9×10⁻⁴ – 7.8×10⁻³) · 작은 Δt 에서 오차/Δt² ≈ **4.0** [판독 · 카드 산술] — 어느 마디 · 속도장인지 [미확인].
- **표 I** (추정 = 식 85 · 왼쪽 기울기 / 계산 = 식 86): 도약 1 · 2 · 3 = **2.34×10⁻⁸ / 1.81×10⁻⁸ · 9.36×10⁻⁸ / 7.60×10⁻⁸ · 2.81×10⁻⁷ / 1.84×10⁻⁷** (계산/추정 0.77 · 0.81 · 0.65 [카드 산술]) · 원문 *"tight bounds"*.  [카드 산술] 고정 속도장이라 a_p = 0 → 추정 = ¼(기울기 × v)Δt² = 1.5 · 6 · 18 ×Δt² → 표 I 값이 **Δt = 1.25×10⁻⁴** 와 정확히 맞는다 (= 10⁻³/8 · 그림 6b 의 'Δt₀/8').  ⚠ 원문은 *"Using an initial time-step (before refinement) of Δt0 = 0.01"* (p.1224) — 0.01 이면 Δt₀/8 = 1.25×10⁻³ 이라 추정이 100 배 크고 그림 6a 의 도약은 한계의 1 % 뿐이다.  10⁻³ 이면 그림 6a (Δt₀) 도약 1.43×10⁻⁶ · 4.67×10⁻⁶ · 1.37×10⁻⁵ [판독] = 한계 1.5 · 6.0 · 18 ×10⁻⁶ 의 **95 · 78 · 76 %** → **인쇄 0.01 은 10⁻³ 의 오기로 읽힌다** [카드 산술 · 카드 해석].  그림 6a/6b 도약 비 80 · 62 · 75 (2 차면 8² = 64) [판독 · 카드 산술].
- 전체 MPM (§6.2 · 그림 11): 64 셀 · **100 PPC** · A 0.05 · E 10⁴ · ρ₀ 1.0 · CFL 0.1 · 선형 기저 · 한 걸음 Forward-Euler + 매 걸음 두 걸음 위치로 도약 오차를 따로 쌓음 → 한 입자의 변위 오차 최대 **1.82×10⁻⁴** (t ≈ 0.0158) ↔ 쌓인 도약 오차 끝값 **1.60×10⁻⁵** (≈ **8.8 %**) [판독 · 카드 산술] · *"the global jump error is a relatively small percentage of the overall error, even with 100 PPC"* (p.1233).

### 3-4. 노드 적분 오차의 누적 (§5.3 · 식 87–115 · 그림 7–9 · `fig_7.png` – `fig_9.png` · `eq_093_…` – `eq_115_…` · `txt_p12_quadrature_errors_compounding.png` · `txt_p21_p22_force_error_C1_C2_alpha_inverse_ppc.png` · `txt_p24_global_error_dt_independent_floor.png`)
- 왜 MPM 만의 문제인가: *"Quadrature errors are unique in MPM, in that they are fairly low order and time-dependent, or coupled, in standard Eulerian MPM … quadrature errors have a compounding effect on MPM"* (p.1218).
- 단순 문제: g(x) = −J · 0 · J · 3J/2 (같은 네 구간 · 식 87 · 그림 7 은 J = 1 로 그림 [판독]) · '외부 가속도' a_e = ∫g dx 를 입자 영역 [x_p ± Δx/2] 만 중점값 g(x_p)Δx 로 (88) → 입자가 움직이며 오차가 시간에 따라 바뀜 (p.1227).  ⚠ 원문 *"The function g(x) was chosen such that ∫g(x)dx = 0"* (p.1226) ↔ 식 (87) · 그림 7 의 값으로 ∫g = −J/3 + J/6 + (3J/2)(1/6) = **J/12** [카드 산술] — 원문 안 어긋남 (그림 9 의 기준해가 a_e = 0 인지 [미확인]).
- 노드 힘 오차 (앞 논문 [11] · 고른 간격 물질점 · 상수 응력): E_f = σ·[∫∇φ_i dΩ − ΔxΣ_p∇φ_ip] (93) — 괄호 = 조각 상수 (선형) · 조각 선형 (B-spline) 함수의 합성 중점 적분 오차 · 입자 경계가 불연속에 맞으면 0.  상한: **선형 E_total = 2σΔx/h** (94 · 도약마다 C₁ = ½) · **2차 B-spline E_total = σΔx²/h²** (95 · C₂ = ⅛) (p.1227–1228).
- 걸음당 가속도 오차 **ε = Cαγ(t)** (96 · α = Δx/h = PPC 의 역수 · γ(t) ∈ [−1, 1] · `eq_096_acceleration_error_alpha_gamma.png`) → 최악 (γ 의 절댓값 1) 을 N 걸음 쌓으면 (97–111) **E_q = ½TCαΔt + ½T²Cα** (112 · 선형) · **½TCα²Δt + ½T²Cα²** (113 · B-spline · GIMP).  ★ 둘째 항 ½T²Cα^k 는 **Δt 와 무관** — *"we would expect global errors to decrease with the decreasing time-step Δt, but to be limited by the last term, which has no dependence on the time-step"* (p.1230) · T² 로 자라고 · Δx 로 준다 · *"it is worth noting that the global error in many simulations oscillate around the true solution"* (p.1230 · 그림 9 는 일부러 단조 증가하게 만든 문제).
- 그림 9 (단순 문제 · Δx = 1/4 · 1/8 · Δt₀/2 – Δt₀/16): 끝 (t ≈ 0.39) 오차 Δx 1/4 = **0.0158 · 0.0149 · 0.0145** (Δt₀/4 · /8 · /16) · Δx 1/8 = **0.00355 · 0.00265 · 0.00224** [판독] · 1 차 외삽 바닥 0.0142 · 0.0018 (비 7.7 — 식 115 의 Δx 비례면 2 · 식은 γ 최악 상한) [카드 산술] · Δt₀ · J [미확인].

### 3-5. 전체 MPM 1D 주기 막대 (§6.1–6.3 · 식 129–132 · 그림 2 · 10 · 12 · 13 · `fig_2.png` · `fig_10.png` · `fig_12.png` · `fig_13.png` · `txt_p26_periodic_bar_problem_definition.png` · `txt_p27_p29_constant_ppc_convergence_lost_n2_particles.png`)
- 제조해: **u = A sin(2πX)cos(Cπt)** (129) · F = 1 + 2Aπcos(2πX)cos(Cπt) (130) · 체적력 **b = C²π²u(2F⁻² + 1)** (131) · 1D neo-Hookean **σ = (E/2)(F − 1/F)** (132 · ν 0) · C = √(E/ρ₀) 파속 · A = 최대 변형 비율 · 정의역 [0, 1] 주기 (앞 논문 [12] 와 같은 막대) · 1D 에서 PK1 = Cauchy 로 구현 (p.1232).  [카드 산술] 식 (131) 은 (129) + (132) 에서 유도된다.
- 그림 10: E 10⁴ · ρ₀ 1 · A 0.1 · t = 0.0025 = 1/8 주기 · 0.005 = 1/4 주기 → 주기 0.02 = 2/C → **C = 100** [카드 산술].
- 그림 12 (standard · 4 PPC · 한 입자의 가속도 · 세 곡선 = 선형 (파선) · 2차 B-spline (점선) · 정해 'True' (실선)): 선형 기저는 격자 넘김마다 도약 (t = 0.74 · 3.85 · 4.31 ×10⁻³ 에서 −3.44 → −5.75 · −1.04 → −2.07 · −2.41 → −3.26 ×10³ [판독] — 첫 도약 2.31×10³ = 같은 시각 정해 −4.24×10³ 의 55 % [판독 · 카드 산술]) · 2차 B-spline 은 연속이지만 정해에서 +0.53×10³ (t 0.74×10⁻³ · 13 %) · +0.12×10³ (2.0×10⁻³) · −0.90×10³ (3.8×10⁻³) · −1.26×10³ (4.5×10⁻³) 벗어난다 [판독 · 카드 산술 — 연속 ≠ 정확 · 이 그림의 셀 수 [미확인]] · 정해 곡선 (PDF 의 3 차 Bézier 4 조각) = −4353·cos(100πt) 에 0.01 % 안으로 맞는다 → **C = 100** · A·sin(2πX_p) = 0.0441 [판독 · 카드 산술] · *"A close inspection shows that a_i is only C0 continuous for quadratic B-spline basis functions"* · *"This jump in the acceleration is unaffected by the time-step selection"* (p.1233).
- 그림 13a (standard · 선형 · PPC 고정 · 한 주기 뒤 RMS 변위 오차): 처음 O(h²) 뒤 *"convergence is lost"* — 최소 = 2 PPC **9.47×10⁻³** (h 1/8) · 4 PPC **4.40×10⁻³** (1/16) · 8 PPC 1.66×10⁻³ (1/32) · 16 PPC 8.47×10⁻⁴ (1/32) · 32 PPC 3.75×10⁻⁴ (1/32) · 64 PPC 1.49×10⁻⁴ (1/64) · 1024 셀에서 9.45×10⁻² · 5.45×10⁻² · 4.01×10⁻² · 1.89×10⁻² · 5.31×10⁻³ · 1.39×10⁻³ [판독] → 최소는 PPC^−1.19 [카드 산술] · 128 → 1024 셀에서 오차가 N^0.53–1.08 로 **커진다** (3.0–9.5 배) [카드 산술] · 2 · 4 · 8 PPC 는 1024 셀 오차가 4 셀 (2.07 · 2.31 · 2.28 ×10⁻²) 보다 크다 [판독].  ⚠ 가로축 이름은 'Grid Cells' 인데 눈금은 10⁰ – 10⁻⁴ (= h) [판독].
- 그림 13b (PPC = N/4): 9.46×10⁻³ (8 셀) → 3.42×10⁻⁴ (256 셀) · 기울기 **0.96** [판독 · 카드 산술] · 점들이 그림 13a 의 대각 (N = 4·PPC) 과 같다 [판독] · *"This ever increasing number of PPC results in a seemingly consistent first-order method. This, however, may be prohibitive in practice as the total number of particles is increasing quadratically with the number of grid cells"* (p.1234–1235).

### 3-6. ★ 전체 MPM 의 균형점 (§6.4 · 식 133–138 · 그림 14–19 · `fig_14.png` – `fig_19.png` · `eq_133_…` – `eq_138_…` · `txt_p29_stability_limit_single_step_lte.png` · `txt_p30_c1_c2_balance_2048_cells_precise.png` · `txt_p31_p32_standard_mpm_first_order_plateau_balance.png`)
- 왜 한 걸음인가: *"One limitation on the previous studies has been the stability of the solution, requiring the CFL number to be less than unity … If a simulation fails due to stability reasons, the global error cannot be measured"* (p.1235).
- 공간 오차 = **격자 가속도 L2 오차 ε_a² = ∫(ã − a)²dx** (133 · ã = Σa_iφ_i · 134) · 시각 = *"approximately 1/10 the period of oscillation (specifically at time t = 0.2122·C)"* (p.1236) — [카드 산술] '·C' 면 C = 100 에서 t = 21.2 (주기 0.02 의 1,061 배) → **'/C'** (t = 2.122×10⁻³ = 주기의 0.106) 로 읽힌다 · 4 PPC · 주기 경계.
- 그림 14 (moving-mesh · 128–8192 셀): 선형 · B-spline 기울기 **2.000 · 1.999** [판독] · 1024 셀 선형 **1.79×10⁻²** (인쇄 1.7895×10⁻² · 판독/인쇄 1.0002) · B-spline 2.585×10⁻² [판독].
- 그림 15 (moving-mesh · 2²⁰ 셀 · 한 걸음 격자 속도 오차): 3 차 (Δt 3.1×10⁻⁶ – 4.0×10⁻⁴) · Δt 10⁻⁴ 에서 1.13×10⁻⁵ (인쇄 1.1277×10⁻⁵) · Δt ≤ 1.56×10⁻⁶ 에서 다시 오름 (9.3×10⁻¹² → 3.8×10⁻¹¹ [판독]) — 원문 설명 없음 · 공간 항 c₁h²Δt 는 1.7×10⁻¹⁴ 뿐 [카드 산술] (반올림 오차일 수 있다 [카드 해석]).
- 그림 16 (moving-mesh · 2048 셀): 작은 Δt 는 기울기 1 (= c₁h²Δt 꼴) · 큰 Δt 는 3 · 점근선 교차 선형 **1.945×10⁻⁵** (예측 1.9917×10⁻⁵ · −2.3 %) · B-spline **2.156×10⁻⁵** (예측 2.3908×10⁻⁵ · −9.8 %) [판독 · 카드 산술] · B-spline 은 Δt 2.5×10⁻⁵ 에서 오목 (5.8×10⁻¹¹ — 두 오차 부호가 반대인 상쇄로 보인다 [카드 해석]).  ⚠ 절대 크기는 c₁h²Δt · c₂Δt³ 의 약 0.004 배 (두 항이 같은 배수라 교차점은 그대로 — 두 항 모두 cos(Cπt) 에 비례해 평가 시각이 1/4 주기 근처면 이렇게 된다 [카드 해석]) · 그림 15 와 같은 Δt 에서 228 배 차 — 노름 · 시각 [미확인].
- 그림 17 (standard · 128–8192 셀): 선형 기저 2 · 4 · 6 PPC = 처음 2 차 → 끝 **1 차** (2048 → 8192 기울기 1.01 · 1.00 · 1.06) · 1024 셀 4 PPC **5.92×10⁻²** (인쇄 5.9119×10⁻² · 판독/인쇄 1.0014) · 2 PPC 0.237 · 6 PPC 0.0319 · 2차 B-spline 4 PPC = 128 → 512 기울기 **2.00** · 2048 → 8192 **1.73** · 4096 → 8192 **1.61** [판독 · 카드 산술] — 원문 *"Quadratic B-spline basis functions still exhibit the expected second-order spatial convergence"* (p.1237) 는 고운 끝에서 판독과 어긋난다 · 선형 쪽은 *"initially exhibit second-order spatial convergence with smaller numbers of grid cells when approximation or mass-lumping errors are dominating. However, the asymptotic O(h) quadrature errors eventually dominate"* (p.1237).
- 그림 18 (standard · 2²⁰ 셀): 큰 Δt 3 차 · Δt 10⁻⁴ 1.13×10⁻⁵ (인쇄 1.1278×10⁻⁵) · 작은 Δt 의 **평탄** = 선형 1.31×10⁻⁷ · B-spline 1.08×10⁻⁸ (Δt ≤ 6.25×10⁻⁶ 에서 Δt 와 거의 무관) [판독] · 원문 *"a convergence plateau is reached, where the larger spatial errors in standard MPM are starting to dominate"* (p.1238) — 식 (126) 의 공간 항 c₁hΔt 는 Δt 에 비례해야 하므로 이 평탄은 그 꼴이 아니다 (걸음 전부터 있던 격자 속도 투영 오차로 읽힌다 [카드 해석]).
- 그림 19 (standard · 2048 셀): 선형 교차 **7.06×10⁻⁵** (예측 5.1196×10⁻⁵ · **+38 %**) · B-spline **2.86×10⁻⁵** (예측 2.6507×10⁻⁵ · +7.7 %) [판독 · 카드 산술] — 원문 *"The transition point between spatial and temporal errors dominating occurs precisely at our estimate"* (p.1238).  [카드 산술] 판독 기울기 1 계수 ÷ c₁h = 0.0083 · 3 차 계수 ÷ c₂ = 0.0044 — 두 항이 다른 배수라 교차가 √(0.0083/0.0044) = 1.38 배로 옮겨 간다.
- [카드 산술] **균형점의 CFL** (= cΔt/h · c = 100 · 원문에 CFL 식 없음): 2048 셀 CFL 1 ↔ Δt 4.88×10⁻⁶ → 균형점 CFL **4.08** (moving-mesh 선형) · **4.90** (moving-mesh B-spline) · **10.5** (standard 선형) · **5.43** (standard B-spline).  2 차 공간이면 균형 CFL = cC 로 h 와 무관 (4.1–5.4) · 선형 standard 는 cC/√h 로 h 와 함께 커진다 (19 셀 아래에서만 1 미만).
- [카드 산술] B-spline 의 c₁ (원문 미인쇄 · 균형 Δt 에서 역산 · c₂ 같다고 둠): moving-mesh 2.71×10⁴ (1024 셀 ε_a 0.0259 = 판독 0.02585 와 맞음) · standard 3.33×10⁴ (ε_a 0.0318 · 판독 512 · 2048 셀 사이 기하 보간 0.0320).

### 3-7. ★ 권고 · 표 II (§7 · §8 · `tab_2.png` · `txt_p34_guidelines_ppc_must_increase_dt_near_stability.png` · `txt_p34_p35_table2_setup_cfl01_vs_cfl09.png` · `txt_p35_p36_conclusion_two_guidelines_second_order_limit.png` · `txt_p3_quadrature_midpoint_bspline_second_order_limit.png`)
- 오차 목록 (p.1239–1240): 보간 (FE 꼴 · O(h^k) · 선형으로도 O(h²) · *"rarely the limiting factor"*) · 덩어리 질량 (O(h²) · *"rarely the limiting error"* · 안정 · 단조성 이점은 *"not explored in this work"*) · 표준 시간 적분 · 시간 도약 (매끈한 기저가 차수를 바꾼다) · 노드 적분 (전역 ∝ α^k · *"The choice of Δt does not affect these quadrature errors"*).
- *"If the number of PPC remains constant, α also remains constant, and the global displacement error will not be reduced as grid resolution is increased. To have a consistent method, α must be reduced as grid resolution is increased, meaning the number of PPC must increase as the number of grid cells is increased"* (p.1240).
- *"the time-step Δt, where spatial and temporal errors are balanced, is much higher than the stability limit when the explicit centered difference time-stepping scheme is used on this type of a problem … running with a time-step significantly lower than the stability limit has no effect on reducing the temporal errors further"* (p.1240).
- **표 II** (1D 주기 막대 · RMS 입자 위치 오차 · 실행 시간): 모의 1 = 선형 · **128 셀 · 4 PPC · CFL 0.1** → **2.21×10⁻² · 9.62 s** / 모의 2 = 2차 B-spline · **64 셀 · 4 PPC · CFL 0.9** → **8.39×10⁻⁵ · 0.50 s** — 오차 263 배 · 시간 19.2 배 [카드 산술] · T · A · E · 기계 [미확인] (그림 13a 4 PPC · 128 셀 1.68×10⁻² [판독] 과 같은 자릿수 · B-spline 64 셀 값은 선형 4 PPC 의 최소 4.40×10⁻³ 보다도 52 배 작다 [카드 산술]).
- 결론 두 권고 (p.1241): ① 매끈한 기저 (2차 B-spline) 가 노드 적분 오차 · 전역 오차를 크게 줄인다 ② 안정 한계 근처 Δt 면 대부분 충분.  공간 한계: *"Midpoint integration errors are also second-order and therefore, whereas higher-order basis functions may improve the overall error further, spatial convergence rates will not improve with the current integration strategies. For higher than second-order spatial convergence, more advanced techniques than nodal integration as currently employed would be required"* (p.1209) · *"the nodal integration and the implicit mass lumping in MPM currently restrict the method to second-order in space [11]. To further reduce errors in the method, more advanced error control techniques beyond simple grid refinement may be required"* (p.1241).

### 3-8. ★ 저자가 적은 한계 · 원문 안 어긋남
**저자 한계**
1. moving-mesh MPM: *"not well suited for large deformation problems and can experience mesh entanglement issues"* (p.1219 · `txt_p13_moving_mesh_not_for_large_deformation.png`) — 분석 도구로만 쓴다 · *"it remains effective for small deformation problems"* (p.1209).
2. 권고의 범위: *"guidelines for the practitioner when implementing a similar variant of MPM as used in this paper"* (p.1241) · 명시 시간 적분만 분석 (p.1208) · 보간 오차 *"received little treatment in this paper"* (p.1240).
3. 그림 9 의 단조 증가는 설계된 것 — 실제는 해 둘레에서 진동 (p.1230).
4. 공간 2 차 한계 (노드 적분 · 덩어리 질량 · p.1209 · p.1241).

**원문 안 어긋남 (카드 산술 · 대조 — 인용 때 표지)**
5. Δt₀ = 0.01 (p.1224) ↔ 표 I · 그림 6 이 맞는 값 10⁻³ (§3-3).
6. 그림 14 · 본문의 't = 0.2122·C' ↔ '/C' (§3-6).
7. *"∫g dx = 0"* (p.1226) ↔ 식 (87) · 그림 7 의 값 J/12 (§3-4).
8. 참고 [22] (Tran · Kim · Berzins · IJNMF 2009) 의 DOI 가 10.1002/nme.2360 = 참고 [11] 의 DOI (p.1243) · 학술지 (IJNMF) 와도 맞지 않는 접두 (nme).
9. 참고 [12] 권 **32(2)** (p.1242) ↔ 정본 `steffen2008_…` L3 · L416 (원문 첫 쪽) **31(2)** [다른 카드].
10. *"precisely"* (p.1236 · p.1238) ↔ 판독 교차 +38 % (standard 선형) · B-spline 2 차 (p.1237) ↔ 고운 끝 1.6–1.7 · 그림 13 가로축 이름 'Grid Cells' ↔ 눈금 h.
11. 기호 겹침: C = 파속 √(E/ρ₀) (§6.1) · 균형 상수 √(c₁/c₂) (124 · 128) · 적분 오차 상수 (96) · α = 걸음 비율 (81) · Δx/h (96).
12. 미인쇄: CFL 식 · 'RMS displacement error' (그림 13 · 표 II) 와 'L2 errors in the grid velocity' (그림 15–19) 의 식 · §6.3–6.4 · 표 II 의 A · E · T.

---

## 4. ★ 방법 — 계산 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 계산 사슬 (무엇을 어떻게 갈랐나)
1. **이론**: 식 (1) 의 공간 · 시간 항 → 균형식 (124 · 128).
2. **단순 문제 1** (§5.2): 고정 조각 선형 속도장 (공간 오차 = 속도장의 꺾임만) → 도약 오차 해석 (80–82) · 측정 (그림 5 · 6 · 표 I).
3. **단순 문제 2** (§5.3): 같은 속도장 + 불연속 g(x) 의 중점 적분 '외부 가속도' (88–92) → 노드 적분 오차 누적 해석 (93–113) · 측정 (그림 9).
4. **전체 MPM** (§6): 1D 주기 막대 제조해 (129–132) → 도약 (그림 11) · 노드 적분 (그림 12 · 13) → 한 걸음 국소 오차로 c₁ · c₂ (그림 14 · 15 · 17 · 18) → 균형 예측 · 확인 (그림 16 · 19).
5. **권고** (§7) → 시연 (표 II).

### 4-2. 이산화 · 계산 규모 (인쇄된 것만)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 차원 | 1D (다차원은 분리형 곱 식 29 · 3D B-spline 문장만 · 2D/3D 계산 없음) | [인쇄] p.1214–1215 |
| 격자 | 그림 13: 4–1024 셀 · 그림 14 · 17: 128–8192 셀 · 그림 15 · 18: 2²⁰ 셀 · 그림 16 · 19: 2048 셀 (h = 4.88×10⁻⁴) · §6.2: 64 셀 · 표 II: 128 · 64 셀 | [인쇄] 캡션 · p.1233 · p.1236 · p.1240–1241 |
| 셀당 물질점 (PPC) | 2 · 4 · 8 · 16 · 32 · 64 (그림 13a) · N/4 (그림 13b) · 4 (그림 12 · 14–16 · 18–19 · 표 II) · 2 · 4 · 6 + B-spline 4 (그림 17) · 100 (그림 11) | [인쇄] |
| 시간 적분 | 명시 Forward-Euler (18–22) · 엇갈린 중심차분 (23–27 · 64–65) · 그림 11 = Forward-Euler + 두 걸음 비교 | [인쇄] p.1213–1214 · p.1233 |
| 시간 간격 | 그림 5–6: Δt₀/2ⁿ (Δt₀ = 0.01 인쇄 · 10⁻³ 로 읽힘) · 그림 11: CFL 0.1 · 그림 15–19: 7.8×10⁻⁷ – 4.0×10⁻⁴ · 표 II: CFL 0.1 · 0.9 · CFL 식 [미확인] | [인쇄] · [카드 산술] |
| 재료 | 1D neo-Hookean σ = (E/2)(F − 1/F) · ν 0 · E 10⁴ · ρ₀ 1 (§6.2 · 그림 10) · §6.3–6.4 · 표 II 는 인쇄 없음 (§6.3 은 *"simulated again"* · 그림 12 정해 곡선 = C 100 [판독 · 카드 산술]) | [인쇄] p.1232–1233 · [미확인] |
| 진폭 A | 0.05 (§6.2) · 0.1 (그림 10) · §6.4 는 c₂ 해석값이 A 0.05 · C 100 에서 인쇄값과 같다 | [인쇄] · [카드 산술] |
| 계산 비용 | 표 II 실행 시간 9.62 · 0.50 s (기계 [미확인]) · 그 밖 [미확인] | [인쇄] p.1241 |
| 코드 | 이름 없음 (감사: Utah MPM Group) | [미확인] |
| 맞춘 값 | **없음** — c₁ · c₂ 는 맞춤이 아니라 한 점에서의 **측정** · 실험 대조 없음 · 검증 = 제조해 · 해석 추정 | [인쇄] |

### 4-3. 입자 처리 ★
- 'particle' = **물질점 (적분점 · 질량 운반)** — 알갱이가 아니다.  물질점 영역 (voxel) = 폭 Δx (1D) · 영역이 셀 경계를 걸칠 때 노드 적분 오차가 커진다 (p.1218 · 그림 8).
- moving-mesh 에서는 물질점이 셀에 정렬된 '이상적 자리' 에 고정 (그림 1 · p.1216) · standard 에서는 셀을 넘는다 (그림 2 · 12).
- 접촉 · 다물체 · 강체 · 소성 · 형상 변화 없음 (한 물체 탄성 막대).

### 4-4. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **말 없음** (DEM · discrete element · contact · granular · powder 0 회 [카드 전문 검색]).  가까운 문장은 FE 쪽: *"these algorithms have enabled, from the engineering perspective, complicated large deformation simulations where finite element-type methods often fail due to numerical issues such as mesh-entanglement"* (p.1209).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — 소성 **0 회** (본문 · 참고문헌 제목에만 2 회 — [14] Zhang 2008 · [15] Love · Sulsky 2006).  큰 변형: moving-mesh MPM (≈ FEM) 은 *"not well suited for large deformation problems and can experience mesh entanglement issues. The use of moving-mesh MPM may seem counter intuitive as large deformation problems are one of the main strengths of MPM"* (p.1219) — 그래서 큰 변형은 격자를 매 걸음 되돌리는 standard MPM 이 맡고, 그 대가가 **시간에 따라 바뀌고 쌓이는 노드 적분 오차**다 (*"quadrature errors have a compounding effect on MPM"* p.1218) [카드 해석].  우회 · 비용: 매끈한 기저 (B-spline · 적분 오차 α → α²) · PPC 를 격자와 함께 (1D 입자 O(N²)) · 표 II (B-spline 64 셀 CFL 0.9 가 선형 128 셀 CFL 0.1 보다 오차 263 배 작고 19 배 빠름).  Love · Sulsky [15, 16] 의 에너지 일관 (암시 · 일관 질량) 판은 *"add considerable computational complexity … and hence are not often used in practice"* (p.1210).
3. **2D / 3D** — 1D 만.  기저는 분리형 곱 (식 29 · 3D B-spline p.1215) 으로 다차원 확장 · **1D 결론을 2D/3D 로 옮기는 데 대한 말 없음**.  [카드 해석] PPC 와 α 는 방향마다 (3D 셀당 물질점 = PPC³) · 그림 13b 의 'PPC ∝ N' 을 3D 방향마다 옮기면 물질점 ∝ N⁶ [카드 산술].
4. **압력을 뺄 때의 거동** — **다루지 않았다** (누름 · 뺌 · 판 없음 · 탄성파 주기 운동만).

### 4-5. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| standard MPM | 물질점이 움직이고 격자는 매 걸음 처음 자리로 되돌림 (grid reset) · 물질점이 셀을 넘는다 |
| moving-mesh MPM | 격자가 물질과 함께 움직이는 (완전 Lagrangian) MPM — 실제로는 참조 배치에서 기저를 계산하고 변위만 들고 다닌다 · FEM 에 가깝다 (적분점 = 물질점) |
| 노드 적분 (nodal integration) | 영역 적분을 물질점 값의 합 Σ_p f(x_p)V_p 로 — 준-중점 규칙 |
| 노드 적분 (quadrature) 오차 | 피적분 함수 (∇φ) 의 불연속을 물질점 영역이 걸칠 때 중점 규칙이 내는 오차 · 선형 기저 O(Δx/h) · B-spline O((Δx/h)²) |
| 격자 넘김 (grid crossing) 오차 | 물질점이 셀 경계를 넘을 때 가속도 · 힘이 튀는 것 — 이 논문은 노드 적분 오차로 본다 |
| 시간 도약 (jump) 오차 | 속도장의 꺾임을 한 걸음에 넘을 때의 오차 (두 걸음 적분과의 차) · O(Δt²) |
| 덩어리 질량 (row-sum) | 질량 행렬의 행 합을 대각에 · 분할의 합이면 m_i = ∫ρφ_i |
| 엇갈린 중심차분 (CD) | 속도를 반 걸음에 두는 2 차 명시 적분 — standard MPM 절차에서 v_p 를 반 걸음 앞으로 초기화하면 같다 |
| 국소 절단 오차 (LTE) | 정확한 상태에서 한 걸음만 갔을 때의 오차 — 누적 · 안정 조건 없이 잴 수 있다 |
| 균형점 (transition · inflection point) | 공간 오차 항과 시간 오차 항이 같아지는 Δt |
| α | Δx/h = PPC 의 역수 (식 96) · 식 (81) 에서는 걸음 비율 (다른 뜻) |
| PPC | particles-per-cell · 1D 셀당 물질점 수 |
| 제조해 (manufactured solution) | 원하는 해를 정하고 그 해가 되도록 체적력을 만든 시험 문제 (식 129–131) |

---

## 5. Figure set ★
| 그림 | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| **Fig. 1** (`fig_1.png`) | (a) 참조 (b) standard (셀 넘음) (c) moving-mesh (이상적 자리) 의 물질점 · 격자 | moving-mesh = 진단 모드의 그림 |
| **Fig. 2** (`fig_2.png` · 손 크롭) | standard · 선형 기저에서 한 물질점을 따라간 격자 가속도장 (시간 축) — 격자 넘김마다 튐 · §6.1 막대의 정성 예 (각주 §) | 셀 넘김 튐의 모양 — 우리 판 반력 시계열을 볼 때의 대조 그림 |
| **Fig. 3** (`fig_3.png` · 다시 자름) | (a) 고정 조각 선형 속도장 (b) 입자 위치 x(t) | 도약 오차 단위 시험의 입력 |
| **Fig. 4** (`fig_4.png`) | 한 걸음 ↔ 두 걸음으로 꺾임 넘기 | 도약 오차의 정의 |
| **Fig. 5** (`fig_5.png` · 다시 자름) | 도약 오차 vs Δt (로그) · 2 차 기준선 | 기울기 2.00 [판독] |
| **Fig. 6** (`fig_6.png` · 손 크롭) | (a) Δt₀ – Δt₀/8 의 위치 오차 시간열 · 도약 셋 (b) Δt₀/8 만 | 표 I 대조 (Δt₀ = 10⁻³ 로 맞음) |
| **Table I** (`tab_1.png` · 손 크롭) | 도약 셋의 추정 · 계산 | 추정 상한이 맞는 예 |
| **Fig. 7** (`fig_7.png` · 다시 자름) | g(x) (J = 1) | ∫g = J/12 확인 |
| **Fig. 8** (`fig_8.png` · 다시 자름) | 물질점 영역이 (a) 조각 상수 (선형 ∇φ) (b) 조각 선형 (B-spline ∇φ) 의 꺾임을 걸침 | 노드 적분 오차의 그림 설명 |
| **Fig. 9** (`fig_9.png` · 다시 자름) | 단순 문제 전역 오차 (Δx 1/4 · 1/8 · Δt₀/2 – /16) | Δt 무관 바닥 · Δx 의존 |
| **Fig. 10** (`fig_10.png`) | 1D 주기 막대 물질점 · 영역 (t = 0 · 1/8 · 1/4 주기) | 제조해의 모양 (C = 100 확인) |
| **Fig. 11** (`fig_11.png` · 다시 자름) | 64 셀 · 100 PPC 한 물질점 변위 오차 · 쌓인 도약 오차 | 도약 몫 ≈ 9 % [판독] |
| **Fig. 12** (`fig_12.png` · 다시 자름) | 4 PPC 한 물질점 가속도 · 선형 (튐) ↔ B-spline (연속) ↔ 정해 (실선) | 기저의 효과 · 연속이어도 정해와 13–185 % 차 [판독] · 정해 곡선으로 C = 100 확인 |
| **Fig. 13** (`fig_13.png`) | (a) PPC 고정 격자 사다리 (b) PPC = N/4 | ★ 고정 PPC 사다리의 함정 (U6) |
| **Fig. 14** (`fig_14.png` · 다시 자름) | moving-mesh 가속도 L2 오차 vs 셀 수 | c₁ 측정 (2 차) |
| **Fig. 15** (`fig_15.png`) | moving-mesh 2²⁰ 셀 한 걸음 속도 오차 vs Δt | c₂ 측정 (3 차) |
| **Fig. 16** (`fig_16.png` · 다시 자름) | moving-mesh 2048 셀 — 기울기 1 → 3 전이 | 균형점 확인 |
| **Fig. 17** (`fig_17.png` · 다시 자름) | standard 가속도 L2 오차 (선형 2 · 4 · 6 PPC · B-spline 4 PPC) | standard 선형의 1 차 꼬리 |
| **Fig. 18** (`fig_18.png`) | standard 2²⁰ 셀 한 걸음 속도 오차 — 큰 Δt 3 차 · 작은 Δt 평탄 | 평탄 = Δt 무관 공간 오차 |
| **Fig. 19** (`fig_19.png`) | standard 2048 셀 전이 | 균형점 (선형 교차 +38 % [판독]) |
| **Table II** (`tab_2.png` · 손 크롭) | 두 설정의 RMS 오차 · 실행 시간 | ★ 권고 시연 |
| 식 크롭 138 (`eq_001_…` – `eq_138_…`) · 근거 문단 20 (`txt_p*`) | 식 (1)–(138) 전부 · 인용 문장 | 보고서 MPM 절 붙임 |

## 6. Post-processing ★
- **오차 노름**: 한 주기 뒤 RMS 변위 오차 (그림 13 · 표 II — 식 [미확인]) · 격자 가속도 L2 (식 133 · 연속 적분) · 한 걸음 뒤 격자 속도 L2 (그림 15–19 — 식 [미확인] · 그림 15 는 연속 L2 해석값과 맞는다 [카드 산술]) · 단순 문제 = 정확해와의 위치 차 절댓값 (그림 9) · 도약 = 두 걸음 − 한 걸음 (식 86) · 쌓인 도약 = 그 합 (그림 11).
- **상수 추출**: 수렴 구간의 한 점으로 c₁ = ε_a/h^p · c₂ = ε_v/Δt³ (식 135–138).
- **균형 예측**: Δt = √(c₁/c₂)·h^{p/2} → 다른 해상도 (2048 셀) 의 Δt 사다리에서 기울기 전이 확인.
- **판독 (이 카드)**: PDF 벡터 경로 — digitized.csv note 열에 방법 전부 · 인쇄 점 재현 (그림 14 · 15 · 17 · 18 의 인쇄값: 판독/인쇄 1.0002 · 1.0018 · 1.0014 · 1.0011 [카드 산술]) · 점근선 교차 = 작은 Δt 기울기 1 · 큰 Δt 기울기 3 계수의 교점 · 그림 12 정해 = PDF 의 3 차 Bézier 4 조각을 t 에서 평가.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 다른 카드 · CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 하중 · 이산화가 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| 이산화 | standard / moving-mesh MPM · 선형 · 2차 B-spline · ∇φ 내부력 · 덩어리 질량 · Forward-Euler / CD | MLS-MPM · APIC · 2차 B-spline · 명시 · f32 [다른 카드 `hu2018_…` L498 (우리 코드 판독)] | 기저 = 같은 2차 B-spline (C¹) · 힘 식 다름 (MLS) · 전달 다름 (APIC ↔ FLIP 증분) — C₂ = ⅛ · α² 는 **∇φ 노드 적분** 의 값이라 우리 MLS 힘에 그대로 옮기지 않는다 |
| 시간 적분 | Forward-Euler (18–22) · v_p 를 반 걸음 앞으로 두면 엇갈린 CD (23–27) | P2G 에서 격자 운동량에 dt·f (MLS 힘) → 격자 속도 → G2P (APIC) → F → J2 반환 → x += dt·v [다른 카드 `hu2018_…` L26–L31 (우리 코드 판독)] | 같은 갱신 꼴 (갱신된 격자 속도로 위치) → 정지에서 출발하면 사실상 CD [카드 추론] · 시간 차수는 우리 코드로 재야 한다 |
| 셀당 물질점 | 1D 2–100 · 주 시험 4 | 방향당 2 (셀당 8) [다른 카드 `homel2017_…` L499 · `sadeghirad2011_…` L516] | α = ½ (방향당) — 1D 상한 비 (식 95 ÷ 94) B-spline/선형 = α/2 = ¼ [카드 산술 · 1D 상수 응력 한정] |
| 시간 간격 | 그림 11 · 표 II CFL 0.1 · 0.9 · 균형 CFL 4.1–10.5 [카드 산술] | dt = 0.4 dx/√M (ρ = 1 규약) + 판 Mach [다른 카드 `gritton2017_…` L538 (우리 코드 판독)] · M 의 뜻 [미확인] (`steffen2008_…` §7-1) | M 이 P파 계수면 Courant 0.4 — 이 논문의 균형 CFL (≈4) 의 1/10 이면 시간 국소 오차 몫 ≈1 % [카드 산술 · 그 문제의 상수 전제 · 우리 문제로 옮기지 않는다] |
| 격자 해상도 | h = 1/4 – 1/8192 · 2⁻²⁰ (무차원 막대 [0, 1] · 해의 파장 1) | dx 0.141 µm (n_grid 384) · SE 지름 ≈ 1 µm ≈ 7 셀 [다른 카드 `sadeghirad2011_…` L517] · d_h/dx ≳ 3.5 규칙 [우리 기록 · CLAUDE.md] | 이 논문은 h 를 해의 매끈함에만 견준다 — 알갱이 · 틈 길이 대비 규칙 없음 |
| 격자 수렴 | 가속도 L2 · 2 차 (moving-mesh · B-spline) · 1 차 (standard 선형) · 고정 PPC 선형 = 최소 뒤 증가 (그림 13a) | 좁은 · 넓은 침대 SE 응력 비 (φ 0.72) 128 → 192 → 288 증분 0.170 · 0.163 · 겉보기 차수 ≈ 0.10 (미수렴) [우리 기록 · CLAUDE.md] | 우리 비수렴의 후보 둘 — 기하 해상 (좁은 채널) ↔ 고정 PPC 적분 바닥 — 을 가를 대조 (§8 U6) [카드 추론] |
| Δt · 재하 결합 | Δt 만 바꾼다 (해 = 제조해 · 그대로) | `--sub` 40/80/160 (속도 사다리 · 같은 변형 이력) → 정착 기공 14.38 / 12.76 / 11.08 % (미수렴) [우리 기록 · 비교 문서 F 절] · n_grid > 391 에서 CFL 이 dt 를 물어 판 속도가 바뀜 (512 가 384 보다 31 % 빠름 → `--platen-mach`) [우리 기록 · CLAUDE.md] | 이 논문은 Δt 를 **해와 떼어** 바꾼다 — 우리 쪽은 dt · 판 속도 · 해상도가 엮인 적이 있다 → 축마다 따로 (§9) |
| 재료 | 1D neo-Hookean · E 10⁴ · ρ₀ 1 · ν 0 (무차원) | MPM J2 · E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 · μ 0.51 GPa) · DEM E_eff 1.35 GPa (18 배 연화) · Heckel P_y 138 MPa [우리 기록] | 소성 · 거의 비압축 · 접촉 없음 → 수치 크기 전이 불가 |
| 하중 | 체적력 제조해 · 탄성파 동역학 · 한 주기 | 판 압축 ≈ 300 MPa · 판 Mach 0.01–0.03 (준정적) [우리 기록] | 하중 꼴 · 시간 척도 다름 |
| 오차 추정 | 해석 모형 + 제조해 + 한 걸음 국소 오차 + 균형 예측 | 해석해 단위 시험 없음 · 격자 · 속도 사다리 [우리 기록 · 비교 문서 F 절] | ★ U2 · U6 에 바로 쓸 절차 (§9) |

### 7-2. ★ "안정 한계 근처면 충분" 을 우리 압밀에 들일 때
- 쓸 수 있는 것: 명시 MPM 에서 Δt 를 안정 한계 아래로 더 줄여도 시간 오차가 공간 오차 아래라 답이 거의 안 바뀌는 영역이 있다 — **그 영역인지는 시험으로** (Courant 계수만 반으로 · 판 Mach · 격자 · PPC 고정).
- 붙일 꼬리표: 1D · 탄성 · 매끈한 제조해 · 중심차분 · 균형 CFL 4–10 은 그 문제의 상수 · 접촉 · 소성 반환 · 판 서보 같은 비매끈 사건은 이 분석 밖.
- 쓰지 말 것: 우리 속도 사다리 (`--sub` · 판 Mach) 의 변화를 '시간 이산 오차' 로 읽는 것 (재하 속도 = 물리 · 관성) · 이 논문의 c₁ · c₂ · 균형 Δt 숫자.

### 7-3. ★ 고정 PPC 사다리 ↔ 우리 격자 사다리
- 이 논문 (1D · 선형 기저): 고정 PPC 사다리는 최소 뒤 커진다 (그림 13a · 128 → 1024 셀 3.0–9.5 배 [판독]) · B-spline 은 적분 오차가 α² 로 작아 같은 범위에서 2 차에 가깝다 (그림 14 · 17 · 고운 끝 1.6–1.7 [판독]).
- 우리 (2차 B-spline · 방향당 2 PPC 고정 [다른 카드]): 격자 사다리의 비수렴 (≈0.10) 후보에 '고정 PPC 적분 바닥' 을 넣고 같은 침대를 **PPC (방향당 2 · 3) × 격자 둘**로 엇갈려 가른다 — `bardenhagen2004_…` §9 · `steffen2008_…` §9 행동 4 와 같은 권고 [다른 카드].

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = MPM 의 **수치 오차** 반쪽 (우리 MPM = MECHANICS 쪽의 신뢰 구간을 정하는 절차).  DEM 쪽 · 수송 쪽은 없다.
- 없는 것: 접촉 · 다물체 · 소성 · 거의 비압축 · 압밀 · 탈압 · 2D/3D.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md · 다른 카드: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM MLS-MPM · 2차 B-spline · 방향당 2 PPC · E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 = **재료 없는 1D 탄성 수치 해석** — 랩 표준과 나란히 놓을 숫자는 하나도 없다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ **수치 판정의 결과 전 등록 꼴**: 오차 꼴 (식 122 · 126) 을 먼저 적고 상수를 한 점에서 재 균형 Δt 를 예측 → 다른 해상도 (2048 셀) 에서 확인 (그림 16 · 19) · 표 I = 추정 상한 ↔ 측정.  반면교사: *"precisely"* 를 눈 대조로만 (판독 +38 %) · Δt₀ · 시각 · ∫g 의 인쇄 어긋남 → 등록 칸에 **노름 식 · 평가 시각 · CFL 식 (어느 파속) · 예측 허용폭** 을 둔다 | 기공 연산자 · 압밀 판정 없음 |
| **단계 1** (3D 메모리 · 장 수) | 비용 감각만: 선형 기저로 일관되려면 PPC ∝ N → 1D 물질점 O(N²) (*"prohibitive"* p.1235) · 3D 방향마다면 ∝ N⁶ [카드 산술] → 매끈한 기저로 PPC 를 고정할 수 있게 하는 편이 메모리 쪽 해법 [카드 추론] · 표 II 실행 시간 9.62 ↔ 0.50 s (1D) | 3D 메모리 · 입자별 장 수 없음 |
| **단계 2** (2D MPM 코드 · 단위 시험) | ★★ **이 논문의 몫** — ① 1D 주기 막대 제조해 (식 129–132 · A 0.05 · E 10⁴ · ρ₀ 1 · C 100 [카드 산술]) 에서 **격자 가속도 L2 오차 (식 133) 를 t = 0.2122/C 한 시각에** 재는 공간 시험 + **한 걸음 격자 속도 오차** 의 시간 시험 → c₁ · c₂ → 균형 Δt 예측 · 확인 ② 도약 오차 단위 시험 (고정 조각 선형 속도장 · 마디를 걸음 가운데 · 기울기 2 · 표 I 상한) ③ 노드 적분 시험 (불연속 g · 물질점 영역 중점 · Δt 무관 바닥) ④ moving-mesh 모드 = 노드 적분 · 격자 넘김을 끈 진단판.  `steffen2008_…` §9 의 같은 막대 (T = 1/C · Δt 4×10⁻⁶ · 8–512 셀) 와 함께 쓰면 공간 차수 + 시간 차수 + 균형점을 한 막대로 [카드 추론] | 2D 계산 · 소성 · 거의 비압축 · 판 경계 시험 없음 |
| **단계 3** (2D 접촉 표현 비교) | 없음 (접촉 0 회).  두 접촉 표현을 견줄 때 Δt 를 같은 Courant 로 두는 근거 정도 — '안정 한계 근처면 시간 오차가 판정을 가르지 않는다' 가 접촉 문제에서도 서는지는 확인 대상 [카드 추론] | 접촉 · 다물체 없음 |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 경고: 맞출 때 쓴 격자 · PPC 의 적분 오차가 σ_y 에 흡수된다 — 고정 PPC 는 격자를 조여도 전역 오차가 안 준다 (p.1240) → σ_y 맞춤 전 PPC × 격자 엇갈린 수렴 · Δt 는 안정 한계 근처 (줄여도 이득 없음 · p.1240).  우리 σ_y 0.30 GPa 는 n_grid 384 · 방향당 2 PPC 에서 정했다 [우리 기록 · 다른 카드] | 순수 SE · 항복 · 기공 없음 · 랩 표준 (10–13 % · 1.64 g/cm³) 과 견줄 숫자 없음 |
| **단계 5** (3D 복합 압밀) | 큰 변형 = standard MPM 영역 → 노드 적분 오차가 시간에 따라 바뀌고 쌓인다 (p.1218) · 매끈한 기저 (우리 2차 B-spline) 가 그 몫을 α → α² 로 줄인다 (식 113) · 쌓인 오차는 해 둘레에서 진동할 수 있다 (p.1230) — 프레임별 값의 흔들림을 물리로 읽기 전에 그 크기를 잰다 [카드 추론] | 복합 · AM 마스크 · 하중 몫 없음 |
| **단계 6** (탈압 · 되돌아옴) | 없음 — 단, 되돌아옴 (springback) 은 큰 두 상태의 작은 차라 같은 해상도 · PPC 의 수치 오차 바닥 (식 112–113 의 Δt 무관 항 꼴) 을 먼저 재고 견준다 [카드 추론] | 누름 · 뺌 · 판 없음 |
| **단계 7** (형상 · 피복 · 수송) | 없음 | — |
| **후보 D0** (지금 DEM) | 없음 (DEM 0 회) | — |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 없음 (주기 경계만 · 경계 처리는 `steffen2008_…` 의 몫) | — |
| **후보 A** (MPM 강체 AM + SE 한 속도장) | SE 연속체 쪽의 기저 · PPC · Δt 규칙 (위 단계 4–5) · moving-mesh 진단 (AM 이 정지 장애물이면 SE 물질점만 셀을 넘는다 — AM 둘레 적분 오차는 이 논문 밖) | 강체 · 장애물 경계 없음 |
| **후보 A′** (입자별 속도장) | 없음 (한 물체) | — |
| **후보 B** (입자별 FE + 접촉) | ★ 인용할 문장: FE 형 방법은 큰 변형에서 *"often fail due to numerical issues such as mesh-entanglement"* (p.1209) · moving-mesh MPM (≈ FEM) 도 *"not well suited for large deformation problems and can experience mesh entanglement issues"* (p.1219) — 입자별 FE 의 큰 변형 위험에 대한 MPM 쪽 진술 (수치 문턱 없음) | 입자별 FE 계산 없음 |
| **후보 C · C′** (큰 변형 · 탄소성 접촉 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀) | 없음 | — |
| **U0–U6** | **U0** 꼴 '0 이어야 하는 양': ∫g = 0 이면 외부 가속도 0 (p.1227) — ⚠ 인쇄 값으로는 J/12 (§3-4) · **U1**: 지름당 셀 내용 없음 · 쓸 것 = 한 시각 공간 오차 사다리의 꼴 (그림 14 · 17) · **U6**: ★ 절차 — 공간 (한 시각) · 시간 (한 걸음) 오차를 따로 재고 c₁ · c₂ → 균형 Δt · 격자 × PPC 엇갈림 (그림 13) · Δt 는 안정 한계 근처 | U2 (경사면 마찰) · U3 · U4 · U5 없음 |
| **R1–R7** | 없음 (1D 탄성 한 물체 · 접촉 · 미끄럼 · 경계 기억 · 탈압 · 형상 · 파괴 0 회) | — |
| **결과 전 대조 항목** | ① 우리 MLS-MPM 으로 이 1D 주기 막대 (A 0.05 · E 10⁴ · ρ₀ 1 · 4 PPC · 주기) — 격자 가속도 L2 오차 (식 133 · t = 0.2122/C) 의 기울기 2 (moving-mesh 판 2.000 [판독] · standard B-spline 고운 끝 1.6–1.7 [판독]) · 한 걸음 속도 오차 3 차 · c₂ = (1/24)A(Cπ)⁴\|cos(0.2122π)\|/√2 = 1.13×10⁷ (해의 성질 · CD 면 같은 값) [카드 산술] ② 균형 Δt 의 CFL (이 논문 4.1–10.5 [카드 산술]) ↔ 우리 Courant 0.4 ③ 우리 압밀 침대에서 Courant 계수만 0.4 → 0.2 (판 Mach · 격자 · PPC 고정) — 이 논문 결론대로면 정착 기공 · wallP 가 바뀌지 않아야 한다 (바뀌면 시간 이산 밖의 결합) — 맞추는 데 쓰지 않음 | 랩 표준 순수 SE (10–13 % · 1.64 g/cm³) 와 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: 재료 없음 (무차원 neo-Hookean · E 10⁴ · ρ₀ 1 · ν 0) ↔ 우리 MPM J2 소성 · E 1.53 GPa · ν 0.49 (거의 비압축) · DEM E_eff 1.35 GPa · 1D ↔ 우리 3D 무질서 침대 · 탄성파 동역학 · 매끈한 제조해 ↔ 준정적 판 압축 (≈300 MPa · 판 Mach 0.01–0.03) · 접촉 · 서보 · 소성 반환 · 고른 물질점 배치 · 한 물체 ↔ DEM 덤프 씨앗 · AM 마스크 + SE.  ⇒ 값은 하나도 옮기지 않고 **오차 모형의 꼴 · 시험 절차 · 기저 / PPC / Δt 규칙의 방향**만 옮긴다.

## 9. 적용 인사이트 (행동)
1. **단위 시험 (단계 2 · U6) = 공간 · 시간 따로**: 1D 주기 막대 (식 129–132) 를 우리 MLS-MPM 에 넣어 ① 한 시각 (t = 0.2122/C) 격자 가속도 L2 오차의 h 사다리 (128–2048) ② 2²⁰ 에 가까운 고운 격자에서 한 걸음 속도 오차의 Δt 사다리 → c₁ · c₂ · 균형 Δt 를 결과 전에 등록하고 중간 해상도에서 기울기 1 → 3 전이를 확인한다.  `steffen2008_…` §9 의 전역 RMS 시험과 같은 막대.
2. **Courant 반감 팔 (단계 4–6 의 사전 점검)**: 압밀 침대 하나에서 Courant 계수만 0.4 → 0.2 (판 Mach · 격자 · PPC · 서보 고정) — 정착 기공 · wallP · 두께가 같으면 '안정 한계 근처면 충분' 이 우리 문제에서도 선다.  다르면 그 차가 시간 이산 오차인지 판 · 서보 결합인지 따로 본다.
3. **격자 × PPC 엇갈린 사다리**: 우리 격자 사다리 (128 · 192 · 288 · 384) 를 PPC (방향당 2 · 3) 와 엇갈려 — 고정 PPC 적분 바닥과 기하 해상 (d_h/dx) 을 가른다.
4. **보고 칸**: 노름 식 · 평가 시각 · CFL 식 (어느 파속) · 반 걸음 초기화 여부 · 예측 허용폭 — 이 논문의 인쇄 어긋남 (Δt₀ · t · ∫g) 이 그 칸이 비어 생겼다.
5. **흐름 밖**: 없음 (수송 · 접촉망 · 계면 저항과 닿는 내용 없음).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In explicit MPM, the time-step that balances spatial and temporal errors can be estimated from two measured constants — Δt = √(c₁/c₂)·h for second-order spatial error and √(c₁/c₂)·√h for standard MPM with piecewise-linear basis functions; for a 1-D elastic bar this balance lies well above the stability limit, so time-steps near the stability limit already give spatially dominated solutions (Steffen, Kirby & Berzins, *Int. J. Numer. Meth. Engng* 82 (2010) 1207–1243)."
- "With piecewise-linear basis functions and a fixed number of particles per cell, MPM quadrature errors are not reduced by grid refinement; the number of particles per cell must increase with the number of grid cells, whereas quadratic B-splines reduce the quadrature error from O(Δx/h) to O((Δx/h)²) (Steffen et al., 2010)."
- 국문 (한정어와 함께): *"명시적 MPM 에서는 안정 한계 근처의 시간 간격이면 충분하고 더 줄여도 공간 오차가 지배해 답이 거의 바뀌지 않는다 (Steffen 외 2010 · 1D 탄성 막대 · 균형 Δt 가 안정 한계의 4–10 배 [카드 산술]) — 셀당 물질점을 고정한 채 격자만 조이면 선형 기저에서는 오차가 줄지 않는다."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**: §3-8 의 1–4.
**카드가 본 한계**
1. **1D · 탄성 · 매끈한 해 · 주기 경계** — 접촉 · 판 경계 · 소성 · 큰 변형 (standard 의 실제 큰 변형) · 2D/3D 미검증.
2. 상수 · 균형 CFL 은 그 문제의 값 (A · E · 기저 · PPC) — 숫자 전이 금지.
3. *"precisely"* · B-spline '2 차' 는 판독과 어긋난다 (§3-6).
4. 원문 안 어긋남 (Δt₀ · t · ∫g · DOI · [12] 권) — 인용 때 표지.
5. 노름 · CFL 식 미인쇄 — 우리 코드로 다시 재기 전에는 값 비교 불가.
6. 우리 MLS-MPM 의 힘 식 · APIC 는 이 논문 (∇φ · FLIP 증분) 과 달라 C₁ · C₂ 같은 상수가 그대로 안 온다.
7. 그림 9 · 13 의 '오차가 커진다' 는 1D 선형 기저 결과 — 우리 B-spline 에서 같은 일이 생기는지는 시험해야 한다.
8. 그림 15 · 16 의 절대 크기 차 (228 배) · 그림 15 의 작은 Δt 오름 · 그림 18 평탄의 원인은 원문에 없다 — 카드 해석은 해석일 뿐.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| [18] | Lawson J, Berzins M, Dew PM. Balancing space and time errors in the method of lines for parabolic equations. SIAM Journal on Scientific and Statistical Computing 1991; 12(3):573–594. | ★ 식 (1) 균형 모형 · 오차 제어의 원전 — 카드 없음 |
| [11] | Steffen M, Kirby RM, Berzins M. Analysis and reduction of quadrature errors in the material point method (MPM). International Journal for Numerical Methods in Engineering 2008; 76(6):922–948. DOI: 10.1002/nme.2360. | ★ 식 (93)–(95) (C₁ ½ · C₂ ⅛) 의 원 분석 — 카드 없음 (wishlist 에 있음) |
| [7] | Wallstedt PC, Guilkey JE. An evaluation of explicit time integration schemes for use with the generalized interpolation material point method. Journal of Computational Physics 2008; 227(22):9628–9642. | ★ 이 논문이 설명하려는 '시간 0 차 수렴' 관측 · USF · USL · CD 비교 — 카드 없음 (wishlist 에 있음) |
| [3] | Brydon AD, Bardenhagen SG, Miller EA, Seidler GT. Simulation of the densification of real open-celled foam microstructures. Journal of the Mechanics and Physics of Solids 2005; 53:2638–2660. | 실제 미세구조를 MPM 으로 치밀화 · *"ease of initial discretization of complex geometries"* (p.1215) — 정본 `bardenhagen2005_…` (같은 권 597–617) 와 **다른 논문** · 카드 없음 |
| [4] | Nairn JA. Numerical simulations of transverse compression and densification in wood. Wood and Fiber Science 2006; 38(4):576–591. | MPM 셀 구조 압축 · 치밀화 — 카드 없음 (정본 `nairn2015_…` 는 다른 논문) |
| [22] | Tran LT, Kim J, Berzins M. Solving time-dependent PDEs using the material point method, a case study from gas dynamics. International Journal for Numerical Methods in Fluids 2009; DOI: 10.1002/nme.2360. | 도약 오차 식 (76) 의 출처 · ⚠ 인쇄 DOI = [11] 의 DOI (오기로 보임) · wishlist 에 2007 기술 보고서 판 |
| [17] | Bardenhagen S. Energy conservation error in the material point method for solid mechanics. Journal of Computational Physics 2002; 180:383–403. | 명시 갱신 순서 시험 — wishlist 에 있음 |
| [15] · [16] | Love E, Sulsky DL. An energy-consistent material-point method for dynamic finite deformation plasticity. International Journal for Numerical Methods in Engineering 2006; 65(10):1608–1638. · Love E, Sulsky DL. An unconditionally stable, energy-momentum consistent implementation of the material-point method. Computer Methods in Applied Mechanics and Engineering 2006; 195(33–36):3903–3925. | 에너지 일관 · 무조건 안정 MPM (소성) — [15] 는 wishlist 에 있음 (그 줄 연도 2005) |
| [21] | Guilkey JE, Weiss JA. Implicit time integration for the material point method: quantitative and algorithmic comparisons with the finite element method. International Journal for Numerical Methods in Engineering 2003; 57(9):1323–1338. | 정본 카드 있음 (`guilkey2003_implicit_mpm_newton_quasistatic_fem_comparison`) |
| [10] · [12] | Bardenhagen SG, Kober EM 2004 (CMES 5(6)) · Steffen M, Wallstedt PC, Guilkey JE, Kirby RM, Berzins M 2008 (CMES — 이 목록은 32(2) · 원문은 31(2)) | 정본 카드 있음 (`bardenhagen2004_…` · `steffen2008_…`) |
| [1] | Sulsky D, Chen Z, Schreyer HL. A particle method for history-dependent materials. Computer Methods in Applied Mechanics and Engineering 1994; 118:179–196. | 후보 표 N-40 |

## 13. [미확인] 목록 (본문 37 쪽 전수에 없음)
1. CFL 의 식 (어느 파속 — 이 카드는 cΔt/h · c = √(E/ρ₀) 로 계산).
2. 'RMS displacement error' (그림 13 · 표 II) 와 'L2 errors in the grid velocity' (그림 15–19) 의 식 (합 · 정규화).
3. §6.3 · §6.4 · 표 II 의 A · E · 최종 시각 T (그림 15 의 c₂ 해석값으로 A 0.05 · C 100 이 맞는다 · 그림 12 정해 곡선 = C 100 [카드 산술]).
4. 그림 5 의 마디 · 속도장 · 그림 9 의 Δt₀ · J (그림 7 은 J = 1 로 그림).
5. 그림 15 · 16 의 절대 크기 228 배 차이 · 그림 15 작은 Δt 의 오름 · 그림 18 평탄의 원인.
6. 2차 B-spline 의 c₁ (원문 미인쇄 · 이 카드가 균형 Δt 에서 역산).
7. 실행 기계 · 코드 이름 · 실행 시간 (표 II 밖).
8. 3차 B-spline 식 (`stomakhin2013_…` L64 의 'Steffen et al. 2008' 원전 — 이 논문에도 없음).
9. 그림 9 의 기준해 (a_e = 0 인지 · ∫g = J/12 와의 관계).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 본문 37 쪽을 글자 층 추출 + 전 쪽 렌더로 읽음.  서지 = 첫 쪽 머리 (학술지 · 권 · 쪽 · DOI · 온라인 날짜) · 접수 / 수정 / 수락 · 교신 · 연구비 (p.1207) · 호 = 쪽 옆 내려받기 배너.  원문 낱말 셈: DEM · discrete element · contact · granular · powder · compaction · unload = 0 · plastic 본문 0 (참고문헌 제목 2) · '1-D' 18 · 'three-dimension' 2 (기저 문장) · 'stability limit' 5 · 'implicit' 7.
- 그림 크롭 **179 장** = 도구 17 (Fig. 1 · 3–5 · 7–19) 중 **다시 자름 10** (Fig. 3 · 7 · 8 · 9 · 14 · 17 = 쪽 머리글 섞임 · Fig. 5 = 가로축 이름 'Δt' 잘림 · Fig. 11 = 도구 크롭에 같은 쪽 Fig. 12 그래프가 들어감 · Fig. 12 · 16 = 앞 그림 캡션 끝줄 섞임) + 그대로 7 + 손 크롭 162 (Fig. 2 · 6 = 도구 '영역 없음' · Table I · II = 로마 숫자 라벨이라 도구가 놓침 · 식 138 · 근거 문단 20).  식 (74) 는 윗줄 아래첨자 조각이 섞여 한 번 다시 자름 · 식 (81) · (96) 은 파일 이름의 그리스 문자 오기 (theta · zeta → alpha · gamma) 를 고침.  전부 Read 로 열어 확인 (식 · 문단은 12 · 4 장씩 묶은 검토 그림으로) · `figures.json` 의 `recrop` · `manual_crop` · `note_manual`.
- 판독: digitized.csv 250 행 — 각 그림의 축 보정 · 표지 판독 방법을 note 열에.  인쇄 점 재현 (그림 14 · 15 · 17 · 18 = 판독/인쇄 1.0002 · 1.0018 · 1.0014 · 1.0011) · 표 I ↔ 그림 6b 도약 (1.79 · 7.50 · 18.2 ×10⁻⁸ [판독] ↔ 1.81 · 7.60 · 18.4).
- 산술 확인: c₁ = 1.7895×10⁻² × 1024² = 1.8764×10⁴ ✓ · c₂ 해석값 1.1277×10⁷ ✓ · Δt_bal = √(c₁/c₂)·h = 1.99176×10⁻⁵ ✓ · standard 5.1196×10⁻⁵ ✓ · 식 (131) 유도 ✓ · 표 I 추정 = Δt 1.25×10⁻⁴ ✓ · 마디 넘는 시각 3 개 ✓ · ∫g = J/12 (원문 '0' 과 다름).
- 2 차 인용 대조: `gritton2017_…` L91 · `steffen2008_…` L131 · L411 · 후보 표 L61 서지 칸 — 고치지 않았다 (카드 문제 = 정독 출력 batch_78 의 "카드 문제" 절).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (555 장 · 이 카드 전) + DOI 'nme.2787' · 제목 'Decoupling and balancing' · 'steffen' grep — 카드 없음 (`steffen2008_…` = 다른 논문 · CMES).

## 🔗 관련 카드
- 같은 Utah 무리 · MPM 수치 검증: `steffen2008_mpm_implementation_choices_gimp_bspline_boundary` (ref. [12] · 같은 1D 막대 · 경계 처리 · 기저) · `guilkey2003_implicit_mpm_newton_quasistatic_fem_comparison` (ref. [21] · 암시 MPM) · `gritton2017_mpm_chemomechanical_coupling_silicon_anode` (이 논문을 ref. [36] 으로 인용) · `bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing` (ref. [10] · 셀 넘김 잡음) · `bardenhagen2005_mpm_foam_densification_simulation` (같은 권 다른 논문).
- 우리 MPM 이산화 · 해상도 · 시간 간격: `hu2018_mls_mpm_cpic_two_way_rigid_coupling` · `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` · `sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability` · `nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions` · `devaucorbeil2020_mpm_after_25_years_review`.
- MPM 압밀 (변형 입자): `nezamabadi2022_mpm_cd_plastic_particle_compaction` · `nguyen2017_mpm_bpm_deformable_particle_compaction` · `stomakhin2013_mpm_snow_elastoplastic`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
