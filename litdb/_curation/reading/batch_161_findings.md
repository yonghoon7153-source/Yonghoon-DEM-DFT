# batch 161 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-24 · 후보 표 N-156 · 새 카드)

대상: `dave2003_dry_coating_dem_mechanofusion_hybridizer_maic_three_devices` — R. Dave · W. Chen · A. Mujumdar · W. Wang · R. Pfeffer, "Numerical simulation of dry particle coating processes by the discrete element method", *Adv. Powder Technol.* **14** (4) (2003) 449–470 · DOI 10.1163/156855203769710672 (원문 22 쪽에 인쇄 없음 · PDF 메타데이터 XMP 와 지시서 메모가 같음).
건식 입자 코팅 장치 셋 — 메카노퓨전 (MF · 2D host 만) · Hybridizer (축소 3D host 만 · 공기 없음) · 자기 보조 충격 코팅 MAIC (자석 100 개 · 점 쌍극자 식 1–6) — 을 Walton 형 소프트 구 DEM 으로 하나씩 돌려 장치 규모 운동 에너지 · host 규모 충돌 빈도 · 평균 충돌 속도 · 안쪽 조각 힘을 내고, 게스트는 시간 간격 (≤ 10⁻⁹ s) 때문에 넣지 못해 덩어리 하나의 충돌 문제로 미룬 개관.
쪽 = 인쇄 p.449–470 (PDF p.1–22 · 인쇄 = 448 + PDF) · 그림 20 (그림 7–9 · 12–16 = 1-bit 300 dpi 래스터) · 표 0 · 번호 식 6 (MAIC 쌍극자) · 참고 12 · SI 없음 · 계산 = DEM 셋 · 실험 0 (그림 1 SEM 만) · 고른 의도 대조 = **일부** (세 장치 DEM = 채움 · '비교 (충돌 에너지 · 빈도)' = 장치마다 다른 양을 나란히 놓았을 뿐 · '어느 장치를 흉내 낼지' = 원문 권고 없음 → 카드 산술로 MF 꼴).
인용 서지 (질문 k · l 용): R. Dave, W. Chen, A. Mujumdar, W. Wang, R. Pfeffer, *Adv. Powder Technol.* **14** (4) (2003) 449–470.

⚠ 글자 층은 합자 (fi · fl · ff) 와 기호 ('=' → 'D' · µ → '¹' · × → '£' · π → '¼') 를 깨뜨린다 — 인용문 · 식 · 숫자는 400 dpi 렌더로 확인 · 그림 값은 원 래스터 좌표 판독 (`litdb/figures/<slug>/digitized.csv` 112 행).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (고체전해질 · 압밀 · 기공 없음 — 이름 없는 host · 'magnesium 흉내' 구 · 자석의 장치 속 운동).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 (압밀 · 탈압 없음).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 물성은 MF 의 누름 법선 강성 20,000 kg/s² · 반발 계수 0.85 뿐 (p.456 · 접촉 법칙 입력값 · 재료 물성 아님).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (장치마다 한 종 단분산 · 압밀 없음).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] dave2003_… | **Walton 형 소프트 구 하나 · 대안 · 범위 논의 없음** — 상호작용 범위를 *"frictionless, elastic hard spheres to elastic-plastic, frictional soft spheres"* 로 적고 [9, 10] 의 소프트 구를 고름 · *"This approach can handle complicated inter-particle forces arising from auto-adhesion, friction and the presence of a viscous fluid."* (p.452 · 이 논문 계산에 점착 · 유체 항은 없음) · MF 물성 = e 0.85 · K1 20,000 kg/s² (p.456) · 맞춘 값 0 | 카드 §3-1 · §3-2 · §4-2 | [인쇄] | 접선 법칙 · 마찰 값 [미확인] · Hybridizer 강성 [미확인] · 큰 변형 범위 말 없음.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 없음).  덧붙임 (흐름 밖 · DEM 판독 규칙): 등부피 고리 V_i = V/N · 고리 너비 ≥ 최대 입경 → 7 고리 (p.455) — 칸 해상도 규칙의 DEM 판.

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] dave2003_… | **2D ↔ 3D 를 장치마다 따로 골랐을 뿐 · 전이 말 없음** — MF 2D *"so as to keep the computations to a reasonable value"* (p.455) · Hybridizer *"Unlike the MF system, here, the simulation is carried out in three-dimensions."* (p.462) · 2D → 3D 전이 시험은 같은 그룹 chen2004 (운동 세기 −4 – +2 % · 충돌 압력 +11 – +17 % · 그 카드 §3-3) | 카드 §4-3 (iii) | [인쇄] | MF · Hybridizer 는 장치 · 물성이 달라 2D ↔ 3D 비교가 아니다.

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
- [h] dave2003_… | **FE · MPM 으로 넘긴 것 없음 · 대신 규모 나누기 (장치 DEM → 덩어리 하나의 충돌 DEM)** — *"the overall problem can be divided into sub-parts"* (p.452) · *"rather than modeling a complete dry particle coating system including host particles and agglomerates, one could focus on agglomerate behavior through particle dynamics simulations to improve on computational speed"* (p.453) · 덩어리 경우 셋 = host 충돌 · 평판 벽 충돌 · 두 평판 사이 압축 (p.468–469 · 계산 미보고) | 카드 §3-8 · §7-2 · §7-4 | [인쇄] | 넘긴 시점 · 경계 조건 (충돌 속도 분포) 의 연결 방법 없음 — 우리 DEM → MPM 단일 충돌 나눔과 같은 생각 [카드 해석].

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] dave2003_… | **가압 · 탈압과 닿는 한계 없음** — 원문이 스스로 남긴 것은 장치 · 계산 쪽: *"the results are quite limited without the inclusion of guest particles, fluid effects, realistic device dimensions and operating conditions that very closely mimic the experiments"* (p.468) · 빈도 · 접촉 힘 · 틈 · 입자 성질 의존 *"will appear in a separate paper"* (p.459) · 덩어리 풀림 *"The detailed computations, not reported here"* (p.469) · Hybridizer 공기 = *"In a subsequent study"* (p.460) · MAIC 자석 + host = *"being performed"* (p.467) | 카드 §11 | [인쇄] | —

## k — DEM 의 한계
- [k] dave2003_… (R. Dave, W. Chen, A. Mujumdar, W. Wang, R. Pfeffer, *Adv. Powder Technol.* 14 (4), 449–470, 2003) | **말한 것 — 게스트를 넣으면 계산이 감당 안 됨 · 시간 간격 장벽 · 유체 · 실제 치수 부재** — *"it is clear that by itself in its current form, DEM cannot provide a full picture of the dry coating process due to the severe computational burden created when guest particles are included in the simulation"* (p.469) · *"The major limiting factor in these simulations is the time-step for the numerical integration, which is a strong inverse function of the particle size. Hence, if realistic guest particles are used, e.g. 1 µm or even as small as 200 nm, then the time-step becomes as small, or smaller than 10⁻⁹ s."* · *"simulating even a finite number of very small particles is still unrealistic"* (p.468) · Hybridizer: *"for a more realistic modeling, one must include the effect of the fluid in the system and its drag force on the particles"* (p.452) · 공기 없는 결과 = *"conservative"* (p.461) · 반대 쪽 주장: *"the particle stiffness does not significantly affect the kinematics of the system [1]"* (p.456 — ⚠ [1] = Yokoyama 등 Kona 실험 논문 · 정본 walton1993 카드는 깊은 흐름의 강성 민감을 옮김) | 카드 §3-8 · §4-3 (i) · §3-10 | [인쇄] | 믿을 수 있는 겹침 · 밀도 상한 · 모양 불변 말 없음.

## l — 소성변형이 왜 어려운가 · 우회 · 값 · 비용
- [l] dave2003_… (같은 서지) | **논의 없음 · 우회 = 소프트 구 접촉 법칙 · 비용 = 시간 간격** — 입자 모양 변화 · 게스트 막 = 범위 밖 · 소성 쪽은 상호작용 범위 말뿐 (*"elastic-plastic, frictional soft spheres"* p.452) · 맞춘 값 0 (e 0.85 · K1 20,000 kg/s² = 고른 값) · 비용: *"The simulations reported in the previous sections utilized larger particles that required time-steps of 10⁻⁶ to 10⁻⁷ s and simulating only several seconds of physical time, required a number of hours on a computer workstation."* (p.468) · 처방 = *"highly sophisticated numerical schemes as well as clever algorithm development … without simulating the complete system at the smallest length scale"* (p.468) | 카드 §3-8 · §4-3 (ii) | [인쇄] | 입자 수 · 계산 시간 숫자 · 하드웨어 [미확인].

## m — 받아들일 통찰
- [m] dave2003_… | **코팅 과정 DEM 의 가장 싼 장치 꼴 = 메카노퓨전 꼴 (드럼 덱 + 고정 원통 + 긁개 입자)** — 원문: MF 만 공기 없이 *"good qualitative agreement"* (p.452) · Hybridizer 는 공기 · 항력 필수 (p.452) · MAIC 는 쌍극자 힘 새로 (p.465) / 카드 산술: MF 평균 충돌 0.29 m/s (chen2004 판독) 면 B2-U 물성 SE–SE 겹침 0.32 % (1 % 계약 안) · Hybridizer 평균 2.5–12.7 m/s (그림 15 판독) 면 1.8–6.8 % → 1 % 계약에 E 4.6–119 배 · Δt 0.47–0.09 배 | 카드 §7-2 | [판독] · [카드 산술 · Hertz δ ∝ v^0.8 · 1 % = 1.17 m/s (chen2004 카드 §7-2)] | 흐름 밖: Ⓒ 코팅 믹싱 · 축소 3D · 공기 없음 · 강성 [미확인].
- [m] dave2003_… | **충돌 셈의 정의를 결과 전에 적고 입자끼리 / 경계로 나눈다** — Hybridizer 입자–경계 1.14 × 10⁶ ↔ 입자–입자 1.22 × 10³ /s (그림 12 판독 · 경계 / 입자끼리 370–1900) 인데 '충돌' 정의가 없고, MF 강성이면 입자–경계 접촉 시간 5.9 µs 라 1 초 10⁶ 번의 따로인 충돌이 들어갈 수 없다 [카드 산술 · 가정] · MF (chen2004 계 평균) 입자끼리 / 경계 ≈ 7 ↔ Hybridizer 경계 / 입자끼리 ≈ 940 = 장치별 응력 꼴의 숫자 | 카드 §3-6 · §0-3 · §9-2 | [판독] · [카드 산술] | 흐름 밖: Ⓒ · 단계 0 · 셈 정의 [미확인].
- [m] dave2003_… | **게스트 수준 = 덩어리 하나의 충돌 셋 (host 충돌 · 평판 벽 충돌 · 두 평판 사이 압축) → MPM 단일 충돌 경우 목록** — *"These cases take into account most interactions that an agglomerate would undergo"* · 풀림 ∝ 충돌 속도 · ∝ 1/게스트 표면 에너지 · 낮은 속도 = 되튐 · 두 면 사이 압축이 가장 많이 깸 (p.468–469 · 미보고) — 속도는 DEM 분포에서 뽑는다 | 카드 §3-8 · §8 (U0–U6) · §9-3 | [인쇄] | 흐름 밖: Ⓒ (DEM → MPM) · 정성 · 값 0.
- [m] dave2003_… | **게스트 시간 간격 장벽 (≤ 10⁻⁹ s) = 우리 믹서 덱이 SE 를 parcel (CGF 151.4 · 실제 r 0.5 µm) 로 다루는 이유의 문헌 근거** — 같은 장벽을 거친 입자로 돌아가는 셈 · parcel 이 덩어리 풀림 · 붙음 물리를 지키는지는 미검증 | 카드 §7-1 · §8 (D0) | [인쇄] · [카드 해석] | 흐름 밖: Ⓒ · 후보 D0.

## n — 논문 에이전트 후보
- [n] K. D. Kafui and C. Thornton, Computer simulated impact of agglomerates, in: Powder & Grains '93, C. Thornton (Ed.), pp. 401–406. Balkema, Rotterdam (1993). (원문 참고 [11]) | ★ m · j (G1) — 이 논문의 덩어리 풀림 모형이 바탕으로 삼은 접근 (*"The agglomerate break-up model is based on the approach taken by Kafui et al. [11] that includes the simulation of agglomerates impacting a wall."* p.453 · '풀림 ∝ 충돌 속도 · ∝ 1/표면 에너지' 의 바탕) · 우리 MPM 단일 충돌 경우 목록 · 점착 축 | papers/ 에 없음 (ls · grep 'Kafui' · 'Computer simulated impact of agglomerates' 0 건) · wishlist L448 의 Kafui 는 다른 서지 (2002 유동층).
- [n] M. Ramlakhan, C.-Y. Wu, S. Watano, R. N. Dave and R. Pfeffer, Dry particle coating using Magnetically Assisted Impaction Coating (MAIC): modification of surface properties and optimization of system and operating parameters, Powder Technol. 112 (1-2), 137–148 (2000). (원문 참고 [5]) | m (G3) — 건식 코팅 장치의 운전 변수 최적화 실험 (rpm 에 해당하는 장 · 자석 변수의 최적이 있으면 G3 의 실험 쪽) | papers/ 에 없음 (grep 'Ramlakhan' = 다섯 카드 모두 Pfeffer 2001 총설의 공저자 표기뿐).
- [n] M. Otani, M. Hironori, U. Tetsuya and S. Kunio, Mechanism of particle shape modification by dry impact blending, Advanced Powder Technol. 7 (4), 291–303 (1996). (원문 참고 [3]) | l · m — Hybridizer 충격으로 입자 모양이 바뀌는 기전 (막 · 소성 쪽 · DEM 이 못 보이는 부분) | papers/ 에 없음 (otani2023 · otani2025 카드는 다른 논문).
- [n] H. Honda, K. Ono, T. Ishizaka, T. Matsuno, T. Katano and M. Koishi, Surface modification of powders by the high speed impact method, J. Soc. Powder Technol., Japan 24, 593–599 (1987). (원문 참고 [2]) | m — Hybridizer 실험 (제목 = 고속 충격법) · 장치 치수 · 운전 창 | papers/ 에 없음.
- [n] R. K. Singh, A. Ata, J. Fitz-Gerald and Y. I. Rabinovich, Dry coating method using magnetically assisted impaction in a randomly turbulent fluidized bed, Kona 15, 121–131 (1997). (원문 참고 [4]) | m — MAIC 실험 (이 논문이 MAIC 실험으로 처음 든 문헌 · 자석 · 장 · 시간의 실험 값) | papers/ 에 없음.
- (참고 · 후보로 세지 않음) T. Yokoyama, K. Uehara and M. Naito, The Angmill Mechanofusion system and its applications, Kona 5, 59–68 (1987). (원문 참고 [1]) — wishlist L744 에 같은 권 · 쪽이 chen2004 판 서지 (Toh. Yokoyama · K. Urayama · Toy. Yokoyama) 로 이미 있음 · **두 원문의 공저자가 다르다** (원 Kona 논문으로 확인 필요) · G. Lian, C. Thornton and M. J. Adams, … 'wet' agglomerates, Powder & Grains '97, pp. 159–162 (원문 참고 [12]) — 액교 덩어리라 우선순위 낮음 · J. Chen & C. C. Huang Kona 15 (1997) 113 (참고 [7]) = wishlist L745 · Walton & Braun 1986 (참고 [9]) = `status.tsv` N-72 제외 · Cundall & Strack 1979 (참고 [8]) = wishlist 에 있음.

## 카드 문제
- **`chen2004_mechanofusion_dry_coating_dem_2d_host_scraper_inner_piece_collision_frequency` L50** (§0-1 의도 대조 '의 첫 선례' 행): *"같은 그룹의 MAIC DEM 은 `pfeffer2001` 카드 §⑧ 에 있다 (다른 장치) → 'MF 장치 DEM 으로 정본에서 가장 이른 카드' 까지만 말할 수 있다"* — `pfeffer2001_dry_particle_coating_engineered_particulates` 카드 자신이 §⑧ (L35) 에 *"2D Mechanofusion (호스트만)"* · L148 에 MF 2D DEM (inner piece = 편심 원통 · scraper = 둥근 입자 여럿 · 영역 법선 힘 ≈0.65–1.6 × 10⁻³ N) 을 옮겼다 → 정본에서 MF 장치 DEM 의 가장 이른 카드는 pfeffer2001 (2001) 이고, 그 다음이 이 논문 (2003) · chen2004 (2004) 다.  chen2004 카드는 고치지 않았다.
- 덧붙임 (카드 오류 아님 · 원문끼리 다름): 이 논문 참고 [1] *"T. Yokoyama, K. Uehara and M. Naito … Kona 5, 59–68 (1987)"* ↔ chen2004 참고 [3] *"Toh. Yokoyama, K. Urayama, Toy. Yokoyama, Kona 5 (1987) 59."* — 같은 권 · 첫 쪽에 공저자가 다르다 (wishlist L744 = chen2004 판) · 이 논문 참고 [10] *"O. Walton and R. Braun, Numerical simulation of inclined chute flows in monodisperse, inelastic, frictional spheres, Mech. Mater. 16, 239–246 (1993)"* ↔ 정본 `walton1993_…` 카드 (원문 확인) = 단독 저자 O. R. Walton · *"… flows of monodisperse …"* · 239–247 → 이 논문 쪽 오기로 보임.

## 공백 검사 G1–G4 (★ 이 카드의 핵심 산출 · 카드 §0-2 와 같은 판정)
- **G1 — 점착 대비를 설계 변수로 혼합 결과 (덮임 ↔ 뭉침 · 섞임 ↔ 분리) 를 예측** → **없음** | 근거: 점착 값 0 · 게스트 0 · 혼합 지수 0 (세 장치 모두) · 가장 가까운 문장 = *"The detailed computations, not reported here, indicate that the extent of break-up of an agglomerate is proportional to the relative impact velocity and inversely proportional to the surface energy of the primary guest particles."* (p.469) — 게스트 한 종의 응집이지 host ↔ 게스트 점착 대비가 아니고, 덮임 ↔ 뭉침 예측이 아니며, 계산도 안 보였다 | 좁힐 필요 없음 · 덧붙일 것 = '풀림 ∝ 1/γ_게스트' 는 우리 논지의 SE–SE 응집 쪽과 방향이 같은 정성 진술 (인용은 '방향' 까지).
- **G2 — 점착 입력을 따로 재고 (AFM · IGC · 접촉각 등) 혼합 결과를 미리 예측** → **없음** | 근거: 점착 · 표면 에너지 측정값 0 · MF 입력은 값만 (p.456) · 실험 대조는 정성 서술 (*"at least qualitatively"* p.459 · *"good agreement with well-known experimental observations"* p.467 · 인용 · 그림 없음) | 좁힐 필요 없음.
- **G3 — 회전 속도 최적을 입자 수준 맞교환 (덩어리 풀림 ↔ 벽 부착 손실 등) 으로 설명** → **일부** | 근거: (가) 벽 부착 ↔ 운동 세기의 입자 수준 대조 — 긁개 없음 = *"particles stick to the boundary during processing and their rotation is only rigid body rotation"* (p.457) · 편차 운동 에너지 평균 *"about 2 times"* (p.458 · 판독 1.98) · 원심 · 무점착 · 긁개 유무로 바꿈 (rpm 아님) (나) 덩어리 풀림의 낮은 속도 쪽 한계 = *"when the impact takes place at a very low velocity, the agglomerate does not shatter and even rebounds"* (p.469 · 미보고) (다) rpm 은 세기를 단조로 키울 뿐 (MF 안쪽 조각 힘 ∝ ω^1.98 · Hybridizer 충돌 속도 ∝ rpm^1.01 [판독]) · 최적 · 맞교환 없음 · 공정 쪽 위 한계 = MF 의 열 한 줄 (*"kept under control to prevent burning of the particles"* p.454) | 우리 문장을 이렇게 좁힌다: *"벽 부착이 충돌 세기를 깎는다는 입자 수준 대조 (긁개 유무 · 원심) 와 덩어리 풀림의 낮은 속도 쪽 한계 (되튐) 는 무점착 DEM 개관에 이미 서술돼 있다 (Dave 2003 · Chen 2004) — 우리 몫은 점착 대비가 있는 계에서 rpm 을 축으로 덩어리 풀림 ↔ 벽 점착 손실의 맞교환과 그 최적을 보이는 것"*.
- **G4 — 공정 × 재료 상태도 (회전 세기 × 점착 · Bond 수 등) 가 다른 재료로 옮겨 감** → **없음** | 근거: 상태도 · Bond 수 0 · 재료는 장치마다 하나씩 (이름 없는 1200 kg/m³ host · 'magnesium 흉내' 2500 kg/m³ · 자석) · 재료를 바꾼 계산 없음 | 좁힐 필요 없음.
