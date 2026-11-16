# batch 126 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 표 N-77)

대상: `strauss2018_cam_particle_size_inactive_ncm622_electronic_percolation` — F. Strauss · T. Bartsch · L. de Biasi · A-Y. Kim · J. Janek · P. Hartmann · T. Brezesinski, "Impact of Cathode Material Particle Size on the Capacity of Bulk-Type All-Solid-State Batteries", *ACS Energy Letters* **3** (4) (2018) 992–996 · DOI 10.1021/acsenergylett.8b00275 · Letter (본문 5 쪽 + SI 8 쪽)
코팅 없는 NCM622 다결정 2차 입자 세 크기 (d50 4.0 / 8.3 / 15.6 µm) 를 β-Li₃PS₄ 와 7 : 3 wt (탄소 없음) 로 섞어 375 MPa 성형 · 55 MPa 운전한 반쪽 셀의 용량 · ex situ XRD 비활성 CAM · DC 분극 부분 전도도 — DEM · 모델 없음.
쪽 = PDF 쪽 (본문 p.n = 학술지 991 + n · SI p.n = S-n) · 판독 원자료 = `litdb/figures/strauss2018_cam_particle_size_inactive_ncm622_electronic_percolation/digitized.csv` (75 행) · 고른 의도 = '입도 설계 — CAM 입경 효과 (우리 PC/SC) · SE 4 µm · NCM 5 µm 입경 효과 (hippauf2019 p.2 인용) · 같은 그룹 (schmitt2026) · lei2026 은 원 논문 카드 없음' → 의도 대조 = **일부** (CAM 크기 · 같은 그룹 채움 · PC/SC 는 PC 만 · 'SE 4 µm' 없음)

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 순수 SE 기공 · 밀도 없음.  맨 SE 전도도만:
- [a] strauss2018_… | 맨 β-Li₃PS₄ σ **"approximately 0.2 mS/cm"** · 전자 차단용 1.5Li₂S·0.5P₂S₅·LiI 유리 **1.3 mS/cm (375 MPa 냉간)** | 카드 §3-1 · p.3 · SI p.2 | [인쇄] | 측정 조건 · 기공 [미확인] · β-Li₃PS₄ (LPSCl 아님)

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 되돌아옴 측정 없음.  상태만:
- [b] strauss2018_… | 모든 전기화학 · 전도도 측정 = **375 MPa 성형 뒤 55 MPa 로 낮춘 상태 (누른 채)** · ex situ XRD = 첫 충전 뒤 분해 (압력 0 · *"without breaking the pellet apart"*) — 그 사이 두께 · 밀도 변화 없음 | 카드 §3-1 · §4-3 (4) · SI p.2–3 | [인쇄] | 부분 탈압 상태의 측정 예일 뿐

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 역학 값 없음.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 하중 · 힘 자료 없음 (AM 망의 **전자 연결** 만 — 질문 m).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙 · 계산 없음.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음.

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 계산 없음 · 2D/3D 진술 없음.

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 기공 · 밀도 측정 없음.  대략값 대조만 (반면교사):
- [i] strauss2018_… | 복합 10–12 mg *"approx. 90 µm thickness and 1.9 mAh/cm² loading"* 375 MPa → 겉보기 밀도 ≈**1.68 g cm⁻³** = 이론 (NCM622 4.76 [표 S1 V 에서 카드 산술] · β-Li₃PS₄ 1.85–1.90 가정) 의 ≈0.51–0.52 · 분리막 60 mg ≈400 µm 는 지름 10 mm 면 1.91 g cm⁻³ · 12 mm 면 면 용량이 1.1–1.3 mAh cm⁻² → 대략값끼리 한 지름으로 안 맞는다 | 카드 §3-1 · §3-6 (6) · SI p.2 | [카드 산술] (로딩을 1C = 180 mAh g⁻¹ 로 셈 · 진밀도 가정) | 기공률로 쓰지 않는다 · 단면 SEM 은 ≈150 µm [판독 · 거칢]

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압과 닿는 것)
- [j] strauss2018_… | 저자: 낮은 CE 원인 *"not yet fully understood"* (p.2) · 건식 분말 혼합의 성분 분리 *"might be also affected by the particle size"* (p.4 · SEM/EDX 로 *"do not reveal major inhomogeneities"*) · XRD 해석에 부반응 용량 미포함 · NCM-S 비활성 분율은 검출 한계 근처 (−11 %) (SI p.4) | 카드 §3-6 · §11 | [인쇄] | —
- [j] strauss2018_… | 카드가 본 한계: σ 는 **SOC 0** 에서만 (충전 상태 σ_e 없음) · 비활성 분율은 첫 충전 뒤 한 번 (이온 고립 · 전자 고립 미분리) · SE 입경 · 기공 · 진밀도 · 셀 지름 · 시편 두께 [미확인] · 본문 압력 0 (전부 SI) · 인쇄 σ 식 (R×A)/l 거꾸로 · operando '75 s' ↔ 그림 S3 축 180 s | 카드 §3-6 · §11 · §13 | [미확인] · [판독] | 압밀 · 탈압 단계 자체가 없다

## k — DEM 의 한계 (서지: F. Strauss et al., ACS Energy Lett. 3 (2018) 992–996)
- [k] strauss2018_… (Strauss · … · Brezesinski 2018, ACS Energy Lett. 3, 992–996) | **말 없음** — DEM · discrete · simulation 낱말 0 회 (본문 + SI).  닿는 문장은 반대 방향 하나: *"This is in agreement with percolation theory, predicting that composites made of small particles offer many more contact points between them than those consisting of relatively large (spherical) particles, thereby providing sufficient pathways for electron conduction."* (p.4 · 인용 [26] SOFC) — 접점 수로 전자 망을 설명 (DEM 접촉망이 세는 양과 같은 그림) | 카드 §4-3 (1) · `txt_p4_electronic_3_orders_percolation_segregation.png` | [인쇄] | DEM 한계의 근거로 쓰지 않는다

## l — 소성변형이 왜 어려운가 · 택한 우회와 값
- [l] strauss2018_… (Strauss · … · Brezesinski 2018, ACS Energy Lett. 3, 992–996) | **말 없음** (plastic · elastic · deform 0 회) — 역학 문장 둘뿐: 황화물 SE *"the favorable mechanical properties of this class of SE materials allow good processability as well as high conductivity, even when cold pressed"* (p.1 · [4–6]) · *"the volume contraction during charging leads to a reduced electrical contact between the CAM particles and the SE"* (p.2 · [9, 18] · 측정 아님) | 카드 §4-3 (2) · `txt_p1_carbon_free_cam_size_20_to_5um.png` · `txt_p2_chemomech_contact_c30_c50.png` | [인쇄] | 우회 · 맞춘 값 · 계산 비용 없음 (실험)

## m — 받아들일 통찰
- [m] strauss2018_… | **우리 DEM σ_e 의 실험 짝 = 탄소 없는 복합체** (DEM 에는 탄소가 없다): 같은 7 : 3 wt 에서 AM d50 4.0 → 15.6 µm 로 전자 σ 8.8e-4 → 1.4e-6 S cm⁻¹ (≈2.8 자릿수) · 비활성 AM 2 → 31 % · 이온 σ 크기 무관 → **결과 전 대조 항목 (방향)** — 고체 중 AM ≈0.48 · AM 4 / 8 / 16 µm · SE 크기 두 값으로 감싼 우리 DEM 망이 같은 방향을 내는가 | 단계 7; 후보 D0; 결과 전 대조 항목 | 근거 그림 4 · SI 표 S1 · p.2–4 (카드 §7-1 · §8)
- [m] strauss2018_… | **판별 산술**: 끊김 없이 이어진 구 망은 (같은 변형률 · 접촉 반지름 ∝ R) σ_eff 가 입자 크기와 무관하다 → 이 논문 같은 자릿수 차이는 **연결성 (고립 입자)** 에서만 나와야 한다 — 우리 망이 φ_AM ≈0.5 근처에서 percolation 변화를 내는지가 시험의 요점 · 동시에 우리 Stage 22.5 σ_e 폼의 크기 항 부호 (코퍼스 적합 · shi2019 카드 L570–571 정정) 를 이 실측과 대조 | 단계 7; 후보 D0 | 근거 카드 §7-2 [카드 해석]
- [m] strauss2018_… | **함정 — 이 논문을 '작은 AM = 단결정 = σ_AM ↑' 라벨 (AM_S) 이나 NCM(r) 입계 계수의 근거로 쓰지 않는다**: 세 시료 모두 다결정 2차 입자 (SEM 그림 1a–c) · 저자 기전 = 망의 접점 수 (p.4) | 흐름 밖: σ_e 폼 · PC/SC 라벨 | 근거 p.1 초록 'secondary particle size' · 그림 1a–c · p.4
- [m] strauss2018_… | **DC 분극 보고 꼴**: 이온 차단 (SS | 복합 | SS · 375 MPa 2 min · 1 h 휴지) · 전자 차단 (Li/In | 1.3 mS/cm 유리 | 복합 | 유리 | Li/In · 6 h 휴지) · 300 mV · 정상 영역 선형 맞춤 · 55 MPa 유지 — 원문은 σ 식을 (R×A)/l 로 거꾸로 인쇄했고 두께 · 면적 · 유리 층 저항을 적지 않았다 → 우리 SBE · DBE σ_e 앵커 기록에 이 칸들을 채운다 | 흐름 밖: DC 분극 앵커 (σ_e 실험 앵커) | 근거 SI p.3 (`txt_SIp3_lib_pouch_dc_polarization.png` · `eq_S02_conductivity_sigma_RA_over_l.png`)

## n — 논문 에이전트 후보
- [n] Koerver, R.; Aygün, I.; Leichtweiß, T.; Dietrich, C.; Zhang, W.; Binder, J. O.; Hartmann, P.; Zeier, W. G.; Janek, J. Capacity Fade in Solid-State Batteries: Interphase Formation and Chemomechanical Processes in Nickel-Rich Layered Oxide Cathodes and Lithium Thiophosphate Solid Electrolytes. Chem. Mater. 2017, 29, 5574−5582. | j · 조건 R2 — '충전 수축 → CAM–SE 전기 접촉 감소' 의 인용처 (카드 §3-2 · §4-3) | papers/ ls (koerver2017* 없음 · koerver2018 은 다른 논문) · grep 'Capacity Fade in Solid-State' = barai2021 · jung2019 · koerver2018 의 인용뿐 → 카드 없음 (wishlist L153 에 이미 있음)
- [n] Zhang, W.; Schröder, D.; Arlt, T.; Manke, I.; Koerver, R.; Pinedo, R.; Weber, D. A.; Sann, J.; Zeier, W. G.; Janek, J. (Electro)chemical Expansion During Cycling: Monitoring the Pressure Changes in Operating Solid-State Lithium Batteries. J. Mater. Chem. A 2017, 5, 9929−9936. | b · j · 조건 R2 · R4 — 같은 인용처 + 이 논문 셀 장치의 출처 (SI [2]) | papers/ ls (zhang2017* 없음) · grep 'Monitoring the Pressure Changes' = benhadjali2026 · koerver2018 · schmitt2026 의 인용뿐 → 카드 없음 (wishlist L202 에 이미 있음)
- [n] Zhang, W.; Weber, D. A.; Weigand, H.; Arlt, T.; Manke, I.; Schröder, D.; Koerver, R.; Leichtweiss, T.; Hartmann, P.; Zeier, W. G.; et al. Interfacial Processes and Influence of Composite Cathode Microstructure Controlling the Performance of All-Solid-State Lithium Batteries. ACS Appl. Mater. Interfaces 2017, 9, 17835−17845. | i · m — 7 : 3 wt 최적의 근거 · 같은 계 복합 양극 미세구조 (카드 §3-1) | papers/ ls · grep 'Interfacial Processes and Influence of Composite Cathode' = lee2024 의 인용뿐 → 카드 없음
- [n] Chen, D.; He, H.; Zhang, D.; Wang, H.; Ni, M. Percolation Theory in Solid Oxide Fuel Cell Composite Electrodes with a Mixed Electronic and Ionic Conductor. Energies 2013, 6, 1632−1656. | k · m — '작은 입자 = 접점 많음 → 전자 경로' 의 percolation 근거 (p.4 · 카드 §4-3) | papers/ ls (chen2013* 없음 · chen2011 은 다른 논문) · grep 'Percolation Theory in Solid Oxide' 0 건 → 카드 없음
- [n] de Biasi, L.; Kondrakov, A. O.; Geßwein, H.; Brezesinski, T.; Hartmann, P.; Janek, J. Between Scylla and Charybdis: Balancing Among Structural Stability and Energy Density of Layered NCM Cathode Materials for Advanced Lithium-Ion Batteries. J. Phys. Chem. C 2017, 121, 26163−26171. | 조건 R2 · R7 — NCM 격자 · 부피 vs Li (화학–역학 입력 · 카드 §3-3) | papers/ ls (debiasi* 없음) · grep 'Scylla and Charybdis' = koerver2018 · stallard2022 의 인용뿐 → 카드 없음
- (세지 않음) (17) Nam 2018 J. Power Sources 375, 93 = 후보 표 N-78.

## 카드 문제
1. **`hippauf2019_dry_film_ptfe_sulfide_cathode_sheet` L276** — 참고 24 (= 이 논문) 의 메모 *"SE 4 µm · NCM 5 µm 입경 효과 (본문 p.2 인용)"* ↔ 이 원문 (본문 5 쪽 + SI 8 쪽) 에는 **SE (β-Li₃PS₄) 입경이 없다** · 4.0 µm 는 **NCM-S 의 d50** (d90 4.8 µm) · '≈5 µm' 은 NCM 범위 끝 (*"approximately 20 to 5 μm"*).  Hippauf 본문 p.2 의 그 문장은 이 트리에 PDF 가 없어 대조하지 못했다 (Hippauf 원문의 인용이 그렇게 적었을 수도 있다) — 카드는 고치지 않았다.
2. **`kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps` L282** — 메모 *"CAM 입경 효과 (우리 PC/SC)"* ↔ 이 원문의 세 시료는 **모두 다결정 2차 입자** (단결정 없음) → 'SC' 쪽은 이 논문에 없다.  서지는 원문과 같다 (표기 'L. De Biasi' · 'A.Y. Kim' ↔ 원문 'Lea de Biasi' · 'A-Young Kim').
3. **`minnmann2022_designing_cathodes_solidstate` L88** (가리킨 카드 아님) — *"CAM 2차입자 최적 지름 3–5 µm (refs 36,37 = Strauss 2018 + Bielefeld 2019 인용)"* ↔ 이 원문은 최적을 말하지 않는다 (가장 작은 d50 4.0 µm 가 셋 중 가장 좋았을 뿐 · 4 µm 아래 미측정) — Minnmann 원문의 설계 문장으로 보인다 (Minnmann 원문 미대조).
4. **`cronau2022_wet_milling_particle_size_ionic_conductivity` L89** (가리킨 카드 아님) — *"p.1 (CAM < 5 µm 전형)"* ↔ 이 원문의 < 5 µm 시료는 NCM-S 하나 (d90 4.8) · '전형' 은 이 원문 주장이 아니다 (Cronau 원문의 인용 범위).
5. **`lei2026_se_particle_size_effects_review` L244 · L279** — *"카드를 만든 뒤 쓴다"* · '카드 없음' → 이 카드로 해소 (오류 아님).  L122 의 2 차 인용 값 (162 → 84 · CE 70 → 50 % · 비활성 2 → 31 % · σ_e 10⁻³ → 10⁻⁶ · 이온 무관) 은 원문과 모두 같다.
6. 이 카드 (strauss2018) 자체 — 없음 (원문 쪽 결함 8 항목은 카드 §3-6).
