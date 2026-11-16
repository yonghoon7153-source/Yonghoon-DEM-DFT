<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 후보 표 1 순위 N-51 · 정독 91) 에서 꼭 뽑으라고 한 항목.
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표).  같은 축 (무른 입자 압밀 · 입자 해상) 의 이웃 = cardenasbarrantes2022_soft_spheres_3d_compaction_nscd.md (이 논문 ref 14).
     두 필수 절 = §0-1 고른 의도 대조 · §8 자세한 분석.
     원문 = 정정판 (Soft Matter 2024, 20, 1702–1718 · 17 쪽 · 'Note added after first publication' — 2024-08-30 판이 2024-01-29 원판을 대체 · 식 (3) · (4) 정정).  보충 자료 (ESI) 없음 (본문 'ESI' 0 회).
     쪽 표기 = PDF 쪽 p.1–17 (인쇄 쪽 = PDF 쪽 + 1701 · p.1 = 1702).  크롭 파일 이름의 pN 과 figures.json 의 page 는 PDF 쪽이다.
     값 표지: [인쇄] = 본문 · 캡션 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 275 행 — 그림은 PDF 안 300 dpi 래스터라 300 dpi 쪽 렌더 = 원본 해상도 ·
     축 = 프레임 안쪽 눈금 위치의 선형 / 로그 맞춤 · 표지 = 범례에서 뽑은 색에 가장 가까운 색의 연결 성분 테두리 상자 중심 · 겹친 표지는 조각 · 묶음으로 남아 경향만) ·
     [판독 · 눈금] = 픽셀 자 없이 눈금에 대 본 값 · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 ·
     [다른 카드] = 정본의 다른 카드 (slug 병기) · [우리] / [우리 산술] = 우리 쪽 값 (CLAUDE.md 출처) 과 견주는 계산 · [미확인] = 17 쪽 전수에 없음.
     원문 17 쪽은 글자 층 추출 + 그림 · 식 · 근거 문단 렌더로 전부 읽었다.  글자 층은 ν → 'n' · φ → 'f' · '<' → 'o' · '~' → 'B' 로 깨지고 '−' 부호를 잃는다 — 부호 · 기호는 렌더에서 확인했다.
     실험 없음 · 전지 재료 없음 — 일반 입상체 (k · d · m 무차원 단위) 계산. -->
# 결합입자 모델 (BPM) 로 탄성 변형 입자의 3D 침대를 재밍 너머 고압까지 누르다 — 입자 1024 개 × 점 입자 ~5000 개 · 다체 결합 항으로 ν −0.11–0.4 · Hertz DEM 과 φ − φ_c ≈ 0.1 에서 갈라지지만 같은 지표 (φ_MC) 로는 압력 2 배 안 · DEM 의 φ_sphere 는 1 을 넘는다 · 입자 부피 변형률 ∝ (φ − φ_c)^{3/2} · 비구형도 지수 ~5/2 (2.3–2.7) · 침대 포아송 비 1/2 → ~1/4 → 상승 · 소성 · 탈압 없음 — Clemmer · Monti · Lechman (Soft Matter 2024)

> slug `clemmer2024_bpm_elastic_grain_compaction_beyond_jamming` · DOI `10.1039/D3SM01373A` · type `BPM 3D (LAMMPS BPM package · 회전 없는 점 입자 + 결합 · 다체 항으로 ν 조절 · 입자 1024 개 × 점 ~5000 · 등방 압밀 · 주기 경계) + Hertz DEM 대조 (LAMMPS GRANULAR · Mindlin 접선 · 구름 / 비틀림 마찰) — 선형 탄성만 (소성 · 파괴 · 응집 · 탈압 없음) · 전지 재료 없음 (무차원)` · PDF `c5736bb1-51._A_soft_departure_from_jamming_the_compaction_of_deformable_granular_matter_under_high_pressures.pdf` · digested `2026-11-12` · status ✅
>
> **저자**: **Joel T. Clemmer\*** · Joseph M. Monti · Jeremy B. Lechman — Sandia National Laboratories, Albuquerque, New Mexico 87185, USA — \* 교신 (jtclemm@sandia.gov) · *Soft Matter* **2024**, **20**, **1702–1718** (Paper · 17 쪽) · DOI 10.1039/d3sm01373a (본문 인쇄는 소문자) · 접수 2023-10-12 · 수락 2023-12-19 · 출판 2024-01-29 · **이 PDF = 2024-08-30 정정판** (*"This version of the article published 30 August 2024 replaces the original version published 29 January 2024. This corrects eqn (3) and (4) which appeared incorrectly in the original pdf."*, p.15) · © The Royal Society of Chemistry 2024 (미국 정부 비독점 이용권 유지 · CC 표기 없음) · 연구비 = Advanced Simulation and Computing program · Sandia 계약 DE-NA0003525 · 감사 = D. S. Bolintineanu · G. S. Grest · L. E. Silbert · 기여 = Clemmer (분석 · 개념 · 소프트웨어 · 초고) · Monti (분석 · 검토) · Lechman (개념 · 연구비 · 검토) (p.14 · p.16).
> **이웃 카드 (링크만)**: [`cardenasbarrantes2022_soft_spheres_3d_compaction_nscd`](cardenasbarrantes2022_soft_spheres_3d_compaction_nscd.md) (이 논문 ref 14 — 3D NSCD · 비구형도 지수 5/2 를 이 논문이 다시 얻음) · [`cantor2020_compaction_model_highly_deformable_particles`](cantor2020_compaction_model_highly_deformable_particles.md) (ref 13) · [`gonzalez2012_nonlocal_contact_confined_granular`](gonzalez2012_nonlocal_contact_confined_granular.md) (ref 27 · 비국소 DEM) · [`giannis2021_stress_based_multicontact_dem`](giannis2021_stress_based_multicontact_dem.md) (ref 75 · 다접촉 DEM) · [`luding2008_cohesive_frictional_contact_models`](luding2008_cohesive_frictional_contact_models.md) (ref 73 · 구름 / 비틀림 마찰) · [`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`](homel2017_mpm_field_gradient_partitioning_fracture_self_contact.md) (ref 33 · MPM) · [`sankar2026_fiber_scale_dem_carbon_felt_manufacturing`](sankar2026_fiber_scale_dem_carbon_felt_manufacturing.md) (이 논문을 ref 73 으로 인용 · 후보 표 근거 카드 L726) · [`tovar2026_cold_spray_cathode_composite_dem_plastic_elastic_bond`](tovar2026_cold_spray_cathode_composite_dem_plastic_elastic_bond.md) (결합 수준 소성을 넣은 결합구 입자 — 이 논문에 없는 반쪽).
> **판독 원자료**: `litdb/figures/clemmer2024_bpm_elastic_grain_compaction_beyond_jamming/digitized.csv` (275 행 — Fig. 6a 표지 · Fig. 6b 표지 · Fig. 11a 안 그림 φ_c(ν) 7 점 · Fig. 12a 안 그림 · Fig. 14a 안 그림 ν_P) · 그림 크롭 **46 장** (도구 15 중 다시 자름 3 + 손 크롭 31 = Fig. 3 · 식 10 · 근거 문단 20) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 입자 하나를 점 입자 ~5000 개의 결합망 (BPM) 으로 풀어 **선형 탄성만** 넣은 3D 단분산 입자 1024 개를 등방으로 누르면, 재밍 근처 (φ − φ_c ≲ 0.1) 에서는 점접촉 Hertz DEM 과 같은 척도 (P ∝ (φ − φ_c)^{3/2} · Z − Z_c ∝ (φ − φ_c)^{1/2}) 를 따르다가 **φ − φ_c ≈ 0.1 에서 마찰이 무관해지고 DEM 과 갈라진다** (접촉끼리의 탄성 상호작용 · 2 체 가정의 끝, p.10 · p.13 · p.14).  그래도 **같은 지표 (몬테카를로 φ_MC) 로 견주면 DEM 의 오차는 압력 2 배 안**이다 (p.9 · p.14; [판독] 같은 φ_MC 에서 P_BPM/P_DEM ≈ 1.1–1.2 (φ 0.70) → 1.4–1.5 (0.90) → 1.6–1.8 (0.95)).  단 **DEM 의 φ_sphere (구 부피 합) 는 고압에서 1 을 넘어** 쓸 수 없다 (P/E_eff ≈ 0.1 에서 φ_sphere ≈ 1.04–1.05, 같은 상태의 φ_MC ≈ 0.90 [판독], p.9).  입자 해상 계산만 주는 것 = **입자 부피 변형률 ∝ (φ − φ_c)^{3/2} · 비구형도 ∝ (φ − φ_c)^{~5/2} (ν 에 따라 2.3–2.7) · 침대 포아송 비 1/2 → ~1/4 → 상승**.  **소성 · 파괴 · 응집 · 탈압은 없다** — 저자: *"This comparison also assumes there is no plastic deformation or fracture in the system."* (p.14).

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 방법 — 결합입자 (BPM) 로 변형 입자 | 회전 없는 점 입자 (지름 d) · 1.5d 안 이웃 모두 결합 (점당 ~15 결합) · 결합력 = 조화 스프링 k_B(r₀,ij − r_ij) + **다체 항** a_B([(V_i+V_j)/(V₀,i+V₀,j)]^{1/3} − r_ij/r₀,ij) (식 1) · 국소 부피 대리량 V_i = Σ r_ij³ (식 2) · 감쇠 (식 3) · 다른 입자의 점끼리 = 조화 + 3 차 반발 (a_P = 50k/d²) + 감쇠 (식 4) · 입자 = 반지름 10d 구 (~5000 점) · 거친 / 매끈한 표면 두 종 = 마찰 높음 / 낮음 (마찰은 표면 요철에서만 생긴다) | [인쇄] p.3–6 · 식 (1)–(4) |
| ② ★ 보정 · 맞춘 값 | 덩어리 시편 (L = 50d · 주기) 을 변형률 0.5 % 까지 등방 압축 · 단순 전단 → K · G 맞춤 → **G/K ≈ 0.6 + 0.475 a_B/(kd)** · **K = 1.365 k/d − 0.14 k²(a_B + 1.168kd)⁻¹** · 비압축 극한 a_B ≈ −kd · 실용 한계 **ν ≲ 0.46** (순 다체력 0 구속이면 ~0.48) · 쓴 범위 ν −0.11 … 0.4 · DEM 마찰계수는 **φ_c 만 맞춤** (BPM 입자 마찰을 직접 재지 않음) | [인쇄] p.5 · p.8–9 |
| ③ ★ 해상도 · 수렴 | 탄성률 → 크기 극한 ~L⁻² · 표본 산포 ~L⁻³ᐟ² · 국소 변형률 편차 ~L⁻¹ · 이 해상도에서 거시 물성 산포 ~1 % · 국소 변형률 0.1–0.01 % · 입자 반지름 2.5 · 5 · 7.5d 를 10d 와 견준 압밀 곡선이 수렴 (7.5d ↔ 10d 차 < 표지 크기) · 선형 탄성 벗어남 ≈ 10 % at 변형률 10 % · 부피 변형률 50 % 에서 압력 ~2 배 | [인쇄] p.5 · p.6 · p.9 · p.15 |
| ④ ★ DEM (단단한 구 · 점접촉) 의 한계를 말한 문장 | *"to explicitly model elastic deformation one inevitably needs to add internal degrees of freedom to grains"* (p.2) · *"DEM simulations fail to account for elastic interactions between contacts"* (p.9) · φ_sphere > 1 (p.9) · *"In traditional DEM simulations, Poisson's ratio only affects the stiffness of Hertzian contact force"* (p.10) · 갈림점 = *"This threshold may therefore mark the end of the assumption that grain–grain interactions are two-body"* (p.13) · 그러나 *"differences never exceeded a factor of two"* (p.14) | [인쇄] p.2 · p.9 · p.10 · p.13 · p.14 |
| ⑤ ★ 소성 · 큰 변형이 왜 어려운가 · 우회 · 비용 | FEM (MPFEM · NSCD) = 구성식은 정확하지만 큰 변형에서 *"mesh entanglements"* · 파편화 표현이 어렵다 · 메시 없는 연속체 (peridynamics · MPM) = *"fairly complex and computationally expensive"* · BPM = 결합력을 설계 · 보정해야 하고 수렴 정보가 적다 (p.2) · **이 논문은 소성을 넣지 않았다** (탄성은 *"precursor to potential plastic deformation or fracture"*, p.2 · 패키지에 결합 변형률 이력으로 소성을 넣을 자리만, p.8) · 비용: **점 ~5×10⁶ · 2×10⁷ 걸음 · ~40 h · 288 (다체 없음) / 480 (다체) 프로세서** · 다체 항 = 힘 계산 ~2 배 · 회전 자유도 = ~10 배 | [인쇄] p.2 · p.4 · p.8 · p.14 |
| ⑥ ★ 2D / 3D | **3D** · Cauchy 관계: 쌍 중심력만이면 ν 가 **2D 1/3 · 3D 1/4** 로 묶인다 (p.3) · *"most simulations have either been limited to two dimensions or only explored comparisons in compaction curves to experiments"* (p.1) · 2D (Vu 2021) 에서도 E_eff 척도가 ν 차를 설명했다 (p.11) · 2D → 3D 수치 전이 없음 | [인쇄] p.1 · p.3 · p.11 |
| ⑦ ★ 압력을 뺄 때 | **다루지 않았다** — 압밀은 올리는 가지만 · 침대 탄성률은 저장 상태에서 부피 0.06 % / 전단 0.04 % 작은 변형으로 잰다 (p.13) · 탈압 · 되돌아옴 · 이력 없음 (선형 탄성이라 원칙상 전부 되돌아온다 [카드 해석]) | [인쇄] p.13 |
| ⑧ 압밀 곡선 숫자 | P/E_eff (E_eff ≡ 3K(1−2ν)/(2−2ν²)) vs φ_MC — BPM 매끈 φ 0.703 → 1.2×10⁻² · 0.756 → 2.8×10⁻² · 0.838 → 7.3×10⁻² · 0.904 → 0.14 · 0.979 → 0.42 · 0.996 → 0.83 [판독 Fig. 6b] · φ_c **0.5979** (매끈) / **0.5836** (거친) · Z_c **~5.2 / ~5.05** (DEM [4.91, 4.98] / [4.52, 4.57]) | [인쇄] p.9–10 · [판독] |
| ⑨ 재료 | **일반 입상체 · 무차원** (k · d · m) — 전지 재료 · 실험 대조 없음 | — |

⛔ **한정어 (떼지 말 것)**: ① **선형 탄성만** — 소성 · 파괴 · 응집 · 탈압 없음 (저자 스스로, p.14) ② **단분산 구 · 등방 압축 · 주기 경계** — 다이 (일축) · 벽 · 크기 분포 · 두 상 (단단한 AM + 무른 SE) 없음 ③ 압력은 **P/E_eff** 로만 (무차원) — 실제 압력 · 재료 값 없음 ④ "2 배 안" 은 **같은 지표 (φ_MC) 로 바꾼 뒤**의 말이고 선형 탄성 · 시험한 ν (−0.11–0.4) 안의 말이다 (p.14) ⑤ 마찰은 표면 요철에서만 · DEM 마찰계수와의 대응 없음 (p.6) ⑥ 큰 변형 (부피 변형률 ≳ 10 %) 의 비선형 탄성은 *"uncontrolled"* (p.6 · p.14).
⇒ **절대값 전이: 0 건** (재료 · 단위 없음).  전이되는 것은 **꼴 · 척도 · 방법** — φ_sphere 가 1 을 넘는 시점과 크기 [판독], 같은 지표에서 DEM ↔ 입자 해상 계산의 압력 차 (≤ 2 배 · 탄성 한정), 갈림점 φ − φ_c ≈ 0.1, 해상도 수렴 규칙, 그리고 **탄성만이면 실제 강성의 LPSCl 은 300 MPa 에서 φ ≈ 0.75 에 머문다**는 카드 산술 (§7-3).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-51 의 '왜' 칸)

의도 원문: *"l · e — 'bpm/rotational 의 인용처 · 결합입자로 변형 입자를 고압 압밀한다면 우리 SE 18 배 연화의 대안 경로와 맞닿는다 — 원문 미확인, 정본 카드 없음'"* (가리킨 카드 = `sankar2026_fiber_scale_dem_carbon_felt_manufacturing` L726 · 후보 표의 서지 판정 "일부만 (저자 성만 · 제목 일부)")

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "bpm/rotational 의 인용처" | **일부** | 이 논문 = LAMMPS **BPM 패키지**를 소개한 논문 (§2.6 p.8): *"Currently, the package includes an implementation of a point-particle-based model, as used in this work, as well as a more common model based on DEM particles with rotational degrees of freedom and bonds that transmit shear forces and torques.[51]"* — 회전 결합 모형의 식은 **ref 51 (Y. Wang, Acta Geotechnol., 2009)** 에 귀속되고 이 논문 자신의 계산은 **회전 없는 점 입자** 모형이다.  style 이름 'bpm/rotational' 은 원문에 **0 회** ('rotational' 8 회는 모두 설명 문장).  ⇒ 패키지 인용처로는 맞고 회전 결합 식의 출처로는 ref 51 |
| "결합입자로 변형 입자를 고압 압밀" | **채움** (탄성만) | 3D · 입자 1024 개 × 점 ~5000 개 (~5×10⁶) · 등방 · 주기 · P/E_eff 10⁻⁶ (재밍) → ~1 (φ_MC → 1) · 부피 변형률 ~60 % 상태까지 (Fig. 5 캡션) [인쇄 p.7–8 · Fig. 5–7] — **선형 탄성 입자만** |
| "우리 SE 18 배 연화의 대안 경로와 맞닿는다" | **일부** | 맞닿는 곳: (a) 입자 형상 변화 · 부피 변형 · 접촉끼리의 상호작용을 **입자를 풀어서** 낸다 (DEM 이 못 내는 정보, p.10–13) (b) 같은 지표에서 DEM 과의 차가 **압력 2 배 안**이라는 정량 (p.9 · p.14).  못 닿는 곳: **소성 없음** — 우리 18 배 연화가 묶은 재배열 · 입계 미끄럼 · 미세 파괴 · 소성 유동 (CLAUDE.md frame [2]) 은 이 모델에 없고, 저자는 연화 · 실험 보정을 말하지 않는다.  탄성만이면 LPSCl 실제 강성 (E 22.06 · ν 0.360 [우리 DFT]) 에서 300 MPa = P/E_eff ≈ 0.024 → φ_MC ≈ 0.74–0.75 ([카드 산술] · Fig. 6b [판독] · §7-3) — 랩 표준 순수 SE 기공 10–13 % (φ 0.87–0.90) 에 이 탄성 곡선으로 닿으려면 E 를 **4–6 배** 낮춰야 한다 ([카드 산술] · 단분산 · 등방 · Hertz 류 탄성 한정 · 우리 18 배 (hooke/hysteresis · 일축) 와 같은 양 아님) |
| "원문 미확인, 정본 카드 없음" | **채움 (해소)** | 이 카드로 원문 확인 · 정본 카드 생김 |
| (질문 l) 소성이 왜 어려운가 · 우회 · 비용 | **일부** | 이유 = 내부 자유도가 필요 · FEM 메시 엉킴 · 메시 없는 연속체의 비용 (p.2) · 우회 = BPM (탄성) · 비용 ~40 h × 288 / 480 프로세서 (p.8) · **소성은 넣지 않음** — 소성 · 응집은 *"previously studied using MPFEM[19]"* (p.14) |
| (질문 e) 점접촉 법칙이 큰 변형에서 깨지는 범위 · 대안 | **채움** | 단일 입자 Hertz 는 겹침/반지름 **25 %** 까지 맞는다 (매끈 입자 · Fig. 4 · p.9) · 침대에서는 **φ − φ_c ≈ 0.1** 에서 DEM 과 갈라진다 (접촉끼리의 탄성 상호작용, p.10 · p.14) · 대안 = 비국소 DEM (refs 27 · 75) *"would likely improve DEM results"* (p.14 — 시험 안 함) · Harthong 2012 MPFEM 의 접촉 독립 깨짐 φ ≈ 0.7 과 같은 자리 (p.14) |

**가리킨 카드 · 같은 저자를 언급한 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `sankar2026_…` L726 | *"ref 73 Clemmer 2024 … 제목상 'compaction of deformable granular matter under high pressures' (Soft Matter 20, 1702) 이고 `bpm/rotational` 의 인용처다. 결합입자로 변형 입자를 고압 압밀한다면 우리 SE 18 배 연화의 대안 경로와 맞닿는다 — 원문 미확인"* | 제목 = **"A soft departure from jamming: the compaction of deformable granular matter under high pressures"** (부제만 옮김) · Soft Matter **2024, 20, 1702–1718** ✓ · 저자 3 명 · `bpm/rotational` → 패키지 논문 (자기 계산 = 점 입자 모형 · 회전 결합 식 = ref 51) · "대안 경로" → 탄성 한정 | **일부** — 서지 값은 맞음 · '인용처' 는 패키지 인용으로만 맞음 |
| `sankar2026_…` L45 | *"ref 73 Clemmer 2024 (`bpm/rotational` 인용처, 제목상 …)"* | 위와 같음 | **일부** (같은 이유) |
| `sankar2026_…` L67 | *"`bpm/rotational` (refs 72–73)"* | 이 논문 = BPM 패키지 소개 · 회전 결합 식은 ref 51 (Wang 2009) | **일부** — 회전 결합 모형의 식 출처는 이 논문이 아니다 |
| `zunker2025_…` L41 · L197 · L645 | 감사절의 *"Sandia 의 Dan Bolintineanu · Joel Clemmer 가 LAMMPS 구현 도움"* · GRANULAR 서브모델 | 이 논문의 인용이 아님 (같은 저자의 다른 기여) | 대조 대상 아님 |

⇒ **의도 대조 결과: 일부** — 결합입자로 변형 입자의 3D 고압 압밀은 **채움** (탄성만); `bpm/rotational` 인용처는 패키지 인용으로만 **일부** (자기 계산은 회전 없는 점 입자 · 회전 결합 식은 ref 51); "18 배 연화의 대안 경로" 는 **일부** — 형상 · 접촉 상호작용은 주지만 연화가 묶는 소성 · 재배열은 없고, 탄성만으로는 300 MPa 에서 φ ≈ 0.75 에 머문다 ([카드 산술]).

---

## 1. 한 줄 요약
"재밍 너머 고압" 에서 입자가 변형할 때 무엇이 바뀌는지 보려고, 입자 하나를 점 입자 결합망 (BPM) 으로 풀어 선형 탄성 + 마찰 (표면 요철) 을 넣고, 결합력에 **다체 항**을 더해 입자 재료의 ν 를 −0.11 부터 0.4 까지 바꾸면서 1024 개 입자를 등방으로 φ → 1 까지 누른 뒤, 마찰계수만 맞춘 Hertz DEM 과 견준다.
결과: 재밍 근처는 알려진 척도 그대로 · **φ − φ_c ≈ 0.1 에서 세 가지가 함께 바뀐다** (마찰 무관 · 멱법칙 이탈 · DEM 이탈) · 같은 φ 지표면 DEM 오차는 2 배 안 · DEM 이 못 내는 입자 부피 변형률 · 비구형도 · 침대 탄성률은 멱법칙을 따르고 ν 에 크게 기댄다 · 침대 포아송 비는 1/2 에서 ~1/4 까지 내려갔다가 다시 오른다.
저자의 위치: *"elastic deformation always serves as a precursor to potential plastic deformation or fracture and is therefore an important limit to establish before overlaying such additional inelastic mechanisms or extending to nonlinear elasticity"* (p.2).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| J. T. Clemmer\* · J. M. Monti · J. B. Lechman (Sandia National Laboratories) | Soft Matter 20, 1702–1718 (2024) · © RSC · 이 PDF = 2024-08-30 정정판 | 10.1039/D3SM01373A | **없음** — 일반 입상체 (무차원 · 단분산 구 · 선형 탄성 · 마찰 = 요철) | BPM 3D 계산 (LAMMPS BPM 패키지) + Hertz DEM 대조 (LAMMPS GRANULAR) · 재밍 척도 이론과 대조 |

- **1저자 메모와의 대조**: 제목 · 학술지 · 권 20 · 쪽 1702–1718 · 2024 · DOI — **같다** (DOI 대소문자만 다름: 본문 인쇄 `10.1039/d3sm01373a`).  다른 점 ① 메모의 저자는 Joel T. Clemmer 한 명 → **원문 3 명** (+ Joseph M. Monti · Jeremy B. Lechman) ② 이 PDF 는 **2024-08-30 정정판** (식 (3) · (4) 정정 · 원판 출판일 2024-01-29).
- **후보 표 · 가리킨 카드의 서지**: 제목 = 부제만 (*"compaction of deformable granular matter under high pressures"*) · 저자 성만 → 위 원문 서지로 바로잡는다.
- **글의 꼴**: 1 서론 → 2 방법 (2.1 BPM 정의 · 2.2 다체 결합 식 · 2.3 보정 · 2.4 입자 생성 · 압밀 절차 · 2.5 같은 조건 DEM · 2.6 LAMMPS 구현) → 3 결과 (3.1 재밍에서 벗어남 · 마찰 의존 · 3.2 포아송 비와 입자 변형 · 3.3 침대 탄성) → 4 결론 → 부록 A (BPM 수렴) → 참고문헌 82.  그림 16 · 표 0 · 번호 식 9 · ESI 없음.
- **그룹 맥락**: 같은 저자의 앞선 BPM = refs 53 · 57 (Clemmer & Robbins, PRL 2022 · PRE 2023 — 파괴 · 보정 시험) · ref 64 (Clemmer · Long · Brown, Mech. Mater. 2023 — 결합 기준 상태 · 변형률 이력 (소성) · 비affine 운동과 비선형 탄성) · 마찰 · 재밍 = ref 5 · 24 (Santos · Bolintineanu · Grest · Lechman · Silbert …) — 정본 카드 없음.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ BPM 모델 정의 (p.3–4 · 식 (1)–(4) · Fig. 1 · `eq_01_bond_force_multibody.png` · `eq_01b_dilation_stretch_definitions.png` · `eq_02_local_volume_proxy.png` · `eq_03_bond_dissipative_force.png` · `eq_04_pair_force_nonbonded.png` · `txt_p4_volume_proxy_cost.png` · `txt_p4_pair_forces_calibration_packing.png` · `fig_1.png`)
- 점 입자 (회전 자유도 없음 · 지름 d · 질량 m) · 결합 = 중심력 · 크기 (식 1) **k_B (r₀,ij − r_ij) + a_B ( [(V_i + V_j)/(V₀,i + V₀,j)]^{1/3} − r_ij/r₀,ij )** [인쇄 p.3].
  - 첫 항 = 조화 스프링 — 홀로면 *"an elastic material with ν = 1/4 in 3D and a bulk modulus K that depends on k_B and the specific bond topology"* [인쇄 p.3].
  - 둘째 항 = 편차 꼴: 국소 부피 팽창 **D_ij ≡ [(V_i + V_j)/(V₀,i + V₀,j)]^{1/3}** 과 결합 늘음 **λ_ij ≡ r_ij/r₀,ij** 의 차 → G 를 조절하고 K 에는 영향이 작다 · 힘은 여전히 같고 반대 [인쇄 p.3].
  - Fig. 1 (네 점): 등방 수축 / 팽창은 D = λ 라 다체 항 0 → K 는 조화 항이 정한다 · 단순 전단에서 바깥 결합 넷은 서로 상쇄 · 안쪽 대각선 둘 (압축 · 신장) 에서만 D − λ 가 생긴다 → **a_B > 0 이면 전단 응력 ↑ · a_B < 0 이면 ↓** [인쇄 p.3–4].
- 국소 부피 대리량 (식 2) **V_i = Σ_{j≠i} r_ij³** (결합 이웃 합 · 비만 쓰므로 상수 무시 · 이웃이 구면에 고르게 있다고 가정) — *"this multibody formulation approximately doubles the computational time needed to calculate forces. In contrast, we find forces that account for rotational degrees of freedom can take approximately ten times longer to calculate than a simple harmonic term"* [인쇄 p.4].
- 감쇠 (식 3 · 결합 점 사이) **−Γ r̂_ij · δv⃗_ij** — DPD 꼴 · 법선 상대속도만 감쇠 · 선 · 각 운동량 보존 [인쇄 p.4].
- 결합 없는 점끼리 (식 4 · 거리 d 안 · '쌍 상호작용' · 결합 점 사이에서는 끔) **k_P (d − r_ij) + a_P (d − r_ij)³ − Γ r̂_ij · δv⃗_ij** — 3 차 항 = 매우 높은 압력에서 한 입자의 표면 점이 다른 입자 표면 점을 넘어가 두 입자가 맞물리는 것을 막는다 → 점끼리는 조금 겹쳐도 **입자 볼록 껍질 (convex hull) 끼리는 겹치지 않는다** · k_P 만 키우는 대신 3 차 항을 쓴 이유 = 재밍 근처 작은 겹침에서는 모든 힘이 같은 강성 [인쇄 p.4].
- 매개변수: **k ≡ k_B = k_P** · 시간 단위 **τ ≡ √(m/k)** · **Γ = √(km)** · **a_P = 50k/d²** · a_B 여러 값 [인쇄 p.4].
- 덩어리 결합망 만들기: 정육면체 (한 변 L) 에 지름 d 단분산 구를 **부피분율 0.64** 로 무작위 · 주기 경계 · 겹침 제거 (식 4, a_P = 0 + 점성 감쇠) → 감쇠를 끄고 rms 속도 **0.03** 으로 **1000τ** → 감쇠를 켜고 **3000τ** 냉각 → 재밍 문턱 근처 무질서 충전 → **1.5d 안 이웃 모두 결합 (점당 ~15 결합)** · 속도 0 · velocity-Verlet · **Δt = 0.1τ** [인쇄 p.4].
- ⚠ 정정판 주석: 식 (3) · (4) 는 원판 (2024-01-29) PDF 에서 잘못 인쇄됐다 [인쇄 p.15] — **원판 PDF 의 식 (3) · (4) 를 쓰지 말 것** (이 카드의 식 크롭은 정정판).

### 3-2. ★ 보정 — 탄성률 · ν 범위 (p.5 · Fig. 2 · 식 (5) · `eq_05_virial_stress_tensor.png` · `txt_p5_gk_k_fits_poisson_limit.png` · `fig_2.png`)
- 시험: L = 50d 정육면체 · 거의 준정적 변형률 속도 (더 느려도 차이 없음) · 점 위치를 전역 변형에 맞춰 affine 재배치 · **변형률 0.5 %** 까지 등방 압축 (→ K) · 단순 전단 (→ G) · 응력 = 식 (5) **σ_αβ = −(1/V)( Σ_particles v_α v_β − Σ_interactions F r_α r_β/|r⃗| )** (느린 속도라 virial 이 지배) · 최소제곱 직선 [인쇄 p.5].
- **G/K ≈ 0.6 + 0.475 a_B (kd)⁻¹** (a_B = 0 에서 ν = 1/4 ↔ G/K = 3/5 로 묶음) · 비압축 극한 (G/K = 0 · ν = 1/2) ≈ **a_B = −kd** (*"the point where the multibody force is approximately equal in magnitude to the harmonic force"*) [인쇄 p.5].
  - ⚠ 원문 오기: *"the multibody term can both increase ν above 1/4 for a_B < 0 and decrease ν below 1/4 for a_B < 0"* — 둘째 "< 0" 는 Fig. 2b (a_B > 0 에서 ν < 1/4) 와 반대다 (렌더로 확인 · "> 0" 이어야).
- **K = 1.365 k/d − 0.14 k² (a_B + 1.168 kd)⁻¹** — 비압축 근처에서 K 가 떨어진다 (압축 때 점들이 다체 항으로 압축 결합력을 줄이도록 자리를 옮김 · 비affine 변위 ↑, 부록) [인쇄 p.5].  [카드 산술] a_B = 0 → K ≈ 1.245 k/d (Fig. 2b 안 그림 ≈ 1.24 [판독 · 눈금]) → E_eff = 3K(1 − 2ν)/(2 − 2ν²) ≈ 0.996 k/d ≈ k/d.
- 불안정: *"At a_B ≤ −k_B, this can destabilize a simulation as the strength of the multibody force can exceed the harmonic force in a bond"* → 일부 점 쌍이 거의 완전히 겹침 → **실용 ν ≲ 0.46** · (a) 규칙 격자 또는 (b) 한 점이 이웃에 주는 순 다체력 = 0 구속으로 완화 → (b) 로 **ν ~0.48** · 결합 수 ↑ · 정확한 부피는 비등방 · 복잡성 때문에 쓰지 않고 *"recognize that this entails an initial calibration for K"* [인쇄 p.5].
- [카드 산술] ν = (3 − 2G/K)/(2(3 + G/K)): a_B = −0.8kd → G/K 0.22 → ν 0.398 · a_B = 3.0kd → G/K 2.025 → ν −0.105 — Fig. 10 캡션의 (a_B = −0.8kd · ν = 0.40) · (3.0kd · ν = −0.11) 와 맞는다 [인쇄 p.11 캡션].  나머지 ν (0.03 · 0.11 · 0.17 · 0.32) 에 쓴 a_B 는 인쇄되지 않았다 — 같은 식으로 역산하면 ≈ 1.6 · 0.96 · 0.52 · −0.40 kd [카드 산술 · 참고만].

### 3-3. ★ 해상도 · 수렴 (p.5–6 · p.9 · p.15–16 · Fig. 15 · 16 · `txt_p5_resolution_convergence.png` · `txt_p6_nonlinear_elasticity_limits.png` · `txt_p9_phic_resolution_convergence.png` · `fig_15.png` · `fig_16.png`)
- BPM 의 해상도 = 단위 부피당 점 입자 수 [인쇄 p.5].
- 덩어리 L = 2–200 d (점 ~10 – 10⁷ 개 · L = 200 은 실현 1 개 · 그 밖은 실현 여럿): **|K(L)/K(200) − 1| ∝ L⁻²** (모든 a_B · ν) · **σ_K(L)/K(200) ∝ L⁻³ᐟ²** (√N 척도 — 작은 영역 N ~ L³ 개의 독립 탄성률 합) · G 도 비슷한 크기 · **L ~ 16 (점 ~5000 = 입자 하나 크기) 에서 물성 산포 < 1 %** [인쇄 p.15 · Fig. 15 점선 기울기 −2 · −3/2].
- 비affine 변형률 (부피 2.5 % 압축 / 전단 2.5 % 뒤) **∝ 1/L** — 비affine 변위 자체는 크기 무관 (초기 충전의 성질 · 냉각 속도로 조절 가능) · ν 가 클수록 (비압축 근처) 압축에서 위로 이동 · 전단에서는 이동이 작다 [인쇄 p.15–16 · Fig. 16 (a) 기울기 −1].
- 이 논문 해상도에서: 입자의 거시 물성 산포 **~1 %** · 입자 안 점의 국소 변형률이 연속체 탄성해에서 **~0.1 %–0.01 %** 벗어난다 (작은 변형률) [인쇄 p.5].
- 큰 변형: 변형률이 커지면 비affine 운동 ↑ → 선형 탄성에서 벗어남 · *"this emergent nonlinear elasticity is still uncontrolled"* · 압밀된 덩어리 시편에서 **변형률 10 % 에 ≈10 %** 벗어남 (무시할 만) · 침대의 입자 부피 변형률이 이 한계를 넘는 것은 **φ ≳ 0.9** (가장 조밀한 2–3 개) · **부피 변형률 50 %** 에서 압력이 선형 예측과 **~2 배** → 가장 조밀한 침대는 비선형 탄성이 무시할 수 없을 수 있다 [인쇄 p.6].
- 압밀 곡선의 입자 해상도: 매끈 입자 반지름 **2.5 · 5 · 7.5 d** 를 10d 와 견줌 → 해상도 ↑ 면 같은 압력에서 φ 가 커지지만 (요철의 상대 크기 ↓ 일 수 있음) 수렴 · **7.5d ↔ 10d 의 φ 차 < 그림 6 표지 크기** [인쇄 p.9].  [카드 산술] 입자당 점 수 ≈ 0.64 × (2R/d)³ = 80 · 640 · 2 160 · 5 120 (R = 2.5 · 5 · 7.5 · 10 d).

### 3-4. 단일 입자 Hertz 검증 (p.6–7 · Fig. 3 · 4 · 식 (6) · `fig_3.png` · `fig_4.png` · `eq_06_hertz_force_normalization.png` · `txt_p6_rough_smoother_grains_friction.png` · `txt_p7_eeff_hertz_large_overlap.png`)
- 입자 만들기: (거친) 결합 충전에서 중심 **10d** 안 점만 남김 → **~5000 점** · 표면 불규칙 / (매끈) 결합 전 점 구를 조화 구형 벽 (강성 k · 차단 d) 안에서 진폭이 지수로 줄어드는 지름 진동 + 점성으로 표면 점을 정렬한 뒤 결합 — *"it still does not represent an ideally smooth sphere"* · 해상도 ↑ 면 요철의 상대 크기 ↓ [인쇄 p.6 · Fig. 3].
- 마찰: *"friction only emerges in a point-particle-based BPM through the geometric corrugation on the surface of grains"* → 거친 = 마찰 높음 · 매끈 = 낮음 · *"There is not a clear connection between the roughness and the friction coefficients in traditional DEM simulations and the upper and lower bounds on achievable friction coefficients are unknown"* [인쇄 p.6].
- 시험: 구를 수학적으로 매끈한 두 벽 사이에서 대칭으로 누름 · 벽 속도 **5 × 10⁻⁴ τ⁻¹** (렌더 확인) · 벽–점 조화 (강성 k · 차단 d) · 힘 = 두 벽 법선력 평균 · 질량 중심을 약한 스프링으로 붙듦 (벽–구 마찰이 없어 옆으로 빠지는 것 방지 · 법선력 영향 무시할 만) · **거친 292 개 · 매끈 50 개 (무작위 회전) 평균** [인쇄 p.6–7].
- 식 (6) **(3/(8R²E_eff)) f(δ) = (δ/R)^{3/2}** · **E_eff ≡ 3K(1 − 2ν)/(2 − 2ν²)** · δ 의 0 = 힘이 처음 **10⁻³ E_eff R²** 를 넘는 순간 · R = **10d** 로 가정 (요철 때문에 R 정의가 모호) [인쇄 p.7].  [카드 산술] E = 3K(1 − 2ν) 이므로 **E_eff = E/(2(1 − ν²))** = 같은 두 구 Hertz 접촉의 유효 탄성률 E* · Fig. 4 세로축 = f/(E_eff R²) = (8/3)(δ/R)^{3/2} (점선).
- 결과: 매끈 입자 = Hertz 와 *"markedly strong agreement"* · 거친 입자 = 더 약하고 산포 큼 (요철 = 표면 돌기 · 접촉이 바깥 점 위치에 달림) · 매끈 입자는 넓은 ν 에서 맞음 = 자유 표면 · 큰 변형에서 다체 항의 검증 · 양 끝 ν 에서 조금 더 벗어남 [인쇄 p.7] · 본문: *"the grain–grain normal forces are well described by the Hertzian model up to significant overlaps of 25% of the radius (Fig. 4)"* [인쇄 p.9].
  - [판독 · 눈금] Fig. 4b 의 ν = 0.4 곡선은 δ/R ≈ 0.15 위에서 Hertz 선 아래로 · δ/R ≈ 0.24 에서 ≈ 0.28 vs Hertz ≈ 0.31 · Fig. 4a 거친 입자 띠 ≈ 0.24–0.27.
- 큰 압입: FEM 연구는 Hertz 가 큰 압입 깊이에서 법선력을 **과소 예측**한다고 했다 (ref 68) · 거의 선형 탄성 실리콘을 단단한 구로 누른 실험은 Fig. 4 보다 깊은 압입까지 Hertz 와 잘 맞았다 (ref 69) · 요철 · 큰 변형 비선형 탄성이 *"coincidentally"* 일치를 좋게 할 수 있다 [인쇄 p.7].

### 3-5. ★ 출발 상태 · 압밀 절차 · 비용 (p.7–8 · Fig. 5 · `fig_5.png` · `txt_p7_compaction_protocol.png` · `txt_p8_dem_matching_lammps_cost.png`)
- 출발: 전통 DEM 으로 만든 **입자 1024 개 · 부피분율 57 %** 느슨한 충전 틀 (ref 70 · Fig. 5a 는 128 개 = 1/8) → 틀 자리에 BPM 입자를 놓음 (주기 경계를 넘는 점 · 결합 재배치) → 이완 · 살짝 팽창해 접촉을 모두 끊음 → 결합 평형 길이 재설정 → **재밍 바로 아래의 무응력 입상 상태** (Fig. 5b) [인쇄 p.7].
- 재밍: **P_T = 10⁻⁶ k/d** 에서 Berendsen 압력 조절 (이득 0.1d/k · 등방 팽창 / 수축) 로 t = 2 × 10⁵ [인쇄 p.7].
- 압밀: 상자를 일정 **참 변형률 속도 ε̇** 로 세 방향 **등방** 압축 (점 위치를 상자 비율로 이동) · ε̇ 초기 **10⁻⁹ τ⁻¹** → 2 × 10⁵ 시간마다 점점 올려 **10⁻⁶ τ⁻¹** 까지 (재밍 근처 · 먼 곳을 로그로 고르게) · 점당 평균 운동에너지 늘 **< 10⁻⁶ kd²** (관성 작음) · 일부는 훨씬 느린 순수 압력 제어로 돌려 *"no identifiable differences"* · **실현 5 개 평균** [인쇄 p.7].
- Fig. 5 (c)(d) = 같은 DEM · BPM 계를 **부피 변형률 ~60 %** 로 누른 상태 — DEM 은 구가 겹치고 (c) BPM 은 입자가 다면체처럼 납작해진다 (d) [인쇄 캡션 p.7 · 그림].
- 비용: 압밀 한 번 = **점 ~5 × 10⁶ · 2 × 10⁷ 걸음 · ~40 h · 288 프로세서 (다체 없음) / 480 프로세서 (다체)** · DEM = LAMMPS GRANULAR 패키지 [인쇄 p.8].  [카드 산술] Δt = 0.1τ 이므로 2 × 10⁷ 걸음 = 2 × 10⁶ τ.
- 패키지 (§2.6): 공개 · 주 LAMMPS 배포판에 포함 · 결합 style 여럿 · 결합이 자료를 저장 (기준 상태 · 변형률 이력 = **소성 모델용**, ref 64) · 이웃과 통신 (다체) · 여러 하중 조건에서 끊김 (**파괴 · 파편화**, refs 53 · 57) · 결합 점 사이 쌍 힘을 겹치거나 끔 · 병렬 효율 [인쇄 p.8].

### 3-6. ★ 같은 조건의 DEM · φ 정의 · "2 배 안" (p.8–10 · Fig. 6 · 7 · 식 (7) · `fig_6.png` · `fig_7.png` · `eq_07_phi_sphere.png` · `txt_p8_phi_sphere_vs_phi_mc.png` · `txt_p9_phi_sphere_exceeds_unity_factor_two.png` · `txt_p10_zc_deviation_factor_two_dem_poisson.png`)
- DEM: 법선 = Hertz + Tsuji–Tanaka–Ishida 감쇠 · 접선 = Mindlin 무미끄럼 + 미끄럼 마찰 μ_s · 구름 · 비틀림 = 스프링–대시포트–슬라이더 (Luding · Marshall) μ_r · μ_t [인쇄 p.8–9].
- DEM 마찰은 **φ_c 만 맞춤** (BPM 입자에 기계 시험을 하지 않음 · Silbert · Santos 의 φ_c(μ) 에서 시작해 손으로 맞춤): **거친 ↔ {μ_s, μ_r, μ_t} = {0.3, 0, 0} · {0.15, 0.1, 0.1}** · **매끈 ↔ {0.15, 0, 0} · {0.1, 0.05, 0.05}** · *"While these values are not unique and a more rigorous fitting protocol may have arrived at different values … we would not expect a more thorough mapping between BPM and DEM simulations results to change results"* [인쇄 p.9].
- φ 정의: DEM 표준 **φ_sphere = (1/V) Σ (4/3)πR_i³** (식 7) — BPM 에는 부적합 (요철 · 변형) → **몬테카를로 φ_MC**: 상자 안 무작위 점 **10⁷** 개를 모든 점 입자 (반지름 d/2) 와 각 입자의 볼록 껍질 (점 사이 틈 포함) 에 대해 검사 → **넷째 자리** 불확도 · 재밍 근처 **φ_MC ~0.60 (매끈) · ~0.58 (거친)** at P/E_eff = 10⁻⁶ [인쇄 p.8].
- ★ **φ_sphere > 1**: *"At very high pressures in DEM simulations, deficiencies in the above definition of φ_sphere are apparent in Fig. 6(a) as it exceeds unity. As noted in other works on deformable particles, this definition does not account for overlapping regions of DEM particles … and overestimates φ. While this effect is negligible in the hard-particle limit typically studied using DEM, it is significant in the high pressure limit."* → DEM 에도 φ_MC (**10⁶** 점) [인쇄 p.9].
  - [판독 Fig. 6a ↔ 6b, 같은 압력의 같은 점]: DEM {0.1, 0.05, 0.05} — P/E_eff ≈ 6 × 10⁻³: φ_sphere 0.678 ↔ φ_MC 0.674 · ≈ 10⁻²: 0.708 ↔ 0.700 · ≈ 2 × 10⁻²: 0.767 ↔ 0.749 · ≈ 4 × 10⁻²: 0.855 ↔ 0.811 · ≈ 6 × 10⁻²: 0.928 ↔ 0.854 / DEM {0.15, 0.1, 0.1} — ≈ 0.10: **1.045 ↔ 0.899** → [카드 산술] **Δφ = 0.004 · 0.008 · 0.018 · 0.044 · 0.074 · 0.146**.  P/E_eff ≈ 0.1 에서 φ_sphere 로 잰 기공률 = **−4.5 %** · φ_MC 로 잰 기공률 = **≈ 10 %**.  (Fig. 6a 의 가로축은 ≈ 1.07 에서 끝나 더 높은 압력의 DEM 점은 그림 밖이다 [카드 해석].)
- 압밀 곡선 (Fig. 6b · P/E_eff vs φ_MC · [판독] · 로그 압력 선형 보간 [카드 산술]):

  | φ_MC | BPM 매끈 | BPM 거친 | DEM {0.1, 0.05, 0.05} (매끈 짝) | DEM {0.15, 0.1, 0.1} (거친 짝) | P_BPM/P_DEM (매끈 · 거친) |
  |---|---|---|---|---|---|
  | 0.70 | 1.15 × 10⁻² | 1.27 × 10⁻² | 0.97 × 10⁻² | 1.17 × 10⁻² | 1.18 · 1.09 |
  | 0.75 | 2.5 × 10⁻² | 2.7 × 10⁻² | 2.0 × 10⁻² | 2.3 × 10⁻² | 1.25 · 1.19 |
  | 0.80 | 4.7 × 10⁻² | 4.9 × 10⁻² | 3.6 × 10⁻² | 4.1 × 10⁻² | 1.30 · 1.20 |
  | 0.85 | 8.2 × 10⁻² | 8.4 × 10⁻² | 5.8 × 10⁻² | 6.4 × 10⁻² | 1.42 · 1.31 |
  | 0.90 | 0.138 | 0.142 | 0.094 | 0.101 | 1.47 · 1.41 |
  | 0.95 | 0.275 | 0.269 | 0.156 | 0.171 | 1.76 · 1.58 |

  - 원문: *"Comparing DEM and BPM results, the shape of compaction curves is now qualitatively quite similar and we see errors associated with DEM are limited to within about a factor of two."* [인쇄 p.9] — [카드 해석] 판독상 DEM 이 **같은 φ_MC 에 더 낮은 압력** (더 무르다) 이고 그 차가 φ 와 함께 커진다.  같은 부호의 3D 증거 = `cardenasbarrantes2022_soft_spheres_3d_compaction_nscd` (NSCD · 점접촉 DEM 이 P/E\* ≈ 0.04 위에서 더 조밀한 쪽으로) [다른 카드].
  - 거친 · 매끈 BPM 곡선은 φ ≈ 0.7 에서 한 곡선으로 모인다 (*"compaction curves for the two BPM systems coalesce as friction becomes irrelevant"*) — *"tangential forces become less relevant as particles become fully confined by large normal forces and can no longer rotate"* · 처음 (재밍 근처) DEM ↔ BPM 의 φ 차는 짝끼리 **≤ 0.003** [인쇄 p.9].
- 원인 설명 (저자): Hertz 가 겹침 25 % 까지 맞으므로 차가 크지 않은 것이 놀랍지 않다 · DEM 은 접촉끼리의 탄성 상호작용을 못 넣는다 (비국소 DEM 이 더 나을 것, refs 27 · 75) · DEM 은 완전 선형 탄성이고 BPM 도 넓은 선형 범위라 **비선형이 크면 차가 더 벌어질 것** · neo-Hookean 재료로 시험하자는 제안 [인쇄 p.9].
- 끝: BPM 은 φ_MC → 1 에서 압력이 치솟는다 (φ ≈ 0.98 → P/E_eff ≈ 0.4 · ≈ 0.996 → ≈ 0.7–0.8 [판독]) · DEM φ_MC 곡선은 φ = 1.0 에서 P/E_eff ~1–2 까지 [판독 · 눈금] · *"the expected upturn in pressure at the maximum packing fraction of 1.0 is now visible in DEM results"* [인쇄 p.9].

### 3-7. 재밍 척도 · 갈림점 φ − φ_c ≈ 0.1 (p.9–11 · Fig. 7–9 · 11 · `fig_7.png` · `fig_8.png` · `fig_9.png` · `fig_11.png` · `txt_p9_phic_resolution_convergence.png`)
- φ_c: 최소 φ 에서 시작해 작은 φ − φ_c 의 **P ∝ (φ − φ_c)^{3/2}** (Hertz 재밍, ref 76) 구간을 최대화하도록 손맞춤 → **BPM φ_c = 0.5979 (매끈 · 마찰 낮음) · 0.5836 (거친 · 마찰 높음)** · 척도는 **φ − φ_c ~ 10⁻¹** 까지 · 그 뒤 φ → 1 로 가며 압력이 가속 · 이 문턱 ≈ 마찰이 무관해지고 BPM–DEM 이 갈라지는 점 [인쇄 p.9 · Fig. 7 기울기 3/2].
- Z: rattler (접촉 ≤ 2) 제외 · **Z_force** = 두 입자의 점끼리 닿으면 접촉 · **Z_geometry** = 질량 중심 거리 < 차단 (입자 안 점의 최대 거리 평균 × 2 + d = **20.27d (매끈) · 20.53d (거친)**) [인쇄 p.10–11].  Z_force 는 재밍 근처에서 BPM 이 DEM 보다 체계적으로 높다 (요철 · 힘을 안정에 쓰지 않는 접촉도 셈) · Z_geometry 는 DEM 과 비슷 (높은 / 낮은 마찰 DEM 사이) 하지만 φ → 1 에서 덜 오른다 (입자 변형을 안 셈) [인쇄 p.10–11].
- **Z_c** (Z_force 최솟값에서 손맞춤): **BPM ~5.05 (거친) · ~5.2 (매끈)** · **DEM ∈ [4.52, 4.57] (높은 마찰) · ∈ [4.91, 4.98] (낮은 마찰)** · 마찰 없는 3D 등정 Z_c = 6 · **Z − Z_c ∝ (φ − φ_c)^{1/2}** 확인 (Fig. 9 기울기 1/2 · BPM 은 Z_force) [인쇄 p.10–11].
- 갈림: *"BPM simulations reproduce the expected scaling near the jamming transition until deviations set in at φ−φ_c ~ 0.1. This transition also corresponds to a limit where friction becomes less important and the internal deformation of grains becomes relevant … However, if one considers analogous metrics, the predictions from DEM are still within a factor of two from the BPM simulations suggesting results from DEM simulations can still be somewhat informative far from the hard-sphere limit assuming systems are nearly linear elastic."* [인쇄 p.10].
- ν 를 바꾼 매끈 BPM (ν −0.11 … 0.4 · Fig. 11): P/E_eff(φ − φ_c) · Z_force − Z_c (Z_c = 5.2 고정) 는 **E_eff 척도를 빼면 ν 에 거의 무관** — φ → 1 가까이까지 [인쇄 p.11] · φ_c 는 ν ↑ 와 함께 조금 준다: **0.5981 (−0.11) · 0.5983 (0.03) · 0.5981 (0.11) · 0.5980 (0.17) · 0.5979 (0.25) · 0.5978 (0.32) · 0.5977 (0.4)** [판독 Fig. 11a 안 그림 · ν = 0.25 값이 인쇄 0.5979 를 재현].
- [판독 · 눈금] Fig. 8: φ − φ_c ≈ 0.4 에서 Z_force ≈ 13–14 (BPM · DEM) · Z_geometry (BPM) ≈ 10.8–11.5.

### 3-8. ★ 포아송 비와 입자 변형 — DEM 이 못 내는 양 (p.10–13 · Fig. 10 · 12 · 13 · 식 (8) · (9) · `fig_10.png` · `fig_12.png` · `fig_13.png` · `eq_08_grain_volumetric_strain.png` · `eq_09_asphericity.png` · `txt_p12_volumetric_strain_asphericity_exponents.png`)
- DEM 에서 ν 는 Hertz 강성만 바꾼다 → *"DEM simulations produce trivially identical results as stresses are simply scaled by a constant factor, E_eff"* — 그래서 이 절은 BPM (매끈 · 마찰 낮음) 만 [인쇄 p.10].
- Fig. 10: 같은 상자 부피로 누른 **ν = 0.40 (a_B = −0.8kd · φ = 0.86)** ↔ **ν = −0.11 (a_B = 3.0kd · φ = 0.80)** — ν 높은 (비압축에 가까운) 입자는 접촉에서 납작해져 형상이 많이 바뀌고, 음의 ν (auxetic) 입자는 구형을 유지하는 대신 부피가 더 줄어 φ 가 낮다 [인쇄 p.11 · 캡션 렌더 확인].
- 정의 (입자 점들의 볼록 껍질에서 V_g · A_g): **부피 변형률 ε_V_g ≡ (V₀,g − V_g)/V₀,g** (식 8) · **비구형도 α ≡ A_g^{3/2}/(6√π V_g)** (식 9 · 구 = 1 · 그 밖 > 1 · refs 14 · 20 과 같은 정의) [인쇄 p.11].
- 부피 변형률: ⟨ε_V⟩ ∝ **(φ − φ_c)^{3/2}** — 거시 압력과 비례해 움직인다 · φ − φ_c ~ 0.1 뒤 가속 (빈 곳이 차며 φ → 1) · ν ↑ 면 아래로 · *"grains with ν = 0.4 experience approximately a quarter of the volumetric compression of grains with a near-zero Poisson's ratio at very large pressures"* [인쇄 p.12].
  - [카드 산술] 같은 P/E_eff 에서 입자 부피 변형 ∝ 1/K · K/E_eff = (2 − 2ν²)/(3(1 − 2ν)) → ν 0.03 : 0.709 · ν 0.4 : 2.8 → 1/K 비 **0.25** = "a quarter" 와 같은 꼴 (선형 탄성 산술).
  - [판독 Fig. 12a 안 그림] ε_V (φ − φ_c)^{−3/2} 의 평탄 구간 (φ − φ_c ≈ 0.004–0.016): ν −0.11 ≈ 0.49–0.56 · 0.03 ≈ 0.41–0.46 · 0.25 ≈ 0.26 · 0.4 ≈ 0.15 · 가장 조밀한 점: ν −0.11 (φ − φ_c 0.377) ≈ 2.19 → [카드 산술] ε_V ≈ 2.19 × 0.377^{1.5} ≈ **0.51** · ν 0.4 (0.331) ≈ 0.57 → ε_V ≈ 0.11 (표지가 심하게 겹쳐 거칢).
- 비구형도: 무압 α₀ **~1.002** (점 입자로 구를 만든 결함) · α − α₀ 는 **φ − φ_c ~ 10⁻³** 위에서 지수 **~5/2** (ν = 1/4) 로 자란다 — Cárdenas-Barrantes (NSCD) 와 같은 지수 · φ − φ_c ~ 0.1 뒤 가속 · ν 에 따라 지수 **2.3 (ν = 0.4) ~ 2.7 (ν = −0.11)** 로 읽을 수 있다 · φ − φ_c ~ 10⁻³ 에서 α 가 ν 에 따라 **~5 배** 차 · φ → 1 에서는 모인다 (*"As spheres can never fully fill a volume, grains must distort in this limit"*) · 더 넓은 척도 구간에는 **α < 10⁻³** 을 푸는 고해상도 입자가 필요 [인쇄 p.12].
- 분포: 입자별 ε_V · α 는 모든 경우 (거친 / 매끈 · ν) **거의 정규분포** (z-점수) · 평균과 표준편차가 같은 멱법칙으로 자라고 분포 꼴은 압력에 거의 무관 (Fig. 13 · P/E_eff = **1.3 × 10⁻⁵ · 9.2 × 10⁻⁵ · 1.6 × 10⁻³ · 1.2 × 10⁻² · 7.3 × 10⁻²** [인쇄 범례] · ν = 1/4) · *"To predict yield and the accumulation of damage in powders, it is important to know the likelihood of a particular strain state in grains"* [인쇄 p.12–13] · [판독 · 눈금] 로그 안 그림에서 |z| ≳ 3 꼬리는 정규 곡선 위로 조금 벗어난다 (특히 α 의 +쪽).

### 3-9. 침대 (packing) 의 탄성 — 탈압의 첫 자료 (p.13 · Fig. 14 · `fig_14.png` · `txt_p13_packing_poisson_minimum_two_body.png`)
- 측정: 압밀 중 저장 → **10⁵ 걸음** 이완 → **부피 0.06 %** (참 변형률 속도 10⁻⁸ τ⁻¹) 또는 **전단 0.04 %** (2 × 10⁻⁸ τ⁻¹) 를 걸어 직선 맞춤 · 입자 재배열 허용 · **실현 5 개 중 2 개만** [인쇄 p.13 · 렌더 확인].
- **K_P ∝ (φ − φ_c)^{1/2}** · **G_P ∝ (φ − φ_c)** (재배열 허용 · 비affine) — 그 뒤 가속 [인쇄 p.13 · Fig. 14 기울기 1/2 · 1].  ⚠ Fig. 14 세로축의 정규화 (E_eff 인지 k/d 인지) [미확인].
- ν_P: 재밍 근처 **1/2** (G_P ≪ K_P · 입자 재료 ν 와 무관) → G_P 가 빨리 커져 감소 → **φ − φ_c ~ 0.1 에서 최소 ~1/4** (*"particularly in the dataset with ν = −0.11"*) → 다시 상승 (자유 부피가 사라지며 K_P 가 빨리 커짐 · 돌기가 납작해져 접촉 미끄럼이 쉬워져 G_P/K_P ↓) [인쇄 p.13].  [판독 Fig. 14a 안 그림] 최솟값 ≈ **0.26** (ν −0.11 · φ − φ_c ≈ 0.14) · ≈ **0.29** (ν 0.4 · ≈ 0.05) · ≈ **0.30** (ν 0.25 · ≈ 0.1) · 마지막 점 ≈ 0.32–0.39.
- 해석 (저자 · 확정 아님): 최소 1/4 은 Cauchy 관계 (쌍 중심력 → 3D ν = 1/4) 의 반영일 수 있다 — 그 압력에서 접촉 위상이 굳고 마찰이 무관해져 힘이 사실상 중심력 · 더 높은 φ 에서 BPM–DEM 이 갈라짐 = 접촉이 비Hertz · 서로 탄성 상호작용 → *"This threshold may therefore mark the end of the assumption that grain–grain interactions are two-body."* · 실험 (Carnavas & Page 1998 · Hentschel & Page 2007) 도 압밀 분말 (구리 · 강 · 알루미늄 · 유리) 에서 ν 최소 ~1/4 또는 조금 위를 보였다 [인쇄 p.13].

### 3-10. ★ 저자 한계 · 원문 안 어긋남
**저자 한계 (원문)**: ① 탄성만 — *"This comparison also assumes there is no plastic deformation or fracture in the system"* · *"many applications also depend on the activation of inelastic mechanisms not modeled here such as plasticity and cohesion as previously studied using MPFEM"* (p.14) ② 단분산 · 결함 없는 구 · 큰 변형의 비선형 탄성 미통제 — *"a rigorous characterization of deviations from linear elasticity at large volumetric strains ≳10% and frictional forces are uncharacterized"* (p.14) ③ 마찰 ↔ 요철 대응 · 마찰계수의 상한 / 하한 모름 (p.6) ④ BPM 은 결합력 설계 · 보정이 미리 정해지지 않고 FEM 처럼 수렴 정보가 많지 않다 (p.2) ⑤ ν_P 최소의 해석은 *"detailed characterization of grain–grain forces and more accurate measurements of elastic moduli are necessary"* (p.13) ⑥ 마찰 · 요철은 전단 등 다른 변형에서 더 중요할 수 있다 (p.14).
**원문 안 어긋남 (카드가 본 것 — 고치지 않고 적는다)**:
1. p.5 *"decrease ν below 1/4 for a_B < 0"* — Fig. 2b 와 반대 (a_B > 0 이어야 · 렌더 확인).
2. 불안정 문턱 *"a_B ≤ −k_B"* (p.5) — a_B 의 단위는 kd (힘) 인데 k_B (강성) 로 적힘 (같은 쪽의 비압축 극한은 a_B ≈ −kd).
3. ν 라벨의 반올림 차: Fig. 4b · 15 · 16 범례 −0.1 · 0.1 ↔ Fig. 11 · 12 · 14 · 본문 −0.11 · 0.11.
4. 결론 p.14 *"we varied the Poisson's ratio of grains v from 0.4 to 0.11"* — ν 를 v 로 적고 아래 끝의 부호가 빠짐 (같은 결론 오른쪽 단은 *"2.7 at ν = −0.11"*).
5. Fig. 16 캡션은 (a) 의 기울기 −1 만 적고 (b) 의 점선은 설명하지 않는다.
6. p.9 *"less than the size of as symbol"* (오타).
7. 그림 세로축: Fig. 12a 의 눈금 글자가 10², 10⁻¹, 10⁻⁴ (부피 변형률 축이 10² 까지 그려짐 · 자료는 ≲ 0.6) · Fig. 14 세로축 단위 없음.

---

## 4. ★ 방법 — 계산 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 계산 사슬
덩어리 결합망 (L = 50d) 으로 K · G 보정 → 구 입자 잘라내기 (거친 / 매끈 · ~5000 점) → 단일 입자 Hertz 검증 (두 벽 · 292 / 50 개) → DEM 느슨한 틀 (1024 개 · 57 %) 에 BPM 입자 배치 → 무응력 재설정 → P_T = 10⁻⁶ k/d 재밍 → 등방 일정 참 변형률 속도 압밀 (10⁻⁹ → 10⁻⁶ τ⁻¹ · 실현 5) → φ_MC · Z_force · Z_geometry · ε_V · α → (저장 상태) 작은 변형 탄성률 K_P · G_P · ν_P (실현 2).  같은 틀로 DEM (Hertz + Mindlin + 구름 / 비틀림 · 마찰 4 짝) 압밀 → φ_sphere · φ_MC · Z.

### 4-2. 입자 처리 ★
- 입자 = 점 입자 ~5000 개의 결합망 → **입자 형상 변화 (탄성) 를 실제로 푼다** (DEM 의 겹침 대리가 아니다) · 입자 볼록 껍질끼리 겹치지 않는다 (3 차 반발).
- 소성 · 파괴 · 응집 없음 — 결합은 끊어지지 않고 기준 상태도 바뀌지 않는다 (패키지에는 끊김 · 변형률 이력 기능이 있으나 이 논문은 선형 탄성만 다룬다, p.8 · p.14).
- 마찰 = 표면 요철 (기하) 에서만 · 입자 간 마찰계수 입력 없음.
- 단분산 (모든 입자 반지름 10d) · 한 상.
- DEM 쪽: 단단한 구 + Hertz (겹침 대리) · 접촉 독립 · 형상 불변.

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — §0 표 ④ (p.2 · p.9 · p.10 · p.13 · p.14) + 정량: φ_sphere > 1 (p.9 · [판독] Δφ 0.15 at P/E_eff 0.1) · 갈림점 φ − φ_c ≈ 0.1 · 같은 지표 압력 오차 ≤ 2 배 (선형 탄성 한정 · [판독] 1.1–1.8).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — p.2 의 세 길 (FEM = 메시 엉킴 · 파편화 · 메시 없는 연속체 = 복잡 · 비쌈 · BPM = 결합력 설계 · 보정 · 수렴 정보 부족) + 이 논문 비용 (p.8: 점 5 × 10⁶ · 2 × 10⁷ 걸음 · ~40 h · 288 / 480 프로세서) + 다체 ×2 · 회전 ×10 (p.4).  **우회는 탄성까지만** — 소성은 *"precursor"* (p.2) · 패키지 기능 (p.8) · MPFEM 선행 연구 (p.14) 로만 언급.
3. **2D / 3D** — 3D · Cauchy 2D 1/3 vs 3D 1/4 (p.3) · *"most simulations have either been limited to two dimensions …"* (p.1) · 2D (Vu 2021) 의 E_eff 척도와 같은 결론 (p.11) · 2D → 3D 수치 전이 없음.
4. **압력을 뺄 때** — 없음 (§3-9 의 작은 변형 탄성률은 탈압 곡선이 아니다).

### 4-4. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| BPM (bonded particle model) | 입자 (알갱이) 하나를 점 입자 묶음 + 미리 정한 결합망으로 표현 · 결합의 상대 변위 = 내부 변형률 · 무응력 기준 상태가 분명함 |
| 다체 (multibody) 항 | 결합력에 두 점 주변 국소 부피 변화 (D_ij) 와 결합 늘음 (λ_ij) 의 차를 넣어 G/K (= ν) 를 조절 |
| Cauchy 관계 | 쌍 중심력만 쓰는 무질서 충전의 ν 가 2D 1/3 · 3D 1/4 로 묶이는 제약 |
| 재밍 · φ_c | 압력을 버티기 시작하는 충전율 · 마찰이 클수록 낮다 |
| φ_sphere | 구 부피 합 / 상자 부피 (겹친 몫을 두 번 셈) |
| φ_MC | 무작위 점이 점 입자 (d/2 구) 또는 입자 볼록 껍질 안에 드는 비율 (합집합 · 몬테카를로) |
| E_eff | 3K(1 − 2ν)/(2 − 2ν²) = E/(2(1 − ν²)) — 같은 두 구 Hertz 유효 탄성률 · 압력 무차원화 |
| Z_force · Z_geometry | 점끼리 힘이 오가면 접촉 / 질량 중심 거리 기준 접촉 |
| rattler | 접촉 ≤ 2 인 입자 (Z 에서 뺌) |
| 비구형도 α | A^{3/2}/(6√π V) (볼록 껍질) · 구 = 1 |
| ν_P | 침대 (packing) 자체의 포아송 비 (K_P · G_P 에서) |
| auxetic | ν < 0 (한 방향으로 누르면 옆도 줄어듦) |
| 비affine 변위 | 전역 변형을 그대로 따른 위치에서 벗어난 몫 |

---

## 5. Figure set ★
| 그림 | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| **Fig. 1** (`fig_1.png`) | 네 점 결합망의 등방 수축 · 팽창 · 단순 전단 (빨강 점선 = 줄어든 결합 · 초록 점선 = 늘어난 결합) | 다체 항이 전단에서만 켜지는 이유 — 보고서 방법 절 |
| **Fig. 2** (`fig_2.png`) | (a) G/K vs a_B (점선 G/K = 0.6 · a_B = 0) (b) ν vs a_B + 안 그림 K vs a_B · 빨간 선 = 맞춤식 | ν 범위 (−0.1 … 0.47) · 비압축 근처 K 감소 — 보정 표 |
| **Fig. 3** (`fig_3.png`, 손 크롭) | 거친 / 매끈 입자 (~5000 점) 렌더 | 입자 해상 = 점 5000 개의 감각 |
| **Fig. 4** (`fig_4.png`) | (a) f/(E_eff R²) vs 겹침/반지름 — 거친 (파랑 · 띠 = 1 표준편차) · 매끈 (빨강) · Hertz (검정 점선) (b) 매끈 7 ν · 안 그림 로그 (수평 점선 = 10⁻³ E_eff R² 문턱 · 기울기 3/2) | ★ 단위 시험 U1 / U5 꼴 (구 하나 두 벽 압축 → Hertz · 겹침 25 % 까지) — 우리 MPM 입자 하나 압축 시험의 대조 선 |
| **Fig. 5** (`fig_5.png`, 다시 자름) | (a) DEM 128 입자 느슨한 틀 (b) 같은 BPM (c)(d) 부피 변형률 ~60 % 의 DEM · BPM | DEM 겹침 (c) vs BPM 형상 변화 (d) — φ_sphere 문제의 그림 |
| **Fig. 6** (`fig_6.png`) | P/E_eff vs φ — (a) DEM φ_sphere (1 을 넘음) (b) DEM φ_MC · 안 그림 재밍 근처 (0.58–0.61) · 점선 φ 0.5836 · 0.5979 · 1.0 | ★★ 기공 연산자 반면교사 + 탄성만의 압밀 곡선 (§3-6 표) |
| **Fig. 7** (`fig_7.png`) | P/E_eff vs φ − φ_c (로그–로그 · 점선 기울기 3/2) | 갈림점 φ − φ_c ≈ 0.1 |
| **Fig. 8** (`fig_8.png`) | Z_force (a) · Z_geometry (b) vs φ − φ_c (Z < 14 만) | 접촉 수 정의 차 — 우리 CN 정의 표지 |
| **Fig. 9** (`fig_9.png`) | Z_force − Z_c vs φ − φ_c (점선 기울기 1/2) | 척도 확인 |
| **Fig. 10** (`fig_10.png`) | 1024 입자 침대 렌더 — ν 0.40 (φ 0.86) vs −0.11 (φ 0.80) 같은 부피 · 결합 수로 색칠 | 입자 형상 변화의 3D 그림 (탄성) |
| **Fig. 11** (`fig_11.png`, 다시 자름) | (a) 7 ν 의 P/E_eff vs φ − φ_c + 안 그림 φ_c(ν) (b) Z_force − Z_c | P 곡선이 ν 에 무관 (E_eff 척도) |
| **Fig. 12** (`fig_12.png`) | (a) ⟨ε_V⟩ (기울기 3/2) + 안 그림 ε_V (φ − φ_c)^{−3/2} (b) ⟨α − α₀⟩ (5/2) + 안 그림 | ★ 입자 형상 · 부피 변형의 크기 — 단계 7 · R6 |
| **Fig. 13** (`fig_13.png`) | ε_V · α 의 z-점수 분포 (다섯 압력 · ν = 1/4) + 로그 안 그림 | 입자별 변형은 정규 분포 — 손상 · 파괴 확률의 출발 |
| **Fig. 14** (`fig_14.png`) | (a) K_P (기울기 1/2) + 안 그림 ν_P (b) G_P (1) · ν −0.11 · 0.25 · 0.4 | 침대 탄성률 · ν_P — 단계 6 (탈압 강성) 의 정성 기준 |
| **Fig. 15** (`fig_15.png`) | (a) \|K(L)/K(200) − 1\| (기울기 −2) (b) σ_K/K(200) (−3/2) vs L | 해상도 수렴 규칙 — 단위 시험 보고 꼴 |
| **Fig. 16** (`fig_16.png`, 다시 자름) | 평균 비affine 변형률 vs L — (a) 압축 (b) 단순 전단 (기울기 −1) | 해상도 오차의 꼴 |
| 식 크롭 10 (`eq_01`–`eq_09` · `eq_01b`) · 근거 문단 20 (`txt_p*`) | 식 (1)–(9) · 식 (1) 의 정의 문단 · 인용 문장 | 보고서 붙임 |

## 6. Post-processing ★
- **φ_MC**: 몬테카를로 — 상자 안 무작위 점 10⁷ (BPM) · 10⁶ (DEM) · 점 입자 (d/2 구) ∪ 입자 볼록 껍질 · 넷째 자리 불확도.
- **Z**: Z_force (점 접촉) · Z_geometry (20.27d · 20.53d) · rattler (≤ 2 접촉) 제외.
- **φ_c · Z_c**: 최솟값에서 시작해 멱법칙 구간을 최대화하도록 손맞춤.
- **입자 형상**: 입자별 볼록 껍질 → V_g · A_g → ε_V (식 8) · α (식 9) · α₀ 를 뺌 · z-점수 분포.
- **탄성률**: 작은 변형 직선 최소제곱 (덩어리 0.5 % · 침대 부피 0.06 % / 전단 0.04 %).
- **수렴**: 크기 L 사다리 (2–200 d) · 실현 여럿 · 평균 · 표준편차 · 입자 반지름 사다리 (2.5–10 d).
- **판독 (이 카드)**: §머리 주석 · digitized.csv 의 note 열 (축 보정 · 색 · 성분 규칙).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 하중 · 정의가 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| 입자 표현 | BPM — 입자당 점 ~5000 · 형상 변화 (탄성) | DEM = 단단한 구 + hooke/hysteresis 겹침 (형상 불변) · MPM = 연속체 (J2 소성 · 형상 변화) [우리] | BPM 은 DEM 과 MPM 사이 — 형상은 풀되 소성 없음 |
| 재료 | 무차원 선형 탄성 · ν −0.11–0.4 | LPSCl DFT E 22.06 · ν 0.360 · B₀ 26.23 GPa · DEM E_eff 1.35 GPa (18 배 연화) · MPM E 1.53 · σ_y 0.30 GPa · ν 0.49 [우리] | 절대값 비교 불가 · MPM ν 0.49 는 BPM 범위 (≲ 0.46–0.48) 밖 |
| 하중 | 등방 · 주기 · 단분산 1024 개 | 일축 다이 (판) · 벽 · 크기 분포 · 두 상 [우리] | 다른 응력 경로 |
| φ 연산자 | φ_MC (합집합 + 볼록 껍질) — φ_sphere 는 고압에서 > 1 | ε_sphere (구 부피 합 · 소성 유동의 재료 보존으로 정당화) · ε_union (확인용) · 조밀한 순수 SE 는 ε_sphere 가 음수 → ε_union [우리 · CLAUDE.md 2026-06-06] | ★ 같은 현상 · 다른 정당화 (§7-2) |
| DEM 오차 크기 | 같은 φ_MC 에서 P 차 ≤ 2 배 ([판독] 1.1–1.8) · 탄성 한정 | 연화 DEM ↔ 소성 MPM 의 차 = 구성모델 차 · 관례 오프셋 1.251 %p (real_14) [우리] | 탄성 BPM ↔ Hertz DEM 의 차는 우리 DEM ↔ MPM 차의 **탄성 몫만** |
| 갈림점 | φ − φ_c ≈ 0.1 (φ ≈ 0.69–0.70) | 순수 SE 300 MPa 의 φ ≈ 0.87–0.90 (랩 표준 10–13 %) [카드 산술] | 우리 압밀은 **2 체 접촉 가정이 깨진 영역** (φ − φ_c ≈ 0.25–0.3 — 우리 φ_c 는 [미확인] · 0.58–0.64 가정) |
| 입자 변형 | ε_V ∝ (φ − φ_c)^{3/2} · α − α₀ ∝ (φ − φ_c)^{~5/2} (탄성) | MPM 소성 형상 변화 (SEM 대조) [우리] | 탄성 형상 변화는 300 MPa LPSCl 에서 작다 (§7-3) |
| 탈압 | 없음 · ν_P · K_P · G_P (작은 변형) | 단계 6 계획 (탈압 · 되돌아옴) [우리] | 침대 탄성률의 꼴만 |

### 7-2. ★ φ_sphere > 1 ↔ 우리 ε_sphere / ε_union
- **같은 현상**: 구 겹침을 두 번 세는 φ_sphere 가 고압에서 1 을 넘는다 — [판독] P/E_eff ≈ 0.1 에서 φ_sphere ≈ 1.045 vs φ_MC ≈ 0.90 (기공 −4.5 % vs ≈ 10 %).  우리 조밀한 순수 SE DEM 의 음수 ε_sphere 와 같은 현상 [우리 · CLAUDE.md 2026-06-06].
- **다른 정당화**: 이 논문의 입자는 탄성 (부피가 실제로 준다 · 가장 조밀한 상태에서 ε_V ≈ 0.1–0.5 [판독 · 카드 산술]) 이라 합집합 (φ_MC) 이 맞다.  우리는 SE 를 거의 비압축 소성으로 보고 (부피 탄성률 ≫ 300 MPa · 탄성 부피 변형률 ≈ P/K ≈ 0.300/26.23 ≈ 1.1 % [카드 산술 · 우리 DFT B₀]) 겹친 몫이 옆으로 밀려 나온다고 보아 ε_sphere 를 쓴다.  ⇒ **연산자 선택은 입자가 부피를 보존하는가 (소성 · 큰 K) 아니면 압축되는가 (탄성 · 작은 K) 에 달려 있다** [카드 해석] — 단계 0 등록에 이 이유를 적는다.
- **크기 감각**: 이 논문의 Δφ = φ_sphere − φ_MC = 0.004 (P/E_eff 6 × 10⁻³) · 0.008 (10⁻²) · 0.018 (2 × 10⁻²) · 0.044 (4 × 10⁻²) · 0.074 (6 × 10⁻²) · 0.146 (0.1) [판독 · 카드 산술] ↔ 우리 real_14 ε_sphere ↔ ε_union ≈ 1.5 %p (13.47 vs 14.98 %) · MPM 관례 ↔ ε_sphere 1.251 %p [우리].

### 7-3. ★ 탄성만의 압밀 곡선 ↔ 우리 18 배 연화 ([카드 산술] · 정성)
- 이 논문 곡선 (Fig. 6b · BPM · 단분산 · 등방 · 마찰 있음) 에 LPSCl 실제 탄성 (E 22.06 GPa · ν 0.360 [우리 DFT]) 을 넣으면: E_eff = 22.06/(2(1 − 0.360²)) = **12.67 GPa** → 300 MPa = **P/E_eff 0.0237** → **φ_MC ≈ 0.74–0.75** (기공 ≈ 25–26 %; BPM 거친 0.740 · 매끈 0.746 · DEM 0.744–0.764) [카드 산술 · 판독 보간].
- 같은 곡선에서 랩 표준 순수 SE 기공 10–13 % (φ 0.87–0.90 — 랩 표준 · 판정하지 않음) 에 닿는 압력: P/E_eff ≈ **0.10** (φ 0.87) · **0.14** (0.90) → 300 MPa 에서 E_eff ≈ 2.9–3.0 · 2.1–2.2 GPa → E (ν 0.36) ≈ 5.1–5.2 · 3.7–3.8 GPa → 실제 22.06 대비 **4.3–6.0 배 연화** [카드 산술].
- 우리 DEM: E_eff (1.35 GPa · DEM 입력 ν 0.3) = 0.742 GPa → 명목 P/E_eff 0.40 → 이 곡선이면 φ ≈ 0.98 (기공 ≈ 2 %) — 실제 우리 순수 SE DEM 은 ε_union ≈ 10 % [우리] → **명목 P/E_eff 는 우리 DEM 으로 옮겨지지 않는다** (접촉 법칙 hooke/hysteresis ≠ Hertz · 일축 다이 ≠ 등방 주기 · 크기 분포 ≠ 단분산) — 여기의 "4–6 배" 와 우리 "18 배" 는 **같은 양이 아니다**.
- MPM: E 1.53 · ν 0.49 → E_eff 1.007 GPa → P/E_eff 0.298 → 탄성만이면 φ ≈ 0.956 (기공 ≈ 4–5 %) [카드 산술 · ν 0.49 는 BPM 범위 밖이라 외삽] — 우리 MPM 은 σ_y 0.30 GPa 소성과 함께 순수 SE ≈ 10 % (보정 수렴값) [우리].
- 입자 형상 · 부피 변형 (탄성만 · 실제 강성): φ − φ_c ≈ 0.15 에서 ε_V ≈ (0.28–0.41) × 0.15^{1.5} ≈ **1.6–2.4 %** (ν 0.32–0.4 의 Fig. 12a 안 그림 값 [판독]) · α − α₀ ≈ (0.5–0.65) × 0.15^{2.5} ≈ **0.4–0.6 %** (Fig. 12b 안 그림 [판독 · 눈금]) [카드 산술] — ⇒ **실제 강성의 LPSCl 은 탄성만으로는 300 MPa 에서 거의 변형하지 않는다** → SEM 의 납작해진 SE 는 소성이라는 우리 frame [1] · [2] 의 읽기와 맞는다 [카드 해석 · 단분산 · 등방 한정].

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = 역학 쪽 (입자 형상 · 부피 · 침대 탄성) 의 **탄성 한정판** + DEM 쪽 (P–φ · Z) 의 **입자 해상 대조**.
- 없는 반쪽: 소성 · 파괴 · 응집 · 탈압 · 수송 (σ) · 두 상 (AM + SE) · 다이 · 벽.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 = 무차원 선형 탄성 · 단분산 · 등방 · 3D — **재료 · 하중 경로 · 소성 유무가 다르다**.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ ① **φ_sphere 는 고압에서 1 을 넘는다** — 크기 [판독] (P/E_eff 0.1 에서 Δφ ≈ 0.15 · 0.02 에서 0.02) ② **φ_MC 정의** (점 d/2 구 ∪ 입자 볼록 껍질 · 10⁷ 점 · 넷째 자리) = 몬테카를로 합집합의 꼴 ③ 연산자 선택 이유 (입자가 부피를 보존하나 · 압축되나) 를 결과 전에 적는다 ④ Z 정의 둘 (Z_force / Z_geometry) 이 재밍 근처 · 고압에서 다르다 — CN 정의에 표지 | 실험 · 진밀도 · 질량 기공 없음 |
| **단계 1** (3D 메모리 · 장 수) | 입자 해상의 크기: 점 ~5 × 10⁶ (1024 × ~5000) · 2 × 10⁷ 걸음 · ~40 h × 288 / 480 프로세서 · 다체 ×2 · 회전 ×10 [인쇄] · 수렴 해상도 = 입자 반지름 7.5d (점 ≈ 2 160 [카드 산술]) · [카드 산술] 우리 real_14 의 SE 32 832 개를 7.5d 로 풀면 ≈ 7 × 10⁷ 점 · 10d 면 ≈ 1.7 × 10⁸ | 메모리 숫자 없음 |
| **단계 2** (2D MPM 코드 · 단위 시험) | Cauchy: 쌍 중심력 이산 모형의 ν 는 2D 에서 1/3 로 묶인다 — 2D 이산 대조 모형을 쓸 때 경고 | 2D 코드 · 시험 없음 |
| **단계 3** (2D 접촉 표현 비교) | 같은 φ 지표에서 "점접촉 DEM ↔ 입자 해상" 의 압력 차 ≤ 2 배 (3D · 탄성) · 갈림점 φ − φ_c ≈ 0.1 — 단계 3 결과를 읽을 때의 크기 감각 | 2D · MPM 아님 |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | ★ **탄성만의 기준선**: LPSCl 실제 강성이면 300 MPa 에서 φ_MC ≈ 0.75 [카드 산술] — σ_y 하나를 맞출 때 "탄성만으로 얼마까지" · 랩 표준 (10–13 %) 까지 남는 몫 = 소성 · 재배열 몫 | 실험 기공 아님 · 단분산 · 등방 |
| **단계 5** (3D 복합 압밀) | 없음 (한 상 · 단분산) | AM + SE · 하중 몫 없음 |
| **단계 6** (탈압 · 되돌아옴) | 침대 탄성 K_P ∝ (φ − φ_c)^{1/2} · G_P ∝ (φ − φ_c) · ν_P 1/2 → ~1/4 → 상승 [인쇄 · 판독] — 탈압 강성 · 옆 팽창의 정성 기준 · 실험 (Hentschel & Page) 도 압밀 분말 ν 최소 ~1/4 | 탈압 곡선 · 잔류 · 소성 없음 |
| **단계 7** (형상 · 피복 · 수송) | 입자 형상 지표 (볼록 껍질 ε_V · α · 식 8 · 9) 와 분포 (정규) — 우리 MPM 입자 형상 지표의 정의 후보 · 탄성 크기 (§7-3) | 피복 · 수송 없음 |
| **후보 D0** (지금 DEM) | DEM 의 φ_sphere 결함 · 갈림점 · "2 배" — 우리 DEM 이 φ ≈ 0.87–0.90 (갈림점 위) 에서 돈다는 표지 | 연화 · hooke/hysteresis 아님 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉) | 구 하나를 매끈한 두 벽 사이에서 누르는 시험 (벽–점 조화 · 질량 중심 약한 스프링) = 벽 접촉 단위 시험의 꼴 | 마찰 · 분리 값 없음 |
| **후보 A · A′** (MPM 강체 AM · 입자별 장) | 없음 (MPM 아님) · 같은 φ_MC 에서 접촉 해상 ↔ 점접촉 차의 크기 감각 | — |
| **후보 B** (입자별 FE + 접촉) | ★ **B 의 이산판 (B-BPM)** — 입자를 점 결합망으로 풀어 형상 변화 · 접촉 상호작용을 냄 · 소성은 결합 변형률 이력으로 넣을 자리 (패키지 · ref 64) · 비용 · 수렴 규칙 · 마찰은 요철 · FEM 메시 엉킴 · 파편화 문제를 피함 (p.2) | 소성 미구현 · 마찰 대응 없음 · ν ≲ 0.46 |
| **후보 C** (큰 변형 접촉 DEM · MDR 류) | 점접촉이 깨지는 자리 (φ − φ_c ≈ 0.1 · 단일 입자는 겹침 25 % 까지 Hertz) 와 크기 (2 배) — 대안 접촉 법칙의 시험 영역 · 비국소 DEM (refs 27 · 75) 제안 | 대안 법칙을 시험하지 않음 |
| **후보 C′** (항복 캡 탄소성 접촉 DEM) | 없음 (소성 없음) | — |
| **후보 M0** (균질화 압밀 · 캡 소성 · Heckel) | 침대 탄성률의 φ 의존 꼴 (멱법칙 → 가속) — 균질화 모델의 탄성 부분 | 소성 · 캡 없음 |
| **U0–U6** | ★ **U1** = 구 하나를 두 매끈한 벽 사이 압축 → Hertz (식 6 · E_eff · 10⁻³ E_eff R² 문턱 · 겹침 25 % 까지 · ν −0.1–0.4) — 우리 MPM 입자 하나 압축의 해석해 대조 꼴 · **U5** = 입자끼리 Hertz 쌍 · **U6** = 해상도 수렴 (입자 반지름 2.5 / 5 / 7.5 / 10 d · 덩어리 L⁻² · L⁻³ᐟ² · L⁻¹) · ★ **탄성 한정 벤치마크**: 우리 MPM 을 σ_y → ∞ (탄성만) 로 두고 단분산 구 침대를 등방 주기 압축해 Fig. 6b 의 P/E_eff(φ_MC) 와 견준다 (결과 전 대조 · ν ≤ 0.46) | U0 · U2 · U3 · U4 없음 · 우리 MPM 은 일축이 기본 — 등방 주기 모드 필요 |
| **R1–R7** | **R6** (SE 형상 변형) — 탄성 형상 변화의 크기 (α − α₀ · ε_V) · **R4** (탈압) — 침대 탄성률만 · **R2** (미끄럼 · 분리) — 마찰 = 요철 | R1 (AM 하중 분담) · R3 · R5 · R7 없음 |
| **결과 전 대조 항목** | ① 탄성만 압밀 곡선 Fig. 6b (BPM 매끈 · 거친 · §3-6 표 [판독]) ② φ_sphere − φ_MC (Δφ ≈ 0.15 at P/E_eff 0.1) ③ 갈림점 φ − φ_c ≈ 0.1 · P/E_eff ≈ 10⁻² ④ ν_P 최소 ≈ 0.26–0.30 · 끝 ≈ 0.32–0.39 [판독] — 맞추는 데 쓰지 않음 | 랩 표준 (재료값) 과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: 일반 입상체 (무차원) · 3D · 단분산 (반지름 10d) · 등방 주기 · 선형 탄성 · 마찰 = 요철 · 가압만 (탈압 없음) — 우리 = LPSCl (+ NCM) · 크기 분포 · 일축 다이 300 MPa · 소성 (MPM) / 연화 겹침 (DEM).

## 9. 적용 인사이트 (행동)
1. **단계 0 — 연산자 이유 적기**: "ε_sphere (재료 보존 · 비압축 소성) ↔ ε_union / φ_MC (탄성 압축 · 합집합)" 의 선택 이유를 결과 전 등록 문서에 적고, 이 논문의 Δφ 꼴 (P/E_eff ↑ 면 0 → 0.15) 을 근거로 인용한다.
2. **탄성 한정 벤치마크 (U6 변형)**: MPM 에 등방 주기 압축 모드 + 탄성만 (σ_y → ∞) 으로 단분산 구 침대를 눌러 Fig. 6b 곡선과 견준다 — 해상도 사다리 (입자 지름당 셀 수) 와 함께 · ν 는 0.25 (Cauchy 기준) 와 0.36 (LPSCl) 두 점 · 결과 전 기대값 = §3-6 표.
3. **"탄성만이면 φ ≈ 0.75" 문장**을 단계 4 의 기준선으로 — 소성 σ_y 가 메우는 몫 = 0.75 → 0.87–0.90 (랩 표준) [카드 산술 · 등방 · 단분산 한정].
4. **DEM 갈림점 꼬리표**: 우리 DEM 결과를 인용할 때 "φ − φ_c ≈ 0.25–0.3 = 2 체 접촉 가정이 깨진 영역 · 탄성 BPM 대비 압력 오차 ≲ 2 배는 탄성 한정 (Clemmer 2024)".
5. **입자 형상 지표**: MPM 입자 형상 변화 보고에 볼록 껍질 ε_V · α (식 8 · 9) 와 z-점수 분포를 쓴다 — 탄성 크기 (§7-3 · ≈ 2 % · 0.5 %) 와 소성 크기를 가르는 기준.
6. **흐름 밖 (섬유 DEM)**: `bpm/rotational` 을 쓰는 섬유 DEM (sankar2026) 을 인용할 때 "LAMMPS BPM 패키지 (Clemmer 2024) + 회전 결합 식 (Wang 2009 · 이 논문 ref 51)" 로 나눠 적는다.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Clemmer et al. (*Soft Matter* 20 (2024) 1702–1718) resolved each of 1024 monodisperse, linear-elastic grains with ~5000 bonded point particles and compressed the packing isotropically far beyond jamming; with a consistent Monte Carlo packing fraction, Hertzian DEM differed from the grain-resolved result by at most a factor of two in pressure, whereas the DEM sphere-sum packing fraction exceeded unity at high pressure."
- "In that bonded-particle model, compaction curves for different friction coalesced and departed from the jamming power laws at φ − φ_c ≈ 0.1, which the authors relate to the end of the two-body (independent-contact) assumption; plasticity and fracture were not modelled (Clemmer et al., 2024)."
- 국문 (한정어와 함께): *"입자를 점 결합망 (~5000 점) 으로 푼 선형 탄성 3D 압밀에서 Hertz DEM 의 오차는 같은 φ 지표로 압력 2 배 안이었고, DEM 의 구 부피 합 φ 는 고압에서 1 을 넘었다 (Clemmer 2024) — 단 소성 · 파괴 · 탈압은 없다."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**: §3-10 의 ①–⑥.
**카드가 본 한계**
1. **탄성만** — "18 배 연화의 대안" 으로 쓸 때 소성 몫 (재배열 · 유동 · 파괴) 을 다루지 않는다.
2. **무차원 · 재료 없음** — 절대값 전이 0 · §7-3 의 LPSCl 값은 카드 산술 (등방 · 단분산 · Hertz 류 탄성 한정).
3. **단분산 · 등방 · 주기** — 우리 일축 다이 · 크기 분포 · 두 상과 다르다.
4. **"2 배" 는 φ_MC 로 바꾼 뒤 · 선형 탄성 · ν −0.11–0.4 한정** — 비선형 · 소성이 크면 더 벌어진다고 저자가 적는다 (p.9).
5. **판독 값은 겹친 표지 때문에 거칠다** (경향) — 특히 φ ≲ 0.61 (재밍 근처 묶음) 과 Fig. 12a 안 그림의 φ − φ_c > 0.3.
6. Fig. 14 세로축 단위 · ν 0.03–0.32 의 a_B · 덩어리 보정 시편의 실현 수 [미확인].
7. 갈림점 φ − φ_c ≈ 0.1 은 세 신호 (마찰 무관 · 멱법칙 이탈 · DEM 이탈) 가 겹친 관찰이고 원인 분해는 없다.
8. 마찰 = 요철 · DEM 마찰 대응은 φ_c 맞춤뿐 (*"not unique"*).
9. 탄성률 (Fig. 14) 은 실현 5 개 중 2 개만.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| [29] | B. Harthong, J.-F. Jérier, V. Richefeu, B. Chareyre, P. Dorémus, D. Imbault and F.-V. Donzé, Int. J. Mech. Sci., 2012, 61, 32–43. | ★ MPFEM 탄소성 입자에서 접촉 독립이 φ ≈ 0.7 근처에서 깨짐 (p.14) — 질문 e · k · 정본 `harthong2009_…` 와 다른 논문 · 카드 없음 |
| [19] | Q. Ku, J. Zhao, G. Mollon and S. Zhao, Powder Technol., 2023, 421, 118455. | ★ 응집 소성 입자의 MPFEM 압밀 (p.2 · p.14 — 이 논문이 다루지 않은 소성 · 응집) — 질문 l · 카드 없음 |
| [64] | J. T. Clemmer, K. N. Long and J. A. Brown, Mech. Mater., 2023, 184, 104693. | ★ BPM 결합의 기준 상태 · 변형률 이력 (소성) · 비affine 운동과 비선형 탄성 (p.6 · p.8) — "결합입자 소성" 의 원전 · 카드 없음 |
| [16] | T. L. Vu, S. Nezamabadi and S. Mora, J. Mech. Phys. Solids, 2021, 146, 104201. | 2D MPM 변형 입자 압밀 · E_eff 척도가 ν 차를 설명 (p.11) — 질문 f · g · 카드 없음 (`vu2019_…` 는 PRE 2019 실험) |
| [80] | M. L. Hentschel and N. W. Page, J. Mater. Sci., 2007, 42, 1261–1268. | 압밀 분말 (구리 · 강 · 알루미늄 · 유리) ν 최소 ~1/4 실험 (p.13) — 단계 6 탈압 강성 · 카드 없음 |
| [28] | G. Mollon, Granular Matter, 2022, 24, 1–20. | DEM 에서 입자 형상 변형을 근사하는 방식 (p.2) — 후보 C · 카드 없음 |
| [51] | Y. Wang, Acta Geotechnol., 2009, 4, 117–127. | 회전 결합 BPM (DEM 입자 + 전단 · 토크 결합) 의 식 출처 (p.8) — `bpm/rotational` 인용 정리용 · 카드 없음 |
| [14] · [13] · [27] · [75] · [73] · [33] | Cárdenas-Barrantes 2022 · Cantor 2020 · Gonzalez 2012 · Giannis 2021 · Luding 2008 · Homel 2017 | 정본 카드 있음 (`cardenasbarrantes2022_…` · `cantor2020_…` · `gonzalez2012_…` · `giannis2021_…` · `luding2008_…` · `homel2017_…`) |

## 13. [미확인] 목록 (본문 17 쪽 전수에 없음)
1. 실제 재료 · 단위 (전부 k · d · m 무차원) · 실험 대조.
2. ν 0.03 · 0.11 · 0.17 · 0.32 에 쓴 a_B 값 (카드 역산만).
3. Fig. 14 의 K_P · G_P 정규화 (E_eff 인지 k/d 인지).
4. 덩어리 보정 시편 (L = 50d) 의 실현 수 · K · G 값 자체 (맞춤식만).
5. 탈압 · 되돌아옴 · 이력 (하지 않음).
6. 마찰계수 ↔ 요철 대응 (원문 스스로 모름).
7. Fig. 5d 의 "부피 변형률 ~60 %" 의 정의 (상자 부피 변형률로 읽힘 [카드 해석]).
8. 거친 입자의 ν ≠ 1/4 압밀 (ν 를 바꾼 것은 매끈 입자만).
9. 다체 항이 있는 압밀의 시간 (같은 2 × 10⁷ 걸음 · 480 프로세서 외).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 17 쪽 글자 층 추출 + 그림 · 식 · 근거 문단 렌더로 읽음.  서지 = p.1 (제목 · 저자 3 명 · 소속 · 접수 / 수락 · DOI · 출판일) · p.15 (정정 주석) · p.14 · p.16 (기여 · 감사 · 연구비).  낱말 셈 (대소문자 무시): DEM 69 · BPM 80 · plastic 9 · rotational 8 · 'bpm/rotational' 0 · unload / decompress / springback 0 · ESI 0 · MPM 1 · material point 2.
- 글자 층이 깨뜨린 기호를 렌더로 확인: ν (n) · φ (f) · ≲ · ≳ · < (o) · ~ (B) · 빠진 '−' (a_B = −0.8kd · ν = −0.11 · 기울기 −2 · −3/2 · −1 · 5 × 10⁻⁴ τ⁻¹ · 10⁻⁸ τ⁻¹ · < 10³ 입자).
- 그림 크롭 **46** = 도구 15 (Fig. 1–2 · 4–16) 중 다시 자름 3 (fig_5 · fig_11 · fig_16 — 위쪽 회색 쪽 줄) + 손 크롭 31 (Fig. 3 · 식 10 · 근거 문단 20).  46 장 전부 Read 로 열어 확인 · txt_p10 은 앞 줄 아래쪽이 섞여 한 번 다시 자름 · 두 단에 걸친 문단 8 개는 위아래로 이음.  `figures.json` 의 recrop · manual_crop · viewed_how.
- 판독: digitized.csv 275 행 · 점검 = Fig. 11 안 그림 ν 0.25 의 φ_c 가 인쇄 0.5979 를 재현 · Fig. 6b 판독이 본문의 "2 배 안" 과 맞음 (최대 비 ≈ 1.8).
- `figures/_sources.json`: 도구가 남의 카드 항목 셋 (choi2018 · devasconcelos2019 · heenan2020) 까지 고쳐 되돌렸다 — 이 카드 항목만 더함.
- 2 차 인용 대조: `sankar2026_…` (L45 · L67 · L726) · `zunker2025_…` (L41 · L197 · L645 — 이 논문 인용 아님) — 고치지 않았다 (카드 문제 = 정독 출력 batch_91 의 "카드 문제" 절).
- 정본 litdb 중복 확인: `litdb/papers/` 566 파일 목록 + DOI (D3SM01373A) · 'Clemmer' · 'Lechman' · 'Monti' · 'soft departure' · 'departure from jamming' grep — 카드 없음 (인용만: `sankar2026_…` · `zunker2025_…` 감사절) (2026-11-12).

## 🔗 관련 카드
- 무른 / 변형 입자 압밀 (입자 해상): `cardenasbarrantes2022_soft_spheres_3d_compaction_nscd` (ref 14) · `cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd` · `cardenasbarrantes2021_soft_pentagons_compaction_micromechanics_nscd` · `cantor2020_compaction_model_highly_deformable_particles` (ref 13) · `nguyen2017_mpm_bpm_deformable_particle_compaction` (MPM vs BPM 2D) · `nezamabadi2022_mpm_cd_plastic_particle_compaction` · `vu2019_soft_grain_compression_beyond_jamming_dic` · `bares2021_soft_rigid_mix_experiment_dic_proceedings`.
- 점접촉 DEM 의 한계 · 대안: `gonzalez2012_nonlocal_contact_confined_granular` (ref 27) · `giannis2021_stress_based_multicontact_dem` (ref 75) · `brodu2015_multiple_contact_dem_dense_granular` · `harthong2009_high_density_compaction_dem_voronoi_contact_law` · `zunker2025_dem_large_deformation_compaction` · `luding2008_cohesive_frictional_contact_models` (ref 73).
- 결합구 (BPM) 사용처: `sankar2026_fiber_scale_dem_carbon_felt_manufacturing` (LAMMPS `bpm/rotational` 섬유 · 이 논문을 ref 73 으로 인용) · `tovar2026_cold_spray_cathode_composite_dem_plastic_elastic_bond` (결합 수준 소성 결합구 입자 — 이 논문에 없는 소성 반쪽).
- DEM 구름 · 비틀림 마찰 (DEM 대조 팔의 μ_r · μ_t · §13 의 6 — 쓴 모델의 원전 = ref 73 `luding2008_…` · 윗줄): `ai2011_rolling_resistance_contact_models_dem` · `wensrich2012_rolling_friction_shape_contact_eccentricity_dem` (구름마찰을 모양 대리로 정량 점검) — 이 둘은 이 논문이 인용하지 않음.
- MPM 접촉: `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` (ref 33).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
