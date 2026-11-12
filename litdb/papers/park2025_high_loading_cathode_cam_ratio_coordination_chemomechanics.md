<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 1저자 11-12 후보 여덟 편의 6 번 · 후보 표 N-6) 에서 꼭 뽑으라고 한 항목.
     본 = stavola2023_thick_nmc111_lpscl_lithiation_gradient_tortuosity.md (XCT · 복합 양극 카드의 꼴) · jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (같은 Hatzell–Mukherjee 그룹 · 같은 묶음 · 절 번호 체계).
     두 필수 절 (§0-1 고른 의도 대조 · §8 자세한 분석) 은 같은 묶음의 jeong2024 · doux2020_pressure_effects_sulfide_se_jmca · mcgrogan2017 카드와 같은 꼴.
     원문 = 출판본 (ACS Nano 2025, 19 (24), 22262–22269 · 8 쪽 · © ACS — 열린 이용 표기 없음) + Supporting Information (5 쪽 PDF = 표지 1 + 그림 S1–S4).
     쪽 표기 = 본문은 PDF 쪽 "p.n" (인쇄 쪽 = 22261 + n · p.1 = 22262 … p.8 = 22269).  SI 는 "SI p.n" = SI PDF 쪽 n (SI p.1 = 표지 · 그림 S1–S4 = SI p.2–5).  크롭 파일 이름의 pN 과 figures.json 의 page 는 PDF 쪽이다.
     값 표지: [인쇄] = 본문 · SI · 표 · 그림 안 글자로 적힌 값 · [판독 · 벡터] = PDF 안 벡터 경로의 꼭짓점 좌표를 같은 그림의 눈금 (역시 벡터) 으로 환산한 값 (재현 = litdb/figures/<slug>/digitized.csv 584 행 —
     그림 1 · 2d–e · 3g–h · 5g · SI 그림 S1 은 래스터가 아니라 벡터라 판독 정밀도가 높다: 빈도 ±0.0005 · 응력 면적 ±0.01 %p · 용량 ±0.2 mAh g⁻¹ 급) · [판독] = 래스터 그림을 눈금으로 읽은 값 (거칢) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드에 적힌 값 (그 카드 slug 병기) ·
     [우리] / [우리 산술] = 우리 쪽 값 (CLAUDE.md · 작업 가지 docs/data 의 출처를 그 자리에 적음) 과 견주는 계산 · [미확인] = 본문 8 쪽 + SI 5 쪽 전수에 없음.
     원문 13 쪽은 글자 층 추출 (pdftotext layout · raw) + 전 쪽 렌더로 전부 읽었다 (본문 p.7 의 두 모델 식은 수식 글꼴이라 렌더에서 옮겼다).  DEM · 입자 계산 · 압밀 시뮬레이션은 없다 — 실험 (XCT · FIB-SEM · 3D XANES · 전기화학) + 2D 선형 탄성 화학–역학 메조 모델. -->
# NCM811 : Li₆PS₅Cl **질량비 70:30 · 80:20 · 85:15** 복합 양극의 XCT 미세구조 (microstructure) — NCM–NCM 배위수 분포 (평균 4.8 · 6.5 · 7.4 · 복셀 0.65 µm · 기공망 모형) · 상 분율 (공극 + 탄소 14.7 · 18.1 · 23.3 %) · XCT 단면 위 2D 선형 탄성 + 확산 변형 응력 (> 2 GPa 면적이 비선형으로 증가) · FIB-SEM 균열 · 3D XANES Ni 흰선 불균일 — Park · Naik · Vishnugopi · Xiao · Drakopoulos · Vo · Zhong · Mukherjee · Hatzell (ACS Nano 2025)

> slug `park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics` · DOI `10.1021/acsnano.5c04431` · type `experiment + continuum model (synchrotron micro-CT 상 분할 · NCM 망 배위수 (기공망 모형 · Avizo) · FIB-SEM 균열 · 3D XANES Ni 흰선 에너지 · 2D XCT 단면 위 선형 탄성 + 확산 변형 메조 모델 — DEM · 입자별 계산 · 압밀 시뮬레이션 없음)` · PDF `06b00677-6._Chemo-mechanical_behavior_and_stability_of_high-loading_cathodes_in_solid-state_batteries.pdf` · SI `54daa555-6._Sup_Chemo-mechanical_behavior_and_stability_of_high-loading_cathodes_in_solid-state_batteries.pdf` · digested `2026-11-12` · status ✅
>
> **저자**: Se Hwan Park ¹ · Kaustubh G. Naik ² · Bairav S. Vishnugopi ² · Xianghui Xiao ³ · Michael Drakopoulos ³ · Nghia T. Vo ³ · Zhong Zhong ³ · Partha P. Mukherjee ² · **Kelsey B. Hatzell\*** ¹,⁴,⁵ — ¹ Andlinger Center for Energy and the Environment, Princeton · ² School of Mechanical Engineering, Purdue · ³ Brookhaven National Laboratory, National Synchrotron Light Source II · ⁴ Dept. Mechanical and Aerospace Engineering, Princeton · ⁵ Dept. Chemical and Biological Engineering, Princeton — \* 교신 (kelsey.hatzell@princeton.edu) · *ACS Nano* **2025**, **19** (24), **22262–22269** (8 쪽 · Article · 호 24 = 원문 다운로드 경로 '…/19/24/22262/…') · 접수 2025-03-13 · 수정 2025-05-31 · 승인 2025-06-02 · 출판 2025-06-11 · © 2025 ACS (열린 이용 표기 없음) · 키워드 *solid-state batteries, cathode, chemo-mechanics, stress, fracture* · 연구비 = DOE BES EFRC (MUSIC) **DE-SC0023438** · NSLS-II 27-ID (HEX) · 18-ID (FXI) · CFN 사용 (인쇄 계약 번호 DE-SC0023462) · ORCID 표기 = Park · Vo · Hatzell.
> **이웃 카드 (링크만)**: [`jeong2024_operando_densification_chemomechanics_se_size_composite_cathode`](jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md) (이 논문 ref (3) — 같은 그룹 · 같은 모델 매개변수 계열 · c_max 52 500 의 인용처) · [`gandla2026_layered_cathode_degradation_diagnostics_review`](gandla2026_layered_cathode_degradation_diagnostics_review.md) (리뷰 ref [104] · 그림 5g–h = 이 논문 그림 2 재수록 · L32 · L116 · L121 · L249 · L260 · L335–337 · L379 · L419) · [`li2026_electrochemomechanical_coupling_asslmb_review`](li2026_electrochemomechanical_coupling_asslmb_review.md) (리뷰 ref [51] · [86] · L18 · L66 · L98 · L104 · L135 · L152) · [`bielefeld2019_microstructural_modeling_composite_cathode`](bielefeld2019_microstructural_modeling_composite_cathode.md) (ref (7) — "80:20 이면 충분" 이론) · [`deng2016_elastic_superionic_electrolytes_dft`](deng2016_elastic_superionic_electrolytes_dft.md) (ref (16) — LPSCl 22 GPa) · [`intergranular_cracking_nmc811_jmca2023`](intergranular_cracking_nmc811_jmca2023.md) (ref (13) — NMC811 입계 균열) · [`stavola2023_thick_nmc111_lpscl_lithiation_gradient_tortuosity`](stavola2023_thick_nmc111_lpscl_lithiation_gradient_tortuosity.md) (ref (18)).
> **판독 원자료**: `litdb/figures/park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics/digitized.csv` (584 행 — 그림 2e 배위수 확률 (CN 0–18 × 3) + 파생 통계 · 그림 2d 인쇄 상 분율 · 그림 3g 응력 분포 (0.2 GPa 칸 50 × 3) + 파생 · 그림 3h (> 2 GPa 면적 ± 표준편차) · 그림 5g 흰선 히스토그램 (33 × 3) + 파생 · 그림 1d · 1e (50 사이클 × 3) · 그림 1a–c 곡선 끝점 · SI 그림 S1 봉우리 · 그림 3a 래스터 축 보정) · 그림 크롭 **56 장** (도구 10 전부 그대로 + 손 크롭 46 = 그래픽 초록 1 · 패널 19 · 식 2 · 근거 문단 24 · 본 뒤 다시 렌더 24) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: LiNbO₃ 코팅 NCM811 (Ampcera) 과 Li₆PS₅Cl (NEI) 을 **질량비 70:30 · 80:20 · 85:15** (탄소 C65 는 (NCM + LPSCl) : C = 100 : 3) 로 섞어 **300 MPa 2 분** 에 조립한 셀을 싱크로트론 micro-CT (복셀 **0.65 µm** · 시야 2 × 2 mm²) 로 찍어 분할하면 — NCM 부피분율 **0.391 · 0.506 · 0.500**, 공극 + 탄소 (한 덩어리로만 분할된다) **0.147 · 0.181 · 0.233** 이고 (그림 2d [인쇄]), **기공망 모형 (pore-network model) 으로 센 NCM–NCM 배위수 평균이 4.8 · 6.5 · 7.4** 로 오른다 (p.3 [인쇄] · 분포 = 그림 2e · 벡터 판독으로 평균 4.88 · 6.55 · 7.40 재현 · 표준편차 2.43 · 2.63 · 3.08).  그 XCT **2D 단면 (≈260 × 260 µm = 400 × 400 복셀)** 위에 선형 탄성 + 확산 변형 (Ω = 2 × 10⁻⁶ m³ mol⁻¹) 을 풀면 80 % 방전에서 **σy > 2 GPa 인장 면적 0.25 → 1.23 → 2.42 % · 압축 1.73 → 2.90 → 3.98 %** (세 단면 평균 · 그림 3h [판독 · 벡터]) 로 비선형 증가하고, 20 사이클 뒤 FIB-SEM 에서 80:20 · 85:15 만 넓은 입자 균열 · 계면 공극이 보이며 (70:30 은 폭 < 50 nm 균열 몇 개), 3D XANES (40 nm) 에서 방전 끝 Ni 흰선 에너지가 **8353.4 → 8353.8 → 8353.9 eV** (덜 리튬화) · 입자 안 표준편차 **0.31 → 0.36 → 0.41 eV** 로 커진다.  0.2C 50 사이클 유지율 **94.6 · 76.8 · 74.1 %**.  저자 결론 = *"the pronounced degradation observed at higher NCM contents is primarily driven by increased interparticle stress rather than intraparticle stress"* (p.6).  **'접촉' (연결) 판정 기준 · 분할 방법 · 입경 · 촬영 때 압력 · 진밀도는 원문에 없다.**  계산 쪽은 압밀 시뮬레이션이 아니라 **소성 · 파괴 · 접촉이 없는 2D 선형 탄성** 이라 응력 ±5 GPa (색 막대) 가 그대로 남는다.

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ NCM–NCM 배위수 분포 vs 조성 | 평균 **4.8 · 6.5 · 7.4** (70:30 · 80:20 · 85:15) [인쇄 p.3] · 분포 (정수 CN 0–18 의 빈도 · 합 1.00) [판독 · 벡터]: 최빈 **5 · 5 · 6** (70:30 은 CN 4 = 0.174 ≈ CN 5 = 0.175) · 중앙 5 · 6 · 7 · 표준편차 2.43 · 2.63 · 3.08 · P(CN ≤ 2) **16.0 · 4.1 · 3.0 %** · P(CN ≥ 10) **4.6 · 13.2 · 23.7 %** · P(CN = 0) 0.73 % · < 0.13 % · < 0.13 % · 빈도 > 0.001 인 마지막 CN 14 · 16 · 18 [카드 산술] | [인쇄] p.3 · [판독 · 벡터] 그림 2e |
| ② ★ 접촉 판정 · 분할법 · 분해능 | 판정 = *"The pore-network model developed from the segmented images reveals the connectivity of NCM particles"* · *"the number of neighboring NCM particles connected to a given particle"* · *"more physical connections"* (p.3) · 분할 · 망 = Thermo Scientific **Avizo** (p.7) — **거리 문턱 · 입자 분리 (watershed 등) · 망 매개변수 [미확인]** · 복셀 **0.65 µm** · 시야 2 × 2 mm² · 50 keV · 투영 1800 장 / 180° · Algotom FBP 재구성 (p.7) · NCM 단면 지름 ≈2–15 µm [판독 그림 4] → NCM 지름당 ≈3–23 복셀 [카드 산술] | [인쇄] p.3 · p.7 · [판독] |
| ③ ★ 조성 기준 · 성형압 · 기공 | **질량비** (*"mass ratios (70:30, 80:20, and 85:15)"* p.2 · *"weight ratios"* p.6) · 탄소 (NCM + LPSCl) : C65 = 100 : 3 (복합 전체의 2.91 wt% [카드 산술]) · LPSCl 80 mg 펠릿 **80 MPa** → 양극 (NCM **9 mg cm⁻²**) · Li–In 을 올려 **셀 전체 300 MPa 2 분** (지름 10 mm PEEK) · 운전 적층압 **50 MPa** · 30 °C (p.7) · XCT 상 분율 (그림 2d [인쇄]) NCM 0.391 · 0.506 · 0.500 · LPSCl 0.462 · 0.310 · 0.267 · **공극 + 탄소 0.147 · 0.181 · 0.233** (*"distinguishing empty spaces from carbon particles is challenging"* p.3) · **XCT 시편의 촬영 때 압력 · 사이클 전후 · 진밀도 기공 [미확인]** | [인쇄] p.2 · p.3 · p.6 · p.7 · 그림 2d |
| ④ ★ 미세구조 응력 (모델) | 2D 영역 = XCT 단면 (≈260 × 260 µm [판독 래스터 축] = 0.65 µm 복셀 400 × 400 [카드 산술]) · 세 상 (NCM811 · SE · 공극/탄소) · ∇·σ = 0 · **선형 탄성** + 확산 변형 c_max(1 − c/c_max)Ω/3 δij (CAM 만) · 위아래 = 적층압 (값 [미확인]) · 옆 x 구속 · 조성마다 단면 3 장 평균 ± 표준편차 (p.7) · 표 1: c_max 52 500 mol m⁻³ (ref 3) · **E_SE 22 GPa (ref 30) · ν_SE 0.27 · E_AM 200 GPa (ref 17) · ν_AM 0.3** · Ω 2 × 10⁻⁶ m³ mol⁻¹ · 결과 (80 % 방전): 색 막대 ±5 GPa · > 2 GPa 면적 (그림 3h [판독 · 벡터]) 인장 **0.25 ± 0.08 · 1.23 ± 0.23 · 2.42 ± 0.07 %** · 압축 **1.73 ± 0.42 · 2.90 ± 0.65 · 3.98 ± 0.33 %** · σy 분포 표준편차 0.69 · 0.88 · 1.00 GPa (그림 3g [카드 산술]) | [인쇄] p.3 · p.4 · p.7 · 표 1 · [판독 · 벡터] |
| ⑤ 화학–역학 열화 (균열 · 접촉 잃음) | FIB-SEM (20 사이클 = 0.1C 1 + 0.2C 19): 조립 직후 셋 다 균열 없음 · 20 사이클 뒤 **70:30 = 폭 < 50 nm 균열 몇 개 · 80:20 · 85:15 = 넓은 입자 안 균열 + 계면 공극 많음** (그림 4 · S3) · 나노 CT 에서 80:20 · 85:15 입자 조각남 (그림 5 · S4) · 정량 (균열 부피 · 접촉 면적) **없음** | [인쇄] p.5 · p.6 · 그림 4 · 5 |
| ⑥ 3D XANES (무엇을 · 해상도) | FXI (18-ID) 나노 CT + Ni K 흡수단 여러 에너지 · 공간 해상도 **40 nm** · 20 사이클 뒤 **1.9 V (vs Li/In) 까지 방전한 가루** (지름 3 mm 폴리이미드 관) · 평균 흰선 에너지 **8353.4 · 8353.8 · 8353.9 eV** · 입자 안 표준편차 **0.31 · 0.36 · 0.41 eV** (p.6 [인쇄]) — ⚠ 그림 5g 곡선의 평균 · 표준편차는 **8353.24 · 8353.54 · 8353.70 eV · 0.26 · 0.28 · 0.33 eV** [판독 · 벡터 · 카드 산술] — 같은 순서이나 인쇄값보다 0.16–0.26 eV 낮다 | [인쇄] p.6 · p.7 · [판독 · 벡터] 그림 5g |
| ⑦ 전기화학 | 방전 용량 (mAh g⁻¹) 0.1C **156.7 · 155.3 · 144.6** · 0.2C **136.6 · 137.3 · 128.0** · 0.5C **123.2 · 117.4 · 76.4** · 0.2C 50 사이클 뒤 **133.1 · 107.0 · 89.8** · 유지율 **94.6 · 76.8 · 74.1 %** (= 50 번째 ÷ 2 번째 사이클 [카드 산술 · 셋 모두 재현]) · dQ/dV: 80:20 · 85:15 봉우리 분극 · 감소 (SI 그림 S1) · 1C = 180 mA g⁻¹ · 1.9–3.6 V vs Li/In | [인쇄] p.2 · p.7 · [판독 · 벡터] |
| ⑧ 저자 한계 | *"Distinguishing and quantifying the individual contributions of interparticle and intraparticle stresses are challenging, as these phenomena are highly coupled and amplify each other"* (p.6) · 60:40 이면 응력은 줄겠지만 *"can limit effective electronic conduction and material utilization, and also exacerbate reaction heterogeneity"* (p.6) | [인쇄] p.6 |

⛔ **한정어 (떼지 말 것)**: ① 배위수 = **XCT 분할 + 기공망 모형의 '연결' 수** (복셀 0.65 µm · 판정 기준 미인쇄) — DEM 의 겹침 (δ > 0) 접촉 수와 **이름만 같다** ② 조성 = **NCM : LPSCl 질량비** (탄소는 따로 100 : 3) ③ 상 분율의 "공극" 은 **공극 + 탄소** — 진밀도 기공이 아니고 탄소를 뺄 수 없다 ④ XCT 시편의 **촬영 때 압력 · 사이클 전후는 인쇄되지 않았다** (조립 300 MPa 2 분 · 운전 50 MPa) ⑤ 응력 모델 = **2D · 선형 탄성 · 소성 · 파괴 · 접촉 · 박리 없음 · 압밀 이력 없음** (방전 0 % = 무응력 · SI 그림 S2) — ±5 GPa · "> 2 GPa 면적" 은 탄성 상한 지표이지 실제 응력이 아니다 ⑥ 재료 · 입경: LiNbO₃ 코팅 NCM811 (다결정 2 차 입자로 읽힌다 — p.6 *"primary particles in secondary particles"* [카드 해석]) · NEI LPSCl — 입경 · D50 [미확인].
⇒ **절대값 전이: 0 건.** 전이되는 것은 **방향** (NCM 질량비 70 → 85 % 에서 NCM–NCM 연결 수 ↑ · 분포 넓어짐 · 공극 + 탄소 ↑ · 고응력 면적 비선형 ↑ · 사이클 열화 ↑) 과 **측정 · 보고 꼴** (CN 분포를 정수 빈도로 · 세 단면 평균 ± 표준편차 · 공극/탄소 묶음 표지) 뿐이다.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-6 의 '왜' 칸)

의도 원문: *"d · i · 결과 전 대조 항목 — XCT 로 센 NCM–NCM 배위수 분포 vs 조성 (NCM811 : LPSC 70:30 · 80:20 · 85:15) = 우리 AM–AM CN 대조 원전 ★★ (gandla) · 3D XANES · 미세구조 응력 ★ (li2026) · 비교 문서는 리뷰 재수록 그림 판독 (± 0.5) 뿐이라 접촉 판정 · CT 분해능 · 질량 / 부피 기준 · 성형압 · 기공이 없음 · gandla 도 조성비 기준 · 접촉 판정 [미확인]"* (가리킨 카드 = gandla2026 L337 · L419 · L447 · li2026 L152 · 비교 문서 `comparison_vs_ours_DEM.md` §E — 지금 정본에서는 L3032)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "d" (단단한 + 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍) | **일부** | 하중 몫 · 압축 계산 **없음**.  있는 것 = 단단한 NCM 망의 연결 수가 NCM 질량비와 함께 오른다는 **구조 지표** (CN 4.8 → 6.5 → 7.4 · p.3) 와, 그것이 *"restricts the freedom for individual particles to expand"* (p.4) 라는 **사이클 중 구속** 논리 — 누를 때의 재밍 · 하중 분담이 아니라 충방전 부피 변화의 구속이다 |
| "i" (복합 양극의 압력별 기공) | **일부** | **압력별이 아니라 조성별 · 한 압력**: 셀 전체 300 MPa 2 분 조립 (p.7) 뒤 XCT 공극 + 탄소 **14.7 · 18.1 · 23.3 %** (p.3 · 그림 2d [인쇄]) — 탄소와 공극을 못 가르고 (p.3) · 진밀도 기공이 아니며 · 촬영 때 압력 (50 MPa 적층압 유지 여부) [미확인].  저자 해석: SE 가 적으면 *"less effective filling of the interstitial voids between NCM particles during electrode densification, resulting in higher residual porosity"* (p.3) |
| "결과 전 대조 항목 — XCT 로 센 NCM–NCM 배위수 분포 vs 조성 (70:30 · 80:20 · 85:15)" | **채움** | 그림 2e (정수 CN 0–18 의 빈도) · 평균 4.8 · 6.5 · 7.4 (p.3) · 벡터 판독 (§3-2 · digitized.csv) 으로 분포 전체와 표준편차 · 꼬리 · 비율까지 |
| "= 우리 AM–AM CN 대조 원전 ★★ (gandla)" | **채움 (같은 이름 · 다른 연산자)** | 원전 확인 — gandla 그림 5h = 이 논문 그림 2e.  단 '연결' 의 정의가 DEM 접촉과 다르다 (§7-2 정의 대조표) — 맞대기는 **모양 · 방향만** |
| "3D XANES" | **채움** | FXI 18-ID · 40 nm · 20 사이클 뒤 1.9 V 방전 가루 · Ni 흰선 평균 8353.4 · 8353.8 · 8353.9 eV · 표준편차 0.31 · 0.36 · 0.41 eV (p.6 · p.7) — ⚠ 그림 5g 곡선 통계와 인쇄값이 0.16–0.26 eV 어긋남 (§3-6) |
| "미세구조 응력 ★ (li2026)" | **채움 (2D 선형 탄성 한정)** | 2D XCT 단면 · 선형 탄성 + 확산 변형 · 표 1 물성 · > 2 GPa 면적 (그림 3h) · 소성 · 파괴 · 접촉 없음 (p.3 · p.7) |
| "접촉 판정 [미확인]" | **없음 (원문에도 없음)** | 원문은 "pore-network model" · "connected" · Avizo 만 적는다 — 거리 문턱 · 입자 분리 알고리즘 · 망 매개변수 · 경계 (슬래브 면) 입자 처리 **미인쇄**.  ⇒ 이 [미확인] 은 원 논문으로도 풀리지 않는다 |
| "CT 분해능" | **채움** | 복셀 **0.65 µm** · 시야 2 × 2 mm² · 50 keV 단색 · 투영 1800 장 / 180° · Algotom (평탄화 · 회전 중심 · 고리 제거 · FBP) (p.7) |
| "질량 / 부피 기준" | **채움** | 조성 = **질량비** (p.2 · p.6) · 부피는 XCT 분할 상 분율로 따로 (그림 2d) — 저자 *"the volumetric ratio … aligns well with the experimentally used mass ratio"* (p.3 · 쓴 진밀도 미인쇄 · §3-2 에서 카드가 검산) |
| "성형압" | **채움 (촬영 상태는 미확인)** | SE 펠릿 80 MPa → 셀 전체 300 MPa 2 분 · 적층압 50 MPa (p.7) · XCT 는 *"The cell assemblies in a PEEK die were imaged"* (p.7) — 그때 압력 · 사이클 전후 [미확인] |
| "기공" | **일부** | 공극 + 탄소 한 덩어리 (위 i 칸) — 진밀도 · 질량 기공 없음 |
| "gandla 도 조성비 기준 [미확인]" | **해소** | 질량비 (p.2 *"solid electrolyte mass ratios (70:30, 80:20, and 85:15)"* · p.6 *"The NCM-to-LPSCl weight ratios were 70:30, 80:20, and 85:15"*) |

**가리킨 카드 · 같은 논문을 옮긴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `gandla2026_…` L121 | *"그림 5g: 시야 **1 mm** · 분할 NCM / SE / 공극+탄소 · NCM 망"* · *"그림 5h [판독 · ±0.5 CN]: 최빈 배위수 ≈4.5 (70:30, 최대 빈도 0.177) · ≈5.3–5.5 (80:20, 0.157) · ≈5–6.5 평탄 (85:15, 0.127) · 꼬리 끝 ≈12 · ≈15 · ≈17–18"* · *"NCM 입자 사이 배위수 (직접 접촉 수)"* | 1 mm = 그림 2a 의 눈금 화살표 ✓ (촬영 시야는 2 × 2 mm²) · 벡터 판독: CN 4 · 5 = 0.174 · 0.175 (70:30) · CN 5 = 0.159 (80:20) · CN 5–7 = 0.125–0.130 (85:15) ✓ (±0.5 안) · 꼬리: 빈도 > 0.001 인 끝 14 · 16 · 18 (70:30 의 CN 13–15 는 0.004–0.001 이라 재수록 래스터에서 안 보였다) · **"직접 접촉 수" = 카드의 해석** — 원문은 "connected" · "physical connections" 만 쓰고 판정 기준이 없다 | **일부** — 값은 맞고 70:30 꼬리 끝이 짧게 읽혔으며, '직접 접촉' 은 원문보다 강한 표현 |
| `gandla2026_…` L337 | *"① 조성비 질량/부피 기준 [미확인] ② XCT 분해능 · '접촉' 판정 (실측 겹침 vs 근접 문턱) [미확인] ③ 입경 · PC/SC 분포 [미확인] ④ 원 논문 [104] 카드 없음"* | ① 질량비 ✓ 해소 ② 분해능 0.65 µm ✓ 해소 · 판정 기준 = 원문에도 없음 ③ 입경 = 원문에도 없음 (NCM 단면 ≈2–15 µm [판독]) · PC 로 읽힘 (*"primary particles in secondary particles"* p.6 [카드 해석]) ④ 이 카드 | **채움** — ① ② (분해능) ④ 해소 · 판정 기준 · 입경은 원 논문으로도 [미확인] |
| `gandla2026_…` L32 · L379 | *"XCT 로 잰 NCM–NCM 배위수 분포 (… → 최빈 ≈4.5 · ≈5.5 · ≈5–6.5)"* | 최빈 = 정수 CN **5 (CN 4 와 동률) · 5 · 6** [판독 · 벡터] · 평균 4.8 · 6.5 · 7.4 [인쇄] | **채움** (판독 정밀도 차) |
| `gandla2026_…` L116 | *"사이클 부피 변화 최대 ~10 % [103, 104]"* | 원문 서론 *"CAM experiences volume changes of up to ∼10%"* (p.1 · refs 11–13 인용) ✓ | **채움** |
| `gandla2026_…` L249 | *"메조 화학-기계 모델 (단층촬영 미세구조 입력) · NCM 비율 ↑ → 입자간 응력 · 고응력 영역 비선형 증가"* | p.3 *"a nonlinear rise in high-stress areas"* ✓ · 모델 = **2D 단면 · 선형 탄성** (리뷰 문장에는 차원 · 구성식이 없다) | **채움** (차원 · 구성식 한정 빠짐) |
| `gandla2026_…` L260 | *"[104] 의 메조 모델이 단층촬영 형상을 그대로 쓴다는 것만 적혀 있고, 입자 형상 · 접촉 · 소성 처리는 [미확인]"* | 이제 확인: 2D 연속체 · 상마다 E · ν · 소성 없음 · 접촉 · 박리 없음 (상이 붙어 있다고 읽힘 [카드 해석]) · 공극/탄소 물성 [미확인] (*"Table S1"* 이 SI 에 없다) | **해소** (§3-4 · §4-3) |
| `gandla2026_…` L419 · L447 | 서지 *"S. H. Park, K. G. Naik, B. S. Vishnugopi, et al., … ACS Nano 19, no. 24 (2025): 22262–22269"* · "카드 없음" | 서지 ✓ (DOI 10.1021/acsnano.5c04431) · 이제 카드 있음 | **채움** |
| `li2026_…` L66 | *"Park [51] (…70:30 / 80:20 / 85:15): 80:20 · 85:15 열화 심함 · **미세구조 기반 모의에서 방전 중 NCM 부피변화 ≈10 %** · 85:15 가 70:30 보다 > 2 GPa 응력 영역이 훨씬 넓음 · 3D XANES: NCM 많을수록 방전 끝 리튬화 덜 되고 불균일"* | 열화 ✓ (94.6 · 76.8 · 74.1 %) · > 2 GPa ✓ (인장 ×9.6 · 압축 ×2.3 [카드 산술]) · XANES ✓ · **"≈10 %" 는 모의 결과가 아니라 서론의 문헌값** (p.1 · refs 11–13) — 모델의 Ω c_max / 3 = 3.5 % 선 변형 (≈10.5 % 부피, c 를 0 → c_max 전부 쓸 때) [카드 산술] 이 값으로 그 자릿수와 맞을 뿐 원문은 이 둘을 잇지 않는다 | **일부** — 서론 문헌값을 모의 결과로 옮김 (리뷰 문장 · 그 카드의 표기) |
| `li2026_…` L18 · L104 · L98 · L135 · L152 | "Park 2025 (NCM811:LPSC 70:30 / 80:20 / 85:15)" · "(c) Park 3D XANES (로딩)" · "(d, e) 복합양극 응력 (Farzanian · Park, 로딩 의존)" · "원 논문 카드 필요 … 정본 카드 없음" · 서지 *"Park, S.H.; … Hatzell, K.B. … ACS Nano 2025, 19, 22262–22269"* (번호 51 · 86 두 개) | ✓ · "로딩" = 면 로딩이 아니라 **CAM 질량비** (면 로딩은 셋 다 NCM 9 mg cm⁻²) · 이제 카드 있음 | **채움** — "로딩" 낱말만 한정 (CAM 비율) |
| `comparison_vs_ours_DEM.md` L3032 (§E) | *"그림 5h (Park 2025 ACS Nano 재수록): XCT NCM–NCM 배위수 최빈 ≈4.5 · ≈5.5 · ≈5–6.5 (… 판독 ±0.5) — DEM AM–AM CN 과 같은 양 (접촉 판정 · CT 분해능 · 질량/부피 기준 미기재 → 모양 · 방향만)"* | 질량비 ✓ · 분해능 0.65 µm ✓ · 판정 기준은 원문에도 없음 · "같은 양" → **같은 이름 · 다른 연산자** | **일부** — 비교 문서 §E 에 원전 줄을 보탠다 (옛 줄은 그대로) |

⇒ **의도 대조 결과: 채움 (CN 분포 · 질량 기준 · CT 분해능 · 성형압 · 3D XANES · 미세구조 응력) · 일부 (d · i · 기공 = 공극 + 탄소 · 촬영 때 압력 미확인) · 없음 (접촉 판정 기준 — 원 논문에도 없음)**.  2 차 인용은 값은 맞고, '직접 접촉' (gandla) · '모의에서 ≈10 %' (li2026) · '로딩' (li2026) 세 표현이 원문보다 앞서 나갔다.

---

## 1. 한 줄 요약
같은 재료 (LiNbO₃ 코팅 NCM811 · NEI LPSCl · C65 3 phr) 로 **CAM 질량비만 70 → 80 → 85 %** 바꾼 복합 양극을 **싱크로트론 micro-CT** 로 분할해 상 분율 · NCM 망 배위수를, **2D 선형 탄성 메조 모델** 로 방전 중 응력을, **FIB-SEM · 3D XANES** 로 20 사이클 뒤 균열 · Li 불균일을, **전기화학** 으로 율속 · 수명을 본다.
NCM 이 많을수록 NCM–NCM 연결이 많아지고 (4.8 → 7.4) · 무른 SE 가 줄며 · 고응력 면적이 비선형으로 늘고 · 입자 균열과 계면 공극 · 리튬화 불균일이 커지며 · 수명이 짧아진다.
저자 제안: *"incorporating mechanically soft pillar phases within the composite cathode offers a promising approach to buffer stress accumulation"* (p.6) · 초록: *"Coatings that suppress active material-active material interactions during cycling may aid in suppressing the generation of local stress hotspots"* (p.1).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| S. H. Park · K. G. Naik · B. S. Vishnugopi · X. Xiao · M. Drakopoulos · N. T. Vo · Z. Zhong · P. P. Mukherjee · **K. B. Hatzell\*** (Princeton · Purdue · BNL NSLS-II) | ACS Nano 19 (24) 22262–22269 (2025) · © ACS | 10.1021/acsnano.5c04431 | **Li₆PS₅Cl** (NEI) + **LiNbO₃ 코팅 NCM811** (Ampcera) + Super C65 · Li–In 대극 | 실험 (micro-CT · FIB-SEM · 나노 CT / 3D XANES · 전기화학) + 2D 선형 탄성 화학–역학 메조 모델 (Purdue Mukherjee 그룹) |

- **1저자 메모와의 대조**: 저자 (S. H. Park, K. G. Naik, B. S. Vishnugopi, … K. B. Hatzell) · 제목 · 학술지 · 권 19 · 쪽 22262–22269 · 2025 — **같다**.  DOI = 10.1021/acsnano.5c04431 (원문 p.1).  덧붙임 ① 호 = 24 (원문 다운로드 경로 · gandla 카드의 인용과 같음) ② 저자 9 명 전부 위 ③ 출판 2025-06-11.
- **글의 꼴**: 서론 → 결과 (전기화학 → 미세구조 → 응력 분포 → 사이클 뒤 기계 열화 → 반응 불균일) → 결론 → 실험 (전기화학 · 특성 분석 · 모델) → 참고문헌 31.  그림 5 · 표 1 · **번호 없는 식 둘** (p.7) / SI: 그림 S1–S4 (표 · 식 없음 — 본문이 가리키는 *"Table S1"* 은 없다).
- 그룹 맥락: 모델 쪽은 Naik · Vishnugopi · Mukherjee (Purdue) — 같은 그룹의 Jeong 2024 (ref 3 · 정본 카드 있음) 와 물성 계열이 같다 (E_SE 22 · ν_SE 0.27 · E_AM 200 · ν_AM 0.3 · c_max 52 500 [다른 카드 jeong2024 §3-7]).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 재료 · 조성 · 시편 (p.2 · p.6–7 · `txt_p2_intro_200gpa_mass_ratios.png` · `txt_p6_experimental_materials.png` · `txt_p7_cell_assembly_cycling.png`)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| CAM | **LiNbO₃ 코팅 LiNi₀.₈Co₀.₁Mn₀.₁O₂ (NCM811)** · Ampcera · 입경 · D50 · 단결정/다결정 **미인쇄** | [인쇄] p.6 |
| SE | **Li₆PS₅Cl (LPSCl)** · NEI Corporation · 입경 미인쇄 | [인쇄] p.6 |
| 도전재 | Super C65 carbon black | [인쇄] p.6 |
| 조성 | NCM : LPSCl **질량비 70:30 · 80:20 · 85:15** · (NCM + LPSCl) : C65 = **100 : 3** · 건식 혼합 (*"dry-mixing"* — 기구 · 시간 미인쇄) | [인쇄] p.2 · p.6 |
| 복합 전체 기준 | NCM **67.96 · 77.67 · 82.52 wt%** · LPSCl 29.13 · 19.42 · 14.56 wt% · C65 2.91 wt% | [카드 산술] (조성 ÷ 1.03) |
| 대극 | Li–In — *"pressing Li and In foils (Alfa Aesar) in a 95:5 weight ratio"* (Li : In 순서 그대로 · 어느 쪽이 95 인지 원문 순서 외 근거 없음) | [인쇄] p.7 |
| 셀 조립 | LPSCl **80 mg** 을 지름 **10 mm** PEEK 다이에서 **80 MPa** 펠릿 → 한쪽에 양극 (NCM **9 mg cm⁻²**) · 반대쪽에 Li–In → **조립 셀 300 MPa 2 분** | [인쇄] p.7 |
| 운전 | 적층압 **50 MPa** · 0.1–0.5C (**1C = 180 mA g⁻¹**) · **1.9–3.6 V vs Li/In** · **30 °C** | [인쇄] p.7 |
| 셀 하나의 NCM | 0.785 cm² × 9 mg cm⁻² = **7.07 mg** · 1C 전류 **1.62 mA cm⁻²** · 0.1C 첫 방전 면적 용량 (70:30) ≈ **1.41 mAh cm⁻²** | [카드 산술] |
| ★ "High-loading" 의 뜻 | 제목의 "high-loading" = **CAM 비율 (질량비)** 이다 — 면 로딩은 셋 다 NCM 9 mg cm⁻² (≈1.4 mAh cm⁻²) 로 같다 (초록 *"Increasing the ratio of cathode active materials"*) | [인쇄] p.1 · p.7 · [카드 해석] |
| 양극 두께 | **≈48 · ≈37 · ≈38 µm** (70:30 · 80:20 · 85:15) — 가정: XCT 시편 = 전기화학 셀과 같은 9 mg cm⁻² · ρ_NCM811 = 4.74–4.80 g cm⁻³ [다른 카드: `bielefeld2020_…` 4.76 · `kim2025_impedance_…` 4.77 · `schlautmann2023_…` 4.78 · `lee2026_lpscl_coating_thickness_ncm811` 4.8] · 식 t = (9 mg cm⁻² ÷ ρ_NCM) ÷ φ_NCM(XCT) · 원문에 두께 없음 | [카드 산술] |
| 전압 환산 | 1.9–3.6 V vs Li/In ≈ 2.52–4.22 V vs Li/Li⁺ — Li–In 전위 0.62 V 는 **원문에 없는 가정** | [카드 산술 · 가정] |

### 3-2. ★ XCT · 상 분율 · NCM 망 배위수 (p.3 · p.7 · 그림 2 · `fig_2a`–`fig_2e.png` · `txt_p3_microstructure_cn.png` · `txt_p7_xct_method.png`)
- **촬영** [인쇄 p.7]: NSLS-II **HEX (27-ID)** · *"The cell assemblies in a PEEK die were imaged"* · 단색 **50 keV** · 투영 **1800 장 / 180°** · 시야 **2 × 2 mm²** · 복셀 **0.65 µm** · Algotom (평탄화 · 회전 중심 [28] · 고리 제거 [29] · FBP) · 분할 · 시각화 · 분석 = Thermo Scientific **Avizo**.  촬영 때 압력 · 셀 상태 (사이클 전 · 뒤) · 분석 부피 · 분할 방법 (문턱 · 필터 · 분리) **미인쇄**.
- **보이는 것** [판독]: 그림 2a 2D 단면 (눈금 화살표 1 mm · 밝은 둥근 점 = NCM) · 2b 분할 (NCM 연파랑 · SE 진파랑 · 공극/탄소 빨강) · 2c NCM 망 (공–막대 · 얇고 넓은 판 꼴 — 색의 뜻 미인쇄) · 3a–c 의 모델 입력 단면은 ≈260 × 260 µm (아래 §3-4).
- **상 분율 (그림 2d · 막대 안 인쇄 숫자)**:

| 조성 (질량) | NCM | LPSCl | 공극 + 탄소 | NCM/(NCM+SE) (XCT) | 같은 비 — 질량비 + 진밀도 [카드 산술] |
|---|---|---|---|---|---|
| 70:30 | **0.391** | **0.462** | **0.147** (본문도 14.7 %) | 0.458 | 0.445 (ρ_SE 1.64 랩 표준) · 0.478 (1.87 랩 표준과 다른 문헌 값 [다른 카드 `schlautmann2023_…` · `var2026_…`]) |
| 80:20 | **0.506** | **0.310** | **0.181** | 0.620 | 0.579 · 0.611 |
| 85:15 | **0.500** | **0.267** | **0.233** | 0.652 | 0.661 · 0.690 |

  [카드 산술] 가정 ρ_NCM811 4.77 g cm⁻³ [다른 카드] · 탄소 무시.  XCT 의 NCM 몫은 두 진밀도로 계산한 띠와 ±0.04 안 — 저자 *"aligns well with the experimentally used mass ratio"* (p.3) 는 그 범위에서 선다 (원문은 쓴 진밀도를 인쇄하지 않았다).  ⚠ 85:15 의 NCM 부피분율 (0.500) 이 80:20 (0.506) 보다 작다 — 공극 + 탄소가 0.181 → 0.233 으로 크게 늘었기 때문 (원문의 설명 두 가지: NCM 이 무거워 전체 부피 ↓ · SE 가 적어 *"less effective filling of the interstitial voids between NCM particles during electrode densification"*).
- ★ **NCM–NCM 배위수 (그림 2e · 본문 p.3)**: 정의 *"The coordination number that quantifies the connectivity represents the number of neighboring NCM particles connected to a given particle. A higher coordination number indicates more physical connections between the NCM particles."* · 망 = *"The pore-network model developed from the segmented images"* · 평균 **4.8 · 6.5 · 7.4** [인쇄].
  **벡터 판독** (digitized.csv fig2e · 그림은 투명도를 평탄화한 여러 다각형 → 정수 CN 의 꼭짓점 → 계열마다 테두리 띠의 가운데):

| CN | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 70:30 | .0073 | .0471 | .1052 | .1445 | .1743 | .1754 | .1225 | .0867 | .0543 | .0361 | .0211 | .0130 | .0055 | .0035 | .0017 | .0007 | .0005 | 0 | 0 |
| 80:20 | <.0013 | .0062 | .0338 | .0640 | .1209 | .1585 | .1491 | .1380 | .1104 | .0866 | .0569 | .0287 | .0217 | .0136 | .0065 | .0017 | .0025 | .0005 | 0 |
| 85:15 | <.0013 | .0052 | .0242 | .0556 | .0857 | .1250 | .1296 | .1250 | .1090 | .1016 | .0778 | .0581 | .0401 | .0226 | .0155 | .0084 | .0075 | .0038 | .0021 |

  검산 [카드 산술]: 합 **0.9995 · 1.0001 · 0.9974** (확률 질량 = 입자의 몫) · 평균 **4.88 · 6.55 · 7.40** (인쇄 4.8 · 6.5 · 7.4) · 표준편차 **2.43 · 2.63 · 3.08** · 중앙 5 · 6 · 7 · 최빈 5 (CN 4 와 동률) · 5 · 6 · P(CN ≤ 2) **16.0 · 4.1 · 3.0 %** · P(CN ≥ 10) **4.6 · 13.2 · 23.7 %**.  ⚠ CN 0 의 80:20 · 85:15 는 한 덩어리 (≤ 0.0013) · CN ≥ 15 의 70:30 · 80:20 꼬리와 CN 8 의 80:20 · 85:15 (교차) 는 테두리 띠가 겹쳐 ±0.001 신뢰.
  ⇒ NCM 이 많아지면 **분포 전체가 오른쪽으로 · 넓게** (sd 2.4 → 3.1) 가고, **연결이 적은 NCM (CN ≤ 2) 이 16 % → 3 % 로 줄며** 연결이 많은 NCM (CN ≥ 10) 이 5 % → 24 % 로 는다.  70:30 에서 외톨이 NCM (CN 0) 이 0.7 % 있다.
- **분해능 감각** [카드 산술 · 판독]: NCM 단면 지름 ≈2–15 µm (그림 4 · 10 µm 막대) · 나노 CT 입자 ≈8–13 µm (그림 5 · 10 µm 막대) → 0.65 µm 복셀로 NCM 지름당 ≈3–23 복셀.  LPSCl · 탄소의 크기는 원문에 없다.  **두 NCM 사이 틈이 복셀 하나 (0.65 µm) 보다 좁으면 분할에서 붙어 보일 수 있다** — 그 경우 '연결' 은 겹침이 아니라 근접 문턱 ≈ 1 복셀 [카드 해석 · 원문은 해상도의 영향을 말하지 않는다].
- **슬래브 기하** [카드 해석]: 양극 두께 ≈37–48 µm [카드 산술 §3-1] 는 NCM 3–5 개 지름 — 그림 2c 의 얇은 판 꼴과 맞는다.  분리막 · 집전체 면에 닿은 NCM 은 그쪽에 이웃이 없어 CN 이 낮게 나올 수 있다 (우리 DEM 의 벽 효과와 같은 꼴) — 원문은 경계 입자를 뺐는지 적지 않는다.

### 3-3. 전기화학 (p.2 · p.7 · 그림 1 · SI 그림 S1 · `fig_1a`–`fig_1e.png` · `fig_S1.png` · `txt_p2_rate_cycling_capacities.png`)
- **율속 (방전 · mAh g⁻¹)** [인쇄 p.2 · 그림 1d 표지와 ±0.03 일치 [판독 · 벡터]]:

| 조성 | 0.1C | 0.2C | 0.5C |
|---|---|---|---|
| 70:30 | **156.7** | **136.6** | **123.2** |
| 80:20 | **155.3** | **137.3** | **117.4** |
| 85:15 | **144.6** | **128.0** | **76.4** |

  저자: 0.1 · 0.2C 에서 70:30 ≈ 80:20 · 0.5C 에서 갈림 → *"the 80:20 microstructure may have a more tortuous structure"* (tortuosity 측정 없음) · 85:15 는 모든 율속에서 낮다 → *"inefficient ion transport across the cathode thickness"*.
- **그림 1a–c 곡선 끝점** [판독 · 벡터]: 첫 0.1C 충전 **240.9 · 232.6 · 233.5** mAh g⁻¹ → 첫 사이클 효율 (인쇄 0.1C 방전 ÷ 첫 충전) **65.0 · 66.8 · 61.9 %** [카드 산술 · 원문에 효율 없음].  ⚠ 곡선 끝과 인쇄값이 다른 두 칸: **70:30 0.1C 방전 곡선 끝 158.6 (인쇄 156.7)** · **80:20 0.5C 방전 곡선 끝 114.1 (인쇄 117.4 · 그림 1d 표지도 117.4)** — 나머지 일곱 칸은 ±0.1 안.
- **수명 (그림 1e · 0.1C 1 사이클 → 0.2C)** [인쇄 p.2]: 유지율 **94.6 · 76.8 · 74.1 %** · 50 사이클 뒤 **133.1 · 107.0 · 89.8** mAh g⁻¹.  [판독 · 벡터] 사이클 1 (0.1C) 156.7 · 153.8 · 144.6 · 사이클 2 (0.2C) **140.7 · 139.2 · 121.2** · 사이클 20 139.2 · 121.9 · 102.1 · 사이클 50 133.2 · 107.0 · 89.8 → **유지율 = 사이클 50 ÷ 사이클 2** (94.64 · 76.83 · 74.11 % [카드 산술] — 인쇄값 셋 모두 재현).  ⚠ 사이클 2 (0.2C) 가 그림 1d 의 0.2C (136.6 · 137.3 · 128.0) 와 다르다 (+4.1 · +1.9 · −6.8) — 수명 셀과 율속 셀이 같은지 [미확인].  FIB-SEM · XANES 가 본 "20 사이클 뒤" 는 이 곡선에서 첫 0.2C 대비 98.9 · 87.6 · 84.2 % 자리 [카드 산술 · 같은 셀이라는 가정 없이 꼴만].
- **dQ/dV (SI 그림 S1 · 2 · 20 · 50 번째 사이클)** [판독 · 벡터 · 잡음 포함 최대점]: 충전 봉우리 높이 (mAh g⁻¹ mV⁻¹) · 자리 (V vs Li/In) — 70:30 **0.076 → 0.069 → 0.065** · 3.18 → 3.20 V / 80:20 **0.054 → 0.043 → 0.036** · 3.15 → 3.23 V / 85:15 **0.051 → 0.038 → 0.036** · 3.18 → 3.28 V.  방전 골 70:30 −0.051 → −0.049 · 80:20 −0.043 → −0.033 · 85:15 −0.041 → −0.029.  ⇒ 본문 (p.2) *"The redox peaks of 80:20 and 85:15 … become more polarized and decrease in intensity"* · *"in the 70:30 cathode, the peak position and intensity remain stable"* 와 같은 방향 (70:30 도 높이는 −14 % · 80:20 −33 % · 85:15 −28 % [카드 산술]).

### 3-4. ★ 화학–역학 응력 모델 (p.3 · p.4 · p.7 · 표 1 · 그림 3 · SI 그림 S2 · `eq_01_…` · `eq_02_…` · `tab_1.png` · `fig_3abc` · `fig_3def` · `fig_3g` · `fig_3h.png` · `fig_S2.png` · `txt_p7_modeling_*.png` · `txt_p7_bc_three_slices.png`)
- **영역**: *"a 2D computational domain was established by using X-ray tomography-derived microstructural data"* · 분할 세 상 *"NCM811 (cathode active material), solid electrolyte, and void/carbon"* (p.7) · 그림 3a–c 단면 축 [판독 · 원래 래스터 눈금]: **260.5 × 260.0 µm** → 0.65 µm 복셀 **400 × 400** [카드 산술].  ★ [카드 해석] 단면 (260 µm) 이 양극 두께 (≈37–48 µm [카드 산술]) 보다 크므로 이 단면은 **두께 방향 단면이 아니라 집전체와 나란한 면** 이다 — 그러면 "위아래 = 적층압" 경계는 실제 적층압 방향 (면에 수직) 이 아니라 면 안의 y 방향에 걸린다 (원문은 단면 방향 · 이 선택을 적지 않는다).
- **지배식 (번호 없음 · p.7 · 렌더에서 옮김)**: (가) ∇·σ = 0 (준정적) · (나) **ε_ij = ε_ij^mech + ε_ij^diff = (1/E)[(1 + ν)σ_ij − ν σ_kk δ_ij] + c_max(1 − c/c_max)Ω/3 · δ_ij** — *"The mechanical strain component is obtained based on the linear elasticity formulation, whereas the diffusion-induced component is a function of the Li concentration, c, within the active material, and the partial molar volume of Li, Ω"* · *"The diffusion-induced component is only considered within the cathode active material, whereas within the solid electrolyte and void/carbon phases, it is zero."*
- **경계 · 반복**: *"The top and bottom boundaries are given the applied stack pressure as the boundary condition, whereas the side boundaries are kept constrained in the x-direction"* (적층압 값 [미확인] — 실험은 50 MPa) · *"simulations were repeated by using three distinct tomography slices for each cathode composition. The resulting stress metrics were averaged, and the standard deviations are presented"* (p.7).
- **표 1 (본문 p.4)** [인쇄]: c_max **52 500 mol m⁻³** (ref 3 = Jeong 2024) · E_SE **22 GPa** (ref 30 = Singh 2022 Cell Rep. Phys. Sci.) · ν_SE **0.27** (출처 없음) · E_AM **200 GPa** (ref 17 = Woodcox 2021 J. Power Sources) · ν_AM **0.3** · Ω **2 × 10⁻⁶ m³ mol⁻¹**.  ⚠ 같은 22 GPa 를 서론 (p.1) 은 ref **16 (Deng 2016 · 제1원리)** 로 인용 — 그 카드의 Li₆PS₅Cl 은 E 22.1 · **ν 0.37** [다른 카드 `deng2016_…` 표 III] 로 표 1 의 ν 0.27 과 다르다.  [카드 산술] SE K = E/(3(1 − 2ν)) = **15.9 GPa** · G = E/(2(1 + ν)) = **8.7 GPa** · AM K 167 · G 76.9 GPa.
- **표 1 에 없는 것**: 공극/탄소 상의 물성 (본문은 *"as detailed in Table S1"* 이라 하나 **SI 에 표가 없다**) · 농도장 c(x) 를 어떻게 정했나 (확산 · 반응식 없음 — 입자마다 균일 · SoC 비례인지 [미확인]) · "80 % 방전" 의 c/c_max · 무응력 기준 상태 · 평면 변형 / 평면 응력 · 격자 · 요소 수 · 풀이기 · 계산 비용 · 계면 조건 (붙음 / 미끄럼).
- **변형의 크기** [카드 산술]: Ω c_max / 3 = **0.035 (선 3.5 %)** → 부피 ≈10.5 % (c 를 0 → c_max 전부 쓰면) — 서론의 *"volume changes of up to ∼10%"* 와 같은 자릿수.  E_AM × 2.8 % (0.8 × 3.5 %) = **5.6 GPa** — 색 막대 ±5 GPa 의 자릿수와 맞는다 (가정: 80 % 방전 = c 범위의 80 % · 가까운 이웃이 완전히 막는 경우 · 크기 감각만).
- ⚠ **부호** [카드 산술 · 카드 해석]: 인쇄된 ε_diff = (c_max − c)Ω/3 는 리튬화 (c ↑) 에서 **줄어든다** (수축) — 본문은 *"an overall increase in the volumetric expansion of the composite electrode during lithiation"* (p.3–4 · ref 31 Koerver 2018) 라고 쓴다.  기준 상태가 인쇄되지 않아 식 · 본문 · 그림 S2 (방전 0 % 가 거의 무응력) 를 하나로 맞출 수 없다 — 인장 · 압축 자리 (어느 상이 어느 부호) 해석에 걸린다.  같은 그룹의 Jeong 2024 는 *"stress-free state in the fully delithiated state"* · ε = ĉΩ/3 로 적었다 [다른 카드 jeong2024 §3-7].
- **결과** [인쇄 p.3]: *"As lithiation progresses, significant stresses are generated within the cathodes due to the volume changes in the NCM, with the stress distribution being strongly dependent on microstructural stochasticity"* · *"increasing the NCM-to-solid electrolyte ratio yields higher stress magnitudes … leading to more severe formation of stress hotspots"* · *"Increasing NCM content within the cathode composite yields a nonlinear rise in high-stress areas"*.
  - **그림 3h (세 단면 평균 ± 표준편차)** [판독 · 벡터]: σ > +2 GPa (인장) **0.25 ± 0.08 · 1.23 ± 0.23 · 2.42 ± 0.07 %** · σ < −2 GPa (압축) **1.73 ± 0.42 · 2.90 ± 0.65 · 3.98 ± 0.33 %** · 85:15 ÷ 70:30 = 인장 **×9.6** · 압축 **×2.3** [카드 산술].  ⚠ 가로축 자리가 NCM wt% 에 비례 (70 → 80 → 85 의 간격 10 : 5) 이다.
  - **그림 3g (한 곡선 · 어느 단면인지 미인쇄 · 0.2 GPa 칸)** [판독 · 벡터 · 카드 산술]: 칸 합 99.9 · 99.8 · 99.6 % · 0 근처 (±0.1 GPa) 최고 22.8 · 18.2 · 16.8 % · > +2 GPa 0.18 · 1.14 · 2.29 % · < −2 GPa 1.29 · 2.52 · 3.47 % (그림 3h 평균보다 조금 작고 85:15 압축은 1.5 표준편차 밖) · 평균 σy −0.025 · −0.027 · −0.023 GPa · 표준편차 **0.69 · 0.88 · 1.00 GPa**.
  - **SI 그림 S2** (방전 0 · 40 · 80 %): 0 % 는 거의 무응력 (균일한 연노랑) · 40 % 에서 망 꼴의 압축 띠 (파랑) 와 인장 점 (빨강) 이 생기고 80 % 에서 커진다 [판독 · 색].  고응력은 NCM 덩이 사이의 좁은 목 · 띠에 모인다 [판독 · 그림 3d–f · 그 자리가 NCM 상인지 SE 상인지는 원문이 가르지 않는다].
- **저자의 기전 셋** (p.3–4): ① 같은 SoC 에서 NCM 이 많으면 부피 변화 총량 ↑ ② 무른 SE (*"much lower Young's modulus"*) 가 적어 *"mechanically compliant pathways"* ↓ ③ *"a higher coordination number of cathode particles for higher NCM content … enhances interparticle contact and restricts the freedom for individual particles to expand"* — ③ 의 CN 은 3D 망 (그림 2e) 의 값인데 응력은 2D 단면에서 계산했다 (2D 단면의 이웃 수는 3D CN 과 다르다 [카드 해석]).

### 3-5. 사이클 뒤 기계 열화 — FIB-SEM (p.5 · 그림 4 · SI 그림 S3 · `fig_4abc.png` · `fig_4def.png` · `fig_S3.png` · `txt_p5_fibsem_cracks.png` · `txt_p7_fibsem_xanes_method.png`)
- 방법 [인쇄 p.7]: 20 사이클 (0.1C 1 + 0.2C 19) 뒤 · 이온 빔 가공 **10 kV · 60 → 1.1 nA** (인쇄 그대로) · Helios G5 Dual Beam · BNL CFN.
- 결과 [인쇄 p.5]: 조립 직후 셋 다 *"intact NCM particles without visible cracks"* · 20 사이클 뒤 70:30 *"only a few narrow cracks less than 50 nm width appear in some NCM particles (Figure S3), but most particles remain intact"* · 80:20 · 85:15 *"extensive cracks develop within NCM particles"* (주황 화살표) · *"larger amounts of interfacial voids are visible in 80:20 and 85:15 cathodes"*.  균열 길이 · 부피 · 접촉 면적의 숫자 **없음** (단면 각 한 장).
- [판독 · 그림 4 · 10 µm 막대]: NCM 단면 지름 ≈2–15 µm · 조립 직후 SE 영역 안에 작은 검은 틈이 이미 보인다 (특히 70:30 · 85:15) · NCM 단면은 FIB 커튼 줄무늬가 있는 치밀한 원판.

### 3-6. 반응 불균일 — 3D XANES (p.6 · p.7 · 그림 5 · SI 그림 S4 · `fig_5ace.png` · `fig_5bdf.png` · `fig_5g.png` · `fig_S4.png` · `txt_p6_xanes_white_line.png`)
- 방법 [인쇄 p.6–7]: 흡수단을 가로지르는 여러 에너지에서 단층 촬영 → 흰선 에너지 = 산화 상태 (Ni · Mn 흰선이 높을수록 탈리튬) · *"The typical spatial resolution in 3D XANES is at the tens of nanometer scale"* · FXI (18-ID) · 사이클 뒤 가루를 지름 3 mm 폴리이미드 관에 에폭시 봉입 (Ar) · *"Spatial resolution of the image is 40 nm"* · TXM-Sandbox 재구성 · ImageJ · Avizo 분할.
- 결과 [인쇄 p.6]: 모두 1.9 V 까지 방전했는데 평균 Ni 흰선 **8353.4 · 8353.8 · 8353.9 eV** → *"lower degrees of Li ion intercalation in NCM particles and inefficient utilization of NCM"* · 입자 안 표준편차 **0.31 · 0.36 · 0.41 eV** · 80:20 · 85:15 입자 조각남 (*"The fractured NCM particles could further scatter into small pieces during the sampling process"*).
- ⚠ **그림 5g 곡선 통계** [판독 · 벡터 · 카드 산술]: 평균 **8353.24 · 8353.54 · 8353.70 eV** · 표준편차 **0.263 · 0.279 · 0.333 eV** · 최빈 8353.2 · 8353.5 · 8353.7 · 곡선 합 0.999 · 0.998 · 0.993 (0.1 eV 칸) → 인쇄 평균보다 **0.16 · 0.26 · 0.20 eV 낮고** 표준편차는 0.05–0.08 eV 작다 — 순서 · 방향은 같다.  그림 5g 가 *"over the particles in (a, c, e)"* (캡션) 인데 본문 통계가 같은 입자 · 같은 처리에서 왔는지 [미확인].  흰선 에너지 → Li 함량 환산식 · 색 막대 (±1.5 eV) 의 기준값 미인쇄.
- [판독 · 그림 5 · 10 µm 막대]: 나노 CT 입자 ≈8–13 µm · 80:20 · 85:15 에서 쐐기 모양으로 떨어져 나간 조각.

### 3-7. ★ 저자가 적은 한계 · 원문 안 어긋남
**저자 한계 (원문)**: ① 입자 사이 · 입자 안 응력의 기여는 *"challenging"* 이라 가르지 못하고, 70:30 · 80:20 의 첫 용량이 비슷하다는 데서 입자 안 (1 차 입자 이방 변형) 응력은 비슷하리라 보고 *"it is reasonable to conclude … primarily driven by increased interparticle stress"* (p.6 — 측정이 아니라 추론) ② 60:40 이면 기계는 낫지만 전자 전도 · 이용률이 나빠질 수 있다 (p.6 · ref 7) ③ 탄소와 공극을 분할에서 가르기 어렵다 (p.3).
**원문 안 어긋남 (카드가 본 것 — 고치지 않고 적는다)**:
1. 본문 p.7 *"as detailed in Table S1"* ↔ SI 에 표가 없다 (그림 S1–S4 뿐) · 본문 표 1 에는 SE · CAM 만 → **공극/탄소 물성 [미확인]**.  SI 안내 (*"Additional electrochemical measurement; chemo-mechanics modeling analysis; tomography characterization; and FIB-SEM images"*) 와 실제 SI (그림 넷) 도 다르다.
2. LPSCl E 22 GPa 의 출처 둘 — 서론 ref 16 (Deng 2016) ↔ 표 1 ref 30 (Singh 2022) · ν_SE 0.27 은 출처 없음 (Deng 의 ν 0.37 [다른 카드]).
3. 확산 변형 식의 부호 (리튬화 때 수축) ↔ 본문 "리튬화 때 팽창" · 기준 상태 미인쇄 (§3-4).
4. 그림 1a–c 곡선 끝 ↔ 인쇄값: 70:30 0.1C 158.6 vs 156.7 · 80:20 0.5C 114.1 vs 117.4 (§3-3).
5. 그림 1e 사이클 2 ↔ 그림 1d 0.2C (140.7 · 139.2 · 121.2 vs 136.6 · 137.3 · 128.0) — 셀 동일 여부 미인쇄.
6. 그림 5g 곡선의 평균 · 표준편차 ↔ 본문 인쇄 통계 (§3-6).
7. 응력 논증의 셋째 요인 (CN) 은 3D 값 ↔ 응력 계산은 2D 단면 (§3-4).
8. 표기: 본문 p.2 *"As the charging rate increases to 0.5C"* (보고한 값은 방전 용량) · Li–In *"Li and In foils … 95:5 weight ratio"* (어느 쪽이 95 인지 순서 외 근거 없음) · 표 1 텍스트 층은 위첨자가 값에 붙어 *"525003 · 2230 · 20017"* 로 나온다 (렌더로 52 500 [3] · 22 [30] · 200 [17] 확인).

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 사슬
- **시편**: 건식 혼합 → SE 80 mg 펠릿 80 MPa → 양극 (NCM 9 mg cm⁻²) · Li–In → 셀 전체 300 MPa 2 분 → 적층압 50 MPa · 30 °C 운전.  같은 꼴의 셀을 (가) XCT (*"cell assemblies in a PEEK die"* · 상태 미인쇄) (나) 율속 · 수명 (다) 20 사이클 뒤 FIB-SEM · 가루 XANES 에 썼다.
- **XCT → 분할 (Avizo) → 상 분율 · 기공망 모형 → NCM–NCM CN 분포**.  분할 · 분리 · 망 매개변수 미인쇄.
- **XCT 2D 단면 (조성마다 3 장) → 상 배정 → 선형 탄성 + 확산 변형 응력 (80 % 방전) → σy 지도 · 면적 분포 · > 2 GPa 면적 (평균 ± 표준편차)**.
- **20 사이클 → FIB-SEM 단면 (조성마다 1 장 + 확대 S3) · 나노 CT + XANES (입자 몇 개)**.

### 4-2. 모델 사슬
분할된 XCT 단면 → 상마다 E · ν (표 1) → 활물질에만 고유 변형 (c 의 함수) → 준정적 평형 → σy.  **압밀 · 성형 단계 (300 MPa) 는 모델에 없다** — 방전 0 % 가 무응력이고 (SI 그림 S2), 조립 압력이 남긴 잔류 응력 · 접촉 상태는 들어가지 않는다.  전기화학 (확산 · 반응) 식도 없다 — c 를 어떻게 정했는지 [미확인].

### 4-3. 입자 처리 ★
- 실험 (XCT): **복셀 분할된 상** → NCM 은 기공망 모형에서 '입자 (마디)' 와 '연결 (목)' 으로 바뀐다 (분리 기준 미인쇄) · SE · 탄소는 입자로 다루지 않는다.
- 모델: **2D 연속체 (상마다 E · ν · 선형 탄성)** — 입자 형상 변화 · 소성 · 접촉 법칙 · 미끄럼 · 분리 · 파괴 **없음** · NCM 끼리 맞닿은 자리는 같은 상의 연속 영역 (픽셀) 이 되어 붙어 있다 [카드 해석] · NCM–SE 계면도 붙어 있다 [카드 해석 · 원문 미기재].
- DEM 처럼 구 · 점접촉으로 두는 부분은 **없다** (DEM 이 등장하지 않는다).

### 4-4. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **말 없음** (본문 · SI 에 DEM · discrete · particle simulation 낱말 0 회).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — **말 없음**: 본문 · SI 에 *"plastic"* 0 회 · 모델은 *"The mechanical strain component is obtained based on the linear elasticity formulation"* (p.7) 로 소성 · 파괴를 **넣지 않았고** 이유를 적지 않았다.  그 결과 응력이 ±5 GPa (색 막대) · "> 2 GPa 면적" 까지 탄성으로 남는다 — LPSCl 이 실제로 그만큼 버틴다는 뜻이 아니다 [카드 해석].  계산 비용 · 격자 [미확인].
3. **2D / 3D** — XCT · CN 은 3D (그림 2c 망) · 응력은 *"a 2D computational domain"* (p.7) · *"two-dimensional (2D) tomography slices"* (p.3) · 2D → 3D 전이에 대한 말 **없음** · 3D CN 을 2D 응력 해석의 원인으로 묶는다 (§3-4).
4. **압력을 뺄 때의 거동** — **다루지 않았다**: 조립 300 MPa → 운전 50 MPa 사이의 탈압 · 되돌아옴 · 그 상태의 기공 · 접촉 변화 없음 · 모델은 적층압을 경계로만 둔다 (값 미인쇄).

### 4-5. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| micro-CT (HEX 27-ID) | 단색 50 keV 흡수 단층 · 복셀 0.65 µm · 시야 2 × 2 mm² · FBP 재구성 |
| 기공망 모형 (PNM) | 분할된 한 상 (여기선 **NCM 상**) 을 마디 (입자) 와 목 (연결) 의 망으로 바꾼 것 — 이름은 '기공' 이지만 고체 상에 썼다 |
| 배위수 (CN) | 한 NCM 입자에 '연결' 된 이웃 NCM 입자 수 — 판정 기준 미인쇄 |
| 공극/탄소 상 | 탄소가 가벼워 빈 곳과 구별이 안 돼 한 클래스로 분할한 영역 |
| 메조 화학–역학 모델 | 분할 단면 위 상마다 E · ν · 활물질 고유 변형 (Ωc) 의 선형 탄성 응력 |
| 3D XANES | 흡수단 여러 에너지의 나노 단층 → 화소마다 흰선 에너지 (Ni 산화 상태) |
| 흰선 (white-line) 에너지 | XANES 봉우리 자리 — 높을수록 탈리튬 (Ni 산화) |
| 유지율 | 50 번째 ÷ 2 번째 (첫 0.2C) 사이클 방전 용량 [카드 산술로 확인] |

---

## 5. Figure set ★
| 그림 | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| **그래픽 초록** (`fig_toc_graphical_abstract.png`) | 낮은 / 높은 CAM 비 그림 — 높은 쪽에서 CAM–CAM 목마다 응력 점 | 발표용 개념도 (값 없음) |
| **Fig. 1** (`fig_1.png` · 패널 `fig_1a`–`1e`) | (a–c) 조성별 충방전 0.1 / 0.2 / 0.5C · (d) 율속 · (e) 0.2C 50 사이클 + 유지율 표지 | 전기화학 결과 (흐름 밖) — 곡선 끝 · 사이클 값 [판독 · 벡터] |
| **Fig. 2** (`fig_2.png` · `fig_2a`–`2e`) | (a) 2D XCT 단면 (1 mm) · (b) 분할 · (c) NCM 망 · (d) 상 분율 막대 (숫자 인쇄) · (e) ★ CN 분포 | ★ (e) 우리 AM–AM CN 분포와 같은 축 (빈도 vs 정수 CN) — 모양 · 방향 대조 · (d) 공극 + 탄소 상한 |
| **Fig. 3** (`fig_3.png` · `fig_3abc` · `3def` · `3g` · `3h`) | (a–c) 모델 입력 단면 260 µm · (d–f) σy 80 % 방전 · (g) 응력 분포 · (h) > 2 GPa 면적 | 탄성 상한 응력의 그림 언어 — 우리 MPM 응력장과 **나란히 보기만** (구성식 다름) · 보고 꼴 (세 단면 평균 ± sd) |
| **Fig. 4** (`fig_4.png` · `fig_4abc` · `4def`) | FIB-SEM 조립 직후 / 20 사이클 뒤 · 주황 화살표 균열 | R7 (AM 파괴) 의 정성 표적 · NCM 크기 판독 |
| **Fig. 5** (`fig_5.png` · `fig_5ace` · `5bdf` · `5g`) | 나노 CT 입자 · Ni 흰선 지도 · 히스토그램 | 흐름 밖 (반응 불균일) · 그림 통계 ↔ 인쇄 통계 어긋남 표지 |
| **Table 1** (`tab_1.png`) | 모델 매개변수 (c_max · E · ν · Ω) | E_SE 22 · ν 0.27 = 우리 DFT (22.06 · ν 0.360) 와 E 만 같음 |
| **SI Fig. S1** (`fig_S1.png`) | dQ/dV 2 · 20 · 50 사이클 | 흐름 밖 |
| **SI Fig. S2** (`fig_S2.png`) | 단면 + σy 방전 0 · 40 · 80 % | 무응력 기준 = 방전 0 % 의 근거 그림 |
| **SI Fig. S3** (`fig_S3.png`) | 70:30 의 좁은 균열 확대 (5 µm 막대) | "< 50 nm" 의 그림 |
| **SI Fig. S4** (`fig_S4.png`) | 나노 CT 입자 앞 · 위 보기 | 조각난 입자 3D |
| 식 크롭 2 (`eq_01` · `eq_02`) · 근거 문단 24 (`txt_p*`) | 번호 없는 두 식 · 인용 문장 · 참고문헌 (3) · (7) · (16)–(17) · (29)–(30) | 보고서 붙임 |

## 6. Post-processing ★
- **상 분율**: 분할 복셀 세기 (진밀도 불필요) — 공극과 탄소는 한 클래스.
- **CN**: 기공망 모형 (Avizo) 의 NCM 마디마다 연결 수 → 정수 빈도 분포 · 평균.
- **응력 지표**: σy 지도 → 0.2 GPa 칸 면적 분포 (합 100 %) → |σy| > 2 GPa 인장 · 압축 면적 → 세 단면 평균 ± 표준편차.
- **XANES**: 화소별 흰선 에너지 → 입자 안 표준편차 · 조성별 히스토그램 (0.1 eV 칸).
- **수명**: 유지율 = C50 / C2 [카드 산술로 확인].
- **판독 (이 카드)**: 벡터 그림 (1 · 2d–e · 3g–h · 5g · S1) = PDF 경로 꼭짓점 × 눈금 (벡터) · 래스터 (2a–c · 3a–f · 4 · 5a–f) = 눈금 · 막대로 크기만 — digitized.csv note 열에 방법 전부 (스크립트는 큐레이터 작업 폴더 · 커밋 밖).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · 작업 가지 `docs/data/` 출처를 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **측정 상태 · 연산자 · 재료 조건이 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| AM–AM 배위수 (조성별) | XCT · 기공망 '연결' · 평균 **4.8 · 6.5 · 7.4** · sd 2.43 · 2.63 · 3.08 (NCM:LPSCl 70 · 80 · 85 wt%) | DEM `am_am_cn` (LHS-130 · LIGGGHTS · 300 MPa · E_SE 1.35 GPa · 같은 질량비 기준 `am_pct` 70 · 80 · 85) 중앙 **3.91 · 4.92 · 5.36** (n 21 · 21 · 24 · 범위 2.16–4.94 · 2.12–5.90 · 3.51–6.12) · 입자간 표준편차 중앙 2.08 · 2.60 · 2.47 [우리 · 작업 가지 `docs/data/lhs_handover_20261001.csv` 읽기 · 정의 = `calc_am_am_cn` 열 사전 J20-j] · 130 행 최댓값 6.63 | **방향 같음** (AM 질량비 ↑ → CN ↑ · 퍼짐 비슷) · XCT 가 0.9–2.0 (×1.23–1.38) 높다 · Park 85:15 평균 7.4 는 우리 130 행 최댓값 위 → **연산자 (근접 연결 vs 겹침) · 입경 분포 · 상태가 다르다** (§7-2) — 값 맞춤 금지 |
| AM 부피분율 | XCT NCM **0.391 · 0.506 · 0.500** | DEM `phi_am_mass_conserving` 중앙 **0.457 · 0.559 · 0.604** [우리 · 같은 파일] | 다른 연산자 (분할 복셀 ↔ 질량 보존 합집합) · 조성 같은 축 · 우리 쪽이 높다 (공극 정의 · 탄소 · 분할 차) |
| 공극 | XCT **공극 + 탄소** 14.7 · 18.1 · 23.3 % (300 MPa 조립 · 촬영 압력 미인쇄) | DEM `porosity_union_exact_pct` 중앙 **7.3 · 10.5 · 14.2 %** [우리 · 같은 파일] · 랩 표준 순수 SE 10–13 % (300 MPa) · 진밀도 1.64 [우리 · CLAUDE.md · 고정] | **방향 같음** (AM ↑ → 공극 ↑) · 그들 값은 탄소 포함 = 공극의 상한 · 절대값 대조 불가 |
| SE 탄성 (모델 입력) | E_SE **22 GPa** · ν **0.27** (K 15.9 · G 8.7 GPa [카드 산술]) | DFT E_VRH 22.06 · B₀ 26.23 · ν 0.360 · G 8.11 GPa · DEM E_eff 1.35 · MPM 1.53 GPa (ν 0.49 · K 25.5) [우리] | E 숫자는 우리 DFT 와 같다 (Deng 2016 경로) · **ν · K 가 다르다** · 그들 모델은 압밀이 없어 연화가 필요 없다 |
| AM 탄성 | E_AM **200 GPa** · ν 0.3 | DEM NCM 140 GPa [우리] | 다른 입력값 |
| 응력장 | 2D · 선형 탄성 · 사이클 (80 % 방전) · ±5 GPa · > 2 GPa 면적 (인장 0.25 → 2.42 · 압축 1.73 → 3.98 %) | MPM (J2 · σ_y 0.30 GPa · 압밀 중) — SE 의 편차 응력은 항복에서 막힌다 · AM 은 얼린 장애물 · 사이클 응력 없음 [우리] | **다른 하중 (사이클 고유 변형 ↔ 압밀) · 다른 구성식 (탄성 ↔ 소성)** — 숫자 대조 불가 · "> 2 GPa" 는 우리 MPM 의 SE 에선 뜻이 없다 |
| 사이클 열화 | 유지율 94.6 · 76.8 · 74.1 % · 80:20 · 85:15 균열 · 계면 공극 | A10 접촉 원장 (`scripts/cycle_contact_ledger.py`): AM–SE · SE–SE 만 Bucci CZM · **AM–AM 은 다시 닫힘** (사이클 손상 없음) · AM 파괴 없음 [우리 · CLAUDE.md A10] | 저자는 열화를 **입자 사이 (AM–AM) 응력** 탓으로 본다 → 우리 A10 이 빠뜨린 경로 후보 (R7 · 흐름 밖) |

### 7-2. ★ 배위수 정의 대조 — "같은 이름 · 다른 연산자"
| 항목 | Park 2025 (XCT) | 우리 DEM `am_am_cn` |
|---|---|---|
| 입자 | 분할된 NCM 영역 → 기공망 모형의 마디 (분리 방법 미인쇄) | 구 (AM_P · AM_S · mono 는 AM) — 정확한 기하 |
| '연결' 판정 | 기공망 모형의 목 (Avizo · 거리 문턱 미인쇄) · 복셀 0.65 µm — 틈 < 1 복셀이면 붙어 보일 수 있다 [카드 해석] | 접촉 덤프의 쌍 = 겹침 δ > 0 (LIGGGHTS) |
| 상태 | 300 MPa 2 분 조립 뒤 · 촬영 때 적층압 (50 MPa) 유지 여부 · 사이클 전후 미인쇄 | 300 MPa 압축 끝 덤프 한 프레임 · 하중 제거 회복 없음 [우리] |
| 모집단 | *"a given particle"* 전부 (CN 0 = 0.73 % 가 분포에 있다) · 슬래브 면 (분리막 · 집전체) 입자 포함 여부 미인쇄 | AM 전 입자 (접촉 0 · 벽 접촉 포함 · 벽 입자는 CN 이 낮다 — 열 사전 한정어) |
| 조성 기준 | NCM : LPSCl **질량비** (탄소 3 phr 따로) | `am_pct` = AM : SE **질량비** (탄소 없음) — **같은 기준** |
| 입경 | NCM 단면 ≈2–15 µm [판독] · LPSCl 미인쇄 · D50 미인쇄 | LHS 설계 r_AM_P · r_AM_S · r_SE (bimodal · mono 섞임) |
| 두께 / 영역 | 양극 ≈37–48 µm [카드 산술] · 분석 영역 ≈1 mm 폭 (그림 2a) | RVE 50 µm · 두께 31–70 µm [우리 · LHS 설계] |
| 통계 | 평균 · 분포 (정수 빈도) | 평균 · 모집단 표준편차 |

⇒ **맞대기 규칙 (결과 전에 적어 둠)**: ① 모양 · 방향 (평균 · sd · 오른쪽 꼬리가 AM 질량비와 함께 움직이는가) 만 견준다 ② 우리 쪽은 **두 연산자** 로 같이 낸다 — 겹침 (δ > 0) 과 '틈 ≤ 0.65 µm' (XCT 복셀 하나와 같은 근접 문턱 · 카드 제안) — 둘 사이에 XCT 값이 오는지가 연산자 차이의 크기 ③ 벽 · 슬래브 면 입자를 뺀 값을 따로 ④ 값 차이를 모델 오차로 읽지 않는다 (frame[4] — 맞추지 않는다).

### 7-3. 응력 모델 ↔ 우리 MPM · A10
- 그들의 "고응력 면적" 은 **소성 · 파괴 · 접촉 열림이 없는 탄성 상한** 이다.  우리 MPM 은 SE 에 J2 항복 (σ_y 0.30 GPa · 일축 0.318 GPa [우리 CLAUDE.md]) 이 있어 같은 하중이면 SE 편차 응력이 그 위로 못 간다 — 이 그림의 ±5 GPa 를 우리 MPM 결과와 같은 표에 넣지 않는다.
- 그들은 압밀 이력을 넣지 않고 방전 0 % 를 무응력으로 둔다 (SI 그림 S2).  우리 계획의 단계 5 → 6 (압밀 → 탈압) 이 남기는 잔류 응력 · 접촉 상태가 사이클 응력의 출발점이 된다는 점을 이 논문은 다루지 않는다 — **우리 쪽이 줄 수 있는 것**.
- A10 (사이클 접촉 원장) 은 AM–AM 접촉을 사이클마다 다시 닫히게 두고 AM 파괴를 넣지 않는다 [우리 CLAUDE.md A10].  이 논문은 AM 질량비가 높을 때의 열화를 입자 사이 응력 → NCM 균열로 설명한다 (추론 · p.6) — A10 의 "AM–AM 재폐합" 가정에 대한 **정성적 반대 증거 후보** (흐름 밖 · R7).

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **실험 (구조 · 연결 수 · 열화 관찰)** + **2D 탄성 응력** — 우리 분업으로는 DEM 쪽 (배위수 · 상 분율) 의 **측정 쪽 짝** 과 MPM 쪽 (응력장) 의 **탄성 · 2D 한정판**.
- 없는 반쪽: 압밀 과정 (입자 재배열 · SE 소성 유동 · AM 하중 분담) · 탈압 · 접촉 열림 · 파괴의 계산.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = LiNbO₃ 코팅 NCM811 + NEI Li₆PS₅Cl + C65 — 계는 같지만 **연산자 (XCT 분할 · 기공망) · 조성 표 (탄소 3 phr) · 상태 (300 MPa 조립 뒤 · 촬영 압력 미인쇄)** 가 다르다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ **배위수 연산자를 결과 전에 등록하는 꼴** — XCT 쪽 '연결' 은 근접 문턱 ≈ 복셀 (0.65 µm) 일 수 있고 판정 기준이 미인쇄 → 우리 CN 을 낼 때 ① 겹침 δ > 0 ② 틈 ≤ 0.65 µm ③ 벽 입자 제외 를 칸으로 둔다 (§7-2) · ★ **공극 표지**: "공극" 이 탄소를 포함한 상한일 수 있다 → 문헌 공극을 받을 때 '공극 + 탄소' 표지 칸 | 진밀도 기공 · 압력별 곡선 없음 |
| **단계 1** (3D 메모리 · 장 수) | 크기 감각: XCT 시야 2 × 2 mm² @0.65 µm ≈ 3 077² 복셀/단면 [카드 산술] · 모델 단면 400 × 400 · 양극 ≈37–48 µm (NCM 3–5 지름) → 우리 RVE 50 µm 가 두께 방향으로 이 양극 전체에 해당 | 입자별 장 · 메모리 숫자 없음 |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | 반면교사: 2D 단면 위 연속체 (한 상 = 한 영역) 는 맞닿은 AM 끼리를 **붙은 한 덩이** 로 다룬다 — 접촉을 떼어 보지 않으면 "AM–AM 목에 응력이 몰린다" 는 그림 (3d–f) 의 크기가 붙음 가정에 묶인다 [카드 해석] | 한 속도장 ↔ 입자별 속도장 비교 없음 |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 없음 (순수 SE 기공 · 항복 없음) · 탄성 입력 ν 0.27 이 Deng 의 0.37 · 우리 DFT 0.360 과 다르다는 것만 | 맞춤 표적 아님 |
| **단계 5** (3D 복합 압밀) | ★ **결과 전 대조 항목 (방향 · 모양)**: 같은 300 MPa (2 분) 에서 AM 질량비 70 → 80 → 85 % 일 때 ① NCM–NCM CN 평균 4.8 → 6.5 → 7.4 · sd 2.4 → 3.1 · P(CN ≤ 2) 16 → 3 % ② NCM 부피 0.391 → 0.506 → 0.500 ③ 공극 + 탄소 14.7 → 18.1 → 23.3 % (공극 상한) — 우리 3D 복합 압밀 (DEM · 앞으로 MPM A′) 이 **같은 방향 · 비슷한 퍼짐** 을 내는지 | 촬영 압력 미인쇄 · 입경 미인쇄 · 탄소 포함 · 하중 몫 없음 |
| **단계 6** (탈압 · 되돌아옴) | 반면교사: 조립 300 MPa → 운전 50 MPa 의 탈압 상태를 그들은 계산하지 않고 사이클 응력의 출발을 무응력으로 둔다 → 우리 단계 6 의 결과 (잔류 응력 · 열린 접촉) 가 **사이클 응력 계산의 출발 상태** 로 쓰일 자리가 있다 [카드 해석] | 탈압 자료 없음 |
| **단계 7** (형상 · 피복 · 수송) | 공극 + 탄소 · NCM 망 연결 · 그림 3a–c 의 SE · 공극 배치 (그림) · 저자의 "85:15 SE 망 고굴곡" 은 측정 없음 · ★ CN 분포의 정수 빈도 꼴 = 우리 접촉망 보고 꼴 (`am_am_cn` · `_std` 에 분포 열을 더할 때) | 수송 측정 (EIS · tortuosity) 없음 |
| **후보 D0** (지금 DEM) | ★ LHS-130 `am_am_cn` 중앙 3.91 · 4.92 · 5.36 (70 · 80 · 85 wt%) 과 같은 질량비 축에서 **방향 · 퍼짐 같음 · 값은 0.9–2.0 낮음** (§7-1) — 연산자 차이 (겹침 ↔ 근접 연결) 를 먼저 재야 해석이 선다 | DEM 은 탄소 · LiNbO₃ 코팅 · 실제 입형을 갖지 않는다 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 슬래브 면 (분리막 · 집전체) 에 닿은 NCM 의 CN 이 낮아질 수 있다는 경계 효과 — 판 · 벽 접촉 규칙을 쓸 때 경계 입자 CN 을 따로 보고 | 원문 값 없음 |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | A′ 가 낼 수 있는 것 = AM–AM 접촉의 열림 · 미끄럼 (그들 모델은 못 한다) → "AM–AM 목 응력" 을 접촉이 열리는 경우와 붙은 경우로 갈라 볼 수 있다 · 결과 전 대조 = 위 단계 5 셋 | 그들 숫자를 A′ 결과의 맞춤 표적으로 쓰지 않는다 |
| **후보 B** (입자별 FE + 접촉) | 없음 — 그들 모델은 상 연속체 (입자 · 접촉 없음) | — |
| **후보 C** (큰 변형 접촉 DEM · MDR 류) | 없음 | — |
| **후보 C′** (항복 캡 탄소성 접촉 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀 · 캡 소성 · Heckel) | 없음 (압밀 곡선 없음) | — |
| **U0–U6** | **U1** (해상도) 쪽 경고: 0.65 µm 복셀에서 NCM ≈3–23 복셀/지름 · SE 크기 미인쇄 — 연결 판정이 해상도에 묶인다 · **U6** (작은 조밀 충전의 해상도 수렴) 의 관측량에 CN 분포 (정수 빈도) 를 넣을 근거 | U0 · U2–U5 없음 |
| **R1–R7** | **R7** (AM 파괴): 20 사이클 뒤 80:20 · 85:15 의 넓은 균열 · 70:30 의 < 50 nm 균열 (정성) · **R1** (AM 하중 분담): 탄성 AM (200 GPa) 이 고유 변형을 받는 상 — 압밀 하중 분담은 없음 · **R2** (미끄럼 · 분리): 계면 공극 관찰 (정성) · 계산 없음 | R3 · R4 · R5 · R6 없음 (R5 — 맞춘 값 0 개 · 전부 인용 물성) |
| **결과 전 대조 항목** | ① AM 질량비 70 → 85 % (300 MPa 조립) 의 **NCM–NCM CN 평균 4.8 → 7.4 · sd 2.4 → 3.1** (XCT · 복셀 0.65 µm · 기공망 · 판정 기준 미인쇄) ② **NCM 부피 0.391 · 0.506 · 0.500 · 공극 + 탄소 0.147 · 0.181 · 0.233** ③ (흐름 밖 · A10) 유지율 94.6 · 76.8 · 74.1 % 와 균열 정성 — 맞추는 데 쓰지 않음 | 순수 SE 랩 표준 (10–13 % · 1.64) 과 같은 표에 넣지 않는다 · 탄성 응력 ±5 GPa 는 대조 항목이 아니다 |

- **재료 · 차원 · 조건 차이**: 재료 계는 같다 (LPSCl + NCM811) — 그러나 LiNbO₃ 코팅 · C65 3 phr · NEI 입경 미상 · XCT 분할 연산자 · 300 MPa 2 분 조립 (우리 DEM 300 MPa 목표 압밀 · 판 고정) · 촬영 상태 미인쇄 · 30 °C 운전.  응력은 2D · 탄성 · 사이클 (우리 MPM 은 3D · 소성 · 압밀).

## 9. 적용 인사이트 (행동)
1. **결과 전 대조 항목 등록 (단계 5)**: "AM 질량비 70 → 80 → 85 % (300 MPa) 에서 AM–AM 배위수 평균 4.8 → 6.5 → 7.4 · sd 2.4 → 3.1 (Park 2025 · XCT 0.65 µm · 기공망)" 을 **방향 · 퍼짐 항목** 으로 — 값은 맞추지 않는다.
2. **CN 연산자 두 판 (단계 0 · D0)**: 우리 DEM 침대에서 AM–AM CN 을 겹침 (δ > 0) 과 틈 ≤ 0.65 µm 로 함께 계산해 둘의 차이를 잰다 (근접 문턱이 CN 을 얼마나 올리는지).  XCT 값 (4.8 · 6.5 · 7.4) 이 그 띠에 들어오는지를 결과 전에 적고 본다.  벽 입자 제외 값도 같이.
3. **공극 인용 꼬리표**: 문헌 "공극" 이 탄소를 포함하는지 (이 논문은 포함) · 진밀도 분모가 있는지 · 촬영 때 압력을 함께 적는다.
4. **탄성 응력 숫자 비교 금지**: ±5 GPa · "> 2 GPa 면적" 은 탄성 상한 — 우리 MPM (J2 소성) 응력 · 랩 항복 값 옆에 놓지 않는다.  쓸 수 있는 것은 "AM 비율 ↑ → 고응력 면적 비선형 ↑" 의 방향과 보고 꼴 (세 단면 평균 ± sd).
5. **흐름 밖 (A10 · 열화)**: 우리 생산 조성 (ps45 기준 NCM 81.6 : LPSCl 18.4 wt% [다른 카드 gandla2026 L335]) 은 이 논문의 80:20 과 85:15 사이 — 균열 · 유지율이 크게 나빠지는 구간이다.  A10 의 "AM–AM 재폐합 · AM 파괴 없음" 가정이 그 구간에서 빠뜨리는 것을 1저자 결정 항목으로 올린다.
6. **2D ↔ 3D 묶음 주의**: 3D CN 을 2D 응력의 원인으로 묶은 논증 (p.4) 을 인용할 때 차원 한정을 붙인다.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In LiNbO₃-coated NCM811–Li₆PS₅Cl composite cathodes pressed at 300 MPa, raising the NCM:LPSCl mass ratio from 70:30 to 80:20 and 85:15 raised the mean NCM–NCM coordination number measured by synchrotron X-ray tomography (0.65 µm voxels, pore-network model) from 4.8 to 6.5 and 7.4 (Park et al., *ACS Nano* 19 (2025) 22262)."
- "A 2D linear-elastic chemo-mechanical model on the tomography slices showed a nonlinear rise of the area under |σy| > 2 GPa with NCM content, and after 20 cycles extensive NCM cracking appeared only in the 80:20 and 85:15 cathodes (capacity retention 94.6, 76.8 and 74.1 % after 50 cycles at 0.2C)."
- 국문 (한정어와 함께): *"같은 300 MPa 조립에서 NCM 질량비를 70 → 85 % 로 올리면 XCT (복셀 0.65 µm · 기공망) 로 센 NCM–NCM 연결 수가 4.8 → 7.4 로 오르고 분포가 넓어진다 (Park 2025) — 연결 판정 기준이 인쇄되지 않아 DEM 접촉 수와는 모양 · 방향만 견준다."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**: §3-7 의 ①–③.
**카드가 본 한계**
1. **배위수 연산자 미인쇄** — 거리 문턱 · 분리 방법 · 망 매개변수 · 경계 입자 처리 없음 → DEM 접촉 수와 같은 양이라고 쓰지 않는다.
2. **공극 = 공극 + 탄소** · 진밀도 기공 없음 · 압력별 아님 · 촬영 때 압력 미인쇄.
3. **응력 = 2D · 선형 탄성** · 소성 · 파괴 · 접촉 · 박리 · 압밀 이력 없음 · 공극/탄소 물성 · 적층압 값 · c(x) · 기준 상태 · 격자 · 풀이기 미인쇄 · 식 부호 ↔ 본문 '팽창' 어긋남.
4. **단면 방향** — 260 µm 단면은 면과 나란한 면일 수밖에 없다 [카드 산술 · 해석] → "위아래 = 적층압" 이 실제 방향과 다르다.
5. **인과는 추론** — "입자 사이 응력이 주원인" 은 첫 용량이 비슷하다는 데서 나온 추론 (p.6) · 균열 · 공극 정량 없음 · FIB-SEM 단면 각 한 장.
6. **수치 어긋남**: 그림 1a–c 곡선 끝 둘 · 그림 1e ↔ 1d · 그림 5g ↔ 본문 XANES 통계 (§3-7).
7. **입경 · PSD · 코팅 두께 미인쇄** — CN 은 입경 분포에 강하게 걸리는데 그 정보가 없다.
8. **전이 한계**: 같은 계라도 LiNbO₃ 코팅 · C65 3 phr · 300 MPa 2 분 · 30 °C · 9 mg cm⁻² · 한 배치.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| (23) | Choi, S.; Jeon, M.; Ahn, J.; Jung, W. D.; Choi, S. M.; Kim, J.-S.; Lim, J.; Jang, Y.-J.; Jung, H.-G.; Lee, J.-H.; et al. Quantitative analysis of microstructures and reaction interfaces on composite cathodes in all-solid-state batteries using a three-dimensional reconstruction technique. ACS Appl. Mater. Interfaces 2018, 10, 23740−23747. | ★ 14.7 % 공극/탄소가 *"similar to prior studies"* 의 근거 · 3D 재구성 복합 양극 정량 — 카드 없음 (shi2019 · nakamura2020 카드가 인용만) |
| (9) | Naik, K. G.; Jangid, M. K.; Vishnugopi, B. S.; Dasgupta, N. P.; Mukherjee, P. P. Interrogating the Role of Stack Pressure in Transport-Reaction Interaction in the Solid-State Battery Cathode. Adv. Energy Mater. 2024, No. 2403360. | ★ 같은 모델 그룹의 **적층압** 의존 양극 모델 (경계 적층압 값 · 구성식 단서) — 카드 없음 |
| (14) | Kim, S. Y.; Cha, H.; Kostecki, R.; Chen, G. Composite cathode design for high-energy all-solid-state lithium batteries with long cycle life. ACS Energy Lett. 2023, 8, 521−528. | 고 CAM 비율 복합 양극 설계 · 기계 열화 — 카드 없음 (여러 카드가 인용만) |
| (30) | Singh, D. K.; Henss, A.; Mogwitz, B.; Gautam, A.; Horn, J.; Krauskopf, T.; Burkhardt, S.; Sann, J.; Richter, F. H.; Janek, J. Li6PS5Cl microstructure and influence on dendrite growth in solid-state batteries with lithium metal anode. Cell Rep. Phys. Sci. 2022, 3, No. 101043 | 표 1 의 E_SE 22 GPa 출처 (서론은 ref 16) — 그 논문에 22 GPa 가 있는지 [미확인] · 카드 없음 |
| (17) | Woodcox, M.; Shepard, R.; Smeu, M. First principles investigation into the interwoven nature of voltage and mechanical properties of the LixNMC-811 cathode. J. Power Sources 2021, 516, No. 230620. | E_AM 200 GPa 출처 (Li 함량 의존 NMC811 탄성) — 카드 없음 |
| (4) | Lin, L.; Ayyaswamy, A.; Zheng, Y.; Fan, A.; Vishnugopi, B. S.; Mukherjee, P. P.; Hatzell, K. B. Nonintuitive role of solid electrolyte porosity on failure. ACS Energy Lett. 2024, 9, 2387−2393. | 같은 그룹 · SE 기공과 파괴 — 카드 없음 (lei2026 · thompson2026 이 인용만) |
| (21) | Jangid, M. K.; Cho, T. H.; Ma, T.; Liao, D. W.; Kim, H.; Kim, Y.; Chi, M.; Dasgupta, N. P. Eliminating chemo-mechanical degradation of lithium solid-state battery cathodes during 4.5 V cycling using amorphous Nb2O5 coatings. Nat. Commun. 2024, 15, No. 10233. | 코팅으로 화학–기계 열화 억제 (초록의 'coatings' 제안과 같은 축) — 카드 없음 |
| (31) · (11) · (12) | Koerver 2018 EES 11, 2142 · de Biasi 2017 J. Phys. Chem. C 121, 26163 · Li 2020 Chem. Mater. 32, 6358 | 부피 변화 · 두께 방향 SOC — Koerver 2018 은 같은 묶음 다른 트리에서 카드 진행 (후보 N-9) · 나머지는 카드 없음 |
| (3) · (7) · (13) · (16) · (18) | Jeong 2024 · Bielefeld 2019 · Parks 2023 · Deng 2016 · Stavola 2023 | 정본 카드 있음 (`jeong2024_…` · `bielefeld2019_…` · `intergranular_cracking_nmc811_jmca2023` · `deng2016_…` · `stavola2023_…`) |

## 13. [미확인] 목록 (본문 8 쪽 + SI 5 쪽 전수에 없음)
1. **배위수 판정 기준** — 거리 문턱 · 입자 분리 (watershed 등) · 기공망 모형 매개변수 · 경계 (슬래브 면) 입자 처리 · 분석 부피 · 입자 수.
2. XCT 시편의 촬영 때 압력 (50 MPa 유지 여부) · 사이클 전후 · 분할 방법 (문턱 · 필터).
3. 진밀도 (NCM811 · LPSCl · C65) · 질량 · 진밀도 기공 · 탄소의 부피 몫 · 양극 두께.
4. NCM811 · LPSCl 입경 · D50 · 단결정 / 다결정 (다결정으로 읽힘) · LiNbO₃ 코팅 두께 · 혼합 방법.
5. 모델: 공극/탄소 물성 (*"Table S1"* 없음) · 적층압 값 · c(x) 정하는 법 · "80 % 방전" 의 c/c_max · 무응력 기준 · 평면 변형 / 응력 · 격자 · 요소 수 · 풀이기 · 계산 비용 · 계면 조건 · 단면 방향.
6. ν_SE 0.27 의 출처 · Singh 2022 에 22 GPa 가 있는지.
7. 그림 2c 공의 색 뜻 · 그림 3g 가 어느 단면인지 · 그림 5 색 막대 기준값 · 흰선 에너지 → Li 함량 환산.
8. 그림 1e 셀과 그림 1d 셀이 같은지 · 그림 1a–c 곡선 끝 ↔ 인쇄값 차이의 이유 · 그림 5g ↔ 인쇄 통계 차이의 이유.
9. Li–In 의 Li : In 비 (어느 쪽이 95).
10. 균열 · 계면 공극의 정량 (길이 · 부피 · 접촉 면적).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 본문 8 쪽 + SI 5 쪽을 글자 층 추출 + 전 쪽 렌더로 읽음.  서지 = 본문 p.1 (제목 · 저자 9 명 · DOI · *"Cite This: ACS Nano 2025, 19, 22262−22269"* · 접수 · 수정 · 승인 · 출판일) · p.7 (소속 · ORCID · 교신) · p.7–8 (감사 · 연구비).  SI p.1 = 같은 제목 · 저자 · 소속.  원문 낱말 셈: DEM · discrete = 0 · plastic = 0 · elastic 4 (본문) · 2D 4 · two-dimensional 1 · unload · release = 0 · contact 5 (*"interparticle contact"* · *"interfacial contact loss"* · *"solid−solid contact"* 등).
- 그림 크롭 **56 장** = 도구 10 (그림 1–5 · SI 그림 S1–S4 · 표 1 — 열어 보고 전부 그대로 둠 · 캡션만 고침: f1 · f2 · f3 · f5 는 이웃 본문이 캡션에 붙어 잘라냄 · t1 은 위첨자가 값에 붙어 52500/22/200 + 참고 번호로 고침) + 손 크롭 46 (그래픽 초록 1 · 패널 19 · 식 2 · 근거 문단 24).  본 뒤 다시 렌더한 것 24 (패널 1a–1e · 2a–2d · 3abc · 3def · 3g · 5g — 이웃 패널 축 글자 · 화살표 · 'Segmentation' 조각 · 잘린 라벨 / 식 둘 · 근거 문단 9 — 앞뒤 줄 조각).  56 장 전부 Read 로 열어 확인.  `figures.json` 의 `manual_crop` · `caption_fix` · `note_manual`.
- 판독: digitized.csv 584 행 — 벡터 그림은 경로 꼭짓점 × 벡터 눈금 (그림 2e 는 투명도 평탄화 다각형의 정수 CN 꼭짓점 묶음 · 계열 배정 창은 스크립트에 기록) · 검산 = 그림 2e 합 1.00 · 평균 4.88 · 6.55 · 7.40 (인쇄 4.8 · 6.5 · 7.4) · 그림 1d 표지 = 인쇄 율속 9 칸 (±0.03) · 그림 1e C50/C2 = 인쇄 유지율 3 칸 · 그림 3g 칸 합 99.6–99.9 % · 그림 5g 곡선 합 0.993–0.999.
- 2 차 인용 대조: 정본 카드 gandla2026 (L32 · L116 · L121 · L249 · L260 · L335–337 · L379 · L419 · L447) · li2026 (L18 · L66 · L98 · L104 · L135 · L152) · 비교 문서 §E L3032 — 고치지 않았다 (카드 문제 = 정독 출력 batch_50 의 "카드 문제" 절).
- 우리 쪽 값: 작업 가지 (stoic) `docs/data/lhs_handover_20261001.csv` 를 읽기만 함 (`am_pct` 70 · 80 · 85 행의 `am_am_cn` · `am_am_cn_std` · `phi_am_mass_conserving` · `porosity_union_exact_pct` 중앙값) · 정의 = 그 파일의 열 사전 (`lhs_handover_20261001_columns.tsv`) · `am_pct` 가 질량 기준임은 `docs/reviews/lhs_handover_judgments_20260924.md` L641 (*"am_pct = 100·(1 − pdd_SE)"*).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (park20* = park2019 · park2020 × 2 · park2024 · park2026 × 6 — 다른 논문) + 쪽 번호 '22262' · 제목 낱말 · 저자 (Vishnugopi · Naik) grep — 카드 없음 (인용만: gandla2026 · li2026 · jeong2024 · lei2026 · stavola2023 · zhang2026_anode_free 는 저자 이름만 겹침 · kang2025_bollard 는 제목 낱말 'High-Loading Cathodes' 만 겹치는 다른 논문) (2026-11-12).

## 🔗 관련 카드
- 같은 그룹 · 같은 모델 계열: `jeong2024_operando_densification_chemomechanics_se_size_composite_cathode` (SE 입경 축) — 이 카드는 CAM 비율 축.
- 복합 양극 미세구조 · 연결: `bielefeld2019_microstructural_modeling_composite_cathode` · `minnmann2024_microstructure_porosity_visualization` · `shi2019_high_am_loading_particle_size_assb` · `tailored_cathode_microstructure_low_pressure_assb`.
- 화학–역학 열화 · 균열: `intergranular_cracking_nmc811_jmca2023` · `gandla2026_layered_cathode_degradation_diagnostics_review` · `li2026_electrochemomechanical_coupling_asslmb_review` · `kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review`.
- 탄성 입력: `deng2016_elastic_superionic_electrolytes_dft`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
