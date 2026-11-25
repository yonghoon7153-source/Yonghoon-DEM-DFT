<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 (후보 표 N-156 · 4 순위 · 1저자 11-23 업로드 · 믹서 논지 · 코팅 과정 DEM 구현 시도 Q3) 에서 꼭 뽑으라고 한 항목.
     본 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표) · 믹싱 · 점착 절 구성 = jarray2019_cohesion_driven_mixing_segregation_drum.md · 같은 그룹 짝 = chen2004_mechanofusion_dry_coating_dem_2d_host_scraper_inner_piece_collision_frequency.md (§0-2 공백 검사 꼴 · §7-2 코팅 DEM 대입 꼴 · 같은 메카노퓨전 계산의 전체 판).
     쪽 표기 = 인쇄 쪽 "p.NNN" (Adv. Powder Technol. 14 (4) (2003) 449–470 · PDF n 쪽 = 인쇄 p.(448 + n) · figures.json 의 page 와 크롭 이름 txt_p<n> · eq 의 page 는 PDF 쪽).  보충 자료 (SI) 안내 없음 · 표 0 · 그림 20 · 번호 식 6 (MAIC 자기 쌍극자 · 이 논문의 번호 식 전부) · 참고문헌 12.
     값 표지: [인쇄] = 본문 · 그림 안 글자 / [판독] = 그림에서 읽은 값 (그림 7–9 · 12–16 은 1-bit 300 dpi 래스터 — 격자선 · 눈금 직선 맞춤으로 환산하고 표지 중심 = 열기 (binary opening) 뒤 무게중심 · 겹친 시간 계열은 한 덩어리의 가운데 + 퍼짐 · 재현 = litdb/figures/<slug>/digitized.csv 112 행) /
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산 (식 · 가정 병기) / [우리 산술] = 원문 밖 값 (우리 덱 · 리포 문서 · 다른 정본 카드) 과 엮은 계산 / [다른 카드 값] = 정본 카드의 값 그대로 / [카드 추론] · [카드 해석] = 이 카드의 해석 / [그림 관찰] = 그림을 보고 적은 꼴 (수치 아님) / [미확인] = 원문 22 쪽 전수에 없음.
     글자 층은 합자 (fi · fl · ff 가 빠짐: 'uid' · 'xed' · 'eld' · 'signicantly') 와 기호 ('=' → 'D' · µ → '¹' · × → '£' · π → '¼' · 내적 점 → '¢' · 위첨자 마이너스 → '¡') 를 깨뜨린다 — 인용한 문장 · 숫자 · 식은 전부 400 dpi 렌더 (근거 크롭 20 · 식 크롭 6) 로 확인했다.  압밀 · 탈압 · MPM · FEM 은 이 논문에 없다. -->
# 건식 입자 코팅 장치 셋 — 메카노퓨전 (2D · host 1500 개 · 400 µm · 2000 rpm: 긁개가 있으면 편차 운동 에너지 ≈2 배 · 안쪽 조각 힘 ∝ 회전² [판독] ↔ 본문 '선형') · Hybridizer (축소 3D · 공기 없음 · 10,000 rpm: 입자–경계 충돌 ≈10⁶ /s ≫ 입자–입자 ≈10³ /s · 평균 충돌 속도 ∝ rpm 2.5–12.7 m/s) · 자기 보조 충격 코팅 MAIC (자석 100 개 쌍극자 DEM · 진동장 = 유동화) 를 한 Walton 형 소프트 구 DEM 으로 개관 — 게스트 (1 µm → 시간 간격 ≤10⁻⁹ s) · 점착 · 막 형성은 못 넣음 — Dave · Chen · Mujumdar · Wang · Pfeffer (Adv. Powder Technol. 2003)

> slug `dave2003_dry_coating_dem_mechanofusion_hybridizer_maic_three_devices` · DOI `10.1163/156855203769710672` · type `DEM (Walton-type soft-sphere code [9, 10] · normal loading stiffness 20,000 kg/s² · e 0.85 · tangential law / friction values not given · three dry-coating devices: Mechanofusion = 2-D host-only (1500 × 400 µm · 1200 kg/m³ · scraper = 3 fixed spheres · gap 1.6 mm · 2000 rpm 10 s · inner-piece force 1000–4000 rpm × 500–1500 particles) / Hybridizer = 3-D scaled-down (blade = 3 overlapping spheres × 6 · recycle tube replaced by exit → re-entry · no air · 400 µm · 2500 kg/m³ · 5,000–25,000 rpm) / MAIC = 100 magnets alone (point-dipole force + torque · uniform oscillating field) · no guest particles · no adhesion values · no film formation · agglomerate break-up computations not reported · validation = qualitative statements only)` · PDF `1db10fd7-Numerical_simulation_of_dry_particle_coating_processes_by_the_discrete_element_method.pdf` · digested `2026-11-24` · status ✅
>
> **원제**: *Numerical simulation of dry particle coating processes by the discrete element method* (p.449)
> **저자**: **Rajesh Dave**¹\* (교신 · dave@adm.njit.edu) · **Wenliang Chen**¹ · **Ajit Mujumdar**¹ · **Wenqiang Wang**¹ · **Robert Pfeffer**² — ¹ Department of Mechanical Engineering · ² Department of Chemical Engineering, New Jersey Center for Engineered Particulates, New Jersey Institute of Technology, Newark NJ 07102, USA (p.449) · *Advanced Powder Technology* **14** (4) (2003) **449–470** · © VSP and Society of Powder Technology, Japan 2003 · 접수 2003-01-31 · 게재 확정 2003-03-19 · 키워드 *Dry particle coating; numerical simulation; discrete element method; hybridizer; mechano fusion; MAIC* · **DOI 는 원문 22 쪽 어디에도 인쇄돼 있지 않다** — PDF 메타데이터 (XMP) 의 *doi:10.1163/156855203769710672* 가 지시서 메모와 같다 · 연구비 New Jersey Commission on Science and Technology R&D Excellence Award (# 01-2042-007-24) · NSF (CTS-9985618) (p.469).
> **이웃 카드 (링크만)**: [`chen2004_mechanofusion_dry_coating_dem_2d_host_scraper_inner_piece_collision_frequency`](chen2004_mechanofusion_dry_coating_dem_2d_host_scraper_inner_piece_collision_frequency.md) (같은 그룹 · 같은 메카노퓨전 계산의 전체 판 · 이 논문이 *"will appear in a separate paper"* 라고 미룬 빈도 · 접촉 힘) · [`pfeffer2001_dry_particle_coating_engineered_particulates`](pfeffer2001_dry_particle_coating_engineered_particulates.md) (같은 그룹 총설 · ref [6] · MF 2D DEM 과 MAIC DEM (자석 + host) 이 이미 실림) · [`walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem`](walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem.md) (ref [10] · 접촉 법칙 · 코드 계보 · 서지 다름 §3-10) · [`kawaguchi2017_dry_coating_parametric_na2so4_model_se`](kawaguchi2017_dry_coating_parametric_na2so4_model_se.md) · [`kawaguchi2018_dry_coating_model_se_particle_powtec`](kawaguchi2018_dry_coating_model_se_particle_powtec.md) (실제 Hybridizer NHS-0 로 황화물 모델 SE 를 NCM 에) · [`kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact`](kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact.md) (메카노퓨전 AMS-Mini 로 LPSCl 을 NCM811 에) · [`kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable`](kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable.md) (고강도 믹서 + DEM) · [`lee2026_mechanical_halogen_argyrodite_drycoating`](lee2026_mechanical_halogen_argyrodite_drycoating.md) (우리 랩 · RAM 건식 코팅 + FEM 단일 충돌).
> **판독 원자료**: `litdb/figures/dave2003_dry_coating_dem_mechanofusion_hybridizer_maic_three_devices/digitized.csv` (112 행 — 그림 7 28 · 그림 8 25 · 그림 9a 8 · 9b 13 · 그림 12 8 · 13 8 · 14 4 · 15 4 · 그림 16 14) · 크롭 **46 장** (그림 20 = 도구 20 장 전부 다시 자름 · 식 6 · 근거 문단 20) — `figures.json`.
> **이 카드가 서랍에 들어온 이유**: 후보 표 N-156 (1저자 11-23 업로드 · 믹서 논지) — *"메카노퓨전 · Hybridizer · 자기 보조 충돌 코팅 (MAIC) 세 장치 DEM 비교 (충돌 에너지 · 빈도) = 코팅 과정 DEM 에서 어느 장치를 흉내 낼지 고르는 근거 (Q3)"*.

> ★★ **한 줄로 왜 중요한가**: (i) 건식 코팅 장치 셋을 **한 Walton 형 소프트 구 코드** 로 돌린 개관이라 장치마다 다른 **응력 꼴** 이 숫자로 갈린다 — 메카노퓨전 = 원심으로 벽에 눌린 층을 안쪽 조각의 수렴 틈에서 압축 · 전단 (긁개가 그 층을 깨면 편차 운동 에너지 1.98 배 · 안쪽 조각 힘 ∝ ω^1.98 [판독]) / Hybridizer = **경계 (날 · 벽) 충돌이 입자끼리 충돌의 370–1900 배** (입자당 1.14 × 10⁶ ↔ 1.22 × 10³ /s · 1000 개 · 10,000 rpm = 937 배 [판독 · 카드 산술]) · 평균 충돌 속도 ∝ rpm^1.01 (2.50 → 12.74 m/s · 5000 → 25,000 rpm [판독]) / MAIC = 자석 쌍극자의 회전 · 충돌 (진동장에서만 운동이 사그라지지 않음).  (ii) **게스트를 못 넣는 이유를 숫자로** — 1 µm · 200 nm 게스트면 시간 간격 ≤ 10⁻⁹ s · host (400 µm) 계산도 10⁻⁶–10⁻⁷ s 로 '몇 초 = 몇 시간' (p.468) → 게스트 수준은 **덩어리 하나의 충돌 셋** (host · 평판 벽 · 두 평판 사이 압축) 으로 따로 본다 (Thornton 그룹 방식 · 계산 미보고: 풀림 ∝ 충돌 속도 · ∝ 1/게스트 표면 에너지 · 낮은 속도 = 되튐 · 두 벽 사이 압축이 가장 많이 깸 · p.468–469).  (iii) 저자들이 **장치마다 모델링에 꼭 필요한 물리** 를 적었다 — 메카노퓨전은 공기 없이 *"good qualitative agreement"* · Hybridizer 는 *"one must include the effect of the fluid in the system and its drag force"* · MAIC 는 자기 쌍극자 힘 · 토크를 새로 넣음 (p.452 · p.465) — 이것과 우리 덱 산술을 합치면 코팅 과정 DEM 의 **가장 싼 꼴 = 메카노퓨전 꼴 (회전 챔버 + 고정 안쪽 원통 + 고정 긁개)** 이다 [카드 산술 · 추론 · §7-2].
> ⚠ 단 **개관 (preliminary) 논문** — MF = 2D host 만 (chen2004 의 앞선 요약판 · 그림 7 · 9 는 같은 자료) · Hybridizer = 축소 3D · 공기 없음 · 장치 치수 · 강성 · 마찰 [미확인] · MAIC = 자석 100 개만 · 수치 0 · 덩어리 풀림 = 말뿐 · **점착 값 · 게스트 · 막 형성 0** · 실험 대조 = 정성 서술 (그림 · 값 없음) · 장치끼리 공통 지표 없음.  **절대값 전이 ✗** (장치 · 크기 · 재료 · 차원 · 강성 · 공기 모두 다름) — 옮길 것은 **장치별 응력 꼴 · 판독 틀 · 지수 (경향)** 이다.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 서브 µm 게스트를 µm host 에 기계적 힘으로 입히는 건식 코팅 장치 셋 — 메카노퓨전 (MF · Hosokawa) · Hybridizer (Nara) · 자기 보조 충격 코팅 (MAIC) — 을 Walton 형 소프트 구 DEM 으로 하나씩 돌려 (MF = 2D host 만 · Hybridizer = 축소 3D host 만 · 공기 없음 · MAIC = 자석 100 개만 · 점 쌍극자), 장치 규모의 운동 에너지 · host 규모의 충돌 빈도 · 평균 충돌 속도 · 고정 부품 (안쪽 조각) 힘을 내고, 게스트는 시간 간격 장벽 (≤ 10⁻⁹ s) 때문에 넣지 못해 '덩어리 하나의 충돌' 문제로 나눠 풀자는 방향을 적은 22 쪽 개관 (p.449–470).

| 우리 질문 (지시서 · 꼭 뽑을 것) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 장치 셋의 기하 · 운전 | **MF**: 회전 원통 챔버 + 고정 둥근 안쪽 조각 + 고정 긁개 · 원심 → 벽 · 수렴 틈 고전단 충돌 · 발산 틈에서 서로 · 벽에 붙음 · 긁개가 긁어 흩음 · **최대 2000 rpm** · 열 → 운전 시간 관리 (p.453–454) / **Hybridizer**: 원통 챔버 + 날 6 개 회전자 + 순환관 · 실험실 규모 **최대 16,000 rpm** · 기체가 입자를 순환 · 매우 짧은 시간에 코팅 (p.459–460) / **MAIC**: **1–2 mm 영구 자석** (barium ferrite · 폴리우레탄 피복) + host + 게스트를 작은 유리 용기에 · 진동 전원 코일 · 자석 회전 → 미세 전단 → 게스트 덩어리 풀림 (p.464–465) | [인쇄] · §0-3 |
| ② ★ DEM 모형 (2D/3D · 접촉 · 점착 · 게스트) | 공통 = Walton [9, 10] 소프트 구 코드를 장치마다 고침 (p.453) · 점착 **값 0** (모델이 *"auto-adhesion"* 을 다룰 수 있다고만 p.452) · **게스트 0 (세 장치 모두)** / MF = **2D · 1500 개 · 400 µm · 1200 kg/m³ · e 0.85 · 누름 법선 강성 20,000 kg/s² · 틈 1.6 mm · 2000 rpm 10 s** (p.455–456) / Hybridizer = **3D 축소 · 400 µm · 2500 kg/m³** · 날 = 겹친 구 셋 · 순환관 대신 출구 → 재투입 (p.461–462) / MAIC = 쌍극자 힘 · 토크 (식 1–6) · 자석 100 개 (p.465–467) | [인쇄] · §3-2 · §3-5 · §3-7 |
| ③ ★ 충돌 에너지 | MF: 편차 병진 운동 에너지 고리 평균 **22.6 ↔ 11.5 J/m³** (긁개 있음 ↔ 없음 · 1.98 배 · 본문 *"about 2 times"*) · 회전 운동 에너지 4.09 ↔ 2.47 [판독 · 카드 산술] / Hybridizer: 편차 병진 운동 에너지 바깥 고리 최대 **468 J/m³** (10,000 rpm · 1000 개) · 평균 충돌 속도 **2.50–12.74 m/s** [판독] / MAIC: 없음 — 충돌 하나의 에너지 **분포** 는 세 장치 모두 없음 | §3-3 · §3-6 |
| ④ ★ 충돌 빈도 | MF: 이 논문에 없음 (*"will appear in a separate paper"* p.459 = chen2004 표 2) / Hybridizer: 입자–경계 **9.9 × 10⁵ → 1.40 × 10⁶ /s** · 입자–입자 **582 → 1867 /s** (500 → 1500 개 · 10,000 rpm · 1.0 s 시점 · 입자당) · rpm 따라 입자–입자 ∝ rpm^0.97 · 입자–경계 ≈ 평평 (5000 → 20,000 rpm 에 −9 %) [판독 · 카드 산술] / MAIC: 없음 | §3-6 |
| ⑤ ★ 회전 속도 (rpm) 공정 축 | MF 안쪽 조각 힘 ∝ ω^**1.98** (법선) · 1.96 (접선) [판독] (본문 *"increase linearly"* ↔ 그림 범례 'Fn ~ w2') · 채움마다 지수 2.08–2.51 [카드 산술] / Hybridizer 충돌 속도 ∝ rpm^**1.01** · 입자–입자 빈도 ∝ rpm^0.97 [판독 · 카드 산술] — **최적 rpm 없음 (전부 단조)** | §3-4 · §3-6 |
| ⑥ ★ 실험 대조 | MF: 폴리스티렌 실험 [1] 의 힘 vs rpm *"linear relationship"* · 법선/접선 비 *"around 5"* 가 *"similar"* (실험 그림 · 값 없음 · p.459) · *"good qualitative agreement … with the experimental measurements and with kinetic theory"* (p.452 · 대조 안 보임) / Hybridizer: 없음 / MAIC: *"good agreement with well-known experimental observations"* (인용 없음 · p.467) | §3-4 · §11 |
| ⑦ ★ 장치별 응력 꼴 (서로 다른 점) | MF = 원심으로 눌린 층의 **압축 · 마모 · 마찰 전단** (*"compression, attrition and frictional shearing"* p.454) — 긁개가 층을 깸 / Hybridizer = **고속 충돌 · 경계 지배** (입자–경계 ≫ 입자–입자) + 기체 순환 / MAIC = 자석 회전의 **미세 전단 + 부드러운 충돌** (*"inducing soft coating by powder impaction"* · *"The spinning action induces micro-shear"* p.464–465) — 숫자로 갈림: MF (chen2004) 입자끼리/경계 ≈ 7 ↔ Hybridizer 경계/입자끼리 ≈ 940 [다른 카드 값 · 카드 산술 · §0-3] | §0-3 |
| ⑧ ★ 게스트 · 막 형성 · 점착 | 셋 다 게스트 0 · 막 0 · 점착 값 0 — 게스트 수준 = **덩어리 하나의 충돌 셋** (host · 평판 벽 · 두 평판 사이 압축) · 풀림 ∝ 충돌 속도 · ∝ 1/게스트 표면 에너지 · 낮은 속도 = 되튐 · **계산 미보고** (p.468–469) | §3-8 |
| ⑨ ★ 우리 코팅 과정 DEM 에 고를 장치 | 원문 권고 없음 · 카드 산술 → **MF 꼴** (지름 25 mm = 우리 드럼 · 평균 충돌 0.29 m/s (chen2004) = 우리 SE 강성에서 겹침 0.32 % · 공기 불필요) ↔ Hybridizer 꼴 (평균 2.5–12.7 m/s → 겹침 1.8–6.8 % · 1 % 계약을 지키려면 E 4.6–119 배 · Δt 0.47–0.09 배 + 공기 항력) ↔ MAIC 꼴 (자기 쌍극자 힘 새로 · 우리 공정 아님) | §7-2 [카드 산술 · 추론] |
| ⑩ '점착 비 기준' (γ_AM/γ_SE · 같은 SE 탐침 AFM 힘 비) | **없음** — 점착 대비 0 · 게스트 표면 에너지 한 줄 (덩어리 풀림 ∝ 1/γ_게스트 · 미보고) 만 | §0-2 |

⛔ **한정어 (떼지 말 것)**: ① **개관 (preliminary) · 계산 상세 대부분 없음** — MF 챔버 · 안쪽 조각 지름 · 마찰 · 접선 법칙 · Δt / Hybridizer 장치 치수 · 축소 비 · 강성 · e · 마찰 · 충돌 셈 정의 / MAIC 자석 크기 · 모멘트 · B0 · f · 셀 [미확인] ② MF = 2D · Hybridizer = 축소 3D (채움 비 유지) · **공기 없음** ③ 세 장치 모두 **host (또는 자석) 한 종 · 단분산 · 게스트 0 · 점착 값 0** ④ 재료 = 이름 없는 1200 kg/m³ host (MF) · *"mimicking magnesium powder"* 2500 kg/m³ (Hybridizer) · 자석 (MAIC) — 우리 NCM (4.85) · LPSCl (1.64 g/cm³) 과 다른 값 ⑤ **장치끼리 공통 지표가 없다** (MF = 에너지 · 힘 · Hybridizer = 빈도 · 속도 · 에너지 · MAIC = 그림) — 장치 사이 크기 비교는 이 카드의 산술 (§0-3 · §7-2) 뿐 ⑥ 실험 대조 = 정성 서술 (그림 · 값 없음) ⑦ 반복 · 시드 · 오차 없음 ⑧ 그림 판독 = [판독] (1-bit 래스터 · 격자선 · 눈금 직선 맞춤 · 잔차는 digitized.csv 의 method 칸 · 겹친 시간 계열은 덩어리 가운데).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-156 의 '왜' 칸)

의도 원문: *"후보 표 6 절 (우선순위 4 · 1저자 11-23 업로드 · 믹서 논지) — 메카노퓨전 · Hybridizer · 자기 보조 충돌 코팅 (MAIC) 세 장치 DEM 비교 (충돌 에너지 · 빈도) = 코팅 과정 DEM 에서 어느 장치를 흉내 낼지 고르는 근거 (Q3)"* · 근거 칸 = *"1저자 11-23 업로드 (메인 세션 검색 제안 → 1저자 PDF)"* → **가리킨 카드 없음** (2 차 인용 대조 대상 없음) · 지시서 덧붙임 (꼭 뽑을 것 = 장치마다 기하 · 운전 · DEM (2D/3D · 접촉 · 점착 · 게스트) · 충돌 에너지 · 빈도 · 결과 비교 · 실험 대조 · 장치별 응력 꼴 · 우리 구현에 고를 장치와 근거 / 우리 질문 = '점착 비 기준' · rpm 공정 축 · 코팅 과정 DEM / 공백 검사 G1–G4).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "메카노퓨전 · Hybridizer · 자기 보조 충돌 코팅 (MAIC) 세 장치" | **채움** | 제목 · 초록 (p.449) · §2 MF (p.453–459) · §3 Hybridizer (p.459–464) · §4 MAIC (p.464–468) |
| "DEM" | **채움 (장치마다 범위가 다름)** | *"the DEM model developed by Walton et al. [9] is used and modified to analyze the Mechanofusion, Hybridizer and MAIC systems"* (p.453) — MF 2D host 만 (p.455) · Hybridizer 3D host 만 · 공기 없음 (p.460–462) · MAIC 자석 100 개만 (p.465–467) |
| "비교" | **일부 (나란히 놓았을 뿐)** | 공통 지표로 견준 표 · 그림 · 문장 없음 — 장치마다 다른 양: MF = 회전 · 편차 운동 에너지 · 안쪽 조각 힘 (그림 7–9) · Hybridizer = 입자당 충돌 빈도 · 평균 충돌 속도 · 편차 운동 에너지 (그림 12–16) · MAIC = 자석 배치 그림 (그림 18–20) · 맺음도 장치 비교가 아니라 'DEM 의 쓸모' (p.469) |
| "(충돌 에너지 · 빈도)" | **일부** | 충돌 빈도 = Hybridizer 만 (MF 는 *"will appear in a separate paper"* p.459) · '충돌 에너지' = 운동 에너지 밀도 (MF · Hybridizer 고리) + 평균 충돌 속도 (Hybridizer) — 충돌 하나의 에너지 분포 없음 · MAIC 는 둘 다 없음 |
| "= 코팅 과정 DEM 에서 어느 장치를 흉내 낼지 고르는 근거 (Q3)" | **일부** | 원문은 장치를 고르지 않는다 · 대신 장치마다 모델링에 필요한 것을 적었다 — MF 공기 없이 정성 일치 (p.452) · Hybridizer 공기 · 항력 필수 (p.452 · p.460–461) · MAIC 쌍극자 힘 · 토크 (p.465) · 게스트 = 시간 간격 ≤ 10⁻⁹ s (p.468) → 고르기는 이 카드의 산술 (§7-2 · MF 꼴) |
| (꼭 뽑을 것) 장치마다 기하 · 운전 · DEM (2D/3D · 접촉 · 점착 · 게스트) | **채움 (치수 · 물성 일부 [미확인])** | §0-3 · §3-2 · §3-5 · §3-7 |
| (꼭 뽑을 것) 충돌 에너지 · 빈도 · 결과 비교 · 실험 대조 · 응력 꼴 | **일부** | §3-3–3-7 · 실험 대조 = 정성 서술뿐 · 응력 꼴 = 원문 서술 + 이 카드의 빈도 비 (§0-3) |
| (꼭 뽑을 것) 우리 구현에 고를 장치와 근거 | **일부 (카드 산술)** | §7-2 |
| (우리 질문) '점착 비 기준' | **없음** | 점착 값 0 · 점착 대비 0 |
| (우리 질문) rpm 공정 축 | **일부** | 단조 경향만 (MF 힘 ∝ ω^≈2 · Hybridizer 충돌 속도 ∝ rpm) · 최적 · 맞교환 없음 |
| (우리 질문) 코팅 과정 DEM | **일부** | 장치 · host 규모까지 · 게스트 · 막 = 없음 (방향 = 덩어리 충돌 셋) |
| 가리킨 카드의 2 차 인용 값 | **해당 없음** | 근거 칸 = 1저자 업로드 · 정본 카드 가운데 이 논문을 인용한 카드 없음 (papers/ 전수 git grep 'dry particle coating processes' · '156855203769710672' · 'Mujumdar' · 'Adv. Powder Technol. 14' · 'Dave … 2003' = 0 건 · 2026-11-24) |

⇒ **의도 대조 결과: 일부** — 세 장치 DEM 은 원문이 채운다 / '비교 (충돌 에너지 · 빈도)' 는 장치마다 다른 양을 나란히 놓은 것뿐 (공통 지표 · MF 빈도 · MAIC 수치 없음) / '어느 장치를 흉내 낼지' 는 원문 권고가 없다 — 장치별 모델링 요구 (공기 · 쌍극자 · 시간 간격) 와 우리 덱 산술로 이 카드가 고른다 (§7-2: MF 꼴).

---

## 0-2. ★ 공백 검사 G1–G4 — 우리 믹서 논지 문장을 이 논문이 이미 했나 (정독 출력 batch_161 끝 절과 같은 판정)

| # | 우리 공백 문장 (11-23 지시) | 판정 | 근거 (쪽 · 문장) | 반례 · 일부면 우리 문장을 이렇게 좁힌다 |
|---|---|---|---|---|
| **G1** | 점착 대비를 설계 변수로 혼합 결과 (덮임 ↔ 뭉침 · 섞임 ↔ 분리) 를 예측 | **없음** | 점착 값 0 · 게스트 0 · 혼합 지수 0 (세 장치 모두).  가장 가까운 문장 = 게스트 덩어리 풀림: *"The detailed computations, not reported here, indicate that the extent of break-up of an agglomerate is proportional to the relative impact velocity and inversely proportional to the surface energy of the primary guest particles."* (p.469) — 게스트 **한 종의 응집 (표면 에너지)** 이지 host ↔ 게스트 **점착 대비** 가 아니고, 덮임 ↔ 뭉침 예측이 아니며, 계산도 안 보였다 | 좁힐 필요 없음.  덧붙일 것 = '덩어리 풀림 ∝ 충돌 속도 · ∝ 1/γ_게스트' 는 우리 논지의 SE–SE 응집 쪽 (γ_S ↑ → SE 덩어리가 덜 풀림) 과 방향이 같은 **정성 진술** 이다 (Dave 2003 · 미보고 계산 · 인용은 '방향' 까지) |
| **G2** | 점착 입력을 따로 재고 (AFM · IGC · 접촉각 등) 혼합 결과를 미리 예측 | **없음** | 점착 · 표면 에너지 측정값 0 · MF 입력은 값만 (p.456) · 실험 대조는 정성 서술 (p.459 · p.467) | 좁힐 필요 없음 |
| **G3** | 회전 속도 최적을 입자 수준 맞교환 (덩어리 풀림 ↔ 벽 부착 손실 등) 으로 설명 | **일부** | (가) 벽 부착 ↔ 운동 세기의 입자 수준 대조: 긁개 없음 = *"particles stick to the boundary during processing and their rotation is only rigid body rotation"* (p.457) · 편차 운동 에너지 평균 *"about 2 times"* (p.458 · 판독 1.98) — 원심 · 무점착 · **긁개 유무로 바꿈 (rpm 아님)** (나) 덩어리 풀림의 낮은 속도 쪽: *"when the impact takes place at a very low velocity, the agglomerate does not shatter and even rebounds"* (p.469 · 미보고 계산) (다) rpm 은 세기를 단조로 키울 뿐 (MF 힘 ∝ ω^1.98 · Hybridizer 충돌 속도 ∝ rpm^1.01 [판독]) · 최적 · 맞교환 없음 · 공정 쪽 위 한계는 MF 의 열 한 줄 (*"The running time and other operating conditions are kept under control to prevent burning of the particles."* p.454) | 우리 문장을 이렇게 좁힌다: *"벽 부착이 충돌 세기를 깎는다는 입자 수준 대조 (긁개 유무 · 원심) 와 덩어리 풀림의 낮은 속도 쪽 한계 (되튐) 는 무점착 DEM 개관에 이미 서술돼 있다 (Dave 2003 · Chen 2004) — 우리 몫은 점착 대비가 있는 계에서 rpm 을 축으로 덩어리 풀림 ↔ 벽 점착 손실의 맞교환과 그 최적을 보이는 것"* |
| **G4** | 공정 × 재료 상태도 (회전 세기 × 점착 · Bond 수 등) 가 다른 재료로 옮겨 감 | **없음** | 상태도 · Bond 수 0 · 재료는 장치마다 하나씩 (이름 없는 host · 'magnesium 흉내' · 자석) · 재료를 바꾼 계산 없음 | 좁힐 필요 없음 |

---

## 0-3. ★ 세 장치 한 표 (지시서 '꼭 뽑을 것' — 기하 · 운전 · DEM · 잰 양 · 결과 · 실험 대조 · 응력 꼴)

| 항목 | 메카노퓨전 (MF) | Hybridizer | MAIC |
|---|---|---|---|
| 실제 장치 (원문 서술) | Hosokawa Micron (1980 년대 중반) · 회전 원통 챔버 + 고정 둥근 안쪽 조각 (반지름 < 챔버) + 고정 긁개 날 · 최대 2000 rpm · 열 많음 → 운전 시간 관리 (p.453–454 · 그림 3) | Nara Machinery (도쿄) · 원통 챔버 + 날 6 개 회전자 · 위 출구 → 순환관 → 가운데 · 실험실 규모 최대 16,000 rpm · *"very intense … very short amount of time"* (p.459–460 · 그림 10) | 1–2 mm 영구 자석 (보통 barium ferrite · 폴리우레탄 피복) + host + 게스트 · 작은 봉한 유리 용기 · 진동 전원 코일 (p.464–465 · 그림 17) |
| 응력 꼴 (원문 말) | 원심 압축 → 수렴 틈 *"high shear-rate collisions"* · *"compression, attrition and frictional shearing"* · 발산 틈에서 서로 · 벽에 붙음 → 긁개가 긁음 (p.454) | 날 · 벽과 *"many impacts"* · 기체 + 원심으로 순환 (p.460) | 자석이 *"spin and collide and to fluidize the powder mixture"* · *"The spinning action induces micro-shear, which helps to deagglomerate the guest particles"* · *"soft coating by powder impaction"* (p.464–465) |
| 계산 차원 | **2D** (*"so as to keep the computations to a reasonable value"* p.455) | **3D** (*"Unlike the MF system, here, the simulation is carried out in three-dimensions."* p.462) | 직육면체 셀 · 그림 18–20 = 3D 로 그려짐 [그림 관찰 · 차원 서술 없음] |
| 입자 | host 만 · **1500 개 · 400 µm · 1200 kg/m³** (p.456) | host 만 · **400 µm · 2500 kg/m³** (*"mimicking magnesium powder"*) · 500–1500 개 (p.462 · 그림 12) | **자석 100 개만** (크기 · 모멘트 [미확인]) (p.466) |
| 접촉 · 물성 | Walton 소프트 구 · **e 0.85 · 누름 법선 강성 20,000 kg/s²** (p.456) · 마찰 · 접선 [미확인 — chen2004 에는 있음] | *"The same model has also been used to simulate the Hybridizer system"* (p.452) · 강성 · e · 마찰 [미확인] | Walton 코드 + **점 쌍극자 힘 · 토크 (식 1–6)** · 균일 진동장 B0 sin(2πft) k (식 3) |
| 경계 · 특수 처리 | 챔버 원 · 편심 안쪽 원 · 긁개 = 같은 크기 고정 구 (그림 4 = 셋) 를 비스듬히 · 긁개–벽 틈 0 · 긁개–챔버 상호작용 없음 (p.454) | 날 = **겹친 구 셋** · 순환관 없음 → 바깥 경계에 닿으면 출구 영역에서 빼고 같은 수를 안쪽 원통 바깥 경계로 **다시 넣음** · 축소 장치 · 채움 비 유지 (p.461–462 · 그림 11) | 모멘트를 회전 행렬로 몸체 좌표 갱신 (식 6) · 실험실 좌표 힘 · 토크 → 주축 몸체 좌표로 바꿔 Euler 식에 (p.466) |
| 공기 · 유체 | 없음 (원문 말 없음 · *"good qualitative agreement"* p.452) | **없음 — 그러나 중요** (*"the air (gas) in this system plays an important role"* · 다음 연구에서 항력 · 이 결과는 *"conservative"* p.460–461) | — |
| 운전 (계산) | 2000 rpm · 10 s · 진단 2 s 평균 · 힘 = 1000–4000 rpm × 500–1500 개 (p.456 · 그림 9) | 10,000 rpm (그림 12 · 14 · 16) · 5000–25,000 rpm (그림 13 · 15) · 충돌 수 = 1.0 s 시점 · 그림 16 은 t 0–10 s | 장 0 · 정적 균일 · 진동 (B0 · f [미확인]) |
| 잰 양 | 회전 · 편차 병진 운동 에너지 (등부피 고리 7) · 안쪽 조각 장시간 평균 힘 | 입자당 충돌 빈도 (입자–입자 · 입자–경계) · 평균 충돌 속도 · 편차 병진 운동 에너지 (등부피 고리 7) | 자석 배치 (사슬 · 정렬 · 유동화) — 수치 0 |
| 핵심 값 | 편차 KE 고리 평균 22.6 ↔ 11.5 J/m³ (1.98 배) · 회전 KE 4.09 ↔ 2.47 · Fn 1.01 × 10⁻³ → 1.54 × 10⁻² N (1000 → 4000 rpm · ∝ ω^1.98) · Fn/Ft 4.41–4.51 [판독 · 카드 산술] | 입자–경계 1.14 × 10⁶ /s · 입자–입자 1.22 × 10³ /s (1000 개 · 10,000 rpm) · 평균 충돌 속도 2.50 → 12.74 m/s (∝ rpm^1.01) · 4.41–5.83 m/s (∝ N^−0.25) · 편차 KE 고리 7 468 J/m³ [판독] | 장 0 → 사슬 · 덩어리 · 정적 → 정렬 · *"No significant chains"* · 진동 → *"the motion of particles never decays"* · 수직 운동 + 회전 (p.466–467) |
| 실험 대조 | 폴리스티렌 [1] 과 '선형' · Fn/Ft ≈5 '비슷' · 채움 포화 · *"at least qualitatively"* (p.459) — 실험 그림 · 값 없음 | 없음 | *"good agreement with well-known experimental observations"* (인용 없음 · p.467) |
| 원문 판단 | 긁개 = *"a crucial component … cannot be ignored in modeling/analysis"* (p.459) | *"for a more realistic modeling, one must include the effect of the fluid in the system and its drag force on the particles"* (p.452) | *"This demonstrates the importance of the time-varying character of the external field in supporting the particles' motion."* (p.467) |

**장치끼리 숫자를 나란히 놓으면** [카드 산술 · 다른 카드 값 — 정의 · 차원 · 재료 · rpm 이 달라 크기 비교가 아니라 꼴 비교]:
- **충돌의 꼴**: MF (chen2004 표 2 의 인구 가중 계 평균 · 2D · 2000 rpm) 입자–입자 6.9 × 10³ · 입자–경계 940 /s → **입자끼리 / 경계 ≈ 7** (chen2004 카드 §3-7 [그 카드 산술]) ↔ Hybridizer (이 논문 · 3D · 10,000 rpm · 1000 개) 입자–입자 1.22 × 10³ · 입자–경계 1.14 × 10⁶ /s → **경계 / 입자끼리 ≈ 940** [판독 · 카드 산술] — MF = 눌린 층 속 입자끼리 충돌이 지배 · Hybridizer = 날 · 벽 충격이 지배.  ⚠ '충돌' 셈 정의는 두 논문 모두 [미확인] (§3-6 의 접촉 시간 모순).
- **편차 병진 운동 에너지**: MF 긁개 있음 최대 37.2 J/m³ (고리 4 · 2D · 1200 kg/m³) ↔ Hybridizer 최대 468 (고리 7 · 3D · 2500 kg/m³) → 12.6 배 · 고리 평균 22.6 ↔ 129 → 5.7 배.
- **충돌 속도**: MF 법선 평균 0.285 m/s (chen2004 그림 16 판독 · 2000 rpm) ↔ Hybridizer 평균 5.05 m/s (10,000 rpm · 무엇의 평균인지 [미확인]) → 18 배.

---

## 1. 한 줄 요약
**건식 입자 코팅 장치 셋 (메카노퓨전 · Hybridizer · MAIC) 을 한 Walton 형 소프트 구 DEM 코드로 다룬 NJIT 그룹의 개관 — 메카노퓨전 2D 는 긁개가 벽에 붙어 같이 도는 층을 깨 편차 운동 에너지를 두 배로 만든다는 것과 안쪽 조각 힘의 회전 의존 (그림 기울기 ≈2 · 본문 '선형') 을, Hybridizer 축소 3D 는 경계 충돌이 입자끼리 충돌보다 세 자릿수 많고 평균 충돌 속도가 rpm 에 비례한다는 것을, MAIC 는 진동 자기장에서만 자석 운동이 유지된다는 것을 보이고, 게스트 입자는 시간 간격 (≤10⁻⁹ s) 때문에 넣지 못해 덩어리 하나의 충돌 문제로 나눠 풀자고 제안한 22 쪽 논문.**  점착 · 막 형성 · 장치 비교의 공통 지표는 없고, 실험 대조는 정성 서술이다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **R. Dave\* · W. Chen · A. Mujumdar · W. Wang** (NJIT 기계공학) · **R. Pfeffer** (NJIT 화학공학) | *Adv. Powder Technol.* 14 (4) (2003) 449–470 · 22 쪽 | 10.1163/156855203769710672 (원문 인쇄 없음 · PDF 메타데이터) | MF: 이름 없는 host (400 µm · 1200 kg/m³) / Hybridizer: 'magnesium 흉내' 400 µm · 2500 kg/m³ / MAIC: 자석 (실제 장치 = barium ferrite 1–2 mm · 계산 값 [미확인]) / 그림 1 실험 = PMMA 150 µm + 서브 µm alumina (MAIC) · SE · AM · 전극 재료 없음 | **계산 (DEM · 장치 셋 개관)** · 실험 0 (그림 1 SEM 사진만) · 압밀 0 |

- **1저자 메모 · 후보 표와의 대조**: 저자 다섯 · 제목 · 학술지 · 권 14 (4) · 쪽 449–470 · 2003 = **같다** · DOI = 원문 22 쪽에 **인쇄 없음** → PDF 메타데이터 (XMP) 값과 같다 (메모의 "첫 쪽 · DOI … = 검색 · 원문에서 확인" 가운데 '첫 쪽' 에는 DOI 가 없다) · 이름 전체 = Rajesh · Wenliang · Ajit · Wenqiang · Robert.
- **글의 꼴**: 1. 서론 (1.1 모델링 문제 · 1.2 DEM) → 2. MF (2.1 기하 모형 · 2.2 진단량 · 2.3 결과: 2.3.1 긁개 있음 / 없음 비교 · 2.3.2 안쪽 조각 힘) → 3. Hybridizer (3.1 모형 · 3.2 결과) → 4. MAIC (식 1–6 · 자석 100 개) → 5. 덩어리 풀림 · 앞으로 → 6. 맺음 → 참고 12.
- **계보**: Cundall & Strack 1979 [8] (DEM) · Walton & Braun 1986 [9] · 1993 [10] (접촉 · 코드) · Yokoyama 등 1987 [1] (MF 실험 · 이 논문의 대조) · Honda 등 1987 [2] · Otani 등 1996 [3] (Hybridizer 실험) · Singh 등 1997 [4] · Ramlakhan 등 2000 [5] (MAIC 실험) · Pfeffer 등 2001 [6] (같은 그룹 총설) · Chen & Huang 1997 [7] (MF 유체역학 바탕 해석 모형) · Kafui & Thornton 1993 [11] · Lian · Thornton · Adams 1997 [12] (덩어리 충돌 DEM).
- **같은 그룹 세 보고의 자리**: `pfeffer2001` (총설 · MF 2D DEM · MAIC DEM (자석 + host) 그림) → **이 논문 (2003 · 장치 셋 개관 · Hybridizer 3D 추가 · MAIC 는 자석만)** → `chen2004` (MF 2D 전체 판 · 표 · 빈도 · 3D 점검) — §3-9.

---

## 3. 핵심 수치 · 식 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 왜 어려운가 — 세 길이 규모 · 모델링 요구 · DEM 고르기 (p.449–453 · 그림 1 · 2 · `txt_p1_…` · `txt_p2_p4_…` · `txt_p4_modeling_…` · `txt_p4_dem_…` · `txt_p5_…`)
- 건식 코팅 = *"tiny, sub-micron-sized (guest or fine) particles are coated onto relatively larger, micron-sized (host or core) particles"* · 용매 · 결합제 · 물 없음 · *"pioneered, mostly in Japan, about 10 years ago, and are still in the R&D stage of development and are rarely used commercially"* (p.449–450).
- 그림 1 (MAIC 실험 · SEM): 서브 µm alumina → 150 µm PMMA · 2.5 min = 큰 게스트 덩어리 · 10 min = *"fairly uniform"* (p.450) — 코팅이 덩어리 → 분산으로 시간에 따라 나아간다 (*"after repeated collisions of host particles (along with the guest agglomerates) with other host particles as well as with system components"*).
- 크기 차: *"ranging from 1 to 2 orders of magnitude (for the example shown in Fig. 1, it is over 2 orders of magnitude)"* → **세 길이 규모** = 장치 (기하 · 운동) · host (운동 · 충돌) · 게스트 (운동 · 덩어리 풀림 · host 로 옮겨 감) (p.450–452).
- 모델링 요구 (p.452): *"the modeling should take into account the mechanism of the motion of the device and the nature of collisions, i.e. intensity and frequency of collisions among particles as well as between the particles and the device. It should also account for the agglomerate break-up and transfer of guest particles from one host particle to another. Needless to say, taking care of all of these aspects is a major undertaking and is beyond the scope of this paper. However, the overall problem can be divided into sub-parts"*.
- 앞선 이론 = MF 의 유체역학 바탕 해석 [7] 하나 — *"it cannot provide information at the particle scale"* (p.450).
- **DEM 고르기 (p.452)**: 상호작용은 *"frictionless, elastic hard spheres to elastic-plastic, frictional soft spheres"* 사이 · 이 연구 = [9, 10] 의 소프트 구 · *"This approach can handle complicated inter-particle forces arising from auto-adhesion, friction and the presence of a viscous fluid."* (⚠ 이 논문 계산에 점착 · 유체 항은 없다) · 처음 상태 = 임의 위치 (입자끼리 겹침 허용 · 경계 · 고정 입자와는 금지) · 작은 임의 속도 · 총 운동량 0 · 그림 2 흐름도 (처음 위치 · 방향 · 속도 → 연결 목록 갱신 → 힘 · 토크 → 운동 방정식 적분 → 평균량 → t + Δt).
- 덩어리 쪽 (p.453): Kafui 등 [11] (덩어리 → 벽 충돌) · Lian 등 [12] (젖은 덩어리 쌍 충돌) → *"rather than modeling a complete dry particle coating system including host particles and agglomerates, one could focus on agglomerate behavior through particle dynamics simulations to improve on computational speed"* · 논문 목적 = *"to introduce this new exciting field for application of DEM"*.

### 3-2. ★ 메카노퓨전 — 장치 · 모형 · 조건 (p.453–456 · 그림 3–6 · `txt_p6_mf_…` · `txt_p6_p7_…` · `txt_p7_zones_…` · `txt_p7_p8_…`)
| 항목 | 원문 | 표지 |
|---|---|---|
| 장치 | Hosokawa Micron · 1980 년대 중반 · 회전 원통 챔버 + 고정 둥근 안쪽 조각 + 고정 긁개 날 · 안쪽 조각 반지름 < 챔버 (p.453 · 그림 3 = 챔버 벽 · 날 · 축 · 둥근 조각 · 회전 화살표) | [인쇄] · [그림 관찰] |
| 작동 | 원심으로 벽에 압축 → 수렴 틈에서 고전단 충돌 (입자끼리 · 챔버 벽 · 안쪽 조각) → 발산 틈에서 *"they adhere to each other and to the chamber wall"* → 날이 긁어 다시 흩음 · *"compression, attrition and frictional shearing"* · *"high speeds (up to 2000 r.p.m.)"* · 열 → *"kept under control to prevent burning of the particles"* (p.454) | [인쇄] |
| 기하 모형 | 바깥 원 = 챔버 · 편심 안쪽 원 = 안쪽 조각 · *"Exact modeling of the scraper is rather complicated"* → 긁개 = 고정 구 (powder 와 같은 크기) 를 비스듬히 · 긁개–벽 틈 0 · *"there is no interaction between scraper and the chamber"* (p.454 · 그림 4 의 긁개 = 구 셋 · 캡션의 'inset' 은 따로 없음 [그림 관찰]) | [인쇄] |
| 차원 · 입자 | **2D · host 만** (*"only a limited number of particles are required"* · *"so as to keep the computations to a reasonable value"* p.455) · **1500 개 · 400 µm · 1200 kg/m³ · 반발 계수 0.85 · 누름 법선 강성 20,000 kg/s²** (p.456) | [인쇄] |
| 틈 · 운전 | 안쪽 조각–챔버 경계 **1.6 mm** · **2000 rpm · 10 s** (p.456) · 힘 계산 1000–4000 rpm × 500–1500 개 (그림 9) | [인쇄] · [판독] |
| 진단 | 시간 평균 (*"long enough compared to the typical time taken by any particle interaction … short compared to the time scale of major changes"*) · 등부피 고리 V_i = V/N · **고리 너비 ≥ 최대 입경** (입자가 두 고리까지만) → **7 고리** (p.455 · 그림 5) · 2 s 동안 부피 평균 · 2D 부피 = 고리 두께를 host 지름 하나 (p.456) | [인쇄] |
| 이 논문에 없는 것 | 챔버 · 안쪽 조각 지름 · 마찰 · 접선 법칙 · Δt · 코드 이름 · 계산 시간 (chen2004 에는 챔버 25 mm · 안쪽 원통 10 mm · μ 0.4/0.5 · Walton–Braun 식 · Δt 식이 있다 — 그 카드 §3-1–3-2) | [미확인] |

- 카드 산술 (chen2004 카드 §3-2 와 같은 값): m = (π/6)d³ρ = **4.02 × 10⁻⁸ kg** · 되돌림 강성 K2 = K1/e² = 27,682 N/m (Walton–Braun 이면) · 두 입자 접촉 시간 (π/2)(1 + e)√(m_eff/K1) = **2.91 µs** (m_eff = m/2) · 입자–벽 4.12 µs (m_eff = m) · 지름 1 % (4 µm) 겹침 = 상대 법선 속도 3.99 m/s (입자–입자) · 2.82 m/s (입자–벽) [카드 산술 · 선형 스프링 누름 가지].
- **강성 둔감 주장**: *"It is noted that the particle properties may affect the simulation results; however, the particle stiffness does not significantly affect the kinematics of the system [1]."* (p.456) — ⚠ [1] = Yokoyama 등 Kona 실험 논문 (§3-10 · §11).

### 3-3. ★ 메카노퓨전 — 긁개 있음 ↔ 없음 (그림 6–8 · p.456–459 · `txt_p8_p9_…` · `txt_p9_p11_…`)
| 고리 (안 → 밖) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 고리 평균 [카드 산술] |
|---|---|---|---|---|---|---|---|---|
| 회전 KE · 있음 (J/m³ · 그림 7a) | 0.48 | 0.67 | 0.95 | 1.44 | 3.07 | 8.44 | **13.56** | 4.09 |
| 회전 KE · 없음 (그림 7b) | 0.12 | 0.39 | 0.70 | 1.30 | 3.29 | **10.06** | 1.42 | 2.47 |
| 편차 병진 KE · 있음 (J/m³ · 그림 8a) | 3.1 | 10.3 | 26.6 | **37.2** | 30.6 | 26.5 | 24.1 | **22.6** |
| 편차 병진 KE · 없음 (그림 8b) | 2.2 | 5.8 | 4.8 | 3.9 | 13.3 | **44.7** | 5.5 | **11.5** |

(전부 [판독] — 범례 t = 0 · 2 · 4 · 6 · 8 · 10 s 가운데 t ≥ 2 s 표지가 겹친 덩어리의 가운데 · 퍼짐 (예: 그림 8a 고리 4 35.8–38.5) 은 digitized.csv · t = 0 은 회전 KE 0 · 편차 KE 1.9–3.6 J/m³ (처음 임의 속도) · 2 s 부터 겹침 = 2 s 안에 정상)

- **읽기 (원문)**: 있음 = 회전 KE 가 반지름 따라 커짐 (*"the boundary zones have a larger rotational kinetic energy"*) / 없음 = 고리 7 회전 KE 가 떨어짐 → *"This implies that without the scraper, particles stick to the boundary during processing and their rotation is only rigid body rotation, which is subtracted off in the calculations."* (p.457 · 챔버 강체 회전은 빼고 계산) / 편차 KE = *"deviatoric or fluctuational"* · 있음 = *"evenly distributed"* · 없음 = *"much smaller"* · 예외 고리 6 (*"the outer boundary of the inner piece induces a larger fluctuation in the particle velocities"*) · 평균 *"about 2 times"* (p.458) → 판독 **1.98 배** · 회전 KE 1.66 배 [카드 산술] / 결론 *"the scraper is a crucial component of the MF system and does more than just preventing caking of the powder material. Unless the MF design is drastically altered, it is clear that the scraper is required for the proper operation of the device and cannot be ignored in modeling/analysis."* (p.458–459).
- ★ **chen2004 와 대조** (같은 조건 — 1500 · 1.6 mm · 400 µm · 1200 · 0.85 · 20,000 · 2000 rpm · 10 s): 그림 7 = chen2004 그림 7 과 고리마다 0.06 J/m³ 안 (같은 자료) [판독 · 다른 카드 값] / **그림 8 은 다르다** — 긁개 있음 고리 값이 chen2004 그림 8 ('운동 세기 지표' 식 10 · 2–4 s 평균) 의 **0.51–0.78 배** · 고리 평균 22.6 ↔ 32.6 · 있음/없음 비 **1.98 ↔ 2.37** (chen2004 본문 'more than twice') [판독 · 카드 산술] → 같은 계산의 다른 추정기 (이 논문 = 'deviatoric' 편차 KE · chen2004 = 영역 평균 속도를 뺀 지표 — *"not an accurate measure of the true deviatoric kinetic energy"* 그 논문 p.127) 이거나 다른 평균 창으로 보인다 — 두 원문 모두 설명 없음 [카드 추론 · 원인 미확인].

### 3-4. ★ 메카노퓨전 — 안쪽 조각 힘 (그림 9 · p.459 · `txt_p11_inner_piece_…`)
- 정의: *"This is a diagnostic quantity that can actually be measured experimentally, and can be used to monitor the system during its operation and for analyzing power consumption [1]."* · 모든 순간 값의 평균 = 장시간 평균 (p.459).

| rpm (1500 개) | 1000 | 2000 | 3000 | 4000 | 로그 기울기 (최소제곱) |
|---|---|---|---|---|---|
| 법선 Fn (N · 그림 9a) | 1.01 × 10⁻³ | 4.02 × 10⁻³ | 9.10 × 10⁻³ | 1.54 × 10⁻² | **1.98** |
| 접선 Ft (N) | 2.29 × 10⁻⁴ | 9.03 × 10⁻⁴ | 2.04 × 10⁻³ | 3.41 × 10⁻³ | **1.96** |
| Fn/Ft | 4.41 | 4.45 | 4.47 | 4.51 | — |

([판독] 로그–로그 축 · 범례 'Fn ~ w2' · 'Ft ~ w2' 굵은 선 · chen2004 그림 11a 와 0–3 % 안 = 같은 자료 · 끝점 기울기 1.97 · 1.95 [카드 산술])

- **채움 × rpm (그림 9b · N · 선형 축)** [판독 · 크기 순으로 rpm 배정 — 범례 표지 뒤바뀜 §3-10]:

| 채움 (개) | 500 | 800 | 1000 | 1200 | 1500 |
|---|---|---|---|---|---|
| 1000 rpm | ≈3 × 10⁻⁵ (세 표지 겹침) | 4.5 × 10⁻⁴ | 7.3 × 10⁻⁴ | 8.3 × 10⁻⁴ | 9.2 × 10⁻⁴ |
| 2000 rpm | ″ | 2.8 × 10⁻³ | 3.4 × 10⁻³ | 4.0 × 10⁻³ | 4.0 × 10⁻³ |
| 3000 rpm | ″ | 7.1 × 10⁻³ | 7.9 × 10⁻³ | 8.9 × 10⁻³ | 9.0 × 10⁻³ |

- 채움마다 rpm 지수 (1000–3000 rpm 최소제곱): 800 개 **2.51** · 1000 개 2.17 · 1200 개 2.17 · 1500 개 **2.08** [카드 산술] (chen2004 카드 §3-5 의 2.44 · 2.18 · 2.18 · 2.08 과 같은 꼴 · 값은 chen2004 그림 12 와 −8 – 0 % = 같은 자료).
- 원문 서술 (p.459): *"are found to increase linearly with the rotational speed of the chamber, as shown in Fig. 9a. This is in good agreement with an experimental study of polystyrene beads in the MF system, which also shows a linear relationship for the normal and tangential force with rotational speed [1]. Also, the ratio of the calculated normal force to the tangential force (around 5) is similar to the experimental result from [1]."* · *"For the same rotational speed, the force on the inner piece increases but gradually levels off as the loading of the system increases. At each loading, the increase in the force on the inner piece is linear with rotational speed. This behavior is also observed experimentally [1], indicating that the DEM simulations, at least qualitatively, can predict the experimental data."* → **그림 9a 의 범례 · 기울기 (≈2) 와 '선형' 이 맞지 않는다** — chen2004 는 같은 자료를 'ω²' (최적 맞춤 1.97 · Yokoyama 2.1) 로 적었다 [판독 · 다른 카드 값 · §3-10] · Fn/Ft 판독 4.4–4.5 ↔ 본문 'around 5'.
- 빈도 · 접촉 힘 · 틈 · 입자 성질 의존: *"These results are not presented here due to space limitations and will appear in a separate paper."* (p.459) = chen2004.

### 3-5. ★ Hybridizer — 장치 · 모형 (그림 10 · 11 · p.459–462 · `txt_p11_p13_…` · `txt_p13_p14_…`)
| 항목 | 원문 | 표지 |
|---|---|---|
| 장치 | *"a commercial powder surface modification system, called the Hybridizer (Nara Machinery, Tokyo, Japan)"* · 원통 챔버 + **날 6 개** 회전자 · 위 열림 → 관이 장치 가운데로 = 분말 순환 경로 · *"the blades rotate up to 16 000 r.p.m. (for a laboratory scale system)"* (p.459–460) · 그림 10 = 분말 투입구 · 밸브 · 배출구 · 순환관 · 케이싱 · 날 · 회전자 · 고정자 · 재킷 [그림 관찰] | [인쇄] |
| 작동 | 날 · 벽과 많은 충격 · *"Due to the presence of gas (air or other gases) and the centrifugal force of rotation, the particles get carried along with the gas through the recycle tube and are constantly recirculated. This is a very intense processing system and dry coating takes place in a very short amount of time."* (p.460) | [인쇄] |
| 공기 | *"It is evident that the air (gas) in this system plays an important role. However, the present simulation work is carried out without the effect of air … In a subsequent study, the effect of air is taken into account by adding a drag force due to the air motion."* · *"the results presented here are conservative, since when the effect of air is included, the particles will undergo more severe motions"* (p.460–461) | [인쇄] |
| 모형 | 날 = **겹친 구 셋** · *"the recycle tube is not explicitly modeled"* → 미리 정한 바깥 경계에 닿으면 출구 영역에서 빼고 *"another particle is generated and re-enters the chamber through the outer boundary of the inner cylinder"* · **축소 장치 · 채움 비 유지** · **3D** (p.461–462) · 그림 11 = 날 6 개 (구 셋씩 방사형) · 가운데 안쪽 원통에서 바깥으로 재투입 화살표 · 출구 = 바깥 원 오른쪽 위 호 [그림 관찰] | [인쇄] · [그림 관찰] |
| 입자 · 운전 | **400 µm · 2500 kg/m³** (*"mimicking magnesium powder"*) · 500–1500 개 · 기준 **1000 개 · 10,000 rpm** · rpm 5000–25,000 (p.462 · 그림 12–16) | [인쇄] · [판독] |
| 이 논문에 없는 것 | 챔버 · 회전자 · 날 치수 · 축소 비 · 채움 비 값 · 강성 · e · 마찰 · Δt · 계산 시간 · **충돌 셈 정의** | [미확인] |

- 카드 산술: m = 8.38 × 10⁻⁸ kg (400 µm · 2500 kg/m³).
- 우리 쪽 [다른 카드 값]: 실제 NHS-0 = 챔버 안지름 125 mm · 깊이 49 mm · 회전자 118 mm · 날 6 개 (`kawaguchi2017` 카드 L58) · 16,000 rpm = 날 끝 98.9 m/s (`kawaguchi2018` 카드 L63 [그 카드 산술]) · 선속도 50 m/s = 부분 피복 · ≥ 80 m/s = 완전 피복 (`kawaguchi2017` 카드 L8) / NJIT 의 Hybridizer Mg 코팅 실험 = Mg 75 µm · 5000–12,000 rpm · 2–4 분 (`pfeffer2001` 카드 L118) — 이 계산의 400 µm 와 다르다 · 계산 rpm 위 끝 **25,000 은 실험실 장치 최대 (16,000) 를 넘는다**.

### 3-6. ★ Hybridizer — 충돌 빈도 · 충돌 속도 · 운동 에너지 (그림 12–16 · p.462–464 · `txt_p14_p15_…` · `txt_p15_p16_…`)
**(가) 채움 (10,000 rpm · 1.0 s 시점 · 입자당)**

| 채움 (개) | 500 | 800 | 1000 | 1500 | 기울기 (채움 · 로그) |
|---|---|---|---|---|---|
| 입자–경계 (/s · 그림 12) | 9.85 × 10⁵ | 1.06 × 10⁶ | **1.14 × 10⁶** | 1.40 × 10⁶ | 0.32 |
| 입자–입자 (/s · 그림 12) | 582 | 977 | **1220** | 1867 | 1.06 |
| 경계 / 입자끼리 [카드 산술] | 1690 | 1090 | 937 | 751 | — |
| 평균 충돌 속도 (m/s · 그림 14) | 5.83 | 5.37 | 5.06 | 4.41 | **−0.25** |

**(나) rpm (1000 개)**

| rpm | 5000 | 10,000 | 20,000 | 25,000 | 기울기 (rpm · 로그) |
|---|---|---|---|---|---|
| 입자–경계 (/s · 그림 13) | 1.17 × 10⁶ | 1.13 × 10⁶ | 1.06 × 10⁶ | 1.08 × 10⁶ | **−0.06** |
| 입자–입자 (/s · 그림 13) | 611 | 1208 | 2341 | 2919 | **0.97** |
| 경계 / 입자끼리 [카드 산술] | 1915 | 933 | 454 | 371 | — |
| 평균 충돌 속도 (m/s · 그림 15) | 2.50 | 5.05 | 10.19 | 12.74 | **1.01** |

([판독] — 그림 12 · 13 = 로그 축 1–10⁷ (잔차 ≤ 0.012 자릿수) · 그림 14 · 15 = 선형 축 · 회색 마름모는 점묘라 닫기 (closing) 뒤 열기 · 기울기 = 로그–로그 최소제곱 [카드 산술])

- **원문 (p.462–463)**: *"each particle goes through on average about 1.0 × 10⁶ number of collisions with the boundary when the particle loading is 1000"* (판독 1.14 × 10⁶) · *"the number of particle–boundary collisions is several orders of magnitude higher than the number of particle–particle collisions"* (판독 370–1900 배 ≈ 3 자릿수) · *"In both cases, the number of collisions increases with increase in loading as well as increase in the rotational speed of the rotor. However, the increase in frequency of particle–boundary collisions is not significant as the loading or the rotation speeds increase. Nonetheless, particle collisions with the boundaries of the system, which include the blades as well, are dominant"* (⚠ 그림 13 의 입자–경계는 rpm 따라 늘지 않고 −9 % · §3-10) · 빈도 = *"an important parameter that plays a significant role in coating effectiveness"*.
- **충돌 힘 · 속도 (p.463)**: *"if a guest particle were present on the surface of a host particle, the impact force will determine how well the guest particle will get embedded onto the host particle. The relative impact velocity of the collision and the particle properties determine the force of impact during a collision."* · *"the impact velocities are inversely proportional with the particle loading, and are proportional to the rotational speed"* → 판독: **rpm 비례는 맞음** (기울기 1.01 · 5.0–5.1 × 10⁻⁴ m/s per rpm · 16,000 rpm 보간 8.1 m/s [카드 산술]) · 채움에는 '반비례' (−1) 가 아니라 **N^−0.25** (3 배 채움에 −24 %) [카드 산술 · §3-10] · '평균 충돌 속도' 가 입자–입자 · 입자–경계 어느 충돌의 평균인지 [미확인].
- **편차 병진 KE (그림 16 · 10,000 rpm · 1000 개 · 등부피 고리 7 · p.463–464)** [판독]: **5 · 19 · 31.5 · 46.1 · 113 · 223 · 468 J/m³** (고리 1 → 7 · t ≥ 2 s 표지 겹침 · 퍼짐 ±5–7 · 1 px = 1.2 J/m³) · t = 0 = 0 — *"indicating highest values occur at the outer zones"* · 고리 평균 129 [카드 산술] · 범례 t = 0 · 2 · 4 · 6 · 8 · 10 s → 이 런은 ≥ 10 s (충돌 수는 1.0 s 시점).
- ★ **규모 감각 · 셈 정의 모순 [카드 산술 · 가정]**: 입자–경계 충돌 사이 평균 **0.87 µs** · 입자–입자 0.82 ms (1000 개 · 10,000 rpm) / MF 강성 (K1 20,000 · e 0.85) 을 그대로 쓰면 이 입자의 입자–경계 접촉 시간 = **5.9 µs** → 1 초에 10⁶ 번의 '따로인' 충돌은 들어갈 수 없다 (접촉 시간 × 빈도 = 5.9) · 원문의 시간 간격 10⁻⁷ s 에 접촉당 40 step (chen2004 규칙) 이면 접촉 ≥ 4 µs → 최대 2.5 × 10⁵ /s ⇒ 강성이 훨씬 높았거나 (접촉 시간 ≤ 0.87 µs 면 K ≥ 9 × 10⁵ N/m) '충돌' 을 접촉 step 이나 날의 구 셋 접촉을 따로 세었을 수 있다 — 원문 정의 없음 [카드 추론 · 미확인].
- 같은 평균 속도의 겹침 (만약 MF 강성이면): 5.05 m/s → 입자–입자 1.8 % · 입자–경계 2.6 % · 12.74 m/s → 4.6 % · 6.5 % (지름 대비) [카드 산술 · 가정 = K1 20,000 N/m · 이 논문의 Hybridizer 강성 [미확인]].

### 3-7. ★ MAIC — 자기 쌍극자 DEM (식 1–6 · 그림 17–20 · p.464–468 · `eq_01_…`–`eq_06_…` · `txt_p16_p17_…` · `txt_p18_p19_…`)
- **장치 (p.464–465 · 그림 17)**: *"magnetic particles are used to agitate host and guest powders, thus inducing soft coating by powder impaction"* · 1–2 mm 영구 자석 (*"usually barium ferrite, coated with polyurethane"*) + host + 게스트 → 작은 유리 용기 · 봉한 용기를 진동 전원 코일에 · 자석이 *"spin and collide and to fluidize the powder mixture. The spinning action induces micro-shear, which helps to deagglomerate the guest particles and enhances the coating process."* · 그림 17 = 칼라 코일 (N–S · S–N) · AC 전원 · 용기 확대 (게스트 · 자석 · host) [그림 관찰] · 그림 1 (MAIC 실험) = PMMA 150 µm + 서브 µm alumina.
- **범위**: *"The focus of this preliminary study is on understanding the motion of the magnetic particles alone under the effect of the external field."* · 자석 = 점 쌍극자 (*"a reasonable and widely used approximation"*) (p.465).
- **식** (크롭 `eq_01_…`–`eq_06_…` · 이 논문의 번호 식 전부):
  - (1) **F = (m·∇)B** — 장의 기울기가 자석을 옮긴다 · (2) **T = m × B** — m 과 B 가 나란할 때만 토크 0 → 그 밖에는 돈다 (p.465).
  - (3) **B_ext = B0 sin(2πft) k** — 공간 균일 · 시간 진동 · k = 중력 방향 단위 벡터 · *"It is noted that this represents a conservative case, as compared to actual situations where the field will not be uniform in space and may even be rotating its direction. These two conditions will cause translation and sustained rotation of the particle, respectively."* (p.465–466).
  - (4) **B(j : i) = µ0/(4π r_ji³) [3(m_j·n_ji)n_ji − m_j]** — 쌍극자 j 가 i 자리에 만드는 장 (r_ji = 거리 · n_ji = j → i 단위 벡터) · (5) **F(j : i) = 3µ0/(4π r_ji⁴) [(m_j·m_i)n_ji + (m_j·n_ji)m_i + (m_i·n_ji)m_j − 5(m_j·n_ji)(m_i·n_ji)n_ji]** — 쌍극자–쌍극자 힘 (p.466).
  - (6) **m_i(t) = R⁻¹(t) m_i(0) = Rᵀ(t) m_i(0)** — 모멘트를 몸체 좌표 회전 행렬로 갱신 (힘 · 토크는 실험실 좌표 · Euler 식은 주축 몸체 좌표 → 토크를 바꿔 넣는다 · 원문 'principle body frame') (p.466).
- **검증 · 결과 (p.466–467 · 그림 18–20 · 자석 100 개 · 직육면체 셀의 직교 투영)**:
  - 장 0 → 쌍극자끼리만 → 퍼텐셜 에너지를 줄이며 일부는 소산 → *"After a short time, the system becomes still and forms a certain pattern (chains, agglomerates) in space."* (그림 18).
  - 정적 균일장 → 쌍극자가 장과 나란히 돌고 진동하다 소산으로 멈춤 → *"No significant chains are observed."* (그림 19).
  - *"These simulated results are in good agreement with well-known experimental observations, thus verifying the modified Walton code."* (인용 없음).
  - 진동장 (식 3) → *"the motion of particles never decays, even if there is energy dissipation"* · 많은 자석이 *"'fluidized'"* · 수직 운동 + 회전 (그림 20) · *"At present, a more comprehensive set of simulations is being performed to understand the motion of the magnets along with the host particles"* (p.467).
- **이 논문에 없는 것**: 자석 크기 · 모멘트 · B0 · f · 셀 크기 · 접촉 물성 · 충돌 빈도 · 에너지 · host [미확인] — 같은 그룹 `pfeffer2001` 카드는 MAIC DEM (자석 50 개 유동화 · 자석 2.36 mm 10–80 개 + PMMA 200 µm 1000 개의 충돌 수) 을 이미 옮겼다 (그 카드 L35 · L226–227) [다른 카드 값] → MAIC 쪽은 이 논문이 2001 총설보다 **적게** 보인다.

### 3-8. ★ 게스트 · 덩어리 풀림 · 시간 간격 · 맺음 (p.468–469 · `txt_p20_p21_…` · `txt_p21_concluding_…`)
- 한계 (p.468): *"the results are quite limited without the inclusion of guest particles, fluid effects, realistic device dimensions and operating conditions that very closely mimic the experiments"*.
- ★ **시간 간격**: *"The major limiting factor in these simulations is the time-step for the numerical integration, which is a strong inverse function of the particle size. Hence, if realistic guest particles are used, e.g. 1 µm or even as small as 200 nm, then the time-step becomes as small, or smaller than 10⁻⁹ s. The simulations reported in the previous sections utilized larger particles that required time-steps of 10⁻⁶ to 10⁻⁷ s and simulating only several seconds of physical time, required a number of hours on a computer workstation."* (p.468) → 같은 물리 시간에 step 수 10²–10³ 배 [카드 산술] · Δt ∝ d (Rayleigh · Hertz 꼴) 로 400 µm 의 10⁻⁷ s 를 옮기면 1 µm 2.5 × 10⁻¹⁰ · 200 nm 5 × 10⁻¹¹ s (≤ 10⁻⁹ 와 맞음) [카드 산술 · 가정] · 처방 = *"highly sophisticated numerical schemes as well as clever algorithm development are required that can take into account various length scales, without simulating the complete system at the smallest length scale"*.
- ★ **덩어리 풀림 (Thornton 그룹 [11, 12] 방식 · p.468–469)**: 경우 셋 = 덩어리–host 충돌 · 덩어리–평판 벽 충돌 · 두 평판 사이 압축 (*"These cases take into account most interactions that an agglomerate would undergo"*) · *"The detailed computations, not reported here, indicate that the extent of break-up of an agglomerate is proportional to the relative impact velocity and inversely proportional to the surface energy of the primary guest particles. Usually, when the impact takes place at a very low velocity, the agglomerate does not shatter and even rebounds. Among the three typical cases that are considered, usually the compression between two flat walls causes the most damage to the agglomerate. This could happen when the agglomerate is in between two colliding host particles or one host particle and the device boundary — both scenarios are highly likely during dry coating."* — 값 · 그림 0 [미확인].
- **맺음 (p.469)**: *"it is clear that by itself in its current form, DEM cannot provide a full picture of the dry coating process due to the severe computational burden created when guest particles are included in the simulation. Nonetheless, at the device level, DEM is useful for computing various kinematic variables such as rotational and translational kinetic energies, and, subsequently, granular temperature and granular pressure. At the host particle level, DEM is useful for computing the various forces acting on the particles in the system, and the distribution and frequency of collisions as well as their relative impact velocities."* — ⚠ 이 논문 안에는 입자 온도 · 입자 압력 · 충돌 **분포** 그림이 없다 (평균만 · 입자 압력은 chen2004).

### 3-9. ★ 같은 그룹 세 보고 — 겹침 · 다름 (`pfeffer2001` · 이 논문 · `chen2004`) [다른 카드 값 · 카드 산술]
| 항목 | `pfeffer2001` (총설) | 이 논문 (2003 개관) | `chen2004` (MF 전체 판) |
|---|---|---|---|
| MF DEM | 2D · host 만 · 긁개 = 둥근 입자 여럿 · 영역 1–4 · 영역 법선 힘 ≈0.65–1.6 × 10⁻³ N (그 카드 L148 · 판독) · 입자 크기 [그 카드 미확인] | 2D · 1500 · 400 µm · 1.6 mm · 2000 rpm · 회전 · 편차 KE (그림 7 · 8) · 안쪽 조각 힘 (그림 9) | 같은 조건 + 챔버 25 mm · 안쪽 원통 10 mm · 식 1–12 · 표 1 · 2 · 고리 7 · 영역 4 · 빈도 · 3D 점검 |
| 같은 자료 | — | 그림 7 = chen2004 그림 7 (0.06 J/m³ 안) · 그림 9a = 11a (0–3 %) · 그림 9b = 12 (−8 – 0 %) [판독] | ← |
| 다른 자료 | — | 그림 8 (편차 KE) ≠ chen2004 그림 8 (운동 세기 지표) — 0.51–0.78 배 · 있음/없음 1.98 ↔ 2.37 | ← |
| 힘 ∝ rpm | — | 본문 '선형' · 범례 'ω²' | 'ω² · 최적 1.97 · Yokoyama 2.1' |
| 강성 둔감 인용 | — | [1] (Yokoyama 등 · Kona 실험) | [10, 11] (Walton 1993 · Tsuji 1992) |
| Hybridizer | 실험 (Mg 75 µm · 5000–12,000 rpm · 그 카드 L118) | **3D 축소 DEM** · 빈도 · 속도 · KE | 없음 |
| MAIC DEM | 자석 50 개 유동화 · 자석 2.36 mm 10–80 + PMMA 200 µm 1000 · 충돌 수 vs 자석 수 (그 카드 L35 · L226–227) | 자석 100 개만 · 배치 그림 · 쌍극자 식 1–6 | 없음 |
| 덩어리 풀림 | [그 카드에 없음] | 방향만 (미보고 계산 · 경우 셋) | 없음 ('게스트 규모 모형' = 앞으로) |

⇒ 정본에서 **MF 장치 DEM 의 가장 이른 카드는 `pfeffer2001` (2001)** 이고 이 논문은 그 중간 판 · `chen2004` 가 전체 판이다 (§13 · 카드 문제: `chen2004` 카드 L50 의 'MF 장치 DEM 으로 정본에서 가장 이른 카드' 서술).

### 3-10. 원문 안 어긋남 (§11 에 다시)
1. **'선형' ↔ 'ω²'**: 본문 *"increase linearly with the rotational speed"* · *"At each loading, the increase … is linear with rotational speed"* (p.459) ↔ 그림 9a 범례 'Fn ~ w2' · 'Ft ~ w2' · 로그–로그 기울기 1.98 · 1.96 [판독] · 그림 9b 채움마다 2.08–2.51 [카드 산술] — chen2004 는 같은 자료를 'square' 로 적었다.
2. **그림 9b 범례 표지 뒤바뀜**: 범례 '◆ N = 1000rpm · ■ N = 2000rpm' 인데 ◆ 계열이 2000 rpm 크기 (그림 9a · chen2004 그림 12 와 대조) · ■ 계열이 1000 rpm 크기 [판독 · 카드 추론] · x 축 제목 *"loading of particles (s)"* (단위 's' 는 오기로 보임).
3. **그림 4 캡션 'inset'**: *"Note the formation of the scraper using three fixed spheres as shown in the inset"* ↔ 따로 확대한 그림 없음 (긁개 구 셋은 본 그림의 벽에) [그림 관찰].
4. **Hybridizer 충돌 수 vs rpm**: *"the number of collisions increases with … increase in the rotational speed"* ↔ 그림 13 입자–경계 −9 % (5000 → 20,000 rpm) · 기울기 −0.06 [판독] (원문 다음 문장 *"not significant"* 가 일부 받친다).
5. **'반비례'**: *"the impact velocities are inversely proportional with the particle loading"* ↔ 그림 14 = N^−0.25 (3 배 채움 −24 %) [판독 · 카드 산술].
6. **계산 rpm 범위**: 그림 13 · 15 = 25,000 rpm 까지 ↔ 실험실 장치 *"up to 16 000 r.p.m."* (p.459) · MF 힘 1000–4000 rpm ↔ *"up to 2000 r.p.m."* (p.454) — 실제 장치 범위 밖으로 뻗은 계산.
7. **'kinetic theory' 일치**: *"good qualitative agreement has been found with the experimental measurements and with kinetic theory"* (p.452) — 이 논문에 대조가 없다.
8. **강성 둔감의 근거**: *"the particle stiffness does not significantly affect the kinematics of the system [1]"* (p.456) — [1] = Yokoyama · Uehara · Naito 의 Kona 실험 논문 (DEM 강성 시험일 수 없다) · chen2004 는 같은 주장을 [10, 11] (Walton 1993 · Tsuji 1992) 로 받쳤다 · 정본 `walton1993` 카드는 오히려 *"pronounced sensitivity of the velocity and character of the deeper flows to the effective stiffness"* 를 옮겼다 (그 카드 L31 · 깊은 흐름) [다른 카드 값].
9. **충돌 셈 ↔ 접촉 시간**: 입자–경계 1.0 × 10⁶ /s (평균 간격 0.87 µs) ↔ MF 강성 접촉 시간 5.9 µs · Δt 10⁻⁷ s × 40 step = 4 µs [카드 산술 · 가정 · §3-6] — 셈 정의 [미확인].
10. **시간 간격 범위**: *"time-steps of 10⁻⁶ to 10⁻⁷ s"* (p.468) ↔ 같은 MF 변수의 chen2004 식 Δt = πe√(m/2K1)/40 = 6.7 × 10⁻⁸ s (chen2004 카드 §3-2 [그 카드 산술]) — 범위 바로 아래 (자릿수 표현으로 읽힌다 [카드 추론]).
11. **그림 8 ≠ chen2004 그림 8** (같은 조건 · §3-3) — 추정기 · 평균 창 설명 없음.
12. **참고문헌 서지**: [10] *"O. Walton and R. Braun, Numerical simulation of inclined chute flows in monodisperse, inelastic, frictional spheres, Mech. Mater. 16, 239–246 (1993)"* ↔ 정본 `walton1993` 카드 = **단독 저자** O. R. Walton · 제목 *"… flows of monodisperse …"* · **239–247** / [1] *"T. Yokoyama, K. Uehara and M. Naito, The Angmill Mechanofusion system and its applications, Kona 5, 59–68 (1987)"* ↔ chen2004 의 같은 권 · 쪽 인용 [3] = *"Toh. Yokoyama, K. Urayama, Toy. Yokoyama, Kona 5 (1987) 59."* (공저자가 다름 · 어느 쪽이 맞는지 원 Kona 논문 [미확인]).
13. 글자: *"The sealed container is than placed"* (then) · *"principle body frame"* (principal) · 초록 낱말 붙음 (*"resultsillustratethe"*).

---

## 4. ★ 방법 — 모델 사슬 · 입자 처리 · 이 묶음의 네 질문 · 용어집

### 4-1. 모델 사슬
1. 문제 나누기: 세 길이 규모 (장치 · host · 게스트) → 장치 · host 규모 = 장치 DEM (host 만) · 게스트 규모 = 덩어리 하나의 충돌 DEM (Thornton 방식 · 미보고) (p.450–453 · p.468–469).
2. 장치마다 Walton 코드 고침: MF = 2D 단면 (편심 안쪽 원 · 긁개 고정 구 셋) / Hybridizer = 3D 축소 (날 = 겹친 구 셋 × 6 · 출구 → 재투입 · 공기 없음) / MAIC = 점 쌍극자 힘 · 토크 · 진동장 (식 1–6).
3. 처음 상태 = 임의 위치 · 작은 임의 속도 · 총 운동량 0 (p.452).
4. 진단: 등부피 고리 7 (MF · Hybridizer 운동 에너지) · 장시간 평균 고정 부품 힘 (MF) · 입자당 충돌 수 (Hybridizer · 1.0 s 시점) · 평균 충돌 속도 (Hybridizer) · 배치 그림 (MAIC).
5. 검증: 정성 서술 (MF 폴리스티렌 '선형' · Fn/Ft ≈5 · MAIC '잘 알려진 관찰').

### 4-2. ★ 입자 처리 (particle treatment)
- **구 · 단분산 · 한 종** (MF · Hybridizer = host 만 · MAIC = 자석만) — 게스트 0.
- **강체 구 + 소프트 구 접촉 (CONTACT 쪽의 탄소성)** — Walton 형 '소프트 구' 는 겹침으로 힘을 내는 접촉 법칙 (MF = 누름 강성 20,000 kg/s² · e 0.85) · **입자 모양 (SHAPE) 은 바뀌지 않는다** · 소성 · 막 · 파쇄 0.
- 경계 = 입자 (MF 긁개 = 고정 구 · Hybridizer 날 = 겹친 구 셋) — 우리 LIGGGHTS 의 메시 벽과 다르다.
- 자석 = 점 쌍극자 + 몸체 좌표 모멘트 (식 6) — 우리 덱에 없는 장거리 힘.

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
- **(i) DEM 의 한계 (말한 것)**: *"it is clear that by itself in its current form, DEM cannot provide a full picture of the dry coating process due to the severe computational burden created when guest particles are included in the simulation"* (p.469) · *"The major limiting factor in these simulations is the time-step for the numerical integration, which is a strong inverse function of the particle size"* · 게스트 1 µm · 200 nm → *"as small, or smaller than 10⁻⁹ s"* · *"simulating even a finite number of very small particles is still unrealistic"* (p.468) · *"the results are quite limited without the inclusion of guest particles, fluid effects, realistic device dimensions and operating conditions that very closely mimic the experiments"* (p.468) · Hybridizer 공기 없음 = *"conservative"* (p.461) · MF 2D = 계산량 때문 (p.455) · 반대 쪽: *"the particle stiffness does not significantly affect the kinematics of the system [1]"* (p.456 · 근거 인용 문제 §3-10).
- **(ii) 소성변형**: 왜 어려운지 논의 없음 · 우회 = 소프트 구 접촉 법칙 (*"elastic-plastic, frictional soft spheres"* 쪽 · p.452) · 맞춘 값 0 (e 0.85 · K1 20,000 = 고른 값) · 입자 모양 변화 0 · 게스트 막 = 범위 밖.
- **(iii) 2D ↔ 3D**: MF = 2D (*"so as to keep the computations to a reasonable value"* p.455) · Hybridizer = 3D (p.462) · 2D → 3D 전이에 대한 말 · 시험은 이 논문에 없음 (chen2004 의 3D 점검: 운동 세기 −4 – +2 % · 충돌 압력 +11 – +17 % — 그 카드 §3-3).
- **(iv) 탈압**: 해당 없음 (압밀 없음).

### 4-4. 기법 미니 용어집
- **건식 입자 코팅 (dry particle coating)**: 서브 µm 게스트를 µm host 에 용매 · 결합제 없이 기계적 힘 (충돌 · 압축 · 전단) 으로 붙이는 공정.
- **메카노퓨전 (Mechanofusion · MF)**: 회전 챔버의 원심으로 가루를 벽에 밀고 고정 안쪽 조각–벽 사이 좁은 틈에서 압축 · 전단 · 마찰 열로 입히는 Hosokawa 장치 · 고정 긁개가 벽 층을 긁는다.
- **Hybridizer**: 날 6 개 고속 회전자 (실험실 ≤16,000 rpm) 가 가루를 날 · 벽에 부딪치게 하고 기체가 순환관으로 다시 돌리는 Nara 장치 (고충격).
- **MAIC (magnetically assisted impaction coating)**: 진동 자기장 속 1–2 mm 자석이 돌고 부딪치며 host · 게스트를 유동화 · 미세 전단으로 덩어리를 푸는 장치 (이 논문이 든 실험 = Singh 등 [4] · Ramlakhan 등 [5]).
- **편차 (요동) 병진 운동 에너지 (deviatoric / fluctuational translational KE)**: 평균 흐름 속도를 뺀 속도 성분의 운동 에너지 밀도 (J/m³) — 입자 온도의 대리.
- **회전 운동 에너지 (챔버 강체 회전을 뺀)**: 벽에 붙어 챔버와 같이 도는 입자는 0 이 되게 만든 진단량 (MF 그림 7).
- **등부피 고리 (equal-volume annular zones)**: V_i = V/N · 고리 너비 ≥ 최대 입경 (한 입자가 두 고리까지만).
- **입자당 충돌 빈도 (collision frequency per particle)**: 누적 충돌 수 ÷ 입자 수 (Hybridizer 1.0 s 시점) — 셈 정의 [미확인].
- **점 쌍극자 (point dipole)**: 자석을 모멘트 m 하나로 — 힘 (m·∇)B · 토크 m × B · 쌍 힘 식 5.
- **덩어리 풀림 (agglomerate break-up)**: 게스트 덩어리가 host · 벽 · 두 면 사이에서 깨지는 정도 — 충돌 속도 ↑ · 게스트 표면 에너지 ↓ 일수록 커진다 (미보고 계산).

---

## 5. Figure set ★ (크롭 46 장 = `litdb/figures/dave2003_dry_coating_dem_mechanofusion_hybridizer_maic_three_devices/`)
| 그림 (크롭 파일) | 내용 | 우리 활용 |
|---|---|---|
| Fig. 1 (`fig_1.png` · 다시 자름) | MAIC 코팅 과정 SEM — (a) 코팅 전 PMMA · (b) 2.5 min · (c) 5 min · (d) 10 min · (e) 표면 확대 | 코팅 = 덩어리 → 분산의 시간 진행 (게스트 규모의 실험 그림) |
| Fig. 2 (`fig_2.png` · 다시 자름) | DEM 알고리즘 흐름도 | — |
| Fig. 3 (`fig_3.png` · 다시 자름) | MF 장치 그림 (챔버 벽 · 날 · 축 · 둥근 조각 · 회전) | 코팅 장치 기하 용어 |
| Fig. 4 (`fig_4.png` · 다시 자름) | MF 단순 기하 — 원 챔버 · 편심 안쪽 원 · 긁개 = 고정 구 셋 | 우리 드럼에 '안쪽 원통 + 긁개' 를 넣는 최소 기하 |
| Fig. 5 (`fig_5.png` · 다시 자름) | 등부피 고리 (점선 · 축척 아님 · Zone 1 · 2 · 7) | 칸 너비 ≥ 최대 입경 규칙 |
| Fig. 6 (`fig_6.png` · 다시 자름) | 긁개 없음 (왼쪽) · 있음 (오른쪽) 두 기하 | 긁개 유무 대조 설계 |
| Fig. 7 (`fig_7.png` · 다시 자름) | ★ 회전 운동 에너지 고리 분포 (a 있음 · b 없음 · t = 0–10 s) | 벽 고리의 '같이 돎' 판독 (챔버 ω 뺌) |
| Fig. 8 (`fig_8.png` · 다시 자름) | ★ 편차 병진 운동 에너지 고리 분포 (a 있음 · b 없음) | 1.98 배 · chen2004 그림 8 과 다른 값 |
| Fig. 9 (`fig_9.png` · 다시 자름) | ★ 안쪽 조각 힘 — (a) rpm (로그–로그 · 'Fn ~ w2') · (b) 채움 × rpm (범례 뒤바뀜) | rpm 지수 ≈2 · 포화 |
| Fig. 10 (`fig_10.png` · 다시 자름) | Hybridizer 장치 그림 (투입구 · 밸브 · 배출구 · 순환관 · 케이싱 · 날 · 회전자 · 고정자 · 재킷) | 고충격 장치 기하 |
| Fig. 11 (`fig_11.png` · 다시 자름) | Hybridizer 계산 모형 — 날 6 개 = 겹친 구 셋 · 출구 · 재투입 영역 | 순환 경로 대신 출구 → 재투입 경계 |
| Fig. 12 (`fig_12.png` · 다시 자름) | ★ 입자당 충돌 빈도 vs 채움 (10,000 rpm · 로그) | 경계 ≫ 입자끼리 (750–1700 배) |
| Fig. 13 (`fig_13.png` · 다시 자름) | ★ 입자당 충돌 빈도 vs rpm (1000 개 · 로그) | 입자끼리 ∝ rpm · 경계 ≈ 평평 |
| Fig. 14 (`fig_14.png` · 다시 자름) | 평균 충돌 속도 vs 채움 (10,000 rpm) | N^−0.25 ('반비례' 아님) |
| Fig. 15 (`fig_15.png` · 다시 자름) | ★ 평균 충돌 속도 vs rpm (1000 개) | ∝ rpm^1.01 · DEM → MPM 단일 충돌 속도 규모 |
| Fig. 16 (`fig_16.png` · 다시 자름) | Hybridizer 편차 병진 운동 에너지 고리 분포 (t = 0–10 s) | 바깥 고리 최대 468 J/m³ |
| Fig. 17 (`fig_17.png` · 다시 자름) | MAIC 장치 그림 (칼라 코일 · AC 전원 · 용기 확대: 게스트 · 자석 · host) | — |
| Fig. 18 (`fig_18.png` · 다시 자름) | 자석 100 개 · 장 0 → 사슬 | 쌍극자 DEM 검증 꼴 |
| Fig. 19 (`fig_19.png` · 다시 자름) | 정적 균일장 → 정렬 · 성긴 배치 | — |
| Fig. 20 (`fig_20.png` · 다시 자름) | 진동장 → 유동화 | — |
| 식 크롭 6 장 (`eq_01_…` – `eq_06_…`) | 식 1–6 (자기 힘 · 토크 · 진동 외부장 · 쌍극자 장 · 쌍극자–쌍극자 힘 · 모멘트 갱신) — 이 논문의 번호 식 전부 | 장거리 힘 DEM 의 최소 식 묶음 |
| 근거 문단 20 장 (`txt_p1_…` – `txt_p21_…`) | 초록 · 세 길이 규모 · 모델링 요구 · DEM 고르기 · 덩어리 방식 · MF 작동 · 긁개 모형 · 고리 · MF 변수 · 회전 KE · 편차 KE · 안쪽 조각 힘 · Hybridizer 장치 · 모형 · 빈도 · 충돌 속도 · MAIC 장치 · 결과 · 시간 간격 · 맺음 | 원문 인용용 (파일 이름의 pN = PDF 쪽) |

## 6. Post-processing ★
- **원문이 한 것**: 등부피 고리 부피 평균 (2 s) · 장시간 평균 안쪽 조각 힘 · 입자당 누적 충돌 수 (1.0 s 시점) · 평균 충돌 속도 · 시간별 고리 운동 에너지 (t = 0–10 s) · 자석 배치 그림.  반복 · 시드 · 오차 · 분포 (평균만) · 맞춤 · 계산 시간 (워크스테이션 '몇 시간' 만) 없음.
- **이 카드의 후처리**: 그림 7–9 · 12–16 은 PDF 안의 **1-bit 300 dpi 래스터** (벡터 아님) → 원 래스터를 꺼내 (xref 35–73) 격자선 · 눈금으로 축을 직선 맞춤 (로그 축은 자릿수 맞춤 · 잔차는 digitized.csv method 칸: 예 그림 7a 0.021 J/m³ · 그림 9a 0.0024 자릿수 · 그림 12 0.011 자릿수) → 굵은 선 · 점선을 지우는 열기 (9 × 9 · 그림 8a 는 13 × 13) · 점묘 회색 표지는 3 × 3 닫기 먼저 → 표지 무게중심 · 겹친 시간 계열은 덩어리 가운데 + 퍼짐 (112 행) → 교차 검산: 그림 7 ↔ chen2004 그림 7 (0.06 J/m³ 안) · 그림 9a ↔ chen2004 11a (0–3 %) · 그림 9b ↔ chen2004 12 (−8 – 0 %) · 그림 8 ↔ chen2004 8 (다름 0.51–0.78) → 카드 산술 (고리 평균 · 비 · 로그 기울기 · 질량 · 접촉 시간 · 1 % 겹침 속도 · 충돌 간격 · 겹침 · 우리 덱 겹침 · 강성 · Δt 배수 · 날 끝 속도 · 부피 비).  스크립트 = 이 묶음 scratchpad (끝난 뒤 지움) — 값 · 방법은 `digitized.csv` 의 method · note 칸에 남겼다.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 리포 문서 출처를 병기)

### 7-1. 비교표 (믹서 드럼 DEM ↔ 이 논문 세 장치)
| 항목 | 이 논문 | 우리 (믹서 B2-U 덱 · `chen2004` 카드 §7-1 이 옮긴 덱 값 + 리포 `docs/reviews/mixer_b2_u_development_20261122/README.md` · 읽기만) | 같음 / 다름 · 왜 |
|---|---|---|---|
| 코드 · 차원 | Walton 계열 자체 코드 · MF 2D · Hybridizer 3D · MAIC 3D 셀 | LIGGGHTS · 3D | — |
| 장치 · 운동 | 원심 MF (2000 rpm · 지름 [미확인] — chen2004 25 mm) · 날 충격 Hybridizer (5000–25,000 rpm) · 자기 진동 MAIC | 39 각형 드럼 R 12.58 mm · L 5.03 mm · 76.7 rpm · Fr 0.0827 · 중력 폭포 꼴 | 셋 다 우리와 다른 운동 체제 |
| 입자 | 한 종 단분산 400 µm (1200 · 2500 kg/m³) · 자석 100 | 3 상 parcel (CGF 151.4 · AM_P r 0.681 · AM_S 0.303 · SE 0.0757 mm · 4.85 / 1.64 g/cm³) · 100,000 계획 | 다상 · 다분산 · 점착 = 우리만 |
| 접촉 | Walton 소프트 구 (K1 20,000 kg/s² · e 0.85) · 쌍극자 (MAIC) | Hertz + 접선 이력 + SJKR 점착 (기하평균 W_ij = 2√(γ_iγ_j)) + 구름 마찰 · COR 0.3 | 우리 압밀 DEM (hooke/hysteresis) 이 Walton 계보 |
| 점착 | 없음 (값 0) | γ_AM/γ_SE **0.1** (비코팅 U) · **1** (코팅 C) · γ_W/γ_SE **0.00256** · Bo_SE **0.21244** (B1-U) · **21.244** (B2-U) | 우리 질문의 축 = 이 논문에 없음 |
| 게스트 | 없음 (≤10⁻⁹ s 장벽) | SE = parcel (CGF 151.4 · 실제 r 0.5 µm [카드 산술 0.0757 mm / 151.4]) · AM_P : SE 반지름 비 9.0 [카드 산술] | 우리 = 거친 입자 (coarse-graining) 로 돌아감 · host : 게스트 크기 차 1 자릿수 (원문 1–2 자릿수의 아래 끝) |
| 시간 간격 · 비용 | 10⁻⁶–10⁻⁷ s · '몇 초 = 몇 시간' (워크스테이션) | 2.373 × 10⁻⁷ s · B1-U 2 바퀴 **25 h 7 m 43 s** (리포 README) | 같은 자릿수 Δt |
| 판독 | 등부피 고리 (회전 · 편차 KE) · 입자당 충돌 (입자끼리 · 경계) · 평균 충돌 속도 · 고정 부품 힘 | Lacey M (16×16×4 · 12×12×3 · 8×8×2) · SE 군집 몫 · AM 접촉 SE | 서로의 빈칸 |
| 칸 규칙 | 고리 너비 ≥ 최대 입경 (p.455) | 16×16×4 축 방향 칸 1.26 mm ↔ AM_P parcel 지름 1.363 mm (`chen2004` 카드 §7-1 [우리 산술]) | 같은 규칙 · 판독기 배분 방식 [미확인] |

### 7-2. ★ 코팅 과정 DEM 구현 (1저자 11-23 Q3) — 장치 고르기 · 잴 양 · 구 DEM 의 끝 [카드 산술 · 추론]
| 장치 꼴 | 원문이 적은 모델링 요구 | 충돌 속도 규모 | 우리 B2-U 물성에서 SE–SE 겹침 [카드 산술: Hertz δ ∝ v^0.8 · 1 % = 1.17 m/s (`chen2004` 카드 §7-2)] | 1 % 계약을 지키려면 [카드 산술: δ ∝ (v²/E)^0.4 · Rayleigh Δt ∝ E^−½] | 비용 어림 | 판정 |
|---|---|---|---|---|---|---|
| 지금 드럼 (중력 · 76.7 rpm) | — | 벽 0.101 m/s | 0.14 % | 그대로 | B1-U 2 바퀴 25.13 h (리포 README) | 지금 계산 |
| **MF 꼴** (회전 챔버 + 고정 안쪽 원통 + 고정 긁개) | 긁개 필수 (*"cannot be ignored in modeling/analysis"* p.459) · 공기 없이 정성 일치 (p.452) | 법선 평균 0.285 m/s · 벽 2.62 m/s (`chen2004` 그림 16 판독 · 2000 rpm · 2D) | 평균 **0.32 %** · 벽 속도 1.9 % | 평균 = 그대로 · 벽 속도 꼬리만 계약 밖 (E 5.0 배면 1 %) | 2000 rpm 1 s ≈ **14 h** (`chen2004` 카드 §7-2 · 우리 덱 그대로 · 틈 1.6 mm = AM_P parcel 1.2 개) | ★ **가장 쌈** |
| Hybridizer 꼴 (날 6 + 순환) | 공기 항력 필수 (*"one must include the effect of the fluid … drag force"* p.452 · *"conservative"* p.461) · 3D · 날 · 순환 경로 | 평균 2.50–12.74 m/s (그림 15 · 축소 3D · 5000–25,000 rpm) · 실제 NHS-0 날 끝 62–99 m/s (10,000–16,000 rpm · `kawaguchi2018` 카드 L63 · [카드 산술]) | **1.8–6.8 %** | E **4.6–119 배** · Δt 0.47–0.09 배 (step 2.1–10.9 배) | MF 꼴 1 s 의 2.1–10.9 배 + 기체 결합 (CFD–DEM) [비용 미확인] · 실제 장치 부피 = 우리 드럼의 ≈240 배 (601 ↔ 2.5 cm³ [카드 산술 · NHS-0 125 mm × 49 mm]) | 비쌈 |
| MAIC 꼴 (자석 + 진동장) | 쌍극자 힘 · 토크 (식 1–6) · 진동장 · 자석 (1–2 mm) ≫ host | [미확인] | [미확인] | — | 새 힘 모델 | 우리 공정 아님 |

- ⇒ **고를 꼴 = MF 꼴** [카드 추론] — 근거 넷: ① 원문이 MF 만 '공기 없이' 정성 일치라고 적었다 (p.452) · Hybridizer 는 공기 필수 · MAIC 는 새 힘 ② 평균 충돌 속도가 우리 SE 강성의 1 % 겹침 계약 안 (0.32 %) ③ 챔버 지름이 우리 드럼과 같다 (25 ↔ 25.2 mm · `chen2004`) → 덱의 3 상 parcel · 점착 (SJKR · 기하평균) 을 그대로 두고 **고정 원통 + 긁개 입자만 더한다** ④ 정본의 실제 NCM–LPSCl 건식 코팅 장치가 이 꼴이다 (`kim2023` = Hosokawa AMS-Mini 메카노퓨전 · 헤드–벽 3 mm · 긁개–벽 ≈0.4 mm · 20 g · 2000 rpm 1 h = 안 입혀짐 → 5000 rpm 5 h = 고른 껍질 · 그 카드 L68 · L73–76 [다른 카드 값]).
- ⚠ **남는 문제**: 틈 1.6 mm = AM_P parcel 1.2 개 (CGF 151.4) → 틈 속 압축 · 전단이 parcel 하나 규모로 뭉개진다 (틈/AM_P 4 면 CGF 44.4 · 0.1 s ≈ 186 h — `chen2004` 카드 §7-2) · 게스트 (SE) 는 parcel — 이 논문이 넘지 못한 게스트 장벽 (≤ 10⁻⁹ s) 을 우리는 **거친 입자로 돌아가는 셈** 이고, parcel 이 게스트 수준 물리 (덩어리 풀림 · 붙음) 를 지키는지는 미검증 [카드 해석].
- **DEM 이 보일 수 있는 것 (잴 양)**: (a) 영역별 **입자당** 충돌 빈도 — 상 쌍별 (SE–AM · SE–SE · AM–AM · 입자–벽 · 입자–고정 부품) · 입자끼리 ↔ 경계 비 (MF ≈ 입자끼리 지배 · Hybridizer ≈ 경계 지배 §0-3) (b) 충돌 속도 · 에너지 **분포** (평균만이 아니라 꼬리 — 원문은 평균뿐) (c) 고정 부품 장시간 평균 힘 · 동력 (실험과 잇는 양 · rpm 지수 ≈2) (d) 벽 · 챔버와 같이 도는 입자 몫 (챔버 ω 를 뺀 회전 에너지 ≈ 0 인 입자) (e) SE parcel 이 AM parcel 에 붙어 있는 몫 (게스트 피복의 parcel 판) · SE 덩어리 크기 분포 (f) 덩어리 풀림 경우 셋 (host · 벽 · 두 면 사이) 의 빈도 — 원문의 셋 그대로.
- **구 DEM 이 못 보이는 것**: 막 형성 (SE 가 AM 위로 펴짐 · 소성 · 녹아 붙음) · 게스트 덩어리 속 풀림 · 열 — 원문도 *"DEM cannot provide a full picture … when guest particles are included"* (p.469) → **DEM (장치 · parcel 규모: 충돌 속도 분포 · 덩어리 풀림 경우의 빈도 · SE 부착 몫) → MPM 단일 충돌 (SE 덩어리 / 입자를 AM 표면에 · 분포에서 뽑은 대표 속도 · 원문의 경우 셋 = host 충돌 · 벽 충돌 · 두 면 사이 압축)** 로 넘긴다 [카드 추론] · 충돌 속도 크기 감각: MF 법선 0.07–0.42 m/s (`chen2004` 그림 16) · Hybridizer 평균 2.5–12.7 m/s (이 논문 그림 15) · `lee2026_mechanical_…` FEM 15 m/s (그 카드 L310 · 'RAM 60 G 에서 이 속도가 나오는 유도 없음') [다른 카드 값].

### 7-3. 랩 기준과 나란히
- 이 논문에 압밀 · 기공 · 진밀도가 없다 → 랩 표준 (순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³) 과 **나란히 놓을 숫자가 없다**.  host 밀도 1200 · 2500 kg/m³ = 랩 표준 SE 1.64 · 우리 덱 NCM 4.85 와 **다른 문헌 값** (재료 이름 없음 · 'magnesium 흉내').
- 편차 운동 에너지 (MF 22.6 · Hybridizer 129 J/m³ 고리 평균) 는 압밀 300 MPa (= 3 × 10⁸ J/m³) 의 10⁶–10⁷ 분의 1 [카드 산술] — 다른 양 (요동 운동 에너지 밀도) 이라 견주지 않는다.

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 코팅 장치 셋의 **기계 환경 (운동 에너지 · 충돌 빈도 · 충돌 속도 · 고정 부품 힘)** — DEM 쪽 (입자 · 접촉 · 영역 통계).
- **없는 것**: 게스트 · 점착 · 막 · 모양 변화 · 압밀 · 수송 · MPM ⇒ 우리 Ⓒ 코팅 활물질 믹싱에서 **'장치가 입자에 무엇을 하는가' 의 판독 틀** 과 **장치 고르기의 근거** 만 준다.  ★ 원문의 '세 길이 규모 + 나눠 풀기' (p.450–453) 와 '게스트 = 덩어리 하나의 충돌' (p.468–469) 은 우리 **DEM (장치 · parcel) → MPM (단일 충돌 · 막)** 나눔과 같은 생각이다 [카드 해석].

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문은 압밀 계획 바깥 (흐름 밖: Ⓒ 코팅 믹싱) 이다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (판정 기준 결과 전 등록) | ★ 흐름 밖 (Ⓒ 코팅 DEM): 결과 전에 고정할 판독 — 입자당 충돌 빈도를 **입자끼리 / 경계로 나눠** (Hybridizer 는 경계 ≫ 입자끼리 · 셈 정의를 먼저 적는다 — 원문은 정의가 없어 접촉 시간과 모순 §3-6) · 평균 충돌 속도 (어느 충돌의 평균인지) · 등부피 고리 (너비 ≥ 최대 입경) 의 편차 · 회전 운동 에너지 (챔버 강체 회전을 뺀) · 고정 부품 장시간 평균 힘 | 기공 연산자 · 압밀 판정 기준 없음 |
| **단계 1–6** (3D 메모리 · 2D MPM · 접촉 표현 · 순수 SE · 복합 압밀 · 탈압) | 없음 | — |
| **단계 7** (형상 · 피복 · 수송) | 없음 (그림 1 SEM = 코팅 진행의 실험 사진뿐) | 게스트 · 피복 정량 0 |
| **후보 D0** (지금 DEM) | Walton 소프트 구 = 우리 압밀 DEM (hooke/hysteresis) 과 같은 계보 · ★ **게스트 시간 간격 장벽 (≤ 10⁻⁹ s · p.468)** = 우리 믹서 덱이 SE 를 parcel (CGF 151.4) 로 다루는 이유의 문헌 근거 [카드 해석] · 강성 둔감 주장 (p.456) 은 근거 인용 문제 (§3-10) — ⚠ 우리 압밀에는 안 옮겨진다 (300 MPa 기공은 힘으로 정해지는 준정적 양 → 우리는 E_eff 1.35 GPa 를 실험 기공에 맞춤 · frame [2]) | 강성 · 겹침 실측 분포 없음 · 접촉 법칙 시험 없음 |
| **후보 C′** (항복 캡 탄소성 접촉) | 없음 — '소프트 구' 의 소성 쪽은 상호작용 범위 말뿐 (p.452) | 항복 · 캡 · 다접촉 0 |
| **후보 A′-0 · A · A′ · B · C · M0** | 없음 | — |
| **U0–U6** | 흐름 밖 판: **덩어리 하나의 충돌 셋** (host 충돌 · 평판 벽 충돌 · 두 평판 사이 압축 · p.468–469) = 우리 MPM 단일 충돌 (U3 · U5 의 Ⓒ 판) 의 경우 목록 · 기대 꼴 = 풀림 ∝ 충돌 속도 · 낮은 속도 = 되튐 · 두 면 사이 압축이 가장 많이 깸 (정성 · 미보고) | 해상도 · 수렴 시험 없음 |
| **R1–R7** | 없음 (R2 미끄럼 · 분리 = 접선 법칙 미기재 · R4 탈압 · R7 AM 파괴 없음) | — |
| **결과 전 대조 항목** (흐름 밖: Ⓒ 코팅 DEM) | ① MF 꼴: 고정 부품 힘 ∝ ω^≈2 (그림 9a 기울기 1.98 · 채움마다 2.08–2.51) · 긁개를 빼면 편차 KE ≈ 절반 · 벽 고리 회전 KE 떨어짐 ② Hybridizer 꼴: 평균 충돌 속도 ∝ rpm^1.01 · ∝ N^−0.25 · 입자끼리 빈도 ∝ rpm^0.97 · 경계 빈도 ≈ 평평 · 경계 / 입자끼리 370–1900 ③ 덩어리 풀림 ∝ 충돌 속도 · ∝ 1/γ_게스트 (정성) | 크기 · 문턱 전이 금지 (2D / 축소 3D · 무점착 · 단분산 · 공기 없음 · 강성 [미확인]) |

- **우리 DEM 과 견줄 자리**: 우리 18 배 연화 (24 → 1.35 GPa) 는 압밀 기공에 맞춘 **유효 탄성률** (재배열 · 입계 미끄럼을 뭉친 대리) · 이 논문의 무른 강성 (MF 20,000 kg/s²) 은 **계산 시간용** (운동학만 지킨다는 주장) — 같은 '무르게' 라도 정당화가 다르다 [카드 해석].
- **우리 MPM 과 견줄 자리**: 없음 · 다만 막 형성 (SE 가 AM 위에서 소성으로 펴짐) 을 MPM 단일 충돌 (E 1.53 · σ_y 0.30 · ν 0.49 = 압밀 보정값 · 충돌 속도 영역에서는 미검증) 로 볼 때 경계 조건 (충돌 속도) 의 크기 감각 — Hybridizer 꼴 평균 2.5–12.7 m/s (이 논문) · MF 꼴 법선 0.07–0.42 m/s (`chen2004`) [판독].
- **재료 · 차원 · 조건 차이**: 이름 없는 1.2 · 2.5 g/cm³ 단분산 구 (0.4 mm) · 자석 ↔ 우리 NCM · LPSCl parcel (실입경 1–9 µm · 점착 · 3 상) · 2D / 축소 3D ↔ 3D · 원심 · 고충격 · 자기 ↔ 중력 드럼 · 공기 · 열 없음 ↔ 진공 DEM.

## 9. 적용 인사이트 (행동)
1. **코팅 과정 DEM 의 첫 꼴 = MF 꼴 (드럼 덱 + 고정 원통 + 긁개 입자)** (흐름 밖: Ⓒ) — 결과 전 등록에 긁개 유무 대조 (편차 KE ≈2 배 · 벽 고리 회전 KE 떨어짐) 와 고정 부품 힘 rpm 지수 (≈2) 를 기대값으로 넣는다 (근거 §0-3 · §7-2).
2. **충돌 셈의 정의를 먼저 적는다** (단계 0) — 접촉 하나 = 충돌 하나 (시작 step 에서 셈) · 입자끼리 / 경계 · 상 쌍별.  이 논문의 입자–경계 10⁶ /s 는 접촉 시간 (MF 강성이면 5.9 µs) 과 안 맞아 정의 없이는 장치끼리 비교가 안 된다 (§3-6).
3. **게스트 수준은 덩어리 하나의 충돌 셋으로 나눠 MPM 단일 충돌 경우 목록으로** — host 충돌 · 벽 충돌 · 두 면 사이 압축 (원문 p.468–469) · 속도는 DEM 분포에서 뽑는다 (평균만 쓰지 않는다).
4. **Hybridizer 꼴은 먼저 겹침 계약 · 강성 · 공기를 정한다** — 평균 충돌 2.5–12.7 m/s 면 우리 SE 강성 (B2-U) 에서 겹침 1.8–6.8 % (1 % 계약 밖) · 지키려면 E 4.6–119 배 → Δt 0.47–0.09 배 · 원문도 공기 없는 결과를 *"conservative"* 라 했다.
5. **rpm 축 결과 전 기대 (단조 쪽)**: 충돌 속도 ∝ rpm · 입자끼리 빈도 ∝ rpm · 경계 빈도 ≈ 평평 · 고정 부품 힘 ∝ rpm² → 평균 충돌 에너지 ∝ rpm² [카드 산술 · 평균 속도²] — 최적은 이 단조 세기에 점착 쪽 손실 (벽 점착 · 덩어리 재형성) 이 맞서야 생긴다 (우리 논지 몫 · G3).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Early DEM studies of three dry particle coating devices — Mechanofusion (2-D, host particles only), the Hybridizer (scaled-down 3-D, without air) and magnetically assisted impaction coating (100 magnets, point-dipole forces) — computed device-level kinetic energies and host-level collision frequencies and impact velocities, but could not include guest particles because the time step would drop to ≤10⁻⁹ s (Dave et al., Adv. Powder Technol. 14 (2003) 449–470, p. 468)."
- "In the simulated Hybridizer, particle–boundary collisions outnumbered particle–particle collisions by about three orders of magnitude (~1 × 10⁶ vs ~1 × 10³ s⁻¹ per particle at 10,000 rpm), and the average impact velocity scaled linearly with rotor speed (2.5–12.7 m/s for 5,000–25,000 rpm) (Dave et al. 2003, Figs. 12–15; values digitized)."
- "Removing the scraper from a simulated Mechanofusion chamber halved the deviatoric kinetic energy because the wall layer co-rotated with the chamber (Dave et al. 2003, Figs. 7–8; ratio digitized)."
- "The authors noted that for realistic Hybridizer modelling 'one must include the effect of the fluid in the system and its drag force on the particles' (Dave et al. 2003, p. 452)."
- 국문: *"건식 코팅 장치 셋의 DEM 개관 (Dave 2003) 은 host 규모의 충돌 환경까지만 냈다 — 게스트는 시간 간격 (≤10⁻⁹ s) 때문에 넣지 못하고 덩어리 하나의 충돌 문제로 미뤘다."*
- 국문: *"Hybridizer 꼴 계산에서는 날 · 벽 충돌이 입자끼리 충돌보다 세 자릿수 많다 (Dave 2003 그림 12 판독) — 메카노퓨전 (입자끼리 지배) 과 응력 꼴이 다르다."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
**원문이 스스로 적은 한계**
1. 게스트 · 유체 · 실제 장치 치수 · 운전 조건이 없어 *"quite limited"* (p.468) · 시간 간격 장벽 (p.468) · DEM 만으로는 *"cannot provide a full picture"* (p.469).
2. MF 2D = 계산량 (p.455) · Hybridizer 공기 없음 = *"conservative"* (p.461) · MAIC = 자석만 · *"preliminary"* (p.465).
3. 빈도 · 접촉 힘 · 틈 · 입자 성질 의존은 *"will appear in a separate paper"* (p.459) · 덩어리 풀림 계산 *"not reported here"* (p.469).

**카드가 본 한계 · 원문 안 어긋남**
4. **점착 · 게스트 · 다분산 · 다상 · 막 · 열 = 범위 밖** — 우리 논지 (점착 대비) 와 코팅 결과는 직접 없다.
5. 장치끼리 공통 지표 없음 — 장치 비교는 카드 산술 (§0-3) 뿐 · '충돌' 셈 정의 없음 (접촉 시간과 모순 §3-6).
6. '선형' ↔ 'ω²' · 그림 9b 범례 뒤바뀜 · 그림 4 'inset' · 그림 13 입자–경계 감소 ↔ '증가' · '반비례' ↔ N^−0.25 · 계산 rpm 이 장치 최대를 넘음 · 'kinetic theory' 대조 안 보임 · 강성 둔감을 실험 논문 [1] 로 인용 · 그림 8 ≠ chen2004 그림 8 · 참고 [1] · [10] 서지 (§3-10).
7. 실험 대조 = 정성 서술 (그림 · 값 · 재료 · 장치 대조 없음) · 반복 · 시드 · 오차 · 분포 (평균만) 없음.
8. Hybridizer · MAIC 계산 상세 (치수 · 강성 · e · 마찰 · Δt · 축소 비 · B0 · f · 자석 크기) [미확인] — 재현 불가.
9. **절대값 전이 금지** — 장치 · 크기 · 재료 · 차원 · 강성 · 공기 모두 다르다; 옮길 것 = 응력 꼴 · 판독 틀 · 지수.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| [11] | K. D. Kafui and C. Thornton, Computer simulated impact of agglomerates, in: Powder & Grains '93, C. Thornton (Ed.), pp. 401–406. Balkema, Rotterdam (1993). | ★ 이 논문의 덩어리 풀림 모형이 바탕으로 삼은 접근 (*"based on the approach taken by Kafui et al. [11]"* · 덩어리 → 벽 충돌 DEM · p.453) — 우리 MPM 단일 충돌 경우 목록 · 점착 축 | 없음 |
| [5] | M. Ramlakhan, C.-Y. Wu, S. Watano, R. N. Dave and R. Pfeffer, Dry particle coating using Magnetically Assisted Impaction Coating (MAIC): modification of surface properties and optimization of system and operating parameters, Powder Technol. 112 (1-2), 137–148 (2000). | ★ 운전 변수 최적화 (G3 의 실험 쪽) | 없음 |
| [3] | M. Otani, M. Hironori, U. Tetsuya and S. Kunio, Mechanism of particle shape modification by dry impact blending, Advanced Powder Technol. 7 (4), 291–303 (1996). | Hybridizer 충격으로 입자 모양이 바뀌는 기전 (막 · 소성 쪽) | 없음 |
| [2] | H. Honda, K. Ono, T. Ishizaka, T. Matsuno, T. Katano and M. Koishi, Surface modification of powders by the high speed impact method, J. Soc. Powder Technol., Japan 24, 593–599 (1987). | Hybridizer 실험 (제목 = 고속 충격법 · 장치 치수 · 운전 창) | 없음 |
| [4] | R. K. Singh, A. Ata, J. Fitz-Gerald and Y. I. Rabinovich, Dry coating method using magnetically assisted impaction in a randomly turbulent fluidized bed, Kona 15, 121–131 (1997). | MAIC 실험 (이 논문이 MAIC 실험으로 처음 든 문헌) | 없음 |
| [12] | G. Lian, C. Thornton and M. J. Adams, A microscopic simulation of oblique collisions of 'wet' agglomerates, in: Powder & Grains '97, R. P. Behringer and J. T. Jenkins (Eds), pp. 159–162. Balkema, Rotterdam (1997). | 젖은 덩어리 쌍 충돌 DEM (액교 점착) | 없음 |
| [1] | T. Yokoyama, K. Uehara and M. Naito, The Angmill Mechanofusion system and its applications, Kona 5, 59–68 (1987). | MF 실험 (폴리스티렌 힘 vs rpm) — chen2004 의 같은 권 · 쪽 인용과 공저자가 다름 (§3-10) | 없음 (wishlist L744 = chen2004 판 서지) |
| [7] | J. Chen and C. C. Huang, A preliminary model for Mechanofusion powder processing, Kona 15, 113–120 (1997). | MF 해석 모형 (유체역학 바탕) | 없음 (wishlist L745) |
| [6] | R. Pfeffer, R. N. Dave, D. Wei and M. Ramlakhan, Synthesis of engineered particulates with tailored properties using dry particle coating, Powder Technol. 117, 40–67 (2001). | 같은 그룹 총설 | `pfeffer2001_dry_particle_coating_engineered_particulates` |
| [10] | O. Walton and R. Braun, Numerical simulation of inclined chute flows in monodisperse, inelastic, frictional spheres, Mech. Mater. 16, 239–246 (1993). | 접촉 법칙 · 코드 계보 (서지가 정본과 다름 §3-10) | `walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem` |
| [9] | O. Walton and R. Braun, Viscosity and temperature calculations for shearing assemblies of inelastic, frictional disks, J. Rheol. 30 (5), 949–980 (1986). | 접촉 법칙 원전 | **제외** (내려받기 불가 · `status.tsv` N-72) |
| [8] | P. A. Cundall and O. D. L. Strack, A discrete numerical model for granular assemblies, Geotechnique 29, 47–65 (1979). | DEM 원전 | 없음 (wishlist 에 이미 있음) |

## 13. [미확인] 목록 (원문 22 쪽 전수에 없음)
1. MF: 챔버 · 안쪽 조각 지름 · 마찰 · 접선 법칙 · Δt · 코드 이름 · 계산 시간 (chen2004 에 일부 있음).
2. Hybridizer: 챔버 · 회전자 · 날 치수 · 축소 비 · 채움 비 값 · 강성 · e · 마찰 · Δt · 계산 시간 · '충돌' 셈 정의 · '평균 충돌 속도' 의 대상.
3. MAIC: 자석 크기 · 모멘트 · B0 · f · 셀 크기 · 접촉 물성 · 차원 서술.
4. 덩어리 풀림 계산의 값 · 그림 · 모형 (*"not reported here"*).
5. 실험 대조의 값 · 그림 (MF 폴리스티렌 · MAIC 관찰) · 'kinetic theory' 대조.
6. 그림 8 이 chen2004 그림 8 과 다른 이유 (추정기 · 평균 창).
7. 참고 [1] 의 공저자 (Uehara · Naito ↔ chen2004 의 Urayama · Yokoyama) · [10] 의 저자 · 제목 · 끝 쪽.
8. 우리 쪽: MF 꼴 · Hybridizer 꼴 계산의 실제 비용 (§7-2 는 비례 어림) · 판독기의 칸 배분 방식.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-24)
- 서지: 후보 표 N-156 · 지시서 메모 (R. Dave · W. Chen · A. Mujumdar · W. Wang · R. Pfeffer · 제목 · Adv. Powder Technol. 14 (4) (2003) 449–470) = 원문 첫 쪽 · 머리글과 같음 · **DOI 는 22 쪽 글자 층 전수에 없음** (PDF 메타데이터 XMP 의 doi:10.1163/156855203769710672 = 메모와 같음) · 날짜 둘 · 키워드 6 · 교신 이메일 · 연구비 둘 · SI 안내 없음.
- 숫자: 글자 층 + 400 dpi 렌더로 대조 — 1–2 orders · 1500 · 1.6 mm · 400 µm · 1200 kg/m³ · 0.85 · 20 000 kg/s² · 2000 r.p.m. · 10 s · 2 s · seven zones · about 2 times · around 5 · 16 000 r.p.m. · six rotor blades · three overlapping spheres · 400-µm · 2500 kg/m³ · 1.0 s · 10 000 r.p.m. · 1.0 × 10⁶ · 1–2 mm · 100 magnetic particles · 1 µm · 200 nm · 10⁻⁹ s · 10⁻⁶ to 10⁻⁷ s · 150 µm · 2.5 · 5 · 10 min · 식 1–6.
- 그림: 그림 7–9 · 12–16 = 1-bit 300 dpi 래스터 → 원 래스터 좌표 판독 (112 행) · 교차 검산 (그림 7 · 9a · 9b ↔ chen2004 그림 7 · 11a · 12 = 같은 자료 · 그림 8 ↔ chen2004 그림 8 = 다른 값) · 그림 1–6 · 10 · 11 · 17–20 은 그림 관찰.
- 크롭 46 장 전부 열어 확인 (도구 20 장 → 전부 손으로 다시 자름: 도구 크롭이 글 폭 전체로 여백이 고르지 않음 · 그림 17 캡션에 다음 문단이 섞임 · 그림 17 의 'host particle' 이름표가 가장자리 / 식 6 장 = 식 번호별로 손으로 자름 (400 dpi) / 근거 문단 20 · 한 장 (`txt_p6_mf_…`) 은 문장 경계에서 시작하게 앞 낱말 'ber.' 를 흰색으로 가림).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 + 'dry particle coating processes' · '156855203769710672' · 'Mujumdar' · 'Adv. Powder Technol. 14' grep — 카드 없음 · 인용한 카드도 없음 (2026-11-24) · 같은 저자 · 같은 해 다른 카드 없음 (같은 그룹 짝 = `chen2004` · 2004).

## 🔗 관련 카드
- 같은 그룹 · 같은 계산: `chen2004_mechanofusion_dry_coating_dem_2d_host_scraper_inner_piece_collision_frequency` (MF 전체 판 · 그림 7 · 9 같은 자료 · 그림 8 다른 값 · 빈도 표) · `pfeffer2001_dry_particle_coating_engineered_particulates` (같은 그룹 총설 · ref [6] · MF 2D DEM 과 MAIC DEM (자석 + host) 이 먼저 실림 · NJIT Hybridizer Mg 실험) · `walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem` (ref [10] · 코드 계보 · 깊은 흐름은 강성에 민감).
- 같은 장치 꼴의 SE 코팅 실험 · DEM: `kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact` (MF 꼴 · LPSCl → NCM811) · `kawaguchi2017_dry_coating_parametric_na2so4_model_se` · `kawaguchi2018_dry_coating_model_se_particle_powtec` (Hybridizer NHS-0 · 날 끝 속도 창) · `kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable` (고강도 믹서 + DEM · SI ∝ n^1.76) · `lee2026_mechanical_halogen_argyrodite_drycoating` (우리 랩 · RAM · FEM 단일 충돌 15 m/s).
- 드럼 · 점착 이웃: `chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed` (Walton–Braun + 점착 드럼 DEM) · `mellmann2001_transverse_bed_motion_rotating_cylinders_slumping_rolling_cascading_froude` (드럼 운동 꼴 — MF 는 원심 꼴 쪽).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
