<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 후보 표 N-52 · 정독 101) 에서 꼭 뽑으라고 한 항목.
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 · 두 필수 절 §0-1 · §8) · 계산 논문의 방법 절 · 식 크롭 꼴 = gritton2017_mpm_chemomechanical_coupling_silicon_anode.md.
     원문 = 출판본 (J. Mech. Phys. Solids 198 (2025) 106060 · 19 쪽 · CC BY-NC-ND).  보충 자료는 없다 (원문이 보충 자료를 말하지 않는다 · 부록 = 본문 p.16 의 Fig. A.1 · A.2).
     쪽 표기 = PDF 쪽 = 인쇄 쪽 번호 (p.1–19 · 참고문헌 p.17–19).  크롭 파일 이름의 pN 과 figures.json 의 page 도 같은 번호다.
     기호: 원문의 임계 에너지 해방률 𝒢c 는 이 카드에서 G_c 로, 이력 장 ℋ_d 는 H_d 로 적는다.  ℓ₀ = phase-field 특성 폭 · L₀ = 2ℓ₀ · ξ = 손상 변수 (0 = 온전 · 1 = 완전 파괴).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 1155 행 — 전압–용량 곡선과 Fig. A.1 은 벡터 경로라 꼭짓점 좌표를 그대로 읽고
     축은 인쇄된 눈금 두 개로 보정 · Fig. 14a 'No pores' 곡선 끝과 Fig. 3 상 분율 · 입자 크기는 박힌 래스터의 색 분류) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) ·
     [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드에 적힌 값 (그 카드 slug 병기) · [우리] = 우리 쪽 값 (CLAUDE.md 출처) · [미확인] = 본문 19 쪽 전수에 없음.
     원문 19 쪽을 글자 층 추출 + 전 쪽 렌더로 전부 읽었다.  DEM · 입자 계산 · 압밀 계산 · 소성은 이 논문에 없다 — 주어진 미세구조 위의 연속체 유한요소 (선형 탄성 + phase-field 손상) 다. -->
# 황화물 전고체전지 복합 양극 (NMC811 + Li₆PS₅Cl) 의 전기화학–화학–역학 완전 결합 2D 평면변형 유한요소 phase-field 파괴 모형 (COMSOL · AT-1 · ℓ₀ 100 nm · ≈3.5 M 자유도 · 선형 탄성 · 소성 없음) — 운전 적층압 0 / 5 / 40 MPa · 공극 15 % ↔ 0 % · 계면 G_c 0.2–2 J m⁻² · LLZO 대조: 0.1 C 충전 용량 무압 150.7 ↔ 40 MPa 185.7 mAh g⁻¹ [벡터 판독] · 출발 = 무응력 (성형 잔류 응력 무시) — Taghikhani · Huber · Weddle · Asle Zaeem · Berger · Kee (J. Mech. Phys. Solids 2025)

> slug `taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode` · DOI `10.1016/j.jmps.2025.106060` · type `FEM (2D plane-strain · fully coupled electro-chemo-mechanical continuum + AT-1 phase-field fracture · COMSOL Multiphysics · segregated solver · ≈3.5 M DOF · linear elastic, small strain) — DEM · 입자 계산 · 압밀 · 소성 없음` · PDF `0f941354-52._Modeling_coupled_electro-chemo-mechanical_phenomena_within_all-solid-state_battery_composite_cathodes.pdf` (19 쪽 · 보충 자료 없음) · digested `2026-11-12` · status ✅
>
> **저자**: **Kasra Taghikhani\*** ᵃ · William Huber ᵃ · Peter J. Weddle ᵇ · Mohsen Asle Zaeem ᵃ · J. R. Berger ᵃ · Robert J. Kee ᵃ — ᵃ Department of Mechanical Engineering, Colorado School of Mines, Golden, 80401, CO, USA · ᵇ National Renewable Energy Laboratory, Golden, 80401, CO, USA — \* 교신 (kasrataghikhani@mines.edu) · *J. Mech. Phys. Solids* **198** (2025) **106060** · 접수 2024-12-02 · 수정 2025-01-28 · 수락 2025-01-29 · 온라인 2025-02-06 · © 2025 The Authors · Elsevier · **CC BY-NC-ND** · 키워드 *All-solid-state battery · Composite cathode · Electro-chemo-mechanical modeling · Phase-field fracture · Degradation predictions* · 연구비 = AFOSR **FA9550-22-1-0053** · NREL (DOE **DE-AC36-08GO28308**) · 자료 = *"No data was used for the research described in the article."* (p.17)
> **이웃 카드 (링크만)**: 이 논문을 가리킨 카드 = [`lei2026_se_particle_size_effects_review`](lei2026_se_particle_size_effects_review.md) (L115 · L144 · L172 — ⚠ 거기 적힌 값은 이 논문에 없다 · §0-1) · [`liang2026_interface_bottleneck_solid_state_batteries`](liang2026_interface_bottleneck_solid_state_batteries.md) (L246 · ref [97]) · [`zhang2026_polymer_electrolyte_modeling_perspective`](zhang2026_polymer_electrolyte_modeling_perspective.md) (L124 · ref 162).  이 논문이 딛고 선 것 = [`bielefeld2020_effective_ionic_conductivity_binder`](bielefeld2020_effective_ionic_conductivity_binder.md) · [`bielefeld2019_microstructural_modeling_composite_cathode`](bielefeld2019_microstructural_modeling_composite_cathode.md) (Bielefeld 2022 는 카드 없음) · [`doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density`](doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density.md) (미세구조 그림의 원 SEM) · [`mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation`](mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation.md) (LPSC G_c 의 출처) · [`deng2016_elastic_superionic_electrolytes_dft`](deng2016_elastic_superionic_electrolytes_dft.md) (LPSC E · ν) · [`bucci2017_chemomech_failure_assb_cycling_czm`](bucci2017_chemomech_failure_assb_cycling_czm.md) (같은 질문의 응집 영역 모형) · [`kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation`](kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md) · [`trevisanello2021_sc_pc_ncm_cracking_diffusion`](trevisanello2021_sc_pc_ncm_cracking_diffusion.md).
> **판독 원자료**: `litdb/figures/taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode/digitized.csv` (1155 행 — Fig. 7 · 8a · 9a · 10a · 11 · 12 · 13 · 14a 전압–용량 곡선의 벡터 꼭짓점 · Fig. 13 세 사이클의 꺾임점 요약 · Fig. A.1 표지 79 개 · Fig. 3 상 면적 분율과 입자 · 공극 크기) · 그림 크롭 **89 장** (도구 15 = Fig. 1–14 + Table 1 전부 다시 자름 · 손 크롭 74 = 부록 그림 2 · 패널 7 · **식 40 = 식 (1)–(40) 하나씩** · 근거 문단 25) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: LiₓNi₀.₈Mn₀.₁Co₀.₁O₂ (NMC) 입자가 Li₆PS₅Cl (LPSC) 매트릭스에 박힌 복합 양극의 **(40 × 40) µm² 2D 단면** (공극 "≈15 %" · SEM 그림을 손으로 고쳐 만든 기하) 위에서 Li 확산 · 전하 보존 · 준정적 힘 평형 · **AT-1 phase-field 파괴** 를 완전 결합해 COMSOL 로 풀어 (2 차 삼각 요소 · ≈3.5 M 자유도 · ℓ₀ 100 nm), 0.1 C 충전 용량이 **운전 적층압 0 MPa 에서 150.7 → 40 MPa 에서 185.7 mAh g⁻¹**, **공극 15 % → 0 % 에서 184.1 → ≈190–191**, **계면 G_c 0.2 / 1.0 / 2.0 J m⁻² (무압) 에서 145.6 / 150.7 / 185.8**, **SE 를 LLZO 로 바꾸면 181.4** (LPSC 186.4) 로 달라진다고 보고한다 (전부 [판독 · 벡터 경로] — 원문 본문에는 이 용량 숫자가 "186" 하나만 인쇄돼 있다).  **모든 재료는 선형 탄성 · 작은 변형** (LPSC E 22.1 GPa · ν 0.37) — 소성 · 큰 변형 · 접촉 · 가압 성형 · 탈압 계산은 없고, 출발 상태는 **무응력**이다 (*"This assumption neglects the effect of residual stress developed during the fabrication process"*, p.9).  검증은 Bielefeld 2022 에서 다시 실은 전압 곡선 한 벌 (세 전류) 이고 모형은 세 전류 모두 용량을 **+4.7 / +7.0 / +13.7 %** 과대 예측한다 [판독].

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 무엇을 · 몇 차원으로 · 어떤 격자로 풀었나 | **2D 평면 변형** (면 밖 방향 화학 팽창 없음) · 반쪽 셀 = (40 × 40) µm² 복합 양극 + 10 µm SE 분리막 + 1 µm 집전체 · COMSOL Multiphysics 유한요소 · **2 차 삼각 요소 · "approximately 3.5 million degrees of freedom"** · segregated solver · 계면에서 h_max < 0.5 ℓ₀ · 요소 수 · 시간 간격 · 계산 시간 [미확인] | [인쇄] p.9 · p.11 · Fig. 3 · 6 |
| ② ★ 지배 방정식 · 구성식 · 파괴 · 계면 · 경계 조건 | 식 **(1)–(40)** 전부 (§4-1 · 식 번호별 크롭 40 장): AT-1 파괴 에너지 (5) · 부피–편차 인장 / 압축 분리 (7)–(11) · 화학 팽창 변형률 (13) · 화학–역학 퍼텐셜 (22) · 유속 (24) · 전하 보존 (25)(26) · 힘 평형 (27) · 손상된 응력–변형률 (28)–(30) · 문턱 + 이력 장 (32)–(34) · Butler–Volmer (38) · 손상으로 깎인 교환 전류 (39) · 응력 항이 든 과전압 (40) | [인쇄] p.3–9 |
| ③ ★ 재료 값 표 | Table 1 (24 행 · §3-2 전사): NMC E **175.27 GPa** · ν 0.2819 · G_c 2.5 J m⁻² · β^iso 1.5759 × 10⁻⁷ m³ mol⁻¹ · K_ed 100 S m⁻¹ / LPSC E **22.1 GPa** · ν **0.37** · G_c **2.785 J m⁻²** · K_el 0.7 mS cm⁻¹ / 계면 G_c **1.0 J m⁻²** (출처 없음) · ℓ₀ **1 × 10⁻⁷ m** / LLZO E 149.8 GPa · G_c 9.7416 J m⁻² · K_el 0.33 mS cm⁻¹ | [인쇄] p.10 Table 1 |
| ④ ★ 적층압 (externally applied pressure) 효과 — 값과 조건 | 운전 중 **왼쪽 (분리막 쪽) 경계에 일정 압력 p** · 위 · 오른쪽 · 아래는 롤러 · 0.1 C 충전 끝 용량 [판독]: **0 MPa 150.7 · 5 MPa 185.6 (사이클 런 CC 끝) · 40 MPa 185.7–186.5** mAh g⁻¹ → 0 ↔ 5 MPa 사이에서 다 변하고 5 ↔ 40 MPa 는 ≈1 mAh g⁻¹ 차 · 무압 곡선에는 계면 균열이 자랄 때 생기는 전압 계단 셋 (Q ≈ 103 · 122–124 · 128) · 저자 스스로 *"the present model has limitations in evaluating the effects of changing external pressure"* (p.13) · 압력별 실험 대조 없음 | [판독] Fig. 9a · 10a · 13 · [인쇄] p.12–14 |
| ⑤ ★ 공극 (void) 효과 | 두 구조만: "≈15 % porosity" (그림 기하 · 2D 면적 분율 — 래스터 판독 **12.5 % (윤곽선 빼고 다시 나누면 14.5 %)**) ↔ "no pores" · 0.1 C · 40 MPa 끝 용량 **184.1 ↔ ≈190–191** [판독] (+3–4 %) · 공극 없는 쪽이 균열은 훨씬 많다 (*"the pores act as a stress relieving interface"*, p.14) · 공극 자리를 무엇으로 채웠는지 [미확인] · 공극 크기 · 분포를 바꾼 계산은 없다 | [판독] Fig. 14a · Fig. 3 · [인쇄] p.14 |
| ⑥ ★ 계면 분리 · 균열 (조건 R2 · R7) | 분리 = **손상 변수 ξ** (계면 G_c 1.0 J m⁻² 를 폭 ℓ₀ 의 띠로 퍼뜨림 · Fig. 5) → ξ 가 커지면 교환 전류 (39) · 확산 (21) · 인장 / 전단 강성 (28) 이 (1 − ξ)² 로 꺼진다 · **분리 틈 (nm) · 미끄럼 · 마찰 · 다시 닿음은 없다** · 균열은 *"mainly concentrated at the electrode-electrolyte interfaces"* (p.12) · NMC 내부 파괴는 G_c 2.5 로 허용돼 있으나 1 차 입자 사이 (입계) 파괴는 넣지 않았다고 스스로 적음 (p.11 · p.13) | [인쇄] p.9 · p.11–13 |
| ⑦ 검증에 쓴 실험 | 전압–용량 곡선 한 벌 (0.02 C · 0.1 C · 빠른 전류) — 그림 캡션: *"Experimental data reproduced with permission from Bielefeld et al. (2022)"* · 본문은 Janek 그룹 실험 (Ruess 2020 · Trevisanello 2021 · Conforto 2021) 이라고 적음 · **실험 셀의 조성 · 적층압 · 온도 · 두께는 이 논문에 인쇄되지 않았다** [미확인] · 모형 ÷ 실험 끝 용량 203.8 / 194.6 · 183.8 / 171.7 · 128.4 / 112.9 [판독] | [인쇄] p.3 · p.11 · [판독] Fig. 7 |
| ⑧ ★ DEM 한계를 말한 문장 | **말 없음** — DEM · 입자 계산을 쓰지도 언급하지도 않는다 (낱말 *discrete · DEM* 0 회).  선행 방법 목록은 응집 영역 · phase-field · 연속체 손상 · 유효 스프링 · 확장 유한요소 (p.2–3) | 원문 전수 |
| ⑨ ★ 소성 · 큰 변형 | **없음** — LPSC 를 *"sufficiently malleable so as to maintain interfacial contact under external pressure"* (p.2) 라고 부르면서 계산은 선형 탄성 · 작은 변형 (식 12 · 28 · 30) · 이유 설명 없음 · 낱말 *plastic · yield · creep* 0 회 | [인쇄] p.2 · p.4 · p.7 |
| ⑩ ★ 2D ↔ 3D | 2D 를 고른 이유 = 계산 자원 (*"Practical limitations for needed computational resources make full three-dimensional simulations impractical for parametric studies"*, p.14) · 2D 의 인공물을 스스로 적음: *"The fracture effects are exaggerated in a 2D model because the cracks propagate infinitely in the out-of-plane direction."* (p.12) · 과대 예측의 원인 첫째로 *"using a 2D model"* (p.11) | [인쇄] p.9 · p.11 · p.12 · p.14 |
| ⑪ ★ 압력을 뺄 때 (탈압) | **다루지 않음** — 압력은 운전 내내 일정 (0 · 5 · 40 MPa) · 성형 가압 · 탈압 · 잔류 응력은 넣지 않았고 *"These residual stress effects are the focus of ongoing studies."* (p.9) · 낱말 *unload · springback* 0 회 | [인쇄] p.9 |

⛔ **한정어 (떼지 말 것)**: ① **2D 평면 변형** — 균열이 면 밖으로 무한히 이어진 것으로 계산된다 (저자 스스로 "exaggerated") ② **선형 탄성 · 작은 변형** — SE 의 소성 유동 · 응력 이완 없음 ③ **출발 = 무응력** — 성형압 · 잔류 응력 · 탈압 이력 없음 ④ **계면 G_c 1.0 J m⁻² 와 ℓ₀ 100 nm 는 가정값** (측정 없음 · 보정 없음) 이고 결과는 이 둘에 문턱처럼 걸린다 (G_c 1.0 → 2.0 에서 150.7 → 185.8) ⑤ 용량 숫자는 전부 **[판독]** (원문 본문 인쇄값은 "186 mAh g⁻¹" 하나) ⑥ 검증은 **전압 곡선 한 벌** — 압력 · 공극 · 계면 인성 · LLZO 대조에는 실험이 없다 ⑦ "공극 15 %" 는 **손으로 고친 2D 그림의 면적 분율** — 질량 · 진밀도 기공이 아니다 ⑧ 재료 값은 다른 재료에서 온 것이 섞여 있다 (LPSC G_c = 70Li₂S–30P₂S₅ **유리**의 파괴 인성에서 · LPSC E = DFT).

⇒ **절대값 전이: 안 된다.**  용량 · 전압 수치는 2D · 가정 물성 · 과대 예측 (+5–14 %) 위의 모형 출력이라 우리 값 옆에 나란히 놓을 수 없다.  옮길 수 있는 것은 (i) **식 구조** (손상이 반응 · 확산 · 강성을 한꺼번에 끄는 방식 · 응력이 화학 퍼텐셜과 과전압에 들어가는 항) (ii) **재료 표의 출처 사슬** (어느 값이 어디서 왔고 어느 값이 가정인지) (iii) **방향** — 압축 상태가 계면 분리를 줄인다 · 공극이 응력을 풀어 준다 · 2D 는 분리 효과를 부풀린다 (iv) **이 계열 모형이 비워 둔 입력** = 성형 뒤 잔류 응력과 계면 상태 (우리 단계 5 · 6 이 내야 할 것).

## 0-1. ★ 고른 의도 대조 (후보 표 N-52 의 '왜' 칸)

> 의도 (후보 표 그대로): *"조건 R2 · R7 (배치 표기 j · m) — 고체전지 복합 양극의 전기화학-기계 결합 모델: 계면 분리 · 균열 (다른 카드의 2 차 인용뿐 — lei2026 = 2D FEM · 계면 분리 최대 틈 · liang2026 = FEM phase-field fracture) · 구성식 · 재료 · 검증은 원문 확인 필요"*

| 의도의 문장 | 판정 | 원문 위치 · 값 · 계산 조건 |
|---|---|---|
| "고체전지 복합 양극의 전기화학-기계 결합 모델" | **채움** | NMC811 + Li₆PS₅Cl 복합 양극 반쪽 셀 · Li 보존 (19) + 전하 보존 (25)(26) + 힘 평형 (27) + phase-field (34) 를 한 계로 푼다 (p.3–9) · 응력 → 확산 (24) · 응력 → 반응 (40) · 손상 → 반응 (39) · 확산 (21) · 강성 (28) 의 양방향 결합 |
| "계면 분리" (R2) | **일부** | 분리는 **손상 변수 ξ 의 띠** 로만 나온다 (계면 G_c 1.0 J m⁻² [가정] · ℓ₀ 100 nm · 손상 그림 Fig. 9b · c · 10b · c · 14b · c · A.2).  변위의 불연속 (틈 nm) · 미끄럼 · 마찰 · 다시 닿은 뒤의 반응 회복은 **없다** — 손상된 띠는 압축 부피 강성만 남고 전단 · 인장은 0 (식 28) · 교환 전류는 (1 − ξ)² 로 꺼진 채 (식 39) · 조건 = 운전 중 일정 적층압 0 / 5 / 40 MPa · 300 K · 출발 무응력 |
| "균열" (R7 = AM 파괴) | **일부** | NMC 에 G_c 2.5 J m⁻² (Lim 2017) 를 줘서 입자 내부 손상이 가능하지만, 결과 서술은 *"cracks are mainly concentrated at the electrode-electrolyte interfaces"* (p.12) 이고 NMC 는 등방 연속체 (1 차 입자 방위 · 입계 없음) — *"neglecting factors such as randomly oriented primary-secondary morphology, inter-granular fracture"* (p.11) · *"future models should … incorporate the fracture mechanism within the polycrystalline NMC particles"* (p.13) |
| lei2026 = "2D FEM" | **채움 (차원만)** | *"The proposed two-dimensional (2D) model"* (p.3) · 평면 변형 (p.9) |
| lei2026 = "계면 분리 최대 틈" (L115 의 9.3 · 16.0 · 13.8 nm @ r_s 0.5 · 1.5 · 3.0 µm · 단결정 · 다결정) | **없음** | 이 논문에는 **nm 단위 분리 틈 · 입자 반지름 사다리 · 단결정 ↔ 다결정 비교 · von Mises 응력이 하나도 없다** (본문 19 쪽 · 그림 16 개 전수 · 낱말 *nm* 은 ℓ₀ 설명에도 안 쓰임 · 응력 그림은 제1 주응력 한 장 Fig. 8c).  서론이 약속한 *"cathode particle size, cathode-particle crystallinity"* 조사도 결과 절에 없다 (§3-11 ⑫) |
| liang2026 = "FEM phase-field fracture" | **채움** | AT-1 정칙화 (식 5) · 문턱 + 이력 장 (식 32–34) · COMSOL 유한요소 (p.9) · liang2026 L246 의 서지 (JMPS 198, 106060) 도 원문과 같다 |
| "구성식 · 재료 · 검증은 원문 확인 필요" | **채움** (한정 셋) | 구성식 = 식 (1)–(40) (§4-1) · 재료 = Table 1 (§3-2) · 검증 = Fig. 7 (§3-5).  한정: ① 검증은 전압 곡선 한 벌이고 모형이 용량을 +4.7 / +7.0 / +13.7 % 높게 낸다 [판독] ② 계면 G_c · ℓ₀ 는 가정 ③ 원문 안 표기 어긋남 16 건 (§3-11) |

**가리킨 카드의 2 차 인용 ↔ 원문** (그 카드들은 고치지 않았다 — 카드 문제로 보고):

| 카드 · 줄 | 카드에 적힌 것 | 원문 (이 논문) | 판정 |
|---|---|---|---|
| `lei2026_…` L115 | *"NMC 단결정 · 다결정 2D FEM (Taghikhani): 계면 분리 최대 틈 **9.3 nm (r_s 0.5 µm) · 16.0 (1.5) · 13.8 (3.0)** — 비단조 … [2차 · ref 166 · `Fig. 4c`]"* | 해당 값 · 그림 · 서술 없음 | **없음** — 리뷰의 ref 166 은 이 JMPS 논문이 아닌 다른 논문으로 보인다.  이 논문의 참고문헌 목록에 *Taghikhani, Weddle, Hoffman, Berger, Kee, 2023. "Electro-chemo-mechanical finite-element model of single-crystal and polycrystalline NMC cathode particles embedded in an argyrodite solid electrolyte." Electrochim. Acta 460, 142585* 이 있고 제목이 lei2026 의 서술 (단결정 · 다결정 · 입자 단위) 과 맞는다 [카드 해석 · 그 원문과 리뷰의 ref 166 서지는 미확인 — lei2026 카드에 ref 166 의 서지가 적혀 있지 않다] |
| `lei2026_…` L144 | *"(ii) 2D FEM 전기화학–기계 (Taghikhani · Jiao · Xu)"* | 2D FEM 전기화학–역학 = 맞음 (종류) | 종류는 **채움** · 어느 Taghikhani 논문인지는 위와 같은 문제 |
| `lei2026_…` L172 | *"(c) NMC 입자 r_s 0.5 · 1.5 · 3.0 µm 의 Li 농도 · von Mises … (c) [166]"* | 그런 그림 없음 (Fig. 8b = 전극 전체의 Li 농도 · Fig. 8c = 제1 주응력) | **없음** |
| `liang2026_…` L246 | *"FEM phase-field fracture(복합양극 **[97]** Taghikhani et al., *JMPS* **198**, 106060)"* | 맞음 | **채움** |
| `zhang2026_polymer_…` L124 | ref 162 서지 전문 + *"ASSB 복합양극 전기화학-기계 결합 모델"* | 저자 6 명 · 제목 · 권 · 논문 번호 모두 원문과 같다 | **채움** |

⇒ **의도 대조 결과: 일부** — 전기화학–역학 결합 2D 유한요소 phase-field 모형 · 구성식 · 재료 표 · 검증 곡선은 **채움**; 계면 분리는 손상 변수로만 (틈 · 미끄럼 없음) · AM 파괴는 사실상 계면뿐이라 **일부**; lei2026 이 적은 "계면 분리 최대 틈 9.3 / 16.0 / 13.8 nm" 는 이 논문에 **없음** (다른 Taghikhani 논문일 가능성 — 후보 표 근거 칸의 귀속 문제).

## 1. 한 줄 요약

Bielefeld 2020 · 2022 의 미세구조 분해 전기화학 모형에 **역학과 phase-field 파괴를 얹은** 2D 유한요소 모형이다 — 충전 (탈리튬) 으로 NMC 가 줄어들면 NMC–LPSC 계면에 인장이 걸려 손상 띠가 생기고, 그 띠에서는 반응 · 확산이 꺼져 용량이 준다는 사슬을 **운전 적층압 · 공극 · 계면 인성 · SE 종류 · 사이클** 다섯 축으로 돌려 본 것.  결과는 정성 지침 (압력 · 계면 코팅 · 공극의 절충) 으로 읽어야 하고 (*"important qualitative insights"*, p.15), 압밀 · 소성 · 탈압은 범위 밖이다.

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 · 소속 | Kasra Taghikhani (교신) · William Huber · Mohsen Asle Zaeem · J. R. Berger · Robert J. Kee (Colorado School of Mines, Dept. of Mechanical Engineering) · Peter J. Weddle (NREL) |
| 학술지 | *Journal of the Mechanics and Physics of Solids* 198 (2025) 106060 · DOI 10.1016/j.jmps.2025.106060 · 접수 2024-12-02 → 수정 2025-01-28 → 수락 2025-01-29 → 온라인 2025-02-06 · CC BY-NC-ND |
| 분량 · 구성 | 19 쪽 (본문 p.1–16 · 참고문헌 p.17–19) · 그림 14 + 부록 그림 A.1 · A.2 · 표 1 · 번호 붙은 식 40 · 보충 자료 없음 |
| 절 | 1 Introduction / 2 Model formulation and implementation (2.1 Fracture energy · 2.2 Elastic strain energy · 2.3 Chemical energy · 2.4 Thermodynamics · 2.5 Governing equations [2.5.1 Transport · 2.5.2 Mechanics · 2.5.3 Phase-field fracture] · 2.6 Initial and boundary conditions [2.6.1 Transport · 2.6.2 Mechanics and fracture] · 2.7 Implementation and model parameters) / 3 Results and discussion (3.1 Validation · 3.2 Li concentration and stress profiles · 3.3 External pressure dependence · 3.4 Sensitivity to electrolyte material properties · 3.5 Effect of interfacial strength · 3.6 Cycling behavior · 3.7 Porosity) / 4 Summary and conclusions / Appendix |
| 저자 기여 (p.15) | Taghikhani = 초고 · 소프트웨어 · 방법 · 가시화 · 개념 / Huber = 방법 · 형식 해석 / Weddle = 개념 · 자원 / Asle Zaeem = 형식 해석 / Berger · Kee = 감독 · 연구비 |
| 1저자 메모와의 대조 | 저자 6 명 · 제목 · 학술지 · 권 198 · 논문 번호 106060 · 연도 2025 · DOI — **전부 원문과 같다 (다른 점 없음)**.  후보 표의 "(DOI 카드에 없음)" 은 원문 p.1 에서 채움 |
| 글의 꼴 | 모형 정식화 (p.3–10 · 식 40 개) 가 절반 · 결과는 조건당 전압–용량 곡선 한 장 + 손상 색 지도 · 균열 길이 · 활성 면적 손실 같은 정량 표는 없다 |
| 그룹 맥락 | 같은 저자의 선행 = 흑연 · NMC811 다결정 입자의 화학–역학 (2020 · 2021b) · argyrodite 에 박힌 단결정 / 다결정 NMC 입자 유한요소 (2023 · *Electrochim. Acta* 460, 142585) · 평면 변형 ↔ 평면 응력 가정의 결과 (2024 · *Electrochim. Acta* 479, 143790) — 이 논문은 그것을 전극 규모 (입자 ≈125 개) 로 넓힌 것 [원문 p.6 · p.9 · p.10 의 자기 인용] |

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 계산 영역 · 미세구조 (p.5–6 · p.11 · Fig. 3 · 4 · `fig_3.png` · `fig_4.png` · `txt_p6_microstructure_segmentation_illustrator_im2mesh.png` · `txt_p11_model_size_validation_overprediction_2d.png`)

- **영역** [인쇄 p.11]: *"The half-cell 2D model consists of a (40 × 40) μm² composite cathode structure with a 10 μm solid-electrolyte separator and a 1 μm current collector (Fig. 3). The particle and void distributions are random, with variable void sizes and related active surface areas."*  대극 (Li) 은 모형에 없다 — 분리막 왼쪽 면에 전위 0 과 압력을 준다.
- **출처** [인쇄 Fig. 3 캡션 · p.6 · p.15]: *"Heterogeneous composite cathode structure with ≈15% porosity is developed based on a scanning-electron-microscopy (SEM) image reported by Doerrer et al. (2021)"* · *"The figure is edited and phase-segmented using Adobe Illustrator and im2mesh. The porosity and particle sizes have adjusted to match values reported by Bielefeld et al. (2022)."* → **실측 단면이 아니라 손으로 고친 그림**이다.  [다른 카드 `doerrer2021_…`] 그 SEM 은 **단결정** NMC83 (D50 3.4 µm) 70 : LPSCl 27.5 : C65 2.5 wt% 를 500 MPa 로 누른 양극 (상대밀도 ≈0.90) 인데, 이 논문은 그 윤곽을 등방 "다결정 2 차 입자" 로 쓰고 공극을 ≈15 % 로 맞췄다.
- **상 면적 분율** [판독 · Fig. 3 에 박힌 래스터 823 × 664 px · 40 µm = 650 px → 16.25 px µm⁻¹ · 색 분류 · 집전체 왼쪽 40 µm 구간]: 공극 (흰색) **12.5 %** · SE (노랑) **24.2 %** · AM (회색) **49.1 %** · 검은 윤곽선 8.5 % · 나머지 (경계 번짐) 5.7 % → 윤곽선 · 나머지를 빼고 다시 나누면 **공극 14.5 % · SE 28.2 % · AM 57.3 %** (인쇄 "≈15 %" 와 맞는다) · AM ÷ (AM + SE) = **67 %** (면적) · 경계: 윤곽선을 전부 AM 으로 치면 AM 63 % · 전부 SE 로 치면 SE 38 %.  분리막 폭 = 9.6 µm (차이로).
- **입자 · 공극 크기** [판독 · 같은 래스터의 연결 성분 · 등가 원 지름]: AM 조각 **125 개** · 지름 0.6–8.2 µm · 중앙 **2.0 µm** · 면적 가중 중앙 **3.9 µm** / 공극 **87 개** · 0.4–3.0 µm · 중앙 **1.5 µm** · 면적 가중 중앙 **2.1 µm** (윤곽선을 빼서 조금 작게 읽힌다 · 2D 단면 · 원문은 입도 통계를 인쇄하지 않았다).
- **경계 모양** [판독 Fig. 5 · 6 확대]: AM 윤곽은 매끈한 곡선인데 **공극 경계는 계단 꼴** (화소 경계가 그대로 격자가 됨) — 오목한 모서리의 응력 집중이 균열 시작점을 정할 수 있다 [카드 해석 · 원문 말 없음].  공극 자리는 요소가 없는 구멍이다 (Fig. 6).
- **탄소 · 바인더**: 따로 그리지 않는다 — *"The present model does not explicitly include a conductive-carbon phase within the electrolyte phase. The effects of a percolating electrically conductive carbon-binder phase are implicitly captured as part of the composite electrolyte structure."* (p.6) · *"assumes that electronic conduction is not a limiting factor … and assumes a relatively high electronic conductivity for NMC particles"* (p.7).
- [카드 산술] 면적 분율을 부피 분율로 보면: AM 면적 적재 = 40 µm × 0.573 × 4.77 g cm⁻³ ≈ **10.9 mg cm⁻²** (경계 9.4–12.1) → 186 mAh g⁻¹ 이면 ≈2.0 mAh cm⁻² · AM : SE = 67 : 33 (면적) 은 ρ_NMC 4.77 · ρ_SE 1.64 g cm⁻³ (우리 랩 표준 진밀도 — 원문은 SE 밀도를 쓰지 않는다) 로 **AM ≈85.5 wt%** 에 해당 — Doerrer 원 전극 (70 wt%) 보다 훨씬 AM 이 많은 기하다.

### 3-2. ★ 재료 값 표 — Table 1 "Model parameters." 전사 (p.10 · `tab_1.png`)

| 묶음 | 매개변수 (원문 표기 · 인용) | 기호 | 값 | 단위 |
|---|---|---|---|---|
| 공통 | Anodic symmetry factor | α_a | 0.5 | – |
| 공통 | Cathodic symmetry factor | α_c | 0.5 | – |
| 공통 | Universal gas constant | R | 8.314 | J mol⁻¹ K⁻¹ |
| 공통 | Faraday's constant | F | 96 485.33 | C mol⁻¹ |
| 공통 | Temperature | T | 300 | K |
| 공통 | **Interface critical energy release rate** (출처 없음) | G_c | **1.0** | J m⁻² |
| 공통 | **Phase-field characteristic width** (출처 없음) | ℓ₀ | **1 × 10⁻⁷** | m |
| 공통 | Initial intercalation fraction (Bielefeld et al., 2022) | x₀ | 0.9729 | – |
| 공통 | Cut-off voltage (Bielefeld et al., 2022) | V_Cutoff | 4.2 | V |
| NMC | Electronic conductivity (Bielefeld et al., 2022) | K_ed | 100 | S m⁻¹ |
| NMC | Mass density (Bielefeld et al., 2022) | ρ | 4770 | kg m⁻³ |
| NMC | Maximum Li concentration (Mele et al., 2020) | [Li]_max | 51.554 | kmol m⁻³ |
| NMC | Young's modulus (Taghikhani et al., 2024) | E | **175.27** | GPa |
| NMC | Poisson's ratio (Taghikhani et al., 2024) | ν | 0.2819 | – |
| NMC | Critical energy-release rate (Lim et al., 2017) | G_c | **2.5** | J m⁻² |
| NMC | Chemical-expansion-coefficient (Taghikhani et al., 2024) | β^iso | 1.5759 × 10⁻⁷ | m³ mol⁻¹ |
| LPSC | Ionic conductivity (Ruess et al., 2020) | K_el | **0.7** | mS cm⁻¹ |
| LPSC | Young's modulus (Deng et al., 2015) | E | **22.1** | GPa |
| LPSC | Poisson's ratio (Deng et al., 2015) | ν | **0.37** | – |
| LPSC | Critical energy release rate (McGrogan et al., 2017) | G_c | **2.785** | J m⁻² |
| LLZO | Ionic conductivity (Zhang et al., 2015) | K_el | 0.33 | mS cm⁻¹ |
| LLZO | Young's modulus (Ni et al., 2012) | E | 149.8 | GPa |
| LLZO | Poisson's ratio (Ni et al., 2012) | ν | 0.257 | – |
| LLZO | Critical energy release rate (Ni et al., 2012) | G_c | 9.7416 | J m⁻² |

- 표에 **없는 것**: 확산 계수 · 교환 전류 · 평형 전위 (농도 함수 — Fig. A.1) · SE 영역의 전자 전도도 (탄소를 "암묵적으로" 넣었다는 값) · 집전체 물성 · 1 C 전류의 정의 · NMC 의 방향성 (등방으로 평균) — [미확인].
- 본문 값과의 차이: LPSC G_c 는 본문 · Fig. 5 캡션에서 **2.79** (표 2.785) · 초기 x 는 본문 **0.97** (표 0.9729).
- 출처의 정체 [다른 카드]: LPSC E 22.1 · ν 0.37 = `deng2016_elastic_superionic_electrolytes_dft` 의 **DFT** 값 (그 카드: Li₆PS₅Cl B 28.7 · G 8.1 · E 22.1 GPa — 이 논문은 "Deng et al., 2015" 로 인용 · J. Electrochem. Soc. 163 (2), A67) · LPSC G_c 의 인용처 `mcgrogan2017_…` 는 **70Li₂S–30P₂S₅ 유리**의 E 18.5 ± 0.9 GPa · K_Ic 0.23 ± 0.04 MPa·m^½ (Vickers 9.8 N) 를 잰 논문 — **argyrodite 값이 아니고**, 2.785 를 어떻게 얻었는지는 인쇄되지 않았다 ([카드 산술] K²/E = 0.23² / 18.5 = 2.86 J m⁻² · 2.785 가 되려면 E ≈ 19.0 GPa) [미확인].  NMC G_c 2.5 (Lim 2017 · Sci. Rep. 7, 39669) · NMC E · ν · β (Taghikhani 2024) 는 그 원문을 보지 못했다.
- *"these parameters are assumed to be constant to reduce the computational cost … However, in reality, the properties may vary with concentration"* (p.10) · *"there is evidence that they [G_c] can depend on Li concentration and cycling (Xu et al., 2017; Taghikhani et al., 2023)"* (p.9).

### 3-3. 농도 의존 물성 — Fig. A.1 (p.16 · `fig_A1.png` · `fig_A1a.png` · `fig_A1b.png` · `fig_A1c.png` · 캡션 *"Reproduced with permission from Bielefeld et al. (2022)"*)

| 물성 | 표지 수 [판독] | 모양 [판독 · 표지 중심] |
|---|---|---|
| (a) 확산 계수 D — 축 *"D × 10⁻¹⁶ (m² s⁻¹)"* | 25 | x 0.22 에서 0.15 → 0.28 에서 3.35 → 0.31–0.38 에서 ≈3.5–3.8 → **최고 6.85 (x 0.465)** → 0.55–0.77 에서 ≈3.2–3.8 → 0.80 에서 1.90 → 0.83 에서 0.44 → 0.85 에서 0.21 → **x ≥ 0.88 에서 ≈0.05–0.10** (마지막 표지 x 0.943) — 최고 ÷ 최저 ≈125 배 |
| (b) 교환 전류 밀도 i₀ — 축 *"i₀ × 10⁻¹⁰ (A m⁻²)"* | 25 | x 0.25 에서 3.45 → **최고 15.4 (x ≈0.61–0.64)** → 0.73 에서 12.9 → 0.81 에서 7.5 → 0.89 에서 3.7 → 0.98 에서 1.7 — ⚠ 눈금 숫자에 10⁻¹⁰ 을 곱하는지 나누는지, 그리고 단위가 맞는지는 축 표기만으로 정할 수 없다 [미확인] |
| (c) 개회로 전압 (V vs. Li⁺/Li) | 29 | x 0.221 에서 4.220 → 0.248 에서 4.189 → 0.40 에서 4.00 → 0.52 에서 3.87 → 0.61 에서 3.80 → 0.76 에서 3.71 → 0.91 에서 3.62 → 0.968 에서 3.59 → 그 뒤 급락 (0.979 에서 3.02 · 0.994 에서 2.69) · **4.2 V 가 되는 x ≈0.238** [카드 산술 · 두 표지 사이 선형 보간] |

- D 축의 숫자를 10⁻¹⁶ m² s⁻¹ 단위로 읽으면 D = 5 × 10⁻¹⁸ – 6.9 × 10⁻¹⁶ m² s⁻¹ [카드 해석].  [우리 · CLAUDE.md STEP4 절] 우리 STEP4 의 다결정 NCM 확산 계수 띠 4 × 10⁻¹⁵ – 3 × 10⁻¹⁴ m² s⁻¹ 보다 한두 자릿수 낮다 (정의 · 입자 반지름 규약 대조 전 — 원전 = Bielefeld 2022 · Ruess 2020 · 둘 다 카드 없음).
- 농도 의존 물성의 출처는 본문에서 *"(Ruess et al., 2020; Bielefeld et al., 2022)"* (p.10) — 이 논문 자체의 측정은 없다.

### 3-4. ★ 수치 구현 (p.7–9 · p.16 · Fig. 5 · 6 · A.2 · `txt_p9_implementation_dof_length_scale_mesh.png` · `txt_p7_threshold_linear_solution_factor_9_8.png` · `txt_p16_appendix_mesh_vs_length_scale.png`)

- **풀이기** [인쇄 p.9]: *"The system of fully coupled differential–algebraic equations is solved numerically using the finite-element method embedded in COMSOL Multiphysics. The quadratic triangular mesh structure consists of approximately 3.5 million degrees of freedom. Considering the size of the problem, the model is solved using a segregated solver."*  종속 변수 = Li 농도 [X] · 변위 u_i · 전극 전위 Φ_ed · 전해질 전위 Φ_el · 손상 ξ (p.6).
- **길이 척도** [인쇄 p.9]: *"The value of length scale parameter ℓ₀ is critical in strength-dominated phase-field problems, particularly in scenarios with small or non-existent initial defects. In the absence of empirical data on strength of materials, the parameter selection relies on reasonable approximations aligned with available estimates in the literature (Xu et al., 2019; Bai et al., 2020; Wu et al., 2016). The selected parameter aims to balance accuracy with computational efficiency, while recognizing the inherent limitations of the model."* → ℓ₀ 100 nm 는 **강도 자료 없이 고른 값**이다.
- **격자** [인쇄 p.9 · p.16]: 계면에서 *"the maximum element mesh size h_max is less than half of the crack length-scale parameter (h_max < 0.5 ℓ₀)"* · *"the elements are generally about 4–5 smaller than the length scale parameter in the model (c.f., Fig. A.2)"* · 분리막은 성긴 격자 (Fig. 6).  **요소 수 · 격자 수렴 시험 · 시간 간격 · 허용 오차 · 계산 시간 · 기계는 인쇄되지 않았다** [미확인].
- **G_c 를 퍼뜨리는 법** [인쇄 p.9]: *"The critical energy release rates are distributed by solving the phase-field equation. The length scale parameter is selected to match the characteristic width ℓ₀"* — 계면의 1.0 이 폭 ℓ₀ 로 번져 NMC 2.5 · LPSC 2.79 로 이어진다 (Fig. 5 색 막대 눈금 1.0–2.6 · 위 끝 ≈2.8 [판독]).
- **문턱 + 이력 장** [인쇄 p.7–8]: 부등식 (31) 을 그대로 풀지 않고 문턱 에너지 (32) 와 이력 장 (33) 으로 **선형 식 (34)** 을 엇갈림 (staggered) 풀이에서 푼다 — *"While this solution procedure is efficient … because it makes the phase-field equation linear, it does not lead to a profile which solves the Euler–Lagrange equations of the energy functional. In computations, the energy release rate ought to be corrected by a factor of 9∕8."* 이어서 1D 문제 (35)–(37) 로 *"leads to an overestimation of fracture dissipation by a factor of 15∕8√2"* (= 1.326 [카드 산술]).  두 인자 (9/8 ↔ 15/(8√2)) 가 따로 인쇄돼 있고, Table 1 의 G_c 가 보정된 값인지는 [미확인].
- [카드 산술 · 어림] 자유도로 본 격자: 2 차 삼각 요소는 요소당 절점 ≈2 개 · 절점당 미지수 4–5 개 → 요소 ≈3.5 M ÷ 9 ≈ 39 만 개 · 영역 (51 × 40 µm² 에서 공극 제외) ÷ 39 만 → 고르게 나누면 한 변 **≈0.10 µm ≈ ℓ₀**.  계면 전체 (AM 조각 125 개의 등가 원 둘레 합 ≈950 µm) 의 ±L₀ 띠 (폭 0.4 µm) 를 h = 50 nm 로 채우는 데만 ≈3.2 M 자유도가 든다 — "계면 띠에서 h < 0.5 ℓ₀" 는 좁은 띠에서만 성립할 수 있고 *"generally about 4–5 smaller"* (h ≈ 20–25 nm) 는 3.5 M 자유도로는 띠 전체에서 성립하기 어렵다 (가정: 정삼각형 · 띠 폭 · 둘레 어림 — 확인 불가).
- [판독 · 거칢] Fig. A.2 (눈금 막대 없음): ξ = 1 인 붉은 띠가 요소 2–3 개 폭이고 ξ 1 → 0 전이가 요소 1–2 개 폭이다.  식 (36) 의 해석 프로파일은 ξ = 0.1 까지 1.63 L₀ = 326 nm [카드 산술: L₀·ln 10 / √2] 이므로 요소가 ℓ₀ 의 1/4–1/5 이면 전이가 요소 13–16 개에 걸쳐야 한다 — **그림과 "4–5 배 작다" 는 문장이 함께 성립해 보이지 않는다** (그 문장의 근거로 제시된 그림이다 · 확정 불가).

### 3-5. 검증 — Fig. 7 (p.11 · `fig_7.png` · p = 40 MPa · digitized.csv fig7)

| 전류 (모형 범례) | 실험 끝 (4.2 V) [판독] | 모형 끝 [판독] | 차 | 용량 50 mAh g⁻¹ 에서의 전압 — 실험 / 모형 [판독] |
|---|---|---|---|---|
| 0.02 C | 194.6 mAh g⁻¹ | 203.8 | +9.2 (**+4.7 %**) | 3.706 / 3.719 V |
| 0.1 C | 171.7 | 183.8 | +12.1 (**+7.0 %**) | 3.749 / 3.768 V |
| 빠른 전류 — 범례 *"Simulation - 0.5 C"* · 캡션 · 본문 *"5 C"* | 112.9 | 128.4 | +15.5 (**+13.7 %**) | 3.895 / 3.896 V |

- 실험 곡선 셋은 같은 실선 (범례 "Experiment" 하나) 이라 어느 곡선이 어느 전류인지는 가까운 모형 곡선과 짝지었다 [카드 해석].  **실험 조건 (셀 구성 · 조성 · 적층압 · 온도) 은 이 논문에 없다** [미확인] — 캡션은 Bielefeld 2022 재수록, 본문은 *"the experimental work reported by Janek and coworkers (Ruess et al., 2020; Trevisanello et al., 2021; Conforto et al., 2021)"*.
- 빠른 전류의 정체 [카드 해석]: (i) 같은 용량 50 mAh g⁻¹ 에서 모형 전압이 0.02 → 0.1 C 에서 +49 mV, 0.1 C → 빠른 전류에서 +128 mV 높다 (실험도 +43 · +146 mV) [판독] — 전류 5 배씩의 사다리로는 자연스럽고 50 배 (5 C) 로는 너무 작다 (α = 0.5 의 Tafel 항만으로도 2RT/F·ln 50 = 202 mV · 300 K [카드 산술]) (ii) 입자 확산 시간 r² / D ≈ (2 µm)² / 3.5 × 10⁻¹⁶ m² s⁻¹ ≈ 1.1 × 10⁴ s ≈ 3.2 h [카드 산술 · r = 판독 면적 가중 중앙 지름 3.9 µm 의 절반 · D = Fig. A.1a 평탄부] 는 5 C 의 충전 시간 0.2 h 보다 훨씬 길어 128 mAh g⁻¹ (Δx 0.44) 를 내기 어렵다 → **범례의 0.5 C 쪽이 맞아 보인다.**  원문 대조 (Bielefeld 2022) 전에는 확정하지 않는다.
- 저자 해석 [인쇄 p.11]: *"the simulations consistently over-predict the capacity for all three charging rates. Although the trends are well predicted, the quantitative discrepancies are likely due to model simplifications, including using a 2D model, the assumption of isotropic behavior in cathode particles, and neglecting factors such as randomly oriented primary-secondary morphology, inter-granular fracture, and formation of resistive cathode-electrolyte interphase (CEI) layer."* · *"the discrepancies between simulation and experiment increases at higher C-rates. This behavior might be attributed to the faster formation CEI layer at higher charging rates."*
- [카드 산술] 용량의 질량 기준은 인쇄되지 않았다.  Table 1 로 계산하면 x 한 단위 = [Li]_max·F / (ρ·3.6) = 51 554 × 96 485.33 / 4770 / 3.6 = **289.7 mAh g⁻¹** → 0.1 C 끝 185.7 은 Δx 0.641 (평균 x 0.332) · 0.02 C 끝 203.8 은 Δx 0.704 (평균 x 0.269) · 평형 한계 (x₀ 0.9729 → 4.2 V 의 x 0.238) = Δx 0.735 = 212.9 mAh g⁻¹.  (식량 97.28 g mol⁻¹ 로 세면 x 한 단위 = 275.5 mAh g⁻¹ 이고 평형 한계가 202.5 로 0.02 C 모형 끝값 203.8 보다 작아져 모순 → 저자의 분모는 [Li]_max / ρ 로 보인다 [카드 해석].  ρ / [Li]_max = 92.5 g mol⁻¹ 은 NMC811 식량과 5 % 어긋난다.)

### 3-6. ★ 적층압 · 공극 · 계면 인성 · SE 종류 — 값과 조건 (p.12–14 · Fig. 8–12 · 14 · digitized.csv)

공통 조건: 0.1 C 정전류 충전 → 4.2 V 차단 · 300 K · x₀ 0.9729 · 출발 무응력 · ξ = 0 · 압력 = 왼쪽 경계의 일정 견인력 · 위 · 오른쪽 · 아래 롤러 · 2D 평면 변형.  용량은 전부 **[판독]** (벡터 꼭짓점 · 눈금 보정 · 읽기 오차 ≈±0.2 mAh g⁻¹ · ±1 mV).

| 조건 (모형 입력) | 그림 | 끝 용량 @ 4.2 V (mAh g⁻¹) | 곡선에서 읽은 것 | 손상 (원문 그림 · 문장) |
|---|---|---|---|---|
| **기준**: 40 MPa · 공극 "≈15 %" · 계면 G_c 1.0 · LPSC | Fig. 8a · 10a / 7 / 11 / 14a | **185.7–185.8** / 183.8 / 186.4 / 184.1 | 매끈 · V@100 = 3.858–3.861 · V@150 = 4.021–4.027 · ⚠ 같은 명목 조건인데 그림마다 끝값이 183.8–186.4 로 다르다 | *"Due to the lower fracture toughness, the cracks are mainly concentrated at the electrode-electrolyte interfaces"* (p.12) — Fig. 10c · 14b 에 가는 균열 몇 줄 |
| **무압 (0 MPa)** · 그 밖 같음 | Fig. 9a · 10a · 12 | **150.7** (기준 대비 −35.0 · **−18.8 %**) | Q ≈103 까지 40 MPa 곡선과 겹친 뒤 **계단 셋**: Q 103.2 (3.873 → 3.899–3.904 V) · 122.0–124.0 (3.978 → 4.038 V) · 127.7–128.9 (+14 mV) · V@125 = 4.037 (기준 +100 mV) | Fig. 9b → c: 분리막 쪽에서 공극과 공극을 잇는 계면 균열이 계단 앞뒤로 자람 · Fig. 10b: 충전 끝에 전극 전체로 퍼짐 · *"The simulation profile predicts sudden jumps, which are not observed experimentally."* (p.12) |
| **5 MPa** (사이클 런의 첫 충전) | Fig. 13 | CC 끝 **185.6** (CV 300 s 뒤 187.2) | 40 MPa 사이클 런 (186.5 · 188.3) 과 ≈1 mAh g⁻¹ 차 · V@100 = 3.859 (40 MPa 3.858) | 손상 그림 없음 |
| 무압 · **계면 G_c 0.2** (범례 · 본문은 0.5) | Fig. 12 | **145.6** | 계단 Q 82.6–83.8 (3.832 → 3.865 V) · V@100 = 3.937 | 그림 없음 |
| 무압 · **계면 G_c 2.0** | Fig. 12 | **185.8** | **기준 (40 MPa · G_c 1.0) 곡선과 다섯 점에서 1 mV 안으로 같다** (V@50 / 100 / 125 / 150 / 175 = 3.764 / 3.859 / 3.937 / 4.021 / 4.132) | 그림 없음 · *"adding a coating layer to strengthen the bond … could substantially improve the capacity"* (p.14) |
| 40 MPa · **공극 0 %** ("No pores") | Fig. 14a · c | **≈190–191** (래스터 끝점 190.1 @ 4.195 V · 기준 184.1 대비 +3–4 %) | V@50 = 3.753 (15 % 구조보다 −11 mV) | Fig. 14c: 계면을 따라 수십 µm 길이 균열 여러 줄 · *"The porous structure exhibits significantly less fracture, since the pores act as a stress relieving interface."* (p.14) |
| 40 MPa · **SE = LLZO** | Fig. 11 | **181.4** (LPSC 186.4 대비 −5.1 · −2.7 %) | V@50 = 3.771 (LPSC 3.764) · V@175 = 4.159 (LPSC 4.133) | 그림 없음 · *"LLZO, on the other hand, exhibits more pronounced fracture at higher voltages."* (p.13) |
| (실험 · Bielefeld 2022 재수록 · 0.1 C) | 전 그림 | 171.7 | V@100 = 3.857 · V@150 = 4.077 · 계단 없음 | — |

- **압력** [인쇄 p.13]: *"The application of external pressure induces a more compressive stress state, which consequently limits fracture compared to the no-pressure scenario."* 그리고 한계 고백: *"It is notable that the present model has limitations in evaluating the effects of changing external pressure. Modifying the pressure results in only slightly changes to the voltage profiles. To capture this effect, future models should include a larger region of interest or incorporate the fracture mechanism within the polycrystalline NMC particles."* → 판독도 같은 말을 한다: **0 MPa 만 다르고 5 · 40 MPa 는 거의 같다.**
- [카드 해석] 압력 응답은 **문턱형**이다 — (i) 5 ↔ 40 MPa 가 겹치고 (ii) 무압에서 계면 G_c 를 2 배로만 해도 기준 곡선과 겹치고 (iii) G_c 를 1/5 로 낮춰도 150.7 → 145.6 (−3 %) 밖에 안 변한다.  문턱 에너지 (식 32) 가 계면에서 1.875 MJ m⁻³ [카드 산술], G_c 2.0 이면 3.75 MJ m⁻³ — 충전 끝까지 계면 구동 에너지가 그 사이에 머문다는 뜻으로 읽힌다.  선형 탄성 중첩으로는 5 MPa 의 압축 편향이 화학 변형 응력 (Fig. 8c 눈금 −200 … 800 MPa) 보다 두 자릿수 작으므로, 0 ↔ 5 MPa 의 큰 차는 문턱 근처 거동이거나 무압 = 왼쪽 면 자유라는 경계 조건의 효과일 수 있다 — 원문은 기전을 가르지 않았다.
- **SE 대조** 는 한 번에 세 가지가 바뀐다 (K_el 0.7 → 0.33 mS cm⁻¹ · E 22.1 → 149.8 GPa · G_c 2.785 → 9.7416 J m⁻²) — 저자 결론 *"LPSC performs slightly better … due to more compliant structure, and higher ionic conductivity"* (p.15) 의 두 원인은 분리되지 않았다.  곡선 시작부터 LLZO 가 +7 mV 높은 것은 이온 저항 쪽 신호다 [카드 해석].
- **공극** [인쇄 p.14]: *"ASSBs composite cathode porosity can range from approximately 6% to 30%, depending on the material and fabrication process (Bielefeld et al., 2020)."* · *"removing the voids increases capacity due to higher active surface areas"* · *"While voids inherently reduce initial contact area …, they can reduce cycle-induced fracture which results in improved first-cycle Couloumbic efficiencies by inhibiting crack propagation"* (효율 숫자는 없다) · *"the composite cathode porosity presents a complex trade-off"*.  서론의 *"external pressure can be applied to reach a desirable goal of 5% void volume fraction within the composite electrode structure (Kodama et al., 2020)"* (p.2) 는 [다른 카드 `kodama2020_…`] 로는 뒷받침되지 않는다 — 그 논문은 순수 Li₆PS₅Br 분말 (≤103 MPa) 이고 기공 숫자가 없다.  "6–30 %" 도 [다른 카드 `bielefeld2020_…`] 에는 없는 문장이다 (그 카드의 계산 입력은 5 · 10 · 15 · 20 %) — 원문 대조는 하지 못했다.

### 3-7. 사이클 — Fig. 13 (p.14 · `fig_13.png` · digitized.csv fig13 · 5 MPa ↔ 40 MPa · 세 사이클)

| 꺾임점 [판독] | 5 MPa | 40 MPa |
|---|---|---|
| 첫 충전 CC 끝 (4.2 V 도달) | 185.6 mAh g⁻¹ | 186.5 |
| CV 300 s 뒤 (충전 끝) | 187.2 | 188.3 |
| 전류가 뒤집힌 직후 전압 | 4.123 V | 4.121 V |
| 첫 방전 끝의 위치 (최저 전압 ≈3.50 V) | Q = 52.6 | Q = 52.5 |
| 첫 방전 용량 [카드 산술: 차] | **134.6** | **135.8** |
| 첫 사이클 효율 [카드 산술: 방전 ÷ 충전] | **71.9 %** | **72.1 %** |
| 다음 충전 시작 전압 | 3.611 V | 3.616 V |
| 2 번째 충전 / 방전 [카드 산술] | 135.5 / 135.4 | 136.7 / 136.6 |
| 3 번째 충전 / 방전 [카드 산술] | 135.4 / 135.4 | 136.6 / 136.6 |

- 원문 [인쇄 p.14]: *"Both models reach the maximum capacity of 186 mAh g⁻¹. … The simulation predicts that the most significant capacity-loss occurs during the first cycle, as the cracked surfaces reduce the active interfaces and thus impede the Li-ion transport. Capacity retention improves in the following cycles, which is consistent with the experimental findings (Doerrer et al., 2021). … Although both models perform similarly, the 40 MPa case has slightly higher capacity at the end of the second cycle. … The cycling fatigue and degradation of fracture toughness is not incorporated in the current work."*
- **규약 어긋남**: 본문은 *"1 C constant-current charge, followed by 300 s constant-voltage hold, and 0.1 C constant-voltage discharge"* 인데 그림 안 글자는 *"0.1 CCC · 300 s - CVC · 0.1 CCDC"* 다.  첫 충전 곡선이 다른 그림의 0.1 C 곡선과 겹친다 (V@100 = 3.858–3.859) → **그림 쪽 (0.1 C 충전 · 0.1 C 정전류 방전) 이 맞다** [판독].  방전 하한 전압은 인쇄되지 않았다 (판독 ≈3.50 V).
- [카드 산술] 첫 방전 끝의 평균 x = 0.9729 − 52.6 / 289.7 = **0.79** — Fig. A.1a 의 D 가 x > 0.8 에서 한 자릿수 넘게 떨어지는 구간 바로 앞이다.  **균열을 끈 대조 계산이 없어서**, 첫 사이클 손실 28 % 가운데 균열 몫과 확산 · 반응 속도 몫 (x → 1 에서 D 급감) 은 인쇄된 자료로 가를 수 없다 [카드 해석].
- [다른 카드 `doerrer2021_…`] 원문이 "일치" 라고 한 실험의 첫 사이클 효율은 단결정 NMC83 ≈85 % (2.5 · 10 MPa · 0.2 MPa 에서 ≈83 %) · 다결정 ≈70 % — 모형 72 % 는 다결정 쪽 값에 가깝고, 그 실험의 적층압 0.2 → 10 MPa 차는 2 %p 남짓이다 (재료 · 전압 창 · 온도가 다르다 — 나란히 놓을 때 표지 필수).

### 3-8. 농도 · 응력 분포 — Fig. 8 (p.11–12 · `fig_8.png` · 0.1 C · 40 MPa · 충전 끝)

- [인쇄 p.12] *"Despite the relatively slow 0.1 C rate, the Li concentration profile ranges from x = 0.25 to x = 0.70 intercalation fraction. The void distribution and crack propagation are the main factors contributing to the high concentration gradients. As highlighted in the magnified call-out, the reaction ceases at the fractured interfaces."* (색 눈금은 0.3–0.7 [판독])
- [판독 Fig. 8b · 8c · 10c · 14b] 40 MPa 에서도 균열이 없는 것이 아니다 — 전극 가운데 높이를 **가로로 (압력을 건 방향과 나란히) 잇는 균열 띠** 가 보이고, 분리막 쪽 큰 공극 옆의 한 입자는 충전 끝에도 x ≈0.7 로 남아 있다 (Fig. 8b 의 붉은 입자).  [카드 해석] 압력 축에 수직인 면의 분리는 눌려 막히지만 압력 축과 나란한 면은 옆 방향 구속 응력 (균질 어림 ν / (1 − ν)·p ≈ 23.5 MPa [카드 산술]) 만 받는다 — 한 방향 적층압이 모든 방향의 계면을 누르지는 못한다.
- [인쇄 p.12] *"The stress is highest at the electrode-electrolyte interfaces (Fig. 8c). Additionally the stress concentration at the crack-tips are illustrated in the stress call-out."* · 제1 주응력 색 눈금 **−200 … 800 MPa** [판독 · 눈금 글자].  선형 탄성이라 이 크기의 응력이 그대로 남는다 — [다른 카드 `lee2025_heckel_argyrodite_powder_densification_nanoindentation`] 의 LPSCl 나노압입 경도 1.41 GPa · [우리] MPM 항복 문턱 0.30 GPa 와 견주면 SE 가 소성으로 풀어 줄 수 있는 범위다 [카드 해석 — 정의가 다른 양들이라 방향만].

### 3-9. [카드 산술] 묶음 (원문에 없는 값 — 식 병기)

- 화학 팽창: β^iso·[Li]_max = 1.5759 × 10⁻⁷ × 51 554 = **8.12 × 10⁻³ / x 단위** (선형) → 0.1 C 충전 (Δx 0.641) 에서 선 수축 0.52 % · 부피 (3D 등방) 1.56 % · 평면 변형 모형 안에서는 면 안 두 방향만 = 면적 1.04 %.  [다른 카드 `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` · 그 카드의 그림 2a 판독] NCM-811 단위 격자 부피 변화 ≈ −1.4 % (x 0.46) · ≈ −3.9 % (x 0.25) · ≈ −6.5 % (x ≈0.15) ↔ 이 모형의 선형 β 로는 x₀ 0.9729 에서 같은 x 까지 **−1.25 % · −1.76 % · −2.0 %** [카드 산술: 3 × 8.12 × 10⁻³ × Δx] — 중간 충전 상태는 맞고 **고전압 쪽 (x < 0.3) 의 급한 수축은 절반 아래로 잡는다** (입자 표면이 x 0.25 까지 가는 계산이라 고전압 구간의 계면 인장이 실제보다 작게 들어갔을 수 있다 [카드 해석 — 판독값끼리의 비교 · 격자 값과 등방 평균의 대응은 가정]).
- 문턱 에너지 ψ^th = 3G_c / (8L₀) · L₀ = 200 nm: 계면 **1.875** · NMC 4.69 · LPSC 5.22 · LLZO 18.27 MJ m⁻³.
- 그 문턱의 일축 응력 어림 σ = √(2Eψ^th): 계면 (LPSC 강성) **≈288 MPa** · LPSC ≈480 MPa · NMC ≈1.28 GPa · LLZO ≈2.34 GPa — 강도는 √(G_c·E / ℓ₀) 로 정해지므로 **ℓ₀ 를 고른 것이 곧 강도를 고른 것**이다.
- 함축 파괴 인성 K = √(G_c·E) (평면 응력 / 평면 변형): LPSC 0.248 / 0.267 · NMC 0.662 / 0.690 · LLZO 1.21 / 1.25 MPa·m^½.
- 문턱 풀이의 소산 = 15 / (8√2) = **1.326 G_c** (균열 하나) → 입력 G_c 를 그대로 쓰면 실효 인성이 33 % 높다.
- LPSC K = E / (3(1 − 2ν)) = **28.3 GPa** · G = E / (2(1 + ν)) = **8.07 GPa** / NMC K 133.9 · G 68.4 GPa / LLZO K 102.7 · G 59.6 GPa.
- 균질 일축 변형 (옆면 롤러) 에서 40 MPa 의 옆 방향 응력 = ν / (1 − ν) × 40 = 23.5 MPa (LPSC ν 0.37) · 5 MPa 이면 2.9 MPa.

### 3-10. ★ 저자가 적은 한계 (원문 문장)

1. 잔류 응력 무시: *"The present model assumes the structure to be stress-free at the initial condition (x = 0.97). This assumption neglects the effect of residual stress developed during the fabrication process. These residual stress effects are the focus of ongoing studies."* (p.9)
2. 2D: *"The fracture effects are exaggerated in a 2D model because the cracks propagate infinitely in the out-of-plane direction."* (p.12) · *"Although the model itself is fully capable of representing three-dimensional geometries, the computation times are significant as compared to two-dimensional studies."* (p.11)
3. 압력 민감도: *"the present model has limitations in evaluating the effects of changing external pressure."* (p.13)
4. 등방 NMC · 입계 파괴 없음: *"the model does not resolve the orientation of individual primary particles"* (p.10) · *"The decohesion of primary-secondary cathode particles was previously analyzed at the particle level (Taghikhani et al., 2023) and remains a subject of ongoing and future investigation."* (p.10)
5. 길이 척도 · 강도 자료 없음 (§3-4 인용) · 물성이 상수 (p.10) · G_c 가 농도 · 사이클에 따라 변할 수 있음 (p.9) · 사이클 피로 없음 (p.14).
6. 새 표면 비활성: *"it is assumed that fracture does not lead to activation of new surfaces, as the solid electrolyte cannot infiltrate the cracks."* (p.10)
7. 공간 전하층 미해상 (p.7) · SE 안 Li 농도 일정 (p.6) · 탄소 상 암묵 (p.6) · CEI 없음 (p.11).
8. 결론의 자기 평가: *"The predictions depend on fundamental materials properties, some of which are yet to be measured and validated. Moreover, even for nominally the same battery, microscale electrode-electrolyte geometric details vary from one cell to the next. Thus, a model such as the present one, provides the means to gather important qualitative insights"* (p.15)

### 3-11. ⚠ 원문 안 어긋남 (인쇄 그대로 · 카드가 고치지 않았다)

1. p.6 *"electrode potential Φ_el, electrolyte potential Φ_ed"* ↔ 뒤의 정의 (Φ_el = 전해질 상 · Φ_ed = 전극 상) — 첨자가 뒤바뀐 문장.
2. Fig. 7 범례 *"Simulation - 0.5 C"* ↔ 캡션 · 본문 *"5 C"* (§3-5).
3. 초기 x: 본문 0.97 ↔ Table 1 0.9729.
4. LPSC G_c: 본문 · Fig. 5 캡션 2.79 ↔ Table 1 2.785.
5. 계면 G_c 사다리: 본문 §3.5 *"0.5, 1, and 2 J m⁻²"* ↔ Fig. 12 범례 0.2 · 1.0 · 2.0.
6. 사이클 규약: 본문 *"1 C … charge … 0.1 C constant-voltage discharge"* ↔ Fig. 13 *"0.1 CCC · 300 s - CVC · 0.1 CCDC"* (§3-7).
7. 결론 *"Expectedly, the half-cell capacity increases with higher C-rates."* (p.15) ↔ §3.1 *"the capacity is significantly higher at lower C-rates"* (p.11) · Fig. 7.
8. 결론 *"consistent with previously published measurements … under a range of external pressures and charging conditions (Conforto et al., 2021)"* (p.15) ↔ 본문에 실린 실험은 전류 세 가지의 곡선 한 벌 (캡션 출처 Bielefeld 2022) 뿐 — 압력별 실험 대조는 어디에도 없다.
9. 문턱 풀이 보정 인자: *"a factor of 9∕8"* (p.7) ↔ 유도된 *"15∕8√2"* (p.8) · Table 1 값의 보정 여부 미기재.
10. 식 (11) 의 ⟨x⟩₋ = −x (x ≤ 0) 를 식 (10) 에 넣으면 압축 에너지가 음수가 된다 — 식 (28) 의 둘째 항 (압축에서 K·I₁) 과 부호가 맞지 않는다 [카드 산술].
11. 문턱 에너지 표기: 식 (32) ψ^th ↔ 식 (33) ψ₀^th.
12. 서론 (p.3) 이 약속한 *"cathode particle size, cathode-particle crystallinity"* 의존성 조사가 결과 절에 없다.
13. 미세구조: 캡션은 Doerrer 2021 의 SEM (단결정 NMC · 상대밀도 ≈0.90 [다른 카드]) 기반이라 하고 모형은 등방 "다결정 2 차 입자" · 공극 ≈15 % · *"The particle and void distributions are random"* (p.11).
14. 같은 명목 조건 (0.1 C · 40 MPa · 기준 구조) 의 끝 용량이 그림마다 183.8 (Fig. 7) · 184.1 (Fig. 14a) · 185.7–185.8 (Fig. 8a · 10a) · 186.4 (Fig. 11) [판독].
15. 격자 주장 ↔ Fig. A.2 · 자유도 (§3-4 의 두 어림).
16. Table 1 의 ρ 4770 kg m⁻³ 와 [Li]_max 51.554 kmol m⁻³ 는 식량 92.5 g mol⁻¹ 를 뜻한다 — NMC811 (97.28) 과 5 % 차 [카드 산술].  참고문헌 목록의 Kristensen 2021 항목은 제목이 빠져 있다.

## 4. ★ 방법 — 식 번호별 · 풀이 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. ★ 식 (1)–(40) — 하나씩 (크롭 = `eq_NN_….png` · 400 dpi · 흰 여백 7 pt · 이웃 문단 없음)

| 식 | 쪽 | 인쇄된 식 (글자로 옮김) | 뜻 · 주의 | 크롭 |
|---|---|---|---|---|
| (1) | 3 | Ψ^f = ∫_Γ G_c dΓ | 날카로운 균열의 표면 에너지 | `eq_01_fracture_surface_energy_sharp_crack.png` |
| (2) | 3 | Ψ^f ≈ ∫_Ω G_c γ dΩ | Bourdin 정칙화 — γ = 균열 표면 밀도 | `eq_02_fracture_surface_energy_regularized.png` |
| (3) | 3 | γ = (1/c₀)[α(ξ)/ℓ₀ + ℓ₀ (∂ξ/∂x_i)²] | 일반 꼴 (Wu 2017) · α = 기하 균열 함수 | `eq_03_crack_surface_density_generic.png` |
| (4) | 3 | c₀ = 4 ∫₀¹ √α(ξ̂) dξ̂ | 정규화 상수 | `eq_04_scaling_parameter_c0.png` |
| (5) | 3 | Ψ^f = ∫_Ω G_c (3/(4L₀)) (ξ + (L₀²/4)(∂ξ/∂x_i)²) dΩ | **AT-1** (α = ξ) · L₀ = 2ℓ₀ — *"incorporates a nucleation threshold"* | `eq_05_at1_surface_energy_functional.png` |
| (6) | 4 | Ψ^e = ∫_Ω ψ₀(ξ) dΩ | 탄성 에너지 | `eq_06_elastic_strain_energy_functional.png` |
| (7) | 4 | ψ₀ = g(ξ) ψ₀⁺ + ψ₀⁻ | 인장 몫만 손상 | `eq_07_strain_energy_tension_compression_split.png` |
| (8) | 4 | Ψ^e = ∫_Ω (g(ξ) ψ₀⁺ + ψ₀⁻) dΩ | (7) 대입 | `eq_08_elastic_energy_functional_degraded.png` |
| (9) | 4 | ψ₀⁺ = ½ K I₁(ε^e)⟨I₁(ε^e)⟩₊ + 2μ J₂(ε^e) | **부피–편차 분리**: 양의 부피 몫 + 편차 전부 → 손상되면 전단도 못 버틴다 (마찰 없는 균열) | `eq_09_tensile_energy_vol_dev_split.png` |
| (10) | 4 | ψ₀⁻ = ½ K I₁(ε^e)⟨I₁(ε^e)⟩₋ | 압축 부피 몫 — 손상돼도 남는다 | `eq_10_compressive_energy.png` |
| (11) | 4 | ⟨x⟩₊ = {0, x < 0 ; x, x ≥ 0} · ⟨x⟩₋ = {−x, x ≤ 0 ; 0, x > 0} | Macaulay 괄호 — ⚠ 인쇄된 ⟨x⟩₋ 는 (28) 과 부호가 안 맞는다 (§3-11 ⑩) | `eq_11_macaulay_brackets.png` |
| (12) | 4 | ε_ij = ½ (∂u_i/∂x_j + ∂u_j/∂x_i) | **작은 변형률** | `eq_12_total_strain_displacement.png` |
| (13) | 4 | ε^e_ij = ε_ij − β_ij Δ[X] | 화학 팽창 = 열 팽창과 같은 꼴 · Δ[X] = 무응력 기준 대비 농도 변화 | `eq_13_elastic_strain_chemical_expansion.png` |
| (14) | 4 | Ψ^c = ∫_Ω RT [X]_max [(1 − x) ln(1 − x) + x ln x] dΩ | 이상 용액 · x = [X]/[X]_max · 화학 에너지는 손상과 무관하다고 가정 (p.5) | `eq_14_chemical_energy_ideal_solution.png` |
| (15) | 5 | d𝒟/dt = ∫_Ω (σ_ij ∂ε_ij/∂t + μ ∂[X]/∂t − J_k ∂μ/∂x_k − dΨ/dt) dV ≥ 0 | Clausius–Duhem (등온 · 외력 없음) | `eq_15_clausius_duhem_dissipation_inequality.png` |
| (16) | 5 | Ψ = 탄성 (8) + 파괴 (5) + 화학 (14) | 전체 자유 에너지 | `eq_16_total_free_energy_elastic_fracture_chemical.png` |
| (17) | 5 | dΨ/dt = (∂Ψ/∂ε_ij) ε̇_ij + (∂Ψ/∂[X]) [Ẋ] + (∂Ψ/∂ξ) ξ̇ + (∂Ψ/∂∇ξ) ∇ξ̇ | 시간 미분 | `eq_17_free_energy_time_derivative.png` |
| (18) | 5 | ∫(σ_ij − ∂Ψ/∂ε_ij) ε̇_ij dV + ∫(μ − ∂Ψ/∂[X]) [Ẋ] dV − ∫ J_k ∂μ/∂x_k dV − ∫((∂Ψ/∂ξ) ξ̇ + (∂Ψ/∂∇ξ) ∇ξ̇) dV ≥ 0 | 여기서 (22) · (28) · (31) 이 나온다 | `eq_18_dissipation_inequality_expanded.png` |
| (19) | 6 | ∂[X]/∂t + ∂J_k/∂x_k = 0 | NMC 안 Li 보존 | `eq_19_li_mass_conservation.png` |
| (20) | 6 | J_k = −(D^eff_kℓ / RT) [X] (1 − [X]/[X]_max) ∂μ/∂x_ℓ | 화학–역학 퍼텐셜 기울기가 유속 (Bohn 2013) | `eq_20_flux_chemo_mechanical_potential.png` |
| (21) | 6 | D^eff_kℓ = g(ξ) D_kℓ | **깨진 곳은 확산도 끊긴다** | `eq_21_effective_diffusivity_degradation.png` |
| (22) | 6 | μ = ∂Ψ/∂[X] = RT ln([X] / ([X]_max − [X])) − β_ij σ_ij | 응력 항 −β_ij σ_ij | `eq_22_chemo_mechanical_potential.png` |
| (23) | 6 | (20) 에 (22) 대입 | 중간 꼴 | `eq_23_flux_substituted.png` |
| (24) | 6 | J_k = −D^eff_kℓ [∂[X]/∂x_ℓ − [X] (1 − [X]/[X]_max) (β_ij / RT) ∂σ_ij/∂x_ℓ] | Fick 항 + 응력 기울기 항 · 완전 치환형 (*"fully substitutional"*) | `eq_24_flux_concentration_and_stress_gradient.png` |
| (25) | 6 | −∂/∂x_k (K^eff_el ∂Φ_el/∂x_ℓ)_k = 0 | SE 이온 전하 보존 (SE 안 Li 농도 상수) · K^eff_el 의 정의 (손상 의존) 는 인쇄되지 않음 [미확인] | `eq_25_charge_conservation_electrolyte.png` |
| (26) | 6 | −∂/∂x_k (K^eff_ed ∂Φ_ed/∂x_ℓ)_k = 0 | 전극 상 전자 전하 보존 | `eq_26_charge_conservation_electrode.png` |
| (27) | 7 | ∂σ_ij/∂x_j = 0 | 준정적 힘 평형 (체적력 없음) | `eq_27_momentum_balance_quasi_static.png` |
| (28) | 7 | σ_ij = g(ξ) [½ K (I₁δ_ij + abs(I₁) δ_ij) + 2μ dev(ε^e_ij)] + ½ K (I₁δ_ij − abs(I₁) δ_ij) · I₁ = I₁(ε^e) | **구성식 = 선형 탄성 + 손상** (소성 항 없음) | `eq_28_stress_strain_degraded_vol_dev.png` |
| (29) | 7 | g(ξ) = (1 − ξ)² | 손상 함수 | `eq_29_degradation_function.png` |
| (30) | 7 | (28) 과 같은 꼴 · ε^e 자리에 전체 변형률 ε | SE 는 화학 팽창이 없다 | `eq_30_stress_strain_solid_electrolyte_total_strain.png` |
| (31) | 7 | G_c (3/(4L₀)) (1 − (L₀²/2) ∂²ξ/∂x_i²) − 2(1 − ξ) ψ₀⁺ ≥ 0 · ξ̇ (같은 식) = 0 · ξ̇ ≥ 0 | 비가역 손상의 부등식 묶음 | `eq_31_phase_field_evolution_inequalities.png` |
| (32) | 7 | ψ^th = 3 G_c / (8 L₀) | **손상 시작 문턱** | `eq_32_threshold_strain_energy.png` |
| (33) | 7 | H_d = max_t {ψ₀^th, ψ₀⁺(t)} | 이력 장 (되돌아가지 않게) | `eq_33_history_field.png` |
| (34) | 7 | G_c (3/(4L₀)) (1 − (L₀²/2) ∂²ξ/∂x_i²) − 2(1 − ξ) H_d = 0 | **실제로 푸는 선형 식** | `eq_34_phase_field_evolution_equation.png` |
| (35) | 8 | (34) 의 1D 꼴 (ψ₀⁺ = 0) · ξ(0) = 1 · ξ(∞) = 0 | 문턱 풀이의 점검 문제 | `eq_35_phase_field_1d_boundary_value_problem.png` |
| (36) | 8 | ξ(x) = exp(−(√2 / L₀) x) | 1D 해 | `eq_36_phase_field_1d_solution.png` |
| (37) | 8 | Ψ^f = G_c ∫₀^∞ (3/(4L₀)) [exp(−(√2/L₀)x) + ½ exp(−(2√2/L₀)x)] dx = (15 / (16√2)) G_c | 반쪽 균열의 에너지 → 온 균열 1.326 G_c | `eq_37_fracture_energy_threshold_overestimate.png` |
| (38) | 8 | F ṡ_Li⁺ = i_BV = i₀^eff [exp(α_a F η / RT) − exp(−α_c F η / RT)] | 계면 반응 (Butler–Volmer · 단일 전자) | `eq_38_butler_volmer.png` |
| (39) | 9 | i₀^eff = g(ξ) i₀ | **깨진 계면에서 반응이 꺼진다** | `eq_39_effective_exchange_current_density_damage.png` |
| (40) | 9 | η = Φ_ed − Φ_el − E^eq − β_ij σ_ij / F · i, j = 1, 2, 3 | 과전압에 응력 항 | `eq_40_overpotential_with_stress.png` |

**초기 · 경계 조건** (Fig. 4 · p.8–9 · `fig_4.png` · `txt_p8_transport_initial_boundary_conditions.png` · `txt_p9_mechanics_bc_stress_free_plane_strain_gc.png`): 수송 — 초기 x = 0.97 균일 · 오른쪽 경계 (집전체) 에 전극 전류 i_ed = i_tot · 왼쪽 경계에 Φ_el = 0 · 위 · 아래 −n·i_el = −n·i_ed = 0 · NMC–SE 계면에 i_BV.  역학 — 위 · 오른쪽 · 아래 **롤러** · 왼쪽 (분리막 면) 에 **압력 p** · 초기 무응력 · ξ = 0 균일 · **평면 변형 + 면 밖 화학 팽창 없음** (*"This simplification provides a more accurate representation of the state of stress in 3D particles (Taghikhani et al., 2024)"*, p.9).

### 4-2. 풀이 사슬

1. SEM 그림 (Doerrer 2021) → Adobe Illustrator 로 편집 · 상 분할 → im2mesh 로 격자 (p.6) → 공극률 · 입자 크기를 Bielefeld 2022 값에 맞춤.
2. G_c 지도: 계면 1.0 · NMC 2.5 · LPSC 2.79 를 phase-field 꼴 식으로 폭 ℓ₀ 에 퍼뜨림 (Fig. 5).
3. COMSOL: [X] · u · Φ_ed · Φ_el · ξ 를 segregated 로 시간 적분 (정전류 → 4.2 V 차단 · 사이클 런은 CV 300 s + 정전류 방전).
4. 출력: 전압–용량 곡선 · Li 농도 · 제1 주응력 · ξ 색 지도.  균열 길이 · 활성 면적 · 반응 전류 분포의 수치는 내지 않았다.

### 4-3. 입자 처리 ★

- **AM** = 2D 다각형 조각 ≈125 개 (판독) · 등방 선형 탄성 연속체 · 1 차 입자 · 방위 · 입계 없음 · 조각 안에서 Li 확산 (19)–(24).
- **SE** = 조각 사이를 메운 **한 덩어리 연속체** (입자 · 입계 없음 — 서론은 *"polycrystalline Li₆PS₅Cl (LPSC) solid electrolyte matrix"* 라고 부른다) · 선형 탄성 · Li 농도 상수.
- **공극** = 구멍 (요소 없음 · 경계 자유).  **탄소 · 바인더** = 없음 (암묵).
- **계면** = 처음엔 완전 접합된 연속체 · 낮은 G_c 띠 · 손상되면 인장 · 전단 강성 0 · 압축 부피 강성만 남음 → **접촉 판정 · 마찰 · 틈 벌어짐 · 다시 닿아 반응 회복은 모형에 없다.**
- 즉 "입자를 푼다" 는 것은 기하를 풀었다는 뜻이고, 입자끼리의 **접촉 역학은 없다** — 처음부터 붙어 있는 복합재가 깨지는 계산이다.

### 4-4. ★ 이 묶음의 네 질문 (원문 문장과 위치)

| 질문 | 원문 |
|---|---|
| (i) DEM (단단한 구 · 점접촉) 의 한계를 말했나 | **말 없음.**  DEM 을 쓰지도 인용하지도 않는다.  선행 방법 분류 (p.2–3): *"cohesive zone modeling … phase-field fracture … continuum damage … effective springs … and extended-finite-elements … to predict electrode cracking"* · P2D 에 대해서만 *"P2D models significantly simplify factors such as structural anisotropy, lattice deformations, and associated particle fracture and phase separations, making them less appropriate for studying ASSBs"* (p.2) |
| (ii) 입자의 소성 · 큰 변형을 넣기 어려운 이유 · 우회 · 비용 | **이유를 말하지 않고 뺐다.**  서론은 *"sulfide-based solid electrolytes (e.g., LPSC) are sufficiently malleable so as to maintain interfacial contact under external pressure"* (p.2) 인데 구성식은 선형 탄성 (28) · 작은 변형 (12).  우회 = 없음 (탄성 + 취성 파괴).  비용 = 2D 에서 ≈3.5 M 자유도 · *"Considering the size of the problem, the model is solved using a segregated solver"* (p.9) · 3D 는 *"impractical for parametric studies"* (p.14) · 물성을 상수로 둔 이유도 *"to reduce the computational cost"* (p.10) |
| (iii) 2D 인가 3D 인가 · 전이에 대한 말 | **2D 평면 변형.**  *"Although the model is fully capable of representing three-dimensional microstructures, the present paper reports results in a two-dimensional setting using a plane-strain assumption."* (p.14) · *"The fracture effects are exaggerated in a 2D model because the cracks propagate infinitely in the out-of-plane direction."* (p.12) · 과대 예측의 첫 원인 *"using a 2D model"* (p.11) · 평면 변형 + 면 밖 화학 팽창 없음이 3D 입자 응력을 더 잘 나타낸다는 근거는 자기 논문 (Taghikhani 2024) |
| (iv) 압력을 뺄 때의 거동 | **다루지 않음.**  적층압은 운전 내내 일정 · 성형압 · 탈압 · 잔류 응력 없음 (p.9 인용 §3-10 ①) |

### 4-5. 기법 미니 용어집

- **phase-field 파괴**: 균열을 선으로 두지 않고 손상 변수 ξ (0–1) 가 폭 ℓ₀ 에 걸쳐 번진 띠로 나타낸다 · ℓ₀ → 0 이면 Griffith 이론으로 돌아간다 (p.3).
- **AT-1 / AT-2**: 기하 균열 함수 α(ξ) = ξ / ξ².  AT-1 은 손상이 시작되는 에너지 문턱이 있다 (식 32).
- **임계 에너지 해방률 G_c** (J m⁻²): 균열 면을 단위 넓이 만드는 데 드는 에너지.  K = √(G_c·E′) 로 파괴 인성과 이어진다.
- **길이 척도 ℓ₀**: 손상 띠의 폭이자, 초기 결함이 없는 문제에서는 **강도**를 정하는 매개변수 (σ_c ∝ √(G_c·E / ℓ₀)).
- **이력 장 H_d**: 지금까지의 인장 변형 에너지 최댓값 — 손상이 되돌아가지 않게 한다.
- **부피–편차 분리**: 변형 에너지를 팽창 (인장) · 압축 · 전단으로 나눠 팽창 + 전단만 손상시키는 방식 — 닫힌 균열이 압축은 전하지만 전단은 못 전한다 (마찰 없음).
- **화학–역학 퍼텐셜**: 화학 퍼텐셜에 −β_ij σ_ij 를 더한 것 — 인장 응력이 걸린 곳으로 Li 가 모인다.
- **평면 변형**: 면 밖 변형률 0.  2D 균열은 면 밖으로 무한히 이어진 면이 된다.
- **segregated solver**: 변수 묶음을 번갈아 푸는 풀이 (한꺼번에 푸는 fully coupled 의 반대) — 메모리를 아낀다.
- **롤러 경계**: 면에 수직인 변위만 막고 미끄럼은 자유.
- **CC / CV**: 정전류 / 정전압.  그림 13 의 CCC · CVC · CCDC = 정전류 충전 · 정전압 충전 · 정전류 방전.
- **im2mesh**: 분할된 그림을 다각형 격자로 바꾸는 도구 (원문이 이름만 적음).

## 5. Figure set ★ (전부 `litdb/figures/taghikhani2025_…/` · 다시 자른 것은 figures.json 의 `recrop`)

| 그림 | 무엇을 보여 주나 | 우리가 재사용할 것 | 크롭 |
|---|---|---|---|
| Fig. 1 | 복합 양극 반쪽 셀의 이상화 그림 — 집전 박 / NMC 2 차 입자 + Li₆PS₅Cl + 나노 탄소 / 분리막 / Li | 없음 (개념도) | `fig_1.png` |
| Fig. 2 | (a) 날카로운 균열 (b) 번진 균열 (c) 손상 프로파일과 ℓ₀ | phase-field 설명 그림 (발표용) | `fig_2.png` |
| Fig. 3 | 계산 기하 — 10 µm SE + 40 × 40 µm² 복합 + 집전체 · 노랑 SE · 회색 AM · 흰색 공극 "≈15 %" | 상 분율 · 입자 · 공극 크기 판독 (§3-1) — "모형의 공극률" 이 무엇인지의 예 | `fig_3.png` |
| Fig. 4 | 초기 · 경계 조건 (붉은 글자 = 수송 · 회색 = 역학) | **적층압을 주는 방식** (한 면 견인력 + 세 면 롤러) 의 본 | `fig_4.png` |
| Fig. 5 | G_c 지도 (1.0 계면 띠 · 2.5 NMC · 2.79 LPSC) + 확대 | 계면 띠 폭 · 공극 경계의 계단 꼴 | `fig_5.png` |
| Fig. 6 | 유한요소 격자 — 계면 촘촘 · 분리막 성김 + 확대 | 격자 등급 (요소 수는 없음) | `fig_6.png` |
| Fig. 7 | ★ 검증: 0.02 C · 0.1 C · 빠른 전류의 전압–용량 (실험 실선 · 모형 점선류 · p = 40 MPa) | 과대 예측 크기 (§3-5) | `fig_7.png` |
| Fig. 8 | (a) 0.1 C 전압 (b) 충전 끝 Li 농도 (c) 제1 주응력 · 확대 원 | 응력 크기 (눈금 −200 … 800 MPa) · 깨진 계면 둘레에 Li 가 남는 모습 | `fig_8.png` · `fig_8a.png` |
| Fig. 9 | ★ 무압: (a) 계단 있는 전압 곡선 · 두 동그라미 = (b) 계단 전 (c) 계단 뒤 ξ 지도 | 계면 균열 ↔ 전압 계단의 대응 (2D 인공물 경고와 함께) | `fig_9.png` · `fig_9a.png` |
| Fig. 10 | ★ (a) 무압 ↔ 40 MPa ↔ 실험 (b) 무압 (c) 40 MPa 의 충전 끝 ξ 지도 · 확대 | **적층압 유무의 손상 비교** (§3-6) | `fig_10.png` · `fig_10a.png` |
| Fig. 11 | LLZO ↔ LPSC (0.1 C · 40 MPa) | SE 강성 · 인성 · 전도도 묶음 대조 | `fig_11.png` |
| Fig. 12 | ★ 계면 G_c 0.2 · 1.0 · 2.0 (무압 · 0.1 C) | 계면 인성 문턱 (§3-6) | `fig_12.png` |
| Fig. 13 | 5 ↔ 40 MPa 세 사이클 · 그림 안 규약 글자 | 첫 사이클 손실 판독 (§3-7) | `fig_13.png` |
| Fig. 14 | ★ (a) 공극 15 % ↔ 없음 ↔ 실험 (b) 15 % (c) 공극 없는 구조의 ξ 지도 | **공극이 균열을 줄인다** 는 그림 (c 의 긴 균열) | `fig_14.png` · `fig_14a.png` |
| Fig. A.1 | NMC811 의 D(x) · i₀(x) · 개회로 전압 (Bielefeld 2022 재수록) | 농도 의존 물성의 모양 (§3-3) — 원전 확인 뒤 STEP4 대조 | `fig_A1.png` · `fig_A1a.png` · `fig_A1b.png` · `fig_A1c.png` |
| Fig. A.2 | 충전 끝 (0.1 C · 40 MPa) 의 균열 확대 + 격자 선 | 손상 띠 ↔ 요소 크기 (§3-4) | `fig_A2.png` |
| Table 1 | 모형 매개변수 24 행 | §3-2 전사 | `tab_1.png` |

근거 문단 크롭 25 장 (`txt_pN_….png`) 은 §3 · §4 의 인용문마다 이름을 적었다 (제목 · 초록 `txt_p1_title_authors_abstract.png` 포함).

## 6. Post-processing ★

- **원문이 한 것**: 조건마다 전압–용량 곡선 한 장 + ξ · 농도 · 주응력 색 지도.  용량 (mAh g⁻¹) 의 분모 · 1 C 전류 · 평균화 방법은 적지 않았다 [미확인].  균열 길이 · 손상 면적 · 살아 있는 계면 길이 · 반응 전류 분포 · 수송 경로 길이 같은 **정량 지표는 없다** — *"tortuous pathways"* 는 말로만 (τ 값 없음 · 우리 τ 규약과 견줄 양이 없다).
- **이 카드가 한 것** (재현 = digitized.csv 의 note 열): (i) 곡선은 벡터 경로 → 꼭짓점 좌표를 눈금 두 개로 선형 보정 (그림마다 눈금 위치 기록) (ii) Fig. 13 은 한 경로에 세 사이클이 이어져 있어 용량이 단조인 가지로 나눔 (iii) Fig. 14a 의 'No pores' 곡선 끝은 래스터에 들어 있어 1200 dpi 렌더의 붉은 화소 위치로 읽음 (iv) Fig. A.1 은 붉은 표지 (채운 경로) 의 중심 (v) Fig. 3 은 박힌 래스터의 색 분류 · 연결 성분.
- 판독의 자기 점검: 같은 실험 곡선이 Fig. 7–14 여덟 그림에 다시 실려 있고 끝값이 171.7–171.8 로 모인다 (그림마다 따로 보정한 값) → 보정 오차 ≈±0.1 mAh g⁻¹.

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (우리 수치는 CLAUDE.md 출처를 병기)

### 7-1. 비교표 (모든 행에서 **차원 · 구성식 · 무엇을 계산하는지가 다르다**)

| 항목 | 이 논문 | 우리 [우리 · CLAUDE.md] | 같음 / 다름 · 왜 |
|---|---|---|---|
| 푸는 문제 | **주어진** 미세구조 위의 충방전 (전기화학 + 응력 + 파괴) | 분말을 **눌러** 구조를 만드는 압밀 (DEM · MPM) → 그 구조의 수송 | 겹치지 않는다 — 이 논문은 우리 사슬의 **하류** (구조가 주어진 뒤) |
| 차원 | 2D 평면 변형 | DEM 3D · MPM 3D (2D 는 시험용) | 2D 값은 3D 로 옮기지 않는다 |
| SE 구성식 | 선형 탄성 E 22.1 GPa · ν 0.37 + 취성 손상 | DEM: 탄성-이력 접촉 · 무르게 맞춘 E_eff 1.35 GPa (18 배) / MPM: J2 소성 E 1.53 · σ_y 0.30 · ν 0.49 | 이 논문의 E 는 **실제 강성** (우리 DFT E_VRH 22.06 · ν 0.360 과 같은 수준) — 우리 무른 값은 재배열의 대리이지 물성이 아니다.  소성은 우리만 |
| AM | 선형 탄성 E 175.27 GPa · ν 0.2819 · 등방 · 화학 팽창 | DEM: 단단한 구 (E 140 GPa 입력) / MPM: 얼린 골격 | 강성은 같은 자릿수 · 이 논문만 화학 팽창과 파괴 인성을 가짐 |
| 계면 | 완전 접합 → 손상 (G_c 1.0 J m⁻² 가정) | DEM: 접촉 (겹침 · 면적) · 접촉 원장 (사이클 뒤 처리 · Bucci G_c 2.8 ± 1.8) | 이 논문에는 접촉이 없고 우리에겐 연속체 파괴가 없다 |
| 출발 상태 | 무응력 · 손상 0 · 그린 기하 | DEM 압밀 끝 상태 (300 MPa → 이완 · 언로딩 계산 진행 중) | **우리 단계 5 · 6 의 출력이 이 계열 모형의 빠진 입력** |
| 압력 | 운전 적층압 0 / 5 / 40 MPa (일정) | 성형압 300 MPa → 탈압 | 다른 압력이다 (운전 ↔ 성형) |
| 공극 | 2D 면적 분율 "≈15 %" (그린 것) ↔ 0 % | 압밀 결과로 나오는 기공 (real_14 ε_sphere 15.6 %) · 랩 표준 순수 SE 10–13 % | 숫자가 비슷해 보여도 정의가 다르다 — 나란히 놓지 않는다 |
| 이온 전도 | K_el 0.7 mS cm⁻¹ (균질 SE · 공극은 기하로) | σ₀ 보고 기준 1.5 mS cm⁻¹ (솔버 상수 3.0) · 접촉망은 접촉 협착 포함 | 이 논문의 SE 는 협착 없는 연속체 — 우리 복셀 가지와 같은 쪽 |
| 전자 전도 | NMC 100 S m⁻¹ (= 1000 mS cm⁻¹) · *"not a limiting factor"* | σ_AM 모형 기준 50 mS cm⁻¹ (측정 NCM811 4.1–5.2 의 약 10 배 — CL-92) | 이 논문은 전자 쪽 제한을 일부러 없앴다 (우리 값의 20 배) |
| 검증 | 전압 곡선 한 벌 · +5–14 % 과대 | 압밀: 실험 기공 · 수송: EIS 앵커 | 검증 대상이 다르다 |

### 7-2. ★ 운전 적층압 0 → 5 → 40 MPa 를 우리 단계 6 과 나란히 놓을 때

- 이 논문의 압력은 **운전 중 한 면에 건 견인력**이고 출발이 무응력이다.  우리 단계 6 (탈압) 이 내는 것은 **성형 뒤 남는 응력과 계면 상태** — 이 논문이 *"focus of ongoing studies"* 라고 비워 둔 바로 그 입력이다.
- 모형 안에서는 0 MPa 만 나쁘고 (−19 %) 5 MPa 부터는 40 MPa 와 같다 [판독].  "몇 MPa 의 압축이 남아 있으면 계면 분리가 용량에 안 보이는가" 의 문턱이 0–5 MPa 사이라는 뜻이지만, 2D (분리 효과 과장) · 계면 G_c 와 ℓ₀ 가정 · 선형 탄성 위의 값이다 — **방향 (압축이 남으면 분리가 줄어든다) 만 가져온다.**
- [다른 카드 `doerrer2021_…`] 실험에서 적층압 0.2 → 2.5 → 10 MPa 의 첫 효율은 ≈83 → 85 → 85 % 로 차가 작다 (단결정 NMC83) — 모형의 "5 MPa 이상 포화" 와 방향은 같고, 모형의 "0 MPa 급락" 에 해당하는 실험점 (정확히 0) 은 없다.

### 7-3. ★ G_c 2.785 · 1.0 · 2.5 ↔ 우리 접촉 원장 (cycle_contact_ledger · Bucci G_c 2.8 ± 1.8)

- 이 논문의 LPSC G_c 2.785 J m⁻² 와 우리 원장의 2.8 ± 1.8 J m⁻² 는 **같은 뿌리**다 — 둘 다 McGrogan 2017 의 70Li₂S–30P₂S₅ 유리 K_Ic 0.23 MPa·m^½ · E 18.5 GPa 에서 K²/E 로 나온 값 ([다른 카드 `mcgrogan2017_…` L72: bucci2017 카드의 2.8 ± 1.8 = K²/E · 그 카드 산술 2.86]).  ⇒ **두 논문이 같은 값을 썼다고 독립 앵커 둘로 세지 않는다.**  argyrodite 의 측정 파괴 인성은 이 사슬 어디에도 없다.
- 계면 G_c 1.0 J m⁻² 는 출처가 없다 ([다른 카드 `bucci2017_…`] 의 "황화물 SE 대표값 1.0 J m⁻²" 와 숫자가 같지만 그쪽은 SE 덩어리 값이고 이 논문은 인용하지 않았다).  이 값이 1 ↔ 2 사이에서 결과가 갈린다 (§3-6) — 우리 원장의 계면 판정도 같은 민감도를 가질 것이다.
- 깨진 계면의 반응: 이 논문 = (1 − ξ)² 로 꺼지고 **돌아오지 않는다** (식 39 · 이력 장 · *"fracture does not lead to activation of new surfaces"*).  우리 원장의 재습윤 세 가지 (forbid / partial / elastic) 가운데 **forbid** 에 해당한다.

### 7-4. 탄성 상수

| | 이 논문 | 우리 |
|---|---|---|
| LPSC | E 22.1 · ν 0.37 → K 28.3 · G 8.07 GPa [카드 산술] | DFT E_VRH 22.06 · B₀ 26.23 · ν 0.360 · μ 8.11 GPa / Bazzoun 2026 DEM 입력 22.1 · 0.37 / MPM K 25.5 · μ 0.51 GPa (전단만 무르게) / DEM E_eff 1.35 GPa |
| NMC | E 175.27 · ν 0.2819 (Taghikhani 2024 · 원문 미확인) | DEM 입력 140 GPa · Bazzoun 2026 E_CAM 161.5 |

- 이 논문의 SE 는 "실제 강성 + 소성 없음" 이라 제1 주응력이 수백 MPa 까지 선다 (§3-8).  우리 MPM 처럼 전단 문턱 0.30 GPa 에서 흐르게 하면 계면 인장이 풀릴 것 — 어느 쪽이 실제에 가까운지는 이 논문으로 가릴 수 없다 (frame [4]: 서로 맞추지 않는다).

### 7-5. frame[5] — 어느 반쪽을 가졌나

- **가진 것**: 주어진 구조에서의 **충방전 중 응력 · 계면 손상 · 반응 차단** (우리 DEM · MPM 어느 쪽에도 없는 하류 물리).
- **없는 것**: 압밀 (구조를 만드는 일) · 소성 형상 변화 (MPM 의 몫) · 접촉망 · 협착 · 퍼콜레이션 · Furnas 골 (DEM 의 몫) · 탈압.
- 우리 쪽에서 이 논문의 자리는 **단계 7 뒤** (사이클 중 열화) 이고, 압밀 모형을 고르는 근거로는 쓸 수 없다.

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나

| 이름 | 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| 단계 0 (기공률 연산자) | "공극 ≈15 %" 가 **2D 그림의 면적 분율** 인 실례 — 색 분류로 12.5 % (윤곽선 빼면 14.5 %) [판독] · 공극 조각 87 개 · 중앙 1.5 µm.  모형 논문의 "porosity" 는 입력 기하이지 측정이 아니라는 표지 문장의 근거 | 질량 · 진밀도 기공 · 압력별 기공 없음.  랩 표준 (순수 SE 10–13 % · 진밀도 1.64) 과 견줄 값 없음 — SE 밀도를 쓰지 않는다 |
| 단계 1 (3D 메모리 · 장 수) | 비용의 감: 40 × 40 µm² 2D 에서 변수 5 개 · ≈3.5 M 자유도 · segregated · 3D 는 *"impractical for parametric studies"* | 메모리 · 시간 · 기계 숫자 없음 |
| 단계 2 (2D 코드 · 단위 시험) | 1D 해석해 (식 35–37) 로 수치 기법의 편향 (소산 1.326 배) 을 스스로 잰 방식 = "풀이 편의가 만든 오차를 해석해로 정량" 의 본 | MPM · 접촉 시험과 직접 닿는 것은 없음 |
| 단계 3 (2D 접촉 표현 비교) | **2D 경고문** (p.12): 2D 에서는 분리가 면 밖으로 무한한 면이 되어 효과가 과장된다 · 실험에 없는 전압 계단이 나온다 → 우리 2D 벤치마크에서 분리 · 미끄럼 효과를 3D 크기로 읽지 않는다는 한정어의 근거 | 접촉 표현 (한 속도장 ↔ 입자별) 과는 무관 |
| 단계 4 (3D 순수 SE) | 없음 (SE = 선형 탄성 연속체 · 항복 없음) | — |
| 단계 5 (3D 복합 가압) | 없음 — 가압 계산을 하지 않는다.  출발 구조는 그림 | 성형압 · 하중 분담 · 입자 재배열 전부 없음 |
| 단계 6 (탈압) | **간접**: (i) 이 계열 최신 모형이 출발을 무응력으로 두고 잔류 응력을 "진행 중 연구" 로 남겼다는 문장 (p.9) = 우리 탈압 결과 (잔류 응력 · 계면 상태) 가 채울 자리 (ii) 모형 안의 적층압 응답은 0–5 MPa 문턱형 [판독] | 탈압 거동 · 되돌아옴 · 잔류 응력 값 없음 |
| 단계 7 (형상 · 피복 · 수송) | 손상이 **반응 (39) · 확산 (21) · 강성 (28)** 을 같은 (1 − ξ)² 로 끄는 구조 · 과전압의 응력 항 (40) · 깨진 계면은 다시 살아나지 않는다는 가정 · K_el 0.7 mS cm⁻¹ · K_ed 100 S m⁻¹ | 피복률 · 수송 tortuosity · 유효 전도도 숫자 없음 (말로만 *"tortuous pathways"*) |
| 후보 D0 (지금 DEM) | 접촉 원장의 계면 파괴 판정에 쓸 **G_c 출처 사슬 정리** (§7-3: 2.785 = 우리 2.8 과 같은 뿌리 · 계면 1.0 은 무출처) · 계면 인성 민감도가 문턱형이라는 경고 | DEM 에 대한 말 없음 |
| 후보 A′-0 (MPM 접촉 부품) | 대조 사례: 분리를 손상 띠로 나타내면 **닫힌 뒤 전단을 못 전한다** (식 9 · 28) — 미끄럼 · 마찰을 따로 줄 접촉 규칙이 왜 필요한지의 반례 | 접촉 판정 · 마찰 법칙 없음 |
| 후보 A (AM 강체 + SE 한 장) | 없음 (AM 은 탄성체 · 움직임 없음 · 처음부터 접합) | — |
| 후보 A′ (입자별 속도장) | 없음 | — |
| 후보 B (입자별 FE + 접촉) | **B 가 아니다** — 상 분해 유한요소이지만 접촉이 없고 작은 변형이다.  비용 감 (2D 3.5 M 자유도) 만 | 큰 변형 · 접촉 탐지 · 입자 재배열 없음 |
| 후보 C · C′ · M0 | 없음 | — |
| U0–U6 | 없음 (U3 "눌렀다 떼기" · U4 "판 분리" 와 닿는 계산 없음) | — |
| R1 (AM 하중 분담) | 없음 — 40 MPa 를 걸지만 상별 응력 몫은 내지 않는다 | — |
| R2 (미끄럼 · 분리) | **일부** — 분리 = 손상 (계면 G_c 1.0 · ℓ₀ 100 nm) · 분리가 반응을 끄는 결합 · 적층압이 분리를 줄인다는 방향 | 미끄럼 · 마찰 · 틈 · 재접촉 없음.  lei2026 의 "최대 틈 nm" 는 이 논문에 없다 |
| R3 (SE 입자 경계 기억) | 없음 (SE = 한 덩어리) | — |
| R4 (탈압 · 되돌아옴) | 없음 | — |
| R5 (맞추는 값은 하나) | 반면교사: 맞춘 값이 **0 개** 인 대신 가정값 둘 (계면 G_c · ℓ₀) 이 결과를 정하고, 검증 곡선과의 차 (+5–14 %) 는 그대로 둠 — "보정 없음" 과 "근거 있음" 은 다르다 | — |
| R6 (SE 형상 변형) | 없음 (작은 변형 탄성) | — |
| R7 (AM 파괴) | **일부** — NMC G_c 2.5 J m⁻² (Lim 2017) · 함축 K ≈0.66–0.69 MPa·m^½ [카드 산술] · 결과에서는 계면이 먼저 깨진다 | 1 차 입자 사이 (입계) 파괴 · 방향성 없음 — 저자 스스로 다음 과제 |
| 결과 전 대조 항목 | 후보 (방향만): ① 압축이 남은 상태에서 계면 분리 감소 ② 공극 없는 구조가 균열은 더 많음 ③ 2D 가 분리 효과를 과장 | 크기는 대조에 쓰지 않는다 (2D · 가정 물성) |

**재료 · 차원 · 조건 차이 (한눈에)**: 재료 = NMC811 + Li₆PS₅Cl 로 우리와 같은 계 (단, LPSC 파괴 인성은 유리 값 · 탄성은 DFT) · 차원 = 2D 평면 변형 ↔ 우리 3D · 조건 = 운전 적층압 0–40 MPa · 300 K · 충방전 ↔ 우리 성형 300 MPa · 탈압 · 구성식 = 선형 탄성 + 취성 손상 ↔ 우리 접촉 이력 / J2 소성.

## 9. 적용 인사이트 (행동)

1. **접촉 원장 문서에 G_c 계보를 적는다** — Bucci 2.8 ± 1.8 과 Taghikhani 2.785 는 둘 다 McGrogan 유리 K²/E 다 (독립 앵커 아님) · 계면 1.0 J m⁻² 는 무출처 가정 (§7-3).
2. **단계 6 의 산출물 목록에 "성형 뒤 잔류 응력 장 · 계면 상태" 를 명시한다** — 이 논문 p.9 의 문장을 "하류 모형이 비워 둔 입력" 의 인용으로 쓴다 (§10 ①).
3. **2D 벤치마크 (단계 2 · 3) 보고에 p.12 의 2D 경고문을 붙인다** — 분리 · 균열 효과를 2D 크기로 읽지 않는다 (§10 ②).
4. "소성이 왜 빠지는가" 의 사례로 쓴다: 황화물 SE 를 "malleable" 이라 부르면서 선형 탄성으로 계산한 최신 결합 모형 (§4-4 (ii)) — DEM 한계 문장은 이 논문에서 찾지 않는다 (말 없음).
5. STEP4 의 농도 의존 D · i₀ · 개회로 전압은 이 논문이 아니라 **원전 (Bielefeld 2022 · Ruess 2020) 을 받아** 대조한다 — 이 논문 Fig. A.1 은 재수록이고 i₀ 축 표기가 모호하다.
6. 후보 표 · lei2026 카드의 "Taghikhani 최대 틈 9.3 / 16.0 / 13.8 nm" 는 **Taghikhani 2023 (Electrochim. Acta 460, 142585) 원문을 받아** 확인한다 (정독 출력 n 절).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)

1. 잔류 응력 [인쇄 p.9]: *"The present model assumes the structure to be stress-free at the initial condition (x = 0.97). This assumption neglects the effect of residual stress developed during the fabrication process. These residual stress effects are the focus of ongoing studies."*
2. 2D [인쇄 p.12]: *"The fracture effects are exaggerated in a 2D model because the cracks propagate infinitely in the out-of-plane direction."*
3. 3D 비용 [인쇄 p.14]: *"Practical limitations for needed computational resources make full three-dimensional simulations impractical for parametric studies."*
4. 압력 [인쇄 p.13]: *"The application of external pressure induces a more compressive stress state, which consequently limits fracture compared to the no-pressure scenario."*
5. 공극 [인쇄 p.14]: *"The porous structure exhibits significantly less fracture, since the pores act as a stress relieving interface."*
6. 길이 척도 [인쇄 p.9]: *"In the absence of empirical data on strength of materials, the parameter selection relies on reasonable approximations aligned with available estimates in the literature"*
7. 자기 평가 [인쇄 p.15]: *"The predictions depend on fundamental materials properties, some of which are yet to be measured and validated."*
8. 수치 (우리 문장으로 · 표지 필수): "2D 평면 변형 phase-field 모형에서 0.1 C 충전 용량은 운전 적층압 0 MPa 에서 150.7, 40 MPa 에서 185.7 mAh g⁻¹ 였다 [Taghikhani 2025 · Fig. 10a 벡터 판독 · 계면 G_c 1.0 J m⁻² 가정 · 출발 무응력]."

## 11. 주의/한계 (over-claim 방지)

1. **2D 평면 변형** — 저자 스스로 분리 효과가 과장된다고 적었다.  용량 차 (−19 %) 를 3D 크기로 인용하지 않는다.
2. **선형 탄성 · 작은 변형** — SE 소성 · 크리프 · 접촉 없음.  "malleable" 은 서론의 말일 뿐 계산에 없다.
3. **출발 무응력 · 그린 기하** — 성형 이력이 없다.  "공극 15 %" 는 면적 분율.
4. **가정값 둘 (계면 G_c · ℓ₀) 이 결과를 정한다** — 문턱형 (§3-6).  ℓ₀ 는 강도 자료 없이 골랐다.
5. **검증이 얇다** — 전압 곡선 한 벌 · 과대 예측 +4.7 / +7.0 / +13.7 % [판독] · 실험 조건 미기재 · 압력 · 공극 · 계면 · LLZO 대조는 실험 없음 · 결론의 "range of external pressures … (Conforto et al., 2021)" 은 본문 자료로 뒷받침되지 않는다.
6. **격자 근거가 약하다** — 요소 수 · 수렴 시험 없음 · Fig. A.2 · 자유도 어림이 "4–5 배 작다" 와 맞지 않아 보인다 (§3-4).
7. **수치 대부분이 [판독]** — 원문 본문의 용량 숫자는 "186" 하나.  같은 조건의 끝값이 그림마다 183.8–186.4 로 다르다.
8. **재료 값의 재료가 섞여 있다** — LPSC G_c = Li₂S–P₂S₅ 유리에서 · LPSC E = DFT · NMC E · β = 자기 논문 · 계면 G_c = 무출처.  화학 팽창은 **농도에 선형 · 등방** 이라 고전압 쪽 급수축 (koerver2018 카드의 격자 곡선) 을 절반 아래로 잡는다 (§3-9).
9. **원문 안 어긋남 16 건** (§3-11) — 특히 C-rate (0.5 ↔ 5) · 계면 G_c (0.2 ↔ 0.5) · 사이클 규약.
10. **첫 사이클 손실의 원인** 은 균열로 단정할 수 없다 (균열 없는 대조 계산 없음 · §3-7).
11. **SE 대조 (LLZO)** 는 전도도 · 강성 · 인성이 한꺼번에 바뀐 것 — 원인 분리 없음.
12. 2 차 인용 주의: lei2026 의 "최대 틈 9.3 / 16.0 / 13.8 nm" 를 이 논문 값으로 옮기지 않는다 (§0-1).

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 서지 (원문 목록 그대로) | 왜 | 정본 카드 |
|---|---|---|
| Bielefeld, A., Weber, D.A., Rueß, R., Glavas, V., Janek, J., 2022. Influence of lithium ion kinetics, particle morphology and voids on the electrochemical performance of composite cathodes for all-solid-state batteries. J. Electrochem. Soc. 169 (2), 020539. | ★ 검증 곡선 · D(x) · i₀(x) · 개회로 전압 · x₀ · 공극률 · 입자 크기의 원전 — 실험 조건과 0.5 C ↔ 5 C 를 가를 수 있다 | 없음 (bielefeld 카드는 2019 · 2020 판) |
| Taghikhani, K., Weddle, P.J., Hoffman, R.M., Berger, J.R., Kee, R.J., 2023. Electro-chemo-mechanical finite-element model of single-crystal and polycrystalline NMC cathode particles embedded in an argyrodite solid electrolyte. Electrochim. Acta 460, 142585. | ★ lei2026 L115 의 "계면 분리 최대 틈 nm" 의 원문일 가능성 (조건 R2 · R7) | 없음 |
| Taghikhani, K., Singh, A., Weddle, P.J., Colclasure, A.M., Smith, K., Berger, J.R., Kee, R.J., 2024. Consequences of plane-strain and plane-stress assumptions in fully coupled chemo-mechanical Li-ion battery models. Electrochim. Acta 479, 143790. | ★ 2D 가정 (평면 변형 ↔ 평면 응력) 이 3D 입자 응력과 얼마나 다른가 — 질문 g · NMC E · ν · β 의 출처 | 없음 |
| Conforto, G., Ruess, R., Schröder, D., Trevisanello, E., Fantin, R., Richter, F.H., Janek, J., 2021. Editors' choice—quantification of the impact of chemo-mechanical degradation on the performance and cycling stability of NCM-based cathodes in solid-state Li-ion batteries. J. Electrochem. Soc. 168 (7), 070546. | 화학–역학 열화의 정량 실험 — 결론이 "압력 범위 실험" 의 근거로 든 논문 | 없음 |
| Zhang, F., Guo, Y., Zhang, L., Jia, P., Liu, X., Qiu, P., Zhang, H., Huang, J., 2023. A review of the effect of external pressure on all-solid-state batteries. Etransportation 15, 100220. | 성형압 ↔ 운전 적층압을 나눠 다룬 리뷰 (서론이 "fabrication 중 균열 · 공극" 의 근거로 인용) | 없음 |
| Ruess, R., Schweidler, S., Hemmelmann, H., Conforto, G., Bielefeld, A., Weber, D.A., Sann, J., Elm, M.T., Janek, J., 2020. Influence of NCM particle cracking on kinetics of lithium-ion batteries with liquid or solid electrolyte. J. Electrochem. Soc. 167 (10), 100532. | LPSC K_el 0.7 mS cm⁻¹ · 농도 의존 물성 · 실험 곡선의 한 원전 | 없음 |
| Lim, J.-M., Hwang, T., Kim, D., Park, M.-S., Cho, K., Cho, M., 2017. Intrinsic origins of crack generation in Ni-rich LiNi0.8Co0.1Mn0.1o2 layered oxide cathode material. Sci. Rep. 7, 39669. | NMC G_c 2.5 J m⁻² 의 출처 (조건 R7) | 없음 |
| McGrogan, F.P., Swamy, T., Bishop, S.R., Eggleton, E., Porz, L., Chen, X., Chiang, Y.-M., Van Vliet, K.J., 2017. Compliant yet brittle mechanical behavior of Li2S-P2S5 lithium-ion-conducting solid electrolyte. Adv. Energy Mater. 7 (12). | LPSC G_c 2.785 의 인용처 (유리 값) | `mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation` |
| Deng, Z., Wang, Z., Chu, I.-H., Luo, J., Ong, S.P., 2015. Elastic properties of alkali superionic conductor electrolytes from first principles calculations. J. Electrochem. Soc. 163 (2), A67. | LPSC E 22.1 · ν 0.37 (DFT) | `deng2016_elastic_superionic_electrolytes_dft` |
| Doerrer, C., Capone, I., Narayanan, S., Liu, J., Grovenor, C.R.M., Pasta, M., Grant, P.S., 2021. High energy density single-crystal NMC/Li6PS5Cl cathodes for all-solid-state lithium-metal batteries. ACS Appl. Mater. Interfaces 13 (31), 37809–37815. | 미세구조 그림의 원 SEM · 사이클 "일치" 의 근거 | `doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density` |
| Kodama, M., Ohashi, A., Hirai, S., 2020. In situ X-ray computational tomography measurement of single particle behavior of sulfide solid electrolyte under high-pressure compression. J. Power Sources Adv. 4, 100019. | "5 % void" 문장의 인용처 (뒷받침 안 됨) | `kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation` |
| Bucci, G., Swamy, T., Chiang, Y.-M., Carter, W.C., 2017. Modeling of internal mechanical failure of all-solid-state batteries during electrochemical cycling, and implications for battery design. J. Mater. Chem. A 5 (36), 19422–19430. | 같은 질문의 응집 영역 모형 (G_c 사다리) | `bucci2017_chemomech_failure_assb_cycling_czm` |
| Koerver, R., Zhang, W., de Biasi, L., Schweidler, S., Kondrakov, A.O., Kolling, S., Brezesinski, T., Hartmann, P., Zeier, W.G., Janek, J., 2018. Chemo-mechanical expansion of lithium electrode materials–on the route to mechanically optimized all-solid-state batteries. Energy Env. Sci. 11 (8), 2142–2158. | 화학 팽창의 실험 원전 (이 논문은 균열 = 용량 감소의 근거로만 인용) — 이 모형의 선형 β 와 견줄 격자 부피 곡선 (§3-9) | `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` |

## 13. [미확인] 목록 (본문 19 쪽 전수에 없음)

1. 검증 실험의 셀 구성 · 조성 · 적층압 · 온도 · 전극 두께 · 전류의 정의 (0.5 C ↔ 5 C).
2. 용량 (mAh g⁻¹) 의 분모 · 1 C 전류 값 · i_tot.
3. 요소 수 · 격자 수렴 시험 · 시간 간격 · 허용 오차 · 계산 시간 · 기계.
4. 계면 G_c 1.0 J m⁻² 와 ℓ₀ 100 nm 의 근거 값 · LPSC G_c 2.785 의 계산 과정 · Table 1 의 G_c 가 문턱 보정 (9/8 또는 15/(8√2)) 을 거쳤는지.
5. K^eff_el · K^eff_ed 의 정의 (손상 의존 여부) · SE 영역의 전자 전도도 · 집전체 물성.
6. i₀ 축의 배율 · 단위 (Fig. A.1b) · D · i₀ 의 측정법.
7. AM : SE 조성 · 입도 통계 · 공극 크기 분포 (판독값만 있음) · "No pores" 구조에서 공극 자리를 채운 재료.
8. 방전 하한 전압 (판독 ≈3.50 V) · 사이클 규약의 실제 전류.
9. 손상 면적 · 균열 길이 · 살아 있는 계면 비율 같은 정량 지표.
10. 5 MPa 단일 충전의 손상 그림 · 0–5 MPa 사이의 압력 사다리.
11. 서론이 말한 입자 크기 · 결정성 의존 결과.
12. NMC E · ν · β^iso (Taghikhani 2024) · NMC G_c (Lim 2017) · K_el (Ruess 2020) 의 원 측정 조건 — 그 원문들을 보지 못했다.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)

- 본문 19 쪽을 글자 층 추출 + 전 쪽 렌더로 읽음.  서지 = p.1 (제목 · 저자 6 명 · 소속 · DOI · 접수 · 수정 · 수락 · 온라인 날짜 · 라이선스) · 쪽 머리글 (*Journal of the Mechanics and Physics of Solids 198 (2025) 106060*).  1저자 메모와 다른 점 없음.  원문 낱말 셈: DEM · discrete = 0 · plastic · yield · creep = 0 · unload · springback = 0 · malleable = 1 (p.2).
- 그림 크롭 **89 장** = 도구 15 (Fig. 1–14 · Table 1 — **15 장 전부 다시 자름**: 그림 14 장은 본문 단 너비로 잘려 좌우 흰 여백이 넓어 잉크 상자 ± 6 pt 로 · 표 1 은 쪽 머리글 · Fig. 6 · 본문 문단이 섞여 표만 다시) + 손 크롭 74 (부록 그림 A.1 · A.2 · 패널 7 = 8a · 9a · 10a · 14a · A.1a–c · 식 40 · 근거 문단 25).  본 뒤 다시 자른 손 크롭 = 식 (37) (두 번 — 아래 문단의 근호 조각) · `fig_10a` (색 막대 글자 조각) · 근거 문단 4 장 (p1 · p8 · p12 · p15) · 이름 고침 1 장.  89 장 전부 열어 확인 (식 · 문단은 원 해상도 묶음 · 그림은 낱장 또는 묶음 · 끝에 모음 그림 두 장).  패널 크롭 8a · 9a · 10a 는 쪽에 박힌 래스터를 메모리 사본에서 숨기고 **벡터 층만** 그린 것이라 플롯의 오른쪽 틀 선 (래스터에 들어 있음) 이 빠져 있다 — 손대지 않은 모습은 `fig_8.png` · `fig_9.png` · `fig_10.png`.  `figures.json` 의 `recrop` · `manual_crop` · `crop_note` · `note_manual`.
- 식 크롭: 표시 식 40 개를 식 번호별로 400 dpi · 흰 여백 7 pt — 위아래 본문 글자는 쪽의 메모리 사본에서 지우고 (그림 · 선은 그대로) 식의 잉크 상자만 잘랐다.
- 판독: digitized.csv 1155 행 — 축 보정 눈금 · 방법을 그림마다 note 열에.  같은 실험 곡선의 끝값이 여덟 그림에서 171.7–171.8 로 재현.  인쇄값과의 대조: 본문 "186 mAh g⁻¹" ↔ 판독 185.6 · 186.5 · Fig. 3 캡션 "≈15 %" ↔ 판독 14.5 % · 본문 x 0.25–0.70 ↔ 색 눈금 0.3–0.7.
- 2 차 인용 대조: 정본 카드 lei2026 (L115 · L144 · L162 · L172 · L174 · L213 · L234) · liang2026 (L246) · zhang2026_polymer (L124) — 고치지 않았다 (카드 문제 = 정독 출력 batch_101 의 "카드 문제" 절).  다른 카드 대조: kodama2020 · bielefeld2020 · doerrer2021 · mcgrogan2017 · deng2016 · bucci2017 · lee2025_heckel · koerver2018 (각 카드의 해당 줄).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (taghikhani* 없음) + DOI (10.1016/j.jmps.2025.106060 · 106060) · 제목 낱말 grep — 인용만 (lei2026 · liang2026 · zhang2026_polymer) · 카드 없음 (2026-11-12 · 시작할 때와 쓰기 직전 두 번).

## 🔗 관련 카드
- 이 논문을 가리킨 리뷰: `lei2026_se_particle_size_effects_review` · `liang2026_interface_bottleneck_solid_state_batteries` · `zhang2026_polymer_electrolyte_modeling_perspective`.
- 미세구조 분해 전기화학 모형 (선행): `bielefeld2019_microstructural_modeling_composite_cathode` · `bielefeld2020_effective_ionic_conductivity_binder`.
- 화학–역학 파괴 · 박리 모형: `bucci2017_chemomech_failure_assb_cycling_czm` · `bucci2018_mechanical_instability_interface_delamination` · `barai2021_delamination_cathode_llzo_multiscale` · `tian2020_electrochemo_mechanical_stress_assb` · `park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics` (2D 선형 탄성 응력) · `jeong2024_operando_densification_chemomechanics_se_size_composite_cathode` (선형 탄성 메조 모형).
- 재료 값의 출처: `mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation` · `deng2016_elastic_superionic_electrolytes_dft` · `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` · `lee2025_heckel_argyrodite_powder_densification_nanoindentation`.
- 실험 쪽 이웃: `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` (NCM-811 격자 부피 변화 · 구속 셀 응력) · `doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density` · `trevisanello2021_sc_pc_ncm_cracking_diffusion` · `kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation` · `minnmann2021_jes_charge_transport_bottlenecks` · `minnmann2022_designing_cathodes_solidstate` · `shi2019_high_am_loading_particle_size_assb`.
- 화학–역학 리뷰: `li2026_electrochemomechanical_coupling_asslmb_review`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
