# batch 90 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-13)

대상: `wensrich2012_rolling_friction_shape_contact_eccentricity_dem` — C.M. Wensrich, A. Katterfeld, "Rolling friction as a technique for modelling particle shape in DEM", *Powder Technology* 217 (2012) 409–417 · DOI 10.1016/j.powtec.2011.10.057 (후보 표 N-50 · 가리킨 카드 = `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` L244).
구름마찰로 입자 모양을 대리하는 DEM 기법의 정량 점검 — 접촉 편심 → μ_r 추정 (식 9) + PFC3D 3D 안식각 150 런 (구 + 모델 C 구름마찰 ↔ 이중 · 삼중 점묶음) + 단일 입자 굴림 시험 · 실험 · 압밀 · 소성 · 탈압 없음.
쪽 = 학술지 p.409–417 (PDF p.1–9) · 판독 원자료 = `litdb/figures/wensrich2012_rolling_friction_shape_contact_eccentricity_dem/digitized.csv` (357 행 · Fig 8 · 9 = 벡터 좌표 · Fig 2 · 6 = 래스터 보정).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (SE · 압력 · 기공 0 — 5 mm 일반 구의 중력 안식각 · porosity · density 0 회 · 표 1 의 ρ 2000 은 입자 밀도).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 (탈압 0).  가장 가까운 것은 정지 쪽 함정 하나 — 모델 A 구름 토크의 정지 계 기어감 (아래 j · k).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 (항복 · 경도 0).  ⚠ 모델 C 의 *"elastic–plastic spring dashpot"* (p.410) 의 '소성' 은 **구름 토크가 한계 μ_r R_r F_n 에서 미끄러지는 것** 이지 재료 항복이 아니다 — 일축 항복 세기와 견줄 값 없음.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (단일 성분 · 하중 분담 0).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] wensrich2012_rolling_friction_shape_contact_eccentricity_dem | 큰 변형 범위 = 말 없음.  대신 **구름 저항 모델의 대안 넷 (Ai 분류)** 과 설정: A 일정 토크 (식 1 · 정지 계 기어감) · B 점성 (식 3 · 인쇄 꼴이 토크 × 속도) · C 탄소성 스프링–대시포트 (식 4 · 5) · D 접촉 무관 — 이 논문 = C · 구름 강성 k_r = R_r² k_s (식 7 · 전단과 같은 고유 진동수 → 임계 Δt 불변) · 구름 감쇠 없음 (높은 k_r 이면 전단 감쇠가 진동을 잡는다) · **맞춘 값 0** (설정 규칙뿐) | 카드 §3-2 · p.409–411 · 식 1–8 | [인쇄] | 구름 토크 법칙이지 법선 접촉 (Hertz–Mindlin no-tension) 의 대안 아님
- [e] wensrich2012_rolling_friction_shape_contact_eccentricity_dem | 모양 대리 계수의 기하 추정 μ_r ≈ ⟨e⟩/R_r (식 9) — **맞춘 값 0 (예측)** · AOR 대조 결과 같은 안식각에 드는 μ_r 은 추정의 0.35–0.59 배 (구 μ_r 0.18 줄 8 칸) · 원문 *"approximately half"* · *"by at least a factor of two"* | 카드 §3-4 · §3-7 · p.412 · p.416 · Fig 9 | [인쇄] · [판독 · 벡터] · [카드 산술] | 5 mm 중력 더미 · 겹친 구가 기준

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 0).  (DEM 수치 쪽만: Δt = PFC 임계 Δt 의 25 % · 보통 3–4 μs · 반복 2 런 · 수렴 시험 0 — 카드 §3-1.)

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] wensrich2012_rolling_friction_shape_contact_eccentricity_dem | 편심 해석은 2D 타원에서 시작해 *"The previous analysis applies only to the two dimensional case, however we can develop this further into three dimensions by averaging the calculated eccentricity over the surface of revolution"* (p.412) — 가중 (띠 y ds) 이 값을 바꾼다: AR 3 에서 2D 둘레 평균 ÷ ∛(AR) **0.830** ↔ 3D 표면 평균 prolate **0.752** (−9 %) · oblate **0.708** (−15 %) | 카드 §3-4 · §4-4 (iii) · 식 13–14 | [인쇄] · [카드 재계산] | 회전 타원체 · 무차원 · DEM 시험 없음
- [g] wensrich2012_rolling_friction_shape_contact_eccentricity_dem | 원문 Fig 6 의 oblate 선은 원문 식 재계산보다 AR 1.7 → 3 에서 +0.02 → +0.12 높고 '2D 둘레 평균 ÷ prolate 부피 반지름' 꼴과 ±0.006 안에서 겹친다 — 2D 꼴이 3D 그림에 섞였을 가능성 | 카드 §3-4 · §11-2 | [판독 · 래스터] · [카드 재계산] · 원인 [추정] | 계산 과정 [미확인] · 본 결론 (점묶음) 무영향

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 (넘김 0).  서론 인용만: ref [4] Dratt · Katterfeld · Wheeler 2010 (컨베이어 벨트 처짐의 FEM–DEM 결합 · 기계 부품 · 입자 아님 · 내용 없음).

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] wensrich2012_rolling_friction_shape_contact_eccentricity_dem | 모델 A (우리 압축 · 믹서 덱 `cdt` 꼴 · 정본 카드 표기) 의 정지 기어감은 3D 7000 입자 더미에서도 5 s 뒤 정착 중 — **크기 · 압력 아래 거동 미측정** → 판 고정 이완 · 언로딩 판정 전 cdt ↔ epsd2 같은 침대 한 런 · Δt × ½ 필요 | 카드 §7-3 · §8 단계 6 · p.410 · p.414 | [인쇄] (정성) · 크기 [미확인] | 중력 더미 · 300 MPa 아님
- [j] wensrich2012_rolling_friction_shape_contact_eccentricity_dem | 우리 μ_r (압축 AM 0.2/0.1 · SE–SE 0.1 · 믹서 0.075) 의 모양 근거 없음 · 식 (9) 환산은 R_r 정의 (cdt R_ef = R/2 ↔ 입자 반지름) 와 '절반' 규칙에 따라 SE–SE 0.1 = prolate AR 1.08–1.35 로 갈린다 · 조밀 압밀에서 구름마찰의 몫 [미확인] | 카드 §7-3 · §9 | [카드 산술] | 정본 카드 표기 · 리포 미대조

## k — DEM 의 한계
- [k] wensrich2012_rolling_friction_shape_contact_eccentricity_dem (Wensrich & Katterfeld 2012 · Powder Technol. 217, 409–417) | 축척 · 구 이상화: *"Practically this means scaling of particle size and stiffness, and idealisation in the form of spheres and simplified contact mechanics."* · 두 질문: *"how to get idealised spherical particles to behave like a bulk material made up of many more real particles of a wide size distribution and arbitrary shape"* | p.409 · 크롭 `txt_p1_scaling_spheres_two_questions_rolling_torque` | [인쇄] | 산업 DEM 일반 진술
- [k] wensrich2012_rolling_friction_shape_contact_eccentricity_dem (Wensrich & Katterfeld 2012 · Powder Technol. 217, 409–417) | 모양은 비싸서 대리: *"In a granular material these mechanisms can be important, however in a practical situation they are most likely dwarfed by the effects of shape. Shape is an expensive thing to model in DEM, and so rolling friction is typically used in an effort to model this effect."* | p.409 · `txt_p1_energy_loss_sources_shape_expensive` | [인쇄] | 비용 수치 없음
- [k] wensrich2012_rolling_friction_shape_contact_eccentricity_dem (Wensrich & Katterfeld 2012 · Powder Technol. 217, 409–417) | 보정값 ≠ 물성 (조율 매개변수 고백): *"the link between the model and the mechanism is not at all clear. In particular, there is currently no physical reasoning that is applied in the selection of a value for rolling friction, rather it tends to be treated as a parameter to be 'tuned' in an effort to produce realistic behaviour."* · *"Without any physical basis, the coefficient can only ever be considered a 'tuneable parameter'."* | p.410 · p.416 · `txt_p2_link_unclear_*` · `txt_p8_conclusions_*` | [인쇄] | —
- [k] wensrich2012_rolling_friction_shape_contact_eccentricity_dem (Wensrich & Katterfeld 2012 · Powder Technol. 217, 409–417) | 대리의 정량 한계: 구 + 모델 C 구름마찰이 같은 '등가' μ_r 의 겹친 구보다 안식각 *"up to 10° higher"* (판독 4.1–10.9°) · *"by at least a factor of two"* · 기전: *"shape can both create or encourage rolling as well as resist it, while all of the rolling friction models resist rolling in all cases"* | p.412 · p.416 · Fig 9 | [인쇄] · [판독 · 벡터] | 5 mm 중력 · 고정 모양
- [k] wensrich2012_rolling_friction_shape_contact_eccentricity_dem (Wensrich & Katterfeld 2012 · Powder Technol. 217, 409–417) | 정지 계 · 보정: 모델 A 의 *"bulk material creeping due to rapid oscillations in the rolling resistance due to the discontinuity in Eq. (1)"* (p.410) · 예비 A 런 더미가 5 s 뒤 *"still in the process of settling"* (p.414) · *"the notion of 'critical damping' used in most DEM studies (including the present) is based on a simplified one degree-of-freedom system"* (p.411) · *"One bulk parameter from one type of test is entirely insufficient"* (p.416) | 카드 §4-4 (i) | [인쇄] | 수치 없음 (기어감 크기)
- [k] wensrich2012_rolling_friction_shape_contact_eccentricity_dem | 말 없음: 믿을 수 있는 겹침 · 상대밀도 · 변형률 상한 · 접촉 독립 가정 · 조밀 영역 강성 | 카드 §4-4 (i) | — | —

## l — 소성변형이 왜 어려운가
- [l] wensrich2012_rolling_friction_shape_contact_eccentricity_dem (Wensrich & Katterfeld 2012 · Powder Technol. 217, 409–417) | **말 없음** — *"plasticity"* 는 구름 손실의 접촉 이력 근원 목록에 한 번 (*"micro-sliding, visco-elasticity, plasticity, surface adhesion, etc."* — 그리고 모양에 *"dwarfed"*) · 모델 C 의 *"elastic–plastic"* = 구름 토크 법칙 · 입자는 고정 모양 (구 · 겹친 구) | p.409 · p.410 · 카드 §4-4 (ii) | [인쇄] | 입자 소성 · 큰 변형 논의 0
- [l] wensrich2012_rolling_friction_shape_contact_eccentricity_dem (Wensrich & Katterfeld 2012) | 택한 우회와 값: 모양을 계산하지 않고 **토크로 흉내 (구름마찰 · 싸다)** 또는 **겹친 구로 고정 모양 (비싸다 · 비용 수치 없음)** · 맞춘 값 0 (식 9 = 예측) · 검증 = 안식각 150 런 (7000 입자 · PFC3D · 3–4 μs) → 예측이 ≈2 배 과대 | p.409 · p.412–416 · 카드 §3-7 | [인쇄] · [카드 산술] | 형상 변형 (SE 소성) 과 다른 문제 — 고정 모양의 대리

## m — 받아들일 통찰
- [m] wensrich2012_rolling_friction_shape_contact_eccentricity_dem | 무엇: **우리 μ_r 의 지위 = '조율 매개변수' 로 등록 + 모양 환산 규칙** (식 9 μ_r ≈ ⟨e⟩/R_r · R_r 정의 (cdt R_ef = R/2 ↔ 입자 반지름) · AOR '절반' 을 결과 전에 적어야 함 — 안 적으면 SE–SE 0.1 이 AR 1.08–1.35 사이 어디로도 읽힌다) | 후보 D0 · 단계 5 | p.410 · p.416 · 카드 §7-3 [카드 산술]
- [m] wensrich2012_rolling_friction_shape_contact_eccentricity_dem | 무엇: **단일 구 굴림 단위 시험의 해석 기대값** — 정지 토크 μ_r R m g · 감속 μ_r g/(1.4R) · 전환 각속도 (5/7)v₀/R · 굴림 진동 주기 2π√(1.4mR²/k_r) (Fig 2 판독 0.756 μN·m ↔ 0.751 · 528 ↔ 539 rad/s² · 40.4 ↔ 41.2 rad/s · ≈120 ↔ 121 ms) → LIGGGHTS cdt ↔ epsd2 단일 구 시험 표 | U2 | 카드 §3-3 [판독 · 래스터 · 카드 산술]
- [m] wensrich2012_rolling_friction_shape_contact_eccentricity_dem | 무엇: **함정 — A 꼴 (cdt) 구름 토크의 정지 기어감** (2D Ai 에 이어 3D 7000 입자 더미도 5 s 뒤 정착 중) → 판 고정 이완 · 언로딩 판정에 'cdt ↔ epsd2 같은 침대 한 런' · 'Δt × ½' 를 결과 전 등록 | 단계 6 · R4 | p.410 · p.414 · 카드 §7-3
- [m] wensrich2012_rolling_friction_shape_contact_eccentricity_dem | 무엇: **보정 설계 규칙 — 관측량 하나 = 매개변수 하나 · 반복 산포를 판정 띠에** (안식각 등고선이 (μ_p, μ_r) 넓은 범위를 지남 · 같은 칸 두 반복 차 평균 0.6–1.0° · 최대 2.5°) | 단계 0 · 단계 4 (R5) · 흐름 밖: 믹서 D3 (SE–SE 점착 유동성 앵커) | p.416 · Fig 9 · 카드 §3-6 · §3-8 [판독 · 벡터]

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
litdb 확인 = 정본 `litdb/papers/` 파일 목록 566 장 (`git ls-tree` · 이 카드 포함) + `git grep` (제1 저자 성 · 권 · 쪽 · 제목 낱말) + `_curation/wishlist.md` grep.
- [n] D. Markauskas, R. Kačianauskas, A. Džiugys, R. Navakas, Investigation of adequacy of multi-sphere approximation of elliptical particles for DEM simulations, Granular Matter 12 (2010) 107–123. ([16] 그대로) | k · m — 이 논문의 '모양의 정답' (겹친 구) 이 실제 모양 (타원) 을 얼마나 담는지 — 겹친 구 대리의 한계 (카드 §11-1 · §12) | papers/ 'markauskas' 없음 · grep 'Markauskas' = coetzee2017 (인용만) · wishlist 없음
- [n] H.P. Zhu, A.B. Yu, A theoretical analysis of the force models in discrete element method, Powder Technology 161 (2006) 122–129. ([15] 그대로) | e · k — 편심을 구름마찰 계수의 정의로 쓰는 예 (식 9 의 이웃 · p.412 의 refs 7 · 13 · 15) · DEM 힘 모델의 이론 분석 | papers/ 'zhu2006' 없음 · '161 (2006) 122' grep 0 · wishlist 없음
- [n] T.-T. Ng, Shear strength of assemblies of ellipsoidal particles, Geotechnique 54 (2004) 659–669. ([17] 그대로) | k · m — 비구형 (타원체) 을 대리 없이 푼 DEM 의 강도 — 구름마찰 대리와 견줄 직접 계산 | papers/ 'ng2004' 없음 · 'Ng, Shear strength' grep 0 · wishlist 없음
- [n] Y.C. Zhou, B.D. Wright, R.Y. Yang, B.H. Xu, A.B. Yu, Rolling friction in the dynamic simulation of sandpile formation, Physica A 269 (1999) 536–553. ([13] 그대로) | k · e — 모델 A · B 원전 (= 우리 cdt 꼴) | papers/ 없음 · **wishlist L208 에 이미 있음** (새로 올리지 않음)
- [n] K. Iwashita, M. Oda, Rolling resistance at contacts in simulation of shear band development by DEM, Journal of Engineering Mechanics ASCE 124 (1998) 285–292. ([14] 그대로) | k · e — 모델 C · k_r = R_r² k_s 원전 | papers/ 없음 · **wishlist L209 에 이미 있음** (새로 올리지 않음)

## 카드 문제
- 없음 — 가리킨 카드 `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` 의 2 차 인용에는 **숫자가 없고** 귀속 문장은 원문과 맞다: L87 *"수정 탄소성 스프링–대시포트 (Wensrich & Katterfeld 2012)"* · L144 *"EPSD 구름마찰 — 구름 저항을 탄소성 스프링–대시포트로 모델 (Wensrich & Katterfeld)"* · L191 · L49 · L244 서지 (제목 · 학술지 · 권 · 쪽 · 연도 = 원문 첫 쪽).  단서 하나만 빠짐 — EPSD (모델 C) 의 원형은 Iwashita & Oda [14] · Ai [12] 이고 이 논문은 강성 (k_r = R_r² k_s) · 감쇠 (없음) 설정을 고른 판이다 (p.410–411 · p.414).  LIGGGHTS 는 원문에 0 회 — LIGGGHTS EPSD 계열과의 관계는 원문으로 확인되지 않는다.
- (참고 · 문제 아님 · 낡은 표기) `roessler2019_…` L244 *"카드 없음"* · `ai2011_rolling_resistance_contact_models_dem` L340 *"정본 카드 없음"* — 이 카드로 해소 (그 카드들은 고치지 않음).
- (참고 · 문제 아님) `coetzee2017_dem_calibration_review` L162–163 의 따옴표 문장 *"there is no physical reasoning for choosing a value for rolling friction other than tuning the bulk behaviour to be more realistic"* 은 리뷰 (Coetzee · §3 p.106) 의 풀어쓰기다 — 원문 낱말은 p.410 *"there is currently no physical reasoning that is applied in the selection of a value for rolling friction, rather it tends to be treated as a parameter to be 'tuned' in an effort to produce realistic behaviour"* (뜻 같음).  L611 · L50 의 귀속은 원문과 같다.
- (원문 자체의 어긋남 — 카드 문제 아님 · 새 카드 §11) Fig 6 oblate 선이 원문 식 (9) · (12)–(15) 재계산보다 AR 3 에서 ≈0.11 높음 (prolate · R_r 그림은 ±0.005) · R_r 두 정의 (식 2 ↔ 식 9 · 15 — 안식각 런이 어느 쪽을 썼는지 미기재) · 식 (3) 차원 · 식 (5) 절댓값 · Fig 5 정규화 미기재 · 'Tertiary' ↔ 'ternary' 표기 · *"up to 10°"* ↔ 판독 최대 10.9° · *"within 1–2%"* ↔ 곡선 0–3.3 %.
