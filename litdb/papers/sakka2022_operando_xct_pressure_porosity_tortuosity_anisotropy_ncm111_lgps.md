<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 1저자 11-12 후보 표 N-44 · 1저자가 궁금해한 여섯 항목) 에서 꼭 뽑으라고 한 항목.
     본 = doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density.md (복합 양극 압력 · 밀도 실험 카드의 꼴) · 곁 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (X 선 CT 기공 · 복셀 한정어) ·
     두 필수 절 (§0-1 고른 의도 대조 · §8 자세한 분석) 은 같은 묶음의 park2025 · jeong2024 카드와 같은 꼴.
     원문 = 출판본 (J. Mater. Chem. A 2022, 10, 16602–16609 · 8 쪽 · "Licensed under CC-BY 4.0") + ESI (16 쪽 PDF = 표지 + 그림 S1–S16 · 표 없음).
     쪽 표기 = 본문 "p.n" = PDF 쪽 n (인쇄 쪽 = 16601 + n · p.1 = 16602 … p.8 = 16609) · ESI "SI p.n" = ESI PDF 쪽 n (SI p.1 = 표지 · 그림 S1 = SI p.2 … 그림 S15 · S16 = SI p.16).  크롭 파일 이름의 pN · figures.json 의 page 는 PDF 쪽이다.
     값 표지: [인쇄] = 본문 · ESI · 그림 안 글자로 적힌 값 · [판독] = 래스터 그림을 그 그림의 눈금으로 환산한 값 (재현 = litdb/figures/<slug>/digitized.csv 538 행 — 본문 그림은 300 dpi 래스터 원본 픽셀에서) ·
     [판독 · 벡터] = ESI 그림 S15 (유일한 벡터 그림) 의 표지 경로 좌표를 눈금 선분으로 환산한 값 · [카드 판독] = 원문에 없는 지표를 이 카드가 그림 화소로 센 값 (논문의 값이 아님) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [가정] = 원문에 없는 성분 밀도 등을 카드가 넣은 값 · [다른 카드] = 정본의 다른 카드에 적힌 값 (slug 병기) ·
     [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [우리] = 우리 쪽 값 (CLAUDE.md 출처) · [미확인] = 본문 8 쪽 + ESI 16 쪽 전수에 없음.
     원문 24 쪽은 글자 층 (pdftotext raw · layout · PyMuPDF) + 전 쪽 렌더로 전부 읽었다 (µ · × 같은 기호는 글자 층에서 'm' · 빈칸으로 깨져 렌더로 확인).
     DEM · MPM · FEM · 입자 계산 · 압밀 시뮬레이션은 없다 — 실험 (누른 채 싱크로트론 X 선 CT + 같은 셀 EIS + 정전류) 만. -->
# NCM111 (LiNbO₃ 코팅) + LGPS (Li₁₀GeP₂S₁₂) + 아세틸렌 블랙 1 : 1 : 0.1 wt% 복합 양극을 지름 1 mm 셀에서 **누른 채** 싱크로트론 X 선 CT (복셀 ≈0.5 µm) 로 0 · 6 · 12 · 50 · 100 MPa 단계마다 본 미세구조 (microstructure) — 복합 양극 기공 (porosity) 44 → 23 % · 같은 셀 LGPS 층 53 → ≈5 % · NCM/LGPS 접촉 면적 분율 75–78 → 83–84 % (50 MPa 에서 멈춤) · SE 경로 기하 tortuosity 는 50 MPa 까지 줄다가 100 MPa 에서 다시 늘고 퍼짐 · 가압 방향 (Z) 면은 LGPS 와 닿고 옆면은 공극과 닿는 이방성 (정성) · R_ct 약 15 배 감소 — Sakka · Yamashige · Watanabe · Takeuchi · Uesugi · Uesugi · Orikasa (J. Mater. Chem. A 2022)

> slug `sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps` · DOI `10.1039/D2TA02378D` · type `experiment (operando cell: synchrotron X-ray CT under monitored uniaxial load 0–100 MPa · 3-phase voxel segmentation porosity · NCM/LGPS contact area fraction · SE pathway geometric tortuosity histogram · EIS in the same cell · galvanostatic cycling — no DEM / MPM / particle model)` · PDF `e433fb54-44._Pressure_dependence_on_the_three-dimensional_structure_of_a_composite_electrode_in_an_all-solid-state_battery.pdf` · SI `699ac537-44._Sup_Pressure_dependence_on_the_three-dimensional_structure_of_a_composite_electrode_in_an_all-solid-state_battery.pdf` · digested `2026-11-12` · status ✅
>
> **저자**: **Yuya Sakka** ᵃ · Hisao Yamashige ᵇ · Ayaka Watanabe ᵃ · Akihisa Takeuchi ᶜ · Masayuki Uesugi ᶜ · Kentaro Uesugi ᶜ · **Yuki Orikasa\*** ᵃ — ᵃ Department of Applied Chemistry, Ritsumeikan University (Kusatsu, Shiga) · ᵇ Toyota Motor Corporation · ᶜ Japan Synchrotron Radiation Research Institute (JASRI, SPring-8) — \* 교신 (orikasa@fc.ritsumei.ac.jp) · *J. Mater. Chem. A* **2022**, **10**, **16602–16609** (8 쪽 · Paper) · 접수 2022-03-24 · 승인 2022-07-08 · 출판 2022-07-22 · *"Licensed under CC-BY 4.0"* (p.1 머리) · 연구비 = JSPS KAKENHI 19H02694 · NEDO JPNP20004 · SPring-8 BL20XU 과제 2019B1726 · 2020A0502 · 2021A1005 · 2021A1539 · 2021B1724 (p.7) · 이해 상충 없음 · 기여: Y.S. · Y.O. 착상 · operando CT · H.Y. 셀 설계 · Y.S. 충방전 · CT 분석 · A.W. 입경과 공극 (LFP) · A.T. · M.U. · K.U. 빔라인 · 재구성 (p.6).
> **이웃 카드 (링크만)**: [`jeong2024_operando_densification_chemomechanics_se_size_composite_cathode`](jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md) (참고 [22] = 이 논문 · NCM811–LPSCl XCT 기공) · [`tailored_cathode_microstructure_low_pressure_assb`](tailored_cathode_microstructure_low_pressure_assb.md) (ref 12 = 이 논문 · "Sakka(Sakuda)" 표기) · [`fan2026_sulfide_assb_stability_review_ECERD2600097`](fan2026_sulfide_assb_stability_review_ECERD2600097.md) (리뷰 · 비교 문서 §A 의 [151]) · ref 15 = [`doux2020_pressure_effects_sulfide_se_jmca`](doux2020_pressure_effects_sulfide_se_jmca.md) · ref 26 = [`doux2020_stack_pressure_assb`](doux2020_stack_pressure_assb.md) · ref 43 = [`sakuda2013_sulfide_mechanical_property`](sakuda2013_sulfide_mechanical_property.md) · ref 40 = [`minnmann2021_jes_charge_transport_bottlenecks`](minnmann2021_jes_charge_transport_bottlenecks.md) · ref 39 = [`froboese2019_microstructure_ionic_conductivity_assb_electrode`](froboese2019_microstructure_ionic_conductivity_assb_electrode.md) · ref 19 = [`bucci2018_mechanical_instability_interface_delamination`](bucci2018_mechanical_instability_interface_delamination.md) · 같은 꼴 (복합 양극 XCT) = [`park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics`](park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics.md) · 같은 꼴 (황화물 누른 채 XCT) = [`kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation`](kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md) · [`korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens`](korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens.md) · 압밀 중 tortuosity = [`miss2026_pressure_tortuosity_composite_cathode_coating`](miss2026_pressure_tortuosity_composite_cathode_coating.md) · LGPS 결정 = [`kamaya2011_lgps_lithium_superionic_conductor`](kamaya2011_lgps_lithium_superionic_conductor.md).
> **판독 원자료**: `litdb/figures/sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps/digitized.csv` (538 행 — 그림 3a 표지 10 · 3b 인쇄 % 15 · 3c 표지 5 · 5c 막대 칸 170 + 통계 50 · 6a · 6b 표지 8 · 2a · 2b 곡선 끝 26 · SI S3b 표지 5 · SI S15 벡터 표지 204 · 카드 판독 = SI S13 방향별 경계색 25 · SI S6 층 두께 20) · 그림 크롭 **58 장** (도구 23 중 다시 자름 13 · 손 크롭 35 = 패널 17 · 근거 문단 18 · 식 0 — 원문에 번호 식 · 인라인 식이 없다) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: LiNbO₃ 코팅 LiNi₀.₃₃Co₀.₃₃Mn₀.₃₃O₂ (NCM111) · 550 °C 고상 합성 Li₁₀GeP₂S₁₂ (LGPS) · 아세틸렌 블랙 (AB) 을 막자사발에서 **1 : 1 : 0.1 (질량)** 로 섞은 양극 1.0 mg 을 LGPS 1.0 mg · In–Li 와 **지름 1 mm 실린더**에 넣고, 위쪽 나사로 누르며 아래 막대 밑 **하중 센서**로 압력을 보는 셀을 SPring-8 BL20XU (20 keV · 화소 ≈0.5 µm · 시야 ≈1.0 × 1.0 mm · 1800 투영 / 180°) 에서 **누른 채** 0 · 6 · 12 · 50 · 100 MPa 마다 찍고 (따로 제조압을 가하지 않았다 — *"the pressure shown in this study corresponds to the previously reported fabrication pressure"* p.3), Dragonfly 4.1 로 NCM · LGPS · 공극 세 상을 **투과 세기**로 나눠 512 × 512 × 50 µm³ 안에서 셌다 (p.2–3).
그 결과 복합 양극 기공은 **44 → 42 → 39 → 31 → 23 %** (그림 3b [인쇄]) · 같은 셀의 LGPS 층은 **53 → 41 → 39 → 15 → 4.3 %** [판독 그림 3a] (본문 *"23% and 5% at a pressure of 100 MPa"* p.4) 로, 12 MPa 까지는 두 층이 비슷하다가 그 뒤 복합 양극만 덜 줄었다 — 저자 해석 = 단단하고 큰 NCM 이 하중을 먼저 받아 NCM 틈이 **"low-pressure spots"** 가 되고 옆에서 미는 힘이 없어 LGPS 가 그 틈을 못 메운다 (p.6 · 그림 7).
NCM 표면 중 LGPS 와 닿은 몫 (**접촉 면적 분율**) 은 **78.3 · 74.9 · 77.9 · 84.3 · 82.7 %** [판독 그림 3c] — *"increases by approximately 10% when the pressure is greater than 50 MPa compared with ≤ 12 MPa"* · *"stopped when the pressure reached 50 MPa"* (p.4).  SE 로 이어진 경로 길이 ÷ 두께 (기하 tortuosity · 36 × 36 × 50 µm³ · 경로 N = 100) 는 평균 **6.54 → 5.27 → 4.51 → 3.83 → 5.38** · 표준편차 **1.12 · 0.97 · 0.69 · 0.84 · 1.26** [판독 그림 5c · 카드 산술] 로 50 MPa 까지 줄다가 **100 MPa 에서 다시 늘고 퍼진다** (p.5 · p.6 — 저자: *"a trade-off between the connectivity of AM/SE and the tortuosity of SE"*, 그러나 *"minor impact"* 예상).
접촉의 **방향**은 그림 (XY · YZ · XZ 단면 · 3D) 을 보고 *"good contact with LGPS in the Z-axis direction, which is the pressure direction … preferential contact with the voids … in the horizontal direction"* (p.4) 라고 적었을 뿐 **방향별 지표 · 값은 없다** — 이 카드가 SI 그림 S13 (XZ 단면, 512 × 50 µm) 화소로 센 녹색 (NCM/LGPS) 몫은 위 · 아래 면 **0.89–0.96** · 옆면 **0.65–0.85** [카드 판독 · 원문에 없는 지표] 다.
같은 셀 EIS: R_ct **865 → 412 → 166 → 58 kΩ** (×1/15) · 겉보기 전도도 **7.84 → 9.73 × 10⁻⁵ S/cm** (+24 %) [판독 그림 6] · 첫 방전 **27.4 · 39.7 · 44.1 mAh g⁻¹** (6 · 50 · 100 MPa · 0.01C) [판독 그림 2b].
**재료가 우리와 다르다 (LGPS · NCM111 · AB 4.8 wt%) · 압력이 ≤ 100 MPa · CT 분할 기공 (진밀도 분모 없음 · 0.5 µm 아래 기공 못 봄 · AB 가 '공극' 쪽으로 갔는지 미기재) · 분석 영역 하나 · 반복 없음.**

| 1저자가 궁금해한 것 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 압력별 기공 · 접촉 면적 — 값 · 단계 · **누른 채 / 뺀 뒤** · 기공 정의 · 분모 · 분할 문턱 | **누른 채 (in situ · operando 셀)** — 0 (가루를 넣은 상태) · 6 · 12 · 50 · 100 MPa: 복합 양극 기공 **44 · 42 · 39 · 31 · 23 %** [인쇄 그림 3b] (표지 판독 44.2 · 42.3 · ≈39 · 30.6 · 22.9 %) · LGPS 층 **53.0 · 40.9 · 39.0 · 15.0 · 4.3 %** [판독 그림 3a] (본문 100 MPa = 5 %) · NCM / LGPS 부피 **18 / 38 · 25 / 33 · 30 / 31 · 29 / 41 · 33 / 44 %** [인쇄 3b] · 접촉 면적 분율 **78.3 · 74.9 · 77.9 · 84.3 · 82.7 %** [판독 3c] · **정의**: 기공 = 세 상 분할의 공극 복셀 부피 ÷ 분석 영역 (512 × 512 × 50 µm³) [카드 해석 — 원문은 *"identified based on the transmission intensity"* 만] · 접촉 면적 분율 = *"the fraction of the area in contact between NCM and LGPS with respect to the surface area of the NCM particles"* (p.4) · **분모 = 진밀도 · 성분 밀도 쓰지 않음** (영상 부피) · **분할 문턱 · 알고리즘 · 영역 위치 [미확인]** · 뺀 뒤 = 50 MPa → 0 MPa 한 번 (그림 S14 · 정성, 숫자 없음) | [인쇄] p.2–4 · 그림 3 · [판독] |
| ② ★ "과압하면 tortuosity 가 오른다" 가 원문에 있나 | **있다** — *"when the pressure was 100 MPa, the tortuosity had increased and so had the variation"* (p.5) · *"it has been confirmed that the tortuosity increases at 100 MPa"* · *"High-pressure fabrication … causes such an increase in tortuosity, suggesting the trade-off between the connectivity of AM/SE and the tortuosity of SE"* (p.6) · **어느 압력부터 · 얼마**: 50 → 100 MPa 에서 평균 3.83 → **5.38** · 중앙 3.75 → 5.2 · 최빈 3.75 → 5.55 · 최소 2.45 → 2.75 · 표준편차 0.84 → 1.26 [판독 · 카드 산술] · ⚠ "과압" = **100 MPa** (우리 300 MPa 의 1/3) · 정의 = SE 경로 길이 ÷ 두께 (**기하 · 수송 tortuosity 아님**) · 압력마다 36 × 36 × 50 µm³ 하나 · 저자도 *"minor impact on the electrochemical properties"* 예상 | [인쇄] p.5–6 · [판독] 그림 5c |
| ③ ★ 이방 접촉 ("가압 방향 접촉 ↑ ↔ 측방 기공 지배") 이 원문에 있나 · 어떻게 쟀나 | **있다 (정성)** — 그림 4a (XY · YZ · XZ 단면, 녹 = NCM/LGPS · 청 = NCM/공극) 와 4c · S13 을 **눈으로 보고** 적었다: *"Detailed observations of these images reveal …"* (p.4) · 높은 압력에서도 *"though less frequently"* (p.5) · 공극 모양이 가압 방향을 따른다 (그림 4c 노란 타원) · **방향별 지표 · 값 없음** · 카드 판독 (SI S13 · 한 단면 · 화소): 녹색 몫 Z 면 / 옆면 = **0.93 / 0.66 (0) · 0.89 / 0.65 (6) · 0.92 / 0.68 (12) · 0.96 / 0.85 (50) · 0.93 / 0.74 (100 MPa)** · 위 면 ↔ 아래 면 차이 ≤ 0.03 | [인쇄] p.4–5 · [카드 판독] §3-5 |
| ④ ★ 재료 · 조성 · 입경 · CT 조건 · 셀 · 압력 측정 | NCM111 (LiNbO₃ · 구동 유동 코팅기 MP-01 Powrex) · LGPS (550 °C · Ar) · AB (Denka) · **1 : 1 : 0.1 wt** (막자사발 · Ar) · vol% **[미확인]** → 카드 ≈ **28 : 65 : 7 vol%** [카드 산술 · 가정 밀도] · 입경: NCM *"on the order of 10 µm"* (p.4) · SEM [판독 · 대략] NCM 구형 2 차 입자 ≈5–18 µm · LGPS 불규칙 ≈1–10 µm · CT: BL20XU · 20 keV · Si(111) DCM · CMOS C13440-20CU · **화소 ≈0.5 µm** · 시야 ≈1.0 × 1.0 mm · 1800 장 / 180° · 0.05 s · Dragonfly 4.1 · **복셀 ÷ SE 입경 ≈ 1/2–1/20** (LGPS 는 2–20 복셀 · 입자 사이 ≲1 µm 기공은 못 본다 — 저자: LFP 나노 공극 *"challenging to quantify correctly due to the resolution"* p.4) · 셀: 지름 1 mm 실린더 (O-링) · 위 막대 + 나사로 누름 · 아래 막대 = 하중 센서 위 · 두 막대 = 집전체 · NCM 적재 **60 mg cm⁻²** (p.2) | [인쇄] p.2–4 · [판독] SI S1 · S2 · [카드 산술] |
| ⑤ ★ 접촉 면적 ↔ 충방전 (R_ct · 용량 · 과전압) | 같은 셀 EIS (SI S15 Nyquist · S16 회로 R_SE + (R_CT ∥ C) + ((R + Z_W) ∥ C)): **R_ct 8.65 · 4.12 · 1.66 · 0.58 × 10⁵ Ω** (6 · 12 · 51 · 102 MPa) [판독 그림 6b] — *"inversely proportional to the pressure"* ↔ 접촉 분율 (p.5) · 결론 *"an order of magnitude reduction in charge transfer resistance"* · 겉보기 전도도 **7.84 · 7.99 · 9.12 · 9.73 × 10⁻⁵ S/cm** [판독 6a] ↔ 기공 · 첫 방전 **27.4 · 39.7 · 44.1 mAh g⁻¹** · 첫 충전 44.7 · 88.5 · 162.8 [판독 그림 2b] · 한 셀 단계 상승 (S3) 용량 향상 **100 · 127 · 156 · 188 · 198 %** (6 · 12 · 25 · 50 · 100 MPa) [판독 S3b] · *"the effect of the charge transfer resistance reduction was particularly dominant"* (p.6) · 과전압 값 없음 · ⚠ 50 · 100 MPa 의 그림 6b R_ct 가 S15 의 보이는 반원 폭 (≈55 · ≈20 kΩ [판독 · 벡터]) 의 약 3 배 [카드 산술 · §3-7] | [인쇄] p.5–6 · [판독] |
| ⑥ ★ 압력 범위 (우리 300 MPa 와 나란히) | **0 · 6 · 12 · 50 · 100 MPa** (CT) · 6–100 MPa (충방전 · EIS) · 25 MPa 는 S3 한 셀에만 · 표지 위치는 6.3 · 12.6 · 51 · 102 MPa 쯤 [판독 그림 6 · S3b] · 우리 = 300 MPa [우리 CLAUDE.md] (이 논문 최고 압력의 3 배 — 판정 없이 나란히) | [인쇄] p.2–5 · [판독] |
| ⑦ 저자 한계 | 높은 적재 (1 mm 지름 · 저울 읽음 한계) · 두꺼운 전극의 불균일 반응 (p.2–3) · LGPS 산화 분해 (첫 충전 비가역) · tortuosity 는 문헌 1–10 이라 *"relative comparison"* (p.5) · LFP 나노 공극 해상도 (p.4) | [인쇄] |
| ⑧ DEM · 소성 · 2D/3D · 탈압 | DEM · 모델 **없음** · *"high pressure is applied to improve solid-to-solid contact between powders, which involves plastic deformation within composite electrodes"* (p.1) · 3D CT (방향 판단은 2D 단면) · 탈압 50 → 0 MPa: *"No clear changes were detected with respect to the void in the pressure-released condition"* (p.4 · 그림 S14 · 숫자 없음) | [인쇄] |

⛔ **한정어 (떼지 말 것)**: ① **재료가 우리 계가 아니다** — SE = **LGPS** (Li₆PS₅Cl 아님) · AM = **NCM111** (LiNbO₃ 코팅 · NCM811 아님) · 탄소 AB 4.8 wt% ② 압력 **≤ 100 MPa** · **따로 제조압 없이** 그 압력을 바로 누른 채 측정 ③ 기공 = **0.5 µm 화소 CT 의 세 상 분할** — 진밀도 · 질량 분모 없음 · 문턱 미기재 · AB 가 공극으로 분류됐는지 미기재 · 화소 아래 기공 미검출 ④ 분석 영역 = 512 × 512 × 50 µm³ (기공 · 접촉) · 36 × 36 × 50 µm³ (tortuosity) **하나씩 · 반복 없음** · 영역의 깊이 위치 미기재 ⑤ 같은 셀을 차례로 누른 것으로 읽힌다 (SI S5 의 같은 LGPS 덩어리가 모든 압력에 보임 [카드 해석]) — 원문은 그 순서를 명시하지 않았다 ⑥ tortuosity = **기하 경로 길이 ÷ 두께** (경로 추출 알고리즘 · 시작점 · 연결 규칙 미기재) — 수송 tortuosity · τ_Laplace 아님 ⑦ 이방성은 **눈으로 본 정성 진술** · 방향별 수치는 이 카드의 그림 판독 (S13) 뿐 ⑧ 셀이 **지름 1 mm** — 벽 마찰로 양극/SE 경계가 그릇 모양 (SI S6, 가운데가 가장자리의 ≈1.4–1.5 배 두께 [카드 판독]).
⇒ **절대값 전이: 0 건.**  전이되는 것은 **방향과 측정 꼴** — 단단한 AM 이 있으면 같은 압력에서 SE 층보다 복합 양극의 기공이 덜 준다 (100 MPa 23 ↔ 5 %) · 접촉 분율은 50 MPa 뒤 평탄 · 기하 tortuosity 의 평균 · 퍼짐이 100 MPa 에서 커진다 · Z 면 ↔ 옆면 접촉 비대칭 — 그리고 **누른 채 단계 CT + 같은 셀 EIS** 라는 실험 꼴.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-44 의 '왜' 칸)

의도 원문: *"i · m — 복합 양극에서 압력↑ → 공극↓ · CAM–SE 실접촉면적↑ 이지만 과압 → tortuosity↑ · 이방 접촉구조 (가압 방향 접촉↑ ↔ 측방은 pore 지배 약접촉) 라는 압력–구조 1 차 자료 · 비교 문서는 리뷰 경유 2 차 인용이라 'cite 는 1 차로'"* (가리킨 카드 = 비교 문서 `comparison_vs_ours_DEM.md` §A L456–458 · L464)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "i" (복합 양극 압력별 기공) | **채움** | 그림 3a · 3b (p.3–4): 0 · 6 · 12 · 50 · 100 MPa → **44 · 42 · 39 · 31 · 23 %** [인쇄 3b] · **누른 채** (operando 셀 · 하중 센서) · 상온 (충방전 298 K · CT 온도 미기재) · 기공 = CT 세 상 분할 (분모 = 영상 부피 · 진밀도 쓰지 않음) · 조성 1 : 1 : 0.1 wt (NCM111 : LGPS : AB) |
| "m" (받아들일 통찰) | **채움** | §8 · §9 — 누른 채 단계 CT + 같은 셀 EIS 꼴 · 접촉 분율 정의 · AM 하중 차폐의 실험 쪽 증거 (같은 압력 SE 층 5 % ↔ 복합 23 %) · 방향별 접촉 관측량 |
| "복합 양극에서 압력↑ → 공극↓" | **채움** | 44 → 23 % (0 → 100 MPa) · 12 MPa 까지는 SE 층과 비슷, 그 뒤 복합 쪽 감소가 둔해짐 (p.4) · 두 단계 치밀화: ≤ 12 MPa 는 NCM 몫 ↑ (18 → 30 %), > 12 MPa 는 LGPS 몫 ↑ (31 → 44 %) (그림 3b · p.4) |
| "CAM–SE 실접촉면적↑" | **일부** | 원문 양은 **면적이 아니라 분율** (NCM/LGPS 경계 ÷ NCM 표면) — 78.3 · 74.9 · 77.9 → 84.3 · 82.7 % [판독 3c] · 단조가 아니다 (0 MPa > 6 MPa) · **50 MPa 에서 멈춤** (p.4) · 절대 접촉 면적 (µm²) · NCM–NCM 접촉은 없다 |
| "이지만 과압 → tortuosity↑" | **채움 (한정어 셋)** | 100 MPa 에서 평균 · 퍼짐 증가 (p.5 · p.6) · 50 → 100 MPa 평균 3.83 → 5.38 · 표준편차 0.84 → 1.26 [판독 · 카드 산술] · ⚠ "과압" = 100 MPa · ⚠ 기하 경로 길이 ÷ 두께 · 압력마다 한 영역 · ⚠ 저자: *"minor impact on the electrochemical properties, since … charge/discharge … does not exhibit significant differences at pressures above 50 MPa"* (p.6) |
| "이방 접촉구조 (가압 방향 접촉↑ ↔ 측방은 pore 지배 약접촉)" | **채움 (정성) · 수치는 없음** | p.4–5 · 그림 4 · S13 — 단면을 보고 쓴 문장 · **방향별 지표 · 값 없음** · 카드 판독 (S13): Z 면 녹색 몫 0.89–0.96 ↔ 옆면 0.65–0.85 (§3-5) · ⚠ 결론의 *"marginally perpendicular to the applied pressure"* · *"improving the contact interface in the vertical direction"* (p.6) 은 p.4 의 "Z 방향 접촉 좋음" 과 낱말 쓰임이 엇갈린다 (§3-9) |
| "압력–구조 1 차 자료" | **채움** | 자체 측정 · 그림 3 · 4 · 5 · S4–S14 (단 LGPS · NCM111 · ≤ 100 MPa) |
| "비교 문서는 리뷰 경유 2 차 인용이라 'cite 는 1 차로'" | **채움** | 이 카드 = 원 논문 · 비교 문서 §A 의 [151] 줄을 이 카드로 이었다 (그 줄만 + 보탬 한 줄) |

**가리킨 카드 · 같은 논문을 옮긴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `comparison_vs_ours_DEM.md` L456–457 | *"압력↑ → porosity↓·CAM-SE 실접촉면적↑ → R_ct+R_bulk 동시↓, 단 과압 → tortuosity↑·이방 접촉구조(가압방향 접촉↑ ↔ 측방 pore-지배 약접촉 잔존)[151 Sakka JMCA 2022]"* | porosity↓ ✓ · 접촉 = **분율** ↑ (50 MPa 에서 멈춤) · R_ct↓ ✓ (×1/15) · **"R_bulk" 는 원문 양이 아니다** — 원문은 겉보기 전도도 ↑ (+24 %) · 과압 = **100 MPa** · τ = 기하 경로 · 이방성 = 정성 | **일부** — 방향은 맞고 양의 이름 둘 (접촉 면적 · R_bulk) 과 "과압" 의 크기가 원문보다 앞섬 |
| `comparison_vs_ours_DEM.md` L457–458 | *"= 우리 DEM 압력스윕·τ_Laplace 이방성 검증거리(신규)"* | 원문 τ 는 **Z 방향 기하 경로 길이 ÷ 두께** 하나뿐 — 옆 방향 τ · Laplace (수송) τ 없음 · 이방성은 **접촉** 의 방향 문제이지 τ 의 방향 문제가 아니다 | **없음** (τ_Laplace 이방성) — 견줄 자리는 우리 τ_geo (`tortuosity_SE_wall` · Dijkstra) 의 압력 변화 · AM–SE 접촉의 방향 통계 (§7-2) |
| `comparison_vs_ours_DEM.md` L464 | *"cite는 1차([151],[191] 등)로; porosity 절대값 없음(우리 Minnmann/Doux/Sakuda 유지)"* | 원 논문은 **CT 분할 기공 절대값을 준다** (복합 44 → 23 % · LGPS 층 53 → ≈5 %) — 단 LGPS · ≤ 100 MPa · 진밀도 분모 없음 | **채움** (1 차 cite 원칙) · "porosity 절대값 없음" 은 리뷰에 대한 말 (원 논문에는 있다) |
| `comparison_vs_ours_DEM.md` L450 | 리뷰 카드 경로 *"papers/li2026_sulfide_stability_review_ecer.md"* | 정본 `papers/` 에 그 파일 없음 — 정본 리뷰 카드 = `fan2026_sulfide_assb_stability_review_ECERD2600097` (CLAUDE.md 의 litdb 정본 규칙) | **카드 문제** (링크가 동결 사본 이름) — 보고만 |
| `tailored_cathode_microstructure_low_pressure_assb` L78 | *"Sakka(Sakuda) et al.(ref 12)이 X선 CT로 50 MPa에서 SE가 내부 cavity를 채워 접촉면적↑·R_ct↓(12 MPa 이하 대비)를 보였으나"* | 1저자 = **Yuya Sakka** (Ritsumeikan · 교신 Orikasa) — "Sakuda" 는 다른 연구자 · *"at high pressures, LGPS fills the voids around the NCM particles, resulting in an increased contact area"* · ≈10 % (> 50 vs ≤ 12 MPa) · R_ct 역비례 ✓ | **일부** — 내용은 맞고 저자 표기가 틀림 |
| `tailored_cathode_microstructure_low_pressure_assb` L78 | *"모델 연구는 25 MPa면 안정 계면접촉에 충분(ref 12 모델)"* | 이 논문에 **모델이 없고 25 MPa 진술도 없다** (25 MPa 는 S3 한 셀의 한 단계일 뿐 · 그 셀의 용량 향상 156 %) | **없음** — 다른 문헌이 섞인 것으로 보인다 [카드 해석] |
| `jeong2024_…` L355 ([22]) | 서지 *"Y. Sakka, H. Yamashige, A. Watanabe, A. Takeuchi, M. Uesugi, K. Uesugi, Y. Orikasa, J. Mater. Chem. A 2022, 10, 16602."* · 이유 *"복합 양극 미세구조 ↔ 반응 부피"* | 서지 ✓ (원문 1 쪽) · Jeong 원문 문장 *"The composite cathode microstructure (e.g. solid-electrolyte-cathode contact area and density of voids) is responsible for the reaction volume … [21,22]"* ↔ 이 논문 *"The contact area between NCM and LGPS serves as a reactive area for charge-transfer"* (p.4) | **채움** |
| `fan2026_sulfide_assb_stability_review_ECERD2600097` L172 | *"성형압: 압↑→기공↓접촉↑이나 과압은 채널 꼬임·이방성 접촉(Fig 10b)"* | 같은 내용 · 과압 = 100 MPa · 채널 꼬임 = 기하 경로 τ | **채움** (크기 한정 빠짐) |

⇒ **의도 대조 결과: 채움 (i · m · 공극↓ · 과압 τ↑ (100 MPa · 기하 경로) · 이방 접촉 (정성) · 1 차 자료 · 1 차 cite) · 일부 (접촉 "면적" = 분율 · 50 MPa 에서 멈춤) · 없음 (방향별 수치 — 원문에 없음 · τ_Laplace 이방성 — 원문에 없음)**.  2 차 인용은 방향이 맞고, "R_bulk" · "실접촉면적" · "τ_Laplace" · "25 MPa 모델" 네 표현이 원문보다 앞서 나갔다.

---

## 1. 한 줄 요약
황화물 고체 전지의 복합 양극을 **따로 성형하지 않고**, 지름 1 mm 의 전기화학 + X 선 CT 겸용 셀에서 하중 센서로 압력을 보며 0 → 6 → 12 → 50 → 100 MPa 로 눌러 단계마다 싱크로트론 CT (0.5 µm) 와 EIS 를 함께 잰 연구다.
기공은 복합 양극 44 → 23 % · LGPS 층 53 → 5 % 로 줄고 (12 MPa 위에서 복합만 덜 줄어듦 — 단단하고 큰 NCM 이 하중을 먼저 받아 틈이 "저압 자리" 가 됨), NCM 표면의 LGPS 접촉 분율은 ≈75–78 → 83–84 % 로 늘다가 50 MPa 에서 멈추며, 그만큼 R_ct 가 865 → 58 kΩ 으로 떨어져 방전 용량이 늘었다.
SE 경로의 기하 tortuosity 는 50 MPa 까지 줄지만 100 MPa 에서 다시 커지고 퍼진다 (AM 이 장애물이 되는 효과가 기공 감소를 이김 — 저자 해석).  단면을 보면 NCM 의 **위 · 아래 면은 LGPS 와 붙고 옆면은 공극과 닿는** 이방성이 있어, 일축 가압의 한계 (옆에서 미는 힘이 없음) 를 보여준다는 것이 결론이다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (AM / SE / 도전재 · 음극) | 연구유형 |
|---|---|---|---|---|
| Y. Sakka · H. Yamashige · A. Watanabe · A. Takeuchi · M. Uesugi · K. Uesugi · Y. Orikasa\* (Ritsumeikan · Toyota · JASRI) | *J. Mater. Chem. A* 10 (2022) 16602–16609 · Paper · CC BY 4.0 | 10.1039/D2TA02378D | **LiNbO₃ 코팅 LiNi₀.₃₃Co₀.₃₃Mn₀.₃₃O₂** (NCM · 공급사 [미확인]) / **Li₁₀GeP₂S₁₂** (자체 550 °C 합성) / **아세틸렌 블랙** (Denka) · 바인더 없음 · 음극 **In–Li** (In 박 Nilaco + Li 박 Honjo Metal 압착) | 실험 — operando 셀 X 선 CT (SPring-8 BL20XU) · 세 상 분할 · 접촉 분율 · 기하 tortuosity · EIS · 정전류 |

- **1저자 메모와의 대조**: 저자 일곱 · 제목 *"Pressure dependence on the three-dimensional structure of a composite electrode in an all-solid-state battery"* · J. Mater. Chem. A 10 (2022) 16602–16609 · DOI 10.1039/D2TA02378D · CC BY 4.0 — PDF 1 쪽 · 메타데이터 (Subject 줄) 와 **모두 같다**.  덧붙임: 원문 인쇄 DOI 는 소문자 `10.1039/d2ta02378d` · CC 표지는 *"Licensed under CC-BY 4.0"* (p.1 오른쪽 위).
- 글의 꼴: Introduction → Experimental terms → Results and discussion → Conclusions (번호 없는 절) — 본문 그림 7 · **표 0 · 식 0** · 참고문헌 44 · ESI = 표지 (S.1–S.5 목차) + 그림 S1–S16 (표 · 식 없음).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 재료 · 조성 · 셀 · 압력 (p.2 · `txt_p2_materials_cell.png` · `txt_p2_cell_6mpa_loading.png` · 그림 1)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 양극 활물질 | **LiNbO₃ 코팅 LiNi₀.₃₃Co₀.₃₃Mn₀.₃₃O₂ (NCM)** · 코팅 = *"rolling fluidised coating machine (MP-01, Powrex)"* · 절차는 ref 35 (Ohta 2007) · 두께 · 공급사 [미확인] | [인쇄] p.2 |
| 고체 전해질 | **Li₁₀GeP₂S₁₂ (LGPS)** · *"solid-state reaction at 550 °C under an Ar flow"* · σ · 결정상 확인 [미확인] | [인쇄] p.2 |
| 도전재 | **아세틸렌 블랙 (AB)** · *"DENKA BKACK, Denka Co., Ltd"* (인쇄 오타) | [인쇄] p.2 |
| 혼합 | 막자사발 · Ar 글러브박스 · **질량비 1 : 1 : 0.1** (NCM : LGPS : AB) · 바인더 없음 · 시간 [미확인] | [인쇄] p.2 |
| vol% (원문 없음) | NCM 4.7 [다른 카드 `landesfeind2016_tortuosity_eis_electrodes_separators` 의 NMC111 4.7 g/cm³] · LGPS 2.05 [다른 카드 `kamaya2011_lgps_lithium_superionic_conductor` 의 X 선 밀도 산수] · AB 1.9 [가정 — `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` 의 Super C65 값 · 다른 탄소] → **NCM 28.2 · LGPS 64.8 · AB 7.0 vol%** · LGPS/NCM 부피비 2.29 · 고체 밀도 2.79 g/cm³ | [카드 산술] |
| 셀 | 양극 복합체 **1.0 mg** · 전해질 **1.0 mg** · In–Li 박을 **지름 1 mm** 실린더에 넣음 · O-링 밀봉 · 위쪽 나사로 적층압 조절 (p.2) · 위 스테인리스 막대로 누르고 아래 막대는 **하중 센서 (load-sensing transducer)** 위 · 두 막대 = 집전체 · 같은 셀에서 압력을 바꾸며 충방전 + CT (p.2 · 그림 1) · 실린더 재질 [미확인] | [인쇄] p.2 |
| 적재 | NCM **60 mg cm⁻²** (*"much higher than the reported condition … due to the electrode diameter of 1 mm and the readability of the precision electronic balance"*) ↔ 1.0 mg × (1/2.1) ÷ π(0.05 cm)² = **60.6 mg cm⁻²** | [인쇄] p.2 · [카드 산술] |
| 충방전 | 298 K · HJ1001SDE (Hokuto Denko) · 0.01C · 2.0–4.0 V (vs In–Li, 그림 축) · C 의 기준 용량 [미확인] | [인쇄] p.2 · [판독] 그림 2 |
| 압력 단계 | CT · EIS: **0 · 6 · 12 · 50 · 100 MPa** (0 = 넣은 가루, 누르기 전 [카드 해석]) · 정전류: 셀마다 6 · 50 · 100 MPa (그림 2b) + 한 셀을 6 → 12 → 25 → 50 → 100 MPa 로 두 사이클씩 (그림 S3) · **유지 시간 · 가압 속도 · 각 단계의 CT 전 대기 [미확인]** · 표지 위치는 6.3 · 12.6 · 51 · 102 MPa 쯤 (실측 압력으로 찍힌 것으로 보인다 [카드 해석]) | [인쇄] p.2–4 · [판독] |
| 제조압 | **없음** — *"Since no pressure was added during fabrication in our experiments, the pressure shown in this study corresponds to the previously reported fabrication pressure"* (p.3) — 적층압 = 제조압 한 값 | [인쇄] p.3 |

### 3-2. ★ CT 조건 · 분할 · 분석 영역 · 해상도 (p.2–3 · `txt_p2_ct_conditions.png` · `txt_p3_ct_region_segmentation.png` · SI S4–S11)
- **장비**: SPring-8 BL20XU · 단색 **20 keV** (undulator · Si(111) 이중 결정 단색기) · 가시광 변환형 검출기 + CMOS (C13440-20CU, Hamamatsu) · **화소 ≈0.5 µm** · **시야 ≈1.0 × 1.0 mm** · **1800 투영 / 180°** · 노출 0.05 s · 재구성 = BL20XU 쪽 (기여 문단 p.6) · 알고리즘 [미확인] · 공간 분해능 (화소 아닌 실제) [미확인].
- **분할**: Dragonfly 4.1 (Object Research Systems) · *"The proportions of NCM, LGPS, and voids were identified based on the transmission intensity (Fig. S7–S11)"* (p.3) · **문턱 값 · 필터 · 부분 부피 처리 [미확인]** · SI S7–S11 = 각 압력의 회색조 (x-y · y-z · z-x) + 세 상 결과 (보라 = AM · 녹 = 전해질 · 청 = 기공).  **AB 의 분류 [미확인]** — AB 는 X 선 흡수가 작아 공극 쪽으로 갈 수 있다 [카드 해석] (park2025 카드는 같은 문제로 '공극 + 탄소' 한 클래스를 인쇄했다 [다른 카드]).
- **분석 영역**: 기공 · 부피 · 접촉 = **512 × 512 × 50 µm³** (*"cropped from the obtained three-dimensional images"*) · tortuosity = **36 × 36 × 50 µm³** (p.5) · 영역의 깊이 위치 · 개수 · 같은 영역을 압력마다 따라갔는지 [미확인] (SI S7–S11 의 y-z · z-x 단면이 50 µm 두께 판 = 화소 ≈100 개 [카드 산술 50 / 0.5]).
- **입경 ↔ 화소** (★ 1저자 질문 ④): NCM *"on the order of 10 µm"* (p.4) · SI S1 [판독 · 대략 — 10 µm 눈금 막대 = 109 원본 화소로 입자 몇 개를 잼] 구형 2 차 입자 ≈5–18 µm → **10–36 화소/지름** · LGPS SI S2 [판독 · 대략 — 10 µm = 104 화소] 불규칙 입자 ≈1–10 µm (응집 포함 더 큼) → **2–20 화소/지름** · 막자사발 혼합 뒤의 LGPS 크기 [미확인].  ⇒ LGPS 입자 자체는 대부분 풀리지만 **입자 사이 ≲ 1 µm (2 화소) 기공은 분할에서 빠진다** — 저자도 LFP 전극 (입자 수백 nm) 에 대해 *"nanoscale voids, which is challenging to quantify correctly due to the resolution of X-ray CT"* (p.4) 라고 적었다 → **CT 기공은 하한일 수 있다** [카드 해석].

### 3-3. ★ 압력별 기공 · 부피 분율 (p.3–4 · 그림 3a · 3b · `fig_3a.png` · `fig_3b.png` · `txt_p4_porosity_two_stage.png`)
| 압력 (MPa) | 복합 양극 기공 % [인쇄 3b] (표지 [판독 3a]) | LGPS 층 기공 % [판독 3a] | NCM % [인쇄 3b] | LGPS % [인쇄 3b] | LGPS/NCM 부피비 [카드 산술] |
|---|---|---|---|---|---|
| 0 (가루) | **44** (44.2) | **53.0** | 18 | 38 | 2.11 |
| 6 | **42** (42.3 — 빨간 원에 일부 가림) | **40.9** | 25 | 33 | 1.32 |
| 12 | **39** (표지가 빨간 원 뒤에 숨음) | **39.0** | 30 | 31 | 1.03 |
| 50 | **31** (30.6) | **15.0** | 29 | 41 | 1.41 |
| 100 (≈101) | **23** (22.9) · 본문 23 % | **4.3** · 본문 *"5%"* | 33 | 44 | 1.33 |

- 저자 서술 (p.4): *"there is no great difference between the composite electrode layer and the SE layer at pressures of less than 12 MPa. However, at high pressures, the pressure dependence of the porosity of the composite electrode is reduced."* · 원인 = NCM 의 높은 영률 (ref 37) 과 큰 입경 · *"Hard NCM particles are slightly deformed by applied pressure and the NCM particle size is larger than that of LGPS, resulting in more voids around the NCM particles."*
- **두 단계 치밀화** (p.4): ≤ 12 MPa — *"The proportion of LGPS decreases while the proportion of NCMs increases"* (NCM 18 → 30 %) · *"In composites with different Young's moduli, large pressures can be applied to materials that have larger Young's moduli"* (ref 25) · *"This also causes the soft LGPS to contract (ref 38), thus reducing the apparent volume fraction."* · > 12 MPa — *"the volume of NCM does not increase, and the porosity decreases due to the increasing LGPS"* (31 → 44 %) · *"The volume ratio of NCM and LGPS does not follow the relative modulus because the direction of pressure is in one direction, and the particle size and shape are also different between NCM and LGPS."*
- ⚠ **[카드 산술 · 카드 해석] 조성이 압력마다 같아야 한다**: 같은 가루의 고체 부피비는 압력과 무관해야 하는데 분할된 LGPS/NCM 부피비가 **2.11 → 1.32 → 1.03 → 1.41 → 1.33** 으로 흔들리고, 명목 (1 : 1 wt, 가정 밀도) **2.29** 에 0 MPa 만 가깝다.  저자는 *"soft LGPS to contract"* 로 설명하지만 고체 하나가 12 MPa 에서 부피를 수십 % 줄이려면 체적탄성률이 ≈ 0.012 GPa / 0.37 ≈ **30 MPa** 여야 한다 [카드 산술] — 황화물 고체의 체적탄성률은 GPa 급 (예: 우리 LPSCl DFT B₀ 26.23 GPa [우리 · 다른 재료]) 이다.  ⇒ 분할 (부분 부피 · 문턱) · 영역 표본 (NCM 이 많은 곳) · 화소 아래 LGPS 기공의 차이일 가능성이 크다 [카드 해석] — 원문으로 가릴 수 없다.
- **[카드 산술] Heckel 꼴 (판독 기공 · 누른 채 · 세 점 12 · 50 · 101 MPa)**: ln(1/ε) = K·P + A → **LGPS 층 K = 0.0248 MPa⁻¹ · P_y ≈ 40 MPa** (R² 1.000 · 다섯 점이면 41 MPa · R² 0.998 · 본문 5 % 를 쓰면 43 MPa) · **복합 양극 K = 0.0060 MPa⁻¹ · P_y ≈ 168 MPa** (R² 0.999 · 다섯 점 155 MPa).  ⇒ 같은 셀 · 같은 압력에서 단단한 NCM 이 섞이면 겉보기 항복 압력이 **≈4 배** 오른다 [카드 산술] — 원문은 Heckel 을 쓰지 않았다.
- **[카드 판독 + 카드 산술] 질량 ↔ 두께 ↔ CT 기공 대조 (SI 그림 S6 · 500 µm 막대 = 180 화소 → 2.78 µm/화소 · 열 창 28 개)**: 층 두께 평균 = 양극 **388 · 345 · 298 · 291 µm** · LGPS 층 **355 · 322 · 243 · 223 µm** (6 · 12 · 50 · 100 MPa · ±10 %) · 양극/SE 경계는 **그릇 모양** (가운데 ≈1.4–1.5 × 가장자리).
  · 두께 비 대조: 양극 t₁₀₀/t₆ = **0.750** ↔ CT 기공이 주는 (1 − 0.424)/(1 − 0.229) = **0.748** · LGPS 층 **0.628** ↔ (1 − 0.409)/(1 − 0.043) = **0.617** — **CT 기공의 압력 변화는 두께 변화와 2 % 안에서 맞는다** (같은 셀을 차례로 누른 것과 일관).
  · 절대 질량: 두께 × (1 − ε) = 양극 207–224 µm · LGPS 197–213 µm 의 고체 ↔ 진술 1.0 mg 이면 양극 **457 µm** · LGPS **621 µm** (가정 밀도) → CT 단면 속 고체는 진술 질량의 **≈47 % · ≈33 %** (≈0.47 · ≈0.33 mg 상당) 뿐 [카드 산술 · 가정 밀도].  ⇒ "1.0 mg" (저울 읽음 한계 문장 p.2) 이 이 CT 셀에 그대로 들어갔다고 볼 수 없다 · **기공을 질량으로 다시 셀 수 없다** — 어느 쪽이 틀렸는지는 원문으로 가릴 수 없다.

### 3-4. ★ NCM/LGPS 접촉 면적 분율 · 탈압 (p.4 · 그림 3c · S13 · S14 · `fig_3c.png` · `txt_p4_contact_fraction_release.png`)
- **정의** (p.4): *"The contact area fraction represents the fraction of the area in contact between NCM and LGPS with respect to the surface area of the NCM particles (Fig. S13)."* · *"The contact area between NCM and LGPS serves as a reactive area for charge-transfer during charge/discharge."* · 계산 = 분할된 NCM 경계 화소를 NCM/LGPS (녹) · NCM/공극 (청) 으로 나눈 것으로 보인다 (SI S13 범례) [카드 해석] · 표면적 계산법 (복셀 면 수 · 메시) · NCM–NCM 맞닿은 면 · NCM–AB 면의 처리 [미확인].
- **값 [판독 그림 3c]**: **78.3 (0) · 74.9 (6) · 77.9 (12) · 84.3 (50) · 82.7 % (101 MPa)** · 본문 *"increases by approximately 10% when the pressure is greater than 50 MPa compared with the state under a pressure less than or equal to 12 MPa"* ↔ [카드 산술] 평균 77.0 → 83.5 % (+6.5 %p · ×1.08) · 6 → 50 MPa 는 +9.4 %p (×1.13) — "10 %" 가 %p 인지 상대 % 인지 원문이 가리지 않는다.
- 저자 해석 (p.4): 낮은 압력에서는 *"the NCM particles are pressurised preferentially (ref 24), and so contact with the surrounding LGPS is not increased"* · 높은 압력에서는 *"LGPS fills the voids around the NCM particles"* · *"the improvement in the contact area fraction stopped when the pressure reached 50 MPa. After 50 MPa, there is a small change in the volume of the voids, but no change in the contact area fraction."*
- **★ 탈압 (단계 6 쪽 · 질문 b)**: *"we compared X-ray CT images of the composite electrode under 50 MPa press and at 0 MPa after 50 MPa press (Fig. S14). No clear changes were detected with respect to the void in the pressure-released condition."* (p.4) — **XY 단면 한 장씩 · 숫자 (기공 · 두께 · 되돌아옴) 없음** · 같은 셀로 보인다 (밝은 덩어리가 같은 자리 [카드 해석]) · 100 MPa 에서 뺀 상태 · 유지 시간 [미확인].

### 3-5. ★ 이방 접촉 (p.4–5 · 그림 4 · SI S13 · `fig_4a.png`–`fig_4c.png` · `fig_S13.png` · `txt_p4_p5_anisotropy.png`)
- **원문 (정성)**: *"During uniaxial pressing, the anisotropy phenomenon occurs within the contacted state between NCM and LGPS. … Detailed observations of these images reveal that the NCM particles have good contact with LGPS in the Z-axis direction, which is the pressure direction. On the other hand, preferential contact with the voids is observed in the horizontal direction, which is not the pressure direction. Such anisotropy of the contacted interface is predominantly observed at low pressures, but also even at high pressures, though less frequently. Therefore, it can be concluded that NCM does not have good contact with LGPS horizontally, even at high pressures. In addition, as shown in Fig. 4c, many voids in the horizontal direction can be confirmed and the shape of the voids depends on the pressure direction."* (p.4–5) · 그림 4a 의 단면 = 압력마다 XY · YZ · XZ 한 장씩 (≈45 µm 칸 · 10 µm 막대) · 그림 4c = 6 · 100 MPa 3D (노란 타원 = 옆으로 긴 공극).
- **방향별 지표 · 값: 원문에 없다.**
- **[카드 판독 · 원문에 없는 지표] SI 그림 S13 (XZ 단면 512 × 50 µm · 압력마다 한 장 · 원본 984 × 532 화소 ≈0.52 µm/화소)** — 녹 (NCM/LGPS) · 청 (NCM/공극) 경계 화소를 그 자리의 바깥 법선 (가우시안 2 화소로 부드럽게 한 NCM 마스크의 기울기) 방향으로 나눔 · Z 면 = |n_Z| ≥ cos 45° · 글자 · 눈금 막대 · 띠 가장자리 화소 제외 (`digitized.csv` figS13_readout · 스크립트는 큐레이터 작업 폴더):

| 압력 (MPa) | 녹색 몫 전체 | Z 면 (위 · 아래) | 옆면 (X) | 위 면 ↔ 아래 면 | |n_Z| 0–0.25 → 0.75–1 (네 칸) | 그림 3c 접촉 분율 [판독] |
|---|---|---|---|---|---|---|
| 0 | 0.82 | **0.93** | **0.66** | 0.93 ↔ 0.92 | 0.54 · 0.63 · 0.80 · 0.93 | 78.3 % |
| 6 | 0.80 | **0.89** | **0.65** | 0.90 ↔ 0.89 | 0.61 · 0.61 · 0.75 · 0.90 | 74.9 % |
| 12 | 0.82 | **0.92** | **0.68** | 0.93 ↔ 0.91 | 0.60 · 0.67 · 0.77 · 0.93 | 77.9 % |
| 50 | 0.91 | **0.96** | **0.85** | 0.96 ↔ 0.95 | 0.83 · 0.84 · 0.87 · 0.96 | 84.3 % |
| 100 | 0.85 | **0.93** | **0.74** | 0.95 ↔ 0.92 | 0.66 · 0.73 · 0.83 · 0.94 | 82.7 % |

  · 원문 진술과 같은 방향: 모든 압력에서 **Z 면이 옆면보다 녹색 (LGPS 접촉) 몫이 0.11–0.27 크다** · 법선이 Z 에 가까울수록 단조 증가 · 차이는 0–12 MPa 에서 가장 크고 (0.24–0.27) 50 MPa 에서 가장 작다 (0.11) — *"predominantly observed at low pressures, but also even at high pressures"* 와 맞음.
  · 이 판독의 전체 녹색 몫 (0.80–0.91) 은 그림 3c (74.9–84.3 %) 보다 3–7 %p 높지만 **압력 순서가 같다** (50 > 100 > 0 ≈ 12 > 6) — 판독 방법이 원문의 3D 값과 같은 쪽으로 움직인다는 대조.
  · 한정: 2D 단면 하나 · 그림 화소 (테두리 선 굵기 · 압축) · 위 · 아래 면 차이 (≤ 0.03) 는 판독 잡음 안 · 원문의 양이 아니다 — 인용할 때 반드시 [카드 판독] 으로.

### 3-6. ★ tortuosity (p.5–6 · 그림 5 · `fig_5a.png`–`fig_5c.png` · `txt_p5_tortuosity.png` · `txt_p6_tortuosity_tradeoff.png`)
- **정의** (p.5): *"Fig. 5a shows the analysed area, which was 36 × 36 × 50 µm³ … In the calculation, a three-dimensional pathway connected by SE particles was extracted in the composite electrode (Fig. 5a), and this value was divided by the thickness of the observed region (Fig. 5b)."* · 그림 5b = 2D 모식 (LGPS 녹 · 나머지 검정 · 'in' → 'out' 노란 경로) · 그림 5c = 압력마다 **N = 100** 경로의 히스토그램 (가로 = *"flexural index"*) · 빨간 원 = 최빈 · 파란 원 = 최소 · **경로 추출 알고리즘 (최단 경로 · 골격 · 연결 규칙) · 시작점 100 개를 고른 법 · 경로 길이의 단위 계산 [미확인]**.
- 문헌 범위 1–10 이라 *"this study discusses a relative comparison with the pressure"* (p.5).
- **[판독 그림 5c · 0.1 칸 막대를 눈금 격자로 셈 · 카드 산술]** (칸 중심 · 표본 표준편차 · 압력마다 읽힌 합 98–101 ↔ 인쇄 N = 100):

| 압력 (MPa) | 평균 | 중앙 | 표준편차 | 사분위 25–75 | 최소 칸 (파란 원) | 최빈 칸 (빨간 원) | 최대 칸 | ≥ 6 의 몫 |
|---|---|---|---|---|---|---|---|---|
| 0 | **6.54** | 6.35 | 1.12 | 5.75–7.15 | 4.45 | 5.65 | 10.85 | 62 % |
| 6 | **5.27** | 5.15 | 0.97 | 4.75–5.55 | 3.45 | 5.15 | 9.35 | 11 % |
| 12 | **4.51** | 4.45 | 0.69 | 3.95–4.85 | 3.35 | 4.65 · 4.75 | 6.25 | 4 % |
| 50 | **3.83** | 3.75 | 0.84 | 3.25–4.25 | 2.45 | 3.75 | 5.85 | 0 % |
| 100 | **5.38** | 5.2 | 1.26 | 4.55–6.15 | 2.75 | 5.55 | 8.65 | 28 % |

  · 원문 진술 (*"Minimum and mode values decrease with increasing pressure. In contrast, when the pressure was 100 MPa, the tortuosity had increased and so had the variation."* p.5 · *"a reduced change in the minimum value of the tortuosity but … an increase in the average tortuosity"* p.6) 과 판독이 같다: 최소는 2.45 → 2.75 로 거의 그대로, 평균은 3.83 → 5.38, 퍼짐은 0.84 → 1.26.
- **저자 기전 (p.6)**: *"There are two factors that change the tortuosity in composite electrodes: it decreases with the increased volume of the void and increases with the increased volume of the AMs. … For small-sized voids, large NCMs act as obstacles in the Li-ion pathway. Therefore, at 100 MPa when the AMs are well filled, the effect of increasing the AM is superior to the effect of decreasing the porosity, resulting in high tortuosity."* · *"the increase of the tortuosity reduces the effective ionic conductivity, which directly leads to a decrease in rate capability"* (ref 44) · 그러나 *"minor impact … since the pressure dependence of the charge/discharge measurement does not exhibit significant differences at pressures above 50 MPa"*.
- ⚠ [카드 해석] **압력마다 36 × 36 × 50 µm³ 하나** — NCM (≈10 µm) 이 가로로 3–4 개 들어가는 크기라 100 MPa 의 증가가 표본 (어느 NCM 이 영역에 들어왔나) 차이일 수 있다 · 반복 · 영역 위치 [미확인] · 이 값들은 **기하 경로 τ** (최단 경로라면 우리 τ_geo 와 같은 이름) 로, 우리 LHS-130 벽 기준 Dijkstra τ_geo 1.29–4.15 [우리 CLAUDE.md J20-n] 보다 훨씬 크다 — 경로 추출 규칙이 달라서일 수 있다 (§7-2).

### 3-7. 전기화학 (p.2–3 · p.5 · 그림 2 · 6 · SI S3 · S15 · S16)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 6 MPa 고정 10 사이클 (그림 2a · 0.01C) | 충전 끝 (4.0 V) **44.6 · 23.6 · 16.4 · 12.0 · 9.0 · 7.2 · 5.7 · 4.6 · 4.0 · 3.6** · 방전 끝 (2.0 V) **27.1 · 18.2 · 13.1 · 9.7 · 7.2 · 5.6 · 4.5 · 3.8 · 3.3 · 2.9 mAh g⁻¹** · 10 사이클 유지 10.6 % [카드 산술] · 저자: *"Because a pressure of 6 MPa is very small, both the capacity and cycling performance are low"* · NCM 부피 변화로 *"specific spots"* 의 접촉이 떨어져 감소 | [판독] · [인쇄] p.2–3 |
| 셀마다 첫 사이클 (그림 2b) | 6 MPa 충 **44.7** / 방 **27.4** · 50 MPa **88.5 / 39.7** · 100 MPa **162.8 / 44.1 mAh g⁻¹** · 첫 효율 61 · 45 · 27 % [카드 산술] · 방전 ×1.45 · ×1.61 (6 → 50 · 100) [카드 산술] · 큰 첫 충전 = *"irreversible capacity due to oxidative decomposition of the electrolyte"* (ref 36) · 6 MPa 곡선은 그림 2a 첫 사이클과 같다 [판독] | [판독] · [인쇄] p.3 |
| 한 셀 단계 상승 (SI S3) | 같은 셀 방전 끝 [판독 · 대략, 실선/점선을 순서로 가름] **35.1 (6 MPa 1) · 20.3 (2) · 20.9 · 17.5 (12 MPa) · 19.8 · 17.4 (25) · 21.7 · 18.2 (50) · 14.3 · ≈10.4 (100 MPa)** · S3b 용량 향상 **100 · 126.8 · 155.8 · 188.3 · 197.5 %** (6.3 · 12.6 · 25.7 · 51.0 · 102 MPa) [판독] · 캡션: *"The discharge capacity of the latter measurements is divided by that of the former at the same cycle … 200% indicates that the capacity is twice the baseline rate (6 MPa)"* · ⚠ S3a 값과 그림 2a (6 MPa 고정 셀) 의 같은 사이클 값으로 127 · 156 · 188 · 198 % 를 **재현하지 못했다** (예: 12 MPa 3 번째 20.9 ÷ 그림 2a 3 번째 13.1 = 159 %) — 계산 규칙 [미확인] · 결론의 *"logarithmic increase"* ↔ [카드 산술] ln P 당 기울기 38 · 41 · 47 → 13 %/ln (50 → 100 MPa 에서 포화) | [판독] · [인쇄] SI p.4 · p.6 |
| 겉보기 전도도 (그림 6a) | **7.84 · 7.99 · 9.12 · 9.73 × 10⁻⁵ S/cm** (6.3 · 12.6 · 50.9 · 101.8 MPa) · +24 % [카드 산술] · *"increases almost linearly with increasing pressure. This corresponds well to the behaviour of the porosity reduction"* · 어느 저항 (R_SE ?) · 두께 · 면적으로 환산했는지 [미확인] | [판독] · [인쇄] p.5 |
| R_ct (그림 6b) | **8.65 · 4.12 · 1.66 · 0.58 × 10⁵ Ω** (6.4 · 12.5 · 51.0 · 102.0 MPa) · ×1/14.9 [카드 산술] · 면적 0.00785 cm² 이면 **6.8 · 3.2 · 1.3 · 0.46 kΩ cm²** [카드 산술] · 맞춤 회로 = SI S16 (R_SE + (R_CT ∥ C) + ((R + Z_W) ∥ C)) · 맞춤 값 표 · 주파수 범위 · 진폭 [미확인] | [판독] · [인쇄] p.5 |
| Nyquist (SI S15 · 벡터) | 6 MPa: 반원 꼭대기 Z″ ≈ 410 kΩ (Z′ ≈ 458) · 반원 뒤 최소 Z″ ≈ 119 kΩ (Z′ ≈ 986) · 12 MPa: 꼭대기 ≈ 178 (Z′ ≈ 259) · 최소 ≈ 55 (Z′ ≈ 450–463) · 50 MPa: 반원 Z′ ≈ 35 → 최소 Z″ ≈ 6.3 (Z′ ≈ 88–90) · 100 MPa: Z′ ≈ 14–19 → 최소 Z″ ≈ 3.0 (Z′ ≈ 34–35) kΩ [판독 · 벡터] · 높은 주파수 쪽 점 몇 개는 Z″ < 0 (틀 밖 · 그림에서 잘림) | [판독 · 벡터] SI p.16 |
| ⚠ R_ct ↔ 반원 폭 | 보이는 반원 폭 ≈ **880 · 400 · 55 · 20 kΩ** [판독 · 벡터 · 카드 산술] ↔ 그림 6b **865 · 412 · 166 · 58 kΩ** — 6 · 12 MPa 는 같고 **50 · 100 MPa 는 그림 6b 가 약 3 배** · 맞춤의 어느 요소가 R_CT 인지 · 두 RC 중 어느 쪽에 낮은 주파수 꼬리가 들어갔는지 원문이 적지 않았다 [미확인] | [카드 산술] |
| 저자의 연결 | *"The increase in the capacity of the charge/discharge reaction (Fig. 1) is mainly attributed to the improved interface between NCM and LGPS, resulting in a reduction of the charge-transfer resistance."* (p.5 — 용량은 그림 2 인데 "Fig. 1" 로 인쇄) · 결론: R_ct 감소 효과가 *"particularly dominant"* | [인쇄] p.5–6 |

### 3-8. LFP 대조 (p.4 · SI S12 · `fig_S12.png` · `txt_p4_lfp_nanovoids.png`)
- *"We examined X-ray CT analysis of the LiFePO₄ (LFP) electrode as the composite electrode with hundreds of nanometer-sized particles of AM (Fig. S12). The void ratio is approximately 5% at 50 MPa, which is much lower than that of the micron-sized NCM electrode. This result implies that the small particles can fill the large void spaces. However, note that the small size of LFP particles tends to form nanoscale voids, which is challenging to quantify correctly due to the resolution of X-ray CT."* — LFP 전극 조성 · SE · 방법 [미확인] (SEM 1 µm 막대 · CT 단면 한 장).

### 3-9. ★ 저자가 적은 한계 · 원문 안 어긋남
**원문이 스스로 적은 것**
1. 적재 60 mg cm⁻² 가 *"much higher than the reported condition"* (1 mm 지름 · 저울) · 두꺼운 전극의 *"inhomogeneous charge/discharge reaction due to the high ionic resistance in through-plain direction"* (p.2–3).
2. LGPS 산화 분해로 첫 충전 비가역 (p.3 · ref 36).
3. tortuosity 는 문헌 1–10 → 상대 비교만 (p.5) · LFP 나노 공극은 CT 해상도로 못 셈 (p.4).
4. tortuosity 증가의 영향은 작을 것 (50 MPa 위 용량 차이 없음) (p.6).

**카드가 본 어긋남 (원문 문장 · 그림끼리)**
5. p.5 *"This corresponds to the increase of the contact area fraction of NCM/LGPS as shown in Fig. 3b"* — 접촉 분율은 **그림 3c** · *"capacity … (Fig. 1)"* — 용량은 **그림 2 · S3**.
6. *"NMC/LGPS"* (그림 4 · S13 캡션 · p.4) = NCM 오타 · *"DENKA BKACK"* (p.2) · *"through-plain"* (p.3).
7. **결론 낱말**: *"The contact interface between the AM and the SE was marginally perpendicular to the applied pressure. By improving the contact interface in the vertical direction …"* (p.6) ↔ p.4 *"good contact with LGPS in the Z-axis direction, which is the pressure direction"* — "vertical" 이 옆면 (세로 면) 을 뜻하는지 Z 방향을 뜻하는지 원문이 가리지 않는다 [카드 해석: 옆면 (법선이 수평) 접촉을 늘리라는 뜻으로 읽힌다].
8. **분할 조성** (§3-3): LGPS/NCM 부피비 2.11 → 1.03–1.41 (명목 2.29) · 저자의 "LGPS 수축" 설명은 크기가 맞지 않는다 [카드 산술].
9. **질량 · 두께** (§3-3): CT 단면 속 고체 = 진술 질량의 ≈47 % (양극) · ≈33 % (LGPS) [카드 산술 · 가정 밀도].
10. **R_ct ↔ S15** (§3-7): 50 · 100 MPa 에서 ≈3 배 [카드 산술].
11. **S3b 계산 규칙** (§3-7): 재현 안 됨 [카드 산술].
12. p.6 *"Under uniaxial pressing, the voids in the composite electrodes that contain AMs have a large Young's modulus that is not sufficiently reduced."* — 공극의 영률이라는 문장의 뜻이 원문에서 풀리지 않는다 [카드 해석: AM 이 든 복합체의 공극이 잘 줄지 않는다는 뜻으로 읽힌다].
13. SI 목차 S.2 *"under various pressures"* ↔ 본문 쪽 머리 *"under various fabrication pressures"* (SI p.4) — 같은 실험.

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 사슬
가루 (NCM111-LiNbO₃ · LGPS · AB) → 막자사발 1 : 1 : 0.1 → 지름 1 mm 실린더에 양극 1.0 mg · LGPS 1.0 mg · In–Li 박 (O-링) → 위 나사로 누름 · 아래 하중 센서로 압력 확인 → **각 압력 (0 · 6 · 12 · 50 · 100 MPa) 에서 누른 채** ① 싱크로트론 CT (20 keV · 0.5 µm · 1800 장) ② EIS (Nyquist → R_SE · R_CT 맞춤) → CT 재구성 → Dragonfly 세 상 분할 → 512 × 512 × 50 µm³ 에서 기공 · 부피 · 접촉 분율 · 36 × 36 × 50 µm³ 에서 SE 경로 tortuosity (N = 100) → 단면 · 3D 를 보고 방향 판단.  따로: 셀마다 첫 충방전 (6 · 50 · 100 MPa) · 6 MPa 10 사이클 · 한 셀 단계 상승 (6 → 100 MPa · 10 사이클) · 50 → 0 MPa 탈압 단면 (S14) · LFP 전극 50 MPa CT (S12).
- 안 한 것: 압력 유지 시간 · 가압 속도 · 반복 셀 · 진밀도 / 질량 기공 · 분할 문턱 공개 · 방향별 수치 · 옆 방향 tortuosity · 수송 tortuosity (Laplace · 확산) · 100 MPa 에서의 탈압 · 단면 SEM · 입도 분포 측정.

### 4-2. 입자 처리
- 실험 — 실제 가루.  NCM = 구형 2 차 입자 (≈10 µm) · LGPS = 불규칙 입자 (≈1–10 µm) · AB = 따로 분할하지 않음 (세 상 = NCM · LGPS · 공극).  저자는 NCM 을 *"hard"* (거의 변형하지 않음) · LGPS 를 *"soft"* (작은 입자 · 작은 영률 → 틈을 메움) 로 다룬다 — **영률로 설명**하고 항복 · 소성 유동의 값은 쓰지 않는다.
- 우리 대응 (CLAUDE.md): DEM = 단단한 구 · hooke/hysteresis 접촉 · SE 영률 18 배 연화 (1.35 GPa) — 입자 모양은 안 변함 · MPM = AM 얼린 장애물 + SE J2 소성 (E 1.53 · σ_y 0.30 · ν 0.49).  이 논문의 "NCM 이 하중을 먼저 받아 틈이 저압 자리" 는 **AM 이 하중을 나눠 지는 경우 (R1)** 의 실험 쪽 정성 진술이다 — 우리 MPM 의 얼린 AM 은 하중 0 이라 이 기전이 없다 (CLAUDE.md DO-NOT 블록).

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **말 없음** (본문 · ESI 에 DEM · discrete element · particle simulation 낱말 0 회 · 계산 없음).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — 계산이 없어 말도 없다.  재료 쪽 진술만: *"During electrode fabrication, high pressure is applied to improve solid-to-solid contact between powders, which involves plastic deformation within composite electrodes."* (p.1) · *"Hard NCM particles are slightly deformed by applied pressure"* (p.4) · *"LGPS with a smaller grain size and Young's modulus can fill the voids located around the NCMs"* (p.4) · *"Since no force is applied from the horizontal direction, the gap cannot be fully filled"* (p.6).  ⇒ 일축 가압 + 단단한 AM = 옆 방향 응력 부족 → 소성 SE 가 AM 옆 틈에 못 들어간다는 **정성 기전** (맞춘 값 · 계산 비용 0).
3. **2D / 3D** — CT 는 3D · 방향 판단은 2D 단면 (그림 4a · S13) 과 3D 렌더 (그림 4c) 를 눈으로 · tortuosity 는 3D 영역 (모식 2D) · 2D → 3D 전이 말 없음.
4. **압력을 뺄 때의 거동** — 50 → 0 MPa 한 번 · *"No clear changes were detected with respect to the void in the pressure-released condition"* (p.4 · S14) — 정성 · 숫자 없음 · 100 MPa 탈압 없음.

### 4-4. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| operando CT 셀 | 같은 셀에서 압력을 바꾸며 충방전 · EIS 와 X 선 CT 를 할 수 있는 지름 1 mm 셀 (그림 1) |
| 적층압 (stack pressure) ↔ 제조압 (fabrication pressure) | 저자는 둘을 나누지만 이 실험은 따로 제조압 없이 적층압 하나 → 그 값이 제조압에 해당 (p.3) |
| 세 상 분할 | 투과 세기로 NCM (밝음) · LGPS · 공극 (어두움) 을 나눔 (Dragonfly) |
| 접촉 면적 분율 | NCM 표면 중 LGPS 와 닿은 몫 (나머지는 공극과 닿음) |
| tortuosity (*"flexural index"*) | SE 로 이어진 3D 경로 길이 ÷ 관측 두께 — 기하 τ |
| low-pressure spot | 단단한 AM 사이 틈 — 판 압력이 AM 에 걸려 틈에는 압력이 덜 감 (그림 7) |
| 겉보기 전도도 (apparent conductivity) | EIS 에서 낸 셀 전도도 (환산 [미확인]) |
| R_ct | 양극 쪽 전하 이동 저항 (S16 회로의 R_CT) |

---

## 5. Figure set ★
| 그림 (크롭 파일) | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| Fig. 1 (`fig_1.png`) | 셀 층 구조 (스테인리스 / NCM / LGPS / In–Li / 스테인리스 · ⌀1 mm) + 전기화학 · 압력 모니터 · 20 keV X 선 카메라 | ★ 누른 채 측정 꼴 (단계 6 실험 대조 설계) |
| Fig. 2 (`fig_2.png` · `fig_2a` · `fig_2b`) | (a) 6 MPa 10 사이클 (b) 6 · 50 · 100 MPa 첫 사이클 | 전기화학 (흐름 밖) [판독] |
| Fig. 3 (`fig_3.png` · `fig_3a` · `fig_3b` · `fig_3c`) | (a) 복합 · SE 층 기공 vs 압력 (b) NCM · LGPS · 공극 부피 (인쇄 %) (c) 접촉 면적 분율 | ★★ 압력별 기공 · 부피 · 접촉 — 결과 전 대조의 방향 |
| Fig. 4 (`fig_4.png` · `fig_4a` · `fig_4b` · `fig_4c`) | (a) XY · YZ · XZ 단면의 NCM 경계색 (b) 축 · 가압 방향 (c) 6 · 100 MPa 3D (옆으로 긴 공극) | ★ 이방 접촉의 근거 그림 (정성) |
| Fig. 5 (`fig_5.png` · `fig_5a` · `fig_5b` · `fig_5c`) | (a) 36 × 36 × 50 µm³ 영역 (b) 경로 모식 (c) tortuosity 히스토그램 N = 100 × 5 | ★ 과압 τ↑ 의 근거 · 판독 통계 (§3-6) |
| Fig. 6 (`fig_6.png` · `fig_6a` · `fig_6b`) | (a) 겉보기 전도도 (b) R_ct vs 압력 | 접촉 ↔ R_ct |
| Fig. 7 (`fig_7.png`) | 가압 전 · 가압 중 (Force line · Low pressure spot) · 가압 뒤 ((a) 가압 방향 공극 (b) AM 이 만든 공극) | ★ AM 하중 차폐 · 옆 틈 기전의 모식 (R1) |
| SI S1 · S2 (`fig_S1.png` · `fig_S2.png`) | NCM SEM (SU6600 · 15 kV) · LGPS SEM (S-4800 · 1.5 kV · 대기 노출 없음) | 입경 판독 (복셀 대비) |
| SI S3 (`fig_S3.png` · `fig_S3a` · `fig_S3b`) | 한 셀 단계 상승 10 사이클 · 용량 향상 % | 전기화학 (계산 규칙 미확인) |
| SI S4 · S5 (`fig_S4.png` · `fig_S5.png`) | 양극 · 전해질 층 XY 단면 0–100 MPa (500 µm 막대) | 같은 셀 표지 (S5 의 LGPS 덩어리) |
| SI S6 (`fig_S6.png`) | 세로 단면 0–100 MPa (양극 · SE · 음극) | ★ 그릇 모양 경계 · 두께 판독 (§3-3) |
| SI S7–S11 (`fig_S7.png`–`fig_S11.png`) | 압력마다 회색조 + 세 상 분할 (x-y · y-z · z-x) | 분할 결과의 모양 (문턱은 미기재) |
| SI S12 (`fig_S12.png`) | LFP SEM · LFP 전극 50 MPa CT | 작은 AM 대조 |
| SI S13 (`fig_S13.png`) | XZ 단면 NCM 경계색 0–100 MPa (512 × 50 µm) | ★ 방향별 판독의 원자료 (§3-5) |
| SI S14 (`fig_S14.png`) | 50 MPa ↔ 뺀 뒤 0 MPa XY 단면 | 탈압 (정성) |
| SI S15 · S16 (`fig_S15.png` · `fig_S15a` · `fig_S15b` · `fig_S16.png`) | Nyquist (벡터) · 맞춤 회로 | R_ct 근거 · 반원 폭 대조 |
| 근거 문단 18 장 (`txt_p1_abstract` · `txt_p1_p2_fabrication_vs_stack_pressure` · `txt_p2_ct_anisotropy_gap` · `txt_p2_materials_cell` · `txt_p2_ct_conditions` · `txt_p2_cell_6mpa_loading` · `txt_p3_initial_capacity_step_cell` · `txt_p3_no_fabrication_pressure` · `txt_p3_ct_region_segmentation` · `txt_p4_porosity_two_stage` · `txt_p4_lfp_nanovoids` · `txt_p4_contact_fraction_release` · `txt_p4_p5_anisotropy` · `txt_p5_tortuosity` · `txt_p5_impedance` · `txt_p6_low_pressure_spots` · `txt_p6_tortuosity_tradeoff` · `txt_p6_conclusions`) | 인용 문장 전부 (식이 없어 정의가 다 문장에 있다) | 보고서 붙임 |

## 6. Post-processing ★
- **원문**: Dragonfly 4.1 세 상 분할 → 부피 분율 · 기공 · 접촉 분율 · 경로 tortuosity (방법 세부 미기재) · EIS 등가회로 맞춤 (S16 · 소프트웨어 미기재).
- **이 카드**: 본문 그림 = 300 dpi 래스터 원본 화소에서 눈금 · 표지 무게중심 (그림 3a · 3c · 6) · 곡선 끝 (그림 2) · 막대 높이 (그림 5c — 0.1 칸 · 1 개 = 9.6 화소 격자를 그려 눈으로 셈 · 겹친 원 · 선이 막대 꼭대기를 가리는 칸이 있어 합이 98–101) · SI S3b 표지 · SI S15 = 벡터 표지 좌표 · **카드 판독 둘** (SI S13 경계색 × 법선 방향 · SI S6 층 두께) — 전부 `digitized.csv` note 열에 방법.  카드 산술 = vol% (가정 밀도) · LGPS/NCM 부피비 · Heckel 꼴 · 두께 비 · 질량 대조 · R_ct 면적값 · 용량 비 · 첫 효율.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (우리 수치는 CLAUDE.md 출처를 그 자리에 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 압력 · 측정 연산자가 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| 재료 | NCM111 (LiNbO₃) + **LGPS** + AB 4.8 wt% | NCM811 + **Li₆PS₅Cl** (탄소는 일부 계열만) | 다른 SE · 다른 AM · 탄소 있음 |
| 압력 · 상태 | 0–100 MPa · **누른 채** (적층압 = 제조압) | DEM 300 MPa · 판 정지 + 판 고정 이완 (하중 아래) [우리] | 상태 같음 (누른 채) · 압력 3 배 다름 |
| 순수 SE 기공 | LGPS 층 **15 % (50) · 4.3 % (101 MPa)** [판독 · CT 분할] · Heckel P_y ≈ 40 MPa [카드 산술] | 랩 표준 **10–13 % @300 MPa · 진밀도 1.64** [우리 · 고정] · DEM 순수 SE Heckel **P_y 138 MPa** [우리] | **랩 표준과 다른 문헌 값 (다른 재료 · CT 분할 · 분모 없음)** — 판정 아님 |
| 복합 기공 | **44 → 23 %** (0 → 100 MPa) · P_y ≈ 168 MPa [카드 산술] | real_14 DEM ε_sphere **15.6 %** (300 MPa) [우리 CLAUDE.md SE-DUMP 절] · [DEM 우선 (수영)] 단계 5 = 예측값 | 조성 (LGPS 65 vol% [카드 산술] ↔ SE ≈ 26 vol%) · 압력 · 연산자 다름 |
| AM 의 효과 | 같은 압력에서 SE 층 5 % ↔ 복합 23 % · 12 MPa 위에서 복합만 둔화 · 저자 = NCM 이 하중을 먼저 받음 | DEM 은 AM 이 하중을 나눠 진다 (접촉망) · MPM 은 AM 얼림 = 하중 0 → SE 가 100 % 를 져 과압축 (R1 · CLAUDE.md DO-NOT) | **R1 의 실험 쪽 방향 증거** (값 전이 아님) |
| AM–SE 접촉 | 접촉 분율 (NCM 경계 중 LGPS 몫) **75–84 %** (CT 화소 이웃) | DEM 피복 Hertz ≈18 % · Tabor ≈48–52 % · MPM 기하 피복 46/70 → 소성 52/74 (밴드 0.13 / 0.26 µm) [우리 CLAUDE.md] | **연산자 다름** — 그들은 '공극이 아닌 쪽' 을 다 접촉으로 센다 (틈 허용폭 = 화소) · CLAUDE.md 는 화소 이웃 피복을 쓰지 말라고 적는다 (MPM 미리보기 26 %) |
| 접촉 방향 | Z 면 ↔ 옆면 비대칭 (정성) · 카드 판독 0.89–0.96 ↔ 0.65–0.85 | **지표 없음** (CLAUDE.md 에 방향별 피복 · 접촉 법선 통계 없음) | 새 관측량 후보 (§8) |
| tortuosity | 기하 경로 ÷ 두께 · 평균 6.5 → 3.8 → 5.4 (0 · 50 · 100 MPa) | τ_geo (벽 기준 Dijkstra · `tortuosity_SE_wall` = `tau_geo_SE_dij`) LHS-130 1.29–4.15 · 64 행 1.26–1.60 [우리 CLAUDE.md J20-n] · 수송 tortuosity (tau2) 는 다른 양 [우리 τ 규약] | **같은 이름 (기하) · 다른 연산자** — 경로 추출 규칙 미기재 · 우리보다 크다 |
| 탈압 | 50 → 0 MPa: 공극 변화 *"no clear changes"* (정성) | 언로딩 시험 (등록 단계) [우리] | 값 대조점 없음 · 방향만 (작은 되돌아옴?) |
| 수송 | R_ct · 겉보기 σ (환산 미기재) | 접촉망 σ · 복셀 σ | 대조점 아님 |

### 7-2. ★ 정의 대조 — "같은 이름 · 다른 연산자"
| 항목 | Sakka 2022 | 우리 |
|---|---|---|
| 기공 | CT 세 상 분할의 공극 복셀 몫 (512 × 512 × 50 µm³ 영역 · 화소 0.5 µm · 문턱 미기재 · AB 분류 미기재) | DEM ε_sphere (구 부피 합 · 질량 보존) / ε_union · 순수 SE 랩 표준은 진밀도 1.64 기준 [우리] |
| 접촉 | NCM 경계 화소 중 LGPS 와 이웃한 몫 (공극과의 이웃 = 나머지) | DEM 접촉 = 겹침 δ > 0 · 피복 = AM 표면 중 SE 가 밴드 안 (Hertz / Tabor) [우리] |
| tortuosity | SE 로 이어진 경로 길이 ÷ 두께 (N = 100 경로 · 분포) | τ_geo = 최단 경로 ÷ 두께 (Dijkstra · 벽 기준) · tau2 = φ σ₀ / σ_eff (수송) [우리 τ 규약] |
| 상태 | 누른 채 · 각 압력 · 같은 셀 (읽힘) | 300 MPa 압축 끝 덤프 · 하중 아래 |

⇒ **맞대기 규칙 (결과 전에 적어 둠)**: ① 기공 · 접촉 · τ 는 **방향과 모양만** 견준다 (재료 · 압력 · 연산자가 다르다) ② 우리 쪽 접촉 방향 통계를 낼 때 **AM 표면의 법선 방향별 (|n_z| 칸) SE 피복** 을 따로 센다 — 이 논문 (카드 판독) 의 "Z 면 > 옆면" 이 우리 DEM · MPM 에서도 나오는지 ③ τ 는 우리 τ_geo 의 압력 의존 (같은 침대를 여러 압력에서) 로만 견준다 — τ_Laplace · tau2 와 섞지 않는다 ④ 값 차이를 모델 오차로 읽지 않는다 (frame[4]).

### 7-3. 나란히 놓을 정본 카드 (값 · 조건 그대로 · 기존 카드는 고치지 않는다)
| 카드 | 계 | 압력 · 상태 | 측정 | 그 카드의 값 |
|---|---|---|---|---|
| **이 논문** | NCM111 + LGPS + AB (1 : 1 : 0.1 wt) | 0–100 MPa · 누른 채 | CT 분할 (0.5 µm) | 복합 44 → 23 % · LGPS 층 53 → 4.3 % · 접촉 분율 75–84 % |
| `jeong2024_operando_densification_chemomechanics_se_size_composite_cathode` | NCM811 + LPSCl 70 : 27.5 : 2.5 wt% (SE ≈1 vs 3–5 µm) | 무하중 (그 카드) | XCT 분할 (복셀 0.92 µm) | 11 vs 16 % [다른 카드] |
| `park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics` | NCM811 + LPSCl 70 : 30 · 80 : 20 · 85 : 15 wt + C65 | 셀 300 MPa 2 분 조립 · 촬영 압력 미인쇄 | XCT (0.65 µm) | '공극 + 탄소' 14.7 · 18.1 · 23.3 % [다른 카드] |
| `doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density` | SC-NMC83 + LPSCl + C65 70 : 27.5 : 2.5 | 500 MPa · 뺀 뒤 단면 | 단면 SEM 문장 안 (방법 · 분모 미기재) | 상대밀도 ≈ 0.90 · PC 50 / 250 / 500 MPa = 0.78 / 0.82 / 0.86 [다른 카드] |
| `miss2026_pressure_tortuosity_composite_cathode_coating` | NMC622 + Li₃PS₄–LiI 유리 | 8.8 → 663 MPa · 누른 채 | EIS tortuosity factor (수송) | τ_ion 압력 의존 *"weak"* (예: pc 무코팅 ≈3.4 → 2.6) [다른 카드] |
| `kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation` | 순수 황화물 (Li₆PS₅Br 주) | ≤ 103 MPa · 누른 채 | XCT (1.62 µm) + 복셀 FV | 기공률 · 진밀도 숫자 없음 [다른 카드] |
| `korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens` | 순수 LPSCl | 76.2 → 510 MPa · 누른 채 | μ-CT + 두께 환산 | S11 12.1 → 8.6 % (자기 두께와 모순) [다른 카드] |

- 읽는 법: **누른 채 CT 로 복합 양극의 압력별 기공 곡선을 준 카드는 정본에서 이것이 처음**이다 (다른 카드들은 한 압력 · 뺀 뒤 · 무하중 · 순수 SE).  단 SE 가 LGPS 라 우리 LPSCl 침대의 값 대조가 아니라 **방향 · 모양 대조** 다.  압밀 중 tortuosity 의 압력 의존은 이 논문 (기하 · 100 MPa 에서 상승) 과 Miß 2026 (수송 · 663 MPa 까지 약하게 감소) 이 정의 · 재료 · 압력 범위가 달라 서로 반대처럼 보인다 — 맞대지 않는다.

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **실험 (누른 채 구조 + 같은 셀 EIS)** — 우리 분업으로는 DEM 쪽 (접촉 · 경로 · 기공) 의 **측정 쪽 짝** 이고 MPM 쪽 (형상 · 소성 유동) 은 그림 (SE 가 AM 틈을 못 메움) 으로만.
- 없는 반쪽: 모델 · 하중 분담 값 · 응력 · 소성 · 수송 tortuosity · 옆 방향 경로 · 300 MPa 영역.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = LiNbO₃ 코팅 NCM111 + **LGPS** + AB — 우리 계 (NCM811 + LPSCl) 와 **SE 부터 다르다** · ≤ 100 MPa · CT 분할 · 누른 채.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ **문헌 기공 칸 넷**을 결과 전에 둘 근거: ⓐ 상태 (누른 채 ↔ 뺀 뒤) ⓑ 연산자 (CT 분할 ↔ 질량 · 두께) ⓒ 분모 (영상 부피 ↔ 진밀도) ⓓ 탄소 분류 (AB 가 공극에 들어갔나) · ★ **질량 · 두께 · CT 기공 삼각 대조**: 이 논문은 두께 비가 CT 기공과 2 % 안에서 맞지만 절대 질량은 ≈1/2–1/3 (§3-3) → 문헌 CT 기공을 받을 때 "두께로 자기 일관을 확인했나" 칸 · ★ 접촉 분율의 분모 (AM 표면) · 틈 허용폭 (화소) 칸 | 진밀도 기공 · 분할 문턱 없음 |
| **단계 1** (3D 메모리 · 장 수) | 크기 감각: 1 mm 시야 @0.5 µm ≈ 2000 × 2000 화소/단면 [카드 산술] · 분석 영역 512 × 512 × 50 µm³ ≈ 1024 × 1024 × 100 복셀 · τ 영역 36 × 36 × 50 µm³ — NCM (10 µm) 3–4 개 폭 (표본 작음) | 입자별 장 · 메모리 숫자 없음 |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | ★ **관측량**: AM 경계를 법선 방향 (|n_z|) 칸으로 나눈 SE 접촉 몫 — 이 논문 (카드 판독) 은 Z 면 0.89–0.96 ↔ 옆면 0.65–0.85 · 한 속도장 ↔ 입자별 속도장이 **옆면 공극** 을 다르게 남기는지가 판별 거리 (일축 가압에서 옆 방향 응력이 AM 틈으로 전달되느냐) | 2D 계산 · 값 없음 (방향만) |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | **랩 표준과 다른 문헌 값 (다른 재료)**: LGPS 층 누른 채 CT 기공 53 → 41 → 39 → 15 → 4.3 % (0 → 101 MPa) · Heckel P_y ≈ 40 MPa [카드 산술] — LPSCl 이 아니므로 맞춤 표적이 아니다 · 같은 꼴의 LPSCl 곡선 (누른 채 · 두께로 자기 일관 확인) 을 찾을 때의 본보기 | 진밀도 분모 없음 · 화소 아래 기공 미검출 (하한일 수 있음) · 다른 재료 |
| **단계 5** (3D 복합 압밀) | ★ **결과 전 대조 항목 (방향 · 모양)**: ① 같은 압력에서 SE 단독층보다 복합 양극의 기공이 덜 준다 (100 MPa 4.3 ↔ 22.9 %) · 겉보기 P_y 40 ↔ 168 MPa (×4) [카드 산술] ② 저압에서는 AM 몫이 먼저 늘고 (재배열) 고압에서 SE 몫이 는다 (두 단계) ③ 접촉 분율은 어느 압력 위에서 평탄 ④ AM 틈 · 옆면 공극이 남는다 (방향 비대칭) — 우리 3D 복합 압밀 (DEM · 앞으로 MPM A′) 이 같은 **방향** 을 내는지 | LGPS · NCM111 · ≤ 100 MPa · 조성 (SE 65 vol%) 이 우리와 다름 · 하중 몫 값 없음 |
| **단계 6** (탈압 · 되돌아옴) | 50 → 0 MPa 에서 공극 *"no clear changes"* (정성) — 큰 되돌아옴이 없다는 약한 방향 · ★ 실험 꼴: **같은 셀을 누른 채 → 뺀 뒤 CT** 로 같은 자리를 비교 (S14) | 숫자 · 100 MPa 탈압 · 두께 없음 |
| **단계 7** (형상 · 피복 · 수송) | ★ 접촉 분율 ↔ R_ct (865 → 58 kΩ) · 기하 τ 분포 (평균 · 퍼짐 · 최소) 를 함께 보고하는 꼴 · τ 를 **분포** (N = 100 경로) 로 내고 최소 · 최빈 · 평균을 따로 보는 법 (100 MPa 에서 최소는 그대로 · 평균 · 퍼짐 상승) | 수송 τ · 우리 τ_geo 와 연산자 다름 · 영역 하나 |
| **후보 D0** (지금 DEM) | DEM 에서 바로 셀 수 있는 것: AM–SE 접촉의 **법선 방향 분포** (접촉점 벡터의 z 성분) · AM 표면 방향별 피복 · SE 경로 τ_geo 의 압력 의존 — 결과 전에 "Z 면 피복 > 옆면 피복" 을 적어 두고 본다 | DEM 의 구 · 점접촉으로 옆 틈 메움 (소성 유동) 은 원리상 안 나온다 (frame[1]/[2]) — 방향 비대칭이 나와도 기전이 다를 수 있다 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 셀 벽: 지름 1 mm 셀에서 양극/SE 경계가 그릇 모양 (가운데 ≈1.4–1.5 × 가장자리 [카드 판독]) → 작은 지름 실험은 벽 마찰로 층 두께 · 압력이 가운데와 가장자리에서 다르다는 한정어 (우리 침대는 주기 경계) | 벽 마찰 값 없음 |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | ★ **R1 의 실험 쪽 진술**: *"uniaxial pressing preferentially pushes the NCM particles … the pressure of the flat current collector is not sufficiently applied to the space between the AM particles"* (p.6 · 그림 7) — AM 이 하중을 지는 모델 (A · A′) 에서만 생기는 "저압 자리" · 결과 전 대조 = 단계 5 의 ①–④ | 맞춤 표적 아님 · 하중 몫 숫자 없음 |
| **후보 B** (입자별 FE + 접촉) | 없음 | — |
| **후보 C** (큰 변형 접촉 DEM · MDR 류) | 없음 | — |
| **후보 C′** (항복 캡 탄소성 접촉 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀 · 캡 소성 · Heckel) | [카드 산술] 누른 채 CT 기공의 Heckel 꼴이 SE 층 (R² 1.00 · P_y ≈ 40 MPa) · 복합 (R² 1.00 · P_y ≈ 168 MPa) 모두 12–101 MPa 에서 직선 — 복합 양극 균질화 모델이 AM 분율에 따라 P_y 를 키우는 꼴의 **방향** 대조 (LGPS) | 다른 재료 · 세 점 · ≤ 100 MPa |
| **U0–U6** | **U1 · U6** (해상도) 쪽 경고: 0.5 µm 화소에서 LGPS 2–20 화소/지름 · 입자 사이 ≲ 1 µm 기공 미검출 — 실험 기공과 계산 기공을 견줄 때 **같은 해상도로 거른** 계산 기공을 함께 낸다 (계산 침대를 0.5 µm 로 복셀화해 같은 세 상 분할) | U0 · U2–U5 없음 |
| **R1–R7** | **R1** (AM 하중 분담): 저자 기전 = NCM 이 먼저 눌림 → 틈 저압 (정성 · 그림 7) · **R2** (미끄럼 · 분리): 옆면 공극 · 탈압 뒤 공극 변화 없음 (정성) · **R6** (SE 형상 변형): LGPS 가 NCM 둘레를 메움 · 공극이 가압 방향을 따라 납작해짐 (그림 4c) | R3 · R4 (값) · R5 (맞춘 값 0 개) · R7 (AM 파괴 관찰 없음) |
| **결과 전 대조 항목** | ① 복합 ↔ SE 단독 기공 차이 (같은 압력 · 누른 채) — LGPS 계 100 MPa 22.9 ↔ 4.3 % ② 접촉 분율 평탄 압력 (≈50 MPa · LGPS 계) ③ 방향별 접촉 (Z 면 > 옆면 · 카드 판독) ④ 기하 τ 분포의 평균 · 퍼짐이 어느 압력 위에서 다시 커지는지 — **전부 방향 항목 · 맞추지 않음** | LPSCl 값 아님 · 우리 랩 표준 (10–13 % · 1.64) 과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: SE (LGPS ↔ LPSCl) · AM (NCM111-LiNbO₃ ↔ NCM811) · 탄소 AB 4.8 wt% · 조성 (SE ≈65 vol% [카드 산술] ↔ 우리 생산 SE ≈26 vol%) · 압력 (≤ 100 ↔ 300 MPa) · 셀 지름 1 mm (벽 효과) ↔ 주기 RVE · 연산자 (CT 분할 ↔ 구 부피 / 질량 보존).

## 9. 적용 인사이트 (행동)
1. **결과 전 대조 항목 등록 (단계 5 · 방향)**: "같은 압력에서 복합 양극 기공 > SE 단독층 기공 · 차이가 압력과 함께 커진다 (LGPS 계: 12 MPa 0 %p → 100 MPa 19 %p · Sakka 2022 · 누른 채 CT)" — 꼬리표 "LGPS · NCM111 · AB · CT 분할 0.5 µm · 분모 없음".
2. **새 관측량 (D0 · 단계 3 · 단계 5)**: AM 표면 법선의 |n_z| 칸별 SE 피복 몫 (+ 접촉 법선 분포) 을 DEM · MPM 공통으로 정의해 둔다 — 이 논문의 정성 결론 (Z 면 > 옆면) 을 우리 계산이 내는지 결과 전에 적고 본다.  같은 침대를 여러 압력에서 덤프해 τ_geo 분포 (평균 · 퍼짐 · 최소) 를 함께 낸다.
3. **문헌 기공 인용 꼬리표 (단계 0)**: 상태 · 연산자 · 분모 · 탄소 분류 + **두께로 자기 일관을 확인했는지** — 이 논문은 두께 비 ✓ · 절대 질량 ✗ (§3-3).
4. **해상도 맞춤 (U1 · U6)**: 실험 CT 기공과 견줄 때는 계산 침대를 같은 화소 (0.5 µm) 로 복셀화 · 분할한 값을 같이 낸다 (화소 아래 기공이 빠지는 효과를 양쪽에 같이).
5. **인용 한정 (비교 문서 [151])**: "과압 → tortuosity↑" 를 쓸 때 "100 MPa · 기하 경로 τ · 영역 하나 · 저자도 영향 작다고 봄" 을, "이방 접촉" 을 쓸 때 "정성 (방향별 수치는 원문에 없음)" 을 붙인다 · τ_Laplace 와 잇지 않는다.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Operando synchrotron X-ray CT of a LiNbO₃-coated NCM111/Li₁₀GeP₂S₁₂/acetylene black (1:1:0.1 wt) composite cathode held at 0–100 MPa showed the porosity falling from 44 to 23 %, while the LGPS separator layer in the same cell fell to about 5 % (Sakka et al., *J. Mater. Chem. A* 10 (2022) 16602)."
- "The fraction of the NCM surface in contact with LGPS rose by roughly 10 % above 50 MPa compared with ≤ 12 MPa and then levelled off, and the charge-transfer resistance fell by about an order of magnitude."
- "The authors observed (qualitatively, from CT slices) that NCM/LGPS contact is good along the pressing direction but voids dominate laterally, which they attribute to low-pressure spots between stiff active-material particles under uniaxial pressing."
- 국문 (한정어와 함께): *"LGPS · NCM111 복합 양극을 누른 채 0–100 MPa 에서 찍은 CT 에서 기공은 44 → 23 % (같은 셀 LGPS 층은 ≈5 %) 로 줄고 NCM–LGPS 접촉 분율은 50 MPa 에서 멈췄다 (Sakka 2022) — 0.5 µm 화소 분할 값 · 진밀도 분모 없음 · 이방 접촉은 정성 관찰이다."*

## 11. 주의/한계 (over-claim 방지)
1. **우리 계가 아니다** — LGPS · NCM111 · AB.  LPSCl · NCM811 값처럼 쓰지 않는다.
2. **≤ 100 MPa** · 따로 제조압 없음 — "과압" 은 100 MPa 를 뜻한다.
3. **CT 분할 기공** — 진밀도 분모 없음 · 문턱 · 필터 미기재 · AB 분류 미기재 · 0.5 µm 아래 기공 못 봄 (하한일 수 있음).
4. 분석 영역 **하나씩 · 반복 없음** · τ 영역은 NCM 3–4 개 폭 — 100 MPa 의 τ 증가는 표본 차이를 배제하지 못한다 [카드 해석].
5. 이방성 = **정성** · 방향별 수치는 이 카드의 그림 판독뿐.
6. 접촉 = **분율** (면적 아님) · 공극이 아닌 쪽을 다 접촉으로 셈 (틈 허용폭 = 화소).
7. **원문 안 어긋남** — 분할 조성비 흔들림 · 질량 ↔ 두께 · R_ct ↔ 반원 폭 · S3b 계산 규칙 · 그림 번호 둘 (§3-9).
8. 지름 1 mm 셀 · 그릇 모양 층 경계 (벽 효과) — 분석 영역 깊이에 따라 값이 달라질 수 있다 [카드 해석].

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 25 | A. Ohashi, M. Kodama, N. Horikawa and S. Hirai, J. Power Sources, 2021, 483, 229212. | *"In composites with different Young's moduli, large pressures can be applied to materials that have larger Young's moduli"* 의 근거 — 단단한 AM 의 하중 몫 (질문 d · R1) · 카드 없음 |
| 24 | A. Ohashi, M. Kodama, X. Y. Sun, S. Hori, K. Suzuki, R. Kanno and S. Hirai, J. Power Sources, 2020, 470, 228437. | *"the NCM particles are pressurised preferentially"* · *"strain caused by the pressure reduces the contact between the AM and SE"* 의 근거 (질문 d · i) · 카드 없음 (heck2026 카드가 서지만: "Stress distribution in the composite electrodes of sulfide all-solid-state lithium-ion batteries") |
| 37 | E. J. Cheng, K. Hong, N. J. Taylor, H. Choe, J. Wolfenstine and J. Sakamoto, J. Eur. Ceram. Soc., 2017, 37, 3213–3217. | NCM 의 *"high Young's modulus"* 근거 — NCM111 기계 물성 (질문 c) · 카드 없음 |
| 18 | H. Fathiannasab, L. K. Zhu and Z. W. Chen, J. Power Sources, 2021, 483, 229028. | 가압 변형이 AM–SE 접촉을 줄인다 · AM/SE CT 구조 분석 (질문 i) · 카드 없음 |
| 34 | A. Neumann, S. Randau, K. Becker-Steinberger, T. Danner, S. Hein, Z. Y. Ning, J. Marrow, F. H. Richter, J. Janek and A. Latz, ACS Appl. Mater. Interfaces, 2020, 12, 9277–9291. | CT 구조 + 시뮬레이션 (불균일 충방전) · tortuosity 1–10 문헌 (질문 h · m) · 카드 없음 |
| 15 | J. M. Doux, Y. Y. C. Yang, D. H. S. Tan, H. Nguyen, E. A. Wu, X. F. Wang, A. Banerjee and Y. S. Meng, J. Mater. Chem. A, 2020, 8, 5049–5055. | 제조압 50 ↔ 150 MPa 용량 — 카드 = `doux2020_pressure_effects_sulfide_se_jmca` |
| 26 | J. M. Doux, H. Nguyen, D. H. S. Tan, A. Banerjee, X. F. Wang, E. A. Wu, C. Jo, H. D. Yang and Y. S. Meng, Adv. Energy Mater., 2020, 10, 1903253. | 적층압 · 덴드라이트 — 카드 = `doux2020_stack_pressure_assb` |
| 43 | A. Sakuda, A. Hayashi and M. Tatsumisago, Sci. Rep., 2013, 3, 2261. | SE 기공 ↔ 겉보기 전도도 — 카드 = `sakuda2013_sulfide_mechanical_property` |
| 40 | P. Minnmann, L. Quillman, S. Burkhardt, F. H. Richter and J. Janek, J. Electrochem. Soc., 2021, 168, 040537. | tortuosity 문헌 범위 — 카드 = `minnmann2021_jes_charge_transport_bottlenecks` |
| 39 | L. Froboese, J. F. v. d. Sichel, T. Loellhoeffel, L. Helmers and A. Kwade, J. Electrochem. Soc., 2019, 166, A318–A328. | tortuosity 문헌 범위 — 카드 = `froboese2019_microstructure_ionic_conductivity_assb_electrode` |
| 19 | G. Bucci, B. Talamini, A. Renuka Balakrishna, Y.-M. Chiang and W. C. Carter, Phys. Rev. Mater., 2018, 2, 105407. | AM–SE 접촉 손실 — 카드 = `bucci2018_mechanical_instability_interface_delamination` |
| 9 | N. Kamaya, K. Homma, Y. Yamakawa, M. Hirayama, R. Kanno, M. Yonemura, T. Kamiyama, Y. Kato, S. Hama, K. Kawamoto and A. Mitsui, Nat. Mater., 2011, 10, 682–686. | LGPS 원전 — 카드 = `kamaya2011_lgps_lithium_superionic_conductor` |
| 22 | M. J. Wang, E. Kazyak, N. P. Dasgupta and J. Sakamoto, Joule, 2021, 5, 1371–1390. | 적층압 실용 상한 1 MPa (p.2) — 카드 없음 (정본 papers/ 에 'Kazyak' · 'Joule … 1371' 없음) |

## 13. [미확인] 목록 (본문 8 쪽 + ESI 16 쪽 전수에 없음)
1. **세 상 분할 문턱 · 필터 · 부분 부피 처리 · AB 의 분류** · 분석 영역 (512 × 512 × 50 · 36 × 36 × 50 µm³) 의 깊이 위치 · 압력마다 같은 자리인지.
2. **압력 유지 시간 · 가압 속도 · CT 전 대기 시간** · 압력 단계를 한 셀로 차례로 했는지 (그림으로는 같은 셀로 읽힘).
3. 접촉 분율의 표면적 계산법 · NCM–NCM 면 처리 · *"approximately 10%"* 가 %p 인지.
4. tortuosity 경로 추출 알고리즘 · 시작점 100 개 · 연결 규칙.
5. 겉보기 전도도의 환산 (저항 · 두께 · 면적) · EIS 주파수 · 진폭 · 맞춤 값 표 · R_CT 와 낮은 주파수 꼬리의 배정.
6. vol% 조성 · 성분 밀도 · 실제로 셀에 들어간 질량 (§3-3 질량 대조) · LGPS σ · NCM 공급사 · LiNbO₃ 두께.
7. S3b 용량 향상의 계산 규칙 (재현 안 됨) · C 기준 용량.
8. 100 MPa 에서의 탈압 · 뺀 뒤 기공 숫자.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 본문 8 쪽 · ESI 16 쪽을 글자 층 추출 (pdftotext raw · layout · PyMuPDF) + 렌더로 읽음.  µ (화소 0.5 µm · 영역 µm³) · × 는 글자 층이 'mm' · 빈칸으로 깨져 렌더 조각으로 확인.  서지 = PDF 1 쪽 (제목 · 저자 · 소속 · Cite this · 접수 / 승인 · DOI · "Published on 22 July 2022 · Licensed under CC-BY 4.0") + PDF 메타데이터 (Subject 줄) + 쪽 바닥글.
- 그림 크롭 **58 장** = 도구 23 (본문 그림 1–7 · ESI 그림 S1–S16) 중 **13 장 다시 자름** (f1 · f4 회색 그림 괘선 · f7 · fS16 고르지 않은 여백 · fS1 · fS2 · fS3 · fS5 · fS7 · fS10 · fS11 · fS12 그림 아래가 잘림 — ESI 래스터의 소프트 마스크가 캡션 첫 줄 가까이까지 뻗음 · fS1 · fS15 절 머리 줄 섞임) · 캡션 정리 3 (f2 '|' 가 'j' 로 · f4 · f5 줄바꿈 하이픈) + **손 크롭 35** (패널 17 · 근거 문단 18) — 본 뒤 다시 렌더 7 (f2a · f2b · f6a · f6b 마스크가 그림 끝까지 안 닿음 · f3b 위 여백 · f4b · f4c 'Z = press direction' 을 b 로).  58 장 전부 열어 확인.  번호 식 · 인라인 식 없음 (식 크롭 0).
- 판독: 본문 그림은 모두 300 dpi 래스터 한 장씩 (렌더 300 dpi = 원본) · ESI 는 111–230 dpi 래스터 + 소프트 마스크 (흰 바탕에 합성해 읽음) · ESI S15 만 벡터.  재현 값: 그림 3a 의 복합 기공 표지 44.2 · 42.3 · 30.6 · 22.9 = 그림 3b 인쇄 44 · 42 · 31 · 23 · SE 층 4.3 ↔ 본문 5 % · 그림 5c 판독 최빈 · 최소 칸 = 원문 빨간 · 파란 원 자리 · S13 판독 녹색 몫의 압력 순서 = 그림 3c 순서 · S6 두께 비 = CT 기공 비 (2 % 안).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 + DOI (D2TA02378D) · "Sakka" · 제목 낱말 grep — 이 논문 카드 없음 (jeong2024 [22] · tailored ref 12 · 비교 문서 §A [151] 에 인용만).

## 🔗 관련 카드
- 이 논문을 인용한 정본 카드 · 문서: [`jeong2024_operando_densification_chemomechanics_se_size_composite_cathode`](jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md) (참고 [22]) · [`tailored_cathode_microstructure_low_pressure_assb`](tailored_cathode_microstructure_low_pressure_assb.md) (ref 12 · "Sakka(Sakuda)") · `comparison_vs_ours_DEM.md` §A [151] (리뷰 경유) · [`fan2026_sulfide_assb_stability_review_ECERD2600097`](fan2026_sulfide_assb_stability_review_ECERD2600097.md) (리뷰 Fig 10b).
- 복합 양극 CT · 기공: `park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics` · `jeong2024_operando_densification_chemomechanics_se_size_composite_cathode` · `minnmann2024_microstructure_porosity_visualization` · `doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density`.
- 누른 채 황화물 CT: `kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation` · `korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens`.
- 압력 · tortuosity: `miss2026_pressure_tortuosity_composite_cathode_coating` · `doux2020_pressure_effects_sulfide_se_jmca` · `doux2020_stack_pressure_assb`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
