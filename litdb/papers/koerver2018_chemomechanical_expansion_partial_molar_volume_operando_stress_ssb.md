<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 1저자 11-12 후보 표 N-9) 에서 꼭 뽑으라고 한 항목 (탈압 이완 · 되돌아옴 · 접촉 손실 · 재료별 ΔV · 스택압 측정 · 기계적 최적화 · 모델 · 저자 한계).
     본 = sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps.md (같은 묶음 · §0-1 고른 의도 대조 · §8 자세한 분석 꼴) · 곁 = benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem.md (이 논문의 ΔV 를 FEM 고유변형에 쓴 카드).
     원문 = 출판본 (Energy Environ. Sci. 2018, 11, 2142–2158 · 17 쪽 · Paper · RSC "Licence and permissions" 표지 — CC 표지 없음) + ESI (10 쪽 PDF = 표지 + 그림 S1–S8 · 표 S1–S4 · 식 S1–S11 · ESI 참고문헌 3).
     쪽 표기 = 본문 "p.NNNN" = 인쇄 쪽 (PDF 쪽 = 인쇄 − 2141 · p.2142 = PDF 1 … p.2158 = PDF 17) · ESI "S n" = ESI 인쇄 쪽 = ESI PDF 쪽 n.  크롭 파일 이름의 pN · figures.json 의 page 는 PDF 쪽이다.
     값 표지: [인쇄] = 본문 · ESI · 그림 안 글자로 적힌 값 · [판독] = 래스터 그림을 그 그림의 눈금으로 환산한 값 (재현 = litdb/figures/<slug>/digitized.csv 201 행 — 그림 2 · S5 는 원본 래스터 화소에서 눈금 보정 · 그림 4 · 5 · S1 · S6 은 열어 본 크롭에서 눈금 눈대중) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드에 적힌 값 (slug 병기) · [우리] = 우리 쪽 값 (CLAUDE.md · 리포 코드 출처 병기) · [미확인] = 본문 17 쪽 + ESI 10 쪽 전수에 없음.
     원문 27 쪽은 글자 층 (pdftotext raw · layout · PyMuPDF) + 렌더로 전부 읽었다.  ⚠ 글자 층이 마이너스 부호를 잃는다 — LTO "0.2%" · LFP "7%" · "659 bar" · "427 bar" · "ΔVcryst(NCM) = 6%" 는 렌더에서 각각 −0.2 % · −7 % · −659 bar · −427 bar · −6 % (부호는 렌더로 확인).
     DEM · MPM · FEM · 입자 계산 · 압밀 시뮬레이션은 없다 — 실험 (구속 셀 operando 힘 센서 · 압력별 OCV · operando XRD 모음) + 0D/1D 선형 탄성 추정 (Δp = −ε_vol K · Reuss 직렬 균질화) 뿐. -->
# 리튬 전극 재료의 화학-기계 팽창 (chemo-mechanical expansion) — 단위 격자 부피 변화 ΔV/V₀ 모음 (NCM-111 · 523 · 622 · 811 · NCA · LCO · 그림 2a — NCM-811 은 x ≈ 0.15 에서 ≈ −6.5 %) · Li 부분 몰 부피 (partial molar volume) · OCV 의 압력 의존 (In|LTO +0.122 mV/MPa → +11.81 cm³/mol) · 구속 셀 operando 축 응력 σ₁₁ (CAM/LTO ≈ ±0.6 × 10⁵ Pa · Li/NCM-811 ≈ 15 × 10⁵ Pa) · Reuss 직렬 균질화 정수압 추정 (+100 · −427 bar) · LCO + NCM-811 섞기 (55 : 45 wt) 로 응력 상쇄 — Koerver · Zhang · de Biasi · Schweidler · Kondrakov · Kolling · Brezesinski · Hartmann · Zeier · Janek (Energy Environ. Sci. 2018)

> slug `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` · DOI `10.1039/C8EE00907D` · type `experiment + linear-elastic continuum estimate (operando force-sensor stress monitoring of volume-constrained solid-state cells · pressure-dependent OCV → reaction / partial molar volume · operando XRD unit-cell volume compilation · Δp = −εvol·K + Reuss homogenisation · SEM/EDX after cycling — no DEM / MPM / FEM particle model)` · PDF `b7a27d60-9._Chemo-mechanical_expansion_of_lithium_electrode_materials_on_the_route_to_mechanically_optimized_all-solid-state_batteries.pdf` · SI `35a618f5-9._Sup_Chemo-mechanical_expansion_of_lithium_electrode_materials_on_the_route_to_mechanically_optimized_all-solid-state_batteries.pdf` · digested `2026-11-12` · status ✅
>
> **저자**: **Raimund Koerver** ᵃᵇ · Wenbo Zhang ᵃᵇ · Lea de Biasi ᶜ · Simon Schweidler ᶜ · Aleksandr O. Kondrakov ᵈ · Stefan Kolling ᵉ · Torsten Brezesinski ᶜ · Pascal Hartmann ᵈ · **Wolfgang G. Zeier\*** ᵃᵇ · **Jürgen Janek\*** ᵃᵇᶜ — ᵃ Institute of Physical Chemistry, Justus-Liebig-University Giessen · ᵇ Center for Materials Research (LaMa), JLU Giessen · ᶜ Battery and Electrochemistry Laboratory (BELLA), Institute of Nanotechnology, KIT · ᵈ BASF SE (Ludwigshafen) · ᵉ Institute of Mechanics and Materials, Technische Hochschule Mittelhessen — \* 교신 (wolfgang.g.zeier@… · juergen.janek@phys.chemie.uni-giessen.de) · *Energy Environ. Sci.* **2018**, **11**, **2142–2158** (17 쪽 · Paper) · 접수 2018-03-28 · 승인 2018-05-29 · 출판 2018-05-29 (p.2142) · 연구비 = BASF SE (International Network for Electrochemistry and Batteries) · R. K. = Funds of the Chemical Industry (FCI) · 감사 = H. Weigand (operando 압력 장치) · W. Koerver (LabVIEW) · I. Aygün (셀 제작) (p.2153–2154) · 이해 상충 없음 · 저자 기여 문단 [미확인].
> **이웃 카드 (링크만)**: 이 논문을 인용한 정본 카드 = [`jung2019_cathode_electrolyte_chemical_reaction_sulfide_assb`](jung2019_cathode_electrolyte_chemical_reaction_sulfide_assb.md) (ref 29) · [`benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem`](benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem.md) (ref 3 · NMC622 ΔV) · [`barai2021_delamination_cathode_llzo_multiscale`](barai2021_delamination_cathode_llzo_multiscale.md) (ref 36 · V̄) · [`doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density`](doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density.md) (ref 14) · [`tian2020_electrochemo_mechanical_stress_assb`](tian2020_electrochemo_mechanical_stress_assb.md) (ref 4) · [`park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics`](park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics.md) (ref 31) · [`nolan2018_computation_accelerated_design_review`](nolan2018_computation_accelerated_design_review.md) (ref 156) · 이 논문이 인용한 정본 카드 = ref 33 [`sakuda2013_sulfide_mechanical_property`](sakuda2013_sulfide_mechanical_property.md) · ref 34 [`bucci2017_chemomech_failure_assb_cycling_czm`](bucci2017_chemomech_failure_assb_cycling_czm.md) · ref 89 [`deng2016_elastic_superionic_electrolytes_dft`](deng2016_elastic_superionic_electrolytes_dft.md) · 같은 묶음 = [`sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps`](sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps.md) · [`jeong2024_operando_densification_chemomechanics_se_size_composite_cathode`](jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md).
> **판독 원자료**: `litdb/figures/koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb/digitized.csv` (201 행 — 그림 2a 표지 103 · 그림 2b 열 표본 38 · 그림 S5 힘 곡선 39 · 그림 4 · 5 · S6 · S1 눈대중 21) · 그림 크롭 **72 장** (도구 15 = 14 다시 자르거나 캡션 고침 + 1 그대로 · 손 57 = 패널 10 · 표 3 · 식 23 · 근거 문단 21 · 아래 §5) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 리튬 저장 전극 재료 (양극 NCM · NCA · LCO · LFP · 음극 Li · In · 흑연 · Si · LTO) 의 Li 함량에 따른 부피 변화를 **세 가지 방법**으로 본 논문이다 — ① operando XRD 단위 격자 부피 (자체 + 문헌 35–37 모음 · 그림 2a) 와 그것을 미분한 **Li 부분 몰 부피 V̄m(Li)** (식 1–2 · 그림 2b), ② 고체 셀 OCV 의 **압력 의존** (∂E_oc/∂p = −Δ_rV_m/nF · 식 3) 으로 잰 반응 부피 (In|LTO **+0.122 mV MPa⁻¹ → V̄′m(Li, In/InLi) ≈ +11.81 cm³ mol⁻¹** · 결정학 값 +7.89 보다 ≈ +50 % · 식 7), ③ **펠릿 셀 (지름 ≈ 10 mm [카드 산술]) 을 고정 틀에 넣고 (10 Nm 조임 ≈ 60 ± 8 MPa) 바닥 힘 센서로 잰 충방전 중 축 응력 변화 σ₁₁** (그림 4 · 5 · S5 · S6) 와 그것의 선형 탄성 추정 (Δp = −ε_vol K · 식 11 · Reuss 균질화 · 식 12 · S8–S11).
측정된 응력 변화는 작다 — LTO 상대에서 **LCO ≈ +0.6 × 10⁵ Pa (≈ 0.06 MPa) · NCM-811 ≈ −0.45 ~ −0.6 × 10⁵ Pa** [판독 그림 4a · 4b · 축 단위 "σ₁₁ / 10⁵ Pa"] · Li 금속 음극이면 ≈ 15 × 10⁵ Pa (≈ 1.5 MPa) · 흑연 ≈ 6 × 10⁵ Pa · InLi ≈ 10–13 × 10⁵ Pa [판독 그림 4c · 4d · S6b] — ⚠ 본문은 LCO 값을 *"+0.6 MPa"* (p.2149) 로 적었으나 그림 축과 ESI 표 S4 (σ₁₁ = −0.06 MPa exp.) 로는 **0.06 MPa** 다 (§3-9 ①).
저자 제안 = 부호가 반대인 두 양극 (팽창 LCO + 수축 NCM-811) 을 **55 : 45 wt** 로 섞으면 셀 응력이 거의 상쇄되고 (그림 5c · *"Δσ₁₁ ~ 0"*) 사이클 뒤 접촉도 보존된다 (그림 S7 ↔ 단일 NCM 은 수축해 SE 와 떨어짐 · 그림 S8 · Koerver 2017 재게재).
**압력을 빼는 (탈압) 실험은 없다** — 제조 35 kN (≈ 445 MPa) 뒤 운전 ≈ 70 MPa · 고정 틀 60 ± 8 MPa 로 낮췄다고만 적고 (p.2153) 그 사이의 되돌아옴 · 접촉 손실은 재지 않았다.  있는 것은 **고정 변위 틀의 응력 이완** (그림 S5 — 비우지 않은 셀 ≈ 65.2 → 62.3 MPa (0.5 → 15.5 h) · 빈 틀 ≈ 65.1 → 62.5 MPa (0.2 → 15.5 h) [판독] — 저자는 *"mechanical drift of an empty cell casing due to the plastic insulators"* 로 보고 빼 버린다) 과 정성 문장들 (§3-7) 뿐이다.
**재료가 우리와 다르다 (SE = β-Li₃PS₄ · LGPS · AM = NCM-811 · NCA · LCO) · 그림 2a 는 대부분 문헌 XRD 모음 · 응력은 축 방향 한 성분 · 모델은 0D/1D 선형 탄성 · 반복 · 오차 막대 없음 (그림 3 제외).**

| 1저자가 꼭 뽑으라 한 것 (이 묶음 N-9) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 가압을 뺄 때 (탈압 · 압력 해제) 의 이완 · 되돌아옴 · 접촉 손실 — 값 · 그림 · 측정법 (두께 · 압력 · 시간) | **탈압 실험 없음** (두께 · 되돌아옴 값 0) · 있는 것: ⓐ 고정 틀 (변위 고정) 응력 이완 그림 S5 — 셀 5.128 → 4.894 kN = 65.2 → 62.3 MPa (0.5 → 15.5 h, OCV 대기) · 빈 틀 5.119 → 4.913 kN = 65.1 → 62.5 MPa (0.2 → 15.5 h) → 4.845 kN = 61.7 MPa (62 h) [판독] · 측정법 = 바닥 힘 센서 (KMT 55) + 10 Nm 조임 (≈ 60 ± 8 MPa) + 20 h OCV 대기 + 손으로 그린 기준선 빼기 (p.2153) ⓑ 접촉 손실 = 탈리튬 중 NCM 수축으로 SE 와 떨어짐 (그림 S8 · 사이클 뒤 SEM · 정성 · Koerver 2017 재게재) ⓒ *"re-tightening a cell is not sufficient to recover capacity fade due to contact loss"* (p.2151 · Tian & Qi 2017 계산 인용) ⓓ *"plastic deformation is slow and perhaps not effective enough"* (p.2151) | [판독] 그림 S5 · [인쇄] p.2151 · p.2153 · S8 |
| ② ★ 전극 재료별 부피 변화 ΔV (NCM 조성 · 충방전 상태 · 격자 상수 · 값 · 표) | **표는 없고 그림만** (그림 2a · ΔV/V₀ vs x(Li), 탈리튬 방향) — 끝점 [판독]: NCM-111 **−2.0 %** (x ≈ 0.24) · NCM-523 **−3.3 %** (0.22) · NCM-622 **−4.8 %** (0.19) · NCA **−5.7 %** (0.17) · NCM-811 **−6.5 %** (0.15) · LCO 최대 **+2.2 %** (x ≈ 0.6) → 0 (0.46) → −1.0 % (0.43) · 인쇄값: LCO *"roughly +2%"* (→ Li₀.₅CoO₂) · 모델 입력 LCO **+1.4 %** · NCM-811 **−6 %** (*"when charging to 4.3 V vs. Li"* · de Biasi 2017 인용) · LTO **−0.2 %** · LFP **≈ −7 %** · 흑연 **≈ 13 %** (완전 리튬화) · Si **≤ 400 %** · 격자 상수 a · c 값 [미확인] (그림 1a 의 개념만) · 데이터 출처 = *"LCO in this work, others see ref. 35–37"* | [판독] 그림 2a · [인쇄] p.2144–2146 · S5 · 표 S3 |
| ③ ★ 스택압 · 셀 압력 측정 (장치 · 압력 변화 곡선) | 장치 = 바깥 Al 틀 + 안쪽 Al 틀 + PEEK 절연 둘 + 강 피스톤 + **바닥 힘 센서** · 위 나사로 초기 압력 (그림 S2) · 10 Nm ≈ 60 ± 8 MPa · 25 °C · 곡선 = 그림 4 (σ₁₁ vs 시간 · x(Li)) · 그림 S5 (보정 전 힘 4.75–5.15 kN ≈ 60.5–65.5 MPa) · 그림 S6 · 그림 5 | [인쇄] p.2149 · p.2153 · S2 · [판독] |
| ④ ★ 복합 양극 / 음극의 팽창 · 수축 · 기계적 최적화 제안 | NCM · NCA 수축 (충전) ↔ LCO · Li · 흑연 · In 팽창 (충전 때 음극 리튬화) · LTO "영 변형" · 제안 = **섞기** (전지 전체: NCM + 흑연 · 전극 안: LCO + NCM) · **최소 기공** (*"Good SSBs may require a minimum porosity"*) · 입경 · 나노 입자 · 유연 성분 / 고분자 바인더 · 영 변형 양극 탐색 (p.2151) | [인쇄] p.2151 · 그림 5 |
| ⑤ ★ 모델 (있으면) | 0D/1D 선형 탄성: ⓐ 모든 면 구속 단일 재료 (β-Li₃PS₄) → Δp = −ε_vol K (식 11 · S1–S7) → **+144 bar (LCO/LTO) · −659 bar (NCM/LTO)** ⓑ 위만 열린 원통 (지름 1 cm · 높이 500 µm · 양극층 50 µm · CAM : SE = 1 : 1 vol) 을 Reuss 직렬 스프링으로 균질화 (E_cathode 50.4 · E_cell 30.2 · K_cell 21.8 GPa · ν 0.27) + 측정 σ₁₁ 입력 → **p_R = +9.98 MPa (LCO) · −42.66 MPa (NCM-811)** (식 12 · S8–S11 · 표 S4) · 소성 · 이방성 · 불균일 응력 무시 | [인쇄] p.2149 · p.2151 · S4–S7 |
| ⑥ ★ 저자 한계 | *"The formal treatment is restricted to a relatively simple macroscopic picture, as any more detailed treatment will require numerical methods"* (p.2143) · 이방성 · 불균일 응력장 무시 (p.2143) · 압력이 균일이 아니라 일축 · CAM 방향 무작위 아님 · LGPS 산화 (p.2147) · 소성 무시 (p.2149 · p.2152) · 완전 구속 아님 (p.2151) · 응력 응답은 SE · 전극 조합 · 미세구조 · 공정마다 고유 (p.2152) | [인쇄] |
| ⑦ 우리 쪽 — 단계 6 · 사이클 원장 `--dv-pct` · `--cycle-dv-*` 기본값과 나란히 | §7-2 표 — 우리 `--dv-pct` 5.1 (NMC811 3.0–4.3 V · Kondrakov 2017 이라는 help 글) · `--cycle-dv-sc` −0.051 · `--cycle-dv-poly` +0.059 × 0.30 ↔ 이 논문 NCM-811: SI −6 % (4.3 V) [인쇄] · 그림 2a −6.5 % (x ≈ 0.15) · ≈ −3.9 % (x ≈ 0.25) · ≈ −1.4 % (x ≈ 0.46) [판독] · 이 논문 ASSB 셀 (그림 4b) 이 실제로 간 창 x 0.85 → ≈ 0.53 [판독] — **판정 없이 나란히** | [우리] · [인쇄] · [판독] |
| ⑧ DEM · 소성 · 2D/3D · 탈압 (이 묶음 네 질문) | DEM **말 없음** · 소성은 "무시했다 · 앞으로 고려해야" 문장들 (§4-3) · 실험 = 3D 펠릿 셀 · 모델 = *"simplified (cylindrical) 3D model"* 을 1D 직렬 스프링으로 균질화 · 탈압 실험 없음 | [인쇄] |

⛔ **한정어 (떼지 말 것)**: ① **재료가 우리 계가 아니다** — SE = **β-Li₃PS₄** (응력 셀) · **LGPS** (OCV 셀) · AM = **NCM-811 · NCA-801505 · LCO (LiNb₀.₅Ta₀.₅O₃ 코팅)** — LPSCl 은 표 1 의 문헌 탄성 상수 한 줄뿐 ② 그림 2a 의 NCM · NCA 곡선은 **문헌 모음** (refs 35–37 · 파우치 셀 operando XRD · 0.1C · 25 °C) — 이 논문 ASSB 셀이 간 x 창과 다르다 ③ 응력 = **고정 변위 틀 안의 축 성분 σ₁₁ 하나** (옆 성분은 계산) · 보정 = 손으로 그린 기준선 · Savitzky–Golay 평활 ④ "실험과 모델 일치" (p.2151) 는 **측정 σ₁₁ 을 입력으로 넣은 Reuss 추정 ↔ 선형 변형 추정** 사이의 비교다 (옆 응력 · 정수압은 재지 않았다 [카드 해석]) ⑤ 압력 단위가 섞여 있다 — 힘을 MPa 로 (*"a force of 60 ± 8 MPa"*) · 10⁵ Pa (= bar) 축 · 본문 *"+0.6 MPa"* ⑥ 반복 셀 · 오차 [미확인] (그림 3 의 OCV 기울기 오차 막대만).
⇒ **절대값 전이: 0 건** (LPSCl · NCM811 계 압밀 · 탈압 값으로 쓸 숫자 없음).  전이되는 것은 **방향 · 크기 자릿수 · 측정 꼴** — (i) 충전 때 NCM 수축 · LCO 팽창 (부호) (ii) 고정 틀에서 CAM 만의 부피 변화가 만드는 축 응력은 스택압의 **≈ 0.1 %** 자릿수 [카드 산술 0.06 / 60] (iii) Li 금속 · 흑연 음극은 그 10–30 배 (iv) 고정 변위 틀 응력은 틀 (PEEK) 이완만으로도 15 h 에 ≈ 4–5 % 준다 [판독 · 카드 산술] — 탈압 · 유지 실험을 설계할 때 **틀 몫을 빈 틀로 따로 재는 꼴**.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-9 의 '왜' 칸)

의도 원문: *"b · j (단계 6) — jung2019 가 무가압 in situ SEM 을 한 동기 = '가압 해제 이완 [29] 을 배제' → 탈압 이완 · 접촉 손실 근거 후보 (jung2019 L280 · L440) · 'FEM 고유변형의 NMC622 ΔV 출처 (우리 --cycle-dv-* 기본값과 대조할 원전)' (benhadjali2026)"* (가리킨 카드 = `jung2019_cathode_electrolyte_chemical_reaction_sulfide_assb` L280 · L440 · `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` L430)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "b" (압력을 뺄 때 되돌아오는 양과 잰 방법) | **없음** (되돌아옴 값 · 두께 0 건) | 원문에 **탈압 (압력 해제) 측정이 없다**.  탈압 사건은 있다: 제조 35 kN (≈ 445 MPa) → 운전 ≈ 70 MPa (p.2153) · OCV 시험에서 2.8 t 까지 올렸다가 다음 충전 때 0.5 t 로 되돌림 (*"The pressure was set to 0.5t during charge"* · p.2153 [카드 해석]) — 그러나 그 사이 두께 · 접촉 · OCV 되돌아옴은 보고하지 않았다 |
| "j" (논문이 스스로 적은 한계 중 가압 · 탈압과 닿는 것) | **채움** | 소성 무시 (p.2149 *"(and plasticity; here ignored in the estimates)"* · p.2152 *"plasticity … neglected"*) · *"not being perfectly constrained, plastic effects will consume some of the locally developed stress"* (p.2151) · *"plastic deformation is slow and perhaps not effective enough"* (p.2151) · *"An important aspect is the reversibility of the deformation to avoid dead space"* (p.2152) · 압력 일축 · 불균일 (p.2147) |
| "(단계 6)" | **일부** | 단계 6 에 줄 실험 값 = 고정 변위 틀 응력 이완 (그림 S5 · ≈ 4.5 % / 15 h · 틀 탓) 과 사이클 응력 크기 (그림 4) 뿐 · 탈압 되돌아옴 값 없음 (§8 단계 6) |
| "jung2019 가 무가압 in situ SEM 을 한 동기 = '가압 해제 이완 [29] 을 배제'" | **없음 (그 뜻의 문장 · 값)** | 이 논문 어디에도 **'가압 해제 (pressure release) 뒤 이완'** 을 다룬 문장 · 데이터가 없다 (본문 17 쪽 + ESI 전수 · 'release' 낱말은 *"stress release of the active materials"* (p.2148 · 활물질 응력이 SE 탄성 변형으로 풀린다는 뜻) 한 번).  가장 가까운 것 = ⓐ *"The obtained stress is corrected by the materials mechanical relaxation"* (p.2149 · 고정 틀 응력 이완을 빼는 보정) ⓑ 그림 S5 빈 틀 표류 ⓒ 그림 S8 (NCM 수축 → SE 와 떨어짐 · 사이클 유발) ⓓ re-tightening 문장 (p.2151).  ⇒ jung2019 의 [29] 인용이 이 넷 중 무엇을 가리켰는지는 Jung 2019 원문 문장으로만 가린다 — jung2019 카드에 원문 영어 문장이 없다 [미확인] |
| "→ 탈압 이완 · 접촉 손실 근거 후보" | **일부 (접촉 손실 = 정성 · 탈압 이완 = 없음)** | 접촉 손실: 그림 S8 (사이클 뒤 SEM · *"The NCM particles contract during delithiation and lose contact with the SE"* · 재게재) · p.2148 *"volume changes … can cause delamination of electrode materials from the SE and crack nucleation"* · p.2151 re-tightening — **값 없음** · 탈압 이완: 없음 (위 줄) |
| "'FEM 고유변형의 NMC622 ΔV 출처'" | **채움 (그림 · 2 차 모음)** | 그림 2a 에 **NCM-622** 계열이 있다 — ΔV/V₀ 0 (x ≈ 0.9) → ≈ −1.0 % (x ≈ 0.56) → ≈ −3.0 % (0.29) → **≈ −4.8 % (x ≈ 0.19, 마지막 점)** [판독] · 그림 2b 에 V̄m(Li, NCM-622) 곡선 · ⚠ **표 · 수식 없음** · 출처 = *"All data for NCM materials … obtained from crystallographic data [… see ref. 35–37]"* (그림 2 캡션) → 측정 원전은 **de Biasi 2017 [37] · Kondrakov 2017 [35]** (파우치 셀 operando XRD · 0.1C · 25 °C · p.2153) |
| "(우리 --cycle-dv-* 기본값과 대조할 원전)" | **일부** | 대조는 §7-2 표로 나란히 (판정 없이).  우리 기본값의 help 글은 **Kondrakov 2017 (NMC811 3.0–4.3 V) 5.1 %** 라고 적는다 [우리 `scripts/cycle_contact_ledger.py:604` · `scripts/mpm3d_compaction.py:865`] — 이 논문은 그 값을 인쇄하지 않는다 (NCM-811 인쇄값 = SI 의 −6 % · 그림은 −6.5 % 끝점).  우리 값의 원전 확인은 Kondrakov 2017 카드가 필요하다 (§12 · 질문 n) |

**가리킨 카드 · 같은 논문을 옮긴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `jung2019_…` L440 | 서지 *"29 R. Koerver, et al. Chemo-mechanical expansion of lithium electrode materials–on the route to mechanically optimized all-solid-state batteries, Energy Environ. Sci., 2018, 11, 2142–2158."* | p.2142 머리 · 제목 · 권 · 쪽 같음 | **채움** |
| `jung2019_…` L280 | *"무가압 in situ SEM 으로 균열 생성 확인 (가압 해제 이완 [29] 을 배제하려는 시도)"* | 이 논문에 **가압 해제 이완** 을 다룬 문장 · 값이 없다 (위 표) · 있는 것 = 고정 틀 응력 이완 보정 (p.2149) · 수축 → 접촉 손실 (그림 S8) | **없음 (원문과 안 맞음)** — jung2019 원문 문장 대조 필요 · 카드 문제로 보고 |
| `benhadjali2026_…` L430 | 서지 + *"카드 없음 — FEM 고유변형의 NMC622 ΔV 출처"* | 서지 같음 · NCM-622 ΔV(x) = 그림 2a (끝 −4.8 % [판독]) | **채움** (단 2 차 모음 — 측정 원전 = refs 35/37) |
| `benhadjali2026_…` L241 | *"ΔV = Koerver 2018 [3] 의 NMC622 부피 변화 (탈리튬에서 잰 값을 리튬화에도 가역으로 · Figure S2 [미확인])"* | 그림 2a 의 x 축 = 탈리튬 방향 (캡션) · 가역성은 이 논문이 따로 보이지 않음 | **채움** (가역 가정은 Ben Hadj Ali 쪽 가정) |
| `barai2021_…` L19 · L130 | *"V̄(Li) = Koerver 2018 EES 11, 2142 (ref 36) 실험"* | V̄ 곡선 = 그림 2b (*"All data for NCM materials, LCO and graphite were obtained from crystallographic data [LCO in this work, others see ref. 35–37]"*) — 실험 (XRD) 은 맞고 NCM 은 **2 차 모음** · LCO 는 OCV 로도 (그림 3) | **일부** — NCM V̄ 의 측정 원전은 refs 35–37 |
| `barai2021_…` L687 · L218 | *"V̄ 의 실험 원전 · Fig. S2 · Fig. 10a 의 원데이터 … 원데이터가 필요"* · Barai Fig. S2a NMC 판독 ≈ 3 (x 0.47) · ≈ 8 (0.32) · ≈ 15.5 (0.26) cm³/mol | 이 논문은 **표가 없다** (그림 2b 곡선뿐) · 그림 2b NCM-811 열 표본 ≈ 3.0 · 9.0 · 17.1 (같은 x · NCM-622 도 비슷) [판독 · ±0.5–1] | **일부** — 같은 자릿수 · '원데이터' 는 이 논문이 아니라 refs 35–37 에 있다 |
| `doerrer2021_…` L309 | *"전극 부피 변화 (LTO 0.2 %)"* | p.2145 *"a negligible volumetric strain of −0.2% upon delithiation"* (렌더 부호) | **일부** (부호 빠짐 — 글자 층이 '−' 를 잃는 곳) |
| `tian2020_…` L603 | *"부피–농도의 비선형 관계"* | p.2144 *"the dependence on lithium content is not necessarily linear"* · 흑연 *"strongly non-linear"* | **채움** |
| `park2025_…` L353 | *"부피 변화 · 두께 방향 SOC — … (후보 N-9)"* | 부피 변화 = 그림 2a · 두께 방향 SOC 는 이 논문 내용 아님 (다른 refs 몫) | **채움 (부피 변화)** |
| `nolan2018_…` L531 | *"화학-기계 팽창 | 156 | Koerver 2018 EES 11, 2142"* | 주제 같음 | **채움** |
| `comparison_vs_ours_DEM.md` L2795 (benhadjali 줄) | *"AM 리튬 고유변형 (Koerver 2018 ΔV …)"* | 위와 같음 | **채움** |

⇒ **의도 대조 결과: 채움 (j · NMC622 ΔV 출처 = 그림 2a (2 차 모음)) · 일부 (단계 6 · 접촉 손실 정성 · 우리 --cycle-dv-* 대조는 나란히만) · 없음 (b = 탈압 되돌아옴 값 · '가압 해제 이완 [29]' 에 해당하는 문장)**.  jung2019 L280 의 '가압 해제 이완' 귀속은 이 원문으로 확인되지 않는다.

---

## 1. 한 줄 요약
고체 전지에서는 액체가 부피 변화를 흡수해 주지 못하므로, 전극 재료의 Li 부분 몰 부피 (부피 ÷ Li 몰 · 결정학 · OCV 압력 의존 두 길) 와 구속 셀의 응력 (힘 센서 · 선형 탄성 추정 두 길) 을 함께 보고, 부호가 반대인 재료를 섞어 셀 응력을 줄이자고 제안한 논문이다.
NCM · NCA 는 충전 때 줄고 (Ni 많을수록 크게 · NCM-811 ≈ −6.5 % [판독]) LCO 는 x ≈ 0.6 까지 ≈ +2 % 늘었다가 준다; Li · 흑연 · In 음극은 충전 때 리튬화로 늘어 CAM 보다 10 배 넘는 응력을 낸다.
고정 틀에서 잰 응력 변화는 CAM/LTO 셀에서 ≈ 0.05–0.07 MPa (스택 ≈ 60 MPa 의 0.1 %) 로 작지만, 완전 구속을 가정한 선형 탄성 추정은 수십 MPa 의 정수압을 준다 — 저자는 실제 셀이 완전히 구속되지 않고 소성 · 기공이 일부를 흡수한다고 본다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (CAM / SE / 음극) | 연구유형 |
|---|---|---|---|---|
| R. Koerver · W. Zhang · L. de Biasi · S. Schweidler · A. O. Kondrakov · S. Kolling · T. Brezesinski · P. Hartmann · W. G. Zeier\* · J. Janek\* (JLU Giessen · KIT BELLA · BASF · TH Mittelhessen) | *Energy Environ. Sci.* 11 (2018) 2142–2158 · Paper | 10.1039/C8EE00907D (인쇄 소문자 `10.1039/c8ee00907d`) | **NCM-811 · NCA-801505 (BASF) · LCO (Alfa Aesar 97 % · LiNb₀.₅Ta₀.₅O₃ 코팅)** / **β-Li₃PS₄** (결정질 · BASF) · **LGPS** (자체 고상 합성 · OCV 셀) / **LTO (BASF) · 흑연 (BASF) · Li 박 · In 박 (6 mm)** | 실험 (operando 응력 · 압력별 OCV · SEM/EDX · operando XRD 는 문헌 절차) + 선형 탄성 추정 |

- **1저자 메모와의 대조**: 저자 열 명 · 제목 · *Energy Environ. Sci.* 11 (2018) 2142–2158 · DOI C8EE00907D — PDF 1 쪽 · 메타데이터 (Subject 줄 *"Energy & Environmental Science (2018), 11, 2142-2158, doi:10.1039/C8EE00907D"*) 와 **모두 같다**.  덧붙임: 인쇄 DOI 는 소문자 · 제목 끝에 †(ESI) · ESI 표지 제목은 *"… on the route to mechanically optimized solid-state batteries"* ("all-" 없음).
- 글의 꼴: 1 Introduction → 2 Chemical expansion of electrode materials → 3 The reaction volume of operating cells (E_oc = f(p)) → 4 Pressure build-up in operating cells (Mechanical properties · formal treatment · experimental results · interpretation · Chemo-mechanical balancing) → 5 Conclusion → 6 Experimental methods — 본문 그림 5 · **표 1** · 번호 식 12 · 참고문헌 115 · ESI = 그림 S1–S8 · 표 S1–S4 · 식 S1–S11.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 재료 · 셀 · 압력 이력 (p.2153 · `txt_p11_p12_cell_assembly_pressures.png` · `txt_p12_stress_monitoring_protocol.png` · 그림 S2)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| SE (응력 셀) | 결정질 **β-Li₃PS₄** (BASF) — ESI p.S4 는 *"β-Li₃PS₄ glass ceramic"* 이라 부른다 | [인쇄] p.2152 · S4 |
| SE (OCV 셀) | **LGPS** (고상 합성 · ref 66 절차) | [인쇄] p.2152 |
| CAM | NCM-811 · NCA-801505 (BASF) · LCO (Alfa Aesar 97 % · LiNb₀.₅Ta₀.₅O₃ 졸-겔 코팅) · 입경 [미확인] | [인쇄] p.2152 |
| 건조 · 보관 | 진공 Büchi 오븐 250 °C 밤새 · Ar 글러브박스 (H₂O · O₂ < 0.1 ppm) | [인쇄] p.2152 |
| 조성 (질량) | 양극 CAM : β-Li₃PS₄ = **70 : 30** · 섞기 양극 = NCM-811 : LCO 55 : 45 → **NCM-811 : LCO : SE = 38 : 32 : 30 wt%** (카드 산술 38.5 : 31.5 : 30) · LTO : SE = 35 : 65 · 흑연 : SE = 50 : 50 · 마노 유발 15 min · vol% [미확인] | [인쇄] p.2152–2153 |
| 셀 | 양극 복합체 **12 mg** · SE 분리막 **60 mg ≈ 400 µm** · 음극 LTO 복합체 35 mg 또는 흑연 복합체 12 mg 또는 In · Li 박 6 mm · 셀 지름 [미확인] → **≈ 10 mm** [카드 산술: 35 kN ÷ 445 MPa = 78.7 mm² · 그림 S5 축 5.15 kN ↔ 65.5 MPa = 78.6 mm² · 표 S3 r = 0.5 cm 와 같음] | [인쇄] p.2153 · [카드 산술] |
| 분리막 겉보기 밀도 | 60 mg ÷ (π · 0.5² cm² × 0.040 cm) = **1.91 g/cm³** [카드 산술 · 지름 10 mm 가정 · 두께 "≈ 400 µm"] — β-Li₃PS₄ 진밀도 · 기공률 [미확인] | [카드 산술] |
| ★ 압력 이력 | ① 분말만인 셀 = **조립 뒤 35 kN (≈ 445 MPa)** 로 누름 · 금속박 음극 셀 = 분말을 35 kN 으로 누른 뒤 음극을 얹음 ② 전기화학 중 **≈ 70 MPa** (*"a reduced pressure of approximately 70 MPa"*) ③ 응력 측정 셀 = 틀을 **10 Nm** 로 조임 *"corresponding to a force of 60 ± 8 MPa"* (힘을 MPa 로 적음) · 누름 시간 · 속도 [미확인] | [인쇄] p.2153 |
| 응력 측정 | 힘 센서 **KMT 55** (Inelta) 를 바닥 강 피스톤에 · *"This allows to adjust a certain strain during battery cycling as well as to monitor the uniaxial stress response"* · 측정 전극이 센서 쪽 · LabVIEW 11.0.1 · 25 °C · SP-300 | [인쇄] p.2153 |
| 사이클 | NCM · NCA · 섞기 → 4.3 V vs Li · LCO → 4.2 V vs Li · 음극 전위 가정 In 0.6 · LTO 1.55 · 흑연 0.10 V vs Li · 섞기 셀 창 1–2.75 V (LTO) · 186 µA cm⁻² · 0.1C × 5 → 0.25C × 5 → 0.1C 계속 · **충방전 전 OCV 20 h** (셀 틀 표류를 줄이려고) | [인쇄] p.2153 |
| XRD | 자체 회절계 Mo-Kα₁,₂ · 파우치 셀 · 0.1C · 25 °C (NCM · NCA · LCO 단위 격자 부피) — 세부는 refs 35 · 36 · 112 | [인쇄] p.2153 |
| SEM/EDX | Zeiss Merlin · Leica EM VC500 Ar 이송 · 5 kV · 100 pA (SEM) · 1000 pA (EDX) · Oxford XMAX EXTREME | [인쇄] p.2153 |

### 3-2. ★ 전극 재료별 부피 변화 ΔV (그림 2a · p.2144–2146 · `fig_2a.png` · `txt_p3_ncm_volume_contraction.png` · `txt_p4_lto_lfp_two_phase.png`)
| 재료 | 상태 · 방향 | ΔV | 표지 · 위치 |
|---|---|---|---|
| **NCM-111** | 탈리튬 x 1 → ≈ 0.24 (그림 2a 마지막 점) | **≈ −2.0 %** · x 0.44 에서 ≈ −0.8 % | [판독] 그림 2a |
| **NCM-523** | → x ≈ 0.22 | **≈ −3.3 %** · x 0.51 ≈ −1.0 % | [판독] |
| **NCM-622** | → x ≈ 0.19 | **≈ −4.8 %** · x 0.56 ≈ −1.0 % · 0.29 ≈ −3.0 % | [판독] |
| **NCA** (Ni 0.8 · Co 0.15 · Al 0.05) | → x ≈ 0.17 | **≈ −5.7 %** · x 0.50 ≈ −0.9 % · 0.26 ≈ −3.3 % | [판독] |
| **NCM-811** | → x ≈ 0.15 | **≈ −6.5 %** · x 0.46 ≈ −1.4 % · 0.25 ≈ −3.9 % · 0.19 ≈ −5.7 % | [판독] |
| NCM-811 (모델 입력) | *"NCM-811 experiences contraction of roughly 6 % when charging to 4.3 V vs. Li"* (ESI ref 2 = de Biasi 2017) · 표 S3 *ΔV_cryst(charge)* **−6.0 %** · 본문 *"ΔV_cryst(NCM) = −6%"* | [인쇄] S5 · 표 S3 · p.2151 |
| **LCO** | x 1 → 0.6 팽창 → 그 뒤 수축 | 최대 **≈ +2.2 %** (x ≈ 0.59–0.61) · 0 (x ≈ 0.46) · ≈ −1.0 % (x ≈ 0.43) [판독] · 본문 *"increases upon delithiation to Li₀.₅CoO₂ by roughly +2%"* · 모델 입력 **+1.4 %** (*"approximately 1.4 % during delithiation"*) | [판독] · [인쇄] p.2144 · S5 · 표 S3 |
| LTO (Li₄Ti₅O₁₂) | 탈리튬 | **−0.2 %** (*"negligible volumetric strain of −0.2% upon delithiation"* · 렌더 부호) | [인쇄] p.2145 |
| LFP | LiFePO₄ → FePO₄ (두 상) | **≈ −7 %** (렌더 부호) | [인쇄] p.2145 |
| 흑연 | 완전 리튬화 (*"Li6C"* 인쇄 그대로) | **≈ 13 %** · 강한 비선형 | [인쇄] p.2144 |
| Si | 리튬화 | **최대 400 %** | [인쇄] p.2144 |
| a · c 격자 상수 값 | — | **[미확인]** (본문은 *"While the layered compounds exhibit unit cell expansions along the z-direction due to the higher Coulombic repulsion … the x–y-directions directly depend on the nature and size of the transition metal"* (p.2144) 의 방향 설명뿐) | [인쇄] p.2144 |

- 판독 방법: 그림 2 원본 래스터 (xref 279 · 1503 × 610 px · 300 dpi) — 패널 a 틀 x 83–713 · y 29–534 px · x 눈금 0.8/0.6/0.4/0.2 = 208.5/335.0/460.5/587.0 px · y 눈금 2/0/−2/−4/−6 % = 54.5/156/256/357.5/458 px · 표지 중심 = 색 분리 성분 상자 중심 (겹친 표지는 분리 못 함) · 끝점은 3 배 확대 격자에서 눈으로 (±2 px = ±0.003 x · ±0.04 %) — `digitized.csv`.
- ⚠ 그림 2a 의 끝점은 **회절 실험이 간 가장 깊은 탈리튬** 이다 — 같은 "4.3 V" 라도 셀 · 율속 · 온도에 따라 x 가 다르다.  이 논문의 **ASSB 셀** (그림 4b · LTO 상대 · 2.75 V = 4.3 V vs Li 가정) 은 x **0.85 → ≈ 0.53** [판독] 까지만 갔고, 그 창의 NCM-811 ΔV 는 그림 2a 로 **≈ −1.0 ~ −1.2 %** [판독 · 이웃 계열 사이 보간] 이다 — 모델 입력 −6 % 와 자릿수가 다르다 [카드 해석 · 원문 언급 없음].

### 3-3. Li 부분 몰 부피 V̄m(Li) (식 1–2 · 그림 2b · p.2145–2146 · `eq_01_partial_molar_volume_definition.png` · `eq_02_volume_change_integral.png` · `fig_2b.png`)
- 정의 (식 1) V̄m(Li) ≡ (∂V/∂n(Li))_{T, p, nᵢ≠n_Li} · 적분 (식 2) ΔV = ∫ V̄m(Li) dn(Li) — *"In contrast to relative volume changes, i.e. the volumetric strain, it represents the absolute volume change upon lithiation"* (p.2145).
- 기준 = Li 금속 몰 부피 **12.97 cm³ mol⁻¹ (298 K)** — *"a kind of typical upper limit"* (p.2145) · 그런데 고 Ni NCM · NCA 는 아주 낮은 x 에서 이보다 크다 → *"severe changes in chemical bonding"* (p.2145).
- 두 상 재료 = 겉보기 V̄′m (반응 부피): **In → InLi +7.89 cm³ mol⁻¹** (V_m(In) 15.71 · V_m(InLi) 23.60 · ref 11) · **FP → LFP +11.62** · **LTO ≈ 0** · **a-Si → Li₁₅Si₄ 8.85** (1 Li 당 · 3580 mA h g⁻¹ · Si 당 > 3.75 Li) [인쇄] p.2145–2146.
- 그림 2b 곡선 [판독 · 색 분리 열 표본 · ±0.5–1 cm³/mol]: NCM-811 ≈ 2 (x 0.9–0.6) → 2.6 (0.5) → 3.0 (0.47) → 6.0 (0.35) → 9.0 (0.32) → 11.7 (0.30) → 17.1 (0.26) → 20.1 (0.24) · NCM-111 ≈ 0.5–1.7 (x 0.9–0.5) → 5.0 (0.30) → 8.2 (0.24) · LCO ≈ −2.3 (0.9) · −3.7 (0.8) · −3.9 (0.7) → 부호 바뀜 x ≈ 0.58–0.6 → 급상승 · 본문: NCM *"small positive partial molar volume, which increases steeply for x < 0.4 when a and c axis shrink simultaneously"* · LCO *"changes sign to positive values for x < 0.6"* (p.2146).
- 결론 문장: *"when lithium is inserted into an electrode active material (except LCO), its volume increases"* → 양극 · 음극이 반대로 움직여 순 압력이 줄어드는 조합 (LTO/NCM) ↔ 같이 느는 조합 (LCO + 흑연 · Li) (p.2146).

### 3-4. OCV 의 압력 의존 — 반응 부피 (식 3–10 · 표 S1 · S2 · 그림 3 · S1 · p.2146–2147 · `eq_03`–`eq_10` · `tab_S1.png` · `tab_S2.png` · `fig_S1.png`)
- 식 (3) (∂E_oc/∂p)_{T,nᵢ} = −Δ_rV_m/(nF) · 식 (5) Δ_rV_m(방전) = V̄m(Li, Li_rCat) − V̄m(Li, Li_mAn) · 셀 = **InLi | LGPS | LTO/LGPS** 와 **InLi | LGPS | LCO/LGPS** · 압력을 차례로 올리며 OCV (그림 S1 · ESI *"as a function of the ramped up stress"*).
- **In|LTO**: 기울기 **1.22 × 10⁻⁵ V (10⁵ Pa)⁻¹ = +0.122 mV MPa⁻¹** → **V̄′m(Li, In/InLi) ≈ +11.81 cm³ mol⁻¹** (식 7 · 표 S1) — 결정학 +7.89 보다 **≈ +50 %** (*"the OCV appears to be more affected by the applied pressure than predicted"* · p.2147).
- **In|LCO** (표 S2 · 그림 3) — x(Li) 0.65 · 0.75 · 0.80 · 0.86 · 0.94 에서 기울기 2.27 · 3.40 · 10.17 · 8.56 · 8.43 × 10⁻⁶ V (10⁵ Pa)⁻¹ (오차 0.58 · 0.58 · 1.40 · 0.71 · 1.11 × 10⁻⁶) → −F(∂E/∂p) 2.19 · 3.28 · 9.84 · 8.26 · 8.13 cm³ mol⁻¹ → V̄m(Li, LiₓCoO₂) = **+5.70 · +4.61 · −1.95 · −0.37 · −0.24** (결정학 In 7.89 기준 · 그림 3) 또는 +9.62 · +8.53 · +1.97 · +3.55 · +3.68 (OCV In 11.81 기준) [인쇄] · 본문 *"ranges from −2 to +6 cm³ mol⁻¹"* · 부호 바뀜이 회절 (x 0.6) 보다 높은 x (≈ 0.785 [카드 산술: x 0.80 (−1.95) ↔ 0.75 (+4.61) 직선 보간]) 에서 [카드 산술: 표 S2 두 열 = 7.89 − 열 4 · 11.81 − 열 4 · 다섯 줄 모두 재현].
- 압력 단계 (p.2153): 충전 때 **0.5 t** · 각 SOC 에서 OCV 를 *"5 different pressures: 0.5t–1.2t–1.7t–2.2t–2.8t (55 MPa–94 MPa–143 MPa–192 MPa)"* — **하중 다섯 · MPa 값 넷** [인쇄] · 그림 S1 의 점 = ≈ 49 · 96 · 140 · 193 · 236 MPa (S1a) · ≈ 55 · 98 · 141 · 192 · 233 MPa (S1b) [판독 · 눈대중 ±2 MPa] → 다섯째 ≈ 233–236 MPa 가 인쇄에서 빠짐 · OCV 안정 기준 *"voltage drop < ~0.005 V s⁻¹"* · 0.1C (LCO 셀 90 µA · LTO 셀 140 µA — ESI 그림 S1 캡션은 LTO 셀에 *"0.1 C (90 µA)"*).
- 저자 해석 (p.2147 · `txt_p6_ocv_nonideal_uniaxial_plastic.png`): *"We believe that this difference is mainly due to the non-ideal pressure experiment. In fact, pressure is not applied uniformly but uniaxially, and orientation of the anisotropic CAM particles may not be perfectly random. … Furthermore, only if the applied pressure is transferred completely to the LCO, the OCV will reflect the full pressure. Thus, non-isochoric plastic deformation as well as the porosity of the SE may influence the OCV measurement under pressure."*
- 크기 감각 (p.2147): *"even severe pressure changes on the order of 1 MPa cause only relatively small OCV changes of around 0.1 mV"* — [카드 산술] 0.122 mV MPa⁻¹ × 300 MPa ≈ **37 mV** (In|LTO 기울기를 300 MPa 로 늘린 값 · 원문 아님).

### 3-5. ★ 구속 셀 operando 응력 (그림 4 · 5 · S5 · S6 · p.2149–2151 · `fig_4a`–`fig_4d` · `fig_5.png` · `fig_S5.png` · `fig_S6a` · `fig_S6b` · `txt_p8_stress_results.png`)
| 셀 (측정 전극 = 센서 쪽) | 충전 끝 σ₁₁ (오른쪽 패널 · 평활선) | 시간 패널 극값 | 표지 |
|---|---|---|---|
| LTO/SE \| SE \| **LCO**/SE (ref 11 자료) | **≈ +0.57 × 10⁵ Pa** (x 0.95 → 0.645) | 0.1C 봉우리 ≈ +0.6–0.68 · 첫 사이클 ≈ +0.33 · 0.25C ≈ +0.42 | [판독 · 눈대중 ±0.05] 그림 4a · 5a |
| LTO/SE \| SE \| **NCM-811**/SE | **≈ −0.45 × 10⁵ Pa** (x 0.85 → 0.535) | 첫 골 ≈ −0.62 · 뒤 골 ≈ −0.42 | [판독] 그림 4b · 5b |
| LTO/SE \| SE \| **NCA**/SE | **≈ −0.53 × 10⁵ Pa** (x 0.85 → 0.505) | 골 ≈ −0.55 ~ −0.6 | [판독] 그림 S6a |
| **Li** \| SE \| NCM-811/SE | **≈ +14.7 × 10⁵ Pa** (x 0.88 → 0.495) | 첫 봉우리 ≈ +17 · 0.25C ≈ +10.5 | [판독 ±0.5] 그림 4c |
| **C₆**/SE \| SE \| NCM-811/SE | **≈ +6.1 × 10⁵ Pa** (x 0.85 → 0.445) | 봉우리 ≈ +6.7 | [판독] 그림 4d |
| **InLi** \| SE \| NCM-811/SE | **≈ +10.6 × 10⁵ Pa** (x 0.85 → 0.485) | 첫 봉우리 ≈ +12.8 · ESI *"up to 10 bar"* | [판독] 그림 S6b · [인쇄] S8 |
| LTO \| SE \| **NCM-811 : LCO 55 : 45** | ≈ 0 (충전 끝) · 중간 최소 ≈ −0.15 × 10⁵ Pa (≈ 3 h) | *"Δσ₁₁ ~ 0"* | [판독] 그림 5c |

- **단위**: 모든 σ₁₁ 축이 **"σ₁₁ / 10⁵ Pa"** (= bar) 다 — 0.6 × 10⁵ Pa = **0.06 MPa**.  ⚠ 본문 *"a net stress of σ₁₁(LCO/LTO) = +0.6 MPa – which is substantial"* (p.2149) 는 축 · 표 S4 (σ₁₁ = −0.06 MPa *exp.* · 고체역학 부호 = 압축 음) 와 **10 배** 어긋난다 (§3-9 ①).
- 본문 비율: *"When LTO is replaced by a metal anode or graphite (Fig. 4c and d), the stress response experiences a ten- to twenty-fold increase, respectively"* (p.2149) — [카드 산술] 판독으로는 Li ≈ 14.7 / 0.5 ≈ **25–30 배** · 흑연 ≈ 6.1 / 0.5 ≈ **≈ 12 배** → "respectively" 의 순서가 그림과 반대로 읽힌다 (§3-9 ③).
- 크기 대비 [카드 산술]: CAM/LTO 0.05–0.07 MPa ÷ 스택 ≈ 60 MPa ≈ **0.1 %** · Li ≈ 1.5 MPa ≈ 2.5 % · InLi ≈ 1.0–1.3 MPa ≈ 2 %.
- 율속: 0.25C 에서 용량이 줄어 응력 변화도 작다 (*"less lithium is transferred"* · p.2149).
- **그림 S5 (보정 전 원자료 · InLi | SE | NCM-811/SE)** [판독 · 원본 래스터 535 dpi 보정 · `digitized.csv`]:
  - OCV 대기 (0 → ≈ 16 h): 셀 (주황) ≥ 5.15 kN (축 위로 잘림) → 5.128 kN (0.5 h · 65.2 MPa) → 5.036 (2 h · 64.1) → 4.940 (8 h · 62.9) → **4.894 kN (15.5 h · 62.3 MPa)** — 0.5 → 15.5 h 에 −0.234 kN (−2.9 MPa · −4.6 %) [카드 산술].
  - 빈 틀 표류 (회색 · *"mechanical drift of an empty cell casing due to the plastic insulators"*): 5.119 kN (0.2 h · 65.1 MPa) → 5.009 (2 h) → **4.913 (15.5 h · 62.5 MPa)** → 4.887 (27 h) → 4.845 kN (62 h · 61.7 MPa) · 0.2 → 62 h 에 −0.274 kN (−3.4 MPa · −5.4 %) [카드 산술].
  - 사이클 (0.1C): 봉우리 · 골 = 4.977 (22.5 h) / 4.878 (27.0) · 4.948 / 4.855 · 4.927 / 4.838 · 4.910 / 4.824 · 4.897 / 4.813 kN → 진폭 ≈ 0.08–0.10 kN = **≈ 1.0–1.2 MPa** · 골이 27 → 62 h 에 −0.065 kN 내려가는데 같은 구간 빈 틀은 −0.042 kN → 차 ≈ −0.023 kN (≈ −0.3 MPa) 는 틀로 설명 안 되는 몫 [카드 산술 · 판독 · 원문 해석 없음].
  - 힘 축 ↔ 응력 축: 4.75–5.15 kN ↔ 60.5–65.5 MPa (같은 높이) → 면적 ≈ 78.6 mm² (지름 ≈ 10.0 mm) [카드 산술].
  - OCV 대기는 그림에서 **≈ 16 h** [판독] — 방법 절은 *"kept at OCV for 20 h"* (p.2153).

### 3-6. ★ 선형 탄성 추정 — 모든 면 구속 · Reuss 균질화 (식 11 · 12 · S1–S11 · 표 S3 · S4 · 그림 S3 · S4 · p.2149 · 2151 · S4–S7)
- **가정** (ESI p.S4 · `txt_SI_p4_linear_strain_fluid_assumption.png`): *"we assume that the SSB is composed of a single material, which in this case has the mechanical properties of the herein employed β-Li₃PS₄ glass ceramic. We further assume that due to the sufficient elasticity of the solid electrolyte it behaves like a fluid in a system, which is constrained on all sides."*
- 식: κ_T = 1/K = 3(1 − 2ν)/E (S1) → Hencky 적분 (S2) → Δp = −ln(V/V₀)/κ_T (S3) = −ln(1 + ε_vol)/κ_T (S4) → 선형화 **Δp ≈ −ε_vol K** (S5 · 본문 식 11) · 모든 면 구속이면 σ₁₁ = σ₂₂ = σ₃₃ = −E/(1 − 2ν) ε₀ = −3Kε₀ (S6) · p = −⅓(σ₁₁ + σ₂₂ + σ₃₃) = −K ε_vol, ε_vol = −3ε₀ (S7, 인쇄 그대로).
- **표 S3** (원통 r = 0.5 cm · h = 500 µm · 완전 구속): LiCoO₂ m(CAM) 0.0084 g · ρ 4.75 g cm⁻³ · ΔV_cryst(charge) **+1.4 %** → **p = +14.39 MPa (+143.9 bar)** · LiNi₀.₈Co₀.₁Mn₀.₁O₂ 0.0084 g · 4.64 g cm⁻³ · **−6.0 %** → **−65.97 MPa (−659.7 bar)** · 본문 *"Δp(LCO/LTO) = 144 bar and Δp(NCM/LTO) = −659 bar"* [인쇄].  [카드 산술] 표의 입력 (m 8.4 mg = 12 mg × 0.70 ✓) 으로 셀 부피 분율 ε = (m/ρ)/(π r² h) × ΔV = 6.30 × 10⁻⁴ (LCO) · 2.77 × 10⁻³ (NCM) → 두 줄을 같은 K 로 재현하려면 K = 22.8 GPa (LCO) · 23.8–23.9 GPa (NCM) 가 필요하다 — 한 K 로 재현 안 됨 (표 1 β-Li₃PS₄ K 21.4 · 식 S1 로 28.9/(3 × 0.46) = 20.9 GPa).
- **Reuss** (ESI p.S5–S6 · `txt_SI_p5_reuss_inputs.png` · `txt_SI_p6_reuss_values.png`): *"In the experimental setup, only the stress component σ₁₁ in axial direction has been measured directly"* · 양극층 50 µm 의 CAM : SE = **1 : 1 (부피)** · E_SE (β-Li₃PS₄) **28.9 GPa** · E_CAM LCO **191** · NCM **198 GPa** (표 1 의 NCM-111 = 199.0) · 직렬 스프링 E_Cathode^eff = (V_SE/E_SE + V_CAM/E_CAM)⁻¹ (S8) = **50.4 GPa** → 셀 단위 V_Cathode/V_Cell = 0.1 → **E_Cell^eff = 30.2 GPa** · **K_Cell^eff = 21.8 GPa** · ν_eff = ν(β-Li₃PS₄) = **0.27** · 고유변형 ε₀,Cathode^eff = ε₀,CAM V_CAM (S9) · 옆 구속 σ₁₁ = 3K((1 − ν)/(1 + ν) ε₁₁ − ε₀) (S10) · σ₂₂ = σ₃₃ = 3K(ν/(1 + ν) ε₁₁ − ε₀) (S11) — 측정 σ₁₁ 로 ε₁₁ 을 풀고 σ₂₂ · σ₃₃ 를 계산 [카드 산술: (0.5/28.9 + 0.5/198)⁻¹ = 50.44 ✓ · (0.1/50.4 + 0.9/28.9)⁻¹ = 30.19 ✓ · 30.2/(3 × 0.46) = 21.88 ✓].
- **표 S4**: LiCoO₂ σ₁₁ = **−0.06 MPa exp.** · σ₂₂ = σ₃₃ = −14.94 calc. → **p_R = +9.98 MPa (+99.8 bar)** · p_L = +143.9 bar / NCM-811 σ₁₁ = **+0.05 exp.** · σ₂₂ = σ₃₃ = −63.96 calc. (인쇄) → **p_R = −42.66 MPa (−426.6 bar)** · p_L = −655.6 bar · 본문 *"compressive pressure of p(LCO/LTO) = 100 bar … tensile pressure is p(NCM/LTO) = −427 bar"* [인쇄].  [카드 산술] p = −(σ₁₁ + 2σ₂₂)/3 → LCO (+9.98 ✓) · NCM 은 σ₂₂ = **+63.96** 이어야 −42.66 이 나온다 (인쇄 부호 −63.96 이면 +42.62) · 역산 ε₀ (인쇄 안 됨) = σ₂₂ 식에서 3.61 × 10⁻⁴ (LCO) · −1.55 × 10⁻³ (NCM) = 0.0258 × ΔV_cryst — V_CAM 0.5 × V_Cathode/V_Cell 0.1 의 선 (ΔV/3 × 0.05 = 0.0167 ΔV) · 부피 (0.05 ΔV) 어느 쪽과도 안 맞음 → 재현 안 됨.
- 저자 결론: *"the results from the experiment agree very well with the change in hydrostatic pressure from the calculation of the linear strain (see ESI†) – despite the simple formal approach. The experimental values can very well be used as a basis for a more sophisticated 3D approximation."* (p.2151) — ⚠ [카드 해석] 측정한 것은 σ₁₁ (≈ 0.05 MPa) 하나이고, p_R 의 크기 (10–43 MPa) 는 **가정한 ε₀ (ΔV_cryst)** 가 거의 다 정한다 — "일치" 는 p_R ↔ p_L 두 추정 사이 (≈ 69 % · 65 % [카드 산술 99.8/143.9 · 426.6/655.6]) 의 말이다.

### 3-7. ★ 탈압 · 이완 · 접촉 손실 — 원문에 있는 것 / 없는 것 (질문 b · R4)
**있는 것**
1. **고정 변위 틀의 응력 이완** (그림 S5 · p.2149 · p.2153): *"The obtained stress is corrected by the materials mechanical relaxation and hence the net pressure changes for a given electrode configuration can be extracted"* · *"Cells were kept at OCV for 20 h prior to cycling to minimize drifts arising from the cell casing"* · *"The nominal stress was calculated by subtracting a manually drawn baseline to further reduce contributions from a mechanical drift and subtract the constantly applied force"* — 값은 §3-5 (≈ 65 → 62.3 MPa · 15.5 h) · 저자는 이것을 **틀 (PEEK 절연) 의 표류**로 보고 뺀다 (재료 성질로 보고하지 않음).
2. **수축 → 접촉 손실** (그림 S8 · 사이클 뒤 SEM · Koerver 2017 Chem. Mater. 재게재): *"The NCM particles contract during delithiation and lose contact with the SE."* · 섞기 양극은 *"good preservation of the contact"* (그림 S7) · *"A delamination of the active materials from the SE is not observed as recently shown for single CAM cathodes"* (p.2151) — 정성 · 값 없음.
3. **다시 조이기의 한계** (p.2151): *"Application of an external pressure cannot fully compensate delamination of electrode materials. Calculations by Tian et al. have shown that re-tightening a cell is not sufficient to recover capacity fade due to contact loss of materials."* (ref 30 = Tian & Qi 2017 JES · 계산 인용 · 이 논문 자료 아님).
4. **소성 · 기공 · 시간** (p.2151): *"Good SSBs may require a minimum porosity in the electrode composites to avoid too strong changes in stress. A certain part of the stress is indeed taken up by the porosity, but this depends critically on the plasticity of the SE. Pore-filling due to volume changes of electrode materials and plastic deformation of SE and electrodes will never work perfectly, as plastic deformation is slow and perhaps not effective enough. Therefore, stress changes will always occur."*
5. **되돌릴 수 있음** (p.2152): *"An important aspect is the reversibility of the deformation to avoid dead space and high internal transfer resistances by cracks and voids, as this will result in electrochemical isolation of active materials."*

**없는 것** [미확인 = 전수에 없음]: 압력을 뺄 때의 두께 · 부피 되돌아옴 · 접촉 면적 변화 · OCV 이력 (압력 내림 쪽) · 제조 445 MPa → 70 MPa 사이에 일어난 일 · 응력 이완의 전극 몫 (틀 몫과 분리) · 시간 상수.

### 3-8. 표 1 탄성 상수 (p.2148 · `tab_1.png` — E/GPa · ν · G/GPa · K/GPa · 출처)
| 재료 | E | ν | G | K | 출처 · 표지 |
|---|---|---|---|---|---|
| LiCoO₂ | 191.0 | 0.24 | 80 | 122.4 ᵇ | J. Sakamoto [79] (Cheng 2017 J. Asian Ceram. Soc. · 이론 표지 없음) |
| LiNi₀.₃₃Co₀.₃₃Mn₀.₃₃O₂ | **199.0** | 0.25 | 78 | 132.6 ᵇ | J. Sakamoto [80] (Cheng 2017 J. Eur. Ceram. Soc. 37, 3213 · 이론 표지 없음) |
| LiFePO₄ ᵃ | 117.8 | 0.30 | 45.5 | 98.2 ᵇ | G. Ceder [81] |
| LiMn₂O₄ ᵃ | 194.0 | 0.26 | 77.0 | 134.7 ᵇ | K. J. Kim [82] |
| xLi₂S(100 − x)P₂S₅ | 14–23 | 0.27–0.37 | 5–9 | 13–21 ᵇ | Tatsumisago · Van Vliet [33, 83–85] |
| γ-Li₃PS₄ ᵃ | 36.9 | 0.26 | 14.1 | 31.9 | H. Yan [86] |
| β-Li₃PS₄ ᵃ | **28.9** | **0.27** | 11.3 | **21.4** | H. Yan [86] |
| Li₁₀GeP₂S₁₂ ᵃ | 37.2 | 0.30 | 14.3 | 31.0 ᵇ | Ouyang · Zeier [87, 88] |
| Li₇P₃S₁₁ ᵃ | 21.9 | 0.36 | 8.1 | 23.9 | S. P. Ong [89] |
| **Li₆PS₅X (X = Cl, Br, I) ᵃ** | **22–30** | **0.33–0.37** | **8–11** | **28–30** | S. P. Ong [89] = 정본 `deng2016_elastic_superionic_electrolytes_dft` |
| LLZO · Ta-LLZO · Al-LLZO | 150.3 · 154.9 · 162.6 | 0.26 · 0.24 · 0.26 | 60.0 · 62.5 · 64.6 | 102.8 · 99.2 · 112.4 | Wolfenstine · Sakamoto · Siegel [73, 90, 91] |
| LiPON ᶜ · γ-Li₃PO₄ ᵃ · LiTi₂(PO₄)₃ ᵃ · NaZr₂(PO₄)₃ ᵃ · 75Na₂S·25P₂S₅ | 77.0 · 103.4 · 143.7 · 120.9 · 14.0 | 0.25 · 0.26 · 0.25 · 0.27 · 0.32 | 31.0 · 40.9 · 57.6 · 47.7 · 5.3 | 51.3 ᵇ · 72.5 · 95.0 · 86.3 · 13.0 ᵇ | Pharr [92] · Ong [89] · Tatsumisago [83] |
| Li · In · LiTi₂O₄ ᵃ · 흑연 · α-Si ᵃ | 4.9 · 12.6 · 181.0 · 32.0 · 96.0 | 0.42 · 0.45 · 0.25 · 0.31 · 0.29 | 4.2 · 4.4 · 73.1 · 12.0 · 62.0 | 11.0 · 42.2 · 125.1 · 28.1 ᵇ · 90.0 | [75, 93–98] |

각주: ᵃ 이론 예측 · ᵇ *"Complementary results of calculation based on eq. a1"* (eq. a1 은 원문 어디에도 없다 [미확인]) · ᶜ 박막 측정.  본문: *"Thiophosphate-based SEs have Young's moduli on the order of 20 GPa and are quite elastic (K/G > 1.75)"* (p.2149 · Pugh [99]) · *"only two constants are necessary to describe an isotropic material uniquely"* (p.2148) — [카드 산술] 인쇄 G 는 E · ν 로 다시 계산한 값과 조금씩 다르다 (LCO 80 ↔ 191/2.48 = 77.0 · Li 4.2 ↔ 4.9/2.84 = 1.7).

### 3-9. ★ 원문 안 어긋남 (원문 비판 목록 — §11 에 다시)
1. **σ₁₁ 단위**: 본문 *"+0.6 MPa"* (p.2149) ↔ 그림 4a 축 *"σ₁₁ / 10⁵ Pa"* 의 +0.6 ↔ 표 S4 *"σ₁₁ = −0.06 [MPa] exp."* → 0.06 MPa (10 배 · 본문이 bar 를 MPa 로 적은 것으로 읽힌다 [카드 해석]).
2. **표 S4 부호**: NCM-811 σ₂₂ = σ₃₃ = −63.96 (인쇄) 이면 p_R = +42.62 — 인쇄 −42.66 은 +63.96 에서 나온다 [카드 산술].
3. **배수 순서**: *"a ten- to twenty-fold increase, respectively"* (금속 → 10 · 흑연 → 20) ↔ 판독 Li ≈ 25–30 배 · 흑연 ≈ 12 배 [카드 산술].
4. **OCV 기울기 크기**: 초록 *"in the order of 1 mV/100 MPa"* ↔ 표 S1 0.122 mV MPa⁻¹ (= 12.2 mV/100 MPa) · LCO 0.023–0.102 mV MPa⁻¹ (2.3–10.2 mV/100 MPa) · 본문 p.2147 *"1 MPa … around 0.1 mV"* [카드 산술].
5. **압력 목록**: 하중 다섯 (0.5t–2.8t) ↔ MPa 넷 (55–94–143–192) · 그림 S1 점 다섯 (다섯째 ≈ 233–236 MPa [판독]).
6. **p_L 두 값**: 표 S3 −659.7 bar ↔ 표 S4 p_L −655.6 bar (같은 양 [카드 해석]).
7. **E_NCM**: 표 1 NCM-111 199.0 ↔ ESI *"for NCM 198 GPa … (see Table 1)"* · 계산 대상은 NCM-811 (표 1 에 없음).
8. **셀 지름**: 그림 S3 캡션 *"1000 µm (diameter)"* ↔ 그림 안 *"1 cm"* · 표 S3 *r = 0.5 cm* · 35 kN ↔ 445 MPa (≈ 10 mm) [카드 산술].
9. **OCV 대기**: 방법 *"20 h"* ↔ 그림 S5 ≈ 16 h [판독].
10. **전류**: 방법 LTO 셀 *"140 µA"* ↔ ESI 그림 S1 캡션 LTO 셀 *"0.1 C (90 µA)"*.
11. **교차 참조**: 방법 *"(example can be found in the ESI, Fig. S3)"* (기준선 예 = 실제 그림 S5) · 섞기 절 *"As shown in Fig. 2, LCO exhibits a positive and NCM-811 a negative nominal stress change"* (응력은 그림 4) · *"(compare to Fig. S8, ESI†).88"* (그림 S8 = ref 8 Koerver 2017 · ref 88 = Wang 2014 LGPS 탄성) · ESI *"As depicted in Figure A1"* · *"see Figure S3a/S3b"* (스프링 = 그림 S4).
12. **V̄ 부호 말**: ESI p.S8 *"The negative partial molar volume of NCM-811"* ↔ 본문 그림 2b · p.2151 *"combining LCO with NCM (one with negative and one with positive partial molar volume of lithium)"* (NCM = 양) — ESI 는 "충전 때 줄어드는 부피" 를 뜻한 것으로 읽힌다 [카드 해석].
13. **"Li6C"** (p.2144 · 흑연 완전 리튬화) — LiC₆ 를 뜻한 것으로 읽힌다 [카드 해석].

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 사슬
(가) **결정학**: 파우치 셀 operando XRD (Mo-Kα · 0.1C · 25 °C) 로 단위 격자 부피 V(x) → ΔV/V₀ (그림 2a) → 미분 V̄m(Li) (그림 2b) — NCM · NCA · 흑연은 refs 35–37 · LCO 는 이 논문.
(나) **열역학**: InLi | LGPS | 양극/LGPS 셀을 SOC 마다 0.5 → 2.8 t 다섯 압력에서 OCV → 기울기 → 반응 부피 (식 3–10 · 표 S1 · S2 · 그림 3).
(다) **역학**: 10 mm 펠릿 셀 (35 kN ≈ 445 MPa 로 성형) 을 고정 틀에 10 Nm 로 조이고 (≈ 60 ± 8 MPa) 20 h OCV → 바닥 힘 센서로 σ₁₁(t) → 손으로 그린 기준선 빼기 → Savitzky–Golay 평활 → σ₁₁ vs x(Li) (x = 이론 용량으로 환산) (그림 4 · 5 · S5 · S6).
(라) **추정**: Δp = −ε_vol K (완전 구속) · Reuss 직렬 균질화 + 측정 σ₁₁ → 옆 응력 · 정수압 (표 S3 · S4).
(마) **사후 SEM/EDX**: 사이클 뒤 단면 (그림 S7 · S8).
- 안 한 것: 압력 해제 측정 · 두께 측정 · 옆 응력 측정 · 반복 셀 · 기공 · 입경 · 탈압 OCV.

### 4-2. 입자 처리
- 실험 — 실제 분말 펠릿.  모델은 입자를 풀지 않는다: CAM 과 SE 를 **부피 분율 두 상의 직렬 스프링** 으로 (그림 S4) · 셀은 **한 재료** (유효 E · ν · 고유변형).  입자 형상 · 접촉 · 소성 · 이방성 · 불균일 응력 없음.
- 우리 대응 (CLAUDE.md): DEM = 단단한 구 · hooke/hysteresis 접촉 · SE 영률 18 배 연화 (1.35 GPa) / MPM = AM 얼린 장애물 + SE J2 소성 (E 1.53 · σ_y 0.30 · ν 0.49 → K 25.5 GPa) / 사이클 = A10 접촉 장부 (`scripts/cycle_contact_ledger.py`) 와 MPM A-1 `--cycle-deform` (AM 반경을 (1 + ΔV)^(1/3) 로) — 이 논문의 ΔV 는 그 반경 변화의 입력 자리에 해당한다.

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **말 없음** (본문 · ESI 에 DEM · discrete element · particle simulation 낱말 0 회).  모델 일반의 한계만: *"The formal treatment is restricted to a relatively simple macroscopic picture, as any more detailed treatment will require numerical methods."* (p.2143) · *"For the sake of simplicity, we neglect the anisotropy of the materials and inhomogeneous stress fields"* (p.2143) · 결론 *"This can be particularly supported by developing advanced computational models, which consider the volumetric change and mechanical parameters of solid electrolytes and active materials."* (p.2152).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — 이유는 적지 않고 **무시했다** 고 적는다: *"the elasticity (and plasticity; here ignored in the estimates) of the cell. The measured pressure can be compared to the calculated (estimated) data and used to judge the plastic flow in the battery experimentally."* (p.2149) · *"Operando X-ray diffraction is used to obtain the crystallographic volume change of single materials; however, plasticity, deformation or combinatory effects of the electrode materials are neglected. In particular, plasticity of the solid–electrolyte has to be considered in future studies, as this component needs to compensate volume changes of the electrode materials."* (p.2152) · 우회 = **SE 를 유체처럼 (모든 면 구속 · 탄성)** (ESI p.S4) · 맞춘 값 **0 개** (입력 = 표 1 · XRD ΔV · 측정 σ₁₁) · 계산 비용 0 (손 계산).  소성 관련 다른 문장: SE 는 *"will itself suffer from the resulting local stress due to elastic and plastic deformation"* (p.2144) · *"non-isochoric plastic deformation as well as the porosity of the SE may influence the OCV measurement under pressure"* (p.2147) · *"plastic effects will consume some of the locally developed stress"* · *"plastic deformation is slow and perhaps not effective enough"* (p.2151).
3. **2D / 3D** — 실험 = 3D 펠릿 · 모델 = *"a simplified (cylindrical) 3D model of a single electrode cell"* (그림 S3) 을 **1D 직렬 스프링** 으로 균질화 (그림 S4) · *"The experimental values can very well be used as a basis for a more sophisticated 3D approximation."* (p.2151) · 2D → 3D 전이 말 없음.
4. **압력을 뺄 때의 거동** — **다루지 않음** (§3-7).  고정 변위에서의 응력 이완 (틀 탓) · 사이클 수축의 접촉 손실 (정성) 뿐.

### 4-4. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| 부분 몰 부피 V̄m(Li) | Li 를 조금 넣을 때 상의 부피가 느는 양 ÷ Li 몰 (식 1) — 상대 변형이 아니라 절대 부피 |
| 겉보기 부분 몰 부피 V̄′m | 두 상 재료 (In/InLi · FP/LFP · LTO) 의 반응 부피를 1 Li 당으로 |
| 반응 부피 Δ_rV_m | 셀 반응의 부피 변화 = 양극 V̄ − 음극 V̄ (식 5) — OCV 의 압력 기울기를 정한다 (식 3) |
| 충전 부피 · 방전 부피 | 저자가 제안한 말 (*"discharge volume and charge volume"* · p.2144) |
| σ₁₁ (nominal / net stress) | 바닥 힘 센서가 본 축 응력 변화 (기준선 · 일정 힘을 뺀 값) |
| 고유변형 ε₀ (eigenstrain) | 응력 없이 생기는 변형 (여기서는 Li 함량에 따른 CAM 부피 변화) — 구속되면 응력 |
| Reuss 근사 | 상들을 직렬로 이어 같은 응력을 받는다고 보는 하한 균질화 (식 S8) |
| 영 변형 (zero-strain) | 충방전 부피 변화가 거의 없는 재료 (LTO −0.2 %) |
| 화학-기계 균형 (chemo-mechanical balancing) | 부호가 반대인 재료를 섞어 순 부피 변화 · 응력을 줄이는 설계 |

---

## 5. Figure set ★
| 그림 (크롭 파일) | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| Fig. 1 (`fig_1.png`) | 세 실험 모식: (a) XRD 격자 (b) OCV 의 압력 의존 (∂E/∂p = −Δ_rV_m/nF) (c) 사이클 중 Δp = −ε_vol·K | 측정 꼴 |
| Fig. 2 (`fig_2.png` · `fig_2a` · `fig_2b`) | (a) ΔV/V₀ vs x(Li) — LCO · NCM-111 · 523 · 622 · NCA · 811 (b) V̄m(Li) — + 흑연 · Li · LFP · a-Si · In · LTO 수평선 | ★★ 재료별 ΔV · V̄ (§3-2 · §3-3 · §7-2) |
| Fig. 3 (`fig_3.png`) | V̄m(Li, LiₓCoO₂) vs x (OCV · 오차 막대) | LCO 부호 바뀜 (OCV 기반) |
| Fig. 4 (`fig_4.png` · `fig_4a`–`fig_4d`) | 네 셀 (LCO/LTO · NCM-811/LTO · Li/NCM-811 · C₆/NCM-811) 의 전압 · σ₁₁ (10⁵ Pa) vs 시간 · σ₁₁ vs x(Li) | ★ 사이클 응력 크기 (§3-5) |
| Fig. 5 (`fig_5.png`) | 한 사이클 σ₁₁ · 전압: LCO (Δσ > 0) · NCM (Δσ < 0) · 섞기 (Δσ ~ 0) | ★ 섞기 상쇄 |
| Table 1 (`tab_1.png`) | 탄성 상수 (CAM · SE · 음극) + 각주 | E · ν · K 입력 (§3-8 · §7) |
| SI S1 (`fig_S1.png` · `fig_S1a` · `fig_S1b`) | OCV vs p (10⁵ Pa): In‖LTO 6 · 8 h · LCO‖In 다섯 SOC | 압력 다섯 단계 [판독] |
| SI 표 S1 · S2 (`tab_S1.png` · `tab_S2.png`) | 기울기 · 반응 부피 | 식 7 · 10 의 숫자 |
| SI S2 (`fig_S2.png`) | 응력 측정 장치 (바깥 · 안쪽 Al 틀 · PEEK 절연 1 · 2 · 집전체 · 펠릿 · 움직이는 피스톤 · 힘 센서 · 초기 압력 나사) | ★ 고정 틀 측정 꼴 · 틀 이완원 (PEEK) |
| SI S3 (`fig_S3.png`) | 원통 모델 (1 cm · 50 µm 양극층 + 450 µm SE · 옆 · 바닥 구속) → 균질화 | 경계조건 |
| SI 표 S3 (`tab_S3.png`) | 완전 구속 선형 추정 (LCO +14.39 · NCM-811 −65.97 MPa) | §3-6 |
| SI S4 (`fig_S4.png`) | CAM/SE 단위 셀 → 직렬 스프링 → 유효 재료 | Reuss |
| SI 표 S4 (`tab_S4.png`) | σ₁₁ exp · σ₂₂ · σ₃₃ calc · p_R · p_L | §3-6 · §3-9 ② |
| SI S5 (`fig_S5.png`) | 보정 전 힘 · 응력 (주황) · 빈 틀 표류 (회색) · 전압 (파랑) vs 시간 | ★★ 고정 변위 응력 이완 (§3-5 · §3-7) |
| SI S6 (`fig_S6.png` · `fig_S6a` · `fig_S6b`) | NCA/LTO · InLi/NCM-811 응력 | §3-5 |
| SI S7 (`fig_S7.png`) | 섞기 양극 사이클 뒤 SEM · EDX (S · Ni · Co) · *"intimate contact"* | 섞기 접촉 보존 (정성) |
| SI S8 (`fig_S8.png`) | 단일 NCM-811 양극 사이클 뒤 SEM — NCM 과 SE 사이 틈 (재게재) | ★ 수축 → 접촉 손실 (정성) |
| 식 23 장 (`eq_01`–`eq_12` · `eq_S01`–`eq_S11`) | 식 번호별 | 보고서 붙임 (§3-3 · 3-4 · 3-6) |
| 근거 문단 21 장 (`txt_p1_abstract` · `txt_p3_ssb_boundary_elastic_plastic` · `txt_p3_ncm_volume_contraction` · `txt_p4_lto_lfp_two_phase` · `txt_p6_ocv_nonideal_uniaxial_plastic` · `txt_p7_stress_coupling_delamination` · `txt_p7_mechanical_properties` · `txt_p8_thiophosphate_elastic_matrix` · `txt_p8_stress_formal_setup` · `txt_p8_stress_results` · `txt_p10_reuss_hydrostatic_pressure` · `txt_p10_plastic_retightening_min_porosity` · `txt_p10_chemo_mechanical_balancing` · `txt_p11_conclusion_plasticity_reversibility` · `txt_p11_p12_cell_assembly_pressures` · `txt_p12_stress_monitoring_protocol` · `txt_p12_pressure_ocv_protocol` · `txt_SI_p4_linear_strain_fluid_assumption` · `txt_SI_p5_reuss_inputs` · `txt_SI_p6_reuss_values` · `txt_SI_p8_s6_text_indium_10bar`) | 인용 문장 (§3-7 · §4-3) | 보고서 붙임 |

## 6. Post-processing ★
- **원문**: XRD Rietveld (세부는 refs 35 · 36 · 112) · OCV 선형 회귀 (표 S1 · S2) · 응력 = 손으로 그린 기준선 빼기 + Savitzky–Golay · x(Li) = 이론 용량으로 환산 (p.2153) · 선형 탄성 손 계산 (ESI).
- **이 카드**: 그림 2 = 원본 래스터 (300 dpi) 화소 · 눈금 보정 · 색 분리 성분 중심 (패널 a) · 색 분리 열 표본 (패널 b) · 그림 S5 = 원본 래스터 (535 dpi) 곡선 추적 · 극값 · 그림 4 · 5 · S1 · S6 = 눈금 눈대중 — 전부 `digitized.csv` note 열에 방법.  카드 산술 = 셀 지름 · 분리막 겉보기 밀도 · 표 S2 · S3 · S4 재현 · Reuss 재현 · 비율 · 대비.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (우리 수치는 CLAUDE.md · 리포 코드 출처를 그 자리에 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 상태 · 측정 연산자가 다르다**)
| 양 | 이 논문 | 우리 | 같은가 · 왜 다른가 |
|---|---|---|---|
| SE 탄성 (LPSCl 류) | 표 1 Li₆PS₅X E 22–30 · ν 0.33–0.37 · G 8–11 · K 28–30 GPa (이론 · Deng 2016) | DFT E_VRH 22.06 · B₀ 26.23 · ν 0.360 · μ 8.11 GPa [우리 CLAUDE.md] · MPM K 25.5 · μ 0.51 · DEM E_eff 1.35 GPa | E · ν · G 는 범위 안 · K 는 우리 B₀ 가 −6 ~ −13 % [카드 산술] · MPM 은 K 만 실물 자릿수 (전단 15.8 배 연화) · DEM 은 18 배 연화 |
| SE 탄성 (응력 셀) | β-Li₃PS₄ E 28.9 · ν 0.27 · K 21.4 | — | 우리 계 아님 |
| CAM 영률 | NCM-111 **199.0 GPa** · ν 0.25 (Cheng 2017 [80]) · LCO 191 | DEM AM E **140 GPa** [우리 CLAUDE.md "rigid 140 GPa AM skeleton"] — ⚠ 그 값의 출처 인용은 철회 이력 (CLAUDE.md 규율 ⑥ · `SELF-51` · `CL-90`) | 조성이 다르다 (111 ↔ 811) · 우리 140 은 출처 [미확인] 상태 · 이 표가 NCM 계 자릿수 하나를 준다 (판정 아님) · NMC811 실측은 정본 `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` (나노압입 138 ± 24 GPa (n = 29) · 인장 165 ± 7 GPa (n = 3)) [다른 카드] |
| Pugh K/G | Li₆PS₅X 28–30 / 8–11 = 2.5–3.8 [카드 산술] · 본문 thiophosphate *"K/G > 1.75"* | DFT 26.23 / 8.11 = 3.23 [카드 산술] · MPM 25.5 / 0.51 = 50 (설계상) | MPM 의 K/G 는 물성이 아니라 부피 보존 소성의 대리 (frame [2]) |
| AM 사이클 부피 변화 | §7-2 | §7-2 | 나란히만 |
| 고정 변위 응력 이완 | 15.5 h 에 ≈ 4.5 % (셀) · ≈ 4.0 % (빈 틀) [판독 · 카드 산술] — 틀 탓 | MPM `hold` = 목표에서 판을 고정하고 침대가 이완 · settled_over_target 0.021 (real_14) · 0.009–0.049 (P:S 킷) [우리 CLAUDE.md DO-NOT 블록] | **같은 이름 · 다른 기전** — 이쪽은 틀 크리프 (시간) · 우리는 속도 무관 소성 모델의 동역학 정착 — 같은 표에 넣지 않는다 |
| 사이클 응력 (고정 틀) | CAM/LTO ≈ 0.05–0.07 MPa · Li ≈ 1.5 MPa | 우리 사이클 계산은 응력을 내지 않는다 (A10 = 접촉 장부 · A-1 = 기하) | 그들만 있음 |

### 7-2. ★ 사이클 ΔV — 우리 기본값과 나란히 (판정 없이 · 질문 의도 ⑦)
| 출처 | 조성 · 형태 | 상태 · 창 | ΔV | 표지 · 위치 |
|---|---|---|---|---|
| 우리 `cycle_contact_ledger.py --dv-pct` | AM 공통 (help: NMC811) | help *"Kondrakov 2017 NMC811 3.0–4.3V"* | **5.1 %** (크기 · 스윕 5.9 *"Yun/Kang"*) | [우리] `scripts/cycle_contact_ledger.py:604` |
| 우리 `mpm3d_compaction.py --cycle-dv-sc` | SC (AM_S) | 충전 상태 하나 · *"Kondrakov NMC811 c-axis collapse"* | **−0.051** (스윕 −0.059) · 등방 근사 | [우리] `scripts/mpm3d_compaction.py:865` |
| 우리 `--cycle-dv-poly` × `--dv-pct-poly` | poly (AM_P) 외피 | 미세 균열 팽창 외피 | **+0.059 × 0.30 = +1.77 %** (외피 반경 몫) [카드 산술] | [우리] `scripts/mpm3d_compaction.py:871` · `:876` |
| 이 논문 ESI · 표 S3 | NCM-811 | *"when charging to 4.3 V vs. Li"* (de Biasi 2017 인용) | **−6 %** | [인쇄] S5 · 표 S3 |
| 이 논문 그림 2a | NCM-811 | x ≈ 0.15 (마지막 점) | **≈ −6.5 %** | [판독] |
| 〃 | NCM-811 | x ≈ 0.25 | ≈ −3.9 % | [판독] |
| 〃 | NCM-811 | x ≈ 0.46 | ≈ −1.4 % | [판독] |
| 이 논문 그림 4b ASSB 셀 | NCM-811 (LTO 상대 · 2.75 V) | x 0.85 → ≈ 0.53 | 그림 2a 로 ≈ −1.0 ~ −1.2 % | [판독 · 카드 해석] |
| 이 논문 그림 2a | NCM-622 | x ≈ 0.19 | ≈ −4.8 % | [판독] (benhadjali2026 FEM 입력 계열) |
| 〃 | NCA · NCM-523 · NCM-111 | x ≈ 0.17 · 0.22 · 0.24 | ≈ −5.7 · −3.3 · −2.0 % | [판독] |
| 이 논문 본문 | LCO | Li₀.₅CoO₂ 까지 · 모델 입력 | *"roughly +2%"* · +1.4 % | [인쇄] p.2144 · S5 |

- 우리 기본값 5.1 % 의 원전 (Kondrakov 2017) 은 **이 논문의 ref 35** 이고 그림 2a 의 NCM 자료 출처 중 하나다 — 그러나 이 논문은 5.1 이라는 숫자를 인쇄하지 않는다 → 원전 확인은 Kondrakov 2017 카드로 (§12 · 질문 n).
- ⚠ 부호 규약: 우리 `--dv-pct` 는 크기 (부호 없음) · `--cycle-dv-sc` 는 부호 있음 (− = 충전 수축) · 이 논문 그림 2a 는 ΔV/V₀ (탈리튬 방향 · NCM 음).

### 7-3. 나란히 놓을 정본 카드 (값 · 조건 그대로 · 기존 카드는 고치지 않는다)
- `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` — 이 논문의 NMC622 ΔV 를 FEM 고유변형으로 (적층압 68 MPa · 선형 탄성) · 그 카드 EM-01: 고유변형 응력은 σ ∝ E 라 연화 E 로는 1/20 [다른 카드].
- `barai2021_delamination_cathode_llzo_multiscale` — 이 논문의 V̄ 를 박리 모델 구동력으로 (V̄ × E_SSE) [다른 카드].
- `bucci2017_chemomech_failure_assb_cycling_czm` (ref 34) — CZM 으로 사이클 박리 · 균열 [다른 카드].
- `deng2016_elastic_superionic_electrolytes_dft` (ref 89) — 표 1 의 Li₆PS₅X 줄 원전 [다른 카드].
- `sakuda2013_sulfide_mechanical_property` (ref 33) — 황화물 탄성 · 성형성 [다른 카드].
- `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` — NMC811 2 차 입자 영률 실측 (나노압입 138 ± 24 · 인장 165 ± 7 GPa) — 이 논문 표 1 의 NCM-111 199 GPa 와 조성 · 측정법이 다르다 [다른 카드].

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **실험 (부피 · 응력) + 0D/1D 균질화 탄성** — 우리 분업으로는 어느 쪽도 아니다 (접촉망 수송 · 소성 형상 둘 다 없음).  우리에게 주는 것은 **사이클 입력 (ΔV)** 과 **구속 셀 응력의 크기 자릿수**.
- 없는 반쪽: 입자 · 접촉 · 소성 · 압밀 · 탈압 · 기공.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = β-Li₃PS₄ · LGPS + NCM-811 · NCA · LCO — 우리 계 (NCM811 + LPSCl) 와 **SE 가 다르다** · 기공 · 압밀 자료 없음.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | 압력 · 응력 **단위 표지 규칙**의 반례 셋: ① 힘을 MPa 로 적음 (*"a force of 60 ± 8 MPa"*) ② 축 10⁵ Pa ↔ 본문 MPa (10 배) ③ 하중 (t) ↔ MPa 환산 목록 결손 → 문헌 압력을 받을 때 "힘 · 면적 · 단위 배수" 를 칸으로 둔다 · 분리막 겉보기 밀도 1.91 g/cm³ [카드 산술] 은 진밀도가 없어 기공으로 못 바꾼다 | 기공 값 없음 · 진밀도 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | ★ 해석해 하나: **완전 구속 블록의 고유변형 → 정수압 p = 3Kε₀** (식 S6 · S7) · 옆 구속 · 위 자유면 응력 σ₁₁ · σ₂₂ (식 S10 · S11) — MPM 에 AM 부피 변화 (`--cycle-deform`) 를 고유변형으로 넣을 때의 단위 시험 후보 | 우리 MPM 은 지금 AM 반경을 바꾸는 기하 (고유변형 응력 아님) |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | **랩 표준과 다른 문헌 값 (탄성만)**: 표 1 Li₆PS₅X E 22–30 · ν 0.33–0.37 · K 28–30 GPa (Deng 2016 이론) — 항복 · 경도 · 기공 곡선 없음 → σ_y 맞춤 표적 아님 · 우리 DFT (E 22.06 · B₀ 26.23 · ν 0.360) 와 나란히 | LPSCl 실측 아님 · 소성 값 0 |
| **단계 5** (3D 복합 압밀) | 제조 조건 = CAM : β-Li₃PS₄ 70 : 30 wt · 35 kN ≈ 445 MPa · 운전 ≈ 70 MPa (p.2153) — 압밀 결과 (두께 · 기공) 는 없음 | 결과 전 대조 숫자 없음 |
| **단계 6** (탈압 · 되돌아옴) | ★ 실험 쪽에서 가져올 **꼴**: ① 고정 변위 틀 응력 이완 ≈ 4–5 % / 15 h 는 틀 (PEEK) 몫이 크다 → 탈압 · 유지 실험은 **빈 틀 기준선** 을 같이 잰다 (그림 S5) ② 사이클 응력은 스택의 ≈ 0.1 % (CAM/LTO) — 탈압 계산에서 사이클 효과와 섞지 않는다 ③ [카드 산술 · 원문 아님] 표 1 Li₆PS₅X 상수로 **치밀체** 일축 변형 (다이 안) 탈압 되돌아옴 상한 = σ/M, M = E(1 − ν)/((1 + ν)(1 − 2ν)) → 300 MPa 에서 **≈ 0.68–0.77 %** (E 30 · ν 0.33 → M 44.4 GPa · E 22 · ν 0.37 → M 38.9 GPa) · 우리 MPM (E 1.53 · ν 0.49) M = K + 4μ/3 = 26.2 GPa → **≈ 1.15 %** — 기공 있는 성형체는 더 무르다 (더 크게 되돌아옴) · DEM 은 접촉망 강성이 정하므로 이 식으로 못 센다 | 이 논문 자체의 탈압 값 0 · LPSCl 탄성은 이론값 · 다공체 아님 |
| **단계 7** (형상 · 피복 · 수송) | 섞기 양극은 사이클 뒤 접촉 보존 (그림 S7) ↔ 단일 NCM 은 수축 · 틈 (그림 S8) — 정성 · *"the "softness" of a SE influences the intrinsic ionic transport itself … the pressure influence on the ion transport in soft materials is still unknown"* (p.2149) | 정량 피복 · 수송 없음 |
| **후보 D0** (지금 DEM) | 사이클 기하 입력 (ΔV) 의 출처 계열 (그림 2a) · ★ 고유변형 응력은 **변형 제어** → 응력 ∝ K: 같은 ε_vol 에서 우리 DEM 의 연화 강성 (E 1.35) 은 실물 K (28–30) 대비 응력을 **≈ 20 배 넘게 작게** 낸다 [카드 산술: E 1.35 · ν 0.3 → K 1.1 GPa] — 사이클 응력을 DEM 에서 읽지 않는다 (benhadjali2026 EM-01 과 같은 결론 [다른 카드]) | DEM 계산 없음 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 경계조건 본보기: 옆 · 바닥 구속 + 위 자유 (그림 S3) · 바닥 센서 = 판 반력 (우리 `wallP`) | 벽 마찰 · 미끄럼 없음 |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | **R1** 의 실험 쪽 문장: *"only if the applied pressure is transferred completely to the LCO, the OCV will reflect the full pressure"* (p.2147) — AM 이 받는 압력 몫이 OCV 에 들어간다 (In 반응 부피 +50 % 과대의 한 원인으로 제시) | 하중 몫 숫자 없음 |
| **후보 B** (입자별 FE + 접촉) | 동기 문장만 (*"advanced computational models"* · Christensen–Newman 응력 모델 [67, 68]) | 없음 |
| **후보 C · C′** (큰 변형 · 항복 캡 접촉 DEM) | 없음 | — |
| **후보 M0** (균질화) | ★ Reuss 직렬 균질화 (식 S8 · S9) = M0 꼴의 **탄성** 판 — E_cathode 50.4 · E_cell 30.2 · K 21.8 GPa · 맞춘 값 0 개 | 소성 · 캡 · Heckel 없음 |
| **U0–U6** | 직접 해당 없음 · 덧붙일 해석 시험 = 단계 2 줄 (식 S6 · S10 · S11) | — |
| **R1–R7** | **R1** (위 A 줄 · 정성) · **R4** (탈압 = 없음 · 고정 변위 이완 = 틀 몫 · §3-7) · **R5** (그들 모델 맞춘 값 0 · 입력 = 표 1 + XRD) · **R6** (SE *"elastic and plastic deformation"* 정성) · **R7** (이방 부피 변화 → 2 차 입자 균열 · refs 7, 25–29 · 정성) | R2 · R3 없음 |
| **결과 전 대조 항목** | ① 고정 틀 (≈ 60 MPa) 에서 CAM 만의 사이클 응력 변화 ≈ 0.05–0.07 MPa (NCM-811 음 · LCO 양) · Li 음극 ≈ 1.5 MPa [판독] — 우리가 구속 RVE 사이클 응력을 계산하게 되면 자릿수 대조 ② NCM-811 ΔV 는 창에 따라 −1 ~ −6.5 % (그림 2a) — 사이클 계산 결과를 낼 때 **어느 x 창의 ΔV 인지** 를 결과 전에 적는다 ③ 탈압 되돌아옴 상한 (치밀 탄성) ≈ 0.7–0.8 % @ 300 MPa [카드 산술] — 계산이 그보다 훨씬 크면 다공 · 접촉망 효과 (또는 연화) 몫 | β-Li₃PS₄ · 문헌 XRD · 판독 · 카드 산술 — 우리 랩 표준 (10–13 % · 1.64) 과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: SE (β-Li₃PS₄ · LGPS ↔ LPSCl) · CAM (NCM-811 은 같으나 코팅 · 입경 [미확인]) · 조성 (70 : 30 wt) · 제조 445 MPa ↔ 우리 300 MPa · 측정 = 고정 틀 축 응력 ↔ 우리 = 압밀 · 수송 계산 · 모델 0D/1D ↔ 우리 3D 입자.

## 9. 적용 인사이트 (행동)
1. **사이클 ΔV 를 쓸 때 창을 같이 적는다 (흐름 밖: A10 · A-1)**: "NCM-811 −6 % (4.3 V, 문헌 XRD) ↔ 같은 논문 ASSB 셀이 간 창 x 0.85 → 0.53 (그림 2a 로 ≈ −1 %)" — 우리 `--dv-pct 5.1` · `--cycle-dv-sc −0.051` 의 help 에 "어느 x 창 · 어느 셀" 인지 칸이 없다 (메인 세션 판단 · 코드 고침 아님).
2. **고유변형 응력 해석 시험 (단계 2 · U)**: 식 S6 (완전 구속 p = 3Kε₀) · S10 · S11 (옆 구속) 을 MPM 단위 시험 후보로 — AM 고유변형을 구성식에 넣게 되면 결과 전에 해석해를 적어 둔다.
3. **탈압 · 유지 실험 · 계산의 기준선 (단계 6 · R4)**: 고정 변위 응력 이완은 틀 몫이 크다 (그림 S5) — 실험 대조를 받을 때 "빈 틀 기준선을 뺐나" 칸 · 우리 `hold` 의 정착과 같은 표에 두지 않는다.
4. **인용 한정 (b)**: "탈압 이완" 근거로 이 논문을 쓰지 않는다 — 쓸 수 있는 문장은 *"plastic deformation is slow and perhaps not effective enough"* · re-tightening (Tian & Qi 계산 인용) · 수축 → 접촉 손실 (그림 S8 · 정성).
5. **단위 (단계 0)**: 문헌 응력은 축 단위로 다시 읽는다 — 이 논문 본문 *"+0.6 MPa"* 는 0.06 MPa.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Koerver et al. compiled operando-XRD unit-cell volume changes of layered cathodes: the volume contraction on delithiation grows with Ni content, reaching about −6.5 % for NCM-811 at x(Li) ≈ 0.15 (read from their Fig. 2a), while LiCoO₂ expands by roughly +2 % (*Energy Environ. Sci.* 11 (2018) 2142)."
- "In a volume-constrained solid-state cell (β-Li₃PS₄ separator, ~60 MPa initial stack pressure), the cathode volume change alone changed the axial stress by only ~0.6 × 10⁵ Pa (LCO/LTO, compressive) or a similar tensile amount (NCM-811/LTO), whereas lithium-metal or graphite anodes raised it by an order of magnitude more."
- "The authors note that plastic effects were ignored in their estimates and that 'plastic deformation is slow and perhaps not effective enough', so stress changes will always occur in solid-state batteries."
- 국문 (한정어와 함께): *"Koerver 2018 의 구속 셀 (β-Li₃PS₄ · 고정 틀 ≈ 60 MPa) 에서 CAM 만의 사이클 응력 변화는 ≈ 0.06 MPa 자릿수였고 (그림 축 10⁵ Pa · 본문 'MPa' 표기는 10 배 어긋남) · NCM-811 의 −6 % 는 4.3 V 문헌 XRD 값이다 — 그 셀이 실제로 간 x 창 (≈ 0.85 → 0.53) 에서는 그림 2a 로 ≈ −1 % 다."*

## 11. 주의/한계 (over-claim 방지)
1. **우리 계가 아니다** — β-Li₃PS₄ · LGPS SE.  LPSCl 은 표 1 이론 탄성 한 줄뿐.
2. **그림 2a 는 문헌 모음** (refs 35–37 · 파우치 셀) — NCM 원전 인용은 de Biasi 2017 · Kondrakov 2017 로.
3. **탈압 실험 없음** — "가압 해제 이완" 근거로 쓰지 않는다 (§3-7).
4. **응력 = 축 성분 하나 · 고정 변위 틀** — 옆 응력 · 정수압은 계산값 · 기준선은 손으로.
5. **원문 안 어긋남 13 건** (§3-9) — 특히 σ₁₁ 단위 (10 배) · 표 S4 부호 · 배수 순서 · 초록 OCV 기울기.
6. **반복 · 오차 없음** (그림 3 OCV 기울기 오차만) · 입경 · 기공 · 코팅 두께 [미확인].
7. **"모델-실험 일치"** 는 측정 σ₁₁ 을 입력으로 쓴 두 추정 사이의 말이다 [카드 해석].

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 11 | W. Zhang, D. Schröder, T. Arlt, I. Manke, R. Koerver, R. Pinedo, D. A. Weber, J. Sann, W. G. Zeier and J. Janek, (Electro)Chemical Expansion during Cycling: Monitoring the Pressure Changes in Operating Solid-State Lithium Batteries, J. Mater. Chem. A, 2017, 5, 9929–9936. | 같은 장치의 첫 보고 · 그림 4a LCO 자료 원전 · In/InLi 7.89 — 질문 b · j · 카드 없음 |
| 30 | H.-K. Tian and Y. Qi, Simulation of the Effect of Contact Area Loss in All-Solid-State Li-Ion Batteries, J. Electrochem. Soc., 2017, 164, E3512–E3521. | *"re-tightening a cell is not sufficient"* 의 원전 (접촉 면적 손실 계산) — 질문 b · 단계 6 · 카드 없음 (정본 `tian2020_electrochemo_mechanical_stress_assb` 는 다른 논문) |
| 37 | L. de Biasi, A. O. Kondrakov, H. Geßwein, T. Brezesinski, P. Hartmann and J. Janek, Between Scylla and Charybdis: Balancing Among Structural Stability and Energy Density of Layered NCM Cathode Materials for Advanced Lithium-Ion Batteries, J. Phys. Chem. C, 2017, 121, 26163–26171. | 그림 2a NCM 계열 · ESI 의 NCM-811 −6 % (4.3 V) 원전 — 우리 `--cycle-dv-*` 대조 · 카드 없음 |
| 35 | A. O. Kondrakov, A. Schmidt, J. Xu, H. Geßwein, R. Mönig, P. Hartmann, H. Sommer, T. Brezesinski and J. Janek, On the Anisotropic Lattice Strain and Mechanical Degradation of High- and Low-Nickel NCM Cathode Materials for Li-Ion Batteries, J. Phys. Chem. C, 2017, 121, 3286–3294. | 우리 `--dv-pct 5.1` · `--cycle-dv-sc −0.051` help 의 원전 (*"Kondrakov 2017 NMC811 3.0–4.3V"*) — 값 확인 · 카드 없음 |
| 8 | R. Koerver, I. Aygün, T. Leichtweiß, C. Dietrich, W. Zhang, J. O. Binder, P. Hartmann, W. G. Zeier and J. Janek, Capacity Fade in Solid-State Batteries: Interphase Formation and Chemomechanical Processes in Nickel-Rich Layered Oxide Cathodes and Lithium Thiophosphate Solid Electrolytes, Chem. Mater., 2017, 29, 5574–5582. | 그림 S8 (수축 → 접촉 손실) 원전 — 질문 b · R4 · 카드 없음 |
| 80 | E. J. Cheng, K. Hong, N. J. Taylor, H. Choe, J. Wolfenstine and J. Sakamoto, Mechanical and Physical Properties of LiNi0.33Mn0.33Co0.33O2 (NMC), J. Eur. Ceram. Soc., 2017, 37, 3213–3217. | 표 1 NCM-111 E 199 GPa 의 원전 — 우리 AM E 140 GPa (출처 철회 이력) 옆에 놓을 실측 · 카드 없음 (sakka2022 카드도 후보로 적음) |
| 34 | G. Bucci, T. Swamy, Y.-M. Chiang and W. C. Carter, Modeling of Internal Mechanical Failure of All-Solid-State Batteries during Electrochemical Cycling, and Implications for Battery Design, J. Mater. Chem. A, 2017, 5, 19422–19430. | 카드 = `bucci2017_chemomech_failure_assb_cycling_czm` |
| 33 | A. Sakuda, A. Hayashi and M. Tatsumisago, Sulfide Solid Electrolyte with Favorable Mechanical Property for All-Solid-State Lithium Battery, Sci. Rep., 2013, 3, 2261. | 카드 = `sakuda2013_sulfide_mechanical_property` |
| 89 | Z. Deng, Z. Wang, I.-H. Chu, J. Luo and S. P. Ong, Elastic Properties of Alkali Superionic Conductor Electrolytes from First Principles Calculations, J. Electrochem. Soc., 2016, 163, A67–A74. | 표 1 Li₆PS₅X 줄 원전 — 카드 = `deng2016_elastic_superionic_electrolytes_dft` |
| 105 | A. Reuss, Berechnung Der Fließgrenze von Mischkristallen Auf Grund Der Plastizitätsbedingung Für Einkristalle, ZAMM, 1929, 9, 49–58. | Reuss 균질화 원전 (M0 꼴) — 카드 없음 (우선 낮음) |

## 13. [미확인] 목록 (본문 17 쪽 + ESI 10 쪽 전수에 없음)
1. **압력 해제 (탈압) 측정** — 두께 · 부피 되돌아옴 · 접촉 · OCV 내림 쪽 · 제조 445 → 70 MPa 사이의 변화.
2. 셀 지름 (인쇄 없음 · 카드 산술 ≈ 10 mm) · 가압 시간 · 속도 · 펠릿 두께 (분리막 "≈ 400 µm" 만) · 기공 · 진밀도.
3. CAM 입경 · LCO 코팅 두께 · β-Li₃PS₄ 결정상 · σ.
4. 반복 셀 수 · 응력 오차 · 기준선 그리는 규칙.
5. 그림 2a 의 NCM 각 계열이 어느 참고문헌 (35 · 36 · 37) 의 어느 셀에서 왔는지 · 격자 상수 a · c 값.
6. 표 S3 의 K (재현 안 됨) · 표 S4 의 ε₀ 값 · "eq. a1" (표 1 각주 ᵇ).
7. 다섯째 압력 (2.8 t) 의 MPa 값.
8. 저자 기여 문단.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 본문 17 쪽 · ESI 10 쪽을 글자 층 (pdftotext raw · layout · PyMuPDF) 으로 전부 읽고 렌더로 확인 — 마이너스 부호 (LTO · LFP · NCM ΔV · −659 bar · −427 bar) 와 식 (11) 의 부호는 렌더로만 보인다 (글자 층은 'Dp = evolK').  서지 = PDF 1 쪽 (제목 · 저자 · 소속 · Cite this · 접수 / 승인 · DOI · *"Published on 29 May 2018"*) + PDF 메타데이터 Subject 줄 + 쪽 머리글.
- 그림 크롭 **72 장** = 도구 15 (본문 그림 1–5 · 표 1 · SI 그림 S1–S8 · 표 S2) 중 **다시 자름 13** (f1 · f3 회색 그림 괘선 · f2 · f4 · f5 쪽 전체 폭 → 래스터 + 3 pt · fS1 패널 b x 축 제목 잘림 · fS2 표 S2 섞임 + 아래 잘림 · fS3 '1' 방향 화살표 잘림 · fS5 표 S4 섞임 + x 축 잘림 · fS6 · fS7 · fS8 아래 잘림 · t1 각주 빠짐) + **캡션만 고침 1** (tS2) + **그대로 1** (fS4) · 도구가 못 낸 **표 S1 · S3 · S4 손 크롭** (S1 = 번호 공백 · S3 = 본문 참조를 후보로 잡고 0 개 · S4 = fS5 에 섞여 있었음) · 손 크롭 **57** (패널 10 = 2a 2b · 4a–4d · S1a S1b · S6a S6b · 표 3 · 식 23 = 본문 (1)–(12) · ESI (S1)–(S11) · 근거 문단 21 (본문 17 · ESI 4)) — 본 뒤 다시 자름 2 (txt_p1 오른쪽 잘림 · txt_p11 두째 조각이 그림 5 아래 + 캡션을 담음 → 오른쪽 단 글 시작 303 pt 로).  72 장 전부 열어 확인.
- 판독: 본문 그림은 모두 300 dpi 래스터 한 장씩 · ESI 그림 S1 · S2 · S5 · S6 · S7 · S8 은 279–686 dpi 래스터 (S1 · S6 · S7 · S8 은 소프트 마스크) · S3 · S4 는 벡터.  재현 확인: 표 S2 의 두 V̄ 열 = 7.89 · 11.81 − (−F ∂E/∂p) 다섯 줄 모두 · Reuss 50.4 · 30.2 · 21.8 · 표 S4 LCO p_R · 그림 2a 판독 끝점이 본문 *"roughly +2%"* (LCO) · 표 S3 −6.0 % (NCM-811) 와 같은 자릿수 · 그림 S5 힘 축 ↔ 응력 축 = 지름 10 mm.
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 + DOI (C8EE00907D) · "Koerver" · 제목 낱말 grep — 이 논문 카드 없음 (jung2019 [29] · benhadjali2026 [3] · barai2021 [36] · doerrer2021 [14] · tian2020 [4] · park2025 [31] · nolan2018 [156] 에 인용만).

## 🔗 관련 카드
- 이 논문을 인용한 정본 카드: `jung2019_cathode_electrolyte_chemical_reaction_sulfide_assb` · `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` · `barai2021_delamination_cathode_llzo_multiscale` · `doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density` · `tian2020_electrochemo_mechanical_stress_assb` · `park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics` · `nolan2018_computation_accelerated_design_review`.
- 화학-기계 · 사이클 응력: `bucci2017_chemomech_failure_assb_cycling_czm` · `kim2023_chemomech_failure_highstrain_anode` · `lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging` · `kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review`.
- 탄성 상수: `deng2016_elastic_superionic_electrolytes_dft` · `sakuda2013_sulfide_mechanical_property`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
