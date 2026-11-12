<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 꼴 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md ·
     MPM 이웃 = bardenhagen2005_mpm_foam_densification_simulation.md (이 논문을 'expensive … area of algorithm research' 로 가리킨 카드) ·
     steffen2008_mpm_implementation_choices_gimp_bspline_boundary.md (같은 Uintah 무리 · 명시 MPM 의 오차) · bardenhagen2001_mpm_improved_contact_granular_stress_waves.md
     (ref 14 · 같은 원판 4 개 응력파의 명시 MPM 판) · gritton2017_mpm_chemomechanical_coupling_silicon_anode.md (명시 MPM 의 준정적 장치 = 질량 스케일링).
     쪽 표기 = PDF 쪽 p.1–16 (학술지 쪽 = PDF 쪽 + 1322 · p.1 = 1323 · p.16 = 1338).  보충 자료 (SI) 안내 없음 (16 쪽 글자 층 전수).
     값 표지: [인쇄] = 본문 · 식 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 눈으로 읽은 것 (방법 병기) · [카드 산술] = 인쇄 값으로 이 카드가 계산한 값 (식 병기) ·
     [카드 해석] · [카드 추론] · [추정] = 이 카드의 해석 · [미확인] = 원문 (본문 16 쪽 전수) 에 없음.
     원문 16 쪽은 글자 층 전수 + 3–13 쪽 렌더 (100–200 dpi) + 근거 크롭 렌더 (p.1 · 2 · 14 · 15) 로 읽었고 그리스 문자 · 식은 렌더로 대조했다 (글자 층은 μ · κ · ρ · ν · σ 가 빠진다) · 16 쪽 (참고문헌) 은 글자 층. -->
# 암시적 MPM (격자 변위 증분의 Newton 반복 + 사다리꼴 시간 적분) — 준정적은 질량 행렬 · 관성항을 빼서 · 2D 평면변형률 초탄성 빌릿 50 % 압축이 암시 FE (NIKE3D) 와 가로 변위 2.1 % (정적) · 2.5 % (동적 판 50 cm/s) 로 맞고 명시 MPM 은 같은 동적 문제에서 6.7 % · 최대 유효 응력 14 % 벗어남 · 걸음당 CPU 309 배 ↔ 걸음 70 배 → 이 예에서 암시가 끝까지 ≈4.3 배 더 걸림 [카드 산술] · 셀당 입자 2 × 2 는 30 % 넘어 수렴 실패 · 다물체 접촉은 '격자 두 칸' 떨어져서도 시작 · 소성 · 분말 · 탈압 · DEM 없음 — Guilkey · Weiss (Int. J. Numer. Meth. Engng 2003)

> slug `guilkey2003_implicit_mpm_newton_quasistatic_fem_comparison` · DOI `10.1002/nme.729` · type `MPM (방법 논문 — 암시 MPM · Newton 증분-반복 · 사다리꼴 (요약은 Newmark) 시간 적분 · 준정적 판 = 질량 행렬 · 관성항 제거 · 압축성 neo-Hookean 초탄성 · 2D 평면변형률 빌릿 50 % 압축 ↔ 암시 FE (NIKE3D) · 명시 MPM 대조 · 2D 평면응력 원판 4 개 응력파 ↔ 광탄성 실험 — 분말 · 압밀 · 소성 · 탈압 · DEM 없음)` · PDF `d52f189c-38._Implicit_time_integration_for_the_material_point_method_Quantitative_and_algorithmic_comparisons_with_the_finite_element_method.pdf` · digested `2026-11-12` · status ✅
>
> **저자**: **J. E. Guilkey\*** (교신 · Department of Mechanical Engineering, University of Utah, Salt Lake City · guilkey@humpback.mech.utah.edu) · **J. A. Weiss** (Department of Bioengineering, University of Utah) · *Int. J. Numer. Meth. Engng* **57** (2003) 1323–1338 (16 쪽 · 호 = Wiley 내려받기 줄의 '2003, 9' — 논문 머리글에는 권 · 쪽만) · 접수 2002-01-11 · 수정 2002-07-05 · 승인 2002-10-23 · 연구비 Department of Energy ASCI Initiative (W-7405-ENG-48) · 감사의 글 = U.S. DOE · Center for the Simulation of Accidental Fires and Explosions (같은 번호) · Scott Bardenhagen · Keith Roessig · Joe Foster (응력파 자료) · John Schmidt (선형 풀이기) (p.1 · p.15).  SI 없음.
> **이웃 카드 (링크만)**: [`bardenhagen2005_mpm_foam_densification_simulation`](bardenhagen2005_mpm_foam_densification_simulation.md) (이 논문을 *"expensive … area of algorithm research"* 로 가리킨 카드 · L253 · L299 · L519) · [`steffen2008_mpm_implementation_choices_gimp_bspline_boundary`](steffen2008_mpm_implementation_choices_gimp_bspline_boundary.md) (L102 '암시 판도 있다') · [`bardenhagen2000_mpm_granular_multibody_frictional_contact`](bardenhagen2000_mpm_granular_multibody_frictional_contact.md) (이 논문 ref 3) · [`bardenhagen2001_mpm_improved_contact_granular_stress_waves`](bardenhagen2001_mpm_improved_contact_granular_stress_waves.md) (ref 14 · 같은 원판 응력파의 명시 MPM) · [`nezamabadi2022_mpm_cd_plastic_particle_compaction`](nezamabadi2022_mpm_cd_plastic_particle_compaction.md) · [`nguyen2017_mpm_bpm_deformable_particle_compaction`](nguyen2017_mpm_bpm_deformable_particle_compaction.md) (암시 MPM 으로 소성 입자를 실제로 누른 뒤 선례) · [`hu2018_mls_mpm_cpic_two_way_rigid_coupling`](hu2018_mls_mpm_cpic_two_way_rigid_coupling.md) (우리 명시 MLS-MPM 의 원전) · [`gritton2017_mpm_chemomechanical_coupling_silicon_anode`](gritton2017_mpm_chemomechanical_coupling_silicon_anode.md) (명시 MPM 의 다른 준정적 장치 = 밀도 인위 증가) · [`devaucorbeil2020_mpm_after_25_years_review`](devaucorbeil2020_mpm_after_25_years_review.md).
> **판독 원자료**: 없음 — 축이 있는 그래프가 없다 (그림 2 · 3 = 등고 그림 + 색 막대 0.00–3.17e+07 dyne/cm² [인쇄] · 그림 4 = 광탄성 무늬).  크롭 53 장 (그림 4 (재크롭 1) · 식 29 (번호 식 (1)–(22) 22 + 알고리즘 단계 블록 7) · 근거 문단 20 (재크롭 8)) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: MPM 의 격자 계산이 *"exactly the same as those performed for finite element calculations"* (물질점 = 적분점) 라는 관찰 위에 **격자 변위 증분을 Newton 으로 푸는 암시 MPM** (사다리꼴 시간 적분 · 일관 접선 = 초탄성 탄성 텐서) 을 세우고, 준정적은 **질량 행렬 기여와 관성항을 빼는 것** 으로 얻는다 — 2D 평면변형률 초탄성 빌릿 (40 × 40 cm · 붙은 강체 판 · 50 % 압축) 에서 암시 FE (NIKE3D) 와 **가로 변위 2.1 % (정적) · 2.5 % (동적)** 로 맞고, 같은 동적 문제 (판 50 cm/s = P파 속도의 ≈1.9 % [카드 산술]) 를 **명시 MPM** 으로 풀면 변위 **6.7 %** · 최대 유효 응력 **14 %** 벗어난다 · 대신 암시 걸음은 **70 배 이상 크지만 걸음당 CPU 가 309 배** — 이 예에서는 명시 MPM 이 끝까지 ≈4.3 배 빨랐다 [카드 산술] (저자: *"for a stiffer billet material or a slower platen velocity, IMPM would provide both a more efficient and a more accurate solution"*).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 명시 MPM 을 '천천히' 돌리는 것의 대안 | **암시 MPM** — 선형화한 운동 방정식 KK·du = Fext − Fint − M·a := Q (식 11) 를 Newton 으로 · 사다리꼴 (식 14–15) · 걸음 크기는 CFL 이 아니라 **한 걸음 안의 격자 셀 변형** 이 정한다 (판이 걸음마다 반 칸 · 셀을 짓눌러 뒤집으면 Newton 발산) · 준정적 = Step 2 의 (4/dt²)M 과 Step 3 의 관성 (셋째) 항을 뺌 | [인쇄] p.4–7 · p.12 · p.15 · 식 (11)–(16) |
| ② 그 비용 | 동적 빌릿: 명시 dt ≈ **7 × 10⁻⁵ s** ↔ 암시 dt ≈ **5 × 10⁻³ s** (*"more than 70 times"*) · 걸음당 CPU **0.39 s ↔ 121 s** (SGI Origin 200 · 225 MHz 한 프로세서 · *"a factor of 309"*) → 암시가 이기려면 걸음이 309 배 이상 커야 한다 · 이 예의 끝까지 시간 ≈1,114 s ↔ ≈4,840 s (≈4.3 배) [카드 산술] · NIKE3D (암시 FE) 는 같은 계산에서 *"much shorter"* · 가장 비싼 곳 = 선형 연립 풀이 (CG 가 실패하면 직접 풀이 — *"much more robust … but also much slower"*) | [인쇄] p.7 · p.12 · p.14–15 · [카드 산술] §3-4 |
| ③ FEM 과의 정량 대조 | 정적: 아래 오른쪽 가로 변위 **7.38 (IMPM) ↔ 7.23 cm (FEM) = 2.1 %** · 동적: **7.44 ↔ 7.26 cm = 2.5 %** · 최대 유효 응력 **4.3 %** · 등고선 · 모양 = *"excellent agreement"* (눈) — 대조량은 변위 한 점 + 최대 응력 한 값뿐 · FE 격자 수렴 · 하중–변위 곡선 없음 | [인쇄] p.10–11 · 그림 2 · 3 |
| ④ 명시 MPM 의 오차와 원인 | 동적 빌릿 EMPM: 7.94 cm (IMPM 보다 6.7 % · FE 보다 9.4 % [카드 산술]) · 최대 유효 응력 14 % · 작은 압축에선 잘 맞다가 큰 변형에서 벌어짐 · 원인 둘 = 반복 없는 오차 누적 (dt 를 줄이면 나아짐) + **이웃 셀 입자 수 차에 비례하는 노드 내부력 불균형** [12] — *"for quasi-static solutions this artifact can be so large that the explicit solution can be destroyed"* | [인쇄] p.11–12 · [카드 산술] |
| ⑤ 해상도 규칙 | 셀당 입자 **2 × 2 → 30 % 압축 넘어 수렴 실패 · 3 × 2 · 3 × 3 수렴 · 4 × 4 에서 *"improved noticeably"*** · 입자를 늘려도 연립식 크기는 그대로 (*"only the grid nodes contribute degrees of freedom"*) · 원판: 지름당 50 칸 (암시) ↔ 80 칸 (명시) → *"The contact between adjacent disks is modelled more accurately with increased resolution"* · 격자 수렴 시험 없음 | [인쇄] p.10–11 · p.13 |
| ⑥ 다물체 접촉 | *"Contact occurs when information from the two bodies is interpolated to common nodes. While each field remains independent, this interaction may begin to take place when the particles are as much as two grid cells apart."* → 빌릿과 판 사이에 **틈** · 암시 반복 안에서 접촉을 어떻게 넣었는지 (법칙 · 분리 · 마찰) = [미확인] | [인쇄] p.10 |
| ⑦ 소성 · 큰 변형 | **소성 계산 없음** — 초탄성 (압축성 neo-Hookean) 을 고른 이유 = *"objective and path independent for arbitrarily large deformations"* · 에너지 꼴이면 *"consistent tangent [7] will always be available"* · 대칭 접선 강성 · Step 5 는 *"any relevant history variables"* 를 받는 자리만 둠 | [인쇄] p.6 · p.8 |
| ⑧ 2D / 3D | 계산은 전부 **2D** (빌릿 평면변형률 · 원판 평면응력) — *"for ease of illustration, our IMPM implementation is completely three dimensional"* · FE 는 삼선형 육면체 + 평면변형률 경계 · 2D → 3D 전이 진술 없음 | [인쇄] p.9 · p.10 · p.13 |
| ⑨ 탈압 | **없음** (빌릿은 50 % 까지 누르기만 · 원판은 타격 응력파) | — |
| ⑩ DEM 한계 | **말 없음** (DEM 0 회 · 'discrete' 는 *"The discrete form of the equations of motion"* (p.4) 한 번뿐) — 가까운 말: MPM 은 *"the use of the regular grid eliminates the need for doing costly searches for contact surfaces"* (FE 대비) · 입상체 응력파에서 *"contact between individual grains, which MPM is able to handle with relative ease"* | [인쇄] p.1–2 · p.12 |
| ⑪ 저자가 적은 한계 | NIKE3D 가 더 빠르고 *"will likely continue to be faster even after optimization"* (입자–격자 보간 단계 때문) · 물질점이 최적 적분점이 아니라 Newton 수렴 · 정확도에 영향 · 입자 이동으로 셀당 입자 수가 변함 → 입자 세분 기법 필요 · CG 비효율 (조건수 나쁨) 은 *"not performed a thorough investigation"* | [인쇄] p.7–8 · p.11 · p.14 |

⛔ **한정어 (떼지 말 것)**: ① 재료 = **가상 초탄성** (빌릿 μ 6.0e6 · κ 6.0e7 dyne/cm² (= 0.6 · 6 MPa) · ν 0.45 · ρ 10.0 g/cm³ · 원판 μ 72 · κ 102 GPa · ρ 1900 kg/m³ — *"approximating Plexiglas"*) — LPSCl · NCM 이 아니다 ② **한 덩어리 빌릿 · 붙은 판** — 분말 · 다입자 압밀 · 기공 없음 ③ **2D** 계산뿐 (코드는 3D) ④ **소성 없음** ⑤ 탈압 없음 ⑥ 비용 숫자 = **2003 년 SGI Origin 200 한 프로세서 · 2D · 그 코드** (*"written to demonstrate a new algorithm"*) — 비율 (309) 은 코드 · 크기 · 풀이기에 묶인 값.
⇒ **절대값 전이**: 재료 값 · 변위 · 응력 · CPU 초는 **전이 안 됨**.  옮길 수 있는 것 = **방법과 그 비용 구조** — (a) 준정적을 관성 없이 푸는 식 (식 11 에서 관성 빼기) (b) 암시 걸음 = '반 칸 · 변형 50 %' 규칙 (c) 명시 ↔ 암시 손익분기 = '걸음 크기 비 ≥ 걸음당 비용 비' (d) 명시 MPM 의 준정적 오차 원인 (오차 누적 · 셀 입자 수 불균형) (e) 다물체 접촉 틈 '두 칸'.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-38 의 '왜' 칸)

의도 원문 (`S8_candidates.md` N-38): *"f · l — 준정적을 암시적 MPM 으로 풀고 FEM 과 정량 비교한 논문 · bardenhagen2005 가 "expensive … area of algorithm research" 로 가리킨 자리 (카드 §3-9 · §4-4) → 명시적 풀이를 천천히 돌리는 것의 대안과 그 비용"*

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| (f) MPM 의 접촉 · 다물체 · 해상도 규칙 · 수치 오차 추정 | **채움 (일부)** | 접촉 틈 '두 칸' (p.10) · 셀당 입자 2 × 2 / 3 × 3 / 4 × 4 (p.10–11) · 원판 50 ↔ 80 칸 (p.13) · 오차 추정 = 독립 코드 (NIKE3D) 대조 + 명시 ↔ 암시 대조 (p.10–11) — 격자 수렴 · 해석해 · 오차 노름 **없음** · 암시 반복 안의 접촉 처리 **[미확인]** |
| (l) 소성이 왜 어려운가 | **일부 (간접)** | 소성 계산 **없음** · 초탄성을 고른 이유만 (*"objective and path independent for arbitrarily large deformations"* · 일관 접선 [7] · 대칭 접선 · p.8) · 이력 변수를 받는 자리 (Step 5 · p.6) · *"no assumptions have been made about the material model"* (p.7) — 소성의 어려움 · 비용을 말한 문장 없음 |
| "준정적을 암시적 MPM 으로 풀고" | **채움** | p.7 *"A quasi-static solution is readily obtained by simply eliminating the mass matrix contribution to the total stiffness matrix (Step 2) and removing the inertial (third) term in Step 3"* · §5.1.1 (p.9–11) 정적 빌릿 — 판을 *"quasi-time"* 걸음마다 반 칸 (0.5 cm 셀 [인쇄 '0.5 cm²']) · 50 % 압축 · 2D 평면변형률 · 초탄성 · 4 분의 1 대칭 · 붙은 강체 판 |
| "FEM 과 정량 비교" | **채움 (좁음)** | NIKE3D (암시 FE · 삼선형 육면체 · 요소 0.3–0.5 cm · 자동 걸음) — 정적 가로 변위 **7.38 ↔ 7.23 cm (2.1 %)** (p.10) · 동적 **7.44 ↔ 7.26 cm (2.5 %)** · 최대 유효 응력 **4.3 %** (p.11) · 모양 · 등고 = 눈 (그림 2 · 3).  대조 양이 둘뿐 · FE 해의 격자 수렴 · 오차 막대 · 하중–변위 곡선 없음 · 시간 비교는 *"not presented"* (p.13) |
| "bardenhagen2005 가 'expensive … area of algorithm research' 로 가리킨 자리" | **채움 (GIMP 아님)** | 이 논문 스스로 비용을 적는다: 걸음당 CPU 309 배 (p.12) · 선형 풀이 = *"the most costly part of the algorithm described here"* (p.15) · NIKE3D 가 *"much shorter"* (p.14) · 연구 과제로 남긴 것 = 입자 세분 기법 (p.11) · 격자 재설정 시점 조절 (p.8) · 준-Newton (BFGS) (p.15).  ⚠ 이 논문은 **삼선형 형상 함수의 표준 MPM** (p.2) 이다 — Bardenhagen 2005 의 *"for GIMP methods"* 귀속은 원 논문 (Bardenhagen 2005) 의 범위 표현 (카드는 원문 그대로 옮김 — 카드 문제 아님) |
| "명시적 풀이를 천천히 돌리는 것의 대안" | **채움** | 암시 dt 는 CFL 이 아니라 셀 변형으로 제한 (*"The only time-step restriction for IMPM is related to the magnitude of cell deformation in the computational grid during a single iteration of the Newton method"* p.15) · *"particularly for quasi-static loading scenarios"* (p.15) · 운동 에너지가 변형 에너지보다 작은 문제에서 IMPM 이 더 정확 (p.11 · 문턱 값 없음) |
| "그 비용" | **채움 (동역학 예 한 건)** | dt 7 × 10⁻⁵ ↔ 5 × 10⁻³ s (> 70 배) · 걸음당 0.39 ↔ 121 s (309 배) · 손익분기 = 걸음 309 배 (p.12) — 정적 빌릿 · 원판의 CPU · 메모리 · 반복 수 · 입자 · 노드 수 **[미확인]** |
| 가리킨 카드의 **2 차 인용** — `bardenhagen2005_…` L253 (§3-9) · L299 (§4-4) · L519 (§11 표 4 행) | **맞음 · 숫자 옮김 없음** | L253 = Bardenhagen 2005 원문 문장 인용 (이 논문을 근거 둘 중 하나로) · L299 *"준정적에는 암시적 풀이가 낫지만 비싸고 연구 중"* · L519 *"암시적 풀이는 비싸고 연구 중"* = 이 원문 (p.11–15) 과 같은 방향 (정확도 이득 · 걸음당 비용 · 남은 연구) |
| 다른 카드의 2 차 인용 — `steffen2008_…` L102 *"암시 판도 있다 (Guilkey · Weiss 2003 · …)"* | **맞음** | 이 논문 = 암시 MPM (p.4–7) |
| 후보 표 서지 (*"Guilkey, J.E., Weiss, J.A., 2003. … Int. J. Numer Meth. Eng. 57, 1323–1338."*) | **같음** | 원문 첫 쪽: *Int. J. Numer. Meth. Engng* 2003; 57:1323–1338 (DOI: 10.1002/nme.729) — 제목 대소문자 · 학술지 약어 표기만 다름 · 호 '9' 는 Wiley 내려받기 줄 (본문 머리글 아님) |
| (꼭 뽑을 것) 측정 조건 — 누른 채 / 뺀 뒤 · 압력 · 온도 · 조성 · 진밀도 | **해당 없음** | 계산 논문 · 가상 재료 · 단위계 CGS (dyne/cm²) · 압력 · 기공 · 밀도 기준 개념 없음 · 탈압 없음 |

⇒ **의도 대조 결과: 채움 (f 의 접촉 · 해상도 일부 · 준정적 암시 MPM · FEM 정량 대조 · 비용) / 일부 (l — 소성 계산 없음 · 일관 접선 · 이력 변수 자리만 · FEM 대조는 변위 한 점 + 최대 응력 한 값 · 'GIMP' 아님) / 없음 (분말 · 압밀 · 기공 · 탈압 · DEM).**

---

## 1. 한 줄 요약
명시 MPM 은 CFL (dt < dx/c) 때문에 느린 동역학 · 준정적 문제와 유체–고체 결합에서 걸음이 지나치게 작다 (p.2) — 그래서 MPM 의 격자 계산이 FE 의 조립과 같다는 점 (물질점 = 적분점 · 격자를 걸음마다 원위치 = 메시 엉킴 없음) 을 이용해 **격자 변위 증분을 Newton 으로 푸는 암시 MPM** 을 만들고 (일관 접선 = 압축성 neo-Hookean 의 공간 탄성 텐서 · 사다리꼴 시간 적분), 2D 초탄성 빌릿 50 % 압축 (정적 · 동적) 을 NIKE3D (암시 FE) · 명시 MPM 과, 원판 4 개 응력파를 명시 MPM · 광탄성 실험과 견준다 — 암시는 FE 와 2.1–2.5 % 로 맞고 명시보다 정확하며 잡음이 적지만 걸음당 309 배 비싸, 더 단단한 재료나 더 느린 재하에서만 시간도 이긴다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| J. E. Guilkey\* · J. A. Weiss (University of Utah — 기계공학 · 생체공학) | Int. J. Numer. Meth. Engng 57 (2003) 1323–1338 · 16 쪽 | 10.1002/nme.729 | **없음** — 가상 초탄성 (빌릿: 고무 같은 μ 0.6 · κ 6 MPa · ρ 10 g/cm³ / 원판: μ 72 · κ 102 GPa · ρ 1900 kg/m³) | 방법 (암시 MPM 알고리즘 · 구현) + 수치 대조 (NIKE3D · 명시 MPM) + 다른 논문의 광탄성 실험과 정성 대조 |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 문제 · 재료 · 이산화
| 항목 | 빌릿 (§5.1) | 원판 4 개 (§5.2) | 표지 · 쪽 |
|---|---|---|---|
| 기하 | 40.0 × 40.0 cm · 위아래 판에 **붙음** (*"bonded between two plates"*) · 부풀어 판에 옆으로 닿음 · 4 분의 1 대칭 (빌릿 4 분의 1 = 20 × 20 cm [카드 산술] · 격자는 부풂을 받으려 더 넓다 (그림 1c [판독])) | 지름 1 cm 원판 넷을 한 줄로 · 가장자리끼리 닿음 · 타격 5.6 m/s | [인쇄] p.9 · p.13 |
| 차원 | 2D **평면변형률** (*"for ease of illustration"*) | 2D **평면응력** | [인쇄] p.9 · p.13 |
| 재료 | μ = 6.0e6 · κ = 6.0e7 dyne/cm² (ν = 0.45) · ρ = 10.0 g/cm³ → E = 9κμ/(3κ + μ) = 1.74e7 dyne/cm² = **1.74 MPa** · ν = (3κ − 2μ)/(2(3κ + μ)) = 0.4516 [카드 산술 — 인쇄 0.45 와 맞음] · K/G = 10 | μ = 72 GPa · κ = 102 GPa · ρ = 1900 kg/m³ → *"longitudinal wave speed of 1 cm/µs"* — √((κ + 4μ/3)/ρ) = 1.02 cm/µs [카드 산술 — 맞음] · ν = 0.214 · E = 174.9 GPa [카드 산술] | [인쇄] p.9 · p.13 |
| 구성식 | 압축성 neo-Hookean (식 20) — *"employed in the examples that follow"* | 같음 (그 문장 범위) | [인쇄] p.8 |
| 파속 | c_P = √((κ + 4μ/3)/ρ) = **26.1 m/s** · c_S = √(μ/ρ) = 7.75 m/s · c_P/c_S = 3.37 [카드 산술] | c_L = 1 cm/µs (인쇄) | [카드 산술] · [인쇄] |
| MPM 격자 | *"0.5 cm² cell size"* (넓이 단위로 인쇄 — 반 칸 = 0.25 cm = 50 cm/s × 5 × 10⁻³ s [카드 산술] 이 맞으므로 **변 0.5 cm** 로 읽음) → 빌릿 4 분의 1 한 변 40 칸 [카드 산술] | 지름당 **50 칸** (명시 판 Bardenhagen 은 80 칸) → 칸 0.02 cm = 200 µm [카드 산술] | [인쇄] p.10 · p.13 |
| 셀당 입자 | **4 × 4** (*"to accommodate the large strains"*) — 2D 한 층으로 빌릿 25,600 개 [카드 산술 · 수 미인쇄] | **2 × 2** | [인쇄] p.10 · p.13 |
| 형상 함수 | 삼선형 (*"We assume use of trilinear shape functions"*) | 같음 | [인쇄] p.2 |
| 판 | *"the platen was represented as rigid"* · 그림 1c · 2a 의 위쪽 띠 = 판 물질점 [판독 · 카드 해석] | — (경계 · 벽 [미확인]) | [인쇄] p.9 · [판독] |
| FE (NIKE3D) | 삼선형 육면체 · 요소 ≈0.3–0.5 cm · 자동 걸음 · 경계로 평면변형률 · 모서리 쪽 조밀 (그림 1d [판독]) | — | [인쇄] p.10 |
| 걸음 | 정적: 판이 *"quasi-time"* 걸음마다 **반 칸** · 동적 IMPM: 반 칸 (≈5 × 10⁻³ s) · EMPM: Courant 자동 ≈7 × 10⁻⁵ s | IMPM: 종파가 **반 칸을 지나는 시간** (= 0.01 µs [카드 산술]) | [인쇄] p.10 · p.12 · p.13 |

### 3-2. ★ 정적 빌릿 — IMPM ↔ NIKE3D (§5.1.1 · 그림 2 · p.10)
| 양 | IMPM | FEM | 차 | 표지 |
|---|---|---|---|---|
| 아래 오른쪽 (가운데 높이 · 옆면) 가로 변위 @ 50 % | **7.38 cm** | **7.23 cm** | **2.1 %** (= 0.15/7.23 = 2.07 % [카드 산술]) | [인쇄] p.10 |
| 모양 · von Mises 등고 | *"excellent agreement"* | — | 눈 | [인쇄] p.10 · 그림 2 |
| 색 막대 (두 그림 같은 눈금) | 0.00 – **3.17e+07 dyne/cm²** (= 3.17 MPa = 5.3 μ [카드 산술]) | 같음 | — | [인쇄 · 그림 안 글자] |
- 걸음 수 [카드 산술]: 반 높이 20 cm 의 50 % = 판 이동 10 cm ÷ 반 칸 0.25 cm = **40 걸음** (원문은 걸음 수를 적지 않음).
- 그림 2 [판독 · 눈]: 높은 응력 (빨강) = 가운데 아래 (가운데 높이 · 대칭면 쪽) · 부푼 옆면 = 낮음 (파랑) · MPM (a) 는 판 물질점 띠가 오른쪽 위에 보이고 빌릿 윗면과 판 사이가 벌어져 보인다 (원문이 말한 틈).

### 3-3. ★ 동적 빌릿 — IMPM · EMPM · FEM (§5.1.2 · 그림 3 · p.11–12)
| 양 | IMPM | EMPM | FEM | 표지 |
|---|---|---|---|---|
| 판 속도 | 50 cm/s (셋 같음) | | | [인쇄] p.11 |
| 판 속도 ÷ 파속 | V/c_P = 50/2608 = **0.019** · V/c_S = 0.065 | | | [카드 산술] |
| 아래 오른쪽 가로 변위 | **7.44 cm** | **7.94 cm** (IMPM 보다 *"6.7% greater"*) | **7.26 cm** | [인쇄] p.11 |
| IMPM ↔ FEM | 변위 **2.5 %** · 최대 유효 응력 **4.3 %** | | | [인쇄] p.11 |
| EMPM ↔ IMPM | 최대 유효 응력 **14 %** · 변위 6.7 % | | | [인쇄] p.11 |
| EMPM ↔ FEM | 변위 (7.94 − 7.26)/7.26 = **9.4 %** | | | [카드 산술 — 원문은 이 비를 안 적음] |
| 정적 → 동적 (같은 방법) | 7.38 → 7.44 (**+0.8 %**) | — | 7.23 → 7.26 (**+0.4 %**) | [카드 산술] |
- 원문 해석: *"the comparisons between results for the IMPM and EMPM are much better at smaller amounts of platen compression. With increasing compression and the associated larger deformations experienced by the particles, the explicit results deviated farther from the FEM solution"* · *"Generally, in problems where the kinetic energy is small in comparison to the strain energy, we have found that IMPM yields more accurate results than EMPM"* (p.11 · 에너지 비 숫자 없음).
- 원인 둘 (p.12): ① *"with any explicit method, since there is no iterative procedure to minimize the error in each time step, error builds up over subsequent time steps"* — dt 를 줄이면 나아짐 ② *"as particles move through the computational grid, adjacent cells may contain differing numbers of particles. It has been shown [12] that this can lead to an imbalance in internal force at the nodes that is proportional to the difference in the number of particles in the neighbouring cells … for quasi-static solutions this artifact can be so large that the explicit solution can be destroyed"* — 더 낮은 입자 밀도의 EMPM 은 해를 못 얻음 (어떤 밀도인지 [미확인]) · IMPM 은 3 × 2 · 3 × 3 에서도 수렴.
- ★ **물리 속도 효과 ↔ 명시 수치 오차** [카드 산술]: 같은 판 속도 (V/c_P 0.019) 에서 **관성 (물리) 이 바꾼 변위 = FE 0.4 % · IMPM 0.8 %** 인데 **명시 MPM 의 벗어남 = FE 대비 9.4 %** — 이 문제에서는 명시 수치 오차가 물리 속도 효과보다 한 자릿수 크다.
- 그림 3 [판독 · 눈]: EMPM (b) 은 판과 닿는 윗면 · 오른쪽 위 모서리에 국소 점 (노랑 · 초록) 이 보이고 IMPM (a) · FEM (c) 은 매끈 — 원문 *"noise"* 진술 (원판 절) 과 같은 방향.

### 3-4. ★ 시간 간격 · CPU 비용 (p.12 · p.13 · p.15)
| 항목 | 값 | 표지 |
|---|---|---|
| EMPM dt | ≈ **7 × 10⁻⁵ s** — *"selected automatically each time step based on the Courant stability criterion by monitoring material wave speed and particle velocities"* → Courant 수 C = dt · c_P/Δx = 7e-5 × 2608/0.5 = **0.37** [카드 산술 · Δx = 0.5 cm 로 읽음] | [인쇄] p.12 |
| IMPM dt | ≈ **5 × 10⁻³ s** = 판이 걸음마다 **반 칸** — *"This choice is based on the limitations of deformation of the computational grid during a single iteration of the Newton method. If the platen was allowed to completely crush or invert a cell in a single time step, Newton iterations diverged"* | [인쇄] p.12 |
| dt 비 | *"more than 70 times larger"* (5e-3/7e-5 = 71.4 [카드 산술]) | [인쇄] p.12 |
| 걸음당 CPU | EMPM **0.39 s** · IMPM **121 s** · SGI Origin 200 (225 MHz) 한 프로세서 · *"a factor of 309"* (121/0.39 = 310 [카드 산술 — 0.39 의 반올림 차]) | [인쇄] p.12 |
| 손익분기 | *"to be considered 'efficient' it would be necessary to take implicit time steps at least 309 times larger than the explicit time step"* | [인쇄] p.12 |
| 이 예의 끝까지 시간 | 판 이동 10 cm ÷ 50 cm/s = 0.2 s → EMPM 0.2/7e-5 ≈ 2,857 걸음 × 0.39 s ≈ **1,114 s (≈19 분)** · IMPM 40 걸음 × 121 s = **4,840 s (≈81 분)** → **≈4.3 배** (= 309/71.4) [카드 산술 — 원문은 총 시간을 안 적음] | [카드 산술] |
| 걸음 비의 일반식 | 판 이동량을 같게 두면 N_명시/N_암시 = **1/(2 · Mach · C)** (Mach = V/c_P) — 이 논문 값 (0.0192 · 0.37) 을 넣으면 **71** = 원문 *"more than 70"* 와 맞음 [카드 산술] | [카드 산술] |
| 저자 결론 | *"for a stiffer billet material or a slower platen velocity, IMPM would provide both a more efficient and a more accurate solution"* (명시 dt 는 파속에, 암시 dt 는 셀 변형에 묶이므로) | [인쇄] p.12 |
| 결론 절 일반화 | *"Time steps hundreds of times larger than that dictated by the CFL condition have been used successfully"* — ⚠ 이 논문의 예에서 보인 것은 빌릿 ≈71 배 · 원판 = 반 칸 파 통과 (Courant ≈0.5 꼴) 뿐 (*"a time-step size at least 4 times larger gives results that are practically indiscernible"* 는 비슷한 문제의 미제시 시험) [카드 관찰] | [인쇄] p.13 · p.15 |
| 걸음당 변형 한계 | *"the method reported here is limited by a strain of 50% per time step, that of Cummins and Brackbill is limited to 1% strain per time step"* · Cummins–Brackbill (행렬 없는 Newton–Krylov) 은 명시 dt (CFL 0.25) 의 **10 배** 를 넘으면 해 없음 — 차이의 원인 = *"our approach employs a consistent tangent"* | [인쇄] p.15 |
| 가장 비싼 곳 · 풀이기 | *"the inversion of a large linear system of equations at each iteration, which is the most costly part of the algorithm described here"* · CG 와 직접 풀이 — 걸음마다 CG 먼저 · 실패하면 직접 · 직접은 *"much more robust … but also much slower"* · CG 실패 원인 = *"likely … numerical ill-conditioning in the stiffness matrix"* | [인쇄] p.7 · p.15 |
| NIKE3D 와의 시간 | *"times to solution between the IMPM code and NIKE3D were not presented"* · *"solution times with NIKE3D are much shorter than those with IMPM for the same simulation"* · 최적화 뒤에도 FE 가 빠를 것 (입자–격자 보간 단계) | [인쇄] p.13–14 |
| 다음 비용 절감 | 준-Newton (BFGS · Matthies–Strang) — 큰 선형 풀이 횟수를 줄임 (구현 안 함) | [인쇄] p.15 |

### 3-5. 셀당 입자 수 (ppc) 와 수렴 (p.8 · p.10–12)
| 분포 | 결과 | 표지 |
|---|---|---|
| 2 × 2 | 작은 변형은 좋음 · **30 % 압축 넘어 수렴 실패** (정적 IMPM) | [인쇄] p.10 |
| 3 × 2 · 3 × 3 | 수렴 (정적 · 동적 IMPM) | [인쇄] p.11 · p.12 |
| 4 × 4 | 3 × 3 → 4 × 4 에서 *"quality of the solution improved noticeably"* · 결과 그림 · 수치는 4 × 4 | [인쇄] p.11 |
| 비용 | 입자가 늘면 계산 · 저장이 늘지만 *"the number of equations in the linear system remains unchanged since only the grid nodes contribute degrees of freedom"* → *"the need for particle refinement techniques"* | [인쇄] p.11 |
| 원인 · 처방 | 셀당 물질점 수가 변함 (FE 적분점은 고정 · 최적 위치) → 입자 밀도를 올려 완화 · 격자를 원위치하는 시점을 조절하면 (엉킴 직전까지 그대로) 정확도 개선 가능 (제안) | [인쇄] p.7–8 |

### 3-6. 원판 4 개 응력파 — IMPM · EMPM · 실험 (§5.2 · 그림 4 · p.12–14)
| 항목 | 값 | 표지 |
|---|---|---|
| 비교 대상 | EMPM = Bardenhagen [14] (지름당 80 칸) · 실험 = Roessig [15, 16] 광탄성 | [인쇄] p.12–13 |
| 무늬 합성 | F = cos(2π f_no (σ1 − σ2)/max(σ1 − σ2)) (식 22 · [13]) · **f_no = 7** *"selected to give the best visual match"* | [인쇄] p.13 |
| 프레임 시간 (원판 하나 파 통과 시간으로 무차원) | 실험 **2.6 · 6.6 · 9.2** · EMPM **2.2 · 5.5 · 7.7** · IMPM **1.9 · 4.8 · 6.7** — 짝은 눈으로 · 모든 프레임에 같은 시간 축척 | [인쇄] p.13 · 그림 4 캡션 |
| 시간 축척 | EMPM/실험 = 0.846 · 0.833 · 0.837 · IMPM/실험 = 0.731 · 0.727 · 0.728 [카드 산술] | [카드 산술] |
| 저자 해석 | *"The difference in scaling factors between the explicit and implicit results may be due to the difference in the resolution used for the calculations. The contact between adjacent disks is modelled more accurately with increased resolution."* · 암시가 *"shows less noise"* | [인쇄] p.13 |
| ⚠ 다른 차이 (해석 한정) | 해상도 (50 ↔ 80 칸) 말고도 셀당 입자 (2 × 2 ↔ `bardenhagen2001_…` L124 의 1 개) · 구성식 (이 논문 neo-Hookean ↔ `bardenhagen2001_…` L122 의 선형 hypoelastic) · 시간 적분이 다르다 [카드 관찰 · 다른 카드 대조] | — |
| 걸음 | 반 칸 파 통과 = 0.01 µs → 파 통과당 100 걸음 [카드 산술] · 4 배 큰 걸음 = 비슷한 문제에서 구별 안 됨 (이 문제에선 안 시험) | [인쇄] p.13 · [카드 산술] |
| 실험 원판 실재 | 원문 *"approximating Plexiglas"* — 그러나 1 cm/µs 는 `bardenhagen2001_…` L121 의 실험 종파속 0.27 cm/µs (Marsh 1980) 와 다르다 → 값은 무차원 시간용 단위 [카드 관찰 · 다른 카드 대조] | [인쇄] p.13 |

### 3-7. 원문에 **없는** 값 (정직 목록)
| 찾은 것 | 상태 |
|---|---|
| 수렴 허용치 ε_d · ε_e (식 13) · Newton 반복 수 · 이차 수렴 실측 | **[미확인]** (*"user-selected values"*) |
| 노드 · 자유도 · 입자 수 · 메모리 · 정적 빌릿과 원판의 CPU | **[미확인]** |
| 암시 반복 안의 접촉 처리 (접촉 법칙 · 분리 · 마찰 · 판–빌릿 '붙음' 구현) | **[미확인]** |
| 직접 풀이기의 이름 · CG 전처리 | **[미확인]** |
| FE 해의 격자 수렴 · 요소 수 · NIKE3D 의 접촉 설정 | **[미확인]** |
| 하중–변위 (판 반력) 곡선 · 응력 값 자체 (최대 응력은 % 차만) | **없음** |
| 운동 에너지 ↔ 변형 에너지 비의 값 | **없음** (말만) |
| 소성 · 분말 · 기공 · 탈압 · 3D 계산 · DEM | **없음** |
| 원판 계산의 경계 (벽) · 타격자 표현 | **[미확인]** |

---

## 4. ★ 방법 — 명시 복습 → 암시 알고리즘 → 준정적 → 구성식 → 접촉

### 4-1. 명시 MPM 복습 (§2 · 식 1–10 · Sulsky–Schreyer [2] 꼴)
- 격자 운동 방정식 M_g·a_g = Fext_g − Fint_g (1) · M = 질량 행렬 (*"typically lumped"*).
- P2G: M_i = Σ_p S_ip m_p (2) · v_i = Σ_p S_ip m_p v_p / M_i (3) (*"ensures momentum conservation"*) · Fext_i = Σ_p S_ip Fext_p (4).
- ∇v_p = Σ_i G_ip v_i (5) → 구성식 → σ_p → Fint_i = Σ_p G_ip σ_p v_p (6) (v_p = 입자 부피).
- 격자 속도 v^L_g = v_g + a_g dt (7) · 격자 위치 x^L_g = x_g + v^L_g dt (8) — *"never carried out explicitly"* → 격자는 걸음 끝에 원위치 · 입자 v_p += Σ S_ip a_i dt (9) · x_p += Σ S_ip v^L_i dt (10).
- ⚠ 원문은 (7) 을 *"The backward Euler method"* 라 부르고 *"the conditional stability of the backward Euler integration method"* 라 적는다 (p.3 · p.4) — (7) 은 걸음 처음의 가속도로 가는 전진 (forward) 꼴이고 backward Euler 는 조건 없이 안정한 암시 꼴이라 이름이 맞지 않는다 [카드 관찰 · `steffen2008_…` L102 는 같은 갱신을 Forward-Euler 로 적는다].

### 4-2. 암시 MPM — 선형화 · Newton · 사다리꼴 (§3 · 식 11–16 · 알고리즘 Step 1–8)
| 단계 | 내용 | 표지 |
|---|---|---|
| 착상 | *"calculations on the computational grid are carried out in a manner that is exactly the same as those performed for finite element calculations. The material points essentially function as integration points for the assembly"* · 선형화 식 = 변위 기반 비선형 FE 와 같음 (Gauss 점 대신 물질점) | [인쇄] p.4 |
| 선형화 (11) | KK^{k−1}(t+dt)·du^k = Fext(t+dt) − Fint^{k−1}(t+dt) − M·a^{k−1}(t+dt) := Q^k · 목표 = 잔차 Q 의 노름 최소 | [인쇄] p.4 |
| 갱신 (12) | u^k = u^{k−1} + du^k — **u_g 는 t → t+dt 의 격자 변위** (총 변위 아님 · 총량은 입자 위치 · F_p 에) = 표준 암시 FEA 와의 근본 차이 | [인쇄] p.4 |
| 수렴 (13) | ‖du^k‖/‖du^max‖ < ε_d **그리고** ‖du^k Q^k‖/‖du^0 Q^0‖ < ε_e (ε 값 미인쇄) | [인쇄] p.4–5 |
| 시간 적분 (14)–(16) | *"unconditionally stable trapezoidal rule"* u(t+dt) = dt/2 (v(t) + v(t+dt)) · v(t+dt) = v(t) + dt/2 (a(t) + a(t+dt)) → a^k = 4/dt² u^{k−1} − 4/dt v(t) − a(t) · 요약은 *"Newmark integration"* (사다리꼴 = Newmark 평균 가속도 꼴 · β · γ 숫자는 원문에 없음 [카드 해석]) | [인쇄] p.1 · p.5 |
| 격자 재설정의 결과 | 이전 걸음의 격자 v · a 를 못 쓴다 (빈 셀로 들어간 입자 · 노드 값 없음) → v_g(t) · a_g(t) 는 입자 v_p · a_p 를 식 (3) 꼴로 보간 | [인쇄] p.5 |
| Step 1 | P2G — M_g · v_g(t) · Fext_g(t+dt) (식 2–4) | [인쇄] p.5 |
| Step 2 | u^{k−1} = 0 (k = 1) = 격자 원위치 · 입자는 변형된 자리 → 발자국이 바뀌어 Fint · KK 를 새로: Fint = Σ_e ∫ B_L^T σ_p dv · Kmat = Σ_e ∫ B_L^T D_p B_L dv · Kgeo = Σ_e ∫ B_NL^T σ_p B_NL dv · **KK = Kmat + Kgeo + (4/dt²) M** (B_L · B_NL = 물질점 위치의 삼선형 기울기로 만든 선형 · 비선형 변형률–변위 행렬 · D_p = 공간 탄성 텐서 (Voigt)) | [인쇄] p.5–6 |
| Step 3 | KK du = Fext − Fint − M(4/dt² u − 4/dt v − a) := Q 풀이 (희소 대칭) | [인쇄] p.6 |
| Step 4 | u^k = u^{k−1} + du^k · v^k = (2/dt) u^k − v(t) | [인쇄] p.6 |
| Step 5 | ∇u_p = G_p u_g · **F_p(t+dt) = (∇u_p + 1) F_p(t)** (곱셈 분해) · σ_p 는 F_p 와 *"any relevant history variables"* 로 · D_p 는 σ_p 에서 | [인쇄] p.6 |
| Step 6–7 | 수렴 판정 (13) → F_p · Fint · KK 저장 · a_g(t+dt) (16) → 입자로 u_p · a_p 보간 → x_p += u_p · v_p += ½(a_p(t) + a_p(t+dt)) dt | [인쇄] p.6–7 |
| Step 8 주석 | *"exact linearization"* + 정확한 적분 · 탄성 텐서 + 수렴 반경 안의 dt 면 **이차 수렴** 기대 · 그러나 물질점이 최적 표본 위치가 아니라 적분 정확도로 수렴이 흐려질 수 있음 → 셀 안 입자 분포를 보고 격자 · 입자를 조절하면 나아질 것 | [인쇄] p.7 |
| FE 와의 경계 | *"If the grid was not reset after each time step, the approach would be exactly the same as the FE method. However, it is largely this resetting of the mesh that distinguishes MPM from FEM by avoiding mesh distortion issues"* · 처음 메시 만들기 쉬움 · 엉킴 *"completely avoided"* | [인쇄] p.7 |

### 4-3. 준정적 판 (p.7 · p.9)
- *"A quasi-static solution is readily obtained by simply eliminating the mass matrix contribution to the total stiffness matrix (Step 2) and removing the inertial (third) term in Step 3."* — 정적 빌릿 (§5.1.1) 이 이 판이다 (*"the mass matrix contribution to the stiffness matrix was neglected and the inertial (third) term in Equation (11) was also eliminated"*).
- 하중은 판 변위로 · 판은 *"quasi-time"* 한 걸음에 반 칸.  관성이 없으니 판 속도 (Mach) 라는 손잡이가 **없다** [카드 해석] — 명시 MPM 의 준정적 흉내 (판을 천천히 · `bardenhagen2005_…` §4-4) 나 질량 키우기 (`gritton2017_…`) 와 다른 길.

### 4-4. 구성식 (§4 · 식 17–21)
- 고른 이유: *"Hyperelasticity was chosen as the primary constitutive framework for our MPM code because it is objective and path independent for arbitrarily large deformations and it is readily extended to other material behaviours. Further, constitutive formulations based on energy functionals ensure that a so-called 'consistent tangent' [7] will always be available to ensure optimal convergence behaviour during the Newton iterations, and the resulting elasticity tensor will always lead to a symmetric tangent stiffness matrix."* (p.8).
- W = U(J) + W̃(C̃) (17) — 부피 · 편차 분리 *"ensures that decoupling of the pressure variable from the stress is trivial so that alternate multi-field variational principles can be applied for future analyses of nearly and fully incompressible material behaviour"* (p.8 · 앞으로의 일).
- σ = (2/J) F ∂W/∂C F^T = p1 + (2/J) dev[F̃ ∂W̃/∂C̃ F̃^T] (18) · p = ∂U/∂J · dev[·] = [·] − ⅓([·]:1)1 (19).
- 압축성 neo-Hookean: W̃ = (μ/2)(Ĩ1 − 3) · U = (κ/2)[ln J]² (20) · 공간 탄성 텐서 c = (JU′)′J 1⊗1 − 2JU′ I + 2μ[I − ⅓ 1⊗1] − (2J/3)[s⊗1 + 1⊗s] (21) (s = 편차 Cauchy 응력 · [10]).

### 4-5. 접촉 · 경계 (p.1–2 · p.9–10 · p.12–13)
- 이점: *"having an advantage over traditional finite element (FE) methods in that the use of the regular grid eliminates the need for doing costly searches for contact surfaces [3]"* (p.1–2).
- 틈: *"there is a gap between the particles of the billet and those of the platen in the deformed MPM particle geometry. This is a result of the way contact between bodies is represented with MPM. Contact occurs when information from the two bodies is interpolated to common nodes. While each field remains independent, this interaction may begin to take place when the particles are as much as two grid cells apart."* (p.10) — 물체마다 장을 따로 두는 다물체 접촉 꼴로 읽힌다 [카드 해석 · `bardenhagen2000_…` 의 꼴과 같은 부류].
- 판: 강체 · 빌릿 윗면과 **붙음** · 부푼 옆면이 판에 닿음 (그림 1b) — 그 두 접촉 (붙음 · 닿음) 을 암시 반복에서 어떻게 다뤘는지 **[미확인]**.
- 원판끼리: *"The contact between adjacent disks is modelled more accurately with increased resolution"* (p.13).

### 4-6. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압 (이 묶음의 네 질문)
- **(i) DEM 한계 진술 = 말 없음** — DEM 0 회 · 'discrete' 는 운동 방정식의 *"discrete form"* (p.4) 한 번뿐.  가까운 문장은 FE 대비 MPM 의 이점 둘 (접촉면 탐색 불필요 p.1–2 · 메시 엉킴 회피 p.1 · p.7 · p.15) 과 입상체 응력파 (*"the importance of contact between individual grains, which MPM is able to handle with relative ease"* p.12).
- **(ii) 소성 · 큰 변형을 계산에 넣는 어려움** — 소성은 **넣지 않았다**.  큰 변형 쪽 어려움 (원문): ① FE 메시 엉킴 → MPM 은 격자를 걸음마다 원위치 (p.1 · p.7) ② 물질점 이동 → 셀당 물질점 수 변동 → 적분 정확도 · Newton 수렴 저하 · 명시에선 노드 힘 불균형 (p.7–8 · p.12) ③ 한 걸음 셀 변형이 크면 (셀을 짓눌러 뒤집으면) Newton 발산 → 걸음 = 반 칸 · 변형 50 % (p.12 · p.15) ④ 셀당 입자 2 × 2 는 30 % 넘어 실패 (p.10).  소성으로 갈 길은 구조만: 일관 접선 [7] (Simo–Taylor 1985 · 제목 *"Consistent tangent operators for rate-independent elasto-plasticity"*) · Step 5 의 이력 변수 자리 · 부피 구속의 다장 변분 원리 (p.8 · 앞으로) — 우회 · 비용 · 검증 값 없음.
- **(iii) 차원**: 계산 2D (평면변형률 빌릿 · 평면응력 원판) · *"our IMPM implementation is completely three dimensional"* (p.9) · FE 는 삼선형 육면체로 평면변형률 · 2D → 3D 진술 없음.
- **(iv) 탈압**: 없음.

### 4-7. 기법 미니 용어집
- **명시 (explicit) 시간 적분** = 지금 걸음의 힘으로 다음 상태를 바로 계산 — 계산은 싸지만 dt < dx/c (Courant · CFL) 를 넘으면 불안정.
- **암시 (implicit) 시간 적분** = 다음 걸음의 상태를 미지수로 두고 방정식을 풀어 구함 — 걸음마다 연립식을 푼다 · 무조건 안정 (사다리꼴) · 걸음 크기는 정확도 · 수렴이 정한다.
- **Newton (증분-반복) 풀이** = 비선형 식을 현재 추정에서 선형화 (접선 강성 KK) 해 고치는 일을 잔차가 작아질 때까지 되풀이.
- **일관 접선 (consistent tangent)** = 구성식 갱신 알고리즘을 정확히 미분한 접선 — 이것이 있어야 Newton 이 이차 수렴 (소성은 반환 사상 알고리즘의 미분이 필요 · [7]).
- **재료 강성 · 기하 강성 (Kmat · Kgeo)** = 응력–변형 기울기 몫 · 현재 응력이 회전 · 늘어남에 주는 몫 (큰 변형 FE 의 두 항).
- **사다리꼴 규칙 (trapezoidal rule)** = 걸음 처음 · 끝의 평균 속도 · 가속도로 적분 (Newmark 평균 가속도 꼴).
- **준정적 (quasi-static)** = 관성 (질량 × 가속도) 을 무시한 평형 — 암시에선 그 항을 빼기만 하면 된다.
- **셀당 입자 (ppc · 4 × 4)** = 한 격자 칸 안에 처음 놓는 물질점 수 (2D 방향마다).
- **CG · 직접 풀이** = 반복으로 푸는 공액 기울기 (싸지만 조건수에 약함) ↔ 행렬 분해 (튼튼하지만 비싸고 메모리 큼).
- **NIKE3D** = LLNL 의 비선형 암시 3D FE 코드 (원문 [11]).

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 (a–d) | 빌릿 처음 · 압축 상태 그림 (붙은 판 빗금) · MPM 처음 배치 (4 × 4 입자 · 판 물질점 띠) · FE 처음 메시 (모서리 조밀 · 강체 판) | 단계 2 단위 시험 (빌릿) 의 기하 · 경계 그림 |
| 2 (a · b) | ★ 정적 50 % — MPM (입자) ↔ FEM (메시) · von Mises 0–3.17e+07 dyne/cm² | IMPM ↔ FE 2.1 % 의 모양 대조 · 판–빌릿 틈 |
| 3 (a–c) | ★ 동적 50 % (판 50 cm/s) — IMPM · EMPM · FEM · 같은 색 막대 | 명시 MPM 의 국소 잡음 (윗면 · 모서리) [판독 · 눈] |
| 4 | 원판 4 개 응력파 — 암시 (위) · 명시 (가운데) · 실험 (아래) × 세 시각 | 다물체 접촉 · 해상도 → 파 시간 축척 (0.73 ↔ 0.84 [카드 산술]) |
| 식 크롭 29 장 | `eq_01`–`eq_22` (번호 식마다 한 장 · 명시 MPM (1)–(10) · 선형화 · Newton · 수렴 (11)–(13) · 사다리꼴 (14)–(16) · 구성식 (17)–(21) · 무늬 (22)) + `eq_s2a` · `eq_s2b` · `eq_s3` · `eq_s4` · `eq_s5` · `eq_s7a` · `eq_s7b` (§3.3 알고리즘 단계의 번호 없는 식 블록) | 보고서 MPM 절에 붙일 암시 MPM 지배식 · 알고리즘 |
| 근거 문단 20 장 | `txt_p1_summary_*` · `txt_p2_cfl_*` · `txt_p4_*` (둘) · `txt_p5_*` · `txt_p7_*` (셋) · `txt_p8_*` (둘) · `txt_p9_*` · `txt_p10_*` (둘) · `txt_p11_*` (둘) · `txt_p12_*` · `txt_p13_*` (둘) · `txt_p14_*` · `txt_p15_*` | 원문 인용용 (숫자 · 정의 · 단정의 근거 문단만) |

## 6. Post-processing ★
- **무엇을 (원문)**: 아래 오른쪽 입자 (MPM) · 노드 (FE) 의 가로 변위 · 최대 유효 응력의 % 차 · von Mises 등고 (격자 위) · 무늬 세기 (식 22) · 프레임 시간 (눈 짝짓기 · 같은 시간 축척 제약).
- **안 한 것**: 하중–변위 곡선 · 오차 노름 · 격자 · 입자 수렴 연속 (ppc 는 말로만) · 에너지 시계열 · CPU 의 정적 판 · NIKE3D 시간 · 3D.
- **이 카드의 후처리**: 파속 · Mach · Courant 수 · 걸음 수 · 총 CPU 시간 · 물리 ↔ 수치 변위 차 · 원판 시간 축척 · 단위 환산 (dyne/cm² → MPa) — 전부 [카드 산술] 로 표지 · 그림은 눈으로만 (축 있는 그래프 없음 → digitized.csv 없음).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 가지에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · 다른 카드의 우리 코드 판독 출처를 병기)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 시간 적분 | **암시** (Newton + 사다리꼴) · 준정적 판 = 관성 없음 | **명시** MLS-MPM (Taichi) · dt = 0.4 dx/√M (ρ = 1 규약) + 판 Mach (`--platen-mach`) [다른 카드의 우리 코드 판독 · `gritton2017_…` L538 · M 의 뜻 [미확인] · `steffen2008_…` L303] | 우리는 이 논문이 *"hindered by the explicit time step size restriction"* 라 부른 쪽 · 준정적은 Mach 0.01–0.03 으로 흉내 (CLAUDE.md) |
| 형상 함수 · 셀당 입자 | 삼선형 · 4 × 4 (2D) | 2차 B-spline (MLS) [`hu2018_…`] · 방향당 2 (셀당 8) [`homel2017_…` L499 우리 코드 판독] | 우리 방향당 2 = 이 논문이 30 % 에서 실패한 2 × 2 와 **수는 같다** — 단 형상 함수 (선형 ↔ 2차) · 풀이 (암시 Newton ↔ 명시) 가 달라 그 실패를 옮기지 않는다 [카드 추론] |
| 재료 | 압축성 neo-Hookean (빌릿 K/G = 10 · ν 0.45) | SE: J2 소성 · E 1.53 GPa · ν 0.49 → K 25.5 · G 0.513 GPa · K/G ≈ **50** [카드 산술 · CLAUDE.md 값] · AM = 고정 격자 장애물 (scaffold) | 우리 SE 는 이 빌릿보다 5 배 더 비압축 (K/G) — 부피 잠김 (locking) 위험은 이 논문이 *"future analyses of nearly and fully incompressible"* 로 넘긴 영역 [카드 추론] |
| 하중 | 붙은 강체 판 · 변위 제어 · 50 % | 판 = 노드 속도 처방 (`k * dx > wall_z` · `steffen2008_…` 의 우리 코드 판독) · 응력 정지 (hold · servo) · 300 MPa | 판 표현이 다르다 (이 논문 = 판 물질점 + 다물체 접촉 → 틈 '두 칸' · 우리 = 경계 조건 → 이 틈은 없고 경계 기하 오차 (≤ 3h/2 · `steffen2008_…`) 가 대신) [카드 추론] |
| 대조 기준 | 독립 FE 코드 (NIKE3D) · 같은 문제 | 순수 SE 기공 10–13 % (랩 표준 · 300 MPa) · DEM ↔ MPM (frame [4]) | 우리에게 **같은 문제의 정적 기준 해** (FE · 해석해 · 암시) 가 없다 — 이 논문의 대조 꼴 (정적 · 동적 · 명시 셋을 한 문제에) 이 빠진 칸 |
| 재하율 | 정적 ↔ 동적 (V/c_P 0.019) 차 = FE 0.4 % · IMPM 0.8 % (변위) [카드 산술] · 명시 오차 9.4 % | real_14 Mach 0.0306 → 0.01: 두께 −0.0 % · σ +4.8 % / Lee 침대 Mach 0.03 → 0.01: 기하 같음 · 정착/목표 0.6032 → 0.6577 (+9.0 %) (CLAUDE.md) | 우리 '재하율 효과' 가 물리 (관성) 인지 명시 수치 (오차 누적 · 셀 입자 수 불균형) 인지 가르지 않았다 (§7-4) |
| 3D | 2D 계산 (코드 3D) | 3D 계산 (scaffold · n_grid 192–512) | 차원이 다르다 — 비용 · 메모리는 3D 에서 따로 어림 (§7-3) |
| 소성 · 탈압 | 없음 | J2 소성 · 탈압은 언로딩 키트 (DEM) 쪽 · MPM 제하 없음 | 둘 다 탈압 없음 |

### 7-2. ★ 랩 기준과 나란히 (판정 없이)
| 출처 | 재료 | 조건 | 진밀도 분모 | 기공 |
|---|---|---|---|---|
| **랩 표준** | LPSCl (순수 SE) | 300 MPa | **1.64 g/cm³** (고정) | **10–13 %** |
| 이 논문 | 가상 초탄성 빌릿 (μ 0.6 · κ 6 MPa · ρ 10 g/cm³) | 50 % 압축 · 응력 0–3.17 MPa (색 막대) | 해당 없음 (한 덩어리 연속체) | **해당 없음** (분말 · 기공 없음) |
| 우리 DEM 순수 SE | LPSCl · E_eff 1.35 GPa (18 배 연화) · Heckel P_y 138 MPa | 300 MPa · 가압 중 | 구 부피 합 | ε_union ≈10 % · 겹침 11–12 % (CLAUDE.md 2026-06-06) |
| 우리 MPM 순수 SE | LPSCl · E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 | 300 MPa · 가압 중 | MPM 관례 | 10.0 % — 보정 표적 · 외부 앵커 아님 (`CL-94`) |
- 이 논문은 이 표에 **값을 하나도 넣지 못한다** — 표는 "랩 표준과 다른 문헌 값" 의 자리를 비워 둔다는 기록이다.  이 논문이 주는 것은 수치가 아니라 **계산 방법** (§7-3 · §7-4 · §8).

### 7-3. ★ 명시 '천천히' ↔ 암시 준정적 — 우리 쪽 비용 어림 [카드 산술 · 전부 논문 밖]
- **걸음 수 비** (판 이동량 같게 · 암시 = 이 논문의 '반 칸' 규칙 · 명시 = Courant C · 판 Mach): N_명시/N_암시 = **1/(2 · Mach · C)** — 이 논문 값으로 71 (원문 *"more than 70"* 과 맞음).  우리 Mach 0.03 · C 0.4 (위 7-1 의 dt = 0.4 dx/√M 이 P파 기준이라면 — [미확인]) → **42** · Mach 0.01 → **125**.
- **손익분기** (이 논문의 기준 = 걸음 비 ≥ 걸음당 비용 비): 이 논문 2D 코드의 비용 비 309 를 그대로 두면 우리 판에서 암시는 **2.5 배 (Mach 0.01) – 7.4 배 (Mach 0.03) 느리다** · 암시가 이기는 판 속도는 Mach < 1/(2 · 0.4 · 309) = **0.004** — 지금 쓰는 0.01–0.03 보다 느린 쪽.  ⚠ 비용 비 309 는 2D · 직접 풀이 대비 · 2003 년 값 — 3D · 소성 (Newton 반복 수 ↑) 이면 커지고 행렬 없는 풀이 · GPU 면 작아질 수 있다 [카드 추론].
- **메모리** (3D 직접 풀이의 벽): n_grid 384 = 5.66 × 10⁷ 노드 × 3 = **1.7 × 10⁸ 자유도** · 삼선형 결합 27 노드 × 3 = 81 비영/행 → 1.4 × 10¹⁰ 비영 · CSR (8 B 값 + 4 B 열) ≈ **165 GB** · 2차 B-spline (결합 5³ = 125 노드 → 375 비영/행) 이면 ≈ **760 GB** [카드 산술 · 격자 전체를 자유도로 친 상한 · 물질 없는 노드를 빼면 줄어든다] — 우리 GPU (V100 32 GB · A6000 48 GB) 에 강성 행렬이 안 들어간다.  행렬 없는 Newton–Krylov (Cummins–Brackbill) 은 이 논문 보고로 *"time steps greater than 10 times the explicit time step"* 에서 해가 없었다 (p.15).
- ⇒ **우리 3D 압밀 (scaffold) 의 지금 크기 · 판 Mach 에서 '암시로 바꾸면 빨라진다' 는 이 논문 자료로 서지 않는다** [카드 추론].  암시가 값을 하는 자리는 (a) 관성 없는 **기준 해** (작은 2D · 단위 시험 · U1 · 단계 4 대조) (b) 단단한 AM 이 물질로 들어와 명시 dt 가 AM 파속에 묶일 때 (후보 A · A′ · CLAUDE.md '③ AM-as-material CFL/OOM blow-up' 의 CFL 쪽 — OOM 쪽은 행렬 저장으로 더 나빠진다).

### 7-4. ★ 물리 속도 효과 ↔ 명시 수치 오차 — 우리 '재하율' 읽기에 주는 경고
- 이 논문 빌릿 (V/c_P = 0.019 · 우리 Mach 0.01–0.03 대와 같은 자릿수): 같은 동역학 문제의 **정적 → 동적 변위 차 = FE 0.4 % · IMPM 0.8 %** (물리 관성) ↔ **명시 MPM 의 벗어남 = FE 대비 9.4 % · IMPM 대비 6.7 % · 최대 응력 14 %** (수치) [카드 산술 · 인쇄 p.10–11].
- 우리 CLAUDE.md 는 real_14 의 Mach 0.0306 → 0.01 σ +4.8 % 를 *"느릴수록 σ↑ = 관성이 응력을 낮추고 있었다"* 로, Lee 침대의 Mach 0.03 → 0.01 정착/목표 +9.0 % 를 *"느린 플래튼이 정착응력을 더 많이 남긴다"* 로 읽는다.  이 논문은 같은 Mach 대에서 **명시 수치 오차 (오차 누적 · 셀 입자 수 불균형) 가 물리 관성보다 한 자릿수 클 수 있다** 는 사례다 — 우리 변화량에서 물리 몫과 수치 몫을 가르는 기준 해가 아직 없다 [카드 추론].  ⚠ 형상 함수 (이 논문 선형 → 셀 넘김 잡음 큼 · 우리 2차 B-spline → 작음 · `bardenhagen2004_…` · `steffen2008_…`) · 재료 (소성) 가 달라 크기는 옮기지 않는다.
- 가르는 법 (제안 · 결과 전 등록): 같은 시험 (U1 빌릿 또는 SE 입자 하나) 을 우리 명시 MPM 으로 Mach 0.03 · 0.01 · 0.003 에 돌리고 **관성 없는 기준 해** (정적 FE · 해석해 · 작은 암시) 와 견준다 — Mach → 0 의 극한이 기준 해에 붙으면 물리, 안 붙으면 수치.

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: MPM (연속체 · 큰 변형) 의 **풀이 방법** 한 갈래 (암시 · 준정적) 와 그 비용 · FE 와의 관계 (*"exactly the same as the FE method"* if no reset).
- **없는 것**: 입자 접촉망 · 분말 · 기공 · 소성 · 압밀 실험 대조.  ⇒ MPM (역학) 쪽 **도구 상자** 의 칸 하나 — 수송 (DEM 접촉망 · STEP3) 쪽에는 주는 것이 없다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | (1) 다물체 장 접촉의 **틈 '두 칸까지'** (p.10) → 물체 (입자) 마다 장을 두는 MPM 에서 물질점 위치로 센 기공에는 **수치 틈 (≤ 2Δx × 접촉 면적)** 이 섞일 수 있다 — 연산자 등록에 '물체 사이 틈 ≤ 2Δx 를 기공으로 세는가' 칸 [카드 추론] (2) 원판 대조는 **무늬 수 f_no = 7 을 '가장 잘 보이게'** 고르고 프레임을 **눈으로** 짝지었다 (p.13) — 대조의 자유 손잡이 둘 → 견줄 양 · 방법을 결과 전에 못 박는 이유의 원문 사례 | 기공 · 밀도 값 없음 |
| **단계 1** (3D 메모리 · 장 수) | (1) 암시 = **격자 노드만 자유도** (*"only the grid nodes contribute degrees of freedom"* p.11) — 셀당 입자를 늘려도 연립식 크기 불변 (2) 대신 전역 강성 행렬 — 우리 3D 크기 어림 1.7 × 10⁸ 자유도 · ≈165 GB (삼선형) · ≈760 GB (2차 B-spline) [카드 산술 · §7-3] (3) 입자마다 속도장 (A′) 이면 자유도가 장 수만큼 곱해진다 [카드 추론] | 메모리 · 시간 측정 없음 · 3D 계산 없음 |
| **단계 2** (2D MPM 코드 · 단위 시험) | ★ **빌릿 시험 = 2D 평면변형률 단위 시험 후보** — 40 × 40 cm · 4 분의 1 대칭 · μ 6.0e6 · κ 6.0e7 dyne/cm² · ρ 10 g/cm³ · 압축성 neo-Hookean (식 20) · 붙은 강체 판 · 50 % · 비교값 FE **7.23 cm (정적) · 7.26 cm (동적 50 cm/s)** · 색 막대 최대 3.17e+07 dyne/cm² — 우리 코드 (명시) 의 Mach 사다리를 이 FE 값에 견주면 §7-4 의 물리 · 수치 가르기가 그대로 된다 · 식 (1)–(16) · Step 1–8 = 암시 판 구현 체크리스트 | FE 기준의 격자 수렴 없음 (요소 0.3–0.5 cm 하나) · 판–빌릿 '붙음' · 옆면 접촉 처리 [미확인] · 하중–변위 곡선 없음 · 우리 SE (J2) 와 재료 다름 |
| **단계 3** (2D 접촉 표현 비교) | 다물체 장 접촉의 틈 (두 칸) · 원판 4 개: 해상도 (50 ↔ 80 칸) · 셀당 입자 · 구성식이 다르면 파 시간 축척이 0.73 ↔ 0.84 로 달라짐 [카드 산술] · *"The contact between adjacent disks is modelled more accurately with increased resolution"* — 접촉 표현 · 해상도가 결과 양을 바꾼 사례 | 한 속도장 ↔ 입자별 장 대조 없음 · 누르는 힘 비교 없음 · 마찰 · 분리 규칙 미기술 |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 관성 없는 **기준 해** 를 만드는 법 (식 11 에서 질량 · 관성항 빼기 · 판을 걸음마다 반 칸) → 우리 판 Mach 의존 (real_14 σ +4.8 % · Lee 침대 정착/목표 +9 %) 을 물리 · 수치로 가를 기준 (§7-4) · σ_y 를 맞추기 전에 Mach → 0 극한이 기준 해에 붙는지 보는 순서 [카드 추론] | 소성 · 분말 · 3D · 기공 · 실험 앵커 없음 |
| **단계 5** (3D 복합 압밀) | 암시 dt 는 *"magnitude of cell deformation"* 에만 묶임 (p.15) → AM (E ≈140 GPa) 을 움직이는 물질로 넣으면 명시 dt 가 AM 파속에 묶이는 문제의 해법 쪽 · 저자: 더 단단한 재료일수록 암시가 유리 (p.12) [카드 추론] | 두 강성 물질 · 하중 분담 계산 없음 · 메모리 벽 (§7-3) |
| **단계 6** (탈압 · 되돌아옴) | 없음 — 정적 Newton 판은 하중 단계를 거꾸로 돌릴 수 있는 꼴 (식 11 의 관성 뺀 판) 이지만 원문은 하지 않았다 [카드 추론] | 탈압 · 분리 · 잔류 변형 없음 |
| **단계 7** (형상 · 피복 · 수송) | 없음 | — |
| **후보 D0** (지금 DEM) | 없음 (DEM 언급 0) | — |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 강체 판 = 물질점 띠 + 다물체 장 접촉 → 틈 '두 칸' (p.10) · 판–빌릿 '붙음' (*"bonded"*) — 우리 판은 노드 속도 처방이라 이 틈은 없다 (대신 경계 기하 오차 · `steffen2008_…`) [카드 추론] | 미끄럼 · 분리 법칙 · 암시 안 접촉 처리 [미확인] |
| **후보 A** (MPM 강체 AM · SE 한 속도장) | 강체를 MPM 안에 두는 한 꼴 (판 = 강체) · 암시 = CFL 탈출 → AM 을 움직일 때의 dt 문제 쪽 해법 후보 · 단 CLAUDE.md 의 'AM-as-material CFL/OOM' 가운데 **OOM 은 더 나빠진다** (강성 행렬) [카드 추론] | 강체 운동 방정식 · 결합 방법 미기술 |
| **후보 A′** (입자마다 속도장 · 다물체 마찰 접촉) | *"While each field remains independent, this interaction may begin to take place when the particles are as much as two grid cells apart"* → 입자마다 장을 두면 SE–SE 사이에도 같은 틈 → 충전이 성기게 보일 수 있다 (기공 과대) — 단계 3 대조에 '틈 / 기공 차' 를 결과 전 항목으로 [카드 추론] · 원판 응력파 = 다물체 접촉의 실험 대조 꼴 | 암시 반복 안의 접촉 [미확인] · 마찰 · 분리 없음 |
| **후보 B** (입자마다 FE + 접촉) | ★ *"If the grid was not reset after each time step, the approach would be exactly the same as the FE method"* (p.7) · NIKE3D 가 같은 계산에서 *"much shorter"* · *"The implicit FEM will likely continue to be faster even after optimization"* (p.14) · MPM 의 이점 = *"avoiding mesh entanglement … superior choice for certain problems that demonstrate extreme deformation and contact"* (p.15) → **B ↔ A′ 를 가르는 기준 = 입자 변형이 메시를 엉키게 할 만큼 큰가** (안 엉키면 FE 가 빠르다 — 저자 말) [카드 추론] | 다입자 FE 계산 · 엉킴 문턱 값 없음 |
| **후보 C · C′** (MDR · 항복 캡 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀 · 캡 · Heckel) | 없음 — 암시 정적 Newton 풀이는 연속체 압밀 FE (캡 소성) 의 표준 풀이와 같은 부류 [카드 해석] | 분말 구성식 없음 |
| **U0–U6** | **U1** (한 덩어리 큰 압축 · 해상도 = 셀당 입자: 2 × 2 → 30 % 에서 수렴 실패 · 3 × 3 수렴 · 4 × 4 개선) · **U5** (같은 원판 4 개 · 다물체 · 광탄성 대조 — `bardenhagen2001_…` 와 같은 문제의 암시 판) · **U6** 쪽 (셀당 입자 · 격자 50 ↔ 80 칸 — 정식 수렴 시험은 아님) | U0 · U2 · U3 · U4 없음 |
| **R1–R7** | **R2** (미끄럼 · 분리) — 틈 '두 칸' 만 · 법칙 없음 · **R5** (맞추는 값 하나) — 원판 대조에 눈으로 고른 손잡이 둘 (f_no 7 · 시간 축척) → 반면교사 · **R6** — 빌릿 큰 변형 (부풂 · 판에 닿음) 은 초탄성 = 되돌아가는 변형 (영구 형상 변화 아님) | R1 · R3 · R4 · R7 없음 |
| **결과 전 대조 항목** | 빌릿: FE 7.23 (정적) · 7.26 cm (동적) · IMPM 7.38 · 7.44 · EMPM 7.94 cm · 최대 유효 응력 차 IMPM↔FEM 4.3 % · EMPM↔IMPM 14 % (2D · 가상 재료 · 단위 시험 대조용) · 원판 프레임 실험 2.6 · 6.6 · 9.2 / EMPM 2.2 · 5.5 · 7.7 / IMPM 1.9 · 4.8 · 6.7 (정성) | 우리 재료 · 압밀 양과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: 가상 초탄성 (고무 같은 E 1.74 MPa · ρ 10 g/cm³ · K/G 10) ↔ 우리 LPSCl (J2 · K/G ≈50) · NCM · 2D (평면변형률 · 평면응력) ↔ 우리 3D · 한 덩어리 붙은 빌릿 ↔ 분말 침대 · 동역학 · 변위 제어 50 % ↔ 응력 300 MPa · 소성 없음 · 탈압 없음.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **'재하율 효과' 를 관성으로 부르기 전에 정적 기준 해와 견준다** — 이 논문에서 같은 Mach 대 (0.019) 의 물리 속도 효과는 변위 0.4–0.8 %, 명시 MPM 의 수치 벗어남은 9.4 % (§3-3 · §7-4).  우리 Mach 사다리 (0.03 → 0.01: real_14 σ +4.8 % · Lee 침대 정착/목표 +9 %) 를 이 꼴로 다시 읽을 기준 해 (U1 빌릿 FE 7.23 cm 또는 작은 암시 · 해석해) 를 등록한다 (단계 2 · 단계 4).
2. **암시로 바꾸면 빨라진다는 기대를 숫자로 먼저 막는다** — 걸음 수 비 1/(2 · Mach · C) (이 논문 71 재현) ↔ 걸음당 비용 비 (이 논문 309) · 우리 Mach 0.01–0.03 이면 42–125 < 309 · 3D 강성 행렬 ≈165–760 GB (§7-3).  암시는 '기준 해 · 단단한 AM 을 물질로 넣는 경우' 에 쓴다 (단계 1 · 후보 A).
3. **다물체 MPM 의 접촉 틈 '두 칸' 을 기공 연산자 · A′ 대조의 결과 전 항목으로** — 입자마다 장을 두면 SE–SE 사이에 수치 틈이 생겨 기공이 과대해질 수 있다 (단계 0 · 단계 3 · 후보 A′).
4. **셀당 입자 수는 '큰 변형에서의 수렴' 으로 정한다** — 2 × 2 는 30 % 에서 실패 · 4 × 4 에서 개선 (선형 형상 함수 · 암시) · 우리 방향당 2 (2차 B-spline · 명시) 는 SE 가 기공으로 흐르는 국소 큰 변형에서 사다리 (2 · 3 · 4) 로 확인 (U6) [카드 추론].
5. **B ↔ A′ 고르기의 원문 기준** — 격자를 원위치하지 않으면 MPM = FE · 같은 계산에서 FE 가 빠르다 (저자) → 입자별 FE (후보 B) 는 '입자 메시가 엉키지 않는 한' 이 비용상 이긴다 · MPM 은 극단 변형 · 접촉에서 (후보 선택 근거 문장).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "An implicit MPM (Newton iterations on incremental grid displacements with trapezoidal time integration; quasi-static by dropping the mass-matrix and inertial terms) matched an implicit FE code (NIKE3D) within 2.1 % in bulge displacement for a plane-strain hyperelastic billet compressed to 50 % (Guilkey & Weiss, Int. J. Numer. Meth. Engng 57 (2003) 1323–1338)."
- "In the same dynamic billet problem the explicit MPM deviated by 6.7 % in displacement and 14 % in peak effective stress from the implicit solution; implicit time steps were >70× larger but each cost 309× more CPU time (Guilkey & Weiss 2003)."
- 국문: *"명시 MPM 의 준정적 흉내 (판을 천천히) 와 암시 MPM 은 같은 문제에서 걸음 수 70 배 ↔ 걸음당 비용 309 배로 맞바뀐다 — 암시는 더 단단한 재료 · 더 느린 재하에서만 시간도 이긴다 (Guilkey · Weiss 2003)."*
- 국문: *"다물체 MPM 의 접촉은 공통 노드에서 일어나 물질점이 격자 두 칸 떨어져서도 시작될 수 있다 — 물체 사이 틈은 수치 산물이다 (Guilkey · Weiss 2003, p.1332)."*
- 국문 (카드 산술 표지 필수): *"같은 판 속도 (P파의 ≈2 %) 에서 관성이 바꾼 변위는 0.4–0.8 % 인데 명시 MPM 의 벗어남은 9.4 % 였다 (Guilkey · Weiss 2003 의 인쇄 값으로 계산)."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **재료 · 문제 = 가상 초탄성 한 덩어리 2D** — 소성 · 분말 · 압밀 · 기공 · 탈압 · 3D 계산이 없다.  비용 숫자는 그 코드 · 그 기계 (SGI Origin 200 · 2003) 의 값.
2. **'backward Euler'** (p.3 · p.4) — 명시 갱신 (7) 의 이름이 맞지 않는다 (전진 꼴 · `steffen2008_…` L102 는 Forward-Euler).
3. **요약 'Newmark' ↔ 본문 '사다리꼴'** — 같은 계열이지만 Newmark 계수는 인쇄되지 않았다.
4. **'0.5 cm² cell size'** — 길이에 넓이 단위 (반 칸 · dt · 판 속도로 변 0.5 cm 로 읽힌다 [카드 산술]).
5. **p.8 'deviatoric version of the right Cauchy–Green deformation tensor F̃'** — C̃ 자리에 F̃ 가 인쇄됨 · 식 (6) 의 v_p (부피) ↔ 굵은 v_p (속도) 기호 겹침 · G_ip 정의가 식 (3) 뒤 (쓰기 전) 에 나옴.
6. **"hundreds of times larger than … CFL"** (p.15) — 이 논문 예는 빌릿 ≈71 배 · 원판 = 반 칸 파 통과 (Courant ≈0.5 꼴) 뿐 · '4 배 큰 걸음' 은 미제시 시험 [카드 관찰].
7. **FE 대조가 좁다** — 변위 한 점 + 최대 응력 한 값 · FE 격자 수렴 · 오차 막대 없음 · 정적 판 · NIKE3D 의 시간 *"not presented"*.
8. **암시 반복 안의 접촉 처리 · 수렴 허용치 · 반복 수 · 입자 · 노드 수 · 메모리** — 미기술.
9. **원판 대조** — 눈으로 고른 손잡이 둘 (f_no 7 · 프레임 시간 축척) + 해상도 · 셀당 입자 · 구성식이 함께 다르다 → 시간 축척 차를 해상도로 돌린 것은 후보 하나 · *"approximating Plexiglas"* 인데 c_L 1 cm/µs (실험 Plexiglas 0.27 cm/µs · `bardenhagen2001_…` L121) [카드 관찰].
10. **'더 낮은 입자 밀도' 의 EMPM 실패** (p.12) — 어떤 밀도인지 없음.
11. **인용 번호 · 오타**: 본문 *"Matthies and Strang [16]"* ↔ 목록 [17] (목록 [16] = Roessig 외) · ref 14 저자 *"Guilkey JG"* (본인 이니셜 JE) · ref 6 *"Elascitity"* · p.13 *"IMPM time-step size for was chosen"* · p.11 *"The results of these comparison"*.
12. ⚠ 이 카드의 [카드 산술] (파속 · Mach · Courant · 걸음 수 · 총 시간 · 물리 ↔ 수치 비 · 우리 쪽 비용 · 메모리) 은 인쇄 값과 가정 (Δx = 0.5 cm · 4 분의 1 모델의 판 이동 10 cm · 우리 C 0.4) 에서 나온 어림 — 원문 값처럼 인용하지 않는다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 12 | Zhou S. The Numerical Prediction of Material Failure Based on the Material Point Method. PhD Dissertation, Department of Mechanical Engineering, University of New Mexico, 1998. | 명시 MPM 의 '이웃 셀 입자 수 차에 비례하는 노드 내부력 불균형' 의 원전 — 준정적 명시 풀이를 망가뜨리는 기전 (p.12) | 없음 (papers/ ls · grep) |
| 7 | Simo JC, Taylor RL. Consistent tangent operators for rate-independent elasto-plasticity. Computer Methods in Applied Mechanics and Engineering 1985; 48:101–118. | 소성 (J2) 을 암시 Newton 에 넣는 일관 접선의 원전 (p.8 · p.15) — 질문 l | 없음 |
| 9 | Simo JC, Taylor RL, Pister KS. Variational and projection methods for the volume constraint in finite deformation elastoplasticity. Computer Methods in Applied Mechanics and Engineering 1985; 51:177–208. | 부피 · 편차 분리 (식 17) 근거 · 거의 비압축 소성 (우리 SE ν 0.49) 의 부피 구속 | 없음 |
| 16 | Roessig KM, Foster JC, Bardenhagen SG. Dynamic stress chain formation in a two-dimensional particle bed. Experimental Mechanics 2002; 42(3):329–337. | 그림 4 실험 (원판 층 광탄성 · 응력 사슬) 의 출처 — 2D 접촉 표현 대조 (단계 3 · U5) 의 실험 표적 후보 | 없음 |
| 17 | Matthies H, Strang G. The solution of nonlinear finite-element equations. International Journal for Numerical Methods in Engineering 1979; 14:1613–1626. | BFGS — 큰 선형 풀이 횟수를 줄이는 다음 단계 (p.15 · 본문은 [16] 으로 오기) | 없음 |
| 13 | Cummins SJ, Brackbill JU. An implicit particle-in-cell method for granular materials. Journal of Computational Physics 2002; 180:506–548. | 행렬 없는 Newton–Krylov 암시 PIC (≤ 10 배 · 1 % 변형) — 같은 자리 | 후보 표 N-39 |
| 1 · 2 | Sulsky D, Chen Z, Schreyer HL (1994) CMAME 118:179–196 · Sulsky D, Zhou S, Schreyer HL (1995) Comput. Phys. Commun. 87:236–252 | MPM 원전 둘 | 후보 표 N-40 · `wishlist.md` L195 |
| 3 | Bardenhagen SG, Brackbill JU, Sulsky D. The material-point method for granular materials. CMAME 2000; 187:529–541. | 다물체 접촉 (공통 노드 · 장 분리) | `bardenhagen2000_mpm_granular_multibody_frictional_contact` |
| 14 | Bardenhagen SG, Guilkey JG, Roessig KM, Brackbill JU, Witzel WM, Foster JC. … Computer Modeling in Engineering and Sciences 2001; 2:509–522. | 같은 원판 응력파의 명시 MPM (80 칸) | `bardenhagen2001_mpm_improved_contact_granular_stress_waves` |
| 11 | Maker BN, Ferencz RM, Hallquist JO. NIKE3D … LLNL UCRL-MA-105268, 1990. | 대조 FE 코드 설명서 | 없음 (코드 설명서 · 후보 아님) |

---

## [미확인] 목록
- 수렴 허용치 ε_d · ε_e · Newton 반복 수 · 이차 수렴 실측.
- 노드 · 자유도 · 입자 수 · 메모리 · 정적 빌릿과 원판의 CPU 시간 · NIKE3D 시간.
- 암시 반복 안의 접촉 처리 (판–빌릿 '붙음' · 옆면 접촉 · 원판끼리 · 벽) · 마찰 · 분리.
- 직접 풀이기 이름 · CG 전처리 · 실패 판정.
- FE 메시 수렴 · 요소 수 · NIKE3D 접촉 · 경계 설정 · 두께 방향 요소 수.
- '더 낮은 입자 밀도' 로 실패한 EMPM 의 분포 · 원판 경계 · 타격자 표현.
- MPM 격자 크기의 정확한 뜻 ('0.5 cm²' — 이 카드는 변 0.5 cm 로 읽음).
- 우리 쪽: dt = 0.4 dx/√M 의 M 이 P파 계수인지 (Courant 0.4 의 전제).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 서지: 후보 표 메모 (Guilkey, J.E., Weiss, J.A., 2003 · 제목 · Int. J. Numer Meth. Eng. 57, 1323–1338) = 원문 첫 쪽과 같음 (대소문자 · 약어만 다름) · DOI 원문 첫 쪽 · PDF 문서 정보 (Subject 'Numerical Meth Engineering 2003.57:1323-1338') 와 같음 · PDF 문서 정보의 저자 칸은 비어 있음 (첫 쪽에 두 저자).  SI · 부록 안내 없음.
- 숫자: 글자 층 + 렌더로 대조 — 40.0 × 40.0 cm · 6.0e6 · 6.0e7 dyne/cm² · 0.45 · 10.0 g/cm³ · 0.5 cm² · 4X4 · 0.3–0.5 cm · 7.38 · 7.23 cm · 2.1 % · 2X2 · 30 % · 3X2 · 3X3 · 50 cm/s · 4.3 % · 7.44 · 7.26 cm · 2.5 % · 14 % · 7.94 cm · 6.7 % · 7 × 10⁻⁵ s · 5 × 10⁻³ s · 70 · 0.39 s · 225 MHz · 121 s · 309 · 1 cm · 72 GPa · 102 GPa · 1900 kg/m³ · 1 cm/µs · 5.6 m/s · 50 · 80 cells · f_no 7 · 2.6 · 6.6 · 9.2 · 2.2 · 5.5 · 7.7 · 1.9 · 4.8 · 6.7 · 4 times · 20 years · 10 times · CFL 0.25 · 50 % · 1 % · 색 막대 3.17e+07 (그림 2 · 3).
- 'DEM' · 'unload' · 'porosity' · 'friction' · 'slip' · 'separat' · 'lock' 0 회 · 'discrete' 1 회 (*"The discrete form of the equations of motion"* p.4) · 'plastic' 3 회 = 참고문헌 제목뿐 ([7] elasto-plasticity · [9] elastoplasticity · [15] plastic bonded explosives) · 'incompressib' 1 회 (p.8 앞으로의 일) · 'granular' = §5.2 와 참고문헌 제목 (글자 층 검색).
- 그림: 도구 크롭 4 장 (그림 4 는 쪽 머리글이 섞여 재크롭) · 축 있는 그래프 없음 → 판독 원자료 없음.
- 정본 중복 확인: papers/ 목록 (554 장) · DOI 'nme.729' · 제목 'Implicit time integration for the material point' · 'Guilkey' · 'Weiss' grep — 카드 없음 (bardenhagen2005 L253 · steffen2008 L102 인용만).

## 🔗 관련 카드
- 이 논문을 인용한 카드: `bardenhagen2005_mpm_foam_densification_simulation` (L253 · L299 · L519) · `steffen2008_mpm_implementation_choices_gimp_bspline_boundary` (L102).
- 같은 무리 (Utah · Uintah · Guilkey): `bardenhagen2001_mpm_improved_contact_granular_stress_waves` (이 논문 ref 14) · `steffen2008_mpm_implementation_choices_gimp_bspline_boundary` · `nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions` · `gritton2017_mpm_chemomechanical_coupling_silicon_anode` · `bardenhagen2005_mpm_foam_densification_simulation`.
- MPM 접촉 · 다물체: `bardenhagen2000_mpm_granular_multibody_frictional_contact` (ref 3) · `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` · `hu2018_mls_mpm_cpic_two_way_rigid_coupling`.
- 암시 MPM 으로 소성 입자를 누른 뒤 선례: `nezamabadi2022_mpm_cd_plastic_particle_compaction` · `nguyen2017_mpm_bpm_deformable_particle_compaction`.
- 셀 넘김 · 보간 오차: `bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing` · `sadeghirad2011_mpm_cpdi_convected_particle_domain_extension_instability` · `steffen2008_mpm_implementation_choices_gimp_bspline_boundary`.
- 총설: `devaucorbeil2020_mpm_after_25_years_review`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
