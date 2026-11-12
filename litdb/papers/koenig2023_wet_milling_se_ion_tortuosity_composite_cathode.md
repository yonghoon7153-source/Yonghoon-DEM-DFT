<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 1저자 11-12 후보 표 N-13 · 꼭 뽑으라고 한 항목).
     본 = sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps.md (같은 묶음 · 복합 양극 압력 · 기공 · tortuosity 실험 카드의 꼴 · §0-1 고른 의도 대조 · §8 자세한 분석) ·
     곁 = miss2026_pressure_tortuosity_composite_cathode_coating.md (같은 그룹 · τ 규약 대조 절) · minnmann2021_jes_charge_transport_bottlenecks.md (이 논문이 견준 τ² 자료).
     원문 = 출판본 (ACS Appl. Energy Mater. 2023, 6, 9356–9362 · 7 쪽 · "© 2023 The Authors. Published by American Chemical Society") + SI (9 쪽 S-1–S-9 = 그림 S1–S6 · 표 S1–S3 · 식 (S1) · 참고 1–7).
     쪽 표기 = 본문 "p.n" = PDF 쪽 n (인쇄 쪽 = 9355 + n · p.1 = 9356 … p.7 = 9362) · SI "SI p.n" = SI PDF 쪽 n = 인쇄 S-n.  크롭 파일 이름의 pN · figures.json 의 page 는 PDF 쪽이다.
     값 표지: [인쇄] = 본문 · SI · 그림 안 글자로 적힌 값 · [판독] = 래스터 그림을 그 그림의 눈금으로 환산한 값 (재현 = litdb/figures/<slug>/digitized.csv 82 행 · 원본 래스터 = 본문 ≈300 dpi · SI ≈220 dpi) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드에 적힌 값 (slug 병기) ·
     [우리] = 우리 쪽 값 (메인 리포 CLAUDE.md 출처) · [미확인] = 본문 7 쪽 + SI 9 쪽 전수에 없음.
     원문 16 쪽은 글자 층 (PyMuPDF) + 식 · 표 · 그림 쪽 렌더로 전부 읽었다 (식의 분수 · 위첨자 · β 같은 기호는 글자 층에서 흩어져 렌더로 확인).
     DEM · MPM · FEM · 입자 계산 · 압밀 시뮬레이션은 없다 — 실험 (순수 SE 펠릿 EIS · 복합 양극 펠릿 두께 · 대칭셀 EIS · SEM/EDX · XRD) 만. -->
# Li₅.₃PS₄.₃ClBr₀.₇ 유리-세라믹 SE 를 고에너지 건식 밀링 (HDM) 뒤 **저에너지 습식 밀링 (LWM)** 한 번 더 (헵탄 + 다이부틸에터 · ⌀1 mm 볼 · 200 rpm · 2 h) — SE 입경 D50 1.01 → 0.79 µm · D95 3.17 → 1.25 µm · 다결정 NCM85/10/5 (LiNbO₃) 와 70:30 · 80:20 · 85:15 wt% (탄소 · 바인더 없음) 복합 양극을 Li / SE / 복합 / SE / Li 대칭셀 (SOC50 · 전자 차단 Warburg-short) 로 잰 **이온 수송 tortuosity τ_eff = σ₀·ε_SE/σ_eff** (= 우리 tau2 · 수송 tortuosity) 가 ε_SE ≈ 0.235 에서 35.4 → 8.0 · 392 MPa 펠릿 공극 (80:20) 22.7 → 13.5 % — 그러나 **순수 SE 펠릿 σ₂₅°C 도 4.43 → 1.09 mS/cm (×0.25) 로 떨어져** 절대 유효 이온 전도도는 ε_SE ≈ 0.235 에서 거의 같고 (≈0.029 → ≈0.032 mS/cm) ≈0.45 에서는 절반 [카드 산술] — König · Miß · Janin · Roling (ACS Appl. Energy Mater. 2023)

> slug `koenig2023_wet_milling_se_ion_tortuosity_composite_cathode` · DOI `10.1021/acsaem.3c01242` · type `experiment (symmetric cell Li/SE/composite/SE/Li impedance at SOC50 — low-frequency Warburg-short under electron blocking · tau_eff = sigma0*eps_SE/sigma_eff (tortuosity factor) · composite porosity from 392 MPa pellet thickness + estimated densities · SE PSD from SEM · FIB-SEM/EDX · no DEM / MPM / particle model)` · PDF `a54f15d9-13._Mitigating_the_ion_transport_tortuosity_in_composite_cathodes_of_all-solid-state_batteries_by_wet_milling_of_the_solid_electrolyte_particles.pdf` · SI `ff65464d-13._Sup_Mitigating_the_ion_transport_tortuosity_in_composite_cathodes_of_all-solid-state_batteries_by_wet_milling_of_the_solid_electrolyte_particles.pdf` · digested `2026-11-12` · status ✅
>
> **저자**: Christoph König · Vanessa Miß · Laura Janin · **Bernhard Roling\*** — Department of Chemistry, Philipps-Universität Marburg (D-35032 Marburg · SI p.1 = Hans-Meerwein-Straße 4) — \* 교신 (roling@staff.uni-marburg.de · ORCID 0000-0001-7383-1495, p.6) · *ACS Appl. Energy Mater.* **2023**, **6** (18), **9356–9362** (7 쪽 · Article · 호 18 = 매 쪽 바닥 내려받기 경로 `…/6/18/9356/…`) · 접수 2023-05-17 · 승인 2023-08-15 · 출판 2023-09-06 (p.1) · *"© 2023 The Authors. Published by American Chemical Society"* (p.1 바닥 · 라이선스 종류 [미확인]) · 연구비 = DFG (p.6) · 이해 상충 없음 · 핵심어 argyrodites · composite cathode · ion transport · particle size reduction · all-solid-state battery (p.1) · 참고문헌 본문 36 · SI 7.
> **이웃 카드 (링크만)**: 같은 그룹 = [`miss2026_pressure_tortuosity_composite_cathode_coating`](miss2026_pressure_tortuosity_composite_cathode_coating.md) (참고 [12] = 이 논문 · 압밀 중 τ_eon · τ_ion) · [`miss2026_insitu_conductivity_porosity_pressure_compaction`](miss2026_insitu_conductivity_porosity_pressure_compaction.md) (같은 그룹 · 가압 중 두께 · 공극) · [`cronau2022_wet_milling_particle_size_ionic_conductivity`](cronau2022_wet_milling_particle_size_ionic_conductivity.md) (ref 30 · 같은 LWM 계열 · σ 하락) · [`kaiser2018_ion_transport_limitations_assb_sulfide_electrodes`](kaiser2018_ion_transport_limitations_assb_sulfide_electrodes.md) (ref 22 · 같은 대칭셀 꼴) · [`hlushkou2018_void_space_ion_transport_assb_cathode`](hlushkou2018_void_space_ion_transport_assb_cathode.md) (ref 31) · 견준 자료 = [`minnmann2021_jes_charge_transport_bottlenecks`](minnmann2021_jes_charge_transport_bottlenecks.md) (ref 23) · [`park2020_digitaltwin_assb_foundational`](park2020_digitaltwin_assb_foundational.md) (ref 36 · SI 표 S3) · [`shi2019_high_am_loading_particle_size_assb`](shi2019_high_am_loading_particle_size_assb.md) (ref 24) · [`bielefeld2020_effective_ionic_conductivity_binder`](bielefeld2020_effective_ionic_conductivity_binder.md) (ref 26) · [`froboese2019_microstructure_ionic_conductivity_assb_electrode`](froboese2019_microstructure_ionic_conductivity_assb_electrode.md) (ref 17) · LIB 띠 = [`landesfeind2016_tortuosity_eis_electrodes_separators`](landesfeind2016_tortuosity_eis_electrodes_separators.md) (ref 19) · [`thorat2009_quantifying_tortuosity_porous_liion`](thorat2009_quantifying_tortuosity_porous_liion.md) (ref 18) · 전자 σ = [`wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni`](wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni.md) (ref 34) · TLM = [`siroma2015_transmission_line_model_porous_electrode_impedance`](siroma2015_transmission_line_model_porous_electrode_impedance.md) (SI ref 4) · 이 논문을 옮긴 카드 = [`lei2026_se_particle_size_effects_review`](lei2026_se_particle_size_effects_review.md) ([78]) · [`wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode`](wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode.md) ([57]).
> **판독 원자료**: `litdb/figures/koenig2023_wet_milling_se_ion_tortuosity_composite_cathode/digitized.csv` (82 행 — 그림 4 표지 16 + LIB 띠 가장자리 10 · 그림 S2 아레니우스 표지 24 + 카드 맞춤 6 · 그림 S3 누적 수준 16 · 나이퀴스트 마지막 점 · 꼭대기 10) · 그림 크롭 **53 장** (도구 15 중 다시 자름 2 · 손 크롭 38 = 식 10 · 그림 5 패널 8 · 근거 문단 20 (본문 16 + SI 4) · 본 뒤 다시 렌더 2) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 같은 그룹 (Marburg · Roling) 이 고에너지 건식 볼밀로 만든 유리-세라믹 **Li₅.₃PS₄.₃ClBr₀.₇** (HDM) 을 헵탄 + 다이부틸에터 속에서 ⌀1 mm 지르코니아 볼 · 200 rpm · 2 h 로 한 번 더 갈면 (LWM) SE 입경이 **D50 1.01 → 0.79 µm · D95 3.17 → 1.25 µm** (SEM 영상 분포 · SI 그림 S3 [인쇄]) 로 작아지고 좁아지며, 이 SE 를 다결정 **NCM85/10/5** (BASF · 3–6 µm · LiNbO₃ 1 wt%) 와 막자사발에서 **70:30 · 80:20 · 85:15 wt%** (탄소 · 바인더 없음) 로 섞은 복합 양극의 **이온 수송 tortuosity** — 원문 식 (9) **τ_eff = (σ_ion,electrolyte/σ_ion,eff)·ε_SE** = 우리 **tau2 (수송 tortuosity · tortuosity factor · √ 아님)** — 가 HDM **6.3 · ≈21 · 35.4** (ε_SE 0.450 · 0.289 · 0.234) 에서 LWM **3.1 · ≈4.7 · 8.0** (ε_SE 0.459 · 0.324 · 0.237) 로 내려간다 (p.4–5 [인쇄] · 가운데 두 값은 그림 4 [판독]).  σ_ion,eff 는 Li / SE / 복합 / SE / Li 대칭셀을 **SOC50** (전자 σ ≫ 이온 σ 로 가정) 에 두고 낮은 주파수의 Li 농도 기울기 (전자 차단) 가 만드는 **Warburg-short** 를 맞춰 얻은 R_ion 과 따로 누른 펠릿의 두께로 낸다 (식 4 · 5).
**그러나** 원문 본문이 말하지 않은 숫자가 SI 그림 S2 범례에 있다 — 순수 SE 펠릿 σ₂₅°C **HDM 4.43 · LWM 1.09 mS/cm** [인쇄] (392 MPa 90 s 로 만들고 98 MPa 에서 85 → 30 °C 측정 · 25 °C 값은 외삽 — 이 카드의 ln σ – 1/T 맞춤 12 점이 4.43 · 1.09 를 그대로 다시 낸다 [카드 산술]).  τ_eff 는 각자의 펠릿 σ 로 나눈 값이므로 — LWM τ 가 LWM 펠릿 1.09 로 정규화됐다는 것은 원문에 없지만 그림 S6 호 높이로 근사 검사하면 그렇게 맞는다 [카드 산술 · 근사 §3-8] — **절대 유효 이온 전도도 σ_eff = σ₀·ε_SE/τ** 는 ε_SE ≈ 0.235 에서 HDM **≈0.029** ↔ LWM **≈0.032 mS/cm** (+10 %) · ε_SE ≈ 0.45 에서 HDM **≈0.32** ↔ LWM **≈0.16 mS/cm** (−49 %) [카드 산술].  ⇒ ε_SE ≈ 0.235 의 τ 하락 4.4 배 가운데 **약 94 % (로그 기준) 가 기준 펠릿 σ 의 4.1 배 하락**이다 [카드 산술 ln 4.06 / ln 4.42].
공극은 따로 만든 **20 mg 펠릿 (⌀10 mm PEEK 관 · 스테인리스 피스톤 · 392 MPa)** 의 **마이크로미터 캘리퍼 두께**와 **추정 진밀도** (NCM 4.81 g/cm³ = NCM80/15/5 문헌값을 빌림 · SE 2.01 g/cm³ = 음이온 몰부피 규칙의 직선 위 별) 로 낸 값 — 표 1: HDM **11.1 · 22.7 · 21.3 %** · LWM **9.4 · 13.5 · 20.2 %** (70:30 · 80:20 · 85:15) [인쇄 p.3].  lei2026 이 옮긴 "13.5 vs 22.7 %" 는 **80:20 한 쌍**이다.  ⚠ 원문 식 (6) · (8) 은 **공극비 V_void/V_solid** 꼴로 인쇄돼 있고 SI 표 S2 의 "ε_void" 칸 (0.125 · 0.294 · 0.271 · 0.103 · 0.156 · 0.253) 은 그 식 그대로 · 본문 표 1 은 참 기공률 1 − V_solid/(d·A) — 같은 d · V_solid 에서 두 표가 **다른 양**이다 (6 행 모두 재현 [카드 산술] §3-4).
**재료가 우리와 다르다 (Br 치환 유리-세라믹 argyrodite · NCM85 다결정 3–6 µm · 탄소 없음 · SOC50) · 공극은 한 압력 (392 MPa) · 뺀 뒤로 읽히는 캘리퍼 두께 · n = 1 · τ 는 기준 펠릿마다 정규화가 다르다.**

| 1저자가 궁금해한 것 (이 묶음 ★) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ SE 조성 · 습식 밀링 조건 · 입경 전/뒤 | **Li₅.₃PS₄.₃ClBr₀.₇ (LPSClBr₀.₇) 유리-세라믹** · HDM = Pulverisette 7 premium line · 2 g · 20 mL ZrO₂ 단지 · ⌀10 mm 볼 10 개 · **850 rpm · 8.25 h (99 × (5 분 밀링 + 15 분 휴지))** · 막자사발 (p.2) — 따로 열처리 없음 · LWM = HDM 분말 2 g + **헵탄 4.0 mL + 다이부틸에터 0.8 mL** · 20 mL ZrO₂ 단지 · **⌀1 mm 볼 30 g** · **200 rpm · 2 h (30 분 밀링 · 30 분 휴지)** · 비활성 기체 아래 플라스크로 옮겨 진공 건조 · 막자사발 (p.2) · 입경 (SEM 영상 분포 · SI 그림 S3): **D50 1.01 → 0.79 µm · D95 3.17 → 1.25 µm** [인쇄 그림 안] · D10 ≈0.69 → ≈0.51 · D90 ≈2.2 → ≈1.16 · 최소 ≈0.6 → ≈0.39 · 최대 ≈7 → ≈1.9 µm [판독] · XRD 두 분말 같은 반사 (그림 S1 · 정량 없음) | [인쇄] p.2 · SI p.2–3 · [판독] |
| ② ★ 복합 양극 조성 | NCM85/10/5 : LPSClBr₀.₇ = **70:30 · 80:20 · 85:15 wt%** · 막자사발 15 분 · 탄소 · 바인더 없음 (*"We avoid a conductive additive"* p.2) → 부피분율 (표 1): HDM ε_AM / ε_SE = 43.9 / 45.0 · 48.4 / 28.9 · 55.3 / 23.4 % · LWM 44.7 / 45.9 · 54.1 / 32.4 · 56.1 / 23.7 % [인쇄] · 고체 중 SE 몫 50.6 · 37.4 · 29.7 % (두 SE 같음 [카드 산술]) · 20 mg / ⌀10 mm = 25.2–26.4 mg cm⁻² (AM 17.6–22.1) [카드 산술] | [인쇄] p.3 · 표 1 |
| ③ ★ 성형압 · 측정압 · 복합 양극 공극 (13.5 vs 22.7 %) | **공극 펠릿**: 20 mg 혼합물 · ⌀10 mm PEEK 관 · 스테인리스 피스톤 · **392 MPa** (유지 시간 [미확인]) · 두께 = **마이크로미터 캘리퍼 (Mitutoyo)** (p.3) → 하중을 뺀 뒤 두께로 읽힌다 [카드 해석 — 원문은 '뺀 뒤' 를 명시하지 않음] · 공극 = 1 − V_solid/(d·A) (표 1 값이 이것과 6/6 같음 [카드 산술]) · V_solid = m(w_AM/ρ_AM + w_SE/ρ_SE) · **분모 = 추정 진밀도** NCM 4.81 (ref 32 의 NCM80/15/5 값) · SE 2.01 (그림 S4 규칙 · 역산 2.0095–2.0105 [카드 산술]) · **"13.5 vs 22.7 %" = 80:20 · LWM ↔ HDM** · 나머지 쌍 9.4 ↔ 11.1 (70:30) · 20.2 ↔ 21.3 (85:15) · ⚠ SI 표 S2 같은 행 = 0.156 ↔ 0.294 (공극비) · **대칭셀 측정압**: 셀 조립 392 MPa (두 번) · SOC50 충전 98 MPa · 마지막 Li 박 98 MPa · 대칭셀 EIS 때 압력 [미확인] · 순수 SE 펠릿: 제조 392 MPa 90 s · 측정 98 MPa | [인쇄] p.2–4 · 표 1 · SI 표 S2 · [카드 산술] |
| ④ ★ tortuosity 정의 | 식 (9) **τ_eff = (σ_ion,electrolyte/σ_ion,eff)·ε_SE** (p.4) — σ_ion,electrolyte = *"the ionic conductivity of the pure solid electrolyte"* · ε_SE = 복합 양극 전체 부피 (d·A) 기준 SE 부피분율 (표 1) · σ_ion,eff = d_cathode/(R_ion·A) (식 5) ⇒ **τ_eff = 우리 tau2 (수송 tortuosity = tortuosity factor = τ² 꼴 · √ 아님)** · 원문 이름 *"effective ion transport tortuosity τ_eff"* ('factor' 낱말 없음) · 측정 = **Li / SE / 복합 / SE / Li 대칭셀 EIS** (10⁶–10⁻⁴ Hz · 10 mV) — 높은 주파수 = 이온 · 전자 병렬 (식 2) · 중간 = 2R_electrolyte + 계면 반원 (R ∥ CPE · 10⁵–10¹ Hz) · 낮은 주파수 = 전자 차단 Li 농도 기울기 → **Warburg-short** R_ion·tanh((iωτ)^α)/(iωτ)^α (식 4 · 이상적이면 α = 0.5) — 그 앞 조건 = **SOC50 에서 NCM 전자 σ ≥ 이온 σ × 100** (LCO 유추 · 원문 측정 아님 p.4) · SOC0 확인 = SI 그림 S5 (T 형 TLM · σ_eon 1.43 ↔ σ_ion 0.176 mS/cm = 8.1 배) | [인쇄] p.3–4 · SI p.6–7 |
| ⑤ ★ lei2026 의 "ε_SE 0.237 을 tortuosity 처럼" 표기 | **원문에는 그런 표기가 없다** — 원문은 언제나 둘을 따로 적는다: *"τ_eff = 8.0 for ε_SE^LWM = 0.237"* (p.5 두 번) · *"tortuosities as low as 8.0 … at solid electrolyte volume fraction around 0.25"* (p.1) · *"ε_SE^LWM = 0.237 was as low as τ_eff = 8.0"* (p.5 결론) ⇒ 문제는 **리뷰 (Lei 2026) 의 옮김** 쪽 (lei2026 카드 L238 은 리뷰 문장을 옳게 짚었다) | [인쇄] p.1 · p.5 |
| ⑥ ★ 순수 SE 펠릿 σ (기준 상태) | **100 mg** · CompreCell + CompreDrive (rhd) · **392 MPa 90 s 로 펠릿** · 측정 중 **98 MPa** · Autolab PGSTAT302N · 10⁵–10¹ Hz · 10 mV · **85 → 30 °C 5 °C 간격** (p.2–3) → 그림 S2 범례 **σ₂₅°C HDM 4.43 · LWM 1.09 mS/cm** [인쇄] — 25 °C 는 측정 범위 밖 (외삽) · 30 °C 측정 ≈4.90 · ≈1.54 · 85 °C ≈18.1 · ≈16.2 [판독] · 카드 맞춤 E_a ≈0.22 · ≈0.39 eV [카드 산술 · 원문 없음] · **어느 σ 를 식 (9) 에 넣었는지 · 대칭셀 EIS 온도 [미확인]** · 펠릿 두께 · 밀도 · 공극 [미확인] | [인쇄] p.2–3 · SI 그림 S2 · [판독] · [카드 산술] |
| ⑦ 저자 한계 | 명시한 한계는 거의 없다 — SOC50 전자 σ 를 문헌 유추로 가정 (p.4) · Ebner 확산 모사는 *"has to be taken with caution"* (남의 한계) · 계산 미세구조가 τ 를 과소평가 (남의 한계 p.2) · 반복 · 오차 막대 없음 · LWM 펠릿 σ 하락 (×0.25) 은 본문에서 한 번도 말하지 않는다 (§3-10) | [인쇄] p.2 · p.4 |
| ⑧ DEM · 소성 · 2D/3D · 탈압 | DEM · 모델 **없음** (낱말 0 회) · 계산 미세구조에 대한 말 한 문장: *"the results of theoretical studies on computer-generated microstructures appear to underestimate the ion transport tortuosities in real composite electrodes of ASSBs"* (p.2) · 소성 · 입자 변형 설명 없음 (*"poor particle contacts"* · *"gaps between the particles"* p.1) · SEM/EDX 단면은 2D (FIB) · 입도 분포도 2D SEM 영상에서 · 탈압 · 되돌아옴 값 없음 (공극 두께가 뺀 뒤 캘리퍼로 읽힐 뿐) | [인쇄] p.1–2 · §4-4 |
| ⑨ 우리 쪽에 놓을 자리 | τ 규약 번역 §4-2 (τ_eff = tau2 · f = ε/τ · tau = √τ) · SE 입경 효과 ↔ 우리 Cronau(r_SE) (모델 가정 · `SELF-51`) · d_h (채널 폭) · 생산 SE ⌀1.0 µm §7-1 · 복합 공극 ↔ real_14 DEM 15.6 % (300 MPa · 누른 채) §7-1 · 결과 전 대조 항목 §8 | — |

⛔ **한정어 (떼지 말 것)**: ① **SE 가 LPSCl 이 아니다** — Br 치환 Li₅.₃PS₄.₃ClBr₀.₇ 유리-세라믹 (HDM · 열처리 없음) · CAM = 다결정 NCM85/10/5 (3–6 µm · LiNbO₃) · **탄소 없음** · SOC50 ② τ_eff 는 **각 SE 의 순수 펠릿 σ 로 나눈 값** (σ₀ 가 HDM 4.43 · LWM 1.09 로 4 배 다름 — LWM 쪽 σ₀ 선택은 [미확인] · 근사 검사로 1.09) → τ 하락 ≠ 절대 σ_eff 상승 ③ 공극 · 두께 · ε_SE 는 **따로 누른 20 mg 펠릿 (392 MPa 한 번 · 캘리퍼)** 의 값 — 대칭셀 속 양극은 392 MPa 를 두 번 + 98 MPa 단계를 거쳤다 ④ 진밀도 = **추정값** (NCM 4.81 은 다른 조성 문헌값 · SE 2.01 은 음이온 몰부피 규칙) ⑤ 식 (6) · (8) 인쇄 꼴 = 공극비 · 표 1 = 참 기공률 · 표 S2 = 공극비 ⑥ R_ion 은 대부분 호가 실수축에 닿기 전에 끝난 스펙트럼의 Warburg-short **외삽** ⑦ 본문 R_ion · 두께 · ε_SE 와 τ 두 값이 식 (5) · (9) 로 서로 맞지 않는다 (σ₀ 와 무관한 비 검사 8.37 ↔ 5.62 [카드 산술] §3-8) ⑧ 반복 · 오차 없음 (n = 1) · 25 °C σ₀ 는 외삽.
⇒ **절대값 전이: 0 건** (재료 · 상태 · 정규화가 다르다).  전이되는 것은 **꼴과 방향** — ① 같은 질량비에서 SE 를 작고 좁게 하면 392 MPa 펠릿 공극이 준다 (80:20 에서 9.2 %p · 나머지 1–2 %p) ② 각자의 펠릿 σ 로 정규화한 τ 는 ε_SE ≲ 0.3 에서 크게 준다 ③ 그 τ 하락의 대부분이 **기준 σ₀ 하락** 일 수 있다는 **정규화 함정** — 우리 tau2 · f · σ_ion 보고 규칙 (§4-2 · §9) 에 바로 쓸 교훈.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-13 의 '왜' 칸)

의도 원문: *"i (· 흐름 밖 수송 겸) — 복합 양극 공극 'LWM 13.5 vs 22.7 %' (lei2026 표 L267) · SE 습식 분쇄로 복합 양극 이온 tortuosity 를 낮춤 (wolf2026) · 압력 조건은 카드 줄에 없음 · lei2026 L238 = König 가 ε_SE 0.237 을 tortuosity 처럼 적었다는 표기 문제"* (가리킨 카드 = `lei2026_se_particle_size_effects_review` L279 · L267 · L238 · `wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode` L348)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "i" (복합 양극의 압력별 기공) | **일부** | **압력별이 아니라 한 압력 · 조성별**: 392 MPa 로 누른 20 mg 펠릿 (⌀10 mm PEEK · 스테인리스 피스톤) 의 캘리퍼 두께 → 표 1 공극 HDM 11.1 · 22.7 · 21.3 % · LWM 9.4 · 13.5 · 20.2 % (70:30 · 80:20 · 85:15 wt%) [인쇄 p.3] · 상태 = 뺀 뒤로 읽힘 [카드 해석] · 분모 = 추정 진밀도 (NCM 4.81 · SE 2.01) · 상온 · n = 1 · 압력 곡선 · Heckel 없음 |
| "(· 흐름 밖 수송 겸)" | **채움** | τ_eff (= tau2) vs ε_SE 곡선 둘 (HDM · LWM 각 3 점) + 견준 문헌 (Minnmann · Park · LIB 띠) · 그림 4 · §3-7 · 정규화 함정 §3-8 |
| "복합 양극 공극 'LWM 13.5 vs 22.7 %' (lei2026 표 L267)" | **채움 (조건 보탬)** | 표 1 (p.3): **80:20 wt%** 의 LWM 13.5 % ↔ HDM 22.7 % [인쇄] — 392 MPa · 캘리퍼 두께 · 추정 진밀도 · 같은 행의 SI 표 S2 값은 0.156 ↔ 0.294 (식 8 그대로의 공극비 — 같은 양이 아님 §3-4) · 70:30 (9.4 ↔ 11.1) · 85:15 (20.2 ↔ 21.3) 쌍은 차이가 작다 → "13.5 vs 22.7" 은 세 쌍 중 **가장 큰 차이** 한 쌍 |
| "SE 습식 분쇄로 복합 양극 이온 tortuosity 를 낮춤 (wolf2026)" | **채움 (한정어 둘)** | τ_eff HDM 35.4 → LWM 8.0 (ε_SE 0.234 → 0.237) · 6.3 → 3.1 (0.450 → 0.459) [인쇄 p.5] · ⚠ τ 는 각 SE 의 순수 펠릿 σ (4.43 · 1.09 mS/cm) 로 정규화 — 절대 σ_eff 는 0.235 근처 +10 % · 0.45 근처 −49 % [카드 산술 §3-8] · ⚠ 본문 R_ion ↔ τ 비 불일치 (§3-8) |
| "압력 조건은 카드 줄에 없음" | **채움 (원문에 있다)** | 공극 펠릿 **392 MPa** (p.3) · 대칭셀: 분리막 98 MPa → 전지 392 MPa → SOC50 충전 98 MPa → 보호층 98 MPa → SE / 복합 / SE 392 MPa → Li 박 98 MPa (p.3) · 순수 SE 펠릿 392 MPa 90 s · 측정 98 MPa (p.2) · 대칭셀 EIS 때 압력 [미확인] |
| "lei2026 L238 = König 가 ε_SE 0.237 을 tortuosity 처럼 적었다는 표기 문제" | **없음 (원문 쪽)** | König 원문은 τ_eff = 8.0 과 ε_SE^LWM = 0.237 을 언제나 따로 쓴다 (p.1 · p.5 × 2 · 결론 p.5) — 표기 문제는 리뷰가 옮기며 생긴 것 (lei2026 카드 L238 은 그것을 **리뷰의 결함**으로 옳게 적었다 · 의도 문장의 "König 가 … 적었다" 는 주어가 틀렸다) |

**가리킨 카드 · 같은 논문을 옮긴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `lei2026_se_particle_size_effects_review` L267 | ref [78] 서지 *"König, C., Miß, V., Janin, L., et al.: … ACS Appl. Energy Mater. 6, 9356–9362 (2023)"* · 이유 *"LWM 공극 13.5 vs 22.7 %"* | 서지 ✓ (p.1) · 13.5 / 22.7 % = 표 1 의 **80:20** LWM / HDM ✓ — 조성 · 압력 (392 MPa) · 측정 (캘리퍼 + 추정 진밀도) 이 빠짐 | **채움** (조건 한정 없음 — 보고만) |
| `lei2026_se_particle_size_effects_review` L238 | *"König [78] 의 'lower ion transport tortuosity … (ε_SE = 0.237 for LWM)' 는 부피분율을 tortuosity 처럼 적음"* (리뷰의 결함 목록) | 원문은 τ_eff = 8.0 · ε_SE^LWM = 0.237 을 따로 적는다 — 카드 줄은 **리뷰** 문장을 짚은 것이라 옳다 | **채움** (카드 줄 맞음 · 의도 표의 주어가 어긋남) |
| `lei2026_se_particle_size_effects_review` L244 · L279 | König 2023 = "카드 없음 · 다른 카드의 참고문헌 줄에만 (→ wolf2026)" | 이 카드로 해소 | **채움** (이제 카드 있음) |
| `wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode` L348 | ref [57] 서지 *"… ACS Applied Energy Materials 6, no. 18 (2023): 9356–9362"* · 이유 *"카드 없음 — 복합 양극 이온 tortuosity 를 SE 습식 분쇄로 낮춤"* | 서지 ✓ (호 18 = 바닥 경로) · 방향 ✓ — 단 정규화 τ 의 하락이고 절대 σ_eff 는 0.235 근처에서 거의 같다 [카드 산술] | **일부** (방향 맞음 · 정규화 한정어 없음) |
| `miss2026_pressure_tortuosity_composite_cathode_coating` L265 | ref [12] *"(SE 습식 밀링으로 τ_ion 완화)"* · *"같은 그룹 τ_ion 규약 · SE 입경 효과"* | ✓ · 같은 그룹이지만 σ₀ 기준이 다르다 (Miß 2026 = 같은 압력의 순수 펠릿 · König = 392 / 98 MPa 펠릿 한 값 · ε 는 König = 공극 포함 전체 부피 기준 ↔ Miß 2026 = 명목 1 − ε_CAM [다른 카드]) | **채움** |
| `minnmann2021_jes_charge_transport_bottlenecks` (§ 재현표 L270–277) | 원문 (König p.2) *"τ_eff values increasing from 2.4 to 130, when lowering the SE volume fraction from 0.61 to 0.25 … mitigated to 34"* | 카드: τ_ion² 2.40 … 130 (φ_SE 61 … 25 % · 공극 14 % 가정) · fine SE 33.8 = **밀링 전 SE 의 σ₀ 1.6 으로 정규화** (1.2 로 하면 25.4) [다른 카드] — 그림 4 의 Minnmann LWM 점 (33.6 [판독]) 과 König LWM 점은 **정규화 기준이 다르다** (§3-7) | **채움** (값 같음 · 기준 다름은 König 쪽 한계) |
| `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` (§3-5) | 원문 (König p.2) *"a very strong increase of τ_eff from 1.8 to 316, when the SE volume fraction was lowered from 0.63 to 0.3"* | 카드: ε **0.665** 에서 1.8 (TLM) / 1.6 (Li⁺) · ε 0.297 에서 ≈3.3 × 10² (Li⁺) / ≈2.2 × 10³ (TLM) [다른 카드 · 판독] — "0.63" 은 카드의 0.665 와 다르다 | **일부** (König 의 2 차 인용 차 — 보고만) |
| `park2020_digitaltwin_assb_foundational` (§4 · L19 · L196 · L209) | 원문 (König SI p.8) *"no value is available for the ionic conductivity of LPSCl prepared by a heat-treatment procedure by Park et al."* → σ_ion 2.52 mS/cm (결정질 LPSCl · Adeli 2019) 가정 · 그림 4 표지 *"HDM: Park et al."* | 카드: Park SI 표 S1 에 LPSCl σ = −4.45 × 10⁻³·ε_s + 4.64 × 10⁻³ S cm⁻¹ (모사 입력식) · LPSCl = 볼밀 600 rpm 10 h + **550 °C 5 h 어닐** · NCM711 · NBR 2 wt% [다른 카드] — "HDM" 표지는 그 공정과 다르다 · 설계 vol% 합 88.0 / 80.2 / 71.7 % (남는 12.0 / 19.8 / 28.3 %) [다른 카드] | **일부** (König 쪽 표지 · 가정 한계 — 보고만) |

⇒ **의도 대조 결과: 채움 (흐름 밖 수송 · 13.5 vs 22.7 % (80:20 · 392 MPa) · 습식 분쇄 → τ↓ (정규화 한정) · 압력 조건) · 일부 (i = 한 압력뿐 · 압력 곡선 없음) · 없음 (König 원문의 "ε_SE 0.237 을 tortuosity 처럼" 표기 — 리뷰 쪽 문제)**.  2 차 인용은 값이 맞고, "τ 를 낮춤" 에는 **σ₀ 정규화 한정어**가 빠져 있다.

---

## 1. 한 줄 요약
Marburg (Roling) 그룹이 황화물 고체 전지 복합 양극의 느린 이온 수송을 **SE 입자를 한 번 더 습식으로 갈아** (LWM) 줄일 수 있는지 본 짧은 실험 논문이다.
유리-세라믹 Li₅.₃PS₄.₃ClBr₀.₇ 을 HDM 만 한 것과 LWM 을 더 한 것으로 NCM85 다결정과 세 질량비 (70:30 · 80:20 · 85:15) 의 탄소 없는 복합 양극을 만들고, Li / SE / 복합 / SE / Li 대칭셀을 SOC50 에 둔 채 낮은 주파수 Warburg-short 로 이온 저항을 뽑아 **τ_eff = σ₀·ε_SE/σ_eff** 를 냈다.  ε_SE ≈ 0.24 에서 τ 가 35.4 (HDM) → 8.0 (LWM) 로 내려가 *"the lowest value reported so far"* 이고 액체 LIB 와 같은 범위라는 것이 결론이다 — 근거는 SEM 에서 본 **더 작고 좁은 SE 분포 → 더 고른 SE 배치 → 협착 (constrictivity) 감소** 라는 정성 설명.
SI 에만 있는 순수 SE 펠릿 σ (4.43 → 1.09 mS/cm) 를 넣어 보면 절대 유효 전도도는 ε_SE ≈ 0.24 에서 거의 그대로이고 ≈0.45 에서는 오히려 절반이라, "tortuosity 완화" 는 **각자의 펠릿 기준으로 본 상대값**이라는 한정이 붙는다 [카드 산술].

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (AM / SE / 도전재 · 음극) | 연구유형 |
|---|---|---|---|---|
| C. König · V. Miß · L. Janin · B. Roling\* (Philipps-Universität Marburg) | *ACS Appl. Energy Mater.* 6 (18) (2023) 9356–9362 · Article | 10.1021/acsaem.3c01242 | **LiNbO₃ 1 wt% 코팅 다결정 LiNi₀.₈₅Co₀.₁₀Mn₀.₀₅O₂** (NCM85/10/5 · BASF · 3–6 µm) / **Li₅.₃PS₄.₃ClBr₀.₇ 유리-세라믹** (자체 HDM · ± LWM) / **도전재 · 바인더 없음** · 대칭셀 = Li 박 양쪽 (조립 단계에서 In 박 음극) | 실험 — 순수 SE 펠릿 EIS (85–30 °C) · 복합 양극 펠릿 두께 공극 · 대칭셀 EIS (SOC50 · Warburg-short) · SOC0 이온 차단 셀 T 형 TLM · SEM 입도 · FIB-SEM/EDX · XRD |

- **1저자 메모와의 대조**: 저자 넷 · 제목 *"Mitigating the Ion Transport Tortuosity in Composite Cathodes of All-Solid-State Batteries by Wet Milling of the Solid Electrolyte Particles"* · ACS Appl. Energy Mater. 6 (2023) 9356–9362 — PDF 1 쪽 · 쪽 바닥과 **모두 같다**.  덧붙임: 호 **18** (바닥 내려받기 경로) · DOI `10.1021/acsaem.3c01242` · PDF 메타데이터 제목 칸은 `ae3c01242 1..7` (원고 번호).
- 글의 꼴: Introduction → Experimental Section → Theoretical Background → Results and Discussion → Conclusions — 본문 그림 5 · **표 1 · 식 9** · 참고문헌 36 · SI = 그림 S1–S6 · 표 S1–S3 · 식 (S1) · 참고 1–7.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 재료 · 합성 · 입경 (p.2–3 · SI p.2–3 · `txt_p2_hdm_lwm_synthesis.png` · `txt_p3_composite_mixing_cam.png` · `fig_S1.png` · `fig_S3.png`)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| SE (HDM) | **Li₅.₃PS₄.₃ClBr₀.₇ 유리-세라믹 (gc)** · 행성 볼밀 Pulverisette 7 premium line (Fritsch) · 2 g · Li₂S (99.9 % Alfa Aesar) · P₂S₅ (for synthesis · Sigma-Aldrich) · LiCl (≥99.98 %) · LiBr (≥99.9 %) (Sigma-Aldrich) · 20 mL ZrO₂ 단지 · **⌀10 mm ZrO₂ 볼 10 개** · **850 rpm** · **8.25 h** (99 주기 × 5 분 밀링 + 15 분 휴지 — 휴지 포함 33 h [카드 산술]) · 막자사발 → *"yellow-to-beige powder"* · 열처리 없음 (원문에 어닐 단계가 없다) | [인쇄] p.2 |
| SE (LWM) | HDM 분말 **2 g** + **헵탄 4.0 mL + 다이부틸에터 0.8 mL** (부피비 5 : 1 [카드 산술]) · 20 mL ZrO₂ 단지 · **⌀1 mm ZrO₂ 볼 30 g** (볼 : 분말 = 15 : 1 [카드 산술]) · **200 rpm · 2 h (30 분 밀링 · 30 분 휴지)** — 2 h 가 밀링 시간인지 전체 시간인지 [미확인] · 현탁액을 비활성 기체 아래 플라스크로 · 진공 건조 (온도 · 시간 [미확인]) · 막자사발 · 습식이 소형 볼 건식보다 *"higher product yield"* (p.2 · 수율 값 [미확인]) | [인쇄] p.2 |
| XRD | STOE STADI MP · Cu Kα · Debye–Scherrer · 마크 관 (Hilgenberg) 밀봉 · 그림 S1: 두 분말 같은 반사 (≈15.5 · 18 · 25.5 · 30 · 31.3 · 45 · 47.9 · 52.4 · 59.3 °2θ 근처 [판독 · 대략]) — 상 · 결정도 정량 없음 | [인쇄] p.2 · [판독] SI 그림 S1 |
| SE 입도 (SI 그림 S3) | SEM 영상 (그림 5a · 5e) 에서 낸 **누적 분포** — **HDM D50 1.01 · D95 3.17 µm · LWM D50 0.79 · D95 1.25 µm** [인쇄 그림 안] · D10 ≈0.69 / ≈0.51 · D25 ≈0.80 / ≈0.61 · D75 ≈1.63 / ≈0.97 · D90 ≈2.2 / ≈1.16 µm [판독] · 최소 ≈0.6 / ≈0.39 · 최대 ≈7 / ≈1.9 µm [판독] · D95/D50 3.1 / 1.6 · (D90 − D10)/D50 ≈1.5 / ≈0.82 [카드 산술] · 수 기준인지 · 셀 입자 수 · 크기 정의 (등가 원 · Feret) · 2D 영상 [미확인] | [인쇄] SI p.3 · [판독] |
| CAM | **다결정 LiNi₀.₈₅Co₀.₁₀Mn₀.₀₅O₂** (NCM85/10/5 · BASF SE) · *"typical particle size of 3−6 μm"* · **LiNbO₃ 1 wt%** 졸–겔 (refs 29 · 30) | [인쇄] p.3 |
| 복합 양극 | 막자사발 · **15 분** · AM : SE = **70:30 · 80:20 · 85:15 (질량)** · 탄소 · 바인더 없음 (탄소에서의 SE 분해를 피함 · ref 28) | [인쇄] p.2–3 |
| 진밀도 (분모) | NCM **4.81 g/cm³** — *"The density of NCM80/15/5 was assumed to be identical to that of NCM85/10/5 (ρ = 4.81 g/cm³ ³²)"* (ref 32 = LiNi₀.₈CoₓMn₀.₂₋ₓO₂ 논문 → 문장 방향이 뒤바뀐 것으로 읽힌다 [카드 해석]) · SE **≈2.01 g/cm³** = 그림 S4 의 직선 y = 0.648·x 위 별 [판독 ≈(3.10, 2.01)] · 카드 산술: M 297.0 g/mol · V_m(음이온) 95.8 cm³/mol (r(S²⁻) 184 · r(Cl⁻) 181 · r(Br⁻) 196 pm 구 부피 합) → 0.648 × 3.10 = **2.009** · 표 S2 역산 **2.0095–2.0105** (6 행) | [인쇄] p.4 · SI p.3–4 · [카드 산술] |
| 참고 밀도 (SI 표 S1) | Li₆PS₅Cl **1.86** · Li₆PS₅Cl₀.₇₅Br₀.₂₅ 1.92 · Li₆PS₅Cl₀.₅Br₀.₅ 1.96 · Li₆PS₅Cl₀.₂₅Br₀.₇₅ 2.03 · Li₆PS₅Br 2.09 g/cm³ (출처 위첨자: Cl = SI ref 1 Dewald 2019 · 혼합 = ref 2 Kraft 2017 · Br = ref 3 Yu 2019 — 그림 S4 캡션 렌더 확인) · V_m(음이온) 93.5 → 97.54 cm³/mol · ⚠ Li₆PS₅Cl 1.86 = **랩 표준 (1.64 g/cm³) 과 다른 문헌 값** (판정하지 않음) | [인쇄] SI p.4 |

### 3-2. ★ 순수 SE 펠릿 σ — 기준 상태 (p.2–3 · SI 그림 S2 · `txt_p2_p3_se_pellet_conductivity_protocol.png` · `fig_S2.png`)
- **절차 (원문)**: 분말 100 mg → CompreCell (rhd instruments) → CompreDrive 자동 다이 프레스 · **392 MPa 90 s** 로 펠릿 · 측정 중 **98 MPa** · Autolab PGSTAT302N · **10⁵–10¹ Hz** · 10 mV rms · **85 → 30 °C (5 °C 간격)** (p.2–3).  펠릿 지름 · 두께 · 밀도 · 공극 · 전극 [미확인].
- **값**:

| SE | σ₂₅°C (그림 S2 범례) | 30 °C 측정 [판독] | 85 °C 측정 [판독] | 카드 맞춤 ln σ – 1/T (12 점) |
|---|---|---|---|---|
| HDM | **4.43 mS/cm** [인쇄] | ≈4.90 | ≈18.1 | σ₂₅ = 4.43 · σ₃₀ = 5.11 · E_a ≈0.224 eV [카드 산술] |
| LWM | **1.09 mS/cm** [인쇄] | ≈1.54 | ≈16.2 | σ₂₅ = 1.09 · σ₃₀ = 1.40 · E_a ≈0.390 eV [카드 산술] |

- 읽는 법: ① 25 °C 는 측정 범위 (85–30 °C) **밖** — 범례값은 외삽이고 카드 맞춤이 소수 둘째 자리까지 그대로 다시 낸다 [카드 산술] ② HDM/LWM 비는 25 °C 4.06 · 30 °C ≈3.2 · 85 °C ≈1.1 [카드 산술 · 판독] — 높은 온도에서는 거의 같고 낮은 온도로 갈수록 벌어진다 (LWM 의 활성화 에너지가 큼) [카드 해석 — 원문은 이 그림을 본문에서 논하지 않는다] ③ 같은 그룹의 Cronau 2022 (Li₅.₅PS₄.₅Cl₁.₅ 유리-세라믹 · 같은 ⌀1 mm 볼 · 200 rpm LWM) 는 2.5 → 1.73 mS/cm (2 h · ×0.69) · 50 h 0.36 · 저자 해석 = 부분 비정질화 [다른 카드 `cronau2022_wet_milling_particle_size_ionic_conductivity`] — 이 논문의 2 h LWM 은 ×0.25 로 더 크게 떨어졌다 (SE 조성 · 측정 온도 처리 다름) ④ 그 하락은 입경 D50 1.01 → 0.79 µm 와 함께 일어났지만 원문은 원인을 말하지 않는다 — **입경 자체의 효과로 읽을 근거 없음** [카드 해석].

### 3-3. ★ 복합 양극 조성 · 두께 · 공극 (p.3 · 표 1 · SI 표 S2 · `tab_1.png` · `tab_S2.png` · `txt_p3_porosity_pellet_392MPa_caliper.png`)
| SE · AM : SE (wt%) | m (g) [인쇄 S2] | d (µm) [인쇄 S2 · cm 넷째 자리] | V_solid (cm³) [인쇄 S2] | ε_AM / ε_SE / 공극 (%) [인쇄 표 1] | SI 표 S2 "ε_void" [인쇄] | 고체 중 SE 몫 · 적재 [카드 산술] |
|---|---|---|---|---|---|---|
| HDM 70:30 | 0.0206 | 87 | 0.006073 | 43.9 / 45.0 / **11.1** | 0.125 | 50.6 % · 26.2 mg cm⁻² (AM 18.4) |
| HDM 80:20 | 0.0201 | 88 | 0.005343 | 48.4 / 28.9 / **22.7** | 0.294 | 37.4 % · 25.6 (20.5) |
| HDM 85:15 | 0.0204 | 83 | 0.005127 | 55.3 / 23.4 / **21.3** | 0.271 | 29.7 % · 26.0 (22.1) |
| LWM 70:30 | 0.0198 | 82 | 0.005837 | 44.7 / 45.9 / **9.4** | 0.103 | 50.7 % · 25.2 (17.6) |
| LWM 80:20 | 0.0207 | 81 | 0.005503 | 54.1 / 32.4 / **13.5** | 0.156 | 37.5 % · 26.4 (21.1) |
| LWM 85:15 | 0.0202 | 81 | 0.005077 | 56.1 / 23.7 / **20.2** | 0.253 | 29.7 % · 25.7 (21.9) |

- **절차**: 혼합물 20 mg → ⌀10 mm PEEK 관 → 스테인리스 피스톤으로 **392 MPa** → 펠릿 두께를 **마이크로미터 캘리퍼** (Mitutoyo) 로 (p.3).  유지 시간 · 하중을 뺀 뒤인지 · 몰드에서 꺼냈는지 · 반복 수 [미확인] — 캘리퍼라 하중 아래 측정은 아니다 [카드 해석].
- **두께 해상도**: 표 S2 가 두께를 cm 넷째 자리 (1 µm) 까지만 적는다 → 반올림 ±0.5 µm 만으로 공극 ±≈0.5 %p (δε = (1 − ε)·δd/d) [카드 산술] — 70:30 의 HDM ↔ LWM 차 1.7 %p · 85:15 의 1.1 %p 는 이 폭의 두세 배.
- **AM 하중 · 탄소**: 탄소가 없으므로 공극에 탄소가 섞이지 않는다 (XCT 카드들의 '공극 + 탄소' 문제가 없다) · 대신 SE 몫이 같은 질량비에서 HDM ↔ LWM 이 같다 → 공극 차이는 SE 의 입도 · 모양 차이에서 온다 — 단 두 SE 에 **같은 진밀도 2.01** 을 썼으므로 LWM 이 SE 진밀도를 바꿨다면 (비정질화 등) 그 몫도 공극 차에 섞인다 [카드 해석].
- **비단조**: HDM 80:20 공극 (22.7 %) 이 85:15 (21.3 %) 보다 크다 — SE 몫이 더 큰데 공극이 크다 · n = 1 이라 산포인지 가릴 수 없다 [카드 해석].

### 3-4. ★ 공극 식 (6) · (8) ↔ 표 1 ↔ 표 S2 — 같은 측정의 두 양 (p.4 · SI p.5 · `eq_06_thickness_vs_solid_volume_porosity.png` · `eq_08_porosity_as_printed.png` · `txt_si_p5_porosity_eq8.png`)
- 인쇄 식: (6) **d_cathode = (V_solid/A)·(1 + ε_void)** · (7) V_solid = m(w_AM/ρ_AM + w_SE/ρ_SE) · (8) **ε_void = d_cathode·A/V_solid − 1** (p.4) — 이 꼴의 ε_void 는 **공극비 e = V_void/V_solid** 다 (참 기공률이면 d = V_solid/(A(1 − ε)) · ε = 1 − V_solid/(d·A)).
- SI p.5: *"The porosity of the composite electrodes, ε_void, was calculated by using Eq. (8)"* → 표 S2 의 ε_void 칸.
- **재현** [카드 산술 · A = π(0.5 cm)² = 0.78540 cm²]:

| 행 | 1 − V_s/(d·A) | 표 1 공극 | d·A/V_s − 1 | 표 S2 ε_void |
|---|---|---|---|---|
| HDM 70:30 | 11.12 % | 11.1 | 0.1251 | 0.125 |
| HDM 80:20 | 22.69 % | 22.7 | 0.2936 | 0.294 |
| HDM 85:15 | 21.35 % | 21.3 | 0.2715 | 0.271 |
| LWM 70:30 | 9.37 % | 9.4 | 0.1034 | 0.103 |
| LWM 80:20 | 13.50 % | 13.5 | 0.1560 | 0.156 |
| LWM 85:15 | 20.19 % | 20.2 | 0.2530 | 0.253 |

⇒ **표 1 = 참 기공률 (6/6) · 표 S2 = 식 (8) 그대로의 공극비 (6/6)** — 본문 표 1 의 ε_AM + ε_SE + 공극 = 100.0 % (6 행) 이고 ε_SE 도 같은 d·A 를 분모로 다시 나온다 (예: HDM 70:30 ε_SE 45.00 %) [카드 산술].  τ 계산 (식 9) 에 들어간 ε_SE 는 표 1 값 (본문 p.4–5 의 0.450 · 0.289 · 0.234 · 0.459 · 0.237 · 그림 4 x 값 [판독] 과 같음) — **식 (6) · (8) 의 인쇄 꼴은 계산에 쓰인 정의와 다르다** (인쇄 결함 [카드 해석]) · SI 표 S2 를 인용하면 공극을 1.1–1.3 배 크게 옮기게 된다.

### 3-5. 대칭셀 · 측정 사슬 · 압력 이력 (p.3 · 그림 1 · `fig_1.png` · `txt_p3_symmetric_cell_assembly_pressures.png` · `txt_p3_electrochemistry_eis_conditions.png`)
| 단계 | 원문 | 압력 |
|---|---|---|
| 1 분리막 | LPSClBr₀.₇ (HDM) **150 mg** · ⌀10 mm PEEK 관 | 98 MPa |
| 2 전지 | 한쪽에 복합 양극 **20 mg** · 다른 쪽 **In 박 25 mg** (⌀10 mm · 99.99 % Carl Roth) → 통째로 누름 | **392 MPa** |
| 3 SOC50 | 상온 · 0.1 C · 3.9–2.5 V · 한 번 완전 충방전 뒤 **SOC50 까지 충전** (BioLogic SP-150) | 적층 98 MPa |
| 4 보호 · 전자 차단층 | 양극 쪽에 LPSClBr₀.₇ (HDM) **250 mg** (*"for protection against mechanical fracture and as an electron-blocking layer"*) | 98 MPa |
| 5 음극 제거 | In 음극을 긁어냄 → 드러난 분리막 면에 LPSClBr₀.₇ (HDM) **100 mg** → SE / 복합 / SE | **392 MPa** |
| 6 Li 전극 | 양쪽에 Li 박 **10 mg** (⌀10 mm) | 98 MPa |
| 7 EIS | NEISYS (Novocontrol) · 개방 전위 · **10⁶–10⁻⁴ Hz** · 10 mV rms · RelaxIS 맞춤 · 홈메이드 셀 (그림 1) | **[미확인]** · 온도 [미확인] |

- 읽는 법: 양극은 392 MPa 를 **두 번** (2 · 5 단계) 받고 98 MPa 단계를 세 번 거친다 → 식 (5) 의 d_cathode · 식 (9) 의 ε_SE 는 **따로 한 번 누른 공극 펠릿** (§3-3) 의 값이다 (같은 20 mg) — 셀 속 양극의 실제 두께 · 공극과 같다는 근거 [미확인].
- 두 SE 층은 각각 250 mg (150 + 100 · 250) [카드 산술] — 2R_electrolyte 는 높은 주파수 절편으로 빼고 그림을 그렸다 (p.4).

### 3-6. ★ 임피던스 해석 · τ 정의 (p.3–4 · SI p.6–7 · 식 1–5 · 9 · S1 · `eq_01_*` … `eq_09_*` · `eq_S1_t_type_transmission_line.png` · `txt_p4_warburg_fit_electronic_assumption.png` · `fig_2.png` · `fig_S5.png`)
- 식 (1) Z_cell = 2R_electrolyte + Z_interfaces + Z_composite · (2) Z_composite(ω → ∞) = R_ion·R_e−/(R_ion + R_e−) · (3) 중간 주파수 Z_cell = 2R_electrolyte + Z_interfaces (R_e− ≪ R_ion 이고 R_e− ≪ 2R_electrolyte 이면) · (4) 낮은 주파수 **Z_cell = 2R_electrolyte + R_interfaces + R_ion·tanh(iωτ)^α/(iωτ)^α** (인쇄 꼴 그대로 — τ = 정상 농도 기울기 형성 시간 상수 · 이상적이면 α = 0.5) · (5) **σ_ion,eff = (1/R_ion)·(d_cathode/A)** · (9) **τ_eff = (σ_ion,electrolyte/σ_ion,eff)·ε_SE** (p.3–4 [인쇄]).
- 그림 2: 낮은 주파수에서 Li⁺ 가 SE 를 지나 복합 양극에 들어오고 전자는 양극 안에서만 움직여 (전자 차단) Li 농도 기울기 (D_Li⁺ · M_Li⁺ · D_e− · M_e−) 가 생긴다 — 그래서 **확산형 (Warburg-short) 임피던스**.
- 맞춤: 2R_electrolyte (높은 주파수 절편) 를 빼고 10⁵–10¹ Hz 반원 = 계면 (R ∥ CPE) · 낮은 주파수 = Warburg-short (본문 인라인 식은 (iωβ) 로 인쇄 — 식 (4) 의 τ 와 기호가 다름 [인쇄 p.4]) (p.4) · α · τ · 맞춤 오차 [미확인].
- **전제 = 전자 σ ≫ 이온 σ (SOC50)**: *"NCM622, NCM811, and NCM83/11/6 exhibit an electronic conductivity above 1 mS/cm"* (SOC0 · refs 33 · 34) · LCO 는 SOC0 ≈0.01 → SOC50 > 100 mS/cm (ref 35) → *"it is reasonable to assume that the electronic conductivity of NCM at 50% state of charge (SOC50), which is not available in the literature, is at least as high as that of LCO at SOC50"* → *"at least 2 orders of magnitude higher than the ionic conductivity"* (p.4) — **유추 · 측정 아님**.
- **SOC0 확인 (SI 그림 S5)**: HDM 복합 양극 (조성 [미확인]) · 금속 / 복합 / 금속 이온 차단 셀 · **제조 · 적층 392 MPa** · T 형 TLM (식 S1 · Siroma 2015) — Z_ion = R_ion · Z_eon = R_eon^bulk + (R_eon^gb ∥ CPE_eon^gb) · Z_int = CPE_int → **R_ion 66.5 · R_eon^bulk 4.37 · R_eon^gb 3.83 Ω cm² · σ_ion 0.176 · σ_eon 1.43 mS/cm** [인쇄 그림 안] · σ_eon/σ_ion = **8.1** · 함의 두께 ≈117 µm (σ·R 두 경로 같음 — 20 mg 펠릿의 81–88 µm 와 다름 → 질량 다른 시료 [카드 산술 · 카드 해석]).  ⇒ SOC0 에서는 '두 자릿수' 가 아니라 **8 배** — SOC50 의 두 자릿수는 유추에 기댄다.

### 3-7. ★ τ_eff 결과 (p.4–5 · 그림 3 · 4 · S6 · `fig_3.png` · `fig_4.png` · `fig_S6.png` · `txt_p4_p5_results_rion_tau.png` · `txt_p5_sem_interpretation_lowest_tau_lib_comparison.png`)
| SE | AM : SE (wt%) | ε_SE (표 1) | R_ion (Ω cm²) | τ_eff (= 우리 tau2) | tau = √τ · f = ε/τ [카드 산술] |
|---|---|---|---|---|---|
| HDM | 70:30 | 0.450 | **22.6** [인쇄 p.4] | **6.3** [인쇄 p.5] (그림 4 6.27 [판독]) | 2.51 · 0.0714 |
| HDM | 80:20 | 0.289 | [미확인] | ≈21.3 [판독 그림 4] | ≈4.62 · ≈0.0136 |
| HDM | 85:15 | 0.234 | **347** [인쇄 p.5] | **35.4** [인쇄 p.5] (35.5 [판독]) | 5.95 · 0.0066 |
| LWM | 70:30 | 0.459 | [미확인] | **3.1** [인쇄 p.5] (3.04 [판독]) | 1.76 · 0.148 |
| LWM | 80:20 | 0.324 | [미확인] | ≈4.72 [판독 그림 4] | ≈2.17 · ≈0.0686 |
| LWM | 85:15 | 0.237 | [미확인] | **8.0** [인쇄 p.5] (8.03 [판독]) | 2.83 · 0.0296 |

- 스펙트럼 (그림 3 · S6): ε_SE 가 작은 시료의 낮은 주파수 호는 **실수축에 닿기 전에 끝난다** — HDM 0.289 마지막 점 Z′ ≈190 · −Z″ ≈36 · 0.234 ≈311 · ≈84 · LWM 0.324 ≈107 · ≈14 · 0.237 ≈225 · ≈76 · 0.459 (삽입 그림) ≈44.5 · ≈8 Ω cm² [판독] (10⁻⁴ Hz 까지 쟀는데) → R_ion 은 Warburg-short 맞춤의 **외삽**.  HDM 0.450 만 거의 닫힌다 (삽입 그림 · 끝 ≈26.5 = 계면 ≈3.8 + R_ion 22.6 [판독 · 카드 산술]).  호 꼭대기 / R_ion = 7.5 / 22.6 ≈0.33 · 111.6 / 347 ≈0.32 [판독 · 카드 산술] — 이상 Warburg-short (α = 0.5) 는 0.417 · α 0.45 → 0.358 · α 0.40 → 0.305 [카드 산술 · 수치 계산] ⇒ 관측 비는 **α ≈0.41** 의 납작한 호에 해당 (원문 α 값 [미확인]).
- 그림 4 (log y · x = ε_SE 또는 ε_LE %): 이 연구 HDM (빈 원) · LWM (찬 원) · **Minnmann 2021 HDM** (빈 네모) 25.0 % 131 · 33.0 % 15.3 · 44.0 % 4.33 · 53.2 % 3.13 · 61.1 % 2.32 · 100 % 1.00 · **Minnmann LWM** (찬 네모) 25.0 % 33.6 · **Park 2020 'HDM'** (세모 · SI 표 S3) 21.9 % 17.6 · 34.9 % 9.79 · 47.9 % 3.53 [판독] · **LIB 띠** (refs 19 · 20 보간) ε 26.8–52.4 % · τ ≈3.0–6.9 (ε 30 % 에서 4.85–6.18) [판독] · 점선 = *"guides for the eye"* (맞춤 아님).
- 원문 결론 문장: *"to our knowledge, an ion transport tortuosity value of τ_eff = 8.0 for ε_SE^LWM = 0.237 is the lowest value reported so far for a composite electrode with such a low SE volume fraction"* · LWM 값은 *"in the same range as tortuosity data obtained for composite electrodes of laboratory-scale LIBs"* (p.5).
- ⚠ **정규화가 섞인 그림**: Minnmann 의 LWM 점 (33.6) 은 **밀링 전 SE σ₀ (1.6)** 로 나눈 값이고 [다른 카드 `minnmann2021_jes_charge_transport_bottlenecks` — 1.2 로 하면 25.4] · Park 점은 **가정한 결정질 LPSCl σ₀ 2.52** (SI p.8) · 이 연구 LWM 점은 (근사 검사상) **LWM 자신의 σ₀ 1.09** — 같은 축에 기준이 다른 세 τ 가 있다 [카드 해석 · §3-8].
- SI 표 S3 (Park 2020 환산): 60:38:2 → vol 35.1 : 47.7 : 5.2 · σ_eff 0.339 mS/cm (log −3.47) · τ 3.5 / 70:28:2 → 40.4 : 34.7 : 5.1 · 0.089 (−4.05) · 9.8 / 80:18:2 → 45.0 : 21.7 : 5.0 · 0.031 (−4.51) · 17.6 [인쇄] — 2.52·φ/σ 로 3.55 · 9.83 · 17.64 재현 [카드 산술].

### 3-8. ★★ τ 정규화가 숨긴 것 — 절대 σ_eff · 기준 σ₀ · 본문 수의 자기 일관 [카드 산술]
**(a) 절대 유효 이온 전도도** σ_eff = σ₀·ε_SE/τ (식 9 를 뒤집음 · σ₀ = 그림 S2 의 σ₂₅°C):

| ε_SE (HDM ↔ LWM) | HDM σ_eff (σ₀ 4.43) | LWM σ_eff (σ₀ 1.09) | LWM / HDM | τ 비 HDM / LWM | ln(σ₀ 비) / ln(τ 비) |
|---|---|---|---|---|---|
| 0.234 ↔ 0.237 | **0.0293 mS/cm** (본문 R · d 로는 0.0239) | **0.0323** | **1.10** (R 경로 1.35) | 4.42 | **0.94** |
| 0.289 ↔ 0.324 | 0.0601 (τ 판독) | 0.0748 (τ 판독) | 1.25 (ε 다름) | 4.51 | 0.93 |
| 0.450 ↔ 0.459 | **0.316** (R 경로 0.385) | **0.161** | **0.51** (R 경로 0.42) | 2.03 | 1.98 |

⇒ ε_SE ≈ 0.235 에서 τ 가 4.4 배 준 것 가운데 **로그로 약 94 % 가 σ₀ 의 4.1 배 하락**이고 절대 σ_eff 는 +10 % (R 경로 +35 %) · ε_SE ≈ 0.45 에서는 LWM 복합 양극의 절대 σ_eff 가 **절반**이다.  같은 HDM 펠릿 σ₀ (4.43) 로 LWM 을 정규화하면 τ_LWM = 12.6 · ≈19.2 · 32.5 (0.459 · 0.324 · 0.237) — 0.237 의 32.5 는 HDM 0.234 의 35.4 · Minnmann LWM 33.6 과 거의 같다 [카드 산술 · σ₀ 가정].
**(b) LWM τ 의 σ₀ 는 어느 것인가** (원문 [미확인] · 근사 검사): HDM 의 호 꼭대기 / R_ion ≈0.32–0.33 을 LWM 호에 그대로 쓰면 R_ion ≈35 · ≈100 · ≈280 Ω cm² (0.459 · 0.324 · 0.237 · 꼭대기 ≈11.3 · ≈32.5 · ≈91 [판독]) → τ(σ₀ 1.09) ≈2.1 · ≈4.4 · ≈8.9 ↔ τ(σ₀ 4.43) ≈8.6 · ≈17.7 · ≈36 — 원문 3.1 · ≈4.7 · 8.0 은 **σ₀ = 1.09 (LWM 자기 펠릿)** 쪽과 맞는다 [카드 산술 · 근사 — 호 모양이 같다는 가정].
**(c) 본문 R_ion · 두께 · ε_SE ↔ τ 의 자기 일관**: 식 (5) · (9) 로 τ₂/τ₁ = (R₂/R₁)(d₁/d₂)(ε₂/ε₁) — **σ₀ 와 단위에 무관** — = (347/22.6)(87/83)(0.234/0.450) = **8.37** 인데 인쇄 τ 비 = 35.4/6.3 = **5.62**.  σ₀ = 4.43 이면 R · d 로 τ = 5.18 · 43.3 (인쇄 6.3 · 35.4) · 인쇄 τ 를 맞추려면 σ₀ 5.39 · 3.62 가 필요 (두 값의 기하평균 4.42) [카드 산술].  원인 (R · τ 의 인쇄 · 두께 · 온도 · σ₀) [미확인] — **본문 숫자 넷 가운데 적어도 하나는 다른 조건의 값**이다.

### 3-9. SEM/EDX (p.5 · 그림 5 · `fig_5.png` · `fig_5a.png` … `fig_5h.png`)
- 5a · 5e: 순수 SE 분말 (5 µm 막대) — HDM 은 큰 각진 덩어리 (수 µm) + 작은 알갱이 · LWM 은 ≈1 µm 이하 알갱이의 응집체 [카드 판독 · 정성].
- 5b–d: HDM 복합 양극 (ε_SE^HDM 0.289 = 80:20) FIB 단면 (2 µm 막대) + S (SE) · Ni (NCM) EDX · 5f–h: LWM (ε_SE^LWM 0.324 = 80:20) — 원문: *"the narrower size distribution of the SE particles leads to a more homogeneous spatial distribution of these particles inside the composite electrode, which should result in fewer constrictivities for the ion transport"* (p.5) — **정성 · 정량 지표 없음** (EDX 면적분율 · 분포 지표 [미확인]).  두 단면 모두 FIB 커튼 줄무늬 · NCM 2 차 입자 단면 ≈2–4 µm [카드 판독 · 대략].

### 3-10. ★ 저자가 적은 한계 · 원문 안 어긋남
**원문이 스스로 적은 것**
1. SOC50 의 NCM 전자 σ 는 *"not available in the literature"* → LCO 유추로 *"we can safely assume"* (p.4).
2. 남의 결과에 대한 한계: Ebner 확산 모사 *"has to be taken with caution since … diffusion simulations can underestimate ion transport tortuosity as compared to values obtained from impedance spectroscopy"* · 계산 미세구조 (Bielefeld · Yamakawa) *"appear to underestimate the ion transport tortuosities in real composite electrodes"* (p.2).

**카드가 본 어긋남 (원문 문장 · 그림 · 표끼리)**
3. **식 (6) · (8) ↔ 표 1 ↔ 표 S2** (§3-4) — 인쇄 식 = 공극비 · 표 1 = 참 기공률 · 표 S2 = 공극비 (6/6) [카드 산술].
4. **R_ion ↔ τ 비** (§3-8c) — 8.37 ↔ 5.62 [카드 산술].
5. **순수 SE σ 하락 (×0.25) 을 본문이 말하지 않는다** — SI 그림 S2 범례에만 있고 τ 해석에 쓰지 않았다 · LWM 에 어느 σ₀ 를 넣었는지도 없다 (§3-8b).
6. *"The same spectral shape … was obtained for electrodes with SE particles prepared by LWM (see Figure S4)"* (p.5) — LWM 스펙트럼은 **그림 S6** (S4 = 밀도 그림).
7. *"The density of NCM80/15/5 was assumed to be identical to that of NCM85/10/5 (ρ = 4.81 g/cm³ ³²)"* (p.4) — 쓴 CAM 은 NCM85/10/5 · ref 32 는 LiNi₀.₈CoₓMn₀.₂₋ₓO₂ → 문장 방향이 바뀜 [카드 해석].
8. Warburg-short 인라인 식은 **(iωβ)** · 식 (4) 는 **(iωτ)** (p.4) — 같은 시간 상수의 두 기호.
9. 그림 4 범례 *"HDM: Park et al."* — Park 2020 LPSCl 은 볼밀 + 550 °C 어닐 [다른 카드 `park2020_digitaltwin_assb_foundational`] · SI p.8 *"no value is available for the ionic conductivity of LPSCl … by Park et al."* ↔ Park SI 표 S1 의 σ 식 (모사 입력) [다른 카드].
10. Kaiser 2018 인용 *"from 0.63 to 0.3"* ↔ 정본 카드 ε 0.665 · 0.297 [다른 카드 `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes`].
11. LWM 2 h *"(30 min milling; 30 min rest)"* — 2 h 가 밀링 시간인지 전체 시간인지 문장만으로 가릴 수 없다 (HDM 쪽 *"8.25 h (99 cycles; 5 min milling; 15 min rest)"* 는 밀링 시간 = 8.25 h 로 맞음 [카드 산술]).
12. 그림 S5 시료 조성 · 두께 미기재 (함의 두께 ≈117 µm ≠ 20 mg 펠릿 81–88 µm) [카드 산술].

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 사슬
원료 → HDM (850 rpm · 8.25 h) → [± LWM 헵탄 / DBE · ⌀1 mm · 200 rpm · 2 h · 건조] → ① 순수 SE 펠릿 (392 MPa 90 s · 98 MPa · 85→30 °C EIS → σ₂₅ 외삽) ② SEM 분말 영상 → 입도 누적 분포 ③ XRD → NCM85 (LiNbO₃) 와 막자사발 15 분 (70:30 · 80:20 · 85:15) → ④ 20 mg 펠릿 392 MPa → 캘리퍼 두께 → 공극 · ε_AM · ε_SE (추정 진밀도) ⑤ 대칭셀 조립 (98 → 392 → SOC50 → 98 → 392 → 98 MPa) → EIS 10⁶–10⁻⁴ Hz → Warburg-short R_ion → σ_eff (④ 의 두께) → τ_eff (① 의 σ₀ · ④ 의 ε_SE) ⑥ FIB-SEM/EDX 단면 (80:20) ⑦ SOC0 이온 차단 셀 T 형 TLM (전자 ≫ 이온 확인).
- 안 한 것: 압력 곡선 · 하중 아래 두께 · 탈압 · 반복 · 오차 · 펠릿 밀도 · 분할 영상 기공 · 전자 σ (SOC50) 측정 · 율속 · 충방전 성능 비교 · 절대 σ_eff 보고 · LWM 의 σ 하락 원인 분석.

### 4-2. ★ τ 정의 ↔ 우리 τ 명명 규약 (메인 리포 CLAUDE.md ★★ τ 블록 · `comparison_vs_ours_DEM.md` J 절)
| 원문 이름 · 식 | 원문 값 | 우리 키 · 이름 | 같은가 |
|---|---|---|---|
| *"effective ion transport tortuosity τ_eff"* = (σ_ion,electrolyte/σ_ion,eff)·ε_SE (식 9) | 3.1 … 35.4 | **`tau2_ion_<mode>` = 수송 tortuosity (tortuosity factor · φ·σ₀/σ_eff)** | **같은 꼴** — 원문 τ_eff 는 τ² 자리 (√ 아님 · 'factor' 낱말 없음 = Thorat 꼴) |
| σ_ion,eff/σ_ion,electrolyte = ε_SE/τ_eff | 0.0066 … 0.148 [카드 산술] | `f_ion_<mode>` | 같음 |
| √τ_eff | 1.76 … 5.95 [카드 산술] | `tau_ion_<mode>` (웹앱 τ_Lap,eff) | 원문에 없음 |
| ε_SE = SE 부피 / (d·A) (공극 포함 전체) | 0.234 … 0.459 | φ_SE (SE 구 부피 합 / 전극 부피 · 공극 포함 상자) | 같은 분모 (공극 포함) |
| σ_ion,electrolyte = 순수 SE 펠릿 (392 MPa 90 s · 98 MPa · 25 °C 외삽) — **SE 마다 자기 펠릿** | 4.43 (HDM) · 1.09 (LWM) | σ₀ = 솔버 σ_grain 3.0 (펠릿값 · `CL-91`) · 보고 기준 1.5 mS/cm (1저자 10-12) — **한 값으로 고정** | **기준 상태가 다르다** |
| 기하 경로 τ | 없음 | `tau_geo_SE_dij` (배포 키 `tortuosity_SE_wall`) | — |

- 환산 규칙 (식만): tau2_우리꼴 = τ_eff × (σ₀_우리 / σ_펠릿) × (φ_우리 / ε_SE).  우리 tau2 는 솔버 σ₀ 가 약분되는 **기하 · 접촉망** 양이라 — König 의 '자기 펠릿' τ 와 같은 뜻은 **펠릿 σ 가 복합체 속 SE 의 고유 σ 변화를 똑같이 품을 때만** 이다 (펠릿에는 자기 입계 · 기공이 들어 있다 — 우리 σ_grain 3.0 이 펠릿값이라는 `CL-91` 과 같은 문제).
- litdb J 절 "기준 상태 장부" 에 한 줄: **SE 마다 자기 펠릿 ≡ 1 (392 MPa 제조 · 98 MPa 측정 · 25 °C 외삽)** — Minnmann (밀링 전 SE 펠릿 ≡ 1 · 같은 그림의 LWM 점 포함) · Miß 2026 (같은 압력 펠릿 ≡ 1) · Kaiser (고정 펠릿) 와 다르다.

### 4-3. ★ 입자 처리 (실험 — 시뮬레이션 없음)
- 실제 분말.  SE = HDM 유리-세라믹 (각진 큰 덩어리 + 작은 알갱이 · D95 3.17 µm · 최대 ≈7 µm ≈ NCM 크기) ↔ LWM (≈1 µm 이하 알갱이 응집 · D95 1.25 µm) · NCM = 다결정 2 차 입자 3–6 µm.  변형 · 소성 · 하중 분담 값은 없다 — 원문 설명은 **크기 분포 → 공간 분포 → 협착 (constrictivity)** 의 기하 · 위상 설명뿐.
- 우리 대응 (CLAUDE.md): DEM = 단단한 구 · hooke/hysteresis · SE 영률 18 배 연화 (1.35 GPa) · 생산 SE **⌀1.0 µm 단분산** (r 0.5 µm) — 이 논문의 **LWM 분포 (D50 0.79 · D95 1.25 µm) 가 우리 단분산 SE 에 더 가깝고** HDM 의 굵은 꼬리 (NCM 크기 SE) 는 우리 침대에 없다 [카드 해석].  MPM = AM 얼린 장애물 + SE J2 (E 1.53 · σ_y 0.30 · ν 0.49) — 입도 분포 폭을 다루지 않는다.

### 4-4. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **말 없음** (DEM · discrete element · particle simulation 낱말 0 회).  가장 가까운 문장 = 계산 미세구조 일반: *"Much lower τ_eff values were obtained by Bielefeld et al. for computed ASSB cathode microstructures. They reported a tortuosity value of 5.0 for an SE volume fraction of 0.3 … Yamakawa et al. … τ_eff value of 11 for an SE volume fraction of 0.25. Thus, the results of theoretical studies on computer-generated microstructures appear to underestimate the ion transport tortuosities in real composite electrodes of ASSBs."* (p.2) — Bielefeld 2020 = GeoDict 확률 배치 복셀 (DEM 아님 [다른 카드 `bielefeld2020_effective_ionic_conductivity_binder`]) · Yamakawa 2020 = 위상장 + 회귀 (카드 없음).  LIB 쪽: *"diffusion simulations can underestimate ion transport tortuosity as compared to values obtained from impedance spectroscopy"* (p.2 · ref 20).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — 계산이 없어 말도 없다.  재료 쪽 진술만: *"an inhomogeneous distribution of CAM and SE particles in the composite cathode as well as gaps between the particles can lead to bottlenecks or constrictivities for the ion transport"* (p.1) · *"poor particle contacts"* (p.1 초록).  ⇒ 맞춘 값 0 개 · 계산 비용 0.
3. **2D / 3D** — 측정은 3D 덩어리 (EIS · 두께) · 미세구조 근거는 **2D** (FIB-SEM/EDX 단면 · SEM 분말 영상에서 낸 입도 분포) · 2D → 3D 전이 말 없음 · 2D 영상 입도는 3D 부피 분포가 아니다 [카드 해석].
4. **압력을 뺄 때의 거동** — 없음.  공극 두께가 캘리퍼 (하중을 뺀 뒤로 읽힘) 일 뿐 되돌아옴을 따로 재지 않았다 · 대칭셀은 98 ↔ 392 MPa 를 오갔지만 그 사이 두께 · 공극 측정 없음.

### 4-5. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| HDM | high-energy dry milling — 850 rpm · ⌀10 mm 볼 · 8.25 h 합성 밀링 (유리-세라믹 생성) |
| LWM | low-energy wet milling — 헵탄 + 다이부틸에터 · ⌀1 mm 볼 · 200 rpm · 2 h 입경 줄이기 |
| 대칭셀 (Li / SE / 복합 / SE / Li) | 양쪽 Li 금속 · 두꺼운 SE 층 사이에 복합 양극 — 낮은 주파수에서 Li⁺ 가 양극을 지나고 전자는 막힘 |
| Warburg-short | 유한 길이 확산 임피던스 R·tanh(√(iωτ))/√(iωτ) (여기서는 지수 α 일반화) — 낮은 주파수 극한 = R_ion |
| SOC50 | 충전 상태 50 % — NCM 전자 σ 가 이온 σ 보다 훨씬 커지도록 둔 상태 (가정) |
| T 형 TLM | 이온 · 전자 두 레일 + 계면 가지 전송선 모델 (Siroma 2015) — SOC0 이온 차단 셀의 맞춤 (식 S1) |
| constrictivity | 단면이 좁아지는 협착 — 원문은 SE 분포가 고르면 줄어든다고 정성 서술 |
| 유리-세라믹 (gc) | 밀링으로 만든 비정질 + 결정 혼합 SE (열처리 없음) |

---

## 5. Figure set ★
| 그림 (크롭 파일) | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| Fig. 1 (`fig_1.png`) | 홈메이드 대칭셀 — 스테인리스 피스톤 · PEEK 관 · Li / LPSClBr₀.₇ / 복합 / LPSClBr₀.₇ / Li | 측정 꼴 (흐름 밖 수송) |
| Fig. 2 (`fig_2.png`) | 낮은 주파수 Li 농도 기울기 · 전자 차단 모식 (D_Li⁺ · M_Li⁺ · D_e− · M_e−) | Warburg-short 해석 근거 |
| Fig. 3 (`fig_3.png`) | HDM 세 ε_SE 의 나이퀴스트 (2R_electrolyte 뺌 · 삽입 = 0.450) | ★ 호가 실수축에 닿지 않는 외삽 (§3-7) [판독] |
| Fig. 4 (`fig_4.png`) | τ_eff vs ε_SE (log) — 이 연구 HDM · LWM · Minnmann · Park · LIB 띠 | ★★ tau2 vs φ_SE 의 실험 곡선 (결과 전 대조 · 정규화 한정) [판독] |
| Fig. 5 (`fig_5.png` · `fig_5a.png` … `fig_5h.png`) | (a) HDM 분말 (b–d) HDM 80:20 단면 + S · Ni (e) LWM 분말 (f–h) LWM 80:20 단면 + S · Ni | SE 공간 분포 정성 근거 (2D) |
| Table 1 (`tab_1.png`) | ε_AM · ε_SE · 공극 (6 시료) | ★ 공극 (참 기공률) · ε_SE |
| SI Fig. S1 (`fig_S1.png`) | XRD HDM · LWM | 상 변화 정성 (정량 없음) |
| SI Fig. S2 (`fig_S2.png`) | 순수 SE 아레니우스 · σ₂₅°C 4.43 · 1.09 | ★★ 기준 σ₀ · 정규화 함정의 근거 [판독] |
| SI Fig. S3 (`fig_S3.png`) | 입도 누적 분포 · D50 · D95 | ★ SE 입도 (우리 SE ⌀1.0 µm 와 견줌) [판독] |
| SI Fig. S4 · Table S1 (`fig_S4.png` · `tab_S1.png`) | 음이온 몰부피 규칙 ρ = 0.648·M/V_m · 아지로다이트 다섯 밀도 | 진밀도 추정의 근거 · LPSCl 1.86 (랩 표준과 다른 문헌 값) |
| SI Table S2 (`tab_S2.png`) | m · d · V_solid · ε_void (공극비) | ★ 공극 재현 · 두 정의 (§3-4) |
| SI Fig. S5 (`fig_S5.png`) | SOC0 이온 차단 셀 스펙트럼 + T 형 TLM · R · σ 인쇄 | 전자 ≫ 이온 가정의 SOC0 확인 (8.1 배) |
| SI Fig. S6 (`fig_S6.png`) | LWM 세 ε_SE 나이퀴스트 | ★ LWM σ₀ 근사 검사 (§3-8b) [판독] |
| SI Table S3 (`tab_S3.png`) | Park 2020 τ 환산 (σ 2.52 가정) | 비교 자료의 기준 |
| 식 10 장 (`eq_01_cell_impedance_sum` · `eq_02_composite_high_frequency_parallel` · `eq_03_cell_impedance_intermediate` · `eq_04_warburg_short_low_frequency` · `eq_05_effective_ionic_conductivity` · `eq_06_thickness_vs_solid_volume_porosity` · `eq_07_solid_volume_from_mass` · `eq_08_porosity_as_printed` · `eq_09_effective_tortuosity_definition` · `eq_S1_t_type_transmission_line`) | 원문 식 (1)–(9) · (S1) 인쇄 그대로 | 보고서 식 절 붙임 (식 6 · 8 은 '인쇄 꼴 = 공극비' 표지와 함께) |
| 근거 문단 20 장 (`txt_p1_abstract` · `txt_p1_tau_definition_target` · `txt_p1_p2_lib_tortuosity_literature` · `txt_p2_assb_literature_models_underestimate` · `txt_p2_study_design_soc50_no_carbon` · `txt_p2_hdm_lwm_synthesis` · `txt_p2_p3_se_pellet_conductivity_protocol` · `txt_p3_composite_mixing_cam` · `txt_p3_porosity_pellet_392MPa_caliper` · `txt_p3_symmetric_cell_assembly_pressures` · `txt_p3_electrochemistry_eis_conditions` · `txt_p4_density_assumptions` · `txt_p4_warburg_fit_electronic_assumption` · `txt_p4_p5_results_rion_tau` · `txt_p5_sem_interpretation_lowest_tau_lib_comparison` · `txt_p5_p6_conclusions` · `txt_si_p3_p4_density_estimation` · `txt_si_p5_porosity_eq8` · `txt_si_p6_p7_tlm_soc0_model` · `txt_si_p8_park_tau_sigma_2p52`) | 인용 문장 전부 | 보고서 붙임 |

## 6. Post-processing ★
- **원문**: RelaxIS 등가회로 맞춤 (계면 R ∥ CPE + Warburg-short) · SOC0 T 형 TLM 맞춤 · SEM 영상 입도 누적 분포 · 밀도 규칙 직선 맞춤 (y = 0.648·x) · 식 (5)–(9) 계산 · 그림 4 점선 = 눈 맞춤.
- **이 카드**: 원본 래스터 (본문 ≈300 dpi · SI ≈220 dpi) 에서 눈금 · 표지 중심 (그림 4 · S2) · 누적 곡선 첫 화소 줄 (S3) · 호 마지막 점 · 꼭대기 (그림 3 · S6) — 전부 `digitized.csv` method 열에 방법.  카드 산술 = 표 1 ↔ 표 S2 재현 · ρ_SE 역산 · 적재 · σ_eff 두 경로 · τ 비 검사 · σ₀ 근사 검사 · 아레니우스 맞춤 · Park 재현 · 함의 두께.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (우리 수치는 메인 리포 CLAUDE.md 출처를 그 자리에 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 상태 · 정규화가 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| 재료 | NCM85/10/5 (LiNbO₃ · 3–6 µm) + **Li₅.₃PS₄.₃ClBr₀.₇ 유리-세라믹** · 탄소 없음 | NCM811 (P:S 이봉) + **Li₆PS₅Cl** [우리] | 다른 SE (Br 치환 · 유리-세라믹) · 다른 AM |
| SE 입도 | HDM D50 1.01 · D95 3.17 · LWM D50 0.79 · D95 1.25 µm (2D SEM) | 생산 SE ⌀1.0 µm (r 0.5) **단분산** [우리 CLAUDE.md] | D50 은 HDM 과 비슷 · 분포 폭은 LWM 쪽이 우리 단분산에 가깝다 [카드 해석] |
| SE σ 와 입경 | 2 h LWM 에서 펠릿 σ₂₅ ×0.25 (D50 1.01 → 0.79 µm) | Cronau(r_SE) = **모델 가정** (r ≥ 0.5 → 1.00 · 0.3–0.5 → 0.90 · `SELF-51`) [우리] | 이 논문의 하락은 같은 그룹 Cronau 2022 처럼 **밀링 손상과 함께 움직이는 값**으로 읽힌다 — 입경 인자 근거 아님 [카드 해석] |
| 복합 공극 | 392 MPa · 뺀 뒤 캘리퍼: 9.4–22.7 % · 고체 중 SE 30 % (85:15) 에서 21.3 / 20.2 % | real_14 DEM ε_sphere **15.6 %** (300 MPa · 누른 채 · SE ≈26–27 % of solid) [우리 CLAUDE.md SE-DUMP 절] | 상태 (뺀 뒤 ↔ 누른 채) · 압력 · SE · AM 크기 다름 — 판정 아님 |
| 순수 SE | 공극 값 없음 · σ₂₅ 4.43 / 1.09 (392 MPa 펠릿 · 98 MPa) · LPSCl 진밀도 문헌 1.86 (SI 표 S1) | 랩 표준 **10–13 % @300 MPa · 진밀도 1.64** [우리 · 고정] · σ₀ 보고 1.5 · 솔버 3.0 [우리] | 1.86 은 **랩 표준과 다른 문헌 값** (판정 아님) |
| τ 정의 | τ_eff = σ₀·ε_SE/σ_eff (자기 펠릿 σ₀) | tau2 = φ·σ₀/σ_eff (고정 σ₀ · 약분) [우리 τ 규약] | 같은 꼴 · 다른 기준 상태 (§4-2) |
| τ 크기 | HDM 6.3 · ≈21 · 35.4 · LWM 3.1 · ≈4.7 · 8.0 (ε_SE 0.45 · 0.29–0.32 · 0.235) | ps45 Hertz tau2 **7.24–5.03** (AM 고체 64.7–64.9 %) · 그 73–75 % = SE–SE 협착 [우리 CLAUDE.md 10-13] | 자릿수 감각만 (재료 · φ_SE · 기준 다름) |
| 절대 σ_eff | HDM 0.316 / 0.029 · LWM 0.161 / 0.032 mS/cm (ε 0.45 / 0.235) [카드 산술] | ps45 Hertz σ_ion (σ₀ 1.5) 0.0587–0.0893 mS/cm [우리] · Bazzoun 2026 EIS 0.137 / 0.101 / 0.065 (70 / 75 / 80 wt% · LPSCl · 400 MPa) [다른 카드 `bazzoun2026_dem_fem_rnm_ionic`] | 다른 SE · 다른 온도 처리 — 값 대조 아님 |
| 탈압 | 없음 | 언로딩 시험 (등록 단계) [우리] | 대조점 없음 |

### 7-2. ★ 정의 대조 — "같은 이름 · 다른 연산자"
| 항목 | König 2023 | 우리 |
|---|---|---|
| 공극 | 1 − V_solid/(d·A) · d = 캘리퍼 (뺀 뒤) · V_solid = 질량 / 추정 진밀도 (표 1) — ⚠ 식 (6) · (8) · 표 S2 는 공극비 | DEM ε_sphere (구 부피 합 · 질량 보존) / ε_union · 순수 SE 랩 표준은 진밀도 1.64 기준 [우리] |
| ε_SE / φ_SE | SE 부피 (질량 / 2.01) ÷ d·A | SE 구 부피 합 ÷ 전극 부피 [우리] |
| σ₀ | 각 SE 의 순수 펠릿 (392 / 98 MPa · 25 °C 외삽) | 솔버 σ_grain 3.0 (펠릿값 · `CL-91`) · 보고 1.5 — 한 값 [우리] |
| σ_eff | Warburg-short R_ion (외삽) + 펠릿 두께 | Kirchhoff 접촉망 (Holm 협착) · 복셀 FV (STEP3 · CONTACT_FREE 가지) [우리] |
| τ | τ_eff (= tau2 꼴) | tau2 · f · tau · τ_geo [우리 τ 규약] |

⇒ **맞대기 규칙 (결과 전에 적어 둠)**: ① τ 는 **f (= ε/τ) 와 절대 σ_eff 를 함께** 견준다 — 정규화 기준이 다른 τ 끼리는 맞대지 않는다 ② 우리 쪽 "SE 를 작게" 하는 팔은 **기하 (tau2) 와 고유 σ 변화 (σ₀) 를 따로** 보고한다 — 이 논문은 둘이 반대로 움직여 절대 σ_eff 가 거의 그대로였다 ③ 공극은 표 1 (참 기공률) 만 쓴다 (표 S2 공극비 쓰지 않음) ④ 값 차이를 모델 오차로 읽지 않는다 (frame[4]).

### 7-3. 나란히 놓을 정본 카드 (값 · 조건 그대로 · 기존 카드는 고치지 않는다)
| 카드 | 계 | 압력 · 상태 | 측정 | 그 카드의 값 |
|---|---|---|---|---|
| **이 논문** | NCM85 + Li₅.₃PS₄.₃ClBr₀.₇ (HDM / LWM) · 70:30 · 80:20 · 85:15 wt% · 탄소 없음 | 392 MPa · 뺀 뒤 (캘리퍼) | 두께 + 추정 진밀도 · 대칭셀 EIS | 공극 11.1 · 22.7 · 21.3 / 9.4 · 13.5 · 20.2 % · τ 6.3 → 35.4 / 3.1 → 8.0 |
| `minnmann2021_jes_charge_transport_bottlenecks` | NCM622 + LPSCl (± LWM) | 380 MPa · 공극 실측 7.6–17 % (평균 14 % 를 가정값으로) | 일반화 TLM · τ² | τ_ion² 2.40 → 130 (φ_SE 61 → 25 %) · fine SE 33.8 (밀링 전 σ₀ 1.6 기준) [다른 카드] |
| `park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics` | NCM811 + LPSCl **70:30 · 80:20 · 85:15 wt** + C65 | 300 MPa 2 분 조립 | XCT (0.65 µm) | '공극 + 탄소' 14.7 · 18.1 · 23.3 % [다른 카드] |
| `jeong2024_operando_densification_chemomechanics_se_size_composite_cathode` | NCM811 + LPSCl ≈1 vs 3–5 µm (70 : 27.5 : 2.5 wt%) | 370 MPa · 뺀 뒤 XCT | 분할 기공 | 11 vs 16 % (작은 SE 가 낮음) [다른 카드] |
| `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` | LTO + Li₇P₂S₈I 유리 + C65 | — | 대칭셀 TLM · 전자 차단 Li⁺ | τ 1.6–1.8 (ε 0.665) → ≈3.3 × 10² (0.297) [다른 카드] |
| `miss2026_pressure_tortuosity_composite_cathode_coating` | NMC622 + 0.67Li₃PS₄–0.33LiI 유리 | 8.8 → 663 MPa · 누른 채 | EIS (같은 압력 펠릿 σ₀) | τ_ion 압력 의존 약함 (예: pc 무코팅 ≈3.4 → 2.6) [다른 카드] |
| `cronau2022_wet_milling_particle_size_ionic_conductivity` | Li₅.₅PS₄.₅Cl₁.₅ 유리-세라믹 · LWM (⌀1 mm · 200 rpm) | — | 펠릿 σ | 2.5 → 1.73 (2 h) → 0.36 mS/cm (50 h) [다른 카드] |
| `bazzoun2026_dem_fem_rnm_ionic` | NMC811 + LPSCl 70 / 75 / 80 wt% | 400 MPa | EIS | σ_eff,ion 0.137 / 0.101 / 0.065 mS/cm · 펠릿 1.02 [다른 카드 · 우리 CLAUDE.md] |

- 읽는 법: **같은 질량비 (70:30 · 80:20 · 85:15) 를 쓴 두 실험** (이 논문 · Park 2025) 의 공극은 측정 연산자 (캘리퍼 + 추정 진밀도 ↔ XCT '공극 + 탄소') · 압력 (392 ↔ 300 MPa) · SE · 탄소가 달라 순서도 맞지 않는다 (이 논문 80:20 HDM 22.7 > 85:15 21.3 ↔ Park 18.1 < 23.3).  "작은 SE → 낮은 공극" 방향은 Jeong 2024 와 같다 (이 논문 세 쌍 모두 LWM < HDM).

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **실험 (수송 · 정규화 τ)** — 우리 분업으로는 DEM 쪽 (접촉망 σ_ion · tau2) 의 **측정 쪽 짝**이고 MPM 쪽 (형상 · 소성 유동) 은 FIB 단면 (2D · 정성) 으로만.
- 없는 반쪽: 모델 · 압력 곡선 · 하중 아래 상태 · 탈압 · 응력 · 입자 변형 값 · 3D 미세구조 정량.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = NCM85/10/5 + **Li₅.₃PS₄.₃ClBr₀.₇ 유리-세라믹** · 탄소 없음 — 우리 계 (NCM811 + LPSCl) 와 **SE 부터 다르다** · 392 MPa 한 압력 · 뺀 뒤 캘리퍼.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ **문헌 공극 칸 다섯**의 근거: ⓐ 상태 (캘리퍼 = 뺀 뒤) ⓑ 연산자 (두께 + 질량) ⓒ 분모 (추정 진밀도 — NCM 은 다른 조성 문헌값 · SE 는 음이온 몰부피 규칙) ⓓ **정의 (참 기공률 ↔ 공극비)** — 같은 논문의 표 1 ↔ 표 S2 가 다른 양 (§3-4) ⓔ 두께 해상도 (1 µm → ±0.5 %p) · ★ 표가 m · d · V_solid 를 주면 공극을 다시 계산해 정의를 확인하는 규칙 | 압력 곡선 · 하중 아래 값 · 반복 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 순수 SE 공극 값 없음 · 진밀도 문헌값 표 (SI 표 S1: Li₆PS₅Cl **1.86** — 랩 표준 1.64 와 다른 문헌 값) · 펠릿 제조 392 MPa 90 s | 맞춤 표적 없음 · 다른 SE |
| **단계 5** (3D 복합 압밀) | **결과 전 대조 항목 (방향)**: ① 같은 질량비에서 SE 를 작고 좁게 (D95 3.17 → 1.25 µm) 하면 392 MPa 뒤 공극이 준다 — 80:20 −9.2 %p · 70:30 −1.7 %p · 85:15 −1.1 %p (n = 1) ② AM 몫이 클수록 공극이 크다 (70:30 → 85:15 에서 9–11 → 20–21 %) — 고체 중 SE 30 % (85:15) 에서 20–21 % (뺀 뒤 · 392 MPa) ↔ real_14 DEM 15.6 % (누른 채 · 300 MPa) [우리] | 한 압력 · 다른 SE · 뺀 뒤 · 우리 DEM SE 는 단분산 (HDM 의 굵은 꼬리 없음) |
| **단계 6** (탈압 · 되돌아옴) | 없음 (두께는 뺀 뒤로 읽히나 되돌아옴 몫 분리 안 됨) | — |
| **단계 7** (형상 · 피복 · 수송) | ★★ **τ_eff (= tau2) vs ε_SE 실험 곡선 둘** (HDM · LWM 각 3 점 · 그림 4) + 절대 σ_eff (카드 산술) — 우리 tau2 · f · σ_ion 의 **결과 전 대조 항목 (방향 · 자릿수)** · ★ **정규화 함정**: 처리 (밀링) 가 SE 고유 σ 를 바꾸면 '자기 펠릿 τ' 는 기하 이득을 과장해 보인다 → 우리 보고는 tau2 와 함께 f × σ₀ (절대 σ_ion) 와 σ₀ 기준을 늘 같이 (§9) | 다른 SE · σ₀ 선택 [미확인] · 본문 수 자기 불일치 (§3-8c) · 25 °C 외삽 |
| **후보 D0** (지금 DEM) | ★ SE 입도 축 결과 전 대조: 우리 DEM 은 단분산 SE (⌀1.0 µm) 라 **LWM 쪽 분포가 더 가까운 실험 짝** · DEM 접촉망에서 SE 를 줄이면 접촉 · 경로가 늘어 tau2 가 줄 것 (방향) — 그 크기를 이 논문 τ 비 (4.4 배 at 0.235) 로 견주면 안 된다 (그 대부분이 σ₀ 차) · 같은 σ₀ 로 보면 0.235 에서 HDM ≈ LWM (35.4 ↔ 32.5 [카드 산술]) | DEM 의 구 · 점접촉 · 협착 모형이 '분포 균질성' 을 어디까지 담는지 이 논문은 말하지 않는다 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 없음 | — |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | 없음 (FIB 단면의 'SE 가 NCM 사이를 고르게 채움' 은 정성 그림뿐 · R6 참고) | 하중 몫 · 변형 값 없음 |
| **후보 B** (입자별 FE + 접촉) | 없음 | — |
| **후보 C** (큰 변형 접촉 DEM · MDR 류) | 없음 | — |
| **후보 C′** (항복 캡 탄소성 접촉 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀 · 캡 소성 · Heckel) | 없음 (한 압력) | — |
| **U0–U6** | 없음 | — |
| **R1–R7** | **R6** (SE 형상 변형): FIB 단면에서 SE 가 NCM 둘레 · 사이를 메운 모습 (정성 · 2D) · **R3** (SE 입자 경계 기억): 이 논문은 경계 · 입계를 다루지 않음 — 다만 LWM 펠릿 σ 의 큰 하락 + 높은 활성화 에너지 (0.39 ↔ 0.22 eV [카드 산술]) 는 '작게 간 SE 의 입계 · 손상' 이 수송에 들어간다는 방향 신호 [카드 해석] | R1 · R2 · R4 · R5 · R7 값 없음 |
| **결과 전 대조 항목** | ① τ_eff(ε_SE) HDM 6.3 / ≈21 / 35.4 · LWM 3.1 / ≈4.7 / 8.0 (자기 펠릿 σ₀) ② 같은 기준 (HDM σ₀) 으로 본 LWM 12.6 / ≈19 / 32.5 [카드 산술] ③ 절대 σ_eff (≈0.03–0.4 mS/cm · LPSClBr₀.₇ · 25 °C 외삽) ④ 392 MPa 공극 9.4–22.7 % (뺀 뒤) — **전부 방향 · 자릿수 항목 · 맞추지 않음** | LPSCl 값 아님 · 우리 랩 표준 (10–13 % · 1.64) 과 같은 표에 넣지 않는다 |

- **흐름 밖 (수송 · 공정 · 입도 설계)**: ① 같은 그룹의 세 τ 규약 (König = 자기 펠릿 · Miß 2026 = 같은 압력 펠릿 · Minnmann = 밀링 전 펠릿) — 정규화를 장부에 적어 두지 않으면 '습식 분쇄로 τ 가 4 배 준다' 같은 문장이 절대 수송 이득처럼 옮겨진다 (wolf2026 L348 · lei2026 L267 의 옮김) ② 입도 설계: 굵은 SE 꼬리 (D95 ≈ CAM 크기) 를 잘라내는 것이 질량비 80:20 에서 공극을 크게 줄였다 — 우리 SE PSD 폭 축 (yano2026 카드 계열) 과 같은 방향의 실험 한 점.
- **재료 · 차원 · 조건 차이**: SE (Li₅.₃PS₄.₃ClBr₀.₇ 유리-세라믹 ↔ Li₆PS₅Cl) · AM (NCM85 다결정 3–6 µm ↔ NCM811 이봉) · 탄소 없음 · SOC50 · 392 MPa (한 번 · 뺀 뒤) ↔ 300 MPa (누른 채) · 대칭셀 EIS (외삽 R) ↔ 접촉망 Kirchhoff · 2D SEM 입도 ↔ 3D 구.

## 9. 적용 인사이트 (행동)
1. **보고 규칙 (단계 7 · 흐름 밖)**: 수송 결과를 낼 때 tau2 하나만 쓰지 않고 **f · 절대 σ_ion · σ₀ 기준**을 같은 줄에 둔다 — 처리 조건이 SE 고유 σ 를 바꾸는 비교 (밀링 · 입경 · 열화) 에서는 특히.  근거: 이 논문의 τ 하락 4.4 배 중 ≈94 % 가 σ₀ 하락 (§3-8a).
2. **문헌 τ 인용 꼬리표 (J 절)**: "τ_eff = tau2 꼴 · σ₀ = 각 SE 자기 펠릿 (392 / 98 MPa · 25 °C 외삽) · LWM σ₀ 선택은 근사 추정" — wolf2026 · lei2026 의 "습식 분쇄로 τ↓" 를 쓸 때 "절대 σ_eff 는 ε_SE 0.235 에서 거의 같음 (König 2023 · 카드 산술)" 을 붙인다.
3. **공극 인용 규칙 (단계 0)**: 문헌 표가 m · d · V_solid 를 주면 공극을 다시 계산해 **참 기공률인지 공극비인지** 확인한다 — 이 논문은 같은 측정에서 두 정의가 공존한다 (표 1 ↔ 표 S2 · 식 6 · 8).
4. **SE 입도 팔 설계 (D0 · 흐름 밖)**: 우리 단분산 SE 침대를 이 논문 LWM 분포 (D50 0.79 · D95 1.25 µm) 쪽의 짝으로 놓고, '굵은 꼬리 (≈CAM 크기)' 를 넣은 팔을 HDM 짝으로 등록할 수 있다 — 기하 tau2 차이만 보고, σ₀ 차이 (밀링 손상) 는 모형 밖 입력으로 따로 둔다 (Cronau(r_SE) 는 이 하락의 근거가 아니다).
5. **임피던스 외삽 표지 (흐름 밖 · Rint 와 무관)**: 문헌 R_ion 을 쓸 때 호가 실수축에 닿았는지 본다 — 이 논문은 대부분 외삽 (§3-7).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Wet milling (heptane/dibutyl ether, 1 mm ZrO₂ balls, 200 rpm, 2 h) of a dry-milled glass-ceramic Li₅.₃PS₄.₃ClBr₀.₇ reduced D50/D95 from 1.01/3.17 to 0.79/1.25 µm and lowered the ion transport tortuosity factor (σ₀ε_SE/σ_eff) of carbon-free NCM85 composite cathodes from 35.4 to 8.0 at ε_SE ≈ 0.24 (König et al., *ACS Appl. Energy Mater.* 6 (2023) 9356)."
- "The same wet milling lowered the pure-SE pellet conductivity at 25 °C (extrapolated) from 4.43 to 1.09 mS cm⁻¹ (SI Fig. S2), so the absolute effective ionic conductivity at ε_SE ≈ 0.24 barely changed (≈0.029 → ≈0.032 mS cm⁻¹; our arithmetic from the reported τ and ε_SE)."
- "Composite porosity from 392 MPa pellets (caliper thickness, estimated true densities) was 22.7 % (dry-milled SE) vs 13.5 % (wet-milled SE) at 80:20 wt%, but only 11.1 vs 9.4 % at 70:30 and 21.3 vs 20.2 % at 85:15."
- 국문 (한정어와 함께): *"Br 치환 유리-세라믹 아지로다이트를 습식으로 한 번 더 갈면 탄소 없는 NCM85 복합 양극의 '자기 펠릿 기준' 이온 tortuosity 가 ε_SE ≈ 0.24 에서 35 → 8 로 준다 (König 2023) — 단 같은 처리로 순수 펠릿 σ 도 4.43 → 1.09 mS/cm 로 떨어져 절대 유효 전도도는 거의 같다 (카드 산술) · 공극은 392 MPa 한 압력 · 캘리퍼 두께 · 추정 진밀도 값이다."*

## 11. 주의/한계 (over-claim 방지)
1. **우리 계가 아니다** — Li₅.₃PS₄.₃ClBr₀.₇ 유리-세라믹 · NCM85 다결정 · 탄소 없음 · SOC50.
2. **τ 정규화** — 각 SE 의 자기 펠릿 σ 로 나눈 상대값 · LWM 쪽 σ₀ 선택 [미확인] · τ 하락을 절대 수송 이득으로 쓰지 않는다.
3. **본문 수 자기 불일치** — R_ion · 두께 · ε_SE 로 다시 낸 τ 비 8.37 ↔ 인쇄 5.62 (§3-8c).
4. **공극 정의 혼재** — 식 (6) · (8) · 표 S2 = 공극비 · 표 1 = 참 기공률.
5. **한 압력 · 뺀 뒤 · n = 1** — 392 MPa 펠릿 캘리퍼 두께 · 셀 속 양극 상태와 다를 수 있음 · 진밀도 추정.
6. **외삽** — R_ion (호가 안 닫힘) · σ₂₅ (측정 30 °C 까지) · SOC50 전자 σ (LCO 유추).
7. **정성 미세구조** — "더 고른 SE 분포 → 협착 감소" 는 2D 단면을 보고 쓴 해석 (정량 지표 없음).
8. **견준 문헌 정규화 혼재** — 그림 4 의 Minnmann LWM (밀링 전 σ₀) · Park (가정 σ₀ 2.52 · 어닐 LPSCl 을 'HDM' 표지) · 이 연구 (자기 σ₀).

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 25 | Kroll, M.; Duchardt, M.; Karstens, S. L.; Schlabach, S.; Lange, F.; Hochstrasser, J.; Roling, B.; Tallarek, U. Sheet-type All-Solid-State Batteries with Sulfidic Electrolytes: Analysis of Kinetic Limitations based on a Cathode Morphology Study. J. Power Sources 2021, 505, No. 230064. | 같은 그룹 · 양극 형태 (SE 입경) ↔ 수송 한계 (질문 i · m) · 카드 없음 |
| 27 | Yamakawa, S.; Ohta, S.; Kobayashi, T. Effect of Positive Electrode Microstructure in All-Solid-State Lithium-Ion Battery on High-Rate Discharge Capability. Solid State Ionics 2020, 344, No. 115079. | 계산 미세구조 τ_eff 11 @ ε_SE 0.25 — "계산이 τ 를 과소평가" 의 근거 (질문 k · m) · 카드 없음 |
| 20 | Cronau, M.; Paulus, A.; Pescara, L. P.; Kroll, M.; Renz, D.; Mekontso, J. A.; Marx, A.; Roling, B. What Limits the Rate Capability of Ultrathick Composite Electrodes in Lithium-Ion Batteries? A Case Study on the Thickness-Dependent Impedance of LiCoO2 Cathodes. Batteries Supercaps 2022, 5, No. e202200194. | LIB 띠 · "확산 모사가 τ 를 과소평가" 근거 (질문 k · m) · 카드 없음 |
| 33 | Miß, V.; Ramanayagam, A.; Roling, B. Which Exchange Current Densities Can Be Achieved in Composite Cathodes of Bulk-Type All-Solid-State Batteries? A Comparative Case Study. ACS Appl. Mater. Interfaces 2022, 14, 38246−38254. | 같은 그룹 · 복합 양극 교환 전류 (흐름 밖 · NCM 전자 σ refs) · 카드 없음 |
| S1 (SI) | Dewald, G. F.; Ohno, S.; Kraft, M. A.; Koerver, R.; Till, P.; Vargas-Barbosa, N. M.; Janek, J.; Zeier, W. G. Experimental Assessment of the Practical Oxidative Stability of Lithium Thiophosphate Solid Electrolytes. Chem. Mater. 2019, 31, 8328–8337. | SI 표 S1 Li₆PS₅Cl 밀도 1.86 g/cm³ 의 출처 (질문 a · 랩 표준 1.64 와 다른 문헌 값) · 카드 없음 |
| 21 | Ebner, M.; Chung, D.-W.; García, R. E.; Wood, V. Tortuosity Anisotropy in Lithium-Ion Battery Electrodes. Adv. Energy Mater. 2014, 4, No. 1301278. | 재구성 확산 모사 τ 1.3–2.0 (LIB) · 카드 없음 |
| 23 | Minnmann, P.; Quillman, L.; Burkhardt, S.; Richter, F. H.; Janek, J. Quantifying the Impact of Charge Transport Bottlenecks in Composite Cathodes of All-Solid-State Batteries. J. Electrochem. Soc. 2021, 168, No. 040537. | 그림 4 비교 · LWM 33.8 — 카드 = `minnmann2021_jes_charge_transport_bottlenecks` |
| 36 | Park, J.; Kim, K. T.; Oh, D. Y.; Jin, D.; Kim, D.; Jung, Y. S.; Lee, Y. M. Digital Twin-Driven All-Solid-State Battery: Unraveling the Physical and Electrochemical Behaviors. Adv. Energy Mater. 2020, 10, No. 2001563. | 그림 4 · SI 표 S3 — 카드 = `park2020_digitaltwin_assb_foundational` |
| 22 | Kaiser, N.; Spannenberger, S.; Schmitt, M.; Cronau, M.; Kato, Y.; Roling, B. Ion Transport Limitations in All-Solid-State Lithium Battery Electrodes containing a Sulfide-based Electrolyte. J. Power Sources 2018, 396, 175−181. | 같은 대칭셀 꼴 — 카드 = `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` |
| 30 | Cronau, M.; Duchardt, M.; Szabo, M.; Roling, B. Ionic Conductivity versus Particle Size of Ball-Milled Sulfide-Based Solid Electrolytes: Strategy Towards Optimized Composite Cathode Performance in All-Solid-State Batteries. Batteries Supercaps 2022, 5, No. e202200041. | 같은 LWM 계열 σ 하락 — 카드 = `cronau2022_wet_milling_particle_size_ionic_conductivity` |
| 24 | Shi, T.; Tu, Q.; Tian, Y.; Xiao, Y.; Miara, L. J.; Kononova, O.; Ceder, G. High Active Material Loading in All-Solid-State Battery Electrode via Particle Size Optimization. Adv. Energy Mater. 2020, 10, No. 1902881. | SE 입경 최적화 (DEM + 실험) — 카드 = `shi2019_high_am_loading_particle_size_assb` |
| 26 | Bielefeld, A.; Weber, D. A.; Janek, J. Modeling Effective Ionic Conductivity and Binder Influence in Composite Cathodes for All-Solid-State Batteries. ACS Appl. Mater. Interfaces 2020, 12, 12821−12833. | 계산 τ 5.0 @ 0.3 — 카드 = `bielefeld2020_effective_ionic_conductivity_binder` |
| 17 | Froboese, L.; van der Sichel, J. F.; Loellhoeffel, T.; Helmers, L.; Kwade, A. Effect of Microstructure on the Ionic Conductivity of an All Solid-State Battery Electrode. J. Electrochem. Soc. 2019, 166, A318−A328. | ε_SE ≲ 0.3 목표 · τ 10–20 @ 0.4 — 카드 = `froboese2019_microstructure_ionic_conductivity_assb_electrode` |
| 19 | Landesfeind, J.; Hattendorff, J.; Ehrl, A.; Wall, W. A.; Gasteiger, H. A. Tortuosity Determination of Battery Electrodes and Separators by Impedance Spectroscopy. J. Electrochem. Soc. 2016, 163, A1373−A1387. | LIB 띠 (3.0 → 7.0 · ε 0.7 → 0.3) — 카드 = `landesfeind2016_tortuosity_eis_electrodes_separators` |
| 18 | Thorat, I. V.; Stephenson, D. E.; Zacharias, N. A.; Zaghib, K.; Harb, J. N.; Wheeler, D. R. Quantifying Tortuosity in Porous Li-ion Battery Materials. J. Power Sources 2009, 188, 592−600. | LIB 띠 (2.5 → 3.5 · ε 0.57 → 0.30) — 카드 = `thorat2009_quantifying_tortuosity_porous_liion` |
| 34 | Wang, S.; Yan, M.; Li, Y.; Vinado, C.; Yang, J. Separating Electronic and Ionic Conductivity in Mixed-Conducting Layered Lithium Transition-metal Oxides. J. Power Sources 2018, 393, 75−82. | SOC0 NCM 전자 σ > 1 mS/cm 근거 — 카드 = `wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni` |
| S4 (SI) | Siroma, Z.; Fujiwara, N.; Yamazaki, S.; Asahi, M.; Nagai, T.; Ioroi, T. Mathematical solutions of comprehensive variations of a transmission-line model of the theoretical impedance of porous electrodes. Electrochim. Acta 2015, 160, 313–322. | T 형 TLM (식 S1) — 카드 = `siroma2015_transmission_line_model_porous_electrode_impedance` |
| S6 · S7 (SI) | Adeli, P.; Bazak, J. D.; Park, K. H.; Kochetkov, I.; Huq, A.; Goward, G. R.; Nazar, L. F. Boosting Solid-State Diffusivity and Conductivity in Lithium Superionic Argyrodites by Halide Substitution. Angew. Chem. Int. Ed. 2019, 58, 8681–8686. | Park 환산의 σ 2.52 mS/cm — 카드 = `adeli2019_halide_substitution_boosting_argyrodite` |

## 13. [미확인] 목록 (본문 7 쪽 + SI 9 쪽 전수에 없음)
1. **식 (9) 에 넣은 σ_ion,electrolyte 값** (HDM · LWM 각각 · 25 °C 외삽값인지) · **대칭셀 EIS 온도** · **대칭셀 EIS 때 적층압**.
2. 공극 펠릿의 유지 시간 · 하중을 뺀 뒤 꺼냈는지 · 반복 수 · 캘리퍼 정밀도 · 셀 속 양극의 실제 두께.
3. R_ion (HDM 0.289 · LWM 셋) · 계면 저항 · Warburg α · τ · 맞춤 오차.
4. 순수 SE 펠릿의 지름 · 두께 · 밀도 · 공극.
5. LWM 2 h 의 뜻 (밀링 ↔ 전체) · 건조 온도 · 시간 · 수율.
6. 입도 분포의 입자 수 · 크기 정의 · 수 / 부피 기준 (2D SEM).
7. XRD 정량 (결정도 · 상 분율) · LWM σ 하락의 원인.
8. 그림 S5 시료의 조성 · 질량 · 두께.
9. 라이선스 종류 (*"© 2023 The Authors. Published by American Chemical Society"* 만 인쇄).
10. 본문 R_ion ↔ τ 비 불일치 (§3-8c) 의 원인.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 본문 7 쪽 · SI 9 쪽을 PyMuPDF 글자 층 + 렌더로 읽음.  식 (1)–(9) · (S1) 은 글자 층에서 흩어져 렌더 조각으로 확인 (식 6 · 8 의 '(1 + ε_void)' · 'd·A/V_solid − 1' · 인라인 Warburg 의 β · SI 그림 S4 캡션 위첨자 1 · 2 · 2 · 2 · 3).  서지 = PDF 1 쪽 (제목 · 저자 · Cite This · 접수 / 승인 / 출판 · DOI) + p.6 저자 정보 + 쪽 바닥 (호 18 · 내려받기 경로).
- 그림 크롭 **53 장** = 도구 15 (본문 그림 1–5 · 표 1 · SI 그림 S1–S6 · 표 S1–S3) 중 **2 장 다시 자름** (fig_S1 = SI p.2 절 머리 줄 *"milling (LWM) step"* 섞임 → 래스터 xref 72 경계 · fig_S3 = 축 이름 아래 0.65 pt 잘림 → 래스터 경계) + **손 크롭 38** (식 10 · 그림 5 패널 8 · 근거 문단 20) — 본 뒤 다시 렌더 2 (x2b · x2c 다음 줄 위첨자 '23' '24' 가 윗줄 상자 위로 올라옴 → 흰 칠 가림).  53 장 전부 열어 확인.
- 판독: 모든 그림이 래스터 (벡터 그림 없음) · 본문 그림 원본 ≈300 dpi · SI ≈220 dpi 에서 화소로 · 재현 확인 = 그림 4 의 이 연구 점 x 값 = 표 1 ε_SE (±0.1 %p) · y 값 = 본문 τ (6.27 · 35.5 · 3.04 · 8.03 ↔ 6.3 · 35.4 · 3.1 · 8.0) · Park 세모 = SI 표 S3 (17.6 · 9.79 · 3.53 ↔ 17.6 · 9.8 · 3.5) · Minnmann 네모 = 정본 카드 값 · 그림 S2 의 ln σ 맞춤 → σ₂₅ 4.43 · 1.09 (범례와 같음) · 그림 S3 D50 판독 1.02 · 0.79 (인쇄 1.01 · 0.79).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 + DOI (`acsaem.3c01242`) · "9356" · 제목 낱말 grep — 이 논문 카드 없음 (lei2026 [78] · wolf2026 [57] · miss2026_pressure_tortuosity [12] 에 인용만).

## 🔗 관련 카드
- 이 논문을 인용한 정본 카드: [`lei2026_se_particle_size_effects_review`](lei2026_se_particle_size_effects_review.md) ([78] · L238 · L267) · [`wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode`](wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode.md) ([57] · L348) · [`miss2026_pressure_tortuosity_composite_cathode_coating`](miss2026_pressure_tortuosity_composite_cathode_coating.md) ([12]).
- 같은 그룹 (Marburg · Roling): `miss2026_insitu_conductivity_porosity_pressure_compaction` · `miss2026_pressure_tortuosity_composite_cathode_coating` · `cronau2022_wet_milling_particle_size_ionic_conductivity` · `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` · `hlushkou2018_void_space_ion_transport_assb_cathode`.
- SE 입도 · 복합 수송: `minnmann2021_jes_charge_transport_bottlenecks` · `schlautmann2023_se_particle_size_composite_transport` · `jeong2024_operando_densification_chemomechanics_se_size_composite_cathode` · `yadav2021_lpscl_sieved_psd_impedance_tortuosity` · `yano2026_se_psd_width_ionic_tortuosity_dem` · `shi2019_high_am_loading_particle_size_assb`.
- 같은 질량비 복합 양극: `park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
