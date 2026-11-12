<!-- 표준 양식 확장 (paper-level STANDALONE — 이 카드만 읽어도 논문을 읽은 것과 같게). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 1저자 11-12 후보 표 N-17 · 정독 59) 에서 꼭 뽑으라 한 항목 (미세구조를 어디서 · 언제 넘겨받았나 · 완전결합 정식화 식 번호별 · 수치 · 경계 · 검증 · 결과 · 저자 한계).
     본 = benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem.md (같은 제1 저자 · 같은 해 · 이 논문의 FEM 틀을 다시 쓰는 다음 편 · 절 번호 · 머리 상자 꼴) · 꼴 = benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode.md (§0-1 고른 의도 대조 · §8 자세한 분석 · 같은 사슬의 1 편 = 이 논문 ref [29]) · 미세구조 원 논문 = alabdali2023_cgmd_wet_manufacturing_ssb_cathode.md (ref [27]) · ΔV 원 = koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb.md (ref [8]).
     원문 = ChemRxiv 프리프린트 v1 (게시 2026-03-22 · 26 쪽 · CC-BY 4.0 · 비심사) — 후보 표 · 가리킨 카드가 적은 출판본 (Energy Storage Materials 90 (2026) 105304) 이 아니다.  SI 없음 (*"Supplementary material … at XXX"* p.23 — Figure S1 · Table S1 · S2 [미확인]).
     쪽 표기 = PDF 쪽 "p.N" (1–26 · p.1 = ChemRxiv 표지 (초록 포함) · 원고 인쇄 쪽 번호 = PDF 쪽 − 1 · 예: PDF p.16 의 인쇄 번호는 15).
     값 표지: [인쇄] = 본문 · 그림 안 글자로 적힌 값 · [판독] = 300 dpi 패널 크롭을 그 그림의 눈금선으로 보정해 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 92 행) · [카드 산술] = 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드 값 (slug 병기) · [우리] = 우리 쪽 값 (CLAUDE.md) · [미확인] = 26 쪽 전수에 없음.
     원문 26 쪽 글자 층 전수 (PyMuPDF 쪽별 · 블록 좌표) + 식 (1)–(16) 렌더 확인 (글자 층은 분수 · 첨자를 잃는다) · 그림 6 장 + 패널 13 장 전부 열람 · 'GPa' · 'Young' · 'modul' · 'Poisson' · 'mesh' · 'element' · 'availab' · 'unload' · 'plastic' · 'contact' 전수 검색 · 업로드 PDF 는 읽기만 했다. -->
# 습식 제조 모의 미세구조 (거친 입자 동역학 · 두께 20 % 압연 한 개 · 기공 12 %) 위의 3D 기계-전기화학 완전결합 반쪽 셀 — AM 안 응력 의존 화학 퍼텐셜 μ = μ₀ + RT ln X − Ωσ_h 가 확산 (식 6–7) 과 평형 전위 (식 9) 를 함께 움직이고, AM · SE · CBD 는 선형 탄성 + Koerver NMC622 ΔV (~4.8 %) 고유변형 · 적층압 68 MPa · 측벽 고정 · 분리막 · 집전체 강체 · 소성 · 파괴 없음 — 첫 사이클 집전체 면 평균 σzz −78 → +35 → −110 MPa · 두께 −0.68 → −3.29 → ≈+0.04 % [판독] · 완전결합의 평균 과전압 ≈2.3 mV 더 큼 [판독] · 물성 표 (SI) 없음 · 전압 곡선 대조만 — Ben Hadj Ali · Valisammagari · Bhutia · Dao · Viallet · Seznec · Franco (ChemRxiv 2026 프리프린트 · 비심사)

> slug `benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode` · DOI `10.26434/chemrxiv.15001135/v1` (출판본 ESM 90 (2026) 105304 · `10.1016/j.ensm.2026.105304` = 후보 표 · benhadjali2026 L443 의 2 차 서지 — 이 PDF 로 확인 안 됨) · type `3D-resolved FEM (COMSOL multiphysics) half-cell on a reused CGMD wet-manufacturing microstructure (LAMMPS slurry → drying → calendering · 20 % thickness reduction · from Alabdali 2023) → voxelization with CBD-overlap reassignment (INNOV) → fully coupled mechano-electrochemical cycling (Fick diffusion with stress-dependent chemical potential · stress-shifted equilibrium potential · symmetric Butler–Volmer (Fig. 1 only) · linear elastic AM / SE / CBD · intercalation eigenstrain from Koerver 2018 ΔV · 68 MPa stack pressure · rigid separator and current collector · fixed lateral walls) vs one-way coupling + experiment (wet NMC622 / LPSCl / carbon-PVDF-HFP half-cell · 60 °C · 1.9–3.7 V vs Li-In · GITT · EIS → OCV, D, j0 inputs) — no plasticity, no fracture, no SI in this PDF` · PDF `6eece8ca-17._Fully_coupled_mechano-electrochemical_modeling_of_3D-resolved_microstructures_for_solid_state_batteries_manufactured_by_wet_processing.pdf` (후보 N-17 · 26 쪽 · 원고형 단일 칼럼 · SI 미포함) · digested `2026-11-12` · status ✅
>
> **원제**: *Fully coupled mechano-electrochemical modeling of 3D-resolved microstructures for solid state batteries manufactured by wet processing* (p.1 · p.2)
> **저자 · 소속 (p.2)**: **Siwar Ben Hadj Ali** ᵃ˒ᵇ˒ᶜ · Abhilash Valisammagari ᵃ˒ᵇ · Pempa Tshering Bhutia ᵃ˒ᵇ · Anh Ha Dao ᵈ · Virginie Viallet ᵃ˒ᵇ · Vincent Seznec ᵃ˒ᵇ˒ᶜ · **Alejandro A. Franco** ᵃ˒ᵇ˒ᶜ˒ᵈ˒ᵉ\* — ᵃ LRCS, Université de Picardie Jules Verne, Hub de l'Energie, UMR CNRS 7314, Amiens · ᵇ RS2E, Hub de l'Energie, FR CNRS 3459 · ᶜ ALISTORE-European Research Institute, FR CNRS 3104 · ᵈ Umicore, Olen (Belgique) · ᵉ Institut Universitaire de France (\* 교신 alejandro.franco@u-picardie.fr).  ⚠ ChemRxiv 표지 (p.1) 는 Franco 를 RS2E · IUF · LRCS · ALISTORE 넷으로만 적는다 (Umicore 없음) ↔ 원고 (p.2) 는 ᵈ (Umicore) 를 포함.
> **판 · 지위 (p.1 · p.22–23)**: ChemRxiv **v1 · 게시 2026-03-22** · **CC-BY 4.0** · ⚠ *"This is a preprint and has not been peer reviewed. Data may be preliminary."* (p.1) · CRediT (p.22): Ben Hadj Ali = 원고 · 시각화 · 소프트웨어 · 방법 · 조사 · 분석 · 데이터 · 구상 / Valisammagari = 검토 · 분석 · 구상 / Bhutia = 검토 · 시각화 · 데이터 / Viallet = 검토 · 연구비 / Seznec = 지도 · 연구비 / Dao = 검토 · 지도 · 방법 · 구상 / Franco = 검토 · 지도 · 자원 · 관리 · 방법 · 연구비 · 구상 · 이해상충 없음 (p.22–23) · 연구비 (p.23) = Umicore DESTINY PhD (EU H2020 MSCA COFUND #945357) · Horizon Europe DigiCell (101135486) · PULSELiON (101069686) · ANR France 2030 PEPR BATMAN (ANR-22-PEBA-0002) · IUF · 계산 = UPJV MatriCS · 데이터 가용성 진술 없음 · 보충자료 링크 = *"at XXX"* (자리표시 · p.23) · 참고문헌 40 개 (p.23–26).
> **같은 그룹 카드 (링크만)**: [`benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem`](benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem.md) (같은 제1 저자 · 같은 해 · 이 논문을 ref [31] 로 인용 · 같은 FEM 식을 식 (12)–(24) 로 다시 씀) · [`benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode`](benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode.md) (ref [29] · 같은 미세구조의 전기화학만 판) · [`alabdali2023_cgmd_wet_manufacturing_ssb_cathode`](alabdali2023_cgmd_wet_manufacturing_ssb_cathode.md) (ref [27] · 미세구조의 출처) · [`koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb`](koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb.md) (ref [8] · NMC622 ΔV) · [`taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode`](taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode.md) (ref [20] · 2D 완전결합 선례) · [`zhang2026_polymer_electrolyte_modeling_perspective`](zhang2026_polymer_electrolyte_modeling_perspective.md) (이 논문을 ref 164 로 인용).
> **판독 원자료**: `litdb/figures/benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode/digitized.csv` (92 행 — 그림 3b · 3c · 4a · 4b · 4c · 4d · 6 · 눈금 보정 화소 판독) · 그림 크롭 **55 장** (도구 6 + 손 49 = 패널 13 · 식 16 · 근거 문단 20 · §5) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 같은 그룹의 습식 제조 CGMD 모의 (Alabdali 2023 [27] · LAMMPS · 슬러리 → 건조 → 압연) 가 만든 NMC622 / Li₆PS₅Cl / 탄소-바인더 (69 : 27.6 : 3.4 wt%) 양극 가운데 **'압연 뒤 두께 20 % 감소' 구조 하나** (AM 평균 10 µm · 기공 12 % · p.7–8) 를, CBD 와 겹친 부피를 AM · SE 에 더하는 복셀화 후처리와 INNOV 다상 메싱으로 COMSOL 에 넘겨 (Al 집전체 + 3D 양극 + SE 분리막 + Li 금속 반쪽 셀 · 40 × 40 µm · 양극 44.6 µm [인쇄 그림 2a]), **AM 안 Li 확산이 정수압 응력 기울기로도 흐르고 (식 6–7) 평형 전위가 Ωσ_h/F 만큼 옮겨지는 (식 5 · 9) 양방향 결합** 과 **AM · SE · CBD 선형 탄성 + 리튬 고유변형 (식 11–16 · Koerver 2018 NMC622 ΔV)** 을 C/10 5 사이클 동안 풀었다 — 한 방향 결합보다 평균 과전압이 ≈2.3 mV 크고 [판독 그림 3b · 평탄부 평균 −51.0 ↔ −53.3 mV], 집전체 면 평균 σzz 는 첫 사이클에 −78 → +35 (충전 끝 · 인장) → −110 MPa (방전 끝) [인쇄 p.16 · 판독 그림 4a], 양극 두께는 −0.68 → −3.29 → ≈+0.04 % [인쇄 p.17 · 판독 그림 4d] 로 움직이며, 국소 응력은 색 막대 끝 (−2.5 · +1 GPa) 까지 포화한다 [판독 그림 5] (p.12–18).  **역학 쪽 검증은 없다** — 실험 대조는 전압 곡선 (1 · 5 번째 사이클) 하나이고, 그 실험 셀에서 뽑은 OCV · D · j₀ 를 입력으로 넣었다 (*"This good matching is expected"* p.20).

| 1저자가 꼭 뽑으라 한 것 (후보 N-17 · 이 논문만의 덧붙임) | 이 논문이 주는 것 | 표지 · 위치 |
|---|---|---|
| ① ★ 미세구조를 어디서 · 언제 넘겨받았나 (제조 모의 단계 · 넘기는 자료 · 겹침 처리 · 메시) | **어디서** = 이전 논문 [27] (Alabdali 2023) 의 CGMD 습식 제조 모의 (LAMMPS · *"force fields … calibrated to match experimental parameters such as particle size distribution, density and viscosity"*) · 탄소와 바인더를 나누지 않음 · 같은 구조를 [29] (전기화학) · [26] (한 방향 역학) 에서 이미 썼다 (p.7) · **언제** = *"a microstructure with 20 % reduction of thickness after pressing"* (p.8) — 제하 · 되튐 · 판 분리 · 이완 · 잔류 응력 서술 **없음** [미확인] · **무엇을** = 메시 (기하) 만 — *"The mesh of the initial electrode microstructure was then imported into COMSOL"* (p.8) · **겹침** = *"overlaps between CBD and AM or between CBD and SE were handled by adding the volume of overlapping regions to AM or SE, respectively"* (p.8) · AM–SE 겹침 규칙은 이 논문에 없음 [미확인] · **메시** = INNOV 복셀화 + 다상 체적 메시 [30, 31] (p.8) · 복셀 크기 · 요소 수 · 메시 수렴 [미확인] | [인쇄] p.6–8 |
| ② ★ 완전결합 정식화 (식 번호별) | 식 (3) Li 보존 · (4) J = −(Dc/RT)∇μ · **(5) μ = μ₀ + RT ln X − Ωσ_h** · (6) J = −D(∇c − (c/RT)∇(Ωσ_h)) · **(7) 응력-농도 결합 PDE (셋째 · 넷째 항 = 역학 되먹임)** · (8) η = φ_s − φ_e − E_eq · **(9) E_eq = −μ/F** · (10) ∇·σ + F_b = 0 (F_b = 0) · **(11) σ = C : ε_e (세 상 선형 탄성)** · (12) ε_t = ε_e + ε_int = ½((∇u)ᵀ + ∇u) · (13) ε_e = ε_t − ε_int · **(14) ε_int = ⅓ Δc Ω I** · (15) Ω = 3λ / ((x − x₀) C_total) · (16) λ = (ΔV/V₀ + 1)^⅓ − 1 · **반응 속도식 = 그림 1 의 대칭 Butler–Volmer i_ct = i₀[exp(Fη/2RT) − exp(−Fη/2RT)] 뿐** (본문에 식 번호 없음) · SE · CBD 의 전하 보존식 · 계면 조건 · 기공 영역 처리 [미확인] | [인쇄] p.8–12 · 그림 1 (`fig_1_eqbox.png`) |
| ③ ★ 기계 쪽 — 구성식 · 물성 · 소성 여부 | **세 상 모두 선형 탄성** (p.11) · AM 은 *"expected to operate predominantly within the elastic regime"* (p.11) · *"The plasticity as a material property is ignored in this study"* (p.15) · 분리막 · 집전체 = **강체** (p.12) · Li-In 부피 변화 0 (= LTO 같은 무변형 음극 · p.16) · **E · ν · Ω · C_total · D · j₀ · OCV 값 = 표 S1 · S2 · 그림 S1 (SI · 이 PDF 에 없음)** · 인쇄된 물성 = NMC622 부피 변화 *"on the order of ~ 4.8 %"* (p.10 · p.21) 뿐 | [인쇄] p.10–12 · p.15–16 · [미확인] |
| ④ ★ 전기화학 · 확산 · 결합 항 | AM 안 Fick + 화학-기계 퍼텐셜 (식 3–7) · 응력 → 평형 전위 (식 8–9) · 리튬 농도 → 고유변형 (식 14–16) = **양방향** · 한 방향 결합 = 같은 매개변수에서 응력 되먹임만 끈 판 ([36] · p.13) · 그림 1 의 *"n-th / (n+1)-th iteration · displacement"* 는 반복 풀이 · 형상 갱신을 암시하나 본문 서술 없음 [미확인] | [인쇄] p.8–10 · p.13 |
| ⑤ ★ 수치 (FEM · 메시 · 풀이기 · 비용) | COMSOL Multiphysics · C/10 정전류 충방전 5 사이클 · UPJV MatriCS **노드 하나 · 500 GB RAM · 1 프로세서 (Xeon E5-2680 v4 · 2.40 GHz · 28 코어)** (p.8) · 요소 수 · 자유도 · 시간 간격 · 풀이기 설정 · 실행 시간 [미확인] · 결과 그림의 변형은 2.8 배 과장 (그림 5 캡션) | [인쇄] p.8 · p.19 |
| ⑥ ★ 경계 | 적층압 **68 MPa** = 경계조건 (식 10 아래 · 그림 2a 위면 화살표) · 집전체 바깥면 **고정 지지 (u = θ = 0, x · y · z)** · 측면 = **고정 벽** (셀 외피 대리 · 그림 2a 초록 네모) · *"the external casing surfaces (in x, y directions) are fixed, and the electrode is flexible to move along the thickness (z direction)"* (p.16) · *"The upper boundary condition allows for minor displacement in the simulations"* (p.21) · ⚠ 고정 벽이 미끄럼을 허용하는지 · 위 경계가 순수 압력인지 [미확인] — σzz 가 +35 MPa (인장) 까지 가는 것은 순수 압력 경계 + 미끄럼 벽으로는 힘 평형이 안 된다 [카드 해석 · §3-9 ③] | [인쇄] p.10 · p.12 · p.16 · p.21 · 그림 2a |
| ⑦ ★ 검증 (실험 · 해석해) | **실험 = 전압 곡선 하나** (그림 6 · 1 · 5 번째 사이클 · 60 °C · 68 MPa · Li-In → Li/Li⁺ +0.65 V 이동) — 충전 일치는 *"expected because the main electrochemical parameters … were extracted from the experimental data obtained during the charging process"* (p.20) · 방전은 모의가 1 사이클 ≈204 ↔ 실험 ≈192 mAh/g [판독] · **역학 (응력 · 두께) 실험 대조 · 해석해 · 메시 수렴 = 없음** · 같은 셀 자료로 매개변수화와 검증을 함께 함 (p.4) | [인쇄] p.4 · p.20–21 · [판독] |
| ⑧ ★ 결과 (응력 · 접촉 · 용량) | 결합 비교 (그림 3): 완전결합 평탄부 과전압 −53.3 ↔ −51.0 mV · 끝 용량 151.9 ↔ 155.6 mAh/g [판독] · 거시 (그림 4): σzz −78 → +35 → −110 MPa (다섯 사이클이 같은 꼴 · 사이클 경계마다 −110 → ≈−76 MPa 로 되돌아감 [판독]) · 두께 −0.68 → −3.29 → +0.04 % · 공간 (그림 5): σzz · σ_h 색 막대 −2.5 … +1 GPa 양끝 포화 · AM–SE 계면 전단 *"up to 1 GPa"* = *"clearly the result of particle loss of contact"* (p.18 · 접촉 모형은 없다) · 결론 *"local stress magnitudes reaching up to 2.5 GPa in compressive and 1 GPa in tensile"* (p.22) = 색 막대 한계값 [카드 해석] · 용량 (그림 6): 모의 1 사이클 ≈203 / 203.5 (충 / 방) ↔ 실험 ≈201 / 192 · 5 사이클 모의 ≈187 ↔ 실험 ≈182 / 183 mAh/g [판독] | [인쇄] · [판독] |
| ⑨ ★ 저자 한계 | 소성 무시 (p.15) · SEI · 열화 미반영 (p.21–22) · 위 경계가 실험의 나사 고정과 다름 (p.21) · Li-In 부피 변화 0 (p.16) · 분리막 · 집전체 강체 (p.12) · 격자 부피 변화의 비등방성 언급 (p.15) 하나 고유변형은 등방 (식 14) · 앞으로 = *"a future model should include the plastic deformation and fracture of AM particles and SE, which may lead to contact loss, crack formation, and mechanical failure during cycling. The integration of damage mechanics …"* (p.22) | [인쇄] |
| ⑩ 우리 쪽 — 질문 h · DEM → STEP3 · STEP4 사슬 · [DEM 우선 (수영)] '가압부터 한 모델' | §7 · §8 — 넘김 시점 (둘 다 '누른 상태' · 잔류 응력 안 넘김) · 이 논문의 '완전결합' 은 **사이클 안의 전기화학 ↔ 탄성** 이지 **가압 → 사이클 한 모델이 아니다** (압밀은 CGMD 가 끝냈고 FEM 은 응력 0 기하 + 68 MPa 경계로 시작) — 재설계 트랙의 '가압부터 한 모델' 의 선례가 아니라 **그 뒤 단계 (사이클 응력) 의 꼴** | §7 · §8 |

⛔ **한정어 (떼지 말 것)**: ① **ChemRxiv 프리프린트 v1 · 비심사** · SI 없음 → **물성 (E · ν · Ω · C_total) · 전기화학 매개변수 (D · j₀ · OCV) · 실험 자료 (그림 S1) 전부 [미확인]** ② 미세구조는 **이 논문이 만든 것이 아니다** — [27] 의 모의 구조 (정본 alabdali2023 카드: 바인더 SBS · 탄소 Super C45 · 용매 p-xylene · NEI LPSCl [다른 카드]) 를 다시 쓴다 ↔ 이 논문 실험 = PVDF-HFP · Super P · n-butyl acetate · POSCO LPSCl (p.4–5) — **조성 wt% 만 같다** ③ 실험 양극은 **3 t 로 눌렀고 (Ø18 mm 원판이면 ≈116 MPa [카드 산술])** 그 두께 · 질량 · 기공은 인쇄되지 않았다 → 모델 구조 (20 % · 12 %) 와 실험 양극의 대응은 **확인되지 않는다** ④ **소성 · 파괴 · 접촉 (분리 · 미끄럼) 모형이 없다** — '접촉 손실' · '입자 재배열' 은 저자의 그림 해석이지 모형 기전이 아니다 ⑤ **역학 검증 0** (응력 · 두께 · 압력 측정 대조 없음) ⑥ 그림 4 의 '첫 사이클 비가역' 은 다섯 사이클마다 같은 꼴로 되풀이되고 사이클 경계에서 되돌아간다 [판독] — 본문 *"only during the first cycle"* 과 맞지 않는다 (§3-9) ⑦ 셀 한 개 · 구조 한 개 · 사이클 다섯 (C/10) · 60 °C.
⇒ **절대값 전이: 0 건** (우리 압밀 · 탈압 · 수송 계산에 넣을 숫자 없음 · 응력 값은 물성 미공개 + 선형 탄성 + 색 포화).  전이되는 것은 **완전결합 식의 꼴 (식 5–9 · 14–16)** · **결합 효과의 자릿수 감** (평균 과전압 ≈2 mV · E_eq 이동 Ωσ_h/F) · **경계조건이 거시 응력을 정한다는 반면교사** (고정 벽 + 강체 분리막 = 사실상 사방 구속) · **'비가역' 을 기전 없이 해석한 반례** · **넘김 연산자 기록 꼴** (겹침 규칙을 글로 적는 것).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-17 의 '왜' 칸)

의도 원문: *"h · j — 습식 공정 3D 분해 미세구조 위에서 기계-전기화학을 한 정식화로 푼 (완전결합) 선례 · 구조를 어디서 · 언제 넘겨받았는지 · FEM 정의 · 구성식 · 물성 · 경계 · 검증 (카드에 없음) · "★ 완전결합 틀의 원 논문 — 다음 독서 1 순위" (benhadjali2026)"* (가리킨 카드 = `zhang2026_polymer_electrolyte_modeling_perspective` L64 · L122 · `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` L443)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "h · j — 습식 공정 3D 분해 미세구조 위에서" | **채움** | CGMD 습식 제조 모의 (슬러리 → 건조 → 압연) 의 3D 구조 (p.6–8 · 그림 1) · 반쪽 셀 영역 40 × 40 µm · 양극 44.6 µm · 전체 74.6 µm [인쇄 그림 2a] · ⚠ 실제로 만든 실험 전극의 3D 재구성이 아니다 (모의 구조 재사용) |
| "기계-전기화학을 한 정식화로 푼 (완전결합) 선례" | **채움 (사이클 안) · 없음 (가압부터)** | 사이클 중 전기화학 ↔ 탄성의 **양방향** 결합 = 채움 — 식 (5) · (7) · (9) + (14)–(16) (p.9–12) · 저자: *"a novel experimentally validated fully coupled mechano-electrochemical modeling workflow based on 3D-resolved cathode microstructures"* (p.4) · ⚠ **압밀 (제조) 은 같은 정식화가 아니다** — CGMD 가 끝낸 기하만 메시로 넘기고 FEM 은 68 MPa 경계에서 시작 (p.8 · p.16) · 소성 · 파괴 · 접촉 없음 (p.15 · p.22) · ⚠ 저자 서론의 *"all the few existing studies rely on one-way coupling"* (3D 해상 · p.4) 와 달리 그들 ref [24] (Schmidt 2023 CMAME) 의 제목은 *"coupling electrochemistry and solid mechanics on resolved microstructures"* — 저자는 [24] 를 *"single cathode particle [21–24]"* 로 묶었다 (p.4) · 원문 확인은 [24] 카드 몫 (정독 n 후보) |
| "구조를 어디서 · 언제 넘겨받았는지" | **일부** | 어디서 = [27] 의 CGMD 구조 · *"These microstructures were further analyzed electrochemically in our previous publication [29] and subsequently used for performing a mechano-electrochemical study [26]"* (p.7) · 언제 = *"20 % reduction of thickness after pressing"* (p.8) — 판을 뗐는지 · 되튐 · 이완 · 응력 넘김 **서술 없음** · ⚠ 같은 '20 %' 구조의 [29] 표 S1 두께 36.8 µm · 41 × 41 µm [다른 카드 benhadjali2025] ↔ 이 논문 그림 2a 양극 **44.6 µm** · 40 × 40 µm [인쇄] — 같은 구조라는 원문 문장과 숫자가 맞지 않는다 (44.6 이 무엇을 잰 길이인지 원문 정의 없음 [미확인]) · 기공 12 % (p.7) ↔ [29] 그림 2 판독 12.0 % · 표 S1 13 % [다른 카드] |
| "FEM 정의" | **채움 · 일부** | COMSOL · 반쪽 셀 (Al 집전체 + 3D 양극 + SE 분리막 + Li 금속) · C/10 5 사이클 · 식 (3)–(16) (p.8–12) · **일부**: BV 꼴은 그림 1 상자에만 (대칭 α = 0.5) · SE · CBD 의 전위 · 전하 보존식 · 상 사이 계면 조건 (완전 접합인지) · 기공 영역 역학 · 큰 변형 여부 · 시간 간격 · 메시 [미확인] |
| "구성식" | **채움** | AM · SE · CBD 선형 탄성 (식 11 · p.11) · 소성 무시 (p.15) · 리튬 고유변형 = 열변형 유비 등방 (식 14 · p.11) · Ω 를 격자 선변형 λ 로 (식 15–16 · ref [23] Iqbal 2022) · 분리막 · 집전체 강체 (p.12) |
| "물성" | **없음 (이 PDF)** | *"All other material properties and simulation parameters used in this study are summarized in Tables S1 and S2"* (p.12) — SI 미포함 (*"at XXX"* p.23) · 인쇄 = NMC622 ΔV ~4.8 % (p.10) · 68 MPa · 1C = 200 mA/g (p.5) · ⇒ benhadjali2026 카드가 [미확인] 으로 남긴 E · ν 는 **이 원 논문 (프리프린트) 본문에도 없다** |
| "경계" | **채움 · 일부** | 68 MPa 적층압 · 집전체 바깥면 고정 (u = θ = 0) · 측면 고정 벽 · 분리막 · 집전체 강체 · Li-In 부피 변화 0 · 위 경계 '약간의 변위' (p.10 · p.12 · p.16 · p.21 · 그림 2a) · **일부**: 고정 벽의 자유도 · 위 경계의 정확한 꼴 [미확인] |
| "검증 (카드에 없음)" | **일부** | 그림 6 전압 곡선 (1 · 5 번째) 만 — 충전 일치는 입력을 충전 자료에서 뽑았기 때문이라고 저자 스스로 적음 (p.20) · 방전은 차이 (SEI · 위 경계 탓, p.21) · 1 사이클 방전 끝 모의 ≈203.5 ↔ 실험 ≈191.7 mAh/g [판독] · **역학 검증 · 해석해 · 메시 수렴 없음** |
| "★ 완전결합 틀의 원 논문 — 다음 독서 1 순위" (benhadjali2026) | **채움** | 이 논문 식 (3)–(16) = benhadjali2026 카드 §4-3 의 식 (12)–(24) 와 **같은 꼴** (Li 보존 · 화학-기계 퍼텐셜 · 결합 PDE · η · E_eq · 평형 · Hooke · 변형률 · 고유변형 · Ω · λ) [다른 카드] · 같은 경계 (68 MPa · 측벽 고정 · 분리막 · 집전체 강체 · Li = 경계) · 같은 ΔV 출처 · 다른 점 = 계산 노드 (이 논문 500 GB · 28 코어 ↔ 그 카드 1000 GB · 64 코어 [다른 카드]) · λ 의 둘째 꼴 (§3-9 ①) |

**가리킨 카드 · 같은 논문을 옮긴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 (이 PDF) | 판정 |
|---|---|---|---|
| `zhang2026_…` L64 | *"Ben Hadj Ali 2025 (제조 모의 미세구조 → 3D 전기화학 방전, ref 36; 완전결합 기계-전기화학, ref 164)"* | ref 164 에 해당하는 이 논문 = 완전결합 기계-전기화학 ✓ · 연도 = ChemRxiv 게시 **2026-03-22** (p.1) · 출판본 2026 (benhadjali2026 L443) | **일부** — 내용 같음 · "2025" 가 ref 164 까지 걸리면 연도가 다르다 (Zhang 원문의 표기인지는 이 카드로 못 가림) |
| `zhang2026_…` L122 | *"164 · Ben Hadj Ali, S.; … Franco, A. A. Fully coupled mechanoelectrochemical modeling of 3D-resolved microstructures for solid state batteries manufactured by wet proc[ess] … · 완전결합 기계-전기화학 (정본 카드 없음 · 서지 일부 잘림 — PDF 원문 끝)"* | 제목 = *"Fully coupled mechano-electrochemical modeling of 3D-resolved microstructures for solid state batteries manufactured by wet processing"* (하이픈 있음) | **채움** (제목 · 저자 처음 · 끝 · 내용) · 학술지 · 권 · 연도 = 그 줄에 없음 · "정본 카드 없음" 은 이 카드로 낡았다 |
| `benhadjali2026_…` L443 | *"S. Ben Hadj Ali, A. Valisammagari, P.T. Bhutia, A.H. Dao, V. Viallet, V. Seznec, A.A. Franco, Fully coupled mechano-electrochemical modeling … wet processing, Energy Storage Materials 90 (2026) 105304. https://doi.org/10.1016/j.ensm.2026.105304."* + *"★ 완전결합 틀의 원 논문 (이 논문 FEM 의 정의 · 물성 · 경계 · 검증) — 다음 독서 1 순위"* | 저자 7 명 · 순서 · 제목 = **같음** (p.2) · 학술지 · 권 · 논문 번호 · DOI = **이 PDF (ChemRxiv v1 · DOI 10.26434/chemrxiv.15001135/v1) 로는 확인 불가** [미확인] · 정의 · 경계 = 있음 · 물성 = 없음 (SI) · 검증 = 전압 곡선만 | **일부** (서지 앞부분 채움 · 출판 정보 미확인 · 물성 없음) |
| `benhadjali2026_…` §4-3 표 (식 (22)–(24)) | *"Ω = 3λ / ((x − x₀) C_total) · λ = (ΔV/V₀ + 1)^{1/3} − 1 = (V_x/V₀)^{1/3} − 1"* | 이 논문 식 (16) = (ΔV/V₀ + 1)^⅓ − 1 = **((V_x − V₀)/V_x + 1)^⅓ − 1** (p.12) | **일부** — 같은 식이되 둘째 꼴이 다르다 · 그 카드 판 (V_x/V₀) 이 항등식으로 맞고 이 논문 판은 V_x 를 분모에 둔 오기 [카드 산술 §3-9 ①] (그 카드의 문제 아님) |
| `benhadjali2026_…` L18 · L441–L443 | *"zhang2026 … (Ben Hadj Ali 선행 2 편을 인용 · 그 둘의 정본 카드는 없음)"* · [29] · [31] 줄 *"카드 없음"* | — | **낡음** — [29] = `benhadjali2025_…` (11-12) · [31] = 이 카드 (11-12) 가 생겼다 (그 카드 줄은 고치지 않는다 · 🔗 관련 카드 한 줄만 더함) |

⇒ **의도 대조 결과: 채움 (h · 습식 3D 모의 구조 위 완전결합 (사이클 안) · FEM 정의 · 구성식 · 경계 · 완전결합 틀의 원 논문 = benhadjali2026 식과 같은 꼴) · 일부 (넘긴 시점 = '압연 뒤' 한 마디 · 되튐 · 응력 넘김 · 복셀 크기 미기재 · 두께 44.6 ↔ 36.8 µm 불일치 / 검증 = 전압 곡선만 · 역학 검증 없음 / 출판 서지 미확인) · 없음 (물성 — SI 미포함 / 가압부터 한 정식화)**.

---

## 1. 한 줄 요약
같은 그룹의 습식 제조 모의 구조 하나 (두께 20 % 압연) 위에서, 충방전 중 리튬 농도가 AM 부피를 바꾸고 (고유변형) 그 응력이 다시 리튬 확산과 평형 전위를 바꾸는 (응력 의존 화학 퍼텐셜) **양방향 결합** 을 3D 반쪽 셀 FEM 으로 풀었다는 프리프린트.  한 방향 결합보다 평균 과전압이 조금 크고 (≈2.3 mV [판독]), 68 MPa 아래서 집전체 면 응력은 충전 끝에 인장 (+35 MPa) 으로 뒤집혔다가 방전 끝에 −110 MPa 가 되며, 국소 응력은 GPa 에 이른다 (색 막대 포화).  모든 고체가 선형 탄성이고 소성 · 파괴 · 접촉 모형이 없으며 물성 표 (SI) 가 PDF 에 없다.  실험 대조는 매개변수를 뽑은 같은 셀의 전압 곡선뿐이다.

## 2. 메타

| 저자 | 판 | DOI | 소재 (AM / SE / C · 바인더) | 연구 유형 |
|---|---|---|---|---|
| S. Ben Hadj Ali · A. Valisammagari · P.T. Bhutia · A.H. Dao · V. Viallet · V. Seznec · A.A. Franco\* (LRCS · RS2E · ALISTORE-ERI · Umicore · IUF) | ChemRxiv v1 2026-03-22 (CC-BY 4.0 · 비심사 · 26 쪽 · SI 없음) · 출판본 = ESM 90 (2026) 105304 [미확인 — 2 차 서지] | 10.26434/chemrxiv.15001135/v1 | 실험: LiNi₀.₆Mn₀.₂Co₀.₂O₂ (NMC622 · Umicore) / Li₆PS₅Cl (POSCO) / Super P (*"Umicore"* 인쇄) + PVDF-HFP (Arkema) — 69 : 27.6 : 3.4 wt% · 모델: AM / SE / CBD (*"Carbon-Binder-solvent Domains"* · 탄소 · 바인더 한 상) 같은 wt% (p.4–7) | 모델 (CGMD 구조 재사용 → 복셀 메시 → COMSOL 3D 기계-전기화학 FEM · 한 방향 ↔ 양방향) + 실험 (반쪽 셀 · 율속 · GITT · EIS → 매개변수 · 전압 곡선 대조) |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 실험 — 재료 · 공정 · 셀 · 측정 (§2 · p.4–6 · `txt_p5_halfcell_assembly_3t_2t_68mpa.png` · `txt_p5_p6_cycling_gitt_protocol.png`)

| 항목 | 값 | 표지 · 위치 |
|---|---|---|
| 조성 | NMC622 : LPSCl : (Super P + PVDF-HFP) = **69 : 27.6 : 3.4** wt% · 고체 합 3000 mg · 탄소 : 바인더 나눔 [미확인] | [인쇄] p.5 |
| 혼합 · 슬러리 | 지르코니아 매체 · AM + SE + 탄소 **2 min · 2000 rpm** · PVDF-HFP 를 n-butyl acetate 에 자석 교반으로 풀어 넣음 · 같은 용매로 **액 함량 46 %** | [인쇄] p.5 |
| 도포 · 건조 | 닥터블레이드 **간극 150 µm** · 얇은 Al 박 · **80 °C 진공 하룻밤** · Ø18 mm 펀칭 · 건조실 이슬점 −60 °C | [인쇄] p.5 |
| SE 펠릿 | LPSCl **100 mg** · 플라스틱 몰드 **2 t** → Ø10 mm 면적이면 **249.7 MPa** [카드 산술: 2000 × 9.80665 N / (π · 5² mm²)] | [인쇄] p.5 · [카드 산술] |
| 양극 압축 | *"The cathode discs were initially compressed at **3 tons** and then punched down to 10 mm diameter"* → Ø18 mm 원판에 걸렸다면 **115.6 MPa** [카드 산술: 3000 × 9.80665 / (π · 9²)] (Ø10 mm 이면 374.6 MPa) · 다이 지름 · 시간 · 온도 [미확인] · **그 뒤 두께 · 질량 값 인쇄 없음** (*"After determining the mass and thickness of the cathode layer"* 만) | [인쇄] p.5 · [카드 산술] · [미확인] |
| 조립 | 양극 원판을 펠릿 한 면 가운데 · **2 t** 로 다시 누름 · 반대 면 = Ø9 mm In 박 가운데 Li 원판 (손으로 눌러 Li-In · In 이 SE 쪽) · Li 쪽 Ø10 mm Ni 집전체 · 나사 셋 · 위판 · **토크 11 N m *"(equal to 68 MPa)"*** (환산 방법 [미확인]) · Ø10 mm 에 68 MPa = 5.34 kN [카드 산술] | [인쇄] p.5 |
| 율속 | **25 사이클 · 60 °C · 1.9–3.7 V vs Li-In** (Li/Li⁺ 로 2.55–4.35 V [카드 산술 +0.65 V]) · **1C = 200 mA/g** · C/10 → C/5 → C/3 → C/2 → 1C 다섯 사이클마다 · 최종 양극 질량 기준 · **처음 다섯 사이클 (그림 S1) 을 모델 검증에** | [인쇄] p.5–6 |
| GITT | 0.05 C · 펄스 60 min · 이완 90 min · 1.9–3.7 V · Weppner–Huggins 식 (1) · r_p = *"radius of NMC622 particle"* (값 [미확인]) | [인쇄] p.6 · `eq_01` |
| EIS | GITT 단계마다 정전위 · 0.1 Hz–10 kHz · 10 mV · RelaxIS → R_ct → 식 (2) **R_ct = RT/(zFAj₀)** · A = *"the geometric active interface area"* (출처 · z 정의 [미확인]) | [인쇄] p.6 · `eq_02` |
| 넘긴 입력 | *"The extracted open circuit voltage, diffusion coefficient D_Li and exchange current density j₀ are employed to parameterize the model. All the experimental results are shown in Figure S1."* — **값은 그림 S1 (SI) 에만** [미확인] | [인쇄] p.6 |

- ⚠ 같은 그룹 2026-11 판 (WIP ↔ CUP) 의 CUP = *"3 t (~116 MPa)"* · 30 s · 상온 → 두께 82 → 72.16 µm (−12 %) · 보고 기공 25.1 % · 2.1–3.7 V vs Li-In [다른 카드 benhadjali2026 §3-2 · §3-3] — 이 논문의 '3 t 압축' 양극이 같은 상태라면 **모델 구조 (두께 −20 % · 기공 12 %) 보다 덜 치밀하다** [카드 해석 · 두 논문의 공정이 같다는 가정].

### 3-2. ★ 넘겨받은 미세구조 (§3.1 · p.6–8 · 그림 1 · 2a · `txt_p6_p7_parameterization_microstructure_source.png` · `txt_p8_oneway_extension_20pct_overlap_voxel.png`)

| 항목 | 값 | 표지 · 위치 |
|---|---|---|
| 출처 | *"This study uses an electrode microstructure generated in our previous work [27]"* — *"a predictive 3D model of the slurry-based manufacturing process"* · CGMD (LAMMPS [28]) · 힘장은 *"calibrated to match experimental parameters such as particle size distribution, density and viscosity [27]"* · 탄소 · 바인더 한 상 | [인쇄] p.6–7 |
| 조성 · 크기 · 기공 | 69 : 27.6 : 3.4 (AM : SE : CBD) · **AM 평균 10 µm** (지름인지 반지름인지 [미확인]) · **기공 12 %** (정의 [미확인]) | [인쇄] p.7 |
| 고른 구조 | *"Specifically, we focus on a microstructure with **20 % reduction of thickness after pressing**."* — 구조 하나 · 반복 · 시드 없음 | [인쇄] p.8 |
| 재사용 이력 | *"These microstructures were further analyzed electrochemically in our previous publication [29] and subsequently used for performing a mechano-electrochemical study [26]."* | [인쇄] p.7 |
| 겹침 처리 | *"overlaps between CBD and AM or between CBD and SE were handled by adding the volume of overlapping regions to AM or SE, respectively. This adjustment implicitly considers the microporosity of the CBD, and enables the transformation of ideal spherical shapes in CGMD into more realistic, irregular shapes of all the composite cathode phases."* · AM–SE 겹침 처리 서술 없음 (같은 사슬 [29] = 우선순위 AM → SE → CBD [다른 카드 benhadjali2025]) | [인쇄] p.8 |
| 메시 | INNOV *"used to voxelize and reconstruct multi-phase volumetric meshes for FEM calculations"* [30, 31] → *"The mesh of the initial electrode microstructure was then imported into COMSOL"* · 복셀 크기 · 요소 종류 · 수 · 수렴 [미확인] | [인쇄] p.8 |
| 영역 치수 | 40 µm × 40 µm (옆) · 전체 74.6 µm · 양극 44.6 µm · 위 = Li metal 면 · 분리막 · 아래 = 집전체 → 분리막 + 집전체 (+ Li 면) = 30.0 µm [카드 산술 74.6 − 44.6] · 각 두께 [미확인] | [인쇄 그림 2a] |
| 넘긴 상태 | 기하만 (메시) · 응력 · 접촉력 · 되튐 · 판 분리 서술 없음 · FEM 의 출발 = *"the entire cell is under compression due to the external load"* (p.16) | [인쇄] · [카드 해석] |

- **[다른 카드 대조 — 같은 '20 %' 구조라는 원문 문장과 숫자]**: [29] (정본 `benhadjali2025_…`) 표 S1 = 두께 **46 · 36.8 · 29.9 µm** (0 · 20 · 35 %) · 41 × 41 µm · 기공 17 · 13 · 6 % · AM 23 · SE 25 · CBD 39 vol% (20 %) [다른 카드] ↔ 이 논문 그림 2a = 양극 **44.6 µm** · 40 × 40 µm [인쇄] — 44.6/46 = 0.970 (건조 두께의 −3.0 %) [카드 산술] · 기공 12 % 는 [29] 의 20 % 구조 (12.0 % 판독 · 13 % 표) 와 맞는다.  ⇒ 그림 2a 의 44.6 µm 가 같은 구조의 다른 길이 (예: 집전체 일부 포함) 인지 다른 구조인지 **원문으로 못 가린다** [미확인].
- 정본 `alabdali2023_…` [다른 카드]: 총 5089 입자 (상별 개수 미보고) · 건조 46 µm · 41 × 41 µm · ε_dry 35 % · 압연 = 강체 평판 등속 하강 · 바닥 고정 · x · y 주기 · 건조 k_n 100 pg µm⁻¹ µs⁻² (= 1 × 10⁵ Pa) · 마찰 X_µ 12.5 · *"springback n/a"* — 이 논문은 이 값을 다시 적지 않는다.

### 3-3. ★ 완전결합 정식화 — 식 번호별 (§3.2 · p.8–12 · `eq_01`–`eq_16` · `fig_1_eqbox.png`)

| 식 | 내용 (렌더 확인) | 뜻 · 결합 | 표지 |
|---|---|---|---|
| (1) | D_Li = (4/9π)(ΔE_s/ΔE_t)² r_p²/t_p | GITT 확산계수 (Weppner–Huggins) — 실험 → 모델 입력 | p.6 |
| (2) | R_ct = RT/(zFAj₀) | EIS → 교환 전류밀도 (선형 BV · 기하 면적 A) | p.6 |
| (3) | ∂c/∂t + ∇·J = 0 | AM 안 Li 보존 (Fick [33]) | p.8 |
| (4) | J = −(Dc/RT)∇μ | 화학-기계 퍼텐셜이 흐름을 몬다 [34] | p.9 |
| (5) | **μ = μ₀ + RT ln X − Ωσ_h** · σ_h = tr(σ)/3 | 정수압 응력의 일 (Ω = 부분 몰 부피) | p.9 |
| (6) | J = −D(∇c − (c/RT)∇(Ωσ_h)) | (4)+(5) — **응력 기울기 흐름** (Li 는 σ_h 가 큰 쪽 = 덜 눌린 쪽으로) | p.9 |
| (7) | ∂c/∂t − D∇²c + (D/RT)∇c·∇(Ωσ_h) + (Dc/RT)∇²(Ωσ_h) = 0 | **셋째 · 넷째 항 = 역학 되먹임** (*"a key advancement … compared to our previous study [36], where the contribution of stress on the lithium diffusion was neglected"* p.9) · D · Ω 상수일 때 (6) 과 맞는다 [카드 산술] | p.9 |
| (8) | η = φ_s − φ_e − E_eq | 반응 과전압 (φ_e = SE 상 전위) | p.10 |
| (9) | **E_eq = −μ/F** | 응력 → 평형 전위 (*"mechanical stress directly alters the equilibrium potential and, consequently, the reaction overpotential η"*) | p.10 |
| 그림 1 | **i_ct = i₀[exp(Fη/2RT) − exp(−Fη/2RT)]** | 대칭 Butler–Volmer (α = 0.5) — **본문에 식 번호 없이 그림 상자에만** | 그림 1 |
| (10) | ∇·σ + F_b = 0 · F_b = 0 | 준정적 평형 · 68 MPa = 경계 [37] | p.10 |
| (11) | σ = C : ε_e | **AM · SE · CBD 모두 선형 탄성** [39] | p.11 |
| (12) | ε_t = ε_e + ε_int = ½((∇u)ᵀ + ∇u) | 작은 변형률 (선형 변형률) — ⚠ 본문은 *"ε_e and ε_int are the total and intercalation-induced strains"* 로 ε_e 를 '전체' 로 잘못 부름 | p.11 |
| (13) | ε_e = ε_t − ε_int | [34] | p.11 |
| (14) | **ε_int = ⅓ Δc Ω I** | 등방 고유변형 = 열변형 유비 [1, 40] · Δc = 지금 − 처음 농도 · ⚠ 그림 1 상자는 같은 식을 *"ε_e"* 로 적음 | p.11 · 그림 1 |
| (15) | Ω = 3λ / ((x − x₀) C_total) | 부분 몰 부피를 격자 선변형에서 (할선 꼴 · x = x₀ 에서 0/0 — 극한만 정의) [23] · C_total 값 [미확인] | p.12 |
| (16) | λ = (ΔV/V₀ + 1)^⅓ − 1 = ((V_x − V₀)/V_x + 1)^⅓ − 1 | ΔV = NMC622 탈리튬에서 잰 값 (리튬화에도 가역 가정 · ref [8] = Koerver 2018 · 그림 2b) · ⚠ 둘째 꼴의 분모 V_x 는 첫째 꼴과 같지 않다 (§3-9 ①) · ⚠ *"V_x is the instantaneous volume, and V_x is the reference unit cell volume corresponding to the maximum or the minimum lithium content during charge/discharge"* — V_x 가 두 번 정의됨 (하나는 V₀) | p.12 |

- **[카드 산술 · 다른 카드 값] 결합 크기의 자릿수**: E_eq 이동 = Ωσ_h/F — Ω ≈ 3 cm³/mol (정본 koerver2018 그림 2b NCM-811 V̄ 판독 · x 0.47 부근 · x < 0.4 에서 9–20 으로 급증 · NCM-622 도 비슷 [다른 카드] · 이 논문 식 (15) 의 할선 Ω 는 x 범위 · C_total [미확인] 에 걸린다) 이고 |σ_h| = 100 MPa 이면 3 × 10⁻⁶ × 1 × 10⁸ / 96485 = **3.1 mV** → 그림 3b 의 평균 과전압 차 ≈2.3 mV [판독] 와 같은 자릿수.  NMC622 ΔV −4.8 % 의 선변형 λ = (0.952)^⅓ − 1 = **−1.63 %** [카드 산술].

### 3-4. ★ 경계 · 영역 · 물성 · 풀이기 · 비용 (p.8 · p.10–12 · p.15–16 · p.21 · 그림 2a · `txt_p8_comsol_halfcell_5cycles_hardware.png` · `txt_p10_p11_stack_bc_dv_linear_elastic.png` · `txt_p12_dv_definition_rigid_separator_bcs_tables.png` · `txt_p15_p16_plasticity_ignored_uniaxial_sigmazz.png`)

| 항목 | 값 | 표지 · 위치 |
|---|---|---|
| 영역 | Al 집전체 + 3D NMC622 복합 양극 + SE 분리막 + Li 금속 음극 (실험은 Li-In · 전위 +0.65 V 이동) | [인쇄] p.8 · p.20 |
| 역학 경계 | 적층압 **68 MPa** (위면) · 집전체 바깥면 고정 지지 *"(u = θ = 0) along the x, y and z axes"* · 측면 **고정 벽** (*"to mimic the mechanical confinement across the lateral directions provided by the cell casing"*) · *"the electrode is flexible to move along the thickness (z direction)"* · 위 경계 *"allows for minor displacement"* | [인쇄] p.10 · p.12 · p.16 · p.21 · 그림 2a |
| 강체 · 무변형 | 분리막 · 집전체 = 강체 (*"their deformation induced by NMC622 volume change is negligible"* · *"allows computational resources to be concentrated on … the active and composite phases"*) · Li-In 부피 변화 0 (*"equivalent to using a zero-strain anode material as lithium titanate"*) | [인쇄] p.12 · p.16 |
| 구성 | AM · SE · CBD 선형 탄성 · 소성 무시 · 파괴 · 손상 없음 · 상 사이 계면 = [미확인] (완전 접합으로 읽힘 [카드 해석 — 메시 공유]) | [인쇄] p.11 · p.15 |
| 물성 | **표 S1 · S2 (SI) — 이 PDF 에 없음** · 같은 사슬의 다른 카드 값 (우리가 이 논문 값으로 쓰지 않는다): [29] 표 S2 = NMC622 C_spec 200 mAh/g · c_max 49 mol/L · ρ 4.77 g/cm³ · SE δ_ion 0.7 mS/cm 등 [다른 카드 benhadjali2025] · 같은 계열 2D 완전결합 [20] = LPSC E 22.1 GPa · ν 0.37 · NMC E 175.27 GPa [다른 카드 taghikhani2025] | [미확인] · [다른 카드] |
| 운전 | 정전류 C/10 · 충방전 **5 사이클** (그림 4 = 약 101.8 h [판독]) · 60 °C · 68 MPa (그림 6 안) | [인쇄] p.8 · 그림 6 |
| 출력 위치 | σzz = **집전체/양극 계면 평균** (*"corresponds to the location where pressure is typically measured experimentally using force or pressure sensors placed at the current collector"*) · 두께 변화 = 양극 | [인쇄] p.16 |
| 계산 자원 | MatriCS 노드 하나 · **500 GB RAM** · Xeon E5-2680 v4 · 28 코어 · 요소 · 자유도 · 실행 시간 [미확인] | [인쇄] p.8 |

### 3-5. 결과 ① — 한 방향 ↔ 양방향 결합 (§4.1 · 그림 3 · p.12–14 · `fig_3b.png` · `fig_3c.png` · `txt_p13_p14_overpotential_sign_mechanism.png` · `txt_p14_soc_mechanical_pull_claim.png`)

- 설계 (p.13): *"(i) one-way coupling, in which electrochemical processes generate mechanical deformation without feedback … (ii) full two-way coupling … For this comparative study, the electrochemical and mechanical parameters were kept identical"* · 비교 조건 (C-rate · 충전인지 방전인지 · 몇 번째 사이클) **원문 없음** [미확인].
- 그림 3b (평균 과전압 vs 비용량) [판독]: 한 방향 −53.8 (0) → 평탄부 (40–110 mAh/g) 평균 **−51.0 mV** → 끝 155.6 mAh/g (−39.3) / 양방향 −56.0 → 평탄부 평균 **−53.3 mV** → 끝 151.9 mAh/g (−41.8) → 차 **≈2.3 mV (≈4.5 %)** · 끝 용량 **양방향이 ≈3.7 mAh/g (2.4 %) 작다** [카드 산술].
- 그림 3c (AM SOC vs DOD) [판독]: 같은 DOD 에서 양방향 SOC 가 높다 — DOD 10 % 0.461 ↔ 0.515 · 40 % 0.749 ↔ 0.828 · 60 % 0.900 ↔ 0.945 · 끝 DOD 77.9 % (0.991) ↔ **75.7 % (1.000)**.
- 저자 해석: 리튬화 때 AM 이 SE · 적층압에 맞서 팽창 → σ_h < 0 → *"this compressive term (Ωσ_h < 0) increases the chemical potential, thereby lowering the equilibrium potential. As a result … the system must overcome a higher overpotential η"* (p.14) · SOC 는 *"the compression acts as a mechanical "pull," promoting lithium accumulation … allowing the battery to reach a higher average SOC before reaching the cutoff voltage"* (p.14) · 결론 *"electrochemical responses can be underestimated when one-way coupling approaches are employed"* (p.21).
- ⚠ [카드 해석] ① 같은 단락 안에서 압축 응력이 μ 를 **올린다** (p.14 위) 와 **내린다** (*"this compressive stress lowers the local chemical potential of lithium"* p.14 아래) 가 함께 있다 — 식 (5) (−Ωσ_h, σ_h < 0) 로는 올린다가 맞다 ② 통과 전하 (DOD) 가 같으면 부피 평균 리튬량은 같아야 하므로, 그림 3c 의 'SOC' 차는 **전하 보존량이 아닌 평균** (표면 · 입자 산술 평균 등) 이어야 한다 — 정의 [미확인] ③ *"higher average SOC before reaching the cutoff"* ↔ 끝 DOD · 끝 용량은 양방향이 작다 ④ η 는 BV (그림 1) 에서 국소 전류가 정한다 — E_eq 이동이 곧 η 증가는 아니다 (전류 분포가 바뀌어야 평균 η 가 바뀐다).

### 3-6. 결과 ② — 거시 응력 · 두께 (§4.2 · 그림 4 · p.14–18 · `fig_4a`–`fig_4d` · `txt_p16_sigmazz_minus78_plus35_minus110.png` · `txt_p17_thickness_068_261_329_0725.png` · `txt_p18_irreversibility_rearrangement_claim.png`)

| 양 (첫 사이클) | 본문 [인쇄] | 그림 [판독] |
|---|---|---|
| σzz 처음 (탈리튬 시작) | **−78 MPa** (p.16) | −78.0 (그림 4b · t 0.15 h) · −77 (4a) |
| σzz 최대 (충전 끝) | 인장 **35 MPa** (p.16) | +35.1 (10.08–10.16 h) |
| σzz 0 지남 | *"a brief transition"* | ≈8.6 h (충전) · ≈11.5 h (방전) [판독 · 눈대중] |
| σzz 방전 끝 | **−110 MPa** *"shows irreversibility"* (p.16) | −109.4 (20.08 h) |
| 두께 처음 | **−0.68 %** (*"the initial compressive load"* · p.17) | −0.70 (그림 4c · 4d) |
| 두께 충전 끝 | 충전 중 **−2.61 %** → **−3.29 %** (p.17) | −3.30 (Q ≈203.7 mAh/g · 그림 4d) |
| 두께 방전 끝 | *"slightly expands by 0.725 % from the initial state"* (p.17) | +0.03 / +0.04 % (그림 4c · 4d) · 그림 4d 표기 *"Irreversible height change"* = −0.70 ↔ +0.03 → 0.73 %p |
| 결론 문장 | *"average axial stress change of approximately 110 MPa … irreversible thickness change of approximately 0.725 %"* · *"only during the first cycle … for the remaining cycles the evolution was completely reversible"* (p.22) | — |

- **다섯 사이클 [판독 그림 4a · 4c]**: 사이클마다 σzz 최대 35.1–35.5 MPa · 최소 −109.4 – −109.8 MPa · 두께 최소 −3.32 % · 방전 끝 +0.04 % 로 **같은 꼴이 되풀이** 되고, 사이클 경계 (20.4 · 40.7 · 61.0 · 81.3 h) 마다 σzz 가 −110 → **≈ −76 MPa**, 두께가 +0.04 → **−0.71 %** 로 **수직으로 되돌아간다** → '비가역' 은 쌓이지 않는다.  두께 최소의 평평한 구간이 사이클마다 길어진다: 0.5 · 0.6 · 1.1 · 2.8 · 3.0 h [판독] (원인 서술 없음).
- **그림 4b Li 농도 축** (*"10³ X mol m⁻³"*): 처음 ≈48.1 (0.15 h) · 충전 끝 ≈0 (10.15 h) · 방전 끝 ≈48.8 (20.3 h) [판독] → 처음과 끝 농도가 같은데 응력 · 두께는 다르다 · 축이 무엇의 농도인지 (부피 평균 · 기준을 뺀 값) [미확인] — [29] 의 c_max 49 mol/L · ρ 4.77 g/cm³ [다른 카드] 로 '전부 비움' 은 49 × 10³ × 96485 / 4.77 × 10⁶ = 991 C/g = **275 mAh/g** [카드 산술] ↔ 모의 충전 용량 ≈203.7 mAh/g [판독] → 축 0 이 '완전 탈리튬' 이면 맞지 않는다.
- 저자 해석 (p.18): *"The externally applied pressure promotes particle rearrangement and densification within the composite cathode during the first cycle. These microstructural adjustments lead to a permanent compaction of the electrode structure, resulting in a residual thickness reduction that is not fully recovered"* — ⚠ [카드 해석] 선형 탄성 · 고정 메시 연속체에는 **재배열 · 치밀화 기전이 없다** · 그림 4d 의 방전 끝 두께는 처음보다 **두껍다** (+0.04 ↔ −0.70 %) — '영구 압밀 · 잔류 두께 감소' 와 방향이 반대.
- **[카드 산술] 겉보기 탄성률**: 적층압 68 MPa ↔ 두께 −0.68 % → 구속 탄성률 M ≈ **10 GPa** (선형 탄성 · 무응력 메시 기준 · 물성 표 없이 역산).
- **[카드 산술 · 가정 둘] 두께 변화의 크기**: 측면이 고정이면 거시 부피 변화 = 두께 변화 · 고체 부피 보존 + 기공 부피 불변이면 Δt/t ≈ φ_AM × ΔV/V = 0.23 (= [29] 20 % 구조 AM 분율 [다른 카드]) × (−4.8 %) = **−1.1 %** ↔ 모델 **−2.61 %** → 나머지 ≈ −1.5 %p 는 기공이 닫히거나 SE · CBD 가 더 눌린 몫이어야 한다 — 원문 분해 없음.

### 3-7. 결과 ③ — 공간 분포 (§4.3 · 그림 5 · p.18–19 · `fig_5a`–`fig_5d` · `txt_p18_spatial_fields_shear_1gpa_contact_loss.png`)

| 패널 | 탈리튬 시작 | 탈리튬 끝 | 리튬화 끝 | 색 막대 · 표지 |
|---|---|---|---|---|
| (a) AM σzz | 고르게 ≈ −0.3 … 0 GPa (접점 일부 ≈ −1) | 적색 포화 (≥ +0.5 … +1 GPa · 인장) 와 청록 · 청색 (−1 … −2) 섞임 | ≈ −0.3 GPa 바탕 + 접점 청색 (−1.5 … −2) | −2.5 … 1 × 10⁹ N/m² (행 제목은 *"[MPa]"*) [판독] |
| (b) AM 정수압 응력 | 주황 (≈ 0 … +0.25) | 진청 포화 (≤ −2.5) + 청록 | 적색 · 진적색 (≥ +0.5 … +1 포화) | 같은 막대 [판독] — ⚠ (a) 와 부호가 반대로 보인다 (탈리튬 끝: σzz 적색 = 인장 ↔ σ_h 청색) → **압력 p = −σ_h (압축 양) 로 그린 것** 으로 읽힌다 [카드 해석 · 원문 정의 없음] |
| (c) AM–SE 계면 전단 | ≈ 0 … 0.1 GPa | 위쪽에 포화 (≥ 1 GPa) 조각 + 넓게 0.2–0.6 | 대부분 ≤ 0.2 · 위쪽 몇 곳 0.5–1 | 0 … 10 × 10⁸ N/m² · 어느 전단 성분인지 [미확인] |
| (d) 양극 부피 변형률 | ≈ 0 … +0.005 | AM 진청 (≤ −0.04 포화) · SE / CBD 노랑 · 주황 (0 … +0.01) | AM **진적색 (≥ +0.02 포화)** | −0.04 … 0.02 [판독] |

- 본문 (p.18): 탈리튬이 진행되면 수축이 *"spatially non-uniform"* · *"This non-uniformity in the nature of strain is likely resulting from partial contact loss"* · 계면 전단 *"reaches up to 1 GPa, which is clearly the result of particle loss of contact between particles (Figure 5c)"* · 캡션: *"All these physics are extracted at the first cycle at C/10 and using a deformation scale factor of 2.8."*
- ⚠ [카드 해석] ① 이 모형에는 접촉 · 분리 · 미끄럼이 없다 (공유 메시 선형 탄성) — 큰 계면 전단은 '접촉 손실의 결과' 가 아니라 결합된 계면이 수축 차를 받은 결과이고, 실제 분리를 보려면 계면 요소 (CZM 등) 가 있어야 한다 ② 결론의 *"2.5 GPa in compressive and 1 GPa in tensile"* (p.22) = 색 막대의 양끝 (−2.5 · +1 × 10⁹) 이고 양끝 색이 포화돼 있어 **계산된 최대값이 아니다** ③ (d) 리튬화 끝 AM 부피 변형률 ≥ +2 % 는 NMC622 ΔV (≤ 0 · 완전 리튬화에서 0 · 그림 2b) 로는 나올 수 없는 크기 — 그림 4 의 '방전 끝이 처음보다 두껍고 더 눌린' 상태와 같은 쪽 · 원인 [미확인].

### 3-8. 결과 ④ — 실험 대조 (§4.4 · 그림 6 · p.19–21 · `fig_6.png` · `txt_p20_p21_validation_charge_discharge_upper_bc.png`)

| 사이클 | 모의 충전 끝 | 모의 방전 끝 | 실험 충전 끝 | 실험 방전 끝 |
|---|---|---|---|---|
| 1 | ≈203.2 mAh/g · 4.32 V | **≈203.5 mAh/g** · 2.83 V | ≈201.3 · 4.32 V | **≈191.7** · 2.92 V |
| 5 | ≈186.8 · 4.25 V | ≈187.1 · 2.76 V | ≈182.2 · 4.28 V | ≈182.8 · 2.73 V |

표지: [판독] 그림 6 (눈금 보정 · ±1–2 mAh/g) · 그림 안 조건 = NMC622 \| LPSCl \| Li · 0.1C 충 · 방 · **60 °C · 68 MPa** · 1C = 200 mA g⁻¹ [인쇄].
- 1 사이클: 모의 쿨롱 효율 ≈100 % (203.5/203.2) ↔ 실험 ≈95 % (191.7/201.3) · 모의 방전이 **+6 %** 크다 · 방전 평탄부 (120 mAh/g) 모의 3.745 ↔ 실험 3.707 V [카드 산술 · 판독].
- 저자 (p.20–21): 충전 일치는 *"expected"* (매개변수를 충전 자료에서) · 방전 차 = SEI 미반영 + *"the discharge process in the simulation is not constrained by experimentally fitted discharge parameters"* + 위 경계가 약간 움직여 방전 끝 압력이 준다 (실험은 나사 고정).
- ⚠ [판독 · 카드 산술] 그림 4a 의 사이클 간격은 다섯 사이클 모두 ≈20.3 h 로 같고 (곡선 0.39–101.8 h · 경계 ≈20.3 · 40.6 · 60.9 · 81.2 h) σzz 최대까지 ≈9.9–10.3 h — C/10 (20 mA/g) 이면 ≈198–206 mAh/g · 첫 사이클 그림 6 의 203.2 + 203.5 mAh/g (= 20.3 h) 와는 맞는다 ↔ 그림 6 의 **5 번째 모의 충전 ≈186.8 · 방전 ≈187.1 mAh/g** (= 18.7 h) · 그림 4c 의 두께 최소 평평한 구간은 0.5 → 3.0 h 로 길어진다 — 휴지 · 정전압 단계가 있는지, 두 그림이 같은 계산인지 원문 서술 없음 [미확인].

### 3-9. ★ 원문 안 어긋남 (원문 비판 목록 — §11 에 다시)
1. **식 (16) 둘째 꼴**: (ΔV/V₀ + 1) = V_x/V₀ 인데 인쇄된 둘째 꼴 ((V_x − V₀)/V_x + 1) = 2 − V₀/V_x 로 다르다 (V_x/V₀ = 0.952 일 때 0.952 ↔ 0.950 [카드 산술]) · *"V_x is the instantaneous volume, and V_x is the reference …"* (V₀ 자리 오기) · 같은 그룹 2026-11 판은 (V_x/V₀)^⅓ − 1 로 바로 적었다 [다른 카드 benhadjali2026 §4-3].
2. **식 (12) 본문**: ε_e 를 *"total"* 로 부름 · **그림 1**: 고유변형을 *"ε_e"* 로 적음 (식 14 는 ε_int) · p.10 *"(see Equation (9))"* ← μ 의 응력 항은 식 (5).
3. **σzz 의 힘 평형** [카드 산술 · 카드 해석]: 집전체 면 고체 넓이 평균으로 읽으면 시작 −78 MPa = 68 / 0.872 → 계면 기공 ≈12.8 % = 구조 기공 12 % (p.7) 와 맞는다 · 그러나 충전 끝 **+35 MPa (인장)** 은 위면 68 MPa 압축만 걸린 순수 압력 경계 + 미끄럼 벽으로는 힘 평형이 안 된다 → 측벽 '고정 벽' 이 전단을 받거나 위 경계가 변위로 묶여 있어야 한다 (p.16 *"flexible to move along the thickness"* · p.21 *"minor displacement"* 로는 어느 쪽인지 [미확인]) → 이 σzz 진폭 (≈113 MPa) 은 **구속 방식이 만든 값** 이다.
4. **'첫 사이클만 비가역'** (p.17–18 · p.22) ↔ 그림 4a · 4c: 다섯 사이클이 같은 꼴 · 경계에서 되돌아감 [판독] · '잔류 두께 감소' ↔ 그림 4d 방전 끝이 더 두껍다 · *"average axial stress change of approximately 110 MPa"* ↔ 시작 대비 −32 MPa (−78 → −110) [카드 산술] (110 은 끝 값).
5. **'재배열 · 영구 압밀'** (p.18) · **'입자 접촉 망 재편'** (*"irreversible structural changes associated with reorganization of the particle contact network"* p.22) · **'접촉 손실'** (p.18) — 선형 탄성 · 공유 메시 모형에 그 기전이 없다 [카드 해석].
6. **μ 부호 서술의 앞뒤 모순** (p.14 · §3-5 ⚠ ①) · **SOC 정의** (§3-5 ⚠ ②) · **끝 용량** (양방향이 작다 ↔ *"higher average SOC before reaching the cutoff"*).
7. **그림 5 단위 · 부호**: 행 제목 *"[MPa]"* ↔ 색 막대 N/m² × 10⁹ · 정수압 패널의 부호 (§3-7) · 결론 GPa 값 = 색 막대 끝.
8. **그림 2a 두께 44.6 µm ↔ [29] 같은 구조 36.8 µm** [다른 카드] · 40 ↔ 41 µm.
9. **그림 4 ↔ 그림 6 대응**: 그림 4 의 사이클 간격은 다섯 번 모두 ≈20.3 h (C/10 이면 사이클마다 ≈406 mAh/g) ↔ 그림 6 의 5 번째 모의 충 + 방 ≈373.9 mAh/g (≈18.7 h) [판독 · 카드 산술] — 휴지 · 정전압 단계 여부 서술 없음 [미확인] (§3-8).
10. **'novel … fully coupled … 3D-resolved' 주장** (p.4) ↔ 자기 ref [24] 제목 (*"… coupling electrochemistry and solid mechanics on resolved microstructures …"*) 을 '단일 입자' 로 묶음 — [24] 원문 확인 필요 (n 후보).
11. **'experimentally validated'** (p.4 · p.21) — 매개변수 (OCV · D · j₀) 와 검증 곡선이 같은 셀 · 같은 충전 자료 · 역학 검증 없음.
12. **표기**: 저자 소속 (p.1 표지 ↔ p.2 원고 · §머리) · *"computatinal"* (p.22) · *"repectively"* (그림 5 캡션) · 그림 3 범례 *"Full-way coupling"* ↔ 본문 *"full two-way coupling"* · 참고문헌 [26] ↔ [36] = 같은 일의 출판본 · 프리프린트 (제목 같음 · 'Solid-State' ↔ 'Solid State') · [28] · [32] 웹 서지 *"(n.d.)"* · [37] 제목에 MathML 조각 · [30] 은 표지 기사 (Cover Feature) 서지 · 결론 *"NMC622 AM undergoes a ~ 4.8 % volume expansion upon de(lithiation)"* (p.21) — 탈리튬은 수축 (그림 2b · p.10 은 *"volumetric change"*).

---

## 4. ★ 방법 — 계산 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 계산 사슬 (단계별)
1. **제조 모의 (이 논문 밖 · [27])**: CGMD · LAMMPS · 슬러리 → 건조 → 압연 (두께 0 … 50 % 감소 [다른 카드 alabdali2023]) · 이 논문은 **20 % 구조 하나** 만 쓴다 (p.8).
2. **후처리 · 메시 (p.8)**: 복셀화 · CBD 와 겹친 부피를 AM / SE 에 더함 (CBD 미세 기공 함축) → 구 → 불규칙 모양 · INNOV 다상 체적 메시.
3. **실험 매개변수화 (p.4–6)**: 반쪽 셀 GITT · EIS → OCV · D_Li · j₀ (값 = 그림 S1 [미확인]).
4. **FEM (p.8–12)**: COMSOL · 반쪽 셀 · 식 (3)–(16) + 그림 1 BV · 68 MPa · 측벽 고정 · 분리막 · 집전체 강체 · C/10 5 사이클 · 한 방향 ↔ 양방향 두 판.
5. **출력 (p.12–19)**: 평균 과전압 · SOC (그림 3) · 집전체 면 평균 σzz · 두께 (그림 4) · AM σzz · σ_h · 계면 전단 · 부피 변형률 지도 (그림 5) · 전압 곡선 대조 (그림 6).

### 4-2. 입자 처리 (우리 축 언어로)
- **제조 단계**: 강체 구 거친 입자 (AM · SE · CBD) + LJ + 입자 Hertz (정본 alabdali2023 [다른 카드]) — 형상 불변 · 겹침 = 압밀 대리 · 응력 출력 없음.
- **넘김**: 겹친 CBD 부피를 AM · SE 에 더하는 **기하 후처리** 로 모양을 만든다 — 역학의 결과가 아니다 (우리 R6 '형상 변형' 의 근거로 쓰지 않는다).
- **FEM 단계**: 공유 메시 위 연속체 · 세 상 선형 탄성 · AM 에만 리튬 고유변형 · 상 사이 계면 = 붙어 있음 [카드 해석] · 입자 정체성 (같은 상 입자 사이 경계) 사라짐.
- **우리 대응** [우리 — CLAUDE.md]: DEM = 강체 구 + hooke/hysteresis (겹침 = 소성 대리 · SE E_eff 1.35 GPa · 18 배 연화) · MPM = SE J2 소성 (E 1.53 · σ_y 0.30 GPa · ν 0.49 → K 25.5 GPa) · AM = 고정 장애물 · STEP3 = 복셀 FV σ · STEP4 = 입자별 구형 1D 확산 + BV (역학 결합 없음).  ⇒ 그들 FEM ≈ "우리 MPM 에서 소성을 빼고 AM 을 탄성체 · 리튬 팽창 · 응력 의존 확산을 넣은 것".

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
- **(i) DEM (단단한 구 · 점접촉) 의 한계**: 직접 문장은 *"enables the transformation of ideal spherical shapes in CGMD into more realistic, irregular shapes of all the composite cathode phases"* (p.8 — 구 모양이 비현실적이라는 전제) 하나 · 겹침 상한 · 밀도 · 연화 언급 없음 · 계산 비용 한계 = *"when simulations are performed on 3D-resolved microstructures, all the few existing studies rely on one-way coupling … due to the complexity of the multiphase microstructure and the high computational cost [25,26]"* (p.4).
- **(ii) 소성 · 큰 변형을 넣기 어려운 이유와 우회**: *"most of the active material is expected to operate predominantly within the elastic regime under typical cycling conditions [17,18]. This simplification is commonly employed … as it allows stress evolution investigation with minimum computational cost."* (p.11) · *"The plasticity as a material property is ignored in this study, however at the electrode scale, due to microstructural rearrangement it might have an irreversibility in the material response."* (p.15–16) · 우회 = **선형 탄성 + 고유변형** (맞춘 값 0 · 물성 SI) · 비용 = 노드 하나 500 GB · 28 코어 · 앞으로 = *"plastic deformation and fracture of AM particles and SE"* · 손상 역학 (p.22).
- **(iii) 2D / 3D**: **3D** · 2D 는 선행 분류로만 — *"Fully coupled models have already been reported for simplified representations, such as 1D configuration [19], 2D domains [20], single cathode particle [21–24], or following homogenized approaches"* (p.4) · 2D → 3D 전이에 대한 말 없음.
- **(iv) 압력을 뺄 때**: **다루지 않음** — 적층압 68 MPa 를 사이클 내내 유지 · 제하 · 되튐 계산 없음 · 위 경계의 '약간의 변위' 가 방전 끝 압력을 줄인다는 서술 (p.21) 만.

### 4-4. 기법 미니 용어집
- **한 방향 (one-way · weak) / 양방향 (two-way · strong · full) 결합**: 전기화학이 역학만 바꾸는가 / 역학이 다시 전기화학을 바꾸는가 (p.3).
- **화학-기계 퍼텐셜 μ**: 화학 퍼텐셜에 정수압 응력의 일 (−Ωσ_h) 을 더한 것 — 인장 (σ_h > 0) 이 μ 를 낮춰 Li 가 인장 쪽으로 흐르고 E_eq = −μ/F 가 오른다.
- **고유변형 (eigenstrain · intercalation strain)**: 응력 없이 생기는 변형 (리튬 농도 변화의 부피 변화) — 구속되면 응력이 된다 (열응력과 같은 꼴) · 변형 제어라 응력 ∝ 탄성률.
- **부분 몰 부피 Ω**: Li 1 mol 이 바꾸는 부피 — 여기서는 격자 부피 자료 (ΔV) 의 할선 값 (식 15).
- **CGMD**: 입자 하나가 실제 입자 (또는 덩이) 하나를 대신하는 거친 입자 동역학 (LAMMPS).
- **INNOV**: Franco 그룹의 미세구조 생성 · 복셀 다상 메싱 도구 [30, 31].
- **Weppner–Huggins GITT · R_ct → j₀**: 식 (1) · (2) — 구형 입자 반지름 · 기하 면적을 가정한 겉보기 값.
- **변형 배율 (deformation scale factor)**: 그림에서 변위를 과장해 그리는 배수 (그림 5 = 2.8) — 물리량 아님.

---

## 5. Figure set ★ (크롭 55 장 = `litdb/figures/benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 (`fig_1.png` · `fig_1_eqbox.png`) | 작업 흐름 — 슬러리 → 건조 → 압연 (CGMD) → NMC SSB 반쪽 셀 (분리막 · 집전체 · 메시) → 식 상자 셋 (전기화학 BV · 물질 전달 J · 부피 팽창 ε) → 다중물리 출력 (리튬화 · 과전압 · 응력) · 결합 고리 (Li 농도 → 역학 · 화학-기계 퍼텐셜 → 전기화학 · *"n-th / (n+1)-th iteration · displacement"*) | ★ BV 꼴의 유일한 출처 (`fig_1_eqbox`) · 결합 고리 그림 한 장 |
| 2 (`fig_2.png` · `fig_2a.png` · `fig_2b.png`) | (a) 반쪽 셀 영역 40 × 40 µm · 74.6 / 44.6 µm · Li metal · 분리막 · 집전체 · 위면 적층압 · 측면 고정 벽 · 아래 고정 지지 (b) Koerver 2018 재수록 ΔV/V₀ vs x(Li) (LCO · NCM-111 · 523 · 622 · NCA · 811) | ★ 경계 그림 (§3-4) · 두께 44.6 µm (§3-2 불일치) · ΔV 원자료 = 정본 koerver2018 그림 2a · ⚠ `fig_2a` 오른쪽 위 옅은 세로선 = 패널 b 래스터 테두리 (원 그림의 일부) |
| 3 (`fig_3.png` · `fig_3b.png` · `fig_3c.png`) | (a) 한 방향 ↔ 양방향 결합 그림 (b) 평균 과전압 vs 비용량 (c) AM SOC vs DOD | ★ 결합 효과 크기 (≈2.3 mV [판독]) · SOC 정의 문제 (§3-5) |
| 4 (`fig_4.png` · `fig_4a`–`fig_4d`) | (a) σzz (집전체 면 평균) · 전위 vs 시간 5 사이클 (b) 1 사이클 σzz · Li 농도 vs 시간 (c) 두께 변화 · 전위 vs 시간 (d) 1 사이클 두께 vs 비용량 + *"Irreversible height change"* | ★ 거시 응력 · 두께 (§3-6) · 사이클 경계 되돌아감 · 평평한 최소 구간 [판독] |
| 5 (`fig_5.png` · `fig_5a`–`fig_5d`) | 탈리튬 시작 · 끝 · 리튬화 끝 × (a) AM σzz (b) AM 정수압 응력 (c) AM–SE 계면 전단 (d) 부피 변형률 · 변형 배율 2.8 (패널 크롭은 열 머리 띠를 위에 붙임) | ★ 색 포화 · 부호 (§3-7) · '접촉 손실' 해석의 근거 그림 |
| 6 (`fig_6.png`) | 모의 ↔ 실험 전압 곡선 (1 · 5 번째 사이클) · NMC622 \| LPSCl \| Li · 0.1C · 60 °C · 68 MPa | ★ 검증의 전부 (§3-8) |

- **식 크롭 16 장** (식 번호마다 하나 · 칼럼 폭 · 식 번호 포함): `eq_01_weppner_huggins_gitt` · `eq_02_rct_exchange_current` · `eq_03_li_conservation_am` · `eq_04_flux_chemomechanical_potential` · `eq_05_mu_hydrostatic_stress` · `eq_06_flux_stress_gradient` · `eq_07_stress_concentration_pde` · `eq_08_overpotential` · `eq_09_eeq_from_mu` · `eq_10_mechanical_equilibrium` · `eq_11_hooke_linear_elastic` · `eq_12_total_strain` · `eq_13_elastic_strain` · `eq_14_intercalation_strain` · `eq_15_partial_molar_volume` · `eq_16_linear_strain_lambda` (+ 그림 1 의 식 상자 `fig_1_eqbox`).
- **근거 문단 크롭 20 장** (카드가 숫자 · 정의 · 단정의 근거로 인용한 문단만):

| 파일 | 근거로 쓴 곳 |
|---|---|
| `txt_p4_prior_coupled_models_novelty_claim` | 선행 = 1D · 2D · 단일 입자 · 균질화 · 3D 는 한 방향 (비용) · 'novel … experimentally validated' (§0-1 · §4-3) |
| `txt_p5_halfcell_assembly_3t_2t_68mpa` | 2 t · 3 t · 토크 11 N m = 68 MPa (§3-1) |
| `txt_p5_p6_cycling_gitt_protocol` | 25 사이클 · 60 °C · 1.9–3.7 V · 1C = 200 mA/g · 처음 다섯 사이클 = 검증 · GITT (§3-1) |
| `txt_p6_p7_parameterization_microstructure_source` | OCV · D · j₀ = 그림 S1 · 구조 출처 [27] · 10 µm · 12 % · [29] · [26] 재사용 (§3-2) |
| `txt_p8_oneway_extension_20pct_overlap_voxel` | 한 방향 [26] 확장 · 20 % 구조 · 겹침 규칙 · INNOV (§3-2) |
| `txt_p8_comsol_halfcell_5cycles_hardware` | COMSOL 반쪽 셀 · 5 사이클 C/10 · 500 GB · 28 코어 (§3-4) |
| `txt_p9_coupling_terms_vs_previous_study` | 식 (7) 셋째 · 넷째 항 = 되먹임 · [36] 대비 (§3-3) |
| `txt_p10_p11_stack_bc_dv_linear_elastic` | 68 MPa 경계 · ΔV ~4.8 % · AM 탄성 가정 · 세 상 선형 탄성 (§3-3 · §4-3) |
| `txt_p12_dv_definition_rigid_separator_bcs_tables` | ΔV 정의 (V_x 두 번) · 분리막 · 집전체 강체 · 고정 지지 · 고정 벽 · 표 S1 · S2 (§3-4 · §3-9) |
| `txt_p13_p14_overpotential_sign_mechanism` | 같은 매개변수 · 과전압 해석 · μ 부호 (§3-5) |
| `txt_p14_soc_mechanical_pull_claim` | SOC · 'mechanical pull' · μ 부호 모순 (§3-5 · §3-9) |
| `txt_p15_p16_plasticity_ignored_uniaxial_sigmazz` | 소성 무시 · z 방향만 자유 · σzz 위치 · 무변형 음극 (§3-4 · §4-3) |
| `txt_p16_sigmazz_minus78_plus35_minus110` | −78 · +35 · −110 MPa (§3-6) |
| `txt_p17_thickness_068_261_329_0725` | −0.68 · −2.61 · −3.29 · 0.725 % · 68 MPa 충분 (§3-6) |
| `txt_p18_irreversibility_rearrangement_claim` | 재배열 · 영구 압밀 해석 (§3-6 · §3-9) |
| `txt_p18_spatial_fields_shear_1gpa_contact_loss` | 공간 분포 · 접촉 손실 · 전단 1 GPa (§3-7) |
| `txt_p20_p21_validation_charge_discharge_upper_bc` | +0.65 V · 충전 일치는 당연 · 방전 차 · 위 경계 (§3-8) |
| `txt_p21_p22_conclusion_irreversibility_local_stress` | 결합 비교 결론 · '110 MPa' · '0.725 %' · 2.5 / 1 GPa (§3-6 · §3-7) |
| `txt_p22_validation_summary_future_plasticity_fracture` | 충전 위주 일치 · 앞으로 소성 · 파괴 · 손상 (§4-3 · §0 ⑨) |
| `txt_p23_supplementary_placeholder_xxx` | SI = *"XXX"* (물성 [미확인] 의 근거) |

- 다시 자른 것 3 (figures.json `recrop`): `txt_p21_p22_conclusion_irreversibility_local_stress` (첫 판이 앞 문단 끝 두 줄을 물었다) · `fig_1_eqbox` (첫 판이 양옆 그림 가장자리를 물었다) · `fig_2a` (첫 판이 패널 b 테두리 선을 물었다).  그림 2 캡션 문자열에 붙은 절 제목만 figures.json 에서 뺐다 (그림은 그대로).

## 6. Post-processing ★
- **저자가 한 것**: GITT (Weppner–Huggins) · EIS (RelaxIS 등가회로 → R_ct → j₀) · FEM 출력 = 계면 평균 σzz · 두께 변화 · AM 평균 과전압 · AM SOC · 3D 장 지도 (σzz · σ_h · 계면 전단 · 부피 변형률 · 변형 배율 2.8) · 전압 곡선 겹쳐 그리기 (+0.65 V 이동).
- **안 한 것**: 장의 분포 · 분위수 · 평균 (지도는 색 막대 포화) · 상별 (SE · CBD) 응력 · 메시 수렴 · 시간 간격 수렴 · 반복 · 오차 막대 · 역학 실험 대조 (두께 · 압력 측정) · 물성 공개 (SI) · 결합 비교의 조건 표기 · 사이클 경계의 되돌아감 설명.
- **우리 후처리 (이 카드)**: 300 dpi 패널 크롭의 축 틀 · 눈금 위치를 화소로 찾아 선형 보정 → 색 화소 (빨강 · 파랑 · 검정) 열마다 극값 → 그림 3b · 3c · 4a · 4b · 4c · 4d · 6 판독 (digitized.csv 92 행 · 인쇄값 재현: −78 ↔ −78.0 · 35 ↔ 35.1 · −110 ↔ −109.4 · −0.68 ↔ −0.70 · −3.29 ↔ −3.30 · 0.725 ↔ 0.73 %p) · 힘 평형 · 두께 · 용량 · 결합 크기 [카드 산술] (§3-3 · §3-6 · §3-9).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (우리 수치는 CLAUDE.md 출처를 그 자리에 적는다)

### 7-1. ★ 넘김 사슬 나란히 (질문 h · 단계별)

| 단계 | 이 논문 | 우리 (CLAUDE.md) | 같음 / 다름 |
|---|---|---|---|
| 제조 · 압밀 | CGMD (LAMMPS · LJ + Hertz · 변위 제어 압연 · 두께 감소율) — 이전 논문 [27] 의 구조 재사용 · 압력 없음 | DEM (LIGGGHTS · hooke/hysteresis · **하중 제어 300 MPa** → 판 고정 이완) | 둘 다 강체 구 · 우리는 압력 축 · 그들은 두께 축 |
| 넘기는 시점 | '압연 뒤 20 %' (되튐 · 판 분리 · 응력 서술 없음) | 300 MPa 도달 뒤 판 고정 이완 덤프 → MPM 재압밀 (scaffold) · 언로딩 등록 = 하중을 뺀 상태 (DEM 우선 Ⓐ) | 둘 다 '누른 상태' 를 넘긴다 · 우리는 탈압 상태를 따로 등록 중 |
| 넘기는 자료 | 메시 (기하) 만 · 잔류 응력 0 · 68 MPa 경계로 새로 시작 | MPM 에 AM 좌표 (고정 장애물) + SE 씨앗 · MPM `--save-state` / `--load-state` 로 F 이력 이어받기 [다른 카드 benhadjali2026 §7-1] | 둘 다 압밀 잔류 응력을 사이클 모형에 넘기지 않는다 |
| 겹침 처리 | CBD 겹침 부피를 AM / SE 에 더함 (형상 = 기하 후처리) | DEM ε_sphere ↔ ε_union · MPM SE 씨앗 = AM 아닌 칸 | 둘 다 AM 우선 · 그들은 CBD 를 줄이고 우리는 겹침을 소성 대리로 둔다 |
| 다음 모델 | COMSOL FEM 선형 탄성 + 리튬 고유변형 + 응력 의존 확산 (사이클) | MPM J2 소성 (압밀) · STEP3 복셀 FV σ · STEP4 입자별 구형 확산 + BV (역학 결합 없음) | 그들 = 사이클 응력 ↔ 전기화학 양방향 · 우리 = 압밀 소성 + 수송 |
| 검증 | 전압 곡선 (매개변수와 같은 셀) | 기공 · 두께 · σ 앵커 (순수 SE 랩 표준 10–13 % · real_14 등) | 그들은 역학 검증이 없다 |

### 7-2. 비교표 (재료 · 상태 · 측정 연산자가 행마다 다르다)

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| SE | Li₆PS₅Cl (POSCO) · 물성 SI | LPSCl · DFT E_VRH 22.06 · B₀ 26.23 GPa [우리] | 같은 SE 화학 · 그들 E [미확인] |
| AM | NMC622 · 선형 탄성 · ΔV ~4.8 % (Koerver) | NMC811 · DEM 강체 · MPM 고정 장애물 · 사이클 부피 변화 = MPM `--cycle-deform` · 접촉 장부 [우리] | AM 응력은 그들만 푼다 |
| 공정 | 습식 (CBD 3.4 wt% · 모의 CBD ≈39 vol% [다른 카드 benhadjali2025]) | 건식 분말 압밀 | 기공 · 두께 절대값 교차 인용 금지 |
| 압력 | 실험 양극 3 t (≈116 MPa [카드 산술]) · 셀 2 t (≈250 MPa) · 적층 68 MPa · 모델 = 68 MPa 경계 | 300 MPa (DEM · MPM) | 압력 축 대응 없음 (모델 구조는 두께 축) |
| 구성 | 선형 탄성 (소성 · 파괴 없음) | DEM E_eff 1.35 GPa (18 배 연화) · MPM E 1.53 · σ_y 0.30 · ν 0.49 [우리] | 변형 제어 (고유변형) 응력은 σ ∝ E — 연화 E 로는 사이클 응력이 E 비만큼 작게 나온다 (22.06/1.35 = 16.3 · 24/1.35 = 17.8 배 [카드 산술 · 우리 값]) · 같은 논지 = benhadjali2026 EM-01 *"반례 (영역 경계)"* [다른 카드] |
| 응력 판독 | 집전체 면 평균 σzz · 장 지도 (포화) | MPM 정수압 · DEM Love–Weber (상대) [우리] | 그들 진폭은 구속 방식이 정한다 (§3-9 ③) |
| 사이클 | C/10 5 사이클 · 60 °C · 양방향 결합 | STEP4 (역학 결합 없음) · A10 접촉 장부 (Bucci CZM) [우리] | 그들이 앞선 축 (응력 ↔ 전기화학) |
| 기공 | 12 % (모의 구조 · 정의 [미확인]) | ε_sphere · 랩 표준 순수 SE 10–13 % (진밀도 1.64 g/cm³) | 같은 이름 다른 양 — 견주지 않는다 |

### 7-3. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: AM 리튬 고유변형 → 응력 → 확산 · 평형 전위 양방향 결합 (사이클) · 3D 해상 반쪽 셀 · 구속 방식에 따른 거시 응력 · 장 지도.
- **없는 것**: 압밀 (가압) 역학 · SE 소성 · 형상 변화 · 접촉 (분리 · 미끄럼) · 파괴 · 접촉 저항 · 잔류 응력 · 탈압 · 역학 검증 · 물성 공개.
- **우리 쪽이 줄 수 있는 것**: 압밀 소성 (MPM) · 압력 축 · 접촉망 수송 · 탈압 상태 (언로딩 등록) — 그들 사이클 모형의 **출발 상태** 가 될 자리.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 = 사이클 FEM (선형 탄성) · 재료 NMC622 + Li₆PS₅Cl + 습식 CBD · 압밀 · 탈압 없음 · 물성 SI → **랩 표준과 나란히 놓을 숫자 없음** (순수 SE 압밀 자료 없음 · 모의 구조 기공 12 % 는 습식 CBD 포함 구조 · 정의 미확인 → '랩 표준과 다른 문헌 값' 으로도 쓰지 않는다).)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ **반례 둘**: ① 같은 '20 % 구조' 가 논문마다 두께 44.6 ↔ 36.8 µm · 옆 40 ↔ 41 µm [인쇄 · 다른 카드] → 우리 등록에 "넘긴 구조의 두께 · 옆 크기 · 기공 정의 · 출처 판 (커밋) 을 숫자로 적는 칸" ② '비가역' 을 두께 · 응력의 시작 ↔ 끝 차로만 정의하고 사이클 경계의 되돌아감을 설명하지 않음 → 우리 '되돌아옴 ρ' 처럼 **양의 정의 (기준 상태 · 측정 압력) 를 결과 전에** | 기공 연산자 자체는 없음 |
| **단계 1** (3D 메모리 · 장 수) | 자릿수 하나: 40 × 40 × (44.6 + 30) µm 반쪽 셀 · 양방향 결합 · C/10 5 사이클 = **노드 하나 500 GB RAM · 28 코어** (p.8) · 저자: 3D 해상 연구가 한 방향에 머문 이유 = *"the high computational cost"* (p.4) | 자유도 · 복셀 크기 · 실행 시간 없음 → 메모리 산식에 못 넣는다 |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 (그들 2D 언급 = 선행 [20] 분류 하나 · 정본 taghikhani2025 [다른 카드]) | — |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나) | 없음 (순수 SE · 항복 없음) | — |
| **단계 5** (3D 복합 압밀) | 없음 (압밀은 이전 논문의 CGMD · 이 논문은 결과 기하만) | — |
| **단계 6** (탈압 · 되돌아옴) | **없음** — 68 MPa 를 사이클 내내 유지 · 제하 계산 없음 · ★ 대신 **반면교사**: 탄성 연속체에 '재배열 · 영구 압밀' 을 귀속 (p.18) → 우리 단계 6 이후 사이클을 들일 때 '비가역' 은 **모형 안의 기전 (소성 · 접촉 열림 · 기공 닫힘) 을 이름으로 적고 그 몫을 따로 셈** · ★ **구속 방식이 거시 응력을 정한다** (§3-9 ③): 측벽 고정 + 강체 분리막 = 사실상 사방 구속 → 탈압 · 사이클 계산의 경계 (판 서보 · 측벽 미끄럼) 를 결과 전에 고정 | 되돌아옴 값 · 측정 없음 |
| **단계 7** (형상 · 피복 · 수송) | 3D 반쪽 셀 출력 꼴 (평균 과전압 · SOC · 장 지도) · 결합 효과의 자릿수 (≈2.3 mV · E_eq 이동 = Ωσ_h/F ≈3 mV @ 100 MPa [카드 산술]) → 우리 STEP4 에 응력 항을 넣을지 판단할 크기 감 | 수송 (σ_ion · σ_e) 출력 없음 · 피복 없음 |
| **후보 D0** (지금 DEM) | 같은 부류의 다른 판: CGMD = 강체 구 + LJ + Hertz (재매개변수 힘장 · 건조 k_n ≈1 × 10⁵ Pa [다른 카드 alabdali2023]) — 둘 다 형상은 후처리 · 다음 모델에 맡긴다 · 사이클 응력은 DEM 에서 읽지 않는다는 근거 하나 더 (그들도 DEM 응력을 넘기지 않음) | 압력 · 응력 출력 없음 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | ★ **경계의 영향 사례**: '고정 벽' 하나로 집전체 면 σzz 가 인장까지 뒤집힌다 [카드 해석 · 힘 평형] → A′-0 의 벽 규칙 (미끄럼 · 분리) 을 정할 때 이 반례를 결과 전 대조로 | 접촉 규칙 자체는 없음 |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | 없음 (FEM · 공유 메시) · 계면 '접촉 손실' 을 보려면 상 사이가 열려야 한다는 근거 (그들은 못 연다) | — |
| **후보 B** (입자별 FE + 접촉) | ★ **"B 에서 접촉을 뺀 판"** 의 실례 — 복셀 메시 FE · 세 상 공유 메시 · 계면 전단 GPa · 분리 해석은 그림 읽기뿐 → B 를 들이면 계면 요소 (CZM · 정본 bucci2017) 가 필수 · 선행 3D 결합 FE = ref [24] Schmidt 2023 (n 후보) | 접촉 · 마찰 · 다물체 없음 · 메시 정보 없음 |
| **후보 C · C′** (큰 변형 · 항복 캡 접촉 DEM) | 없음 · 인용만: [38] Lundkvist 2024 (전극층 탄소성 · 점탄성 DEM — n 후보) | — |
| **후보 M0** (균질화) | 없음 (균질화 결합 모형은 선행 분류로만 · p.4) | — |
| **U0–U6** | 직접 단위 시험 없음 · ★ 이 식에서 뽑을 수 있는 해석 검사: 단일 상 · 사방 구속 등방 고유변형 p = 3Kε₀ (정본 koerver2018 식 S6 [다른 카드]) · 가로 구속 σzz — 그들 그림 4 의 진폭을 이 해석해로 확인할 수 있었으나 하지 않았다 → 우리 사이클 모형 단위 시험 후보 (U3 의 사이클 판) | 해석 검사 · 수렴 보고 없음 |
| **R1–R7** | **R1** (AM 이 움직이고 하중을 나눔) = 연속체로 하중을 나눔 (재배열 없음) · **R2** (미끄럼 · 분리) = **없음** (해석만) · **R3** (SE 입자 경계 기억) = **반례** (메시에서 입자 경계가 사라짐) · **R4** (탈압) = 없음 · **R5** (맞춘 값 하나) = 역학 맞춤 0 · 전기화학 입력 3 (OCV · D · j₀ · 같은 셀 충전 자료) · **R6** (SE 형상 변형) = 없음 (작은 변형 선형 탄성 · 그림 변형 2.8 배 과장) · **R7** (AM 파괴) = 없음 (앞으로) | — |
| **결과 전 대조 항목** | ① 고정 틀 사이클 축 응력의 **측정** 크기: InLi \| SE \| NCM-811 ≈ +1.06 MPa (첫 봉우리 ≈1.28) · LTO \| SE \| NCM-811 ≈ −0.045 ~ −0.06 MPa (10 Nm ≈ 60 ± 8 MPa 고정 틀) [다른 카드 koerver2018 판독] ↔ 이 모델 σzz 진폭 ≈113 MPa (무변형 음극 가정 = LTO 쪽) → 자릿수 2–3 차 · 모든 면 구속 선형 탄성 추정 (NCM-811 ΔV −6.0 % → p = −65.97 MPa · 표 S3 [다른 카드 인쇄]) 쪽에 가깝다 → 우리가 사이클 응력을 내면 **측정 축 응력과 견줄 것** (모델 값과 견주지 않는다) ② 두께 변화: 68 MPa 아래 충전 −2.61 % ↔ 고체 부피만으로 ≈ −1.1 % [카드 산술 §3-6] ③ 결합 크기: 평균 과전압 ≈2.3 mV ↔ 우리 STEP4 응력 항 도입 판단 | 재료 (NCM-811 ↔ 622) · 셀 · 두께가 달라 값 대조 아님 · 자릿수만 |

- **재료 · 차원 · 조건 차이**: SE 같음 (Li₆PS₅Cl) · AM NMC622 ↔ 우리 NMC811 · 습식 (PVDF-HFP · CBD) ↔ 우리 건식 · 압밀 없음 (모의 구조 재사용) ↔ 우리 300 MPa · 3D ↔ 3D · 반쪽 셀 (Li) ↔ 우리 STEP4 반쪽 셀 · 그들 선형 탄성 사이클 ↔ 우리 MPM 소성 압밀 · 60 °C ↔ 우리 온도 인자 없음 (DEM · MPM) [다른 카드 benhadjali2026 §7-1].

## 9. 적용 인사이트 (행동)
1. **[DEM 우선 (수영)] 재설계 트랙 문장 정리**: 이 논문은 *"가압부터 한 모델"* 의 선례가 아니다 — 압밀은 이전 CGMD 몫이고 FEM 은 응력 0 기하에서 사이클만 푼다.  '완전결합' 이라는 낱말을 인용할 때 **"사이클 중 전기화학 ↔ 탄성 양방향"** 으로 한정한다 (§0-1).
2. **사이클 응력 경계를 결과 전에 등록**: 측벽 (미끄럼 / 고정) · 위판 (서보 압력 / 변위 고정) · 분리막 강체 여부 — 이 논문의 +35 MPa 인장은 경계의 산물 [카드 해석] · 측정 축 응력 (정본 koerver2018) 을 대조 항목으로.
3. **'비가역' 의 정의 · 기전 칸**: 시작 ↔ 끝 차 · 사이클 경계 처리 · 쌓임 여부 · 모형 안의 기전 이름 (소성 / 접촉 / 기공) — 그들 그림 4 의 되돌아감 [판독] 이 반례.
4. **넘김 기록 꼴**: '어느 판의 어느 구조 (두께 · 옆 크기 · 기공 정의 · 겹침 규칙 · 복셀 크기)' 를 숫자로 — 같은 그룹 두 논문 사이 44.6 ↔ 36.8 µm 가 반례.
5. **결합 항 도입 판단 (STEP4)**: E_eq 이동 Ωσ_h/F 는 100 MPa 에서 ≈3 mV [카드 산술] · 그들 평균 차 ≈2.3 mV [판독] — 우리 STEP4 의 율속 · 반응 분포 결론을 바꿀 크기인지 먼저 견적 (메인 세션 판단).
6. **장 지도 보고 규칙**: 색 막대 끝 = 최대값으로 쓰지 않는다 (그들 2.5 · 1 GPa) — 우리 EM-06 재현 조건 (분위수 · 포화 몫) 쪽이 옳다 [다른 카드 benhadjali2026 EM-06].

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Ben Hadj Ali et al. (ChemRxiv 2026, preprint, not peer reviewed) solved a two-way coupled mechano-electrochemical half-cell model — stress-dependent chemical potential μ = μ₀ + RT ln X − Ωσ_h entering both Li diffusion and the equilibrium potential, with linear-elastic active material, solid electrolyte and carbon–binder phases and an intercalation eigenstrain from measured NMC622 lattice volume changes — on a single 3D microstructure taken from their earlier wet-manufacturing particle simulation, under a 68 MPa stack-pressure boundary with fixed lateral walls; plasticity was explicitly ignored and experimental validation was limited to voltage profiles of the same cell used for parameterization."
- 국문: *"이 계열의 '완전결합' 은 사이클 중 전기화학 ↔ 선형 탄성의 양방향 결합이다 — 압밀 (제조) 은 앞선 입자 모의가 끝낸 기하로만 넘어오고, 소성 · 파괴 · 접촉 분리는 모형에 없다 (Ben Hadj Ali 2026, 프리프린트)."*
- 국문: *"측벽을 고정하고 분리막을 강체로 둔 3D 선형 탄성 반쪽 셀에서 집전체 면 평균 축 응력은 68 MPa 적층압 아래 첫 충전 끝에 +35 MPa (인장) 까지 뒤집혔다 (Ben Hadj Ali 2026) — 고정 틀 실측 축 응력 변화 (≈0.05–1 MPa, Koerver 2018) 보다 두세 자릿수 크다 (재료 · 셀이 달라 자릿수 대조만)."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **프리프린트 · SI 없음**: 물성 · 전기화학 매개변수 · 실험 자료 (그림 S1 · 표 S1 · S2) 미공개 → 모든 응력 크기는 숨은 E 에 걸려 있다 (변형 제어 · σ ∝ E).
2. **'완전결합' 의 범위**: 사이클 중 전기화학 ↔ 탄성 · 제조 압밀 · 잔류 응력 · 접촉은 결합 밖.
3. **구조 ↔ 실험 대응 없음**: 모델 구조 = [27] 모의 (다른 바인더 · 탄소 · 용매 · SE 공급처 [다른 카드]) · 실험 양극 두께 · 질량 · 기공 미인쇄 · 3 t ≈116 MPa (가정 지름) [카드 산술].
4. **검증의 독립성**: 매개변수와 검증 곡선이 같은 셀 · 같은 충전 자료 · 역학 검증 0 · 메시 · 시간 수렴 0.
5. **경계 · 힘 평형** (§3-9 ③): σzz 진폭은 구속 방식이 정한다 · 실측 축 응력 변화와 2–3 자릿수 차 [다른 카드 · 카드 산술].
6. **'비가역' 해석** (§3-9 ④ · ⑤): 선형 탄성에 재배열 기전 없음 · 그림은 되풀이 · 되돌아감 · 방향 반대.
7. **장 지도** (§3-7): 색 포화 · 부호 · 단위 표기 · 결론 GPa = 색 막대 끝.
8. **결합 비교** (§3-5): 조건 미기재 · SOC 정의 · μ 부호 모순 · 끝 용량은 양방향이 작다.
9. **그림 사이 불일치** (§3-9 ⑧ · ⑨): 두께 44.6 ↔ 36.8 µm [다른 카드] · 그림 4 (사이클 간격 일정) ↔ 그림 6 (5 번째 모의 용량 ≈187 mAh/g) 의 대응 [미확인].
10. **새로움 주장** (§3-9 ⑩): 자기 ref [24] 의 3D 해상 결합 FE 와의 관계 미확인.
11. **실용 범위**: 60 °C · 68 MPa (높은 적층압) · Li-In 반쪽 셀 (모델은 Li 금속 · 음극 부피 변화 0) · C/10 5 사이클 · 구조 하나 · 셀 하나.
12. **전이 한계 (우리 쪽)**: LPSCl 같음 · NMC622 ↔ NMC811 · 습식 ↔ 건식 · 선형 탄성 사이클 ↔ 소성 압밀 — 같은 이름 (stress · thickness change · porosity · irreversibility) 의 다른 양이 섞이지 않게 표지를 붙인다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 6 | S. Mičky, E. Šimon, J. Todt, K. Végsö, P. Nádaždy, P. Krížik, E. Majková, J. Keckes, J. Li, P. Siffalovic, Operando Spatial and Temporal Tracking of Axial Stresses and Interfaces in Solid-state Batteries, Small 20 (2024) 2307837. https://doi.org/10.1002/smll.202307837. | 카드 없음 — 사이클 축 응력의 operando 측정 (이 모델 σzz 와 견줄 실측) |
| 7 | K.G. Naik, M.K. Jangid, B.S. Vishnugopi, N.P. Dasgupta, P.P. Mukherjee, Interrogating the Role of Stack Pressure in Transport-Reaction Interaction in the Solid-State Battery Cathode, Advanced Energy Materials n/a (n.d.) 2403360. https://doi.org/10.1002/aenm.202403360. | 카드 없음 (benhadjali2025 에 인용만) — 적층압 ↔ 수송 · 반응 |
| 8 | R. Koerver, W. Zhang, L. de Biasi, S. Schweidler, A.O. Kondrakov, S. Kolling, T. Brezesinski, P. Hartmann, W.G. Zeier, J. Janek, Chemo-mechanical expansion of lithium electrode materials – on the route to mechanically optimized all-solid-state batteries, Energy Environ. Sci. 11 (2018) 2142–2158. https://doi.org/10.1039/C8EE00907D. | 정본 `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` — ΔV (그림 2b 재수록) · 실측 축 응력 |
| 10 | W. Zhang, D. Schröder, T. Arlt, I. Manke, R. Koerver, R. Pinedo, D.A. Weber, J. Sann, W.G. Zeier, J. Janek, (Electro)chemical expansion during cycling: monitoring the pressure changes in operating solid-state lithium batteries, J. Mater. Chem. A 5 (2017) 9929–9936. https://doi.org/10.1039/C7TA02730C. | 카드 없음 — 운전 중 압력 변화 측정 |
| 17 | K.G. Naik, B.S. Vishnugopi, P.P. Mukherjee, Heterogeneities affect solid-state battery cathode dynamics, Energy Storage Materials 55 (2023) 312–321. https://doi.org/10.1016/j.ensm.2022.11.055. | 카드 없음 — 'AM 은 탄성 영역' 가정의 근거로 인용됨 (p.11) |
| 19 | Y. Shao, X. Shao, L. Sang, H. Liu, A Fully Coupled Mechano-Electrochemical Model for All-Solid-State Thin-Film Li-Ion Batteries with Non-Porous Electrodes: Effects of Chemo-Mechanical Expansions on Battery Performance and Optimization Strategies for Stress Evolution, J. Electrochem. Soc. 169 (2022) 080529. https://doi.org/10.1149/1945-7111/ac8b3a. | 카드 없음 — 1D 완전결합 선례 |
| 20 | K. Taghikhani, W. Huber, P.J. Weddle, M. Asle Zaeem, J.R. Berger, R.J. Kee, Modeling coupled electro-chemo-mechanical phenomena within all-solid-state battery composite cathodes, Journal of the Mechanics and Physics of Solids 198 (2025) 106060. https://doi.org/10.1016/j.jmps.2025.106060. | 정본 `taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode` — 2D 완전결합 + 파괴 |
| 21 | C. Yuan, W. Lu, J. Xu, Electrochemical-mechanical coupling failure mechanism of composite cathode in all-solid-state batteries, Energy Storage Materials 60 (2023) 102834. https://doi.org/10.1016/j.ensm.2023.102834. | 카드 없음 — 복합 양극 결합 파손 |
| 23 | N. Iqbal, J. Choi, C. Lee, H.M.U. Ayub, J. Kim, M. Kim, Y. Kim, D. Moon, S. Lee, Effects of Diffusion-Induced Nonlinear Local Volume Change on the Structural Stability of NMC Cathode Materials of Lithium-Ion Batteries, Mathematics 10 (2022) 4697. https://doi.org/10.3390/math10244697. | 카드 없음 — 식 (15)–(16) 원전 |
| 24 | C.P. Schmidt, S. Sinzig, V. Gravemeier, W.A. Wall, A three-dimensional finite element formulation coupling electrochemistry and solid mechanics on resolved microstructures of all-solid-state lithium-ion batteries, Computer Methods in Applied Mechanics and Engineering 417 (2023) 116468. https://doi.org/10.1016/j.cma.2023.116468. | 카드 없음 (benhadjali2025 에 인용만) — ★ 3D 해상 결합 FE (새로움 주장 확인 · 후보 B) |
| 25 | A.M. Boyce, E. Martínez-Pañeda, A. Wade, Y.S. Zhang, J.J. Bailey, T.M.M. Heenan, D.J.L. Brett, P.R. Shearing, Cracking predictions of lithium-ion battery electrodes by X-ray computed tomography and modelling, Journal of Power Sources 526 (2022) 231119. https://doi.org/10.1016/j.jpowsour.2022.231119. | 카드 없음 — 3D 한 방향 선례 (균열) |
| 26 | S. Ben Hadj Ali, M. Alabdali, V. Viallet, V. Seznec, A.A. Franco, A New Three-Dimensional Microstructure-Resolved Model to Assess Mechanical Stress in Solid-State Battery Electrodes, Batteries & Supercaps 9 (2026) e202500540. https://doi.org/10.1002/batt.202500540. | 카드 없음 — ★ 같은 구조 · 한 방향 결합 판 (물성 표 E · ν 가 있을 가능성 · [36] = 프리프린트 판) |
| 27 | M. Alabdali, F.M. Zanotto, M. Duquesnoy, A.-K. Hatz, D. Ma, J. Auvergniot, V. Viallet, V. Seznec, A.A. Franco, Three-dimensional physical modeling of the wet manufacturing process of solid-state battery electrodes, Journal of Power Sources 580 (2023) 233427. https://doi.org/10.1016/j.jpowsour.2023.233427. | 정본 `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` — 미세구조 출처 |
| 29 | S. Ben Hadj Ali, M. Alabdali, V. Viallet, V. Seznec, A.A. Franco, A computational workflow for the simulation of solid state battery electrodes from manufacturing to electrochemical performance, Journal of Power Sources 630 (2025) 236131. https://doi.org/10.1016/j.jpowsour.2024.236131. | 정본 `benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode` — 같은 구조의 전기화학 판 |
| 30 | M. Chouchane, A.A. Franco, Cover Feature: An Invitation to Engage with Computational Modeling: User‐Friendly Tool for In Silico Battery Component Generation and Meshing (Batteries & Supercaps 9/2021), Batteries & Supercaps 4 (2021) 1375–1375. https://doi.org/10.1002/batt.202100202. | 카드 없음 — INNOV (이 줄은 표지 기사 서지 · INNOV 본 논문 = benhadjali2026 카드 ref [38] · Batteries & Supercaps 4 (2021) 1451–1456 · 10.1002/batt.202100096 [다른 카드]) |
| 31 | M. Chouchane, A. Rucci, A.A. Franco, A Versatile and Efficient Voxelization-Based Meshing Algorithm of Multiple Phases, ACS Omega 4 (2019) 11141–11144. https://doi.org/10.1021/acsomega.9b01279. | 카드 없음 (benhadjali2025 · benhadjali2026 에 인용) — 복셀 다상 메싱 (복셀 크기 · 겹침 처리의 열쇠) |
| 34 | X. Zhang, W. Shyy, A.M. Sastry, Numerical Simulation of Intercalation-Induced Stress in Li-Ion Battery Electrode Particles, J. Electrochem. Soc. 154 (2007) A910. https://doi.org/10.1149/1.2759840. | 카드 없음 — 식 (4)–(5) 원전 |
| 35 | K. Takahashi, K. Higa, S. Mair, M. Chintapalli, N. Balsara, V. Srinivasan, Mechanical Degradation of Graphite/PVDF Composite Electrodes: A Model-Experimental Study, J. Electrochem. Soc. 163 (2015) A385. https://doi.org/10.1149/2.0271603jes. | 카드 없음 — 식 (7) 원전 |
| 36 | S.B.H. Ali, M. Alabdali, V. Viallet, V. Seznec, A.A. Franco, A New Three-Dimensional Microstructure-Resolved Model to Assess Mechanical Stress in Solid State Battery Electrodes, (2025). https://doi.org/10.26434/chemrxiv-2025-84s4f. | 카드 없음 — [26] 의 프리프린트 판 (한 방향 결합 비교 대상) |
| 38 | A. Lundkvist, P.-L. Larsson, A.H.S. Iyer, E. Olsson, Discrete element modelling of the elastic-plastic and viscoelastic properties of a lithium-ion battery electrode layer, Powder Technology 443 (2024) 119873. https://doi.org/10.1016/j.powtec.2024.119873. | 카드 없음 (`song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage` 에 인용만) — 전극층 탄소성 · 점탄성 DEM (후보 C′ · 질문 e · k · l) |
| 39 | R. Xu, Y. Yang, F. Yin, P. Liu, P. Cloetens, Y. Liu, F. Lin, K. Zhao, Heterogeneous damage in Li-ion batteries: Experimental analysis and theoretical modeling, Journal of the Mechanics and Physics of Solids 129 (2019) 160–183. https://doi.org/10.1016/j.jmps.2019.05.003. | 카드 없음 — 식 (11)–(12) 인용 |

## 13. [미확인] 목록 (본문 26 쪽 전수에 없음)
- 출판본 서지 (ESM 90 (2026) 105304 · DOI 10.1016/j.ensm.2026.105304) — 이 PDF 는 ChemRxiv v1.
- 물성 전부 (AM · SE · CBD 의 E · ν · 밀도) · Ω · C_total · D_Li · j₀ · OCV 표 · 그림 S1 · 표 S1 · S2 (SI *"XXX"*).
- 실험 양극의 두께 · 질량 · 기공 · 3 t 압축의 다이 지름 · 시간 · 온도 · 토크 → 68 MPa 환산법 · r_p 값 · EIS 면적 A · z.
- 넘긴 구조: 되튐 · 판 분리 · 이완 · 응력 · 복셀 크기 · 요소 종류 · 수 · 메시 수렴 · AM–SE 겹침 규칙 · '10 µm' 가 지름인지 · '기공 12 %' 정의 · 그림 2a 44.6 µm 의 뜻.
- FEM: SE · CBD 의 전하 보존식 · 상 사이 계면 조건 · 기공 영역 역학 · 측벽 '고정 벽' 의 자유도 · 위 경계의 꼴 · 큰 변형 · 형상 갱신 여부 (그림 1 의 iteration) · 시간 간격 · 풀이기 · 실행 시간 · 자유도.
- 결과: 그림 3 비교의 조건 · 'SOC' 정의 · 그림 4b 'Li concentration' 축 정의 · 그림 5c 전단 성분 · 그림 5b 부호 규약 · 사이클 경계 되돌아감과 평평한 최소 구간의 원인 · 그림 4 ↔ 6 이 같은 계산인지.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 26 쪽 글자 층 전수 (PyMuPDF 쪽별 + 블록 좌표) · 저자 · 소속 · 날짜 · DOI · 라이선스 = p.1–2 (렌더로 소속 위첨자 확인 — Franco ᵃ˒ᵇ˒ᶜ˒ᵈ˒ᵉ) · CRediT · 이해상충 = p.22–23 · 연구비 · 감사 · 보충자료 자리표시 = p.23 · 참고문헌 40 개 = p.23–26 · 'GPa' · 'Young' · 'modul' · 'Poisson' · 'mesh' · 'element' · 'availab' · 'unload' · 'release' · 'plastic' · 'contact' · 'Table S' · 'Figure S' · '2D' 전수 검색.
- 식 (1)–(16) = PDF 쪽 렌더 (300 dpi 크롭 · 열람) 로 분수 · 첨자 · 근호 확인 · 식 (6)–(7) 은 (4)–(5) 에서 D · Ω 상수로 유도해 맞춤 [카드 산술] · 그림 1 의 BV 꼴은 패널 크롭으로 확인.
- 그림 6 장 · 패널 13 장 · 식 16 장 · 근거 문단 20 장 전부 열람 · 다시 자름 3.
- 판독 검산: 그림 4b σzz 시작 −78.0 · 최대 35.1 ↔ 인쇄 −78 · 35 ✓ · 그림 4a 최소 −109.4 ↔ −110 ✓ · 그림 4d 시작 −0.70 · 끝 −3.30 · 비가역 0.73 %p ↔ 인쇄 −0.68 · −3.29 · 0.725 ✓ (≤0.02 %p · 0.4 MPa) · 그림 6 · 3 은 인쇄값 없음 (판독만).
- 정본 대조: `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` (§4-3 식 (12)–(24) · EM-01 · EM-06 · §7-1 · L18 · L441–L443) · `benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode` (표 S1 두께 · 기공 · 분율 · 표 S2 c_max · ρ · 겹침 우선순위) · `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` (입자 수 · 건조 두께 · k_n · X_µ · springback n/a) · `koerver2018_…` (그림 2a NCM-622 −4.8 % · 그림 2b V̄ · 표 S3 · 고정 틀 σ₁₁) · `taghikhani2025_…` (2D · LPSC E 22.1 · ν 0.37) · `zhang2026_polymer_electrolyte_modeling_perspective` (L64 · L122).
- 참고문헌 ↔ 정본 카드 DOI 대조 (git grep · 2026-11-12): [8] · [20] · [27] · [29] 정본 카드 있음 · [1] · [21] · [23] · [26] · [31] · [34] · [35] 는 benhadjali2026 카드에 ([31] 은 benhadjali2025 에도) · [7] · [24] 는 benhadjali2025 카드에 · [38] 은 `song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage` 에 · [9] 는 kalnaus2023 카드에 인용만 · 나머지 (40 개 중) 없음.
- 정본 중복 확인: `litdb/papers/` 파일 목록 + `105304` · `ensm.2026.105304` · `chemrxiv.15001135` · `Fully coupled mechano` · `Valisammagari` grep → 이 논문 카드 없음 (benhadjali2026 L443 · zhang2026 L122 인용만) · 같은 제1 저자 카드 둘 (benhadjali2025 · benhadjali2026) = 다른 논문.
- 인용 서지는 PDF 목록 글자 그대로 (줄바꿈 하이픈만 복원) · [37] 은 표에 넣지 않음 (MathML 조각).

## 🔗 관련 카드
- **같은 제1 저자 · 같은 사슬**: `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` (같은 해 · 이 논문의 FEM 식을 그대로 다시 쓰고 WIP ↔ CUP 실험을 붙인 다음 편 · 이 논문 = 그 카드 ref [31]) · `benhadjali2025_cgmd_calendering_to_3d_electrochemistry_assb_cathode` (같은 구조의 전기화학만 판 · ref [29]) · `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` (구조 출처 · ref [27]) · `ngandjong2021_dem_calendering_digital_twin` · `xu2023_realistic_am_shape_cgmd_calendering` · `qin2026_bilayer_cathode_cgmd_dem_graded_thick_electrode` · `sankar2026_fiber_scale_dem_carbon_felt_manufacturing` (Valisammagari 공저) · `dem_mechanical_stresses_ssb_electrode_cycling` (같은 그룹 LIGGGHTS 사이클 응력 · 이 논문은 인용하지 않음).
- **사이클 응력 · 기계-전기화학**: `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` (ΔV 원 · 실측 축 응력) · `taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode` (2D 완전결합 + phase-field · ref [20]) · `bucci2017_chemomech_failure_assb_cycling_czm` (CZM 계면) · `park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics` (XCT 2D 선형 탄성 확산 변형 응력) · `cronk2026_lis_positive_electrode_geometry_fem` (COMSOL 선형 탄성 · 등방 고유변형) · `kalnaus2023_ssb_critical_role_of_mechanics_stress_relief_review` · `kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review` · `so2021_dem_fabrication_degradation_ductile_particles` · `wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn`.
- **이 논문을 인용한 카드**: `zhang2026_polymer_electrolyte_modeling_perspective` (ref 164).
- **같은 제1 저자 · 같은 해 (2026-11-12 카드)**: [`benhadjali2026_oneway_chemomech_stress_stack_pressure_3d_assb_cathode`](benhadjali2026_oneway_chemomech_stress_stack_pressure_3d_assb_cathode.md) — 참고 [26] (출판본) · [36] (ChemRxiv 판) 의 원문 (한 방향 결합 · AM = NMC811 ≈7 % · 적층압 9 ↔ 68 MPa · C/5–C/20 방전 한 번 · 물성 = SI 표 S2: SE E 18.5 GPa · ν 0.3 (Li₂S–P₂S₅ 유리 원전) · NMC811 175 GPa · CBD 0.35 GPa · ν 0.4) — AM · 적층압 · 사이클 조건이 이 논문 (NMC622 · 68 MPa · C/10 5 사이클) 과 다르다.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
