<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 (후보 표 N-154 · 4 순위 · 1저자 11-23 업로드 · 믹서 공정 축) 에서 꼭 뽑으라고 한 항목.
     본 = mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표) · 믹싱 · 드럼 절 구성 = jarray2019_cohesion_driven_mixing_segregation_drum.md · 같은 묶음 이웃 = liu2013_… (§0-2 공백 검사 꼴 · 우리 드럼 대입 절) · khakhar1999_… · chaudhuri2006_… · nase2001_….
     쪽 표기 = 인쇄 쪽 "p.NNN" (Powder Technol. 118 (2001) 251–270 · PDF n 쪽 = 인쇄 p.(250 + n) · figures.json 의 page 와 크롭 이름 txt_p<n> · eq 의 page 는 PDF 쪽).  보충 자료 (SI) 없음 · 표 2 · 그림 16 · 번호 식 54 · 참고문헌 28.
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자 / [판독] = 그림에서 읽은 값 (그림 16 장 · 표 1 은 1-bit 600 dpi 스캔 래스터 — 원본 화소에서 틀 선 검출 + 눈금 글자 = 틀 끝 · 표지 = 검은 화소 무게중심 · 선 = 화소 열의 검은 구간 중심 · 재현 = litdb/figures/<slug>/digitized.csv 132 행) /
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산 (식 · 가정 병기) / [우리 산술] = 원문 밖 값 (우리 덱 · 리포 문서 · 다른 정본 카드) 과 엮은 계산 / [카드 추론] · [카드 해석] · [추정] = 이 카드의 해석 / [미확인] = 원문 20 쪽 전수에 없음.
     ⚠ 글자 층은 수식 · 그리스 문자를 깨뜨린다 ('=' → 's' · '−' → 'y' · '<' → '-' · '(' ')' → 'Ž' '.' · ε → '´' · Θ → 'Q' · ω → 'v' · μ → 'm' · ρ → 'r' · φ → 'w') — 인용한 숫자 · 식은 전부 220–600 dpi 렌더로 확인했다.  시뮬레이션 (DEM · FEM · MPM) 은 이 논문에 없다 (Watanabe 1999 의 DEM 을 인용만). -->
# 회전 원통 속 자유유동 단분산 층의 가로 운동 일곱 꼴 (미끄럼 · 출렁 · 무너짐 · 구름 · 폭포 · 던짐 · 원심) 과 전이 기준식 · Bed Behavior Diagram — 벽 마찰 모멘트 μ_W,c = 2sin³ε sinΘ/[3πf(1+Fr)] (식 23) · 들어올림 ↔ 무너짐 시간 Fr_c = (3/2)[π(Θ0−Θ)/180]²(sinΘ − tan(2Θ−Θ0)cosΘ)/sinε (식 38) · Blumberg Fr·D/d ≈ 2 (식 39) · 반지름 힘 균형 Fr_c = 1/μ_W · sin(Θ+ε−90°) (식 45 · 48) · 1/sin(φ_i+ε−90°) (식 52) · 규사 실험 둘 (미끄럼 임계 충전 0.054 ↔ 측정 0.04–0.06 · 구름 ↔ 폭포 Fr_c·D/d 1.70 → 0.37 [판독]) — 우리 드럼 (Fr 0.0827 · 충전율 0.30) = 폭포 꼴 창 안 [카드 산술] — Mellmann (Powder Technol. 2001)

> slug `mellmann2001_transverse_bed_motion_rotating_cylinders_slumping_rolling_cascading_froude` · DOI `10.1016/S0032-5910(00)00402-2` · type `theory + experiment (analytical force / moment balances on the bed cross-section at unit depth: wall-friction moment with hydrostatic wall pressure + centrifugal term (slipping ↔ cascading) · slump cycle = lifting time vs Coulomb sliding time of a shear wedge (slumping ↔ rolling) · radial force equilibrium / detachment line (cascading ↔ cataracting) · tangential single-particle balance (centrifuging) · empirical Blumberg criterion (rolling ↔ cascading) · own experiments = glass rotating cylinder 4.6 m × 0.3 m with quartz sand (slipping) and glass-front-plate drums D 0.2–0.5 m with quartz sand 0.24–1.0 mm (rolling ↔ cascading) · literature data (Henein 1983, Watanabe 1999 DEM ball mill, ball-mill practice) · free-flowing monodisperse beds, unbaffled cylinders · no cohesion · no simulation of its own)` · PDF `da8a833e-The_transverse_motion_of_solids_in_rotating_cylinders_forms_of_motion_and_transition_behavior.pdf` · digested `2026-11-24` · status ✅
>
> **원제**: *The transverse motion of solids in rotating cylinders—forms of motion and transition behavior* (p.251)
> **저자**: **J. Mellmann** (단독 · 교신) — Institute of Equipment and Environmental Technology, Faculty of Process and Systems Engineering, Otto-von-Guericke-University Magdeburg, P.O. Box 4120, D-39016 Magdeburg, Germany · jochen.mellmann@VST.uni-magdeburg.de (p.251) · *Powder Technology* **118** (2001) **251–270** · 접수 2000-05-16 · 수정본 2000-09-19 · 키워드 *Rotary kiln; Transverse bed motion; Bed behavior; Mathematical model; Critical Froude number; Critical wall friction coefficient* · 첫 쪽 아래 *"PII: S0032-5910(00)00402-2"* (DOI 문자열은 원문에 인쇄되어 있지 않다 — DOI = 10.1016/ + PII · 검색값과 같은 문자열).
> **이웃 카드 (링크만)**: [`khakhar1999_chaotic_mixing_granular_2d_tumbling_mixers_flowing_layer`](khakhar1999_chaotic_mixing_granular_2d_tumbling_mixers_flowing_layer.md) (구름 꼴 흐름층 기구학 · 그 카드 L350 이 Henein 1983 으로 *"우리 Fr 0.083 이 구르기 영역인지"* 를 물었다) · [`liu2013_wet_cohesive_particles_transverse_mixing_rotating_drum_circulation_period`](liu2013_wet_cohesive_particles_transverse_mixing_rotating_drum_circulation_period.md) (액교 점착 × rpm × 충전율 DEM · 같은 충전율 규약 · 구름 영역 가정) · [`chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed`](chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed.md) · [`nase2001_granular_bond_collision_number_wet_cohesion`](nase2001_granular_bond_collision_number_wet_cohesion.md) · [`jarray2019_cohesion_driven_mixing_segregation_drum`](jarray2019_cohesion_driven_mixing_segregation_drum.md) ('cascading regime' 이라 적은 드럼 실험).
> **판독 원자료**: `litdb/figures/mellmann2001_transverse_bed_motion_rotating_cylinders_slumping_rolling_cascading_froude/digitized.csv` (132 행 — 그림 4 측정 표지 17 + 식 38 선 3 · 그림 9 Watanabe 13 · 그림 10 체류 시간 · 누적 충전 18 + 선 2 · 그림 12 동적 안식각 15 + 선 3 · 그림 13 임계 Fr·D/d 10 + 식 39 선 · 그림 14–16 경계 판독 51) · 크롭 **92 장** (그림 16 = 15 다시 자름 + 1 손 크롭 · 표 2 (다시 자름 1 · 손 크롭 1) · 식 54 = 번호 식 전부 · 근거 문단 20) — `figures.json`.
> **이 카드가 서랍에 들어온 이유**: 후보 표 N-154 (1저자 11-23 업로드 · 믹서 논지) — rpm 을 Froude 수로 등록하기 **전에** 우리 드럼 (B 덱 · 39 각형 · Fr 0.0827 · 충전율 0.30) 이 **어느 운동 꼴인지** 를 정하는 지도.

> ★★ **한 줄로 왜 중요한가**: (i) 드럼 운동 꼴의 경계는 **Fr 하나로 정해지지 않는다** — 미끄럼은 충전율 · 벽 마찰이 주 (Fr 영향 작음), 무너짐 ↔ 구름은 정 · 동 안식각 차 (Θ0 − Θ), 구름 ↔ 폭포는 **Fr·D/d** (입자/드럼 지름비), 폭포 ↔ 던짐은 **Θ + ε** (동적 안식각 + 충전각).  (ii) 이 식들에 우리 드럼을 넣으면 Fr 0.0827 · 충전율 0.30 은 **폭포 (cascading · 콩팥 꼴 표면) 꼴 창 안** — 구름 경계의 1.4–7.7 배 위 (식 39 부피 평균 d ↔ 원문 실측) · 던짐 경계 (Θ 30–40°) 의 0.23–0.42 배 · 미끄럼은 유효 벽 마찰 > 0.24–0.36 이면 없음 · 무너짐은 Θ0 − Θ ≳ 21° 일 때만 [카드 산술].  (iii) 그래서 khakhar1999 · liu2013 카드가 우리 드럼에 대입한 **구름 꼴 흐름층 모형 (평평한 표면 · 얇은 층) 의 전제는 우리 Fr 에서 깨져 있을 수 있다** [카드 추론].  (iv) parcel 크기 (CGF 151) 는 d/D 를 151 배 키워 **구름 ↔ 폭포 경계를 우리 운전점 근처로 끌어온다** — Fr 를 맞춰도 꼴은 보존되지 않는다 [카드 산술].
> ⚠ 단 **자유유동 단분산 · 무배플 원통 한정** (점착 · 점착 대비 · 다분산 · 다각형 벽 · 짧은 드럼은 범위 밖) · 해석 모형은 2D 단위 깊이 · 구름 ↔ 폭포 식 (39) 은 경험식이고 저자 자신의 측정이 5–20 배 낮다 · BBD 의 드럼 지름은 미기재 (판독 역산 ≈0.40 m).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 회전 가마 (rotary kiln) 설계를 위해, 무배플 원통 속 자유유동 단분산 층의 가로 운동을 일곱 꼴 (미끄럼 sliding · 출렁 surging · 무너짐 slumping · 구름 rolling · 폭포 cascading · 던짐 cataracting · 원심 centrifuging) 로 나누고 (표 1 — Fr · 충전율 f · 벽 마찰 μ_W 의 '방향 잡이' 범위), 꼴 사이 경계마다 간단한 힘 · 모멘트 모형으로 임계 벽 마찰 계수와 임계 Froude 수를 충전율의 함수로 유도한 뒤 (식 23 · 38 · 39 · 45 · 48 · 52), 직접 한 두 실험 (유리 원통 미끄럼 → 폭포 · 유리 앞판 드럼 구름 → 폭포) 과 문헌 자료 (Henein 1983 무너짐 → 구름 · Watanabe 1999 볼 밀 원심 · 볼 밀 관행) 로 대조하고, 세 재료 (자갈 3.0 · 석회석 1.5 · 모래 0.5 mm) 의 **Bed Behavior Diagram** (위 = Fr vs f · 아래 = μ_W vs f) 을 그렸다 — 규모 늘림 기준 = **Fr · f · μ_W · d/D · φ_i · Θ · Θ0** · 원통 길이 · 기울기는 가로 운동에 무관 (p.269).

| 우리 질문 (지시서 · 꼭 뽑을 것) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 운동 꼴 일곱의 정의 · 범위 | 표 1: 미끄럼 꼴 (sliding f < 0.1 · μ_W < μ_W,c / surging f > 0.1 · μ_W ≥ μ_W,c · 0 < Fr < 10⁻⁴ · '섞임 없음') · 폭포 계열 (slumping 10⁻⁵–10⁻³ · f < 0.1 / rolling 10⁻⁴–10⁻² · f > 0.1 / cascading 10⁻³–10⁻¹ · f > 0.1 · 셋 다 '혼합' · 회전 가마 · 건조기 · 냉각기 · 혼합 드럼) · 던짐 계열 (cataracting 0.1–1 '분쇄' 볼 밀 / centrifuging Fr ≥ 1 · f > 0.2) — *"orientation values and are dependent on the particular bed material used"* | [인쇄] p.252 표 1 · §3-1 |
| ② ★ 경계식 (Fr · 충전율 · 벽 마찰 · d/D · 내부 마찰각 · 정 · 동 안식각) | 미끄럼 ↔ 폭포 **μ_W,c = 2sin³ε sinΘ / [3πf(1 + Fr)]** (식 23) · 무너짐 ↔ 구름 **Fr_c = (3/2)[π(Θ0 − Θ)/180]²[sinΘ − tan(2Θ − Θ0)cosΘ]/sinε** (식 38) · 구름 ↔ 폭포 **Fr·(D/d) ≈ 2** (식 39 · Blumberg 경험식) · 폭포 ↔ 던짐 **Fr_c = 1/μ_W** (낮은 충전 Θ + ε < 90° · 식 45) · **Fr_c = sin(Θ + ε − 90°)** (높은 충전 · 식 48) · 던짐 ↔ 원심 **Fr_c = 1/sin(φ_i + ε − 90°)** (식 52) · 고리 최소 충전 **f_min = 1 − [1 − 2(d/D)]²** (식 53) · f(ε) = (ε − sinε cosε)/π (식 1) | [인쇄] p.253–263 · §3-2–3-7 |
| ③ ★ Bed Behavior Diagram 숫자 | 세 재료 (표 2 의 d · Θ · Θ0 · μ_W 0.675 공통) — f 0.30 에서 무너짐 ↔ 구름 3.3 × 10⁻⁴ (자갈) · 5.9 × 10⁻⁵ (석회석) · 1.7 × 10⁻⁵ (모래) · 구름 ↔ 폭포 0.015 · 0.0076 · 0.0025 · 폭포 ↔ 던짐 0.33 · 0.31 · 0.25 · 던짐 ↔ 원심 ≈3.2 · 3.5 · 4.4 · 아래 패널 μ_W,c 0.37 · 0.36 · 0.37 · 계단 (Θ + ε = 90°) f 0.14 · 0.15 · 0.18 [판독 · 식으로 검산] · 드럼 지름 미기재 → 식 39 수준에서 **D ≈ 0.40 m** [카드 산술] · ⚠ 모래 아래 패널은 Θ ≈ 37.5° 꼴 (표 2 모래 32.5° 아님) [판독] | §3-8 |
| ④ 검증 실험 (드럼 크기 · 재료) | 4.1 **유리 원통 L 4.6 m · D 0.3 m · 규사 d 0.27 mm · Θ 32.4°** — 체류 시간 꺾임 Du ≈ 0.009 · 임계 충전 0.04 < F_c < 0.06 ↔ Jenike 벽 마찰 (< 2 kPa) φ_W 22.7–26.5° → μ_W 0.47 → 식 23 f_c **0.054** (Henein 판 0.165) · 4.2 **유리 앞판 드럼 D 200 · 300 · 500 mm · 규사 d50 0.24 · 0.5 · 0.75 · 1.0 mm · n 0.5–10 min⁻¹ · f 0.05–0.25 · L/D > 0.3** — 앞판 n_c ≈ 2 ↔ 가운데 3.3 min⁻¹ (D 200 · d 0.24 · f 0.1) · 전이 Fr 10⁻⁴–10⁻² · *"The cylinder diameter had no influence."* · 나머지 전이 = 문헌 자료 | [인쇄] p.264–265 · §3-3 · §3-5 |
| ⑤ 규모 늘림 기준 | *"scaling criteria … Froude number, filling degree, coefficient of wall friction, internal frictional coefficient, dynamic and static angle of repose as well as the ratio of particle to rotating cylinder diameter"* · 길이 · 기울기는 가로 운동 무관 → *"experimental studies on transverse motion behavior can be conducted batchwise in a horizontal rotating drum"* · Fr = ω²R/g = (n/n_c)² · n_c ≈ 42.3/√D | [인쇄] p.251 · p.254 · p.269 · §3-9 |
| ⑥ ★ 우리 드럼은 어느 꼴인가 | **폭포 (cascading) 꼴** [카드 산술 · 범위 밖 외삽] — 표 1 띠 10⁻³–10⁻¹ 안 · 구름 ↔ 폭포: 식 39 Fr_c = 0.012 (SE parcel) · 0.048 (AM_S) · **0.108 (AM_P)** · 0.024 (d32) · 0.058 (부피 평균) → 우리 = 6.9 · 1.7 · **0.76** · 3.4 · 1.4 배 / 원문 자신의 측정 (그림 13 · f 0.26 · 가운데 0.371 [판독]) 이면 Fr_c 0.0022–0.020 → 4.1–37 배 위 · 폭포 ↔ 던짐 (식 48 · f 0.30): Θ 25 · 30 · 35 · 40° → 0.111 · 0.197 · 0.282 · 0.364 → 우리 = 0.75 · 0.42 · 0.29 · 0.23 배 (Θ ≥ 23.4° 이면 던짐 아래) · 미끄럼 (식 23): μ_W,c 0.235–0.357 · 무너짐 (식 38): Θ0 − Θ ≥ 21.2–21.6° 일 때만 | §3-10 |
| ⑦ '점착 비 기준' · 코팅 DEM | **없음** — *"restricted to unbaffled rotating cylinders and free-flowing monodisperse particle beds"* (p.252) · 점착 언급은 Lehmberg 의 *"slightly sticky soda particles"* (Fr 효과 예시 · p.256) 하나 | §0-2 |
| ⑧ DEM 한계 · 소성 · 2D/3D · 탈압 | DEM 한계 **말 없음** (DEM 은 Watanabe 의 *"linear–spring–dashpot"* 볼 밀 계산이 실험과 *"good correspondence"* 라고 인용만) · 소성 **논의 없음** · 모형 = 2D 단위 깊이 단면 · 3D 증거 = 앞판 ↔ 가운데 전이 차 (*"pulling effect of the side walls"*) · 탈압 해당 없음 | §4-3 |
| ⑨ 절대값 전이 | **안 된다** (재료 · 크기 · 점착 · 벽 · 드럼 꼴이 다르다) — 옮길 것 = **꼴 판정의 틀 (식 · 측정할 흐름 물성)** · **경계가 Fr 하나가 아니라는 사실** · 규모 늘림 기준 목록 | §7 · §8 |

⛔ **한정어 (떼지 말 것)**: ① **자유유동 · 단분산 · 무배플 원통** 한정 (점착 · 다분산 · 배플 · 다각형 벽 밖) ② 표 1 범위는 **방향 잡이 값** (재료 따라 움직임) ③ 경계식은 **2D 단위 깊이** 힘 · 모멘트 모형 (끝벽 무시) — 벽 압력은 정수압 가정 (Janssen 대비 ≈12 % 높음) ④ 구름 ↔ 폭포 식 (39) 은 **경험식** · 저자 자신의 측정 (그림 13) 이 그 값 2 보다 1.2–5.4 배 (가운데) · 2.4–22 배 (앞판) 낮다 [판독] — 그런데도 BBD 는 식 39 로 그렸다 ⑤ 무너짐 ↔ 구름 식 (38) 은 Θ0 1° 오차에 Fr 3–6 배 (저자) ⑥ BBD 의 D · φ_i 는 원문 미기재 [미확인] · μ_W 는 세 재료 모두 0.675 (모래 · 소결대 가마 값) ⑦ 우리 드럼 꼴 판정은 **원문 식에 우리 값을 넣은 카드 산술** (원문 범위 밖 외삽 · 덤프 측정 전).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-154 의 '왜' 칸)

의도 원문: *"드럼 운동 꼴 (미끄럼 · 출렁 · 무너짐 · 구름 · 폭포 · 던짐 · 원심) 경계를 Froude 수 · 충전율 · 벽 마찰로 가르는 지도 = rpm 축을 무차원으로 정하는 기준 · 우리 드럼이 어느 꼴인지"* · 근거 칸 = *"1저자 11-23 업로드 (메인 세션 검색 제안 → 1저자 PDF)"* → **가리킨 카드 없음** (2 차 인용 대조 대상 없음) · 지시서 덧붙임 (꼭 뽑을 것 = 꼴마다 경계식 · BBD 숫자 · 검증 실험 · 규모 늘림 기준 · 우리 드럼의 자리 / 우리 질문 = '점착 비 기준' · rpm 공정 축 · 코팅 DEM / 공백 검사 G1–G4).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "드럼 운동 꼴 (미끄럼 · 출렁 · 무너짐 · 구름 · 폭포 · 던짐 · 원심)" | **채움** | 표 1 (p.252) 의 일곱 하위 꼴 = sliding · surging · slumping · rolling · cascading · cataracting · centrifuging + 세 기본 꼴 (slipping · cascading ("tumbling") · cataracting motion) · 본문 2.1–2.3 절 정의 (p.252–253) |
| "경계를 Froude 수 · 충전율 · 벽 마찰로 가르는" | **채움 (한정)** | 표 1 의 Fr · f · μ_W 칸 (*"orientation values … dependent on the particular bed material used"*) + 경계식 6 개 — 그러나 경계식에는 **Θ · Θ0 · φ_i · d/D** 도 들어간다: 미끄럼은 *"the filling degree is the main variable … the Froude number, for slow rotation, exerts an admittedly low influence"* (p.256) · 구름 ↔ 폭포는 Fr·D/d (식 39) · 무너짐 ↔ 구름은 Θ0 − Θ (식 38) |
| "지도" | **채움** | Bed Behavior Diagram 그림 14 · 15 · 16 (자갈 · 석회석 · 모래) — 위 = Fr (10⁻⁵–10) vs f (0–0.5) · 아래 = μ_W vs f · 기준식 목록 p.266 · Henein 측정 대조 (석회석만 어긋남 p.267) · ⚠ 드럼 지름 · φ_i 미기재 · 모래 아래 패널은 Θ ≈ 37.5° 꼴 [판독 §3-8] |
| "= rpm 축을 무차원으로 정하는 기준" | **채움 (한정)** | Fr = ω²R/g (식 3 · R = 원통 **안 반지름** · *"peripheral Froude number"*) = (n/n_c)² · n_c = (30/π)√(g/R) ≈ 42.3/√D (식 4 · D [m]) — 한정: 꼴은 Fr 만으로 정해지지 않는다 (위 줄) · 규모 늘림 기준 7 개 (p.269) |
| "우리 드럼이 어느 꼴인지" | **원문 없음 → 카드 산술로 채움** | §3-10: 폭포 (cascading) 꼴 창 안 — 원문 식에 우리 덱 값을 넣은 외삽 (점착 · 다분산 · 39 각형 · L/D 0.20 · 끝판 회전 = 원문 범위 밖) |
| (꼭 뽑을 것) 꼴마다 경계식 | **채움** | 식 23 · 36/38 · 39 · 45 · 48 · 50–52 · 53 (§3-3–3-7 · 식 크롭 54 장) |
| (꼭 뽑을 것) BBD 숫자 (그림 판독) | **채움 (판독)** | §3-8 표 · digitized.csv — 판독이 식 재계산과 2–6 % 안에서 맞음 (모래 아래 패널 제외) |
| (꼭 뽑을 것) 검증 실험 (드럼 크기 · 재료) | **채움** | 4.1 · 4.2 (p.264–265) — 두 전이만 직접 실험 · 나머지는 문헌 자료 (*"For all other transitions, data researched from the literature have been used"* p.252) |
| (꼭 뽑을 것) 규모 늘림 기준 | **채움** | 초록 · 요약 (p.251 · p.269) |
| (우리 질문) '점착 비 기준' (γ_AM/γ_SE · 같은 SE 탐침 AFM 힘 비) | **없음** | 자유유동 한정 · 점착 대비 0 |
| (우리 질문) 회전 속도 (rpm) 공정 축 | **일부** | 꼴 경계 (무차원 Fr · Fr·D/d) 와 꼴마다 성격 (표 1: 혼합 · 분쇄) 은 채움 · 혼합 최적 rpm · 점착 계의 rpm 효과는 없음 |
| (우리 질문) 코팅 과정 DEM | **없음** | — |
| 가리킨 카드의 2 차 인용 값 | **해당 없음** | 근거 칸 = 1저자 업로드 · 정본 카드 가운데 이 논문을 인용한 카드 없음 (papers/ 전수 grep 'Mellmann' · 'transverse motion of solids' · 'S0032-5910(00)00402' = 0 건) |
| (덧붙임) 이 논문의 인용 ↔ 정본 카드의 같은 원전 인용 | **서지가 다름 (두 건)** | Henein 1983 = 이 논문 *"Metall. Trans. B 14B (3) (1983) 191–220"* ↔ `khakhar1999` 카드 L350 (그 논문 [14]) *"Metall. Trans. B 14, 191–197 (1983)"* · Metcalfe 1995 = 이 논문 *"Avalanche mixing of granular solids"* ↔ `khakhar1999` 쪽 *"… granular materials"* — 어느 쪽이 맞는지 [미확인] (두 논문의 참고문헌이 서로 다르게 적었다 · 카드 오류 아님) |

⇒ **의도 대조 결과: 채움 (한정 둘)** — 일곱 꼴 · 경계식 · 지도 (BBD) · Fr 무차원화는 원문이 채운다; 한정 ① 꼴 경계는 Fr 하나가 아니라 흐름 물성 (Θ · Θ0 · μ_W · φ_i) 과 d/D 에 따라 움직인다 ② '우리 드럼이 어느 꼴인지' 는 원문 식에 우리 값을 넣은 카드 산술 (원문 범위 밖) — 결과 = 폭포 꼴 창 안.  우리 '점착 비' · 코팅 DEM 은 **없음**.

---

## 0-2. ★ 공백 검사 G1–G4 — 우리 믹서 논지 문장을 이 논문이 이미 했나 (정독 출력 batch_159 끝 절과 같은 판정)

| # | 우리 공백 문장 (11-23 지시) | 판정 | 근거 (쪽 · 문장) | 반례 · 일부면 우리 문장을 이렇게 좁힌다 |
|---|---|---|---|---|
| **G1** | 점착 대비를 설계 변수로 혼합 결과 (덮임 ↔ 뭉침 · 섞임 ↔ 분리) 를 예측 | **없음** | *"This study is restricted to unbaffled rotating cylinders and free-flowing monodisperse particle beds."* (p.252) · 혼합 서술은 꼴마다 정성 (표 1 '혼합' · *"No particle mixing takes place in slipping motion"* p.253 · 무너짐 = *"smaller solids mixing"* p.256 · 구름 = *"uniform, good intermixing"* · *"When particle size distribution is very broad, segregation can appear"* p.253) · 점착 낱말은 Lehmberg 의 *"slightly sticky soda particles"* (p.256 · 미끄럼 → 폭포가 Fr > 6.9 × 10⁻⁴ 에서 — 점착의 역할은 말하지 않음) 하나 | 좁힐 필요 없음.  가져올 것 = **운동 꼴을 점착 대비 효과를 읽기 전에 고정할 배경 변수로** — 같은 꼴 안 팔끼리만 대비 효과를 견준다 (꼴이 바뀌면 혼합 성격 자체가 바뀐다 · 표 1) |
| **G2** | 점착 입력을 따로 재고 (AFM · IGC · 접촉각 등) 혼합 결과를 미리 예측 | **없음 (방법 꼴만 선례)** | 점착 입력 0 · 혼합 결과 예측 0.  다만 **따로 잰 흐름 물성 → 운동 꼴 사전 예측 → 실험 대조** 의 꼴은 있다: Jenike 벽 마찰 (*"at low static pressures less than 2 kPa"* · φ_W 22.7–26.5° → μ_W 0.47) 로 식 23 이 임계 충전 0.054 를 내고 체류 시간 꺾임 (0.04–0.06) 과 맞음 (p.264) · *"provides the user of rotary kilns the possibility to estimate the type of motion of the bed materials used from measured particle characteristics"* (p.251) | 좁힐 필요 없음.  인용할 선례 문장 = *"운동 꼴 수준에서는 따로 잰 흐름 물성 (벽 마찰 · 안식각) 으로 꼴 전이를 미리 맞힌 선례 (Mellmann 2001) 가 있다 — 우리 몫은 점착 입력 (W · 같은 탐침 비) 으로 혼합 결과 (덮임 · 뭉침) 를 미리 맞히는 것"* |
| **G3** | 회전 속도 최적을 입자 수준 맞교환 (덩어리 풀림 ↔ 벽 부착 손실 등) 으로 설명 | **일부** | rpm 경계를 **층 · 입자 힘 균형**으로 설명한다: 원심력이 벽 수직력을 키워 벽 마찰 모멘트 ∝ (1 + Fr) (식 13 · 20–21 · 미끄럼 억제) · 들어올림 시간 ∝ 1/ω ↔ 무너짐 시간 (Coulomb 미끄럼) (식 24 · 34–35) · 반지름 힘 균형이 깨지면 이탈 (식 40–48) · 원심력이 벽에 붙잡음 (*"adhesion of a particle on the drum wall"* = 원심 고정 · 점착력 아님 · p.262) · 꼴마다 성격 (표 1: 혼합 ↔ 분쇄) — 그러나 **최적 rpm · 점착 · 덩어리 풀림 · 벽 점착 손실의 맞교환은 없다** | 우리 문장을 이렇게 좁힌다: *"회전 세기에 따른 운동 꼴 경계는 무점착 층의 힘 · 모멘트 균형으로 이미 설명됐다 (Mellmann 2001) — 우리 몫은 점착 대비 계에서 **한 꼴 안의** 최적 rpm 을 덩어리 크기 · 벽 접촉 몫 · 미끄럼 (덤프 관측량) 으로 입자 수준에서 보이고, 꼴 경계를 넘는 팔 (던짐 = 충격 · 분쇄) 은 따로 표지하는 것"* |
| **G4** | 공정 × 재료 상태도 (회전 세기 × 점착 · Bond 수 등) 가 다른 재료로 옮겨 감 | **일부 (반례에 가까움)** | BBD = **공정 (Fr · f) × 재료 흐름 물성 (μ_W · Θ · Θ0 · φ_i · d/D)** 상태도를 세 재료에 같은 식으로 계산하고 Henein 측정과 대조 (*"With the exception of limestone, the predicted boundaries are in agreement with the data"* p.267) · 흐름성이 좋을수록 경계가 1–2 자릿수 낮은 Fr 로 이동 (p.267) · 규모 늘림 기준 목록 (p.269) → **재료 간 이전의 틀은 이미 있다** · 없는 것 = 점착 (Bond · Co) 축 · 점착 대비 · 다분산 (*"free-flowing monodisperse"*) | 우리 문장을 이렇게 좁힌다: *"무점착 자유유동 층의 공정 (Fr · f) × 흐름 물성 상태도와 그 재료 간 이전은 선례 (Mellmann 2001 BBD) 가 있다 — 우리 공백은 **점착 세기 · 점착 대비를 축으로 넣은** 상태도가 다른 재료로 옮겨지는지"* · 연결 고리 제안 = 점착 → 흐름 물성 (Θ · Θ0 · 유효 μ_W 를 덤프에서) → 운동 꼴 (Mellmann 식) [카드 추론] |

---

## 1. 한 줄 요약
**회전 원통 (무배플) 속 자유유동 단분산 층의 가로 운동 일곱 꼴을 정리하고, 꼴 경계마다 단순 힘 · 모멘트 모형으로 임계 벽 마찰 · 임계 Froude 수를 충전율의 함수로 유도해 두 실험 (규사 · 유리 원통) 과 문헌 자료로 맞춘 뒤 Bed Behavior Diagram 으로 묶은 20 쪽 해석 · 실험 논문.**  미끄럼은 충전율 · 벽 마찰이 정하고 (식 23 · Fr 영향 작음), 폭포 계열 · 던짐 계열은 Fr · 충전율 · 흐름 물성 (Θ · Θ0 · φ_i · d/D) 이 정한다 — 구름 ↔ 폭포만 맞는 모형이 없어 경험식 Fr·D/d ≈ 2 를 쓴다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **J. Mellmann** (Otto-von-Guericke-Universität Magdeburg · 단독) | *Powder Technol.* 118 (2001) 251–270 · 20 쪽 | 10.1016/S0032-5910(00)00402-2 (원문 = PII 인쇄) | 자유유동 단분산 입자층 — 규사 (d 0.24–1.0 · 0.27 mm) · 자갈 3.0 · 석회석 1.5 · 모래 0.5 mm (표 2 · 앞 둘은 Henein [6] 값) · 볼 밀 장입물 (문헌) · SE · AM · 전극 재료 없음 | **이론 (해석 힘 · 모멘트 모형) + 실험 (전이 관찰 2 종) + 문헌 자료 대조** (시뮬레이션 0 · 압밀 0) |

- **1저자 메모와의 대조**: 저자 · 제목 · 학술지 · 권 118 · 쪽 251–270 · 2001 — **같다**.  DOI 는 원문에 문자열로 인쇄되어 있지 않고 첫 쪽에 **PII S0032-5910(00)00402-2** 만 있다 (PDF 메타 제목도 같은 PII) — 검색한 DOI 10.1016/S0032-5910(00)00402-2 는 그 PII 와 같은 문자열 (Elsevier 관례) 이다.
- **글의 꼴**: 1. 서론 (회전 가마 열전달 · 'cold core' · 목표 = 꼴 경계의 간단한 식) → 2. 꼴 일곱 (표 1) → 3. 전이 (3.1 기본 계산 · 3.2 미끄럼 ↔ 폭포 · 3.3 폭포 계열 안 (무너짐 ↔ 구름 · 구름 ↔ 폭포) · 3.4 폭포 ↔ 던짐 · 3.5 던짐 ↔ 원심) → 4. 실험 (4.1 · 4.2) → 5. BBD → 6. 요약 → 기호표 → 참고문헌 28 (독일어 학위논문 · 보고서 다수).
- **계보**: Henein · Brimacombe · Watkinson 1983 (BBD 의 원형 · 무너짐 ↔ 구름 측정 · 미끄럼 판정식) · Cross 1979 (축 둘레 모멘트 균형 — 이 논문이 원심력을 더해 확장) · Blumberg 1995 (식 39) · Davis 1919 (반지름 힘 균형 · 이탈선) · Teubner 1977 (단일 입자 원심) · Watanabe 1999 (볼 밀 DEM · 원심) · Rutgers 1965 (Fr 경계 값) · 저자 학위논문 1989 [7] (폭포 운동 모형).

---

## 3. 핵심 수치 · 식 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 운동 꼴 일곱 — 표 1 (p.252 · `tab_1.png`) 과 정의 (p.252–253 · `txt_p2_scope_…` · `txt_p3_slumping_rolling_cascading_…`)
| 기본 꼴 | 미끄럼 (slipping) | | 폭포 계열 (cascading "tumbling") | | | 던짐 계열 (cataracting) | |
|---|---|---|---|---|---|---|---|
| 하위 꼴 | sliding (미끄럼) | surging (출렁) | slumping (무너짐) | rolling (구름) | cascading (폭포) | cataracting (던짐) | centrifuging (원심) |
| 물리 과정 | 미끄럼 | ← | **혼합** | ← | ← | 분쇄 (crushing) | 원심 |
| Froude 수 | **0 < Fr < 10⁻⁴** | ← | **10⁻⁵ < Fr < 10⁻³** | **10⁻⁴ < Fr < 10⁻²** | **10⁻³ < Fr < 10⁻¹** | **0.1 < Fr < 1** | **Fr ≥ 1** |
| 충전율 f | f < 0.1 | f > 0.1 | f < 0.1 | f > 0.1 | ← | f > 0.2 | ← |
| 벽 마찰 μ_W | μ_W < μ_W,c | μ_W ≥ μ_W,c | μ_W > μ_W,c | ← | ← | μ_W > μ_W,c | ← |
| 쓰임 | 쓰지 않음 | ← | 회전 가마 · 반응기 · 회전 건조기 · 냉각기 · **혼합 드럼** | ← | ← | 볼 밀 | 쓰지 않음 |
[인쇄 · 표 1 래스터 · ← = 왼쪽 칸과 합친 칸]

- 범위의 지위: *"To delimit the types of bed motion, the ranges for Froude number and filling degree are specified, which, however, represent orientation values and are dependent on the particular bed material used."* (p.252) — 하위 꼴 Fr 범위가 서로 겹친다 (무너짐 10⁻⁵–10⁻³ ↔ 구름 10⁻⁴–10⁻² ↔ 폭포 10⁻³–10⁻¹).
- **미끄럼 꼴** (p.252–253): 벽이 아주 매끄러우면 sliding (층이 작은 기울기로 쉬고 원통이 그 밑에서 돈다 · Rutgers: 높은 rpm · 충전에서도 *"standing state"*) → 벽 마찰이 늘면 surging (정지 마찰 ↔ 운동 마찰이 번갈아 · 층이 벽에 붙어 오르다 통째로 미끄러져 내림) · *"No particle mixing takes place in slipping motion."* · 거친 벽 · 벽에 단 막대로 막는다.
- **폭포 계열** (p.253): **무너짐** = 저속에서 층이 벽과 강체 회전으로 들려 표면 사태로 되풀이 평탄화 · 사태 빈도 = rpm · 입경 · 원통 지름의 함수 [6,10] · Metcalfe [21]: *"intermixing decreases as the filling degree increases to virtually vanish at f≈0.5"* → **구름** = 표면 얇은 층 (cascading layer) 이 꾸준히 흐르고 대부분 (plug flow region) 은 벽과 강체 회전 · 표면 거의 평평 · 동적 안식각은 rpm · 충전율에 약하게 의존 · *"This type of motion makes a uniform, good intermixing possible. When particle size distribution is very broad, segregation can appear."* → **폭포** = 표면이 휘기 시작 (콩팥 꼴 · *"kidney-shaped bed"* · 휨 높이는 rpm 따라 커짐) · *"The transition to cascading is also dependent on particle size [8]."* · 회전 가마는 대개 폭포 계열 · 그 가운데 구름이 선호.
- **던짐 계열** (p.253): 던짐 = 입자가 층에서 떨어져 기체 공간으로 던져짐 · rpm 이 오르면 던지는 입자 수 · 궤적이 커져 지름을 따라 고른 장막 → 원심 = 바깥 궤도 (r ≈ R) 입자부터 벽에 붙음 · 전체가 고른 막이 되는 것은 아주 높은 rpm 에서만 근사로.  회전 가마에는 무관.

### 3-2. 기본 기하 · Froude 수 (식 1–4 · p.253–254 · 그림 1 · `eq_01`–`eq_04` · `txt_p4_peripheral_froude_critical_speed.png`)
| 식 | 내용 | 표지 |
|---|---|---|
| (1) | **f = (ε − sinε cosε)/π** — 충전율 = 단면에서 층이 차지하는 몫 · ε = 충전각 (층 원호의 반각) · 평평한 표면 가정 | [인쇄] p.253 |
| (본문) | r0 = R cosε (축 ↔ 표면) · 현 s = 2R sinε · 가운데 깊이 h = R − r0 | [인쇄] p.253–254 |
| (2) | r_S = 2sin³ε R/(3πf) — 균질 층의 무게중심 반지름 (원 활꼴의 도심) | [인쇄] p.254 |
| (3) | **Fr = ω²R/g** — *"The centrifugal force is related to the inner radius of the cylinder so that this criterion is also named the peripheral Froude number"* | [인쇄] p.254 |
| (4) | **n_c = (30/π)√(g/R) ≈ 42.3/√D** (n [min⁻¹] · D [m]) — 바깥 궤도 입자가 위 사점에서 원심 (Fr = 1) · *"Hence, the Froude number can also be expressed as Fr = (n/n_c)²"* · 볼 밀은 rpm 을 n_c 의 % 로 적는다 | [인쇄] p.254 |
- [카드 산술 · 식 1 역풀이] f → ε: 0.04 → 33.6° · 0.054 → 37.4° · 0.10 → 46.6° · 0.175 → 57.5° · 0.20 → 60.5° · 0.25 → 66.2° · **0.28 → 69.3° · 0.30 → 71.4° · 0.32 → 73.3°** · 0.40 → 80.9° · 0.50 → 90.0°.

### 3-3. ★ 미끄럼 ↔ 폭포 — 축 둘레 모멘트 균형 (식 5–23 · p.254–256 · 그림 1 · 2 · 11 · 실험 4.1 · `eq_05`–`eq_23` · `txt_p5_…` · `txt_p6_filling_degree_…` · `txt_p6_fig2_range_…` · `txt_p14_*`)
- **선행 값** (p.254): Reuter [4] 실험 *"0 < Fr < 10⁻³"* · 저자 학위논문 모형 [7] Fr ≈ 10⁻⁴ · Rutgers [3] Fr = 10⁻² — *"However, as will be shown the filling degree is the main variable influencing the transition slipping motion–cascading motion, not the Froude number."*
- **모형** (단위 깊이 단면 · 층이 δ 만큼 기울어 있음 · Cross [5] 의 모멘트 균형에 원심력을 더함): 조건 **M2 > M1** (식 5 · 벽 마찰 모멘트가 짐 모멘트를 넘으면 강체 회전 = 폭포 계열 — 무너짐 · 구름은 아직 가르지 않음).
  - 짐 모멘트: M1 = F_g l1 = Mgl1 (6) · l1 = r_S sinδ (7) · m = ρ_b f π R² L (8) · 단위 길이 질량 M = ρ_b R²(ε − sinε cosε) (9) → **M1 = (2/3)ρ_b g R³ sin³ε sinδ** (10).
  - 벽 마찰 모멘트: M2 = F_F l2 (11 · l2 = R) · Coulomb F_F = μ_W F_N (12 · μ_W = tanφ_W = 층 전체에 걸친 '유효' 층/벽 마찰 계수) · F_N = F_G cosκ + F_C (13) · 중력 몫 ∝ 깊이 AE (14 · ⚠ 인쇄는 **ρ_g** — 다른 식은 ρ_b · §3-11) · 원심 몫 ∝ 길이 AB (15) · 면적당 f_F = μ_W ρ_b [g h1 cosκ + ω² h2 (R + r0,x)/2] (16) · dF_F = f_F R dκ (17 · 18) · κ = δ − ε … δ + ε 적분 (19) → **F_F = μ_W ρ_b g R² (1 + Fr)(ε − sinε cosε)** (20) → **M2 = μ_W ρ_b g R³ (1 + Fr)(ε − sinε cosε)** (21).
  - 벽 압력 가정: *"In this study the material is assumed to follow hydrostatics with a linear increase of the compressive force over the height. For comparison taking the physical characteristics of cement [26], this approach calculates about 12% higher vertical pressures than Janssen's formula."* (p.255)
  - 판정: **μ_W > 2sin³ε sinδ / [3(1 + Fr)(ε − sinε cosε)]** (22) · 폭포 계열에서 δ = Θ (동적 안식각) → **μ_W,c = 2sin³ε sinΘ / [3πf(1 + Fr)]** (23) · Fr ≪ 1 이면 Cross [5] 판정과 같다 · f → 0 이면 최대 **μ_W = sinΘ** (p.256).
- **저자 해석** (p.256): *"As Eq. (23) makes clear for given material properties, the filling degree is the main variable affecting the transition to cascading motion whereas the Froude number, for slow rotation, exerts an admittedly low influence."* · 막기 = 벽 거칠기 (막대) · 충전율 ↑ · Fr ↑ · Korotich [9] 유리 원통 + 규사: 충전율 ↑ → 미끄럼 → 폭포 (값 미기재) · **Lehmberg [15]: *"slightly sticky soda particles"* · 무배플 강철관 0.31 m · Fr > 6.9 × 10⁻⁴ 에서 미끄럼 → 폭포** (충전율 미기재) [카드 산술: 0.31 m 관에서 Fr 6.9 × 10⁻⁴ = 2.0 rpm] · 볼 밀은 미끄럼 보상으로 임계 속도의 +5 % [27].
- **그림 2** (Fr ≪ 1 · Θ 25–40° · f 0–0.5): f 0 에서 sinΘ (0.42 · 0.50 · 0.57 · 0.64) · f 0.5 에서 ≈0.18 · 0.21 · 0.24 · 0.27 [판독] = 식 23 (f 0.5 → 0.4244 sinΘ = 0.179 · 0.212 · 0.243 · 0.273 [카드 산술]) · *"critical conditions for the occurrence of slipping motion are only to be expected at low filling degrees"* (p.256).
- **실험 4.1** (p.264 · 그림 10 · 11): 체류 시간 연구의 부산물 — **유리 원통 L 4.6 m · D 0.3 m · 규사 d 0.27 mm · Θ 32.4°** · 투명 벽으로 축 방향 충전율을 재 체류 시간 계산 · 질량 유량을 늘리면 체류 시간이 줄다가 꺾이고 다시 약간 증가 · 낮은 충전에서 층 전체가 미끄럼 → 꺾임 뒤 폭포.
  - 무차원 질량 유량 **Du = ṁ_s/(ρ_b ω R³)** (54) · 꺾임 **Du ≈ 0.009** [인쇄] (판독 0.0091) · *"The critical filling degree at the breaking point amounts to 0.04 < F_c < 0.06."* [인쇄] · 그림 10 판독: 미끄럼 쪽 마지막 점 F 0.034 (Du 0.0079) → 폭포 쪽 첫 점 0.062 (Du 0.0104) · F_c 점선 ≈0.048 · ωT·D/L 29.3–31.4 (미끄럼) → 32.8–35.1 (폭포) [판독].
  - 벽 마찰: *"wall friction angles of quartz sand/glass were measured in a Jenike shear tester at low static pressures less than 2 kPa"* · **φ_W 22.7–26.5° → μ_W 0.47** (평균) [인쇄] · Henein 판정은 sin 대신 tan 이라 ≈19 % 높음 → f_c **0.165** · 식 23 → f_c **0.054** = 체류 시간의 0.04–0.06 과 맞음 [인쇄 · 그림 11] · 카드 재계산 (Θ 32.4° · Fr → 0): **0.0544** [카드 산술] · 저자: *"further experiments are neccessary to prove this criterion"* (철자 = 원문 그대로) (p.265).

### 3-4. ★ 무너짐 ↔ 구름 — 사태 주기의 들어올림 ↔ 무너짐 시간 (식 24–38 · p.256–259 · 그림 3 · 4 · 표 2 · `eq_24`–`eq_38` · `txt_p6_slumping_rolling_…` · `txt_p8_*`)
- **선행** (p.256): Wahlster [10] — 임계 Fr 는 입경에 의존 · 충전율 · 재료에는 거의 무관 · Reuter [4] — 사태 빈도 측정 · 연속 구름 전이 **Fr = 10⁻²** · Schnabel [11] — 사태 모형 (전이 미기록) · Henein [6] — 계산법 (이 논문이 이어받아 단순화).
- **사태 주기 모형** (그림 3): 회전으로 층 안 전단 응력이 커져 표면 기울기가 위 안식각 α_U 에 닿으면 표면 근처 미끄럼면 위 얇은 층이 구르고 → 미끄럼면 기울기가 아래 안식각 α_L 이 되면 끝.  ① 들어올림 시간 **t1 = πγ0/(180ω)** (24 · γ0 = 전단 쐐기 각 [°]) ② 쐐기 무게중심 S1 → S2 평균 거리 **s* = (2/3)s = (4/3)R sinε** (25 · 활꼴을 삼각형 ABC 로) · 평균 경로 기울기 **η = (α_L + α_U)/2** (26) ③ 무너짐 단계: 위치 에너지 → 운동 에너지 · 손실은 미끄럼면 마찰만 (*"Due to lack of information on energy dissipation owing to particle collisions in the slumping step"*) · 힘 균형 F_G sinη − F_I − F_F = 0 (27 · 28–31 · μ_i = tanα_L · Henein) → d²x/dt² = g(sinη − μ_i cosη) (32) → x = ½gt²(sinη − μ_i cosη) (33) → **t2 = √[2s*/(g(sinη − μ_i cosη))]** (34).
- **판정**: Henein 측정에서 *"slumping continues in a stable way as long as the shear wedge ABC can empty itself faster than it is filled anew"* → rpm 이 오르면 t1 이 t2 보다 빨리 줄어 균형 → **t1 < t2 이면 연속 구름** (35) → **Fr_c = (3/8)(πγ0/180)² (sinη − μ_i cosη)/sinε** (36) · 단순화 (Henein 측정): η ≈ Θ · α_U ≈ Θ0 · γ0 ≈ Δα = α_U − α_L → **Δα = 2(Θ0 − Θ)** (37) → **Fr_c = (3/2)[π(Θ0 − Θ)/180]² [sinΘ − tan(2Θ − Θ0)cosΘ]/sinε** (38) = 정 · 동 안식각 둘로 쓴 판정.
- **표 2** (p.259): 자갈 d 3.0 mm · Θ 37.5° · Θ0 40.7° / 석회석 1.5 · 36.0 · 37.8 / 모래 0.5 · 32.5 · 33.7 (자갈 · 석회석 = Henein [6] · 모래 = 저자 자료 — Henein 의 모래는 동적각이 정적각보다 커서 대체) [인쇄].
- **그림 4** (f 0–0.3 · log Fr 10⁻⁶–10⁻²): 식 38 선 · Henein 판정 선 · 측정 표지 (Henein [6]).  카드 재계산 (식 38 · 표 2) [카드 산술]: f 0.1 / 0.3 / 0.5 → 자갈 **4.35 / 3.34 / 3.16 × 10⁻⁴** · 석회석 **7.74 / 5.93 / 5.62 × 10⁻⁵** · 모래 **2.22 / 1.70 / 1.61 × 10⁻⁵** · 판독 f 0.295 선 3.28 × 10⁻⁴ · 5.8 × 10⁻⁵ · 1.70 × 10⁻⁵ = 재계산과 같음 [판독].
  - 측정 표지 [판독]: 자갈 f 0.035–0.19 → **4.9–8.1 × 10⁻⁴** (6 점) · 석회석 0.033–0.18 → **2.7–9.4 × 10⁻⁴** (6 점 · 식 38 의 3–5 배 = 저자 *"approximately half a decimal power"*) · 모래 0.034–0.17 → **2.6–3.8 × 10⁻⁵** (5 점 · 식 38 의 1.2–1.4 배).
  - 저자: *"the fine grained, free flowing sand already begins continuous rolling at a Froude number of approximately Fr = 2·10⁻⁵"* · 자갈은 *"more than a decimal power"* 높음 · 석회석 어긋남 = 흐름 물성 측정 오차 가능 — *"when the static angle of repose Θ0 deviates by 1°, the Froude number varies by the 3- to 6-fold"* (p.258) · Henein 판정 (s* · h 계산법이 달라 직접 비교 불가) 은 석회석에 맞고 자갈 · 모래에서 크게 벗어남.

### 3-5. ★ 구름 ↔ 폭포 — Blumberg 경험식 + 저자 실험 (식 39 · p.259–260 · p.265 · 그림 12 · 13 · `eq_39` · `txt_p9_p10_…` · `txt_p15_…`)
- 서술: 구름의 특징은 거의 평평한 표면 · 폭포 전이의 특징은 표면 휨 — *"mathematically specifying the flatness of an agitated bed surface is difficult. Apart from that, subjective influences strongly characterize its experimental determination."* · Henein [6]: 충전각이 ε > 90° − Θ 를 넘어 층 꼭대기가 II 사분면에 들면 폭포 · Blumberg [8] · 저자: 더 낮은 충전에서도 폭포 · rpm 외에 입경에도 의존 (p.259).
- **식 (39)**: **Fr·(D/d) ≈ 2** — *"ascertained here through observations from experiments on rotating drums with transparent front plates"* · *"the validity of which, however, is not proven for significantly larger dimensions [8]"* (p.260) · 요약: *"Only the transition of rolling–cascading is ascertained through an empirical criterion, for which no suitable mathematical model is known up to now."* (p.268).
- **실험 4.2** (p.265): 유리 앞판 회전 원통에서 동적 안식각 측정 · 규사 좁은 입도 **d50 0.24 · 0.5 · 0.75 · 1.0 mm** · rpm **0.5–10 min⁻¹** · 충전 **0.05–0.25** · 지름 **200 · 300 · 500 mm** · 유리판 너머 사진 (자 · 다림추) · 구름에서 표면 기울기 = Θ (rpm · 충전율에 약하게 의존 · rpm 과 선형) · 폭포에서 콩팥 꼴 → 경사 구간마다 다른 기울기 (κ < Θ_m · κ > Θ_m) · **옆벽의 끌어당김 (pulling effect)** 때문에 앞판 · 뒤판과 가운데 (*"undisturbed flow region"*) 를 따로 쟀다 · 가운데 흐름을 얻으려 **L/D > 0.3** 원통.
  - **그림 12** (D 200 mm · d 0.24 mm · f 0.1): 구름 Θ ≈ 30.9–31.8° (회귀선 0.4 → 7 min⁻¹ 에서 30.97 → 32.80°) · 폭포에서 갈라짐 — 가운데 n 4.2: 32.9 / 29.4° · 5.8: 35.3 / 28.9° · 앞판 n 2.8: 33.0 / 30.2° · 4.2: 35.0 / 29.0° · 5.8: 39.1 / 27.4° [판독] · 전이 *"approximately n_c = 2 min⁻¹"* (앞판 · 뒤판) ↔ **3.3 min⁻¹** (가운데) [인쇄] · 카드 환산: Fr 4.47 × 10⁻⁴ · 1.22 × 10⁻³ → Fr·D/d **0.373 · 1.014** [카드 산술] = 그림 13 의 f 0.10 점 (0.371 · 1.006 [판독]) 과 같다.
  - **그림 13** (D 200 · d 0.24 · Fr_c·D/d vs f · log): **가운데 1.70 · 1.01 · 0.73 · 0.456 · 0.371** · **앞판/뒤판 0.84 · 0.371 · 0.237 · 0.133 · 0.091** (f ≈ 0.047 · 0.102 · 0.150 · 0.197 · 0.260) · 식 39 점선 1.97 [판독] → 측정은 식 39 (2) 의 **1/1.2–1/5.4 (가운데) · 1/2.4–1/22 (앞판)** 이고 충전율이 클수록 더 낮다 [카드 산술].  저자: *"The deviations from the experimental values allow the presumption of a dependence of the critical Froude number on operating variables, which are not accounted for in Eq. (39). As it appears, besides the rotational speed and particle diameter, the transition in the area of parameters studied is also dependent on filling degree. In all experiments the transition rolling–cascading estimated in this way was in the range of Fr = 10⁻⁴–10⁻². The cylinder diameter had no influence. Despite the deviations from the measurements and for lack of a suitable mathematical model, Eq. (39) is used below"* (p.265–266).

### 3-6. ★ 폭포 ↔ 던짐 — 반지름 힘 균형 · 이탈선 (식 40–48 · p.260–262 · 그림 5 · 6 · 7 · `eq_40`–`eq_48` · `txt_p10_*` · `txt_p11_*` · `txt_p12_*`)
- 기준: 기체 공간으로 던져짐 · Davis [23] 의 반지름 힘 균형 = *"the minimum condition for the throw off of particles into the gas space"* · 이탈선 **ω²r/g = sinζ** (40) = 축과 힘의 극 P (높이 g/ω²) 를 지름으로 하는 원 (Thales) · II 사분면에만 · **ω²r/g > sinζ** 이면 던짐 (41) · 바깥 궤도 r = R 가 먼저 · **ζ = Θ + ε − 90° = κ − 90°** (42) · Rutgers [3]: **Fr = 0.3–0.36** (p.260).
- **낮은 충전 (Θ + ε < 90° · ζ < 0)**: 층이 III · IV 사분면 → 벽 마찰로 II 사분면까지 실려 가야 · κ = 90° 에서 원심력만으로 → 접선 힘 균형 m_P g sinκ = μ_W m_P (g cosκ + ω²R) (43) → **μ_W Fr > 1** (44) → **Fr_c = 1/μ_W** (45 · 단일 입자 엄밀) · 그림 6 · 예: 소결대 거칠기 가마의 모래 φ_W ≈ 34° → μ_W 0.675 → **Fr_c 1.48** · Θ 32.5° 면 ε(ζ = 0) = 57.5° → 충전 17.5 % 까지 층이 축 아래 (콩팥 꼴이라 실제로는 그보다 조금 낮음) · 볼 밀 경험: Fr 0.25–0.72 에서 이미 던짐 (높은 충전) [인쇄 p.261] · 카드 검산: 1/0.675 = 1.481 · tan 34° = 0.6745 · f(57.5°) = 0.1752 [카드 산술].
- **높은 충전 (Θ + ε > 90° · ζ > 0)**: I · II 사분면 입자 · F_N = F_C − F_G sinζ (46) · 저속이면 F_N < 0 (P2 에 닿으면 표면을 굴러 폭포) · F_N → 0 이 반지름 균형 → **ω²R/g > sinζ** (47) → **Fr_c = sin(Θ + ε − 90°)** (48) · 그림 7 (Θ 25–40°): *"a detachment of the particles is possible when filling degrees are approximately above 15%. The lower the dynamic angle of repose, the higher the filling degree necessary to reach cataracting motion."* · 볼 밀 운전 (충전 0.35–0.50 · 임계 속도의 65–75 % → **Fr 0.42–0.56**) 이 빗금 칸으로 맞음 (*"the dynamic angle of repose of the mixture of ball charge and bed material to be grinded must be applied"*) · Rose & Sullivan [28] 과도 맞음 [인쇄 p.262] · 카드 검산: 0.65² = 0.4225 · 0.75² = 0.5625 [카드 산술].
- [카드 산술 · 식 48 · f 0.30 (ε 71.36°)]: Θ 25 · 30 · 32.5 · 35 · 37.5 · 40° → **Fr_c 0.111 · 0.197 · 0.240 · 0.282 · 0.323 · 0.364** · (f 0.28: 0.075 · 0.162 · … · 0.331 / f 0.32: 0.145 · 0.231 · … · 0.396).

### 3-7. 던짐 ↔ 원심 — 단일 입자 · 볼 밀 (식 49–53 · p.262–264 · 그림 8 · 9 · `eq_49`–`eq_53` · `txt_p13_*`)
- 고전 정의: 위 사점 (κ = 180°) 에서 원심력 = 중력 → **Fr = 1** (49) · 그러나 다른 각도에서 벽에 붙어 있으려면 Fr > 1 — 접선 균형 (벽 마찰 포함) **Fr = sinκ/μ_W − cosκ = sin(κ − φ_W)/sinφ_W** (50 · 단일 입자의 각 위치별 임계 · κ = 90° 에서 식 45 · μ_W → ∞ · κ = Θ + ε 에서 식 48) · 최대 **Fr_c,P = 1/sinφ_W** (51 · κ = 90° + φ_W) · Teubner [13]: μ_W 0.4 → 최대 **Fr 2.7 at κ 111.8°** [인쇄] (카드 검산 2.693 · 111.80° [카드 산술]) · 볼 밀 실험 [12,13]: 원심은 Fr > 1 에서 시작.
- 층으로: 꼭대기 κ = Θ + ε 가 90° + φ_W 를 넘으면 → **Fr_c = 1/sin(φ_i + ε − 90°)** (52 · Θ 대신 장입물의 내부 마찰각 φ_i · 볼이 원통보다 아주 작을 때 · φ_i + ε > 90° 에서만).
- **Watanabe [24]** (모형 볼 밀 L 0.124 m · D 0.76 m · 그림 9): 충전율 ↑ → 임계 Fr 급감 · f ≈ 70 % 에서 Fr ≈ 1 · *"Simulation calculations following the Discrete Element Method (DEM) using the linear–spring–dashpot model for particle–particle and particle–wall collisions as well as the Coulomb criterion for dynamic friction produced a good correspondence with the experimental results [24]. No centrifuging was observed when filling degrees were less than 30%."* · Watanabe 가 준 μ_i = μ_W = 0.15 의 식 52 는 측정에서 벗어난다 (그림 9 에서 측정은 μ_i 0.3 선 근처 [판독]) · 그림 9 측정 (Watanabe) [판독]: f 0.38 → Fr 10.7 · 0.42 → 7.4 · 0.46 → 5.9 · 0.50 → 4.2 · 0.54 → 2.8 · 0.58 → 1.9 · 0.62 → 1.45 · 0.66 → 1.14 · ≥ 0.70 → ≈1.0.
- 고리 최소 충전 **f_min = 1 − [1 − 2(d/D)]²** (53 · 두께 d 의 닫힌 고리 · 빈 부피 차 무시) · Watanabe d/D 0.066 → **0.2466** [카드 산술] (그림 9 점선 ≈0.25).

### 3-8. ★ Bed Behavior Diagram (그림 14 · 15 · 16 · p.266–268 · `fig_14`–`fig_16` · `txt_p16_*` · `txt_p17_p18_*`)
- 기준식 (p.266): 미끄럼 ↔ 폭포 **식 23** (아래 패널 · μ_W vs f) · 무너짐 ↔ 구름 **식 38** · 구름 ↔ 폭포 **식 39** · 폭포 ↔ 던짐 **식 45 · 48** · 던짐 ↔ 원심 **식 52** (위 패널 · Fr vs f) · 입력 = 표 2 · **μ_W = 0.675 을 세 재료 모두에** (*"For lack of data, a wall friction coefficient of μ_W = 0.675 given for sand in a rotary kiln with sintering zone roughness [25] is applied for all bed materials in the diagrams."* p.268) · **드럼 지름 D · φ_i 는 원문에 없다** [미확인].
- 판독 (f 0.30 · log 축 판독은 식 재계산보다 2–6 % 높게 나오는 경향) [판독 · 카드 산술]:

| 경계 | 자갈 (d 3.0 · Θ 37.5 · Θ0 40.7) | 석회석 (1.5 · 36.0 · 37.8) | 모래 (0.5 · 32.5 · 33.7) | 식 재계산 [카드 산술] |
|---|---|---|---|---|
| 폭포 ↔ 던짐 (낮은 충전 · 평평한 선) | 1.45–1.46 | 1.50–1.51 | 1.50 | 식 45: 1/0.675 = 1.481 |
| 계단 (Θ + ε = 90°) 의 f | 0.144 | 0.151 | 0.177 | 0.138 · 0.149 · 0.175 (그려진 점 간격 때문에 계단이 다음 점에) |
| 폭포 ↔ 던짐 f 0.3 · 0.4 · 0.49 | 0.332 · 0.487 · 0.613 | 0.306 · 0.471 · 0.608 | 0.250 · 0.407 · 0.554 | 식 48: 0.323 · 0.476 · 0.596 / 0.298 · 0.453 · 0.575 / 0.239 · 0.398 · 0.524 |
| 던짐 ↔ 원심 f 0.3 · 0.4 · 0.49 | ≈3.2 · 2.16 · 1.70 | ≈3.5 · 2.36 · 1.86 | ≈4.4 · 2.58 · 1.98 | 식 52 (φ_i = Θ 로 두면) 3.09 · 2.10 · 1.69 / 3.35 · 2.21 · 1.75 / 4.17 · 2.52 · 1.92 — **φ_i 미기재** · 판독은 φ_i ≈ Θ 와 어긋나지 않는다 [카드 추론] |
| 구름 ↔ 폭포 (수평 원 표지) | **0.0149** | **0.0076** | **0.0025** | 식 39 = 2d/D → **D ≈ 403 · 395 · 400 mm** [카드 산술 · D 미기재의 역산] |
| 무너짐 ↔ 구름 f 0.4 · 0.49 | 3.4 · 3.3 × 10⁻⁴ | 5.8 · 5.7 × 10⁻⁵ | — · 1.63 × 10⁻⁵ | 식 38: 3.20 · 3.16 × 10⁻⁴ / 5.69 · 5.62 × 10⁻⁵ / 1.63 · 1.61 × 10⁻⁵ |
| 아래 패널 μ_W,c f 0.005 · 0.1 · 0.2 · 0.3 · 0.4 · 0.49 | 0.59 · 0.496 · 0.426 · 0.368 · 0.315 · 0.266 | 0.578 · 0.480 · 0.417 · 0.361 · 0.304 · 0.257 | **0.596 · 0.501 · 0.430 · 0.369 · 0.311 · 0.263** | 식 23 (Fr → 0): 0.594 · 0.496 · 0.426 · 0.366 · 0.311 · 0.264 / 0.573 · 0.479 · 0.412 · 0.354 · 0.300 · 0.254 / **0.524 · 0.437 · 0.376 · 0.323 · 0.274 · 0.233** |
- ⚠ **모래 아래 패널** [판독 · 카드 산술]: 판독값에서 역산한 Θ = 37.4–38.0° (자갈 37.2–38.1 · 석회석 36.1–36.9 = 표 2 와 맞음) → 그림 16 의 아래 패널은 **Θ ≈ 37.5° (자갈 값) 꼴로 그려져** 표 2 모래 (32.5°) 보다 ≈13 % 높다 · 같은 논문 그림 11 의 규사 (Θ 32.4°) 곡선은 f 0 에서 0.535 = sin 32.4° 로 맞다 → 원문 그림의 그리기 오류로 보인다 (원문 안 어긋남 §3-11).
- 저자 해석 (p.267–268): 아래 패널 = 낮은 충전에서 원치 않는 미끄럼 · 위 패널 = 세 재료 원리상 같음 · *"Only the transitions of slumping–rolling and rolling–cascading differ in the Froude number by one to two decimal powers and shift to lower Froude numbers with increasing flowability of the solids."* · 흐름성 지표 = 동적 안식각 (작을수록 자유유동) · *"As the flowability of the bed increases, the slumping range diminishes until, when the material is free-flowing, it finally disappears (Fig. 16). As observations confirm [6], slipping motion can turn directly into rolling in this case."* (그림 16 에도 Fr ≲ 2 × 10⁻⁵ 아래 'Slumping' 띠는 남아 있다 [판독]) · 무너짐 ↔ 구름 측정 (Henein) 과 석회석 빼고 맞음 · 낮은 충전 (f < 0.15) 의 던짐은 Fr > 1 (식 45) · Θ + ε = 90° 의 계단은 *"a discontinuity given by the model occurs, which in this manner will only happen in the motion of a single particle"* · 볼 밀은 f > 0.2 만 관련 · 낮은 충전에서 던짐 → 원심은 아주 높은 rpm 에서만 · 높은 충전에서 Fr → 1.

### 3-9. 규모 늘림 기준 (scaling criteria) (p.251 · p.268–269 · `txt_p1_abstract_…` · `txt_p19_summary_…`)
- 일곱: **Fr · 충전율 f · 벽 마찰 계수 μ_W · 내부 마찰 계수 (각 φ_i) · 동적 안식각 Θ · 정적 안식각 Θ0 · 입자/원통 지름비 d/D**.
- 무관: *"The parameters of length and inclination of the cylinder, which essentially determine the axial transport, have no influence on the transverse motion, so that generally experimental studies on transverse motion behavior can be conducted batchwise in a horizontal rotating drum."* (p.269)
- 꼴별 주 변수 (요약 p.269): 미끄럼 = 충전율 + 층/벽 마찰 (저속에서 Fr 무시 가능) · 폭포 계열 · 던짐 계열 = Fr + 충전율 + 층 물성.
- 저자 맺음: *"Continuing studies are necessary to experimentally test the criteria worked out and improve the mathematical models developed."* (p.269)

### 3-10. ★ 우리 드럼을 이 지도에 놓기 [우리 산술 · 카드 추론 — 원문 범위 밖 외삽]
우리 값 (읽기만): `scripts/make_mixer_deck.py` (`FR_ANCHOR = 0.0827` · `FR_BAND = (0.055, 0.086)` = *"씽키 컵프레임 밴드 (설계문서 §18-1; ⚠ 1차 출처 미확보)"* · `MU_S = 0.9` (입자–입자 = 입자–벽 정지 마찰) · `MU_R = 0.075` (구름 마찰) · `COR = 0.3` · `plan(…, fill=0.30, pack=0.60)` · 배플 기본 0 · Drum · Front · Back 메시가 함께 회전) · B2-U 덱 메타 (76.6765 rpm · 2 바퀴 · CGF 151.4 — 정본 `liu2013` 카드 §3-10) · 기하 · 입자 = 정본 `khakhar1999` 카드 §3-9 (39 각형 꼭짓점 반지름 12.583 mm · 변 중점 12.542 mm · 축 길이 5.033 mm · 고체 440 mm³ · 드럼 2,493 mm³ → 겉보기 충전 0.28–0.32 · parcel 지름 SE 0.1514 · AM_S 0.6056 · AM_P 1.3626 mm · 99,158 · 708 · 134 개) · `docs/reviews/mixer_b2_u_development_20261122/README.md` (Bo_SE 0.21244 (B1-U) · 21.244 (B2-U) · γ_AM/γ_SE 0.1 · γ_W/γ_SE 0.00256 · B1-U 한 팔 25 시간 7 분 43 초) · ⚠ 옛 덱 (LC_ref_r2 · 75.04 rpm · R 13.14 mm — 정본 `nase2001` 카드) 도 Fr 0.0827.

| 항목 | 이 논문 식 · 범위 | 우리 드럼 값 [우리 산술] | 판정 |
|---|---|---|---|
| Fr (식 3 · R = 안 반지름) | — | 꼭짓점 R **0.0827** · 변 중점 R 0.0824 · n_c = 266.6 rpm (식 4 · 정확식과 42.3/√D 같음) · n/n_c 0.288 | — |
| 충전율 (식 1 · 단면 몫) | — | 덱 0.30 (정지 충전 0.60 의 겉보기 부피) · 실제 0.28–0.32 · ε 71.4° (69.3–73.3°) | 같은 정의 (층이 차지한 단면 몫 · 겉보기) |
| 표 1 띠 | 구름 10⁻⁴–10⁻² · 폭포 10⁻³–10⁻¹ · 던짐 0.1–1 | 0.0827 | **폭포 띠 안** (구름 띠 밖 · 던짐 띠 아래 끝 0.1 의 0.83 배) |
| 미끄럼 ↔ 폭포 (식 23) | μ_W > μ_W,c | f 0.30 · Fr 0.0827: Θ 25 · 30 · 35 · 40° → **0.235 · 0.278 · 0.319 · 0.357** (f 0.28–0.32: 0.228–0.368) | 덱 입자–벽 μ_s 0.9 (+ 구름 마찰 0.075 · 39 각형 · 끝판 회전) → 유효 층/벽 μ_W 가 0.24–0.36 을 넘으면 미끄럼 없음 — 유효값 자체는 [미확인] (덤프로 잰다) |
| 무너짐 ↔ 구름 (식 38) | Fr > Fr_c 면 구름 | 표 2 재료 꼴 (Θ0 − Θ 1.2–3.2°) 이면 Fr_c 1.7 × 10⁻⁵ – 3.3 × 10⁻⁴ → 우리 = **250–4,900 배** · Fr_c = 0.0827 이 되려면 **Θ0 − Θ ≈ 21.2–21.6°** (Θ 40–25°) | 무너짐은 정 · 동 안식각 차가 ≈21° 를 넘는 강한 점착 층에서만 [카드 산술] — B2-U (Bo_SE 21) 의 Θ0 − Θ 는 [미확인] |
| 구름 ↔ 폭포 (식 39 · D = 25.166 mm) | Fr > 2d/D 면 폭포 | d = SE 0.1514 → Fr_c **0.0120** (우리 6.9 배) · AM_S 0.6056 → **0.0481** (1.7 배) · AM_P 1.3626 → **0.108** (**0.76 배**) · Sauter d32 0.302 → 0.0240 (3.4 배) · 부피 평균 0.725 → **0.0576** (1.4 배) · 실입경 1 · 4 · 9 µm (같은 D 라면) → 7.9 × 10⁻⁵ · 3.2 × 10⁻⁴ · 7.2 × 10⁻⁴ (116–1,041 배) | AM_P 만으로 읽을 때만 구름 쪽 · 나머지는 폭포 쪽 |
| 구름 ↔ 폭포 (원문 측정 · 그림 13 · f 0.26 [판독]) | 가운데 Fr_c·D/d 0.371 · 앞판 0.091 | 가운데: SE 0.0022 (37 배) · AM_S 0.0089 (9.3 배) · AM_P 0.020 (4.1 배) · 부피 평균 0.0107 (7.7 배) / 앞판: 5.5 × 10⁻⁴ – 4.9 × 10⁻³ (17–151 배) | **어느 d 로도 폭포** (원문 측정 범위 f ≤ 0.26 밖 0.30 · 규사 · D 200 mm 기준) |
| 폭포 ↔ 던짐 (식 48 · Θ + ε > 90°) | Fr > sin(Θ + ε − 90°) 면 던짐 | f 0.30: Θ 25 · 30 · 32.5 · 35 · 37.5 · 40° → Fr_c **0.111 · 0.197 · 0.240 · 0.282 · 0.323 · 0.364** → 우리 = **0.75 · 0.42 · 0.35 · 0.29 · 0.26 · 0.23 배** · 던짐이 되는 Θ* = 23.4° (f 0.30) · 25.4° (f 0.28) · 21.4° (f 0.32) | Θ ≥ 26° 면 충전 0.28–0.32 모두 던짐 아래 · ⚠ f 0.28 · Θ 25° 면 0.0754 < 0.0827 → 던짐 문턱 넘음 [카드 산술] |
| 던짐 ↔ 원심 (식 52) | — | f 0.30: φ_i 25–40° → 9.03–2.75 | 해당 없음 (≫ 0.0827) |
| 드럼 꼴 | 무배플 원통 | **39 각형** (꼭짓점 R 12.583 · 변 길이 2.025 mm · 꼭짓점 ↔ 변 중점 깊이 0.041 mm = 0.27 d_SE · 0.067 d_AM_S · 0.030 d_AM_P · 면 기울기 ±4.6°) | 원문 범위 밖 — 면 꺾임은 SE parcel 크기의 벽 거칠기 정도 (미끄럼 억제 쪽) [카드 추론] |
| 길이 · 끝벽 | 2D 단위 깊이 · 실험 L/D > 0.3 (가운데 흐름) | **L/D 0.20** · 끝판 (Front · Back) 이 드럼과 함께 회전 · f 0.30 에서 끝판 두 장 접촉 면적 298 mm² ↔ 원통 벽 158 mm² | 층 전체가 끝벽 영향권 (원문 *"pulling effect"* = 앞판 전이가 가운데보다 2.7–4 배 낮은 Fr) → 우리에게는 **앞판 값이 더 가까울 수 있다** (폭포 쪽으로 더) · 끝판 마찰 모멘트는 식 21 에 없다 (미끄럼 더 억제) [카드 추론] |
| 입자 | 자유유동 단분산 | 다분산 3 상 (부피 몫 SE 0.410 · AM_S 0.187 · AM_P 0.403) · SJKR 점착 (Bo_SE 0.21 / 21.2) · 벽 점착 약함 (γ_W/γ_SE 0.00256) | 원문 범위 밖 — 점착은 Θ · Θ0 · 유효 μ_W 를 바꿔 경계를 옮긴다 [카드 추론] |

- ⇒ **판정 [카드 산술 · 범위 밖 외삽]**: 우리 드럼 (Fr 0.0827 · f 0.30) = **폭포 (cascading · 콩팥 꼴 표면) 꼴 창 안** — 아래 경계 = 구름 ↔ 폭포 (식 39 · 부피 평균 d 0.058 → 우리 1.4 배 위 / 원문 실측 0.011 → 7.7 배 위) · 위 경계 = 폭포 ↔ 던짐 (식 48 · Θ 30–40° → 0.20–0.36 → 우리 0.23–0.42 배) · 창 폭 ≈ 0.5 자릿수 (부피 평균 d · Θ 30°: 0.058–0.197) · 미끄럼 = 유효 벽 μ > 0.24–0.36 이면 없음 · 무너짐 = Θ0 − Θ ≳ 21° 일 때만.  ⚠ 점착 · 다분산 · 39 각형 · L/D 0.20 · 끝판 회전 · parcel 크기가 전부 원문 범위 밖이라 **꼴은 덤프에서 직접 판정**해야 한다 (§9 행동 1).
- ⇒ **CGF 와 꼴** [카드 산술]: parcel 은 실입경의 151.4 배라 d/D 가 151 배 크다 → 식 39 의 구름 ↔ 폭포 경계가 실입경 (같은 D) 의 7.9 × 10⁻⁵ – 7.2 × 10⁻⁴ 에서 parcel 의 0.012–0.108 로 올라 **우리 운전점 근처로 온다** — Fr 를 맞춰도 coarse-graining 은 꼴을 보존하지 않는다 (경계가 Fr·D/d 에 걸리므로) · 덱의 Fr 밴드 (0.055–0.086) 아래 끝은 부피 평균 d 의 식 39 경계 (0.058) 와 겹친다.
- ⇒ **공정 축 두세 수준 — 고를 근거** [카드 추론 · 등록 초안 아님] (rpm = 60/(2π)·√(Fr·g/R) · R 12.583 mm · 2 바퀴 벽시계 = B1-U 실측 25.1 시간 × 76.68/rpm 어림 · 충전 · 정착 몫 고정이면 느린 rpm 은 이보다 짧고 빠른 rpm 은 길다):

| Fr | rpm | 이 지도에서 | 고르는 뜻 | 2 바퀴 벽시계 어림 |
|---|---|---|---|---|
| 0.0088 | 25.0 | 식 39 로는 **모든 d 에서 구름** (0.012 아래) · 원문 측정 (가운데 f 0.26) 으로는 SE 기준 폭포 · AM_S · AM_P · 부피 평균 기준 구름 → **구름 ↔ 폭포 경계를 걸침** | 꼴 경계 아래쪽 팔 · Liu 2013 의 15 rpm 과 같은 Fr (문헌 대조) | ≈77 시간 (48 시간 상한 넘음 → 나눠 돌리기) |
| 0.0827 | 76.7 | 폭포 창 가운데 (현재) | 기준 팔 | 25.1 시간 (실측) |
| 0.13 | 96.1 | Θ ≥ 26.1° 면 폭포 안 (식 48) | **같은 꼴 안** 둘째 점 (꼴 안의 rpm 효과) | ≈20 시간 |
| 0.20 | 119.2 | Θ < 30.2° 면 던짐 (식 48) · 표 1 던짐 띠 (0.1–1) 안 | 폭포 ↔ 던짐 경계를 걸침 (Θ 에 따라) | ≈16 시간 |
| 0.30 | 146.0 | Θ < 36.1° 면 던짐 · Rutgers 0.3–0.36 · 볼 밀 0.25–0.72 | **던짐 쪽 팔** (충격 · '분쇄' 성격 = 덩어리 풀림 후보) | ≈13 시간 |
  - 권고 [카드 추론]: **세 수준 = 0.0088 (경계 아래) · 0.0827 (창 안) · 0.30 (경계 위)** + 같은 꼴 안의 rpm 효과를 따로 보려면 **0.13** — 덱의 Fr 밴드 (0.055–0.086) 밖이라 `--allow-off-band` 가 필요하다 · 각 팔에서 꼴을 덤프로 판정한 뒤에만 '꼴 안 rpm 효과' 와 '꼴 바뀜 효과' 를 가른다.

### 3-11. 원문 안 어긋남 (§11 에 다시)
① **식 (14) 의 밀도 기호가 ρ_g** (렌더 확인) — 같은 유도의 식 8 · 15 · 16 · 20 · 21 은 ρ_b (층 겉보기 밀도) → 오식으로 보인다 (결과식 20–23 에는 ρ_b) ② **그림 16 아래 패널** = Θ ≈ 37.5° 꼴 (표 2 모래 32.5° 면 ≈13 % 낮아야) [판독 · 카드 산술 §3-8] ③ 본문 *"the slumping range … finally disappears (Fig. 16)"* ↔ 그림 16 은 Fr ≲ 2 × 10⁻⁵ 아래 'Slumping' 띠를 여전히 그림 [판독] ④ 그림 4 의 Henein 선을 본문은 *"the slipping criterion derived by Henein et al."* 이라 부른다 (p.258) — 그림은 무너짐 ↔ 구름 [카드 해석: 'slumping' 의 오기로 보임] ⑤ BBD 는 식 39 (Fr·D/d = 2) 로 그렸는데 저자 자신의 측정 (그림 13) 은 0.09–1.7 → 구름 ↔ 폭포 선이 측정보다 1.2–22 배 높게 그려진 셈 (저자는 그 사실을 적고 *"for lack of a suitable mathematical model"* 썼다) ⑥ BBD 의 D · φ_i 미기재 (판독 역산 D ≈ 0.40 m · φ_i ≈ Θ 와 어긋나지 않음) ⑦ 표 2 의 μ_W 칸 없음 → 세 재료 모두 모래 가마 값 0.675 (p.268).

---

## 4. ★ 방법 — 모델 · 측정 사슬 · 이 묶음의 네 질문

### 4-1. 모델 사슬 (해석 · 2D 단위 깊이)
- **기하**: 원통 단면 · 평평한 표면 (구름) · 충전각 ε · 무게중심 r_S (식 1–2) · 폭포 꼴에서 층 무게중심이 동적 안식각 Θ 만큼 기울어진다 (δ = Θ).
- **미끄럼 ↔ 폭포**: 축 둘레 모멘트 — 짐 (무게 × r_S sinδ) ↔ 벽 마찰 (정수압 벽 압력 + 원심 (R + r0,x)/2 · 적분) → 식 23.  맞춘 값 0 (입력 = Θ · μ_W · f · Fr).
- **무너짐 ↔ 구름**: 사태 주기 — 들어올림 (전단 쐐기 각 γ0 만큼 회전) ↔ 쐐기 무게중심의 Coulomb 미끄럼 시간 (μ_i = tanα_L) → 식 36 → Henein 측정에서 가져온 세 근사 (η ≈ Θ · α_U ≈ Θ0 · γ0 ≈ 2(Θ0 − Θ)) → 식 38.  맞춘 값 0.
- **구름 ↔ 폭포**: 경험식 (Blumberg) — 모형 없음.
- **폭포 ↔ 던짐**: 반지름 힘 균형 (Davis 의 이탈선) — 낮은 충전은 단일 입자 벽 접선 균형 (식 45) · 높은 충전은 층 꼭대기 입자 (식 48).
- **던짐 ↔ 원심**: 단일 입자 접선 균형 (Teubner · 식 50–51) → 층 꼭대기를 내부 마찰각으로 (식 52) · 고리 최소 충전 (식 53).
- **입력 물성**: Θ · Θ0 (안식각) · μ_W (Jenike 벽 마찰) · φ_i (내부 마찰) · d/D.

### 4-2. 측정 사슬 (재구성)
- 4.1: 연속 유량 유리 원통 (L 4.6 m) → 축 방향 충전율 (벽 너머) → 평균 체류 시간 ωT·D/L · 누적 충전율 F vs Du → 꺾임 (Du ≈ 0.009 · F_c 0.04–0.06) / Jenike 전단 시험기 (< 2 kPa) → φ_W → μ_W 0.47 → 식 23 교점 0.054.
- 4.2: 회분 회전 드럼 (유리 앞판 · D 200 · 300 · 500 mm · L/D > 0.3) → rpm 올리며 사진 (위 · 비스듬히) → 경사 구간별 기울기 → 기울기가 갈라지는 rpm = 구름 ↔ 폭포 (앞판 · 가운데 따로) → Fr_c·D/d vs f (그림 13).
- 나머지: Henein (무너짐 ↔ 구름 측정 · 그림 4 · 14–16) · Watanabe (원심 · 그림 9) · 볼 밀 관행 (그림 7) — 문헌 숫자 대조.
- 반복 · 오차 막대 · 측정 불확도 · 실험 rpm 목록 [미확인].

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말했나** — **말 없음.**  DEM 은 한 곳 — Watanabe [24] 볼 밀 원심의 *"Discrete Element Method (DEM) using the linear–spring–dashpot model for particle–particle and particle–wall collisions as well as the Coulomb criterion for dynamic friction produced a good correspondence with the experimental results"* (p.263) — 를 **성공 사례로** 인용한다.  이 논문 자신의 한계 문장은 모형 쪽: *"the transition behavior between the forms of motion has been investigated in only a few papers or handled as a secondary aspect"* (p.253) · *"The measurement of these bed material properties is, however, only possible with great experimental effort, Eq. (36) being usable only to a limited extent."* (p.258) · *"Due to lack of information on energy dissipation owing to particle collisions in the slumping step, it is assumed that the potential energy is converted solely to kinetic energy lowered by energy losses according to friction at the slip plane."* (p.257) · 식 45 는 *"Strictly taken, it applies only to a single particle, since, besides the wall friction, the inner bed material friction is important in the motion of a bed."* (p.261).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — **해당 없음** (흐르는 자유유동 층 · 입자 변형 0).  계산 비용 개념 없음 (닫힌 식).
3. **2D 인가 3D 인가 · 2D → 3D** — 모형 = **2D 단위 깊이 단면** (*"a cross-section of a cylinder of unit depth"* p.254 · *"the solid bed can be regarded as a bulk solid body infinitely elongated in the axial direction"* p.255).  3D 증거 = 끝벽: *"Taking into consideration the pulling effect of the side walls, these inclination angles were measured both at the front plate/back and in the axial middle of the drum, i.e. in the undisturbed flow region of the bed"* · *"Owing to the pulling effect, the transition behavior at the side walls deviates from that of the undisturbed flow region"* (p.265 · 앞판 2 ↔ 가운데 3.3 min⁻¹) · 길이 · 기울기는 가로 운동 무관 (p.269 — 긴 가마에 대해).
4. **압력을 뺄 때의 거동** — 해당 없음 (압밀 · 탈압 없음).

### 4-4. 기법 미니 용어집
- **충전율 f (filling degree)** = 단면에서 층이 차지하는 몫 = (ε − sinε cosε)/π · **충전각 ε** = 층 원호의 반각.
- **Froude 수 (peripheral)** = ω²R/g (R = 원통 안 반지름) = (n/n_c)² · **임계 속도 n_c** = 바깥 궤도 입자가 위 사점에서 원심되는 rpm ≈ 42.3/√D.
- **동적 안식각 Θ** = 돌고 있는 층 표면의 기울기 · **정적 안식각 Θ0** = 사태 직전의 최대 기울기 (≈ 위 안식각 α_U) · **아래 안식각 α_L** = 사태 뒤 기울기 · **전단 쐐기 각 Δα = α_U − α_L ≈ 2(Θ0 − Θ)**.
- **유효 벽 마찰 계수 μ_W = tanφ_W** = 층 전체가 벽에 대해 갖는 마찰 (Jenike 벽 마찰 시험) · **임계 벽 마찰 μ_W,c** = 미끄럼 ↔ 폭포 경계.
- **내부 마찰각 φ_i** = 층 안 전단 저항 (Coulomb).
- **이탈선 (line of detachment)** = 반지름 힘 균형 ω²r/g = sinζ 인 점들 — 축과 힘의 극을 지름으로 하는 원.
- **Bed Behavior Diagram** = Fr (와 μ_W) 를 충전율에 대해 그린 운동 꼴 지도 (Henein 1983 이 비슷한 꼴을 먼저 제안).
- **pulling effect** = 끝벽 (앞판 · 뒤판) 이 층을 끌어당겨 끝 근처 흐름이 가운데와 달라지는 것.
- **Jenike 전단 시험기** = 분체 흐름 · 벽 마찰을 정 하중 아래 재는 장치.

---

## 5. Figure set ★ (크롭 92 장 = `litdb/figures/mellmann2001_transverse_bed_motion_rotating_cylinders_slumping_rolling_cascading_froude/`)
| 그림 (크롭 파일) | 내용 | 우리 활용 |
|---|---|---|
| 표 1 (`tab_1.png` · 다시 자름) | ★ 일곱 꼴 · 물리 과정 · Fr · f · μ_W · 쓰임 | 우리 Fr 0.0827 = 폭포 띠 (§3-10) · 꼴마다 성격 (혼합 ↔ 분쇄) |
| 표 2 (`tab_2.png` · 손 크롭) | 자갈 · 석회석 · 모래 d · Θ · Θ0 | BBD 입력 · 흐름 물성의 크기 감각 |
| Fig. 1 (`fig_1.png`) | 단면 기하 · 모멘트 균형 (ε · κ · δ = Θ · r_S · 힘 · M1 · M2) | 식 5–23 의 기호 |
| Fig. 2 (`fig_2.png`) | μ_W,c vs f (Θ 25–40°) | 우리 미끄럼 판정 (f 0.30 → 0.24–0.36) |
| Fig. 3 (`fig_3.png`) | 사태 쐐기 ABC · s* · η · α_U · α_L | 식 24–38 의 기호 · 덤프에서 α_U · α_L 재는 법 |
| Fig. 4 (`fig_4.png`) | 무너짐 ↔ 구름 Fr_c vs f (세 재료 · 식 38 · Henein · 측정) | 자유유동이면 Fr_c 10⁻⁵–10⁻³ (우리보다 2–4 자릿수 아래) |
| Fig. 5 (`fig_5.png` · 손 크롭) | 사분면별 힘 균형 · 이탈선 · 극 P (g/ω²) | 던짐 판정 (덤프에서 이탈 입자 세기) |
| Fig. 6 (`fig_6.png`) | 낮은 충전 Fr_c = 1/μ_W (모래 1.48) | 우리 (높은 충전) 해당 없음 |
| Fig. 7 (`fig_7.png`) | ★ 높은 충전 Fr_c = sin(Θ + ε − 90°) · 볼 밀 칸 | 우리 던짐 문턱 0.11–0.36 (Θ 25–40°) |
| Fig. 8 (`fig_8.png`) | 단일 입자 원심 Fr vs κ (μ_W 0.4–1.6) | — |
| Fig. 9 (`fig_9.png`) | 던짐 ↔ 원심 (μ_i 0.15 · 0.3 · 0.5) · Watanabe 측정 · f_min | DEM (linear spring–dashpot) 이 원심을 재현한 선례 |
| Fig. 10 (`fig_10.png`) | 유리 원통 체류 시간 · 누적 충전율 vs Du (꺾임 0.009) | 미끄럼 ↔ 폭포 실험 |
| Fig. 11 (`fig_11.png`) | μ_W,c vs f (식 23 · Henein) + μ_W 0.47 → f_c 0.054 · 0.165 | 따로 잰 입력 → 사전 예측의 선례 (G2 방법 꼴) |
| Fig. 12 (`fig_12.png`) | 동적 안식각 vs rpm (가운데 ↔ 앞판 · 콩팥 꼴 갈라짐) | ★ 덤프에서 꼴 판정 = 경사 구간별 기울기 |
| Fig. 13 (`fig_13.png`) | ★ Fr_c·D/d vs f (가운데 1.70 → 0.37 · 앞판 0.84 → 0.091 · 식 39 = 2) | 우리 구름 ↔ 폭포 경계 (§3-10) · 끝벽 효과 |
| Fig. 14–16 (`fig_14.png` · `fig_15.png` · `fig_16.png`) | ★ Bed Behavior Diagram (자갈 · 석회석 · 모래 · 위 Fr–f · 아래 μ_W–f) | §3-8 판독 · 우리 드럼 판 BBD 를 같은 식으로 그릴 틀 |
| 식 크롭 54 장 (`eq_01_…` – `eq_54_…`) | 번호 식 전부 (식 14 는 인쇄된 ρ_g 그대로) | 보고서 믹서 절에 붙일 식 (식 1 · 3 · 4 · 23 · 38 · 39 · 45 · 48 · 52 · 53 이 핵심) |
| 근거 문단 20 장 (`txt_p1_…` – `txt_p19_…`) | 초록 · 범위 · 꼴 정의 · Fr · 정수압 · 미끄럼 해석 · 무너짐 선행 · 단순화 · 식 39 · Rutgers · 모래 1.48 · 볼 밀 · Teubner/Watanabe · 실험 4.1 · Jenike · 실험 4.2 · BBD 기준 · 흐름성 · 요약 | 원문 인용용 (파일 이름의 pN = PDF 쪽) |

## 6. Post-processing ★
- **원문이 한 것**: 닫힌 식 유도 · 식 곡선 계산 (그림 2 · 4 · 6–9 · 11 · 14–16) · 문헌 측정점 겹치기 · 체류 시간 · 누적 충전율 (그림 10) · 사진에서 경사 구간별 동적 안식각 (그림 12) · 임계 rpm → Fr_c·D/d (그림 13) · Jenike 벽 마찰.  반복 · 오차 · 통계 없음.
- **이 카드의 후처리**: 1-bit 600 dpi 원본 래스터 화소에서 틀 선 검출 · 표지 무게중심 · 선 열 판독 (132 행) → 그림 4 · 7 · 9–16 의 숫자 · 식 23 · 38 · 39 · 45 · 48 · 52 · 53 재계산으로 판독 검산 (2–6 % 안 · 모래 아래 패널 제외) · BBD 의 D 역산 · 모래 아래 패널 Θ 역산 · 식 1 역풀이 (f → ε) · 인쇄 숫자 검산 (f_c 0.0544 · 1/0.675 · ε 57.5° → 17.5 % · Teubner 2.693 / 111.8° · 볼 밀 0.4225–0.5625 · Fig. 12 → Fr·D/d 0.373 · 1.014 · f_min 0.2466) · 우리 드럼 대입 (§3-10 · Fr · ε · 식 23 · 38 · 39 · 48 · 52 · d 선택 다섯 · 39 각형 기하 · 끝판 면적 · rpm 수준표) · 다른 드럼 카드 넷을 이 지도에 (§7-2).  스크립트 = 이 묶음 scratchpad (`dig_*.py` · `analysis.py` · `write_digitized.py`) — 결과는 `digitized.csv` 에 남겼다.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 리포 문서 출처를 병기)

### 7-1. 비교표 (믹서 드럼 DEM)
| 항목 | 이 논문 | 우리 (믹서 B 덱) | 같음 / 다름 · 왜 |
|---|---|---|---|
| 방법 | 해석 힘 · 모멘트 모형 + 전이 관찰 실험 | LIGGGHTS DEM (Hertz–Mindlin · SJKR 점착 · 구름 CDT) | 이 논문 = 꼴 판정의 틀 · 우리 = 꼴이 결과로 나오는 계산 |
| 드럼 | 무배플 원통 · L/D > 0.3 (실험) · D 0.2–0.5 m · 4.6 m 가마형 | 39 각형 · R 12.583 mm · L/D 0.20 · 끝판 회전 | 우리 드럼은 원문 범위 밖 (다각형 · 짧음 · 회전 끝판) |
| 입자 | 자유유동 단분산 규사 · 자갈 · 석회석 0.24–3 mm | parcel 0.151 · 0.606 · 1.363 mm (실입경 1 · 4 · 9 µm · CGF 151.4) · 3 상 | 다분산 · 점착 = 범위 밖 |
| 점착 · 벽 | 없음 · 벽 마찰 μ_W 0.47 (규사/유리) · 0.675 (모래 · 가마) | SJKR 쌍별 · 벽 γ 비 0.00256 · 입자–벽 μ_s 0.9 · μ_r 0.075 | 우리 유효 층/벽 μ_W 는 [미확인] (덤프 측정 필요) |
| Fr · 충전율 | 10⁻⁵–10 · 0–0.5 (실험 0.05–0.25) | 0.0827 · 0.30 | 우리 = 폭포 꼴 창 [카드 산술] |
| 관측량 | 꼴 (사진) · 동적 안식각 · 체류 시간 | M · SE 군집 몫 · AM 접촉 SE · 초기 AM 보존율 | 우리 판독에 **꼴 관측량 (Θ · Θ0 · 표면 곡률 · 이탈 · 미끄럼) 이 없다** → 추가 대상 |

### 7-2. ★ 다른 드럼 카드를 이 지도에 [카드 산술 · 각 카드 값 그대로]
| 카드 | 드럼 · 입자 · 충전 · Fr | 표 1 띠 | 식 39 (2d/D) | 원문 측정 (그림 13 가운데 f 0.26 · 0.371 d/D) | 그 카드의 꼴 가정 |
|---|---|---|---|---|---|
| `liu2013_…` | D 70 mm · d 1.3 mm · 30–92 % · Fr 0.001 · 0.0088 · 0.048 (5 · 15 · 35 rpm) | 5 rpm 구름 · 15 rpm 구름/폭포 겹침 · 35 rpm 폭포 | Fr_c 0.037 → 5 · 15 rpm 구름 · 35 rpm 폭포 | 0.0069 → 15 rpm 도 폭포 | 모형이 *"rolling regime"* 가정 (그 카드 §3-9) — 15 rpm 은 경계 근처 |
| `jarray2019_…` | D 121 mm · d 1.7 mm (r 0.85) · 35 % · 25 rpm · Fr 인쇄 0.21 · 식으로 0.042 (그 카드 L60–62) | 폭포 | 0.028 → 폭포 | 0.0052 → 폭포 | 원문 *"cascading regime"* = 이 지도와 맞음 |
| `chaudhuri2006_…` | D 90 mm (본문) / ≈180 mm (그림 축 · 그 카드 L31 · 서로 어긋남) · d 2 mm · 50 % (그림 판독 ≈55 %) · 12.5 · 20 · 30 rpm → Fr 0.0079 · 0.020 · 0.045 (R 4.5 cm) / 0.016 · 0.040 · 0.091 (R 9 cm) | R 4.5: 구름/폭포 겹침 · 폭포 · 폭포 / R 9: 폭포 셋 | D 90: 0.044 → 12.5 · 20 rpm 구름 · 30 rpm 경계 (1.02 배) / D 180: 0.022 → 12.5 rpm 구름 · 20 · 30 rpm 폭포 | D 90: 0.0082 → 12.5 rpm 경계 · 20 · 30 rpm 폭포 / D 180: 0.0041 → 셋 다 폭포 | 꼴 미기재 [그 카드] |
| `khakhar1999_…` | 준 2D 반 채움 · d 0.8 · 2.0 mm · Fr = ω²L/g 1.6–6.2 × 10⁻⁴ (L = 반 길이) | 구름 띠 | 용기 크기 미기재 → [미확인] | — | *"rolling regime"* — 이 지도와 맞음 |
| **우리 B 덱** | 39 각형 25.2 mm · parcel · 30 % · **0.0827** | **폭포** | 0.012–0.108 → 1.4–6.9 배 위 (AM_P 만 0.76) | 0.0022–0.020 → 4–37 배 위 | khakhar · liu2013 카드의 흐름층 대입은 구름 꼴 전제 → **우리 Fr 에서 그 전제 재확인 필요** |
- ⇒ 우리 드럼 (Fr 0.0827) 은 이 다섯 가운데 Fr 가 높은 쪽이다 (Chaudhuri 30 rpm 을 그림 축 R 9 cm 로 읽은 0.091 만 더 높다) — 구름 꼴을 전제한 두 모형 카드의 Fr (khakhar1999 실험 1.6–6.2 × 10⁻⁴ · liu2013 주 조건 15 rpm 0.0088) 보다 1–2.7 자릿수 위이고, 같은 폭포 꼴 쪽은 Jarray 25 rpm · Chaudhuri 20 · 30 rpm · Liu 35 rpm 이다 [카드 산술].
- ⇒ 동적 안식각 Θ (식 48 의 던짐 문턱을 정한다) 는 점착 · rpm 에 따라 움직인다 — `nase2001_…` 그림 10 (그 카드 L90): 2 mm 젖음 유리구 28.3 → 26.6° (1.1 → 3.8 rpm · 줄어듦) ↔ 마름 23.0 → 25.0° · 그 드럼은 '임계의 10 %' (구름 꼴 · 그 카드 L82) [다른 카드 값] → 우리 rpm 팔의 Θ 는 팔마다 덤프에서 따로 잰다.

### 7-3. 랩 기준과 나란히
- 이 논문에 압밀 · 기공 · 진밀도가 없다 → 랩 표준 (순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³) 과 **나란히 놓을 숫자가 없다**.

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 혼합 공정 (회전 드럼) 의 **운동 꼴 지도** — 회전 세기 (Fr) · 충전율 · 흐름 물성 → 꼴 (미끄럼 · 혼합 계열 · 분쇄 계열).
- **없는 것**: 입자 계산 · 점착 · 다상 · 혼합 정도 정량 · 압밀 · 수송 · MPM ⇒ 우리 Ⓒ 코팅 활물질 믹싱의 **첫 단계 (혼합) 에서 '어느 꼴로 돌리는가' 를 정하는 틀** 만 준다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문은 압밀 계획 바깥 (흐름 밖: Ⓒ 믹서) 이다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (판정 기준 결과 전 등록) | ★ 흐름 밖 (Ⓒ 믹서): rpm 팔을 등록하기 **전에** 꼴 판정 규칙 (식 23 · 38 · 39 · 48 + 덤프에서 잴 Θ · Θ0 · 표면 곡률 · 이탈 입자 · 벽 미끄럼) 과 각 팔의 예상 꼴 (§3-10 표) 을 적는다 — 꼴이 바뀌는 팔과 꼴 안 팔을 결과 전에 가른다 | 기공 연산자 · 압밀 판정 기준 없음 |
| **단계 1–6** (3D 메모리 · 2D MPM · 접촉 표현 · 순수 SE · 복합 압밀 · 탈압) | 없음 | — |
| **단계 7** (형상 · 피복 · 수송) | 없음 (혼합 상태 → 압밀 → 수송으로 넘기는 사슬 없음) | — |
| **후보 D0** (지금 DEM) | 회전 드럼 DEM 의 꼴은 Θ (μ_s · μ_r 가 정함) · 유효 벽 마찰 · d/D 로 정해진다는 틀 → 우리 덱의 μ_r 0.075 (비구형성 대리) · μ_s 0.9 가 Θ 를 거쳐 꼴 경계를 움직인다 [카드 추론] · Watanabe 의 linear spring–dashpot DEM 이 원심 경계를 실험과 맞춘 선례 (p.263) | DEM 한계 진술 없음 · 연화 · 압밀 없음 |
| **후보 A′-0 · A · A′ · B · C · C′ · M0** | 없음 | — |
| **U0–U6** | U2 (경사면 마찰 접촉 회귀) 의 **드럼 판**: 매끈한 벽 · 낮은 충전에서 미끄럼 (sliding) 이 식 23 의 μ_W,c 를 경계로 나타나는지 = 믹서 DEM 의 벽 마찰 단위 시험 (흐름 밖) | 다물체 · 해상도 시험 없음 |
| **R1–R7** | 없음 (압밀 조건) — R2 (미끄럼 · 분리) 의 '층 전체가 벽에 미끄러짐' 은 개념만 닮음 | — |
| **결과 전 대조 항목** (흐름 밖: Ⓒ 믹서) | ① **우리 Fr 0.0827 · f 0.30 = 폭포 꼴 (콩팥 꼴 표면 · 경사 구간별 기울기 갈라짐)** 예측 ↔ 덤프의 표면 꼴 ② 던짐 문턱 Fr = sin(Θ + ε − 90°) — 덤프에서 Θ 를 잰 뒤 값으로 (Θ 30° 면 0.197) ③ 미끄럼 없음 (유효 μ_W > 0.24–0.36) ↔ 벽 미끄럼 속도 ④ 구름 ↔ 폭포 경계는 식 39 ↔ 원문 측정이 5–20 배 갈린다 → 경계 근처 팔 (Fr 0.0088) 은 측정으로만 판정 ⑤ 끝벽 영향 (L/D 0.20) — 끝판 근처 ↔ 가운데 기울기 차 | 크기 · 문턱 전이 금지 (자유유동 · 단분산 · 원통 · 2D 모형) |

- **재료 · 차원 · 조건 차이**: 규사 · 자갈 · 석회석 (mm · 자유유동) ↔ 우리 NCM · LPSCl parcel (실입경 1–9 µm · 점착) · 2D 단면 모형 + 3D 실험 ↔ 우리 3D 짧은 드럼 · 원통 ↔ 39 각형 · 상온 대기 ↔ 우리 진공 DEM (기체 없음).

## 9. 적용 인사이트 (행동)
1. **rpm 팔마다 꼴을 덤프에서 판정한다 (흐름 밖: Ⓒ 믹서 · 단계 0)** — 동적 안식각 Θ (표면 선형 맞춤) · 경사 구간별 기울기 (κ < Θ_m · κ > Θ_m 갈라짐 = 폭포 · 그림 12 방식) · 정적 안식각 Θ0 (회전 정지 뒤 또는 사태 직전 최대) · 표면 위 접촉 0 입자 수 (던짐) · 층 각속도 ↔ 벽 각속도 (미끄럼) — 이 다섯을 판독기에 넣고, 꼴이 같은 팔끼리만 '점착 대비 효과' 를 견준다 (G1 · G3).
2. **rpm 축 = Fr 0.0088 · 0.0827 · 0.30 (+ 0.13)** [§3-10 표] — 구름 ↔ 폭포 경계를 걸치는 팔 · 기준 · 폭포 ↔ 던짐을 걸치는 팔 (+ 같은 꼴 안 둘째 점).  덱의 Fr 밴드 (0.055–0.086) 밖이라 `--allow-off-band` 와 근거 한 줄 (이 카드) 이 필요하다 · 0.0088 팔은 48 시간 상한을 넘어 나눠 돌린다.
3. **khakhar1999 · liu2013 의 흐름층 · 순환 주기 모형을 우리 드럼에 쓸 때 '구름 꼴 전제' 를 표지한다** — 우리 Fr 0.0827 은 이 지도에서 폭포 꼴이라 평평한 표면 · 얇은 층 (k = δ0/L) 가정이 깨질 수 있다 → 그 카드들의 우리 드럼 대입 (k ≳ 0.1 · 순환 주기) 은 덤프의 표면 곡률을 본 뒤에 쓴다.
4. **coarse-graining 과 꼴** — CGF 151 은 Fr 를 지켜도 d/D 를 151 배 키워 구름 ↔ 폭포 경계를 옮긴다 (식 39) → CGF 를 바꾸는 팔 (또는 실입경 비교) 에서는 Fr 뿐 아니라 Fr·D/d 도 보고한다.
5. **덱의 Fr 앵커 (씽키 컵 밴드 · 1차 출처 미확보) 와 이 지도는 다른 장치** — 이 논문은 수평 회전 원통의 꼴 지도이고 씽키 (자전 · 공전 혼합기) 와의 대응은 다루지 않는다 → '씽키와 같은 Fr' 주장을 이 카드로 받치지 않는다.
6. **흐름 물성을 따로 재면 꼴을 미리 맞힐 수 있다** (G2 방법 꼴) — 우리 실험 쪽 원측정 요청에 '분말의 정 · 동 안식각 · 벽 마찰각 (Jenike 류)' 을 넣으면 이 지도로 실제 혼합기의 꼴을 사전 판정할 수 있다 (흐름 밖: 실험 대조).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "The transverse bed motion in rotating cylinders comprises sliding, surging, slumping, rolling, cascading, cataracting and centrifuging; the transition criteria depend on the Froude number, filling degree, wall friction coefficient, particle-to-cylinder diameter ratio, angle of internal friction and the static and dynamic angles of repose (Mellmann, Powder Technol. 118 (2001) 251–270)."
- "Slipping is governed mainly by the filling degree and the bed/wall friction coefficient, μ_W,c = 2sin³ε sinΘ/[3πf(1+Fr)], whereas the Froude number has little influence at slow rotation (Mellmann 2001, Eq. 23)."
- "The rolling–cascading transition has no physical model; the empirical criterion Fr·D/d ≈ 2 (Blumberg) overestimates the measured critical values (Fr_c·D/d ≈ 0.37 in the undisturbed middle and ≈ 0.09 at the end plates at f ≈ 0.26 for 0.24 mm quartz sand; digitized from Mellmann 2001, Fig. 13)."
- 국문: *"우리 드럼 (Fr 0.0827 · 충전율 0.30) 은 Mellmann (2001) 의 전이 기준식으로 보면 폭포 (cascading) 꼴 창 안이다 — 구름 경계의 1.4–7.7 배 위 · 던짐 경계 (동적 안식각 30–40°) 의 0.23–0.42 배 (이 카드 산술 · 원문 범위 밖 외삽)."*
- 국문: *"회전 드럼의 운동 꼴은 Fr 하나로 정해지지 않는다 — 구름 ↔ 폭포는 Fr·D/d, 폭포 ↔ 던짐은 동적 안식각 + 충전각, 미끄럼은 충전율과 벽 마찰이 정한다 (Mellmann 2001)."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
**원문이 스스로 적은 한계**
1. **무배플 원통 · 자유유동 단분산 층 한정** (p.252) · 표 1 범위는 방향 잡이 값 (p.252).
2. 벽 압력 정수압 가정 (Janssen 대비 ≈12 % 높음 · p.255).
3. 미끄럼 판정: *"further experiments are neccessary to prove this criterion"* (철자 = 원문 그대로) (p.265).
4. 식 36 의 물성은 재기 어렵다 → 세 근사 · Θ0 1° 오차에 Fr 3–6 배 (p.258) · 무너짐 단계 충돌 손실 모름 (p.257).
5. 구름 ↔ 폭포 = 경험식 · 모형 없음 · 큰 규모에서 검증 안 됨 (p.260 · p.268) · 측정이 식에서 벗어남 (p.265).
6. 식 45 는 단일 입자 엄밀 (p.261) · 식 52 는 볼 ≪ 원통 · φ_i + ε > 90° (p.263) · Θ + ε = 90° 의 계단은 단일 입자 꼴 (p.268).
7. *"Continuing studies are necessary to experimentally test the criteria worked out and improve the mathematical models developed."* (p.269)

**카드가 본 한계 · 원문 안 어긋남**
8. **점착 · 점착 대비 · 다분산 · 다각형 벽 · 짧은 드럼 · 회전 끝판 = 범위 밖** — 우리 드럼 판정은 외삽 [카드 산술].
9. BBD 의 **D · φ_i 미기재** (판독 역산 D ≈ 0.40 m) · μ_W 0.675 를 세 재료에 공통 (모래 가마 값 · 출처 [25] = 저자가 공저한 **미발표 연구 보고서** (Huckauf · Schlegel · Hoyer · Mellmann · Rensch, IBU-tec GmbH Weimar / Otto-von-Guericke-Universität Magdeburg, 1995 · 원문 목록 *"Forschungsbericht (unveröffentlicht)"*)).
10. **그림 16 아래 패널 = Θ ≈ 37.5° 꼴** (표 2 모래 32.5° 와 어긋남) [판독].
11. BBD 의 구름 ↔ 폭포 선은 식 39 → 저자 측정보다 1.2–22 배 높은 Fr 에 그려졌다 (폭포가 실제로는 더 낮은 Fr 에서 시작할 수 있다).
12. 식 14 의 ρ_g (다른 식은 ρ_b) · 그림 4 의 Henein 선을 본문이 'slipping criterion' 이라 부름 · 'slumping 이 사라진다' ↔ 그림 16 에 띠 남음.
13. BBD 의 측정점 (무너짐 ↔ 구름) 은 Henein [6] 자료 · 저자 측정은 4.1 · 4.2 두 전이뿐 · 반복 · 오차 없음.
14. 2D 단위 깊이 모형 — 끝벽 마찰 모멘트 · 끝벽 끌림은 모형에 없다 (실험에서만 확인).
15. **절대값 전이 금지** — 재료 (규사 · 자갈 · 석회석 mm) · 크기 · 점착 · 드럼 꼴이 모두 다르다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| [6] | H. Henein, J.K. Brimacombe, A.P. Watkinson, Experimental study of transverse bed motion in rotary kilns, Metall. Trans. B 14B (3) (1983) 191–220. | ★ BBD 의 원형 · 무너짐 ↔ 구름 측정 · 자갈 · 석회석 물성 (표 2) · 이 논문이 고쳐 쓴 미끄럼 · 사태 판정 | 없음 (`khakhar1999` 가 인용 · wishlist L722 에 있음 — 거기 서지는 *"14, 191–197"*) |
| [8] | W. Blumberg, Selektive Konvektions- und Kontakttrocknung im Drehrohr. VDI Fortschrittsbericht Nr. 384, VDI-Verlag, Düsseldorf, 1995. | 식 39 (Fr·D/d ≈ 2) 의 원전 · 조건 (원통 크기 · 재료) | 없음 |
| [24] | H. Watanabe, Critical rotation speed for ball-milling, Powder Technol. 104 (1999) 95–99. | DEM (linear spring–dashpot) 으로 원심 경계를 실험과 맞춘 선례 · f_min | 없음 |
| [21] | G. Metcalfe, T. Shinbrot, J.J. McCarthy, J.M. Ottino, Avalanche mixing of granular solids, Nature 374 (2) (1995) 39–41. | 무너짐 꼴의 혼합이 f ≈ 0.5 에서 사라짐 | 없음 (`khakhar1999` · `liu2013` · `nase2001` 인용 · `stewart2001` 은 같은 그룹 1996 논문 · wishlist L725 — 거기 제목은 *"… granular materials"*) |
| [2] | A.A. Boateng, P.V. Barr, Modelling of particle mixing and segregation in the transverse plane of a rotary kiln, Chem. Eng. Sci. 51 (17) (1996) 4167–4181. | 구름 꼴의 혼합 · 분리 ('segregated core') — 우리 AM/SE 크기 분리 | 없음 |
| [3] | R. Rutgers, Longitudinal mixing of granular material flowing through a rotating cylinder, Chem. Eng. Sci. 20 (1965) 1079–1087, 1089–1100. | 미끄럼 Fr 10⁻² · 폭포 ↔ 던짐 Fr 0.3–0.36 | 없음 (정본 papers/ 의 'Rutgers' 는 둘 다 Rutgers University 소속 표기 — 이 원전 인용 아님) |
| [5] | M. Cross, The transverse motion of solids moving through rotary kilns, Powder Technol. 22 (1979) 187–190. | 식 23 의 원형 (원심 없는 모멘트 균형) | 없음 |
| [13] | G. Teubner, Neue Erkenntnisse zur Vorausberechnung der Bewegungsvorgänge und des Leistungsbedarfes in und von Drehtrommeln, … Wiss. Z. HAB Weimar 24 (4/5) (1977) 415–422. | 식 50–51 (단일 입자 원심) | 없음 |

## 13. [미확인] 목록 (원문 20 쪽 전수에 없음)
1. BBD 계산의 드럼 지름 D · 내부 마찰각 φ_i (판독 역산 D ≈ 0.40 m).
2. 실험 4.1 의 rpm · 원통 기울기 · 질량 유량 값 · 반복 / 4.2 의 실험 rpm 목록 · 반복 · 오차 · 앞판 회전 여부 (원통에 붙어 도는지).
3. 표 1 범위의 출처 (문헌 · 저자 경험의 구분).
4. Korotich · Lehmberg 실험의 충전율.
5. 식 39 의 Blumberg 실험 조건.
6. 우리 쪽: 덤프의 Θ · Θ0 · 유효 벽 μ_W · 표면 곡률 (꼴 판정 입력) — 아직 안 잼.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-24)
- 서지: 후보 표 N-154 · 지시서 메모 (J. Mellmann · 제목 · Powder Technol. 118 (2001) 251–270) = 원문 첫 쪽과 같음 · DOI 문자열은 원문에 없고 PII S0032-5910(00)00402-2 인쇄 (첫 쪽 아래 · PDF 메타 제목) — DOI = 10.1016/ + PII · 접수 · 수정 날짜 · 소속 · 이메일 · 키워드 6 개 확인 · SI 안내 없음 (20 쪽 글자 층 전수 · 'doi' 0 회).
- 숫자: 글자 층 + 렌더 (식 220–400 dpi · 그림 · 표 600 dpi) 로 대조 — 표 1 전 칸 · 표 2 아홉 값 · 식 1–54 · 12 % · 6.9 × 10⁻⁴ · 0.31 m · 25–40° · 10⁻² · 2 × 10⁻⁵ · 3- to 6-fold · Fr·D/d ≈ 2 · 0.3–0.36 · 34° · 0.675 · 1.48 · 32.5° · 57.5° · 17.5 % · 0.25–0.72 · 15 % · 0.35–0.50 · 65–75 % · 0.42–0.56 · 0.4 · 2.7 · 111.8° · L 0.124 · D 0.76 m · 30 % · 0.066 · 70 % · 4.6 m · 0.3 m · 0.27 mm · 32.4° · 0.009 · 0.04–0.06 · 2 kPa · 22.7–26.5° · 0.47 · 19 % · 0.165 · 0.054 · 0.24 · 0.5 · 0.75 · 1.0 mm · 0.5–10 min⁻¹ · 0.05–0.25 · 200 · 300 · 500 mm · L/D > 0.3 · 2 · 3.3 min⁻¹ · 10⁻⁴–10⁻² · 0.675 (BBD) · 0.2.
- 그림: 16 장 + 표 1 = 1-bit 600 dpi 래스터 → 원본 화소 판독 (132 행) · 판독 ↔ 식 재계산 대조 (그림 4 식 38 선 · 그림 13 식 39 선 1.97 · 그림 12 ↔ 그림 13 f 0.10 점 · BBD 계단 · 평평한 선 · 무너짐 ↔ 구름 · 폭포 ↔ 던짐 2–6 % · 아래 패널 자갈 · 석회석 Θ ±0.6°).
- 크롭 92 장 전부 열어 확인 (도구 15 그림 → 600 dpi 다시 자름 · 표 1 다시 자름 (도구가 캡션 위 본문을 자름) · 그림 5 · 표 2 손 크롭 · 식 54 · 근거 문단 20 · 식 15 위 티 제거 · 식 17/18 손 분리 · 식 38 분자 잘림 → 다시 자름).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 + 'Mellmann' · 'transverse motion of solids' · PII grep — 카드 없음 · 인용한 카드도 없음 (2026-11-24) · 같은 해 · 같은 저자 다른 카드 없음.

## 🔗 관련 카드
- 드럼 흐름층 · 구름 꼴 기구학: `khakhar1999_chaotic_mixing_granular_2d_tumbling_mixers_flowing_layer` (그 카드의 *"우리 Fr 0.083 이 구르기 영역인지"* 질문에 이 카드 §3-10 이 답한다 — 폭포 꼴 창).
- 점착 × rpm × 충전율 드럼 DEM: `liu2013_wet_cohesive_particles_transverse_mixing_rotating_drum_circulation_period` (구름 영역 가정 · 같은 충전율 규약) · `chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed` · `jarray2019_cohesion_driven_mixing_segregation_drum` ('cascading regime') · `nase2001_granular_bond_collision_number_wet_cohesion` (드럼 동적 각 · 임계의 10 %).
- 점착 혼합 상태도 (점착 축 — 이 지도에 없는 축): `li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy` · `li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation` · `figueroa2009_vdw_adhesion_mixing_segregation_bond_number_phase_diagram`.
- 혼합 지수: `lacey1954_particle_mixing_theory_index`.
- 원심 꼴 (ω²R/g 14–224) 코팅 장치 (메카노퓨전 · 안쪽 조각 + 긁개) 의 2D DEM — 챔버 지름 25 mm 로 우리 드럼과 같고 운동 체제가 다르다 (2026-11-24 카드): `chen2004_mechanofusion_dry_coating_dem_2d_host_scraper_inner_piece_collision_frequency`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
