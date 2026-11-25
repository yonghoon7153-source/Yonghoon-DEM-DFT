<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md (누른 채 CT + 영상 기반 계산) ·
     sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps.md · 계산 쪽 이웃 = sangros2019_dem_calendering_lib_electrode.md (이 논문 ref 19).
     쪽 표기 = 학술지 쪽 p.2746–2768 (본문 PDF 24 쪽 · PDF p.1 = 쪽 번호 없는 그래픽 초록 쪽 · 학술지 쪽 = PDF 쪽 + 2744) · 보충 자료는 쪽 번호가 없어 SI p.1–15 = PDF 쪽.
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv — Fig 3I · 3J · 7A 는 원 래스터 300 dpi,
     SI 그림은 PDF 벡터 경로) · [눈대중] = 눈금 사이를 눈으로 읽은 값 · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 추론] · [카드 관찰] = 이 카드의 해석 ·
     [미확인] = 원문 (본문 24 쪽 + SI 15 쪽 전수) 에 없음.  본문 · SI 전 쪽을 렌더 이미지와 텍스트 층으로 읽었다 (텍스트 층은 µ → m · ± → G 로 깨져 있어 숫자 단위는 렌더로 확인). -->
# 리튬이온 양극 (NMC111 + 탄소-바인더 · 액체 전해질용 · SE 없음) 을 X 선 나노 CT 안에서 누른 채 (in situ · 기둥 압축 3 단계 ≤ 24 %) 본 미세구조 진화 + 그 3D 구조 위 전기화학 모델 — 큰 입자 (7.3 ± 3.1 µm) 는 회전 · 불균일 변형 · 기공 연결 상실 / 작은 입자 (5.2 ± 1.8 µm) 는 집단 변형 · 같은 기공률에서 tortuosity factor 7–9 % 낮음 [판독] · 가압 압력 · 하중 · 탈압 · 역학 계산 없음 — Lu · Daemi · Bertei · Kok · O'Regan · Rasha · Park · Hinds · Kendrick · Brett · Shearing (Joule 2020)

> slug `lu2020_insitu_nanoct_calendering_microstructural_evolution` · DOI `10.1016/j.joule.2020.10.010` · type `experiment + image-based simulation (in situ X-ray nano-CT 기둥 압축 = calendering 모사 · DSS 3 상 분할 · microstructure · porosity · TauFactor tortuosity factor · 3D 미세구조 분해 gPNP 전기화학 모델 COMSOL — 액체 전해질 LIB 양극 · DEM · FEM · MPM 압밀 역학 계산 없음)` · PDF `78a488a6-53._Microstructural_evolution_of_battery_electrodes_during_calendering.pdf` · digested `2026-11-12` · status ✅
>
> **저자**: **Xuekun Lu\*** (교신 · ¹ ² ³) · Sohrab R. Daemi (¹) · Antonio Bertei (⁴) · Matthew D.R. Kok (¹) · Kieran B. O'Regan (³ ⁵) · Lara Rasha (¹) · Juyeon Park (²) · Gareth Hinds (²) · Emma Kendrick (³ ⁵) · Dan J.L. Brett (¹ ³) · **Paul R. Shearing\*** (¹ ³ · Lead Contact) — ¹ Electrochemical Innovation Lab, Dept. of Chemical Engineering, UCL · ² National Physical Laboratory · ³ The Faraday Institution · ⁴ Univ. of Pisa · ⁵ Univ. of Birmingham · *Joule* **4** (2020) 2746–2768 (December 16, 2020 · 본문 23 쪽 + 그래픽 초록 쪽 · Supplemental Information 15 쪽 = 그림 S1–S15 · 표 S1–S4 · 식 (1)–(15) · 참고문헌 7) · 접수 2020-07-10 · 수정 08-10 · 승인 10-19 · 온라인 11-19 · 연구비 EPSRC (EP/R020973/1 · EP/M028100/1) · Faraday Institution (EP/S003053/1 · FIRG003 · FIRG001) · RAEng (CiET1718\59) · UK BEIS National Measurement System · 기여: X.L. · P.R.S. = 구상 / X.L. · S.R.D. · L.R. = in situ CT · 영상 분석 / X.L. · A.B. = 모델 / M.D.R.K. = 파이썬 / K.B.O. · E.K. = 율 특성 시험 (p.2766) · 자료 = 요청 시 Lead Contact (공개 저장소 없음).
> **이웃 카드 (링크만)**: [`he2026_dem_calendering_inhomogeneity_areal_density`](he2026_dem_calendering_inhomogeneity_areal_density.md) (이 논문을 N7 문헌으로 가리킴 · L691) · [`lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode`](lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode.md) (ref 8 로 인용 · L380) · [`sangros2019_dem_calendering_lib_electrode`](sangros2019_dem_calendering_lib_electrode.md) (이 논문 ref 19 = '구 입자 DEM' 비판의 대상) · [`taufactor_tortuosity_factor_tomography_tool`](taufactor_tortuosity_factor_tomography_tool.md) (ref 55 · 계산 도구) · [`tjaden2018_tortuosity_review_calculation_approaches`](tjaden2018_tortuosity_review_calculation_approaches.md) (τ 명명 정본) · [`landesfeind2016_tortuosity_eis_electrodes_separators`](landesfeind2016_tortuosity_eis_electrodes_separators.md) (ref 28) · [`nguyen2020_electrode_tortuosity_factor`](nguyen2020_electrode_tortuosity_factor.md) (같은 관통형 tortuosity factor 의 한계) · [`xu2017_nmc532_nanoindentation_modulus_hardness_toughness`](xu2017_nmc532_nanoindentation_modulus_hardness_toughness.md) (ref 43) · [`kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation`](kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md) · [`sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps`](sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps.md) (황화물 쪽 '누른 채 CT') · [`zhang2026_xct_dem_cathode_calendering_peel_calibration`](zhang2026_xct_dem_cathode_calendering_peel_calibration.md) · [`xu2023_realistic_am_shape_cgmd_calendering`](xu2023_realistic_am_shape_cgmd_calendering.md) · [`ngandjong2021_dem_calendering_digital_twin`](ngandjong2021_dem_calendering_digital_twin.md) (같은 LIB 압연의 입자 계산 쪽).
> **판독 원자료**: `litdb/figures/lu2020_insitu_nanoct_calendering_microstructural_evolution/digitized.csv` (277 행 — Fig 3I · 3J · 7A 래스터 판독 · Fig S3 · S7 · S8 · S10 · S13 · S14 · S15 벡터 판독) · 그림 크롭 92 장 (도구 24 중 23 다시 자름 + 손 68: 그래픽 초록 1 · SI 그림 4 · 패널 19 · 식 22 · 근거 문단 22) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: NMC111 양극 (활물질 : 탄소 : PVDF = 90:5:5 · 액체 전해질용 · 고체전해질 없음) 두 종 — 평균 입경 **7.3 µm (STD 3.1 · AM_L)** 와 **5.2 µm (STD 1.8 · AM_S)** — 을 지름 < 90 µm 기둥으로 깎아 X 선 나노 CT (복셀 64 nm) 안에서 평평한 핀으로 **누른 채** 세 단계 (AM_L 7 → 15 → 22.5 % · AM_S 7 → 13.5 → 24 %) 찍고, 탄소-바인더 (CBD) 만의 막을 따로 찍어 겹치는 DSS 로 3 상 (입자 · CBD · 기공) 을 가른 뒤 형상 · 방향 · 기공 망 · tortuosity factor (TauFactor) 를 재고 그 구조 위에서 3D 전기화학 모델 (COMSOL) 을 돌린다 — 큰 입자 전극은 입자가 돌고 불균일하게 눌리며 기공 연결을 잃고, 작은 입자 전극은 집단으로 눌려 같은 기공률에서 tortuosity factor 가 7–9 % 낮다 [판독 · 카드 산술]; **가압 압력 · 하중 · 하중을 뺀 뒤의 같은 시료 · 압밀 역학 계산은 원문 어디에도 없다.**

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 압연 단계별 두께 · 기공률 · 압축률 | 양 끝만 표로 인쇄 — AM_L **45 → 35 µm · 기공률 0.325 → 0.188** (22.5 %) · AM_S **43 → 33 µm · 0.354 → 0.195** (24 %).  가운데 두 단계는 Fig 3I 판독 — AM_L 0.330 → 0.300 → 0.250 → 0.190 · AM_S 0.350 → 0.300 → 0.270 → 0.195 | [인쇄] Table 1 (p.2757) · [판독] Fig 3I · §3-2 |
| ② 재는 조건 (누른 채 / 뺀 뒤) | 단계 영상 = **핀으로 누른 채** (변위 단계 · 한 단계 1,201 장 × 60 s ≈ 20 h [카드 산술]).  **압력 · 하중 · 변위 속도 · 유지 · 이완 = 인쇄 없음**.  뺀 뒤 값은 다른 시료 (롤 압연 20 %) 의 대조 하나뿐: 기공률 0.203 ↔ 누른 채 22.5 % 의 0.188 | [인쇄] p.2765 · Table S3 · [미확인] |
| ③ 두 입경의 차이 | 7.3 ± 3.1 ↔ 5.2 ± 1.8 µm (평균 1.4 배) · **공급사 (MTI ↔ Targray) · 분포 폭 · 형상 (AM_S 가 더 타원형) 이 함께 다르다** · 분석 입자 수 ≈139 ↔ ≈434 [카드 산술] | [인쇄] p.2748–2750 · p.2764 · §3-3 |
| ④ 입자 재배열 · 변형 · 파쇄 | AM_L: 입자 회전 + 압축 변형 (한 입자 추적) · 입자 사이 미끄럼 · 구름 · ovality 분포의 무작위 변동 (*"heterogeneous and mild"*) · 방향 무작위 유지.  AM_S: 집단 변형 → ovality 0.75 에 몰림 · 방향 군집.  **파쇄 = 이 논문의 관찰 · 정량 없음** (ref 18 의 추측 인용뿐) | [인쇄] p.2748–2751 · Fig 1G · 1H · 2 · §3-4 |
| ⑤ tortuosity 정의 · 도구 | *"Tortuosity, also called tortuosity factor"* · Q_p/Q_b = ε/τ (SI 식 3) ⇒ **τ = tortuosity factor = 우리 tau2 (수송 tortuosity · √ 아님)** · 도구 TauFactor · 3 상 (CBD 포함) 기공상 · 방향 미기재 | [인쇄] SI p.2 · p.2765 · §3-6 |
| ⑥ tortuosity 값 | AM_L **2.58 → 2.94 → 4.65 → 8.79** · AM_S **2.32 → 2.73 → 3.55 → 7.56** [판독] · 표로 인쇄된 것은 2.58 (압연 전) · 8.85 (22.5 %) · 8.34 (롤 20 %) 뿐.  같은 기공률에서 AM_S ÷ AM_L = 0.91–0.93 [카드 산술] | [판독] Fig 3I · [인쇄] Table S3 · S4 |
| ⑦ 수치 모사의 정체 | **압밀 계산이 아니다** — CT 구조 (입자 · CBD · 기공) 를 그대로 격자로 쓴 3D 전기화학 (gPNP · Butler–Volmer · 고체 확산 · COMSOL 5.5 · 반쪽 셀).  DEM · FEM · MPM 역학 없음.  격자 수 · 영역 크기 · 계산 비용 [미확인] | [인쇄] p.2766 · SI p.13–14 |
| ⑧ 실험 대조 | 모델 ↔ 실험은 NMC622 2 mAh cm⁻² 전극 (AM_LH) 한 쌍 — *"in good agreement …, except for a noticeable discrepancy at 5C"* · 5C 끝 용량 모델 ≈88 · 81 ↔ 실험 ≈80 · 73 mAh g⁻¹ [눈대중].  '기둥 압축 = 압연' 은 Table S3 의 *"within 8%"* | [인쇄] p.2755–2756 · Fig 5E · 5F · Table S3 |
| ⑨ DEM 한계 문장 | *"these studies were conducted based on simplified electrode geometries that were artificially synthesized with spherical particles, ignoring the influence of particle shape and orientation … the carbon-binder domain (CBD) … was not taken into account."* (ref 19 = Sangrós Giménez 2019) | [인쇄] p.2747 · §4-4 |
| ⑩ 저자가 건 적용 범위 | 활물질 90–94 wt% · 초기 두께 < 50 µm · 압연 ≈23 % 까지에서 '전해질 수송은 지배 인자가 아니고 고체 확산이 지배' · 후막은 가상 (거울상) 40–70 µm | [인쇄] p.2759–2762 |

⛔ **한정어 (떼지 말 것)**: ① **리튬이온 양극이다 — 고체전해질이 없다.** 무른 상 = 탄소-바인더 (다공 · 눌리면 부피가 준다) · 이온 통로 = 기공 (눌리면 닫힌다).  우리 계 (무른 상 = LPSCl · 이온 통로 = SE) 와 **수송 상이 반대** 다 ② '압연' = **옆 구속 없는 기둥 압축** (지름 < 90 µm · 다이 벽 · 롤 없음) ③ **압력 축이 없다** (하중 · 응력 숫자 0 개) → Heckel · 항복 · 우리 300 MPa 와 놓을 자리가 없다 ④ 단계마다 시료 **하나** (전극당 기둥 하나) · 재현 · RVE 점검은 압연 전 AM_L 에만 ⑤ '큰 / 작은' 은 평균 1.4 배 차이의 **두 전극** — 입경 축의 경향이 아니다 ⑥ 가운데 단계 값은 전부 [판독] ⑦ 기공률은 분할 문턱 ±10 % 에 0.288–0.353 (압연 전 0.325 기준) 으로 움직인다 (Fig S12) ⑧ CBD 안 기공은 **다른 시료 (CBD 만의 막) 의 영상** 을 옮겨 넣은 것 (DSS) ⑨ 모델의 NMC 물성 (OCV · D_s) 은 NMC622 반쪽 셀 값인데 구조는 NMC111 전극이다.
⇒ **절대값 전이: 되지 않는다.** 기공률 · tortuosity factor · 반응 면적 · 용량 어느 것도 우리 계 (NCM811 + LPSCl · 300 MPa 일축 · SE 가 이온 통로) 의 값으로 옮기지 않는다.  옮길 수 있는 것은 **정의와 방법의 교훈** — (a) 이 그룹의 'tortuosity' 는 tau2 꼴이다 (b) 탄소-바인더를 빼면 tortuosity factor 를 2.1–2.6 배 낮게 본다 (합성 구조 · Fig S4) (c) 영상 기공률은 문턱 · 시료 · 시야의 산포를 결과 전에 적어야 한다 (d) 옆 구속 없는 압축은 두께 감소의 81–84 % 만 기공 감소로 간다 [카드 산술] (e) 구 입자 DEM 이 놓치는 것 (형상 · 방향 · CBD) 을 적은 인용 가능한 문장.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-53 의 '왜' 칸)

의도 원문: *"단계 5 (결과 전 대조 후보) — '압연 중 미세구조 진화의 XCT operando — 소입자일수록 균일변형 · 저tortuosity · ⛔ 미digest' (he2026) · '후막 미세구조 설계' (lee2026_li) · LIB 전극 (ASSB 아님)"*

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "압연 중 미세구조 진화의 XCT" | **채움 (단 '압연' = 기둥 압축)** | Fig 1E–G · 1I–K · Fig 2 · 3 — 같은 기둥을 압축 0 → 7 → 15 → 22.5 % (AM_L) · 0 → 7 → 13.5 → 24 % (AM_S) 로 **누른 채** 나노 CT (64 nm) [인쇄] p.2748–2753.  *"in situ compression experiment to replicate the calendering process"* (Context & Scale, p.2746) — 롤 압연은 대조용 다른 시료 (Fig S10 · Table S3) |
| "operando" | **없음 (낱말이 다르다)** | 원문은 처음부터 끝까지 **"in situ"** (요약 · p.2748 · 결론 · 기여).  'operando' 는 ref 4 의 제목에만 나온다.  촬영 중 전기화학은 돌리지 않았다 (전기화학은 영상 위 모델 + 별도 반쪽 셀) |
| "소입자일수록 균일변형" | **채움 (원문 주장 그대로) · 근거는 일부** | 요약: *"electrodes consisting of small particles are structurally stable with more homogeneous deformation and a lower tortuosity"* (p.2746) · 결론 p.2764 같은 문장.  근거 = ovality 분포 (AM_S 압연 뒤 0.65–0.8 에 약 60 % · Fig 2D) · 방향 군집 (Fig 2G–H) · 단면 (Fig 1I–K).  ⚠ 변형률 장 · 입자별 변형률은 재지 않았다 · 비교는 **두 전극** (5.2 ↔ 7.3 µm) 이고 원문 자신이 원인을 *"the smaller and narrower distribution of particle size (STD 1.8 versus 3.1 µm)"* 로 묶는다 (p.2753) → '입경이 작을수록' 이라는 **경향** 은 원문에 없다 (점 두 개 · 분포 폭 · 형상 · 공급사 동반 변화) |
| "저 tortuosity" | **채움 (정성) · 숫자는 그림에만** | *"for a given porosity, AM_L shows a higher pore phase tortuosity than AM_S, especially at high calendering ratios"* (p.2753).  값은 Fig 3I 에만 — AM_L 2.58 / 2.94 / 4.65 / 8.79 ↔ AM_S 2.32 / 2.73 / 3.55 / 7.56 [판독] · 같은 기공률로 맞추면 (ln τ 선형 보간) AM_S ÷ AM_L = 0.93 (ε 0.30) · 0.92 (0.27) · 0.93 (0.25) · 0.91 (0.195) [카드 산술].  정의 = **tortuosity factor** (SI 식 1–3 · TauFactor) · 기공상 · 3 상 (CBD 포함) · **누른 채**.  비교 눈금: 시료 간 표준편차 2.5 % (압연 전 AM_L · n = 3 · Table S4) · 기둥 ↔ 롤 6.1 % (Table S3) |
| "⛔ 미digest" | 해소 | 이 카드 |
| "후막 미세구조 설계" (lee2026_li L380) | **일부** | 두께 축은 (a) 같은 구조를 두께 방향으로 거울상으로 붙이거나 잘라 만든 **가상 전극 40–70 µm** 의 3C 모델 용량 지도 (Fig 7 · p.2760–2762) + (b) 실험 1 · 2 · 3 mAh cm⁻² 전극 30 → 25 · 48 → 39 · 74 → 57 µm (Fig 8).  결론 = AM_S 는 두께와 기공률이 같은 무게 · AM_L 은 기공률 0.25 가 전이점.  '후막' 이라 해도 **≤ 74 µm** |
| "LIB 전극 (ASSB 아님)" | **채움 (맞다)** | NMC111 / NMC622 + C65 (+ KS6L) + PVDF · 1 M LiPF₆ EC/EMC · Li 금속 반쪽 셀 (p.2764–2765) |
| "단계 5 (결과 전 대조 후보)" | **없음 (대조 값으로는 못 쓴다)** | 압력 축 없음 · 옆 구속 없음 · 무른 상이 CBD (부피가 주는 다공 상) · 이온 통로가 기공 → 우리 3D 복합 (AM + SE) 가압 계산과 견줄 **값** 이 없다.  쓸 수 있는 것은 현상 목록 (AM 회전 · 재배열) 과 관측량 정의뿐 (§8) |
| (꼭 뽑을 것) tortuosity 정의 · 도구 | **채움** | SI p.2 식 (1)–(3) · p.2765 *"The tortuosity factor was obtained by the open-source software TauFactor"* |
| (꼭 뽑을 것) 단계별 두께 · 기공률 · 압축률 + 재는 조건 | **일부** | 양 끝 = Table 1 [인쇄] · 가운데 = Fig 3I [판독] · 두께는 양 끝만 (가운데 = 압축률로 환산 [카드 산술]) · 재는 조건 = 누른 채 (압력 미기록) |
| (꼭 뽑을 것) 입자 재배열 · 파쇄 관찰 | **일부** | 재배열 · 회전 · 변형 = 채움 (정성 + ovality · 방향 분포) · 파쇄 = 없음 (§3-4) |
| 가리킨 카드의 **2 차 인용 값** | **해당 없음 (숫자 없음)** | he2026 L691 · lee2026_li L380 모두 서지 + 한 줄 주제뿐 · 서지는 원문과 같다 (*Joule* 4, 2746–2768, 2020).  he2026 L691 의 **"XCT operando"** 만 원문 (in situ) 과 다르다 → 카드 문제로 보고 (그 카드는 고치지 않음) |

---

## 1. 한 줄 요약
액체 전해질용 NMC111 양극 두 종 (평균 7.3 / 5.2 µm) 의 기둥 시료를 나노 CT 안에서 22.5 / 24 % 까지 누르며 3 상 (입자 · 탄소-바인더 · 기공) 구조를 단계별로 재고 그 구조로 3D 전기화학 모델을 돌려, **큰 입자 · 넓은 분포 전극은 재배열 · 기공 연결 상실 · 고체 확산 한계로 압연에 민감하고 작은 입자 전극은 구조가 안정하고 고율 용량을 지킨다** 고 보인 실험 + 영상 기반 모델 논문 — 압력 · 탈압 · 역학 계산은 없다.

## 2. 메타
| 항목 | 내용 |
|---|---|
| 재료계 | **AM_L** = LiNi₀.₃₃Mn₀.₃₃Co₀.₃₃O₂ (MTI, USA) · **AM_S** = 같은 조성 (Targray, Canada) · 둘 다 활물질 : Super C65 (Imerys) : PVDF (Arkema) = **90:5:5 (질량)** · Al 20 µm · 닥터 블레이드 간격 175 µm · 80 °C 진공 하룻밤.  **AM_LH** = NMC622 (BASF 활물질 · AGM Batteries 제조 전극) 130 g m⁻² · 94.5:3:2.5 (활물질 : C65 + KS6L 2:1 : PVDF Solref) · Al 15 µm · *"Uncalendared [sic] and 18% calendered"* · CBD 만의 막 = 탄소 : PVDF 50:50 (NMP) [인쇄] p.2764–2765 |
| 입경 | D_mean 7.3 µm (STD 3.1) · 5.2 µm (STD 1.8) [인쇄] p.2748–2749 — 영상 분할 입자의 크기 (개수 기준 히스토그램 · 등가 지름 정의 [미확인]) |
| 실험 | in situ X 선 나노 CT (Zeiss Xradia Ultra 810 · 5.4 keV · 복셀 64 nm · 시야 64 × 64 µm²) + 나노 기계 시험대 (평평한 스테인리스 핀 · 압전 구동) · 기둥 지름 < 90 µm · 롤 압연 대조 (Fig S10) · micro-CT 대조 (Fig S13) · 반쪽 셀 율 특성 · GITT |
| 압력 · 온도 | **가압 압력 · 하중 인쇄 없음** · 압축률 (두께 감소) 7–24 % · 온도: 모델 298 K (Table S1) · 실험 온도 [미확인] |
| 계산 | 영상 기반 — TauFactor (tortuosity factor) · Avizo XLab (투과도) · Simpleware ScanIP N-2018.03 격자 → COMSOL Multiphysics 5.5 의 gPNP 3D 미세구조 분해 전기화학 (SI 식 4–15) · PoreSpy 합성 구조 (Fig S2 · S4) |
| 차원 | 전부 **3D** (영상 · 정량 · 모델) · 2D 는 단면 표시뿐 |
| 탈압 | 다루지 않음 (누른 채 영상만 · 롤 시료는 다른 시료) |
| 코드 · 자료 | 공개 없음 (*"available from the Lead Contact on request"*) |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 전극 표 (Table 1 · p.2757) [인쇄]
| 전극 | 면적 용량 (mAh cm⁻²) | AM 부피 분율 | 두께 (µm) | 기공률 | 비고 (카드 주석 — 표에는 없는 칸) |
|---|---|---|---|---|---|
| AM_L (Uncal) | 1.5 | 0.46 | 45 | 0.325 | 나노 CT (기둥 · 압축 전) |
| AM_L (22.5 % Cal) | 1.5 | 0.52 | 35 | 0.188 | 나노 CT (누른 채) |
| AM_LH (Uncal) | 2 | 0.57 | 48 | 0.286 | NMC622 · 제조사 전극 |
| AM_LH (18 % Cal) | 2 | 0.62 | 39 | 0.217 | 〃 · 제조사 압연 (탈압 뒤로 읽힘 [카드 추론] · 촬영 조건 미기재) |
| AM_L1.5 (22.5 % Cal) | 2.25 | 0.52 | 53 | 0.188 | **가상** (거울상 1.5 배) |
| AM_L2 (22.5 % Cal) | 3 | 0.52 | 70 | 0.188 | **가상** (2 배) |
| AM_S (Uncal) | 1.5 | 0.45 | 43 | 0.354 | 나노 CT (압축 전) |
| AM_S (24 % Cal) | 1.5 | 0.50 | 33 | 0.195 | 나노 CT (누른 채) |
| AM_S1.5 (24 % Cal) | 2.25 | 0.50 | 50 | 0.195 | **가상** |
| AM_S2 (24 % Cal) | 3 | 0.50 | 66 | 0.195 | **가상** |

- 두께는 압축률과 닫힌다: 45 × (1 − 0.225) = 34.9 · 43 × (1 − 0.24) = 32.7 µm [카드 산술] → 이 논문의 'compression / calendering ratio' = **두께 감소율** (정의는 인쇄돼 있지 않다 — 끝점 일치가 유일한 확인).
- ⚠ **고체 보존이 닫히지 않는다** [카드 산술 · AM 분율 × 두께]: AM 기둥 부피 AM_L 20.7 → 18.2 (−12 %) · AM_S 19.4 → 16.5 (−15 %) · AM_LH 27.4 → 24.2 (−12 %).  옆 구속 일축 압축이라면 AM 분율은 0.59 · 0.59 · 0.70, 기공률은 0.13 · 0.16 · 0.12 가 돼야 한다.  기둥 압축의 옆 흐름 · 분석 부피 차 · 시료 차 (AM 분율 표준편차 1.5 %p · Table S4) 를 가를 수 없다 [카드 추론] — AM_LH (롤 압연품) 도 같은 크기로 안 닫히므로 옆 흐름만의 문제는 아니다.
- 압연 전 AM_L 의 AM 분율: Table 1 **0.46** ↔ Fig S13 · Table S4 **43 %** (같은 시료 1) — 원문 안 불일치.

### 3-2. ★ 압축 단계별 표 — 재는 조건 = **누른 채** (핀 변위 단계 · 압력 미기록)
| 전극 | 단계 (그림 라벨) | 압축률 % (Fig 3I 에 찍힌 값) | 두께 µm | 기공률 | tortuosity factor | 평균 기공 크기 µm | 비반응면적 ×10⁵ m⁻¹ |
|---|---|---|---|---|---|---|---|
| AM_L | 압축 전 | 0 | **45** [인쇄] | 0.330 [판독] (표 1: **0.325**) | 2.58 [판독] (표 S4: **2.58**) | 0.421 [판독] (표 S4: **0.421**) | 3.60 [판독] |
| AM_L | "7% compression" | 7.0 | 41.9 [카드 산술] | 0.300 | 2.94 | 0.379 | 3.29 |
| AM_L | "15% compression" | 15.0 | 38.3 [카드 산술] | 0.250 | 4.65 | 0.343 | 2.77 |
| AM_L | "22.5% compression" | 22.5 | **35** [인쇄] | 0.190 (표 1 · S3: **0.188**) | 8.79 (표 S3: **8.85**) | 0.309 (표 S3: **0.306**) | 2.22 |
| AM_S | 압축 전 | 0 | **43** [인쇄] | 0.350 (표 1: **0.354**) | 2.32 | 0.406 | 6.27 |
| AM_S | "7% compression" | **8.5** (Fig 1I 라벨 · 캡션은 7 %) | 40.0 (7 %) – 39.3 (8.5 %) [카드 산술] | 0.300 | 2.73 | 0.360 | 5.42 |
| AM_S | "13.5% compression" | 13.5 | 37.2 [카드 산술] | 0.270 | 3.55 | 0.335 | 4.12 |
| AM_S | "24% compression" | 24.0 | **33** [인쇄] | 0.195 (표 1: **0.195**) | 7.56 | 0.284 | 2.43 |

- 판독 방법: Fig 3I · 3J 는 원근 3D 산점도이고 점이 세 벽면의 **투영** 으로만 그려져 있다 → 상자 모서리 직선 맞춤 → 면마다 호모그래피 → 눈금 발로 축 범위 → 표식 바깥 테두리 원 맞춤.  같은 양을 두 면에서 따로 읽어 τ ≤ 0.014 · 기공률 ≤ 0.0002 · 압축률 ≤ 0.03 % 로 일치 · 인쇄된 표 값 (굵은 글씨) 과도 0.005 (기공률) · 0.06 (τ) 안.
- 변화율 [카드 산술]: τ ×3.41 (AM_L) · ×3.26 (AM_S) · 기공 크기 −27 % · −30 % · 비반응면적 **−38 % · −61 %** · MacMullin 수 τ/ε 7.8 → 46.3 · 6.6 → 38.8 (×5.9) · f = ε/τ 0.128 → 0.0216 · 0.151 → 0.0258.
- Bruggeman (τ = ε^−0.5) 대비 [카드 산술]: 압축 전 1.48 · 1.37 배 → 끝 3.83 · 3.34 배.  τ = ε^−α 의 α 는 0.86 → 0.90 → 1.11 → 1.31 (AM_L) · 0.80 → 0.83 → 0.97 → 1.24 (AM_S) — **압축이 진행될수록 지수가 커진다** (한 지수로 못 쓴다).
- 옆 구속 일축 압축 · 고체 보존이면 기공률은 0.280 → 0.212 → 0.135 (AM_L) · 0.290 → 0.249 → 0.145 (AM_S) 여야 한다 [카드 산술: 1 − (1 − ε₀)/(1 − c)] — 측정은 0.300 → 0.250 → 0.190 · 0.300 → 0.270 → 0.195.  기공 기둥 (ε × 두께) 의 감소 8.2 · 8.7 µm 는 두께 감소 10.1 · 10.3 µm 의 **81 % · 84 %** — 나머지는 고체가 분석 부피 밖으로 나간 몫 [카드 산술 · 카드 추론].
- 기공 해상도: 평균 기공 = AM_L **6.6 → 4.8 복셀** · AM_S **6.3 → 4.4 복셀** [카드 산술 · 64 nm] · 입자 지름 = 114 (AM_L) · 81 (AM_S) 복셀 · 시야 ÷ 지름 = 8.8 · 12.3 · 두께 ÷ 지름 = 6.2 · 8.3.
- 뺀 뒤 (다른 시료): 롤 압연 AM_L 44.3 → 35.4 µm (20.1 % [카드 산술] · 그림 라벨 '20% Cal') · 기공률 0.203 · τ 8.34 · 기공 0.324 µm · 입경 7.09 µm · NMC 49.7 % (Table S3 [인쇄] · Fig S10).

### 3-3. ★ 두 전극 (입경 두 가지) 의 차이
| 양 | AM_L ('large') | AM_S ('small') | 표지 · 위치 |
|---|---|---|---|
| 분말 공급사 | MTI (USA) | Targray (Canada) | [인쇄] p.2764 |
| D_mean (STD) | 7.3 µm (3.1) | 5.2 µm (1.8) | [인쇄] p.2748–2749 · Fig 1L 캡션 |
| 개수 분포 (%) · 눈금 2 … 18 µm | 2.9 · 21.6 · 29.5 · 20.9 · 12.2 · 5.8 · 5.0 · 0.7 · 1.4 | 21.7 · 22.6 · 35.0 · 14.1 · 5.5 · 0.9 · 0.2 (2 … 14 µm) | [판독 · 벡터] Fig S13 왼쪽 (= Fig 1L) |
| 분석 입자 수 | ≈139 (Fig S10G 의 기둥 압축 22.5 % 시료는 ≈108 — 같은 기둥으로 읽힘 [카드 추론]) | ≈434 | [카드 산술 — 막대 높이가 정수 개/N 으로 떨어지는 최소 N] |
| 눈금 10 µm 이상 구간의 몫 | 25 % | 6.7 % | [카드 산술] |
| 형상 | ovality (1 − b/a) STD 0.22 · 넓음 | STD 0.13 · *"smaller and more elliptical"* · 0.7 근처 | [인쇄] Fig 2C · 2D · p.2750 |
| 확산 한계 율 C50 / C90 | 3C / 0.8C | 5C / 1.8C | [인쇄] Fig S1 · p.2749 (t_D = r²/D_s · C = 3600/t_D · SI p.3) |
| 압축 전 기공률 · AM 분율 · 두께 | 0.325 · 0.46 · 45 µm | 0.354 · 0.45 · 43 µm | [인쇄] Table 1 |
| 기공 세그먼트 / 노드 수 | 1564 / 1416 | 4028 / 3488 (2.6 · 2.5 배) | [인쇄] Fig S3 |
| 투과도 (압축 전 → 뒤) | 1.7 × 10⁻¹³ → 8.2 × 10⁻¹⁴ m² | 2.5 × 10⁻¹³ → 5.6 × 10⁻¹⁴ m² | [인쇄] Fig 3E–H |
| 비반응면적 (압축 전) | 3.60 × 10⁵ m⁻¹ | 6.27 × 10⁵ m⁻¹ (1.74 배) | [판독] Fig 3J |
| 모델 5C 용량 (압축 전 → 끝) | 101 → 87 mAh g⁻¹ | 149 → 142 mAh g⁻¹ | [판독] Fig 7A |

⇒ '입경' 하나만 다른 짝이 **아니다**: 평균 (1.4 배) · 분포 폭 (STD 3.1 ↔ 1.8) · 형상 · 공급사 (분말 제조 이력) 가 함께 다르다.  원문도 구조 차이의 원인을 *"smaller and narrower distribution"* 로 묶어 쓴다 (p.2753) — 크기와 폭을 가르는 실험은 없다.

### 3-4. ★ 입자 재배열 · 변형 · 파쇄 — 무엇을 봤고 무엇을 안 봤나
| 관찰 | 원문 문장 (쪽) | 근거 | 정량 |
|---|---|---|---|
| 입자 변형 + 회전 (AM_L) | *"particle deformation and rotation (Figures 1G and 1H …) are observed as well, which is consistent with the previous speculation.18"* (p.2748) | Fig 1G 붉은 화살표 · Fig 1H 입자 하나 추적 | 한 입자 예시 |
| 장축이 수평으로 눕는다 | *"It finally settles down with the long axis aligning parallel to the horizontal direction, impeding ion transport."* (p.2750) | Fig 1H · 합성 구조 Fig S2 · S4 | 예시 + 합성 구조 τ (HP 4.51 ↔ VP 2.95) |
| 미끄럼 · 구름 | *"This phenomenon occurred concurrently with inter-particle sliding and rolling, as shown in Figure 1H."* (p.2750) | Fig 1H | 없음 |
| 거시적 자기 재배열 (AM_L) | *"AM_L was undergoing macroscopic self-arrangement, with some particles becoming more spherical at the expense of less elongated ones and vice versa."* (p.2750) | Fig 2C 붉은 막대 (분포 차) | ovality 분포 (입자 ≈139 → ≈108 [카드 산술]) |
| 변형의 크기 | *"the particle deformation is heterogeneous and mild (i.e., each region behaves differently)."* (p.2751) | Fig 2C | 없음 |
| 집단 변형 (AM_S) | *"particles deformed collectively to form a preferential orientation and shape, possibly due to the high lateral constraints from neighboring particles as a consequence of high specific area and small inter-particle gap."* (p.2751) | Fig 2D (0.75 뾰족 · 0.65–0.8 에 약 60 %) · 2G–H | 분포 |
| 방향 | AM_L *"randomly distributed … even after calendering"* · AM_S *"a strong preferential arrangement of the particles even before calendering, evidenced by the clusters around 90° and 270°"* · 압연 뒤 바깥 고리로 (더 수평) | Fig 2E–H | 극좌표 산점 |
| AM_S 에서는 안 보이는 것 | *"Unlike AM_L, free particle movement and localized deformation are not evident in AM_S, possibly as a result of the more stable structure formed by the small particle size."* (p.2748) | Fig 1I–K | 없음 |
| CBD 압축 | *"Yellow arrows indicate the compression of CBD."* (Fig 1 캡션) | Fig 1H | 없음 |
| 기공 연결 상실 (AM_L) | *"it mainly reduces the junction nodes of high coordination number in AM_L"* (p.2751) | Fig 3A 점선 원 · Fig S3 | 배위수별 노드 감소 1.8 / 18.3 / 31.4 / 66.8 / 100 % (배위수 1 · 3 · 4 · 5 · 6) ↔ AM_S 15.6 / 23.5 / 25.2 / 41.9 / 0 % [인쇄] |
| **입자 파쇄** | 이 논문의 관찰 문장 **없음**.  (a) ref 18 의 추측 인용 *"active particles undergo re-arrangement, deformation, and finally fracture under the incremental calendering process.18"* (b) 일반론 *"isolated active materials after a fracture.43"* (p.2759) (c) 추정 *"Calendering a thin electrode (ca. 2 to 3 times of the particle size) has a higher chance to generate cracks between the CBD and active material particle surface"* (p.2762 · 근거 영상 인용 없음) | — | 없음 |

- [카드 관찰] Fig 1E (7 % 단계) 의 큰 2 차입자 안에 균열 · 공극 무늬가 이미 보인다 — 0 % 영상이 실리지 않아 압축으로 생긴 것인지 가를 수 없고 원문은 언급하지 않는다.
- [카드 관찰] ovality 0.7 은 인쇄 정의대로면 최단 ÷ 최장 축 = 0.3 인데 단면 (Fig 1) 의 입자는 그보다 둥글어 보인다 — 등가 타원체를 무엇으로 정했는지 (관성 고유값의 비인지 축 길이의 비인지) · 붙은 입자의 분할 방법은 인쇄돼 있지 않다 [미확인].

### 3-5. 기공 망 · 투과도 (Fig 3A–H · S3 · p.2751–2752)
- 세그먼트 · 노드 [인쇄]: AM_S 4028 · 3488 → 3125 · 2773 (24 %) · AM_L 1564 · 1416 → 1349 · 1242 (22.5 %) → 세그먼트 −22.4 % · −13.7 % · 노드 −20.5 % · −12.3 % [카드 산술].  배위수별 막대 [판독 · 벡터] (배위수 1 · 3 · 4 · 5 · 6): AM_S 1474 / 1736 / 231 / 43 / 6 → 1243 / 1327 / 173 / 25 / 6–7 (인쇄 감소율 0 %) · AM_L 634 / 684 / 83 / 12 / 4 → 623 / 559 / 57 / 4 / 0 (막대 높이 판독 ±1 개).
- 원문 해석: AM_S 는 고르게 줄고 AM_L 은 고배위 접합점이 먼저 사라진다 → *"critical for the global connectivity considering the coarse pore structure in AM_L"*.  ⚠ 배위수 1 = 통로의 끝 — 막다른 가지인지 시료 경계인지 구분돼 있지 않다 [카드 관찰].
- 투과도 (Avizo XLab · no-slip): 압축 전 AM_L 은 AM_S 의 *"approximately 70%"* (1.7 / 2.5 = 0.68) · 압축 뒤에는 **뒤집혀** AM_S (5.6 × 10⁻¹⁴) < AM_L (8.2 × 10⁻¹⁴ m²) — *"electrolyte wetting is hindered by the high surface area and viscous resistance"*.
- *"This is conducive to an even distribution of the compressive stress and strain across the whole electrode."* (p.2751) — 추론 문장이다.  응력 · 변형률은 재지도 계산하지도 않았다.

### 3-6. ★ tortuosity — 정의 · 무엇에 대해 · 값
- 정의 [인쇄] SI p.2: *"Tortuosity, also called tortuosity factor, is a material parameter representing the mass transport resistance from the convoluted 3D morphology of the medium and can be obtained from Fickian type diffusion simulations."* — 식 (1) Q_b = −Aσ ΔT/L · 식 (2) Q_p = −A (ε/τ) σ ΔT/L · 식 (3) **Q_p/Q_b = ε/τ**.  ⇒ τ = ε·σ₀/σ_eff = **tortuosity factor = 우리 tau2 (수송 tortuosity)**.  √ 값 (우리 tau · 웹앱 τ_Lap,eff) 이 아니다.
- 도구 [인쇄] p.2765: *"The tortuosity factor was obtained by the open-source software TauFactor.55"* · 어느 상: 본문 *"the Li+ ion transport resistance arising from the convoluted morphology of the pore phase"* · *"based on fully reconstructed electrodes (3 phases)"* (p.2752) · 캡션 *"Measurements in (E–J) use a three-phase electrode"*.  **방향 (두께 방향인지 세 방향 평균인지) · 경계 조건 · 격자 크기 = 인쇄 없음** [미확인].
- 원문은 'tortuosity' 와 'tortuosity factor' 를 같은 말로 쓴다.  Fig S4 는 *"effective mass transport factor f, equal to the ratio of porosity ε to norminal [sic] tortuosity τ_norm"* (f = ε/τ) 로 다시 같은 꼴을 적는다.
- **CBD 를 넣느냐** (Fig S4 · 합성 구조 PoreSpy · 구 SP / 수평 정렬 HP / 수직 정렬 VP) [인쇄]:

| 구조 | CBD 포함 ('full electrode') f · τ · ε | 2 상 ('two phases') f · τ · ε | τ 비 (3 상 ÷ 2 상) [카드 산술] |
|---|---|---|---|
| HP (수평 정렬) | 0.053 (−8.6 %) · 4.51 (+10.8 %) · 0.24 | 0.20 (−9.1 %) · 1.73 (+6.8 %) · 0.36 | 2.61 |
| SP (구) | 0.058 · 4.07 · 0.24 | 0.22 · 1.62 · 0.36 | 2.51 |
| VP (수직 정렬) | 0.077 (+32.7 %) · 2.95 (−27.5 %) · 0.23 (−4.2 %) | 0.26 (+18.2 %) · 1.38 (−14.8 %) · 0.36 | 2.14 |

  괄호 = SP 대비 (인쇄).  ⚠ 3 상과 2 상은 기공률이 다르다 (0.24 ↔ 0.36) — τ 비 2.1–2.6 에는 기공률 차가 함께 들어 있다.  합성 구조에 CBD 를 어떻게 넣었는지는 인쇄돼 있지 않다 [미확인].  입자 방향의 효과: HP ÷ VP = 1.53 (CBD 포함) · 1.25 (2 상) [카드 산술].
- 측정된 실제 전극의 2 상 tortuosity 는 실리지 않았다 (3 상 값만).

### 3-7. 측정의 흔들림 — 문턱 · 시야 · 시료 · 장치
| 점검 | 값 | 표지 · 위치 |
|---|---|---|
| 입자 경계 문턱 (60 % / 50 % FWHM / 40 % / watershed) | D_mean 7.03 / 7.3 / 7.49 / 7.42 µm (−3.7 % · +2.6 % [카드 산술]) | [인쇄] Fig S11 |
| **기공 문턱** (같은 네 가지) | 기공률 0.353 / **0.325** / 0.288 / 0.310 · 기공 크기 0.462 / 0.423 / 0.398 / 0.404 µm (기공률 +8.6 % · −11.4 % [카드 산술]) | [인쇄] Fig S12 (캡션은 S11 의 복사본) |
| RVE (부피 분율 0.1 → 1.0 · 압축 전 AM_L) | τ 2.46 · 2.52 · 2.51 · 2.53 · 2.54 · 2.59 · 2.61 · 2.59 · 2.58 · 2.60 · 기공률 0.303 · 0.329 · 0.335 · 0.334 · 0.331 · 0.330 · 0.330 · 0.333 · 0.332 · 0.330 | [판독 · 벡터] Fig S14 |
| 시료 간 (압축 전 AM_L · 시료 1 / 2 / 3 / 표준편차) | 기공률 0.325 / 0.310 / 0.343 / 0.016 · 기공 0.421 / 0.403 / 0.441 / 0.019 µm · τ 2.58 / 2.64 / 2.51 / 0.065 · 입경 7.32 / 7.03 / 7.71 / 0.341 µm · NMC 43 / 46 / 44 / 1.52 % (표본 표준편차 n − 1 로 재현됨 [카드 산술]) | [인쇄] Table S4 |
| nano-CT ↔ micro-CT (압축 전 AM_L) | Vol_AM 43 ↔ 45 % · D_AM 7.32 ↔ 7.67 µm (본문 *"4.7% difference"*) | [인쇄] Fig S13 · p.2766 |
| 기둥 압축 (22.5 % · 누른 채) ↔ 롤 압연 (20 % · 뺀 뒤) | 기공률 0.188 ↔ 0.203 (7.3 %) · 기공 0.306 ↔ 0.324 µm (5.5 %) · τ 8.85 ↔ 8.34 (6.1 %) · 입경 7.35 ↔ 7.09 µm (3.6 %) · NMC 51.8 ↔ 49.7 % (4.2 %) | [인쇄] Table S3 |

- ⚠ Table S4 '시료 2' 의 0.310 · 0.403 · 7.03 은 Fig S12 watershed (0.310 · 0.404) · Fig S11 60 % 문턱 (7.03) 과 숫자가 겹친다 — 원문 설명 없음 [카드 관찰 · 판정 안 함].
- 재현 · RVE · 문턱 점검은 전부 **압축 전 AM_L** 에 대한 것이다.  압축 뒤 (기공 4–5 복셀) 와 AM_S 에 대해서는 없다.

### 3-8. 전기화학 모델 결과 (60 % DoD 필드 · 율 특성)
- 모델 = 반쪽 셀 (*"NMC622 versus Li metal"* · 물성 Table S1) 을 AM_L · AM_S · AM_LH 의 재구성 3D 구조에 돌림 (p.2753).
- 입자 크기별 리튬화 (AM_L · Table S2 [인쇄]): 5 µm 입자 평균 SoL 0.69 (0.038) / 0.69 (0.043) / 0.66 (0.089) · 11 µm 입자 0.59 (0.075) / 0.60 (0.087) / 0.54 (0.131) — 압축 전 3C / 22.5 % 3C / 22.5 % 5C · 괄호 = 입자 안 표준편차.  본문: 11 µm 입자는 5 µm 입자보다 **14 % (3C) · 18 % (5C)** 덜 리튬화.
- 전해질 농도 구배: 22.5 % 압축에서 2.5 배 · 3C → 5C 에서 +180 % · AM_S 는 25–30 % 낮음 — 그래도 *"Li+ ion transport is not the primary performance-limiting factor"* (두께 ≈35 µm · NMC 분율 ≈0.45 · p.2755).
- 모델 정격 용량 (mAh g⁻¹ · 0.2 / 0.5 / 1 / 2 / 3 / 5C) [판독 · Fig 7A · 삼각형 ±0.7 · \* = 일부 가려진 표식]:

| 전극 | 0.2C | 0.5C | 1C | 2C | 3C | 5C |
|---|---|---|---|---|---|---|
| AM_L (Uncal) | (가림) | (가림) | (가림) | 143.1\* | 129.8 | 101.4 |
| AM_L (22.5 % Cal) | 168.0 | 161.6 | 151.5 | 133.5 | 117.8 | 87.3 |
| AM_L1.5 | 165.5 | 157.1 | 142.1 | 124.6 | 110.0 | 75.9 |
| AM_L2 | 161.8 | 150.2 | 133.9\* | 111.3 | 95.0 | 55.2 |
| AM_S (Uncal) | 179.9\* | (가림) | 170.4\* | 165.3\* | 159.4\* | 148.5 |
| AM_S (24 % Cal) | 177.7 | 174.5 | 168.0 | 161.6 | 156.5 | 142.0 |
| AM_S1.5 | 175.4 | 171.7 | 165.5 | 158.2 | 148.7 | 128.7 |
| AM_S2 | 170.6 | 165.9 | 159.5 | 150.2 | 140.5 | 110.7 |

  원문: AM_L 은 3C 위에서 80 % 를 못 지키고 AM_S 는 5C 에서도 지킨다 (p.2755) — 판독으로는 AM_S 5C/0.2C = 82.5 % (압축 전) · 79.9 % (24 %) · AM_S2 3C/0.2C = 82.4 % [카드 산술].
- 평균 전압 (Fig S8 [판독 · 벡터] · 0.2 → 5C): AM_L 3.801 → 3.707 (압축 전) · 3.801 → 3.657 (22.5 %) · AM_S 3.798 → 3.751 · 3.797 → 3.744 V.  본문 인쇄값 3.706 · 3.656 V 와 맞는다 · 본문 *"AM_S can maintain the Vavg above 3.75 V at 5C"* 는 압축한 AM_S (3.744) 에는 안 맞는다.
- 민감도 두 팔 (AM_L 22.5 % · 3C · Fig 6G): 고체 확산을 빠르게 (Ds_f) → 전압 · 용량 모두 ↑ (≈117 → ≈138 mAh g⁻¹ [눈대중]) · 반응 상수를 빠르게 (j00_f 2 × 10⁻⁵ ↔ 5.06 × 10⁻⁶) → 전압만 ↑ ⇒ *"it is the solid-state diffusion that predominantly restricts the cell performance under high-rate conditions"* (p.2759).  V_eq 차 최대 0.04 V (작은 ↔ 큰 입자) · μ_p 면내 변동 ±0.01 V · μ_e 는 고르다 (*"Due to the high electronic conductivity"*).
- 모델 ↔ 실험 (AM_LH · Fig 5E · F): *"in good agreement with the experimental results (solid lines), except for a noticeable discrepancy at 5C"* (p.2755–2756).
- GITT D_s (NMC622 · Fig S7 [판독 · 벡터]): 압축 전 2.36 × 10⁻¹⁰ (DoD 0) → 9.7 × 10⁻¹¹ (0.48) → 6.5 × 10⁻¹² cm² s⁻¹ (0.92) · 18 % 압연 2.05 × 10⁻¹⁰ → 1.6 × 10⁻¹² (0.95) · 모델 선 Ds_0 2.20 × 10⁻¹⁰ → 4.0 × 10⁻¹² · 압연 ÷ 압축 전 = 0.68–0.87 (DoD ≤ 0.66 · 같은 순번 점끼리 [카드 산술]) — 본문은 *"the solid-state diffusion rate is not markedly dependent on calendering"*.

### 3-9. 두께 × 기공률 (Fig 7D · Fig 8)
- 가상 전극: *"virtually mirroring and/or cropping the existing electrodes of three different porosities"* (p.2762) · 3C 용량 면 — AM_S 145.4–170.0 · AM_L 98.40–145.0 mAh g⁻¹ (컬러바 [인쇄]) · 축 두께 40–70 µm · 기공률 0.20–0.32.
- AM_S: 대각선으로 단조 감소 (*"thickness and porosity play an equivalently important role"*).  AM_L: *"0.25 can be regarded as a transition point, above which the electrode thickness is not particularly influential, compared to the region below 0.25, where a catastrophic performance decrease is observed."*
- 전해질 고갈: 집전체 쪽 C_ey 600 → 500 → 400 mol m⁻³ (AM_S · S1.5 · S2 · 60 % DoD) · AM_S2 방전 끝 (83 % DoD) < 200 mol m⁻³ (초기 700) [인쇄] p.2761.
- 실험 (Fig 8 [인쇄 · 그림 라벨]): 1 mAh cm⁻² 30 → 25 µm · 2 mAh cm⁻² 48 → 39 µm · 3 mAh cm⁻² 74 → 57 µm (*"calendered to ca. 20%"* · 16.7 · 18.8 · 23.0 % [카드 산술]) — 탈압 뒤 두께.  2 mAh 쌍 = Table 1 의 AM_LH (NMC622) 와 같은 두께 · 1 · 3 mAh 전극의 재료 · 조성 [미확인].  3 mAh 압연 전극의 용량은 AM_L2 모델 예측과 *"within 10% variation"*.
- *"the gravimetric capacity assessed in this study highlights the utilization of the active material under calendering, however, the volumetric capacity always increases with incremental calendering."* (p.2763)

---

## 4. ★ 방법 — 장치 · 측정 사슬 · 계산

### 4-1. 장치 · 시료 (p.2765 · Fig 1A–D)
- 압연 전 전극에서 1 mm 원판을 따 에폭시로 핀 끝에 붙이고 레이저로 **지름 < 90 µm 기둥** 으로 깎는다 (ref 53).
- Zeiss Xradia Ultra 810 안의 나노 기계 시험대 (refs 35 · 36): *"A flat-headed stainless-steel pin, attached to a piezo-mechanical actuator, was used to compress the electrode."* — 위에서 누르는 핀 · 아래 집전체 + 받침 핀 (Fig 1B · C) · **옆벽 없음**.
- 5.4 keV 준단색 평행광 · 복셀 64 nm (binning 1) · 시야 64 × 64 µm² · *"1,201 radiographic projections … at an exposure time of 60 s over 144° rotation of the pillars"* · 필터 역투영 · Avizo 9.5.
- **인쇄되지 않은 것**: 하중 · 압력 · 변위량의 절대값 · 변위 속도 · 단계 사이 유지 시간 · 촬영 중 이완 · 압축률을 정한 방법 (핀 변위인지 영상 두께인지) · 시험 온도 · 분위기.
- 롤 압연 대조: 사진 (Fig S10) 뿐 — 롤 간격 · 선하중 · 온도 · 속도 [미확인].

### 4-2. 측정 사슬
1. 전극 기둥과 CBD 만의 막 (탄소 : PVDF 50:50) 을 **따로** 누르고 찍는다 (Fig 1C · 1D).
2. DSS (dual-scan superimposition · refs 25 · 26): 전극 영상에서 입자와 큰 기공을 가르고, 흐릿한 탄소-바인더 영역은 CBD 막 영상 (대비가 더 좋다) 으로 **바꿔 넣는다** → 3 상.  두 시료의 압축 단계를 어떻게 맞췄는지는 인쇄돼 있지 않다 [미확인].
3. 문턱 분할 — FWHM (50 % 대비) 기준 (Fig S11 · S12).
4. 정량: 입자별 관성 모멘트 → 크기 · 장축 방향 · ovality (ref 37) · 기공 골격 + 노드 배위수 · 평균 기공 크기 · 비반응면적 (입자/기공 계면) · tortuosity factor (TauFactor) · 투과도 (Avizo XLab).
5. 같은 3 상 구조를 격자로 만들어 전기화학 모델에 넣는다 (4-3).

### 4-3. ★ 계산
- **tortuosity factor**: TauFactor (ref 55) — 정상 확산 (Laplace) 을 복셀에서 풀어 τ = ε·D₀/D_eff (SI 식 1–3 의 꼴).
- **투과도**: Avizo XLab · 입구 · 출구에 압력차 · no-slip (p.2765–2766).
- **3D 미세구조 분해 전기화학 모델** (p.2766 · SI p.12–14): 3 상 분할 → Simpleware ScanIP N-2018.03 적응 격자 → COMSOL Multiphysics 5.5 · gPNP (ref 56 · Newman 계열 ref 38 · 농축 용액).  *"No volume-averaged material parameters, such as porosity, tortuosity, and particle size were used in the microstructure-resolved model."*

| 영역 | 식 (SI p.13) |
|---|---|
| 기공 (전해질) | (4) F ∂C_ey/∂t + ∇·J_p = 0 · (5) J_p = −t_p σ_io ∇μ_p · (6) −F ∂C_ey/∂t + ∇·J_n = 0 · (7) J_n = (1/t_p) F D_io ∇C_ey − (1 − t_p) σ_io ∇μ_p |
| NMC 입자 | (8) F ∂c_s/∂t + ∇·J_s = 0 · (9) J_s = −F D_s ∇c_s · (10) ∇·J_e = 0 · (11) J_e = −σ_e ∇μ_e |
| CBD | (12) ∇·J_e = 0 · (13) J_e = −σ_e ∇μ_e (전자만 — 이온 · 반응 없음) |
| 기공/NMC 경계 | (14) J_ct = j₀ [exp(αF/RT (μ_p − μ_e + V_eq)) − exp(−(1 − α)F/RT (μ_p − μ_e + V_eq))] · (15) j₀ = j₀₀ C_ey^α c_s^α (c_s^max − c_s)^(1−α) |
| 경계 조건 | 분리막 쪽: μ_p = 0 · n·J_n = n·J_s = n·J_e = 0 / 기공–NMC: n·J_p = J_ct · n·J_n = 0 · n·J_s = J_ct · n·J_e = J_ct / 집전체 쪽: n·J_p = n·J_n = n·J_s = 0 · n·J_e = I/A_e · I = (c_s^acc − c_s^in) v_AM V (F/3600)(C_rate/A) |
| 초기 조건 | C_ey = C_in · μ_p = 0 · c_s = c_s^in · μ_e = OCV |

- 입력 (Table S1 [인쇄]): D_s = GITT 곡선 (칸에는 *"From Error! Reference source not found."* — 깨진 상호참조 · Fig S7) · σ_e(NMC) 1.039 × 10⁻³ S m⁻¹ · c_s^max 32000 mol m⁻³ · SoL_in 0.2 · SoL_max 1 · D_io · σ_io = 농도 · 온도 상관식 (SI ref 5) · C_in 700 mol m⁻³ · t_p 0.38 · σ_e(CBD) 0.375 × 10³ S m⁻¹ · j₀₀ 5.06 × 10⁻⁶ (빠른 팔 2 × 10⁻⁵) A m^2.5 mol^−1.5 · α 0.5 · T 298 K.  CBD ÷ NMC 전자 전도 = 3.6 × 10⁵ 배 [카드 산술].
- **맞춘 값**: 인쇄된 것은 없다 (D_s = GITT · 나머지 = 문헌).  검증 = AM_LH 방전 곡선 6 율 (Fig 5E · F).  **격자 요소 수 · 계산 영역 크기 · 시간 간격 · 수렴 · 계산 시간 = 인쇄 없음** [미확인].
- 본문의 유일한 식 (번호 없음 · p.2759): η_act = μ_p − μ_e + V_eq(SoL).

### 4-4. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM (구 입자) 의 한계 — 원문 문장** (p.2747 서론): *"Spherical particles were used to study the mechanical responses and porosity variation of the electrode under different calendering steps.19 However, these studies were conducted based on simplified electrode geometries that were artificially synthesized with spherical particles, ignoring the influence of particle shape and orientation on mass transport and electrochemical performance. More importantly, the carbon-binder domain (CBD), which is critical in determining the microstructural heterogeneities and electronic conductivity,20,21 especially under compression, was not taken into account."* — ref 19 = Sangrós Giménez 외, *Powder Technol.* 349 (2019) 1–11 (DEM 압연).  이 논문이 꼽은 한계 = **① 구 가정 (형상 · 방향 무시) ② 인공 합성 구조 ③ CBD 누락**.  겹침 · 상대밀도 상한 · 접촉 독립 가정 · 보정값의 지위 같은 접촉역학 쪽 한계는 **말하지 않는다**.  DEM 을 직접 쓰지도 않았다.
- **(ii) 소성 · 큰 변형이 왜 어려운가 / 이 논문의 우회**: 원문은 이유를 논하지 않는다.  우회 = **계산하지 않고 찍는다** — 눌린 실제 구조 (입자 변형 · CBD 압축 포함) 를 나노 CT 로 얻어 그대로 수송 · 전기화학 계산의 격자로 쓴다.  맞춘 역학 값 **0 개** · 대가 = 단계당 ≈20 h 촬영 [카드 산술] · 시야 64 µm (입자 지름의 9–12 배) · 시료 하나 · 응력 정보 없음.
- **(iii) 차원**: 영상 · 정량 · 모델 전부 3D.  2D → 3D 전이에 대한 말은 없다 (ref 22 = 3D ↔ 스테레올로지 비교를 영상 기법 인용으로만 든다).
- **(iv) 압력을 뺄 때**: 다루지 않는다.  단계 영상은 모두 누른 채이고 마지막 단계 뒤 하중을 뺀 영상은 없다.  유일한 '뺀 뒤' 자료 = 롤 압연한 다른 시료 (Table S3 · Fig S10) 와 Fig 8 의 두께 — 압축률이 달라 (22.5 ↔ 20 %) 되돌아옴으로 읽을 수 없다.
- 입자 표현: 영상에서 분할한 **실제 형상** (비구형 2 차입자) — 정량에서는 등가 타원체 (원기둥 표시) · 전기화학 모델에서는 분할 형상 그대로 (구 가정 없음 · 식 8–9 를 3D 로 푼다).

### 4-5. 기법 미니 용어집
- **DSS (dual-scan superimposition)**: 전극과 CBD 만의 시료를 따로 찍어 CBD 영역의 회색값을 대비가 좋은 두 번째 영상으로 바꿔 넣는 3 상 재구성법 (refs 25 · 26).
- **FWHM 분할**: 경계를 가로지르는 회색값 선 프로파일의 50 % 높이를 문턱으로 삼는다.
- **ovality**: 1 − b/a (b/a = 등가 타원체의 최단 ÷ 최장 축) — 0 = 구.
- **tortuosity factor (이 논문의 'tortuosity')**: τ = ε·σ₀/σ_eff (SI 식 3) = Tjaden 의 κ = τ² = 우리 tau2.
- **MacMullin 수**: N_M = τ/ε = σ₀/σ_eff (이 논문은 쓰지 않는다 · 카드 산술용).
- **C50 · C90**: 입자의 50 % · 90 % 가 고체 확산에 막히지 않는 최대 율 — t_D = r²/D_s · C = 3600/t_D (Fig S1 캡션).
- **gPNP**: generalized Poisson–Nernst–Planck — 농축 용액 전해질 + 고체 확산 + Butler–Volmer 를 실제 3D 형상 위에서 푸는 Newman 계열 모델.
- **AM_L1.5 · L2 · S1.5 · S2**: 압축 뒤 구조를 두께 방향으로 거울상 복제해 1.5 · 2 배로 만든 가상 전극.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 그래픽 초록 | 기둥 방사선 사진 · 압축 단계 단면 · 원기둥 표시 · SoL (3C) | 한눈 요약 |
| 1 (A–L) | ★ 장치 (A · B) · 압축 전 방사선 사진 (C) · CBD 만 (D) · AM_L 7 / 15 / 22.5 % 단면 (E–G) · 입자 회전 추적 (H) · AM_S 7 / 13.5 / 24 % + 입자 사이 거리 (I–K) · 입도 (L) | 옆 구속 없는 기둥 압축이라는 사실 · AM 회전 (R1) 의 실측 그림 |
| 2 (A–H) | ★ 입자별 원기둥 표시 (A · B) · ovality 분포 압축 전 / 뒤 / 차 (C · D) · 방향 극좌표 (E–H) | 비구형 입자의 관측량 정의 (구 DEM 에는 없는 양) |
| 3 (A–J) | ★ 기공 골격 (A–D) · 투과도 유선 (E–H) · 압축률–기공률–tortuosity (I) · 압축률–기공 크기–반응 면적 (J) | 단계별 값의 원천 [판독] · tau2 꼴 τ(ε) |
| 4 (A–X) | 60 % DoD 의 SoL · η_act · C_ey · J_p 필드 (압축 전 / 3C / 5C × 두 전극) | 우리 STEP4 출력과 같은 종류 (액체 전해질) |
| 5 (A–I) | 모델 방전 곡선 (A–D) · AM_LH 모델 ↔ 실험 (E · F) · 두께 방향 η_act · SoL (G–I) | 영상 기반 모델의 검증 꼴 (율 6 개 곡선 대조) |
| 6 (A–K) | AM_L 22.5 % 3C: 기본 / 빠른 확산 / 빠른 반응 의 SoL · η_act · 방전 곡선 (G) · μ_e · μ_p · V_eq | 지배 인자를 가르는 민감도 두 팔 |
| 7 (A–D) | ★ 모델 용량 vs 율 (A) · 가상 후막의 SoL · C_ey (B · C) · 두께–기공률 용량 지도 (D) | '후막 설계' 인용의 실제 내용 (가상 ≤ 70 µm) |
| 8 (A–F) | 실험: 1 · 2 · 3 mAh cm⁻² 압연 전 / 뒤 방전 곡선 + 두께 라벨 | 탈압 뒤 두께 (30 → 25 · 48 → 39 · 74 → 57 µm) |
| Table 1 | ★ 전극 10 종의 면적 용량 · AM 분율 · 두께 · 기공률 | 양 끝 인쇄값 · 고체 보존 산술 |
| S1 | 확산 시간 상수 분포 · C50 · C90 | 입자별 확산 한계 척도 |
| S2 | 합성 구조 SP · HP · VP 의 유선 · 플럭스 | 입자 방향 → 수송 |
| S3 | ★ 기공 망 노드 · 세그먼트 (압축 전 / 뒤 × 두 전극) | 연결성 지표의 정의와 값 |
| S4 | ★ f = ε/τ · τ · ε — CBD 포함 ↔ 2 상 | τ 규약 확인 · 제 3 상을 빼면 τ 가 낮아지는 크기 |
| S5 | 0.5C 의 SoL (균일) | 고율과의 대조 |
| S6 | 입자 반경 방향 SoL (5 · 11 µm 입자) | Table S2 의 원자료 |
| S7 | GITT D_s(DoD) · 모델 선 Ds_0 · Ds_f | 모델 입력 (NMC622) |
| S8 | 모델 평균 전압 vs 율 | 본문 3.706 · 3.656 V 의 원천 |
| S9 | GITT 원곡선 | OCV · D_s 출처 |
| S10 | ★ 기둥 압축 ↔ 롤 압연 (분할 · 입도 · 틈 분포 · 44.3 → 35.4 µm) | '기둥 압축 = 압연' 근거의 전부 |
| S11 · S12 | ★ 문턱 민감도 (입자 · 기공) | 영상 기공률의 연산자 민감도 (단계 0) |
| S13 | nano-CT ↔ micro-CT | 대표성 |
| S14 | ★ RVE (부피 분율별 τ · 기공률) | 수렴 보고 꼴 |
| S15 | 시료 2 · 3 의 입도 | 시료 간 산포 |
| Table S1 | 모델 입력 | 4-3 |
| Table S2 | 입자 크기별 평균 SoL | 3-8 |
| Table S3 | ★ 기둥 압축 ↔ 롤 압연 수치 | 누른 채 ↔ 뺀 뒤 (다른 시료) |
| Table S4 | ★ 시료 간 산포 | 측정 잡음 눈금 |
| 식 | SI (1)–(3) tortuosity factor 정의 · (4)–(15) gPNP · 경계 · 초기 조건 · Table S1 전해질 상관식 · Fig S1 캡션 t_D · C · 본문 η_act | 식별 크롭 22 장 (`eq_*.png`) |

## 6. Post-processing ★
| 후처리 | 도구 · 방법 | 수치화 · 그림 | 우리 재사용 |
|---|---|---|---|
| 3 상 분할 | DSS + FWHM 문턱 (Avizo 9.5) | Fig S11 · S12 문턱 민감도 | 영상 대조를 설계할 때 문턱 ±10 % 를 결과 전에 적는 꼴 |
| 입자 형상 · 방향 | 관성 모멘트 → 등가 타원체 → ovality · 장축 각 | 분포 (Fig 2C · D) · 극좌표 (Fig 2E–H) | 구 모델에는 없는 양 — 비구형 입자 계산을 할 때만 |
| 기공 망 | 골격화 + 노드 배위수 | 배위수별 막대 (Fig S3) | 우리 SE 망의 배위 분포와 같은 종류의 연결성 지표 (상은 반대) |
| tortuosity factor | TauFactor (3 상 기공) | 압축률별 (Fig 3I) | tau2 와 같은 꼴 — 이름 대조표 (비교 문서 J 절) |
| 투과도 | Avizo XLab (no-slip) | 값 4 개 (Fig 3E–H) | 대응 양 없음 (ASSB) |
| 비반응면적 | 입자/기공 계면 면적 ÷ 부피 (정의 미기재) | 압축률별 (Fig 3J) | 우리 피복률 · STEP4 반응 면적과 같은 자리 |
| RVE · 재현 | 부피 팽창법 · 시료 3 개 | Fig S14 · Table S4 | 수렴 · 산포 보고 꼴 |
| 확산 한계 | t_D = r²/D_s · C = 3600/t_D | 누적 분포 (Fig S1) | STEP4 입자별 확산 척도 |
| 전기화학 필드 | COMSOL gPNP | 60 % DoD 3D 필드 · 두께 방향 평균 ± 면내 변동 (Fig 5G–I) | 필드를 두께 방향 평균 + 면내 산포 띠로 줄이는 표시법 |

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · `docs/` 출처)

### 7-1. 비교표
| 축 | 이 논문 | 우리 | 같은 것 / 다른 것 / 왜 |
|---|---|---|---|
| 재료계 | NMC111 (· 622) + C65 + PVDF · 액체 전해질 | NCM811 + LPSCl (+ 첨가제) · 전고체 | **다르다** — 값 전이 불가 |
| 이온 통로 | **기공** (눌리면 닫힌다 → τ ↑) | **SE 고체** (눌리면 이어진다) | **반대** — τ(압축) 의 방향을 서로 근거로 쓰지 않는다 |
| 무른 상 | CBD — 다공 · 눌리면 부피가 준다 | SE — 부피 보존 유동 (MPM ν 0.49) | **반대 성질** |
| 가압 | 기둥 압축 · 옆 구속 없음 · 변위 단계 · **압력 미기록** | 판 사이 일축 300 MPa · 주기 경계 (옆 구속) | 다르다 — 두께 감소의 81–84 % 만 기공으로 [카드 산술] |
| 입자 | 실제 형상 (영상) · 회전 · 변형 관찰 | DEM = 구 (겹침이 변형의 대리) · MPM 골격 런 = AM 고정 | 이 논문은 **AM 이 돌고 미끄러진다** 는 실측 그림 (LIB) — 우리 구는 돌아도 장축이 없다 |
| 역학 계산 | **없음** | DEM (탄성-이력 · E_eff 1.35 GPa) · MPM (J2 · E 1.53 · σ_y 0.30) | 견줄 계산이 없다 |
| tortuosity | 'tortuosity' = tortuosity factor (TauFactor · 기공상 3 상) 2.3 → 8.8 | tau2 = φ·σ₀/σ_eff (접촉망 · SE 상) | **같은 꼴 (tau2)** · 다른 상 · 다른 이산화 |
| 반응 면적 | 입자/기공 계면 (CBD 가 덮으면 빠진다) −38 · −61 % | AM 피복률 (SE 가 덮은 몫) · STEP4 반응면 | 같은 자리의 양 — 방향이 반대 (LIB 는 덮이면 손해 · ASSB 는 SE 가 덮어야 반응) |
| 전기화학 | 3D 분해 gPNP (COMSOL) | STEP4 (복셀 + 입자별 구형 확산) | 같은 종류 — 그쪽은 입자 안 확산도 실제 형상 |
| 검증 | 방전 곡선 6 율 (전극 한 쌍) · 5C 불일치 인정 | — | 보고 꼴 참고 |
| 탈압 | 없음 | 언로딩 트랙 | 줄 것 없음 |

### 7-2. ★ 랩 기준과 나란히 (판정 없이)
| 양 | 랩 표준 · 우리 값 | 이 논문 | 비고 |
|---|---|---|---|
| 순수 SE 기공률 | 10–13 % (랩 표준 · 고정) | **없음** (SE 가 없다) | 나란히 놓을 숫자 없음 |
| LPSCl 진밀도 | 1.64 g/cm³ (랩 표준 · 고정) | **없음** | 〃 |
| 복합 전극 기공률 | (우리 DEM 침대 · ε_sphere 등) | 0.33–0.35 → 0.19 (영상 3 상 · CBD 나노 기공 포함 · 누른 채) | 재료 · 연산자 · 상태가 달라 대조하지 않는다 |
| Heckel · 항복 | DEM P_y 138 MPa · MPM σ_y 0.30 GPa | **압력 축 없음** | 대조 불가 |
| tortuosity (tau2 꼴) | 수송 tortuosity (SE 상) | 2.3–8.8 (기공상) | 같은 정의 · 다른 상 — 값 비교 안 함 |

### 7-3. 같은 것 · 다른 것 · 왜 (통제 요인부터)
- **재료 전이**: LIB ↔ ASSB.  이 논문의 '압연하면 tortuosity 가 3.3–3.4 배' 는 **이온 통로인 기공이 닫히기 때문** 이다.  전고체에서 압밀은 이온 통로 (SE) 를 잇는 쪽으로 작용한다 → 이 숫자 · 방향을 우리 σ_ion(P) 의 근거로 쓰면 부호가 틀린다.
- **구속**: 기둥 (옆 자유) ↔ 우리 (옆 구속).  표 1 의 고체 보존이 안 닫히는 것 (§3-1) 이 그 표시다 — 같은 두께 감소에서 우리 쪽이 기공을 더 닫는다.
- **무른 상의 성질**: CBD 는 나노 기공을 가진 압축성 상 (Fig 1H 노란 화살표) — 우리 MPM 의 SE (ν 0.49 · 부피 보존) 와 반대.  'CBD 를 SE 의 대리' 로 읽지 않는다.
- **입자 형상**: 이 논문의 핵심 관찰 (방향 · ovality) 은 비구형 입자에서만 정의된다.  우리 DEM 은 구 — frame [1]/[2] 의 '입자 형상은 안 변한다' 에 더해 '형상 자체가 없다'.
- **판독값**: 가운데 단계 값은 전부 [판독] — 표지 없이 인용하지 않는다.

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문은 **역학도 접촉망도 계산하지 않는다** — 실험 영상이 구조를 주고 (우리 MPM 반쪽이 내려는 '눌린 형상' 을 측정으로 대신) 그 위에서 연속체 수송 · 전기화학 (우리 STEP3 · STEP4 와 같은 종류) 을 푼다.
- 가진 것: 실제 3 상 형상 · 탄소-바인더 · 입자 안 3D 확산.  없는 것: 응력 · 하중 분담 · 접촉 저항 · 탈압 · 조성 · 압력을 바꿔 보는 예측 능력 (영상이 있는 상태만 계산할 수 있다).

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나

| 이름 | 이 논문이 주는 것 | 못 주는 것 |
|---|---|---|
| 단계 0 (기공 연산자 · 판정 기준) | 영상 기공률의 흔들림 눈금: 분할 문턱 ±10 % → 0.288–0.353 (0.325 기준 −11 / +9 %) · 시료 간 ±0.016 · RVE 는 부피의 20 % 부터 기공률 수렴 · τ 는 60 % 부터.  '무엇을 기공으로 세나' = 큰 기공 + CBD 안 나노 기공 (다른 시료에서 옮겨 넣음) — **연산자를 적지 않으면 값이 0.03 씩 움직인다** 는 실례 | 질량 · 진밀도 기준 기공률 (없음) · SE 계의 값 |
| 단계 1 · 2 · 3 | 없음 | — |
| 단계 4 (순수 SE) | 없음 (SE 없음) | 전부 |
| 단계 5 (3D 복합 가압) | 현상 목록: 큰 AM 이 **회전 · 미끄럼** 하며 재배열 (Fig 1H) · 작은 AM 은 이웃 구속으로 집단 거동 · 무른 기지가 AM 사이에서 눌린다.  **값은 못 쓴다** (압력 없음 · 옆 구속 없음 · CBD ≠ SE) | 결과 전 대조 값 (기공률 · 두께 · 압력) |
| 단계 6 (탈압) | 없음 — 누른 채 영상만.  Table S3 (기둥 22.5 % ↔ 롤 20 %) 는 압축률 · 시료가 달라 되돌아옴이 아니다 | 전부 |
| 단계 7 (형상 · 피복 · 수송) | (a) tortuosity factor 정의 문장 + 식 (tau2 꼴) (b) 제 3 상 (CBD) 을 넣으면 τ 2.1–2.6 배 (합성 구조 · 기공률 차 포함) (c) 반응 면적이 압축으로 −38 · −61 % — 구 근사 6φ/D 대비 0.95 → 0.52 (AM_L) · 1.21 → 0.42 (AM_S) [카드 산술 · 평균 지름 구 근사] = 압축 뒤 입자 표면의 절반쯤만 기공에 닿는다 (d) 필드를 '두께 방향 평균 ± 면내 변동' 으로 줄이는 표시 | SE 상 수송 · 접촉 저항 · 전고체 반응면 |
| 후보 D0 (지금 DEM) | 인용할 **한계 문장** (구 · 형상 · 방향 · CBD 누락 · p.2747) — 우리 D0 (구 · 바인더 없음) 에 그대로 해당 | 접촉 법칙 · 겹침 상한 · 연화의 지위에 대한 말 |
| 후보 A′-0 · A′ · B · C · C′ · M0 | 없음 (역학 모델 없음) | — |
| 후보 A (AM 을 움직이는 강체로) | 간접 근거: 눌리는 동안 AM 이 **돌고 자리를 바꾼다** (큰 입자 · 넓은 분포에서 뚜렷) → AM 을 얼려 둔 계산 (우리 골격 런) 이 놓치는 자유도.  단 LIB · 다공 CBD 기지 · 옆 자유 | 전고체 (SE 기지 · 300 MPa) 에서의 AM 운동량 |
| U0–U6 | U6 (해상도 수렴) 에 보고 꼴 하나: 부피 팽창 RVE 곡선 (Fig S14) · 평균 기공 = AM_L 6.6 → 4.8 · AM_S 6.3 → 4.4 복셀 [카드 산술] 에서의 τ 를 수렴 점검 없이 보고한 사례 (반면교사) | 단위 시험 자체 |
| R1 (AM 이 움직이고 하중 분담) | 운동 = 관찰됨 (정성) · **하중 분담 = 없음** (응력 측정 · 계산 없음 · *"even distribution of the compressive stress and strain"* 은 추론) | 하중 몫 |
| R2 (미끄럼 · 분리) | *"inter-particle sliding and rolling"* (정성 · p.2750) · *"cracks between the CBD and active material particle surface"* (추정 · p.2762) | 정량 |
| R3 · R4 · R5 | 없음 (R5: 맞춘 역학 값이 0 개라 해당 없음) | — |
| R6 (무른 입자 형상 변형) | 없음 — 무른 상이 입자가 아니라 CBD 막이다 | — |
| R7 (AM 파괴) | 정량 없음.  ref 18 (Günther 2020) 의 '재배열 → 변형 → 파쇄' 추측을 인용하고 자기 관찰은 *"heterogeneous and mild"* 변형까지 | 파쇄 문턱 · 빈도 |
| 결과 전 대조 항목 | **넣지 않는다** — 압력 · 구속 · 재료 · 수송 상이 달라 무엇을 견줘도 판정이 안 된다.  넣는다면 '구 모델에서도 정의되는 양' (입자 회전량 · 이웃 교체 수) 을 **현상 유무** 로만 | 값 |
| 랩 표준 · 우리 DEM · MPM 과 견줄 자리 | 없음 (순수 SE · 진밀도 · 압력 · 항복 어느 축도 없다).  E_eff 1.35 GPa · P_y 138 MPa · E 1.53 · σ_y 0.30 · ν 0.49 와 나란히 놓을 숫자 0 개 | — |

- **흐름 밖 (접촉망 수송 · STEP4)**: ① 이 그룹의 'tortuosity' 숫자를 우리 표에 옮길 때는 tau2 열에 넣는다 (√ 열 아님).  ② '고체 확산 한계 ↔ 반응 면적 한계' 를 가르는 민감도 두 팔 (D_s ↑ · j₀₀ ↑ · Fig 6G) 은 STEP4 에서 그대로 쓸 수 있는 진단 설계다.  ③ 입자별 확산 한계 율 C = 3600·D_s/r² 의 누적 분포 (C50 · C90) 는 입도 설계 지표로 싸다.  ④ D_s 는 NMC622 · 액체 반쪽 셀 GITT 겉보기 값 (2.4 × 10⁻¹⁰ → 6.5 × 10⁻¹² cm² s⁻¹ = 2.4 × 10⁻¹⁴ → 6.5 × 10⁻¹⁶ m² s⁻¹ [판독]) — 전고체로 옮기지 않는다 (액체 셀 다결정 값의 전이 문제 = 메인 리포 `docs/ncm_sc_poly_electrochem_anchors.md`).

---

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **τ 이름표** — 비교 문서 J 절에 한 줄: Lu 2020 = *"Tortuosity, also called tortuosity factor"* · ε/τ 꼴 = tau2 · TauFactor · 3 상 기공.  같은 그룹의 다른 논문은 그 논문의 정의를 따로 확인한다 (이 논문 = TauFactor 꼴).
2. **영상 대조를 쓸 때의 사전 등록 칸** (단계 0): 분할 문턱 (±10 % 민감도) · 시야 ÷ 입자 지름 · 시료 수 · 누른 채 / 뺀 뒤 · 옆 구속 유무 · 제 3 상 포함 여부 — 이 논문은 그 칸을 SI 에 실어 둔 드문 예이고, 그래도 압축 뒤 상태에 대한 점검은 없다.
3. **in situ CT 문헌을 가압 대조점으로 쓸 때**: 시편이 다이 안인지 (kodama2020 · sakka2022 = 옆 구속) 기둥인지 (이 논문 = 옆 자유) 를 먼저 적는다.  기둥 자료의 기공률–압축률 곡선은 일축 압밀 곡선이 아니다.
4. **'소입자 = 균일 변형' 을 인용할 때의 한정어**: 두 전극 (5.2 ↔ 7.3 µm) · 분포 폭 · 형상 · 공급사 동반 변화 · LIB · 변형률 미측정.  '작을수록' 이 아니라 '작고 분포가 좁은 전극이' 로 쓴다.
5. **반응 면적의 자리**: 압축이 무른 제 3 상을 AM 표면에 눌러 붙여 반응 면적을 줄인다 (LIB 에서는 손해).  우리 쪽에서는 첨가제 (탄소 · 바인더) 가 AM–SE 반응면을 가리는 몫이 같은 자리다 — STEP4 반응면 계산이 그 몫을 빼는지 확인할 항목 [제안].
6. **구 DEM 이 낼 수 있는 대응 관측량**: 방향 · ovality 는 못 내지만 입자별 누적 회전각 · 이웃 교체 수 · 배위수 변화는 D0 덤프에서 낼 수 있다 — '큰 입자 · 넓은 분포일수록 재배열이 크다' 를 우리 침대에서 볼지는 결과 전에 정한다 [제안 · 실행 아님].

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- *"Spherical particles were used to study the mechanical responses and porosity variation of the electrode under different calendering steps. However, these studies were conducted based on simplified electrode geometries that were artificially synthesized with spherical particles, ignoring the influence of particle shape and orientation on mass transport and electrochemical performance."* [인쇄 · p.2747] — 구 입자 DEM 의 한계 (LIB 압연 문맥).
- *"Tortuosity, also called tortuosity factor, is a material parameter representing the mass transport resistance from the convoluted 3D morphology of the medium"* [인쇄 · SI p.2] + Q_p/Q_b = ε/τ (SI 식 3) — 이 논문의 τ 는 tortuosity factor.
- *"electrodes comprised of small particles (AM_S, Dmean = 5.2 ± 1.8 µm …) are structurally stable with homogeneous deformation and a lower pore tortuosity under calendering."* [인쇄 · p.2764] — LIB · 두 전극 · 기둥 압축 한정어와 함께.
- LIB NMC111 양극을 22.5 % · 24 % 누르면 기공상 tortuosity factor 가 2.58 → 8.79 · 2.32 → 7.56 [판독 · Fig 3I] (표 인쇄값 2.58 · 8.85) — 누른 채 · 3 상 · 기둥 압축.
- *"It is worth emphasizing the importance of including CBD in the tortuosity measurement otherwise the effect of microstructural heterogeneity is significantly weakened."* [인쇄 · p.2753].
- *"No volume-averaged material parameters, such as porosity, tortuosity, and particle size were used in the microstructure-resolved model."* [인쇄 · p.2766].

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **압력이 없다.** '압연' 을 다루는 논문인데 하중 · 응력 · 선하중이 하나도 인쇄돼 있지 않다 — 압축률 (두께 감소) 만 있다.  압밀 법칙 (Heckel 등) 과 이을 수 없다.
2. **옆 구속 없는 기둥 압축** 을 '압연의 모사' 로 쓴다.  근거는 Table S3 (서로 다른 압축률 22.5 ↔ 20 % · 시료 하나씩 · 누른 채 ↔ 뺀 뒤) 의 *"within 8%"* 하나.  Table 1 의 고체 보존은 12–15 % 안 닫힌다 [카드 산술].
3. **단계마다 시료 하나.** 재현 (n = 3) · RVE · 문턱 점검은 압축 전 AM_L 에만 있다.  압축 뒤에는 평균 기공이 4–5 복셀이다.
4. **'큰 ↔ 작은' 은 통제된 짝이 아니다** (공급사 · 분포 폭 · 형상 동반).  '균일 변형' 은 형상 · 방향 분포에서 읽은 것이지 변형률 측정이 아니다.
5. **CBD 안 기공은 다른 시료에서 왔다** (DSS).  전극 안 CBD 가 CBD 만의 막과 같게 눌린다는 가정이 값 (기공률 · τ · 반응 면적) 에 들어 있다 [카드 추론].
6. **모델 물성과 구조의 재료가 다르다**: OCV · D_s = NMC622 반쪽 셀 GITT · 구조 = NMC111 (AM_L · AM_S).  검증은 NMC622 전극 (AM_LH) 한 쌍뿐이고 5C 는 어긋난다.  격자 · 영역 · 수렴 정보가 없다.
7. **CBD 는 모델에서 전자만 나르는 균질 고체** — CBD 안 나노 기공의 이온 전도 · 그 안 표면의 반응은 없다 (식 12–13).  영상 분석 (tortuosity factor) 에서는 CBD 나노 기공이 기공상에 들어가는데 전기화학 모델의 기공 영역 정의가 같은지는 인쇄돼 있지 않다 [미확인].
8. **파쇄 · 균열은 인용과 추정** 이다 (§3-4).
9. **원문 안 불일치** (크롭에서 보인다): Fig 3I 의 AM_S 둘째 점 8.5 % ↔ Fig 1I '7%' · Table 1 AM 분율 0.46 ↔ Fig S13 43 % · p.2761 *"Doubling the thickness to 70 µm (AM_S2)"* ↔ Table 1 66 µm · *"by 150% (AM_S1.5)"* (1.5 배) · p.2762 *"the prediction in Figure 8"* (Fig 7) · Fig 5 캡션 'AM_H' · Fig S12 캡션 = S11 복사 · Table S1 깨진 상호참조 · p.2757 '3.75 V 위' ↔ 3.744 V [판독] · *"not markedly dependent on calendering"* ↔ GITT 0.68–0.87 배 [판독].
10. 이 카드의 [카드 산술] (고체 보존 · 구 근사 반응 면적 · 입자 수 역산 · 같은 기공률 τ 비) 은 원문에 없는 계산이다 — 인용할 때 표지를 뗄 수 없다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 19 | Sangrós Giménez, C., Finke, B., Schilde, C., Froböse, L., and Kwade, A. (2019). Numerical simulation of the behavior of lithium-ion battery electrodes during the calendaring process via the discrete element method. Powder Technol. 349, 1–11. | 이 논문이 '구 입자' 라고 비판한 DEM 압연 | 있음 `sangros2019_dem_calendering_lib_electrode` |
| 18 | Günther, T., Schreiner, D., Metkar, A., Meyer, C., Kwade, A., and Reinhart, G.J.E.T. (2020). Classification of calendering-induced electrode defects and their influence on subsequent processes of lithium-ion battery production. Energy Technol. 8, 1900026. | '재배열 → 변형 → 파쇄' 추측의 출처 (R7) | 없음 (wishlist 에 이미 있음) |
| 35 | Daemi, S.R., Lu, X., Sykes, D., Behnsen, J., Tan, C., Palacios-Padros, A., Cookson, J., Petrucco, E., Withers, P.J., Brett, D.J.L., et al. (2019). 4D visualisation of in situ nano-compression of Li-ion cathode materials to mimic early stage calendering. Mater. Horiz. 6, 612–617. | 같은 나노 압축 시험대의 선행판 — 하중 · 변위 기록이 거기 있는지 (이 논문에는 없다) | 없음 |
| 25 | Lu, X., Bertei, A., Finegan, D.P., Tan, C., Daemi, S.R., Weaving, J.S., O'Regan, K.B., Heenan, T.M.M., Hinds, G., Kendrick, E., et al. (2020). 3D microstructure design of lithium-ion battery electrodes assisted by X-ray nano-computed tomography and modelling. Nat. Commun. 11, 2079. | DSS 와 gPNP 모델의 원 논문 (*"as described elsewhere"*) — 격자 · 검증 세부 | 없음 |
| 26 | Daemi, S.R., Tan, C., Volkenandt, T., Cooper, S.J., Palacios-Padros, A., Cookson, J., Brett, D.J.L., and Shearing, P.R. (2018). Visualizing the carbon binder phase of battery electrodes in three dimensions. ACS Appl. Energy Mater. 1, 3702–3710. | CBD 만의 막 영상화 (DSS 의 한 축) — `zhang2023_pfib_multiscale_imaging_4d_thick_cathode` 가 같은 논문의 CBD 내부 미세공극 0.5 를 쓴다 [다른 카드 L175 · 원문 미확인] | 없음 |
| 27 | Usseglio-Viretta, F.L.E., Colclasure, A., Mistry, A.N., Claver, K.P.Y., Pouraghajan, F., Finegan, D.P., Heenan, T.M.M., Abraham, D., Mukherjee, P.P., Wheeler, D., et al. (2018). Resolving the discrepancy in tortuosity factor estimation for Li-ion battery electrodes through micro-macro modeling and experiment. J. Electrochem. Soc. 165, A3403–A3426. | 영상 τ ↔ 전기화학 τ 불일치 (제 3 상 포함 문제) | 없음 |
| 30 | Ebner, M., Chung, D.W., García, R.E., and Wood, V.J.A.E.M. (2014). Tortuosity anisotropy in lithium-ion battery electrodes. Adv. Energy Mater. 4, 1301278. | 입자 형상 · 방향 → tortuosity 이방성 | 없음 |
| 12 | Meyer, C., Kosfeld, M., Haselrieder, W., and Kwade, A. (2018). Process modeling of the electrode calendering of lithium-ion batteries regarding variation of cathode active materials and mass loadings. J. Energy Storage 18, 371–379. | 압연의 압력 축 (이 논문에 없는 것) | 없음 (후보 표 N-61 차례 대기) |
| 13 | Meyer, C., Bockholt, H., Haselrieder, W., and Kwade, A. (2017). Characterization of the calendering process for compaction of electrodes for lithium-ion batteries. Journal of Materials Processing Technology 249, 172–178. | 〃 | 없음 (후보 표 N-55 차례 대기) |
| 55 | Cooper, S.J., Bertei, A., Shearing, P.R., Kilner, J.A., and Brandon, N.P. (2016). TauFactor: an open-source application for calculating tortuosity factors from tomographic data. SoftwareX 5, 203–210. | 계산 도구 | 있음 `taufactor_tortuosity_factor_tomography_tool` |
| 28 | Landesfeind, J., Hattendorff, J., Ehrl, A., Wall, W.A., and Gasteiger, H.A. (2016). Tortuosity determination of battery electrodes and separators by impedance spectroscopy. J. Electrochem. Soc. 163, A1373–A1387. | tortuosity 의 전기화학 측정 | 있음 `landesfeind2016_tortuosity_eis_electrodes_separators` |
| 43 | Xu, R., Sun, H., de Vasconcelos, L.S., and Zhao, K. (2017). Mechanical and structural degradation of LiNixMnyCozO2 cathode in Li-ion batteries: an experimental study. J. Electrochem. Soc. 164, A3333–A3341. | '파쇄 뒤 고립 활물질' 인용 | 있음 `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` |
| 52 | Chen, C.-H., Brosa Planella, F., O'Regan, K., Gastol, D., Widanage, W.D., and Kendrick, E. (2020). Development of experimental techniques for parameterization of multi-scale lithium-ion battery models. J. Electrochem. Soc. 167, 080534. | GITT D_s 를 뽑은 방법 | 없음 (papers/ 파일 목록 · '080534' · 제목 grep 0 건) |
| SI 1 | Tjaden, B., Lane, J., Withers, P.J., Bradley, R.S., Brett, D.J., and Shearing, P.R. (2016). The application of 3D imaging techniques, simulation and diffusion experiments to explore transport properties in porous oxygen transport membrane support materials. Solid State Ionics 288, 315-321. | SI 의 tortuosity 정의 문단이 든 근거 | 없음 (같은 저자의 총설 = `tjaden2018_tortuosity_review_calculation_approaches`) |

## [미확인] 목록
- 가압 **하중 · 압력 · 변위 속도 · 단계 사이 유지 · 촬영 중 이완** · 압축률을 정한 방법 · 시험 온도 · 분위기.
- 압축률 (compression / calendering ratio) 의 정의 — 끝점이 두께 감소율과 맞을 뿐.
- tortuosity factor 의 **방향** · 경계 조건 · 계산 영역 · 실제 전극의 2 상 값.
- 비반응면적 · 평균 기공 크기 · 입경 (등가 지름) · ovality 의 계산 정의 · 붙은 입자의 분할 방법.
- DSS 에서 CBD 막의 압축 단계를 전극 단계에 맞춘 방법.
- 전기화학 모델의 격자 요소 수 · 영역 크기 · 시간 간격 · 수렴 · 계산 시간 · 맞춘 값의 유무 · 기공 영역에 CBD 나노 기공이 들어가는지.
- AM_LH 의 촬영 조건 (나노 CT 인지 · 탈압 뒤인지) · Fig 8 의 1 · 3 mAh cm⁻² 전극 재료 · 조성 · 압연 방법.
- 롤 압연 조건 (간격 · 선하중 · 온도 · 속도) · 반쪽 셀 시험 온도.
- 분말의 제조사 사양 (D50 · 1 차 입자 · 단결정 / 다결정 표기) — 원문은 조성과 공급사만 적는다.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 서지: PDF p.1 (그래픽 초록 쪽) · p.2 머리 · 쪽 아래 *"Joule 4, 2746–2768, December 16, 2020"* · DOI 10.1016/j.joule.2020.10.010 · SI p.1 저자 전원 — 후보 표 · 지시서의 서지와 **같다** (다른 점 없음).
- 본문 24 쪽 + SI 15 쪽 전부를 렌더로 읽고, 그림 · 표 · 식 · 근거 문단 92 장을 잘라 전부 열어 봤다 (도구 24 중 23 다시 자름 · 손 크롭 가운데 19 장은 눈으로 본 뒤 다시 자름).
- 표 1 · S2 · S3 · S4 · Fig S4 · S11 · S12 · S13 의 숫자는 렌더와 텍스트 층을 대조했다.  Table S4 의 표준편차는 표본 표준편차로 다시 계산해 일치를 확인했다.
- 판독: Fig 3I · 3J 는 두 벽면 교차 일치 (τ ≤ 0.014) + 인쇄 표 값 (2.58 · 8.85 · 0.325 · 0.188 · 0.421 · 0.306) 과 대조 · Fig S3 는 막대 합 ↔ 인쇄 노드 수 (3488 · 2773 · 1416 · 1242) · Fig S13 은 구간 평균 ↔ 인쇄 평균 (7.35 ↔ 7.3 · 5.26 ↔ 5.2) · Fig S8 은 본문 3.706 · 3.656 V 와 대조.
- 가리킨 카드: he2026 L691 (서지 같음 · 'operando' 는 원문에 없음) · lee2026_li L380 (서지 같음) — 두 카드 모두 숫자 인용 없음.

## 🔗 관련 카드
- [`sangros2019_dem_calendering_lib_electrode`](sangros2019_dem_calendering_lib_electrode.md) — 이 논문 ref 19 (구 입자 DEM 압연 · 이 논문이 한계를 지적한 대상).
- [`he2026_dem_calendering_inhomogeneity_areal_density`](he2026_dem_calendering_inhomogeneity_areal_density.md) · [`lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode`](lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode.md) — 이 논문을 인용한 카드 (후보 표 N-53 의 근거).
- [`taufactor_tortuosity_factor_tomography_tool`](taufactor_tortuosity_factor_tomography_tool.md) · [`tjaden2018_tortuosity_review_calculation_approaches`](tjaden2018_tortuosity_review_calculation_approaches.md) · [`nguyen2020_electrode_tortuosity_factor`](nguyen2020_electrode_tortuosity_factor.md) · [`landesfeind2016_tortuosity_eis_electrodes_separators`](landesfeind2016_tortuosity_eis_electrodes_separators.md) — tortuosity 정의 · 도구 · 측정.
- [`kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation`](kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md) · [`sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps`](sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps.md) · [`korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens`](korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens.md) — 황화물 계의 '누른 채 CT' (다이 안 · 압력 기록 있음).
- [`zhang2026_xct_dem_cathode_calendering_peel_calibration`](zhang2026_xct_dem_cathode_calendering_peel_calibration.md) · [`xu2023_realistic_am_shape_cgmd_calendering`](xu2023_realistic_am_shape_cgmd_calendering.md) · [`ngandjong2021_dem_calendering_digital_twin`](ngandjong2021_dem_calendering_digital_twin.md) · [`lim2025_virtual_calendering_framework`](lim2025_virtual_calendering_framework.md) — LIB 압연의 입자 계산 · 가상 압연 쪽.
- [`diener2022_roll_gap_springback_calendering`](diener2022_roll_gap_springback_calendering.md) · [`kollenda2024_time_sensitivity_calendered_electrode_springback_storage`](kollenda2024_time_sensitivity_calendered_electrode_springback_storage.md) — 이 논문에 없는 '뺀 뒤 · 되돌아옴' 축.

## 🗨️ Q&A 로그
- (비어 있음)
