<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     꼴 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md (같은 그룹 · 이 논문 ref [19] · 셀과 σ 상승 기전의 앞 논문) ·
     짝 = ohashi2020_stress_distribution_composite_electrode_sulfide_assb.md (같은 그룹 · 이 논문 ref [17] · LGPS + ZrO₂ 복셀 FEM 의 앞 판) ·
     곁 = sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps.md (이 논문을 ref 25 로 인용 · 고른 의도의 출처).
     쪽 표기 = 학술지 논문 번호 229212 의 쪽 p.1–7 (PDF 쪽 = 인쇄 쪽).  보충 자료 (SI) 는 원문에 안내가 없다 (본문 7 쪽 텍스트 층 전수에 'supplementary' 0 회).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv · 그림 4 · 5 · 6 은 벡터 경로의
     좌표 그대로 (틀 사각형 + 눈금 글자 위치로 환산 · 로그축 '1' 이 틀 한가운데 0.02 pt 안) · 그림 8 은 300 dpi 원 래스터의 색 원판 무게중심을 눈금선 위치에 조각선형으로 —
     점선 '400 MPa' 가 398.9 / 400.0 으로 읽힘) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 추론] · [카드 해석] = 이 카드의 해석 ·
     [다른 카드] = 정본의 다른 카드에 적힌 값 (slug 병기) · [우리] = 우리 쪽 값 (CLAUDE.md 출처) · [미확인] = 원문 (본문 7 쪽 전수) 에 없음.
     원문 7 쪽은 전부 렌더 이미지로 읽었고 숫자는 텍스트 층 (PyMuPDF 1.28.2) 과 대조했다. -->
# 활물질 영률이 황화물 SE 의 이온 수송 · 포화 압력을 바꾼다 — Li₅.₅PS₄.₅Br₁.₅ + 지르코니아 (200 GPa · 단단한 활물질 대리) / 나일론 (2 GPa · 무른 활물질 대리) 모형 복합체를 0 → ≈400 MPa 누른 채 EIS · 400 MPa 누른 채 X 선 CT (복셀 5 × 5 × 6 µm) → 선형 탄성 복셀 FEM (VOXELCON · GPU · ≈300³ · 결합 연속체) · 포화 압력 나일론 ≈250 < 순수 SE ≈300 < 지르코니아 22 % ≈350 · 39 / 52 % > 400 MPa [인쇄] · 400 MPa 에서 SE 평균 MPS 291 → 196 · 지르코니아 815 → 598 MPa (22 → 52 vol%) [판독] → 지르코니아 축하중 몫 0.43–0.45 → 0.77–0.78 [카드 산술 · 평균 응력 정리] · 이온 수송 계산 · 기공 · 탈압 없음 — Ohashi · Kodama · Horikawa · Hirai (J. Power Sources 2021)

> slug `ohashi2021_am_youngs_modulus_ion_transport_voxel_fem_ct` · DOI `10.1016/j.jpowsour.2020.229212` · type `experiment + image-based voxel FEM (linear-elastic stress, VOXELCON GPU, bonded continuum) — Li5.5PS4.5Br1.5 + zirconia / nylon (AM stand-ins, 200 / 2 GPa) model composites, EIS sigma_ion(P) 0-400 MPa (pressurized, loading only) + X-ray CT at 400 MPa · no ion-transport simulation · no DEM / MPM / contact law / plasticity / unloading` · PDF `Effect_of_Youngs_modulus_of_active_materials_on_ion_transport_through_solid_electrolyte_in_all-solid-state_lithium-ion_battery.pdf` · digested `2026-11-17` · status ✅
>
> **저자**: A. Ohashi · **M. Kodama\*** (교신) · N. Horikawa · S. Hirai — Tokyo Institute of Technology (NE-8 2-12-1 Meguro, Tokyo, 152-8550) · 원문은 이니셜만 (이름 전체 [미확인] — 같은 그룹 2020 카드는 그 논문에서 Akinari Ohashi · Manabu Kodama 를 읽었다 [다른 카드 `ohashi2020_…`]) · *J. Power Sources* **483** (2021) **229212** (본문 7 쪽 · SI 안내 없음) · 접수 2020-09-15 · 수정 11-05 · 승인 11-09 · 온라인 11-18 · 연구비 Japan Keirin Autorace Foundation (일부) · *"We thank Quint Corporation for the support with the voxel-based FEM stress analysis"* (p.7) · 기여: Ohashi = 방법 · 소프트웨어 · 초고 / Kodama = 개념 · 소프트웨어 · 검토 · 편집 · 연구비 / Horikawa = 검증 · 방법 / Hirai = 과제 관리 (p.7) · 키워드 다섯: Sulfide all-solid-state lithium-ion battery · X-ray computed tomography · Stress analysis · Saturation pressure · Young's modulus (p.1).
> **이웃 카드 (링크만)**: [`ohashi2020_stress_distribution_composite_electrode_sulfide_assb`](ohashi2020_stress_distribution_composite_electrode_sulfide_assb.md) (이 논문 [17] · 같은 그룹 앞 논문 · LGPS + ZrO₂ 100 MPa · 응력 → 국소 σ 계산까지 한 판 · §3-10 나란히) · [`kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation`](kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md) (이 논문 [19] · *"the cell was shown in our previous study [19]"*) · [`sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps`](sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps.md) (이 논문을 ref 25 로 · §0-1) · [`deng2016_elastic_superionic_electrolytes_dft`](deng2016_elastic_superionic_electrolytes_dft.md) (이 논문 [21] — Li₆PS₅Br E 25.3 GPa · ν 0.35) · [`sakuda2013_sulfide_mechanical_property`](sakuda2013_sulfide_mechanical_property.md) ([12]) · [`doux2020_pressure_effects_sulfide_se_jmca`](doux2020_pressure_effects_sulfide_se_jmca.md) ([23]) · [`bielefeld2020_effective_ionic_conductivity_binder`](bielefeld2020_effective_ionic_conductivity_binder.md) ([13]) · [`hlushkou2018_void_space_ion_transport_assb_cathode`](hlushkou2018_void_space_ion_transport_assb_cathode.md) ([14]) · [`koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb`](koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb.md) ([15]) · [`kato2016_high_power_assb_lsipscl_superionic`](kato2016_high_power_assb_lsipscl_superionic.md) ([3]) · [`kamaya2011_lgps_lithium_superionic_conductor`](kamaya2011_lgps_lithium_superionic_conductor.md) ([4]).
> **판독 원자료**: `litdb/figures/ohashi2021_am_youngs_modulus_ion_transport_voxel_fem_ct/digitized.csv` (133 행 — 그림 4 곡선 13 + 0.1 mS/cm 교차 1 · 그림 5 표지 51 + 맞춤 곡선 48 · 그림 6 막대 6 · 그림 8 표지 12 + 점선 점검 2) · 크롭 **36 장** (도구 9 = 그림 8 + 표 1 — 9 장 모두 다시 자름: 원 래스터 5 · 벡터 다시 렌더 3 · 표 손으로 1 / 손 크롭 27 = 패널 8 · 근거 문단 19 · **식 0 — 원문에 번호 매긴 식이 하나도 없다**) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 활물질 대신 전기화학 반응이 없는 **지르코니아 (≈200 GPa · 매끈한 구)** 와 **나일론 (≈2 GPa · 불규칙 입자)** — 둘 다 ≈50 µm — 을 Li₅.₅PS₄.₅Br₁.₅ 분말에 섞어 (지르코니아 22 · 39 · 52 vol% · 나일론 29 · 61 · 75 vol% — CT 복셀 세기) **누른 채** EIS 로 σ(P) 를 0 → ≈400 MPa 재고, 400 MPa 누른 채 찍은 CT 를 그대로 격자로 삼아 **선형 탄성 복셀 FEM** (결합 연속체 · SE 는 해상도 아래 빈틈을 품은 한 상 · E_SE = Li₆PS₅Br 의 DFT 값 25.3 GPa) 으로 같은 400 MPa 를 다시 걸면 — **단단한 상 (지르코니아 복합체에선 지르코니아 · 나일론 복합체에선 SE) 이 평균적으로 인가압보다 큰 응력을 지고**, 지르코니아가 SE 를 가릴수록 SE 의 σ 는 같은 압력에서 낮고 포화 압력이 오른다 (나일론 ≈250 · 순수 SE ≈300 · 지르코니아 22 % ≈350 · 39 / 52 % > 400 MPa) — 다만 **응력은 계산값 (측정 아님) 이고, 이온 수송 계산은 하지 않았으며, 기공 · 탈압 · 소성은 없다**.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 단단한 입자 (AM) 의 하중 몫 (R1) | ★ 400 MPa (선형 탄성 · E_SE 25.3 GPa) **SE 평균 MPS 291 · 234 · 196 MPa · 지르코니아 815 · 692 · 598 MPa** (22 · 39 · 52 vol%) → 지르코니아 축하중 몫 **[0.43, 0.45] · [0.64, 0.68] · [0.77, 0.78]** (평균 응력 정리의 아래 · 위 한계) · 나일론 복합체는 반대: SE 546 · 856 · 918 · 나일론 118 · 165 · 289 MPa (29 · 61 · 75 vol%) → 나일론 몫 [0.03, 0.09] · [0.17, 0.25] · [0.43, 0.54] · 원문 *"Stress concentrates in a material with higher Young's modulus"* (Highlights) | [판독] Fig 8 · [카드 산술] §3-6 · [인쇄] p.1 · p.5 |
| ② 그 계산의 정체 | **선형 탄성 · 결합 연속체 · 등방 (E · ν 만)** 복셀 FEM (VOXELCON · GPU · ≈300 × 300 × 300 복셀 · 복셀 = 요소) · 한쪽 고정 / 반대쪽 400 MPa / 옆면 roller (반경 고정 · 두께 방향 미끄럼) + 양쪽 가상판 · **400 MPa 로 이미 눌린 CT 형상** 에 400 MPa 를 한 번 거는 선형 풀이 — 소성 · 접촉 · 미끄럼 · 분리 · 압밀 이력 · 잔류 응력 · 탈압 없음 · *"nylon and SE are continuous in a FEM"* (p.6) · **이온 수송 계산 없음** (해상도 때문, p.3) | [인쇄] p.3 · p.6 · Fig 3 · 표 1 |
| ③ 순수 SE 의 압력별 σ · 기공 | σ(P) **0.10 (12 MPa) → 0.87 (100) → 1.73 (200) → 2.40 (300) → 2.75 mS/cm (400 MPa)** (Li₅.₅PS₄.₅Br₁.₅ · 25 °C · 누른 채 · 가압만) · *"increases rapidly when the applied pressure is under approximately 300 MPa"* · 기공률 · 상대밀도 · 진밀도 **없음** | [판독] Fig 4 (벡터 경로) · [인쇄] p.4 · [미확인] |
| ④ 복합체의 압력별 σ (실측) | 표지 51 점 (Fig 5) · ≈400 MPa 끝: 나일론 29 / 61 / 75 % = **1.74 (389) · 0.59 (364) · 0.24 (398)** · 지르코니아 22 / 39 / 52 % = **1.77 (386) · 0.99 (372) · 0.63 mS/cm (378 MPa)** · 모든 복합체가 ≈100 MPa 아래에선 그림 바닥 (0.1 mS/cm) 밑 · 200 MPa 에서 나일론 29 % 가 지르코니아 22 % 의 1.22 배 → 400 MPa 에서 0.98 배 (맞춤 곡선) | [판독] Fig 5 · [카드 산술] §3-5 |
| ⑤ 포화 압력 (σ 가 수렴하기 시작하는 압력) | 나일론 **≈250** (세 분율 모두 · *"indistinguishable"*) · 순수 SE **≈300** · 지르코니아 22 % **≈350** · 39 · 52 % **> 400 MPa** — *"approximated values within the scope of our definition"* · 정의가 두 문장으로 다르다 (§3-4) | [인쇄] p.4 · Fig 6 |
| ⑥ 복합체 기공 · 접촉 | **없음** — CT 는 AM 부피 분율만 (복셀 세기) · SE 상에 해상도 아래 빈틈 포함 · *"Nanoscale features … were not visualized in this study"* (약어 상자) | [인쇄] p.2 · p.3 |
| ⑦ 하중을 뺀 뒤 | **없음** (가압 가지 · 400 MPa 한 상태의 응력만) | [미확인] |
| ⑧ DEM 한계 · 소성의 어려움 | DEM 을 쓰지 않는다 (말 없음) · SE 치밀화 기전은 *"SE particles must undergo plastic deformation (crushing) to be densified"* (p.4) 인데 계산은 선형 탄성 · 모형을 고른 이유는 해상도 하나: *"calculation in this study was limited to FEM stress calculation, which is applicable for low resolution dataset"* (p.3) | [인쇄] p.3 · p.4 |
| ⑨ CL-90 ('Wang 2020, JPS 470' 의 NCM 경도 · NCM 140 GPa · LPSCl 24 GPa) | **셋 다 없다** — 입력 = Li₅.₅PS₄.₅Br₁.₅ 자리에 Li₆PS₅Br 의 **25.3 GPa · ν 0.35** (Deng 2016 [21]) · 지르코니아 200.0 · 0.30 · 나일론 2.0 · 0.30 (표 1 · 출처 없음) · NCM 은 *"HYA (e.g., LCO, NCM, Si)"* 한 번 (값 없음) · 이 논문은 **483 권** (470 권 아님) | [인쇄] 표 1 · p.3 · p.6 · §3-9 |

⛔ **한정어 (떼지 말 것)**: ① 재료 = **Li₅.₅PS₄.₅Br₁.₅** (LPSCl 아님 · 그 E · ν 는 측정되지 않아 Li₆PS₅Br 의 DFT 값을 빌림) + **지르코니아 · 나일론** (NCM 아님 · 전기화학 없는 대리) ② 두 대리는 **영률만 다른 것이 아니다** — 모양 (나일론 불규칙 · 거친 덩어리 ↔ 지르코니아 매끈한 구, Fig 1) · 고분자의 소성 · 밀도 · 표면이 함께 다르다 → 결과 차이를 영률로만 돌리는 것은 원문의 해석 [카드 추론] ③ **분율이 짝지어지지 않았다** (나일론 29 / 61 / 75 ↔ 지르코니아 22 / 39 / 52 %) — 결론 1 의 *"under equivalent … volumetric fraction"* 은 측정이 아니라 추론 ④ 응력 = **선형 탄성 · 결합 · 400 MPa 한 상태 · E_SE 한 값 (치밀 결정 DFT 25.3 GPa)** — 같은 그룹 2020 논문이 쓴 압분체 하한 0.3 GPa 계산은 여기 없다 ⑤ 셀 · 시료 지름 · 두께 · 질량 · SE 입경 · σ 환산 기하 · 반복 수 [미확인] · 그림 4 · 5 · 8 에 오차 막대 없음 ⑥ 응력 · σ 숫자는 [판독] (그림 4 · 5 · 6 은 벡터 좌표라 그림 자체에 대해서는 정확 · 그림 8 은 ±3 MPa) ⑦ 탈압 · 기공 · 이온 수송 계산 없음.
⇒ **절대값 전이**: 하지 않는다 (재료 · 대리 · 압력 상태 · 모델이 우리와 다르다).  옮길 수 있는 것 = **꼴과 방향** — (i) 결합 탄성 연속체에서 단단한 상은 인가압의 1.5–2.0 배를 지고 SE 는 0.49–0.73 배만 진다 (E 대비 7.9 · 22–52 vol%) (ii) 단단한 AM 은 같은 압력에서 SE σ 를 낮추고 포화 압력을 올린다 · 무른 상대는 반대 (iii) 그 차이는 포화 압력 위 (≈400 MPa) 에서 거의 사라진다 (200 MPa 1.22 배 → 400 MPa 0.98 배).

---

## 0-1. ★ 고른 의도 대조 (위시 11-17 · sakka2022 n 줄 + 본 세션 의도 넷)

의도 원문 (위시): *"[n] A. Ohashi, M. Kodama, N. Horikawa and S. Hirai, J. Power Sources, 2021, 483, 229212. | d · i — 'In composites with different Young's moduli, large pressures can be applied to materials that have larger Young's moduli' 의 근거 (단단한 AM 하중 몫) · 카드 §12 ref 25"* + 본 세션 의도 넷 (AM 하중 몫 ↔ AM 영률 · 이온 수송 ↔ 압력 · 영률 · CL-90 · [DEM 우선 (수영)] 재설계).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| Sakka 2022 의 *"large pressures can be applied to materials that have larger Young's moduli"* 의 근거 (ref 25) | **채움 (문장 그대로 · 계산값으로)** · 일부 (Sakka 의 쓰임) | Highlights *"Stress concentrates in a material with higher Young's modulus."* · p.5 *"The common phenomenon observed in both Fig. 8a and b is that a stress concentration occurs on the material with higher Young's modulus."* · 조건 = **선형 탄성 복셀 FEM 계산 (응력 측정 아님)** · 400 MPa · 결합 연속체 · Li₅.₅PS₄.₅Br₁.₅ (25.3 GPa) + 지르코니아 (200) / 나일론 (2) · 400 MPa 로 눌린 형상.  ⚠ Sakka 는 이 문장을 **≤ 12 MPa 에서 겉보기 NCM 분율이 늘어나는 것** 의 설명에 썼다 (sakka2022 카드 L126) — 이 논문은 낮은 압력의 겉보기 분율 변화를 다루지 않는다 (400 MPa 한 상태 · 탄성) → 쓰임은 원문 범위 밖 |
| d — 단단한 AM 의 하중 몫 | **채움 (계산)** | Fig 8b [판독]: SE 291 / 234 / 196 · 지르코니아 815 / 692 / 598 MPa (22 / 39 / 52 vol%) · 인가 400 MPa → 지르코니아 축하중 몫 [0.43, 0.45] · [0.64, 0.68] · [0.77, 0.78] [카드 산술 §3-6] · 본문 *"This material will act as a stress support and decrease the stress experienced by the neighboring materials"* (p.5) |
| i — 복합 양극의 압력별 기공 | **없음** | 기공률 · 상대밀도 · 진밀도 · 두께가 본문 · 그림 · 표 어디에도 없다 ('porosity' 0 회 · 'void ratio' 1 회 — 정성) · 압력별 **σ** 는 있다 (Fig 5) |
| (의도 1) AM 영률을 바꾸면 AM · SE 응력 (평균 · 분포 · 비) · 포화 압력이 어떻게 | **채움** (평균 · 비 · 포화 압력) · **일부** (분포) | 평균 = Fig 8 · 비 = §3-6 (지르코니아 ÷ SE 2.80 / 2.96 / 3.05 · 나일론 ÷ SE 0.22 / 0.19 / 0.31 [카드 산술]) · 분포 = Fig 7 의 3D 색 지도 (0–800 MPa) 와 본문 대략값 (*"approximately 400 MPa and above"* · *"roughly 200 MPa"* · *"approximately 300 MPa and below"* · *"roughly 600 MPa and above"*) 뿐 — 히스토그램 · 분산 없음 · 포화 압력 = Fig 6 |
| (의도 1) 복셀 FEM 의 구성식 · 경계 · 해상도 · 입력 물성 | **채움** · 일부 (수치 사양) | 선형 탄성 (*"linear voxel-based finite-element method"* · *"Following Hooke's law"*) · BC Fig 3 · 복셀 5 × 5 × 6 µm (CT) · ≈300³ · 표 1 (E · ν) — 요소 종류 · 풀이기 · 수렴 · 시간 · 메모리 [미확인] |
| (의도 1) 가압만 / 제하 포함 | **가압만** (제하 없음을 확인) | σ(P) 는 가압 가지 · FEM 은 400 MPa 한 번 |
| (의도 2) EIS σ 가 압력 · AM 영률에 따라 어떻게 · 측정 조건 | **채움** · 일부 (조건) | Fig 4 · 5 · 6 · 누른 채 · 25 °C · 정전위 EIS 1 MHz–1 Hz · Li 금속 전극 없음 (p.3) · 조성 = CT 부피 분율 · 시료 두께 · 면적 · 등가회로 · 반복 [미확인] |
| (의도 2) CT 로 본 구조 (기공 · 접촉) 와 σ 를 어떻게 잇나 | **일부** | CT 는 FEM 형상과 부피 분율에만 쓰인다 · 기공 · 접촉 면적을 σ 와 잇는 계산은 없다 (*"ion transportation simulation was not be [sic] conducted"*, p.3) · 연결은 서술로만: SE 응력 ↓ → *"the nanoscale features continue to exist through compression"* → σ ↓ (p.6) |
| (의도 2) 우리 σ_ionic (접촉망 · Holm) · 수송 tortuosity 와 견줄지 | **일부 (견주지 않는 까닭 포함)** | 원문 tortuosity 숫자 0 · 이 카드의 겉보기 f = σ_복합/σ_SE(P) · tau2_app = (1 − φ_AM)/f [카드 산술 §3-7] 만 — SE 상태 차이 (응력) 가 섞인 양이라 우리 tau2 (기준 σ₀ 고정) 와 같은 양이 아니다 |
| (의도 3) CL-90 세 값 · 원 출처 | **채움 (없음을 값으로 확인)** | §3-9 — 세 값 모두 없다 · 영률 출처는 [21] Deng 2016 (SE) · [7] Cheng 2017 (LCO 등) · 지르코니아 · 나일론은 출처 없음 |
| (의도 4) [DEM 우선 (수영)] — AM + SE 를 가압부터 탈압까지 한 모델로 | **일부** | 보여 주는 것 = 결합 탄성 연속체에서의 상별 하중 몫 · 영률 대비의 방향 · 포화 압력 이동 / 못 하는 것 = 압밀 과정 · 소성 · 접촉 · 미끄럼 · 파쇄 · 탈압 (§8) |
| 가리킨 카드 (sakka2022) 의 **2 차 인용 값** | **해당 없음 (숫자 없음)** | sakka2022 카드 L126 · L362 는 이 논문에서 숫자를 옮기지 않았다 (Sakka 의 문장 · 서지뿐) · 서지 *"A. Ohashi, M. Kodama, N. Horikawa and S. Hirai, J. Power Sources, 2021, 483, 229212."* = 원문 머리글 · 첫 쪽과 같다 |

⇒ **의도 대조 결과: 일부** — d (단단한 AM 의 하중 몫) 는 **계산값으로 채움** (측정 아님 · 선형 탄성 · 400 MPa 한 상태) · i (복합 양극 기공) 는 **없음** · CL-90 은 '세 값 없음' 으로 채움.

---

## 1. 한 줄 요약
같은 그룹의 앞 논문 [17] 이 '활물질이 전극 안 응력 분포를 만들고 그것이 SE 의 빈틈 분포 · σ 를 바꾼다' 고 본 데서 출발해 (p.2), **활물질 영률** 이 원인이라면 영률이 다른 두 대리 (지르코니아 ≈200 · 나일론 ≈2 GPa · 둘 다 ≈50 µm) 로 σ(P) 가 갈려야 한다고 보고 Li₅.₅PS₄.₅Br₁.₅ 모형 복합체의 EIS 를 0 → ≈400 MPa 누른 채 잰다 — 나일론 복합체는 ≈250 MPa 에서 포화 (순수 SE ≈300 보다 낮다) · 지르코니아는 22 % 만 ≈350 MPa 에서 포화하고 39 · 52 % 는 400 MPa 까지 포화하지 않으며, 200 MPa 에선 분율이 더 큰 나일론 복합체가 지르코니아 복합체보다 σ 가 높거나 같다.  400 MPa CT 위 선형 탄성 복셀 FEM 은 **영률이 큰 상에 응력이 몰리는** 꼴 (지르코니아 복합체 = 지르코니아 · 나일론 복합체 = SE) 을 보여, 저자는 '단단한 AM 은 SE 를 가려 나노 빈틈 · 입계가 남고 σ 가 낮다 / 무른 AM 은 SE 를 더 눌러 σ 를 높인다' 고 결론짓는다 — 바인더 · 도전재에도 넓힐 수 있다고 적는다 (p.6).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| A. Ohashi · M. Kodama\* · N. Horikawa · S. Hirai (Tokyo Tech) | J. Power Sources 483 (2021) 229212 · 7 쪽 | 10.1016/j.jpowsour.2020.229212 | SE = **Li₅.₅PS₄.₅Br₁.₅** (자체 합성 · Yu 2020 [18] 처방) · CAM 없음 — **지르코니아 (HYA 대리) · 나일론 (LYA 대리)** ≈50 µm · 도전재 · 바인더 없음 | 실험 (누른 채 EIS · X 선 CT) + **영상 기반 선형 탄성 복셀 FEM** (응력만) — DEM · MPM · 압밀 계산 · 이온 수송 계산 없음 |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 셀 · 측정 상수 (p.2–3)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| SE 합성 | Li₅.₅PS₄.₅Br₁.₅ 3 g · 원료 Li₂S · P₂S₅ · LiBr (비 = 숫자 없음) · ZrO₂ 포트 50 ml · 분쇄 보조 디에틸에테르 **0.2 ml** · ZrO₂ 볼 φ10 mm × 16 · 고에너지 진동 밀 (Retsch EMAX) **1200 rpm 10 h** → **400 °C 10 h** · Ar 글러브박스 · *"based on a study by Yu et al. [18]"* · 고른 까닭 = 높은 σ 와 안정성 (높은 대리 분율에서도 σ 를 정확히 잴 수 있게) | [인쇄] p.2 · 크롭 `txt_p2_synthesis_li55ps45br15_milling_400c.png` |
| SE 입경 · 형상 · XRD | 원문에 없음 | [미확인] |
| 대리 입자 | 지르코니아 = 매끈한 구 · 나일론 = 불규칙 · 거친 표면의 덩어리 (Fig 1 SEM · 50 µm 막대) · *"particle sizes were both approximately 50 μm"* · 공급처 · 등급 · 나일론 종류 (PA6 / PA12 …) [미확인] | [인쇄] p.2 · [판독 · 정성] Fig 1 |
| 대리의 물성 (본문) | *"The Young's modulus of zirconia (HYA) and nylon (LYA) are approximately 200 and 2 GPa"* · 문헌 활물질 *"LCO, Si, Sn, and graphite … approximately 190, 185, 50, and 20 GPa, respectively [7]"* | [인쇄] p.2 |
| 섞기 | *"thoroughly mixing zirconia and the SE or by mixing nylon and the SE with a spoon and shaking the container by hand"* | [인쇄] p.2 |
| 부피 분율 | 나일론 **29 · 61 · 75 %** · 지르코니아 **22 · 39 · 52 %** (그림 5 · 6 범례) — *"determined from the X-ray CT image by counting the number of voxels that belonged to the material and comparing it to the entire composite"* · 그림 8 점의 x 위치 28.8 · 60.8 · 74.7 · 22.2 · 39.2 · 52.1 vol% [판독] · 질량 분율 · 시료 질량 [미확인] | [인쇄] p.3 · Fig 5–8 |
| 셀 | 기밀 셀 · *"capable of pressurization up to 450 MPa, X-ray CT visualization, and electrochemical measurement; the cell was shown in our previous study [19]"* · Fig 2: PEEK 소매 + 위 · 아래 스테인리스 막대 (아래에서 가압) · 회전축 수직 · 시료 지름 · 두께 [미확인] | [인쇄] p.2 · Fig 2 |
| EIS | 퍼텐쇼-갈바노스탯 (Admiral Inst. Squidstat Plus) · **정전위 EIS 1 MHz–1 Hz · 25 °C** · *"without a lithium metal electrode to ignore the SE/Li metal interface resistance [19]"* · 등가회로 · σ 환산 기하 · 단계마다 유지 시간 · 반복 [미확인] | [인쇄] p.3 · 크롭 `txt_p2_p3_eis_potentiostatic_1mhz_1hz_25c.png` |
| X 선 CT | 텅스텐 표적 **160 kV · 70 µA** · 선원–시료 **25 mm** · 선원–검출기 **1000 mm** (기하 배율 40 [카드 산술]) · **복셀 5 × 5 × 6 µm · 시야 5.12 × 5.12 × 6.14 mm** (= 1024 × 1024 × 1023 복셀 [카드 산술]) · *"sufficiently wide to measure the entire compressed composite electrode"* · EIS 뒤에 찍음 · 계산에 쓴 것 = *"X-ray CT measurements under 400 MPa"* · 투영 수 · 재구성 · 이진화 문턱 · 6 µm 축이 어느 방향인지 · 다른 압력의 CT 유무 [미확인] | [인쇄] p.3 · 크롭 `txt_p3_xct_160kv_voxel_5x5x6um_fov_volume_fraction.png` |
| 해상도 대 입자 | 대리 50 µm = 복셀 10 개 (가로) · 8.3 개 (6 µm 축) [카드 산술] · SE 입자 · 입계 · 나노 빈틈은 안 풀린다 (*"Nanoscale features … not visualized"*) | [카드 산술] · [인쇄] p.2 |

### 3-2. ★ 순수 SE 의 σ(P) — Li₅.₅PS₄.₅Br₁.₅ (Fig 4 · p.4)
| 압력 (MPa) | 12.3 | 25 | 50 | 100 | 150 | 200 | 250 | 300 | 350 | 400 |
|---|---|---|---|---|---|---|---|---|---|---|
| σ (mS/cm) | **0.10** (그림 바닥) | 0.205 | 0.426 | **0.868** | 1.316 | **1.734** | 2.101 | **2.402** | 2.615 | **2.745** |
- 전부 [판독] — 그림 4 의 파란 선은 **벡터 경로** (#58) 라 그 좌표를 그대로 환산 (틀 x 364.95 ↔ 0 · 520.89 ↔ 400 MPa · 로그 y 686.93 ↔ 0.1 · 553.82 ↔ 10 · '1' 글자 중심이 틀 한가운데 0.02 pt 안).  선만 있고 측정 표지가 없다 — **측정값을 이은 선인지 맞춤인지** [미확인] · 오차 막대 없음.
- 원문: *"The ionic conductivity at 400 MPa roughly corresponds with the reported ionic conductivity [18]"* (Yu 2020 의 값은 인쇄 안 됨 [미확인]) · *"the ionic conductivity increases rapidly when the applied pressure is under approximately 300 MPa. At pressures above 300 MPa, the ionic conductivity nearly converges to a particular value"* · 기전 = 입자 **사이** 빈틈과 입자 **안** 빈틈의 감소 [19,24] · *"as the larger voids disappear as the pressure is increased, SE particles must undergo plastic deformation (crushing) to be densified"* (p.4).
- 모양 [카드 산술]: 400 MPa σ 의 **32 % 가 100 · 63 % 가 200 · 87 % 가 300 MPa** 까지 (0.868 · 1.734 · 2.402 ÷ 2.745).  같은 그룹 kodama2020 의 Li₆PS₅Br (75–150 µm · ≤ 103 MPa) 은 103 MPa 에서 0.79 mS/cm [다른 카드 `kodama2020_…` §3-2] — 재료 · 입경 · 셀이 달라 나란히만.

### 3-3. ★ 복합체의 σ(P) — 그림 5 표지 (가압 가지 · 25 °C · 누른 채)
| 계열 | (압력 MPa, σ mS/cm) 표지 [판독 · 벡터 중심] |
|---|---|
| 나일론 29 % (원 · 실선) | (99.3, 0.102) · (130.5, 0.483) · (154.7, 0.763) · (167.8, 0.879) · (211.4, 1.18) · (237.7, 1.47) · (279.3, 1.67) · (349.9, 1.72) · (370.6, 1.79) · (388.6, 1.74) |
| 나일론 61 % (삼각 · 점선) | (127.7, 0.163) · (176.1, 0.355) · (216.3, 0.437) · (275.2, 0.573) · (338.8, 0.600) · (364.4, 0.589) |
| 나일론 75 % (네모 · 파선) | (222.5, 0.124) · (243.3, 0.177) · (297.2, 0.204) · (348.4, 0.235) · (365.1, 0.237) · (397.6, 0.241) |
| 지르코니아 22 % (원 · 실선) | (103.4, 0.134) · (136.7, 0.338) · (158.2, 0.515) · (184.4, 0.877) · (204.5, 1.11) · (239.1, 1.26) · (275.8, 1.39) · (315.3, 1.58) · (328.5, 1.64) · (351.3, 1.74) · (386.0, 1.77) |
| 지르코니아 39 % (삼각 · 점선) | (122.8, 0.178) · (162.3, 0.247) · (190.6, 0.321) · (203.1, 0.356) · (232.9, 0.546) · (267.5, 0.552) · (297.3, 0.653) · (312.5, 0.780) · (341.6, 0.888) · (372.1, 0.993) |
| 지르코니아 52 % (네모 · 파선) | (168.5, 0.128) · (187.9, 0.184) · (223.2, 0.283) · (237.1, 0.348) · (289.0, 0.447) · (320.1, 0.500) · (355.4, 0.586) · (378.2, 0.626) |
- 표지는 벡터 도형 (원 = 곡선 네 조각 · 삼각 = 선 셋 · 네모 = 사각) 의 중심 — 그림 자체에 대해 0.1 MPa · 0.3 % 안 [판독].  **맞춤 곡선** (실선 · 점선 · 파선) 의 함수꼴은 원문에 없다 [미확인] — 나일론 61 % 곡선은 ≈340 MPa 에서 꼭짓점을 지나 400 MPa 에서 내려간다 (0.626 → 0.592 [판독]).
- 맞춤 곡선 값 [판독]: 200 MPa = 나일론 29 / 61 / 75 % **1.17 · 0.419 · 0.101** · 지르코니아 22 / 39 / 52 % **0.958 · 0.395 · 0.235** · 400 MPa = 나일론 **1.77 · 0.592 · 0.239** · 지르코니아 **1.80 · 1.08 · 0.671 mS/cm** (지르코니아 39 · 52 % 의 400 MPa 값은 마지막 표지 372 · 378 MPa 위의 곡선 연장).
- 그림 바닥 0.1 mS/cm 아래 · 첫 표지 압력 (≈100–223 MPa) 아래의 측정이 있었는지 [미확인] · 오차 막대 없음 · 반복 수 [미확인].

### 3-4. ★ 포화 압력 — 그림 6 · 정의 (p.2 · p.4)
| 계 | 포화 압력 (MPa) | 표지 |
|---|---|---|
| 순수 SE | **≈300** | [인쇄] p.4 |
| 나일론 29 · 61 · 75 % | **≈250 · ≈250 · ≈250** (막대 윗변 250.2 [판독 · 벡터]) | [인쇄] p.4 · Fig 6 |
| 지르코니아 22 % | **≈350** (막대 350.5 [판독]) | [인쇄] p.4 · Fig 6 |
| 지르코니아 39 · 52 % | **> 400** (막대는 400.0 에서 잘리고 *"> 400 MPa"* 표지) | [인쇄] Fig 6 · p.4 |
- **정의가 둘**: 약어 상자 *"Applied pressure at which ionic conductivity begins to converge to a constant value"* (p.2) ↔ 본문 *"we defined this saturation pressure as the point at which the function of the ionic conductivity with respect to pressure deters from a linear relationship"* (p.4) — 어느 축 (선형 · 로그) 에서의 '선형' 인지 · 판정 문턱 [미확인] · 값은 *"approximated values within the scope of our definition of saturation pressure"* (p.4).
- 저자 서술: *"saturation pressure increased in the following order: nylon composites (250 MPa), pure SE (300 MPa), zirconia composite (>400 MPa)"* · *"there is a correlation between the Young's modulus of the active material and the saturation pressure"* · 나일론 분율 사이 차이는 *"indistinguishable from the experimental results in Fig. 5a"* (p.6).

### 3-5. ★ 200 MPa · 400 MPa 비교 — 원문 주장 ↔ 판독
| 원문 주장 (p.4) | 판독 [맞춤 곡선 · 카드 산술] | 가까운 표지 [판독] |
|---|---|---|
| 200 MPa: 나일론 29 % > 지르코니아 22 % | 1.17 ÷ 0.958 = **1.22 배** | 211.4 MPa 1.18 ↔ 204.5 MPa 1.11 |
| 200 MPa: 나일론 61 % ≈ 지르코니아 39 % | 0.419 ÷ 0.395 = **1.06 배** | 216.3 MPa 0.437 ↔ 203.1 MPa 0.356 |
| 200 MPa: 나일론 61 % > 지르코니아 52 % | 0.419 ÷ 0.235 = **1.79 배** | — |
| ≥ 400 MPa: 지르코니아 22 % > 나일론 29 % | 1.80 ÷ 1.77 = **1.02 배** | 386.0 MPa 1.767 ↔ 388.6 MPa 1.739 (1.016 배) — ⚠ 나일론 29 % 의 350–389 MPa 세 표지가 1.72 · 1.79 · 1.74 로 ±2 % 흔들린다 → **차이는 표지 흩어짐 안** |
| 400 MPa: 지르코니아 39 · 52 % > 나일론 61 % | 1.08 · 0.671 ÷ 0.592 = **1.83 · 1.13 배** | 372.1 MPa 0.993 · 378.2 MPa 0.626 ↔ 364.4 MPa 0.589 (1.69 · 1.06 배) |
- 읽는 법: 200 MPa 에선 **분율이 7–22 %p 더 큰** 나일론 복합체가 지르코니아 복합체와 같거나 높다 — 영률 (또는 같이 바뀐 모양 · 소성) 의 효과가 분율 효과를 넘는다 [카드 추론] · 400 MPa 에선 그 이득이 사라지거나 뒤집힌다.  ⚠ 같은 분율의 짝은 하나도 없다 — *"when the nylon and zirconia volumetric fraction was the same"* (p.4) 은 측정이 아니라 분율이 더 큰 나일론이 이기는 데서 끌어낸 추론.

### 3-6. ★ 응력 분포 — 그림 7 · 8 (선형 탄성 복셀 FEM · 인가 400 MPa)
| 복합체 · AM vol% | SE 평균 MPS (MPa) | AM 평균 MPS (MPa) | SE ÷ 인가 | AM ÷ 인가 | AM ÷ SE | Σ φ·MPS ÷ 400 | AM 축하중 몫 [아래, 위] | Reuss 몫 (= φ) | Voigt 몫 |
|---|---|---|---|---|---|---|---|---|---|
| 나일론 29 % | **546** | **118** | 1.37 | 0.30 | 0.22 | 1.055 | [0.03, 0.09] | 0.29 | 0.031 |
| 나일론 61 % | **856** | **165** | 2.14 | 0.41 | 0.19 | 1.086 | [0.17, 0.25] | 0.61 | 0.110 |
| 나일론 75 % | **918** | **289** | 2.30 | 0.72 | 0.31 | 1.116 | [0.43, 0.54] | 0.75 | 0.192 |
| 지르코니아 22 % | **291** | **815** | 0.73 | 2.04 | 2.80 | 1.016 | **[0.43, 0.45]** | 0.22 | 0.690 |
| 지르코니아 39 % | **234** | **692** | 0.585 | 1.73 | 2.96 | 1.032 | **[0.64, 0.68]** | 0.39 | 0.835 |
| 지르코니아 52 % | **196** | **598** | 0.49 | 1.50 | 3.05 | 1.013 | **[0.77, 0.78]** | 0.52 | 0.895 |
- 평균 MPS = 그림 8 의 *"averaged absolute value of the minimum principal stress"* (p.5) — 원 래스터 (xref 96 · 300 dpi) 의 색 원판 무게중심을 눈금선 (0–1000 MPa · 100 마다) 에 조각선형으로 맞춤 · ±3 MPa [판독] (점선 'Applied Pressure' = 398.9 · 400.0 으로 읽혀 점검 통과).  *"The minimum principal stress is the maximum compressive stress experienced at a particular voxel"* (p.5).
- **AM 축하중 몫의 한계** [카드 산술 · 같은 그룹 2020 카드와 같은 방법]: 평균 응력 정리 — 옆면 roller (두께 방향 견인 0) 이면 복합체 전체의 부피 평균 축응력 = 인가 400 MPa 이고, 압축을 양으로 모든 점에서 MPS ≥ 축응력 → **아래 = 1 − (1 − φ)·⟨MPS⟩_SE / 400 · 위 = φ·⟨MPS⟩_AM / 400** (가정: 그림의 '평균' = 상별 부피 평균 · φ = 표시 분율).  **Σ φ·MPS ÷ 400 = 1.01–1.12** (MPS ≥ 축응력과 맞는 방향 — 판독 일관 점검).
- Reuss (등응력 · 몫 = φ) · Voigt (등변형 · 몫 = φE_AM / (φE_AM + (1 − φ)E_SE), E_SE 25.3) 사이에 FEM 몫이 모두 들어간다 [카드 산술] — 지르코니아는 Reuss (= φ) 보다 0.21–0.29 위 · 나일론은 Voigt 보다 0.00–0.35 위.
- 3D 지도 (그림 7 · 0–800 MPa 색 막대) 원문 서술: 나일론 29 % — SE + 빈틈 *"approximately 400 MPa and above"* · 나일론 *"overall colored blue … roughly 200 MPa"* · 지르코니아 22 % — SE + 빈틈 *"approximately 300 MPa and below"* · 지르코니아 *"overall colored red … roughly 600 MPa and above"* (p.5) — 나일론은 그림 8 평균 (118) 과 숫자가 다르다 (≈200 ↔ 118) · 지르코니아 '≈600 이상' 은 815 와 모순은 아니다 (색 인상 · 대략값 [카드 해석]).
- 분율과의 관계 (원문): 나일론이 늘면 SE 응력 ↑ (*"stress to concentrate on the limited volume of the SE"*) · 나일론 자신의 응력도 ↑ (*"Because nylon and SE are continuous in a FEM, the increase in the strain of the SE induces an increase in the strain of an adjacent nylon. Following Hooke's law, the increased strain leads to an increase in the stress of nylon"*, p.6) · 지르코니아가 늘면 SE · 지르코니아 응력 **둘 다** ↓ (*"the rigidity of the stress support increases"*, p.6).

### 3-7. 복합체 σ ÷ 순수 SE σ (같은 인가압) · Bruggeman 대조 [카드 산술]
| 계 (φ_AM) | f = σ_복합 / σ_SE(P) — 첫 표지 · 200 · 300 · 400 MPa | f ÷ (1 − φ_AM)^1.5 (200 / 400 MPa) | tau2_app = (1 − φ_AM) / f (200 / 400 MPa) |
|---|---|---|---|
| 나일론 29 % | 0.119 (99 MPa) · 0.676 · 0.710 · 0.644 | 1.13 / 1.08 | 1.05 / 1.10 |
| 나일론 61 % | 0.150 (128) · 0.242 · 0.253 · 0.216 | 0.99 / 0.89 | 1.61 / 1.81 |
| 나일론 75 % | 0.066 (223) · 0.058 · 0.090 · 0.087 | 0.47 / 0.70 | 4.29 / 2.88 |
| 지르코니아 22 % | 0.150 (103) · 0.553 · 0.645 · 0.656 | 0.80 / 0.95 | 1.41 / 1.19 |
| 지르코니아 39 % | 0.170 (123) · 0.227 · 0.304 · 0.394 | 0.48 / 0.83 | 2.68 / 1.55 |
| 지르코니아 52 % | 0.088 (169) · 0.135 · 0.187 · 0.245 | 0.41 / 0.74 | 3.55 / 1.96 |
- σ_SE(P) = 그림 4 곡선 (같은 인가압) · 복합체 = 그림 5 맞춤 곡선 (첫 열만 표지) · φ_SE = 1 − φ_AM (CT 의 'SE' 는 해상도 아래 빈틈을 품는다).  ⚠ 이 f · tau2_app 는 **겉보기** — 복합체 안 SE 의 압밀 상태가 순수 SE 와 다르다는 것 (이 논문의 주장 자체) 이 섞여 있어 기하 tortuosity 도, 우리 수송 tortuosity (tau2 · 기준 σ₀ 고정 · CLAUDE.md τ 규약) 도 아니다.
- 읽는 법 [카드 추론]: 200 MPa 에서 지르코니아 복합체는 Bruggeman 의 0.41–0.80 · 나일론 29 / 61 % 는 0.99–1.13 (방향 = 원문) · 400 MPa 에선 0.74–0.95 와 0.70–1.08 로 가까워진다.  **첫 표지 (≈100–130 MPa)** 에서 나일론 29 · 61 % · 지르코니아 22 · 39 % 는 순수 SE 의 0.12–0.17 뿐 — 단단하든 무르든 ≈50 µm 대리가 낮은 압력에서 SE 망을 크게 끊는다 (원문은 이 '늦은 시작' 을 다루지 않는다).

### 3-8. 국소 응력 → σ 의 거친 점검 [카드 산술 · 카드 추론 — 원문에 없는 계산]
같은 그룹 2020 논문 [17] 은 복셀마다 FEM 응력으로 순수 SE σ(P) 를 읽어 넣어 전도를 풀었다 [다른 카드 `ohashi2020_…` §4-3].  이 논문은 그 계산을 하지 않았으므로, 상 평균으로만 같은 생각을 대 본다: σ_추정 = σ_SE(P = SE 평균 MPS) × (1 − φ_AM)^1.5.
- 지르코니아 22 / 39 / 52 %: σ_SE(291 / 234 / 196 MPa) = 2.35 / 1.98 / 1.70 → σ_추정 **1.62 / 0.94 / 0.56** ↔ 400 MPa 맞춤 1.80 / 1.08 / 0.671 → 실측 ÷ 추정 **1.12 / 1.15 / 1.19**.
- 나일론: SE 평균 MPS (546–918 MPa) 가 그림 4 범위 (≤ 400) 밖 → σ_SE ≥ 2.745 로만 (단조 가정) σ_추정 ≥ 1.64 / 0.67 / 0.34 ↔ 실측 1.77 / 0.59 / 0.24 → 29 % 1.08 · **61 % 0.88 · 75 % 0.70 (실측이 추정의 아래 한계보다 작다)**.
- ⇒ 지르코니아 쪽은 '응력이 낮아 덜 다져진 SE' 와 Bruggeman 기하만으로 10–20 % 안에서 맞는다 · 나일론 61–75 % 는 SE 가 더 눌렸다 해도 기하 (SE 25–39 % · 불규칙 대리) 항이 이긴다 — **원문의 '무른 AM → SE 응력 ↑ → σ ↑' 는 낮은 분율 (29 %) 에서만 수치로 받쳐진다** [카드 추론 · 상 평균 · Bruggeman · 응력 상태를 일축 압력과 같게 둔 거친 가정].

### 3-9. 입력 물성 (표 1) · 정본 카드 · CL-90 대조
| 원문 값 (표 1 · p.3) | 원문의 근거 | 대조 |
|---|---|---|
| Li₅.₅PS₄.₅Br₁.₅ E **25.3 GPa** · ν **0.35** | *"The Young's modulus and Poisson's ratio of Li5.5PS4.5Br1.5 have not been measured. Therefore, in this study, we used the typical parameters of lithium-argyrodite with bromine (Li6PS5Br)"* · *"LPS, Li6PS5Cl, Li6PS5Br, and Li6PS5I have Young's moduli in the range of 20–30 GPa … [21]"* | [21] = Deng 2016 · `deng2016_…` Table III: Li₆PS₅Br **E 25.3 · ν 0.35** (0 K 정적 DFT) [다른 카드] → 값 · ν 둘 다 같다 · 같은 표: Li₆PS₅Cl 22.1 · Li₆PS₅I 30.0 · Li₇P₃S₁₁ 21.9 GPa (이 논문의 'LPS' = Li₇P₃S₁₁, p.1) → '20–30 GPa' 와 맞는다 |
| 지르코니아 E **200.0 GPa** · ν **0.30** | 표에 출처 없음 · 본문 *"approximately 200"* | 출처 [미확인] |
| 나일론 E **2.0 GPa** · ν **0.30** | 표에 출처 없음 · 본문 *"approximately … 2 GPa"* | 출처 [미확인] · 나일론 종류 [미확인] |
| 문헌 활물질 *"LCO, Si, Sn, and graphite … approximately 190, 185, 50, and 20 GPa, respectively [7]"* (p.2) | [7] = Cheng · Taylor · Wolfenstine · Sakamoto, *"Elastic properties of lithium cobalt oxide (LiCoO 2 )"*, J. Asian Ceram. Soc. 5 (2017) 113–117 | `koerver2018_…` L187 이 같은 Cheng 2017 (J. Asian Ceram. Soc.) 에서 LCO **191.0 GPa** · ν 0.24 를 옮겼다 [다른 카드] → LCO 190 은 맞는 쪽 · **Si · Sn · 흑연 값이 LCO 논문 한 편에서 왔는지** [미확인] (제목상 LCO 만) |
| **CL-90 세 값** (NCM 경도 · NCM E 140 GPa · LPSCl E 24 GPa) | — | **없음** — NCM 은 *"HYA (e.g., LCO, NCM, Si)"* (p.6) 한 번 · 값 없음 · 경도 단어 0 회 · LPSCl 은 '20–30 GPa 범위' 의 한 이름으로만 (값 없음) · 이 논문 = **483 권 229212** (CL-90 의 *"470 (article 228413)"* 와 권 · 번호가 다르다) · 같은 그룹 470 권 논문 (228437) 도 세 값이 없다 [다른 카드 `ohashi2020_…` §3-6] |

### 3-10. 같은 그룹 2020 논문 ([17] · `ohashi2020_…`) 과 나란히 [다른 카드 · 카드 산술]
| 항목 | 2020 ([17]) | 2021 (이 카드) |
|---|---|---|
| SE | LGPS (< 40 µm) | Li₅.₅PS₄.₅Br₁.₅ (입경 [미확인]) |
| 대리 | ZrO₂ (< 150 µm) 19 · 42 · 55 · 67 vol% | 지르코니아 (≈50 µm 구) 22 · 39 · 52 · 나일론 (≈50 µm) 29 · 61 · 75 vol% |
| 압력 | 100 MPa 한 점 (순수 SE 0–≈129) | σ(P) 0–≈400 · CT · FEM 400 MPa |
| σ 측정 | DC | 정전위 EIS 1 MHz–1 Hz · 25 °C |
| CT 복셀 | 4 × 4 × 5 µm | 5 × 5 × 6 µm |
| FEM | ≈300 × 300 × 400 · E_SE 21.7 ↔ 0.3 GPa 두 극단 | ≈300³ · E_SE 25.3 GPa 한 값 |
| 이온 수송 계산 | 응력 → 국소 σ (Case 1–3) | **없음** |
| SE 평균 ÷ 인가 (단단한 상 복합체) | 0.877 · 0.660 · 0.609 · 0.489 (19 · 42 · 55 · 67) | 0.73 · 0.585 · 0.49 (22 · 39 · 52) |
| 단단한 상 몫 아래 한계 | 0.29 · 0.62 · 0.73 · 0.84 | 0.43 · 0.64 · 0.77 |
| 단단한 상 ÷ SE 평균 (E 대비) | 2.24 (42 %) (9.2) | 2.80 · 2.96 · 3.05 (7.9) |
- 비슷한 분율에서 2021 의 SE 몫이 더 작다 (22 vs 19 %: 0.73 vs 0.88 · 52 vs 55 %: 0.49 vs 0.61) — E 대비는 오히려 작은데 (7.9 vs 9.2) — 입경 (≈50 µm 구 ↔ < 150 µm) · 압력 · 시편 · 격자 · SE 가 다 달라 원인을 가를 수 없다 [카드 추론].

### 3-11. 원문 안 어긋남 (고치지 않고 적는다)
1. p.5 *"zirconia composite containing 22% zirconia (LYA)"* ↔ 그림 7 캡션 *"(HYA)"* (지르코니아 = HYA 가 맞는 쪽).
2. 약어 상자 *"Low Young' modulus"* · p.2 *"high Young' modulus"* (어포스트로피 뒤 s 빠짐) · p.3 *"simulation was not be conducted"*.
3. 포화 압력 정의 두 문장이 다르다 (§3-4) · *"at a saturation pressure of 400 MPa or above"* (p.4) — 400 MPa 는 어느 복합체의 포화 압력도 아니다.
4. 정렬 문장 *"zirconia composite (>400 MPa)"* (p.4) ↔ 같은 쪽 · 그림 6 의 지르코니아 22 % ≈350 MPa.
5. 셀: *"capable of pressurization up to 450 MPa … shown in our previous study [19]"* ↔ [19] (kodama2020) 의 셀은 *"maximum ≈100 MPa (PEEK durability)"* [다른 카드 `kodama2020_…` §3-1] — 같은 셀인지 [미확인] · X 선 조건도 다르다 (그쪽 CT = Mo 66 kV · 복셀 1.62 µm · 160 kV 텅스텐은 스프링 영상용 ↔ 이쪽 CT = 160 kV 텅스텐 · 5 × 5 × 6 µm).
6. 참고문헌 [10] = *"A. Hayashi, M. Tatsumisago, Mechanical properties of sulfide glasses in all-solid-state batteries, J. Ceram. Soc. Japan. (2018) 719–727."* — 권 없음 · 같은 제목을 2020 논문 정독 출력은 *"A. Kato, M. Nose, M. Yamamoto, A. Sakuda, A. Hayashi, M. Tatsumisago … 126 (2018) 719–727"* 로 적었다 [다른 카드 정독 `batch_92_findings.md`] → 이 논문의 [10] 은 저자가 잘렸다.
7. 참고문헌 [20] Nagano 2004 — 학술지 이름 없이 *"https://doi.org/10.11396/jjsndi.53.701, 2004, 53, 701-708"* · 2020 논문은 같은 문헌을 *"52, 2004 … 701-701"* 로 적었다 [다른 카드 정독] — 권 · 쪽 [미확인].
8. [7] (LCO 탄성 논문) 하나에 LCO · Si · Sn · 흑연 넷의 영률을 붙였다 (§3-9).
9. p.2 오른쪽 단 첫머리 *"Li5.5PS4.5Br1.5"* 는 아래첨자 없이 조판됨 · 그림 5 캡션 *"zirconia composite"* (단수).

---

## 4. ★ 방법 — 실험 · CT · 복셀 FEM

### 4-1. 측정 사슬 (재구성)
Ar 글러브박스 → SE 합성 (§3-1) → 대리 (지르코니아 · 나일론 ≈50 µm) 와 숟가락 · 손 흔들기로 섞기 → 기밀 셀 (PEEK 소매 + 스테인리스 막대 · Fig 2) → 단계 가압 (표지 압력 ≈100 → ≈400 MPa · 순수 SE 곡선 0–400) → 단계마다 정전위 EIS (25 °C · 1 MHz–1 Hz · Li 금속 없음) → σ (기하 [미확인]) → EIS 뒤 **400 MPa 누른 채** X 선 CT (160 kV · 복셀 5 × 5 × 6 µm) → 복셀 세기로 부피 분율 → 같은 CT 를 FEM 격자로.
- **압력을 뺄 때 (탈압)**: 없다 — σ · 응력 모두 가압 가지 · 400 MPa 한 상태 (*"under high pressures up to 450 MPa"* 는 셀 · 실험 조건 문장 · 그림의 끝은 ≈400 MPa).

### 4-2. ★ 복셀 FEM (§2.2 · p.3 · Fig 3 · 표 1)
| 항목 | 내용 | 표지 |
|---|---|---|
| 지배 · 구성 | 선형 탄성 (Hooke) — *"linear stress analysis"* · *"linear voxel-based finite-element method"* · *"Following Hooke's law"* (p.6) · 등방 (표 1 = E · ν 만) | [인쇄] p.3 · p.6 |
| 소프트웨어 | VOXELCON [17,20] · Quint Corporation 지원 | [인쇄] p.3 · p.7 |
| 형상 | 400 MPa 누른 채 CT · *"voxel data from the X-ray CT measurement can be directly used as a mesh one-to-one, minimizing error related to meshing complex structures"* · *"approximately 300 × 300 × 300 voxels"* (≈2.7 × 10⁷ 요소 [카드 산술]) · 시야 1024³ 복셀 중 어느 부분 · 거친 다시 표본 여부 [미확인] | [인쇄] p.3 |
| 상 | 둘 — AM (지르코니아 또는 나일론) / SE (**+ 해상도 아래 나노 빈틈**: *"the nanoscale voids below the resolution of the X-ray CT system were incorporated in the SE"*) · 그림 7 이름표 *"SE + Voids"* · CT 에 보이는 빈틈을 따로 두었는지 [미확인] | [인쇄] p.3 · p.5 · Fig 7 |
| 물성 | 표 1 (§3-9) — SE 25.3 · 0.35 / 지르코니아 200.0 · 0.30 / 나일론 2.0 · 0.30 | [인쇄] 표 1 |
| 경계 | 양 끝에 가상판 · *"One end of the plate was fixed, and a pressure of 400 MPa was applied from the other end"* · 옆면 *"roller constraint … fixed in the radial direction but allowed to slide along the thickness direction"* · *"the condition is the same as that in the experiment"* (벽 마찰 없음) | [인쇄] p.3 · Fig 3 |
| 하중 이력 | 하나 — 400 MPa 로 이미 눌린 형상에 무응력에서 400 MPa 를 한 번 (선형이라 응력 비는 인가압과 무관 · 압밀 이력 · 잔류 응력 · 소성 없음) | [카드 추론] — 원문은 이 점을 말하지 않는다 |
| 접촉 | 없음 — 결합 연속체 (*"nylon and SE are continuous in a FEM"*, p.6) · 미끄럼 · 분리 · 접촉 면적 없음 | [인쇄] p.6 |
| 출력 | 복셀마다 최소 주응력 (MPS) · 상별 평균 절댓값 (그림 8) · 3D 지도 (그림 7 · 0–800 MPa) | [인쇄] p.5 |
| 풀이 · 자원 | GPU (*"to conduct large-scale stress analysis … a graphics-processing unit (GPU) was used"*) · 요소 종류 · 풀이기 · 수렴 · 시간 · 메모리 · GPU 기종 | [인쇄] p.3 · [미확인] |
| 맞춘 값 | **없음** (물성 = 빌린 DFT 값 · '대략' 값) · 검증 = 실측 σ 경향과의 정성 대조뿐 | [인쇄] |
| 이온 수송 계산 | **하지 않음** — *"in order to conduct an experiment under high pressures up to 450 MPa, X-ray CT measurement in high resolution was difficult to perform due to the limitation with the X-ray CT system. Since accurate ion transportation simulation will require structural measurement in high resolution, calculation in this study was limited to FEM stress calculation"* | [인쇄] p.3 · 크롭 `txt_p3_boundary_conditions_roller_no_ion_transport_simulation.png` |

### 4-3. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM 한계 진술 = 말 없음** — DEM 을 쓰지 않는다 (압밀을 계산하지 않고 눌린 CT 형상을 그대로 쓴다).  가장 가까운 것은 연속체 가정을 결론의 이유로 쓴 문장: *"From the viewpoint of a continuous model, because the stress concentration occurs in a greater magnitude on the SE as the volumetric fraction of nylon increases, the strain of the SE increases. Because nylon and SE are continuous in a FEM, the increase in the strain of the SE induces an increase in the strain of an adjacent nylon."* (p.6) — 입자 사이 미끄럼 · 분리가 허용되면 이 사슬 (무른 상의 응력 ↑) 이 약해질 수 있다 [카드 추론].
- **(ii) 소성 · 큰 변형을 넣기 어려운 이유 = 논의 없음** · 우회 = **압밀은 실험이 하고 계산은 마지막 형상의 탄성 응답만** · 비용 = ≈300³ 복셀 한 번 (GPU · 시간 [미확인]).  원문은 SE 치밀화에 소성이 필요하다고 스스로 적는다: *"as the larger voids disappear as the pressure is increased, SE particles must undergo plastic deformation (crushing) to be densified"* (p.4) — 계산은 그것을 담지 않는다 (E_SE = 치밀 결정 DFT 값).  모형을 고른 이유는 해상도 하나 (*"applicable for low resolution dataset"*, p.3).
- **(iii) 차원**: 측정 · 계산 모두 **3D** (CT 부피 · ≈300³) · 2D 는 없음 · 2D → 3D 전이 진술 없음.
- **(iv) 탈압**: 없음.

### 4-4. 기법 미니 용어집
- **최소 주응력 (MPS)** = 한 점의 세 주응력 가운데 (압축 = 음 부호 관례에서) 가장 작은 값 — 절댓값이 그 점의 **최대 압축 응력** (*"the maximum compressive stress experienced at a particular voxel"*).  축 방향 성분과는 다르고 언제나 그 이상이다.
- **평균 응력 정리** = 경계 견인력만으로 부피 평균 응력이 정해진다는 정리 — 옆면 미끄럼 (roller) 이면 복합체 전체의 평균 축응력 = 인가압 → 상별 평균으로 하중 몫의 한계를 낸다 (§3-6).
- **포화 압력 (saturation pressure)** = σ(P) 가 더 오르지 않기 시작하는 압력 (이 논문의 이름 · 정의 둘).
- **HYA / LYA** = 이 논문의 이름 — SE 보다 영률이 큰 / 작은 활물질 (대리 = 지르코니아 / 나일론).
- **Voigt (등변형) · Reuss (등응력)** = 두 상 복합체의 두 극단 — 하중 몫의 위 · 아래 기준.
- **복셀 FEM** = CT 복셀 하나를 육면체 요소 하나로 쓰는 유한요소 (메시 만들기 없음 · 계면이 계단꼴).
- **roller (미끄럼) 경계** = 벽에 수직한 변위만 막고 벽을 따라 미끄럼은 자유 (= 마찰 없는 다이 벽).
- **나노 스케일 특징 (nanoscale features)** = 이 논문의 이름 — CT 로 안 보이는 입자 사이 빈틈 · 굽은 경로 · 입계.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 (a · b) | 나일론 (불규칙 · 거친 덩어리) · 지르코니아 (매끈한 구) SEM · 50 µm 막대 | 두 대리가 **모양도** 다르다는 증거 (영률만 다른 실험이 아니다) · 크롭 `fig_1a` · `fig_1b` |
| 2 | 장치 개요 — X 선 선원 · PEEK · 스테인리스 막대 · 검출기 · 아래에서 가압 · 회전 | 누른 채 CT · EIS 셀의 꼴 |
| 3 | FEM 경계 — 위 고정 (가상판) · 옆면 roller · 아래 400 MPa · 회색 원통 + 검은 입자 (어느 시료인지 [미확인]) | 우리 MPM · DEM 다이 경계 (마찰 없는 벽) 와 같은 꼴 |
| 4 | ★ 순수 Li₅.₅PS₄.₅Br₁.₅ σ(P) (0–400 MPa · 로그 0.1–10 mS/cm · 선만) | 포화 ≈300 MPa · §3-2 |
| 5 (a · b) | ★ 나일론 / 지르코니아 복합체 σ(P) (표지 + 맞춤 곡선) | 결과 전 대조 항목 후보 (방향) · §3-3 · §3-5 |
| 6 | ★ 포화 압력 막대 (나일론 250 × 3 · 지르코니아 350 · > 400 · > 400) | 영률 · 분율 → 포화 압력 이동 · §3-4 |
| 7 (a · b) | 3D MPS 지도 (복합체 → SE + 빈틈 → 대리 · 0–800 MPa) 나일론 29 % · 지르코니아 22 % | 단단한 상이 붉다 — 그림 한 장 요약 · 크롭 `fig_7a` · `fig_7b` |
| 8 (a · b) | ★ 상별 평균 MPS vs 분율 (점선 = 인가 400 MPa) | **AM 하중 몫 (R1)** 의 탄성 연속체 값 · §3-6 |
| 표 1 | E · ν (SE 25.3 · 0.35 · 지르코니아 200.0 · 0.30 · 나일론 2.0 · 0.30) | 구성 입력 전부 (식 대신 이 표) · CL-90 대조 |
| 근거 문단 19 장 | `txt_p2_*` (약어 · 정의 · 목적 · 합성 · 셀 · 대리 영률) · `txt_p2_p3_*` (EIS) · `txt_p3_*` (CT · VOXELCON · 400 MPa CT · 물성 가정 · 경계 · 수송 계산 생략) · `txt_p4_*` (순수 SE · 포화 정의 · 소성 · 복합체 순서 · 200 / 400 MPa 비교) · `txt_p4_p5_*` (포화 순서 · 상관) · `txt_p5_*` (그림 7 · 8 서술) · `txt_p5_p6_*` (분율 경향 · 연속체) · `txt_p6_*` (HYA 보호 · LYA / HYA 기전) · `txt_p6_p7_conclusions` | 원문 인용용 |
| 식 | **없음** — 원문에 번호 매긴 식이 하나도 없다 (구성 = 표 1 · 경계 = p.3 문장 · 그림 3) | 보고서 MPM 절에는 표 1 · 그림 3 · 경계 문단 크롭을 붙인다 |

## 6. Post-processing ★
- **원문이 한 것**: EIS → σ (기하 미인쇄) · CT 복셀 세기 → AM 부피 분율 · 복셀 FEM → MPS 지도 · 상별 평균 · σ(P) 에서 포화 압력 '대략' 읽기.
- **안 한 것**: 기공률 · 상대밀도 · 진밀도 · tortuosity · 접촉 면적 · 응력 히스토그램 · E_SE 민감도 (2020 논문의 0.3 GPa 극단 같은 것) · 해상도 · 격자 수렴 · 반복 측정 · 오차 막대 · 탈압 · 같은 분율 짝 · 이온 수송 계산.
- **이 카드의 후처리**: 벡터 경로 판독 (그림 4 곡선 · 그림 5 표지 51 · 맞춤 곡선 · 그림 6 막대) · 원 래스터 색 원판 무게중심 (그림 8 · 눈금선 조각선형 · 점선 점검) · 평균 응력 정리 한계 · Voigt / Reuss · 같은 압력 비 f · Bruggeman 대조 · 겉보기 tau2 · 상 평균 국소 응력 점검 · 2020 논문과 나란히 — 판독 원자료 `digitized.csv` (133 행 · method 칸에 방법).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · `comparison_vs_ours_DEM.md` 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 재료 | Li₅.₅PS₄.₅Br₁.₅ + 지르코니아 / 나일론 (대리 · ≈50 µm) | LPSCl + NCM811 (AM_P · AM_S 두 크기) | 재료 · 대리 다름 — 꼴만 |
| 압력 · 상태 | 0 → ≈400 MPa · 누른 채 · 가압만 · FEM = 400 MPa 한 상태 | 300 MPa 가압 → 판 고정 이완 (DEM) · MPM 서보 / hold · 언로딩 키트 진행 | 같은 '누른 채' · 이 논문은 압밀 과정을 계산하지 않는다 |
| 하중 몫 | 지르코니아 [0.43, 0.45] → [0.77, 0.78] (22 → 52 vol% · 탄성 연속체) | DEM AM–AM 0.517 · 0.598 · 0.675 · 0.620 · 상별 virial 0.726 · 0.768 · 0.794 · 0.763 (100 · 200 · 300 · 600 MPa · CLAUDE.md 실측 4 점) · MPM = AM 얼림 → 0 | 같은 이름 · 다른 양 (§7-3) |
| E 대비 | 7.9 (200 / 25.3) · 0.079 (2 / 25.3) | DEM ≈104 (140 / 1.35) · 실제 NCM811 ÷ LPSCl ≈6 (138 ± 24 [다른 카드 sedlatschek2026] ÷ DFT 22.06 [우리]) [카드 산술] | 이 논문의 지르코니아 대비 (7.9) 는 **실제 재료 대비** 쪽에 가깝고 우리 DEM 의 연화 대비와는 13 배 다르다 |
| SE 구성 | 선형 탄성 25.3 GPa (치밀 결정 DFT) · 빈틈 품은 한 상 | DEM E_eff 1.35 GPa (18 배 연화) · MPM E 1.53 · σ_y 0.30 · ν 0.49 (J2) | frame [2] 의 다른 층 (§7-4) |
| 수송 | 실측 σ(P) (EIS) · 계산 없음 | 접촉망 Kirchhoff/Holm (DEM) · STEP3 복셀 FV (MPM) | 실측 경향 (방향) 만 대조 |
| 기공 | 없음 | 랩 표준 10–13 % (순수 SE · 300 MPa) · real_14 ≈15.6 % | 견줄 것 없음 (§7-2) |
| 탈압 | 없음 | DEM 언로딩 키트 · MPM 제하 없음 | — |

### 7-2. ★ 랩 기준과 나란히 (판정 없이)
| 출처 | 재료 | 압력 · 상태 | 진밀도 분모 | 기공 |
|---|---|---|---|---|
| **랩 표준** | LPSCl (순수 SE) | 300 MPa | **1.64** (고정) | **10–13 %** |
| 이 논문 | Li₅.₅PS₄.₅Br₁.₅ (순수 · 복합) | 0–≈400 MPa · 누른 채 | **없음** | **없음** (숫자 미인쇄 · CT 는 AM 분율만) |
- 이 논문으로는 **"랩 표준과 다른 문헌 값"** 자리도 채울 수 없다 — 기공 · 밀도 숫자가 하나도 없다.  순수 SE σ 포화 (≈300 MPa) 는 압밀이 끝나 가는 압력의 **간접 표지** 일 뿐 기공률이 아니다.

### 7-3. ★ AM 하중 몫 (MPM DO-NOT ② · R1) — 연속체 탄성 기준선, 두 번째 점
- **주는 것**: 결합 · 선형 탄성 · 400 MPa 에서 **지르코니아 (E 대비 7.9) 의 축하중 몫 [0.43, 0.45] · [0.64, 0.68] · [0.77, 0.78] (22 · 39 · 52 vol%) · SE 평균 응력 = 인가압의 0.73 · 0.585 · 0.49** [판독 · 카드 산술].  같은 그룹 2020 논문 (ZrO₂ · E 대비 9.2 · 100 MPa) 의 ≥ 0.29 · 0.62 · 0.73 · 0.84 [다른 카드] 와 함께 **'단단한 상이 분율과 함께 하중을 더 진다'** 의 연속체 점이 두 벌이 된다.
- 우리 MPM 의 문제 (AM 을 얼려 판 반력에 AM 몫 0 → SE 가 100 % 를 져 과압축: R1 ε_sphere 1.13 % ↔ 실험 15.6 % · CLAUDE.md DO-NOT) 의 방향을 문헌 계산이 다시 받친다 — 단단한 상이 연속체로 하중을 나누면 SE 평균 응력은 인가압 아래로 내려간다 (이 논문 범위 22–52 vol% 에서 0.73–0.49 배 · 우리 침대의 값을 예측하는 숫자가 아니다 · 후보 A · A′ 에서 볼 방향).
- 우리 DEM 과 숫자 [카드 산술 · 같은 양 아님]: 우리 침대 φ_AM ≈0.62 (전체 부피 기준 · ohashi2020 카드와 같은 셈) 는 이 논문 지르코니아 최대 52 % **밖** → 보간 · 외삽하지 않는다 · 52 % 의 [0.77, 0.78] 이 우리 DEM 300 MPa 상별 virial 0.794 · AM–AM 0.675 옆에 있다는 것 **이상을 말하지 않는다** — 양 (MPS 로 묶은 축응력 몫 ↔ 접촉망 · virial) · 모델 (결합 탄성 연속체 ↔ 연화 강구 접촉망) · 재료 · E 대비 (7.9 ↔ 104) · 압력 (400 ↔ 300) · 기공 (SE 상에 묻음 ↔ ≈15 %) 이 다 다르다 (frame [4] — 서로 맞춘 것이 아니다 → 교차검증으로 인용하지 않는다).
- 나일론 (E 대비 0.079) 쪽은 우리 계에 없는 경우 (NCM 은 LPSCl 보다 단단하다) — 바인더 · 고분자 첨가제 쪽 감각으로만 (원문도 *"can be extended to the presence of binders or conductive additives"*, p.6).

### 7-4. E 축 (frame [2]) — 25.3 GPa 는 어느 층인가 · HYA / LYA 구분은 E_SE 선택에 달린다
- 표 1 의 SE 25.3 GPa = Li₆PS₅Br 의 0 K DFT (Deng 2016) — frame [2] 의 **실제 bulk 층** (우리 DFT LPSCl E_VRH 22.06 · Deng LPSCl 22.1) 이다.  우리 DEM 1.35 GPa (재배열 대리로 18 배 연화) · MPM 1.53 GPa (ν 0.49 · K 25.5) 와는 다른 층이다.
- ⚠ **HYA / LYA 구분은 E_SE 를 무엇으로 두느냐에 달린다** [카드 추론 · 다른 카드]: 같은 그룹이 잰 압분체의 겉보기 강성은 훨씬 낮다 — kodama2020 Li₆PS₅Br 가압 할선 *"25 MPa to 250 MPa"* · ohashi2020 LGPS 압분체 0.3 GPa [다른 카드].  그 값들에 견주면 나일론 (2 GPa) 은 **SE 압분체보다 단단하다** → '나일론 복합체에서 응력이 SE 로 몰린다' 는 FEM 결론은 E_SE 25.3 이라는 선택에 묶여 있다 (원문은 E_SE 한 값만 계산).  실측 (나일론 복합체의 낮은 포화 압력 · 200 MPa 의 높은 σ) 은 그 FEM 해석과 같은 방향이지만, 나일론이 **모양 · 소성** 도 다르므로 증거로는 약하다.
- 우리 쪽 의미 [카드 추론]: 우리 DEM 의 대비 (≈104) 는 이 논문 지르코니아 (7.9) 보다 훨씬 커 — 이 논문의 방향을 따르면 — SE 가 더 가려진다.  우리 복합체 SE 겹침 1.75 % ↔ 순수 SE 11–12 % (CLAUDE.md 2026-06-06 'AM 하중 차폐') 가 같은 방향의 우리 관측이다 (같은 양 아님).

### 7-5. 수송 (σ_ion) — 단단한 AM 의 벌점 · 포화 압력 이동
- 실측 방향 셋: ① 같은 압력에서 단단한 대리는 SE σ 에 벌점 (200 MPa: 분율이 7–22 %p 더 큰 나일론과 같거나 낮다) ② 포화 압력 ↑ (지르코니아 22 % ≈350 · 39 / 52 % > 400 ↔ 순수 ≈300 ↔ 나일론 ≈250) ③ 포화 위 (≈400 MPa) 에선 차이가 표지 흩어짐 안으로 줄어든다 (22 % 지르코니아 ÷ 29 % 나일론 = 1.02).
- 우리 접촉망 σ_ionic 은 SE 접촉 면적 (Hertz / Tabor) 과 SE 망 기하를 보고 AM 강성은 겹침 (SE 압축 정도) 을 통해서만 들어온다 — '단단한 AM 이 SE 를 덜 다지게 해 σ 를 낮춘다' 는 이 논문의 기전은 우리 DEM 에서는 **SE–SE 겹침 · 면적 감소** 로 나타나야 할 방향이다 [카드 추론] · 크기 대조는 하지 않는다 (대리 · 재료 · E 대비 다름).
- 겉보기 tau2_app 1.1–2.9 (400 MPa · §3-7) 는 우리 수송 tortuosity (tau2 = φ_SE · σ₀ / σ_eff · 기준 σ₀ 고정) 와 **같은 양이 아니다** — 기준이 '같은 인가압의 순수 SE σ' 라 SE 상태 차이가 분모에 섞인다.

### 7-6. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 실측 σ(P) (두 영률 대리 · 여섯 분율) · 400 MPa 형상의 상별 **탄성 응력** (계산).
- **없는 것**: 압밀 역학 (DEM · MPM · 소성 · 접촉 · 미끄럼 · 파쇄) · 기공 · 접촉 수 · 면적 · 수송 계산 · 탈압.  ⇒ MPM / 역학 쪽에 '단단한 AM 이 하중을 나눠 진다' 의 탄성 기준선을, DEM / 수송 쪽에 '단단한 AM → SE σ 벌점 · 포화 압력 ↑' 의 실측 방향을 준다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | (1) CT 부피 분율 = 복셀 세기 · 'SE' 상이 해상도 아래 빈틈을 품는다 → 5 µm 급 CT 로는 **AM 분율만** 확실하고 기공은 셀 수 없다 (연산자 등록에 '해상도 아래는 어느 상에 넣었나' 칸) (2) ★ 상별 평균 MPS 로 하중 몫의 **아래 · 위 한계** 를 내는 관측량 정의 (§3-6) — 우리 DEM · MPM 출력에도 같은 식으로 셀 수 있다 · Σ φ·MPS ÷ P ≥ 1 이 판독 · 출력 일관 점검 | 기공 숫자 · 진밀도 · 문턱 |
| **단계 1** (3D 메모리 · 장 수) | ≈300³ (2.7 × 10⁷) 복셀 선형 탄성 한 번 · GPU (2020 년) [카드 산술] — 크기 감각 | 메모리 · 시간 [미확인] · 다물체 장 아님 |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | 결합 연속체 (= 한 속도장 · 분리 없음) 가 결론을 만드는 자리를 원문이 스스로 적었다 — *"Because nylon and SE are continuous in a FEM, the increase in the strain of the SE induces an increase in the strain of an adjacent nylon"* (p.6) → 단계 3 에서 '한 속도장 ↔ 입자별 장' 이 **무른 상의 응력** 을 얼마나 바꾸는지 재면 이 문장의 크기를 가른다 [카드 추론] | 2D 계산 · 수치 없음 |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 순수 Li₅.₅PS₄.₅Br₁.₅ σ(P) 포화 ≈300 MPa (400 MPa σ 의 87 % 가 300 MPa 까지) — 압밀이 끝나 가는 압력대의 간접 표지 | 맞춤 표적 아님 (기공 없음 · 재료 다름) — 랩 표준이 표적 |
| **단계 5** (3D 복합 압밀) | ★ 결과 전 대조 항목: 'SE 평균 축응력 ÷ 인가압 vs 단단한 상 분율' 탄성 연속체 세 점 (E 대비 7.9) + 2020 논문 네 점 (9.2) · '포화 압력이 단단한 상 분율과 함께 오른다' 의 실측 방향 · 같은 압력 σ 벌점의 크기 (200 MPa f/Bruggeman 0.41–0.80) | 대리 · 탄성 · 400 MPa 한 상태 · 우리 φ_AM ≈0.62 는 범위 밖 |
| **단계 6** (탈압 · 되돌아옴) | 없음 | — |
| **단계 7** (형상 · 피복 · 수송) | 실측 σ(P) 두 벌 (영률 둘 · 분율 셋) · 낮은 압력 (≈100 MPa) 에서 복합체가 순수 SE 의 0.12–0.17 뿐이라는 '늦은 시작' (§3-7) | 수송 계산 · tortuosity 숫자 없음 |
| **후보 D0** (지금 DEM) | 방향 점검: 단단한 AM → SE 차폐 (우리 SE 겹침 1.75 ↔ 11–12 %) 와 같은 방향 | 크기 대조 불가 (E 대비 104 ↔ 7.9) |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 경계 = 고정판 · 하중판 + **마찰 없는 옆벽 (roller)** · *"same as that in the experiment"* — 우리 다이 경계와 같은 꼴 (벽 마찰 0) | 벽 마찰 · AM–SE 미끄럼 없음 |
| **후보 A** (MPM 강체 AM · SE 한 속도장) | ★ 강체에 가까운 AM (E 대비 7.9) 이 움직이고 결합되면 SE 몫이 인가압의 0.49–0.73 — 후보 A 의 첫 결과를 놓을 기준선 (방향 · 자릿수) | 강체 아님 · 결합 · 접촉 없음 |
| **후보 A′** (입자별 속도장 · 마찰 접촉) | 이 논문이 **못 한** 것 = 분리 · 미끄럼 — 결합 가정이 무른 상 응력을 올리는 사슬 (p.6) 을 A′ 가 시험할 수 있다 | — |
| **후보 B** (입자별 FE + 접촉) | 영상 기반 복셀 FEM 의 선례 (메시 없이 CT 그대로) · 비용 감각 | 입자별 · 접촉 · 소성 아님 |
| **후보 C · C′** (MDR · 항복 캡 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀) | ★ '유효 SE 압력 κ = P_SE / P' 를 균질화 보정으로 쓸 수 있는지의 시험 거리: FEM κ (지르코니아 22 % 0.73 · 나일론 29 / 61 / 75 % 1.37 / 2.14 / 2.30) ↔ 포화 압력 비로 본 κ (300/350 = 0.86 · 300/250 = 1.20 — 나일론 세 분율 같음) [카드 산술] — 방향은 같고 FEM 의 κ 가 1 에서 더 멀다 (지르코니아 0.27 ↔ 0.14 · 나일론 0.37–1.30 ↔ 0.20) | 포화 압력이 '대략' 값 · 정의 둘 · 39 / 52 % 는 '> 400' 이라 비를 못 낸다 |
| **U0–U6** | U1 (입자 지름당 셀 수): 대리 50 µm = 10 복셀 (8.3 · 6 µm 축) · SE 입자는 안 풀림 — 해상도 규칙의 근거 문장은 아님 (원문은 해상도 시험을 하지 않았다) | 수렴 시험 없음 |
| **R1–R7** | **R1** ★ 탄성 연속체 하중 몫 (§3-6) · **R5** 맞춘 값 0 (물성 빌림) · **R7** 정성만 — *"its mechanical tolerance against compression may be a limiting factor in fabrication"* · *"increasing the volumetric fraction of HYA in an electrode could protect the HYA from overloading"* (p.6) | R2 (미끄럼 · 분리) · R3 · R4 · R6 없음 |
| **결과 전 대조 항목** | (a) SE 평균 MPS ÷ 인가 · AM 몫 [아래, 위] vs φ_AM (지르코니아 세 점 · 나일론 세 점) (b) σ_복합 / σ_SE(P) vs P — 단단한 대리 벌점이 포화 위에서 줄어드는 꼴 (c) 포화 압력 순서 (나일론 < 순수 < 지르코니아 · 지르코니아 분율 ↑ → ↑) — 전부 '대리 · Li₅.₅PS₄.₅Br₁.₅ · 25 °C · 누른 채 · 가압만 · 탄성 계산' 표지 | 절대값 대조 금지 |

- **재료 · 차원 · 조건 차이**: Li₅.₅PS₄.₅Br₁.₅ ↔ LPSCl · 대리 (지르코니아 · 나일론 ≈50 µm) ↔ NCM811 (AM_P · AM_S) · 400 ↔ 300 MPa · 3D = 같음 · 누른 채 = 같음 · 탄성 계산 ↔ 우리 압밀 계산.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **하중 몫은 한계 둘로 보고한다** — 상별 평균 MPS 만 있어도 평균 응력 정리로 [1 − (1 − φ)⟨MPS⟩_SE / P, φ⟨MPS⟩_AM / P] 가 나온다 (이 논문 22 % 지르코니아 폭 0.02) — 우리 MPM 에서 AM 이 하중을 지게 한 뒤 (후보 A · A′) 같은 두 숫자를 내면 DEM 의 AM–AM · 상별 virial 과 **같은 축 위에** 놓인다 (단계 0 · 5 · R1).
2. **영률만 바꾸는 시험은 모양 · 크기 · 소성을 묶어 둔다** — 이 논문의 두 대리는 모양 (불규칙 ↔ 구) · 소성이 같이 달라 '영률 효과' 를 가르지 못했다 → 우리 DEM / MPM 에서 AM 영률 민감도를 돌릴 때는 같은 침대 · 같은 PSD 에서 E 하나만 (단계 3 · 4 · 5).
3. **E_SE 선택이 '어느 상이 단단한가' 를 정한다** — 치밀 결정 25.3 GPa 면 나일론 2 GPa 가 '무르고', 압분체 0.3 GPa 면 '단단하다' (§7-4) → 우리 DEM 의 SE (1.35 · 18 배 연화) 와 AM (140 GPa 입력 · CL-90 = 출처 철회 · 값은 측정 범위 안) 의 대비 (≈104) 는 실제 재료 대비 (NMC811 138 ÷ LPSCl 22.06 ≈ 6.3) 의 ≈17 배 · 이 논문 지르코니아 대비 (7.9) 의 ≈13 배 [카드 산술] — 하중 몫 · 차폐를 문헌 연속체 값과 견줄 때 대비부터 병기 (frame [2]).
4. **포화 압력 이동을 실측 표적으로** — 단단한 AM 분율 ↑ → 포화 압력 ↑ (350 → > 400 MPa) 은 우리 DEM σ_ionic(P) 사다리 (100–600 MPa) 에서 '포화가 늦어지는가' 로 바로 볼 수 있는 방향 표적 (크기 대조 금지 · 대리).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In a linear-elastic voxel FEM of an X-ray CT volume compacted at 400 MPa, the stiffer phase carries more than the applied pressure on average: zirconia (200 GPa) in a Li₅.₅PS₄.₅Br₁.₅ (25.3 GPa assumed) composite averages ≈600–815 MPa minimum principal stress while the solid electrolyte averages ≈200–290 MPa at 22–52 vol% zirconia (digitized from Ohashi et al., J. Power Sources 483 (2021) 229212, Fig. 8b)."
- "With 200 GPa zirconia as an active-material stand-in, the ionic conductivity of Li₅.₅PS₄.₅Br₁.₅ composites saturates only above ≈350 MPa (22 vol%) or not within 400 MPa (39 and 52 vol%), versus ≈300 MPa for the pure electrolyte and ≈250 MPa with 2 GPa nylon (Ohashi et al. 2021, Fig. 6; approximate values as stated by the authors)."
- 국문: *"단단한 활물질 대리 (지르코니아) 는 결합 탄성 계산에서 인가압의 1.5–2.0 배를 지고 SE 는 0.49–0.73 배를 진다 (22–52 vol% · 400 MPa · Ohashi 2021 판독) — 응력은 계산값이며 기공 · 소성 · 탈압은 없다."*
- 국문: *"Ohashi 2021 의 '영률 효과' 는 모양 · 소성도 다른 두 대리 (구 ↔ 불규칙 고분자) 의 비교다 — 영률만의 효과로 인용하지 않는다."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **응력은 계산값** — 측정이 아니다 · 선형 탄성 · 결합 · 400 MPa 한 상태 · E_SE 한 값 (치밀 결정 DFT) — 응력 비는 인가압에 무관한 꼴 (선형) 인데 실제 압밀은 비선형 · 소성 (원문 p.4 가 스스로 적음).
2. **대리 둘은 영률만 다르지 않다** — 모양 (Fig 1) · 고분자 소성 · 밀도 · 표면 — '영률' 로 돌린 것은 해석.
3. **같은 분율의 짝이 없다** — 결론 1 의 'equivalent volumetric fraction' 은 추론.
4. **포화 압력** — 정의 둘 · *"approximated values"* · 나일론 분율 차이 *"indistinguishable"*.
5. **400 MPa 의 '지르코니아 22 % > 나일론 29 %'** 는 1.6–1.8 % 차 — 표지 흩어짐 (±2 %) 안 [판독 · 카드 산술].
6. **E_SE 선택에 묶인 LYA 해석** — 압분체 강성 (같은 그룹 kodama2020 · ohashi2020 [다른 카드]) 으로 보면 나일론도 SE 보다 단단하다 (§7-4).
7. **기공 · 밀도 · 시료 치수 · σ 환산 기하 · 반복 · 오차 막대 · SE 입경 없음**.
8. **수송 계산 없음** — 응력 → σ 연결은 서술 (*"nanoscale features continue to exist"*) 뿐 · 이 카드의 상 평균 점검 (§3-8) 은 지르코니아만 10–20 % 안 · 나일론 61–75 % 는 안 맞는다.
9. **셀 표기 어긋남** — '450 MPa 셀 = [19] 의 셀' ↔ [19] 의 ≈100 MPa 한계 (§3-11).
10. **참고문헌 품질** — [10] 저자 잘림 · [20] 학술지 이름 없음 · [7] (LCO 논문) 에 넷의 영률.
11. **E · ν 출처** — 지르코니아 · 나일론 · 그 ν 는 출처 없음 · SE 값은 다른 조성 (Li₆PS₅Br) 의 DFT.
12. ⚠ **판독 값** — 그림 4 · 5 · 6 은 벡터 좌표 (그림 자체에 정확) · 그림 8 은 ±3 MPa — 그래도 [판독] 표지로만 인용.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 17 | A. Ohashi, M. Kodama, S. Xueying, S. Hori, K. Suzuki, R. Kanno, S. Hirai, Stress distribution in the composite electrodes of sulfide all-solid-state lithium-ion batteries, J. Power Sources 470 (2020) 228437, https://doi.org/10.1016/j.jpowsour.2020.228437. | 같은 그룹 앞 판 (LGPS + ZrO₂ · 응력 → 국소 σ) · *"they correspond with the results obtained in a previous study [17]"* (p.5) | `ohashi2020_stress_distribution_composite_electrode_sulfide_assb` |
| 19 | M. Kodama, S. Komiyama, A. Ohashi, N. Horikawa, K. Kawamura, S. Hirai, High-pressure in situ X-ray computed tomography and numerical simulation of sulfide solid electrolyte, J. Power Sources 462 (2020) 228160, https://doi.org/10.1016/j.jpowsour.2020.228160. | 셀 · σ 상승 기전 · 포화 기전 *"already been clarified [19]"* | `kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation` |
| 21 | Z. Deng, Z. Wang, I.-H. Chu, J. Luo, S.P. Ong, Elastic properties of alkali superionic conductor electrolytes from first principles calculations, J. Electrochem. Soc. 163 (2016) A67–A74, https://doi.org/10.1149/2.0061602jes. | E_SE 25.3 · ν 0.35 · '20–30 GPa' | `deng2016_elastic_superionic_electrolytes_dft` |
| 24 | M. Kodama, A. Ohashi, S. Hirai, In situ X-ray computational tomography measurement of single particle behavior of sulfide solid electrolyte under high- pressure compression, J. Power Sources Adv. 4 (2020) 100019, https://doi.org/10.1016/j.powera.2020.100019. | 입자 **안** 빈틈 감소 근거 [19,24] · 단일 SE 입자 고압 거동 (질문 a · c · l) | 없음 (papers/ ls · grep "100019") |
| 7 | E.J. Cheng, N.J. Taylor, J. Wolfenstine, J. Sakamoto, Elastic properties of lithium cobalt oxide (LiCoO 2 ), J. Asian Ceram. Soc. 5 (2017) 113–117, https://doi.org/10.1016/j.jascer.2017.03.001. | LCO · Si · Sn · 흑연 190 · 185 · 50 · 20 GPa 의 근거 (LCO 논문 하나) | 없음 (2020 카드 정독 n 줄에 이미 있음) |
| 18 | C. Yu, Y. Li, W. Li, K.R. Adair, F. Zhao, M. Willans, J. Liang, Y. Zhao, C. Wang, S. Deng, R. Li, H. Huang, S. Lu, T.-K. Sham, Y. Huang, X. Sun, Enabling ultrafast ionic conductivity in Br-based lithium argyrodite electrolytes for solid-state batteries with different anodes, Energy Storage Mater 30 (2020) 238–249. | SE 처방 · 400 MPa σ 가 *"roughly corresponds"* 한 문헌 값 | 없음 |
| 22 | A. Sakuda, Favorable composite electrodes for all-solid-state batteries, J. Ceram. Soc. Japan. 126 (2018) 675–683, https://doi.org/10.2109/jcersj2.18114. | 복합 전극 σ–압력 곡선 (*"similar to that of many of reported curves [19,22,23]"*) | 없음 |
| 23 | J.M. Doux, Y. Yang, D.H.S. Tan, H. Nguyen, E.A. Wu, X. Wang, A. Banerjee, Y. S. Meng, Pressure effects on sulfide electrolytes for all solid-state batteries, J. Mater. Chem. A. 8 (2020) 5049–5055, https://doi.org/10.1039/c9ta12889a. | σ–압력 곡선 (같은 문장) | `doux2020_pressure_effects_sulfide_se_jmca` |
| 25 | G. Bucci, T. Swamy, S. Bishop, B.W. Sheldon, Y.-M. Chiang, W.C. Carter, The effect of stress on battery-electrode capacity, J. Electrochem. Soc. 164 (2017) A645–A654, https://doi.org/10.1149/2.0371704jes. | 활물질 압축 → 용량 감소 (p.6) | 없음 (`bucci2017_chemomech_failure_assb_cycling_czm` 은 JMCA 판 · 다른 논문 · 2020 카드 정독 n 줄에 있음) |
| 26 | A. Sakuda, A. Hayashi, M. Tatsumisago, Recent progress on interface formation in all-solid-state batteries, Curr. Opin. Electrochem. 6 (2017) 108–114, https://doi.org/10.1016/j.coelec.2017.10.008. | 상온 가압 소결 · 포화 압력 상승을 제조에서 고려해야 한다는 근거 | 없음 |
| 20 | Y. Nagano, Y. Ikeda, H. Kawamoto, N. Takano, Image-based modeling by 3-D CT for homogenization stress analysis - application to porous ceramics -. https://doi.org/10.11396/jjsndi.53.701, 2004, 53, 701-708. | VOXELCON · 영상 기반 응력 해석의 방법 원전 (학술지 이름 없음) | 없음 (2020 카드 정독 n 줄에 있음) |
| 12 | A. Sakuda, A. Hayashi, M. Tatsumisago, Sulfide solid electrolyte with favorable mechanical property for all-solid-state lithium battery, Sci. Rep. 3 (2013) 2–6, https://doi.org/10.1038/srep02261. | 압축이 접촉 · σ 를 좋게 한다 (서론) | `sakuda2013_sulfide_mechanical_property` |
| 13 | A. Bielefeld, D.A. Weber, J. Janek, Modeling effective ionic conductivity and binder influence in composite cathodes for all-solid-state batteries, ACS Appl. Mater. Interfaces 12 (2020) 12821–12833, https://doi.org/10.1021/acsami.9b22788. | 활물질 부피가 이온 전도를 막는다 (서론) | `bielefeld2020_effective_ionic_conductivity_binder` |
| 14 | D. Hlushkou, A.E. Reising, N. Kaiser, S. Spannenberger, S. Schlabach, Y. Kato, B. Roling, U. Tallarek, The influence of void space on ion transport in a composite cathode for all-solid-state batteries, J. Power Sources 396 (2018) 363–370, https://doi.org/10.1016/j.jpowsour.2018.06.041. | 같은 문장 (서론) | `hlushkou2018_void_space_ion_transport_assb_cathode` |
| 15 | R. Koerver, W. Zhang, L. De Biasi, S. Schweidler, A.O. Kondrakov, S. Kolling, T. Brezesinski, P. Hartmann, W.G. Zeier, J. Janek, Chemo-mechanical expansion of lithium electrode materials-on the route to mechanically optimized all-solid-state batteries, Energy Environ. Sci. 11 (2018) 2142–2158, https://doi.org/10.1039/c8ee00907d. | 역학–구조 ↔ 이온 전도 (서론) | `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` |
| 10 | A. Hayashi, M. Tatsumisago, Mechanical properties of sulfide glasses in all-solid-state batteries, J. Ceram. Soc. Japan. (2018) 719–727. | 접촉 유지 과제 (서론) · ⚠ 저자 잘림 · 권 없음 (§3-11) | 없음 (2020 카드 정독 n 줄에 Kato 외 판으로 있음) |

---

## [미확인] 목록
- 저자 이름 전체 · SE 입경 · 형상 · XRD · 원료 비 · 지르코니아 · 나일론 공급처 · 등급 · 나일론 종류 · 대리의 E · ν 출처.
- 시료 질량 · 지름 · 두께 · 질량 분율 · 진밀도 · 기공률 · 상대밀도.
- EIS 등가회로 · σ 환산 기하 · 단계 유지 시간 · 가압 속도 · 반복 수 · 450 MPa 까지 눌렀는지 · 첫 표지 아래 압력의 값.
- CT 투영 수 · 재구성 · 이진화 문턱 · 6 µm 축의 방향 · 다른 압력의 CT 유무 · 그림 3 시료.
- FEM 요소 · 풀이기 · 수렴 · 시간 · 메모리 · GPU · ≈300³ 이 시야의 어느 부분인지 · CT 빈틈을 따로 두었는지 · '평균' 이 부피 평균인지.
- 포화 압력 판정 방법 (축 · 문턱) · 그림 4 곡선 · 그림 5 맞춤 곡선의 함수꼴 · Yu 2020 의 σ 값.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-17)
- 서지: 1저자 메모 (A. Ohashi · M. Kodama\* · N. Horikawa · S. Hirai (Tokyo Institute of Technology) · 제목 · J. Power Sources 483 (2021) 229212 · 하이라이트 다섯) = 원문 첫 쪽 · 머리글 · PDF 메타데이터 (subject *"Journal of Power Sources, 483 (2021) 229212. doi:10.1016/j.jpowsour.2020.229212"*) 와 같음 · DOI 첫 쪽에서 읽음.  SI · 부록 · 그래픽 초록 없음 (7 쪽 · 첫 쪽 래스터 셋 = 출판사 로고 · 표지 · 업데이트 표시).
- 숫자: 텍스트 층 + 7 쪽 렌더로 대조 — 3 g · 50 ml · 0.2 ml · 16 · φ10 mm · 1200 rpm · 10 h · 400 °C · 10 h · 450 MPa · ≈50 μm · 190 · 185 · 50 · 20 GPa · 200 · 2 GPa · 1 MHz–1 Hz · 25 °C · 160 kV · 70 μA · 25 mm · 1000 mm · 5 × 5 × 6 μm · 5.12 × 5.12 × 6.14 mm · 300 × 300 × 300 · 400 MPa · 20–30 GPa · 표 1 여섯 값 · 300 · 250 · 350 · > 400 MPa · 29 · 61 · 75 · 22 · 39 · 52 % · 200 · 400 MPa (비교 문장) · ≈400 · ≈200 · ≈300 · ≈600 MPa (그림 7 서술) — 전부 위치 확인.
- 낱말 전수: 'porosity' 0 · 'density' = energy density 뿐 · 'plastic' 1 (p.4) · 'unload' · 'decompress' · 'release' 0 · 'DEM' 0 (걸린 2 개는 'demonstrate') · 'friction' 0 · '2D' 0 · 'Eq.' 0 · 'supplementary' 0.
- 판독 점검: 그림 4 · 5 의 로그축 '1' 글자 중심 = 틀 한가운데 (차 < 0.02 pt) · 그림 6 막대 윗변 = 눈금 (250.2 · 350.5 · 400.0) · 그림 8 점의 x = 표시 분율 (28.8 / 60.8 / 74.7 · 22.2 / 39.2 / 52.1) · 점선 398.9 · 400.0 MPa · Σ φ·MPS ÷ 400 = 1.01–1.12 (평균 응력 정리와 맞는 방향).
- 정본 중복 확인: `git ls-tree` papers/ 목록 (ohashi* · kodama* 확인) · '229212' · 'Horikawa' · 제목 낱말 grep — 카드 없음 (sakka2022 의 인용 · kodama2020 의 저자 줄뿐) · 같은 그룹 2020 카드 (`ohashi2020_…`) 는 다른 논문 (470 권 228437).

## 🔗 관련 카드
- 같은 그룹: `ohashi2020_stress_distribution_composite_electrode_sulfide_assb` (이 논문 [17] · LGPS + ZrO₂ · 응력 → 국소 σ) · `kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation` (이 논문 [19] · 셀 · 순수 SE in situ CT).
- 이 논문을 인용한 카드: `sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps` (ref 25 · *"large pressures can be applied to materials that have larger Young's moduli"*).
- 복합체 응력 · 하중 몫: `park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics` (XCT 2D 선형 탄성) · `jeong2024_operando_densification_chemomechanics_se_size_composite_cathode` (선형 탄성 메조 모델 · E_AM 200 GPa) · `martinbouvard2003_dem_composite_cold_compaction` (DEM 경질–연질 힘비 — 다른 양).
- 탄성 상수: `deng2016_elastic_superionic_electrolytes_dft` · `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` (NMC811 138 ± 24 GPa) · `stallard2022_cathode_mechanical_properties_review`.
- 압밀 · σ(P): `doux2020_pressure_effects_sulfide_se_jmca` · `sakuda2013_sulfide_mechanical_property` · `heck2026_densification_sulfide_se_binder_scalable` · `miss2026_insitu_conductivity_porosity_pressure_compaction`.
- 활물질 부피 · 바인더 → 이온 전도: `bielefeld2020_effective_ionic_conductivity_binder` · `hlushkou2018_void_space_ion_transport_assb_cathode`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
