<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = doux2020_pressure_effects_sulfide_se_jmca.md · miss2026_insitu_conductivity_porosity_pressure_compaction.md ·
     lee2025_heckel_argyrodite_powder_densification_nanoindentation.md (황화물 SE 의 압력별 구조 · σ) · 계산 쪽 이웃 = so2021_dem_mold_pressure_assb_coldpress.md
     (otani2023 이 이 논문과 같은 방향의 근거로 함께 든 ref 7).
     쪽 표기 = 학술지 논문 번호 228160 의 쪽 p.1–8 (PDF 쪽 = 인쇄 쪽).  보충 자료 (SI) 는 원문에 안내가 없다 (본문 8 쪽이 전부).
     값 표지: [인쇄] = 본문 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv · 원 래스터 300 dpi 에서
     큰 눈금 직선 맞춤 · 잔차 y ≤ 0.001 · x ≤ 0.11 MPa) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 추론] · [추정] = 이 카드의
     해석 · [미확인] = 원문 (본문 8 쪽 전수) 에 없음.  원문 8 쪽은 전부 렌더 이미지로 읽었고 숫자는 텍스트 층과 대조했다. -->
# 순수 황화물 SE 를 누른 채 (in situ · ≤ 103 MPa) X 선 CT 로 본 densification (입자 파쇄 → 틈 메움 → 상온 가압 소결) 과 XCT 복셀 유한체적 σ_ion ↔ EIS — 주 재료 Li₆PS₅Br (75–150 µm 체 분급) · 계산 ÷ 실측 1.80 (8.7 MPa) → 1.07 (104 MPa) [판독] · 감압 103 → 28 MPa 에서 σ −20 % · 변형률 변화는 오차 막대 안 · 기공률 숫자 · 진밀도 없음 · "contact resistance 무시 가능" 의 근거 문장 — Kodama · Komiyama · Ohashi · Horikawa · Kawamura · Hirai (J. Power Sources 2020)

> slug `kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation` · DOI `10.1016/j.jpowsour.2020.228160` · type `experiment + image-based simulation (in situ XCT 가압 셀 · EIS impedance · XCT 복셀 유한체적 σ_ion — 순수 황화물 powder densification · contact resistance · tortuosity · DEM · FEM · MPM 압밀 계산 없음)` · PDF `2038fbfe-8._High-pressure_in_situ_X-ray_computed_tomography_and_numerical_simulation_of_sulfide_solid_electrolyte.pdf` · digested `2026-11-12` · status ✅
>
> **저자**: **M. Kodama\*** (교신 · 원문은 이니셜만 — 이름 전체 [미확인]) · S. Komiyama · A. Ohashi · N. Horikawa · K. Kawamura · S. Hirai — Tokyo Institute of Technology (NE-8 2-12-1 Meguro, Tokyo · School of Engineering) · *J. Power Sources* **462** (2020) 228160 (본문 8 쪽 · SI 안내 없음) · 접수 2020-02-23 · 수정 04-03 · 승인 04-04 · 온라인 04-18 · 연구비 Japan Keirin Autorace Foundation (일부) · 기여: Kodama = 개념 · 방법 · 소프트웨어 · 초고 / Komiyama = 검증 · 자원 / Ohashi = 검토 · 편집 / Horikawa = 검증 / Kawamura = 자원 / Hirai = 과제 관리 (p.7).
> **이웃 카드 (링크만)**: [`otani2023_ionic_conductivity_path_resistance_separation_model`](otani2023_ionic_conductivity_path_resistance_separation_model.md) (그 논문 ref 22 = 이 논문 · '③ 격자 부정합 저항 무시') · [`yadav2021_lpscl_sieved_psd_impedance_tortuosity`](yadav2021_lpscl_sieved_psd_impedance_tortuosity.md) (ref 5) · [`faka2026_particle_size_consolidation_strain_lpscl`](faka2026_particle_size_consolidation_strain_lpscl.md) (ref 12) · [`sakuda2013_sulfide_mechanical_property`](sakuda2013_sulfide_mechanical_property.md) (이 논문 ref 8) · [`deng2016_elastic_superionic_electrolytes_dft`](deng2016_elastic_superionic_electrolytes_dft.md) (이 논문 ref 17) · [`kato2016_high_power_assb_lsipscl_superionic`](kato2016_high_power_assb_lsipscl_superionic.md) (ref 7) · [`thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography`](thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography.md) (초고압 흡수 단층촬영 · 같은 질문의 GPa 판) · [`lee2025_heckel_argyrodite_powder_densification_nanoindentation`](lee2025_heckel_argyrodite_powder_densification_nanoindentation.md) (같은 Li₆PS₅Br 의 Heckel · 나노압입).
> **판독 원자료**: `litdb/figures/kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation/digitized.csv` (81 행 — Fig 3a · 3c · 4a · 4c · 5a · 5b · 6a · 6b · 6c) · 그림 크롭 44 장 (그림 8 재크롭 + 그래픽 초록 1 + 패널 17 · 식 6 · 근거 문단 12) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 체로 거른 **75–150 µm** Li₆PS₅Br 분말을 PEEK 원통 (지름 [미확인] · 축척 막대로 ≈0.58–0.61 mm [판독]) 에 넣고 스프링으로 **0 → 103 MPa** 누르며 **누른 채** X 선 CT (복셀 1.62 µm · 시야 1.14 mm) 와 EIS (25 °C) 를 재고, 그 CT 영상을 그대로 격자로 써서 **기공 σ = 0 · SE σ = 400 MPa 치밀 펠릿 값** 의 정상 전도 (Laplace) 를 유한체적으로 푼다 — **순수 SE 의 압력별 구조는 영상으로 있지만 기공률 · 상대밀도 숫자 · 진밀도는 원문 어디에도 없고**, 계산이 실측을 저압에서 1.8 배 · 고압에서 1.07 배로 넘는 것을 저자는 *"almost the same"* 으로 읽어 **입자 사이 접촉 저항을 무시할 수 있다** 고 결론짓는다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 순수 SE 의 압력별 기공 · 상대밀도 (누른 채) | **숫자 없음** — 단면 영상 (8.4 · 31.4 · 62.2 · 103.0 MPa) 과 변형률 곡선뿐.  이 카드가 잰 2D 면적 분율: 계산 단면의 기공 ≈31 % (8.4) · ≈1–4 % (103.0 MPa) · 인쇄 CT 단면의 검은 면적 27–40 % (8.4) → 4–18 % (103.0 MPa, 문턱 64–128 에 따라) | 영상 [인쇄] Fig 3b · 7 · 8 · 면적 분율 [판독 · 단면 한 장] §3-3 |
| ② 측정법 (XCT 분해능 · 문턱 · 기공 정의 · 진밀도 분모) | 복셀 **1.62 µm** · 시야 **1.14 mm** 정육면체 · Mo 66 kV / 44 mA 실험실 의사 평행광 · *"resolution of 1.0 μm"* (복셀보다 작다 — 원문 어긋남) · 흰 = SE · 검정 = 기공 · **이진화 문턱 · 재구성 · 투영 수 · 진밀도 = 원문에 없음** | [인쇄] p.2 · [미확인] |
| ③ 하중을 뺀 뒤 | 103.0 → ≈28 MPa 까지만 감압 (0 아님): σ 0.79 → 0.63 mS/cm (**−20 %**) · 구조 유지 (영상) · 변형률 0.462 → 0.473 (**오차 막대 ±0.02 안** — 되돌아옴 측정 불가) · 같은 압력의 가압 값보다 σ 가 1.65 배 (28 MPa) | [판독 · 카드 산술] Fig 4 · §3-5 |
| ④ 입자 형상 · 접촉 · 균열 | 8.4 MPa: 큰 틈 · 작은 접촉 → 8.4 → 31.4 MPa: **입자가 부서진다** (crushed) · 작은 조각이 기공을 메움 → 31.4 → 103.0 MPa: 기공 수 · 크기 감소 · **경계가 거의 안 보임** (= Sakuda 의 상온 가압 소결) · 감압해도 유지 | [인쇄] p.5 · Fig 3b · 4b |
| ⑤ 수치 모사의 정체 | **압밀 계산이 아니다** — CT 영상 기반 3D 정상 전도 (∇·j = 0 · 옴 법칙 · σ 기공 0 / SE σ_400MPa · 식 1–4) · 유한체적 · SOR · OpenMP · **350³ 격자 (복셀 1.62 µm = 567 µm 정육면체 [카드 산술])** · 위 1 V / 아래 0 V · **접촉 저항 · 내부 응력 효과 무시** · DEM · FEM · MPM 역학 계산 없음 | [인쇄] p.3 · 식 (1–1)–(4) |
| ⑥ 실험 대조 | 계산 ÷ EIS — Li₆PS₅Br 가압 **1.80 (8.7) · 1.20–1.27 (32) · 1.15 (63) · 1.07 (104 MPa)** · 감압 1.07–1.09 · Li₆PS₅Cl **2.3–2.6 (9.4) → 1.03 (96 MPa)** · LPS 유리세라믹 0.70–1.28 · LPS 유리 0.94–1.08 | [판독 · 카드 산술] Fig 5 · 6 · §3-6 |
| ⑦ 입계 (접촉) 저항을 무시한 근거 (otani2023 의 ③) | (1) 계산 ≈ 실측 (2) *"The 0.2% proof stress of sulfide solid electrolyte (E = 20 GPa) is about 40 MPa"* → 접점 응력 ≥ 내력 → 소성 변형 → *"would suppress the crystal lattice mismatch at particle interface, leading to the conclusion that contact resistance has a negligibly small influence"* — (2) 의 40 MPa 는 **출처 없음 · 재료 미지정 · 20 GPa × 0.2 % 와 정확히 같다** [카드 산술] | [인쇄] p.5 · §3-9 |
| ⑧ E · 항복 | 가압 *"effective Young's modulus ranged from 25 MPa to 250 MPa"* (할선 판독 55 → 211 MPa) · 감압 *"remained almost constant at 25 GPa"* (자료로 가를 수 없음) · *"From molecular dynamics simulation, the Young's modulus of Li6PS5Br is 25 GPa [17]"* — [17] Deng 2016 은 **0 K 정적 DFT** (정본 카드 · Li₆PS₅Br E 25.3 GPa) | [인쇄] p.5 · [판독] Fig 3c · 4c |
| ⑨ 저자가 적은 한계 | 분해능 부족 → 큰 입자만 · 최대 ≈100 MPa (PEEK 내구) · *"for high-accuracy numerical simulation of solid electrolyte compression, nonlinear numerical simulation is required"* · *"the size of solid electrolyte particles used in this study was very large … but the principles revealed can be applied for smaller solid electrolyte particles"* | [인쇄] p.2 · p.5 |

⛔ **한정어 (떼지 말 것)**: ① 주 재료 = **Li₆PS₅Br** (LPSCl 은 그림 6 의 σ 비교 하나뿐 · 합성 · 입경 · 영상 [미확인]) ② 입경 **75–150 µm** (우리 DEM SE ≈1 µm 의 75–150 배) — 해상도 때문에 일부러 고른 크기 ③ 최대 **103 MPa** (우리 300 MPa 의 ⅓) ④ **기공 숫자 · 진밀도 · 시료 질량 · 높이 · 지름 [미확인]** — 이 카드의 면적 분율은 2D 단면 한 장 · 인쇄 영상 판독 ⑤ 복셀 1.62 µm 보다 작은 틈은 안 보이므로 **CT 기공은 하한** [카드 추론 — 저자도 그래서 큰 입자를 골랐다] ⑥ EIS 의 σ 환산 기하 (두께 · 면적) · 오차 막대 정의 · 입력 σ_400MPa 값 [미확인] ⑦ 감압은 ≈28 MPa 에서 멈춤 (0 아님).
⇒ **절대값 전이**: 기공 절대값은 **없다** (전이할 숫자 자체가 없음).  σ(P) 가압 · 감압 곡선은 같은 계열 다른 재료 (Br) 의 in situ 자료 — 결과 전 대조 항목으로만 (재료 · 입경 · 압력 범위 표지 필수).  옮길 수 있는 것은 **방법의 교훈** — 복셀 유한체적 (접촉 저항 없음) 은 저밀도에서 실측을 1.8–2.6 배 넘고 고밀도에서 1.03–1.07 배로 좁혀진다 (순수 SE · 입자 지름당 46–93 복셀).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-8 의 '왜' 칸)

의도 원문: *"a — 순수 황화물 SE 를 고압에서 in situ XCT (누른 채 구조 · 공극) · otani2023 이 '③ 격자 부정합 저항 무시' 를 refs 7 · 22 와 같은 방향이라 할 때의 근거 22 (otani2023 L265 '카드 없음 — 고압 in situ XCT · 황화물 입계 저항 무시 근거') · yadav2021 = '입도 · 치밀화 (faka2026 ref 12 와 같은 논문)'"*

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| (a) "순수 황화물 SE 를 … in situ XCT (누른 채 구조)" | **채움** | Fig 3b (가압 8.4 · 31.4 · 62.2 · 103.0 MPa) · Fig 4b (감압 103.0 · 50.0 · 27.8 MPa) — XY · ZX 단면 · Li₆PS₅Br 75–150 µm · **누른 채** (스프링 하중 유지 중 촬영) · 온도 숫자 없음 (EIS 는 25 °C) [인쇄] p.2 · p.4–5 |
| (a) "고압에서" | **일부** | 이 논문의 '고압' = XCT 셀 기준 *"high pressure (>1 MPa)"* (p.2) · 실제 최대 **≈100 MPa** (*"because of a limitation with mechanical durability of the PEEK part"* p.2) · 마지막 점 103.0 MPa — 우리 300 MPa 의 ⅓ |
| (a) "공극" (누른 채 기공 값) | **없음 (숫자)** · 일부 (정성) | 기공률 · 상대밀도 · 진밀도 · *"volume ratio of pores"* 의 숫자가 본문 · 그림 · 캡션 어디에도 없다 (8 쪽 전수) — 영상 (흰 = SE · 검정 = 기공) 과 정성 문장 (*"large gaps"* · *"the volume ratio of pores decreased"* · *"small amount of voids"*) 뿐.  이 카드의 2D 면적 분율 (§3-3) 은 **[판독 · 단면 한 장]** |
| otani2023 의 '③ 격자 부정합 저항 무시' 근거 22 | **채움** | p.5: *"This deformation of solid electrolyte would suppress the crystal lattice mismatch at particle interface, leading to the conclusion that contact resistance has a negligibly small influence."* · Highlights: *"The contact resistance between SE particles is negligibly small."* · 조건 = Li₆PS₅Br · 누른 채 8.4–103 MPa · EIS 25 °C ↔ 복셀 계산 (접촉 저항 항 없음).  근거의 세기: 계산 ÷ 실측 **1.07 (104 MPa)** 이지만 **1.80 (8.7 MPa)** [카드 산술] · 0.2 % 내력 40 MPa 는 출처 없음 |
| otani2023 L265 서지 · 표기 "고압 in situ XCT · 황화물 입계 저항 무시 근거" | **채움 (표현 하나 다름)** | 서지 "M. Kodama, S. Komiyama, A. Ohashi, et al., J. Power Sources 462 (2020) 228160" = 원문과 같다.  다만 원문이 무시한 것은 **입자 사이 접촉 저항 (contact resistance between solid electrolyte particles)** 이고 '입계 저항' 을 따로 다루지 않는다 — 치밀 펠릿 안의 입계 몫은 입력 σ_400MPa 에 이미 들어 있다 (식 4) |
| otani2023 L30 · L81 "refs 7 · 22 의 황화물 입계 저항 무시와 정합" | **채움 (같은 단서)** | 위와 같은 문장 · 같은 한정.  ⚠ 인용 고리: 이 논문은 같은 결론의 뒷받침으로 **Otani 그룹** 의 refs 19 (Otani · … · Inoue · Kaburagi · Ishiguro, 60th Battery Symposium 2019) · 20 (Miyuki · Morino · Otani, Denki Kagaku 88 (2020) 54–64) 를 든다 (p.5) — 두 그룹이 서로를 근거로 든다 [카드 관찰] |
| yadav2021 L321 "입도 · 치밀화" | **일부** | 입도: 20–40 · 40–75 · 75–150 µm 체 분급 분말의 σ 가 *"almost the same and did not depend on particle size"* (p.2) — **숫자 · 압력 · 그림 없음**.  치밀화: Fig 3c 변형률 곡선 · Fig 3b 파쇄 → 메움 → 소결 (정성).  서지 (Kodama, M. et al. … J. Power Sources 462, 228160 (2020)) = 원문과 같다 |
| yadav2021 "(faka2026 ref 12 와 같은 논문)" | **채움** | faka2026 L251 "M. Kodama, S. Komiyama, A. Ohashi, … S. Hirai, J. Power Sources 462 (2020): 228160" = 같은 논문 (저자 끝 S. Hirai ✓) |
| faka2026 L251 "고압 in situ XCT + 수치 모의 (황화물)" | **채움** | 위 ⑤ · Fig 2 · 5 · 6 |
| (꼭 뽑을 것) 조성 · 입경 · 시편 · 다이 | **일부** | 조성 Li₆PS₅Br (Li₂S + P₂S₅ + LiBr · 원료 비 숫자 없음 · 490 °C 5 h) · 75–150 µm · PEEK 원통 + 스테인리스 집전체 · 스프링 + 나사 · 두랄루민 몸체 [인쇄] p.2 — 시편 지름 · 높이 · 질량 [미확인] (지름 ≈0.58–0.61 mm 는 [판독]) · 다른 세 SE 의 조성 · 합성 · 입경 [미확인] |
| (꼭 뽑을 것) 압력별 공극 · 상대밀도 · 진밀도 분모 | **없음** | 위 (a) 공극 줄 |
| (꼭 뽑을 것) 하중을 뺀 뒤 | **일부** | 103.0 → ≈28 MPa (0 아님) — σ · 변형률 · 영상 (Fig 4) |
| (꼭 뽑을 것) 형상 · 접촉 · 균열 | **채움 (정성)** | 파쇄 · 메움 · 경계 소멸 (p.5) · 저압 접촉 면적 작음 · 흐름 집중 (Fig 7 · p.5) · 고압 접촉 넓음 (Fig 8 · p.6) |
| (꼭 뽑을 것) 수치 모사 + 실험 대조 | **채움** | 영상 기반 (image-based) 3D 정상 전도 FV — 구성식 = 옴 법칙 이진 σ · 매개변수 = σ_400MPa (값 미인쇄) · 경계 = Dirichlet 1 / 0 V · 격자 = 350³ · 1.62 µm · 대조 = Fig 5 · 6 |
| 가리킨 카드의 **2 차 인용 값** | **해당 없음** | otani2023 · yadav2021 · faka2026 세 카드 모두 이 논문에서 **숫자를 옮기지 않았다** (서지 · 주제 표기뿐) |
| (덧붙임) yadav2021 L51 의 [5] 귀속 | **원문에 없음** | yadav2021 원 논문이 [5] (= 이 논문) 에 *"compacity … morphology and size of individual particles and their distribution"* 를 귀속 — 이 논문은 입경 분포별 충전 밀도를 재지 않았다 (입경별 σ '거의 같음' 한 문장뿐).  **Yadav 원문의 인용 문제** (카드는 원문 그대로 옮김 — 카드 문제 아님) |

⇒ **의도 대조 결과: 일부** — 누른 채 구조 (in situ XCT) · 입계 (접촉) 저항 무시의 근거 문장은 **있다**; 기공률 · 상대밀도 숫자 · 진밀도는 **없다** · '고압' 은 ≤ 103 MPa.

---

## 1. 한 줄 요약
SEM 단면은 반드시 하중을 뺀 뒤 (ex situ) 라 상온 가압 소결의 과정을 볼 수 없다는 동기 (p.2) 에서, X 선이 통과하는 PEEK 원통 셀 (XESC) 로 **Li₆PS₅Br 분말을 누른 채** CT · EIS 를 0 → 103 → 28 MPa 로 잰다 — 가압하면 입자가 부서지고 조각이 틈을 메워 103 MPa 에서 경계가 거의 사라지며 (σ 0.17 → 0.79 mS/cm [판독]), 감압해도 구조 · σ 가 대부분 남는다 (−20 %).  같은 CT 영상에 이진 σ (기공 0 · SE = 400 MPa 펠릿 값) 를 주고 푼 3D 유한체적 전도가 EIS 와 *"almost the same"* 이므로 **입자 사이 접촉 저항과 내부 응력의 σ 효과는 무시할 만하다** 고 결론 — Li₆PS₅Cl · LPS 유리 · LPS 유리세라믹에서도 같다고 적는다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| M. Kodama\* · S. Komiyama · A. Ohashi · N. Horikawa · K. Kawamura · S. Hirai (Tokyo Tech) | J. Power Sources 462 (2020) 228160 · 8 쪽 | 10.1016/j.jpowsour.2020.228160 | **순수 SE 만** — Li₆PS₅Br (자체 합성 · 주 재료) · Li₆PS₅Cl · LPS 유리 · LPS 유리세라믹 (출처 · 조성 [미확인]) · CAM 없음 | 실험 (in situ XCT + EIS) + **영상 기반 계산** (복셀 FV 정상 전도) — 압밀 · 역학 계산 없음 |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 셀 · 측정 상수 (p.2 · p.3)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| Li₆PS₅Br 합성 | Li₂S · P₂S₅ · LiBr 3 g (원료 비 = *"specified quantity"* — 숫자 없음) · ZrO₂ 포트 50 ml · 디에틸에테르 0.1 ml · ZrO₂ 볼 φ10 mm × 16 · 고에너지 진동 밀 1200 rpm 20 h → **490 °C 5 h** · Ar 이슬점 < −80 °C · XRD (Rigaku RINT-ULTIMA III · CuKα · 40 kV) Li₆PS₅Br 봉우리만 | [인쇄] p.2 |
| 다른 세 SE | Li₆PS₅Cl · LPS 유리 · LPS 유리세라믹 — 합성 · 조성 · 공급 · 입경 · 체 분급 여부 | [미확인] (p.2 범위 문장 · Fig 6 뿐) |
| 입경 | **75–150 µm** (스테인리스 체) — *"to prevent a formation of small scale void that is smaller than resolution"* · 20–40 / 40–75 / 75–150 µm 의 σ *"almost the same"* (숫자 없음) | [인쇄] p.2 |
| 셀 (XESC) | PEEK 원통 + 스테인리스 집전체 (위 · 아래) · 스프링 (두랄루민 몸체 안) + 나사 · 스프링 변형을 **160 kV · 70 µA 텅스텐 경 X 선 영상**으로 읽어 스프링 응력–변형 특성으로 압력 환산 · 최대 ≈100 MPa (PEEK 내구) · O-링 밀봉 · 이슬점 < −70 °C | [인쇄] p.2 · Fig 1a |
| 시료 지름 · 높이 · 질량 | 원문에 없음 · 지름은 단면 원과 200 µm 막대로 **≈0.58 mm (Fig 3b, 원 317–322 px · 110 px = 200 µm) · ≈0.61 mm (Fig 4b, 220 px · 72 px = 200 µm)** | [미확인] · [판독] |
| XCT | 실험실 의사 평행광 · Mo 표적 66 kV / 44 mA · 금속 필터 없음 · 냉각 CCD + 섬광체 + 현미경 · 시료–섬광체 8 mm · **시야 1.14 × 1.14 × 1.14 mm³ · 복셀 1.62 µm** (= 시야 704 복셀 [카드 산술]) · *"resolution of 1.0 μm"* | [인쇄] p.2 |
| XCT 처리 | 투영 수 · 노출 · 재구성 · 잡음 처리 · **이진화 문턱** · 기공 정의 (흰 = SE · 검정 = 기공 · 그림 캡션) | [미확인] (캡션만 [인쇄]) |
| EIS | 정전류 EIS 1 MHz–10 Hz · **25 °C** · 등가회로 R1 + C ∥ (R2 + Zw) (R1 = 벌크 · R2 = 전하이동 · C = 용량 · Zw = Warburg) · σ 는 R1 에서 | [인쇄] p.2 · Fig 1b |
| σ 환산 기하 · 오차 막대 | 두께 · 면적 · 반복 수 (오차 막대 = 무엇의 표준편차인지) | [미확인] |
| 변형률 | *"measured by the distance from the upside current collector to the downside current collector using X-ray CT"* — 기준 높이 h₀ (0 MPa?) 의 값 · 정의 | [인쇄] p.5 · [미확인] |
| 계산 입력 σ_400MPa | *"measured with another cell"* · 400 MPa 에서 *"the volume ratio of pores to solid electrolyte particles is almost zero"* [8] — **값 인쇄 안 됨**.  하한: 이진 매질 (σ ∈ {0, σ₀}) 의 유효 σ 는 σ₀ 를 넘지 못하므로 σ_400MPa ≥ 계산 σ (≈100 MPa) = **Br ≥ 0.84 · Cl ≥ 1.14 · 유리세라믹 ≥ 0.127 · 유리 ≥ 0.136 mS/cm** | [인쇄] p.3 · [카드 산술 · 하한] |

### 3-2. ★ 가압 중 σ_ion — Li₆PS₅Br (Fig 3a · 5a 검정 · p.4 · p.6)
| 압력 (MPa) | σ_EIS (mS/cm) | 오차 막대 (판독) | 계산 σ (빨강 · Fig 5a) | 계산 ÷ 실측 [카드 산술] |
|---|---|---|---|---|
| 0 | 0 | — | 0 | — |
| 8.7–8.8 | **0.170** | 0.137–0.205 | **0.307** (8.7) | **1.80** |
| 23.8 (x 19.2–28.5) | 0.322 | 0.258–0.386 | — | — |
| 32.0 (계산점) | (보간 0.438) | — | **0.557** | 1.27 (보간) · 1.20 (가장 가까운 34.0 점) |
| 34.0 | 0.465 | (표지 안) | — | — |
| 46.6 (x 43.5–49.7) | 0.507 | 0.475–0.541 | — | — |
| 63.1 | 0.653 | 0.600–0.704 | **0.748** | **1.15** |
| 74.7 (x 71.3–78.0) | 0.712 | 0.650–0.773 | — | — |
| 90.9 | 0.771 | 0.722–0.819 | — | — |
| 103.8 | **0.789** | (표지 안) | **0.844** | **1.07** |
- 전부 [판독] (Fig 3a · 5a 의 같은 검정 점을 두 래스터에서 따로 읽어 x ±0.15 MPa · y ±0.001 안에서 같음 — 판독 재현성) · 압력 축 값은 그림 점 위치.  CT 영상 압력 (8.4 · 31.4 · 62.2 · 103.0 [인쇄 Fig 3b]) 과 계산점 x (8.7 · 32.0 · 63.1 · 103.8 [판독]) 는 0.3–0.9 MPa 어긋난다.
- 원문 문장: *"the ionic conductivity increased with the increase in applied pressure"* (p.3) — σ 숫자는 본문에 없다 (그림뿐).
- 모양 [카드 산술]: 103.8 MPa σ 의 **41 % 가 23.8 MPa · 59 % 가 34.0 MPa · 64 % 가 46.6 MPa 까지** (0.322 · 0.465 · 0.507 ÷ 0.789 · 판독 값).

### 3-3. ★ 가압 중 구조 · 기공 (Fig 3b · 7 · 8 · p.5–6) — 숫자는 원문에 없다
- **원문 (정성)**: 8.4 MPa *"large gaps existed between solid electrolyte particles and the contact area between electrolyte particles was very small"* → 8.4 → 31.4 MPa *"the size of the solid electrolyte particles decreased because they were crushed by the high pressure. Small solid electrolyte particles filled the pores, and the volume ratio of pores decreased"* → 31.4 → 103.0 MPa *"reduced the number and size of pores, and particle boundaries were difficult to see at 103.0 MPa"* = *"equivalent to room-temperature sintering [8]"* (p.5).
- **이 카드의 2D 면적 분율 [판독 · 단면 한 장 · 기공률 아님]**:

| 압력 (MPa) | 인쇄 CT 단면 XY 검은 면적 (문턱 64 / 96 / 128) | ZX 검은 면적 (64 / 96 / 128) | 계산 단면 흰 (기공) 면적 (Fig 7b · 8b) |
|---|---|---|---|
| 8.4 | 27.2 / 31.7 / 36.3 % | 28.2 / 34.0 / 40.2 % | **31.3 %** (전위 지도 31.1 %) |
| 31.4 | 14.8 / 19.4 / 24.6 % | 13.9 / 18.9 / 24.3 % | — |
| 62.2 | 7.8 / 12.2 / 18.3 % | 5.8 / 9.9 / 15.9 % | — |
| 103.0 | 3.8 / 7.3 / 14.3 % | 6.2 / 11.0 / 17.6 % | **1.2 %** (선 · 경계 화소 3.1 % 를 더해도 ≤ 4.3 %) |
- 방법: 원 래스터 (300 dpi) 의 최소 RGB 를 문턱 셋으로 · XY = 원 안쪽 (테두리 6 px 제외) · ZX = 단면 사각 안쪽 · 계산 단면 = 가상 전극 사이 영역의 흰 (모든 채널 > 225) 화소.  ⚠ 고압에서는 문턱 민감도 (×2–4) 가 신호보다 크다 — 인쇄 영상은 회색 반점 (잡음 · JPEG) 이 있어 이진 영상이 아니다.  계산 단면 (이진 입력의 렌더) 이 더 깨끗하다.
- ⚠ 복셀 1.62 µm 보다 작은 틈은 둘 다에서 안 보인다 → **CT 기공은 하한** [카드 추론].  103.0 MPa 의 ≈1–4 % 를 기공률로 인용하지 않는다 (2D · 한 장 · 해상도 하한).

### 3-4. ★ 변형률 (Fig 3c · p.5) — 가압
| 압력 (MPa) | 변형률 | 오차 막대 | 할선 P/ε (MPa) [카드 산술] |
|---|---|---|---|
| 14.5 (x 10.2–18.8) | 0.264 | 0.188–0.342 | 55 |
| 27.1 | 0.383 | 0.355–0.410 | 71 |
| 33.9 | 0.380 | 0.348–0.410 | 89 |
| 46.2 | 0.431 | (표지 안) | 107 |
| 61.1 | 0.446 | (표지 안) | 137 |
| 73.7 (x 70.3–77.1) | 0.466 | 0.447–0.486 | 158 |
| 89.3 (x 86.2–92.4) | **0.491** | 0.467–0.514 | 182 |
| 99.9 (x 96.0–104.0) | 0.473 | (표지 안) | 211 |
- 전부 [판독] · 원문: *"Increase in strain from 0 to 0.4 rapidly occurred from 0 MPa to 30 MPa, but more slowly for pressures between 30 MPa and 100 MPa"* · *"the effective Young's modulus ranged from 25 MPa to 250 MPa"* (p.5) — 할선 55–211 MPa [카드 산술] 이 그 띠 안 (그림의 점선 = 원점에서 그은 할선 E 25 MPa · 250 MPa · 2.5 GPa · 25 GPa).
- 접선 [카드 산술]: 14.5 → 27.1 MPa **107 MPa** · 33.9 → 99.9 MPa **≈0.71 GPa** (구간별 0.24–0.99 GPa).  27.1 → 33.9 · 89.3 → 99.9 MPa 에서는 변형률이 줄었다 (0.383 → 0.380 · 0.491 → 0.473 — 오차 막대 안) → 측정 흩어짐 ≈ ±0.02.
- **처음 충전 상대밀도의 상한** [카드 산술]: 다이 (옆 변형 0) 이면 D = D₀ / (1 − ε) 이고 D ≤ 1 이므로 **D₀ ≤ 1 − ε_max = 0.51 (ε 0.491) – 0.53 (ε 0.473)** — 75–150 µm 각진 Li₆PS₅Br 의 부은 상태가 ≤ 51–53 % 였다.  D₀ 자체 · 다이 반경 변형 (PEEK) · 벽 마찰 [미확인] → D(P) 곡선은 만들 수 없다.
- 형상 [카드 산술]: 103 MPa 변형의 **≈81 % 가 27 MPa 까지** (0.383 / 0.473).

### 3-5. ★ 감압 (Fig 4 · 5b · p.5) — 103.0 → ≈28 MPa
| 압력 (MPa) | σ_EIS (mS/cm) | 같은 압력 가압 σ (보간) · 비 [카드 산술] | 변형률 (Fig 4c) | 계산 σ (Fig 5b) |
|---|---|---|---|---|
| 103.8 | **0.789** (0.736–0.839) | 0.789 · 1.00 | 0.462 (0.442–0.483) | 0.844 |
| 84.4 | 0.759 | 0.747 · 1.02 | 0.463 | — |
| 61.2 | 0.728 | 0.636 · 1.15 | 0.480 | — |
| 51.4 | 0.713 | 0.550 · 1.30 | 0.480 | 0.766 |
| ≈32.0 (계산점) | (보간 0.647) | — | — | 0.689 |
| 28.2 | **0.634** (0.582–0.685) | 0.383 · **1.65** | 0.473 | — |
- 전부 [판독] · σ 감소 103.8 → 28.2 MPa = **−19.7 %** (0.634 / 0.789) [카드 산술] · 원문: *"The ionic conductivity slightly decreased with the decrease in applied pressure from 103.0 MPa to 30 MPa"* · *"The structure was relatively unaffected by depressurization and the densified room-temperature-synthesized structure was maintained, even at 30 MPa"* (p.5).
- **되돌아옴 (springback) 은 이 자료로 잴 수 없다** [카드 산술]: 감압 변형률 0.462 → 0.473 (**+0.011** — 탄성 회복이면 줄어야 하는데 늘었다 · 오차 막대 ±0.02 안).  ΔP 75.7 MPa 에서 기대 회복은 E 25 GPa 이면 −0.003 · 2.5 GPa 이면 −0.030 — 둘 다 막대 안이라 저자의 *"the Young's modulus remained almost constant at 25 GPa"* 는 자료로 가를 수 없는 문장이다.
- ⚠ 다이 (옆 변형 0) 에서 응력 ÷ 변형률은 영률 E 가 아니라 **구속 탄성률 M = E(1 − ν)/((1 + ν)(1 − 2ν))** 이다 — Deng 2016 의 Li₆PS₅Br (E 25.3 · ν 0.35, 정본 deng2016 카드 Table III) 이면 M ≈ 40.6 GPa [카드 산술].  원문은 다이 측정을 'Young's modulus' 로 부른다.
- 가압 끝 (99.9 MPa 0.473 · 89.3 MPa 0.491) 과 감압 시작 (103.8 MPa 0.462) 이 0.011–0.029 어긋난다 (같은 상태로 보이는데) — 측정 흩어짐 ±0.02 의 다른 증거 [카드 산술].
- ⚠ 감압 CT 영상 압력 (103.0 · 50.0 · **27.8** [인쇄 Fig 4b]) ↔ Fig 5b 계산점 x (103.8 · 51.4 · **32.0** [판독]) — 27.8 ↔ 32.0 은 4.2 MPa 차.

### 3-6. ★ 계산 ↔ EIS — 네 재료 (Fig 5 · 6 · p.5)
| 재료 | 계산점 압력 (MPa) → 계산 ÷ 실측 [카드 산술 · 가장 가까운 EIS 점 / EIS 직선 보간] |
|---|---|
| Li₆PS₅Br 가압 (Fig 5a) | 8.7 → **1.80 / 1.80** · 32.0 → 1.20 / 1.27 · 63.1 → 1.15 / 1.15 · 103.8 → **1.07 / 1.07** |
| Li₆PS₅Br 감압 (Fig 5b) | 103.8 → 1.07 / 1.07 · 51.4 → 1.08 / 1.08 · 32.0 → 1.09 / 1.07 |
| Li₆PS₅Cl (Fig 6a) | 9.4 → **2.28 / 2.56** · 35.8 → 1.23 / 1.19 · 68.9 → 1.27 / 1.24 · 96.0 → **1.03 / 1.03** |
| LPS 유리세라믹 (Fig 6b) | 6.8 → 0.94 / 1.09 · 30.0 → **0.72 / 0.70** · 59.2 → 1.28 / 1.23 · 103.9 → 1.03 / 1.08 |
| LPS 유리 (Fig 6c) | 43.7 → 1.02 / 1.08 · 64.9 → 1.08 / 1.06 · 90.2 → 0.94 / 0.95 |
- EIS 값 (끝점) [판독]: Li₆PS₅Cl ≈**1.11 mS/cm (≈94 MPa)** (빨강에 가려 원 맞춤 — §6) · LPS 유리세라믹 0.124 (113.0 MPa · x 104.3–121.8) · LPS 유리 0.144 (91.2 MPa).
- **읽는 법 [카드 추론]**: 두 아지로다이트 (Br · Cl) 는 **저압일수록 계산이 높다** (×1.8–2.6 → ×1.03–1.07) — 계산에 없는 것 (복셀보다 좁은 접촉 목 · 접촉 저항 · 해상도 미만 틈) 이 저밀도에서 크다는 방향.  유리 · 유리세라믹은 양쪽으로 흩어져 (0.70–1.28) 방향이 없다.  저자 문장 *"The simulated results are almost the same as the experimental results"* (p.5) 은 고압에서도 계산이 실측보다 높다 (≥ 60 MPa 에서 +3–27 % · ≈100 MPa 에서 +3–7 %) · 저압 한 점에서는 ×1.8–2.6 이다.
- 오차 막대 크기: EIS ±0.03–0.06 mS/cm (Br) = 63–91 MPa 에서 ±6–9 % [판독] — ≈100 MPa 의 계산 ÷ 실측 1.03–1.07 은 그 안.

### 3-7. 전위 · 이온 흐름 지도 (Fig 7 · 8 · p.5–6)
- 8.4 MPa: *"the electric field distorted significantly and the iso-lines (black lines) of the electric potential are not parallel to the electrodes. In addition, ion flux focused in a small area of contact and ion flux density was high"* · 103.0 MPa: *"the electric field was homogeneous … The contact area of the solid electrolyte was very wide after room-temperature synthesis, and the ion flux density was almost homogenous … leads to low tortuosity"* [인쇄] p.5–6.
- 지도 = 계산 영역의 한 수직 단면 (가로 ÷ 세로 ≈1.0 [판독]) · 흐름 색 = 상대값 (0–1) · tortuosity 숫자 · 단면 위치 [미확인].

### 3-8. 시편 크기 · 계산 영역 · 축척 막대 — 서로 맞지 않는 인쇄값 [판독 · 카드 산술]
- 인쇄: 시야 1.14 mm · 복셀 1.62 µm · 계산 격자 350³ → **계산 영역 = 567 µm 정육면체 (42,875,000 셀)** [카드 산술].
- 축척 막대 (Fig 3b · 4b, 200 µm) 로 잰 단면 원 지름 **≈0.58–0.61 mm** — 이 원통 안에 567 µm 정사각이 다 들어가지 못한다 (내접 정사각 0.41–0.43 mm · 들어가는 몫 82–87 % [카드 산술]).  Fig 2 의 100 µm 막대 (126 px) 로 재면 정육면체 렌더 폭 ≈0.49 mm (두 면 · 원근 — 대략).
- ⇒ 축척 막대 · 시야 · 격자 가운데 어느 수가 틀렸는지, 계산 영역이 원통 안 어디인지 [미확인].  어느 경우든 **계산 영역 = 원래 입자 지름 3.8–7.6 개 · 입자 지름당 46–93 복셀** [카드 산술 — 567 µm ÷ 75–150 µm · 75–150 µm ÷ 1.62 µm] — 대표 부피 (RVE) 로 충분한지 원문은 다루지 않는다.

### 3-9. E · 항복 문장과 정본 카드 대조
| 원문 값 (p.5) | 원문의 근거 | 대조 (정본 카드) |
|---|---|---|
| *"From molecular dynamics simulation, the Young's modulus of Li6PS5Br is 25 GPa [17]"* | [17] Deng 2016 J. Electrochem. Soc. 163, A67 | `deng2016` 카드: **0 K 정적 DFT (PBEsol · 유한 변형 응력–변형)** · AIMD · MD 없음 · Li₆PS₅Br E **25.3** · ν 0.35 (Table III) → 값은 맞고 **방법 이름이 틀림** (결론 1 항에도 'molecular dynamics') |
| *"The 0.2% proof stress of sulfide solid electrolyte (E = 20 GPa) is about 40 MPa"* | **인용 없음** · 어느 재료인지 없음 | 40 MPa = 20 GPa × 0.002 와 정확히 같다 [카드 산술] — 0.2 % 오프셋 내력이 아니라 '변형률 0.2 % 의 탄성 응력' 일 가능성 [추정].  `lee2025` 카드 Li₆PS₅Br: Heckel σ_y,eff 133 MPa (P_y 400 MPa ÷ 3) · H 1.68 GPa → H/3 ≈ 0.56 GPa (그 카드의 우리 산술) — 40 MPa 는 그보다 3.3–14 배 낮다 |
| 가압 *"effective Young's modulus ranged from 25 MPa to 250 MPa"* · 감압 *"almost constant at 25 GPa"* | Fig 3c · 4c 의 할선 점선 | 가압 = 분말 압밀의 겉보기 할선 (재료 E 아님) · 감압 = 자료 해상도 밖 (§3-5) |
| [8] 400 MPa 에서 *"volume ratio of pores … almost zero"* | Sakuda 2013 Sci. Rep. | `sakuda2013` 카드: 75Li₂S·25P₂S₅ **유리** · *"exceeds 90 % at over 350 MPa"* (본문 유일 수치) — '거의 0' 보다 약하다 (≤ 10 % 기공) · 재료도 다르다 |

---

## 4. ★ 방법 — 장치 · 측정 사슬 · 계산

### 4-1. 장치 (Fig 1a · p.2)
PEEK 원통 (X 선 창) 안 분말을 위 · 아래 스테인리스 집전체가 누른다.  힘은 두랄루민 몸체 안 스프링이 내고 나사로 조인다 (**하중 제어 · 하중 유지 중 촬영**) — 스프링 변형을 160 kV 경 X 선 영상으로 읽어 스프링 특성으로 압력을 계산한다.  같은 셀이 EIS (대칭 차단 전극) 를 겸한다.  최대 ≈100 MPa 는 PEEK 내구 한계 (p.2).

### 4-2. 측정 사슬 (재구성)
분말 (75–150 µm) → PEEK 원통 → 나사로 압력 단계 (가압 0 → 103.8 MPa · 감압 → 28 MPa) → 단계마다 (i) 스프링 영상 → 압력 (ii) CT (복셀 1.62 µm) → 집전체 거리 → 변형률 · 단면 영상 (iii) EIS (1 MHz–10 Hz · 25 °C) → R1 → σ (기하 미인쇄) → 선택한 단계의 CT 를 계산에 (8.4 · 31.4/32.0 · 62.2/63.1 · 103.0/103.8 · 감압 51.4 · 27.8/32.0 MPa).
- **압력을 뺄 때 (탈압)**: 감압은 ≈28 MPa 에서 멈춘다 — 0 MPa 의 치수 회복 · 영상 · σ 는 없다.  다이 안 감압 가지의 변형률 변화가 오차 막대 안이라 되돌아옴 크기는 측정되지 않았다 (§3-5).

### 4-3. ★ 계산 (§2.2 · p.3 · 식 1–4)
| 항목 | 내용 | 표지 |
|---|---|---|
| 지배식 | ∇ × E = 0 (1–1) · E = −grad φ (1–2) · ∇ · j = 0 (2) · E = σ · j (3, 인쇄 그대로 — σ 를 전도도로 두면 거꾸로, 옴 법칙은 j = σE) · σ = 0 (기공) / σ_400MPa (SE) (4) | [인쇄] p.3 · 크롭 `eq_*.png` |
| 물리 가정 | 정상 상태 · 유도 자기장 없음 · 운반수 1 · 상호 확산 무시 · Li⁺ 농도 균일 → Nernst–Planck 가 옴 법칙으로 | [인쇄] p.3 |
| 형상 입력 | in situ CT 의 3D SE / 기공 분포 그대로 (image-based) · 전위차 없이 찍은 영상 (전위차를 걸고 찍어도 구조 변화 없음) | [인쇄] p.3 |
| 경계 | 가상 전극 두 장 (Fig 2 회색) 사이 · 위 1 V / 아래 0 V (Dirichlet) · 옆면 경계 [미확인] | [인쇄] p.3 |
| 이산화 | 유한체적 [15] · 격자 350 × 350 × 350 · 복셀 = CT 복셀 1.62 µm | [인쇄] p.3 |
| 풀이 | 축차 과완화 (SOR) [16] · OpenMP 병렬 · 수렴 기준 · 반복 수 · 시간 · 메모리 [미확인] | [인쇄] · [미확인] |
| 유효 σ 환산 | 전류 → σ_eff 식 (기하) [미확인] | [미확인] |
| 무시한 것 | *"The contact resistance between solid electrolyte particles and the change in ionic conductivity from internal stress is neglected in this numerical simulation."* | [인쇄] p.3 |
| 맞춘 값 | **없음** — σ_400MPa 는 다른 셀에서 잰 값 (맞춤 아님) · 계산은 예측 | [인쇄] p.3 |
| 비용 | 42.9 M 셀 한 번 · SOR — 시간 [미확인] | [카드 산술] · [미확인] |
- **우리 STEP3 와 같은 부류**: 이진 σ 복셀 FV · SE 셀 사이 면은 그대로 이어짐 · 계면 저항 항 0 = 우리 `CONTACT_FREE` 가지 (CL-81).  다른 점: 그들은 **실측 CT** 를 격자로 · 우리는 MPM 상 격자 · 입자 지름당 복셀 수 46–93 (그들) ↔ SE 2.5–7 (우리 vox 0.15–0.4 µm · SE ⌀1 µm) [카드 산술].

### 4-4. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM 한계 진술 = 말 없음** — 이 논문은 DEM 을 쓰지 않는다 (압밀을 계산하지 않고 측정한 CT 구조를 그대로 쓴다).  가까운 문장: *"This tendency is a widely observed phenomenon for powder materials and highly porous media, and the strain–stress characteristics become nonlinear [18]. This finding suggests that, for high-accuracy numerical simulation of solid electrolyte compression, nonlinear numerical simulation is required."* (p.5) — 압밀 계산이 비선형이어야 한다는 일반론뿐.
- **(ii) 소성 · 큰 변형을 계산에 넣는 어려움 = 논의 없음** — 우회는 **압밀을 계산하지 않고 측정한다** (in situ CT = 실제 입자 파쇄 · 소성 · 소결이 끝난 형상을 그대로 격자로).  비용 = 실험 (XESC · 최대 100 MPa · 75–150 µm 로 제한) · 계산은 정적 전도 하나.  소성에 관한 문장은 하나 — 접점 응력이 0.2 % 내력 (≈40 MPa · 출처 없음) 을 넘으므로 *"the solid electrolyte can plastically deform"* (p.5).  관측 기전 = **파쇄 (crushing) → 조각이 틈을 메움 → 경계 소멸** (p.5) — 단단한 구 · 형상 고정 모델에 없는 세 가지.
- **(iii) 차원**: 측정 · 계산 모두 **3D** (CT 부피 · 350³ 격자).  2D 는 표시용 단면뿐 · 2D → 3D 전이 진술 없음.
- **(iv) 탈압**: 103 → ≈28 MPa 의 σ · 변형률 · 영상 (Fig 4) — 0 MPa 없음 · 되돌아옴 측정 해상도 밖 (§3-5).

### 4-5. 기법 미니 용어집
- **in situ XCT (가압 중 X 선 CT)** = 하중을 건 채 시료를 돌려 투영을 모아 3D 를 재구성 — SEM 단면 (반드시 하중을 뺀 뒤 · 이온 밀링) 과 달리 누른 상태 그대로.
- **복셀 (voxel)** = CT 3D 영상의 화소 (여기 1.62 µm 정육면체).  **분해능** = 구별할 수 있는 가장 작은 거리 (보통 복셀의 2 배 이상) — 그보다 좁은 틈은 고체로 보인다.
- **영상 기반 계산 (image-based simulation)** = 이진화한 CT 영상의 각 복셀에 물성을 주고 바로 푸는 계산 (형상을 모델로 만들지 않음).
- **유한체적 (FV) + SOR** = 셀마다 들어오고 나가는 전류의 균형을 세우고 (FV) · 그 연립식을 축차 과완화로 반복해 푼다.
- **상온 가압 소결 (room-temperature pressure sintering)** = 황화물 SE 가 가열 없이 압력만으로 입자 경계가 사라질 만큼 치밀해지는 현상 (Sakuda 2013 의 이름).
- **0.2 % 내력 (proof stress)** = 소성 변형률 0.2 % 가 남는 응력 (금속의 항복 대용) — 이 논문 값은 출처 없음.
- **구속 탄성률 M** = 옆 변형을 막은 (다이) 일축 압축의 응력 ÷ 변형률 = E(1 − ν)/((1 + ν)(1 − 2ν)) = K + 4G/3 — 다이 감압 기울기는 E 가 아니라 M.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 (a · b) | XESC 도면 (PEEK 원통 · 집전체 · 스프링 · 나사 · 두랄루민) · Nyquist + 등가회로 R1 + C ∥ (R2 + Zw) | 가압 중 측정 셀 설계 예 (하중 제어) · σ = R1 |
| 2 | 계산 영역 (CT 노랑 SE + 가상 전극 회색 · 1 V / 0 V · 100 µm 막대) | 영상 기반 계산의 경계 · 영역 크기 대조 (§3-8) |
| 3a | ★ 가압 중 σ (Li₆PS₅Br) | 결과 전 대조 항목 후보 (재료 · 입경 표지) |
| 3b | ★ 가압 중 CT 단면 (8.4 · 31.4 · 62.2 · 103.0 MPa · XY · ZX) | 파쇄 → 메움 → 소결 (R6 · 형상) 의 실측 그림 · 2D 면적 분율 [판독] |
| 3c | ★ 가압 변형률 + 할선 E 점선 | 처음 충전 상한 D₀ ≤ 0.51–0.53 · 압밀 곡선 모양 (27 MPa 까지 81 %) |
| 4a | 감압 σ | σ 이력 (같은 압력에서 1.65 배) |
| 4b | 감압 CT 단면 (103.0 · 50.0 · 27.8 MPa) | 감압해도 구조 유지 (정성) |
| 4c | 감압 변형률 + E 점선 | 되돌아옴 측정 해상도 밖 (±0.02) — 언로딩 표적 아님 |
| 5 (a · b) | ★ 계산 (빨강) ↔ EIS (검정) 가압 · 감압 | 복셀 FV (CONTACT_FREE) ÷ 실측 = 1.80 → 1.07 |
| 6 (a–c) | Li₆PS₅Cl · LPS 유리세라믹 · LPS 유리 계산 ↔ EIS | LPSCl: 2.3–2.6 → 1.03 |
| 7 (a · b) | 8.4 MPa 전위 · 상대 이온 흐름 지도 | 접촉 목의 전류 집중 = 협착의 그림 |
| 8 (a · b) | 103.0 MPa 전위 · 흐름 지도 | 고밀도에서 균일 흐름 |
| GA | 그래픽 초록 (3D 렌더 넷 + Fig 5a 요약) | — |
| 식 크롭 6 장 | `eq_01_1_*` · `eq_01_2_*` · `eq_02_*` · `eq_03_*` (인쇄 그대로 E = σ·j) · `eq_04_*` · `eq_01_04_governing_set_with_symbols` | 보고서 수송 절에 붙일 지배식 |
| 근거 문단 12 장 | `txt_p2_*` (동기 · 재료 넷 · 합성 · 셀 · XCT · EIS · 입경 선택) · `txt_p3_*` (계산 모델 · 계산 사양 · 접촉 저항 무시) · `txt_p3_p5_*` (구조 · 변형률 · 유효 E) · `txt_p5_*` (감압 · 계산 ↔ 실측 · 0.2 % 내력 · 격자 부정합) · `txt_p5_p6_*` · `txt_p6_p7_conclusions` | 원문 인용용 |

## 6. Post-processing ★
- **무엇을**: EIS → R1 → σ (기하 미인쇄) · CT → 집전체 거리 → 변형률 · CT 단면 (정성) · 영상 기반 FV → 계산 σ · 전위 · 상대 흐름 지도.
- **안 한 것**: 기공률 · 상대밀도 계산 · 진밀도 · tortuosity 숫자 (본문은 'low tortuosity' 말만) · 입자 크기 분포 변화 · 접촉 면적 정량 · 해상도 수렴 (격자 · 복셀 바꾸기) · RVE 크기 시험 · 반복 측정 수 · 0 MPa 감압.
- **이 카드의 후처리**: 원 래스터 판독 (Fig 3a · 3c · 4a · 4c · 5a · 5b · 6a–c · 81 행 · 범례 표지 제외 · 가려진 검은 점 둘은 보이는 호에 고정 반지름 원 맞춤 — 6a ≈94 MPa · 6b ≈7.8 MPa (경계 5 화소 · 낮은 신뢰)) · 계산 ÷ 실측 (가장 가까운 점 · 직선 보간 둘) · 할선 · 접선 · D₀ 상한 · 감압 이력 비 · 2D 면적 분율 (문턱 셋) · 축척 막대 → 원 지름 (원 맞춤).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · `docs/` 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 재료 · 입경 | Li₆PS₅Br (주) · 75–150 µm · LPSCl 은 σ 하나 | Li₆PS₅Cl · DEM SE r 0.5 µm 계열 | 재료 다름 (Br) · 입경 75–150 배 — 파쇄가 주 기전인 체제 |
| 압력 · 상태 | 0 → 103.8 → 28 MPa · **누른 채** | 300 MPa · 가압 중 (판 고정 이완) | 같은 '누른 채' · 압력 ⅓ |
| 기공 | 숫자 없음 (2D 판독 ≈31 % → ≈1–4 %) | 랩 표준 10–13 % (300 MPa) · DEM ε_union ≈10 % · MPM 10.0 % (보정 표적 · CL-94) | 견줄 수 없다 (§7-2) |
| σ 솔버 | CT 복셀 FV · σ 기공 0 / SE σ_400MPa · 접촉 저항 0 | STEP3 복셀 FV (CONTACT_FREE · CL-81) · 접촉망 Holm (DEM) | **같은 부류** — 그들의 계산 ÷ 실측이 CONTACT_FREE 의 실측 대조 선례 (§7-3) |
| 입력 σ | 400 MPa 치밀 펠릿 값 (인쇄 안 됨 · Br ≥ 0.84 mS/cm 하한) | σ_grain 3.0 (펠릿 · Cronau 2021 SI S2c · CL-91) · 보고 σ₀ 1.5 | 둘 다 '치밀 펠릿 값' 을 입자 내부에 — 펠릿 안 입계 몫이 이미 들어 있다 |
| 해상도 | 입자 지름당 46–93 복셀 (처음) | STEP3 SE 지름당 2.5–7 복셀 · MPM 규칙 d_h/dx ≳ 3.5 | 그들은 해상도를 위해 입자를 키웠다 · 우리는 격자가 거칠다 |
| 탈압 | 103 → 28 MPa · σ −20 % · 변형률 변화 ±0.02 안 | DEM 언로딩 키트 (진행) · MPM 제하 없음 | 되돌아옴 표적은 못 준다 |
| 형상 | 파쇄 → 메움 → 경계 소멸 (CT · 3D) | MPM = 소성 형상 변화 (파쇄 없음) · DEM = 구 고정 | MPM 쪽 정성 증거 · 단 **파쇄**는 우리 MPM 에 없다 |
| E · 항복 | 가압 할선 55–211 MPa · 감압 "25 GPa" (해상도 밖) · 0.2 % 내력 "40 MPa" (출처 없음) | DEM E_eff 1.35 GPa (18 배 연화) · σ_y_eff 46 MPa (Heckel P_y 138 ÷ 3) · MPM E 1.53 · σ_y 0.30 · ν 0.49 (K 25.5 GPa) | 같은 양이 하나도 없다 (§7-4) |

### 7-2. ★ 랩 기준과 나란히 (판정 없이)
| 출처 | 재료 · 입경 | 압력 · 상태 | 진밀도 분모 | 기공 |
|---|---|---|---|---|
| **랩 표준** | LPSCl | 300 MPa | **1.64** (고정) | **10–13 %** |
| 이 논문 (원문) | Li₆PS₅Br · 75–150 µm | 103 MPa · 누른 채 | **없음** | **없음** (숫자 미인쇄) |
| 이 논문 (이 카드 판독 · 계산 단면 한 장) | 같음 | 103.0 MPa · 누른 채 | 해당 없음 (영상 면적) | ≈1.2 % (흰) · ≤ 4.3 % (경계 화소 포함) — **2D · 복셀 1.62 µm 미만 기공 제외 = 하한** |
| 이 논문 (인쇄 CT 단면 · 문턱 64–128) | 같음 | 103.0 MPa | 해당 없음 | 3.8–17.6 % (XY · ZX · 문턱에 따라) |
| 우리 DEM 순수 SE | LPSCl | 300 MPa · 가압 중 | 구 부피 합 | ε_union ≈10 % · 겹침 11–12 % (CLAUDE.md 2026-06-06) |
| 우리 MPM 순수 SE | LPSCl | 300 MPa · 가압 중 | MPM 관례 | 10.0 % (σ_y 0.30) — 보정 표적 · 외부 앵커 아님 (`CL-94`) |
- 이 표는 **"랩 표준과 다른 문헌 값"** 의 자리이고, 이 논문 줄은 원문 값이 아니라 판독이다 — 재료 (Br) · 입경 (75–150 µm) · 압력 (103 MPa) · 측정 (2D · 해상도 하한) 이 넷 다 다르다.

### 7-3. ★ 복셀 σ (STEP3) ↔ 이 논문의 계산 — CONTACT_FREE 의 실측 대조 선례
- 이 논문의 계산은 우리 STEP3 와 **같은 부류** (이진 σ · 계면 저항 0 · 면 그대로 이음) 이고, 그 결과를 **같은 시료의 EIS** 와 직접 견준 드문 자료다 — 순수 SE 에서 계산 ÷ 실측 = **1.80 (Br, 8.7 MPa) · 2.3–2.6 (Cl, 9.4 MPa) → 1.03–1.07 (≈100 MPa)** [카드 산술].
- ⇒ CL-81 의 *"복셀 σ 는 CONTACT_FREE 가지 위 (상한 쪽)"* 와 **방향이 같다** (계산 > 실측) · 크기는 밀도에 강하게 달린다 (저밀도 ×2 안팎 · 고밀도 ×1.05 안팎).  저밀도의 차이가 '접촉 저항' 인지 '복셀보다 좁은 목' (해상도) 인지 이 자료로는 가를 수 없다 [카드 추론].
- ⚠ 우리 쪽에 크기를 옮기지 않는다: (i) 순수 SE ↔ 우리 복합체 (AM + 첨가제) (ii) 그들 입자 지름당 46–93 복셀 ↔ 우리 SE 2.5–7 복셀 — 우리 목은 훨씬 덜 풀렸다 (iii) 입력 σ 의 정체 (400 MPa 펠릿 ↔ Cronau 펠릿 3.0) 가 다르다 (iv) 유리 · 유리세라믹은 ×0.70–1.28 로 양쪽 흩어짐.
- CL-81 이 *"미실행 1순위 = 복셀 ÷ 접촉망 대조"* 라고 적은 질문의 **실험 쪽 이웃** — 같은 침대에서 복셀 σ 와 실측 σ 를 견준 꼴 (우리는 복셀 ↔ 접촉망 · 이 논문은 복셀 ↔ EIS).

### 7-4. E · 항복 축 (frame [2]) — 같은 양이 아니다
- 가압 할선 (55–211 MPa) · 접선 (≈0.7 GPa, 34–100 MPa) [카드 산술] = **분말 압밀의 겉보기 컴플라이언스** — 우리 DEM E_eff 1.35 GPa (접촉 강성 매개변수 · 18 배 연화) 와 다른 양 · 원문의 *"effective Young's modulus … significantly lower than … molecular dynamics"* 는 우리 frame [2] 의 '연화 = 재배열 대리' 와 **말이 비슷할 뿐** 숫자를 옮기지 않는다.
- 다이 감압 기울기 = 구속 탄성률 M — 우리 MPM (E 1.53 · ν 0.49) 이면 **M ≈ 26.2 GPa** (= K 25.5 + 4G/3 0.68) [카드 산술] · 실제 Li₆PS₅Br (Deng E 25.3 · ν 0.35) 이면 ≈40.6 GPa [카드 산술] — 이 논문의 '25 GPa' 는 자료 해상도 밖이라 어느 쪽 대조 표적도 못 된다.
- "0.2 % 내력 ≈ 40 MPa" 는 우리 DEM σ_y_eff 46 MPa 와 **숫자만 가깝다** — 출처 없는 값 · E × 0.002 와 같음 · 재료 미지정 → 우리 σ_y 의 근거로 쓰지 않는다 (같은 Li₆PS₅Br 의 lee2025 Heckel σ_y,eff 는 133 MPa).

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 순수 SE 의 누른 채 3D 구조 (실측) · 그 구조 위의 **수송** (복셀 전도) ↔ 실측 σ.
- **없는 것**: 압밀 **역학 계산** (DEM · FEM · MPM 0) · 기공 숫자 · 접촉 수 · 면적 · 하중 · 복합체.  ⇒ DEM / 수송 쪽에 '복셀 FV 의 저밀도 과대' 라는 방법 교훈을, MPM / 역학 쪽에 '파쇄 → 메움 → 소결' 의 정성 그림과 '비선형 계산이 필요' 라는 일반론만 준다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ (1) CT 기공 = **이진화 복셀 부피 분율** (우리 ε_union 쪽 연산자 · 실제 점유 공간) 이지만 **복셀보다 작은 틈이 빠지는 하한** — 연산자 등록에 '해상도 · 문턱 · 하한 여부' 칸 (2) 변형률 기반 밀도 D = D₀/(1 − ε) 는 **D₀ 없이는 못 쓴다** → 우리 판 간격 기반 두께 연산자도 처음 충전 (D₀) 을 같이 기록 (3) 인쇄 영상 판독은 문턱에 따라 ×2–4 흔들린다 (§3-3) — 결과 전 대조 항목으로 쓰려면 문턱 규칙을 먼저 등록 | 기공 숫자 · 진밀도 · 문턱 규칙 원문 |
| **단계 1** (3D 메모리 · 장 수) | 350³ = 42.9 M 셀 정상 전도 한 장 (SOR · OpenMP · 2020 년 계산) [카드 산술] — 크기 감각뿐 | 메모리 · 시간 [미확인] · 역학 장 아님 |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 압밀 곡선의 **모양** (75–150 µm Li₆PS₅Br: 103 MPa 변형의 81 % 가 27 MPa 까지 · 할선 55 → 211 MPa) · 처음 충전 D₀ ≤ 0.51–0.53 [카드 산술] · 기전 = **파쇄 우세** (큰 입자) — 우리 SE (≈1 µm) 체제와 다를 수 있다는 경고 (CLAUDE.md 의 Fan 2026 '> 3 µm 파쇄 · < 1 µm 협동 변형' 과 같은 방향의 정성 증거 [카드 추론]) | 맞춤 표적 아님 (기공 숫자 없음 · 103 MPa · Br · 입경 75–150 배) — 랩 표준이 표적 |
| **단계 5** (3D 복합 압밀) | 없음 (순수 SE 만) | — |
| **단계 6** (탈압 · 되돌아옴) | ★ (1) 치밀화는 **비가역** — 감압 σ 가 같은 압력 가압 값의 1.65 배 (28 MPa) · 구조 유지 (2) 되돌아옴은 측정 해상도 (±0.02) 밖 → 기대 크기: 다이 감압의 기울기 = 구속 탄성률 M (E 아님) · 우리 MPM 이면 M ≈ 26 GPa → 300 MPa 를 뺄 때 치밀 SE 의 탄성 회복 ≈ 1.1 % [카드 산술: 0.3 / 26.2 · 가정 = 기공 없는 SE · 다이 · 순수 탄성 제하] — 이 논문의 '25 GPa' 문장은 근거가 아니다 | 0 MPa 값 · 치수 회복 숫자 · 시간 의존 |
| **단계 7** (형상 · 피복 · 수송) | ★ 복셀 FV (접촉 저항 0) ÷ 실측: 순수 SE 1.8–2.6 배 (≈9 MPa) → 1.03–1.07 배 (≈100 MPa) — STEP3 (CONTACT_FREE) 의 실측 대조 선례 · 저밀도 목에 흐름이 몰리는 지도 (Fig 7) = 협착의 그림 · 입력 σ 를 치밀 펠릿 값으로 두는 관례 (우리 σ_grain 3.0 · CL-91 과 같은 꼴) | 우리 복합체 · 우리 해상도로 크기 전이 불가 (§7-3) · tortuosity 숫자 없음 |
| **후보 D0** (지금 DEM) | 없음 (DEM 없음) — 정성: 큰 SE 의 치밀화 = 파쇄 · 메움 · 경계 소멸 (구 고정 모델에 없는 기전 셋) | E · 항복 대조 숫자 없음 (§7-4) |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 없음 | 벽 마찰 · PEEK 반경 변형 [미확인] |
| **후보 A · A′** (MPM 강체 AM / 입자별 속도장) | 없음 | — |
| **후보 B** (입자별 FE) | 없음 | — |
| **후보 C · C′** (MDR · 항복 캡 DEM) | 없음 | 0.2 % 내력 40 MPa 는 캡 · 항복 값으로 못 쓴다 (출처 없음) |
| **후보 M0** (균질화 압밀 · Heckel · 캡) | 변형률 곡선 (가압 9 점 · 감압 5 점) — D₀ 가 있으면 Heckel 꼴로 바꿀 수 있는 자료 · 원문: *"nonlinear numerical simulation is required"* | D₀ 없음 → Heckel P_y 를 낼 수 없다 |
| **U0–U6** | **U6** (작은 조밀 충전 압축의 해상도 수렴) 쪽 규칙의 실측판: 그들은 *"gaps … smaller than resolution"* 을 피하려 입자를 키웠다 (입자 지름당 46–93 복셀) — 우리 '지름당 셀 수' 규칙의 근거 문장 (U1 · U6) | 해상도 수렴 시험 자체는 없다 |
| **R1–R7** | **R4** (탈압) σ · 구조 유지 · 회복 해상도 밖 · **R6** (SE 형상 변형) CT 3D 정성 (파쇄 → 메움 → 경계 소멸) · **R3** (SE 입자 경계 기억) — 103 MPa 에서 경계가 1.62 µm 복셀로는 안 보인다 (해상도 한정 문장) · **R7** 은 AM 이 아니라 **SE 파쇄** (75–150 µm) | R1 · R2 · R5 없음 |
| **결과 전 대조 항목** | Li₆PS₅Br σ (가압 9 점 · 감압 5 점) · Li₆PS₅Cl σ (가압 8 점) · 변형률 (가압 9 · 감압 5) — 전부 [판독] · '누른 채 · 25 °C · 75–150 µm (Br) · LPSCl 입경 미상 · 기하 미인쇄' 표지와 함께 · 복셀 ÷ 실측 비 (방법 비교용) | 기공 절대값 비교 금지 (숫자 없음) |

- **재료 · 차원 · 조건 차이**: 재료 Li₆PS₅Br (주) ↔ 우리 Li₆PS₅Cl · 입경 75–150 µm ↔ ≈1 µm · 103 MPa ↔ 300 MPa · 누른 채 = 같음 · 3D = 같음 · 순수 SE ↔ 우리 복합 (단계 5 이후) · 시료 ⌀ ≈0.6 mm [판독] ↔ 우리 RVE.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **복셀 σ 를 실측과 견줄 때 밀도를 같이 적는다** — 같은 CONTACT_FREE 부류 계산이 순수 SE 에서 저밀도 ×1.8–2.6 · 고밀도 ×1.03–1.07 (§3-6) → STEP3 σ_ion 을 실험 옆에 놓을 때 '협착 미포함 = 상한' 한정어 (CL-81) 와 함께 기공 수준을 병기 (단계 7).
2. **해상도 규칙의 실측 근거** — *"to prevent a formation of small scale void that is smaller than resolution"* 로 입자를 키운 것 = 지름당 셀 수가 모자라면 틈 · 목이 사라져 σ 를 과대평가한다는 같은 경고 (우리 MPM d_h/dx ≳ 3.5 · STEP3 vox 수렴 문제) (U1 · U6).
3. **다이 감압의 기울기는 구속 탄성률 M** — 언로딩 시험 기대값을 E 로 세우지 않는다 · 우리 MPM (ν 0.49) 은 M ≈ 26 GPa 로 실재 쪽 (K 가 실제) (단계 6).
4. **치밀화 비가역 · σ 이력** — 28 MPa 에서 감압 σ = 가압 σ 의 1.65 배 · 103 MPa 대비 −20 % — 작동압 (적층압) σ 를 앵커로 쓸 때 '성형 최고압 · 측정압 · 가압 / 감압 가지' 를 표에 같이 (doux2020 의 Ti 전극 이력과 같은 꼴).
5. **인용 고리 주의** — '황화물 입자 사이 접촉 저항 무시' 는 이 논문 ↔ Otani 그룹이 서로를 근거로 든다 · 이 논문의 근거는 고압 (≥ 60–100 MPa) 일치 + 출처 없는 0.2 % 내력 — Rint ② (SE–SE 계면) 에서 '0 으로 둔다' 의 근거로 쓰려면 압력 범위를 붙인다.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In situ X-ray CT of 75–150 µm Li₆PS₅Br under 8.4–103 MPa shows particle crushing, pore filling by fragments and vanishing particle boundaries (room-temperature pressure sintering); the densified structure is retained on unloading to ≈30 MPa (Kodama et al., J. Power Sources 462 (2020) 228160)."
- "An image-based finite-volume conduction model on the in situ CT volume (pores σ = 0, solid σ of a 400 MPa pellet, no interparticle contact resistance) exceeds the measured EIS conductivity by a factor of ≈1.8 at 8.7 MPa and ≈1.07 at 104 MPa for Li₆PS₅Br (digitized from Kodama et al. 2020, Fig. 5a)."
- 국문: *"영상 기반 복셀 전도 계산 (접촉 저항 0) 은 순수 황화물에서 저밀도일수록 실측을 크게 넘는다 (×1.8–2.6 → ×1.03–1.07, Kodama 2020 판독)."*
- 국문: *"Kodama 2020 의 기공은 숫자로 보고되지 않았다 — '누른 채 구조' 의 인용은 영상 · 정성으로만."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **기공률 · 상대밀도 · 진밀도 · 시료 질량 · 지름 · 높이 미인쇄** — '누른 채 공극' 의 숫자 인용 불가 (본문 8 쪽 전수).
2. **"almost the same"** ↔ 계산 ÷ 실측 1.80 (8.7 MPa) · Cl 2.3–2.6 (9.4 MPa) [판독 · 카드 산술] — '접촉 저항 무시' 결론은 고압 범위에서만 자료가 받친다.
3. **0.2 % 내력 ≈ 40 MPa (E = 20 GPa)** — 출처 없음 · 재료 미지정 · E × 0.002 와 같다 [카드 산술].
4. **[17] Deng 2016 = 0 K 정적 DFT** ↔ 본문 · 결론의 'molecular dynamics' (값 25 GPa ↔ 25.3 은 맞음).
5. **[8] Sakuda 2013 = 75Li₂S·25P₂S₅ 유리 · > 90 % (> 350 MPa)** ↔ '400 MPa 에서 기공 거의 0' — 근거보다 강한 표현.
6. **식 (3) E = σ·j** (σ = 전도도로 정의) — 거꾸로 인쇄 · *"From Eqs. (1–1), electric potential can be defined by Eqs. (1) and (2)"* 의 식 (1) 은 없는 번호.
7. **'분해능 1.0 µm' < 복셀 1.62 µm** — 불가능한 조합 (어느 쪽이 맞는지 [미확인]).
8. **축척 막대 (원통 ⌀ ≈0.58–0.61 mm) ↔ 계산 영역 567 µm** — 정육면체가 원통에 다 안 들어간다 (§3-8).
9. **'Young's modulus ≈ 25 GPa' (감압)** — 자료 해상도 밖 (±0.02 ↔ 25 GPa 면 0.003) · 다이 측정은 M 이다 · Fig 4c 기준선은 감압하면 변형률이 커지는 쪽으로 그려졌다 (탄성 회복의 반대 부호).
10. **셀 부품 번호** — 본문 (PEEK = ② · 집전체 = ① · ③ · PEEK 부품 = ②) ↔ 캡션 (② = 고체전해질 · ③ = PEEK 옆벽 · ④ = 아래 집전체).
11. **압력 표기** — CT 영상 압력과 계산점 x 가 0.3–4.2 MPa 어긋남 (가장 큰 것: 감압 27.8 ↔ 32.0 [판독]) · Fig 5 캡션 'decreased from 103.0 MPa' ↔ 본문 '100 MPa'.
12. **오타 · 표기**: 'L6PS5Br' (p.2 · p.6) · 'X-rat CT' (p.3) · 그림 축 'Ion condictivity' · 'Ioncondictivity' · 본문 'Marm et al.' ↔ ref [13] 첫 저자 M.B. Dixit · ref [13] 학술지 이름 누락 (DOI = ACS Appl. Mater. Interfaces) · ref [18] 쪽 '17–619' (DOI jamdsm.2018jamdsm0022).
13. **다른 세 SE** — 합성 · 조성 · 입경 · 영상 · 변형률 없음 (σ 그림 하나씩) — *"these characteristics are found to be valid for all tested materials"* (초록) 는 σ 비교 하나의 확장.
14. **RVE · 해상도 시험 없음** — 계산 영역 = 원 입자 3.8–7.6 개 · 격자 · 복셀 바꾼 수렴 시험 0 · 계산 영역이 시료의 어디인지 · 어느 압력의 영상이 Fig 2 인지 [미확인].
15. ⚠ **판독 값**은 원 래스터 보정 (두 래스터의 같은 자료가 x ±0.15 MPa · y ±0.001 로 일치) — 그래도 [판독] 표지로만 인용.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 8 | A. Sakuda, A. Hayashi, M. Tatsumisago, Sulfide solid electrolyte with favorable mechanical property for all-solid-state lithium battery, Sci. Rep. 3 (2013) 2261. | 상온 가압 소결 · 400 MPa 입력 σ 의 근거 | `sakuda2013_sulfide_mechanical_property` |
| 17 | Z. Deng, Z. Wang, I.H. Chu, J. Luo, S.P. Ong, Elastic properties of alkali superionic conductor electrolytes from first principles calculations, J. Electrochem. Soc. 163 (2016) A67–A74. | Li₆PS₅Br E 25 GPa (원문 'MD' 오기) | `deng2016_elastic_superionic_electrolytes_dft` |
| 7 | Y. Kato, S. Hori, T. Saito, K. Suzuki, M. Hirayama, A. Mitsui, M. Yonemura, H. Iba, R. Knnno, High-power all-solid-state batteries using sulfide superionic conductors, Nat. Energy 1 (2016) 16030. | 서론 (25 mS/cm) | `kato2016_high_power_assb_lsipscl_superionic` |
| 18 | Y. Lei, S. Yan, S. Huang, W. Lu, S. Sun, M. Shou, F. Feng, Experimental and numerical investigation of densification behaviors during powder compaction, J. Adv. Mech. Design, Syst. Manuf. 12 (2018) 17–619. | 분말 압밀의 비선형 응력–변형 · 수치 압밀 (질문 e · l) | 없음 (papers/ ls · grep) |
| 19 | K. Otani, T. Muta, T. Furuta, M. Murata, M. Iwasaki, T. Miyuki, G. Inoue, T. Kaburagi, Y. Ishiguro, Calculational Study of Ionic Conductivity Reduction Observed in All-Solid-State-Batteries, The 60th Battery Symposium, Japan, 2MH23, 2019. | '접촉 저항 무시' 의 공동 근거 (학회 초록 · otani2023 의 앞판) | 없음 |
| 20 | T. Miyuki, Y. Morino, K. Otani, Denki Kagaku 88 (2020) 54–64. | 기공비 ↔ tortuosity 지수 상관 (같은 근거 · 같은 그룹) | 없음 |
| 13 | M.B. Dixit, M. Regala, F. Shen, X. Xiao, K.B. Hatzell, Tortuosity Effects in Garnet-Type Li7La3Zr2O12 Solid Electrolytes, 11, 2018, pp. 2022–2030. | 산화물 SE 의 CT 기반 tortuosity (단계 7) | 없음 |
| 12 | C. Tan, S.R. Daemi, O.O. Taiwo, T.M.M. Heenan, D. Jl Brett, P.R. Shearing, Evolution of electrochemical cell designs for in-situ and operando 3D characterization, Materials 11 (2018) 2157. | in situ CT 셀 재료 (PEEK · PFA) | 없음 |
| 15 · 16 | M. Tanaka, Y. Okuno, Plasma behavior in a high-temperature noble gas plasma disk-shaped MHD power generator, Electr. Eng. Jpn. 197 (2016) 33–40. · S.P. Frankel, Convergence rate of iterative treatments of partial differential equations, Am. Math. Soc. 4 (1950) 65–75. | FV 이산화 · SOR 의 출처 (방법 추적만 — [15] 는 플라스마 발전기 논문) | 없음 |
- **같은 그룹 · 이 논문이 인용하지 않은 후속 (다른 카드가 인용)**: M. Kodama, A. Ohashi, S. Hirai, J. Power Sources Adv. 4 (2020) 100019 (단일 SE 입자 고압 XCT · `faka2026` ref 21) · A. Ohashi, M. Kodama, … S. Hirai, J. Power Sources 470 (2020) 228437 (복합 전극 응력 분포 · `heck2026` ref 61) — 정본 카드 없음 (grep "100019" · "228437").

---

## [미확인] 목록
- 기공률 · 상대밀도 · 진밀도 · 시료 질량 · 지름 · 높이 · 처음 충전 밀도 D₀ · 변형률 기준 높이 h₀.
- XCT 투영 수 · 노출 · 재구성 알고리즘 · 잡음 처리 · **이진화 문턱** · '분해능 1.0 µm' 의 정의.
- EIS σ 환산 기하 · 오차 막대 정의 (반복 수) · 어느 압력의 Nyquist 인지 (Fig 1b).
- 입력 σ_400MPa 의 값 (재료별) · 그 셀의 기하 · 밀도.
- 계산: 옆면 경계 · 수렴 기준 · 반복 수 · 시간 · 메모리 · 유효 σ 환산식 · 계산 영역의 위치 · Fig 2 의 압력.
- 다른 세 SE (Li₆PS₅Cl · LPS 유리 · LPS 유리세라믹) 의 출처 · 조성 · 합성 · 입경 · 영상.
- 다이 (PEEK) 반경 변형 · 벽 마찰 · 가압 / 감압 속도 · 단계 유지 시간 · 온도 (CT 중).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 서지: 1저자 메모 (M. Kodama, S. Komiyama, A. Ohashi, … · 제목 · J. Power Sources 462 (2020) 228160) = 원문 첫 쪽과 같음 · 전체 저자 여섯 (N. Horikawa · K. Kawamura · S. Hirai 추가) · DOI 원문 첫 쪽 · PDF 메타데이터와 같음.  SI · 부록 안내 없음 (8 쪽 텍스트 층 전수).
- 숫자: 텍스트 층 + 8 쪽 렌더로 대조 — 1.14 mm · 1.62 µm · 66 kV · 44 mA · 8 mm · 160 kV · 70 µA · 100 MPa · 1 MHz–10 Hz · 25 °C · −70 · −80 °C · 3 g · 50 ml · 0.1 ml · 16 · φ10 mm · 1200 rpm · 20 h · 490 °C · 5 h · 75–150 · 20–40 · 40–75 µm · 1.0 µm · 1 V · 350 × 350 × 350 · 8.4 · 31.4 · 62.2 · 103.0 · 50.0 · 27.8 MPa · 0 → 0.4 · 30 MPa · 25 GPa · 25–250 MPa · 0.2 % · 20 GPa · 40 MPa — 전부 위치 확인.
- 'porosity' 는 본문에 한 번 (*"volume ratio and porosity"* p.5) — 숫자와 함께 나온 곳 없음 · '%' 는 '0.2%' (두 번) 뿐 · 'density' 는 'current density' · 'ion(-)flux density' · 서론의 'energy density' 뿐 · 'relative / true / theoretical density' · 'packing' · 'supplementary' 0 회.
- 판독 보정: 각 그림의 큰 눈금 직선 맞춤 (잔차 y ≤ 0.001 · x ≤ 0.11 MPa) · Fig 3a ↔ 5a · 4a ↔ 5b 의 같은 자료 대조로 재현성 확인 · 겹침 그림 (검출 원 · 범례 제외) 을 눈으로 확인.
- 정본 중복 확인: papers/ 목록 · DOI · '228160' · 'High-pressure in situ X-ray' · 'kodama' grep — 카드 없음 (otani2023 · yadav2021 · faka2026 인용 · heck2026 은 같은 그룹 다른 논문 인용).

## 🔗 관련 카드
- 이 논문을 인용한 카드: `otani2023_ionic_conductivity_path_resistance_separation_model` (ref 22) · `yadav2021_lpscl_sieved_psd_impedance_tortuosity` (ref 5) · `faka2026_particle_size_consolidation_strain_lpscl` (ref 12).
- 압밀 · 회복 실측 (황화물 SE): `doux2020_pressure_effects_sulfide_se_jmca` · `miss2026_insitu_conductivity_porosity_pressure_compaction` · `lee2025_heckel_argyrodite_powder_densification_nanoindentation` · `thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography` · `heck2026_densification_sulfide_se_binder_scalable` · `var2026_sulfide_se_mechanical_properties_local_indentation_pellet` · `sakuda2013_sulfide_mechanical_property`.
- 영상 기반 수송 · tortuosity: `taufactor_tortuosity_factor_tomography_tool` · `landesfeind2018_tortuosity_impedance_vs_tomography` · `hlushkou2018_void_space_ion_transport_assb_cathode` · `minnmann2024_microstructure_porosity_visualization`.
- 접촉 저항 · 경로 분리: `otani2023_ionic_conductivity_path_resistance_separation_model` · `so2021_dem_mold_pressure_assb_coldpress` (otani2023 의 ref 7).
- 탄성 상수: `deng2016_elastic_superionic_electrolytes_dft`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
