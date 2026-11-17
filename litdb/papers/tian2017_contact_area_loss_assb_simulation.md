<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     본 = tian2020_electrochemo_mechanical_stress_assb.md (같은 그룹 · 이 논문이 그 카드의 ref [24]) · 절 체계 = ohashi2020_stress_distribution_composite_electrode_sulfide_assb.md (같은 키트 · 같은 날).
     고른 의도 = 위시 11-17 W-1117-3 · 정독 batch_51 (koerver2018) 의 n 줄 (ref 30) — §0-1.
     쪽 표기 = PDF 쪽 (p.1 = IOP 표지 · 논문 아님 · p.2–11 = 학술지 E3512–E3521 · 인쇄 쪽 = PDF 쪽 + 3510).  크롭 파일 이름의 pN · figures.json 의 page 도 PDF 쪽이다.
     보충 자료 (SI) = 원문에 안내 없음 (10 쪽 텍스트 층 전수에 'supplement' · 'supporting' 0 회) · 그래픽 초록 없음.
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 214 행 · 300 dpi 원 래스터 픽셀을 눈금으로 환산 —
     방법은 그 파일의 method · note 칸) · [판독 · 눈으로] = 격자 눈금을 눈으로 읽은 어림 (오차 범위 병기) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 · 가정 병기 ·
     스크립트 = 카드 §3-5 의 검산 절차) · [카드 해석] · [카드 추론] = 원문에 말이 없어 이 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드에 적힌 값 (slug 병기) ·
     [우리] = 우리 쪽 값 (CLAUDE.md 출처) · [미확인] = 원문 (본문 10 쪽 전수) 에 없음.
     크롭 · 판독 원자료는 같은 날 앞 회차가 만들었고 이 회차가 전부 다시 열어 보고 독립 검산했다 (§원문 대조 기록). -->
# 접촉 면적 손실 → 방전 용량 (1-D Newman 전기화학 · Li | LiPON-like Li₃PO₄ 1500 nm | LiCoO₂ 320 nm 박막 셀 · 접촉 인자 γ = A/A₀ 1 → 0.75 · 0.1–20 C) 과 압력 → 실접촉 면적 (Persson 다척도 탄성 접촉 · 무점착 · 박막 Li₃PO₄–LiCoO₂ ↔ 압분 LGPS–TiS₂) — 1 C 에서 γ 0.8 이면 용량 −20 % · 3.8 V 기울기 ≈1 · 4.0 V −0.34 → −0.26 · 20 MPa 70 % → 거칠어진 뒤 49 % → ≈57–60 MPa 로 회복 · 그림 6 곡선 = 인쇄 식 26 (E*/σ₀ 1 제곱) 꼴 — Tian & Qi (J. Electrochem. Soc. 2017)

> slug `tian2017_contact_area_loss_assb_simulation` · DOI `10.1149/2.0481711jes` · type `continuum — 1-D Newman-type electrochemical FEM (Li / LiPON-like Li3PO4 / LiCoO2 film cell; contact factor gamma scales the cathode exchange current and the interfacial Li source, worst case = lost cathode material) + Persson multi-scale elastic contact theory (power-law roughness spectrum, no adhesion, erf closed form) for contact ratio vs pressure — no DEM / MPM / particles / plasticity / unloading` · PDF `Simulation_of_the_effect_of_contact_area_loss_in_all-solid-state_Li-ion_batteries.pdf` · digested `2026-11-17` · status ✅
>
> **저자 (머리글 그대로)**: **Hong-Kang Tian** · **Yue Qi**\* ᶻ — Department of Chemical Engineering and Materials Science, Michigan State University, East Lansing, Michigan 48824, USA · \* Electrochemical Society Member · ᶻ 교신 `yueqi@egr.msu.edu` · *J. Electrochem. Soc.* **164** (11) **E3512–E3521** (2017) · Manuscript submitted 2017-04-17 · revised 2017-06-07 · Published 2017-06-23 · *"This was Paper 1153 presented at the New Orleans, Louisiana, Meeting of the Society, May 28-June 1, 2017"* · **JES Focus Issue on Mathematical Modeling of Electrochemical Systems at Multiple Scales in Honor of John Newman** · OA **CC BY 4.0** (p.2 · `txt_p2_abstract_box_doi_dates.png`) · 자금 = DOE BES EFRC **NEES** (Nanostructures for Electrical Energy Storage · Award DESC0001160) (p.10).
> **이웃 카드 (링크만)**: [`tian2020_electrochemo_mechanical_stress_assb`](tian2020_electrochemo_mechanical_stress_assb.md) (같은 그룹 후속 · 이 논문 = 그 카드 ref [24] · 2.5D 축대칭 COMSOL 화학-역학 · 이 논문이 *"more sophisticated 2D and 3D models … are being developed"* (p.9) 라 한 갈래의 하나 [카드 해석]) · [`koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb`](koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb.md) (이 논문을 ref 30 으로 · *"re-tightening a cell is not sufficient"* — 고른 의도의 출처 · §0-1) · [`ohashi2020_stress_distribution_composite_electrode_sulfide_assb`](ohashi2020_stress_distribution_composite_electrode_sulfide_assb.md) (이 논문을 ref [7] 로 · 서론 근거) · [`deng2016_elastic_superionic_electrolytes_dft`](deng2016_elastic_superionic_electrolytes_dft.md) (이 논문 ref 67 = LGPS E 21.7 GPa · ν 0.37 의 원전) · [`greenwood1966_constriction_resistance_microcontact_cluster_real_area`](greenwood1966_constriction_resistance_microcontact_cluster_real_area.md) (다른 Greenwood 1966 — 미세접촉 군집의 협착 · 겉보기 면적 규칙 · 이 논문의 ref 43 Greenwood–Williamson 1966 과 **다른 논문**) · [`bucci2017_chemomech_failure_assb_cycling_czm`](bucci2017_chemomech_failure_assb_cycling_czm.md) (사이클 부피 변화 → 박리 · 이 논문 ref 34 는 다른 Bucci 2014 JMPS).
> **판독 원자료**: `litdb/figures/tian2017_contact_area_loss_assb_simulation/digitized.csv` (214 행 — 그림 2b 두 직선 맞춤 + 0.5 단위 점 · 그림 4 의 3.7 V 끝 용량 + 임계선 18 · 그림 5 표식 60 · 그림 6 곡선 107 + erf 맞춤 10 + A · B · C 원 중심 3) · 크롭 **67 장** (도구 6 = 그림 1–6 → 6 장 모두 원 래스터에서 다시 자름 / 손 크롭 61 = 표 3 (도구가 JES 로마 숫자 캡션을 못 읽음) · 패널 14 · 식 24 (번호 1–27 전부 · 짝 셋) · 근거 문단 20) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 이 논문은 **입자를 하나도 풀지 않는다** — 박막 전고체 셀 (Li 금속 | 1500 nm LiPON-like 'Li₃PO₄' | 320 nm LiCoO₂) 을 1-D Newman 꼴 연속체로 놓고, 양극–전해질 계면의 접촉 손실을 **접촉 인자 γ = A/A₀** 하나로 넣어 (교환 전류 i₀ ∝ γ · 계면 Li 생성 ∝ 1/γ = **닿지 않은 LiCoO₂ 는 못 쓴다는 최악 가정**) 정전류 방전을 풀면, 1 C 에서 γ 0.8 이면 용량 −20 % · 10 C 에서 γ < 0.85 이면 수명 끝 (80 %) [인쇄 p.8] · 낮은 차단 전압 (3.8 V) 에서 용량 손실 ↔ 접촉 손실 기울기 ≈1 · 4.0 V 에서 −0.34 (0.1 C) → −0.26 (20 C) [인쇄 p.8]; 이어 **Persson 다척도 탄성 접촉 이론** (자기 닮은 거칠기 C(q) ∝ q^m × 10^I · 무점착 · 관찰 척도 = 1 C Li 확산 길이 3.6 µm) 으로 압력 → 접촉 비율을 계산해, 박막 계면이 20 MPa 에서 ≈70 % → 사이클로 거칠어지면 ≈49 % → **≈60 MPa 로 올리면 70 % 로 되돌아온다** 고 제안한다 [인쇄 p.10 · 판독 Fig. 6a].  압분 LGPS–TiS₂ 계면은 19 MPa ≈40 % · 230 MPa ≈95 % 로 Li et al. 2016 의 사이클 유지율 차이와 *"agree well"* 이라 적는다 (정량 대조 아님) [인쇄 p.10].

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 접촉 면적 비율 ↔ 성능 (용량 · 전압 · 저항) 의 정량 | **용량**: 3.7 V 끝 용량 (1 C) 9.58 · 9.10 · 8.63 · 8.15 · 7.63 · 7.16 µAh cm⁻² (γ 1 → 0.75) = 최대 9.60 의 거의 γ 배 · 10 C 9.05 → 6.59 · 3.8 V 기울기 0.98–1.01 · 4.0 V 0.339 → 0.266 [판독 Fig. 4 · 5] (인쇄 −0.34 · −0.26) · **전압**: 같은 율에서 γ ↓ → 방전 곡선 전체가 내려간다 (*"increase of interface resistance and ohmic loss"*) — **저항 값 (Ω · Ω cm²) 은 없다** | [판독] Fig. 4b · 4c · 5 · [인쇄] p.8 · [미확인] |
| ② ★ 다시 조이기 (재가압) 로 되돌아오는 몫 · 조건 | 박막 Li₃PO₄–LiCoO₂: 점 A (≈20 MPa · γ ≈0.70) → 사이클로 거칠어짐 (m, I 변경) → 같은 압력의 점 B (γ ≈0.49 · *"around 20% of the contact area is lost"*) → 점 C (≈57 MPa [판독] · *"increasing the contract pressure to 60 MPa will recover the contact area to 70% again"* [인쇄]) · 곡선 맞춤으로 회복 배수 **(c_검정/c_분홍)² = 2.58** (출발점과 무관) [카드 산술] · 용량 회복은 **계산하지 않았다** — 그림 5 의 직선 관계로 '거꾸로 읽자' 는 제안뿐 (p.10) | [인쇄] p.10 · [판독] Fig. 6a · [카드 산술] §3-6 |
| ③ 압력 → 접촉 (조건) | Persson 탄성 · 무점착 · E* 박막 68.35 · 압분 22.67 GPa [카드 산술 식 24 + Table 3] · 관찰 척도 3.6 µm (ξ ≈2700) · C(q) = Flys et al. [47] 의 RMS 15 · 120 nm 시료 (전고체 시료 아님) · **누른 채 · 상온 개념 없음 (탄성) · 하중을 빼는 계산 없음** | [인쇄] p.5–7 · Table 3 |
| ④ ★ 인쇄 식 · 그림의 정합 (재현 검산) | 그림 6 의 열 곡선은 erf(c√σ) 꼴 (rms 0.003–0.009 · 선형 erf(cσ) 꼴은 0.09–0.17) — **인쇄 식 26 (E*/σ₀ 의 1 제곱)** 에 Table 3 · 그림 2b 의 (m, I) · ξ 2700 을 넣으면 c 가 0.95 (박막) · 0.975 (압분) 배로 맞는다 · 식 22–23 을 적분한 Persson 꼴 (제곱) 이면 같은 입력에서 20 MPa γ ≈0.014 (박막) — **그림 6 · 본문 압력 숫자 (20 → 70 % · 60 MPa · 19 → 40 % · 230 → 95 %) 는 인쇄 식 26 에 묶인 값** · 원문은 이 차이를 말하지 않는다 | [판독] · [카드 산술] §3-5 |
| ⑤ 우리 사이클 접촉 원장 · Holm 협착과 견줄 꼴 | i₀ ∝ γ (반응 면적) = R_ct ∝ 1/γ 와 같은 꼴 · 따로 '닿지 않은 물질은 못 쓴다' (용량 ∝ γ · 최악) · **전해질 쪽 전류 밀도는 γ 에 무관** (*"the current density at the solid-electrolyte side of the interface is not affected by the loss of contact area"*) → 전해질 쪽 협착 (Holm 1/(2σa) · 퍼짐) 저항 **없음** | [인쇄] p.5 · 식 17 · 18 · [카드 해석] |
| ⑥ DEM 한계 · 소성의 어려움 · 2D/3D · 탈압 | DEM 을 쓰지 않음 (말 없음) · 가까운 문장 = *"Hertz, Greenwood-Williamson, and Bush models are not appropriate for large contact area (>50%) because they neglect the interaction between contacted asperities"* (p.3) · 소성: Li 금속 쪽은 *"low hardness … creep … plastic deformation"* 이라 좋은 접촉으로 보고 제외 · 세라믹 계면은 *"elastic without adhesion"* (p.7) · 1-D → *"2D and 3D models … are being developed"* (p.9) · 탈압 **없음** | [인쇄] p.2–3 · p.7 · p.9 · p.10 |

⛔ **한정어 (떼지 말 것)**: ① 재료 = **LiCoO₂ / LiPON-like Li₃PO₄ 박막** (전기화학 계산) · **LGPS / TiS₂** (접촉 계산 둘째 경우) — LPSCl · NCM **없음** ② 전기화학 매개변수 = Danilov 2011 [15] 가 박막 실험에 맞춘 값 (γ = 1) · γ 는 손으로 준 변수 (1 → 0.75) ③ 용량 ↔ 접촉 기울기 1 은 **가정에서 나온다** (*"Since we have assumed loss of material due to the loss of contact area, the capacity loss drops with loss of contact area with a slope of 1"*, p.8) ④ 압력 계산 = **탄성 · 무점착 · 다척도 평균장** · 사이클 = (m, I) 를 손으로 바꿔 흉내 (계산된 거칠어짐 아님) ⑤ **그림 6 · 압력 숫자는 인쇄 식 26 의 1 제곱 꼴** (Persson 원 꼴 = 제곱 · 원문 식 23 도 제곱) [카드 산술] ⑥ 실험 대조 = Li et al. 2016 의 **정성** (용량 유지 좋음 / 나쁨) 뿐 — 접촉 면적 실측 0 ⑦ 1-D (입자 · 형상 · 측면 확산 없음) · 하중 해제 · 되돌아옴 · 소성 · 파괴 계산 없음.
⇒ **절대값 전이**: 하지 않는다 (재료 · 박막 형상 · 탄성 접촉 · 식 26 꼴 · 다른 시료의 C(q)).  옮길 수 있는 것 = **꼴과 절차** — (i) 접촉 손실의 두 갈래 (반응 면적 → 과전압 · 닿지 않은 물질 → 용량) 를 따로 세는 회계 (ii) 깊은 차단에서는 용량 ∝ γ (최악 · 1 : 1) · 얕은 차단 · 고율에서는 같은 율 기준 상대 손실이 접촉 손실의 1.0–1.45 배 [카드 산술 §3-4] (iii) '접촉 비율' 은 **관찰 척도와 함께** 정의해야 한다 (원문 = Li 확산 길이 √(4Dt) 로 자름) (iv) '거칠어진 계면은 같은 압력으로 같은 접촉을 못 얻는다 → 더 높은 압력' 이라는 방향 (배수는 식 꼴에 따라 2.6 ↔ 1.6 [카드 산술]).

---

## 0-1. ★ 고른 의도 대조 (위시 11-17 W-1117-3 · batch_51 n 줄 + 본 세션 의도 셋)

의도 원문 (wishlist 원문 그대로): *"[n] H.-K. Tian and Y. Qi, Simulation of the Effect of Contact Area Loss in All-Solid-State Li-Ion Batteries, J. Electrochem. Soc., 2017, 164, E3512–E3521. (ref 30) | b · 단계 6 · R4 — "re-tightening a cell is not sufficient to recover capacity fade due to contact loss" 의 원전 (접촉 면적 손실 계산) | 카드 §3-7 ③ · §12"*.  본 세션이 덧붙인 의도 = ① [DEM 우선 Ⓐ] 언로딩 · 탈압 뒤 접촉 손실 — 접촉 면적 (비율) ↔ 전기화학 성능 (용량 · 전압 · 저항) 정량 · 다시 조이기로 되돌아오는 몫 · 조건 (압력 · 면적 비율 · 전류) ② 우리 사이클 접촉 원장 (접촉 개구 → R_ct 몫 · σ 몫) 과 협착 (Holm) 표현에 견줄 값 · 모델 꼴 (연속체? 계면? 2D/3D? 경계 조건) · 입력 물성과 출처 ③ 못 하는 것 (입자 해상 · 소성 · 실험 대조 여부).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 (계산) 조건 |
|---|---|---|
| (b) 압력을 뺄 때 되돌아오는 양 · 잰 방법 | **없음** | 하중을 줄이거나 빼는 계산 · 측정이 없다 ('unload' · 'relax' · 'decompress' 0 회 · 'release' 1 회 = *"the same amount of Li-ion will be generated and released at these two interfaces"* (p.4 · 압력 뜻 아님)).  그림 6 은 **가압 곡선 하나** (탄성 · 무점착이라 하중 경로와 무관한 함수 [카드 해석]) · 사이클의 효과는 하중이 아니라 **(m, I) 를 손으로 바꿔** 넣었다: *"(m, I) values were changed to mimic the effect interface roughening due to battery cycling"* (p.9 · `txt_p9_p10_…`) |
| 단계 6 (탈압 · 되돌아옴 계산) · R4 | **없음 (탈압 계산 0)** · 쓸 수 있는 꼴만 | 압력 → 접촉 곡선 (그림 6) 과 접촉 → 용량 지도 (그림 5) 를 잇는 **두 단계 절차** (p.10) 는 있다 — 탈압 계산의 결과 (접촉 손실) 를 용량 벌점으로 바꾸는 '뒷단' 으로만 쓸 수 있다 [카드 해석 · §8] |
| *"re-tightening a cell is not sufficient to recover capacity fade due to contact loss"* 의 원전 | **일부 (좁은 해석으로만) · 원문 결론은 반대 방향** | 원문 10 쪽에 'tighten' · 'sufficient' · 'insufficient' **0 회**.  원문이 말하는 것: 거칠어진 계면은 **같은 압력** (≈20 MPa) 에서 γ ≈0.70 → 0.49 (점 A → B) · *"Then to get the original contact area and the capacity back, it needs to follow the pink line, for instance, increasing the contract pressure to 60 MPa will recover the contact area to 70% again"* (p.10) · 결론: *"The model is further applied to suggest how much pressures should be applied to recover the contact area and capacity loss due to cycling"* (p.10).  ⇒ '원래 압력으로 다시 조이는 것만으로는 원래 접촉이 안 된다' 는 **점 A → B 로 맞다** (탄성 · 무점착 모델 안) · 그러나 원문은 **더 높은 압력이면 접촉 (과 가정상 용량) 을 되찾는다** 고 결론짓는다 · 용량 회복은 계산하지 않았다 (그림 5 직선의 역산 제안).  Koerver 2018 의 *"Application of an external pressure cannot fully compensate delamination"* (박리 · 소성 · 느린 변형) 은 이 논문 모델 **밖** (박리 · 소성 · 이력 없음) |
| "(접촉 면적 손실 계산)" | **채움** | 두 겹: ① γ 를 손으로 준 1-D 전기화학 (γ 1 · 0.95 · 0.9 · 0.85 · 0.8 · 0.75 × 0.1 · 1 · 5 · 10 · 20 C · 그림 3–5) ② Persson γ(σ) (박막 · 압분 × (m, I) 다섯 쌍 · 0–200 / 0–500 MPa · 그림 6) |
| `koerver2018_…` L178 (2 차 인용 원문) | **카드 = Koerver 원문 그대로 (카드 문제 아님)** | L178: *"Application of an external pressure cannot fully compensate delamination of electrode materials. Calculations by Tian et al. have shown that re-tightening a cell is not sufficient to recover capacity fade due to contact loss of materials."* (Koerver p.2151 · ref 30) — Koerver 의 문장을 옳게 옮겼다.  **귀속이 원문과 다르다** (위 행) → 인용할 때 'Koerver 2018 이 Tian & Qi 2017 을 그렇게 읽었다' 로 쓴다 |
| `koerver2018_…` L29 ⓒ · L53 · L358 · L380 | **같음 (귀속 한정 필요)** | L358 *"쓸 수 있는 문장은 … re-tightening (Tian & Qi 계산 인용)"* · L380 *"'re-tightening a cell is not sufficient' 의 원전"* — 원문에서 그 문장은 나오지 않는다 (이 카드 확인) → 정독 출력 batch_94 '카드 문제' 에 적음 (그 카드는 고치지 않는다) |
| `ohashi2020_…` L339 ([7] · *"접촉 면적 감소 계산 (서론 근거)"*) · `tian2020_…` L26 · L606 (ref [24] · *"접촉 면적 손실 모사 (같은 그룹)"*) | **채움 (숫자 옮김 없음)** | 두 카드 모두 서지 · 주제만 · 숫자 없음.  ohashi2020 [7] 의 학술지 표기 'Electrochem. Soc.' (J. 빠짐) 는 Ohashi 원문 참고문헌의 꼴 (그 카드 §11 에 이미 적힘) |
| ① 접촉 면적 비율 ↔ 용량 · 전압 · 저항 | **채움 (용량) · 일부 (전압) · 없음 (저항 값)** | 용량: Fig. 4b · 4c · 5 (§3-4) · 전압: 방전 곡선 하강 (Fig. 4b · 4c · *"The drop of voltage can be considered as the increase of interface resistance and ohmic loss due to loss of interface contact area"*, p.8) · 저항 (Ω cm² · EIS) 값 [미확인] · 조건 = 정전류 방전 · 0.1–20 C · 3.7–4.2 V · 25 °C 등 온도 [미확인] (식의 T 값 없음) |
| ① 다시 조이기 몫 · 조건 (압력 · 면적 비율 · 전류) | **채움 (계산 · 박막 · 탄성)** | 압력 20 → 60 MPa (본문) · ≈22 → ≈57 MPa (원 중심 [판독]) · 면적 비율 0.70 → 0.49 → 0.70 · 전류 조건은 접촉 계산에 **없다** (기계 계산) — 용량 쪽은 그림 5 (율별) 로 따로 |
| ② 모델 꼴 · 경계 조건 · 입력 물성 · 출처 | **채움** | 1-D 연속체 (*"solved by finite element analysis"*, p.10 · 프로그램 · 격자 · 시간 간격 [미확인]) · 계면 = 평평한 유효면 (*"one can always reduce the contact to a flat surface with an effective rough surface"*, p.4) · 경계 · 초기 · 멈춤 조건 = Table 1 · 매개변수 = Table 2 (Danilov [15] 맞춤) · 탄성 = Table 3 (refs 36 · 37 · 67 · 68 · 69) · C(q) = Flys [47] |
| ② R_ct 몫 · σ 몫 · Holm 협착과 견줄 값 | **일부 (꼴만)** | 반응 면적 꼴 i₀ ∝ γ (식 17) · 물질 손실 꼴 R_Lis ∝ 1/γ (식 18) · 전해질 쪽 협착 없음 · σ (이온 · 전자) 값 · 저항 값 없음 · 전자: *"the φs is assumed to be the same everywhere in LiCoO2"* (p.4 · 전자 경로 손실 계산 안 함) |
| ③ 못 하는 것 — 입자 해상 · 소성 · 실험 대조 | **채움 (원문이 스스로 적음)** | 입자 해상 0 (1-D · 평평한 계면) · 소성 0 (*"elastic without adhesion"*) · 실험 대조 = Li et al. [26] 정성 · 한계 두 문단 (p.10): 최악 가정 → 2-D · 3-D 필요 · 액체 전해질에서 온 식 (Butler–Volmer · 이중층 · 결함 수송) |

⇒ **의도 대조 결과: 일부** — '접촉 면적 손실 계산' 은 **채움**; 'b · 단계 6 · R4' (탈압 · 되돌아옴) 는 **없음**; *"re-tightening is not sufficient"* 는 원문 문장이 **없고** 원문 결론은 '더 높은 압력이면 회복' — '같은 압력으로는 회복 안 됨' 이라는 좁은 뜻으로만 맞는다.

---

## 1. 한 줄 요약

1-D 박막 전고체 셀 모델에 접촉 인자 γ 를 넣어 **용량 손실 ≈ 접촉 손실 (깊은 차단 · 최악 가정)** 을 보이고, Persson 탄성 다척도 접촉 이론으로 **압력 → 접촉 비율** 을 계산해 '거칠어진 계면은 압력을 ≈3 배 올리면 접촉을 되찾는다' 는 처방까지 잇는 첫 정량 시도 — 단, 그림 6 곡선은 인쇄 식 26 (Persson 원 꼴과 다른 1 제곱) 을 따르고 용량 회복은 계산이 아니라 두 그림의 연결 제안이다.

---

## 2. 메타

| 항목 | 값 |
|---|---|
| 서지 | H.-K. Tian and Y. Qi, "Simulation of the Effect of Contact Area Loss in All-Solid-State Li-Ion Batteries", *J. Electrochem. Soc.* **164** (11) E3512–E3521 (2017) · DOI 10.1149/2.0481711jes |
| 위시 서지 대조 | 위시 줄 (*"J. Electrochem. Soc., 2017, 164, E3512–E3521"*) = 원문 머리글 · 끝 쪽 E3521 ✓ · DOI 는 위시에 없었고 원문 초록 상자에서 확인 |
| 형식 | 원저 (이론 · 계산) · OA CC BY 4.0 · JES Focus Issue (Newman) · 10 쪽 · 그림 6 · 표 3 · 식 27 · 참고문헌 69 |
| 계산 | 1-D 전기화학 (Nernst–Planck + Butler–Volmer + 고체 확산 · FEM) + Persson 접촉 (반해석 erf) — 실험 0 |
| 재료 | 전기화학: Li 금속 · LiPON-like 'Li₃PO₄' 1500 nm · LiCoO₂ 320 nm (박막) · 접촉: Li₃PO₄–LiCoO₂ (film) · LGPS–TiS₂ (bulk) |
| PDF | 11 쪽 = IOP 표지 (p.1 · 다운로드 기록 · 'You may also like' 목록 — 논문 아님) + 논문 p.2–11 |
| 보충 자료 · 그래픽 초록 | 없음 (안내 없음) |
| 연구비 | NEES EFRC (DOE BES · DESC0001160) |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 모델 기하 · 조건 (p.3–5 · Fig. 1 · Table 1)

- 기하 [인쇄 p.3 · Fig. 1a]: Li 금속 음극 | **1500 nm** LiPON-like 고체 전해질 (*"referred as Li3PO4"*) | **320 nm** LiCoO₂ — 계면 x = 0 (음극) · x = 1500 nm (양극) · 끝 x = 1820 nm · A₀ = 1 cm² (*"set it is 1 cm2 in this 1-D model"*, p.4).
- 방전 = 정전류 · C-rate **0.1 · 1 · 5 · 10 · 20 C** (*"the range of C-rate usually is between 0.1 C to 10 C"* 를 근거로, p.4) · 시작 Li₀.₅CoO₂ ≈4.2 V · OCV = Fig. 3c (Li_xCoO₂ · x 0.5–1) · 차단 3.7–4.2 V 창 (*"most of the batteries operate between these values"*, p.8) · 그림 5 는 3.8 · 4.0 V 차단.
- 경계 · 초기 · 멈춤 (Table 1 · 원문 Table I): i_pos = 정한 값 · Φ_s,neg = 0 · E_eq,neg = 0 (접지) / 초기 x = 0.5 (C_Lis / C_Li,max) · Φ_s,pos = 4 · Φ_ep = 0 / **멈춤 = 양극 계면에서 C_Lis = C_Li,max** / 풀 변수 C_Li+(x,t) · C_Lis(x,t) · Φ_s,pos(t) · Φ_ep(x,t) [인쇄].  ⚠ 본문 p.4 는 *"The simulation would end at the desired cutoff voltage"* — 멈춤 조건이 둘 (§3-7).
- 접촉 인자 γ = **1 · 0.95 · 0.9 · 0.85 · 0.8 · 0.75** (Fig. 3–5 범례) · 용량 Q_out = t × C_rate / A₀ (식 27) · 임계 용량 = 최대의 **80 %** (*"end of life"*, p.8).
- 전자: *"Since the electron conductivity is much higher than the ionic conductivity in LiCoO2, it is considered as a good electronic conductor. Therefore, the ϕs is assumed to be the same everywhere in LiCoO2"* (p.4) — 전자 경로 · 전자 접촉 손실은 계산 밖.
- 온도 T: 식 2 · 12 에 있으나 값 [미확인].

### 3-2. 매개변수 (Table 2 = 원문 Table II · Table 3 = 원문 Table III · [인쇄])

| 기호 | 뜻 | 값 |
|---|---|---|
| C_Li,total | 전해질의 전체 Li 농도 | **6.01 × 10⁴** mol m⁻³ (지수 '4' 가 링크 색 — 식 7 산술로 확인 ↓) |
| C_Li,max · C_Li,min | 양극의 최대 · 최소 Li 농도 | **23300 · 11650** mol m⁻³ |
| D_Li+ | 고체 전해질 (Li₃PO₄) 의 Li⁺ 확산 계수 | **9 × 10⁻¹⁶** m² s⁻¹ |
| D_Lis | LiCoO₂ 의 Li 확산 계수 | **1.76 × 10⁻¹⁵** m² s⁻¹ |
| δ | 평형 이동 Li⁺ 분율 | **0.18** |
| k_d · k_r | 해리 · 재결합 속도 상수 (표의 단위 mol m⁻² s⁻¹) | **2.13 × 10⁻⁵ · 9 × 10⁻⁹** |
| k_pos · k_neg | 반응 속도 상수 (mol m⁻² s⁻¹) | **5.1 × 10⁻⁴ · 0.01** |
| α_pos · α_neg | 전하 이동 계수 | **0.6 · 0.5** |

- 출처: *"The parameters used and listed in Table II are based on the research of Danilov and Notten et al.,15 where they have fitted to the experimental data"* (p.4) — 이 논문이 맞춘 값은 **없다** (γ = 1 의 박막 실험 맞춤을 빌림).
- 검산 [카드 산술]: 식 7 k_d = k_r C₀ δ² / (1 − δ) = 9 × 10⁻⁹ × 6.01 × 10⁴ × 0.18² / 0.82 = **2.137 × 10⁻⁵** = 표의 2.13 × 10⁻⁵ → C₀ = 6.01 × 10⁴ 로 읽는 것이 맞다.  LiCoO₂ 이론 면적 용량 (x 0.5 → 1 · 320 nm · ΔC 11650 mol m⁻³) = 11650 × 320 × 10⁻⁹ × 96485 / 3.6 = **9.99 µAh cm⁻²** ↔ 그림 4a 최대 9.60 (임계선 7.681 = 0.8 × 9.60 [판독]) = 이론의 96 %.
- 탄성 (Table 3): Li₃PO₄ **E 103.4 GPa · ν 0.26** (ref 36 둘 다) · LiCoO₂ **171 GPa** (ref 37) · **0.2** (ref 69) · LGPS **21.7 GPa · 0.37** (ref 67 = Deng 2016 · [다른 카드] `deng2016_…` 의 LGPS 21.7 · 0.37 과 같음 — `ohashi2020_…` §0-1) · TiS₂ **228 GPa · 0.11** (ref 68).  유효 계수 (식 24) [카드 산술]: 박막 **E\* = 68.35 GPa** · 압분 **22.67 GPa**.  ⚠ ref 36 (Yang et al. 2016 ACS AMI) 은 서론에서 Li 금속 크리프 근거 (refs 36–38) 로도 인용된다 — 그 논문이 Li₃PO₄ 탄성을 담는지 [미확인].

### 3-3. 접촉 손실 → 양극 표면 Li 농도 (Fig. 3 · p.7–8)

- Fig. 3a (1 C) · 3b (10 C): x = 1500 nm 의 C_Lis 가 γ 가 작을수록 · 율이 높을수록 빨리 오른다 (*"the constant current imposed the same amount of Li produced at LiCoO2 surface, so the local concentration of Li is higher when the contact area is reduced"*, p.7) → 평탄 = C_max ≈2.33 × 10⁴ mol m⁻³ [판독 · 눈으로] = Table 2 의 23300 (본문 p.8 은 *"which is 23000 mol/m3"* — §3-7).
- 표면 포화 시각 [판독 · 눈으로 · 격자 눈금 · ±50 s (a) · ±10 s (b)]: 1 C γ 1 ≈3,550 s · γ 0.75 ≈1,900 s · 10 C γ 1 ≈340 s · γ 0.75 ≈255 s.  (1 C γ 1 의 3,550 s ≈ 이론 1 h 의 0.99 [카드 산술].)
- 기전 (원문): *"Since the diffusion rate of Lis is not as fast as the reaction rate, the high surface concertation of Lis leads to less utilized electrode particles at the cutoff voltage"* (p.8) — 용어 'particles' 는 1-D 모델에 입자가 없으므로 비유 [카드 해석].

### 3-4. 접촉 손실 → 방전 곡선 · 용량 (Fig. 4 · 5 · p.8–9)

- Fig. 4a (γ = 1): 3.7 V 끝 용량 0.1 C **9.63** · 1 C **9.58** · 5 C **9.37** · 10 C **9.05** · 20 C **8.47** µAh cm⁻² [판독] — *"the discharge capacity can still be maintained above 80% of the maximum capacity even at 20 C with perfect contact area"* (p.8 · 8.47 / 9.60 = 0.88 [카드 산술]).
- Fig. 4b (1 C): γ 1 · 0.95 · 0.9 · 0.85 · 0.8 · 0.75 → **9.58 · 9.10 · 8.63 · 8.15 · 7.63 · 7.16** (= 9.60 의 0.998 · 0.948 · 0.899 · 0.849 · 0.795 · 0.746 = 거의 γ) [판독 · 카드 산술] · Fig. 4c (10 C): **9.05 · 8.54 · 8.06 · 7.57 · 7.09 · 6.59** [판독] — 7.57 (γ 0.85) 이 임계 7.68 아래.  원문: *"if discharging at 1 C, the battery would lose 20% of the capacity if the contact area is less than 80% of the cross-section area (γ = 0.8). If discharging at 10 C, the battery would be at the "end of life" if the contact area is less than 85%"* (p.8).
- Fig. 5 (100 % = 0.1 C 용량 · [판독 · digitized.csv]):

| 차단 · 율 | γ 1 | 0.95 | 0.9 | 0.85 | 0.8 | 0.75 | 기울기 (γ 1 → 0.75) [카드 산술] | 같은 율 γ 1 기준 상대 손실 [카드 산술] |
|---|---|---|---|---|---|---|---|---|
| 3.8 V · 0.1 C | 99.71 | 94.91 | 90.03 | 85.18 | 80.18 | 75.23 | 0.979 | 24.6 % |
| 3.8 V · 1 C | 99.23 | 94.62 | 89.65 | 84.29 | 79.41 | 74.56 | 0.987 | 24.9 % |
| 3.8 V · 5 C | 97.09 | 92.15 | 87.21 | 82.15 | 77.15 | 72.23 | 0.994 | 25.6 % |
| 3.8 V · 10 C | 93.53 | 88.53 | 83.50 | 78.38 | 73.62 | 68.38 | 1.006 | 26.9 % |
| 3.8 V · 20 C | 86.91 | 82.09 | 77.18 | 72.03 | 66.91 | 61.62 | 1.012 | 29.1 % |
| 4.0 V · 0.1 C | 34.23 | 32.66 | 30.94 | 29.19 | (범례에 가림) | 25.75 | 0.339 | 24.8 % |
| 4.0 V · 1 C | 34.30 | 32.78 | 30.97 | 29.23 | (범례에 가림) | 25.70 | 0.344 | 25.1 % |
| 4.0 V · 5 C | 29.67 | 28.11 | 26.47 | 24.87 | 23.29 | 21.75 | 0.317 | 26.7 % |
| 4.0 V · 10 C | 26.56 | 25.02 | 23.53 | 22.02 | 20.50 | 18.95 | 0.304 | 28.7 % |
| 4.0 V · 20 C | 18.35 | 17.06 | 15.66 | 14.39 | 13.11 | 11.71 | 0.266 | 36.2 % |

- 원문 (p.8): *"At the cutoff voltages of 3.8 V, the slopes of all the lines are almost 1; and at the cutoff of 4.0 V, the absolute value of the slopes are all smaller than 1. For example, the slope of 0.1 C is −0.34 and the slope of 20 C is −0.26"* — 판독 기울기 0.339 · 0.266 과 같다 (판독 검증).  기울기 1 의 이유 = 가정 (§0 한정어 ③) · 4.0 V 는 표면 농도 (생성 ↔ 확산) 가 지배 · *"At higher rate, less diffusion time, the role of loss contact area will be more dominating, such the slope decreases with increasing C rate"* (p.8–9).
- ★ **읽는 법 (함정)** [카드 산술]: 4.0 V 의 '기울기 < 1' 은 **0.1 C 깊은 용량 기준 %** 로 잰 것이다.  같은 율 · 같은 차단의 γ = 1 용량 기준으로 보면 γ 1 → 0.75 (접촉 −25 %) 에서 용량 −24.8 % (0.1 C) → **−36.2 % (20 C)** — 상대 손실은 **비례 이상** 이고 율이 높을수록 커진다 (원문의 '기울기가 율과 함께 줄어든다' 와 반대처럼 보이는 것은 기준의 차이).

### 3-5. 압력 → 실접촉 비율 (Persson · Fig. 2b · 6 · 식 19–26 · p.5–7 · p.9)

- 길이 척도 [인쇄 p.5]: L = A₀^½ · q_L = 2π/L · q = ξ q_L · 관찰 척도 = 1 C 의 Li 확산 길이 *"3.6 μm, based on √4Dt"* → *"the lower limit of the q is defined by the magnification ξ of around 2700 for A0 = 1 cm2"*.  [카드 산술] √(4 × 9 × 10⁻¹⁶ × 3600) = **3.60 µm** (= 전해질 D_Li+ · LiCoO₂ D_Lis 면 5.03 µm) · ξ = 1 cm / 3.6 µm = **2778** · q_L = 628 m⁻¹ (log 2.80) · ξq_L = 1.70 × 10⁶ m⁻¹ (log 6.23).  ⚠ 원문의 'lower limit of the q' 는 식 26 의 적분 **위** 끝 ξq_L 자리로 읽힌다 [카드 해석] · 원문은 q 를 'wavelength' 라 부른다 (p.5).
- 거칠기 [인쇄 p.5–6]: AFM RMS — 박막 양극 ≈10–20 nm (refs 54–58) · 압분 양극 ≈100–200 nm (refs 59–61) · *"Currently, C(q) is not available for all-solid-state battery electrode and solid-electrolyte surface yet"* → Flys et al. [47] 의 RMS **15 nm** (박막 대표) · **120 nm** (압분 대표) C(q) · 범례 (Fig. 6): 박막 (m, I) = (−2.77, −11.35) → (−2.82, −10.85) → (−2.87, −10.35) → (−2.92, −9.85) → (−2.97, −9.35) · 압분 (−3.08, −8.61) → (−3.13, −8.11) → (−3.18, −7.61) → (−3.23, −7.11) → (−3.28, −6.61) — 한 단계 Δm −0.05 · ΔI +0.5 [인쇄 · 카드 산술].
- ⚠ 그림 2b [판독 · 직선 맞춤 · digitized.csv · 독립 재확인]: 그어진 **압분 선 m −3.076 · I −8.619** = 본문 p.9 · Fig. 6b 범례의 (−3.08, **−8.61**) — 그림 안 표지 *"I = -8.11"* 은 오기 · 그어진 **박막 점선 기울기 −2.63 (I −11.94)** ≠ 인쇄 −2.77 (log q 4.5 에서만 만나고 7.5 에서 0.43 단위 위).  Fig. 6a 검은 곡선은 **인쇄 쌍 (−2.77, −11.35)** 으로 맞고 (c 비 0.946) 그어진 점선 쌍을 넣으면 1.22 [카드 산술] → 계산에는 인쇄 값이 쓰였고 2b 점선만 어긋난다 [카드 해석].
- ★ **그림 6 곡선의 꼴 — 인쇄 식 26 재현 검산** [판독 + 카드 산술]: 열 곡선을 γ = erf(c√σ) (σ in MPa) 로 맞추면 rms **0.0025–0.0086** (선형 꼴 erf(cσ) 은 0.092–0.167) — 박막 c = 0.15802 · 0.12489 · 0.09834 · 0.07736 · 0.06087 · 압분 0.09634 · 0.07552 · 0.05900 · 0.04603 · 0.03589 MPa^−½.  인쇄 식 26 G = (π/4)(E*/σ₀) ∫ q³C(q) dq (1 제곱 · C = 10^I q^m · q_L → ξq_L 거듭제곱 그대로 · ξ 2700) 로 예측한 c 와의 비 = 박막 **0.946–0.949** · 압분 **0.974–0.976** (ξ 2778 이면 0.962–0.964 · 0.986–0.988) — 열 곡선 모두 거의 같은 비 → 그림 6 은 **인쇄 식 26 꼴** 로 계산됐다.  식 22–23 (원문 · f(ξ) 에 (E/(1−ν²))²) 을 적분한 꼴 (Persson · 제곱) 이면 같은 입력에서 박막 γ(20 MPa) = **0.0144** · 압분 γ(19 MPa) = **0.0141** (그림 6 의 ≈0.70 · ≈0.45) · 박막 γ 0.7 에 **≈1150 MPa** · 압분 γ 0.95 에 **≈2110 MPa** (인쇄 꼴 19.2 · 196 MPa).  적분은 위 끝이 지배 (q³C ∝ q^(3+m) · 4 + m > 0) 라 log q 2.8–4.5 (그려지지 않은 범위) 처리에 둔감하다 [카드 산술].
- ⚠ 식 25 가운데 적분 (위 끝 √G) 은 erf(√G/2) 와 같다 — 오른쪽 erf(1/(2√G)) 와 맞으려면 위 끝이 1/√G 여야 한다 [카드 산술 · 수학 항등식] · 그림 6 은 오른쪽 꼴 (σ₀ ↑ → γ ↑) 을 따른다.
- 원문 서술 (p.9): *"at low applied pressure, the increase of contact area with the applied pressure is nearly linear, which agrees with other contact models, such as the theories of Hertz, Greenwood-Williamson, and Bush. When the contact area ratio is greater than 60% (A/A0 = 0.6), it needs much more pressure to increase the contact area further"* — '거의 선형' 은 √σ 꼴 곡선 (낮은 압력에서 기울기가 가장 가파름) 과 맞지 않는다 [판독] · 선형은 제곱 꼴 (γ ∝ σ₀) 의 성질 [카드 산술].
- 박막 ↔ 압분 (같은 압력): 20 MPa 검은 곡선 0.68 ↔ 0.47 [카드 산술 · 맞춤] = *"at the same applied pressure the film-type has more contact area than the bulk-type"* (p.9).
- 정규화 확인 [카드 산술 · 가정 ⟨h²⟩ = 2π ∫ q C(q) dq (2D 등방)]: 인쇄 (m, I) 로 그려진 범위 (log q 4.5–7.5) 의 RMS = 박막 **112 nm** · 압분 **444 nm** — 표지 15 · 120 nm 와 다르다 · C(q) 정규화 · RMS 를 잰 범위가 원문에 없어 **판정하지 않는다** (C(q) 는 Flys 시료의 것이라 이 논문 안에서 확인 불가).

### 3-6. 다시 조이기 (A → B → C) · Li et al. 대조 (Fig. 6 · p.10)

- 원문 (p.10): *"if the initial condition for the film-type battery is under 20 MPa, as starting from point A in Figure 6a, the contact area is around 70%. After cycling, it may decrease to point B, since the surface becomes much rougher, it also means around 20% of the contact area is lost. Then to get the original contact area and the capacity back, it needs to follow the pink line, for instance, increasing the contract pressure to 60 MPa will recover the contact area to 70% again."*
- 원 중심 [판독 · 하늘색 채움 중심]: A (22.4 MPa · 0.706) · B (22.7 MPa · 0.490) · C (56.9 MPa · 0.705) — B · C 는 분홍 점선 (m −2.87 · I −10.35) 위 · '20 % lost' = 절대 0.21 (상대 30 %).
- 맞춤 곡선으로 [카드 산술]: γ(20 MPa) 검정 0.682 · 분홍 0.466 (절대 −0.216 · 상대 −31.7 %) · 분홍이 0.682 에 닿는 압력 **51.6 MPa** · 60 MPa 에서 분홍 0.719 · **회복 배수 (c_검정/c_분홍)² = 2.58** (출발 압력과 무관 · 인쇄 식 26 꼴의 J 비 2.59 와 같음) — Persson 제곱 꼴이면 같은 두 C(q) 의 배수는 √(J 비) = **1.61** [카드 산술].
- 그림 5 와의 연결 (p.10 제안): *"based on Figure 5, the lost contact area can be estimated by the capacity drop. Then, based on Figure 6, the applied pressure needed to recover the contact area and capacity can be obtained"* — ⚠ 점 A · B 의 γ (0.70 · 0.49) 는 그림 4–5 가 계산한 γ 범위 (1 → 0.75) **밖** 이고, 그림 4–5 의 γ = 1 에 가까운 상태 (γ ≥ 0.99) 는 그림 6a 검은 곡선에서 ≈130 MPa 위다 [카드 산술 · 맞춤 erf(0.158√σ) · 카드 해석] → 두 계산은 **같은 셀의 결합 계산이 아니다**.
- Li et al. [26] (In-Li / LGPS / TiS₂ · 실험): p.2 *"increased from 19 MPa to 228 MPa, the cycle stability was enhanced considerably"* · p.10 *"They applied two different pressures, 19 and 230 MPa … at 19 MPa, the contact area is only about 40% … to 230 MPa, the contact area is estimated to be around 95%"* — Fig. 6b 검은 곡선 맞춤 γ(19) **0.447** · γ(230) **0.961** [카드 산술] · 대조는 '접촉 40 % ↔ 나쁜 유지율 · 95 % ↔ 좋은 유지율' 의 정성 · 압분 계산에도 박막 전기화학 관계를 쓴다: *"It can be expected the predicted capacity loss due to contact area loss relationship is general for other all-solid-state batteries"* (p.9 · `txt_p9_p10_…`).

### 3-7. 원문 안 어긋남 (고치지 않고 적는다 · `figures.json` note_manual)

1. Fig. 2b 압분 선 표지 *"I = -8.11"* ↔ 본문 p.9 · Fig. 6b 범례 −8.61 (그어진 선 −8.62 [판독]) · Fig. 2b 박막 점선 기울기 −2.63 ↔ 인쇄 −2.77 (§3-5).
2. 식 23 (제곱) ↔ 식 26 (1 제곱 · 그림 6 이 따름) · 식 25 가운데 적분 = erf(√G/2) ≠ erf(1/(2√G)) (§3-5).
3. 식 14 *"∂C/∂t = −D∇²C + R"* — 확산 항 부호가 '−' (보통 꼴 +D∇²C) · 식 9 이동 항 '+' (양이온 보통 꼴 −zF D C ∇φ /RT · 원문은 부호 규약을 말하지 않음).
4. 본문 p.8 *"maximum Li concentration, which is 23000 mol/m3"* ↔ Table 2 23300 (Fig. 3 평탄 ≈2.33 × 10⁴ [판독]).
5. 멈춤 조건: Table 1 (계면 C_Lis = C_Li,max) ↔ p.4 (*"end at the desired cutoff voltage"*).
6. Li et al. 압력: p.2 *"228 MPa"* ↔ p.10 *"230 MPa"*.
7. p.9 *"nearly linear"* ↔ Fig. 6 의 √σ 꼴 (§3-5).
8. Table 2 가 k_d 와 k_r 에 같은 단위 mol m⁻² s⁻¹ — 식 7 이면 k_d = k_r × 농도 (단위가 같을 수 없다).
9. 식 13 ↔ 17 기호 바뀜 (C_Lis,max → C_Li,max · C_Li,all → C_Li+,0).
10. 'I 감소' (p.6 *"smaller y-intercept"* · p.9 *"the intercept, I, would be decreased"* · p.10 *"decreasing I"*) 는 크기 말 — 값은 −11.35 → −9.35 로 커진다.
11. Fig. 5 축 이름 *"Loss of Contact Area (γ)"* 인데 눈금은 γ 자체 (1 → 0.75).

---

## 4. ★ 방법 — 1-D Newman 전기화학 + 접촉 인자 + Persson 접촉역학

### 4-1. 전기화학 (식 1–15 · p.3–4 · `eq_*.png`)
- 음극 (x = 0): Li ⇌ Li⁺ + e⁻ (식 1) · Butler–Volmer i_neg = F A₀ k_neg (C_Li+/C_Li,all)^α_neg (…) (식 2) · η = φs − φep − Eeq (식 3 · 음극 Eeq = 0).
- 전해질: 평형 이동 분율 δ (식 4) · 이동 Li⁺ ⇌ 갇힌 Li₀ (식 5–7) · 순 생성 r = k_r[(C₀δ)² − C_Li+²] (식 8) · Nernst–Planck + 보존 (식 9–10) · 전기 중성 (C_Li+ = C_n−).
- 양극 (x = 1500 nm): Li₁₋ₓCoO₂ + xLi⁺ + xe⁻ ⇌ LiCoO₂ (식 11) · Butler–Volmer (식 12) · 농도 의존 i₀ (식 13 — (C_max − C_Lis)^α (C_Lis − C_min)^(1−α) 꼴) · LiCoO₂ 안 Fick 확산 (식 14) · 계면 원천 R_Lis = ν i_pos/(n_e F) (식 15 · ν = n_e = 1).
- ⚠ 시작 C_Lis = 0.5 C_max = C_min (Table 1 · 2) 이면 식 13 의 (C_Lis − C_min)^0.4 항이 0 — 원문은 이 처리를 말하지 않는다 [카드 추론] · Fig. 3a · 3b 의 첫 점은 ≈1.18 × 10⁴ mol m⁻³ [판독 · 눈으로] 로 C_min 11650 보다 조금 위.

### 4-2. 접촉 손실을 넣는 법 (식 16–18 · p.4–5 · Fig. 1b · `txt_p4_p5_…` · `txt_p5_constant_…`)
- γ = A/A₀ (식 16) · *"one can always reduce the contact to a flat surface with an effective rough surface"* (p.4).
- i₀,pos 에 γA₀ (식 17) — 반응 면적 감소 → 같은 전류에 큰 과전압.
- R_Lis 를 1/γ 배 (식 18): *"the current density at the solid-electrolyte side of the interface is not affected by the loss of contact area, but the production rate of Li on the positive electrode side of the interface would be scaled to match the same current"* (p.5) — 1-D 의 LiCoO₂ 단위 면적에 같은 전류를 1/γ 배 밀도로 넣는 셈 = **닿은 γ 몫만 쓰이고 나머지 (1 − γ) LiCoO₂ 는 못 쓴다** (최악 가정 · Fig. 1b 붉은 빗금) [카드 해석 · 원문 p.5 *"in the worst case, the loss of contact … would cause the loss of LiCoO2 material, in which Li-ion cannot be stored"*].
- 협착 (퍼짐) 저항 · 측면 확산 · 전자 경로 손실 = **넣지 않음**.

### 4-3. Persson 다척도 접촉 (식 19–26 · p.5–7)
- 거칠기 스펙트럼 C(q) (식 19) · 자기 닮음 C ∝ q^m × 10^I (Fig. 2b) · 확대율 ξ 마다 응력 분포 P(σ, ξ) (식 20) · γ = ∫ dσ P (식 21) · ξ 방향 확산 방정식 ∂P/∂ξ = f(ξ) ∂²P/∂σ² · f = (π/4)(E/(1−ν²))² q_L q³ C(q) (식 22–23) · 유효 계수 식 24.
- 초기 · 경계 (p.7): ξ = 1 에서 P(σ,1) = δ(σ − σ₀) (평평한 완전 접촉) · σ → ∞ 에서 P → 0 · **σ < 0 에서 P = 0 (점착 없음)** · *"The different properties of the contact, such as elastic contact, adhesion or elastoplastic contact can be addressed by changing the initial and boundary conditions of Equation 22. Since both Li3PO4 and LiCoO2 are ceramic materials, the contact is considered to be elastic without adhesion in this study"* (p.7).
- 닫힌 해 (식 25–26): γ = erf(1/(2√G)) · G = (π/4)(E/((1−ν²)σ₀)) ∫_{q_L}^{ξq_L} dq q³C(q) (인쇄 · §3-5 의 제곱 문제).
- 맞춘 값 0 개 — C(q) (다른 시료 AFM) · E · ν (문헌) · ξ (확산 길이 논리) · 사이클 (m, I) 걸음 (손으로).

### 4-4. 수치 · 비용 · 검증
- *"it was solved by finite element analysis"* (p.10) — 프로그램 · 요소 수 · 시간 간격 · 수렴 · 계산 시간 [미확인] (원문에 'COMSOL' 0 회).
- 검증: γ = 1 에서 *"This result is similar to other models with perfect contact area.27,30"* (p.8 · 정성) · 접촉 계산은 Li et al. [26] 정성 대조 (§3-6) · 해석해 · 격자 수렴 · 민감도 분석 없음.

### 4-5. 이 묶음의 네 질문 (i)–(iv)
- (i) **DEM 한계** — DEM 을 쓰지 않는다 (말 없음).  가까운 문장 (거친 면 미세돌기 모델의 한계): *"The well-known Hertz, Greenwood-Williamson, and Bush models are not appropriate for large contact area (>50%) because they neglect the interaction between contacted asperities"* (p.3) · *"a perfect contacted interface at macroscopic view may not be 100% in contact at the nanometer scale"* (p.3).  ⚠ 입자 DEM 의 점접촉 · 접촉 독립 가정과 **같은 논리** 지만 대상이 다르다 (한 계면의 미세돌기) [카드 해석].
- (ii) **소성 · 큰 변형이 어려운 이유와 우회** — 원문은 '어렵다' 고 하지 않는다: Li 금속 쪽 소성은 *"it is more likely to maintain a good contact … due to plastic deformation"* (p.2–3) 이라 **계산에서 뺐고**, 세라믹 계면은 탄성 · 무점착으로 두었다 (elastoplastic 은 경계 조건으로 가능하다고만 · p.7).  우회 = 연속체 1-D + 통계적 접촉 이론 (반해석 · 비용 언급 없음).
- (iii) **2D / 3D** — 전기화학 1-D · Persson 은 반무한 3D 탄성체의 2D 등방 거친 면 (*"assuming isotropic in x-y direction"*, p.5).  원문: *"The linear relationship may be due to the simplified 1D model and the assumption of worst scenario … more sophisticated 2D and 3D models that can describe the local concentration change and the amount of accessible cathode material more accurately are being developed for further study"* (p.9) · *"For future work, 2-D or 3-D continuum models need to be developed to capture the 2-D and 3-D diffusion of Li in the positive electrode after losing contact"* (p.10).
- (iv) **압력을 뺄 때** — **다루지 않는다** · 사이클 = (m, I) 변경.

---

## 5. Figure set ★

| 그림 | 무엇을 보이나 | 우리가 쓸 것 |
|---|---|---|
| Fig. 1 (`Fig. 1a` · `Fig. 1b`) | 1-D 모델 · 계면 확대 (닿은 A ⊂ A₀ · 붉은 빗금 = 못 쓰는 LiCoO₂) | '접촉 손실 = 물질 손실 (최악)' 가정을 한 장으로 설명할 때 |
| Fig. 2 (`Fig. 2a` · `Fig. 2b`) | 압분 ↔ 박막 계면 · 확대할수록 접촉이 줄어드는 그림 · C(q) 두 직선 | 척도 의존 접촉 개념도 · ⚠ 2b 표지 −8.11 · 점선 기울기 어긋남 |
| Fig. 3 (`Fig. 3a` · `Fig. 3b` · `Fig. 3c`) | γ ↓ · 율 ↑ → 계면 Li 농도가 일찍 포화 · LiCoO₂ OCV | 기전 (전류 집중 → 표면 포화) 의 예 |
| Fig. 4 (`Fig. 4a` · `Fig. 4b` · `Fig. 4c`) | 방전 곡선 (γ = 1 율별 · 1 C · 10 C 의 γ 별) · 80 % 임계선 | γ ↔ 용량 · 전압 하강의 정량 (§3-4) |
| Fig. 5 (`Fig. 5a` · `Fig. 5b`) | 남은 용량 vs γ (3.8 · 4.0 V) | 기울기 ≈1 (깊은 차단) · 기준 함정 (§3-4) |
| Fig. 6 (`Fig. 6a` · `Fig. 6b`) | γ(σ) (박막 0–200 · 압분 0–500 MPa) · A → B → C | 재가압 처방의 방향 · ⚠ 인쇄 식 26 꼴 (§3-5) |
| Table 1–3 (= 원문 Table I–III) | 조건 · 매개변수 · 탄성 | 입력 출처 추적 |

---

## 6. Post-processing ★

- 용량 = Q_out = t × C_rate / A₀ (식 27) · 차단 전압 3.7 (Fig. 4) · 3.8 · 4.0 V (Fig. 5) · 100 % = 0.1 C 용량 (p.8) · 임계 = 최대의 80 %.
- 기울기 = 남은 용량 % vs γ 직선 (원문 값 −0.34 · −0.26 · 방법 [미확인] — 판독 끝점 기울기와 같다).
- 접촉 비율 = 식 25 (관찰 척도 3.6 µm 에서) · 회복 압력 = 같은 γ 를 주는 σ 를 다른 (m, I) 곡선에서 읽기.
- 이 카드의 판독 (`digitized.csv`): 그림 2b = 색 화소 열별 중앙값 → 최소제곱 직선 · 그림 4 = 3.7 V 축 바로 위 끝 화소 · 그림 5 = γ 눈금 열 ±6 px 안 표식 중앙 · 그림 6 = 색 화소 열별 중앙 → erf(c√σ) 맞춤 · A/B/C = 채움 화소 중심 · 독립 재확인 = 그림 2b 축 눈금 (46.75 px/단위) · 직선 맞춤 차이 ≤ 0.007 · 그림 6a 눈금 (0.8 · 1.0 · 50 · 150 MPa) · 검은 곡선 20/100 MPa · 6b 50/300 MPa 차이 ≤ 0.007.
- 검산 스크립트 (카드 산술 전부): E* · J = 10^I (ξq_L^(4+m) − q_L^(4+m))/(4+m) · 두 꼴의 γ · c 비 · 회복 배수 · RMS · 상대 손실 — 값은 §3-5 · §3-6 · §3-4.

---

## 7. 우리 DEM+MPM 대비 (우리 값 = CLAUDE.md 출처 · `comparison_vs_ours_DEM.md` B 절 2026-11-17 줄)

| 축 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 접촉 손실 → 전기화학 | i₀ ∝ γ (반응 면적) + 물질 손실 ∝ (1 − γ) (최악) · 1-D | A10 사이클 접촉 원장 (`scripts/cycle_contact_ledger.py` · CLAUDE.md 07-22 절): 접촉 개구 → f_broken · A_rel · 반응면 R_ct 몫 · σ_rel · Γ* | 반응 면적 꼴은 **같은 자리** (R_ct ∝ 1/면적) [카드 해석] · '닿지 않은 물질 → 용량' 갈래는 그 원장 출력 목록에 없다 [카드 해석 · CLAUDE.md 07-22 절 기준] — 원문도 이 갈래를 최악 가정이라 부른다 |
| 계면 협착 | 없음 (전해질 쪽 전류 밀도 불변) | 접촉망 Holm R = 1/(2σa) (접촉마다) · STEP3 복셀 = 협착 항 0 (CONTACT_FREE · CL-81) | **다르다** — 이 논문의 γ 벌점은 반응 · 물질 쪽이고, 우리 수송 벌점 (협착) 은 없다.  `greenwood1966_…` 의 '군집 겉보기 면적이 협착을 정한다' 는 원문의 관찰 척도 자르기 (3.6 µm 아래 무늬 = 고르게 퍼짐) 와 같은 방향의 생각 [카드 해석 · 원문은 Greenwood 1966 협착 논문을 인용하지 않음] |
| 접촉 비율의 정의 | 평평한 계면의 실접촉 비율 · 관찰 척도 3.6 µm | 피복률 (AM 표면 중 SE 가 간격 띠 안에 있는 몫) — real_14 기하 검산 (CLAUDE.md 06-17 절): 간격 ≤ 0 이면 16 % (≈ DEM Hertz 18) · 0.14 µm (1 복셀) 안이면 49 % (≈ Tabor 52) | 정의 · 척도가 다르다 (3.6 / 0.14 ≈ 26 배 [카드 산술]) → **숫자 비교 안 함** |
| 압력 → 접촉 | Persson 탄성 · 무점착 · 다척도 평균장 | DEM: 매끈한 구 겹침 면적 (Hertz · Stage-E Tabor · 부피 상한) · MPM: 소성 SE 형상 → 피복 | 우리는 입자 아래 거칠기 (다척도) 를 안 푼다 · 이 논문은 입자 · 소성을 안 푼다 → 서로의 빈칸 |
| 탄성 계수 | E* 박막 68.35 · 압분 22.67 GPa | LPSCl DFT 쌍 (E 22.06 · ν 0.360) ↔ 단단한 AM 극한 E* 25.34 GPa [카드 산술] · DEM 연화 1.35 (ν 0.3) → E* 1.48 GPa | 압분 LGPS–TiS₂ 의 E* 가 LPSCl 계와 같은 자릿수 · 그러나 C(q) · 식 꼴 문제로 전이 안 함 (아래 줄) |
| 예시 산술 (같은 양 아님) | 압분 C(q) · 300 MPa | LPSCl 극한 E* 25.34: 인쇄 꼴 γ 0.978 · 제곱 꼴 **0.197** / DEM 연화 E* 1.48: 둘 다 ≈1.000 [카드 산술] | 18 배 연화 계수를 탄성 접촉 이론에 넣으면 실접촉이 포화한다 — 연화가 '빈틈을 메우는 유동' 의 대리라는 frame [2] 와 같은 방향의 산술일 뿐 · 원문과 무관 |
| 탈압 · 재가압 | 없음 (탄성이라 가역 · 이력 없음) | [DEM 우선 Ⓐ] 언로딩 키트 (ULR1 · G2c′ 진행 중) | 이 논문은 '재가압이 접촉을 되돌린다' 를 **탄성 가역** 으로만 말한다 — 소성 SE 의 이력 (같은 압력에서 다른 접촉) 은 원문 밖 |
| 순수 SE 기공 · 랩 표준 (10–13 % · 1.64 g/cm³) | 없음 | — | 나란히 놓을 숫자 없음 |

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나

| 계획 이름 | 이 논문이 주는 것 | 못 주는 것 |
|---|---|---|
| 단계 0 (관측량 · 판정 기준) | '접촉 비율은 관찰 척도와 함께 정의한다' — 원문은 척도를 물리 (1 C Li 확산 길이 √(4Dt) = 3.6 µm) 로 고정 · 우리 피복 · 접촉 면적 보고에 척도 (띠 두께 · 복셀) 를 같이 적는 규칙의 근거 문장 (p.5) | 기공 연산자 · 판정 숫자 |
| 단계 1–4 | 없음 (입자 · MPM · 순수 SE 압밀 없음) | 전부 |
| 단계 5 (복합 압축) | 없음 | 복합 기공 · 하중 몫 |
| 단계 6 (탈압 · 되돌아옴) | 탈압 계산 결과 (AM–SE 접촉 손실) 를 **전기화학 벌점으로 바꾸는 뒷단 꼴**: 깊은 차단 = 용량 손실 ≈ 접촉 손실 (1 : 1 · 최악) · 얕은 차단 · 고율 = 같은 율 기준 1.0–1.45 배 [카드 산술 §3-4] · 반응 면적 i₀ ∝ γ | 탈압 자체 · 이력 · 잔류 접촉 · 시간 이완 |
| 단계 7 (형상 · 피복 · 수송) | 반응 면적 ↔ 물질 접근 두 갈래 회계 · 피복 → 용량 · 과전압의 1-D 해석 틀 | 협착 · 퍼짐 · 측면 확산 (원문이 2-D/3-D 를 숙제로 남김) |
| 후보 D0 (지금 DEM) | 매끈한 구의 겹침 면적은 미세돌기 (다척도) 접촉을 담지 않는다는 반대편 근거 · 큰 접촉 비율 (> 50 %) 에서 미세돌기 독립 가정이 깨진다는 문장 (p.3) | DEM 자체의 한계 문장 |
| 후보 A′-0 · A · A′ (MPM 접촉 규칙) | 무점착 = 인장 견인 없음 (P(σ < 0) = 0) 이라는 분리 조건의 연속체 꼴 | 미끄럼 · 마찰 · 다물체 |
| 후보 B · C · C′ | 없음 (Persson 은 접촉 법칙 대안이 아니라 한 계면의 통계 이론) | — |
| 후보 M0 (균질화) | 계면 한 장의 '압력 → 실접촉' 하위 격자 법칙 꼴 (erf · C(q)) — 쓰려면 식 꼴 (제곱) 을 먼저 재현 | 압밀 · 기공 |
| U0–U6 | U3 (분리 · 잔류 압흔 · 되돌아옴) 에 쓸 것 없음 (탄성 · 압흔 없음) | 전부 |
| R1 · R3 · R6 · R7 | 없음 (AM 하중 · 입자 경계 · 형상 · 파괴 0 · 파괴는 서론 정성) | — |
| R2 (미끄럼 · 분리) | 분리 (무점착) 만 | 미끄럼 |
| R4 (탈압 · 되돌아옴) | 없음 — '재가압 = 더 높은 압력이면 회복' (탄성 가역) 방향만 | 이력 |
| R5 (맞추는 값은 모델마다 하나) | 전기화학 = Danilov 가 박막 실험에 맞춘 **여러 값** (Table 2) 을 빌림 · 접촉 = 맞춘 값 0 (그러나 C(q) · ξ · (m, I) 걸음은 손 선택) — '맞춘 값 0 인데 실측 대조도 정성뿐' 인 꼴은 피할 본보기 | — |
| 결과 전 대조 항목 | (가) Li et al. 2016 (In-Li / LGPS / TiS₂) 의 19 ↔ 228/230 MPa 유지율 차이 (원전 카드 없음 · n 후보) (나) 깊은 차단 용량 ∝ 접근 가능 물질 이라는 1 : 1 꼴 | 우리 재료 (LPSCl · NCM) 값 |
| 랩 기준 (순수 SE 10–13 % · LPSCl 1.64 g/cm³) | 나란히 놓을 값 없음 | — |
| 우리 DEM (E_eff 1.35 · 18 배 연화 · Heckel P_y 138 MPa) | 연화 E* 1.48 GPa 를 Persson 에 넣으면 300 MPa 실접촉 ≈1.0 (두 꼴 모두) [카드 산술 · 같은 양 아님] | Heckel · 압밀 |
| 우리 MPM (E 1.53 · σ_y 0.30 · ν 0.49) | 없음 — 탄성 · 무점착 계면 이론은 소성 SE 형상 흐름과 다른 기전 | — |
| [DEM 우선 Ⓐ] 언로딩 · 접촉 손실 | ★ 쓸 수 있는 것은 **'접촉 손실 → 성능' 꼴** (§3-4) 과 **두 갈래 회계** · 쓸 수 없는 것은 **압력 숫자** (§3-5 식 꼴 · 다른 재료 · 탄성) | — |
| [DEM 우선 (수영)] 한 모델 가압 → 탈압 | 없음 (1-D + 반해석 두 조각을 '절차' 로 이은 예 — 한 모델 아님) | — |

★ **가장 큰 함정 셋** (우리 쪽에서 이 논문을 인용할 때):
1. **압력 숫자를 Persson 이론값으로 인용하지 않는다** — 그림 6 은 인쇄 식 26 (1 제곱) 꼴이고, 원 꼴 (제곱) 이면 같은 입력에서 20 MPa 실접촉 ≈1.4 % · 70 % 에 ≈1150 MPa [카드 산술 §3-5].  인용은 '거칠어지면 같은 압력에서 접촉이 줄고, 되찾으려면 더 높은 압력이 필요하다 (이 논문 계산에서 ≈2.6–3 배)' 까지.
2. **'re-tightening is not sufficient' 를 이 논문의 결론으로 인용하지 않는다** — 원문 결론은 반대 방향 (더 높은 압력으로 회복) · 그 문장은 Koerver 2018 의 해석 (§0-1).
3. **'용량 손실 ∝ 접촉 손실 (기울기 1)' 을 발견으로 인용하지 않는다** — 최악 가정에서 나온 값 (원문 스스로 p.8 · p.10) · 깊은 차단에서만.

---

## 9. 적용 인사이트 (내 연구에 어떻게)

1. **접촉 손실을 두 장부로** — 반응 면적 (R_ct ∝ 1/A) 과 접근 가능 물질 (용량 ∝ A · 최악) 을 따로 적고, 깊은 차단 · 얕은 차단 · 율별로 무엇이 지배하는지 가른다 (원문: 3.8 V = 물질 · 4.0 V = 표면 농도 · 확산) → 우리 A10 사이클 원장의 '접촉-기계 몫 vs 화학 몫' 분해에 그대로 붙는 꼴.
2. **기준을 밝힌다** — 같은 결과가 '0.1 C 깊은 용량 기준' 이면 기울기 0.27–0.34, '같은 율 γ = 1 기준' 이면 상대 손실이 접촉 손실의 1.0–1.45 배 [카드 산술] — 보고 · 덱에서 분모를 적는다.
3. **문헌의 '압력 → 접촉' 법칙을 쓰기 전에 한 곡선을 인쇄 식으로 재현한다** — 이 논문은 식 23 과 26 이 서로 다르고 그림이 26 을 따른다 (재현 비 0.95–0.99) · 재현 안 하면 50 배 다른 접촉을 '이론값' 으로 들고 온다.
4. **관찰 척도를 물리로 자르는 법** — 반응 · 확산이 고르게 퍼지는 길이 (√(4Dt)) 보다 작은 무늬는 접촉 비율에 넣지 않는다 (원문 ξ ≈2700) — 우리 피복 띠 · 복셀 크기 선택의 정당화 문장으로 (재료 값은 옮기지 않음).

---

## 10. 인용 가능 문장 (deck/paper 용 · 영문 초안 · 표지 그대로)

- "Tian and Qi (2017) incorporated a contact factor γ = A/A0 into a 1-D Newman model of a film-type Li|LiPON|LiCoO2 cell and found that, at a low cutoff voltage, the capacity loss follows the contact-area loss with a slope of about 1 — a consequence of their worst-case assumption that non-contacted LiCoO2 is inaccessible." [인쇄 p.2 · p.8]
- "Using Persson's multi-scale contact theory for an elastic, non-adhesive interface, they estimated that a roughened film-type interface needs roughly three times the stack pressure (20 → 60 MPa) to regain about 70 % contact." [인쇄 p.10] — 한정: 탄성 · 박막 · 인쇄 식 26 꼴 (§3-5).
- "Koerver et al. (2018) cite this work as showing that re-tightening a cell is insufficient; the original instead concludes that a sufficiently higher pressure would recover the contact area, while capacity recovery is inferred rather than simulated." [카드 해석 · §0-1]
- "They noted that Hertz, Greenwood–Williamson and Bush models are not appropriate for contact ratios above 50 % because they neglect the interaction between contacting asperities." [인쇄 p.3]

---

## 11. 주의/한계 (over-claim 방지 · 원문 비판)

1. **최악 가정이 결과를 만든다** — 기울기 1 (3.8 V) 은 가정의 직접 결과 (원문 p.8 · p.10 이 인정).  측면 확산이 있으면 손실은 작아진다 (원문의 2-D/3-D 숙제).
2. **식 꼴** — 식 23 (제곱) ↔ 식 26 (1 제곱) · 그림 6 은 26 · 낮은 압력 '거의 선형' 서술과 곡선 꼴이 맞지 않음 · 식 25 적분 위 끝 오기 (§3-5).  압력 숫자는 이 식 꼴에 묶여 있다.
3. **C(q) 는 다른 시료 (Flys 2015) 의 것** · 사이클 거칠어짐은 손으로 바꾼 (m, I) · RMS 정규화 미확인 (§3-5).
4. **두 계산은 결합되지 않았다** — 그림 4–5 의 γ (1 → 0.75) ↔ 그림 6 의 A · B (0.70 · 0.49) · γ ≥ 0.99 는 그림 6a 에서 ≈130 MPa 위 (§3-6).
5. **실험 대조는 정성** — Li et al. 의 유지율 좋음 / 나쁨 ↔ 계산 접촉 40 / 95 % · 접촉 면적 실측 0 · Li et al. 재료 (LGPS / TiS₂) 와 전기화학 모델 (LiCoO₂ 박막) 이 다르다 (*"general for other all-solid-state batteries"* 라는 기대 문장으로 이음).
6. **박막 전기화학 매개변수는 빌림** (Danilov 2011) · 온도 · 프로그램 · 격자 · 수렴 [미확인].
7. **전자 · 협착 · 소성 · 박리 · 탈압 없음** — 서론은 *"fracture and disconnection will impede Li-ion transport, as well as electron transport"* (p.2) 라 하지만 모델은 반응 면적 · 물질만.
8. **인쇄 어긋남 11 건** (§3-7).
9. 액체 전해질에서 온 식 (원문 한계 문단 p.10): 결함 수송 · 분극 · Butler–Volmer 의 전고체 적용성.

---

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 번호 | 서지 (원문 목록 그대로) | 왜 | litdb |
|---|---|---|---|
| 26 | W. J. Li, M. Hirayama, K. Suzuki, and R. Kanno, Mater. Trans., 57(4), 549 (2016). | 유일한 실험 앵커 — 제조 · 운전 압력 19 ↔ 228 MPa 의 사이클 유지율 (In-Li / TiS₂ / LGPS) · 우리 결과 전 대조 (b · R4) | 카드 없음 |
| 49 | B. N. J. Persson, Surf. Sci. Rep., 61(4), 201 (2006). | 식 25–26 의 원 꼴 (제곱 여부) 확인 · 탄소성 · 점착 경계 조건 (p.7 문장의 근거) | 카드 없음 |
| 62 | B. N. Persson, The Journal of Chemical Physics, 115(8), 3840 (2001). | 식 22 (확산 방정식) 의 원전 | 카드 없음 |
| 43 | J. Greenwood and J. Williamson, in "Proceedings of the Royal Society of London A: Mathematical, Physical and Engineering Sciences", Vol. 295, p. 300. The Royal Society, 1966. | '큰 접촉 (> 50 %) 에서 미세돌기 독립 가정이 깨진다' 의 대상 모델 (질문 e · k) — 정본 `greenwood1966_…` 은 다른 논문 (Br. J. Appl. Phys. 17) | 카드 없음 |
| 47 | O. Flys, S. Kallberg, G. Ged, Z. Silvestri, and B. G. Rosen, Surf. Topogr.-Metrol. Prop., 3(4), 10 (2015). | C(q) (RMS 15 · 120 nm) 의 원전 — 정규화 · RMS 범위 확인 (§3-5) | 카드 없음 |
| 15 | D. Danilov, R. A. H. Niessen, and P. H. L. Notten, J. Electrochem. Soc., 158(3), A215 (2011). | Table 2 매개변수 전부의 출처 (맞춘 실험) | 카드 없음 |
| 44 | A. Bush, R. Gibson, and T. Thomas, Wear, 35(1), 87 (1975). | 같은 '> 50 %' 문장의 Bush 모델 | 카드 없음 |
| 12 | D. Santhanagopalan, D. Qian, T. McGilvray, Z. Y. Wang, F. Wang, F. Camino, J. Graetz, N. Dudney, and Y. S. Meng, J. Phys. Chem. Lett., 5(2), 298 (2014). | operando 원소 지도의 LiCoO₂ Li 불균일 (*"may be partially caused by imperfect contact"*) · `tian2020_…` ref 57 과 같은 논문 | 카드 없음 |
| 67 | Z. Deng, Z. B. Wang, I. H. Chu, J. Luo, and S. P. Ong, J. Electrochem. Soc., 163(2), A67 (2016). | LGPS E 21.7 · ν 0.37 | `deng2016_elastic_superionic_electrolytes_dft` |
| 34 | G. Bucci, S. P. Nadimpalli, V. A. Sethuraman, A. F. Bower, and P. R. Guduru, Journal of the Mechanics and Physics of Solids, 62, 276 (2014). | 사이클 기계 반응 (서론) — 정본 `bucci2017_…` 은 다른 논문 | 카드 없음 |
| 30 | A. A. Talin, D. Ruzmetov, A. Kolmakov, K. McKelvey, N. Ware, F. El Gabaly, B. Dunn, and H. S. White, ACS Appl. Mater. Interfaces, 8(47), 32385 (2016). | φs 균일 가정 · 3D 마이크로전지 · `tian2020_…` ref 28 과 같은 논문 | 카드 없음 |
| 37 · 68 · 69 · 36 | (원문 목록 그대로) M. Qu, W. H. Woodford, J. M. Maloney, W. C. Carter, Y. M. Chiang, and K. J. Van Vliet, Adv. Energy Mater., 2(8), 940 (2012) · T. Lorenz, D. Teich, J. O. Joswig, and G. Seifert, J. Phys. Chem. C, 116(21), 11714 (2012) · X. R. Xiao, W. Wu, and X. S. Huang, J. Power Sources, 195(22), 7649 (2010) · Y. H. Yang, Q. Wu, Y. H. Cui, Y. C. Chen, S. Q. Shi, R. Z. Wang, and H. Yan, ACS Appl. Mater. Interfaces, 8(38), 25229 (2016) | Table 3 탄성 출처 (LiCoO₂ E · TiS₂ · LiCoO₂ ν · Li₃PO₄) | 카드 없음 |

---

## [미확인] 목록

- 계산 프로그램 · 요소 · 격자 · 시간 간격 · 수렴 · 계산 시간 (*"finite element analysis"* 한 마디).
- 온도 T 값 · 4.0 V 기울기를 낸 방법 (직선 맞춤인지 끝점인지).
- C(q) 정규화 (2D/1D · 2π 인자) 와 Flys RMS 의 잰 범위 · 그려지지 않은 log q 2.8–4.5 의 C(q) 처리.
- 식 13 의 시작점 (C_Lis = C_min) 처리 · 멈춤 조건 둘 중 무엇이 쓰였는지.
- ref 36 (Yang 2016) 이 Li₃PO₄ E · ν 를 담는지 (서론에서는 Li 금속 크리프 근거).
- Li et al. [26] 의 접촉 면적 실측 여부 (원문은 유지율만 말함).
- 압분 (LGPS–TiS₂) 계산의 관찰 척도 · ξ (박막과 같은 2700 인지).

---

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-17)

- 본문 10 쪽 (PDF p.2–11) 을 PyMuPDF 텍스트 층으로 전부 읽고, 그림 · 표 · 식 · 근거 문단은 크롭 렌더로 확인.  PDF p.1 (IOP 표지 · 다운로드 기록 · 관련 목록) 은 논문이 아니다 — 서지는 p.2 머리글 · 초록 상자에서.
- 크롭 **67 장** 전부 열어 봄 (그림 6 통째 · 패널 14 · 표 3 · 식 24 · 근거 문단 20 — 라벨 붙인 점검 판으로).  다시 자름 = 이 회차 **2** (`txt_p9_p10_…` = 문장 중간 'case was modeled.' 로 시작하던 것을 p.9 왼쪽 단 소제목부터 세 조각으로 · `txt_p2_abstract_box_doi_dates.png` = 이름에 있는 날짜 줄이 빠져 있던 것을 포함) · 앞 회차 다시 자름 = 그림 6 장 (원 래스터 · 고른 여백) + 초록 1 (양옆 잘림).
- 판독 독립 재확인: 그림 2b 축 눈금 (y 46.75 px/단위 · x log q 7 = 787 px) 과 두 직선 맞춤 (m −3.076 · I −8.619 / m −2.633 · I −11.938 — 앞 회차 −3.077 · −8.612 / −2.634 · −11.931) · 그림 6a 눈금 (A/A₀ 0.8 · 1.0 · σ 50 · 150 MPa) · 검은 곡선 20 · 100 MPa (6a) · 50 · 300 MPa (6b) 점 판독 차이 ≤ 0.007 · 그림 5 끝점 기울기 0.339 · 0.266 ↔ 인쇄 −0.34 · −0.26.
- Persson 재현: 인쇄 식 26 으로 열 곡선의 c 를 0.95–0.99 배로 재현 (§3-5) · 식 23 제곱 꼴이면 50 배 작은 접촉.
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 + DOI (2.0481711jes) · 'E3512' · 'contact area loss' · 'Tian' grep — 이 논문 카드 없음 (koerver2018 [30] · ohashi2020 [7] · tian2020 [24] 에 인용만).

---

## 🔗 관련 카드

- 이 논문을 인용한 정본 카드: `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` (ref 30 · re-tightening 문장) · `ohashi2020_stress_distribution_composite_electrode_sulfide_assb` (ref [7]) · `tian2020_electrochemo_mechanical_stress_assb` (ref [24] · 같은 그룹 후속).
- 이 논문이 인용한 정본 카드: ref 67 `deng2016_elastic_superionic_electrolytes_dft`.
- 접촉 · 협착 이웃: `greenwood1966_constriction_resistance_microcontact_cluster_real_area` (다른 Greenwood 1966 · 군집 협착) · `bucci2017_chemomech_failure_assb_cycling_czm` (사이클 박리).

---

## 🗨️ Q&A 로그

(아직 없음)
