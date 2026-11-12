# batch 71 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `brodu2015_multiple_contact_dem_dense_granular` — N. Brodu, J. A. Dijksman, R. P. Behringer, "Multiple-contact discrete-element model for simulating dense granular media", *Phys. Rev. E* **91**, **032201** (2015) · DOI 10.1103/PhysRevE.91.032201 (후보 표 N-30 · 고른 의도 = e · k · 가리킨 카드 = `comparison_vs_ours_DEM` §A · `giannis2021_stress_based_multicontact_dem` · `gonzalez2012_nonlocal_contact_confined_granular`).
접촉 독립 (binary) DEM 에 같은 알의 다른 접촉이 만든 반무한 탄성체 변위 × γ 를 겹침에 더하는 3D 다접촉 DEM (MC-DEM) 을 내고, 자체 하이드로겔 514 알 3D 접촉력 실측 (일축 반복 압축 · 변형률 ≤ 13.4 %) 에 다섯 정식화를 대조한 논문 — 탄성 전용 · 배터리 소재 없음.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (SE 없음 · 기공 · 상대 밀도 보고 0 · 하이드로겔).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] brodu2015_multiple_contact_dem_dense_granular | 가압 · 탈압 가지를 따로 잼 (*"We explicitly separate loading and unloading phases as some hysteresis is observed, which the simulations also reproduce."*) · 판 힘 이력 고리 ÷ 가압 일 = 실험 0.212 · MC-DEM 0.163 · 접촉 독립 0.214 (Δ 1–25 mm · 사다리꼴) · 탈압 끝 (Δ ≈ 1 mm) 판 힘 실험 0.03 N · 모형 0.12–0.18 N | p.3 · 그림 3 · 카드 §3-4 (a) · §14-7 | [인쇄] · [판독] · [카드 산술] | 탄성 알 — 되돌아옴 (두께) · 잔류 변형 값 없음 · 잰 방법 = 스캔마다 판 힘 + 판이 위에 뜬 스캔 10 (p.3) · 측정법 상세는 [8]
- [b] brodu2015_… | 탈압 가지의 미시 비례 곡률: *"the scaling for the simulations presents some curvature in the unloading phase, which does not show up in the experimental data"* · 원인 후보 = Coulomb 마찰 가정 (하이드로겔은 비 Coulomb 가능) | p.5 · 그림 6 · 카드 §4-6 (iv) | [인쇄] | 정량 없음

## c — 항복 · 경도 · 크리프 값과 정의. 일축 항복 세기와 견줄 환산이 카드에 있는가
이 배치에 없음 (소성 · 항복 · 경도 · 크리프 0 — 탄성 하이드로겔 E 23.3 kPa ('best estimate' · p.3 [인쇄]) · 일축 환산 없음).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (한 재료).  곁 정보: 재밍 근처 · 위의 조밀 침대에서 binary 가 *"a good approximation"* 이 아니라는 원문 (*"The situation is different in dense granular packings near or above jamming."* p.1) · 접촉력 분포 p(f) (Δ 18 mm 탈압: 실험 봉우리 0.034 N · 평균 62.6 mN ↔ 접촉 독립 0.009 N · 35.8 mN [판독 · 카드 산술] · 카드 §3-4 (b)).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안 (multi-contact · MDR · EEPA · Thornton-Ning · Storåkers). 대안마다 맞춘 값이 몇 개인가
- [e] brodu2015_multiple_contact_dem_dense_granular | **MC-DEM (변위 기반 다접촉)**: 식 (1) δ_{k→c} = −γ (1+ν)F_k/(2πE d_kc) {(n_k·u_kc)(n_c·u_kc) + (3−4ν) n_k·n_c − (1−2ν)(n_k+u_kc)·n_c/(1+n_k·u_kc)} 를 δ_c 에 더해 F ∝ (δ_c + Σ_k δ_{k→c})^{3/2} · **맞춘 값 1 개 (γ ≈ 1.19)** · 대상 = 최대 압축 판 힘 (Rtop = 1) · 비용 O(ZN) | p.2 · p.3 · p.5 · `eq_01_…png` · 카드 §3-2 · §4-2 | [인쇄] | 분수는 (1−2ν) 항에만 · 이론값 γ = 1 (반무한) · 0.5 (ν 0.5 무한 공간) 밖 · 반복 여부 [미확인] · 탄성 전용
- [e] brodu2015_… | **맞추지 않은 대안 넷의 다입자 성적 (표 I)**: Independent contacts Rtop 0.43 · errf 3.39 N · errZ 0.51 · bhat×10² 7.21 / Point force on sphere (Bondareva) 0.44 · 3.23 · 0.53 · 6.51 / Sphere to sphere (Gonzalez–Cuitiño [14] 식 (3)) 0.70 · 1.82 · 0.34 · 2.57 / Elastic half-space (γ = 1) 0.80 · 1.26 · 0.40 · 1.90 — 맞춘 값 0 개씩 | p.4 표 I · 카드 §3-3 | [인쇄] | 침대 하나 · 변형률 ≤ 13.4 % · 깨지는 범위의 문턱 (몇 % 부터) 은 원문에 없음
- [e] brodu2015_… | 식 (1) 은 E 와 무관 (*"Eq. (1) does not depend on the Young's modulus, which appears both in the force in the numerator and in the denominator"*) → 상대 보정 ∝ γ√(δ/R) · 맞대 접촉 (ν 0.5 · γ 1.19) 이면 δ/R 0.05 · 0.10 · 0.22 에서 4.0 · 5.6 · 8.4 % | p.6 · 카드 §14-2 | [인쇄] · [카드 산술] | 다른 각의 접촉 합 아님 (예시)

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 (지름당 셀 수). 수치 오차를 어떻게 추정했나
이 배치에 없음 (MPM 없음 · FEM 도 일부러 피함 — *"does not require the use of costly finite-element methods"* p.1).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 (실험 · 계산 모두 3D · 2D 에 대한 말 없음).

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 (넘김 없음 · 알 형상 변형을 FEM 대신 해석 선형 탄성으로 DEM 안에서 계산 · p.1).

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] brodu2015_multiple_contact_dem_dense_granular | 저자 한계: *"The full extent of the validity of this model is, however, an open question. In particular, we have only compared our simulations to experiments on soft particles."* · *"it may be that MC-DEM becomes less relevant with harder materials, except perhaps close to jamming"* · *"the empirical parameter γ in Eq. (1) may itself depend on … Z and the packing fraction φ"* | p.6 · `txt_p5_p6_conclusion_validity_soft_particles_gamma_z_phi.png` · 카드 §4-7 | [인쇄] | —
- [j] brodu2015_… | γ 를 경계 조건으로 바꾸는 일은 *"very complicated and any solution would need to be updated at every simulation step"* · ν < 0.5 미해결 · ν = 0 에서 직교 접촉에 잘못된 결합 (카드 산술로 괄호 −0.086 ≠ 0 확인) | p.5 · 카드 §4-7 · §14-3 | [인쇄] · [카드 산술] | —
- [j] brodu2015_… | 카드가 단 한계: 침대 하나 · γ 를 같은 실험에 맞춤 (점검 지표도 같은 자료) · 측정법 · 알 크기 · 판 면적 · 응력 · 반복 여부 [미확인] · 그림 5 의 어느 가지가 가압인지 표지 없음 · γ 와 E 가 판 힘 하나로 안 나뉨 (판 힘 ∝ E) | 카드 §11 · §11-1 · §14-4 | [카드 해석] · [카드 산술] | —

## k — DEM 의 한계
인용 서지: **Brodu, Dijksman & Behringer (2015), Phys. Rev. E 91, 032201 (다접촉 DEM · 하이드로겔 514 알 3D 실측 대조).**
- [k] brodu2015_multiple_contact_dem_dense_granular (Brodu · Dijksman · Behringer · 2015 · Phys. Rev. E 91, 032201) | *"The conventional DEM approach [1] assumes that all contact forces are binary, i.e., independent of forces acting elsewhere on a particle. This is not rigorously true, since the deformation of a particle at a contact generates strain that propagates internally, thereby correlating with deformations at other contacts on the same particle."* · *"The binary assumption avoids computational complexity and makes conventional DEM feasible."* | p.1 §II · `txt_p1_binary_assumption_mean_field_dense_jamming.png` · 카드 §4-6 (i) | [인쇄] | 접촉 독립 가정이 깨지는 밀도 · 겹침 문턱 수치 없음
- [k] brodu2015_… (Brodu et al. 2015 · Phys. Rev. E 91) | *"Without correlation between contacts, this method is similar in spirit to a mean-field approach and provides only a first-order description of the granular assembly properties."* · *"The situation is different in dense granular packings near or above jamming."* | p.1 §II | [인쇄] | —
- [k] brodu2015_… (Brodu et al. 2015 · Phys. Rev. E 91) | *"two key effects that are not taken into account in traditional DEM: (i) shape deformations induce the formation of new contacts; (ii) every contact force is affected by other contact forces in its vicinity"* · *"which the basic DEM model is unable to achieve"* (새 접촉 생성) · *"Unlike the standard DEM, where spheres are not deformable, the radius now effectively changes per contact."* | p.1 §I · p.2–3 | [인쇄] | —
- [k] brodu2015_… (Brodu et al. 2015 · Phys. Rev. E 91) | **수치**: *"The traditional DEM implementation with independent contacts clearly fails to reproduce the measurements."* — 측정 E 의 binary Hertz 판 힘 = 실험의 0.43 (최대 압축 13.4 %) · errf 3.39 N · *"the top force being halved for the same compression level in the classic DEM case"* · 선형 스프링은 *"even less accurate, due to the lack of nonlinear stiffening at the contact level"* (실행 안 함) | p.4 · p.5 · 표 I · `txt_p4_p5_independent_fails_linear_spring_gc_vs_half_space.png` | [인쇄] | ⚠ 방향 = binary 가 **너무 무르다** (탄성 알) — 우리 LPSCl DEM 의 '측정 E 가 너무 단단 → 18× 연화' 와 부호 반대

## l — 소성변형이 왜 어려운가
- [l] brodu2015_multiple_contact_dem_dense_granular (Brodu · Dijksman · Behringer · 2015 · Phys. Rev. E 91, 032201) | **소성은 다루지 않는다** (탄성 알 · 일반 DEM 덧붙임 목록에만 *"Depending on the model, various features are added: plasticity, cohesion, tangential forces"* p.1).  입자 **변형** 을 넣는 우회 = FEM 대신 해석 선형 탄성: *"our method does not involve finite-element method (FEM) calculations. Particle shape deformations are computed with analytic linear elasticity calculations."* · 정확한 경계 조건은 *"very complicated and any solution would need to be updated at every simulation step"* → γ 로 대신 · 관성 행렬은 *"recomputing the inertia matrix of each grain using the surface deformations would be very costly, so we keep the inertia of a sphere"* · **맞춘 값 1 (γ ≈ 1.19 · Rtop = 1 에)** · 검증 = 같은 실험의 errf · errZ · bhat · 비용 = O(ZN) (계산 시간 미기재) · 알 514 개 | p.1 · p.3 · p.5 · `txt_p1_two_key_effects_no_fem_analytic_elasticity.png` · `txt_p2_p3_new_contacts_inertia_cost_ozn.png` · 카드 §4-6 (ii) | [인쇄] | 탄성 전용 — 소성 형상 · 하중 이력 · 탈압 되돌아옴의 어려움에 대한 말은 없다

## m — 받아들일 통찰
- [m] brodu2015_multiple_contact_dem_dense_granular | **'맞춘 지표 1 · 점검 지표 셋' 을 한 표로** (표 I: γ ↔ Rtop · 점검 errf · errZ · bhat) — 보정 보고에서 맞춘 관측량과 점검 관측량을 결과 전에 나누고, 점검이 같은 자료면 그렇다고 적는다 | 단계 0; 조건 R5; 결과 전 대조 항목 | p.3–5 · 카드 §3-3 · §4-5
- [m] brodu2015_… | **측정 해상도 문턱 τ 와 분포 거리 D = −log⟨B⟩** — 실측 (XCT · SEM) 접촉 수와 견줄 때 계산 쪽 약한 접촉을 실측 해상도만큼 지운 뒤 Z 를 비교 (τ = errZ 최소 문턱 = 해상도 어림 4 mN) · 분포는 압축 수준 평균 뒤 로그 | 단계 7; 결과 전 대조 항목 | p.3–4 · `eq_unnumbered_sV_bhattacharyya_distance_in_text.png` · 카드 §3-3
- [m] brodu2015_… | **'한 스칼라 ↔ 한 수' 식별 함정**: 식 (1) 이 E 무관이라 MC-DEM 판 힘 ∝ E (준정적 · 중력 없음) → γ 와 E 추정이 판 힘 하나로 안 나뉜다 (binary 도 E × 2.3 이면 Rtop 1) — 우리 σ_y (MPM) 나 E_eff (DEM) 하나를 기공 하나에 맞출 때도 엉키는 입력을 결과 전에 적는다 · 다접촉 항을 넣을 땐 γ = 0 ≡ binary 영 점검 | 단계 4; U0; 후보 C′ | p.2 · p.6 · 카드 §3-2 · §14-4
- [m] brodu2015_… | **같은 자료 · 같은 E 에서 접촉 표현만 바꾼 판 힘 비** 를 크기 자리표로 — 탄성 조밀 3D 침대 13.4 % 에서 binary ÷ 결합 = 0.43 · 맞추지 않은 결합끼리 0.70 ↔ 0.80 (두 독립 구현 Brodu · Giannis 가 binary 0.43 ↔ 0.44 로 정합) | 단계 3; 후보 D0; 후보 A′ | 표 I · 카드 §7-5

## n — 논문 에이전트 후보
- [n] N. Brodu, J. A. Dijksman, and R. P. Behringer, Spanning the scales of granular materials through microscopic force imaging, Nat. Commun. 6, 6361 (2015). | k · e · U5 — 이 논문 실험의 원전: 3D 접촉력 측정법 (광탄성 여부) · 알 크기 · 판 면적 · 응력 · 자료 공개 여부 = 카드 [미확인] 넷을 닫는다 (카드 §12 · §11-1 · 원문 p.1 · p.3 [8]) | litdb 확인: papers/ ls `brodu*` 없음 · grep "Spanning the scales" · "microscopic force imaging" 0 건 ("6361" 은 다른 카드의 다른 숫자뿐) → 카드 없음
- [n] O. Zhupanska, Contact problem for elastic spheres: Applicability of the Hertz theory to non-small contact areas, Int. J. Eng. Sci. 49, 576 (2011). | e · k — Hertz 를 큰 접촉면적으로 넓힐 때의 한계 (이 논문 'Sphere to sphere' 의 [16]) | litdb 확인: `zhupanska*` 없음 · grep "Zhupanska" = gonzalez2012 언급만 → 카드 없음
- [n] M. Saadatfar et al., Mapping forces in a 3D elastic assembly of grains, J. Mech. Phys. Solids 60, 55 (2012). (서지 일부만 — 원문 목록이 "et al." 로 적음) | U5 · 후보 A′ — 3D 탄성 알 접촉력 실측 (다물체 검증 자료 후보 · 이 논문 [6]) | litdb 확인: `saadatfar*` 없음 · grep "Saadatfar" · "Mapping forces in a 3D" 0 건 → 카드 없음
- [n] L. E. Silbert, D. Ertaş, G. S. Grest, T. C. Halsey, and D. Levine, Geometry of frictionless and frictional sphere packings, Phys. Rev. E 65, 031304 (2002). | 단계 7 · 우리 CN 해석 — 약한 마찰 구가 쉴 때 Z 4–5 (이 논문 [20] · 원문 p.4) | litdb 확인: `silbert*` 없음 · grep "Silbert" = benhadjali2026 · shi2019 언급만 · "frictionless and frictional sphere" 0 건 → 카드 없음
- [n] M. Clusel, E. Corwin, A. O. N. Siemens, and J. Brujić, A "granocentric" model for random packing of jammed emulsions, Nature 460, 611 (2009). | e — γ 를 알 단위 통계 (Z · φ) 의 함수로 바꾸자는 저자 제안의 근거 (이 논문 [22] · 원문 p.5) | litdb 확인: `clusel*` 없음 · grep "Clusel" · "granocentric" 0 건 → 카드 없음

## 카드 문제
- `gonzalez2012_nonlocal_contact_confined_granular` **L607 (· L609)** (가리킨 카드): *"★ 두 계보의 진짜 공통점 = 같은 실험 앵커. 셋 다 Tatara 1989 고무구 … 로 검증한다."* — Brodu 2015 원문 6 쪽에 Tatara · 단일 구 · 고무 0 건.  MC-strain 의 Tatara 대조는 Giannis 2021 의 재구현 (γ 0.55 · giannis2021 L70 · L85) 이다.  고치지 않음.
- `comparison_vs_ours_DEM` **L763–L766** (가리킨 카드 · 후보 표의 L749): *"★ 세 정식화가 같은 실험(Tatara 1989 고무구)을 각자 복원한다"* — 같은 이유로 '각자' 가 원문으로 서지 않는다 (Brodu 는 Tatara 를 쓰지 않음).  *"구분력은 다입자 · 다배치 예측에 있다"* 는 맞고, 그 다입자 시험이 Brodu 표 I 에 있다 (GC 근사 0.70 · γ = 1 0.80 · 맞춤 1.00).  고치지 않음.
- `gonzalez2012_…` **L502 · L592 · L737**: Brodu 의 γ 에 *"이론앵커 있음 (ν→½ 0.5 / ν→0 1)"* — 원문 = γ = 1 은 반무한 (half-space) 해 · γ = 0.5 는 ν = 0.5 의 무한 공간 (full-space) 해 (p.2) · ν = 0 에서는 식 (1) 이 직교 접촉에 결합을 잘못 준다고 저자가 적음 (p.5) · 맞춤 1.19 는 [0.5, 1] 밖.  (giannis2021 L77 · L459 의 같은 말은 [41 Greaves 2011] 출처로 적혀 Giannis 원문의 서술일 수 있다 — Giannis PDF 미열람 [미확인] · Brodu 원문의 말은 아니다.)  고치지 않음.
- `gonzalez2012_…` **L541 · L591** · `comparison_vs_ours_DEM` **L744 · L761** (그리고 후보 표 N-30 '왜' 칸): *"O(C²) + 반복"* — 원문 = **O(ZN)** (Z 알당 접촉 · N 알당 이웃 · p.3) · 'iterat' 0 건.  `giannis2021_…` **L144–L146 · L458** 의 *"원리적으로 반복 … Brodu 는 준정적 가정으로 1회 반복만"* 도 Brodu 원문에 없다 (원문의 '준정적' 은 반발 계수를 1 근처로 고른 이유 한 줄 · p.3).  고치지 않음.
- `giannis2021_…` **L567** · `gonzalez2012_…` **L834** · `comparison_vs_ours_DEM` **L767** (그리고 후보 표 '왜' 칸): *"광탄성 하이드로겔 … 실험 데이터 공개 (딸려 있어)"* — 원문에 'photoelastic' 0 건 · 측정법은 [8] 로 넘김 · 공개한 것은 시뮬레이션 소스 코드 [23] 뿐 (자료 공개 문장 0 건).  [8] 의 실제 측정법은 [미확인].  고치지 않음.
- `giannis2021_…` **L135–L140** (§4.2 식 7 옮김): 분수 막대가 (3 − 4ν)n_k·n_c − (1 − 2ν)(n_k + u_kc)·n_c 전체 위 — Brodu 식 (1) 은 (1 − 2ν) 항의 (n_k + u_kc)·n_c ÷ (1 + n_k·u_kc) 에만 분수 (원문 인쇄 · Boussinesq 반무한 해의 벡터 꼴과 같음 · 카드 §14-1).  Giannis 원문 식 7 의 인쇄는 [미확인] — 카드 옮김의 문제인지 Giannis 원문의 문제인지 가리지 못함.  고치지 않음.
- (관찰 · 문제 아님) `giannis2021_…` L72 · L274 의 514 하이드로겔 MC-strain γ **1.12** (*"[49] 가 제안한 값"*) ↔ 이 논문의 맞춤 **1.19** — 출처가 [49] 로 적혀 있음.  giannis2021 L86 그림 11a 판독값 (고전 245 · γ=1 455 · 실험 555 Pa) 은 이 논문 Rtop 0.43 · 0.80 과 0.44 · 0.82 로 정합 [카드 산술].
- (참고 · 카드 아님) 후보 표 `litdb/_curation/S8_candidates.md` N-30 서지 = 원문과 같음 (제목 · DOI 는 원문에서 채움: *"Multiple-contact discrete-element model for simulating dense granular media"* · 10.1103/PhysRevE.91.032201).  근거 칸의 비교 문서 줄 번호 L743 · L747–753 은 지금 L744 · L757–L767.
- (참고 · 카드 아님) `litdb/figures/_sources.json`: 이 배치의 `extract_figures.py` 가 다른 카드 줄 셋 (choi2018 `figures` 8 → 32 · devasconcelos2019 `pdfs` 목록 다시 씀 · heenan2020 `figures` 16 → 39) 을 바꿨으나 HEAD 값으로 되돌리고 이 카드 줄만 더했다 (batch_69 와 같은 현상).
