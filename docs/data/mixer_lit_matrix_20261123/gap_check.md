# 믹서 문헌 매트릭스 — 공백 주장 G1–G4 반례 검사 (2026-11-23)

- 기준: 정본 `origin/claude/friendly-meitner-lldvar` @ `a65bbdb24` (litdb/papers/ 는 `d0b7bfb88` 과 같음 — 바뀐 것은 `_curation` 뿐)
- 대상: `matrix.json` 76 행 = 카드 53 + 제목 23 (뺀 것 = `excluded.md`)
- 표기: `slug Lnn` = 그 카드의 줄 번호 · *"…"* = 카드에 적힌 인용 그대로 · 제목 행 근거 = **카드 전 · 제목 · 후보 표 설명 기준** (`litdb/_curation/status.tsv` · `S8_candidates.md` · `evac/tools/queue.json` 줄 번호 — 원문 · 카드로 확인한 것이 아니다)
- 판정 낱말: **holds** = 쓰인 대로 선다 · **weakened** = 좁혀야 선다 · **broken** = 쓰인 대로는 무너진다
- 범위: 이 서랍 (정본 카드 + 큐) 안에서만 찾았다 — 서랍 밖 검색은 하지 않았다

## 요약

| 주장 | 판정 | 가장 강한 반례 (카드) | 가장 강한 반례 후보 (카드 전 · 제목 · 후보 표 설명 기준) |
|---|---|---|---|
| G1 | weakened | `begat2004_cohesive_adhesive_balance_partII_fine_particle_delivery` L29–L30 (약학 · Λ₁₂ = 접착 ÷ 자기 응집이 '운반체 위 고른 분포 ↔ 덩어리' 를 가름) | N-112 두 편 (Li–McCarthy 2003 PRL · 2005 PRE) · N-110 Figueroa 2009 · N-150 Chaudhuri 2006 |
| G2 | broken (분야를 한정하지 않으면) · 전지 · 황화물로 좁히면 holds | `begat2004_cohesive_adhesive_balance_afm_colloid_probe` L22 (AFM 비로 혼합 결과 예측) + Part II L30 (실제 혼합으로 대조) | N-152 Jones 2008 (AFM CAB → 16 제형) |
| G3 | weakened | `hayakawa2022_high_shear_mixer_dry_mixing_ncm523_lpscl_composite_cathode` L31 · L34 · L36 · L102 (황화물 · 칼날 rpm ↑ = SE 가 AM 에 더 붙고 벽 부착 손실도 커짐) | N-150 Chaudhuri 2006 · N-153 Liu 2013 (점착 × 회전 속도) |
| G4 | weakened | `nase2001_granular_bond_collision_number_wet_cohesion` L31 (Co = 점착 γ × 회전 ω 한 무차원 수) · `jarray2019_cohesion_driven_mixing_segregation_drum` L144 (Bo_g 상태도) | N-112 둘째 (PRE 2005 상태도) · N-150 Chaudhuri 2006 |

---

## G1 — "AM–SE 표면의 점착 대비를 설계 변수로 써서 SE-on-AM 피복 ↔ SE–SE 응집을 예측한 연구는 없다"

**판정: weakened.**  쓰인 대로는 'AM–SE' 라는 재료 이름 덕에만 선다.  개념 — *손님–숙주 접착 ÷ 손님 자기 응집* 이 *숙주 표면에 고르게 붙음 ↔ 손님끼리 덩어리* 를 가른다 — 은 약학 운반체 혼합에서 이미 수로 이름 붙고 (Λ₁₂ · CAB) 결과와 대조됐다.  전지 쪽에는 부분 반례만 있다.

반례 (카드):
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

반례 후보 — **카드 전 · 제목 · 후보 표 설명 기준** (가장 강한 것부터):
- **N-112 첫째** · Li & McCarthy 2003, PRL 90, 184301 *"Controlling Cohesive Particle Mixing and Segregation"* (status.tsv L118 = 지금 카드 작성 중 '도는 중') — queue.json N-112-1 메모: *"입상 Bond 수의 정의 (쌍별 Bo_ij) · 상태도의 축 · 혼합 ↔ 분리 경계 식 · 실험 (습윤 · 입자 크기 · 밀도 · 접촉각)"* · S8 L148 *"점착으로 분리 조절 · 점착 혼합 상태도 (Bo 축)"* → 쌍별 점착으로 혼합 ↔ 분리를 '조절' = 점착 대비를 설계 변수로 쓴 꼴.  한정 (같은 메모): *"액체 다리 (습윤) 점착이지 건식 vdW 가 아니라는 한계"*.
- **N-112 둘째** · Li & McCarthy 2005, PRE 71, 021305 *"Phase diagrams for cohesive particle mixing and segregation"* (status.tsv L119) — queue.json N-112-2 메모: *"입자 수준 점착 모델 · 상태도 (혼합 / 분리 상) · 경계가 역학 · 표면 성질로 정해지는 식"*.
- **N-110** · Figueroa, Li, McCarthy 2009, Powder Technol. 195, 203–212 *"Predicting the impact of adhesive forces on particle mixing and segregation"* (status.tsv L116 · S8 L146 · alizadeh2018 L268) — 제목 자체가 '점착력 → 혼합 · 분리 예측'.
- **N-150** · Chaudhuri et al. 2006, Powder Technol. 165, 105–114 (S8 L286): *"다른 크기 이원계는 같은 · 다른 크기 쌍 힘의 상대 크기로 혼합 무늬가 달라짐"* — 같은 쌍 ↔ 다른 쌍 힘의 대비 · S8 이 이미 *"G1 · G4 반례 후보"* 로 적음.
- N-152 · Jones et al. 2008 (S8 L288) — AFM CAB 로 16 제형 (약학) · N-113 · Egermann 1980 (제목 = PDF 파일명 *"Effects of adhesion on mixing homogeneity part I ordered adhesion random adhesion"*).

아직 아무도 하지 않은 것 (이 서랍 기준): 황화물 SE · AM 쌍에서 같은 SE 탐침으로 잰 접착 ÷ 응집 비를 변수로 두고 결과를 'SE-on-AM 피복률 ↔ SE–SE 응집' 의 정량 지표로 잰 연구 · 그 경계를 점착 크기 × 회전 속도 위에 입자 수준 (DEM) 으로 그린 연구.

**좁힌 문장 (권고)**: *"황화물 SE 복합 양극의 건식 혼합에서, 같은 SE 탐침으로 잰 AM–SE 접착 ÷ SE–SE 응집 비가 'SE 가 AM 을 덮는가 ↔ SE 끼리 뭉치는가' 를 가르는 경계를 점착 크기 × 회전 속도 위에서 입자 수준으로 그리고 그 비를 측정 입력으로 쓴 연구는 없다 — 같은 꼴의 수 (CAB · Λ₁₂) 는 약학 운반체 혼합에 (Begat 2004 Part I · II), 쌍별 점착에 따른 혼합 ↔ 분리는 모델 입상계에 (Jarray 2019 · Li–McCarthy 2003 / 2005 [카드 전]) 이미 있다."*

---

## G2 — "점착을 독립 측정 (AFM · IGC · 접촉각) 하고 그것으로 혼합 결과를 런 전에 예측한 연구는 없다"

**판정: broken (분야를 한정하지 않으면) — 전지 · 황화물로 좁히면 holds.**  약학은 AFM · 표면 에너지 (IGC) · 원심 탈착으로 잰 점착에서 혼합 결과를 예측했다.  전지 쪽 가장 가까운 것은 사후 상관이다.

반례 (카드):
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

반례 후보 — **카드 전 · 제목 · 후보 표 설명 기준** (그 밖 G2 partial 제목 행 = N-110 Figueroa 2009 제목의 'Predicting' · N-111 Capece 2015 다성분 Bond 수로 흐름 예측 · N-112 첫째 queue 메모의 실험 (습윤 · 접촉각) — 셋 다 측정 입력 → 혼합 결과 사전 예측인지 미확인): N-152 · Jones et al. 2008, Eur. J. Pharm. Biopharm. 69, 496–507 — S8 L288 *"콜로이드 탐침 AFM 으로 잰 점착 · 응집 비 (CAB) 로 16 제형의 혼합물 성능을 예측한 약학 선례 (Begat 2004 I · II 후속) = 우리 G2 ('잰 점착 비 → 결과 예측') 를 '전지 · 황화물 복합 양극' 으로 좁혀야 하는 근거"* (결과가 흡입 성능인지 혼합 균질도인지는 카드 전 미확인).

**좁힌 문장 (권고)**: *"전지 — 황화물 SE 복합 양극 — 에서 AM · SE 쌍의 점착을 독립 측정 (같은 SE 탐침 AFM · IGC · 접촉각) 하고 그 값을 혼합 런 전에 등록해 혼합 결과 (SE 피복 ↔ SE–SE 응집) 를 예측 · 검증한 연구는 없다 — 약학 운반체 혼합에는 측정 → 예측 선례가 있고 (Begat 2004 · Jones 2008 [카드 전] · Ahfat 1997 [카드 인용]), 전지 쪽 가장 가까운 것은 AFM-FS W_ad 와 잔류 SE 의 사후 상관이다 (Lee 2026 · 실리콘 탐침 · 5 조성)."*

---

## G3 — "황화물 복합체 혼합의 회전 속도 최적을 입자 수준에서 SE 탈응집 ↔ SE 벽 손실 (또는 비슷한) 상충으로 설명한 연구는 없다"

**판정: weakened.**  그 상충 자체는 황화물 복합체에서 실험으로 이미 관찰 · 해석됐다 (Hayakawa 2022).  쓰인 대로 남는 것은 **입자 수준 (DEM) 설명** 과 **내부 최적** 두 요소다.

반례 (카드):
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

반례 후보 — **카드 전 · 제목 · 후보 표 설명 기준**:
- N-150 · Chaudhuri 2006 (S8 L286): *"점착 × 회전 속도 → 혼합 속도 (점착이 커지면 혼합 속도가 올랐다 내려감 · … · 점착 혼합은 빠른 회전이 낫다 — 초록)"*
- N-153 · Liu, Yang, Yu 2013 (S8 L289): *"점착 (액교) × 회전 속도 × 충전율을 DEM 으로 (점착은 대체로 혼합을 낮춤 · 64 % 충전에서는 마른 입자가 가장 나쁨 — 하이라이트)"*
- N-151 · Li & McCarthy 2006 (S8 L287): *"어떤 조건에서는 느린 전단이 더 잘 섞음"*

**좁힌 문장 (권고)**: *"황화물 복합 양극 건식 혼합에서 회전 세기를 올리면 SE 탈응집 (AM 위 부착) 과 SE 벽 부착 손실이 함께 커진다는 관찰은 있다 (Hayakawa 2022 · 모델 물질 Kawaguchi 2017) — 그러나 두 효과를 입자 수준 (점착 DEM) 에서 함께 풀어 회전 세기의 내부 최적을 예측한 연구는 없다 (기존 혼합기 DEM = 할라이드 · 단조 · 벽 손실 없음: Frankenberg 2024 · Kissel 2026)."*

---

## G4 — "SE 물질 사이에 옮겨 쓸 수 있는 공정 × 재료 지도 (회전 세기 × 점착 / Bond) 는 없다"

**판정: weakened.**  점착 (Bo · Co) × 회전 세기 지도는 모델 입상계에서 이미 그려졌다 (카드 수준 = 무차원 수 · 상태도 · 카드 전 = Li–McCarthy · Chaudhuri · Liu).  쓰인 대로 남는 것은 **SE 물질 사이의 전이** 와 **'SE-on-AM 피복 ↔ SE–SE 응집' 결과 축**.

반례 (카드):
1. `nase2001_granular_bond_collision_number_wet_cohesion` — **partial**: L31 *"Co = F_c/F_Bg = 2πRγ / (πρ_sλ²R⁴(du/dy)²) … 드럼: Co = 4γ/(ρ_sλ²R³ω²)·(δ/R_t)⁴"* · L30 *"Co 가 지배 변수 라고 제안"* — 회전 (ω) × 점착 (γ) 를 한 무차원 수로 묶어 드럼 흐름 전이를 정리 · 단 흐름 (동적 각) 이지 혼합 아님 · 액체 다리 · L31 *"λ² = 값이 주어지지 않은 상수"*.
2. `jarray2019_cohesion_driven_mixing_segregation_drum` L144 — **partial**: *"SI Fig 4 의 네 칸: Bo_g < 1 · 위 = 분리 … · 1 < Bo_g < Bo_g^c = 혼합 · Bo_g > Bo_g^c = 분리"* · 같은 줄 *"⚠ '혼합' 칸에 든 점은 case 8 하나"* — 재료 축 상태도 · 공정 축 없음 · 유리구.
3. `jadidi2023_dem_batch_solid_mixers_review` L55 · L56 — **partial**: *"F_cohesion/W_p = 0.1"* (점착이 혼합을 돕는 구간) · *"CED > 80 kJ m⁻³"* (망치는 구간) — 한 축 문턱 모음.
4. 한 재료 공정 지도 (**partial**): `kawaguchi2017_…` (선속도 × 시간 × 게스트 비율) · `frankenberg2025_…` L28 (rpm × 시간 → E_m) · `frankenberg2024_…` (SI · SN vs n) · `kissel2026_…` L33 (회전수 × 시간).
5. 재료 축 · 재료 간 전이 · 한 SE 의 공정 × 크기 (**partial** · 지도 아님):
   - `lee2026_mechanical_halogen_argyrodite_drycoating` — SE 5 조성 (재료 축) · 공정 축 없음.
   - `kawaguchi2018_dry_coating_model_se_particle_powtec` L23 — 황화물 SE 를 구할 수 없어 압분 펠릿 압입으로 *"역학 성질이 비슷하다고 본"* Na₂SO₄ 를 대리로 씀 = 재료 간 전이 규칙의 암묵 사례 · 한정 L38 (닮게 고른 압입 응답 둘도 *"12 % · 20 % ↔ 6 %"* 다름).
   - `wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode` L33 — 공정 (압출 ↔ 배치) × NCM 크기 (8.7 ↔ 3.8 µm) 에서 껍질 유무 · *"운동에너지 ∝ D³ → ≈12 배"* 어림 · 한 SE.
6. 전이 규칙 자체의 불안: `lischka2025_dem_eirich_intensive_mixer_dry_mixing` L64 (응집수 불변 → γ ∝ R*^{8/5}) · L68 그 규칙으로 실제 입경까지 밀면 *"γ_real ≈ … 6.3 × 10⁻⁵ J/m²"* = *"비물리적으로 작다"* — 점착 축을 재료 · 크기 사이에 옮기는 규칙이 아직 서 있지 않다 (G4 의 공백을 오히려 받쳐 줌).

반례 후보 — **카드 전 · 제목 · 후보 표 설명 기준** (가장 강한 것부터):
- **N-112 둘째** · Li & McCarthy 2005 PRE *"Phase diagrams for cohesive particle mixing and segregation"* — queue.json N-112-2 메모: *"상태도 (혼합 / 분리 상) · 경계가 역학 · 표면 성질로 정해지는 식"* · *"실험 장치 (회전 드럼)"* → 점착 혼합 · 분리 상태도 = '공정 × 재료 지도' 꼴에 가장 가까움.
- **N-112 첫째** · 2003 PRL (S8 L148 *"점착 혼합 상태도 (Bo 축)"*) · **N-110** Figueroa 2009 (점착력 → 혼합 · 분리 예측).
- **N-150** · Chaudhuri 2006 (S8 L286): *"우리 '점착 × rpm 지도' 의 가장 가까운 선례 (G1 · G4 반례 후보)"*.
- N-153 · Liu 2013 (S8 L289): *"우리 드럼과 같은 꼴의 공정 축 선례 (G4 일부 후보)"* · N-151 · Li & McCarthy 2006 (전단 × 점착 상태도) · N-154 · Mellmann 2001 (S8 L290: 드럼 운동 꼴 경계를 *"Froude 수 · 충전율 · 벽 마찰로 가르는 지도"* — 점착 축 없음) · N-111 · Capece 2015 (다성분 Bond 수 · 흐름).

**좁힌 문장 (권고)**: *"점착 (Bo · Co) × 회전 세기 지도는 모델 입상계 (유리구 · 습윤 액교) 에서 그려졌다 (Nase 2001 Co · Jarray 2019 Bo_g 상태도 · Li–McCarthy 2003 / 2005 · Chaudhuri 2006 · Liu 2013 [카드 전]) — 실측 점착이 다른 황화물 SE 물질들 사이에 옮겨 쓸 수 있는 회전 세기 × 점착 지도를 'SE-on-AM 피복 ↔ SE–SE 응집' 결과 축으로 세운 연구는 없다."*

---

## 불확실 · 한계

1. 제목 행 23 은 카드 전이다 — 결과 · 조건을 확인하지 않았다.  특히 N-110 · N-112 두 편 · N-150–N-153 이 카드가 되면 G1 · G4 판정이 더 좁아질 수 있다 (N-112 첫째는 지금 카드 작성 중 · status.tsv L118).  카드가 나오면 이 표를 다시 대조한다.
2. Begat 2004 의 '런 전 예측' 여부는 두 편 접수일이 같아 확인 불가 — G2 의 contradicts 는 '측정 → 예측 → 대조' 의 꼴에 대한 판정이다.
3. `lee2026_mechanical_halogen_argyrodite_drycoating` 는 우리 랩 논문 (카드 L8) — 반례 · 근거로 쓸 때 자기 인용임을 밝힌다.
4. 카드가 인용한 2 차 근거 (Ahfat 1997 · Cline & Dalby 2002 · Tran 2021 · Giraud 2021 · Yazdani & Hashemabadi 2019 · Sarkar & Wassgren 2010 · Pantaleev 2017) 는 원문 미확인 — 큐 후보.
5. 판정은 이 서랍 (정본 `litdb/papers/` 의 .md 617 개 — 서식 · 색인 파일 포함 — 중 grep 후보 + 큐) 범위다.  서랍 밖 문헌은 찾지 않았다.
