# batch 155 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-24 · 후보 표 N-111 · 새 카드)

대상: `capece2015_multicomponent_granular_bond_number_cohesive_blend_flow_function` — M. Capece, R. Ho, J. Strong, P. Gao, "Prediction of powder flow performance using a multi-component granular Bond number", *Powder Technol.* **286** (2015) 561–571 · DOI 10.1016/j.powtec.2015.08.031.
단일 분말 11 개 (APAP · Avicel PH 105 · 101 · 102 · 200 · Starch 1500 · 다섯은 R972 나노 건식 코팅 판) 의 입상 Bond 수 (Rumpf 다돌기 반데르발스 힘 · 돌기 200 nm **가정** · IGC 분산 표면 에너지 → Hamaker) 와 환형 전단 흐름 함수 계수로 ff_c = 15.7·Bo^−0.27 을 맞추고, **혼합물 Bond 수** (쌍 Bo 를 표면적 몫의 곱으로 가중한 조화평균 · 혼합쌍 = Hamaker 기하평균 · 지름 · 돌기 · 무게 조화평균) 를 같은 식에 넣어 이원 · 삼원 · 오원 혼합물의 ff_c 를 혼합물 자료에 맞추지 않고 예측했다.
쪽 = PDF 쪽 p.1–11 (인쇄 쪽 = PDF + 560) · SI 없음 · 계산 (DEM · FEM · MPM) 없음 · 고른 의도 대조 = **일부** (다성분 Bo 정의 · 흐름 예측 검증 = 채움 / '우리 3 상 Bo 정의에 직접' = 일부 — 쌍 무게 · 힘 법칙 · 출력이 우리와 다르다 / 회전 속도 축 · 코팅 DEM = 없음 · 카드 §0-1).
인용 서지 (질문 k · l 용): M. Capece et al., *Powder Technol.* **286** (2015) 561–571, DOI 10.1016/j.powtec.2015.08.031.
⚠ 이원 혼합물 ff_c 는 **그림에만** 있다 (그림 3 · 4 · 6) → 카드의 이원 값은 [판독] (`digitized.csv` 55 행 · 순수 성분 점이 표 1 ff_c 를 0.00–0.04 로 재현) · 표 2–5 의 쌍 Bo · Bo_Mix · 예측은 카드 산술로 전부 재현 (원문에 없는 표면적 몫 식 f_SA = x/(ρ d32) 를 역산) · 코팅 삼원 AAD 1.01 만 재현 안 됨 (표 3 으로 1.37).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (고체전해질 · 압밀 · 기공 없음 — 제약 분체 흐름 시험).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 (탈압 없음 · 환형 전단의 예압 1 kPa · 파괴 250–600 Pa 는 흐름 시험이지 압밀이 아니다 · 카드 §4-3).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 (원문 `yield` 12 회는 전부 흐름 시험의 뜻 — *yield locus* · *unconfined yield strength* · *to yield or flow* · 경도 · 탄성은 *"not taken into account"* 로만 (p.10) · 카드 원문 대조 기록).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (압밀 없음 · 입자 = 강체 구 + 돌기).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 (점착 힘 = Rumpf 다돌기 · 강체 구 · 변형을 넣은 점착 모형은 *"may also be employed"* 한 문장뿐 (p.5) · 큰 변형 진술 없음).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음.

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 (실물 3D 분말 · 2D ↔ 3D 진술 0).

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] capece2015_… | 원문 한계 = 흐름은 *"consolidation stress and time"* · 습도 · 장치 · 모양 · *"mechanical properties (elasticity and hardness)"* 에 달렸는데 고려하지 않았다 (p.10) · *"Cohesion force models which consider deformation … potentially used to predict the effect of consolidations stress"* (p.5) — 단 여기 '압밀' 은 환형 전단 예압 **1 kPa** 수준 (우리 300 MPa 의 30 만 분의 1) | 카드 §3-7 · §4-3 | 인쇄 | 가압 · 탈압 계산의 근거가 아니다 (흐름 시험의 이력 변수)

## k — DEM 의 한계
- [k] capece2015_… (M. Capece et al., *Powder Technol.* 286, 561–571, 2015) | **말 없음 (계산 없음)** — 원문 11 쪽 글자 층 (참고문헌 앞) 에 `DEM` · `discrete element` · `simulat` · `finite element` · `plastic` = **0 회** · 모형 일반의 한계만: *"Particulate processes remain exceedingly difficult to model, design, and control … particle-scale interactions are difficult to resolve. Additionally, constitutive relationships derived from first-principles relating bulk-scale behavior, particle-scale interactions, and particle properties are generally unattainable."* (p.1) · *"particle assemblies have very complex behavior in comparison to particle–particle interactions quantified by the Bond number"* (p.5) | 카드 §4-3 · 원문 대조 기록 | 인쇄 · 카드 셈 | 측정 + 반경험 모형 논문 — 단단한 구 · 점접촉 DEM 의 한계를 말하는 문헌이 아니다

## l — 소성변형이 왜 어려운가 · 우회 · 값 · 비용
- [l] capece2015_… (같은 서지) | **논의 없음 · 우회 = 넣지 않음** — vdW 힘이 *"mechanical properties such as hardness and elasticity"* 에 달렸다 (p.2) · 변형을 넣은 점착 모형은 *"may also be employed"* (p.5) 라고만 하고 쓰지 않았다 (강체 구 + 돌기 200 nm 가정) · 맞춘 값 = α · β 둘 (단일 분말 8 점) · 계산 비용 해당 없음 | 카드 §4-1 · §4-2 · §4-3 | 인쇄 | 소성 · 큰 변형 문헌이 아니다

## m — 받아들일 통찰
- [m] capece2015_… | **판가름 수 감도 표에 '거칠기' 와 '쌍 무게 규약' 두 축을 더한다** — 논지 §2-3 의 0.31 (AM_S 0.39) 은 매끈한 구 · 가벼운 쪽 무게 규약의 값이고, 이 논문의 Rumpf 다돌기 힘 (돌기 200 nm) 으로는 R\* 기하 이득이 1.80 → **1.08** 이라 판가름 수가 **0.857 (0.879)** 로, 쌍 무게를 조화평균 (식 13) 으로 두면 크기비 1 : 9 에서 혼합쌍 Bo 가 절반 (1.999 배) 이라 1.23 (매끈) · 3.43 (돌기) 로 옮겨 간다 [카드 산술] · 논지 §2-7 의 *"거칠기 · 모양 — 실제 접촉 반경은 … 돌기 반경일 수 있다"* 를 숫자로 만든 것 | 흐름 밖: Ⓒ 믹서 논지 · 결과 전 대조 항목 — 왜: P1 (비코팅 SE–SE 응집) 이 거칠기 하나로 훨씬 쉬워지고 코팅의 기하 이득이 사라질 수 있다 → AFM 측정 묶음에 **돌기 크기 (지형)** 를 넣고 감도 표를 B2-U · B2-C 판독 전에 등록 (카드 §7-2 · §9-1)
- [m] capece2015_… | **쌍 Bo 의 분모 규약을 덱 · 등록에 명시하고, Capece 쌍 Bo 를 우리 부착 판정에 쓰지 않는다** — 원문의 무게 조화평균 근거는 *"A harmonic mean is also used to define particle weight."* 한 문장 (p.7) · 목적이 혼합물 전체 흐름이라 '작은 SE 가 큰 AM 에서 떨어지나' 를 보는 우리 판정에는 가벼운 쪽 무게 (Figueroa · 논지 · 덱) 가 맞다 [카드 해석] · 그대로 쓰면 r = 1 (코팅) 에서도 SE–AM Bo 가 SE–SE 의 0.54 배라 순서가 뒤집힌다 [카드 산술] | 단계 0 · 후보 D0 — 왜: 문헌 Bo 를 옮길 때 규약 변환을 같이 적지 않으면 같은 '쌍 Bo' 이름으로 2 배 다른 값을 섞는다 (카드 §7-2 · §9-2)
- [m] capece2015_… | **'무작위 접촉' 기준선을 식으로 쓴다 — 표면적 몫의 곱** (식 14 · *"the likelihood or probability that these two materials come into contact"* p.7) → 우리 조성 (덱 80 : 18 · P : S 7 : 3) 에서 SE–SE 0.608 · SE–AM 0.344 · AM–AM 0.049 [우리 산술] · 원문이 *"may offer a superior formulation"* 이라 부른 배위수 가중을 DEM 은 직접 잰다 | 흐름 밖: Ⓒ 믹서 판독 (SE 군집 무작위 대비 · AM–SE 접촉 분율) — 왜: '무작위 대비' 관측량의 분모를 결과 전에 한 식으로 고정할 수 있다 (카드 §7-3 · §9-3 · §9-4)
- [m] capece2015_… | **흐름 지표 (Bo_Mix) 와 혼합 상태를 섞지 않는다** — 조화평균이라 우리 조성에서 무게 4.9 % 인 AM–AM 쌍이 1/Bo_Mix 의 95–99 % 를 차지하고, 코팅 (γ_AM ↑) 은 이 지표로 Bo_Mix ×9.5 = '덜 흐른다' 로 나온다 [우리 산술] · 원문은 혼합물을 *"well-mixed"* 로 가정한다 (p.7) | 단계 0 · 흐름 밖: Ⓒ 관측량 설계 — 왜: 논지 P2 (분산) 와 다른 축이라 결과 전에 갈라 적지 않으면 '코팅 = 흐름 나빠짐' 을 '분산 나빠짐' 으로 읽게 된다 (카드 §7-3 · §9-6)
- [m] capece2015_… | **표면적은 d32 기하와 BET 를 둘 다 적고, 예측 오차는 '끝점 포함 여부 · AAD · 상대 · 치우침' 을 같이 적는다** — BET 로 가중하면 APAP–PH 200 50 : 50 의 APAP 몫이 0.944 → 0.198 로 뒤집힌다 (원문은 기하 면적으로 성공) [카드 산술] · 인쇄 이원 AAD 0.40 · 0.99 · 0.16 은 끝점을 뺀 값임이 판독으로만 드러났고 코팅 삼원 1.01 은 재현이 안 된다 | 단계 0 · 흐름 밖: 보고 양식 — 왜: NCM 2 차 입자는 다공이라 BET ≫ 기하일 것 · 우리 보고에서도 같은 모호가 생긴다 (카드 §9-5 · §9-8)
- [m] capece2015_… | **코팅 숙주 간 이동을 관측량으로** — 코팅 분체와 비코팅 분체를 섞는 팔을 *"due to the likelihood of R972 transferring from coated particles to as-received particles in the mixing process"* 때문에 만들지 않았다 (p.9) | 흐름 밖: Ⓒ 코팅 팔 판독 — 왜: 우리 DEM 은 SE 입자의 '붙은 AM id' 이력으로 그 이동을 직접 잴 수 있다 (카드 §9-7)

## n — 논문 에이전트 후보
- [n] Y. Chen, J. Yang, R. Dave, R. Pfeffer, Fluidization of coated group C powders, AICHE J. 54 (2008) 104–121. (원문 참고 [21]) | ★ m · e — **식 (1) 다돌기 모형 · 식 (5) 코팅 돌기 힘 · 1 % R972 선택의 원전** · 돌기 크기 → 힘 → 유동화의 검증 (우리 '거칠기 감도' 축의 근거) | litdb 확인: papers/ 623 목록 `ls` 에 chen2008 없음 · `grep -r -i` 'Fluidization of coated' (md · tsv · json · figures 제외) = 이 카드만 → 카드 없음
- [n] L. Jallo, Y. Chen, J. Bowen, F. Etzler, R. Dave, Prediction of inter-particle adhesion force from surface energy and surface roughness, J. Adhes. Sci. Technol. 25 (2011) 367–384. (원문 참고 [25]) | ★ m · G2 — 표면 에너지 + 거칠기 → 점착력 예측을 AFM 으로 검증한 논문 (돌기 가정의 근거 · 우리 SE 탐침 AFM 설계) | litdb 확인: `grep -r -i` 'inter-particle adhesion force from surface energy' = 이 카드 + `mohammadijam2014_…` 참고문헌 표 ref 49 (인용만) → 카드 없음
- [n] M. Capece, Z. Huang, D. To, M. Aloia, C. Muchira, R. Davé, A. Yu, Prediction of porosity from particle scale interactions: surface modification of fine cohesive powders, Powder Technol. 254 (2014) 103–113. (원문 참고 [23]) | m · 단계 5 (간접) — 같은 1저자의 Bo → 충전 기공률 (압밀 전 출발 침대의 기공을 쌍 점착으로) | litdb 확인: `grep -r -i` 'Prediction of porosity from particle scale' = 이 카드만 → 카드 없음
- [n] A. Yu, C. Feng, R. Zou, R. Yang, On the relationship between porosity and interparticle forces, Powder Technol. 130 (2003) 70–76. (원문 참고 [24]) | m — 기공률 ↔ 입자간 힘 (Bo) 의 원 관계 · 점착 침대의 출발 기공 | litdb 확인: `grep -r -i` 'porosity and interparticle forces' = 이 카드만 → 카드 없음
- [n] Castellanos, The relationship between attractive interparticle forces and bulk behaviour in dry and uncharged fine powders, Adv. Phys. 54 (2005) 263–376. (원문 참고 [17]) | m — 입상 Bond 수 정의 · 건식 미분체 리뷰 (deng2021 카드도 인용) | litdb 확인: `grep -r -i` 'attractive interparticle forces' = 이 카드 + `deng2021_…` (인용만) → 카드 없음

## 카드 문제
- 수치 문제 없음 — 이 논문을 인용 · 언급한 정본 카드는 둘 (`alizadeh2018_dem_adhesion_calibration_segregation_heap` · `deng2021_mechanical_surface_energy_tester_bond_number`) 이고 옮긴 서지는 원문과 **같다** (옮긴 수치 없음).
- `alizadeh2018_…` **L274** '왜' 칸 *"다성분 입상 Bond 수 — 우리 3 상 Bo 정의에 직접"* — **과한 기대 (문제 아님)**: 이 논문의 쌍 Bo 는 무게 조화평균 · Rumpf 돌기 힘 · 출력 = 흐름이라 우리 3 상 Bo 에 '직접' 쓰면 SE–AM ↔ SE–SE 순서가 뒤집힌다 [카드 산술] → 판정 **일부**.  고치지 않았다 (새 카드 §0-1 · §7-2).
- `deng2021_…` **L323** '왜' 칸 *"이종 혼합 (AM + SE) 의 Bo 정의"* · **L208** *"혼합물로 넓힌 것 = 다성분 Bond 수 (ref [10] Capece 2015 …)"* — L208 은 **맞음** · L323 은 위와 같은 이유로 **일부**.  고치지 않았다.
- 정본 밖 참고: 논지 §2-3 (`docs/hetero_thesis.md`) 의 0.31 · 0.39 는 매끈한 구 · 가벼운 쪽 무게 규약의 값이다 — 틀린 것은 아니고 규약 한정어가 필요하다 (§2-7 이 이미 거칠기를 말로 경고).  리포 문서는 고치지 않았다 (읽기만).

## 공백 검사 G1–G4 (★ 이 카드의 핵심 산출 · 카드 §0-2 와 같은 판정)
- **G1 — 점착 대비를 설계 변수로 혼합 결과 (덮임 ↔ 뭉침 · 섞임 ↔ 분리) 를 예측** → **없음 (혼합 상태를 가정한다)** | 근거: *"the Bond number for a well-mixed ternary or any N-component mixture can be determined by Eq. (8) with the weighting function of Eq. (14)"* (p.7) · 가중 = *"the likelihood or probability that these two materials come into contact"* (p.7 · 무작위 접촉) · 코팅 *"It was assumed that the R972 was equally distributed to all materials during mixing"* (p.3) · 결과 관측량 = ff_c 하나 | 좁힐 필요 없음.  ★ 가져올 것 = 무작위 접촉 기준선 (표면적 몫의 곱) → 우리 'SE 군집 무작위 대비' 의 분모
- **G2 — 점착 입력을 따로 재고 (AFM · IGC · 접촉각 등) 혼합 결과를 미리 예측** → **일부 — 반례 (결과 = 혼합물의 흐름일 때)** | 근거: IGC γ_d (p.4 · 셋은 이 논문 측정 · 셋 + 코팅값은 Huang [26]) → Hamaker (식 4) → 쌍 Bo (식 1 · 9–13) → Bo_Mix (식 8 · 14) → ff_c (식 7 · α β 는 단일 성분에서만 맞춤) → 혼합물 60 점 + 맞춤 밖 전분 · *"Experiments would mainly serve to confirm the theoretical predictions"* (p.9) · ⚠ 사전 등록 · 상관 통계 없음 · 혼합 **상태** 는 결과가 아님 | 좁힐 문장: "따로 잰 표면 에너지 (IGC) → 혼합물 Bond 수 → 혼합물 **거시 흐름** 을 혼합물 자료에 맞추지 않고 예측한 선례 (Capece 2015 · 제약 분체 2–5 성분 · AAD 0.13–1.01)" 를 먼저 적고 우리 몫을 ① 결과 = 혼합 **상태** 와 압밀 뒤 수송 ② 입력 = 같은 SE 탐침 AFM 의 쌍별 부착 (기하평균 가정 대신) ③ 무기 황화물 · 건조 불활성 ④ 결과 전 등록 · 판정선 으로 좁힌다
- **G3 — 회전 속도 최적을 입자 수준 맞교환 (덩어리 풀림 ↔ 벽 부착 손실 등) 으로 설명** → **없음** | 근거: 혼합 · 코팅 = LabRAM **75 g · 60 Hz · 10 min** 한 조건 (p.3) · 공정 축 · 입자 수준 관측 0 · 코팅 입자에서 비코팅 입자로 R972 가 옮겨 갈 가능성만 말로 (p.9) | 좁힐 필요 없음.  ★ 가져올 것 = 손님 입자의 숙주 간 이동을 실험 설계에서 피했다는 사실 → 우리 코팅 팔의 관측량
- **G4 — 공정 × 재료 상태도 (회전 세기 × 점착 · Bond 수 등) 가 다른 재료로 옮겨 감** → **일부 (재료 · 조성 축만 · 제약 부형제 안)** | 근거: 삼원 예측 ff_c 지도 (그림 5 · 7 · 조성 × ff_c) · *"the model parameters α and β are expected to be material independent … This should be confirmed only after a wider range of materials have been examined"* (p.5) · 이전 증거 = 맞춤 밖 전분 1 종 (4.66 ↔ 5.35) · 공정 축 0 · 부피밀도 × ff_c 상태도는 Huang [41] 을 *"would be most useful"* 로 제안만 (p.10) | 좁힐 문장: "Bond 수 → 흐름의 한 곡선 (α β) 이 같은 계열 다른 부형제로 옮겨 간 선례 (전분 1 종)" → 우리 몫 = 공정 축 (rpm · Fr · 혼합 시간) × 점착 비 의 2 차원 지도 · 무기 재료 · 혼합 상태와 압밀 뒤 결과
