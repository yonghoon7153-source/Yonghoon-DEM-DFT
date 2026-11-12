<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 1저자 11-12 후보 표 N-23) 에서 꼭 뽑으라고 한 항목.
     본 = sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile.md (NCM 기계 물성 · 나노압입 카드의 꼴 · 2 차 인용 매핑 · 우리 E_AM / H_AM 대조) ·
     두 필수 절 (§0-1 고른 의도 대조 · §8 자세한 분석) 은 같은 묶음의 sakka2022 · park2025 · jeong2024 카드와 같은 꼴.
     원문 = 출판본 (Extreme Mechanics Letters 9 (2016) 495–502 · 8 쪽 · © 2016 Elsevier Ltd) · 보충 자료 (SI) 없음 (본문에 SI 언급 없음).
     쪽 표기 = "p.n" = PDF 쪽 n (학술지 쪽 = 494 + n · p.1 = 495 … p.8 = 502).  크롭 파일 이름의 pN · figures.json 의 page 는 PDF 쪽이다.
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독 · 벡터] = 그림 3b · 3c · 4 · 6 · 3a 삽입도는 **벡터 경로**라 좌표를 축 틀 (검은 선 · 눈금) 로 환산한 값 (재현 = litdb/figures/<slug>/digitized.csv 287 행 · 정밀도 ≈ 그림 선 굵기) ·
     [카드 판독] = 원문에 없는 양을 이 카드가 그림에서 끌어낸 값 (예: 막대 높이의 공통 단위 1/N) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) ·
     [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본 다른 카드에 적힌 값 (slug 병기) · [우리] = 우리 쪽 값 (작업 트리 파일 · CLAUDE.md 출처) · [미확인] = 본문 8 쪽 전수에 없음.
     원문 8 쪽은 글자 층 (pdftotext layout · raw · PyMuPDF 줄 좌표) + 전 쪽 렌더로 읽었다.  눈금 숫자 · 축 이름은 그림 안에서 글자가 아니라 경로 (glyph path) 라 렌더로 확인했다.
     계산 · 모델은 없다 — 실험 (Berkovich 나노압입 · 격자 (grid) 압입 · 통계 분해 · 질량-두께 기공) 만. -->

# NMC532 · PVDF · CB (90 : 5 : 5 wt%) 양극 (액체계 LIB 용 · 캘린더링 안 함 · 기공 56 %) 의 상별 탄성률 · 경도 — 단일 입자 targeted 압입 (깊이 창 75–150 nm) **E 138.73 ± 18.78 · H 8.89 ± 1.86 GPa** · 별도 CB/PVDF (50/50 wt% · 기공 61 %) 필름 **E 1.78 ± 0.35 · H 0.043 ± 0.01 GPa** · 깊이 100 nm 격자 압입 + 3 상 Gaussian CDF 분해 = 입자 123.02 ± 20 · 기지 4.40 ± 2 · '계면' 45.24 ± 27.58 GPa (표면 분율 38.40 · 15.64 · 45.96 %) — de Vasconcelos · Xu · Li · Zhao (Extreme Mech. Lett. 9 (2016) 495–502)

> slug `devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode` · DOI `10.1016/j.eml.2016.03.002` · type `exp (instrumented nanoindentation: Keysight G200 Berkovich, Oliver–Pharr, constant strain rate 0.05 1/s, 5 s hold, nu 0.3 assumed; targeted indentation on single NMC532 particles (depth sweep 50–420 nm) + separate CB/PVDF 50/50 films (350 tests, 200–2200 nm); grid indentation at 100 nm depth + statistical deconvolution (tri-modal Gaussian CDF fit, shared surface fractions, genetic algorithm); mass–thickness porosity of uncalendered electrodes — no model)` · PDF `ee82444d-23._Grid_indentation_analysis_of_mechanical_properties_of_composite_electrodes_in_Li-ion_batteries.pdf` (8 쪽 · SI 없음) · digested `2026-11-12` · status ✅

> elements: Li, Ni, Mn, Co, O

> **저자**: **Luize Scalco de Vasconcelos** ᵃ · Rong Xu ᵃ · Jianlin Li ᵇ · **Kejie Zhao\*** ᵃ — ᵃ School of Mechanical Engineering, Purdue University (West Lafayette, IN 47906) · ᵇ Energy and Transportation Science Division, Oak Ridge National Laboratory (Oak Ridge, TN 37831-6479) — \* 교신 (kjzhao@purdue.edu) · *Extreme Mechanics Letters* **9** (**2016**) **495–502** · 접수 2016-01-28 · 수정본 2016-03-06 · 승인 2016-03-07 · 온라인 2016-03-09 (p.1) · 키워드 NMC cathode · Grid indentation · Statistical analysis · Mechanical properties · Batteries · 연구비 = Purdue 착수 연구비 · 3M nontenured faculty award (K.Z.) · ORNL (UT-Battelle, DOE 계약 DE-AC05-00OR22725) 의 DOE Battery Manufacturing R&D Facility (EERE Vehicle Technologies Office) 가 **전극 시료를 만들었다** (p.7).  쪽 머리글의 저자 표기는 *"L.S.d. Vasconcelos et al."* — 그래서 인용하는 논문들이 *"Vasconcelos et al."* 로 적는다.
> **이웃 카드 (링크만)**: [`sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile`](sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile.md) (참고 [28] = 이 논문 · "139 GPa · H 8.9") · [`wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn`](wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn.md) (참고 [26] = 이 논문 · 138.73 · 1.78 을 FE 입력으로) · [`xu2017_nmc532_nanoindentation_modulus_hardness_toughness`](xu2017_nmc532_nanoindentation_modulus_hardness_toughness.md) (같은 그룹 · NMC532 이차입자 142.5 · CB+PVDF 기지 1.78 · 0.043 같은 값) · [`sharma2023_nmc_single_crystal_anisotropic_nanoindentation`](sharma2023_nmc_single_crystal_anisotropic_nanoindentation.md) (같은 그룹 · 참고 [24] = 이 논문) · [`stallard2022_cathode_mechanical_properties_review`](stallard2022_cathode_mechanical_properties_review.md) (양극재 압입 리뷰) · [`shi2019_high_am_loading_particle_size_assb`](shi2019_high_am_loading_particle_size_assb.md) (참고 [2] = 이 논문 · DEM 입력 귀속) · [`xu2023_realistic_am_shape_cgmd_calendering`](xu2023_realistic_am_shape_cgmd_calendering.md) (E_AM 135 의 출처 묶음에 "grid indentation") · LPSCl 쪽 압입 = [`lee2025_heckel_argyrodite_powder_densification_nanoindentation`](lee2025_heckel_argyrodite_powder_densification_nanoindentation.md).
> **판독 원자료**: `litdb/figures/devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode/digitized.csv` (287 행 — 그림 3c 깊이별 E · H 14 (평균 · SD · 깊이 SD) · 그림 4 CB/PVDF 14 · 그림 3a 삽입도 하중–변위 52 · 그림 3b 막대 93 + N 추정 6 · 그림 6a · 6c 경험 CDF 십자 104 + 분모 추정 2 · 표 2 혼합 CDF ↔ 그린 맞춤 곡선 · 십자 대조 8) · 그림 크롭 **40 장** (도구 8 전부 다시 자름 · 손 크롭 32 = 패널 18 · 식 3 · 근거 문단 11) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: Purdue (Zhao 그룹) 이 ORNL 에서 슬롯다이로 만든 **캘린더링하지 않은** NMC532 (Toda America) 90 · PVDF (Solvay 5130) 5 · CB (Denka) 5 wt% 양극 (적재 12.5 mg/cm² · 두께 45–57 µm · 질량-두께 기공 평균 56 %) 의 윗면을 연마해 Keysight G200 · Berkovich 로 눌렀다 — ① **지름 > 8 µm 입자 한가운데를 고른 targeted 압입**을 최대 깊이 50–420 nm 로 바꿔 가며 E · H 의 깊이 의존을 보고, 표면 · 장비 영향 (< 75 nm) 과 주변 기지 · 입자 내부 기공 영향 (> 150 nm) 사이의 **창 75–150 nm** 평균을 **E 138.73 · H 8.89 GPa** 로 냈고 (p.4 · 표 2 의 ± = **18.78 · 1.86**), ② 기지는 전극 안에서 바로 누르면 아래에 묻힌 NMC 를 건드리므로 **따로 만든 CB/PVDF 50/50 wt% 필름 (기공 61 %)** 에 350 회를 눌러 **E 1.78 · H 0.043 GPa** (± 0.35 · 0.01) 를 냈으며, ③ 전극 위 33 × 33 µm 에 **깊이 100 nm 로 121 회** 격자 압입을 하고 E · H 의 누적 분포를 **같은 표면 분율을 공유하는 세 Gaussian** (입자 · 기지 · '계면') 으로 동시에 맞춰 (식 3 · 유전 알고리즘 150 세대 × 3000 점) **입자 123.02 ± 20 · 기지 4.40 ± 2 · 계면 45.24 ± 27.58 GPa** (H 7.78 ± 1.40 · 0.13 ± 0.01 · 1.44 ± 1.42) · 표면 분율 **38.40 · 15.64 · 45.96 %** 를 얻었다 (표 2).  입자 값은 두 방법이 **11 % 안** (123.02 / 138.73 = 0.887 [카드 산술]) 에서 맞고, 기지 값은 격자 쪽이 **2–3 배 크다** — 저자 해석 = 얕은 압입도 표면 아래에 묻힌 NMC 를 건드린다 (p.7).
⇒ **"138.73 ± 18.78 GPa (NCM) · 1.78 ± 0.35 GPa (CB/PVDF)" 는 이 논문의 값이 맞다 — 단 둘 다 *targeted* 값이고 (격자 값은 123.02 · 4.40), NCM 은 NMC532 (NCM811 아님) 이며, 1.78 은 *전극 속 기지* 가 아니라 *따로 만든 61 % 다공 CB/PVDF 필름* 의 값이다.**

| 1저자가 꼭 뽑으라고 한 것 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 전극 — 조성 · 바인더 · 도전재 · 처리 | **NMC532** (LiNi₀.₅Mn₀.₃Co₀.₂O₂, Toda America) **90** · **PVDF** (Solvay 5130) **5** · **CB** (Denka, powder grade) **5 wt%** · NMP (Sigma Aldrich) 용매 · **슬롯다이 코팅** (제조법 = 참고 [40], ORNL Battery Manufacturing R&D Facility) · NMC 적재 **12.5 mg/cm²** · 전극 두께 (Al 제외) **45–57 µm** (그림 2c) · NMC = 거의 구형 이차입자 **평균 지름 ≈10 µm** (추정 · SEM) · 일차입자가 촘촘히 뭉친 입자 (그림 2b) · **"As-prepared samples were not calendered."** (p.3) · 윗면 연마: 유리판에 Crystalbond 로 붙이고 **3 · 1 µm 다이아몬드 페이스트** (+ microid diamond extender) → **0.05 µm 콜로이드 실리카** · 기공 (식 1, 질량-두께) **55.32 · 55.86 · 57.15 % (평균 56 %)** · CB/PVDF 50/50 wt% 필름 (Al 위 · 두께 17.74 µm) **61.39 · 63.71 · 57.95 % (평균 61 %)** (표 1) · 전해질 · 리튬화 이력 **없음** (as-prepared · 건조 시료) | [인쇄] p.2–3 · 표 1 · 그림 2 |
| ② ★ 격자 압입 — 장비 · 압자 · 깊이 · 간격 · 점 수 | **Keysight G200** · **Berkovich** · 일정 변형률 속도 **0.05 s⁻¹** · 최대 하중 유지 **5 s** · 해석 ν **0.3 (가정)** · Oliver–Pharr [42] (p.3–4) · 격자 깊이 **100 nm 고정** (p.5; 방법 절은 *"typically 100 nm"* p.4) · 간격 **3–5 µm** (p.4) · 지도 (그림 5) = **33 × 33 µm 에 121 회** (p.5) → 11 × 11 이면 간격 3.3 µm [카드 산술] · ⚠ **통계 분해 (그림 6) 에 쓴 압입 수는 원문에 없다** — 그림 6a · 6c 경험 CDF 의 높이가 전부 **1/243 의 정수배** (51 · 53 점 · 최대 어긋남 0.06 · 0.07 개) [카드 판독] → 분해에 쓴 표본은 121 이 아니라 **≈243** 으로 보인다 (§3-6) | [인쇄] p.3–5 · [카드 판독] 그림 6 |
| ③ ★ 상별 E · H ± · 분포 · 분리법 | **표 2** (아래 §3-6 표) · 분리법 = **누적분포 (CDF) 맞춤** — 상마다 Gaussian CDF (식 2) 를 표면 분율 f_i 로 섞은 함수를 E · H 의 실험 CDF 에 **동시에** 맞춘다 · **f_i 는 E 와 H 가 공유** (식 3) · 상 3 개 = 입자 · 기지 · **'계면'** (*"Such mixed regions are referred as interface, the third constituent phase"* p.6) · 최적화 = **유전 알고리즘 150 세대 × 3000 점** (p.6) · 초기 범위 = 그림 5 등고선에서 입자 **120–160 GPa** · 기지 **0.1–10 GPa** (p.6) · 분포 = 그림 6 (CDF · PDF) · targeted 깊이별 분포 = 그림 3b (50 · 100 · 150 nm) · 깊이 의존 = 그림 3c · 4 | [인쇄] p.4–7 · 표 2 · 식 2 · 3 |
| ④ ★ 138.73 · 1.78 이 원문의 값인가 | **그렇다** — 138.73 = p.4 본문 · 그림 3c 안 글자 *"138.73 ± 18.78 GPa"* · 표 2 targeted · 1.78 = p.4 본문 · 그림 4a 안 글자 *"1.78 ± 0.35 GPa"* · 표 2 targeted.  ⚠ 조건: 138.73 = **targeted · 깊이 창 75–150 nm 평균 · NMC532** (창 밖 50 nm 는 151.6 · 420 nm 는 73.4 GPa [판독 · 벡터]) · 1.78 = **별도 CB/PVDF 필름 · 61 % 기공 · 200–2200 nm 일곱 깊이 평균** (깊이별 1.47–2.22 GPa [판독 · 벡터]) | [인쇄] p.4 · 표 2 · 그림 3c · 4a |
| ⑤ 저자 한계 | 기지 값은 기공에 크게 좌우 — 덜 다공이면 더 크다 (p.4) · 격자의 기지 값은 묻힌 NMC 때문에 2–3 배 (p.7) · 표면 분율 ≠ 부피 분율 (p.4) · 깊이 창 (p.4) · 충전 상태 (SOC) 에 따른 변화는 **다음 연구** (p.7) | [인쇄] |
| ⑥ DEM · 소성 · 2D/3D · 탈압 | DEM · 모델 **없음** · 모델에 대한 유일한 말 = *"The mechanical properties of electrodes are prerequisite parameters for the mechanics models. Nevertheless, elastic modulus, hardness, and fracture strength of most emerging electrode materials are unknown a priori that makes theoretical predictions questionable."* (p.1–2) · 2D/3D = 표면 분율 ≠ 부피 분율 (p.4) · 탈압 = 압입 제하 곡선만 (그림 3a 삽입도 — 최대 ≈406 nm 에서 하중 0 이 될 때 ≈201 nm [판독 · 벡터]) · 전극 수준 가압 · 탈압 **없음** | [인쇄] · [판독 · 벡터] |

⛔ **한정어 (떼지 말 것)**: ① 재료 = **NMC532 + PVDF + CB 의 액체계 LIB 양극** — 고체전해질 (LPSCl) 없음 · NCM811 아님 ② **캘린더링 안 한** 56 % 다공 전극 · 압력 이력 없음 · 전해질 · 충방전 이력 없음 ③ 138.73 은 **targeted · 75–150 nm 창** 값 (같은 논문의 격자 입자 값 123.02 · 깊이 420 nm 값 73.4) ④ 1.78 · 0.043 은 **별도 50/50 CB/PVDF 필름 (61 % 기공)** — 전극 속 기지 (격자 분해 4.40 · 0.13) 와 2–3 배 다르다 ⑤ ν = 0.3 **가정** (NMC · CB/PVDF 같은 값) ⑥ 통계 분해에 쓴 압입 수 **미기재** (그림 6 에서 ≈243 [카드 판독] · 그림 5 는 121) ⑦ 시료 한 종류 · 33 × 33 µm 한 구역.
⇒ **절대값 전이**: NMC 이차입자 탄성률 · 경도 **자릿수** 는 같은 산화물 층상 양극의 국소 물성이라 우리 AM (NCM811) 쪽 근거로 **"NMC532 · targeted · 75–150 nm" 꼬리표를 달고** 나란히 놓을 수 있다 (정본 [Sedl26] NCM811 138 ± 24 와 같은 띠).  **CB/PVDF 값은 우리 계 (건식 · PTFE · SE 가 기지를 채움) 로 전이 0 건** — 다른 재료 · 다른 기공 · 다른 상.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-23 의 '왜' 칸)

의도 원문: *"c (AM) — ★ 138.73 ± 18.78 GPa (NCM) · 1.78 ± 0.35 GPa (CB/PVDF) 의 원전으로 보임 (정본 Sedlatschek 카드: NMC532 139 GPa · H 8.9) — 확보 1 순위"* (가리킨 카드 = `wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn` L418 · L424)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "c (AM)" (질문 c: AM 의 항복 · 경도 · 크리프 값과 정의, 일축 항복과 견줄 환산) | **일부** | 경도 **있음** — targeted **H 8.89 ± 1.86 GPa** (창 75–150 nm) · 격자 입자 **7.78 ± 1.40** (100 nm) · 깊이별 9.54 (51 nm) → 5.36 GPa (419 nm) [판독 · 벡터] · 정의 = Oliver–Pharr 압입 경도 (Berkovich · 하중 ÷ 투영 접촉 면적) · **일축 항복 환산 · 크리프 값 없음** (5 s 최대 하중 유지는 했으나 크리프를 보고하지 않음 — 삽입도에서 유지 중 ≈10 nm 더 들어감 [판독 · 벡터]) · 조건 = 상온 (온도 미기재) · 건조 · 리튬화 이력 없는 pristine 전극 · 캘린더링 안 함 |
| "138.73 ± 18.78 GPa (NCM)" | **채움 (조성 한정)** | p.4 *"The average values of Young's modulus and hardness are 138.73 GPa and 8.89 GPa, respectively, in the optimum window of indentation depth ranging from 75 nm to 150 nm."* · 그림 3c 안 *"138.73 ± 18.78 GPa"* · 표 2 targeted.  ⚠ "NCM" = **NMC532** · 단일 이차입자 한가운데 (지름 > 8 µm) · 압입 깊이 75–150 nm 의 네 깊이 (≈75 · 97 · 128 · 152 nm [판독 · 벡터]) 를 모은 값 · ν 0.3 가정 |
| "1.78 ± 0.35 GPa (CB/PVDF)" | **채움 (시료 한정)** | p.4 *"… the average values of Young's modulus and hardness are 1.78 GPa and 0.043 GPa, respectively."* · 그림 4a 안 *"1.78 ± 0.35 GPa"* · 표 2 targeted 기지.  ⚠ **전극 속 기지가 아니다** — 따로 만든 **CB/PVDF 50/50 wt% 필름** (Al 위 17.74 µm · 기공 61 %) · 350 회 · 깊이 200–2200 nm · 일곱 깊이 평균 1.789 [카드 산술] (깊이별 1.47–2.22) · 전극 속 기지 (격자 분해) 는 **4.40 ± 2** |
| "의 원전으로 보임" | **채움** | 저자 · 제목 · 학술지 · 권 · 쪽 · DOI 모두 원문 1 쪽과 같다 (§2) · 두 값 모두 이 논문의 자체 측정 (2 차 인용 아님) |
| "(정본 Sedlatschek 카드: NMC532 139 GPa · H 8.9)" | **채움** | 138.73 · 8.89 를 반올림한 값 · NMC532 ✓ · "이차입자" ✓ (*"a single NMC532 particle which is closely packed by primary powders"* p.2) |
| "확보 1 순위" | **채움** | 이 카드 (원전 카드) |

**가리킨 카드 · 같은 논문을 옮긴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `wang2027_…` L8 · L28 · L89 | *"138.73 ± 18.78 GPa (NCM 입자) and 1.78 ± 0.35 GPa (CB/PVDF)"* (Wang 2027 원문 문장 · [25,26]) · *"NMC532 로 보임"* | 두 값 ✓ (표 2 targeted) · NMC532 ✓ | **채움** — "보임" [추정] 은 이 카드로 **확정** |
| `wang2027_…` L316 · `comparison_vs_ours_DEM.md` L4400 | *"138.73 은 NMC532 **grid** 압입값으로 보인다"* | 138.73 = **targeted** (단일 입자 · 75–150 nm 창) · 격자 (grid) 입자 값 = **123.02 ± 20** | **일부** — 조성 ✓ · 방법 ✗ (grid 아님) |
| `wang2027_…` L319 | *"압입 산포 ±18.78/138.73 = ±13.5 %"* | 산술 ✓ — 단 18.78 은 **개별 압입의 SD** (네 깊이를 모은 것 · 깊이 사이 차 포함) 이지 평균의 불확도가 아니다 | **채움 (해석 한정)** |
| `wang2027_…` L418 | *"카드 없음 — … 원전으로 보임 … 확보 1 순위"* | 이 카드 | **채움** |
| `sedlatschek2026_…` L139 · L129–131 | [28] → *"139 GPa · H 8.9 GPa · NMC532 다결정 2차입자"* | 138.73 · 8.89 (targeted) 반올림 ✓ · NMC532 ✓ · 이차입자 ✓ | **채움** |
| `shi2019_…` L120 · L176 · L181 · L435 | `[2]` de Vasconcelos 2016 EML 에 **E_AM 177.5 · ν_AM 0.3 · ρ_AM 4.85 · σ_y,AM 12.6** 을 귀속 (Shi 2019 SI Table 1) · 카드는 *"귀속 오류 공산"* | 이 논문에 **177.5 없음 · 12.6 없음 · 4.85 없음** (NMC 이론 밀도 = **4.77** mg/mm³ p.3) · ν 0.3 = 이 논문의 **압입 해석 가정값** (p.3) 으로만 있음 | **없음** (세 값) — shi2019 카드의 의심이 원문으로 **확정** (177.5 · 12.6 은 `xu2017_…` 의 소결 펠릿 값) |
| `comparison_vs_ours_DEM.md` L1116 | *"Shi 의 `[2]` EML 2016 귀속은 오귀속 공산"* | 위와 같음 | **채움 (확정)** |
| `xu2017_…` L140 | Xu 2017 그림 4b 의 **CB+PVDF 기지 E 1.78 ± 0.35 · H 0.043 ± 0.01 GPa** (그 카드: stated) | 이 논문 표 2 targeted 기지와 **소수 셋째 자리까지 같다** | **같은 값** — 같은 그룹의 이 논문 값이 2017 논문에 다시 쓰인 것으로 보인다 [카드 해석 · 이 논문으로 재측정 여부 판정 불가] |
| `xu2017_…` L348 | *"7.8 · 8.9 는 같은 Zhao 그룹의 de Vasconcelos 2019 Exp. Mech. · 2016 EML"* | 8.9 = 이 논문 targeted 8.89 ✓ · ⚠ 이 논문 **격자** 입자 H 도 **7.78 ≈ 7.8** — [Sedl26] 의 매핑 (7.8 → [27] 2019) 이 맞는지는 [27] 원문이 필요 (이 논문으로 판정 불가) | **채움 (8.9)** |
| `sharma2023_…` L60 | *"[24] de Vasconcelos 2016 EML (grid 압입)"* | ✓ | **채움** |
| `xu2023_realistic_am_shape_cgmd_calendering` L110 · L361 | E_AM **135 GPa** = refs [39–41] *"(Xu/Zhao 그룹 실험 + grid indentation)"* | 이 논문에 **135 없음** (138.73 targeted · 123.02 grid) · 그 [39–41] 에 이 논문이 들었는지 이 카드로 판정 불가 | **없음 (135)** |
| `so2021_dem_mold_pressure_assb_coldpress` L40 | *"H_AM (Si hardness) 10.6 GPa — de Vasconcelos [38]"* | 이 논문은 **Si 를 재지 않았다** (NMC532 · CB/PVDF 만) — so2021 카드에 [38] 의 서지가 없어 어느 de Vasconcelos 논문인지 판정 불가 | **이 논문 아님** (판정 불가 표지) |

⇒ **의도 대조 결과: 채움 (138.73 ± 18.78 · 1.78 ± 0.35 = 원전 · NMC532 139 · H 8.9 = 반올림) · 일부 (c 의 일축 항복 환산 · 크리프 = 없음 · "NCM" = NMC532 · 1.78 = 별도 61 % 필름) · 2 차 인용 = 값은 맞고 "grid 압입값" (wang2027 L316 · 비교 문서 L4400) 은 원문과 다르다 (targeted) · Shi 2019 의 [2] 귀속 (177.5 · 12.6 · 4.85) 은 원문에 없음.**

---

## 1. 한 줄 요약
액체계 LIB 의 상용형 NMC532 복합 양극처럼 **강성이 두 자릿수 다른 상이 섞인 전극**에서 상마다의 탄성률 · 경도를 빠르게 얻으려고, 많은 수의 얕은 나노압입을 격자로 찍고 E · H 의 누적 분포를 세 Gaussian (입자 · 기지 · 둘이 섞인 '계면') 으로 동시에 분해한 뒤, 같은 전극 단일 입자와 따로 만든 CB/PVDF 필름에 대한 targeted 압입으로 검증한 방법 논문이다 — 입자는 두 방법이 맞고 (139 ↔ 123 GPa) 연한 기지는 격자 쪽이 2–3 배 크게 나온다.

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 · 소속 | 위 머리 상자 (Purdue 3 · ORNL 1) |
| 학술지 | *Extreme Mechanics Letters* **9** (2016) **495–502** (8 쪽 · Letter) · © 2016 Elsevier Ltd. All rights reserved. |
| DOI | `10.1016/j.eml.2016.03.002` (p.1 바닥 · PDF 메타데이터 *"Extreme Mechanics Letters, 9 (2016) 495-502. doi:10.1016/j.eml.2016.03.002"*) · ISSN 2352-4316 |
| 이력 | 접수 2016-01-28 · 수정본 2016-03-06 · 승인 2016-03-07 · 온라인 2016-03-09 |
| 연구유형 | 실험 (나노압입 방법론) — 모델 · 계산 없음 |
| 시료 | NMC532 · PVDF · CB 양극 (ORNL 슬롯다이) + CB/PVDF 50/50 필름 (Al 위) |
| 보충 자료 | 없음 · 원자료 공개 진술 없음 |
| 서지 메모와의 차이 | 1저자 메모 *"L. S. de Vasconcelos, R. Xu, J. Li, K. Zhao, … Extreme Mech. Lett. 9 (2016) 495–502"* 와 **같다** (1저자 전체 이름 = Luize Scalco de Vasconcelos) |

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 전극 · 시료 (p.2–3 · `txt_p2_materials_preparation.png` · `txt_p3_porosity_definitions_not_calendered.png` · 그림 2 · 표 1)
- 성분: NMC532 (Toda America) · PVDF (Solvay 5130) · CB (Denka, powder grade) · NMP (Sigma Aldrich) → 슬롯다이 코팅 · **90 / 5 / 5 wt%** · 제조 세부 = 참고 [40] · 적재 **12.5 mg/cm²** (*"The areal loading of the NMC cathode was 12.5 mg/cm²"*) [인쇄 p.2].
- 미세구조 (그림 2): 거의 구형 NMC 이차입자 **≈10 µm** (*"estimated average diameter of approximately 10 µm"*) + CB/PVDF 다공 기지 · 이차입자 = 일차입자가 촘촘히 뭉친 것 (2b · 축척 1 µm) · 두께 (Al 제외) **45–57 µm** (2c) [인쇄 p.2].
- 처리: **캘린더링 안 함** · 윗면 연마 (유리 · Crystalbond · 3 → 1 µm 다이아몬드 페이스트 + microid diamond extender → 0.05 µm 콜로이드 실리카) [인쇄 p.3].
- 기공 (식 1 · 표 1): 이론 밀도 **NMC 4.77 · CB 1.90 · PVDF 1.76 · Al 2.70 mg/mm³** [인쇄 p.3].

| 표 1 | CB/PVDF 1 | 2 | 3 | 양극 1 | 2 | 3 |
|---|---|---|---|---|---|---|
| A_s (mm²) | 145.81 | 712.09 | 174.85 | 2886.65 | 1179.34 | 591.46 |
| h_s (µm) | 17.74 | 17.74 | 17.74 | 56.93 | 55.33 | 57.26 |
| h_Al (µm, 원문 열 이름) | 16.57 | 16.57 | 16.57 | **0.015** | **0.015** | **0.015** |
| w_s (mg) | 1.47 | 6.67 | 7.49 | 418.64 | 166.13 | 83.60 |
| ε (%) | 61.39 | 63.71 | 57.95 | 55.32 | 55.86 | 57.15 |

평균 **61 % (CB/PVDF) · 56 % (양극)** [인쇄 p.3] (= 61.02 · 56.11 [카드 산술]).
- ⚠ **표 1 원문 안 어긋남 셋** [카드 산술 — 식 1 을 표 값으로 다시 계산]:
  ① 양극 열의 h_Al **"0.015 (µm)"** 는 **0.015 mm (= 15 µm)** 로 읽어야 ε 가 재현된다 — 15 µm 이면 **55.31 · 55.85 · 57.13 %** (인쇄 55.32 · 55.86 · 57.15 와 0.02 %p 안) · 글자 그대로 0.015 µm 이면 **38.0 · 38.1 · 39.9 %**.
  ② **CB/PVDF 열은 식 1 로 재현되지 않는다** — A_s·h_Al·ρ_Al (Al 질량) 이 **6.52 · 31.86 · 7.82 mg** 로 시료 무게 w_s (1.47 · 6.67 · 7.49 mg) 보다 크다 (전극 질량이 음수).  w_s 를 코팅 질량만으로 읽어도 68.9 · 71.1 · −32.1 % 로 인쇄 값과 다르고, 시료 3 은 두께가 같은데 면적당 질량이 다른 둘의 **4.3–4.6 배** (0.0428 ↔ 0.0101 · 0.0094 mg/mm²).
  ③ 표 1 이 주는 양극 코팅 질량은 **10.45 · 10.04 · 10.08 mg/cm²** (NMC 9.41 · 9.03 · 9.08) — 본문의 *"areal loading … 12.5 mg/cm²"* 의 **0.72–0.84 배** (12.5 가 공칭 제조 사양인지 · 표 1 시료가 다른지 원문에 없음).
- 표면 분율과 부피 분율 [카드 산술]: 성분 이론 밀도로 NMC 는 고체 부피의 **77.5 %** · 기공 56.1 % 이면 전극 부피의 **34.0 %** (시료별 33.2–34.6 %) — 격자 분해의 입자 **표면** 분율 **38.40 %** 보다 4 %p 작다 (저자도 *"The surface fraction … may deviate from the overall volume fraction"* p.4).

### 3-2. ★ 압입 조건 (p.3–5 · `txt_p3_indentation_setup.png` · `txt_p4_targeted_and_grid_method.png`)
- 장비 · 압자: **Keysight G200 · Berkovich** · 일정 변형률 속도 **0.05 s⁻¹** · ν **0.3** (해석 가정) · 최대 하중 유지 **5 s** · E · H = **Oliver–Pharr** [42] [인쇄 p.3–4].
- targeted (NMC): *"indenting the center of selected particles of diameter larger than 8 µm"* · 기지와의 거리가 충분 · 광학상으로 위치 선정 · 매 시험 압자 좌표 재보정 [인쇄 p.4] · 최대 깊이 **50–420 nm** (그림 3c — 일곱 깊이 ≈52 · 75 · 97 · 128 · 152 · 199 · 420 nm [판독 · 벡터]) · 깊이별 시험 수 **미기재** — 그림 3b 막대 높이의 공통 단위로 **50 nm 70 회 · 100 nm 43 회 · 150 nm 50 회** [카드 판독 — E · H 패널이 같은 N 을 독립으로 줌 · 75 · 125 · 200 · 420 nm 는 판독 불가].
- targeted (CB/PVDF): 전극 속 기지는 *"NMC particles are likely to be buried underneath the CB/PVDF coating. Even relatively shallow indents may probe NMC particles immediately below the indented area"* → **별도 CB/PVDF 필름** · **350 회** · 깊이 **200–2200 nm** (얕으면 표면 거칠기 · 깊으면 Al 기판) [인쇄 p.4].
- 격자: *"the indentation depth (typically 100 nm) is much smaller than the characteristic size of the constituent phases, and the spacing between the indents (3–5 µm) is larger than the size of individual impression"* [인쇄 p.4] · 실제 격자 = **100 nm 고정** · 그림 5 = **121 회 · 33 × 33 µm** [인쇄 p.5].

### 3-3. ★ targeted NMC532 — 깊이 의존과 창 75–150 nm (p.4 · 그림 3 · `fig_3c.png` · `txt_p4_nmc_depth_window.png`)
저자 문장: *"Results below 75 nm are likely to be influenced by the surface features of the particles and also by the instrument precision limitation. At the other end, indentation performed over 150 nm might be affected by the surrounding compliant medium as well as particle internal porosity, resulting in a gradually decreasing modulus and hardness at larger indentation depth."* (p.4) · 빨간 점 = 평균 · 막대 = 표준편차 (p.4).

| 최대 깊이 (nm) [판독 · 벡터] | E (GPa) 평균 ± SD [판독 · 벡터] | H (GPa) 평균 ± SD [판독 · 벡터] | 창 안? | 시험 수 [카드 판독] |
|---|---|---|---|---|
| 51.7 (± 9.9) | **151.6 ± 22.7** | **9.54 ± 1.96** | 아니오 (< 75) | 70 |
| 74.5 (± 4.6) | 149.1 ± 16.7 | 9.05 ± 1.20 | 예 | — |
| 97.3 (± 6.9) | 141.2 ± 21.2 | 9.05 ± 1.97 | 예 | 43 |
| 127.7 (± 4.5) | 137.7 ± 15.0 | 8.68 ± 2.21 | 예 | — |
| 152.0 (± 12.2) | 127.7 ± 22.4 | 8.88 ± 2.09 | 예 | 50 |
| 199.1 (± 6.8) | 121.3 ± 18.4 | 7.39 ± 2.01 | 아니오 | — |
| 419.5 (± 16.0) | **73.4 ± 8.7** | **5.36 ± 1.05** | 아니오 (> 150) | — |

- 창 평균 [인쇄]: **E 138.73 ± 18.78 · H 8.89 ± 1.86 GPa** (그림 3c 안 글자 · 표 2).  네 깊이 평균의 단순 평균 **138.91 · 8.92** [카드 산술] — 인쇄 값과 같은 쪽 (차이는 깊이별 시험 수 가중으로 설명 가능 · 가중치는 원문에 없음).
- 막대 그래프 (그림 3b) 검산 [카드 산술 — 막대 중심 × 개수]: E 150.6 ± 22.0 (50 nm) · 140.8 ± 21.0 (100 nm) · 127.4 ± 22.1 (150 nm) · H 9.49 ± 1.93 · 9.00 ± 1.98 · 8.83 ± 2.09 — 그림 3c 점 (151.6 · 141.2 · 127.7 · 9.54 · 9.05 · 8.88) 과 1 GPa · 0.05 GPa 안 ⇒ N 추정과 판독이 서로 맞는다.  ⚠ 100 nm 의 E 막대 하나 (136.3–142.2 GPa) 는 축 위 끝 0.18 에서 **잘렸다** — 개수 = 43 − 나머지 = 8 (확률 0.186) [카드 판독].
- 크기: 420 nm 값은 창 평균의 **0.53 (E) · 0.60 (H) 배** [카드 산술] · 50 → 152 nm 사이에도 E 가 **151.6 → 127.7 (−16 %)** 로 이미 내려간다 — "창" 안에서도 깊이에 따라 단조 감소.
- 저자: *"All the data obey a typical normal distribution with relatively small deviation, which indicates that the indentations are indeed performed within the particles."* (p.4).
- 삽입도 (그림 3a, *"a set of 400 nm maximum displacement"* p.4): 하중 최대 **≈20.4 mN** (변위 ≈397 nm) → 유지 중 변위 **≈406 nm** 까지 (≈10 nm 더 들어감) → 제하 끝 (하중 0) **≈201 nm** ⇒ h_f / h_max **≈0.49** [판독 · 벡터 · 카드 산술] · 하중 축 0–22 mN · 변위 축 0–450 nm.

### 3-4. ★ targeted CB/PVDF 필름 (p.4 · 그림 4 · `fig_4a.png` · `fig_4b.png` · `txt_p4_cbpvdf_porosity.png`)

| 최대 깊이 (nm) [판독 · 벡터] | E (GPa) ± SD [판독 · 벡터] | H (GPa) ± SD [판독 · 벡터] |
|---|---|---|
| 202 | 1.53 ± 0.76 | 0.052 ± 0.025 |
| 524 | 1.47 ± 0.45 | 0.044 ± 0.014 |
| 838 | 1.49 ± 0.37 | 0.039 ± 0.012 |
| 1048 | 1.97 ± 0.31 | 0.044 ± 0.008 |
| 1587 | 1.87 ± 0.21 | 0.040 ± 0.005 |
| 1908 | 1.98 ± 0.19 | 0.042 ± 0.005 |
| 2118 | **2.22 ± 0.22** | 0.042 ± 0.005 |

- 인쇄: **E 1.78 ± 0.35 · H 0.043 ± 0.01 GPa** (그림 4 안 글자 · 표 2) · *"The mechanical properties are relatively insensitive to the indentation depth"* (p.4).  일곱 깊이 평균 **1.789 · 0.0432** [카드 산술] = 인쇄 값 · 일곱 평균의 SD 0.27 (모집단) — 인쇄 0.35 는 350 회 전체의 SD 로 보인다 [카드 해석].
- ⚠ "깊이에 둔감" 의 크기: E 가 524 → 2118 nm 에서 **1.47 → 2.22 GPa (×1.51)** [판독 · 벡터] · 가장 깊은 압입 = 필름 두께 (17.74 µm) 의 **11.9 %** [카드 산술] — Al 기판이 끼어들 수 있는 깊이 [카드 해석 · 저자는 기판 효과를 깊은 쪽 한계로만 언급].
- 저자: *"the mechanical properties of the CB/PVDF samples are highly dependent on the porosity—the tested samples have a porosity of 61% which is close to the typical set in commercial batteries. One may expect to obtain higher values of modulus and hardness for samples of low porosity."* (p.4).

### 3-5. 격자 지도 (p.5–6 · 그림 5 · `txt_p5_p6_grid_121_interface.png`)
- *"We regard the NMC particle as one constituent phase and the mixture of surrounding CB/PVDF as another general component. In grid indentation, we fix the maximum indentation depth as 100 nm."* (p.5) · *"121 tests in a 33 µm × 33 µm area"* · 광학상과 *"excellent match"* (p.5).
- 등고선 (그림 5b · c — 색 막대 위 끝 160 GPa · 9 GPa) 에서 입자 **120–160 GPa** · 기지 **0.1–10 GPa** 범위를 읽어 최적화 초기 범위에 썼다 (p.6).  그림 5 의 등고선은 11 × 11 점을 보간한 다각형 모양이라 점 값을 되살릴 수 없다 (판독하지 않음).
- *"due to the small size of the particles embedded in the matrix, a significant fraction of the data exhibit mixed properties of the particles and the matrix. Such mixed regions are referred as interface, the third constituent phase of the composite electrode in the light of the mechanical properties."* (p.5–6) — '계면' 은 **물리적 계면 상이 아니라 압입 부피가 두 상에 걸친 측정** 이다 [카드 해석 · 저자 문구 *"in the light of the mechanical properties"*].

### 3-6. ★ 통계 분해 — 식 2 · 3 · 표 2 · 그림 6 (p.4 · p.6–7 · `eq_02_gaussian_cdf_phase.png` · `eq_03_joint_cdf_deconvolution.png` · `fig_6*.png` · `txt_p6_p7_genetic_algorithm_agreement.png`)

**식 (2)** (p.4) 상 i 의 이론 누적분포: C_i(x) = ∫₀ˣ (1/(σ_i√(2π))) exp(−(u−µ_i)²/(2σ_i²)) du, x = E 또는 H · µ_i 평균 · σ_i 표준편차.
**식 (3)** (p.4) 미지수 {f_i, µ_i^E, σ_i^E, µ_i^H, σ_i^H} (Σ f_i = 1, n 상) 를 min [ (Σ_{i=1}^n f_i C_i^E − C_exp^E)² + (Σ_{i=1}^n f_i C_i^H − C_exp^H)² ] 로 — **E 와 H 의 CDF 에 같은 f_i** (*"while maintaining the same surface fraction f_i in the elastic modulus and hardness CDFs"*).  최적화 = **유전 알고리즘 150 세대 × 3000 점** · *"insensitive to the initial guesses and consistently converges to similar results"* (p.6–7).  PDF (그림 6b · d) 는 CDF 로 정한 같은 값으로 그렸고 *"the PDFs fit well … even the parameters are completely determined by minimizing the CDFs"* (p.7).

**표 2** [인쇄 p.7]

| 상 | 표면 분율 (%) 격자 | E (GPa) 격자 | E (GPa) targeted | H (GPa) 격자 | H (GPa) targeted |
|---|---|---|---|---|---|
| 입자 (Particles) | **38.40** | **123.02 ± 20** | **138.73 ± 18.78** | **7.78 ± 1.40** | **8.89 ± 1.86** |
| 기지 (Matrix) | **15.64** | **4.40 ± 2** | **1.78 ± 0.35** | **0.13 ± 0.01** | **0.043 ± 0.01** |
| 계면 (Interface) | **45.96** | **45.24 ± 27.58** | — | **1.44 ± 1.42** | — |

(그림 6b · d 범례는 같은 값을 *"123.02 ± 20.00 · 4.40 ± 2.00 · 45.24 ± 27.58 GPa"* · *"7.78 ± 1.40 · 0.13 ± 0.01 · 1.44 ± 1.42 GPa"* 로 적는다 [인쇄].)  표면 분율 합 100.00 % [카드 산술].
- 비 [카드 산술]: 격자 ÷ targeted = 입자 **E 0.887 · H 0.875** · 기지 **E 2.47 · H 3.02** (저자 *"by a factor of 2–3"*) · targeted 입자 ÷ 기지 E = **77.9 (1.9 자릿수)** — 서론의 *"2–3 orders of magnitude"* 는 일반 진술.
- 저자 해석: 입자는 *"stiff and hard materials and the experimental measurements are minimally influenced by the surrounding medium"* · 기지는 *"NMC particles are likely buried underneath the surface of CB/PVDF coating and even shallow indentation may probe the NMC particles in a portion of grid indentation. This comparison may not be unreasonable given the complexity of the microstructure of the composite samples."* (p.7).
- ★ **분해에 쓴 표본 수** [카드 판독]: 그림 6a 의 E 경험 CDF 십자 **51 개** (1.6–179.5 GPa, ≈3.5 GPa 간격) · 6c 의 H 십자 **53 개** (0.14–15.4 GPa, ≈0.29 GPa 간격) 의 높이가 모두 **k / 243** (정수 k · 최대 어긋남 0.058 · 0.073 개 · 121 · 122 · 242 · 244 로는 평균 0.2–0.27 개 어긋남) — 원문은 이 수를 적지 않았다.  121 회 지도 (그림 5) 의 **두 배쯤** 이 분해에 들어간 것으로 보인다 (다른 구역을 더했는지 · 분모 규약 (i/(N+1)) 인지 판정 불가).  막대 (그림 6b · d) 는 이 CDF 를 ≈3.5 GPa · 0.28 GPa 간격으로 차분한 것과 맞는다 [카드 판독].
- 경험 CDF 의 몇 점 [카드 판독]: E ≤ 8.7 GPa **43/243 = 17.7 %** · ≤ 51.4 GPa **41.6 %** · ≤ 101.1 GPa **69.5 %** (→ 101 GPa 넘는 압입 30.5 %) · ≤ 179.5 GPa 242/243 · H ≤ 0.70 GPa **23.5 %** · ≤ 3.04 GPa **48.6 %** · ≤ 12.8 GPa 243/243.
- ★ **표 2 값이 그린 맞춤 곡선을 되살리나** [카드 산술 — 혼합 CDF Σ f_i Φ((x−µ_i)/σ_i) 를 곡선 꼭짓점에서 계산]: E (그림 6a) = **되살린다** — 하한 −∞ 의 보통 Gaussian CDF 로 **RMS 0.010** (최대 0.042), 식 2 그대로 하한 0 이면 RMS 0.031 ⇒ 그림은 사실상 보통 CDF 로 그렸다 · H (그림 6c) = **되살리지 못한다** — RMS **0.046–0.048** (최대 0.08–0.09, H < 6 GPa 에서 그린 곡선이 0.04–0.10 낮음) ⇒ 표 2 의 H 값 (특히 기지 0.13 ± 0.01 · 계면 1.44 ± 1.42) 과 그린 H 곡선 사이에 원문 안 어긋남이 있다.  실험 CDF 대비 맞춤 RMS = E 0.023 · H 0.042.

### 3-7. ★ 저자가 적은 한계 · 원문 안 어긋남
**저자 한계 (인쇄)**: ① 기지 값은 기공에 크게 좌우 (61 % · 덜 다공이면 더 큼) (p.4) ② 격자 기지 값 2–3 배 = 묻힌 NMC (p.7) ③ 표면 분율 ≠ 부피 분율 (p.4) ④ 깊이 창 (75 / 150 nm) (p.4) ⑤ SOC · 사이클에 따른 변화 = 다음 연구 (p.7 · *"Few data are available so far that compile the dependence of mechanical properties of electrodes on the state of charge"* p.2).
**원문 안 어긋남 · 빈 곳 (이 카드가 찾은 것)**:
1. 표 1 h_Al 단위 (µm 열에 0.015 = 실제 mm) · CB/PVDF 열 식 1 재현 불가 · 적재 12.5 ↔ 표 1 의 10.0–10.5 mg/cm² (§3-1) [카드 산술].
2. 식 2 의 적분 하한 0 ↔ 그림 6a 맞춤 곡선은 하한 −∞ 의 보통 CDF 로 재현 (§3-6) [카드 산술].
3. 표 2 의 H 값이 그림 6c 의 H 맞춤 곡선을 되살리지 못함 (RMS 0.046–0.048) [카드 산술].
4. 분해 표본 수 미기재 · CDF 분모 243 ↔ 지도 121 회 [카드 판독].
5. targeted NMC 의 깊이별 시험 수 미기재 (그림 3b 에서 70 · 43 · 50 [카드 판독]) · 138.73 이 네 깊이를 어떤 가중으로 모았는지 미기재.
6. 격자 기지 H **0.13 ± 0.01** 의 SD 가 평균의 8 % 로, targeted 기지 (0.043 ± 0.01 = 23 %) 보다 좁다 — 격자 기지 상이 사실상 몇 점의 묶음일 수 있다 [카드 해석].
7. 그림 3b E 패널 사이 눈금 글자 *"250/0"* · *"250/20"* 은 인접 패널 글자가 겹친 것 — 눈금 선 위치로 보면 세 E 패널 모두 **20–250 GPa** [판독 · 벡터].

## 4. ★ 방법 — 측정 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 사슬
슬롯다이 코팅 (ORNL) → 캘린더링 없이 연마 → (a) 광학상으로 고른 큰 입자 한가운데 targeted 압입 · 깊이 50–420 nm → 깊이 창 75–150 nm 평균 (b) CB/PVDF 50/50 필름 targeted 350 회 · 200–2200 nm → 평균 (c) 33 × 33 µm 격자 121 회 · 100 nm → E · H 지도 → (그림 6 의 표본으로) E · H 실험 CDF → 세 Gaussian 동시 맞춤 (공유 f_i · 유전 알고리즘) → 표 2 (d) 질량-두께 기공 (식 1).

### 4-2. 입자 처리
- 이 논문의 대상 = **우리 DEM 구 하나의 표면 근처 국소 물성** (깊이 0.05–0.4 µm · 이차입자 지름 ≈10 µm) — 75–150 nm 창은 일차입자 · 입계를 몇 개 품는 부피 [카드 해석] · 420 nm 에서는 *"particle internal porosity"* 와 주변 기지가 끼어들어 E 가 절반으로 준다.
- **입자 전체 (whole-particle) 유효 탄성률 · 입자 압축 · 접촉 강성은 재지 않았다.**
- 우리 DEM: AM = **탄성 구** E **140 GPa** · ν **0.25** (AM_P · AM_S 같은 값) [우리 — 작업 트리 `docs/data/real14_reference_20260928/input_real_14.liggghts` 29–30 행 *"youngsModulus peratomtype 1.4e8 1.4e8 0.135e7"* · *"poissonsRatio peratomtype 0.25 0.25 0.30"*] · 우리 MPM: AM = 동결 scaffold (역학 응답 0) · 첨가제 상 (VGCF · PTFE · SuperP · SDCP) 은 MPM 물질점으로 탄성 상수를 갖는다 (§7).

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
| 질문 | 원문 | 위치 |
|---|---|---|
| (i) DEM (단단한 구 · 점접촉) 의 한계 | **말 없음** — DEM · 입자 모델을 쓰지 않는다.  모델 쪽에 대한 유일한 문장: *"The mechanical properties of electrodes are prerequisite parameters for the mechanics models. Nevertheless, elastic modulus, hardness, and fracture strength of most emerging electrode materials are unknown a priori that makes theoretical predictions questionable."* · *"the mechanical properties of composite electrodes are highly dependent on the packing density of the active material from the elementary powders and tortuosity of the surrounding medium [29]"* | p.1–2 (`txt_p1_p2_prerequisite_parameters_twofold.png`) |
| (ii) 입자 소성 · 큰 변형이 어려운 이유 · 우회 · 비용 | **말 없음 (모델 관점)** — 측정 쪽 어려움 두 가지만: *"First, electrodes in commercial batteries are heterogeneous materials … the elastic modulus changes by 2–3 orders of magnitude"* · *"Second, the mechanical properties of active materials may vary significantly with the state of charge"* (Si 의 취성 → 연성 전이 예) · 소성 저항 (경도 H) 을 **재지만** 입자 계산에 넣는 법 · 일축 항복 환산은 없다 | p.2 |
| (iii) 2D 인가 3D 인가 · 2D → 3D | 표면 (2D) 지도로 3D 미세구조의 상 분율을 잰다 — *"The surface fraction of individual components in the selected indentation area may deviate from the overall volume fraction in the samples."* · 이 카드 산술: 입자 표면 분율 38.4 % ↔ 부피 분율 ≈34 % (§3-1) | p.4 (`txt_p4_surface_vs_volume_fraction.png`) |
| (iv) 압력을 뺄 때의 거동 | 전극 수준 탈압 **없음** — 압입 제하 곡선만 (Oliver–Pharr 의 E 가 제하 강성에서 나온다) · 삽입도 h_f / h_max ≈0.49 [판독 · 벡터] | p.4 · 그림 3a |

### 4-4. 기법 미니 용어집
- **targeted (단일 위치) 압입**: 광학상으로 고른 한 상의 한가운데만 누르는 법.  주변 상의 영향을 피하려고 깊이를 작게 · 거리를 크게.
- **격자 (grid) 압입**: 상 크기보다 훨씬 얕게 · 압흔보다 넓은 간격으로 많이 찍어, 각 상이 표면 분율만큼 뽑히게 하는 통계적 압입 (Constantinides 2006 [34] · Ulm 2007 [35]).
- **통계 분해 (deconvolution)**: 측정값 분포를 상별 분포 (여기서는 Gaussian) 의 가중합으로 나누는 것.  가중치 = 표면 분율 f_i.
- **CDF 맞춤**: 히스토그램 대신 누적분포로 맞춤 — 막대 폭 선택에 덜 민감.  이 논문은 E · H 를 **같은 f_i** 로 함께 맞춘다.
- **'계면' 상**: 압입 부피가 입자와 기지에 걸친 측정의 묶음 — 재료의 계면 상 (interphase) 이 아니다.
- **Oliver–Pharr**: 제하 곡선의 초기 기울기 (접촉 강성) 와 압자 면적 함수로 reduced modulus · 경도를 얻는 표준법 [42] — 시료의 E/(1−ν²) 를 정하므로 E 를 내려면 ν 를 가정한다 (여기 0.3).
- **깊이 창**: 얕은 쪽 (표면 · 장비) 과 깊은 쪽 (주변 상 · 기판 · 내부 기공) 영향 사이에서 값이 덜 변하는 구간.
- **Berkovich**: 삼각뿔 다이아몬드 압자.  **변형률 속도 0.05 s⁻¹** = 하중 증가율 ÷ 하중 일정 (Ṗ/P).
- **질량-두께 기공 (식 1)**: (겉보기 부피 − 성분별 이론 밀도로 계산한 고체 부피) ÷ 겉보기 부피 · 집전체 질량을 빼고.

## 5. Figure set ★

| 그림 · 표 | 무엇을 보여주나 | 우리가 쓸 점 |
|---|---|---|
| **그림 1** (`fig_1.png` · `fig_1a` · `fig_1b`) | (a) 두 상 (빨강 · 파랑) 위 삼각 압입 격자 (b) 측정 물성 분포 = 상 A · B Gaussian 의 합 (도식) | 격자 압입 원리 한 장 — 우리 복셀 · 물질점 상 분율 보고에 같은 "확률 = 표면 분율" 논리 |
| **그림 2** (`fig_2.png` · `fig_2a`–`fig_2c`) | SEM (a) 윗면 (축척 10 µm) (b) NMC532 이차입자 한 개 — 일차입자가 촘촘히 (1 µm) (c) 단면 · Al 위 두께 45–57 µm (10 µm) | 캘린더링 안 한 액체계 전극의 출발 구조 (다공 · 입자 사이 CB/PVDF 거미줄) — 우리 압밀 전극과 구조가 다름 |
| **그림 3** (`fig_3.png` · `fig_3a` · `fig_3a_inset` · `fig_3b` · `fig_3c`) | (a) 광학상 + 고른 입자 (화살표) · 삽입도 = 400 nm 하중–변위 (b) 50 · 100 · 150 nm 에서 E (20–250 GPa) · H (0–15 GPa) 히스토그램 + 정규 맞춤 (c) 최대 깊이 50–420 nm 에 따른 E · H (평균 ± SD) · 파란 상자 = 창 · **"138.73 ± 18.78 GPa" · "8.89 ± 1.86 GPa"** | ★ 이 카드의 핵심 그림 — E_AM 의 깊이 (탐침 부피) 의존 · 창 선택이 값을 ±20 % 움직임 · U3 형태 대조용 실측 하중–변위 한 개 |
| **그림 4** (`fig_4.png` · `fig_4a` · `fig_4b`) | CB/PVDF 필름 E · H vs 최대 깊이 200–2200 nm · **"1.78 ± 0.35 GPa" · "0.043 ± 0.01 GPa"** | 다공 CBD 강성 한 점 (61 %) · 우리 PTFE 1.80 GPa 입력과 숫자가 겹친다는 경고의 출처 (§7) |
| **그림 5** (`fig_5.png` · `fig_5a`–`fig_5c`) | 33 × 33 µm 광학상 · E 지도 (색 막대 ~160 GPa) · H 지도 (~9 GPa) — 121 회 | 상 지도가 광학상과 맞음 · 입자 경계 근처 중간값 띠 = '계면' |
| **그림 6** (`fig_6.png` · `fig_6a`–`fig_6d`) | E · H 의 실험 CDF (×) + 세 Gaussian CDF 맞춤 (식 표기 그림 안) · PDF 막대 + 성분 곡선 · 범례에 표 2 값 | ★ 분해 결과 · 카드 판독: 십자 높이 = k/243 · E 맞춤은 표 2 로 재현 · H 맞춤은 안 됨 |
| **표 1** (`tab_1.png`) | 기공 보정 — A_s · h_s · h_Al · w_s · ε (CB/PVDF 3 · 양극 3) | 질량-두께 기공 연산자의 실례 + 단위 실수의 크기 (55 ↔ 38 %) |
| **표 2** (`tab_2.png`) | 상별 표면 분율 · E · H (격자 · targeted) | ★ 이 카드의 숫자 원천 |
| 식 1–3 (`eq_01_porosity_mass_thickness.png` · `eq_02_gaussian_cdf_phase.png` · `eq_03_joint_cdf_deconvolution.png`) | 기공 · 상 CDF · 공유 f_i 동시 맞춤 | 보고서 붙임용 |

### 5-1. 크롭 색인 — `litdb/figures/devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode/`
- 도구 (`tools/litdb/extract_figures.py --clean`, 300 dpi) 8 장 (그림 1–6 · 표 1–2) — **8 장 전부 다시 자름**: 그림은 단 전체 폭이라 좌우 여백이 넓고 고르지 않음 → 내용 경계 + 사방 14 px · 표 1 · 2 는 x 501.0 / 500.0 pt 에서 끝나 표 괘선 (503.1 pt 까지) 끝이 잘림 → 괘선 끝까지 · 표 캡션 정리 (도구가 표 글자 전체를 캡션에 넣었음).  다시 자른 뒤 본 다음 한 번 더: `fig_6` (첫 재단이 그림 5 캡션 끝줄을 위에 물었음) · `fig_3a_inset` (첫 클립이 현미경상의 회색 테를 물었음 → 삽입도 흰 상자 안으로 · 벡터라 600 dpi).
- 손 크롭 32: 패널 18 (`fig_1a` `fig_1b` · `fig_2a` `fig_2b` `fig_2c` · `fig_3a` `fig_3a_inset` `fig_3b` `fig_3c` · `fig_4a` `fig_4b` · `fig_5a` `fig_5b` `fig_5c` · `fig_6a` `fig_6b` `fig_6c` `fig_6d`) · 식 3 (`eq_01` 기공 · `eq_02` 상 CDF + 기호 정의 줄 · `eq_03` 공유 f_i 문단 + 식) · 근거 문단 11 (`txt_p1_p2_prerequisite_parameters_twofold` · `txt_p2_materials_preparation` · `txt_p3_porosity_definitions_not_calendered` · `txt_p3_indentation_setup` · `txt_p4_targeted_and_grid_method` · `txt_p4_surface_vs_volume_fraction` · `txt_p4_nmc_depth_window` · `txt_p4_cbpvdf_porosity` · `txt_p5_p6_grid_121_interface` · `txt_p6_p7_genetic_algorithm_agreement` · `txt_p7_conclusion_future_cycles`).
- 40 장 전부 Read 로 열어 확인 (잘림 · 이웃 문단 · 쪽 머리글 없음).  여백 = 흰 화소를 덧붙여 만듦 (클립을 넓히지 않아 이웃 글자가 들어올 수 없다).

## 6. Post-processing ★
- E · H: Oliver–Pharr [42] · ν 0.3 · 5 s 유지 · 변형률 속도 0.05 s⁻¹ (면적 함수 · 열 표류 · 접촉 강성 보정 **미기재**).
- 깊이별 평균 ± SD (그림 3c · 4) → 창 75–150 nm 평균 (NMC) · 일곱 깊이 평균 (CB/PVDF).
- 격자: E · H 지도 (그림 5 · 등고선 보간) → 실험 CDF → 식 3 (세 Gaussian · 공유 f_i) · 유전 알고리즘 · 초기 범위는 지도에서 · PDF 는 같은 값으로 그림.
- 기공: 식 1 (질량 · 두께 · 면적 · 성분 이론 밀도 · Al 질량 차감).
- 도구 · 소프트웨어 이름 **미기재** (유전 알고리즘 구현 · 그림 도구).
- 이 카드의 판독: 그림 3b · 3c · 4 · 6 · 3a 삽입도는 벡터 경로 → 축 틀 (검은 사각형 선) · 눈금 선 좌표로 선형 환산 (PyMuPDF `get_drawings`) · 빨간 꺾은선 꼭짓점 = 점 중심 · 검은 세로 선 끝 = ±SD · 막대 = 채운 사각형 (한 막대가 두 조각으로 그려진 곳은 합침) · 십자 = 같은 사각형을 가진 두 획 · 재현 = `digitized.csv` 의 note 칸 (경로 번호 · pt 좌표 · 축 틀).

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (우리 수치는 작업 트리 파일 · CLAUDE.md 출처를 그 자리에 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 상태가 다르다** — 이 논문 = NMC532 액체계 LIB 전극 · pristine · 캘린더링 안 함)

| 항목 | 이 논문 | 우리 | 판정 (판정 없이 나란히 · 차이의 이유) |
|---|---|---|---|
| **E_AM** | targeted **138.73 ± 18.78** (75–150 nm · NMC532) · 격자 입자 **123.02 ± 20** (100 nm) · 420 nm **73.4 ± 8.7** [판독 · 벡터] | DEM **140 GPa** (AM_P · AM_S) [우리 — `input_real_14.liggghts` L29] | 140 은 targeted 의 **+0.9 %** · 격자 입자의 **+13.8 %** [카드 산술] — 같은 띠의 위쪽 끝.  ⚠ 조성 NMC532 ↔ NCM811 (NCM811 = [Sedl26] 138 ± 24 와 같은 띠) |
| **E/(1−ν²)** (압입이 실제로 정하는 양 · Hertz 가 쓰는 양) | (138.73, ν 0.3) → **152.45** · (123.02, 0.3) → 135.19 | (140, ν 0.25) → **149.33** | 우리 ÷ targeted **−2.0 %** · ÷ 격자 **+10.5 %** [카드 산술] |
| **ν_AM** | **0.3 가정** (NMC · CB/PVDF 공통) | 0.25 [우리 — L30] | 이 논문은 ν 의 출처가 될 수 없다 (가정값) |
| **H_AM** | targeted **8.89 ± 1.86** · 격자 **7.78 ± 1.40** · 51 nm 9.54 → 419 nm 5.36 [판독 · 벡터] | `scripts/am_load_balance_jam.py` `--h-am` 기본 **4.0** (L609 · *"NCM811 계 문헌대 ≈ 3~6"*) · `scripts/fracture_model.py` H_AM **6.0** (*"hardness (informational) source unverified (SELF-51)"*) [우리] | 4.0 은 targeted 의 **0.45 배** · 격자의 0.51 배 · 6.0 은 0.67 배 [카드 산술] — **우리 "3–6 GPa" 밴드 밖** (위). [Sedl26] §7.5 · [Xu17-NMC] §7-2 와 같은 결론을 **원전**에서 확인 |
| CBD · 바인더 강성 | 다공 **CB/PVDF 50/50 필름 (61 %)** targeted **1.78 ± 0.35 · H 0.043** · 전극 속 기지 (격자) 4.40 ± 2 · H 0.13 | MPM 첨가제 표 `ADD_E_NU` (`scripts/mpm3d_compaction.py` L155–162): **PTFE (1.80, 0.30)** · SuperP (0.50, 0.30) · VGCF (100, 0.30) · SDCP (9.00, 0.35) · SWCNT (0.50, 0.30) — PTFE · SuperP · SDCP 는 *"사용자 지정 2026-08-18 · 근거 문헌/측정 미기재"* [우리] | ⚠ **우리 PTFE 1.80 GPa 와 이 논문 CB/PVDF 1.78 GPa 가 반올림하면 같다** — 같은 뿌리인지 **미확인** (우리 쪽 기록에 출처 없음).  이 논문의 값은 **PVDF + CB 61 % 다공 복합 필름** 이라 **PTFE 고체 · 섬유 · SE 가 채운 건식 전극의 출처가 될 수 없다**.  SuperP 0.50 은 이 논문과 무관 |
| SE (LPSCl) | **없음** | DEM E_eff 1.35 GPa (18 배 연화) · MPM E 1.53 · σ_y 0.30 · ν 0.49 [우리 CLAUDE.md] · LPSCl 압입 E 27.6 · H 1.41 GPa [다른 카드 `lee2025_…` §3-6] | AM : SE 강성 대비 [카드 산술]: E 138.73 ÷ 27.6 = **5.0** · ÷ 22.06 (우리 DFT E_VRH) = **6.3** · ÷ 1.35 (DEM) = **103** · ÷ 1.53 (MPM) = **91** · H 8.89 ÷ 1.41 = **6.3** |
| 전극 기공 | **56 %** (캘린더링 없음 · 질량-두께 · 액체계 · SE 없음) | 우리 복합 ≈15 % @300 MPa (real_14) · 랩 표준 순수 SE 10–13 % (진밀도 1.64 g/cm³ · 고정) | 다른 양 (압력 없음 · SE 없음) — 같은 표에 넣지 않는다 |
| 일차입자 · 내부 | 이차입자 = 일차입자 뭉치 (그림 2b) · 깊으면 *"particle internal porosity"* | 구 하나 (내부 없음) | 깊이 의존이 "입자 전체 유효 E < 국소 E" 의 정성 근거 — 크기는 미정 |

### 7-2. ★ 정의 대조 — "같은 이름 · 다른 양"
- **"E_NCM ≈ 139 GPa"** = 단일 이차입자 한가운데 · **깊이 75–150 nm** · ν 0.3 가정 · Oliver–Pharr — *입자 전체* 의 접촉 강성이나 압축 탄성률이 **아니다**.  같은 입자를 420 nm 로 누르면 73 GPa.  DEM 의 접촉 E* 에 넣을 때 "국소 압입값" 꼬리표를 단다.
- **"E_CB/PVDF ≈ 1.8 GPa"** = **따로 만든 61 % 다공 필름** 의 값 — 전극 속 기지 (4.40) 와 다르고, 기공이 줄면 커진다 (저자).  "CBD 강성" 으로 FE 에 넣는 관행 (`wang2027_…` 1.8 GPa) 의 원전이지만, **우리 건식 · PTFE · SE 계에는 해당 상이 없다**.
- **"H_AM"** = Oliver–Pharr 압입 경도 (평균 접촉압) — 우리 `am_load_balance_jam.py` 의 H_AM (*"AM 크라운이 버티는 접촉 평균압"*) 과 이름만 같다 ([Sedl26] §7.5).
- **'계면 (interface)'** = 압입 부피가 두 상에 걸친 측정의 통계 묶음 — 계면 저항 · 피복의 '계면' 과 다른 양.
- **"surface fraction"** = 연마면 위 압입이 각 상에 떨어진 비 — 부피 분율 · 피복률과 다르다 (§3-1 의 38.4 ↔ 34 %).

### 7-3. 나란히 놓을 정본 카드 (값 · 조건 그대로 · 기존 카드는 고치지 않는다)

| 카드 | 재료 · 방법 | E (GPa) | H (GPa) | 이 카드와의 관계 |
|---|---|---|---|---|
| **이 카드** | NMC532 이차입자 · targeted 75–150 nm · ν 0.3 | **138.73 ± 18.78** | **8.89 ± 1.86** | — |
| 이 카드 (격자) | NMC532 · 100 nm 격자 분해 | 123.02 ± 20 | 7.78 ± 1.40 | 같은 논문 |
| `sedlatschek2026_…` | NCM811 2 차입자 단면 · Berkovich CSM 5 mN · ν 0.32 · n 29 | 138 ± 24 (인장 165 ± 7) | — | 다른 조성 · 같은 띠 |
| `xu2017_…` | NMC532 이차입자 · Berkovich 1 mN · 15 입자 · ν 0.3 | 142.5 ± 11.3 | 8.6 ± 1.3 | 같은 그룹 · 같은 조성 · 다른 하중 규약 (1 mN) |
| `xu2017_…` | NMC532 소결 펠릿 | 177.5 ± 19.5 | 12.6 ± 1.4 | 치밀 쪽 (Shi 2019 가 이 논문에 잘못 단 값) |
| `sharma2023_…` | NMC622 단결정 결정립 (VRH) | 140.16 (ν 0.253) | — | 결정 한 알 · 이방 ±15 % |
| `lee2025_…` | Li₆PS₅Cl 펠릿 (2.5 % 공극) 나노압입 | 27.6 | 1.41 ± 0.24 | SE 쪽 짝 (다른 재료) |
| `wang2027_…` | (사용례) NCM811 복셀 FE 입력 | 140 · CBD 1.8 | — | 이 논문 값을 입력으로 씀 (ν 0.30 무출처) |

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **입자 · 기지의 국소 기계 물성 측정** — 우리 분업으로는 두 모델 모두의 **입력 물성 쪽** (DEM 접촉 E* · MPM AM 탄성 (A′ · B 에서) · 첨가제 상 E).  전극 스케일의 압밀 · 수송 · 형상은 **없다**.
- 없는 반쪽: 입자 전체 압축 · 접촉 강성 · 파괴 · 고체전해질 · 가압 / 탈압 · 압력 이력.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = NMC532 + PVDF + CB 액체계 양극 — **SE 가 없고** · 압력 이력이 없고 · AM 조성도 다르다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ **질량-두께 기공 연산자 (식 1)** 의 실례 — 성분 이론 밀도 (NMC 4.77 · CB 1.90 · PVDF 1.76 · Al 2.70 mg/mm³) · 집전체 질량 차감 · 두께 · 면적 · ★ **단위 하나가 값을 17 %p 움직인 실례**: 표 1 의 h_Al "0.015 µm" 를 글자대로 쓰면 ε 38 % · 15 µm 이면 55 % [카드 산술] → 우리 기공 칸에 **항마다 단위를 적는다** · ★ **판독 창을 결과 전에** — 이 논문은 깊이 창 75–150 nm 를 데이터를 보고 정했고 (E 가 창 안에서도 149 → 128 로 감소) 창 선택이 E 를 최대 2 배 움직인다 (151.6 ↔ 73.4) → 우리 압입 · 응력 판독 창도 결과 전에 적는다 | 진밀도 · 기공의 압력 의존 없음 · SE 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 (모델 없음) | — |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | ★ **측정 쪽 함정 하나**: 연한 상을 복합 안에서 누르면 밑에 묻힌 단단한 상이 겉보기 E · H 를 **2–3 배** 올린다 (CB/PVDF 4.40 ↔ 1.78 · 0.13 ↔ 0.043) — 우리 SE 물성 앵커는 **순수 SE 펠릿 측정** 에서 (복합 단면 압입 값을 SE 물성으로 쓰지 않는다) | SE 숫자 0 · LPSCl 아님 |
| **단계 5** (3D 복합 압밀) | AM 탄성 입력의 **띠** — NMC532 국소 E **123 (격자) – 139 (targeted) GPa** · 깊이 420 nm 73 GPa (주변 · 내부 기공 포함) · AM : 실제 SE 강성 대비 **5–6 배** (E · H 둘 다 [카드 산술]) | 입자 전체 E · 압밀 응력 · AM 하중 몫 없음 |
| **단계 6** (탈압 · 되돌아옴) | 압입 수준의 되돌아옴 한 곡선 — NMC532 · Berkovich · ≈406 nm 에서 h_f / h_max ≈0.49 [판독 · 벡터] (AM 이 눌린 쪽 · SE 아님) | 전극 수준 탈압 · 두께 회복 없음 |
| **단계 7** (형상 · 피복 · 수송) | '표면 분율 ≠ 부피 분율' (§3-1 · 38.4 ↔ 34 %) — 단면 · 표면에서 센 상 분율을 부피 분율로 쓰기 전의 경고 | 수송 · 피복 값 없음 |
| **후보 D0** (지금 DEM) | ★ E_AM 140 GPa 의 **원전 쪽 근거 하나 더** — NMC532 targeted 138.73 (+0.9 %) · E/(1−ν²) 로 −2.0 % · 단 같은 논문 격자 값 123.02 이면 우리 140 은 +13.8 % → AM–AM 접촉 E* 의 문헌 폭 ≈ **±10 %** [카드 산술] (AM–SE 접촉은 SE 연화가 지배해 무관 — [Sedl26] §7.2) · ★ H_AM "3–6 GPa" 밴드에 **원전 반례** (8.89 · 7.78) | 입자 전체 · 접촉 강성 측정 아님 · NMC532 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 없음 | — |
| **후보 A** (MPM 강체 AM · SE 한 속도장) | AM 을 강체로 둘 근거의 숫자 — AM : SE 경도 비 ≈6.3 (8.89 ÷ 1.41 [다른 카드]) · 탄성 비 5–6 (실제) · 우리 MPM SE (E 1.53) 대비 **≈91** [카드 산술] — 300 MPa 압밀의 평균 접촉압 수준에서 AM 은 국소 항복에 멀다 [카드 해석 · 접촉 국소 압력은 평균보다 클 수 있다] | 강체 근사의 오차 크기 · 접촉 응력 분포 없음 |
| **후보 A′** (입자별 속도장 · 다물체 마찰 접촉) | AM 을 탄성체로 풀 때의 E · H 입력 (NMC532) + ν 미측정이라는 사실 (0.3 가정) | 마찰 · 접촉 법칙 · NCM811 값 없음 |
| **후보 B** (입자별 FE + 접촉) | 이차입자 FE 의 균질 E 를 고를 때의 경고 — 국소 압입 E (139) 와 깊은 압입 E (73) 가 두 배 차이 · 저자 원인 = 주변 기지 + **입자 내부 기공** · 다결정 입자를 균질 탄성 구로 둘 때 어느 값인지 정하고 꼬리표를 단다 | 입자 전체 압축 곡선 없음 |
| **후보 C** (큰 변형 접촉 DEM · MDR 류) | AM 쪽 (E, H) 쌍 — H/E = **0.064** (NMC532 targeted [카드 산술]) · LPSCl 0.051 [다른 카드] · MDR 류의 항복 입력을 경도에서 잡으려면 환산이 필요 (원문 없음 — Tabor H/3 ≈ 3.0 GPa 는 **취성 세라믹의 항복이 아니다** · [Stallard22] 의 *"H/3 로 인장강도 추정 불가"*) | 일축 항복 · 크리프 · 큰 변형 거동 없음 |
| **후보 C′** (항복 캡 탄소성 접촉 DEM · Thornton–Ning 류) | AM–AM 접촉 항복압의 자릿수 = 압입 경도 **7.8–8.9 GPa** (NMC532) — 300 MPa 압밀에서 AM–AM 접촉은 이 값에 닿기 전까지 탄성 영역 [카드 해석] | 접촉 수준 항복 측정 아님 |
| **후보 M0** (균질화 압밀 · 캡 소성 · Heckel) | 없음 | — |
| **U0–U6** | **U3** (단단한 압자 · 소성체를 눌렀다 떼기) 의 **실측 형태 하나** — NMC532 · Berkovich · 하중 최대 ≈20.4 mN · 유지 중 ≈10 nm 크리프 · 잔류 깊이 ≈201 / 406 nm [판독 · 벡터] (압자 · 재료 모두 U3 와 다름 — 형태 대조만) · **U1 · U6** (해상도) 쪽 유비: "탐침 부피 ≪ 상 크기 · 간격 > 압흔" 규칙 = 우리 "지름당 셀 수" · d_h/dx 규칙과 같은 꼴 [카드 해석] | U0 · U2 · U4 · U5 없음 |
| **R1–R7** | **R1** (AM 하중 분담) — AM 이 기지보다 78 배 단단 (액체계) · **R4** (탈압 되돌아옴) — 압입 수준 곡선 하나 · **R7** (AM 파괴) — 400 nm 압입에서 파괴 · 팝인 서술 **없음** | R2 · R3 · R6 (SE 형상) 없음 · R5 — 물리 모델이 없다 (통계 분해의 맞춘 값 = 상마다 µ_E · σ_E · µ_H · σ_H × 3 + f_i 3 = 15 개, Σ f_i = 1 이라 독립 14 개 [카드 산술]) |
| **결과 전 대조 항목** | ① AM 국소 E 띠 **123–139 GPa** (NMC532 · 100 nm 격자 · 75–150 nm targeted) — 우리 E_AM 입력이 이 띠 안에 있는지 (맞추지 않음 · 꼬리표 "NMC532 · 압입 국소") ② AM 압입 경도 **7.8–8.9 GPa** — H_AM 을 "압입 경도" 라 부를 때의 기준 (우리 4.0 · 6.0 은 밖) ③ 다공 CBD 1.8 GPa (61 %) 는 **대조 항목에 넣지 않는다** (우리 계에 같은 상 없음) | LPSCl · NCM811 값 아님 · 우리 랩 표준 (10–13 % · 1.64) 과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: AM (NMC532 ↔ NCM811) · 계 (액체계 LIB 양극 ↔ 황화물 ASSB 복합 양극) · 기지 (PVDF + CB 다공 ↔ SE + 탄소 + PTFE) · 상태 (pristine · 캘린더링 없음 · 기공 56 % ↔ 300 MPa 압밀 · ≈15 %) · 측정 (표면 국소 압입 ↔ 입자 전체 접촉) · ν (0.3 가정 ↔ 0.25).

## 9. 적용 인사이트 (행동)
1. **E_AM 140 GPa 출처 문장에 원전 하나를 더한다 (D0 · 표 S2)**: *"NMC532 secondary particles, targeted Berkovich nanoindentation within 75–150 nm: 138.73 ± 18.78 GPa (ν = 0.3 assumed); grid indentation + statistical deconvolution: 123.02 ± 20 GPa (de Vasconcelos et al., Extreme Mech. Lett. 9 (2016) 495)"* — NCM811 은 [Sedl26] 이 주 출처 · ⛔ *"140 GPa (de Vasconcelos 2016)"* 금지 (140 은 이 논문에 없다).
2. **H_AM "3–6 GPa" 문구 (D0 · `am_load_balance_jam.py`)**: 원전 두 값 (8.89 · 7.78) 이 밴드 밖 — [Sedl26] §8 ② · [Xu17-NMC] §7-2 처방 (재명명 "입자 스케일 유효 지지압" 또는 판정선 재등록) 의 근거가 하나 더 (원전) 생긴다.  이 카드는 코드를 바꾸지 않는다.
3. **⚠ 우리 PTFE E 1.80 GPa (MPM `ADD_E_NU`) 의 출처를 채울 때 이 논문을 쓰지 않는다** — 숫자는 같아도 재료가 다르다 (PVDF + CB 61 % 다공 필름).  출처는 여전히 **미기재** 로 둔다 (원장 · 문서에 "PTFE 1.80 = 사용자 지정 · 출처 없음 · CB/PVDF 1.78 [devasconcelos2016] 과 우연히 같은 값일 수 있음" 한 줄).
4. **압입 값을 인용할 때 붙일 꼬리표 (단계 0)**: 방법 (targeted / 격자) · 깊이 (창) · ν (가정값) · 시험 수 · 시료 상태 (캘린더링 · 이력).  이 논문은 같은 입자에서 창만 바꿔도 E 가 151.6 → 73.4 GPa.
5. **SE 물성 앵커는 순수 SE 펠릿에서 (단계 4)**: 복합 단면에서 잰 연한 상 값은 밑의 단단한 상 때문에 2–3 배 부풀 수 있다 (이 논문의 기지).
6. **비교 문서 §G 의 [Wang27-GNN] "138.73 = NMC532 grid 압입값" 은 원전으로 정정된 사실을 이 카드가 갖는다** (targeted) — 비교 문서에 새 항목 [deVasc16] 으로 적었다 (기존 줄은 그대로).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Targeted Berkovich nanoindentation at the centre of NMC532 secondary particles (> 8 µm) in an uncalendered NMC532/PVDF/CB (90:5:5 wt%) electrode gave E = 138.73 ± 18.78 GPa and H = 8.89 ± 1.86 GPa within a 75–150 nm depth window, and grid indentation with statistical deconvolution gave 123.02 ± 20 GPa and 7.78 ± 1.40 GPa for the particle phase (de Vasconcelos et al., *Extreme Mech. Lett.* 9 (2016) 495–502)."
- "A separately prepared CB/PVDF (50/50 wt%) film of 61 % porosity gave E = 1.78 ± 0.35 GPa and H = 0.043 ± 0.01 GPa; grid indentation of the matrix inside the electrode gave values 2–3 times larger, which the authors attribute to NMC particles buried beneath the surface."
- 국문 (한정어와 함께): *"NMC532 이차입자의 국소 탄성률은 Berkovich 압입 75–150 nm 에서 138.73 ± 18.78 GPa (격자 분해 123.02 ± 20) · 경도 8.89 ± 1.86 GPa 이고 (de Vasconcelos 2016, ν 0.3 가정 · 캘린더링 안 한 액체계 전극), 같은 입자를 420 nm 까지 누르면 73 GPa 로 준다 (주변 기지 · 내부 기공)."*
- ⛔ 쓰지 말 것: *"CBD (carbon-binder) modulus 1.8 GPa (de Vasconcelos 2016)"* 를 건식 · PTFE · 황화물 전극의 상 물성처럼 — 61 % 다공 CB/PVDF 필름 값이다.

## 11. 주의/한계 (over-claim 방지)
1. **NMC532 · 액체계 · pristine · 캘린더링 안 함** — NCM811 · 압밀 ASSB 와 다르다.
2. **국소 압입 값** — 입자 전체 · 접촉 강성이 아니다 · 깊이에 강하게 의존 (75–150 nm 창은 데이터를 보고 정함).
3. **ν 0.3 가정** — 이 논문으로 ν 를 인용하지 않는다.
4. **1.78 = 별도 61 % CB/PVDF 필름** — 전극 속 기지는 4.40 (격자) · 다공도에 크게 의존.
5. **분해 표본 수 미기재** (CDF 분모 243 [카드 판독]) · 구역 하나 (33 × 33 µm) · 시료 한 종류.
6. **표 2 의 H 값이 그림 6c 맞춤을 재현하지 못함** · 식 2 하한 0 ↔ 그림은 보통 CDF [카드 산술].
7. **표 1 단위 · 재현 불가 · 적재 불일치** [카드 산술].
8. '계면' 은 측정 묶음 — 물리 계면 상으로 쓰지 않는다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| [34] | G. Constantinides, K.R. Chandran, F.-J. Ulm, K. Van Vliet, Grid indentation analysis of composite microstructure and mechanics: principles and validation, Mater. Sci. Eng.: A 430 (2006) 189–202. | 격자 압입 원리 · 검증 규칙 (깊이 ≪ 상 크기 · 간격) 의 원전 — 질문 c · m · 카드 없음 |
| [35] | F.J. Ulm, M. Vandamme, C. Bobko, J. Alberto Ortega, K. Tai, C. Ortiz, Statistical indentation techniques for hydrated nanocomposites: concrete, bone, and shale, J. Am. Ceram. Soc. 90 (2007) 2677–2692. | 다공 복합체의 통계 압입 · 상 물성의 다짐 (packing) 의존 — 질문 c (다공 SE 펠릿 압입 해석) · 카드 없음 |
| [42] | W.C. Oliver, G.M. Pharr, An improved technique for determining hardness and elastic modulus using load and displacement sensing indentation experiments, J. Mater. Res. 7 (1992) 1564–1583. | 우리 모든 압입 앵커 (H_AM · LPSCl H 1.41) 의 H · E_r 정의 원전 — 질문 c · 카드 없음 (papakyriakou2021 · stallard2022 가 인용만) |
| [29] | B. Vijayaraghavan, D.R. Ely, Y.-M. Chiang, R. García-García, R.E. García, An analytical method to determine tortuosity in rechargeable battery electrodes, J. Electrochem. Soc. 159 (2012) A548–A552. | *"packing density … and tortuosity of the surrounding medium"* 의 근거 · tortuosity 해석식 (정본 J 절) — 단계 7 · 카드 없음 (froboese2019 · tjaden2018 이 인용만) |
| [41] | J. Nohava, P. Haušild, Š Houdková, R. Enžl, Comparison of isolated indentation and grid indentation methods for HVOF sprayed cermets, J. Therm. Spray Technol. 21 (2012) 651–658. | targeted ↔ 격자 비교의 선례 (연한 상 과대 문제) — 질문 c · 카드 없음 |
| [40] | J. Li, C. Daniel, S.J. An, D. Wood, Evaluation residual moisture in lithium-ion battery electrodes and its effect on electrode performance, MRS Adv. (2015) 1–7. | 이 전극의 제조법 원전 (슬롯다이 · ORNL) — 시료 조건 확인용 |
| [7] | S. Yu, R.D. Schmidt, R.G. Mendez, E. Herbert, N.J. Dudney, J.B. Wolfenstine, et al., Elastic properties of the solid electrolyte Li7 La3 Zr2 O12 (LLZO), Chem. Mater. 28 (2016) 197–206. | 산화물 SE 탄성 (LLZO) — SE 기계 물성 문헌 지도용 (황화물 아님) |
| [30] | Y. Qi, H. Guo, L.G. Hector, A. Timmons, Threefold increase in the Young's modulus of graphite negative electrode during lithium intercalation, J. Electrochem. Soc. 157 (2010) A558–A566. | SOC 에 따른 E 변화의 예 (흑연) |

## 13. [미확인] 목록 (본문 8 쪽 전수에 없음)
1. 통계 분해 (그림 6) 에 쓴 압입 수 · 구역 수 (카드 판독 243) · 분모 규약.
2. targeted NMC 의 깊이별 시험 수 (카드 판독 70 · 43 · 50 은 50 · 100 · 150 nm 만) · 138.73 의 가중 방식 · 창 안 총 시험 수.
3. Oliver–Pharr 세부 (면적 함수 보정 · 열 표류 · 하중 · 최대 하중) · 온도 · 습도 · 대기 (건조 상자인지).
4. CB/PVDF 필름의 제조 (용매 · 건조) · 두께 측정법 · 표 1 CB/PVDF 열의 계산 방식.
5. 적재 12.5 mg/cm² 와 표 1 (10.0–10.5) 의 관계.
6. NMC532 의 일차입자 크기 · 이차입자 내부 기공률 · PSD.
7. 그림 5 지도의 점 값 · 격자 정렬 (11 × 11 인지).
8. ν 측정 · 크리프 (5 s 유지) 값 · 압입 중 균열 여부.

## 14. 🧮 카드 산술 원장 (원문 숫자만으로 · 재현 = 식 그대로)

| # | 계산 | 결과 | 비고 |
|---|---|---|---|
| D1 | 식 1, 양극 (h_Al = 15 µm) | 55.31 · 55.85 · 57.13 % | 인쇄 55.32 · 55.86 · 57.15 |
| D2 | 식 1, 양극 (h_Al = 0.015 µm 글자대로) | 38.01 · 38.05 · 39.93 % | 단위 실수 크기 |
| D3 | 식 1, CB/PVDF — Al 질량 A_s h_Al ρ_Al | 6.52 · 31.86 · 7.82 mg > w_s 1.47 · 6.67 · 7.49 | 재현 불가 |
| D4 | 표 1 양극 코팅 질량 ÷ 면적 | 10.45 · 10.04 · 10.08 mg/cm² (NMC 9.41 · 9.03 · 9.08) | ↔ 12.5 mg/cm² 의 0.72–0.84 |
| D5 | NMC 부피 분율 (이론 밀도 · ε) | 고체의 77.5 % · 전극의 34.6 · 34.2 · 33.2 % (평균 34.0) | ↔ 표면 분율 38.40 % |
| D6 | 그림 3c 창 네 깊이 단순 평균 | E 138.91 · H 8.92 GPa | ↔ 138.73 · 8.89 |
| D7 | 그림 3b 막대 (개수 × 중심) | E 150.6/140.8/127.4 · H 9.49/9.00/8.83 (50/100/150 nm) | ↔ 3c 점 151.6/141.2/127.7 · 9.54/9.05/8.88 |
| D8 | 그림 4 일곱 깊이 평균 | E 1.789 · H 0.0432 GPa · E 의 SD 0.27 (모집단) · 524 → 2118 nm ×1.51 | ↔ 1.78 · 0.043 |
| D9 | 격자 ÷ targeted | 입자 E 0.887 · H 0.875 · 기지 E 2.47 · H 3.02 | 저자 "2–3" |
| D10 | targeted 입자 ÷ 기지 E | 77.9 (10^1.89) | 서론 "2–3 orders" 는 일반 진술 |
| D11 | 420 nm ÷ 창 | E 0.53 · H 0.60 | |
| D12 | 삽입도 h_f/h_max · 유지 중 변위 | 200.6 / 406.3 = 0.494 · 406.3 − 396.6 = 9.7 nm | [판독 · 벡터] 입력 |
| D13 | E/(1−ν²): (138.73, 0.3) · (123.02, 0.3) · 우리 (140, 0.25) | 152.45 · 135.19 · 149.33 → 우리 −2.0 % · +10.5 % | 압입 · Hertz 공통량 |
| D14 | E_AM 비: 140 ÷ 138.73 · ÷ 123.02 | +0.92 % · +13.8 % | |
| D15 | H_AM 비: 8.89 ÷ 4.0 · 7.78 ÷ 4.0 · 8.89 ÷ 6.0 | 2.22 · 1.95 · 1.48 | 우리 값은 밴드 밖 |
| D16 | AM : SE 비 (E 138.73 ÷ 27.6 · 22.06 · 1.35 · 1.53 · H 8.89 ÷ 1.41) | 5.0 · 6.3 · 103 · 91 · 6.3 | [다른 카드] lee2025 · [우리] |
| D17 | H/E: NMC532 (8.89/138.73) · LPSCl (1.41/27.6) | 0.064 · 0.051 | |
| D18 | Tabor H/3 (원문에 없음 · 참고만) | 2.96 · 2.59 GPa | 취성 세라믹의 항복이 아님 |
| D19 | 그림 6 CDF 분모 | 243 (최대 어긋남 0.058 · 0.073 개) · 121 · 122 · 242 · 244 = 평균 0.21–0.27 개 | [카드 판독] |
| D20 | 표 2 혼합 CDF ↔ 그린 곡선 (RMS) | E: −∞ 0.0096 · 0 0.0306 · H: −∞ 0.0476 · 0 0.0456 | ↔ 실험 십자 E 0.0226 · H 0.0418 (−∞) |
| D21 | 격자 간격 (11 × 11 가정) | 33 / 10 = 3.3 µm | 원문 3–5 µm |
| D22 | 가장 깊은 CB/PVDF 압입 ÷ 필름 두께 | 2118 / 17 740 = 11.9 % | |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 본문 8 쪽을 글자 층 (pdftotext layout · raw · PyMuPDF 줄 좌표) + 렌더로 읽음.  서지 = PDF 1 쪽 (제목 · 저자 · 소속 · 이력 · 키워드 · DOI · ISSN) + PDF 메타데이터 (*"Extreme Mechanics Letters, 9 (2016) 495-502. doi:10.1016/j.eml.2016.03.002"*) + 쪽 머리글.  SI · 원자료 링크 없음.
- 그림 판독: 그림 3b · 3c · 4 · 6 과 그림 3a 삽입도는 **벡터** (PyMuPDF `get_drawings`) — 축 틀 · 눈금 선 좌표로 환산 (예: 그림 3c 탄성률 축 x 99.97 → 255.79 pt = 0 → 500 nm, y 356.05 → 241.92 pt = 60 → 180 GPa).  그림 2 · 3a 현미경상 · 5a 는 ≈300 dpi 래스터 · 그림 5b · 5c 등고선은 벡터 채움 (판독하지 않음).  재현 값: 그림 3c 창 단순 평균 138.91 ↔ 인쇄 138.73 · 그림 4 일곱 평균 1.789 ↔ 1.78 · 그림 3b 막대 평균 ↔ 3c 점 (1 GPa 안) · 그림 6a 표 2 재현 RMS 0.010.
- 크롭 40 장 (§5-1) · 전부 열어 확인.
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (ls-tree · 517 개) + DOI (`eml.2016.03.002`) · "Grid indentation" · "Vasconcelos" · "495–502" · "EML 2016" grep — **이 논문 카드 없음** (sedlatschek2026 [28] · wang2027 [26] · sharma2023 [24] · shi2019 [2] · xu2017 · 비교 문서 L1116 · L4400 에 인용만).

## 🔗 관련 카드
- 이 논문을 인용 · 사용한 정본 카드: [`sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile`](sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile.md) ([28]) · [`wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn`](wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn.md) ([26] · 140 · 1.8 GPa 입력) · [`sharma2023_nmc_single_crystal_anisotropic_nanoindentation`](sharma2023_nmc_single_crystal_anisotropic_nanoindentation.md) ([24]) · [`shi2019_high_am_loading_particle_size_assb`](shi2019_high_am_loading_particle_size_assb.md) ([2] · 귀속 오류) · [`xu2017_nmc532_nanoindentation_modulus_hardness_toughness`](xu2017_nmc532_nanoindentation_modulus_hardness_toughness.md) (같은 그룹 · 같은 CB+PVDF 값).
- NCM 기계 물성 사슬: [`stallard2022_cathode_mechanical_properties_review`](stallard2022_cathode_mechanical_properties_review.md) · [`wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem`](wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem.md).
- SE 압입 짝: [`lee2025_heckel_argyrodite_powder_densification_nanoindentation`](lee2025_heckel_argyrodite_powder_densification_nanoindentation.md) · [`papakyriakou2021_mechanical_behavior_inorganic_li_solid_electrolytes_nanoindentation`](papakyriakou2021_mechanical_behavior_inorganic_li_solid_electrolytes_nanoindentation.md).
- E_AM 를 입력으로 쓴 DEM · CGMD: [`xu2023_realistic_am_shape_cgmd_calendering`](xu2023_realistic_am_shape_cgmd_calendering.md) (135 GPa) · [`so2021_dem_mold_pressure_assb_coldpress`](so2021_dem_mold_pressure_assb_coldpress.md).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
