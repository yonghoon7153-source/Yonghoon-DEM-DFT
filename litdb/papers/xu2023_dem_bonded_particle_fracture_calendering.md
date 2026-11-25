<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 본 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md · 같은 1 저자 · 같은 해 다른 논문 = xu2023_realistic_am_shape_cgmd_calendering.md
     (J. Power Sources 554 — 이 논문의 ref [44] = 2 차 입자 실형상 · 처음 (건조) 구조의 출처) · 계산 쪽 이웃 = ngandjong2021_dem_calendering_digital_twin.md (ref [41]) ·
     sangros2019_dem_calendering_lib_electrode.md (ref [27]) · he2026_dem_calendering_inhomogeneity_areal_density.md (이 논문을 백로그 N6 으로 가리킨 카드) ·
     song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage.md (명목 응력 파괴 판정) · tovar2026_cold_spray_cathode_composite_dem_plastic_elastic_bond.md (결합구 응집체 파단).
     쪽 표기 = 학술지 쪽 'e202300371 (n of 10)' 의 n (PDF 쪽 = 인쇄 쪽 p.1–10) · SI 쪽 = SI PDF 쪽 (SI p.1 = 표지 · SI p.2–7 = 내용).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv · 300 dpi 렌더에서 눈금 직선 맞춤 ·
     잔차 x ≤ 0.10 · y ≤ 0.19 축 단위 · 색 마스크의 무게중심 / 세로 단면 중앙값) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) ·
     [카드 추론] · [추정] = 이 카드의 해석 · [관찰] = 영상 · 그림을 보고 적은 것 · [미확인] = 본문 10 쪽 + SI 7 쪽 + 보충 영상 세 편 어디에도 없음.
     원문 17 쪽은 전부 렌더 이미지로 읽었고 숫자는 텍스트 층과 대조했다. -->
# NMC111 2 차 입자를 1.59 µm 1 차 구의 결합 입자 모델 (BPM · Potyondy–Cundall 결합 파단) 로 묶은 LIGGGHTS 캘린더링 DEM — 결합 강도 법선 0.1 · 접선 0.038 GPa · 전극 전체 끊긴 결합 1.8 · 4.5 · 11.1 % (50 · 100 · 150 MPa) · 고른 입자 하나에서 '끊긴 결합 ≈10 % ↔ 전극 압력 ≈120 MPa' 를 2 차 입자 균열 기준으로 추측 · 입자 E_p 5 GPa 를 최대 압력에 맞춤 · 나노 XCT (41 nm) 로 150 MPa 균열 관찰 · 되돌아옴 31–38 % · 액체 LIB (SE 없음) — Xu · Paredes-Goyes · Su · Scheel · Weitkamp · Demortière · Franco (Batteries & Supercaps 2023)

> slug `xu2023_dem_bonded_particle_fracture_calendering` · DOI `10.1002/batt.202300371` · type `DEM (LIGGGHTS 수정판 · 결합 입자 모델 BPM · 헤르츠 + SJKR 점착) + 실험 (나노 XCT 41 nm · 마이크로 XCT · 롤 압연) — 액체 LIB NMC111/CBD 양극 · 2 차 입자 결합 파단 · 압축 + 이완 · SE 없음 · 수송 계산 없음` · PDF `d8b9e078-70._Computational_model_for_predicting_particle_fracture_during_electrode_calendering.pdf` · digested `2026-11-16` · status ✅
>
> **저자**: **Jiahui Xu** · Brayan Paredes-Goyes · Zeliang Su · Mario Scheel · Timm Weitkamp · Arnaud Demortière · **Alejandro A. Franco\*** (교신 · alejandro.franco@u-picardie.fr) — LRCS (UMR CNRS 7314 · Université de Picardie Jules Verne · Amiens) · RS2E (FR CNRS 3459) · ALISTORE-ERI (FR CNRS 3104) · Synchrotron SOLEIL (Scheel · Weitkamp) · Institut Universitaire de France (Franco) · *Batteries & Supercaps* **2023, 6, e202300371** (본문 10 쪽 · SI 7 쪽 · 보충 영상 3 편) · 'Very Important Paper' · 12/2023 호 표지 (Cover Feature) · 접수 2023-08-31 · 수정 09-14 · 승인 원고 온라인 09-15 · 확정판 10-25 · CC BY · 연구비 ERC ARTISTIC (772873) · ERC PoC SMARTISTIC (101069244) · IUF · EQUIPEX ANATOMIX (ANR-11-EQPX-0031) · SOLEIL 과제 20201695 · 마이크로 CT 자료 수집 도움 MATEIS (INSA Lyon) · 계산 MatriCS (p.8–10) · 자료 = 교신 저자에게 요청 (p.9).
> **이웃 카드 (링크만)**: [`xu2023_realistic_am_shape_cgmd_calendering`](xu2023_realistic_am_shape_cgmd_calendering.md) (같은 1 저자 · 같은 해 · 다른 논문 = 이 논문 ref [44]) · [`ngandjong2021_dem_calendering_digital_twin`](ngandjong2021_dem_calendering_digital_twin.md) (ref [41]) · [`sangros2019_dem_calendering_lib_electrode`](sangros2019_dem_calendering_lib_electrode.md) (ref [27]) · [`lu2020_insitu_nanoct_calendering_microstructural_evolution`](lu2020_insitu_nanoct_calendering_microstructural_evolution.md) (ref [11]) · [`diener2022_roll_gap_springback_calendering`](diener2022_roll_gap_springback_calendering.md) (ref [58]) · [`he2026_dem_calendering_inhomogeneity_areal_density`](he2026_dem_calendering_inhomogeneity_areal_density.md) (이 논문을 가리킨 카드 · L499 · L690) · [`song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage`](song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage.md) · [`tovar2026_cold_spray_cathode_composite_dem_plastic_elastic_bond`](tovar2026_cold_spray_cathode_composite_dem_plastic_elastic_bond.md) · [`wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem`](wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem.md) · [`clemmer2024_bpm_elastic_grain_compaction_beyond_jamming`](clemmer2024_bpm_elastic_grain_compaction_beyond_jamming.md).
> **판독 원자료**: `litdb/figures/xu2023_dem_bonded_particle_fracture_calendering/digitized.csv` (112 행 — 그림 4a · 4b · 5b · S2f · S3 · S4b · S5 · S6b · S7b · S8) · 크롭 61 장 (그림 13 · 표 4 · 패널 8 · 식 9 · 근거 문단 20 · 영상 정지 화면 6 · 표지 1) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 마이크로 XCT (PETRA III P05 · 화소 0.64 µm) 로 뜬 실형상 NMC111 2 차 입자를 **지름 1.59 µm 1 차 구의 응집체**로 만들고, 같은 2 차 입자 안에서 처음 맞닿은 1 차 구 쌍마다 **원기둥 결합 (BPM)** 을 걸어 결합 응력이 강도 (법선 0.1 · 접선 0.038 GPa [인쇄 SI 표 3]) 를 넘으면 끊기게 한 LIGGGHTS 캘린더링 DEM 으로, 위판을 0.01 m/s 로 최대 40 % 까지 눌렀다가 같은 속도로 되돌리며 (**누른 채 → 뺀 뒤**) 끊긴 결합 몫을 센다 — 전극 전체는 50 · 100 · 150 MPa 에서 **1.8 · 4.5 · 11.1 %** [인쇄 p.7] 가 끊기고, 고른 큰 입자 하나 (11.96 µm · 1 차 입자 426 · 결합 1748) 가 120 MPa 를 넘어서야 뚜렷이 끊기는 것 (40 % 뒤 17 %) 과 나노 XCT 의 '150 MPa 균열 · 80 MPa 온전' 을 엮어 '끊긴 결합 ≈10 % ≈ 120 MPa 이면 2 차 입자가 깨진다' (요지) 고 **추측** (*"we can speculate"* p.8) 한다 — 입자 E_p 5 GPa 는 최대 압력에 맞췄고, 결합 강도는 보정하지 않았으며 (매개변수 연구만), 수송 (σ) 계산은 없다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 조건 R7 — 압밀 계산 **안에서** AM 이 깨지나 | **예 (결합 파단 = 입자 안 연결 소실)**: 깨짐이 계산 중에 일어나 역학에 되먹임 (입자가 *"slight deformation"*) · 우리 Auerbach (접촉별 사후 분류) 와 다르다.  단 저자 스스로 *"Since the nano-fracture we observe is smaller than the scale of our model, we are not able to observe the fracture of the secondary particle from the simulation results"* — 균열 자체가 아니라 **결합 끊김 몫**이 대리량 | [인쇄] p.4 · p.7 |
| ② '>120 MPa → 결합 파단 >10 %' (he2026 L690) 의 원문 정의 | **고른 입자 하나**에 대한 **추측 기준**: *"secondary particle cracking occurs when the number of broken bonds is approximately above 10%, i.e., when the applied pressure is approximately above 120 MPa"* (p.8).  이 입자는 90 % 선을 ≈34.6 % 압축 · **≈122 MPa** 에서 넘는다 [판독 · 보간].  **전극 전체**는 4.5 % (100 MPa) · 11.1 % (150 MPa) [인쇄] → 10 % 를 ≈38.2 % · **≈144 MPa** 에서 넘는다 [판독 · 보간] | [인쇄] p.7–8 · [판독] 그림 4b · 5b |
| ③ 결합 모델 | 법선 / 접선 힘 증분 ΔF = (E_b A_b/l_b) v_r Δt · ((E_b/2(1+Po_b)) A_b/l_b) v_r Δt (식 4–5) · 보 이론 최대 응력 (식 6–7) · σ_B^n ≥ σ_B^cn **또는** σ_B^t ≥ σ_B^ct 이면 끊김 · 결합 감쇠 없음 · 다시 붙지 않음 (처음 접촉 쌍에만 생성) | [인쇄] p.4–5 · SI 표 3 |
| ④ 맞춘 값과 맞춘 대상 | **E_p · Po_p 를 압연 최대 압력에 맞춤** (*"straightforwardly calibrated by fitting the maximum pressure"*) → NMC E **5 GPa** · ν 0.3 [인쇄 SI 표 1] · 결합 강도 = *"should be found by calibration"* 인데 **매개변수 연구 하나 (그림 S3) 만** | [인쇄] p.4 · SI p.3 |
| ⑤ 1 차 입자 수 · 2 차 입자 형상 출처 | 고른 입자 426 개 (결합 1748 · 1 차 입자당 결합 수 2 × 1748 / 426 = 8.21 [카드 산술]) · 전극 전체 1 차 입자 수 [미확인] · 전체 결합 ≈38,470 [판독 그림 S8] · 형상 = **마이크로** XCT (0.64 µm · ref [44]) — 나노 XCT (41 nm) 는 균열 관찰에만 | [인쇄] p.4 · p.7 · [판독] |
| ⑥ 압력–기공률 검증 | 실험 표 1 (뺀 뒤): 0 · 80 · 150 MPa → 47.97 · 27.75 · 25.17 % [인쇄] · 모의 (뺀 뒤 · 이론 물질 부피): 0 · 12.4 · 40 · 80 · 120 · 157.6 MPa → 50.0 · 44.4 · 42.3 · 38.1 · 32.7 · 29.2 % [판독] — **80 MPa 에서 +9.5 %p** · 157.7 MPa 런 29.12 % ↔ 실험 25.16 % (*"slightly higher"*) | [인쇄] 표 1 · p.7 · [판독] 그림 4a |
| ⑦ 하중을 뺀 뒤 | **있다** — 위판을 같은 속도로 처음 자리까지 되돌림 · 되돌아옴 정도 h₂/h₁ = 31.2 · 37.7 · 36.3 · 33.0 · 32.6 % (12.5 · 40 · 80 · 120 · 157.7 MPa) [판독 그림 S4b] · 40 % 런은 압축도 ≈26–27 % 에서 판 하중이 0 [판독 그림 4b] · 이완 중 끊긴 결합 = 전체 끊김의 3 % [인쇄 p.7] | [인쇄] p.5–7 · [판독] |
| ⑧ DEM 한계 (원문 문장) | *"This may be due to the inability of the simulation to capture the plastic behavior exhibited by the electrode during this process since we use an elastic contact model."* (p.7) · 1 차 입자 1.59 µm 구 = 조대화 (*"the real primary particle crystal shape is not spherical and the size is smaller"* p.5) · 1 차 입자 겹침이 기공률 오차 (p.5–6) · 1 차 입자 사이 SJKR 이 있어야 응집체가 안정 (p.4) · *"These observations are qualitative"* (p.8) | [인쇄] |
| ⑨ 계산 비용 · 차원 | **3D** · 런당 **2–9 일 × 28 코어** (Xeon E5-2680 v4 · 1 노드 · 128 GB) · Δt 0.01 ns · 위판 0.01 m/s · 판 면적 910 µm² · 상자 높이 · 입자 수 [미확인] | [인쇄] p.5 · p.6 |
| ⑩ 수송 (σ) | **없다** — *"In the future, the microstructures obtained from the model will be used in a finite element method simulator"* (p.8) | [인쇄] |

⛔ **한정어 (떼지 말 것)**: ① 재료 = **액체 LIB NMC111 : C65 : PVdF = 96 : 2 : 2** — **SE 가 없다** (AM 이 하중을 전부 진다 = 우리 f_AM ≡ 1 극한) ② 공정 = **롤 압연** (실험) ↔ **평판** (모의) · 실험 압력은 롤 간격 · 두께에서 공식으로 **계산한** 값 (p.2–3) ③ 압력 ≤ 157.7 MPa (우리 300 MPa 의 ≈½) ④ '120 MPa · 10 %' = **추측** · 입자 하나 · 결합 강도 미보정 ⑤ 입자 E_p 5 GPa = **맞춘 값** (같은 그룹 앞 논문 135 GPa · Ngandjong 200 GPa 의 1/27–1/40) — 물성 아님 ⑥ 모의 기공률 · 압축도 · 되돌아옴 정도가 고체 부피 보존 하나로 서로 맞지 않는다 (§3-9 [카드 산술]) ⑦ 실험 기공률은 압연 뒤 (하중 뺀 뒤) · 모의 기공률도 이완 뒤 (157.7 MPa 런만 최대 압력 값 26.72 % 도 인쇄).
⇒ **절대값 전이**: 압력 · 기공률 · 끊긴 결합 몫 · 되돌아옴 정도의 절대값은 **LPSCl/NCM 복합 양극 (300 MPa 냉간 성형) 에 옮기지 않는다** (재료 · 공정 · 상 구성 · 맞춘 E 가 다 다르다).  옮길 수 있는 것은 **방법** — 결합 입자 응집체로 AM 파괴를 압밀 중에 계산하는 꼴 · 위치별 (집전체 쪽 / 가운데 / 윗면) 집계 · 두 기공 연산자 병기 · 압축 → 같은 속도 되돌림 프로토콜 · 그리고 '파괴 기준을 입자 하나 + 정성 영상으로 추측' 하는 함정.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-70 의 '왜' 칸)

의도 원문: *"조건 R7 — "bonded-particle 입자파괴 모델 (>120 MPa → bond 파단 >10 %) · 우리 Auerbach / f_intact 의 문헌 대응물 · ⚠ litdb 의 xu2023_realistic_am_shape_cgmd_calendering (JPS 554) 와 다른 논문""* (근거 = he2026 L690 · 서지 메모 "Xu 2023 (Batteries & Supercaps 6, e202300525)").

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "bonded-particle 입자파괴 모델" | **채움** | BPM (ref [51] Potyondy–Cundall) — 같은 2 차 입자 안에서 *"in contact in the initial microstructure"* 인 1 차 구 쌍에 원기둥 결합 · 식 (4)–(7) · 파단 = σ_B^n ≥ σ_B^cn 또는 σ_B^t ≥ σ_B^ct [인쇄 p.4–5] · LIGGGHTS 수정판 [56] · 3D · 모의 |
| ">120 MPa" | **일부 (정의 다름)** | 120 MPa = **위판 (전극) 압력** — 고른 입자 하나 (등가 지름 11.96 µm · 아래-가운데) 가 *"noticeable bond breakage only when the electrode is subjected to a calendering pressure of the electrode exceeding 120 MPa"* (p.7) · 누른 채 (압축 중) · 이 입자의 90 % 선 통과 ≈122 MPa [판독 · 보간] · 전극 전체는 ≈144 MPa 에서 10 % [판독 · 보간] · 집전체 쪽 입자는 10 MPa 아래부터 끊김 (p.8 · 그림 S6) |
| "bond 파단 >10 %" | **일부 (추측 기준 · 입자 단위)** | *"we can speculate that in the model, secondary particle cracking occurs when the number of broken bonds is approximately above 10%, i.e., when the applied pressure is approximately above 120 MPa"* (p.8) — 근거 = 나노 XCT 150 MPa 균열 (그림 1b · 정성) + 그림 5d 입자 하나.  **보정 · 통계 없음** (결합 강도는 매개변수 연구만) · 10 % 는 **2 차 입자 하나의 결합 중 끊긴 몫** (전극 전체 몫 아님) · 전극 전체 몫은 1.8 · 4.5 · 11.1 % @ 50 · 100 · 150 MPa [인쇄 p.7] |
| "→" (압력이 원인 · 몫이 결과의 규칙) | **없음 (그런 규칙으로 적히지 않음)** | 원문은 '10 % 이면 깨졌다고 본다' (기준) + '그때 압력이 ≈120 MPa' (이 입자) 의 두 단계 — 압력 문턱 규칙이 아니다.  *"the number of bond breaks is not linearly related to the reduction of the thickness due to the uneven force inside the electrode"* (p.8) · 위치에 따라 같은 압력에서 끊김 몫이 9 % (윗면) ↔ 46 % (집전체 쪽) [판독 그림 S7b · S6b, 40 % 압축] |
| "우리 Auerbach / f_intact 의 문헌 대응물" | **일부** | 같은 자리 (압밀 DEM 안의 AM 파괴) 를 다른 양으로: 이 논문 = 2 차 입자 **안** 결합의 끊긴 몫 (계산 중 · 역학 되먹임 있음 · 수송 없음) ↔ 우리 Auerbach = 접촉별 힘 ÷ P_c 의 **사후** 분류 · f_intact = 파괴로 뺀 접촉을 제외한 몫이 σ 폼에 들어감 (CLAUDE.md σ_ionic T1 · σ_e Stage 22.5).  이 논문에 **f_intact 대응 (파괴 → 전도) 은 없다** (FEM 은 '미래') |
| "⚠ xu2023_realistic (JPS 554) 와 다른 논문" | **채움** | 이 논문 = Batteries & Supercaps 6, e202300371 · JPS 554, 232294 는 이 논문의 **ref [44]** = 실형상 2 차 입자 · 슬러리 · 건조 구조의 출처 (p.2 · p.4) |
| he2026 L690 의 서지 "*Batteries & Supercaps* 6, e202300525" | **다름 → 카드 문제** | 원문 첫 쪽 · 모든 쪽 머리글 · PDF 메타 = **e202300371** · DOI 10.1002/batt.202300371.  he2026 카드에 참고문헌 목록이 없어 오기가 he2026 원문의 것인지 카드의 것인지 [미확인] |
| he2026 L499 "(bonded-particle, >120 MPa 에서 bond 파단 >10 %)" | **일부 (값은 같고 정의가 빠짐)** | 숫자 120 · 10 은 원문과 같다 · '추측 · 입자 하나 · 입자 단위 몫' 이 빠졌다 → 카드 문제 (고치지 않음) |
| (지시서) "2 차 입자 형상의 출처 (나노 단층 촬영)" | **다름** | 형상 = **마이크로 XCT** (*"extracted from the micro-scale XCT … P05 beamline of the PETRA III … pixel size of 0.64 μm"* p.4) · 나노 XCT (SOLEIL ANATOMIX TXM · 복셀 41 nm) 는 압연 전 · 80 · 150 MPa 전극의 **균열 관찰**에만 (p.3 · 그림 1 · S1) |
| 가리킨 카드의 **2 차 인용 값** | **같음 (숫자) · 정의 일부** | he2026 의 120 MPa · 10 % 는 원문 숫자와 같다 · 원문 번호 · 정의가 다르다 (위 두 줄) · `wet_processing_resolved_am_ssb_cathode_manufacturing` L45 · L239 의 "ref [38] Xu, Paredes-Goyes 2023 (Batteries & Supercaps) = 압연 중 입자 fracture 예측 모델 (LIB)" = 원문과 같다 (숫자 없음) |

⇒ **의도 대조 결과: 일부** — 결합 입자 파괴 모델은 **있다 (채움)**; '120 MPa · 10 %' 는 숫자는 있으나 **고른 입자 하나의 추측 기준**이고 전극 전체로는 ≈144 MPa 에서 10 % [판독]; Auerbach 대응은 **같은 자리 · 다른 양** (사후 분류 ↔ 계산 중 결합 파단) 이고 f_intact (파괴 → 전도) 대응은 **없다**.

### 0-2. ★ 결합 모델 · 맞춤 · 검증 · 비용 한 표 (지시서 요청)

| 항목 | 원문 값 · 정의 | 표지 · 쪽 |
|---|---|---|
| 결합이 생기는 쌍 | 같은 2 차 입자의 1 차 구 가운데 **처음 구조에서 맞닿은** 쌍 · 끊기면 다시 안 생김 [카드 추론 — 재생성 문장 없음] | [인쇄] p.5 |
| 결합 기하 | *"assumed cylindrical bond"* · 단면 A_b · 길이 l_b · 관성 I · 극관성 J · R_min = 두 입자 중 작은 반지름 — **A_b (결합 반지름 배수) · l_b 값 [미확인]** | [인쇄] p.4 |
| 법선 강성 | ΔF_B^n = (E_b A_b / l_b) v_r^n Δt (식 4) · **E_b = 10 GPa** [인쇄 SI 표 3] ↔ 본문 *"these two bond properties are set to the same value as the particle parameters"* (입자 E_p 5 GPa) — **어긋남** | [인쇄] p.4 · SI p.3 |
| 접선 강성 | ΔF_B^t = ((E_b/2(1+Po_b)) A_b / l_b) v_r^t Δt (식 5) · 표 S3 *"Elastic modulus"* 3.84 GPa = 10/(2 × 1.3) = 3.846 GPa = 전단 탄성률 [카드 산술 · Po_b = 0.3 가정 = 입자 ν] | [인쇄] · [카드 산술] |
| 모멘트 | 축 · 전단 모멘트 증분 ΔM_B^n · ΔM_B^t 는 *"Similar expressions can be found in Ref. [52]"* — **식 인쇄 없음** | [인쇄] p.4 |
| 최대 응력 | σ_B^n = −\|F_B^n\|/A_b + \|M_B^t\| R_min / I (식 6) · σ_B^t = \|F_B^t\|/A_b + \|M_B^n\| R_min / J (식 7) | [인쇄] p.4 |
| 강도 · 파단 기준 | **σ_B^cn 0.1 GPa · σ_B^ct 0.038 GPa** [인쇄 SI 표 3] · 끊김 = σ_B^n ≥ σ_B^cn **또는** σ_B^t ≥ σ_B^ct · 본문 *"For normal and shear breakage to be possible, σ_B^cn = σ_B^ct"* ↔ 표 S3 은 두 값이 다르다 (비 0.38 = G/E 0.3846 [카드 산술]) — **어긋남** | [인쇄] p.4 · SI p.3 |
| 결합 감쇠 | *"we do not consider damping for the bonds"* | [인쇄] p.5 |
| 결합 밖 1 차 입자 사이 | SJKR 점착 (식 3) 도 같이 — *"required to ensure the stability of the secondary particle. This limitation will be further investigated"* | [인쇄] p.4 |
| 맞춘 값 · 대상 | **E_p · Po_p ← 압연 최대 압력** (표 1 의 압력–기공률 곡선으로 *"parameterization"*) · 결과 NMC E 5 GPa · ν 0.3 · CBD 2 GPa · 0.45 · Al 69 · 스테인리스 (롤) 200 GPa [인쇄 SI 표 1] · 결합 강도 = 보정 안 함 (매개변수 연구 그림 S3: 'Sigma value' 0.1–1.0 ×10⁶ · 단위 인쇄 없음 · 시험 조건 인쇄 없음) | [인쇄] p.4–5 · SI p.3 |
| 1 차 입자 | 지름 **1.59 µm** 구 (*"coarse-grained"* · 실제 1 차 입자는 더 작고 비구형) · 고른 입자 426 개 = 11.96 µm (1.59 × 426^⅓ = 11.96 µm [카드 산술] — 등가 지름 = 1 차 구 부피 합의 구 지름) · 전체 수 [미확인] | [인쇄] p.5 · p.7 |
| CBD | 지름 **1.16 µm** 구 · 나노 기공 **27 %** ([57] 과 비슷) | [인쇄] p.4 · p.5 |
| 형상 출처 | **마이크로 XCT** (PETRA III P05 · 화소 0.64 µm) + 실험 PSD — ref [44] (= `xu2023_realistic_…` 카드: 1 차 구 = 0.642 µm 복셀 2×2×2 묶음의 등부피 구 1.59 µm) | [인쇄] p.4 |
| 처음 구조 | ref [44] 의 **건조 모의 결과** (LAMMPS · CGMD) | [인쇄] p.4 |
| 경계 · 하중 | 위판 = 롤 · 아래판 = 집전체 · 판에 평행한 방향 주기 경계 · 중력만 · 위판 0.01 m/s (실험 라인 속도 0.009 m/s · 압력에 영향 *"negligible"* 확인) · 판 면적 **910 µm²** (정사각이면 한 변 30.17 µm [카드 산술]) | [인쇄] p.4–6 |
| 압력 정의 | 위판 접촉력 ÷ 910 µm² | [인쇄] p.6 |
| 프로토콜 | 정해진 변위까지 압축 (최대 압력 기록) → **같은 속도로 처음 자리까지 되돌림** (이완) → 이완 뒤 기공률 | [인쇄] p.5 |
| 압력–기공률 검증 | 그림 4a — 실험 4 점 · 모의 6 점 × 두 연산자 (§3-6) | [인쇄] · [판독] |
| 실험 균열 대조 | 나노 XCT — 압연 전 · 80 MPa 온전 · 150 MPa 뚜렷한 균열 (정성 · 정량 없음) | [인쇄] p.3 |
| 시간 간격 · 비용 | Δt **0.01 ns** (*"around 1.5% of Rayleigh time"*) · 런당 **2–9 일** · 28 코어 1 노드 · 128 GB | [인쇄] p.5 |

---

## 1. 한 줄 요약
같은 그룹이 앞 논문 [44] 에서 만든 '실형상 2 차 입자 = 1 차 구 응집체' 건조 전극을 LIGGGHTS 로 옮겨, 1 차 구 사이에 **끊어질 수 있는 결합 (BPM)** 을 넣고 평판으로 0–157.7 MPa 를 눌렀다 뺀다 — 결합은 압력에 비선형으로 끊겨 (50 · 100 · 150 MPa 에서 1.8 · 4.5 · 11.1 %) 집전체 쪽 · 큰 입자 · 곡률 큰 곳에 몰리고, 이완 중에는 거의 안 끊긴다 (전체의 3 %).  나노 XCT 가 150 MPa 에서만 균열을 보였으므로 '끊긴 결합 ≈10 % (≈120 MPa) = 2 차 입자 균열' (요지) 을 추측 기준으로 제안한다.  모의 기공률은 실험보다 높고 (80 MPa 에서 +9.5 %p [판독]) 저자는 그 원인을 **탄성 접촉 모델이 소성을 못 잡기 때문**으로 적는다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| J. Xu · B. Paredes-Goyes · Z. Su · M. Scheel · T. Weitkamp · A. Demortière · A. A. Franco\* (LRCS · RS2E · ALISTORE · SOLEIL · IUF) | Batteries & Supercaps 6 (2023) e202300371 · 10 쪽 + SI 7 쪽 + 영상 3 | 10.1002/batt.202300371 | **CAM 만 (액체 LIB)** — NMC111 (Umicore) : C65 : PVdF 5130 = 96 : 2 : 2 · Al 22.5 µm 집전체 · **SE 없음** | 실험 (나노 XCT 41 nm · 마이크로 XCT · 롤 압연 전극) + **3D DEM** (LIGGGHTS + BPM · 헤르츠 + SJKR) — 수송 · FEM · MPM 없음 |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 실험 전극 · 압연 · 측정 (p.2–3)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 조성 · 혼합 | NMC111 (Umicore) · C65 (C-NERGY™ super C65) · PVdF (Solef™ 5130/1001, Solvay) **96 : 2 : 2 (무게)** 하룻밤 예비 혼합 → NMP 로 고형분 맞춤 → Dispermat CV3-PLUS 고전단 **2 h · 25 °C** | [인쇄] p.2 |
| 도포 · 건조 | 콤마 코터 PDL250 (People & Technology) · **Al 22.5 µm** · 오븐 85 °C · 95 °C | [인쇄] p.2 |
| 압연 | 시제품 랩 프레스 캘린더 BPN250 · 여러 롤 간격 · 라인 속도 **0.54 m/min** (= 0.009 m/s [카드 산술]) · **60 °C** | [인쇄] p.2 |
| 압력 산정 | *"obtained from a calculation by using the roll gaps and the thickness of the electrode, which was calibrated by measuring the applied force of the corresponding roll gap through the utilization of a force sensor film (ELF … FlexiForce sensors, Tekscan)"* [7] — 사내 공식 (간격 + 압연 전 두께 → 압력) · 공식 자체 [미확인] | [인쇄] p.2–3 |
| 롤 간격 → 압력 | — → 0 · **21 µm → 80 MPa** · **6 µm → 150 MPa** (*"these gaps refer to the gap between two rolls before calendering"* · 압연 중에는 간격이 늘어난다) | [인쇄] p.3 · 표 1 |
| 압연 전 두께 | 본문 *"The electrode of a thickness of 114 μm"* ↔ 표 1 **99.03 ± 0.87 µm** — 어긋남 (§3-2) | [인쇄] p.3 |
| 나노 XCT | SOLEIL **ANATOMIX** · TXM 흡수 모드 · 단색 **8.327 keV** · 180° 에 투영 500 장 (500 ms) 또는 360° 에 1000 장 (500 ms · offset 15 µm) · PyHST2 재구성 · 평활 필터 · 화소 = 복셀 **41 nm** · 비국소 평균 + 언샤프 마스크 · Trainable Weka (랜덤 포레스트 · FIJI) 3 상 분할 (AM · 매크로 기공 · 나노 균열) · Avizo 9.4 시각화 | [인쇄] p.3 |
| 나노 XCT 시료 | 전극 가운데에서 잘라 에폭시로 금속 바늘에 붙이고 레이저 마이크로 절삭기로 시야 크기에 맞춤 | [인쇄] p.2 |
| 마이크로 XCT (그림 S2) | 전극 0 · 100 · 120 · 150 MPa · 두 상 분할 (매크로 기공 · AM) · 장치 · 복셀 · tortuosity 계산법 **[미확인]** (감사의 글: 마이크로 CT 자료 수집 = MATEIS · INSA Lyon) | [인쇄] SI p.2 · p.9 |

### 3-2. ★ 표 1 — 질량 · 두께 · 기공률 (압연 뒤 · 하중 뺀 뒤) 과 정합 산술
| 롤 간격 (µm) | 압력 (MPa) | 질량 (mg) | 두께 (µm) | 기공률 (%) |
|---|---|---|---|---|
| – | 0 | 22.37 ± 0.29 | 99.03 ± 0.87 | 47.97 ± 0.87 |
| 21 | 80 | 22.97 ± 0.11 | 79.67 ± 0.06 | 27.75 ± 0.23 |
| 6 | 150 | 22.30 ± 0.68 | 75.4 ± 0.79 | 25.17 ± 1.2 |
- 전부 [인쇄] p.3 · 기공률 계산식 · 시료 면적 · 진밀도 (상별 · 혼합) · 측정 압력 (두께를 잴 때) **[미확인]**.
- **정합 산술** [카드 산술]: 같은 면적 A · 같은 고체 밀도 ρ_s 라면 m / (t (1 − ε)) = A ρ_s 가 세 줄에서 같아야 한다.  인쇄 두께로는 0.434 · 0.399 · 0.395 mg/µm (**9.8 % 어긋남**) · 두께에서 **Al 22.5 µm 를 빼면** 0.562 · 0.556 · 0.563 (**1.3 % 안**) ⇒ 표 1 의 두께는 **집전체를 포함한 값**으로 읽어야 세 열이 맞는다 [카드 추론] — 그렇게 읽으면 코팅 두께 76.5 → 57.2 (−25.3 %) → 52.9 µm (−30.9 %) [카드 산술].  인쇄 두께 그대로의 감소는 −19.5 % · −23.9 % [카드 산술].
- 본문 p.7 은 150 MPa 실험 기공률을 **25.16 %** 로 적는다 (표 1 은 25.17).

### 3-3. ★ 실험 관찰 — 나노 XCT · 마이크로 XCT (그림 1 · S1 · S2)
- **원문 (정성)**: 압연 전 = 합성 때 생긴 기공만 · *"the particle structure is intact without cracks"* · 80 MPa = *"the particles remained relatively intact"* (그림 S1) · 150 MPa = *"the particles showed obvious cracks"* (p.3) · *"The cracks are not evenly distributed or exist in every secondary particle. However, due to the small size of our electrode volume, the cracks could not be accurately quantified."* (p.3–4).
- [관찰] 그림 S1 (80 MPa) 의 두 큰 입자 안에도 갈라진 틈이 보인다 — 합성 기공인지 압연 균열인지 원문은 가르지 않는다.
- **마이크로 XCT (그림 S2f · [판독])**: 기공률 0 · 100 · 120 · 150 MPa → **51.1 · 26.2 · 23.5 · 21.4 %** · tortuosity factor **1.53 · 4.00 · 5.84 · 7.82** (계산법 · 방향 · 정의 [미확인] — 우리 규약으로 'tortuosity factor' = tau2 꼴인지 원문은 정의하지 않는다).
- ⚠ 같은 150 MPa 에서 표 1 (질량 · 두께) 25.17 % ↔ 마이크로 XCT 21.4 % [판독] — 측정법 · 해상도 (CBD 를 어느 상에 넣었는지 [미확인]) 가 다르다.  100 · 120 MPa 전극은 표 1 에 없다.

### 3-4. 모델 매개변수 (SI 표 1–3 · 본문)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| E (GPa) | NMC **5** · CBD **2** · Al 69 · 스테인리스 200 | [인쇄] SI 표 1 |
| ν | NMC 0.3 · CBD 0.45 · Al 0.3 · 스테인리스 0.3 | [인쇄] SI 표 1 |
| SJKR 점착 에너지 밀도 (단위 인쇄 없음) | NMC–NMC 5e5 · NMC–CBD 2e5 · NMC–Al 0 · NMC–스테인리스 5e5 · CBD–CBD 1e5 · CBD–Al 0 · CBD–스테인리스 3e5 · Al–스테인리스 0 | [인쇄] SI 표 2 |
| 결합 | E 10 GPa · 'Elastic modulus' 3.84 GPa · σ_B^n 0.1 GPa · σ_B^t 0.038 GPa | [인쇄] SI 표 3 |
| 반발 계수 e_p · 마찰 μ_t · 밀도 · 결합 반지름 · 구름 마찰 | **[미확인]** (본문은 e_p 를 강성 · 감쇠의 입력으로 이름만 적는다) | — |
| 1 차 구 · CBD 구 | 1.59 µm · 1.16 µm (나노 기공 27 %) | [인쇄] p.5 · p.4 |
| Δt · 판 속도 | 0.01 ns (*"around 1.5% of Rayleigh time"*) · 0.01 m/s | [인쇄] p.5 |
- **같은 그룹 앞 논문과의 차이** [카드 산술 · 이웃 카드 값]: NMC E = 5 GPa ↔ `xu2023_realistic` (LAMMPS JKR) **135 GPa** · `ngandjong2021` **200 GPa** → **1/27 · 1/40** (나노압입 NMC532 142.5 GPa (`xu2017_…` 카드) 의 1/28.5) · CBD 지름 1.16 ↔ 1.3 µm · CBD 나노 기공 27 % ↔ 47–50 %.
- **Δt 대조** [카드 산술 · 가정 ρ_NMC = 4.65 g/cm³ (`ngandjong2021` 카드의 CGMD 입력표 값 — 이 논문에는 밀도가 없다)]: T_R = πR√(ρ/G)/(0.1631ν + 0.8766) · G = E/(2(1+ν)) · R 0.795 µm · E 5 GPa · ν 0.3 → **T_R ≈ 4.2 ns → Δt/T_R ≈ 0.24 %** (결합 E 10 GPa 로 하면 0.34 %) — 원문 *"around 1.5%"* 와 **≈6 배** 다르다 · 1.5 % 가 되려면 ρ ≈ 0.12 g/cm³ — 질량 배율 · 다른 반지름을 썼는지 [미확인].
- Δt × 판 속도 = 판이 한 단계에 10⁻⁴ nm · 1 µm 내려가는 데 **10⁷ 단계** [카드 산술] — 상자 높이 [미확인] 이라 총 단계 수는 셀 수 없다.

### 3-5. ★ 압력 ↔ 압축도 — 세 벌의 인쇄 · 판독 값 (같은 40 % 런)
| 압축도 | 본문 p.5 (*"14.2 … 157.7 MPa … 10%, 20%, 30%, and 40%"*) | 그림 3 캡션 (b–e) | 그림 4b 압축 곡선 [판독] | 그림 5b · S6b · S7b 스냅숏 [판독] |
|---|---|---|---|---|
| 10 % | **14.2** | 9.2 | 13.9 | — |
| ≈12.8 % | — | — | 22.1 (12 %) | 25 MPa |
| ≈19.9 % | — | — | — | 50 MPa |
| 20 % | **50.3** | 20.1 | 50.9 | — |
| ≈25.3 % | — | — | 73.4 (25 %) | 75 MPa |
| 30 % | **98.7** | 50.9 | 99.7 | 100 MPa @ 30.1 % |
| ≈35.1 % | — | — | 124.7 (35 %) | 125 MPa |
| ≈39.3 % | — | — | 153.4 (39.5 %) | 150 MPa |
| 40 % | **157.7** | 146.8 | ≈157 (끝점) | — |
- 본문 값 · 그림 4b · 스냅숏 셋은 서로 맞는다 · **그림 3 캡션 값만 다르다** (9.2 · 20.1 · 50.9 · 146.8 MPa 는 그림 4b 의 ≈8 · ≈12 · ≈20 · ≈38 % 자리) [카드 산술] — 캡션 오기인지 다른 런인지 [미확인].
- 그림 4a · S4b 의 모의 점 (최대 압력) 은 12.4–12.5 · 40.0 · 79.8–80.0 · 120.0 · 157.6–157.7 MPa [판독] — 10 % 압축 런의 최대 압력 ≈12.5 MPa ↔ 40 % 런의 10 % 지점 13.9–14.2 MPa.  다섯 런의 압축도 (첫 점 = 10 % · 마지막 = 40 %) 외에 가운데 셋 [미확인].

### 3-6. ★ 압력–기공률 검증 (그림 4a · 표 1 · p.5–7)
| 최대 압력 (MPa) | 실험 (그림 4a · [판독]) | 실험 (표 1 · [인쇄]) | 모의 · 이론 물질 부피 (빨강 · [판독]) | 모의 · 입자 메시 (주황 · [판독]) | 모의 (빨강) − 실험 [카드 산술] |
|---|---|---|---|---|---|
| 0 | 48.0 | 47.97 | 50.0 (주황에 반쯤 가림) | 50.0 | +2.0 |
| 12.4 | — | — | 44.4 | 45.2 | — |
| 40 | — | — | 42.3 | 43.2 | — |
| 80 | **28.6** | **27.75** | 38.1 | 39.1 | **+9.5 (그림) · +10.4 (표)** |
| 120 | 27.8 | (줄 없음) | 32.7 | 34.7 | +4.9 |
| 150 / 157.6 | 25.2 | 25.17 | 29.2 (본문 29.12 %) | 31.9 | +4.0 |
- 기공률은 모의 · 실험 모두 **하중을 뺀 뒤** (모의 = 이완 뒤 · *"calculated from the electrodes after relaxation"* p.5) · 157.7 MPa 런은 **최대 압력에서 26.72 %** 도 인쇄 (p.7).
- 두 연산자 차 (주황 − 빨강) = 0.1 (0) · 0.8 · 0.9 · 1.0 · 2.0 · 2.7 %p [판독 · 카드 산술] — *"The difference comes from the overlapping appearing after the calendering between the primary particles of AM, resulting in a higher simulation error under high calendering pressures."* (p.5–6).
- 저자 판정: *"Overall, our simulation results have a reasonable agreement with the experimental results"* (p.6) · 157.7 MPa: *"the simulation results are slightly higher than the experimental results. This may be due to the inability of the simulation to capture the plastic behavior exhibited by the electrode during this process since we use an elastic contact model."* (p.7) · 초록 *"the changes of the applied pressure and porosity are consistent with the experimental values"* ↔ 80 MPa +9.5 %p [판독].
- ⚠ 그림 4a 의 실험 점 넷 ↔ 표 1 셋: 80 MPa 점 28.6 % [판독] ≠ 표 27.75 % (막대 ±0.23 밖) · 120 MPa 점 27.8 % [판독] 은 표에 없다 (값이 표의 80 MPa 와 같다) · 마이크로 XCT 120 MPa 는 23.5 % [판독] — 그림 4a 실험 점의 출처 [미확인].

### 3-7. ★ 결합 파단 — 전극 전체 (그림 4b · S8 · p.7–8)
- 원문: *"approximately 1.8%, 4.5%, and 11.1% of the bonds are broken when the pressure reaches 50 MPa, 100 MPa, and 150 MPa, respectively. Almost all bond fractures occur under the stress of compression during the calendering process, while only a negligible number of bonds undergo changes during electrode relaxation. The latter accounts for 3% of the total bond fractures"* [인쇄 p.7].
- 그림 4b 초록 [판독]: 남은 결합 99.9 (5 %) · 99.2 (10 %) · 98.7 (15 %) · 98.2 (20 %) · 97.3 (25 %) · 95.5 (30 %) · 92.5 (35 %) · 90.2 (38 %) · 88.9 (39 %) · 이완 중 ≈88.1 % 그대로 → 끝 ≈11.9 % 끊김 · **10 % 통과 ≈38.2 % ≈144 MPa** [판독 · 보간].
- 그림 S8 (전극을 세 겹 *"three identical volumes"* 로 나눔 · [판독]): 아래 (집전체 쪽) ≈13,420 → ≈11,100 (**−17.3 %**) · 가운데 ≈12,680 → ≈11,730 (−7.5 %) · 위 ≈12,370 → ≈11,160 (−9.8 %) · 합 ≈38,470 → ≈33,990 (**−11.6 %**) [카드 산술].  아래 겹은 압축도 ≈5 % (≈3 MPa) 부터 줄고, 가운데 · 위는 ≈20 % 까지 거의 그대로 [판독].  ⚠ 세 겹의 처음 결합 수가 다르다 (같은 부피인데 아래가 가운데 · 위보다 6–8 % 많다 [카드 산술]) — 겹을 처음 높이로 나눴는지 지금 높이로 나눴는지 [미확인].
- 원문 해석: *"the number of bond breaks is not linearly related to the reduction of the thickness due to the uneven force inside the electrode"* · *"bond breakage occurs just after calendering starts, which indicates that cracks can appear in the particles even at the beginning of calendering"* (p.8).

### 3-8. ★ 결합 파단 — 입자별 (그림 5 · S5 · S6 · S7)
| 입자 | 원문 | 남은 결합 [판독] | 표지 |
|---|---|---|---|
| 그림 5 — 아래-가운데 · 등가 지름 **11.96 µm** · 1 차 입자 **426** · 결합 **1748** | *"noticeable bond breakage only when … exceeding 120 MPa and has 17% bonds break after 40% compression degree"* · *"slight deformation of the particle"* | 99.4 (20 % · 50 MPa) · 99.0 (25 %) · 96.9 (30 % · 100 MPa) · 96.5 (32 %) · 94.3 (33 %) · 91.2 (34 %) · 89.3 (35 % · 125 MPa) · 87.9 (37 %) · 83.5 (38–40 %) → **90 % 통과 ≈34.6 % ≈122 MPa** [보간] · 17 % = 297 결합 [카드 산술] | [인쇄] p.7–8 · [판독] 그림 5b |
| 그림 S6 — 집전체 쪽 | *"experienced earlier bond breakage at below 10 MPa and exhibited noticeable deformation when the electrode was subjected to a pressure of 75 MPa"* · 집전체가 변위 · 회전을 막는다는 해석 | 99.2 (5 %) · 97.7 (6 %) · 94.1 (10 %) · 89.3 (15 %) · 85.1 (20 %) · 73.2 (25 %) · 67.7 (30 %) · 58.4 (35 %) · **≈54 (39.7 %)** | [인쇄] p.8 · [판독] 그림 S6b |
| 그림 S7 — 윗면 쪽 | *"fewer bond breakages, even under high pressure, with less than 10% of bonds being fractured"* | ≥ 99.2 (≤ 37 %) · 96.5 (38 %) · **≈91.4 (39.7 %)** | [인쇄] p.8 · [판독] 그림 S7b |
| 그림 S5 — 10 % 압축 뒤 지름별 | *"most of the cracks appear in bigger particles"* · *"bigger secondary particles will break first"* [15] | 끊긴 결합 수 ≈21 (5.8–6.1 µm 둘) · 21 (6.9) · 51 (8.5) · 57 (10.2) · **93 (11.0 µm)** · 나머지 1.9–10.7 µm 는 ≈0 [판독] | [인쇄] p.7 · [판독] |
- ⚠ 그림 S5 의 가장 큰 x 는 ≈11.0 µm 이고 그림 5 의 11.96 µm 입자 자리 (10 % 에서 0 끊김이면 ≈12 µm 의 0 점) 가 보이지 않는다 [관찰] — S5 의 '지름' 정의 (등가 지름인지) · 포함 입자 [미확인].
- 곡률: *"cracks are more likely to appear in regions where the curvature is higher,[60] which is also corroborated in our model by the particles shown in Figure 5 and Figure S8"* (p.8) — 곡률을 계산한 수치 없음.

### 3-9. ★ 되돌아옴 (그림 S4 · 4b · 영상 S3 · p.6–7) 과 질량 보존 산술
- 정의 (그림 S4a · [인쇄]): *"h₁: compressed thickness"* · *"h₂: spring back thickness"* · *"Spring back degree = h₂/ h₁×100%"* (그림 안 글자) — 그림에서 h₁ 은 처음 윗면 → 압축 윗면 (= 변위), h₂ 는 압축 윗면 → 되돌아온 윗면 [관찰].
- 값 (그림 S4b · [판독]): 최대 압력 12.5 · 40.0 · 80.0 · 120.0 · 157.7 MPa → **31.2 · 37.7 · 36.3 · 33.0 · 32.6 %**.  원문: *"In general, the higher the maximum applied pressure, the lower the spring back degree"* · 첫 점 (10 %) 만 예외 — *"the pressure applied to the electrode is not high enough to reach the elastic conditions, and the microstructure evolution is mostly governed by particle rearrangement"* (p.7) · 되돌아옴 = *"fast elastic recovery of the electrode as reported in the literature."*[58] (p.6).
- 40 % 런 (그림 4b 빨강 · [판독]): 위판 하중 0 이 되는 압축도 ≈26–27 % → 되돌아옴 ≈13 %p = 변위 40 % 의 ≈33 % [카드 산술] — 그림 S4b 의 157.7 MPa 점 32.6 % 와 맞는다.
- 영상 S3 (3 초 간격 표본 · [관찰]): 최대 압축 ≈21 s · 판이 침대에서 떨어지는 때 ≈28–30 s · 끝 (41.7 s) 에 판은 처음 자리 · 침대는 처음보다 얇다.
- ⚠ **질량 보존 산술** [카드 산술]: 처음 기공률 ≈50.0 % [판독 그림 4a] 에서 두께를 40 % 줄이면 고체 부피 보존으로 ε = 1 − 0.500/0.600 = **16.7 %** 여야 하는데 인쇄값은 **26.72 %** (최대 압력) · 26.72 % 는 두께 비 0.682 (−31.8 %) 를 뜻한다.  이완 뒤 29.12 % 는 두께 비 0.705 를 뜻해 최대 압력 (0.682) 대비 **+3.4 %** 만 두꺼워진 셈인데, 되돌아옴 32.6 % 는 압축 두께 0.600 → 0.730 (처음 두께의 +13.0 %p · 압축 두께 대비 **+21.7 %**) 을 뜻하고 고체 부피 보존이면 이완 뒤 ε ≈ 31.5 % 여야 한다 (인쇄 29.12 %).  ⇒ **처음 기공률 · 압축도 · 최대 / 이완 기공률 · 되돌아옴 정도가 한 고체 부피로 함께 맞지 않는다** — '압축도' 의 기준 높이 (상자 높이 · 침대 맨 위 입자) · 기공률의 부피 정의 (부분 부피인지) · h₂ 를 잰 방법이 원문에 없다 [미확인].

### 3-10. 결합 강도 매개변수 연구 (그림 S3)
- 원문 캡션: *"The relation between bond fractures and bond strength parameter values was investigated. In this study, all the other parameters used in the simulations were kept constant."* · 본문: *"Here, as a first DEM model for the fracture of NMC particles, a simple parametric study is performed to elucidate the influence of this value"* (p.4).
- [판독]: 'Sigma value' 0.1 · 0.3 · 0.5 · 0.8 · 1.0 (×10⁶) → 끊기지 않은 결합 **0.7 · 78.7 · 93.8 · 96.7 · 96.8 %**.
- ⚠ 축 단위 · 시험한 압축도 · 압력 **인쇄 없음** — Pa 라면 0.1–1 MPa 로 표 S3 의 σ_B^n **0.1 GPa (= 1 × 10⁸ Pa)** 보다 100–1000 배 작고, 표 S3 값은 시험 범위 밖이다 [카드 산술] · 표 S3 의 값이 이 연구에서 어떻게 골라졌는지 [미확인].

### 3-11. 원문 안에서 서로 맞지 않는 인쇄값 (모음)
1. 결합 E_b: 본문 '입자 값과 같게' ↔ SI 표 3 **10 GPa** (입자 5 GPa).
2. 강도: 본문 σ_B^cn = σ_B^ct ↔ SI 표 3 0.1 ≠ 0.038 GPa.
3. 압력: 본문 14.2 · 50.3 · 98.7 · 157.7 MPa ↔ 그림 3 캡션 9.2 · 20.1 · 50.9 · 146.8 MPa (같은 10–40 %).
4. 실험 점: 그림 4a 80 MPa 28.6 % · 120 MPa 27.8 % [판독] ↔ 표 1 80 MPa 27.75 % · 120 MPa 줄 없음.
5. 압연 전 두께: 본문 114 µm ↔ 표 1 99.03 µm · 150 MPa 기공률 본문 25.16 ↔ 표 25.17 %.
6. 모의 기공률 · 압축도 · 되돌아옴의 질량 보존 (§3-9).
7. Δt '≈1.5 % Rayleigh 시간' ↔ 밀도 가정 산술 0.24 % (§3-4).
8. 식 (6) 첫 항 *"−|F_B^n|/A_b"* — 절댓값 앞 음수 부호 (법선력이 인장이어도 최대 법선 응력을 줄이는 꼴) · 원전 [51] 의 부호 규약과 대조 [미확인].

---

## 4. ★ 방법 — 실험 사슬 · 계산

### 4-1. 측정 사슬 (재구성)
슬러리 (96 : 2 : 2) → 도포 (Al 22.5 µm) → 건조 (85 / 95 °C) → 롤 압연 (60 °C · 0.54 m/min · 간격 21 · 6 µm) → (a) 질량 · 두께 → 기공률 (표 1) (b) 나노 XCT (가운데 조각 · 41 nm · 압연 전 / 80 / 150 MPa) → 3 상 분할 → 균열 정성 (c) 마이크로 XCT (0 · 100 · 120 · 150 MPa) → 기공률 · tortuosity factor (그림 S2).  **모든 측정이 압연 뒤 (하중 뺀 뒤)** — *"it is difficult to obtain in operando the mechanical behavior of particles under each pressure"* (p.4).

### 4-2. ★ 계산 (p.4–5 · SI p.3)
| 항목 | 내용 | 표지 |
|---|---|---|
| 코드 | 슬러리 · 건조 = LAMMPS [54] (앞 논문 [44]) · 압연 = **LIGGGHTS [55] 수정판 [56] (BPM 구현)** | [인쇄] p.5 |
| 입자 | AM = 실형상 2 차 입자 (마이크로 XCT · PSD) = **1.59 µm 1 차 구 응집체** · CBD = 1.16 µm 구 (나노 기공 27 %) | [인쇄] p.4–5 |
| 접촉 (입자–입자) | **헤르츠 탄성** 법선 + 접선 (누적 접선 변위 · 쿨롱 상한) + 점성 감쇠 (식 1–2) · k_n · k_t · γ_n · γ_t ← E_p · Po_p · e_p (*"estimated from"* — 식 [미확인]) | [인쇄] p.4 |
| 점착 | SJKR F_C = −c_CED A_COH n (식 3) — 2 차 입자 · CBD 사이 + 같은 2 차 입자의 1 차 입자 사이 (안정성 때문) · c_CED = SI 표 2 | [인쇄] p.4 |
| 결합 (1 차 입자 사이) | BPM — 식 (4)–(7) · 파단 기준 · 결합 감쇠 없음 · E_b · Po_b = 입자 값 (본문) / 10 GPa (SI) | [인쇄] p.4–5 |
| 경계 | 위판 (롤) · 아래판 (집전체) · 판에 평행한 방향 주기 · 중력 | [인쇄] p.4 |
| 하중 | 위판 하강 0.01 m/s → 정해진 변위 (최대 40 %) → 같은 속도로 처음 자리까지 상승 | [인쇄] p.5 |
| 읽기 | 압력 = 위판 접촉력 ÷ 910 µm² · 기공률 (이완 뒤) = 이론 물질 부피 (빨강) · 입자 좌표 · 반지름 메시 (주황) · 결합 수 (전체 · 입자별 · 세 겹) | [인쇄] p.5–8 |
| 맞춤 | E_p · Po_p ← 최대 압력 (압력–기공률 곡선) · 강도 = 매개변수 연구만 | [인쇄] p.4–5 |
| 수치 | Δt 0.01 ns · *"verified to give numerical stability"* · 판 속도 영향 *"negligible"* 확인 (값 [미확인]) | [인쇄] p.5 |
| 비용 | 런당 2–9 일 (압축도에 따라) · 28 코어 · 1 노드 · 128 GB · 런 수 = 최대 압축 다섯 [판독 그림 S4b] | [인쇄] p.5 |
| 입자 수 · 상자 높이 · 조성 (모의 AM : CBD) | **[미확인]** (전체 결합 ≈38,470 [판독]) | — |

### 4-3. 식 (번호별 크롭)
- (1) **F_E^n = k_n δ n − γ_n v_r^n** — 법선 탄성 (헤르츠) + 감쇠 · `eq_01_normal_hertz_damped.png`
- (2) **F_E^t = −min(μ_t |F_E^n|, |−k_t S_t − γ_t v_r^t|) t** — 접선 · 쿨롱 상한 · `eq_02_tangential_coulomb_capped.png`
- (3) **F_C = −c_CED A_COH n** — SJKR 점착 · `eq_03_sjkr_cohesion.png`
- (4) **ΔF_B^n = (E_b A_b / l_b) v_r^n Δt** — 결합 법선 힘 증분 · `eq_04_bond_normal_force_increment.png`
- (5) **ΔF_B^t = ((E_b/2(1 + Po_b)) A_b / l_b) v_r^t Δt** — 결합 접선 힘 증분 · `eq_05_bond_tangential_force_increment.png`
- (6) **σ_B^n = −|F_B^n|/A_b + |M_B^t| R_min / I** — 결합 최대 법선 응력 (인쇄 그대로) · `eq_06_bond_max_normal_stress.png`
- (7) **σ_B^t = |F_B^t|/A_b + |M_B^n| R_min / J** — 결합 최대 전단 응력 · `eq_07_bond_max_shear_stress.png`
- 파단 기준 (줄글 · 번호 없음): **σ_B^n ≥ σ_B^cn 또는 σ_B^t ≥ σ_B^ct** · *"For normal and shear breakage to be possible, σ_B^cn = σ_B^ct"* · 되돌아옴 정도 = **h₂/h₁ × 100 %** (그림 S4a · `fig_S4a.png`)
- 묶음 (기호 정의 포함): `eq_01_03_contact_set_with_symbols.png` · `eq_04_07_bond_set_failure_criterion_with_symbols.png`

### 4-4. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM 한계 진술 (원문 문장 · 위치)**:
  - *"This may be due to the inability of the simulation to capture the plastic behavior exhibited by the electrode during this process since we use an elastic contact model."* (p.7 · 기공률이 실험보다 높은 이유)
  - *"Although the real primary particle crystal shape is not spherical and the size is smaller than the primary particle size within the model, here, we perform a coarse-grained simulation with primary spherical particles of 1.59 μm diameter to simulate the AM mechanical behavior against the strain."* (p.5)
  - *"The difference comes from the overlapping appearing after the calendering between the primary particles of AM, resulting in a higher simulation error under high calendering pressures."* (p.5–6 · 구 겹침 = 기공 연산자 오차)
  - *"Since the nano-fracture we observe is smaller than the scale of our model, we are not able to observe the fracture of the secondary particle from the simulation results."* (p.7)
  - *"the addition of cohesion (SJKR) between primary particles in our simulations was required to ensure the stability of the secondary particle. This limitation will be further investigated in future work."* (p.4)
  - *"These observations are qualitative, in future work, a fully calibrated model will allow to elucidate the crack propagation trajectories"* · *"due to the scale limitation, we cannot observe the fracture and the reintegration of the material due to the binder after the fracture generation"* (p.8)
- **(ii) 소성 · 큰 변형을 넣기 어려운 이유와 우회 · 비용**: 원문은 소성을 넣지 **않았다** (탄성 헤르츠) 고 스스로 적고 그것을 기공률 차의 원인으로 지목한다 (p.7).  '입자 모양 변화' 는 소성이 아니라 **결합으로 묶인 1 차 구의 재배열 · 결합 끊김** 으로 대리한다 (*"slight deformation of the particle … accompanied by the bond breakage"* p.7).  우회의 값: 입자 E_p 를 **5 GPa 로 낮춰 최대 압력에 맞춤** (같은 그룹 앞 논문 135 · 200 GPa 의 1/27–1/40 [카드 산술]) — 우리 DEM 의 18 배 연화와 같은 꼴의 '맞춘 탄성률' (§7-4).  비용 = 런당 2–9 일 × 28 코어.  결론의 관찰 문장: *"With the increase of the pressure and the decrease of the electrode porosity, the source of the microstructural change in the electrode changes from the movement of particles to the deformation and fracture of particles."* (p.8).
- **(iii) 차원**: 측정 (XCT) · 계산 모두 **3D** · 2D 는 표시용 단면뿐 · 2D → 3D 전이 진술 없음.
- **(iv) 탈압**: **있다** — 같은 속도로 위판을 처음 자리까지 되돌림 · 되돌아옴 정도 31–38 % · 이완 중 결합 끊김 = 전체의 3 % (*"may be attributed to the interaction forces among the AM secondary particles during the rearrangement in the relaxation process"* p.7) · 실험 쪽 되돌아옴 측정은 없다 (표 1 은 압연 뒤 두께뿐).

### 4-5. 기법 미니 용어집
- **결합 입자 모델 (BPM · bonded-particle model)** = 두 입자 사이에 가상의 원기둥 '접착 막대' 를 두어 힘 · 모멘트를 전하고, 막대의 최대 응력이 강도를 넘으면 끊는 DEM 기법 (Potyondy–Cundall 2004 · 암석 파괴에서 시작).
- **1 차 / 2 차 입자** = NMC 다결정 입자 (2 차, 수–십 µm) 는 작은 결정 (1 차) 의 응집체 — 이 모델의 1 차 구 1.59 µm 는 실제 1 차 입자보다 크다 (조대화).
- **SJKR (simplified JKR)** = 접촉 면적 × 점착 에너지 밀도로 당기는 힘을 주는 단순 점착 법칙.
- **되돌아옴 정도 (spring back degree)** = 압축 변위 대비 되돌아온 높이의 비율 (이 논문 정의 h₂/h₁).
- **TXM (투과 X 선 현미경) 나노 XCT** = 렌즈로 확대한 X 선 단층 촬영 (여기 복셀 41 nm) — 1 차 입자 사이 나노 균열이 보이는 해상도.
- **Rayleigh 시간** = 레일리 표면파가 입자를 지나는 시간 — DEM 시간 간격의 안정 기준으로 그 몇 % 를 쓴다.
- **두 기공 연산자** = '이론 물질 부피' (고체 부피를 입자 부피 합으로 · 겹침 무시) ↔ '메시' (입자 좌표 · 반지름으로 실제 차지 공간) — 겹침이 많을수록 차이가 커진다 (우리 ε_sphere ↔ ε_union 과 같은 꼴).

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 나노 XCT 단면 + 3D — (a) 압연 전 입자 1–3 (b) 150 MPa 입자 4–6 · 보라 = 나노 균열 | R7 실험 쪽 정성 근거 (NMC111 · LIB 롤 압연 · 150 MPa) |
| 2 | 계산 흐름 (마이크로 XCT 형상 → 슬러리 · 건조 → 압연 · 결합 구조) | 제조 사슬 · 형상 출처 |
| 3 | 40 % 런 단계 (0–40 %) — 입자 / 결합 (하늘색 = 끊길 결합) | 끊김 위치 (판 · 집전체 근처) 그림 · 캡션 압력 어긋남 (§3-5) |
| 4 (a · b) | ★ (a) 압력–기공률 (실험 · 두 연산자) (b) 압력–압축도 (압축 · 이완) + 결합 수 | 기공 연산자 병기 · 되돌아옴 · 끊김–압력 곡선 (판독 digitized.csv) |
| 5 (a–d) | ★ 고른 입자 (11.96 µm) — 위치 · 압력 + 결합 수 · 형상 · 결합 | '120 MPa · 10 %' 의 출처 |
| S1 | 나노 XCT 80 MPa 단면 | '80 MPa 온전' 의 근거 (틈 보임 — §3-3) |
| S2 (a–f) | 마이크로 XCT 0 · 100 · 120 · 150 MPa · 분할 · 기공률 + tortuosity factor | 실험 쪽 기공 · tortuosity 추세 (방법 미확인) |
| S3 | 결합 강도 매개변수 연구 | 강도 미보정의 근거 · 단위 미확인 |
| S4 (a · b) | 되돌아옴 정도 정의 · 압력별 값 | 단계 6 보고 꼴 |
| S5 | 10 % 압축 뒤 지름별 끊긴 결합 수 | 크기 의존 (큰 입자 먼저) |
| S6 · S7 | 집전체 쪽 · 윗면 쪽 입자 | 위치 의존 (54 % ↔ 91 % 남음) |
| S8 | 세 겹 결합 수 | z 겹별 집계의 본 |
| 표 1 · S1–S3 | 실험 전극 · 모델 물성 · 점착 · 결합 | §3-2 · §3-4 |
| 영상 S2 (inbox 'Sup2' · 41.7 s · 1024×768 · 10 fps) | **결합 변화** — 2 차 입자별 색 결합망 · 압축 (≈0–21 s) → 이완 (≈21–41.7 s) · 본문 *"A video showing bonds change during the calendering simulation"* 과 내용 일치 [관찰] · 정지 화면 `vid_S2_t00s` · `vid_S2_t21s` | 결합망 표현 예 |
| 영상 S3 (inbox 'Sup3' · 41.7 s · 1024×768 · 10 fps) | **구조 변화** — 같은 런의 입자 (CBD 검정) · 판이 ≈28–30 s 에 떨어짐 [관찰] · *"A video showing structure change during the calendering simulation"* · 정지 화면 `vid_S3_t21s` · `vid_S3_t41s` | 되돌아옴 시각 |
| 영상 S4 (inbox 'Sup4' · 17.0 s · 1728×720 · 25 fps · 소리 트랙 무음 −91 dB) | **입자 상세** — 나노 XCT 로 본 150 MPa 압연 2 차 입자 하나 (청록 표면 · 보라 나노 균열 · 5 µm 막대) 회전 → 단면 회전 · *"A video showing particle details"* [관찰] · 정지 화면 `vid_S4_t04s` · `vid_S4_t16s` | 균열의 3D 모습 (어느 입자인지 원문에 없음 — 그림 1b 의 단면 입자 5 와 같은 표현) |
| 표지 | 12/2023 Cover Feature 그림 (본문 1 쪽 제목 옆 축소판) | 자료 없음 |
| 식 크롭 9 장 | (1)–(7) 각각 + 묶음 둘 (기호 정의 · 파단 기준 포함) | 보고서 R7 절에 붙일 식 |
| 근거 문단 20 장 | `txt_p1_*` · `txt_p2_*` · `txt_p3_*` · `txt_p4_*` · `txt_p5_*` · `txt_p6_p7_*` · `txt_p7_p8_*` · `txt_p8_*` (figures.json 에 한 줄 뜻) | 원문 인용용 |
- 영상 번호 = inbox 파일 이름 (Sup2 · Sup3 · Sup4) · 원문 (p.8) 은 번호 없이 세 편을 '입자 상세 · 구조 변화 · 결합 변화' 순으로 적는다 — 파일 번호 순서와 반대 [관찰].

## 6. Post-processing ★
- **무엇을**: 압력 (판 접촉력 ÷ 910 µm²) · 기공률 (두 연산자 · 이완 뒤) · 결합 수 (전체 · 입자별 정규화 · 세 겹 절대 수 · 지름별) · 되돌아옴 정도 · 실험: 질량 · 두께 기공률 · 나노 XCT 3 상 분할 (정성) · 마이크로 XCT 기공률 · tortuosity factor.
- **안 한 것**: 균열 정량 (*"could not be accurately quantified"*) · 접촉 수 · 배위수 · 힘 사슬 · 입자 응력 · 강도 보정 · 실험 되돌아옴 · 수송 (σ) · 해상도 (1 차 구 크기) 수렴 · 반복 · 오차 막대 (모의) · 실험 균열 ↔ 모의 끊김의 입자 대 입자 대조.
- **이 카드의 후처리**: 그림 4a · 4b · 5b · S2f · S3 · S4b · S5 · S6b · S7b · S8 판독 (112 행 · 300 dpi 렌더 · 눈금 직선 맞춤 · 화살표 · 범례 제외 구간) · 10 % 통과 압력 보간 (전체 ≈144 · 입자 ≈122 MPa) · 표 1 정합 산술 (Al 22.5 µm 포함 추론) · 질량 보존 산술 · Rayleigh 시간 산술 (가정 밀도) · 결합 전단 탄성률 · 강도 비.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · `docs/` 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 재료 · 상 | NMC111 + CBD (액체 LIB) · **SE 없음** | LPSCl SE + NCM811 (+ 첨가제) | 상 구성이 다르다 — AM 이 하중을 다 진다 (우리 f_AM ≡ 1 극한) |
| 공정 · 압력 | 롤 압연 (실험) / 평판 (모의) · ≤ 157.7 MPa · 60 °C | 다이 냉간 성형 300 MPa · 상온 | 압력 ≈½ · 공정 다름 |
| AM 표현 | **1.59 µm 1 차 구 응집체 + BPM 결합** (실형상) | DEM = 구 1 개 (E 140 GPa · CLAUDE.md) · MPM = 동결 강체 골격 | 그들은 AM 안쪽 자유도가 있다 · 우리는 없다 |
| AM 파괴 | 결합 끊김 (계산 중 · 역학 되먹임) · 끊긴 몫 1.8–11.1 % | Auerbach 사후 분류 (P_c = A·K_IC²·R/E\* × Lawn 배수 1 · 3 · 11 · 32 — `wheatcroft2023` 카드 §7.3 이 옮긴 우리 식) · f_intact → σ 폼 (CLAUDE.md) | §7-3 |
| 접촉 법칙 | 헤르츠 탄성 + 감쇠 + SJKR | hooke/hysteresis (DEM) · J2 연속체 (MPM) | 둘 다 '소성 없는 DEM' — 그들은 그 한계를 문장으로 적었다 |
| 맞춘 탄성률 | **NMC E_p 5 GPa** (최대 압력) | SE E_eff 1.35 GPa (18 배 연화 · 기공 · Cronau 겹침) · MPM 1.53 GPa | §7-4 |
| 탈압 | 같은 속도 되돌림 · 되돌아옴 31–38 % · 이완 중 끊김 3 % | DEM 언로딩 키트 진행 (CLAUDE.md 10-14 H0–H5 PASS) · MPM 제하 없음 | 보고 꼴은 가져올 수 있다 (단계 6) |
| 기공 연산자 | 이론 물질 부피 ↔ 메시 (최대 2.7 %p 차) | ε_sphere ↔ ε_union (관례 오프셋 1.251 %p · CLAUDE.md 2026-08-12 정정) | 같은 구조의 함정 |
| 수송 | 없음 (FEM 은 미래) | 접촉망 Holm (DEM) · 복셀 FV (STEP3) | 우리 쪽만 |

### 7-2. ★ 랩 기준과 나란히 (판정 없이)
| 출처 | 재료 | 압력 · 상태 | 진밀도 분모 | 기공 |
|---|---|---|---|---|
| **랩 표준** | 순수 LPSCl | 300 MPa | **1.64 g/cm³** (고정) | **10–13 %** |
| 이 논문 (실험 · 표 1) | NMC111 : C65 : PVdF 96 : 2 : 2 (SE 없음) | 0 · 80 · 150 MPa (롤 · 압연 뒤) | [미확인] | 47.97 · 27.75 · 25.17 % [인쇄] |
| 이 논문 (마이크로 XCT) | 같음 | 0 · 100 · 120 · 150 MPa (압연 뒤) | 해당 없음 (영상 분할) | 51.1 · 26.2 · 23.5 · 21.4 % [판독] |
| 이 논문 (모의 · 이완 뒤) | 같음 (모델) | 12.4–157.6 MPa | 해당 없음 | 44.4 → 29.2 % (이론 부피) · 45.2 → 31.9 % (메시) [판독] |
- 이 표는 **"랩 표준과 다른 문헌 값"** 의 자리다 — SE 가 없는 액체 LIB 양극이라 랩 표준 (순수 SE) 과 같은 양이 아니다.  같은 줄에 두지 않는다.

### 7-3. ★ 조건 R7 — 우리 Auerbach / f_intact ↔ 이 논문의 결합 파단
- **같은 점**: 둘 다 '구 DEM 이 AM 을 깨지 못한다' 는 빈칸을 DEM 안에서 메우려는 장치 · 둘 다 크기 의존 (그들: 큰 입자 먼저 [그림 S5] · 우리: P_c ∝ R 이라 힘으로는 큰 입자가 늦게, 명목 응력으로는 먼저 — `song2025` 카드 §7-2 의 사다리).
- **다른 점 (같은 양이 아니다)**: ① 그들의 몫 = 2 차 입자 **안** 결합의 끊긴 비율 (입자 내부 손상) ↔ 우리 Auerbach = **입자 사이 접촉**의 힘 ÷ P_c 등급 · f_intact = 파괴로 뺀 접촉을 제외한 몫 ② 그들은 계산 **중** 끊어 역학이 바뀐다 (입자 *"slight deformation"*) ↔ 우리는 **사후** (압밀 경로는 그대로) ③ 그들은 수송이 없다 ↔ 우리는 f_intact 가 σ 폼에 들어간다 (σ_ionic β_F · σ_e β_Fe — CLAUDE.md) ④ 그들의 문턱 (결합 강도) 은 **보정 안 됨** ↔ 우리 P_c 의 K_IC (AM_P 0.3 · AM_S 1.0 MPa·m^½) 도 옛 출처가 실재 미확인 (`wheatcroft2023` 카드 §0 · SELF-51) — **둘 다 강도 앵커가 없다**.
- **숫자를 옮기지 않는 이유**: 그들의 '10 % ↔ 120 MPa' 는 입자 하나의 추측 · LIB · 맞춘 E_p 5 GPa 의 결과다.  우리 300 MPa 침대에서 '끊긴 결합 10 %' 에 해당하는 양을 만들려면 AM 을 응집체로 바꿔야 하고, 그 순간 비용 · 매개변수 (A_b · 강도 · E_b) 가 새로 생긴다.
- **가져올 것 (보고 꼴)**: 끊김 · 파괴 등급을 **z 세 겹 (집전체 쪽 · 가운데 · 위)** 과 **입자 크기 계급**으로 나눠 보고 (그림 S5 · S8 · S6 · S7) — 그들 모델에서 집전체 쪽이 가장 많이 · 가장 일찍 (−17.3 % ↔ −7.5 · −9.8 %) [판독 · 카드 산술] — 우리 Auerbach 표에 같은 나눔을 붙이면 he2026 N2 (z-슬랩 응력) 와 한 표가 된다.

### 7-4. 맞춘 탄성률 (frame [2]) — E_p 5 GPa 는 물성이 아니다
- 그들의 E_p 5 GPa 는 *"straightforwardly calibrated by fitting the maximum pressure"* 의 결과로, 같은 그룹 앞 논문들의 NMC 값 (135 · 200 GPa) 보다 27–40 배 작다 [카드 산술].  우리 DEM 의 SE E_eff 1.35 GPa (24 → 18 배 연화) 와 **같은 인식론** (맞춘 탄성률 = 빠진 기전 (재배열 · 소성 · 결합 거동) 을 접어 넣은 값) — 단 연화된 것은 **AM** (우리는 SE) 이고 재료 · 공정이 다르다.  ⇒ 숫자 대조는 하지 않는다.  문장으로만: *"한 탄성률을 최대 압력 하나에 맞추면 같은 계의 문헌 탄성률보다 수십 배 작아진다 (Xu 2023 · 이 논문 SI 표 1)"*.
- ⚠ 그 결과 결합 강성 (E_b · 본문은 E_p 와 같게) 도 맞춘 값을 물려받는다 — 결합 강도 0.1 GPa 와 짝을 이루는 강성이 물성에서 떨어져 있어 '응력 문턱' 의 뜻이 흐려진다 [카드 추론].

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: DEM 쪽 — AM 응집체 재배열 · 결합 파단의 위치 · 크기 의존 · 압력–압축도–되돌아옴 곡선.
- **없는 것**: SE · 소성 형상 변화 (그들 스스로 '탄성 접촉') · 접촉망 수송 · MPM / FEM 역학.  ⇒ 우리 DEM 쪽 R7 보고 꼴과 '맞춘 탄성률' 의 고백 문장을 준다 · MPM 쪽에는 *"plastic behavior … elastic contact model"* 이라는 '왜 연속체 소성이 필요한가' 의 근거 문장 하나를 준다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공률 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ (1) 한 논문 안 두 연산자 (이론 물질 부피 ↔ 메시) 의 차가 압력과 함께 0.1 → 2.7 %p 로 커진다 [판독] — 우리 ε_sphere ↔ ε_union 등록에 '압력별 차' 칸 (2) '최대 압력에서' (26.72 %) ↔ '이완 뒤' (29.12 %) 를 따로 등록 (3) **항등식 검사**: t/t₀ = (1 − ε₀)/(1 − ε) (고체 부피 보존) 를 보고 표에 자동 대조 — 이 논문의 인쇄값은 그 검사를 통과하지 못한다 (§3-9) (4) 실험 두께에 집전체가 들어갔는지 (표 1 산술 §3-2) — '두께' 의 정의를 등록 | 순수 SE 기공 · 진밀도 없음 |
| **단계 1** (3D 메모리 · 장 수) | 비용 감각뿐: 런당 2–9 일 × 28 코어 · 결합 ≈38,470 [판독] | 입자 수 · 메모리 [미확인] · MPM 장 아님 |
| **단계 2 · 3** (2D MPM · 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나 맞춤) | 없음 (SE 없음) · '맞춘 값 하나 (E_p) ← 최대 압력' 의 선례 = R5 꼴 | 맞춤 표적 아님 |
| **단계 5** (3D 복합 압밀) | 일부 — AM 응집체 + CBD 복합 압연 (SE 없음) · 위치별 손상 (집전체 쪽 먼저) | SE 하중 분담 · 소성 없음 |
| **단계 6** (탈압 · 되돌아옴) | ★ 프로토콜 = **같은 속도로 처음 자리까지 되돌림** · 되돌아옴 정도 = h₂/h₁ (변위 대비) 31–38 % · 높은 압력일수록 낮아지고 낮은 압력은 재배열 지배라 예외 · 이완 중 손상 3 % [인쇄 · 판독] — 우리 언로딩 보고 꼴 (최대 압력 기공 · 이완 뒤 기공 · 변위 대비 되돌아옴 · 이완 중 손상) | LIB · 탄성 접촉 · 실험 되돌아옴 없음 · 질량 보존 어긋남 (§3-9) |
| **단계 7** (형상 · 피복 · 수송) | 없음 (FEM 은 미래) | — |
| **후보 D0** (지금 DEM) | 같은 계열 (구 · 탄성 접촉) 이 스스로 쓴 한계 문장 (*"elastic contact model"* p.7) · 맞춘 탄성률 E_p 5 GPa (27–40 배 작음) = 우리 연화와 같은 인식론 | 숫자 대조 불가 (AM ↔ SE) |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 판 점착이 비대칭: 롤 (스테인리스) 과 NMC 5e5 · CBD 3e5 ↔ 집전체 (Al) 와 0 [인쇄 SI 표 2] — 판마다 다른 접촉 규칙을 둔 예 | 마찰 · 단위 [미확인] |
| **후보 A · A′** (MPM 강체 AM / 입자별 속도장) | 없음 | — |
| **후보 B** (입자별 FE) | 없음 | — |
| **후보 C · C′** (큰 변형 · 항복 캡 DEM) | 근거 문장만 — 탄성 접촉이 소성 거동을 못 잡아 기공률이 높다 (p.7) | C · C′ 을 쓰지 않았다 |
| **후보 M0** (균질화 압밀) | 없음 | — |
| **U0–U6** | **U1** (입자 하나 · 해상도): 11.96 µm = 1 차 구 426 개 (지름당 ≈7.5 개 [카드 산술]) · 나노 균열 (41 nm 복셀로 보이는 것) 은 1 차 구 (1.59 µm = 39 복셀 [카드 산술]) 아래 — 모델 해상도가 파괴 해상도를 정한다 · **U3** 류 (눌렀다 떼기) 의 전극 판 | 해상도 수렴 시험 없음 |
| **R1–R7** | **R7** ★ (위 §7-3) · **R4** (탈압 · 위 단계 6) · **R3** (입자 경계 기억) — 결합 ID 가 '처음 맞닿은 1 차 입자 쌍' 을 기억 · 끊기면 다시 안 생김 [카드 추론] · **R5** (맞춘 값 하나) — E_p (+ Po_p) 하나 · 강도는 미보정 · **R1** (AM 이 움직이며 하중) — AM 만 있어 f_AM ≡ 1 · **R2** (미끄럼 · 분리) — 쿨롱 · SJKR (μ_t 값 [미확인]) · **R6** (SE 형상 변형) 없음 | SE 관련 조건 (R1 의 분담 · R6) 은 주지 못한다 |
| **결과 전 대조 항목** | (가) **z 세 겹 손상 분포** — 집전체 쪽 > 위 > 가운데 (−17.3 · −9.8 · −7.5 %) [판독 · 모델 값] (나) **NMC111 LIB 롤 압연 균열 브래킷** — 80 MPa 온전 · 150 MPa 뚜렷한 균열 (나노 XCT 정성) (다) 되돌아옴 정도 31–38 % 의 압력 추세 (모델 값) | 맞추는 값 아님 · '모델 · LIB · 롤 압연' 표지 필수 |

- **재료 · 차원 · 조건 차이**: 재료 NMC111/CBD (LIB) ↔ 우리 NCM811/LPSCl · 3D = 같음 · 압력 ≤ 157.7 ↔ 300 MPa · 롤 / 평판 ↔ 다이 · 60 °C ↔ 상온 · 측정 = 압연 뒤 ↔ 우리 DEM / MPM 은 누른 채 (판 고정 이완) 가 기본.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **R7 보고에 위치 · 크기 나눔을 붙인다** — Auerbach 등급 수를 z 세 겹 · 입자 크기 계급으로 (그들 그림 S5 · S8 의 꼴) — 결과 전 대조 항목 (가) (근거 §3-7 · §3-8).
2. **기공률은 '최대 압력' · '뺀 뒤' 두 값 + 두 연산자 + 항등식 검사로 보고** — 한 논문 안에서 넷이 서로 안 맞는 사례 (§3-6 · §3-9) — 단계 0 · 6.
3. **'파괴 기준' 을 입자 하나 + 정성 영상으로 정하지 않는다** — 그들의 10 % 는 입자 하나 (122 MPa) 와 전극 전체 (144 MPa) 에서 압력이 다르고, 위치로 9 ↔ 46 % 가 갈린다 [판독] — 우리 Auerbach 문턱의 K_IC 0.3 도 옛 출처가 실재 미확인이라 같은 함정 (R7 · `wheatcroft2023` 카드 §0 · SELF-51).
4. **'맞춘 탄성률 = 물성 아님' 의 외부 사례** — 같은 그룹이 같은 NMC 에 135 · 200 GPa (앞 논문) 와 5 GPa (이 논문) 를 쓴다 — frame [2] 서술의 인용 근거 (§7-4).
5. **흐름 밖: 접촉망 수송** — 결합이 끊긴 2 차 입자의 내부 전자 경로 손실은 우리 σ_e (AM 은 '안이 꽉 찬 구') 에 없는 항이다 — 그들도 계산하지 않았다 (FEM 은 미래) → R7 이 σ_e 에 닿는 다음 자리.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "A bonded-particle DEM of NMC111 secondary particles (1.59 µm primary spheres, bond strengths 0.1/0.038 GPa) calendered to 50, 100 and 150 MPa breaks about 1.8, 4.5 and 11.1% of the intra-particle bonds; the authors speculate that a secondary particle cracks once ≈10% of its bonds are broken, which for one selected particle occurs above ≈120 MPa (Xu et al., Batteries & Supercaps 6 (2023) e202300371)."
- "The same authors attribute the remaining porosity mismatch to 'the inability of the simulation to capture the plastic behavior … since we use an elastic contact model' (Xu et al. 2023, p.7)."
- 국문: *"결합 입자 DEM 의 '끊긴 결합 10 % ≈ 120 MPa' 는 입자 하나에서 추측한 기준이며, 전극 전체로는 ≈144 MPa 에서 10 % 에 이른다 (Xu 2023 그림 4b 판독)."*
- 국문: *"최대 압력 하나에 맞춘 입자 탄성률은 5 GPa 로, 같은 그룹이 같은 NMC 에 쓴 135–200 GPa 의 1/27–1/40 이다 (Xu 2023 SI 표 1 · 카드 산술)."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **'120 MPa · 10 %' = 추측 · 입자 하나** — 보정 · 통계 없음 · 전극 전체 10 % 는 ≈144 MPa [판독] · 위치로 9–46 % 끊김 [판독].
2. **결합 강도 미보정** — 그림 S3 의 'Sigma value' 단위 · 시험 조건 없음 · 표 S3 의 0.1 GPa 는 시험 범위 밖 (Pa 로 읽으면) [카드 산술].
3. **결합 매개변수 어긋남** — E_b 10 ↔ '입자와 같게' (5) · σ_t 0.038 ≠ σ_n 0.1 ↔ 'σ_cn = σ_ct'.
4. **'reasonable agreement' · 초록 'consistent'** ↔ 80 MPa 에서 모의가 +9.5 %p [판독] — 고압 끝 (≈150 MPa) 에서만 +4 %p.
5. **그림 4a 실험 점 ↔ 표 1** — 80 MPa 값 다름 · 120 MPa 출처 없음 [판독].
6. **압력 세 벌** — 그림 3 캡션 값이 본문 · 그림 4b 와 다르다.
7. **모의 기공률 · 압축도 · 되돌아옴의 질량 보존 어긋남** (§3-9) — 기준 높이 · 부피 정의 미인쇄.
8. **표 1 두께에 집전체 포함 추정** [카드 추론] · 본문 114 µm ↔ 99.03 µm.
9. **Δt '≈1.5 % Rayleigh'** — 밀도 가정 산술로 0.24 % (≈6 배) [카드 산술 · 가정].
10. **1 차 입자 사이 SJKR 이 필요** — 결합만으로 응집체가 서지 않는다 (저자 고백) · 결합과 점착이 섞여 '결합 강도' 의 뜻이 흐려진다.
11. **소성 · 수송 없음** — 저자 스스로 '탄성 접촉' · FEM 은 미래 · 파괴가 성능에 주는 영향은 계산되지 않았다.
12. **공정 · 압력 정의 차** — 실험 압력 = 롤 간격 · 두께 공식 (계산) ↔ 모의 = 평판 접촉력 ÷ 910 µm² · 롤 ≠ 평판.
13. **재료** — 액체 LIB NMC111 (SE 없음) · AM 하중 분담 없음 (f_AM ≡ 1).
14. **그림 S5 에 11.96 µm 입자가 안 보인다** [관찰] · 세 겹의 처음 결합 수가 6–8 % 다르다 [카드 산술].
15. **식 (6) 부호** — −|F_B^n| (인쇄 그대로) · 원전 대조 [미확인].
16. **판독 값**은 300 dpi 렌더 눈금 맞춤 (잔차 x ≤ 0.10 · y ≤ 0.19 축 단위) — 그래도 [판독] 표지로만 인용.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 51 | D. O. Potyondy, P. A. Cundall, Int. J. Rock Mech. Min. Sci. 2004, 41, 1329. | BPM 원전 — 식 (6)–(7) · 파단 기준 · σ_cn = σ_ct 조건의 출처 (질문 l · R7) | 없음 (papers/ ls · grep 'Potyondy' = 인용만) |
| 56 | M. Schramm, M. Z. Tekeste, C. Plouffe, D. Harby, Biosyst. Eng. 2019, 186, 349. | 쓴 LIGGGHTS BPM 수정판 — 우리 LIGGGHTS 에 결합을 넣는 경로 | 없음 |
| 52 | Y. Guo, J. Curtis, C. Wassgren, W. Ketterhagen, B. Hancock, AIP Conf. Proc. 2013, 1542, 491. | 결합 힘 · 모멘트 증분식 (모멘트 식은 이 논문에 인쇄 없음) | 없음 |
| 36 | A. Lundkvist, P.-L. Larsson, E. Olsson, Powder Technol. 2023, 425, 118574. | 바인더 점탄성으로 '하중 뺀 강성' 을 잡는 압연 DEM (질문 b · 단계 6) | 없음 (wishlist 의 Lundkvist 2024 와 다른 논문) |
| 13 | R. Sim, S. Lee, W. Li, A. Manthiram, ACS Appl. Mater. Interfaces 2021, 13, 42898. | 고 Ni 양극 압연 중 균열 · 융합 (SEM) — R7 실험 | 없음 |
| 15 | F. Huttner, A. Diener, T. Heckmann, J. C. Eser, T. Abali, J. K. Mayer, P. Scharfer, W. Schabel, A. Kwade, J. Electrochem. Soc. 2021, 168, 090539. | NCM622 압연 입자 깨짐 · '큰 입자 먼저' · '초기에도 균열' | 없음 (wishlist L57 에 있음) |
| 31 · 32 | R. Ge, D. J. Cumming, R. M. Smith, Powder Technol. 2022, 403, 117366. · R. Ge, A. M. Boyce, Y. Shui Zhang, P. R. Shearing, D. J. Cumming, R. M. Smith, Chem. Eng. J. 2023, 465, 142749. | XCT 처음 구조 + AM 사이 결합 (바인더) 압연 DEM | 없음 (wishlist L242 · L326) |
| 53 | D. André, M. Jebahi, I. Iordanoff, J. Charles, J. Néauport, Comput. Methods Appl. Mech. Eng. 2013, 265, 136. | 다른 결합 파단 기준 | 없음 |
| 59 | J. Zhang, J. Sun, H. Huang, Z. Yuan, Particuology 2023, 85, 252–267. | 압축 중 역학 곡선 대조 (p.7) | 없음 |
| 60 | Y. K. Chen-Wiegart, Z. Liu, K. T. Faber, S. A. Barnett, J. Wang, Electrochem. Commun. 2013, 28, 127. | 곡률 큰 곳 균열 | 없음 |
| 7 | E. N. Primo, M. Chouchane, M. Touzin, P. Vazquez, A. A. Franco, J. Power Sources 2021, 488, 229361. | 롤 간격 → 압력 공식 · 센서 필름 보정 | 없음 |
| 11 | X. Lu, S. R. Daemi, A. Bertei, M. D. R. Kok, K. B. O’Regan, L. Rasha, J. Park, G. Hinds, E. Kendrick, D. J. L. Brett, P. R. Shearing, Joule 2020, 4, 2746. | 압연 미세구조 XCT | `lu2020_insitu_nanoct_calendering_microstructural_evolution` |
| 27 | C. Sangrós Giménez, B. Finke, C. Schilde, L. Froböse, A. Kwade, Powder Technol. 2019, 349, 1. | 압연 DEM (AM 만) · 높은 압력일수록 되돌아옴 낮음 | `sangros2019_dem_calendering_lib_electrode` |
| 41 | A. C. Ngandjong, T. Lombardo, E. N. Primo, M. Chouchane, A. Shodiev, O. Arcelus, A. A. Franco, J. Power Sources 2021, 485, 229320. | 판 · 집전체 표현 · 미세 압입 대조 | `ngandjong2021_dem_calendering_digital_twin` |
| 44 | J. Xu, A. C. Ngandjong, C. Liu, F. M. Zanotto, O. Arcelus, A. Demortière, A. A. Franco, J. Power Sources 2023, 554, 232294. | 실형상 · 처음 구조 | `xu2023_realistic_am_shape_cgmd_calendering` |
| 58 | A. Diener, S. Ivanov, W. Haselrieder, A. Kwade, Energy Technol. 2022, 10, 2101033. | 빠른 탄성 회복 (되돌아옴) | `diener2022_roll_gap_springback_calendering` |

---

## [미확인] 목록
- 모의: 전체 1 차 입자 · 2 차 입자 · CBD 수 · 모의 조성 · 상자 높이 · 처음 두께 · 반발 계수 e_p · 마찰 μ_t · 밀도 · 결합 반지름 (A_b) · l_b · 모멘트 증분식 · k_n · k_t · γ 식 · 판 속도 시험 값 · 다섯 런의 압축도 (가운데 셋) · '압축도' 의 기준 높이 · 기공률 부피 정의 · h₂ 측정법.
- 강도: 그림 S3 의 'Sigma value' 단위 · 시험 조건 · 표 S3 값의 선택 근거.
- 실험: 기공률 계산식 · 시료 면적 · 진밀도 · 두께 측정 압력 · 두께에 집전체 포함 여부 (산술상 포함 [카드 추론]) · 114 µm 의 뜻 · 그림 4a 120 MPa 실험 점 출처 · 마이크로 XCT 장치 · 복셀 · tortuosity 계산법 · 나노 XCT 조각의 위치 · 수.
- 그림 S5 의 지름 정의 · 그림 S8 겹 나눔 기준 · 영상 S4 의 입자가 어느 입자인지.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-16)
- 서지: 지시서 메모 (J. Xu · B. Paredes-Goyes · Z. Su · M. Scheel · T. Weitkamp · A. Demortière · A. A. Franco · 제목 · Batteries & Supercaps 2023, 6, e202300371 · DOI 10.1002/batt.202300371) = 원문 첫 쪽 · 모든 쪽 머리글 · PDF 메타데이터 (subject *"Batteries & Supercaps 2023.6:e202300371"*) 와 같음.  후보 표 · he2026 L690 의 'e202300525' 는 원문과 다름.  본문 10 쪽 · SI 7 쪽 (표지 1 + 내용 6) · 영상 3 편 (ffprobe: 41.7 s · 41.7 s · 17.0 s).
- 숫자: 텍스트 층 + 17 쪽 렌더로 대조 — 96 : 2 : 2 · 2 h · 25 °C · 22.5 µm · 85 · 95 °C · 0.54 m/min · 60 °C · 8.327 keV · 500 · 1000 투영 · 500 ms · 15 µm · 41 nm · 114 µm · 21 · 6 µm · 표 1 15 칸 (± 기호는 텍스트 층에서 빠짐 — 렌더로 확인) · 1.16 µm · 27 % · 0.64 µm · 0.01 m/s · 0.009 m/s · 0.01 ns · 1.5 % · 2–9 일 · 28 코어 · 2.40 GHz · 128 GB · 14.2 · 50.3 · 98.7 · 157.7 MPa · 10–40 % · 1.59 µm · 910 µm² · 157.7 · 26.72 · 29.12 · 25.16 % · 1.8 · 4.5 · 11.1 % · 50 · 100 · 150 MPa · 3 % · 11.96 µm · 426 · 1748 · 120 MPa · 17 % · 10 % · 10 MPa · 75 MPa · 0–157 MPa · 9.2 · 20.1 · 50.9 · 146.8 MPa (그림 3 캡션) · SI 표 1–3 전 칸 — 전부 위치 확인.
- 판독 보정: 각 그림의 큰 눈금 직선 맞춤 (그림 4a x 9 · y 8 눈금 · 4b x 9 · 왼 y 9 · 오른 y 9 · 5b · S6b · S7b 각 x 9 · 왼 9 · 오른 6 · S8 x 9 · y 9 · S2f x 9 · y 6 · S3 x 5 · y 6 · S4b x 9 · y 7 · S5 x 7 · y 6) · 화살표 · 범례 구간 제외 · 가려진 점 (그림 4a 0 MPa 빨강) 표지.
- 정본 중복 확인: papers/ 목록 · DOI '202300371' · 제목 낱말 · 'Paredes' · 'Weitkamp' grep — 카드 없음 (같은 1 저자 · 같은 해 `xu2023_realistic_…` = 다른 논문 · `wet_processing_…` · `he2026_…` 는 인용만).

## 🔗 관련 카드
- 같은 1 저자 · 같은 해 (다른 논문): `xu2023_realistic_am_shape_cgmd_calendering` (J. Power Sources 554 — 이 논문 ref [44] · 실형상 2 차 입자 · 건조 구조의 출처).
- 이 논문을 인용 · 가리킨 카드: `he2026_dem_calendering_inhomogeneity_areal_density` (백로그 N6 · L499 · L690) · `wet_processing_resolved_am_ssb_cathode_manufacturing` (ref [38] · L45 · L239).
- 같은 그룹 압연 DEM 계보: `ngandjong2021_dem_calendering_digital_twin` · `galvezaranda2024_time_dependent_dl_calendering_microstructure` · `vijay2025_hybrid_cgmd_dl_slurry_microstructure` · `benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode`.
- AM 파괴 판정 (조건 R7): `song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage` · `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` · `tovar2026_cold_spray_cathode_composite_dem_plastic_elastic_bond` · `heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct` · `dang2019_nmc111_secondary_particle_flat_punch_fracture_strength`.
- 결합 입자 (BPM) 로 입자 변형을 낸 다른 계산: `clemmer2024_bpm_elastic_grain_compaction_beyond_jamming` · `nguyen2017_mpm_bpm_deformable_particle_compaction`.
- 압연 되돌아옴: `diener2022_roll_gap_springback_calendering` · `kollenda2024_time_sensitivity_calendered_electrode_springback_storage` · `sangros2019_dem_calendering_lib_electrode`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
