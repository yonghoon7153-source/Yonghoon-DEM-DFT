<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 (후보 표 N-111 · 1저자 11-23 = 3 순위에서 앞당겨 먼저 · 믹서 논지 공백 검사) 에서 꼭 뽑으라고 한 항목.
     본 = mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표 꼴) ·
     덧붙임 = jones2008_cohesive_adhesive_balance_carrier_dpi_performance_slightly_cohesive_optimum.md · figueroa2009_vdw_adhesion_mixing_segregation_bond_number_phase_diagram.md (믹서 논지 · 공백 검사 G1–G4 절 구성).
     쪽 표기 = **PDF 쪽 p.1–11** (인쇄 쪽 = PDF 쪽 + 560 · PDF p.1 = 인쇄 561).  크롭 파일 이름의 pN · figures.json 의 page 도 PDF 쪽이다.  SI 없음 · 표 5 · 번호 붙은 식 15 · 그림 7 · 참고문헌 41.
     값 표지: [인쇄] = 본문 · 표 · 캡션 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 55 표지 — Fig. 3 · 4 · 6 의 1-bit 래스터 (≈800 dpi) 를
     800 dpi 로 렌더 · 축 = 판 틀선 (아래 = 인쇄 y 최소 · 위 = 인쇄 y 최대) · 표지 중심 = 21 px 정사각 침식 뒤 무게중심 · 순수 성분 표지가 인쇄 표 1 ff_c 를 0.00–0.04 로 재현) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산 (식 병기 · 스크립트 = 세션 scratchpad) · [우리 산술] = 우리 쪽 값 (리포 문서 · 덱 생성기 상수) 과 견주는 계산 · [카드 해석] · [카드 판정] = 이 카드의 읽기 ·
     [미확인] = 원문 11 쪽 전수에 없음.  ★ 이 카드의 재현: 식 (1)·(4)·(9)–(15) + 표 1 입력 + (원문에 식이 없는) 표면적 몫 f_SA = x_i/(ρ_i d32_i) 정규화 로 표 2–5 의 Bo_ij · Bo_Mix · f_SA · 예측 ff_c 를
     전부 재현 (인쇄 d32 그대로 ±1.3 % · 표 1 의 Bo 에서 역산한 d32 로 쌍 Bo ±0.4 % · Bo_Mix ±0.8 % · 예측 ff_c 는 인쇄 자릿수 안) · 8 점 로그–로그 최소제곱 (단일 성분 Bo > 1) 이 인쇄 α 15.7 · β 0.27 을 15.702 · 0.2724 로 재현.
     계산 (DEM · FEM · MPM · 모사) 은 없다 — 측정 + 반경험 모형 논문. -->
# 혼합물 (다성분) 입상 Bond 수 — 쌍마다 Rumpf 꼴 다돌기 반데르발스 힘 (IGC 분산 표면 에너지 → Hamaker · 기하평균 결합 · 조화평균 지름 · 돌기 · 무게) 으로 Bo_ij 를 내고 표면적 몫의 곱으로 가중한 조화평균 Bo_Mix 를 단일 성분에서 맞춘 ff_c = 15.7·Bo^−0.27 에 넣어 이원 · 삼원 · 오원 제약 분체 혼합물의 흐름 함수 계수를 예측 (평균 절대 편차 0.13–1.01) — **혼합 상태 (덮임 · 분리) 는 예측하지 않는다** (잘 섞였다고 가정) · 돌기 200 nm 가정에서는 우리 논지의 R\* 기하 이득 (1.8) 이 1.08 로 줄고 혼합쌍 무게를 조화평균으로 두면 SE–AM 쌍 Bo 가 SE–SE 의 절반이 된다 [카드 산술] — Capece · Ho · Strong · Gao (Powder Technol. 2015)

> slug `capece2015_multicomponent_granular_bond_number_cohesive_blend_flow_function` · DOI `10.1016/j.powtec.2015.08.031` · type `experiment + semi-empirical model (granular Bond number from a Rumpf-type multi-asperity van der Waals force with IGC dispersive surface energy and an assumed 200 nm asperity -> ring-shear flow function coefficient ffc = alpha*Bo^-beta fitted on single powders; multi-component (blend) Bond number = surface-area-weighted harmonic mean of pair Bond numbers with geometric-mean Hamaker and harmonic-mean diameter / asperity / weight; APAP + four MCC grades + pregelatinized starch, as-received and nano-dry-coated with 1 wt% R972 silica; binary, ternary and quinary blends in a resonant acoustic mixer; no DEM / FEM / MPM / simulation)` · PDF `50640237-111._Prediction_of_powder_flow_performance_using_a_multi-component_granular_Bond_number.pdf` · SI 없음 · digested `2026-11-24` · status ✅
>
> **저자**: **Maxx Capece ᵃ,\*** · Raimundo Ho ᵇ · John Strong ᵃ · Ping Gao ᵃ — ᵃ Drug Product Development, Research and Development, AbbVie Inc., North Chicago, IL 60064, USA · ᵇ Process Research and Development, AbbVie Inc., North Chicago · \* 교신 (AbbVie Inc., 1 N. Waukegan Road, North Chicago · maxx.capece@abbvie.com) · *Powder Technology* **286** (2015) **561–571** · 접수 2015-04-13 · 수정본 2015-07-29 · 승인 2015-08-01 · 온라인 2015-08-20 · 키워드 *Inter-particle cohesion; Granular Bond number; Flow function coefficient; Powder flowability; Formulation development* · 연구비 = **AbbVie** (저자 넷 모두 AbbVie 직원 · *"may own AbbVie stock/options"*) [인쇄 p.1 · p.11].
> **이웃 카드 (링크만)**: [`figueroa2009_vdw_adhesion_mixing_segregation_bond_number_phase_diagram`](figueroa2009_vdw_adhesion_mixing_segregation_bond_number_phase_diagram.md) (쌍별 vdW Bond 수 · 기하평균 결합 · 가벼운 쪽 무게 — 같은 해석 재료로 '혼합 ↔ 분리' 를 가른다) · [`li2006_cohesive_mixing_shear_cell_collision_number_phase_diagram`](li2006_cohesive_mixing_shear_cell_collision_number_phase_diagram.md) · [`li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation`](li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation.md) · [`li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy`](li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy.md) (쌍 Bo 위계) · [`nase2001_granular_bond_collision_number_wet_cohesion`](nase2001_granular_bond_collision_number_wet_cohesion.md) (Bo_g ≈ 1 전이) · [`deng2021_mechanical_surface_energy_tester_bond_number`](deng2021_mechanical_surface_energy_tester_bond_number.md) (이 논문 = 그 ref [10] · '측정 Bond 수') · [`alizadeh2018_dem_adhesion_calibration_segregation_heap`](alizadeh2018_dem_adhesion_calibration_segregation_heap.md) (이 논문 = 그 ref 27 · 가리킨 카드) · [`pfeffer2001_dry_particle_coating_engineered_particulates`](pfeffer2001_dry_particle_coating_engineered_particulates.md) (이 논문 ref [28] = 나노 건식 코팅) · [`mohammadijam2014_inverse_gas_chromatography_review`](mohammadijam2014_inverse_gas_chromatography_review.md) (IGC · Schultz) · [`jones2008_cohesive_adhesive_balance_carrier_dpi_performance_slightly_cohesive_optimum`](jones2008_cohesive_adhesive_balance_carrier_dpi_performance_slightly_cohesive_optimum.md) (따로 잰 점착 비 → 제형 성능).
> **판독 원자료**: `litdb/figures/capece2015_multicomponent_granular_bond_number_cohesive_blend_flow_function/digitized.csv` (55 행 — Fig. 3 이원 25 + Fig. 4 이원 24 + Fig. 6 이원 6 · 행마다 이 카드가 다시 낸 Bo_Mix · 예측 ff_c · 편차 · 95 % 예측 구간) · 크롭 **47 장** (그림 7 (Fig. 1 손 크롭 · Figs. 2–7 다시 자름) · 표 5 (전부 다시 자름) · 식 15 · 근거 문단 20) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 제약 분체의 흐름 (Schulze 환형 전단 · 예압 1 kPa 의 흐름 함수 계수 ff_c = 압밀 응력 ÷ 비구속 항복 강도) 이 입자 사이 반데르발스 점착 ÷ 입자 무게 (입상 Bond 수 Bo_g) 로 정해진다는 가정에서 출발해, **단일 분말** 11 개 (acetaminophen APAP · Avicel PH 105 · 101 · 102 · 200 · Starch 1500 · 그 가운데 다섯을 R972 나노 실리카로 건식 코팅) 의 Bo 를 Rumpf 꼴 '다돌기' 힘 (식 1 · 돌기 지름 200 nm **가정** · IGC 분산 표면 에너지 → Hamaker 식 4) 과 d32 · 진밀도로 계산해 ff_c = α·Bo^−β (식 6 · Bo > 1 인 8 점 맞춤 → **α 15.7 · β 0.27**) 를 세우고, **"As a major novelty"** 혼합물 Bond 수를 **모든 쌍 (N(N+1)/2) 의 쌍 Bo 를 표면적 몫의 곱으로 가중한 조화평균** (식 8 · 14 · 15) 으로 정의해 — 혼합쌍은 Hamaker 기하평균 (식 10) · 지름 · 돌기 · **무게 조화평균** (식 11–13) — 같은 α · β 로 이원 · 삼원 · 오원 혼합물의 ff_c 를 **혼합물 자료에 맞추지 않고** 예측했다 (평균 절대 편차: 이원 0.40 · 코팅 이원 0.99 · 삼원 0.34 · 코팅 삼원 1.01 · 전분 이원 0.16 · 전분 삼원 0.13 · 오원 1 점 2.95 ↔ 2.57).
**혼합 상태 (덮임 · 군집 · 분리) · 회전 속도 · DEM · 압밀 · 탈압 · 고체전해질은 이 논문에 없다.**  혼합물은 *"well-mixed"* 로 **가정**하고 (p.7) 접촉 확률을 표면적 몫으로 둔다 — 혼합 결과를 예측하는 틀이 아니라 **'잘 섞인 혼합물의 거시 흐름'** 을 예측하는 틀이다.

| 우리 질문 (이 묶음 · 지시서 덧붙임) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 다성분 Bo 정의 (성분별 Bo → 혼합물 Bo) | **식 (8)** Bo_g,Mix = (Σ_i Σ_j w_ij / Bo_g,ij)^−1 (가중 조화평균) · **식 (9)** Bo_g,ij = F_ad,ij / W_ij · **식 (14)** w_ij = f_SA,i f_SA,j (Σ Σ w_ij = 1) · **식 (15)** 이원 = (f²_SA,1/Bo_11 + 2 f_SA,1 f_SA,2/Bo_12 + f²_SA,2/Bo_22)^−1 · 혼합쌍 힘 = 식 (1) 또는 (5) 에 **식 (10)** A = √(A_i A_j) · **식 (11)** d_p = 2 d_i d_j/(d_i + d_j) · **식 (12)** d_asp 조화평균 · **식 (13)** W_ij = 2 W_i W_j/(W_i + W_j) | [인쇄] p.6–7 · `eq_08`–`eq_15` |
| ② ★ 결합 규칙 · 표면 에너지 · 거칠기 입력 | Hamaker = **기하평균** (A ∝ γ_d · 식 4 → A_ij ∝ √(γ_d,i γ_d,j) = 우리 논지 §2-1 의 W_ij ≈ 2√(γ_i γ_j) 와 같은 규칙) · 표면 에너지 = **IGC 분산 성분 γ_d 만** (Schultz · C6–C10 알칸 · 30 °C · RH 32 % · 덮임 5 %) · 거칠기 = **돌기 지름 200 nm 를 모든 분말에 가정** (*"natural surface roughness"* [35–39]) · 코팅 분체 = R972 돌기 16 nm (식 5) · 크기 = d32 · 모양 = 구 | [인쇄] p.2 · p.4 · `txt_p4_bond_number_calc_…` |
| ③ ★ 흐름 예측 검증 | 단일 성분 8 점 맞춤 (R² 0.982 · 로그–로그 [카드 산술]) → 맞춤 밖 **Starch 1500 예측 4.66 ↔ 실측 5.35** (−13 %) · 이원 17 혼합 AAD **0.40** · 코팅 이원 15 혼합 **0.99** · 전분 이원 4 혼합 **0.16** · 삼원 8 **0.34** · 코팅 삼원 8 **1.01** · 전분 삼원 7 **0.13** · 오원 1 점 **2.95 ↔ 2.57** · ★ [판독 + 카드 산술] 이원 AAD 셋은 **순수 성분 끝점을 뺀 혼합물만** 의 값으로 재현된다 (0.405 · 0.999 · 0.166 · 끝점을 넣으면 0.347 · 0.898 · 0.252) · 재구성한 95 % 예측 구간 밖 = 36 혼합 점 가운데 1 (판독 오차 안) · ⚠ 코팅 삼원 1.01 은 표 3 의 8 쌍으로 **1.37** — 재현 안 됨 | [인쇄] p.5 · p.8–10 · 표 2–5 · [판독] Fig. 3 · 4 · 6 · §3-6 |
| ④ ★ 우리 AM + SE 혼합물 Bo 계산에 쓸 수 있나 | **틀은 이식 가능 · 숫자는 아니다** [카드 판정 · §7-3] — ① 쌍 Bo 의 분모 (무게 조화평균) 가 Figueroa · 우리 논지 · 덱의 '가벼운 쪽 무게' 와 달라 크기비 1 : 9 에서 혼합쌍 Bo 가 **절반** 이 된다 ② 돌기 200 nm 힘 법칙에서는 R\* 기하 이득이 **1.8 → 1.08** 로 줄어 논지 판가름 수 γ_A/γ_S 0.31 이 **0.86** 으로 옮겨 간다 [카드 산술] ③ 조화평균 Bo_Mix 는 우리 조성 (AM_P : AM_S : SE = 57 : 24 : 18 wt%) 에서 무게가 4.9 % 인 **AM–AM 쌍이 1/Bo_Mix 의 95–99 % 를 차지** — '흐름 지표' 로서도 굵은 AM 이 정한다 ④ α · β 는 제약 분체 · 1 kPa · RH 33 % 의 맞춤값 — 전이 불가 ⑤ 혼합 상태 (덮임 · 군집) 는 이 틀의 출력이 아니다 | §7-2 · §7-3 |
| ⑤ ★ '점착 비 기준' (γ_AM/γ_SE · SE 탐침 AFM) | 기하평균 결합 · IGC γ_d 측정 = 같은 축의 **입력 쪽** 선례 · 그러나 점착 대비로 **혼합 결과** 를 가른 시험은 없다 (결과 = ff_c) | §0-2 G1 · G2 |
| ⑥ ★ 회전 속도 (rpm) 공정 축 | **없음** — LabRAM 진동 혼합기 **75 g · 60 Hz · 10 min · 50 g 한 조건** (코팅도 같은 조건) · 회전 없음 | [인쇄] p.3 |
| ⑦ ★ 코팅 과정 자체의 DEM | **없음** (계산 0) — 실험은 있다: 나노 건식 코팅 (R972 1 % w/w · *"It was assumed that the R972 was equally distributed to all materials during mixing"*) · 코팅 분체 + 비코팅 분체 혼합은 **R972 가 옮겨 갈 수 있어 만들지 않았다** (p.9) | [인쇄] p.3 · p.9 |
| ⑧ DEM 한계 · 소성 · 2D / 3D · 탈압 | DEM · simulation · plastic **0 회** · *"Cohesion force models which consider deformation may also be employed to evaluate the influence of a particle's mechanical properties and potentially used to predict the effect of consolidations stress"* (p.5) · 실물 3D 분말 · 탈압 없음 (환형 전단 예압 1 kPa · 전단 250–600 Pa) | §4-3 |
| ⑨ 절대값 전이 | **안 된다** — 유기 약물 · 셀룰로오스 · 전분 (8.8–122.5 µm · ρ 1.29–1.56 g/cm³) · 공기 중 RH 33 % · 1 kPa 흐름 시험 ↔ 우리 LPSCl 1 µm + NCM 4 · 9 µm · Ar · 300 MPa 압밀.  옮길 것은 **식의 꼴 · 결합 규칙 · 표면적 가중의 뜻 · 검증 꼴 (맞춤 밖 성분 · 혼합물) · 보고 규약** | §7 |

⛔ **한정어 (떼지 말 것)**: ① 출력 = **흐름 함수 계수 ff_c** (1 kPa 예압 환형 전단) — 혼합 상태 · 분리 · 덮임이 아니다 ② 혼합물은 **잘 섞였다고 가정** (가중 = 표면적 몫의 곱 = 무작위 접촉 확률) ③ 돌기 지름 **200 nm 는 모든 분말에 가정** (측정 아님 · 저자도 한계로 적음) · 모양 = 구 · 크기 = d32 ④ 표면 에너지 = **IGC 분산 성분만** (극성 · 산 · 염기 없음 · 30 °C · RH 32 %) · 셋만 이 논문에서 잼 (APAP · PH 200 · Starch) · 나머지 셋 (PH 105 · 101 · 102) 과 코팅 값 34.00 은 Huang [26] 에서 옴 ⑤ α 15.7 · β 0.27 은 **8 점 (as-received 5 + 코팅 3 · Bo 1.08–4.77 × 10³)** 의 로그–로그 맞춤 — Bo < 1 은 *"ff_c > 10"* 으로만 다룸 ⑥ 이원 AAD 는 **순수 끝점을 뺀** 값 [판독 + 카드 산술] ⑦ 코팅 삼원 AAD **1.01 은 표 3 으로 재현 안 됨 (1.37)** ⑧ 재료 = 제약 분체 (배터리 아님) · 공기 중 · RH 33 % 3 일 보관.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-111 의 '왜' 칸)

의도 원문: *"믹싱 (Bo) — "다성분 입상 Bond 수 — 우리 3 상 Bo 정의에 직접 · 카드 없음 · ★ 다음 후보" · deng2021 도 "★ 혼합물 (다성분) Bo" 로 인용"* (근거 칸 = [b02 · `alizadeh2018_dem_adhesion_calibration_segregation_heap` · L274]) + 지시서 덧붙임 (*"꼭 뽑을 것: 다성분 granular Bond 수 정의 (혼합물의 Bo 를 성분별 Bo 에서 만드는 식) · 흐름 예측 검증 · 우리 AM + SE 혼합물 Bo 계산에 쓸 수 있는지"* · 우리 질문 = '점착 비 기준' · 회전 속도 공정 축 · 코팅 과정 DEM).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "믹싱 (Bo)" | **일부** | Bo 는 혼합물의 **흐름** 을 위해 정의됐다 — 혼합은 시료 준비 단계 (LabRAM 75 g · 60 Hz · 10 min · p.3) 이고 혼합 결과 (균일도 · 분리 · 덮임) 는 재지 않았다 |
| "다성분 입상 Bond 수" | **채움** | *"As a major novelty, a granular Bond number is defined for multi-component mixtures (i.e. powder blends)"* (p.1) · 식 (8)–(15) (p.6–7) · *"absent from literature to the authors' knowledge"* (p.6) |
| "우리 3 상 Bo 정의에 직접" | **일부** | 3 성분 식은 있다 (식 8 · 삼원 표 2–4 · 오원 표 5) — 그러나 ① 혼합쌍 무게 = **조화평균** (식 13 · 근거 = *"A harmonic mean is also used to define particle weight"* 한 문장) ↔ 우리 논지 · 덱 · Figueroa 2009 = **가벼운 쪽 무게** ② 힘 = **Rumpf 다돌기** (돌기 200 nm 가정 · 크기 의존 약함) ↔ 우리 = 매끈한 구 JKR · SJKR (F ∝ R\*) ③ 결합 = Bo_Mix (흐름 지표) ↔ 우리 = 쌍 Bo 의 **순서** (누가 누구에 붙나) — 그대로 넣으면 SE–AM ↔ SE–SE 순서가 **뒤집힌다** (§7-2) |
| "카드 없음" | **확인** | papers/ 623 파일 목록 + DOI `powtec.2015.08.031` · `Capece` · `multi-component granular` grep — 인용만 (alizadeh2018 L274 · deng2021 L208 · L323) (2026-11-24) |
| deng2021 "★ 혼합물 (다성분) Bo" (그 카드 L323 '왜' = *"이종 혼합 (AM + SE) 의 Bo 정의"*) | **일부** | 혼합물 Bo 정의 = 채움 · '이종 혼합 (AM + SE) 의 Bo' 로 쓰기에는 위 ①–③ 의 규약 차이 · 출력 차이 |
| (덧붙임) "다성분 granular Bond 수 정의 (혼합물의 Bo 를 성분별 Bo 에서 만드는 식)" | **채움** (+ 카드 재현) | 위 식 · ★ 표면적 몫 f_SA 의 식은 **인쇄되지 않았다** (*"calculated based on the Sauter mean diameter"* p.7) — [카드 산술] f_SA,i = (x_i/(ρ_i d32_i)) / Σ 로 표 2–4 의 f_SA 를 끝자리까지 재현 |
| (덧붙임) "흐름 예측 검증" | **채움** (+ 카드 검증) | §0 ③ · §3-6 — 맞춤 밖 성분 1 (전분) + 혼합물 60 점 (이원 36 = 그림 · 삼원 23 · 오원 1 = 표) · 통계 = 평균 절대 편차뿐 (상관 · 보정 · 교차검증 없음) · 코팅 삼원 1.01 재현 안 됨 |
| (덧붙임) "우리 AM + SE 혼합물 Bo 계산에 쓸 수 있는지" | **일부** | §0 ④ · §7-3 — 틀 (쌍 Bo + 결합 규칙 + 접촉 확률 가중) 은 이식 가능 · 쌍 정의 · 힘 법칙 · α β · 출력은 바꿔야 |
| (우리 질문) '점착 비 기준' (γ_AM/γ_SE · 같은 SE 탐침 AFM) | **일부 (입력 쪽만)** | 기하평균 Hamaker (식 10) = 같은 결합 규칙 · IGC γ_d 로 입력 · AFM 없음 · 점착 대비 → 혼합 결과 시험 없음 |
| (우리 질문) 회전 속도 (rpm) 공정 축 | **없음** | 진동 혼합기 한 조건 (p.3) |
| (우리 질문) 코팅 과정 자체의 DEM | **없음** | 계산 0 · 실험 코팅만 (§0 ⑦) |

**가리킨 카드 · 같은 논문을 인용한 카드의 2 차 인용 대조** (카드는 고치지 않는다):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `alizadeh2018_…` **L274** (참고문헌 표 ref 27) | *"M. Capece, R. Ho, J. Strong, P. Gao, Prediction of powder flow performance using a multi-component granular Bond number, Powder Technol. 286 (2015) 561–571"* · '왜' *"다성분 입상 Bond 수 — 우리 3 상 Bo 정의에 직접"* | Maxx Capece · Raimundo Ho · John Strong · Ping Gao · 같은 제목 · Powder Technology 286 (2015) 561–571 · DOI 10.1016/j.powtec.2015.08.031 | 서지 **같음** (이니셜 꼴) · '왜' 는 **일부** (규약 차이 · 위 표) — 옮긴 수치 없음 |
| `deng2021_…` **L208** | *"혼합물로 넓힌 것 = 다성분 Bond 수 (ref [10] Capece 2015 · [23] Giraud 2021)"* | 원문이 혼합물로 넓혔다 (p.6–7) | **채움** |
| `deng2021_…` **L323** (참고문헌 표 ref 10) | 같은 서지 · *"이종 혼합 (AM + SE) 의 Bo 정의"* | 위와 같음 | 서지 **같음** · '왜' **일부** |
| 후보 표 N-111 서지 | *"M. Capece, R. Ho, J. Strong, P. Gao … Powder Technol. 286 (2015) 561–571"* | 첫 쪽 · 머리글 | **같음** (다른 점 없음) |

⇒ **의도 대조 결과: 일부** — 다성분 Bond 수 정의 · 흐름 예측 검증은 **채움** (카드가 표 2–5 를 재현하고 이원 AAD 의 계산 규약을 판독으로 밝힘 · 코팅 삼원 1.01 은 재현 안 됨); '우리 3 상 Bo 정의에 직접' 은 **일부** (쌍 무게 · 힘 법칙 · 출력이 우리와 달라 그대로 넣으면 SE–AM ↔ SE–SE 순서가 뒤집힌다); 회전 속도 축 · 코팅 DEM 은 **없음**.

---

## 0-2. ★ 공백 검사 G1–G4 — 우리 믹서 논지 문장을 이 논문이 이미 했나 (정독 출력 batch_155 끝 절과 같은 판정)

| # | 우리 공백 문장 (11-23 지시) | 판정 | 근거 (쪽 · 문장 · 값) | 반례면 우리 문장을 이렇게 좁힌다 |
|---|---|---|---|---|
| **G1** | 점착 대비를 설계 변수로 **혼합 결과** (덮임 ↔ 뭉침 · 섞임 ↔ 분리) 를 예측 | **없음** (혼합 상태를 **가정** 한다) | *"the Bond number for a well-mixed ternary or any N-component mixture can be determined by Eq. (8) with the weighting function of Eq. (14)"* (p.7) · 가중 = *"the likelihood or probability that these two materials come into contact"* (p.7 · 무작위 접촉) · 코팅: *"It was assumed that the R972 was equally distributed to all materials during mixing"* (p.3) · 결과 관측량 = ff_c 하나 | 좁힐 필요 없음.  ★ 가져올 것 = **무작위 접촉 기준선** (접촉 확률 ∝ 표면적 몫의 곱) — 우리 '무작위 대비 SE 군집' 관측량의 분모를 이 식으로 적을 수 있다 (우리 조성에서 SE–SE 0.608 · SE–AM 0.344 · AM–AM 0.049 [우리 산술 §7-3]) |
| **G2** | 점착 입력을 **따로 재고** (AFM · IGC · 접촉각 등) 혼합 결과를 미리 예측 | **일부 — 반례 (결과 = 혼합물의 흐름일 때)** | IGC γ_d (p.4 · 셋 (APAP · PH 200 · 전분) 은 이 논문 측정 · 셋 (PH 105 · 101 · 102) 과 코팅값 34.00 은 Huang [26]) → Hamaker (식 4) → 쌍 Bo (식 1 · 9–13) → Bo_Mix (식 8 · 14) → ff_c (식 7 · α β 는 **단일 성분** 에서만 맞춤) → 혼합물 60 점 + 맞춤 밖 전분 — *"Experiments would mainly serve to confirm the theoretical predictions"* (p.9) · ⚠ 사전 등록 · 상관 통계 없음 · 혼합 **상태** 는 결과가 아님 | "따로 잰 표면 에너지 (IGC) → 혼합물 Bond 수 → **혼합물 거시 흐름** 을 혼합물 자료에 맞추지 않고 예측한 선례 (Capece 2015 · 제약 분체 2–5 성분 · AAD 0.13–1.01)" 를 먼저 적고, 우리 몫을 ① 결과 = **혼합 상태** (SE 군집 무작위 대비 · AM–SE 접촉 분율) 와 **압밀 뒤 수송** ② 입력 = **쌍별 부착 (같은 SE 탐침 AFM)** — 기하평균 규칙 가정 대신 W_AS 를 직접 ③ 무기 황화물 · 건조 불활성 ④ 결과 전 등록 · 판정선 으로 좁힌다 |
| **G3** | 회전 속도 최적을 입자 수준 맞교환 (덩어리 풀림 ↔ 벽 부착 손실 등) 으로 설명 | **없음** | 혼합 · 코팅 = LabRAM **75 g · 60 Hz · 10 min** 한 조건 (p.3) — [카드 산술] 정현 진동이면 변위 진폭 ≈5.2 mm · 속도 진폭 ≈1.95 m/s · 가속도 75 g ↔ 우리 드럼 Fr 0.0827 (≈900 배) · 공정 축 · 입자 수준 관측 0 · 코팅 입자에서 비코팅 입자로 R972 가 옮겨 갈 가능성만 말로 (p.9) | 좁힐 필요 없음.  ★ 가져올 것 = **'손님 입자의 숙주 간 이동'** 을 실험 설계에서 피했다는 사실 (p.9) — 우리 코팅 팔에서 SE 가 코팅 AM ↔ 비코팅 AM ↔ SE 덩어리 사이로 옮겨 가는지를 관측량 (SE 입자의 숙주 AM id 이력) 으로 |
| **G4** | 공정 × 재료 상태도 (회전 세기 × 점착 · Bond 수 등) 가 다른 재료로 옮겨 감 | **일부 (재료 · 조성 축만 · 제약 부형제 안)** | 삼원 예측 ff_c 지도 (그림 5 · 7 = 조성 × ff_c · 재료 한 세트씩) · *"the model parameters α and β are expected to be material independent … This should be confirmed only after a wider range of materials have been examined"* (p.5) · 이전 증거 = 맞춤 밖 **전분 1 종** (4.66 ↔ 5.35) · 공정 축 0 · 부피밀도 × ff_c 상태도는 Huang [41] 을 *"would be most useful"* 로 제안만 (p.10) | "Bond 수 → 흐름의 한 곡선 (α β) 이 같은 계열 다른 부형제로 옮겨 간다는 선례 (전분 1 종 · 제약 분체 안)" → 우리 몫 = **공정 축 (rpm · Fr · 혼합 시간) × 점착 비** 의 2 차원 지도 · 무기 재료 · 혼합 상태와 압밀 뒤 결과 |

---

## 1. 한 줄 요약

미세한 제약 분체 (≲100 µm) 는 반데르발스 점착이 무게보다 수천 배 커서 흐르지 않는데, 정작 제형 개발은 성분을 섞은 **혼합물** 을 다룬다 — 이 논문은 "혼합물의 Bond 수" 를 처음 정의해 그 흐름을 입자 성질만으로 미리 맞히려 한다.
먼저 단일 분말 11 개의 Bo (Rumpf 다돌기 힘 · IGC 표면 에너지 · 돌기 200 nm 가정) 와 환형 전단 ff_c 로 **ff_c = 15.7·Bo^−0.27** (Bo > 1) 을 세우고, 혼합물은 **모든 쌍의 Bo 를 '그 두 성분이 만날 확률' (표면적 몫의 곱) 으로 가중한 조화평균** 으로 묶어 같은 식에 넣는다 — 크기가 크게 다른 혼합물 (APAP 9 µm + PH 200 123 µm) 에서 미세 성분 10 % 만 넣어도 흐름이 무너지는 현상이 표면적 가중으로 그대로 나온다.
이원 · 삼원 · 오원 혼합물과 맞춤 밖 전분까지 평균 절대 편차 0.13–1.01 로 맞고, 저자는 "제형 설계 공간을 실험 전에 그린다" 는 용도를 제안한다 — 다만 이 틀은 **잘 섞인 혼합물을 가정** 하고 흐름만 예측하며, 혼합 상태 · 분리 · 덮임은 계산하지 않는다.

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **M. Capece\*** · R. Ho · J. Strong · P. Gao (AbbVie Inc., North Chicago) | *Powder Technol.* **286** (2015) 561–571 · 접수 2015-04-13 · 온라인 2015-08-20 | 10.1016/j.powtec.2015.08.031 | **acetaminophen (APAP · Spectrum)** · **미결정 셀룰로오스 Avicel PH 105 · 101 · 102 · 200** (FMC · d50 20–200 µm 등급) · **전호화 전분 Starch 1500** (Colorcon) · 코팅재 **Aerosil R972** (Evonik · 16 nm 소수성 나노 실리카) — 배터리 소재 **아님** | 실험 (LabRAM 혼합 · 나노 건식 코팅 · Schulze RST-XS 환형 전단 · 레이저 회절 PSD · He 비중병 · IGC · BET) + 반경험 모형 (Bo → ff_c) |

- **1저자 메모 (후보 표) 와의 대조**: 저자 넷 · 순서 · 제목 · 학술지 · 권 286 · 쪽 561–571 · 2015 — **같다**.  첫 쪽 판권 줄의 DOI `http://dx.doi.org/10.1016/j.powtec.2015.08.031` · PDF 메타 제목도 같다.  메모의 "M. Capece" = **Maxx** Capece.
- **글의 꼴**: 초록 · 1. Introduction (p.1–2) → 2. Theoretical preliminary (p.2 · 식 1–3) → 3. Materials and methods (p.3–4 · §3.1 재료 · §3.2 혼합 · §3.3 표면 개질 · §3.4 흐름 · §3.5 입도 · §3.6 진밀도 · §3.7 표면 에너지 (식 4) · §3.8 Bo 계산 (식 5)) → 4. Results and discussion (p.4–10 · §4.1 단일 분말 (식 6) · §4.2 혼합물 Bo 정의 (식 7–15) · §4.3 예측 · §4.4 용도) → 5. Conclusions (p.10) → 기호표 · 감사 → 참고문헌 41 (p.11).  **SI 없음 · 표 5 · 그림 7 · 번호 식 15**.
- 중복 확인 (2026-11-24): 정본 `litdb/papers/` 623 파일 목록 + `git grep -i` (DOI `powtec.2015.08.031` · `Capece` · `multi-component granular`) — 이 논문 카드 **없음** (인용 = alizadeh2018 · deng2021) · 같은 저자 다른 논문 (ref [23] Capece 2014 Powder Technol. 254) 카드도 없음 → 새 카드.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 준비 · 측정 조건 [인쇄 p.3–4 · `txt_p3_…` · `txt_p4_igc_…`]
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 혼합 | LabRAM (Resodyn) 진동 혼합기 · 유리 병 (높이 10 cm · 안지름 9 cm · 병 350 g) · 분말 **50 g** · **10 min · 75 g (가속도) · 60 Hz** | [인쇄] p.3 |
| 나노 건식 코팅 | R972 (16 nm) **1 % w/w 모든 경우** · 혼합과 같은 조건 · 코팅 혼합물은 성분 전부 + R972 를 **한 번에 넣어 혼합과 코팅을 한 단계로** · *"It was assumed that the R972 was equally distributed to all materials during mixing"* | [인쇄] p.3 |
| 흐름 | Schulze RST-XS 환형 전단 셀 (높이 13 mm · 안 / 바깥 지름 32 / 64 mm · 날개 16 개 × 3 mm) · **예압 (pre-consolidation) 1 kPa** · 파괴 전단 **250 · 390 · 600 Pa** → 항복 궤적 → ff_c = 압밀 응력 ÷ 비구속 항복 강도 · 시료 **RH 33 % 3 일** 보관 · 세 번 | [인쇄] p.3 |
| 입도 | Helos 레이저 회절 (Fraunhofer) + Rodos 건식 분산 0.5 bar · 누적 부피 분포 (그림 1) → **d32 (Sauter)** 를 특성 크기로 | [인쇄] p.3 · p.4 |
| 진밀도 | He 비중병 AccuPyc II 1340 · 다섯 번 평균 | [인쇄] p.3 |
| 표면 에너지 | IGC-SEA (FID) · 실란화 기둥 300 × 4 mm · 총 표면적 0.25 m² 가 되게 시료량 (BET: **APAP 0.291 · PH 200 1.18 · Starch 0.694 m²/g** · 나머지는 Huang [26] 의 γ 를 써서 BET 안 함) · 30 °C · **RH 32 %** · 2 h 조건화 · Schultz 법 (C6–C10 알칸) · 덮임 5 % · 두 번 · 메탄 = 죽은 부피 | [인쇄] p.3–4 |
| Hamaker | **식 (4) A = 24π D0² γ_d** (Frenkel · D0 = 0.165 nm [34]) | [인쇄] p.4 |

- [카드 산술] BET ↔ d32 기하 비표면적 6/(ρ d32): APAP **0.528** · PH 200 **0.0314** · Starch **0.126 m²/g** → BET/기하 = **0.55 · 37.6 · 5.5** — MCC · 전분은 BET 가 기하 면적보다 훨씬 크다 (내부 · 표면 거칠기).  ⇒ 표면적 가중 (식 14) 을 **BET 로 하면** APAP–PH 200 50 : 50 의 APAP 몫이 **0.944 → 0.198** 로 뒤집힌다 [카드 산술] — 원문은 **d32 기하 면적** 을 썼고 (p.7) 그 선택으로 예측이 맞았다.
- [판독 · 눈대중] 그림 1: APAP 는 ≈2 µm 부터 시작하는 넓은 분포 (누적 0.5 ≈15–20 µm ↔ d32 8.8 µm) · PH 200 이 가장 굵다 (누적 0.5 ≈220 µm ↔ d32 122.5 µm) — d32 는 미세 쪽에 무게가 실린 평균이다.

### 3-2. ★ 단일 성분 Bo — 식 (1)–(5) [인쇄 p.2 · p.4 · `eq_01`–`eq_05` · `txt_p2_eq1_terms_…` · `txt_p4_bond_number_calc_…`]
| 식 | 인쇄된 꼴 | 뜻 · 가정 |
|---|---|---|
| (1) | **F_cohesion = A/(12 z0²) · ( d_p/(2 (H0/z0)²) + 3 d_asp d_p/(d_asp + d_p) )** | '다돌기 (multi-asperity)' = Rumpf 식의 변형 [21] · 첫 항 = 거리 H0 의 두 입자 사이 비접촉 힘 · 둘째 항 = 입자–돌기 접촉 힘 · *"The contribution of the non-contact force is typically small and can be neglected unless separation distance is about 20 nm or less"* · z0 = **0.4 nm** |
| (2) | **H0 = z0 + d_asp/2** | 돌기 = 반구 가정 (분포를 알면 더 정확 [22]) |
| (3) | **Bo_g = F_cohesion / W_g** | 점착 (다른 입자면 *"adhesion force for dissimilar particles"*) ÷ 무게 · *"Particles with higher cohesion forces relative to their weight (Bo_g > 1) are considered cohesive"* |
| (4) | **A = 24π D0² γ_d** | Hamaker ← 분산 표면 에너지 (Frenkel · D0 0.165 nm) |
| (5) | **F_cohesion = A d_asp/(24 z0²)** | 코팅 분체: R972 가 촘촘한 인공 돌기 → **돌기–돌기 접촉만** · R972 의 A · d_asp (16 nm) 로만 계산 [21] |

- 원문 가정 [인쇄 p.4]: *"Particle size, true density, and surface energy were measured for each material while asperity size was assumed to be 200 nm in all cases"* · *"The Sauter mean diameter d32 was used as the characteristic particle size … Particles were assumed spherical."*
- [카드 산술 · 식의 뜻] 식 (1) 의 첫 항은 지름 d_p 인 **같은 두 구** 가 H0 떨어진 Hamaker 힘 A d_p/(24 H0²) 와 같고, 둘째 항은 입자 (d_p) – 돌기 (d_asp) 구–구 Hamaker 힘 A/(12 z0²)·d_asp d_p/(d_asp + d_p) 의 **정확히 3 배** 다 (원문은 '3' 의 뜻을 적지 않는다 [카드 해석: 세 돌기 접촉]).  돌기가 없으면 (d_asp → 0 · H0 → z0) 식 (1) 은 A d_p/(24 z0²) = **A R\*/(6 z0²)** (매끈한 구 · F ∝ R\*) 로 돌아간다 — 돌기가 있으면 d_p ≫ d_asp 에서 F ≈ A d_asp/(4 z0²) 로 **입자 크기와 거의 무관** 해진다.
- [카드 산술] 표 1 입력으로 F (식 1): APAP **21.3 nN** · PH 105 30.2 · PH 101 27.0 · PH 102 35.9 · PH 200 30.2 · Starch 21.2 nN (크기 8.8–122.5 µm 인데 힘은 1.7 배 안) · 비접촉 항의 몫 ≤ **0.16 %** · 무게 W = ρ g π d³/6: **4.5 pN (APAP) → 14.7 nN (PH 200)** (3,260 배) ⇒ 표 1 의 Bo 차이는 **거의 전부 무게 (∝ ρ d³)** 다.  코팅 (식 5 · A 6.98 × 10⁻²⁰ · 16 nm) = **0.291 nN** — 자연 거칠기 힘의 1/73–1/123.

### 3-3. ★ 표 1 — 입자 성질 · Bo · ff_c [인쇄 p.4 · `tab_1.png`] + 재현 [카드 산술]
| 물질 | d32 (µm) | ρ (kg/m³) | d_asp (nm) | γ_d (mJ/m²) | A (J) | Bo_g | ff_c (SE) |
|---|---:|---:|---:|---:|---:|---:|---:|
| APAP | 8.8 | 1291 | 200 | 33.95 | 6.97 × 10⁻²⁰ | 4.77 × 10³ | 1.40 (0.02) |
| Avicel PH 105 | 11.7 | 1559 | 200 | 47.80 ᵇ | 9.81 × 10⁻²⁰ | 2.34 × 10³ | 2.00 (0.05) |
| Avicel PH 101 | 32.2 | 1562 | 200 | 42.33 ᵇ | 8.69 × 10⁻²⁰ | 1.01 × 10² | 4.53 (0.09) |
| Avicel PH 102 | 63.1 | 1563 | 200 | 56.05 ᵇ | 1.15 × 10⁻¹⁹ | 1.78 × 10¹ | 6.28 (0.09) |
| Avicel PH 200 | 122.5 | 1562 | 200 | 47.11 | 9.67 × 10⁻²⁰ | 2.05 | 13.0 (0.35) |
| Starch 1500 | 31.7 | 1500 | 200 | 33.20 | 6.82 × 10⁻²⁰ | 8.61 × 10¹ | 5.35 (0.05) |
| APAP (SM) | 8.8 | 1291 | 16 | 34.00 ᵇ | 6.98 × 10⁻²⁰ | 6.51 × 10¹ | 5.27 (0.10) |
| PH 105 (SM) | 11.7 | 1559 | 16 | 34.00 ᵇ | 6.98 × 10⁻²⁰ | 2.25 × 10¹ | 8.30 (0.48) |
| PH 101 (SM) | 32.2 | 1562 | 16 | 34.00 ᵇ | 6.98 × 10⁻²⁰ | 1.08 | 14.1 (1.14) |
| PH 102 (SM) | 63.1 | 1563 | 16 | 34.00 ᵇ | 6.98 × 10⁻²⁰ | 1.44 × 10⁻¹ | 12.3 (0.64) |
| PH 200 (SM) | 122.5 | 1562 | 16 | 34.00 ᵇ | 6.98 × 10⁻²⁰ | 1.97 × 10⁻² | 15.1 (3.50) |

ᵃ 200 nm = 자연 거칠기 · 16 nm = R972 코팅 · ᵇ Huang et al. [26] 의 값 · ff_c 는 예압 1 kPa · 괄호 = 표준 오차 [인쇄 표 1 각주].
- [카드 산술] 식 (4) 로 표 1 의 A 를 **세 자리까지 재현** (APAP 6.969 × 10⁻²⁰ 등 · R972 34.00 → 6.979 × 10⁻²⁰).  식 (1) · (3) · (5) 로 표 1 Bo 를 **±1.2 % 안** 에서 재현 (APAP −1.2 % 가 가장 크다 · 표 1 Bo 로 d32 를 역산하면 APAP 8.765 · PH 105 11.718 · PH 101 32.178 · PH 102 63.071 · PH 200 122.478 · Starch 31.728 µm — 표의 d32 는 반올림값이고 Bo 는 반올림 전 값으로 계산됐다).  g = 9.81 m/s² 는 원문에 숫자가 없다 [카드 가정].
- 코팅의 효과 (Bo 비 as-received ÷ SM): APAP 73 · PH 105 104 · PH 101 94 · PH 102 124 · PH 200 104 [카드 산술] — 원문: *"inter-particle cohesion is lower for surface modified materials due to the low surface energy and small size of R972 which act as artificial asperities"* (p.4).

### 3-4. ★ 식 (6) — Bo → ff_c 맞춤 (그림 2) [인쇄 p.4–5 · `fig_2.png` · `eq_06` · `txt_p4_ffc_plateau_…` · `txt_p5_fit_…`]
- **관찰**: Bo 가 줄면 ff_c 가 오르다가 **Bo_g = 1 에서 최대 · Bo < 1 에서 변하지 않음** (*"attains a maximum and remains invariant for Bond numbers less than one"* p.4) · Bo < 1 인 코팅 PH 102 · PH 200 = ff_c 12.3 · 15.1 (*"all non-cohesive powders with Bo_g < 1 have excellent flow performance with ff_c > 10"* p.5).
- **맞춤**: *"Eq. (6) was fit to the data of Fig. 2 only for materials with Bo_g > 1 … A simple linear regression was used to determine the model parameters after linearizing Eq. (6). The best fit of Eq. (6) with parameters α = 15.7 and β = 0.27 along with the 95% confidence intervals describes the data well for Bond number spanning four orders of magnitude"* (p.5) · Starch 1500 은 맞춤에서 뺌 (그림 2 캡션).
- [카드 산술 · 재현] Bo > 1 인 점 = as-received 5 + 코팅 APAP · PH 105 · **PH 101 (Bo 1.08)** = **8 점** → log10 ff_c ↔ log10 Bo 최소제곱 **α 15.702 · β 0.2724 · R² 0.982** (인쇄 15.7 · 0.27 재현) · 코팅 PH 101 을 빼면 (7 점) 16.52 · 0.281 · as-received 5 점만이면 15.20 · 0.273 ⇒ 인쇄 맞춤은 **8 점** 이다.  인쇄 예측값들 (전분 4.66 · 표 2 의 2.84 등) 도 반올림 전 15.702 · 0.2724 로 나온다 (전분 4.666).
- 원문의 상관 통계: 인쇄된 R² · 표준 오차 · 잔차 없음 [미확인] — 위 R² 는 카드 산술.
- [카드 산술] 재구성한 95 % 신뢰 구간 (8 점 · t 2.447) at Bo = 1: **13.1–18.8** · 그림 2 의 점선과 같은 크기 [판독 · 눈대중].

### 3-5. ★ 혼합물 Bo — 식 (7)–(15) [인쇄 p.6–7 · `eq_07`–`eq_15` · `txt_p6_mixture_…` · `txt_p7_combining_…`]
| 식 | 인쇄된 꼴 | 원문 근거 |
|---|---|---|
| (7) | ff_c,Mix = α (Bo_g,Mix)^−β | *"Eq. (7) logically follows"* — 같은 α · β |
| (8) | **Bo_g,Mix = (Σ_i Σ_j w_ij / Bo_g,ij)^−1** | *"the Bond number of a multi-component mixture must account for all interactions between two particles of each and every material"* · 이원 3 · 삼원 6 · N 성분 N(N+1)/2 쌍 · *"weighted harmonic mean"* |
| (9) | Bo_g,ij = F_ad,ij / W_ij | 쌍 Bond 수 (일반형) |
| (10) | **A = √(A_i A_j)** | *"A geometric mean is used to define the Hamaker constant"* (근거 인용 없음) |
| (11) · (12) | d_p · d_asp = **조화평균** 2xy/(x + y) | *"a harmonic mean is often used to define a characteristic particle size [18]"* |
| (13) | **W_ij = 2 W_i W_j/(W_i + W_j)** | *"A harmonic mean is also used to define particle weight."* (근거는 이 한 문장) |
| (14) | **w_ij = f_SA,i f_SA,j** (Σ Σ w_ij = 1) | *"the vdW force is mainly a phenomenon arising from particles in close contact"* → 표면적 몫의 곱 = 두 성분이 만날 확률 · *"Using the actual number of contacts (i.e. coordination number) between the various components may offer a superior formulation, but determining the coordination number may be difficult for multi-component mixtures with particles of different sizes"* |
| (15) | Bo_g,Binary = (f²_SA,1/Bo_11 + 2 f_SA,1 f_SA,2/Bo_12 + f²_SA,2/Bo_22)^−1 | *"For material A with a fine particle size blended with material B with a coarse particle size, A–A interactions will be most likely, followed by A–B interactions, and lastly B–B interactions … the predominant type of interaction as determined by surface area will influence bulk powder behavior most significantly"* |

- [카드 산술 · 식의 뜻] 식 (11) 의 조화평균 지름 = **4 R\*** — 식 (1) 첫 항에 넣으면 지름이 다른 두 구의 Hamaker 힘과 정확히 같다 (그래서 조화평균은 '근사' 가 아니라 구–구 기하) · 식 (13) 의 무게 조화평균은 질량이 크게 다르면 **가벼운 쪽 무게의 2 배** 로 간다 (W_A/W_S → ∞ 에서 W_ij → 2 W_S) — 이것이 Figueroa 2009 (가벼운 쪽 무게) 와 **2 배** 다른 이유 (§7-2).
- [카드 산술] 조화평균 (식 8) 은 **가장 약한 쌍** 이 지배한다: 무게 몫이 작아도 Bo_ij 가 매우 작으면 1/Bo_ij 가 합을 차지한다.

### 3-6. ★ 검증 — 이원 · 삼원 · 오원 + 맞춤 밖 성분 [인쇄 p.7–10 · 표 2–5 · 그림 3–7 · [판독] digitized.csv]

**(a) 표 2–5 재현** [카드 산술 · 표 1 입력 + 식 + f_SA = x_i/(ρ_i d32_i) 정규화]: 표 2 · 3 · 4 의 f_SA **23 행 전부 끝자리 ±0.002** · 쌍 Bo (Bo_12 · Bo_13 · Bo_23) **15 값 ±1.3 %** (표 1 의 Bo 로 역산한 d32 면 ±0.4 %) · Bo_Mix **23 행 ±1.1 %** (역산 d32 면 ±0.8 %) · 예측 ff_c 23 행 = 인쇄 자릿수 안 (차 ≤0.015 · 인쇄 '12.4' 한 행 = 12.45) · 오원 Bo_Mix **458 (인쇄 4.58 × 10²)** · 예측 2.959 (인쇄 2.95) ⇒ 원문 계산 사슬은 이 카드의 식 그대로이고 **f_SA 의 식 (원문 미인쇄) 은 질량 몫 ÷ (ρ d32) 정규화** 다.

**(b) 예측 정확도**
| 시험 | 점 수 | 인쇄 AAD | 이 카드 재계산 | 표지 |
|---|---:|---|---|---|
| 이원 as-received (그림 3 · APAP + PH 200 / 102 / 101 / 105) | 17 혼합 (+ 끝점 8) | **0.40** | 혼합만 **0.405** · 끝점 포함 0.347 · 평균 상대 편차 16.0 % (최대 39.5 % = PH 200 · APAP 0.4) · 치우침 (예측 − 실측) −0.05 | [판독 + 카드 산술] |
| 이원 코팅 (그림 4 · Bo_Mix < 1 은 모형 안 그림) | 15 혼합 (+ 끝점 6) | **0.99** | 혼합만 **0.999** · 끝점 포함 0.898 · 12.2 % · 치우침 **−0.69** (모형이 덜 흐르게 예측) | [판독 + 카드 산술] |
| 이원 APAP + 전분 (그림 6) | 4 혼합 (+ 끝점 2) | **0.16** | 혼합만 **0.166** · 끝점 포함 0.252 · 7.5 % | [판독 + 카드 산술] |
| 삼원 as-received (표 2 · APAP/101/200 · APAP/101/102 × 4 조성) | 8 | **0.34** | **0.344** · 10.4 % · 치우침 −0.23 | [인쇄 표 + 카드 산술] |
| 삼원 코팅 (표 3) | 8 | **1.01** | ⚠ **1.37** (APAP/101/200 1.66 · APAP/101/102 1.08) · 14.7 % · 최대 36 % — **인쇄값 재현 안 됨** | [인쇄 표 + 카드 산술] |
| 삼원 APAP/101/전분 (표 4) | 7 | **0.13** | **0.126** · 5.3 % | [인쇄 표 + 카드 산술] |
| 오원 (표 5 · APAP 0.10 + PH 102 · 101 · 105 · 전분 각 0.225) | 1 | — | 예측 2.95 ↔ 실측 **2.57 (0.01)** · +15 % | [인쇄] |
| 맞춤 밖 성분 (전분) | 1 | — | Bo 8.61 × 10¹ → **4.66 ↔ 5.35** · −13 % | [인쇄] p.9 |

- ★ **이원 AAD 의 계산 규약** [판독 + 카드 산술]: 인쇄 0.40 · 0.99 · 0.16 은 **순수 성분 끝점 (APAP 0 · 1) 을 뺀 혼합물만** 으로 재현된다 — 끝점 (단일 분말) 은 α · β 맞춤에 쓰인 점들이라 빼는 것이 맞지만 원문은 그 규약을 적지 않았다.
- **95 % 예측 구간** [카드 산술 · 8 점 맞춤으로 재구성 · Bo 2.05 에서 9.24–18.04 · Bo 4770 에서 1.10–2.23 = 그림 3 의 점선과 같다 [판독 · 눈대중]]: 혼합 36 점 가운데 구간 밖 **1 점** (그림 3 PH 200 · APAP 0.4 = 2.41 ↔ 아래 경계 2.44 · 판독 오차 ±0.04 안) — 원문 *"within the 95% prediction interval"* (코팅 이원 · p.9) 과 맞는다.
- 원문 해석: 코팅 쪽이 더 빗나가는 것은 *"less-cohesive materials (Bond numbers close to one) and their flowability is less influenced by the vdW force"* · 코팅 APAP + 코팅 PH 105 의 큰 빗나감은 PH 105 자신이 식 (6) 에서 벗어나서 (*"the vdW force may be over-predicted for Avicel PH 105"*) · 삼원이 이원보다 조금 낫다 → *"the model's predictive capability does not diminish with higher number of components"* (p.9).
- ★ 원문이 강조한 현상: **크기가 크게 다른 혼합물의 급락** — APAP (d32 9 µm) 10 % 만 넣어도 PH 200 (123 µm) 의 ff_c 가 13.05 → **8.86** [판독] (예측 7.27 · Bo_Mix 16.9 [카드 산술]) · *"Due to the high surface area of APAP relative to Avicel PH 200, the bulk powder behavior is substantially affected by APAP"* (p.8).

### 3-7. 원문이 적은 한계 · 원문 안 어긋남
**원문 한계 (p.5 · p.10)**: ① ff_c 는 부피밀도를 빼므로 *"cannot be used as a stringent prediction of flowability"* (중력 흐름은 부피밀도 · 실제 응력이 같이 정한다) ② 흐름은 이력 (압밀 응력 · 시간) · 환경 (습도) · 장치 (기하 · 재질) · 모양 · 기계 성질 (탄성 · 경도) 에 달렸는데 **고려하지 않았다** ③ **응집 (agglomeration) 을 넣지 않았다** — *"may affect calculation of the Bond number [26]"* ④ 돌기 200 nm 가정 *"may not be suitable for the wide variety of materials"* ⑤ α · β 의 물질 무관성은 *"should be confirmed only after a wider range of materials have been examined"* ⑥ 비점착 (Bo < 1) 분말은 이 틀 밖 (모양 · PSD 가 더 중요 [6–12]).
**원문 안 어긋남 (카드가 본 것)**:
1. ⚠ **코팅 삼원 AAD '1.01'** (p.9) ↔ 표 3 의 8 쌍으로 **1.37** [카드 산술] — 그림 5 의 값 (11.34 · 13.01) 으로 바꿔도 1.37 · 반쪽 (APAP/101/102) 만이면 1.08 · 어느 규약으로도 1.01 이 안 나온다.
2. *"Avicel PH 105 by itself also deviates somewhat from Eq. (6) as seen in Fig. 1"* (p.9) — 그림 1 은 입도 분포 → **그림 2** 여야.
3. 그림 3 의 PH 200 판 범례 **α = 15.6** ↔ 캡션 · 본문 15.7 (그 판의 곡선은 15.7 로 그린 것과 같다 [판독 + 카드 산술]).
4. *"Eq. (6) is not capable of describing the behavior of SM Avicel PH 101, SM PH 102, and SM PH 200"* (p.5) ↔ 코팅 PH 101 (Bo 1.08 > 1) 은 **맞춤에 들어 있다** (넣어야 α · β 가 재현된다) · 맞춤 예측 15.38 ↔ 실측 14.1 ± 1.14 (+9 % · 신뢰 구간 12.9–18.4 안) [카드 산술] — 원문 괄호 *"ffc values would be significantly over-estimated"* 는 코팅 PH 102 · PH 200 (식 6 외삽 26.6 · 45.8 ↔ 실측 12.3 · 15.1) 에만 맞는다.
5. 식 기호: N 성분 쌍 수 *"∑_{i=l}^{N} i"* · 제약식 *"∑_{i −l}^{N}"* — 'l' · '−l' 는 '= 1' 의 조판 오류로 보인다 [카드 해석].
6. 오자: 'Shulze' (본문) · 'Shultz' (ref [40]) = Schulze · 'Sympactec' · 그림 2 범례 'As-Recieved' · 그림 2 캡션 'dotted lines' ↔ 그림은 파선.  참고문헌 목록: [29] 저자 칸에 '94–102,' 가 끼어 있다 · [30] 'Spring-Verlag' · [16] 쪽 '7–93' · [31] 'Powder Technol. 25 (2014)' (권 번호가 2014 년과 안 맞는다 [카드 해석]) · [17] 이름 첫 글자 없음.
7. 오원 예측 2.95 ↔ 반올림 전 계수로 2.959 (2.96) — 끝자리 차.
8. *"correlates well"* (p.1 · p.4) — 상관계수 · R² 는 인쇄되지 않았다 (카드 산술 R² 0.982).

---

## 4. ★ 방법 — 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 · 계산 사슬
분말 (as-received 6 · R972 코팅 5) → d32 (레이저 회절) · ρ (He 비중병) · γ_d (IGC · 셋은 이 논문 · 나머지 Huang [26]) · d_asp (200 nm 가정 · 코팅 = 16 nm) → 식 (4) A → 식 (1) / (5) F → 식 (3) Bo → 환형 전단 ff_c (1 kPa) → **식 (6) 맞춤 (Bo > 1 · 8 점)** → 혼합물: 질량 몫 → f_SA (d32 기하 면적) → 쌍 Bo (식 9–13) → Bo_Mix (식 8 · 14 · 15) → 식 (7) 예측 ff_c → LabRAM 으로 실제 혼합 · 전단 → 대조 (AAD).
- **맞춘 값과 맞춘 대상**: α · β 둘 (단일 분말 8 점) — 그 밖 혼합물 예측에는 맞춘 값 0.  가정한 값 = z0 0.4 nm · D0 0.165 nm · d_asp 200 nm (코팅 16 nm) · 구형 · d32.
- **검증**: 맞춤 밖 성분 1 (전분) · 혼합물 60 점 (이원 36 = 그림에만 · 삼원 23 · 오원 1 = 표) · 통계 = AAD (상관 · 교차검증 · 사전 등록 없음).

### 4-2. 입자 처리 (우리 축 언어로)
- 입자 = **구 (d32 하나)** · 크기 분포 · 모양 · 응집은 버린다 · 표면 = 돌기 하나의 크기 (200 nm · 16 nm) 로 대표 · 점착 = **비접촉 반데르발스만** (모세관 · 정전기 · 소성 변형 · 접촉 넓어짐 없음 — RH 33 % 인데도 *"In the absence of condensed moisture capillary forces are irrelevant"* p.2).
- 침대 · 배치 · 접촉망 없음 — 혼합물 = 표면적 몫으로만 기술 (무작위 접촉) · 거시 흐름 = 쌍 Bo 의 가중 조화평균 하나.
- 우리 대응: 믹서 DEM = SJKR (매끈한 구 · 접촉 면적 × CED · F ∝ R\*) · 쌍별 CED 를 γ 비에서 기하평균으로 · 쌍 Bo 분모 = 작은 (가벼운) 쪽 무게 · 거친 입자 parcel — **이 논문과 같은 것은 결합 규칙 (기하평균) 하나** (§7-1).

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말했나** — **말 없음 (계산 없음)**.  원문 11 쪽에 `DEM` · `discrete element` · `simulation` · `finite element` · `plastic` = **0 회** (셈 = 원문 대조 기록).  모형 일반의 한계로 말한 것: *"Particulate processes remain exceedingly difficult to model, design, and control … particle-scale interactions are difficult to resolve. Additionally, constitutive relationships derived from first-principles relating bulk-scale behavior, particle-scale interactions, and particle properties are generally unattainable."* (p.1) · *"particle assemblies have very complex behavior in comparison to particle–particle interactions quantified by the Bond number"* (p.5).
2. **소성 · 큰 변형을 넣기 어려운 이유 · 우회 · 비용** — 계산 없음.  소성 쪽 문장: vdW 힘은 *"mechanical properties such as hardness and elasticity"* 에 달렸다 (p.2) · *"Cohesion force models which consider deformation may also be employed to evaluate the influence of a particle's mechanical properties and potentially used to predict the effect of consolidations stress"* (p.5) · 결론의 한계 목록에 *"mechanical properties (elasticity and hardness)"* (p.10) — **우회 = 넣지 않음** (강체 구 + 돌기).
3. **2D 인가 3D 인가** — 실물 3D 분말 · 2D ↔ 3D 진술 없음.
4. **압력을 뺄 때의 거동** — 없음.  환형 전단의 예압 1 kPa · 파괴 전단 250–600 Pa (항복 궤적) 뿐 — 압밀 · 탈압 · 되돌아옴 없음 (우리 300 MPa 의 30 만 분의 1).

### 4-4. 기법 미니 용어집
- **입상 Bond 수 (granular Bond number) Bo_g**: 입자 사이 인력 ÷ 입자 무게 · > 1 = 점착성 (원문) · 흐름 · 유동화 · 부피밀도와 상관한다 [17,22–26].
- **흐름 함수 계수 ff_c**: 압밀 응력 σ1 ÷ 비구속 항복 강도 σc (환형 전단의 항복 궤적에서) · 클수록 잘 흐름 · 원문은 *"ffc > 10"* 을 *"free-flowing criteria"* 로만 쓴다 (p.5) · 그 밖의 관례 구간 경계값은 인쇄되지 않았다 (Jenike [32] · Schulze [30] 인용만) [미확인].
- **Rumpf 다돌기 (multi-asperity) 모형**: 거친 표면의 두 구 — 큰 구 사이 거리 H0 의 약한 비접촉 힘 + 돌기를 통한 접촉 힘 (식 1) · 돌기가 작을수록 힘이 작다 (나노 코팅이 흐름을 좋게 하는 원리).
- **Hamaker 상수 · Frenkel 관계**: A = 24π D0² γ_d (식 4 · D0 = 0.165 nm 차단 거리).
- **IGC (역기체 크로마토그래피) · Schultz 법**: 분말을 채운 기둥에 알칸 탐침을 흘려 머무름 시간으로 분산 표면 에너지 γ_d 를 낸다 (`mohammadijam2014_…`).
- **나노 건식 코팅 (nano-dry-coating)**: 고강도 혼합 · 분쇄로 나노 입자 (R972) 를 숙주 입자 표면에 흩어 붙여 인공 돌기를 만든다 [28] (`pfeffer2001_…`).
- **LabRAM (공진 음향 혼합기)**: 병을 수직으로 진동 (여기 75 g · 60 Hz) 시키는 무날개 혼합기.
- **표면적 몫 f_SA**: 성분 i 의 표면적 ÷ 전체 표면적 — 이 논문은 d32 기하 면적 (x/(ρ d32)) 을 썼다 [카드 산술].
- **AAD (average absolute deviation)**: 예측 ff_c 와 실측의 차의 절댓값 평균 (ff_c 단위).

---

## 5. Figure set ★ (크롭 47 장 = `litdb/figures/capece2015_multicomponent_granular_bond_number_cohesive_blend_flow_function/`)

| 자료 (크롭 파일) | 내용 | 우리 활용 |
|---|---|---|
| Fig. 1 (`fig_1.png` · 손 크롭) | 여섯 분말의 누적 부피 분포 (1–1000 µm 로그 축) | d32 가 미세 쪽 평균이라는 감각 (§3-1) |
| Fig. 2 (`fig_2.png`) | ★ Bo_g ↔ ff_c (로그–로그) · as-received (검정) · 코팅 (흰) · 식 (6) 선 + 95 % 신뢰 구간 · Bo = 1 세로선 (Non-cohesive ↔ Cohesive) · α 15.7 · β 0.27 | ★ Bo → 흐름 곡선 · Bo < 1 평탄 · 8 점 맞춤 재현 (§3-4) |
| Fig. 3 (`fig_3.png`) | 이원 as-received (APAP + PH 200 / 102 / 101 / 105) ff_c vs APAP 질량 몫 · 예측 곡선 + 95 % 예측 구간 (PH 200 판 범례 α = 15.6) | ★ 판독 25 점 → AAD 0.405 재현 (§3-6) · 크기 차 큰 혼합물의 급락 |
| Fig. 4 (`fig_4.png`) | 이원 코팅 (같은 넷) · Bo_Mix < 1 구간은 곡선 없음 | ★ 판독 24 점 → AAD 0.999 재현 · 모형이 덜 흐르게 예측 (치우침 −0.69) |
| Fig. 5 (`fig_5.png`) | 삼원 (APAP/101/200 · APAP/101/102 · as-received 위 · 코팅 아래) 예측 ff_c 색 지도 + 실측 값 글자 | ★ '조성 설계 공간' 지도 문법 (G4) · 실측 값 = 표 2 · 3 |
| Fig. 6 (`fig_6.png`) | 이원 APAP + Starch 1500 | ★ 맞춤 밖 성분의 이원 예측 · AAD 0.166 재현 |
| Fig. 7 (`fig_7.png`) | 삼원 APAP / PH 101 / Starch 1500 예측 색 지도 + 실측 7 점 | 표 4 와 같은 값 |
| Table 1 (`tab_1.png`) | 11 분말의 d32 · ρ · d_asp · γ_d · A · Bo · ff_c | ★ 입력 전부 · 재현 (§3-3) |
| Table 2 · 3 · 4 (`tab_2.png` · `tab_3.png` · `tab_4.png`) | 삼원 질량 · 표면적 몫 · 쌍 Bo · Bo_Mix · 예측 · 실측 ff_c | ★ f_SA 식 역산 · 표 3 AAD 불일치 (§3-6) |
| Table 5 (`tab_5.png`) | 오원 한 점 (Bo_Mix 458 · 2.95 ↔ 2.57) | 다성분 확장 1 점 |
| 식 (1)–(15) (`eq_01_multi_asperity_cohesion_force_rumpf.png` · `eq_02_separation_distance_h0.png` · `eq_03_granular_bond_number_definition.png` · `eq_04_hamaker_from_dispersive_surface_energy.png` · `eq_05_coated_asperity_contact_force.png` · `eq_06_ffc_power_law_bond_number.png` · `eq_07_mixture_ffc_power_law.png` · `eq_08_mixture_bond_number_weighted_harmonic_mean.png` · `eq_09_pair_bond_number_adhesion_over_weight.png` · `eq_10_hamaker_geometric_mean.png` · `eq_11_particle_diameter_harmonic_mean.png` · `eq_12_asperity_diameter_harmonic_mean.png` · `eq_13_pair_weight_harmonic_mean.png` · `eq_14_weighting_fractional_surface_area_product.png` · `eq_15_binary_mixture_bond_number.png`) | 힘 · Bo · 맞춤 · 혼합물 정의 전부 (식 번호 포함) | ★ 보고서 · 덱에 그대로 |
| 근거 문단 20 장 (`txt_p1_abstract.png` · `txt_p2_vdw_only_capillary_irrelevant_electrostatic_10x_weaker.png` · `txt_p2_eq1_terms_noncontact_20nm_z0_04nm_hamaker.png` · `txt_p2_bond_number_ratio_bo_gt1_cohesive.png` · `txt_p2_single_component_only_two_questions.png` · `txt_p3_labram_mixing_75g_60hz_and_r972_nano_dry_coating_1pct.png` · `txt_p3_ring_shear_1kpa_250_390_600pa_33rh.png` · `txt_p4_igc_schultz_30c_32rh_hamaker_d0.png` · `txt_p4_bond_number_calc_asperity_200nm_eq5_d32_spherical.png` · `txt_p4_ffc_plateau_below_bo1_and_sm_lower_bo.png` · `txt_p4_vdw_dominates_noncohesive_not_predicted.png` · `txt_p5_fit_bo_gt1_alpha_157_beta_027_and_deviation_sources.png` · `txt_p5_alpha_beta_material_independent_bulk_density_caveat.png` · `txt_p6_mixture_bond_number_definition_absent_from_literature.png` · `txt_p7_combining_rules_weighting_fsa_coordination_number.png` · `txt_p7_p8_binary_prediction_aad_040_disparate_sizes.png` · `txt_p9_sm_binary_aad_099_ternary_034_101_no_mixed_coating.png` · `txt_p9_starch_bo_861_ffc_466_aad_016_013.png` · `txt_p10_conclusions_scope_bo_gt1_and_limitations.png` · `txt_p10_intended_use_phase_map_huang41.png`) | 초록 · vdW 만 · 식 (1) 두 항 · Bo 정의 · 단일 성분만이던 선행 · 혼합 · 코팅 · 환형 전단 · IGC · Bo 계산 가정 · Bo < 1 평탄 · 비점착 제외 · 맞춤 · α β 물질 무관 · 혼합물 정의 · 결합 규칙 · 가중 · 이원 0.40 · 코팅 이원 0.99 · 삼원 0.34 · 1.01 · 혼합 코팅 팔 안 만듦 · 전분 · 결론 · 용도 | 카드가 인용한 숫자 · 정의 · 단정의 근거 (파일 이름의 pN = PDF 쪽) |

## 6. Post-processing ★
- **원문이 한 것**: 표준 식 계산 (식 1–5 · 8–15) · 선형화 최소제곱 (α · β · 95 % 신뢰 · 예측 구간) · AAD · 삼원 예측 색 지도 (MATLAB 꼴 그림 [카드 해석]).  상관계수 · 잔차 분석 · 교차검증은 인쇄되지 않았다.
- **이 카드가 한 것**: ① 표 1 의 A · Bo 재현 (식 4 · 1 · 3 · 5) 과 d32 역산 ② 8 점 맞춤으로 α · β 재현 (7 점 · 5 점 대안과 구분) ③ f_SA 식 역산 · 표 2–5 의 쌍 Bo · Bo_Mix · 예측 재현 ④ 그림 3 · 4 · 6 판독 55 점 (800 dpi · 침식 표지 검출 · 순수 성분으로 축 검증) → 이원 AAD 규약 (끝점 제외) 확인 ⑤ 95 % 예측 구간 재구성 · 구간 밖 점 세기 ⑥ 표 3 AAD 불일치 ⑦ BET ↔ 기하 면적 · 가중 뒤집힘 ⑧ 우리 조성 · 크기로의 이식 산술 (§7-3).  스크립트 = 세션 scratchpad (저장 안 함 · 끝에 지움 — 계산 방법은 각 절의 식 · 판독 방법은 `digitized.csv` 머리말) · 판독 결과 = `digitized.csv`.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 리포 문서 · 덱 생성기 상수를 출처로 적는다)

### 7-1. 비교표 (**모든 행에서 재료 · 관측량이 다르다** — 이 논문 = 제약 분체 8.8–122.5 µm · 공기 중 · 흐름 ↔ 우리 = LPSCl SE 1 µm + NCM 4 · 9 µm · Ar · 혼합 상태 → 300 MPa 압밀 → 이온 망)
| 항목 | 이 논문 | 우리 (믹서 B 계열 · 논지) | 같음 / 다름 · 왜 |
|---|---|---|---|
| 혼합쌍 점착 결합 | Hamaker **기하평균** (식 10 · A ∝ γ_d) | 쌍별 CED = γ 비에서 **기하평균** (논지 §2-1 W_ij ≈ 2√(γ_i γ_j) · 논지 §4 D2) | **같다** |
| 힘 법칙 | Rumpf **다돌기** (돌기 200 nm · F 가 크기에 거의 무관) | SJKR (매끈한 구 · F ∝ W R\*) · 논지 §2-1 JKR (3/2)π W R\* | ★ **다르다** — 거칠기를 넣으면 R\* 기하 이득이 사라진다 (§7-2) |
| 쌍 Bo 분모 | **두 무게의 조화평균** (식 13 → 가벼운 쪽 × 2) | **작은 (가벼운) 쪽 무게** (논지 §2-1 · Figueroa 2009 식 22 · 덱) | ★ **2 배 다르다** (크기비 1 : 9 에서 1.999 배 [우리 산술]) |
| 출력 | 혼합물 ff_c (흐름 · 1 kPa) | 혼합 상태 (Lacey M 16×16×4 · 12×12×3 · 8×8×2 · SE 군집 · AM–SE 접촉 분율) → 압밀 뒤 망 | 관측량이 다르다 — 이 논문은 혼합 상태를 **가정** |
| 접촉 가중 | 표면적 몫의 곱 (무작위 접촉) | DEM 이 실제 쌍 종류별 접촉 수를 준다 | 원문이 *"superior formulation"* 이라 부른 것 (배위수 가중) 을 우리는 **잴 수 있다** |
| 공정 | LabRAM 75 g · 60 Hz · 10 min (한 조건) | 드럼 75.04 rpm · Fr 0.0827 · 2 바퀴 (`li2005_…` §7-1) | 공정 축 둘 다 없음 · 세기 ≈900 배 (가속도 비 [카드 산술]) |
| 표면 에너지 입력 | IGC γ_d 측정 (공기 · RH 32 %) | γ_AM/γ_SE = **0.1 (U)** · γ_W/γ_SE 0.00256 (B1-U · B2-U · `docs/reviews/mixer_b2_u_development_20261122/README.md`) · 코팅 팔 **1 (C)** (지시서 · 논지 §2) — 둘 다 가정값 | 우리 비는 측정이 아니다 (논지 §2-8) |
| 크기 · 밀도 | 8.8–122.5 µm · 1.29–1.56 g/cm³ | SE 1 · AM_S 4 · AM_P 9 µm · 2.00 · 4.80 g/cm³ (논지 §2-3 · 덱 상수 `scripts/make_mixer_deck.py` `DENS` · `D_REAL_UM` — `hersey1975_…` 카드 §3 이 옮긴 값) | 혼합쌍 크기비 (작은 ÷ 큰 d32) 0.072 (APAP–PH 200) – 0.98 (PH 101–전분) ↔ 우리 0.111 (SE–AM_P) · 0.25 (SE–AM_S) · 0.44 (AM_S–AM_P) — 그들 범위 안 |
| 압밀 · 탈압 · 소성 | 없음 (1 kPa) | 300 MPa · 언로딩 | 비교 대상 아님 |

### 7-2. ★ 혼합쌍 Bo 정의 셋 — Capece ↔ Figueroa · 우리 논지 · 덱 [카드 산술 · 1 = SE 1 µm · ρ 2.00 · 2 = AM_P 9 µm (AM_S 4 µm) · ρ 4.80 · 같은 γ (r = γ_A/γ_S = 1)]
| 힘 법칙 × 분모 규약 | Bo(SE–AM_P) ÷ Bo(SE–SE) at r = 1 (AM_S) | '같은 Bo' 문턱 r\* = γ_A/γ_S (AM_S) | 뜻 |
|---|---|---|---|
| 매끈 (d_asp → 0 · F ∝ R\*) × **가벼운 쪽 무게** (논지 · Figueroa · **덱**) | **1.80** (1.60) | **0.309** (0.391) | 우리 논지 §2-3 그대로 · 덱 B-C 의 SE–AM_P 38.2 ÷ SE–SE 21.2 = 1.80 · B-U 12.1 ÷ 21.2 = 0.571 ≈ 1.8·√0.1 (0.569) (`figueroa2009_…` §7-3) |
| 돌기 200 nm (Capece 식 1) × 가벼운 쪽 무게 | **1.08** (1.067) | **0.857** (0.879) | ★ 거칠기가 R\* 기하 이득을 지운다 — SE–SE 우세 조건이 0.31 → 0.86 으로 **훨씬 쉬워진다** |
| 매끈 × **무게 조화평균** (Capece 식 13) | 0.90 (0.81) | 1.23 (1.54) | r = 1 (코팅) 에서도 SE–SE Bo 가 더 크다 |
| 돌기 200 nm × 무게 조화평균 (**Capece 그대로**) | **0.54** (0.54) | **3.43** (3.47) | 코팅 AM 도 SE 를 붙잡지 못하는 것처럼 보인다 — 분모 규약의 인공물 [카드 해석] |

- 산술: Bo_SA/Bo_SS = (F_SA/F_SS) × (W_SS/W_SA) · F_SA/F_SS = g(d_SA)/g(d_SS) (g = 식 (1) 괄호 · d = 조화평균 지름 1.8 · 1 µm) × √r · W_AP/W_S = 9³ × 2.4 = **1,750** (AM_S 153.6) → 조화평균 무게 = W_S × **1.999** (1.987) · 문턱 r\* = (1/(r = 1 에서의 비))².  돌기 16 nm 면 1.026 · 2 nm 면 1.70 (가벼운 쪽 무게) — **돌기가 몇 nm 만 넘어도** 기하 이득이 사라진다 [카드 산술].
- ★ [카드 해석] **어느 분모가 맞나** — 혼합기의 흔듦이 떼려는 것은 **작은 SE 입자** (큰 AM 은 닻) 이므로 '부착이 살아남나' 를 보려면 SE 의 무게 (관성) 가 분모인 Figueroa · 논지 · 덱의 규약이 물리에 맞다.  Capece 의 조화평균 무게는 *"A harmonic mean is also used to define particle weight"* (p.7) 한 문장이 근거이고, 목적 (혼합물 전체의 흐름) 이 다르다 ⇒ **Capece 의 쌍 Bo 를 우리 SE–AM ↔ SE–SE 판정에 쓰지 않는다**.
- ★ [카드 산술] **그러나 힘 법칙 쪽 경고는 그대로 우리에게 걸린다**: 논지 §2-7 이 이미 *"거칠기 · 모양 — 실제 접촉 반경은 입자 반경이 아니라 돌기 반경일 수 있다 (R\* 기하가 약해진다)"* 라고 적었고, 이 논문의 식 (1) 꼴로 크기를 재면 돌기 200 nm (이 논문의 '자연 거칠기' 가정값) 에서 판가름 수가 **0.31 → 0.86 (AM_P) · 0.39 → 0.88 (AM_S)** 로 움직인다 — **P1 (비코팅 SE–SE 응집이 남는다) 이 훨씬 쉬워지고, 코팅의 기하 이득 (SE 가 AM 에 붙는 쪽이 1.8 배 유리) 은 1.08 로 줄어든다** (그러면 코팅 효과는 γ 비 자체 (ΔW = 0) 에서만 온다).  NCM · LPSCl 의 표면 돌기 크기는 [미확인].

### 7-3. ★ 우리 AM + SE 혼합물에 Capece 식을 넣으면 [우리 산술 · 덱 조성 = AM : SE : VGCF : PTFE 80 : 18 : 1 : 1 · P : S 7 : 3 (`scripts/make_mixer_deck.py` `WT` · `PS` — `hersey1975_…` 카드 §3 · 레시피 = `comparison_vs_ours_DEM.md` 의 80:18:1:1) 에서 VGCF · PTFE 를 빼고 정규화 → AM_P 57.1 · AM_S 24.5 · SE 18.4 wt% · 크기 · 밀도 위와 같음 · 돌기 200 nm (원문 가정) · r = 0.1 (U) / 1 (C)]
| 양 | U (γ_A/γ_S 0.1) | C (1) | 뜻 |
|---|---|---|---|
| 표면적 몫 f_SA (d32 기하) | SE **0.780** · AM_S 0.108 · AM_P 0.112 | 같음 | SE 가 표면의 78 % (APAP 가 그들 혼합물에서 차지한 꼴) |
| 접촉 확률 (식 14) | SE–SE **0.608** · SE–AM **0.344** · AM–AM **0.049** | 같음 | ★ '무작위 접촉' 기준선 — 우리 SE 군집 관측량의 분모 후보 (G1) |
| 쌍 Bo ÷ Bo_SE–SE (Capece 규약) | SE–AM 0.17 · AM–AM 1 × 10⁻⁴ – 7 × 10⁻⁴ | SE–AM 0.54 · AM–AM 7 × 10⁻⁴ – 7 × 10⁻³ | AM–AM 은 무겁고 (×1,750–1.7 × 10⁶ 질량) 힘은 비슷 |
| **Bo_Mix ÷ Bo_SE–SE** | **0.0038** | **0.036** | 조화평균이라 **AM–AM 이 1/Bo_Mix 의 99 % (U) · 95 % (C)** 를 차지 — 흐름 지표로서도 굵은 AM 이 정한다 |
| (매끈한 구 · 가벼운 쪽 무게로 바꾸면) | 0.027 | 0.23 | 그때 AM–AM 몫 97 % (U) · 81.5 % (C) · 네 규약 (돌기 200 nm / 매끈 × 조화평균 / 가벼운 쪽) 전체 80–99 % |

- ⇒ [카드 판정] **우리 3 상에 '혼합물 흐름 지표' 로는 계산할 수 있다** (입력 = 상별 d32 · ρ · γ_d (IGC · 불활성) · 돌기 크기 · 질량 몫) — 다만 ① 출력이 흐름 (덮임 · 군집 아님) ② α · β 는 제약 분체 8 점 맞춤 ③ 조화평균이라 AM–AM 이 지배 → **코팅 (γ_AM ↑) 은 이 지표로 Bo_Mix 를 약 10 배 키운다 = '덜 흐른다'** 는 예측이 나온다 (논지의 '코팅 → 분산이 좋아짐' 과 다른 축 · 모순이 아니다 — 흐름 ↔ 분산).
- ⇒ [우리 산술] **절대 Bo**: 실제 1 µm LPSCl 입자를 이 식으로 (γ_d 30–50 mJ/m² 가정 — 이 논문 재료의 범위 · LPSCl 값 [미확인]) 넣으면 F_SE–SE ≈ **16–27 nN** · 무게 10.3 fN → **Bo ≈ 1.6–2.6 × 10⁶** — 이 논문 맞춤 범위 (≤ 4.77 × 10³) 의 330–550 배 밖 · 우리 덱 Bo_SE (B1-U **0.21244** · B2-U **21.244** · `docs/reviews/mixer_b2_u_development_20261122/README.md`) 는 거친 입자 parcel 의 **설계값** 이라 이 숫자와 같은 양이 아니다 (5–7 자릿수 차).

### 7-4. 공정 축 — 이 논문은 진동 혼합 한 점
- LabRAM 75 g · 60 Hz · 10 min (코팅도 같은 조건) — [카드 산술] 정현 진동이면 변위 진폭 a/(2πf)² ≈ **5.2 mm** · 속도 진폭 a/(2πf) ≈ **1.95 m/s** ↔ 우리 드럼 벽 속도 ≈0.10 m/s (논지 §2-6 '벽 속도 103 mm/s') · Fr 0.0827.
- 원문은 혼합 세기 · 시간을 바꾸지 않았다 — 공정 축 정보 0.  다만 **혼합과 코팅을 한 단계로** (성분 + R972 동시 투입) 했고, 코팅 분체와 비코팅 분체를 섞는 팔은 **나노 입자 이동** 때문에 만들지 않았다 (p.9) — 우리 '코팅 AM + 비코팅 성분' 혼합에서도 같은 이동 (SE 의 숙주 간 이동) 이 관측 대상이다.

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 압밀 **전** 단계 (혼합물 흐름) 를 쌍 점착 (결합 규칙 · 표면 에너지 측정) 으로 잇는 해석 사슬 · 그 사슬의 실험 검증 꼴 (맞춤 밖 성분 · 혼합물) · '무작위 접촉 확률' 기준선.
- **없는 것**: 혼합 상태 · 입자 수준 관측 · 공정 축 · 압밀 · 탈압 · 수송 · 계산 모델.  DEM · MPM 어느 쪽의 검증 표적도 아니다 — 우리 믹서 트랙 (Ⓒ) 의 **정의 · 규약 · 관측량 설계** 쪽에 쓴다 (frame[4]: 이 논문의 모형은 자기 실험에 맞춘 것이라 우리 모델과 맞추지 않는다).

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 = 제약 분체의 **혼합물 흐름** — 압밀 · 기공 숫자가 없어 랩 표준과 나란히 놓을 값은 없다 · 모든 행에 "재료 다름 · 관측량 다름".)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (관측량 · 판정 기준을 결과 전에) | ★ ① **쌍 Bo 의 분모 규약** (가벼운 쪽 무게 ↔ 조화평균) 과 **힘 법칙** (매끈 R\* ↔ 돌기) 을 결과 전에 적는다 — 규약만 바꿔도 SE–AM ↔ SE–SE 순서가 바뀐다 (§7-2) ② **표면적 가중의 면적 정의** (d32 기하 ↔ BET) 를 적는다 — APAP–PH 200 50 : 50 에서 가중이 0.94 → 0.20 으로 뒤집힌다 (§3-1) ③ **AAD · 오차 보고에 끝점 포함 여부** 를 적는다 (원문은 안 적었고 판독으로만 밝혀짐) | 기공 연산자 · 압밀 판정선 없음 |
| **단계 1 · 2 · 3** | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 맞춤) | 없음 — 1 kPa 환형 전단은 흐름 시험이지 압밀이 아니다 | 항복 · 경도 · 밀도 없음 |
| **단계 5** (3D 복합 압밀) | 간접 — 압밀 전 혼합 침대의 '접촉 확률' 기준선 (표면적 몫의 곱 · 우리 조성 SE–SE 0.608 · SE–AM 0.344 · AM–AM 0.049 [우리 산술]) 을 압밀 DEM 출발 배치의 무작위 대비 지표로 | 압밀 · 하중 몫 없음 |
| **단계 6 · 7** | 없음 | — |
| **후보 D0** (지금 DEM · 믹서 덱) | ★ ① 덱의 결합 규칙 (기하평균) 이 이 논문과 같다 ② 덱의 힘 법칙 (SJKR · F ∝ R\*) 은 **매끈한 구** — 돌기가 지배하면 SE–AM 기하 이득이 1.8 → 1.08 (§7-2) → '거칠기 민감도' 를 덱 설계의 알려진 한계로 적는다 ③ 덱 Bo 는 parcel 설계값 — 실입자 Bo (≈10⁶) 와 섞지 않는다 | 압밀 DEM (E_eff 1.35) 과 무관 |
| **후보 A′-0 · A · A′ · B · C · C′ · M0** | 없음 (접촉 역학 · 소성 · 균질화 없음) | — |
| **U0–U6** | 없음 | — |
| **R1–R7** | 없음 | — |
| **결과 전 대조 항목** | ① 판가름 수 감도 표 (매끈 · 가벼운 쪽 0.31 / 0.39 · 돌기 200 nm 0.86 / 0.88) 를 B2-U · B2-C 판독 **전** 에 등록 ② 혼합물 흐름 (ff_c) 을 혼합 품질로 쓰지 않는다 (이 논문은 혼합 상태를 가정) | 숫자 표적은 옮기지 않는다 |
| **흐름 밖: Ⓒ 코팅 활물질 믹싱** (믹서 논지 · 11-23 결정) | ★ ① **다성분 Bo 의 원전** — 정의 · 결합 · 가중 식 (8)–(15) 을 인용 (G2 · G4 좁히기) ② **'따로 잰 표면 에너지 → 혼합물 결과' 선례 (결과 = 흐름)** → 우리 novelty 를 '혼합 **상태** · 압밀 뒤 수송 · 쌍별 AFM' 으로 좁힌다 ③ **거칠기 경고의 정량화** (판가름 수 0.31 → 0.86) ④ **배위수 가중 (원문의 'superior')** 을 DEM 으로 잰다 ⑤ 코팅 숙주 간 이동 (p.9) 을 관측량으로 | 회전 속도 · 입자 수준 맞교환 · 혼합 상태 예측 · 코팅 DEM 은 **없다** (§0-2 G1 · G3) |

- **재료 · 차원 · 조건 차이**: 유기 약물 · 셀룰로오스 · 전분 (8.8–122.5 µm · 1.29–1.56 g/cm³) ↔ LPSCl 1 µm (2.00) + NCM 4 · 9 µm (4.80) · 공기 RH 32–33 % ↔ Ar 건조 · 1 kPa 흐름 ↔ 300 MPa 압밀 · 진동 75 g ↔ 드럼 Fr 0.083 · ff_c ↔ (Lacey M · 군집 · 접촉 · 기공 · f_ion).

## 9. 적용 인사이트 (행동)
1. **논지 §2-3 판가름 수에 '거칠기 감도' 한 줄을 단다 (Ⓒ · 결과 전 대조)** — 매끈한 구 JKR 의 0.31 (AM_P) · 0.39 (AM_S) 는 돌기가 지배하는 접촉 (이 논문의 Rumpf 다돌기 식 · 돌기 200 nm) 에서는 **0.86 · 0.88** 로 옮겨 간다 [카드 산술 §7-2].  NCM · LPSCl 표면 돌기 크기 (AFM 지형) 를 같은 측정 묶음에 넣는다.
2. **쌍 Bo 의 분모 규약을 덱 · 등록 문서에 명시한다 (단계 0)** — 우리는 '가벼운 쪽 무게' (Figueroa · 논지 · 덱) 를 쓴다 · Capece 의 조화평균 무게는 크기비 1 : 9 에서 혼합쌍 Bo 를 절반으로 만든다 → 문헌 값을 옮길 때 규약 변환을 같이 적는다.
3. **믹서 판독에 '쌍 종류별 접촉 수' 를 등록한다** — 원문이 *"may offer a superior formulation"* 이라 한 배위수 가중을 DEM 은 직접 준다 → 접촉 가중 혼합물 Bo(t) (흐름 쪽 관측량) 와 표면적 가중 기준선 (무작위 접촉 · §7-3) 을 나란히.
4. **'무작위 대비 SE 군집' 의 분모로 표면적 몫의 곱을 쓴다** — 우리 조성 SE–SE 0.608 · SE–AM 0.344 · AM–AM 0.049 [우리 산술] = 무작위 접촉 확률의 한 정의 (원문 식 14) · 실측 쌍 접촉 분율이 이 값에서 얼마나 벗어나는지가 응집 · 덮임의 신호다.
5. **표면적은 기하 (d32) 와 BET 를 둘 다 적는다** — NCM 2 차 입자는 다공이라 BET ≫ 기하일 것 (이 논문 MCC 37.6 배 · 전분 5.5 배) → 원문이 성공한 규약은 기하 면적.
6. **흐름 지표로 혼합 품질을 대신하지 않는다** — 이 논문의 Bo_Mix 는 '잘 섞인' 가정 위의 흐름 예측 · 코팅 (γ_AM ↑) 은 이 지표에서 **덜 흐르는** 쪽 (Bo_Mix ×10) 으로 나온다 → 논지 P2 (분산) 와 다른 축이라고 결과 전에 적는다.
7. **코팅 팔 설계: 숙주 간 이동을 관측량으로** — 원문은 코팅 분체 ↔ 비코팅 분체 혼합을 *"the likelihood of R972 transferring from coated particles to as-received particles"* 때문에 피했다 (p.9) → 우리 DEM 은 SE 입자의 '붙은 AM id' 이력으로 이동을 잴 수 있다.
8. **보고 규약** — 예측 오차는 '끝점 포함 / 제외' · 'AAD / 상대 편차 / 치우침' 을 같이 (이 논문 이원 AAD 0.40 · 0.99 · 0.16 은 끝점 제외 · 상대 편차 16 · 12 · 7.5 % · 코팅 이원 치우침 −0.69 [판독 + 카드 산술]).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Capece et al. defined a granular Bond number for powder blends as the surface-area-weighted harmonic mean of the pair Bond numbers, Bo_g,Mix = (Σ_i Σ_j f_SA,i f_SA,j / Bo_g,ij)^−1, with a geometric-mean Hamaker constant and harmonic-mean particle diameter, asperity size and weight for dissimilar pairs; with ff_c = 15.7·Bo^−0.27 fitted on single powders it predicted the ring-shear flow function coefficient of binary, ternary and quinary pharmaceutical blends with average absolute deviations of 0.13–1.01 (*Powder Technol.* 286 (2015) 561–571)." [인쇄 p.6–10 · 식 7–15]
- "In that framework the blend is assumed to be well mixed and the contact probability is the product of fractional surface areas; the mixing state itself is not predicted (Capece et al. 2015)." [인쇄 p.7]
- 국문 (한정어와 함께): *"혼합물의 Bond 수를 모든 쌍의 Bond 수의 표면적 가중 조화평균으로 정의하면 제약 분체 혼합물의 흐름을 입자 성질만으로 예측할 수 있었다 (Capece 2015 · 평균 절대 편차 0.13–1.01) — 다만 그 틀은 잘 섞인 혼합물을 가정한 흐름 예측이고, 혼합 상태 (덮임 · 분리) 를 예측하지 않는다."*
- 국문 (금지 표지): *"Capece 2015 의 쌍 Bond 수 (무게 조화평균 · 돌기 200 nm) 를 우리 SE–AM ↔ SE–SE 부착 판정에 그대로 쓰지 않는다 — 분모 · 힘 법칙 규약이 달라 순서가 뒤집힌다."*
- ⚠ §7-2 · §7-3 의 환산 (판가름 수 0.86 · Bo_Mix 몫 · 실입자 Bo ≈10⁶) 은 **[카드 산술 · 우리 산술]** — 원문 값으로 인용하지 않는다.

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. ★ **혼합 상태를 가정한다** — 출력은 흐름 (ff_c) 하나 · 혼합 균일도 · 분리 · 덮임은 재지도 예측하지도 않았다 (가중 = 무작위 접촉).
2. ★ **돌기 200 nm 를 모든 분말에 가정** — 측정 없음 · 그런데 힘 (따라서 Bo) 은 이 값에 거의 비례한다 (d_p ≫ d_asp) — 저자도 한계로 적었다 (p.10).
3. ★ **쌍 무게 조화평균의 근거가 한 문장** — 크기비가 클수록 혼합쌍 Bo 를 2 배까지 낮춘다 (§7-2) · 대안 (가벼운 쪽 무게 · 배위수 가중) 과 견준 시험 없음.
4. **α · β = 8 점 맞춤** (as-received 5 + 코팅 3 · 같은 물질 계열 · 전분 1 종으로만 맞춤 밖 확인) · 물질 무관성은 저자 스스로 *"should be confirmed"* (p.5).
5. **통계가 AAD 하나** — 상관계수 · 교차검증 · 사전 등록 없음 · 이원 AAD 는 끝점 제외 규약 (미기재) · **코팅 삼원 1.01 은 표 3 으로 재현 안 됨 (1.37)**.
6. **γ_d 의 출처가 섞였다** — 셋은 이 논문 IGC (APAP · PH 200 · Starch) · PH 105 · 101 · 102 와 코팅값 34.00 은 Huang [26] (조건 [미확인]) · 분산 성분만 (극성 · 산 · 염기 · 정전기 · 모세관 빠짐 · RH 32–33 %).
7. **ff_c 는 흐름의 일부** — 부피밀도 · 실제 응력이 빠짐 (저자: *"cannot be used as a stringent prediction of flowability"*).
8. **혼합 · 코팅 한 조건 · 혼합 코팅 팔 없음** — 공정 축 0 · 코팅의 균일 분배는 가정.
9. **전이 한계**: 제약 분체 · 공기 중 · 1 kPa · 진동 75 g — 우리 황화물 · NCM · Ar · 드럼 · 압밀로 α · β · Bo 숫자를 옮기지 않는다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| [21] | Y. Chen, J. Yang, R. Dave, R. Pfeffer, Fluidization of coated group C powders, AICHE J. 54 (2008) 104–121. | ★ 식 (1) 다돌기 모형 · 식 (5) 코팅 돌기 힘 · 1 % R972 선택의 원전 — 카드 없음 |
| [25] | L. Jallo, Y. Chen, J. Bowen, F. Etzler, R. Dave, Prediction of inter-particle adhesion force from surface energy and surface roughness, J. Adhes. Sci. Technol. 25 (2011) 367–384. | ★ 표면 에너지 + 거칠기 → 점착력 예측의 AFM 검증 (돌기 가정의 근거 · 우리 AFM 설계) — 카드 없음 |
| [23] | M. Capece, Z. Huang, D. To, M. Aloia, C. Muchira, R. Davé, A. Yu, Prediction of porosity from particle scale interactions: surface modification of fine cohesive powders, Powder Technol. 254 (2014) 103–113. | 같은 1저자 · Bo → 충전 기공률 (압밀 전 출발 침대) — 카드 없음 |
| [24] | A. Yu, C. Feng, R. Zou, R. Yang, On the relationship between porosity and interparticle forces, Powder Technol. 130 (2003) 70–76. | 기공률 ↔ 입자간 힘 (Bo) 의 원 관계 — 카드 없음 |
| [17] | Castellanos, The relationship between attractive interparticle forces and bulk behaviour in dry and uncharged fine powders, Adv. Phys. 54 (2005) 263–376. | 입상 Bond 수의 정의 · 리뷰 (deng2021 카드도 인용) — 카드 없음 |
| [26] | Z. Huang, J. Scicolone, L. Gurumuthy, R. Davé, Flow and bulk density enhancements of pharmaceutical powders using a conical screen mill: a continuous dry coating device, Chem. Eng. Sci. (2014) http://dx.doi.org/10.1016/j.ces.2014.05.038. | 표 1 의 γ_d 넷 (PH 105 · 101 · 102 · 코팅 34.00) 의 출처 · Bo ↔ ff_c 선행 |
| [41] | Z. Huang, J. Scicolone, X. Han, R. Davé, Improved blend and tablet properties of fine pharmaceutical powders via dry particle coating, Int. J. Pharm. 478 (2015) 447–455. | 부피밀도 × ff_c 상태도 (G4 의 저자 제안) |
| [28] | R. Pfeffer, R. Dave, D. Wei, M. Ramlakhan, Synthesis of engineered particulates with tailored properties using dry particle coating, Powder Technol. 117 (2001) 40–67. | ✅ 정본 카드 `pfeffer2001_dry_particle_coating_engineered_particulates` |
| [18] | F. Podczeck, Particle–Particle Adhesion in Pharmaceutical Powder Handling, Imperial College Press, London, 1998. | 조화평균 지름 · 정전기 10 배 약함의 근거 |
| [33] · [34] | J. Schultz, L. Lavielle, C. Martin, … J. Adhes. 23 (1987) 45–60 · J. Israelachvili, Intermolecular and Surface Forces, Academic Press, London, 1992. | IGC 분산 표면 에너지 · D0 0.165 nm |
| [30] · [32] | D. Schulze, Powder and Bulk Solids … 2008 · A. Jenike, Storage and flow of solids, Bull. No. 123 … 1964. | ff_c 규약 |

## 13. [미확인] 목록 (원문 11 쪽 전수에 없음)
1. 돌기 크기의 측정 (200 nm · 16 nm 는 가정 · 문헌값) · 거칠기 분포.
2. 표면적 몫 f_SA 의 식 (카드가 역산 · §3-6) · g 값 · 무게 계산의 세부.
3. Huang [26] γ_d 의 측정 조건 · 코팅 분체의 γ_d 34.00 이 R972 값인지 코팅 분체 값인지.
4. 회귀 통계 (R² · 잔차 · 매개변수 불확도) · 이원 AAD 의 끝점 규약 · 코팅 삼원 AAD 1.01 의 계산 규약.
5. 혼합 균일도 · 혼합물 SEM · R972 분배 · 혼합 시간 · 세기 감도.
6. ff_c 의 관례 구간 (자유 흐름 등) · 부피밀도 · 압밀 응력 σ1 값.
7. 단일 분말 반복 (표준 오차만 · n = 3) 밖의 재현성 · 다른 예압.
8. NCM · LPSCl 의 γ_d · 돌기 크기 (이 카드 §7 산술의 가정 · 원문과 무관).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-24)
- PDF 11 쪽 전수를 글자 층 (`pymupdf` text) + 쪽 렌더로 읽었다 (식은 글자 층이 깨져 렌더에서 옮김).  서지 = p.1 머리 (제목 · 저자 넷 · 소속 · 접수 · 온라인 · 판권 줄 `http://dx.doi.org/10.1016/j.powtec.2015.08.031`) · PDF 메타 제목도 같다.  SI 없음.
- **원문 낱말 셈** (글자 층 · 참고문헌 앞 · 대소문자 무시): `DEM` (낱말) · `discrete element` · `simulat` · `finite element` · `plastic` · `segregat` · `rotat` · `rpm` = **0 회** · `yield` 12 회 (전부 흐름 시험의 뜻 — *yield locus* · *unconfined yield strength* · *to yield or flow*) · `deform` 2 회 (p.2 모형 목록 *"particle deformation behavior"* · p.5 한계 문장) · `compress` 2 회 (둘 다 *direct compression* 정제) · `porosity` 3 · `mixing` 7 · `coating` 14 · `asperit` 19 · `Hamaker` 8 · `coordination` 2 · `Bond number` 72 (줄끝 하이픈 이음) · `agglomerat` 3 · 참고문헌 41.
- **크롭 47 장** = 도구 11 (Figs. 2–7 · Tables 1–5) 을 **전부 다시 자름** (그림 = 단 · 쪽 폭 빈 여백 · 표 = 쪽 전체 · 표 4 · 5 는 같은 p.10 쪽) + Fig. 1 손 크롭 (캡션 글자 덩어리가 오른쪽 단 본문과 한 덩어리라 도구가 못 잡음) + 식 15 + 근거 문단 20 (12 장은 단 · 쪽을 넘는 이어진 조각 2–4 개를 쌓음 · 첫 판에서 문장이 끊긴 것은 이어지는 조각을 붙여 다시 자름).  47 장 전부 열어 확인 · `figures.json` 의 `recrop` · `manual_crop` · `viewed` · `pieces`.  도구가 고친 남의 카드 `_sources` 항목 (choi2018 등) 은 되돌리고 이 slug 한 항목만 더했다.
- **재현 · 판독**: 표 1 의 A (식 4) · Bo (식 1 · 3 · 5) · 8 점 맞춤 α β · 표 2–5 의 f_SA · 쌍 Bo · Bo_Mix · 예측 ff_c 를 재현 (§3-3 · §3-4 · §3-6) · 그림 3 · 4 · 6 표지 55 개 판독 (`digitized.csv`) → 이원 AAD 0.405 · 0.999 · 0.166 (끝점 제외) · 표 3 AAD 1.37 (인쇄 1.01 재현 안 됨).
- 정본 litdb 중복 확인: `litdb/papers/` 623 파일 목록 + `git grep -i` (DOI `powtec.2015.08.031` · `Capece` · `multi-component granular`) — 카드 없음 (인용만: alizadeh2018 L274 · deng2021 L208 · L323) (2026-11-24).
- 2 차 인용 대조: alizadeh2018 · deng2021 의 서지 · '왜' 칸 (§0-1 끝 표) — 고치지 않았다 (정독 출력 `batch_155_findings.md` 의 '카드 문제' 절).

## 🔗 관련 카드
- 쌍별 Bond 수 · 혼합 ↔ 분리 (같은 해석 재료 · 다른 분모 규약 — 가벼운 쪽 무게): [`figueroa2009_vdw_adhesion_mixing_segregation_bond_number_phase_diagram`](figueroa2009_vdw_adhesion_mixing_segregation_bond_number_phase_diagram.md) · [`li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy`](li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy.md) · [`li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation`](li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation.md) · [`li2006_cohesive_mixing_shear_cell_collision_number_phase_diagram`](li2006_cohesive_mixing_shear_cell_collision_number_phase_diagram.md).
- Bond 수 원 정의 · 측정: [`nase2001_granular_bond_collision_number_wet_cohesion`](nase2001_granular_bond_collision_number_wet_cohesion.md) · [`deng2021_mechanical_surface_energy_tester_bond_number`](deng2021_mechanical_surface_energy_tester_bond_number.md) (이 논문 = 그 ref [10]).
- 이 논문을 인용한 카드 (가리킨 카드): [`alizadeh2018_dem_adhesion_calibration_segregation_heap`](alizadeh2018_dem_adhesion_calibration_segregation_heap.md) (ref 27 · L274).
- 표면 에너지 · 점착 측정: [`mohammadijam2014_inverse_gas_chromatography_review`](mohammadijam2014_inverse_gas_chromatography_review.md) (IGC · Schultz) · [`begat2004_cohesive_adhesive_balance_afm_colloid_probe`](begat2004_cohesive_adhesive_balance_afm_colloid_probe.md) · [`jones2008_cohesive_adhesive_balance_carrier_dpi_performance_slightly_cohesive_optimum`](jones2008_cohesive_adhesive_balance_carrier_dpi_performance_slightly_cohesive_optimum.md) · [`johnson1971_jkr_surface_energy_contact_elastic_solids`](johnson1971_jkr_surface_energy_contact_elastic_solids.md).
- 나노 건식 코팅 · 정렬 혼합: [`pfeffer2001_dry_particle_coating_engineered_particulates`](pfeffer2001_dry_particle_coating_engineered_particulates.md) (ref [28]) · [`hersey1975_ordered_mixing_concept`](hersey1975_ordered_mixing_concept.md).
- 유동성 시험 (D3 앵커 쪽): [`geldart2006_powder_flowability_angle_of_repose_tester`](geldart2006_powder_flowability_angle_of_repose_tester.md) · [`molerus1975_theory_of_yield_cohesive_powders`](molerus1975_theory_of_yield_cohesive_powders.md).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
