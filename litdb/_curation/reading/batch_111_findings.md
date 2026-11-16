# batch 111 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 표 N-72 둘째 · 대피 세션)

대상: `walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem` — O. R. Walton, "Numerical simulation of inclined chute flows of monodisperse, inelastic, frictional spheres", *Mechanics of Materials* **16** (1993) 239–247 (DOI 원문 인쇄 없음 [미확인])
단분산 1 mm 구의 17° 경사면 중력 정상 흐름 3D DEM (Walton–Braun 이력 선형 법선 + 2D 면 증분 접선) — 압밀 · 탈압 · 형상 소성 없음 · 재료 이름 없음 · 실험 없음.
쪽 = 학술지 인쇄 쪽 p.239–247 (PDF 9 쪽 · 스캔) · 판독 원자료 = `litdb/figures/walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem/digitized.csv` (113 행) · 고른 의도 = 후보 D0 (이력 접촉 계보) · '걸쇠 스프링 접촉' (pfeffer2001 L300) → 의도 대조 결과 **일부** (이력 법선 · 증분 접선의 원문 식은 채움 · '걸쇠 스프링' 이름은 원문에 없음 · 값 표는 일부 · 1986 2D 원판이 아니라 그 3D 확장).  첫째 논문 (Walton & Braun 1986) 원문은 보지 못했다 [미확인] (카드 §0-2).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 재료 이름 없는 단분산 1 mm 구 · 중력 흐름 · 압력 없음.  가장 가까운 숫자 = 흐름 속 충전율 0.32–0.745 (깊이 · 높이에 따라 · Fig. 1 [판독] · 카드 §3-4) — 랩 표준 (300 MPa 순수 SE 10–13 % · 1.64 g/cm³) 과 다른 상태 · 다른 재료 (카드 §7-2).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem | 계 단위 탈압 계산은 없다 — 접촉 하나의 제하 가지만: F_N = K₂(α − α₀) · α₀ = *"the relative 'overlap' where the unloading force is set to zero (due to inelastic deformation of the surfaces)"* → 끝까지 풀면 회복 e²α_max · 잔류 (1 − e²)α_max (e 0.85 → 잔류 27.8 %) | 카드 §4-1 · §3-5 · §7-4 · 원문 p.240 (`eq_04`) | [인쇄] 식 · [카드 산술] 잔류 비 | 흐름 논문 · 측정 아님 · 재재하 경로 원문에 없음

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 재료 항복 · 경도 · 크리프 값이 없다.  접촉 법칙에 항복 · 캡이 없고 (선형 이력) 소성은 α₀ (와 접선 γ 1–2 = *"frictional contacts involving plastic deformation in the contact region"*, p.241) 로만 들어간다 — 일축 항복과의 환산 없음.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 한 종류 단분산 입자 · 혼합 · 하중 분담 없음 (정지 = μ 1.0 에서 흐름이 멈춤 [판독 Fig. 2] 은 재밍이 아니라 경사면 마찰 정지).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] walton1993_… | 이 논문의 법칙 = WB 이력 선형 법선 (K₁ 재하 · K₂ 제하 · K₂ > K₁ · e = √(K₁/K₂) 충돌 속도 무관) + 2D 면 증분 접선 (식 (1) K_T = K₀(1 − (T − T*)/(μF_N − T*))^γ 증가 · K₀(1 − (T* − T)/(μF_N + T*))^γ 감소 · γ 1/3 = Mindlin 닮음 · 1–2 = 접촉 소성 닮음) · 맞춘 값 0 개 (e · μ · K 훑기) · 법칙 근거 (실험 · FE) 는 Walton (1992) 로 미룸 | 카드 §4-1 · §4-2 · 원문 p.240–241 · p.244 | [인쇄] | 흐름 · 겹침 ≤5 % 영역 · 큰 변형 영역 검증 없음
- [e] walton1993_… | ★ 강성 (점접촉 법칙의 인공 매개변수) 이 결과를 바꾸는 범위: 무른 구 동적 겹침 ≤5 % of d → 깊은 흐름 (N/σ² > 10) 속도 · 전단층이 바뀜 · 동적 ≈0.5 % 인 얕은 흐름은 둔감 (p.246) · N/σ² 20 에서 K 100 ↔ 1000 속도 비 1.33 [판독 · 카드 산술] | 카드 §3-2 · §3-3 · §7-3 | [인쇄] · [판독] | 흐름 기전 (바닥층 위로 미끄러져 넘기) — 압밀로 크기 전이 없음
- [e] walton1993_… | 선형 극한: γ = 0 이면 접선이 선형 → Cundall–Strack TRUBALL 과 *"essentially identical results"* (Trent and Walton 1987 사신) — 우리 `tangential history` ≈ γ = 0 극한 [카드 추론] | 카드 §4-2 · §4-5 · 원문 p.244 | [인쇄] · [카드 추론] | 대조 근거가 사신 · LIGGGHTS 세부 대조 [미확인]

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 — MPM 없음.  (MPM 판 · 벽 이력 마찰 구현 때 쓸 접선 기억 갱신 순서 9 단계는 m 절.)

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] walton1993_… | *"The propensity to form crystalline regions is much more pronounced in two-dimensions than in three and such crystallizations have often been seen in past simulation calculations (see for example Walton and Braun (1986))"* · 결정 비전단 영역은 같은 크기 · 매끈한 바닥 · 작은 칸 (5 또는 10 입자 폭) 탓에 실험보다 두드러질 것 | 카드 §3-2 · §4-6 (iii) · 원문 p.245 (`txt_p245_crystals_*`) | [인쇄] | 2D 숫자 비교 없음 · 단분산
- [g] walton1993_… | 모델 자체가 2D WB (원판) 의 3D 확장 (p.240) · 검증으로 든 실험은 *"essentially 2-dimensional chute flows (between two vertical walls, one particle diameter apart)"* (Drake 1988; 1992) — 그림 · 숫자 없음 | 카드 §4-4 · §0-2 · 원문 p.240 | [인쇄] | 대조 그림 없음

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 — FE · MPM 없음 (이력 법선이 흉내 내는 FE 계산은 Walton (1992) 로 미룸, p.241).

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] walton1993_… | 계 탈압 계산 없음 · 재재하 경로 · α₀ 다회 갱신 규칙이 원문에 없음 · K 의 정체 (K₁ · K₂ · K₀) · K₀ · γ · Δt 미기재 — 단계 6 에 이 꼴을 쓰려면 재재하 규칙을 우리 덱 (Luding eq 6) 에서 가져와야 | 카드 §3-6 · §4-1 · [미확인] 목록 | [미확인] | —
- [j] walton1993_… | 저자 한계: 결정화 과장 가능 (단분산 · 매끈한 바닥 · 작은 칸) · 실험 (Johnson et al. 1990) 과 정성적으로 다름 · 평판 거칠기 미반영 · *"Further simulations and interpretation of the flows are in progress"* | 카드 §11 · 원문 p.245–246 | [인쇄] | 흐름 맥락

## k — DEM 의 한계 (원문 문장 · 인용 서지 = O. R. Walton, Mech. Mater. 16 (1993) 239–247)
- [k] walton1993_… (Walton 1993, Mech. Mater. 16, 239–247) | ★ *"An unanticipated finding is the pronounced sensitivity of the velocity and character of the deeper flows to the effective stiffness of the nearly-rigid contact normal force model."* — 무른 구 정적 겹침 ≈ *"one half of one percent of a particle diameter"* · 동적 *"up to 5% of a diameter overlap"* · *"Increasing the stiffness by 1 or 2 orders of magnitude significantly increased the depth of the shearing layer and produced lower mean flow velocities for the flows deeper than 10 per unit area"* | 카드 §3-2 · §4-6 (i) · 원문 p.246 (`txt_p246_stiffness_*`) | [인쇄] | 흐름 · 단분산 · 강성 보정값이 물성이 아니라는 직접 고백은 아님 (결과가 인공 강성에 달린다는 관찰)
- [k] walton1993_… (Walton 1993) | *"nearly-rigid particles interacting via contact forces and gravity"* (p.239) · *"The simulation model assumes that the displacements from one time step to the next are relatively small"* (p.241) · 구만 (*"in anticipation of utilizing non-spherical particles in future calculations"*, p.240) | 카드 §4-2 · §4-3 · §4-6 | [인쇄] | —
- [k] walton1993_… (Walton 1993) | 결정 비전단 영역은 *"probably more pronounced than would be typical in a physical test"* — 같은 크기 · 완벽히 매끈한 판 · 작은 칸 · 실험 흐름 (Johnson et al. 1990) 과 *"differ qualitatively"* | 카드 §3-2 · 원문 p.245–246 | [인쇄] | —

## l — 소성변형이 왜 어려운가 · 우회 · 비용 (인용 서지 = O. R. Walton, Mech. Mater. 16 (1993) 239–247)
- [l] walton1993_… (Walton 1993) | 소성을 입자 형상이 아니라 **접촉 법칙 안** 에 넣는 우회: 제하 강성 K₂ > K₁ 이 남기는 α₀ (*"due to inelastic deformation of the surfaces"*) · 에너지 손실 = *"only via displacement-dependent hysteretic loading/unloading paths and sliding friction"* (감쇠 없음) · 접선 γ 1–2 = *"more closely mimics the behavior of frictional contacts involving plastic deformation in the contact region (Drake and Walton, 1992)"* · 맞춘 값 0 (훑기) · 법칙 근거 = *"Experimental evidence for this model, and finite element calculations that this model mimics, are discussed in Walton (1992)"* (이 논문 밖) · 비용 = 입자 63–1000 개 · 시간 · Δt [미확인] | 카드 §4-1 · §4-2 · §4-6 (ii) · 원문 p.239–241 | [인쇄] | 왜 어려운지에 대한 설명은 원문에 없다 (우회만) · 형상 변화 · 부피 보존 흐름 · 이웃 접촉 상호 영향 없음

## m — 받아들일 통찰
- [m] walton1993_… | **U5 기대값** — 이력 선형 법선이면 e = √(K₁/K₂) 가 충돌 속도와 무관 · 접촉 시간 (π/2)√(m*/K₁)(1 + e) · 잔류 α₀ = (1 − e²)α_max [카드 산술] → 우리 덱 k̂₂/k₁ = 5 · 3 · 1.5 (SE–SE · AM–SE · AM–AM) 의 이력 몫 e 0.45 · 0.58 · 0.82 를 두 입자 충돌로 확인 · 자리 = U5 · 후보 D0 · 근거 = 원문 p.240 + `luding2008` §7.1
- [m] walton1993_… | **탈압 회복은 이력 비의 출력** — 접촉 하나 잔류 = (1 − k₁/k₂)δ_max → SE–SE 가 k̂₂ 에 닿으면 80 % 잔류 · 20 % 회복 [카드 산술] · 단계 6 결과 전 등록에 k̂₂/k₁ 를 같이 적고 맞추는 값 (R5) 과 섞지 않는다 · 자리 = 단계 6 · 조건 R4 · R5 · 근거 = 원문 p.240 식 꼴 + 카드 §7-4
- [m] walton1993_… | **강성 보고 의무** — 연화 강성 결과마다 겹침 분포 (평균 · 최대 · 동적) + 강성 ×10 민감도 (원문은 그 둘로 깊은 흐름 결론이 바뀜을 보였다) · 자리 = 후보 D0 · 근거 = 원문 p.246 · Fig. 2
- [m] walton1993_… | **접선 기억 갱신 순서 9 단계** (옛 마찰력 투영 → 크기 보존 → 상대 변위 → 평행 / 수직 분해 → T* 의 법선력 비례 → 식 (1) → 뒤집힘 −T* → 수직 = K₀ → 벡터 합 · μF_N 절단) = 판 · 벽 이력 마찰 구현 점검표 · 자리 = 후보 A′-0 · 단계 2 · 근거 = 원문 p.241 · p.244 (`eq_07`–`eq_18`)

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드 없음 · papers/ ls + grep 확인)
- [n] Walton, O.R. (1992), Numerical simulation of inelastic frictional particle–particle interactions, in: Roco, ed., Particulate Two-Phase Flow, Ch. 25, Butterworth–Heinemann, Boston. | ★ e · l — 이력 법선 (K₁/K₂) 의 실험 근거와 그 법칙이 흉내 내는 FE 계산 (원문 p.241 이 미룬 곳) · '걸쇠 스프링' 이름의 출처일 수도 [추정] | papers/ ls 'walton*' = 이 카드뿐 · grep 'Particulate Two-Phase Flow' = 이 카드뿐 — 카드 없음
- [n] Drake, T.G. and O.R. Walton (1992), Comparison of Experimental and Simulated Grain Flows, J. Appl. Mech., submitted. (서지 일부만 — 출판 권호 없음) | e · l — 접선 γ = 1–2 가 접촉 소성을 닮는다는 근거 · 실험 ↔ 계산 슈트 흐름 대조 | papers/ ls 'drake*' 없음 · grep 'Drake' = 이 카드뿐
- [n] Cundall, P.A. and O.D.L. Strack (1979b), A discrete numerical model for granular assemblies, Geotechnique 29, 47–65. | e · k — D0 계보의 원점 (선형 접촉 · TRUBALL · γ = 0 극한의 대조 대상) | papers/ ls 'cundall*' 없음 · grep 'Geotechnique 29' = 인용 카드 4 장 (morenoatanasio2007 · silbert2001 · stewart2001 · thorntonyin1991) — 카드 없음
- [n] Mindlin, R.D. (1949), Compliance of elastic bodies in contact, J. Appl. Mech., Trans. ASME 16, 259–268. | e — 증분 접선 강성 (식 (1)) 의 원전 | papers/ ls 'mindlin*' 없음 · grep 'Compliance of elastic bodies in contact' = morrissey2013 (인용) — 카드 없음
- (Walton, O.R., and R.L. Braun (1986), J. Rheol. 30 (5), 949–980. — ⛔ 후보 표 N-72 첫째 · 1저자 내려받기 불가로 이미 제외 · 다시 올리지 않는다)

## 카드 문제
- **paulick2015_elastic_particle_properties_dem_review** — L239 (*"① | 1–10 % | … | [25] Walton 1993, §2.1 p.67"*) · L395 (*"유동 패턴 | 경사 슈트, 단분산 비탄성 마찰구 | 오버랩 1–10 % | 영향 없음 | [25] p.67"*) · L552 (*"[25] Walton 1993 — … 'the flow pattern … is not affected by a reduced elasticity as long as the overlap stays within a range of 1–10 %'"*) · L744 · L868 (*"[25] Walton 1993 의 1–10 % (밑변 미명시) 가 이 리뷰 전체의 상한"*) — **Walton 1993 원문 (9 쪽 전수) 에 '1–10 %' · 'not affected' · 'reduced elasticity' 가 없다**.  원문의 겹침 문장은 p.246 하나 — 무른 구 정적 ≈0.5 % · 동적 ≤5 % of d · 깊은 흐름은 강성에 *"pronounced sensitivity"* · 얕은 흐름 (< 5 per σ²) 만 둔감 (반대 방향).  [25] 의 서지는 카드에 없지만 설명 ('경사 슈트, 단분산·비탄성·마찰구') 이 이 논문 제목과 같다.  Paulick 2015 원문이 그렇게 귀속했는지 · 카드 옮김인지는 Paulick PDF 대조 [미확인] — **카드는 고치지 않았다** (관련 카드 절에 원문 카드 링크 한 줄만 더함).  L868 의 '문헌 상한' 논증은 이 귀속에 기대므로 다시 볼 일.
- (카드 문제 아님 · 기록) **pfeffer2001_dry_particle_coating_engineered_particulates** L144 · L284 — 접선 식 감소 가지의 분자 "T − T*" (Pfeffer 원문 인쇄 그대로 옮김 · 그 카드가 *"원 Walton 형과의 대조 [미확인]"* 이라 적음) ↔ Walton 1993 식 (1) 은 **T* − T** → Pfeffer 2001 원문의 옮김 차이 (그 카드의 [미확인] 하나가 풀림) · 같은 줄의 "Mindlin–Deresiewicz 단순형" ↔ Walton 1993 은 Mindlin (1949) 만 인용 · "e = √(K₁/K₂) (속도 무관 가정)" ↔ 원문은 가정이 아니라 법칙이 낳는 성질.  그 밖의 2 차 인용 값 (적재 K₁α · 제하 K₂(α − α₀) · α₀ · γ ≈ 1/3 · T′ = T + K_TΔS · 서지) 은 원문과 같다.
- (일치 · 기록) **silbert2001_chute_flow_bagnold_spring_dashpot_hertz_dem** L494 *"3D chute DEM · 마찰 방향 기억 (D0)"* · L50 *"…as does Walton [23]"* — 원문 (평행 / 수직 분해 · T* 부호 기억, p.244) 과 같다.
