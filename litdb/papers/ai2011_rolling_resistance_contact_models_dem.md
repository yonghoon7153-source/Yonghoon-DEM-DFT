<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 형식 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md
     (절 번호 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표) · 이웃 = morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis.md (이 논문을 'EDEM 기본 구름 = Model A' 로 인용)
     · roessler2019_dem_cohesive_aor_cylinder_lift_calibration.md (EPSD ↔ 우리 cdt) · luding2008_cohesive_frictional_contact_models.md (우리 압축 덱 m5 구름마찰 값).
     쪽 표기 = 학술지 쪽 p.269–282 (PDF 쪽 = 학술지 쪽 − 268 · figures.json 의 page 는 PDF 쪽).  보충 자료 (SI) 안내 없음 (14 쪽 · p.281–282 = 참고문헌 84 편).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv · 박힌 원 래스터 200 ppi 에서 프레임 선으로
     눈금 보정) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 추론] · [추정] = 이 카드의 해석 · [미확인] = 원문 (14 쪽 전수) 에 없음 ·
     [정본 카드 표기] = 우리 LIGGGHTS 덱 설정을 다른 정본 카드에서 옮긴 것 (리포 덱과의 대조는 이 카드에서 하지 않았다).
     원문 14 쪽은 텍스트 층 전수 + 쪽 렌더로 읽었고 식 22 개 번호 (27 식) 는 렌더로 대조했다. -->
# DEM 구름저항 (rolling resistance) 모델 네 부류 — A 방향 일정 토크 (Zhou 1999 형 · LIGGGHTS `cdt` 와 같은 꼴) · B 점성 · C 탄소성 스프링–대시포트 (이 논문의 일반 모델 · 되굴림 가지) · D 접촉 무관 (평형 위반 · 제외) — 2D PFC2D 기준 시험 셋 + 2D 광탄성 원판 모래더미 (실험 안식각 27°): A 는 정지하면 토크가 2Δt 주기로 뒤집혀 잔류 운동에너지 · 기어내림 (Δt 를 줄여도 안 없어짐) · B 는 정적 토크 0 · C 만 안정 — 구름저항 = 구 · 원판 DEM 이 못 담는 입자 모양 · 큰 변형 · 접촉 주변 소성 · 점착의 대리 — Ai · Chen · Rotter · Ooi (Powder Technology 2011)

> slug `ai2011_rolling_resistance_contact_models_dem` · DOI `10.1016/j.powtec.2010.09.030` · type `DEM 이론 (구름저항 모델 리뷰 · 네 부류 분류 + 일반 모델 제안) + 2D 기준 시험 (PFC2D · Hertz–Mindlin + 구름 토크 C++ 구현) + 2D 광탄성 원판 모래더미 실험 대조 — 압밀 · 기공 · 탈압 · 소성 입자 · SE · 3D 계산 없음` · PDF `247fb88f-19._Assessment_of_rolling_resistance_models_in_discrete_element_simulations.pdf` · digested `2026-11-12` · status ✅
>
> **저자**: **Jun Ai** · **Jian-Fei Chen\*** (교신) · **J. Michael Rotter** · **Jin Y. Ooi** — Institute for Infrastructure and Environment, Joint Research Institute for Civil and Environmental Engineering, School of Engineering, The University of Edinburgh (Edinburgh EH9 3JL, Scotland, U.K.) · *Powder Technology* **206** (2011) 269–282 (호 번호는 원문 PDF 에 인쇄 안 됨) · 접수 2010-03-31 · 수정 2010-08-15 · 승인 2010-09-22 · 온라인 2010-09-29 · Crown Copyright © 2010 · 연구비 EPSRC (grant GR/T23541) · Scottish Funding Council (Heriot-Watt 와의 Joint Research Institute · ERPem) · J. Ai = University of Edinburgh Scholarship (p.281).
> **이웃 카드 (링크만)**: 이 논문을 인용한 [`chibwe2020_nnsi_segregation_index`](chibwe2020_nnsi_segregation_index.md) (그 논문 ref [43] · 'CDT') · [`jadidi2023_dem_batch_solid_mixers_review`](jadidi2023_dem_batch_solid_mixers_review.md) ('원저 Ai 2011') · [`morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis`](morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis.md) ('EDEM 기본 = Model A') · 우리 덱의 구름마찰 표기 [`luding2008_cohesive_frictional_contact_models`](luding2008_cohesive_frictional_contact_models.md) · [`shenouda2020_dem_metal_powder_am_liggghts_tutorial`](shenouda2020_dem_metal_powder_am_liggghts_tutorial.md) · [`roessler2019_dem_cohesive_aor_cylinder_lift_calibration`](roessler2019_dem_cohesive_aor_cylinder_lift_calibration.md) · CDT 식 [`sun2026_dem_extrusion_recirculation_dry_electrode`](sun2026_dem_extrusion_recirculation_dry_electrode.md) · 구름마찰 = 비구형 대리의 쓰임 [`hare2026_dem_pept_dry_mixing_nmc622_eirich`](hare2026_dem_pept_dry_mixing_nmc622_eirich.md) · [`frankenberg2024_dem_high_intensity_mixer_assb`](frankenberg2024_dem_high_intensity_mixer_assb.md).
> **판독 원자료**: `litdb/figures/ai2011_rolling_resistance_contact_models_dem/digitized.csv` (1,633 행 — Fig 19 단면 4 계열 + 경사 맞춤 8 · Fig 17 · 8a · 6a · 7 · 12) · 크롭 67 장 (그림 19 + 표 1 · 식 27 · 근거 문단 20) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 구 · 원판 DEM 은 실제 입자의 모양 (비구형 · 비원형) · 큰 변형 · 접촉 주변 소성 · 점착이 만드는 구름 저항을 담지 못해 (§2 · p.270) 그 효과를 **접촉마다 한 쌍의 토크** 로 넣는데, 이 논문은 그 모델들을 네 부류 (**A 방향 일정 토크 · B 점성 · C 탄소성 스프링–대시포트 · D 접촉 무관**) 로 나누고 2D (PFC2D) 기준 시험 셋 + 2D 광탄성 원판 모래더미로 견준다 — **A** (우리 LIGGGHTS `rolling_friction cdt` 와 같은 꼴 [정본 카드 표기 · 카드 대조]) 는 정지 상태에서 토크가 매 Δt 뒤집혀 (*"a period of twice the time step"*) 잔류 운동에너지 · 기어내림 (creeping) 을 남기고 Δt 를 줄여도 *"reduced, but not eliminated"*, **B** 는 정적 토크가 0 이라 경사에서 되굴러 내려오고 원판 25 개 정착에서 뚜렷한 더미가 없으며 (*"No significant pile was formed also for Model B"*) 모래더미는 서지만 실험보다 훨씬 낮고, 되굴림 가지를 넣은 일반 **C** 만 안정 · Δt 무관 · 실험 안식각 27° 에 *"very close"* — 식 · 시험은 전부 2D 이고 3D 는 주장 한 문장뿐이다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 구 DEM 의 '모양' 한계 (질문 k) | 문장 넷 — DEM 은 원판 · 구 (또는 강체 묶음) 로 입자를 둔다 (p.269) · 준정적 계에서 구름저항은 *"particle shape (non-sphericity in 3D or non-circularity in 2D) and inter-particle bonds"* 를 대리하려 넣는다 (p.270) · 비원형성은 모든 실제 입자에 있고 *"large deformations of spheres or disks"* 에서도 생기며 *"of special importance in DEM modelling, when idealized circular or spherical particles are used"* (p.270) · 구름저항 없는 원판은 더미를 못 세운다 (시험 3 · p.278) | [인쇄] p.269–271 · 278 |
| ② 구름저항 모델의 원전 · 분류 (고른 의도) | **이 논문 = 분류 (A–D) + 일반 Model C 의 원전**.  A 부류의 대표는 Zhou et al. [17] (1999) — *"The model proposed in Zhou et al. [17] is typical"* (p.273) · DEM 에 '구름 마찰' 을 처음 넣은 것은 Sakaguchi et al. [18] (p.270) · 회전 스프링형 (C 부류 앞선 것) 은 Iwashita & Oda [11] (p.270) | [인쇄] p.270 · 273 |
| ③ 'CDT' 와의 관계 | 원문 이름 = **"directional constant torque models"** (p.273 · 279 · 280) — **'CDT' · 'constant directional torque' 낱말은 원문에 없다** (14 쪽 전수).  식 (8a) M_r = −(ω_rel/\|ω_rel\|) μ_r R_r F_n 의 꼴 = 정본 카드가 옮긴 LIGGGHTS cdt 식 (`sun2026` 식 15: τ = μ_r k_n δ_n R_ef · ω̂) 의 꼴 [카드 대조 · LIGGGHTS 소스 대조 전] | [인쇄] p.273 · [카드 대조] |
| ④ 소성 · 큰 변형 (질문 l) | 접촉 주변 소성 = 구름 소산의 *"major source"* · 에너지는 계면이 아니라 *"within the solid at the location of the maximum shear stress"* (p.270) — DEM 은 이것을 μ_r 하나 (A · B) 또는 회전 스프링 + 토크 상한 (C · *"similar to the loading-unloading stress-strain curve of an elastic perfectly plastic material"* p.274) 로 접는다.  C 의 매개변수 = μ_r · k_r (J_n 또는 θ_r^m) · η_r · f | [인쇄] p.270 · 274 |
| ⑤ 2D ↔ 3D (질문 g) | 식 · 시험 모두 2D 원판 · *"For simplicity, all formulations and examples are presented in 2D form, though the general conclusions are also applicable to 3D systems"* (p.269 초록 · 서론 두 번) — **3D 계산 0** · 3D 운동학은 Kuhn & Bagi [73–77] 로 넘김 · 비틀림 (twisting) 0 회 | [인쇄] p.269 · 272 · [카드 관찰] |
| ⑥ 압력 · 탈압 (질문 b) | **압밀 · 기공 · 압력 탈압 없음** (중력 아래 원판 굴림 · 정착 · 쌓기뿐).  '되돌림' 은 회전 방향에만 — C 의 되굴림 가지 (Fig 4 B→C→D→E) · 정지 토크를 0 으로 되돌리려면 각 θ_r^m 만큼 되굴러야 한다 (p.274) · 경사 시험에서 *"rolls back very slightly before becoming stationary"* (p.277) | [인쇄] p.274 · 277 |
| ⑦ 시간 간격 (질문 m) | A: 잔류 KE *"~10³"* (Δt 5 × 10⁻⁵ s) → *"~10"* (1 × 10⁻⁵ s) 정규화 단위 (p.278) · 진동 주기 2Δt (p.280) · C: 차이 *"well within numerical rounding errors"* (p.279) · Δt_crit = Thornton–Randall 식 (21)–(22) | [인쇄] p.275 · 278–280 |
| ⑧ 실험 대조 | 2D 광탄성 원판 3000 개 (Zuriguel et al. [83]) 의 평균 안식각 **27°** (p.280) ↔ C *"very close"* · A · B *"significantly smaller"* — 모델 각의 숫자는 원문에 없다 · 이 카드 판독: **C 27.9° / 29.4° · A 18.5° / 21.0° · B (μ_r 0.3) 16.6° / 12.9° · B (μ_r 0.8) 15.6° / 18.4°** (왼 / 오른 경사) · 더미 높이 C 0.272 m · A 0.253 → 0.219 m (기어내림) · B 0.187–0.195 m | [인쇄] p.280 · [판독] Fig 17 · 19 |
| ⑨ 저자가 적은 한계 | 매개변수가 *"often empirical and consequently very problem dependent"* (p.271) · J_n 의 이론 범위 0.25–0.5 무시 (p.273) · f = 0 고정 (p.274) · 모래더미는 겉모양 · 안식각만 견줌 (응력 · 접촉력은 [84] 박사논문) · 구름 기전 규명은 범위 밖 (p.271) · 공기 저항 등 제외 (p.270) | [인쇄] |

⛔ **한정어 (떼지 말 것)**: ① 재료 = **고무 같은 광탄성 원판** (모래더미 E 4 MPa) · 시험 원판 표 1 E **40 MPa** · ν 0.49 · ρ 1056 kg/m³ — 분말 · SE · AM 아님 ② **2D 원판** (PFC2D) ③ **중력만** — 압력 · 압밀 · 탈압 없음 ④ μ_r · θ_r^m 등은 **맞춘 값이 아니라 고른 값** (*"were chosen to be 0.8 and 0.3"* p.280) ⑤ 표 1 의 E 40 MPa 와 *"about 10% of the critical time step"* 이 식 (21)–(22) 로 맞지 않는다 (34 % [카드 산술 §3-10]) ⑥ 모델 안식각 숫자는 원문에 없다 — 위 각은 이 카드의 판독 (높이 창 · 좌우에 따라 ±2° 안팎).
⇒ **절대값 전이**: 없음 (재료 · 차원 · 하중이 모두 다르다).  옮길 수 있는 것은 (i) 구 DEM 한계의 **인용 문장** (ii) 구름 모델 부류의 **정지 거동** (A 의 Δt 의존 잔류 KE · 기어내림) — 우리 cdt 덱을 시험할 꼴 (iii) 해석 기준이 있는 **단위 시험 꼴** (경사면 원판 정지 조건 μ_r ≥ tan α · 정지 토크 m g r sin α).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-19 의 '왜' 칸)

의도 원문: *"k — 구 DEM 이 입자 모양을 담지 못해 비구형성을 구름마찰 (CDT, constant directional torque) 로 대리하는 모델의 원전 · DEM 의 "모양이 안 변한다" 한계를 인용할 문헌 후보 (jadidi2023 도 "원저 Ai 2011" 로 인용)"* — 가리킨 카드 = `chibwe2020_nnsi_segregation_index` (L273 · L790) · `jadidi2023_dem_batch_solid_mixers_review` (L99 · L544).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "구 DEM 이 입자 모양을 담지 못해" | **채움** | p.269 *"In a DEM model, a granular medium is usually treated as an assembly of 2D disks or 3D spheres [3,4], or else as clumps of these shapes made by rigidly connecting and overlapping multiple disks or spheres [5–7]."* · p.270 §2 e) *"This lack of circularity is present in all real particles … It is of special importance in DEM modelling, when idealized circular or spherical particles are used."* — 조건: 2D 원판 · 중력 · 압력 없음 |
| "비구형성을 구름마찰로 대리" | **채움 (일반 구름저항)** | p.270 *"In modelling a pseudo-static system, rolling resistance is often introduced to represent the effects on rolling of particle shape (non-sphericity in 3D or non-circularity in 2D) and inter-particle bonds. These have led to the use of terms such as "shape parameter" and "bond area parameter" [e.g., 21]."* · p.273 J_n 의 이론 범위를 무시해 *"rolling resistance arising from other sources such as out-of-roundness and adhesion"* 를 담는다 · p.279 *"a static torque can still exist due to adhesion or shape effect"* |
| "… (CDT, constant directional torque) 로 대리하는 모델" | **일부** | 'CDT' · 'constant directional torque' 낱말은 **원문에 없다** — 원문 이름은 *"directional constant torque models"* (A 부류 · 식 8a · p.273).  그리고 원문은 모양 대리를 **A 에 묶지 않는다**: 모양 효과는 *정적* 토크를 남기는데 (p.279) A 는 준정적 계에서 *"non-stop oscillating torque"* (p.279) — 정적 지지 (*"packing support"*) 에는 C 를 권한다 |
| "… 모델의 원전" | **없음 (원전 아님)** | A 부류의 대표 = Zhou et al. [17] (*Physica A* 269 (1999) 536–553) — *"The model proposed in Zhou et al. [17] is typical"* (p.273) · '구름 마찰' 을 DEM 에 처음 넣은 것 = Sakaguchi et al. [18] (1993 · 입자 기준 토크) (p.270).  **이 논문은 분류 (A–D) · 비교 시험 · 일반 Model C (되굴림 가지 + 감쇠 스위치 f) 의 원전**이다 |
| "DEM 의 '모양이 안 변한다' 한계를 인용할 문헌" | **일부** | '입자 모양이 하중에서 변하지 않는다' 는 문장 그대로는 없다.  있는 것: 이상화한 원 · 구 (p.270) · 비원형성이 *"large deformations of spheres or disks"* 에서도 생긴다 (p.270 — 강체 원판은 그 몫을 못 낸다 [카드 추론]) · 접촉 주변 소성이 구름 소산의 주원인 (p.270) · *"in conventional DEM analyses, rolling takes place without any resistance at the contacts"* (p.270 · Iwashita & Oda [11] 을 옮김) · 초기 DEM 은 더미를 세우려 회전 · 접선력을 끄거나 속도를 0 으로 되돌리는 *"arbitrary treatments"* 가 필요했다 (p.271) — '모양' 한계의 인용 근거로는 쓸 수 있고, '모양 불변 (소성 형상 변화 없음)' 의 직접 근거로는 약하다 |
| "jadidi2023 도 '원저 Ai 2011' 로 인용" — jadidi2023 L99 *"세 모델 — Model A 일정토크 / Model B 점성 / Model C 탄소성 spring-dashpot. [원저 Ai 2011] 'Model C 가 가장 적합'"* | **같은 뜻 (범위 한정어 빠짐)** | 원문은 **네 부류** (D = 접촉 무관 · *"violating equilibrium"* · 처음부터 제외 · p.274 · 280) 이고 시험한 대표 모델이 셋 (A · B · C) — '세 모델' 은 시험한 셋과 같다.  '가장 적합' ↔ 원문 *"Model C can provide stable torques and appears to work well in all the critical aspects examined in this paper"* (p.280) · *"applicable to most problems"* (p.279) · 모래더미에 *"should be the best model type for this application"* (p.280) — 범위 = 이 논문의 2D 시험 · 한 실험 |
| jadidi2023 L544 *"rolling resistance / 비구형 대리 \| 小 \| Model C (Ai 2011) · Frankenberg μ_r=0.2 선례"* | **같음** | 위와 같다 (C · 비구형 대리) |
| chibwe2020 L273–274 *"비구형성 대리로 CDT(constant directional torque) 모델 [43, Ai 2011] T_r,ij = (ω_rel/\|ω_rel\|)·μ_r·r*·\|F^N_ij\|, μ_r = 0.5"* | **일부 — 다른 점 셋** | (1) 이름 — 원문은 'directional constant torque' · 'CDT' 낱말 없음 (2) 부호 — 원문 식 (8a) 는 **−**(ω_rel/\|ω_rel\|) (회전 반대 방향) · 카드 식에는 − 가 없다 (chibwe2020 원문을 안 봤으므로 카드 옮김의 차이인지 chibwe2020 원문 표기인지 [미확인]) (3) 귀속 — 이 꼴의 원전은 Zhou et al. [17] · Ai 2011 은 그것을 A 부류로 분류 · 평가한 논문.  r* ↔ 원문 R_r = r_i r_j/(r_i + r_j) (식 5 · 평면이면 r_i) — 같은 양인지는 chibwe2020 정의에 달림 [미확인] · μ_r 0.5 는 chibwe2020 의 값 (원문 시험 0.2 · 0.3) |
| chibwe2020 L790 *"CDT rolling friction — 상수 방향 토크형 구름저항 모델 [43]. 구로 비구형성을 흉내 내는 표준 수법."* | **일부** | '구로 비구형성을 흉내 낸다' = 원문의 일반 구름저항 진술 (p.270) 과 같은 방향 · 다만 원문은 A 부류를 준정적 계에서 *"should be used with care"* (p.279) 로 적는다 — '표준 수법' 은 카드의 말 |
| (덧붙임) morrissey2013 L264 *"구름 τ_i = −μ_r · abs(f_hys) · R_i ω_i (식 4.2 · EDEM 기본 = Ai et al. 2011 의 Model A)"* · L456 서지 *"Powder Technology, 206(3): pp. 269–282"* | **꼴은 A 부류 · '(3)' 은 원문 PDF 에 없음** | 가리킨 카드 아님 (참고).  'EDEM 기본' 이라는 말은 이 논문에 없다 (원문은 EDEM v.2.1 [19] 을 '구름 마찰' 낱말 쓰임의 예로만 든다 · p.269).  호 '(3)' 은 원문 쪽 머리 · 첫 쪽에 인쇄되지 않았다 [미확인] |
| (꼭 뽑을 것) 네 부류 · 식 번호별 · 매개변수 | **채움** | §3-4 표 (식 8–20) · 크롭 `eq_08a … eq_20` |
| (꼭 뽑을 것) 일반 모델 제안 | **채움** | Model C = 스프링 + 감쇠 (식 10) · 되굴림 가지 (Fig 4) · 감쇠 스위치 f (식 17) — §3-4 |
| (꼭 뽑을 것) 기준 시험 · 해석해 · 숫자 | **일부** | 세 시험의 설정 · 결과 그림 (Fig 5–15) — **해석해는 원문에 없다** (기대 거동은 말로만).  이 카드가 정역학 · 진동 해석으로 그림 값을 대조 (§3-6 · 3-7 · [카드 산술]) |
| (꼭 뽑을 것) 2D 모래더미 | **채움 (각은 판독)** | 설정 · 매개변수 · 결과 §3-9 · 실험 27° [인쇄] · 모델 각 [판독] |
| (꼭 뽑을 것) 3D 적용 문장 · 'C 가 가장 적합' 의 근거 · 저자 한계 | **채움** | ⑤ · ⑨ · 위 jadidi2023 줄 |
| (꼭 뽑을 것) 우리 LIGGGHTS 덱의 구름마찰 설정 | **정본 카드 표기로 채움 (리포 대조 전)** | 압축 덱 `gran model hooke/hysteresis tangential history rolling_friction cdt` · `coefficientRollingFriction` AM 0.2 / 0.1 혼합 · SE–SE 0.1 · 믹서 덱 `… cohesion sjkr rolling_friction cdt` · μ_r 0.075 — §7-2 (⚠ jadidi2023 L101 은 '우리 덱은 구름마찰을 쓰지 않는다' 고 적어 다른 정본 카드와 어긋난다 — 카드 문제) |

⇒ **의도 대조 결과: 일부** — '구 DEM 은 모양을 못 담아 구름저항으로 대리한다' 의 인용 문장은 **있다** (p.269 · 270 · 271); 이 논문은 CDT (방향 일정 토크) 의 **원전이 아니다** (원전 = Zhou et al. 1999 [17] · 이 논문 = 분류 · 평가 · 일반 C 의 원전 · 'CDT' 낱말 없음); '모양이 변하지 않는다' 는 직접 문장은 **없다**.

---

## 1. 한 줄 요약
기존 DEM 의 법선 · 접선 스프링–감쇠 접촉에 **구름 저항 토크** 를 더하는 모델들을 근원 다섯 (미세 미끄럼 · 소성 · 점성 이력 · 점착 · 모양) 과 함께 정리하고 네 부류로 나눈 뒤 (A 방향 일정 토크 · B 점성 · C 탄소성 스프링–대시포트 · D 접촉 무관 = 평형 위반으로 제외), 되굴림 가지 · 감쇠 스위치를 넣은 일반 Model C 를 제안해 PFC2D 2D 원판 시험 셋 (평면 굴림 · 10° 경사 굴림 · 25 원판 정착) 과 2D 광탄성 원판 모래더미 (3000 개 · 안식각 27°) 로 견준다 — A 는 정지하면 토크가 매 Δt 부호를 바꿔 (주기 2Δt) 잔류 운동에너지 · 기어내림을 남기고 그 크기가 Δt 에 걸리며, B 는 멈춘 입자에 토크를 못 줘 경사에서 되굴러 내려오고 25 원판에서 뚜렷한 더미가 없으며 모래더미는 실험보다 훨씬 낮고, C 만 정적 지지와 에너지 소산을 함께 하며 Δt 에 둔감하다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| Jun Ai · Jian-Fei Chen\* · J. Michael Rotter · Jin Y. Ooi (University of Edinburgh) | Powder Technology 206 (2011) 269–282 · 14 쪽 (호 번호 미인쇄) | 10.1016/j.powtec.2010.09.030 | 원판 (2D) — 시험 원판 R 5 mm · t_d 6.67 mm · E 40 MPa · ν 0.49 · ρ 1056 kg/m³ (표 1) · 광탄성 원판 6.9 / 8.9 mm (E 4 MPa) · SE · AM 아님 | 리뷰 + 모델 제안 + 2D DEM 기준 시험 (PFC2D) + 2D 실험 대조 (남의 실험) |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 구름 저항의 근원과 용어 (§2 · p.269–270)
| 항목 | 원문 | 표지 · 쪽 |
|---|---|---|
| 용어 | 동적 흐름 (사태 · 용기 배출 · 쌓기 · 회전 드럼 · 공압 이송 · 스크루) 에서는 *"rolling friction"* · 준정적 계 (전단띠 · **구속 압축 (confined compression)** · 관입) 에서는 *"rolling resistance"* — 둘 다 접촉에서 *"a pair of torques"* 로 쓸 수 있어 이 논문은 모두 'rolling resistance' 로 부른다 · 정확한 정의는 범위 밖 | [인쇄] p.269–270 |
| 정의 | *"Free rolling"* = 합 접선력이 없는 운동 · 구름 저항 = 접촉 압력의 비대칭 (앞 절반이 높음) 이 만드는 짝힘 M_r | [인쇄] p.270 |
| a) 미세 미끄럼 · 마찰 [22–27] | 탄성 상수가 다른 두 물체에서 · μ_s 와 탄성 상수 차에 의존 · 보통 매우 작다 · 곡률 차에 의한 것은 대개 무시 가능 | [인쇄] p.270 |
| **b) 접촉 주변 소성 [22,28–31]** | *"Plastic deformation is a major source of energy dissipation during particle rolling contact, and is thus an important cause of rolling friction. Here the energy is not usually dissipated at the interface, but within the solid at the location of the maximum shear stress caused by the contact."* | [인쇄] p.270 · 크롭 `txt_p2_source_b_*` |
| c) 점성 이력 [28,32–39] | 점탄성 입자의 구름에서 큰 소산 · 온도 · 변형 속도에 크게 의존 | [인쇄] p.270 |
| d) 표면 점착 [40–45] | 분리 지점에서 점착 결합을 끊으며 소산 · 바깥 압력이 없어도 클 수 있다 · (서브)마이크론 입자 사이에서 가장 중요 (응집체) | [인쇄] p.270 |
| **e) 모양 효과 [20,48]** | 비구형 · 비원형 모양 · *"This lack of circularity is present in all real particles, but it can also arise from large deformations of spheres or disks"* · 엄밀히는 'rolling friction' 이 아니지만 중요한 구름 저항 근원 · *"It is of special importance in DEM modelling, when idealized circular or spherical particles are used."* | [인쇄] p.270 · 크롭 `txt_p2_source_e_*` |
| 범위 | 공기 저항 (다상) 등은 다루지 않음 · *"This paper deals only with rolling resistance arising at or around the contact points."* | [인쇄] p.270 |

### 3-2. 앞선 모델 (§3 · p.270–271) — 원문 요약 그대로
| 누구 [번호] | 무엇 | 이 논문의 평 |
|---|---|---|
| Bardet & Huang [9] | DEM 에 회전 구속을 처음 (미세 극성 효과) · 회전을 막으면 집합체의 내부 마찰각이 회전 자유일 때보다 높다 | 접촉 짝힘이 짝으로 안 나온다 (Morgan [51] 의 회전 감쇠와 같이) |
| Sakaguchi et al. [18] | DEM 에 *"rolling friction"* 개념을 처음 · 토크 = 구름 마찰 계수 × 법선력 · 사일로 막힘 (원판 아치가 보통 DEM 에서는 쉽게 무너짐) | 토크가 *"particle–based, and not based on a contact pair"* |
| Iwashita & Oda [11] (MDEM) | 전단띠의 큰 공극 · 회전 경사가 보통 수치 방법으로 재현되지 않음 — *"in conventional DEM analyses, rolling takes place without any resistance at the contacts"* · 회전 스프링 + 대시포트 + 비인장 결합 + 슬라이더 (Fig 1) · 회전 강성 ∝ 법선력 (뒤에 법선력 × 겹침 폭 [52]) | Oda & Iwashita [48]: 회전 저항은 강도를 정하는 주된 성분의 하나 · 접촉뿐 아니라 **입자 모양** 에서도 온다 |
| Tordesillas & Walsh [54] · [55] · [57] | 회전 저항 + 접촉 이방성 · 강체 펀치 압입에서 미시 · 거시 구성 응답에 큰 영향 · 힘사슬 좌굴 | 상대 회전 = 두 입자 좌표 회전의 차 |
| Jiang et al. [20] · [21] | MDEM 은 *"four artificial parameters, with three of them chosen separately by trial and error and the fourth related to particle overlap"* → 순수 미끄럼 · 순수 구름 재정의 · 접촉 폭을 나타내는 *"shape parameter"* · 결합 입자 [21] | 이 논문 운동학이 따르는 틀 (회전 반지름만 바꿈) |
| Zhou et al. [17] (첫째) | 토크 ∝ 법선력 · 방향은 상대 회전 반대 → 굵은 구로 안정한 더미 · 같은 그룹이 여러 후속 [63–68] 에 씀 | = **A 부류의 대표** (p.273) |
| Zhou et al. [17] (둘째) · Zhu & Yu [69] · Feng et al. [70] · Li et al. [56] | 토크 ∝ 상대 각속도 (점성) · 동적 구름 마찰 · 미끄럼/구름 성분 분리 | 각속도 의존 모델은 *"unsatisfactory for reproducing a stable sandpile with a realistic angle of repose [17,69]"* · Li 등은 매개변수가 많다 |
| 종합 | *"the importance of rolling resistance, particularly in DEM simulation of circular or spherical particles, has been gradually realized"* · *"the selection of parameters in some models is often empirical and consequently very problem dependent"* · 기전 규명은 범위 밖 | [인쇄] p.271 |

### 3-3. 핵심 매개변수 (§4 · p.272–273 · 식 1–7)
| 항목 | 식 · 값 | 표지 |
|---|---|---|
| 구름 저항 계수 | **μ_r = tan β** (식 1 · 무차원) — β = 구름 저항 토크가 중력 토크와 맞서는 최대 경사각 (Fig 2b).  관례적 정의는 편심 e (길이 단위) [71,72] · 많은 DEM 연구 [17,18,64–66,68,69] 가 e 를 씀 · 일부는 길이 × 무차원으로 나눔 [52,56,70] | [인쇄] p.272 · 크롭 `eq_01_*` |
| 2D 운동학 | dS_i = r_i(dθ_i + dφ) · dS_j = r_j(dθ_j − dφ) (식 2a · 2b) · dU_r = (r_j dS_i − r_i dS_j)/(r_i + r_j) · dU_s = (dS_i + dS_j)/2 (식 3a · 3b · Jiang [20]) · dθ_r = dθ_i − dθ_j (식 4) | [인쇄] p.272 |
| 회전 반지름 | **R_r = r_i r_j/(r_i + r_j)** (식 5 · 이 논문) → dθ_r = dU_r/R_r (식 6) · 평면 접촉이면 R_r = r_i (r_j = ∞ · 오목면은 r_j < 0) · Jiang et al. [20] 은 2 r_i r_j/(r_i + r_j) (평면에서 2 r_i) | [인쇄] p.272 |
| 회전 강성 k_r | (7a) k_s R_r² — Iwashita & Oda [11] · (7b) 3 k_n μ_r² R_r² — Jiang et al. [20] · **(7c) 2 J_n R_r F_n** — Bardet & Huang [78] (2D Hertz 원기둥 접촉 · J_n 이론 0.25–0.5 · 단단한 고무 원기둥 실험 ≈0.5) · *"kr has the units of a couple in all three of these models"* · (7c) 채택 · **0.25 ≤ J_n ≤ 0.5 제한은 무시** (*"permitting consideration of rolling resistance arising from other sources such as out-of-roundness and adhesion"*) | [인쇄] p.272–273 |

### 3-4. ★ 네 부류 (§5 · p.273–274 · 식 8–20)
| 부류 (원문 이름) | 식 | 매개변수 | 원문 평 |
|---|---|---|---|
| **A — Directional constant torque models** (대표 = Zhou et al. [17]) | **M_r = −(ω_rel/\|ω_rel\|) μ_r R_r F_n** (8a) · ω_rel = ω_i − ω_j (8b) — 크기 일정 · 방향은 늘 상대 회전 반대 · 접촉 짝마다 쌍으로 | μ_r (하나) | 동적 흐름 (회전 드럼) 의 소산에는 쓸 수 있으나 준정적 계에서 *"non-stop oscillating torque"* · *"should be used with care"* · Δt 가 *"sufficiently small"* (p.279) |
| **B — Viscous models** (대표 = Zhou et al. [17] 둘째) | **M_r = −μ_r R_r F_n (ω_i r_i − ω_j r_j)** (9) — 괄호 = 회전에 의한 접촉점 상대 병진 속도 | μ_r (하나 · 속도에 곱함) | 점성이 중요할 때 · *"should not be used for modelling pseudo-static systems"* (정적 토크 0) (p.279) |
| **C — Elastic-plastic spring-dashpot models** (앞선 것 = Iwashita & Oda [11] · Jiang et al. [20] · 이 논문이 일반화) | M_r = M_r^k + M_r^d (10) · ΔM_r^k = −k_r Δθ_r (11) · M^k_{r,t+Δt} = M^k_{r,t} + ΔM^k_r, \|M^k_{r,t+Δt}\| ≤ M^m_r (12) · **M_r^m = μ_r R_r F_n** (13) · θ_r^m = M_r^m/k_r (14) · θ_r^m = μ_r/(2J_n) (15) · k_r = μ_r R_r F_n/θ_r^m (16) · M^d = −C_r θ̇_r (\|M^k\| < M^m) · −f C_r θ̇_r (\|M^k\| = M^m) (17) · C_r = η_r C_r^crit (18) · C_r^crit = 2√(I_r k_r) (19) · I_r = 1/[1/(I_i + m_i r_i²) + 1/(I_j + m_j r_j²)] (20) | μ_r · k_r (J_n 또는 θ_r^m) · η_r · f (스위치) | 스프링 토크는 *"similar to the loading-unloading stress-strain curve of an elastic perfectly plastic material (Fig. 4)"* · 핵심 개선 = **되굴림 가지** (앞선 모델은 되굴림 · 반복 구름에 불완전) · f = 0 이면 감쇠는 완전 동원 전에만 (진동 방지) · f = 1 이면 늘 (물리적 점성) · **이 논문 전 계산 f = 0** · *"applicable to most problems"* (p.279) |
| **D — Contact-independent models** ([9,18,51]) | 토크가 입자 하나의 전체 회전 · 회전 속도에 의존 | — | 접촉한 두 입자에 다른 토크 → *"thus violating equilibrium"* · *"clearly deficient"* · 더 다루지 않음 (p.274) |

- 그림 4 (Spring torque of elastic-plastic spring-dashpot model) [인쇄 · 그림 안 글자]: 세로축 −M_r^k · 가로축 θ_r · O→A 기울기 k_r 로 −M_r^m 까지 · A→B 수평 (완전 동원) · B→C 기울기 k_r 로 되내림 · D→E 반대쪽 상한 · *"Dashline: rolling backwards"* — 회전 방향의 탄–완전소성 고리.
- 제안의 뜻 [카드 추론]: '탄소성' 은 **회전 자유도 하나의 토크–각 관계** 이름이다 — 입자 재료의 소성 · 법선 접촉의 소성 (Thornton–Ning · MDR 류) 과 다른 것.

### 3-5. 계산 설정 (§6.1 · p.274–275 · 표 1)
| 항목 | 값 | 표지 |
|---|---|---|
| 코드 | 상용 **PFC2D** (Itasca v.3.1 [8]) · 법선 · 접선 = PFC2D 내장 **Hertz–Mindlin** · 구름 모델 = PFC2D User Writing C++ 로 구현 | [인쇄] p.275 |
| 원판 (표 1) | 반지름 R **5 mm** · 두께 t_d **6.67 mm** · 탄성률 E **40 MPa** · 푸아송비 **0.49** · 밀도 ρ **1056 kg/m³** · 미끄럼 마찰 μ_s **0.8** · 구름 저항 μ_r **0.2** · 구름 점성 감쇠비 η_r **0.3** | [인쇄] 표 1 · 크롭 `tab_1.png` |
| Model C 회전 강성 | **J_n = 0.5** → θ_r^m = μ_r/(2J_n) = **0.2 rad (11.5°)** [카드 산술 · 식 15] | [인쇄] p.275 |
| 시간 간격 | Δt = **5 × 10⁻⁵ s**, *"which is about 10% of the critical time step Δtcrit of the system"* (따로 적지 않으면 전부) · Δt_crit = (π r_min/χ)√(ρ/G) (식 21) · χ = 0.163ν + 0.8766 (식 22) — Thornton & Randall [80] · 다른 식 비교는 Chung [82] | [인쇄] p.275 · ⚠ §3-10 |
| 중력 | 9.8 m/s² | [인쇄] p.275 |

### 3-6. 시험 1 — 평면 위 원판 하나 (Fig 5–8 · p.275–276)
설정 [인쇄]: 원판을 단단한 평면에 중력으로 정착 → 평형 뒤 병진 속도 **v₀ = 1.0 m/s** · 각속도 0 을 준다.

| 모델 | 원문 (거동) | 이 카드의 판독 · 대조 |
|---|---|---|
| A (Fig 6) | 구름 거리가 늘다 일정해짐 · 토크는 처음 일정 (식 8a) → 멈춘 뒤 **같은 크기의 + / − 를 오가며 진동** (Fig 6b · 0.509–0.512 s) — 앞으로 가던 속도가 0 이 되면 일정 토크가 원판을 거꾸로 돌리고, 회전 방향이 바뀌면 토크 방향도 바뀌어 *"stepwise oscillation"* · 접선 마찰력도 진동 · *"could inadvertently influence the numerical results in an undesirable manner"* | 토크 판 **+5.42 × 10⁻⁶ N·m** [판독 Fig 6a] = μ_r R_r F_n = 0.2 × 0.005 m × 5.42 × 10⁻³ N = **5.42 × 10⁻⁶ N·m** [카드 산술 · m = ρπR²t_d = 5.53 × 10⁻⁴ kg] · 진동 시작 t ≈ **0.508 s** [판독] · 구름 거리 ≈ **0.189 m** [판독] · Fig 6b 표지 간격 = Δt · 한 번 오르내림 ≈ 2Δt [판독 · 눈] |
| B (Fig 7) | 남는 마찰력 없이 서서히 정지 · 토크는 0 에서 빠르게 올라 꼭지 뒤 0 으로 (각속도에 비례 · 처음 각속도 0 → 처음 토크 0) | 꼭지 **3.77 × 10⁻⁶ N·m** (t ≈ 0.04 s · 선 위 끝) [판독] ↔ μ_r R_r F_n × (2/3)v₀ = **3.61 × 10⁻⁶** [카드 산술 · 미끄럼 → 순수 구름 전환 속도 2v₀/3 (원판 I = mR²/2) 가정 · 4 % 차] · 6 s 에 거리 ≈ 0.53 m [판독 · 눈] |
| C (Fig 8) | 감쇠가 최종 위치를 바꾼다 (η_r 0 · 0.3 · 1.0 · 1.5) · **η_r = 0 이면 마지막 자리에서 영구 진동** — A 와 비슷하나 주파수가 Δt 가 아니라 **k_r 과 질량** 이 정함 · 감쇠가 있으면 진폭이 줄어 0 으로 · k_r 이 크면 주파수가 높다 (Fig 8c · J_n 0.25 · 0.4 · 0.5) · *"Model C can therefore successfully simulate this test problem as long as the damping component of the rolling torque is included"* | t = 0.6 s 거리 η_r 0 / 0.3 / 1.0 / 1.5 = **0.191 (0.191–0.193 진동) / 0.182 / 0.161 / 0.148 m** [판독 Fig 8a] · η_r 0 의 진동 주기 ≈ **0.17 s** (골 0.60 · 0.77 · 0.935 s) [판독 · 눈 Fig 8b] ↔ 2π√(I_r/k_r) = **0.174 s** [카드 산술 · I_r = I + mR² = 1.5 mR² = 2.07 × 10⁻⁸ kg·m² (평면 r_j = ∞) · k_r = μ_r R_r F_n/θ_r^m = 2.71 × 10⁻⁵ N·m/rad] · J_n 0.25 · 0.4 이면 0.246 · 0.194 s [카드 산술] — Fig 8c 에서 J_n 0.25 가 가장 느리게 출렁인다 [판독 · 눈] |

### 3-7. 시험 2 — 10° 경사를 오르는 원판 (Fig 9–12 · p.276–277)
설정 [인쇄]: 경사 **α = 10°** · 원판 성질 시험 1 과 같음 · 경사 방향 중력을 끄고 법선으로 정착 → 중력 복원 + 경사 따라 **v₀ = 1.0 m/s** (각속도 0) · η_r 0.3 · **μ_r 0.2 (β = 11.3°)** → 구름 저항각이 있는 모델이면 경사에서 멈춰야 한다.

| 모델 | 원문 (거동) | 이 카드의 판독 · 대조 |
|---|---|---|
| A (Fig 10) | 꼭대기에서 같은 비현실적 진동 토크 · 겉보기로 멈춘 뒤 각속도가 아주 작은 진폭으로 **0 이 아닌 평균 (≈0.05 rad/s)** 둘레를 진동 — 매 Δt 방향이 바뀌므로 진동 빈도는 Δt 가 정하고 크기도 Δt 에 걸림 · 그 평균 때문에 원판이 *"thereafter moves down the slope at a very slow speed"* | 꼭대기 거리 ≈ 0.1043 m (0.27 s) → 1 s 에 ≈ 0.10426 m 로 계단식 감소 [판독 Fig 10c · 눈] · 각속도 0–0.097 rad/s 띠 [판독 · 눈] |
| B (Fig 11) | 올랐다가 **다시 굴러 내려온다** — 꼭대기에서 각속도 0 → 토크 0 → 막을 토크 없음 · μ_r 은 오르는 높이 · 시간만 바꿀 뿐 · *"Model B is not suitable for systems that have a static phase"* | 거리 꼭지 ≈ 0.15 m (≈0.44 s) → 1 s 에 ≈ 0 [판독 · 눈] |
| C (Fig 12 · μ_r 0.1 · 0.2 · 0.4) | μ_r 이 작으면 되굴러 내려오고 충분히 크면 멈춘다 · 꼭대기 뒤 **아주 조금 되굴러 (roll back) 멈춘다** — 중력 토크와 맞설 저항 토크를 키우는 데 필요 · 멈춘 뒤 저항 토크는 **μ_r 과 무관하게 일정** | 거리: μ_r 0.1 꼭지 **0.137 m (0.37 s)** → 0.95 s 에 0.042 m (내려옴) · 0.2 → **0.096 m 정지** (꼭지 ≈0.102 m @ ≈0.27 s [판독 · 눈] · 되굴림 ≈ 6 mm) · 0.4 → **0.067 m 정지** (꼭지 ≈0.070 m @ 0.18 s) [판독 Fig 12a] · 정지 토크 **−4.68 ~ −4.81 × 10⁻⁶ N·m** (μ_r 0.4) [판독 Fig 12b] |

★ **해석 대조 [카드 산술 — 원문에 해석해는 없다]**: 경사에 멈춘 원판의 정역학 — 접선 마찰 F_t = m g sin α · 중심에 대한 모멘트 F_t R = M_r ⇒ 필요한 정지 토크 **M_r = m g R sin α = 4.71 × 10⁻⁶ N·m** (판독 −4.7 과 같다) · 줄 수 있는 최대 = M_r^m = μ_r R F_n = μ_r R m g cos α ⇒ **정지 조건 μ_r ≥ tan α = 0.176** (= 식 1 의 β ≥ α).  μ_r 0.1 → M^m = 2.67 × 10⁻⁶ < 4.71 → 내려옴 (판독 −2.62 = 완전 동원) · 0.2 → 5.34 × 10⁻⁶ ✓ 정지 · 0.4 → 10.68 × 10⁻⁶ ✓ 정지 (Fig 12b 초기 판 ≈ +10.7 [판독 · 눈]).  A 의 일정 토크 (5.34 × 10⁻⁶) 는 필요한 4.71 × 10⁻⁶ 과 같아질 수 없어 매 Δt 넘치거나 반대로 가 평형을 못 낸다 [카드 추론].

### 3-8. 시험 3 — 원판 25 개 정착 (Fig 13–15 · p.277–279)
| 항목 | 값 | 표지 |
|---|---|---|
| 배치 | 같은 원판 **25 개** (5 층 × 5 · r = 5 mm · 50 mm × 50 mm · 층마다 r 만큼 비켜 쌓음 · *"Shifting gap = r"*) · 단단한 평면 위 | [인쇄 · 그림 안 글자] Fig 13 |
| 조건 | t = 0 에 중력으로 놓음 · 점성 접촉 감쇠 **η = η_r = 0.6** · A · B · C + 구름저항 없음 (대조) · 각각 **Δt 1.0 × 10⁻⁵ s · 5.0 × 10⁻⁵ s** | [인쇄] p.278 |
| t = 10 s 모습 (Fig 14) | A · C = 더미 · **구름저항 없음 = 거의 모든 원판이 굴러 나가 더미 없음** · B = 뚜렷한 더미 없음 (*"most of the disks still close to where they were generated (i.e. they did not roll away)"*) · Δt 가 최종 위치에 눈에 띄는 영향 (특히 B) | [인쇄] p.278 |
| 운동에너지 (Fig 15 · 정규화 단위 = 원판 하나가 1°/s 로 도는 KE) | 구름저항 없음: 꼭지 뒤 일정 (계속 굴러 소산 없음) · **A: ~10³ (Δt 5 × 10⁻⁵ s) → ~10 (Δt 1 × 10⁻⁵ s)** — *"the maximum oscillation velocity resulting from the oscillating torque decreases with the decrease of time step"* · B: 서서히 줄어 **~10⁻³** (두 Δt 차이 무시 가능) · **C: 빠르게 줄어 무시할 만함 · Δt 의 차이는 *"well within numerical rounding errors"*** | [인쇄] p.278–279 · [판독 · 눈] 구름저항 없음 ≈ 10⁸ · A ≈ 2 × 10³ / 2 × 10¹ · B ≈ 1.5–3 × 10⁻³ · C ≈ 10⁻¹⁷–10⁻¹⁹ |
| 정규화 단위의 크기 | ½ (½ m R²) (1°/s)² = **1.05 × 10⁻¹² J** → '~10³' ≈ 10⁻⁹ J [카드 산술 · I = mR²/2] | [카드 산술] |
| 결론 | *"Model C is therefore superior in its ability to form a static pile without any significant residual kinetic energy and its insensitivity to the computational time step."* | [인쇄] p.279 |

### 3-9. ★ 2D 모래더미 — 광탄성 원판 실험 (Fig 16–19 · p.279–280)
| 항목 | 값 | 표지 |
|---|---|---|
| 실험 | Zuriguel et al. [83] 의 **2D 광탄성 모래더미** · 알루미늄 틀 + 앞뒤 Perspex 판 **7.0 mm** 간격 · 원판 **3000** 개 (지름 **6.9 mm 2500 개 + 8.9 mm 500 개**) · 두께 6.67 mm · 밀도 1056 kg/m³ · **영률 4 MPa** · 호퍼 → 좁은 통로 → 단단한 평면 · 배출 ≈ 7 s · **평균 안식각 27°** | [인쇄] p.279–280 |
| 장치 치수 | 호퍼 높이 440 mm · 350 mm · 통로 폭 55 mm · 통로 길이 220 mm · 낙하 높이 350 mm | [인쇄 · 그림 안 글자] Fig 16 (350 mm 둘의 뜻은 그림 화살표로만) |
| 계산 | μ_s **0.8** · μ_r **0.3** (*"were chosen"*) · θ_r^m **0.05 (2.86°)** · Δt **2.0 × 10⁻⁵ s** (*"about 6% of the critical time step"*) · 실험 **50 s** 를 모사 · A · B · C 모두 (B 는 μ_r 0.8 도) | [인쇄] p.280 |
| 환산 | θ_r^m 0.05 ⇒ J_n = μ_r/(2θ_r^m) = **3.0** (이론 범위 0.25–0.5 밖 — 저자가 범위를 무시한다고 적은 대로) · μ_r 0.3 ⇒ β = 16.7° · 50 s ÷ 2 × 10⁻⁵ s = **2.5 × 10⁶ 걸음** · 정규화 단위 (큰 원판 8.9 mm 1°/s) = 6.6 × 10⁻¹³ J | [카드 산술] |
| 높이 (Fig 17) | B · C 는 배출 끝 뒤 곧 일정 · **A 는 KE 가 50 s 뒤에도 크고 더미가 계속 납작해짐 ('creeping')** — *"the perturbation due to the oscillating rolling frictional torque in Model A is significant even in such a small granular system"* · B 는 더미를 세우지만 (*"Models B and C produced stable piles"*) 높이가 μ_r 0.3 → 0.8 로 올려도 실험보다 *"much smaller"* · B 의 잔류 KE 도 크다 (*"The total residual kinetic energy was also large"*) · C 는 안정 · 잔류 KE 무시 가능 | [인쇄] p.280 · [판독] C **0.272 m** (일정) · A **0.253 (8.5 s) → 0.219 m (45–48 s)** · B μ_r 0.8 **0.195** · μ_r 0.3 **0.187 m** |
| 운동에너지 (Fig 18) | — | [판독 · 눈] 50 s: A ≈ 10⁶ (튐 10⁸) · B (0.8) ≈ 10¹–10² · B (0.3) ≈ 10⁰ · C ≈ 3 × 10⁻¹⁴ (≈24 s 뒤) |
| 겉모양 · 안식각 (Fig 19 · t = 50 s) | A 의 표면은 바깥쪽에서 크게 휜다 (실험 더미는 삼각형에 가깝다) · *"The angle of repose predicted by rolling resistance Models A and B was significantly smaller than the experimental value of 27°, whilst that predicted by Model C was very close to the experimental value."* · *"Model C produced satisfactory predictions for the sandpile formation in all aspects examined in this study, but Models A and B both had serious shortcomings."* | [인쇄] p.280 |
| ★ 모델 안식각 (이 카드) | **C 27.9° (왼) / 29.4° (오)** · A 18.5° / 21.0° · B (μ_r 0.3) 16.6° / 12.9° · B (μ_r 0.8) 15.6° / 18.4° — 꼭대기 높이 C ≈0.27 · A ≈0.21–0.22 · B ≈0.19 m | [판독] Fig 19 원 래스터 · 높이 창 (C 0.10–0.22 · A 0.08–0.17 · B 0.04–0.16 m) 안 점의 직선 맞춤 · 창에 따라 ±2° 안팎 (C 왼쪽 창 0.03–0.22 m 이면 26.8°) · 검은 두 곡선 (A · C) 은 색이 같아 위아래 순서로 갈랐다 (digitized.csv 머리 설명) |
| 범위 | 이 절은 겉모양 · 안식각만 견줌 — 응력 분포 · 접촉력 · 충전 구조는 Ai 박사논문 [84] | [인쇄] p.279 |

### 3-10. 원문 안의 어긋남 · 확인할 것 [카드 산술]
1. **표 1 E 40 MPa ↔ "Δt ≈ 10 % of Δt_crit"** — 식 (21)–(22) 에 표 1 (R 5 mm · ν 0.49 → χ 0.9565 · G = E/2(1+ν) = 13.4 MPa · ρ 1056) 을 넣으면 **Δt_crit = 1.46 × 10⁻⁴ s → Δt 5 × 10⁻⁵ s = 34 %**.  E 가 **4 MPa** 이면 Δt_crit = 4.61 × 10⁻⁴ s → **10.9 %** ('about 10 %' 와 맞음).  모래더미 (E 4 MPa · r_min 3.45 mm · ν 0.49 로 가정 — 모래더미 ν 는 인쇄 안 됨) 는 Δt_crit = 3.18 × 10⁻⁴ s → 2 × 10⁻⁵ s = **6.3 %** ('about 6 %' 와 맞음).  표 1 원판은 두께 6.67 mm · 밀도 1056 kg/m³ 가 광탄성 원판과 같다 ⇒ 표 1 의 '40' 이 '4' 의 오식일 가능성 [추정] — 어느 쪽인지 [미확인].  (시험 3 의 Δt 1 × 10⁻⁵ s 는 E 40 이면 6.9 % · E 4 이면 2.2 %.)
2. **식 (9) 의 차원** — 식 (1) 의 무차원 μ_r 로 읽으면 M_r = μ_r R_r F_n (ω r) 의 차원이 N·m · (m/s) = **N·m²/s** 로 토크가 아니다 → B 의 μ_r 은 s/m 단위여야 한다.  Fig 7 꼭지 (3.77 × 10⁻⁶ N·m [판독]) 는 μ_r 0.2 를 숫자 그대로 넣은 값 (3.61 × 10⁻⁶ [카드 산술]) 과 4 % 안 [추정: 숫자 그대로 넣었다].  원문은 k_r 세 식에 대해서만 *"dimensionally correct"* 라 적는다 (p.273).
3. **시험 1 · 2 의 Model C 에서 J_n = 0.5 · μ_r 0.2 ⇒ θ_r^m = 0.2 rad (11.5°)** — 모래더미의 θ_r^m 0.05 rad (2.86°) 의 네 배 [카드 산술] · 두 설정의 J_n (0.5 ↔ 3.0) 이 다르다는 말은 원문에 없다 (모래더미는 θ_r^m 를 직접 줌).
4. PDF 메타데이터 Subject 는 *"Powder Technology, 206 (2010) 269-282"* — 쪽 머리 인쇄는 **2011** (온라인 · 저작권 2010).  호 번호 '(3)' 은 원문 어디에도 인쇄되지 않았다 (다른 카드 · 후보 표의 '206(3)' 은 원문 밖 출처).

---

## 4. ★ 방법 — 계산 사슬 · 한계 진술

### 4-1. 계산 사슬 (재구성)
2D 원판 → PFC2D (Itasca 3.1) → 법선 · 접선 = 내장 Hertz–Mindlin (감쇠 · 마찰 μ_s) → **회전 자유도에 접촉 짝 토크 하나 더** (A: 식 8 · B: 식 9 · C: 식 10–20 — User Writing C++) → 명시적 시간 적분 · Δt = Δt_crit 의 ≈10 % (식 21–22 · ⚠ §3-10) → 시험 1 · 2 (원판 하나) · 시험 3 (25 개) · 모래더미 (3000 개 · 50 s) → 관측량 = 구름 거리 · 토크 · 각속도 · 총 운동에너지 · 더미 높이 · 표면 윤곽.
- **맞춘 값 없음** — 시험 매개변수는 표 1 · 모래더미 μ_s · μ_r · θ_r^m 은 *"chosen"* (p.280) · 실험 대조는 안식각 · 겉모양 한 가지.
- 계산 비용 · 시간 [미확인] (원판 수 1 · 25 · 3000 · 모래더미 2.5 × 10⁶ 걸음 [카드 산술]).

### 4-2. ★ DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM 한계를 말한 문장 (원문 그대로)**:
  - *"In a DEM model, a granular medium is usually treated as an assembly of 2D disks or 3D spheres [3,4], or else as clumps of these shapes made by rigidly connecting and overlapping multiple disks or spheres [5–7]."* (p.269)
  - *"In modelling a pseudo-static system, rolling resistance is often introduced to represent the effects on rolling of particle shape (non-sphericity in 3D or non-circularity in 2D) and inter-particle bonds."* (p.270)
  - *"This lack of circularity is present in all real particles, but it can also arise from large deformations of spheres or disks. … It is of special importance in DEM modelling, when idealized circular or spherical particles are used."* (p.270)
  - *"… in conventional DEM analyses, rolling takes place without any resistance at the contacts."* (p.270 · Iwashita & Oda [11] 의 인식을 옮김) · Sakaguchi [18]: 원판 아치는 보통 DEM 에서 *"not stable and could easily be broken"* (p.270)
  - *"In early studies using conventional DEM, special treatments or assumptions are required in a simulation to form a stable heap of particles with a finite angle of repose [17]. … Such arbitrary treatments can only have a weak basis, and may significantly distort the outcome, resulting in predictions of uncertain accuracy [17]."* (p.271)
  - 보정값이 물성이 아니라는 고백에 가까운 것: J_n 의 이론 범위를 일부러 무시해 *"out-of-roundness and adhesion"* 까지 μ_r · J_n 에 담는다 (p.273) · *"the selection of parameters in some models is often empirical and consequently very problem dependent"* (p.271) · MDEM *"three of them chosen separately by trial and error"* (p.271).
  - 입자 겹침 · 상대밀도 · 변형률의 믿을 수 있는 상한 · 접촉 독립 가정 · 조밀 영역의 과강성 = **말 없음**.
- **(ii) 소성 · 큰 변형을 계산에 넣기 어려운 이유와 우회**: 원인 진술 = 소성은 *"within the solid at the location of the maximum shear stress"* 에서 소산되고 (p.270) 큰 변형은 비원형성을 만든다 (p.270) — 강체 원판 · 구는 이 둘을 기하로 낼 수 없다 [카드 추론].  우회 = 접촉마다 **회전 토크 한 쌍** — A · B 는 μ_r 하나, C 는 회전 스프링 k_r + 상한 μ_r R_r F_n (탄–완전소성 '비유') + 감쇠 η_r (+ 스위치 f).  검증 = 2D 시험 셋 (기대 거동) + 2D 실험 하나 (안식각 27°).  비용 = 원판 3000 개 · 50 s 가 PFC2D 로 가능 (시간 [미확인]).
- **(iii) 차원**: 모든 식 (2–20) · 시험이 **2D 원판**.  3D 전이 = *"though the general conclusions are also applicable to 3D systems"* (p.269 두 번) 한 문장 — **근거 · 3D 시험 없음**.  2D · 3D 일반 모양의 운동학은 Kuhn & Bagi [73–77] 로 넘긴다 (p.272) · 3D 에만 있는 비틀림 (twisting · 회전축이 접촉 법선) 은 언급 0 회 [카드 관찰].
- **(iv) 탈압**: 압력을 다루지 않는다 — 압밀 · 기공 · 압력 제거 없음.  회전 방향의 '하중 제거' 만: C 의 되굴림 가지 (Fig 4) · *"when the contact rolling torque should reduce back to zero, the rolling angle is required to reduce by the angle θ_r^m"* (p.274) · 경사에서 작은 되굴림 뒤 정지 (p.277).

### 4-3. 기법 미니 용어집
- **구름 저항 (rolling resistance) · 구름 마찰 (rolling friction)** = 접촉한 두 입자의 *상대 회전* 에 맞서는 짝힘 (토크 한 쌍).  준정적 계는 '저항', 동적 흐름은 '마찰' 로 부르는 경향 (이 논문은 모두 '저항').
- **μ_r = tan β** (무차원 · 이 논문) ↔ **편심 e** (길이 · 관례) — 같은 이름 '구름 마찰 계수' 가 단위가 다른 두 양이다 → μ_r 값을 논문 · 코드 사이에 옮기기 전에 정의 · 회전 반지름 규약 (R_r = r_i r_j/(r_i + r_j) ↔ Jiang 의 2배) 을 먼저 맞춘다 [카드 추론].
- **방향 일정 토크 (directional constant torque · A)** = 크기 μ_r R_r F_n 은 그대로 두고 방향만 상대 회전 반대로 · 각속도가 0 을 지나면 부호가 뒤집힌다 → 정지 상태에서 매 Δt 진동.
- **탄소성 스프링–대시포트 (elastic-plastic spring-dashpot · C)** = 회전 스프링 k_r 이 상한 M^m 까지 (탄성) · 넘으면 상한에 머묾 (완전 '소성') · 되굴리면 기울기 k_r 로 내려옴 (되굴림 가지) + 회전 점성 감쇠.
- **packing support (정적 지지)** = 멈춘 입자에도 남는 토크가 아치 · 더미를 받치는 일 (C · 모양 · 점착에는 있고 B · 점성 이력에는 없음).
- **creeping (기어내림)** = A 의 끝없는 토크 진동이 계를 계속 흔들어 더미가 천천히 납작해지는 일 (모래더미 Fig 17).
- **Δt_crit (Thornton–Randall [80])** = 임계 시간 간격 (π r_min/χ)√(ρ/G) · χ = 0.163ν + 0.8766 (식 21–22 · r_min = 가장 작은 입자 반지름 · G = 전단 탄성률 · ρ = 밀도).  다른 식과의 비교는 Chung [82] 로 넘김 (p.275).

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | MDEM 접촉 모형 (법선 k_n · C_n · 비인장 결합 / 미끄럼 k_s · C_s · 슬라이더 / 구름 k_r · C_r · 회전 슬라이더) | 회전 자유도의 스프링–대시포트–슬라이더 그림 |
| 2 (a · b) | 구름 저항의 기전 (편심 e · M_r = F_n e) · 구름 저항각 β (경사) | μ_r = tan β 의 뜻 — 경사 단위 시험의 기준 |
| 3 | 두 원판의 운동학 (dS_i · dS_j · dθ · dφ) | 식 (2)–(6) |
| 4 | ★ Model C 스프링 토크 — 탄–완전소성 고리 · 되굴림 (Dashline) | 회전 방향 '하중 제거' 가지 — 압력 탈압과 다른 것 |
| 5 · 9 | 시험 1 · 2 도식 (v₀ · ω · mg · F_n · F_t · M_r · 경사 α) | 단위 시험 꼴 |
| 6 · 7 · 8 | 시험 1 — A (진동 · 0.509–0.512 s 확대) · B · C (η_r · J_n 효과) | A 의 정지 진동 · C 의 진동 주기 = k_r · 질량 [판독 대조 §3-6] |
| 10 · 11 · 12 | 시험 2 — A (작은 진동 · 0 아닌 평균 각속도) · B (되굴러 내려옴) · C (μ_r 0.1 · 0.2 · 0.4) | 정지 조건 μ_r ≥ tan α 의 수치 확인 [카드 산술 §3-7] |
| 13 · 14 · 15 | 시험 3 — 25 원판 배치 · t = 10 s 모습 · 운동에너지 (두 Δt) | 'Δt 를 줄이면 결과가 바뀌는가' 판별 꼴 |
| 16 · 17 · 18 · 19 | 모래더미 장치 · 높이 · 운동에너지 · 표면 윤곽 (t = 50 s) | 안식각 대조 [판독 §3-9] |
| 표 1 | 시험 원판 · 접촉 성질 | ⚠ E 40 MPa ↔ Δt 10 % (§3-10) |
| 식 크롭 27 장 | `eq_01` · `eq_02a` · `eq_02b` · `eq_03a` · `eq_03b` · `eq_04` … `eq_07a` · `eq_07b` · `eq_07c` · `eq_08a` · `eq_08b` · `eq_09` … `eq_22` (식 번호마다 한 장 · 400 dpi) | 보고서 DEM 접촉 절에 붙일 구름 토크 식 |
| 근거 문단 20 장 | `txt_p1_front_matter_*` (서지) · `txt_p1_p2_pseudostatic_*` · `txt_p2_source_b_*` · `txt_p2_source_e_*` · `txt_p2_iwashita_oda_*` · `txt_p3_early_dem_*` · `txt_p3_mdem_*` · `txt_p5_kr_units_*` · `txt_p5_model_a_*` · `txt_p5_p6_model_c_*` · `txt_p6_spring_torque_*` · `txt_p6_damping_term_*` · `txt_p6_model_d_*` · `txt_p7_pfc2d_*` · `txt_p10_model_a_*` · `txt_p11_model_c_superior_*` · `txt_p11_model_a_use_with_care_*` · `txt_p12_sandpile_parameters_*` · `txt_p12_fig19_profile_*` · `txt_p12_conclusions_*` | 원문 인용용 |

## 6. Post-processing ★
- **무엇을**: 구름 거리 · 토크 · 각속도 시계열 · 총 운동에너지 (정규화 · 반로그) · 더미 높이 시계열 · 표면 윤곽 · 시점 사진.
- **안 한 것**: 해석해와의 정량 비교 · 안식각의 숫자 (모델) · 응력 · 접촉력 분포 (→ [84]) · 매개변수 민감도의 체계적 표 · 3D · 계산 시간.
- **이 카드의 후처리**: 원 래스터 판독 (Fig 6a · 7 · 8a · 12 · 17 · 19 · digitized.csv 1,633 행 · 프레임 선 기준 선형 보정) · Fig 19 표면 윤곽의 경사 직선 맞춤 (높이 창 · 좌우 따로) · 정역학 (경사 정지 조건 · 정지 토크) · 회전 진동 주기 (2π√(I_r/k_r)) · Model B 꼭지 (2v₀/3) · Δt_crit (식 21–22) · 정규화 KE 단위 · 모래더미 J_n 환산.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 가지에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · 정본 카드 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 차원 · 입자 | 2D 원판 (PFC2D) · 원판 1 · 25 · 3000 개 | 3D 구 (LIGGGHTS) · AM + SE 이원 · 수만–수십만 개 | 차원 · 모양 다름 |
| 하중 | 중력만 (굴림 · 정착 · 쌓기) | 300 MPa 압축 (판) · 정착 · 판 고정 이완 · 언로딩 · 믹서 드럼 회전 | 압밀 · 탈압은 이 논문에 없다 |
| 법선 접촉 | Hertz–Mindlin (PFC2D 내장) | 압축 = `hooke/hysteresis` (Luding 계열 이력 · 18 배 연화 E_eff 1.35 GPa) · 믹서 = Hertz + SJKR [정본 카드 표기] | 다름 |
| 구름 토크 | A · B · C 비교 · C 권장 | **`rolling_friction cdt` = A 부류** (압축 · 믹서 둘 다) [정본 카드 표기 · 식 꼴 대조 §7-2] | ★ 우리가 쓰는 것이 이 논문이 준정적 계에 '주의' 라 한 부류 |
| μ_r | 0.2 (시험) · 0.3 (모래더미) · 0.8 (B 만) | 압축 AM 0.2 / 0.1 혼합 · SE–SE 0.1 · 믹서 0.075 [정본 카드 표기] | μ_r 정의 (tan β ↔ 코드의 계수) · 회전 반지름 규약이 같은지 [미확인] → 값 비교 금지 |
| 재료 상수 | 원판 E 40 / 4 MPa · ν 0.49 · ρ 1056 (고무 같은 광탄성) | DEM SE E_eff 1.35 GPa (18 배 연화 · 재배열 대리) · Heckel P_y 138 MPa · MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 | ν 0.49 는 **숫자만 같다** (그들 = 고무 원판 · 우리 MPM = 체적 강성을 살리고 전단만 무르게 한 규약) [카드 관찰] |
| 검증 | 2D 실험 안식각 27° 한 점 | 랩 표준 순수 SE 기공 10–13 % (300 MPa) · 진밀도 1.64 g/cm³ · Cronau 겹침 · Heckel | 견줄 양이 없다 |
| 시간 간격 | Δt_crit 의 ≈6–10 % (식 21–22) · A 는 Δt 에 결과가 걸림 | (우리 덱 Δt 값은 이 카드에서 확인 안 함) | ★ cdt 를 쓰는 한 Δt 의존을 감시할 이유 |

### 7-2. ★ 우리 덱의 구름마찰 설정 — 정본 카드 표기 (그 카드들이 리포 덱에서 옮겼다고 적은 것 · 이 카드는 리포 정본을 열지 않았다 → μ_r 숫자는 리포 대조 전 '확인된 값' 으로 인용하지 않는다)
| 덱 | 표기 | 출처 (정본 카드 · 줄) |
|---|---|---|
| 압축 덱 (`thin9` · real_14 계열) | `pair_style gran model hooke/hysteresis tangential history rolling_friction cdt` · `fix m5 … coefficientRollingFriction` | `shenouda2020_dem_metal_powder_am_liggghts_tutorial` L233–234 (`thin9:61` · `thin9:32–45`) · `otani2025_dem_se_dispersion_aggregation_compression` L367 |
| 압축 덱 μ_r 값 | AM 0.2 / 0.1 혼합 · SE–SE **0.1** (*"구름저항(표면거칠기/비구형 흉내)"*) | `luding2008_cohesive_frictional_contact_models` L185 (*"우리 real_14/thin9 값"*) |
| 믹서 덱 | `pair_style gran model hertz tangential history cohesion sjkr rolling_friction cdt` · μ_r **0.075** (hare2026 세트) | `nase2001_granular_bond_collision_number_wet_cohesion` L158 · `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` L191 (`scripts/make_mixer_deck.py`) |
| LIGGGHTS cdt 의 식 꼴 | τ_CDT = μ_r k_n δ_n R_ef · ω̂_{r,s} | `sun2026_dem_extrusion_recirculation_dry_electrode` L201 (그 논문 식 15) |
| LIGGGHTS 의 C 부류 이름 | `rolling_friction epsd2` (튜토리얼) · EPSD = *"구름 저항을 탄소성 스프링–대시포트로 모델 (Wensrich & Katterfeld)"* | `shenouda2020_…` L233 · `roessler2019_…` L144 |

- **대조 [카드 대조]**: cdt 식 (크기 μ_r × 탄성 법선력 × 반지름 · 방향 = 상대 회전 단위벡터) 은 이 논문 식 (8a) 의 꼴 (크기 μ_r R_r F_n · 방향 −ω_rel/\|ω_rel\|) 과 같다 ⇒ **우리 두 덱의 구름 토크는 A 부류**.  epsd 계열이 이름상 C 부류다.  LIGGGHTS 문서 · 소스가 이 논문을 원전으로 드는지 · 감쇠 · 되굴림 처리가 Model C 와 같은지는 [미확인].
- ⚠ **정본 카드끼리 어긋남**: `jadidi2023_dem_batch_solid_mixers_review` L101 *"우리 덱은 rolling resistance 를 이 축에서 논의한 적이 없다 … 비구형 대리(rolling friction) 라는 이 분야의 표준 우회로를 쓰지 않는다"* ↔ 위 다섯 카드의 `rolling_friction cdt` 표기 — 카드 문제로 보고 (이 카드는 고치지 않음).
- ★ **이 논문이 우리 쪽에 거는 질문 [카드 추론]**: 원문 §7.2 는 A 부류가 *"rotating drum"* 같은 동적 흐름의 소산에는 쓸 만하다고 하고 준정적 계에서 *"non-stop oscillating torque"* 를 경고한다 → 우리 **믹서 (회전 드럼 · 동적 흐름) 는 A 가 쓸 만한 자리**, **압축의 정착 · 판 고정 이완 · 언로딩 (준정적) 은 A 의 약점 자리**.  조밀하게 눌린 침대에서 그 진동이 결과 (기공 · 이완 · 되돌아옴) 에 얼마나 들어가는지는 이 논문으로 알 수 없다 — 크기 미측정.

### 7-3. ★ 랩 기준과 나란히 (판정 없이)
| 출처 | 재료 | 조건 | 기공 · 진밀도 |
|---|---|---|---|
| **랩 표준** | LPSCl (순수 SE) | 300 MPa | 기공 **10–13 %** · 진밀도 **1.64 g/cm³** (고정) |
| 이 논문 | 2D 광탄성 원판 (E 4 MPa) · 시험 원판 (E 40 MPa) | 중력 · 쌓기 · 압력 없음 | **없음** (기공 · 밀도 숫자 0 · 안식각 27° · 더미 높이뿐) |
- 이 줄은 "랩 표준과 다른 문헌 값" 의 자리조차 아니다 — 견줄 양이 없다.

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: DEM 이 구 · 원판 모양 때문에 잃는 회전 저항을 접촉 토크로 되돌리는 **모델 수준의 처방** 과 그 처방들의 정지 · 동적 거동 비교.
- **없는 것**: 입자 형상 변화 · 접촉 소성 · 압밀 · 수송 · 3D.  ⇒ 우리 DEM (D0) 의 '모양 대리' 매개변수 (μ_r · 모델 종류) 를 점검할 근거를 주고, MPM 쪽에는 '구름 저항은 원래 모양 · 큰 변형 · 접촉 주변 소성에서 나온다' (§2 b · e) 는 문장만 준다 — 형상을 풀어 계산하는 MPM 에서는 이 대리가 필요 없다 [카드 추론].

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  우리 덱 구름마찰 = §7-2 정본 카드 표기.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | 등록 칸 후보: DEM 결과마다 **구름 토크 모델 이름 (cdt / epsd …) · μ_r · Δt** 를 같이 적는다 — A 부류는 정지 상태 결과 (잔류 KE · 더미 모양) 가 Δt 에 걸린다 (시험 3: ~10³ → ~10 · 모래더미 기어내림) | 기공 연산자 · 기공 숫자 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 (원판 DEM) — 2D 원판 운동학 (식 2–6) · 회전 관성 I_r (식 20) 은 2D 강체 원판 시험의 기준식으로 빌릴 수 있다 | MPM 식 아님 |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 없음 (MPM 단계).  DEM 의 '부어 쌓기' 정착에는 해당: 구름 저항 없는 원 · 구는 더미 · 아치를 못 세운다 (시험 3 · p.278) — 출발 충전 상태가 구름 모델 · μ_r 에 걸린다 [카드 추론] | 압력 · 기공 없음 |
| **단계 5** (3D 복합 압밀) | 없음 | — |
| **단계 6** (탈압 · 되돌아옴) | 회전 방향 되굴림 가지 (Fig 4) 의 꼴뿐 — 압력 탈압 아님.  ★ 우리 DEM 판 고정 이완 · 언로딩이 cdt (A 부류) 위에서 돈다면 정지 상태 토크 진동이 잔류 KE · 기어내림을 보탤 수 있다 → 언로딩 판정에 'Δt 를 바꿨을 때 잔류 KE · 되돌아옴 변화' 를 한 칸 [카드 추론 · 크기 미측정] | 되돌아옴 숫자 없음 |
| **단계 7** (형상 · 피복 · 수송) | 없음.  간접: 회전 저항이 아치 · 큰 공극 · 강도에 관여한다는 앞선 연구 요약 (Iwashita & Oda · Oda & Iwashita · Bardet · p.270) → 충전 구조 → 접촉망 [추정] | 수송 없음 |
| **후보 D0** (지금 DEM) | ★★ (1) 우리 압축 · 믹서 덱은 **cdt = A 부류** [정본 카드 표기 · 식 꼴 대조] — 원문이 준정적 계에서 *"should be used with care"* 라 한 부류 (2) μ_r 은 18 배 연화 E_eff 1.35 GPa 와 **별개의 대리 매개변수** — 연화가 재배열 · 입계 미끄럼 · 미세 파괴를 대리하듯 μ_r 은 모양 · 큰 변형 · 접촉 주변 소성 · 점착 (§2 b–e) 을 대리한다 [카드 추론] (3) 우리 μ_r (AM 0.2/0.1 · SE–SE 0.1 · 믹서 0.075) 의 근거 · 보정 기록은 정본 카드에도 없다 [미확인] | 3D · 조밀 압밀에서의 크기 · 영향 [미확인] |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 회전 자유도가 있는 강체–벽 접촉의 해석 기준: 경사면 원판의 정지 조건 μ_r ≥ tan α · 정지 토크 m g R sin α (§3-7 [카드 산술]) — 접촉 규칙 회귀 시험의 꼴 | MPM 접촉 규칙 자체는 없음 |
| **후보 A · A′** (MPM 강체 AM / 입자별 속도장) | 원문 §2 e 가 말하는 근원 (모양 · 큰 변형) 과 b (접촉 주변 소성) 를 MPM 은 형상 · 변형으로 직접 푼다 → 구름 저항의 대리 매개변수가 필요 없다 [카드 추론].  단 강체 AM 끼리의 직접 접촉 (후보 A) 은 둥근 강체라 회전 저항이 기하로 생기지 않는다 [카드 추론] | MPM 계산 · 검증 없음 |
| **후보 B** (입자별 FE) | 없음 | — |
| **후보 C · C′** (MDR · 항복 캡 DEM) | ⚠ **이름 함정** — 이 논문의 'elastic-plastic spring-dashpot' 은 **회전 방향** 토크 상한이지 법선 접촉의 소성 (Thornton–Ning · MDR) 이 아니다.  대안 접촉 법칙의 '맞춘 값 수' 비교에는: A · B = μ_r 하나 · C = μ_r · k_r (J_n 또는 θ_r^m) · η_r (+ f) · MDEM = 넷 (셋은 시행착오) | 법선 소성 · 큰 겹침 한계 없음 |
| **후보 M0** (균질화 압밀) | 없음 | — |
| **U0–U6** | ★ **U2** (경사면 마찰 접촉 회귀) 쪽 — 시험 2 (10° · μ_r 0.2 → β 11.3° > α → 정지 · 정지 토크 4.71 × 10⁻⁶ N·m · μ_r 0.1 은 되굴러 내려옴) 는 정역학 기준이 있는 구름 시험 꼴 · ★ **U5** (다물체) 쪽 — 시험 3 (25 원판 정착 · 구름저항 없는 대조 팔 포함) · 그리고 U6 (해상도 수렴) 과 같은 꼴의 **시간 간격 수렴** 판별 = '결과가 Δt 에 걸리면 모델 결함' (A: ~10³ → ~10 · C: 반올림 오차 안) — 압축 · 해상도 수렴 자체는 아님 · U0 · U1 · U3 · U4 해당 없음 | 해석해 자체는 원문에 없음 (이 카드의 산술) |
| **R1–R7** | **R6** (SE 형상 변형) — 비원형성은 큰 변형에서도 생기고 (p.270) 접촉 주변 소성이 구름 소산의 주원인 (p.270) → 구 DEM 은 둘 다 μ_r 에 접는다 = R6 을 요구하는 근거 문장 후보 · **R5** (맞추는 값 하나) — C 는 넷 · MDEM 넷 중 셋은 시행착오 · 모래더미 J_n 환산 3.0 (이론 0.25–0.5 밖) — R5 와 맞서는 예 · **R2** (미끄럼 · 분리) — 구름은 미끄럼과 따로 (식 3a · 3b) · **R4** (탈압 · 되돌아옴) — 회전 되굴림만 (압력 탈압 없음) · R1 · R3 · R7 없음 | — |
| **결과 전 대조 항목** | 우리 재료 값 없음.  DEM 코드 검증용 (재료 무관): 시험 1–3 의 정역학 · 진동 대조 (§3-6 · 3-7) · 2D 광탄성 원판 안식각 27° (실험 · 원문 인쇄) | LPSCl · NCM · 압밀 값 0 |

- **재료 · 차원 · 조건 차이**: 고무 같은 광탄성 원판 (E 4 · 40 MPa) ↔ 우리 LPSCl · NCM (DEM 연화 E_eff 1.35 GPa · AM 140 GPa) · 2D ↔ 3D · 중력 쌓기 ↔ 300 MPa 압밀 · mm 원판 ↔ µm 입자 · 응집 없음 ↔ 우리 SE–SE 점착 · 맞춘 값 없음 (고른 값) ↔ 우리 E_eff 를 기공에 맞춤.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **우리 cdt 의 정지 거동을 단위 시험으로 먼저 재기** — LIGGGHTS 단일 구를 10° 경사에 굴려 (μ_r 0.2 · 시험 2 꼴) 정지하는지 · 평균 각속도가 0 인지, 25 구 정착 (시험 3 꼴) 의 잔류 KE 가 Δt 를 반으로 줄일 때 얼마나 바뀌는지를 cdt ↔ epsd2 로 견준다 — 결과 전에 '정지 조건 μ_r ≥ tan α · 잔류 KE 의 Δt 의존' 을 등록 (후보 D0 · U2 · U6) [원문 §6.3 · 6.4 · 7.2].
2. **압축 정착 · 판 고정 이완 · 언로딩 결과에 Δt 의존 칸** — A 부류 위에서 도는 한, 이완 판정 (KE 문턱) 과 되돌아옴 측정에 '같은 런을 Δt × ½ 로' 한 번 (단계 6) [원문 p.278 · 280].
3. **μ_r 은 정의 · 규약을 붙여서만 옮긴다** — tan β (무차원) ↔ 편심 e (길이) · R_r 규약 (r_i r_j/(r_i + r_j) ↔ Jiang 2 배) · 코드 (cdt ↔ epsd) 가 다르면 같은 숫자가 다른 물리다 (`roessler2019` L191 의 'μ_r 값 비교 금지' 와 같은 결론) [원문 p.272].
4. **보고서 DEM 한계 절의 문장** — '구 DEM 은 모양 · 큰 변형 · 접촉 주변 소성을 담지 못해 구름 토크로 대리하며, 그 매개변수는 경험적 · 문제 의존이다' 를 이 논문 p.270–271 로 인용 (질문 k) — 단 '형상 불변' 의 직접 근거로는 다른 카드 (`hare2026` · `morrissey2013` 등의 원문 문장) 와 함께.
5. **믹서 (회전 드럼) 와 압축 (준정적) 의 처방을 나눠 본다** — 원문 §7.2–7.4 의 쓰임 지도 (A = 동적 흐름 · C = 정적 + 동적 · B = 점성) 를 우리 두 덱에 대 보면 믹서의 cdt 는 '쓸 만한 자리', 압축의 cdt 는 '주의 자리' [카드 추론].

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In DEM, particles are idealised as discs or spheres (or rigid clumps of them); rolling resistance is introduced to represent the effects of particle shape and inter-particle bonds, and the lack of circularity of real particles 'can also arise from large deformations of spheres or disks' (Ai et al., Powder Technol. 206 (2011) 269–282, p. 270)."
- "Plastic deformation around the contact is 'a major source of energy dissipation during particle rolling contact', dissipated within the solid at the location of the maximum shear stress — a mechanism a rigid-sphere contact cannot resolve and must lump into a rolling coefficient (Ai et al. 2011, p. 270)."
- "Directional constant-torque rolling models leave a torque that flips sign every time step at rest (period 2Δt), producing residual kinetic energy and creeping collapse that are 'reduced, but not eliminated, by adopting smaller time steps' (Ai et al. 2011, p. 280; 2D PFC2D benchmarks)."
- 국문: *"구 DEM 은 입자 모양 · 큰 변형 · 접촉 주변 소성이 만드는 구름 저항을 담지 못해 접촉 토크로 대리하며, 그 매개변수 선택은 경험적이고 문제에 따라 다르다 (Ai et al. 2011, 2D)."*
- 국문: *"방향 일정 토크 (LIGGGHTS cdt 꼴) 구름 모델은 정지 상태에서 2Δt 주기로 토크가 뒤집혀 잔류 운동에너지를 남기며 Δt 를 줄여도 없어지지 않는다 (Ai et al. 2011, 2D 시험)."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **CDT 의 원전이 아니다** — A 부류의 원전 = Zhou et al. [17] (1999) · 이 논문 = 분류 · 평가 · 일반 C 의 원전 · 'CDT' 낱말 없음.
2. **2D 원판만** — 3D 는 *"also applicable"* 한 문장 (근거 · 시험 없음) · 비틀림 언급 0.
3. **재료 = 고무 같은 광탄성 원판 · mm 크기 · 중력** — 분말 · 압밀 · SE · AM 에 숫자를 옮기지 않는다.
4. **맞춘 값이 없다** — μ_r · θ_r^m · η_r 은 고른 값 · 실험 대조는 안식각 한 가지 (모델 각 숫자는 원문에 없음 · 이 카드 판독).
5. **표 1 E 40 MPa ↔ 'Δt ≈ 10 % Δt_crit'** 불일치 (34 % · E 4 MPa 이면 10.9 %) [카드 산술 §3-10].
6. **식 (9) 차원** — 무차원 μ_r 이면 토크가 아님 [카드 산술 §3-10].
7. **'Model C 가 가장 적합'** 은 이 논문의 2D 시험 · 한 실험 범위의 결론 — 일반화하지 않는다.
8. **J_n 범위 무시 · f = 0 고정** — C 의 매개변수가 '근원 여럿을 담는 맞춤 손잡이' 임을 저자가 스스로 밝힘 (p.273 · 274).
9. **시험 2 Model A 의 평균 각속도 ≈0.05 rad/s** (원문) — 판독한 거리 감소 (≈6 × 10⁻⁵ m / 0.7 s) 와 크기가 맞는지는 판독 해상도 밖 [판독 · 미확인].
10. ⚠ **판독 값** 은 원 래스터 (200 ppi) 기준 — [판독] 표지로만 인용 · 검은 두 곡선 (A · C) 은 위아래 순서로 갈랐다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 17 | Y.C. Zhou, B.D. Wright, R.Y. Yang, B.H. Xu, A.B. Yu, Rolling friction in the dynamic simulation of sandpile formation, Physica A 269 (1999) 536–553. | **A 부류 (방향 일정 토크) 의 원전** · B (각속도 비례) 도 · 더미를 세우려면 구름 마찰이 필요 (질문 k) | 없음 (papers/ ls · grep "Physica A 269") |
| 11 | K. Iwashita, M. Oda, Rolling resistance at contacts in simulation of shear band development by DEM, J. Eng. Mech. Asce 124 (1998) 285–292. | MDEM · *"rolling takes place without any resistance"* (보통 DEM) · 회전 스프링 (질문 k) | 없음 (grep "Iwashita") |
| 20 | M.J. Jiang, H.S. Yu, D. Harris, A novel discrete model for granular material incorporating rolling resistance, Comput. Geotech. 32 (2005) 340–357. | 접촉 폭 '모양 매개변수' · k_r = 3k_nμ_r²R_r² (식 7b) · MDEM 매개변수 비판 (질문 e · k) | 없음 |
| 48 | M. Oda, K. Iwashita, Study on couple stress and shear band development in granular media based on numerical simulation analyses, Int. J. Eng. Sci. 38 (2000) 1713–1740. | 회전 저항 = 강도의 주된 성분 · **입자 모양** 에서도 온다 (질문 k) | 없음 |
| 83 | I. Zuriguel, T. Mullin, J.M. Rotter, Effect of particle shape on the stress dip under a sandpile, Phys. Rev. Lett. 98 (2007) 028001. | 모래더미 실험 (안식각 27°) 의 출처 · 입자 모양 효과 (질문 k) | 없음 (grep "Zuriguel") |
| 80 | C. Thornton, C.W. Randall, Applications of theoretical contact mechanics to solid particle system simulation, Micromechanics of Granular Materials, 1988, pp. 133–142. | Δt_crit 식 (21)–(22) 의 출처 (질문 m) | 없음 |
| 78 | J.P. Bardet, Q. Huang, Rotational stiffness of cylindrical particle contacts, Proc., Second Int. Conf. on Micromechanics of Granular Media, 1993, pp. 39–43. | k_r = 2J_nR_rF_n (식 7c) · J_n 0.25–0.5 | 없음 |
| 84 | J. Ai, Particle scale and bulk scale investigation of granular piles and silos, Ph.D. The University of Edinburgh, 2010. | Model C 모래더미의 응력 · 접촉력 · 충전 구조 | 없음 |
| 22 | K.L. Johnson, Contact mechanics, Cambridge Univerisity Press, 1985. | 구름 저항의 미세 미끄럼 · 소성 근원 (원문 철자 'Univerisity' 그대로) | 없음 (`johnson1971_jkr_surface_energy_contact_elastic_solids` 는 JKR 논문 · 이 책 아님) |
| 5 · 6 | J.F. Favier, M.H. Abbaspour-Fard, M. Kremmer, A.O. Raji, Shape representation of axisymmetrical, non-spherical particles in discrete element simulation using multi-element model particles, Eng. Comput. 16 (1999) 467–480. · J.F. Favier, M.H. Abbaspour-Fard, M. Kremmer, Modeling nonspherical particles using multisphere discrete elements, J. Eng. Mech. Asce 127 (2001) 971–977. | 구름 대리 대신 **모양을 구 묶음으로** — 다른 우회 (질문 k · l) | 없음 (papers/ ls) |
- 같은 계열 · 이 논문이 인용하지 않은 후속 (다른 정본 카드가 인용): Wensrich & Katterfeld 2012 (구름 마찰로 모양 모델링 · `roessler2019` · `coetzee2017` 인용 · 후보 표 N-50) — 정본 카드 없음.

---

## [미확인] 목록
- 호 번호 (원문 PDF 에 인쇄 안 됨 · 다른 카드의 '206(3)').
- 표 1 의 E (40 MPa) 와 'Δt ≈ 10 % Δt_crit' 중 어느 쪽이 맞는지 · 모래더미의 ν.
- 계산 시간 · 하드웨어 · 시험 3 · 모래더미의 PFC2D 감쇠 설정 세부 (η 0.6 이외).
- Fig 16 의 두 '350 mm' 의 뜻 (그림 화살표만).
- LIGGGHTS cdt · epsd2 가 이 논문을 원전으로 드는지 · 구현이 식 (8) · (10)–(20) 과 같은지 (소스 대조 전).
- 우리 덱 μ_r (AM 0.2/0.1 · SE–SE 0.1 · 믹서 0.075) 의 근거 · 보정 기록 · 그리고 리포 덱의 현재 값 (이 카드는 정본 카드 표기만 옮김).
- chibwe2020 원문의 CDT 식 부호 · r* 정의.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 서지: 1저자 · 후보 표 메모 (J. Ai, J.-F. Chen, J. M. Rotter, J. Y. Ooi · 제목 · Powder Technology 206 (2011) 269–282 · DOI) = 원문 첫 쪽 · 쪽 머리와 같음 · 이름 전체 = Jun Ai · Jian-Fei Chen · J. Michael Rotter · Jin Y. Ooi · 호 '(3)' 은 원문에 없음 · PDF 메타데이터 Subject 의 연도는 2010 (인쇄 2011).  SI · 부록 안내 없음 (14 쪽 텍스트 층 전수).
- 숫자: 텍스트 층 + 쪽 렌더로 대조 — 5 mm · 6.67 mm · 40 MPa · 0.49 · 1056 kg/m³ · 0.8 · 0.2 · 0.3 (표 1) · J_n 0.5 · 5 × 10⁻⁵ s · 10 % · 0.163 · 0.8766 · 9.8 m/s² · 1.0 m/s · 0.509–0.512 s · 10° · 11.3° · 0.05 rad/s · 25 · 0.6 · 1.0 × 10⁻⁵ · 5.0 × 10⁻⁵ s · 10 s · 1°/s · ~10³ · ~10 · ~10⁻³ · 7.0 mm · 3000 · 2500 · 6.9 mm · 500 · 8.9 mm · 4 MPa · 7 s · 27° · 0.8 · 0.3 · 0.05 (2.86°) · 2.0 × 10⁻⁵ s · 6 % · 50 s · 0.25–0.5 · GR/T23541 — 전부 위치 확인.
- 'CDT' · 'constant directional' 0 회 · 'directional constant torque' 5 회 (p.273 두 번 · 279 두 번 · 280 한 번) · 'twist' · 'torsion' · 'spin' 0 회 · 'compaction' · 'porosity' 0 회 · 'confined compression' 1 회 (용어 설명 p.269).
- 판독 보정: 각 그림 원 래스터 (200 ppi) 의 프레임 선 (어두운 행 · 열) 을 축 끝 눈금으로 써 선형 환산 · 경사 시험 정지 토크 (−4.7 × 10⁻⁶) · 시험 1 토크 판 (5.42 × 10⁻⁶) · Model C 진동 주기 (0.17 s) 가 독립 산술과 맞아 보정을 확인.
- 정본 중복 확인: papers/ 목록 (`ai*` 없음) · DOI '10.1016/j.powtec.2010.09.030' · 'rolling resistance model' · 'Ai 2011' grep — 카드 없음 (chibwe2020 · jadidi2023 · morrissey2013 이 인용만).

## 🔗 관련 카드
- 이 논문을 인용한 카드: `chibwe2020_nnsi_segregation_index` (ref [43] · 'CDT') · `jadidi2023_dem_batch_solid_mixers_review` ('원저 Ai 2011' · Model C) · `morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis` ('EDEM 기본 = Model A' · 서지 '206(3)').
- 우리 덱의 구름마찰 표기: `luding2008_cohesive_frictional_contact_models` (m5 값) · `shenouda2020_dem_metal_powder_am_liggghts_tutorial` (cdt ↔ epsd2) · `otani2025_dem_se_dispersion_aggregation_compression` (pair_style) · `nase2001_granular_bond_collision_number_wet_cohesion` (믹서 pair_style) · `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` (EPSD ↔ cdt · μ_r 비교 금지) · `sun2026_dem_extrusion_recirculation_dry_electrode` (CDT 식).
- 구름마찰 = 비구형 대리의 쓰임 · 보정: `hare2026_dem_pept_dry_mixing_nmc622_eirich` (μ_r 0.075) · `frankenberg2024_dem_high_intensity_mixer_assb` (μ_r 0.2) · `bazzoun2025_dem_parameter_sensitivity_assb_cathode` (rolling friction method) · `thakur2014_eepa_adhesive_elastoplastic_dem` (EDEM 구름 · 두 구 묶음) · `alizadeh2018_dem_adhesion_calibration_segregation_heap` (구 묶음 ↔ μ_r) · `coetzee2017_dem_calibration_review` (Wensrich & Katterfeld) · `paulick2015_elastic_particle_properties_dem_review` (안식각에 마찰 · 구름 마찰의 영향) · `boschpadros2014_dem_liggghts_msc_thesis` (μ_r = e_r/R · 비틀림 마찰).
- 접촉 법칙 (법선 소성 — 이름이 비슷한 다른 것): `thorntonning1998_adhesive_elastoplastic_contact` · `morrissey2013_…` · `luding2008_…`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
