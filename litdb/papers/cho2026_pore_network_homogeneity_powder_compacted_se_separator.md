<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 1저자 11-23 '논문에이전트 부탁' (후보 표 밖 · U-1123-2 · 정독 145) 에서 꼭 뽑으라 한 항목.
     본 = mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation.md (절 번호 체계 · 머리 요약 상자 · 서지 표 · 그림 표 꼴).  두 필수 절 = §0-1 고른 의도 대조 · §8 자세한 분석.
     원문 = **ChemRxiv 원고 v2 (동료 심사 전 · 2026-10-08 게시 · CC-BY 4.0)** — 66 쪽 PDF 하나에 표지 · 본문 · 그림 · SI 가 다 있다:
       p.1 ChemRxiv 표지 (제목 · 저자 · 초록 · 게시 문구) · p.2 제목 쪽 (소속 · 교신) · p.3 초록 · p.4–20 본문 + Methods + 감사 · p.21–23 참고문헌 50 ·
       p.24–29 본문 그림 1–5 + 캡션 · p.30–50 그림 S1–S21 · p.51–63 보충 노트 1–3 · p.64–65 표 S1–S2 · p.66 SI 참고문헌 13.
     쪽 표기 = PDF 쪽 (원고에 인쇄 쪽 번호 없음).  크롭 파일 이름의 pN · figures.json 의 page 도 PDF 쪽.
     값 표지: [인쇄] = 본문 · 그림 안 글자 · 표 S1–S2 · [판독] = 그림에서 읽은 값 (원본 래스터 화소 — litdb/figures/<slug>/digitized.csv 123 행 · 축 = 눈금 화소 탐색) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [우리 산술] = 우리 쪽 값과 견주는 계산 · [미확인] = 66 쪽 전수에 없음.
     원문은 글자 층 추출 + 그림 · 표 · 식 쪽 렌더로 전부 읽었다 (식에 번호가 없고 글자 층이 깨진다 — 'β_Sn = ¿' — 식은 렌더에서 옮겼다).
     계산 = 이미지 기반 **선형 탄성 FEM** (COMSOL 6.3 · 2D 평면변형 전기화학–역학 단방향 결합 + 3D 역학) — **DEM · MPM 없음**. -->
# 분말을 눌러 만든 argyrodite 황화물 SE 분리막 — 입도 분포 (PSD) 가 넓으면 (BD) 더 치밀해도 (440 MPa 기공 1.73 % ↔ 좁은 ND 6.19 %) 공극이 뭉쳐 남고 (FIB-SEM 국소 기공 8.129 ↔ 6.752 %) 국소 탄성률 · 경도가 넓게 흩어지며 (나노압입 지도 HI_Er · 낮은 Er 몫 · Moran's I) Sn 음극 전셀에서 분리막이 깨지고 떨어진다 (100 사이클 유지율 63.1 ↔ 94.6 %) · 순수 SE 펠릿 기공 110–440 MPa × 3 분말 (표 S1 · 진밀도 1.64 g/cm³ · 다이 안 두께) · 2D 평면변형 선형 탄성 FEM 응력 집중 (파괴 · 박리 · 소성 없음) · 3D GeoDict 구조 (같은 D50 · 기공 6.752 %) — Cho · H.-J. Kim · J.-S. Kim · Park · Y. Kim · Lee · J. Kim · H. Kim · Jung (SNU · ChemRxiv 2026 v2 · 동료 심사 전)

> slug `cho2026_pore_network_homogeneity_powder_compacted_se_separator` · DOI `10.26434/chemrxiv.15009882/v2` · type `experiment + image-based linear-elastic FEM (ChemRxiv preprint v2, not peer reviewed · three commercial argyrodite SE powders with different PSD · uniaxial cold-pressed pure-SE pellets 110–440 MPa, bulk porosity from in-mold micrometer thickness and theoretical density 1.64 · FIB-SEM tomography pore maps · in-SEM Berkovich nanoindentation mapping (110 indents, HI, Moran's I) · Sn-anode / NCM622 full cells with load-cell stack pressure · post-mortem cryo cross-section SEM · 2D plane-strain electrochemical-mechanical FEM on FIB-SEM digital twins (COMSOL 6.3, one-way, bonded, no fracture) + 3D GeoDict GrainGeo microstructures under 20 MPa — no DEM, no MPM)` · PDF `dc2d13d5-41._Pore-network_homogeneity_for_mechanically_reliable_powder-compacted_solid-electrolyte_separators.pdf` · SI = 같은 PDF (p.30–66) · digested `2026-11-23` · status ✅
>
> **저자**: **Hyeok-Rae Cho** ¹ʼ⁵ · **Hyeong-Jong Kim** ¹ʼ⁴ʼ⁵ · Jae-Seung Kim ⁴ · Beom Jin Park ¹ · Youngkyung Kim ¹ · Daeyeon Lee ¹ · Jiwon Kim ¹ · Hyojun Kim ¹ · **Sung-Kyun Jung\*** ¹ʼ²ʼ³ʼ⁴ — Seoul National University: ¹ Department of Materials Science and Engineering · ² School of Transdisciplinary Innovations · ³ Research Institute of Advanced Materials (RIAM) · ⁴ Institute for Rechargeable Battery Innovations Research — ⁵ 공동 1저자 (*"These authors contributed equally"*) · \* 교신 (p.2).  ChemRxiv 표지 (p.1) 는 같은 소속을 번호만 다르게 적는다 (1 MSE · 2 IRBIR · 3 STI · 4 RIAM — H.-J. Kim 1,2 · J.-S. Kim 2 · S.-K. Jung 1,3,2,4).  *"Posted on 8 October 2026 — CC-BY 4.0 — This is a preprint and has not been peer reviewed. Data may be preliminary."* (p.1).
> 연구비 (p.20): SNU New Faculty Startup Fund · NRF (RS-2023-00261543 · RS-2025-25441254 · RS-2026-25537773) · KBSI (RS-2024-00402584) · KIMM (NK243H) · NST (GTL24012-000) · MOTIE (RS-2025-02413378 *"Development of Continuous Mass Production Processes and Quality Control Technologies for Sulfide-Based Solid Electrolytes with a Capacity of 500 kg/day for Commercialization"* · RS-2026-25539994).  저자 기여 (p.20): 개념 · 설계 H.-R.C. · H.-J.K. / 나노압입 · 전기화학 · 사후 분석 H.-R.C. / SEM J.K. · H.K. / FIB-SEM 3D 재구성 · FEM H.-J.K. / 감독 S.-K.J.  이해 충돌 없음 (p.21).
> **이웃 카드 (링크만)**: [`var2026_sulfide_se_mechanical_properties_local_indentation_pellet`](var2026_sulfide_se_mechanical_properties_local_indentation_pellet.md) (ref 19 — 200 mg · ⌀13 mm 다이 안 상대밀도 · 오일 보호 압입) · [`lee2025_heckel_argyrodite_powder_densification_nanoindentation`](lee2025_heckel_argyrodite_powder_densification_nanoindentation.md) (ref 22 — 같은 진밀도 1.64) · [`papakyriakou2021_mechanical_behavior_inorganic_li_solid_electrolytes_nanoindentation`](papakyriakou2021_mechanical_behavior_inorganic_li_solid_electrolytes_nanoindentation.md) (ref 21) · [`korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens`](korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens.md) (ref 32) · [`faka2026_particle_size_consolidation_strain_lpscl`](faka2026_particle_size_consolidation_strain_lpscl.md) (ref 34) · [`schlautmann2023_se_particle_size_composite_transport`](schlautmann2023_se_particle_size_composite_transport.md) (ref 36) · [`yano2026_se_psd_width_ionic_tortuosity_dem`](yano2026_se_psd_width_ionic_tortuosity_dem.md) (같은 축 — SE PSD 폭) · [`miss2026_insitu_conductivity_porosity_pressure_compaction`](miss2026_insitu_conductivity_porosity_pressure_compaction.md) (가압 중 ↔ 놓은 뒤) · [`doux2020_pressure_effects_sulfide_se_jmca`](doux2020_pressure_effects_sulfide_se_jmca.md) (ref 14) · [`doux2020_stack_pressure_assb`](doux2020_stack_pressure_assb.md) (ref 13) · [`kim2023_chemomech_failure_highstrain_anode`](kim2023_chemomech_failure_highstrain_anode.md) (ref 16 — Kang · Shin) · [`koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb`](koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb.md) (ref 8) · [`park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics`](park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics.md) (ref 45) · [`benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode`](benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode.md) (ref 48 · SI ref 4 — 출판본 서지) · [`torii2025_lpscl_mechanical_anisotropy_dft`](torii2025_lpscl_mechanical_anisotropy_dft.md) (SI ref 13 — SE ν 0.37) · [`minnmann2021_jes_charge_transport_bottlenecks`](minnmann2021_jes_charge_transport_bottlenecks.md) (SI ref 10 — NCM622 σ_e) · [`wang2024_hot_pressed_lpscl_pressure_invariant_conductivity`](wang2024_hot_pressed_lpscl_pressure_invariant_conductivity.md) (ref 49) · [`doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density`](doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density.md) (ref 50 — LiNbO₃ 코팅).
> **판독 원자료**: `litdb/figures/cho2026_pore_network_homogeneity_powder_compacted_se_separator/digitized.csv` (123 행 — 그림 1b D 값 · 1f 국소 기공 산포 · 1i Er/H · 2a–b 중앙값 · 바이올린 범위 · 2c HI_Er · 2h Moran's I · S8a HI_H · S8f · 4f/g/h 막대 · 5g 막대 · S9c 율속 · 그림 안 인쇄 글자 · 5a ↔ 1a · 5d ↔ S6 곡선 대조) · 그림 크롭 81 장 (도구 27 (다시 자름 5) + 손 54: 그림 S15 1 · 패널 20 · 식 문단 14 · 근거 문단 19) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 결정상 · 이온전도도가 비슷한 상용 argyrodite 분말 셋 (SE-1 = **BD**: 넓고 두 봉우리 · D50 ≈9.9 µm [판독] / SE-2: 중간 / SE-3 = **ND**: 좁은 · D50 ≈1.6 µm [판독]) 을 200 mg · ⌀13 mm PEEK 다이에서 **110 · 220 · 330 · 440 MPa (2 분)** 로 눌러 **다이에서 꺼내지 않은 채** 두께를 재 기공을 내면 (분모 = Li₆PS₅Cl 진밀도 **1.64 g/cm³**) 넓은 PSD 가 가장 치밀하다 (440 MPa **BD 1.73 ± 0.32 % ↔ ND 6.19 ± 0.46 %** · 표 S1) — 그러나 FIB-SEM 3D 재구성 (복셀 45 nm) 에서 BD 의 국소 기공은 **8.129 %** 로 펠릿 평균의 4.7 배이고 공극이 덩어리로 뭉친다 (ND 6.752 %) · in-SEM 나노압입 지도 (110 점 · 330 × 300 µm²) 에서 BD 는 국소 Er · H 가 넓게 흩어지고 무른 자리가 모여 있다 (HI_Er 0.74 → 0.24 ↔ ND 0.16 → 0.04 [판독] · 440 MPa Moran's I ≈0.16 ↔ ≈−0.07 [판독]) · Sn 합금 음극 전셀 (20 MPa · 30 °C) 에서 분리막만 BD 로 바꾸면 100 사이클 유지율 **63.1 %** (ND-ND **94.6 %**) 로 떨어지고 (음극 SE 만 바꾸면 76.1 %) 분리막 균열 · 음극 계면 박리가 보인다 — 저자 결론 *"pore-network homogeneity is a key determinant of the mechanical reliability"* (p.1).
**모델**: FIB-SEM 단면으로 만든 **2D 평면변형 선형 탄성 FEM** (Sn 리튬화 → 화학 변형 · 단방향 · 접합 계면 · 기공 = 자유 표면 · 균열 · 박리 · 소성 없음 · SE E = BD 의 Er 33.13 GPa 를 두 분리막에 같이) 과 **3D GeoDict GrainGeo 구조** (같은 D50 1.584 µm · 같은 기공 6.752 % · 20 MPa) 의 응력 집중 비교 — **DEM · MPM · 압밀 계산 · 탈압은 없다.**

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 잰 재료 · 시편 꼴 | 상용 argyrodite 분말 셋 — SE-1 (BD) Inchems · SE-2 Jeong Kwan (한국) · SE-3 (ND) *"a commercial supplier"* · 셋 다 고상 합성 · XRD 같은 argyrodite 상 (그림 S1a) · **조성 = "argyrodite" · 표 S2 의 "LPSCl" · 진밀도 가정 Li₆PS₅Cl 뿐** (정확한 화학식 [미확인]) · σ_ion 1.53 · 1.35 · 1.7 mS/cm (440 MPa 펠릿 · 30 °C) | [인쇄] p.6 · p.15 · 그림 S1 · 표 S2 |
| ② ★ 순수 SE 압력별 기공 | **표 S1 (평균 ± 표준편차 · 펠릿 5 개)**: 110 / 220 / 330 / 440 MPa → BD 13.78 / 7.88 / 4.94 / 1.73 % · SE-2 21.84 / 13.84 / 8.04 / 3.69 % · ND 23.75 / 15.82 / 9.28 / 6.19 % · 분모 = Li₆PS₅Cl 진밀도 **1.64 g/cm³** (출처 인용 없음) · **측정 상태 = 누른 뒤 다이 안 (꺼내지 않음) · 하중 상태 = 사진 (그림 S2) 상 프레스 밖** | [인쇄] 표 S1 · 그림 S3 · p.17 · [카드 해석] 그림 S2 |
| ③ ★ 두께 | 0.9–1.3 mm (압력 · 분말에 따라 · 조건별 숫자 없음) · 디지털 마이크로미터 5 점 평균 · [카드 산술] 질량 보존 두께 0.935 (BD 440) – 1.205 mm (ND 110) | [인쇄] p.17 · 그림 S3 · §3-2 |
| ④ ★ 공극망 균일성 지표 | FIB-SEM 국소 기공 지도 (z 방향 기공 복셀 비율 · x–y 마다) — 평균 = 국소 기공 · 표준편차 = 공간 편차: BD 8.129 % (±≈4.4 %p [판독]) ↔ ND 6.752 % (±≈1.6 %p [판독]) · 공극 크기 분포 (그림 S6) BD 꼬리 ≥2 µm ↔ ND ≤1.1 µm | [인쇄] p.7 · 그림 1f · S5 · S6 · [판독] |
| ⑤ ★ 국소 기계 이질성 | Berkovich 10 mN · 5–2–5 s · 깊이 0.4–2.3 µm · 110 점 / 지도 · 지도 하나 ≈1 h · **HI = IQR/중앙값** · 낮은 Er 몫 (모은 자료의 20 번째 백분위 12.228 GPa 아래): BD 59.0 → 2.72 % · ND 18.1 → 0 % (110 → 440 MPa) · Moran's I (440 MPa) BD 가 높다 · 국소 Er 은 성형압에 선형 (ND y = 0.06566x + 11.752 · Pc 0.985) | [인쇄] p.8 · p.17–18 · 그림 2 · S8 · [판독] |
| ⑥ 전셀 · 적층압 | NCM622 (LiNbO₃) ‖ Sn 복합 음극 · N/P 1.0 · 20 MPa · 30 °C · 적층압 변동 BD-ND 1.4–3.6 ↔ ND-ND 1.6–3.8 MPa (그림 안 글자) — 비슷 · 0.2C 100 사이클: BD-ND 376.1 → 237.2 mAh/g_Sn (63.1 %) · ND-ND 441.0 → 417.1 (94.6 %) · SE2-ND 89.2 % · ND-BD 76.1 % → 분리막 쪽 손실 31.5 %p ↔ 음극 쪽 18.5 %p | [인쇄] p.9–10 · 그림 3 · S9 |
| ⑦ 사후 단면 | BD-ND: 분리막 안 균열 + Sn 음극 / 분리막 계면 근처 박리 (빨강 표시) · ND-ND: *"largely intact"* · *"Intimate contact"* | [인쇄] p.11 · 그림 4a–b · S10 |
| ⑧ ★ 계산 모델 | ① 2D: COMSOL 6.3 · Sn 음극 단면 (FIB-SEM) + 분리막 3D 재구성에서 기공률이 같은 2D 단면 · Fick + Ohm + Butler–Volmer (Sn–SE 접점만) · 0.2C 로 750 mAh/g_Sn 까지 · **평면변형 · 선형 등방 탄성 · ε_ch 단방향 · 접합 계면 · 기공 자유 표면 · 20 MPa (집전체 쪽) + 롤러** · 분리막 SE E = 33.13 GPa (BD Er) · ν 0.37 → 고응력 면적 몫 BD 14.4 ↔ ND 4.8 % (P90 · von Mises [판독]) ② 3D: GrainGeo 복셀 0.2 µm · 100 × 100 × 75 (20 × 20 × 15 µm) · 기공 6.752 % 고정 · 20 MPa → 고응력 부피 몫 좁은 6.8 ↔ 넓은 13.7 % (P90 [판독]) | [인쇄] p.11–14 · p.19 · SI p.52–63 · 표 S2 · [판독] |
| ⑨ ★ DEM 한계 · 소성 · 2D/3D · 탈압 | **DEM 말 없음** (DEM · discrete element 0 회) · 소성 없음 — *"does not explicitly simulate crack initiation, crack propagation, or interfacial separation … indicators of mechanically vulnerable regions rather than … direct predictions of fracture"* (p.12) · 2D: *"the apparent connectivity of individual Sn domains in the 2D geometry does not necessarily represent their actual three-dimensional electronic connectivity"* (p.58) · 탈압 = 없음 (펠릿 두께는 누른 뒤 한 번 · 회복량 없음) | §4-3 |
| ⑩ ★ 판독 관찰 (원인 미확인) | (a) **그림 5a 에 'Narrow PSD' 곡선이 안 보인다** (화소 검사 0) · 보이는 'Broad PSD' 곡선은 그림 1a 의 ND 실측 PSD 와 판독 정밀도 안에서 같은 꼴 (D50 1.584 ↔ ND ≈1.59 µm) (b) **그림 5d (GrainGeo 구조 공극 크기) 와 그림 S6 (FIB-SEM BD · ND) 의 곡선이 같은 꼴** (봉우리 비 1.71 = 1.71) · 복셀 0.2 µm 인데 0.1 µm 계급 (c) SN3 · 표 S2 의 *"Er = 33.13 GPa; Figure 1i"* ↔ 그림 1i BD 판독 **31.0 GPa** | [판독] §3-9 |
| ⑪ 절대값 전이 | 재료가 **argyrodite (Li₆PS₅Cl 계로 가정)** 라 우리 SE 와 같은 계 · 분모도 랩 표준과 같은 1.64 — 다만 **우리 분말의 PSD 가 아니다** (같은 압력에서 PSD 만으로 기공이 1.73–6.19 % · 13.78–23.75 % 로 갈린다) · FEM 응력 (GPa) 은 선형 탄성 · 접합 가정의 상대 지표 (절대값 전이 불가) | §7 |

⛔ **한정어 (떼지 말 것)**: ① **ChemRxiv 원고 · 동료 심사 전** (*"Data may be preliminary"*) ② 펠릿 기공은 **다이 안 · 누른 뒤** 두께 + **진밀도 1.64** 가정 (분말 실제 조성 · 밀도 미측정) ③ 나노압입 지도는 **조건마다 펠릿 하나 · 110 점** (공간 통계의 반복 = 펠릿 간 반복 없음) · Er = 환산 탄성률 (영률 아님 · 다공 펠릿 표면의 국소 유효값) ④ FEM = **2D 평면변형 · 선형 탄성 · 접합 · 파괴 없음 · 단방향** — 응력 크기 (거리 칸 평균 2.2–4.1 · P95 최대 12.7 GPa · 히스토그램 꼬리 ≈100 GPa 계급 [판독]) 는 같은 SE 의 압입 경도 (440 MPa ≈2.2–2.7 GPa [판독]) 보다 크거나 수십 배 — **상대 비교만** ⑤ BD ↔ ND 는 **D50 · PSD 폭 · 기공 셋이 함께 바뀐 비교** (저자도 p.13 에서 인정) — 3D GrainGeo 비교가 이를 가르려 했으나 그림 5a · 5d 의 판독 관찰 (⑩) 이 그 그림의 입력을 [미확인] 으로 만든다 ⑥ 전셀 = Sn 합금 음극 · NCM622 · 1.186 mAh/cm² · 20 MPa · 30 °C — 우리 복합 양극 압밀과 다른 하중 (음극 팽창).

---

## 0-1. ★ 고른 의도 대조 (후보 표 밖 · U-1123-2 · 1저자 11-23 '논문에이전트 부탁')

의도 원문 (지시서 '이 논문만의 덧붙임'): *"분말 압축 SE 분리막의 공극망 균일성 ↔ 기계 신뢰성 — 우리 순수 SE 기준 (랩 표준: 기공률 10–13 % · 진밀도 1.64 g/cm³) 과 견줄 값 (압력 · 기공률 · 두께 · 측정법) 을 원문 그대로 모은다. · ChemRxiv 원고 (동료 심사 전) 표지."*  가리킨 카드 (근거 칸) = **없음** (후보 표 행이 아니다).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "분말 압축 SE 분리막의 공극망 균일성 ↔ 기계 신뢰성" | **채움** (한정 셋) | 논문의 주제 그 자체 (p.1 초록 · 그림 1–5).  BD ↔ ND: 펠릿 기공 1.73 ↔ 6.19 % (440 MPa) · 국소 기공 8.129 ↔ 6.752 % · HI_Er 0.24 ↔ 0.04 (440 MPa [판독]) · 유지율 63.1 ↔ 94.6 % · 사후 균열 · 박리 (BD).  한정: ① 상관 + 2D 탄성 응력 지도이지 파괴 계산이 아니다 (p.12) ② D50 · PSD 폭 · 기공이 함께 바뀐다 (p.13) ③ 원고 · 심사 전 |
| "우리 순수 SE 기준과 견줄 값 — **압력**" | **채움** | 110 · 220 · 330 · 440 MPa · 2 분 (그림 S3 글) · 200 mg · ⌀13 mm PEEK 다이 · 연마한 스테인리스 막대 (p.17 · 그림 S7a) · 누름 속도 [미확인] · 온도 (글러브박스 · 숫자 없음) [미확인] |
| "— **기공률**" | **채움** | 표 S1 (3 분말 × 4 압력 · 평균 ± 표준편차 · n = 5 펠릿) · 식 = 1 − m/(π r² t ρ_th) (그림 S3) · 300 MPa 값은 없다 → [카드 산술] 220–330 보간 ND ≈10.7–11.1 · SE-2 ≈9.3–9.6 · BD ≈5.6–5.7 % (§3-2) |
| "— **두께**" | **일부** | 범위 **0.9–1.3 mm** 만 인쇄 (조건별 숫자 없음) · 질량 보존으로 [카드 산술] 0.935–1.205 mm (인쇄 범위와 맞다) |
| "— **측정법**" | **채움** (한정) | *"To minimize microcrack formation during demolding, the pellet thickness was measured while the pellet remained inside the mold"* · 디지털 마이크로미터 5 점 평균 (그림 S2 · S3) · 펠릿 5 개.  한정: 다이째 (PEEK 몸통 + 막대) 를 마이크로미터에 물린 사진뿐 (표시창 '1003' mm · ZERO 단추 — 영점 상대 측정으로 보임 [카드 해석]) — 막대 길이를 빼는 절차 · 영점 · 남은 하중 [미확인] · **하중은 뺀 뒤 (프레스 밖)** [카드 해석 · 사진] |
| "— **진밀도 1.64 g/cm³**" | **채움** | *"The theoretical density of Li6PS5Cl was taken as 1.64 g cm−3."* (그림 S3 글 · p.32) — **랩 표준과 같은 수** · 출처 인용 없음 · 분말 실제 조성 · 비중병 밀도 [미확인] |
| "랩 표준 (기공률 10–13 %) 과 견줄" | **채움** (견줄 값만 · 판정 없음) | 같은 분모 · 같은 상태 (다이 안 · 하중 제거 후) 의 문헌 값: 330 MPa ND 9.28 · SE-2 8.04 · BD 4.94 % / 220 MPa 15.82 · 13.84 · 7.88 % — **랩 표준과 다른 문헌 값 (분말 PSD 가 다르다)** |
| "ChemRxiv 원고 (동료 심사 전) 표지" | **채움** | p.1 *"This is a preprint and has not been peer reviewed. Data may be preliminary."* · v2 · 2026-10-08 · CC-BY 4.0 · 카드 머리 · ⛔ 한정어 ① 에 표지 |

**가리킨 카드 · 이 논문을 인용한 카드의 2 차 인용 대조**: **해당 없음** — 후보 표 행이 아니고, 정본 `papers/` 에 이 논문 (DOI `15009882` · 제목 'pore-network homogeneity' · 저자 Hyeok-Rae · Hyeong-Jong) 을 적은 카드가 없다 (git grep 0 건 · 2026-11-23).

⇒ **의도 대조 결과: 채움** (한정: 두께는 범위 0.9–1.3 mm 만 = 일부 · 다이 안 측정의 막대 처리 · 남은 하중은 사진뿐).

---

## 1. 한 줄 요약
분말 압축 SE 분리막의 기계 상태는 흔히 펠릿 평균 기공 · 평균 탄성률 · 셀 적층압 변화로만 판단하는데, 이 원고는 **결정상 · 전도도가 비슷한 argyrodite 분말 셋** 으로 넓은 PSD 가 더 잘 채워 펠릿 기공은 낮추지만 (440 MPa 1.73 %) **공극을 덩어리로 남겨** 국소 탄성률이 넓게 흩어지고 (FIB-SEM · 나노압입 지도), Sn 음극의 팽창 하중 아래 그 분리막만 깨진다는 것을 보인다 (적층압 변동은 비슷 · 유지율 63.1 ↔ 94.6 %).
2D 이미지 기반 탄성 FEM 이 BD 의 뭉친 공극 둘레에 von Mises · 인장 정수압이 몰리는 것을 보이고, 같은 D50 · 같은 기공의 3D 구조 비교가 *"PSD-dependent particle packing provides an additional origin of mechanical heterogeneity"* (p.14) 를 받친다 — 결론: 분리막 설계 기준에 **이온전도도 · 치밀화 말고 공극망 균일성** 을 더하라.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE) | 연구유형 |
|---|---|---|---|---|
| H.-R. Cho · H.-J. Kim (공동 1저자) · J.-S. Kim · B. J. Park · Y. Kim · D. Lee · J. Kim · H. Kim · **S.-K. Jung\*** (서울대) | **ChemRxiv 원고 v2 (2026-10-08 게시 · 동료 심사 전 · CC-BY 4.0)** · PDF 66 쪽 (본문 + SI) | 10.26434/chemrxiv.15009882/v2 | 상용 argyrodite 분말 셋 (SE-1 BD · SE-2 · SE-3 ND) — 순수 SE 펠릿 · 분리막 / 전셀: LiNbO₃-SC-NCM622 · Sn | 실험 (PSD · 펠릿 기공 · FIB-SEM · in-SEM 나노압입 지도 · 전셀 + 적층압 · 사후 SEM) + 이미지 기반 선형 탄성 FEM (2D 평면변형 전기화학–역학 · 3D 역학) |

- **1저자 메모와의 대조**: 저자 (H.-R. Cho · H.-J. Kim · J.-S. Kim · B. J. Park · Y. Kim · D. Lee · J. Kim 외 — 외 = Hyojun Kim · Sung-Kyun Jung\*) · 제목 · ChemRxiv v2 · 첫 쪽 날짜 8 October 2026 · DOI · 66 쪽 — **모두 같다**.  덧붙임: ① 66 쪽 = 본문 + 그림 + **SI 전부 포함** (그림 S1–S21 · 보충 노트 1–3 · 표 S1–S2 · SI 참고문헌 13) ② 공동 1저자 (Cho · H.-J. Kim) ③ 교신 = Sung-Kyun Jung (표지는 대문자 'SUNG-KYUN JUNG') ④ PDF 꼬리 정보 subject *"ChemRxiv 2026.2026"* · 생성 2026-10-09 04:59 (−07:00 · 게시 다음 날) · 제작 iText 4.2.0.
- **글의 꼴**: 도입 (p.4–6) → 소제목 넷: *Decoupling bulk densification from local pore-network homogeneity* (p.6–7) · *Spatial heterogeneity of mechanical response governed by pore network architecture* (p.7–9) · *Separator-dependent cycling stability under comparable cell-level pressure evolution* (p.9–11) · *Pore-network heterogeneity and local stress concentration in solid-electrolyte separators* (p.11–13) · *Separating particle-size and distribution effects on pore architecture and separator mechanics* (p.13–14) → 결론 (p.14–15) → Methods (p.15–20) → 참고문헌 50 (p.21–23) → 그림 1–5 + 캡션 (p.24–29) → SI (p.30–66).  그림 5 · 그림 S 21 · 표 S 2 · 번호 붙은 식 0 (식은 SI 글 · 그림 S14 안).
- 같은 그룹 · 이웃 원고: SI 참고문헌 [2] Park C. et al. *Nat. Commun.* 16, 8838 (2025) = FIB-SEM 전처리 절차 (*"same image-preprocessing procedure as that used in our previous study"* p.52) · [3] Lee D. et al. *Joule* 9, 102046 (2025) = 전기화학–역학 모형 · Table S2 값 출처 — 두 편 모두 정본 카드 없음.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 분말 셋 — 출처 · 상 · 전도도 · 입도 (p.6 · p.15 · p.17 · 그림 1a–b · S1 · 표 S2 · `txt_p6_psd_bulk_porosity_110_440.png`)
| 항목 | SE-1 (**BD**) | SE-2 | SE-3 (**ND**) | 표지 |
|---|---|---|---|---|
| 공급 | Inchems Co., Ltd. | Jeong Kwan Co., Ltd. (Korea) | *"a commercial supplier"* | [인쇄] p.15 |
| 합성 | *"All three samples were synthesized by solid-state routes"* (용매 잔류 영향 최소화 [39]) | ← | ← | [인쇄] p.6 |
| 상 | argyrodite (XRD · Cu Kα · SmartLab · 냉간 펠릿 · '#' = 필름 봉우리 ≈38.3 · ≈44.4°) | ← | ← | [인쇄] 그림 S1a · [판독] '#' 위치 |
| σ_ion (440 MPa 펠릿 · 30 °C · PEIS 7 MHz–0.1 Hz · 10 mV) | **1.53 mS/cm** | **1.35** | **1.7** | [인쇄] 그림 S1b · 표 S2 (SE-2 는 그림 S1b 에만) |
| PSD 꼴 | *"broad and asymmetric … both fine and coarse particle fractions"* — 두 봉우리 ≈1 µm (≈1.2–1.3 %) · ≈15–20 µm (≈2.8–2.9 %) · 100 µm 까지 | 한 봉우리 ≈1.6 µm (≈4.3–4.4 %) · ≈10 µm 에서 끝 | 한 봉우리 ≈2 µm (≈3.85–3.9 %) · ≈12 µm 에서 끝 | [인쇄] p.6 · [판독] 그림 1a |
| D10 | ≈0.81 µm | SE-3 표지에 가림 (≈0.47) | ≈0.47 µm | [판독] 그림 1b (로그축 84 px/decade) |
| D50 | **≈9.9 µm** | ≈1.2–1.4 | **≈1.59 µm** | [판독] |
| D90 | ≈38 µm | ≈3.1–3.6 | ≈4.3 µm | [판독] |
| D95 | ≈52 µm | ≈3.9–4.5 | ≈5.5 µm | [판독] |
| 조성 · 밀도 | **화학식 · 할로젠 비 · 비중병 밀도 없음** — 진밀도는 *"theoretical density of Li6PS5Cl … 1.64 g cm−3"* 로 가정 · 표 S2 는 "Solid Electrolyte (LPSCl)" | ← | ← | [미확인] · [인쇄] 그림 S3 |

- PSD 측정 = Microtrac Bluewave (p.17) — 건식 / 습식 분산 · 분산매 · 초음파 [미확인].
- 저자 문장: *"SE-1 exhibited larger D50, D90 and D95 values than SE-2 and SE-3. We therefore refer to SE-1 and SE-3 as BD and ND, representing broad- and narrow-PSD samples"* (p.6) — **BD 는 'PSD 가 넓은' 동시에 'D50 이 6 배 큰' 분말이다** [카드 산술 9.9/1.59 = 6.2 · 판독값].
- [카드 해석] σ_ion 셋은 1.35–1.7 mS/cm (±12 %) 로 가깝다 — 저자가 *"comparable ionic conductivities"* 로 묶은 근거.  펠릿 기공이 1.73–6.19 % 로 달라도 (440 MPa) σ 가 PSD 순서를 따르지 않는다 (SE-2 가 가장 낮다).

### 3-2. ★ 순수 SE 펠릿 기공 — 표 S1 · 측정 사슬 · 산술 검산 (p.6 · p.17 · 그림 1c · S2 · S3 · 표 S1 · `txt_p17_bulk_porosity_in_mold_thickness.png` · `eq_unnumbered_figS3_*.png`)
**표 S1 (인쇄 · 평균 ± 표준편차 · 조건마다 독립 펠릿 5 개)**
| 압력 (MPa) | SE-1 (BD) | SE-2 | SE-3 (ND) |
|---|---|---|---|
| 110 | **13.78 ± 0.17 %** | 21.84 ± 0.15 % | **23.75 ± 1.21 %** |
| 220 | 7.88 ± 0.23 | 13.84 ± 0.38 | 15.82 ± 0.91 |
| 330 | 4.94 ± 0.30 | 8.04 ± 0.68 | 9.28 ± 0.44 |
| 440 | **1.73 ± 0.32** | 3.69 ± 0.85 | **6.19 ± 0.46** |

**측정 사슬 (인쇄)**: Ar 글러브박스 (O₂ · H₂O < 1 ppm) → 분말 **200 mg** → **⌀13 mm PEEK 다이 · 연마한 스테인리스 막대 (플런저)** → **일축 냉간 가압 110–440 MPa · 2 분** (그림 S3 글 — 본문 p.17 은 유지 시간을 적지 않는다) → *"To minimize microcrack formation during demolding, the pellet thickness was measured while the pellet remained inside the mold"* (p.17) → **디지털 마이크로미터 5 곳** → t = (t₁+…+t₅)/5 → ρ_bulk = m/(π r² t) → **기공 (%) = [1 − ρ_bulk/ρ_theoretical] × 100 · ρ_theoretical = 1.64 g/cm³ (Li₆PS₅Cl)** → 펠릿 5 개 평균 ± 표준편차.
- **하중 상태**: 글에는 '다이 안' 만 있고 하중을 뺐는지 적지 않았다.  그림 S2 사진은 **프레스 밖에서 다이째 (금속 원판 + PEEK 고리 둘 + 스테인리스 막대) 를 마이크로미터 두 앤빌 사이에 물린 모습** → **누른 뒤 · 하중 제거 · 다이 안 (반경 구속 유지)** [카드 해석 · 사진].  사진의 표시창 = '1003' (단위 mm · 소수점은 사진에서 분명치 않음 — 1.003 mm 이면 인쇄 두께 범위 0.9–1.3 mm 안) · 'ON/OFF ZERO' 단추 → 원판 · 막대를 물린 채 영점을 잡아 펠릿 두께만 읽은 것으로 보인다 [판독 · 카드 해석 — 절차 글 없음].  막대 길이를 빼는 법 · 영점 · 마이크로미터 측정력 [미확인].
- **두께**: *"0.9-1.3 mm depending on the applied pressure and SE type"* (p.17) — 조건별 값은 없다.  [카드 산술] 질량 보존 t = m/(π r² ρ_th (1 − ε)) = 0.200 g / (1.3273 cm² × 1.64 g/cm³ × (1 − ε)): BD 1.066 → 0.935 mm · SE-2 1.176 → 0.954 · ND 1.205 → 0.979 mm (110 → 440 MPa) — 인쇄 범위 (0.9–1.3) 와 맞다.
- **300 MPa (우리 압축 압력) 값은 없다** → [카드 산술] 220–330 MPa 보간: 선형 BD **5.74** · SE-2 **9.62** · ND **11.06 %** / 로그-선형 5.61 · 9.32 · 10.73 %.
- **Heckel (원문은 하지 않았다)** [카드 산술] ln(1/ε) = K·P + A (4 점): BD K = 0.00608 /MPa (**P_y ≈ 164 MPa** · R² 0.964) · SE-2 0.00534 (**≈187 MPa** · 0.985) · ND 0.00415 (**≈241 MPa** · 0.997) / 220–440 MPa 만: 145 · 166 · 234 MPa.  ⚠ 누른 뒤 (다이 안 되돌아옴 포함) 밀도의 Heckel 이다 — 가압 중 Heckel 과 같은 양이 아니다.
- 같은 압력에서 ND − BD = 9.97 · 7.94 · 4.34 · 4.46 %p (110 → 440 MPa) [카드 산술] — PSD 만으로 기공이 2–4 배 다르다 (440 MPa 6.19/1.73 = **3.6 배**).
- 저자 해석: *"multiscale particle packing in a broadly distributed powder, where fine particles can occupy interstitial voids between coarse particles and thereby increase pellet-scale densification"* (p.6).

### 3-3. ★ FIB-SEM — 국소 기공 · 공극 크기 (p.6–7 · p.18 · SI p.52–53 · 그림 1d–h · S4 · S5 · S6 · S11 · `txt_p7_bulk_vs_fibsem_local_porosity.png` · `txt_p18_thresholds_moran_fibsem_voxels.png`)
| 항목 | 값 | 표지 |
|---|---|---|
| 장비 · 조건 | ZEISS Crossbeam 550 · FIB 15 nA · 슬라이스 75 nm · 면내 화소 45 nm → 밀링 방향 재표본화 = **45 nm 등방 복셀** (물리 두께 보존 · 복셀 수 > 실제 슬라이스 수) · 정렬 · 커튼 줄무늬 · 잡음 제거 (선행 연구 절차) · **watershed 분할 (SE / 기공 둘)** | [인쇄] p.18 · SI p.52–53 |
| 부피 | BD 932 × 1536 × 1064 복셀 = 41.94 × 69.12 × 47.88 µm · ND 1045 × 1034 × 1282 = 47.03 × 46.53 × 57.69 µm (그림 S11 캡션은 47.025) — 둘 다 **440 MPa 펠릿** | [인쇄] |
| 실제 슬라이스 | [카드 산술] BD ≈638 · ND ≈769 장 (47.88 · 57.69 µm ÷ 75 nm) | [카드 산술] |
| 국소 기공 (부피 평균) | **BD 8.129 % · ND 6.752 %** (펠릿 1.73 · 6.19 %) — 국소/펠릿 = 4.70 · 1.09 [카드 산술] | [인쇄] p.7 · 그림 1f · S11 |
| 국소 기공의 공간 편차 | 기공 분율 지도 (x–y 마다 z 방향 기공 복셀 비율 · 그림 S5) 의 표준편차 = 그림 1f 막대: **BD ≈±4.4 %p (3.7–12.6 %) · ND ≈±1.6 %p (5.2–8.3 %)** · 지도 색 0–30 % · 지도 넓이 BD ≈48 × 42 · ND ≈58 × 47 µm [판독 그림 1d–e 축 끝 — 부피의 세 변 가운데 둘과 같은 크기] | [판독] 그림 1f · [인쇄] 그림 S5 캡션 |
| 공극 크기 분포 | 그림 S6: 계급 0.1 · 0.3 · 0.5 … µm · 둘 다 봉우리 0.3 µm · **ND 는 1.1 µm 에서 끝 · BD 는 ≥2.0 µm 꼬리** · y 축 "Counts" 눈금 없음 | [판독] 그림 S6 |
| 저자 한정 | *"Because FIB-SEM tomography probes a finite local volume and depends on imaging resolution and segmentation criteria, these local values should not be interpreted as direct substitutes for pellet-averaged porosity."* (p.7) | [인쇄] |

### 3-4. ★ 나노압입 지도 — 조건 · 지표 · 값 (p.7–9 · p.17–18 · SI p.51 · 그림 1i · 2 · S7 · S8 · `txt_p8_hi_low_er_threshold_moran.png` · `txt_p17_nanoindentation_protocol.png` · `eq_unnumbered_SN1_*.png`)
**조건 (인쇄)**: PI 89 (Methods = *"Hysitron"* · 그림 S7 = *"Bruker"*) · SEM 안 · 손수 만든 비노출 시편 홀더 · **Berkovich** · 펠릿 **조각** 의 윗면 (그림 S7b — 연마 여부 [미확인] · 막대 면에 닿았던 면으로 보임 [카드 해석]) · **330 × 300 µm² · 110 점 · 간격 30 µm** (= 11 × 10 격자 [카드 산술]) · **최대 10 mN · 부하 5 s – 유지 2 s – 제하 5 s** · 자동 · 지도 하나 ≈1 h · 깊이 ≈0.4–2.3 µm (그림 S7 캡션) · Oliver–Pharr: H = P_max/A_c · h_c = h_max − 0.75 P_max/S · A_c = 24.5 h_c² (이상 · 실제는 보정한 면적 함수) · E_r = (√π/(2β)) S/√A_c.  저자: *"the measured Er and H values were interpreted as local effective mechanical responses of the pressed SE pellets because they reflect not only the mechanical response of the SE phase but also local porosity, particle packing, and surface condition"* (SI p.51).
- **시편 수**: *"110 indents on one pellet per SE"* (그림 1 캡션) — 조건 (분말 × 압력) 마다 **펠릿 하나**.

| 지표 · 정의 | BD | ND | 표지 |
|---|---|---|---|
| 그림 1i (440 MPa · 평균 ± SD) Er | **≈31.0 ± 7.1 GPa** | **≈38.4 GPa** (SD 막대가 표지 고리 안 → ≲1.9) | [판독] 표지 고리 화소 · 축 5.3 px/GPa |
| 그림 1i H | ≈2.21 ± 0.75 GPa | ≈2.72 GPa (고리 + 막대 ≲±0.2) | [판독] 오른 축 53 px/GPa |
| 중앙값 Er (그림 2a · 2b) 110 → 440 MPa | ≈10.1 → ≈32.1 GPa | ≈14.6 → ≈38.5 GPa | [판독] 바이올린 흰 점 (상자 안 흰 화소 중심 · 축 눈금 0 = 418.5 · 60 = 99 px) |
| 바이올린 범위 Er (110 · 440 MPa · 그려진 꼴의 끝 — 자료 끝과 같다는 보장 없음) | ≈0.5–59 · ≈2–51 GPa | ≈5–20 · ≈25–44 GPa | [판독] 같은 축 |
| 중앙값 H (110 → 440 MPa) | ≈0.53 → ≈2.36 GPa | ≈1.31 → ≈2.74 GPa | [판독] 같은 법 (오른 축 0–6 GPa) |
| **HI_Er = IQR_Er / median_Er** (110 · 330 · 440 MPa) | **0.74 · 0.37 · 0.24** | **0.16 · 0.075 · 0.039** | [판독] 그림 2c · [인쇄] 정의 p.8 |
| HI_H (110 · 330 · 440) | 1.44 · 0.68 · 0.34 | 0.28 · 0.065 · 0.042 | [판독] 그림 S8a |
| 낮은 Er 몫 (< 12.228 GPa = 네 지도 모은 440 점의 20 번째 백분위) 110 → 440 | **59.0 → 2.72 %** | **18.1 → 0 %** | [인쇄] 그림 2h 안 글자 · p.18 |
| 낮은 H 몫 (< 0.748 GPa) 110 → 440 | 60.9 → 8.18 % | 10.9 → 0 % | [인쇄] 그림 S8f |
| Moran's I (440 MPa · Er) | ≈0.16 | ≈−0.07 | [판독] 그림 2h 오른 축 |
| Moran's I (440 MPa · H) | ≈0.17 | ≈0.01 | [판독] 그림 S8f |
| 국소 Er vs 성형압 (110–440 MPa · 그림 안 맞춤 · Pc = Pearson) | y = 0.05469x + 6.371 (Pc 0.705) | y = 0.06566x + 11.752 (Pc 0.985) | [인쇄] 그림 S8g |
| 국소 H vs 성형압 | y = 0.003706x + 0.518 (Pc 0.471) | y = 0.004377x + 1.058 (Pc 0.974) | [인쇄] 그림 S8h |

- **검산** [카드 산술]: 낮은 몫 × 110 = 자리 수 — Er 64.9 · 19.9 · 2.99 · 0 → 65 + 20 + 3 + 0 = **88 = 440 × 0.20** ✓ · H 67 + 12 + 9 + 0 = 88 ✓ (정의와 인쇄 숫자가 서로 맞다).
- Moran's I 가중: *"unit weights for horizontally and vertically adjacent sites and zero weights otherwise. Self-pairs were excluded, and no row standardization was applied."* (p.18) — 유의성 검정 · 기댓값 (−1/(n−1) = −0.0092 [카드 산술]) 은 원문에 없다 [미확인].
- [카드 해석] 440 MPa 에서도 BD 의 Er 표준편차 (≈7.1 GPa) 가 ND (≲1.9 GPa) 의 ≳3.7 배 · 바이올린 범위 BD ≈2–51 ↔ ND ≈25–44 GPa [판독] — *"coexistence of mechanically compliant and relatively stiff regions"* (p.9) 의 근거.
- 지도 격자 (그림 2d–g 축): X 0–300 · Y 0–270 µm = **11 × 10 점** [판독] — '330 × 300 µm²' 는 점마다 30 µm 칸을 둔 넓이 [카드 해석] · 색 막대 BD 110 MPa 5.0–20.0 GPa · BD 440 MPa 위 끝 42.0 GPa — 막대 위에 빨강 칸이 붙어 있다 (범위 밖 값 표시로 보임 [카드 해석] · 이 규칙을 캡션에 적은 것은 H 지도의 그림 S8 뿐).

### 3-5. ★ 전셀 · 적층압 · 사이클 (p.9–10 · p.15–16 · 그림 3 · S9 · `txt_p9_stack_pressure_comparable.png` · `txt_p10_capacity_retention_values.png` · `txt_p16_*.png`)
**셀 (인쇄)**: 양극 = 단결정 NCM622 (BASF) 에 LiNbO₃ 습식 코팅 (1 g 당 Li-Nb 에톡사이드 400 µL + 에탄올 800 µL · 1 h · 50 °C 진공 건조 · 350 °C 30 분 공기 · 10 °C/min [50]) : SE-3 (ND) : CNF = **65 : 30 : 5 wt%** (막자 15 분) · 음극 = Sn (Alfa Aesar) : SE = **60 : 40 wt%** (Thinky AR-100 · 지르코니아 볼 5 · 2000 rpm 30 분 · 음극 SE = BD / SE-2 / ND) · 조립: SE 200 mg → ⌀13 mm PEEK · **20 MPa 30 s 예비 가압** → 양극 11 mg · **220 MPa 2 분** → 음극 3.5 mg · **440 MPa 2 분** → 바깥 강철 케이스 · 토크 렌치 **20 MPa** · N/P 1.0 (Sn 750 · NCM622 220 mAh/g) · 하중형 셀 (TLP1109-SR, Teraleader) · WBCS 3000 · **30 °C** · 화성: C/10 · 1.186 mAh/cm² 한도 → 2.0 V 방전 → 0.1C 2 회 (2.0–4.0 V) → 0.2C · **1C = 1.186 mA/cm²**.
- [카드 산술] 면적 용량 검산: 양극 11 × 0.65 = 7.15 mg NCM ÷ 1.327 cm² × 220 mAh/g = **1.185 mAh/cm²** · 음극 3.5 × 0.60 = 2.1 mg Sn ÷ 1.327 × 750 = **1.187 mAh/cm²** → 인쇄 1.186 · N/P 1.0 과 맞다 · 750 mAh/g_Sn = Li₃.₃Sn [카드 산술 · Li₄.₄Sn = 993 mAh/g].
- [카드 해석] 분리막 SE 층은 20 MPa 예비 가압 뒤 양극 (220 MPa) · 음극 (440 MPa) 가압을 함께 받는다 → 셀 분리막의 마지막 성형압 = 440 MPa (펠릿 · FIB-SEM · 나노압입의 440 MPa 와 같은 이름) — 원문은 이 대응을 따로 말하지 않는다.

| 셀 [분리막 SE – 음극 SE] | 0.2C 방전 처음 → 100 사이클 (mAh/g_Sn) | 유지율 | 표지 |
|---|---|---|---|
| ND-ND | 441.0 → 417.1 | **94.6 %** | [인쇄] p.10 |
| BD-ND | 376.1 → 237.2 | **63.1 %** | [인쇄] |
| SE2-ND | 403.8 → 360.1 | 89.2 % | [인쇄] p.10 · 그림 S9 |
| ND-SE2 (분리막 ND · 음극 SE-2) | (그림 S9e 곡선만) | ≈93.6 % [카드 산술 94.6 − 1] | [인쇄] 그림 S9f 손실 **1** %p (SE2-ND **5.4** %p = 94.6 − 89.2 ✓) |
| ND-BD | (처음 ≈426 [카드 산술 324.4/0.761]) → 324.4 | 76.1 % | [인쇄] p.10 |
| 손실 (ND-ND 기준) | 분리막에 BD **31.5 %p** ↔ 음극에 BD **18.5 %p** | — | [인쇄] p.10 · 그림 3g |

- **적층압 변동** (초기 사이클 · 0.1C → 0.2C → 0.4C): ND-ND *"Stress change range : 1.6 ~ 3.8 MPa"* · BD-ND *"1.4 ~ 3.6 MPa"* [인쇄 · 그림 3a–b 안 글자] — 본문 *"pressure variations of several megapascals, with comparable magnitudes over the measured early cycles"* (p.9).
- 그림 3a–b 시간축 ≈0–85 h · 구간 0.1C (≈0–44 h) → 0.2C → 0.4C [판독] · BD-ND 의 0.4C 구간 끝 (≈78–82 h) 전압 선이 빽빽한 띠로 그려진다 — **원문 설명 없음** (관찰 · 원인 미확인).
- 율속 (그림 S9c · 첫 0.1C 뒤 0.2 / 0.4 / 0.8 / 1C / 다시 0.2C): BD-ND ≈393 / 287 / 139 / 96 / 388 · SE2-ND ≈413 / 331 / 195 / 146 / 418 · ND-ND ≈443 / 369 / 236 / 181 / 460 mAh/g_Sn [판독 · 사이클 구간 중앙값].
- 저자 결론: *"the magnitude of the cell-level mechanical load alone cannot account for the separator-dependent degradation"* (p.10).

### 3-6. 사후 단면 (p.11 · p.17 · 그림 4a–b · S10)
- cryo 단면 연마 (IB-19520CCP · 5 kV · 4 h) · SEM JSM-7600F · 100 사이클 뒤.
- BD-ND: *"cracks within the SE separator together with local delamination near the Sn composite anode-SE separator interface"* (그림 4a 빨강 = 균열 · 박리 · 그림 S10 = 원본 ↔ 표시 쌍) · ND-ND: *"a largely intact separator and interface without obvious cracking or delamination"* (그림 4b · *"Intimate contact"*).  눈금 150 µm.  균열 길이 · 면적 몫 숫자 없음 [미확인] · 시편 수 [미확인].

### 3-7. ★ 2D 디지털 트윈 FEM (전기화학–역학) — 식 · 값 · 가정 (p.11–13 · p.19 · SI p.52–63 · 그림 4c–h · S11–S21 · 표 S2 · `eq_unnumbered_SN3_*.png` · `eq_unnumbered_figS14_*.png` · `txt_p11_*` · `txt_p19_*` · `txt_p60_*` · `txt_p61_*`)
**기하**: Sn 복합 음극 = FIB-SEM **한 장의 관통 단면** (바깥 면 → 분리막 · 3D 재구성 안 함) 을 Sn (밝음 · watershed) → 기공 → 나머지 = SE 로 분할 · 분리막 = 3D 재구성 (BD · ND) 에서 **기공률이 3D 부피와 같은 2D 단면** 을 잘라 붙임 (*"cropping slices whose porosity matched that of the corresponding 3D volume"* 그림 S11 캡션) · 두 모형은 음극 · 크기 · 처리 · 격자 기준이 같고 분리막 단면과 **측정 이온전도도 (1.53 · 1.7 mS/cm)** 만 다르다 · COMSOL 6.3 (p.19 · SI p.54–55) · 격자 (요소 수 · 크기) · 풀이 설정 · 계산 시간 [미확인].
**지배식 (SI 노트 3 · 렌더에서 옮김)**: ∂c_Li/∂t + ∇·N_Li = 0 · N_Li = −D_Li ∇c_Li (Sn 안) · i_Sn = −σ_Sn ∇φ_Sn · i_SE = −κ_SE ∇φ_SE · ∇·i = 0 · j_loc = i₀[exp(α_a Fη/RT) − exp(−α_c Fη/RT)] (Sn–SE 가 맞닿은 곳만) · η = φ_Sn − φ_SE − U_eq(θ) · θ = (c_Li − c_Li,0)/(c_Li,max − c_Li,0) · −n·N_Li = j_loc/F · 0.2C 일정 전류 · **750 mAh/g_Sn 에서 끝** · 바깥 경계 절연 (양 끝 집전체 제외) · 양극 = 균질화 영역 (그림 S14: i_e = −σ_e,eff ∇φ_e · i_ion = −σ_i,eff ∇φ_ion · NCM 구 확산 · 1/r² ∂/∂r(D_s r² ∂c_s/∂r)).
**역학**: ∇·σ = 0 · ε = ε_el + ε_ch · σ = C:(ε − ε_ch) · **ε_ch = β_Sn θ I** (Sn 에만 · SE 에 화학 변형 없음) · *"The linear expansion coefficient was related to the volumetric expansion of Sn according to"* 뒤의 식은 **인쇄가 깨져 'βSn=¿' 로만 보인다** (γ_V 값도 없음) [미확인] · 그림 S14 는 같은 것을 **ε_Li = ⅓ β(SOL) I** 로 적는다 · **평면변형 [D] = E/((1+ν)(1−2ν)) [[1−ν, ν, 0], [ν, 1−ν, 0], [0, 0, (1−2ν)/2]]** (그림 S14) · **단방향** (응력이 화학 퍼텐셀 · 반응에 되먹임 없음) · *"The solid phases were assumed to remain mechanically bonded throughout the simulation, and displacement continuity was imposed at the Sn-SE and SE-SE interfaces"* · 기공 = 자유 표면 · **집전체 쪽 20 MPa · 나머지 롤러** (SI p.60–61).
**재료 (표 S2 · 인쇄)**: Sn c_max 271000 mol/m³ · σ_Sn 8.7 × 10⁴ S/cm · D (Sn → LiSn → Li₇Sn₃ → Li₅Sn₂ → Li₇Sn₂ → Li₂₂Sn₅) 1.1e-17 → 4.5e-17 → 4.3e-17 → 5.1e-17 → 1.6e-16 → 3.4e-16 m²/s · **E 50 → 41.1 → 31.29 → 30.73 → 29.75 → 28.08 GPa** · ν 0.33 → 0.2419 → 0.1791 → 0.1721 → 0.1617 → 0.1538 · Li 부분 몰부피 (Sn → Li₇Sn₂) 7.8775 → 8.4550 → 8.9106 → 9.9611 → 12.088 cm³/mol · i₀ (Sn) 0.01 mA/cm² · OCV 그림 S15 / NCM622 c_max 47764 mol/m³ · σ_e 1.00 × 10⁻² S/cm (Minnmann 2021) · D 2.00 × 10⁻¹² m²/s · i₀ **"2.254872 A cm⁻²"** (인쇄 단위 그대로 — 크기가 Sn 의 2 × 10⁵ 배 [카드 산술] · 단위 오기 가능성 [카드 해석]) / **SE: κ BD 1.53 · ND 1.7 mS/cm · E = 33.13 GPa ("Figure 1i, BD" — *"The measured reduced modulus of the BD pellet (Er = 33.13 GPa) was used directly as an approximate Young's modulus input"*) · ν 0.37 (Torii 2025 [SI 13] · DFT)**.
**출력 지표**: σ_vM = √(3/2 s:s) · σ_h = ⅓ tr σ (σ_h > 0 만 인장 분석 — *"particularly relevant to crack opening and interfacial separation in brittle sulfide electrolytes"*) · 분리막 SE 만 · **모은 (BD + ND) 분포의 P90 · P95 를 공통 문턱** 으로 f_high = A(σ > 문턱)/A_SE · 가까운 기공 경계까지 거리 (2D 유클리드 거리 지도) 0–0.1 · 0.1–0.3 · 0.3–0.5 µm 칸의 평균 · P95.

| 결과 (끝 충전 · 750 mAh/g_Sn) | BD | ND | 표지 |
|---|---|---|---|
| f_high-VM (P90) | **≈14.4 %** | ≈4.8 % | [판독] 그림 4f |
| f_high-VM (P95) | ≈8.1 % | ≈1.8 % | [판독] |
| f_high-tensile (P90) | ≈13.8 % | ≈7.5 % | [판독] 그림 4g |
| f_high-tensile (P95) | ≈5.1 % | ≈1.8 % | [판독] |
| σ_vM 평균 / P95 (0–0.1 µm) | ≈4.1 / **≈12.7 GPa** | ≈3.5 / ≈7.7 GPa | [판독] 그림 4h |
| σ_vM 평균 / P95 (0.1–0.3 µm) | ≈3.5 / ≈9.2 | ≈2.6 / ≈4.6 | [판독] |
| σ_vM 평균 / P95 (0.3–0.5 µm) | ≈3.0 / ≈6.9 | ≈2.2 / ≈3.5 | [판독] |
| 색 범위 | von Mises 0–20 GPa · 정수압 −2…2 GPa (그림 4e) / −5…5 GPa (그림 S19) · 히스토그램 (그림 S20) von Mises 꼬리 ≈100 GPa 계급까지 (BD) | | [판독] |

- [카드 산술] P90 정의 검산: (14.4 + 4.8)/2 = 9.6 % · P95 (8.1 + 1.8)/2 = 4.9 % — 두 분리막 SE 면적이 비슷하면 10 · 5 % 에 가까워야 한다 ✓ (인장은 σ_h > 0 영역만 문턱을 잡으므로 이 등식이 안 선다).
- 두 모형의 Sn 리튬화는 *"nearly identical"* (그림 S17 · x in LiₓSn 0–4.4) · 첫 충전 곡선은 실험 (0.1C) ↔ 계산 (0.2C) 으로 *"qualitatively"* 만 비교 (그림 S16 · 750 mAh/g_Sn 끝 전압 실험 ≈4.34 (BD) · ≈4.16 V (ND) ↔ 계산 ≈4.46 · ≈4.52 V [판독 · 곡선 오른끝 화소 · 축 131.8 px/V]) — ND 쪽 계산 ↔ 실험 차 (≈0.36 V) 가 BD (≈0.11 V) 보다 크다 (원문 설명 없음).
- 복합 음극 안 SE 의 응력 지도 (그림 S18 · S19) 는 실렸으나 본문 해석 없음 — S19 (왼 = BD · 오른 = ND · 캡션) 정수압은 BD 모형 쪽이 색 아래 끝 (−5 GPa) 근처 색으로 거의 채워져 더 압축 [판독 · 정성 · 원문 설명 없음] · 그림 S20 인장 정수압 꼬리 BD ≈35 · ND ≈18 GPa 계급까지 [판독].
- 저자 한정: *"the digital-twin model does not explicitly simulate crack initiation, crack propagation, or interfacial separation. The calculated stress fields should therefore be interpreted as indicators of mechanically vulnerable regions rather than as direct predictions of fracture."* (p.12).

### 3-8. ★ 3D 아래-위 (bottom-up) 구조 — GeoDict GrainGeo (p.13–14 · p.19 · SI p.56 · 그림 5 · `txt_p13_*` · `txt_p14_*` · `txt_p56_*`)
- 목적: *"Separating the effects of median particle size, PSD breadth, and total porosity … is challenging because these variables change simultaneously in the experimentally compacted powders"* (p.13) → 같은 D50 · 같은 기공 · 다른 PSD 폭의 3D 구조.
- 생성: GeoDict **GrainGeo** · **복셀 0.2 µm · 100 × 100 × 75 = 20 × 20 × 15 µm** · 그림 5a 의 PSD 를 입력 · **기공 6.752 % 로 고정 (= ND FIB-SEM 국소 기공)** · D50 = 1.584 µm (그림 5a 글자) → 복셀 → 메시 → COMSOL 6.3 3D 역학 FEM · **20 MPa** · 고응력 부피 몫 = 공통 문턱 넘는 SE 부피 / SE 부피 (기공 제외) (SI p.56).  알갱이 모양 · 겹침 허용 여부 · 6.752 % 를 맞춘 방법 · 재료 값 (본문은 *"material properties … held constant"* 만) · 경계 조건 (20 MPa 말고) · 격자 수 [미확인].
- 결과: 좁은 PSD = 작고 고른 공극 · 낮고 고른 von Mises / 넓은 PSD = 커지고 이어진 공극 둘레 응력 집중 (그림 5b–f · von Mises 색 0–80 MPa) · **고응력 부피 몫 P90 좁은 ≈6.8 ↔ 넓은 ≈13.7 % · P95 ≈3.4 ↔ ≈7.1 %** [판독 그림 5g] · 검산 (6.8 + 13.7)/2 = 10.2 % · (3.4 + 7.1)/2 = 5.3 % ✓ [카드 산술].
- 저자 결론 (범위 한정 포함): *"the distinct stress responses can be attributed primarily to differences in the pore architectures generated by different PSDs within the present model framework"* (p.14).
- [카드 해석] D50 1.584 µm 가 복셀 0.2 µm 로 **≈8 칸** 이고, 공극 크기 봉우리 0.3 µm 는 **1.5 칸** — 공극 둘레 응력 집중은 이 해상도에서 풀리지 않는다 (우리 MPM 의 d_h/dx ≳ 3.5 규칙과 같은 문제 · §8 U6).

### 3-9. ★ 판독 관찰 · 원문 안 어긋남 (원인 미확인 — 저자 확인 전에는 그 그림을 독립 결과로 인용하지 않는다)
1. **그림 5a — 'Narrow PSD' 곡선이 보이지 않는다.**  범례에는 검정 'Narrow PSD' · 빨강 'Broad PSD' 가 있으나 그림 안 (D50 세로선 · 범례 · 글자를 빼면) 검정 화소가 **0 개** [판독 · 원본 래스터 xref 46 화소 검사].  보이는 빨강 곡선은 **그림 1a 의 SE-3 (ND) 실측 PSD 와 0.1-decade 마다 차이 ≤0.25 %p** (예: 1 µm 3.09 ↔ 3.16 · 2 µm 3.87 ↔ 3.85 %) 이고, 인쇄 D50 1.584 µm 도 ND 의 D50 [판독 ≈1.59 µm] 과 같다 → **'넓은 PSD' 로 그려진 것은 ND 분말의 PSD 꼴** [카드 해석].  두 입력 PSD 의 숫자 (폭 · 범위) 는 원문에 없다 [미확인].
2. **그림 5d (GrainGeo 두 구조의 공극 크기 분포) ≈ 그림 S6 (FIB-SEM BD · ND).**  두 그림 모두 x 0–2.0 µm · 계급 0.1 · 0.3 · 0.5 … µm · y 축 눈금 없는 "Counts" 이고, 꼭짓점마다 정규화 높이가 0.01–0.04 안에서 같다 · 0.3 µm 봉우리 비 (좁은/넓은 · ND/BD) **1.71 = 1.71** · 좁은 = ND 둘 다 1.1 µm 에서 끝 [판독 · digitized.csv].  게다가 GrainGeo 복셀은 0.2 µm 인데 0.1 µm 계급 값이 있다 (복셀 45 nm 인 FIB-SEM 이면 가능) [카드 해석].  원문은 두 그림의 관계를 말하지 않는다.
3. **분리막 E 의 값**: SI 노트 3 · 표 S2 는 *"Er = 33.13 GPa; Figure 1i"* (BD) 라 적는데, 그림 1i 의 BD Er 표지 중심은 **≈31.0 GPa** [판독 · 고리 화소 866–878 · 축 5.3 px/GPa · 판독 오차 ≈±0.2 GPa] · 그림 2b 중앙값 ≈32 GPa · 그림 S8g 맞춤선의 440 MPa 값 30.4 GPa [카드 산술 0.05469 × 440 + 6.371].  33.13 이 어디서 왔는지 [미확인].
4. 화학 변형 식: 본문 ε_ch = β_Sn θ I (β_Sn = '선 팽창 계수') ↔ 그림 S14 ε_Li = ⅓ β(SOL) I — β 와 부피 팽창 γ_V 의 관계식은 인쇄가 깨졌다 ('β_Sn = ¿') [미확인].
5. 장비 이름: Methods *"PI 89, Hysitron"* ↔ 그림 S7 *"PI 89, Bruker"* (같은 계열 상표 · 내용 어긋남 아님 [카드 해석]).
6. NCM622 i₀ *"2.254872 A cm⁻²"* (표 S2) — 단위 그대로 옮김 · 크기 의문 [카드 해석].
7. 글자 층 결함 (인쇄는 정상): 'µm' 이 'μmm' 로 · 그림 4 · S21 캡션의 거리 칸 문구가 겹쳐 나온다 — 렌더로 확인 (figures.json 캡션은 고쳐 둠).

### 3-10. ★ 저자가 적은 한계 (원문 그대로)
1. 국소 기공 ≠ 펠릿 평균: *"these local values should not be interpreted as direct substitutes for pellet-averaged porosity"* (p.7).
2. 나노압입 = 국소 유효 응답: *"they reflect not only the mechanical response of the SE phase but also local porosity, particle packing, and surface condition"* (SI p.51).
3. 모형에 파괴 · 박리 없음: *"Explicit fracture and interfacial separation were not simulated."* (p.19) · *"indicators of mechanically vulnerable regions rather than … direct simulations of crack formation or delamination"* (SI p.61).
4. 2D 의 연결성: *"Because the highly interconnected Sn morphology cannot be fully represented in a two-dimensional cross section, the apparent connectivity … does not necessarily represent their actual three-dimensional electronic connectivity"* → 전자 수송은 빠르다고 가정 (SI p.58).
5. 실험 변수의 얽힘: D50 · PSD 폭 · 기공 *"change simultaneously in the experimentally compacted powders"* (p.13) · 3D 결과는 *"within the present model framework"* (p.14).
6. 계산 ↔ 실험 충전 비교는 *"qualitative"* (율 0.2C ↔ 0.1C · SI p.59).

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 · 계산 사슬
분말 셋 (상 · σ · PSD) → [순수 SE] 200 mg · ⌀13 mm PEEK · 110–440 MPa · 2 분 → 다이 안 마이크로미터 두께 5 점 → 기공 (TD 1.64) × 펠릿 5 → [440 MPa 펠릿] FIB-SEM 3D (45 nm) → 국소 기공 지도 · 공극 크기 → [110 · 330 · 440 MPa 펠릿 조각] in-SEM Berkovich 110 점 지도 → HI · 낮은 몫 · Moran's I → [전셀] 분리막 / 음극 SE 바꿔 넣기 (BD · SE-2 · ND) · 적층압 · 100 사이클 → 사후 cryo 단면 → [모형] FIB-SEM 단면 (음극) + 분리막 2D 단면 → COMSOL 2D 평면변형 단방향 FEM → 응력 지표 / GrainGeo 3D (같은 D50 · 같은 기공) → 3D 탄성 FEM 20 MPa → 고응력 부피 몫.
- **맞춘 값**: 없음 (모형은 측정 · 문헌 값을 넣기만) · 넣은 값 = SE E 33.13 GPa (BD Er) · ν 0.37 (DFT) · κ 측정값 · Sn · NCM 문헌값 (표 S2).
- **검증**: 첫 충전 곡선 정성 비교 (그림 S16) · 두 모형 리튬화 같음 (그림 S17) · 응력 지도 ↔ 사후 균열 위치의 '일치' (정성) — 응력 크기 · 균열 판정 검증 없음.

### 4-2. 입자 처리
- **실험** = 실제 분말 압분체 (순수 SE 펠릿 · 분리막) — 입자 모양 · 소성 · 파쇄는 *"Particle morphology, agglomeration, surface chemistry, particle fracture, and compaction history all influence how solid-electrolyte powders pack and consolidate"* (p.5) 로만 언급 · 측정 안 함.
- **2D 모형** = 분할된 연속체 (SE · 기공 · Sn) — **입자 경계 · 접촉 · 미끄럼 없음** (SE–SE 도 접합 · 변위 연속) · 기공만 자유 표면.  압밀 과정 없음 (누른 뒤 구조를 그대로 씀).
- **3D 모형** = GrainGeo 알갱이 배치 (기하 생성 · 동역학 · 압밀 없음) → 연속체로 합쳐 탄성 FEM — 알갱이 사이 접촉 · 경계 처리 [미확인].
- 우리 대응: DEM = 구 + hooke/hysteresis 접촉 (모양 불변 · 연화 E_eff 1.35 GPa · 접촉망 수송) · MPM = J2 연속체 (SE 형상 소성 · 기공 채움) — 이 논문 모형은 **둘 다 아닌 '누른 뒤 이미지 위 탄성 FE'** 다 (frame[5] 의 어느 반쪽도 계산하지 않는다 · 측정이 압밀 결과를 준다).

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말했나** — **말 없음.**  원문 66 쪽에 DEM · discrete element 0 회.  입자 계산 없이 **이미지 → 연속체 FE** 로 갔다.  관련 문장: 압분체는 *"residual pores, interparticle boundaries, locally constrained contacts, and load-bearing ligaments whose spatial arrangement emerges during powder consolidation"* 를 가진다 (p.4) — 그러나 그 배열을 만드는 계산 (DEM · MPM) 은 없다.
2. **소성 · 큰 변형을 넣기 어려운 이유 · 우회 · 비용** — 이유 서술 없음.  우회 = **누른 뒤의 실측 구조 (FIB-SEM) 를 그대로 기하로** 써서 압밀 계산을 건너뜀 · SE 는 **선형 탄성** (소성 · 크리프 없음) · 파괴 · 박리 없음 · 단방향 결합.  비용 (요소 수 · 시간) [미확인].  결과로 응력이 GPa 급 (§3-7) — SE 가 실제로는 흐르거나 깨질 크기 [카드 해석].
3. **2D 인가 3D 인가** — 전기화학–역학 모형 = **2D 평면변형** (그림 S14 *"Plane strain (2D)"* · SI p.54 *"two-dimensional digital twins"*) · 분리막 2D 단면은 3D 부피와 기공률이 같게 고름 · 3D = GrainGeo 역학만.  2D → 3D 경고 = Sn 연결성 문장 (SI p.58) 하나 — 응력장의 2D/3D 차이는 다루지 않았다.
4. **압력을 뺄 때의 거동** — **없음.**  펠릿 기공은 누른 뒤 다이 안 한 번 (가압 중 · 꺼낸 뒤 · 되돌아옴 없음) · 셀은 20 MPa 일정 체결 · 적층압 *변화* 는 운전 중 음극 팽창 · 수축의 결과 (그림 3a–b).  모형도 20 MPa 일정.

### 4-4. 기법 미니 용어집
- **BD / ND**: broad- / narrow-distribution — 이 원고의 이름 (SE-1 · SE-3).
- **FIB-SEM 단층 촬영**: 집속 이온빔으로 한 겹씩 깎으며 SEM 을 찍어 3D 를 쌓는 법 (여기 45 × 45 × 75 nm → 45 nm 등방 재표본화).
- **국소 기공 분율 지도**: 3D 분할 부피에서 x–y 마다 z 방향 기공 복셀 비율 → 2D 지도 · 평균 = 국소 기공 · 표준편차 = 공간 편차 (그림 S5).
- **HI (heterogeneity index)**: IQR / 중앙값 — 극값에 둔한 상대 산포.
- **Moran's I**: 이웃끼리 값이 닮은 정도 (양 = 뭉침 · 0 ≈ 무작위 · 음 = 엇갈림) · 여기 가중 = 상하좌우 이웃 1 · 행 표준화 안 함.
- **공통 (pooled) 문턱**: 두 집단을 모은 분포의 백분위 (P20 · P90 · P95) 를 같은 문턱으로 써 집단마다 넘는 몫을 비교 — 집단별 문턱의 함정 (각자 10 %) 을 피한다.
- **디지털 트윈 (여기 뜻)**: 실측 영상을 분할해 만든 FE 기하 (top-down) · 알갱이 생성기로 만든 기하 (bottom-up · GeoDict GrainGeo).
- **평면변형**: z 변형 0 인 2D 탄성 (ν 가 면외 응력을 만든다).
- **하중형 셀 (load-type cell case)**: 체결 하중을 로드셀로 읽어 운전 중 적층압 변화를 기록하는 셀.

---

## 5. Figure set ★
| 그림 (크롭 파일) | 내용 | 우리 활용 |
|---|---|---|
| Fig. 1 (`fig_1.png`) · 1a · 1b · 1c · 1f · 1i | (a) PSD 셋 (b) D10–D95 (c) 펠릿 기공 110–440 MPa (d–e) 440 MPa FIB-SEM 국소 기공 지도 BD · ND (0–30 %) (f) 펠릿 ↔ 국소 기공 (g–h) 3D 재구성 (눈금 15 µm) (i) 440 MPa Er · H | ★ 순수 SE 압력별 기공 (표 S1 숫자) · PSD 와 함께 등록할 꼴 · 국소 ↔ 평균 기공의 차 |
| Fig. 2 (`fig_2.png` 다시 자름) · 2a · 2b · 2c · 2h | (a–b) 110 · 440 MPa Er · H 바이올린 (c) HI_Er (d–g) 11 × 10 Er 지도 (h) 낮은 Er 몫 (인쇄 59.0 · 18.1 · 2.72 · 0) · Moran's I | ★ 공간 이질성 지표 (HI · 공통 문턱 · Moran's I) 를 우리 장 출력에 쓸 정의 |
| Fig. 3 (`fig_3.png`) | (a–b) ND-ND · BD-ND 전압 · 적층압 변화 (1.6–3.8 · 1.4–3.6 MPa) (c–e) 0.2C 전압 곡선 4 · 10 · 50 · 100 번째 (f) 사이클 · 쿨롱 효율 (g) 손실 31.5 · 18.5 %p | 흐름 밖 (전셀 열화) — '평균 하중이 같아도 국소가 다르다' 의 실험 근거 |
| Fig. 4 (`fig_4.png` 다시 자름) · 4f · 4g · 4h | (a–b) 사후 단면 (c) 디지털 트윈 기하 (d–e) von Mises (0–20 GPa) · 정수압 (−2…2 GPa) (f–g) 고응력 면적 몫 (h) 기공 거리별 응력 | 응력 집중 후처리 (공통 P90 · 거리 칸) 를 MPM 응력장에 그대로 |
| Fig. 5 (`fig_5.png`) · 5a · 5d · 5g | (a) 입력 PSD (보이는 곡선 하나 · D50 1.584 µm) (b–c) 좁은 · 넓은 3D 구조 (d) 공극 크기 (e–f) von Mises 0–80 MPa (g) 고응력 부피 몫 | ⚠ §3-9 판독 관찰 (5a · 5d) — 결론 문장만 저자 주장으로 · 숫자 인용 보류 |
| Fig. S1 (`fig_S1.png` 다시 자름) | XRD 셋 · Nyquist + σ 1.53 · 1.35 · 1.7 mS/cm | σ₀ 범위 감각 |
| Fig. S2 (`fig_S2.png` 다시 자름) | 다이째 마이크로미터 사진 | ★ '다이 안 · 하중 뺀 뒤' 측정의 실물 |
| Fig. S3 (`fig_S3.png`) · 식 둘 | 두께 · 밀도 · 기공 식 · TD 1.64 | ★ 기공 연산자 (단계 0) |
| Fig. S4 · S5 · S6 | 분할 (회색조 히스토그램) · 국소 기공 지도 만드는 법 · 공극 크기 분포 | 공극망 지표의 정의 |
| Fig. S7 (`fig_S7.png`) | 다이 · 막대 사진 · 비노출 홀더 · in-SEM 압입기 · 압흔 격자 SEM · ND Er 지도 | 측정 셋업 |
| Fig. S8 · S8a · S8f · S8g · S8h | H 쪽 지표 · Er/H vs 성형압 산점 + 인쇄 맞춤선 | ★ 국소 Er–성형압 선형 (ND Pc 0.985) |
| Fig. S9 · S9c | SE-2 끼운 셀 · 율속 | 흐름 밖 |
| Fig. S10–S13 | 균열 표시 · 3D → 2D 단면 · 2D 트윈 만드는 법 · 두 기하 | 기하 처리 절차 |
| Fig. S14 (`fig_S14.png`) · 식 둘 | 지배식 + 평면변형 [D] + 셀 기하 (음극 · 분리막 · 균질 양극) | ★ 모형 정의 (2D) |
| Fig. S15 (`fig_S15.png` 손 크롭) | Sn · NCM622 OCV | 입력 |
| Fig. S16–S21 | 첫 충전 비교 · LiₓSn 지도 · 복합 음극 SE 의 von Mises · 정수압 · 응력 히스토그램 (로그) · 거리 칸 설명 | 응력 분포 꼬리의 크기 감각 (GPa–100 GPa) |
| Table S1 (`tab_S1.png`) | ★ 기공 3 × 4 (평균 ± SD) | ★ 결과 전 대조 항목 |
| Table S2 (`tab_S2.png` 다시 자름 · 각주 포함) | 모형 입력 · E 33.13 각주 | 입력 · §3-9 ③ |
| 식 문단 14 장 (`eq_unnumbered_*`) | 그림 S3 (2) · 그림 S14 (2) · SI 노트 1 (2) · SI 노트 3 (8) | 보고서 식 절에 그대로 |
| 근거 문단 19 장 (`txt_p*`) | 게시 문구 · 기공 · 국소 기공 · 지표 · 적층압 · 유지율 · 트윈 · 파괴 없음 · 같은 D50 · 모형 범위 · 셀 조립 · 화성 · 다이 안 두께 · 압입 · 문턱 · FEM · GrainGeo · 결합 · 경계 | 인용 근거 (파일 이름의 pN = PDF 쪽) |

## 6. Post-processing ★
- **원문이 한 것**: 기공 = 질량 · 두께 · TD · 펠릿 5 개 평균 ± SD · FIB-SEM 분할 (watershed) → 국소 기공 지도 (z 투영) · 평균 · SD · 공극 크기 분포 (방법 [미확인]) · Oliver–Pharr (Er · H) · HI (IQR/중앙값) · 공통 P20 문턱 몫 · Moran's I (상하좌우 이웃) · Pearson (성형압 ↔ Er · H) · 전기화학 (Sn 질량 용량 · 유지율 · 손실 %p) · 응력 = σ_vM · σ_h · 공통 P90 · P95 면적 / 부피 몫 · 기공 경계 거리 칸 평균 · P95.  도구 = COMSOL 6.3 · GeoDict · (영상 처리 · 통계 도구 이름 [미확인]).
- **이 카드의 후처리**: 원본 래스터 (그림 1 xref 49 · 2 xref 44 · 4 xref 29 · 5 xref 46 · S6 xref 47 · S8 xref 35 · S9 xref 43 · 그림 S16 은 300 dpi 크롭) 에서 눈금 화소로 축을 잡고 표지 고리 · 막대 끝 · 곡선을 읽음 (`digitized.csv` 123 행) · 낮은 몫 × 110 = 자리 수 (88 = 20 % × 440) · P90/P95 평균 검산 · 면적 용량 · N/P 검산 · 두께 역산 · 300 MPa 보간 · Heckel · 그림 5a ↔ 1a · 5d ↔ S6 곡선 대조 · 그림 1i ↔ 표 S2 대조.  스크립트 = 대피 세션 scratchpad (`digitize_all.py` · `poreps2.py` · `curvecmp.py`) — 결과는 `digitized.csv` 에 남겼다.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| SE 재료 | 상용 argyrodite 셋 (Li₆PS₅Cl 로 가정 · 화학식 [미확인]) · PSD 셋 (D50 ≈1.6–9.9 µm [판독]) | Li₆PS₅Cl (DEM SE 생산 기본 r_SE 0.5 µm = ⌀1.0 · 코퍼스 r_SE 대부분 0.5–1.5 µm — CLAUDE.md) | 같은 계 · PSD 다름 |
| 진밀도 분모 | **1.64 g/cm³** (Li₆PS₅Cl 가정 · 출처 인용 없음) | 랩 표준 **1.64 g/cm³** (CLAUDE.md 1저자 11-10 Q5 · 고정) | **같은 수** — 판정하지 않는다 |
| 순수 SE 기공 · 측정 상태 | 다이 안 · 하중 뺀 뒤 (사진) · 110–440 MPa · 2 분 | 랩 표준 **10–13 %** (고정) · ps45 실험 = *"다이 안 · 하중 제거 후"* (`comparison_vs_ours_DEM.md` A 절 [Miss26] 블록) | 같은 상태 이름 · **랩 표준과 다른 문헌 값** (PSD 가 다르다): 300 MPa 보간 ND ≈10.7–11.1 · SE-2 ≈9.3–9.6 · BD ≈5.6–5.7 % [카드 산술] |
| Heckel | P_y ≈164 (BD) · 187 · 241 MPa (ND) [카드 산술 · 누른 뒤 밀도] | DEM 순수 SE P_y **138 MPa** (R² 0.965 · E 1.35 · 가압 중) | 다른 양 (누른 뒤 ↔ 가압 중 · 실물 ↔ 연화 DEM) — 크기 감각만 |
| SE 탄성 | 국소 Er 110 MPa ≈10–14 → 440 MPa ≈31–38 GPa [판독] · FEM 입력 E 33.13 (BD Er 를 영률로) · ν 0.37 | DFT E_VRH **22.06 GPa** (ν 0.360) · DEM **E_eff 1.35 GPa** · MPM **1.53 GPa** (ν 0.49 · K 25.5) | 압입 Er 은 다공 표면 국소 값 · (1 − ν²) 로 환산하면 E ≈0.86 Er [카드 산술] · DEM/MPM 연화값은 재배열 대리 (frame [2]) — 같은 층이 아니다 · [우리 산술] 33.13 / 1.53 = 21.7 배 |
| SE 강도 | 압입 H 440 MPa ≈2.2 (BD) · ≈2.7 GPa (ND) [판독] · 모형은 항복 없음 | MPM σ_y **0.30 GPa** (Hencky 문턱 · 일축 환산 0.32–0.45) · DEM σ_y_eff 46 MPa | 그 FEM 응력 (평균 2–4 · P95 ≤12.7 GPa [판독]) 은 우리 MPM 이면 σ_y 에 잘린다 — 크기 비교 금지 |
| 접촉 · 계면 | 모든 고체 계면 **접합** · SE–SE 도 연속 · 기공 자유 표면 | DEM 점접촉 · 분리 가능 / MPM 한 속도장 (A′-0 = 미끄럼 · 분리 부품 계획) | 실험은 계면 박리를 보였는데 모형은 못 낸다 — 우리 A′-0 의 동기와 같은 빈칸 |
| 차원 | 2D 평면변형 (음극 + 분리막) · 3D (GrainGeo 역학) | DEM 3D · MPM 2D/3D | 2D → 3D 응력 전이 근거 없음 |
| 압밀 과정 | 계산 안 함 (누른 뒤 영상) | DEM · MPM 이 압밀을 계산 | 이 논문은 압밀 결과 (기공 · 구조) 를 **측정으로** 준다 — 우리 계산의 결과 전 대조 자료 |
| 공극망 균일성 | 국소 기공 지도 SD · 공극 크기 · Moran's I · HI | 없음 (우리는 ε 하나 · 퍼콜레이션 · 피복) | 우리가 못 하는 지표 (§7-4 · §9) |
| 수송 | σ_ion 1.35–1.7 mS/cm (440 MPa · 30 °C) | 보고 기준 σ₀ **1.5 mS/cm** (CLAUDE.md 10-12) | 같은 범위 — 판정 없음 |

### 7-2. ★ 순수 LPSCl 계 펠릿의 압력별 기공 — 정본 카드와 나란히 (재료 · 분모 · 측정 상태 칸을 꼭 본다 · 판정 없음 · 기존 카드는 고치지 않는다)
| 카드 | 분말 | 다이 · 시료 | 측정 상태 | 진밀도 분모 | 값 |
|---|---|---|---|---|---|
| **이 논문** | 상용 argyrodite × 3 (D50 ≈1.6 · 1.2–1.4 · 9.9 µm [판독]) | PEEK ⌀13 mm · 200 mg · 2 분 | **다이 안 · 하중 뺀 뒤** (마이크로미터) | **1.64** | 220 / 330 MPa: ND 15.82 / 9.28 · SE-2 13.84 / 8.04 · BD 7.88 / 4.94 % · 440 MPa 6.19 · 3.69 · 1.73 % |
| `var2026_sulfide_se_mechanical_properties_local_indentation_pellet` | Li₆PS₅Cl ~10 µm | 스테인리스 컵 ⌀13 mm · 200 mg | 다이 안 · 하중 뺀 뒤 (캘리퍼) | 1.87 (랩 표준과 다른 값) | 상대밀도 0.68 · 0.73 · 0.78 @ 100 · 220 · 400 MPa (그 카드 L21) |
| `lee2025_heckel_argyrodite_powder_densification_nanoindentation` | 상용 Li₆PS₅Cl | (그 카드) | **가압 중** (하중 아래) | 1.64 | 300 MPa ≈15 % (그 카드 L25 · 판독) |
| `korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens` | 상용 LPSCl (응집체) | ⌀7.0 mm [그 카드 산술] · in situ XCT | **가압 중** | (그 카드: 진밀도 숫자 없음) | 12.12 → 8.61 % (76.2 → 510 MPa) · 300 MPa 보간 9.96 % (그 카드 L25 · 한정어 다수) |
| `miss2026_insitu_conductivity_porosity_pressure_compaction` | µc-Li₅.₅PS₄.₅Cl₁.₅ | 다이 (피스톤 압축 보정) | 가압 중 / 다이 안 놓은 뒤 | 1.87 (결정밀도 · 랩 표준과 다른 값) | 300 MPa 7.1–7.6 / 8.6 % (재계산 · 본문 미인쇄 — `comparison_vs_ours_DEM.md` A 절 [Miss26]) |
| 우리 랩 표준 | (랩 분말 · PSD 는 이 표에 없음) | — | 다이 안 · 하중 제거 후 (ps45 실험 표기) | 1.64 | **10–13 %** (고정 · 판정 대상 아님) |

- 같은 분모 · 같은 다이 크기 · 같은 질량이어도 **분말 PSD 만으로** 같은 압력의 기공이 2–4 배 갈린다 (이 논문) → 랩 표준 10–13 % 를 MPM 단계 4 의 표적으로 쓸 때 **그 분말의 PSD (D10 · D50 · D90) 를 같이 등록** 해야 문헌 값과 견줄 수 있다 [카드 해석].

### 7-3. 이 논문 값이 우리 계에 들어오는 길
1. **단계 4 결과 전 대조 (순수 SE)** — 표 S1 을 PSD 꼬리표와 함께 (ND 가 우리 DEM SE 크기 1.0 µm 에 가장 가깝다 [카드 해석 · D50 ≈1.6 µm]).
2. **공극망 균일성 지표** — 우리 DEM · MPM 침대에서 같은 정의 (z 투영 국소 기공 지도 · SD · Moran's I · 공통 문턱) 로 계산하면 실측 (BD ≈±4.4 · ND ≈±1.6 %p) 과 견줄 수 있다 (해상도 · 시야 · 분할 차이 꼬리표).
3. **응력 후처리** — 공통 P90/P95 몫 · 기공 경계 거리 칸 통계를 우리 MPM σ 장에 그대로.

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 압밀 **결과** 의 실측 (기공 · 3D 공극망 · 국소 기계 지도) 과, 그 위의 탄성 응력 집중 (2D/3D) — 우리 DEM (패킹 · PSD · 공극 배치) 과 MPM (형상 · 응력장) 양쪽의 **결과 전 대조 자료**.
- **없는 것**: 압밀을 계산하는 모형 (DEM · MPM) · 소성 · 파괴 · 계면 분리 · 탈압 · 접촉망 수송.  ⇒ 이 논문은 "PSD → 공극망" 을 **측정으로** 보이고 "공극망 → 응력" 을 **탄성으로** 보인다 — "PSD → 공극망" 을 **계산** 하는 것은 우리 DEM 의 몫 (Furnas 류 패킹), "공극망 → 응력 · 소성 흐름" 은 MPM 의 몫.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = 상용 argyrodite (Li₆PS₅Cl 로 가정) — 같은 계 · 다른 PSD.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ ① **같은 연산자의 실물**: ε = 1 − m/(π r² t · 1.64) · t = 다이 안 5 점 평균 · 하중 뺀 뒤 — 랩 표준과 같은 분모 · 같은 상태 → 등록 칸 = {분말 PSD (D10/50/90) · 질량 · 다이 지름 · 압력 · 유지 시간 · 측정 상태 (가압 중 / 다이 안 뺀 뒤 / 꺼낸 뒤) · 두께 기구 · 펠릿 수} ② **국소 ↔ 평균 기공을 섞지 않는다** — FIB-SEM 국소 8.129 % ↔ 펠릿 1.73 % (BD · 4.7 배) · 저자 경고 (p.7) ③ **공통 문턱 (pooled 백분위) 비교** 를 결과 전에 정해 두는 꼴 (P20 · P90 · P95) | 가압 중 두께 · 되돌아옴 · 분말 실제 밀도 · 두께 조건별 값 |
| **단계 1** (3D 메모리 · 장 수) | 없음 | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 기공 둘레 응력 집중의 해석 원전 목록 (Inglis 1913 [27] · Davis 2017 [31] — 카드 없음) → 소성 전 탄성 한계에서 MPM 이 구멍 둘레 집중 (원형 구멍 3 배 류) 을 내는지 시험할 근거 [카드 해석] | 이 논문의 FE 해상도 · 수렴 정보 없음 |
| **단계 3** (2D 접촉 표현 비교) | 없음 (접합 연속체뿐) | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | ★ 표 S1 — argyrodite 순수 SE 의 4 압력 × 3 PSD 기공 (같은 분모) · 300 MPa 보간 ND ≈10.7–11.1 % [카드 산술] · **PSD 감도** (같은 압력 2–4 배) → σ_y 맞춤 표적 (랩 표준 10–13 %) 은 **그 분말의 PSD 와 짝** 이어야 한다 · Heckel P_y 164–241 MPa [카드 산술] · 국소 Er 이 성형압에 선형 (ND Pc 0.985) | 맞춤 표적은 랩 표준 (이 값은 '랩 표준과 다른 문헌 값') · 가압 중 값 없음 · 분말 밀도 미측정 |
| **단계 5** (3D 복합 압밀) | 없음 (복합 양극 65 : 30 : 5 를 220 MPa 로 눌렀다는 공정만 · 기공 없음) | 복합 기공 · 하중 몫 |
| **단계 6** (탈압 · 되돌아옴) | 없음 — 측정이 '다이 안 · 뺀 뒤' 한 상태라 되돌아옴이 값 안에 섞여 있다 (가를 수 없음) | 회복량 · 가압 중 두께 |
| **단계 7** (형상 · 피복 · 수송) | ★ 공극망 지표 (국소 기공 지도 SD · 공극 크기 분포 · Moran's I · HI) 를 우리 침대 출력에 더할 정의 · σ_ion 1.35–1.7 mS/cm (440 MPa · 30 °C) = 보고 기준 σ₀ 1.5 와 같은 범위 | 망 σ · tortuosity · 피복 없음 · 공극망 → σ 연결 없음 |
| **후보 D0** (지금 DEM) | 넓은 PSD 가 작은 입자로 큰 입자 사이를 채워 치밀해진다 (저자 해석) = **DEM 이 소유한 기하 패킹 효과** (Furnas) 의 실측 쪽 · 그러나 공극이 뭉쳐 남는다 → DEM 침대에서 PSD 폭별 '공극 뭉침' 을 지표로 낼 수 있다 (흐름 밖: 50 kg SE 입도 설계) · BD 1.73 % (440 MPa) 는 단단한 구 바닥 (~20 %) 아래 — 소성 흐름 없이는 못 간다 (frame [1] · [2] 와 같은 결론) | 이 논문은 DEM 을 쓰지 않았다 — 연화 E_eff 를 정당화 · 반박할 숫자 아님 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 반면교사: 모형이 **모든 계면을 접합** 해 실험에서 본 **음극–분리막 계면 박리** 를 못 낸다 → 분리 가능한 접촉 부품의 필요 (원문은 이 한계를 스스로 적음 · SI p.61) | 박리 기준 · 점착 값 없음 |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | 없음 (Sn 은 강체가 아니라 팽창하는 탄성체) · 다만 '같은 평균 하중 · 다른 국소 응력' 이 공극 배치에서 나온다는 증거 → 입자별 장이 없어도 **공극 기하 해상도** 가 응력 꼬리를 정한다 [카드 해석] | 소성 · 접촉 |
| **후보 B** (입자별 FE + 접촉) | 이미지 기반 연속체 FE 의 선례 (접촉 없음 · 접합) — MPFEM 과 다른 쪽: 입자 경계 · 미끄럼 없이도 국소 응력 꼬리를 본다 | 계산 비용 · 요소 수 · 수렴 [미확인] |
| **후보 C · C′** (큰 변형 · 항복 캡 접촉 DEM) | 없음 · 국소 H (440 MPa ≈2.2–2.7 GPa [판독]) 는 다공 펠릿 표면값이라 접촉 캡으로 바로 쓰지 않는다 | — |
| **후보 M0** (균질화 압밀 · Heckel) | ★ 표 S1 → PSD 별 Heckel (P_y 164 · 187 · 241 MPa · R² 0.964–0.997 [카드 산술]) — M0 맞춤 자료 (PSD 꼬리표 · '누른 뒤' 꼬리표) | 가압 중 곡선 · 압력 점 4 개뿐 |
| **U0–U6** | **U6** (작은 조밀 충전 압축의 해상도 수렴): GrainGeo 복셀 0.2 µm · D50 ≈8 칸 · 공극 봉우리 0.3 µm = **1.5 칸** → 공극 둘레 응력 꼬리는 미해상 (우리 규칙 d_h/dx ≳ 3.5 와 견줄 반례) · FIB-SEM 45 nm 에서 0–0.1 µm 거리 칸 = ≈2 칸 | U0–U5 없음 |
| **R1–R7** | **R2** (미끄럼 · 분리): 실험 = 계면 박리 · 모형 = 접합 → 필요성의 실례 · **R6** (SE 형상 변형): BD 가 440 MPa 에서 1.73 % 까지 치밀 = 작은 입자 채움 + 소성 (원문은 기전을 가르지 않음) · **R5** (맞추는 값 하나): 이 모형은 맞춘 값이 없다 (측정 · 문헌 값만 넣음) — 두 분리막에 같은 E (BD Er) 하나를 넣어 강성 차를 지웠다 · SE 균열 (R 목록 밖 · R7 = AM 파괴) | R1 · R3 · R4 · R7 없음 |
| **결과 전 대조 항목** | ① 표 S1 (PSD · TD 1.64 · 다이 안 뺀 뒤 · 2 분 · 200 mg · ⌀13 mm · n 5 꼬리표) ② FIB-SEM 국소 기공 8.129 · 6.752 % + 공간 SD ≈4.4 · 1.6 %p [판독] ③ HI_Er · 낮은 Er 몫 · Moran's I (440 MPa) ④ 국소 Er/H vs 성형압 맞춤선 (그림 S8g–h 인쇄) — **맞추는 데 쓰지 않음** | 원고 (심사 전) · 펠릿 하나 · 그림 5 의 판독 관찰 |

- **재료 · 차원 · 조건 차이**: 같은 argyrodite 계 (조성 [미확인]) · 분말 PSD 다름 · 순수 SE 펠릿 (복합 양극 아님) · 2D 평면변형 탄성 (우리 MPM = 소성) · 하중 = Sn 음극 팽창 + 20 MPa (우리 = 300 MPa 판 압축) · 30 °C.

## 9. 적용 인사이트 (행동)
1. **랩 표준 기공 (10–13 %) 옆에 분말 PSD 를 적는다 (단계 0 · 4)** — 같은 분모 1.64 · 같은 '다이 안 · 뺀 뒤' 상태에서 PSD 만 바꿔도 440 MPa 기공이 1.73 ↔ 6.19 %, 110 MPa 13.78 ↔ 23.75 % (표 S1).  MPM σ_y 맞춤 표적의 꼬리표 = {분말 · D10/50/90 · 다이 · 질량 · 유지 시간 · 측정 상태}.
2. **공극망 균일성 지표를 우리 침대 출력에 더한다 (단계 7 · 흐름 밖: SE 입도 설계)** — z 투영 국소 기공 지도의 평균 · SD · Moran's I (상하좌우 이웃 · 행 표준화 없음) 와 공극 크기 분포.  ε 하나로는 BD (1.73 %) 가 '가장 좋은' 분리막으로 보이지만 국소로는 가장 나쁘다 (8.129 % · ±4.4 %p).
3. **응력장 비교는 공통 (pooled) 문턱으로 (단계 7 · MPM 후처리)** — 두 조건의 분포를 모아 P90 · P95 를 잡고 넘는 몫을 비교 · 기공 경계 거리 칸 (0–0.1 · 0.1–0.3 · 0.3–0.5 µm) 평균 · P95.  검산 = 몫의 평균이 10 · 5 % 근처 (면적 같을 때).
4. **이미지 기반 탄성 응력의 크기를 믿지 않는다 (단계 2 · 7)** — 접합 · 선형 탄성 · 2D 에서 SE von Mises P95 가 12.7 GPa · 히스토그램 꼬리 ~100 GPa 까지 (SE 압입 경도 ≈2–3 GPa 의 수 배–수십 배) → 상대 비교만 · 소성 (우리 MPM σ_y 0.30) 이 들어가면 꼬리가 잘린다.
5. **그림 5 (같은 D50 · 같은 기공 3D) 는 인용 보류 (출처 확인 전)** — 5a 에 좁은 PSD 곡선 없음 · 5d ≈ S6 (§3-9) · 결론 문장 (*"within the present model framework"*) 만 저자 주장으로.
6. **'평균 하중이 같아도 국소가 다르다' 를 적층압 해석의 주석으로 (흐름 밖: 셀 열화)** — 적층압 변동 1.4–3.6 ↔ 1.6–3.8 MPa 로 비슷한데 유지율 63.1 ↔ 94.6 %.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Uniaxially cold-pressed (2 min, 200 mg, Ø13 mm PEEK die) commercial argyrodite separators reached bulk porosities of 13.78 → 1.73 % (broad PSD) and 23.75 → 6.19 % (narrow PSD) from 110 to 440 MPa, measured from in-mold micrometer thickness with a Li6PS5Cl theoretical density of 1.64 g cm−3 (Cho et al., ChemRxiv 2026, preprint, Table S1)."
- "Despite its lower bulk porosity (1.73 %), the broad-PSD pellet showed a FIB-SEM local porosity of 8.129 % with clustered pore-rich regions, versus 6.752 % for the narrow-PSD pellet (6.19 % bulk) (Cho et al., ChemRxiv 2026, preprint)."
- 국문 (한정어와 함께): *"분말 입도 분포가 넓으면 펠릿은 더 치밀해도 (440 MPa 1.73 %) 공극이 뭉쳐 남고 국소 탄성률이 넓게 흩어진다 — 평균 기공 하나로 분리막의 기계 상태를 말할 수 없다 (Cho 2026 · ChemRxiv 원고 · 동료 심사 전)."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계** — §3-10 의 여섯 (국소 ≠ 평균 기공 · 압입 = 국소 유효값 · 파괴 · 박리 없음 · 2D 연결성 · 변수 얽힘 · 정성 비교).

**카드가 본 한계 · 원문 안 어긋남**
1. **동료 심사 전 원고** (v2) — 값 · 그림이 바뀔 수 있다.
2. **분말 조성 · 진밀도 미측정** — 1.64 는 Li₆PS₅Cl 가정 (출처 없음) · 분말마다 다를 수 있는 할로젠 비 · 불순물이 분모를 바꾼다.
3. **나노압입 지도 = 조건마다 펠릿 하나** — 지도 안 110 점은 공간 표본이지 펠릿 간 반복이 아니다 · Moran's I 유의성 없음.
4. **D50 · PSD 폭 · 기공이 함께 바뀐 비교** (BD D50 ≈9.9 ↔ ND ≈1.6 µm [판독]) — 전셀 · 지도 · 응력 차이를 'PSD 폭' 하나로 돌릴 수 없다 (저자도 p.13 인정) · 그 분리를 맡은 그림 5 는 판독 관찰 (§3-9 ①②) 로 입력이 [미확인].
5. **모형 E 값 (33.13) ↔ 그림 1i (≈31.0 [판독])** 어긋남 · 두 분리막에 같은 E — 측정된 ND 의 더 높은 Er (≈38.4) 은 쓰지 않았다 (강성 차를 지우고 기하만 남긴 설계 — 결론은 '기하 효과' 로 한정해야 한다 [카드 해석]).
6. **응력 크기는 물리적이지 않다** — 선형 탄성 · 접합 · 2D 평면변형 · 날카로운 기공 모서리 → 평균 2–4 GPa · P95 ≤12.7 GPa · 꼬리 ~100 GPa [판독] · 균열 판정 기준 (K_IC · G_c) 과 잇지 않았다.
7. **사후 균열 정량 없음** — 단면 몇 장 · 면적 몫 · 시편 수 없음.
8. **전셀 하나씩** (셀 반복 수 · 오차 막대 [미확인]) · Sn 음극 · 20 MPa · 30 °C 한 조건.
9. **전이 한계**: 같은 argyrodite 계지만 분말 PSD · 공급처가 다르다 · 순수 SE 펠릿 (복합 양극 아님) · 이 응력은 음극 팽창 하중 (우리 300 MPa 압밀과 다른 하중).

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄 · 정본 카드 없음 확인 = papers/ 목록 + 제목 · 저자 grep, 2026-11-23)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| [38] | Diallo, M. S. et al. Effect of solid-electrolyte pellet density on failure of solid-state batteries. Nat. Commun. 15, 858 (2024). | ★ 펠릿 밀도 ↔ 전지 파괴 (제목) — 이 원고 p.5 가 '넓은 PSD = 치밀 · 저항 낮춤' (refs 34 · 37 · 38) 과 '뭉친 공극 · 고르지 않은 하중 길' (refs 34 · 38) 의 근거로 인용 · 정본은 faka2026 · miss2026 이 이름만 언급 · 카드 없음 |
| [35] | Li, J. et al. Processing-structure-property relationships in practical thin solid-electrolyte separators for all-solid-state batteries. J. Phys. Energy 6, 025023 (2024). | ★ 얇은 SE 분리막의 공정–구조–물성 — 같은 축 · 카드 없음 |
| [11] | Han, S. Y. et al. Stress evolution during cycling of alloy-anode solid-state batteries. Joule 5, 2450–2465 (2021). | 합금 음극 적층압 변화 (이 원고의 하중 원천) · 카드 없음 |
| [28] | Sammis, C. G. & Ashby, M. F. The failure of brittle porous solids under compressive stress states. Acta Metall. 34, 511–526 (1986). | 다공 취성체의 압축 파괴 — 공극 ↔ 균열 기전의 고전 · 카드 없음 |
| [37] | Park, C. et al. Electrochemical Properties of Composite Cathode Using Bimodal Sized Electrolyte for All-Solid-State Batteries. J. Electrochem. Soc. 166, A5318–A5322 (2019). | 두 봉우리 SE 입도 (BD 와 같은 꼴) — 정본 cronau2022 · kawaguchi2023 · park2020 이 인용만 · 카드 없음 |
| [26] | Dixit, M. et al. Differences in the Interfacial Mechanical Properties of Thiophosphate and Argyrodite Solid Electrolytes and Their Composites. ACS Appl. Mater. Interfaces 14, 44292–44302 (2022). | 계면 역학 물성 (점착 · 박리) — 정본 kang2026 이 인용만 · 카드 없음 |
| [27] · [31] | Inglis 1913 (Trans. Inst. Nav. Archit. 55, 219–230) · Davis, Healy, Bubeck, Walker 2017 (J. Struct. Geol. 102, 193–207) | 구멍 둘레 응력 집중의 해석 · 3D 공극 응력 — 단위 시험 원전 · 카드 없음 |
| [SI 2] · [SI 3] | Park, C. et al. Nat. Commun. 16, 8838 (2025) · Lee, D. et al. Joule 9, 102046 (2025) | 같은 그룹의 FIB-SEM 절차 · 전기화학–역학 모형 (표 S2 값) · 카드 없음 |

## 13. [미확인] 목록 (66 쪽 전수에 없음)
1. 분말 화학식 · 할로젠 비 · 비중병 (실제) 밀도 · TD 1.64 의 출처.
2. 펠릿 두께 조건별 값 · 다이 안 측정에서 막대 길이 처리 · 영점 · 남은 하중 · 누름 속도 · 온도.
3. PSD 측정 분산 조건 · 분말 모양 · 응집 — Methods 는 분말 모양을 SEM 으로 보았다고 적지만 (p.17) 그 그림이 없다.
4. 공극 크기 분포 계산법 (FIB-SEM · GrainGeo) · 분할 문턱 · 국소 기공 지도의 z 깊이 (부피 전체인지).
5. 나노압입 면 (연마 여부) · 면적 함수 보정 값 · 열 표류 · 하중–깊이 곡선 · 펠릿 간 반복 · Moran's I 유의성.
6. FEM 격자 · 요소 수 · 풀이 설정 · 계산 시간 · β_Sn–γ_V 관계식 ('¿') · γ_V 값.
7. GrainGeo 두 입력 PSD 의 숫자 · 알갱이 모양 · 겹침 · 기공 6.752 % 를 맞춘 법 · 3D 재료 값 · 경계 조건 · 그림 5a 의 좁은 PSD 곡선 · 그림 5d 와 S6 의 관계.
8. 표 S2 의 E 33.13 GPa 가 그림 1i 어느 값인지 (판독 ≈31.0).
9. 전셀 반복 수 · 오차 · 사후 균열 정량.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-23)
- PDF 66 쪽 전부 글자 층 추출 + 그림 · 표 · 식 · 캡션 쪽 렌더로 읽음.  서지 = p.1 (ChemRxiv 표지 · 게시 문구 · DOI) · p.2 (저자 · 소속 · 공동 1저자 · 교신) · p.20–21 (연구비 · 기여 · 이해 충돌) · PDF 꼬리 정보.  원문 낱말 셈: DEM · discrete element · MPM = 0 · plastic(ity) = 0 · Heckel = 0 · springback · unloading (펠릿) = 0.
- 그림 크롭 **81 장** = 도구 27 (그림 1–5 · S1–S14 · S16–S21 · 표 S1–S2) 가운데 **다시 자름 5** (fig_2 = 그림 1 캡션 끝줄 섞임 · fig_4 = 도구가 그림 5 래스터를 잘랐다 (p.28 의 그림 4 래스터로) · fig_S1 = 캡션 끝 · 'Supplementary Materials' 섞임 · fig_S2 = 사진 래스터가 쪽 위로 넘침 · tab_S2 = 각주 잘림) + 손 54 (그림 S15 = 래스터가 앞 쪽 p.43 · 패널 20 · 식 문단 14 (원문 식 번호 없음) · 근거 문단 19).  81 장 전부 열어 확인 (패널 · 식 · 글 크롭은 겹쳐 쌓은 확인 그림으로).  손 크롭 넷은 한 번 더 렌더 (fig_2h · fig_S8f = 오른 축 글자 잘림 · fig_4g · fig_4h · fig_5a · fig_5d = 이웃 패널 글자 · 축 끝).
- 판독: 원본 래스터 7 개 (+ 그림 S16 크롭) 에서 눈금 화소 탐색으로 축 → 표지 · 막대 · 곡선 (`digitized.csv` 123 행) · 인쇄 숫자와의 검산 (낮은 몫 자리 수 88 · P90/P95 평균 · 그림 1f 펠릿 1.73 판독 1.732).
- 중복 확인: `litdb/papers/` 목록 + DOI (15009882) · 제목 ('pore-network homogeneity' · 'mechanically reliable') · 저자 (Hyeok-Rae · Hyeong-Jong) grep — 카드 없음 · 같은 성 · 같은 해 `cho2026_eipc_zn_anode_azib` 은 **다른 사람** (Yanghyun Cho · 수계 Zn) 이라 '관련 카드' 짝을 걸지 않았다.

## 🔗 관련 카드
- SE 입도 · PSD 폭 축: `yano2026_se_psd_width_ionic_tortuosity_dem` · `schlautmann2023_se_particle_size_composite_transport` · `faka2026_particle_size_consolidation_strain_lpscl` · `jeong2024_operando_densification_chemomechanics_se_size_composite_cathode` · `koenig2023_wet_milling_se_ion_tortuosity_composite_cathode`.
- 순수 LPSCl 압밀 · 기공 · 측정 상태: `var2026_sulfide_se_mechanical_properties_local_indentation_pellet` · `lee2025_heckel_argyrodite_powder_densification_nanoindentation` · `korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens` · `miss2026_insitu_conductivity_porosity_pressure_compaction` · `doux2020_pressure_effects_sulfide_se_jmca`.
- 황화물 SE 나노압입: `papakyriakou2021_mechanical_behavior_inorganic_li_solid_electrolytes_nanoindentation` · `mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation` · `torii2025_lpscl_mechanical_anisotropy_dft` (ν 0.37 원전).
- 이미지 기반 전기화학–역학 응력: `benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode` · `park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics` · `kim2023_chemomech_failure_highstrain_anode` (Kang · Shin · 고변형 음극) · `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` · `doux2020_stack_pressure_assb`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
