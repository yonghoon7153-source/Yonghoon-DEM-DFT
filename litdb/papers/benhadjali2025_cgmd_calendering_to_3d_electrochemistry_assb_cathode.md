<!-- 표준 양식 확장 (paper-level STANDALONE — 이 카드만 읽어도 논문을 읽은 것과 같게). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 1저자 11-12 후보 표 N-18) 에서 꼭 뽑으라고 한 항목 (제조 모의 → 넘김 → 3D 전기화학 · 단계별 검증 · 비용 · 영상 · 저자 한계 · 우리 DEM → MPM → STEP3/4 사슬과 나란히).
     본 = benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem.md (같은 제1 저자 · 같은 사슬의 다음 편) · 꼴 = koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb.md (§0-1 고른 의도 대조 · §8 자세한 분석) · 제조 모의 원 논문 = alabdali2023_cgmd_wet_manufacturing_ssb_cathode.md (본문 ref [13]).
     원문 = 출판본 (J. Power Sources 630 (2025) 236131 · 10 쪽 · CC BY 4.0) + SI (Elsevier mmc1.docx = 그림 S1 · S2 · 표 S1 · S2 · 참고문헌 S1–S4) + 보충 영상 셋 (mmc2–4.mp4 · 각 2.4 s · 72 프레임 · 640 × 480).
     쪽 표기 = "p.N" = 인쇄 쪽 = PDF 쪽 (1–10).  SI 쪽 = LibreOffice 로 바꾼 PDF 의 쪽 (docx 는 쪽 번호가 없다).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 원본 300 dpi 래스터를 그 그림의 눈금선으로 보정해 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 96 행) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드에 적힌 값 (slug 병기) ·
     [우리] = 우리 쪽 값 (CLAUDE.md · 메인 리포 문서 출처 병기) · [미확인] = 본문 10 쪽 + SI 전수에 없음.
     원문 10 쪽은 글자 층 (pdftotext raw · layout · PyMuPDF 줄 좌표) + 렌더로 전부 읽었고, 식 (1)–(9) 는 렌더로 첨자 · 근호를 확인했다 (글자 층은 식 (7) 의 근호를 잃는다).  SI docx 는 XML 을 직접 읽고 LibreOffice 변환 PDF 로 다시 보았다.  업로드 원문은 읽기만 했다. -->
# 습식 제조 모의 (CGMD · 슬러리 → 건조 → 판 하강 캘린더링 0 · 20 · 35 %) 로 만든 NMC622 / Li₆PS₅Cl / 탄소-바인더 양극을 겹침 우선순위 (AM → SE → CBD) + 복셀 다상 메싱 (INNOV) 으로 COMSOL 3D 전기화학 (AM 안 Fick · 옴 · Butler–Volmer · t⁺ = 1) 에 넘겨 반쪽 셀 방전 — 캘린더링 35 % 가 C/5 에서 ≈92 vs ≈38 mAh/g [판독] · SE 굴곡 τ_g ≈10 → ≈4 · AM 표면 SE 피복 ≈10 → ≈28 % — 넘긴 구조 = 목표 두께 그대로 (되튐 · 잔류 응력 · 외력 없음) · 실험 대조 없음 — Ben Hadj Ali · Alabdali · Viallet · Seznec · Franco (J. Power Sources 630, 236131, 2025)

> slug `benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode` · DOI `10.1016/j.jpowsour.2024.236131` · type `CGMD wet-manufacturing microstructures (LAMMPS · Lennard-Jones + granular Hertz · slurry → drying → calendering 0/20/35 % thickness reduction · reused from Alabdali 2023) → overlap post-processing (AM > SE > CBD) + voxel multiphase meshing (INNOV) → COMSOL 3D-resolved half-cell discharge FEM (Fick in AM · Ohm in AM/CBD/CC/SE · Butler–Volmer at AM–SE · t+ = 1 · C/5–C/50) + GeoDict voxel transport (ConductoDict/DiffuDict · tau_g = sqrt(phi/Deff) · McMullin) — no mechanics, no experiment` · PDF `be97bf85-18._A_computational_workflow_for_the_simulation_of_solid_state_battery_electrodes_from_manufacturing_to_electrochemical_performance.pdf` · SI `9da350e2-18_Sup_zip/1-s2.0-S0378775324020846-mmc1.docx (+ mmc2–4.mp4)` · digested `2026-11-12` · status ✅
>
> **원제**: *A computational workflow for the simulation of solid state battery electrodes from manufacturing to electrochemical performance* (p.1)
> **저자 · 소속 (p.1)**: **Siwar Ben Hadj Ali** ᵃ˒ᵇ˒ᶜ · Mohammed Alabdali ᵃ˒ᵇ · Virginie Viallet ᵃ˒ᵇ · Vincent Seznec ᵃ˒ᵇ˒ᶜ · **Alejandro A. Franco** ᵃ˒ᵇ˒ᶜ˒ᵈ\* — ᵃ Laboratoire de Réactivité et Chimie des Solides (LRCS), Université de Picardie Jules Verne, Hub de l'Energie, UMR CNRS 7314, Amiens · ᵇ RS2E, Hub de l'Energie, FR CNRS 3459 · ᶜ ALISTORE-European Research Institute, FR CNRS 3104 · ᵈ Institut Universitaire de France (\* 교신 alejandro.franco@u-picardie.fr).
> **판 · 지위 (p.1 · p.9)**: J. Power Sources **630** (2025) **236131** · 접수 2024-11-08 · 수정 2024-12-18 · 승인 2024-12-25 · 온라인 2025-01-03 · open access **CC BY 4.0** (© 2024 The Authors) · 연구비 = Umicore DESTINY PhD 프로그램 (EU H2020 MSCA COFUND #945357) · Horizon Europe PULSELiON (101069686) · IUF · 이해 상충 없음 · *"Data is available upon reasonable request."* (p.9) · CRediT: Ben Hadj Ali = 원고 · 시각화 · 소프트웨어 · 방법 · 조사 · 분석 · 데이터 · 구상 / Alabdali = 검토 · 방법 · 조사 · 분석 · 구상 / Viallet · Seznec = 지도 / Franco = 검토 · 지도 · 자원 · 관리 · 방법 · 연구비 · 구상.
> **같은 그룹 카드 (링크만)**: [`benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem`](benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem.md) (같은 제1 저자 · 같은 사슬의 다음 편 = 기계-전기화학 FEM + WIP ↔ CUP 실험 · 이 논문을 ref [29] 로 인용) · [`alabdali2023_cgmd_wet_manufacturing_ssb_cathode`](alabdali2023_cgmd_wet_manufacturing_ssb_cathode.md) (둘째 저자 · 이 논문 ref [13] = 미세구조 셋의 출처) · [`dem_mechanical_stresses_ssb_electrode_cycling`](dem_mechanical_stresses_ssb_electrode_cycling.md) (ref [32] · LIGGGHTS 등방 압축 + 사이클 응력) · [`ngandjong2021_dem_calendering_digital_twin`](ngandjong2021_dem_calendering_digital_twin.md) (ref [24] · 겹침 후처리의 LIB 선례) · [`zhang2026_polymer_electrolyte_modeling_perspective`](zhang2026_polymer_electrolyte_modeling_perspective.md) (이 논문을 ref 36 으로 인용).
> **판독 원자료**: `litdb/figures/benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode/digitized.csv` (96 행 — 그림 2c–f 막대 12 · 3e 마커 12 · 6a/6b 곡선 36 · 7 막대 18 · 8a/8b 마커 9 · 영상 색 9) · 그림 크롭 **51 장** (도구 8 + 손 43 = 패널 12 · SI 5 · 식 9 · 근거 문단 17 · §5) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 같은 그룹이 먼저 낸 습식 제조 CGMD 모의 (Alabdali 2023 [13] — 슬러리 → 건조 → 평판 등속 하강 캘린더링) 에서 두께를 **0 · 20 · 35 % 줄인 NMC622 / Li₆PS₅Cl / CBD 양극 셋** (41 × 41 µm · 두께 46 · 36.8 · 29.9 µm · 기공 17 · 13 · 6 % — 표 S1 · 그림 S2) 을, **겹침 우선순위 후처리 (AM → SE → CBD · 겹친 CBD 부피를 AM / SE 로 옮김 → 구가 불규칙 모양이 됨)** 와 **자체 INNOV 의 복셀화 다상 메싱** 으로 COMSOL 에 넘겨, Li 박 | LPSCl 분리막 20 µm | 복합 양극 | 집전체 반쪽 셀의 **3D 방전 (AM 안 3D Fick · AM/CBD/CC 옴 · SE 옴 (t⁺ = 1) · AM–SE 접촉 Butler–Volmer · 외력 없음 · AM 부피 변화 없음)** 을 C/5–C/50 으로 풀고, GeoDict 로 SE 상의 τ_g = √(φ_SE/D_eff) · δ_ion · δ_e 와 상 사이 비계면적을 셌다 — 캘린더링이 셀수록 용량이 크고 (C/5: Cal0% ≈38 · Cal20% ≈63 (인쇄 62.8) · Cal35% ≈92 mAh/g [판독 그림 3e]), 리튬화가 고르고 (그림 4 · 영상), SE 전위 강하가 크게 줄며 (C/10 · 50 mAh/g 에서 ≈0.090 → ≈0.017 V [판독 그림 6b]), τ_g 는 ≈10.2 → ≈4.3 [판독] 으로 준다 (p.4–8).  **이 논문 안에 실험 대조는 없다** (저자: *"Our future work will involve experimental studies to directly compare the simulation results with experimental data"* p.9).

| 1저자가 꼭 뽑으라 한 것 (이 묶음 N-18) | 이 논문이 주는 것 | 표지 · 위치 |
|---|---|---|
| ① ★ 흐름 전체 — 슬러리 · 건조 · 캘린더링 모의 = 어떤 방법 · 매개변수 · 압력 | 방법 = **CGMD (거친 입자 분자 동역학 · LAMMPS [22])** — *"based on applying force fields/contact forces representing the interaction between particles and their mechanical properties, and these force fields were parameterized to match experimental properties"* (p.2) · 세 단계 = 슬러리 준비 · 건조 (*"the CBD particles containing solvent shrunk to the diameter corresponding to the solid size"*) · 캘린더링 (*"a plane moving downward at constant speed to compress the electrode while maintaining the bottom surface fixed"*) · 탄소와 바인더를 나누지 않는다 · **매개변수 · 힘장 · 하강 속도 · 입자 수 = 이 논문에 없음 → [13] [23–25] 에 맡김** · **압력 = 없음** (캘린더링 정도 = 두께 감소 % · *"due to the applied calendering pressure"* 라고만) · 정본 alabdali2023 카드 [다른 카드]: LJ 12-6 + granular Hertz (LAMMPS `lj/cut` + `granular`) · 건조 k_n 100 pg µm⁻¹ µs⁻² (= 1 × 10⁵ Pa) · 마찰 X_µ 12.5 · NPT 300 K · AM 중심 ≈10 µm · SE 7 계급 ⌀1–8 µm | [인쇄] p.2 · [미확인] · [다른 카드] |
| ② ★ 넘김 — 무엇을 · 언제 · 어떻게 · 메시 · 겹침 처리 · 해상도 | **무엇** = 상 배치 (기하) 만 · **언제** = 캘린더링이 끝난 상태 — 표 S1 두께 36.8 · 29.9 µm 가 정확히 46 × 0.80 · × 0.65 [카드 산술] = **목표 두께 그대로 (되튐 없음)** · 제하 · 판 분리 · 이완 서술 없음 [미확인] · 전기화학은 *"without the application of any external forces, with the calendering process applied exclusively before"* (p.3) · 응력 넘김 없음 · **어떻게** = ⓐ 겹침 우선 AM → SE → CBD · *"For each instance of overlap between AM and CBD or between AM and SE, we adjust the volume calculations by reducing the volume attributed to the CBD and adding this reduced volume to the AM or SE, respectively"* (p.3) → 구 → 불규칙 모양 ⓑ INNOV [27, 28] *"relies on a voxelization technique to create multi-phase volumetric meshes"* (p.3) · **복셀 크기 · 요소 수 · 메시 종류 · 수렴 = [미확인]** | [인쇄] p.2–3 · 표 S1 · 그림 2b · S2 · [카드 산술] |
| ③ ★ 3D 전기화학 — 식 · 물성 · 경계 · 풀이기 | 식 (1)–(6) (§3-3) · 영역 4 상 AM · CBD · SE · CC · 음극 = Li 박 표면 (BV · i0 3 A cm⁻² · SOC 무관) · 경계 = 음극 표면 φ_s,ext = 0 (Dirichlet) + CC 자유단 전류 (방전율) · 물성 = 표 S2 (SE δ_ion 0.7 · AM δ_e 100 S/m · CBD 200 S/m · CC 300 S/m · CC/AM · CC/CBD 접촉 2 × 10⁻³ Ω m² · NMC622 C_spec 200 mAh/g · c_max 49 mol/L · ρ 4.77 g/cm³ · L_SE 20 µm · L_CC 10 µm · i0c · D_AM · V0 = refs [17] · [31]) · 풀이기 COMSOL Multiphysics · 2.6–4.2 V · C/5 · C/10 · C/20 · C/50 | [인쇄] p.3–4 · 표 S2 |
| ④ ★ 각 단계 검증 (실험 기공 · 두께 · 방전 곡선) | **이 논문 안에는 없다** — 기공 · 두께 · 방전 곡선 어느 것도 실험과 견주지 않았다 (*"the model accurately captures the loss of specific capacity while increasing the C-rate"* p.4 = 실험 없는 자기 서술) · 제조 모델의 실험 대조는 [13] 몫 (정본 alabdali2023 카드: 슬러리 밀도 1.90 ↔ 1.89 g/cm³ · 점도-전단율 · 건조 기공 문헌 ≈50 % (CBD 나노 기공 가정) — 캘린더링 단계는 탐색이지 검증 아님 [다른 카드]) | [인쇄] p.4 · p.9 · [다른 카드] |
| ⑤ ★ 계산 비용 | COMSOL = MatriCS 1 노드 · **500 GB RAM** · Xeon E5-2680 v4 2.40 GHz **28 코어** (p.4) · GeoDict = *"standard desktop computer"* (p.4) · 실행 시간 · 자유도 · 메시 크기 [미확인] | [인쇄] p.4 |
| ⑥ ★ 영상이 보여 주는 것 | mmc2 · mmc3 · mmc4 = COMSOL 애니메이션 *"Surface: Concentration (mol/m³)"* (AM 표면 Li 농도 · 색 0 → 4.9 × 10⁴ = c_max 49 mol/L) · *"C_rate(1)=0.02"* (= C/50) · Time 0 → 24.93 → 49.95 h · 생김새로 mmc2 = Cal0% · mmc3 = Cal20% · mmc4 = Cal35% (그림 4 와 같은 시점 · 같은 입자 배치) · 처음 농도 ≈ 0.2 c_max · 끝 프레임 하위 5 % 농도 ≈ 0.56 (Cal0%) · 0.71 (Cal20%) · 0.89 c_max (Cal35%) [판독 · 대강 · 3D 음영 포함] · **본문은 영상을 가리키지 않는다** | 영상 프레임 0 · 36 · 71 [판독] |
| ⑦ ★ 저자 한계 | 모델 쓸 범위 ≤35 % (그 위에서 CBD 부피 잠식 → 전기전도 감소) · AM 부피 변화 미반영 (*"we did not account for the volume change in AM during lithiation"*) · 부산물 · 접촉 손실 불확실 → 깨끗한 AM 매개변수 · 음극 i0 크게 · 단축 캘린더링이 산업 율속에 못 미침 (*"maximum of 200 mAh/g at a low C-rate of C/50"*) · 등방 압축 필요 · 앞으로 = AM 부피 변화 · 실험 대조 (p.2 · p.4 · p.9) | [인쇄] |
| ⑧ DEM · 소성 · 2D/3D · 탈압 (이 묶음 네 질문) | DEM 한계 = ≤35 % 문장 하나 (§4-3) · 소성 = 말 없음 (모양 변화는 겹침 후처리의 기하 결과) · **3D (+ 시간 = '4D')** · 2D ↔ 3D 말 없음 · 탈압 = 다루지 않음 (넘긴 구조 = 목표 두께 · 외력 없음) | [인쇄] p.2–3 · p.9 |
| ⑨ 우리 쪽 — 질문 h · DEM → MPM → STEP3/4 와 단계별로 | §7-1 표 — 넘기는 시점 (둘 다 '누른 상태' · 우리 = 300 MPa 도달 후 판 고정 이완 덤프 → MPM 재압밀) · 겹침 처리 (둘 다 AM 우선 · 그들 = CBD 부피 이동 · 우리 = MPM SE 씨앗은 AM 아닌 칸에만 · DEM ε_sphere ↔ ε_union) · 해상도 (그들 [미확인] ↔ 우리 MPM dx 0.141 µm · STEP3 0.4 / 0.15 µm · STEP4 0.8 / 0.4 µm) · 전기화학 (그들 AM 안 3D Fick ↔ 우리 STEP4 입자별 구형 1D) · 검증 (그들 없음 ↔ 우리 기공 · 두께 · σ 앵커) | §7-1 |

⛔ **한정어 (떼지 말 것)**: ① **실험 없는 순수 계산** — 방전 곡선 · 용량 · τ · σ · 피복 모두 모델 값 ② 제조 모델 (CGMD) 의 매개변수 · 힘장 · 하강 속도 · 입자 수가 **이 논문에 없다** ([13] 몫) ③ **압력 축이 없다** — 캘린더링 = 두께 감소율 (0 · 20 · 35 %) ④ **복셀 크기 · 메시 · 자유도 · 실행 시간 미기재** ⑤ GeoDict 수송 계산과 COMSOL 전기화학의 **입력 전도도가 다르다** (σ_AM 0.005 ↔ 100 S/m · σ_CBD 15.93 ↔ 200 S/m · σ_SE 1.25 ↔ 0.7 mS/cm — §3-9) ⑥ 기공 17 · 13 · 6 % 는 CBD (38–40 vol%) 를 고체로 센 값이고 (1 − ε) × 두께가 보존되지 않는다 (−16 · −26 % · §3-9) ⑦ 재료 = NMC622 + Li₆PS₅Cl (우리와 같은 SE 화학) 이나 습식 CBD 가 40 vol% 가까이 들어간 양극 (우리 건식 · 탄소/바인더 적은 침대와 다름).
⇒ **절대값 전이: 0 건** (압밀 · 탈압 · 수송 절대값으로 쓸 숫자 없음).  전이되는 것은 **사슬의 모양** (제조 모의 → 겹침 후처리 → 복셀 메시 → 3D 전기화학) · **넘김 연산자를 글로 적는 꼴** (우선순위 · 부피 이동 규칙) · **함정 셋** (부피 보존 위반 · 계산마다 다른 입력 σ · 'geometric' 이라 부른 √(φ/f)) · **경향** (캘린더링 → SE 망 연결 · τ ↓ · 율속 ↑ · 리튬화 균일).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-18 의 '왜' 칸)

의도 원문: *"h — 제조 모의 미세구조 → 3D 전기화학 방전으로 넘긴 선례 (습식 · 단축 캘린더링 → 전기화학 · 넘긴 시점과 방법) · "우리 DEM → STEP4 와 같은 사슬 · 정본 카드 없음" (zhang2026) · "같은 사슬의 1 편" (benhadjali2026)"* (가리킨 카드 = `zhang2026_polymer_electrolyte_modeling_perspective` L64 · L121 · `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` L441)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "h — 제조 모의 미세구조 → 3D 전기화학 방전으로 넘긴 선례" | **채움** | p.2 §2 *"Our computational modeling workflow consists of two main parts. The first part is already published [13] … The second part is devoted to the simulation of the electrochemical behavior of the electrodes upon discharge by using the Finite Element Method (FEM)"* · 그림 1 · 2 · S2 · 방전 = 반쪽 셀 · 2.6–4.2 V · C/5–C/50 (p.4 · 그림 3) |
| "(습식 · 단축 캘린더링 → 전기화학" | **채움** | 습식 = 슬러리 · 건조 · 캘린더링 CGMD (p.2) · 단축 = *"a plane moving downward at constant speed … bottom surface fixed"* (p.2) · *"conventional calendering method employed, which involves uniaxial compression"* · *"conventional unidirectional rolling calendering techniques"* (p.9) · 두께 감소 0 · 20 · 35 % · **압력 값 없음** |
| "· 넘긴 시점" | **일부** | 넘긴 시점 = **캘린더링 목표 두께에 닿은 구조** — 표 S1 두께 46 · 36.8 · 29.9 µm = 46 × 1 · 0.80 · 0.65 [카드 산술] → 되튐 (springback) 이 없다 · 전기화학은 외력 없이 · 캘린더링은 그 전에만 (p.3) · ⚠ 판을 뗐는지 · 이완 단계가 있었는지 · 그때의 응력은 **원문에 없다** [미확인] (정본 alabdali2023 카드: *"springback n/a — 평판을 떼는 서술 없음"* [다른 카드]) |
| "과 방법)" | **일부** | 방법 = 겹침 우선순위 AM → SE → CBD + CBD 부피를 AM 또는 SE 로 옮김 (p.3) + INNOV 복셀화 다상 체적 메싱 [27, 28] (p.3) · **복셀 크기 · 요소 수 · 메시 수렴 [미확인]** · 이 규칙으로 (1 − ε) × 두께가 Cal0 → Cal35 에서 −26 % 줄어드는 것은 원문이 설명하지 않는다 (§3-9 ⑤) |
| "우리 DEM → STEP4 와 같은 사슬" (zhang2026) | **채움 (같은 자리 · 다른 부품)** | 사슬 자리는 같다 (입자 제조 모의 → 복셀 → 3D 전기화학 방전) · 다른 부품: 그들 = CGMD (LJ + Hertz · 변위 제어) → 겹침 후처리 → COMSOL FEM (AM 안 3D Fick) · 우리 = DEM (하중 제어 300 MPa) → MPM (SE 소성 재압밀) → STEP3 복셀 FV → STEP4 (입자별 구형 1D 확산) — §7-1 |
| "· 정본 카드 없음" (zhang2026) | **채움** | 2026-11-12 정본 `litdb/papers/` 파일 목록 + DOI (`jpowsour.2024.236131` · `236131`) · 제목 낱말 grep — 이 논문 카드 없음 (benhadjali2026 · zhang2026 에 인용만) → 이 카드가 첫 카드 |
| "같은 사슬의 1 편" (benhadjali2026) | **채움** | 같은 그룹 · 같은 NMC622 / LPSCl 습식 사슬의 **역학 없는** 판 — 2026 판 (ChemRxiv) 은 같은 사슬에 선형 탄성 + 리튬 고유변형 · 응력 의존 화학 퍼텐셜을 얹고 CUP ↔ WIP 실험을 붙였다 [다른 카드] · 이 논문 결론의 *"isostatic pressing rolling technology need to be considered in the future"* (p.9) 가 2026 판의 주제가 되었다 [카드 해석] |

**가리킨 카드 · 같은 논문을 옮긴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `zhang2026_…` L64 | *"Ben Hadj Ali 2025 (제조 모의 미세구조 → 3D 전기화학 방전, ref 36; 완전결합 기계-전기화학, ref 164)"* | 이 논문 = 제조 모의 미세구조 → 3D 전기화학 방전 (역학 결합 없음) | **채움** (ref 36 부분) |
| `zhang2026_…` L121 | *"36 · Ben Hadj Ali, S.; Alabdali, M.; Viallet, V.; Seznec, V.; Franco, A. A. … J. Power Sources 2025, 630 · 제조 모의 → 3D 전기화학 (ASSB) — 우리 DEM → STEP4 와 같은 사슬 (정본 카드 없음)"* | 저자 · 제목 · 학술지 · 권 · 연도 같음 (쪽 = 논문 번호 236131 은 그 줄에 없음) | **채움** |
| `benhadjali2026_…` L441 | 서지 *"… Journal of Power Sources 630 (2025) 236131. https://doi.org/10.1016/j.jpowsour.2024.236131."* + *"같은 사슬의 1 편 (습식 · 단축 캘린더링 → 전기화학) · 우리 DEM → STEP4 와 같은 자리"* | 서지 같음 · 습식 · 단축 · 전기화학 같음 | **채움** |
| `benhadjali2026_…` L295 (§6 τ 규약) | *"같은 그룹 Alabdali 2023 은 τ = √(η/D_eff) 로 셌다 … 이 논문 'geometric tortuosity' 의 정의 [미확인]"* | 이 논문 식 (7) 이 **τ_g = √(φ_SE/D_eff)** 를 인쇄 (p.4) · 그림 8a 의 τ_g 와 그림 8b 의 δ_ion 이 Cal20 · Cal35 에서 그 식을 1 % 안에서 맞춘다 [카드 산술 §3-8] | **일부** — 같은 그룹의 정의는 확인 · 2026 판 자체의 정의는 그 원문 몫 (여전히 미확인) |
| `benhadjali2026_…` L450 (ref [39] 줄) | *"복셀 메싱 (겹친 구를 어떻게 하나의 고체로 잇는지 = 기공 정의 §10-5 의 열쇠)"* | 이 논문 §2.2 가 겹침 규칙 (AM → SE → CBD · CBD 부피 이동) 을 인쇄 (p.3) | **일부** — 같은 그룹 규칙 하나는 확인 · 2026 판이 같은 규칙을 썼는지는 미확인 |
| `sankar2026_…` L45 | *"ref 64 Ben Hadj Ali 2025"* (서지 없음) | — | **미확인** (서지 일부만 · 이 논문인지 그 카드로 못 가림) |

⇒ **의도 대조 결과: 채움 (h 선례 · 습식 · 단축 캘린더링 → 3D 전기화학 · 같은 사슬의 1 편 · 정본 카드 없음 · zhang2026 · benhadjali2026 서지) · 일부 (넘긴 시점 = 목표 두께 그대로 · 되튐 · 응력 · 판 분리 미기재 / 넘긴 방법 = 겹침 규칙 · INNOV 복셀 메싱은 있으나 복셀 크기 · 메시 · 수렴 미기재) · 없음 (각 단계의 실험 검증 · 압력 값)**.

---

## 1. 한 줄 요약
고체 전지 복합 양극의 전기화학 성능을 '제조 공정 모의가 만든 미세구조' 위에서 처음 계산했다는 작업 흐름 논문이다 — 같은 그룹의 CGMD 습식 제조 모의 (슬러리 → 건조 → 단축 캘린더링) 가 만든 0 · 20 · 35 % 압연 구조를 겹침 후처리와 복셀 메싱으로 COMSOL 에 넘겨 3D 방전을 풀었다.  캘린더링이 셀수록 AM–SE 접촉 면적이 늘고 SE 이온 경로의 굴곡 (τ_g ≈10 → ≈4) 과 SE 전위 강하가 줄어 고율 용량이 크게 오르고 (C/5 ≈38 → ≈92 mAh/g [판독]), 저율에서는 차가 작아진다 (C/50 ≈172 → ≈197 [판독]).  역학 (응력 · 부피 변화 · 되튐) 과 실험 대조는 없다 — 저자는 단축 압연의 한계와 등방 압축 · AM 부피 변화 · 실험 대조를 다음 일로 적었다.

## 2. 메타

| 저자 | 판 | DOI | 소재 (AM / SE / C · 바인더) | 연구 유형 |
|---|---|---|---|---|
| S. Ben Hadj Ali · M. Alabdali · V. Viallet · V. Seznec · A.A. Franco\* (LRCS · RS2E · ALISTORE-ERI · IUF) | J. Power Sources 630 (2025) 236131 · CC BY 4.0 · 10 쪽 + SI docx + 영상 3 | 10.1016/j.jpowsour.2024.236131 | NMC622 / Li₆PS₅Cl / CBD (탄소 + 바인더 한 상 · 구분 안 함) — 조성 wt% 이 논문에 없음 [미확인] (원 침대 = 정본 alabdali2023 69.0 : 27.6 : 3.4 wt% [다른 카드]) | 계산만 — CGMD 제조 미세구조 재사용 + 후처리 · 복셀 메싱 + COMSOL 3D 전기화학 FEM + GeoDict 복셀 수송 |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 사슬과 침대 셋 (p.2 · 표 S1 · 그림 2 · 그림 S1 · S2 · `tab_S1.png` · `fig_2cf.png` · `fig_S2.png` · `fig_S1g.png`)

| 항목 | 값 | 표지 · 위치 |
|---|---|---|
| 제조 모의 | CGMD · LAMMPS [22] · 슬러리 → 건조 → 캘린더링 · *"These simulations account for the AM, the SE and the CBD but it does not distinguish explicitly between carbon and binder"* · 힘장 = 실험 물성에 맞춰 매개변수화 | [인쇄] p.2 · `txt_p2_model_description_cgmd_steps.png` |
| 건조 | *"the CBD particles containing solvent shrunk to the diameter corresponding to the solid size to mimic the evaporation of the solvent"* · 지름 값 [미확인] (정본 alabdali2023: ⌀7.5 → 3.0 µm 순간 축소 [다른 카드]) | [인쇄] p.2 |
| 캘린더링 | 평판 등속 하강 · 바닥 고정 · 캘린더링 정도 = *"a different percentage of reduction of the thickness due to the applied calendering pressure"* · 속도 · 압력 [미확인] | [인쇄] p.2 |
| 쓸 범위 | *"The usability of this model is limited for calendering degrees under or equal to 35 %, as it was discussed in Ref. [13] because above 35 % a decrease in the electrical conductivity was observed due to the partial occupation of the volume of CBD particles by other materials due to high pressure."* | [인쇄] p.2 · `txt_p2_calendering_degrees_35pct_limit.png` |
| 상자 | **41 µm × 41 µm × 46 · 36.8 · 29.9 µm** (그림 S2 의 화살표 표기) | [인쇄 그림] SI p.3 |
| 표 S1 — 캘린더링 (%) | 머리 = **0 · 10 · 35** — 가운데는 20 이어야 한다 (46 × 0.80 = 36.8 · 본문 · 그림 2 · S2 = 0 · 20 · 35) | [인쇄] · [카드 산술] |
| 표 S1 — 두께 (µm) | **46 · 36.8 · 29.9** | [인쇄] |
| 표 S1 — AM : SE : CBD (vol%) | **22 : 21 : 40 · 23 : 25 : 39 · 29 : 27 : 38** | [인쇄] |
| 표 S1 — 기공 (%) | **17 · 13 · 6** (각 열 합 100) | [인쇄] |
| 그림 2c–f 판독 | CBD **41.0 · 40.1 · 37.9** · SE **21.0 · 25.1 · 27.1** · AM **22.0 · 22.9 · 28.9** · 기공 **17.0 · 12.0 · 6.1** % (Cal0% 합 101.0) | [판독 ±0.2 %p · 원본 래스터 틀선 보정] |
| SE 입도 (그림 S1g · 모델 입력) | 지름 1–2 · 2–3 · … · 7–8 µm = **7 · 22.5 · 25.7 · 22.1 · 11.1 · 7.12 · 4.48 %** (막대 위 인쇄 · 합 100.0) · 개수 평균 지름 ≈3.97 µm [카드 산술: 계급 가운데값 가중] · 측정 = 습식 볼밀 SE 의 SEM (그림 S1a–f · *"Adapted with permission from Alabdali et al. [S1]"*) | [인쇄 그림] · [카드 산술] |
| AM 크기 · 입자 수 | 이 논문에 없음 — AM 비표면 0.16 m²/g (p.7) ↔ 구 등가 지름 **≈7.9 µm** [카드 산술: d = 6/(ρ S) = 6/(4.77 g/cm³ × 0.16 m²/g)] · 정본 alabdali2023: AM 중심 ≈10 µm · 전 입자 5089 개 [다른 카드] | [미확인] · [카드 산술] |

### 3-2. ★ 넘김 — 후처리 · 메싱 (p.2–3 · 그림 2b · S2 · `txt_p2_p3_overlap_postprocessing.png` · `txt_p3_meshing_innov_voxelization.png`)

- **겹침 처리 (§2.2)**: *"During this step, overlaps are handled based on the prioritization of the AM then the SE and finally the CBD. For each instance of overlap between AM and CBD or between AM and SE, we adjust the volume calculations by reducing the volume attributed to the CBD and adding this reduced volume to the AM or SE, respectively. This adjustment implicitly considers the porosity of the CBD by reducing its presence in overlapping regions, as one knows that CBD can be porous [26]. Moreover, it reflects the spatial redistribution of material, leading to the transformation of the initially spherical particles into more realistic, irregular shapes for AM, SE and CBD. This approach has been used in our group previously for LIB electrodes simulation [24]."* [인쇄 p.3]
  - [카드 해석] 문장대로면 AM–SE 겹침에서도 'CBD 부피를 줄여' SE 에 더한다 — AM–SE 겹침에 CBD 가 없으면 뜻이 서지 않는다 · 세 상이 겹친 자리 · SE–CBD 겹침 · 같은 상끼리 겹침 (AM–AM · SE–SE) 의 처리는 원문에 없다 [미확인].
- **메싱**: *"The meshes have been generated with our in house software INNOV [27, 28], which relies on a voxelization technique to create multi-phase volumetric meshes for FEM calculations."* [인쇄 p.3] · 그림 2b = 메시 표면 (삼각형) · 그림 S2 = '입자 미세구조 → 3D 재구성 기하 → 다상 메시' 세 줄 · **복셀 크기 · 요소 종류 · 요소 수 · 계면 처리 · 메시 수렴 = [미확인]** (본문에 'µm' 숫자가 하나도 없다 — 두께는 표 S1 · 그림 S2 에만).
- **넘긴 시점 · 상태**: 캘린더링이 끝난 구조 · *"The electrochemical evaluation of the ASSB cell is conducted without the application of any external forces, with the calendering process applied exclusively before the electrochemical simulation. This approach allows us to isolate and analyze the intrinsic effects of calendering on the cell performance."* [인쇄 p.3] · 두께 = 목표 그대로 (46 × 0.80 = 36.8 · 46 × 0.65 = 29.9 [카드 산술]) ⇒ **되튐이 없는 '누른 상태'의 기하** [카드 해석] · 응력 · 접촉력 · 겹침량은 넘기지 않음.
- **CBD 다공성**: 메시에서는 CBD 를 한 상으로 · *"The porosity of CBD is accounted implicitly in the electrochemical model through the transport parameters of CBD"* [인쇄 p.4].

### 3-3. ★ 3D 전기화학 모델 (§2.3 · 식 (1)–(6) · 표 S2 · `eq_01`–`eq_06` · `tab_S2.png` · `txt_p3_p4_…` · `txt_p4_bc_…`)

| 식 | 내용 (렌더 확인) | 표지 · 위치 |
|---|---|---|
| (1) | ∂C_s/∂t = −∇(−D_AM ∇C_s) — AM 입자 안 Li 확산 (3D · 복셀 메시 모양 그대로) · D_AM = SOC 의존 · *"derived from the experimental data reported by Bielfeld et al. [31]"* ([31] = Ruess 외 2020 · Bielefeld 는 다섯째 저자 · 철자 'Bielfeld' 오기) | [인쇄] p.4 · `eq_01_fick_diffusion_am.png` |
| (2) | ∇(−δ_e,i ∇φ_s) = 0 — AM · CBD · CC 의 전자 전위 (옴) · δ_e,i = 그 영역의 유효 전자 전도도 | [인쇄] p.4 · `eq_02_…` |
| (3) | ∇(−δ_ion ∇φ_SE) = 0 — SE 의 이온 전위 (전하 보존) · **t_Li⁺ = 1** (*"This results in negligible lithium ion concentration gradients in the SE"*) | [인쇄] p.4 · `eq_03_…` |
| (4) | J_BV = i0 [exp(F η/2RT) − exp(−F η/2RT)] — AM–SE 접촉의 Butler–Volmer (α 0.5 대칭 · 표 S2 α_c 0.5) · i0 = SOC 의존 · ref [17] (Bielefeld 2022) | [인쇄] p.4 · `eq_04_butler_volmer.png` |
| (5) | R_CT = RT/(zFAi0) — i0 를 EIS 로 잰 R_CT (*"measured … on similar interfaces [31]"*) 에서 얻는 관계 · A = 활성 면적 · z = 1 | [인쇄] p.4 · `eq_05_…` |
| (6) | η = φ_AM − φ_SE − V0^NMC622 — V0 = *"adapted from data in Ref. [31] for a NMC half-cell discharged at a C/10 rate in the first cycle"* | [인쇄] p.4 · `eq_06_overpotential.png` |

- **음극**: Li 박 · *"we model the stripping of lithium metal by the Butler-Volmer equation as well. However, as this work is focused on the composite cathode, we assume a high exchange current density which is independent from the anode's SOC"* (p.4) · 표 S2: α_a 0.5 · **i0a = 3 A cm⁻² ("Exchange current density factor")** · V0Li 0 V.
- **경계**: *"Dirichlet boundary condition on the electric potential on the anode surface (φ_s,ext = 0) and a current flux boundary condition at the free end of the CC to match the desired discharge rate"* (p.4) · 옆면 (xz · yz) 경계 · 상 사이 계면 조건 (AM–AM · AM–CBD · CBD–CC 연속인지) = [미확인] (주기 경계 문장은 GeoDict 절 (§2.4) 에만 있다).
- **넣지 않은 것**: *"In this model and in contrast to our previous work in Ref. [32], we did not account for the volume change in AM during lithiation. As the formation of side products and the loss of contact area due to swelling and shrinking of the AM introduces significant uncertainties in the kinetic parameters, therefore we extract AM parameters at the pristine state from previous studies."* (p.4).
- **표 S2 전부** [인쇄 SI]: 음극 α_a 0.5 · i0a 3 A cm⁻² · V0Li 0 V / SE: L_SE **20 µm** · δ_ion **0.7** *"mS.cm-2"* (단위 오기 — 전도도 [S2]) / 양극 NCM622: L_C *"See Figure S2"* · i0c *"See reference"* [S2] (A m⁻²) · α_c 0.5 · V0 *"See reference"* [S3] · D_AM *"See reference"* [S3] (m² s⁻¹) · C_spec **200 mAh g⁻¹** · c_max **49 mol L⁻¹** · ρ **4.77 g cm⁻³** (*"Gravimetric density"* — 질량 밀도) · δ_e,AM **100 S m⁻¹** / CBD: δ_e,CBD **200 S m⁻¹** / CC: L_CC **10 µm** · δ_e,CC **300 S m⁻¹** · R_CC_AM **2 × 10⁻³ Ω m²** [S4] · R_CC_CBD **2 × 10⁻³ Ω m²** (= 20 Ω cm² [카드 산술]).
  - [카드 산술] c_max 49 mol/L 로 셈한 NMC622 이론 용량 = 49 × 26.80 Ah/mol ÷ 4.77 kg/L ≈ **275 mAh/g** → C_spec 200 mAh/g = c_max 의 ≈73 %.
- **운전 · 풀이**: 2.6–4.2 V vs Li⁺/Li · C/5 · C/10 · C/20 · C/50 (p.4) · 1C 의 정의 [미확인] · COMSOL Multiphysics [29] (6.2 문서 링크) · MatriCS 1 노드 500 GB RAM · Xeon E5-2680 v4 28 코어 (p.4) · 시간 · 자유도 [미확인].

### 3-4. 수송 계산 — GeoDict (§2.4 · 식 (7)–(9) · `txt_p4_charge_transport_geodict.png` · `eq_07`–`eq_09`)

- 도구 = GeoDict 2023 (Math2Market) ConductoDict · DiffuDict · *"using a standard desktop computer"* · *"δ and τg are two chosen parameters to provide a quantitative indication … They are simple observables"* (p.4).
- **δ_e**: 영역 안 Poisson · z 방향 (캘린더링 면에 수직) **1 V** · Ohm 법칙 · σ_AM **0.005 S m⁻¹** · σ_CBD **15.93 S m⁻¹** [34–36] (p.4).  ⚠ 표 S2 의 FEM 입력 (100 · 200 S m⁻¹) 과 다르다 (§3-9 ⑦).
- **τ_g** (식 7 · 렌더 확인): **τ_g = √(φ_SE / D_eff)** · φ_SE = SE 부피 분율 · D_eff = SE 상 안 Fick 1 법칙 · 바깥 xy 면 사이 Δc (식 8: **D_eff = −j × length / Δc**) · *"Since τg is only a geometrical magnitude, it is independent of the values chosen for Δc and the diffusion coefficient within the SE"* (p.4).
- **δ_ion** (식 9): **N_M = D_eff / D_bulk = δ_ion / δ_bulk** (*"McMullin number [37]"*) · **D_bulk = 1 m² s⁻¹** · **δ_bulk = 1.25 mS cm⁻¹** (*"provided by the supplier"*) · 입력 등방 · **바깥 xz · yz 면 주기 경계** (p.4).  ⚠ 표 S2 의 FEM SE 입력은 0.7 (§3-9 ⑦) · [37] 은 [25] 와 같은 논문 (유기 Na 이온 전극 제조) 의 중복 번호 — McMullin 수의 원전으로 보기 어렵다 [카드 해석] (§3-9 ⑪).
- [카드 해석] D_bulk = 1 이면 D_eff 는 무차원 **f** (= σ_eff/σ₀) 와 같다 → 그들 τ_g = √(φ/f) = **우리 tau (√tau2 · flux τ)** · 그들 N_M = **f** (문헌 McMullin N_M = 1/f 의 역수) · *"geometrical"* 이라 불렀으나 최단 경로 τ_geo 가 아니라 확산 해에서 나온 수송량 (우리 τ 규약 · §7-3).

### 3-5. 방전 곡선 · 용량 (그림 3 · `fig_3.png` · `fig_3e.png` · `txt_p4_p5_results_capacity_c_rate.png`)

| C-rate | Cal0% | Cal20% | Cal35% | 표지 |
|---|---|---|---|---|
| C/5 | **38.2** | **62.7** (인쇄 **62.8**) | **92.2** | [판독 그림 3e] · [인쇄] p.4 |
| C/10 | 81.1 | 114.1 | 140.0 | [판독] |
| C/20 | 127.7 | 156.6 | 174.2 | [판독] |
| C/50 | **171.8** | **188.4** (인쇄 **188.28**) | **197.3** | [판독] · [인쇄] p.4 |

- 단위 mAh g⁻¹ · 2.6 V 끝 · 판독 = 원본 래스터 · 왼쪽 축 눈금 11 개 (0–200) 선형 맞춤 (잔차 ≤0.3 mAh/g) · **Cal20% 인쇄값 둘을 0.1 안에서 재현**.  ⚠ y = 200 눈금은 틀 위선이 아니라 그 아래에 있다 (틀 위 = ≈205 [판독]).
- [카드 산술] Cal35%/Cal0% = **2.41 배 (C/5)** · 1.73 (C/10) · 1.36 (C/20) · **1.15 (C/50)** — 저자 해석: 고율 = 운동학 (전하 수송 · 활성 면적 · 분극) 지배 · 저율 = 열역학 지배 (p.5).
- 결론의 *"the capacity reaches a maximum of 200 mAh/g at a low C-rate of C/50"* (p.9) ↔ 그림 3e 최대 ≈197.3 [판독] · 200 = 표 S2 의 C_spec 입력값.
- 방전 곡선 (그림 3a–d): 4.1–4.2 V 에서 시작 · ≈3.6–3.7 V 고원 · Cal0% C/5 는 ≈3.45 V 에서 꺾여 급강 [판독 · 눈대중].

### 3-6. 리튬화 · 이온 전류 · 과전압 · 영상 (그림 4–6 · `fig_4.png` · `fig_5.png` · `fig_6a`–`fig_6d` · `txt_p5_…` · `txt_p6_…`)

- **그림 4 (C/50 · AM 안 [Li]/[Li_max] · 0–1)**: 3.9 · 3.65 · 2.6 V = **25 · 75 · 100 % DOD** (p.5) · 위 = 분리막 쪽 · 아래 = 집전체 쪽 · Cal35% = 전체가 고르게 · Cal0% = *"localized lithiation, which is due to a reduced number of percolating pathways"* (p.5) — DOD 100 % 에서 Cal0% 는 가운데 · 아래 일부 입자가 ≈0.3–0.5 로 남는다 [판독 색 · 눈대중].
- **그림 5 (가운데 방전 · C/50 · 국소 이온 전류 밀도 0–14 mA cm⁻²)**: 3D + x = 10 · 20 · 30 µm 단면 · Cal0% 에 좁은 고전류 통로 (병목) · *"increased bottlenecks (i.e. localized regions where ion movement is significantly restricted) impede ion flow in the uncalendered electrode"* (p.5).
- **그림 6a · 6b 판독 [판독 · 원본 래스터 · 눈금 맞춤]** (V · 50 mAh/g 지점 / 곡선 끝):

| 양 · C-rate | Cal0% | Cal20% | Cal35% |
|---|---|---|---|
| 활성화 과전압 · C/10 | 0.079 / 0.059 (끝 ≈82 mAh/g) | 0.077 / 0.055 | 0.071 / 0.053 |
| 활성화 과전압 · C/20 | 0.055 / 0.040 | 0.048 / 0.035 | 0.044 / 0.035 |
| 활성화 과전압 · C/50 | 0.027 / 0.022 | 0.020 / 0.016 | 0.020 / 0.018 |
| SE 전위 · C/10 | **0.090** / 0.187 | 0.037 / 0.088 | **0.017** / 0.041 |
| SE 전위 · C/20 | 0.064 / 0.173 | 0.026 / 0.078 | 0.012 / 0.036 |
| SE 전위 · C/50 | 0.039 / 0.139 | 0.015 / 0.067 | 0.006 / 0.031 |

  - [카드 산술] C/10 · 50 mAh/g 에서 Cal0% → Cal35%: 활성화 과전압 −0.008 V (−10 %) ↔ SE 전위 −0.073 V (−81 %) — **캘린더링이 줄인 손실의 대부분은 SE 이온 경로 (옴) 쪽** 이고 활성화 쪽 차는 작다 · 본문은 *"Cal0% exhibits a much higher activation overpotential (η_act) compared to Cal20% and Cal35%, primarily due to the lower active area"* (p.6) 로 활성 면적을 앞세운다 (그림 6c 의 끝 시점 지도 · 그림 6a 평균값으로는 C/10 에서 10 % 차).
- **그림 6c**: C/50 방전 끝 AM–SE 반응 계면의 η_act (0–0.1 V) 3D · **6d**: 활성 (AM–SE) 면적 분포 3D — Cal35% 가 더 촘촘하고 이어진 면 (정성).
- **영상 mmc2–4** (본문 언급 없음 · 각 2.4 s · 72 프레임 · 640 × 480 · h264): COMSOL *"Surface: Concentration (mol/m³)"* · 색 막대 0 → ≈4.9 × 10⁴ (= c_max 49 mol/L — 눈금 0.5 간격 보정 [판독]) · *"C_rate(1)=0.02"* · Time **0 → 24.93 → 49.95 h** · 생김새 = 그림 4 의 세 침대 (mmc2 Cal0% · mmc3 Cal20% · mmc4 Cal35%) · 색 막대 대응 (입자 화소 중앙값 · 대강): 0 h ≈ 0.20 · 0.21 · 0.21 · 24.93 h ≈ 0.59 · 0.61 · 0.66 · 49.95 h ≈ 0.99 · 1.00 · 0.99 c_max · 끝 하위 5 % ≈ **0.56 · 0.71 · 0.89** [판독 · 3D 음영 포함 · 대강].
  - ⚠ [카드 산술] C/50 를 C_spec 200 mAh/g 기준으로 두면 4 mA/g × 49.95 h ≈ 199.8 mAh/g — 그런데 Cal0% 는 2.6 V 에서 ≈172 mAh/g (≈43 h) 에 끝난다 [판독 그림 3e] → 세 영상이 모두 49.95 h 까지 가는 까닭 (정지 조건 · 1C 정의) 은 [미확인].

### 3-7. 계면 면적 · AM 피복 (§3.1 · 그림 7 · `fig_7a.png` · `fig_7b.png` · `txt_p7_p8_interfacial_area_coverage.png`)

| 비계면적 (m² g⁻¹) | Cal0% | Cal20% | Cal35% | 표지 |
|---|---|---|---|---|
| AM–기공 | **0.0202** | 0.0120 | **0.0045** | [판독] · 인쇄 0.02 → 0.004 (p.7) |
| SE–기공 | 0.0395 | 0.0255 | 0.0098 | [판독] |
| AM–SE | **0.0106** | 0.0129 | **0.0186** | [판독] · 인쇄 0.01 → 0.019 (p.7) |
| CBD–기공 | 0.358 | 0.231 | 0.111 | [판독] |
| AM–CBD | 0.055 | 0.057 | 0.062 | [판독] |
| SE–CBD | 0.110 | 0.102 | 0.096 | [판독] |

- 본문 (p.7): AM 비표면 **0.16 m² g⁻¹** (*"is measured at"* — 방법 [미확인]) · AM 표면 중 SE 피복 **≈10 % (Cal0%) → ≈28 % (Cal35%)** · Cal35% 에서 기공 ≈6 % · CBD **24 %** · 다른 AM **42 %** (합 100 [카드 산술]).
- [카드 산술] 위 막대와 본문 % 가 **한 분모로 맞지 않는다**: AM–SE / AM 비표면 = 0.0106/0.16 = **6.6 %** · 0.0186/0.16 = **11.6 %** (본문 10 · 28 %) · Cal35% 에서 AM–CBD / AM–SE = 0.062/0.0186 = **3.3** ↔ 본문 24/28 = 0.86 — '무엇의 g 당' 인지 · 피복 % 의 분모 · 복셀 면 넓이 추정법 [미확인] → **값보다 경향만** 쓴다.
- 해석 (p.7–8): 압력이 빈자리를 줄여 AM–SE 연결 ↑ · Bielefeld [17] 의 원뿔형 (cone-like) 구조와 같은 방향 · *"maximizing S_AM-SE and minimizing residual porosity are key to fabricating highly compact electrodes"*.

### 3-8. τ_g · δ_e · δ_ion (§3.2 · 그림 8 · `fig_8a.png` · `fig_8b.png` · `txt_p8_tortuosity_conductivity.png`)

| 양 | Cal0% | Cal20% | Cal35% | 표지 |
|---|---|---|---|---|
| τ_g (식 7) | **10.2** | **6.21** | **4.30** | [판독 그림 8a] · 인쇄 *"approximately 10"* → *"around 4"* (p.8) |
| δ_e (mS cm⁻¹) | **0.240** | 0.300 | **0.310** | [판독 그림 8b 왼쪽 축] · 인쇄 **0.24 · 0.31** (p.8) |
| δ_ion (mS cm⁻¹) | 0.0030 | 0.0080 | 0.0180 | [판독 그림 8b 오른쪽 축] · 본문 값 없음 |
| f = δ_ion / 1.25 (= 그들 N_M) | 0.0024 | 0.0064 | 0.0144 | [카드 산술] |
| √(φ_SE / f) (φ_SE = 표 S1 0.21 · 0.25 · 0.27) | 9.35 | 6.25 | 4.33 | [카드 산술] — Cal20 · Cal35 는 τ_g 판독과 1 % 안 · Cal0 는 9 % 어긋남 (τ_g 10.2 이려면 δ_ion ≈0.0025) |
| tau2 (우리 '수송 tortuosity' = τ_g²) | ≈104 | ≈38.6 | ≈18.5 | [카드 산술 · 판독 τ_g 제곱] |

- 본문 (p.8): τ_g 가 높은 까닭 = SE 입자의 고르지 않은 분포 · 이어진 이온 통로 부족 → 병목 · 캘린더링으로 SE 분포가 고르게 · δ_e 는 *"less dependence on the calendering degree"* · 그 증가는 AM–CBD 접촉 면적 증가 탓 (그림 7b).
- [다른 카드] 같은 미세구조를 쓴 원 논문 (정본 alabdali2023 카드 판독): τ_g 10.2 (0 %) · 6.1 (20 %) · 4.24 (35 %) ↔ 이 논문 10.2 · 6.21 · 4.30 [판독] — **같은 값을 다시 그렸다** · δ_e 2.43 · 3.03 · 3.15 S m⁻¹ (= 24.3 · 30.3 · 31.5 mS cm⁻¹) ↔ 이 논문 0.240 · 0.300 · 0.310 mS cm⁻¹ — **비 (Cal35/Cal0 = 1.30 ↔ 1.29) 는 같고 크기는 ≈100 배 차** (24.3/0.240 · 30.3/0.300 · 31.5/0.310 = 101 · 101 · 102 [카드 산술]) → 둘 중 한쪽의 축 단위가 틀렸다 (어느 쪽인지 원문으로 못 가림) · 같은 그룹 2026 판의 σ_e,eff ≈10⁻³ mS cm⁻¹ [다른 카드 benhadjali2026] 까지 합치면 **같은 그룹 세 논문의 δ_e 가 4 자릿수에 걸친다** — 절대값 인용 금지.

### 3-9. ★ 원문 안 어긋남 (원문 비판 목록 — §11 에 다시)

1. **그림 2 캡션** *"for the 10 %, 20 % and 35 % calendering degrees"* ↔ 패널 제목 Cal0% · Cal20% · Cal35% · 본문 0 · 20 · 35 % (p.2–3).
2. **표 S1 머리** *"0 · 10 · 35"* ↔ 두께 36.8 = 46 × 0.80 → 20 % [카드 산술].
3. **표 S1 ↔ 그림 2c · 2f**: CBD 40 · 39 ↔ 41.0 · 40.1 · 기공 (Cal20%) 13 ↔ 12.0 [판독] (그림 Cal0% 합 101 %).
4. **표 S2 단위** δ_ion *"mS.cm-2"* (전도도인데 cm⁻²) · ρ *"Gravimetric density"* (질량 밀도).
5. **부피 보존 위반** [카드 산술]: (1 − ε) × 두께 = (0.83 × 46) **38.18** → (0.87 × 36.8) **32.02** → (0.94 × 29.9) **28.11 µm** = **−16.1 · −26.4 %** · 상별 (분율 × 두께): AM 10.12 → 8.46 → 8.67 · SE 9.66 → 9.20 → 8.07 · CBD 18.40 → 14.35 → 11.36 µm — 단단한 구 (AM) 의 부피까지 줄어든다 (반올림 ±0.5 %p 로도 AM −12 % 이상) → 겹침 후처리 (우선순위 · union) 또는 분석 부피의 정의 탓 [카드 해석 · 원문 설명 없음].
6. **같은 0 % 침대의 상 분율이 원 논문과 다르다** [다른 카드]: 정본 alabdali2023 카드 = 두께 46 µm · ε_dry **35 %** (그림 표기) · 판독 AM ≈0.21 · SE ≈0.22 · CBD ≈0.20 ↔ 이 논문 표 S1 = AM 22 · SE 21 · **CBD 40 · 기공 17 %** — AM · SE 는 같고 기공 ↔ CBD 사이로 ≈18–20 %p 가 옮겨 갔다 (CBD 나노 기공을 CBD 상에 넣었는지 [미확인]).
7. **계산마다 다른 입력 전도도**: GeoDict (본문 p.4) σ_AM 0.005 · σ_CBD 15.93 S m⁻¹ · δ_bulk 1.25 mS cm⁻¹ ↔ COMSOL (표 S2) δ_e,AM **100** · δ_e,CBD **200** S m⁻¹ · δ_ion **0.7** — AM 20,000 배 · CBD 12.6 배 · SE 0.56 배 [카드 산술] → 그림 8 의 δ_e · δ_ion 은 전기화학 모델이 본 전도도가 아니다.
8. **결론 '200 mAh/g'** (p.9) ↔ 그림 3e 최대 ≈197.3 [판독] (200 = C_spec 입력) · 같은 조건 Cal20% 인쇄 188.28 (p.4).
9. **피복 % ↔ 비계면적** (§3-7) — 한 분모로 맞지 않음.
10. **δ_e 크기** — 원 논문 (alabdali2023 카드) 과 100 배 (§3-8).
11. **참고문헌**: [25] = [37] (Lombardo 2022 · 같은 논문 두 번호 · [37] 은 McMullin 수의 출처로 인용됨) · *"Bielfeld et al. [31]"* (p.4 · [31] = Ruess 외 · 철자) · [38] 서지 *"Adv. Energy Mater. n/a, 2403360"* (권호 없음).
12. **오타**: 그림 5 캡션 *"Calcualted"* · *"middlle"* · *"exibits"* · 그림 8 캡션 *"calendaring"* · p.5 *"uncalendared"* · 그림 S1g 축 *"Percenatge"* · 교신 표기 *"Corresponding author. author."*.
13. **활성화 과전압의 강조** — 그림 6a 평균값의 Cal0 ↔ Cal35 차는 C/10 에서 ≈10 % · 같은 조건 SE 전위 차는 ≈81 % (§3-6) ↔ 본문 *"much higher activation overpotential"*.
14. **영상 시간** 49.95 h (세 침대 공통) ↔ Cal0% 의 C/50 방전 끝 ≈172 mAh/g (§3-6).
15. **식 (7) ↔ 그림 8 (Cal0%)** — √(φ/f) 9.35 ↔ τ_g 10.2 [카드 산술 · 판독] (Cal20 · Cal35 는 1 % 안).

---

## 4. ★ 방법 — 계산 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 계산 사슬 (단계별)
1. **제조 모의 (이 논문 밖 · [13])**: CGMD · LAMMPS · 슬러리 (NPT) → 건조 (CBD 입자 축소) → 캘린더링 (강체 평판 등속 하강 · 바닥 고정 · x · y 주기 [다른 카드 alabdali2023]) · 0 · 20 · 35 % 두께 감소 구조 셋.
2. **후처리 (§2.2)**: 겹침 우선순위 AM → SE → CBD · CBD 부피 이동 → 불규칙 모양.
3. **메싱 (§2.2)**: INNOV 복셀화 다상 체적 메시 (Cal0% · Cal20% · Cal35%).
4. **전기화학 (§2.3)**: COMSOL · 반쪽 셀 (Li 박 표면 | LPSCl 20 µm | 양극 | CC 10 µm) · 식 (1)–(6) · 표 S2 · 2.6–4.2 V · C/5–C/50 · 외력 · 부피 변화 없음.
5. **수송 (§2.4)**: 같은 구조 (복셀) 를 GeoDict 로 · δ_e (1 V) · τ_g (식 7) · δ_ion (식 9) · 비계면적 (§3.1).
6. **해석 (§3)**: 방전 곡선 · 용량 · 리튬화 지도 · 이온 전류 지도 · 과전압 · 계면 · τ · δ.

### 4-2. 입자 처리 (우리 축 언어로)
- **CGMD**: 거친 입자 **구** (AM · SE · CBD) · Hertz 탄성 접촉 + LJ 점착 + 마찰 [다른 카드] · **접촉 소성 · 모양 소성 · 파괴 없음** · 치밀화 = 재배열 + 겹침.
- **넘김**: 구 → 겹침 우선순위 + CBD 부피 이동 → 복셀 다상 — '불규칙 모양' 은 **역학이 아니라 기하 후처리** 의 결과 (*"leading to the transformation of the initially spherical particles into more realistic, irregular shapes"* p.3).  같은 상의 입자 경계 (SE–SE 입계 · AM–AM 접점) 는 메시에서 사라진다 [카드 해석] — 접촉 저항 · 협착 항 없음 (CC/AM · CC/CBD 접촉 저항만 표 S2).
- **FEM**: 역학 없음 · AM 은 확산 영역 (3D) · SE · CBD · CC 는 전도 영역.
- **우리 대응**: DEM = 강체 구 + hooke/hysteresis (δ = 소성 대리 · E_eff 1.35 GPa) · MPM = SE J2 소성 (E 1.53 · ν 0.49 · σ_y 0.30 GPa · AM = 고정 장애물) · STEP3 = MPM 상 복셀 위 FV σ (CONTACT_FREE · CL-81) · STEP4 = 같은 복셀 위 BV + 입자별 구형 1D 확산 [우리 CLAUDE.md · `docs/step4_v2_design.md` §1].

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
- **(i) DEM (단단한 구 · 점접촉) 의 한계를 말한 문장**: 하나 — *"The usability of this model is limited for calendering degrees under or equal to 35 %, as it was discussed in Ref. [13] because above 35 % a decrease in the electrical conductivity was observed due to the partial occupation of the volume of CBD particles by other materials due to high pressure."* (p.2) · 그리고 모양에 대해 *"The transformation from spherical to irregular particle shapes in our FEM electrochemical modeling environment is a result of a specific postprocessing step performed on the CGMD simulation data."* (p.2–3) — CGMD 입자는 구로 남는다.  DEM 이라는 낱말은 등방 압축 선행 연구 [32] 를 가리킬 때 한 번 (p.9).  겹침 · 상대밀도 상한 · 접촉 독립 가정 · 보정값의 지위에 대한 말 없음.
- **(ii) 소성 · 큰 변형을 넣기 어려운 이유 · 우회 · 비용**: **말 없음** — 소성 낱말 0 회 · 서론은 황화물 SE 의 *"malleability caused by low Young's moduli, which allows the electrodes to be densified at low temperatures without the need for energy-intensive sintering processes [11,12]"* (p.2) 를 말하지만 모델에 넣지 않았다 · 우회 = **겹침 후처리로 모양만 바꾼다** (부피 이동 규칙 · 맞춘 값 0) · AM 부피 변화도 *"significant uncertainties"* 로 뺐다 (p.4) · 비용 = 500 GB · 28 코어 노드 (시간 [미확인]).
- **(iii) 2D / 3D**: 3D (+ 시간 = *"4D (3 spatial coordinates, and time)"* · 초록) · 2D ↔ 3D 전이 말 없음.
- **(iv) 압력을 뺄 때**: **다루지 않음** — 전기화학은 외력 없이 (p.3) · 넘긴 구조 = 목표 두께 그대로 (되튐 없음 [카드 산술]) · 등방 압축이 사이클 중 AM–SE 응력을 줄인다는 말은 DEM 선행 [32] 인용 (p.9).

### 4-4. 기법 미니 용어집
- **CGMD (coarse-grained MD)**: 입자 하나가 실제 입자 (또는 덩이) 하나를 대신하는 거친 입자 동역학 — Franco 그룹은 LAMMPS 로 슬러리 · 건조 · 캘린더링을 푼다 (힘장 = LJ + granular Hertz [다른 카드]).
- **CBD (carbon-binder domain)**: 탄소 + 바인더 (+ 나노 기공) 를 한 상으로 본 영역.
- **캘린더링 정도 (calendering degree)**: 두께 감소율 (%) — 압력이 아니다.
- **겹침 우선순위 후처리**: 겹친 자리를 어느 상으로 칠할지 순서를 정하고 (AM → SE → CBD) 겹친 부피를 옮기는 기하 규칙.
- **INNOV**: Franco 그룹의 미세구조 생성 · 메싱 도구 [27] (복셀화 다상 메싱 [28]).
- **ConductoDict / DiffuDict**: GeoDict 의 전도 · 확산 풀이 모듈 (복셀).
- **McMullin 수 (이 논문 정의)**: D_eff/D_bulk = δ_ion/δ_bulk = f (문헌의 N_M = 1/f 와 역수).
- **τ_g (이 논문)**: √(φ_SE/D_eff) — 확산 해에서 나온 수송 τ (우리 tau) · 이름만 'geometric'.
- **t⁺ = 1 (단일 이온 전도체)**: SE 안 염 농도 기울기 없음 → SE 는 옴 전도만.
- **DOD (depth of discharge)**: 방전 깊이 — 그림 4 는 전압 3.9 · 3.65 · 2.6 V 로 25 · 75 · 100 % 를 대신 표시.

---

## 5. Figure set ★ (크롭 51 장 = `litdb/figures/benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode/`)

| 파일 | 내용 | 우리 활용 |
|---|---|---|
| `fig_1.png` | 작업 흐름 — 슬러리 → 건조 → 건조 전극 → 캘린더링 → 압연 전극 → 전기화학 → 방전된 전극 (범례 AM · SE · CBD_slurry · CBD_dry · 기공 · CC · Li 금속) | 사슬 위상 한 장 (우리 DEM → MPM → STEP3/4 와 나란히 · §7-1) |
| `fig_2.png` · `fig_2a.png` · `fig_2b.png` · `fig_2cf.png` | (a) CGMD 구조 셋 + 세로 단면 (b) 메시 셋 (c–f) 상 분율 막대 (CBD · SE · AM · 기공) — ⚠ 캡션 *"10 %, 20 % and 35 %"* | ★ 겹침 후처리 전 (구) ↔ 후 (복셀 다상) · 표 S1 과 1 %p 어긋남 (§3-9 ③) |
| `fig_3.png` · `fig_3e.png` | (a–d) C/5 · C/10 · C/20 · C/50 방전 곡선 (e) 2.6 V 끝 용량 vs C-rate | ★ 구조만의 율속 차 (§3-5 표) |
| `fig_4.png` | C/50 · 25 · 75 · 100 % DOD 의 AM [Li]/[Li_max] 3D 지도 × Cal0/20/35 | 리튬화 불균일 (정성) · 우리 STEP4 입자별 SOC 지도와 같은 꼴 |
| `fig_5.png` | 가운데 방전 이온 전류 밀도 3D + x 단면 셋 | 병목 통로 (정성) |
| `fig_6.png` · `fig_6a`–`fig_6d.png` | (a) 평균 활성화 과전압 (b) SE 전위 vs 용량 (c) η_act 지도 (d) 활성 면적 지도 | ★ 손실 분해 판독 (§3-6 표 — SE 옴이 주 몫) |
| `fig_7.png` · `fig_7a.png` · `fig_7b.png` | 이온망 · 전자망 비계면적 막대 | 비계면적 판독 (§3-7) · 분모 미확인 |
| `fig_8.png` · `fig_8a.png` · `fig_8b.png` | (a) τ_g vs 캘린더링 (b) δ_e · δ_ion (두 y 축) | ★ 식 (7) · (9) 재현 검사 (§3-8) · τ 규약 (§7-3) |
| `fig_S1.png` · `fig_S1g.png` | SE SEM (a–f) · 모델 SE 입도 7 계급 (g) | 입도 입력 (원 논문 [S1] 그림) |
| `fig_S2.png` | 입자 구조 → 3D 재구성 기하 → 다상 메시 (Cal0/20/35 · 상자 41 × 41 × 46 · 36.8 · 29.9 µm) | ★ 넘김 세 단계 그림 (치수 유일 출처) |
| `tab_S1.png` | 캘린더링 · 두께 · 부피 분율 · 기공 (머리 '10' 오기) | §3-1 · §3-9 ⑤ 부피 보존 검사 |
| `tab_S2.png` | 전기화학 매개변수 (변환 PDF 두 쪽 이어 붙임) | §3-3 · GeoDict 입력과 대조 (§3-9 ⑦) |
| `eq_01`–`eq_09` | 식 (1)–(9) 한 장씩 | 보고서 붙임용 (지배식 · 수송 정의) |
| `txt_*` 17 장 | 근거 문단 (하이라이트 · 초록 · 선행 한계 · 사슬 · 35 % 한계 · 겹침 후처리 · 메싱 · 외력 없음 · 경계 · GeoDict · 결과 · 결론 · 한계 · 데이터 가용성) | 인용 문장 원문 확인용 |

## 6. Post-processing ★
- **저자가 한 것**: CGMD 구조 → 겹침 후처리 → INNOV 복셀 메시 → COMSOL 방전 (용량 · 리튬화 지도 · 이온 전류 지도 · 평균 활성화 과전압 · SE 전위 · η_act 지도 · 활성 면적 지도) · GeoDict (δ_e · τ_g · δ_ion · 상 사이 비계면적 · AM 피복 %).
- **안 한 것**: 실험 대조 · 복셀 · 메시 수렴 · 복셀 크기 보고 · 반복 (다른 실현) · 오차 막대 · 압력 판독 · 되튐 · 잔류 응력 · AM 부피 변화 · 계면 저항 (CC 접촉 제외) · 같은 입력 전도도로 GeoDict 와 COMSOL 맞추기 · 손실 분해의 정량 (옴 ↔ 활성화 ↔ 확산) 표.
- **이 카드가 한 것**: 원본 300 dpi 래스터 (PDF 안 JPEG) 를 그림마다 눈금선 · 틀선으로 보정해 판독 (그림 2c–f · 3e · 6a/6b · 7 · 8 → `digitized.csv` 96 행 · 그림 3e · 7 · 8 은 인쇄값 재현 확인) · 표 S1 부피 보존 검사 · 식 (7) · (9) 재현 검사 · c_max → 이론 용량 · AM 구 등가 지름 · 영상 3 개 × 3 프레임 색 막대 대응 · 원 논문 카드 (alabdali2023) 와 τ_g · δ_e 대조.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (우리 수치는 CLAUDE.md · 메인 리포 문서 출처를 그 자리에 적는다)

### 7-1. ★ 넘김 사슬 나란히 (질문 h · 단계별)

| 단계 | 이 논문 (Franco 그룹 2025) | 우리 (메인 리포) | 같음 / 다름 · 왜 |
|---|---|---|---|
| 제조 · 압밀 모의 | CGMD (LAMMPS · LJ + granular Hertz · NPT) · 슬러리 → 건조 → 평판 등속 하강 [13] | DEM (LIGGGHTS · hooke/hysteresis · SE E_eff 1.35 GPa = 24 GPa 의 18 배 연화) · 건식 분말 침대 [우리 CLAUDE.md frame [2]] | 둘 다 형상 불변 구 · 그들은 습식 공정 사슬 · 우리는 건식 압밀 |
| 압축 제어 | **변위** (두께 0 · 20 · 35 % 감소) · 압력 없음 | **하중** (300 MPa 도달 → 판 고정 이완) [우리] | 그들은 두께를 맞추고 우리는 압력을 맞춘다 |
| 넘기는 시점 | 목표 두께 그대로 (되튐 없음 [카드 산술]) · 외력 · 응력 없이 전기화학 | DEM 끝 덤프 (real_14 step 2,060,000 = PHASE 4 판 고정 완화 · 판 z 30.2845 µm [우리 CLAUDE.md FAM 줄]) → MPM 이 SE 를 다시 누른다 → STEP3/4 는 MPM 상 격자에서 | **둘 다 '누른 상태'** 를 넘긴다 · 하중 뺀 상태 (언로딩) 는 둘 다 아직 없다 (우리 = DEM 언로딩 등록 · 준비 중 [우리 CLAUDE.md DEM 우선 Ⓐ]) |
| 무엇을 넘기나 | 구 좌표 · 반지름 · 상 → 기하만 | AM 좌표 (얼린 골격 · `--am-scaffold`) + SE 중심 (`--se-dump` 씨앗) → MPM 이 SE 를 소성으로 다시 압밀 [우리 CLAUDE.md scaffold 절] | 그들 = 기하 그대로 · 우리 = 기하 + **역학 재계산** (MPM) |
| 겹침 처리 | 우선순위 AM → SE → CBD · 겹친 CBD 부피를 AM / SE 로 옮김 · 결과 (1 − ε)·t −16 · −26 % (§3-9 ⑤) | DEM 기공 = ε_sphere (구 부피 합 · 질량 보존) ↔ ε_union (겹침 한 번) · real_14 차 1.251 %p [우리 CLAUDE.md 08-12 정정] · MPM SE 씨앗 = AM 이 아닌 칸에만 (voxel union) [우리 CLAUDE.md SE-DUMP 절] | **둘 다 AM 우선** · 그들 규칙은 질량을 보존하지 않는다 → 우리 연산자 규칙 (단계 0) 에 '부피 보존 검사' 를 같이 둔다 |
| 해상도 | 복셀 크기 · 메시 [미확인] | MPM n_grid 384 · dx 0.141 µm (real_14) [우리 CLAUDE.md d_h 절] · STEP3 vox 0.4 (원고) · 0.15 µm (Phase A · 구 스탬프) [우리 CLAUDE.md SR-01] · STEP4 개발 0.8 · 결론 0.4 µm [우리 `docs/step4_v2_design.md` §2] | 그들 해상도 정보 없음 → 그들 값의 격자 의존은 판정 불가 (우리 STEP3 은 격자 미수렴을 실측으로 안다 — CL-41) |
| 수송 | GeoDict 복셀 (δ_e · τ_g · δ_ion) · 입력 σ 가 전기화학과 다름 | STEP3 복셀 FV (CONTACT_FREE) + DEM 접촉망 Kirchhoff/Holm (FULL) [우리 CL-81] | 그들 = 우리 STEP3 와 같은 CF 부류 · 접촉망 FULL 과 견주지 않는다 |
| 전기화학 | COMSOL FEM · **AM 안 3D Fick (복셀 모양 그대로)** · SE 옴 (t⁺ = 1) · BV (AM–SE) · CC 10 µm + CC 접촉 저항 · 음극 BV (i0 크게) | STEP4-v2 · 같은 복셀 위 전자 · 이온 두 망 + AM\|SE 면 BV · **입자별 구형 1D Fick** (실측 반경 · 표면 유입 균일 살포) · t⁺ ≈ 1 · R_int 직렬 [우리 `scripts/step4_dyn.py` 머리 · `docs/step4_v2_design.md` §1] | 같은 물리 (단일 이온 SE · BV · 고체 확산) · 다른 것 = 입자 안 확산의 해상 (3D ↔ 구형 1D) · 우리 쪽 각도 비해상 한계는 우리 문서가 스스로 적었다 |
| 검증 대상 | 이 논문 안 없음 · 제조 단계는 [13] (슬러리 밀도 · 점도 · 건조 기공 [다른 카드]) | 기공 · 두께 (real_14 LIGGGHTS 15.6 % · 30.28 µm) · σ_ion (Bazzoun EIS 0.137 mS/cm) · σ_e (DC 분극 SBE 1.63 · DBE 4.68 mS/cm) [우리 CLAUDE.md] | 그들 사슬의 어느 단계도 이 논문에서 실험과 닿지 않는다 |
| 계산 비용 | COMSOL 1 노드 500 GB · 28 코어 · 시간 [미확인] · GeoDict 데스크톱 | GPU (MPM · STEP3/4) · CPU DEM [우리] | 비교 불가 (그들 시간 · 자유도 없음) |

### 7-2. 비교표 (재료 · 상태 · 측정 연산자가 행마다 다르다)

| 양 | 이 논문 | 우리 | 같은가 · 왜 다른가 |
|---|---|---|---|
| SE · AM | Li₆PS₅Cl · NMC622 (입경 [미확인] · 구 등가 ≈7.9 µm [카드 산술]) | LPSCl · NMC811 [우리] | SE 화학 같음 · AM 조성 · 크기 다름 |
| 조성 · 공정 | 습식 · CBD 38–40 vol% (표 S1) · wt% 미기재 | 건식 · 탄소 · 바인더 적은 침대 (ps45 = 첨가제 없음) [우리] | 출발 상태가 다르다 — 기공 · 상 분율 교차 인용 금지 |
| 기공 (압연 후) | 17 · 13 · 6 % (CBD 를 고체로 · 0 · 20 · 35 % 두께 감소) | 순수 SE 랩 표준 10–13 % @300 MPa · real_14 복합 15.6 % (ε_sphere) [우리] | 압력 축 없음 · CBD 정의 · 부피 비보존 → **같은 표에 넣지 않는다** |
| f · τ | f = 0.0024 → 0.0144 · τ_g = √(φ/f) 10.2 → 4.3 · tau2 ≈104 → 18.5 [카드 산술 · 판독] (SE 21–27 vol%) | ps45 Hertz FULL tau2 5.03–7.24 · 협착 뺀 CF 1.25–1.79 [우리 `docs/data/ps45_r45_network_g2_20261007/README.md`] | SE 분율 · CBD · 기공이 크게 다르다 — 크기 비교 금지 · 방향 (압밀 → τ ↓) 만 같다 |
| δ_e | 0.24 → 0.31 mS/cm (GeoDict · σ_AM 0.005 · σ_CBD 15.93 S/m) — 원 논문과 100 배 차 (§3-8) | 원고 σ_e 앵커 SBE 1.63 · DBE 4.68 mS/cm [우리 CLAUDE.md 10-19] | 재료 · 첨가제 · 정의 다름 · 그들 절대값은 신뢰 불가 |
| 전기화학 출력 | 용량 vs C-rate · 리튬화 지도 · 과전압 | STEP4 V(t) · 입자별 SOC · 분극 분해 [우리 `docs/step4_v2_design.md` §0] | 같은 출력 꼴 — 그들 그림 6 이 '옴 ↔ 활성화' 분해 의 본보기 |

### 7-3. τ 명명 규약 대조 (우리 규약 · CLAUDE.md τ 절)
- 그들 **τ_g = √(φ_SE/D_eff)** (식 7 · D_bulk = 1) = 우리 **tau** (√tau2 · flux τ) — 'geometric' 이라 불렀으나 우리 τ_geo (최단 경로 / 두께) 가 아니다 → 우리 표로 옮길 때 이름 = "정의 √(φ/f) 의 τ (그들 'geometric tortuosity')".
- 그들 **N_M = D_eff/D_bulk = δ_ion/δ_bulk** = 우리 **f** — 문헌 McMullin 수 (N_M = 1/f) 와 **역수** (COMSOL 예제의 'McMullin number' = f 와 같은 쓰임 — CLAUDE.md τ 절이 적은 함정과 같다).
- 우리 표의 **수송 tortuosity (tau2) = φ/f = τ_g²** ≈ 104 · 38.6 · 18.5 [카드 산술] — 'tortuosity factor' 이름은 이 값에만.
- 협착 배수 (τ_FULL/τ_CF) 는 낼 수 없다 (복셀 융합 · FULL 가지 없음).

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 공정 사슬의 기하 → **3D 해상 전기화학** (입자 안 3D 확산 · 리튬화 · 이온 전류 · 과전압 지도) · 복셀 수송 (CF 부류).
- **없는 것**: 역학 전부 (압력 · 응력 · 소성 · 되튐 · 부피 변화) · 접촉 단위 협착 · 실험 대조 · 해상도 정보.
- **우리 쪽이 줄 수 있는 것**: DEM = 하중 제어 압밀 · 접촉망 FULL σ / MPM = SE 소성 · 기공 메움 / STEP4 = 같은 꼴의 방전 (구형 1D) · 언로딩 (준비 중).  ⚠ 그들의 3D 입자 안 확산은 우리 STEP4 보다 앞선 축이다 (우리 `scripts/step4_dyn.py` 머리 주석이 *"입자 표면 유입의 각도분해"* 를 범위 밖으로 적었다).

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 = 계산만 · 재료 NMC622 + Li₆PS₅Cl + CBD 38–40 vol% · 압력 축 없음 · 순수 SE 없음.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ **반례 하나**: 겹침 우선순위 + 부피 이동 규칙으로 센 기공에서 (1 − ε) × 두께가 0 → 35 % 압연에 **−26 %** (단단한 AM 몫까지 −14–16 %) [카드 산술 §3-9 ⑤] → 우리 연산자 등록에 "압밀 상태마다 상별 (분율 × 두께) 보존 검사 · 겹침 규칙 (우선순위 · union · 부피 이동) 을 글로" 를 같이 둔다 · 기공의 분모 · CBD 를 고체로 셌는지 칸 | 순수 SE 기공 · 진밀도 없음 → 랩 표준 (10–13 % · 1.64) 과 나란히 놓을 숫자 없음 |
| **단계 1** (3D 메모리 · 장 수) | 자릿수 하나: 41 × 41 × 30–46 µm 다상 복셀 메시의 COMSOL 반쪽 셀을 **500 GB RAM · 28 코어 노드** 에서 풀었다 (p.4) | 자유도 · 복셀 크기 · 실행 시간 없음 → 메모리 산식에 못 넣는다 |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 없음 (순수 SE · 항복 · 경도 없음) | — |
| **단계 5** (3D 복합 압밀) | ★ **쓸 범위 판정 꼴**: 단단한 구 모의를 더 누르면 *"partial occupation of the volume of CBD particles by other materials"* → 수송량이 꺾인다 → ≤35 % 만 쓴다 (p.2) — 우리 DEM 의 겹침 대리가 무너지는 압밀 (순수 SE 의 ε_sphere 음수 · CLAUDE.md) 과 같은 부류 · 결과 전 등록에 '압밀 정도별 수송량이 단조인지' 를 유효성 문지기로 | 압력 값 · 하강 속도 · 힘장이 이 논문에 없다 · 두께 감소율 축을 압력 축으로 옮기지 않는다 |
| **단계 6** (탈압 · 되돌아옴) | **없음** — 넘긴 구조 = 목표 두께 그대로 (46 × 0.80 · × 0.65 [카드 산술]) · 외력 없음 · 응력 넘김 없음 → *"탈압 상태를 넘겼다"* 의 근거로 쓸 수 없다 · 반대로 '누른 상태를 넘긴 선례' 로는 쓸 수 있다 (우리 현재 사슬도 그렇다) | 되튐 값 · 측정 없음 |
| **단계 7** (형상 · 피복 · 수송) | ★ 사슬의 끝 꼴: 복셀 메시 위 3D 방전 + GeoDict 수송 + 상 사이 비계면적 + AM 피복 % + 손실 분해 (활성화 ↔ SE 전위) — 우리 STEP3/4 산출 꼴과 같다 · ★ 그들 그림 6 판독: 캘린더링 효과의 대부분은 SE 옴 (C/10 에서 −81 %) 이지 활성화 (−10 %) 가 아니다 (§3-6) → 우리 STEP4 분극 분해 보고에 같은 두 칸을 둔다 | 실험 대조 없음 · 비계면적 분모 미확인 · δ 절대값 신뢰 불가 (§3-8) |
| **후보 D0** (지금 DEM) | 같은 부류의 다른 판: 그들 CGMD = 강체 구 + LJ + Hertz (힘장 재매개변수 · 건조 k_n ≈1 × 10⁵ Pa [다른 카드]) · 우리 = 강체 구 + hooke/hysteresis (E_eff 1.35 GPa) — 둘 다 모양은 후처리 · 다음 모델 (MPM / FEM) 에 맡긴다 | 압력 · 응력 출력 없음 → D0 의 압밀 대조 숫자 없음 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 없음 (FEM 은 역학이 없다) | — |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | 넘김 규칙의 본보기 하나: **AM 우선** (겹친 자리는 AM) — 우리 MPM 씨앗 규칙 (SE = AM 아닌 칸) 과 같다 · 그들은 그 뒤 역학을 풀지 않는다 | 다물체 · 강체 결합 정보 없음 |
| **후보 B** (입자별 FE + 접촉) | 복셀 다상 메시 위 FEM 의 실례 (전기화학) · 표 S2 의 CC 접촉 저항 출처 [S4] Schmidt 2023 = 3D 해상 미세구조의 전기화학 + 고체역학 결합 FE (질문 n 후보) | 역학 FE 아님 · 메시 정보 없음 |
| **후보 C · C′** (큰 변형 · 항복 캡 접촉 DEM) | 없음 | — |
| **후보 M0** (균질화) | 없음 | — |
| **U0–U6** | **U6** (작은 조밀 충전의 해상도 수렴) 의 **반례**: 복셀 크기 · 메시 수렴을 보고하지 않은 3D 결과 → 우리 결과 보고에 '복셀 / 지름' 칸 필수 · 식 (7)–(9) 는 해석 검사 꼴 (D_eff = −j·L/Δc · √(φ/f)) | 직접 단위 시험 없음 |
| **R1–R7** | **R1** (AM 이 움직이고 하중을 나눔) = CGMD 에선 AM 이 움직이나 하중 출력 없음 · **R2** 없음 · **R3** (SE 입자 경계 기억) = **반례** — 메시에서 같은 상 입자 경계가 사라진다 (SE 연속체 · 접촉 저항 없음) · **R4** (탈압) = 없음 · **R5** (맞추는 값 하나) = 이 논문 안 맞춘 값 0 (전기화학 매개변수 전부 문헌 · CGMD 는 [13] 에서 다수 맞춤 [다른 카드]) · **R6** (SE 형상 변형) = 기하 후처리 대리 (역학 아님) · **R7** (AM 파괴) = 없음 (깨끗한 AM) | — |
| **결과 전 대조 항목** | ① 같은 SE 분율 · 같은 정의 (f = σ_eff/σ₀ · τ = √(φ/f)) 로 우리 STEP3 결과를 낼 때 그들 f 0.0024 → 0.0144 (SE 21 → 27 vol% · CBD 40 → 38 · 기공 17 → 6) 를 **방향 · 자릿수** 대조로만 ② 캘린더링 (압밀) 이 C/5 용량을 2.4 배 · C/50 을 1.15 배 올린 크기 [판독 · 카드 산술] — 우리 STEP4 압밀 정도 스윕을 하게 되면 '고율에서만 크게 · 저율에서 작게' 를 결과 전에 적는다 ③ 손실 분해에서 SE 옴 몫이 활성화 몫보다 압밀에 훨씬 민감하다 (§3-6) | 실험 아님 · 습식 CBD 40 vol% · NMC622 — 랩 표준 (10–13 % · 1.64) 과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: SE 같음 (Li₆PS₅Cl) · AM NMC622 ↔ 우리 NMC811 · 습식 CBD 38–40 vol% ↔ 우리 건식 · 압력 없음 (두께 감소율) ↔ 우리 300 MPa · 3D ↔ 3D · 전기화학 = 반쪽 셀 (Li 박) ↔ 우리 STEP4 반쪽 셀 · 그들 역학 없음 ↔ 우리 MPM 소성.

## 9. 적용 인사이트 (행동)
1. **넘김 연산자를 글로 적고 보존 검사를 단다 (단계 0 · 단계 7 · 흐름 밖: STEP3 래스터화)**: 그들 규칙 (AM → SE → CBD · 겹친 CBD 부피 이동) 은 (1 − ε)·t 를 −26 % 만들었다 (§3-9 ⑤) — 우리 DEM → MPM (SE 씨앗 = AM 아닌 칸) · MPM → STEP3 (상 래스터) 넘김마다 상별 부피 보존표 (넘기기 전 ↔ 후) 를 결과와 같이 낸다 (메인 세션 판단).
2. **'쓸 범위' 문지기 (단계 5 · D0)**: 압밀 정도별 수송량이 갑자기 꺾이면 강체 구 겹침 인공물로 본다 (그들 35 % 한계의 근거가 바로 그것) — 등록 문서에 결과 전 문지기로.
3. **계산마다 같은 입력 σ (흐름 밖: STEP3 · STEP4)**: 그들 GeoDict ↔ COMSOL 입력이 20,000 배까지 달랐다 (§3-9 ⑦) — 우리 STEP3 · STEP4 는 같은 σ 표를 쓰는지 매니페스트에서 같이 보인다 (지금 규약 확인용 · 코드 고침 아님).
4. **τ 이름 (흐름 밖: τ 규약)**: 그들 'geometric tortuosity' = √(φ/f) · 'McMullin number' = f — 문헌에서 이 그룹 값을 옮길 때 우리 키 (`tau_*` · `f_*` · `tau2_*`) 로 다시 이름 붙인다 (§7-3).
5. **손실 분해 보고 꼴 (단계 7 · 흐름 밖: STEP4)**: 그림 6 의 '평균 활성화 과전압 vs 용량' + 'SE 전위 vs 용량' 두 곡선 · 세 C-rate — 우리 STEP4 분극 분해 그림을 같은 꼴로 내면 문헌과 바로 나란히 놓인다.
6. **인용 한정 (h)**: "제조 모의 구조를 3D 전기화학에 넘긴 선례" 로 인용할 수 있다 · "탈압 · 되튐 · 응력을 넘긴 선례" · "실험으로 검증된 사슬" 로는 쓰지 않는다.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Ben Hadj Ali et al. (J. Power Sources 630 (2025) 236131) passed CGMD-simulated wet-processed NMC622/Li₆PS₅Cl/carbon–binder cathodes (0, 20 and 35 % calendering thickness reduction) through an overlap-priority post-processing (AM > SE > CBD) and voxel-based multiphase meshing into a 3D-resolved COMSOL half-cell model; the more calendered electrode delivered about 92 vs 38 mAh g⁻¹ at C/5 (read from their Fig. 3e) and showed more uniform lithiation, while the SE 'geometric tortuosity' √(φ_SE/D_eff) fell from about 10 to 4. No experimental comparison was made, and the calendered geometry was transferred at the target thickness without springback or residual stress."
- 국문 (한정어와 함께): *"제조 모의 미세구조를 3D 전기화학에 넘긴 같은 사슬의 선례 (Ben Hadj Ali 2025) 는 목표 두께에 닿은 '누른 상태' 의 기하만 넘겼다 — 되튐 · 응력 · 압력 값 · 복셀 크기 · 실험 대조는 없다."*
- 국문: *"그들 그림 6 에서 캘린더링이 줄인 손실은 대부분 SE 이온 경로 쪽이다 (C/10 · 50 mAh/g 에서 SE 전위 −81 % ↔ 평균 활성화 과전압 −10 % [판독])."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **실험 대조 0 건** — 방전 곡선 · 용량 · τ · σ · 피복 모두 모델 값 · "model accurately captures" 는 실험 없는 서술.
2. **제조 모델 매개변수가 이 논문에 없다** — 힘장 · 하강 속도 · 입자 수 · PSD 일부 (SE 만 그림 S1) · AM 크기 [13] 몫.
3. **압력 축 없음** — 두께 감소율만 · *"applied calendering pressure"* 값 없음.
4. **해상도 · 메시 · 비용 정보 없음** — 복셀 크기 · 요소 수 · 수렴 · 실행 시간 · 자유도.
5. **넘김 연산자의 부피 비보존** (§3-9 ⑤) · 원 논문과 상 분율 어긋남 (§3-9 ⑥).
6. **입력 전도도 불일치** (GeoDict ↔ COMSOL · §3-9 ⑦) → 그림 8 과 전기화학이 다른 물성 위.
7. **δ_e 절대값** — 같은 구조의 원 논문과 100 배 (§3-8) · 같은 그룹 2026 판과 또 2 자릿수.
8. **비계면적 · 피복 % 분모 미확인** (§3-7) — 경향만.
9. **활성화 과전압 강조** — 그들 그림 6 숫자로는 SE 옴 몫이 압도 (§3-6 · §3-9 ⑬).
10. **'first'** — *"for the first time"* (p.2 · p.8) · *"First of its kind"* (하이라이트) 는 '제조 모의 구조 + ASSB 전기화학' 조합에 한정된 주장이다 (3D 미세구조 전기화학 자체는 [17] [18] 이 했다고 저자가 적었다).
11. **영상** — 본문 언급 없음 · 세 영상 시간 동일 (§3-6) · 색 판독은 대강.
12. **전이 한계 (우리 쪽)**: SE 같음 · AM NMC622 ↔ NMC811 · 습식 CBD 40 vol% ↔ 건식 · 역학 없음 ↔ 우리 MPM 소성 — 같은 이름 (porosity · tortuosity · conductivity) 의 다른 양이 섞이지 않게 표지를 붙인다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 번호 | 서지 (원문 목록 그대로 · 줄바꿈 하이픈만 복원) | 왜 · 카드 |
|---|---|---|
| 13 | M. Alabdali, F.M. Zanotto, M. Duquesnoy, A.-K. Hatz, D. Ma, J. Auvergniot, V. Viallet, V. Seznec, A.A. Franco, Three-dimensional physical modeling of the wet manufacturing process of solid-state battery electrodes, J. Power Sources 580 (2023) 233427, https://doi.org/10.1016/j.jpowsour.2023.233427. | 카드 = `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` — 이 논문 미세구조 셋의 출처 (힘장 · 단계 · 검증) |
| S4 | Schmidt, C.P.; Sinzig, S.; Gravemeier, V.; Wall, W.A. A Three-Dimensional Finite Element Formulation Coupling Electrochemistry and Solid Mechanics on Resolved Microstructures of All-Solid-State Lithium-Ion Batteries. Comput. Methods Appl. Mech. Eng. 2023, 417, 116468, doi:10.1016/j.cma.2023.116468. | 카드 없음 — ★ 해상 미세구조 위 전기화학 + 고체역학 결합 FE (질문 h · 후보 B) · 표 S2 CC 접촉 저항 출처 |
| 28 | M. Chouchane, A. Rucci, A.A. Franco, A versatile and efficient voxelization-based meshing algorithm of multiple phases, ACS Omega 4 (2019) 11141–11144, https://doi.org/10.1021/acsomega.9b01279. | 카드 없음 (후보 표 N-43) — 넘김 메싱의 원전 (겹친 구 → 상 · 복셀 크기 규칙) |
| 27 | M. Chouchane, A.A. Franco, An invitation to engage with computational modeling: user-friendly tool for in silico battery component generation and meshing, Batt. Supercaps 4 (9) (2021) 1451–1456, https://doi.org/10.1002/batt.202100096. | 카드 없음 (후보 표 N-73) — INNOV |
| 23 | M. Alabdali, F.M. Zanotto, B. Notredame, V. Viallet, V. Seznec, A.A. Franco, Experimental and computational analysis of slurry-based manufacturing of solid-state battery composite cathode, Batt. Supercaps (2024) e202400709, https://doi.org/10.1002/batt.202400709. | 카드 없음 — 같은 사슬의 실험 + 계산 (슬러리 · 코팅 · 미세구조) |
| 24 | A.C. Ngandjong, T. Lombardo, E.N. Primo, M. Chouchane, A. Shodiev, O. Arcelus, A.A. Franco, Investigating electrode calendering and its impact on electrochemical performance by means of a new Discrete element method model: towards a digital twin of Li-ion battery manufacturing, J. Power Sources 485 (2021) 229320, https://doi.org/10.1016/j.jpowsour.2020.229320. | 카드 = `ngandjong2021_dem_calendering_digital_twin` — 겹침 후처리의 LIB 선례 |
| 32 | M. Alabdali, F.M. Zanotto, M. Chouchane, A.C. Ngandjong, V. Viallet, V. Seznec, Y. S. Meng, A.A. Franco, Understanding mechanical stresses upon solid-state battery electrode cycling using Discrete element method, Energy Storage Mater. 70 (2024) 103527, https://doi.org/10.1016/j.ensm.2024.103527. | 카드 = `dem_mechanical_stresses_ssb_electrode_cycling` — 등방 압축 · 사이클 응력 DEM |
| 17 | A. Bielefeld, D.A. Weber, R. Rueß, V. Glavas, J. Janek, Influence of lithium ion kinetics, particle morphology and voids on the electrochemical performance of composite cathodes for all-solid-state batteries, J. Electrochem. Soc. 169 (2022) 020539, https://doi.org/10.1149/1945-7111/ac50df. | 카드 없음 (후보 표 N-89) — i0 출처 · 3D 미세구조 전기화학 선행 · 원뿔형 구조 |
| 31 | R. Ruess, S. Schweidler, H. Hemmelmann, G. Conforto, A. Bielefeld, D.A. Weber, J. Sann, M.T. Elm, J. Janek, Influence of NCM particle cracking on kinetics of lithium-ion batteries with liquid or solid electrolyte, J. Electrochem. Soc. 167 (2020) 100532, https://doi.org/10.1149/1945-7111/ab9a2c. | 카드 없음 — D_AM · V0 · R_CT 출처 (NCM 균열 · R7) |
| 38 | Naik, K.G.; Jangid, M.K.; Vishnugopi, B.S.; Dasgupta, N.P.; Mukherjee, P.P. Interrogating the role of stack pressure in transport-reaction interaction in the solid-state battery cathode. Adv. Energy Mater. n/a, 2403360, doi:10.1002/aenm.202403360. | 카드 없음 — 적층압 ↔ 수송-반응 (단계 6 · d) |
| 18 | A. Neumann, S. Randau, K. Becker-Steinberger, T. Danner, S. Hein, Z. Ning, J. Marrow, F.H. Richter, J. Janek, A. Latz, Analysis of interfacial effects in all-solid-state batteries with thiophosphate solid electrolytes, ACS Appl. Mater. Interfaces 12 (2020) 9277–9291, https://doi.org/10.1021/acsami.9b21404. | 카드 없음 — 마이크로 CT 구조 위 3D 전기화학 (접촉 · 박리) |
| 8 | P. Minnmann, J. Schubert, S. Kremer, R. Rekers, S. Burkhardt, R. Ruess, A. Bielefeld, F.H. Richter, J. Janek, Editors' choice—visualizing the impact of the composite cathode microstructure and porosity on solid-state battery performance, J. Electrochem. Soc. 171 (2024) 060514, https://doi.org/10.1149/1945-7111/ad510e. | 카드 = `minnmann2024_microstructure_porosity_visualization` |
| 15 | P. Minnmann, L. Quillman, S. Burkhardt, F.H. Richter, J. Janek, Editors' choice—quantifying the impact of charge transport bottlenecks in composite cathodes of all-solid-state batteries, J. Electrochem. Soc. 168 (2021) 040537, https://doi.org/10.1149/1945-7111/abf8d7. | 카드 = `minnmann2021_jes_charge_transport_bottlenecks` |
| 14 · 16 · 20 · 34 · 41 · 42 | Bielefeld 2020 · Bielefeld 2019 · Hlushkou 2018 · Amin & Chiang 2016 · Shi 2020 · Schlautmann 2023 (원문 목록 그대로) | 카드 = `bielefeld2020_effective_ionic_conductivity_binder` · `bielefeld2019_microstructural_modeling_composite_cathode` · `hlushkou2018_void_space_ion_transport_assb_cathode` · `aminchiang2016_nmc_electronic_ionic_transport_vs_li` · `shi2019_high_am_loading_particle_size_assb` · `schlautmann2023_se_particle_size_composite_transport` |
| 21 · 35 · 36 · 39 · 40 | K.G. Naik, B.S. Vishnugopi, P.P. Mukherjee, Kinetics or transport: Whither goes the solid-state battery cathode? ACS Appl. Mater. Interfaces 14 (2022) 29754–29765 · C. Liu, T. Lombardo, J. Xu, A.C. Ngandjong, A.A. Franco, An experimentally-validated 3D electrochemical model revealing electrode manufacturing parameters' effects on battery performance, Energy Storage Mater. 54 (2023) 156–163 · B.L. Trembacki et al., J. Electrochem. Soc. 165 (2018) E725–E736 · M. Chouchane et al., J. Power Sources 444 (2019) 227285 · K.G. Naik et al., Energy Storage Mater. 55 (2023) 312–321 | 카드 없음 — 액체 LIB · 고체 양극 3D 전기화학 선행 (우선 낮음) |
| 25 = 37 | T. Lombardo, F. Lambert, R. Russo, F.M. Zanotto, C. Frayret, G. Toussaint, P. Stevens, M. Becuwe, A.A. Franco, Experimentally validated three-dimensional modeling of organic-based sodium-ion battery electrode manufacturing, Batt. Supercaps 5 (8) (2022) e202200116, https://doi.org/10.1002/batt.202200116. | 카드 없음 — 같은 논문이 두 번호 (§3-9 ⑪) |

## 13. [미확인] 목록 (본문 10 쪽 + SI 전수에 없음)
1. **CGMD 매개변수** (힘장 · 하강 속도 · 입자 수 · AM 크기 · CBD 지름) · **압력 값** — [13] 몫.
2. **복셀 크기 · 메시 종류 · 요소 수 · 수렴 · 실행 시간 · 자유도**.
3. **판을 뗐는지 · 이완 · 응력** (넘긴 상태의 역학).
4. **겹침 규칙의 나머지** (같은 상 겹침 · SE–CBD · 세 상 겹침) · 부피 비보존의 원인 · 원 논문과 상 분율이 다른 까닭.
5. **FEM 옆면 경계 · 상 사이 계면 조건** · 1C 정의 · 영상 시간 49.95 h 의 정지 조건.
6. **비계면적의 '무엇의 g'** · 피복 % 분모 · 'measured' 0.16 m²/g 의 방법.
7. **i0c · D_AM · V0 의 실제 값 · 함수 꼴** (*"See reference"*).
8. 양극 조성 wt% · 질량 · 면적 용량.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 서지 = PDF 1 쪽 (제목 · 저자 · 소속 · 접수 · 수정 · 승인 · 온라인 · DOI · 라이선스) + PDF 메타데이터 *"Journal of Power Sources, 630 (2025) 236131. doi:10.1016/j.jpowsour.2024.236131"* + 쪽 머리글 · SI docx 머리 (같은 제목 · 저자) · 1저자 메모와 다른 점 없음 (권 · 쪽 · DOI 는 메모에 비어 있던 것을 원문으로 채움 · SI 파일 이름 S0378775324020846 = PII).
- 본문 10 쪽 = pdftotext (raw · layout) + PyMuPDF 줄 좌표로 전부 읽음 · 식 (1)–(9) 렌더 확인 (식 (7) 의 근호 · 식 (6) 의 첨자는 렌더에서만).  'video' · 'movie' · 'µm' · 'voxel size' · 'element' · 'pressure' 낱말 전수 검색 — 영상 · 복셀 크기 · 압력 값 없음 확인.
- SI = mmc1.docx (XML 직접 파싱: 단락 20 · 표 2 · 그림 2) + LibreOffice 변환 PDF 5 쪽 렌더 대조 · 영상 mmc2–4 = ffprobe (2.4024 s · 72 프레임 · 640 × 480 · h264) + 프레임 0 · 36 · 71 추출.
- 그림 크롭 51 장 전부 열어 봄 — 도구 8 그대로 (캡션 = figures.json · 그림 2 캡션 오기 표지) · 손 43 · 본 뒤 다시 자름 3 (식 4 · 근거 문단 2 — 앞 줄 섞임) + 같은 규칙으로 경계 다듬음 8.
- 판독 검산: 그림 3e Cal20% C/5 62.7 ↔ 인쇄 62.8 · C/50 188.4 ↔ 188.28 ✓ · 그림 7a AM–기공 0.0202 → 0.0045 ↔ 0.02 → 0.004 · AM–SE 0.0106 → 0.0186 ↔ 0.01 → 0.019 ✓ · 그림 8b δ_e 0.240 · 0.310 ↔ 0.24 · 0.31 ✓ · 그림 6 곡선 끝 용량 ↔ 그림 3e (≈172 · ≈188 · ≈197) ✓ · 그림 2c–f ↔ 표 S1 (§3-9 ③ 어긋남 둘).
- 정본 litdb 중복 확인 (2026-11-12): `litdb/papers/` 파일 목록 + DOI (`jpowsour.2024.236131` · `236131`) · 제목 낱말 · 'Ben Hadj Ali' grep — 카드 없음 (benhadjali2026 [29] · zhang2026 [36] 인용만 · sankar2026 'ref 64 Ben Hadj Ali 2025' 는 서지 없음).
- 정본 대조: `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` §3-1 (46 µm · ε_dry 35 % · 상 분율 판독) · §3-2 (τ_g · δ_e 판독 · τ = √(η/D_eff)) · §3-4 (springback n/a) · §4-4 (힘장 표) · `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` §3-8 · §6 · §11 [29] · `zhang2026_polymer_electrolyte_modeling_perspective` L64 · L121.
- 메인 리포 (읽기만) 대조: CLAUDE.md (frame [2] · scaffold · SE-DUMP · d_h · FAM 줄 · τ 규약 · 10-19 σ_e 앵커) · `docs/step4_v2_design.md` §0–§2 · `scripts/step4_dyn.py` 머리 주석 — 우리 쪽 파일은 고치지 않았다.

## 🔗 관련 카드
- **같은 그룹 · 같은 사슬**: `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` (다음 편 · 기계-전기화학 + WIP ↔ CUP) · `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` (미세구조 원전 [13]) · `dem_mechanical_stresses_ssb_electrode_cycling` ([32] · DEM 등방 · 사이클 응력) · `ngandjong2021_dem_calendering_digital_twin` ([24] · 겹침 후처리 LIB 선례) · `xu2023_realistic_am_shape_cgmd_calendering` · `qin2026_bilayer_cathode_cgmd_dem_graded_thick_electrode` · `wet_processing_resolved_am_ssb_cathode_manufacturing` (Weitze 2024 · 습식 ASSB · springback) · `zhang2026_polymer_electrolyte_modeling_perspective` (이 논문 인용).
- **3D 미세구조 수송 · 전기화학**: `bielefeld2019_microstructural_modeling_composite_cathode` ([16]) · `bielefeld2020_effective_ionic_conductivity_binder` ([14]) · `minnmann2021_jes_charge_transport_bottlenecks` ([15]) · `minnmann2024_microstructure_porosity_visualization` ([8]) · `hlushkou2018_void_space_ion_transport_assb_cathode` ([20]) · `schlautmann2023_se_particle_size_composite_transport` ([42]) · `shi2019_high_am_loading_particle_size_assb` ([41]) · `bazzoun2026_dem_fem_rnm_ionic` (DEM → FEM · RNM σ_ion 의 실험 대조가 있는 쪽).
- **τ · 수송 정의**: `landesfeind2016_tortuosity_eis_electrodes_separators` ([6]) · `landesfeind2018_tortuosity_impedance_vs_tomography` ([7]) · `aminchiang2016_nmc_electronic_ionic_transport_vs_li` ([34] · σ_AM 0.005 S/m 출처 계열).
- **화학-기계 (이 논문이 뺀 축)**: `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` ([3]).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
