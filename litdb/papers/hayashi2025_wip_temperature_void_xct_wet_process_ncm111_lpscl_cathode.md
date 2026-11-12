<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 후보 표 N-64 · 정독 116) 에서 꼭 뽑으라고 한 항목.
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 상자 · 두 필수 절 §0-1 고른 의도 대조 · §8 자세한 분석).
     원문 = 출판본 7 쪽 (J. Jpn. Soc. Powder Powder Metallurgy 72 (2025) S1167–S1173 · Supplement · CC BY-NC-ND · 영문) · 보충 자료 없음 · 표 없음 · 번호 붙은 식 · 따로 조판된 식 없음.
     쪽 표기 = "p.N" = PDF 쪽 N (1–7) = 인쇄 쪽 S(1166 + N) (p.1 = S1167 … p.7 = S1173).  크롭 파일 이름의 pN 과 figures.json 의 page 도 PDF 쪽이다.
     값 표지: [인쇄] = 본문 · 캡션 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 107 행 — Fig. 3 · Fig. 8 은 벡터 그림이라 표지 중심과 축 틀을
     PDF 그리기 객체에서 그대로 읽었다 (화소 판독 아님) · Fig. 2 · 4 · 5 · 6 · 7 · 9 는 PDF 에 박힌 원 래스터 (200–257 dpi) 에서 색 · 회색값으로 읽었다) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드에 적힌 값 (그 카드 slug 병기) ·
     [우리] = 우리 쪽 값 (CLAUDE.md 출처) · [미확인] = 본문 7 쪽 전수에 없음.
     원문 7 쪽은 글자 층 추출 + 전 쪽 렌더로 전부 읽었다 (글자 층은 µ · ° · Ω 를 잃는다 — 렌더에서 옮겼다).  DEM · MPM · FEM · 어떤 계산도 없다 — 실험만 (공정 → 구조 → 전지). -->
# 슬러리 도포 LiNbO₃ 코팅 NCM111 + Li₆PS₅Cl 복합 양극 시트 (74 : 23 : 3 wt% · 바인더 · 아세틸렌 블랙 · Al 박 · 도포 뒤 ≈170 µm) 의 온간 등방 가압 (WIP · **600 MPa 하나** · 상온–190 °C · 유지 1 s–1 min) — 압력을 뺀 뒤 SPring-8 싱크로트론 X 선 CT (화소 0.65 µm · AM / SE / 기공 + 탄소 세 갈래 분류) 의 'void ratio' 0.19 → 0.057 (상온) · 0.042 (100 °C) · 0.039 (150 °C) · 두께 169 → 103 · 97 · 95 µm · 1 s 에 두께는 끝나고 기공은 0.087 → 0.029 (60 s) 로 뒤따라 준다 · 0.1C 방전 ≈110 → 125 → 128 mAh/g · EIS 호 (R2) 축소 — 압력별 값 · 단축 가압 대조 · 진밀도 기공은 없다 — Hayashi · Mori · Fukuda · Ito · Manabe (J. Jpn. Soc. Powder Powder Metallurgy 2025)

> slug `hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode` · DOI `10.2497/jjspm.16C-SIS6-03` · type `experiment (wet slurry-coated cathode sheet · warm isostatic pressing (WIP) densification / compaction · ex situ synchrotron X-ray CT 3-class voxel segmentation porosity ("void ratio") · thickness · cryo-FIB cross-section SEM / EDS microstructure morphology · charge–discharge · EIS impedance — no DEM / MPM / FEM)` · PDF `87762e6f-64._Application_of_Warm_Isostatic_Pressing_to_Densification_of_All_Solid-State_Composite_Cathode_Electrodes_in_All_Solid-State_Lithium-Ion_Batteries.pdf` · SI 없음 · digested `2026-11-12` · status ✅
>
> **원제**: *Application of Warm Isostatic Pressing to Densification of All Solid-State Composite Cathode Electrodes in All Solid-State Lithium-Ion Batteries* (p.1)
> **저자**: **Kazushi HAYASHI\*** ¹ · Takuya MORI ² · Kazunori FUKUDA ² · Hiroyuki ITO ³ · Yasuo MANABE ³ — ¹ Applied Physics Research Laboratory, Kobe Steel, Ltd. (Kobe) · ² Kobelco Research Institute, Inc. (Kobe) · ³ New Business Development Division, Machinery Business, Kobe Steel, Ltd. (Takasago) — \* 교신 (hayashi.kazushi@kobelco.com) · *J. Jpn. Soc. Powder Powder Metallurgy* **72** (2025) **S1167–S1173** (쪽 아래 인쇄: *"Journal of the Japan Society of Powder and Powder Metallurgy" Vol. 72 Supplement* · "March, 2025") · 접수 2024-06-28 · 수정 2024-09-19 · 채택 2024-09-23 · ©2025 Japan Society of Powder and Powder Metallurgy · **CC BY-NC-ND** · 키워드 *Warm Isostatic Pressing (WIP), All-solid-state battery, Synchrotron X-ray computed tomography (CT), Electrochemical performance* · 빔타임 = SPring-8 BL16B2 (SUNBEAM) 과제 2021A5320 · 2021B5320 · 2022A5320 · 2022B5320 · 2023A5320 · 2023B5320 · 연구비 · 이해관계 진술 없음 (저자 소속 = WIP 장치 제조사).
> **이웃 카드 (링크만)**: [`benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem`](benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem.md) (이 논문을 ref [27] 로 인용 — 그 카드 L439 가 "카드 없음" 으로 가리켰다 · WIP 400 MPa · 80 °C ↔ 단축 116 MPa) · [`interfacial_impedance_formulation_assb_cathode`](interfacial_impedance_formulation_assb_cathode.md) (이 논문 ref 15 = Choi 2024 · 단축 ↔ 등방 가압 · WIP 500 MPa · 85 °C) · [`sakuda2013_sulfide_mechanical_property`](sakuda2013_sulfide_mechanical_property.md) (ref 10) · [`froboese2019_microstructure_ionic_conductivity_assb_electrode`](froboese2019_microstructure_ionic_conductivity_assb_electrode.md) (ref 9) · [`sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps`](sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps.md) (같은 AM — LiNbO₃ 코팅 NCM111 · SPring-8 CT · **누른 채** 0–100 MPa) · [`jeong2024_operando_densification_chemomechanics_se_size_composite_cathode`](jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md) (무하중 XCT 분할 기공) · [`larson2025_hot_pressing_argyrodite_low_stack_pressure_conductivity`](larson2025_hot_pressing_argyrodite_low_stack_pressure_conductivity.md) · [`wang2024_hot_pressed_lpscl_pressure_invariant_conductivity`](wang2024_hot_pressed_lpscl_pressure_invariant_conductivity.md) (순수 LPSCl 열간 가압).
> **판독 원자료**: `litdb/figures/hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode/digitized.csv` (107 행 — Fig. 3 표지 6 · Fig. 8 표지 8 (벡터) · Fig. 2 a–d · Fig. 9 범주 그림의 면적 분율 · Fig. 4 세 곡선 (끝 용량 · 평탄 · 정해진 용량의 전압) · Fig. 5 Nyquist 호 · Bode · Fig. 6 SEM 회색값 분율 · 덩이 지름 · Fig. 7 Mn 띠 높이) · 그림 크롭 **36 장** (도구 2 장 = 둘 다 다시 자름 + 손 34 = 도구가 놓친 Fig. 1–7 · 패널 11 · 등가 회로 삽입도 1 · 근거 문단 15 · **식 크롭 0 — 원문에 식이 없다**) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: LiNbO₃ 코팅 NCM111 · Li₆PS₅Cl · 아세틸렌 블랙 · 바인더를 슬러리로 Al 박에 발라 말린 복합 양극 시트 (74 : 23 : 3 wt% · 도포 뒤 ≈170 µm) 를 라미네이트 봉지에 진공 밀봉해 **600 MPa 한 압력**으로 등방 가압하면서 온도 (상온 · 100 · 150 · 190 °C) 와 유지 시간 (1 · 30 · 60 s) 만 바꿨더니 — **압력을 뺀 뒤** 지름 0.8 mm 유리 모세관에 넣어 찍은 싱크로트론 X 선 CT (SPring-8 BL16B2 · 30 keV · 화소 0.65 µm) 의 "void ratio" (= 기공 **+ 탄소** 로 분류된 복셀 ÷ 전체 복셀) 가 가압 전 0.19 → 상온 0.057 → 100 °C 0.042 → 150 °C 0.039 로 [판독 · 벡터 그림], 두께가 ≈170 → ≈104 → 94 µm 로 (본문) 줄고, 0.1C 방전 용량이 ≈110 → 125 → 128 mAh g⁻¹ 로 늘고 과전압이 ≈0.1 V 줄며, EIS 의 호 (저자: 전하이동 저항 — ref. 16 인용) 가 작아진다 (p.3–4).  100 °C 에서 유지 시간만 바꾸면 **두께는 1 s 에 이미 95 µm** 인데 void ratio 는 0.087 (1 s) → 0.036 (30 s) → 0.029 (60 s) 로 뒤따라 준다 — 저자는 *"densification was interrupted due to contact with each AM particle"* 뒤 등방압 아래에서 AM · SE 가 움직이며 기공이 서서히 메워지는 **두 단계**로 읽는다 (p.5).  **압력을 바꾼 자료 · 단축 가압한 전극과의 대조 · 질량 / 진밀도 기공 · 가압 중 상태 · 탈압 회복은 없다.**

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 재료 · 조성 · 시편 꼴 | AM = **Li(Ni₁/₃Mn₁/₃Co₁/₃)O₂ (NCM111) · LiNbO₃ 코팅** · SE = **Li₆PS₅Cl** · 도전재 = 아세틸렌 블랙 · **바인더 있음** (종류 [미확인]) · 용매 (종류 [미확인]) → 슬러리 → **Al 박 위 도포 · 건조 (습식 시트)** · *"electrode composition of 74:23:3wt%"* (세 숫자가 각각 무엇인지 원문이 짝짓지 않았다 — 순서상 AM : SE : (탄소 + 바인더) 로 읽힘 [카드 해석] · §3-1) · 도포 뒤 두께 ≈170 µm · 입경: SE *"on the order of several microns"* · AM *"very coarse after coating"* (숫자 없음) · SEM 에서 AM 덩이의 단면 지름 중앙 ≈6 µm (2.5–8.9 µm) [판독] · 로딩 · 밀도 [미확인] | [인쇄] p.1 · p.2 · [판독] Fig. 6 |
| ② ★ 가압 (방식 · 압력 · 온도 · 시간) | **등방 (WIP)** — 피스톤식 수직 CIP 장치 + 외부 시료 히터 (Kobe Steel) · 용기 ⌀80 × 180 mm · **600 MPa (고정)** · 온도 **상온 (RT) – 190 °C** (장치 최대) · 순서: 압력 매체 가열 → 대기압에서 시료 장입 → 가압 → 유지 → 감압 · 유지 **1 min** (따로 말이 없으면) · 시간 시리즈 1 · 30 · 60 s (100 °C) · 압력 매체 · 승압 · 감압 속도 [미확인] | [인쇄] p.2 · p.5 |
| ③ ★ **압력별** 기공 · 상대밀도 · 두께 | **없음** — *"the process pressure was set at 600 MPa"* (p.2) · *"WIP was conducted at 600 MPa for all experiments"* (p.2).  있는 것 = **온도별 3 점 + 시간별 3 점 + 가압 전** 의 void ratio · 두께 (아래 표 · §3-4 · §3-5).  상대밀도 · 질량 기공 **없음** | [인쇄] p.2 · [판독] Fig. 3 · Fig. 8 |
| ④ ★ 기공을 어떻게 쟀나 | 싱크로트론 X 선 CT · SPring-8 SUNBEAM **BL16B2** · 단색 **30 keV** · 180° · 0.1° 마다 · 노출 4 s · 검출기 Xsight Micron LC · **유효 화소 0.65 µm** · 시료 = **⌀0.8 mm 유리 모세관 (Ar)** 에 봉입 = **압력을 뺀 뒤 (ex situ)** · 성분별로 따로 정한 CT 값으로 복셀을 **AM / SE / 기공 · 탄소 세 갈래**로 분류 (*"Voids and carbon-related materials were not distinguished"*) · void ratio = 기공 · 탄소 복셀 수 ÷ 전체 복셀 수 · 분석 부피 · 문턱값 · 반복 [미확인] | [인쇄] p.2 · p.3 |
| ⑤ 온도 효과 (600 MPa · 60 s) | void ratio **0.0568 (RT) → 0.0419 (100 °C) → 0.0386 (150 °C)** · 두께 **102.97 → 97.46 → 94.74 µm** [판독 · 벡터] (본문 *"approximately 104 µm to 94 µm"* · *"saturated trend at around 0.04"*) · 190 °C 는 SEM · EDS 뿐 (수치 없음) | [판독] Fig. 3 · [인쇄] p.3 |
| ⑥ 시간 효과 (600 MPa · 100 °C) | 가압 전 **0.1906 · 169.3 µm** → 1 s **0.0873 · 94.5 µm** → 30 s **0.0362 · 99.0 µm** → 60 s **0.0287 · 97.5 µm** [판독 · 벡터] · 본문 *"The thickness of the electrode after 1 s WIP was 95 µm, consistent with the 30 and 60 s samples, within the variation of sample preparation"* · *"suggesting a two-step process"* | [판독] Fig. 8 · [인쇄] p.5 |
| ⑦ 미세구조 (SE 경계 · 합체) | 단면 SEM (cryo-FIB): 상온 WIP = 치밀해졌지만 *"most AM and SE particles remained isolated, with boundaries"* · 190 °C = *"the SE particles coalesced to form large particles without boundaries"* · Mn EDS: 고온에서 AM 이 *"replaced"* (자리 옮김으로 읽힘) → *"a softening of the SE, resulting in increased fluidity and enhanced movement of particles"* (정량 없음) | [인쇄] p.5 · Fig. 6 · Fig. 7 |
| ⑧ 전기화학 ↔ 기공 | 0.1C 방전 **≈110 · 125 · 128 mAh g⁻¹** (RT · 100 · 150 °C) · 과전압 150 °C 가 RT 보다 **≈0.1 V** 낮음 · EIS: 원점에서 ≈20 Ω 떨어진 호 + 저주파 꼬리 · 호 = 전하이동 관련 저항 (ref. 16 인용) · *"changes in R2 are dominant"* · **맞춤값 미인쇄** · 호 폭 [판독] ≈123 → 75 → 64 Ω · 0.01 Hz 임피던스 크기 252 → 177 → 148 Ω | [인쇄] p.4 · [판독] Fig. 4 · Fig. 5 |
| ⑨ 저자가 말한 기전 | (1) 순간 치밀화 (1 s 에 두께 완료) → AM 끼리 닿아 멈춤 → *"many voids remained in the SE because the contact of the AM particles resulted in releasing applied pressure in the surroundings"* (2) 등방압 아래 AM · SE 가 움직이며 기공이 서서히 감소 — **응력 · 물성 측정 없는 추론** · *"the mechanical properties of the SE should be clarified, which will be an extension of the present work"* | [인쇄] p.5 |
| ⑩ 없는 것 | 압력 의존 · 단축 가압 전극 대조 · 질량 · 진밀도 · 상대밀도 · 가압 중 (in situ) 상태 · 탈압 회복 · 이온 / 전자 전도도 · tortuosity · 피복 · 접촉 면적 · 입자 파괴 평가 · 오차 막대 · 반복 수 · WIP 안 한 전극의 전지 자료 · 190 °C 의 수치 · 고온에서의 화학 변화 확인 (XRD 등) | 전수 확인 |

**조건별 값 한 표** (600 MPa 등방 · 전부 **압력을 뺀 뒤** · void ratio = 기공 + 탄소 복셀 분율 · 두께 재는 법 [미확인]):

| 조건 | void ratio (CT · 3D 복셀) | 두께 (µm) | 가압 전 대비 두께 [카드 산술] | 범주 그림 한 장의 면적 분율 AM / SE / 기공 + 탄소 [판독] | 전지 (0.1C 방전 · EIS 호 폭) |
|---|---|---|---|---|---|
| 가압 전 (도포 · 건조) | **0.1906** [판독 Fig. 8] | **169.3** [판독] (본문 "approximately 170") | — | 0.298 / 0.506 / 0.197 (Fig. 2d) | 자료 없음 |
| 상온 (RT) · 60 s | **0.0568** [판독 Fig. 3] | **102.97** (본문 "approximately 104") | −39.2 % | 0.453 / 0.484 / 0.063 (Fig. 2a) | ≈110 [인쇄] (109.7 [판독]) · ≈123 Ω [판독] |
| 100 °C · 1 s | **0.0873** [판독 Fig. 8] | **94.54** (본문 "95") | −44.2 % | 0.552 / 0.362 / 0.086 (Fig. 9) | — |
| 100 °C · 30 s | **0.0362** [판독 Fig. 8] | **99.03** | −41.5 % | — | — |
| 100 °C · 60 s | **0.0419** [판독 Fig. 3] ↔ **0.0287** [판독 Fig. 8] | **97.46** (두 그림에서 같음) | −42.4 % | 0.525 / 0.427 / 0.048 (Fig. 2b) | ≈125 [인쇄] (126.1) · ≈75 Ω |
| 150 °C · 60 s | **0.0386** [판독 Fig. 3] (본문 "around 0.04") | **94.74** (본문 "94") | −44.0 % | 0.497 / 0.463 / 0.041 (Fig. 2c) | ≈128 [인쇄] (129.2) · ≈64 Ω |
| 190 °C (유지 시간 미기재) | **없음** | **없음** (Mn EDS 띠 ≈102 µm [판독 Fig. 7b]) | — | — | 없음 (SEM · EDS 만) |

⛔ **한정어 (떼지 말 것)**: ① **압력은 600 MPa 하나** — "압력별" 자료가 아니다 · 등방 (유체 압력 · 봉지) 이고 단축 가압한 같은 전극이 없다 ② void ratio 는 **기공 + 탄소 갈래의 복셀 분율** (질량 · 진밀도 기공 아님) · **압력을 뺀 뒤** · 화소 0.65 µm — SE 입자 ("수 µm") 사이의 잔 기공은 "SE 갈래" 에 묻힌다: 가압 전 CT 값 0.19 인데 두께가 39–44 % 줄었으므로 가압 전 전체 기공은 **≥ 0.39–0.44** 여야 한다 [카드 산술 · §3-6] ③ 조건마다 **시료 하나** (오차 막대 · 반복 없음) — 같은 조건 (100 °C · 60 s) 의 void ratio 가 두 그림에서 0.042 ↔ 0.029 로 다르고 두께 산포는 저자 스스로 *"within the variation of sample preparation"* (≈ ±2–3 µm) ④ 온도 축은 3 점 (190 °C 는 수치 없음) · 고온에서 SE · 계면의 화학 변화는 확인하지 않았다 ⑤ EIS 호의 "전하이동" 귀속은 인용 하나 · 맞춤값 미인쇄 · 그린 사이클 번호 · 측정 온도 [미확인] ⑥ 재료: NCM111 (우리 NCM811) · 바인더 든 **슬러리 시트** (우리 = 바인더 없는 분말 침대 DEM · 건식) · 조성 74 wt% AM.
⇒ **절대값 전이: 0 건.**  전이되는 것은 **방향** (같은 압력에서 온도 ↑ · 유지 시간 ↑ → 보이는 기공 ↓ · 계면 저항 ↓ · 두께는 순간에 끝남) 과 **측정 · 보고 꼴** (영상 기공의 연산자 · 탄소 포함 · 무하중 표지 · 두께와 같이 보고) 뿐이다.

**등방 600 MPa ↔ 우리 일축 300 MPa** (머리 요약용): ① 하중 경계 — 이 논문은 진공 봉지를 사이에 둔 **유체 압력** (단단한 판 · 금형 벽 · 벽 마찰 없음 · 시트 윗면이 요철을 따라 눌림) ↔ 우리 DEM · MPM 은 **단단한 판 + 옆면 주기 / 구속** ② 응력 상태 — 등방은 옆 방향 응력도 p (거시 편차 응력 ≈0) ↔ 일축 구속 압축은 옆 응력이 축 응력보다 작다 [카드 해석 — 원문은 응력 상태를 논하지 않았다] ③ 그런데 **변형은 두께 방향뿐**이다: 범주 그림의 AM 기둥 (AM 면적 분율 × 두께) 이 가압 전후 49.5 ± 2.5 µm 로 보존된다 [판독 · 카드 산술 · §3-6] — Al 박 위 얇은 시트라 면 방향으로 퍼지지 않는다 → 운동학은 우리 일축과 같고 **경계 응력만 다르다** ④ 압력 2 배 · 온도 (상온–190 °C ↔ 우리 상온) · 바인더 · 출발 상태 (도포 · 건조 시트 ↔ 느슨한 분말) 가 다르다 ⑤ 측정 상태 — 이 논문은 전부 **감압 뒤**, 우리 ε 는 판 고정 상태 (DEM) · 랩 표준은 순수 SE 300 MPa.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-64 의 '왜' 칸)

의도 원문: *"단계 5 (결과 전 대조 후보) — "★ WIP 복합 양극 치밀화 (계면 · 전하이동 저항 감소의 선행)" · 압력별 기공 값이 있는지는 [미확인]"* (가리킨 카드 = `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` L439)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "WIP 복합 양극 치밀화" | **채움** | p.1 초록 · p.3 · p.5–6 · Fig. 2 · 3 · 8 · 9 — NCM111 (LiNbO₃ 코팅) + Li₆PS₅Cl 슬러리 시트 74 : 23 : 3 wt% · **600 MPa 등방** · 상온–150 °C · 60 s: void ratio (CT 기공 + 탄소 복셀 분율 · 화소 0.65 µm · **감압 뒤**) 0.191 → 0.057 · 0.042 · 0.039 [판독] · 두께 ≈170 → ≈104 → 94 µm [인쇄] · 진밀도 기준 없음 |
| "(계면 · 전하이동 저항 감소의 선행)" | **채움** (한정 셋) | 초록 *"The voids in the electrodes decreased as the WIP temperature increased, resulting in improved charge-discharge properties, which suggests a reduction in charge transfer resistance"* · 결론 *"EIS showed that the resistance related to charge transfer decreased with increasing WIP temperature, indicating the formation of an excellent interface between AM and SE"* (p.6) · Fig. 5 — ⚠ (i) 변수는 **온도** (압력 아님) (ii) R2 맞춤값 미인쇄 — 호 폭 ≈123 → 75 → 64 Ω 는 [판독] (iii) "전하이동" 귀속은 ref. 16 인용 하나 (분리 시험 없음) · 셀 = 시트 전극 + 600 µm 펠릿 SE + In–Li · 구속압 150 MPa · EIS 3.3 V (충전 중) |
| "압력별 기공 값이 있는지는 [미확인]" | **없음** | 압력은 **600 MPa 하나** (p.2 두 군데 · p.4 · p.5 · p.6 · 캡션 Fig. 4 · Fig. 8).  대신 있는 것 = 온도별 (RT · 100 · 150 °C) 과 유지 시간별 (1 · 30 · 60 s @100 °C) void ratio · 두께 (위 조건별 표).  상대밀도 · 질량 기공 · 가압 중 값 없음 |
| "단계 5 (결과 전 대조 후보)" | **일부** | 복합 양극을 누른 뒤의 구조 값이 있다는 점에서 후보는 맞다 — 그러나 등방 · 600 MPa · 바인더 든 시트 · 승온 · 감압 뒤 · 영상 갈래 분율이라 우리 단계 5 (일축 300 MPa · 분말) 와 **같은 양이 아니다** → 방향 항목으로만 (§8 · §9) |

**가리킨 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `benhadjali2026_…` L439 (그 논문 ref [27]) | 서지 *"K. Hayashi, T. Mori, K. Fukuda, H. Ito, Y. Manabe, Application of Warm Isostatic Pressing to Densification of All Solid-State Composite Cathode Electrodes in All Solid-State Lithium-Ion Batteries, 粉体および粉末冶金 72 (2025) S1167–S1173. https://doi.org/10.2497/jjspm.16C-SIS6-03."* | 저자 다섯 · 제목 · 권 72 · 2025 · S1167–S1173 · DOI **같다** (p.1 머리).  학술지 이름은 원문 인쇄가 *"J. Jpn. Soc. Powder Powder Metallurgy"* (쪽 아래 *"Journal of the Japan Society of Powder and Powder Metallurgy" Vol. 72 Supplement*) — 일본어 이름은 이 PDF 에 인쇄되어 있지 않다 (그 카드는 benhadjali 원문 목록의 표기를 그대로 옮긴 것 · 오류 아님) | **채움** |
| `benhadjali2026_…` L439 | *"카드 없음 — ★ WIP 복합 양극 치밀화 (계면 · 전하이동 저항 감소의 선행)"* | 초록 · 결론과 같은 내용 (위 표) · 이제 카드 있음 | **채움** — 단 "치밀화" 의 측정이 영상 갈래 분율 (기공 + 탄소) 이고 변수가 온도 · 시간이라는 한정이 그 한 줄에는 없다 (요약 한 줄이라 당연 · 카드 문제 아님) |
| 후보 표 N-64 | *"압력별 기공 값이 있는지는 [미확인]"* | **없음** (600 MPa 하나) | [미확인] 해소 = **없음** |

⇒ **의도 대조 결과: 일부** — WIP 복합 양극 치밀화 · 전하이동 저항 감소 서술은 **채움** (값은 온도 · 시간 축 · 영상 기공 · 호 폭은 판독), **압력별 기공은 없음** (600 MPa 하나 · 단축 가압 대조도 없음), 단계 5 대조에는 **방향으로만** 쓸 수 있다.  가리킨 카드의 2 차 인용은 원문과 같다 (카드 문제 0 건).

---

## 1. 한 줄 요약
Kobe Steel 그룹이 자사 CIP 장치에 히터를 단 WIP 로 **슬러리 도포 복합 양극 시트**를 600 MPa 에서 누르며 온도 · 유지 시간을 바꾸고, 감압 뒤 싱크로트론 CT 의 세 갈래 복셀 분류 (AM · SE · 기공 + 탄소) 로 "void ratio" 를, 따로 두께를, cryo-FIB 단면 SEM · Mn EDS 로 입자 경계를, 펠릿 SE 에 얹은 시험 셀로 0.1C 충방전 · EIS 를 봤다.
온도를 올릴수록 보이는 기공 · 두께 · 과전압 · EIS 호가 줄고 용량이 늘며 (상온 → 100 °C 의 변화가 크고 100 → 150 °C 는 작다), 190 °C 에서는 SE 입자 경계가 사라진다.  시간 축에서는 두께가 1 s 에 끝나고 기공만 60 s 까지 뒤따라 준다 → 저자의 "두 단계" 해석.
저자의 결론: *"The duration dependence of the structural changes suggests two process steps. The enhanced movement of AM and SE particles could lead to improved electrochemical properties of the electrodes."* (p.6 · `txt_p6_conclusions_acknowledgments.png` · 초록 = `txt_p1_abstract_keywords.png`)

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| K. Hayashi\* · T. Mori · K. Fukuda · H. Ito · Y. Manabe (Kobe Steel · Kobelco Research Institute) | J. Jpn. Soc. Powder Powder Metallurgy 72 (2025) S1167–S1173 (Supplement · CC BY-NC-ND) | 10.2497/jjspm.16C-SIS6-03 | **Li₆PS₅Cl** + **NCM111 (LiNbO₃ 코팅)** + 아세틸렌 블랙 + 바인더 · 슬러리 시트 74 : 23 : 3 wt% · 대극 In–Li | 실험 (WIP 공정 변수 → 감압 뒤 싱크로트론 X 선 CT · 두께 · 단면 SEM / EDS · 충방전 · EIS) — 계산 없음 |

- **후보 표 · 가리킨 카드의 서지와의 대조**: 저자 · 제목 · 권 · 쪽 · 연도 · DOI **같다**.  덧붙임 ① 원문 인쇄 학술지 이름 = 영문 약칭 + 쪽 아래 *"Vol. 72 Supplement"* (증간호) ② DOI 접미사 **16C-SIS6-03** 은 발표 세션 번호 꼴 — 어떤 학회의 논문집인지는 원문에 인쇄되지 않았다 [미확인] ③ 접수 2024-06-28 · 수정 2024-09-19 · 채택 2024-09-23 (p.7) · 발행 "March, 2025" ④ PDF 문서 정보의 제목 = `jjspm72-Supplement-16C-SIS6-03`.  (근거 크롭: 머리 서지 = `txt_p1_header_title_authors_affiliations.png` · 날짜 = `txt_p7_references_rest_received_dates.png`)
- **글의 꼴**: Abstract → Introduction → Experiment (A. Sample Preparation · B. Structural Evaluation · C. Electrochemical Characterization) → Results (A. Structure of Composite Electrodes · B. Electrochemical Performance) → Discussion → Conclusions → Acknowledgments → References 16.  그림 9 · 표 0 · 식 0 (등가 회로 그림 하나).
- **맥락**: 저자 소속이 CIP / WIP 장치 제조사 — 같은 저자들의 앞선 보고가 ref. 14 (*SPring-8/SACLA Research Reports* 10 (2022) 471–477 · 일본어).  서론이 든 WIP 선행 = Lee 2020 (ref. 13 · *"over 900 Whl⁻¹ by using WIP"* [원문의 2 차 인용]) · Choi 2024 (ref. 15 — 정본 카드 있음).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 재료 · 조성 · 시편 (p.1 · p.2 · Fig. 6 · `txt_p1_sample_preparation.png` · `txt_p2_results_structure_ct_categories.png` · `fig_6.png`)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| CAM | Li(Ni₁/₃Mn₁/₃Co₁/₃)O₂ · **LiNbO₃ 코팅** (두께 · 방법 · 제조사 [미확인]) · 입경 숫자 없음 — *"which was very coarse after coating"* | [인쇄] p.1 · p.2 |
| SE | Li₆PS₅Cl (제조사 · 합성 [미확인]) · 입경 *"on the order of several microns, smaller than that for AM"* | [인쇄] p.1 · p.2 |
| 도전재 · 바인더 · 용매 | 아세틸렌 블랙 · *"a binder"* · *"a solvent"* (종류 · 양 [미확인]) | [인쇄] p.1 |
| 조성 | *"a slurry with an electrode composition of **74:23:3wt%**"* — 네 성분 (AM · SE · 탄소 · 바인더) 에 숫자 셋 → 무엇이 3 인지 (탄소 + 바인더 합인지 · 바인더는 따로인지) 원문에 없다 | [인쇄] p.1 |
| 전극 꼴 | 슬러리를 **Al 박 (집전체)** 에 도포 → 건조 (조건 [미확인]) → 두께 *"approximately 170 µm"* → 라미네이트 봉지에 진공 밀봉 → WIP | [인쇄] p.1 |
| SEM 에서 읽은 크기 (Fig. 6 · 눈금 10 µm = 75–77 px · 시야 ≈60 × 45 µm) | 밝은 (AM) 덩이의 단면 등가 지름 **2.5–8.9 µm · 중앙값 ≈6 µm** (a: 29 개 · c: 22 개) — 다결정 2 차 입자 (안쪽에 잔 기공) · 단면이라 실제 지름보다 작게 읽힌다 · 가압 전 SE = ≈1 µm 이하 알갱이 + 5–10 µm 덩어리 [판독 · 거칢] | [판독] `digitized.csv` fig6 |
| CT 범주 그림으로 본 AM : SE (가압 뒤 · 면적) | AM/(AM + SE) = 0.484 (RT) · 0.551 (100 °C) · 0.518 (150 °C) [판독 · 한 단면씩] | [판독] Fig. 2 |
| ↔ 무게비로 계산한 부피비 | 74 : 23 : 3 을 AM : SE : (탄소 + 바인더) 로 읽고 진밀도 NMC111 **4.653** · 카본 블랙 **1.834** g cm⁻³ [다른 카드: `ngandjong2021_dem_calendering_digital_twin` — Umicore NMC111 · C65 · 이 논문 재료와 같은 제품인지는 모름] 과 SE **1.64** (랩 표준) 를 넣으면 고체 부피 분율 AM 0.504 · SE 0.444 · 탄소 + 바인더 0.052 · AM/(AM + SE) = **0.531** · SE 에 1.87 [다른 카드: `schlautmann2023_se_particle_size_composite_transport` 표 S1 — 랩 표준과 다른 문헌 값] 을 넣으면 0.533 · 0.412 · 0.055 · **0.564** [카드 산술] — 판독 0.48–0.55 와 겹친다 (단면 산포 안 · 어느 밀도가 맞는지는 이 자료로 못 가린다) | [카드 산술] |
| 로딩 · 전극 밀도 · 지름 · 진밀도 | **[미확인]** — 그래서 질량 기준 기공을 만들 수 없다 | — |

### 3-2. ★ WIP 장치 · 조건 (p.2 · p.5 · `txt_p2_wip_apparatus_conditions.png`)
- 장치: *"a piston-type vertical CIP apparatus equipped with external sample heaters (Kobe Steel, Ltd.)"* · 용기 **⌀80 mm × 180 mm** [인쇄 p.2].
- 압력 **600 MPa** (고정) · 온도 **RT – 190 °C** (*"maximum temperature for the system"*) [인쇄 p.2].  Fig. 3 은 RT 를 25 °C 에 찍었다 [판독].
- 순서 [인쇄 p.2]: 용기 안 압력 매체를 가열 → 매체가 목표 온도에 닿으면 **대기압에서** 전극 장입 → 매체로 가압 → 공정 압력에서 유지 → 감압.  유지 시간 **1 min** (*"unless otherwise specified"*) · *"The process duration refers to the holding time at the maximum pressure"*.
- 시간 시리즈 (Fig. 8): **600 MPa · 100 °C** · 유지 **1 · 30 · 60 s** [인쇄 p.5 · 캡션].
- **[미확인]**: 압력 매체의 종류 · 승압 · 감압 속도 (승압에 걸린 시간이 1 s 유지보다 길 수 있다 [카드 해석]) · 시료가 매체 온도에 닿는 시간 · 190 °C 시료의 유지 시간 · 봉지 재질 · 조건별 시료 수.
- 상온의 "WIP" 는 사실상 CIP 다 (Fig. 1 의 화살표 글자도 *"CIP, WIP"*) [카드 해석].

### 3-3. ★ X 선 CT · 분류 · "void ratio" 의 정의 (p.2 · p.3 · `txt_p2_structural_evaluation_xct.png` · `txt_p3_void_ratio_thickness_resolution.png`)
- **촬영** [인쇄 p.2]: SPring-8 **SUNBEAM BL16B2** · 단색 **30 keV** · 회전 **180°** · **0.1°** 마다 · 노출 **4 s** · 검출기 Xsight Micron LC (Rigaku Innovative Technologies Europe) · **유효 화소 0.65 µm** · 시료 = **지름 0.8 mm 유리 모세관** 에 봉입 (Ar).  [카드 산술] 투영 ≈1 800 장 · 노출만 ≈2 h / 시료.
- **상태**: WIP 뒤 감압 → 전극에서 떼어 낸 조각을 모세관에 넣음 = **무하중 · ex situ** (가압 중 영상 아님).  모세관 지름 0.8 mm 안의 조각 크기 · 채취 위치 · 두께 방향 [미확인].
- **분류** [인쇄 p.2]: *"Based on the CT values separately determined for the various components (AM, SE and voids/carbon), each voxel was classified into three categories"* · *"Voids and carbon-related materials were not distinguished due to their high transparency to X-rays."*  문턱값 · 전처리 (필터) · 분석 부피 · 재구성 도구 [미확인].
- **정의** [인쇄 p.3 · Fig. 3 캡션]: void ratio = *"the ratio between the number of voxels for voids/carbon and those for all components"* → **(기공 + 탄소 복셀) ÷ 전체 복셀**.  ⚠ 토질역학의 간극비 e = V_v/V_s 가 아니고, 탄소 (와 아마 바인더) 가 들어 있는 **영상 갈래 분율**이다.
- **표시** [인쇄 p.2]: 재구성 단면은 대비를 뒤집어 (AM 이 가장 밝게 · SE · 탄소 · 기공 순으로 어둡게) SEM 과 견주기 쉽게 했다 · 범주 그림 = 초록 AM · 빨강 SE · 검정 기공 + 탄소.
- **표시 그림의 크기** [판독 · 카드 산술]: 눈금 막대 25 µm = 원 래스터 65–67 px → 0.379 µm / px · 한 패널 517 × 173 px = **≈196 × 66 µm** = CT 화소로 ≈301 × 101 개 (그림은 CT 화소를 ≈1.7 배 늘려 실었다).
- **저자의 해상도 한정** [인쇄 p.3]: *"the value of 0.04 means almost all voids were diminished within the resolution of the CT measurements, as the region contained both voids and carbon-related materials."*  → 0.04 는 "기공 4 %" 가 아니라 "이 해상도에서 남은 기공 + 탄소 갈래".  [카드 산술] 무게비로 본 탄소 + 바인더의 고체 부피 몫이 0.052–0.055 (§3-1) 로 같은 크기다 — 저자 말과 어긋나지 않는다 (단 화소보다 잘게 흩어진 탄소는 이 갈래에 안 잡힌다).

### 3-4. ★ 온도별 void ratio · 두께 — 600 MPa · 60 s (p.3 · Fig. 2 · Fig. 3 · `fig_3.png` · `fig_2.png` · `fig_2a–2d.png`)
| WIP 온도 | void ratio [판독 · 벡터] | 두께 (µm) [판독 · 벡터] | 본문 [인쇄 p.3] |
|---|---|---|---|
| 가압 전 | 0.1906 (Fig. 8 의 t = 0 표지) | 169.3 | *"as-fabricated value of 170 µm"* |
| RT (25 °C 에 찍힘) | **0.0568** | **102.97** | *"from approximately 104 µm …"* |
| 100 °C | **0.0419** | **97.46** | *"the void ratio decreased at 100°C"* |
| 150 °C | **0.0386** | **94.74** | *"… to 94 µm"* · *"a saturated trend at around 0.04 after the 150°C WIP treatment"* |

- 본문 정성 서술 [인쇄 p.2 · p.3]: 가압 뒤 (i) AM 영역 (초록) 이 늘고 (ii) SE 영역 (빨강) 이 줄고 (iii) SE 영역 안의 기공 · 탄소 (검정) 가 거의 사라진다 · *"The reduction of voids primarily occurred in the SE region"* · *"Generally, both void ratio and thickness of the composite electrodes decreased with increasing process temperature."*
- [카드 산술] 변화량: 가압 전 → RT **−0.134** (보이는 기공의 70 %) · RT → 150 °C **−0.018** · 두께 RT → 150 °C **−8.2 µm (−8.0 %)**.  ⇒ **치밀화의 대부분은 온도가 아니라 600 MPa 가 한다** (온도 몫은 보이는 기공 1.8 %p · 두께 8 %) — 원문 그림에서 바로 나오는 크기 감각.
- 표지 값과 본문의 차이: 본문 "≈104 µm" ↔ 표지 102.97 µm (1 µm) · "94" ↔ 94.74 — 반올림 수준.

### 3-5. ★ 유지 시간별 — 600 MPa · 100 °C (p.5 · Fig. 8 · Fig. 9 · `fig_8.png` · `fig_9.png` · `txt_p5_discussion_duration_two_step.png`)
| 유지 시간 | void ratio [판독 · 벡터] | 두께 (µm) [판독 · 벡터] |
|---|---|---|
| 가압 전 (*"Values before WIP"*) | **0.1906** | **169.3** |
| 1 s | **0.0873** | **94.54** (본문 *"95 µm"*) |
| 30 s | **0.0362** | **99.03** |
| 60 s | **0.0287** | **97.46** |

- 저자의 읽기 [인쇄 p.5]: *"The void ratio drastically decreased immediately after pressing for 1 s and then gradually decreased, suggesting a two-step process."* · *"The electrode densified instantly, and the distribution of AM after a WIP of 1 s was similar to that for the longer case"* · *"This indicates that densification was interrupted due to contact with each AM particle."* · *"However, at this stage, many voids remained in the SE because the contact of the AM particles resulted in releasing applied pressure in the surroundings. Then, due to isostatic pressing, the voids gradually diminished with the movements of the AM and the SE particles increased."*
- ★ **두께는 시간과 함께 줄지 않는다** — 94.5 (1 s) · 99.0 (30 s) · 97.5 (60 s): 저자 = *"consistent … within the variation of sample preparation"*.  그런데 보이는 기공은 1 s → 60 s 에 0.087 → 0.029 (−5.9 %p) 로 줄었다.  고체가 보존되고 면적이 같다면 기공 5.9 %p 는 두께 ≈5.5 µm 감소에 해당하는데 [카드 산술: 0.0587 × 94.5], 실제 두께는 +3–4.5 µm 다.  ⇒ (a) 시료 간 로딩 산포가 그만큼 크거나 (저자 말) (b) 큰 기공이 CT 해상도 아래의 잔 기공으로 나뉘어 "SE 갈래" 로 넘어갔거나 (c) 둘 다 — 원문 자료로는 가를 수 없다 [카드 해석].  **"두 단계" 의 둘째 단계가 전체 기공의 감소인지 기공 크기의 재분배인지는 열려 있다.**
- ⚠ **같은 조건 · 다른 값**: 600 MPa · 100 °C · 60 s 의 void ratio 가 Fig. 3 에서 **0.0419**, Fig. 8 에서 **0.0287** 이다 (차 0.013 = Fig. 8 값의 46 %) — 두께 표지는 두 그림에서 **97.46 µm 로 같다** (같은 시료의 두께를 두 그림에 쓴 것으로 읽힌다 [카드 해석]).  분석 영역 · 문턱 · 시료가 달랐는지 원문에 설명 없음 → 이 논문 void ratio 의 재현 폭은 **≈ ±0.007 이상**으로 봐야 한다 (온도 효과 RT → 150 °C 0.018 과 같은 자릿수).
- 1 s 시료의 범주 그림 (Fig. 9): AM 0.552 · SE 0.362 · 기공 + 탄소 **0.086** [판독] — Fig. 8 의 0.0873 과 같다 (표시 단면이 3D 값을 대표한다는 내부 점검).

### 3-6. ★ 범주 그림의 면적 분율 · 기둥 수지 — 영상 기공 ≠ 전체 기공 (Fig. 2 · Fig. 9 · `digitized.csv` fig2 · fig9)
**판독** (원 래스터 · 화소마다 가장 가까운 색 = 초록 / 빨강 / 검정 · 눈금 막대 글상자 제외 · **조건마다 표시된 2D 단면 한 장**):

| 시료 | AM (초록) | SE (빨강) | 기공 + 탄소 (검정) | ↔ 3D void ratio [판독] |
|---|---|---|---|---|
| 가압 전 (Fig. 2d) | 0.298 | 0.506 | **0.197** | 0.1906 |
| RT · 60 s (Fig. 2a) | 0.453 | 0.484 | **0.063** | 0.0568 |
| 100 °C · 1 s (Fig. 9) | 0.552 | 0.362 | **0.086** | 0.0873 |
| 100 °C · 60 s (Fig. 2b) | 0.525 | 0.427 | **0.048** | 0.0419 (Fig. 3) · 0.0287 (Fig. 8) |
| 150 °C · 60 s (Fig. 2c) | 0.497 | 0.463 | **0.041** | 0.0386 |

- 검정 분율이 인쇄 그림의 3D 값과 ±0.006 안에서 맞는다 (100 °C · 60 s 는 Fig. 3 쪽 값과) → 색 판독과 저자의 복셀 세기가 같은 것을 센다.
- **기둥 수지** [카드 산술 · 분율 × 두께 · µm · 가정: 단면 한 장의 면적비 = 부피비]:

| 시료 | 두께 t | AM 기둥 | SE 갈래 기둥 | 기공 + 탄소 기둥 | (1 − void)·t (3D 값) |
|---|---|---|---|---|---|
| 가압 전 | 169.3 | 50.4 | 85.6 | 33.3 | 137.0 |
| RT · 60 s | 103.0 | 46.7 | 49.8 | 6.5 | 97.1 |
| 100 °C · 1 s | 94.5 | 52.2 | 34.2 | 8.1 | 86.3 |
| 100 °C · 60 s | 97.5 | 51.2 | 41.7 | 4.6 | 93.4 (Fig. 8 값이면 94.7) |
| 150 °C · 60 s | 94.7 | 47.0 | 43.8 | 3.9 | 91.1 |

  1. **AM 기둥이 보존된다**: 49.5 ± 2.5 µm (n = 5 · 46.7–52.2) — AM 면적 분율이 0.30 → 0.45–0.55 로 느는 비 (1.5–1.9) 가 두께비 (1.64–1.79) 와 같다.  ⇒ 전극은 **면 방향으로 퍼지지 않고 두께만** 줄었고 (Al 박 위 시트 · 등방압이어도 운동학은 일축), AM 분류는 조건 사이에 일관된다.
  2. **"기공 아닌" 기둥 (1 − void)·t 는 보존되지 않는다**: 137 → 86–97 µm (−29 … −37 %).  고체가 사라질 수는 없으므로 가압 전의 "SE 갈래" 85.6 µm 가운데 절반쯤 (가압 뒤 34–50 µm) 만 고체였고 나머지는 **화소 0.65 µm 가 못 가른 잔 기공** (SE 알갱이 사이 · 탄소 · 바인더 포함) 이었다.
  3. **가압 전 전체 기공의 하한**: 가압 뒤 기공이 0 이상이므로 ε(가압 전) ≥ 1 − t(뒤)/t(전) = **0.39 (RT 시료 기준) – 0.44 (150 °C · 1 s 시료 기준)** [카드 산술 · 가정: 면적 · 고체 보존].  CT 가 본 것은 **0.19** — 절반도 안 된다.
  4. 온도 축도 마찬가지: 두께는 RT → 150 °C 에 8.0 % 줄었는데 (같은 로딩이라면 기공 ≈8 %p) 보이는 기공은 1.8 %p 만 줄었다 — 단 두께의 시료 산포 (± 2–3 µm ≈ ± 3 %) 가 섞여 있다.
- ⇒ **이 논문의 void ratio 는 "화소보다 큰 기공 + 탄소" 의 분율이고, 전체 기공률로 읽으면 가압 전 상태를 절반 이하로, 가압 효과 (−13 %p) 를 실제 (두께로는 −39 … −44 %) 의 1/3 로 줄여 읽게 된다.**  (같은 교훈의 다른 재료 실례 = `cottrino2013_insitu_xct_granulated_alumina_die_compaction` [다른 카드].)

### 3-7. 카드 어림 — 가압 뒤 전체 기공 (⛔ 원문 값이 아니다 · 인용 금지)
- AM 기둥 49.5 µm 와 무게비 (§3-1 의 가정) 로 "기공 없는 두께" 를 만들면: SE 1.64 (랩 표준) → **98.2 µm** · SE 1.87 (랩 표준과 다른 문헌 값) → **92.9 µm** [카드 산술 · 고체 진밀도 3.17 · 3.35 g cm⁻³].
- 잰 두께 (94.5–103.0 µm) 와 견주면 전체 기공 = RT **4.7 % (1.64) · 9.8 % (1.87)** · 100 °C 60 s **−0.8 · 4.7 %** · 150 °C **−3.7 · 1.9 %** [카드 산술].  음수는 AM 기둥의 불확도 (± 5 % = ± 5 %p) 안이다.
- 쓸 수 있는 말은 여기까지: *"600 MPa 등방 · 상온 · 감압 뒤의 전체 기공은 한 자릿수 % 수준, 150 °C 에서는 그보다 수 %p 낮다 — 단 이 카드의 어림이고 불확도가 값과 같은 크기다."*  로딩 · 진밀도가 인쇄되지 않아 닫을 수 없다.

### 3-8. 단면 SEM · Mn EDS (p.5 · Fig. 6 · Fig. 7 · `fig_6a–6c.png` · `fig_7a–7b.png` · `txt_p5_discussion_sem_eds_softening.png`)
- 시편: cryo-FIB 로 낸 단면 (*"to avoid damage to the samples during preparation"*) [인쇄 p.2] · 본문은 *"cross-sectional secondary electron microscopy (SEM)"* 로 인쇄.
- **Fig. 6** (눈금 10 µm · 시야 ≈60 × 45 µm [판독]): (a) RT WIP · (b) **190 °C** WIP · (c) 가압 전.
  - 저자 [인쇄 p.5]: RT = 치밀해졌으나 *"most AM and SE particles remained isolated, with boundaries between adjacent AM similarly observed"* · 190 °C = *"unclear boundaries and notable particle coalescence. In particular, the SE particles coalesced to form large particles without boundaries"* · *"The surface features after RT WIP treatment were similar to those obtained from the cross-section before WIP, suggesting that the high-temperature WIP enhanced the coalescence of both the AM and SE."*
  - 그림에서 보이는 것 [판독 · 카드 해석 — 원문에 색 설명 없음]: 밝은 회색 = AM 2 차 입자 (둥근 덩이 · 안쪽 잔 기공 · 뚜렷한 균열은 이 세 시야에서 안 보임) · 중간 회색 = SE · 검정 = 빈 곳.  (c) 는 AM 사이에 ≈1 µm 이하 SE 알갱이와 큰 빈 곳 · (a) 는 SE 조각 사이 경계선이 촘촘히 남음 · (b) 는 20–30 µm 폭의 매끈한 SE 영역 (안에 금 같은 선) 과 함께 왼쪽 AM 무리 둘레에 검은 틈이 남아 있다.
  - 회색값 분율 [판독 · 문턱 = 패널 히스토그램의 골 · 한 시야 · 거칢]: 밝은 (AM) 분율 가압 전 0.36 → RT 0.49 · 190 °C 0.46 · 어두운 (회색값 < 64) 분율 가압 전 **0.38** → RT 0.12 · 190 °C 0.09.  SEM (≈0.13 µm / px) 은 가압 전 빈 곳을 CT (0.19) 의 두 배쯤 본다 — §3-6 의 두께 하한 (≥ 0.39–0.44) 쪽 [단면 SEM 의 어두운 부분에는 그늘 · 깊이 효과가 섞인다].
- **Fig. 7** (Mn K 지도 · 눈금 50 µm = 99 px · 두 패널 같은 배율 [판독]): (a) RT · (b) 190 °C.  저자 [인쇄 p.5]: *"The EDS results shown in Fig. 7 reveal that AM were replaced after the high-temperature WIP treatment. This implies a softening of the SE, resulting in increased fluidity and enhanced movement of particles during WIP."* ("replaced" = 자리가 바뀌었다는 뜻으로 읽힘 [카드 해석] · 정량 없음.)
  - Mn 띠 높이 [판독 · 줄별 Mn 화소 밀도의 반값 경계]: (b) 190 °C **≈102 µm** (위 · 아래 경계가 다 화면 안) · (a) RT **≥ 121 µm** (띠가 화면 위로 나감 — 하한).  ⚠ Fig. 3 의 RT 두께 103 µm 와 맞지 않는다 (단면의 기울기 · 기울기 보정 · 시료 대응 [미확인]) → 이 띠 높이를 두께 자료로 쓰지 않는다.
- 190 °C 시료의 void ratio · 두께 · 전지 자료는 없다 (Fig. 3 의 온도 축은 150 °C 까지).

### 3-9. 전기화학 (p.2 · p.4 · Fig. 1 · 4 · 5 · `fig_1.png` · `fig_4.png` · `fig_5a.png` · `fig_5b.png` · `fig_5a_equivalent_circuit.png` · `txt_p2_electrochemical_characterization.png` · `txt_p4_charge_discharge_eis.png`)
- **셀** [인쇄 p.2 · Fig. 1]: *"hybrid structure"* = WIP 한 (또는 안 한) 복합 전극 시트 + **펠릿 SE** (Li₆PS₅Cl · **단축 600 MPa** 성형 · 두께 **600 µm**) + **In–Li 합금** 대극 · 유효 면적 **≈1 cm²** · 측정 중 **구속압 150 MPa** (*"to maintain contact between the components"*).  전극 지름 · 측정 온도 [미확인].
- **충방전** [인쇄 p.2]: **0.1 C** · 방전 CC · 충전 CC + CV (**3.68 V · 1 h**) · 방전 차단 **2.48 V** · **3 사이클**.  전압은 In–Li 대극 기준의 셀 전압 (Li/Li⁺ 환산은 원문에 없다).  1C 의 전류 · 용량의 질량 기준 [미확인].
- **Fig. 4** (0.1C 곡선 · 검정 RT · 빨강 100 °C · 파랑 150 °C · 몇 번째 사이클인지 [미확인]):

| | RT | 100 °C | 150 °C | 표지 |
|---|---|---|---|---|
| 방전 용량 (mAh g⁻¹) | ≈110 | ≈125 | ≈128 | [인쇄] p.4 |
| 방전 끝 (2.48 V) | 109.7 | 126.1 | 129.2 | [판독] |
| CC 충전 끝 (3.68 V 도달) | 146.9 | 159.8 | 164.6 | [판독] |
| 충전 끝 (CV 1 h 뒤) | 157.9 | 163.9 | 173.1 | [판독] |
| 방전 ÷ 충전 | 0.695 | 0.769 | 0.747 | [카드 산술] |
| 충전 가지 전압 @ 60 · 80 · 100 mAh g⁻¹ (V) | 3.306 · 3.356 · 3.425 | 3.263 · 3.302 · 3.358 | 3.237 · 3.276 · 3.332 | [판독] |
| 방전 가지 전압 @ 60 · 80 · 100 mAh g⁻¹ (V) | 3.076 · 2.997 · 2.820 | 3.134 · 3.062 · 2.981 | 3.157 · 3.084 · 3.011 | [판독] |

  - 판독 점검: CV 평탄 3.681–3.683 V · 방전 끝 2.483 V = 인쇄된 3.68 · 2.48 V 재현.
  - 본문 [인쇄 p.4]: *"The overpotential for the 150°C cell was about 0.1 V lower than that for RT"* ↔ [판독] 충전 가지 RT − 150 °C = 0.069 · 0.080 · 0.093 V (60 · 80 · 100 mAh g⁻¹) · 방전 가지 0.081 · 0.087 · 0.191 V ✓.  *"the change was significant between the RT and the 100°C treatments and relatively minor between 100 and the 150°C cells"* · *"The change suggests that charge-discharge performance correlates well with the reduction of voids in the SE"*.
  - 캡션 · 본문 모두 *"(a) RT, (b) 100°C, and (b) 150°C"* — "(b)" 가 두 번이고 그림에는 패널 글자가 없다.
- **EIS** [인쇄 p.2 · p.4]: **3.3 V** (충전 중 셀 전압이 3.3 V 가 된 뒤) · 진폭 **10 mV** · **0.01 Hz – 7 MHz**.  등가 회로 (Fig. 5a 안) = **R1 – (R2 ∥ CPE1) – (R3 ∥ CPE2)** · **맞춤값 미인쇄**.
  - 저자 [인쇄 p.4]: Nyquist = 원점에서 크게 떨어진 대칭 호 + 일정한 기울기의 증가 · *"The arc is attributed to the resistance related to charge-transfer¹⁶⁾"* · *"the resistance between the interfaces decreased with increasing WIP temperature, while the Li-ion intercalation remained virtually unchanged"* · 원점 오프셋 **(~ 20 Ω)** = *"bulk (Ohmic) resistance at the interface between the composite electrodes and the pellet-shaped SE and should be excluded from the present analysis"* · Bode 에서 *"changes in R2 are dominant"*.
  - **판독** (원 래스터 · 축 = 그림 틀 / 눈금):

| | RT | 100 °C | 150 °C |
|---|---|---|---|
| 호의 왼쪽 끝 Z′ (Ω) | (다른 두 곡선에 가려짐 — 20 으로 둠) | 19.2 | 21.4 |
| 호 꼭대기 Z′ · −Z″ (Ω) | 77.6 · 38.0 | 56.9 · 23.2 | 53.2 · 18.2 |
| 호 뒤 골 Z′ (Ω) | 143.3 | 93.8 | 85.7 |
| **호 폭** (Ω) [카드 산술] | **≈123** | **≈75** | **≈64** |
| 저주파 끝 (0.01 Hz) Z′ · −Z″ (Ω) | 250.5 · 36.1 | 176.6 · 26.2 | 148.5 · 19.4 |
| 꼬리의 실수부 길이 (Ω) [카드 산술] | 107 | 83 | 63 |
| 임피던스 크기 @ 0.01 Hz (Ω) | 252 | 177 | 148 |
| 임피던스 크기 @ 100 Hz (Ω) | 142 | 94 | 85 |
| 위상 봉우리 (° @ Hz) | −29.3 @ ≈1.5 × 10⁴ | −25.0 @ ≈1.3 × 10⁴ | −19.8 @ ≈1.4 × 10⁴ |

  - 내부 점검: Bode 의 100 Hz 값 (142 · 94 · 85) = Nyquist 골의 Z′ (143 · 94 · 86) · 0.01 Hz 크기 = Nyquist 끝점의 √(Z′² + Z″²) (253 · 179 · 150) ✓.
  - [카드 산술] 호 폭의 비 RT : 100 : 150 °C = 1 : 0.61 : 0.52 · 용량비 1 : 1.15 : 1.18 · 보이는 기공 0.057 : 0.042 : 0.039 — 셋 다 RT → 100 °C 에서 크게, 100 → 150 °C 에서 조금 움직인다 (3 점 · 시료 하나씩).
  - [카드 산술] 위상 봉우리 주파수가 세 시료에서 같다 (1.3–1.5 × 10⁴ Hz).  이상적인 R1 – (R2 ∥ C) 로 보면 호 꼭대기 주파수 f₀ = f_peak ÷ √((R1 + R2)/R1) ≈ 5.5 · 5.8 · 6.7 kHz → C = 1/(2π f₀ R2) ≈ **2.3 · 3.7 · 3.7 × 10⁻⁷ F** (셀 ≈1 cm²) · 시간 상수 ≈ (2.4–2.9) × 10⁻⁵ s 로 거의 같다 — **R 은 줄고 C 는 늘어 곱이 그대로** = 계면의 성질이 아니라 **유효 면적 (닿은 면적) 이 늘어난 꼴**이다 [카드 해석 · CPE 지수 미상 · 어림].  원문은 이 호를 인용 하나로 전하이동에 귀속했고 대칭 셀 · 온도 · SOC 의존 같은 분리 시험은 없다.
  - [판독] 저주파 꼬리의 실수부 길이도 107 → 83 → 63 Ω 로 준다 — 본문의 *"Li-ion intercalation remained virtually unchanged"* 는 꼬리의 모양 (기울기) 을 가리키는 것으로 읽힌다 [카드 해석].
  - [카드 산술 · 가정] 오프셋 20 Ω 이 전부 분리막 펠릿의 벌크 저항이라면 600 µm ÷ (σ × 1 cm²) = 20 Ω → σ ≈ **3.0 mS cm⁻¹** — 원문은 SE 의 전도도를 인쇄하지 않았고 오프셋을 "전극–펠릿 계면의 벌크 저항" 이라고만 적었다 (어림 · 인용 금지).

### 3-10. ★ 저자가 적은 한계 · 원문 안 어긋남
**저자 한계 (원문)**: ① WIP 의 치밀화 기전과 공정 압력 · 온도의 영향은 *"still an open question"* (p.1 — 이 논문은 그 가운데 온도 · 시간만 봤다) ② 0.04 는 CT 해상도 안의 값 · 기공과 탄소를 못 가른다 (p.2 · p.3) ③ 두께는 *"within the variation of sample preparation"* 만큼 흔들린다 (p.5) ④ 기전을 확인하려면 *"the mechanical properties of the SE should be clarified"* — 다음 일 (p.5).
**원문 안 어긋남 (카드가 본 것 — 고치지 않고 적는다)**:
1. 같은 조건 (600 MPa · 100 °C · 60 s) 의 void ratio: Fig. 3 **0.042** ↔ Fig. 8 **0.029** (두께 표지는 같다) [판독].
2. 본문 "≈104 µm" (RT) ↔ 표지 102.97 µm [판독].
3. Fig. 7(a) RT 의 Mn 띠 ≥ 121 µm ↔ Fig. 3 RT 두께 103 µm [판독].
4. Fig. 4 캡션 · 본문 "(b)" 두 번 · 그림에 패널 글자 없음.
5. p.2 *"The working electrode was a composite electrode with and without WIP treatment"* ↔ WIP 안 한 전극의 전지 자료는 실리지 않았다.
6. 190 °C 시료는 SEM · EDS 에만 (void ratio · 두께 · 전지 없음) — "고온 WIP 가 전기화학을 개선한다" 는 문장의 전지 자료는 150 °C 까지다.
7. 결론 *"implying a correction with the void ratio"* (correlation) · p.2 *"SEM images shown blow"* · *"secondary electron microscopy (SEM)"* · p.4 *"The frequency at the apex of the semicircle corresponds to the resistance"*.
8. 본문 *"Li-ion intercalation remained virtually unchanged"* ↔ 저주파 꼬리의 실수부 길이는 107 → 63 Ω 로 준다 [판독].
9. 조성 74 : 23 : 3 — 네 성분에 숫자 셋.
10. 서론의 *"high pressure (~600 MPa) CIP at elevated temperatures"* 는 WIP 일반의 압력처럼 적혀 있다 — 정본의 다른 WIP 카드는 400–500 MPa · 80–85 °C 를 쓴다 [다른 카드: `benhadjali2026_…` · `interfacial_impedance_formulation_assb_cathode` · `jun2026_ppma_econductive_binder_si_lowpressure_assb`].

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 사슬
- **시편**: 슬러리 (AM + SE + 아세틸렌 블랙 + 바인더 + 용매) → Al 박 도포 · 건조 (≈170 µm) → 라미네이트 봉지 진공 밀봉 → WIP (600 MPa · 상온–190 °C · 1 s–1 min) → 감압 · 개봉.
- **구조**: (i) 조각을 ⌀0.8 mm 유리 모세관 (Ar) 에 넣어 싱크로트론 CT (화소 0.65 µm) → 세 갈래 복셀 분류 → void ratio (ii) 두께 (재는 법 미기재) (iii) cryo-FIB 단면 → SEM · Mn EDS.
- **전지**: WIP 한 시트를 단축 600 MPa 로 따로 만든 600 µm Li₆PS₅Cl 펠릿 + In–Li 와 겹쳐 150 MPa 구속 → 0.1C 3 사이클 · 3.3 V EIS.
- **세 측정이 같은 시료인지** (CT 조각 · 단면 · 전지 전극) 는 적혀 있지 않다.  구조는 무하중, 전지는 150 MPa 구속 — 상태가 다르다.

### 4-2. 계산 · 모델
**없음.**  식 · 표 · 수치 모사 · 접촉 법칙 · 격자 · 입자 수 · 맞춤 변수 — 해당 없음.  유일한 "모델" 은 Fig. 5(a) 의 등가 회로 R1 – (R2 ∥ CPE1) – (R3 ∥ CPE2) 이고 맞춤값도 인쇄되지 않았다.

### 4-3. 입자 처리 ★
- 실험이라 입자 가정이 없다.  영상 쪽에서 입자는 **복셀 갈래 (AM · SE · 기공 + 탄소)** 로만 다뤄진다 — SE 입자 하나하나는 화소 0.65 µm 로 풀리지 않고 ("수 µm" 입자 = 지름당 화소 몇 개), SE 갈래는 SE + 그 사이 잔 기공 + (아마) 바인더 · 잘게 흩어진 탄소의 묶음이다 (§3-6).
- 입자 형상 변화는 **SEM 사진의 정성 서술**뿐: 상온 600 MPa 에서는 SE 입자 경계가 남고, 190 °C 에서는 합쳐져 경계가 없어진다 (p.5).  변형량 · 접촉 면적 · 피복률 수치 없음.

### 4-4. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **말 없음** (본문에 DEM · simulation · model 낱말 0 회 · 계산이 아예 없다 — 등가 회로 그림 하나뿐).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — 계산이 없으므로 해당 없음.  실험 쪽 서술만: 고온에서 *"a softening of the SE, resulting in increased fluidity and enhanced movement of particles during WIP"* (p.5 · 추론) · 서론이 인용한 Sakuda 2013 의 유리 SE 상온 가압 (상대밀도 > 90 % @ > 350 MPa) 과 200 °C 열간 가압 (유리 전이 근처) (p.1 · `txt_p1_intro_sakuda_density_wip_open_question.png`) · *"the mechanical properties of the SE should be clarified"* (p.5).  SE 의 항복 · 크리프 · 온도 의존 물성 값은 없다.
3. **2D / 3D** — CT 는 3D (복셀 수로 void ratio) · 실은 그림은 2D 단면 · SEM · EDS 는 2D 단면.  2D → 3D 전이에 대한 말 **없음**.  [판독] 표시 단면의 2D 검정 분율이 3D 값과 ±0.006 안에서 같다 (§3-6).
4. **압력을 뺄 때의 거동** — **다루지 않았다**: 모든 구조 값이 감압 뒤 한 상태 · 가압 중 값이 없어 되돌아온 양을 알 수 없다 · 감압 속도 [미확인].  전지는 150 MPa 로 다시 구속해 쟀다.

### 4-5. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| WIP (warm isostatic pressing) | 가열한 압력 매체로 사방에서 누르는 가압 — 여기선 CIP 장치 + 외부 히터 · 600 MPa · ≤ 190 °C · 시료는 진공 봉지 안 |
| CIP · HIP | 상온 · 고온 등방 가압 — 이 논문의 "RT WIP" 는 CIP 와 같다 |
| process duration | 최대 압력에서의 유지 시간 (승압 · 감압 시간 제외) |
| void ratio (이 논문) | (기공 + 탄소로 분류된 복셀) ÷ (전체 복셀) — 영상 갈래 분율 · 토질역학의 간극비 e 아님 · 전체 기공률 아님 |
| categorized composition image | CT 값 문턱으로 복셀을 AM (초록) · SE (빨강) · 기공 + 탄소 (검정) 로 칠한 단면 |
| effective pixel size | 검출기 화소를 시료 위로 환산한 크기 (0.65 µm) — 분해능은 이보다 나쁘다 (보통 화소의 2–3 배 [카드 해석]) |
| hybrid test cell | 시트 전극 + 따로 누른 펠릿 SE + In–Li 를 겹쳐 구속압 (150 MPa) 으로 붙인 평가 셀 |
| confining pressure | 측정 중 셀에 거는 압력 (150 MPa) — 성형압 (600 MPa) 과 다른 것 |
| R1 · R2 · R3 | 등가 회로의 직렬 저항 (원점 오프셋 ≈20 Ω) · 고주파 호 (저자: 전하이동 관련) · 저주파 요소 (저자: Li 삽입 쪽) |
| cryo-FIB | 얼린 상태에서 집속 이온 빔으로 단면을 내는 법 (황화물 손상을 줄이려고) |

---

## 5. Figure set ★
| 그림 | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| **Fig. 1** (`fig_1.png`) | 시험 셀 도식 — 집전체 위 복합 전극 ("CIP, WIP") · SE 펠릿 · In–Li · 위아래 구속압 150 MPa | 시트 전극 + 펠릿 SE "hybrid" 셀의 꼴 — 전극만의 효과를 보려는 배치 (전극–펠릿 접촉이 직렬로 낀다) |
| **Fig. 2** (`fig_2.png` · 패널 `fig_2a` · `2b` · `2c` · `2d`) | 재구성 CT 단면 (위 · 대비 반전) + 범주 그림 (아래) — (a) RT (b) 100 °C (c) 150 °C (d) 가압 전 · 눈금 25 µm | ★ 범주 그림의 면적 분율 [판독] (§3-6) — AM 기둥 보존 · SE 갈래 축소 = **영상 기공 ≠ 전체 기공** 의 실례 · 우리 DEM 단면과 나란히 보기 (값 대조 아님) |
| **Fig. 3** (`fig_3.png`) | void ratio (왼축 0–0.06) · 두께 (오른축 90–110 µm) vs WIP 온도 (0–200 °C) — 표지 3 + 3 (RT · 100 · 150 °C) | ★ 온도별 값 [판독 · 벡터] — 방향 항목 (결과 전 대조) · 압력 축이 아님을 명시 |
| **Fig. 4** (`fig_4.png`) | 0.1C 충방전 곡선 (전압 2.2–4.0 V · 용량 0–180 mAh g⁻¹) — RT · 100 · 150 °C | 과전압 · 용량의 온도 방향 (흐름 밖 · 전지) |
| **Fig. 5** (`fig_5.png` · `fig_5a` · `fig_5b` · `fig_5a_equivalent_circuit`) | (a) Nyquist (0–300 Ω) + 등가 회로 · (b) Bode (크기 · 위상) | ★ 호 폭 ≈123 → 75 → 64 Ω [판독] · 봉우리 주파수 불변 → 면적 효과 꼴 [카드 해석] — Rint ② 의 정성 짝 |
| **Fig. 6** (`fig_6.png` · `fig_6a` · `6b` · `6c`) | 단면 SEM — (a) RT WIP (b) 190 °C WIP (c) 가압 전 · 눈금 10 µm | ★ **상온 600 MPa 에서도 SE 입자 경계가 남는다** (조건 R3 · R6 의 사진 근거 · 정성 · 한 시야) · 190 °C 에서 합체 |
| **Fig. 7** (`fig_7.png` · `fig_7a` · `7b`) | Mn K EDS 지도 — (a) RT (b) 190 °C · 눈금 50 µm | AM 분포 (자리 옮김의 정성 근거) · 띠 높이는 두께 자료로 쓰지 않음 (§3-8) |
| **Fig. 8** (`fig_8.png` · 다시 자름) | void ratio (0–0.25) · 두께 (0–180 µm) vs 유지 시간 (0–80 s) @600 MPa · 100 °C · "Values before WIP" | ★ **두께는 1 s 에 끝 · 보이는 기공은 60 s 까지** [판독 · 벡터] — 시간 의존 (우리 모델에 없는 축) |
| **Fig. 9** (`fig_9.png` · 다시 자름) | WIP 1 s 시료의 CT 단면 + 범주 그림 | 1 s 에 AM 배치는 이미 최종 꼴 · 기공 + 탄소 0.086 [판독] |
| 근거 문단 15 (`txt_p*`) | 머리 서지 · 초록 · 서론 · 시편 · WIP · CT · 전지 · 결과 · 고찰 · 결론 · 참고문헌 | 보고서 붙임 · 인용 근거 |

## 6. Post-processing ★
- **void ratio**: CT 값 문턱으로 세 갈래 분류 → 복셀 수의 비 (진밀도 불필요 · 탄소 포함 · 화소 0.65 µm) — 분석 부피 · 문턱 · 필터 [미확인].
- **두께**: 재는 법 [미확인] (집전체 포함 여부도) · 조건마다 값 하나.
- **SEM · EDS**: 정성 (경계 · 합체 · Mn 분포) — 정량 지표 없음.
- **충방전**: 0.1C 곡선 겹쳐 그리기 · 용량 · 과전압 (읽는 위치 미기재).
- **EIS**: Nyquist · Bode 겹쳐 그리기 · 등가 회로 제시 (맞춤값 없음) · 호의 귀속은 인용.
- **판독 (이 카드)**: 벡터 그림 2 장은 그리기 객체에서 · 래스터 그림은 원 래스터에서 색 / 회색값 분류 — `digitized.csv` 의 note 열에 방법 전부.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **가압 방식 · 측정 상태 · 연산자 · 재료 꼴이 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| 가압 | **등방 600 MPa** · 봉지 · 상온–190 °C · 1 s–1 min · 감압 뒤 측정 | **일축 300 MPa** · 단단한 판 · 옆면 주기 · 상온 · DEM = 변위 정지 뒤 판 고정 [우리] | 경계 · 압력 · 온도 · 상태가 다 다르다 — 단 변형은 둘 다 두께 방향 (§3-6) |
| 복합 양극 기공 | CT 기공 + 탄소 갈래 **0.057** (RT) · 0.042 · 0.039 · 화소 0.65 µm · 무하중 | real_14 DEM ε_sphere **15.6 %** (300 MPa · 판 고정 · 구 부피 합) · 랩 표준 순수 SE 10–13 % (300 MPa · 진밀도 1.64) [우리 · CLAUDE.md] | **다른 양** — 영상 갈래 분율 ↔ 구 부피 합 ↔ 질량 / 진밀도.  0.057 을 "600 MPa 기공 5.7 %" 로 우리 값 옆에 놓지 않는다 |
| 가압 전 상태 | 도포 · 건조 시트 · CT 0.19 · 두께 하한으로 ε ≥ 0.39–0.44 [카드 산술] | DEM 삽입 · 정착 침대 (느슨한 분말) [우리] | 출발 상태가 다르다 (바인더 든 시트 ↔ 분말) — 두께 변화율 (−39 … −44 %) 은 견주지 않는다 |
| AM 부피 분율 | 가압 뒤 AM 면적 분율 0.45–0.55 [판독] (74 wt% NCM111) | 우리 코퍼스 φ_AM 0.37–0.88 [우리 · CLAUDE.md σ_e 유효 범위] | 범위 안 — 조성 자리만 겹친다 |
| AM 하중 분담 | 저자 서술: AM 끼리 닿으면 *"releasing applied pressure in the surroundings"* → SE 쪽 기공이 남는다 (추론 · 측정 없음) | DEM 접촉 비리얼의 AM 몫: AM–AM 규약 0.52–0.68 · 상 규약 0.73–0.79 (100–600 MPa) [우리 · CLAUDE.md] · MPM 은 AM 을 얼려 SE 가 100 % 를 진다 → 정직하게 누르면 ε_sphere 1.1 % 로 과압축 [우리] | **방향 같음** — 우리 "AM 하중분담 ②" 가 유일한 병목이라는 진단의 실험 쪽 서술 짝 (정성) |
| SE 입자 경계 | 상온 600 MPa 뒤에도 SEM 에서 경계가 보인다 · 190 °C 에서 사라진다 (정성 · 한 시야) | DEM = 구가 영원히 남음 (경계 항상) · MPM 한 속도장 = 경계 없음 · 복셀 FV = SE–SE 계면 저항 항 0 (CONTACT_FREE 가지) · Rint ② = 계면 항 추가 중 [우리 · CLAUDE.md CL-81] | 상온 가압체에는 SE–SE 경계가 실재한다는 사진 근거 — "경계 없는 연속체" 쪽이 상한이라는 우리 표기와 같은 방향 |
| 시간 의존 | 두께 1 s 에 완료 · 보이는 기공 0.087 → 0.029 (60 s) @100 °C | DEM = 준정적 서보 · MPM = 속도 무관 J2 (재하율 효과는 관성 +4.8 % 뿐) [우리 · CLAUDE.md] | **우리에게 없는 축** (크리프 · 점소성 · 온도) — 맞추지 않는다 · 한정어로 적는다 |
| 온도 | 상온 → 150 °C: 보이는 기공 −1.8 %p · 두께 −8 % · 190 °C: SE 합체 | 상온 물성 하나 [우리] | 우리 범위 밖 |
| 계면 저항 | EIS 호 폭 ≈123 → 75 → 64 Ω (≈1 cm²) [판독] · 봉우리 주파수 불변 | 접촉망 σ (Holm 협착) · STEP4 BV 반응 · Rint ② [우리] | 정의가 다르다 (셀 임피던스의 호 ↔ 유효 전도도) — 방향 (닿은 면적 ↑ → 저항 ↓) 만 |
| SE 이온 σ₀ | 인쇄 없음 · 오프셋 20 Ω ↔ 600 µm 펠릿이면 3.0 mS cm⁻¹ [카드 산술 · 가정] | 보고 기준 1.5 · 풀이기 상수 3.0 mS cm⁻¹ [우리 · CLAUDE.md] | 어림일 뿐 — 근거로 쓰지 않는다 |
| tortuosity · σ_ion · σ_e · 피복 | **없음** | 접촉망 · 복셀 σ · tau2 · 피복 [우리] | 견줄 것 없음 |

### 7-2. ★ void ratio 0.057 · 0.04 를 우리 계획에 들일 때
- 쓸 수 있는 것: **600 MPa 등방 · 상온에서 화소 0.65 µm 로 보이는 기공 + 탄소가 ≈6 % · 온도를 150 °C 로 올리면 ≈4 % (탄소 몫과 같은 크기) 로 준다**는 방향 · 크기 감각.
- 붙여야 할 꼬리표: 감압 뒤 · 영상 갈래 분율 (탄소 포함) · 화소 0.65 µm · 시료 하나 · 재현 폭 ≥ ±0.007 · 등방 · 바인더 시트.
- 쓰지 말 것: 우리 ε_sphere (15.6 %) · 랩 표준 (10–13 %) 과의 차이를 "압력 300 → 600 MPa 의 효과" 나 "모델 오차" 로 읽는 것 — 연산자가 다르다 (§3-6: 이 연산자는 가압 전 기공을 절반 이하로 읽는다).

### 7-3. ★ "두 단계" ↔ 우리 모델
- 저자의 첫 단계 (순간 치밀화 → AM 접촉에서 멈춤) = 우리 DEM 이 그리는 그림 (AM 골격이 하중을 받고 SE 는 가려진다 · AM-shielding [우리 · CLAUDE.md]) 과 같다.
- 둘째 단계 (같은 두께에서 기공이 시간에 따라 줄어듦) 는 **재료의 시간 의존 유동**이고 우리 DEM (탄성-이력 접촉) · MPM (속도 무관 J2) 어디에도 없다.  우리 MPM 의 "재하율 효과" (느린 판 → 정착 응력 +4.8–9 % [우리]) 는 관성이지 크리프가 아니다 — 같은 말로 묶지 않는다.
- ⚠ 둘째 단계가 전체 기공의 감소인지 기공 크기의 재분배인지 원문이 가르지 못한다 (§3-5) → 우리 쪽에서 "유지 시간이 길면 기공이 준다" 를 사실로 쓰려면 두께 + 질량이 같이 있는 다른 자료가 필요하다.

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **실험 (공정 변수 → 무하중 영상 구조 · 두께 · 전지)**.  우리 분업으로는 DEM 쪽 (기공 · AM 골격 · 하중 가림) 의 **정성 짝**과 MPM 쪽 (SE 형상 변형 · 합체) 의 **사진 짝**이다.
- 없는 반쪽: 압력 축 · 가압 중 상태 · 탈압 · 응력 · 물성 · 수송 지표 · 어떤 계산.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = LiNbO₃ 코팅 NCM111 + Li₆PS₅Cl + 아세틸렌 블랙 + 바인더의 **슬러리 시트** · **등방 600 MPa** · 상온–190 °C — 계는 가깝지만 **가압 방식 · 압력 · 온도 · 시편 꼴 · 기공 연산자가 다르다**.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ 반면교사 넷 — ① **영상 갈래 분율 ≠ 전체 기공**: 가압 전 CT 0.19 ↔ 두께 하한 ≥ 0.39–0.44 [카드 산술] · (1 − void)·t 가 137 → 86–97 µm 로 안 보존 → 영상 기공을 받을 때 **기둥 보존 검사** (분율 × 두께) 를 먼저 ② **갈래에 탄소가 섞인다** (기공 + 탄소 · 바닥 0.04 ≈ 탄소 부피 몫) → 우리 복셀 지표를 CT 와 견줄 때 탄소 · 바인더 상을 기공과 **합친 갈래**로 다시 세야 같은 양이 된다 ③ **같은 조건 두 값** (0.042 ↔ 0.029) → 재현 폭을 모르는 영상 값은 방향으로만 ④ 이름 함정 "void ratio" (간극비 아님) | 질량 · 진밀도 기공 · 압력 곡선 · 순수 SE 값 — 랩 표준 (10–13 % · 1.64) 과 나란히 놓을 숫자 **없음** |
| **단계 1** (3D 메모리 · 장 수) | 크기 감각만: CT 표시 영역 ≈196 × 66 µm (≈301 × 101 화소) · 전극 두께 95–103 µm · AM 단면 지름 5–9 µm [판독] | 입자별 장 · 메모리 숫자 없음 |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 없음 (순수 SE 기공 · 항복 없음 — 분리막 펠릿은 "단축 600 MPa" 한 줄뿐 · 밀도 미기재).  정성: 온도 ↑ → SE 합체 (190 °C) · 저자도 SE 물성이 필요하다고 적음 | 맞춤 표적 아님 · 우리 상온 σ_y 를 이 논문의 고온 거동과 견주지 않는다 |
| **단계 5** (3D 복합 압밀) | ★ **결과 전 대조 항목 (방향 · 정성)**: ① 복합 (AM ≈50 vol%) 을 누르면 **변형은 순간에 AM 골격에서 멈추고** 그 뒤 기공은 SE 영역 안에서 준다 (p.5 · Fig. 8 · 9) ② 가압 뒤 AM 분율 0.45–0.55 · 기공은 SE 영역에 남는다 (Fig. 2) ③ 상온 600 MPa 등방 뒤 보이는 기공 + 탄소 ≈6 % ④ 범주 그림 3 갈래의 기둥 수지 (우리 3D 결과에도 같은 검사를 걸 수 있다: AM 기둥 보존 · 기공이 어느 상 옆에 남는지) | 일축 · 300 MPa · 분말 · 무바인더가 아니다 · 절대값 · 가압 중 기공 · AM 하중 몫의 측정 없음 |
| **단계 6** (탈압 · 되돌아옴) | 없음 — 모든 값이 감압 뒤 한 상태 (되돌아온 양을 알 수 없다).  쓸 수 있는 것은 "문헌의 가압체 구조 값은 대개 감압 뒤" 라는 표지 하나 | 내리는 곡선 · 회복량 · 가압 중 값 없음 |
| **단계 7** (형상 · 피복 · 수송) | 정성: 상온 가압체 = SE 입자 경계 남음 (피복은 닿은 면 위주) · 190 °C = SE 합체.  EIS 호 폭 123 → 75 → 64 Ω [판독] · 시간 상수 불변 → **닿은 면적이 는 꼴** [카드 해석] — 우리 피복 · 접촉 면적 → 계면 저항 사슬의 정성 짝 | 피복률 · 접촉 면적 · σ_ion · σ_e · tortuosity 수치 없음 |
| **후보 D0** (지금 DEM) | AM 골격이 먼저 닿아 하중을 받고 SE 가 가려진다는 저자 서술 = D0 가 가진 반쪽 (AM-shielding) 의 실험 쪽 말 · 조성 한 점 (74 wt% NCM111 ≈ AM 50 vol% [카드 산술]) | D0 는 유지 시간 · 온도 · SE 합체를 못 낸다 · 견줄 기공 값도 연산자가 달라 없음 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 경계 조건의 다른 끝: **유체 압력 + 봉지** (판 · 벽 · 벽 마찰 없음) 인데도 변형은 두께 방향뿐 (AM 기둥 보존) → "시트 + 등방압 ≈ 일축 변형 + 균일 수직 압력 경계" 로 모델링해도 된다는 운동학 근거 [카드 해석] | 마찰 · 분리 값 없음 |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | R1 의 정성 근거 (AM 접촉이 주변 압력을 푼다 · AM 이 고온에서 자리를 옮긴다) — AM 을 얼리면 SE 가 100 % 를 져 과압축한다는 우리 진단과 같은 방향 | AM 하중 몫 · 이동량 수치 없음 · 속도 무관 소성으로는 둘째 단계를 못 낸다 |
| **후보 B** (입자별 FE + 접촉) | 없음 | — |
| **후보 C** (큰 변형 접촉 DEM · MDR 류) | 없음 | — |
| **후보 C′** (항복 캡 탄소성 접촉 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀 · 캡 소성 · Heckel) | 온도 · 유지 시간에 따른 두께 6 점 (94.5–103 µm) — 크리프 든 균질화 모델의 정성 표적 (시료 산포 ± 2–3 µm 가 신호와 같은 크기) | 압력 축 · 질량 · 밀도 없음 → Heckel · 캡 맞춤 불가 |
| **U0–U6** | **U1** (해상도) 의 실험판 경고: SE 입자 "수 µm" 에 화소 0.65 µm (지름당 화소 ≈3–8) 로는 입자 사이 기공이 갈래에서 빠진다 — 우리 규칙 (d_h/dx ≳ 3.5) 과 같은 종류의 문턱 · **U6** (조밀 충전 수렴) 쪽: 표시 단면 하나의 분율이 3D 값과 ±0.006 안 [판독] | U0 · U2 · U3 · U4 · U5 없음 |
| **R1–R7** | **R1** (AM 이 움직이고 하중을 나눠 짐) — p.5 의 두 문장 (정성 · 추론) + Mn EDS 의 자리 옮김 (190 °C) · **R3** (SE 입자 경계 기억) — 상온 600 MPa 뒤에도 경계가 남는다 (SEM · 한 시야) · **R6** (SE 형상 변형) — 190 °C 에서 합체 (정량 없음) · **R7** (AM 파괴) — 600 MPa 인데 파괴에 대한 말이 없다 · SEM 세 시야에서 뚜렷한 균열은 안 보임 [판독 · 평가 아님] | R2 · R4 · R5 없음 |
| **결과 전 대조 항목** | ① 복합 양극을 누르면 두께는 순간에 끝나고 기공은 SE 영역에 남는다 (방향) ② 가압 뒤 AM 기둥이 보존된다 (우리 3D 결과의 자체 검사로) ③ 상온 등방 600 MPa · 감압 뒤 · 화소 0.65 µm 의 기공 + 탄소 갈래 ≈0.057 (꼬리표와 함께 · 값 대조 아님) ④ 온도 ↑ → EIS 호 ↓ · 봉우리 주파수 불변 — 맞추는 데 쓰지 않음 | 순수 SE 랩 표준과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: NCM111 (우리 NCM811) · LiNbO₃ 코팅 · 바인더 + 아세틸렌 블랙 든 슬러리 시트 (우리 DEM = 무바인더 분말 · r_SE 0.5 µm) · 74 : 23 : 3 wt% · 등방 600 MPa (우리 일축 300 MPa) · 상온–190 °C · 감압 뒤 · 3D 실물 (영상은 3D · 그림은 2D).

## 9. 적용 인사이트 (행동)
1. **결과 전 대조 항목 등록 (단계 5)**: "복합 양극 (AM ≈50 vol%) 에서 두께 변형은 순간에 AM 골격에서 멈추고, 남는 기공은 SE 영역에 있다 (Hayashi 2025 · 등방 600 MPa · 영상)" 를 **방향 항목**으로 — 값은 대조에 쓰지 않는다.
2. **기공 연산자 표 (단계 0) 에 칸 둘 추가**: (i) 영상 갈래에 **탄소가 섞였는지** (ii) **기둥 보존 검사** (분율 × 두께) 를 했는지.  이 논문이 실례: 가압 전 CT 0.19 ↔ 두께 하한 ≥ 0.39–0.44.
3. **우리 3D 결과에 같은 검사를 건다**: 가압 전후 AM 기둥 (φ_AM × 두께) 이 보존되는지 · 남은 기공이 어느 상 옆에 있는지 (SE–SE 사이 / AM 둘레) 를 세 갈래로 세어 본다 — 이 논문의 Fig. 2 와 같은 꼴로 그리면 나란히 볼 수 있다.
4. **시간 의존 한정어**: 우리 DEM · MPM 에는 유지 시간 · 온도 축이 없다는 문장을 계획 문서의 한계 목록에 — 이 논문의 "두 단계" 를 재현 표적으로 삼지 않는다 (둘째 단계의 정체가 미정 · §3-5).
5. **SE–SE 경계 (조건 R3 · Rint ②)**: "상온 600 MPa 등방 뒤에도 SE 입자 경계가 단면 SEM 에 남는다 (190 °C 에서야 사라진다)" 를 SE–SE 계면 항을 두는 정성 근거 한 줄로 — 한 시야 · 정량 없음 표지와 함께.
6. **등방 ↔ 단축을 직접 견준 자료가 필요하면** 이 논문이 아니라 `interfacial_impedance_formulation_assb_cathode` (Choi 2024 · UP-C / IP-C / IP-P) 와 `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` (WIP 400 MPa ↔ CUP 116 MPa · 압력도 다름) 을 본다.
7. **실험 원측정을 받을 때 (DEM 신뢰성 세트)**: 두께만이 아니라 **질량 · 면적 · 진밀도 · 측정 때의 압력 상태** 를 같이 받는다 — 이 논문은 그 넷이 없어 전체 기공을 닫지 못한다 (§3-7).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "For slurry-coated LiNbO₃-coated NCM111 / Li₆PS₅Cl composite cathode sheets (74:23:3 wt%), warm isostatic pressing at 600 MPa reduced the electrode thickness from about 170 µm to about 104 µm at room temperature and 94 µm at 150 °C, and the void ratio determined by synchrotron X-ray CT after pressing (voxel fraction of voids plus carbon, 0.65 µm pixels) saturated at about 0.04 (Hayashi et al., *J. Jpn. Soc. Powder Powder Metallurgy* 72 (2025) S1167–S1173)."
- "With increasing WIP temperature the 0.1 C capacity increased from about 110 to 125 and 128 mAh g⁻¹ and the overpotential decreased by about 0.1 V (Hayashi et al., 2025)."
- 국문 (한정어와 함께): *"슬러리 도포 NCM111 / Li₆PS₅Cl 양극 시트를 600 MPa 로 등방 가압하면 두께는 1 s 안에 끝나고 (≈170 → ≈95 µm), 영상에서 보이는 기공은 유지 시간 · 온도와 함께 더 준다 (Hayashi 2025 · 감압 뒤 CT · 화소 0.65 µm · 기공 + 탄소 분율) — 이 값은 전체 기공률이 아니고, 압력은 600 MPa 하나다."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**: §3-10 의 ①–④.
**카드가 본 한계**
1. **압력 축이 없다** — 600 MPa 하나 · 단축 가압 대조 없음 → "WIP 가 단축보다 낫다" · "압력 ↑ → 기공 ↓" 를 이 논문으로 말할 수 없다.
2. **void ratio 는 영상 갈래 분율** (기공 + 탄소 · 화소 0.65 µm · 감압 뒤) — 전체 기공의 일부만 본다 (가압 전은 절반 이하 · §3-6).  분석 부피 · 문턱 · 반복 미기재.
3. **시료 하나씩 · 오차 막대 없음** — 같은 조건의 void ratio 가 0.042 ↔ 0.029 · 두께 산포 ± 2–3 µm.  온도 효과 (0.057 → 0.039) 는 이 산포의 2–3 배, 100 → 150 °C 의 차 (0.003) 는 산포 안이다.
4. **온도 3 점** (RT · 100 · 150 °C) · 190 °C 는 사진뿐 · 고온에서 SE 분해 · AM–SE 반응 여부를 확인하지 않았다 (XRD · XPS 없음) — 전지 개선을 구조만의 효과로 읽는 것은 저자 해석.
5. **"두 단계" 는 3 점 (1 · 30 · 60 s) + 두께 불변에서 나온 해석** — 승압 시간 미기재 · 둘째 단계가 전체 기공 감소인지 미정 (§3-5).
6. **EIS**: 맞춤값 없음 · 호의 귀속은 인용 하나 · 전극–펠릿 접촉 (150 MPa 로 눌러 붙임) 이 직렬로 끼어 있다 · 측정 온도 · 사이클 번호 미기재.
7. **단면 SEM · EDS 는 한 시야씩** · Mn 띠 높이가 두께 값과 안 맞는다 (§3-8).
8. **로딩 · 밀도 · 진밀도 · 입경 · 바인더 · 용매 미기재** — 재현 · 질량 기준 환산 불가.
9. **저자 소속 = 장치 제조사** · 이해관계 진술 없음.
10. **전이 한계**: NCM111 · 바인더 시트 · 등방 · 600 MPa · 승온 · 감압 뒤 — 우리 (NCM811 · 무바인더 분말 · 일축 300 MPa · 상온) 로 값이 넘어오지 않는다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 13 | Y.-G. LEE, S. FUJIKI, C. JUNG, N. SUZUKI, N. YAHIRO, R. OMODA, D.-S. KO, T. SHIRATSUCHI, T. SUGIMOTO, S. RYU, L. H. KU, T. WATANABE, Y. PARK, Y. AIHARA, D. IM, I. T. HAN: Nat. Energy, 5 (2020) 299–308. | ★ WIP 를 쓴 ASSB 의 원전 (서론: *"over 900 Whl⁻¹ by using WIP … improved the contact properties"*) — WIP 조건 · 기공 값 확인용 · 카드 없음 (`minnmann2021_jes_charge_transport_bottlenecks` 도 "한 자릿수 기공" 으로 2 차 인용 · `dixit2022_isostatic_pressing_ssb_large_scale_manufacturing_review` 의 SI 문헌 표에는 "LPSCl 계 파우치 셀 WIP 490 MPa" 로 올라 있고 밀도 칸은 빈칸 [다른 카드 · 2 차]) · 저자 철자는 이 논문 목록 그대로 (YAHIRO · L. H. KU — 그 카드가 옮긴 같은 문헌의 표기는 Yashiro · Ku, J. H.) |
| 12 | M. DIXIT, C. BEAMER, R. AMIN, J. SHIPLEY, R. EKLUND, N. MURALIDHARAN, L. LINDQVIST, A. FRITZ, R. ESSEHI, M. BALASIBRAMANIAN, I. BELHAROUAK: ACS Energy Lett., 7 (2022) 3936–3946. | ★ 등방 가압 (CIP · HIP) 의 ASSB 적용 — **정본 카드 있음** (`dixit2022_isostatic_pressing_ssb_large_scale_manufacturing_review` · 같은 날 다른 작업이 추가 — push 직전에 확인): 그 카드의 결론 = 같은 압력의 단축 ↔ 등방 대조 값은 **없다** · 황화물 SE 의 등방 가압 밀도 자료 0 건 · 자체 시연은 안티페로브스카이트 펠릿 (단축 ~12 % → CIP 414 MPa ~1.8 % → WIP 345 MPa · 135 °C 0.15 %) [다른 카드] — 이 논문 (600 MPa 하나) 과 합쳐도 복합 양극의 등방 ↔ 단축 같은 압력 짝은 생기지 않는다 · 저자 철자는 이 논문 목록 그대로 (BALASIBRAMANIAN — 그 카드의 원문 표기는 Balasubramanian) |
| 14 | K. HAYASHI, T. MORI, K. FUKUDA: SPring-8/SACLA Research Reports, 10 (2022) 471–477 (in Japanese). | ★ 같은 저자들의 앞선 CT 보고 — 이 논문에 없는 분석 조건 (분석 부피 · 문턱) · 압력 조건이 있을 수 있다 · 카드 없음 |
| 16 | Y. MORINO: Electrochem. 90 (2022) 027001 (4 pages). | EIS 호를 "전하이동" 에 귀속한 유일한 근거 — 귀속 조건 확인용 · 카드 없음 |
| 11 | B. D. L. CAMPÉON, H. B. RAJENDRA, N. YABUUCHI: ChemSusChem, 17 (2024) e202301054 (12 pages). | HIP · CIP 가 ASSB 부품 치밀화에 쓸 만하다는 근거로 인용 — 등방 가압의 압력 · 밀도 자료 가능 · 카드 없음 |
| 10 | A. SAKUDA, A. HAYASHI, M. TATSUMISAGO: Sci. Rep., 3 (2013) 2261 (5 pages). | 정본 카드 있음 (`sakuda2013_sulfide_mechanical_property`) — 서론의 2 차 인용 (> 90 % @ > 350 MPa · 360 MPa 에서 벌크 전도도 근접 · 200 °C 열간 가압) 이 그 카드의 [인쇄] 값과 **같다** [다른 카드] |
| 15 | W. CHOI, J. H. KU, Y. KIM, H. GWON, G. YOON, D. YU, JU-SIK KIM: ACS Appl. Mat. Interfaces, 16 (2024) 26066–26078. | 정본 카드 있음 (`interfacial_impedance_formulation_assb_cathode`) — WIP · 단축 ↔ 등방 대조 |
| 9 | L. FROBOESE, J. F. VAN SICHEL, T. LOELHOEFFEL, L. HELMERS, A. KWADE: J. Electrochem. Soc., 166 (2019) A318–A328. | 정본 카드 있음 (`froboese2019_microstructure_ionic_conductivity_assb_electrode`) |
| 6 · 4 | Deiseroth 2008 · Kamaya 2011 | 정본 카드 있음 (`deiseroth2008_li6ps5x_argyrodite_high_li_mobility` · `kamaya2011_lgps_lithium_superionic_conductor`) |

원문 목록 크롭: `txt_p6_references_first_part.png` (1–5 번) · `txt_p7_references_rest_received_dates.png` (6–16 번 + 접수 · 수정 · 채택 날짜).

## 13. [미확인] 목록 (본문 7 쪽 전수에 없음)
1. 압력 의존 (600 MPa 하나) · 단축 가압한 같은 전극 · 가압 중 상태 · 탈압 회복.
2. 로딩 (mg cm⁻²) · 전극 밀도 · 전극 지름 · 진밀도 · 질량 기준 기공 · 상대밀도.
3. 74 : 23 : 3 의 세 숫자가 각각 무엇인지 · 바인더 · 용매 종류 · 건조 조건.
4. AM · SE 의 입경 수치 · 제조사 · LiNbO₃ 코팅 두께 · SE 의 전도도.
5. WIP 압력 매체 · 승압 · 감압 속도 · 190 °C 시료의 유지 시간 · 조건별 시료 수.
6. CT 분석 부피 · 문턱값 · 전처리 · 재구성 도구 · 조각의 채취 위치 · 반복 · 오차.
7. 두께를 재는 법 · 집전체 포함 여부.
8. 전지: 측정 온도 · 그린 사이클 번호 · 용량의 질량 기준 · 1C 전류 · WIP 안 한 전극의 자료 · 등가 회로 맞춤값.
9. 190 °C 의 void ratio · 두께 · 전지 자료 · 고온에서의 화학 변화 확인.
10. 단면 SEM · EDS 의 기울기 보정 · CT · 전지 시료와의 대응.
11. 같은 조건 (100 °C · 60 s) 의 void ratio 가 두 그림에서 다른 까닭.
12. DOI 접미사 16C-SIS6-03 의 학회 이름.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 본문 7 쪽을 글자 층 추출 + 전 쪽 렌더로 읽음.  서지 = p.1 머리 (학술지 약칭 · 권 72 · 2025 · S1167-S1173 · DOI · ©2025 · CC BY-NC-ND · 제목 · 저자 다섯 · 소속 셋) · 쪽 아래 (*"Vol. 72 Supplement"* · "March, 2025") · p.7 접수 · 수정 · 채택일.  원문 낱말 셈: DEM · simulation · discrete · model = 0 · plastic = 0 · porosity = 0 ("void ratio" 13 회 · "relative density" 는 서론의 Sakuda 인용 1 회) · softening 1 (p.5) · unload · springback = 0 · "600 MPa" 9 회 (그 가운데 하나는 분리막 펠릿의 단축 성형압) · 다른 WIP 압력 0.
- 그림 크롭 **36 장** = 도구 2 (Fig. 8 · Fig. 9 — **둘 다 다시 자름**: 오른축 제목 잘림 / 쪽 폭 띠 + 캡션에 결론 문단 섞임) + 손 크롭 34 (도구가 못 뽑은 Fig. 1–7 · 패널 11 (Fig. 2 a–d · 5 a–b · 6 a–c · 7 a–b) · 등가 회로 삽입도 1 · 근거 문단 15).  본 뒤 다시 자른 것 = fig_2a–2d (JPEG 번짐 줄) · fig_2c · 2d 한 번 더 (라벨 옆 번짐 띠) · fig_5a (래스터 테두리 선).  **식 크롭 0** — 원문에 번호 붙은 식 · 따로 조판된 식이 없다 (등가 회로 그림이 유일한 모델 표현).  36 장 전부 Read 로 열어 확인.  `figures.json` 의 `recrop` · `manual_crop` · `note_manual`.
- 판독: `digitized.csv` 107 행 — Fig. 3 · Fig. 8 은 PDF 벡터 객체 (표지 중심 · 축 틀) · Fig. 2 · 9 는 원 래스터의 색 분류 (검정 분율이 3D 인쇄 그림 값과 ±0.006) · Fig. 4 는 인쇄된 3.68 · 2.48 V 를 3.681–3.683 · 2.483 V 로 재현 · Fig. 5 는 Nyquist 골 ↔ Bode 100 Hz · 끝점 ↔ 0.01 Hz 크기가 서로 맞음.
- 2 차 인용 대조: `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` L439 (서지 · 한 줄 요약) — 원문과 같다 · 고치지 않았다 (그 카드 "🔗 관련 카드" 에 이 카드를 가리키는 한 줄만 더함).  서론의 Sakuda 2013 인용은 정본 `sakuda2013_sulfide_mechanical_property` 의 [인쇄] 값과 대조 (같다).
- 다른 카드에서 옮긴 값: NMC111 4.653 · 카본 블랙 1.834 g cm⁻³ (`ngandjong2021_dem_calendering_digital_twin`) · Li₆PS₅Cl 1.87 g cm⁻³ (`schlautmann2023_se_particle_size_composite_transport`) — 이 논문의 재료 값이 아니다 (카드 산술의 가정).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (hayashi\* 없음) + DOI (jjspm) · 제목 낱말 · 'S1167' grep — 카드 없음 (인용만: `benhadjali2026_…`) (2026-11-12).  push 직전 원격 끝에서 다시 봄: 이 논문 카드는 여전히 없고, ref 12 의 카드 `dixit2022_isostatic_pressing_ssb_large_scale_manufacturing_review` 가 같은 날 새로 들어와 있어 §12 의 12 · 13 번 행과 "🔗 관련 카드" 를 그에 맞게 고쳤다 (그 카드의 값은 [다른 카드] — 원 논문을 이 작업에서 보지 않았다).  그 카드가 *"후보 표의 이웃 (카드가 생기면 서로 가리킬 것): N-64 Hayashi 2025"* 라고 적어 두어, 그 카드 "🔗 관련 카드" 끝에 이 카드를 가리키는 한 줄만 더했다 (다른 곳은 고치지 않았다).

## 🔗 관련 카드
- **이 논문을 인용한 카드**: `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` (ref [27] · WIP 400 MPa · 80 °C · 5 min ↔ 단축 ≈116 MPa · 게이지 두께 82 → 60.7 µm · 보고 기공 34 → 10.9 % [그 카드]).
- **등방 · 온간 · 열간 가압**: `dixit2022_isostatic_pressing_ssb_large_scale_manufacturing_review` (이 논문 ref 12 · 등방 가압 Focus Review · 같은 압력의 단축 ↔ 등방 대조 값 없음 · 황화물 SE 등방 밀도 자료 0 건) · `interfacial_impedance_formulation_assb_cathode` (Choi 2024 = 이 논문 ref 15 · 단축 ↔ 등방 · WIP 500 MPa · 85 °C) · `jun2026_ppma_econductive_binder_si_lowpressure_assb` (파우치 WIP 450 MPa · 80 °C) · `cronk2026_lis_positive_electrode_geometry_fem` (WIP 500 MPa · 80 °C) · `larson2025_hot_pressing_argyrodite_low_stack_pressure_conductivity` (150 °C 열간 단축 · 순수 LPSCl · 입자 융합) · `wang2024_hot_pressed_lpscl_pressure_invariant_conductivity` (20–200 °C · 150–450 MPa · 순수 LPSCl) · `thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography` · `kakar1967_deformation_theory_hot_pressing` · `minnmann2021_jes_charge_transport_bottlenecks` (WIP "한 자릿수 기공" 2 차 인용).
- **복합 양극의 영상 기공 (연산자 주의)**: `sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps` (같은 LiNbO₃ 코팅 NCM111 · **누른 채** CT 0–100 MPa · 기공 44 → 23 %) · `jeong2024_operando_densification_chemomechanics_se_size_composite_cathode` (무하중 XCT 분할 11 vs 16 % · 복셀 0.92 µm) · `cottrino2013_insitu_xct_granulated_alumina_die_compaction` (영상 기공 ≠ 전체 기공 · 기둥 비보존) · `kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation` · `minnmann2024_microstructure_porosity_visualization`.
- **가압 · 기공 기준**: `sakuda2013_sulfide_mechanical_property` (이 논문 ref 10) · `miss2026_insitu_conductivity_porosity_pressure_compaction` · `lee2025_heckel_argyrodite_powder_densification_nanoindentation` · `doux2020_pressure_effects_sulfide_se_jmca`.
- **습식 시트 · 슬러리 전극**: `froboese2019_microstructure_ionic_conductivity_assb_electrode` (이 논문 ref 9) · `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` · `wet_processing_resolved_am_ssb_cathode_manufacturing`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
