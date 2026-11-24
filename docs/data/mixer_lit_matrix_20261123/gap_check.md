# 믹서 문헌 매트릭스 — 공백 주장 G1–G4 반례 검사 (2026-11-23 · 11-24 갱신)

- 기준 (11-24): 정본 `origin/claude/friendly-meitner-lldvar` @ 커밋 `c32e89830` (N-157 끝 상태표 커밋) — 11-23 판 기준 `a65bbdb24` (litdb/papers/ 는 `d0b7bfb88` 과 같음) 의 후손 · 그 사이 기존 카드에 덧붙은 줄은 모두 카드 끝 (링크 절) 이라 11-23 판 줄 번호가 그대로 맞다
- 대상: `matrix.json` 77 행 = 카드 67 + 제목 10 (뺀 것 = `excluded.md`) — 11-23 판 76 행 (카드 53 + 제목 23) 에서 큐 13 이 카드 행이 되고 N-157 이 새 행으로 들어왔다
- 표기: `slug Lnn` = 그 카드의 줄 번호 · *"…"* = 카드에 적힌 인용 그대로 · 제목 행 근거 = **카드 전 · 제목 · 후보 표 설명 기준** (`litdb/_curation/status.tsv` · `S8_candidates.md` · `evac/tools/queue.json` 줄 번호 — 원문 · 카드로 확인한 것이 아니다) · 11-24 새 카드 행의 판정 = 그 카드 §0-2 (공백 검사) 판정을 이 표의 낱말로 옮긴 것 (`matrix.json` 의 `meta.legend.gap_notes`)
- 판정 낱말: **holds** = 쓰인 대로 선다 · **weakened** = 좁혀야 선다 · **broken** = 쓰인 대로는 무너진다
- 범위: 이 서랍 (정본 카드 + 큐) 안에서만 찾았다 — 서랍 밖 검색은 하지 않았다
- 11-24 갱신 (1저자 11-24 — litdb 새 카드 14 편 반영 · G1–G4 좁힌 판정): 판정 낱말은 그대로 두고 근거 · 좁힌 문장 · 가장 강한 반례를 고쳤다 · 절마다 '11-24 새 카드' 목록을 더했다 · 카드 전 후보는 남지 않았다

## 요약

| 주장 | 판정 | 가장 강한 반례 (카드) | 11-24 새 카드 (큐 14 편) 가 바꾼 것 |
|---|---|---|---|
| G1 | weakened · 직접 반례 없음 | `begat2004_cohesive_adhesive_balance_partII_fine_particle_delivery` L29–L30 (약학 · Λ₁₂ = 접착 ÷ 자기 응집이 '운반체 위 고른 분포 ↔ 덩어리' 를 가름) · `figueroa2009_vdw_adhesion_mixing_segregation_bond_number_phase_diagram` L80 (건식 vdW · 기하평균 결합 · 위 경계 = 논지 §2-3 판가름 수와 같은 식 · 섞임 ↔ 분리) · `li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation` L84 (젖음비 → 섞임 ↔ 분리 상 · 11 쌍 IS 변화 부호 · 액체 다리) | 섞임 ↔ 분리 쪽 반례가 카드로 섰다 (Li–McCarthy 2003 · 2005 · 2006 · Figueroa 2009 · Chaudhuri 2006 = partial) · 덮임 ↔ 뭉침을 점착 대비로 예측한 카드는 없다 · Jones 2008 = CAB ↔ 혼합 균일도 무관 (supports) |
| G2 | broken (분야를 한정하지 않으면) · 전지 · 황화물 · 같은 SE 탐침 AFM 쌍별 · 압밀 뒤 이온 경로로 좁히면 holds | `begat2004_cohesive_adhesive_balance_afm_colloid_probe` L22 (AFM 비로 혼합 결과 예측) + Part II L30 (실제 혼합으로 대조) · `jones2008_cohesive_adhesive_balance_carrier_dpi_performance_slightly_cohesive_optimum` L77 (같은 배치 AFM CAB 16 값 → 흡입 성능 · 혼합 균일도와는 무관) · `li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation` L85 (따로 잰 접촉각 → 상 · 변화 부호 11/11 · 모델 입상계) | 정면 반례 넷 (Jones 2008 · Li–McCarthy 2003 · 2005 · 2006) + 일부 (Capece 2015 · IGC → 혼합물 흐름) — 전지 · 황화물 쪽 반례는 없다 |
| G3 | weakened | `hayakawa2022_high_shear_mixer_dry_mixing_ncm523_lpscl_composite_cathode` L31 · L34 · L36 · L102 (황화물 · 칼날 rpm ↑ = SE 가 AM 에 더 붙고 벽 부착 손실도 커짐) · `chen2004_mechanofusion_dry_coating_dem_2d_host_scraper_inner_piece_collision_frequency` L73 (벽 부착 (원심) 이 법선 충돌 세기를 반으로 · 긁개 유무 · 무점착 2D) · `dave2003_dry_coating_dem_mechanofusion_hybridizer_maic_three_devices` L72 (같은 대조 + 덩어리 풀림의 낮은 속도 쪽 되튐 · rpm 단조) · `mellmann2001_transverse_bed_motion_rotating_cylinders_slumping_rolling_cascading_froude` L73 (rpm 경계 = 운동 꼴 전이 · 힘 · 모멘트 균형) | 벽 부착 ↔ 충돌 세기 대조 (Chen · Dave) · 회전 세기에 따른 방향 · 꼴 바뀜 (Li–McCarthy 2006 · Mellmann) · 회전당 혼합 (Chaudhuri · Liu) = 모두 단조 · 최적 · 맞교환 없음 → '점착 대비가 있는 계에서 rpm 축' · '한 운동 꼴 안' 으로 좁힘 |
| G4 | weakened | `mellmann2001_transverse_bed_motion_rotating_cylinders_slumping_rolling_cascading_froude` L74 (BBD = 공정 (Fr · 충전율) × 흐름 물성 상태도 · 세 재료 · 점착 축 없음) · `nase2001_granular_bond_collision_number_wet_cohesion` L31 (Co = 점착 γ × 회전 ω 한 무차원 수) · `jarray2019_cohesion_driven_mixing_segregation_drum` L144 (Bo_g 상태도) · `liu2013_wet_cohesive_particles_transverse_mixing_rotating_drum_circulation_period` L80 (rpm × 균일 γ 지도 · 차원 축 · 한 재료) · `figueroa2009_vdw_adhesion_mixing_segregation_bond_number_phase_diagram` L83 (ℜ 상태도가 액체 다리 → 건식 vdW 로 · 공정 축 없음) | Mellmann 2001 (공정 × 흐름 물성 · 세 재료) 이 반례에 가까움 · Chaudhuri 2006 은 상태도 없음 (supports — 원문 '최적 Bond 수는 규모 의존') → '점착 축을 넣은 상태도' 로 좁힘 |

---

## G1 — "AM–SE 표면의 점착 대비를 설계 변수로 써서 SE-on-AM 피복 ↔ SE–SE 응집을 예측한 연구는 없다"

**판정: weakened.**  11-24 카드 14 편 (큐 → 정본) 을 대조한 뒤에도 *덮임 ↔ 뭉침* (SE-on-AM 피복 ↔ SE–SE 응집) 을 점착 대비로 예측한 직접 반례 없음.  그러나 점착 대비로 *섞임 ↔ 분리* 상을 예측하는 해석 경계는 모델 입상계에 이미 있고 (Li–McCarthy 2003 · 2005 · 2006 액체 다리 · Figueroa 2009 건식 vdW · 기하평균 결합 — 그 위 경계가 논지 §2-3 판가름 수와 같은 식), 같은 · 다른 쌍 점착을 따로 둔 DEM (Chaudhuri 2006) 과 약학의 수 (Λ₁₂ · CAB — Begat 2004 · Jones 2008) 도 있다.  쓰인 대로는 'AM–SE' 재료 이름과 덮임 · 군집 관측량 덕에만 선다.

반례 (카드) — 11-23 판:
1. `begat2004_cohesive_adhesive_balance_partII_fine_particle_delivery` — **contradicts (개념 · 약학)**
   - L29: *"**Λ₁₂ = F^ad₁₂ / F^co₁₁** (식 4, 재료 1 = 약물 · 재료 2 = 운반체)"*
   - L30: *"salbutamol (Λ 16.88 ± 0.91) = "uniform distribution of highly dispersed … particles over the lactose surface" · budesonide (Λ 0.22 ± 0.21) = "remain agglomerated and unevenly spread" · 함량 RSD **4.2 % vs 28.1 %**"*
   - 한정 L19: *"서로 다른 두 약물의 대비 (같은 분말의 표면을 바꾼 비교가 아니다) · 혼합 조건 하나 · 운반체가 미세 lactose (중앙 9.29 µm) 라 크기비 ≈ 2–2.5"* — 대비를 스윕한 것이 아니라 두 물질 (n = 2) 비교다.
2. `begat2004_cohesive_adhesive_balance_afm_colloid_probe` L22 — **partial**: *"salbutamol sulfate–lactose 는 **접착 우세** (혼합 잘 됨 예측) · budesonide–lactose 는 **응집 우세** (분리 · 불균일 예측)"* · 단 L217 *"실제 혼합 시험은 이 논문에 없다"*.
3. `jarray2019_cohesion_driven_mixing_segregation_drum` — **partial**: L7 *"점착을 켜고 끄는 것만으로 혼합 ↔ 분리를 뒤집는다"* · L81–L82 F_AA 0.06 · 0.075 · 0.11 mN ↔ F_AB 0.028 · 0.04 · 0.06 mN — 종 사이 점착 대비가 변수 · 단 mm 유리구 · 결과 = 혼합지수 (AM 위 SE 피복 아님).
4. `lee2026_mechanical_halogen_argyrodite_drycoating` — **partial (전지 · 황화물에서 가장 가까움)**: L40 *"코팅 품질을 결정하는 것은 SE 의 이온전도도나 산화안정성이 아니라 SE 의 기계적 물성(특히 NCM 표면과의 접착일 W_ad)이다"* — 단 단일 W_ad (AM–SE ↔ SE–SE 대비 아님) · E · σ_ys 와 함께 움직임 · 결과 = 미부착 잔류 SE.  ⚠ 카드 L8 `lab: our-lab` (자체 · 공저 논문) — 반례로 쓸 때 밝힐 것.
5. `alizadeh2018_dem_adhesion_calibration_segregation_heap` — **partial**: L16 *"코팅으로 한 성분의 표면만 바꾸면 혼합 · 분리가 바뀐다"* · L28 *"Γ_코팅–비코팅 = 0.5 × Γ_코팅–코팅"* · L30 *"지나친 점착 → 미분 부착 덩어리 → 재분리 (S_n 2.58) = 최적 코팅량 존재"* — 더미 형성 (혼합기 아님) · 세제 과립.
6. `mohammadijam2014_inverse_gas_chromatography_review` L30 — **partial**: *"살부타몰 설페이트–MgSt 의 W_adh < 살부타몰 응집 W_co (응집 조절제)"* — 해석이지 혼합 결과 예측은 아님.

카드가 인용한 2 차 근거 (카드 없음 · 원문 미확인):
- Yazdani & Hashemabadi 2019 (DEM) — `jadidi2023_dem_batch_solid_mixers_review` L484: *"서로 다른 점착 입자 사이에 **입자간 점착이 없으면 균일 혼합이 달성되지 않았다**"* (jarray2019 L324 도 인용)
- Sarkar & Wassgren 2010 (DEM) — jarray2019 L326: *"점착이 더 세면 혼합을 해친다 (DEM)"*

11-24 새 카드 (큐 → 정본 카드 · 판정 = 그 카드 §0-2 를 옮김):
- `figueroa2009_vdw_adhesion_mixing_segregation_bond_number_phase_diagram` (N-110) — **partial** (카드: 반례 = 섞임 ↔ 분리 · 일부 = 덮임 ↔ 뭉침): L80 *"세로축 ϕ = √(Γ11/Γ22) = 점착 대비 (그림 2)"* · *"식 (30)–(32) 의 위 경계 ϕ = 2/(1+β) = 논지 §2-3 문턱 (§7-2)"* · 건식 vdW · 기하평균 결합 · DEM 9 케이스 IS 부호 — 한정 L41 *"DEM 만 — 실험 없음"* · 4 mm 가상 구 · 덮임 · 군집 관측량 없음 (IS = 농도 표준편차) · 크기비 0.5 에서 기본 점착으로는 둘이 반대 (L22).
- `li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy` (N-112-1) — **partial** (반례 = 섞임 ↔ 분리 · 일부 = 덮임 ↔ 뭉침): L75 *"When Bo_g1-2 > {Bo_g1-1, Bo_g2-2}, or the materials are adhesive, we expect that segregation will be limited at equilibrium."* · *"덮임 관측은 없다"* — 액체 다리 · mm 구 · 사진 정성 (L36).
- `li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation` (N-112-2) — **partial**: L84 *"Our theory would predict that all experiments should lie in either the upper left or lower right quadrants (as our critical values do)"* · 11 쌍 IS 변화 부호 + DEM 2 쌍 · 덮임 ↔ 뭉침은 말로만 (*"the smaller ones will adhere to the larger ones (a simple physical example might be sand sticking to a bowling ball)"*) · 덮임 관측량 없음.
- `li2006_cohesive_mixing_shear_cell_collision_number_phase_diagram` (N-151) — **partial**: L81 *"both ℜ1 and ℜ2 are less than 1 … favoring intimate particle mixing"* · 전단 흐름 (0.18 rps) 9 쌍 + 0.02 rps 1 쌍의 부호 = 예측 · 덮임 관측량 없음 (IS = 벽 사진 농도 표준편차).
- `chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed` (N-150) — **partial**: L92 *"we specify independently the normal contact forces between like and unlike particles"* · K_bb 150 = *"the formation of agglomerated "islands", thus hampering mixing"* — 사후 관찰 · 예측 규칙 · 문턱 없음 · 원문 '다른 쌍 점착은 늘 혼합을 돕는다' 는 K_rb = 0 짝과 견주면 서지 않는다 [카드 판정 · L92].
- `jones2008_cohesive_adhesive_balance_carrier_dpi_performance_slightly_cohesive_optimum` (N-152) — **supports** (카드: 없음 · 오히려 반대 결과): L76 *"There was no apparent relationship between content uniformity and drug-carrier CAB ratio."* — CAB 는 하류 성능 (FPD) 은 갈랐지만 혼합 균일도는 못 갈랐다 → 혼합 상태는 균일도가 아니라 AM–SE 접촉 · SE 군집으로 잰다 (L76).
- `egermann1980_ordered_vs_random_adhesion_pseudorandom_mixture_homogeneity` (N-113) — **supports** (없음): L78 *"complete but random adhesion"* — 점착 대비를 변수로 두지 않음 · 가져올 제약 = 다 붙어도 배분이 무작위면 균질도 상한 = 무작위 (Lacey M ≈ 1).

반례 후보 — **카드 전: 없음 (11-24)** — 11-23 판의 후보 (N-112 두 편 · N-110 · N-150 · N-152 · N-113) 는 모두 정본 카드가 되어 위 '11-24 새 카드' 에 판정과 함께 옮겼다 · 남은 카드 전 10 행은 11-23 제목 판정에서 이 공백의 반례 · 부분 후보가 아니었다 (다시 읽지 않음).

아직 아무도 하지 않은 것 (이 서랍 기준 · 11-24): 황화물 SE · AM 쌍에서 같은 SE 탐침으로 잰 접착 ÷ 응집 비를 변수로 두고 결과를 'SE-on-AM 피복 ↔ SE–SE 응집' 의 정량 지표 (AM–SE 접촉 분율 · 무작위 대비 SE 군집) 로 잰 연구 · 그 경계를 크기비 0.5 아래 (우리 0.11–0.25) 에서 입자 수준 (DEM) 으로 그린 연구.

**좁힌 문장 (권고)**: *"황화물 SE 복합 양극의 건식 혼합에서 AM–SE 접착 ÷ SE–SE 응집 비 (같은 SE 탐침으로 잰 값) 로 'SE 가 AM 을 덮는가 ↔ SE 끼리 뭉치는가' 를 덮임 · 군집의 정량 지표로 예측한 연구는 없다 — 점착 대비로 섞임 ↔ 분리 상을 예측하는 해석 경계는 액체 다리 (Li–McCarthy 2003 · 2005 · 2006) 와 건식 vdW · 기하평균 결합 규칙 (Figueroa 2009 — 그 위 경계가 논지 판가름 수 0.31 · 0.39 와 같은 식) 에, 쌍별 점착 DEM 은 Chaudhuri 2006 에, 같은 꼴의 수 (Λ₁₂ · CAB) 는 약학 운반체 혼합에 (Begat 2004 Part I · II · Jones 2008 — CAB 는 혼합 균일도와 무관) 이미 있고, 그 경계는 크기비 0.5 아래 (우리 0.11–0.25) 에서 아직 서지 않았다 (Figueroa 2009)."*

---

## G2 — "점착을 독립 측정 (AFM · IGC · 접촉각) 하고 그것으로 혼합 결과를 런 전에 예측한 연구는 없다"

**판정: broken (분야를 한정하지 않으면) — 전지 · 황화물 · 같은 SE 탐침 AFM 쌍별 · 압밀 뒤 이온 경로로 좁히면 holds.**  측정 → 예측의 꼴은 약학 (AFM CAB · IGC 표면 에너지 → 혼합 결과 · 흡입 성능 · 혼합물 흐름: Begat 2004 · Jones 2008 · Capece 2015) 과 모델 입상계 (따로 잰 접촉각 → 섞임 ↔ 분리 상 · 변화 부호: Li–McCarthy 2003 · 2005 · 2006) 에 이미 있다.  전지 쪽 가장 가까운 것은 여전히 사후 상관이다.

반례 (카드) — 11-23 판:
1. `begat2004_cohesive_adhesive_balance_afm_colloid_probe` L22 (위 G1-2 의 예측 문장) + `begat2004_cohesive_adhesive_balance_partII_fine_particle_delivery` L30 (실제 혼합 RSD 4.2 % vs 28.1 % · SEM) — **contradicts (약학)**.  Part II L15: 이 카드는 Part I 카드가 *"혼합 예측은 검증되지 않았다 (II 편 [미확인])"* 로 남긴 빈칸을 채운다.  ⚠ 한정: Part I L47 · Part II L49 의 접수일이 둘 다 **2004-02-20** → 예측이 혼합 시험 **전** 에 나왔는지는 확인할 수 없다.
2. `lee2026_mechanical_halogen_argyrodite_drycoating` — **partial (전지)**: L94–L95 AFM-FS (Park Systems NX-10 · 드라이룸 · **실리콘 프로브 PPP-NCHR** · W_ad = 후퇴곡선 F < 0 면적) · L230 *"R(W_ad 계산, W_ad AFM) = **+0.994**"* · L40 (W_ad 가 코팅 품질을 정함) — 측정은 독립이지만 피복과의 관계는 5 조성 **사후** 상관 · 탐침이 SE · AM 이 아님 · our-lab (L8).
3. `jarray2019_cohesion_driven_mixing_segregation_drum` — **partial**: L42 자체 제작 미세저울로 잰 떼는 힘 0.06 · 0.075 · 0.11 mN → Bo_g · ΔW 상태도 · 그러나 L284 *"**에너지 장부만으로는 결과를 예측하지 못한다 — ΔW 의 부호 역전.**"* (측정 입력이 있어도 예측력은 반대 쪽 증거).
4. `deng2021_mechanical_surface_energy_tester_bond_number` · `mohammadijam2014_inverse_gas_chromatography_review` — **partial**: 독립 측정 경로 (표면 에너지 시험기 · IGC) 는 있으나 혼합 결과 예측에 쓰지 않음 (mohammadijam2014 L168 *"없는 것: 입자 접촉 역학 · 혼합 · 압밀 · 수송"*).

카드가 인용한 2 차 근거 (카드 없음 · 원문 미확인):
- Ahfat et al. 1997, Int. J. Pharm. 156:89–95 *"Predicting mixing performance using surface energy measurements"* — begat2004 Part I L222 (제목만으로도 G2 를 그대로 반박하는 꼴)
- Cline & Dalby 2002, Pharm. Res. 19:1274–1277 *"Predicting the quality of powders for inhalation from surface energy and area"* — begat2004 Part I L223
- Tran et al. 2021, Chem. Eng. Res. Des. 165, 467–476 *"Adhesion force measurement by centrifuge technique as tool for predicting interactive mixture stability"* — deng2021 L320
- Giraud et al. 2021 (단일 성분 성질 → 혼합물 **유동성** 예측 · 혼합 결과 아님) — deng2021 L330
- 예측의 한계: Pantaleev 2017 — `jadidi2023_dem_batch_solid_mixers_review` L63 *"보정 단계에서 DEM 과 FT4 측정이 잘 맞았음에도 불구하고, 믹싱 시스템 DEM 모델은 실험 혼합속도를 정성적으로만 예측할 수 있었다"*

11-24 새 카드 (큐 → 정본 카드 · 판정 = 그 카드 §0-2 를 옮김):
- `jones2008_cohesive_adhesive_balance_carrier_dpi_performance_slightly_cohesive_optimum` (N-152) — **contradicts (정면 · 약학)**: L77 *"Table 1 = 짝 논문 [29] 의 콜로이드 탐침 AFM CAB 16 값 (같은 배치 · p.2 · p.3) → 성능 (FPD) 과 대조 → 담체별 내부 최대 (p.9)"* — 결과 = 흡입 성능 (혼합 균일도는 CAB 와 무관 · L31) · L77 *"사전 등록 · 맞춤 · 통계 검정은 없고"* (그림 비교).
- `li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy` (N-112-1) — **contradicts (모델 입상계 · 정성)**: L76 *"Fig. 1 predicts the formation of an E phase (points 2d on Fig. 1). … We therefore take identical, roughened 0.4 mm (radius) particles …"* — 따로 잰 접촉각 → 예측 상이 실험을 이끈 순서 · 힘 · 표면 에너지 측정 없음 · γ 값 없음 · min 가정 · 사진 판정.
- `li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation` (N-112-2) — **contradicts**: L85 *"The wetting angles of beads are measured by inspection of magnified images of roughly microliter sized droplets on actual particle surfaces."* → ℜ → 상 · 변화 부호 11/11 · '미리' 등록 표지 없음 · 반복 없음.
- `li2006_cohesive_mixing_shear_cell_collision_number_phase_diagram` (N-151) — **contradicts**: L82 *"The wetting angles of beads are measured by inspection of magnified images of roughly micro-liter sized droplets on actual particle surfaces"* → 정적 · 전단 두 상태도에서 상 · 부호 · γ · κ 숫자 없음 (영역 판정은 주장).
- `capece2015_multicomponent_granular_bond_number_cohesive_blend_flow_function` (N-111) — **partial (약학 · 결과 = 혼합물의 흐름)**: L78 *"Experiments would mainly serve to confirm the theoretical predictions"* · IGC γ_d → Bo_Mix → ff_c 를 혼합물 자료에 맞추지 않고 예측 — 혼합 상태는 결과가 아님 (L24 · 'well-mixed' 가정).
- supports (점착이 들어가지만 독립 측정 → 예측 아님 · DEM 쪽): `figueroa2009_vdw_adhesion_mixing_segregation_bond_number_phase_diagram` (N-110) L81 *"the particle diameter is scaled up to 4 mm (with corresponding increases in the surface energy to obtain the proper Bovdw range)"* · `chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed` (N-150) L93 *"This is just a convenient way of defining how strong cohesion is, as compared to the particle weight (i.e. 20 times the weight, 30 times the weight, etc.)"* · `liu2013_wet_cohesive_particles_transverse_mixing_rotating_drum_circulation_period` (N-153) L78 *"In the present study, the minimum separation distance was treated as a fitting parameter."* — 우리 DEM 도 같은 함정 (맞춤 매개변수가 '따로 잰 입력' 과 섞이면 '미리 예측' 이 무너진다 · L78).

반례 후보 — **카드 전: 없음 (11-24)** — 11-23 판의 후보 (N-152 · N-110 · N-111 · N-112 첫째) 는 모두 정본 카드가 되어 위 '11-24 새 카드' 에 판정과 함께 옮겼다 · 남은 카드 전 10 행은 11-23 제목 판정에서 이 공백의 반례 · 부분 후보가 아니었다 (다시 읽지 않음).

**좁힌 문장 (권고)**: *"전지 · 황화물 — 황화물 SE 복합 양극 — 에서 AM · SE 쌍의 점착을 같은 SE 탐침 AFM 으로 쌍별 (SE–SE · SE–AM · SE–코팅 AM) 독립 측정하고 그 값을 맞춤 없이 혼합 런 전에 등록해 혼합 결과 (SE 피복 ↔ SE–SE 응집) 와 압밀 뒤 이온 경로를 예측 · 검증한 연구는 없다 — 측정 → 예측의 꼴은 약학 (Begat 2004 · Jones 2008 AFM CAB → 혼합 결과 · 흡입 성능 · Capece 2015 IGC → 혼합물 흐름 · Ahfat 1997 [카드 인용]) 과 모델 입상계 (Li–McCarthy 2003 · 2005 · 2006 접촉각 → 섞임 ↔ 분리 상 · 액체 다리) 에 이미 있고, 전지 쪽 가장 가까운 것은 AFM-FS W_ad 와 잔류 SE 의 사후 상관이다 (Lee 2026 · 실리콘 탐침 · 5 조성)."*

---

## G3 — "황화물 복합체 혼합의 회전 속도 최적을 입자 수준에서 SE 탈응집 ↔ SE 벽 손실 (또는 비슷한) 상충으로 설명한 연구는 없다"

**판정: weakened.**  상충 관찰은 황화물 복합체 실험에 이미 있다 (Hayakawa 2022).  11-24 카드로 더해진 것 — 벽 부착 ↔ 충돌 세기의 입자 수준 대조 (무점착 코팅 장치 DEM · 원심 · 긁개 유무: Chen 2004 · Dave 2003), 회전 세기에 따른 방향 · 꼴 바뀜의 힘 비 설명 (Li–McCarthy 2006 · Mellmann 2001), 점착 혼합에서 빠른 회전이 회전당 낫다는 DEM 관찰 · 제안 (Chaudhuri 2006 · Liu 2013) — 은 모두 단조이고 최적 · 맞교환이 없다.  쓰인 대로 남는 것은 **점착 대비가 있는 계에서 rpm 축의 맞교환과 내부 최적** 을 **한 운동 꼴 안** 에서 입자 수준으로 보이는 것이다.

반례 (카드) — 11-23 판:
1. `hayakawa2022_high_shear_mixer_dry_mixing_ncm523_lpscl_composite_cathode` — **partial (가장 가까움)**
   - L31: *"12,500 rpm = 큰 SE 덩어리 줄고 일부 SE 가 AM 에 붙음 · 25,000 rpm = **SE 대부분이 AM 에 붙음**"*
   - L34: *"순 SE 16 → 14.0 · 13.5 · 12.2 wt% = "adhesion of the SE particles to the inner wall of the HSM" · 회전이 빠를수록 더 (p.4) → 투입 SE 의 **14.5 · 18.1 · 27.1 %** 손실 … [카드 산술 · AM 손실 0 가정]"* · L102 원문 *"the adhesion of the SE particles was more pronounced at higher rotating speeds of the chopper"*
   - L36: σ_ion 이 회전수와 무관했던 것은 *"the difference in the net SE fraction"* (분산 ↑ 과 SE 몫 ↓ 가 겹침) — 상충의 해석까지 있다.
   - 한정: L37 *"DEM · simulation · model 0 회"* · L32 Rs / Rct 101 / 32.0 → 79.3 / 19.6 → 71.0 / 13.0 (가장 빠른 25,000 rpm 이 가장 낮음 = 내부 최적 아님) · L39 회전수와 순 SE 몫이 함께 바뀜.
2. `kawaguchi2017_dry_coating_parametric_na2so4_model_se` L83 — **partial**: *"50 m/s 는 12.7 % 로 더 낮음 = 충격이 약해 덜 붙음"* (벽 부착의 속도 의존) · 모델 물질 Na₂SO₄.
3. `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` — **partial**: L160 *"≈165 mAh g−1 after an energy input of ≈500 ± 100 J g−1"* · 1000 rpm 20 min ≈90 · L185 LPSCl 결정자 *"25 nm 아래 는 용량 하락의 한 원인"* — 황화물 공정 세기의 내부 최적을 경쟁 기전으로 설명 · 단 L36 유성 볼밀 (혼합기 아님) · 볼만 DEM · 벽 손실 아님.
4. `kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable` L33 (회전수 시리즈 · 피복 γ 0.884 → 0.9998) · `frankenberg2024_dem_high_intensity_mixer_assb` L30 (최적 혼합시간 ~30 min 뒤 포화) — **partial**: DEM 응력으로 속도 → 피복을 입자 수준 설명 · 단조 · 할라이드 · 벽 손실 없음.
5. `lischka2025_dem_eirich_intensive_mixer_dry_mixing` L105 *"툴이 빠를수록 충돌률이 떨어진다 … 기전 = 원심"* · `hare2026_dem_pept_dry_mixing_nmc622_eirich` L30 *"수확체감"* — **partial**: 속도의 수확체감을 입자 수준으로 · SE 없음.
6. `tao2023_dry_mixing_degree_ptfe_fiberization_dry_nmc622_cathode` L20 (혼합 시간 10 · 30 · 60 분에서 *"30 분이 최선인 역 U 자"*) · `zhang2026_mixing_sequence_shear_speed_ptfe_fibrillation_dry_graphite_anode` L25 (5000 · 10000 · 15000 rpm 비교) — **partial**: 혼합 세기의 내부 최적 (역 U) · PTFE 섬유화 건식 전극 · SE 없음 · 정량 기전 없음.
7. 벽 손실 사례 (supports · 상충 해석 없음): `nakamura2020_dry_coating_ncm_li3ps4_core_shell` (행 card_refs L30) · `hayakawa2023_dry_coated_composite_particles_conductive_additives_ab_vgcf` (L97–L98).
8. 고강도 혼합의 다른 대가 (제외 행 · 참고): `lee2025_halide_segregation_uhs_mixing_li_chalcogen_assb` L25 — 2000 rpm 원심 혼합의 기계화학 분해 (LiX 편석) · 칼코겐 양극 · 상충 최적 아님.

11-24 새 카드 (큐 → 정본 카드 · 판정 = 그 카드 §0-2 를 옮김):
- `chen2004_mechanofusion_dry_coating_dem_2d_host_scraper_inner_piece_collision_frequency` (N-155) — **partial**: L73 *"more and more particles get attached to the chamber wall because of the centrifugal force"* · *"particles stick to the boundary during the processing, and undergo mostly rigid body rotation"* · 법선 충돌 속도 반 — rpm 은 힘을 단조로 키울 뿐 (∝ ω^≈2) · 벽 부착은 rpm 이 아니라 긁개 유무로 바꿨다 · 원심 · 무점착 2D.
- `dave2003_dry_coating_dem_mechanofusion_hybridizer_maic_three_devices` (N-156) — **partial**: L72 *"particles stick to the boundary during processing and their rotation is only rigid body rotation"* · *"when the impact takes place at a very low velocity, the agglomerate does not shatter and even rebounds"* (미보고 계산) — rpm 단조 · 최적 · 맞교환 없음.
- `mellmann2001_transverse_bed_motion_rotating_cylinders_slumping_rolling_cascading_froude` (N-154) — **partial**: L73 rpm 경계를 층 · 입자 힘 균형으로 설명 (벽 마찰 모멘트 ∝ (1 + Fr) · 들어올림 ↔ 무너짐 시간 · 이탈 · *"adhesion of a particle on the drum wall"* = 원심 고정 · 점착력 아님) — 최적 rpm · 점착 · 맞교환 없음 → 같은 꼴 안 팔끼리만 견준다 (우리 드럼 = 폭포 꼴 창 안 [카드 산술 · 범위 밖 외삽 · L33]).
- `li2006_cohesive_mixing_shear_cell_collision_number_phase_diagram` (N-151) — **partial**: L83 *"our theory predicts that the particle distribution could be manipulated by varying shearing condition and that, in this specific instance, shearing (stirring) harder will cause more segregation!"* · 6c → 6e (−6.54 → +10.47 %) · 두 속도 · 최적 없음.
- `chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed` (N-150) — **partial**: L94 *"Higher tumbler speeds transmit more shear to the system, breaking up the coherent particle bonds, resulting in better mixing"* · K 120 하나 · 세 속도 단조 · 벽 부착 · 다시 뭉침 계수 없음.
- `liu2013_wet_cohesive_particles_transverse_mixing_rotating_drum_circulation_period` (N-153) — **partial**: L79 *"suggesting that the cohesion reduces the slipping of particles against the drum so the bed turn-over time also decreases with increasing drum speed"* — 제안 (미끄럼 · 회전 시간 자료 없음) · 3 점 단조.
- `figueroa2009_vdw_adhesion_mixing_segregation_bond_number_phase_diagram` (N-110) — **supports**: L82 5 rpm 고정 · [판독] 점착 런 스냅숏의 빈 위쪽 벽에 붙은 작은 입자 (원문 논의 없음) · *"choose the degree of adhesion such that cohesive interactions are not overwhelmed by collisional forces, yet cohesion is small enough that large particle clusters are not persistent"*.

반례 후보 — **카드 전: 없음 (11-24)** — 11-23 판의 후보 (N-150 · N-153 · N-151) 는 모두 정본 카드가 되어 위 '11-24 새 카드' 에 판정과 함께 옮겼다 · 남은 카드 전 10 행은 11-23 제목 판정에서 이 공백의 반례 · 부분 후보가 아니었다 (다시 읽지 않음).

**좁힌 문장 (권고)**: *"황화물 복합 양극 건식 혼합에서, 점착 대비가 있는 계에서 rpm 축의 SE 탈응집 (AM 위 부착) ↔ SE 벽 점착 손실 맞교환과 그 내부 최적을 한 운동 꼴 안 (Mellmann 2001 의 꼴 · 우리 드럼 = 폭포 꼴 [카드 산술]) 에서 입자 수준 (점착 DEM · 끊긴 SE–SE 결합 · 벽에 붙은 SE 몫) 으로 보인 연구는 없다 — 회전 세기를 올리면 SE 탈응집과 SE 벽 부착 손실이 함께 커진다는 관찰은 있고 (Hayakawa 2022 · 모델 물질 Kawaguchi 2017), 벽 부착 ↔ 충돌 세기의 입자 수준 대조는 무점착 코팅 장치 DEM 에 (Chen 2004 · Dave 2003 — 원심 · 긁개 유무 · rpm 단조), 회전 세기에 따른 방향 · 꼴 바뀜의 힘 비 설명은 모델 입상계에 (Li–McCarthy 2006 · Mellmann 2001 · Chaudhuri 2006 · Liu 2013) 있으며, 기존 혼합기 DEM 은 할라이드 · 단조 · 벽 손실 없음이다 (Frankenberg 2024 · Kissel 2026)."*

---

## G4 — "SE 물질 사이에 옮겨 쓸 수 있는 공정 × 재료 지도 (회전 세기 × 점착 / Bond) 는 없다"

**판정: weakened.**  점착 × 회전 세기의 무차원 수 · 지도 조각은 모델 입상계에 있고 (Nase 2001 Co · Jarray 2019 Bo_g 상태도 · Liu 2013 rpm × 균일 γ · Li–McCarthy 2006 흐름 세기로 상태도 고르기), 점착 대비 (Bo 비 ℜ) 의 재료 × 재료 상태도는 점착 종류를 넘어 옮겨 갔으며 (Li–McCarthy 2003 · 2005 → Figueroa 2009), 무점착 층의 공정 (Fr · 충전율) × 흐름 물성 상태도와 그 재료 간 이전은 반례에 가깝다 (Mellmann 2001 BBD · 세 재료).  쓰인 대로 남는 것은 **점착 축을 넣은 상태도** 의 **황화물 SE 물질 사이 전이** 와 **'SE-on-AM 피복 ↔ SE–SE 응집' 결과 축** 이다.

반례 (카드) — 11-23 판:
1. `nase2001_granular_bond_collision_number_wet_cohesion` — **partial**: L31 *"Co = F_c/F_Bg = 2πRγ / (πρ_sλ²R⁴(du/dy)²) … 드럼: Co = 4γ/(ρ_sλ²R³ω²)·(δ/R_t)⁴"* · L30 *"Co 가 지배 변수 라고 제안"* — 회전 (ω) × 점착 (γ) 를 한 무차원 수로 묶어 드럼 흐름 전이를 정리 · 단 흐름 (동적 각) 이지 혼합 아님 · 액체 다리 · L31 *"λ² = 값이 주어지지 않은 상수"*.
2. `jarray2019_cohesion_driven_mixing_segregation_drum` L144 — **partial**: *"SI Fig 4 의 네 칸: Bo_g < 1 · 위 = 분리 … · 1 < Bo_g < Bo_g^c = 혼합 · Bo_g > Bo_g^c = 분리"* · 같은 줄 *"⚠ '혼합' 칸에 든 점은 case 8 하나"* — 재료 축 상태도 · 공정 축 없음 · 유리구.
3. `jadidi2023_dem_batch_solid_mixers_review` L55 · L56 — **partial**: *"F_cohesion/W_p = 0.1"* (점착이 혼합을 돕는 구간) · *"CED > 80 kJ m⁻³"* (망치는 구간) — 한 축 문턱 모음.
4. 한 재료 공정 지도 (**partial**): `kawaguchi2017_dry_coating_parametric_na2so4_model_se` (선속도 × 시간 × 게스트 비율 · 행 card_refs L22) · `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` L28 (rpm × 시간 → E_m) · `frankenberg2024_dem_high_intensity_mixer_assb` (SI · SN vs n · 행 card_refs L26–L36) · `kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable` L33 (회전수 × 시간).  (11-24: 줄인 slug 를 다 적고 행 줄을 더함)
5. 재료 축 · 재료 간 전이 · 한 SE 의 공정 × 크기 (**partial** · 지도 아님):
   - `lee2026_mechanical_halogen_argyrodite_drycoating` — SE 5 조성 (재료 축 · 행 card_refs L127–L135 물성 표) · 공정 축 없음.
   - `kawaguchi2018_dry_coating_model_se_particle_powtec` L23 — 황화물 SE 를 구할 수 없어 압분 펠릿 압입으로 *"역학 성질이 비슷하다고 본"* Na₂SO₄ 를 대리로 씀 = 재료 간 전이 규칙의 암묵 사례 · 한정 L38 (닮게 고른 압입 응답 둘도 *"12 % · 20 % ↔ 6 %"* 다름).
   - `wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode` L33 — 공정 (압출 ↔ 배치) × NCM 크기 (8.7 ↔ 3.8 µm) 에서 껍질 유무 · *"운동에너지 ∝ D³ → ≈12 배"* 어림 · 한 SE.
6. 전이 규칙 자체의 불안: `lischka2025_dem_eirich_intensive_mixer_dry_mixing` L64 (응집수 불변 → γ ∝ R*^{8/5}) · L68 그 규칙으로 실제 입경까지 밀면 *"γ_real ≈ … 6.3 × 10⁻⁵ J/m²"* = *"비물리적으로 작다"* — 점착 축을 재료 · 크기 사이에 옮기는 규칙이 아직 서 있지 않다 (G4 의 공백을 오히려 받쳐 줌).

11-24 새 카드 (큐 → 정본 카드 · 판정 = 그 카드 §0-2 를 옮김):
- `mellmann2001_transverse_bed_motion_rotating_cylinders_slumping_rolling_cascading_froude` (N-154) — **partial (반례에 가까움)**: L74 *"With the exception of limestone, the predicted boundaries are in agreement with the data"* · BBD = 공정 (Fr · 충전율) × 재료 흐름 물성 (μ_W · Θ · Θ0 · φ_i · d/D) 을 세 재료에 같은 식으로 · 규모 늘림 기준 목록 (p.269) — 없는 것 = 점착 (Bond · Co) 축 · 점착 대비 · 다분산 (*"free-flowing monodisperse"*).
- `liu2013_wet_cohesive_particles_transverse_mixing_rotating_drum_circulation_period` (N-153) — **partial**: L80 공정 × 균일 점착 지도 = rpm 3 × γ 3 (그림 6) · 충전 7 × γ 3 — 차원 축 · 한 재료 · *"It is also unclear if the current results can be extended to other systems."*
- `li2006_cohesive_mixing_shear_cell_collision_number_phase_diagram` (N-151) — **partial**: L84 공정 축 = 연속 지도가 아니라 영역 선택 (Co ≫ Bo_g → 정적 그림 · Bo_g > Co → 동적 그림) · 재료 = 유리구 하나 · *"This simple characterization measure may serve as a useful tool for controlling particle mixing in a sheared cohesive system"*.
- `li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy` (N-112-1) — **partial**: L78 상태도 = 재료 × 재료 (크기비 × 젖음비 · 밀도비 판) · *"This tool allows calculation of the scale-independent particle cohesion force in pseudostatic systems"* · 공정 축 없음.
- `li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation` (N-112-2) — **partial**: L87 같은 틀을 유리–유리 → 아크릴–유리 → 3D DEM 짝으로 옮겨 맞춤 · *"works well even down to size ratios of 0.25 (i.e., interaction probability ratios of 16 to 1)"* · 공정 축 없음.
- `figueroa2009_vdw_adhesion_mixing_segregation_bond_number_phase_diagram` (N-110) — **partial**: L83 ℜ 틀이 액체 다리 → 건식 vdW (DEM) 로 옮겨 감 · *"our predicted trends were recovered in all cases studied here simply by increasing the degree of cohesion, suggesting that this approach may be somewhat robust to device geometry"* · 공정 축 없음.
- `jones2008_cohesive_adhesive_balance_carrier_dpi_performance_slightly_cohesive_optimum` (N-152) — **partial (재료 축만)**: L79 *"Extrapolation of the available data suggests, however, that had these studies included a drug-carrier combination with a slightly cohesive CAB ratio, it might have produced the best performance"* — 다른 약물 · 장치 · 농도로 경향이 옮겨 감 (외삽) · 공정 축 없음.
- `capece2015_multicomponent_granular_bond_number_cohesive_blend_flow_function` (N-111) — **partial (재료 · 조성 축만)**: L80 *"the model parameters α and β are expected to be material independent … This should be confirmed only after a wider range of materials have been examined"* · 맞춤 밖 전분 1 종 · 공정 축 0.
- supports: `chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed` (N-150) L95 *"the optimum values of bond numbers are scale dependent"* — 상태도 없음 · 오히려 G4 의 필요성을 받친다 · `khakhar1999_chaotic_mixing_granular_2d_tumbling_mixers_flowing_layer` (N-118) L89 옮겨 가는 규칙 = 크기 (Pe) 뿐 · *"the Péclet number increases, and therefore the effectiveness of the diffusion decreases with increasing system size"* (비점착).

반례 후보 — **카드 전: 없음 (11-24)** — 11-23 판의 후보 (N-112 두 편 · N-110 · N-150 · N-153 · N-151 · N-154 · N-111) 는 모두 정본 카드가 되어 위 '11-24 새 카드' 에 판정과 함께 옮겼다 · 남은 카드 전 10 행은 11-23 제목 판정에서 이 공백의 반례 · 부분 후보가 아니었다 (다시 읽지 않음).

**좁힌 문장 (권고)**: *"공정 (회전 세기) 축에 점착 축을 넣은 상태도 — 점착 세기 · 대비 (Bo · ℜ) × 회전 세기 (Fr · Co) — 를 'SE-on-AM 피복 ↔ SE–SE 응집' 결과 축으로 세우고 그것이 실측 점착이 다른 황화물 SE 물질 사이로 옮겨 감을 보인 연구는 없다 — 무점착 층의 공정 (Fr · 충전율) × 흐름 물성 상태도와 그 재료 간 이전은 있고 (Mellmann 2001 BBD · 세 재료), 점착 대비 (Bo 비 ℜ) 의 재료 × 재료 상태도는 액체 다리에서 건식 vdW 로 옮겨 갔으며 (Li–McCarthy 2003 · 2005 → Figueroa 2009 · DEM), 공정 축은 영역 선택 (Li–McCarthy 2006 · 한 재료) · 차원 축 지도 (Liu 2013 · rpm × 균일 γ · 한 재료) · 흐름의 무차원 수 (Nase 2001 Co · Jarray 2019 Bo_g 상태도) 로만 있다."*

---

## 불확실 · 한계

1. 제목 행 10 (N-95 · N-102 · N-103 · N-114 두 편 · N-115 · N-116 · N-117 · N-127 · N-129) 은 카드 전이다 — 11-23 제목 판정에서 어느 공백의 반례 · 부분 후보도 아니었고 11-24 에 다시 읽지 않았다.  11-23 판의 제목 행 13 (N-110 · N-111 · N-112 두 편 · N-113 · N-118 · N-150–N-156) 은 11-24 에 정본 카드가 되어 카드로 다시 판정했다 — 제목 기준 판정이 카드 기준으로 바뀐 칸 = `README.md` '11-24 갱신' 표.  (11-23 판 1 항: *"제목 행 23 은 카드 전이다 — … 카드가 나오면 이 표를 다시 대조한다"* → 이번 갱신이 그 대조다.)
2. Begat 2004 의 '런 전 예측' 여부는 두 편 접수일이 같아 확인 불가 — G2 의 contradicts 는 '측정 → 예측 → 대조' 의 꼴에 대한 판정이다.  11-24 새 카드의 G2 반례 (Li–McCarthy 2003 · 2005 · 2006 · Jones 2008) 에도 '미리 등록' 표지가 없다 — 같은 꼴의 판정이다.
3. `lee2026_mechanical_halogen_argyrodite_drycoating` 는 우리 랩 논문 (카드 L8) — 반례 · 근거로 쓸 때 자기 인용임을 밝힌다.
4. 카드가 인용한 2 차 근거 (Ahfat 1997 · Cline & Dalby 2002 · Tran 2021 · Giraud 2021 · Yazdani & Hashemabadi 2019 · Sarkar & Wassgren 2010 · Pantaleev 2017) 는 원문 미확인 — 큐 후보.
5. 판정은 이 서랍 (정본 `litdb/papers/` 의 .md — 서식 · 색인 파일 포함 11-23 판 `a65bbdb24` 617 개 · 11-24 `c32e89830` 631 개 (새 카드 14) — 중 grep 후보 + 큐) 범위다.  서랍 밖 문헌은 찾지 않았다.  11-24 에는 새 카드 14 편만 더 대조했다 (기존 카드 · `excluded.md` 는 다시 훑지 않음 · 두 판 사이 새로 생긴 카드는 이 14 편뿐).
6. 11-24 새 카드 행의 G 판정은 그 카드 §0-2 판정을 이 표의 낱말로 옮긴 것이다 (규칙 = `matrix.json` `meta.legend.gap_notes`) — 카드가 '반례' 라 한 칸이 이 표에서 partial 인 곳 (G1 · 카드 = 섞임 ↔ 분리 반례 · 덮임 ↔ 뭉침 일부) 은 이 표의 G1 주장이 덮임 ↔ 뭉침이기 때문이다 · '없음' 을 supports 와 unrelated 로 가른 것은 이 표의 판단 (같은 주제면 supports).
7. N-157 `damore2022_lpscl_symmetry_breaking_surface_energy_wulff_pbe0` (D'Amore 2022 · LPSCl 표면 에너지 DFT) 는 네 공백 판정을 바꾸지 않는다 (카드 §0-2 = 네 칸 모두 없음 · L67–L70).  우리 쪽 함의 (카드 산술 · 카드 §7-3 · 측정 아님): 청정 · 0 K 두 면 평균 γ_S (0.291–0.344 J/m² · 면적 가중 ≈0.296) 를 다른 정본 카드의 청정 DFT AM 면과 짝지은 γ_A/γ_S 0.58–6.8 은 판가름 수 0.31 (논지 §2-8) 위 = 청정 표면끼리면 SE 가 AM 을 덮는 쪽 — 논지 P1 의 조건 (실제 AM 표면 γ_A ≪ 청정 DFT) 을 드러낼 뿐 판가름 수를 정하지 않는다 (총 표면 에너지 ≠ 점착 일 W · 기하평균 결합 규칙은 분산 성분에 세운 규칙 · 카드 L302–L303).
8. 이 파일은 11-23 판을 같은 폴더에서 고친 것이다 (`README.md` '11-24 갱신') — 11-23 판 = git 이력 (이 폴더 · 커밋 `9012b2492`).
