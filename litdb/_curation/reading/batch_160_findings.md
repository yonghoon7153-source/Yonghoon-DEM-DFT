# batch 160 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-24 · 후보 표 N-155 · 새 카드)

대상: `chen2004_mechanofusion_dry_coating_dem_2d_host_scraper_inner_piece_collision_frequency` — W. Chen · R.N. Dave · R. Pfeffer · O. Walton, "Numerical simulation of Mechanofusion system", *Powder Technol.* **146** (2004) 121–136 · doi:10.1016/j.powtec.2004.07.014 (원문 첫 쪽 인쇄).
회전 원통 챔버 + 고정 편심 안쪽 조각 (press head) + 고정 긁개로 된 메카노퓨전 건식 코팅 장치를 host 만 (게스트 0) · 점착 없이 2D 소프트 구 DEM (Walton–Braun 부분 걸쇠 스프링 · 증분 미끄럼 마찰) 으로 돌려, 긁개 있음 / 없음의 고리별 회전 · 운동 에너지 · 충돌 압력, 안쪽 조각 힘의 회전 속도 · 채움 의존 (Yokoyama 실험과 멱지수 꼴 대조), 기능 영역 넷의 입자당 힘 · 충돌 속도 · 회전 · 충돌 빈도를 낸 계산 논문.
쪽 = 인쇄 p.121–136 (PDF p.1–16 · 인쇄 = 120 + PDF) · 그림 20 (전부 벡터 · 그림 11b · 13b 는 Yokoyama 재수록) · 표 2 · 번호 식 12 + 번호 없는 Δt 식 · 참고 16 · SI 없음 · 계산 = 2D DEM + 3D 점검 둘 · 실험 0 · 고른 의도 대조 = **일부** (장치 DEM · 2D · Walton–Braun · 점착 없음 · host 만 = 채움 · '첫 선례' = 원문 주장 없음 · '코팅 과정 DEM 의 출발점' = 장치 · host 규모 충돌 통계까지).
인용 서지 (질문 k · l 용): W. Chen, R.N. Dave, R. Pfeffer, O. Walton, *Powder Technol.* **146** (2004) 121–136.
⚠ 글자 층은 그리스 문자 · 첨자 · 수식 기호를 깨뜨린다 ('=' → '¼' · α → 'a' · μ → 'l' · ω → 'x' · Δ → 'D') — 인용문 · 식 · 숫자는 300–400 dpi 렌더로 확인 · 그림 값은 벡터 좌표 판독 (`litdb/figures/<slug>/digitized.csv` 337 행).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (고체전해질 · 압밀 · 기공 없음 — 이름 없는 1.20 g/cm³ host 구의 장치 속 충돌 통계).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 (압밀 · 탈압 없음).  접촉 하나 수준의 되돌림만 있다: Walton–Braun 되돌림 가지 N_u = K2(α − α0) · K2 = K1/e² (e 0.85 → K2 = 27,682 N/m [카드 산술]) · α0 = *"finite plastic deformation"* (식 1–2 · p.123 · 카드 §3-2) — 층 규모 되돌아옴 측정 없음.

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 (기계 물성 0 — 입력 = K1 20,000 N/m (*"selected according to impact mechanics and the condition that the maximum particle deformation is less than 1%"* p.124) · e 0.85 (*"assumed to be independent of the impact velocity for the elastic-plastic case considered here"* p.123) · μ_pp 0.4 · μ_pw 0.5 (표 1) · 재료 이름 · 경도 · 항복 응력 없음.  '탄소성' = 이력 접촉 (K2 > K1 · α0) 이지 항복 값이 아니다 · 카드 §4-2).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (host 한 종 · 압축 없음).  안쪽 조각 힘이 채움 따라 오르다 포화 (그림 12 · 13a · 3000 rpm 7.1 → 9.1 × 10⁻³ N · 800 → 1500 개 [판독]) 는 장치 힘이지 하중 분담이 아니다.

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] chen2004_… | **큰 변형 논의 없음 · 작은 겹침 조건에서만 운동학이 강성에 둔하다** — *"We have observed that under stable conditions, the value of stiffness does not significantly change the kinematics of the results, as long as significant overlap does not occur during collisions"* [10, 11] (p.123–124) · K1 은 최대 변형 < 1 % 로 고름 (p.124) · 그러나 *"The duration of individual collisions and the peak force during a collision is known to be a strong function of the interparticle stiffness (and/or the specific form assumed for the interaction force–displacement relation)."* (p.131) → 순간 힘 · 접촉 시간은 정성 (p.133) | 카드 §3-2 · §4-3 | [인쇄] | 대안 법칙 제시 없음 · 겹침 실측 분포 없음 (평균 법선 힘의 선형 겹침 0.10–0.22 µm = 지름의 0.026–0.055 % [카드 산술]).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 없음).  해상도 비슷한 규칙 하나: 진단 칸 (등부피 고리) 너비 ≥ 최대 입경 → 큰 입자도 한 순간 두 칸까지만 (*"the radial width of each zone is equal or greater than the maximum diameter of particles"* p.125) — DEM 판독 칸 규칙 (우리 Lacey 16×16×4 축 칸 1.26 mm < AM_P parcel 1.363 mm [우리 산술 · 칸 = 외접 상자 등분 가정]).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] chen2004_… | **2D ↔ 3D 점검 둘 (z 주기 · 강체 끝벽 · 두께 10 지름 · 긁개 있음 · 0–1 s)** — 정상 값 (0.6–1.0 s 평균): 운동 세기 2D 32.8 ↔ 3D 주기 33.5 (+2.3 %) · 강체 벽 31.4 (−4.2 %) · 충돌 압력 435 ↔ 481 (+10.6 %) · 508 (+16.7 %) [판독 그림 10 · 카드 산술] · 본문 *"Generally, the differences are not more than about 10%"* (p.130) ↔ 강체 벽 압력 +16.7 % · 2D 근거 = *"The transport of the particle in the third dimension (z-direction) does not play an import role"* (p.124 · 'import' = 원문) | 카드 §3-3 | [판독] · [인쇄] | 3D 점검은 고리 평균 두 양 · 1 s 뿐 — 안쪽 조각 힘 · 충돌 빈도 · 충돌 속도는 2D 만 · 2D 슬랩 힘 (N) 을 실제 장치 힘 (kg) 과 크기 비교하지 않았다.

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 (넘긴 계산 0).  계획 문장만: host 규모 결과를 *"for developing a basis for a full-scale system simulation that may capture the phenomena at multiple length scales"* (p.122) · 게스트 영향은 *"in terms of change in certain properties of the host particles"* (p.122) · *"Future work will focus on … guest-scale modeling"* (p.136) — 다중 규모 사슬의 첫 고리로 자리매김 (FE · MPM 언급 없음).

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] chen2004_… | **가압 · 탈압과 닿는 한계 없음** — 원문이 스스로 남긴 것은 장치 · 계산 쪽: 힘 오차 크기 *"will be explored in a subsequent paper"* (p.124) · *"We plan to include a systematic parametric investigation in a future paper."* (p.124) · *"Although a systematic sensitivity study has not yet been performed to completely verify the robustness of the simulation results"* (p.131) · 게스트 규모 모형 (p.136) | 카드 §11 | [인쇄] | —

## k — DEM 의 한계
- [k] chen2004_… (W. Chen, R.N. Dave, R. Pfeffer, O. Walton, *Powder Technol.* 146, 121–136, 2004) | **말한 것 — 연화 강성 · 게스트 제외 · 2D** — *"It is noted that using small value of stiffness will provide inaccurate results for the contact forces. The significance and magnitude of the error in the force calculations will be explored in a subsequent paper."* (p.124) · *"the spring-stiffness in the force model is chosen to be much smaller than that of a real particle material. While this choice provides reasonable results for the kinematics of the system, the actual values of the instantaneous computed forces are lower, and the contact durations are higher, than would be expected for real particle–particle collisions (with higher effective stiffnesses). The results shown in this section should therefore be considered primarily as qualitative indications of what is happening within the system."* (p.133) · *"Due to the computational limitations, it is impractical to include the fine particles in this modeling effort."* (p.122) · 반대 쪽: *"That time-integral of the force, which controls the kinematics of the flow, is relatively insensitive to the stiffness"* (p.131) | 카드 §4-3 | [인쇄] | 연화 강성의 정당화 = '운동학 · 시간 적분 운동량 전달' 한정 — 우리 압밀 DEM 의 18 배 연화 (E_eff 1.35 GPa · 기공에 맞춘 유효 탄성률) 와 정당화가 다르다 (준정적 압밀 기공은 겹침 ∝ 힘/강성) [카드 추론].

## l — 소성변형이 왜 어려운가 · 우회 · 값 · 비용
- [l] chen2004_… (같은 서지) | **논의 없음 · 우회 = 이력 접촉 법칙 · 비용 = 강성으로 Δt 조절** — 입자 모양 변화 0 · 소성 = Walton–Braun 부분 걸쇠 스프링 (*"a partially latching-spring model proposed by Walton and Braun [9] for an elastic-plastic material"* p.123 · e 0.85 고정) · 비용: *"The CPU time increases as nlog(n) where n is the number of particles."* (p.124) · *"a smaller stiffness value allows a larger time step and a shorter computation time. However, unduly small stiffness causes a time step with unstable simulation results."* (p.123) · Δt = πe√(m/2K1)/40 = 6.69 × 10⁻⁸ s · 10 s = 1.49 × 10⁸ step [카드 산술] | 카드 §3-2 · §4-3 | [인쇄] · [카드 산술] | 실제 계산 시간 · 하드웨어 · 코드 이름 [미확인] · 접선 강성 비 s 값 [미확인].

## m — 받아들일 통찰
- [m] chen2004_… | **코팅 꼴 계산의 판독은 '기능 영역 × 입자당' 으로 결과 전 등록** — 총 누적 충돌은 입력 영역이 최대 (입자–경계 4.4 배 · 입자–입자 7.4 배 · 긁개 영역 대비 [카드 산술] · 본문 *"almost five times"* p.134) 인데 입자당 (식 12) 은 안쪽 조각 ≈ 입력 (1.54e4 · 1.52e4 /s · 표 2) — 인구가 순위를 뒤집는다 (영역 인구 ≈112 · 135 · 338 · 937 [카드 산술]) | 카드 §3-7 · §9-1 | [인쇄] · [카드 산술] | 흐름 밖: Ⓒ · 단계 0 · 2D · 무점착 · 단분산.
- [m] chen2004_… | **벽 부착 몫 = 관측량** — 긁개가 없으면 원심으로 벽에 붙은 층이 챔버와 같이 돌아 (*"particles stick to the boundary during the processing, and undergo mostly rigid body rotation"* p.127) 법선 충돌 속도 평균 0.285 → 0.146 m/s · 긁개 영역 0.424 → 0.071 [판독 그림 16] — 챔버 ω 를 뺀 회전 에너지 (식 8) 처럼 '드럼과 같이 도는 입자 몫' 을 덤프에서 센다 | 카드 §3-4 · §3-6 · §9-2 | [판독] · [인쇄] | 원심 · 무점착 (우리 벽 점착 γ_W/γ_SE 0.00256 과 다른 원인).
- [m] chen2004_… | **순간 힘 대신 시간 적분량 (운동량 전달 · 소산 일 · SI) 을 보고** — 연화 강성에서 순간 힘 · 접촉 시간은 틀리고 시간 적분은 덜 틀린다 (p.131 · p.133) · `kissel2026` · `frankenberg2024` 의 SI 가 같은 쪽 | 카드 §9-3 | [인쇄] | —
- [m] chen2004_… | **장치에서 잴 수 있는 양의 rpm 지수로 DEM 점검** — *"This is a diagnostic quantity that can actually be measured experimentally, and can be used to monitor the system during its operation, and for analyzing power-consumption."* (p.130) · 계산 ∝ ω^1.98 [판독] ↔ 실험 본문 2.1 (재수록 그림 1.70 [판독]) → 우리 코팅 계산이면 축 동력 · 토크 (또는 E_m) 의 rpm 지수를 결과 전 대조 항목으로 | 카드 §3-5 · §9-4 | [판독] · [인쇄] | 지수 꼴만 · 크기 대조 없음.
- [m] chen2004_… | **우리 드럼 덱을 MF 꼴로 돌릴 때의 규모 어림** — 챔버 지름 25 mm ≈ 우리 드럼 25.2 mm · 2000 rpm 1 s = 4.2 × 10⁶ step ≈ 14 h (CGF 151.4 · 100,000 parcel) · 틈 1.6 mm = AM_P parcel 1.2 개 → 틈/AM_P 4 면 CGF 44.4 · 4.0 × 10⁶ parcel · Δt 7.0 × 10⁻⁸ s · 0.1 s ≈ 186 h · B2-U 물성 Hertz 겹침 1 % = 상대 법선 속도 1.17 (SE–SE) – 1.52 m/s (AM_P–AM_P) · 벽 속도 2.62 m/s 충돌이면 1.5–1.9 % | 카드 §7-2 | [카드 산술 · 가정: 비용 ∝ parcel × step · B1-U 25 h 7 m 43 s 비례] | 실제 비용 [미확인] · 막 형성은 DEM 으로 안 보인다 (MPM 단일 충돌 몫).

## n — 논문 에이전트 후보
- [n] Toh. Yokoyama, K. Urayama, Toy. Yokoyama, Kona 5 (1987) 59. (원문 참고 [3]) | ★ m (G2 · G3) — 이 논문의 대조 실험 원전 (안쪽 조각 힘 vs rpm · 채움 · 폴리스티렌 550 g · 탈크 AM-35 · 100 넘는 host/게스트 조합) · 본문 'normal ≈ 2.1 승' ↔ 재수록 그림 1.70 [판독] 의 원 수치 확인 · 실제 장치 크기 · 동력 | papers/ · wishlist 에 없음 (2026-11-24 grep 'Yokoyama' = pfeffer2001 의 다른 서지뿐).
- [n] J. Chen, C.C. Huang, Kona 15 (1997) 113. (원문 참고 [7]) | m — 메카노퓨전의 '작용 구역' 해석 모형 (입자끼리 · 긁개 무시 · 이 논문이 고치려 한 유일한 앞선 이론) — 장치 규모 해석식 (힘 · 동력 ↔ rpm) 이 있으면 우리 결과 전 대조에 쓸 수 있다 | papers/ · wishlist 에 없음.
- [n] Toh. Yokoyama, K. Urayama, Toy. Yokoyama, KONA 1 (1983) 53. (원문 참고 [1]) | m — 메카노퓨전의 기원 (장치 원리 · 1980 년대 중반) | papers/ · wishlist 에 없음.
- [n] A.J. Matchett, T. Yanagida, S. Kobayashi, Powder Technol. 107 (n1/2) (2000) 13. (원문 참고 [12]) | g — 2D 근사 근거 (셋째 방향 무한 · 흐름이 셋째 방향과 무관) | papers/ 에 없음 · wishlist 의 Matchett 은 다른 서지 (Asmar · Langston · Matchett · Walters, 진동 점착 DEM).
- [n] Y. Tsuji, T. Tanaka, T. Ishida, Powder Technol. 71 (1992) 239. (원문 참고 [11]) | k · e — '작은 겹침이면 운동학이 강성에 둔하다' 의 둘째 근거 [10, 11] (첫째 = `walton1993` 카드) · 소프트 구 DEM 의 고전 | papers/ 에 카드 없음 · wishlist 에 없음 · `chung2008_dem_parameters_bulk_behaviour_confined_compression` 의 참고 표에 서지만 있음.
- [n] O.R. Walton, in: M.C. Roco (Ed.), Numerical Simulation of Inelastic, Frictional Particle–Particle Interactions, Particulate Two-Phase Flow, Butterworth-Heinemann, 1993, p. 885. (원문 참고 [15]) | k · m — 입자 압력 (비리얼) 식 · Walton–Braun 법칙 해설서 | papers/ · wishlist 에 없음.
- (참고 · 후보로 세지 않음) O.R. Walton, R. Braun, J. Rheol. 30 (5) (1986) 949. (원문 참고 [9]) — 접촉 법칙 원전 · `status.tsv` N-72 = 제외 (내려받기 불가) · P.A. Cundall, O.D.L. Strack, Geotechnique 29 (1979) 47. (원문 참고 [8]) — wishlist L417 에 이미 있음.

## 카드 문제
없음 — 가리킨 카드 없음 (근거 칸 = 1저자 업로드) · 정본에 이 논문을 인용한 카드도 없음 (papers/ grep 'Mechanofusion system' · 'powtec.2004.07.014' · 'Wenliang' = 0 건 · 이 카드 전).  덧붙임 (정본 카드 오류 아님): `pfeffer2001_dry_particle_coating_engineered_particulates` 의 'MF 외통 200–1600 rpm' (그 카드 L76 · 총설의 장치 서술) 과 이 논문의 계산 1000–4000 rpm 은 다른 진술 (축소 2D 모형의 계산 범위) 이라 모순이 아님 · 이 논문의 참고 [2] 저자 'R.N.D. Wei' 는 이 논문 쪽 오기 (pfeffer2001 원문 저자 = D. Wei).

## 공백 검사 G1–G4 (★ 이 카드의 핵심 산출 · 카드 §0-2 와 같은 판정)
- **G1 — 점착 대비를 설계 변수로 혼합 결과 (덮임 ↔ 뭉침 · 섞임 ↔ 분리) 를 예측** → **없음** | 근거: *"An existing, widely used, cohesionless contact model (Walton–Braun) is used for two-dimensional simulation studies"* (p.121) · 게스트 0 (*"impractical to include the fine particles"* p.122) · host 한 종 단분산 · 혼합 지수 0 — '덮임' 은 결과가 아니라 충돌 통계에서의 추론 (*"powder coating is more likely to occur mainly within the inner-piece and scraper areas where high collisional momentum transfer is occurring"* p.133 · *"most of the coating action should take place in the inner-piece area"* p.135) | 좁힐 필요 없음 · 가져올 것 = '어디서 덮일까' 를 힘 × 빈도 지도로 먼저 정하는 판독 틀.
- **G2 — 점착 입력을 따로 재고 (AFM · IGC · 접촉각 등) 혼합 결과를 미리 예측** → **없음** | 근거: 점착 입력 0 · 입력 대부분 *"selected based on expected empirical values"* (p.124) · 실험과 맞춘 것은 안쪽 조각 힘의 멱지수 하나 (*"no adjustments were made to any of the assumed simulated particle or wall properties in order to obtain this result"* p.131) | 좁힐 필요 없음 · 인용할 선례 = '장치에서 잴 수 있는 양 (안쪽 조각 힘 · 동력) 의 rpm 지수로 DEM 을 점검' (점착 입력으로 혼합 결과를 미리 맞힌 것은 아님).
- **G3 — 회전 속도 최적을 입자 수준 맞교환 (덩어리 풀림 ↔ 벽 부착 손실 등) 으로 설명** → **일부** | 근거: 벽 부착 ↔ 충돌 세기의 입자 수준 대조는 있다 — 긁개 없음: *"more and more particles get attached to the chamber wall because of the centrifugal force"* (p.127) · 법선 충돌 속도 평균 절반 (0.285 → 0.146 m/s [판독]) · 'glancing' 충돌 (p.133) · 덩어리 풀림은 결론의 추론뿐 (*"These collisions are likely to cause deagglomeration of the fine guest particles"* p.136) — 그러나 rpm 은 힘을 단조로 키울 뿐 (∝ ω^≈2 · 최적 없음) · 벽 부착은 rpm 이 아니라 긁개 유무로 바꿈 · 부착 원인 = 원심 (무점착) | 우리 문장을 좁힌다: *"벽 부착 (원심 고정) 이 충돌을 '스치는' 꼴로 바꿔 법선 충돌 세기를 반으로 깎는다는 입자 수준 대조는 무점착 2D DEM 으로 이미 있다 (Chen 2004 · 긁개 유무) — 우리 몫은 점착 대비가 있는 계에서 rpm 을 축으로 덩어리 풀림 ↔ 벽 점착 손실의 맞교환과 최적을 보이는 것"*.
- **G4 — 공정 × 재료 상태도 (회전 세기 × 점착 · Bond 수 등) 가 다른 재료로 옮겨 감** → **없음** | 근거: 재료 하나 (이름 없음 · 1.20 g/cm³) · 상태도 0 · 회전 × 채움의 힘 지도 (그림 12 · 13a) 만 · *"Different values, for example, of the coefficient of friction might have a quantitative effect"* · *"We plan to include a systematic parametric investigation in a future paper."* (p.124) | 좁힐 필요 없음.
