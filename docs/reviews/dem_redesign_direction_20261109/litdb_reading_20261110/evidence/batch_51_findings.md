# 배치 51 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-12)

카드 = `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` (원문 = 출판본 17 쪽 + ESI 10 쪽 · 그림 크롭 72 장 = 도구 15 (다시 자름 13 · 캡션 고침 1 · 그대로 1) +
손 크롭 57 (패널 10 · 표 3 · 식 23 · 근거 문단 21 · 본 뒤 다시 렌더 2) · 판독 원자료 `litdb/figures/<slug>/digitized.csv` 201 행 — 그림 2 · S5 는 원본 래스터 눈금 보정 · 그림 4 · 5 · S1 · S6 은 눈대중).
서지 (k · l 인용용) = Koerver R., Zhang W., de Biasi L., Schweidler S., Kondrakov A. O., Kolling S., Brezesinski T., Hartmann P., Zeier W. G., Janek J.,
*Chemo-mechanical expansion of lithium electrode materials – on the route to mechanically optimized all-solid-state batteries*, Energy Environ. Sci. 11, 2142–2158 (2018), DOI 10.1039/C8EE00907D.
⚠ 재료 = SE **β-Li₃PS₄** (응력 셀) · **LGPS** (OCV 셀) · CAM NCM-811 · NCA · LCO — LPSCl 은 표 1 이론 탄성 (Deng 2016) 한 줄뿐 · DEM · MPM · 압밀 시뮬레이션 없음 (0D/1D 선형 탄성 추정) · 탈압 실험 없음.
쪽 = 인쇄 쪽 p.2142–2158 (PDF 쪽 = 인쇄 − 2141) · ESI = S1–S10.  ⚠ 글자 층이 마이너스 부호를 잃는다 (LTO −0.2 % · LFP −7 % · −659 · −427 bar · NCM −6 %) — 부호는 렌더로 확인.

---

## a — 순수 SE 압력별 기공 곡선 · 진밀도 · 상태

- [a] koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb | **없음** — 기공 · 진밀도 · 압력별 밀도 곡선 없음 · 분리막 β-Li₃PS₄ 60 mg ≈ 400 µm (지름 ≈ 10 mm [카드 산술: 35 kN ÷ 445 MPa]) → 겉보기 밀도 1.91 g/cm³ [카드 산술] — β-Li₃PS₄ 진밀도 [미확인] 이라 기공률로 못 바꿈 | 카드 §3-1 · 원문 p.2153 | [인쇄] · [카드 산술] · [미확인] | β-Li₃PS₄ · LPSCl 아님

## b — 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] koerver2018_… | **탈압 (가압 해제) 측정 없음** — 제조 35 kN ≈ 445 MPa → 운전 ≈ 70 MPa (p.2153) 와 OCV 시험의 2.8 t → 0.5 t 되돌림 (p.2153 · *"The pressure was set to 0.5t during charge"* [카드 해석]) 사이의 두께 · 접촉 · OCV 되돌아옴 보고 없음 | 카드 §3-7 · §0-1 · 원문 p.2153 | [인쇄] · [미확인] | —
- [b] koerver2018_… | 있는 것 = **고정 변위 틀의 응력 이완** (그림 S5): 셀 (InLi | SE | NCM-811/SE) 5.128 → 4.894 kN = **65.2 → 62.3 MPa** (0.5 → 15.5 h OCV 대기 · −4.6 %) · 빈 틀 5.119 → 4.913 kN = 65.1 → 62.5 MPa (0.2 → 15.5 h) → 61.7 MPa (62 h) — 저자 = *"mechanical drift of an empty cell casing due to the plastic insulators"* → 기준선으로 빼 버림 (*"The obtained stress is corrected by the materials mechanical relaxation"* p.2149 · *"kept at OCV for 20 h prior to cycling to minimize drifts arising from the cell casing"* p.2153) · 측정법 = 바닥 힘 센서 KMT 55 + 10 Nm 조임 (≈ 60 ± 8 MPa) | 카드 §3-5 · §3-7 · 그림 S5 · S2 | [판독 원본 래스터 535 dpi] · [인쇄] | 틀 (PEEK) 몫 · 전극 되돌아옴 아님 · 사이클 중 골이 빈 틀보다 −0.023 kN (≈ −0.3 MPa) 더 내려감 [카드 산술 · 원문 해석 없음]
- [b] koerver2018_… | 접촉 손실 (정성): *"The NCM particles contract during delithiation and lose contact with the SE"* (ESI 그림 S8 · Koerver 2017 재게재 · 사이클 유발) · *"re-tightening a cell is not sufficient to recover capacity fade due to contact loss of materials"* (p.2151 · Tian & Qi 2017 계산 인용) | 카드 §3-7 · 원문 p.2151 · S8 | [인쇄] | 값 없음 · 탈압 유발 아님

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] koerver2018_… | **항복 · 경도 · 크리프 값 없음** — 표 1 탄성 상수만: Li₆PS₅X **E 22–30 · ν 0.33–0.37 · G 8–11 · K 28–30 GPa** (이론 · S. P. Ong [89] = Deng 2016) · β-Li₃PS₄ E 28.9 · ν 0.27 · K 21.4 (이론) · LGPS 37.2 · NCM-111 **199.0 GPa** · ν 0.25 (Cheng 2017 [80] · 이론 표지 없음) · LCO 191 · 본문 *"Thiophosphate-based SEs … quite elastic (K/G > 1.75)"* (Pugh) — 일축 항복 환산 없음 | 카드 §3-8 · 원문 p.2148–2149 · 표 1 | [인쇄] | 탄성만 · 표 1 인쇄 G 가 E · ν 와 조금씩 안 맞음 (Li 4.2 ↔ 1.7 [카드 산술])

## d — 단단한 입자 + 무른 입자 혼합 압축의 하중 몫 · 재밍

- [d] koerver2018_… | 하중 몫 숫자 없음 · 정성: *"only if the applied pressure is transferred completely to the LCO, the OCV will reflect the full pressure. Thus, non-isochoric plastic deformation as well as the porosity of the SE may influence the OCV measurement under pressure"* (p.2147) — In 반응 부피가 OCV 로 +11.81 ↔ 결정학 +7.89 cm³/mol (+50 %) 인 한 원인으로 제시 · Reuss 모델은 CAM : SE 1 : 1 (vol) 직렬 = 같은 응력 가정 (하중 몫 개념 없음) | 카드 §3-4 · §3-6 · §8 후보 A | [인쇄] | 재밍 · 압축 계산 없음

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위 · 대안

- 이 배치에 없음 (접촉 법칙 · DEM 없음 — 모델은 0D/1D 균질 선형 탄성)

## f — MPM 접촉 · 다물체 · 강체 결합 · 해상도 규칙

- 이 배치에 없음 (MPM 없음).  단 MPM 단위 시험 후보가 될 해석해 = 완전 구속 블록의 고유변형 정수압 **p = 3Kε₀** (식 S6 · S7) · 옆 구속 σ₁₁ = 3K((1 − ν)/(1 + ν) ε₁₁ − ε₀) · σ₂₂ = 3K(ν/(1 + ν) ε₁₁ − ε₀) (식 S10 · S11) — 카드 §3-6 · §8 단계 2 · [인쇄] ESI p.S5–S6

## g — 2D → 3D 전이 경고 · 증거

- [g] koerver2018_… | 모델 = *"a simplified (cylindrical) 3D model of a single electrode cell"* (그림 S3 · 지름 1 cm · 높이 500 µm · 양극층 50 µm) 을 **1D 직렬 스프링** 으로 균질화 (그림 S4) · *"The experimental values can very well be used as a basis for a more sophisticated 3D approximation"* (p.2151) · 2D ↔ 3D 비교 말 없음 | 카드 §4-3 ③ | [인쇄] | 0D/1D ↔ 3D 이지 2D ↔ 3D 아님

## h — DEM 에서 FE · MPM 으로 넘긴 선례 · 시점

- 이 배치에 없음 (DEM · FE 계산 없음 · 결론에 *"advanced computational models"* 요청만 p.2152)

## i — 복합 양극 (AM + SE) 의 압력별 기공

- [i] koerver2018_… | **없음** — 양극 = CAM : β-Li₃PS₄ **70 : 30 wt** (섞기 38 : 32 : 30) · 12 mg · 35 kN ≈ 445 MPa 성형 · 기공 · 두께 미보고 · 저자 제안 *"Good SSBs may require a minimum porosity in the electrode composites to avoid too strong changes in stress"* (p.2151 · 값 없음) | 카드 §3-1 · §3-7 | [인쇄] · [미확인] | —

## j — 카드가 스스로 적은 한계 중 가압 · 탈압과 닿는 것

- [j] koerver2018_… | 소성 무시: *"(and plasticity; here ignored in the estimates)"* (p.2149) · *"however, plasticity, deformation or combinatory effects of the electrode materials are neglected. In particular, plasticity of the solid–electrolyte has to be considered in future studies"* (p.2152) · 완전 구속 아님: *"besides not being perfectly constrained, plastic effects will consume some of the locally developed stress"* (p.2151) · 압력 일축 · 불균일 · CAM 방향 무작위 아님 (p.2147) · 이방성 · 불균일 응력장 무시 (p.2143) · 응력 응답은 SE · 전극 조합 · 미세구조 · 공정 · 균질도마다 고유 (p.2152) | 카드 §0 ⑥ · §4-3 | [인쇄] | —
- [j] koerver2018_… | 원문 안 어긋남 13 건 (카드 §3-9) — σ₁₁ 단위 (본문 *"+0.6 MPa"* ↔ 그림 축 10⁵ Pa · 표 S4 −0.06 MPa = 10 배) · 표 S4 NCM σ₂₂ 부호 · *"ten- to twenty-fold, respectively"* 순서 (판독 Li ≈ 25–30 배 · 흑연 ≈ 12 배) · 초록 *"1 mV/100 MPa"* ↔ 0.122 mV/MPa · 압력 하중 다섯 ↔ MPa 넷 · 그림 S3 캡션 1000 µm ↔ 1 cm · OCV 대기 20 h ↔ ≈ 16 h | 카드 §3-9 | [인쇄] · [판독] · [카드 산술] | —

## k — DEM 의 한계 (인용할 서지 = Koerver et al. 2018, Energy Environ. Sci. 11, 2142)

- [k] koerver2018_… (Koerver et al., *Energy Environ. Sci.* 2018) | **말 없음** — DEM · discrete element · particle simulation 낱말 0 회.  모델 일반의 한계 문장만: *"The formal treatment is restricted to a relatively simple macroscopic picture, as any more detailed treatment will require numerical methods."* (p.2143) · *"For the sake of simplicity, we neglect the anisotropy of the materials and inhomogeneous stress fields"* (p.2143) | 카드 §4-3 ① | [인쇄] | DEM 한계 근거로 인용 불가

## l — 소성변형이 왜 어려운가 · 우회 · 값 · 비용 (인용할 서지 = Koerver et al. 2018, Energy Environ. Sci. 11, 2142)

- [l] koerver2018_… (Koerver et al., *Energy Environ. Sci.* 2018) | 이유는 적지 않고 **무시했다 · 앞으로 고려해야** 라고 적는다: *"the elasticity (and plasticity; here ignored in the estimates) of the cell. The measured pressure can be compared to the calculated (estimated) data and used to judge the plastic flow in the battery experimentally."* (p.2149) · *"In particular, plasticity of the solid–electrolyte has to be considered in future studies, as this component needs to compensate volume changes of the electrode materials."* (p.2152) · 시간 · 효과: *"Pore-filling due to volume changes of electrode materials and plastic deformation of SE and electrodes will never work perfectly, as plastic deformation is slow and perhaps not effective enough. Therefore, stress changes will always occur."* (p.2151) · 되돌릴 수 있음: *"An important aspect is the reversibility of the deformation to avoid dead space and high internal transfer resistances by cracks and voids"* (p.2152) | 카드 §3-7 · §4-3 ② | [인쇄] | 우회 = SE 를 모든 면 구속 *"fluid"* 처럼 (*"due to the sufficient elasticity of the solid electrolyte it behaves like a fluid in a system, which is constrained on all sides"* · ESI p.S4) · Δp = −ε_vol K · Reuss 직렬 (E_cell 30.2 · K 21.8 GPa) · **맞춘 값 0 개** (입력 = 표 1 + XRD ΔV + 측정 σ₁₁) · 계산 비용 0 (손 계산) · 검증 = p_R ↔ p_L 두 추정 사이 (≈ 65–69 %) [카드 해석]

## m — 받아들일 통찰

- [m] koerver2018_… | **사이클 ΔV 는 x 창과 같이 적는다** — 같은 논문 안에서 NCM-811 이 −6 % (ESI · 4.3 V 문헌 XRD) · −6.5 % (그림 2a 끝 x ≈ 0.15) 인데 그 논문의 ASSB 셀은 x 0.85 → ≈ 0.53 (그림 4b) 까지만 가서 그 창의 ΔV 는 ≈ −1 % [판독] | 흐름 밖: 사이클 원장 `--dv-pct 5.1` · `--cycle-dv-sc −0.051` 입력 표기 (help 에 창 칸 없음) | 카드 §3-2 · §7-2
- [m] koerver2018_… | **고정 변위 응력 이완 = 틀 몫부터 따로** — 빈 틀만으로 15.5 h 에 ≈ 4 % (≈ 65 → 62.5 MPa) 떨어진다 (그림 S5) → 탈압 · 유지 실험 대조를 받을 때 '빈 틀 기준선' 칸 · 우리 MPM `hold` 정착과 같은 표에 넣지 않는다 | 단계 6 · 조건 R4 · 결과 전 대조 항목 | 카드 §3-5 · §3-7 · §8
- [m] koerver2018_… | **고유변형 응력 해석해를 단위 시험으로** — 완전 구속 p = 3Kε₀ (식 S6) · 옆 구속 σ₁₁ · σ₂₂ (식 S10 · S11) — AM 부피 변화를 MPM 구성식에 고유변형으로 넣게 되면 결과 전에 적어 둘 해석해 · 같은 ε 에서 σ ∝ K → DEM 연화 강성 (E 1.35 → K ≈ 1.1 GPa) 은 실물 K 28–30 대비 응력을 ≈ 20 배 넘게 작게 낸다 [카드 산술] | 단계 2 · U (덧붙임) · 후보 D0 | 카드 §3-6 · §8
- [m] koerver2018_… | **문헌 응력 단위 함정** — 본문 *"+0.6 MPa"* ↔ 그림 축 *"σ₁₁ / 10⁵ Pa"* (= 0.06 MPa) · 힘을 MPa 로 (*"a force of 60 ± 8 MPa"*) · 하중 t ↔ MPa 목록 결손 → 문헌 압력 인용에 '힘 · 면적 · 배수' 칸 | 단계 0 | 카드 §3-9 ①⑤

## n — 논문 에이전트 후보 (원문 참고문헌 목록 서지 그대로 · litdb 확인 = 정본 `litdb/papers/` 파일 목록 + 저자 · 권호 grep)

- [n] W. Zhang, D. Schröder, T. Arlt, I. Manke, R. Koerver, R. Pinedo, D. A. Weber, J. Sann, W. G. Zeier and J. Janek, (Electro)Chemical Expansion during Cycling: Monitoring the Pressure Changes in Operating Solid-State Lithium Batteries, J. Mater. Chem. A, 2017, 5, 9929–9936. (ref 11) | b · j — 같은 operando 압력 장치의 첫 보고 · 그림 4a LCO 응력 자료 원전 · In/InLi 반응 부피 7.89 — 기준선 · 이완 처리 원 설명이 있을 수 있음 | 카드 §12 · §3-5 | litdb 확인: 파일 없음 · "9929" 언급 3 카드 (카드 아님)
- [n] H.-K. Tian and Y. Qi, Simulation of the Effect of Contact Area Loss in All-Solid-State Li-Ion Batteries, J. Electrochem. Soc., 2017, 164, E3512–E3521. (ref 30) | b · 단계 6 · R4 — *"re-tightening a cell is not sufficient to recover capacity fade due to contact loss"* 의 원전 (접촉 면적 손실 계산) | 카드 §3-7 ③ · §12 | litdb 확인: 파일 없음 (정본 `tian2020_electrochemo_mechanical_stress_assb` 는 다른 논문) · "E3512" 언급 1
- [n] L. de Biasi, A. O. Kondrakov, H. Geßwein, T. Brezesinski, P. Hartmann and J. Janek, Between Scylla and Charybdis: Balancing Among Structural Stability and Energy Density of Layered NCM Cathode Materials for Advanced Lithium-Ion Batteries, J. Phys. Chem. C, 2017, 121, 26163–26171. (ref 37 · ESI ref 2) | 흐름 밖 (사이클 ΔV) · j — 그림 2a NCM 계열 · ESI NCM-811 −6 % (4.3 V) 의 원전 → 우리 `--cycle-dv-*` 대조 · benhadjali2026 NMC622 ΔV 의 측정 원전 | 카드 §0-1 · §7-2 · §12 | litdb 확인: 파일 없음 · "Scylla" 언급 1
- [n] A. O. Kondrakov, A. Schmidt, J. Xu, H. Geßwein, R. Mönig, P. Hartmann, H. Sommer, T. Brezesinski and J. Janek, On the Anisotropic Lattice Strain and Mechanical Degradation of High- and Low-Nickel NCM Cathode Materials for Li-Ion Batteries, J. Phys. Chem. C, 2017, 121, 3286–3294. (ref 35) | 흐름 밖 (사이클 ΔV) · R7 — 우리 `--dv-pct 5.1` · `--cycle-dv-sc −0.051` help 글의 원전 (*"Kondrakov 2017 NMC811 3.0–4.3V"*) · 이 논문은 5.1 을 인쇄하지 않는다 → 값 확인 | 카드 §7-2 · §12 | litdb 확인: 파일 없음 · "Kondrakov" 언급 5 카드
- [n] R. Koerver, I. Aygün, T. Leichtweiß, C. Dietrich, W. Zhang, J. O. Binder, P. Hartmann, W. G. Zeier and J. Janek, Capacity Fade in Solid-State Batteries: Interphase Formation and Chemomechanical Processes in Nickel-Rich Layered Oxide Cathodes and Lithium Thiophosphate Solid Electrolytes, Chem. Mater., 2017, 29, 5574–5582. (ref 8) | b · R4 · R7 — 그림 S8 (NCM 수축 → SE 와 떨어짐) 원전 · 접촉 손실의 사이클 관측 | 카드 §3-7 ② · §12 | litdb 확인: 파일 없음 · "5574" 언급 6 카드 (jung2019 L440 · tian2020 L605 등 인용만)

## 카드 문제

- `jung2019_cathode_electrolyte_chemical_reaction_sulfide_assb` L280 — *"무가압 in situ SEM 으로 균열 생성 확인 (가압 해제 이완 [29] 을 배제하려는 시도)"* 의 [29] = 이 논문인데, 이 논문에는 **가압 해제 (pressure release) 이완** 을 다룬 문장 · 값이 없다 (본문 17 쪽 + ESI 전수 · 'release' 는 *"stress release of the active materials"* 한 번) · 가장 가까운 것 = 고정 틀 응력 이완 보정 (p.2149) · NCM 수축 → 접촉 손실 (그림 S8) — jung2019 카드에 Jung 2019 원문 영어 문장이 없어 어느 쪽인지 [미확인] → jung2019 원문 확인 필요 (고치지 않음).
- `doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density` L309 — *"전극 부피 변화 (LTO 0.2 %)"* ↔ 원문 *"−0.2% upon delithiation"* (부호 빠짐 — 글자 층이 '−' 를 잃는 자리).
- `barai2021_delamination_cathode_llzo_multiscale` L19 · L130 · L687 — V̄ 의 *"실험 원전"* 으로 이 논문을 적었으나, 이 논문의 NCM V̄ 는 refs 35–37 의 결정학 자료를 모은 **2 차** 이고 표가 없다 (그림 2b 곡선뿐) → *"원데이터가 필요"* 는 refs 35–37 에서 찾아야 한다.  barai L218 의 판독 (≈ 3 · 8 · 15.5 cm³/mol @ x 0.47 · 0.32 · 0.26) 은 이 논문 그림 2b NCM-811 판독 (≈ 3.0 · 9.0 · 17.1) 과 같은 자릿수 [판독 ±0.5–1].
- 정본 INDEX_DEM.md 의 sedlatschek2026 줄과 이 카드 §7-1 이 우리 DEM AM E 140 GPa (출처 철회 이력 · CLAUDE.md 규율 ⑥) 옆에 NMC811 실측 (138 ± 24 · 165 ± 7 GPa) 을 같이 두게 됐다 — 정리는 메인 세션 판단.
