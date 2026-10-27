<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps.md.
     쪽 표기 = 학술지 쪽 "p.N" = 154901-N (PDF 쪽 = N + 1 — PDF 1 쪽은 AIP 표지 · "Articles You May Be Interested In").
     SI 없음 — 원문에 보충자료 언급이 없고, 부록 (p.9) 이 표 I–III 을 "complete dataset and source data for figures" 라고 부른다 · 원자료는 교신저자 요청 (p.9).
     값 표지: [인쇄] = 본문 · 표 · 그림 안에 숫자로 적힌 값 · [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv — 그림 8 안 인쇄 숫자 48 개) ·
     [우리 산술] = 인쇄값으로 우리가 다시 한 계산 — 독립 복셀 FV 재현 포함 (litdb/figures/<slug>/ours_voxel_fv_reproduction.csv) · [추정] = 우리 해석 · 가정이 든 어림 (가정을 그 자리에 적음) ·
     [미확인] = 원문 (본문 12 쪽 + 표지 전수) 에 없음.
     원문 13 쪽 텍스트 층 전수 + 그림 8 · 표 3 · 식 6 = 크롭 17 장 전부 렌더로 열람.  표 I–III 은 칸마다 렌더 · 텍스트 층과 대조 (source_data_tables.csv · 27 행 전부 일치) ·
     τ = ε/κ̄ 를 표 값으로 전부 다시 계산 · 그림 8 안 숫자 48 개를 표 II 로 다시 계산 · 표 I · II 의 κ̄ 를 우리 복셀 FV 로 다시 풀었다 (§7-3). -->

# 자이로이드 (gyroid) 구조 전해질의 미세구조 해상 (microstructure-resolved) FEM 주기 단위셀 균질화 — 공극률 0.2 → 0.9 에서 정규화 강성 0.599 → 0.0328 (×1/18) · 이온전도 0.0872 → 0.574 (×6.6) · 공극률 60 % 고정에서 축 늘림 (a:b:c) 만으로 강성 방향차 최대 ×28 · 전도 ×5 · 원문 'tortuosity' τ = ε/κ̄ = 우리 수송 tortuosity (tau2) · 우리 복셀 FV 재현 = 시트형 고체에서만 표 I ±1.1 % — Tianyang Zhou · Cesar Metlich · Landon C. Riley · Dimitris C. Lagoudas (Texas A&M · San José State, J. Appl. Phys. 2026)

> slug `zhou2026_gyroid_structural_electrolyte_stiffness_ionic_tradeoff` · DOI `10.1063/5.0341375` · type `FEM (COMSOL periodic unit-cell homogenization · linear elastic C_eff on the solid + steady ionic conduction κ_eff on the liquid of designed gyroid microstructures; continuum; idealized geometry; no particles · no DEM · no MPM · no experiment)` · PDF `a46c93b2-3._Microstructure-resolved_modeling_of_gyroid_structural_electrolytes_Mechanical_and_transport_behavior.pdf` · digested `2026-10-27` · status ✅
>
> **원제**: *Microstructure-resolved modeling of gyroid structural electrolytes: Mechanical and transport behavior* (p.1)
> **저자 · 소속 (p.1)**: **Tianyang Zhou\*** (1, 2) · Cesar Metlich (1) · Landon C. Riley (1) · Dimitris C. Lagoudas (1) — (1) Department of Aerospace Engineering, **Texas A&M University**, College Station, Texas 77843, USA · (2) Department of Aerospace Engineering, **San José State University**, San Jose, California 95192, USA (\* 교신 tianyang.zhou@sjsu.edu)
> *J. Appl. Phys.* **140**, 154901 (2026) · 접수 2026-04-30 · 승인 2026-09-25 · 온라인 2026-10-15 (p.1) · Special Topic *"Advances in Applied Mechanics and Applied Physics from the 2025 SES Annual Technical Meeting"* (p.1) · 연구비 AFOSR FA9550-25-1-0312 · FA9550-22-1-0388 (p.9) · 이해상충 없음 (p.9) · 데이터 = 교신저자 요청 (p.9).
> **같은 축 카드 (링크만)**: [`bazzoun2026_dem_fem_rnm_ionic`](bazzoun2026_dem_fem_rnm_ionic.md) (같은 DEM 구조를 연속체 FEM ↔ 접촉망 RNM 으로 — 연속체 수송의 우리 쪽 대조) · [`lee2026_unveiling_ptfe_dry_electrode_digital_twin`](lee2026_unveiling_ptfe_dry_electrode_digital_twin.md) (실구조 FV σ 로 tau2) · [`tjaden2018_tortuosity_review_calculation_approaches`](tjaden2018_tortuosity_review_calculation_approaches.md) (τ 정의) · [`taufactor_tortuosity_factor_tomography_tool`](taufactor_tortuosity_factor_tomography_tool.md) (복셀 FV tau2 — 우리 재현과 같은 부류) · [`ender2011_3d_reconstruction_composite_cathode`](ender2011_3d_reconstruction_composite_cathode.md) · [`hlushkou2018_void_space_ion_transport_assb_cathode`](hlushkou2018_void_space_ion_transport_assb_cathode.md) (연속체 tau2 ≥ 1) · [`song2025_porous_argyrodite_modulus_fracture_toughness`](song2025_porous_argyrodite_modulus_fracture_toughness.md) (다공 LPSCl 펠릿 E — §8-6 의 역학 대조).
> **원자료 · 판독 · 재현**: `litdb/figures/zhou2026_gyroid_structural_electrolyte_stiffness_ionic_tradeoff/` — `source_data_tables.csv` (표 I–III 전사 [인쇄]) · `digitized.csv` (그림 8 안 숫자 [판독] ↔ 표 II 재계산) · `ours_voxel_fv_reproduction.csv` (우리 독립 복셀 FV — **논문 값 아님**) · 크롭 17 장 `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 식 (1) 의 자이로이드 등위면으로 만든 **이상화된 이중연속 (bicontinuous) 단위셀** 하나에 대해, 고체 골격 (인쇄 고분자 대표값 E_s 3 GPa · ν_s 0.3) 에는 선형 탄성을, 액체 상 (1 M LiTFSI · 디글라임/FEC · κ_l 3.53 × 10⁻³ S/cm) 에는 정상 이온 전도를 **따로** 풀어 (COMSOL 주기 균질화) 정규화 유효 물성 Ē · κ̄ · τ 를 낸 순수 계산 논문 — 공극률을 0.2 → 0.9 로 올리면 **강성은 ×1/18, 전도는 ×6.6** (서로 반대) 이고, 공극률 60 % 에서 셀을 한 축으로 늘리면 (a:b:c) **그 축은 강성 · 전도가 함께 오르고 가로 축은 함께 내린다** — 방향차는 강성 (E_max/E_min 최대 20.5) 이 전도 (κ_max/κ_min 최대 4.0) 보다 훨씬 크다 (p.5–8 · 표 I–II).  실험 검증은 없다 (저자 명시 "geometry-controlled prediction", p.6).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 무엇을 어떻게 풀었나 | MATLAB 으로 식 (1) 등위면 → STL → COMSOL Multiphysics · **완전한 주기 단위셀 1 개** · 주기 경계 · 역학 = 6 단위 거시 변형 → C_eff → S_eff = C_eff⁻¹ → E_i = 1/S_ii · 수송 = x · y · z 단위 전위 기울기 3 개 → κ_eff 대각 · 고체–액체 경계는 역학 무견인 · 수송 절연 (i·n = 0) · 각 상 등방 · 두 문제 비결합 | [인쇄] p.3–5 · 식 (1)–(18) |
| ② ★ 원문 'tortuosity' 는 우리 어느 τ 인가 | **τ_i = ε/κ̄_i** (식 19) · κ̄ 는 액체 적분 ÷ **셀 전체 부피** (식 16–18) ⇒ κ̄ = 우리 **f** · τ = φ/f = 우리 **tau2 = 수송 tortuosity (제곱근 아님)** · 원문은 'factor' 를 붙이지 않고 "path complexity" 로 읽는다 · 표 값으로 ε/κ̄ 재계산 = 인쇄 τ 와 최대 0.006 (표 I) · 0.014 (표 II) 차 = 반올림 | [인쇄] p.4–6 · [우리 산술] |
| ③ 공극률 ↔ 강성 ↔ 전도 (1:1:1) | ε 0.20 → 0.90: Ē **0.599 → 0.0328** · κ̄ **0.0872 → 0.574** · τ **2.29 → 1.57** · 차원값 1.80 → 0.0984 GPa · 3.08 × 10⁻⁴ → 2.03 × 10⁻³ S/cm | [인쇄] p.5–6 · 표 I · 그림 3 |
| ④ 이방성 (ε 0.60) | Ē 0.0125–0.348 (**×28** = Ē_x(4:1:1)/Ē_z(4:4:1)) · κ̄ 0.105–0.559 (**×5.3**) · τ 1.07–5.70 · E_max/E_min 2.3 → 20.5 ↔ κ_max/κ_min 2.0 → 4.0 · 방향 평균 Ē 0.164–0.175 (거의 보존) ↔ κ̄ 0.297–0.324 (3–11 % 하락) | [인쇄] 표 II · 그림 4–8 · [우리 산술] |
| ⑤ ★ 우리 STEP3 부류 복셀 FV 로 다시 풀면 | **시트형 고체 (−s ≤ F ≤ s)** 로 풀면 표 I 8 점이 **−0.3 … +1.1 %**, 표 II 18 점이 **0.0 … +2.1 %** (N 64 · 128 · 1 차 Richardson) · **네트워크형 (F ≥ t)** 은 **+15 … +45 %** ⇒ 원문 고체 = 시트형 (원문 미기재) · 해상도 오차 N 64 = −3.5 … −8.5 % (d_h/dx 9.4 … 3.3) ≈ **−0.28/(d_h/dx)** | [우리 산술] §7-3 |
| ⑥ ★ 우리 접촉망 (ps45) 수송 tortuosity 와 | φ ≈ 0.3 의 매끈한 연속 채널: tau2 **2.14** (시트 · 원문 표 I) · **≈1.80** (네트워크 · 우리 재현) · 등방 연속체 하한 (3−φ)/2 = **1.35** ↔ ps45 Hertz FULL **5.03–7.24** (= 2.4–4.0 배) · CF (협착 뺀 같은 망) **1.25–1.79** — 7:3 (1.282) · 10:0 (1.247) 은 등방 연속체 하한 아래 | [우리 산술 · 추정 — 기하 다름] §7-4 |
| ⑦ 역학 (MPM 쪽) | 선형 탄성 균질화 C_eff (6 단위 변형) = **우리에게 없는 능력** · E ∝ ρⁿ 국소 n 1.12 (ρ 0.1–0.2) → 2.04 (ρ 0.7–0.8) = 시트 TPMS 꼴 · (1:1:1) 탄성 거의 등방 (A 1.06–1.15) · 소성 · 압밀 · 접촉 · 파괴 없음 | [우리 산술] §3-4 · §7-5 |
| ⑧ 실험 · 보정 | **없음** — 재료값은 "dimensional reference" (p.5) · 실험 검증 = 향후 (방향별 기계 시험 + 차단 전극 임피던스, p.8) ⇒ frame [4] 앵커가 못 된다 · 대신 **해법 검증 (verification) 표적** | [인쇄] p.5–8 |

⛔ **한정어 (떼지 말 것)**: ① 소재 = 인쇄 고분자 대표값 (PLA · FFF, E_s 3 GPa · ν_s 0.3) + **액체** 전해질 — 황화물 SE · 입자 · 접촉 · 계면 저항 **없음** ② **이상화된 매끈한 TPMS** — 인쇄 해상도 · 거칠기 · 층간 계면 · 결함 · 불완전 침투 미반영 (저자 명시 p.6 · p.8) ③ 선형 탄성 · 균일 농도 극한 (농도 구배 없음) → 정규화 값은 **절대 크기와 무관** (채널 크기 효과 없음, p.5) ④ 실험 없음 ⑤ 주기 단위셀 하나 (전극 두께 · 집전체 경계 없음) ⑥ **고체가 등위면의 어느 쪽인지 원문 미기재** — 우리 재현이 시트형으로 판정 (§7-3, [우리 산술]) ⑦ 메시 · 요소 · 수렴 정보 없음 ⑧ 역학 ↔ 수송 비결합 (응력 보조 전해질 재분배 미고려, p.3) ⑨ 원문 τ = **tau2** — √ 로 읽지 않는다.

---

## 1. 한 줄 요약

구조 배터리 (structural battery) 의 전해질은 하중을 견디는 강성과 이온 수송을 함께 요구하는데, 지금까지는 주로 **고체/액체 조성** (PIPS 같은 상분리 이중연속 구조) 으로 그 균형을 잡아 왔다.  이 논문은 적층 제조 (additive manufacturing) 로 만들 수 있는 **설계된 기하** — 자이로이드 이중연속 단위셀과 그 축 늘림 (a:b:c) — 를 두 번째 손잡이로 제시하고, 고체 골격에 선형 탄성 · 액체 상에 정상 전도를 주기 균질화로 풀어 (COMSOL), **공극률은 강성과 전도를 반대로 (trade-off), 기하 이방성은 한 축에서 둘을 같이 올리고 가로 축에서 같이 내린다 (재분배)** 는 것과, 이방성의 효과가 강성에서 훨씬 크다 (E 방향차 ×20.5 ↔ κ ×4.0) 는 것을 표 세 장 (부록 = 그림의 원자료) 으로 보인다 (그림 3–8).

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **T. Zhou\*** · C. Metlich · L. C. Riley · D. C. Lagoudas (Texas A&M 항공우주 · San José State 항공우주) | *J. Appl. Phys.* 140, 154901 (2026) · Special Topic (2025 SES) | 10.1063/5.0341375 | **고체** = 인쇄 고분자 대표값 E_s 3 GPa · ν_s 0.3 (PLA · FFF 문헌 [61]) · **액체** = 1 M LiTFSI in 디글라임 90 wt% + FEC 10 wt%, κ_l 3.53 × 10⁻³ S/cm (실온 · 문헌 [5]) — 특정 고분자–전해질 짝이 아님 (p.5) | FEM 주기 단위셀 균질화 (역학 + 수송 따로) · 설계 기하 매개 연구 (공극률 8 수준 · 이방성 6 수준) · **실험 없음** |

- 키워드 · 주제: structural battery electrolyte · TPMS (triply periodic minimal surface) · additive manufacturing · stiffness–conductivity trade-off.
- 같은 그룹 선행: [60] Zhou 2026 (Springer 책 장 — 저온 SBE 의 미세구조 의존 E · κ 모델링) · [3] · [4] (다기능 효율 지표) · [10] · [11] (탄소섬유 전극 손상).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 모형 입력 · 설정 (p.3–5)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 기하 | **식 (1)** sin(2πx/a)cos(2πy/b) + sin(2πy/b)cos(2πz/c) + sin(2πz/c)cos(2πx/a) − t = 0 · a = b = c 이면 보통 자이로이드 · t = 부피분율 조절 (이 문장에 Maskery 2018 [48] 인용) · a:b:c = 기하 이방성 표기 | [인쇄] p.3 · eq_1.png |
| 고체 / 액체 | MATLAB → STL (고체) → COMSOL · 액체 = 직육면체 − 고체 (그림 2) · **공극률 = 액체 부피분율** · 고체가 등위면의 어느 쪽인지 (F ≥ t 한쪽 = 네트워크형 / −s ≤ F ≤ s 막 = 시트형) **[미확인]** → 우리 재현 = 시트형 (§7-3) | [인쇄] p.3 · [우리 산술] |
| 역학 지배식 | ∇·σ = 0 in Ω_s · σ = ℂ_s : ε · ε = ½[∇u + (∇u)ᵀ] (식 2–4) · u = ε_avg X + u\* (식 5) · 주기 조건 u_dst − u_src = ε_avg (X_dst − X_src) (식 6) · σ_avg = (1/V_cell) ∫_Ωs σ dV (식 7 — 액체는 응력 0) · Voigt 6 성분 (식 8) · 단위 변형 6 경우 → C_eff 6 열 (식 9) · S_eff = C_eff⁻¹ (식 10) · **E_i = 1/S_ii** (식 11) · G = 전단 순응 항 · ν = 비대각 순응 항 (표 III 주) | [인쇄] p.3–4 · p.10 |
| 수송 지배식 | **i = −κ_l ∇ϕ** (식 12) · ∇·i = 0 in Ω_l (식 13) · 고체 = 이온전도 0 · 수송 영역에서 제외 · 경계 i·n = 0 · ϕ = (∇ϕ)_avg·X + ϕ\* (식 14) · 주기 조건 (식 15) · **i_avg = (1/V_cell) ∫_Ωl i dV** (식 16) · i_avg = −κ_eff (∇ϕ)_avg (식 17) · 보고값 = κ_eff 대각 · 전위 기준점 하나 고정 | [인쇄] p.4 · eq_12 · 16 · 17 |
| 가정 | 균일 전해질 조성 · 일정 κ_l · 염 농도 구배 무시 · 정상 상태 = "uniform concentration limit" (농도 구배를 넣으면 시간 · 전류 · 크기 의존이 생긴다 — 범위 밖) · 각 상 등방 · 응력 ↔ 전해질 재분배 결합 미고려 | [인쇄] p.3 · p.5 |
| 정규화 | **Ē_i = E_i^eff/E_s · κ̄_i = κ_i^eff/κ_l** (식 18) · Ḡ = G_eff/G_s, G_s = E_s/(2(1+ν_s)) (표 III 주) · 선형이라 차원값은 E_s · κ_l 에 비례 — 단 역학 정규화 응답은 ν_s 에 의존 (p.5) | [인쇄] p.5 · p.10 |
| 재료값 | κ_l = **3.53 × 10⁻³ S/cm** (1 M LiTFSI · 디글라임 90 wt% + FEC 10 wt% · 실온 · [5]) · E_s = **3 GPa** · ν_s = **0.3** (인쇄 PLA 대표값 · [61]) — "dimensional reference" · 실제 예측에는 인쇄 · 전해질 노출 뒤 측정값이 필요 | [인쇄] p.5 |
| 영역 · 경계 | **완전한 주기 단위셀 1 개** · 대응면 주기 경계 — 선형 문제에서 반복 셀을 더 넣어도 정보가 늘지 않는다 · 균일 변위/견인 경계는 셀 수에 의존하고 셀이 늘면 주기 결과로 수렴 (p.5) · 균일 크기 변경에 정규화 값 불변 = **절대 기공 · 채널 크기 효과 없음** (얇은 벽의 인쇄 결함 · 작은 채널의 크기 의존 수송은 범위 밖, p.5) | [인쇄] p.5 |
| 메시 | 요소 종류 · 크기 · 수렴 시험 **[미확인]** · "Small differences between symmetry-equivalent directions arise from STL geometry import and finite element meshing" (표 III 주) | [인쇄] p.10 |
| 연구 설계 | **공극률 연구**: (1:1:1) · ε = 0.2, 0.3, …, 0.9 (중간 범위 = 상용 LIB 고분자 분리막 공극률 [63]) · **이방성 연구**: ε = 0.60 · (1:1:1) · (2:1:1) · (2:2:1) · (4:1:1) · (4:2:1) · (4:4:1) | [인쇄] p.5 |

### 3-2. ★ 공극률 연구 — 표 I (1:1:1) [인쇄] + 우리 산술

| ε | Ē [인쇄] | κ̄ = f [인쇄] | τ [인쇄] | ε/κ̄ [우리 산술] | 등방 HS 하한 (3−ε)/2 [우리 산술] | Bruggeman ε^−½ [우리 산술] | Archie m = ln κ̄ / ln ε [우리 산술] | Ē/(1−ε) [우리 산술] | 국소 n (Ē ∝ (1−ε)ⁿ) [우리 산술] |
|---|---|---|---|---|---|---|---|---|---|
| 0.90 | 0.0328 | 0.574 | 1.57 | 1.568 | 1.050 | 1.054 | 5.27 | 0.328 | — |
| 0.80 | 0.0712 | 0.487 | 1.64 | 1.643 | 1.100 | 1.118 | 3.22 | 0.356 | 1.12 |
| 0.70 | 0.118 | 0.406 | 1.72 | 1.724 | 1.150 | 1.195 | 2.53 | 0.393 | 1.25 |
| 0.60 | 0.176 | 0.332 | 1.81 | 1.807 | 1.200 | 1.291 | 2.16 | 0.440 | 1.39 |
| 0.50 | 0.249 | 0.264 | 1.90 | 1.894 | 1.250 | 1.414 | 1.92 | 0.498 | 1.55 |
| 0.40 | 0.340 | 0.199 | 2.01 | 2.010 | 1.300 | 1.581 | 1.76 | 0.567 | 1.71 |
| 0.30 | 0.456 | 0.140 | 2.14 | 2.143 | 1.350 | 1.826 | 1.63 | 0.651 | 1.90 |
| 0.20 | 0.599 | 0.0872 | 2.29 | 2.294 | 1.400 | 2.236 | 1.52 | 0.749 | 2.04 |

- 원문 서술 (p.5): 20 → 90 % 에서 정규화 강성 ≈95 % 감소 (우리 산술 94.5 %) · 전도 ≈7 배 (6.58) · τ 2.29 → 1.57 — *"porosity modifies the transport pathways directly beyond the proportional porosity contribution"*.
- [우리 산술] **등방 연속체 상한을 지킨다**: (1:1:1) 은 입방 대칭이라 전도 텐서가 등방 → Hashin–Shtrikman 상한 κ̄ ≤ 2ε/(3−ε) (절연 2 상) · 즉 tau2 ≥ (3−ε)/2 — 8 점 모두 위.  Wiener 하한 tau2 ≥ 1 도 당연히 위.
- [우리 산술] **Bruggeman · Archie 꼴이 아니다**: ε 0.2 에서는 Bruggeman (2.24) 과 거의 같지만 ε 0.9 에서 1.57 ↔ 1.05 — 겉보기 Archie 지수가 1.52 → 5.27 로 흐른다.  [추정] 시트형 고체면 두 액체 미로를 가르는 벽이 얇아져도 남아 tau2 가 1 로 안 간다 (벽 두께 → 0 이어도 절연 막이 전류를 미로로만 보낸다) — §7-3 판정과 같은 그림.
- [우리 산술] 강성 국소 지수 n 이 저밀도 1.12 → 고밀도 2.04 — 저밀도에서 거의 선형 (Ē ≈ 0.33 ρ) = 굽힘 지배 (n ≈ 2) 가 아니라 늘림 (stretching) 지배에 가까운 시트형 TPMS 꼴 [추정 — 역학 쪽 시트 판정의 두 번째 근거].

### 3-3. ★ 이방성 연구 — 표 II (ε 0.60) [인쇄] + 그림 8 [판독] + 우리 산술

| a:b:c | Ē_x | Ē_y | Ē_z | κ̄_x | κ̄_y | κ̄_z | τ_x | τ_y | τ_z | E_max/E_min (그림 8) | κ_max/κ_min (그림 8) | 방향 평균 Ē [우리 산술] | 방향 평균 κ̄ [우리 산술] | 조화 평균 κ̄ [우리 산술] |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (1:1:1) | 0.176 | 0.176 | 0.176 | 0.332 | 0.332 | 0.332 | 1.81 | 1.81 | 1.81 | 1.0 | 1.0 | 0.176 | 0.332 | 0.332 |
| (2:1:1) | 0.275 | 0.117 | 0.117 | 0.480 | 0.241 | 0.241 | 1.25 | 2.49 | 2.49 | 2.3 | 2.0 | 0.170 | 0.321 | 0.289 |
| (2:2:1) | 0.222 | 0.222 | 0.0676 | 0.392 | 0.392 | 0.189 | 1.53 | 1.53 | 3.18 | 3.3 | 2.1 | 0.171 | 0.324 | 0.289 |
| (4:1:1) | 0.348 | 0.0714 | 0.0714 | 0.559 | 0.166 | 0.166 | 1.07 | 3.62 | 3.62 | 4.9 | 3.4 | 0.164 | 0.297 | 0.217 |
| (4:2:1) | 0.312 | 0.159 | 0.0339 | 0.517 | 0.273 | 0.135 | 1.16 | 2.20 | 4.44 | 9.2 | 3.8 | 0.168 | 0.308 | 0.231 |
| (4:4:1) | 0.256 | 0.256 | 0.0125 | 0.417 | 0.417 | 0.105 | 1.44 | 1.44 | 5.70 | 20.5 | 4.0 | 0.175 | 0.313 | 0.210 |

- 원문 서술 (p.6–8): (4:1:1) 이 x 강성 최고 (0.348) · 가로 축은 크게 줄어 "redistribution rather than an absolute increase in load-bearing capacity" (p.7) · 강성 방향차 최대 ×28 (Ē_x(4:1:1) ↔ Ē_z(4:4:1)) · 전도 ≈×5 (κ̄_x(4:1:1) ↔ κ̄_z(4:4:1), 우리 산술 5.32) · 둘 다 **늘림이 커질수록 이득이 줄어든다** (diminishing returns, p.7) · E_max/E_min 2.3 → 20.5 ↔ κ_max/κ_min 2.00 → 4.0 (p.8) · 60 % 차원값 Ē 0.0125–0.348 → **0.0375–1.044 GPa** · κ̄ 0.105–0.559 → **3.71 × 10⁻⁴–1.97 × 10⁻³ S/cm** (p.8).
- 그림 8 열지도 (각 방향 값 ÷ (1:1:1) 값) 36 칸 · 막대 12 개 = 표 II 의 반올림 전 값 (±0.01 · `digitized.csv`) · (2:1:1) E 비 2.3 은 표 값 비 2.35 의 반올림 칼날 · (4:1:1) Ē_y 0.41× ↔ Ē_z 0.40× · (2:1:1) κ̄_y 0.72× ↔ κ̄_z 0.73× 처럼 대칭 방향이 갈리는 것은 표 III 주의 메시 잡음.
- [우리 산술] **방향 평균**: 이방성은 방향 평균 Ē 를 거의 보존하고 (0.164–0.175 ↔ 0.176, −7 … −1 %) 방향 평균 κ̄ 는 조금 (0.297–0.324, −11 … −2 %), 조화 평균 κ̄ 는 많이 (0.210–0.289, −37 … −13 %) 내린다 — 가로 방향 손실이 커서.
- [우리 산술] **방향별 점은 한 직선 위**: 그림 7 의 18 점이 **Ē ≈ −0.057 + 0.720 κ̄ (R² 0.991)** — 같은 공극률에서 기하 이방성은 한 방향의 강성과 전도를 **같이** 움직인다.  ⇒ "trade-off" 는 물성 사이가 아니라 **방향 사이** (원문도 "directional trade-off", p.8).  물성 사이 trade-off 는 공극률 (표 I) 의 몫.

### 3-4. 탄성 상수 더 — 표 III [인쇄] + 우리 산술

- (1:1:1): Ḡ 0.0342 (ε 0.9) → 0.644 (ε 0.2) · ν 0.329 (ε 0.9) → 0.277 (ε 0.3, 최소) → 0.278–0.279 (ε 0.2) · ε 0.5 에서 ν_xy 0.288 ↔ ν_xz · ν_yz 0.287 · ε 0.2 에서 ν_yz 0.279 = 메시 잡음 (표 III 주).
- 이방성 (ε 0.6): Ḡ 최저 = (4:4:1) 의 Ḡ_yz · Ḡ_xz 0.101 · ν_xz 1.434 · ν_yz 1.435 ((4:4:1)) · ν_xz 0.782 ((4:2:1)).
- [우리 산술] (1:1:1) 입방 이방성 계수 A = 2(1+ν)G/E = **1.06–1.15** (A = 1 이면 등방) — 자이로이드의 알려진 거의 등방 탄성과 맞다.
- [우리 산술] **ν > 0.5 는 오류가 아니다**: (4:4:1) 에서 ν_zx = ν_xz·E_z/E_x = 0.070 · 정치성 판정식 1 − ν_xyν_yx − ν_yzν_zy − ν_zxν_xz − 2ν_yxν_zyν_xz = **0.686 > 0** — 이방 재료에서 허용되는 값.

### 3-5. 문헌 비교 · 배경 수치 (2 차 인용 — 원문이 인용한 값)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| ★ 재구성 PIPS 구조 전해질 (Duan 2023 [6]) | 액체 부피분율 ≈37–38 % · 고분자 벌크 강성의 ≈28 % · 액체 전도의 ≈3 % ↔ 자이로이드 ε 0.4: Ē 0.340 · κ̄ 0.199 · [우리 산술 — 원문 근사값] PIPS tau2 ≈ 0.375/0.03 ≈ **12.5** ↔ 자이로이드 **2.01** (≈6 배) · 저자: "smooth and fully connected transport pathways" 의 차 · 실험 검증된 개선이 아니라 기하 통제 예측 | [인쇄] p.6 · [우리 산술] |
| SBE 실험 (PIPS) [26] | 유효 탄성계수 ≈400–600 MPa · 유효 이온전도 ≈10⁻⁴ S/cm | [인쇄] p.2 |
| Zekoll 2018 [58] (자이로이드 · 다이아몬드 · 스피노달 세라믹–고분자 혼성 전해질) | 자이로이드가 최선 — 압축 파괴 변형 +28 % · 굽힘 파괴 변형 최대 5 배 (순수 세라믹 대비) · 이온전도는 세라믹 부피분율에 거의 비례해 감소 | [인쇄] p.2 |
| 이온액체 전해질 | 열안정 200–500 °C · 1–20 × 10⁻³ S/cm [13,14] · Brutti 2020 [15] LiTFSI IL 5.97 × 10⁻³ (20 °C) · 1.28 × 10⁻² S/cm (50 °C) | [인쇄] p.1 |
| 고분자 전해질 · 이오노겔 | PEO 계 10⁻⁸–10⁻⁷ S/cm (≈65 °C 아래) [20] · 이오노겔 10⁻⁴–10⁻³ S/cm — 5.5 × 10⁻⁴ S/cm · 연신 427 % [21] · LLZO 혼성 1.93 × 10⁻³ S/cm (20 °C) [24] · Melodia 2023 [45] (PIMS–DLP): 저장 전단 탄성률 > 400 MPa · 최대 1.2 × 10⁻³ S/cm (30 °C) · Su 2024 [53] 자이로이드 액정 준고체 전해질 Zn 전지 2500 회 90.9 % (1 A g⁻¹) | [인쇄] p.1–2 |

---

## 4. ★ 방법 — 계산 사슬 · 입자 처리

### 4-1. 계산 사슬
식 (1) 등위면 (MATLAB) → 고체 STL (그림 1) · 액체 = 직육면체 − 고체 (그림 2) → COMSOL Multiphysics → ① 고체 영역 선형 탄성 주기 균질화 (단위 변형 6 경우 → C_eff → S_eff → E_i · G_ij · ν_ij) ② 액체 영역 정상 전도 주기 균질화 (단위 기울기 3 경우 → κ_eff 대각) → 정규화 (식 18) → τ_i = ε/κ̄_i (식 19) → 표 I–III · 그림 3–8 (방향 막대 · E–κ 지도 · 이방성 비 · 열지도).  두 문제는 **같은 기하 · 다른 상** 위에서 독립 (p.3).

### 4-2. ★ 입자 처리 (우리 축 언어로)
- **입자 없음** — 연속체 두 상 (고체 골격 · 액체) 의 설계 기하.  DEM 의 접촉망도, MPM 의 소성 흐름도 없다.
- 고체 = **선형 탄성** (작은 변형) · 소성 · 손상 · 파괴 없음 · 액체 = 응력 0.
- 수송 = 액체 한 상의 **연속 전도** — 고체–액체 경계 절연 · 같은 상 안의 계면 (입자 경계) 이 **없다** → 우리 STEP3 와 같은 "CONTACT_FREE" 부류 (접촉 협착 항이 정의상 0) 이고, 이 기하에서는 그것이 **정확한 물리**다 (막힘 없는 연속 액체).
- 이방성 = 셀의 **아핀 늘림** (a:b:c) — 위상 그대로, 부피분율 그대로 (p.3).
- [우리 산술] 고체 정의: 시트형 (두 등위면 사이 막) 이라야 표 I 이 재현된다 (§7-3).

### 4-3. 기법 미니 용어집
- **TPMS (triply periodic minimal surface)**: 세 방향 주기 · 평균곡률 0 인 곡면.  자이로이드는 그 대표 (Schoen G).  식 (1) 은 그 삼각함수 근사 ("nodal approximation") — 우리 계산에서 F = 0 면적 3.091 / 단위셀 (흔히 인용되는 ≈3.09 와 같음 — 출처 카드 없음 [미확인]).
- **네트워크형 vs 시트형 TPMS**: 네트워크형 = 한 등위면의 한쪽 (F ≥ t) 을 고체로 → 고체 · 액체 둘 다 미로 한 덩어리 · 시트형 = 두 등위면 사이 막 (−s ≤ F ≤ s) 을 고체로 → 액체가 **서로 떨어진 두 미로**.  시트형은 같은 밀도에서 더 뻣뻣하고 (늘림 지배), 막이 액체를 갈라 tau2 가 1 로 안 간다.
- **주기 균질화 (periodic homogenization)**: 단위셀에 평균 변형 (또는 평균 기울기) + 주기 요동을 주고 부피 평균 응력 (전류) 으로 유효 텐서를 읽는 법.  균일 변위 · 견인 경계보다 셀 수 의존이 없다 (p.5).
- **Voigt 표기 · 순응 (compliance)**: 6 성분 벡터 응력 · 변형 · S = C⁻¹ · E_i = 1/S_ii · 이방 재료에서는 ν_ij 가 0.5 를 넘을 수 있다.
- **Wiener · Hashin–Shtrikman 경계**: 절연 상이 섞인 2 상 매질에서 f = κ̄ ≤ ε (Wiener — 방향 무관) · 통계적 등방이면 κ̄ ≤ 2ε/(3−ε) (HS) ⇒ tau2 ≥ 1 · tau2 ≥ (3−ε)/2.  [우리 산술 — 표준 식 · 원문에 없음]
- **tortuosity factor (= tau2)**: φσ₀/σ_eff.  원문의 τ 가 이것 (식 19) — √ 를 취하지 않는다 (우리 τ 규약).
- **d_h = V_liquid/S_interface**: 부피 ÷ 계면 넓이 (원기둥이면 지름/4).  우리 MPM 해상도 규칙 (d_h/dx) 과 같은 꼴 [우리 산술 — §7-3 의 해상도 오차 표기에만 씀].

---

## 5. Figure set ★ (크롭 17 장 = `litdb/figures/zhou2026_gyroid_structural_electrolyte_stiffness_ionic_tradeoff/`)

| 파일 | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| `fig_1.png` | 그림 1 — 고체 영역 6 기하 ((1:1:1) · (2:1:1) · (2:2:1) · (4:1:1) · (4:2:1) · (4:4:1)) · 축 표지 x 빨강 · y 초록 · z 파랑 | 곡면 **벽 (sheet)** 처럼 보인다 — §7-3 시트 판정과 맞는 정성 근거 |
| `fig_2.png` | 그림 2 — 액체 영역 (같은 6 기하 · 직육면체 − 고체) | 액체가 벽에 갈린 미로 — 4:4:1 은 판 모양 층 (z 로 눌린 꼴) |
| `fig_3.png` | 그림 3 — (a) (1:1:1) Ē (주황 · 왼쪽 축) · κ̄ (초록 · 오른쪽 축) vs 공극률 0.2–0.9 · (b) 계산 τ vs 공극률 (2.29 → 1.57) | 공극률 = 물성 사이 trade-off · τ 는 tau2 (√ 아님) |
| `fig_4.png` | 그림 4 — 6 기하 × x · y · z 정규화 탄성계수 막대 (밑에 고체 기하 그림) | 늘린 축 ↑ · 가로 축 ↓ · (4:4:1) z 0.0125 |
| `fig_5.png` | 그림 5 — 같은 배치의 정규화 이온전도 막대 (밑에 액체 기하 그림) | 강성보다 방향차가 작다 (최대 0.559 ↔ 0.105) |
| `fig_6.png` | 그림 6 — 계산 τ 막대 · (4:4:1) z **5.70** · (4:1:1) x **1.07** | 협착 없이 기하 (눌린 꼴) 만으로 tau2 ≈ 5.7 — 우리 ps45 FULL 5.0–7.2 와 같은 크기 (§7-4) |
| `fig_7.png` | 그림 7 — Ē vs κ̄ 지도 (x 보라 원 · y 초록 네모 · z 파랑 세모 · 기하 표지) | 18 점 한 직선 (Ē ≈ −0.057 + 0.720 κ̄, R² 0.991 [우리 산술]) — 방향 사이 trade-off |
| `fig_8.png` | 그림 8 — 위: E_max/E_min (주황) · κ_max/κ_min (초록) 막대 · 아래: 6 물성 × 6 기하 열지도 ((1:1:1) 대비 배수 · 0.1×–2.0× 색 막대) | 이방성 효과의 크기 비 (강성 20.5 ↔ 전도 4.0) · 숫자 48 개 → `digitized.csv` |
| `tab_I.png` | 표 I — (1:1:1) · ε 0.2–0.9 · Ē · κ̄ · τ | 원자료 (그림 3) |
| `tab_II.png` | 표 II — ε 0.6 · 6 기하 · Ē · κ̄ · τ 방향별 | 원자료 (그림 4–8) |
| `tab_III.png` | 표 III — Ē · Ḡ · ν (공극률 8 + 이방 5 행) · 주 (대칭 방향 차 = STL · 메시) | ν > 0.5 행 · 메시 잡음 언급 |
| `eq_1.png` | 식 (1) 등위면 | 재현 입력 |
| `eq_12.png` · `eq_16.png` · `eq_17.png` | i = −κ_l∇ϕ · i_avg = (1/V_cell)∫_Ωl i dV · i_avg = −κ_eff(∇ϕ)_avg | **V_cell 정규화** ⇒ κ̄ = f (§7-2) |
| `eq_18.png` | Ē_i = E_i^eff/E_s · κ̄_i = κ_i^eff/κ_l | 정규화 |
| `eq_19.png` | τ_i = ε (1/κ̄_i) · "where ε is the porosity" | τ = tau2 의 근거 문장 |

---

## 6. Post-processing ★

- **원문**: 표 값 → 차원값 (× E_s · × κ_l) · τ (식 19) · 방향 막대 (그림 4–6) · E–κ 산점 지도 (그림 7) · 이방성 비 E_max/E_min · κ_max/κ_min + (1:1:1) 대비 열지도 (그림 8).  통계 · 오차 막대 없음 (결정론 계산).  도구 = MATLAB (기하) · COMSOL (FE) — 버전 [미확인] · 그림 글꼴로 보아 matplotlib 계열 [추정].
- **우리 (이 카드)**:
  1. 표 I–III 전사 → 텍스트 층과 프로그램 대조 (27 행 전부 일치) + 렌더 대조 · ε/κ̄ 재계산 (`source_data_tables.csv`).
  2. 그림 8 안 숫자 48 개 판독 (2 배 확대) ↔ 표 II 재계산 (±0.01 · `digitized.csv`) · 그림 3–7 은 표의 그림 — 육안 대조 (화소 판독 불필요).
  3. ★ **독립 복셀 FV 재현** (`ours_voxel_fv_reproduction.csv`): 식 (1) 을 단위셀 N³ 격자 (N 64 · 128) 셀 중심에서 계산 → 고체 정의 둘 (시트 · 네트워크, 분위수로 ε 정확히 맞춤) → 액체만 전도 (고체 0 · 경계면 절연 = 조화평균 면 규칙) · 주기 · 단위 기울기 · κ̄ = 셀 부피 평균 전류 · 비입방 복셀 (a/N · b/N · c/N) 로 a:b:c 아핀 늘림 · CG (Jacobi, rtol 10⁻¹⁰, 전부 수렴) · 1 차 Richardson (2κ₁₂₈ − κ₆₄).  사용 전 손풀이 검사: 전부 액체 = 1 · 판 0.5/0.5/0 · 막대 = 면적분율 · 절연 벽 0 / 15/16 (정확) · 절연 구 φ 0.1 · 0.3 ↔ Maxwell −0.7 · −2.2 % (N 48).
  4. d_h = V_liq/S (공면적 공식 · 256³ · 검산 = F = 0 면적 3.091 / 단위셀 — 흔히 인용되는 ≈3.09 와 같음, 출처 카드 없음) → d_h/dx.
  5. 파생: HS · Bruggeman · Archie · 강성 국소 지수 · 입방 이방성 계수 · ν 정치성 · 방향 평균 · E–κ 직선.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 메인 리포 `docs/data/ps45_r45_network_g2_20261007/README.md` · `scripts/step3_sigma.py` · CLAUDE.md 의 해당 절을 병기해 적는다)

### 7-1. 비교표

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 대상 | 설계된 자이로이드 단위셀 (고체 골격 + 액체) · 입자 없음 | LPSCl SE + NCM811 압밀 복합 양극 · 입자 (DEM 구 · MPM 소성 SE) | ⛔ 계 · 소재 · 상 다름 — **정규화 기하 결과만** 옮길 수 있다 |
| 수송 솔버 | 연속체 FEM (COMSOL) · 주기 단위셀 · x · y · z | ① 접촉망 Kirchhoff + Holm (DEM) ② STEP3 복셀 FV (`solve_sigma_z` — "Finite volume, harmonic-mean face" · **z 만** · 옆면 Neumann 또는 `periodic_xy`) | 연속체 (그들) ≈ 우리 ② 의 부류 (CONTACT_FREE · CL-81) · 우리 ① 의 접촉 협착 항은 그들에 없다 |
| 계면 저항 | 없음 (액체 한 상 연속 · 고체 경계 절연) | 접촉망 = 접촉마다 1/(2σa) · STEP3 = 0 (Rint ①′ 구현 기구는 기본 꺼짐) | 그들 기하에서는 0 이 정확 · 우리 입자 매질에서는 0 이 결손 |
| τ 정의 | τ = ε/κ̄ (식 19) | tau2 = φ_SE σ₀/σ_eff (키 `tau2_ion_<mode>`) | **같은 양** (§7-2) |
| 역학 | 선형 탄성 주기 균질화 → C_eff (이방 E · G · ν) | MPM J2 소성 압밀 (E_eff 1.53 GPa · σ_y 0.30 GPa · ν_SE 0.49 — 3D 생산값) · DEM hooke/hysteresis (E_eff 1.35 GPa) | 그들 = 작은 변형 탄성 텐서 · 우리 = 큰 변형 압밀 과정 — **다른 질문** · 유효 탄성 텐서는 우리에게 없다 (§7-5) |
| 이방성 | 아핀 늘림 a:b:c 를 손잡이로 · 방향 3 개 다 계산 | 압밀 (z) 이 만든 이방성 · σ 는 z 만 | 우리 σ_x · σ_y 미측정 — §8-4 |
| 검증 | 실험 없음 | 실험 앵커에 각각 보정 (frame [4]) | 이 논문은 **해법 검증 표적** (verification) 으로만 |

### 7-2. ★ τ 규약 — 원문 τ = 우리 tau2 (수송 tortuosity)
- 식 (16) 이 액체 적분을 **셀 전체 부피 V_cell** 로 나눈다 → κ_eff 는 복합체 유효 전도 → κ̄ = κ_eff/κ_l = 우리 **f** (`f_ion_<mode>` 의 같은 정의).
- 식 (19) τ_i = ε/κ̄_i → 우리 **tau2 = φ/f** (`tau2_ion_<mode>`) · Tjaden κ = τ² · TauFactor τ · COMSOL τ_F 와 같은 양 (litdb J 절 표의 tau2 행).  원문은 'tortuosity factor' 라는 낱말을 쓰지 않는다 (Thorat 와 같은 경우) — **√ 를 씌우지 않는다**.
- 원문은 τ 를 "path complexity" · "more direct conduction paths" 로 읽는다 (p.7) — 그러나 tau2 에는 경로 길이와 단면 변화가 함께 든다 (Holzer 의 협착 δ 와 같은 몫).  (4:1:1) x 의 1.07 은 거의 곧은 채널 (Wiener 1 근처).
- 기준 상태: σ₀ = **액체 벌크 κ_l** (모형 입력 · 순수 상 ≡ 1) — 우리 σ₀ (펠릿 3.0 · 보고 1.5 mS/cm) 와 지위가 다르지만 **정규화 tau2 는 σ₀ 와 무관** (선형) — 기준 상태 장부 (J 절) 의 "모형 입력 벌크 = 1" 부류.

### 7-3. ★ 우리 STEP3 부류 복셀 FV 로 표 I · II 를 다시 풀었다 [우리 산술 — 독립 재현 · 논문 값 아님]

**표 I (1:1:1) — κ̄**

| ε | 원문 κ̄ | 시트 N 64 | 시트 N 128 | 시트 외삽 | 외삽 ÷ 원문 − 1 | 네트워크 외삽 | 네트워크 ÷ 원문 − 1 | d_h/dx (시트, N 64) |
|---|---|---|---|---|---|---|---|---|
| 0.9 | 0.574 | 0.5541 | 0.5633 | 0.5725 | −0.26 % | 0.8341 | +45.3 % | 9.39 |
| 0.8 | 0.487 | 0.4684 | 0.4776 | 0.4868 | −0.04 % | 0.6841 | +40.5 % | 8.40 |
| 0.7 | 0.406 | 0.3908 | 0.3986 | 0.4064 | +0.10 % | 0.5523 | +36.0 % | 7.57 |
| 0.6 | 0.332 | 0.3169 | 0.3249 | 0.3329 | +0.27 % | 0.4353 | +31.1 % | 6.77 |
| 0.5 | 0.264 | 0.2499 | 0.2568 | 0.2637 | −0.11 % | 0.3326 | +26.0 % | 5.89 |
| 0.4 | 0.199 | 0.1881 | 0.1940 | 0.1999 | +0.45 % | 0.2435 | +22.4 % | 5.06 |
| 0.3 | 0.140 | 0.1311 | 0.1363 | 0.1415 | +1.07 % | 0.1666 | +19.0 % | 4.19 |
| 0.2 | 0.0872 | 0.0798 | 0.0835 | 0.0872 | +0.00 % | 0.0999 | +14.6 % | 3.28 |

- **표 II (ε 0.6 · 시트)**: 18 칸 외삽 ÷ 원문 − 1 = **0.00 … +2.10 %** · 가장 큰 차는 눌린 가로 방향 ((4:4:1) z +2.1 % · (4:1:1) y · z +1.4 % · (4:2:1) z +1.4 %) = 비입방 복셀의 느린 수렴 [추정] · N 64 원값은 −3.9 … −8.0 %.
- **판정 ①** — 원문 고체 = **시트형** (두 등위면 사이 막).  네트워크형은 모든 ε 에서 +15 … +45 % 어긋나고 격자를 조여도 멀어진다.  그림 1 의 곡면 벽 모양 (정성) · 저밀도 강성 n ≈ 1.1 (늘림 지배, §3-2) 과도 맞는다.  원문 식 (1) 은 등위면 **하나** 만 적는다 → 재현하려는 사람은 이 카드의 판정을 써야 한다.
- **판정 ②** — 조화평균 면 복셀 FV (우리 STEP3 와 같은 부류) 는 이 매끈한 기하에서 **1 차로 수렴하고 (오차 ∝ 1/N), 덜 풀린 쪽은 항상 낮게 (−) 나온다**.  같은 기하 · 같은 방정식에서 두 이산화 (FEM ↔ 복셀 FV) 가 1 % 안 = **해법 검증 (verification)** · 물리 검증 (validation) 아님 (frame [4] 의 교차검증과 다른 층).
- **판정 ③ — 해상도 오차 규칙 (이 기하 한정)**: 원문 대비 오차 ≈ **−0.28/(d_h/dx)** (시트 28 점 · d_h/dx 1.6–18.8 · 최대 잔차 1.3 %p · 곱 −0.22 … −0.35) — d_h/dx 1.64 → −16.4 % (N 32 · ε 0.2) · 3.3 → −8.5 % · 4.7 → −7.3 % · 6.6 → −4.2 % · 9.4 → −3.5 % · 18.8 → −1.9 %.
  - 우리 MPM SE 응력 규칙 (d_h/dx ≳ 3.5 — 3.43 셀 +4.0 % · 1.18 셀 +23.8 %, 메인 CLAUDE.md SE 응답곡선 절 ⑤) 과 **다른 양이지만 같은 크기대** — 전도는 d_h/dx 3.5 에서 ≈ −8 %.
  - 우리 STEP3 σ_ion 절대값이 vox 0.4 → 0.25 에서 **SBE +27.0 % · DBE +26.7 %** 로 오른 것 (메인 CLAUDE.md SR-01 · CL-24) 과 **방향이 같다** (덜 풀린 채널 = σ 낮음) [추정 — 우리 쪽은 첨가제 · 목 (neck) · 가짜 상호연결이 섞여 크기 대조 불가].  ⚠ 이 기하에는 입자 접촉 목이 없어 STEP3 의 두 번째 인공물 (가짜 상호연결 = σ↑, CL-24) 이 **나타나지 않는다** — 이 규칙은 "계단 길이" 인공물 하나만 잰 값이다.

### 7-4. ★ 우리 접촉망 (ps45) 수송 tortuosity 와의 대조 — "매끈한 연속 채널" 기준선 [우리 산술 · 추정]

| 양 (φ ≈ 0.3) | 값 | 출처 |
|---|---|---|
| 등방 연속체가 가질 수 있는 최소 tau2 = (3−φ)/2 (HS) | **1.350–1.358** (φ_SE 0.2837–0.2994) | [우리 산술 — 표준 식] |
| 매끈한 연속 채널 · 네트워크형 자이로이드 (한 미로) | **≈1.80** (ε 0.3 · 외삽 κ̄ 0.1666) | 우리 재현 |
| 매끈한 연속 채널 · 시트형 자이로이드 (두 미로) | **2.14** (ε 0.3) | 원문 표 I |
| 눌린 (4:4:1) 시트형의 z 방향 · ε 0.6 | **5.70** | 원문 표 II |
| 우리 ps45 Hertz FULL (0:10 · 3:7 · 5:5 · 7:3 · 10:0) | **7.243 · 5.973 · 5.450 · 5.030 · 5.286** | `docs/data/ps45_r45_network_g2_20261007/README.md` |
| 우리 ps45 CF (협착 뺀 같은 망) | **1.789 · 1.503 · 1.372 · 1.282 · 1.247** | 같은 README (협착 전력 몫 73.0–74.7 %) |

- 우리 FULL 5.0–7.2 = 매끈한 연속 채널 (1.8–2.1) 의 **2.4–4.0 배** — 그 차가 접촉 목 (Holm 협착) 몫이라는 ps45 해석 (협착 전력 73–75 %) 과 같은 방향 [추정 — 기하 다름].
- ⚠ 우리 CF 의 **7:3 (1.282) · 10:0 (1.247) 은 등방 연속체 하한 (1.350 · 1.352) 아래**, 5:5 (1.372) 는 겨우 위 — 매끈한 채널 (1.8–2.1) 보다 낮다.  등방 연속체라면 불가능한 값이므로 ① CF 원기둥 bulk 과전도 (단면 πr² · 1.2–1.4 배 · 단순입방 T → 2/3 — 메인 CLAUDE.md τ 블록 · Codex 10-06 5 차) 와 ② 압밀이 만든 z 방향 접촉 이방성 (그러면 z 는 유리할 수 있다 — (4:1:1) x 1.07 처럼) 중 무엇 몫인지 **이 대조로는 가를 수 없다** [추정].  CF × 1.2–1.4 = 1.50–2.50 이면 매끈한 채널 범위로 들어온다 [우리 산술].  ⇒ ps45 README 의 *"경로 몫은 이보다 조금 크고 협착비는 조금 작다"* 한정어를 **연속체 하한이 수치로 뒷받침**한다 (CF 를 '경로 몫' 그대로 읽지 않는다).
- 기하 이방성만으로 (눌린 4:4:1) z tau2 가 1.81 → **5.70 (×3.1)** — 협착 없이도 우리 FULL 크기에 닿는다.  [추정] 연속체로 보면 압밀로 판처럼 눌린 SE 영역도 z tau2 를 키울 수 있는데, DEM 구 (강체) 는 그 몫을 못 그리고 MPM-STEP3 는 그릴 수 있다 (frame [5]) · 반대로 압밀 방향 접촉 정렬은 z 를 유리하게 만든다 — 두 효과의 부호가 반대라 크기는 **측정 전 미상**.

### 7-5. 역학 (MPM 쪽)
- 이 논문의 역학 = **작은 변형 선형 탄성의 유효 텐서**.  우리 MPM 은 J2 소성 압밀 **과정** (형상 변화 · 공극 채움 · 응력장) 이고 균질화 C_eff 를 내지 않는다 — 같은 질문이 아니다.
- 우리에게 없는 능력: **복셀 격자 위 선형 탄성 주기 균질화** (단위 변형 6 경우).  압밀이 끝난 MPM 상 격자 (STEP3 가 쓰는 그 격자) 에 걸면 전극의 이방 탄성 텐서 (E_x · E_z · ν) 를 낼 수 있다 [제안] — 단 접촉이 완전 결합으로 들어가 실제보다 뻣뻣하다 (언로딩 · 스프링백은 접촉이 열리므로 비선형) [추정].
- [우리 산술 · 추정] **다공도만으로는 압밀 펠릿의 연화를 설명 못 한다**: 매끈한 시트 자이로이드는 공극 20 % 에서도 강성의 **60 %** (Ē 0.599) 를 지키는데, 냉간압착 LPSCl 펠릿 (공극 13 ± 2 %) 은 조밀 결정의 **≈21 %** (4.7 ÷ 22.1 GPa — `song2025_porous_argyrodite_modulus_fracture_toughness`) 다 → 펠릿의 약함은 공극 부피가 아니라 **입자 사이 목 (접촉)** 에 있다는 쪽 — 우리 frame [2] (연화 = 재배열 · 입계 미끄럼 · 미세파괴의 대리) 의 방향과 맞다 (기하 · 재료 다름 · 자릿수 감).

### 7-6. frame [5] · Rint · 이종기술 · 믹서
- **frame [5]**: 이 논문은 "연속체 역학 + 연속체 수송" 의 **선형 · 설계 기하** 판 — 우리 MPM (역학) + STEP3 (복셀 σ) 쪽 반쪽만, 그것도 과정 (압밀) 없이.  없는 반쪽 = 입자 · 접촉망 (DEM) · 소성 · 실험.
- **frame [4]**: 실험 보정이 없어 앵커가 못 된다 · 우리 재현은 같은 기하 · 같은 방정식의 **해법 검증**이라 "DEM ↔ MPM 서로 맞춤 금지" 규율과 충돌하지 않는다.
- **Rint**: 해당 없음 — 액체가 한 상으로 연속이라 같은 상 계면 (입자 경계) 이 없다.
- **이종기술 논지 · 믹서**: 해당 없음 (혼합 · 코팅 · 응집 없음).

---

## 8. ★★ 우리 연구에 주는 insight (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

**8-1. 원문 τ 는 tau2 다 — 이름이 'tortuosity' 여도.**
- 논문: τ_i = ε/κ̄_i · κ̄ = V_cell 정규화 (식 16–19).
- 뜻: 우리 수송 tortuosity (tau2) 와 그대로 같은 양 · √ 를 씌우면 다른 양이 된다 (1.81 → 1.35 — 웹앱 τ_Lap,eff 쪽 꼴).
- 할 일: litdb J 절 tau2 행에 추가 (색인 줄 파일) · 덱 · 보고에서 이 값을 쓸 때 "수송 tortuosity (= φσ₀/σ_eff, 제곱근 아님)" 한 줄 병기.

**8-2. 답이 알려진 기하 = 복셀 σ 해법 검증 표적.**
- 논문: 표 I 8 점 · 표 II 18 점 (부록이 원자료).
- 우리 산술: 조화평균 면 복셀 FV 가 시트형에서 N 64 · 128 + 1 차 Richardson 으로 **−0.3 … +1.1 %** (표 I) · **0.0 … +2.1 %** (표 II).
- 할 일: STEP3 (또는 웹앱 τ 계산) 에 "자이로이드 시트 κ̄" 시험을 상주시킬 후보 [제안] — CPU 수 초 (N 64) · 기대값 = 표 I × (1 − 0.28/(d_h/dx)) · 판정 = 표 I 8 점 Richardson 외삽 ±1.5 % (표 II 눌린 방향은 ±2.5 %).  격자 · 면 규칙 · 경계 처리를 바꾸는 커밋의 회귀 시험으로 쓸 수 있다.

**8-3. 덜 풀린 매끈한 채널은 σ 를 1/N 꼴로 낮춘다 — d_h/dx 로 미리 읽힌다.**
- 우리 산술: 오차 ≈ −0.28/(d_h/dx) (d_h = V/S).
- 뜻: STEP3 격자를 고를 때 SE 상의 d_h/dx 를 스캐폴드에서 먼저 재면 계단 인공물의 크기를 런 전에 어림할 수 있다 (MPM d_h/dx 규칙과 같은 방식) — 단 입자 목은 d_h 보다 좁아 실제 오차가 더 크고, 가짜 상호연결 (σ↑) 이 반대 방향으로 겹친다 (CL-24) [추정].
- 할 일: STEP3 침대 하나에서 SE 상 V/S 를 재어 이 규칙에 대 보는 짧은 진단 [제안 · 미등록].

**8-4. 이방성은 강성을 크게, 전도를 작게 바꾼다 — 우리는 z 만 잰다.**
- 논문: E_max/E_min ≤ 20.5 ↔ κ_max/κ_min ≤ 4.0 · 한 방향에서 E 와 κ 는 같이 움직인다 (Ē ≈ −0.057 + 0.720 κ̄, R² 0.991 [우리 산술]).
- 뜻: 압밀 (z) 로 생긴 이방성이 있다면 우리 전극의 면내 (x · y) σ 는 z 와 다를 수 있고, 강성은 더 크게 다를 것이다 [추정].
- 할 일: STEP3 를 x · y 로도 풀어 κ_z/κ_x 를 한 침대에서 재기 (지금 `solve_sigma_z` 는 z 만) [제안] · 그 값이 1 근처면 "z 만 잰다" 는 한정이 필요 없어진다.

**8-5. 협착 없이 기하만으로도 tau2 ≈ 5–6 이 나온다.**
- 논문: (4:4:1) z τ 5.70 · (4:2:1) z 4.44 (ε 0.6).
- 뜻: 우리 FULL tau2 5.0–7.2 를 "대부분 접촉 협착" 으로 읽는 것은 **접촉망 모형 안의 분해**이고 (ps45 협착 전력 73–75 %), 연속체에서 판 모양 SE 영역이 만드는 기하 몫은 그 모형에 없다 [추정].
- 할 일: MPM 압밀 침대의 STEP3 tau2 (z) 를 같은 조성의 DEM CF · FULL 과 나란히 보고할 때, 이 기하 몫의 가능성을 한정어로 둔다 (CL-81 복셀 ÷ 접촉망 대조가 열리면 같이) [제안].

**8-6. 매끈한 다공 구조는 공극 20 % 에서 강성 60 % 를 지킨다.**
- 논문: Ē(ε 0.2) = 0.599 · [우리 산술] 국소 n 2.04 (ρ 0.7–0.8) · ρ 0.8 → 1 은 2.30 (ρ = 1 에서 Ē = 1 로 놓고).
- 뜻: 13 % 공극 LPSCl 펠릿의 21 % (Song 2025) 는 공극이 아니라 입자 목 탓 — 우리 E_eff 연화의 정당화 (frame [2]) 와 같은 방향 · 다만 이 논문은 펠릿과 기하 · 재료가 달라 **방향만** [추정].

**8-7. "trade-off" 를 나눠 말한다.**
- 논문: 공극률 = 물성 사이 trade-off (Ē ↓ · κ̄ ↑) · 이방성 = 방향 사이 재분배 (한 방향의 Ē · κ̄ 같이).
- 할 일: 우리 보고에서 "강성–전도 trade-off" 를 말할 때 두 손잡이를 섞지 않는다.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In periodic finite-element homogenization of an idealized gyroid structural electrolyte, increasing porosity from 0.2 to 0.9 lowered the normalized stiffness from 0.599 to 0.0328 and raised the normalized ionic conductivity from 0.0872 to 0.574; at 60 % porosity, unit-cell stretching changed the directional stiffness by up to 28× but the directional conductivity by only ≈5× (Zhou et al., *J. Appl. Phys.* 140, 154901, 2026)."
- "The 'tortuosity' reported there, τ = ε/κ̄ with κ̄ normalized by the whole-cell volume, is the tortuosity factor (φσ₀/σ_eff) — not its square root."
- 국문: *"설계된 자이로이드 단위셀에서 공극률은 강성과 이온전도를 반대로 움직이고 (공극 20 → 90 %: 강성 ×1/18 · 전도 ×6.6), 축 늘림은 한 방향의 둘을 같이 움직인다 (Zhou 2026, 계산 · 실험 검증 없음)."*
- ⚠ 우리 재현 문장은 **[우리 산술]** 표지와 함께만: *"같은 기하를 조화평균 면 복셀 FV 로 다시 풀면 시트형 고체에서 표 I 이 ±1.1 % 안에서 재현된다 (1 차 Richardson · 논문 값 아님)."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **고체 정의 미기재 [우리 산술]**: 식 (1) 은 등위면 하나 (F = t) 뿐인데 고체가 F ≥ t (네트워크형) 인지 −s ≤ F ≤ s (시트형) 인지 적지 않는다.  우리 재현에서 네트워크형은 표 I 과 +15 … +45 % 어긋나고 시트형만 ±1.1 % 로 맞는다 — 원문 그대로 재현하려면 이 판정을 따라야 한다 (그림 1 의 벽 모양도 시트형).
2. **메시 · 요소 · 수렴 정보 없음**: 대칭 방향 차를 "STL 가져오기 · 메시" 탓으로만 적는다 (표 III).  우리 외삽이 1–2 % 안에서 맞으므로 그들 FEM 은 그 정도로 수렴한 것으로 보인다 [추정].
3. **실험 없음 · 재료값 대표값**: E_s 3 GPa · ν_s 0.3 · κ_l 3.53 mS/cm 는 "dimensional reference" — 특정 고분자–전해질 짝이 아니다 (p.5) · 인쇄 결함 · 거칠기 · 층간 계면 · 침투 불완전 · 고분자 팽윤 (전해질 노출) 미반영 (p.5 · p.8).  Duan PIPS 대비 "≈6 배 덜 구불" 은 저자도 "geometry-controlled prediction" 으로 한정 (p.6).
4. **비결합 · 균일 농도**: 응력 ↔ 전해질 재분배 · 농도 구배 · 전달수 · 열역학 인자 없음 (p.3 · p.5) — 운전 중 수송이 아니라 정적 기하 수송 지표.
5. **단위셀 하나 · 주기**: 전극 두께 방향 경계 (집전체 · 분리막) · 유한 두께 효과 없음 — 우리 전극 (판 사이 수십 입자) 과 경계 조건이 다르다.
6. **'tortuosity' 이름**: tau2 를 'tortuosity' 로 부르고 경로 복잡도로 해석한다 — 단면 변화 (협착 δ) 몫도 같이 들어 있다.
7. **ν > 0.5 (표 III (4:4:1) 1.434 · 1.435)** 는 오류가 아니다 — 이방 재료 · 정치성 판정 양수 [우리 산술].
8. **반올림 칼날**: 그림 8 · 본문의 (2:1:1) E_max/E_min 2.3 ↔ 표 값 비 2.35 · (4:4:1) τ_z 5.70 ↔ 0.6/0.105 = 5.714 — 표가 반올림 값이라 생기는 차이 (오류 아님).
9. **"trade-off" 그림 7 의 뜻**: 한 방향 안에서 Ē 와 κ̄ 는 같이 움직인다 (R² 0.991 직선) — 물성 사이 trade-off 가 아니라 방향 사이 재분배 (원문도 "directional trade-off").
10. **전이 한계**: 액체 전해질 · 고분자 골격 · 설계 TPMS — 황화물 입자 복합 양극의 절대값 · 공정에 옮길 수 없다.  옮길 수 있는 것 = 정규화 기하 관계 · τ 정의 · 해법 검증 기준 · 이방성의 상대 크기 (강성 ≫ 전도).

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 5 | S. Deshpande, V. Vidyaprakash, S. Oka, S. S. Dasari, K. W. Liu, C. Wang, J. L. Lutkenhaus, and M. J. Green, "Low-temperature structural battery electrolytes produced by polymerization-induced phase separation," ACS Appl. Polym. Mater. 6(11), 6323–6333 (2024). | 카드 없음 — κ_l 3.53 × 10⁻³ S/cm 의 출처 |
| 6 | S. Duan, M. Cattaruzza, V. Tu, R. M. Auenhammer, R. Jänicke, M. K. G. Johansson, F. Liu, and L. E. Asp, "Three-dimensional reconstruction and computational analysis of a structural battery composite electrolyte," Commun. Mater. 4(1), 49 (2023). | 카드 없음 — ★ 재구성 실구조 (PIPS) 의 같은 균질화 · 이상 기하와의 대조 (tau2 ≈12.5 ↔ 2.0 [우리 산술]) |
| 8 | V. Tu, L. E. Asp, N. Shirshova, F. Larsson, K. Runesson, and R. Jänicke, "Performance of bicontinuous structural electrolytes," Multifunct. Mater. 3(2), 025001 (2020). | 카드 없음 — 합성 · 재구성 미세구조 계산 균질화의 선행 |
| 26 | R. Tavano, M. Spagnol, N. Al-Ramahi, R. Joffe, J. Xu, and L. E. Asp, "Mechanical characterisation of a structural battery electrolyte," Polymer 312, 127646 (2024). | 카드 없음 — SBE 실측 400–600 MPa · 10⁻⁴ S/cm |
| 48 | I. Maskery, L. Sturm, A. O. Aremu, A. Panesar, C. B. Williams, C. J. Tuck, R. D. Wildman, I. A. Ashcroft, and R. J. M. Hague, "Insights into the mechanical properties of several triply periodic minimal surface lattice structures made by polymer additive manufacturing," Polymer 152, 62–71 (2018). | 카드 없음 — 식 (1) 의 출처 · 고체 정의 (시트/네트워크) 확인 후보 |
| 51 | J.-W. Luo, L. Chen, T. Min, F. Shan, Q. Kang, and W. Tao, "Macroscopic transport properties of gyroid structures based on pore-scale studies: Permeability, diffusivity and thermal conductivity," Int. J. Heat Mass Transfer 146, 118837 (2020). | 카드 없음 — ★ 자이로이드 확산 · 열전도의 독립 수치 = 우리 복셀 시험 (§8-2) 의 두 번째 기준값 후보 |
| 55 | D. W. Abueidda, M. Elhebeary, C.-S. Shiang, S. Pang, R. K. Abu Al-Rub, and I. M. Jasiuk, "Mechanical properties of 3D printed polymeric gyroid cellular structures: Experimental and finite element study," Mater. Des. 165, 107597 (2019). | 카드 없음 — 인쇄 자이로이드 강성 실측 ↔ FE |
| 58 | S. Zekoll, C. Marriner-Edwards, A. K. O. Hekselman, J. Kasemchainan, C. Kuss, D. E. J. Armstrong, D. Cai, R. J. Wallace, F. H. Richter, J. H. J. Thijssen, and P. G. Bruce, "Hybrid electrolytes with 3D bicontinuous ordered ceramic and polymer microchannels for all-solid-state batteries," Energy Environ. Sci. 11(1), 185–201 (2018). | 카드 없음 — ★ 전고체 쪽 이중연속 설계 기하 (세라믹–고분자) |
| 59 | D. Carlstedt, K. Runesson, F. Larsson, V. Tu, R. Jänicke, and L. E. Asp, "Computational modelling of structural batteries accounting for stress-assisted convection in the electrolyte," Int. J. Solids Struct. 238, 111343 (2022). | 카드 없음 — 이 논문이 뺀 역학 ↔ 수송 결합 |
| 60 | T. Zhou, C. Metlich, J. A. Pranada, D. Lagoudas, A. Castellanos, and S. Lin, "Modeling the microstructure-dependent elastic modulus and ionic conductivity of structural battery electrolyte for low-temperature applications," in Repair and Multifunctional Applications (Springer Nature Switzerland, 2026), pp. 273–286. | 카드 없음 — 같은 그룹 선행 (방법 원형) |
| 63 | D. P. Finegan, S. J. Cooper, B. Tjaden, O. O. Taiwo, J. Gelb, G. Hinds, D. J. L. Brett, and P. R. Shearing, "Characterising the structural properties of polymer separators for lithium-ion batteries in 3D using phase contrast x-ray microscopy," J. Power Sources 333, 184–192 (2016). | 카드 없음 — 분리막 공극률 범위 · TauFactor 그룹 (`taufactor_…` · `cooper2017_…` 와 같은 저자들) |
| 64 | N. Qiu, Y. Wan, Y. Shen, and J. Fang, "Experimental and numerical studies on mechanical properties of TPMS structures," Int. J. Mech. Sci. 261, 108657 (2024). | 카드 없음 — 위상별 (자이로이드 · 다이아몬드 · 프리미티브) 강성 차 |
| 66 | M. Zhao, X. Li, D. Z. Zhang, and W. Zhai, "TPMS-based interpenetrating lattice structures: Design, mechanical properties and multiscale optimization," Int. J. Mech. Sci. 244, 108092 (2023). | 카드 없음 — 이중연속 (interpenetrating) 격자 설계 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-27)
- 원문 13 쪽 (표지 + 본문 12 쪽) 텍스트 층 전수 · 저자 · 소속 · 날짜 · 연구비 · DOI · Special Topic = p.1 · p.9.  보충자료 언급 없음 (텍스트 검색) · 메시 · 요소 · 수렴 서술 없음 (텍스트 검색).
- 식 (1) 의 "− t = 0" · 식 (12) · (17) 의 음부호 · 식 (19) 의 꼴은 텍스트 층에서 기호가 빠지거나 바뀌어 (¼ · þ) **쪽 렌더 (eq 크롭)** 로 확인.
- 표 I–III = 칸마다 렌더와 텍스트 층 대조 + 프로그램 대조 (27 행 · 불일치 0) · 표 III 의 Ē 열 = 표 I · II 와 같음.  τ = ε/κ̄ 재계산 최대 차 0.014 (반올림).
- 그림 1–8 = 삽입 래스터 8 장 (모두 300 dpi) · 겹치는 글자 · 벡터 없음 확인 → 래스터 경계 그대로 크롭 · 그림 8 안 숫자 48 개 = 2 배 확대 렌더로 판독 · 그림 3–7 은 표와 육안 대조.
- 정본 litdb 중복 확인: `git ls-tree` 로 `litdb/papers/` 전수 (442 파일 · 정본 `aaa275e20`) + DOI (`5.0341375`) · 'gyroid' · 'Tianyang' · 'Lagoudas' · 'Metlich' · '154901' · 'TPMS' · 'triply periodic' 로 `litdb/` (md · json · csv) grep — 이 논문 카드 없음 · 자이로이드 · TPMS 를 다룬 카드도 없음 ('structural battery' 는 sendek2017 한 줄 언급뿐).
- 우리 재현 스크립트 (독립 · 약 150 줄 · numpy/scipy · 손풀이 시험 15 개 통과) 는 이 세션 스크래치에만 있다 (사라질 수 있음) — 방법 전부를 `ours_voxel_fv_reproduction.csv` 머리 주석과 §6-3 에 적었다 (다시 짤 수 있게).

## 🔗 관련 카드
- 연속체 ↔ 접촉망 수송: `bazzoun2026_dem_fem_rnm_ionic` · `bielefeld2020_effective_ionic_conductivity_binder` · `froboese2019_microstructure_ionic_conductivity_assb_electrode` (고분자 전해질 + 비활성 구 모델계).
- τ 정의 · 연속체 tau2 ≥ 1: `tjaden2018_tortuosity_review_calculation_approaches` · `taufactor_tortuosity_factor_tomography_tool` · `cooper2017_simulated_impedance_diffusion_porous_media` · `ender2011_3d_reconstruction_composite_cathode` · `hlushkou2018_void_space_ion_transport_assb_cathode` · `holzer2013_constrictivity_effective_transport_porous_layers` · `thorat2009_quantifying_tortuosity_porous_liion` (같은 'factor' 없는 τ) · `nguyen2020_electrode_tortuosity_factor`.
- 실구조 FV σ: `lee2026_unveiling_ptfe_dry_electrode_digital_twin` · `minnmann2021_jes_charge_transport_bottlenecks`.
- 역학 (다공 SE 강성): `song2025_porous_argyrodite_modulus_fracture_toughness`.
- FEM 압축 · 디지털 트윈: `lim2025_virtual_calendering_framework` · `park2020_digitaltwin_assb_foundational`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
