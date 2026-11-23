<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 (후보 표 N-155 · 4 순위 · 1저자 11-23 업로드 · 믹서 논지 · 코팅 과정 DEM 구현 시도 Q3) 에서 꼭 뽑으라고 한 항목.
     본 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표) · 믹싱 · 점착 절 구성 = jarray2019_cohesion_driven_mixing_segregation_drum.md · 같은 묶음 이웃 = mellmann2001_… (§0-2 공백 검사 꼴 · 우리 드럼 대입 절).
     쪽 표기 = 인쇄 쪽 "p.NNN" (Powder Technol. 146 (2004) 121–136 · PDF n 쪽 = 인쇄 p.(120 + n) · figures.json 의 page 와 크롭 이름 txt_p<n> · eq 의 page 는 PDF 쪽).  보충 자료 (SI) 안내 없음 · 표 2 · 그림 20 · 번호 식 12 + 번호 없는 시간 간격 식 1 · 참고문헌 16.
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자 / [판독] = 그림에서 읽은 값 (그림은 전부 벡터 — PyMuPDF get_drawings 로 막대 꼭대기 · 표지 중심 · 경로 꼭짓점의 정확한 좌표를 읽고 눈금 · 격자선으로 환산 · 재현 = litdb/figures/<slug>/digitized.csv 337 행 · 축 환산 오차 ≈ 0.3–0.6 pt) /
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산 (식 · 가정 병기) / [우리 산술] = 원문 밖 값 (우리 덱 · 리포 문서 · 다른 정본 카드) 과 엮은 계산 / [카드 추론] · [카드 해석] = 이 카드의 해석 / [미확인] = 원문 16 쪽 전수에 없음.
     글자 층은 그리스 문자 · 첨자를 깨뜨린다 ('=' → '¼' · α → 'a' · μ → 'l' · γ → 'c' · Δ → 'D' · ω → 'x' · ' → 'b … Q') — 인용한 숫자 · 식은 전부 300–400 dpi 렌더로 확인했다.  압밀 · 탈압 · MPM · FEM 은 이 논문에 없다. -->
# 메카노퓨전 (회전 챔버 + 고정 안쪽 조각 + 고정 긁개) 장치의 2D DEM — Walton–Braun 부분 걸쇠 스프링 (K1 20,000 N/m · e 0.85 · 점착 없음) · host 1500 개 (반지름 0.2 mm · 1.20 g/cm³) · 챔버 25 mm · 안쪽 원통 10 mm · 틈 1.6 mm · 2000 rpm 10 s: 긁개가 벽에 붙는 층을 깨 운동 세기 지표 2.4 배 · 법선 충돌 속도 2.0 배 · 안쪽 조각 힘 ∝ ω^1.98 (Yokoyama 실험과 같은 꼴) · 입자당 충돌 1.5 × 10⁴ /s (안쪽 조각 · 입력 영역) — 게스트 · 점착 · 막 형성 없음 — Chen · Dave · Pfeffer · Walton (Powder Technol. 2004)

> slug `chen2004_mechanofusion_dry_coating_dem_2d_host_scraper_inner_piece_collision_frequency` · DOI `10.1016/j.powtec.2004.07.014` · type `DEM (2-D soft-sphere · Walton–Braun partially latching spring normal force K1 / K2 = K1/e² + incrementally slipping friction tangential force (K0 = sK1 / sK2, γ = 1) · leap-frog · cohesionless · monodisperse host spheres r 0.2 mm restricted to a plane · chamber / inner-piece = boundary particles · scraper = fixed particles · zero gravity in-plane · 3-D check runs (periodic / rigid end walls, 10 diameters) · validation = exponent of the inner-piece force vs Yokoyama 1987 experiments (reproduced figures) · no guest particles · no adhesion · no film formation)` · PDF `8f6e1608-Numerical_simulation_of_mechanofusion_system.pdf` · digested `2026-11-24` · status ✅
>
> **원제**: *Numerical simulation of Mechanofusion system* (p.121)
> **저자**: **Wenliang Chen**ᵃ · **Rajesh N. Dave**ᵃ\* (교신 · rajesh.n.dave@njit.edu) · **Robert Pfeffer**ᵃ · **Otis Walton**ᵇ — ᵃ New Jersey Center for Engineered Particulates, New Jersey Institute of Technology, Newark, NJ · ᵇ Grainflow Dynamics, Livermore, CA (p.121) · *Powder Technology* **146** (2004) **121–136** · 접수 2003-10-07 · 수정본 2004-07-13 · 게재 확정 2004-07-13 · 온라인 2004-09-21 · 키워드 *Dry particle coating; Mechanofusion; Discrete element simulations; Soft-sphere modeling* · 첫 쪽에 *"doi:10.1016/j.powtec.2004.07.014"* 인쇄 · 연구비 NSF CTS-9985618 · New Jersey Commission on Science and Technology (p.135).
> **이웃 카드 (링크만)**: [`pfeffer2001_dry_particle_coating_engineered_particulates`](pfeffer2001_dry_particle_coating_engineered_particulates.md) (같은 NJIT 그룹 총설 · 이 논문의 ref [2] · 메카노퓨전 원리 · MAIC 의 Walton 형 DEM) · [`walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem`](walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem.md) (공저자 Walton 의 접촉 법칙 3D 판 · ref [10]) · [`kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact`](kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact.md) (같은 꼴 장치 (Hosokawa AMS-Mini) 로 LPSCl 을 NCM811 에 입힌 실험) · [`kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable`](kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable.md) (고강도 믹서 메카노퓨전 + 거친 입자 DEM · 점착 없음) · [`chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed`](chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed.md) (같은 Walton–Braun 법칙 + 상수 인력 점착의 드럼 DEM) · [`mellmann2001_transverse_bed_motion_rotating_cylinders_slumping_rolling_cascading_froude`](mellmann2001_transverse_bed_motion_rotating_cylinders_slumping_rolling_cascading_froude.md) (드럼 운동 꼴 — 메카노퓨전 = 원심 꼴 쪽).
> **판독 원자료**: `litdb/figures/chen2004_mechanofusion_dry_coating_dem_2d_host_scraper_inner_piece_collision_frequency/digitized.csv` (337 행 — 그림 7 · 8 · 9 고리 영역 막대 42 · 그림 10 시간 곡선 36 · 그림 11a 8 · 11b 13 · 그림 12 15 · 13a 15 · 13b 경로 꼭짓점 · 그림 15–18 막대 36 · 그림 19 · 20 누적 충돌 144) · 크롭 **55 장** (그림 20 + 표 2 = 도구 22 장 전부 다시 자름 · 식 13 (번호 식 12 + 시간 간격 식) · 근거 문단 20) — `figures.json`.
> **이 카드가 서랍에 들어온 이유**: 후보 표 N-155 (1저자 11-23 업로드 · 믹서 논지) — *"코팅 장치 (메카노퓨전) DEM 의 첫 선례 (2D · Walton–Braun 탄소성 · 점착 없음 · host 만) = 코팅 과정 DEM 구현 시도 (1저자 11-23 Q3) 의 출발점"*.

> ★★ **한 줄로 왜 중요한가**: (i) 코팅 장치 속에서 **어디서 · 얼마나 자주 · 얼마나 세게** host 가 부딪히는지를 기능 영역 넷 (안쪽 조각 · 긁개 · 입력 · 자유 확산) 으로 나눠 **입자당** 으로 낸 판독 틀 — 입자당 충돌 1.54 × 10⁴ /s (안쪽 조각) · 1.52 × 10⁴ (입력) ↔ 3.14 × 10³ (자유 확산) [인쇄 표 2] · 법선 충돌 속도 0.07–0.42 m/s [판독] · 평균 법선 힘 2.0–4.4 × 10⁻³ N [판독].  (ii) **긁개 (scraper) 가 없으면 원심으로 벽에 붙은 층이 챔버와 같이 돌아** 충돌이 '스치는' 꼴이 되고 운동 세기 지표가 2.4 배 · 법선 충돌 속도가 2 배 낮아진다 [판독 · 카드 산술] = 벽 부착이 충돌 세기를 깎는 입자 수준 대조 (점착이 아니라 원심 · 무점착).  (iii) 안쪽 조각 힘 ∝ ω^1.98 (계산 · 1000–4000 rpm) — 저자들은 Yokoyama 실험 (본문 'normal 2.1 승') 과 같다고 했지만 다시 그린 실험 그림의 기울기는 1.70 [판독] 이다.  (iv) **연화 강성의 정직한 고백**: *"using small value of stiffness will provide inaccurate results for the contact forces"* · 결과는 *"primarily as qualitative indications"* — 운동학 (시간 평균 운동량 전달) 은 강성에 둔하지만 순간 힘 · 접촉 시간은 아니다.
> ⚠ 단 **2D (3D 점검 셋) · 점착 없음 · host 단분산 한 종 · 게스트 0 · 막 형성 0 · 실제보다 작은 장치 (25 mm · 틈 0.8–1.6 mm ↔ 실제 2–5 mm) · 재료 이름 없음 (밀도 1.20 g/cm³)** — 우리 SE · AM 계로 옮길 것은 **판독 틀과 경향** 이지 크기가 아니다.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 회전하는 원통 챔버 속에 고정된 둥근 안쪽 조각 (press head) 과 고정 긁개가 있는 메카노퓨전 (MF) 건식 코팅 장치를, **host 입자만** (게스트는 0.1–2 wt% 이지만 개수가 너무 많아 제외) 2D 소프트 구 DEM (Walton–Braun 이력 스프링 · 증분 미끄럼 마찰 · 점착 없음) 으로 돌려, 긁개가 있을 때 / 없을 때의 회전 · 운동 에너지 · 충돌 압력을 반지름 방향 등부피 고리 7 개로 비교하고 (긁개 = 벽 덩어리 제거 + 분산), 안쪽 조각에 걸리는 힘을 회전 속도 (1000–4000 rpm) · 채움 (500–1500 개) 의 함수로 계산해 Yokoyama 의 실험과 **멱지수 꼴** 로 맞춘 뒤, 기능 영역 넷의 입자당 힘 · 충돌 속도 · 회전 · 충돌 빈도를 내 *"코팅은 주로 안쪽 조각 영역에서"* 라고 결론 냈다 (p.121–136).

| 우리 질문 (지시서 · 꼭 뽑을 것) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 장치 기하 | 실제 MF: 안쪽 조각–벽 틈 **2–5 mm** · 긁개–벽 틈 **≈0.5 mm** (p.121–122) / 모형: 챔버 지름 **25 mm** · 안쪽 원통 지름 **10 mm** (편심 · 그림 5 중심 ≈ (12.5, 6.5) mm [판독]) · 틈 **0.8–1.6 mm** (기준 1.6 · 1.0 은 '보이지 않음') · 긁개 = host 와 같은 크기 (지름 0.4 mm) 의 **고정 입자 몇 개 · 벽과 틈 0** (표 1 · p.123) · 회전 = 시계 방향 (그림 1 화살표 · 그림 5b 벡터 [판독]) | [인쇄] 표 1 · §3-1 |
| ② ★ DEM (식 · 2D · 크기 · 개수 · 물성 · 시간 간격) | 법선 = **Walton–Braun 부분 걸쇠 스프링** N_l = K1α (누름) · N_u = K2(α − α0) (되돌림) · e = √(K1/K2) (식 1–2) / 접선 = **증분 미끄럼 마찰** K_T = K0(1 ∓ …)^γ · T′ = T + K_TΔS (식 3–4 · K0 = sK1 · sK2 · s < 1 · γ = 1) / leap-frog (식 5–7) · m = (1/6)πd³ρ · I = (1/10)md² (평면에 묶인 구) / **r 0.2 mm · 1500 개 · ρ 1.20 × 10³ kg/m³ · K1 20,000 N/m · μ_pp 0.4 · μ_pw 0.5 · e 0.85** (표 1) / **Δt = πe√(m/2K1)/n · n = 40** (p.123–124) → Δt ≈ 6.7 × 10⁻⁸ s · 10 s = 1.5 × 10⁸ step [카드 산술] · 중력 없음 · 임의 처음 위치 · 작은 임의 속도 (총 운동량 0) | [인쇄] · §3-2 |
| ③ ★ 회전 속도 · 채움 | 1000–4000 rpm (표 1) · 비교 기준 **2000 rpm · 1500 개 · 틈 1.6 mm · 10 s** (p.125) · 채움 스윕 500 · 800 · 1000 · 1200 · 1500 개 × 1000 · 2000 · 3000 rpm (p.131) → 2D 면적 분율 0.15–0.46 (빈 면적 기준) [카드 산술] · 2000 rpm = 벽 속도 2.62 m/s · ω²R/g = 55.9 [카드 산술] | §3-5 · §3-8 |
| ④ ★ 에너지 (운동 · 회전) | 회전 운동 에너지 (식 8 · 챔버 ω 를 빼서 '벽에 붙어 같이 도는' 입자 = 0): 긁개 있음 영역 7 **13.5 J/m³** · 고리 평균 4.08 ↔ 없음 영역 7 **1.41** · 평균 2.45 / 운동 세기 지표 (식 10): 있음 고리 3–7 이 35.8–47.4 · 평균 **32.6 J/m³** ↔ 없음 영역 6 만 50.6 · 평균 **13.7** (2.37 배 · 본문 'more than twice') [판독 · 카드 산술] | §3-4 |
| ⑤ ★ 충돌 압력 | 식 11 의 둘째 (충돌 · 접촉) 항만: 있음 4.97 → **2417** (고리 1 → 7) · 평균 **435** ↔ 없음 1.48 → **5544** · 평균 **914** (2.10 배 · 본문 'nearly twice') [판독 · 단위 표기 'J/m²' — 그림 10b 의 N/m² 와 같은 값 → §3-9] | §3-4 |
| ⑥ ★ 안쪽 조각 힘 | 법선 **9.95 × 10⁻⁴ · 4.01 × 10⁻³ · 9.02 × 10⁻³ · 1.54 × 10⁻² N** (1000 · 2000 · 3000 · 4000 rpm · 1500 개) · 접선 2.27 × 10⁻⁴ … 3.41 × 10⁻³ N · 기울기 **1.98 · 1.96** [판독] (본문 '최적 맞춤 1.97 · 추세선 2') · 법선/접선 4.4–4.6 [판독] (본문 'around 5') · 채움에 따라 오르다 포화 (3000 rpm: 7.1 → 9.1 × 10⁻³ N · 800 → 1500 개) | §3-5 |
| ⑦ ★ 실험 대조 | Yokoyama 등 [3] (Kona 1987 · 그림 11b · 13b 재수록): 폴리스티렌 550 g · 힘 (kg) vs n (rpm) — Fc 0.60 kg (159 rpm) → 11.5 kg (913 rpm) · 기울기 **1.70** · Ft 1.82 → 0.97 (국소) [판독] ↔ 본문 *"normal force varies with the rotational speed to approximately the 2.1 power"* · 탈크 AM-35 접선 힘 vs 채움 무게 (300 · 500 · 800 rpm) = 채움 따라 오르고 기울기 줄어듦 (정성 일치 · 크기 대조 없음) | §3-5 · §3-9 |
| ⑧ ★ 입자 힘 · 충돌 속도 · 빈도 | 기능 영역 넷 (그림 14): 평균 법선 힘 3.52 · 4.37 · 2.09 · 2.05 × 10⁻³ N (안쪽 조각 · 긁개 · 입력 · 자유 확산) · 접선 0.75 · 0.84 · 0.43 · 0.43 × 10⁻³ [판독] / 법선 충돌 속도 있음 0.345 · 0.424 · 0.229 · 0.302 · 평균 0.285 m/s ↔ 없음 0.353 · **0.071** · 0.263 · **0.092** · 평균 0.146 [판독] / 입자당 충돌 (3–10 s 평균 · 1 s 당) 입자–입자 **1.54e4 · 4.92e3 · 1.52e4 · 3.14e3** · 입자–벽 3.31e3 · 8.21e2 · 1.48e3 · 4.81e2 [인쇄 표 2] | §3-6 · §3-7 |
| ⑨ ★ 무엇이 없나 | **게스트 입자 0** (*"impractical to include the fine particles"* p.122) · **점착 0** (*"cohesionless contact model"* p.121 · 그러나 실제 장치에서 입자가 *"adhere to each other and to the chamber wall"* 라고 적는다 p.122) · **막 형성 · 게스트 옮겨 감 · 덩어리 풀림 0** (앞으로의 '게스트 규모 모형' 몫 · p.136) · 열 0 (p.122 서술만) · 실제 힘 크기 0 (연화 강성) · 반복 · 오차 0 | §4-3 · §11 |
| ⑩ '점착 비 기준' (γ_AM/γ_SE · 같은 SE 탐침 AFM 힘 비) | **없음** — 점착 · 점착 대비 · 게스트가 모두 없다 | §0-2 |

⛔ **한정어 (떼지 말 것)**: ① **2D** (평면에 묶인 구 · z 중력 없음 · 3D 점검은 10 지름 두께 둘) ② **점착 없음 · host 한 종 · 단분산 · 게스트 0** ③ 장치가 실제보다 작다 (25 mm · 틈 0.8–1.6 mm) — *"preserving the overall loading of the chamber"* (채움 기준값 [미확인]) ④ 강성이 실제 재료보다 *"much smaller"* — **순간 힘 · 접촉 시간은 정성 값** (p.133) ⑤ 재료 이름 없음 (밀도 1.20 g/cm³ · 실험 대조는 폴리스티렌 · 탈크) ⑥ 실험 대조 = **멱지수 꼴** (2D 슬랩 힘 (N) ↔ 실제 장치 힘 (kg) 크기 비교 없음) ⑦ 반복 · 시드 · 오차 없음 ⑧ 그림 판독값은 [판독] (벡터 좌표 · 축 환산 오차 ≈ 1 % 안).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-155 의 '왜' 칸)

의도 원문: *"후보 표 6 절 (우선순위 4 · 1저자 11-23 업로드 · 믹서 논지) — 코팅 장치 (메카노퓨전) DEM 의 첫 선례 (2D · Walton–Braun 탄소성 · 점착 없음 · host 만) = 코팅 과정 DEM 구현 시도 (1저자 11-23 Q3) 의 출발점"* · 근거 칸 = 1저자 업로드 → **가리킨 카드 없음** (2 차 인용 대조 대상 없음) · 지시서 덧붙임 (꼭 뽑을 것 = 장치 기하 · DEM · 회전 속도 · 채움 · 에너지 · 충돌 압력 · 안쪽 조각 힘 · 실험 대조 · 무엇이 없나 / 우리 질문 = '점착 비 기준' · rpm 공정 축 · 코팅 과정 DEM / 공백 검사 G1–G4).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "코팅 장치 (메카노퓨전) DEM" | **채움** | 제목 · 초록 (p.121) · 그림 1–2 · 5–6 · 표 1 — 회전 챔버 + 고정 안쪽 조각 + 고정 긁개를 DEM 으로 |
| "의 첫 선례" | **원문 주장 없음 (일부)** | 원문은 '처음' 이라 적지 않는다 — *"there has been very little effort devoted to the theoretical analysis of the Mechanofusion system"* + 유일한 앞선 예 = Chen & Huang [7] 의 해석 모형 (*"the interactions among the particles were neglected … the function of the scraper was completely ignored"* p.122) · 같은 그룹의 MAIC DEM 은 `pfeffer2001` 카드 §⑧ 에 있다 (다른 장치) → 'MF 장치 DEM 으로 정본에서 가장 이른 카드' 까지만 말할 수 있다 [카드 추론] |
| "2D" | **채움** | *"using a two-dimensional approximation for the system"* (p.124) · 평면에 묶인 구 (p.125) · 3D 점검 = 주기 경계 · 강체 끝벽, 두께 10 지름 (p.124 · p.130 · 그림 10) |
| "Walton–Braun 탄소성" | **채움 (한정)** | *"a partially latching-spring model proposed by Walton and Braun [9] for an elastic-plastic material"* (p.123) · 초록 *"frictional, elastic-plastic spheres"* — 한정: '탄소성' = **접촉 법칙의 이력 (K2 > K1 · 잔류 겹침 α0)** 이다 · 입자 모양은 안 바뀐다 (§4-2) |
| "점착 없음" | **채움** | *"An existing, widely used, cohesionless contact model (Walton–Braun)"* (p.121) |
| "host 만" | **채움** | *"it is impractical to include the fine particles in this modeling effort"* · *"host/host and host/boundary interactions"* · 단분산 host (p.122) |
| "= 코팅 과정 DEM 구현 시도의 출발점" | **일부** | 주는 것 = 장치 · host 규모의 충돌 통계 (영역별 입자당 빈도 · 힘 · 충돌 속도 · 회전) — 원문 목적 그대로 *"for developing a basis for a full-scale system simulation that may capture the phenomena at multiple length scales"* (p.122) · 게스트 영향은 *"in terms of change in certain properties of the host particles"* 로 나중에 (p.122) / 없는 것 = 게스트 · 점착 · 덩어리 풀림 · 게스트 옮겨 감 · 막 형성 (*"Future work will focus on … guest-scale modeling"* p.136) → 우리 Q3 의 '코팅 과정' 자체는 없다 |
| (꼭 뽑을 것) 장치 기하 · DEM · 회전 · 채움 · 에너지 · 충돌 압력 · 안쪽 조각 힘 · 실험 대조 | **채움** | §3-1–3-7 (표 1 · 식 1–12 · 그림 7–20 판독) |
| (꼭 뽑을 것) 무엇이 없나 | **채움 (없음을 원문으로 확인)** | 게스트 · 점착 · 막 · 열 · 실제 힘 크기 (§0 ⑨ · §11) |
| (우리 질문) '점착 비 기준' | **없음** | 점착 0 · 게스트 0 |
| (우리 질문) 회전 속도 (rpm) 공정 축 | **일부** | 안쪽 조각 힘 ∝ ω^≈2 (계산 1000–4000 rpm · 실험 꼴 대조) · 채움 × rpm 의 힘 지도 (그림 12 · 13a) — 최적 rpm · 코팅 결과 ↔ rpm · 회전에 따른 충돌 속도 · 빈도 변화는 없다 (충돌 통계는 2000 rpm 하나) |
| (우리 질문) 코팅 과정 DEM | **일부** | 장치 규모 판독 틀만 (§7-2) |
| 가리킨 카드의 2 차 인용 값 | **해당 없음** | 근거 칸 = 1저자 업로드 · 정본 카드 가운데 이 논문을 인용한 카드 없음 (papers/ 전수 grep 'Mechanofusion system' · 'powtec.2004.07.014' · 'Wenliang' = 0 건 · 2026-11-24) |

⇒ **의도 대조 결과: 일부** — 장치 (메카노퓨전) DEM · 2D · Walton–Braun · 점착 없음 · host 만은 원문이 채운다 (Walton–Braun 의 '탄소성' 은 접촉 이력뿐) / '첫 선례' 는 원문 주장이 없다 (해석 모형 하나만 앞섬) / '코팅 과정 DEM 의 출발점' 은 장치 · host 규모 충돌 통계까지만 — 게스트 · 점착 · 막 형성은 없다.

---

## 0-2. ★ 공백 검사 G1–G4 — 우리 믹서 논지 문장을 이 논문이 이미 했나 (정독 출력 batch_160 끝 절과 같은 판정)

| # | 우리 공백 문장 (11-23 지시) | 판정 | 근거 (쪽 · 문장) | 반례 · 일부면 우리 문장을 이렇게 좁힌다 |
|---|---|---|---|---|
| **G1** | 점착 대비를 설계 변수로 혼합 결과 (덮임 ↔ 뭉침 · 섞임 ↔ 분리) 를 예측 | **없음** | *"An existing, widely used, cohesionless contact model (Walton–Braun) is used"* (p.121) · 게스트 0 (p.122) · 한 종 단분산 host · 혼합 지수 0 — '덮임' 은 결과가 아니라 **충돌 통계로부터의 추론** (*"powder coating is more likely to occur mainly within the inner-piece and scraper areas where high collisional momentum transfer is occurring"* p.133 · *"most of the coating action should take place in the inner-piece area"* p.135) | 좁힐 필요 없음.  가져올 것 = '어디서 덮일까' 를 **힘 × 빈도 지도** 로 먼저 정하는 판독 틀 (점착 축은 우리가 더한다) |
| **G2** | 점착 입력을 따로 재고 (AFM · IGC · 접촉각 등) 혼합 결과를 미리 예측 | **없음** | 점착 입력 0 · 입력 대부분 *"selected based on expected empirical values"* (p.124) · 실험과 맞춘 것은 **안쪽 조각 힘의 멱지수** 하나 (*"no adjustments were made to any of the assumed simulated particle or wall properties in order to obtain this result"* p.131) | 좁힐 필요 없음.  인용할 선례 문장 = *"장치에서 잴 수 있는 양 (안쪽 조각 힘 · 동력) 의 회전 속도 지수로 DEM 을 점검한 선례 (Chen 2004) — 점착 입력으로 혼합 결과를 미리 맞힌 것은 아니다"* |
| **G3** | 회전 속도 최적을 입자 수준 맞교환 (덩어리 풀림 ↔ 벽 부착 손실 등) 으로 설명 | **일부** | 벽 부착 ↔ 충돌 세기의 **입자 수준 대조는 있다** — 긁개 없음: *"more and more particles get attached to the chamber wall because of the centrifugal force"* (p.127) · *"particles stick to the boundary during the processing, and undergo mostly rigid body rotation"* (p.127) · 법선 충돌 속도 *"twice"* 낮음 · *"glancing"* 충돌 (p.133) · 덩어리 풀림은 결론의 추론뿐 (*"These collisions are likely to cause deagglomeration of the fine guest particles"* p.136) — 그러나 **rpm 은 힘을 단조로 키울 뿐 (∝ ω^≈2) 최적이 없고**, 벽 부착은 rpm 이 아니라 **긁개 유무** 로 바꿨으며, 부착 원인은 점착이 아니라 원심 · 무점착 | 우리 문장을 이렇게 좁힌다: *"벽 부착 (원심 고정) 이 충돌을 '스치는' 꼴로 바꿔 법선 충돌 세기를 반으로 깎는다는 입자 수준 대조는 무점착 2D DEM 으로 이미 있다 (Chen 2004 · 긁개 유무) — 우리 몫은 점착 대비가 있는 계에서 rpm 을 축으로 덩어리 풀림 ↔ 벽 점착 손실의 맞교환과 최적을 보이는 것"* |
| **G4** | 공정 × 재료 상태도 (회전 세기 × 점착 · Bond 수 등) 가 다른 재료로 옮겨 감 | **없음** | 재료 하나 (이름 없음 · 1.20 g/cm³) · 상태도 0 · 회전 × 채움의 **힘 지도** (그림 12 · 13a) 만 · *"Different values, for example, of the coefficient of friction might have a quantitative effect … We plan to include a systematic parametric investigation in a future paper."* (p.124) | 좁힐 필요 없음 |

---

## 1. 한 줄 요약
**메카노퓨전 건식 코팅 장치 (회전 챔버 · 고정 안쪽 조각 · 고정 긁개) 를 host 만 · 점착 없이 2D Walton–Braun DEM 으로 돌려, 긁개가 벽 덩어리를 깨 분산 · 충돌 세기를 두 배로 올린다는 것, 안쪽 조각 힘이 회전 속도 제곱에 비례 (실험과 같은 꼴) 한다는 것, 그리고 기능 영역 넷의 입자당 충돌 빈도 · 힘 · 속도를 낸 16 쪽 계산 논문.**  게스트 · 점착 · 막 형성은 '앞으로의 게스트 규모 모형' 으로 미뤘고, 연화 강성 때문에 힘 크기는 정성 값이라고 스스로 적었다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **W. Chen · R.N. Dave\* · R. Pfeffer · O. Walton** (NJIT · Grainflow Dynamics) | *Powder Technol.* 146 (2004) 121–136 · 16 쪽 | 10.1016/j.powtec.2004.07.014 (원문 인쇄) | 이름 없는 단분산 구 host (반지름 0.2 mm · 1.20 g/cm³) · 경계 = 챔버 · 안쪽 조각 · 긁개 (고정 입자) · 실험 대조 = 폴리스티렌 550 g · 탈크 AM-35 (Yokoyama [3]) · SE · AM · 전극 재료 없음 | **계산 (2D DEM + 3D 점검)** · 실험 0 (남의 실험 그림 재수록) · 압밀 0 |

- **1저자 메모 · 후보 표와의 대조**: 저자 넷 (W. Chen · R.N. Dave · R. Pfeffer · O. Walton) · 제목 · 학술지 · 권 146 · 쪽 121–136 · 2004 · DOI 10.1016/j.powtec.2004.07.014 — **같다** (DOI 는 첫 쪽 아래에 인쇄 · 이름은 원문에서 Wenliang · Rajesh N. · Robert · Otis).
- **글의 꼴**: 1. 서론 (MF 원리 · 다중 규모 문제 · 게스트 제외 이유 · 목표) → 2. 모형 (2.1 기하 · 2.2 접촉 법칙 · 2.3 2D 근거 · 표 1 · 2.4 알고리즘 · 2.5 진단량) → 3. 결과 (3.1 긁개 있음 / 없음 비교: 3.1.1 회전 운동 에너지 · 3.1.2 병진 운동 에너지 (운동 세기 지표) · 3.1.3 입자 압력 · 2D/3D · 3.2 충돌 역학: 3.2.1 안쪽 조각 힘 · 3.2.2 입자 힘 · 3.2.3 충돌 속도 · 3.2.4 충돌 빈도) → 4. 결론 → 참고문헌 16.
- **계보**: Yokoyama 등 1983 [1] (MF 의 기원 · 1980 년대 중반 일본) · Yokoyama 등 1987 [3] (100 가지 넘는 host/게스트 조합 · 안쪽 조각 힘 측정 — 이 논문의 대조 실험) · Tanno 1990 [4] (MF 총설) · Chen & Huang 1997 [7] (MF 의 '작용 구역' 해석 모형 — 입자끼리 · 긁개 무시) · Cundall & Strack 1979 [8] (DEM) · **Walton & Braun 1986 [9]** (접촉 법칙 원전 · 정본 제외 — 내려받기 불가 · `status.tsv` N-72) · Walton 1993 [10] (강성 둔감 · 정본 카드 `walton1993_…`) · Ladd 1988 [14] · Walton 1993 · 1997 [15 · 16] (입자 압력) · Pfeffer 등 2001 [2] (같은 그룹 총설).

---

## 3. 핵심 수치 · 식 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 장치 기하 — 실제 MF ↔ 계산 모형 (p.121–123 · 그림 1 · 2 · 5 · 표 1 · `txt_p1_p2_…` · `txt_p2_operation_…` · `txt_p3_scraper_…` · `tab_1.png`)
| 항목 | 실제 MF (원문 서술) | 계산 모형 | 표지 |
|---|---|---|---|
| 챔버 | 회전 원통 · 한 번에 한 배치 | **지름 25 mm** (원) | [인쇄] p.121–122 · 표 1 |
| 안쪽 조각 (press head) | 고정 · 둥근 끝 · 반지름이 챔버보다 작음 | 편심 **원 (지름 10 mm)** = '큰 고정 입자' (그림 2 캡션) · 그림 5 중심 ≈ (12.5, 6.5) mm · 아래쪽 [판독] | [인쇄] 표 1 · 그림 2 |
| 안쪽 조각–벽 틈 | *"generally ranges from 2 to 5 mm"* | **0.8–1.6 mm** (표 1) · 기준 1.6 mm · 1.0 mm 는 '보이지 않음' (p.133) · 0.8 mm 결과 [미확인] | [인쇄] p.121 · 표 1 · p.133 |
| 긁개 (scraper) | 고정 날 · 벽과 틈 *"usually around 0.5 mm"* · 벽에 붙은 가루를 긁어 다시 흩뜨림 | **같은 크기 (지름 0.4 mm) 고정 입자 몇 개를 비스듬히** · *"zero clearance between the scraper particles and the chamber (without any interaction between scraper and the chamber)"* · 그림 2 · 5b 에서 셋 [판독] | [인쇄] p.121–123 · 표 1 |
| 중력 | (실제 장치 축은 서술 없음) | z 방향 중력 = 2D 라서 **넣지 않음** | [인쇄] p.125 |
| 크기 맞춤 | — | *"the simulated system is much smaller than the actual physical system so that fewer particles can be used, while still preserving the overall loading of the chamber"* (채움 기준값 [미확인]) | [인쇄] p.124 |

- 작동 원리 (p.122): *"When the chamber rotates, powder is forced to the chamber wall by centrifugal action. While passing through the converging space between the rounded inner-piece and chamber wall, mechanical interactions, mainly in the form of high shear-rate collisions, take place … As the particles come out of the diverging space of the inner-piece region, they adhere to each other and to the chamber wall. The blade serves to scrape off the powder attached to the chamber wall."* · *"compression, deagglomeration, and frictional shearing"* · *"a considerable amount of thermomechanical energy may be generated"* · 운전 변수 (국부 온도 · 운전 시간) 를 감시해 열 열화를 막는다.
- 우리 대조 [다른 카드 값]: `kim2023_…` 의 Hosokawa AMS-Mini = 프레스 헤드–벽 틈 **3 mm** · 스크레이퍼–벽 틈 **≈0.4 mm** · 20 g · 2000–5000 rpm (그 카드 L26 · L68 · L73–76) → 이 논문의 '2–5 mm · ≈0.5 mm' 범위 안 · `pfeffer2001_…` 표: MF 외통 200–1600 rpm (그 카드 L76) — 계산 1000–4000 rpm 과 겹치되 위쪽이 넘는다.

### 3-2. ★ DEM 모형 — 식 1–7 · 시간 간격 · 표 1 (p.123–125 · `eq_01_…`–`eq_07_…` · `eq_dt_…` · `txt_p3_p4_…` · `txt_p4_2d_…` · `txt_p4_p5_…` · 그림 3)
- **법선 (식 1–2)**: e = √(K1/K2) (*"assumed to be independent of the impact velocity for the elastic-plastic case considered here"*) · N_l = K1α (누름) · N_u = K2(α − α0) (되돌림 · α0 = 되돌림 선이 0 에 닿는 α = *"finite plastic deformation"*) → K2 = K1/e² = **27,682 N/m** [카드 산술].
- **접선 (식 3–4)**: K_T = K0(1 − (T − T*)/(μN − T*))^γ (T 가 커질 때) · K0(1 − (T* − T)/(μN + T*))^γ (작아질 때) · K0 = sK1 (누름) · sK2 (되돌림) · *"s is less than 1.0"* (값 [미확인]) · **γ = 1 (모든 경우)** · T* = 미끄럼 방향이 바뀔 때의 T (처음 0 · 법선 힘 변화에 비례해 늘임) · T′ = T + K_TΔS — 접촉마다 T 와 T* 둘만 기억.
- **적분 (식 5–7)**: v̇ = F/m · ω̇ = M/I · leap-frog [13] · **m = (1/6)πd³ρ · I = (1/10)md²** = *"for a sphere restricted to a plane, and not for a disk-shaped particle"* (p.125) → m = **4.02 × 10⁻⁸ kg** · I = 6.43 × 10⁻¹⁶ kg·m² [카드 산술].
- **시간 간격 (번호 없음)**: **Δt = πe√(m/2K1)/n · n = 40** (*"the calculation time steps n for each contact"* p.123–124) → Δt = **6.69 × 10⁻⁸ s** · 10 s = **1.49 × 10⁸ step** · 2000 rpm 10 s = 333 바퀴 [카드 산술] · 두 입자 충돌 시간 (π/2)(1 + e)√(m/2K1) = 2.91 µs = 43.5 Δt [카드 산술 · m_eff = m/2].
- **강성 고르기 (p.124)**: *"The normal stiffness K1 is selected according to impact mechanics and the condition that the maximum particle deformation is less than 1%."* → 겹침 1 % (4 µm) 가 되는 상대 법선 속도 = 3.99 m/s [카드 산술 · δ = v√(m_eff/K1)] — 2000 rpm 벽 속도 2.62 m/s · 4000 rpm 5.24 m/s.
- **표 1 (전수 · [인쇄] p.124)**: 반지름 0.2 mm · 개수 1500 · 밀도 1.20 × 10³ kg/m³ · 챔버 지름 25 mm · 안쪽 원통 지름 10 mm · 긁개 지름 0.4 mm · 틈 0.8–1.6 mm · 회전 1000–4000 rpm · 누름 법선 강성 20,000 N/m · 입자–입자 마찰 0.4 · 입자–고체 경계 마찰 0.5 · 반발 계수 0.85.
- **알고리즘 (그림 3)**: 처음 위치 · 방향 · 속도 → 연결 목록 갱신 (새 · 깨진 접촉) → 힘 · 토크 → 운동 방정식 적분 → 평균량 → t = t + Δt.  처음 = *"randomly positioned"* · *"small random velocities; however, the net momentum of the system is initially zero"* (p.124).
- **CPU · 2D 근거 (p.124)**: *"The CPU time increases as n log(n)"* · 2D = 셋째 방향이 무한하거나 그 방향 상호작용을 무시할 수 있을 때 [12] · MF 는 *"transverse x–y plane"* 흐름 → *"The transport of the particle in the third dimension (z-direction) does not play an import role"* (원문 'import' 그대로) · 계산 시간 · 하드웨어 [미확인].

### 3-3. ★ 2D ↔ 3D 점검 (p.124 · p.130 · 그림 10 · `fig_10.png` · `txt_p10_3d_…`)
- 3D 두 가지: z 주기 경계 · 셀 두께 **10 지름** / 양 끝 **강체 벽 · 간격 10 지름** · 긁개 있음 · 0–1 s 시간 평균.
| 양 (0.6–1.0 s 평균) | 2D | 3D 주기 | 3D 강체 벽 | 표지 |
|---|---|---|---|---|
| 운동 세기 지표 (J/m³) | **32.8** | 33.5 (+2.3 %) | 31.4 (−4.2 %) | [판독 · 카드 산술] |
| 평균 충돌 압력 (N/m²) | **435** | 481 (+10.6 %) | **508 (+16.7 %)** | [판독 · 카드 산술] |
- 0.4 s 에 정상 (두 양 모두 0.2 s 4–37 → 0.4 s 정상 값 [판독]).  본문: 운동 세기 2D ≈ 3D 주기 · 강체 벽보다 크다 · 충돌 압력은 강체 벽 3D 가 가장 크다 (*"because of the interactions of particles with boundary walls"*) · *"Generally, the differences are not more than about 10%"* — **강체 벽 충돌 압력 +16.7 % 는 '약 10 %' 를 넘는다** [카드 산술 · §3-9].

### 3-4. ★ 긁개 있음 ↔ 없음 — 진단량 정의와 고리 7 개 (p.125–130 · 식 8–11 · 그림 4–9 · `txt_p5_…` · `txt_p5_p7_…` · `txt_p9_p10_…`)
- **영역 나누기**: 등부피 고리 V_i = V/N · N = 7 · *"the radial width of each zone is equal or greater than the maximum diameter of particles"* → 큰 입자도 한 순간 두 영역까지만 (p.125) · 2D 부피 = 영역 두께를 입자 지름 하나로 (p.127) · 고리 경계 r/R = √(k/7) = 0.378 · 0.535 · 0.655 · 0.756 · 0.845 · 0.926 [판독 = 막대 가장자리 · 식과 0.001 안] · **고리 1–5 의 일부를 안쪽 조각이 차지한다** (틈 1.6 mm · 중심 편심 5.9 mm 가정 → 고리 1–7 의 29 · 28 · 23 · 18 · 12 · 2 · 0 %) [카드 산술 · 기하] — 원문은 이것을 말하지 않는다 (밀도 값이 그만큼 희석).
- **평균 창**: 정상 상태 (2 s 안에 도달) 뒤 2 s (그림 7–9 = 2–4 s) · 진단량 = 영역 부피 평균.
- **식 8** 회전 운동 에너지 E_r^(k) = (1/2V_k)Σ I_i[ω_ix² + ω_iy² + (ω_iz − ω)²] — 챔버 각속도 ω 를 빼 *"if all the particles were glued to the chamber … would be zero"* (p.127).
- **식 9** 편차 병진 운동 에너지 — 영역이 너무 커 국부 평균 속도장을 못 정의 → **식 10 '운동 세기 지표'** (반지름 · 접선 · z 성분을 영역 평균에서 뺀 것 · 2D 라 z = 0) = *"not an accurate measure of the true deviatoric kinetic energy, nor of the granular temperature"* (p.127).
- **식 11** 입자 압력 P = (1/3V_i)[Σ m_i(v_i − v̄_k)² + Σ F_ij R_ij] (Ladd [14] · Walton [15,16]) — 첫 항은 *"only indirectly contribute to collisions"* 라 **둘째 (충돌 · 접촉) 항만** 계산 (p.129–130).

| 고리 (r/R) | 1 (0–0.378) | 2 | 3 | 4 | 5 | 6 | 7 (0.926–1) | 고리 평균 [카드 산술] |
|---|---|---|---|---|---|---|---|---|
| 회전 KE · 있음 (J/m³ · 그림 7a) | 0.48 | 0.69 | 0.96 | 1.44 | 3.06 | 8.43 | **13.50** | 4.08 |
| 회전 KE · 없음 (그림 7b) | 0.14 | 0.38 | 0.69 | 1.28 | 3.24 | **10.00** | 1.41 | 2.45 |
| 운동 세기 · 있음 (J/m³ · 그림 8a) | 6.06 | 17.2 | 35.8 | **47.4** | 42.8 | 42.3 | 36.6 | **32.6** |
| 운동 세기 · 없음 (그림 8b) | 1.96 | 5.00 | 5.16 | 7.33 | 18.5 | **50.6** | 7.57 | **13.7** |
| 충돌 압력 · 있음 (축 'J/m²' · 그림 9a · 로그) | 4.97 | 7.80 | 23.2 | 77.6 | 227 | 285 | **2417** | **435** |
| 충돌 압력 · 없음 (그림 9b) | 1.48 | 1.97 | 3.83 | 27.9 | 236 | 580 | **5544** | **914** |
(전부 [판독] — 막대 꼭대기 벡터 좌표 · 격자선 환산 · digitized.csv)

- 읽기: 있음 = 바깥 절반 (고리 3–7) 에 운동 세기가 고르다 · 회전 KE 가 바깥으로 커진다 (벽 고리가 가장 큼) / 없음 = 벽 고리 7 의 회전 KE 가 작고 (벽과 같이 돈다) 운동 세기는 안쪽 조각과 부딪히는 고리 6 에만 크다 / **고리 평균 비 (있음/없음): 운동 세기 2.37 배 (본문 'more than twice') · 충돌 압력 0.48 배 (= 없음이 2.10 배 · 본문 'nearly twice') · 회전 KE 1.67 배** [카드 산술].
- 고리 평균 ↔ 그림 10 의 2D 정상 값: 운동 세기 32.6 ↔ 32.8 · 충돌 압력 434.6 ↔ 435.1 (0.1 % 안) [판독 · 카드 산술] → 그림 10 의 '평균' = 고리 7 개의 단순 평균 (등부피) 이고 그림 9 의 단위는 그림 10b 와 같은 N/m² (= J/m³) 로 읽힌다 [카드 추론 · §3-9].
- 정성 (그림 5 · 6 · p.127): 있음 = *"particles are well dispersed … within the first 2 s, the system is close to steady state"* · 벡터 = *"zones of swirls and chaotic motion"* / 없음 = *"more and more particles get attached to the chamber wall because of the centrifugal force"* · *"the particles essentially move in a tangential direction along the outer wall"* · 벽 층 2–3 입자 두께 + 가운데 뭉친 무리 (그림 6a) [그림 관찰].
- 요동 속도로 옮기면 (운동 세기 고리 평균 × 전체 부피 πR²d ÷ 1500 입자 = ½m v′²): 있음 v′ ≈ **0.46 m/s** · 없음 **0.30 m/s** [카드 산술 · 등부피 고리 · 구 질량 가정 · 벽 속도 2.62 m/s 의 18 % · 11 %].

### 3-5. ★ 안쪽 조각 힘 · 회전 속도 · 채움 · 실험 대조 (p.130–131 · 그림 11–13 · `txt_p10_p11_…` · `txt_p11_loading_…`)
- 정의: 안쪽 조각과의 모든 상호작용을 매 순간 추적 → **계산 전체의 장시간 평균** 법선 · 접선 힘 (p.130) · *"This is a diagnostic quantity that can actually be measured experimentally, and can be used to monitor the system during its operation, and for analyzing power-consumption."* (p.130).
| rpm (1500 개 · 틈 1.6 mm) | 1000 | 2000 | 3000 | 4000 | 로그 기울기 |
|---|---|---|---|---|---|
| 법선 Fn (N · 그림 11a) | 9.95 × 10⁻⁴ | 4.01 × 10⁻³ | 9.02 × 10⁻³ | 1.54 × 10⁻² | **1.98** |
| 접선 Ft (N) | 2.27 × 10⁻⁴ | 8.79 × 10⁻⁴ | 1.99 × 10⁻³ | 3.41 × 10⁻³ | **1.96** |
| Fn/Ft | 4.38 | 4.57 | 4.53 | 4.52 | — |
([판독] 로그 축 벡터 좌표 · 본문: 추세선 *"power-law constant of 2, which is very close to the actual best-fit value of 1.97"* · Fn/Ft *"around 5"*)

- **채움 × rpm (그림 12 · 13a · 1000 · 2000 · 3000 rpm)** [판독 · N]:
| 채움 (개) | 500 | 800 | 1000 | 1200 | 1500 |
|---|---|---|---|---|---|
| Fn 1000 rpm | 5.0 × 10⁻⁵ | 4.9 × 10⁻⁴ | 7.4 × 10⁻⁴ | 8.3 × 10⁻⁴ | 9.3 × 10⁻⁴ |
| Fn 2000 rpm | 7.4 × 10⁻⁵ | 2.82 × 10⁻³ | 3.41 × 10⁻³ | 4.04 × 10⁻³ | 4.04 × 10⁻³ |
| Fn 3000 rpm | 1.5 × 10⁻⁴ | 7.11 × 10⁻³ | 7.99 × 10⁻³ | 9.02 × 10⁻³ | 9.12 × 10⁻³ |
| Ft 1000 rpm | 1.4 × 10⁻⁵ | 1.24 × 10⁻⁴ | 1.92 × 10⁻⁴ | 2.19 × 10⁻⁴ | 2.46 × 10⁻⁴ |
| Ft 2000 rpm | 2.7 × 10⁻⁵ | 7.09 × 10⁻⁴ | 9.00 × 10⁻⁴ | 1.04 × 10⁻³ | 1.05 × 10⁻³ |
| Ft 3000 rpm | 4.1 × 10⁻⁵ | 1.80 × 10⁻³ | 2.05 × 10⁻³ | 2.28 × 10⁻³ | 2.40 × 10⁻³ |
- 읽기: 500 개는 *"quite small, but are nonzero"* (빈 면적 분율 0.15 [카드 산술] — 원심으로 벽에 붙은 얇은 층이 틈을 거의 안 메운다 [카드 추론]) · 채움 따라 오르다 포화 (*"the rate of increase of the force gradually decreases with particle loading"*) · 높은 rpm 일수록 더 가파름 (p.131) / rpm 기울기는 채움 따라 줄어든다: 800 개 2.44 · 1000 개 2.18 · 1200 개 2.18 · 1500 개 2.08 (Fn · 1000–3000 rpm) [카드 산술] / Fn/Ft 3.8–4.0 (그림 12 · 13a) — 같은 1500 개 값이 그림 11a 와 0–10 % 안에서 같다 (1000 rpm Ft 2.27 ↔ 2.46 × 10⁻⁴ 만 8 % 차) [판독].
- ⚠ 그림 13a 의 y 눈금 글자 = 0.000 · 0.001 · 0.001 · 0.002 · 0.002 · 0.003 (반올림 · 격자 간격은 0.0005 N) — 그림 11a 의 같은 점과 맞춰 0.0005 로 확정 [판독 · §3-9].
- **실험 (Yokoyama 등 [3] · Kona 1987 · 그림 11b · 13b · 허락 받아 재수록)**:
  - 그림 11b — 폴리스티렌 550 g · 힘 (Kg) vs n (r.p.m) 로그–로그: **Fc (열린 원) 0.595 · 1.95 · 3.67 · 5.90 · 8.76 · 9.79 · 11.5 kg** (159 · 321 · 466 · 620 · 778 · 827 · 913 rpm) · **Ft (찬 원) 0.473 · 0.944 · 1.50 · 2.00 · 2.18 · 2.39 kg** (319 · 465 · 628 · 783 · 854 · 940 rpm) [판독 · 51 눈금 아핀 로그 맞춤 · 눈금 잔차 ≤ 0.64 pt (한 눈금만 3.2 pt)] → Fc 기울기 **1.70** (국소 1.66–1.82) · Ft 1.50 (국소 1.82 → 0.97) [카드 산술].
  - 본문: *"The experimental results of Yokoyama indicate that the normal force varies with the rotational speed to approximately the 2.1 power, while the tangential force is not quite a simple power law, but has a slope slightly higher than 2 at low speeds and somewhat less than 2 at higher rotational speeds."* (p.131) → **재수록 그림의 Fc 기울기 1.70 은 '2.1' 과 다르다** · Ft 는 '2 보다 조금 위 → 아래' 꼴이 맞다 (1.82 → 0.97) [판독 · §3-9 · 원 Kona 논문 [미확인]].
  - 그림 13b — **AM-35 · 탈크** 접선 힘 (Kg) vs 채움 무게 (g · 400 g 아래 축 끊김): 300 rpm 은 ≈500 g 에서 0 → ≈1430 g 에서 2.2 kg · 500 rpm ≈730 g → ≈1450 g 에서 5.1 kg · 800 rpm ≈800 g 에서 급상승 (≈940 g 에 7 kg) → ≈1420 g 에서 10.6 kg [판독 · 경로 꼭짓점] — 계산과 **정성 일치** (*"generally consistent with measurements"* p.131) · 크기 대조 없음 (2D 슬랩 N ↔ 실제 장치 kg).
- 원문 해석 (p.131): *"it is expected that this power-law dependence of the forces on the inner-piece varying with the square of the rotation rate is a robust property of the MF system"* · *"no adjustments were made to any of the assumed simulated particle or wall properties"*.

### 3-6. ★ 기능 영역 넷 — 입자 힘 · 충돌 속도 · 회전 (p.132–133 · 그림 14–18 · `txt_p13_…` 셋)
- **영역 (그림 14 · p.132–133)**: 1 = 안쪽 조각 영역 (*"includes the converging-diverging region"*) · 2 = 긁개 영역 · 3 = 입력 영역 (*"where the particles arrive before they enter the inner-piece area"*) · 4 = 자유 확산 영역 (*"where particles get freely dispersed after being removed from the wall by the scraper"*) — 챔버 중심을 지나는 수평선 위 = 4 · 아래는 중심에서 아래로 벌린 두 선으로 2 (왼쪽) · 1 (가운데 · 안쪽 조각) · 3 (오른쪽) [그림 관찰].
- **평균 힘 (그림 15 · 2–4 s · N)** [판독]: 법선 **3.52 · 4.37 · 2.09 · 2.05 × 10⁻³** · 접선 0.75 · 0.84 · 0.43 · 0.43 × 10⁻³ (영역 1 · 2 · 3 · 4) · 법선/접선 4.7–5.2 [카드 산술] (본문 *"about four times larger"*) · 캡션 *"Also shown are the overall average values"* ↔ 평균 막대 **없음** (§3-9).
  - 본문: 영역 1 · 2 가 크다 → *"powder coating is more likely to occur mainly within the inner-piece and scraper areas"* · 긁개 영역이 안쪽 조각 영역보다 조금 큰 것은 *"somewhat counterintuitive"* — 틈 1.6 mm 가 *"somewhat high"* · **1.0 mm 로 줄이면 안쪽 조각 영역 힘이 긁개 영역보다 훨씬 커진다 (보이지 않음)** · 힘 말고 **빈도** 도 본다 (p.133).
  - 평균 법선 힘의 선형 겹침 F/K1 = 0.10–0.22 µm = 지름의 0.026–0.055 % [카드 산술].
- **충돌 속도 (그림 16 · 17)** [판독 · m/s]:
| 영역 | 1 안쪽 조각 | 2 긁개 | 3 입력 | 4 자유 확산 | 계 평균 (막대) |
|---|---|---|---|---|---|
| 법선 · 긁개 있음 | 0.345 | **0.424** | 0.229 | 0.302 | **0.285** |
| 법선 · 긁개 없음 | 0.353 | **0.071** | 0.263 | **0.092** | **0.146** |
| 접선 · 범례 'with' (회색) | 0.677 | 0.301 | 0.633 | 0.400 | 0.479 |
| 접선 · 범례 'without' (검정) | 0.496 | 0.503 | 0.328 | 0.386 | 0.390 |
  - 법선 평균 있음/없음 = **1.96** (본문 *"twice"*) [카드 산술] · 네 영역 단순 평균 (있음 0.325) ≠ '평균' 막대 0.285 → 평균 방식 [미확인].
  - ⚠ 그림 17 범례 그대로 읽으면 '긁개 없음' 의 평균 접선 속도 (0.390) 가 '있음' (0.479) 보다 **낮다** — 본문 *"The system without the scraper has a higher average tangential velocity"* 와 반대 · 그림 16 · 18 의 색 관례 (검정 = 있음) 로 읽으면 본문과 맞는다 (있음 0.390 · 없음 0.479 · 안쪽 조각 영역 없음 0.677) → **범례가 뒤바뀐 것으로 보인다** [카드 추론 · §3-9].
  - 본문 해석: 긁개 없음 = 접선 우세 · *"glancing"* 충돌 (*"with the inner-piece by the particles, which are mostly undergoing rigid body rotation"*) → 표면 개질에 덜 효율적일 것 *"we speculate"* (p.133).
- **회전 속도 (그림 18 · 1/s)** [판독]: 있음 1631 · 1293 · 746 · 685 · 평균 **823** ↔ 없음 1508 · **208** · 769 · 377 · 평균 **492** → 1.67 배 (본문 *"twice"*) [카드 산술] · 안쪽 조각 영역은 *"about the same for both systems"* (1631 ↔ 1508).

### 3-7. ★ 충돌 빈도 — 누적 · 입자당 · 표 2 (p.133–135 · 그림 19 · 20 · 표 2 · 식 12 · `txt_p14_p15_…`)
- 분류: 입자–입자 · 입자–경계 (원통 벽 · 고정 긁개 입자) · 영역별 총 누적 수 → 입자당 (식 12 = 누적 수 ÷ 그 영역의 평균 입자 수) · 같은 운전 조건 (2000 rpm · 1500 개 · 1.6 mm).
- **누적 총 수 (그림 19 · 2 → 10 s)** [판독]: 입자–경계 영역 1 0.70 → 3.65 × 10⁶ · 2 0.22 → 1.13 × 10⁶ · 3 0.93 → **4.94 × 10⁶** · 4 0.83 → 4.45 × 10⁶ / 입자–입자 1 3.1 → 16.8 × 10⁶ · 2 1.4 → 6.8 × 10⁶ · 3 9.8 → **50.9 × 10⁶** · 4 6.2 → 29.7 × 10⁶ — 본문 *"the number of collisions within the input area is largest (almost five times that of the scraper area)"* (입자–경계 4.4 배 · 입자–입자 7.4 배 [카드 산술]) · 경계 충돌 수 ≪ 입자 충돌 수 (*"the projected area in the path of any particle and the other particles is much larger than that of the boundaries"* p.134).
- **입자당 누적 (그림 20 · 10 s)** [판독]: 입자–경계 3.34 × 10⁴ · 8.3 × 10³ · 1.50 × 10⁴ · 4.9 × 10³ / 입자–입자 1.55 × 10⁵ · 4.96 × 10⁴ · 1.53 × 10⁵ · 3.18 × 10⁴ (영역 1–4).
- **표 2 (입자당 1 s · 3–10 s 평균 · [인쇄] p.136)**:
| | 영역 1 안쪽 조각 | 영역 2 긁개 | 영역 3 입력 | 영역 4 자유 확산 |
|---|---|---|---|---|
| 입자–입자 | **1.54e4** | 4.92e3 | **1.52e4** | 3.14e3 |
| 입자–경계 | **3.31e3** | 8.21e2 | 1.48e3 | 4.81e2 |
  - 그림 20 의 3–10 s 기울기 (입자–입자 1.57e4 · 4.98e3 · 1.55e4 · 3.21e3 · 입자–경계 3.37e3 · 840 · 1.51e3 · 504) 가 표 2 와 2–5 % 안 [판독 · 카드 산술].
  - **영역별 평균 입자 수 (역산)** = 그림 19 기울기 ÷ 표 2: 영역 1 ≈ **112** · 2 ≈ 135 · 3 ≈ 338 · 4 ≈ **937** (합 ≈ 1520 ≈ 1500 · 두 충돌 종류에서 같은 값) [카드 산술 · 판독] — 입자의 62 % 가 자유 확산 영역 · 안쪽 조각 영역 7 %.
  - 계 평균 입자당 충돌 (인구 가중) = 입자–입자 6.9 × 10³ /s · 입자–경계 940 /s [카드 산술] → *"a single particle may go through tens of thousands of collisions per second"* 는 영역 1 · 3 의 입자–입자 (1.5 × 10⁴) 에 맞는 말 · 영역 1 에서 충돌 사이 평균 53 µs ↔ 충돌 시간 2.9 µs (접촉 중 ≈5 %) [카드 산술].
- 원문 결론 (p.135): 자유 확산 영역이 가장 적다 (직관과 맞음) · 안쪽 조각 영역이 가장 많다 · 긁개 영역은 힘은 크지만 덜 자주 → *"most of the coating action should take place in the inner-piece area when the results of both the collision dynamics and the collision frequency are taken into consideration"*.

### 3-8. ★ 회전 세기의 무차원화 · 다른 메카노퓨전 · 고속 믹서 카드와 나란히 [카드 산술 · 다른 카드 값 그대로]
| 장치 · 카드 | 크기 | 회전 | 벽 · 날 끝 속도 | ω²R/g (원심 / 중력) | 힘 · 응력 세기 ∝ n^? |
|---|---|---|---|---|---|
| **이 논문 (MF 2D DEM)** | 챔버 25 mm · 틈 0.8–1.6 mm | 1000–4000 rpm (기준 2000) | 1.31–5.24 m/s (2.62) | 14.0–224 (**55.9**) | 안쪽 조각 힘 **1.98** (계산) [판독] |
| Yokoyama [3] 실험 (재수록) | [미확인] | 159–940 rpm | [미확인] | [미확인] | Fc **1.70** [판독] ↔ 본문 '2.1' |
| `kim2023_…` (AMS-Mini · LPSCl 를 NCM811 에) | 헤드–벽 3 mm · 긁개 ≈0.4 mm · 20 g | 2000–5000 rpm × 1–5 h | [미확인] | [미확인] | — (실험) |
| `kissel2026_…` (Picoline + Nobilta · 날개형) | 충전율 10 % · ≈20 g | 1,000–10,000 rpm | 날 끝 40 m/s (10,000) | — | SI_CG ∝ n^**1.76** (그 카드 L183) |
| `frankenberg2024_…` (고강도 믹서 DEM) | — | 5,000–10,000 min⁻¹ | — | — | SI^normal ∝ n^**2.17** · SN ∝ n^0.62 (그 카드 L32–33) |
| `kawaguchi2017_…` (Hybridizer NHS-0) | 챔버 125 mm · 회전자 118 mm | — | 날 끝 50 → ≥ 80 m/s (부분 → 완전 피복) | — | — (실험 · 그 카드 L26 · L29 · L58) |
| `pfeffer2001_…` 총설의 MF | — | 외통 200–1600 rpm | — | — | — (그 카드 L76) |
| 우리 드럼 (B2-U 덱) | R 12.58 mm (지름 25.2) · L 5.03 mm · 39 각형 | **76.7 rpm** | 0.101 m/s | **0.0827** | — |
- ⇒ 이 논문의 25 mm 챔버는 **우리 드럼과 지름이 거의 같다** (25 ↔ 25.2 mm) — 그러나 회전 26 배 · 벽 속도 26 배 · ω²R/g 676 배 (2000 rpm) · 안쪽 조각 · 긁개 유무 · 중력 유무가 다르다 [우리 산술] → Mellmann 지도 (`mellmann2001_…`) 로는 MF = **원심 꼴 (ω²R/g ≫ 1)** — 중력이 꼴을 정하는 우리 드럼 (폭포 꼴) 과 **다른 운동 체제** 이고, MF 는 원심으로 벽에 붙는 층을 안쪽 조각 · 긁개로 기계적으로 깨는 장치다 [카드 추론].
- ⇒ 힘 · 응력 세기의 회전 지수는 장치 · 지표가 달라도 1.7–2.2 사이 (충돌 운동 에너지 ∝ v² ∝ n² 의 꼴) [다른 카드 값 · 카드 해석].

### 3-9. 원문 안 어긋남 (§11 에 다시)
1. **Yokoyama 지수**: 본문 'normal ≈ 2.1 승' ↔ 재수록 그림 11b 의 Fc 기울기 **1.70** [판독 · 51 눈금 맞춤 · 국소 1.66–1.82] — 그림이 다른 자료이거나 본문이 원 논문의 다른 수를 옮겼을 수 있다 (원 Kona 논문 [미확인]).
2. **그림 17 범례**: 검정 = 'without' · 회색 = 'with' (그림 16 · 18 은 반대) — 범례 그대로면 본문과 모순 · 색 관례대로면 본문과 맞음 [카드 추론].
3. **그림 9 단위** 'J/m²' ↔ 같은 평균량의 그림 10b 'N/m²' (고리 평균이 그림 10b 2D 값과 0.1 % 안) — 압력이면 N/m² = J/m³ [카드 추론].
4. **2D/3D 차** *"not more than about 10%"* ↔ 강체 벽 충돌 압력 +16.7 % [카드 산술].
5. **그림 15 캡션** *"Also shown are the overall average values"* ↔ 평균 막대 없음.
6. **비율 말** — 그림 18 평균 1.67 배 ↔ 본문 *"twice"* · 안쪽 조각 법선/접선 4.4–4.6 (그림 11a) · 3.8–4.0 (그림 12 · 13a) ↔ *"around 5"* · 입자 법선/접선 4.7–5.2 (그림 15) ↔ *"about four times"* [판독].
7. **그림 13a y 눈금** 반올림 (0.001 · 0.002 가 두 번씩) · 그림 13a 표지 범례 (■ 1000 · ◆ 2000 rpm) 가 그림 12 (◆ 1000 · ■ 2000) 와 반대.
8. **영역 부피에 안쪽 조각이 들어 있다** (고리 1–5 의 2–29 % [카드 산술]) — 밀도꼴 진단량 (J/m³ · N/m²) 이 그만큼 작게 나온다 · 원문 말 없음.
9. 그림 19a 축 제목 *"numbar"* (오기) · 참고 [2] 저자 *"R.N.D. Wei"* (`pfeffer2001` 원문 저자 = D. Wei) · 본문 *"an import role"* (important).
10. 강성 서술: p.124 *"the selection of the stiffness is not expected to have a significant impact on the results of interest"* (운동학 기준 [10]) ↔ p.133 *"the actual values of the instantaneous computed forces are lower, and the contact durations are higher"* — 같은 논문 안에서 '관심 결과' 의 범위가 운동학 · 시간 평균 힘으로 한정된다 [카드 해석].

---

## 4. ★ 방법 — 모델 사슬 · 입자 처리 · 이 묶음의 네 질문 · 용어집

### 4-1. 모델 사슬
1. 장치 → 2D 단면 (챔버 원 · 편심 안쪽 원 · 긁개 = 고정 입자 몇 개 · 긁개–벽 틈 0) · 장치를 줄이고 채움을 맞춤 (p.123–124).
2. host = 단분산 구 (평면에 묶임 · 구의 관성) · 임의 처음 상태 · 중력 없음 (p.125).
3. 접촉 = Walton–Braun 법선 (K1 · K2 = K1/e²) + 증분 미끄럼 접선 (s · γ = 1) · 점착 없음 (p.123).
4. leap-frog · Δt = πe√(m/2K1)/40 · 10 s (p.123–125).
5. 진단: 등부피 고리 7 (회전 KE · 운동 세기 · 충돌 압력) · 기능 영역 4 (힘 · 충돌 속도 · 회전 · 충돌 빈도) · 안쪽 조각 힘 (장시간 평균) · 3D 점검 둘.
6. 검증: 안쪽 조각 힘의 rpm · 채움 경향 ↔ Yokoyama 실험 (꼴 · 지수만).

### 4-2. ★ 입자 처리 (particle treatment)
- **구 · 단분산 · 한 종** (host 만 · 게스트 0) · 2D (평면에 묶인 구 — 원판이 아님 · I = md²/10).
- **강체 구 + 이력 접촉 (CONTACT 의 탄소성)** — Walton–Braun 의 '소성' 은 되돌림 강성 K2 > K1 과 잔류 겹침 α0 로 **에너지를 잃는 접촉 법칙** 일 뿐 · **입자 모양 (SHAPE) 은 바뀌지 않는다** (겹침 = 기하 대리 · 막 · 변형 · 파쇄 0).
- 강성 = 실제 재료보다 훨씬 무르다 (p.133) · 최대 변형 < 1 % 로 K1 을 고름 (p.124) · e 는 속도 무관 (p.123).
- 경계 = 입자 (챔버 · 안쪽 조각 = '경계 입자' · 긁개 = 고정 입자) — 우리 LIGGGHTS 의 메시 벽과 다르다.

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
- **DEM 의 한계 (말한 것)**: *"It is noted that using small value of stiffness will provide inaccurate results for the contact forces. The significance and magnitude of the error in the force calculations will be explored in a subsequent paper."* (p.124) · *"the spring-stiffness in the force model is chosen to be much smaller than that of a real particle material. While this choice provides reasonable results for the kinematics of the system, the actual values of the instantaneous computed forces are lower, and the contact durations are higher, than would be expected for real particle–particle collisions (with higher effective stiffnesses). The results shown in this section should therefore be considered primarily as qualitative indications of what is happening within the system."* (p.133) · *"The duration of individual collisions and the peak force during a collision is known to be a strong function of the interparticle stiffness (and/or the specific form assumed for the interaction force–displacement relation)."* (p.131) · *"However, unduly small stiffness causes a time step with unstable simulation results."* (p.123) · *"Due to the computational limitations, it is impractical to include the fine particles in this modeling effort."* (p.122) · 반대 쪽 (운동학): *"the value of stiffness does not significantly change the kinematics of the results, as long as significant overlap does not occur during collisions"* [10, 11] (p.123–124) · *"That time-integral of the force, which controls the kinematics of the flow, is relatively insensitive to the stiffness"* (p.131).
- **소성변형**: 왜 어려운지는 논의 없음 · 우회 = Walton–Braun 이력 접촉 (맞춘 값 0 · e 0.85 · K1 20,000 N/m · s · γ 1 = 고른 값) · 입자 모양 변화 0.
- **2D ↔ 3D**: §3-3 — 운동 세기 −4 – +2 % · 충돌 압력 +11 – +17 % [카드 산술] · 본문 '약 10 % 이내'.
- **탈압**: 해당 없음 (압밀 없음) · 접촉 하나의 되돌림 가지 (K2 · α0) 만.

### 4-4. 기법 미니 용어집
- **메카노퓨전 (Mechanofusion · MF)**: Hosokawa 의 건식 코팅 장치 · 회전 챔버의 원심으로 가루를 벽에 밀고, 고정 안쪽 조각 (press head) 과 벽 사이 좁은 틈에서 압축 · 전단 · 마찰 열로 게스트를 host 표면에 '녹여 붙인다' · 고정 긁개가 벽 층을 긁어 다시 흩뜨린다.
- **부분 걸쇠 스프링 (partially latching spring · Walton–Braun)**: 누를 때 K1 · 되돌릴 때 더 단단한 K2 = K1/e² 로 잔류 겹침 α0 를 남기는 선형 이력 법선 힘 — LIGGGHTS `hooke/hysteresis` (Luding 2008) 의 계보 [다른 카드 · `walton1993` · `luding2008`].
- **증분 미끄럼 마찰 (incrementally slipping friction)**: 접선 강성이 μN 에 가까워질수록 줄고 (지수 γ) 미끄럼 방향이 바뀔 때의 접선 힘 T* 를 기억하는 Mindlin–Deresiewicz 꼴 근사.
- **운동 세기 지표 (kinetic intensity indicator)**: 영역 평균 속도에서 뺀 속도 성분의 운동 에너지 밀도 — 영역이 거칠어 '참 편차 에너지' · 입자 온도가 아니다 (식 10).
- **충돌 (입자) 압력 (collisional granular pressure)**: 비리얼 Σ F_ij R_ij / 3V (식 11 의 둘째 항).
- **기능 영역 (area 1–4)**: 안쪽 조각 · 긁개 · 입력 · 자유 확산 — 원통을 각도로 나눈 넷 (그림 14).
- **입자당 충돌 수 (averaged collisions · 식 12)**: 영역 누적 수 ÷ 영역 평균 입자 수 — 총 수 순위를 뒤집는다 (입력 영역 총 수 최대 ↔ 입자당은 안쪽 조각 ≈ 입력).

---

## 5. Figure set ★ (크롭 55 장 = `litdb/figures/chen2004_mechanofusion_dry_coating_dem_2d_host_scraper_inner_piece_collision_frequency/`)
| 그림 (크롭 파일) | 내용 | 우리 활용 |
|---|---|---|
| Fig. 1 (`fig_1.png` · 다시 자름) | MF 장치 그림 (챔버 벽 · 축 · 날 · 둥근 조각 · 회전 화살표) | 코팅 장치 기하 용어 |
| Fig. 2 (`fig_2.png`) | 계산 모형 — 원 챔버 · 편심 안쪽 원 · 긁개 = 고정 입자 셋 (확대) | 우리 드럼에 '안쪽 조각 · 긁개' 를 넣을 때의 최소 기하 |
| Fig. 3 (`fig_3.png` · 다시 자름) | DEM 알고리즘 흐름도 | — |
| Fig. 4 (`fig_4.png`) | 등부피 고리 7 (축척 아님) | 칸 너비 ≥ 최대 입경 규칙 |
| Fig. 5 (`fig_5.png` · 300 dpi) | ★ 긁개 있음 — 0–10 s 입자 그림 · 2 s 속도 벡터 (소용돌이) | 분산 꼴 · 처음 상태 |
| Fig. 6 (`fig_6.png` · 300 dpi) | ★ 긁개 없음 — 벽 층 (2–3 입자) + 가운데 무리 · 벽 따라 접선 흐름 | 벽 부착 = 충돌 세기 손실의 그림 |
| Fig. 7 (`fig_7.png`) | 회전 KE 고리 분포 (있음 · 없음) | 챔버 ω 를 뺀 회전 에너지 (식 8) |
| Fig. 8 (`fig_8.png` · 다시 자름) | ★ 운동 세기 지표 고리 분포 | 평균 32.6 ↔ 13.7 J/m³ |
| Fig. 9 (`fig_9.png`) | ★ 충돌 압력 고리 분포 (로그) | 평균 435 ↔ 914 · 단위 표기 문제 |
| Fig. 10 (`fig_10.png`) | 2D ↔ 3D (주기 · 강체 벽) 0–1 s | 2D 근거 · 차 +17 % 까지 |
| Fig. 11 (`fig_11.png`) | ★ 안쪽 조각 힘 vs rpm (a 계산 · b Yokoyama 폴리스티렌) | 지수 1.98 ↔ 1.70 [판독] |
| Fig. 12 (`fig_12.png`) | 법선 힘 vs 채움 × rpm | 포화 · rpm 지수가 채움 따라 줄어듦 |
| Fig. 13 (`fig_13.png`) | 접선 힘 vs 채움 (a 계산 · b Yokoyama 탈크) | 정성 일치 · y 눈금 반올림 |
| Fig. 14 (`fig_14.png`) | ★ 기능 영역 넷 정의 | 우리 코팅 DEM 판독의 영역 틀 |
| Fig. 15 (`fig_15.png`) | 영역별 평균 법선 · 접선 힘 | 힘 지도 (정성) |
| Fig. 16 (`fig_16.png`) | ★ 영역별 법선 충돌 속도 (있음 · 없음) | MPM 단일 충돌 경계 조건의 크기 감각 |
| Fig. 17 (`fig_17.png`) | 영역별 접선 충돌 속도 (범례 뒤바뀜 의심) | '스치는' 충돌 |
| Fig. 18 (`fig_18.png`) | 영역별 회전 속도 | — |
| Fig. 19 (`fig_19.png`) | 누적 총 충돌 수 (경계 · 입자) | 총 수 ↔ 입자당의 함정 |
| Fig. 20 (`fig_20.png`) | ★ 입자당 누적 충돌 수 | 표 2 의 근거 |
| 표 1 (`tab_1.png` · 다시 자름) | ★ 계산 변수 전부 | §3-2 |
| 표 2 (`tab_2.png` · 다시 자름) | ★ 영역별 입자당 충돌 빈도 (1 s 당) | §3-7 |
| 식 크롭 13 장 (`eq_01_…` – `eq_12_…` · `eq_dt_…`) | 번호 식 전부 + 번호 없는 Δt 식 (인라인 · 앞 줄을 지운 사본에서 자름) | 접촉 법칙 · 진단량 정의 |
| 근거 문단 20 장 (`txt_p1_…` – `txt_p16_…`) | 초록 · 장치 · 작동 · 다중 규모 · 긁개 모형 · Δt · 2D 근거 · 처음 상태 · 고리 · 비교 결과 · 압력 · 2D/3D · 안쪽 조각 힘 · 채움 · 강성 · 영역 힘 · 강성 고백 · 충돌 속도 · 충돌 빈도 · 결론 | 원문 인용용 (파일 이름의 pN = PDF 쪽) |

## 6. Post-processing ★
- **원문이 한 것**: 고리 · 영역 부피 평균 (정상 뒤 2 s · 충돌 빈도는 3–10 s) · 장시간 평균 안쪽 조각 힘 · 로그–로그 멱 맞춤 (기울기 1.97) · 누적 충돌 수 · 입자당 정규화 (식 12) · 남의 실험 그림 재수록 대조.  반복 · 시드 · 오차 · 분포 (평균만) 없음 · 계산 시간 없음.
- **이 카드의 후처리**: 그림 7–20 전부가 벡터라 PyMuPDF `get_drawings` 로 막대 꼭대기 · 표지 중심 · 경로 꼭짓점 · 눈금 · 격자선의 좌표를 읽어 환산 (337 행 · 로그 축은 격자 직선 맞춤 · 그림 11b 는 기울어진 스캔이라 51 눈금 아핀 로그 맞춤) → 교차 검산: 고리 평균 ↔ 그림 10 2D 값 (0.1–0.5 %) · 그림 11a ↔ 그림 12 · 13a 같은 점 (0–10 %) · 그림 20 기울기 ↔ 표 2 (2–5 %) · 영역 인구 합 1520 ↔ 1500 · 카드 산술 (K2 · m · I · Δt · step 수 · 충돌 시간 · 1 % 겹침 속도 · 벽 속도 · ω²R/g · 면적 분율 · 요동 속도 · 고리의 안쪽 조각 몫) · 우리 덱 값 (B2-U deck_meta · `make_mixer_deck.plan()` 읽기만) 과의 대입 (§7).  스크립트 = 이 묶음 scratchpad (`digitize_all.py` 등 · 끝난 뒤 지움) — 값 · 방법은 `digitized.csv` 의 method · note 칸에 남겼다.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 리포 문서 출처를 병기)

### 7-1. 비교표 (믹서 드럼 DEM ↔ 이 논문)
| 항목 | 이 논문 (MF 2D DEM) | 우리 (믹서 B2-U 덱 · 리포 `docs/reviews/mixer_first8_launch_preparation_20261106/planned_assets/PRECAL_R1_B2_U/` 의 `in.mixer` · `deck_meta.json` · 목적 `docs/reviews/mixer_b2_u_development_20261122/README.md` · 읽기만) | 같음 / 다름 · 왜 |
|---|---|---|---|
| 코드 · 차원 | 자체 코드 (이름 [미확인]) · 2D (+ 3D 점검) | LIGGGHTS · 3D | — |
| 장치 | 회전 챔버 25 mm + 고정 안쪽 조각 (10 mm · 틈 1.6 mm) + 고정 긁개 · 중력 없음 | 39 각형 드럼 R 12.58 mm · L 5.03 mm · 중력 · 안쪽 조각 · 긁개 없음 | **지름은 거의 같다** · 운동 체제가 다르다 (원심 ↔ 폭포) |
| 회전 | 1000–4000 rpm (2000) · 벽 2.62 m/s · ω²R/g 55.9 | 76.7 rpm · 0.101 m/s · Fr 0.0827 · 2 바퀴 (1.565 s) | 26 배 · 676 배 [우리 산술] |
| 입자 | host 한 종 · r 0.2 mm · 1.20 g/cm³ · 1500 개 | 3 상 parcel (CGF 151.4): AM_P r 0.681 · AM_S 0.303 · SE 0.0757 mm · 4.85 / 1.64 g/cm³ · 100,000 개 계획 (plan() 재계산: AM_P 143 · AM_S 699 · SE 99,158) | 다분산 · 다상 · 점착 = 우리만 |
| 접촉 법칙 | Walton–Braun 선형 이력 + 증분 미끄럼 · K1 20,000 N/m · e 0.85 · μ 0.4 / 0.5 | `gran model hertz tangential history cohesion sjkr rolling_friction cdt` (Hertz + 접선 이력 + SJKR 점착 · 기하평균 W_ij = 2√(γ_iγ_j) + 구름 마찰) · E AM 1.037 GPa · SE 1.0 × 10⁷ Pa × 20 = 2.0 × 10⁸ · 벽 1.48 GPa · COR 0.3 · μ_s 0.9 · μ_r 0.075 | 우리 압밀 DEM (hooke/hysteresis) 은 이 논문 법선과 **같은 계보** |
| 점착 | 없음 | γ_AM/γ_SE 0.1 (비코팅 U) · 1 (코팅 C) · γ_W/γ_SE 0.00256 · Bo_SE 0.21244 (B1) · 21.244 (B2) | 우리 질문의 축 = 이 논문에 없음 |
| 시간 간격 | 6.7 × 10⁻⁸ s (n = 40 · 충돌 시간 기준) | 2.373 × 10⁻⁷ s (덱 dt 규칙 · SE (×20) 가 정함 · deck_meta `dt.rule_set_by`) | — |
| 길이 · 비용 | 10 s · 1.5 × 10⁸ step · 1500 개 (계산 시간 [미확인]) | 2 바퀴 7.72 M step (채움 포함) · B1-U 한 팔 **25 h 7 m 43 s** (ibb · 리포 `docs/reviews/mixer_b1_pair_return_20261122/README.md` W3 · B2-U 계획 = 1 노드 MPI 20) | — |
| 판독 | 고리 7 (반지름 · 등부피) · 기능 영역 4 · 입자당 충돌 · 안쪽 조각 힘 | Lacey M (칸 16×16×4 · 12×12×3 · 8×8×2) · SE 군집 몫 · AM 접촉 SE | 이 논문 = 충돌 통계 · 우리 = 조성 분산 — **서로의 빈칸** |
| 칸 규칙 | 칸 너비 ≥ 최대 입경 (p.125) | 16×16×4 칸 1.57 × 1.57 × **1.26 mm** ↔ AM_P parcel 지름 1.363 mm [우리 산술 · 칸 = 외접 상자 등분 가정] | 축 방향 칸이 AM_P 보다 작다 → 부피 배분 판독이면 이 규칙 밖 · 중심 배분이면 무관 (우리 판독기 배분 방식 [미확인]) |
| 겹침 기준 | K1 을 '최대 변형 < 1 %' 로 고름 (실측 분포 없음) | 저장 프레임 최대 겹침 1 % 계약 (D-1 · 믹서 등록) | **같은 1 % 문턱** · 그들은 강성 고르는 근거로만 |

### 7-2. ★ 코팅 과정 DEM 구현 (1저자 11-23 Q3) — 이 논문에서 옮길 점 · 빠진 점 · 우리 대입
| 항목 | 이 논문 | 우리가 옮길 점 · 바꿀 점 | 표지 |
|---|---|---|---|
| ① 모사 꼴 | 장치 단면 2D · host 만 · 점착 없음 · 긁개 = 고정 입자 · 안쪽 조각 = 큰 고정 입자 · 10 s (333 바퀴) | 우리 드럼 덱 (같은 지름) 에 **고정 안쪽 원통 (10 mm · 틈) + 고정 긁개 입자** 를 넣고 축을 수직 (중력 = z) 으로 돌리면 MF 꼴의 최소판 · 점착 (SJKR · 기하평균) · 3 상은 우리 덱 그대로 | [카드 추론] |
| ② 잴 양 | 고리별 회전 KE (챔버 ω 뺌) · 운동 세기 · 충돌 압력 · 안쪽 조각 힘 (장시간 평균) · 영역별 입자당 충돌 빈도 · 평균 법선 / 접선 힘 · 충돌 속도 · 회전 | + **상 쌍별** (SE–AM · SE–SE · AM–AM · 입자–벽) 충돌 빈도 · 충돌 에너지 **분포** (평균만이 아니라) · 벽에 붙은 몫 (챔버와 같이 도는 입자 비) · SE 가 AM 에 붙어 있는 몫 (게스트 피복의 DEM 판) · 덩어리 크기 | [카드 추론] |
| ③ 실험과 잇기 | 안쪽 조각 힘의 rpm 지수 (∝ ω^≈2) 를 Yokoyama 측정 꼴과 대조 (크기 대조 없음) | 실제 장치에서 잴 수 있는 양 = 축 동력 · 토크 · 온도 · 비에너지 E_m (`kissel2026` 의 E_m,exp) → DEM 의 안쪽 조각 힘 × 벽 속도 · 소산 일과 대조 · 피복은 XPS · SEM 피복률 (`kissel2026` · `kim2023`) 과 | [카드 추론] |
| ④ 우리 대입 — 규모 · 시간 간격 · 비용 | 1500 개 · Δt 6.7 × 10⁻⁸ s · 1.5 × 10⁸ step | (가) 우리 B2-U 덱 그대로 (CGF 151.4 · 100,000 개 · Δt 2.373 × 10⁻⁷ s) 를 25 mm 챔버에 → 2000 rpm 1 s = 4.2 × 10⁶ step ≈ **14 h** · 0.1 s ≈ 1.4 h (B1-U 25.13 h 를 입자 수 × step 수에 비례로 옮김) — 단 **틈 1.6 mm = AM_P parcel 1.2 개** (이 논문 4 host 지름) · (나) 틈/AM_P 를 4 로 맞추려면 CGF 44.4 → 입자 ≈ 4.0 × 10⁶ · Δt 7.0 × 10⁻⁸ s → 0.1 s ≈ **186 h** (1 s ≈ 1,860 h) | [카드 산술 · 가정: 비용 ∝ N × step · 같은 접촉 밀도 · 같은 기계] |
| ④-2 겹침 계약 | K1 을 '최대 변형 < 1 %' 로 · 2000 rpm 평균 법선 충돌 0.29 m/s 의 겹침 0.07 % | 우리 B2-U 물성 (Hertz) 의 최대 겹침 1 % 가 되는 상대 법선 속도: SE–SE **1.17 m/s** · SE–벽 1.30 · AM_P–벽 1.40 · AM_P–AM_P 1.52 → 2000 rpm 벽 속도 (2.62 m/s) 충돌이면 1.5–1.9 % (계약 밖) · 평균 (0.3–0.4 m/s) 은 0.3–0.4 % | [카드 산술 · Hertz 최대 겹침 식 · 우리 덱 물성] |
| ④-3 구 DEM 이 못 보이는 것 | 막 · 게스트 · 녹아 붙음 · 열 · 실제 힘 | **막 (SE 가 AM 위로 펴짐) 은 DEM 에 안 나온다** → DEM 은 충돌 에너지 · 속도 **분포** 와 SE 의 AM 부착 (피복) 까지 · 막 형성은 그 분포에서 뽑은 대표 충돌을 **DEM → MPM 단일 충돌** (SE 소성 · σ_y · 접착) 로 넘긴다 · 이 논문의 법선 충돌 속도 0.07–0.42 m/s 는 `lee2026_mechanical_…` 의 FEM 충돌 속도 15 m/s (그 카드 L310 — 'RAM 60 G 에서 유도 없음') 보다 35–210 배 낮다 (장치 · 규모 · 2D · 연화 강성이 달라 크기 비교는 아님) | [카드 추론 · 다른 카드 값] |

### 7-3. 랩 기준과 나란히
- 이 논문에 압밀 · 기공 · 진밀도가 없다 → 랩 표준 (순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³) 과 **나란히 놓을 숫자가 없다**.  host 밀도 1.20 g/cm³ = 랩 표준 SE 1.64 · NCM 4.85 와 **다른 문헌 값** (재료 이름 없음).
- 충돌 압력 (고리 평균 435 N/m² · 벽 고리 2.4 × 10³) 은 압밀 300 MPa 의 6.9 × 10⁵ 분의 1 [카드 산술] — 다른 양 (부피 평균 비리얼 · 빈 공간 포함) 이라 압밀 압력과 견주지 않는다.

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 코팅 장치의 **기계 환경 (충돌 빈도 · 세기 · 장소)** — DEM 쪽 (입자 · 접촉 · 영역 통계).
- **없는 것**: 게스트 · 점착 · 막 · 모양 변화 · 압밀 · 수송 · MPM ⇒ 우리 Ⓒ 코팅 활물질 믹싱에서 **'장치가 입자에 무엇을 하는가' 의 판독 틀** 만 준다 · 막 형성 (MPM 몫) 과 점착 대비 (우리 논지) 는 비어 있다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문은 압밀 계획 바깥 (흐름 밖: Ⓒ 코팅 믹싱) 이다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (판정 기준 결과 전 등록) | ★ 흐름 밖 (Ⓒ 코팅 DEM): 판독을 **결과 전에** 고정할 틀 — 기능 영역 (안쪽 조각 · 긁개 · 입력 · 자유 확산 또는 우리 드럼의 꼴별 영역) · **입자당** 정규화 (식 12 — 총 수 순위가 뒤집힌다) · 챔버 회전을 뺀 회전 에너지 (식 8) · 칸 너비 ≥ 최대 입경 · 장시간 평균 힘 | 기공 연산자 · 압밀 판정 기준 없음 |
| **단계 1–6** (3D 메모리 · 2D MPM · 접촉 표현 · 순수 SE · 복합 압밀 · 탈압) | 없음 | — |
| **단계 7** (형상 · 피복 · 수송) | 없음 ('피복' 은 충돌 통계에서 추론한 장소뿐) | 게스트 · 피복 정량 0 |
| **후보 D0** (지금 DEM) | 법선 = **Walton–Braun 부분 걸쇠 스프링 = 우리 압밀 DEM 의 hooke/hysteresis 와 같은 계보** · 연화 강성의 근거를 '운동학 · 시간 평균 운동량 전달은 강성에 둔함' 으로 댄다 (p.123–124 · p.131) — ⚠ **이 근거는 우리 압밀에는 안 옮겨진다**: 300 MPa 압밀의 기공은 힘으로 정해지는 준정적 양이라 겹침 ∝ 힘/강성 이고, 그래서 우리는 E_eff (1.35 GPa · 18 배 연화) 를 실험 기공에 맞춘다 (frame [2]) [카드 추론] · 1 % 변형 문턱 = 우리 믹서 겹침 계약과 같은 수 | 강성 · 겹침 실측 분포 없음 · 접촉 법칙 시험 없음 |
| **후보 C′** (항복 캡 탄소성 접촉) | Walton–Braun = 가장 단순한 선형 이력 (항복 캡 없음) — C′ (Thornton–Ning) 은 `kissel2026` DEM 이 썼다 | 항복 · 캡 · 다접촉 0 |
| **후보 A′-0 · A · A′ · B · C · M0** | 없음 | — |
| **U0–U6** | U5 (비슷한 강성 입자끼리 충돌) 의 최소판 = 두 구 정면 충돌로 e = √(K1/K2) · 잔류 겹침 α0 · 충돌 시간 (π/2)(1 + e)√(m_eff/K1) 를 확인하는 회귀 (흐름 밖) · U3 (단단한 구를 소성 블록에 눌렀다 떼기) 의 '잔류 압흔' 은 접촉 법칙의 α0 로만 닮음 | 다물체 · 해상도 시험 없음 |
| **R1–R7** | R2 (미끄럼 · 분리) — 증분 미끄럼 마찰 (T* 기억) · R4 (탈압 · 되돌아옴) — 접촉 하나의 되돌림 가지 K2 · α0 뿐 | R1 · R3 · R5–R7 없음 |
| **결과 전 대조 항목** (흐름 밖: Ⓒ 코팅 DEM) | ① 안쪽 조각 (프레스 헤드) 힘 ∝ ω^≈2 (계산 1.98 · 실험 그림 1.70 [판독] · 본문 2.1) — 우리 MF 꼴 계산을 하면 같은 지수 범위 (1.7–2.2) 를 결과 전에 적는다 ② 긁개를 빼면 법선 충돌 속도 · 운동 세기가 절반 · 벽 층이 챔버와 같이 돎 ③ 입자당 충돌은 안쪽 조각 · 입력 영역이 최대 · 자유 확산 최소 (영역 순위만 · 크기 전이 금지) | 크기 · 문턱 전이 금지 (2D · 무점착 · 단분산 · 축소 장치 · 연화 강성) |

- **우리 DEM 과 견줄 자리**: 우리 18 배 연화 (24 → 1.35 GPa) 는 압밀 기공에 맞춘 **유효 탄성률** (재배열 · 입계 미끄럼을 뭉친 대리) · 이 논문의 연화는 **계산 시간용 강성 낮춤** (운동학만 지킴) — 같은 '무르게' 라도 정당화가 다르다 [카드 해석].
- **우리 MPM 과 견줄 자리**: 없음 · 다만 막 형성 (SE 가 AM 위에서 소성으로 펴짐) 을 MPM 단일 충돌 (E 1.53 · σ_y 0.30 · ν 0.49 = 압밀 보정값 · 충돌 속도 영역에서는 미검증) 로 볼 때 경계 조건 (충돌 속도 · 각도) 의 크기 감각을 준다 — 법선 0.07–0.42 · 접선 0.30–0.68 m/s (2D · host–host · 2000 rpm · 평균) [판독].
- **재료 · 차원 · 조건 차이**: 이름 없는 1.2 g/cm³ 단분산 구 (0.4 mm) ↔ 우리 NCM · LPSCl parcel (실입경 1–9 µm · 점착 · 3 상) · 2D ↔ 3D · 원심 (ω²R/g 14–224) ↔ 중력 드럼 (0.0827) · 공기 · 열 없음 ↔ 진공 DEM.

## 9. 적용 인사이트 (행동)
1. **코팅 꼴 계산을 하게 되면 판독을 '영역 × 입자당' 으로 먼저 등록한다 (흐름 밖: Ⓒ · 단계 0)** — 영역 (MF 면 안쪽 조각 · 긁개 · 입력 · 자유 확산 · 드럼이면 꼴별 흐름층 · 바닥 · 벽) 마다 입자당 충돌 빈도 · 법선 / 접선 충돌 속도 **분포** · 상 쌍별 (SE–AM · SE–SE) 로.  총 수는 인구에 끌려 순위가 뒤집힌다 (입력 영역 총 수 4.4 · 7.4 배 ↔ 입자당은 안쪽 조각과 같음).
2. **벽 부착 몫 = 관측량으로** — 긁개가 없으면 벽 층이 챔버와 같이 돌아 법선 충돌 세기가 절반이 된다 (원심 · 무점착).  우리 드럼의 벽 점착 (γ_W/γ_SE 0.00256 = 낮게 둔 설계) 의 효과를 보려면 '드럼과 같이 도는 입자 몫' (챔버 ω 를 뺀 상대 각속도 ≈ 0) 을 덤프에서 센다 (식 8 의 생각).
3. **순간 힘 · 최대 힘을 보고하지 않는다 — 시간 적분량 (운동량 전달 · 소산 일 · SI) 으로** — 연화 강성에서는 순간 힘 · 접촉 시간이 틀리고 시간 적분은 덜 틀린다 (p.131 · p.133) · `kissel2026` · `frankenberg2024` 의 응력 세기 SI (소산 일 / 질량) 가 같은 쪽의 지표.
4. **장치에서 잴 수 있는 양으로 DEM 을 점검** — 이 논문은 안쪽 조각 힘의 rpm 지수로 했다 → 우리 믹서 · 코팅 계산은 실제 장치의 축 동력 · 토크 (또는 E_m) 의 rpm 지수를 결과 전 대조 항목으로.
5. **칸 너비 ≥ 최대 입경** (p.125) — 우리 Lacey 16×16×4 의 축 방향 칸 (1.26 mm) 이 AM_P parcel (1.363 mm) 보다 작다 [우리 산술] → 판독기가 중심 배분인지 부피 배분인지 적어 둔다 (부피 배분이면 이 규칙 위반).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "A 2-D soft-sphere DEM of a Mechanofusion chamber (Walton–Braun partially latching spring, cohesionless, 1500 host particles of 0.2 mm radius, 25 mm chamber, 1.6 mm gap, 2000 rpm) showed that the scraper roughly doubles the normal impact velocity and the kinetic intensity by breaking up the wall layer that otherwise co-rotates with the chamber (Chen, Dave, Pfeffer, Walton, Powder Technol. 146 (2004) 121–136; ratios digitized from Figs. 8 and 16)."
- "The time-averaged normal force on the inner-piece scaled with the square of the rotational speed (best-fit exponent 1.97, 1000–4000 rpm), consistent in form with Yokoyama's measurements (Chen et al. 2004)."
- "Per-particle collision frequencies reached ~1.5 × 10⁴ s⁻¹ in the inner-piece and input areas versus ~3 × 10³ s⁻¹ in the free-diffusion area (Chen et al. 2004, Table 2)."
- "Because the spring stiffness was much smaller than that of real particles, instantaneous contact forces were underestimated and contact durations overestimated; force results were explicitly presented as qualitative (Chen et al. 2004, p.133)."
- 국문: *"메카노퓨전 장치의 2D DEM (Chen 2004) 은 host 만 · 점착 없이 장치 속 충돌의 장소 · 빈도 · 세기를 냈다 — 게스트 · 점착 · 막 형성은 앞으로의 과제로 남겼다."*
- 국문: *"긁개가 없으면 원심으로 벽에 붙은 층이 챔버와 같이 돌아 법선 충돌 속도가 절반이 된다 (Chen 2004 그림 16 판독 0.285 ↔ 0.146 m/s)."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
**원문이 스스로 적은 한계**
1. 게스트 제외 (*"impractical"* p.122) · 2D (p.124) · 장치 축소 (p.124).
2. 강성이 실제보다 훨씬 작다 → 순간 힘 ↓ · 접촉 시간 ↑ · 결과는 정성 (p.133) · 힘 오차 크기는 '다음 논문' (p.124).
3. 입력 변수 대부분이 '예상 경험값' · 마찰 등은 정량에 영향 · 체계적 변수 연구는 다음 논문 (p.124).
4. 운동 세기 지표는 참 편차 에너지 · 입자 온도가 아니다 (p.127) · 입자 압력의 운동 항은 평균 속도장이 거칠어 뺐다 (p.130).
5. 감도 연구 없음 (*"Although a systematic sensitivity study has not yet been performed to completely verify the robustness of the simulation results"* p.131).

**카드가 본 한계 · 원문 안 어긋남**
6. **점착 · 게스트 · 다분산 · 다상 · 막 · 열 = 범위 밖** — 우리 논지 (점착 대비) 와 코팅 결과는 직접 없다.
7. Yokoyama 지수 2.1 ↔ 재수록 그림 1.70 [판독] · 그림 17 범례 뒤바뀜 의심 · 그림 9 단위 · 2D/3D '10 %' ↔ +16.7 % · 그림 15 평균 막대 없음 · 비율 말 (1.67 ↔ 'twice' 등) · 그림 13a 눈금 반올림 · 범례 기호 그림 12 와 반대 (§3-9).
8. 고리 부피에 안쪽 조각 몫이 들어 있다 (고리 1–5 의 2–29 %) — 밀도꼴 진단량이 그만큼 작게 나온다 [카드 산술].
9. 실험 대조 = 지수 꼴 하나 (재료 · 장치 · 채움이 다름 · 크기 대조 없음) · 0.8 mm 틈 결과 · s 값 · 코드 · 계산 시간 · 시드 [미확인].
10. 평균만 (분포 0) — 코팅에 중요한 것은 충돌 에너지 분포의 꼬리일 수 있다 [카드 추론].
11. **절대값 전이 금지** — 장치 · 크기 · 재료 · 차원 · 강성 · 중력 모두 다르다; 옮길 것 = 판독 틀 · 영역 순위 · 지수 꼴.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| [3] | Toh. Yokoyama, K. Urayama, Toy. Yokoyama, Kona 5 (1987) 59. | ★ 이 논문의 대조 실험 (안쪽 조각 힘 vs rpm · 채움 · 폴리스티렌 · 탈크) — 'Fn ∝ n^2.1' 의 원 수치 확인 (재수록 그림 1.70 과의 차) · 100 넘는 host/게스트 조합 | 없음 |
| [7] | J. Chen, C.C. Huang, Kona 15 (1997) 113. | MF 의 '작용 구역' 해석 모형 (입자끼리 · 긁개 무시) — 이 논문이 고치려 한 앞선 모형 | 없음 |
| [1] | Toh. Yokoyama, K. Urayama, Toy. Yokoyama, KONA 1 (1983) 53. | MF 의 기원 (1980 년대 중반 일본) | 없음 |
| [4] | K. Tanno, Kona 8 (1990) 74. | MF 총설 (복합 입자 제조) | 없음 |
| [12] | A.J. Matchett, T. Yanagida, S. Kobayashi, Powder Technol. 107 (n1/2) (2000) 13. | 2D 근사의 근거 (셋째 방향 무한 → 흐름이 셋째 방향과 무관) | 없음 |
| [15] | O.R. Walton, in: M.C. Roco (Ed.), Numerical Simulation of Inelastic, Frictional Particle–Particle Interactions, Particulate Two-Phase Flow, Butterworth-Heinemann, 1993, p. 885. | 입자 압력 (비리얼) 식 · Walton–Braun 법칙 해설 | 없음 |
| [9] | O.R. Walton, R. Braun, J. Rheol. 30 (5) (1986) 949. | 접촉 법칙 원전 | **제외** (내려받기 불가 · `status.tsv` N-72 첫째) |
| [10] | O.R. Walton, Mech. Mater. 16 (1993) 239–247. | 강성 둔감 (운동학) 의 근거 | `walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem` |
| [2] | R. Pfeffer, R. Dave, R.N.D. Wei, M. Ramlakhan, … Powder Technol. 117 (2001) 40. | 같은 그룹 총설 (저자 표기 'R.N.D. Wei' = 원문 오기) | `pfeffer2001_dry_particle_coating_engineered_particulates` |
| [8] | P.A. Cundall, O.D.L. Strack, Geotechnique 29 (1979) 47. | DEM 원전 | 없음 (wishlist 에 이미 있음 — 다른 카드의 참고 인쇄 그대로) |

## 13. [미확인] 목록 (원문 16 쪽 전수에 없음)
1. 접선 강성 비 s 의 값 · 계산 코드 이름 · 계산 시간 · 하드웨어 · 시드 · 반복.
2. 0.8 mm 틈의 결과 (표 1 범위에만) · 1.0 mm 틈 결과 (본문 '보이지 않음').
3. 실제 장치 채움 (*"preserving the overall loading"* 의 기준값) · 실제 장치 크기 · 실제 장치 축 방향 (중력).
4. host 재료 이름 (밀도 1.20 g/cm³ 만) · 실제 재료 강성.
5. 그림 16–18 '평균' 막대의 평균 방식 · 그림 15 의 평균 값.
6. Yokoyama 실험 장치 크기 · 2.1 승의 출처 (원 Kona 논문).
7. 우리 쪽: Lacey 판독기의 칸 배분 방식 (중심 · 부피) · MF 꼴 계산의 실제 비용 (위 §7-2 는 비례 어림).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-24)
- 서지: 후보 표 N-155 · 지시서 메모 (W. Chen · R.N. Dave · R. Pfeffer · O. Walton · 제목 · Powder Technol. 146 (2004) 121–136 · DOI 10.1016/j.powtec.2004.07.014) = 원문 첫 쪽과 같음 (DOI 인쇄 · 이름 전체 · 소속 둘 · 날짜 넷 · 키워드 4 · 교신 이메일) · SI 안내 없음 (16 쪽 글자 층 전수).
- 숫자: 글자 층 + 렌더 (300–400 dpi) 로 대조 — 표 1 전 칸 · 표 2 여덟 값 · 식 1–12 · Δt 식 · 2–5 mm · 0.5 mm · 0.1–2 wt% · n = 40 · 1 % · 10 지름 · 1500 · 1.6 mm · 2000 rpm · 10 s · 2 s · 2–4 s · 3–10 s · 1.97 · 2 · around 5 · 2.1 · 500 · 800 · 1000 · 1200 · 1500 · 1000 · 2000 · 3000 rpm · about four times · 1.0 mm · twice · almost five times · tens of thousands · 10 %.
- 그림: 그림 7–20 은 전부 벡터 → `get_drawings` 좌표 판독 (337 행) · 교차 검산 (고리 평균 ↔ 그림 10 · 그림 11a ↔ 12 · 13a · 그림 20 ↔ 표 2 · 인구 합 ↔ 1500) · 그림 1–6 · 14 는 그림 관찰.
- 크롭 55 장 전부 열어 확인 (도구 22 장 → 손으로 다시 자름: 그림 1 라벨 · 그림 3 왼쪽 · 그림 8 오른쪽 축 잘림 · 표 1 · 2 = 쪽 전체 상자 / 식 13 장 = 식 번호별로 손으로 자름 — 그 가운데 Δt 식 하나만 앞 줄 글자가 근호 위로 겹쳐 앞 줄을 지운 사본에서 다시 자름 / 근거 문단 20 · 다섯 장은 문장 경계에서 시작 · 끝나게 앞 · 뒤 낱말을 흰색으로 가림).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 + 'Mechanofusion system' · 'powtec.2004.07.014' · 'Wenliang' grep — 카드 없음 · 인용한 카드도 없음 (2026-11-24) · 같은 저자 · 같은 해 다른 카드 없음.

## 🔗 관련 카드
- 같은 그룹 · 같은 저자: `pfeffer2001_dry_particle_coating_engineered_particulates` (NJIT 총설 · 이 논문 ref [2] · MF 원리 · MAIC DEM) · `walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem` (공저자 Walton · ref [10] · 같은 법선 법칙의 3D 판).
- 메카노퓨전 · 고속 믹서 건식 코팅 실험 · DEM: `kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact` (AMS-Mini · LPSCl → NCM811) · `kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable` (Nobilta · Rocky DEM · SI ∝ n^1.76) · `frankenberg2024_dem_high_intensity_mixer_assb` (SI ∝ n^2.17) · `kawaguchi2017_dry_coating_parametric_na2so4_model_se` · `kawaguchi2018_dry_coating_model_se_particle_powtec` (Hybridizer 날 끝 속도 창) · `lee2026_mechanical_halogen_argyrodite_drycoating` (우리 랩 · FEM 단일 충돌 15 m/s).
- 드럼 · 접촉 법칙 이웃: `chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed` (같은 Walton–Braun 법칙 + 상수 인력 점착) · `mellmann2001_transverse_bed_motion_rotating_cylinders_slumping_rolling_cascading_froude` (드럼 운동 꼴 — MF 는 원심 꼴 쪽) · `luding2008_cohesive_frictional_contact_models` (hooke/hysteresis 정의서).
- 같은 그룹 · 앞선 개관 (2003 · 메카노퓨전 2D · Hybridizer 축소 3D · MAIC 자석 쌍극자 · 이 카드의 그림 7 · 11a · 12 와 같은 자료 · 그림 8 (편차 운동 에너지) 은 다른 값 · 힘 ∝ rpm 을 본문은 '선형' · 2026-11-24 카드): `dave2003_dry_coating_dem_mechanofusion_hybridizer_maic_three_devices`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
