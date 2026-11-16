<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 후보 표 N-40 · 정독 81 · 11-12 대피 세션이 본 세션에서 넘겨받은 1 순위 후보) 에서 꼭 뽑으라고 한 항목.
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 상자 · §0-1 고른 의도 대조 · §8 자세한 분석) · steffen2010_mpm_space_time_error_balance_moving_mesh.md (MPM 수치 카드의 꼴 · 우리 MPM 값의 [다른 카드] 출처).
     원문 = 출판본 (Comput. Methods Appl. Mech. Engrg. 118 (1994) 179–196 · 18 쪽 · SI 없음).  스캔 PDF — 쪽마다 1-bit 영상 한 장 (홀수 쪽 400 dpi · 짝수 쪽 300 dpi) + OCR 글자 층 (식은 OCR 이 깨져 있어 전 쪽 렌더에서 옮겼다).
     쪽 표기 = "p.NNN" 은 학술지 인쇄 쪽 (179–196).  크롭 파일 이름의 pN 과 figures.json 의 page 는 PDF 쪽 = 인쇄 쪽 − 178 (figures.json 에 journal_page 도 적었다).
     값 표지: [인쇄] = 본문 · 식 · 표 · 캡션에 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 144 행 — 스캔 원 해상도로 렌더한 화소에서 축선 옆 눈금을 찾아 최소제곱 보정 · 그림 3 은 스캔이 1–2° 돌아 2D 아핀 보정 · 그림 4a 는 점 (연결 성분) 을 세어 두 원판으로 가름 — 방법은 note 열) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [카드 추론] = 우리 계획으로 옮긴 추론 · [다른 카드] = 정본의 다른 카드에 적힌 값 (slug · 줄) ·
     [우리 기록] = 우리 쪽 값 (지시서 · 비교 문서 · 다른 카드가 옮긴 우리 코드 판독) · [미확인] = 원문 18 쪽 전수에 없음.
     원문 18 쪽은 글자 층 + 전 쪽 렌더로 전부 읽었다.  DEM · 알갱이 · 분말 · 압밀 · 마찰은 없다 — 2D 연속체 물체 (원기둥 · 원판 · 막대 · 층) 의 입자법 계산. -->
# MPM 의 원전 — 이력 의존 (소성) 재료의 상태 (소성 변형률 · 경화 변수) 를 물질점에 싣고 운동량은 매 걸음 다시 까는 격자에서 푸는 PIC/FLIP 확장: 혼합 약형 (3.2) · 물질점 = Dirac 점 질량 (3.4) · 사상 행렬 S_Pi = N_i(X_P) (3.7) · 일관 → 행 합 대각 질량 · FLIP 가중 최소제곱 사상 (4.3) · 12 단계 명시 알고리즘 (6.1–6.7) · 한 속도장 = 특별한 알고리즘 없는 no-slip 충돌 · 2D 예 여섯 (강체 회전 · 탄성 원기둥 진동 · 탄성 원판 충돌 · 막대 튕김 · 탄소성 원판 충돌 · 탄성 ↔ 경화 원판) — Sulsky · Chen · Schreyer (CMAME 1994)

> slug `sulsky1994_mpm_particle_method_history_dependent_materials` · DOI `[미확인]` (첫 쪽 · 머리글에 인쇄 없음 · PDF 문서 정보 제목 `PII: 0045-7825(94)90112-0` · 첫 쪽 아래 `SSDI 0045-7825(94)00033-J`) · type `particle (material point) method formulation + 2D numerical examples (small-deformation rate-form elastoplasticity · explicit time integration · consistent → row-sum lumped grid mass · FLIP weighted-least-squares point→grid map · single-valued grid velocity field = automatic no-slip contact · plane strain · dimensionless elastic / von Mises linear-hardening disks + copper elastic cylinder — 실험 · 압밀 · 알갱이 · 3D 계산 없음)` · PDF `79001f63-40._A_particle_method_for_history-dependent_materials.pdf` · SI 없음 · digested `2026-11-12` · status ✅
>
> **저자**: **D. Sulsky** (a · Department of Mathematics) · **Z. Chen** (b · New Mexico Engineering Research Institute) · **H.L. Schreyer\*** (c · Department of Mechanical Engineering) — University of New Mexico, Albuquerque, NM 87131, USA — \* Corresponding author (전자우편 인쇄 없음) · *Comput. Methods Appl. Mech. Engrg.* **118** (1994) **179–196** (18 쪽) · Received 10 June 1993 · Revised manuscript received 15 February 1994 · 0045-7825/94/$07.00 © 1994 Elsevier Science S.A. · 연구비 = Sandia National Laboratories (Contract No. AC-1801) · National Science Foundation (Contract No. DMS-9102975) · 키워드 없음.
> **이웃 카드 (링크만)**: [`bardenhagen2005_mpm_foam_densification_simulation`](bardenhagen2005_mpm_foam_densification_simulation.md) (가리킨 카드 · §4-1 L278 계보) · [`bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing`](bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing.md) (L283 — 이 논문의 식을 GIMP 의 특수형으로 '정확히 회복') · [`bardenhagen2000_mpm_granular_multibody_frictional_contact`](bardenhagen2000_mpm_granular_multibody_frictional_contact.md) (Sulsky 공저 · 이 논문이 열어 둔 *"relaxation of the no slip condition"* 을 푼 다물체 장) · [`guilkey2003_implicit_mpm_newton_quasistatic_fem_comparison`](guilkey2003_implicit_mpm_newton_quasistatic_fem_comparison.md) (ref. 1 · 명시 MPM 복습) · [`steffen2008_mpm_implementation_choices_gimp_bspline_boundary`](steffen2008_mpm_implementation_choices_gimp_bspline_boundary.md) · [`steffen2010_mpm_space_time_error_balance_moving_mesh`](steffen2010_mpm_space_time_error_balance_moving_mesh.md) (ref. [1]) · [`devaucorbeil2020_mpm_after_25_years_review`](devaucorbeil2020_mpm_after_25_years_review.md) (25 년 리뷰) · [`hu2018_mls_mpm_cpic_two_way_rigid_coupling`](hu2018_mls_mpm_cpic_two_way_rigid_coupling.md) (우리 MLS-MPM 코드 판독).
> **판독 원자료**: `litdb/figures/sulsky1994_mpm_particle_method_history_dependent_materials/digitized.csv` (144 행 — 그림 3a–c 총 에너지 봉우리 + 요약 · 그림 4a 점 · 원판 크기 · 중심 거리 · 그림 5 · 8 · 10 에너지 · 운동량 · 운동 에너지가 총에서 떨어지는 시각) · 그림 크롭 **68 장** (도구 7 = **전부 다시 자름** · 손 크롭 61 = 그림 3 (Fig. 2 · 6 · 7) · 표 1 · 식 37 (식 번호마다 하나 · 400 dpi) · 근거 문단 20) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 관통 · 충돌 · 큰 회전처럼 구성식이 **이력에 의존**하는 문제는 물질점을 따라가야 하는데 Euler 격자는 그것이 어렵고, 순수 Lagrange 격자는 뒤틀려 강성 행렬이 나빠지고 (*"mesh lockup or entanglement"*), 재격자화는 이력 변수를 보간해 오차를 넣는다 (p.179 · `txt_p1_abstract_history_dependent_material_points.png`) — 그래서 이 논문은 PIC/FLIP 의 입자를 **물질점**으로 읽어 구성식 · 이력 변수 (소성 변형률 · 경화 변수) 를 물질점에서 부르고, 운동량은 **매 걸음 처음 자리로 다시 까는 격자** 에서 FE 꼴 약형으로 푸는 방법 (뒤에 'MPM' 으로 불리는 방법 — 이 원문에 그 이름은 0 회) 을 적고, 2D 예 여섯으로 *"impact with no slip is handled without any special algorithm for bodies governed by elasticity and strain hardening plasticity"* (p.179) 를 보인다.

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 이력 의존 (소성) 상태를 물질점에 싣는 까닭 | Euler = 물질점 추적 어려움 · 순수 Lagrange = 뒤틀림 → 강성 행렬 악조건 → lockup · 얽힘 · 재격자화 = 이력 변수 보간 오차 (초록) → *"Since each material point is followed, history-dependent variables, such as plastic strain and strain-hardening parameters, can be associated with the material point for the complete evolution of the problem"* (p.180) · *"Material points are followed so that interpolation for history-dependent variables is not required"* (p.193–194) | [인쇄] p.179 · p.180 · p.182 · p.193–194 |
| ② 방법의 뼈대 | 혼합 약형 (3.2): 운동량 = 격자 · 구성식 + 변형률 속도 = 물질점 · 밀도 ρ = Σ M_P δ[x − X_P] (3.4) · 응력 · 변형률 = 물질 부분 영역 위 조각 상수 (3.3) · S_Pi = N_i(X_P) · G_Pi = N_i∇\|X_P (3.7 · *"stochastic matrix"* — 성분 ≥ 0 · 행 합 1) · 일관 질량 m_ij = Σ_P M_P S_iP S_Pj (3.8) · 내부력 f_i^int = −Σ_P G_iP^T M_P·σ_P^s (3.9) · 비응력 ρσ^s = σ (2.6) | [인쇄] p.181–183 · 식 (2.6) · (3.2)–(3.12) |
| ③ 대류 (격자 넘김) 와 사상 | 격자 → 점 v_P = Σv_iN_i(X_P) (4.1 · 한 값 · 연속) · 점 → 격자 = FLIP 의 질량 가중 최소제곱 [m]{v} = [S]^T[M_D]{V} (4.3) · 실제는 대각 질량 · Burgess 외 [4]: 운동 에너지 · 선운동량 · 각운동량 보존 — 운동 에너지는 일관 질량일 때만 · 대각이면 *"some dissipation of kinetic energy"* | [인쇄] p.184–185 |
| ④ 12 단계 명시 알고리즘 | (6.1) 대각 질량 가속도 → (6.2) 격자 속도 → Step 3–5 물질점 속도 기울기 · 변형률 속도 · 구성식 서브루틴 응력 증분 + 이력 변수 갱신 → (6.3) 사상 → (6.4) 위치 = 격자 속도로 · 점 속도 = 가속도 증분 (FLIP) → (6.5) 새 S · G → (6.6) 일관 질량 → 행 합 → (6.7) 격자 속도 다시 · *"the matrices … are never formed"* | [인쇄] p.185–186 · 식 (6.1)–(6.7) |
| ⑤ ★ 접촉 = 한 속도장 | *"Because the velocity field is forced to be single valued, the algorithm is actually one of no slip"* (p.180) · *"the enforcement of a single-valued velocity field within any element … implies that no sliding occurs along the impact surface. Since no slideline algorithm is required the computational procedure is remarkably efficient for this class of problems"* (p.195) · [판독 · 카드 산술] 두 원판의 상호작용은 재료가 닿기 **≈1 셀 앞** (틈 0.75–1.2 h) 에서 시작 (§3-7) | [인쇄] p.180 · p.195 · [판독] 그림 4a · 5a · 10a |
| ⑥ 소성 구성식 | 작은 변형 rate 꼴 σ̇ = T:ė (2.2) · e = e^e + e^p (2.3) · ė^p = λ̇M (2.4) · T = T^E − (1/A)(T^E:M)⊗(N:T^E) · A = N:T^E:M − H (2.5) · 예: von Mises f = σ̄ − H · H = c₁ + c₂ē (7.5) · **c₁ = 100 (0.1E) · c₂ = 400** (E 1000 · 무차원) | [인쇄] p.180–181 · p.191 |
| ⑦ ★ 하중을 뺀 뒤 | *"residual plastic strains can prevent the elastic strain (and stress) from achieving a zero state even in the unloaded condition"* (p.191) · 탄소성 원판이 *"flattened and remains permanently distorted after separation"* · [판독] 분리 뒤 변형 에너지 0.17–0.36 (0 에 안 감) · 총 에너지 −46 % | [인쇄] p.191 · [판독] 그림 8a |
| ⑧ 수치 검증 | 균일 병진 = 정확 (p.187) · 강체 회전 한 바퀴 (51 × 51 노드 · 628 걸음) 오차 *"neglible"* (수치 없음) · 구리 원기둥 기본 모드 표 1: s · h 를 함께 반으로 → ω^d 0.97 · 0.99 · 1.00 · γ 0.121 · 0.0126 · 0.0041 · 탄성 원판 충돌 총 에너지 −4.3 % [판독] | [인쇄] p.187–189 · 표 1 · [판독] 그림 3 · 5 |
| ⑨ 저자 한계 · 원문 안 어긋남 | 열린 것 = 경계 조건 · no-slip 완화 · 요소당 물질점 수 · 연화 파괴 구역 · locking / hourglassing 상세 분석 (p.195–196) · 작은 변형 한정 (p.180) · 부분 질량 없음 (p.185) · 어긋남 = ρ 'kg/m³' · ω 'Hz' · h '0.80 cm' · 그림 3 캡션 h · (6.3) 의 {v} · 참고 번호 [8]/[9] (§3-8) | [인쇄] · [카드 산술] |

⛔ **한정어 (떼지 말 것)**: ① **작은 변형 rate 꼴** — *"the formulation is limited to small deformations although large translations are allowed"* (p.180) · ė = D (*"no correspondence with physical measurements"*) · 회전도 W (2.1) 는 정의만 되고 응력률은 객관률이 아니다 [카드 해석] ② **2D 평면 변형 예만** (3D 는 문장 둘뿐) ③ 재료 = 무차원 원판 · 막대 (E 1000 · ν 0.3 · ρ 1000) + 구리 원기둥 (탄성 · 실물 값) — **실험 대조 · 맞춘 값 0** ④ 소성 = von Mises + 선형 경화 하나 · 응력 적분 (반환 사상) 은 *"constitutive equation subroutine"* 으로만 · 소성 결과는 정성 (평평해짐 · 에너지 소산) — §7.5 의 위치 그림은 *"not plotted"* ⑤ 접촉 = 한 속도장 no-slip 뿐 — 미끄럼 · 마찰 · 접촉 법칙 없음 ⑥ 'particle' = **물질점** (부분 영역의 기준점) — 알갱이가 아니다 · 원판 · 막대는 연속체 물체 ⑦ 원문 안 단위 · 기호 어긋남 (§3-8).
⇒ **절대값 전이: 0 건.**  전이되는 것은 **방법의 뼈대 (이력 변수는 물질점 · 운동량은 격자 · 섞인 셀은 물질점마다 구성식) · 한 속도장 접촉의 성질 (자동 no-slip · ≈1 셀 앞에서 시작) · 단위 시험의 꼴 (균일 병진 · 강체 회전 · 원기둥 기본 모드 · 원판 충돌의 에너지 · 운동량) · 인용할 문장** 뿐이다.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-40 의 '왜' 칸)

의도 원문: *"f · l — MPM 원전: 이력 의존 (소성) 재료의 상태를 물질점에 싣는 까닭 (카드 §4-1 의 계보) → '소성을 입자 기법에 넣는 방법' 의 1 차 인용처"* (가리킨 카드 = `bardenhagen2005_mpm_foam_densification_simulation` §4-1 · 정본 L278 · b41 findings n 절)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "MPM 원전" | **일부** | 방법은 있다 — PIC/FLIP 를 고체로 넓히고 구성식을 **물질점에서** 부른 첫 판 (*"So far, FLIP has been used for materials governed by history independent constitutive equations for which it is natural to apply the constitutive equation at grid nodes. In this paper, we choose to invoke the constitutive equation at the material points"* p.180) · 혼합 약형 (3.2) · 12 단계 (6.1–6.7).  **이름 'material point method' · 'MPM' = 0 회** (원문은 *"particle method"* · *"extension of the particle-in-cell method"*) — 정본 카드들은 1995 판 (Sulsky · Zhou · Schreyer · Comp. Phys. Comm. 87 · 카드 없음) 과 묶어 인용한다 (`bardenhagen2004_…` L283 · `bardenhagen2005_…` L278 · `guilkey2003_…` L351) |
| "이력 의존 (소성) 재료의 상태를 물질점에 싣는 까닭" | **채움** | 초록 (p.179): *"For these problems, the constitutive equations are history dependent so material points must be followed; this is difficult to implement in a Eulerian scheme. On the other hand, purely Lagrangian methods typically result in severe mesh distortion and the consequence is ill conditioning of the element stiffness matrix leading to mesh lockup or entanglement. Remeshing prevents the lockup and tangling but then interpolation must be performed for history dependent variables, a process which can introduce errors."* · p.180 (위 ① 의 문장) · p.182 *"Invoking constitutive equations at material points simplifies the treatment of history-dependent variables"* · p.186 Step 5 · p.193–194 *"interpolation for history-dependent variables is not required"* · p.195 섞인 셀.  조건: 작은 변형 · 2D · 충돌 (누름 · 압밀 없음) |
| "(카드 §4-1 의 계보)" | **채움** (연도 하나 다름) | 원문 p.179–180: 고전 PIC [1] (*"partially Lagrangian in that only a mass and position is attributed to each particle"*) → FLIP [2, 3] (*"To reduce the amount of numerical dissipation, a 'full-particle' formulation called FLIP … each particle is attributed all the properties of the fluid, including momentum and energy"*) → 일관 질량 [4] (운동 에너지 보존 · 질량 행렬을 걸음마다 역행렬) → Sulsky · Brackbill [5] (탄성 물체 · 유체 속 탄성 물체 · *"interpenetration cannot occur"* → *"non-slipping contact algorithm"*) → 이 논문 (구성식을 물질점에서).  가리킨 카드의 'Harlow 1963' ↔ 이 원문 목록 [1] **1964** (Methods for Computational Physics Vol. 3) |
| "→ '소성을 입자 기법에 넣는 방법' 의 1 차 인용처" | **채움 (한정)** | 넣는 법: 탄소성 접선 (2.2)–(2.5) · 비응력 (2.6)–(2.8) · 물질점마다 *"The stress at material points is updated with the increment obtained from the constitutive equation subroutine. History-dependent variables such as plastic strain and strain-hardening parameters are also updated for each material point"* (Step 5 · p.186) · 예 = von Mises + 선형 경화 (7.5 · c₁ 100 = 0.1E · c₂ 400 · E 1000 · ν 0.3 · ρ 1000) 의 2D 원판 충돌 (§7.5 · §7.6).  한정: **작은 변형** (p.180) · 객관 응력률 없음 [카드 해석] · 응력 적분 알고리즘 미기재 · 결과는 정성 (평평해짐 · 에너지 −46 % [판독]) · 해석해 · 실험 대조 없음 |
| "f" (접촉 · 다물체 · 해상도 규칙 · 수치 오차 추정) | **일부** | 접촉 = 한 속도장 → 자동 no-slip · 침투 없음 (p.180 · p.195) · 다물체 · 미끄럼 · 마찰 = 없음 (*"relaxation of the no slip condition"* 은 열린 문제 p.195) · 해상도 = 요소당 물질점 4 (회전 · 원기둥 · 막대) · 표 1 (지름당 셀 15 · 30 · 60 [카드 산술] → ω^d 0.97 · 0.99 · 1.00 · γ 0.121 · 0.0126 · 0.0041 · s · h 를 함께 반으로) · 오차 추정 = 분산 ω^d = ω/ω^e · 소산 γ (E = E₀exp(−γωt/2π)) · 균일 병진 정확 · 회전 시험.  **지름당 셀 규칙 · 접촉 틈 규칙 = 없음** |
| "l" (소성이 왜 어려운가 · 우회 · 비용) | **채움 (FE 쪽 이유 · 비용 숫자 없음)** | 이유 = 위 초록 (Euler 추적 · Lagrange 뒤틀림 · 재격자화 보간) · 섞인 셀 (*"In purely Eulerian codes, elements (cells) that contain more than one material require special treatment"* p.195) · 우회 = 물질점 + 다시 까는 격자 · 비용 = *"The additional cost of the method over existing finite element algorithms appears in the form of maps between the material points and the grid. The benefit is no mesh distortion and, consequently, no need to remesh in the event that large deformations occur"* (p.194–195) · 회전 시험 *"because of the material points, the computational effort is greater"* (p.187) — **계산 시간 · 기계 · 물질점 수 = [미확인]** |

**가리킨 카드 · 이 논문을 다룬 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `bardenhagen2005_…` **L278** (가리킨 카드 · §4-1) | *"PIC (유체 · Harlow 1963) → 수치 확산을 줄인 개량 (Brackbill 외 1988 · Burgess 외 1992) → 물질점이 구성식의 상태 변수를 싣는 MPM (Sulsky 외 1994 · 1995)"* | p.179–180 의 계보 (위 표) · 이 원문 목록 [1] Harlow **1964** · [3] Brackbill · Kothe · Ruppel 1988 · [4] Burgess · Sulsky · Brackbill 1992 | **채움** — 계보 · 귀속 맞다.  'Harlow 1963' 은 Bardenhagen 2005 목록의 서지라 이 원문으로 판정할 수 없다 (다른 Harlow 문헌일 수 있음 · [미확인]) |
| `bardenhagen2004_…` **L283** | χ_p = δ(x − x_p)V_p → *"the formulation presented in [Sulsky, Chen, and Schreyer (1994); …(1995)] is recovered exactly"* | (3.4) 점 질량 ρ = Σ M_P δ[x − X_P] · (3.3) 조각 상수 U_P · (3.7) S_Pi = N_i(X_P) · G_Pi = N_i∇\|X_P | **채움** |
| `bardenhagen2004_…` **L227** | Sulsky 외의 유도 = 전체 질량 행렬을 만든 뒤 대각화 — *"which typically lacks justification beyond computational tractability"* | (3.8) 일관 질량 → p.184 *"To simplify calculations … a diagonal mass matrix can be employed in which each diagonal term consists of the row sum of m_ij"* · p.185 *"for computation efficiency"* + 대각 질량이면 운동 에너지 약간 소산 (Burgess [4]) | **채움** — 원문 스스로 근거를 계산 편의로 적는다 |
| `bardenhagen2004_…` L611 · `guilkey2003_…` L351 · `steffen2010_…` L337 | 서지 'CMAME 118, 179–196 (1994)' | 첫 쪽 머리 'Comput. Methods Appl. Mech. Engrg. 118 (1994) 179-196' | **채움** |
| `nairn2015_…` **L624** | Nairn 2015 목록 [1] *"118:179–186"* ↔ `bardenhagen2004_…` *"pp. 179–196"* (카드가 남긴 어긋남) | 18 쪽 · 마지막 쪽 머리글 196 → **179–196** | 풀림 — Nairn 2015 목록의 오기 (카드 줄 자체는 원문 그대로 옮겼다) |
| `steffen2008_…` **L401** · `_curation/wishlist.md` L190 | *"Sulsky, D.; Chen, A.; Schreyer, H. L. (1994)"* | 첫 쪽 **Z. Chen** | 인용한 논문 목록의 인쇄 그대로 (카드 오류 아님) — 인용할 때는 'Z. Chen' |
| `devaucorbeil2020_…` **L25** · **L74** | *"Sulsky 1994가 FLIP을 고체역학으로 변형"* · 입자가 *"전체 물리상태 (위치·질량·속도·부피·변형구배 Fₚ·Cauchy 응력 σₚ·온도·내부변수)"* 운반 · *"Sulsky 1994 (MPM 자체)"* | 계보 문장은 맞다 (p.180).  이 원문의 물질점 상태 = 위치 · 속도 · 질량 · 비응력 · 변형률 · 소성 변형률 · 경화 변수 (p.180 · p.185–186) — **변형구배 F · 부피 · 온도 없음** (작은 변형) · 이름 'MPM' 0 회 | **일부** — 상태 목록은 일반 MPM 서술 (1994 귀속으로 읽으면 틀림) |
| `klar2016_…` **L64** | *"이산화 = MPM (Sulsky 1994): 입자 (Lagrangian) 에 질량·운동량·F 저장"* | F 없음 — ė = D (2.1) · 작은 변형 (p.180) | **일부** — 'F 저장' 은 이 원문이 아니다 (카드 문제) |
| `cummins2002_…` **L85** · **L93** (11-12 같은 날 정본에 들어온 카드) | *"MPM (Sulsky 외 [1, 8] · 명시 도약) — … MPM 은 형상 함수를 미분한 뒤 보간"* · 소성 변형률 반경 귀환 = Sulsky 외 [8] (1995) | Step 3 의 속도 기울기 [G]^k{v*}^{k+1} · G_Pi = N_i∇\|X_P (3.7) = 형상 함수 기울기에 격자 속도 · 이 원문에는 응력 적분 (반경 귀환) 알고리즘이 없다 (*"constitutive equation subroutine"* 만) | **채움** — 미분 · 보간 순서 맞음 · 반경 귀환을 1995 판 [8] 에 귀속한 것도 이 원문과 모순 없음 |
| `stomakhin2013_…` **L56** · **L192** ↔ `devaucorbeil2020_…` L74 | *"MPM 자체는 Sulsky et al. 1995"* ↔ *"Sulsky 1994 (MPM 자체)"* | 1994 = 방법의 첫 고체 판 (p.180) · 이름 0 회 · 1995 원문 카드 없음 | 카드 사이 표기 차이 — 이 원문만으로 어느 쪽이 틀렸다고 할 수 없다 (방법은 1994 에 있다) |

⇒ **의도 대조 결과: 채움 (한정)** — 이력 의존 상태를 물질점에 싣는 까닭과 그 계보, '소성을 입자 기법에 넣는 방법' 의 1 차 인용처는 **채움** (단 작은 변형 rate 꼴 · 2D 충돌 예 · 정성 결과), "MPM 원전" 은 **방법만 · 이름 0 회 (일부)**, f 는 **한 속도장 no-slip 과 표 1 수렴뿐 (일부 · 지름당 셀 · 접촉 틈 규칙 없음)**, l 의 비용은 **문장만 · 숫자 없음**.  가리킨 카드 L278 은 원문과 맞다 (Harlow 연도만 판정 불가).

---

## 1. 한 줄 요약
PIC/FLIP 를 고체로 넓혀 입자를 물질점으로 읽고, 구성식 (탄성 · 탄소성) 과 이력 변수를 물질점에서 갱신하면서 운동량은 매 걸음 다시 까는 격자에서 FE 꼴 약형으로 풀어 (질량은 일관 → 행 합 대각 · 격자 ↔ 점 사상은 FLIP), 격자 뒤틀림 · 이력 변수 보간 · 섞인 셀 · 접촉 알고리즘 없이 2D 충돌 · 회전 · 진동을 푼다 (`txt_p1_abstract_history_dependent_material_points.png` · `txt_p1_p2_flip_no_slip_constitutive_at_material_points.png`).
저자의 결론: *"With an extension of the particle-in-cell method, a numerical algorithm has been developed that combines several desirable features"* (p.193) — 갱신 Lagrange 로 읽히는 격자라 대류 미분의 확산이 없고 · 이력 변수 보간이 필요 없고 · 약형의 대칭 · 내부력 벡터 꼴이 FE 와 같다 (p.193–194).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| D. Sulsky · Z. Chen · H.L. Schreyer\* (Univ. New Mexico · 수학과 · NMERI · 기계공학과) | Comput. Methods Appl. Mech. Engrg. 118, 179–196 (1994) | [미확인] (인쇄 없음 · PII 0045-7825(94)90112-0 · SSDI 0045-7825(94)00033-J) | **실제 재료 하나** (구리 원기둥 · 탄성 · E 126 GPa · ν 0.35) + 무차원 탄성 · von Mises 원판 · 막대 · 층 (E 1000 · ν 0.3 · ρ 1000) | 수치 방법 정식화 + 2D 수치 예 |

- **1저자 메모 (후보 표 행) 와의 대조**: 저자 · 제목 · 권 118 · 쪽 179–196 · 1994 — **같다**.  다른 점: 학술지 약어 꼴 ('Comput. Methods Appl. Mech. Engrg.' ↔ 행 'Comp. Methods Appl. Mech. Eng.') · DOI 인쇄 없음 · 초록 첫 줄 'tmpact' 는 OCR (스캔은 'impact').
- **글의 꼴**: 1 서론 → 2 지배 방정식 → 3 지배 방정식의 혼합 약형 → 4 대류 단계 → 5 물질점 생성 → 6 수치 알고리즘 → 7 수치 예 (7.1 회전 · 7.2 진동하는 탄성 원기둥 · 7.3 탄성 물체 둘의 충돌 · 7.4 튀는 막대 · 7.5 비탄성 물체 둘의 충돌 · 7.6 탄성 원판과 경화 원판의 충돌) → 8 결론 → 감사 → 참고문헌 10.  그림 10 · 표 1 · 번호 식 37 ((2.1)–(2.9) · (3.1)–(3.12) · (4.1)–(4.3) · (5.1) · (6.1)–(6.7) · (7.1)–(7.5)).
- 계보: LANL FLIP 계열 (Brackbill) 과 UNM 의 결합 — Sulsky · Brackbill 1991 [5] 의 탄성 판을 이력 의존 재료로 넓힌 판 · 뒤의 Bardenhagen · Brackbill · Sulsky 2000 (다물체 접촉 · 정본 카드) 으로 이어진다 [다른 카드 `bardenhagen2000_…` L53].

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 지배 방정식 · 구성식 (§2 · p.180–181 · 식 2.1–2.9 · `eq_2_01_…` – `eq_2_09_…` · `txt_p2_small_deformation_strain_measure.png` · `txt_p3_lagrangian_eulerian_split_updated_lagrangian.png`)
- **작은 변형**: *"To present the method in the simplest possible context, the formulation is limited to small deformations although large translations are allowed. Therefore there is no need to select from among the various strain and stress tensors and the gradient operators associated with large-deformation theory"* (p.180).
- L = v∇ = D + W (2.1 · D = 대칭 = 변형 속도 · W = 비대칭 = 회전) · 변형률 e 는 ė = D 로 정의 — *"Such a strain tensor is often used for computational convenience, as it is here, even though there is no correspondence with physical measurements, as exists, for example, with Lagrangian or logarithmic strain tensors"* (p.180).
- σ̇ = T:ė (2.2 · 4 차 접선 계수 T · 탄성이면 T = T^E) · e = e^e + e^p (2.3) · ė^p = λ̇M (2.4 · M = 소성 변형률 속도의 진화 함수) · 일관성 ḟ = 0 · *"f < 0 denotes elastic behavior, f = 0 denotes yielding, and f > 0 is not permitted"* · N = ∂f/∂σ → **T = T^E − (1/A)(T^E:M)⊗(N:T^E) · A = N:T^E:M − H** (2.5 · H > 0 경화 · 0 완전 소성 · < 0 연화).
- 비응력 ρσ^s = σ (2.6) · σ̇^s = T^s:ė (2.7) · 작은 변형이라 ρ 일정 → ρT^s = T (2.8) · 운동 방정식 (ρσ^s)·∇ + ρb = ρa · a = v̇ (2.9) · σ = σ^T.
- 혼합 서술: 비응력 = (x, t) 의 함수 (Euler) · 속도 = (X⁰, t) 의 함수 (Lagrange) → *"the acceleration does not contain the convection term which causes a significant amount of numerical error if a purely Eulerian approach is used. Convection is handled in a separate step by mapping quantities from the material points to the grid"* · ALE [6, 7] 와 같은 바탕 · Benson [8] 리뷰 (p.181).  갱신 Lagrange = 걸음 끝의 X 를 다음 걸음의 기준 · 완전 Lagrange = X⁰ (p.181).
- [카드 해석] W 는 (2.1) 에서 정의만 되고 뒤의 어느 식에도 안 쓰인다 → (2.2) 의 응력률은 객관률 (Jaumann 등) 이 아니다 — 응력을 진 채 크게 도는 물체에는 맞지 않는다.  원문은 회전 · 객관성을 말하지 않는다 (회전 시험 §7.1 은 응력 없는 스칼라 수송).

### 3-2. 혼합 약형 · 이산화 (§3 · p.181–184 · 식 3.1–3.12 · 그림 1 · `eq_3_01_…` – `eq_3_12_…` · `fig_1.png` · `txt_p4_momentum_on_grid_material_subdomains.png` · `txt_p5_mapping_matrix_stochastic_gradient.png` · `txt_p6_four_differences_from_fem.png`)
- (3.1) 에 가중 함수 w · ρW · ρW* 를 곱해 현재 배치 Ω 에서 적분 → (3.2) 세 식 (운동량 + 구성식 + 변형률 속도).  *"In (3.2), the momentum equation is to be solved on a grid, whereas the second two equations are to be evaluated at material points in the PIC formulation. Invoking constitutive equations at material points simplifies the treatment of history-dependent variables"* (p.182).
- **물질점**: 처음 배치를 부분 영역 Ω_P⁰ (P = 1, …, N) 으로 나누고 각각 기준 물질점 X_P⁰ · 질량 M_P · 시간이 가면 Ω_P · X_P (같은 질량) — *"From compatibility, these material subdomains remain simply connected but, in general, the shapes of the subdomains will be unknown. Nevertheless, as shown below, the material points, X_P, can be tracked"* (p.182 · 그림 1).
- 조각 상수 기저 U_P (Ω_P 위 1 · 밖 0 · U_I(X_J) = δ_IJ) 로 W · W* · σ^s · e (3.3) · 밀도 = **Dirac 점 질량 ρ = Σ M_P δ[x − X_P]** (3.4) → 물질점의 구성식 · 변형률 속도 (3.5).  *"In many finite element codes, stress and strain rates are determined at element centers or at Gauss points. Here, the tracked material points may appear at arbitrary points within an element"* (p.183).
- **격자**: 통상의 FE 절점 기저 N_i(x) 로 w · v · a (3.6) · S_Pi = N_i(X_P) · G_Pi = N_i∇\|X_P (3.7) — *"[S] can be thought of as a stochastic matrix in the sense that all entries are positive or zero and each row sum is one"* (p.183).  절점 기저의 차수 (이중선형 등) 는 인쇄 없음 [미확인].
- **질량 · 힘**: m_ij = Σ_P M_P S^T_iP S_Pj (3.8) · f_i^int = −Σ_P G^T_iP M_P·σ^s_P (3.9) · b_i = Σ_P S^T_iP M_P b_P · τ̂_i = ∫N_i τ dS (3.10) · f_i^ext = b_i + τ̂_i (3.11) · **Σ_j m_ij a_j = f_i^int + f_i^ext** (3.12) — 변위가 처방된 성분 밖에서.
- **FE 와 다른 넷** (p.184): ① 질량 행렬이 시간에 따라 바뀌어 걸음마다 다시 — 대각 (행 합) 을 써도 된다 ② 기울기 · 응력 · 변형률이 요소 사이를 옮겨 다니는 물질점에서 ③ 점 질량이 힘 벡터에 들어간다 ④ 비응력으로 응력을 물질점에서만.
- [카드 해석] '조각 상수 응력 + 점 질량 + 절점 기저 기울기' = Bardenhagen 2004 의 χ_p = δ(x − x_p)V_p 특수형 [다른 카드 `bardenhagen2004_…` L283] — 셀 경계에서 G_Pi 가 불연속이라 셀 넘김 잡음이 생기는 꼴이다.  이 논문은 셀 넘김 잡음을 말하지 않는다 (예들이 작은 변형 · 요소당 4 점).

### 3-3. 대류 단계 · 사상 (§4 · p.184–185 · 식 4.1–4.3 · `eq_4_01_…` – `eq_4_03_…` · `txt_p6_convective_phase_fixed_grid.png` · `txt_p7_conservation_lumped_mass_dissipation.png`)
- *"A great advantage of this approach is that the computational grid can be chosen for convenience. For example, the grid can be kept fixed in contrast to updated Lagrangian schemes in which elements can become severely distorted and even entangled"* · 격자를 고정하면 물질점이 격자선을 넘으므로 대류가 계산에 들어가야 한다 → Brackbill · Ruppel [2] 의 사상 (p.184).
- *"When the material points move, they transport material properties assigned to them without error. With the use of information carried by the material points, the solution can be reconstructed on any grid … In the numerical examples of Section 7, information is mapped from material points to a uniform Eulerian grid to begin each time step"* (p.184).
- 격자 → 점: v_P = Σ_i v_i N_i(X_P) (4.1 · *"assures single-valuedness and continuity of the velocity field"*) · {V} = [S]{v} (4.2).
- 점 → 격자: [S] 가 직사각이라 FLIP 의 질량 가중 최소제곱 **[m]{v} = [S]^T[M_D]{V}** (4.3 · [m] = (3.8) 과 같은 격자 질량 행렬) — *"However, we also use the diagonal form of the grid mass matrix for computation efficiency in obtaining {v}"* (p.185).
- 보존 (p.185): *"Burgess et al. [4] have shown that this particular formulation for mapping velocity from material points to grid nodes implies that kinetic energy, linear momentum and angular momentum are conserved. Kinetic energy is conserved provided the consistent mass matrix, [m], is used with grid quantities. The result of using a diagonal mass matrix is some dissipation of kinetic energy that has been quantified by Brackbill and Ruppel [2], Brackbill et al. [3] and Burgess et al. [4]"* — 이 논문은 그 소산을 다시 재지 않는다 (예들의 총 에너지 곡선뿐).

### 3-4. 물질점 생성 (§5 · p.185 · 식 5.1 · `eq_5_01_…` · `txt_p7_material_point_generation_partial_mass.png`)
- 정사각 요소 (*"Unless there is some reason to do otherwise, choose square elements"*) · 재료 영역 = 해석적 부등식 g_α(X⁰) ≤ 0 (5.1 · 면 한 조각씩 · 빈 곳도) · 2D 구현 = 직선 · 원 · 타원 조합 · 요소마다 시험 점 → 부등식을 만족하면 그 구성식의 배열에 넣고 초기값 (위치 · 속도 · 질량 = 밀도와 셀당 점 수로) 저장.
- ★ *"No attempt is made to allocate partial masses to account for the fact that material boundaries can pass through a cell. The effect of not allocating partial masses can be assessed by performing a convergence study with respect to changes in the number of material points assigned to each cell"* (p.185) — 그 수렴 연구는 이 논문에 **없다**.  *"The result is a mesh and material point generation scheme that is remarkably general and easy to implement"*.
- [판독 · 카드 산술] 원판 질량: §7.3 = 처음 운동 에너지 / v² = 2.611/0.02 = **130.6** (원판 둘 · |v| = 0.1414 · r = √(M/ρπ) = 0.204) · §7.6 = 2.426/0.02 = **121.3** (r 0.197) — 두 예의 반지름이 인쇄되지 않아 원판 크기 차인지 '부분 질량 없는 생성' 이 격자 위치에 따라 점 수를 바꾼 것인지 가를 수 없다 [미확인].  §7.3 의 점 수 어림 = πr²/(h/2)² = 209 (요소당 2 × 2 가정) ↔ 그림 4a 에서 센 점 192 · 198 (붙은 점이 하나로 세어질 수 있음) [판독].

### 3-5. 12 단계 알고리즘 (§6 · p.185–186 · 식 6.1–6.7 · `eq_6_01_…` – `eq_6_07_…` · `txt_p8_steps_3_5_history_variables.png`)
- 시간 간격 s · t^k = ks · 물질점 질량 대각 [M_P] 는 처음 이산화로 정해 고정 (*"the mass of a material point does not change"*).  t^k 에 [S]^k · [G]^k · [m_D]^k · {v}^k · {X}^k · {f^int}^k · {f^ext}^k 를 안다고 할 때 (한 성분씩 적음 · *"x, y and z for three dimensions"*):
  1. **[m_D]^k{a}^k = {f^int}^k + {f^ext}^k** (6.1 · 대각 질량)
  2. **{v*}^{k+1} = {v}^k + s{a}^k** (6.2 · 명시)
  3. 물질점 속도 기울기 [G]^k{v*}^{k+1} (*"There are nine such combinations in three dimensions"*)
  4. 물질점 변형률 속도 (3.5)
  5. *"The stress at material points is updated with the increment obtained from the constitutive equation subroutine. History-dependent variables such as plastic strain and strain-hardening parameters are also updated for each material point"*
  6. **{V*}^{k+1} = [S]^k{v}^{k+1} · {A}^k = [S]^k{a}^k** (6.3)
  7. **{X}^{k+1} = {X}^k + s{V*}^{k+1} · {V}^{k+1} = {V}^k + s{A}^k** (6.4 · 위치 = 사상된 격자 속도 · 점 속도 = 가속도 증분 = FLIP)
  8. [S]^{k+1} = {N}(X^{k+1}) · [G]^{k+1} = {N}∇\|X^{k+1} (6.5)
  9. 내부력 (3.9)
  10. **[m]^{k+1} = [S^T]^{k+1}[M_D][S]^{k+1}** (6.6) → 행 합 → [m_D]^{k+1}
  11. **[m_D]^{k+1}{v}^{k+1} = [S^T]^{k+1}[M_D]{V^{k+1}}** (6.7 · (4.3) 의 대각 판)
  12. 처음으로.
- *"We want to emphasize that the matrices used to describe the procedure are never formed. Rather, quantities are accumulated by sweeping over elements as done in many finite element programs"* (p.186).
- [카드 해석] 응력이 격자 속도 갱신 (Step 2) **뒤** 의 {v*}^{k+1} 로 갱신되는 순서 — 뒤 문헌의 'USL' (update stress last) 꼴과 같은 순서다 (이 원문에 그 이름은 없다 · 순서별 에너지 오차 = Bardenhagen 2002 · Wallstedt · Guilkey 2008 — 둘 다 카드 없음 [다른 카드 `steffen2008_…` L391–L392]).
- [카드 해석 · 표기 어긋남] (6.3) 의 오른쪽은 {v}^{k+1} 로 인쇄 — 그 시점에 {v}^{k+1} 은 Step 11 전이라 아직 없다 → Step 2 의 {v*}^{k+1} 로 읽어야 정합.

### 3-6. 수치 예 ① 회전 · ② 원기둥 진동 (§7.1–7.2 · p.187–189 · 식 7.1–7.4 · 그림 2 · 3 · 표 1 · `fig_2.png` · `fig_3.png` · `tab_1.png` · `txt_p9_rotation_test_setup_result.png` · `txt_p9_p11_cylinder_setup_dispersion_dissipation.png`)
- **강체 회전** (대류 시험 · 응력 없음): 확산 없는 스칼라의 연속 방정식 dΨ/dt = ∂Ψ/∂t + v·(Ψ∇) = −Ψ(v·∇) (7.1) · Smolarkiewicz 의 홈 파인 원기둥 (반지름 0.15 · 높이 4.0 → Ψ_P = 4.0) · 영역 1.0 정사각 · v = Ωk × (x − x_c) (7.2 · Ω = 0.1 · x_c = (0.5, 0.5, 0)) · 방향당 51 노드 · s = 0.1 · 한 바퀴 628 걸음 · Ψ ≠ 0 요소마다 물질점 4 · 속도는 Step 2 대신 시간 중심 위치에서 처방 (7.3) · 위치 (7.4).  결과 (그림 2b): *"The only source of numerical error is the mapping of the velocity from the grid to the material points at each step and the discrete-time integration algorithm used to update the positions of the material points. The errors associated with the process are neglible compared with the errors associated with convection algorithms on Eulerian grids"* (p.187 · 'neglible' 인쇄 그대로) — **오차 수치 없음** [미확인].  비용: *"This formulation contains fewer grid points than the number used by Smolarkiewicz [9], but because of the material points, the computational effort is greater. However, even when the number of elements is reduced, our results are unchanged"*.
  [카드 산술] h = 1/50 = 0.02 · 반지름/h = 7.5 · 2π/(Ωs) = 628.3 걸음 ✓ · 물질점 ≈ π(0.15)²/(0.02)² × 4 = 707 (홈 부분 빼기 전).
- **균일 병진**: *"if there is no acceleration and if the solution for the velocity can be represented exactly by the element shape functions, then the numerical solution will be exact. A particular case is uniform translation"* (p.187).
- **진동하는 탄성 원기둥** (평면 변형): 무한히 긴 구리 원기둥 R = 0.6 cm · *"ρ = 8.92 kg/m³"* (인쇄 · §3-8) · E = 126 GPa · ν = 0.35 · 1 차 Bessel 꼴 기본 모드 · *"ω^e = 1.73 × 10⁶ Hz for plane strain"* (인쇄 · §3-8) · 반지름 변형 2 % (기본 모드만 들뜸) · 요소당 물질점 4 · 에너지 (점선 = 탄성 변형 · 파선 = 운동 · 실선 = 합).  그림 3a: s = 0.2 µs (ω^e s = 0.35) · *"h = 0.80 cm = 0.133R"* (인쇄 · 0.08 cm 로 읽힘) → 예측 진동수 1.68 × 10⁶ · 분산 ω^d = ω/ω^e = 0.97 · 소산 E = E₀exp(−γωt/2π) 의 **γ = 0.121** (p.188).
- **표 1** (s · h 를 함께 반으로 · p.189): (s µs · sω^e · h cm · ω^d · γ) = **(0.2 · 0.35 · 0.08 · 0.97 · 0.121) · (0.1 · 0.17 · 0.04 · 0.99 · 0.0126) · (0.05 · 0.087 · 0.02 · 1.00 · 0.0041)** — *"Both dissipation and dispersion are reduced to an insignificant amount with mesh and time step refinement. This problem was also studied previously [4, 5], with similar results. The difference between our algorithm and the one in these references is that we apply constitutive equations at the material points rather than at grid nodes"* (p.188–189).
- [카드 산술] R/h = 7.5 · 15 · 30 (**지름당 셀 15 · 30 · 60**) · 단면 물질점 ≈ 707 · 2827 · 11310 (원 전체 · 요소당 4 가정 — 원문은 단면 전체인지 4 분의 1 인지 말하지 않음 [미확인]) · c_P = √((λ+2μ)/ρ) = 4761 m/s (ρ = 8920 kg/m³) → **c_P s/h = 1.19** (세 행 같음) · 막대 파속 √(E/ρ) 3758 m/s → 0.94.  원문은 안정 조건 · CFL 을 말하지 않는다.
- [카드 산술 · 해석해] 평면 변형 축대칭 반지름 모드의 진동수 식 x J₀(x) = ((1−2ν)/(1−ν)) J₁(x) (표면 견인 0) 의 첫 근 x = 2.18677 (ν 0.35) → ω = x c_P/R = **1.7353 × 10⁶ rad/s** (f 276 kHz) · ωs = 0.347 ✓ 인쇄 0.35.  ρ = 8.92 kg/m³ 그대로면 ω = 5.49 × 10⁷ · ωs = 11.0 ✗ — 원문은 진동수 식을 인쇄하지 않는다.
- [판독] 그림 3 총 에너지 봉우리: 간격 1.902 · 1.840 · 1.820 µs → ω = π/간격 = 1.652 · 1.707 · 1.726 rad/µs (ω/ω^e = 0.955 · 0.987 · 0.998 ↔ 인쇄 0.97 · 0.99 · 1.00) · 봉우리 감쇠 → γ = 0.1315 · 0.0149 · 0.0042 (↔ 인쇄 0.121 · 0.0126 · 0.0041) — 그림 3 의 세로축은 'energy *10⁻⁵' · 가로축 'time' (단위 인쇄 없음).

### 3-7. ★ 충돌 예 (§7.3–7.6 · p.189–195 · 식 7.5 · 그림 4–10 · `fig_4.png` – `fig_10.png` · `eq_7_05_…` · `txt_p11_elastic_disk_impact_setup.png` · `txt_p12_p13_elastic_impact_energy_dissipation.png` · `txt_p13_inelastic_impact_vonmises_residual_strain.png`)
- **§7.3 같은 탄성 원판 둘**: E = 1000 · ν = 0.3 · ρ = 1000 (무차원) · 왼쪽 아래 (0.1, 0.1) · 오른쪽 위 (−0.1, −0.1) · 정사각 요소 h = 0.05 · s = 0.001 · 이동 방향 45° · 평면 변형 · 반지름 · 요소당 점 수 인쇄 없음 (처음 중심 거리 0.71 = §7.6 의 문장 p.191–192).  *"there is no error in the numerical solution associated with a uniform translation of an object through a grid"* · 그림 4b = 충돌 중 변형 · 4c–d = 되튐 (p.189).
  에너지 (그림 5a · p.190–191): 처음 = 전부 운동 · 충돌 중 감소 → 분리 뒤 대부분 회복 · 변형 에너지는 최대 변형에서 최대 → *"a nominal value associated with free vibration of the disks after impact. The strain energy is small but not zero at discrete times after impact. The fact that a zero value is not achieved can be attributed to the activation of several modes which do not exhibit zeros at the same time. The total energy (solid line) decreases slightly with time indicating some numerical dissipation"*.  운동량 (그림 5b): 왼쪽 아래 원판의 x · y 성분 (구분 안 될 만큼 같음) · 충돌 뒤 부호 반전.
  [판독] 총 에너지 2.611 (t 0.05) → 2.595 (1.4) → 2.539 (2.0) → 2.499 (2.95) = **−4.3 %** · 운동 에너지 최소 0.074–0.086 (t 1.40–1.41) · 변형 에너지 최대 2.515 (1.41) · 뒤 운동 2.32–2.42 · 변형 0.13–0.21 · x 운동량 12.80–12.96 → −12.05…−12.16 (**크기 비 0.93–0.94**).
  [판독 · 카드 산술] ★ **상호작용은 재료가 닿기 전에 시작**: 운동 에너지가 총에서 떨어지는 시각 t ≈ **0.86–0.88** (2.611 → 2.591 → 2.543) · 자유 비행으로 닿는 시각 t_c = (0.71 − 2r)/0.2828 = **1.04–1.07** (2r = 0.408 [KE 로 산술] – 0.416 [그림 4a 판독]) → 시작 때 재료 사이 틈 0.045–0.061 = **0.9–1.2 h** (t 0.86–0.88) · t = 1.0 에서 운동 에너지 이미 −17 % (2.169) · 그림 4a (t = 1.0) 의 중심 거리 0.445 (자유 비행 0.427 보다 멀다 = 이미 감속) · 두 원판의 가장 가까운 점 사이 0.053 (≈1.07 h) → 재료 틈 ≈ 0.028 (점 반 간격 h/4 를 양쪽에서 뺌 · 요소당 2 × 2 가정).
- **§7.4 튀는 막대**: 직사각 탄성 막대 0.2 × 0.4√2 · 처음 속도 (−0.1, −0.1) · 모서리가 두께 0.25 탄성 층을 친다 · 둘 다 E 1000 · ν 0.3 · ρ 1000 · *"four particles per square element with size h = 0.05"* · s = 0.005 · 첫 모서리 충돌 → 되튐 + 회전 → 둘째 모서리 → *"the bar will not strike the layer again"* (그림 6) · 격자 속도 그림 (그림 7 · *"All points in the layer are actually excited but velocities below a certain level were excluded from the plot"*).  에너지 · 운동량 그림 없음.
  [카드 산술] c_P = √((λ+2μ)/ρ) = 1.160 → c_P s/h = 0.116 (막대) · 0.023 (원판 s 0.001) · 원판 속도/c_P = 0.122.
- **§7.5 탄소성 원판 둘**: §7.3 과 같고 재료만 **von Mises + 선형 경화** — f = σ̄ − H · H = c₁ + c₂ē (7.5) · σ̄ = (3/2 σ^d:σ^d)^{1/2} (*"the second invariant of the stress deviator"*) · ē = ∫(2/3 ė^p:ė^p)^{1/2}dt (*"the plastic strain path invariant"*) · **c₁ = 100 (0.1E) · c₂ = 400**.  위치는 그림 4 와 매우 비슷해 *"are not plotted"* — *"A small difference appears after impact, where a part of each disk is flattened and remains permanently distorted after separation. The amount of separation is not as large as that shown in Fig. 4(d) for the corresponding elastic case"* (p.191).
  에너지 (그림 8a): *"a large dissipation in the total energy (solid line) after impact because of plastic dissipation. After impact, the kinetic energy (dashed line) oscillates about a lower value than existed before the impact and the elastic strain energy (dotted line) does not achieve a value of zero for any time. In addition to the argument concerning the activation of several modes as a reason for non-zero strain energy, there is now the additional factor that residual plastic strains can prevent the elastic strain (and stress) from achieving a zero state even in the unloaded condition"* (p.191).  운동량 (그림 8b): 부호 반전 · 크기 *"significantly decreases"* · x · y 구분 안 됨.
  [판독] 총 에너지 2.61 → 1.50 (t 1.6) → 1.407 (2.95) = **−46 %** · 운동 에너지 최소 0.12 (1.40–1.45) · 변형 최대 1.53 (1.35) · 뒤 운동 1.11–1.31 · 변형 0.17–0.36 · x 운동량 12.85 → −8.12…−8.50 (**크기 비 ≈0.64**) · 운동 에너지가 총에서 떨어지는 시각 ≈0.84–0.88 (§7.3 과 같다).
  [카드 산술] 1D 충격 응력 어림 ρ c_P v = 1000 × 1.160 × 0.1414 ≈ 164 > c₁ = 100 → 충돌면이 항복할 크기 · 항복 변형률 c₁/E = 0.1 · 되튐 병진 운동 에너지 = 2px²/M = 2 × 8.3²/130.6 = 1.05 ≤ 판독 운동 1.11–1.31 (나머지 = 진동) · 탄성 경우 2 × 12.05²/130.6 = 2.22 ≤ 2.32–2.42.
- **§7.6 탄성 원판 ↔ 경화 원판**: 같은 물성 · 격자 · 속도 크기 · s · 아래 왼쪽 = 탄성 · 위 오른쪽 = 탄소성 경화 · 속도 방향 30° · 처음 중심 거리 0.55 (*"slightly smaller than the initial separation of 0.71 used for the previous examples"*).  그림 9: *"a slight flattening of one side of the plastic disk after impact"* · 그림 10a: 에너지 *"intermediate to those of the problems in Sections 7.3 and 7.5"* · 그림 10b–c: *"Because of the direction of motion, the x and y components of momentum are not equal. Furthermore, the relative magnitude of the two components of momentum switches after impact as expected"* (p.192–193).
  [판독] 총 에너지 2.426 → 1.733 (t 1.2) → 1.660 (1.97) = **−32 %** · 운동 에너지가 총에서 0.05 떨어지는 시각 ≈ 0.37 · 탄성 원판 (14.96, 8.62) → (−10.9, −6.7…−6.8) (크기 비 ≈0.74) · 소성 원판 (−14.89, −8.63) → (9.80–9.96, 5.85–5.93) (≈0.67).
  [카드 산술] 자유 비행 접촉 = (0.55 − 2r)/0.2828 = 0.50–0.56 (2r 0.393–0.408) → 운동 에너지가 0.05 떨어지는 t 0.37 의 틈 0.037–0.052 = 0.75–1.05 h (정면 충돌 가정 · §7.3 과 같은 크기).
  ⚠ [판독 · 카드 산술] 두 원판 운동량 합이 처음 (0.07, −0.01) → 뒤 (−1.0…−1.1, −0.85…−0.94) — |p₀| = 17.27 의 ≈ 8 % 가 0 에서 벗어난다 (판독 잔차 ≤ 0.08 단위보다 크다 · 그림 10b–c 를 눈으로 봐도 탄성 원판 ≈ −11 · 소성 원판 ≈ +10).  원문은 이 예에서 운동량 보존을 말하지 않고 원판별 운동량을 어떻게 셌는지도 인쇄하지 않는다 → 원인 해석 보류 [미확인].  'relative magnitude … switches' 도 판독과 안 맞는다 (|x| > |y| 가 앞뒤 모두) — 무엇을 가리키는지 [미확인].

### 3-8. ★ 저자가 적은 한계 · 원문 안 어긋남
**저자 한계**
1. *"Numerous points remain to be investigated in detail, including boundary conditions, relaxation of the no slip condition, the utility of using more or fewer material points per element, and close observations in the material failure zone when softening occurs. Numerical solutions to a rather extensive set of model problems have shown no difficulties with locking or hourglassing but a detailed analysis of typical cells have not been performed"* (p.195–196 · `txt_p17_p18_open_points_locking_hourglassing.png`).
2. 작은 변형 한정 (p.180) · 부분 질량 없음 → 셀당 점 수 수렴 연구로 평가하라 (p.185 · 이 논문엔 없음).
3. 한 속도장 = no slip — *"implies that no sliding occurs along the impact surface"* (p.195).
4. 대각 질량 → 운동 에너지 소산 (p.185 · 정량은 [2–4] 로).

**원문 안 어긋남 (카드 산술 · 대조 — 인용 때 표지)**
5. *"ρ = 8.92 kg/m³"* (p.187) — 구리 8.92 g/cm³ = 8920 kg/m³ 이어야 sω^e = 0.35 가 선다 (§3-6 · [카드 산술]).
6. *"ω^e = 1.73 × 10⁶ Hz"* · 예측 *"1.68 × 10⁶ Hz"* (p.188) — rad/s 로 읽어야 sω^e = 0.35 (Hz 면 2π × 1.73 × 10⁶ × 0.2 × 10⁻⁶ = 2.17) [카드 산술].
7. *"h = 0.80 cm = 0.133R"* (p.188) — 0.133R = 0.080 cm · 표 1 h = 0.08 cm.  그림 3 캡션 *"(a) h = 0.8 cm … (b) h = 0. cm … (c) h = 0.2 cm"* (↔ 표 1 0.08 · 0.04 · 0.02) · 시간 단위 'µ_s' (표 1 · 캡션).
8. (6.3) 오른쪽 {v}^{k+1} ↔ Step 2 의 {v*}^{k+1} (§3-5).
9. 본문의 Smolarkiewicz 참고 번호: [8] 두 번 (p.187) · [9] 한 번 (p.187) — 목록 [8] = Bensen · [9] = Smolarkiewicz.
10. 본문 *"Benson [8]"* (p.181) ↔ 목록 *"D.J. Bensen"*.
11. 인쇄 그대로: *"neglible"* (p.187) · *"a detailed analysis of typical cells have not been performed"* (p.196) · *"to insure"* (p.195).
12. W (2.1) 정의 뒤 미사용 (§3-1 · [카드 해석]).
13. §7.6 운동량 합 ≠ 0 · 'switches' ↔ 판독 (§3-7 · [판독]).

---

## 4. ★ 방법 — 계산 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 계산 사슬
1. **연속체 지배식** (작은 변형 · rate 꼴 탄소성 · 비응력 · 혼합 Euler / Lagrange) — §2.
2. **혼합 약형** (운동량 = 격자 · 구성식 + 변형률 속도 = 물질점) — §3 · (3.2).
3. **기저 선택** (밀도 = 점 질량 · 응력 / 변형률 = 조각 상수 · 격자 = FE 절점 기저) → 이산 운동 방정식 (3.12).
4. **대류 = 사상** (격자 → 점 4.1 · 점 → 격자 FLIP 4.3) — §4.
5. **물질점 생성** (해석적 부등식 · 요소당 점 · 부분 질량 없음) — §5.
6. **12 단계 명시 적분** — §6.
7. **2D 시험 여섯** — §7.

### 4-2. 이산화 · 계산 규모 (인쇄된 것만)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 차원 | **2D** (평면 변형) — 3D 는 문장 둘 (*"nine such combinations in three dimensions"* · *"x, y and z for three dimensions"* p.186) | [인쇄] p.179 · p.185–186 |
| 요소 · 기저 | 정사각 요소 · 통상의 FE 절점 기저 N_i (차수 인쇄 없음) · 격자는 매 걸음 고른 Euler 격자로 다시 | [인쇄] p.183–185 · [미확인] 차수 |
| 격자 크기 | 회전: 방향당 51 노드 (영역 1.0) · 원기둥: h 0.08 · 0.04 · 0.02 cm (R 0.6 cm) · 원판 · 막대: h 0.05 (영역 ≈1.04 [판독 그림 4a]) | [인쇄] p.187–189 · p.191 |
| 요소당 물질점 | 4 (회전 · 원기둥 · 막대 인쇄) · 원판 §7.3 인쇄 없음 (그림 4a 점 간격 = h/2 와 맞다 [판독]) | [인쇄] p.187 · p.188 · p.191 |
| 시간 간격 | 회전 0.1 · 원기둥 0.2 · 0.1 · 0.05 µs · 원판 0.001 · 막대 0.005 · 안정 조건 · CFL 인쇄 없음 | [인쇄] · [미확인] |
| 시간 적분 | 명시 (6.2 · 6.4) · 위치 = 사상된 격자 속도 · 점 속도 = 가속도 증분 (FLIP) | [인쇄] p.186 |
| 질량 | 일관 질량 (3.8 · 6.6) → 행 합 대각 (6.1 · 6.7) · 물질점 질량 고정 | [인쇄] p.184–186 |
| 재료 | 구리 탄성 (E 126 GPa · ν 0.35 · ρ 8.92 [단위 §3-8]) · 무차원 탄성 (E 1000 · ν 0.3 · ρ 1000) · von Mises 선형 경화 (c₁ 100 · c₂ 400) | [인쇄] p.187 · p.189 · p.191 |
| 계산 비용 | 숫자 없음 — 회전 시험 *"the computational effort is greater"* · 결론 *"additional cost … maps between the material points and the grid"* | [인쇄] p.187 · p.194–195 · [미확인] 시간 · 기계 |
| 코드 | 이름 없음 · *"constitutive equation subroutines are also traditional"* (p.184) | [미확인] |
| 맞춘 값 | **없음** — 실험 대조 없음 · 검증 = 균일 병진 정확 · 회전 · 원기둥 해석 진동수 대비 분산 · 소산 · 충돌 에너지 · 운동량 | [인쇄] |

### 4-3. 입자 처리 ★
- 'particle' = **물질점** = 물질 부분 영역 Ω_P 의 기준점 · 질량 M_P · 비응력 · 변형률 · 이력 변수를 싣는다 — 알갱이가 아니다.  물체 (원기둥 · 원판 · 막대 · 층) 는 연속체이고 물질점 수백 – 만 개로 이산화된다 [카드 산술].
- 물질점은 구성식마다 따로 배열 (*"the material point is added to an array associated with a specific constitutive equation"* p.185) → **섞인 셀** 자동 처리: *"By following material points, the appropriate constitutive equation is invoked no matter how many or what kind of material points are located within a single element"* (p.195 · `txt_p17_mixed_cells_single_valued_no_slip.png`).
- 접촉 = 격자 속도장 하나 — 물체 경계 · 접촉면을 따로 추적하지 않는다 (*"no slideline algorithm"*).  분리는 된다 (그림 4c–d · 9) · 미끄럼은 안 된다.
- 형상 변화: 물질점 위치가 그대로 형상 — 탄소성 원판의 평평해짐 (§7.5 · 그림 9) 이 형상 변화의 예 (수치 없음).

### 4-4. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **말 없음** (DEM · discrete element · granular · powder · friction 0 회 [카드 전문 검색]).  가까운 문장은 FE 쪽 (초록의 순수 Lagrange 뒤틀림 · 재격자화 보간) 과 SPH 쪽: *"as material points separate, the basis functions can become severely distorted and special algorithms to handle such cases must be constructed. The proposed approach uses a regular grid so the method is fundamentally different from smooth particle hydrodynamics and the problem with basis functions does not arise"* (p.195).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — 이유 = 초록 세 문장 (Euler 는 물질점 추적이 어렵다 · 순수 Lagrange 는 뒤틀려 강성 행렬이 나빠져 *"mesh lockup or entanglement"* · 재격자화는 *"interpolation must be performed for history dependent variables, a process which can introduce errors"*) + 섞인 셀 (*"In purely Eulerian codes, elements (cells) that contain more than one material require special treatment … an algorithm is usually developed to partition element variables among the materials present"* p.195).  우회 = 물질점이 이력 변수를 싣고 격자를 다시 깐다.  비용 = 점 ↔ 격자 사상 (*"The additional cost of the method over existing finite element algorithms appears in the form of maps between the material points and the grid. The benefit is no mesh distortion and, consequently, no need to remesh in the event that large deformations occur"* p.194–195) — **숫자 없음**.  단, 이 논문 자신은 **작은 변형** 꼴만 다룬다 (p.180) — 큰 변형 소성은 정식화 밖이다.
3. **2D / 3D** — 예는 전부 2D 평면 변형 (*"Example solutions in two dimensions"* 초록 · *"The current implementation in 2-D allows combinations of straight line segments, circles and ellipses"* p.185).  식은 차원에 무관하게 적혔다 (3D 문장 둘 · p.186).  **2D → 3D 전이에 대한 말 없음**.
4. **압력을 뺄 때의 거동** — 누름 · 탈압 실험은 없다.  가장 가까운 것 = 탄소성 충돌 뒤 **분리 (하중 없음)** 에서 *"residual plastic strains can prevent the elastic strain (and stress) from achieving a zero state even in the unloaded condition"* (p.191) · 영구 평평해짐 · 덜 벌어짐 (*"The amount of separation is not as large"*) — 수치 · 그림은 에너지 곡선뿐 (그림 8a · 변형 에너지 0.17–0.36 [판독]).

### 4-5. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| PIC (classical) | 유체를 Lagrange 질량점 (입자) 으로 · 입자에 질량과 위치만 (*"partially Lagrangian"*) |
| FLIP | *"full-particle"* PIC — 입자가 운동량 · 에너지를 포함한 모든 성질을 싣는다 · 격자 → 입자는 변화량 (가속도) 만 더한다 |
| 물질점 (material point) | 물질 부분 영역 Ω_P 의 기준점 · 질량 고정 · 응력 · 변형률 · 이력 변수를 싣는다 |
| 비응력 (specific stress) σ^s | 단위 질량당 응력 (ρσ^s = σ) — 점 질량과 함께 운동 방정식을 물질점 합으로 쓰게 한다 |
| 사상 행렬 [S] · 기울기 행렬 [G] | 현재 물질점 위치에서의 절점 기저 값 · 기울기 (*"stochastic matrix"*) |
| 일관 질량 · 대각 (행 합) 질량 | m_ij = Σ M_P S_iP S_Pj · 행 합을 대각에 (덩어리 질량) |
| 대류 단계 (convective phase) | 물질점 → 격자 사상 — 고정 격자에서 물질 이동을 다루는 단계 |
| 갱신 Lagrange (updated Lagrangian) | 걸음 끝 배치를 다음 걸음의 기준으로 — 이 방법의 격자는 한 걸음 동안 그렇게 읽힌다 |
| 섞인 셀 (mixed cells) | 한 요소 안에 재료가 여럿 — 물질점마다 구성식이라 따로 처리가 필요 없다 |
| slideline | FE 의 접촉면 알고리즘 — 이 방법은 쓰지 않는다 (no slip) |
| 분산 ω^d · 소산 γ | ω/ω^e (해석 진동수 대비) · E = E₀exp(−γωt/2π) 의 감쇠 지수 |
| 소성 변형률 경로 불변량 ē | ∫(2/3 ė^p:ė^p)^{1/2}dt (등가 소성 변형률) |
| locking · hourglassing | FE 요소의 과강성 잠김 · 영 에너지 모드 — *"no difficulties"* (상세 분석 없음) |

---

## 5. Figure set ★
| 그림 | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| **Fig. 1** (`fig_1.png` · 다시 자름) | (a) 처음 · (b) 나중 배치의 격자와 물질 부분 영역 · 기준 물질점 | 물질점 = 부분 영역 기준점의 그림 설명 |
| **Fig. 2** (`fig_2.png` · 손 크롭) | (a) 홈 파인 원기둥 위에서 본 물질점 · 격자 (b) 한 바퀴 뒤 표면 Ψ | 대류 단위 시험의 입력 · 결과 꼴 |
| **Fig. 3** (`fig_3.png` · 다시 자름) | 진동 원기둥 에너지 (a) h 0.08 · s 0.2 µs (b) 0.04 · 0.1 (c) 0.02 · 0.05 [캡션 h 는 인쇄 어긋남] | 분산 · 소산 판독 (γ 0.1315 · 0.0149 · 0.0042 [판독]) |
| **Table 1** (`tab_1.png` · 손 크롭) | s · sω^e · h · ω^d · γ 세 행 | ★ 지름당 셀 15 · 30 · 60 의 분산 · 소산 [카드 산술] |
| **Fig. 4** (`fig_4.png` · 다시 자름) | 탄성 원판 충돌 물질점 (a) t 1.0 (b) 1.5 (c) 2.0 (d) 2.5 | t 1.0 중심 거리 0.445 · 가장 가까운 점 0.053 [판독] |
| **Fig. 5** (`fig_5.png` · 다시 자름) | (a) 에너지 (b) 왼쪽 아래 원판 운동량 | 총 에너지 −4.3 % · 크기 비 0.93–0.94 · 시작 t 0.86 [판독] |
| **Fig. 6** (`fig_6.png` · 손 크롭) | 막대 – 층 충돌 물질점 t 0 – 5 | 두 번 모서리 충돌 · 회전 |
| **Fig. 7** (`fig_7.png` · 손 크롭) | 같은 시각의 격자 속도 화살표 (작은 속도 생략) | 충돌점 국소 속도 |
| **Fig. 8** (`fig_8.png` · 다시 자름) | 탄소성 충돌 (a) 에너지 (b) 운동량 | 총 에너지 −46 % · 크기 비 0.64 · 잔류 변형 에너지 [판독] |
| **Fig. 9** (`fig_9.png` · 다시 자름) | 탄성 ↔ 경화 원판 물질점 t 0.5 – 2.0 | 소성 원판 한쪽 평평해짐 (정성) |
| **Fig. 10** (`fig_10.png` · 다시 자름) | (a) 에너지 (b) 탄성 원판 · (c) 소성 원판 운동량 | 총 에너지 −32 % · 운동량 합 ≠ 0 [판독] |
| 식 크롭 37 (`eq_2_01_…` – `eq_7_05_…`) · 근거 문단 20 (`txt_p*`) | 식 (2.1)–(7.5) 전부 · 인용 문장 | 보고서 MPM 절 붙임 |

## 6. Post-processing ★
- **에너지**: 운동 · 탄성 변형 · 합 (그림 3 · 5a · 8a · 10a) — 계산 식 (물질점 합인지 · 격자인지) 인쇄 없음 [미확인].
- **운동량**: 원판별 x · y 성분 (그림 5b · 8b · 10b–c) — 원판별로 어떻게 셌는지 인쇄 없음 [미확인].
- **분산 · 소산**: ω^d = ω/ω^e (ω^e = 해석 진동수 · 계산 식 미인쇄) · 총 에너지 진폭을 E₀exp(−γωt/2π) 로 근사한 γ (p.188).
- **대류**: 한 바퀴 뒤 Ψ 표면 그림 (그림 2b) — 수치 오차 노름 없음.
- **판독 (이 카드)**: 스캔 원 해상도 (그림 3 · 10 = 400 dpi · 그 밖 300 dpi) 렌더 · 축선 옆 눈금을 찾아 선형 최소제곱 (잔차 ≤ 0.007 에너지 · 0.08 운동량 · 그림 10a 0.004 시간) · 그림 3 = 2D 아핀 (스캔 1–2° 회전) · 선 = 화소 열마다 잉크 덩어리 (실선 = 맨 위 덩어리) · 운동 에너지가 떨어지는 시각 = 둘째 덩어리가 맨 위에서 갈라지는 첫 열 · 그림 4a = 연결 성분 ≤ 12 px 를 점으로 · 두 원판은 k-평균 · 길이 단위 = 점 간격 h/2 가정 — digitized.csv note 열.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 다른 카드 · 지시서 출처를 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 하중 · 차원이 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| 이산화 | 물질점 + 매 걸음 다시 까는 고른 격자 · FE 절점 기저 · 점 질량 · 조각 상수 응력 | MLS-MPM · APIC · 2차 B-spline · 명시 · f32 [다른 카드 `hu2018_…` L498 (우리 코드 판독)] | **뼈대가 같다** (물질점 상태 · 격자 운동량 · 매 걸음 다시) — 기저 · 힘 식 (MLS) · 전달 (APIC ↔ FLIP 증분) 은 다르다 |
| 구성식 · 변형 측도 | 작은 변형 rate 꼴 σ̇ = T:ė · ė = D · 객관률 없음 [카드 해석] | F 갱신 F ← (I + dt·C)F · fixed corotated 응력 + Hencky 변형률 J2 반환 (SVD → 로그 변형률) [다른 카드 `hu2018_…` L26–L31 · L499 (우리 코드 판독)] | **정식화는 옮겨 오지 않는다** — 우리는 큰 변형 (유한 변형) 판 · 이 논문은 '이력 변수를 물질점에' 라는 구조만 준다 |
| 항복 정의 | von Mises σ̄ = (3/2 σ^d:σ^d)^{1/2} ≥ H = c₁ + c₂ē → c₁ = 일축 항복 응력 (일축이면 σ̄ = σ) [카드 산술] | MPM σ_y 0.30 GPa = Hencky 편차 변형 문턱 (일축 압축 환산 0.318 GPa) [다른 카드 `jeong2024_…` L265 · `kalnaus2023_…` L274] | 같은 'von Mises' 라도 문턱의 뜻이 다르다 → 인용 때 환산을 같이 적는다 |
| 항복 변형률 | c₁/E = 0.1 (무차원 원판 · 모델 선택) [인쇄 · 카드 산술] | 연화 재료 0.318/1.53 ≈ 21 % [다른 카드 `kalnaus2023_…` L305] · 실제 강성이면 ≈1.6 % | 둘 다 '모델 재료' — 실물이 아니다 |
| 접촉 | 한 속도장 → 자동 no-slip · 침투 없음 · 분리 가능 · ≈1 셀 앞에서 상호작용 시작 [판독 · 카드 산술] | 한 속도장 (붙음) · AM = 격자 장애물 (속도 0 고정) [다른 카드 `hu2018_…` L500 · L515 (우리 코드 판독: AM 마스크 노드 `grid_v = 0` = 정지 강체 · sticky)] | ★ **같은 성질의 원전** — 우리 SE–SE · SE–AM 계면이 붙는 이유가 이 논문 p.180 · p.195 의 문장이다 |
| 셀당 물질점 | 2D 요소당 4 (= 방향당 2) | 방향당 2 (셀당 8) [다른 카드 `steffen2010_…` §7-1 (`homel2017_…` L499 · `sadeghirad2011_…` L516)] | 방향당 2 는 같다 · 원문은 *"more or fewer material points per element"* 를 열린 문제로 남겼다 |
| 해상도 | 원기둥 지름당 셀 15 · 30 · 60 → ω^d 0.97 · 0.99 · 1.00 · γ 0.121 · 0.0126 · 0.0041 [인쇄 · 카드 산술] · 원판 지름 ≈ 8 셀 [카드 산술] | SE 지름 ≈ 1 µm ≈ 7 셀 (n_grid 384 · dx 0.141 µm) [다른 카드 `steffen2010_…` §7-1 (`sadeghirad2011_…` L517)] | 우리 SE 는 표 1 의 가장 거친 행 (15) 보다 거칠다 — 이 논문 원판 (≈8 셀) 과 비슷한 크기 · 그 원판의 총 에너지 −4.3 % 가 수치 소산 기준선이 될 수 있다 [카드 추론] |
| 시간 간격 | 원기둥 c_P s/h = 1.19 · 원판 0.023 · 막대 0.116 [카드 산술] · 안정 조건 미인쇄 | Courant 0.4 + 판 Mach [다른 카드 `steffen2010_…` §7-1 (`gritton2017_…` L538)] | 원문의 원기둥 행은 P파 Courant 1 을 넘는데도 안정했다 — 이 숫자를 우리 dt 근거로 쓰지 않는다 |
| 재료 | 구리 탄성 (E 126 GPa) · 무차원 E 1000 · ν 0.3 · ρ 1000 | MPM J2 · E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 · DEM E_eff 1.35 GPa (18 배 연화) · Heckel P_y 138 MPa [우리 기록 · 지시서] | 수치 전이 불가 — 랩 표준 (순수 SE 10–13 % · 1.64 g/cm³) 과 견줄 숫자 없음 |
| 하중 | 충돌 (속도 0.1414 · 처음 속도 / c_P 0.12) · 진동 (2 % 반지름 변형) · 회전 | 판 압축 ≈ 300 MPa · 판 Mach 0.01–0.03 (준정적) [우리 기록 · 다른 카드 `steffen2010_…` §7-1] | 동역학 ↔ 준정적 · 누름 · 탈압 없음 |
| 오차 · 검증 | 균일 병진 정확 · 회전 · 해석 진동수 대비 분산 · 소산 · 에너지 · 운동량 곡선 | 해석해 단위 시험 없음 · 격자 · 속도 사다리 [우리 기록 · 비교 문서 F 절] | ★ 단계 2 · U5 에 바로 쓸 시험 (§9) |

### 7-2. ★ 한 속도장 no-slip ↔ 우리 scaffold
- 원문: 한 속도장이 접촉을 *"automatically"* no-slip 으로 만든다 (p.179–180 · p.195) — 미끄럼을 풀려면 *"relaxation of the no slip condition"* (p.195 · 열린 문제) → Bardenhagen · Brackbill · Sulsky 2000 의 물체별 장 [다른 카드 `bardenhagen2000_…` L388: *"단일 속도장 MPM 에서는 침투가 막히는 대신 닿는 물체 사이 no-slip 접촉이 자동으로 걸린다"*].
- 이 카드의 판독이 더하는 것: **상호작용은 재료가 닿기 ≈1 셀 앞에서 시작** (§7.3 틈 0.9–1.2 h · §7.6 0.75–1.05 h [판독 · 카드 산술]) — 두 물체의 물질점이 같은 격자 노드에 사상되는 순간부터 같은 속도를 받기 때문이다 [카드 해석].
- 우리 쪽 [카드 추론]: ① SE 낟알 사이 · SE–AM 사이의 **1 셀 (≈0.14 µm @ n_grid 384) 아래 틈은 이 방법에서 닫힌 것처럼 움직인다** → 기공 · 피복 판정 (단계 0 · 7) 에서 셀 아래 틈을 '열림' 으로 세지 않는 한정 ② 우리 SE–AM 계면의 붙음 (후보 A 의 한계) 은 이 논문이 이름 붙인 성질 그대로 — 인용처 = p.180 · p.195 ③ 후보 A′ (입자별 장) 와의 대조 시험은 '상호작용 시작 틈 / h' 를 같은 칸으로.

### 7-3. ★ 이력 변수 · 작은 변형 꼴 ↔ 우리 F 기반 J2
- 가져올 것: 이력 변수 (소성 변형률 · 경화 변수) 를 물질점이 끝까지 싣는 구조 (Step 5) · 섞인 셀 = 물질점마다 구성식 (p.195) — 우리 AM + SE 한 칸이 이 원리로 선다 (AM 은 우리 쪽에서 물질점이 아니라 장애물이라는 차이).
- 가져오지 말 것: 작은 변형 rate 꼴 (ė = D · 객관률 없음) — 우리 압밀은 SE 변형이 크다 · 우리 코드는 F · SVD · 로그 변형률 [다른 카드 `hu2018_…` L30].  c₁ = 0.1E · c₂ = 400 같은 수.
- 정의 차: 이 논문의 c₁ = 일축 항복 응력 ↔ 우리 σ_y = Hencky 편차 변형 문턱 (일축 압축 0.318 GPa) [다른 카드].

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = MPM (MECHANICS 쪽) 의 **뼈대 원전** — 물질점 · 이력 변수 · 섞인 셀 · 한 속도장 접촉.  DEM · 접촉망 · 수송은 없다.
- 없는 것: 알갱이 · 분말 · 압밀 · 마찰 · 미끄럼 · 큰 변형 정식화 · 3D · 실험.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = 지시서 · 다른 카드: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM MLS-MPM · 2차 B-spline · 방향당 2 PPC · E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 = **2D 연속체 물체의 입자법 정식화 + 시험** — 랩 표준과 나란히 놓을 숫자는 하나도 없다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ① **부분 질량 없는 생성** (p.185) — 물체 질량 · 부피가 격자가 물체를 어떻게 자르느냐에 따라 바뀔 수 있다 (§7.3 M 130.6 ↔ §7.6 121.3 [판독 · 카드 산술 · 원인 미확인]) → 우리 기공 연산자의 고체 부피를 **물질점 수가 아니라 기하 (DEM 덤프 부피)** 로 세는 지금 방식의 근거 문장 · 셀당 점 수 수렴을 결과 전 칸으로 ② **에너지 장부** — 탄성 충돌의 총 에너지 −4.3 % 가 '수치 소산' (원문 *"some numerical dissipation"*) → 소성 소산을 말하기 전에 같은 해상도의 탄성 기준선을 먼저 등록 ③ 한 속도장의 ≈1 셀 앞 상호작용 → 셀 아래 틈을 기공으로 세지 않는 한정 [카드 추론] | 기공 · 압밀 판정 없음 |
| **단계 1** (3D 메모리 · 장 수) | 한 속도장 = 격자 장 하나 (이 논문의 기준 비용) · 물질점 상태 (2D: 위치 · 속도 · 질량 · 비응력 · 변형률 · 소성 변형률 · 경화) → 3D 로 옮기면 점당 ≈ 26 스칼라 (3 + 3 + 1 + 6 + 6 + 6 + 1) [카드 산술] · *"matrices … are never formed"* (p.186) → 메모리 = 벡터뿐 | 3D 계산 · 입자별 장의 메모리 없음 |
| **단계 2** (2D MPM 코드 · 단위 시험) | ★★ **이 논문의 몫** — 2D 시험 여섯을 그대로 단위 시험으로: ① 균일 병진 = 정확 (U0 꼴 · p.187) ② 강체 회전 한 바퀴 (51 × 51 · s 0.1 · 628 걸음 · 4 점/요소 · 처방 속도 7.3–7.4) ③ 원기둥 기본 모드 — 해석 진동수 x J₀(x) = ((1−2ν)/(1−ν)) J₁(x) (x = 2.18677 @ ν 0.35 [카드 산술]) 대비 ω^d · γ 를 지름당 셀 15 · 30 · 60 에서 (표 1 · Courant 고정) ④ 같은 탄성 원판 충돌 (E 1000 · ν 0.3 · ρ 1000 · ±(0.1, 0.1) · h 0.05 · s 0.001) 의 총 에너지 · 운동량 · 상호작용 시작 시각 ⑤ 탄소성 원판 충돌 (c₁ 100 · c₂ 400) ⑥ 탄성 ↔ 경화 원판 (섞인 셀) | 해석해는 ③ 뿐 (원문은 식을 인쇄하지 않음) · 회전 오차 수치 · 판정 허용폭 없음 |
| **단계 3** (2D 접촉 표현 비교 · 한 속도장 ↔ 입자별 장) | ★ **한 속도장 쪽의 원전 문장** (p.180 · p.195) + 판독: 상호작용 시작 틈 0.75–1.2 h · 탄성 원판의 운동량 크기 비 0.93–0.94 · 총 에너지 −4.3 % [판독 · 카드 산술] → 단계 3 의 결과 전 대조 칸 (같은 원판 충돌을 두 표현으로: 시작 틈 / h · 되튐 비 · 에너지).  열린 문제 *"relaxation of the no slip condition"* (p.195) = 입자별 장이 푸는 것 | 입자별 장 · 마찰 · 미끄럼 계산 없음 |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 이력 변수를 물질점에 두는 구조 · von Mises 선형 경화 (7.5) 의 정의 (c₁ = 일축 항복) — 우리 σ_y (Hencky 문턱 · 일축 압축 0.318 GPa) 와 **정의가 다르다** [다른 카드 `jeong2024_…` L265] → 문헌의 'σ_y' 를 견줄 때 환산 칸 | 작은 변형 정식화 (우리 압밀에 못 씀) · 순수 SE · 기공 · 다공 소성 (캡) 없음 · 랩 표준과 견줄 숫자 없음 |
| **단계 5** (3D 복합 압밀) | ★ **섞인 셀 원리** — *"the appropriate constitutive equation is invoked no matter how many or what kind of material points are located within a single element"* (p.195) · 한 격자에 탄성 물체와 탄소성 물체 (§7.6) = 단단한 몸 + 무른 몸을 한 계산에 둔 첫 예 (단 강성 대비 없음 — 두 원판 E 같다) | AM ↔ SE 강성 대비 (우리 MPM 의 AM = 움직이지 않는 장애물) · 하중 몫 · 압밀 없음 |
| **단계 6** (탈압 · 되돌아옴) | ★ *"residual plastic strains can prevent the elastic strain (and stress) from achieving a zero state even in the unloaded condition"* (p.191) · 분리 뒤 변형 에너지 0.17–0.36 [판독] (탄성 경우 0.13–0.21 = 진동 몫) → 탈압 뒤 남는 탄성 에너지를 '잔류 응력' 지표로 쓰되 **진동 몫 (탄성 기준선) 을 빼고** 읽는다 [카드 추론] | 누름 · 탈압 · 되돌아옴 양 없음 · 잔류 형상 수치 없음 (*"not plotted"*) |
| **단계 7** (형상 · 피복 · 수송) | 없음 (수송 없음).  흐름 밖: §9 행동 6 | — |
| **후보 D0** (지금 DEM) | 없음 (DEM 0 회) | — |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 바탕만: 한 속도장 = no-slip 이 기본값이고 규칙 (미끄럼 · 분리 조건) 은 따로 넣어야 한다 · 경계 조건은 열린 문제 (p.195) · 변위 처방 = 격자 노드에서 (p.183) | 접촉 규칙 · 판 경계 계산 없음 |
| **후보 A** (MPM 강체 AM + SE 한 속도장) | ★ **이 후보의 뼈대 원전** — 한 속도장 · 섞인 셀 · 이력 변수 물질점 · 자동 no-slip.  인용처 = p.180 (*"the algorithm is actually one of no slip"*) · p.195 | 강체 (움직이는 단단한 몸) 결합 · 장애물 경계 없음 |
| **후보 A′** (입자별 속도장) | 출발점: 이 논문이 *"relaxation of the no slip condition"* 를 열린 문제로 남겼다 (p.195) → Bardenhagen 2000 이 푼 것 [다른 카드] | 입자별 장 계산 없음 |
| **후보 B** (입자별 FE + 접촉) | ★ 인용할 문장: 순수 Lagrange 격자는 *"severe mesh distortion and the consequence is ill conditioning of the element stiffness matrix leading to mesh lockup or entanglement. Remeshing prevents the lockup and tangling but then interpolation must be performed for history dependent variables, a process which can introduce errors"* (p.179) · FE 접촉 = slideline 알고리즘이 필요 (p.195 의 대비) | 입자별 FE 계산 · 큰 변형 문턱 수치 없음 |
| **후보 C · C′** (큰 변형 · 탄소성 접촉 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀) | 없음 (von Mises = 압력 무관 · 부피 불변 소성 · 캡 없음) | — |
| **U0–U6** | **U0** = 균일 병진 정확 (p.187) · **U1** = 원기둥 기본 모드의 지름당 셀 15 · 30 · 60 분산 · 소산 (표 1 [카드 산술]) — 입자 하나의 '진동' 해상도 (압축 아님) · **U3** 근처 = 탄소성 원판 충돌 뒤 영구 평평해짐 · 잔류 탄성 에너지 (§7.5 · 수치 없음) · **U5** = ★ 같은 탄성 원판 충돌 (§7.3) — 비슷한 강성 물체끼리 충돌의 표준 시험 (판독 기준선 −4.3 % · 0.93–0.94 · 시작 틈 0.9–1.2 h) · 섞인 재료 충돌 (§7.6) | U2 (경사면 마찰) · U4 (판 분리) · U6 (조밀 충전 압축) 없음 |
| **R1–R7** | **R1** 두 물체가 움직이며 하중을 주고받음 (충돌 · 압밀 아님) · **R2** 분리 = 됨 · 미끄럼 = **안 됨** (p.195) · **R3** 재료 종류는 물질점 배열로 기억 · 같은 재료 낟알 경계는 속도장에서 구분 안 됨 [카드 해석] · **R4** 하중 없는 상태의 잔류 탄성 변형 (p.191 · 정성) · **R5** 맞춘 값 0 (모델 수 선택) · **R6** 형상 변화 = 됨 (평평해짐 · 수치 없음) · **R7** 없음 (*"material failure zone when softening occurs"* = 열린 문제 p.196) | 전부 정성 · 2D |
| **결과 전 대조 항목** | ① 우리 MLS-MPM 으로 §7.3 원판 충돌 (r ≈ 0.204 [카드 산술] · 요소당 2 × 2) — 총 에너지 변화 (이 논문 FLIP + 대각 질량 −4.3 % [판독]) · 운동량 크기 비 0.93–0.94 · 상호작용 시작 틈 0.9–1.2 h [판독 · 카드 산술] ② §7.5 탄소성 (c₁ 0.1E · c₂ 0.4E) — 총 에너지 −46 % · 크기 비 ≈0.64 [판독] ③ 원기둥 기본 모드 ω^d · γ (표 1 · 해석 ω = 1.7353 × 10⁶ rad/s [카드 산술]) — 맞추는 데 쓰지 않음 | 랩 표준 순수 SE (10–13 % · 1.64 g/cm³) 와 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: 구리 탄성 · 무차원 탄성 / von Mises 원판 ↔ 우리 LPSCl (MPM J2 E 1.53 GPa · ν 0.49 · DEM E_eff 1.35 GPa) · NCM · 2D 평면 변형 ↔ 3D 무질서 침대 · 충돌 · 진동 동역학 ↔ 준정적 판 압축 (≈300 MPa) · 작은 변형 rate 꼴 ↔ 큰 변형 F 기반 · 고른 물질점 배치 · 해석적 형상 ↔ DEM 덤프 씨앗 · AM 장애물.  ⇒ 값은 하나도 옮기지 않고 **뼈대 · 한 속도장 접촉의 성질 · 시험 꼴 · 인용 문장**만 옮긴다.

## 9. 적용 인사이트 (행동)
1. **U5 원판 충돌을 우리 코드로 (단계 2 · 3)**: §7.3 설정 (E 1000 · ν 0.3 · ρ 1000 · ±(0.1, 0.1) · h 0.05 · s 0.001 · 반지름 0.204 [카드 산술]) 을 우리 MLS-MPM 에 넣고 결과 전에 등록: 총 에너지 변화 · 운동량 크기 비 · **'운동 에너지가 떨어지는 시각 ↔ 자유 비행 접촉 시각' 으로 잰 상호작용 시작 틈 / h**.  같은 시험을 후보 A′ (입자별 장) 로 돌려 같은 칸에 놓는다.
2. **셀 아래 틈의 한정 (단계 0 · 7)**: 한 속도장에서는 ≈1 셀 앞에서 상호작용이 시작된다 [판독 · 카드 산술] — SE–SE · SE–AM 사이 1 셀 (≈0.14 µm) 아래 틈은 기공 · 피복 판정에서 '열림' 으로 세지 않는다는 문장을 결과 전 등록에 넣는다.
3. **탈압 뒤 잔류 에너지 읽기 (단계 6)**: 하중을 뺀 뒤의 탄성 에너지 = 진동 몫 + 잔류 응력 몫 (p.191) — 탄성 기준선 (같은 해상도 · 같은 하중 이력의 탄성 재료) 을 먼저 돌려 진동 몫을 뺀다.
4. **원기둥 기본 모드 해석해 (단계 2 · U1)**: x J₀(x) = ((1−2ν)/(1−ν)) J₁(x) 로 ω 를 미리 계산 → 지름당 셀 7 · 15 · 30 (우리 SE 의 7 셀을 더해) 에서 분산 · 소산.  표 1 은 s · h 를 함께 반으로 했으니 Courant 를 고정한 채 비교.
5. **인용 (보고서 MPM 절)**: '이력 변수를 물질점에' 의 원전 = 이 논문 초록 · p.180 · p.193–194 · '한 속도장 = 자동 no-slip' 의 원전 = p.180 · p.195 · '하중 없는 상태의 잔류 탄성 변형' = p.191.  인용 때 **작은 변형 · 2D 충돌 예** 한정어를 붙인다.
6. **흐름 밖 (복셀 수송)**: 원문의 *"In purely Eulerian codes, elements (cells) that contain more than one material require special treatment … an algorithm is usually developed to partition element variables among the materials present"* (p.195) — 물질점을 격자 칸의 상으로 다시 찍는 우리 복셀 수송 계산은 칸 하나에 상 하나를 두므로 이 '섞인 셀' 문제를 그대로 진다 [카드 추론] → 칸 안 상 비율 · 찍는 우선순위를 보고 칸에 둔다.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "For history-dependent constitutive equations the material points must be followed: purely Lagrangian meshes distort and lock or tangle, and remeshing requires interpolation of history-dependent variables, which introduces errors; the particle (material point) method instead carries plastic strain and hardening parameters on material points and solves the momentum equation on a grid that is reset every step (Sulsky, Chen & Schreyer, *Comput. Methods Appl. Mech. Engrg.* 118 (1994) 179–196; small-deformation formulation, 2-D examples)."
- "Because the grid velocity field is single valued, contact between bodies is automatically no-slip and interpenetration cannot occur, so no contact (slideline) algorithm is needed (Sulsky et al., 1994)."
- "Residual plastic strains can keep the elastic strain and stress non-zero even in the unloaded condition (Sulsky et al., 1994, two-dimensional elastic-plastic disk impact)."
- 국문 (한정어와 함께): *"소성처럼 이력에 의존하는 재료는 물질점을 따라가야 한다 — 격자를 물체에 붙이면 뒤틀리고, 다시 깔면 이력 변수를 보간해 오차가 생긴다.  MPM 의 원전 (Sulsky 외 1994) 은 소성 변형률 · 경화 변수를 물질점에 싣고 운동량만 매 걸음 다시 까는 격자에서 풀어 이를 피했다 (작은 변형 정식화 · 2D 충돌 예).  이 방법은 격자 속도장이 하나라 물체 사이 접촉이 자동으로 미끄럼 없는 접촉이 된다."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**: §3-8 의 1–4.
**카드가 본 한계**
1. **작은 변형 rate 꼴 · 객관률 없음** — 큰 변형 소성의 정식화로 인용하지 않는다 (큰 변형 MPM 소성 = Love · Sulsky 2006 등 · 카드 없음).
2. **2D 평면 변형 · 충돌 · 진동 · 회전** — 압밀 · 분말 · 알갱이 · 탈압 실험 · 3D 계산 없음.
3. 소성 결과는 정성 — 잔류 형상 그림 없음 (§7.5) · 판독 에너지 −46 % 는 소성 + 수치 소산의 합 (나눠 적지 않음).
4. 'MPM' 이름 0 회 — '원전' 이라 쓸 때는 1995 판과 함께 (방법 = 1994 · 이름 = [미확인]).
5. 원문 안 단위 · 기호 어긋남 (ρ · ω · h · (6.3) · 참고 번호) — 인용 때 표지.
6. 상호작용 시작 틈 '≈1 셀' 은 이 카드의 판독 · 산술 (원판 반지름 미인쇄 · 자유 비행 가정 · 판독 시각 ±0.02) — 원문 주장 아님.
7. §7.6 운동량 합 ≠ 0 은 판독이고 원인 미상 — 이 논문의 보존성 결함으로 단정하지 않는다.
8. 원기둥 c_P s/h 1.19 는 카드 산술 (원문은 안정 조건 · 사용한 파속을 말하지 않는다).

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| [4] | D. Burgess, D. Sulsky and J.U. Brackbill, Mass matrix formulation of the FLIP particle-in-cell method, J. Comput. Phys. 103 (1992) 1-15. | ★ 사상 (4.3) 의 보존 (운동 에너지 · 선 · 각운동량) 과 대각 질량의 소산 정량 — 우리 덩어리 질량 판의 근거 · 카드 없음 |
| [5] | D. Sulsky and J.U. Brackbill, A numerical method for suspension flow, J. Comput. Phys. 96 (1991) 339-368. | ★ 한 속도장 → 침투 없음 · no-slip 접촉의 첫 판 · 원기둥 진동 선행 결과 · 카드 없음 |
| [2] | J.U. Brackbill and H.M. Ruppel, FLIP: a method for adaptively zoned, particle-in-cell calculations of fluid flows in two dimensions, J. Comput. Phys. 65 (1986) 314-343. | FLIP 원전 · 사상 · 물질점 생성의 원형 (§5) · 카드 없음 |
| [3] | J.U. Brackbill, D.B. Kothe and H.M. Ruppel, FLIP: a low-dissipation, particle-in-cell method for fluid flow, Comput. Phys. Comm. 48 (1988) 25-38. | 대각 질량 소산 정량 · 카드 없음 |
| [8] | D.J. Bensen, Computational methods in Lagrangian and Eulerian hydrocodes, Comput. Methods Appl. Mech. Engrg. 99 (1992) 235-394. | Lagrange · Euler · 접촉 알고리즘 리뷰 (본문 'Benson') — 한 속도장 혼합 이론의 미끄럼 불가 비판 [다른 카드 `bardenhagen2000_…` L32] · 카드 없음 |
| [1] | F.H. Harlow, The particle-in-cell computing method for fluid dynamics, in: B. Adler, S. Fernbach and M. Rotenberg, eds. Methods for Computational Physics, Vol. 3 (1964) 319-343. | 고전 PIC · 가리킨 카드 L278 의 'Harlow 1963' 과 연도 차 · 카드 없음 |
| [9] | P.K. Smolarkiewicz, A fully multidimensional positive definite advection transport algorithm with small implicit diffusion, J. Comput. Phys. 54 (1984) 325-362. | 회전 시험 (홈 파인 원기둥) 의 출처 · 카드 없음 |
| [6] · [7] | C.W. Hirt, A.A. Amsden and J.L. Cook, An arbitrary Lagrangian-Eulerian computing method for all flow speeds, J. Comput. Phys. 14 (1974) 227-293. · T.B. Belytschko, J.M. Kennedy and D.F. Schoeberle, Quasi-Eulerian finite element formulation for fluid-structure interaction, J. Pressure Vessel Technol. 102 (1980) 62-69. | ALE 바탕 (Lagrange 단계 + 대류 단계) · 카드 없음 |
| [10] | L.D. Libersky, A.G. Petschek, T.C. Carney, J.R. Hipp and F.A. Allahdadi, High strain Lagrangian hydrodynamics: a three-dimensional SPH code for dynamic material response, J. Comput. Phys. 109 (1993) 67-75. | SPH 대비 (기저 뒤틀림) · 카드 없음 |
| (이 논문을 인용한 정본 카드) | `bardenhagen2000_…` · `bardenhagen2004_…` · `bardenhagen2005_…` · `guilkey2003_…` · `steffen2008_…` · `steffen2010_…` · `nairn2015_…` · `devaucorbeil2020_…` · `stomakhin2013_…` · `klar2016_…` | §0-1 대조표 |

## 13. [미확인] 목록 (본문 18 쪽 전수에 없음)
1. DOI (인쇄 없음 · PII · SSDI 만).
2. 원판 반지름 · §7.3 의 요소당 물질점 수 (카드 산술 r ≈ 0.204 · 그림 4a 점 간격 = h/2).
3. 절점 기저의 차수 (이중선형인지).
4. 구성식 서브루틴의 응력 적분 (반환 사상) 알고리즘.
5. 에너지 · 운동량의 계산 정의 (물질점 합 · 격자) · §7.6 운동량 합 ≠ 0 의 원인 · 'switches' 의 뜻.
6. 회전 시험의 오차 수치.
7. 계산 비용 (시간 · 기계 · 물질점 수).
8. §7.5 잔류 형상 수치 (그림 없음 · 'not plotted').
9. 안정 조건 · CFL · 원기둥 예에서 쓴 파속 (카드 산술 c_P s/h 1.19).
10. ω^e 의 계산 식 (원문은 값만 · 카드가 평면 변형 반지름 모드 식으로 재현).
11. 원기둥 계산이 단면 전체인지 4 분의 1 인지 · 물질점 수.
12. 이름 'material point method' 의 첫 출현 (1995 판인지 — 카드 없음) · 가리킨 카드의 'Harlow 1963' 서지.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 본문 18 쪽을 글자 층 (OCR) + 전 쪽 렌더 (110 dpi 훑기 · 크롭은 스캔 원 해상도) 로 읽음 · 식 37 개는 렌더에서 확인.  서지 = 첫 쪽 머리 · 접수 · 수정 · 교신 · ISSN 줄 · 감사 (p.196).  원문 낱말 셈 (OCR · 대소문자 무시): 'material point method' 0 · 'MPM' 0 · 'material point' 69 · 'plastic' 19 · 'history' 10 · 'hardening' 9 · 'slip' 4 · 'unload' 1 · 'contact' 5 · DEM (discrete element) 0 · 'friction' · 'granular' · 'powder' · 'compact' · 'sphere' · 'Jaumann' · 'objectiv' 0 · 'three dimension' 1 · 'two dimension' 2 · '2-D' 1 · 'locking' · 'hourglass' 1.
- 그림 크롭 **68 장** = 도구 7 (Fig. 1 · 3 · 4 · 5 · 8 · 9 · 10) **전부 다시 자름** (스캔 쪽이라 도구 크롭이 쪽 전체 폭 띠였고 캡션이 잘리거나 (6) · 그림 3 은 아래 두 패널 가로축 띠 50 pt 만) + 손 크롭 61 (Fig. 2 · 6 = OCR 이 캡션을 'Fig, 2,' 로 읽어 도구가 놓침 · Fig. 7 = 도구가 '거의 백지 0.992' 로 뺌 · Table 1 = 도구가 표를 안 냄 · 식 37 = 식 번호마다 하나 · 근거 문단 20 · 그중 7 장은 2–3 조각을 이음).  전부 Read 로 열어 확인 · `figures.json` 의 `recrop` · `manual_crop` · `missing_labels_resolved` · `note_manual`.
- 판독: digitized.csv 144 행 — 축 보정 · 선 · 점 판독 방법을 note 열에.  산술 확인: 표 1 의 sω^e = 0.35 ↔ 해석 ω 1.7353 × 10⁶ rad/s × 0.2 µs = 0.347 ✓ (ρ 8920 kg/m³ 일 때만) · 1.68/1.73 = 0.971 ✓ ω^d · 2π/(Ωs) = 628.3 ✓ · 0.133R = 0.080 cm ✓ (인쇄 '0.80 cm' ✗) · 원판 M = KE₀ (원판 둘 합)/v² = 2.611/0.02 = 130.6 ↔ 운동량 판독 12.8–12.96/0.1 = 128–130 ✓.
- 2 차 인용 대조: `bardenhagen2005_…` L278 (가리킨 카드) · `bardenhagen2004_…` L227 · L283 · L611 · `guilkey2003_…` L351 · `steffen2010_…` L337 · `steffen2008_…` L401 · `nairn2015_…` L624 · `devaucorbeil2020_…` L25 · L74 · `klar2016_…` L64 · `stomakhin2013_…` L56 · L192 · `cummins2002_…` L85 · L93 — 고치지 않았다 (카드 문제 = 정독 출력 batch_81 의 "카드 문제" 절).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (556 장 · 이 카드 전) + 'sulsky' · 'particle method for history' · '179–196' grep — 카드 없음 (이 논문을 인용만 한 카드 10 장 · 작성 중 rebase 로 들어온 `cummins2002_…` 포함 11 장).  같은 저자 · 같은 해 다른 카드 없음.

## 🔗 관련 카드
- MPM 계보 (이 논문 → 접촉 → 일반화): `bardenhagen2000_mpm_granular_multibody_frictional_contact` (Sulsky 공저 · 이 논문의 no-slip 을 물체별 장으로 풀어 마찰 · 분리) · `bardenhagen2001_mpm_improved_contact_granular_stress_waves` · `bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing` (이 논문 = GIMP 의 특수형) · `bardenhagen2005_mpm_foam_densification_simulation` (가리킨 카드 · 계보 L278) · `devaucorbeil2020_mpm_after_25_years_review` (25 년 리뷰).
- MPM 수치 · 구현: `guilkey2003_implicit_mpm_newton_quasistatic_fem_comparison` · `steffen2008_mpm_implementation_choices_gimp_bspline_boundary` · `steffen2010_mpm_space_time_error_balance_moving_mesh` · `nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions` · `sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability` · `homel2017_mpm_field_gradient_partitioning_fracture_self_contact`.
- 같은 날 정본에 들어온 이웃: `cummins2002_implicit_mpm_granular_newton_krylov` (Cummins · Brackbill 2002 · 이 논문 = 그 ref. [1] · 알갱이마다 속도장 MPM 의 암시 판).
- 우리 MPM 계열 (MLS · 소성 반환): `hu2018_mls_mpm_cpic_two_way_rigid_coupling` · `stomakhin2013_mpm_snow_elastoplastic` · `klar2016_dp_sand_animation`.
- MPM 압밀 (변형 입자): `nezamabadi2022_mpm_cd_plastic_particle_compaction` · `nguyen2017_mpm_bpm_deformable_particle_compaction`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
