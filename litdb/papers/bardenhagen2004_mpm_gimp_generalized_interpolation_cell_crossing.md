# GIMP 원전 — 물질점에 '입자 특성 함수' χ_p 를 주어 MPM 의 보간을 일반화 (MPM = χ_p 가 델타인 특수한 경우 · 식 34) · contiguous particle GIMP (상자 χ_p · C¹ 가중 · 식 40) · 셀 넘김 잡음의 기전 (균일 응력인데 격자 노드에 힘 불균형) 과 1D 막대 시험 넷 (준정적 중력 기둥 · 충격 · 셀당 입자 1/2/4 · 셀 크기 세 자리 수렴) ★★ 실험 · 접촉 · 소성 · 탈압 · 3D 구현 없음 — 1D 초탄성 막대 (무차원 E 10⁶) — Bardenhagen, Kober (CMES 2004)

> slug `bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing` · DOI `[미확인]` (PDF 에 DOI 미인쇄) · type `MPM (GIMP 원전 — 변분형 + Petrov–Galerkin 이산화로 MPM 을 일반화 · 입자 특성 함수 χ_p · 가중 함수 S̄_vp · ∇S̄_vp (식 19–20) · MPM = 델타 특수형 (식 34) · contiguous particle GIMP (상자 χ_p · C¹ · 식 36–40) · 입자 폭 고정 'GIMP' ↔ 추적 'Finite GIMP' · 1D 초탄성 막대 σ = E(F − 1) 시험 넷 (준정적 중력 기둥 · 충격 · 셀당 입자 1/2/4 · 셀 크기 0.01–10 수렴) · 실험 없음)` · PDF `43049b95-16._The_generalized_interpolation_material_point_method.pdf` (20 쪽 = 본문 19 쪽 + 빈 쪽 1 · 글자 층 온전 · 보충 자료 없음) · digested `2026-11-12` · status ✅
>
> ⚠ **먼저 읽을 것** — ① 시험은 전부 **1D 초탄성 막대** (σ = E(F − 1) · E = 10⁶ · ρ₀ = 1 · 길이 50 · 파속 1000 · *"Any consistent set of units suffices"*) 다 — **LPSCl · NCM 이 아니고 분말 · 입자 층 · 접촉 · 소성도 아니다.  절대값 전이 0 건.**  가져오는 것은 **식 (가중 함수의 일반 꼴 · MPM 과 GIMP 의 관계) · 셀 넘김 잡음의 기전 · 시험 설계 (해석해가 있는 두 1D 문제 · 오차 노름 식 47 · 셀 크기 · 셀당 입자 수 · 재하 속도 사다리)** 와 **저자가 적은 한계**뿐이다.
> ② **3D 구현이 없다** — 저자 스스로 *"implementation of GIMP methods with finite, deforming particles in three dimensions does suffer a practical complication … This may need to be done numerically in general.  The investigation in the following section is performed in one–dimension for simplicity."* (p.484–485).  2D 계산도 없다.
> ③ **접촉 · 다물체 · 소성 · 하중 제거 · 에너지 수지가 없다** — 본문에 'contact' 0 회 (참고문헌 제목 한 번) · 'plastic' 0 회 · 'unload' 0 회 · 'energy' 는 자금 줄 (*Department of Energy*) 한 번 · DEM · 'discrete element' 0 회 [카드 전문 검색].  비탄성 (*inelastic*) 은 **주장으로만** 세 번 나온다 (초록 · p.487 · 결론) — 비탄성 재료로 계산한 예는 없다.
> ④ 시험 변형은 작다 — 준정적 기둥은 끝 변위 = 셀 하나 (평균 변형률 2 % · 바닥 4 % [카드 산술]), 충격은 F = 0.98 (2 %) [인쇄 식 46 · 카드 산술].  저자: *"In both cases examined here average deformations are small, but are sufficient to cause particles to cross cell boundaries."* (p.487).  **큰 변형 (짝 카드 2005 판의 90 % 압축) 은 시험되지 않았다.**
> ⑤ 그림에서 읽은 값은 화소가 아니라 **PDF 그리기 명령의 경로 좌표**에서 읽었다 (11 장 모두 벡터 · gnuplot / xfig 꼴 · 축은 눈금 글자 중심의 최소제곱 사상 · 사상 잔차 ≤ 0.02 눈금 단위) — 그래도 원자료가 아니라 그림이므로 표지는 `[판독]` 이다.  **판독 원자료** = `litdb/figures/bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing/digitized.csv` (Fig. 4–11 의 표지 · 꺾은선 꼭짓점 2,489 행 + 요약 행 · 열 = figure, panel_state, series, x_name, x, y_name, y, note).
> ⑥ 표지: `인쇄` = 본문 · 캡션 · 그림 글자 · `[판독]` = 그림 경로 좌표에서 읽은 값 · `[카드 산술]` = 인쇄값 · 판독값에서 산술로만 (식 병기) · `[미확인]` = 논문에 없음 · `[카드 판독]` · `[카드 추론]` = 논문 밖 판단 · `[다른 카드]` = 정본의 다른 카드에 적힌 것 (slug 병기) · `[우리 기록]` = CLAUDE.md · 정본 카드에 적힌 우리 쪽 값.  쪽 = **학술지 쪽 (p.477–495) = PDF 쪽 + 476**.
>
> 짝 카드: `bardenhagen2005_mpm_foam_densification_simulation` — 이 논문의 contiguous particle GIMP 를 3D 발포체 압축 (공칭 90 %) 에 쓰고 Fig. 1 의 큰 변형률 튐을 이 논문으로 넘긴 카드 (§0-1 대조).  `bardenhagen2000_mpm_granular_multibody_frictional_contact` · `bardenhagen2001_mpm_improved_contact_granular_stress_waves` — 같은 제1 저자의 MPM 다물체 마찰 접촉 (이 논문은 인용만 · 접촉 없음).  `gritton2017_mpm_chemomechanical_coupling_silicon_anode` — MPM 변종 문헌 [32–37] 을 든 카드 (CPDI 사용) · 이 논문 = 그 ref. [37] 이라는 연결은 후보 표 (정독 b40) 의 것 (그 카드에 [37] 서지 줄 없음).  `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` — GIMP · CPDI 를 *"single-point, GIMP, CPDI"* 로 나란히 둔 카드.  `hu2018_mls_mpm_cpic_two_way_rigid_coupling` — 우리 MLS-MPM 이산화 (2차 B-spline 가중) 의 원전 — §4-8 에서 이 논문의 식 (40) 과 이어 붙인다.  `devaucorbeil2020_mpm_after_25_years_review` — MPM 변종 표의 GIMP 줄.

---

## 0. 이 논문이 우리에게 왜 중요한가 (한눈 positioning)

[DEM 우선 (수영)] 은 *"가압부터 탈압까지 한 모델 (MPM) 이 다 계산할 수 있는가"* 를 묻는다.  그 MPM 이 정말 믿을 만한 응력 · 반력을 내는지는 **격자 ↔ 물질점 보간의 매끈함**에 걸려 있고, 그 문제를 처음 식으로 정리하고 1D 시험으로 크기를 보인 원전이 이 논문이다.  읽을 까닭이 넷이다.

**(1) "MPM 은 큰 변형에서 응력 잡음을 낸다" 의 원문 근거와 기전이 있다.**

> *"Examples are used to demonstrate and explain numerical artifact noise which can be expected in MPM calculations.  This noise results in non-physical local variations at the material points, where constitutive response is evaluated.  It is shown to destroy the explicit solution in one case, and seriously degrade it in another.  History dependent, inelastic constitutive laws can be expected to evolve erroneously and report inaccurate stress states because of noisy input.  The noise is due to the lack of smoothness of the interpolation functions, and occurs due to material points crossing computational grid boundaries."* (초록 · p.477 · `txt_p1_abstract_noise_destroys_degrades.png`)

> *"Because of the discontinuous nature of the gradient of the weighting function used in MPM, a force imbalance develops when uniformly stressed material points register non–uniformly on the grid, i.e. different numbers of particles are in adjacent cells.  This force imbalance is proportional to the particle stress multiplied by the difference between the number of particles on each side of a grid vertex."* (p.488 · `txt_p12_cell_crossing_noise_force_imbalance.png`)

**(2) 가중 함수의 일반 꼴이 식으로 있다** — S̄_vp = (1/V_p)∫χ_p S_v dx · ∇S̄_vp = (1/V_p)∫χ_p ∇S_v dx (식 19 · 20).  χ_p 를 델타로 두면 MPM (식 34), 상자로 두면 contiguous particle GIMP (식 36–40).  ★ 이 카드의 산술 (§4-8): **식 (40) 에 l_p = L/2 (셀당 입자 하나) 를 넣으면 2차 B-spline 과 정확히 같다** (수치 확인 차 1 × 10⁻¹⁶) — 우리 MLS-MPM 의 2차 B-spline 가중 [다른 카드 `hu2018_…` §4] 을 이 논문의 틀 안에서 읽을 수 있는 자리.

**(3) 해석해가 있는 1D 단위 시험 두 개와 수렴 시험 설계가 숫자로 있다** — 준정적 중력 기둥 (식 42–44 · 끝 무게 W_f = 40,000) · 막대 충격 (식 46 · 충격 뒤 응력 −20,000) · 오차 노름 식 (47) · 셀 크기 0.01–10 (세 자리) × 셀당 입자 1 · 2 · 4 · 재하 속도 ×5 · ÷4 (Fig. 10–11).  우리 단계 2 (2D MPM 단위 시험) · U6 (해상도 수렴) 의 꼴 그대로다.

**(4) "격자를 조이면 MPM 은 오히려 나빠진다" 는 결과와 그 이유 (finite grid instability) 가 있다.**

> *"Increasing the resolution will always ultimately result in cell crossings, no matter how small the deformation."* · *"The low speed, explicit calculations presented here would be expected to be very susceptible to the finite grid instability."* (p.493 · `txt_p17_p18_convergence_finite_grid_instability_saturation.png`)

우리 압밀 MPM 도 **명시적 · 저속 (판 Mach 0.01–0.03 [우리 기록 · CLAUDE.md])** 이다.  조이면 좋아진다는 가정을 해상도 시험 전에 하지 말라는 원문 근거.

| 우리가 필요한 것 | 이 논문이 주는 것 |
|---|---|
| MPM 응력 · 반력이 수치 잡음을 얼마나 품는가 (단계 2 · 4 · U6) | 기전 (힘 불균형 ∝ 입자 응력 × 노드 양쪽 입자 수 차) + 1D 크기: 준정적 기둥 W 12,000 에서 MPM 최대 편차 W 의 14 % (x ≈ 29) ↔ GIMP 1.7 % · W 30,000 에서 MPM ≥ 63 % (점 10/100 은 그림 밖) ↔ GIMP 2.3 % [판독 · Fig. 4b · 5a] |
| 가중 함수 · 기울기 가중의 정의와 MPM · B-spline 과의 관계 | 식 (19) · (20) · (34) · (38)–(40).  l_p = L/2 ⇒ 2차 B-spline [카드 산술 · §4-8] — 논문은 'B-spline' 낱말을 쓰지 않고 *"quadratic when only one particle is used per cell"* (p.493) 라고만 적는다 |
| 해석해 단위 시험 · 수렴 시험 설계 (단계 2 · U6) | 준정적 기둥 (식 42–43) · 충격 (식 46) · 오차 노름 (식 47) · 셀 0.01–10 · 1–4 p/c · Δt 고정 · 재하 속도 ×5 · ÷4 |
| 셀당 물질점 수 규칙 | **1 개가 GIMP 에서 가장 매끈** (*"suggests that one particle per cell may be the optimal discretization scheme"* p.493) · MPM 은 입자를 늘리면 큰 튐은 조금 작아지나 잦아져 전체가 더 시끄럽다 (p.491) |
| 명시적 · 저속 준정적의 함정 | finite grid instability (Brackbill 1988 인용) · 오차의 바닥이 재하 속도로 정해진다 (Fig. 11: 5 배 빠르면 2.4 배 · 4 배 느리면 2.8 배 작다 [판독 · 카드 산술]) |
| 접촉 · 다물체 · 소성 · 탈압 · 3D · 실험 대조 | **없음** |

### 0-1. ★ 고른 의도 대조 (후보 표 N-16 의 '왜' 칸)

의도 원문: *"f — GIMP 원전 (물질점이 셀을 넘을 때의 잡음 · 가중 함수의 일반 꼴) · bardenhagen2005 가 쓴 contiguous-particle GIMP 의 원전이고 Fig. 1 반력 튐을 이 논문으로 넘김 (§3-3 · §4-1) → CPDI · 우리 B-spline 가중의 비교 기준"* (가리킨 카드 = `gritton2017_…` ref [37] · `bardenhagen2005_…` §3-3 · §4-1 · 정본 L145 · L564)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "f" — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정 | **일부** | **해상도 · 수치 오차 = 채움**: 셀 크기 0.01–10 (*"three orders of magnitude"*) × 셀당 입자 1 · 2 · 4 의 수렴 시험 (Fig. 10 · p.491–493) · 오차 노름 식 (47) = Σ_p ∣σ(x_p) − σ_p∣ 2l_p / (W Δ₀) · 해석해 대조 · 재하 속도 사다리 (Fig. 11).  **접촉 · 다물체 · 강체 결합 = 없음** ('contact' 0 회 [카드 전문 검색]).  '지름당 셀 수' 규칙 = 없음 (입자 · 알갱이가 없는 연속 막대) |
| "GIMP 원전" | **채움** | 제목 · 초록 · §2 (식 1–33) · §5 결론 *"This family of methods has been named the Generalized Interpolation Material Point (GIMP) methods to indicate their relation to the Material Point Method (MPM) … which can be derived as a special case"* (p.494) |
| "물질점이 셀을 넘을 때의 잡음" | **채움** | 기전 (p.488 · `txt_p12_cell_crossing_noise_force_imbalance.png`) · 준정적 (Fig. 4 · 5) · 충격 (Fig. 6 · 7) · 입자 수 (Fig. 9) · 수렴 (Fig. 10 · finite grid instability p.493).  조건: 1D 초탄성 · 무차원 · 평균 변형률 2 % [카드 산술] |
| "가중 함수의 일반 꼴" | **채움** | 식 (19) S̄_vp = (1/V_p)∫_{Ω_p∩Ω} χ_p(x)S_v(x)dx · 식 (20) ∇S̄_vp = (1/V_p)∫_{Ω_p∩Ω} χ_p(x)∇S_v(x)dx (p.481) · 분할의 합 = 1 (식 23) · MPM 특수형 (식 34) · contiguous (식 38–40 · Fig. 2) |
| "bardenhagen2005 가 쓴 contiguous-particle GIMP 의 원전" | **채움 (정의) · 일부 (그 논문이 쓴 판)** | §3.2 *"Contiguous Particles GIMP Method"* (p.485–486) — χ_p = 상자 (식 36–37) · *"It will be referred to as the "contiguous particle GIMP method""* (p.486).  ⚠ 이 논문의 예제에서 'GIMP' 는 **입자 폭을 추적하지 않는** 판 (l_p(t) = l_p^i · p.486 · p.487) 이고, 폭을 추적하는 판은 **'Finite (contiguous particle) GIMP'** 로 따로 부른다 (p.489).  2005 판이 어느 쪽을 3D 에 어떻게 썼는지는 이 논문으로 알 수 없다 [미확인] — 이 논문은 1D 뿐이고 3D 는 *"may need to be done numerically"* 까지만.  뒤 문헌의 이름 ([다른 카드 `sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability` §4-2]): **uGIMP** (영역 고정 · 그 식 19) = 이 논문 예제의 'GIMP' · **cpGIMP** (직사각형 영역을 diag(F) 로 갱신 · 그 식 20) = 1D 에서 이 논문의 'Finite GIMP' 와 같은 갱신 [카드 판독 — 1D 에서 diag(F) = F] |
| "Fig. 1 반력 튐을 이 논문으로 넘김" (2005 판 §3-3 · §4-1) | **일부 (기전만)** | 이 논문이 주는 것: ① MPM 셀 넘김 힘 불균형 ∝ 입자 응력 × 노드 양쪽 입자 수 차 ② contiguous GIMP 에 남는 불균형 ∝ 응력 × (틈 · 겹침 부피 ÷ 처음 입자 부피) · 그 틈 · 겹침이 격자에 고르지 않게 놓일 때만 (p.488) ③ 폭을 추적하지 않으면 경계에서 질량 · 운동량이 격자로 안 넘어가 바닥 응력 (= 반력) 이 작게 나온다 — W 40,000 에서 바닥 입자 −37,737 ↔ 해석 −39,805 (**−5.2 %**) · Finite GIMP −39,787 (−0.01 %) [판독 · Fig. 5b].  **주지 않는 것**: 큰 변형 (2005 판은 공칭 90 %) · 3D · 경계 반력의 시간 이력 · 반력 튐의 크기.  ⇒ 2005 판의 튐을 "틈 · 겹침이 고르지 않게 놓인 탓" 으로 읽는 것은 [카드 추론] |
| "→ CPDI … 의 비교 기준" | **없음 (원문)** | CPDI 는 이 논문 뒤 (2011 · `gritton2017_…` ref. [38] · 같은 날 정본 카드 `sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability`) — 원문에 없다.  그 카드의 2D MMS 비교 (표준 MPM · uGIMP · cpGIMP · CPDI) 가 이 논문 Fig. 10 의 MPM · GIMP · Finite GIMP 짝의 2D 판이다 [카드 판독 · 위 이름 대응].  비교 기준으로 쓸 수 있는 것: 이 논문의 '입자 영역을 추적하면 (Finite GIMP) 경계 손실이 사라진다' (Fig. 5b · 8) 와 '1D 에서만 해석적으로 적분된다' (p.484–485) — CPDI 가 3D 에서 푸는 문제의 자리 [카드 추론] |
| "→ 우리 B-spline 가중의 비교 기준" | **일부 (카드 산술로 채움)** | 원문에 B-spline 0 회 [카드 전문 검색].  식 (40) 에 l_p = L/2 를 넣으면 2차 B-spline 과 같다 (§4-8 · [카드 산술] · 수치 확인) — 원문 근거 문장은 *"Convergence rates are consistent with the smoothness of the weighting functions, which are quadratic when only one particle is used per cell"* (p.493).  기울기 쪽은 다르다: GIMP 의 ∇S̄_vp = dS̄_vp/dx_p (식 39 · p.485) ↔ MLS-MPM 의 대용 기울기 M_p⁻¹N_i(x_i − x_p) (노드 옆 1.5 배) [다른 카드 `hu2018_…` §4-3 · 카드 산술] |

**가리킨 카드 · 같은 문헌을 언급한 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `bardenhagen2005_…` L145 (§3-3) | *"small errors associated with particles crossing computational cell boundaries, resulting in the spikes …"* · *"자세한 것은 Bardenhagen and Kober (2004) 로 넘김"* | 2005 판 자신의 문장 — 이 논문이 셀 넘김 오차의 기전 · 시험을 실제로 담는다 (p.488 · Fig. 4–10) | **같음** (넘긴 곳이 맞다 · 단 큰 변형은 시험 안 함) |
| `bardenhagen2005_…` L278 (§4-1) | GIMP = *"a general mathematical framework … which allows MPM to be derived as a special case.  The GIMP method framework addresses accuracy in handling large material deformations"* (2005 판 문장) | 식 (34) MPM 특수형 · *"It is precisely this property which improves performance in handling finite deformations"* (p.482) | **같음** |
| `bardenhagen2005_…` L563 (§14 GIMP) | *"물질점에 크기 (영역) 를 주어 격자 보간 함수를 일반화한 MPM 계열 기법.  MPM 은 그 특수한 경우"* | χ_p (p.479) · 식 (19)–(20) · (34) | **같음** |
| `bardenhagen2005_…` L564 (§14 contiguous-particle GIMP) | *"물질점 영역이 변형을 따라 서로 이어지도록 갱신하는 변종"* | 원문의 'contiguous particles' = **겹치지 않는 상자 χ_p** (식 36–37 · *"contiguous regions of non–overlapping support"* p.485).  변형을 따라 폭을 갱신하는 것은 **'Finite (contiguous particle) GIMP'** 이고 (p.489), 예제의 'GIMP' 는 폭을 **고정**한다 (l_p(t) = l_p^i · p.486–487) | **2004 원문 이름과 다름 (일부)** — 이름 (상자 χ_p) 과 폭 추적 (Finite) 을 한데 묶었다.  단 뒤 문헌의 이름 (cpGIMP = 크기 추적 · `sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability` §4-2) 과는 맞는다 → 2005 판이 어느 판을 썼는지 [미확인] · 카드 문제로 보고 (정정 대상인지는 2005 원문 확인 뒤) |
| `gritton2017_…` L91 · L234 | L91 = 원문 인용 *"MPM along with the multiple variants of the method are well described in the literature [32–37]"* · *"The MPM algorithm as described in [34, 38]"* · L234 = *"변종의 설명은 이 논문에 없다 — 이름과 ref. [38] 의 제목 … 뿐이다"* — 그 카드에 [37] 의 서지 줄은 없다 (카드 전문 grep · '37' 은 L91 한 줄) | 이 논문 = 가중 함수의 일반 꼴 (식 19–20) 과 contiguous 꼴 (식 40) 을 담는다 | **같음 (내용 수준)** — [37] = 이 논문이라는 연결은 후보 표 (정독 b40) 의 것이고 gritton 원문 목록은 이 카드가 보지 못했다 |
| 후보 표 N-16 서지 (b40 · b41) | *"Comput. Modeling Eng. Sci. 5 477–96"* · *"Comp. Model. Eng. Sci. 5, 477–496"* | 머리글 인쇄 **"cmes, vol.5, no.6, pp.477-495, 2004"** · 마지막 인쇄 쪽 번호 495 (PDF 19 쪽) · PDF 20 쪽은 빈 쪽 | **다름 (쪽 끝)** — 495 ↔ 496 · 호 (no. 6) 는 후보 표에 없음 |

⇒ **의도 대조 결과: 채움 (GIMP 원전 · 셀 넘김 잡음 · 가중 함수의 일반 꼴 · contiguous particle GIMP 의 정의) / 일부 (f 의 해상도 · 오차 쪽만 · 2005 판 반력 튐은 기전만 · B-spline 관계는 카드 산술) / 없음 (접촉 · 다물체 · CPDI · 3D 구현)**.

### 0-2. 이 묶음의 네 질문 (DEM 한계 · 소성 · 2D/3D · 탈압)

| 질문 | 이 논문의 답 (원문 위치) |
|---|---|
| (i) DEM (단단한 구 · 점접촉) 의 한계를 말한 문장 | **말 없음** — DEM · 'discrete element' 0 회 · 'contact' 는 참고문헌 제목 (Bardenhagen 외 2001) 한 번 [카드 전문 검색].  한계를 적은 대상은 **유한요소법**: *"However, body fixed FEM meshes can be difficult and time consuming to generate for complex three–dimensional objects.  Further, mesh distortion associated with large deformations compromises solution accuracy, ultimately requiring re–meshing."* (p.477 · `txt_p1_intro_fem_mesh_distortion_remeshing.png`) — 그리고 MPM 자신의 한계 (셀 넘김 잡음 · finite grid instability) |
| (ii) 입자의 소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용 | **소성 계산은 없다** — 대신 그 어려움의 **수치 쪽 이유 하나**를 적는다: *"In evaluating constitutive response on material points, there is an implicit assumption that neighboring points have similar histories.  Computational artifacts result in nonphysical input to the material point constitutive models … These artifacts will result in erroneous evolution of history variables in inelastic constitutive models.  If there is sufficient dissipation to prevent a complete breakdown, solution divergence may go undetected."* (p.494 · `txt_p18_conclusions_mpm_infinitesimal_only.png`).  우회 = **보간을 한 단계 매끈하게** (C⁰ → C¹ · contiguous particle GIMP) · 비용 = 지지 폭이 넓어져 계산량 증가 (*"The increased support does result in an increase in computational effort"* p.486) — 1D 에서 입자당 노드 2 → 3, 3D 텐서곱이면 8 → 27 [카드 산술 · 같은 꼴 가정] · 3D 는 변형 · 회전하는 입자 영역의 적분이 필요해 *"may need to be done numerically"* (p.484).  **맞춘 값 = 0 개** (재료 · 시험 값을 정해 놓고 계산) |
| (iii) 2D 인가 3D 인가 · 2D → 3D 전이 | **1D 뿐** — *"The investigation in the following section is performed in one–dimension for simplicity.  In one–dimension the weighting functions can be determined analytically."* (p.484–485).  3D 에 대한 말 셋: 형상 함수는 1D 텐트의 곱 (*"S_v(x) = S_v1(x1)S_v2(x2)S_v3(x3)"* · *"An analogous multiplicative decomposition is available for the particle characteristic functions"* p.484) · 3D 의 실제 어려움 (변형 · 회전하는 입자 영역 적분 · p.484) · *"Computational effort and storage requirements are, of course, strongly influenced by the number of particles used, especially in three–dimensions"* (p.491).  2D 결과는 없다 (*"two dimensions"* 는 참고문헌 제목 두 번 — Bardenhagen 외 2000 PRE · Brackbill–Ruppel FLIP) |
| (iv) 압력을 뺄 때의 거동 | **다루지 않는다** — 'unload' 0 회.  준정적 기둥은 중력을 한 방향으로 키울 뿐이고 (40 회 파 통과 시간 동안 선형 증가 · p.487) 충격도 한 번 (파 통과 시간 1 회 · p.489).  재료가 초탄성이라 원리상 되돌아오겠지만 계산은 없다 [미확인] |

---

## 1. 한 줄 요약

**KR:** 물질점 방법 (MPM) 을 가상일 (변분형) 에서 **Petrov–Galerkin** 이산화 — 시험 함수는 격자 형상 함수 S_v, 시행 함수는 **입자 특성 함수 χ_p** (입자가 차지하는 공간 · 부피 분율) — 로 다시 유도하면, 격자 · 입자 사이 전달에 쓰이는 함수가 **가중 함수 S̄_vp = (1/V_p)∫χ_p S_v dx 와 기울기 가중 ∇S̄_vp = (1/V_p)∫χ_p ∇S_v dx** 로 일반화되고 (식 19–20), 나머지 이산 식 (14–18 · 21–22 · 26–27 · 30) 은 MPM 과 같은 꼴이 된다.  χ_p 를 델타로 두면 MPM 이 정확히 나오고 (식 34 · S̄_vp = S_v(x_p)), 겹치지 않는 상자로 두면 1D 에서 해석적으로 적분되는 C¹ 가중 (식 40) — **contiguous particle GIMP** — 가 나온다.  이 틀에서 전체 질량 · 운동량 보존 (식 24–25 · 28) 은 어떤 가중에서나 서고, χ_p 가 현재 배치에서 분할의 합 = 1 이면 균일 응력에서 내부 노드의 내부력이 정확히 0 이 된다 (식 31–33) — MPM 의 델타는 그 조건을 못 지켜, 입자가 셀을 넘어 노드 양쪽 입자 수가 달라지면 **노드에 가짜 힘**이 생긴다 (셀 넘김 잡음).  1D 초탄성 막대 (E 10⁶ · 길이 50 · 셀 50 개 · 셀당 입자 2 · Δt 10⁻⁴) 의 준정적 중력 압축에서 MPM 해는 첫 셀 넘김 직후 흔들리고 (W 12,000) 더 무거워지면 가짜 힘이 물리 힘을 압도해 무너지며 (W 30,000 · 40,000), GIMP 해는 매끈하지만 입자 폭을 고정한 탓에 경계에서 질량이 격자로 덜 넘어가 바닥 응력을 작게 낸다 — 폭을 추적하는 Finite GIMP 는 해석해와 겹친다.  막대 충격에서도 MPM 응력 교란은 *"locked in"* 되고 GIMP 는 매끈하다.  셀당 입자를 늘려도 MPM 은 더 시끄러워지고 (튐이 잦아짐), GIMP 는 셀당 하나가 가장 매끈하다.  셀 크기 세 자리 수렴 시험에서 MPM 오차는 어느 크기 아래로 내려가면 다시 커지고 (셀 넘김이 키운 finite grid instability), GIMP 는 경계 효과의 값에서 포화하며, Finite GIMP 는 가장 빨리 (≈ 2 차) 수렴하다 동역학 (재하 속도) 이 정하는 바닥에서 포화한다.  결론: **MPM 은 셀 넘김이 없는 무한소 변형 문제에만 쓰라**, 유한 변형에는 더 매끈한 보간이 필요하다.

**EN:** Bardenhagen and Kober re-derive the material point method from the principle of virtual work with a Petrov–Galerkin discretization — grid shape functions S_v as test functions and particle characteristic functions χ_p as trial functions — so that grid–particle transfers use generalized weighting and gradient-weighting functions S̄_vp = (1/V_p)∫χ_p S_v dx and ∇S̄_vp = (1/V_p)∫χ_p ∇S_v dx, while all other discrete equations keep the MPM form.  A Dirac-delta χ_p recovers MPM exactly; non-overlapping box χ_p give the C¹ contiguous particle GIMP weighting, analytic in 1D.  Total mass and momentum are conserved for any weighting, and when the χ_p form a partition of unity in the current configuration a uniform stress produces exactly zero internal force at interior nodes — MPM violates this, so particles crossing cells create spurious nodal forces proportional to stress times the particle-count imbalance.  In 1D tests on a hyperelastic bar (quasi-static gravity column with analytic solution, impact with a shock solution, 1–4 particles per cell, cell sizes 0.01–10), MPM stresses become noisy after the first crossing and are destroyed at larger loads; contiguous GIMP stays smooth but loses mass at the boundary when particle widths are not tracked, which tracked-width "Finite GIMP" removes.  MPM error grows under refinement (finite grid instability seeded by cell-crossing noise), GIMP saturates at a boundary-effect level and Finite GIMP converges fastest (≈ second order) until loading-rate dynamics set the floor.  The authors recommend MPM only for infinitesimal deformation (no cell crossings).  No experiments, contact, plasticity, unloading or 3D implementation.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 제목 | **The Generalized Interpolation Material Point Method** |
| 저자 | **S. G. Bardenhagen** (¹ ²) · **E. M. Kober** (³) |
| 소속 (각주 인쇄 그대로) | ¹ Dept. of Mechanical Engineering, University of Utah, Salt Lake City, UT 84112, USA, Graduate Engineering Research Center, University of Florida, 1350 Poquito Rd., Shalimar, FL 32579, USA. · ² Correspondence address: Group T–14, MS B214, Theoretical Division, Los Alamos National Laboratory, Los Alamos, NM 87545, USA. · ³ Group T–14, MS B214, Theoretical Division, Los Alamos National Laboratory, Los Alamos, NM 87545, USA. |
| 저널 | **CMES (Computer Modeling in Engineering & Sciences) vol. 5, no. 6, pp. 477–495, 2004** — 머리글 인쇄 *"Copyright © 2004 Tech Science Press"* · *"cmes, vol.5, no.6, pp.477-495, 2004"* (짝수 쪽 머리글) · 학술지 전체 이름은 이 논문 참고문헌의 다른 CMES 논문 표기 (*"CMES: Computer Modeling in Engineering & Sciences"*) 에서 |
| DOI | **[미확인]** — PDF 에 인쇄 없음 (첫 쪽 · 머리글 · 끝 쪽 전수) |
| 접수 · 게재 | **[미확인]** (인쇄 없음) · PDF 만든 날 2004-06-18 [PDF 메타데이터 · 제목 칸 *main.dvi* · dvips 5.90a → Acrobat Distiller 5.0.5] |
| 키워드 (인쇄) | MPM, PIC, meshless methods, Petrov–Galerkin discretization |
| 분량 | 19 쪽 인쇄 (p.477–495 · **PDF 쪽 = 학술지 쪽 − 476**) + 빈 PDF 쪽 1 · Fig. 1–11 · 번호 식 (1)–(47) · **표 없음** · 참고문헌 28 건 · 보충 자료 없음 |
| 절 구성 | 1 Introduction (p.477–479) · 2 Derivation of the Discrete Equations (p.479–484: 2.1 Initial Discretization · 2.2 Discrete Solution Procedure · 2.3 Observations) · 3 Example GIMP Methods (p.484–487: 3.1 Material Point Method · 3.2 Contiguous Particles GIMP Method · 3.3 Fuzzy Particle GIMP Methods) · 4 Example Calculations (p.487–494: 4.1 Quasi–static Compaction · 4.2 Dynamic Compaction · 4.3 Sensitivity to Particle Discretization · 4.4 Convergence) · 5 Conclusions (p.494) · Acknowledgement · References (p.494–495) |
| 연구 유형 | 수치 방법 (MPM 의 변분형 일반화 + 1D 시험).  실험 없음 · 남의 실험 대조 없음 |
| 자금 | U.S. Department of Energy — Center for the Simulation of Accidental Fires and Explosions, grant **W-7405-ENG-48** (짝 카드 2001 · 2005 판과 같은 과제 번호 [다른 카드]) · Air Force Office of Scientific Research — Research Institute for Autonomous Precision Guided Systems, grant **AFOSR–F49620–00–1–0288** |
| 감사 | Dr. V. Mousseau, T–Division, LANL |
| 코드 | 이름 · 언어 미인쇄 [미확인] |
| PDF 상태 | LaTeX (dvips) 조판 PDF · 글자 층 온전하나 적분 기호 · 윗줄 (S̄) 이 글자 층에서 빠진다 → 식은 렌더로 확인 (식 크롭 47 장) · 그림 11 장 전부 **벡터** (Fig. 1–3 = xfig 꼴 Courier 글자 · Fig. 4–11 = gnuplot 꼴 Helvetica 글자) · 쪽마다 있는 1 × 1 화소 이미지는 머리글 선 · 분수선 같은 줄 (그림 아님) |

**자기 위치 (저자 원문)**
> *"Here the full generality of the variational formulation is exploited.  The variational form of the governing equations provides a consistent framework for generalizing the MPM discretization technique … The use of smoother representations of discrete material point data allows an entire family of methods to be developed.  A significant result of this generalization is smoother representation of particle data on the computational grid.  This removes a numerical artifact inherent in the MPM formulation, which can develop when material points fail to register in a self–similar fashion on the computational grid.  This situation can be expected to arise regularly in finite deformation analyses, and is demonstrated to very seriously degrade the accuracy of solutions obtained using MPM."* (p.478–479 · `txt_p2_p3_smoother_representation_removes_artifact.png`)

---

## 3. 핵심 수치

> **표지** · `인쇄` = 본문 · 캡션 · 그림 글자 · `[판독]` = 그림 경로 좌표 (`digitized.csv`) · `[카드 산술]` = 산술로만 · `[미확인]` = 논문에 없음.  판독값은 추세 · 자릿수 확인용이다 — 논문이 인쇄한 값처럼 쓰지 않는다.  모든 값은 **무차원 (일관 단위)** 이다.

### 3-1. 시험 설정 (§4 · p.487 · `txt_p11_example_setup_E_c_L_dt_40_transits.png`)

| 항목 | 값 | 표지 · 위치 |
|---|---|---|
| 재료 | 1D 초탄성 **σ = E(F − 1)** (식 41) · F = 1D 변형구배 | 인쇄 p.487 |
| E · ρ₀ · 파속 c | **10⁶ · 1 · 1000** (*"Any consistent set of units suffices"*) | 인쇄 p.487 |
| 막대 길이 Δ₀ | **50** | 인쇄 p.487 |
| 격자 (§4.1–4.2) | 셀 **50** 개 · **L = 1** · **셀당 물질점 2** → 물질점 100 · 처음 반폭 l_p^i = L/4 = 0.25 (2l_p^i = L ÷ 셀당 입자 수 · p.485) | 인쇄 p.487 · l_p 는 [카드 산술] |
| 파 통과 시간 | **Δ₀/c = 0.05** | 인쇄 p.487 |
| 시간 간격 | CFL *"Δt ≤ L/c = 10⁻³"* (선형) → *"reduced by an additional factor of ten, i.e. Δt = 10⁻⁴"* (Courant 수 cΔt/L = 0.1) | 인쇄 p.487 · Courant 수는 [카드 산술] |
| 시간 적분 | 명시적 (*"The explicit time stepping algorithm used in all numerical solutions is governed by the CFL stability condition"*) · 갱신 순서 (USF / USL) · 속도 갱신 꼴 (FLIP / PIC 혼합 비율) 미인쇄 — 식 (26)–(27) 은 격자 속도 · 가속도 보간 (FLIP 꼴 · *"serves to reduce numerical diffusion"*) | 인쇄 p.482 · p.487 · [미확인] |
| 두 해의 입자 폭 | 'MPM' · 'GIMP' 둘 다 **l_p(t) = l_p^i** (*"For both of these solutions particle volumes are not tracked"*) · 'Finite GIMP' 만 폭 추적 | 인쇄 p.487 · p.489 |
| 응력 보고 | 물질점의 위치 · 응력 (*"Results are reported at specific stages in the deformation by plotting stresses at material points"*) · 세로 점선 = 셀 경계 | 인쇄 p.487 |
| 해상도 말 | *"While the resolution of the computation is commensurate with the grid cell size, constitutive response is computed on material points only.  In order that inelastic constitutive response be accurately simulated, material point stresses must vary smoothly."* | 인쇄 p.487 |

### 3-2. 준정적 기둥 — 중력 압축 (§4.1 · 식 42–44 · Fig. 4 · 5 · `txt_p12_final_body_force_W40000_first_crossings.png`)

| 항목 | 값 | 표지 · 위치 |
|---|---|---|
| 하중 | 압축 체적력 b (중력) 를 시간에 **선형으로** 키움 · 총 시간 = **파 통과 시간 40 배** (= 2.0 → 20,000 걸음) | 인쇄 p.487 · 걸음 수는 [카드 산술] |
| 해석해 | σ(x) = E{√[(2ρ₀b/E)(Δ − x) + 1] − 1} (0 ≤ x ≤ Δ · 현재 배치 · 식 42) · Δ = Δ₀ + ρ₀bΔ₀²/(2E) (식 43) · 기둥 무게 W = ρ₀∣b∣Δ₀ (식 44) | 인쇄 p.487–488 |
| 끝 하중 | **b_f = −800** (끝 변위 Δ − Δ₀ = −1 = 셀 하나) · **W_f = 40,000** | 인쇄 p.488 |
| 단계별 Δ · 바닥 응력 | W 10,000 → Δ 49.75 · 12,000 → 49.70 · 30,000 → 49.25 · 40,000 → 49.00 · 바닥 해석 응력 = −W (정확히) · 바닥 F = 1 − W/E = 0.99 … **0.96** · 평균 변형률 **2 %** (끝) | [카드 산술 — 식 42–44] |
| 셀 넘김 첫 사건 | W 12,000 에서 x_v ≥ 30 인 셀들의 왼쪽 입자가 왼쪽 셀 경계를 넘어 **29 ≤ x ≤ 30 셀에 물질점 3 개** (*"These cell crossings have substantially perturbed the MPM solution, both for x ≥ 29 … and in the remainder of the column, due to propagation of the cell crossing disturbances"*) | 인쇄 p.488 |
| Fig. 4a (W 10,000 · 넘김 전) | 최대 편차 MPM **96** (W 의 0.96 %) · GIMP **88** (0.88 % · 바닥 입자 x ≈ 0.24: −9,863 ↔ 해석 −9,952) · *"essentially overlie one another"* | [판독] · 인쇄 p.488 |
| Fig. 4b (W 12,000 · 넘김 직후) | MPM 최대 **1,682 (W 의 14 %) · x ≈ 29.0** · RMS 3.4 % · 표지 99 개 (1 개는 그림 밖) ↔ GIMP 최대 **207 (1.7 %)** · 바닥 입자 −11,735 ↔ 해석 −11,942 | [판독 · 카드 산술] |
| Fig. 5a (W 30,000) | MPM 최대 ≥ **19,015 (≥ 63 %)** · x ≈ 9.45 (−5,157 ↔ 해석 −24,172) · RMS ≥ 18 % · **표지 10/100 은 그림 밖** (−40,000 아래 또는 0 위) ↔ GIMP 최대 **689 (2.3 %)** 바닥 · 저자: *"The spurious forces developed due to the low degree of continuity in interpolation are overwhelming the "physical" forces in the system and destroying the solution"* | [판독] · 인쇄 p.488 |
| Fig. 5b (W 40,000) | MPM 표지 **3 개만** 그림 안 (*"only traces of the MPM solution remain"*) · GIMP 바닥 입자 **−37,737 ↔ 해석 −39,805 (−5.2 %)** · Finite GIMP **−39,787 (−0.01 %)** · Finite GIMP 최대 편차 378 (0.95 %) · RMS 0.41 % | [판독] · 인쇄 p.489 |
| GIMP 바닥 손실의 이유 (저자) | *"Because the GIMP solution uses initial particle widths throughout the computation, as a particle approaches the boundary its characteristic function begins to overlap the edge of the computational grid.  The overlapping portion information is not interpolated to the grid."* | 인쇄 p.489 |
| 가짜 힘의 크기 어림 | MPM 1D · 셀당 2 · 노드 한쪽에 입자 하나가 더 있으면 식 (16) · (35) 로 ∣f_v∣ = ∣σ∣V_p/L = ∣σ∣/2 · W 12,000 의 x ≈ 29.5 (σ ≈ −4,860) 에서 ≈ 2,430 ↔ 그 노드의 중력 ρ₀L∣b∣ = 240 → **≈ 10 배** | [카드 산술 — 균일 응력 · 처음 입자 부피 가정] |

### 3-3. 막대 충격 (§4.2 · 식 45–46 · Fig. 6–8 · `txt_p13_p14_dynamic_compaction_setup_shock_locked_in.png`)

| 항목 | 값 | 표지 · 위치 |
|---|---|---|
| 하중 | 막대에 왼쪽으로 처음 속도 **v₀ = c/50** (= 20) → 강체 벽 (계산 경계) 에 충돌 · **파 통과 시간 1 회** (= 0.05 → 500 걸음) · 끝 변위 −1 (준정적과 같다) | 인쇄 p.489 · 숫자는 [카드 산술] |
| 인공 점성 | Richtmyer–von Neumann + 선형 항 · q = c₁ρc∣ε̇L∣ + c₂ρ(ε̇L)² (ε̇ < 0) · 0 (그 밖) (식 45) · **c₁ = 0.2 · c₂ = 2.0** · 입자에서 계산해 σ_p → σ_p − q_p | 인쇄 p.489 |
| 해석해 | 충격 뒤 F = (ct − v₀t)/(ct) = 1 − v₀/c (식 46) = 0.98 → **σ = −20,000** · 충격 앞은 0 | 인쇄 p.490 · F 값은 [카드 산술] |
| 첫 셀 넘김 | 충격 뒤에서 **꼭짓점 x_v = 13** · **12 ≤ x ≤ 13 셀에 물질점 3 개** (식 46 에서 구함 · Fig. 6b (t/파 통과 시간 = 0.30) = *"the situation shortly after the first cell crossing behind the shock"* · 충격 앞의 넘김은 응력이 0 이라 영향 없음) · *"the cell crossing substantially perturbs the MPM solution, but not the GIMP solution"* | 인쇄 p.490 |
| 보고 시점 | 준정적과 **같은 끝 변위** (*"at the same end displacements as in the quasi–static example"*) — t/파 통과 시간 0.25 · 0.30 · 0.75 · 1 ↔ W 10,000 · 12,000 · 30,000 · 40,000 (끝 변위 −0.25 · −0.30 · −0.75 · −1) | 인쇄 p.489 · 짝 짓기는 [카드 산술 — 끝 변위 = −v₀t ↔ −2.5 × 10⁻⁵ W] |
| Fig. 6a (t = 0.25 · 넘김 전) | 충격 뒤 (x < 6.5) 최대 편차 MPM 1,923 (9.6 %) · GIMP 2,445 (12 %) — 벽 근처 (x ≈ 1.2) 의 울림 · *"stresses are uniform within cells in the MPM solution, while in the GIMP solution particle stress variation within cells is more consistent with the smeared shock front"* | [판독] · 인쇄 p.490 |
| Fig. 7a (t = 0.75) | MPM 최대 **9,083 (45 %) · x ≈ 13.0** (넘김 자리) · RMS 1,551 ↔ GIMP 최대 1,924 (x ≈ 30.6 · 충격 뒤 울림) · RMS 631 · *"The stress disturbance in the MPM solution is locked in as required to maintain equilibrium on the grid for non–uniform particle registration"* | [판독] · 인쇄 p.490 |
| Fig. 7b (t = 1) | MPM 최대 **9,159 (46 %) · x ≈ 13.0** (그 자리 그대로) + **x ≈ 37–39 에 둘째 무리** (−11,702 … −17,792) — 저자: *"In Fig. 7(b) the shock has reached the end of the bar, resulting in another cell with three material points as evident in the MPM solution"* · 그 셀 = [36, 37] 로 읽힌다 [카드 산술 — 충격 뒤 x = 0.98 X · 처음 입자 X = 0.25 + 0.5k 가정 · 같은 셈이 첫 넘김 x_v = 13 을 재현] · GIMP 최대 1,507 · RMS 446 (x < 43) | [판독] |
| Fig. 8 (t = 1 · GIMP ↔ Finite GIMP) | x < 43 평균 응력 GIMP **−19,787 (해석보다 1.1 % 작음)** ↔ Finite GIMP **−20,013 (+0.06 %)** · RMS 473 · 426 | [판독 · 카드 산술] |
| 저자 해석 | *"information is lost to the grid when finite deformations are not accounted for.  It should be noted that MPM does not suffer from information loss to the grid unless a particle leaves the computational domain.  Tracking current particle volumes corrects the MPM solutions as well, but does not alleviate cell crossing noise."* | 인쇄 p.491 · `txt_p15_information_loss_and_particles_per_cell.png` |

### 3-4. 셀당 입자 수 (§4.3 · Fig. 9)

| 항목 | 값 | 표지 · 위치 |
|---|---|---|
| 설계 | 충격 문제를 셀당 **1 · 2 · 4** 로 (2 는 §4.2 와 같은 계산) · t = 1 에서 비교 | 인쇄 p.491 |
| MPM (x < 43) | 최대 편차 1 p/c **9,409** · 2 p/c **9,159** · 4 p/c **7,221** · 편차 > 2,000 인 꼭짓점 **2 · 7 · 11 개** (4 p/c 는 판독된 꼭짓점 134/200 기준) | [판독] |
| GIMP (x < 43) | 최대 편차 1,770 · 1,506 · 1,610 · 편차 > 2,000 **0 · 0 · 0** · RMS 695 · 447 · 471 (4 p/c 는 177/200) | [판독] |
| 저자 판정 (MPM) | *"Although the magnitude of the large variations in particle stresses is slightly reduced by using more particles, the increase in frequency of these variations results in a noisier solution overall."* | 인쇄 p.491 |
| 저자 판정 (GIMP) | *"as l_p → 0, then S̄_vp → S_v(x_p), i.e. the GIMP weighting functions tend toward the MPM ones as more particles are used.  Shorter wavelength noise consistent with this limiting behavior can be seen in the GIMP solutions for 4 particles/cell"* · *"as it suggests the use of fewer particles/cell is advantageous, it is of significant practical importance"* | 인쇄 p.491 |
| 가중 함수의 꼭대기 값 | S̄_vp(x_p = x_v) = 1 − l_p/(2L) = **0.75 · 0.875 · 0.9375** (1 · 2 · 4 p/c) — *"except for special cases, S̄_vp∣x_p=x_v < 1"* (p.482) 의 숫자판 | [카드 산술 — 식 40] |

### 3-5. 격자 수렴 (§4.4 · 식 47 · Fig. 10 · 11)

| 항목 | 값 | 표지 · 위치 |
|---|---|---|
| 문제 | Fig. 4a 와 같은 준정적 기둥 · **W = 10,000** (단위 셀에서는 셀 넘김 전) · 인공 점성 없음 | 인쇄 p.491–492 |
| 오차 노름 | Error = Σ_p ∣σ(x_p) − σ_p∣ 2l_p / (W Δ₀) (식 47 · 무차원 · 입자 위치에서의 해석해와) | 인쇄 p.491 |
| 셀 크기 · 셀당 입자 | 셀 **0.01–10** (*"spanning three orders of magnitude"* · 판독된 값 10 · 5 · 2.5 · 1 · 0.5 · 0.25 · 0.1 · 0.05 · 0.025 · 0.01) × **1 · 2 · 4 p/c** × MPM · GIMP · Finite GIMP | 인쇄 p.492 · 셀 값은 [판독] |
| 시간 간격 | *"the same time step size was used regardless of cell size"* — **값은 미인쇄** [미확인].  앞 절의 Δt = 10⁻⁴ 는 셀 1 의 CFL (L/c = 10⁻³) 에 맞춘 값이고 셀 0.01 의 L/c 는 10⁻⁵ 이다 → 이 절의 Δt 는 그보다 작았어야 한다 [카드 산술 · 카드 추론] | 인쇄 p.492 |
| 셀 넘김 여부 | *"For cell sizes 2.5 and larger, there are no cell crossing events for any of the particle densities considered"* · 셀 1 에서는 4 p/c MPM 만 넘김 | 인쇄 p.492 · p.493 |

**Fig. 10 판독 (오차 · 식 47 · W 10,000)** [판독 · 로그 축 · 표지 중심]

| 셀 크기 | 10 | 5 | 2.5 | 1 | 0.5 | 0.25 | 0.1 | 0.05 | 0.025 | 0.01 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 p/c MPM (■) | 0.088 | 0.032 | 0.0053 | 0.0027 | 0.0027 | 0.035 | 0.079 | 0.31 | 0.91 | 점 없음 |
| 2 p/c MPM (●) | 0.047 | 0.024 | 0.012 | 0.0047 | 0.030 | 0.030 | 0.053 | 0.11 | 3.6 | 점 없음 |
| 4 p/c MPM (▲) | 0.047 | 0.024 | 0.012 | 0.024 | 0.023 | 0.038 | 0.053 | 0.073 | 0.13 | 94 |
| 1 p/c GIMP (□) | 0.087 | 0.032 | 0.0059 | 0.0017 | 0.0016 | 0.0016 | 0.0017 | 0.0017 | 0.0017 | 0.0018 |
| 2 p/c GIMP (○) | 0.046 | 0.022 | 0.010 | 0.0033 | 0.0016 | 0.0016 | 0.0017 | 0.0017 | 0.0017 | 0.0017 |
| 4 p/c GIMP (△) | 0.046 | 0.022 | 0.010 | 0.0036 | 0.0022 | 0.0016 | 0.0016 | 0.0017 | 0.0017 | 0.0017 |
| 1 p/c Finite GIMP (×) | 0.086 | 0.032 | 0.0045 | 2.9e−4 | 1.1e−4 | 2.4e−5 | 5.0e−6 | 1.9e−6 | 1.2e−6 | 1.3e−6 |
| 2 p/c Finite GIMP (+) | 0.046 | 0.022 | 0.010 | 0.0031 | 7.8e−4 | 2.4e−4 | 4.9e−5 | 2.1e−5 | 7.7e−6 | 2.6e−6 |
| 4 p/c Finite GIMP (✳) | 0.046 | 0.022 | 0.010 | 0.0031 | 0.0014 | 3.4e−4 | 8.0e−5 | 3.0e−5 | 1.1e−5 | 3.2e−6 |

- **MPM** — 오차의 최소가 셀 크기 · 입자 수마다 다르고 (1 p/c 0.0027 @ 셀 0.5–1 · 2 p/c 0.0047 @ 1 · 4 p/c 0.012 @ 2.5) 그 아래로 조이면 **커진다** (셀 0.025 에서 0.13–3.6 · 0.01 에서 4 p/c 94 · 1 · 2 p/c 는 셀 0.01 의 점이 그림에 없다 — 그림 위로 나갔는지 계산 안 했는지는 본문에 없음 [미확인]) [판독].  저자: *"In all cases examined the error begins to increase with decreasing cell size after some minimum cell size is reached.  This behavior is the result of the excitation, by cell crossing noise, and subsequent unstable growth, of solution instabilities"* (p.493).
- 셀 1 에서 4 p/c MPM (0.024) 이 1 · 2 p/c (0.0027 · 0.0047) 의 5–9 배 [판독 · 카드 산술] = *"It is the only MPM calculation which has had cell crossings at this column weight and grid resolution"* (p.493).
- **GIMP** — 셀 ≤ 0.5 에서 입자 수와 무관하게 **0.0016–0.0018 에서 포화** [판독] = *"The numerical results continue to converge, but to the solution for a column with slightly reduced mass, due to boundary effects"* (p.493).
- **Finite GIMP** — 1 p/c 가 가장 낮다: 셀 1 → 0.1 에서 2.9e−4 → 5.0e−6 (**기울기 ≈ 1.8 차** = log₁₀(2.9e−4/5.0e−6)) · 셀 2.5 → 0.25 에서 ≈ 2.3 차 · 셀 ≤ 0.05 에서 ≈ 1.2–1.9 × 10⁻⁶ 에 포화 [판독 · 카드 산술] = *"Convergence rates are consistent with the smoothness of the weighting functions, which are quadratic when only one particle is used per cell"* (p.493).
- 셀 ≥ 2.5 에서는 2 · 4 p/c 의 세 방법이 거의 같은 값 (MPM 이 10–20 % 높다: 0.010–0.012 · 0.022–0.024 · 0.046–0.047) 이고 1 p/c 는 셀 5 · 10 에서 그 1.5–1.9 배 [판독 · 카드 산술] — 저자: *"Except for two points … the errors for cell sizes of one or larger are all closely clustered, regardless of the algorithm or particle density"* (p.492).  그 "두 점" 은 셀 1 의 4 p/c MPM (위로) 과 1 p/c Finite GIMP (아래로) 로 읽힌다 [카드 판독].

**Fig. 11 판독 (1 p/c Finite GIMP · 재하 속도 · W 10,000)** [판독]

| 셀 크기 | 10 | 5 | 2.5 | 1 | 0.5 | 0.25 | 0.1 | 0.05 | 0.025 | 0.01 |
|---|---|---|---|---|---|---|---|---|---|---|
| faster (중력 5 배 빠르게 · +) | 0.088 | 0.032 | 0.0065 | 7.7e−4 | 1.7e−4 | 4.6e−5 | 1.0e−5 | 3.2e−6 | 2.3e−6 | 3.1e−6 |
| benchmark (×) | 0.088 | 0.032 | 0.0047 | 3.0e−4 | 1.1e−4 | 2.5e−5 | 5.1e−6 | 1.9e−6 | 1.2e−6 | 1.3e−6 |
| slower (4 배 느리게 · ✳) | 0.087 | 0.032 | 0.0047 | 3.0e−4 | 1.0e−4 | 1.7e−5 | 4.8e−6 | 1.6e−6 | 7.0e−7 | 4.7e−7 |

- 셀 0.01 의 바닥 비: faster ÷ benchmark = **2.4** · benchmark ÷ slower = **2.8** [판독 · 카드 산술] — 셀 ≥ 0.1 에서는 세 속도가 거의 겹친다 (이산화 오차가 지배).
- 저자: *"This suggests the primary contribution to the error at the finest grid sizes is the difference between the quasi–static numerical solution and the exact (static) solution, i.e. the error saturation is caused by resolving the dynamics."* (p.494).
- benchmark = *"than for the results in Figs. 4 and 10"* 와 같은 재하 속도 (캡션) — Fig. 10 의 1 p/c Finite GIMP 점과 같은 계산으로 읽힌다: 셀마다 판독 차 1.5–2.7 % (Fig. 11 쪽이 고르게 조금 높다 = 두 그림 축 사상의 차로 읽힌다 · 셀 0.01 · 1 에서 1.32e−6 ↔ 1.30e−6 · 2.98e−4 ↔ 2.91e−4) [판독 · 카드 판독].
- Fig. 10 의 셀 1 · 2 p/c 두 점 (● MPM · ○ GIMP) 은 Fig. 4(a) 의 자료 그대로다 (*"the data from Fig. 4(a) have been used in the error calculations"* p.492) — 이 시점 (W 10,000) 은 셀 1 에서 셀 넘김 전이라 고른 것.

### 3-6. 정식화가 보장하는 것 · 안 하는 것 (식 번호)

| 성질 | 조건 · 식 | 표지 |
|---|---|---|
| 처음 이산화에서 전체 질량 · 운동량 정확 보존 | χ_p^i 가 처음 배치에서 분할의 합 = 1 (식 2) → 식 (7)–(8) · 단 경계 입자는 부피 · 질량 · 운동량이 줄어든다 (Ω^i ∩ Ω_p^i < Ω_p^i) · 상자를 물체 위에 그냥 놓는 근사면 *"Eqn.s 7 and 8 only hold in the limit of infinite spatial resolution"* | 인쇄 p.479–480 |
| 입자 → 격자 전달의 전체 질량 · 운동량 보존 | **어떤 가중에서도** (식 23 → 24–25) | 인쇄 p.481–482 |
| 격자 ↔ 입자 운동량 변화량 일치 | 식 (27) → (28) | 인쇄 p.482 |
| 집중 질량 | *"Finally, it is noted that the Petrov–Galerkin method gives "lumped mass" governing equations directly (Eqn. 14)."* — Sulsky 외의 유도는 전체 질량 행렬을 만든 뒤 대각화하는데 그 단계는 *"which typically lacks justification beyond computational tractability"* | 인쇄 p.484 · `txt_p8_mpm_special_case_not_partition_of_unity_lumped_mass.png` |
| 균일 응력에서 내부 노드 내부력 = 0 | χ_p 가 **현재** 배치에서 분할의 합 = 1 (식 32) ∧ 입자 영역이 물체 안 (Ω_p ∩ Ω = Ω_p) → 식 (31)–(33) · *"in the absence of body forces, static equilibrium is maintained only if Eqn. 33 holds"* | 인쇄 p.483 |
| MPM 은 위를 못 지킨다 | 델타 χ_p (식 34) 는 분할의 합이 아니다 (이탤릭 강조 원문) → *"Hence a uniform stress state on the particles can result in non–zero internal forces on the computational grid"* | 인쇄 p.484 |
| 에너지 · 각운동량 보존 | **말 없음** ('energy' 는 자금 줄 한 번) | [카드 전문 검색] |
| 격자 경계의 특별 처리 | contiguous 상자는 격자 안에 완전히 들어 있어 *"require no special treatment"* · 반대로 지지 폭을 마음대로 넓힌 가중은 경계에서 유령 노드 · 다른 보간 규칙이 필요 (*"Particles near the grid boundary may be required to interpolate information to ghost vertices"*) | 인쇄 p.483 |

### 3-7. 계산 비용

| 항목 | 값 | 표지 |
|---|---|---|
| 지지 폭 | MPM = 입자가 든 셀의 두 노드 · contiguous GIMP = *"support in adjacent cells and in next nearest neighbor cells"* (Fig. 2) — 1D 입자당 노드 2 → 3 · 3D 텐서곱이면 8 → 27 | 인쇄 p.485–486 · 노드 수는 [카드 산술] |
| 계산 시간 · 기계 | **[미확인]** (1D 라 비용 표가 없다) | — |
| 입자 수와 저장 | *"Computational effort and storage requirements are, of course, strongly influenced by the number of particles used, especially in three–dimensions"* | 인쇄 p.491 |

### 3-8. ★ 이 논문에 **없는** 값 (정직 목록)

| 찾은 것 | 상태 |
|---|---|
| 2D · 3D 계산 · 3D 가중 적분 방법 | **없음** (1D 뿐 · 3D 는 *"may need to be done numerically"*) |
| 접촉 · 다물체 · 마찰 · 분리 · 강체 결합 | **없음** |
| 소성 · 점탄성 · 손상 계산 | **없음** (초탄성 막대 · 비탄성은 주장뿐) |
| 하중 제거 · 되돌아옴 | **없음** |
| 에너지 수지 · 에너지 보존 점검 | **없음** |
| §4.4 의 시간 간격 값 · 입자 폭 추적의 식 (Finite GIMP 의 l_p 갱신 규칙) | **[미확인]** — Finite GIMP 는 *"particle widths are tracked and used in the interpolation functions"* 까지만 (p.489) |
| 동적 문제의 오차 노름 · 수렴 | **없음** (오차 노름은 준정적만) |
| fuzzy particle 계산 | **없음** (*"While not examined in detail"* · *"Further analysis/experimentation is needed"*) |
| 코드 이름 · 계산 시간 | **[미확인]** |
| DOI · 접수 · 게재일 | **[미확인]** |
| 실험 · 분말 · 입자 층 · 기공 | **없음** |

---

## 4. 방법 ★

### 4-1. 변분형 → Petrov–Galerkin 이산화 (§2 · 식 1–30)

1. **변분형** (식 1 · `eq_01_variational_form_momentum.png`): ∫_Ω ρ a·δv dx + ∫_Ω σ:∇δv dx = ∫_Ω ρ b·δv dx + ∫_{∂Ω_τ} τ·δv dS — 질량 보존은 *"leaving discrete particle masses unchanged throughout a computation"* 로 자동 (p.479).
2. **입자 특성 함수 χ_p(x)** (p.479 · `txt_p3_particle_characteristic_functions_definition.png`): *"In practice the particle characteristic functions are non zero over a small volume.  They define the space occupied, perhaps only partially, by a given particle, and can be thought of as the spatially varying volume fraction of that particle.  They are functions of current particle position and, most generally, deformation state."*
3. **처음 이산화** (§2.1): χ_p^i 는 처음 배치에서 분할의 합 = 1 (식 2) · 처음 부피 V_p^i = ∫χ_p^i dx (식 3) · 질량 · 운동량 · 응력은 연속체 양을 χ_p^i 로 적분 (식 4–6) → 전체 질량 · 운동량 정확 (식 7–8).  처음부터 겹치는 *"fuzzy"* 입자도 허용 (§3.3).
4. **입자 자료의 연속 표현** f(x) = Σ_p f_p χ_p(x) (식 9) — χ_p 가 매끈함을 정한다.  식 (1) 에 넣으면 부피 적분이 입자별 적분의 합이 된다 (식 10) · 현재 부피 V_p = ∫_{Ω_p∩Ω} χ_p dx (식 11).
5. **격자 시험 함수** g(x) = Σ_v g_v S_v(x) (식 12) · S_v 는 노드 v 에서 1 · 다른 노드에서 0 · 분할의 합 = 1 (식 13).  *"use of both grid and particle basis functions to represent test functions and trial functions, respectively, is a Petrov–Galerkin method … more akin to some of the meshless methods … than the FEM"* (p.481).
6. **이산 운동량 식** ṗ_v = f_v^int + f_v^b + f_v^τ (식 14) · ṗ_v = Σ_p S̄_vp ṗ_p (식 15) · **f_v^int = −Σ_p σ_p·∇S̄_vp V_p** (식 16) · f_v^b = Σ_p m_p b S̄_vp (식 17) · f_v^τ = ∫ τ S_v dS (식 18).
7. **★ 가중 함수 · 기울기 가중** (식 19 · 20 · `eq_19_weighting_function_Svp.png` · `eq_20_gradient_weighting_function.png`): S̄_vp = (1/V_p)∫_{Ω_p∩Ω} χ_p(x)S_v(x)dx · ∇S̄_vp = (1/V_p)∫_{Ω_p∩Ω} χ_p(x)∇S_v(x)dx — *"implicitly functions of grid vertex position x_v and particle position x_p … also functions of the integration domain, i.e. the current particle volume"* (p.481).
8. **입자 → 격자**: m_v = Σ_p m_p S̄_vp (식 21) · p_v = Σ_p p_p S̄_vp (식 22) · v_v = p_v/m_v · 가중의 합 = 1 (식 23) → 전체 보존 (식 24–25).
9. **격자 → 입자**: ẋ_p = Σ_v v_v S̄_vp (식 26) · ṗ_p = m_p Σ_v a_v S̄_vp (식 27) — *"particle positions are updated using (grid) velocities, and particle velocities are updated using (grid) accelerations.  Interpolating changes in position and velocity in this way serves to reduce numerical diffusion"* · 운동량 변화 일치 (식 28).
10. **변형률 속도**: 격자 속도장의 대칭 기울기 (식 29 · 인쇄에서 Σ_v 는 생략된 꼴) 를 입자 영역에서 부피 평균 → ε̇_p = Σ_v ½(∇S̄_vp v_v + v_v ∇S̄_vp) (식 30).
11. **결론 (p.482)**: *"Eqn.s 14 – 18, 21, 22, 26, 27, and 30 are identical in form to those presented for MPM … The difference is that the weighting functions and gradient weighting functions have been generalized."*

### 4-2. 관찰 — 왜 매끈해지나 (§2.3 · `txt_p6_p7_observations_smoother_weighting_analytic.png` · `txt_p7_disorder_errors_reduced_not_eliminated.png`)

- 입자 영역으로 적분하면 격자 형상 함수가 매끈해진다 · 지지가 넓어진다 · S̄_vp∣x_p=x_v < 1 → 노드 위에 있는 입자도 그 노드에만 자료를 보내지 않는다 — *"It is precisely this property which improves performance in handling finite deformations"* (p.482).
- 규칙 격자 덕에 가중 함수를 해석적으로 만든다 (다른 무격자법은 *"considerable effort and computational cost"* · p.483).  MLPG 와 가장 가깝지만 MLPG 는 격자를 없애고 GIMP 는 고정 격자를 쓴다.
- ⚠ 한정: *"However local grid data errors due to particle disorder are only reduced, not eliminated, by using smoother interpolation functions."* → 대신 *"GIMP methods can be easily constructed in which local grid data errors are eliminated completely in at least one important situation"* = 균일 응력 + 현재 분할의 합 = 1 (식 31–33).

### 4-3. MPM = 특수한 경우 (§2.3 · §3.1 · 식 34 · `eq_34_mpm_dirac_delta_special_case.png`)

- **χ_p(x) = δ(x − x_p)V_p** (식 34) → S̄_vp = S_v(x_p) · ∇S̄_vp = ∇S_v(x_p) — *"the formulation presented in [Sulsky, Chen, and Schreyer (1994); Sulsky, Zhou, and Schreyer (1995)] is recovered exactly"* (p.484).  *"the MPM discretization scheme represents a special case where grid shape functions are not smoothed in the construction of the weighting functions."*
- 장점 · 단점 (p.485 · `txt_p9_mpm_registration_abrupt_point_mass_inconsistency.png`): *"computationally efficient because a given particle interpolates information only to the vertices of the grid cell it is contained in … However, this also results in the interpolation being strongly dependent on the registration of the particles on the grid, potentially changing abruptly as particles cross cells."*
- 모순 (p.485): 델타는 분할의 합이 아니라 처음 이산화 (§2.1) 에 못 쓴다 — *"an inconsistency wherein the material points mass and volume are assigned as required by the initial mass density of the continuum body on one hand, but then are assumed to represent infinitesimal points on the other."*
- 격자 형상 함수 (모든 예): 1D 텐트 S_v(x) (식 35 · Fig. 1) · 균일 격자 L_v = L · 다차원은 1D 텐트의 곱.

### 4-4. ★ contiguous particle GIMP (§3.2 · 식 36–40 · Fig. 2 · `txt_p9_p10_contiguous_particle_gimp_C1_cost.png`)

- χ_p(x) = H(x − (x_p − l_p)) − H(x − (x_p + l_p)) (식 36) = 1 (x ∈ Ω_p) · 0 (밖) (식 37) · 2l_p = 현재 입자 크기 · 처음 크기 2l_p^i = L ÷ 셀당 입자 수 → *"contiguous regions of non–overlapping support Ω_p"*.
- *"This generalization is the simplest finite particle generalization in the sense that it retains the grid shape functions used in the original implementation of MPM … but replaces particle mass points with particle volumes.  It represents the very next degree of smoothness obtainable in the family of GIMP methods (with tent grid shape functions)."* (p.485)
- 가중 S̄_vp = (1/2l_p)∫_{x_p−l_p}^{x_p+l_p} S_v(x)dx (식 38) · ∇S̄_vp = (1/2l_p)∫∇S_v(x)dx (식 39) · ∇S̄_vp(x_p) = ∂S̄_vp(x_p)/∂x_p.
- **식 (40)** (`eq_40_cpgimp_piecewise_weighting_function.png`) — d = x_p − x_v 의 7 구간: 0 (d ≤ −L − l_p) · (L + l_p + d)²/(4Ll_p) · 1 + d/L · 1 − (d² + l_p²)/(2Ll_p) (∣d∣ ≤ l_p) · 1 − d/L · (L + l_p − d)²/(4Ll_p) · 0 (d > L + l_p).  *"This specialization has the advantage that it develops weighting functions in C¹ with a minimal amount of additional complexity"* (p.486).  카드 확인: 식 (40) 은 텐트를 [x_p − l_p, x_p + l_p] 에서 평균한 값과 수치로 같다 (차 ≤ 1.2 × 10⁻⁵ · 적분 이산 오차 수준) · 노드에 대한 합 = 1 (식 23) [카드 산술 · 수치 확인].
- **폭을 고정하는 근사 (= 예제의 'GIMP')** (p.486 · `txt_p10_untracked_particle_size_boundary_loss.png`): *"An approximation to the exact weighting functions, which provides considerable simplification in practice, is provided by not tracking current particle volumes, i.e. l_p(t) = l_p^i ∀ p, t.  This is a good approximation for small deformations.  However, errors develop when particle volumes fail to remain contiguous, or overlap the computational boundaries, during finite deformations."* — 경계 밖으로 나간 몫의 질량 · 운동량은 격자로 안 간다.
- **'Finite (contiguous particle) GIMP'** (p.489): *"particle widths are tracked and used in the interpolation functions S̄_vp.  Hence the particle characteristic functions remain a partition of unity throughout the deformation.  Particle characteristic function overlap at the boundary is eliminated and the full weight of the column is reflected in the solution."* — 폭 갱신 식은 미인쇄 [미확인] (1D 에서는 F 로 늘이면 된다 [카드 추론]).

### 4-5. fuzzy particle GIMP (§3.3 · Fig. 3) — 계산 없음

- 겹치는 입자 특성 함수 (1D 텐트 꼴 · 셀당 2 입자 그림) 두 가지: (a) 가장 가까운 이웃과만 겹침 · f(x_p) = f_p · Ω_p^i ≤ 2L — 자료를 국소화 (b) 영역 안 모든 이웃과 겹침 (Ω_p^i = 2L 그림) · f(x_p) ≠ f_p — 무격자법이 선호하는 꼴 · 자료를 퍼뜨림.  셀당 1 입자면 둘이 같아진다.
- *"Both overlapping particle scenarios are a natural extension of the piecewise constant representation of particles (contiguous particle GIMP) to piecewise linear representations … Further analysis/experimentation is needed … their complementary functionality is suggestive of utility in particle addition and deletion algorithms in conjunction with computational grid refinement and coarsening."* (p.487)

### 4-6. ★ 셀 넘김 잡음의 기전 (§4.1 · p.488 · `txt_p12_cell_crossing_noise_force_imbalance.png`)

- **MPM**: 기울기 가중이 불연속 (텐트의 기울기 ±1/L) → 균일 응력 물질점이 격자에 고르지 않게 놓이면 (이웃 셀의 입자 수가 다르면) 노드에 힘 불균형 · 크기 ∝ **입자 응력 × 노드 양쪽 입자 수의 차**.
- **contiguous GIMP**: *"The contiguous particle GIMP gradient weighting functions reduce these artificial force imbalances substantially.  As gaps or overlaps in particle characteristic functions develop (as material points move relative to each other), the particle characteristic functions are no longer a partition of unity and artificial force imbalances can still develop.  However, these force imbalances are proportional to the stress multiplied by the ratio of the gap or overlap volume to the initial particle volume, and only develop when the gaps or overlaps register non–uniformly on the grid."*
- 카드 산술 (식 16 · 35 · 1D · 셀당 2): MPM 의 불균형 = ∣σ∣V_p∣n_L − n_R∣/L = ∣σ∣/2 (한 개 차) — 중력 노드 힘 ρ₀L∣b∣ 의 ≈ 10 배 (W 12,000 · x ≈ 29.5 · §3-2).  GIMP (폭 고정) 의 불균형은 ∣σ∣ × (겹침 ÷ 입자 부피) 꼴 — 국소 변형률 ≈ 0.5 % 면 같은 자리에서 ≈ 12 (중력의 5 %) [카드 산술 · 어림].
- **잠김**: 동적 문제에서 MPM 교란이 *"locked in as required to maintain equilibrium on the grid for non–uniform particle registration"* (p.490).
- **해상도와 함께 나빠짐**: *"for the same deformation, decreasing the cell size results in increasing the number of cell crossings and corresponding noise"* · finite grid instability = *"originates because the particles can support solution variation wavelengths which are unresolvable on the computational grid.  This instability has been shown to depend on the degree of smoothness of the weighting functions, the Mach number of the problem, and the numerical integration scheme used, [Brackbill (1988)]"* (p.493).

### 4-7. ★ 입자 처리 (DEM 의 "무질서 처리" 대응)

| 축 | 이 논문 |
|---|---|
| 물체 | 1D 연속 막대 하나 — 알갱이 · 입자 층 · 접촉이 없다 ('입자' = 물질점) |
| 무질서 | 처음 배치는 규칙 (셀당 1 · 2 · 4 균등 · 상자 폭 L/ppc) — 무질서 · 여러 실현 없음 · 무질서는 변형이 만든 **격자 위 등록의 불균일** 뿐 |
| 크기 | 물질점 크기 2l_p = L/ppc (상자) · 폭 고정 (GIMP) ↔ 추적 (Finite GIMP) |
| 변형 | 1D 초탄성 · 평균 2 % — **형상 변화 · 소성 흐름 없음** |
| 접촉 | 없음 (강체 벽 = 계산 경계 · 충격 문제) |
| 경계 | 바닥 = 계산 격자 경계 (준정적 · 충격) · 위 = 자유 끝 |

### 4-8. ★ 우리 2차 B-spline 가중과의 관계 (원문 식으로 · 판정 없이 · 전부 [카드 산술] / [다른 카드])

1. **식 (40) 에 l_p = L/2 (셀당 입자 하나 · 폭 고정) 를 넣으면** 선형 구간 (−L + l_p < d ≤ −l_p) 이 사라지고 S̄_vp(d) = 3/4 − (d/L)² (∣d∣ ≤ L/2) · ½(3/2 − ∣d∣/L)² (L/2 < ∣d∣ ≤ 3L/2) · 0 (그 밖) = **2차 B-spline N₂(d/L) 와 정확히 같다** (식 대입 · 수치 확인 최대 차 1.1 × 10⁻¹⁶).  ⇒ 원문의 *"quadratic when only one particle is used per cell"* (p.493) 의 정체.
2. 같은 근사에서 기울기 가중 (식 39) = dN₂/dx_p (꼭대기 근처 −2d/L²) — B-spline MPM 의 ∇N 과 같다.
3. 셀당 입자가 둘 이상인데 2차 B-spline 을 쓰면, GIMP 틀로는 **폭 L 의 겹치는 상자** (셀당 2 이면 χ_p = ½ 의 상자 둘이 겹쳐 합 = 1) 와 같다 — 처음 규칙 배치에서만 분할의 합 = 1 이고 입자가 움직이면 깨진다 [카드 추론].  원문 §4-4 의 '폭 고정 → 틈 · 겹침이 생기면 불균형' 이 그대로 걸리는 자리.
4. **우리 MLS-MPM** 은 전달에 2차 B-spline 가중을 쓰고 [다른 카드 `hu2018_mls_mpm_cpic_two_way_rigid_coupling` §4 · 우리 기록], 내부력에는 ∇N 대신 **M_p⁻¹ N_i(x_p)(x_i − x_p)** (M_p = Δx²/4) 를 쓴다 — 1D 로 풀면 노드 바로 옆에서 ∇N 의 1.5 배 · s = ½ · 1 에서 같음 · s = 1.25 에서 0.625 배 [다른 카드 `hu2018_…` §4-3 카드 산술].  ⇒ 우리 전달 가중 = 이 논문의 '셀당 1 · 폭 고정 contiguous GIMP' 와 같은 함수 · 우리 내부력 기울기 = 이 논문 식 (16) + (39) 와 **다른 꼴** (합 0 · 선형장 재현은 같다 [다른 카드]).
5. 이 논문이 MPM 과 GIMP 를 가른 성질 — ① 처음 이산화와 풀이에 같은 χ_p ② 현재 배치의 분할의 합 = 1 → 균일 응력에서 내부력 0 ③ 경계에서 지지가 격자 안에 들어가는가 — 을 우리 MLS-MPM 에 대 보는 것은 **우리 단위 시험의 몫**이다 (이 논문은 MLS 를 모른다).  특히 ③: 2차 B-spline 의 지지는 입자에서 1.5 셀 — 판 · 벽 근처에서 격자 밖 노드 (유령 노드) 처리가 필요하다는 원문 경고 (p.483) 가 걸린다 [카드 추론].

---

## 5. 결과 — 절별

### 5-1. 서론의 논증 (§1 · p.477–479)

FEM 은 성공적이지만 복잡한 3D 물체의 몸에 맞춘 격자 생성 · 큰 변형의 격자 뒤틀림 (재격자화 필요) 이 어렵다 → 점에서 이산화하고 몸에 맞춘 격자를 유지하지 않는 무격자법들 (SPH · Diffuse Element · EFG · RKPM → Partition of Unity Method · ACPG-FEM · MLPG).  MPM 은 PIC 계보의 최신 (*"In MPM the grid may be viewed as a temporary computational scratch pad, as the material points carry the complete solution"* · p.478) 이고 상태 변수를 실은 Lagrange 입자라 이력 의존 구성식에 맞다.  MPM 의 변분형 유도 (Sulsky 외) 가 있었지만 그 틀로 **이산화 자체를 일반화하는 데는 쓰이지 않았다** — 이 논문이 그 일반화다.

### 5-2. 이산 식 (§2 · 식 1–33)

§4-1 · §4-2.  핵심 = 가중 함수만 바뀌고 MPM 식의 꼴은 그대로 · 분할의 합 = 1 이 보존과 균일 응력 평형을 쥔다.

### 5-3. 예시 GIMP (§3 · 식 34–40 · Fig. 1–3)

MPM (델타) → contiguous (상자 · C¹) → fuzzy (겹침 · 선형 조각).  3D 에서 유한하고 변형하는 입자의 실제 구현은 입자 영역 적분 때문에 복잡 → 1D 로 시험 · 폭을 추적하지 않는 근사도 같이 본다 (`txt_p8_p9_3d_practical_complication_untracked_approx.png`).

### 5-4. 준정적 압축 (§4.1 · Fig. 4 · 5)

넘김 전 (W 10,000) 세 해가 겹친다 → 첫 넘김 (W 12,000) 에 MPM 이 x ≥ 29 와 기둥 나머지에서 흔들린다 → W 30,000 에서 가짜 힘이 물리 힘을 압도 → W 40,000 에서 MPM 흔적만 남고, GIMP 는 매끈하나 바닥 응력을 작게 (폭 고정 → 경계 손실) · Finite GIMP 는 해석해와 겹친다.  요약 (`txt_p12_p13_mpm_destroyed_gimp_weight_finite_gimp_summary.png`): *"In summary, the MPM algorithm can be very noisy.  Neighboring material points may experience computational artifacts resulting in radically different deformation histories, compromising the accuracy of stress evaluations, especially for history dependent, inelastic materials.  Material point stress oscillations may even become strong enough to overwhelm the physical forces in the system and destroy the solution, as seen in this example."* (p.489)

### 5-5. 동적 압축 (§4.2 · Fig. 6–8)

넘김 전 (t 0.25) 두 해 비슷 (MPM 은 셀 안 응력이 균일 · GIMP 는 번진 충격면과 더 맞음) → 첫 넘김 직후 (Fig. 6b · t 0.30 · 꼭짓점 x_v = 13) 에 MPM 만 흔들림 → t 0.75 · 1 에 그 교란이 그 자리에 잠긴다 · 충격이 끝에 닿은 t = 1 에 셋 든 셀이 하나 더 (MPM x ≈ 37–39 무리) · GIMP 훨씬 매끈 → Finite GIMP 가 정보 손실을 고친다 (Fig. 8 · 그림 세로 범위를 −22,000 … −16,000 으로 줄여서야 둘이 갈린다).

### 5-6. 셀당 입자 수 (§4.3 · Fig. 9)

MPM: 입자 수가 큰 튐의 빈도를 정한다 (등록 불균일의 자세한 꼴이 입자 수에 매임) · 크기는 조금 줄지만 더 잦아 전체로 더 시끄럽다.  GIMP: 입자 수와 무관하게 매끈 · 4 p/c 에서 짧은 파장 잡음 (l_p → 0 이면 MPM 으로 감) → *"the result is unexpected"* (PIC 에서는 입자를 늘리면 매끈해진다고 기대하므로) · 적은 입자가 유리 = 실용적으로 중요.

### 5-7. 수렴 (§4.4 · Fig. 10 · 11)

MPM = 어느 셀 크기 아래에서 오차가 커진다 (finite grid instability 를 셀 넘김 잡음이 키움 · 좋은 효과와 가를 방법이 없다) · 입자를 늘리면 넘김 잡음은 줄고 최소 뒤 오차 누적이 느려진다.  GIMP = 더 넓은 범위에서 수렴 · 1 p/c 가 늘 조금 낫다 · 경계 효과 값에서 포화 (*"For this algorithm the combination of smoother interpolation and reduced cell crossing noise prevents the finite grid instability from dominating the quality of the calculations"*).  Finite GIMP = 전 범위에서 가장 빠름 · 1 p/c 가 최적일 수 있다 · 가장 고운 격자의 바닥 = 동역학 (재하 속도 ×5 · ÷4 로 확인).

### 5-8. 결론 (§5 · p.494 · `txt_p18_conclusions_mpm_infinitesimal_only.png`)

> (원문 *it* 그대로) *"Two practical advantages of the GIMP methods stand out it this context.  The first is the advantage of using a spatially fixed mesh in generating the weighting functions used to develop continuous representations of discrete data.  The second is the lack of any special treatment required near computational boundaries due to weighting function overlap."*

> *"For this reason, it is suggested that the MPM algorithm only be used for infinitesimal deformation problems, defined in practice by the absence of cell crossings.  For finite deformation problems, greater continuity in interpolation between material points and the computational grid is required for accurate solutions.  The very next degree of smoothness available in the family of GIMP methods, dubbed the contiguous particle GIMP method, is demonstrated to perform decidedly better."*

---

## 6. 그림 · 식 · 근거 글 크롭별 (원 캡션 요지 + MPM 관점)

> 파일 = `litdb/figures/bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing/` · 그림 11 장 (도구 7 장 그대로 · Fig. 7 다시 자름 1 · Fig. 1 · 2 · 10 손 크롭 3 · 300 dpi · 캡션 글자는 figures.json) + 식 47 장 (식 번호마다 하나 · 400 dpi · 사방 7 pt) + 근거 글 20 장 (300 dpi · 여러 토막은 회색 선으로 가름) + `digitized.csv`.  표 없음 · 보충 자료 없음.  [우리 …] 표지는 논문 밖 판단.

| 그림 | 파일 | 원 캡션 요지 | MPM 관점 (우리 MPM · 재설계 후보) |
|---|---|---|---|
| 1 | `fig_1.png` | 1D 텐트 격자 형상 함수 (모든 GIMP 예에 공통) | S_v(x − x_v) — 지지 ±L · 기울기 ±1/L 의 불연속이 MPM 셀 넘김 잡음의 뿌리 (식 35) |
| 2 | `fig_2.png` | contiguous particle GIMP 가중 함수 (1D) | S̄_vp(x_p − x_v) · 꺾임점 ±l_p · L ± l_p · 꼭대기 < 1 (1 − l_p/2L).  **l_p = L/2 이면 2차 B-spline** [카드 산술 §4-8] — 그림은 도식 (꺾임점은 l_p = 0.20 L 인데 'l_p' 눈금 하나만 0.25 L · 높이도 식 40 과 다르다 [판독 — 경로 좌표 · §12-C 6]) |
| 3 | `fig_3.png` | 셀당 2 입자의 fuzzy 이산화 두 꼴 (a) 이웃과만 겹침 (b) 모두와 겹침 | 계산 없는 도식 — 입자 추가 · 삭제 · 격자 세분과 함께 쓰일 수 있다는 저자 전망뿐 |
| 4 | `fig_4.png` | 준정적 기둥 — (a) W 10,000 (b) W 12,000 · △ MPM · ○ GIMP · 대각선 = 해석해 · 세로 점선 = 셀 경계 | ★ [판독] (a) 둘 다 W 의 ≤ 1 % · (b) MPM 최대 1,682 (14 %) @ x ≈ 29 · GIMP 1.7 %.  **우리 쪽**: 해석해가 있는 준정적 단위 시험의 꼴 — 우리 MLS-MPM (3D 일축 막대 · 측면 고정) 로 같은 기둥을 돌려 '첫 셀 넘김 전후' 편차를 같은 노름 (식 47) 으로 적는다 |
| 5 | `fig_5.png` | 같은 기둥 (a) W 30,000 (b) W 40,000 · (b) 의 × = Finite GIMP | ★ [판독] (a) MPM ≥ 63 % (점 10 개 그림 밖) · GIMP 2.3 % (b) GIMP 바닥 −5.2 % · Finite −0.01 %.  **우리 쪽**: 반력 (바닥 응력) 이 경계 처리에 따라 수 % 치우칠 수 있다는 사례 — 우리 판 반력 (wallP) 을 해석해 기둥에서 먼저 잰다 |
| 6 | `fig_6.png` | 막대 충격 (a) t = 0.25 (b) t = 0.30 (파 통과 시간 기준) · 가로선 = 충격 뒤 해석 −20,000 | [판독] 넘김 전에도 충격 뒤 ±10–12 % 울림 (인공 점성 · 충격면) · (b) MPM 만 x ≈ 12–13 에서 튐 (x 12.99: MPM −8,903 ↔ GIMP −16,079 · 둘 다 번진 충격면 안).  **우리 쪽**: 셀 넘김 잡음과 충격면 울림을 가르는 '넘김 전' 기준선 그림 |
| 7 | `fig_7.png` | 같은 충격 (a) t = 0.75 (b) t = 1 | ★ [판독] MPM 교란 9,083–9,159 (45–46 %) 이 x ≈ 13 에 잠김 · GIMP ≤ 9.6 %.  **우리 쪽**: 셀 넘김 교란은 시간이 지나도 안 풀린다 — 준정적 압밀의 '정착' 응력에도 남을 수 있다 [카드 추론] |
| 8 | `fig_8.png` | t = 1 의 GIMP (○) ↔ Finite GIMP (×) · 세로 범위 −22,000 … −16,000 | [판독] 평균 −19,787 (−1.1 %) ↔ −20,013 (+0.06 %).  **우리 쪽**: 입자 영역을 추적하지 않는 보간의 '정보 손실' 은 평균 1 % 급 치우침으로 나타났다 |
| 9 | `fig_9.png` | (a) MPM (b) GIMP · 셀당 1 · 2 · 4 입자 · t = 1 | [판독] MPM 큰 튐 > 2,000 이 2 · 7 · 11 개 · GIMP 0 개.  **우리 쪽**: 셀당 물질점을 늘려 잡음을 줄이려는 시도는 C⁰ 보간에서 역효과 — 우리 씨앗 밀도를 정할 때 1 · 2 · 4 사다리를 같이 돌린다 |
| 10 | `fig_10.png` | MPM · GIMP · Finite GIMP × 1 · 2 · 4 p/c 의 셀 크기 수렴 (W 10,000) · 선 = 1 차 · 2 차 | ★ §3-5 표.  **우리 쪽**: U6 (해상도 수렴) 의 설계 꼴 — 셀 크기 세 자리 × 셀당 입자 셋 · 같은 노름 · '최소 뒤 상승' 이 보이면 finite grid instability 를 의심 |
| 11 | `fig_11.png` | 1 p/c Finite GIMP 의 수렴 · 중력 5 배 빠름 / 기준 / 4 배 느림 | ★ [판독] 셀 0.01 바닥 3.1e−6 · 1.3e−6 · 4.7e−7.  **우리 쪽**: 고운 격자의 오차 바닥을 재하 속도가 정한다 — 우리 판 Mach 사다리 (0.03 → 0.01) 를 격자 사다리와 **엇갈려** 돌려야 두 오차를 가른다 |

**식 그림** (전부 손 크롭 · 400 dpi · 사방 7 pt 흰 여백 · 식 번호 포함 · 이웃 글줄 · 머리글 없음):

| 식 | 파일 | 내용 | 쓰임 |
|---|---|---|---|
| (1) | `eq_01_variational_form_momentum.png` | ∫ρa·δv + ∫σ:∇δv = ∫ρb·δv + ∫τ·δv dS | 지배 방정식 (약형) |
| (2) | `eq_02_initial_partition_of_unity_chi.png` | Σ_p χ_p^i(x) = 1 | 처음 배치 분할의 합 |
| (3) | `eq_03_initial_particle_volume.png` | V_p^i = ∫χ_p^i dx | 처음 부피 |
| (4) | `eq_04_initial_particle_mass.png` | m_p^i = ∫ρ^i χ_p^i dx | 처음 질량 |
| (5) | `eq_05_initial_particle_momentum.png` | p_p^i = ∫ρ^i v^i χ_p^i dx | 처음 운동량 |
| (6) | `eq_06_initial_particle_stress.png` | σ_p^i = ∫σ^i χ_p^i/V_p^i dx | 처음 응력 (부피 평균) |
| (7) | `eq_07_initial_total_mass_conserved.png` | Σ m_p^i = ∫ρ^i dx | 처음 질량 정확 보존 |
| (8) | `eq_08_initial_total_momentum_conserved.png` | Σ p_p^i = ∫ρ^i v^i dx | 처음 운동량 정확 보존 |
| (9) | `eq_09_particle_data_representation.png` | f(x) = Σ f_p χ_p(x) | 입자 자료의 연속 표현 |
| (10) | `eq_10_weak_form_sum_over_particles.png` | 식 (1) 의 입자별 합 꼴 | 시행 함수 = χ_p |
| (11) | `eq_11_current_particle_volume.png` | V_p = ∫_{Ω_p∩Ω} χ_p dx | 현재 부피 |
| (12) | `eq_12_grid_data_representation.png` | g(x) = Σ g_v S_v(x) | 시험 함수 = 격자 형상 함수 |
| (13) | `eq_13_grid_shape_partition_of_unity.png` | Σ S_v = 1 | 격자 분할의 합 |
| (14) | `eq_14_discrete_grid_momentum_equation.png` | ṗ_v = f^int + f^b + f^τ | 격자 운동량 식 (집중 질량) |
| (15) | `eq_15_grid_momentum_rate.png` | ṗ_v = Σ S̄_vp ṗ_p | |
| (16) | `eq_16_internal_force_gradient_weighting.png` | f_v^int = −Σ σ_p·∇S̄_vp V_p | ★ 내부력 — 셀 넘김 잡음이 생기는 항 |
| (17) | `eq_17_body_force.png` | f_v^b = Σ m_p b S̄_vp | 체적력 |
| (18) | `eq_18_traction_force.png` | f_v^τ = ∫τ S_v dS | 표면력 |
| (19) | `eq_19_weighting_function_Svp.png` | S̄_vp = (1/V_p)∫χ_p S_v dx | ★ 가중 함수의 일반 꼴 |
| (20) | `eq_20_gradient_weighting_function.png` | ∇S̄_vp = (1/V_p)∫χ_p ∇S_v dx | ★ 기울기 가중의 일반 꼴 |
| (21) | `eq_21_grid_mass_p2g.png` | m_v = Σ m_p S̄_vp | 입자 → 격자 질량 |
| (22) | `eq_22_grid_momentum_p2g.png` | p_v = Σ p_p S̄_vp | 입자 → 격자 운동량 |
| (23) | `eq_23_weighting_partition_of_unity.png` | Σ_v S̄_vp = 1 | 가중의 분할의 합 |
| (24) | `eq_24_total_mass_conserved_p2g.png` | Σ m_v = Σ m_p | 전달의 질량 보존 |
| (25) | `eq_25_total_momentum_conserved_p2g.png` | Σ p_v = Σ p_p | 전달의 운동량 보존 |
| (26) | `eq_26_particle_position_update.png` | ẋ_p = Σ v_v S̄_vp | 격자 → 입자 위치 |
| (27) | `eq_27_particle_momentum_update.png` | ṗ_p = m_p Σ a_v S̄_vp | 격자 → 입자 운동량 (가속도 보간) |
| (28) | `eq_28_momentum_change_consistency.png` | Σ ṗ_p = Σ ṗ_v | 운동량 변화 일치 |
| (29) | `eq_29_grid_strain_rate.png` | ε̇(x) = ½(∇v + ∇vᵀ) = ½(∇S_v v_v + v_v∇S_v) | 격자 변형률 속도 (Σ_v 생략된 인쇄) |
| (30) | `eq_30_particle_strain_rate_volume_average.png` | ε̇_p = Σ_v ½(∇S̄_vp v_v + v_v ∇S̄_vp) | 입자 변형률 속도 |
| (31) | `eq_31_internal_force_uniform_stress.png` | f_v^int = −σ·Σ ∇S̄_vp V_p | 균일 응력의 내부력 |
| (32) | `eq_32_current_partition_of_unity_chi.png` | Σ χ_p(x) = 1 (현재 배치) | ★ 조건 |
| (33) | `eq_33_zero_internal_force_interior_vertices.png` | f_v^int = −σ·∫∇S_v = 0 if Ω_p∩Ω = Ω_p | ★ 내부 노드 평형 (인쇄에 dx 빠짐) |
| (34) | `eq_34_mpm_dirac_delta_special_case.png` | χ_p(x) = δ(x − x_p)V_p | ★ MPM = 특수한 경우 |
| (35) | `eq_35_tent_grid_shape_function_1d.png` | 1D 텐트 S_v(x) | 격자 형상 함수 |
| (36) | `eq_36_contiguous_particle_step_functions.png` | χ_p = H(x − (x_p − l_p)) − H(x − (x_p + l_p)) | contiguous 상자 |
| (37) | `eq_37_contiguous_particle_indicator.png` | χ_p = 1 (Ω_p 안) · 0 (밖) | 같은 것 |
| (38) | `eq_38_contiguous_weighting_integral.png` | S̄_vp = (1/2l_p)∫S_v dx | contiguous 가중 |
| (39) | `eq_39_contiguous_gradient_weighting_integral.png` | ∇S̄_vp = (1/2l_p)∫∇S_v dx | contiguous 기울기 가중 |
| (40) | `eq_40_cpgimp_piecewise_weighting_function.png` | 7 구간 꼴 (§4-4) | ★ C¹ 가중 · l_p = L/2 ⇒ 2차 B-spline |
| (41) | `eq_41_hyperelastic_1d_sigma_E_F_minus_1.png` | σ = E(F − 1) | 시험 재료 |
| (42) | `eq_42_static_column_analytic_stress.png` | σ(x) = E{√[(2ρ₀b/E)(Δ − x) + 1] − 1} | ★ 기둥 해석해 |
| (43) | `eq_43_column_current_length.png` | Δ = Δ₀ + ρ₀bΔ₀²/(2E) | 기둥 현재 길이 |
| (44) | `eq_44_column_weight_W.png` | W = ρ₀∣b∣Δ₀ | 기둥 무게 (보고 축) |
| (45) | `eq_45_artificial_viscosity_q.png` | q = c₁ρc∣ε̇L∣ + c₂ρ(ε̇L)² (ε̇ < 0) | 인공 점성 |
| (46) | `eq_46_deformation_gradient_behind_shock.png` | F = (ct − v₀t)/(ct) = 1 − v₀/c | 충격 뒤 해석해 |
| (47) | `eq_47_particle_stress_error_measure.png` | Error = Σ ∣σ(x_p) − σ_p∣2l_p/(WΔ₀) | ★ 오차 노름 |

**근거 글 크롭 20 장** (카드가 인용한 문장의 문단만 · 300 dpi): `txt_p1_header_title_authors_affiliations.png` (서지 · 소속) · `txt_p1_abstract_noise_destroys_degrades.png` · `txt_p1_intro_fem_mesh_distortion_remeshing.png` · `txt_p2_p3_smoother_representation_removes_artifact.png` · `txt_p3_particle_characteristic_functions_definition.png` · `txt_p6_p7_observations_smoother_weighting_analytic.png` · `txt_p7_disorder_errors_reduced_not_eliminated.png` · `txt_p8_mpm_special_case_not_partition_of_unity_lumped_mass.png` · `txt_p8_p9_3d_practical_complication_untracked_approx.png` · `txt_p9_mpm_registration_abrupt_point_mass_inconsistency.png` · `txt_p9_p10_contiguous_particle_gimp_C1_cost.png` · `txt_p10_untracked_particle_size_boundary_loss.png` · `txt_p11_example_setup_E_c_L_dt_40_transits.png` · `txt_p12_final_body_force_W40000_first_crossings.png` · `txt_p12_cell_crossing_noise_force_imbalance.png` · `txt_p12_p13_mpm_destroyed_gimp_weight_finite_gimp_summary.png` · `txt_p13_p14_dynamic_compaction_setup_shock_locked_in.png` · `txt_p15_information_loss_and_particles_per_cell.png` · `txt_p17_p18_convergence_finite_grid_instability_saturation.png` · `txt_p18_conclusions_mpm_infinitesimal_only.png` (파일 이름의 pN = PDF 쪽).

---

## 7. Post-processing

| 무엇 | 어떻게 | 우리에게 |
|---|---|---|
| 입자 응력 그림 | 물질점 위치 · 응력을 표지로 + 점선으로 이어 비균일을 강조 · 셀 경계 세로선 · 해석해 선 | 우리 MPM 의 판 반력만 보지 말고 **입자 응력의 공간 분포** 를 셀 경계와 함께 그린다 (셀 넘김 잡음은 그 그림에서만 보인다) |
| 오차 노름 | 식 (47) — 입자 위치의 해석해와 입자 응력의 차를 입자 폭으로 가중 · W Δ₀ 로 정규화 | U6 · 단계 2 의 기록 꼴 (결과 전에 노름을 적는다) |
| 수렴 그림 | 로그–로그 · 1 차 · 2 차 기준선 · 셀 크기 세 자리 × 셀당 입자 셋 | 같은 꼴 |
| 재하 속도 대조 | 같은 셀 사다리를 재하 속도 ×5 · ÷4 로 반복 | 판 Mach 사다리와 격자 사다리를 엇갈려 |
| **이 카드의 판독** (논문 밖) | 벡터 그림 경로 → 눈금 글자 중심으로 축 사상 (최소제곱 · 잔차 ≤ 0.02 눈금) → 표지 중심 (gnuplot 삼각형은 밑변 − 0.5 hpt · 원 · 네모 = 상자 중심 · × + ✳ = 획 중점) · Fig. 9 는 꺾은선 꼭짓점 → `digitized.csv` | `[판독]` 의 출처 — 같은 PDF 가 있으면 다시 낼 수 있다 |

---

## 8. 우리 DEM + MPM 대비

### 8-1. 정면 비교

| 축 | 이 논문 | 우리 DEM | 우리 MPM |
|---|---|---|---|
| 기법 | MPM · GIMP (1D · 명시적 · 셀 고정) | LIGGGHTS 구 입자 [우리 기록] | 명시적 MLS-MPM (Taichi · 2차 B-spline 가중) [우리 기록 · `hu2018_…` 카드] |
| 보간 | 텐트 (MPM · C⁰ 기울기) · 상자 평균 (GIMP · C¹) | — | 2차 B-spline (= 이 논문의 셀당 1 · 폭 고정 GIMP 와 같은 가중 [카드 산술]) · 내부력은 MLS 대용 기울기 [다른 카드] |
| 재료 | 1D 초탄성 σ = E(F − 1) · E 10⁶ (무차원) | 탄성–이력 접촉 · E_eff 1.35 GPa (18 배 연화) [우리 기록] | J2 소성 · E 1.53 GPa · ν 0.49 · σ_y 0.30 GPa [우리 기록] |
| 변형 | 평균 2 % (기둥) · 2 % (충격) | 겹침 | 순수 SE · 복합 압밀 (기공 수십 % → 10 % 급) [우리 기록] — 셀 넘김은 이 논문보다 훨씬 많다 [카드 추론] |
| 하중 | 중력 선형 증가 (파 통과 40 회) · 충격 v₀/c 0.02 | 300 MPa 까지 | 판 Mach 0.01–0.03 [우리 기록] |
| 해상도 시험 | 셀 0.01–10 × 1 · 2 · 4 p/c · 오차 노름 | 해당 없음 | 침대별 d_h/dx 점검 · 격자 사다리 (CLAUDE.md) [우리 기록] |
| 접촉 · 탈압 | 없음 | 접촉 법칙 · 분리 | 한 속도장 (붙음) · 분리 판정 없음 [우리 기록] |
| 검증 | 해석해 둘 (준정적 · 충격) | 실험 기공 (따로 보정) | 실험 기공 · 형상 (따로 보정) |

### 8-2. 전이되는 것 / 안 되는 것

| | 내용 |
|---|---|
| **전이 (방법)** | ① 가중 함수의 일반 꼴 (식 19–20) 과 MPM · GIMP · 2차 B-spline 의 관계 (§4-8) ② 셀 넘김 잡음의 기전과 크기 어림 (§4-6) ③ 해석해 단위 시험 둘 (식 42–44 · 46) 과 오차 노름 (식 47) ④ 수렴 시험 설계 (셀 세 자리 × 셀당 입자 셋 · 재하 속도 대조) ⑤ "명시적 · 저속 PIC 는 finite grid instability 에 취약" 의 원문 ⑥ FEM 격자 생성 · 뒤틀림의 원문 (2004) |
| **전이 (경고)** | ⑦ 셀당 물질점을 늘리는 것이 C⁰ 보간에서는 잡음을 키운다 ⑧ 입자 영역을 추적하지 않는 보간은 경계에서 질량 · 운동량을 잃어 경계 응력 (= 반력) 을 작게 낸다 ⑨ 격자를 조여도 C⁰ MPM 오차는 줄지 않을 수 있다 ⑩ 고운 격자의 오차 바닥은 재하 속도가 정한다 |
| **전이 안 됨** | 모든 값 (무차원 1D 초탄성 · 평균 변형률 2 %) — 우리 압밀의 응력 · 기공 · 반력의 대조값이 아니다.  3D · 접촉 · 소성 · 탈압에 대해서는 **아무 값도 없다** |

### 8-3. frame 판정

- **frame [5]**: MPM 쪽 절반 중에서도 **수치 기반 (보간 · 전달)** 만 다룬다 — 형상 변화 · 소성 흐름 · 응력장의 물리 결과는 없다.  우리 MPM 결과 (기공 · 형상 · 판 반력) 의 **수치 신뢰 한계**를 재는 자리에 쓴다.
- **frame [4]**: 실험 대조 · 맞춘 값이 없다 (맞춘 값 0 개) — 보정 · 교차검증 근거로 쓰지 않는다.  해석해 대조는 **코드 검증** (verification) 이다.
- 연화 틀 (frame [2]) 과 중립.

---

## 9. 깊은 통찰

① **"MPM 은 큰 변형에 강하다" 는 절반만 맞다.**  격자 얽힘이 없다는 뜻에서는 맞지만, 이 원전은 **응력은 셀 넘김마다 흔들린다**고 숫자로 보인다 — 평균 변형률 2 % 에서도 W 의 14 % (첫 넘김) → ≥ 63 % (W 30,000) [판독].  우리 MPM 의 판 반력 · 정착 응력 · 피복 · 소성 변형률 지도는 모두 물질점 응력 이력에서 나온다 → 그 신뢰는 **보간 매끈함**에 걸린다.

② **우리 2차 B-spline 은 이 논문 틀에서 '셀당 1 · 폭 고정 contiguous GIMP' 의 가중과 같다** (§4-8 · 식 40 대입 · 수치 확인).  그러니 이 논문의 GIMP 쪽 결과 — C¹ · 셀 넘김 잡음 크게 감소 · 셀당 1 이 가장 매끈 · 폭을 추적하지 않으면 경계 손실 · 틈 · 겹침 비례 잔류 불균형 — 가 우리 가중의 **기대 거동**이다 [카드 추론].  다만 우리 내부력은 MLS 대용 기울기라 식 (16)+(39) 와 꼴이 다르고, 3D · 큰 변형 · 소성에서는 아무도 재지 않았다 → 기대일 뿐이다.

③ **셀당 물질점 수의 직관이 뒤집힌다.**  PIC 에서 입자를 늘리면 매끈해진다는 기대와 달리, C⁰ MPM 은 큰 튐이 잦아져 더 시끄럽고 (2 → 7 → 11 개 · Fig. 9 [판독]) GIMP 도 l_p → 0 이면 MPM 으로 돌아간다.  ⇒ 우리 SE 씨앗 밀도 (구 하나당 물질점 · 셀당 물질점) 를 정할 때 '많을수록 좋다' 를 쓰지 않는다 — 1 · 2 · 4 사다리로 재는 것이 원문 설계.

④ **격자 수렴 시험이 거꾸로 갈 수 있다.**  C⁰ MPM 은 최소 뒤에 오차가 다시 커진다 (같은 변형에 셀이 작을수록 넘김이 많고, 저속 명시적 PIC 의 finite grid instability 를 그 잡음이 키운다).  우리 격자 사다리 (192 · 288 · 384) 에서 '조이면 값이 계속 움직인다' 를 볼 때 [우리 기록 · CLAUDE.md 의 d_h 접힘 · 비수렴 서술], 그것이 기하 해상 (협착 채널) 인지 보간 잡음 · 불안정인지를 가를 대조군이 필요하다 — 같은 침대를 **셀당 물질점 수만 바꿔** 돌린 팔 [카드 추론].

⑤ **반력은 경계 처리에 민감하다.**  폭을 고정한 GIMP 는 바닥 응력을 −5.2 % (W 40,000) 작게 냈고 평균 응력도 1.1 % 치우쳤다 (충격) [판독].  우리 wallP 는 판 노드에서 재는 반력이고 판 · 바닥 근처 물질점의 가중 지지가 격자 경계 밖으로 나가는지에 따라 같은 부류의 치우침이 생길 수 있다 [카드 추론] — 해석해 기둥 (중력 · 측면 고정) 으로 먼저 잰다.

⑥ **고운 격자의 오차 바닥은 동역학이다.**  Finite GIMP 1 p/c 의 바닥이 재하 속도 5 배에 2.4 배 · 1/4 에 1/2.8 [판독 · 카드 산술] — 판 Mach 와 격자 크기는 **엇갈린 두 손잡이**다.  우리 '판 Mach 0.03 → 0.01 에서 σ +4.8 %' [우리 기록] 같은 숫자는 격자 오차와 따로 읽을 수 없다 — 둘을 엇갈린 사다리로.

⑦ **"eliminating" 과 "reduce" 의 간격.**  초록은 *"capable of eliminating cell crossing noise"* 이고 본문은 *"reduce these artificial force imbalances substantially"* + 틈 · 겹침의 잔류 · *"only reduced, not eliminated"* (일반 매끈화) 다.  인용할 때는 본문 쪽 (감소 · 조건부 0) 으로 쓴다.

⑧ **이 논문의 '큰 변형' 은 작다.**  시험은 평균 2 % · 4 % 다 — 짝 카드 2005 판의 90 % 압축 반력 튐을 이 논문으로 '설명' 하려면 틈 · 겹침 기전 (§4-6) 을 큰 변형에 외삽해야 한다 [카드 추론].  2005 판의 튐 크기 · 원인을 이 논문이 **잰 것은 아니다**.

---

## 10. ★ 자세한 분석 — 우리 계획에 무엇을 주나

(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 = 1D 무차원 초탄성 막대 — **재료 · 차원 · 하중 · 변형 크기가 모두 우리와 다르다**.  기공 · 밀도 값이 없어 랩 표준과 나란히 놓을 숫자는 0 개.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | 기공은 없다.  꼴만: 오차 노름 (식 47) 을 **결과 전에 정의하고** 해석해와 견준 보고 방식 · 보고 시점 (W · t/파 통과 시간) 을 축으로 | 기공 연산자 · 기준 0 |
| **단계 1** (3D 메모리 · 장 수) | 지지 폭 MPM 2 → GIMP 3 노드 (1D) → 3D 텐서곱 8 → 27 [카드 산술] · *"storage … strongly influenced by the number of particles used, especially in three–dimensions"* · 3D 변형 입자 영역 적분은 수치로 (p.484) | 3D 수치 · 장 수 없음 |
| **단계 2** (2D MPM 코드 · 단위 시험) | ★ 해석해 단위 시험 둘: **준정적 중력 기둥** (식 42–44 · W_f 40,000 · 끝 변위 = 셀 하나) · **막대 충격** (식 46 · −E v₀/c) + 오차 노름 (식 47) + 셀 넘김 전후 비교 (W 10,000 ↔ 12,000) · 셀당 입자 1 · 2 · 4 | 1D 뿐 — 2D · 3D 판은 우리가 만든다 (측면 고정 일축 막대) |
| **단계 3** (2D 접촉 표현 비교) | 없음 — 단 어느 접촉 표현이든 같은 가중 위에 선다 (셀 넘김 잡음은 장마다 생긴다 [카드 추론]) | 접촉 0 |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 경고 둘: ① 비탄성 구성식은 잡음 입력에서 이력 변수가 틀리게 진화하고 소산이 크면 발산이 감춰진다 (p.494) → J2 반환을 거치는 우리 소성 변형률 · 정착 응력이 영향받을 자리 ② 저속 명시적 = finite grid instability 취약 (p.493) — 판 Mach 0.01–0.03 은 '저속' 쪽 [우리 기록 · 카드 추론] | σ_y · 기공 값 없음 — 맞춤 표적 아님 |
| **단계 5** (3D 복합 압밀) | 없음 — 얼린 AM 경계 근처 물질점의 가중 지지가 AM 노드 · 격자 경계와 겹치는 문제는 §4-8 ③ 과 같은 부류 [카드 추론] | — |
| **단계 6** (탈압 · 되돌아옴) | 없음 (하중 제거 0) — 잡음이 *"locked in"* 된다는 관찰 (충격 · p.490) 만 탈압 뒤 잔류 응력 해석의 경고로 [카드 추론] | — |
| **단계 7** (형상 · 피복 · 수송) | 없음 — 단 소성 변형률 · 응력 지도는 물질점 응력 이력에서 나오므로 셀 넘김 잡음의 공간 무늬 (셀 경계에 묶인 띠) 를 지도에서 걸러 볼 것 [카드 추론] | — |
| **후보 D0** (지금 DEM) | 없음 (DEM 0 회) | — |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 경계 쪽 원문 두 가지: contiguous 상자는 격자 안에 들어가 특별 처리 불필요 ↔ 지지를 넓힌 가중은 유령 노드 · 다른 보간 규칙이 필요 (p.483) · 폭을 고정하면 경계에서 질량 · 운동량 손실 (Fig. 5b · 8) — 판 · 벽 근처 처리의 점검 항목 | 접촉 규칙 0 |
| **후보 A · A′** (AM 강체 + 한 속도장 · 입자별 속도장) | 장이 늘어도 각 장의 전달은 이 논문의 가중 위 — 셀 넘김 · 경계 손실이 장마다 [카드 추론] | 다물체 0 |
| **후보 B** (입자별 FE + 접촉) | FEM 의 어려움 원문 (2004): *"body fixed FEM meshes can be difficult and time consuming to generate for complex three–dimensional objects.  Further, mesh distortion associated with large deformations compromises solution accuracy, ultimately requiring re–meshing"* (p.477) | FEM 계산 없음 · 시점 2004 |
| **후보 C · C′ · M0** | 없음 | — |
| **U0–U6** | **U6** (해상도 수렴) = Fig. 10 · 11 의 설계 그대로 (셀 세 자리 × 셀당 입자 셋 · 같은 Δt · 오차 노름 · 재하 속도 대조) + 함정 (C⁰ 는 최소 뒤 상승) · **U1** (입자 하나 압축 · 지름당 셀 수) 쪽은 '셀당 물질점 1 이 GIMP 최적' 이라는 1D 결과만 · **U0** · U2–U5 없음 | 지름당 셀 수 규칙 없음 (알갱이 없음) |
| **R1–R7** | 직접 해당 없음.  **R5** (맞추는 값은 모델마다 하나) — 이 논문은 맞춘 값 0 · 해석해 검증만 | R1–R4 · R6 · R7 0 |
| **결과 전 대조 항목** | 우리 코드의 **검증용** 해석해 (식 42 · 46) — 물리 대조값이 아니다 | 우리 압밀의 대조값 0 |

- **재료 · 차원 · 조건 차이**: 1D 연속 막대 ↔ 3D 알갱이 침대 · 초탄성 (무차원 E 10⁶) ↔ J2 소성 (E 1.53 GPa · σ_y 0.30 GPa) · 평균 변형률 2 % ↔ 압밀 큰 변형 · 계산 경계 = 강체 벽 ↔ 판 · 얼린 AM · 오차는 입자 응력 L1 노름 ↔ 우리 보고량은 기공 · 두께 · 판 반력 · 피복.

**구체 행동 (전부 [카드 추론] · 결과 전 등록 대상)**
1. **단계 2 의 첫 단위 시험 = 이 논문의 준정적 기둥** — 우리 MLS-MPM 으로 측면 고정 일축 막대 (중력 선형 증가 · 끝 변위 셀 하나) 를 돌려 식 (47) 노름 · 바닥 반력 (판 반력과 같은 자리) 을 해석해 (식 42) 와 견준다.  셀 크기 세 단 × 셀당 물질점 1 · 2 · 4 × 재하 속도 두 단.
2. **셀 넘김 전후 기준선**: 첫 셀 넘김이 나는 하중을 미리 계산해 (이 논문은 W 12,000 · x_v ≥ 30) 그 전후의 입자 응력 분포를 셀 경계와 함께 그린다 — 잡음의 크기를 W 대비 % 로.
3. **SE 씨앗 밀도 결정**: 같은 침대를 셀당 물질점 수만 바꿔 (1 · 2 · 4 급) 판 반력 · 기공 · 소성 변형률 지도의 변화를 적는다 — '많을수록 좋다' 를 쓰지 않는다.
4. **격자 사다리 해석의 대조군**: 격자를 조여 값이 계속 움직일 때 (d_h 접힘 비수렴 등) 보간 잡음 · 불안정의 몫을 가르기 위해, 같은 격자에서 재하 속도 (판 Mach) 를 바꾼 팔과 셀당 물질점을 바꾼 팔을 함께.
5. **경계 손실 점검**: 판 · 바닥 근처 물질점의 2차 B-spline 지지가 격자 경계 · 판 노드와 어떻게 겹치는지 적고, 해석해 기둥에서 바닥 반력의 치우침 (이 논문 GIMP −5.2 %) 을 잰다.
6. **인용 문장 한정**: "MPM 셀 넘김 잡음" 을 인용할 때는 *"1D 초탄성 막대 · 평균 변형률 2 %"* 를 같이 적는다 · "GIMP 가 셀 넘김 잡음을 없앤다" 대신 *"크게 줄인다 · 틈 · 겹침이 고르지 않게 놓이면 남는다"*.

---

## 11. 논문이 스스로 적은 한계 (원문 근거)

| # | 한계 | 근거 |
|---|---|---|
| 1 | 3D 에서 유한 · 변형 입자의 가중 적분은 입자 영역이 변형 · 회전해 복잡 · 일반적으로 수치 적분 → 시험은 1D | p.484–485 |
| 2 | 폭을 추적하지 않는 근사는 작은 변형에서만 좋다 — 큰 변형에서 틈 · 겹침 · 경계 넘침 → 질량 · 운동량 보존 오차 | p.486 |
| 3 | 더 매끈한 보간도 입자 무질서의 국소 격자 오차를 줄일 뿐 없애지 못한다 (균일 응력 + 분할의 합 = 1 일 때만 0) | p.483 |
| 4 | contiguous GIMP 에도 틈 · 겹침이 고르지 않게 놓이면 가짜 힘이 남는다 | p.488 |
| 5 | 지지가 넓어져 계산량 증가 · 입자 수가 3D 의 계산 · 저장을 좌우 | p.486 · p.491 |
| 6 | finite grid instability 의 나쁜 효과와 셀을 줄이는 좋은 효과를 가를 방법이 없다 | p.493 |
| 7 | 준정적 해는 동역학을 품어 해석 (정적) 해와 늘 조금 다르다 — 가장 고운 격자의 오차 바닥 | p.492 · p.494 |
| 8 | fuzzy particle 은 자세히 안 봤다 · 더 연구 필요 | p.486–487 |
| 9 | 시험의 평균 변형은 작다 (그래도 셀 넘김은 난다) | p.487 |
| 10 | 비탄성 재료에서는 이력 변수가 틀리게 진화하고 발산이 감춰질 수 있다 — 이 논문은 탄성으로만 보였다 (*"as illustrated in this manuscript for elastic materials"*) | p.494 |

---

## 12. 불확실 · PDF 에 없는 것 · 인쇄 어긋남

**A. 논문에 없는 것 ([미확인])** — §3-8 의 목록.  특히 ① §4.4 의 시간 간격 ② Finite GIMP 의 폭 갱신 식 ③ 3D 적분 방법 ④ 1 · 2 p/c MPM 의 셀 0.01 점 (그림에 없음) ⑤ DOI · 접수일 ⑥ 코드 · 계산 시간.

**B. 카드가 그림 · 식에서 역산한 것 (논문의 주장이 아님)** — ① 식 (40) 의 l_p = L/2 = 2차 B-spline (§4-8) ② 가짜 힘 크기 어림 (§3-2 · §4-6) ③ Fig. 4–11 의 판독값 · 기울기 · 바닥 비 ④ Fig. 10 의 "두 점" 의 정체 ⑤ §4.4 Δt 가 10⁻⁴ 보다 작았어야 한다는 것.  전부 [판독 · 카드 산술 · 카드 추론].

**C. 인쇄 어긋남 · 읽을 때 걸리는 곳**
1. p.493 *"may be seen in Fig. 4(c)"* — Fig. 4 에는 (a) · (b) 뿐이다 (불안정하게 자란 해의 예는 Fig. 5a 로 읽힌다 [카드 판독]).
2. 초록 *"capable of eliminating cell crossing noise"* ↔ 본문 *"reduce these artificial force imbalances substantially"* · 잔류 불균형 (p.488) · *"only reduced, not eliminated"* (p.483).
3. 식 (29) 는 Σ_v 없이 인쇄 (∇S_v v_v 의 노드 합이 암시) · 식 (33) 은 적분에 dx 가 빠짐.
4. Fig. 11 캡션 *"five times faster, and 4 times slower"* ↔ 본문 *"five time faster and four times more slowly"* (*time* 오탈자 · p.494 · 렌더로 확인).  ⚠ 글자 층에서 붙어 나오는 낱말 (*contiguousparticle* · *substantiallyperturbs* · *solutionoverlies* · *contributionsto* · 참고문헌 *distributionin*) 은 **인쇄에는 띄어 있다** (렌더 확인) — 글자 층의 산물이지 인쇄 오류가 아니다.
5. p.493 *"Although difficult to discern in Fig 10"* (Fig. 뒤 마침표 빠짐) · p.477 *"all may considered"* (be 빠짐) · p.485 *"the virtue that is computationally efficient"* (it 빠짐) · p.494 *"stand out it this context"* (in → it) · p.493 *"seen in Fig. 4(c)"* (없는 패널 — 위 1) — 다섯 다 렌더로 확인.
6. Fig. 2 는 도식이다 — 그림 경로로 읽으면 곡선의 꺾임점 (−L±l_p · −l_p · L±l_p 눈금 다섯) 은 l_p = 0.20 L 인데 'l_p' 눈금 하나만 0.25 L 자리에 있고, 높이 (세로 '1' 눈금 기준) 는 꼭대기 0.81 · −l_p 에서 0.75 · −L+l_p 에서 0.25 ↔ 식 (40) (l_p = 0.2 L) 이면 0.90 · 0.80 · 0.20 이다 [판독 — 경로 좌표 · 가로 L = 73.74 pt · 세로 1 = 58.99 pt].
7. Fig. 6 · 7 의 '해석해' 가로선은 충격 뒤 값 (−20,000) 만이고 충격면의 위치 · 번짐은 그리지 않았다 — 날카로운 충격이면 현재 좌표의 충격면 = (c − v₀)t = 12.25 · 14.7 · 36.75 · 49.0 (t/파 통과 0.25 · 0.30 · 0.75 · 1 · 벽 = x 0) [카드 산술 — 식 46].
8. 머리글의 쪽 범위 *"pp.477-495"* ↔ 이 논문을 인용한 두 논문의 표기 *"477–96"* · *"477–496"* (후보 표 N-16 · §0-1).

**D. 정본의 다른 카드와의 어긋남 (카드는 고치지 않음 — 카드 문제)**
- `bardenhagen2005_mpm_foam_densification_simulation` L564 (§14 용어집) *"contiguous-particle GIMP — 물질점 영역이 변형을 따라 서로 이어지도록 갱신하는 변종"* — 원문의 contiguous particle GIMP 는 **겹치지 않는 상자 χ_p** 의 선택 (식 36–37) 이고, 폭을 변형에 따라 갱신하는 판은 따로 **'Finite (contiguous particle) GIMP'** 다 (p.489).  예제의 'GIMP' 는 폭을 고정한다 (p.486–487).  다만 뒤 문헌의 이름 (`sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability` §4-2 의 cpGIMP = 직사각형 영역을 diag(F) 로 갱신 · uGIMP = 고정) 과는 그 카드의 정의가 맞는다 → 2005 판이 3D 에서 어느 판을 썼는지는 [미확인] (2005 원문 확인 거리).
- (참고 · 어긋남 아님) `devaucorbeil2020_mpm_after_25_years_review` L36 의 *"C¹ smooth (유한 입자영역) · cell-crossing 완화 · B-spline류와 동류"* 는 contiguous particle GIMP 에 맞고 (C¹ · p.486), 'B-spline 동류' 는 원문에는 없지만 §4-8 의 산술과 맞는다 · `homel2017_…` L238 *"GIMP … 는 유한 영역으로 줄이지만 다 없애지 못하며"* 는 본문 (p.483 · p.488) 과 맞고 초록 표현 (*eliminating*) 과는 다르다 (위 C-2).

---

## 13. 인용 가능 문장 (덱 · 원고용)

- "MPM 의 보간을 변분형 · Petrov–Galerkin 틀로 일반화한 GIMP 에서 MPM 은 입자 특성 함수가 델타인 특수한 경우이고, 입자에 유한한 상자 영역을 주면 C¹ 가중을 얻는다 (Bardenhagen & Kober, CMES 5, 477, 2004 · 식 19–20 · 34 · 40)."
- "MPM 의 셀 넘김 잡음은 텐트 형상 함수의 불연속 기울기 때문에, 균일한 응력의 물질점이 격자에 고르지 않게 놓일 때 노드 양쪽 입자 수 차에 비례하는 가짜 힘으로 생긴다 (같은 문헌 p.488)." — 1D 초탄성 막대 · 평균 변형률 2 % 라는 한정을 붙인다.
- "같은 문헌은 MPM 을 셀 넘김이 없는 무한소 변형 문제에만 쓰라고 권하고, 유한 변형에는 더 매끈한 보간 (contiguous particle GIMP) 이 필요하다고 결론짓는다 (p.494)."
- "셀 크기 수렴 시험에서 MPM 오차는 어느 크기 아래로 조이면 다시 커졌다 — 저속 명시적 PIC 의 finite grid instability 를 셀 넘김 잡음이 키운 것으로 해석됐다 (같은 문헌 Fig. 10 · p.493)." — 오차 노름 · 1D 를 함께.
- "셀당 물질점이 하나일 때 contiguous particle GIMP 의 가중은 2차 B-spline 과 같다 (식 40 에 l_p = L/2 대입 — 이 카드의 산술; 원문은 'quadratic when only one particle is used per cell')." — 산술임을 밝힌다.

## 14. 기법 미니 용어집

- **GIMP (generalized interpolation material point)** — 물질점에 입자 특성 함수 χ_p (공간 부피 분율) 를 주어 격자 ↔ 입자 전달 함수를 일반화한 MPM 계열.  MPM 은 χ_p 가 델타인 특수한 경우.
- **입자 특성 함수 χ_p** — 입자가 차지하는 공간 (부분적일 수 있음) · 현재 위치와 변형 상태의 함수.
- **가중 함수 S̄_vp · 기울기 가중 ∇S̄_vp** — 격자 형상 함수 (기울기) 를 입자 영역에서 χ_p 로 평균한 것 (식 19–20).
- **contiguous particle GIMP** — χ_p = 겹치지 않는 상자 (식 36–37) · 텐트 격자와 함께 C¹ 가중 (식 40).  예제의 'GIMP' = 폭 고정 (l_p(t) = l_p^i).
- **Finite (contiguous particle) GIMP** — 입자 폭을 추적해 분할의 합 = 1 을 유지하는 판 (경계 손실 없음).
- **uGIMP · cpGIMP** (뒤 문헌의 이름 · `sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability`) — uGIMP = 영역 고정 (= 이 논문 예제의 'GIMP') · cpGIMP = 직사각형 영역을 변형 경사의 대각 성분으로 갱신 (1D 에서 'Finite GIMP' 와 같은 갱신 [카드 판독]).
- **fuzzy particle** — 겹치는 χ_p (선형 조각) · 이 논문에서는 계산 안 함.
- **셀 넘김 잡음 (cell crossing noise)** — 물질점이 셀 경계를 넘어 노드 양쪽 등록이 고르지 않을 때 생기는 가짜 노드 힘 · 응력 진동.
- **등록 (registration)** — 물질점이 격자의 어느 셀 · 노드에 걸치는가.
- **분할의 합 = 1 (partition of unity)** — 모든 점에서 기저 함수의 합이 1.
- **Petrov–Galerkin** — 시험 함수와 시행 함수를 다른 기저로 (여기서는 격자 S_v ↔ 입자 χ_p).
- **집중 질량 (lumped mass)** — 대각 질량 행렬 · 여기서는 Petrov–Galerkin 에서 바로 나온다.
- **finite grid instability** — PIC 에서 입자가 격자로 풀 수 없는 짧은 파장의 해 변동을 지녀 생기는 불안정 (Brackbill 1988) · 가중 매끈함 · Mach 수 · 적분법에 달림.
- **CFL 조건** — 명시적 적분의 안정 조건 Δt ≤ L/c.
- **Richtmyer–von Neumann 인공 점성** — 충격을 몇 셀에 번지게 하는 2차 항 (+ 울림을 죽이는 선형 항).
- **파 통과 시간 (wave transit time)** — 막대 길이 ÷ 파속 (= 0.05).
- **p/c** — 셀당 물질점 수 (particles per cell).

## 15. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 · 이유 한 줄 · 정본 카드 없음 확인 = `papers/` 파일 목록 + grep)

- Brackbill, J. U. (1988): The ringing instability in particle–in–cell calculations of low–speed flow. J. Comp. Phys., vol. 75, pp. 469–492. — finite grid instability 의 원전 (가중 매끈함 · Mach 수 · 적분법 의존) · 우리 저속 명시적 압밀 MPM 의 해상도 시험 해석 (질문 f · j).
- Sulsky, D.; Chen, Z.; Schreyer, H. L. (1994): A particle method for history–dependent materials. Comput. Meth. Appl. Mech. Eng., vol. 118, pp. 179–196. — MPM 원전 (이력 의존 재료) · 이 논문이 '정확히 회복' 한다는 식의 출처.
- Sulsky, D.; Zhou, S.-J.; Schreyer, H. L. (1995): Application of a particle–in–cell method to solid mechanics. Comp. Phys. Comm., vol. 87, pp. 236–252. — MPM 원전 둘째.
- Sulsky, D.; Schreyer, H. L. (1996): Axisymmetric form of the material point method with applications to upsetting and Taylor impact problems. Comput. Meth. Appl. Mech. Eng., vol. 139, pp. 409–429. — MPM 으로 금속 원기둥 업세팅 (압축 소성 큰 변형) — 질문 l · 단계 4 의 소성 압축 선례 후보.
- Bardenhagen, S. G.; Brackbill, J. U.; Sulsky, D. (2000): Numerical study of stress distribution in sheared granular material in two dimensions. Phys. Rev. E, vol. 62, pp. 3882–3890. — 2D 입상체 MPM (질문 d · g).

## 16. 관련 카드

- `bardenhagen2005_mpm_foam_densification_simulation` — 이 논문의 contiguous particle GIMP 를 3D 발포체 압축 (공칭 90 %) 에 쓴 후속 · Fig. 1 의 큰 변형률 튐을 이 논문으로 넘김 (§0-1 · §12-D).
- `bardenhagen2000_mpm_granular_multibody_frictional_contact` · `bardenhagen2001_mpm_improved_contact_granular_stress_waves` — 같은 제1 저자의 MPM 다물체 마찰 접촉 (둘 다 이 논문의 참고문헌 목록에 있다 — 본문은 접촉을 다루지 않는다).
- `gritton2017_mpm_chemomechanical_coupling_silicon_anode` — MPM 변종 문헌 [32–37] 을 든 카드 · CPDI 사용 (이 논문 = ref. [37] 은 후보 표의 연결).
- `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` — single-point · GIMP · CPDI 를 나란히 (CPDI = 입자 영역을 변형하는 평행육면체로).
- `sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability` — CPDI 원전 (같은 날 반입) · extension instability 정의 · uGIMP · cpGIMP · CPDI 의 2D 비교 — 이 논문의 GIMP · Finite GIMP 가 그 카드의 uGIMP · cpGIMP 자리 (§0-1).
- `hu2018_mls_mpm_cpic_two_way_rigid_coupling` — 우리 MLS-MPM 이산화 (2차 B-spline · MLS 대용 기울기) 의 원전 — §4-8.
- `devaucorbeil2020_mpm_after_25_years_review` — MPM 변종 표 (standard MPM · GIMP · iMPM/MLS).
- `stomakhin2013_mpm_snow_elastoplastic` · `klar2016_dp_sand_animation` — 우리 탄소성 MPM 계보 (APIC · 2차 B-spline 쪽).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
