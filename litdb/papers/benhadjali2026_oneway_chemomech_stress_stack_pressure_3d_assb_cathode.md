<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 형식 본 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md ·
     같은 사슬 이웃 = benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode.md (1 편 · 전기화학만) · 이 논문 (2 편 · 한 방향 역학) ·
     benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode.md (3 편 · 양방향 · ChemRxiv) · benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem.md (가리킨 카드).
     쪽 표기 = 학술지 쪽 'n of 14' (PDF 쪽 = 인쇄 쪽 · 본문 14 쪽) · SI = 따로 받은 7 쪽 PDF (SI p.1 = 제목 쪽).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv · 원 래스터를
     300 dpi 로 렌더해 큰 눈금 직선 보정 · 표지 중심 · 곡선 끝 열 · 겹친 표지는 눈 판독 — 방법은 그 파일의 note 칸) · [카드 산술] = 인쇄 · 판독 값으로
     이 카드가 계산한 값 (식 병기) · [카드 추론] · [카드 해석] = 이 카드의 해석 · [다른 카드] = 정본 다른 카드에 적힌 값 (원 논문 재확인 아님) ·
     [미확인] = 원문 (본문 14 쪽 + SI 7 쪽 전수) 에 없음.  원문은 텍스트 층 전부와 쪽 렌더로 읽었다. -->
# 습식 제조 모의 구조 (같은 그룹 · 압연 20 %) 위 3D 반쪽 셀 FEM 에서 NMC811 리튬화 팽창 (≈7 %) 이 만드는 변위 · 응력 — 한 방향 결합 (응력 → 확산 되먹임 없음) · AM · SE · CBD 선형 탄성 · 분리막 · 집전체 강체 · 측벽 고정 · 적층압 9 ↔ 68 MPa · C/5–C/20 방전 한 번: 반쪽 셀 0.78 · 1.61 · 2.53 % (9 MPa) ↔ −0.08 · 0.74 · 1.82 % (68 MPa) · AM 평균 von Mises 끝 318–463 MPa [판독] · SE 굴곡도 τ 7.736 → 8.182 → 7.765 · 물성 = SI 표 S2 (SE E 18.5 GPa = 70Li₂S–30P₂S₅ 유리 문헌값 · ν 0.3 · NMC811 175 GPa) · 소성 · 접촉 · 탈압 · 실험 대조 없음 — Ben Hadj Ali · Alabdali · Viallet · Seznec · Franco (Batteries & Supercaps 2026)

> slug `benhadjali2026_oneway_chemomech_stress_stack_pressure_3d_assb_cathode` · DOI `10.1002/batt.202500540` · type `3D microstructure-resolved FEM (COMSOL multiphysics) half-cell on a reused CGMD wet-manufacturing microstructure (LAMMPS slurry → drying → calendering · 20 % calendering degree · from Alabdali 2023) → voxelization with CBD-overlap volume reassignment (INNOV mesh) → one-way coupled electrochemistry → mechanics (Fick diffusion in AM without stress feedback · linear elastic AM / SE / CBD · intercalation eigenstrain from Koerver 2018 NMC811 ΔV) · stack pressure 9 vs 68 MPa · single discharge C/5 · C/10 · C/20 · interfacial area · pore size distribution · GeoDict SE tortuosity · no plasticity, no contact model, no fracture, no unloading, no experiment` · PDF `a98c4bc8-42._A_New_Three_Dimensional_Microstructure_Resolved_Model_to_Assess_Mechanical_Stress_in_Solid_State_Battery_Electrodes.pdf` + SI `c4b1864d-42._Sup_A_New_Three_Dimensional_Microstructure_Resolved_Model_to_Assess_Mechanical_Stress_in_Solid_State_Battery_Electrodes.pdf` · digested `2026-11-12` · status ✅
>
> **저자**: **Siwar Ben Hadj Ali** · Mohammed Alabdali · Virginie Viallet · Vincent Seznec · **Alejandro A. Franco\*** (교신 · alejandro.franco@u-picardie.fr) — LRCS (UMR CNRS 7314 · Université de Picardie Jules Verne · Amiens · 다섯 모두) · RS2E (Hub de l'Energie · 다섯 모두) · ALISTORE-ERI (FR CNRS 3104 · Ben Hadj Ali · Seznec · Franco) · Institut Universitaire de France (Franco) · *Batteries & Supercaps* **9** (2026) e202500540 (본문 14 쪽 · Research Article · © 2025 저자 · CC BY 공개 · 호 = 내려받기 머리글 *"25666223, 2026, 2"*) · 접수 2025-07-17 · 수정 2025-09-10 · *"Version of record online:"* 빈칸 (p.14) · SI 7 쪽 (그림 S1–S2 · 표 S1–S2 · 참고 [S1]–[S11]) · 연구비 = Umicore DESTINY 박사 과정 (H2020 MSCA COFUND #945357 · Ben Hadj Ali · Seznec · Franco) · Horizon Europe PULSELiON 101069686 (Franco · Alabdali) · IUF (Franco) · 이해상충 없음 · 자료 = 요청 시 · *"The authors declare having used ChatGPT (OpenAI) for an initial translation from French to English of some parts of the text"* (p.12–13) · 기여: Ben Hadj Ali = 개념 · 자료 · 분석 · 조사 · 방법 · 소프트웨어 · 시각화 · 초고 (모두 lead) / Alabdali = 시각화 · 검토 (equal) / Viallet = 연구비 (equal) / Seznec = 연구비 · 지도 (equal) / Franco = 개념 · 연구비 · 방법 · 과제 관리 · 자원 · 지도 · 검토 (lead) (p.13).  앞 판 = ChemRxiv 2025 `10.26434/chemrxiv-2025-84s4f` [다른 카드 — `benhadjali2026_fully_coupled_…` L407 의 2 차 서지 · 이 PDF 로 확인 안 됨].
> **이웃 카드 (링크만)**: [`benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode`](benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode.md) (이 논문 ref [16] · 같은 구조의 전기화학판 · 1 편) · [`benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode`](benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode.md) (같은 그룹 · 같은 해 · 양방향판 · 이 논문을 [26] · [36] 으로 인용) · [`benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem`](benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem.md) (같은 그룹 · 같은 해 · 이 논문을 [30] 으로 인용 = 후보 표 근거 카드) · [`alabdali2023_cgmd_wet_manufacturing_ssb_cathode`](alabdali2023_cgmd_wet_manufacturing_ssb_cathode.md) (ref [41] · 구조의 원 출처) · [`koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb`](koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb.md) (ref [6] · ΔV 입력) · [`mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation`](mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation.md) (SI [S4] · SE E) · [`xu2017_nmc532_nanoindentation_modulus_hardness_toughness`](xu2017_nmc532_nanoindentation_modulus_hardness_toughness.md) (SI [S8] · NMC ν) · [`dem_mechanical_stresses_ssb_electrode_cycling`](dem_mechanical_stresses_ssb_electrode_cycling.md) (ref [40] · 같은 그룹 DEM 사이클 응력) · [`taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode`](taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode.md) (ref [64] · 표 1) · [`sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps`](sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps.md) (ref [65]) · [`ngandjong2021_dem_calendering_digital_twin`](ngandjong2021_dem_calendering_digital_twin.md) (ref [45]) · [`neumann2021_garnet_3d_structure_grain_boundaries_li_transport`](neumann2021_garnet_3d_structure_grain_boundaries_li_transport.md) (ref [14]).
> **판독 원자료**: `litdb/figures/benhadjali2026_oneway_chemomech_stress_stack_pressure_3d_assb_cathode/digitized.csv` (239 행 — 그림 3b · 4 삽도 · 6a–d · 7b · 8a–b · 9) · 크롭 61 장 (도구 15 개 전부 다시 자름 = 그림 1–10 · 표 1 · 그림 S1–S2 · 표 S1 (SI 4–5 쪽 이어 붙임) · S2 + 패널 12 · 식 14 (식 1–13 하나씩 + 묶음 1) · 근거 문단 20) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 같은 그룹의 습식 제조 CGMD 모의가 만든 양극 구조 하나 (AM : Li₆PS₅Cl : CBD = 69 : 27.55 : 3.45 wt · AM 10 µm · 기공 ≈12 % · 압연 20 %) 를 CBD 겹침 부피를 AM · SE 로 옮기는 복셀화 + INNOV 메시로 COMSOL 에 넘겨, **AM 안 Fick 확산 (응력 항 없음 = 한 방향)** 이 정한 리튬 농도를 **NMC811 열팽창 꼴 고유변형 (Koerver 2018 ΔV 다시 그림 · ≈7 %)** 으로 바꾸어 **AM · SE · CBD 선형 탄성** 반쪽 셀 (분리막 · 집전체 강체 · 측벽 고정 · Li 금속 바깥면에 적층압) 을 C/5 · C/10 · C/20 방전 한 번 동안 풀었다 — 9 MPa 에서 반쪽 셀이 **0.78 · 1.61 · 2.53 %** 늘고 68 MPa 에서 **−0.08 · 0.74 · 1.82 %** (그림 7a [인쇄]), AM 평균 von Mises 는 DoD 와 함께 커져 끝에서 **318–463 MPa** [판독 그림 7b] · 68 MPa 가 늘 더 크며, 전압 곡선 차이는 ≤0.2 % [판독 그림 4 삽도] — **물성은 SI 표 S2 에만 있고 (SE E 18.5 GPa · ν 0.3 = Li₂S–P₂S₅ 유리 문헌값)**, 맞춘 값 · 실험 대조 · 소성 · 접촉 분리 · 탈압은 없다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 한 방향 결합의 정의 · 식 | *"electrochemistry drives mechanical deformations, while the mechanical field does not influence the electrochemical behavior"* (p.2) · 식 (3) μ = μ₀ + RT ln X − Ωσ_h 에서 응력 항을 지운 식 (4) → 식 (5) 순수 Fick · 단 **변형된 기하가 경로에 미치는 영향** 은 넣었다고 적음 (초록 · p.10 *"Mechanics → Microstructure → Electrochemistry"*) | [인쇄] p.2 · p.4 · p.10 · `eq_03` · `eq_04` · `eq_05` |
| ② ★ FEM 물성 (E · ν · ρ) | **SI 표 S2**: SE (Li₆PS₅Cl 이라 표기) E **1.85 × 10¹⁰ Pa** [S4 McGrogan 2017 = 70Li₂S–30P₂S₅ 유리] · ν **0.3** [S5 Sakuda 2013 J. Ceram. Soc. Jpn. = Li₂S–P₂S₅ 유리] · ρ 1.87 × 10³ (출처 없음) / NMC811 E **1.75 × 10¹¹ Pa** [S6 Sun & Zhao 2017 JPCC] · ν 0.3 [S7 · S8] · ρ 5.03 × 10³ [S3] / CBD E **3.5 × 10⁸ Pa** · ν **0.4** [S9 CMC/MWCNT 복합체] · ρ 0.92 × 10³ / Al E 7 × 10¹⁰ · ν 0.35 · ρ 2.7 × 10³ (단위 'Kg·m3' 인쇄 그대로) — 본문에는 숫자 없음 | [인쇄] SI p.6 · `tab_S2.png` |
| ③ ★ 입자 모의 → FEM 넘김 | §3.1 *"From Discrete to Continuum Modeling"*: 복셀화 후처리 · CBD–AM · CBD–SE 겹침 = CBD 부피를 줄여 AM / SE 에 더함 → *"transform the particles from spherical to irregular shapes"* · INNOV [47, 48] 다상 체적 메시 · **넘긴 것 = 기하만** (초기 조건 = 식 (13) c = c_min 하나 · 압연 응력 · 접촉력 · 되튐 서술 없음) · 복셀 크기 · 요소 수 · 메시 수렴 [미확인] | [인쇄] p.4 · p.5 · [미확인] |
| ④ 경계 조건 · 적층압 | 집전체 바깥면 고정 (*"u = θ0"* 인쇄) · 측면 고정 벽 (*"imitate the casing"*) · Li 금속 바깥면 외압 · **분리막 · 집전체 강체** · 9 · 68 MPa = *"provided by our industrial research collaborators as typical operating bounds"* | [인쇄] p.5–6 · 그림 3a |
| ⑤ 팽창 입력 | 그림 3b = Koerver 2018 [6] 의 NMC811 ΔV/V₀ 다시 그림 (x 0.146 → 0.907 · **−7.05 → −0.19 %** [판독]) · 식 (11) λ · 식 (12) Ω (농도 의존) — 이 카드 산술: 전 구간 선 변형 **λ = 0.0240** · 평균 Ω **≈1.93 cm³/mol** | [판독] · [카드 산술] §3-4 |
| ⑥ 두께 · 변위 결과 | C/5 *"≈0.43 μm … 0.98 % increase in electrode thickness"* · C/20 *"1.11 μm … 2.52 %"* (p.7) ↔ 같은 C/20 을 p.8 은 *"≈1.2 μm … ≈2.25 %"* · 그림 7a 9 MPa **0.78 · 1.61 · 2.53 %** · 68 MPa **−0.08 · 0.74 · 1.82 %** · 상별 (C/10 · 9 MPa) AM **4.49 %** · SE **0.45 %** · CBD **0.21 %** — % 의 기준 길이 [미확인] (§3-6: 인쇄 µm ÷ % = 43.9–44.05 µm ↔ 표 S1 양극 36.8 µm) | [인쇄] p.7–9 · [카드 산술] |
| ⑦ 응력 결과 | 그림 7b AM 평균 von Mises [판독]: DoD 0 (C/10) 에서 9 MPa ≈19 · 68 MPa ≈105 MPa → 끝 C/5 318 / 338 · C/10 356 / 358 · C/20 452 / 463 MPa (9 / 68) · 국소 최대 *"up to 3 GPa"* (C/5 · 그림 S2 · p.7) · 그림 5c 색 막대 0–2 GPa (포화) · SE · CBD 압력 지도 = 인장 (음) ↔ 압축 (양) 섞임 · 68 MPa 에서 압축 쪽으로 (그림 7c · 색 막대 ±50 · ±5 MPa 포화) | [판독] · [인쇄] p.7 · p.9–10 |
| ⑧ 미세구조 기술자 | AM–SE 비계면적 (C/10) +10–18 % · AM–CBD +1.5–8 % (변화 없음 대비 · 그림 8 [판독]) · 누적 기공 분포 (C/20 · 그림 9) · **SE 'geometric tortuosity' τ = 7.736 (변화 없음) · 8.182 (9 MPa) · 7.765 (68 MPa)** (C/10 끝 · GeoDict DiffuDict · p.11) — 면적 · 기공 · τ 계산법 [미확인] | [인쇄] p.10–12 · [판독] |
| ⑨ ★ DEM 한계 · 소성 · 차원 · 탈압 | (i) *"the spherical particle hypothesis … is inherently limited in representing realistic electrode microstructures"* (p.4) (ii) 소성 생략 근거 = NMC811 팽창 ≈7 % 로 *"modest"* · CBD · 기공이 변형을 줄여 *"the majority of the AM is expected to remain within the elastic regime"* · 비용 (p.4–5) · 결론에서 소성 · 접촉 상실 · 박리 = 다음 일 (p.12) · 표 1 *"Plasticity: No"* (iii) **3D** · 1D · 2D · 단일 입자 모델은 국소 불균일을 놓친다 (p.2) (iv) **탈압 없음** — 압연 되튐 · 적층압 제거 · 잔류 응력 낱말 0 회 | [인쇄] p.2–5 · p.12 · 표 1 |
| ⑩ 계산 비용 · 검증 | MatriCS 노드 하나 · **500 GB RAM · Xeon E5-2680 v4 28 코어** (p.4) · 실행 시간 · 요소 수 [미확인] · **실험 대조 0** (모델 검증 문장 없음 · *"consistent with experimental findings reported in the literature [65, 67]"* 정성 하나 · p.11) | [인쇄] p.4 · p.11 |

⛔ **한정어 (떼지 말 것)**: ① **SE 물성은 Li₆PS₅Cl 값이 아니다** — E 18.5 GPa · ν 0.3 의 원전은 70Li₂S–30P₂S₅ **유리** (McGrogan 2017 · 압입 ν 0.3 가정 [다른 카드]) 와 Li₂S–P₂S₅ 유리 (Sakuda 2013 JCSJ) · ρ 1.87 은 출처 없음 ② **AM 은 NMC811 로 매개변수만 붙였다** — 구조의 원 논문 (Alabdali 2023 [41]) 은 NMC622 [다른 카드] · 같은 구조의 앞 논문 [16] 도 NMC622 [다른 카드] ③ **모든 고체 선형 탄성 · 작은 변형 · 적합 메시** — 접촉 분리 · 미끄럼 · 재배열 · 소성 · 파괴 기구가 없다 → 저자가 쓰는 *"particle packing"* · *"contact loss"* · *"densification"* 은 이 모델이 계산할 수 있는 기전이 아니다 [카드 해석 · §11] ④ 응력 크기는 입력 E · 경계 (측벽 고정 · 강체 분리막) 에 매인다 — 색 막대 포화 · 최대값 = 국소 ⑤ 적층압 9 · 68 MPa 는 **사이클 중 작동압** — 우리 300 MPa 는 **성형압** (다른 단계) ⑥ % 기준 길이 · 메시 · 면적 · 기공 · τ 계산법 [미확인] · 같은 C/20 팽창이 2.52 % 와 ≈2.25 % 두 값으로 인쇄 ⑦ 실험 대조 없음.
⇒ **절대값 전이**: **응력 · 변위 · 두께 % 의 절대값 전이 불가** (선형 탄성 모델 값 · 유리 SE 물성 · 경계 조건의 함수 · 실험 대조 0).  옮길 수 있는 것: (a) **물성 표 그 자체** (E · ν · ρ 의 출처 사슬 — 특히 'SE = 18.5 GPa' 가 유리값이라는 사실) (b) **넘김 연산자의 꼴** (CBD 겹침 부피 재배정 · 기하만 · 응력 0 출발) (c) **방향 · 꼴** (적층압이 두께 팽창을 줄이고 AM 응력을 늘린다 · 고율에서 같은 DoD 응력이 크다) (d) 두 압력 차분이 C-rate 와 거의 무관 (0.71–0.87 %p) = 선형 겹침의 꼴 [카드 산술 §3-6].

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-42 의 '왜' 칸)

의도 원문 (`S8_candidates.md` N-42): *"h — '일방 결합 응력 (2 편) · ★ 그들 FEM 물성 (E · ν) 이 여기 있을 가능성' → DEM 미세구조 → FEM 응력 넘김의 정의 · 물성"* · 근거 칸 = `[b12 · benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem · L442]`.

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "일방 결합 응력" | **채움** | 정의 p.2 (*"one-way coupling approach, where electrochemistry drives mechanical deformations, while the mechanical field does not influence the electrochemical behavior"*) · 식 (3) → (4) → (5) (p.4 · *"our study is focused on coupling concentration to strain/stress not the other way around"*) · 응력 출력 = 그림 5c (AM von Mises · 끝 · 9 MPa) · 그림 7b (평균 · DoD · 9 / 68 MPa) · 그림 7c (SE · CBD 압력) · 그림 S2 (AM 압력 · C/5 · C/20) — 조건 = **방전 (리튬화) 한 번 · 적층압 누른 채 · 온도 [미확인] (T 는 식 (2) 기호뿐)** · 모델 값 (실험 아님) |
| "(2 편)" (가리킨 카드의 참고문헌 표에서 [29] = '같은 사슬의 1 편' 다음) | **채움** | 이 논문이 앞 전기화학 틀 [16] 을 잇는다고 적는다: *"the present work … extends our pre-existing electrochemical framework[16] by incorporating the lithiation-dependent volumetric expansion of NMC811 during a single discharge"* (p.3) · [16] = `benhadjali2025_…` (JPS 630, 236131) |
| "★ 그들 FEM 물성 (E · ν) 이 여기 있을 가능성" | **채움 (이 논문의 값) · 일부 (가리킨 논문의 값으로서)** | **SI 표 S2 (SI p.6)** 에 E · ν · ρ 가 있다 — SE 18.5 GPa · 0.3 · NMC811 175 GPa · 0.3 · CBD 0.35 GPa · 0.4 · Al 70 GPa · 0.35 (§3-2).  **본문에는 E · ν 숫자가 없다** (본문 'Young' 1 회 = *"Young's modulus and diffusion coefficient of the AM, were independent of the lithium-ion concentrations"* p.6 · 'Poisson' 0 회).  ⚠ 가리킨 카드의 논문 (WIP ↔ CUP · AM = NMC622) 이 **같은 값을 썼는지는 [미확인]** — 그 논문 본문에 E · ν 가 없고 (가리킨 카드 L244 · L413) 그 논문 표 S2 · S3 도 [미확인] · 이 논문의 AM 은 NMC811 (175 GPa · Sun & Zhao DFT) 이라 NMC622 판에 그대로 옮겨졌다고 볼 근거가 없다 |
| "DEM 미세구조 → FEM … 넘김의 정의" | **일부** | 넘긴 것은 **DEM 이 아니라 CGMD** (LAMMPS 거친 입자 분자동역학 · 힘장 = *"calibrated to match experimental observations"* p.3) 의 **압연 20 % 구조** · 정의 = §3.1 (복셀화 · CBD 겹침 부피를 AM / SE 에 더함 · INNOV 메시 · p.4) · 시점 = 압연이 끝난 구조 (압연 = 위 경계 등속 하강 · 아래 고정 · p.3) — 판을 뗐는지 · 되튐 · 이완 [미확인] (같은 구조의 앞 논문은 표 S1 두께 36.8 = 46 × 0.80 → 목표 두께 그대로 [다른 카드 `benhadjali2025_…` §3]) |
| "… FEM **응력** 넘김의 정의" | **없음** | 응력 · 접촉력 · 겹침량을 넘긴다는 문장이 없다 — 역학의 출발 조건은 식 (13) *"c = c_min at t = 0"* 하나뿐이고 적층압은 경계 조건으로 새로 건다 (p.5) · 'residual' · 'springback' · 'unload' · 'relax' 0 회 ⇒ **응력 0 출발 (기하만 넘김)** [카드 해석] |
| "· 물성" | **채움 (출처 사슬 포함)** | SI 표 S1 (전기화학 · SI p.4–5) · 표 S2 (역학 · SI p.6) — §3-2 · §3-3 · ⚠ SE 값은 유리 원전 · NMC811 밀도가 표 S1 (4.77 g·cm⁻³) 과 S2 (5.03 × 10³ kg·m⁻³) 에서 다르다 |
| 가리킨 카드의 **2 차 인용 값** (`benhadjali2026_wip_vs_cup_…` L442) | **같음 (숫자 인용 없음)** | 서지 *"S. Ben Hadj Ali, M. Alabdali, V. Viallet, V. Seznec, A.A. Franco, A New Three-Dimensional Microstructure-Resolved Model to Assess Mechanical Stress in Solid-State Battery Electrodes, Batteries & Supercaps 9 (2026) e202500540"* = 원문 첫 쪽 · 머리글과 같다 (본문 제목은 'Solid-State' · SI 제목은 *"Solid State"* — 하이픈만 다름) · 그 줄은 숫자를 옮기지 않았다 |
| (덧붙임) `benhadjali2026_fully_coupled_…` L400 · L407 (가리킨 카드 아님) | **같음 (서지)** · 관찰 하나 | [26] 서지 = 원문과 같음 · [36] = ChemRxiv 판 (이 PDF 로 확인 안 됨).  같은 카드 L28 *"한 방향 결합 = 같은 매개변수에서 응력 되먹임만 끈 판 ([36] · p.13)"* 은 그 논문 안의 비교 팔 이야기로 읽어야 한다 — 이 원문 ([36] 의 출판본) 은 **AM = NMC811 (≈7 %) · 적층압 9 / 68 MPa · 방전 한 번 · C/5–C/20** 이고 그 카드의 완전결합 판은 NMC622 (≈4.8 %) · 68 MPa · C/10 5 사이클 [다른 카드] — 매개변수가 같지 않다 (카드 문제 후보 · 고치지 않음 · 정독 출력 끝 절) |

⇒ **의도 대조 결과: 일부** — 한 방향 결합 응력 (정의 · 식 · 결과) 과 **물성 표 (E · ν · ρ — SI 표 S2)** 는 **있다**; 넘김의 정의는 **기하 (CGMD → 복셀 → 메시) 만** 있고 **응력 넘김은 없다** · 그 E · ν 가 가리킨 논문 (WIP ↔ CUP) 의 값인지는 [미확인] · SE E · ν 는 Li₆PS₅Cl 이 아닌 유리 원전.

---

## 1. 한 줄 요약
NMC811 은 리튬이 들어가면 부피가 ≈7 % 늘고 액체가 없는 전고체 양극에서는 그 팽창이 바로 응력 · 접촉 문제로 이어진다는 동기 (p.1–2) 에서, 같은 그룹이 습식 제조 CGMD 로 만든 양극 구조 (압연 20 %) 를 복셀 메시로 COMSOL 에 넘겨 **AM 안 확산 → 리튬 농도 → 열팽창 꼴 고유변형 → 선형 탄성 응력 · 변위** 를 한 방향으로 푼 첫 3D 사례라고 주장한다 (p.2 *"To the best of our knowledge, our work presented in this article represents the first attempt"*).  저율일수록 리튬화가 고르게 깊어져 반쪽 셀이 더 늘고 (9 MPa: C/5 0.78 → C/20 2.53 %), 68 MPa 적층압은 팽창을 줄이지만 (C/5 −0.08 % ~ C/20 1.82 %) AM 평균 응력을 늘린다 — 전압 곡선 차이는 작다 (한 방향이라).  응력 · 변형이 계면 비면적 (+10–18 %) · 기공 분포 · SE 굴곡도 (7.74 → 8.18 · 9 MPa / 7.77 · 68 MPa) 를 바꾼다는 *"Mechanics → Microstructure → Electrochemistry"* 를 결론으로 든다.  물성은 SI 표에만 있고, 소성 · 접촉 상실 · 박리 · 양방향 결합 · 실험 대조는 다음 일로 남겼다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| S. Ben Hadj Ali · M. Alabdali · V. Viallet · V. Seznec · A.A. Franco\* (LRCS · RS2E · ALISTORE-ERI · IUF) | *Batteries & Supercaps* 9 (2026) e202500540 · 14 쪽 + SI 7 쪽 | 10.1002/batt.202500540 | 모델: AM (전기화학 · 팽창 = **NMC811** · 구조는 NMC622 판 CGMD 구조 [다른 카드]) / **Li₆PS₅Cl** (이름만 · 역학 물성 = 유리 원전) / CBD (탄소 + 바인더 한 상 · *"carbon-binder-solvent domains"*) · 69 : 27.55 : 3.45 wt · 반쪽 셀 = Al 집전체 + 양극 + SE 분리막 + Li 금속 | **계산만** — CGMD 구조 재사용 → 복셀 메시 → COMSOL 3D FEM (전기화학 → 역학 한 방향) · GeoDict (τ) · 실험 없음 |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 구조 · 조성 · 넘김 (§2 · §3.1 · p.2–4 · `txt_p2_p3_cgmd_microstructure_source.png` · `txt_p3_extension_nmc811_20pct.png` · `txt_p4_voxelization_overlap_innov.png`)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 구조의 출처 | *"previously generated and reported[41] and further analyzed electrochemically in our own recent publication.[16]"* · CGMD · LAMMPS [43] · 슬러리 제조 → 건조 → 압연 (그림 2) | [인쇄] p.2 |
| 조성 | **AM : SE : CBD = 69 : 27.55 : 3.45** (*"weight formulation"*) · 탄소 · 바인더 구분 없음 (*"does not explicitly differentiate between the carbon and binder components"*) | [인쇄] p.2–3 |
| AM 입경 · 기공 | AM **10 µm** · **≈12 % porosity** (압연 20 % 구조) — ⚠ 같은 구조의 앞 논문 표 S1 = 13 % [다른 카드 `benhadjali2025_…` §3] | [인쇄] p.3 |
| 고체 부피 분율 (기공 제외) | ρ (표 S1 AM 4.77 · 표 S2 SE 1.87 · CBD 0.92 g/cm³) 로 **AM 43.90 · SE 44.71 · CBD 11.38 vol%** → 기공 12 % 를 넣으면 AM 38.6 · SE 39.3 · CBD 10.0 · 기공 12.0 % · ρ_AM 5.03 (표 S2) 이면 42.60 · 45.75 · 11.65 % · **랩 표준 SE 진밀도 1.64** 를 넣으면 41.31 · **47.98** · 10.71 % | [카드 산술: (w/ρ)/Σ(w/ρ)] |
| CGMD 힘장 | *"force fields that capture interparticle interactions and mechanical behavior, which were calibrated to match experimental observations"* — 값 · 보정 대상 이 논문에 없음 | [인쇄] p.3 · [미확인] |
| 압연 | *"applying a uniform downward displacement to the top boundary, compressing the electrode while the bottom surface remains fixed"* · 정도 = **20 % calendering degree** (= 두께 감소 · p.3) · 압력 · 되튐 [미확인] | [인쇄] p.3 |
| 복셀화 · 겹침 | *"overlaps between CBD and AM or between CBD and SE are handled based on adjusting the volume calculations by reducing the volume attributed to the CBD and adding this reduced volume to the AM or SE, respectively"* · *"implicitly considers the porosity of the CBD"* [46] · 결과 = *"transformation of the initially spherical particles into more realistic, irregular shapes for AM, SE, and CBD phases"* · AM–SE 겹침 규칙 [미확인] (이 논문 문장 없음) | [인쇄] p.4 |
| 메시 | INNOV [47, 48] (*"used to voxelize and reconstruct multiphase volumetric meshes for FEM calculations"*) · 복셀 크기 · 요소 종류 · 수 · 메시 수렴 [미확인] · 방전 중 *"the mesh is automatically refined by COMSOL based on the local strain field"* (C/10 · 9 MPa · 그림 S1 · p.6–7) | [인쇄] p.4 · p.6–7 |
| 상자 크기 · 양극 두께 | 표 S1 양극 두께 **L_C 36.8 µm** · 분리막 **L_SE 20 µm** · 집전체 **L_CC 10 µm** · Li 금속 두께 · 옆 치수 [미확인] (같은 구조의 앞 논문 41 × 41 µm · 완전결합판 그림 2a 40 × 40 µm · 양극 44.6 µm [다른 카드]) | [인쇄] SI p.4–5 · [미확인] |

### 3-2. ★ 역학 물성 — SI 표 S2 (SI p.6 · `tab_S2.png`)
| 상 | E (Pa · 인쇄) | ν | ρ (인쇄 단위 'Kg·m3') | 출처 (SI 참고문헌 그대로) | K · G · M [카드 산술] |
|---|---|---|---|---|---|
| SE: Li₆PS₅Cl | **1.85 × 10¹⁰** | **0.3** | 1.87 × 10³ | E [S4] McGrogan … Compliant Yet Brittle Mechanical Behavior of Li2S–P2S5 … Adv. Energy Mater. 2017, 7, 1602011 · ν [S5] Sakuda … Evaluation of Elastic Modulus of Li2S–P2S5 Glassy Solid Electrolyte … J. Ceram. Soc. Jpn. 2013, 121, 946–949 · ρ 출처 없음 | K 15.42 · G 7.12 · M 24.90 GPa |
| NMC811 | **1.75 × 10¹¹** | **0.3** | 5.03 × 10³ | E [S6] Sun & Zhao, J. Phys. Chem. C 2017, 121, 6002 (제목 *"Electronic Structure and Comparative Properties of LiNixMnyCozO2 Cathode Materials"*) · ν [S7] Wu & Lu JPCC 2017 · [S8] Xu … J. Electrochem. Soc. 2017, 164, A3333 · ρ [S3] Schmidt … CMAME 2023 | K 145.8 · G 67.3 · M 235.6 GPa |
| CBD | **3.5 × 10⁸** | **0.4** | 0.92 × 10³ | E · ν [S9] Dadfar & Kavoosi, Polym. Compos. 2015, 36, 145 (*"Carboxymethyl Cellulose/Multiwalled Carbon Nanotube Nanocomposites"*) · ρ 출처 없음 | K 0.583 · G 0.125 · M 0.750 GPa |
| Al 집전체 | 7 × 10¹⁰ | 0.35 | 2.7 × 10³ | [S10] Freund & Suresh 2004 (책) · ρ [S11] (책) | K 77.8 · G 25.9 GPa |
- [카드 산술] K = E/(3(1 − 2ν)) · G = E/(2(1 + ν)) · M (구속 탄성률) = K + 4G/3.  E 비: AM/SE **9.46** · AM/CBD **500** · SE/CBD 52.9.
- 원전 대조 [다른 카드]: `mcgrogan2017_…` = **70Li₂S–30P₂S₅ 용융 급랭 유리** · 큐브 코너 압입 · E **18.5 ± 0.9 GPa** · *"ν 0.3 가정"* → 이 논문의 SE E = 그 유리값 그대로 · ν 0.3 의 원전으로 든 [S5] 은 정본 카드 없음 (wishlist 에 이미 있음) · `xu2017_…` = **NMC532** 압입 E 142.5 ± 11.3 GPa ([S8] 은 ν 의 출처로만 인용) · NMC811 E 175 GPa 의 원전 [S6] 은 DFT 논문 (제목 · 카드 없음 · 값 [미확인]).
- 본문은 물성을 *"listed in Table S1 and S2"* 로만 가리킨다 (p.6) · E · D 는 리튬 농도와 무관하다고 둠 (p.6).

### 3-3. 전기화학 매개변수 — SI 표 S1 (SI p.4–5 · `tab_S1.png`)
| 항목 | 값 (인쇄 그대로) | 출처 |
|---|---|---|
| Li 음극 | α_a 0.5 · i₀,a **3 "A.cm-2"** · V₀ 0 V | — |
| SE (Li₆PS₅Cl) | L_SE **20 µm** (분리막) · δ_ion **0.7 "mS.cm-2"** | [S1] Bielefeld 2022 JES 169, 020539 |
| 양극 (*"NCM811"*) | L_C **36.8 µm** · i₀,c "See reference" (A·m⁻²) [S1] · α_c 0.5 · OCV "See reference" [S2] · D_AM "See reference" [S2] · C_spec **200 mAh·g⁻¹** · c_max **49 mol·l⁻¹** · ρ_NMC811 **4.77 g·cm⁻³** · δ_e,AM **100 S·m⁻¹** | [S1] · [S2] Ruess 2020 JES 167, 100532 |
| CBD | δ_e,CBD **200 S·m⁻¹** | — |
| 집전체 (Al) | L_CC **10 µm** · δ_e,CC **300 S·m⁻¹** · R_CC_AM = R_CC_CBD = **2 × 10⁻³ Ω·m²** | [S3] Schmidt 2023 |
- [카드 산술] c_max 49 mol/L · ρ 4.77 → 이론 용량 **275.3 mAh/g** (49 × 96485 / (3.6 × 4.77)) · C_spec 200 mAh/g = **35.6 mol/L** = c_max 의 0.73.  D_AM · OCV · i₀,c 의 숫자는 SI 에도 없다 ("See reference") [미확인].
- ⚠ 같은 SI 안 NMC811 밀도 둘: 4.77 g·cm⁻³ (표 S1) ↔ 5.03 × 10³ kg·m⁻³ (표 S2).

### 3-4. 팽창 입력 — 그림 3b · 식 (10)–(12) (p.5 · `fig_3b.png` · `eq_10_*` · `eq_11_*` · `eq_12_*`)
- 그림 3b = *"predefined volume expansion field applied on the AM phase (NMC811). Figure produced with data from Ref. [6]"* (Koerver 2018) · ΔV/V₀ vs x(Li) 26 점 [판독]: x 0.146 **−7.05 %** · 0.179 −6.09 · 0.208 −5.18 · 0.241 −4.26 · 0.268 −3.42 · 0.301 −2.71 · 0.454 −1.55 · 0.479 −1.38 · 0.609 −0.91 · 0.758 −0.47 · 0.907 **−0.19 %**.
- 원 논문과 대조 [다른 카드 `koerver2018_…` L117 · 판독 대 판독]: NCM-811 x ≈0.15 ≈−6.5 % · 0.19 ≈−5.7 % · 0.25 ≈−3.9 % · 0.46 ≈−1.4 % ↔ 이 그림의 같은 x 보간 −7.0 (0.146) · −5.74 · −3.98 · −1.51 % — 깊은 탈리튬 끝에서만 ≈0.5 %p 크다 · Koerver 의 인쇄 모델 입력은 *"roughly 6 % when charging to 4.3 V"* [다른 카드].  본문의 *"≈7%"* (p.4 · p.12) = 이 그림의 끝점.
- 식 (11) λ = (ΔV/V₀ + 1)^(1/3) − 1 · V_{x=xmax} = *"the initial (with minimum lithium content) unit cell volume"* (인쇄 그대로 — 'xmax' 라는 이름과 '최소 리튬' 이 엇갈림) · 식 (12) Ω = 3λ/((x − x_max)·C_total) · 식 (10) 고유변형 = ⅓ΔcΩI (*"analogously to thermal strain in thermoelasticity"*).
- [카드 산술] 그림 3b 양 끝 (x 0.146 → 0.907) 의 부피비 0.9981/0.9295 = 1.0738 → **λ = 0.02402** (선 변형 2.4 %) · 평균 **Ω = 3λ/(0.761 × 49 000 mol/m³) = 1.93 × 10⁻⁶ m³/mol (≈1.93 cm³/mol)** · ⅓ΔcΩ 를 같은 구간에 쌓으면 λ 로 되돌아온다 (검산).  초기 x (= c_min) 값 [미확인] (그림 6a 의 'SOC' 출발값 0.23–0.29 [판독] 과도 다름 — §3-6).
- 그림 2 (작업 흐름) 의 꼴은 다르다: *"Intercalation strain ε … ε = β × SOC … Expansion coefficient"* (선형 · β 값 없음) ↔ 식 (10)–(12) (농도 의존 Ω) — 그림 2 = 개념도 [카드 해석].

### 3-5. 전기화학 결과 (§4.1 · 그림 4 · p.6 · `fig_4a.png`–`fig_4c.png` · `txt_p6_three_conditions_stack_pressures.png`)
- 창 **2.6–4.2 V vs Li⁺/Li** · C/5 · C/10 · C/20 · 세 조건: (i) 부피 변화 없음 (*"the electrochemical framework previously reported by group[37] was applied"* — ⚠ [37] = von Kolzenberg · Latz · Horstmann (B&S 2022) · 같은 그룹 논문 아님) (ii) 부피 변화 + 9 MPa (iii) 부피 변화 + 68 MPa.
- 그림 4 삽도 [판독]: C/5 · 2.70 V 에서 9 MPa **112.81** · 68 MPa ≈112.97 · 변화 없음 ≈113.0 mAh/g (−0.17 · −0.03 %) / C/10 · 155.97 mAh/g 에서 9 MPa **2.701** · 변화 없음 2.713 · 68 MPa **2.716 V** / C/20 · 2.70 V 에서 변화 없음 **187.18** · 9 MPa 187.40 · 68 MPa **187.53 mAh/g** (+0.12 · +0.19 % [카드 산술]).
- 저자: *"the overall differences in discharge voltage and capacity across the three scenarios are relatively small. This limited variation can be attributed to the one-way coupling approach"* (p.6) · 68 MPa → *"slightly improved capacity, especially at lower C-rates"* · *"9 MPa is not always sufficient to compensate for expansion-induced degradation"* (p.6 — 이 모델에 열화 기구는 없다 [카드 해석]).
- [카드 추론] 한 방향인데도 차이가 생기는 경로 = 초록의 *"microstructural changes due to deformed geometries affecting the particles percolation paths"* (변형된 메시 위 수송) — 크기 ≤0.2 % [판독].
- DoD 끝 [판독 그림 6a] 57.8 (C/5) · 78.6 (C/10) · 94.5 % (C/20) ≈ 용량 ÷ C_spec 200 mAh/g (56.5 · 78.6 · 93.7 % [카드 산술]) → DoD 정의 = 비용량 / 200 mAh/g 으로 보인다 [카드 추론 · 정의 미인쇄].

### 3-6. ★ 변위 · 두께 · 상별 팽창 (§4.2 · §4.3 · 그림 5–7a · p.7–9)
| 양 | C/5 | C/10 | C/20 | 표지 · 쪽 |
|---|---|---|---|---|
| 본문 §4.2 (9 MPa) | **≈0.43 µm = 0.98 %** *"increase in electrode thickness"* | — | **1.11 µm = 2.52 %** | [인쇄] p.7 · `txt_p7_displacement_thickness_s2_peak.png` |
| 본문 p.8 (9 MPa · 그림 6b · 6d) | — | — | *"≈1.2 μm and a cathode expansion ratio of ≈2.25%"* | [인쇄] p.8 · `txt_p8_c20_expansion_phase_contribution.png` |
| 그림 5 최대 / 최소 변위 표지 (반쪽 셀 · 9 MPa · µm) | 0.428 / −0.0903 | 0.707 / −0.151 | 1.11 / −0.206 | [인쇄 그림 안 글자] |
| 그림 5 최대 변위 (AM · SE · CBD) | 0.424 · 0.428 · 0.428 | 0.680 · 0.707 · 0.707 | 1.07 · 1.11 · 1.11 | [인쇄 그림 안 글자] |
| 그림 7a 9 MPa *"The half-cell expand … from initial volume"* | **0.78 %** | **1.61 %** | **2.53 %** | [인쇄] 그림 7a · p.8 |
| 그림 7a 68 MPa | ***"shrink 0.08 %"*** | **0.74 %** | **1.82 %** | [인쇄] 그림 7a · p.8 |
| 9 → 68 MPa 차 | 0.86 %p | 0.87 %p | 0.71 %p | [카드 산술] |
| 겉보기 강성 59 MPa ÷ 차 | 6.86 GPa | 6.78 GPa | 8.31 GPa | [카드 산술 · 해석 = 같은 기준 길이의 변형률로 볼 때] |
| 그림 6b 분리막 z 변위 끝 (9 MPa) | 0.432 µm @DoD 59.7 | 0.659 @78.6 | 1.153 @98.1 | [판독 · 축 0 ↔ 1.3 직선 보정] (인쇄 눈금으로 읽으면 0.40 · 0.708 · 1.164) |
| 그림 6d 양극 팽창률 끝 (9 MPa) | 0.839 % @56.9 | 1.399 % @78.6 | 2.207 % @94.5 | [판독] |
- **기준 길이 (% 의 분모) [카드 산술]**: 인쇄 µm ÷ 인쇄 % = **43.88** (C/5 · 0.43/0.98 %) · **44.05** (C/20 · 1.11/2.52 %) · 43.91 (C/10 · 그림 5 0.707 ↔ 그림 7a 1.61 %) · 43.87 µm (C/20 · 1.11 ↔ 2.53 %) — 그런데 C/5 0.428 ↔ 0.78 % 는 **54.9 µm** · p.8 의 ≈1.2 ↔ ≈2.25 % 는 **53.3 µm** · 그림 6b ↔ 6d 같은 DoD 의 비는 **47.1 µm** (세 C-rate · 두 DoD 에서 47.0–47.6 · 축 위 끝을 1.2 로 보면 43.5) — **표 S1 L_C 36.8 µm 와 맞는 쌍이 없다** (36.8 이면 0.43 µm = 1.17 % · 1.11 µm = 3.02 %) · 반쪽 셀 66.8 µm (36.8 + 20 + 10) 과도 안 맞는다 · 완전결합판 그림 2a 양극 44.6 µm [다른 카드] 에 가장 가깝다 ⇒ **어느 길이로 나눴는지 [미확인]** · 그림 7a 의 C/5 0.78 % 는 §4.2 의 0.98 % 의 오식일 수 있다 [카드 추론].
- **같은 C/20 팽창이 둘**: 2.52 % (p.7) · 2.53 % (그림 7a) ↔ ≈2.25 % (p.8) · 그림 6d 끝 2.21 % [판독] — 12 % 차.
- **상별 (C/10 · 9 MPa · 그림 6c)**: AM **4.49 %** (*"at ≈80% DoD"*) · SE **0.45 %** · CBD **0.21 %** [인쇄 p.8 · 그림 끝 표지] · 곡선 [판독]: AM DoD 0 에서 이미 **0.347 %** → 20 % 0.61 → 40 % 1.11 → 60 % 2.15 → 79.8 % 4.48 % · SE 0.035 → 0.453 % · CBD 0 → 0.211 %.  저자: DoD < 40 % 에서 변화가 작은 것은 *"the elastic accommodation of lithium within the layered NMC811 structure"* (p.7) — 그림 3b 입력이 x 0.3–0.9 구간에서 평평한 것과 같은 꼴 [카드 해석].
- **그림 6a 'SOC'**: DoD 0 에서 **0.288 (C/5) · 0.257 (C/10) · 0.227 (C/20)** · 끝 0.975 (세 C-rate 모두 · DoD 는 57.8 · 78.6 · 94.5 %) [판독] — 끝값이 DoD 와 무관하게 같으므로 **평균 리튬화가 아니라 국소 (표면?) SOC** 로 보인다 · 본문 *"higher local state of charge (SOC) (Figure 6a)"* (p.8) · 정의 [미확인].
- 저자 해석: C/5 = *"The outer shell of the particles exhibits nearly complete lithiation, while the cores remain significantly less lithiated"* → 표면 팽창 · 전체 팽창은 작음 · C/20 = 고른 리튬화 → 가장 큰 팽창 (p.7–8) · 68 MPa 의 억제 = *"due to enhanced particle packing and improved interfacial contact"* (p.8) — 선형 탄성 · 적합 메시에는 재배열 · 접촉 변화가 없으므로 이 모델 안에서는 **탄성 압축의 겹침** 으로 읽힌다 (차 0.71–0.87 %p 가 C-rate 와 거의 무관) [카드 해석].

### 3-7. ★ 응력 (그림 5c · 7b · S2 · p.7 · p.9 · `fig_7b.png` · `fig_S2.png` · `txt_p9_vonmises_68mpa_amplification.png`)
| DoD (%) | C/5 9 / 68 MPa | C/10 9 / 68 MPa | C/20 9 / 68 MPa |
|---|---|---|---|
| 0 | — / — | **18.9 / 104.6** | — / — |
| 10 | 36.1 / 111.4 | 30.2 / 107.3 | 26.2 / 105.1 |
| 20 | 56.8 / 123.6 | 41.9 / 114.5 | 36.1 / 110.5 |
| 40 | 159.6 / 207.0 | 77.6 / 135.7 | 60.4 / 124.5 |
| 60 | → 끝 (곡선이 59–60 % 에서 끝남) | 182.2 / 222.3 | 105.1 / 154.2 |
| 80 | — | → 끝 (79.95 / 77.89 %) | 252.5 / 284.6 |
| 끝 | **317.9 (59.7) / 338.2 (59.2)** | **356.3 / 358.1** | **451.9 (98.2) / 463.1 (97.9)** |
- 전부 [판독] = **NMC811 안 평균 von Mises (MPa)** · 실선 9 MPa · 파선 68 MPa (색별 두 무리 · 추적으로 배정).
- [카드 산술] DoD 0 (C/10) 의 AM 평균 von Mises ÷ 적층압 = **2.10 (9 MPa) · 1.54 (68 MPa)** — 비례가 아니다 (두 점 직선 기울기 1.45 · 절편 5.8 MPa) · DoD 0 첫 점에 이미 AM 팽창 0.35 % (그림 6c) 가 들어 있다 [카드 추론].  68 MPa 의 증폭: DoD 40 % 에서 +47 (C/5) · +58 (C/10) · +64 MPa (C/20) → 끝에서 +20 · +2 · +11 MPa (팽창 응력이 지배하면 차가 준다).
- 같은 DoD 에서는 C/5 > C/10 > C/20 (*"particularly beyond 40% DoD"* p.9) · 끝값은 C/20 이 가장 크다 (깊이 리튬화) — 결론의 *"greater accumulation of mechanical stress over time at lower C-rates"* (p.12) 는 끝값 이야기 [카드 해석].
- 국소: 그림 5c 색 막대 **0–2 GPa** (포화 · 끝 · 9 MPa) · 그림 S2 C/5 압력 *"peak stress values reach up to 3 GPa, predominantly at the particle surfaces"* (p.7) — 그림 S2 색 막대는 **±300 MPa** 라 3 GPa 를 그림에서 읽을 수 없다 [판독] · 그림 2 개념도 색 막대 −200…800 MPa.
- 저자: 68 MPa = *"increases the elastic energy stored in the AM particles, potentially elevating the risk of mechanical failure"* (p.9) · *"maximum stress values and the degree of stress heterogeneity may play a decisive role in local fracture initiation"* (p.10) — 파괴 모델은 없다.

### 3-8. SE · CBD 압력 지도 (그림 7c · p.10 · `txt_p10_se_cbd_pressure_sign_tension.png`)
- *"a complex pattern of tensile (negative pressure) and compressive (positive pressure) regions"* · 인장 → *"vulnerable to cohesion loss, potentially leading to interfacial delamination from AM particles"* · 과한 압축 → *"local densification, which may hinder lithium transport"* · *"An overall transition from tensile to compressive stresses is observed in the SE and CBD phases with increasing stack pressure"* (p.10).
- 색 막대 [판독]: CBD **−5 … +5 MPa** · SE **−50 … +50 MPa** (양끝 포화) · 끝 · C-rate 표기 없음 (본문 *"at the end of discharge"*) · 분포 숫자 · 부피 분율 [미확인].
- 부호 규약 = COMSOL 'pressure' (압축 양) [카드 해석 · 원문은 괄호 설명만].

### 3-9. 계면 비면적 (그림 8 · §5.1 · p.10 · `fig_8a.png` · `fig_8b.png` · `txt_p10_interfacial_area_dod.png`)
| DoD (%) | AM–SE 변화 없음 · 9 · 68 MPa (m²/g) | AM–CBD 변화 없음 · 9 · 68 MPa (m²/g) |
|---|---|---|
| 20 | 0.3626 · 0.4125 (**+13.8 %**) · 0.4132 (+14.0 %) | 0.4123 · 0.4257 (+3.3 %) · 0.4399 (+6.7 %) |
| 40 | 0.3626 · 0.4002 (+10.4 %) · 0.4187 (+15.5 %) | 0.4123 · 0.4183 (+1.5 %) · 0.4389 (+6.5 %) |
| 60 | 0.3626 · 0.4095 (+12.9 %) · 0.4271 (**+17.8 %**) | 0.4123 · 0.4239 (+2.8 %) · 0.4451 (+8.0 %) |
- [판독] 막대 위끝 (y 축은 0.36 · 0.355 부터 시작 — 막대 높이로 비를 읽으면 안 된다) · C/10 (그림 안 글자) · 단위 *"m'g⁻¹"* · *"m²g⁻¹"* (인쇄 그대로) · 캡션 *"in function of SOC"* ↔ 축 *"Depth of dicharge (%)"*.
- [카드 산술] (1) 부피 변화 없음의 AM–SE + AM–CBD = **0.775 m²/g** ↔ 지름 10 µm 구 (*"AM particle size of 10 μm"* 를 지름으로 · ρ 4.77) 의 비표면적 6/(ρd) = **0.126 m²/g** → **6.2 배** — 정규화 (무엇의 g 인지) · 면적 계산법 [미확인] (2) 20 % DoD 의 AM 부피 증가 0.61 % [판독 그림 6c] 가 면 그대로 늘린다면 표면적 +0.41 % (부피^⅔) — 보고된 +13.8 % 는 그 ≈34 배 · 60 % DoD (AM +2.15 %) 에서도 기하 기대 +1.4 % ↔ +12.9 · +17.8 % ⇒ 면적이 **접촉 판정 (틈 문턱 · 다시 복셀화)** 으로 셈해졌을 가능성 [카드 추론 · 방법 미인쇄].
- 저자 해석: 40 % DoD 9 MPa 의 감소 = *"a loss of AM–SE and AM–CBD contact due to the larger AM expansion"* · 68 MPa = *"restores interfacial contact"* (p.10) — 적합 메시 선형 탄성에는 분리 · 재접촉 기구가 없다 [카드 해석 · §11].

### 3-10. 누적 기공 분포 (그림 9 · §5.2 · p.10–11 · `txt_p10_p11_pore_size_distribution.png`)
| 지름 (µm) | 0.2 | 0.6 | 1.0 | 1.4 | 1.8 | 2.2 | 2.6 | 3.0 | 끝 |
|---|---|---|---|---|---|---|---|---|---|
| 변화 없음 | 0.186 | 0.494 | 0.773 | 0.883 | 0.958 | 0.987 | 0.997 | 1.000 | — |
| 9 MPa | 0.134 | 0.352 | 0.644 | 0.807 | 0.917 | 0.965 | 0.983 | 0.994 | 1.000 (4.6) |
| 68 MPa | 0.116 | 0.341 | 0.652 | 0.833 | 0.943 | 0.983 | 0.995 | 0.997 | — |
- [판독] 정규화 누적 (각 곡선 끝 = 1) · C/20 (캡션) · 겹친 표지 일부는 눈 판독 (digitized.csv note).  [카드 산술] 중앙 지름 **0.61 → 0.80 (9 MPa) · 0.80 µm (68 MPa)** — 팽창 판에서 작은 기공의 **몫** 이 줄어 분포가 **큰 쪽으로** 옮겨졌다.
- 저자: 9 MPa 에서 *"small and intermediate pores (0.2–2.6 μm) are significantly reduced and shifted toward smaller diameters, while larger pores (3–4.6 μm) are preserved"* · 68 MPa *"the disappearance of larger pores (>3 μm) and the reduction in smaller pore volume fractions (<=1.4 μm) point to enhanced densification"* (p.10–11) — 'smaller diameters 쪽' 은 그림의 꼴과 반대 [판독 · 카드 해석] · 변화 없음 판에도 3 µm 넘는 기공이 없다 (3.0 에서 1.000) → '사라짐' 은 9 MPa 대비 · 9 MPa 판의 3–4.6 µm 기공은 원 구조에 없던 크기 — 분리 기구가 없는 연속체에서 기공이 커지는 경로 · 총 기공 부피 · 계산 도구 [미확인].
- *"consistent with experimental findings reported in the literature,[65,67]"* (p.11) — [65] Sakka 2022 (`sakka2022_…`) · [67] Yamamoto 2020 (카드 없음) — 정성 문장뿐 · 숫자 대조 없음.

### 3-11. SE 굴곡도 τ (그림 10 · §5.3 · p.11–12 · `fig_10.png` · `txt_p11_p12_tortuosity_values.png`)
- *"geometric tortuosity (τ) of the SE phase, which quantifies the effective pathway length for Li⁺ transport through the contiguous SE network"* · C/10 방전 한 번 뒤 · **GeoDict 2024 DiffuDict** (Math2Market) · *"using a standard desktop computer"* · 변화 없음 **τ = 7.736** · 9 MPa **8.182** (+5.8 % [카드 산술]) · 68 MPa **7.765** (+0.4 %) [인쇄 p.11].
- **정의식 · 방향 · 경계 조건이 이 논문에 없다** [미확인].  같은 그룹 1 편은 τ_g = √(φ_SE/D_eff) 를 인쇄 [다른 카드 `benhadjali2025_…` L131] — 이 논문도 같으면 우리 **tau** (√tau2) 이고 tau2 (수송 tortuosity) = **59.8 · 67.0 · 60.3** [카드 산술 · 정의 가정].
- ⚠ **같은 '압연 20 %' 구조의 바탕 τ 가 다르다**: 이 논문 7.736 (변화 없음 · 방전 뒤) ↔ 1 편 Cal20 τ_g **6.21** [판독 · 다른 카드] ↔ 원 구조 논문 **6.1** [다른 카드 `alabdali2023_…` 판독] — 24–27 % 차 · 이유 (메시 · 상 정의 · 방전 뒤 기하) 원문 설명 없음.
- 저자 해석: 9 MPa 는 *"cannot sufficiently counteract the expansion of the AM. This expansion constricts SE pathways"* · 68 MPa 는 *"maintains interparticle contact and preserves SE continuity during lithiation"* (p.11–12).

### 3-12. 계산 · 하드웨어 (p.4 · `txt_p4_comsol_halfcell_hardware.png`)
- COMSOL Multiphysics · 반쪽 셀 (3D 양극 + SE 분리막 + Li 금속 음극 + Al 집전체) · 방전 한 번 (AM 리튬화) · MatriCS (UPJV) **노드 하나 · 500 GB RAM · 프로세서 하나 (Intel Xeon E5-2680 v4 @ 2.40 GHz · 28 코어)** · 실행 시간 · 자유도 · 시간 간격 · 수렴 기준 [미확인] · τ 는 *"standard desktop computer"* (p.11).
- 저자: *"although more computationally intensive, the 3D framework provides a more accurate description"* (p.4) · 소성을 빼면 *"keeping the computational cost manageable"* (p.5).

---

## 4. ★ 방법 — 사슬 · 식 · 경계

### 4-1. 사슬 (그림 2 · p.2–5)
CGMD 습식 제조 (LAMMPS · 슬러리 → 건조 (탄소-바인더-용매 영역이 줄어 CBD) → 압연 20 %) [41, 16] → **복셀화 후처리** (CBD 겹침 부피 → AM / SE · 구 → 불규칙 모양) → **INNOV** 다상 체적 메시 → **COMSOL** 반쪽 셀 (Li 금속 | SE 분리막 20 µm | 양극 | Al 집전체 10 µm) → (전기화학 [16] 틀) AM 안 Fick 확산 (식 1–5) → 리튬 농도 → 고유변형 (식 10–12 · 그림 3b) → 준정적 평형 · 선형 탄성 (식 6–9) · 적층압 경계 → 출력 (변위 · von Mises · 압력 · 두께) → (변형된 기하) → 계면 비면적 · 기공 분포 · GeoDict τ.
- **넘김 시점 · 상태**: 압연이 끝난 CGMD 구조 · 응력 0 출발 · 압연 압력 · 되튐 · 판 분리 [미확인] — 우리 '성형 → 탈압 → 수송' 사슬에서 **탈압 단계를 건너뛴 넘김**.

### 4-2. ★ 지배식 (p.4–5 · 크롭 `eq_01_li_conservation_in_am.png` … `eq_13_initial_condition_cmin.png` · 묶음 `eq_01_13_governing_set.png`)
| 식 | 인쇄 | 뜻 · 비고 |
|---|---|---|
| (1) | ∂c/∂t + ∇·J = 0 | AM 안 리튬 보존 (Fick [50]) |
| (2) | J = −(D/RT) c ∇μ | 화학-기계 퍼텐셜 기울기 흐름 [51] |
| (3) | μ = μ₀ + RT ln X − Ωσ_h | 응력 의존 화학 퍼텐셜 (σ_h = 정수압 응력 · X = 몰 분율 · Ω = 부분 몰 부피) — *"The third term … results from the fully stress–concentration coupling"* |
| (4) | μ = μ₀ + RT ln X | **한 방향**: 응력 항 지움 [52] |
| (5) | ∂c/∂t − D∇²c = 0 | 순수 Fick — 인쇄는 *"Combining Equations (2) and (3)"* (실제로는 (1) · (2) · (4)) |
| (6) | ∇·σ + F_b = 0 | 준정적 평형 · F_b = 0 [53] |
| (7) | σ = C : ε_e | 후크 법칙 (인쇄 *"Hook's law"*) · AM · SE · CBD 모두 선형 탄성 [61] |
| (8) | ε_t = ε_e + ε_int = ½((∇u)ᵀ + ∇u) | 작은 변형 · 고유변형 더하기 — 다음 문장은 ε_e 를 *"total"* 이라 잘못 부름 |
| (9) | ε_e = ε_t − ε_int | 탄성 변형 [51] |
| (10) | 인쇄 **ε_e** = ⅓ Δc Ω I | 왼쪽은 **ε_int** 여야 한다 (열변형 꼴 [62, 63]) · Δc = 현재 − 초기 농도 |
| (11) | λ = (ΔV/V₀ + 1)^(1/3) − 1 = ((V_{x=x} − V_{x=xmax})/V_{x=xmax} + 1)^(1/3) − 1 | 단위 격자 부피 → 선 변형 (그림 3b 자료) |
| (12) | Ω = 3λ / ((x − x_max) C_total) | 농도 의존 부분 몰 부피 |
| (13) | c = c_min at t = 0 | 초기 조건 (AM 전체 균일) — **역학의 초기 응력 · 변위 조건은 인쇄되지 않음** |
- 전기화학 (BV · SE · CBD 옴 · 계면 저항) 식은 이 논문에 없다 — [16] (`benhadjali2025_…`) 의 틀 · 매개변수는 표 S1.
- 저자의 단순화 이유: *"This intentional simplification allows us to isolate and analyze the mechanical response to electrochemical processes in a controlled and computationally tractable manner. While it neglects mechanisms such as stress-assisted lithium transport and its impact on kinetics …"* (p.4 · `txt_p4_oneway_simplification.png`).

### 4-3. 경계 · 초기 조건 (§3.2.2 · 그림 3a · p.5–6 · `fig_3a.png` · `txt_p5_p6_bc_rigid_separator_si_tables.png`)
- *"Fixed support (u = θ0) for x, y, and z axes was applied at the external surface of the cathode CC"* (인쇄 θ0) · *"The green rectangles indicate fixed walls constraints, which were used to imitate the casing in actual ASSB implementation that may suppress the electrode expansion"* (그림 3a: 분리막 · 양극 · 집전체 옆면) · *"An external pressure was applied at the external surface of the Li metal"* (그림 3a 2D 단면은 SE 윗면에 'Stack pressure' 화살표).
- *"The separator and the CC were considered as rigid body domains"* · *"Treating the SE as a rigid, nondeformable domain allows us to focus computational resources on the mechanical response within the active and composite phases"* (분리막 SE) ↔ 같은 쪽의 *"AM, SE, and CBD phases are treated as linear elastic materials"* (양극 안 SE) — 'SE' 낱말이 두 영역에 같이 쓰였다 · *"The mechanical contribution of the SE will be addressed in our future work"* (p.6).
- E · D 는 리튬 농도와 무관 (p.6) · 옆면 = 고정 벽 (주기 경계 아님 · 'periodic' 0 회).

### 4-4. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM (구 입자) 한계 진술** (p.4 · `txt_p4_spherical_hypothesis_limit.png`): *"It is worth noting that while the spherical particle hypothesis has been widely used to investigate electrochemical behavior due to its computational simplicity, it is inherently limited in representing realistic electrode microstructures. The 3D-resolved microstructure model adopted here allows for the inclusion of irregular particle geometries, polydispersity, and anisotropic connectivity of both solid and pore phases. These features are critical in governing localized ionic transport, current distribution, and mechanical stress concentrations, none of which can be adequately captured by idealized spherical approximations."* — ⚠ 그들의 '불규칙 모양' 은 역학이 아니라 **겹침 부피 재배정 (기하 후처리)** 의 결과 (§3-1) · DEM 선행 [38] (So 2025 · 실리콘 · 표 1 *"DEM · 3D · Plasticity Yes · Irregular particle shape No"*) · 같은 그룹 DEM [40] (사이클 뒤 응력 · p.2) · 겹침 상한 · 밀도 · 연화 언급 없음.
- **(ii) 소성 · 큰 변형을 넣지 않은 이유 · 우회 · 비용** (p.2 · p.4–5 · p.12 · `txt_p4_p5_elastic_regime_linear_elastic.png` · `txt_p12_conclusions_small_strain_plasticity.png`):
  - 선행 비판: *"Others incorporate both electrochemistry and solid mechanics but rely on linear elasticity assumptions,[17–25] which may not be valid for materials that experience volume changes exceeding several hundred percent during full lithiation"* (p.2).
  - 자기 정당화: *"The NMC811 material is considered to undergo a relatively modest volume expansion (≈7%), and in the composite electrode environment, the surrounding carbon binder along with porosity and microstructural heterogeneity help limit effective strain levels.[54,55] As a result, the majority of the AM is expected to remain within the elastic regime.[18,56] Moreover, this assumption is widely adopted in battery modeling studies, even for materials with much larger expansions like Silicon,[57–60] as it enables analysis of stress evolution while keeping the computational cost manageable."* (p.4–5) — 응력 크기 (국소 *"up to 3 GPa"* · 평균 318–463 MPa) 를 항복 · 파괴 기준과 견준 문장은 **없다**.
  - 결론: *"The assumption of small deformations was justified based on the limited volumetric expansion of the AM relative to its particle size, allowing us to effectively model the system within a linear elasticity framework. However, to capture more complex mechanical behaviors such as plastic deformation, contact losses, and interfacial debonding, our future work will focus on developing a fully coupled nonlinear model that incorporates plasticity and more advanced constitutive laws"* (p.12).
  - 표 1 *"This study · FEM · Solid-state lithium ion battery · 3D · Plasticity No · Manufacturing simulation of composite cathode · Carbon and binder Yes · Irregular particle shape Yes"* (p.3).
  - 우회 = **소성을 빼고 SE · CBD 도 선형 탄성** · 맞춘 값 0 (물성 = 문헌 · 유리 원전) · 비용 = 노드 하나 500 GB · 28 코어 (시간 [미확인]).
- **(iii) 차원**: 계산 = **3D** (*"4D-resolved"* = 3D + 시간) · 선행 1D [32] · 2D [33, 34] · 단일 입자 [35–37] 은 *"thereby overlooking crucial local heterogeneities in current density, lithium concentration, and mechanical stress distributions"* (p.2) · 2D → 3D 전이의 정량 진술 없음 · 표 1 에 1D/2D 셋 ([25] · [64] · [39]).
- **(iv) 압력을 뺄 때**: **다루지 않음** — 압연 되튐 · 적층압 제거 · 잔류 응력 · 이완 ('unload' · 'residual' · 'relax' · 'release' · 'springback' 0 회) · 방전 한 번 (충전 · 사이클 없음) → 리튬이 빠질 때의 수축 · 응력 반전도 없다 (같은 그룹 완전결합판이 다룸 [다른 카드]).

### 4-5. 기법 미니 용어집
- **한 방향 결합 (one-way coupling)** = 전기화학 → 역학만 (리튬 농도가 변형을 만들고 응력은 확산 · 반응을 바꾸지 않음) · 양방향 (two-way · full) = 응력이 화학 퍼텐셜 · 평형 전위를 되바꾼다.
- **고유변형 (intercalation / eigenstrain)** = 응력 없이 저절로 생기는 변형 (리튬 함량 → 격자 부피) · 열팽창처럼 총 변형에서 빼고 남은 탄성 변형만 응력을 만든다.
- **부분 몰 부피 Ω** = 리튬 1 mol 이 들어갈 때 늘어나는 부피 — 식 (12) 는 단위 격자 부피 자료 (그림 3b) 에서 Ω(x) 를 만든다.
- **von Mises 응력** = 모양을 바꾸는 (편차) 응력의 크기 · 압력 (정수압) 과 다르다 — 항복 판정에 쓰는 양 (이 논문은 항복을 쓰지 않는다).
- **COMSOL 'pressure'** = −(σ₁₁ + σ₂₂ + σ₃₃)/3 · 압축이 양 · 음수 = 인장.
- **적층압 (stack pressure)** = 셀을 쓸 때 위아래로 거는 작동 압력 (9 · 68 MPa) — 성형압 (우리 300 MPa) 과 다른 단계.
- **DoD (depth of discharge)** = 방전 깊이 — 이 논문 정의 미인쇄 (용량 ÷ 200 mAh/g 과 맞음 [카드 추론]).
- **비계면적 (specific interfacial area)** = 질량당 상 사이 맞닿은 면적 (m²/g).
- **INNOV** = 같은 그룹의 복셀화 · 다상 체적 메시 도구 · **GeoDict DiffuDict** = 복셀 구조 위 확산 해로 유효 확산 · 굴곡도를 내는 상용 모듈.
- **구속 탄성률 M** = 옆을 막은 일축 압축의 응력 ÷ 변형률 = K + 4G/3 — 측벽 고정 셀의 두께 응답은 E 가 아니라 M 에 가깝다.

---

## 5. Figure set ★
| Fig / 크롭 | 내용 | 우리 활용 |
|---|---|---|
| 1 (`fig_1.png`) | AM–SE · AM–CBD 접촉 면의 가능한 역학 현상 개념도 | 열화 기전 목록 (정성) |
| 2 (`fig_2.png`) | 작업 흐름: 슬러리 → 건조 → 압연 → 메시 → 전기화학 · 역학 (*"ε = β × SOC"* 개념 · 색 막대 −200…800 MPa) | 넘김 사슬 그림 (R 계획의 '성형 → 넘김' 자리) |
| 표 1 (`tab_1.png`) | 선행 비교 (방법 · 계 · 차원 · 소성 · 구조 출처 · 탄소/바인더 · 불규칙 모양) — 이 논문 = FEM · 3D · Plasticity **No** | ★ 질문 k · l 의 표 근거 · DEM 선행 [38] 은 소성 Yes · 불규칙 No |
| 3 (`fig_3.png` · `fig_3a.png` · `fig_3b.png`) | (a) 경계 조건 (Li 금속 · SE · 양극 · 집전체 · 고정 벽 · 고정 지지 · 적층압) (b) NMC811 ΔV/V₀ vs x (Koerver 다시 그림) | ★ 경계 등록 꼴 · 팽창 입력 (§3-4) |
| 4 (`fig_4.png` · `fig_4a`–`fig_4c`) | C/5 · C/10 · C/20 방전 곡선 세 조건 + 확대 삽도 | 한 방향 결합의 전기화학 영향 ≤0.2 % [판독] |
| 5 (`fig_5.png`) | 끝 (9 MPa) 의 Li 농도 · z 변위 (AM · SE · CBD · 반쪽 셀 · 최대 / 최소 글자) · von Mises (0–2 GPa) | 변위 인쇄값 (§3-6) · 색 막대 포화 |
| 6 (`fig_6.png` · `fig_6a`–`fig_6d`) | (a) 'SOC' vs DoD (b) 분리막 z 변위 (눈금 글자 불균일) (c) 상별 부피 팽창 (C/10) (d) 양극 팽창률 | ★ 상별 팽창 AM 4.49 · SE 0.45 · CBD 0.21 % · 기준 길이 문제 (§3-6) |
| 7 (`fig_7.png` · `fig_7b.png`) | (a) 9 / 68 MPa 반쪽 셀 팽창 % (그림 안 글자) (b) AM 평균 von Mises vs DoD (c) SE · CBD 압력 지도 (±50 · ±5 MPa) | ★ 적층압 효과 · 두 압력 차분 (§3-6 · §3-7) |
| 8 (`fig_8.png` · `fig_8a` · `fig_8b`) | AM–SE · AM–CBD 비계면적 (C/10 · DoD 20 · 40 · 60) + 3D 렌더 | 계면 지표 (계산법 [미확인]) |
| 9 (`fig_9.png`) | 누적 기공 부피 분율 vs 평균 기공 지름 (C/20 · 세 조건) | 기공 분포 꼴 (정규화 · 총량 [미확인]) |
| 10 (`fig_10.png`) | SE 'geometric tortuosity' 세 점을 이은 선 그림 (7.736 · 8.182 · 7.765 · y 축 7.5–8.5) | τ 규약 (§7-5) |
| S1 (`fig_S1.png`) | 9 MPa NMC811 팽창 뒤 변형 기하 · 변형 메시 (AM · SE · CBD) | 변형 따라 다시 메시 (U6 꼴 참고) |
| S2 (`fig_S2.png`) | C/5 · C/20 AM 압력 분포 (색 막대 ±300 MPa) | 국소 응력 (본문 3 GPa 와 색 막대 불일치) |
| 표 S1 (`tab_S1.png` · SI 4–5 쪽 이어 붙임) | 전기화학 매개변수 | §3-3 |
| 표 S2 (`tab_S2.png`) | ★ 역학 물성 (E · ν · ρ · 출처) | §3-2 · 의도 ② |
| 식 크롭 14 장 | `eq_01_li_conservation_in_am` · `eq_02_flux_chemomechanical_potential` · `eq_03_stress_dependent_chemical_potential` · `eq_04_potential_without_stress_term` · `eq_05_fick_diffusion_oneway` · `eq_06_mechanical_equilibrium` · `eq_07_hooke_law` · `eq_08_total_strain_small_strain` · `eq_09_elastic_strain_split` · `eq_10_intercalation_strain_as_printed` · `eq_11_volumetric_strain_lambda` · `eq_12_partial_molar_volume` · `eq_13_initial_condition_cmin` · `eq_01_13_governing_set` | 보고서 사이클 응력 절에 붙일 지배식 (식 10 인쇄 오기 표지 그대로) |
| 근거 문단 20 장 | `txt_p2_prior_models_oneway_definition` (선행 · 한 방향 정의) · `txt_p2_p3_cgmd_microstructure_source` (구조 출처 · 조성) · `txt_p3_extension_nmc811_20pct` (NMC811 팽창 확장 · 20 %) · `txt_p4_voxelization_overlap_innov` (겹침 재배정 · INNOV) · `txt_p4_spherical_hypothesis_limit` (★ k) · `txt_p4_comsol_halfcell_hardware` (반쪽 셀 · 500 GB) · `txt_p4_oneway_simplification` (식 4–5 · 단순화) · `txt_p4_p5_elastic_regime_linear_elastic` (★ l) · `txt_p5_p6_bc_rigid_separator_si_tables` (경계 · 강체 · 표 S1 · S2) · `txt_p6_three_conditions_stack_pressures` (세 조건 · 9 / 68 MPa 출처) · `txt_p6_p7_strain_based_remeshing` (변형 기반 다시 메시) · `txt_p7_displacement_thickness_s2_peak` (0.43 µm · 0.98 % · 1.11 µm · 2.52 % · 3 GPa) · `txt_p8_c20_expansion_phase_contribution` (≈1.2 µm · ≈2.25 % · 상별) · `txt_p8_p9_stack_pressure_thickness_change` (0.78 · 1.61 · 2.53 · −0.08 · 0.74 · 1.82 %) · `txt_p9_vonmises_68mpa_amplification` (68 MPa 응력 증폭) · `txt_p10_se_cbd_pressure_sign_tension` (인장 · 압축) · `txt_p10_interfacial_area_dod` (계면 · 접촉 상실 해석) · `txt_p10_p11_pore_size_distribution` (기공 분포 문장) · `txt_p11_p12_tortuosity_values` (τ 값 · DiffuDict) · `txt_p12_conclusions_small_strain_plasticity` (★ 작은 변형 · 소성 다음 일) | 원문 인용용 |

## 6. Post-processing ★
- **무엇을**: COMSOL 출력 → 끝 상태 Li 농도 · z 변위 · von Mises (3D 지도) · 분리막 z 변위 · 상별 · 양극 부피 팽창률 · AM 평균 von Mises (DoD 함수) · SE · CBD 압력 지도 · 비계면적 (DoD 20 · 40 · 60) · 누적 기공 분포 (C/20 끝) · GeoDict τ (C/10 끝).
- **안 한 것**: 메시 수렴 · 시간 간격 시험 · RVE 크기 시험 · 반복 (시드) · 응력 분포 통계 (백분위 · 부피 분율) · 항복 · 파괴 판정 · 실험 대조 · 탈압 · 충전 (탈리튬) · 다중 사이클 · 기공률 숫자 (변형 뒤) · τ 정의식.
- **이 카드의 후처리**: 원 래스터 판독 (그림 3b · 4 삽도 · 6a–d · 7b · 8a–b · 9 · 239 행 · 범례 제외 · 7b 는 색별 두 무리를 실선 / 파선으로 추적 배정 · 6b 는 눈금 글자가 고른 간격의 반올림 (1.3/6 = 0.2167 µm 의 배수) 이라 직선 보정 + 인쇄 눈금 판독 둘 다) · 부피 분율 · K · G · M · λ · Ω · 이론 용량 · 기준 길이 · 두 압력 차분 · 표면적 기대값 · 중앙 기공 지름 · 상대 변화 [카드 산술].

---

## 7. 우리 DEM+MPM 대비 (우리 수치 = CLAUDE.md · 정본 카드 병기)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 단계 | 사이클 (방전 한 번) 중 리튬화 팽창 · 작동 적층압 9 / 68 MPa | 성형 (300 MPa 일축) → (탈압 = 계획) → 수송 (STEP3 · STEP4) · 사이클 접촉 원장 (A10) | 다른 단계 — 그들은 우리 사슬의 **성형 뒤 · 사이클 쪽** 에 있다 |
| 구조 출처 | CGMD (거친 입자 MD · 습식 · 압연 20 %) | DEM (LIGGGHTS · 건식 분말 · 300 MPa) · MPM 은 DEM 골격 위 | 둘 다 '입자 모의 → 연속체' — 그들은 기하만 · 응력 0 출발 · 우리 MPM scaffold 도 DEM 압축 끝 좌표 (CLAUDE.md 2026-06-16) |
| 넘김 연산자 | 복셀화 · CBD 겹침 부피 → AM / SE · INNOV 메시 | DEM 구 → MPM 물질점 (SE 씨앗 = DEM 좌표) · STEP3 복셀 | 겹침 처리 규칙을 숫자로 남기는 꼴은 우리 쪽 숙제 (상별 부피표) |
| SE 역학 | 선형 탄성 E 18.5 GPa · ν 0.3 (유리 원전) | DEM E_eff 1.35 GPa (18 배 연화) · MPM E 1.53 · ν 0.49 · σ_y 0.30 GPa (J2) | §7-3 · 같은 양이 아님 |
| AM 역학 | 선형 탄성 175 GPa · ν 0.3 · 리튬화 고유변형 | DEM 구 E 140 GPa (SE 대비 사실상 단단함 · 원장 SELF-51 · 대조 카드 `xu2017_…` NMC532 142.5 GPa) · MPM 에서 AM 고정 (scaffold) | 우리 성형 모델에 AM 고유변형 없음 · 사이클 원장 `--dv-pct` 5.1 % (NMC811 · Kondrakov 2017 이라는 help 글 [다른 카드 `koerver2018_…` §7-2]) ↔ 이 논문 ≈7 % |
| CBD | 한 상 · 0.35 GPa · ν 0.4 | 역학 상 없음 (DEM VGCF E 100 GPa 는 섬유 · PTFE 는 수송 격자만) | 대응 없음 |
| 접촉 · 분리 | 없음 (적합 메시) | DEM 접촉망 (분리 · 재접촉 있음) · MPM 한 속도장 (분리 제한) | 그들 '접촉 상실' 해석은 모델 기구 밖 |
| 출력 응력 | AM 평균 von Mises 끝 318–463 MPa · 국소 GPa (포화) | 사이클 응력 출력 없음 (STEP4 = 역학 결합 없음) | 크기 전이 불가 (σ ∝ E · 경계) |
| 수송 | [16] 전기화학 + GeoDict τ | STEP3 복셀 FV (CONTACT_FREE · CL-81) · DEM 접촉망 Holm | τ 정의 미인쇄 (§7-5) |
| 검증 | 없음 | DEM ↔ 실험 기공 · Bazzoun σ_ion 등 | 그들은 실험 대조 0 |

### 7-2. ★ 랩 기준과 나란히 (판정 없이)
| 출처 | 재료 · 구성 | 압력 · 상태 | 진밀도 분모 | 기공 |
|---|---|---|---|---|
| **랩 표준** | 순수 LPSCl | 300 MPa | **1.64** (고정) | **10–13 %** |
| 이 논문 (원문) | 복합 양극 69 : 27.55 : 3.45 wt (AM (NMC811 매개변수) · Li₆PS₅Cl 이름 · CBD) | CGMD 압연 20 % (압력 [미확인]) · 사이클 전 | SE 1.87 (표 S2 · 출처 없음) — 기공의 분모 정의 [미확인] | **≈12 %** (p.3 · 모델 구조) |
| 같은 구조의 앞 논문 [다른 카드] | 같음 (NMC622) | Cal20 | [미확인] | 13 % (표 S1) |
| 이 카드 산술 (SE 밀도만 바꿔 본 고체 부피 분율) | 같음 | — | 1.87 ↔ **1.64** | (기공 아님) 고체 중 SE 분율 44.7 ↔ 48.0 vol% |
| 우리 DEM 복합 (real_14) | AM : SE 82 : 18 wt · 무바인더 | 300 MPa · 가압 중 | 구 부피 합 | ε_sphere 15.6 % (CLAUDE.md) |
- 이 논문의 SE 밀도 1.87 은 **"랩 표준과 다른 문헌 값"** (출처 미표기 · 랩 1.64 보다 14 % 큼) — 부피 분율 · 기공 분모를 이 값으로 옮기지 않는다.  순수 SE 압밀 자료는 없다.

### 7-3. ★ 물성 축 (frame [2]) — E · ν · K · G · M 을 같은 표에
| 출처 | E (GPa) | ν | K (GPa) | G (GPa) | M = K + 4G/3 (GPa) |
|---|---|---|---|---|---|
| 이 논문 SE (유리 원전) | 18.5 | 0.3 | 15.4 | 7.12 | 24.9 |
| 우리 DFT LPSCl (E_VRH · B₀ · ν) | 22.06 | 0.360 | 26.23 | 8.11 | 37.0 |
| 우리 MPM SE | 1.53 | 0.49 | 25.5 | 0.513 | **26.2** |
| 우리 DEM SE (접촉 매개변수) | 1.35 | 0.3 (DEM 입력) | — | — | — |
- [카드 산술] 이 논문 SE E 는 우리 DFT 의 0.84 배 · K 는 0.59 배 · G 는 0.88 배 · 우리 DEM E_eff 의 13.7 배 · MPM E 의 12.1 배.  ★ **구속 탄성률 M 은 이 논문 SE (24.9) 와 우리 MPM (26.2) 이 거의 같다** — 우리 MPM 은 부피 (K) 를 실재로 두고 전단 (G) 만 연화했으므로 옆을 막은 압축 · 고유변형 체적 응답은 비슷하고 **전단 · 편차 응답은 14 배 다르다** (G 7.12 ↔ 0.513).
- 우리 DEM E_eff 1.35 GPa 는 재배열 · 입계 미끄럼 · 미세 파괴를 묶은 **접촉 강성 매개변수** (frame [2]) — 연속체 고체의 E 와 같은 양이 아니다 · 이 논문의 E 는 연속체 고체 (유리) 의 탄성률.
- 사이클 고유변형 응력은 σ ∝ E (변형 제어) — 우리 연화 E 로 같은 계산을 하면 응력이 E 비만큼 작게 나온다 (22.06/1.35 = 16.3 배 [다른 카드 `benhadjali2026_fully_coupled_…` 비교 문서 C 절 산술과 같음]) ⇒ 사이클 응력은 **실재 E · ν** 로 계산하고 성형의 연화 E 와 섞지 않는다.

### 7-4. 적층압 · 두께 응답 — 모델 안 겉보기 강성
- 9 → 68 MPa (59 MPa) 에 두께 팽창 차 0.71–0.87 %p → 겉보기 **6.8–8.3 GPa** [카드 산술 · %의 기준 길이 미상] — AM 175 · SE 18.5 · CBD 0.35 GPa · 기공 12 % 복합체의 탄성 두께 응답 크기 (모델 입력의 함수 · 측정 아님).
- 선형 겹침이면 차는 C-rate (사건) 무관해야 한다 — 0.86 · 0.87 · 0.71 %p (C/20 만 작음) → 다시 메시 · 끝 DoD 차이 · 큰 변형 효과 중 무엇인지 [미확인].
- ⇒ 우리 단계 6 (탈압) 의 **선형성 진단** 꼴로 쓸 수 있다: 같은 구조에 두 압력을 걸어 차분 강성을 내고 사건 (이력) 과 무관한지 본다 (§9).

### 7-5. τ 규약 (`docs` τ 명명 규약 · 2026-10-03)
- 이 논문 'geometric tortuosity τ' = GeoDict **DiffuDict** (확산 해) 의 값 · 정의식 미인쇄 → **최단 경로 τ_geo 가 아닐 가능성이 크다** (이름만 'geometric') · 같은 그룹 1 편이 인쇄한 τ_g = √(φ_SE/D_eff) 와 같다면 우리 **tau** (√tau2) — '수송 tortuosity' (tau2) 는 59.8 · 67.0 · 60.3 [카드 산술 · 정의 가정].
- 바탕값이 같은 구조의 다른 논문들 (6.1 · 6.21 [다른 카드]) 과 24–27 % 다르다 → 같은 그룹의 τ 를 서로 견줄 때 판 (구조 · 메시 · 상태) 을 숫자로 적는다.

### 7-6. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 성형 **뒤** 구조 위의 사이클 역학 (선형 탄성 고유변형 응력 · 변위) · 수송 기술자 (계면 · 기공 · τ) — MPM 쪽 '응력장 · 형상' 과 이웃이나 **소성 · 형상 변화 없음**.
- **없는 것**: 압밀 역학 (그들 압연은 CGMD) · 접촉망 · 소성 · 탈압 · 실험.  ⇒ 우리에게 주는 것은 (a) 물성 출처 사슬 (b) 넘김 꼴 (c) 사이클 응력 계산의 경계 · 보고 꼴 (d) '선형 탄성 · 작은 변형' 정당화 문장 (인용용 · 한정 필수).

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ (1) **% 의 기준 길이를 같이 등록** — 이 논문은 같은 두께 변화를 0.98 · 0.78 % (C/5) · 2.52 · ≈2.25 % (C/20) 로 적고 µm ÷ % 가 43.9 · 54.9 · 53.3 µm 로 갈린다 (표 S1 36.8 µm 와도 다름) (2) 넘김 때 **상별 부피표** (CBD 겹침 부피 재배정 전 · 뒤) 를 남기는 칸 — 그들은 남기지 않았다 (3) 면적 · 기공 분포 · τ 의 **계산법 (도구 · 문턱 · 정규화)** 칸 | 기공 숫자 (변형 뒤) · 정의식 |
| **단계 1** (3D 메모리 · 장 수) | 자릿수 하나: 3D 반쪽 셀 · 한 방향 · 방전 한 번 = 노드 하나 **500 GB RAM · 28 코어** (p.4) · 같은 그룹 양방향 · 5 사이클도 같은 노드 [다른 카드] | 자유도 · 복셀 크기 · 시간 [미확인] → 메모리 산식에 못 넣는다 |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | 없음 (접촉 표현 자체가 없다 · 적합 메시) | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 없음 — SE 항복 값 없음 · E 18.5 GPa 는 **유리** 압입값 (맞춤 표적 아님) | 순수 SE 압밀 자료 0 |
| **단계 5** (3D 복합 압밀) | 없음 (압밀 = CGMD · 이 논문은 그 뒤) · 복합 조성 · 기공 ≈12 % (압연 20 %) 한 점 | 압력 · 압밀 곡선 [미확인] |
| **단계 6** (탈압 · 되돌아옴) | ★ 간접: (1) 선형 탄성 복합체의 압력 응답 크기 = 59 MPa 당 0.71–0.87 %p (겉보기 6.8–8.3 GPa · 모델 안) — 탈압 되튐을 **탄성만으로** 셀 때의 크기 감각 (입력 E 에 매임) (2) 두 압력 차분의 사건 무관성 = **선형성 진단** 꼴 (3) 이 논문 자체는 탈압 · 되튐 · 잔류 응력을 하나도 다루지 않는다 = '탈압 계산의 선례' 로 인용 금지 | 0 MPa · 잔류 응력 · 되튐 측정 |
| **단계 7** (형상 · 피복 · 수송) | 계면 비면적 · 기공 분포 · SE τ 가 사이클 팽창 + 적층압으로 바뀐다는 꼴 (*"Mechanics → Microstructure → Electrochemistry"* p.10) · τ +5.8 % (9 MPa) ↔ +0.4 % (68 MPa) · AM–SE 면적 +10–18 % | 면적 · τ 계산법 [미확인] · 면적 증가가 기하 기대의 ≈34 배 (§3-9) — 크기 인용 금지 |
| **후보 D0** (지금 DEM) | ★ k 근거 문장 하나 (구 가정의 한계 · p.4) · 표 1 의 DEM 선행 [38] 은 소성 Yes · 불규칙 모양 No — '구 DEM 은 모양을 못 바꾼다' 의 표 근거 | 겹침 상한 · 연화 · 접촉 독립 가정 진술 없음 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 경계의 꼴: 측벽 고정 벽 (*"imitate the casing"*) · 위면 균일 압력 · 아래 고정 · 분리막 · 집전체 강체 — 판 · 벽 모델링의 등록 예 | 벽 마찰 · 분리 · 미끄럼 없음 |
| **후보 A · A′** (MPM 강체 AM / 입자별 속도장) | 없음 (FEM 적합 메시) — 대비: 그들 AM 은 **강체가 아니라 175 GPa 탄성 + 고유변형** | — |
| **후보 B** (입자별 FE + 접촉) | 가장 가까운 이웃이지만 **접촉 없는 상 단위 FE** (입자 경계 없음 · 적합 메시) — B 의 '접촉' 을 빼면 무엇이 남는지의 예 · 메시 = 복셀 기반 + 변형 따라 자동 세분 (그림 S1) | 입자별 접촉 · 분리 · 소성 없음 |
| **후보 C · C′** (MDR · 항복 캡 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀) | 없음 | — |
| **U0–U6** | **U6** (해상도 수렴) 쪽 반면교사: 메시 수렴 보고 0 · 변형 기반 다시 메시만 언급 · **U3** (단단한 구를 소성 블록에 눌렀다 떼기) 류 시험 없음 | 단위 시험 0 |
| **R1–R7** | **R1** (AM 하중 분담) 의 연속체판 지표: AM 평균 von Mises ÷ 적층압 = 2.10 (9) · 1.54 (68 MPa) [판독 · 카드 산술] — 힘 몫이 아니다 · **R4** (탈압) 없음 · **R6** (SE 형상 변형) 없음 (모양 = 기하 후처리) · **R7** (AM 파괴) 언급만 (*"may exacerbate particle fracture"*) · **R2** (미끄럼 · 분리) 없음 · **R3** (SE 입자 경계) 없음 (상 연속체) · **R5** (맞춘 값 하나) — 맞춘 값 0 · 검증 0 | 전부 모델 내부 |
| **결과 전 대조 항목** | 사이클 응력 · 두께 계산을 우리 쪽에 넣을 때 **견줄 외부 값이 아니다** (모델 값) — 견줄 수 있는 것은 측정 (예: `koerver2018_…` 축 응력) · 이 논문은 '같은 계산의 다른 모델 값' 으로만 표에 (재료 · 경계 · 물성 표지 필수) | 실험 0 |

- **재료 · 차원 · 조건 차이**: AM NMC811 매개변수 (구조는 NMC622 판) ↔ 우리 NCM (DEM AM_P / AM_S) · SE 물성 = Li₂S–P₂S₅ 유리 ↔ 우리 LPSCl (DFT · 연화) · CBD 포함 (습식) ↔ 우리 무바인더 건식 · 3D = 같음 · 적층압 9 / 68 MPa (사이클) ↔ 성형 300 MPa · 방전 한 번 · 온도 [미확인].

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **사이클 응력은 실재 E · ν 로 · 경계를 결과 전에 등록** — 고유변형 응력은 σ ∝ E 이고 이 논문 크기는 유리 SE (18.5 GPa) · 측벽 고정 · 강체 분리막의 함수다 → A10 원장 · STEP4 에 역학을 붙일 때 성형 연화 E (1.35 · 1.53) 를 쓰지 않고, 측벽 · 위판 · 분리막 조건을 먼저 적는다 (흐름 밖: 사이클 열화).
2. **% 는 기준 길이와 함께** — 같은 두께 변화가 0.98 / 0.78 %, 2.52 / ≈2.25 % 로 인쇄된 사례 (§3-6) → 우리 두께 · 되튐 보고는 µm 와 분모 길이를 함께 (단계 0 · 6).
3. **두 압력 차분 = 선형성 진단** — 9 ↔ 68 MPa 의 두께 차가 C-rate 와 거의 무관 (0.71–0.87 %p) 하면 선형 겹침 · 어긋나면 비선형 · 다시 메시 효과 → 우리 탈압 계산에서 두 끝 압력의 차분 강성이 이력과 무관한지 본다 (단계 6).
4. **넘김 기록** — CBD 겹침 부피를 AM / SE 에 더하는 규칙은 상별 부피를 바꾼다 (같은 그룹 1 편의 (1 − ε)·t −26 % 반례 [다른 카드]) → 우리 DEM → MPM → STEP3 넘김에도 상별 부피 전 · 뒤 표를 붙인다 (단계 0 · 5).
5. **M 이 같고 G 가 다르다** — 우리 MPM (ν 0.49) 과 이 논문 SE 의 구속 탄성률은 24.9 ↔ 26.2 GPa 로 같은 자리 · 전단 G 는 14 배 차 → 우리 MPM 의 '부피는 실재 · 전단만 연화' 를 설명할 때 문헌 연속체 값과의 대비로 쓸 수 있다 (frame [2] · 단계 4 해설).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "A one-way coupled 3D microstructure-resolved FEM of a wet-processed NMC811/Li₆PS₅Cl/CBD half-cell (linear elastic phases, intercalation eigenstrain from Koerver et al. 2018) predicts a half-cell thickness increase of 0.78–2.53 % at 9 MPa and −0.08–1.82 % at 68 MPa stack pressure for C/5–C/20 discharge (Ben Hadj Ali et al., Batteries & Supercaps 9 (2026) e202500540, Fig. 7a)."
- "The authors justify linear elasticity by the ≈7 % volume change of NMC811 — 'the majority of the AM is expected to remain within the elastic regime' — and defer plasticity, contact loss and debonding to future work (Ben Hadj Ali et al. 2026, pp. 4–5, 12)."
- "The solid-electrolyte elastic constants in that model (E = 18.5 GPa, ν = 0.3; SI Table S2) are taken from Li₂S–P₂S₅ glass studies (McGrogan 2017; Sakuda 2013), not from Li₆PS₅Cl."
- 국문: *"Ben Hadj Ali 2026 의 3D 한 방향 결합 FEM 은 압연 구조를 기하로만 넘겨 응력 0 에서 시작하며, 탈압 · 소성 · 접촉 분리는 다루지 않는다."*
- 국문: *"구 입자 가정의 한계 — 'none of which can be adequately captured by idealized spherical approximations' (Ben Hadj Ali 2026, p.4) — 단, 그들의 불규칙 모양은 겹침 부피 재배정이라는 기하 후처리다."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **SE 물성 원전 = 유리** — E 18.5 GPa [S4] = 70Li₂S–30P₂S₅ 유리 압입 (ν 0.3 가정 [다른 카드]) · ν [S5] = Li₂S–P₂S₅ 유리 · ρ 1.87 출처 없음 — 표 머리 'SE: Li₆PS₅Cl' 과 다르다.
2. **AM 화학** — 구조는 NMC622 판 CGMD (원 논문 [41] · 앞 논문 [16] [다른 카드]) · 이 논문은 NMC811 팽창 · 물성 (175 GPa DFT [S6]) 을 붙였다 · 본문 §2 는 'AM' 이라고만 쓴다.
3. **% 의 기준 길이 미상 · 같은 양 두 값** (§3-6): 0.98 ↔ 0.78 % (C/5) · 2.52 · 2.53 ↔ ≈2.25 % (C/20) · 1.11 ↔ ≈1.2 µm · 표 S1 L_C 36.8 µm 와 맞는 쌍 없음.
4. **식 (10) 왼쪽 ε_e (→ ε_int)** · 식 (8) 뒤 문장 *"εe and εint are the total and intercalation-induced strains"* (ε_e 를 총 변형이라 함) · *"Combining Equations (2) and (3)"* (→ (1) · (2) · (4)) · *"u = θ0"* · *"Hook's law"*.
5. **[37] 귀속** — *"the electrochemical framework previously reported by group[37]"* 의 [37] = von Kolzenberg · Latz · Horstmann (B&S 2022) · 같은 그룹 틀은 [16].
6. **SI 참고 번호** — 본문 *"cited additional references within the Supporting Information.[69–70]"* ↔ SI 는 [S1]–[S11] · 본문 목록은 [69] (Budiman · 표 1 에서만 인용) 로 끝나고 [70] 이 없다 · 표 1 근처 본문이 [40] 을 *"(Table 1)"* 로 가리키나 표에 [40] 줄이 없다.
7. **단위 · 값 인쇄** — δ_ion *"mS.cm-2"* · i₀,a *"3 A.cm-2"* · ρ *"Kg·m3"* · NMC811 밀도 4.77 (표 S1) ↔ 5.03 (표 S2) · 집전체 δ_e 300 S·m⁻¹ (값 그대로 · 판정 안 함).
8. **색 막대 포화 · 불일치** — 그림 5c 0–2 GPa · 그림 7c ±50 · ±5 MPa (양끝 포화) · 본문 '3 GPa' ↔ 그림 S2 색 막대 ±300 MPa.
9. **그림 6b 눈금 글자** 0.0 · 0.2 · 0.4 · 0.7 · 0.9 · 1.1 · 1.3 이 같은 간격 (반올림) — 끝값이 ±0.05 µm 흔들린다.
10. **그림 6a 'SOC' 정의** — DoD 0 출발값이 C-rate 마다 다르고 (0.23–0.29) 끝값은 같다 (0.975) — 평균 리튬화가 아니다 [판독 · 카드 추론].
11. **그림 8 면적** — 정규화 미상 (구 비표면적의 6.2 배) · 증가가 기하 기대의 ≈34 배 · 캡션 *"in function of SOC"* ↔ 축 DoD · *"dicharge"* · *"m'g⁻¹"*.
12. **그림 9 해석** — *"shifted toward smaller diameters"* ↔ 곡선은 작은 기공 몫 감소 (중앙 0.61 → 0.80 µm [카드 산술]) · 9 MPa 판에 원 구조에 없던 3–4.6 µm 기공 · 정규화 누적이라 총 기공 부피 [미확인].
13. **모델 밖 기전으로 설명** — 68 MPa 의 억제 = *"enhanced particle packing and improved interfacial contact"* · 면적 감소 = *"loss of AM–SE … contact"* · *"local densification"* · *"9 MPa is not always sufficient to compensate for expansion-induced degradation"* — 적합 메시 선형 탄성에는 재배열 · 분리 · 치밀화 · 열화 기구가 없다 [카드 해석].
14. **τ 정의 미인쇄 · 바탕값 불일치** — 7.736 ↔ 같은 구조 6.21 · 6.1 [다른 카드].
15. **'SE 강체'** — 분리막 SE 를 강체로 둔 문장과 양극 SE 를 선형 탄성으로 둔 문장이 같은 'SE' 낱말 · *"The mechanical contribution of the SE will be addressed in our future work"* 는 양극 SE 가 응력장을 내는 그림 7c 와 어긋나 보인다.
16. **보충 동영상** — *"shown in the supplementary videos"* (p.7) — 받은 SI PDF 에 없음 [미확인].
17. **응력과 항복 · 파괴 비교 없음** — 평균 318–463 MPa · 국소 GPa 를 NMC811 · SE 의 강도와 견주지 않았다 (위험 문장만).
18. **실험 대조 0** — *"consistent with experimental findings reported in the literature,[65,67]"* (정성) 뿐.
19. ⚠ **판독 값** 은 원 래스터 보정 · 그래도 [판독] 표지로만 인용 · 그림 7b 실선 / 파선 배정은 색 무리 추적 (같은 색 두 무리).

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| [6] | R. Koerver, W. Zhang, L. de Biasi, S. Schweidler, A. O. Kondrakov, S. Kolling, T. Brezesinski, P. Hartmann, W. G. Zeier, J. Janek, Energy Environ. Sci. 2018, 11, 2142. | ΔV 입력 원전 | `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` |
| [16] | S. B. H. Ali, M. Alabdali, V. Viallet, V. Seznec, A. A. Franco, J. Power Sources 2025, 630, 236131. | 같은 구조의 전기화학 틀 (1 편) | `benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode` |
| [41] | M. Alabdali, F. M. Zanotto, M. Duquesnoy, A.-K. Hatz, D. Ma, J. Auvergniot, V. Viallet, V. Seznec, A. A. Franco, J. Power Sources 2023, 580, 233427. | 구조 원 출처 (CGMD) | `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` |
| [40] | M. Alabdali, F. M. Zanotto, M. Chouchane, A. C. Ngandjong, V. Viallet, V. Seznec, Y. S. Meng, A. A. Franco, Energy Storage Mater. 2024, 70, 103527. | 같은 그룹 DEM 사이클 응력 | `dem_mechanical_stresses_ssb_electrode_cycling` |
| [38] | M. So, T. Yano, A. Permatasari, V. L. Nguyen, G. Inoue, Adv. Funct. Mater. 2025, 2423877. | ★ 표 1 의 DEM · 3D · 소성 Yes (실리콘 · 전고체) — 질문 e · k · l | 없음 (papers/ ls · grep '2423877') |
| [69] | B. A. Budiman, A. Saputro, S. Rahardian, M. Aziz, P. Sambegoro, I. P. Nurprasetio, J. Energy Storage 2022, 52, 104810. | 표 1 의 FEM · 전고체 · 3D · 소성 Yes (균질 전극) — 질문 c · l | 없음 |
| [18] | A. M. Boyce, E. Martínez-Pa˜neda, A. Wade, Y. S. Zhang, J. J. Bailey, T. M. M. Heenan, D. J. L. Brett, P. R. Shearing, J. Power Sources 2022, 526, 231119. | 표 1 의 3D · 소성 Yes · XCT 구조 · 탄성 영역 근거로도 인용 ([18, 56]) — 질문 h · l | 없음 |
| [39] | H. Hanyu, Y. Bai, S. Benz, T. Weintraut, S. Wang, A. Henss, D. Raabe, J. Janek, Adv. Mater. 2025, 37, 2415006. | 표 1 의 2D 위상장 · 소성 Yes (실리콘) — 질문 g · l | 없음 |
| [42] | M. Alabdali, F. M. Zanotto, B. Notredame, V. Viallet, V. Seznec, A. A. Franco, Batteries Supercaps 2025, 8, e202400709. | CGMD 제조 모의 (구조 사슬) — 질문 h | 없음 |
| [S4] | McGrogan, F.P.; Swamy, T.; Bishop, S.R.; Eggleton, E.; Porz, L.; Chen, X.; Chiang, Y.; Van Vliet, K.J. … Adv. Energy Mater. 2017, 7, 1602011 | SE E 의 원전 (유리) | `mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation` |
| [S5] | Sakuda, A.; Hayashi, A.; Takigawa, Y.; Higashi, K.; Tatsumisago, M. … J. Ceram. Soc. Jpn. 2013, 121, 946–949 | SE ν 의 원전 (유리) | 없음 (wishlist 에 이미 있음) |
| [S6] | Sun, H.; Zhao, K. … J. Phys. Chem. C 2017, 121, 6002–6010 | NMC811 E 175 GPa 원전 (DFT) | 없음 (wishlist 에 이미 있음) |
| [S8] | Xu, R.; Sun, H.; Vasconcelos, L.S. de; Zhao, K. … J. Electrochem. Soc. 2017, 164, A3333 | NMC ν | `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` |
| [S3] | Schmidt, C.P.; Sinzig, S.; Gravemeier, V.; Wall, W.A. … Comput. Methods Appl. Mech. Eng. 2023, 417, 116468 | 3D FE 전기화학 + 고체역학 (ρ · 접촉 저항 출처) | 없음 (wishlist 에 이미 있음) |
| [S1] · [S2] | Bielefeld 2022 JES 169, 020539 · Ruess 2020 JES 167, 100532 | δ_ion · i₀ · OCV · D 출처 | 없음 (Bielefeld 2022 은 wishlist 에 있음) |
| [54] | A. Lundkvist, P.-L. Larsson, A. H. S. Iyer, E. Olsson, Powder Technol. 2024, 443, 119873. | 'CBD · 기공이 변형을 줄인다' 의 근거 | 없음 (wishlist 에 이미 있음) |
| [64] · [65] · [67] | Taghikhani 2025 JMPS 198, 106060 · Sakka 2022 JMCA 10, 16602 · Yamamoto 2020 JPS 473, 228595 | 미세구조 변화 · 실험 정합 문장 | `taghikhani2025_…` · `sakka2022_…` · Yamamoto 없음 (wishlist 에 있음) |
| [14] | A. Neumann, T. R. Hamann, T. Danner, S. Hein, K. Becker-Steinberger, E. Wachsman, A. Latz, ACS Appl. Energy Mater. 2021, 4, 4786. | 미세구조 해상 전기화학 (역학 없음) 선행 | `neumann2021_garnet_3d_structure_grain_boundaries_li_transport` |

---

## [미확인] 목록
- 메시: 복셀 크기 · 요소 종류 · 수 · 자유도 · 메시 수렴 · 다시 메시 기준.
- 상자 옆 치수 · Li 금속 두께 · % 의 기준 길이 (표 S1 36.8 µm 와 맞지 않음).
- 역학 초기 상태 (압연 응력 · 되튐 · 판 분리) · 적층압을 거는 순서 (방전 전 평형?).
- c_min 값 · 그림 6a 'SOC' 정의 · DoD 정의 · 온도.
- D_AM · OCV · i₀,c 의 숫자 (SI 도 "See reference").
- 계면 비면적 · 기공 분포 · τ 의 계산법 (도구 · 문턱 · 정규화 · τ 정의식).
- 실행 시간 · 시간 간격 · 수렴 기준.
- 가리킨 논문 (WIP ↔ CUP) · 완전결합판이 이 표 S2 의 E · ν 를 그대로 썼는지.
- 보충 동영상 · ChemRxiv 판과의 차이.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 서지: 후보 표 메모 (S. Ben Hadj Ali, M. Alabdali, V. Viallet, V. Seznec, A.A. Franco · 제목 · Batteries & Supercaps 9 (2026) e202500540 · DOI) = 원문 첫 쪽 · 각 쪽 머리글 *"Batteries & Supercaps 2026, 9, e202500540 (n of 14)"* · *"doi.org/10.1002/batt.202500540"* 와 같음 · 저자 이름 전체 · 소속 · 교신 = p.1 · 접수 · 수정 = p.14 · 연구비 · 기여 · 자료 = p.12–13 · SI 제목 *"… in Solid State Battery Electrodes"* (하이픈 없음).
- 숫자: 텍스트 층 + 쪽 렌더 대조 — 69 : 27.55 : 3.45 · 10 µm · ≈12 % · 20 % · 500 GB · 28 코어 · 2.40 GHz · 2.6–4.2 V · C/5 · C/10 · C/20 · 9 · 68 MPa · ≈7 % · 0.43 µm · 0.98 % · 1.11 µm · 2.52 % · 3 GPa · ≈1.2 µm · ≈2.25 % · 4.49 · 0.45 · 0.21 % · 0.78 · 1.61 · 2.53 · 0.08 · 0.74 · 1.82 % · 0.2–2.6 · 3–4.6 · 1.8–3 · >3 · ≤1.4 µm · 7.736 · 8.182 · 7.765 · 표 S1 · S2 전 칸 — 전부 위치 확인.
- 낱말 전수 (본문 · SI): 'unload' · 'residual' · 'relax' · 'release' · 'periodic' · 'yield' · 'validat' 0 회 · 'plastic' 3 회 (표 1 열 머리 · 결론 둘) · 'Young' 본문 1 · SI 4 · 'Poisson' 본문 0 · SI 4 · 'DEM' 본문 3 (서론 p.2 둘 · 표 1 하나) · 'fracture' 2 (위험 문장) · 'crack' SI 1 (참고문헌 제목).
- 판독 보정: 각 그림의 큰 눈금 직선 맞춤 · 그림 6b 눈금 글자 불균일은 두 방식으로 · 그림 7b 같은 색 두 무리 추적 · 그림 9 겹친 표지 눈 판독 — digitized.csv note 칸.
- 정본 중복 확인: papers/ 목록 (`ls benhadj*` = 다른 논문 셋) · DOI '202500540' grep = `benhadjali2026_wip_vs_cup_…` L442 · `benhadjali2026_fully_coupled_…` L400 (인용만) · 제목 낱말 'Three-Dimensional Microstructure-Resolved' 같은 결과 → 카드 없음.

## 🔗 관련 카드
- 같은 그룹 · 같은 사슬: `benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode` (1 편 · 전기화학) · `benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode` (같은 해 · 양방향판 · 이 논문 = 그 카드 [26] · [36]) · `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` (같은 해 · 이 논문 = 그 카드 [30] · 후보 표 근거) · `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` (구조 원 출처) · `dem_mechanical_stresses_ssb_electrode_cycling` ([40]).
- 입력 · 물성 원전: `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` ([6] · ΔV) · `mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation` ([S4] · SE E) · `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` ([S8]).
- 사이클 역학 · 미세구조 변화: `taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode` ([64]) · `sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps` ([65]) · `bucci2017_chemomech_failure_assb_cycling_czm` (같은 저자군의 다른 논문 · 이 논문 [66] 은 JES 2017 판으로 카드 없음).
- 제조 모의 → 연속체 넘김: `ngandjong2021_dem_calendering_digital_twin` ([45]) · `neumann2021_garnet_3d_structure_grain_boundaries_li_transport` ([14]).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
