<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = miss2026_insitu_conductivity_porosity_pressure_compaction.md · lee2025_heckel_argyrodite_powder_densification_nanoindentation.md.
     쪽 표기 = 논문 쪽 "n of 15" (Adv. Energy Mater. e05186).  SI 는 "SI p.Sn" (SI 쪽 번호 S1–S20).
     값 표지: [인쇄] = 본문 · SI · 표 · 그림 안 숫자 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv — 렌더 · 원 래스터에서
     눈금 보정 + 색 표지 무게중심) · [우리 산술] = 이 논문 밖 값 · 식과 엮은 계산 · [미확인] = 원문 (본문 + SI 전수) 에 없음.
     원문 35 쪽 (본문 15 + SI 20) 은 렌더 이미지로 전부 읽었다. -->
# 입경 분포 (D50 4 · 11 · 20 · 40 µm, AMG) 가 Li₆PS₅Cl 압밀 · 격자 변형 · σ_ion 에 미치는 영향 — in situ 가압 EIS (0.1 → 1.5 GPa → 다시 내림) · in-die Heckel · 실험실 / 싱크로트론 XRD (Williamson–Hall · Stephens) · PDF · DFXM 방위 지도 · LIGGGHTS DEM (실측 PSD, E 18.5 GPa, 1.6 GPa) + GeoDict σ: 큰 입자는 1 GPa 에서 "100 %" 치밀 · 작은 입자는 1.5 GPa 에서도 95 % · 넓은 PSD 가 변형 (strain) 을 키운다 — Faka · Alabdali · … · Franco · Zeier (Adv. Energy Mater. 2026)

> slug `faka2026_particle_size_consolidation_strain_lpscl` · DOI `10.1002/aenm.202505186` · type `experiment + DEM (in situ 가압 EIS · in-die Heckel · XRD/PDF/NMR/DFXM · LIGGGHTS Hertz GFF DEM + GeoDict 확산 σ)` · PDF `4. How Particle Size Affects Consolidation Behavior, Strain and Properties of Li6PS5Cl Fast Ionic Conductors.pdf` · SI `4. Sup) How Particle Size Affects Consolidation Behavior, Strain and Properties of Li6PS5Cl Fast Ionic Conductors.pdf` · digested `2026-10-13` · status ✅
>
> **저자**: Vasiliki Faka# · Mohammed Alabdali# · Martin A. Lange · Franco M. Zanotto · Can Yildirim · Mikael Dahl Kanedal · Jędrzej Kondek · Matthias Hartmann · Oliver Maus · Dominik Daisenberger · Michael Ryan Hansen · Jozef Keckes · Daniel Rettenwander · **Alejandro A. Franco\*** · **Wolfgang G. Zeier\*** (# 공동 1저자 · Münster · Amiens LRCS/RS2E · FZ Jülich IMD-4 · ESRF · NTNU · Diamond · Leoben · AIT) · *Adv. Energy Mater.* **2026**, 16, e05186 (본문 15 쪽 + SI 20 쪽) · 접수 2025-09-14 · 수정 2026-01-01 · 승인 2026-01-08 · **CC-BY** · 데이터 보관 `10.17879/12978180830`.
> **같은 시료 · 같은 그룹 카드 (링크만)**: [`schlautmann2023_se_particle_size_composite_transport`](schlautmann2023_se_particle_size_composite_transport.md) (같은 AMG Li₆PS₅Cl 4 · 11 · 20 · 40 µm — PSD 원 자료 = SI ref 1) · DEM 매개변수 원전 [`dem_mechanical_stresses_ssb_electrode_cycling`](dem_mechanical_stresses_ssb_electrode_cycling.md) (Alabdali 2024 ESM, 본문 ref 19 · SI Table S5) · [`alabdali2023_cgmd_wet_manufacturing_ssb_cathode`](alabdali2023_cgmd_wet_manufacturing_ssb_cathode.md) · [`so2021_dem_mold_pressure_assb_coldpress`](so2021_dem_mold_pressure_assb_coldpress.md) (ref 17) · 이웃 압밀 카드 [`lee2025_heckel_argyrodite_powder_densification_nanoindentation`](lee2025_heckel_argyrodite_powder_densification_nanoindentation.md) · [`miss2026_insitu_conductivity_porosity_pressure_compaction`](miss2026_insitu_conductivity_porosity_pressure_compaction.md).
> **판독 원자료**: `litdb/figures/faka2026_particle_size_consolidation_strain_lpscl/digitized.csv` (191 행 — Fig S2 상대밀도 · Fig 1b 감압 가지 σ · Fig 1c DEM ↔ 실험 · Fig 5c 혼합물).

---

## 0. 결론 먼저 — 우리 질문에 대한 답 (★ Codex 인용 대조 포함)

**한 문장**: 같은 AMG Li₆PS₅Cl 을 입경 분포만 달리해 **가압 중 (in-die) 상대밀도 곡선 네 개**와 **가압 → 감압 σ_ion 곡선**을 같은 셀 (CompreCell ⌀6 mm) 에서 준다 — **300 MPa 가압 중 공극은 PSD 에 따라 13 % (40 µm) ~ 26 % (4 µm)** [판독 Fig S2] 로 두 배 벌어지고,
감압 가지에서 σ_ion 은 0.2–0.3 GPa 에서 최대를 찍은 뒤 0.05 GPa 로 내리면 **21–57 % 떨어진다** [판독 Fig 1b] — 하중 제거 쪽의 수송 신호.  DEM 은 **E 18.5 GPa (연화 안 함)** Hertz 로 1.6 GPa 까지 눌렀고 밀도는 보고하지 않았다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ★ Codex 인용 (springback 판정 165 행 *"Faka 등, 2026, §4.2"* — in-die ↔ out-of-die 구분) | **확인됨** — §4.2 "Heckel Analysis" (p.10 of 15): *"There were two types of Heckel analysis. The “in-die” (at pressure) accounts for powder deformation upon applying pressure—in compression. The “out-of-die” (zero pressure) analysis could be used in an already compacted material and also accounts for its elastic recovery."* · 단 이 논문 자신은 **in-die 만** 했다 (out-of-die 밀도 자료 없음) | [인쇄] p.10 |
| ① DEM 언로딩 (ρ_c) | **두께 회복 자료 없음** · 감압 가지 σ_ion(p) 는 있다: 최대 (0.2–0.3 GPa) → 0.05 GPa 에서 40 µm ≈3.74 → ≈1.6 · 20 µm 3.34 → 1.63 · 11 µm 2.66 → 2.01 · 4 µm 2.54 → 1.44 mS/cm | [판독] Fig 1b · S1 |
| ② CL-94 (순수 SE 300 MPa 공극) | **가압 중 ρ_rel @0.3 GPa: 40 µm 87.1 % · 20 µm 84.0 % · 11 µm 77.5 % · 4 µm 73.7 %** → 공극 12.9 · 16.0 · 22.5 · 26.3 % — ρ_rel 분모 = 압밀 시료 Rietveld 결정밀도 (0 압력) | [판독] Fig S2 · 정의 [인쇄] p.10 |
| ③ V2 (상태 · 측정량 · 불확도) | 상태 = 가압 중 · 일정 압력 유지 (0.5 %) · 측정량 = 모터 이동으로 계산한 피스톤 이동 → 밀도 ÷ 결정밀도 · 반복 = **3 회 (σ 측정 "statistical standard deviation values smaller than the plotted size")** · ⚠ 장치 순응도 · 고체 압축 보정 서술 없음 | [인쇄] p.10–11 |
| ④ Heckel (DEM P_y 138 MPa) | 저자 K 값 **미보고** (그림만, 영역 I 재배열 0–0.38 · II 변형 0.38–0.76 · III 파쇄 > 0.76 GPa) · [우리 산술 — Fig S2 판독, 0.4 → 0.75 GPa] **P_y ≈ 280 (40 µm) · 365 (20 µm) · ≈700 MPa (11 · 4 µm)** | Fig 1d · S2 |
| ⑤ E 연화 축 (DEM 1.35 ↔ 실 22–24 GPa) | 이 논문 DEM **Y = 18.5 GPa · ν 0.3 · ρ 1.87** (벽 Y 70 GPa) — 연화 없이 1.6 GPa 까지 · DEM 공극 / 밀도 미보고 | [인쇄] SI Table S5 |
| ⑥ τ · σ 규약 | DEM σ_sim = σ_bulk (2.0 mS/cm) × D_ion/D_bulk (GeoDict 확산, 복셀) = 우리 f 꼴 · 접촉 저항 없음 (CONTACT_FREE 가지 꼴) — 0.7 GPa 이상 f ≈ 0.975 [판독] | [인쇄] p.12 · Fig 1c |

⛔ **한정어 (떼지 말 것)**: ① **순수 SE** (복합체 아님) · AMG 상용 Li₆PS₅Cl ② ⌀6 mm · 100 mg (치밀 두께 ≈1.9 mm [우리 산술]) ③ **in-die** — 장치 순응도 · 고체 탄성 압축 보정 서술 없음 (Table S3 격자로 보면 0.3 GPa 에서 고체 부피 ≈ −1 % [우리 산술]) ④ 40 µm 의 "100 %" 는 고체 압축 · 장치 순응도를 포함할 수 있다 ⑤ 감압 σ 하락의 원인 (접촉 상실 · 두께 회복 · 계면) 은 분리 안 됨 ⑥ Fig 5c 혼합물 곡선은 절대값이 의심스럽다 (§10-4).

---

## 1. 한 줄 요약
D50 4 · 11 · 20 · 40 µm 의 같은 Li₆PS₅Cl 를 in situ 가압 셀 (CompreDrive · ⌀6 mm) 에서 0.1 → 1.5 GPa 로 누르고 다시 빼며 임피던스 · 피스톤 이동을 기록했다.
**큰 입자 (20 · 40 µm) 는 1.0–1.2 GPa 에서 "100 %" 상대밀도에 닿고 Heckel 곡선이 위로 꺾인다 (파쇄)**, **작은 입자 (4 · 11 µm) 는 1.5 GPa 에서도 ≈95 %** · σ_ion 은 큰 입자가 높다 (가압 중 최대 ≈2.9 vs 1.9–2.0 mS/cm).
압축 뒤 XRD 선폭 증가 = 격자 변형 (전위) — **4 µm 가 최대 (WH 2.06 %)** · PDF 응집 길이 30–56 → 13–16 nm · DFXM 이 단일 입자 안 방위 변화 (GND ≈1.1×10¹² m⁻²) 를 처음 보인다.
DEM (실측 PSD) 은 작은 입자 · 넓은 PSD 에서 응력 요동이 크고 단분산에서는 균일 → **"변형은 작은 크기가 아니라 크기 불균일 때문"** · 체로 걸러 4 µm 의 PSD 를 좁히면 변형 2.06 → 1.17 % [판독].

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| V. Faka# · M. Alabdali# · … · **A. A. Franco\*** · **W. G. Zeier\*** (Münster · Amiens · Jülich · ESRF · NTNU · Diamond · Leoben · AIT) | Adv. Energy Mater. 16 (2026) e05186 · CC-BY | 10.1002/aenm.202505186 | **Li₆PS₅Cl (AMG Lithium) — D50,vol 4 · 11 · 20 · 40 µm** · 4 µm 체 거름 · 40 + 4 µm 혼합 — **순수 SE 만** | 실험 (in situ EIS · Heckel · XRD · PDF · NMR · DFXM) + DEM (LIGGGHTS) + GeoDict σ |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 시료 · 셀 · 측정 조건
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| PSD (레이저 회절, 부피 누적) | 4 µm: D10 1 · D50 4 · D90 9 µm · 11 µm: 2 / 11 / 53 · 20 µm: 4 / 20 / 119 · 40 µm: 8 / 40 / 133 µm (Schlautmann 2023 자료) | [인쇄] SI p.S17 Fig S16 캡션 |
| 압력 셀 | CompreDrive + **6C CompreCell (⌀6 mm)** · **100 mg** · Ar (H₂O · O₂ < 0.5 ppm) · 일축 · 압력을 **0.5 % 정확도로 일정 유지** · 피스톤 이동 전 측정 동안 기록 · 가열 맨틀로 **298 K** (측정 시작 2 h 평형) | [인쇄] p.10–11 |
| EIS | Bio-Logic SP-150 · PEIS **150 mV** · 1 MHz – 100 mHz · RelaxIS 3 · Kramers–Kronig 로 맞춤 주파수 범위 확인 · **3 회 반복 · 표준편차가 표지보다 작음** | [인쇄] p.11 |
| 압력 범위 | 0.1 → 1.5 GPa (Fig S2 첫 점 ≈0.01 GPa) · 감압 가지 동일 범위 | [인쇄] p.3 · [판독] |
| 상대밀도 정의 | ρ_rel = 실험 밀도 ÷ **결정밀도 (압밀 시료의 Rietveld)** · 실험 밀도 = **CompreDrive 모터 이동을 in situ 로 감시해 피스톤 이동 계산** | [인쇄] p.10 |
| 결정밀도 값 · 장치 순응도 보정 | **[미확인]** (값 · 보정 서술 없음) | 본문 · SI 전수 |
| DAC (싱크로트론) | Diamond I15 · λ 0.31 Å · 막형 DAC 700 µm 큘릿 · 실리콘 오일 압력매질 (정수압 가정) · 루비 형광 · 0 → 1.5 GPa (Δp 0.1) | [인쇄] p.10 |
| DFXM | ESRF ID03 · 17 keV · 87 Be CRL · 유효 화소 36 nm · (220) 반사 · 2θ 12.05° | [인쇄] p.12 |

### 3-2. ★ in situ σ_ion — 가압 ↔ 감압 (Fig 1b · S1 · p.3) [판독]
- 본문: 빈 점 = 압력 **증가** (1.5 GPa 까지) · 찬 점 = 압력 **감소** (이미 치밀) · *"For pressures higher than 0.7 GPa, there is the so-called activation volume regime, where a linear behavior of ln(σ) vs. pressure is observed and the unit cell contraction takes place"* · 두 무리 — 작은 PSD (4 · 11 µm) 가 σ 가 낮고 큰 PSD (20 · 40 µm) 가 높다 [인쇄] p.3.
- 가압 가지 최대 (육안 판독): 40 µm ≈2.95 (≈0.55 GPa) · 20 µm ≈2.75 (≈0.6) · 11 µm ≈2.05 (0.6–0.7) · 4 µm ≈1.88 (0.7–0.75) mS/cm.
- **감압 가지** (찬 점, 래스터 판독):

| p (GPa) | 1.5 | 1.0 | 0.5 | 0.3 | 0.2 | 0.15 | 0.10 | 0.05 |
|---|---|---|---|---|---|---|---|---|
| 40 µm | — | — | 3.24 | 3.61 | **3.74** | 3.44 | 3.00 | ≈1.6 (육안) |
| 20 µm | 1.91 | 2.39 | 3.13 | **3.34** | 3.21 | 3.02 | 2.55 | 1.63 |
| 11 µm | ≈1.4 (S1) | — | — | 2.66 @0.25 (**최대**) | 2.62 | 2.49 | 2.15 (S1) | 2.01 |
| 4 µm | 1.50 | 1.82 | 2.35 | **2.54** | 2.50 | 2.38 | 2.06 | 1.44 |
- [우리 산술] 감압 최대 → 0.05 GPa 하락: 40 µm ≈ −57 % · 20 µm −51 % · 11 µm −24 % · 4 µm −43 %.  같은 압력에서 감압 가지 > 가압 가지 (≲0.7 GPa) = **비가역 치밀화** · 고압 쪽 겹침 = 활성화 부피 (가역).
- 저자 해석은 감압 저압부 하락을 따로 설명하지 않는다 [미확인 — 기전].

### 3-3. ★★ 가압 중 상대밀도 (Fig S2 · SI p.S2) [판독]
| p (GPa) | ≈0.01 | 0.1 | 0.2 | **0.3** | 0.4 | 0.5 | 0.75 | 1.0 | 1.5 |
|---|---|---|---|---|---|---|---|---|---|
| 40 µm | 64.9 | 77.8 | 83.2 | **87.1** | 90.2 | 92.6 | 97.2 | 100.0 | — |
| 20 µm | 62.0 | 75.0 | 81.0 | **84.0** | 87.0 | 90.0 | 95.0 | 98.0 | (1.2: 100.0) |
| 11 µm | 57.4 | 69.2 | 74.0 | **77.5** | 80.3 | 82.8 | (≈4 µm 와 겹침) | | |
| 4 µm | 47.5 | 61.9 | 68.5 | **73.7** | 77.6 | 80.7 | 86.4 | 90.1 | 94.6 |
- 캡션: *"Li6PS5Cl with smaller PSD achieve 95 % at 1.5 GPa, while Li6PS5Cl with larger PSD achieve 100 % relative density at lower applied pressures (approx. 1 GPa)."* [인쇄] SI p.S2 · 본문 p.4: 40 µm **1 GPa** · 20 µm **1.2 GPa** 에 100 %.
- ⇒ **300 MPa 가압 중 공극 12.9 · 16.0 · 22.5 · 26.3 %** (40 → 4 µm).  초기 충전 (≈0.01 GPa) 도 65 → 48 % 로 PSD 순.
- [우리 산술] 고체 압축 몫: Table S3 의 격자로 0.3 GPa 고체 부피 ≈ −1 % (선형 보간) → 하중 아래 참 공극은 위 값보다 ≈+0.8–0.9 %p · 1 GPa 에서 ≈ −3 % → "100 %" = 참 공극 ≈3 % 가능 (장치 순응도는 별도 · 미확인).

### 3-4. Heckel (Fig 1d · 5c · p.4) — 저자 해석 + 우리 기울기
- 영역 (Fig 1d 배경 · 점선): **I 재배열 0 → ≈0.38 GPa · II 변형 ≈0.38 → 0.76 GPa · III 파쇄 > 0.76 GPa** (20 · 40 µm 만 위로 꺾임) [판독].
- 본문: *"The smallest particles reveal a linear and gradual increase … While linear regions at low pressures indicate plastic deformation, the largest particles … present a deviation from linearity at higher pressure. This behavior is attributed to fragmentation [28] or particle fracturing [13]."* [인쇄] p.4.
- 저자는 **K · P_y 숫자를 내지 않았다**.  [우리 산술 — Fig S2 판독, 0.40 → 0.75 GPa 직선]: K = 3.55 (40 µm) · 2.74 (20 µm) · 1.40 (11 µm, 0.40 → 0.65) · 1.42 GPa⁻¹ (4 µm) → **P_y = 1/K ≈ 280 · 365 · 710 · 700 MPa**.
- ⚠ 큰 입자의 영역 II 기울기에는 파쇄 시작이 섞일 수 있다 (III 경계 0.76 GPa 직전) — 하한 · 상한 아님 · 판독값.

### 3-5. 격자 변형 · 구조 (Fig 2 · S9–S14 · Table S3–S4)
- XRD 선폭 증가 = 압력 유도 전위로 인한 변형 · **4 µm 최대** [인쇄] p.4–5.  Fig 2c (1.5 GPa 뒤 ex situ) [판독]: WH **2.06 · 1.08 · 0.80 · 0.76 %** · RR (Rietveld · Stephens) **1.71 · 0.85 · 0.80 · 0.76 %** (4 · 11 · 20 · 40 µm).
- in situ DAC WH: **4 µm 0.81(4) % · 11 µm 1.27(6) %** — ex situ 와 순서가 뒤집힘 = 빔 (≈60 µm) 이 보는 입자 수가 적어서 (저자 해석) [인쇄] p.5 · Fig S12.
- Table S4 (11 µm, in situ, Stephens): 변형 0.21 % (0 GPa) → 0.30 (0.53) → 0.48 (1.02) → **1.3 % (1.51)** → 1.5 (1.69) → **1.8 % (1.98 GPa)** [인쇄] SI p.S14–S15.
- **Table S3 격자상수 (in situ, Å)** [인쇄] SI p.S14: 4 µm — 0.08 GPa 9.8370(7) · 1.13 9.7310(9) · 1.3 9.7196(9) · 1.35 9.7144(9) · 1.38 9.7116(9) · 1.52 9.7089(9) / 11 µm — 0.08 9.8376(6) · 0.53 9.7836(6) · 1.08 9.7398(7) · 1.31 9.7282(8) · 1.39 9.7236(9) · 1.51 9.7177(9).
- [우리 산술 — Table S3, V = a³, 할선] 11 µm 체적탄성률: 0.08 → 0.53 GPa **K ≈ 27 GPa** (우리 DFT B₀ 26.23 와 +4 %) · 0.53 → 1.08 ≈41 · 1.08 → 1.51 ≈63 GPa (급한 경화 — 비정수압 · 맞춤 오차 가능, 미검증) · 0.08 → 1.51 할선 ≈39 GPa.
- PDF 응집 길이 (Fig 2d) [판독]: 압축 전 30.4 · 45 · 45.7 · 56.4 nm → 압축 뒤 12.8 · 14.8 · 15.7 · 16.0 nm (4 → 40 µm).  단범위 (1.5–20 Å) 차이 없음 [인쇄] p.5.
- NMR: ⁶Li 선폭 소폭 증가 (모두 < 10 Hz) · ³¹P 변화 없음 (PS₄³⁻ 유지) · ⁷Li 이완 Ea 불확도 안에서 같음 [인쇄] p.4 · SI Fig S3–S7 · Table S1–S2.
- DFXM: 평균 방위차 **4 µm 입자 0.0394° · 11 µm 응집체 0.0727°** · 0.0394° 에서 **ρ_GND ≈1.14×10¹² m⁻²** [인쇄] p.6 · *"the first demonstration of DFXM applied to powder-like diffraction patterns from particles"* [인쇄] p.7.
- 체 거름 (Fig 5b) [판독]: 4 µm 넓은 PSD 2.06 % → 거른 뒤 **1.17 %**.

### 3-6. ★ DEM (Fig 1c · 4 · S18–S20 · Table S5 · p.7–8 · p.11–12)
| 항목 | 값 | 표지 |
|---|---|---|
| 코드 · 계 | **LIGGGHTS** · 입자 **20 000** · NVE · 측방 주기 · z 상하 강체 벽 · 위 벽을 내려 **1.6 GPa** 까지 · 모의 시간 **8 ms** (더 길게 해도 차이 없음) · 노드 40 코어 · 375 GB | [인쇄] p.11 |
| 접촉 | GFF (Granular Force Field) — Hertz 이론 ("Hertzian modulus") · 식 F = (k_n δ_n − γ_n v_n) + (k_t δ_t − γ_t v_t) (Eq 3) | [인쇄] p.12 |
| 물성 (Table S5) | **Li₆PS₅Cl Y 18.5 GPa · ν 0.3 · ρ 1.87 g/cm³** · 벽 Y 70.0 GPa · ν 0.3 (출처 Alabdali 2024) · 마찰 · COR [미확인] | [인쇄] SI p.S20 |
| PSD | 실측 PSD 그대로 vs 단일 크기 (D50) | [인쇄] p.7–8 |
| 상자 (Fig 4a · d · e) | 실측 PSD: 4 µm 15×15×42.6 · 11 µm 250×250×234 · 20 µm 250×250×455 · 40 µm 800×800×750 µm / 단일 크기: 200×200×57 · 550×550×156 · 1000×1000×287 · 2000×2000×575 µm | [인쇄 — 그림 안 치수] |
| 입자 응력 (z, 경계 20 % 뺌) | 실측 PSD 중앙값 ≈4.4 · 3.85 · 3.6 · 3.5 GPa, 꼬리 > 10 GPa (4 µm 는 위로 ≈30 GPa) · **단일 크기 ≈3.57 · 3.46 · 3.46 · 3.46 GPa** (좁은 분포) | [판독] Fig 4b · c · S19 |
| 크기별 평균 응력 (Fig S20) | 작은 입자 ≈4–4.5 GPa → 큰 입자 ≈1.5 GPa | [판독] |
| σ_sim (11 µm, GeoDict) | σ_sim = σ_bulk (**2.0 mS/cm**, 실험 RT 값) × D_ion/D_bulk (Fick, xy 주기) · 0.1 GPa **1.30** → 0.3 **1.78** → ≥0.6 **1.94–1.95** ↔ 실험 0.96 → 1.68 → 2.04 (0.6–0.7) → 1.85 (1.0) | [인쇄] p.12 · [판독] Fig 1c |
| DEM 밀도 · 공극 · Heckel | **미보고** | 본문 · SI 전수 |
- 저자: *"the DEM simulations do not account for pressure-induced changes in lattice parameters or variations in intrinsic material properties … the observed enhancement … can be attributed only to geometric factors, i.e., particle rearrangement and void reduction"* · 차이는 *"the assumed geometrical properties of the microstructures"* · 고압에서 사라진다 [인쇄] p.3 · p.5.
- 결론 (p.9): 실험에는 DEM 에 없는 **미세구조 열화 영역** (파쇄 · 입계 증가 · 미세변형) 이 있다 — *"absent in DEM due to its limited spatial resolution"*.
- 응력 기전 문장: *"In polydisperse packings, smaller particles tend to exhibit higher contact pressure and stress, especially under uniaxial compaction. This results from Hertzian contact mechanics, sample geometry …"* (Radjai 2015, ref 34) [인쇄] p.8.
- ⚠ "입자 응력" 의 정의 (stress/atom ÷ 부피? σ_zz? 등가응력?) [미확인] — 1.6 GPa 에서 중앙값 ≈3.5 GPa (≈2.2 배).

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리

### 4-1. 측정 사슬
분말 100 mg → ⌀6 mm CompreCell (298 K) → 압력 계단 상승 (0.1 → 1.5 GPa) · 각 압력 일정 유지 · PEIS → 같은 계단으로 감압 → 피스톤 이동 → 밀도 → ÷ 결정밀도 (압밀 뒤 시료 Rietveld) → ρ_rel · Heckel → 1.5 GPa 압밀 시료 ex situ XRD (WH · Stephens) · PDF · NMR · DFXM → DEM (실측 PSD) 응력 분포 · GeoDict σ.
- 감압 가지에서의 피스톤 이동 (두께 회복) **보고 없음** — 감압 σ 계산에 쓴 두께가 그때그때의 두께인지 [미확인].

### 4-2. ★ 입자 처리
- 실험: 실제 분말 (각진 응집체 · Fig S17) — 큰 입자는 고압에서 **파쇄** (Korjus 2025 ref 13 의 관찰 인용), 작은 입자는 **소성 · 전위** (XRD 선폭 · DFXM).
- DEM: **구 · 강체 · Hertz 탄성 접촉 (연화 없음, E 18.5 GPa)** · 소성 · 파쇄 · 격자 변화 없음 — 형상 불변.  "응력 요동 = 크기 불균일" 은 **접촉망의 힘 분배 (force chain) 결과**이지 소성 결과가 아니다.
- 우리 대응: DEM (E_eff 1.35 GPa 연화 · hooke/hysteresis · 형상 불변) · MPM (J2 형상 소성).  이 논문 DEM 은 우리와 **반대 선택** (물성 E 그대로) — 그 대신 압력을 1.6 GPa 까지 올렸다.

### 4-3. 기법 미니 용어집
- **in-die / out-of-die Heckel**: 가압 중 밀도 (탄성 포함) / 하중 뺀 뒤 밀도 (탄성 회복 포함) — §4.2 정의.
- **Williamson–Hall (WH)**: β cos θ = Cε sin θ + λ/d — 기울기 = 미세변형, 절편 = 결정 크기.
- **Stephens 모델**: 입방정에서 S400 · S220 두 매개변수로 이방성 변형 선폭.  S400 = 2S220 이 아니면 이방성.
- **PDF 응집 길이**: G(r) 진폭이 r 로 줄어드는 길이 — 정렬 영역 크기 (결함 · 크기).
- **DFXM** (dark-field X-ray microscopy): 반사 하나로 입자 안 방위 · 변형 지도 → GND 밀도 ρ_GND = Δθ/(b·화소).
- **활성화 부피 영역**: ln σ 가 p 에 선형으로 감소 (> 0.7 GPa) — 격자 수축이 이온 이동을 어렵게 함 (가역).
- **GFF**: Franco 그룹의 Hertz 기반 DEM 힘장 이름.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a | 압밀 모식 (치밀화 → 압밀 consolidation) | 용어 |
| 1b | σ_ion vs p (4 PSD) — 빈 점 가압 · 찬 점 감압 | ★ 감압 가지 σ 하락 (언로딩 수송 신호) · 활성화 부피 영역 |
| 1c | 11 µm: DEM+GeoDict σ_sim ↔ 실험 (0.1–1.0 GPa) | DEM σ (접촉 저항 없음) 의 포화 ≈0.975 σ_bulk |
| 1d | Heckel (4 PSD) + 영역 I · II · III | ★ in-die Heckel 형태 · 파쇄 꺾임 |
| 2 | (a) XRD 선폭 (b) DAC 반사 이동 (c) WH · RR 변형 vs D50 (d) PDF 응집 길이 (e) Stephens 변형 곡면 | 격자 변형 = 소성 (MPM 쪽 물리의 원자 척도 흔적) |
| 3 | DFXM: 전위 모식 · 장치 · 4 µm / 11 µm 방위 · FWHM · 방위차 지도 (3 · 5 µm 막대) | 입자 안 방위 변화 |
| 4 | DEM: (a) 4 µm 실측 PSD 상자 (b) 실측 PSD 입자 응력 바이올린 (c) 단일 크기 (d, e) 응력 색 3D (0–3 GPa) | ★ 크기 불균일 → 응력 요동 · 벽 근처 응력 낮음 |
| 5 | (a) 체 거름 · 혼합 모식 (b) 변형 2.06 → 1.17 % (c) 40 + 4 µm 혼합 Heckel | 이원 PSD 설계 · ⚠ 혼합물 절대값 의심 (§10-4) |
| S1 | 11 µm 가압 · 감압 σ (치밀화 영역 표지) | ★ 감압 가지 |
| S2 | ρ_rel vs p (4 PSD) | ★★ CL-94 후보 곡선 |
| S3–S7 · Table S1–S2 | ⁶Li · ³¹P MAS NMR · 디컨볼루션 · ⁷Li 이완 · Ea | 국소 구조 불변 |
| S8–S11 | XRD (압축 전 · 뒤) · Rietveld · DAC Rietveld (ambient · 0.53 · 1.02 · 1.51 GPa) | 상 · 격자 |
| S12 | in situ (DLS) ↔ ex situ 변형 (4 · 11 µm) | 측정 표본 수 효과 |
| S13 | Stephens 변형 곡면 vs 압력 (ambient → 1.98 GPa) | 변형 성장 |
| S14 | PDF (전 · 뒤 · 장 · 단범위) | |
| S15 | 방위차 히스토그램 (4 · 11 µm) | |
| S16 | PSD 누적 곡선 | DEM 입력 |
| S17 | SEM (4 PSD, 20 µm 막대) | 형상 (각진 응집체) |
| S18 | DEM 상자 (실측 PSD · 단일 크기) | |
| S19 | DEM 응력 vs D50 (평균 ± 산포) · z 방향 응력 | 응력 요동 크기 |
| S20 | 크기별 평균 입자 응력 | 작은 입자 고응력 |
| Table S3 | DAC 격자상수 vs p (4 · 11 µm) | ★ 체적탄성률 산술 · 고체 압축 보정 |
| Table S4 (+S4b) | Stephens S400 · S220 · 변형 % vs p (11 µm, 0 → 1.98 GPa) | |
| Table S5 | DEM GFF: Li₆PS₅Cl Y 18.5 · ν 0.3 · ρ 1.87 · 벽 Y 70 | ★ DEM 물성 (연화 없음) |

## 6. Post-processing ★
- **무엇을**: 임피던스 적합 (RelaxIS, KK) → σ · 피스톤 이동 → ρ_rel → Heckel (영역 판정만) · XRD Rietveld (TOPAS) · WH · Stephens (GSAS-II 곡면) · PDF (PDFgetX3 · TOPAS, 응집 길이 = 구형 모델) · NMR 디컨볼루션 · DFXM (darfix, COM · FWHM · 기울기 → GND) · DEM 응력 (경계 20 % 뺌, 바이올린) · GeoDict 확산 σ.
- **안 한 것**: Heckel 기울기 숫자 · out-of-die 밀도 · 감압 두께 · DEM 밀도 · DEM 언로딩 · 실험–DEM 밀도 대조.
- **우리 후처리 (이 카드)**: Fig S2 · 1b · 1c · 5c 판독 · Heckel P_y 산술 · Table S3 로 체적탄성률 · 고체 압축 몫 산술.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · `docs/` 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| DEM 코드 · 접촉 | LIGGGHTS · Hertz GFF · **Y 18.5 GPa** · ν 0.3 · 구 · 실측 PSD | LIGGGHTS · hooke/hysteresis · **E_eff 1.35 GPa** (18 배 연화) · 구 (SE r 0.5 · AM PC 4.5 / SC 2.0 µm) | ★ E 선택이 정반대 — 그들은 밀도를 보고하지 않아 "E 18.5 로 실험 밀도가 나오는가" 는 이 논문으로 판정 불가 |
| 압력 | 1.6 GPa (DEM) · 1.5 GPa (실험) | 300 MPa | 압력 축 다름 |
| 순수 SE 300 MPa 공극 | 가압 중 **12.9–26.3 %** (PSD 순) [판독] | MPM 보정 표적 ≈10 % — **출처 철회 (`CL-94`, 외부 앵커 없음)** · DEM 순수 SE ε_sphere 퇴화 영역 | §7-3 |
| 입경 효과 | **실재 · 크다** — 300 MPa 공극 2 배 차 · Heckel P_y 2.5 배 차 | 길이척도 없는 탄성 모델은 입경효과를 못 낸다 (원장 `CL-64`) · 우리 DEM 크기 효과 = 충전 (Furnas) 쪽 | ★ 실험 입경 효과 (작을수록 덜 치밀) 는 우리 DEM 에 없다 — 원인 후보 (응집 · 마찰 · 표면적 · 소성 크기 효과) 는 DEM 접촉 법칙 밖 |
| Heckel P_y | ≈280–365 MPa (20–40 µm) · ≈700 MPa (4–11 µm) [우리 산술] | DEM 순수 SE 138 MPa | DEM 이 2–5 배 무르다 (`lee2025_…` 294–344 MPa 와 같은 방향) |
| σ 모델 | GeoDict 복셀 확산 (접촉 저항 없음) · σ_bulk 2.0 | 접촉망 Holm 협착 (DEM) · 복셀 FV (MPM STEP3, CONTACT_FREE 가지 — `CL-81`) | 그들의 DEM σ = 우리 복셀 σ 와 같은 부류 (협착 없음) — 고압 포화 f ≈0.975 |
| 언로딩 | 감압 σ 가지 (두께 없음) | DEM 언로딩 등록 (ρ_c · P_meas 1 MPa · 판 속도 0.01 mm/s) | §7-2 |

### 7-2. ★ 언로딩 시험 (ρ_c) — 무엇을 주나
- **두께 회복 자료는 없다** (§4-1).  있는 것 = 감압 σ(p): 0.2–0.3 GPa 최대 뒤 0.05 GPa 에서 **−24…−57 %** [판독 + 우리 산술].
- 해석 후보 (원문 미분리 · 우리 추정): ① 하중이 줄며 접촉 면적이 줄어 협착 저항 ↑ (가역 탄성 회복의 수송 신호) ② 두께 회복 (σ = d/(R·A) 의 d 처리 [미확인]) ③ 셀–시료 계면 저항 (저압).  우리 DEM 언로딩 등록의 보조 관측 (접촉 유형별 겹침 회복 · 망 σ 를 출발 · 측정 상태에서 다시 풀기) 이 같은 축을 모델 안에서 준다 — **수송 쪽 대조점 후보** (같은 상태 정의 · 순수 SE ↔ 복합체 차이 · 한정어 그대로).
- 이 논문 감압의 최저 압력은 **0.05 GPa (50 MPa)** — 우리 P_meas 1 MPa 보다 50 배 높다.

### 7-3. ★ CL-94 · V2 — 무엇이 서고 무엇이 안 서나
- **선다**: 원문 확인된 **순수 Li₆PS₅Cl 가압 중 ρ_rel 곡선 네 개** (같은 셀 · 같은 그룹 · 3 회 반복 서술) — 300 MPa 공극 **12.9 (40 µm) · 16.0 (20 µm) · 22.5 (11 µm) · 26.3 % (4 µm)** [판독].
- **안 선다 (아직)**: ① 결정밀도 값 · 장치 순응도 · 고체 압축 보정 [미확인] ② 반복 산포는 σ 에 대해서만 서술 ("표지보다 작다") — 밀도 반복 서술 없음 ③ 우리 SE 입경 (r 0.5 µm, D 1 µm) 은 이 논문 가장 작은 PSD (D50 4 µm) 보다도 작다 → **입경 외삽 필요** (이 자료의 방향대로라면 더 성기다 — 단 우리 실험 분말의 PSD 는 [미확인]).
- ⇒ CL-94 의 "10 % @300 MPa" 표적은 이 논문의 **어느 PSD 보다도 치밀**하다 (가장 치밀한 40 µm 가 12.9 %).  ⚠ 결정 (표적 재보정 · 앵커 채택) = 1저자 — 이 카드는 원장을 고치지 않는다.
- Codex V2 판정 (`docs/reviews/codex_review_model_validation_20261008.md` Q3–Q4) 기준: 상태 (in-die) · 측정량 (모터 이동 밀도) 은 명시, 원측정 (피스톤 이동 원자료) 은 데이터 보관소 `10.17879/12978180830` [미확인 — 열어 보지 않음], 불확도 (밀도) 미서술.

### 7-4. Heckel ↔ frame[3]
- 세 번째 외부 후보 (miss2026 AMI 219–243 · lee2025 294–344 MPa 다음): **입경에 따라 280 → 700 MPa** — 같은 조성의 Heckel 이 PSD 로 2.5 배 바뀐다 ⇒ frame[3] 대조에 **SE 입경 · PSD 를 반드시 맞춰야** 한다.  우리 DEM 138 MPa 는 어느 PSD 보다도 무르다.

### 7-5. E 연화 축 · DEM 방법론 대조
- 이 논문 DEM 은 **E 18.5 GPa (실물 근처)** 로 1.6 GPa 까지 — 우리 frame[2] 의 "강체구 + 탄성 접촉은 실제 소성 분말보다 덜 변형 → E 연화 필요" 와 **정면 대조되는 선택**.  그러나 **DEM 밀도를 보고하지 않아** 그 선택이 실험 밀도를 재현했는지 알 수 없다 — 저자도 *"limited spatial resolution"* · 소성 · 파쇄 부재를 한계로 적는다.
- [우리 산술] 무차원 하중 P/E: 이 DEM 1.6 GPa / 18.5 GPa ≈ 0.086 ↔ 우리 0.3 GPa / 1.35 GPa ≈ 0.22 — 우리 쪽이 ≈2.6 배 크다.  접촉 법칙이 다르므로 (Hertz ↔ hooke/hysteresis) 이 비를 겹침 · 밀도 차로 옮기지 않는다 — 크기 감각만.
- 응력 요동 결론 (크기 불균일 → 작은 입자 고응력) 은 **우리 Auerbach 파괴 판정 · 입자 응력 분포 (LW · stress/atom 규약 문제, `LHS-29`)** 와 같은 축 — "입자 응력" 정의 확인 전에는 수치 비교 금지.

### 7-6. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 순수 SE 의 기계 (in-die 밀도 · Heckel · 격자 변형 · 방위) + 수송 (가압 · 감압 σ) — 실험 · DEM 응력 분포 · 복셀 σ.
- **없는 것**: 복합체 · 접촉 수 · 접촉 면적 · DEM 밀도 · 두께 회복.  ⇒ 우리 DEM (수송 · 패킹) 과 MPM (형상 소성) 모두에 **순수 SE 입경 효과**라는 대조점을 준다 (둘 다 아직 못 냄).

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **Codex 인용 (Faka §4.2) 원문 확인 완료** — springback 판정문 165 행의 문장은 원문과 맞다 (§0 표 첫 행).  우리 글에서 근거로 쓸 때: *"in-die 와 out-of-die (탄성 회복 포함) Heckel 을 구분한다 (Faka 2026 §4.2) — 그 논문 자신은 in-die 만 측정"*.
2. **CL-94 후보 + 입경 경고** — 같은 Li₆PS₅Cl 도 300 MPa 공극이 13–26 %.  표적 하나를 고르려면 우리 실험 SE 의 PSD 부터 [미확인 → 확보].
3. **언로딩 수송 신호** — 감압 σ 하락 (−24…−57 % @0.05 GPa) 은 DEM 언로딩의 망 σ 재계산과 같은 축 (보조 관측 후보).
4. **체적탄성률 교차** — Table S3 저압 할선 K ≈27 GPa ≈ 우리 DFT B₀ 26.23 (in-die 고체 압축 보정의 입력) · 고압 경화는 미검증.
5. **"크기 불균일 → 응력 요동"** — 우리 PC/SC 이원 침대의 입자 응력 분포 해석 · Auerbach 판정의 배경 (LHS-29 정의 문제 해결 뒤).
6. **DEM E 선택의 반례 사례** — E 18.5 GPa + 1.6 GPa 의 DEM 이 밀도를 보고하지 않는다 = 우리 E 연화 정당화 토론에서 "다른 그룹은 연화 안 한다" 는 반론에 대한 답 재료 (그 그룹 DEM 은 밀도를 검증하지 않았다).

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Faka et al. (*Adv. Energy Mater.* 2026, §4.2) distinguish in-die Heckel analysis (at pressure) from out-of-die analysis (zero pressure), which also accounts for elastic recovery; their own densities are in-die only."
- "For the same Li₆PS₅Cl, the in-die relative density at 0.3 GPa ranges from ≈74 % (D50 4 µm) to ≈87 % (D50 40 µm) (read from their Fig. S2)."
- "On decompression, the ionic conductivity of pressed Li₆PS₅Cl peaks near 0.2–0.3 GPa and falls by ≈24–57 % at 0.05 GPa (read from their Fig. 1b)."
- 국문: *"같은 Li₆PS₅Cl 이라도 입경 분포에 따라 300 MPa 가압 중 공극이 13–26 % 로 두 배 벌어진다 (Faka 2026, 그림 판독) — 순수 SE 공극 표적은 입경을 함께 적어야 뜻이 있다."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **in-die 밀도의 보정 서술 부재** — 장치 (피스톤 · 프레임) 순응도 · 고체 탄성 압축 (Table S3 로 1 GPa 에서 ≈3 %) 을 뺐다는 말이 없다.  "100 % 상대밀도" 는 이 둘을 포함할 수 있다.
2. **결정밀도 값 [미확인]** — "압밀 시료의 Rietveld" 라고만 함.
3. **K · P_y 숫자 없음** — 우리 산술 (§3-4) 은 판독 기반 · 영역 II 구간 선택에 따라 ±20 % 흔들릴 수 있다.
4. **Fig 5c 혼합물 (40 + 4 µm)**: 곡선 값 ln(1/(1−ρ)) ≈0.75 → 1.05 (ρ_rel ≈53 → 65 %) [판독] 로 **두 순수 분말 (1.5 GPa 에서 95–100 %) 보다 훨씬 낮다** — 물리적으로 이상 (혼합물이 더 성기다?).  원문은 "선형 · 파쇄 영역 없음" 만 해석 — 밀도 기준 (질량 · 결정밀도) 의 어긋남 가능성 [추정].  ⇒ 이 곡선의 절대값을 인용하지 않는다.
5. **감압 가지의 두께 처리 [미확인]** · 감압 σ 하락의 기전 미분리.
6. **DEM**: 밀도 미보고 · 입자 응력 정의 [미확인] · 마찰 · COR [미확인] · 4 µm 상자 15×15×42.6 µm (넓은 PSD 에서 대표성 의문 — 큰 입자 몇 개가 상자를 채움, Fig 4a 판독) · 실험과의 σ 대조는 11 µm 하나.
7. **in situ DAC 변형 (0.81 vs 1.27 %) ↔ ex situ (2.06 vs 1.08 %) 순서 반전** — 저자도 *"the reason for this difference is at this point unclear"*.
8. **이해관계**: 시료 · PSD 는 공급사 (AMG) 에서 — 같은 시료의 Schlautmann 2023 은 공급사 직원 공저 명시 (그 카드 §); 이 논문은 감사의 글에 AMG 제공만 적는다.
9. **전이 한계**: 순수 SE · ⌀6 mm · 1.5 GPa 까지 · 4–40 µm ↔ 우리 복합체 · 300 MPa · SE r 0.5 µm.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 7 | C. Schneider, C. P. Schmidt, A. Neumann, et al., *Adv. Energy Mater.* 13 (2023): 2203873 | 정본 카드 있음 — Heckel in die (t-Li₇SiPS₈) |
| 8 | J.-M. Doux, Y. Yang, D. H. S. Tan, et al., "Pressure Effects on Sulfide Electrolytes for All Solid-State Batteries," *J. Mater. Chem. A* 8 (2020): 5049–5055 | ⚠ 정본 `doux2020_stack_pressure_assb` 와 다른 논문 — 미 digest |
| 9 | Q. Tran, M. Agrawal, M. Häusler, et al., *Adv. Mater.* 37 (2025): 2501592 (slurry-cast Li₆PS₅Cl 테이프 일축 치밀화 · PSD) | 테이프 치밀화 — 이 묶음 paper 6 계열 |
| 11 | M. S. Diallo, T. Shi, Y. Zhang, et al., *Nat. Commun.* 15 (2024): 858 | 펠릿 밀도 ↔ 파괴 |
| 12 | M. Kodama, S. Komiyama, A. Ohashi, … S. Hirai, *J. Power Sources* 462 (2020): 228160 | 고압 in situ XCT + 수치 모의 (황화물) |
| 13 | O. Korjus, S. Mitra, Q. Berrod, et al., *Energy Storage Mater.* 82 (2025): 104589 | ★ Li₆PS₅Cl in situ 치밀화 · 큰 입자 파쇄 (paper 5 의 같은 축) |
| 14 | C. A. Heck, T. Scharmann, M. Osenberg, et al., *Batteries & Supercaps* 7 (2024): 202300487 | 황화물 분리막 캘린더링 · 스프링백 |
| 19 | M. Alabdali, F. M. Zanotto, M. Chouchane, et al., *Energy Storage Mater.* 70 (2024): 103527 | 정본 카드 `dem_mechanical_stresses_ssb_electrode_cycling` — DEM 물성 출처 |
| 21 | M. Kodama, A. Ohashi, and S. Hirai, *J. Power Sources Adv.* 4 (2020): 100019 | 단일 SE 입자 고압 XCT (접촉 면적 · 구형도 증가) |
| 22 | V. Faka, M. T. Agne, M. A. Lange, et al., *J. Am. Chem. Soc.* 146 (2024): 1710–1721 | 압력 유도 전위 (Li₆PS₅Br) |
| 25 | C. Sun and D. J. W. Grant, *Pharm. Dev. Technol.* 6 (2001): 193–200 | 입자 탄성 변형이 Heckel 에 미치는 영향 — in-die ↔ out-of-die |
| 26 | V. Faka, M. T. Agne, P. Till, et al., *Energy Adv.* 2 (2023): 1915–1925 | 활성화 부피 (miss2026 AMI 카드 §10-5 가 쓴 값의 원전) |
| 34 | F. Radjai, *Comptes Rendus Physique* 16 (2015): 3–9 | 다분산 충전 힘 전달 |
| 39 | R. W. Heckel, *Trans. Metall. Soc. AIME* 221 (1961): 1001–1008 | Heckel 원전 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 15 쪽 · SI 20 쪽 전부 렌더 이미지로 읽고 `pdftotext` 로 인용문 대조 · DOI `10.1002/aenm.202505186` = 본문 1 쪽 인쇄 · §4.2 원문 (p.10) 은 텍스트 층과 렌더 둘로 확인.
- Table S3 · S4 · S5 는 텍스트 층 + 크롭 영상으로 칸마다 대조 (S3 은 텍스트 층 순서가 두 열을 섞어 크롭 영상 기준으로 바로잡음).
- 판독: Fig S2 (렌더 1791×861 px · 안쪽 눈금 탐지) · Fig 1b · 1c · 5c (원 래스터 1800×1743 · 1455×1477) — 색 표지 무게중심 (찬 표지는 침식으로 빈 고리와 분리).
- 그림 크롭 31 장 = 본문 Figure 1–5 · SI Figure S1–S20 · Table S1–S5 (+ S4 둘째 쪽) · **손 크롭 1 장** (tab_S4b = 두 쪽에 걸친 Table S4 의 p.S15 네 행).
- 정본 litdb 중복 확인: DOI · 제목 낱말 · "Faka" papers/ 전수 grep — 이 논문 카드 없음 (miss2026 AMI 카드가 다른 Faka 논문 (2023 Energy Adv.) 을 인용할 뿐).

## 🔗 관련 카드
- 같은 시료 · 같은 그룹: `schlautmann2023_se_particle_size_composite_transport` · `dem_mechanical_stresses_ssb_electrode_cycling` · `alabdali2023_cgmd_wet_manufacturing_ssb_cathode`.
- 압밀 실측: `lee2025_heckel_argyrodite_powder_densification_nanoindentation` · `miss2026_insitu_conductivity_porosity_pressure_compaction` · `schneider2023_particle_size_pressure_transport` · `cronau2021_stack_pressure_ionic_conductivity` · `cronau2022_wet_milling_particle_size_ionic_conductivity`.
- DEM 압밀 · σ: `so2021_dem_mold_pressure_assb_coldpress` · `so2022_dem_contact_model_assb_compaction_sintering` · `zunker2025_dem_large_deformation_compaction`.
- 탄성: `deng2016_elastic_superionic_electrolytes_dft` · `kraft2017_lattice_polarizability_argyrodite_Li6PS5X` (Rietveld 출발 모델, ref 47).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
