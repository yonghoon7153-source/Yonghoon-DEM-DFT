<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 본 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md · 같은 부류 이웃 = ai2011_rolling_resistance_contact_models_dem.md
     (이 논문이 모델 분류 A–D 와 '모델 C 가 낫다' 를 그대로 가져온 ref [12]).
     쪽 표기 = 학술지 쪽 p.409–417 (= PDF p.1–9 · p.409 = PDF p.1).  보충 자료 (SI) 안내 없음 (9 쪽 본문 · 'supplementary' 0 회).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독 · 벡터] = 벡터 그림 (Fig 8 · 9) 의 경로 좌표를 눈금선 · 눈금 글자로 보정해 읽은 값
     (재현 = litdb/figures/<slug>/digitized.csv · 보정 잔차 x ≤ 0.0007 · y ≤ 0.022°) · [판독 · 래스터] = 원 래스터 (Fig 2 · 6, ≈200 dpi) 를 틀 · 격자선으로
     보정해 읽은 값 · [판독 · 눈] = 크롭을 눈으로 읽은 값 · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 재계산] = 원문 식 · 절차를
     그대로 코드로 다시 돌린 값 (scratch · 저장 안 함) · [카드 추론] · [추정] = 이 카드의 해석 · [미확인] = 원문 (9 쪽 전수) 에 없음.
     원문 9 쪽은 텍스트 층 전수 + 그림 · 식 · 근거 문단 크롭 52 장을 직접 열어 읽었다. -->
# 구름마찰로 입자 모양을 대리하는 기법의 정량 점검 (DEM) — 접촉 편심으로 μ_r 를 추정 (μ_r ≈ ⟨e⟩/R_r · 식 9) 하고 PFC3D 안식각 150 런 (구 + 모델 C 구름마찰 ↔ 이중 · 삼중 점묶음) 으로 견줌 → 같은 안식각에 드는 구름마찰은 추정의 ≈절반 (구 μ_r 0.18 줄 0.35–0.59 배 [카드 산술]) · 구 + 구름마찰이 최대 ≈10° 높다 · 안식각 하나로는 (μ_p, μ_r) 를 못 정한다 · 실험 · 압밀 · 소성 · 탈압 없음 — Wensrich · Katterfeld (Powder Technol. 2012)

> slug `wensrich2012_rolling_friction_shape_contact_eccentricity_dem` · DOI `10.1016/j.powtec.2011.10.057` · type `DEM 이론 + DEM 수치 비교 (PFC3D 3D · 안식각 150 런 · 구름 저항 모델 C = 탄소성 스프링–대시포트 구름 토크 ↔ 이중 · 삼중 점묶음 · 단일 입자 굴림 시험 · 접촉 편심 → μ_r 해석 · 몬테카를로) — 실험 · 압밀 · 입자 소성 · 탈압 없음` · PDF `c81b04fd-50._Rolling_friction_as_a_technique_for_modelling_particle_shape_in_DEM.pdf` · digested `2026-11-13` · status ✅
>
> **저자**: **C.M. Wensrich\*** (교신 · christopher.wensrich@newcastle.edu.au · School of Engineering, University of Newcastle, Australia) · **A. Katterfeld** (Institut für Logistik und Materialflusstechnik, Otto-von-Guericke Universität, Magdeburg, Germany) — *Powder Technology* **217** (2012) 409–417 · 접수 2011-06-09 · 수정 2011-10-26 · 승인 2011-10-28 · 온라인 2011-11-06 · 키워드 Discrete element modelling · Rolling friction · Rolling stiffness · Particle shape · Contact eccentricity · DEM calibration (p.409).  연구비 · 기여 표기 없음.
> **이웃 카드 (링크만)**: [`ai2011_rolling_resistance_contact_models_dem`](ai2011_rolling_resistance_contact_models_dem.md) (이 논문 ref [12] — 모델 A–D 분류 · 'C 가 낫다' 의 출처 · 2D) · [`roessler2019_dem_cohesive_aor_cylinder_lift_calibration`](roessler2019_dem_cohesive_aor_cylinder_lift_calibration.md) (이 논문을 구름마찰 모델 출처로 인용 · 후보 표 근거 카드) · [`coetzee2017_dem_calibration_review`](coetzee2017_dem_calibration_review.md) (ref [84] 로 인용) · [`luding2008_cohesive_frictional_contact_models`](luding2008_cohesive_frictional_contact_models.md) (우리 압축 덱 μ_r 표기) · [`hare2026_dem_pept_dry_mixing_nmc622_eirich`](hare2026_dem_pept_dry_mixing_nmc622_eirich.md) (μ_r 0.075 = '비구형성 대리').
> **판독 원자료**: `litdb/figures/wensrich2012_rolling_friction_shape_contact_eccentricity_dem/digitized.csv` (357 행 — Fig 9 원자료 150 점 [벡터] · Fig 8 곡선 꼭짓점 162 [벡터] · Fig 6 36 [래스터] · Fig 2 9 [래스터]) · 크롭 52 장 (그림 9 + 패널 5 + 표 2 + 식 16 + 근거 문단 20 — 도구 크롭 10 장 전부 다시 자름 · 손 크롭 42) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: DEM 은 입자를 구로 이상화하고 모양은 *"computationally expensive"* 라 그 효과를 **구름마찰 (접촉마다 회전을 막는 토크)** 로 대리하는데, 이 논문은 그 계수를 **접촉 편심의 평균 ÷ 굴림 반지름 (μ_r ≈ ⟨e⟩/R_r)** 으로 추정하는 기하 규칙을 세우고 (회전 타원체 · 점묶음에 대해 계산), PFC3D 안식각 시험 150 런 (지름 4.6–5.2 mm · 7000 입자 · 원통 인양) 으로 **같은 '등가' μ_r 의 점묶음 ↔ 구 + 모델 C 구름마찰** 을 견주어 — 정성적으로는 닮았지만 **구 + 구름마찰이 안식각을 최대 ≈10° 더 높게 내고 (같은 안식각에 드는 구름마찰은 추정의 ≈절반)**, 그 까닭을 *"shape can cause rotation as well as resist it, while rolling friction always acts to oppose rolling"* 으로 본다.  덧붙여 **안식각 한 값은 (μ_p, μ_r) 의 넓은 범위가 같이 낸다 → 관측량 하나로 보정할 수 없다** 고 적는다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① DEM 의 한계 (질문 k) | *"Practically this means scaling of particle size and stiffness, and idealisation in the form of spheres and simplified contact mechanics"* (p.409) · *"Shape is an expensive thing to model in DEM, and so rolling friction is typically used"* (p.409) · *"there is currently no physical reasoning that is applied in the selection of a value for rolling friction, rather it tends to be treated as a parameter to be 'tuned'"* (p.410) · *"Without any physical basis, the coefficient can only ever be considered a 'tuneable parameter'"* (p.416) | [인쇄] |
| ② 구름마찰 대리의 크기 | 같은 '등가' μ_r (0.18–0.59) · 같은 μ_p (0.2–0.8) 에서 구 + 구름마찰 − 점묶음 = **이중 6.3–10.9° · 삼중 4.1–10.0°** (칸 평균 25 칸) · 같은 안식각을 내는 구의 μ_r ÷ 점묶음 등가 μ_r = **0.35–0.59** (구 μ_r 0.18 줄 8 칸 · 나머지 줄은 점묶음 범위 밖) | [판독 · 벡터 · 카드 산술] Fig 9 · §3-6 · §3-7 |
| ③ 원문 수치 문장 | *"up to 10° higher"* · *"by at least a factor of two"* · *"approximately half as much rolling friction"* (p.416) · 이중 ↔ 삼중 *"around 2°"* (p.416) · 정착 더미의 '관측' 편심 = 추정보다 *"approximately 10% higher"* (p.416) | [인쇄] |
| ④ 소성 · 큰 변형 (질문 l) | **말 없음** — *"plasticity"* 1 회 (접촉 이력 근원 목록 · p.409) · 모델 C 의 *"elastic–plastic"* = **구름 토크의 스프링 + 한계 미끄럼** (입자 소성 아님) · 입자는 고정 모양 (구 · 겹친 구 묶음) | [인쇄] p.409 · p.410 |
| ⑤ 압밀 · 기공 · 압력 · 탈압 | **없음** — compaction · porosity · pressure · unload 0 회 · 중력 안식각뿐.  정지 쪽 경고 하나: 모델 A (우리 `cdt` 꼴) 는 정지 계에서 *"creeping"* (p.410) · 예비 런에서 5 s 뒤에도 *"still in the process of settling"* (p.414) — 수치 없음 | [인쇄] |
| ⑥ 2D ↔ 3D | 계산은 **3D** (PFC3D) · 편심 해석은 2D 타원에서 시작해 *"develop this further into three dimensions by averaging the calculated eccentricity over the surface of revolution"* (p.412) — 이 카드 재계산: 같은 AR 3 에서 2D 둘레 평균 ÷ ∛(AR) 0.830 ↔ 3D 표면 평균 0.752 (prolate) · 0.708 (oblate) | [인쇄] · [카드 재계산] §3-4 |
| ⑦ 실험 대조 | **없음** — 'experiment' 0 회.  '모양의 정답' 은 **DEM 점묶음 (겹친 구 2 · 3 개)** 자신이다 | [인쇄] p.414 |
| ⑧ 우리 단위 시험에 쓸 꼴 | 단일 입자 굴림 (Fig 2): 정지 토크 고원 ≈0.756 μN·m [판독 · 래스터] = μ_r R m g 0.751 [카드 산술 · ρ 2000 가정] · 감속 ≈528 rad/s² [판독] ↔ μ_r g/(1.4R) 539 · 봉우리 ω 40.4 rad/s [판독] ↔ (5/7)v₀/R 41.2 · 굴림 진동 주기 ≈120 ms [판독 · 눈] ↔ 2π√(1.4mR²/k_r) 121 ms | §3-3 |

⛔ **한정어 (떼지 말 것)**: ① 입자 = **지름 4.6–5.2 mm** · G 10 MPa (E 26 MPa [카드 산술]) · ρ 2000 kg/m³ · **중력 안식각** (7000 입자 · 원통 Ø91 mm) — 우리 µm · 300 MPa 압밀과 무관한 체제 ② '모양' = **겹친 구 묶음** (이중 · 삼중 · 같은 지름) — 실물 입자 · 실험 없음 ③ 구름마찰 = **모델 C (탄소성 스프링–대시포트 구름 토크 · PFC3D UDM)** · k_r = R_r² k_s · 구름 감쇠 없음 — 우리 덱 `rolling_friction cdt` (모델 A 꼴 · 정본 카드 표기) 와 **다른 모델** ④ 반복 2 런 · 칸마다 산포 평균 0.6–1.0° · 최대 2.5° [판독 · 벡터] ⑤ '절반' 은 **구 μ_r 0.18 줄에서만** 보간으로 확인된다 (§3-7) ⑥ 회전 타원체 μ_r 추정 (Fig 6) 은 DEM 으로 시험하지 않았다 (*"so-far entirely untested"* · p.413) — 그리고 그 그림의 oblate 선은 원문 식 재계산과 어긋난다 (§11).
⇒ **절대값 전이**: **전이할 숫자가 없다** (5 mm 중력 더미의 안식각 · μ_r).  옮길 수 있는 것은 **방법 · 규칙 · 함정** — (a) 구름마찰 계수는 모양에서 온 값이 아니면 조율 매개변수다 (b) 기하 추정 μ_r ≈ ⟨e⟩/R_r 은 AOR 기준으로 ≈2 배 과대 (c) 관측량 하나로 매개변수 둘을 정하지 않는다 (d) 모델 A 꼴 구름 토크의 정지 계 기어감 (e) 반복 런 산포.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-50 의 '왜' 칸)

의도 원문: *"k — "구름마찰 모델 (이 논문 DEM) — 카드 없음" · 제목 = 구름마찰로 입자 모양을 모델링 → 구 DEM 이 모양을 담지 못해 대리하는 방법 (N-19 Ai 2011 과 같은 부류 (종합 · 조수 판단))"* · 근거 = `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` L244.

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| (k) "구름마찰 모델 (이 논문 DEM)" — roessler2019 의 구름마찰 모델 출처 | **채움 (단서)** | 이 논문의 DEM 은 **모델 C** (탄소성 스프링–대시포트 구름 토크) 를 PFC3D 4.00-187 의 C++ UDM 으로 구현 (p.414) · 구름 강성 **k_r = R_r² k_s** (식 7 · Iwashita & Oda 와 같은 선택) · **구름 감쇠 없음** 이 *"the ideal case"* (p.411).  모델 C 자체의 출처는 Iwashita & Oda [14] · Ai et al. [12] (p.410) — 이 논문이 만든 모델이 아니라 **강성 · 감쇠 설정을 바꾼 판** [카드 추론] (roessler2019 L87 의 '수정 탄소성 스프링–대시포트' 표기와 맞다).  LIGGGHTS 는 0 회 — LIGGGHTS 의 EPSD 계열이 이 설정과 같은지 [미확인] |
| "제목 = 구름마찰로 입자 모양을 모델링" | **채움** | 제목 그대로 · 초록 첫 문장 *"Shape is a computationally expensive property to model in DEM, and so rolling friction is often employed in order to simulate its effects. However, the precise way in which rolling friction models shape has never been properly outlined."* (p.409) |
| "구 DEM 이 모양을 담지 못해 대리하는 방법" | **채움 (+ 크기까지)** | 구 이상화 (*"idealisation in the form of spheres and simplified contact mechanics"* p.409) · 모양은 비싸서 구름마찰로 대리 (p.409) · 대리의 정량 한계: 구 + 구름마찰 − 점묶음 = 4.1–10.9° (칸 평균) · 같은 안식각에 드는 μ_r = 추정의 0.35–0.59 배 [판독 · 벡터 · 카드 산술] · 기전 차: 모양은 회전을 *"create or encourage"* 하기도 함 (p.412).  ⚠ 원문은 '담지 못함' 이 아니라 **'비싸다'** 로 쓴다 — 점묶음 (EDEM · PFC3D) 으로 모양을 담을 수 있다 (p.413) |
| "(N-19 Ai 2011 과 같은 부류)" | **채움** | 같은 부류 (구름 저항 모델).  이 논문은 Ai [12] 의 네 부류 (A 일정 토크 · B 점성 · C 탄소성 스프링–대시포트 · D 접촉 무관) 를 그대로 쓰고 (p.409–410) · 'C 가 정지 계에서 낫다' 를 3D 더미로 다시 확인 (모델 A 더미가 5 s 뒤에도 정착 중 · p.414).  다른 점: Ai = **2D** 원판 · 모델 거동 / 이 논문 = **3D** · 모양 ↔ 구름마찰의 등가성 |
| 질문 k — DEM 한계 문장 | **채움** (문장) · **말 없음** (압밀 · 밀도 · 겹침 상한 · 소성) | §4-4 (i) 의 원문 문장 9 개 · 압밀 · 겹침 · 상대밀도 · 변형률 상한 · 입자 소성은 다루지 않는다 |
| 가리킨 카드의 **2 차 인용 값** | **해당 없음 (숫자 없음)** · 귀속 문장은 **같음** | roessler2019 L87 (*"수정 탄소성 스프링–대시포트 (Wensrich & Katterfeld 2012)"*) · L144 (*"EPSD 구름마찰 — 구름 저항을 탄소성 스프링–대시포트로 모델 (Wensrich & Katterfeld)"*) · L191 (*"구름마찰 = 탄소성 스프링–대시포트 (Wensrich–Katterfeld)"*) · L49 (*"구름마찰로 모양 대리"*) · L244 (서지 *"Wensrich, C. M., & Katterfeld, A. (2012). Rolling friction as a technique for modelling particle shape in DEM. Powder Technology, 217, 409–417."*) — 원문 첫 쪽 서지 (제목 · 학술지 · 권 · 쪽 · 연도) 와 같고 모델 귀속도 원문과 맞다 (EPSD 원형은 Iwashita & Oda · Ai 라는 단서만 빠짐) |
| (덧붙임) 다른 카드의 2 차 인용 | **같음 (뜻)** | `coetzee2017_dem_calibration_review` L162–163 따옴표 *"there is no physical reasoning for choosing a value for rolling friction other than tuning the bulk behaviour to be more realistic"* = 리뷰 (Coetzee) 의 풀어쓰기 — 원문 낱말은 p.410 *"there is currently no physical reasoning that is applied in the selection of a value for rolling friction, rather it tends to be treated as a parameter to be 'tuned' in an effort to produce realistic behaviour"* (뜻 같음) · L611 *"낮은 sliding 에서 안식각은 rolling 변화에 둔감, 역도 성립"* = p.415 *"if particle friction is small relative to rolling friction … relatively insensitive to further increases in rolling friction, and vice-versa"* (같음) · L50 *"plastic … Wensrich & Katterfeld 의 rolling 손실 열거"* = p.409 의 접촉 이력 목록 (같음) |

⇒ **의도 대조 결과: 채움** — 구름마찰 = 모양 대리라는 진술 · 그 대리가 모양과 같지 않다는 수치 (최대 ≈10° · ≈2 배) · '조율 매개변수' 고백이 원문에 있다.  압밀 · 소성 · 밀도 · 탈압은 다루지 않는다 (흐름 밖).

---

## 1. 한 줄 요약
DEM 에서 모양은 비싸서 구름마찰로 흉내 내지만 그 값을 고를 물리 근거가 없다는 문제 (p.410) 에서 출발해, 비구형 입자의 법선력이 중심을 비켜 지나며 만드는 토크 e·F_n 을 구름마찰 토크 상한 μ_r R_r F_n 에 맞대어 **μ_r ≈ ⟨e⟩/R_r** (식 9) 을 제안하고, 회전 타원체 (해석 적분 · Fig 6) 와 겹친 구 묶음 (몬테카를로 · Fig 8 · 표 2) 의 μ_r 를 계산한 뒤, PFC3D 안식각 150 런으로 **점묶음 ↔ 같은 '등가' μ_r 의 구 + 모델 C 구름마찰** 을 견준다 — 등고선 모양 (미끄럼 · 구름 두 기전이 함께여야 큰 안식각) 은 닮았지만 구 + 구름마찰이 최대 ≈10° 높아 같은 안식각에 드는 구름마찰은 추정의 절반쯤이고, 원인은 모양이 회전을 돕기도 하는데 구름마찰은 늘 막는 데 있다고 본다.  부수 결과: 이중 ↔ 삼중 점묶음은 정규화 편심으로 보면 ≈2° 안에서 겹친다 · 안식각 하나로는 매개변수를 고를 수 없다 · 반복 런이 꼭 필요하다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| C.M. Wensrich\* (Univ. Newcastle) · A. Katterfeld (OVGU Magdeburg) | Powder Technol. 217 (2012) 409–417 · 9 쪽 | 10.1016/j.powtec.2011.10.057 | **일반 입상체 모형** — 지름 4.6–5.2 mm 구 (균일 분포) · G 10 MPa · ν 0.3 · ρ 2000 kg/m³ · 겹친 구 묶음 (이중 · 정삼각 삼중) — 실제 재료 이름 없음 · SE · AM 없음 | DEM 이론 (편심 → μ_r 해석 · 몬테카를로) + DEM 수치 (PFC3D 3D · 안식각 150 런 · 단일 입자 굴림 시험) — 실험 0 |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 안식각 계산 조건 (표 1 · 표 2 · p.414–416)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 코드 | PFC3D 4.00-187 (64 bit · Itasca) · 모델 C 구름마찰 = C++ User Defined Model (UDM) · MS Visual C++ DLL | [인쇄] p.414 |
| 입자 | 지름 **4.6–5.2 mm** · 분포 Uniform · 접촉 **Hertz–Mindlin (no-tension)** · ρ **2000 kg/m³** · G **1e7 Pa** · ν **0.3** · 점성 감쇠비 법선 0.8 · 전단 0.8 · 국소 감쇠 0 | [인쇄] 표 1 |
| 영률 | E = 2G(1 + ν) = **26 MPa** | [카드 산술] |
| 입자 수 · 용기 | **7000** 입자 · 연직 원통 **Ø91 mm × 136.5 mm** (높이 = 1.5 × 지름 [카드 산술]) · 원통 지름 ≈ 입자 지름의 18.6 배 [카드 산술 · 4.9 mm 기준] | [인쇄] p.414 |
| 점묶음 생성 | 맞는 지름의 구를 먼저 만들고 **같은 부피의 무작위 방향 점묶음** 으로 하나씩 바꿈 | [인쇄] p.414 |
| 절차 | 중력으로 **1 s** 정착 → 원통을 **16 mm/s** 로 올림 → 올리기 시작한 뒤 **5 s** 까지 → 더미 분석 | [인쇄] p.414 |
| 안식각 판정 | 더미를 **36 쐐기** 로 나눔 · 둥근 꼭대기 · 납작한 발치를 피하려 안쪽 · 바깥 끝을 버림 (버리는 몫 [미확인]) · 나머지를 **10 반지름 칸** · 칸마다 가장 높은 입자 · 선형 회귀 직선 · 쐐기 각을 평균 | [인쇄] p.414 |
| 매개변수 격자 | μ_p ∈ {0.2, 0.3, 0.4, 0.6, 0.8} × μ_r ∈ {0.18, 0.28, 0.38, 0.49, 0.59} ↔ δ (이중 0.49 · 0.79 · 1.10 · 1.45 · 1.76 / 삼중 0.50 · 0.82 · 1.13 · 1.46 · 1.78) | [인쇄] 표 2 |
| 벽 마찰 | μ_p 와 0.5 중 **작은 값** (μ_p 0.6 · 0.8 이면 0.5) | [인쇄] p.414 |
| 시간 간격 | 소프트웨어 임계 Δt 의 **25 %** · 보통 **3–4 μs** | [인쇄] p.414 |
| 런 수 | **150** = 구름마찰 50 + 이중 50 + 삼중 50 · 칸마다 **2 번** (다른 처음 충전) | [인쇄] p.414 |
| 정착 확인 | 모델 C 런: 5 s 끝 잔류 속도 *"well below 10⁻⁷ m/s"* · 예비 모델 A 런: 5 s 끝에도 정착 중 (수치 없음) | [인쇄] p.414 · [미확인] (A 의 수치) |

### 3-2. 구름 저항 모델 넷과 이 논문의 C 설정 (식 1–8 · p.409–411 · Fig 1)
| 모델 | 식 | 원문 서술 |
|---|---|---|
| **A** (Zhou et al. [13]) | 식 (1) T_r = −μ_r R_r \|F_n\| ω_rel/\|ω_rel\| · 식 (2) R_r = r_i r_j/(r_i + r_j) (벽이면 R_r = r_i) | 늘 법선력에 비례하는 반대 방향 토크 · *"caution must be used when using model A in a static situation … the bulk material creeping due to rapid oscillations in the rolling resistance due to the discontinuity in Eq. (1) at \|ω_rel\| = 0"* (p.410) |
| **B** (Zhou et al. [13]) | 식 (3) T_r = −μ_r R_r \|F_n\| (ω_i r_i − ω_j r_j) | 점성 (상대 굴림 속도 비례) — ⚠ 인쇄 그대로면 토크 × 속도 (N·m · m/s) 로 차원이 맞지 않는다 [카드 관찰 · `ai2011_…` §3-10 의 같은 관찰] |
| **C** (Iwashita & Oda [14] · Ai [12]) | 식 (4) 탄성부 = 증분 스프링 T^k ← T^k − k_r ω_rel Δt, 크기를 μ_r R_r \|F_n\| 에서 자름 · 식 (5) 점성부 T^v = −C_r ω_rel (T^v < μ_r R_r \|F_n\| 일 때만) · C_r = ζ 2√(k_r I_r) (I_r = 등가 관성 모멘트 · p.410) · 둘의 합 | *"elastic–plastic spring dashpot models"* — **'소성' = 회전의 한계 미끄럼** (입자 소성 아님) · 동적 계에서 A (감쇠 없음) 와 C 는 같아지고 정지 계에서는 C 가 낫다 (Ai) (p.410) |
| **D** | — | 접촉과 무관한 각속도 토크 — Ai 가 *"tenuous link to reality"* 로 깊이 보지 않았다 (p.410) |
| 공통 상한 | 식 (8) T_r,max = μ_r R_r \|F_n\| | A 는 늘 이 크기 · C 는 충분히 구른 뒤 이 크기 (p.411) |

- **구름 강성의 선택** (§2 · p.410–411): Ai · Wang 은 Bardet & Huang 의 원판 해석 식 (6) **k_r = 2 J_n R_r \|F_n\|** (J_n 0.25–0.5) 를 썼지만 *"The mechanisms at play in this situation are vastly different from the effects of shape"* 라 버리고, 구름 강성을 *"simply a mechanism to avoid the failings of model A"* 로 보아 **회전 고유 진동수를 전단 강성의 것과 같게** 두는 식 (7) **k_r = R_r² k_s** (k_s = 순간 전단 강성 · Cundall [21]) 를 고른다 — Iwashita & Oda 와 같은 선택.
- **구름 감쇠를 뺀 이유** (p.411): 낮은 k_r (식 6) 에서는 굴림 진동이 느려 전단 감쇠가 거의 안 듣지만 *"With higher levels of rolling stiffness, the shear damping is mobilised and additional rolling damping is not required"* · 고유 진동수를 같은 차수로 두면 *"the calculation of the critical time step is unaffected"*.

### 3-3. 단일 입자 굴림 시험 (Fig 2 · p.411)
- 조건 [인쇄]: 반지름 2.6 mm (d 5.2 mm) 입자를 평면 0.1 mm 위에서 수평 150 mm/s · 각속도 0 으로 놓아 굴러 멈출 때까지 · G 10 MPa · ν 0.3 · μ_p 0.5 · μ_r 0.2 · 감쇠비 (법선 · 전단) 0.8 (캡션) / *"the amount of damping in the shear direction was given by 0.8 times the critical value"* (본문) · PFC3D 4.00-187 · 세 경우 = Iwashita & Oda 강성 (감쇠 없음) · Bardet & Huang J_n 0.5 (감쇠 없음) · Bardet & Huang J_n 0.5 + 임계 감쇠 (ζ = 1).  캡션 · 본문에 **밀도 없음**.
- 원문 관찰 [인쇄 p.411]: J_n 0.5 · 감쇠 없음 = Ai 가 보고한 진동 · 감쇠를 넣으면 ① *"well damped — but not critically damped"* (1 자유도 기준의 '임계 감쇠' 라서) ② 충돌 순간의 큰 토크는 *"almost entirely due to and dependant on the amount of damping"* ③ 접촉이 자리 잡은 뒤 *"a value well above the model A limit for an almost a quarter of the remaining time"* (식 5 가 막으려던 것 · 낮은 강성 탓) ④ 훨씬 빨리 멈춤 · Iwashita & Oda 강성 = 충돌 순간 과도 뒤 A 의 한계에 곧 안착 · 멈춘 뒤 진동은 전단 감쇠가 지움.
- **판독 ↔ 식 [판독 · 래스터 · 카드 산술]** (원 래스터 xref 40 · 틀 보정):

| 양 | 판독 | 식 · 값 | 대조 |
|---|---|---|---|
| A 한계 토크 고원 (t 15–70 ms) | **0.756 μN·m** | μ_r R m g = 0.2 × 2.6 mm × (2000 · (4/3)π(2.6 mm)³ · 9.81) = **0.751 μN·m** (ρ = 표 1 의 2000 가정 · 벽 접촉 R_r = R) | 0.7 % |
| 감속 (한계 토크로 구르는 동안) | ω 16.46 → 8.54 (B&H 감쇠 없음) · 13.54 → 5.62 rad/s (I&O) · 55 → 70 ms ⇒ **528 rad/s²** | 미끄럼 없이 구르는 구: dΩ/dt = −T/(I + mR²) = −μ_r g/(1.4 R) = **−539 rad/s²** | 2 % |
| 봉우리 각속도 | **40.4 rad/s** (B&H 감쇠 없음 · 10.4 ms) · I&O ≈36.5 [판독 · 눈] | 미끄럼 → 구름 전환 끝 속도 (5/7) v₀ = 107 mm/s → Ω = **41.2 rad/s** (구름 저항 0 일 때 상한) | 낮은 k_r 판이 상한에 가깝다 |
| 정지 시각 (I&O) | ≈80 ms [판독 · 눈] | 36.5 rad/s ÷ 528 rad/s² = 69 ms → ≈81 ms | 같음 |
| B&H 감쇠 없음 굴림 진동 | 영점 ≈86 · ≈146 ms → 주기 ≈120 ms · 진폭 ω ≈±10.5 rad/s · 토크 최저 −0.73 μN·m (145 ms) [판독 · 래스터 · 눈] | k_r = 2 J_n R_r F_n = 3.75 × 10⁻⁶ N·m/rad · 접점 둘레 관성 1.4 m R² = 1.39 × 10⁻⁹ kg·m² → 2π√(1.4mR²/k_r) = **121 ms** | 같음 (중심 둘레 0.4 m R² 이면 65 ms — 맞지 않음) |

⇒ Fig 2 는 **해석 기대값이 붙는 단위 시험** 꼴이다 (우리 U2 쪽 · §8).

### 3-4. 편심 → μ_r 추정 (식 9) 과 회전 타원체 (식 10–15 · Fig 3–6 · p.411–413)
- 논리 [인쇄 p.411–412]: 비구형 접촉에서 법선력 작용선이 중심을 비켜 지나 토크 \|T_e\| = e\|F_n\| (Fig 3) → 식 (8) 과 맞대면 *"the product μ_r R_r should be of the same magnitude of the typical eccentricity of a contact"* → **식 (9) μ_r ≈ ⟨e⟩/R_r** (⟨e⟩ = 가능한 모든 접촉의 평균 편심 · R_r = *"the rolling radius of an idealised sphere representing the particle"*).  단서 (같은 쪽): *"shape can both create or encourage rolling as well as resist it, while all of the rolling friction models resist rolling in all cases"*.  편심을 μ_r 의 정의로 직접 쓰는 연구도 있다 (refs 7 · 13 · 15 · p.412).
- 타원 (식 10–12): 접점 (x₀, y₀) 의 법선 직선 (식 11) 까지 중심의 거리 = 부호 있는 편심 (식 12 · 반시계 + · p.412).  2D → 3D: x 축 회전면의 표면 평균 (식 13 · 14 — 띠 가중 y ds) · R_r = ∛(ab²) (부피 등가 구 · 식 15).  x 축 회전에서 a/b > 1 = prolate · a/b < 1 = oblate (Fig 4).
- **Fig 5** (2D 편심의 위치 분포 · a/b 0.25 · 0.5 · 0.75 · 1.33 · 2 · 4): 봉우리 ±1.5 (a/b 4 · 0.25) · ≈±0.71 (2 · 0.5) · ≈±0.29 (1.33 · 0.75) [판독 · 눈].  **정규화 기준은 원문에 없다** — 최대 \|e\| = \|a − b\| [카드 산술] 이고 (a − b)/√(ab) (같은 넓이 원의 반지름) 가 1.5 · 0.707 · 0.289 (1.33 은 0.286) 로 봉우리와 맞는다 [카드 산술 · 추정].
- **Fig 6 ↔ 원문 식 재계산** (위 = μ_r · 아래 = R_r/긴 반지름 · 가로 = 긴 축/짧은 축):

| AR | prolate 재계산 | prolate 판독 (얇은 선) | oblate 재계산 | oblate 판독 (굵은 선) | 2D 둘레 평균 ÷ ∛(AR) | R_r/긴 반지름 식 (prolate · oblate) ↔ 판독 |
|---|---|---|---|---|---|---|
| 1.7 | 0.354 | 0.357 | 0.351 | **0.373** | 0.367 | — |
| 2.0 | 0.464 | ≈0.47 [1.9 · 2.1 보간] | 0.456 | ≈0.49 [1.9 · 2.1 보간] | — | 0.630 · 0.794 |
| 2.1 | 0.498 | 0.503 | 0.488 | **0.531** | 0.530 | 0.610 · 0.781 ↔ 0.611 · 0.782 |
| 2.5 | 0.620 | 0.619 | 0.597 | **0.667** | 0.672 | 0.543 · 0.737 ↔ 0.543 · 0.738 |
| 2.98 | 0.747 | 0.745 | 0.704 | **0.821** | 0.824 | 0.483 · 0.695 ↔ 0.484 · 0.697 |
| 3.0 | 0.752 | — | 0.708 | — | — | 0.481 · 0.693 |
- 재계산 [카드 재계산]: 식 (12) 의 매개변수 꼴 · 식 (14) 띠 적분 (2 × 10⁵ 점) · 식 (15) — 같은 값을 **3D 삼각망 면적 가중 평균 (|x × n|)** 으로 따로 구해 확인 (AR 2: 0.4644 · 0.4564 · AR 3: 0.7521 · 0.7077).  판독 [판독 · 래스터] = 원 래스터 xref 82 (692 × 724 px) 를 틀 · 점선 격자로 보정 (위 0.0032 · 아래 0.0021 / px).
- ⇒ **얇은 선 (prolate) 과 아래 그림 (R_r) 은 원문 식 그대로 (±0.005)** · **굵은 선 (oblate) 은 재계산보다 +0.02 (AR 1.7) → +0.12 (AR 3) 높다** — 그 선은 '표면 가중 없이 2D 둘레 평균 \|e\| ÷ prolate 부피 반지름 ∛(AR)' 과 ±0.006 안에서 겹친다 [카드 재계산 · 원인 추정 — 원문 계산 과정은 [미확인]].  안식각 비교는 점묶음만 썼으므로 이 어긋남은 본 결론에 들어가지 않는다 (§11).
- 원문의 자리매김: *"The validity of this estimated coefficient of rolling friction is so-far entirely untested. However it is pleasing to note that the calculated values shown in Fig. 6 fit notionally within the range of typical values used in practice."* (p.413) — '쓰이는 범위' 의 숫자 [미확인].

### 3-5. 점묶음 (Fig 7 · 8 · 표 2 · p.413)
- 기하 [인쇄]: 이중 = 같은 지름 두 구 · 삼중 = 정삼각형 꼭짓점의 세 구 (*"the simplest form that is fully constrained against free rolling about any axis"*) · 단위 반지름 · 중심 간격 δ (구 반지름으로 정규화).
- 몬테카를로 편심 [인쇄 p.413 · 크롭 `txt_p5_monte_carlo_*`]: ① 구 하나를 무작위로 ② 무작위 단위벡터 ñ → 표면점 x = x_i − ñ (ñ = 접촉 법선) ③ 시험구 중심 x_test = x − ñ ④ \|x_test − x_j\| ≥ 2 (∀ j ≠ i) 가 아니면 버림 (다른 구 속의 점 · 곡률 때문에 닿을 수 없는 점) ⑤ θ = cos⁻¹((x/\|x\|)·ñ) · e = \|x\| sin θ ⑥ 평균.  R_r = 같은 부피 구의 반지름 (삼중의 부피도 몬테카를로).
- **판독 [판독 · 벡터]** ↔ **카드 재계산 (원문 절차 · 10⁶ 표본)**:

| δ | 이중 μ_r 곡선 · 재계산 | 이중 R_eq 곡선 · 재계산 | 삼중 μ_r 곡선 · 재계산 | 삼중 R_eq 곡선 · 재계산 |
|---|---|---|---|---|
| 0.5 | 0.187 · 0.182 | 1.111 · 1.109 | 0.183 · 0.181 | 1.169 · 1.170 |
| 1.0 | 0.349 · 0.347 | 1.189 · 1.191 | 0.340 · 0.340 | 1.305 · 1.305 |
| 1.5 | 0.506 · 0.506 | 1.240 · 1.242 | 0.493 · 0.493 | 1.403 · 1.401 |
| 2.0 | 0.671 · 0.668 | 1.259 · 1.260 (= 2^{1/3}) | 0.654 · 0.656 | 1.443 · 1.442 (= 3^{1/3}) |
- 표 2 (μ_r → δ) ↔ 곡선에서 다시 읽은 δ: 이중 0.49 · 0.79 · 1.10 · 1.45 · 1.76 ↔ 0.483 · 0.785 · 1.091 · 1.454 · 1.759 · 삼중 0.50 · 0.82 · 1.13 · 1.46 · 1.78 ↔ 0.491 · 0.798 · 1.123 · 1.491 · 1.807 [판독 · 벡터] — 재계산 μ_r 은 표 2 값과 ±0.01 [카드 재계산].
- 원문 문장: μ_r *"approximately proportional to the clump spacing"* (곡선 μ_r/δ 0.33–0.44 · 재계산 δ ≥ 0.5 에서 0.33–0.37) · 이중이 삼중의 *"within 1–2%"* (곡선 0–3.3 % · 재계산 0.5–2.7 % [판독 · 카드 재계산]) · *"within the bounds of what would be considered acceptable"* (p.413).

### 3-6. ★ 안식각 150 런 (Fig 9 · p.414–416) — 칸 평균 (두 반복의 평균 · °) [판독 · 벡터]
| μ_p \ μ_r(등가) | 이중 0.18 · 0.28 · 0.38 · 0.49 · 0.59 | 삼중 같은 순서 | 구 + 구름마찰 같은 순서 |
|---|---|---|---|
| 0.2 | 15.9 · 18.5 · 19.5 · 20.5 · 21.1 | 18.5 · 21.6 · 22.7 · 23.6 · 24.3 | 25.4 · 28.3 · 30.4 · 29.8 · 30.3 |
| 0.3 | 20.8 · 24.7 · 26.4 · 26.6 · 28.8 | 22.9 · 26.4 · 28.6 · 29.0 · 29.7 | 27.0 · 31.9 · 35.2 · 36.2 · 38.7 |
| 0.4 | 22.0 · 26.6 · 29.3 · 30.6 · 31.1 | 23.6 · 27.2 · 29.7 · 31.0 · 32.8 | 28.4 · 33.2 · 39.2 · 41.0 · 42.0 |
| 0.6 | 23.1 · 27.0 · 30.7 · 33.0 · 33.3 | 24.4 · 28.2 · 31.1 · 32.9 · 34.9 | 31.5 · 37.5 · 39.5 · 42.4 · 44.0 |
| 0.8 | 23.5 · 27.7 · 29.7 · 32.9 · 34.0 | 24.7 · 28.4 · 31.9 · 32.8 · 35.4 | 33.0 · 37.1 · 40.0 · 42.7 · 44.5 |
- 판독 방법: 위 줄 산점도의 마커 경로 (채운 원 0.2 · 빈 원 0.3 · + 0.4 · × 0.6 · * 0.8) 를 모양으로 갈라 중심 좌표 → 눈금선 · 눈금 글자로 보정 (x 잔차 ≤ 0.0007 · y ≤ 0.022°) · 패널마다 50 점 = 5 × 5 × 반복 2 (원문 150 런과 같은 수) · 범례 상자 안 마커 제외.  두 반복값은 `digitized.csv`.
- [카드 산술] 구 + 구름마찰 − 점묶음 (칸 평균): **이중 6.3–10.9° · 삼중 4.1–10.0°** (원문 *"up to 10° higher"*) · 삼중 − 이중 **−0.2–3.2° · 평균 1.6° · 25 칸 중 23 칸 양** (원문 *"limited to around 2° with the binary particles consistently giving a value lower"*) · 같은 칸 두 반복의 차 평균 **0.61 · 0.78 · 0.96°** · 최대 1.9 · 2.2 · 2.5° (이중 · 삼중 · 구).
- 원문 관찰 [인쇄 p.415–416]: 등고선이 *"begins very steeply before flattening out"* · 미끄럼과 모양 (구름) 은 *"hand-in-hand"* — 한쪽이 작으면 다른 쪽을 키워도 둔감 · *"The only way in which a large angle of repose can be achieved is if both of these mechanisms work together"* · 왼쪽 위 = 구름 지배 · 오른쪽 아래 = 미끄럼 지배 · 작은 δ 에서 점묶음 등고선은 거의 수직 (구 + 구름마찰보다 가파름) · 점묶음은 μ_p 0.2 → 0.3 에서 안식각이 급히 오르고 낮은 μ_r 의 구는 완만 — 판독: μ_r 0.18 에서 이중 +4.9° · 삼중 +4.4° ↔ 구 +1.6° [카드 산술] · 구 + μ_p 0.2 는 μ_r 0.38 뒤 ≈30° 에서 평평 (29.8 · 30.3 — 미끄럼 한계).

### 3-7. ★ '절반' 의 근거 — 같은 안식각을 내는 μ_r 의 비 [카드 산술]
같은 μ_p 에서, 구 + 구름마찰의 칸 평균 안식각을 점묶음 곡선 (칸 평균 · μ_r 사이 직선 보간) 이 내는 '등가' μ_r 를 찾아 비 = μ_r(구) ÷ μ_r(점묶음 등가):

| μ_p | 이중 (구 μ_r 0.18) | 삼중 (구 μ_r 0.18) |
|---|---|---|
| 0.2 | 점묶음 최대 21.1° < 구 25.4° → 범위 밖 | 최대 24.3° < 25.4° → 범위 밖 |
| 0.3 | 0.18 / 0.508 = **0.35** | 0.18 / 0.307 = **0.59** |
| 0.4 | 0.18 / 0.348 = **0.52** | 0.18 / 0.328 = **0.55** |
| 0.6 | 0.18 / 0.418 = **0.43** | 0.18 / 0.402 = **0.45** |
| 0.8 | 0.18 / 0.500 = **0.36** | 0.18 / 0.498 = **0.36** |
- **구 μ_r ≥ 0.28 의 모든 칸** 은 구 안식각이 계산한 점묶음 범위 (δ ≤ 1.76–1.78 ↔ 등가 μ_r ≤ 0.59) 의 최댓값을 넘는다 → 비를 낼 수 없다 (점묶음 안식각이 μ_r 에 단조라면 μ_r 0.28 줄은 비 < 0.28/0.59 = 0.47).
- ⇒ 원문 *"approximately half as much rolling friction"* · *"by at least a factor of two"* (p.416) 는 **보간이 되는 8 칸 (0.35–0.59 · 이중 평균 0.42 · 삼중 0.49)** 과 맞고, 나머지 칸은 '두 배보다 더' 쪽이다.
- 원문의 원인 두 갈래 [인쇄 p.416]: ① 모양은 회전을 돕기도 한다 — *"up to half of the contacts in the non-spherical case would be acting in the 'wrong' direction"* (*"hardly a robust argument"* 라 스스로 적음) ② 흐름 중 생긴 직물 (접촉이 표면에 고르게 퍼지지 않음) — 정착한 삼중 더미에서 잰 '관측' 식 (9) 값이 계산값보다 *"approximately 10% higher"* → *"far too small to account for the observed discrepancy"* (어느 δ · 몇 접촉인지 [미확인]).

### 3-8. 보정 — 관측량 하나로는 못 정한다 (§4.4 · p.416)
- *"a single angle of repose can be achieved from a wide range of parameters — each contour line spans a wide range of both the rolling friction and sliding friction coefficients"* · *"If a single property of a bulk material is measured (say an angle of repose), then Fig. 9 would tend to suggest that there is no method of choosing appropriate particle properties"* · 매개변수 둘로도 그렇고 *"would become even more relevant as the number of 'tuneable' parameters increases"* · *"One bulk parameter from one type of test is entirely insufficient."* · *"statistical scatter is ever present … Repeat simulations under the same conditions are extremely valuable"* [인쇄].
- 예 [카드 산술 · 칸 평균 직선 보간]: 구 + 구름마찰의 안식각 ≈30° = (μ_p 0.2, μ_r ≥ 0.38) · (0.3, 0.24) · (0.4, 0.21) · 이중 점묶음 ≈26° = (0.3, 0.36) · (0.4, 0.27) · (0.6, 0.25) · (0.8, 0.24).

---

## 4. ★ 방법 — 모델 · 시험 · 계산 사슬

### 4-1. 코드 · 모델 C 구현
PFC3D 4.00-187 (Itasca · 64 bit) 의 Hertz–Mindlin (no-tension) 접촉 위에 **모델 C 구름 토크를 C++ UDM 으로 더함** (p.414).  설정 = 식 (4) 탄성부 + k_r = R_r² k_s (식 7) · **구름 감쇠 없음** (전단 감쇠 0.8 이 진동을 잡는다 · p.411).  R_r 은 식 (2) 의 쌍 유효 반지름으로 정의돼 있지만 **안식각 런의 UDM 이 어느 R_r 를 썼는지는 인쇄 안 됨** [미확인 — §11].  점묶음 = PFC3D 의 겹친 구 묶음 (clump) · 무작위 방향.

### 4-2. 안식각 시험의 사슬
구 7000 개 생성 (점묶음 런은 같은 부피의 점묶음으로 바꿈) → 원통 (Ø91 × 136.5 mm) 안 중력 정착 1 s → 원통 16 mm/s 상승 · 틈으로 흘러 더미 → 상승 시작 뒤 5 s → 36 쐐기 · 10 칸 · 최고 입자 · 회귀 → 쐐기 평균 = 안식각 → 칸마다 2 반복.  관측량은 **안식각 하나** (더미 높이 · 밀도 · 접촉 수 · 유동 시간 없음).
- **압력을 뺄 때 (탈압)**: 해당 없음 — 압력 0 · 정착만.  정지 쪽 함정 하나: 모델 A 더미의 기어감 (p.410 · p.414).

### 4-3. 편심 계산
회전 타원체 = 식 (12)–(15) 의 수치 적분 (*"relatively straight forward"* · 격자 · 정밀도 [미확인]) · 점묶음 = 몬테카를로 (§3-5 · 반복 수 [미확인] · *"Any number of iterations can be carried out to reach a required level of accuracy"*) · 부피 = 상자 속 무작위 점의 비 (p.413).

### 4-4. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM 한계 진술 (원문 문장 그대로)**:
  1. *"Practically this means scaling of particle size and stiffness, and idealisation in the form of spheres and simplified contact mechanics."* (p.409)
  2. *"one question concerns how the real contact mechanics and particle properties influence the behaviour of a bulk material, the other concerns how to get idealised spherical particles to behave like a bulk material made up of many more real particles of a wide size distribution and arbitrary shape."* (p.409)
  3. *"In a granular material these mechanisms can be important, however in a practical situation they are most likely dwarfed by the effects of shape. Shape is an expensive thing to model in DEM, and so rolling friction is typically used in an effort to model this effect."* (p.409)
  4. *"the link between the model and the mechanism is not at all clear. In particular, there is currently no physical reasoning that is applied in the selection of a value for rolling friction, rather it tends to be treated as a parameter to be 'tuned' in an effort to produce realistic behaviour."* (p.410)
  5. *"caution must be used when using model A in a static situation. The relevant issue revolves around the bulk material creeping due to rapid oscillations in the rolling resistance due to the discontinuity in Eq. (1) at \|ω_rel\| = 0."* (p.410)
  6. *"the notion of 'critical damping' used in most DEM studies (including the present) is based on a simplified one degree-of-freedom system."* (p.411)
  7. *"shape can both create or encourage rolling as well as resist it, while all of the rolling friction models resist rolling in all cases."* (p.412)
  8. *"If a single property of a bulk material is measured (say an angle of repose), then Fig. 9 would tend to suggest that there is no method of choosing appropriate particle properties."* · *"One bulk parameter from one type of test is entirely insufficient."* (p.416)
  9. *"Shape … is every bit as important as the mechanics of contact. Unfortunately it is also one of the hardest properties to model accurately."* · *"Without any physical basis, the coefficient can only ever be considered a 'tuneable parameter'."* (p.416)
  - 압밀 · 겹침 · 상대밀도 · 변형률 상한 · 접촉 독립 가정 · 조밀 영역 강성에 관한 문장은 **없다** (말 없음).
- **(ii) 소성 · 큰 변형 = 말 없음**: *"plasticity"* 는 구름 손실의 접촉 이력 근원 목록에 한 번 (*"micro-sliding, visco-elasticity, plasticity, surface adhesion, etc."* · p.409) — 그리고 그것은 모양에 *"dwarfed"* 된다고 적는다.  모델 C 의 *"elastic–plastic"* 은 **구름 토크 법칙** (회전 스프링 + 한계에서 미끄러짐) 이다.  입자는 끝까지 **고정 모양** (구 · 겹친 구) 이고 우회는 **모양을 계산하지 않고 토크로 흉내** (싸다) 또는 **겹친 구로 고정 모양** (비싸다 — 비용 수치 [미확인]).  맞춘 값 = 없음 (식 9 는 예측 · AOR 비교가 그 예측의 ≈2 배 과대를 드러냄).
- **(iii) 차원**: 안식각 DEM 은 **3D** (PFC3D) · 편심 해석은 2D 타원 (Fig 4–5) → 회전면 표면 평균으로 3D (식 13–14 · p.412 *"The previous analysis applies only to the two dimensional case, however we can develop this further into three dimensions …"*) · 2D 타원 DEM 은 refs 로만 (p.412 *"and in 2D, [18]"*).  **2D → 3D 의 가중이 값을 바꾼다**: AR 3 에서 2D 둘레 평균 ÷ ∛(AR) 0.830 ↔ 3D prolate 0.752 (−9 %) · oblate 0.708 (−15 %) [카드 재계산] — Fig 6 의 oblate 선이 바로 이 차이 크기만큼 어긋난다 (§3-4).
- **(iv) 탈압**: 없음.  가장 가까운 것 = 정지 · 정착 쪽 모델 A 기어감 (p.410 · p.414 · 수치 없음).

### 4-5. 기법 미니 용어집
- **구름마찰 (rolling friction · rolling resistance)** = 접촉한 두 입자의 상대 굴림을 막는 추가 토크 — 모양 · 접촉 이력의 대리.
- **굴림 반지름 R_r** = 토크 크기 μ_r R_r F_n 의 길이 — 식 (2) 쌍 유효 반지름 r_i r_j/(r_i + r_j) (같은 크기 두 구면 R/2 · 벽이면 R) ↔ 식 (9) · (15) 의 '입자를 나타내는 구' 의 반지름 (§11).
- **접촉 편심 e** = 법선력 작용선과 입자 중심 사이 거리 — 토크 e·F_n.
- **모델 A · B · C · D** = 일정 토크 · 점성 · 탄소성 스프링–대시포트 (구름 스프링 + 한계) · 접촉 무관 (Ai 2011 의 분류).
- **구름 강성 k_r** = 모델 C 의 회전 스프링 — 식 (6) (원판 해석 · 낮음) ↔ 식 (7) (전단 강성과 같은 고유 진동수 · 높음).
- **점묶음 (clump)** = 겹친 구를 한 강체로 묶은 비구형 입자 (EDEM · PFC3D).
- **안식각 (angle of repose, AOR)** = 쌓인 더미 사면의 기울기 — 여기서는 원통 인양 더미의 쐐기 회귀 평균.
- **UDM (User Defined Model)** = PFC3D 에 C++ 로 접촉 법칙을 더하는 틀.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 모델 A (점선) ↔ C (실선) 의 토크–회전각 고리 (탄성부만 · 한 입자가 평면에서 일정 각 굴렀다 되굴림) | A 는 방향이 바뀌는 순간 토크가 뛰고 (불연속) C 는 기울기 k_r 로 이어진다 — 우리 cdt (A 꼴) 의 정지 기어감을 설명할 그림 |
| 2 | ★ 단일 입자 굴림 시험 (토크 · 각속도 vs 시간 · 강성 · 감쇠 세 판) | 해석 기대값이 붙는 단위 시험 (§3-3) — U2 쪽 |
| 3 | 임의 모양 두 입자의 접촉 · 편심 e · 토크 T | 식 (9) 의 그림 · 모양 토크의 방향은 굴림 방향과 무관 |
| 4 | 타원 단면 · 접점 · 띠 ds · 편심 | 식 (10)–(14) 의 기호 |
| 5 | 2D 타원 둘레의 편심 분포 (a/b 0.25–4) | 정규화 [미확인 · 추정 √(ab)] |
| 6 | ★ 회전 타원체 μ_r 추정 · R_r/긴 반지름 vs AR | 모양 → μ_r 환산표 (prolate 만 원문 식과 맞음 · §3-4 · §11) |
| 7 | 정삼각 삼중 점묶음의 기하 | 몬테카를로 절차의 기하 |
| 8 (a · b) | ★ 이중 · 삼중 점묶음의 μ_r · R_eq vs δ | 점묶음 ↔ μ_r 환산 (표 2) — 카드 재계산과 ±0.01 |
| 9 (a · b · c) | ★ 안식각 150 런: 원자료 (위) · 등고선 (아래) | 구름마찰 대리의 크기 (최대 ≈10° · ≈2 배) · 보정 비유일성 (등고선) · 반복 산포 |
| 표 1 | 안식각 입자 물성 | 조건 기록 |
| 표 2 | μ_p · μ_r · δ 격자 | 조건 기록 |
| 식 크롭 16 장 | `eq_01`–`eq_15` (식 번호마다 하나) + `eq_05b` (본문 속 C_r = ζ 2√(k_r I_r)) | 보고서 DEM 절에 붙일 구름 저항 식 · 편심 식 |
| 근거 문단 20 장 | `txt_p1_*` (초록 · DEM 한계 · 손실 근원) · `txt_p2_*` (A 기어감 · 조율 매개변수 · 강성 선택) · `txt_p3_*` (감쇠 · 단일 입자 시험) · `txt_p4_*` (식 9 논리) · `txt_p5_*` (미시험 · 몬테카를로 · 비례) · `txt_p6_*` (계산 사양 · 런 · A 정착) · `txt_p7_*` (등고선 해석) · `txt_p8_*` (10° · 두 배 · 비유일성 · 결론) | 원문 인용용 |

## 6. Post-processing ★
- **무엇을**: 안식각 (쐐기 회귀 평균) · 단일 입자의 토크 · 각속도 시간 이력 · 타원 편심 분포 · 회전 타원체 · 점묶음 μ_r (해석 · 몬테카를로) · 등가 μ_r 로 그린 원자료 · 등고선 (반복 평균) · 정착 더미의 '관측' 편심 (≈10 % 높음).
- **안 한 것**: 실험 · 압밀 · 밀도 · 접촉 수 · 직물 분포 · 유동 시간 · 회전 타원체 DEM · 반복 3 회 이상 · 오차 막대 · 수렴 (Δt · 입자 수 · 원통 크기) · 계산 비용.
- **이 카드의 후처리**: Fig 9 원자료 150 점 · Fig 8 곡선 162 꼭짓점 = **벡터 경로 좌표** (눈금선 ↔ 눈금 글자 보정) · Fig 2 · 6 = 원 래스터 틀 · 격자 보정 · 칸 평균 · 차 · 같은 안식각 μ_r 비 (직선 보간) · 원문 식 (12)–(15) 과 몬테카를로 절차의 재계산 (+ 3D 삼각망 검산) · Fig 2 의 정지 토크 · 감속 · 굴림 진동 주기 · 전환 각속도 해석값.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · 정본 카드 표기를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 목적 · 체제 | 중력 안식각 (5 mm 구 · 7000 개) | 300 MPa 압밀 · 믹서 (µm SE · NCM) | 체제가 다르다 — 방법 · 함정만 옮긴다 |
| 모양 | 구 + 구름마찰 ↔ 겹친 구 (고정 모양) | DEM = 구 + 구름마찰 (μ_r 0.2/0.1 · SE–SE 0.1 · 믹서 0.075 — 정본 카드 표기 · 리포 미대조) · MPM = 실제 형상 변형 | DEM 쪽은 같은 대리 · MPM 은 대리가 필요 없다 |
| 구름 토크 모델 | **C** (탄소성 스프링–대시포트 · k_r = R_r² k_s · 감쇠 없음) | 압축 · 믹서 덱 `rolling_friction cdt` (τ = μ_r k_n δ_n R_ef ω̂ — `sun2026_…` L201 표기) = **A 꼴** [`ai2011_…` §7-2 대조] | 모델이 다르다 → μ_r 숫자 비교 금지 (`roessler2019_…` L191 과 같은 결론) |
| 접촉 법칙 · 강성 | Hertz–Mindlin (no-tension) · G 10 MPa (E 26 MPa) | 압축 hooke/hysteresis · SE E_eff 1.35 GPa (18 배 연화) | 둘 다 '축척된 강성' (원문 p.409) — 우리 SE 가 52 배 뻣뻣 [카드 산술] |
| 보정 | 없음 (식 9 예측 ↔ AOR 대조) | DEM = E_eff 를 순수 SE 기공 (랩 표준 10–13 %) 에 · MPM = σ_y 하나 | 원문 §4.4 의 비유일성 경고가 우리 'μ_r 고정 · 하나만 맞춤' 규칙 (R5) 을 받친다 |
| 탈압 | 없음 | DEM 언로딩 키트 · MPM 제하 없음 | A 꼴 기어감 경고만 |

### 7-2. ★ 랩 기준과 나란히 (판정 없이)
| 출처 | 재료 · 입경 | 압력 · 상태 | 진밀도 분모 | 기공 |
|---|---|---|---|---|
| **랩 표준** | LPSCl | 300 MPa | **1.64** (고정) | **10–13 %** |
| 이 논문 | 일반 구 · 점묶음 4.6–5.2 mm | 중력 (압력 0) · 더미 | 없음 | **없음** (porosity · density 0 회) |
- 나란히 놓을 숫자가 **없다** — 이 논문의 자리는 기공 표가 아니라 '구름마찰 계수의 지위' 다.

### 7-3. ★ 우리 덱의 구름마찰 (A 꼴 `cdt`) ↔ 이 논문 (C)
- **지위**: 우리 압축 덱 μ_r 은 정본 카드 표기로 *"구름저항(표면거칠기/비구형 흉내)"* (`luding2008_…` L185) · 믹서 0.075 는 *"비구형성 대리"* (`hare2026_…` L89) — 이 논문의 말로는 **'조율 매개변수'** 이고 모양에서 온 값이 아니다 (p.410 · p.416).
- **모양 ↔ μ_r 환산 (식 9) 으로 거꾸로 읽으면** [카드 산술 · prolate 재계산 곡선을 거꾸로 풂 · 같은 크기 두 구 기준 · 방향만]: 우리 SE–SE μ_r 0.1 = prolate AR **≈1.16** (숫자를 식 9 에 그대로) · **≈1.08** (우리 cdt 는 R_ef = 쌍 유효 반지름 · 같은 크기 두 구면 R/2 — 같은 토크의 식 9 값 (입자 반지름 기준) 은 0.05) · **≈1.35** (숫자 그대로 + AOR 의 '절반' 규칙 — 식 9 값이 2 배인 모양) → 정의 둘 (R_r · '절반') 에 따라 **AR 1.08–1.35** 로 갈린다.  같은 방식으로 AM 0.2 → 1.16–1.82 · 믹서 0.075 → 1.06–1.25.  ⇒ 정의를 등록하지 않은 모양 환산은 쓰지 않는다 ('절반' 은 5 mm 중력 더미에서만 잰 값 · 압밀 체제는 범위 밖).
- **정지 쪽 함정**: 모델 A 꼴은 정지 계에서 기어간다 (p.410) · 3D 7000 입자 더미가 5 s 뒤에도 정착 중 (p.414 · 수치 없음) — Ai 2011 의 2D 관찰을 3D 로 되풀이.  우리 cdt 로 정착 · 판 고정 이완 · 언로딩을 판정할 때 이 기어감의 크기 (300 MPa 조밀 침대) 는 **미측정** — `ai2011_…` §7 · 비교 문서 F 절 (2026-11-12) 의 'Δt × ½ 같은 런' · 'cdt ↔ epsd2 단위 시험' 과 같은 할 일.

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: DEM (입자 · 접촉) 쪽의 **모양 대리 기법의 한계** 와 그 크기 · 보정 비유일성.
- **없는 것**: 압밀 · 수송 · 실제 형상 변형 · 실험.  ⇒ DEM 쪽에는 '구름마찰 = 조율 매개변수 · A 꼴 기어감 · 단일 관측량 보정 금지' 를, MPM 쪽에는 '고정된 비구형조차 구 + 구름마찰과 다르다 → 형상을 푸는 모델의 필요' 라는 **정성 논거만** 준다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  우리 덱 μ_r = 정본 카드 표기 · 리포 미대조.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ (1) 관측량 하나는 매개변수 둘 이상을 못 정한다 (§4.4 · 등고선 하나가 (μ_p, μ_r) 넓은 범위를 지남 — 예 §3-8) → 등록 때 **'무엇을 고정하고 무엇 하나를 맞추나'** 칸 (2) 반복 2 런의 산포 (칸 평균 차 0.6–1.0° · 최대 2.5°) → 판정 띠에 **시드 산포** 칸 (3) 판정 알고리즘을 인쇄 (쐐기 · 칸 · 회귀) — 연산자 정의를 결과 전에 적는 본보기 | 기공 · 밀도 연산자 없음 · 버리는 몫 [미확인] |
| **단계 1–3** (3D 메모리 · 2D MPM · 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · 값 하나 맞춤) | R5 의 근거 문장 (*"One bulk parameter from one type of test is entirely insufficient"* — 매개변수가 둘 이상 자유일 때) · DEM 쪽: E_eff 를 기공에 맞출 때 μ_r 은 고정값 · 그 값의 근거를 적어야 맞춘 E_eff 가 뜻을 가진다 [카드 추론] | 압밀 · 기공 숫자 없음 · 5 mm 중력 더미 · MPM 은 μ_r 없음 |
| **단계 5** (3D 복합 압밀) | 우리 AM/SE μ_r (0.2/0.1) 의 지위 = 모양 대리 조율값 · 식 (9) 환산 (§7-3) | 조밀 압밀에서 구름마찰의 몫 · 등가성 [미확인] |
| **단계 6** (탈압 · 되돌아옴) | ★ 모델 A 꼴 정지 기어감 (p.410 · p.414 · 3D 더미) → 우리 cdt 로 이완 · 언로딩을 잴 때 **정착 시간 · Δt 수렴 칸 + C (epsd) 대조 한 런** (`ai2011_…` 과 같은 할 일) | 기어감의 크기 · 압력 아래 거동 미측정 |
| **단계 7** (형상 · 피복 · 수송) | 없음 | — |
| **후보 D0** (지금 DEM) | ★ 구름마찰 대리의 정량 한계: 같은 등가 μ_r 에서 구 + 구름마찰이 점묶음보다 4.1–10.9° 높고 · 같은 안식각에 드는 μ_r 은 식 (9) 의 0.35–0.59 배 · 기전 차 (모양은 회전을 돕기도 함) → 우리 μ_r 의 지위를 '조율 매개변수' 로 기록 · 모양 근거를 대려면 SEM 종횡비 → 식 (9) (× R_r 정의 · × '절반' 단서) | 압밀 체제 대조 없음 · 실험 없음 |
| **후보 A′-0 · A · A′** (MPM 접촉 · 강체 AM · 입자별 속도장) | 흐름 밖 논거: 형상을 푸는 모델은 μ_r 대리가 필요 없다 — 고정된 비구형조차 구 + 구름마찰과 같지 않다 (≈2 배) | 정량 없음 |
| **후보 B** (입자별 FE) | 같은 논거 | — |
| **후보 C · C′** (MDR · 항복 캡 DEM) | ⚠ **이름 함정**: 모델 C 의 *"elastic–plastic"* = 구름 토크 (회전 스프링 + 한계 미끄럼) · **법선 접촉 소성 (Thornton–Ning 항복 캡) 과 다른 것** — 섞지 않는다 | 법선 소성 · 큰 변형 없음 |
| **후보 M0** (균질화 압밀) | 없음 | — |
| **U0–U6** | ★ **U2** (경사면 마찰 접촉 회귀) 쪽: Fig 2 단일 입자 굴림 = 해석 기대값이 붙는 시험 — 정지 토크 μ_r R m g · 감속 μ_r g/(1.4R) · 전환 각속도 (5/7) v₀/R · 굴림 진동 2π√(1.4mR²/k_r) (판독과 0.7–2 % · §3-3) → LIGGGHTS cdt ↔ epsd2 단일 구 시험의 기대값 표 | 경사 정지 시험은 `ai2011_…` 쪽 |
| **R1–R7** | **R5** (맞추는 값은 모델마다 하나) — §4.4 문장 · **R6** (SE 형상 변형) — 고정된 비구형도 구 + 구름마찰과 다르다 → 변형하는 모양은 더 멀다 [카드 추론] · **R4** (탈압) — A 꼴 기어감 | R1 · R2 · R3 · R7 없음 |
| **결과 전 대조 항목** | 이 논문의 안식각 값은 우리 계의 대조 항목이 아니다 · 쓸 수 있는 것은 Fig 2 단위 시험 기대값 · '식 (9) × ≈½' 의 방향 | 절대값 전이 금지 |

- **재료 · 차원 · 조건 차이**: 일반 구 · 점묶음 (재료 없음) ↔ LPSCl · NCM811 · 4.6–5.2 mm ↔ µm · 중력 ↔ 300 MPa · 3D = 같음 · Hertz–Mindlin G 10 MPa ↔ hooke/hysteresis E_eff 1.35 GPa · 모델 C ↔ cdt (A 꼴).

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **우리 μ_r 의 지위를 '조율 매개변수' 로 적는다** — 원문 p.410 · p.416 의 문장 그대로.  정본 카드들의 *"비구형 흉내"* 표기는 이 논문 기준으로 '모양에서 유도한 값' 이 아니다 (D0 · 보고서 한정어).
2. **모양 → μ_r 을 쓰려면 정의 둘을 맞춘다** — R_r (우리 cdt 의 R_ef = 쌍 유효 반지름 ↔ 식 (9) 의 입자 반지름 · 같은 크기면 2 배 차) 과 '구름마찰이 모양보다 ≈2 배 세다' (AOR 에서만 잰 값) — 둘 다 적지 않은 환산은 쓰지 않는다 (§7-3).
3. **A 꼴 (cdt) 정지 기어감 = 탈압 · 이완 판정의 함정** — 2D (Ai) 에 이어 3D 더미에서도 5 s 뒤 정착 중 (p.414).  언로딩 판정 전 'cdt ↔ epsd2 같은 침대 한 런' 과 'Δt × ½' 를 결과 전에 등록 (단계 6).
4. **관측량 하나로 매개변수를 맞추지 않는다 · 반복을 넣는다** — §4.4 · 칸 산포 0.6–1.0° (최대 2.5°) → 믹서 D3 (SE–SE 점착 유동성 실측 앵커 — CLAUDE.md) 같은 '벌크 관측량 하나로 접촉 매개변수' 설계는 μ_s · μ_r 를 고정한 채로만 뜻이 있고 반복 런 산포를 판정에 넣는다 [카드 추론].
5. **단일 입자 굴림 시험을 단위 시험으로 가져온다** — 기대값이 해석으로 나온다 (§3-3) · 우리 덱 구름 토크의 구현 확인 (U2).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Rolling friction is typically used in DEM because particle shape is computationally expensive to model; without a physical basis its coefficient is a 'tuneable parameter' (Wensrich & Katterfeld, Powder Technol. 217 (2012) 409–417, pp. 409–410, 416)."
- "In back-to-back PFC3D angle-of-repose simulations (7000 particles, 4.6–5.2 mm), spheres with model C rolling friction gave angles of repose up to ≈10° higher than binary/ternary clumps of the 'equivalent' coefficient μ_r ≈ ⟨e⟩/R_r; about half the estimated rolling friction reproduced the clumps (Wensrich & Katterfeld 2012, p. 416; 4.1–10.9° and 0.35–0.59 digitized from Fig. 9)."
- "A single angle of repose can be produced by a wide range of sliding and rolling friction pairs — 'One bulk parameter from one type of test is entirely insufficient' (Wensrich & Katterfeld 2012, p. 416)."
- 국문: *"DEM 은 모양을 계산하기 비싸 구름마찰로 대리하지만, 그 계수는 물리 근거가 없으면 조율 매개변수일 뿐이다 (Wensrich & Katterfeld 2012)."*
- 국문: *"같은 '등가' 구름마찰의 구는 겹친 구 묶음보다 안식각을 최대 ≈10° 높게 낸다 — 모양은 회전을 돕기도 하지만 구름마찰은 늘 막기 때문이다 (Wensrich & Katterfeld 2012 · 수치 = Fig 9 판독)."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **실험 0 · '모양의 정답' = DEM 점묶음** — 겹친 구 묶음이 실물 모양을 얼마나 담는지는 다루지 않는다 (ref [16] Markauskas 2010 을 인용만).
2. **Fig 6 의 oblate 선 ↔ 원문 식** — 얇은 선 (prolate) 과 R_r 그림은 식 (9) · (12)–(15) 재계산과 ±0.005 로 맞지만 굵은 선 (oblate) 은 +0.02 (AR 1.7) · +0.04 (2.1) · +0.07 (2.5) · +0.12 (2.98) 높다 [판독 · 래스터 · 카드 재계산 (적분 · 3D 삼각망 두 방법 같음)].  그 선은 '2D 둘레 평균 \|e\| ÷ ∛(AR)' 과 ±0.006 안에서 겹친다 — 원인 [추정] · 계산 과정 [미확인].  oblate μ_r 를 인용하려면 재계산값 (AR 2: 0.456 · AR 3: 0.708) 을 함께 적는다.
3. **R_r 의 두 정의** — 식 (9) · (15) · 점묶음의 R_r = 입자 (부피 등가) 반지름 ↔ 모델 토크 식 (1) · (8) 의 R_r = 식 (2) 쌍 유효 반지름 (같은 크기 두 구면 R/2).  안식각 런의 UDM 이 어느 것을 썼는지 [미확인].  식 (2) 였다면 '등가' μ_r 의 토크는 식 (9) 전제의 절반 → 관측된 '구름마찰이 2 배 세다' 는 토크 크기로는 ≈4 배가 된다 [카드 산술 · 가정].  Fig 2 의 벽 접촉 (R_r = R) 은 이를 가르지 못한다.
4. **'절반' 의 표본** — 보간이 되는 칸은 구 μ_r 0.18 줄의 8 칸뿐 (0.35–0.59) · μ_r ≥ 0.28 은 점묶음 범위 밖 (§3-7).
5. **원문 수치 문장 ↔ 판독**: *"up to 10°"* ↔ 이중 최대 10.9° (μ_p 0.2 · μ_r 0.38) · 삼중 최대 10.0° · *"around 2° … consistently"* ↔ −0.2–3.2° · 평균 1.6° · 23/25 칸 · *"within 1–2%"* (μ_r 이중 ↔ 삼중) ↔ 곡선 0–3.3 % · 재계산 0.5–2.7 % [판독 · 벡터 · 카드 재계산].
6. **반복 2 · 오차 막대 없음** — 칸 산포 최대 2.5° 가 이중 ↔ 삼중 차 (≈1.6°) 와 같은 크기.
7. **판정 알고리즘의 버리는 몫** (안쪽 · 바깥 끝) · 원통 상승 16 mm/s — 다른 카드 2 차 인용으로 Roessler & Katterfeld 는 인양식 안식각이 저속 (2 mm/s) 에서만 크기 불변이고 16 mm/s 는 동적 조건이라 한다 (`coetzee2017_…` L613–614 · 이 논문 밖) → 이 논문 안식각의 속도 · 크기 의존 [미확인].
8. **회전 타원체 μ_r 은 DEM 으로 시험 안 함** (*"so-far entirely untested"* · p.413) · *"typical values used in practice"* 의 범위 [미확인].
9. **식 (3) 모델 B** 인쇄 꼴이 토크 × 속도 (차원 불일치 · `ai2011_…` 과 같은 관찰) · **식 (5)** 조건 T^v < μ_r R_r \|F_n\| 에 절댓값이 없다 (인쇄 그대로).
10. **Fig 5 정규화 미기재** (√(ab) 로 추정) · **Fig 2 캡션에 밀도 없음** (고원이 ρ 2000 과 맞음).
11. **모델 A 정착 문장** — *"still in the process of settling"* 의 크기 (속도 · 안식각 차 · 런 수) [미확인].
12. **'관측' 편심 +10 %** — 정착 삼중 더미 하나 · δ · 접촉 수 [미확인].
13. **표기**: 본문 'ternary' ↔ Fig 7 캡션 · Fig 9 (b) 제목 'Tertiary' · Fig 9 (c) 위 'Angle of repose' ↔ 아래 'Angle of Repose' (대소문자).  텍스트 층의 Fig 4 캡션 'a/bb1' 은 인쇄 'a/b<1' 의 글꼴 치환 (인쇄 문제 아님).
14. **계산 비용 · Δt 근거** — '3–4 μs · 임계의 25 %' 만 · 런 시간 · 점묶음 ↔ 구의 비용 비 [미확인] (원문은 '비싸다' 고만 한다).
15. ⚠ **판독 값**은 벡터 좌표 (Fig 8 · 9) 라 정밀하지만 원문 인쇄값이 아니다 — [판독] 표지로만 인용.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 12 | J. Ai, J.-F. Chen, J.M. Rotter, J.Y. Ooi, Assessment of rolling resistance models in discrete element simulations, Powder Technology 206 (2011) 269–282. | 모델 A–D · 'C 가 낫다' 의 출처 (2D) | `ai2011_rolling_resistance_contact_models_dem` |
| 13 | Y.C. Zhou, B.D. Wright, R.Y. Yang, B.H. Xu, A.B. Yu, Rolling friction in the dynamic simulation of sandpile formation, Physica A 269 (1999) 536–553. | 모델 A · B 원전 (= 우리 cdt 꼴) | 없음 (wishlist L208) |
| 14 | K. Iwashita, M. Oda, Rolling resistance at contacts in simulation of shear band development by DEM, Journal of Engineering Mechanics ASCE 124 (1998) 285–292. | 모델 C · k_r = R_r² k_s 원전 | 없음 (wishlist L209) |
| 15 | H.P. Zhu, A.B. Yu, A theoretical analysis of the force models in discrete element method, Powder Technology 161 (2006) 122–129. | 편심을 μ_r 정의로 쓰는 예 (식 9 의 이웃) | 없음 |
| 16 | D. Markauskas, R. Kačianauskas, A. Džiugys, R. Navakas, Investigation of adequacy of multi-sphere approximation of elliptical particles for DEM simulations, Granular Matter 12 (2010) 107–123. | 겹친 구가 실제 모양을 얼마나 담나 (이 논문 '정답' 의 근거) | 없음 (`coetzee2017_…` 인용) |
| 17 | T.-T. Ng, Shear strength of assemblies of ellipsoidal particles, Geotechnique 54 (2004) 659–669. | 타원체 DEM 의 강도 (모양 효과의 직접 계산) | 없음 |
| 18 | L. Rothenburg, R.J. Bathurst, Micromechanical features of granular assemblies with planar elliptical particles, Geotechnique 42 (1992) 79–95. | 2D 타원 입상체 | 없음 (`cantor2020_…` 등 인용) |
| 20 | J.P. Bardet, Q. Huang, Rotational stiffness of cylindrical particle contacts, Powders and Grains '93, Proc. 2nd International Conference on Micromechanics of Granular Media, Birmingham, UK, 1993, pp. 39–43. | 식 (6) k_r = 2J_n R_r F_n 원전 | 없음 (`ai2011_…` 인용) |
| 4 | M. Dratt, A. Katterfeld, C.A. Wheeler, Prediction of conveyor belt deflection by coupling of FEM and DEM simulations, Bulk Solids and Powder, Science and Technology 3 (2010) 380–384. | DEM ↔ FEM 결합 선례 (기계 부품 · 입자 아님 · 서론 인용만) | 없음 |
| 21 · 22 | P.A. Cundall, Computer simulations of dense sphere assemblies (1988) · PFC3D 4.00 User Manual (2011) | k_s 정의 | 없음 |

---

## [미확인] 목록
- 안식각 런의 UDM 이 쓴 R_r (식 2 ↔ 입자 반지름) · 모델 C 의 k_s 값 · 임계 Δt 의 산출.
- 판정 알고리즘의 버리는 몫 (안쪽 · 바깥 끝) · 원통 채움 높이 · 정착 뒤 충전율.
- 모델 A 예비 런의 수 · 정착 미완의 크기 · 런 시간 · 계산 비용 (점묶음 ↔ 구).
- Fig 6 oblate 선의 계산 과정 (재계산과 다름 · §11) · Fig 5 의 정규화 · 수치 적분 · 몬테카를로 반복 수.
- '관측' 편심 +10 % 의 δ · 접촉 수 · 더미 수.
- *"typical values used in practice"* 의 범위 · LIGGGHTS EPSD 계열과 이 논문 설정의 관계.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-13)
- 서지: 후보 표 메모 (Wensrich, C. M., & Katterfeld, A. (2012). Rolling friction as a technique for modelling particle shape in DEM. Powder Technology, 217, 409–417) = 원문 첫 쪽과 같음 · DOI 10.1016/j.powtec.2011.10.057 = 첫 쪽 인쇄 · PDF 문서 정보는 비어 있음 (제목 · 저자 칸 공란).  SI · 부록 없음.
- 숫자: 텍스트 층 9 쪽 전수 대조 — 4.6–5.2 mm · 2000 kg/m³ · 1e7 Pa · 0.3 · 0.8 · 7000 · 91 mm · 136.5 mm · 1 s · 16 mm/s · 5 s · 36 · 10 · 25 % · 3–4 μs · 150 · 50 · 2.6 mm · 0.1 mm · 150 mm/s · 5.2 mm · 10 MPa · 0.5 · 0.2 · J_n 0.25–0.5 · ζ = 1 · 10⁻⁷ m/s · 10° · 2 배 · ≈10 % · ≈2° · 1–2 % · 표 2 의 15 값 — 전부 위치 확인.
- 낱말 횟수 (본문 · 참고문헌 앞): plastic 2 (plasticity 1) · deform 0 · compaction 0 · porosity 0 · pressure 0 · unload 0 · experiment 0 · density 1 (표 1) · LIGGGHTS 0 · EDEM 1 · PFC 3 · calibrat 5 · tuneable 2 · clump 48.
- 판독 보정: Fig 8 · 9 = 벡터 경로 (마커 모양 · 꺾은선 꼭짓점) ↔ 눈금선 · 눈금 글자 · Fig 2 · 6 = 원 래스터 틀 · 격자선 · 재계산: 식 (12)–(15) 수치 적분 + 3D 삼각망 · 몬테카를로 (원문 단계 1–6 · 10⁶ 표본) — scratch, 저장 안 함.
- 정본 중복 확인: papers/ 565 장 목록 · DOI `powtec.2011.10.057` · 'Wensrich' · 'Katterfeld' · 제목 낱말 ('Rolling friction as a technique' · '409–417') grep — 카드 없음 (roessler2019 · coetzee2017 · ai2011 은 인용 · 언급만).

## 🔗 관련 카드
- 이 논문을 인용한 카드: `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` (L49 · L87 · L144 · L191 · L244 — 구름마찰 모델 출처) · `coetzee2017_dem_calibration_review` (ref [84] · L50 · L162 · L611) · `ai2011_rolling_resistance_contact_models_dem` (L257 · L340 — 후속 언급).
- 같은 부류 (구름 저항 모델): `ai2011_rolling_resistance_contact_models_dem` (ref [12] · 모델 A–D · 2D).
- 우리 덱의 구름마찰 표기: `luding2008_cohesive_frictional_contact_models` (L185 μ_r) · `shenouda2020_dem_metal_powder_am_liggghts_tutorial` (cdt ↔ epsd2) · `sun2026_dem_extrusion_recirculation_dry_electrode` (L201 cdt 식) · `otani2025_dem_se_dispersion_aggregation_compression` · `nase2001_granular_bond_collision_number_wet_cohesion` (믹서 pair_style).
- 구름마찰 = 비구형 대리의 쓰임 · 보정: `hare2026_dem_pept_dry_mixing_nmc622_eirich` (μ_r 0.075) · `frankenberg2024_dem_high_intensity_mixer_assb` · `bazzoun2025_dem_parameter_sensitivity_assb_cathode` · `thakur2014_eepa_adhesive_elastoplastic_dem` · `alizadeh2018_dem_adhesion_calibration_segregation_heap` · `paulick2015_elastic_particle_properties_dem_review` · `boschpadros2014_dem_liggghts_msc_thesis` · `jadidi2023_dem_batch_solid_mixers_review`.
- 모양을 직접 푸는 쪽 · 강성 축척: `xu2023_realistic_am_shape_cgmd_calendering` · `lommen2014_dem_speedup_contact_stiffness_reduction_bulk_behavior` · `haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem` (같은 묶음 · 구름 저항 + 강성 연화).
- 이름이 비슷한 다른 것 (법선 접촉 소성): `thorntonning1998_adhesive_elastoplastic_contact`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
