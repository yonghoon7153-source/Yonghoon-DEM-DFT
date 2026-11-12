<!-- 표준 양식 확장 (paper-level STANDALONE — 이 카드만 읽어도 논문을 읽은 것과 같게). ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 이웃 = schmitt2026_chemomech_stability_dry_cathode_separator_sheets.md (바로 앞 카드) ·
     이 논문 DEM 매개변수의 출처 = alabdali2023_cgmd_wet_manufacturing_ssb_cathode.md (본문 ref [35]).
     쪽 표기 = PDF 쪽 "p.N" (1–48 · p.1 = ChemRxiv 표지 · 원고 인쇄 쪽 번호 = PDF 쪽 − 1 · 예: PDF p.9 의 인쇄 번호는 8).
     값 표지: [인쇄] = 본문 · 표 · 그림 안에 숫자로 적힌 값 · [판독] = 그림에서 읽은 값 (figure-read ≈ · 경향용 · 정밀도는 그 자리에) ·
     [우리 산술] = 인쇄값으로 우리가 다시 한 계산 (인용 불가) · [추정] = 우리 해석 · [미확인] = 48 쪽 전수에 없음.
     ⚠ SI · 보충 영상은 이 PDF 에 없다 — 본문이 가리키는 Table S1 (DEM 힘장) · S2 (재료 물성) · S3 (수치 매개변수) · Figure S1–S4 · Video 1–4 는 전부 [미확인].
     그림 8 장 · 표 3 장 크롭 전부 렌더로 열람 (fig_6 = 손 재크롭 판 · tab_1 = 처음 크롭은 머리 + 미가압 행뿐이라 CUP · WIP 행을 p.10 글자 층에서 옮겼고, 11-06 메인 세션이 9 · 10 쪽을 이어 붙여 다시 만들었다 (figures.json `manual_crop`) · fig_8 위쪽 본문 낱말도 잘라냄 (`recrop`)) ·
     식 (1)–(3) · (8) · (12)–(24) 는 PDF 쪽 렌더로 확인 (글자 층은 위 · 아래 첨자를 잃는다).  업로드 PDF 는 읽기만 했다. -->

# 온간 등방 가압 (WIP · 400 MPa · 80 °C · 5 min) vs 냉간 단축 가압 (CUP · ≈116 MPa · 상온 · 30 s) 한 습식 NMC622 : LPSCl : 탄소-바인더 69 : 27.6 : 3.4 양극 — 실험 (게이지 두께 −26 vs −12 % · 보고 기공률 10.9 vs 25.1 % · 60 °C C/2 방전 +≈15 mAh/g [판독]) 을 Franco 그룹 CGMD-DEM 제조 사슬 (LAMMPS · LJ 점착 + 입자 탄성 접촉 · 슬러리 → 건조 → 변위제어 가압 · 유지 · 제하) 과 COMSOL 3D 기계-전기화학 FEM (선형 탄성 + 리튬 고유변형 · 응력 의존 화학 퍼텐셜 · 68 MPa 경계) 으로 잇다 — 모델의 C/2 차이는 수송 불균일에서 나오고 정수압 응력 지도 차이는 작다 · ⚠ 모델의 'WIP' = 같은 물성 · 같은 z 방향 변위의 **더 깊은 목표 (30 vs 20 %) + 4 ms 유지** (등방 하중 · 온도 의존 물성 없음) — Ben Hadj Ali⁺ · Qin⁺ · Bhutia · Weckelmann · Raijmakers · Viallet · Seznec · Dao · Franco\* (ChemRxiv 2026 프리프린트 · 비심사)

> slug `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` · DOI `10.26434/chemrxiv.15011566/v1` · type `exp (WIP vs CUP · thickness gauge · geometric porosity · SEM/EDS · XCT · rate capability · GITT · EIS) + DEM/CGMD manufacturing (LAMMPS lj/sf + gran/hertz/history; slurry NPT → drying → displacement-controlled compaction · hold · unloading) + GeoDict voxel microstructure/tortuosity/porosity + PoreSpy snow2 + COMSOL 3D mechano-electrochemical FEM (linear elastic + intercalation eigenstrain · stress-dependent chemical potential)` · PDF `72. Warm Isostatic vs. Cold Uniaxial Pressing in All-Solid-State Battery Cathodes Linking Microstructure Transport and Mechano-Electrochemical Response.pdf` (inbox #72 · 48 쪽 · 원고형 단일 칼럼 · SI · 보충 영상 미포함) · digested `2026-11-06` · status ✅
>
> **원제**: *Warm Isostatic vs. Cold Uniaxial Pressing in All-Solid-State Battery Cathodes: Linking Microstructure, Transport, and Mechano-Electrochemical Response* (p.2)
> **저자 · 소속 (p.2)**: Siwar Ben Hadj Ali ᵃ˒ᵇ˒ᶜ˒⁺ · Lei Qin ᵃ˒ᵇ˒⁺ · Pempa Tshering Bhutia ᵃ˒ᵇ · Luca Weckelmann ᵈ˒ᵉ · Luc Raijmakers ᵈ · Virginie Viallet ᵃ˒ᵇ · Vincent Seznec ᵃ˒ᵇ˒ᶜ · Anh Ha Dao ᶠ · **Alejandro A. Franco ᵃ˒ᵇ˒ᶜ˒ᵍ\*** — ᵃ Laboratoire de Réactivité et de Chimie des Solides (LRCS), Université de Picardie Jules Verne, Hub de l'Energie, UMR CNRS 7314, Amiens · ᵇ RS2E, Hub de l'Energie, FR CNRS 3459 · ᶜ ALISTORE-ERI, FR CNRS 3104 · ᵈ Institute of Energy Technologies, Fundamental Electrochemistry (IET-1), Forschungszentrum Jülich · ᵉ Institute of Physical Chemistry, RWTH Aachen · ᶠ Umicore, Olen · ᵍ Institut Universitaire de France (\* 교신 alejandro.franco@u-picardie.fr · ⁺ 공동 1저자)
> **판 · 지위 (p.1)**: ChemRxiv · 게시 2026-11-02 · v1 · **CC-BY 4.0** · ⚠ *"This is a preprint and has not been peer reviewed. Data may be preliminary."* · 연구비 (p.44) = Umicore DESTINY PhD 프로그램 (EU H2020 MSCA COFUND #945357) · CDC + Région Hauts-de-France + OPCO 2i (AMI-CMA ElectroMob · France 2030) · EU Horizon Europe DigiCell (101135486) · PULSELiON (101069686) · ANR PEPR BATMAN (ANR-22-PEBA-0002) · IUF · XCT 장비 = FZ Jülich IET-1 (Eichel) · *"Dr. Mohammed Alabdali … for providing the microstructural data"* · 이해상충 없음 (p.43) · 데이터 가용성 진술 없음 · 보충자료 링크 = *"at XXX"* (자리표시 · p.44) · 키워드 없음.
> **같은 그룹 카드 (링크만)**: [`alabdali2023_cgmd_wet_manufacturing_ssb_cathode`](alabdali2023_cgmd_wet_manufacturing_ssb_cathode.md) (ref [35] — 이 논문 DEM 의 힘장 · PSD · 밀도 출처) · [`ngandjong2021_dem_calendering_digital_twin`](ngandjong2021_dem_calendering_digital_twin.md) (ref [37]) · [`xu2023_realistic_am_shape_cgmd_calendering`](xu2023_realistic_am_shape_cgmd_calendering.md) (ref [36]) · [`qin2026_bilayer_cathode_cgmd_dem_graded_thick_electrode`](qin2026_bilayer_cathode_cgmd_dem_graded_thick_electrode.md) (Lei Qin · 같은 사슬 · 스프링백) · [`sankar2026_fiber_scale_dem_carbon_felt_manufacturing`](sankar2026_fiber_scale_dem_carbon_felt_manufacturing.md) · [`dem_mechanical_stresses_ssb_electrode_cycling`](dem_mechanical_stresses_ssb_electrode_cycling.md) (Alabdali 2024 — LIGGGHTS 등방 1/3/5 MPa + 사이클 응력 · Ben Hadj Ali 는 저자 아님 · **이 논문은 인용하지 않는다**) · [`zhang2026_polymer_electrolyte_modeling_perspective`](zhang2026_polymer_electrolyte_modeling_perspective.md) (Ben Hadj Ali 선행 2 편을 인용 · 그 둘의 정본 카드는 없음).
> **판독 원자료**: [판독] 값은 크롭 PNG 를 확대해 눈금 보간 (Fig. 3 · 7 · 8) 하거나 색 화소를 분류해 (Fig. 6) 읽었다 — 스크래치 스크립트 · 리포 밖 · digitized.csv 는 만들지 않았다 (경향용).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 같은 습식 NMC622 양극 (69 : 27.6 : 3.4 wt% · 닥터블레이드 150 µm · 80 °C 진공 건조) 을 ≈116 MPa · 상온 · 30 s 로 단축 가압 (CUP) 하거나 400 MPa · 80 °C · 5 min 으로 온간 등방 가압 (WIP) 했더니, WIP 가 더 얇고 (게이지 −26 vs −12 %) 보고 기공률이 낮고 (10.9 vs 25.1 %) 60 °C 율속에서 C/10 은 같고 (190–192 mAh/g) C/2 에서 ≈15 mAh/g 높았으며 [판독] 조립 직후 임피던스가 낮았다 (R0 11.35 vs 34.51 Ω — 단 첫 사이클 뒤 R0 는 둘 다 ≈12 Ω 로 같아지고 R_int 는 오히려 WIP 가 114 Ω 로 크다 · 표 3); 저자는 같은 건조 구조에서 출발한 DEM 두 판 (목표 변위 20 % → 바로 제하 ↔ 30 % → 353 K 4 ms 유지 → 냉각 · 제하 · 최종 두께 감소 12 · 28 %) 을 0.2 µm 복셀로 COMSOL 에 넘겨, 첫 사이클 C/2 에서 WIP 가 더 높은 용량 · 더 고른 이온 전류 · 활물질 이용을 보이고 AM 정수압 응력 지도의 차이는 상대적으로 작다는 것을 보였다 — 그러나 **모델의 WIP 는 등방 하중도 온도 물성도 없는 '더 깊이 누르고 유지한 단축 압축'** 이고, **실험의 WIP 는 압력 (×3.45) · 온도 · 시간 · 하중 방식이 한꺼번에 다르다** (p.2 · p.7 · p.18–21 · p.25–26 · p.30–31 · p.37–42).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 압축 두 경로 (압력 · 온도 · 시간 · 매체) | CUP = 수동 유압 3 t (~116 MPa · Ø18 mm 원판) · 건조실 상온 (가열 없음) · 30 s / WIP = Quintus 온간 등방 프레스 400 MPa · 80 °C · 5 min · 매체 = 물 99 wt% + Dynalene LC-PG 1 wt% · 실리콘 코팅 이형 필름 두 장 · CC 면을 금속판에 대고 고정 · Al 파우치 진공 밀봉 → 둘 다 Ø10 mm 중앙 재펀칭 | [인쇄] p.7 |
| ② 구조 (실험) | 게이지 82 → 72.16 ± 1.65 / 60.68 ± 1.60 µm · 기공 34.12 → 25.13 ± 1.7 / 10.9 ± 2.4 % · 겉보기 밀도 1.591 → 1.805 / 2.199 g/cm³ · SEM · XCT 정성 (WIP 더 촘촘 · 균일) | [인쇄] p.9–10 · p.32–35 · ⚠ 기공 계산에 쓴 성분 밀도 [미확인] (§3-3) |
| ③ 전기화학 | 60 °C · 2.1–3.7 V vs Li-In · 1C = 200 mA/g · C/10 190–192 (둘 다) · C/2 WIP 158–164 vs CUP 143–149 mAh/g · GITT D ≈8 × 10⁻¹² cm²/s (WIP 탈리튬) · EIS 표 3 | [인쇄] p.10 · p.25–31 |
| ④ DEM 제조 사슬 표현 | LAMMPS hybrid/overlay (lj/sf + gran/hertz/history) · 힘장 · PSD · 밀도 = [35] 그대로 (Table S1 [미확인]) · 슬러리 NPT 300 K 20 ms → 건조 (CBSA Ø6.2 → CBD Ø1.3 µm · 상자 높이 57.61 → 51.94 µm 부과) → 가압 = 윗벽 변위 제어 0.02 µm/µs · CUP 20 % → 바로 제하 / WIP 298 → 353 K 가열하며 30 % → 4 ms 유지 → 냉각 · 제하 · **측방 하중 없음 (x · y 주기) · 온도 의존 물성 없음** | [인쇄] p.13–21 |
| ⑤ DEM 구조 · 수송 | AM–SE 0.049 → 0.060 m²/g (+22 %) · AM–CBD 0.012 → 0.011 · SE 상대 유효 확산 0.060 → 0.128 · 'geometric tortuosity' 2.58 → 1.76 · 기공 26.5 → 15 % (실험 25 → 11) · 두께 감소 12 → 28 % (실험 12 → 26) · 밀도 1.82 → 2.22 g/cm³ · σ_ion,eff ≈0.0075 → ≈0.016 · σ_e,eff ≈0.00097 → ≈0.0027 mS/cm [판독] | [인쇄] p.36–38 · Fig. 7c [판독] |
| ⑥ FEM (지배식 · 물성 · 경계조건 · 출력) | COMSOL 반쪽 셀 (Al CC + 양극 미세구조 + SE 분리막 + Li 금속) · AM 안 Fick + μ = μ₀ + RT ln X − Ωσ_h · E_eq 응력 의존 · AM · SE · CBD 선형 탄성 + AM 등방 고유변형 (Koerver 2018 NMC622 ΔV) · 분리막 · CC 강체 · Li = 2D 경계 · 측벽 고정 · CC 바깥면 완전 구속 · 적층압 68 MPa · 물성 (E · ν) Table S2 [미확인] · 출력 = 국소 용량 · 전해질 전류 밀도 · AM 정수압 응력 | [인쇄] p.21–25 · p.40–41 |
| ⑦ "정수압 응력 차이는 작다" 의 근거 | Fig. 8e 의 3D 지도 + 가운데 YZ 단면 한 장 · AM 상만 · 공통 색 −2 … +4 GPa (위 끝 포화 [판독]) · 분포 · 분위수 · 평균 없음 = **시각 판정** · 제조 잔류 응력은 넘기지 않았다 (기하만 · p.21) | [인쇄] p.41 · [판독] |
| ⑧ 우리 EM-01 – 07 | §8 표 — 응력은 DEM 이 아니라 선형 탄성 FEM (고유변형 = 변형 제어 → σ ∝ E) · DEM 접촉력 · 힘 사슬은 출력에서 뺐다 (p.19) · 제하 회복 (Fig. 2 로 우리가 센 ρ = CUP 10.0 % · WIP 2.9 %) 은 목표 변위 선택에 흡수됐다 | §8 |

⛔ **한정어 (떼지 말 것)**: ① **프리프린트 · 비심사** · SI 없음 (DEM 힘장 · 재료 물성 · 수치 매개변수 · 그림 S1–S4 · 영상 [미확인]) ② 실험 WIP ↔ CUP = **400 ↔ 116 MPa (×3.45) · 80 ↔ 상온 · 5 min ↔ 30 s · 등방 ↔ 단축 — 넷이 동시**에 다르다 ③ 모델 WIP ↔ CUP = **목표 변위 30 ↔ 20 % + 4 ms 유지** (같은 물성 · 같은 z 변위 · 등방 하중 없음) ④ 셀 조립 때 두 양극을 SE 펠릿 위에서 *"under the same load"* 로 다시 누른다 (수치 없음 — 바로 앞 문장의 SE 펠릿 2 t ≈ 250 MPa 로 읽힘 [추정]) — 두께 · 기공 측정과 DEM 비교 대상은 조립 전 원판 ⑤ 셀 수 · 반복 · 오차 막대 (율속 · GITT · EIS) 없음 · DEM 한 실현 · 복셀 · 메시 수렴 없음 ⑥ LPSCl = POSCO (우리와 같은 SE 화학) · NMC622 평균 반지름 5 µm (공급사) · 습식 PVDF-HFP + Super P (우리 건식 · VGCF/PTFE 와 다름) ⑦ DEM 매개변수 출처 [35] 의 재료계는 SBS · Super C45 · p-xylene · NEI LPSCl (정본 카드 alabdali2023) — 이 실험과 바인더 · 탄소 · 용매 · SE 공급처가 다르다.

---

## 1. 한 줄 요약

황화물 ASSB 복합 양극에서 '어떻게 누르느냐' 가 미세구조 · 수송 · 기계-전기화학 응답을 어떻게 바꾸는지를, 같은 습식 NMC622/LPSCl 양극을 냉간 단축 가압 (CUP, ≈116 MPa) 과 온간 등방 가압 (WIP, 400 MPa · 80 °C) 으로 만들어 비교한 실험 + 시뮬레이션 프리프린트.  실험에서 WIP 는 두께 · 기공이 더 줄고 (게이지 −26 % · 보고 기공 10.9 %), 조립 직후 임피던스가 낮으며, 60 °C 율속에서 C/10 은 같고 C/2 에서 앞선다.  시뮬레이션은 Franco 그룹 CGMD-DEM 사슬 (슬러리 → 건조 → 가압) 로 같은 건조 구조에서 CUP · WIP 를 만들고 (WIP = 더 깊은 목표 변위 + 고온 유지 + 제하), 두께 감소 · 밀도를 실험에 맞춘 뒤 GeoDict 로 계면 면적 · 기공 · 확산을, COMSOL 로 완전결합 기계-전기화학 (응력 의존 화학 퍼텐셜 · 선형 탄성 · 고유변형) 을 푼다.  결론: 고율 (C/2) 의 WIP 우위는 사이클 열화 없이 첫 사이클의 **구조 · 이온 전류 분포** 만으로도 나오고, AM 정수압 응력 지도의 차이는 이온 전류 지도보다 작다.  압력 크기 · 온도 · 시간 · 하중 방식이 함께 바뀐 실험이고, 모델은 그중 '더 깊이 누름 + 유지' 만 표현한다.

## 2. 메타

| 저자 | 판 | DOI | 소재 (AM / SE / C / 바인더) | 연구유형 |
|---|---|---|---|---|
| S. Ben Hadj Ali⁺ · L. Qin⁺ · P.T. Bhutia · L. Weckelmann · L. Raijmakers · V. Viallet · V. Seznec · A.H. Dao · A.A. Franco\* (LRCS · RS2E · ALISTORE-ERI · FZ Jülich IET-1 · RWTH · Umicore · IUF) | ChemRxiv 2026-11-02 v1 (CC-BY 4.0 · 비심사) | 10.26434/chemrxiv.15011566/v1 | LiNi₀.₆Mn₀.₂Co₀.₂O₂ (NMC622 · Umicore) / Li₆PS₅Cl (LPSCl · POSCO) / Super P (*"Umicore"* 인쇄) / PVDF-HFP (Arkema) — 69 : 27.6 : 3.4 wt% (탄소 : 바인더 나눔 [미확인]) | 실험 (WIP vs CUP · 구조 · 전기화학) + DEM/CGMD 제조 모의 + GeoDict · PoreSpy 미세구조 해석 + COMSOL 3D 기계-전기화학 FEM |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 조성 · 습식 공정 (p.6–7)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 활물질 | NMC622 (Umicore) · 평균 반지름 r_p = 5 µm (*"based on the supplier-reported particle-size distribution"* — GITT 에 씀) · PSD 자체 [미확인] | [인쇄] p.6 · p.10 |
| SE | Li₆PS₅Cl (*"LPSCl, POSCO supplies"*) · 입도 [미확인] | [인쇄] p.6 |
| 탄소-바인더 (CBD) | Super P (인쇄 *"Umicore"*) + PVDF-HFP (Arkema) | [인쇄] p.6 |
| 질량비 | AM : SE : CBD = **69 : 27.6 : 3.4** · 고체 합 3000 mg | [인쇄] p.6 |
| DEM 의 조성 | 68.96 : 27.58 : 3.46 wt% (CBD = 탄소 + 바인더 · 용매 제외) | [인쇄] p.16 |
| 예비 혼합 | NMC622 + LPSCl + Super P · 지르코니아 매체 · **2000 rpm 2 min** | [인쇄] p.6 |
| 슬러리 | PVDF-HFP 를 n-butyl acetate (Sigma-Aldrich) 에 하룻밤 자석 교반 용해 → 분말에 넣고 → 같은 용매로 **액 함량 46 wt%** → 거시적으로 고를 때까지 혼합 | [인쇄] p.6 |
| 도포 · 건조 | 얇은 Al 박 위 닥터블레이드 **간극 150 µm** → **80 °C 진공 하룻밤** → Ø18 mm 펀칭 · 전 공정 건조실 (이슬점 −60 °C) | [인쇄] p.7 |

### 3-2. ★ 두 압축 경로 · 셀 조립 (p.7–8 · Fig. 1)

| 항목 | CUP | WIP | 표지 |
|---|---|---|---|
| 장치 | 수동 유압 프레스 (Fig. 1 모식 = 상 · 하 펀치 + 다이 벽) | 온간 등방 프레스 (Quintus Technologies · Fig. 1 = 강체 챔버 · 액체 매체 · 밀봉 봉투 · 강체 지지판) | [인쇄] p.7 · Fig. 1 |
| 하중 | **3 t (~116 MPa)** — 축 방향 | **400 MPa 등방** — 매체 = 물 99 wt% + 저전도 열매체 Dynalene LC-PG 1 wt% | [인쇄] p.7 |
| 온도 | 건조실 상온 · *"without additional heating"* (Fig. 1 = 25 °C) | **80 °C** | [인쇄] p.7 · Fig. 1 |
| 시간 | **30 s** | **5 min** | [인쇄] p.7 |
| 시료 고정 | — | 실리콘 코팅 고분자 이형 필름 두 장 사이 · **CC 면을 금속판에** 대고 고정 (강체 지지) · Al 파우치 진공 밀봉 | [인쇄] p.7 |
| 뒤 처리 | 가장자리 효과를 피해 **둘 다 Ø10 mm 중앙부 재펀칭** · 질량 = 분석 저울 · 두께 = 자동 게이지 | | [인쇄] p.7 |

- [우리 산술]: 3 t × 9.807 m/s² / (π · 9² mm²) = **115.6 MPa** (인쇄 ~116 ✓) · SE 펠릿 2 t / Ø10 mm = **249.7 MPa** (인쇄 ~250 ✓) · **압력 비 400/116 ≈ 3.45 · 시간 비 10 · ΔT ≈ +55 K**.
- **셀 조립** [인쇄 p.7–8]: LPSCl **100 mg** 을 플라스틱 몰드에서 **2 t (~250 MPa)** 로 눌러 Ø10 mm 펠릿 → 양극 원판을 한쪽 면 가운데 놓고 *"pressed under the same load to ensure intimate interfacial contact"* (수치 없음 — 앞 문장의 2 t 로 읽힘 [추정]) → 반대 면 = Ø9 mm In 박 가운데 Li 금속 원판 (손으로 살짝 눌러 Li-In · In 이 SE 쪽) · Li 쪽에 Ø10 mm Ni 집전체 → 셀 틀 · 나사 셋 균일 조임 · **토크 11 N m → *"estimated stack pressure of 68 MPa"*** (추정 방법 [미확인]).
- ⚠ CUP 양극 (116 MPa 로 만든 것) 도 조립 때 그보다 높을 수 있는 하중을 한 번 더 받는다 [추정] — 두께 · 기공 · DEM 대조는 조립 **전** 원판이다.
- 셀 수 · 반복 [미확인] (율속 · GITT · EIS 모두 오차 막대 없음).

### 3-3. ★ 구조 — 실험 (표 1 · 표 2 · 식 1 · Fig. 4 · Fig. 5 · p.8–10 · p.32–35)

| 상태 | 게이지 두께 (µm) | 두께 감소 | 기공률 (%) | 기공 감소 | 겉보기 밀도 (g/cm³) |
|---|---|---|---|---|---|
| 미가압 | **82** | Ref | **34.12** | Ref | **1.59 ± 0.04** (본문 1.591 ± 0.04 · DEM 절 1.5918) |
| CUP | **72 ± 1.2** (본문 72.16 ± 1.65) | 12 ± 2 % | **25.1 ± 1.7** (본문 25.13) | 26 ± 5 % | **1.81 ± 0.06** (본문 1.805) |
| WIP | **61 ± 1.6** (본문 60.68 ± 1.60) | 26 ± 2 % | **10.9 ± 2.4** | 68 ± 7 % | **2.20 ± 0.06** (본문 2.199 ± 0.058) |

표지: [인쇄] 표 1 (p.9–10) · 표 2 (p.10) · 본문 p.9.

- **기공률 식 (1)** [인쇄 p.9]: ε = 1 − (m_el/V_el)·(X_NMC/ρ_NMC + X_CBD/ρ_CBD + X_LPSCl/ρ_LPSCl) — m_el · V_el = 펀칭 시료 질량 · 기하 부피 · Ø10 mm 원판 안 **다섯 자리**에서 뗀 시료 · ⚠ **성분 밀도 ρ_i 의 값 [미확인]** · 두께 · 질량이 Al CC 를 포함하는지 [미확인] · 게이지 = *"the probe moves toward the electrode surface and automatically stops upon contact"*.
- **SEM 두께** (Fig. 4a · p.32): 양극층만 **50.10 (미가압) · 47.77 (CUP) · 36.35 µm (WIP)** · CC 포함 **70.7 · 62.7 · 51.3 µm → 감소 11.3 % · 27.5 %** [인쇄] — 저자: 측정법마다 다른 것은 *"lateral heterogeneity of the cathode"*.
- **XCT 두께** (Fig. 5a 그림 안 표기): **CUP 54.5 µm · WIP 37.72 µm** [인쇄 그림].
- **[우리 산술 — 서로 맞나]**:
  - (1 − ε) × 게이지 두께 = **54.0 · 54.0 · 54.1 µm** (미가압 · CUP · WIP) → 같은 면적당 고체량 = 질량 보존과 맞는다.
  - ρ_app / (1 − ε) (식 1 이 쓴 골격 밀도) = **2.415 · 2.411 · 2.468 g/cm³** → WIP 만 +2.3 % (밀도 2.199 를 미가압의 골격 밀도로 다시 세면 기공 ≈8.9 % · 보고 10.9 ± 2.4 의 범위 안).
  - ⚠ 흔히 쓰는 성분 결정 밀도 (NMC622 4.7–4.8 · LPSCl 1.64–1.86 · 탄소 · 바인더 1.8–2.0 g/cm³ — **이 논문에 없는 우리 가정**) 로 69 : 27.6 : 3.4 의 골격 밀도를 세면 **2.99–3.24 g/cm³** → 같은 겉보기 밀도의 기공률은 **47–51 · 40–44 · 27–32 %** (미가압 · CUP · WIP) — 보고값 34 · 25 · 11 % 는 골격 ≈2.41–2.47 g/cm³ 을 뜻한다 → **보고 기공률이 어떤 밀도로 셌는지 원문만으로는 재현되지 않는다** (§10-6).
  - 세 측정의 두께가 크게 다르다: CUP 게이지 72.16 · SEM 47.77 · XCT 54.5 µm (최대 1.51 배) · WIP/CUP 두께 비 = 게이지 0.841 · SEM 양극층 0.761 · SEM CC 포함 0.818 · XCT 0.692.
  - SEM 양극층만의 감소 = **CUP 4.7 % · WIP 27.4 %** · SEM 함축 CC 두께 (포함 − 양극층) = **20.6 · 14.9 · 15.0 µm** — 같은 Al 박이면 같아야 하므로 측정 위치가 다른 값의 조합이다 [추정 · 저자의 '측면 불균일' 설명과 같은 방향].
  - 면적당 질량 ρ_app × 게이지 두께 = **13.0 · 13.0 · 13.3 mg/cm²** → AM ≈ 9.0–9.2 mg/cm² · 1C ≈ 1.8 mA/cm² · C/10 면적 용량 ≈ 1.7 mAh/cm² (두께 · 질량이 같은 정의라는 가정 · 원문에 로딩 없음).

### 3-4. 전기화학 — 율속 · CE (Fig. 3a · 3b · p.10 · p.25–27)

- 조건 [인쇄 p.10]: **60 °C · 2.1–3.7 V vs Li-In** · 명목 용량 200 mAh/g_AM 기준 **1C = 200 mA/g** · **25 사이클** = C/10 → C/5 → C/3 → C/2 → 1C 각 5 사이클 (충 · 방 같은 율) · 비전류 = 최종 AM 질량 기준 · C/10 첫 두 사이클을 모델 검증에 씀 (본문은 *"(Figure 2a)"* 라 적는다 — Fig. 3a 의 오기 · §10-19).
- 본문 [인쇄 p.25–26]: C/10 두 양극 **190–192 mAh/g** (거의 완전 이용) · C/5 · C/3 에서 WIP 가 계속 높고 · **C/2 WIP 158–164 vs CUP 143–149 mAh/g = +10–15 mAh/g** (*"lower polarization and more effective Li⁺ transport pathways"*) · 1C 둘 다 크게 떨어지고 WIP 의 추가 하락이 더 가파르지만 여전히 높다 · 1C 에서 *"the present results do not provide direct evidence that mechanical degradation is responsible"* · C/10 회복 단계가 없어 비가역 열화 몫을 배제 못 함.

| 율 (사이클) | WIP (mAh/g) | CUP (mAh/g) | 차 |
|---|---|---|---|
| C/10 (1→5) | ≈193 → 191 | ≈192 → 190 | ≈1 |
| C/5 (6→10) | ≈185 → 182 | ≈184 → 179.5 | ≈1–2.5 |
| C/3 (11→15) | ≈176 → 171 | ≈168 → 163 | ≈8 |
| C/2 (16→20) | ≈164 → 158 | ≈149.5 → 143.5 | **≈14.5** |
| 1C (21→25) | ≈128.5 → 129.5 → 129 → 128 → 127 | ≈129 → 126.5 → 125 → 124 → 123 | ≈−0.5 (21) → ≈4 |

표지: [판독 ±1 mAh/g] Fig. 3b 확대 렌더.  CE [판독]: 대부분 ≈100 % · CUP 는 율이 바뀌기 직전 사이클 (10 · 15 · 20) 에 ≈95 % · 마지막 사이클 (25) ≈90 % · 첫 사이클 ≈94–95 % (둘 다).  ⚠ 1C 첫 사이클 (21) 은 CUP ≈ WIP (CUP 가 아주 조금 위) — 본문 *"remains higher than that of CUP"* 는 22–25 사이클에 맞다.

### 3-5. GITT — 겉보기 Li⁺ 확산 (Fig. 3c · 3d · 식 2 · p.10 · p.28–29)

- 방법 [인쇄 p.10]: C/20 · 2.1–3.7 V vs Li-In · 펄스 60 min + 개방 90 min · Weppner–Huggins **D_Li = (4/9π) (ΔE_s/ΔE_t)² r_p²/t_p** (식 2 · 렌더 확인) · r_p = 5 µm · 분석 전위 ≈2.9–3.7 V vs Li-In (아래 끝 급변 구간 제외 · Figure S4 [미확인]) · 온도 · 어느 셀 · 몇 번째 사이클인지 [미확인].
- 본문 [인쇄 p.28–29]: 탈리튬 (충전) 에서 WIP 가 대부분 **≈8 × 10⁻¹² cm²/s** 로 안정 · CUP 는 처음 · 끝에서 크게 흔들림 · WIP 가 대체로 높되 *"the differences are modest"* · 리튬화 (방전) 에서는 WIP 가 일부 구간 조금 낮다 · 해석 (AM 수축 → CUP 접촉 손실 · AM 팽창 → WIP 구속) 은 *"possible explanation … rather than a direct determination"* · *"do not permit the observed asymmetry to be attributed uniquely to mechanical effects"*.
- [판독] 충전: WIP 6.5–9.8 × 10⁻¹² (2.95–3.6 V) · 3.66 V ≈3.5 × 10⁻¹² / CUP 2.98 V ≈2.4 × 10⁻¹⁵ → 3.02 V ≈3 × 10⁻¹² → 가운데 7–8.5 × 10⁻¹² → 3.65 V ≈4 × 10⁻¹² → 3.68 V ≈1.8 × 10⁻¹³ · 방전: CUP 2.93 V ≈1.2 × 10⁻¹³ → ≥3.1 V 에서 1.0–1.3 × 10⁻¹¹ / WIP 2.95 V ≈1.0 × 10⁻¹² → 0.6–1.1 × 10⁻¹¹.
- ⚠ 가운데 전위 (≈3.05–3.6 V) 충전 D 는 두 양극이 ≈10–30 % 안 [판독] — "WIP 가 높다" 는 주로 양 끝점이 만든다.
- [우리 산술] 8 × 10⁻¹² cm²/s = **8 × 10⁻¹⁶ m²/s** (r_p 5 µm 규약).

### 3-6. EIS (Fig. 3e–h · 표 3 · 식 3 · p.11–12 · p.30–31)

- 방법 [인쇄 p.11]: GITT 이완 단계마다 정전위 EIS · 10 mV · **10 kHz–0.1 Hz** · 10 배당 8 점 · 주파수마다 3 회 평균 · RelaxIS 적합 · 두 전극 배치 (Li-In 기여를 *"cannot be completely excluded"* · 작고 일정하다고 가정) · 등가회로 (Fig. 3f 안) = **R0 − (R_int ∥ CPE) − ((R_ct − W) ∥ CPE)**.

| | R0 (Ω) | R_int (Ω) | R_ct (Ω) | 합 (Ω) [우리 산술] |
|---|---|---|---|---|
| CUP · 사이클 전 | 34.51 | 64.43 | 355.97 | 454.9 |
| WIP · 사이클 전 | 11.35 | 15.7 | 60.43 | 87.5 |
| CUP · 첫 사이클 뒤 | 12.1 | 16.4 | 50.9 | 79.4 |
| WIP · 첫 사이클 뒤 | 12.8 | **114** | 16.4 | **143.2** |

표지: [인쇄] 표 3 (p.31).

- 본문 [인쇄 p.30–31]: 조립 직후 WIP 의 R0 · R_int · R_ct 가 모두 낮다 (*"improved particle-to-particle and particle-to-electrolyte contacts"*) · 첫 사이클 뒤 *"a marked decrease in impedance is observed for both cathodes"* · R0 가 둘 다 ≈12 Ω 로 수렴 = NMC 리튬화 팽창이 CUP 의 접촉을 메웠다는 해석 · 결론 *"the overall EIS analysis confirms that isostatically presing provides more favorable electrochemical kinetics, in agreement with the lower impedance observed before and after cycling"*.
- ⚠ [우리 산술 · 판독] 첫 사이클 뒤 **WIP 의 R_int 는 15.7 → 114 Ω 로 늘고 합은 WIP 143 Ω > CUP 79 Ω** — Fig. 3f 에서도 WIP 호가 더 크다 (Re ≈115 Ω 까지 · −Im ≈38 Ω ↔ CUP Re ≈77 · −Im ≈14.5 Ω [판독]) → *"lower impedance … after cycling"* 과 반대 (§10-9).
- **R_ct(전위)** [판독]: 충전 (Fig. 3g) CUP ≈135–145 Ω (3.0 V ≈220) · WIP ≈7.3–10 Ω (3.0 V ≈26) → **≈1/15–1/19** / 방전 (Fig. 3h) CUP 2.98 V ≈50 → 3.05–3.37 V ≈7.5–9.5 → ≥3.45 V ≈4.5–5.0 · WIP ≈15 → ≈8.8–9.7 Ω → **3.05–3.7 V 에서는 CUP 가 더 낮다 (최대 ≈2 배)** — 본문 *"the Rct values gradually converge"* (§10-10).
- **j₀ 환산** (식 3 · 렌더 확인): **R_ct = RT/(zFAj₀)** · A = *"the geometric AM-SE interfacial area"* (어디서 온 면적인지 [미확인] · z 정의 없음) · 선형 Butler–Volmer · 균일 계면 가정 → *"effective or apparent exchange-current density"* · j₀ 값 미기재 (Table S2 [미확인]).

### 3-7. SEM · EDS · XCT (Fig. 4 · Fig. 5 · p.12–13 · p.31–35)

- **SEM** [인쇄 p.12]: Ar 글로브박스 안 준비 · Ø10 mm 시료 반 자름 · 구리 테이프 사이 · **극저온 이온 연마 −120 °C · 6 kV 6 h + 4 kV 30 min** · BED-C 3 kV · EDS = FlatQuad · 5 kV · *"A probe current of 90 and high-current mode"* (단위 없음).
- **EDS 범례 (그림 판독)** = S · Cl · P · Ni · O · C · Al ↔ 캡션 *"C, O, Ni, Co, Mn, and Al"* (§10-18).
- 정성 (p.32–34): WIP = *"more homogeneous and nearly isotropic densification"* · AM 이 두께 · 면내 모두 더 가깝다 · SE 가 더 촘촘 · 연속 / CUP = *"more directionally constrained particle arrangement"*.  [판독 · 정성 · 저자 언급 없음] WIP EDS 지도의 AM 몇 개 안에 금 모양 어두운 선 · 점이 보인다 (CUP 지도보다 많아 보임 — 연마 인공물과 구별 안 됨).
- **XCT** [인쇄 p.12–13]: 시료 ≈3 × 3 mm · 무용매 2 액형 수지 (UHU) 매립 · 글로브박스 안 하룻밤 경화 · Zeiss Xradia 620 Versa · 20× 대물 · **복셀 0.68 µm** · 50 kV · 노출 13 s (WIP) / 11 s (CUP) · 투영 1601 장 × 3 · 저에너지 필터 · Dragonfly · **AM 만 문턱 분할** (나머지 = SE + CBD + 기공 합) · 자체 Python 으로 투영 · 열마다 첫 · 끝 AM 복셀 거리 = 국소 두께.
- 결과 (p.34–35): 두 시료 모두 AM 분포는 대체로 고르고 뚜렷한 균열 · 큰 빈자리 · AM 결핍 영역 없음 (보충 영상 3 · 4 [미확인]) · CUP 가 입자 사이 부피가 크고 두껍다 · 최대 세로 거리 분포에서 **CUP 의 긴 꼬리** (국소적으로 두꺼운 곳).  [판독 Fig. 5f] WIP 봉우리 ≈29–30 µm · ≈40 µm 에서 끝 / CUP ≈15–55 µm 로 넓고 ≈60 µm 까지 꼬리.

### 3-8. ★ DEM 제조 사슬 — 수치 (Fig. 2 · p.13–21)

| 단계 | 내용 | 수치 · 표지 |
|---|---|---|
| 입자 · 힘장 | 거친 입자 (coarse-grained) 구 AM · SE · CBSA (슬러리 = 탄소 + 바인더 + 용매 덩이) → 건조 뒤 CBD · LAMMPS `hybrid/overlay` = `lj/sf` + `gran/hertz/history` · 두 하위 꼴이 겹치는 쌍은 힘을 더한다 (식 4) · 매개변수 = [35] 에서 *"retained without additional fitting"* | Table S1 [미확인] · [인쇄] p.13–16 |
| 슬러리 | [35] 의 입자 기반 습식 모델 · 3D 주기 · 공액경사 에너지 최소화 → **NPT/sphere 300 K · 2,000 만 step × 0.001 µs = 20 ms** · 등방 목표압 0 → 100 kPa (≈대기압) · 열욕 · 압욕 감쇠 0.2 · 1000 µs | [인쇄] p.16–17 |
| 건조 | 용매 제거 = **CBSA Ø6.2 µm · 0.05 pg µm⁻³ → CBD Ø1.3 µm · 0.9 pg µm⁻³ 순간 변환** (입자 수 · 정체 그대로) · CBD 고유 나노 기공 50 % (유효 밀도로 넣음) · 슬러리 → 건조 매개변수 교체 (꼴 같음 · 재적합 없음) · 상자 높이 **57.61 → 51.94 µm (−9.84 % 부과)** · x = y = **41.25 µm** · x · y 주기 · z = 입자 벽 (아래 = CC 쪽) · **dt 0.00001 µs** · 298 → 333 K 가열 (500 만 step = 50 µs · 벽을 전극 경계로) → 333 K 에서 높이 줄임 (2,000 만 step = 200 µs) → 333 → 298 K 냉각 (500 만 step = 50 µs · 재배열) = **300 µs** | 건조 밀도 **1.5965 vs 실험 1.5918 g/cm³ (0.29 %)** · [인쇄] p.17–18 |
| 가압 공통 | 같은 건조 구조 (입자 · 좌표 · 정의 · 매개변수 · CC · 치수 동일) · **dt 0.0002 µs** · 아래 CC 경계 고정 · 위 강체 경계를 z 로 변위 · **x · y 주기 · 측방 하중 없음** · *"No external pressure was prescribed"* (변위 제어) · **같은 건조 매개변수 · 온도 의존 탄성 상수 · 접촉 강성 · 상호작용 · 감쇠 변경 없음** · 접촉력 분포 · 힘 사슬은 출력에서 제외 | [인쇄] p.18–19 |
| CUP | **298 K · 0.02 µm µs⁻¹ 로 명목 20 %** → 유지 없이 위 경계를 바로 올림 → 제하 · 이완 · **최종 ≈12 %** (실험 12 % 와 일치) | 밀도 **1.814 vs 1.805 (0.50 %)** · [인쇄] p.20 |
| WIP | 압축하며 **298 → 353 K** · 0.02 µm µs⁻¹ 로 **명목 30 %** → 목표 두께에서 **4 ms 유지 (353 K)** → 같은 방식 제하 + 353 → 298 K 냉각 (**200 만 step = 400 µs**) → 이완 · **최종 ≈28 %** (실험 26 %) | 밀도 **2.217 vs 2.199 (0.82 %)** · [인쇄] p.20 |
| 이완 · 넘김 | 두께 · 운동 에너지가 거의 안정할 때까지 (보충 영상 1 · 2 [미확인]) → **0.2 µm 등방 복셀화** → GeoDict (미세구조 · 유효 수송 · 모듈 이름 미기재) · PoreSpy SNOW2 (기공-목 망) · 자체 INNOV [38] · 복셀 메싱 [39] → COMSOL · *"No additional particle displacement, artificial densification, isotropic rescaling, or phase redistribution"* | [인쇄] p.21 |

- **Fig. 2 치수 (그림 안 표기)** [인쇄 그림]: 평형 슬러리 57.62 µm (본문 57.61) · 건조 **51.94** · CUP 눌림 (298 K) **41.55** → 회복 뒤 **45.71** · WIP 눌림 (353 K) **36.36** → 회복 뒤 **37.40 µm** · 측면 41.25 × 41.25 µm.
- **[우리 산술]**:
  - 명목 감소 41.55/51.94 = 0.800 · 36.36/51.94 = 0.700 ✓ · 최종 감소 **12.0 % · 28.0 %** ✓.
  - **회복 (제하 뒤 되튐)**: 부과 감소 중 되돌아온 몫 = **CUP 40.0 % (4.16 / 10.39 µm) · WIP 6.7 % (1.04 / 15.58 µm)** · 우리 언로딩 등록의 ρ = (h − h₀)/h₀ 꼴로는 **CUP 10.0 % · WIP 2.9 %**.
  - 밀도 × 두께 = 1.5965 × 51.94 = 1.814 × 45.71 = 2.217 × 37.40 = **82.92** (세 상태 같음) → DEM 밀도 = 질량 / 상자 부피 · **밀도 일치 = 두께 감소 일치와 같은 정보**.
  - ⚠ 보고 DEM 기공률 (26.5 · 15 %) × 두께: (1 − ε) × t = **33.6 µm (CUP) ↔ 31.8 µm (WIP) (−5.4 %)** — 구 부피가 보존되면 같아야 한다 → 질량 기준이면 CUP 26.5 % 일 때 WIP ≈10.2 % · WIP 15 % 일 때 CUP ≈30.5 % (§10-5).
  - 가압 속도 0.02 µm µs⁻¹ = **0.02 m/s (20 mm/s)** · CUP 압축 ≈519 µs · WIP 압축 ≈779 µs + 유지 4 ms (= 2,000 만 step) · 실험 유지 5 min 의 **1/75,000** · 준정적 점검 (관성수 등) 보고 없음.
  - 측면 41.25 µm ≈ AM 지름 4 개 (Ø ≈10 µm 가정 — r_p 5 µm · [35] 카드의 AM 중심 ≈10 µm) · DEM **한 실현** (시드 · 반복 서술 없음).
- 건조 상자 높이 51.94 µm (−9.84 %) 와 명목 목표 20 · 30 % 를 **어떻게 골랐는지** 원문에 없다 [미확인].

### 3-9. ★ DEM 구조 · 수송 기술자 (Fig. 6 · Fig. 7 · p.35–38)

| 기술자 | CUP | WIP | 표지 |
|---|---|---|---|
| AM–SE 비계면적 (m²/g · '무엇의 g' [미확인]) | 0.049 | **0.060 (+22 %)** | [인쇄] p.36 · Fig. 7a |
| AM–CBD 비계면적 (m²/g) | 0.012 | 0.011 (−8 %) | [인쇄] p.37 |
| 기공 지름 범위 | ≈0.2–4.2 µm (넓다) | 대부분 ≈1.0–1.8 µm (좁다) | [인쇄] p.37 |
| σ_ion,eff (mS/cm) | ≈0.0075 | ≈0.016 (×2.13) | [판독] Fig. 7c (본문 수치 없음) |
| σ_e,eff (mS/cm) | ≈0.00097 | ≈0.0027 (×2.8) | [판독] Fig. 7c |
| SE 상대 유효 확산 D_eff/D₀ | **0.060** | **0.128** | [인쇄] p.37 |
| *"geometric tortuosity"* (SE) | **2.58** | **1.76** | [인쇄] p.37 · Fig. 7d 축 이름 = *"Tortuosity factor"* |
| DEM 기공률 | **≈26.5 %** | **≈15 %** (−43 %) | [인쇄] p.37 · Fig. 7e |
| 실험 기공률 | 25.1 ± 1.7 % | 10.9 ± 2.4 % | [인쇄] 표 1 |
| 두께 감소 (DEM ↔ 실험) | ≈12 ↔ 12 ± 2 % | ≈28 ↔ 26 ± 2 % | [인쇄] p.38 · Fig. 7f |
| 겉보기 밀도 (DEM ↔ 실험) | ≈1.82 ↔ 1.81 | ≈2.22 ↔ 2.20 g/cm³ (+22 %) | [인쇄] p.38 · Fig. 7g |
| 기공-목 망 (SNOW2 · 0.2 µm · 0.6 µm (≈3 복셀) 넘는 기공 · 목만) | 넓게 잇닿은 망 | 성기고 조각난 망 | [인쇄] p.38 · Fig. 7h (정성) |

- **Fig. 7b 기공 부피 분율** [판독 ±0.005 · 막대 13 개 0.2–5 µm]: CUP 0.046 · 0.077 · 0.127 · 0.105 · **0.148 (1.8)** · 0.130 · 0.102 · 0.093 · 0.083 · 0.043 · 0.033 · 0.007 · 0.005 / WIP 0.095 · 0.147 · **0.212 (1.0)** · 0.155 · 0.175 · 0.111 · 0.069 · 0.013 · 0.011 · 0.012 · 0 · 0 · 0 (합 ≈1.00 둘 다).
- **Fig. 6 상 분율** [판독 · 색 화소 분류 · ±0.03]: **패널 a** (그림 제목 *"WIP"* — §10-15 판정상 **CUP**) = 곡선이 ≈45.5 µm 까지 · 두께 평균 기공 0.43 · AM 0.24 · SE 0.26 · CBD 0.07 · 양 끝 3 µm 뺀 bulk 기공 0.38 · AM 0.27 · SE 0.28 · CBD 0.07 / **패널 b** (제목 *"CUP"* — 판정상 **WIP**) = ≈37.3 µm 까지 · 평균 기공 0.31 · AM 0.30 · SE 0.32 · CBD 0.08 · bulk 기공 0.27 · AM 0.33 · SE 0.31 · CBD 0.09 (패널마다 합 1.00).
- 본문 (p.35): WIP 가 대부분 두께에서 국소 분율 요동이 작고 (*"more homogeneous through-thickness microstructure"*) · CUP 는 위쪽에서 기공이 국소적으로 크다 (제하 뒤 남은 덜 치밀한 영역) · bulk 기공도 CUP 가 높다.
- **[우리 산술]** (§6 에 상세):
  - Fig. 6 두께 평균 고체 분율 비 WIP/CUP = 0.69/0.57 = **1.21** ↔ 두께 비 45.71/37.40 = **1.22** ✓ (Fig. 6 은 고체 부피 보존과 맞는다 · 보고 기공률 26.5 · 15 % 는 1.16 으로 안 맞는다).
  - Fig. 6 평균 기공 + DEM 밀도의 함축 골격 밀도 = 1.814/0.57 ≈ 2.217/0.69 ≈ **3.19 g/cm³** (두 침대 같음) ↔ 실험 식 (1) 의 함축 골격 2.41–2.47.
  - σ_ion,eff / (D_eff/D₀) = 0.0075/0.060 = 0.016/0.128 = **0.125 mS/cm** (두 침대 같음) → 이온 계산에 넣은 SE 고유 σ 가 0.125 mS/cm 라는 뜻 (입력값 원문 없음 · 축 단위 확인 필요 §10-17).
  - 인쇄 τ² × (D_eff/D₀) = 2.58² × 0.060 = **0.399** · 1.76² × 0.128 = **0.397** (두 침대 같음).

### 3-10. ★ FEM 결과 — 율속 · 지도 · 응력 (Fig. 8 · p.38–42)

- **C/10 첫 사이클 (Fig. 8a)**: 두 구조의 모의 · 실험 곡선이 매우 비슷 · *"The model satisfactorily reproduces the overall shape and polarization of the experimental profiles, although some deviation remains close to the end of discharge"* [인쇄 p.39] · 그림 안 조건 = NMC622 \| LPSCl \| Li · 0.1 C 충 · 방 · **60 °C · 68 MPa** · 1C = 200 mA/g.  [판독] 모의 방전 끝 ≈210 mAh/g (CUP · WIP 겹침) ↔ 실험 ≈191–192 · 모의 충전 ≈209–211 ↔ 실험 ≈207–208 → **모의 방전이 ≈10 % 크다**.
- **C/2 (Fig. 8b)**: 모의 = **처음 사이클 (깨끗한 구조)** · 실험 = 율속 시험의 **20 번째 사이클** → *"not intended as a quantitative model validation but rather as a qualitative assessment"* [인쇄 p.39].  [판독] 모의 방전 CUP ≈190 · WIP ≈201 (**차 ≈11**) ↔ 실험 CUP ≈142 · WIP ≈157 (**차 ≈15**) · 모의 충전 ≈197 / ≈205 ↔ 실험 ≈144 / ≈159 → 구조만 다르고 동역학 (j₀ · D) 이 같은 모델이 실험 차의 ≈3/4 을 낸다 [우리 산술 · 판독].
- **국소 용량 (Fig. 8c · 탈리튬 끝 · 색 170–200 mAh/g)** [판독]: C/10 두 구조 모두 거의 전체 ≈200 · C/2 WIP 대부분 ≥193 · CUP 는 넓게 ≈188–193 + 아래쪽에 ≈172–178 영역.
- **전해질 전류 밀도 (Fig. 8d · 탈리튬 90 % · 색 0–20 A/m²)** [판독]: C/10 둘 다 낮다 (≈0–4) · C/2 CUP 는 윗면 · 단면 한 곳에 뜨거운 자리가 몰리고 WIP 는 더 퍼져 있다 · 본문 = CUP 에 *"preferential ionic-transport pathways and locally underutilized AM regions"* [인쇄 p.41].
- **정수압 응력 (Fig. 8e · 탈리튬 끝 · AM 상 · 색 −2 … +4 GPa · 양수 = 인장)** [판독]: AM 안쪽 ≈0–1 GPa · 입자 접점 · 목 ≥3–4 GPa (색 포화) · 3D 지도 윗면에 짙은 포화 영역 · CUP ↔ WIP 패턴 비슷.  본문 [인쇄 p.41]: *"the overall difference between the CUP and WIP stress fields is substantially less pronounced than that observed for the ionic-current distribution"* · 인장은 주로 *"particle-particle contact regions and … geometrically confined areas"* · 활발한 반응 영역과 겹칠 수 있다 · *"the high-rate performance difference is more strongly associated with transport-induced electrochemical heterogeneity than with a pronounced difference in the overall hydrostatic-stress field"*.
- 분포 · 평균 · 분위수 · 상별 응력 · SE 응력 지도 **없음** · [우리 산술] 경계 적층압 68 MPa = 색 천장 4 GPa 의 **1.7 %**.
- 결론 (p.42–43): WIP 의 고율 우위는 *"primarily associated with improved ionic transport and more homogeneous electrochemical utilization"* · 깨끗한 구조 + AM 부피 변화를 넣은 모의에서도 나와 *"independently of accumulated cycling-induced degradation"* · 다음 일 = 비가역 접촉 변화 · 계면 열화 · 손상을 넣은 반복 사이클.

---

## 4. ★ 방법 — 측정 사슬 · DEM · FEM · 입자 처리

### 4-1. 측정 사슬 (실험)
예비 혼합 (2000 rpm 2 min) → PVDF-HFP/n-butyl acetate 슬러리 (액 46 wt%) → 닥터블레이드 150 µm · 80 °C 진공 건조 → Ø18 mm → (CUP 116 MPa · 상온 · 30 s) 또는 (WIP 400 MPa · 80 °C · 5 min) → Ø10 mm 재펀칭 → 질량 · 게이지 두께 · 식 (1) 기공 (다섯 자리) · 밀도 → SEM/EDS · XCT (조립 전 원판) → 셀 조립 (LPSCl 100 mg 펠릿 250 MPa · 양극 '같은 하중' · Li-In · 토크 11 N m ≈ 68 MPa) → 60 °C 율속 25 사이클 · GITT (C/20) · GITT 이완마다 EIS.

### 4-2. ★ DEM 제조 사슬 — 무엇을 어떻게 표현했나 (사용자 질문 ④)

- **힘 (식 4–11 · 렌더 확인)**: F_ij = F^{LJ,SF} + F^{GH} · 12-6 LJ U = 4ε[(σ/r)¹² − (σ/r)⁶] (r < r_c) 를 *shifted-force* 로 (U^{SF} = U(r) − U(r_c) − (r − r_c)·dU/dr\|_{r_c} · r ≥ r_c 에서 0 — 힘이 끝에서 0 으로) · Hertz + 접선 이력 **F^{GH} = √δ · √(R_iR_j/(R_i + R_j)) · [(K_n δ n_ij − m_eff γ_n v_n) − (K_t Δs_t + m_eff γ_t v_t)]** · δ = R_i + R_j − r · m_eff = m_i m_j/(m_i + m_j) · 접선력 ≤ μ 법선력 (Coulomb · LAMMPS `xmu`) · Hertz 는 겹칠 때만 · Silbert 2001 [34].  **K_n · K_t · γ · μ · ε · σ · r_c 값 = Table S1 [미확인]** — 저자는 [35] 값을 그대로 썼다고 적는다 (p.16 · p.18).
  - 정본 카드 `alabdali2023` §4-4 (= [35] SI 표) 의 건조 상태 값: k_n = 100 pg µm⁻¹ µs⁻² (= 1 × 10⁵ Pa · 우리 DEM E_eff 1.35 GPa 의 ≈1/13,500) · 마찰 X_µ = 12.5 · ε_AM = 100 × d_AM · ε_SE = 200 × d_SE · *"ε/kT ~ 10⁸ 이므로 건조 전극에서 열운동은 무의미"* (그 카드의 산술).  ⇒ 같은 값이라면 이 논문 모델의 **접촉 강성 · 점착은 재료 물성이 아닌 재매개변수화 값**이고 **열욕 298 → 353 K 는 건조 동역학에 사실상 영향이 없다** [추정 — 이 PDF 의 Table S1 은 못 봤다].
- **슬러리 → 건조**: CBSA (탄소 + 바인더 + 용매의 유효 입자 · Xu 2023 [36] · Ngandjong 2021 [37] 틀) 를 순간에 CBD (탄소 + 바인더 + 풀리지 않은 나노 기공의 유효 다공 상) 로 줄이고, 상자 높이를 정한 값으로 줄여 '용매 제거 + 전극 수축' 을 표현 — 작은 CBD 가 덩어리 모양 분포를 만들어 EDS 의 CBD 뭉침 (Figure S1 [미확인]) 과 *"qualitatively consistent"*.
- **가압 (CUP · WIP)**: 둘 다 **윗벽 z 변위 제어** · x · y 주기 (측방 치수 고정 = 실험의 면내 변화가 *"negligible"* 이라는 관찰 · 수치 없음) · **측방 하중 없음** · 외부 압력 지정 없음 (저항은 접촉 · 재배열에서만).  ⇒ **등방 (hydrostatic) 하중은 모델에 없다** — 저자 스스로 WIP 모델은 *"reproduced the experimentally observed through-thickness densification together with the prescribed thermal and loading history … rather than explicitly resolving the macroscopic hydrostatic stress field acting on the complete electrode disk"* (p.14).
- **'온간'**: 온도 의존 물성 변경이 **없다** (p.19) → 모델 WIP 와 CUP 의 차 = **명목 목표 (30 vs 20 %) + 목표 두께 4 ms 유지 + (열욕 온도)**.  저자의 *"The principal distinction … was therefore the combined use of elevated-temperature compression and a subsequent high-temperature holding stage … rather than a difference in prescribed pressure or interaction parameters"* (p.20–21) 는 목표 차를 빠뜨린다.
- **RVE 해석** (p.19): 디스크 안 임의 면내 자리의 두께 방향 RVE (CC 포함 · 디스크 중심 · 가장자리 아님) · 주기 경계 = 미세구조의 연속 · z 압축 때 면내 응력은 입자 상호작용 · 주기 망으로 생긴다.

### 4-3. ★ 3D 기계-전기화학 FEM (사용자 질문 ⑥ · p.21–25)

**구성 · 경계** [인쇄]: COMSOL Multiphysics · CUP · WIP 메시를 따로 가져옴 · 반쪽 셀 = **Al CC + NMC622 복합 양극 미세구조 + SE 분리막 + Li 금속 상대전극** (실험은 Li-In · 모델 전위창은 Li/Li⁺ 로 환산) · 두 모델에 **같은 고유 물성 · 전기화학 매개변수 · 운전 조건 · 경계조건**, 기하만 다름 · C/10 정전류 **5 사이클** 모의 (그림은 첫 사이클) · C/2 는 깨끗한 구조 첫 사이클 · UPJV MatriCS 노드 하나 (**1000 GB RAM · 64 코어**) · 실행 시간 · 메시 크기 [미확인].

| 식 | 내용 (렌더 확인) | 표지 |
|---|---|---|
| (12) | ∂c/∂t + ∇·J = 0 (AM 안 Li⁺ 보존) | p.22 |
| (13)–(14) | J = −(Dc/RT)∇μ · **μ = μ₀ + RT ln X − Ωσ_h** · σ_h = tr(σ)/3 | p.22 |
| (15)–(16) | J = −D(∇c − (c/RT)∇(Ωσ_h)) → ∂c/∂t − D∇²c + (D/RT)∇c·∇(Ωσ_h) + (Dc/RT)∇²(Ωσ_h) = 0 (응력-농도 양방향 결합) | p.22 |
| (17)–(18) | η = φ_s − φ_e − E_eq · **E_eq = −μ/F = [−(μ₀ + RT ln X) + Ωσ_h]/F** (국소 응력이 평형 전위 · 과전압을 옮긴다) | p.23 |
| (19) | ∇·σ + F_b = 0 · **F_b = 0** · 적층압 **68 MPa** 를 경계조건으로 | p.23 |
| (20)–(21) | σ = C : ε_e (Hooke · **AM · SE · CBD 모두 선형 탄성**) · ε_t = ε_e + ε_int = ½((∇u)ᵀ + ∇u) | p.24 |
| (22)–(24) | **ε_int = (1/3) Δc Ω I** (등방 고유변형 · 열팽창과 같은 꼴) · Ω = 3λ / ((x − x₀) C_total) · λ = (ΔV/V₀ + 1)^{1/3} − 1 = (V_x/V₀)^{1/3} − 1 · ΔV = Koerver 2018 [3] 의 NMC622 부피 변화 (탈리튬에서 잰 값을 리튬화에도 가역으로 · Figure S2 [미확인]) | p.24–25 |

- **역학 경계** [인쇄 p.25]: 분리막 · CC = 3D **강체** (NMC 부피 변화에 의한 변형 무시) · Li 금속 = 처음부터 **2D 경계** (역학에서 제외) · CC 바깥면 **완전 구속** · 측면 = **고정 벽** (셀 외피의 측방 구속) · Figure S3 [미확인].  ⇒ 응력 계산은 양극 (AM · SE · CBD) 안만.
- **입력** [인쇄 p.25]: OCV = GITT 각 90 min 이완 끝 준평형 전위를 SOC 로 보간 (Figure S4) · Li-In → Li/Li⁺ **+0.65 V** · D (NMC622) · j₀ = §2.2 실험값 · 나머지 물성 · 수치 = **Table S2 · S3 [미확인]** — **E · ν (AM · SE · CBD) 는 본문 어디에도 없다** (본문 'GPa' 는 Fig. 8e 색 막대뿐).
- **명시 안 된 것** [미확인]: 상 사이 계면 조건 (완전 접합인지) · 기공 영역의 역학 처리 · SE · CBD 의 전하 보존식 · Butler–Volmer 꼴 · 분리막 두께 · 어느 양극에서 잰 j₀ · D 를 두 모델에 공통으로 넣었는지 · 메시 수렴.
- **제조 잔류 응력**: DEM 에서 넘어오지 않는다 (기하만 · p.21) — 서론은 *"Manufacturing can additionally introduce residual stresses"* (p.3) 라 적지만 모델의 출발 상태는 응력 0.

### 4-4. ★ 입자 처리 (우리 축 언어로)

- **DEM**: 거친 입자 **구** (AM · SE · CBD) · Hertz 탄성 접촉 (겹침 δ) + LJ 점착 + 마찰 · **접촉 소성 없음 · 형상 소성 없음 · 파괴 없음** · CBD = 유효 다공 입자 (내부 기공 50 %) · '등방' · '온간' = 표현 안 됨 → 실험 WIP 의 더 치밀한 상태를 **더 깊은 목표 변위 + 유지**로 낸다 (치밀화 = 재배열 + 겹침).
- **넘김**: 0.2 µm 복셀 → 메시 — 겹친 구의 공통 부피는 한 번만 세어진다 (복셀 기하의 성질 [추정]) · 계면 = 복셀 면.
- **FEM**: 복셀 기하 위 선형 탄성 연속체 · AM 에만 리튬 고유변형 · SE 항복 · 계면 박리 · 균열 없음.
- **우리 대응**: DEM = 강체 구 + hooke/hysteresis 접촉 (δ = 소성 대리 · 연화 E_eff 1.35 GPa) · MPM = SE J2 소성 (E 1.53 · ν 0.49 · σ_y 0.30 GPa · AM = 고정 장애물) · STEP3 = MPM 상 복셀 위 FV σ.  ⇒ 그들 DEM ≈ 우리 DEM (형상 불변) · 그들 FEM ≈ "우리 MPM 에서 소성을 빼고 AM 을 탄성체로 · 리튬 팽창을 넣은 것" 에 가깝다.

### 4-5. 기법 미니 용어집
- **CUP / WIP / CIP / HIP**: cold uniaxial / warm isostatic / cold isostatic / hot isostatic pressing — 등방 = 유체 매체로 사방에서 같은 압력 (편차 응력이 거시적으로 0) · 단축 = 다이 안 한 축 (측벽 마찰 · 측압 계수 K₀ < 1).
- **CGMD (coarse-grained MD)**: 입자 하나가 실제 입자 (또는 덩이) 하나를 대신하는 거친 입자 동역학 — Franco 그룹은 LAMMPS 로 슬러리 · 건조 · 압연을 푼다.
- **CBSA / CBD**: carbon-binder-solvent aggregate (슬러리) / carbon-binder domain (건조 뒤 다공 상).
- **lj/sf · gran/hertz/history**: LAMMPS 쌍 퍼텐셜 — 끝에서 힘이 0 이 되게 민 LJ · 접선 변위 이력이 있는 Hertz 입자 접촉.
- **NPT/sphere**: 회전 자유도가 있는 구 입자의 등온 · 등압 앙상블.
- **GeoDict · SNOW2 (PoreSpy)**: 복셀 미세구조 해석 상용 도구 · 기공 공간을 기공 · 목 망으로 나누는 분할 알고리즘.
- **INNOV**: Franco 그룹의 미세구조 생성 · 메싱 도구 [38] (복셀 기반 다상 메싱 [39]).
- **고유변형 (eigenstrain)**: 응력 없이 생기는 변형 (여기서는 Li 농도 변화에 의한 부피 변화) — 구속되면 응력이 된다 (열응력과 같은 꼴).
- **화학-기계 퍼텐셜 μ**: μ = μ₀ + RT ln X − Ωσ_h — 인장 (σ_h > 0) 이 μ 를 낮춰 Li 가 인장 쪽으로 흐르고 평형 전위가 Ωσ_h/F 만큼 오른다.
- **Weppner–Huggins GITT**: 펄스 전류의 전압 계단으로 겉보기 확산계수를 낸다 (구형 입자 반지름 r_p 를 가정).
- **R_ct → j₀**: 선형화한 Butler–Volmer R_ct = RT/(zFAj₀) — 면적 A 를 무엇으로 두느냐에 따라 j₀ 가 바뀐다 (그래서 *"apparent"*).
- **Li-In 환산**: 이 논문 +0.65 V (Li-In → Li/Li⁺).

---

## 5. Figure set ★ (크롭 11 장 = `litdb/figures/benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 작업 흐름 — 입력 (조성 · 밀도 · 온도 · PSD) → 전극 제조 (CUP 25 °C 다이 · 축 압력 / WIP 80 °C 강체 챔버 · 액체 매체 · 밀봉 봉투 · 정수압 · 강체 지지) → 같은 셀 구성 → 구조 (SEM · X-CT) · 전기화학 (율속 · GITT · EIS) → DEM (슬러리 · 건조 · 압축 두 판) → 미세구조 → FEM (SOC 지도 · 응력 지도) | 사슬 위상 한 장 · ⚠ 구조 상자의 *"tortuosity, phase distribution"* 은 실험에서 재지 않았다 (XCT = AM 만) |
| 2 | DEM 사슬 스냅샷 — 평형 슬러리 57.62 µm → 건조 51.94 → CUP 298 K 41.55 → 제하 45.71 / WIP 353 K 36.36 → 제하 37.40 µm (측면 41.25) | ★ 회복 산술 (CUP 40.0 % · WIP 6.7 % 의 부과 감소 · ρ 10.0 · 2.9 %) · 밀도 = 두께와 같은 정보 (§3-8) |
| 3 | (a) 1 · 10 · 15 · 20 · 25 사이클 충 · 방 곡선 (b) 방전 용량 + CE vs 사이클 (C/10 → 1C) (c) 충전 GITT D vs 전위 (d) 방전 D (e) 사이클 전 Nyquist (f) 첫 사이클 뒤 Nyquist + 등가회로 (g) 충전 R_ct (h) 방전 R_ct (캡션 = 제목 한 줄뿐) | §3-4 율속 표 · §3-6 표 3 ↔ 3f 대조 (WIP 호가 크다) · 3h CUP 이 낮다 |
| 4 | (a) 단면 SEM + 두께 표기 50.10 · 47.77 · 36.35 µm (b) EDS 겹침 지도 (범례 S · Cl · P · Ni · O · C · Al) | 정성 치밀화 · ⚠ 캡션 원소 목록 불일치 (§10-18) · WIP AM 안 어두운 선 (정성) |
| 5 | XCT — (a) 세로 · 면내 단면 (두께 표기 CUP 54.5 · WIP 37.72 µm) (b) AM 분할 3D (c) 세로 합 투영 (d) 면내 합 투영 (e) 열마다 최대 세로 거리 지도 (f) 그 히스토그램 | 두께 정의 셋째 · 국소 두께 분포 (CUP 꼬리) · 캡션 *"Figure 2e"* 오기 |
| 6 | DEM 두께 방향 상 분율 (기공 · AM · CBD · SE) — ⚠ 패널 제목 *"a) WIP · b) CUP"* ↔ 캡션 *"(a) CUP and (b) WIP"* | ★ §10-15 판정 = 캡션이 맞다 (패널 a = CUP) · 상 분율 평균 판독 (§3-9) · 벽 근처 기공 → 1 |
| 7 | (a) AM–SE · AM–CBD 비계면적 (b) 기공 지름별 부피 분율 (c) 유효 이온 · 전자 전도도 (d) 상대 유효 확산 + *"Tortuosity factor"* 축 (e) 기공률 (f) 두께 감소 (g) 밀도 — DEM ↔ 실험 (h) SNOW2 기공-목 망 | ★ f = D_eff/D₀ · τ 규약 대조 (§7-3) · σ_SE 함축 0.125 mS/cm · 7d 축 단위 · 이름 문제 (§10-16) |
| 8 | (a) C/10 첫 사이클 모의 ↔ 실험 (b) C/2 모의 (첫) ↔ 실험 (20 번째) (c) 탈리튬 끝 국소 용량 (d) 탈리튬 90 % 전해질 전류 밀도 3D + 가운데 YZ 단면 (e) 탈리튬 끝 AM 정수압 응력 3D + YZ 단면 — C/2 · C/10 × WIP · CUP · 공통 색 | ★ 구조만의 율속 차 (≈11 vs 실험 ≈15 mAh/g [판독]) · 응력 '차 작다' 의 근거 = 이 그림뿐 (EM-06) · ⚠ 크롭 위쪽에 본문 한 낱말 (*"increases."*) 이 들어가 있다 (크롭은 그대로 둠) |
| Table 1 | 두께 · 두께 감소 · 기공 · 기공 감소 (미가압 · CUP · WIP) | 크롭 `tab_1.png` = 9 · 10 쪽 이어 붙인 판 (표가 p.9–10 에 걸침 · 11-06 손 작업 · figures.json `manual_crop`) · 값은 §3-3 |
| Table 2 | 겉보기 밀도 1.59 · 1.81 · 2.20 ± 0.04–0.06 g/cm³ | §3-3 · §10-6 골격 밀도 산술 |
| Table 3 | EIS R0 · R_int · R_ct (사이클 전 · 첫 사이클 뒤) | §3-6 · §10-9 |

## 6. Post-processing ★

- **저자가 한 것**: 식 (1) 기하 기공 (다섯 자리) · 게이지 · SEM · XCT 두께 · XCT AM 분할 → 합 투영 · 열별 최대 거리 지도 (자체 Python) · GITT Weppner–Huggins (r_p 5 µm · 준평형 구간만) · EIS RelaxIS 등가회로 → R_ct(전위) → 겉보기 j₀ · DEM → 0.2 µm 복셀 → GeoDict (비계면적 · 기공 지름 분포 · σ_ion,eff · σ_e,eff · 상대 유효 확산 · 'geometric tortuosity' · 기공률) · PoreSpy SNOW2 (0.6 µm 문턱) · INNOV 메시 → COMSOL 장 (국소 용량 · 전해질 전류 · AM σ_h) 지도.
- **안 한 것**: DEM 접촉력 · 힘 사슬 · 응력 (명시 제외) · 제조 잔류 응력 넘김 · 응력 분포 · 분위수 · 상별 응력 · SE 응력 · 압력 판독 (DEM) · 복셀 (0.2 µm) · 메시 수렴 · DEM 반복 · 셀 반복 · 오차 막대 · 성분 밀도 공개 · '등방' 하중 모의 · 온도 효과 분리 팔 (유지만 · 온도만 · 목표만) · 같은 압력 단축 ↔ 등방 실험.
- **우리 후처리 (이 카드)**: Fig. 2 치수 → 회복 · ρ · 밀도 × 두께 · Fig. 6 색 화소 디지털화 (matplotlib 기본 네 색 분류 · 범례 영역 가림 · 열마다 중앙값 → 두께 평균 · 패널 합 1.00 확인) → 상 분율 · 골격 밀도 함축 · 판정 (§10-15) · Fig. 7 마커 판독 (7d 판독 0.0600 · 0.1284 · 2.579 · 1.762 = 인쇄값 재현) · Fig. 3 · 8 곡선 · 막대 판독 · 실험 (1 − ε) × 두께 · ρ/(1 − ε) · 문헌 밀도 골격 · 면적당 질량 · EIS 합.
- **[우리 산술] τ · f · 기공 규약 대조** (우리 τ 명명 규약 — 메인 리포 CLAUDE.md τ 절 · `docs/reviews/tau_conventions_judgment_v2_20261003.md`):
  - f (= σ_eff/σ₀ = D_eff/D₀) = **0.060 (CUP) · 0.128 (WIP)** — 같은 SE 망이면 이온 σ 비와 같아야 하고 실제로 Fig. 7c 이온 비 ×2.13 과 같다.
  - **tau2 (수송 tortuosity) = φ_SE/f** — φ_SE 를 Fig. 6 판독 (두께 평균 0.26 · 0.32 · bulk 0.28 · 0.31) 으로 두면 **≈4.3–4.7 (CUP) · ≈2.4–2.5 (WIP)** · √ (= tau) ≈2.1–2.2 · ≈1.6.
  - 인쇄 τ (2.58 · 1.76) 는 tau2 (φ/f) 꼴과는 맞지 않고 √(φ/f) 꼴에 가깝다 (≈1.1–1.2 배) · τ² × f = 0.40 이 두 침대에서 같다 — 상자 기준 SE 분율 (0.26–0.32 · 두 침대 다름) 로는 안 나오고, 고체 중 SE 몫 (Fig. 6 판독 ≈0.46 · 두 침대 같음) 에 가깝다.  같은 그룹 Alabdali 2023 은 τ = √(η/D_eff) 로 셌다 (정본 카드 alabdali2023 §3-2 · 인쇄값 재현) ⇒ 이 논문 'geometric tortuosity' 의 정의 [미확인] · 우리 쪽 이름 = τ_geo 로 단정하지 않는다.
  - σ_ion,eff / f = **0.125 mS/cm** → 이온 계산의 SE 고유 σ (원문 입력값 없음).
- **[우리 산술] 참고 — 비계면적의 크기**: AM 을 Ø10 µm 구 · ρ 4.7 g/cm³ (가정) 로 두면 AM 비표면 ≈0.128 m²/g_AM → AM–SE 0.049 · 0.060 m²/g 가 'AM g 당' 이면 피복 ≈38 · 47 %, '전극 g 당' 이면 ≈56 · 68 % — 분모 [미확인] · 복셀 면 기반 넓이 추정 (추정기 [미확인] · 면 세기면 등방 ≈1.5 배 과대 — 정본 카드 lindblad2005 · comparison_vs_ours_DEM §B-Rint) ⇒ **값보다 WIP/CUP +22 % 만** 안전.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 — 우리 수치는 메인 리포 출처를 병기해 적는다)

### 7-1. 비교표

| 항목 | 이 논문 | 우리 (메인 리포 출처) | 같음 / 다름 · 왜 |
|---|---|---|---|
| SE | LPSCl (POSCO) · 입도 [미확인] | LPSCl | 같은 SE 화학 (할라이드 전이 문제 없음) · 입도 비교 불가 |
| AM | NMC622 · r_p 5 µm (공급사) · DEM 구 · FEM 선형 탄성 + 고유변형 | NMC811 강체 구 (DEM) · MPM 고정 장애물 | AM 응력 · 팽창은 그들 FEM 만 푼다 (우리 MPM AM = 강체) |
| 공정 · 조성 | 습식 · PVDF-HFP + Super P · 69 : 27.6 : 3.4 · 건조 기공 34 % (보고) | 건식 분말 압밀 (VGCF/PTFE 첨가 침대 · ps45 = 탄소 · 바인더 없음 81.6 wt%) | 출발 상태가 다르다 (테이프 vs 분말) — 기공 절대값 교차 인용 금지 |
| DEM 코드 · 접촉 | LAMMPS lj/sf + gran/hertz/history · k_n ≈1 × 10⁵ Pa 꼴 (정본 alabdali2023 · Table S1 [미확인]) · LJ 점착 | LIGGGHTS hooke/hysteresis · E_eff 1.35 GPa (SE) · AM 140 GPa (CLAUDE.md frame [2]) | 둘 다 형상 불변 · 그들은 재매개변수화 (물성 아님) · 우리는 연화된 물성 스케일 |
| 압축 제어 | **변위 제어** (목표 20 · 30 %) · 압력 판독 없음 | **하중 제어** (300 MPa 도달 → 판 고정 이완) (`docs/effective_modulus_stress.md` §2-1) | 그들은 두께를 맞추고 우리는 압력을 맞춘다 → 그들 응력 상태는 주장이 아니다 |
| 등방 · 온도 | 표현 없음 (x · y 주기 · 측방 하중 없음 · T 의존 물성 없음) | DEM · MPM 둘 다 온도 인자 0 · 판 하나 (`docs/temp_pressure_capability.md` §4 표) | **같은 한계** — WIP 의 '등방 · 온간' 은 두 쪽 모두 못 낸다 |
| 제하 · 회복 | DEM 제하 있음 · ρ CUP 10.0 % · WIP 2.9 % [우리 산술] · 최종 두께를 실험에 맞춤 | DEM 언로딩 등록 (`docs/reviews/dem_unloading_ps45_prereg_20261009.md` — ρ = (h(P_meas) − h₀)/h₀ · P_meas 1 MPa · 실험 두께 = 하중 뺀 뒤) · MPM `--save-state` / `--load-state` (F 이력 · `scripts/mpm3d_compaction.py:114`) | 같은 정의의 ρ — 그들 값은 모델 안 · 보정에 흡수 (§8 EM-02) |
| 기공 규약 | 보고 DEM 26.5 · 15 % ↔ Fig. 6 평균 0.43 · 0.31 [판독] ↔ 질량 보존 환산 (§3-8) · 실험 식 (1) 밀도 [미확인] | ε_sphere (구 부피 합 · 질량 보존) ↔ ε_union (겹침 한 번) · real_14 차 1.251 %p (CLAUDE.md scaffold 절 08-12 정정) · 진밀도 1.64 ↔ 1.86 표지 (comparison_vs_ours_DEM §A) | 같은 부류의 함정 — 정의 없는 기공 일치는 인용하지 않는다 |
| 수송 해법 | GeoDict 복셀 0.2 µm 연속체 (접점 = 복셀 융합 · 협착 항 없음) | 접촉망 Kirchhoff + Holm 1/(2σa) (`scripts/network_conductivity.py`) · STEP3 복셀 FV = CONTACT_FREE 가지 (CL-81 · `docs/voxel_contact_free_gap.md`) | 그들 값 = 우리 STEP3 와 같은 CF 부류 (상한 쪽) · 접촉망 FULL 과 비교 금지 |
| f · tau2 | f 0.060 · 0.128 · tau2 ≈4.3–4.7 · 2.4–2.5 [우리 산술] · σ_SE 함축 0.125 mS/cm | ps45 Hertz FULL tau2 5.03–7.24 · 협착 뺀 CF 1.25–1.79 · 협착 전력 몫 73–75 % (`docs/data/ps45_r45_network_g2_20261007/README.md`) | 그들 CF 꼴 값이 우리 CF 와 FULL 사이 — 조성 · CBD · 기공이 달라 크기 해석 금지 |
| 응력 해법 | COMSOL 선형 탄성 (AM · SE · CBD) + AM 고유변형 · 적층압 68 MPa · 측벽 고정 · 항복 · 박리 없음 · 물성 [미확인] | MPM J2 (E 1.53 · ν 0.49 → K 25.5 GPa ≈ DFT B₀ 26.23 · μ 0.51 · σ_y 0.30 GPa) · DEM Love–Weber (정성 · 상대) (`docs/effective_modulus_stress.md` §1 · §2-4) | 그들은 AM 응력 · 사이클 (탄성 상한쪽) · 우리는 SE 소성 · 압밀 (편차 상한 σ_y) — 겹치는 양은 정수압 (둘 다 상한 없음) |
| 사이클 기하 | 결합 FEM 이 Li 농도로 AM 부피를 계속 바꾼다 (Koerver ΔV) | MPM A-1 `--cycle-deform` (충전 상태 하나 · SC −5.1 % / poly +5.9 % × 0.30 · `scripts/mpm3d_compaction.py:855`) · A10 접촉 장부 (`scripts/cycle_contact_ledger.py` · Bucci CZM) · STEP4 BV + 구형 확산 (역학 결합 없음 · `scripts/step4_dyn.py`) | 그들이 앞선다 (응력 ↔ 전기화학 양방향) · 우리는 SE 소성 · 접촉 개구가 있다 |
| 겉보기 D (GITT) | 8 × 10⁻¹² cm²/s = 8 × 10⁻¹⁶ m²/s (WIP 탈리튬 · r_p 5 µm · 60 °C [미확인]) | STEP4 D_s^poly 4 × 10⁻¹⁵ m²/s (Chen 2020) · 현 기본 3 × 10⁻¹⁴ (Kang&Shin FEM 입력) (`docs/ncm_sc_poly_electrochem_anchors.md`) | 그들 값이 1/5 · 1/37 — 복합체 겉보기 값 (SE 수송 · 접촉 포함) · NMC622 · 60 °C · 정의 차 → 후보 기록만 |

### 7-2. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 공정 사슬 (슬러리 → 건조 → 압축 → 제하) 의 기하 · 복셀 수송 (CF 부류) · **AM 사이클 응력 ↔ 전기화학 양방향 결합** · 율속의 구조 기원 (첫 사이클).
- **없는 것**: 접촉 단위 협착 (Holm) · SE 소성 (형상 변화 · 기공 메움) · 계면 박리 · 균열 · 등방 하중 · 온도 물성 · 압력 판독 · 잔류 응력 · 실험 독립 검증점 (두께 · 밀도는 보정과 같은 정보).
- **우리 쪽이 줄 수 있는 것**: DEM = 압력 제어 압밀 (116 · 400 MPa 같은 압력 축) · 접촉망 FULL σ (협착 포함) / MPM = SE 소성 · 기공 메움 · 정수압 (실제 K) · 잔류 F 이력 (`--save-state`).  ⚠ 둘 다 등방 · 온도가 없어 *"WIP 가 등방이라 좋다"* 는 우리도 시험하지 못한다.

### 7-3. τ 명명 규약 대조 (우리 규약 · CLAUDE.md τ 절)
- 그들 Fig. 7d 축 *"Tortuosity factor"* = 본문 *"geometric tortuosity"* 2.58 · 1.76 — 우리 규약에서 'tortuosity factor' 는 **τ² (tau2) 전용**이라 이 축 이름을 그대로 옮기지 않는다.
- 우리 표로 옮기는 형태: `f_ion` (= D_eff/D₀) 0.060 · 0.128 · tau2 (수송 tortuosity · φ/f · φ 기준 = Fig. 6 판독) ≈4.3–4.7 · 2.4–2.5 [우리 산술] · 인쇄 τ 는 '정의 미확인 τ (√ 꼴에 가까움)'.
- 협착 배수 (τ_FULL/τ_CF) 는 이 논문에서 낼 수 없다 (FULL 가지가 없다).

### 7-4. 압력 이력 · 언로딩 (메인 리포 DEM 우선 Ⓐ)
- 실험 이력: CUP 116 MPa (30 s) → 조립 '같은 하중' (≈250 MPa [추정]) → 68 MPa 적층 / WIP 400 MPa 등방 (5 min · 80 °C) → 조립 '같은 하중' → 68 MPa · 측정 두께 = 조립 전 · 하중 없음.
- 모델 이력: 변위 20 · 30 % → 제하 (압력 모름) → FEM 은 응력 0 에서 68 MPa 경계로 시작.
- 우리 생산 DEM 상태 (300 MPa 도달 · 판 고정 이완) 는 이 둘 어느 쪽에도 없다 — 언로딩 등록 (하중을 뺀 상태 · P_meas 1 MPa) 이 그들의 '제하 뒤 두께 비교' 와 같은 자리다.

### 7-5. 이 비교를 읽을 때의 한정어
- 강체 구 DEM (δ = 접촉 대리) ↔ 소성 연속체 MPM ↔ 선형 탄성 연속체 FEM — 세 모델의 응력은 서로 다른 상한을 갖는다 (DEM 탄성 · MPM σ_y · FEM 무한).
- 우리 E_eff 1.35 (DEM) · 1.53 GPa (MPM) 는 실제 E_SE ≈ 22–24 GPa 를 연화한 대리값 (재배열 · 입계 미끄럼을 뭉친 것) · ~20 % 는 소성 흐름 없는 강체 구의 기공 바닥 — 그들 DEM 은 겹침 · 재배열로 보고 15 % 까지 내지만 정의가 불분명하다.
- 소재: LPSCl 같음 · NMC622 ↔ NMC811 · 습식 ↔ 건식 · 2D/3D 해당 없음 (둘 다 3D) · [판독] ≠ [인쇄].

---

## 8. ★★ 우리 연구에 주는 insight (EM-01 – 07 · DEM ↔ MPM 응력 · 등압 압축의 효과)

### 8-0. EM 질문 기록 (`docs/effective_modulus_stress.md` §4) 에 주는 답 · 반례 · 앵커 후보 — 반영은 메인 세션

| EM | 우리 질문 | 이 논문이 주는 것 | 답 · 반례 · 앵커 후보 |
|---|---|---|---|
| EM-01 | 유효 영률로 누른 응력은 1/20 이라 못 쓰나 | DEM 응력 · 힘 사슬은 출력에서 뺐다 (p.19) · 응력은 COMSOL 선형 탄성 + AM 고유변형 = **변형 제어** 영역 | **반례 (영역 경계)** — 고유변형 응력은 σ ∝ E 라 우리 §1 의 "하중 제어 → 응력 = 경계조건" 이 **사이클 응력에는 서지 않는다** · 연화 E 로는 사이클 응력 크기를 못 낸다 · 그들 E [미확인] → 앵커 아님 · §1 표에 '사이클 (고유변형) 응력' 행 후보 |
| EM-02 | 언로딩 탄성 회복이 연화 E 때문에 과대인가 | DEM 제하 있음 — ρ CUP 10.0 % · WIP 2.9 % (부과 감소의 40.0 · 6.7 %) [우리 산술 · Fig. 2] · 실험은 눌린 두께를 재지 않았다 · 목표 20 · 30 % 로 최종 두께를 맞춤 · 접촉 상수 = 재매개변수화 | **앵커 아님** (회복이 보정에 흡수됐다 · E 가 아니라 점착 · 마찰 · 유지 시간이 정한다 [추정]) · 손잡이 후보 = **같은 건조 침대에서 '더 깊은 목표 (30 %) + 4 ms 유지' 가 ρ 를 10.0 → 2.9 % 로** (둘이 섞여 유지 몫은 분리 안 됨 — 같은 그룹 Qin 2026 에서는 압축이 깊어지는 것만으로도 회복 비가 25–28 → 11–14 % 로 준다 · 온도 효과는 무의미 가정 [추정]) → 우리 언로딩 등록에서 이완 (PHASE 4) 길이 · 출발 압밀 깊이를 기록 칸으로 |
| EM-03 | AM ↔ SE 하중 분담을 실제 강성 · 소성에 맞게 | 상별 응력 · 분담 보고 없음 · FEM 물성 [미확인] | 답 없음 |
| EM-04 | DEM 에서 SE 응력이 σ_y 를 넘는 몫 | SE 응력 지도 없음 (AM 만) · AM 접점 σ_h ≥ 3–4 GPa (색 포화 [판독]) | 답 없음 · 경고: 항복 상한 없는 선형 탄성 모델의 접촉 목 응력은 LPSCl σ_y (0.05–0.30 GPa) 의 10 배를 쉽게 넘는다 — 그 값으로 SE 를 판정하지 않는다 |
| EM-05 | 이완 끝 판 압력이 목표보다 낮다 — 같은 300 MPa 상태로 비교 | DEM 은 변위 제어 · 압력 판독 없음 · FEM 은 68 MPa 경계로 시작 | 대조 — 압력 상태를 주장하지 않고 두께를 맞춘 설계 (우리는 압력을 맞춘다) · 답 아님 |
| EM-06 | MPM 응력장을 같은 조건에서 재현성 있게 | Fig. 8e = AM · 가운데 YZ 단면 한 장 · 공통 색 −2 … +4 GPa (위 끝 포화) · 분위수 · 평균 없음 → *"less pronounced"* 는 시각 판정 | **반면교사** — 우리 §3 재현 조건 (상별 분위수 · 실측 분위수 천장 · 포화 몫 · SELF-45) 이 옳은 쪽 · `/emod` 에 '색 포화 몫' 칸 후보 |
| EM-07 | 언로딩을 MPM 도 DEM 과 같은 절차로 | FEM 은 제하된 DEM 기하에서 **응력 0** 으로 출발 (잔류 응력 미전달 · p.21) · FEM 제하 · 재가압 없음 | 선례 아님 · 우리 `--save-state` / `--load-state` (F 이력) 가 한 칸 앞 · 짝 설계 때 "잔류 응력을 넘길지" 를 결정 항목으로 · 그들의 "WIP ↔ CUP 응력 차 작다" 는 잔류 응력 없는 출발 상태의 결과 |

**8-1. ★★ 이 모델의 'WIP 효과' = 더 깊이 누르고 유지한 단축 압축 — '등방성' 은 실험에서도 모델에서도 분리되지 않았다.**
- 논문: DEM 은 같은 물성 · z 변위만 · x · y 주기 · 측방 하중 없음 · 온도 의존 물성 없음 (p.19) · WIP = 목표 30 % + 4 ms 유지 / CUP = 20 % · 유지 없음.  실험은 400 ↔ 116 MPa · 80 ↔ 상온 · 5 min ↔ 30 s · 등방 ↔ 단축.  정본 카드 alabdali2023 의 건조 힘장 (ε/kT ~ 10⁸) 이 그대로라면 열욕 353 K 는 효과가 없다 [추정].
- 뜻: *"WIP 가 등방이라서 좋다"* 는 이 논문 자료로 주장할 수 없다 — 말할 수 있는 것은 *"더 치밀하게 누르면 (그리고 유지하면) 계면 면적 · 이온 경로 · 고율 이용이 좋아진다"* 까지 (결론의 *"advantages of the multidirectional compaction"* 은 과장 · §10-1).
- 우리: DEM · MPM 둘 다 온도 인자 0 · 판 하나 (`docs/temp_pressure_capability.md` §4) — 같은 한계.  같은 그룹에 LIGGGHTS 등방 압축 선례 (`dem_mechanical_stresses_ssb_electrode_cycling` · 1/3/5 MPa) 가 있다 (이 논문은 인용 안 함).
- 할 일 (1저자): 등방 압축이 과제에 필요해지면 **'같은 평균 응력 · 단축 ↔ 등방' 두 팔을 먼저 등록** (압력 크기를 같게 · 측벽 서보) — 지금 필요는 없음.

**8-2. ★★ DEM ↔ MPM 응력의 분업 — 이 논문은 frame[5] 를 지지하지만 그 연속체에는 소성이 없다.**
- 논문: DEM = 기하만 (응력 출력 제외) · 응력 = 연속체 FEM.  우리 frame[5] (DEM = 수송 · MPM = 역학) 와 같은 선택이다.
- 다른 점: 그들 연속체는 **선형 탄성 + AM 고유변형** (AM 응력 · 사이클) / 우리 MPM 은 **SE J2 소성 + AM 고정** (SE 흐름 · 압밀).  두 모델이 함께 '실제 값' 에 가까운 양은 **정수압** 하나다 — 둘 다 부피 탄성률이 실물 크기 (우리 K 25.5 GPa ≈ DFT B₀) 이고 J2 는 정수압을 막지 않는다 (`docs/effective_modulus_stress.md` §2-4 *"정수압에는 상한이 없다"*) [추정].  그들이 σ_h 를 고른 것은 우리 MPM 판독기 (EM-06 (나)) 의 첫 불변량으로도 맞다.
- 할 일: MPM 응력 판독기를 만들 때 SE σ_h (p) 분포를 먼저 · AM σ_h 는 우리 MPM 에 없다 (AM = 강체) — 사이클 AM 응력이 필요하면 그들 같은 FEM 단계가 따로 있어야 한다 (frame[5] 의 빈칸으로 적기).

**8-3. ★ 두께 · 밀도 '일치' 는 검증이 아니라 보정이다 — 남는 독립 대조는 정의가 불분명한 기공 하나.**
- [우리 산술]: 건조 상자 높이 51.94 µm 는 부과한 값 · DEM 밀도 × 두께 = 82.92 (세 상태 같음) → 밀도 일치 = 두께 일치 · 두께 감소는 목표 변위 (20 · 30 %) 선택의 결과 (선정 근거 미기재).
- 뜻: 우리 CLAUDE.md 의 scaffold 교훈 (*"씨앗이 정답을 인코딩한다 · porosity 는 독립 정보를 담지 않는다"*) 과 같은 구조 — 이 논문의 Fig. 7e–g 세 '검증' 중 둘은 같은 정보다 (frame[4]: 일치 = 교차검증이려면 독립이어야 한다).
- 할 일: 우리 언로딩 등록 · Ⓐ 실험 원측정 (같은 시료 질량 · 면적 · 두께 · 측정 압력 · 공극 정의) 에서 *"무엇을 맞추고 무엇을 남겨 둘지"* 를 미리 나눈다 — 이미 등록의 RB-01 (같은 기준 고체량) 과 같은 방향.

**8-4. ★ 기공률 — 한 논문 안에 DEM 기공이 세 값, 실험 기공은 계산 밀도가 비공개.**
- [우리 산술]: 보고 DEM 26.5 · 15 % ↔ Fig. 6 두께 평균 0.43 · 0.31 (bulk 0.38 · 0.27) [판독] ↔ 질량 보존 환산 (CUP 기준 WIP 10.2 % · WIP 기준 CUP 30.5 %) · 실험 (1 − ε) × 두께 = 54.0 µm (일정 ✓) 이지만 식 (1) 의 골격 2.41–2.47 g/cm³ 은 흔한 결정 밀도로 센 2.99–3.24 보다 25 % 낮다 → 그 밀도면 기공 40–44 · 27–32 % (CUP · WIP).
- 뜻: 이 논문의 *"DEM 15 % ↔ 실험 10.9 %"* 는 정의를 모르고는 일치도 불일치도 아니다.  우리 ε_sphere ↔ ε_union · 진밀도 1.64 ↔ 1.86 표지와 같은 함정.
- 할 일: 이 논문의 기공을 우리 표에 옮길 때 **'보고값 · 정의 미확인 · 골격 밀도 2.41–2.47 함축'** 표지를 붙인다 (압밀 앵커로 쓰지 않는다).

**8-5. 율속의 구조 기원 — 같은 j₀ · D 에서 구조만으로 C/2 차 ≈11 mAh/g (실험 ≈15 의 ≈3/4) [판독].**
- 논문: 이온 전류의 선호 경로 · 국소 미사용 AM (CUP) ↔ 퍼진 전류 · 고른 이용 (WIP).  C/10 첫 사이클 모의 방전은 실험보다 ≈10 % 크다 [판독] · C/2 비교는 저자 스스로 정성.
- 뜻: 우리 STEP4 (구조 → 율속) 와 같은 질문의 외부 사례 — '치밀도 · SE 망 연속성 → 고율 이용' 의 크기 감각 (첫 사이클 · 같은 동역학 · CF 부류 수송).  ⚠ 실험 차에는 R_ct 차 (충전 ≈1/17) 같은 동역학 차도 섞였다.
- 할 일: STEP4 결과를 문헌과 대조할 때 이 논문은 '구조만 바꾼 모델 차 ↔ 실험 차' 의 비 (≈0.75) 로만 · 절대 용량 비교 금지.

**8-6. GITT 겉보기 D — STEP4 D_s 의 ASSB 쪽 후보 점 하나 (채택 아님).**
- 논문: 8 × 10⁻¹² cm²/s = 8 × 10⁻¹⁶ m²/s (NMC622 · r_p 5 µm · WIP 탈리튬 가운데 전위).
- 우리: D_s^poly 4 × 10⁻¹⁵ (Chen 2020) · 현 기본 3 × 10⁻¹⁴ m²/s (`docs/ncm_sc_poly_electrochem_anchors.md`) → 1/5 · 1/37.
- 뜻: 복합체 GITT 겉보기 값 (SE 수송 · 접촉 · 온도 미기재) 이라 입자 고유 D 로 옮기지 않는다 — 앵커 표에 'ASSB 복합체 겉보기 · 60 °C [미확인] · NMC622' 후보 행으로만 (메인 세션 판단).

**8-7. EIS 는 '조립 직후 접촉' 차가 크고 한 사이클 뒤에는 뒤집힌다 — WIP 우위를 R0 · R_int 로 인용하지 않는다.**
- 논문 · [우리 산술]: 사이클 전 합 455 ↔ 87.5 Ω (CUP ↔ WIP) · 첫 사이클 뒤 79 ↔ 143 Ω (WIP R_int 114) · R0 는 ≈12 Ω 로 수렴 · 방전 R_ct 는 CUP 가 낮다 [판독].
- 뜻: 우리 Rint ② · 접촉 저항 앵커 후보로 쓰지 않는다 (두 전극 배치 · 셀 수 · 온도 미기재 · 표 ↔ 본문 불일치).

---

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)

- "Ben Hadj Ali, Qin et al. (ChemRxiv 2026, preprint, not peer reviewed) compared warm isostatic pressing (400 MPa, 80 °C, 5 min) with cold uniaxial pressing (~116 MPa, 30 s) of a wet-processed NMC622/Li₆PS₅Cl/carbon–binder (69:27.6:3.4 wt%) cathode: the cathode thickness decreased by 26 vs 12 % and the reported porosity was 10.9 vs 25.1 %, and at 60 °C the C/2 discharge capacity was 158–164 vs 143–149 mAh g⁻¹ while C/10 was unchanged; first-cycle 3D mechano-electrochemical simulations on DEM-generated microstructures attributed the high-rate gap to ionic-transport heterogeneity, with comparatively small differences in active-material hydrostatic-stress maps."
- 국문: *"이 모델에서 WIP 와 CUP 의 차이는 등방 하중이 아니라 같은 물성 · 같은 z 변위의 더 깊은 목표 (30 vs 20 %) 와 4 ms 유지로 표현됐다 (Ben Hadj Ali 2026, 프리프린트) — 'isostatic 효과' 를 모델이 분리했다고 인용하지 않는다."*
- 국문: *"같은 습식 NMC622/LPSCl 양극에서 온간 등방 가압 (400 MPa · 80 °C) 은 냉간 단축 가압 (≈116 MPa) 보다 두께를 26 vs 12 % 줄였다 (게이지 · Ben Hadj Ali 2026) — 압력 크기 · 온도 · 시간 · 하중 방식이 함께 다르다."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)

1. **실험의 네 인자 동시 변경**: WIP ↔ CUP = 400 ↔ 116 MPa (×3.45) · 80 ↔ 상온 · 5 min ↔ 30 s · 등방 ↔ 단축.  본문 (p.28) *"The combined effect of elevated temperature (80 °C) and isotropic pressure promotes enhanced particle rearrangement"* · 결론 (p.42) *"identical electrode formulations … with the pressing technique as the main variable"* · *"confirmed the advantages of the multidirectional compaction"* — 압력 크기 차를 빼고 서술했다.
2. **모델의 WIP = 목표 30 % + 4 ms 유지**: 같은 물성 · z 변위 · 측방 하중 없음 · 온도 의존 물성 없음 (p.19).  *"principal distinction"* 문장 (p.20–21) 은 목표 차 (20 vs 30 %) 를 빠뜨린다.  열욕 온도가 [35] 힘장에서 무의미하다면 [추정] 모델의 '온간' 효과는 유지 시간이다 — 목표 · 유지 · 온도를 따로 돌린 팔은 없다.
3. **DEM 재료계 ↔ 실험 재료계**: 매개변수 출처 [35] = SBS · Super C45 · p-xylene · NEI LPSCl (정본 카드 alabdali2023) ↔ 이 실험 = PVDF-HFP · Super P · n-butyl acetate · POSCO LPSCl.  본문도 DEM 의 CBSA 를 *"carbon black, Styrene-Butadiene-Styrene (SBS) binder"* 라 적는다 (p.16) — *"which employed the same material system and electrode formulation"* (p.16) 은 조성 · AM · SE 화학까지만 참.
4. **검증의 독립성**: 건조 상자 높이 51.94 µm (−9.84 %) 는 부과값 · 목표 20 · 30 % 의 선정 근거 미기재 · 밀도 일치 = 두께 일치 (밀도 × 두께 = 82.92) → Fig. 7e–g 의 셋 중 둘은 같은 정보 (§8-3).
5. **DEM 기공률 정의**: 보고 26.5 · 15 % 는 (i) 질량 보존 ((1 − ε) × 두께 33.6 ↔ 31.8 µm) 과 (ii) Fig. 6 상 분율 평균 (0.43 · 0.31 [판독]) 둘 다와 맞지 않는다 [우리 산술] — 정의 · 분석 부피 [미확인].  WIP *"slightly higher than the measured value"* (15 vs 10.9 %) 의 뜻도 정의에 달렸다.
6. **실험 기공률의 밀도 기준**: 식 (1) 의 성분 밀도 [미확인] · 표 1 · 2 가 함축하는 골격 2.41–2.47 g/cm³ 은 흔한 결정 밀도로 센 2.99–3.24 g/cm³ (우리 가정) 보다 25 % 낮다 → 그 밀도면 기공 47–51 · 40–44 · 27–32 % [우리 산술] · 두께 · 질량의 CC 포함 여부 [미확인].
7. **두께 측정 셋의 불일치**: CUP 게이지 72.16 · SEM 47.77 · XCT 54.5 µm · 미가압 게이지 82 ↔ SEM 50.10 µm · SEM 함축 CC 두께 20.6 ↔ 14.9 µm · 표 1 CUP 72 ± 1.2 ↔ 본문 72.16 ± 1.65 · DEM 건조 51.94 µm 는 게이지가 아니라 SEM 양극층 (50.10) 크기에 가깝다 (DEM 은 상대 감소만 맞춘다).
8. **셀 조립 재가압**: 두 양극을 *"the same load"* 로 다시 누른다 (수치 없음 · 2 t ≈ 250 MPa 로 읽힘 [추정]) — 전기화학 · EIS 를 잰 양극 상태가 측정 · 모의한 원판 상태와 다를 수 있다 (특히 CUP).
9. **EIS 표 ↔ 본문**: 첫 사이클 뒤 WIP R_int 15.7 → **114 Ω** · 합 WIP 143 > CUP 79 Ω ↔ 본문 *"a marked decrease in impedance is observed for both"* · *"in agreement with the lower impedance observed before and after cycling"* (p.31) — Fig. 3f 에서도 WIP 호가 크다 [판독] · 표에 16.4 가 두 칸 (CUP R_int · WIP R_ct) — 옮김 오류 가능 [추정] · 온도 · 셀 수 [미확인].
10. **R_ct 방전 · GITT 서술**: 방전 R_ct 는 3.05–3.7 V 에서 CUP 가 더 낮다 [판독] ↔ *"gradually converge"* · 가운데 전위 충전 D 는 두 양극이 ≈10–30 % 안 [판독] — "WIP 가 높다" 는 끝점 몫 · CUP 충전 R_ct (≈140 Ω) ↔ 방전 (≈8 Ω) 17 배 차는 첫 충전이 섞였을 가능성 [추정] · GITT · EIS 의 셀 · 사이클 [미확인].
11. **j₀**: 식 (3) 의 z 정의 없음 · A 의 출처 (DEM 면적인지) [미확인] · 값 미기재 · 두 모델에 '같은' j₀ 를 넣었으므로 모델의 C/2 차에는 실험의 R_ct 차 (≈1/17) 가 없다 — 실험 차와 같은 양이 아니다.
12. **FEM 미기재**: E · ν (AM · SE · CBD) · 계면 조건 · 기공 영역 역학 · 메시 · 실행 시간 · 분리막 두께 [미확인] · C/10 첫 사이클 일치는 실험 GITT OCV 를 입력으로 넣은 결과에 가깝다 [추정] · 그런데도 모의 방전 ≈210 ↔ 실험 ≈191 mAh/g (+10 % [판독]) — *"some deviation … close to the end of discharge"* 보다 크다.
13. **응력 결론의 근거**: Fig. 8e 한 장 (AM · 단면 하나 · 색 포화) · 정량 통계 없음 · 선형 탄성 (항복 · 박리 · 파괴 없음 → GPa 접점 응력) · 잔류 응력 미전달 · 경계 적층압 68 MPa 는 색 천장의 1.7 % — WIP ↔ CUP 의 거시 압밀 차가 국소 응력에 작게 보이는 것은 고유변형 지배 · 국소 구속 지배인 모델 구조상 예상되는 결과다 [추정] · 서론의 *"more uniform mechanical load transfer"* 가설을 시험한 것은 아니다.
14. **C/2 비교의 한계**: 모의 = 깨끗한 첫 사이클 · 실험 = 20 번째 사이클 (저자: 정성) · 절대 용량 모의 ≈190 · 201 ↔ 실험 ≈142 · 157 [판독].
15. ★ **Fig. 6 패널 제목 ↔ 캡션** — **판정: 캡션 *"(a) CUP and (b) WIP"* 이 맞고 패널 제목 *"a) WIP · b) CUP"* 이 뒤바뀌었다.**  근거 셋: ① **가로축 끝** = 패널 a 의 곡선은 ≈45.5 µm (기공 → 1) 까지, 패널 b 는 ≈37.3 µm 에서 끝난다 [판독] ↔ Fig. 2 의 제하 뒤 DEM 두께 **CUP 45.71 · WIP 37.40 µm** [인쇄] ② **기공 분율** = 패널 a bulk ≈0.38 > 패널 b ≈0.27 [판독] ↔ 본문 DEM 기공 CUP > WIP (26.5 > 15 %) ③ **본문 서술** (p.35) = *"the WIP cathode exhibits smaller variations … across most of the electrode thickness"* · *"The pore fraction within the bulk region also remains generally higher for CUP"* — 요동이 크고 기공이 높은 쪽이 패널 a.  ⇒ 이 카드는 캡션 기준 (패널 a = CUP) 으로 읽는다.
16. **Fig. 7d 축**: 왼쪽 *"Effective diffusivity (m² s⁻¹)"* 인데 값 0.06–0.128 은 무차원 (본문 *"relative effective diffusivity"*) · 오른쪽 *"Tortuosity factor"* ↔ 본문 *"geometric tortuosity"* — 우리 규약에서 tortuosity factor = τ² (§7-3).
17. **Fig. 7c 크기**: σ_ion,eff ≈0.0075–0.016 mS/cm 와 f 0.060 · 0.128 이 함축하는 SE 고유 σ = **0.125 mS/cm** [우리 산술] — LPSCl 펠릿 값 (정본 카드: `bazzoun2026_dem_fem_rnm_ionic` 1.02 · `schmitt2026_chemomech_stability_dry_cathode_separator_sheets` 2.35 · `cronau2021_stack_pressure_ionic_conductivity` SI 평탄 2.88–3.46 mS/cm) 의 1/8–1/28 · 입력값 원문 없음 · 축 단위 (S/m ↔ mS/cm) 를 먼저 확인할 자리 [추정] · σ_e,eff ≈10⁻³ mS/cm 도 같은 그룹 Alabdali 2023 의 δ_e (24–33 mS/cm · 정본 카드) 와 4 자릿수 다르다 — 입력 [미확인] → 절대값 인용 금지.
18. **Fig. 4b EDS**: 범례 S · Cl · P · Ni · O · C · Al ↔ 캡션 *"C, O, Ni, Co, Mn, and Al"* · 패널 제목 *"Unpresssed"*.
19. **참조 · 번호 오기**: p.10 *"(Figure 2a)"* · p.11 *"Figure 2c and 2d"* (→ Fig. 3) · Fig. 5 캡션 (f) *"Figure 2e"* (→ 5e) · p.35 *"summarized in Figure 5"* (→ Fig. 7) · 결과 절 번호 *"2.3 Microstructural Characterization"* · *"2.4 FEM Simulation Analysis"* (→ 3.x) · 초록 *"and lower geometric."* (낱말 빠짐) · p.12 *"A probe current of 90"* (단위 없음) · p.31 *"presing"* · p.43 *"Luca Weckelmannd"* · p.21 *"microstructure shown in Figure 1"* (작업 흐름 그림).
20. **인용 품질**: p.24 *"Linear-elastic descriptions are widely used in electro-chemo-mechanical simulations … [19–22]"* 의 [19]–[22] = 분말 압축 · HIP 문헌 (전기화학-역학 아님) · p.3 단축 가압 이방성 근거 [12–17] 중 [13]–[17] = LLZO 입계 · Li 침투 문헌 · 웹 제목 꼴 서지 [10] [15] [18] [28] (*"(n.d.)"* · 접속일 2026-08-16) · [28] URL 에 외부 서비스 추적 꼬리 (`utm_source=…`) — 이 카드는 그 URL 을 옮기지 않는다 · [44] 제목에 MathML 조각 · 같은 그룹 DEM 등방 · 사이클 응력 선행 (Alabdali 2024 ESM · 정본 카드 `dem_mechanical_stresses_ssb_electrode_cycling`) 미인용 · 보충자료 링크 *"XXX"*.
21. **통계 · 대표성**: 셀 수 · 반복 · 오차 막대 (율속 · GITT · EIS) 없음 · DEM 한 실현 · 측면 41.25 µm ≈ AM 지름 4 개 · DEM 가압 0.02 m/s · 유지 4 ms (실험의 1/75,000) · 준정적 점검 없음.
22. **실용 범위**: 60 °C · 68 MPa 적층압 (높음) · Li-In 반쪽 셀 (모델은 Li 금속) · 25 사이클 (C/10 회복 단계 없음) · 저자 스스로 장기 사이클 · 손상은 다음 일로 남겼다.
23. **전이 한계 (우리 쪽)**: LPSCl 같음 · NMC622 ↔ NMC811 · 습식 PVDF-HFP ↔ 건식 · DEM 재매개변수화 상수 ↔ 우리 연화 물성 · 선형 탄성 FEM ↔ J2 MPM — 같은 이름 (porosity · tortuosity · stress) 의 다른 양이 섞이지 않게 표지를 붙인다.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 3 | R. Koerver, W. Zhang, L. de Biasi, S. Schweidler, A.O. Kondrakov, S. Kolling, T. Brezesinski, P. Hartmann, W.G. Zeier, J. Janek, Chemo-mechanical expansion of lithium electrode materials – on the route to mechanically optimized all-solid-state batteries, Energy Environ. Sci. 11 (2018) 2142–2158. https://doi.org/10.1039/C8EE00907D. | 카드 없음 — FEM 고유변형의 NMC622 ΔV 출처 (우리 `--cycle-dv-*` 기본값과 대조할 원전) |
| 4 | C. Yuan, W. Lu, J. Xu, Electrochemical-mechanical coupling failure mechanism of composite cathode in all-solid-state batteries, Energy Storage Materials 60 (2023) 102834. https://doi.org/10.1016/j.ensm.2023.102834. | 카드 없음 — 복합 양극 기계-전기화학 실패 (서론 [4]) |
| 9 | J. Zhang, J. Fu, P. Lu, G. Hu, S. Xia, S. Zhang, Z. Wang, Z. Zhou, W. Yan, W. Xia, C. Wang, X. Sun, Challenges and Strategies of Low-Pressure All-Solid-State Batteries, Advanced Materials 37 (2025) 2413499. https://doi.org/10.1002/adma.202413499. | 카드 없음 — 저압 운전 총설 (산업 적층압 수 MPa) |
| 12 | M. Dixit, C. Beamer, R. Amin, J. Shipley, R. Eklund, N. Muralidharan, L. Lindqvist, A. Fritz, R. Essehli, M. Balasubramanian, I. Belharouak, The Role of Isostatic Pressing in Large-Scale Production of Solid-State Batteries, ACS Energy Lett. 7 (2022) 3936–3946. https://doi.org/10.1021/acsenergylett.2c01936. | 카드 없음 — ★ 등방 가압 ASSB 의 기준 문헌 (같은 압력 단축 ↔ 등방 대조가 있는지 볼 것) |
| 19 | M.L.V. Mahesh, V.V. Bhanu Prasad, A.R. James, A comparison of different powder compaction processes adopted for synthesis of lead-free piezoelectric ceramics, Eur. Phys. J. B 89 (2016) 108. https://doi.org/10.1140/epjb/e2016-60390-6. | 카드 없음 — §10-20 인용 불일치의 예 (선형 탄성 근거로 인용됨) |
| 20 | U.M. Attia, Cold-isostatic pressing of metal powders: a review of the technology and recent developments, Critical Reviews in Solid State and Materials Sciences 46 (2021) 587–610. https://doi.org/10.1080/10408436.2021.1886043. | 카드 없음 — CIP 기술 총설 (등방 압축 기전) |
| 23 | F.B. Swinkels, D.S. Wilkinson, E. Arzt, M.F. Ashby, Mechanisms of hot-isostatic pressing, Acta Metallurgica 31 (1983) 1829–1840. https://doi.org/10.1016/0001-6160(83)90129-3. | 카드 없음 — HIP 기전 지도 (Arzt 계열 · 정본 `arzt1982_particle_coordination_densification_spheres` 와 이웃) |
| 25 | D.H.S. Tan, Y.S. Meng, J. Jang, Scaling up high-energy-density sulfidic solid-state batteries: A lab-to-pilot perspective, Joule 6 (2022) 1755–1769. https://doi.org/10.1016/j.joule.2022.07.002. | 카드 없음 — 등방 가압의 공정 부담 (서론) |
| 26 | M. Dixit, C. Beamer, R. Essehli, A. Bisht, R. Amin, M. Li, J. Sharma, T. Rabe, M. Balasubramanian, I. Belharouak, Isostatic pressing of multilayer pouch cells and its implications for battery manufacturing, Device 2 (2024) 100370. https://doi.org/10.1016/j.device.2024.100370. | 카드 없음 — 다층 파우치 등방 가압 |
| 27 | K. Hayashi, T. Mori, K. Fukuda, H. Ito, Y. Manabe, Application of Warm Isostatic Pressing to Densification of All Solid-State Composite Cathode Electrodes in All Solid-State Lithium-Ion Batteries, 粉体および粉末冶金 72 (2025) S1167–S1173. https://doi.org/10.2497/jjspm.16C-SIS6-03. | 카드 없음 — ★ WIP 복합 양극 치밀화 (계면 · 전하이동 저항 감소의 선행) |
| 28 | Enabling Uniform and Accurate Control of Cycling Pressure for All-Solid-State Batteries - Chen - 2024 - Advanced Energy Materials - Wiley Online Library, (n.d.). (URL 은 옮기지 않음 · 원문 p.46–47) | 카드 없음 — 균일 사이클 압력 제어 (서지 미완성 · §10-20) |
| 29 | S. Ben Hadj Ali, M. Alabdali, V. Viallet, V. Seznec, A.A. Franco, A computational workflow for the simulation of solid state battery electrodes from manufacturing to electrochemical performance, Journal of Power Sources 630 (2025) 236131. https://doi.org/10.1016/j.jpowsour.2024.236131. | 카드 없음 — 같은 사슬의 1 편 (습식 · 단축 캘린더링 → 전기화학) · 우리 DEM → STEP4 와 같은 자리 |
| 30 | S. Ben Hadj Ali, M. Alabdali, V. Viallet, V. Seznec, A.A. Franco, A New Three-Dimensional Microstructure-Resolved Model to Assess Mechanical Stress in Solid-State Battery Electrodes, Batteries & Supercaps 9 (2026) e202500540. https://doi.org/10.1002/batt.202500540. | 카드 없음 — 일방 결합 응력 (2 편) · ★ 그들 FEM 물성 (E · ν) 이 여기 있을 가능성 |
| 31 | S. Ben Hadj Ali, A. Valisammagari, P.T. Bhutia, A.H. Dao, V. Viallet, V. Seznec, A.A. Franco, Fully coupled mechano-electrochemical modeling of 3D-resolved microstructures for solid state batteries manufactured by wet processing, Energy Storage Materials 90 (2026) 105304. https://doi.org/10.1016/j.ensm.2026.105304. | 카드 없음 — ★ 완전결합 틀의 원 논문 (이 논문 FEM 의 정의 · 물성 · 경계 · 검증) — 다음 독서 1 순위 |
| 32 | W. Weppner, R.A. Huggins, Determination of the Kinetic Parameters of Mixed-Conducting Electrodes and Application to the System Li3Sb, J. Electrochem. Soc. 124 (1977) 1569–1578. https://doi.org/10.1149/1.2133112. | 카드 없음 — GITT 식 (2) 원전 |
| 34 | L.E. Silbert, D. Ertaş, G.S. Grest, T.C. Halsey, D. Levine, S.J. Plimpton, Granular flow down an inclined plane: Bagnold scaling and rheology, Phys. Rev. E 64 (2001) 051302. https://doi.org/10.1103/PhysRevE.64.051302. | 카드 없음 — gran/hertz/history 꼴 원전 |
| 35 | M. Alabdali, F.M. Zanotto, M. Duquesnoy, A.-K. Hatz, D. Ma, J. Auvergniot, V. Viallet, V. Seznec, A.A. Franco, Three-dimensional physical modeling of the wet manufacturing process of solid-state battery electrodes, Journal of Power Sources 580 (2023) 233427. https://doi.org/10.1016/j.jpowsour.2023.233427. | 정본 카드 `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` — 힘장 · PSD · 밀도의 출처 (건조 k_n · 마찰 · ε/kT) |
| 36 | J. Xu, A.C. Ngandjong, C. Liu, F.M. Zanotto, O. Arcelus, A. Demortière, A.A. Franco, Lithium ion battery electrode manufacturing model accounting for 3D realistic shapes of active material particles, Journal of Power Sources 554 (2023) 232294. https://doi.org/10.1016/j.jpowsour.2022.232294. | 정본 카드 `xu2023_realistic_am_shape_cgmd_calendering` — CBSA/CBD 틀 |
| 37 | A.C. Ngandjong, T. Lombardo, E.N. Primo, M. Chouchane, A. Shodiev, O. Arcelus, A.A. Franco, Investigating electrode calendering and its impact on electrochemical performance by means of a new discrete element method model: Towards a digital twin of Li-Ion battery manufacturing, Journal of Power Sources 485 (2021) 229320. https://doi.org/10.1016/j.jpowsour.2020.229320. | 정본 카드 `ngandjong2021_dem_calendering_digital_twin` — 균질 건조 · 캘린더링 DEM |
| 38 | M. Chouchane, A.A. Franco, An Invitation to Engage with Computational Modeling: User-Friendly Tool for In Silico Battery Component Generation and Meshing, Batteries & Supercaps 4 (2021) 1451–1456. https://doi.org/10.1002/batt.202100096. | 카드 없음 — INNOV |
| 39 | M. Chouchane, A. Rucci, A.A. Franco, A Versatile and Efficient Voxelization-Based Meshing Algorithm of Multiple Phases, ACS Omega 4 (2019) 11141–11144. https://doi.org/10.1021/acsomega.9b01279. | 카드 없음 — 복셀 메싱 (겹친 구를 어떻게 하나의 고체로 잇는지 = 기공 정의 §10-5 의 열쇠) |
| 42 | X. Zhang, W. Shyy, A.M. Sastry, Numerical Simulation of Intercalation-Induced Stress in Li-Ion Battery Electrode Particles, J. Electrochem. Soc. 154 (2007) A910. https://doi.org/10.1149/1.2759840. | 카드 없음 — 화학-기계 퍼텐셜 (식 13–14) 원전 |
| 43 | K. Takahashi, K. Higa, S. Mair, M. Chintapalli, N. Balsara, V. Srinivasan, Mechanical Degradation of Graphite/PVDF Composite Electrodes: A Model-Experimental Study, J. Electrochem. Soc. 163 (2015) A385. https://doi.org/10.1149/2.0271603jes. | 카드 없음 — 응력-농도 양방향 식 (16) |
| 47 | J. Christensen, J. Newman, Stress generation and fracture in lithium insertion materials, J Solid State Electrochem 10 (2006) 293–319. https://doi.org/10.1007/s10008-006-0095-1. | 카드 없음 — 고유변형 · 열팽창 유비 |
| 48 | N. Iqbal, J. Choi, C. Lee, H.M.U. Ayub, J. Kim, M. Kim, Y. Kim, D. Moon, S. Lee, Effects of Diffusion-Induced Nonlinear Local Volume Change on the Structural Stability of NMC Cathode Materials of Lithium-Ion Batteries, Mathematics 10 (2022) 4697. https://doi.org/10.3390/math10244697. | 카드 없음 — Ω · λ 식 (23–24) |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-06)
- 48 쪽 글자 층 전수 (배치 판 · 쪽별 판) · 저자 · 소속 · 날짜 · DOI · 라이선스 = p.1–2 · CRediT · 이해상충 = p.43 · 연구비 · 감사 · 보충자료 자리표시 = p.44 · 참고문헌 48 개 = p.44–48 · 'GPa' · 'Young' · 'modul' · 'Poisson' · 'seed' · 'data availab' 전수 검색 (FEM 물성 · DEM 반복 · 데이터 진술 없음 확인).
- 식 (1) · (2) · (3) · (4)–(9) · (12)–(18) · (20)–(24) = PDF 쪽 렌더 (130 dpi) 로 위 · 아래 첨자 확인 (글자 층은 첨자 소실 · 식 3 의 z 는 렌더에서만 보인다).
- 그림 · 표 크롭 11 장 전부 렌더 열람 · Fig. 3 (b · c–d · e–f · g–h) · Fig. 4 (a · b) · Fig. 7 (b · c–d) · Fig. 8 (a–b · c–d · e) 는 확대해 다시 봄.
- 판독 검산: Fig. 7d 마커 0.0600 · 0.1284 · 2.579 · 1.762 ↔ 본문 0.060 · 0.128 · 2.58 · 1.76 ✓ · Fig. 3b C/2 판독 차 ≈14.5 ↔ 본문 *"around 10-15"* ✓ · Fig. 2 치수로 센 두께 감소 12.0 · 28.0 % ↔ 본문 ≈12 · ≈28 % ✓ · DEM 밀도 = 1.5965 × 51.94 / t 로 1.814 · 2.217 재현 ✓ · Fig. 7b 막대 합 ≈1.00 (두 판) ✓ · Fig. 6 디지털화 패널 합 1.00 (범례 영역 가린 뒤) ✓.
- Fig. 6 판정 (§10-15) = 판독 (곡선 끝 · bulk 기공) + 인쇄 (Fig. 2 두께 · 본문 p.35 서술) 세 근거.
- 정본 대조: `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` §0 · §2 메타 (SBS · Super C45 · p-xylene · NEI LPSCl) · §4-4 건조 힘장 표 (k_n 100 pg µm⁻¹ µs⁻² · X_µ 12.5 · ε/kT ~ 10⁸) · §3-2 (τ = √(η/D_eff) 재현) · `dem_mechanical_stresses_ssb_electrode_cycling` 저자 목록 (Alabdali · Zanotto · Chouchane · Ngandjong · Viallet · Seznec · Meng · Franco — Ben Hadj Ali 없음 · 이 논문 목록에 없음) · `zhang2026_polymer_electrolyte_modeling_perspective` (Ben Hadj Ali 2025 · 완전결합 선행 = 정본 카드 없음) · `qin2026_bilayer_cathode_cgmd_dem_graded_thick_electrode` (스프링백 비 정의 · 같은 사슬) · `bucci2017_chemomech_failure_assb_cycling_czm` (선형 탄성 AM 응력 > 1 GPa · SE 0–200 MPa · CZM).
- 참고문헌 ↔ 정본 카드 DOI 대조: [35] · [36] · [37] 일치 · 나머지 인용 DOI 는 정본 `litdb/papers/` 에 없음 (git grep).
- 정본 중복 확인: `litdb/papers/` 에 이 DOI · 제목 없음 (2026-11-06 · git grep `chemrxiv.15011566` · `Warm Isostatic` = `_sources.json` 한 줄뿐).
- 인용 서지는 PDF 목록 글자 그대로 (줄바꿈 하이픈만 배치 판으로 복원 — Large-Scale · Mixed-Conducting · 0001-6160(83)90129-3) · [28] 은 제목만 (URL 미전재).
- 메인 리포 (읽기만) 대조: `docs/effective_modulus_stress.md` (EM-01–07 · §1 · §2-1 · §2-4 · §3) · `docs/reviews/dem_unloading_ps45_prereg_20261009.md` (ρ 정의 · P_meas) · `docs/data/ps45_r45_network_g2_20261007/README.md` (tau2 · CF · 협착 몫) · `docs/ncm_sc_poly_electrochem_anchors.md` (D_s) · `docs/temp_pressure_capability.md` §4 (온도 인자 0) · `scripts/mpm3d_compaction.py` (`--save-state` 114–123 · `--cycle-deform` 855) — 우리 쪽 정본 파일은 고치지 않았다.

## 🔗 관련 카드
- **같은 그룹 · 같은 사슬**: `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` (DEM 매개변수 원전) · `ngandjong2021_dem_calendering_digital_twin` · `xu2023_realistic_am_shape_cgmd_calendering` · `qin2026_bilayer_cathode_cgmd_dem_graded_thick_electrode` (Lei Qin · 제하 스프링백 25–28 → 11–14 %) · `wet_processing_resolved_am_ssb_cathode_manufacturing` (Weitze 2024 · 습식 ASSB · 회복 10–15 % [그 카드 산술]) · `sankar2026_fiber_scale_dem_carbon_felt_manufacturing` · `dem_mechanical_stresses_ssb_electrode_cycling` (LIGGGHTS 등방 + 사이클 응력 · 미인용 선행) · `zhang2026_polymer_electrolyte_modeling_perspective`.
- **등방 · 온간 · 열간 가압**: `larson2025_hot_pressing_argyrodite_low_stack_pressure_conductivity` (150 °C 열간 단축 가압 · 순수 LPSCl) · `cronk2026_lis_positive_electrode_geometry_fem` (WIP 500 MPa · 80 °C + COMSOL 선형 탄성 · 등방 고유변형 · E_SE 22 GPa) · `jun2026_ppma_econductive_binder_si_lowpressure_assb` (WIP 450 MPa · 80 °C · 5 min 파우치) · `interfacial_impedance_formulation_assb_cathode` (단축 ↔ 등방 원통 · 펠릿 EIS) · `thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography` (준등방 초고압) · `bouvard2000_hard_soft_powder_densification` · `minnmann2021_jes_charge_transport_bottlenecks` (WIP 한 자릿수 기공 언급).
- **사이클 응력 · 기계-전기화학**: `bucci2017_chemomech_failure_assb_cycling_czm` · `so2021_dem_fabrication_degradation_ductile_particles` · `wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn` (복셀 FE 선형 탄성 균질화) · `kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review`.
- **수송 · 이온 앵커**: `bazzoun2026_dem_fem_rnm_ionic` (DEM + FEM + RNM · CAM 70 wt% · 400 MPa) · `schmitt2026_chemomech_stability_dry_cathode_separator_sheets` (같은 날 · 압력 이력이 다른 셀 대조).
- **참고 [12] 의 원문 카드 (2026-11-12 추가)**: `dixit2022_isostatic_pressing_ssb_large_scale_manufacturing_review` (등방 가압 Focus Review · 서지 = 위 참고문헌 표 12 번과 같음 · **같은 압력의 단축 ↔ 등방 대조 값은 없다** — 자체 시연 (안티페로브스카이트 펠릿) 기공 단축 ~12 % (압력 미기재) → CIP 414 MPa ~1.8 % → WIP 345 MPa · 135 °C 0.15 % · 원문은 단축 가압에 대해 '이방성' 낱말 없이 금형 벽 마찰의 밀도 불균일 · 국소 미세구조 차를 말한다 — 대조는 그 카드 §0-1).
- 참고 [27] 의 원전 (2026-11-12 카드): [`hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode`](hayashi2025_wip_temperature_void_xct_wet_process_ncm111_lpscl_cathode.md) — 슬러리 도포 NCM111 (LiNbO₃ 코팅) + Li₆PS₅Cl 시트의 WIP (600 MPa 하나 · 상온–190 °C · 유지 1 s–1 min) · 감압 뒤 싱크로트론 CT 의 기공 + 탄소 복셀 분율 0.19 → 0.057 · 0.042 · 0.039 · 두께 ≈170 → 104 → 94 µm · 압력별 값 · 단축 가압 대조는 없다 (그 카드 §0-1 이 이 카드 L439 의 서지 · 한 줄 요약을 대조 — 원문과 같다).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
