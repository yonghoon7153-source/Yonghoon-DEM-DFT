<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = faka2026_particle_size_consolidation_strain_lpscl.md · lee2025_heckel_argyrodite_powder_densification_nanoindentation.md.
     쪽 표기 = 논문 쪽 "n of 13" (Adv. Funct. Mater. e75195).  SI 는 "SI p.n" (SI PDF 쪽 1–11).
     값 표지: [인쇄] = 본문 · SI · 표 · 그림 안 숫자 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv — 원 래스터 ·
     렌더에서 눈금 보정 + 색 표지 무게중심, 일부 육안) · [우리 산술] = 이 논문 밖 값 · 식과 엮은 계산 · [미확인] = 원문 (본문 + SI 전수) 에 없음.
     원문 24 쪽 (본문 13 + SI 11) 은 렌더 이미지로 전부 읽었다. -->
# 초고압 (≈3.8 GPa) in situ 치밀화 — 비정질 Li₃PS₄ (LPS) 와 결정 Li₆PS₅Cl (LPSCl): 파리–에든버러 프레스 (UToPEC · 준등방 가압) 에서 X-선 흡수 밀도 · 단층촬영 (1.277 µm) · 에너지분산 XRD · 중성자 회절 + 실험실 EIS · 결합원자가 (BVEL) — 두 단계 치밀화 (입계 공극 닫힘 → 격자 수준) · σ 는 LPSCl 135 MPa 에서 최대 3.3 mS/cm 뒤 감소 (활성화 부피 2.32 cm³/mol) · 감압 때 격자 이동은 가역 · 선폭 · σ 증가는 비가역 — Thompson · Korjus · … · Le Floch · Villevieille (Adv. Funct. Mater. 2026)

> slug `thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography` · DOI `10.1002/adfm.75195` · type `experiment (in situ 고압 — PE 프레스 UToPEC · Beer–Lambert 흡수 밀도 · X-선 CT · ED-XRD · NPD · 실험실 EIS · BVEL · 시뮬레이션 없음)` · PDF `5. High Pressure Densification Investigation of Li3PS4 and Li6PS5Cl Solid Electrolytes using Combine X-Ray Diffraction, X-Ray Absorption Tomography and Ionic Measurement.pdf` · SI `5. Sup) High Pressure Densification Investigation of Li3PS4 and Li6PS5Cl Solid Electrolytes using Combine X-Ray Diffraction, X-Ray Absorption Tomography and Ionic Measurement.pdf` · digested `2026-10-13` · status ✅
>
> **저자**: Oskar Thompson# · Ove Korjus# · Adrien Fauchier-Magnan · Clément Albin · Sergio F. Mayer · Emmanuelle Suard · Thomas Hansen · Laura Henry · Nicolas Guignot · Vittoria Pischedda · **Sylvie Le Floch\*** · **Claire Villevieille\*** (# 공동 1저자 · Grenoble LEPMI · ILL · Lyon ILM · SOLEIL) · *Adv. Funct. Mater.* **2026**, 36, e75195 (본문 13 쪽 + SI 11 쪽) · 접수 2026-01-12 · 수정 03-04 · 승인 03-20 · **CC-BY** · 연구비 ANR OpInsolid (ANR-21-CE50-0044) · SOLEIL 빔타임 20230357 · 20240730.
> **이웃 카드 (링크만)**: [`faka2026_particle_size_consolidation_strain_lpscl`](faka2026_particle_size_consolidation_strain_lpscl.md) (같은 축 — 압력 유도 변형 · 활성화 부피) · [`lee2025_heckel_argyrodite_powder_densification_nanoindentation`](lee2025_heckel_argyrodite_powder_densification_nanoindentation.md) · [`miss2026_insitu_conductivity_porosity_pressure_compaction`](miss2026_insitu_conductivity_porosity_pressure_compaction.md) · [`cronau2021_stack_pressure_ionic_conductivity`](cronau2021_stack_pressure_ionic_conductivity.md) (본문 ref 4) · [`sakuda2013_sulfide_mechanical_property`](sakuda2013_sulfide_mechanical_property.md) (ref 17 — 저자가 그 이론밀도를 의심).
> **판독 원자료**: `litdb/figures/thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography/digitized.csv` (74 행 — Fig 1 흡수 밀도 · Fig S2 결정밀도 · Fig 8 σ · Fig S6 WH 변형).

---

## 0. 결론 먼저 — 우리 질문에 대한 답 (★ Codex 인용 대조 포함)

**한 문장**: 순수 LPSCl (NEI 상용, 추정 입경 5 µm) 을 **준등방** 고압 셀에서 3.8 GPa 까지 누르고 ≈1.1–1.8 GPa 까지 되돌리며, 같은 시료의 **거시 (흡수) 밀도 · 결정 (격자) 밀도 · 선폭 · 격자상수**를 따로 잰다 —
**감압 때 격자 수축은 되돌아가고 (탄성), 선폭 (결함 · 미세변형) 과 σ 증가 · 거시 밀도 감소는 남는다 (비가역)**.  그러나 감압이 **0 까지 내려가지 않고** (≈1.15 GPa 에서 멈춤) **다이 압축이 아니며**, 흡수 밀도는 ≈800 MPa 이상에서 결정밀도보다 커져 (음의 공극) 절대값 보정에 문제가 있다 [우리 산술].

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ★ Codex 인용 (springback 판정 130 행 *"감압 시 가역적인 격자 변형과 비가역 변화가 함께 관찰 … Thompson 등, 2026"*) | **확인됨 (한정어 둘)** — p.6 §4.1: *"Upon decompression, the peak shift is reversible, in line with elastic lattice strain, whereas the broadening appears largely irreversible, suggesting the development of permanent microstructural defects or disorder."* · NPD 격자상수도 감압에서 같은 선으로 돌아옴 (SI Table S1: 2249 MPa 9.60589 Å ↔ 2255 MPa released 9.60592 Å) · 비가역 쪽 = WH 변형 (SI Note S2) · 거시 밀도 (p.3) · σ (초록).  한정어: ① 감압은 ≈1.14–1.84 GPa 까지만 (0 아님) ② SI Note S1 은 결정밀도가 감압 뒤 "pristine 보다 높다 → 격자상수의 영구 변화" 라고 적어 본문과 반쯤 엇갈린다 | [인쇄] p.6 · p.7 · SI p.2 · p.6 · p.9 |
| ① DEM 언로딩 (ρ_c) 규모 | **두께 · 거시 회복률 없음** — 감압 3770 → 1144 MPa 에서 흡수 밀도 2.089 → 1.862 g/cm³ (−11 %) · 같은 구간 결정밀도 2.008 → 1.925 (−4.1 %) [판독] → 격자 팽창 몫을 넘는 거시 밀도 감소 (≈7 %p, 오차막대 ±0.03–0.04 g/cm³ 안팎 · [우리 산술]) · 압력 셀에서 꺼낸 뒤 **"several minutes" 지나 자발 파단** (잔류 응력) | [판독] Fig 1 · S2 · [인쇄] p.4 |
| ② CL-94 (순수 SE 300 MPa 공극) | 직접 값 없음 (공극 % 미보고) · [우리 산술] 331–334 MPa 흡수 밀도 1.562 g/cm³ ↔ 같은 압력 결정밀도 1.861 → **≈16 %** · 문헌 이론밀도 (1.77–1.88, 본문) 로는 12–17 % — **준등방 · 다른 상용 분말 · 흡수 밀도 절대 보정 문제** 한정 | [판독] Fig 1 · S2 · TD [인쇄] p.3 |
| ③ V2 (상태 · 측정량 · 불확도) | 상태 = 하중 아래 · 준등방 (붕소–에폭시 개스킷) · 측정량 = 흡수 밀도 (공극 + 격자 압축 모두 포함, 저자 명시) · 불확도 = 그림 오차막대만 · 반복 [미확인] · 압력 = NaCl 상태방정식 교정 곡선 (하중–압력 이력 있음, Fig S8) | [인쇄] p.2–3 · p.10 |
| ④ Heckel | 저자 분석 없음 · 흡수 밀도 점 6–7 개 (66 · 135 MPa 결측) — 적합 의미 낮음 | Fig 1 |
| ⑤ E · K 축 | [우리 산술 — SI Table S1 NPD 격자상수 BM3 맞춤] **K₀ = 22.9 ± 1.0 GPa · K′ 7.2 ± 0.7** (K′ = 4 고정이면 27.5 ± 0.7) ↔ 우리 DFT B₀ 26.23 · 0.3 GPa 에서 고체 부피 −1.24 % | [인쇄] Table S1 → [우리 산술] |
| ⑥ 고유 σ 의 압력 의존 | 활성화 부피 **LPSCl 2.32 · LPS 2.17 cm³/mol** (ln σT 선형 영역 ≈700 → 3800 MPa) · 결합원자가 퍼콜레이션 에너지 0.64 → 0.87 eV | [인쇄] p.9 · Fig 10–11 |

⛔ **한정어 (떼지 말 것)**: ① **준등방 (quasi-isostatic) PE 프레스** — 일축 다이 압축이 아니다 (초록의 "uniaxial compression" 과 실험편 서술이 다르다) ② 감압 최저 ≈1.1–1.8 GPa — **무하중 회복이 아니다** ③ 흡수 밀도 > 결정밀도 (≥800 MPa) = 절대 보정 결함 신호 ④ 순수 SE (LPSCl NEI · LPS 자체 합성) ⑤ σ 는 실험실 다른 실험 ("similar pressure conditions") — 같은 시료 아님 ⑥ 반복 · 시료 수 [미확인].

---

## 1. 한 줄 요약
기밀 고압 셀 (외경 10 mm · 내경 3.5 mm 붕소–에폭시 개스킷 · PTFE 관 · 황동 마개) 을 만들어 SOLEIL PSICHÉ 빔라인의 UToPEC 프레스에서 LPS · LPSCl 을 3.7–3.8 GPa 까지 누르며 **흡수 밀도 · CT · ED-XRD** 를, ILL D20 에서 **중성자 회절**을, 실험실 PE 프레스에서 **EIS** 를 쟀다.
치밀화는 **두 단계**: (i) ≲500 MPa (LPSCl) 입계 공극 닫힘 + 큰 입자 파쇄 → (ii) 평탄부 — 격자 수준 변형 · 입내 공극 제거 (CT 해상도에서 1155 MPa 에 모든 공극 사라짐).  σ 는 접촉 개선으로 오르다 **LPSCl 135 MPa 3.3 mS/cm · LPS 479 MPa** 에서 최대, 그 뒤 격자 수축 · Li 이동 장벽 증가로 감소 (3771 MPa LPSCl 0.14 mS/cm).
감압 때 **격자 이동은 되돌아가지만 선폭 · σ 증가 · 거시 밀도 감소는 남는다** — LPSCl 은 꺼낸 뒤 몇 분 안에 저절로 깨졌다 (잔류 응력 · 입계 파단).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE) | 연구유형 |
|---|---|---|---|---|
| O. Thompson# · O. Korjus# · A. Fauchier-Magnan · C. Albin · S. F. Mayer · E. Suard · T. Hansen · L. Henry · N. Guignot · V. Pischedda · **S. Le Floch\*** · **C. Villevieille\*** | Adv. Funct. Mater. 36 (2026) e75195 · CC-BY | 10.1002/adfm.75195 | **Li₆PS₅Cl (NEI Corporation, 상용, 추정 입경 5 µm, 그대로)** · **비정질 Li₃PS₄** (75Li₂S:25P₂S₅ 볼밀 510 rpm · 5 분 밀링/15 분 휴지 × 360, 열처리 없음) — **순수 SE 만** | 실험 — 싱크로트론 · 중성자 · 실험실 EIS · BVEL (계산) |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 장치 · 조건
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 프레스 | 파리–에든버러 (PE) — 붕소–에폭시 압력매질 + 준원뿔 앤빌 = **"quasi-isostatic compression conditions"** · UToPEC (PSICHÉ, 회전 · 얇은 기둥 · 최대 15 GPa) + 표준 PE | [인쇄] p.10 |
| 셀 "10–3.5" | 개스킷 외경 10 · 내경 3.5 mm · ① PEEK 압출방지 고리 ② 붕소–에폭시 개스킷 ③ 황동 마개 ④ PTFE 관 · 글러브박스 조립 기밀 클램프 | [인쇄] p.10–11 · Fig 12 |
| 압력 교정 | 하중 (kN) → 시료 압력: PTFE 관 안 NaCl 의 in situ XRD + NaCl 상태방정식 (Fig S8) — **하중–압력 이력 고리** (감압 가지가 같은 하중에서 더 높은 압력, 예 ≈44 kN 에서 가압 ≈480 ↔ 감압 ≈1100 MPa [판독]) · Fig S8 세로축 이름 "Pressure (GPa" 인데 눈금은 0–4000 (MPa) | [인쇄] p.10 · [판독] SI p.10 |
| 최대 압력 · 감압 | 3770–3810 MPa · *"Upon releasing the pressure from the press, the internal pressure within the sample decreased from ca. 3800 MPa to ca. 1150 MPa (approximately 30% of the maximum applied value). We did not perform the absorption density measurement below this pressure, as we could not guarantee that the sample would still be airtight."* | [인쇄] p.3 |
| 흡수 밀도 | 백색광 · 다색 분광기 100 keV · y 방향 주사 · Beer–Lambert (NIST 감쇠표) — *"reveals macroscopic density measurement considering all density-related effects, encompassing both morphological (e.g., porosity) and structural (e.g., lattice compression) factors"* | [인쇄] p.2–3 · p.11 |
| CT | 화소 **1.277 µm** · Ilastik 기계학습 분할 · ImageJ 문턱 공극 (공극 % 미보고) | [인쇄] Fig 2–3 캡션 · p.11–12 |
| ED-XRD | 백색광 15–100 keV · 검출기 7 개 (≈8°) · Le Bail 결정밀도 · WH 변형 | [인쇄] p.11 · SI Note S1–S2 |
| NPD | ILL D20 · λ 1.539 Å · VX PE 프레스 · TiZr 구형 개스킷 · Pb 압력 표지 · ≈100 mg · *"0 MPa corresponds to the pressure in the cell after the clamp is locked"* · Fullprof Rietveld | [인쇄] p.7 · p.11 |
| EIS | 실험실 PE 프레스 앤빌에 BioLogic SP300 직결 · 10–30 mV · 7 MHz – 10 Hz · 압력 안정 뒤 3 회 연속 · KK 잔차 < 5 % · RelaxIS 3 · σ 는 펠릿 기하로 정규화 (두께 출처 [미확인]) | [인쇄] p.11 |
| 이론밀도 (문헌) | LPS 1.85–1.93 (결정 LPS 기준) · LPSCl **1.77–1.88 g/cm³** — 저자가 Sakuda 2013 의 LPS 이론밀도 (360 MPa + 200 °C 펠릿 기하) 를 의심 | [인쇄] p.3 |

### 3-2. ★ 흡수 (거시) 밀도 vs 압력 — Fig 1 (p.2) [판독]
| p (MPa) | 334 | 479 | 822 | 1154 | 1461 | 2554 | 3770 | ↓ 3120 | ↓ 1931 | ↓ 1144 |
|---|---|---|---|---|---|---|---|---|---|---|
| LPSCl (g/cm³) | 1.562 | 1.828 | 1.917 | 1.985 | 2.028 | 2.095 | 2.089 | 2.034 | 1.944 | **1.862** |
- LPS: 67–333 MPa ≈1.14 (변화 없음) → 480 1.45 → 820 1.80 → ≈1150 2.05–2.10 → 3772 2.24 [판독].
- 본문: LPSCl 최대 **2.10 g/cm³ = 이론밀도의 ≈110–120 %** · LPS 2.2 (113–119 %) · **≈600 MPa 에서 LPSCl 이 이미 이론밀도를 넘고** LPS 는 ≈900 MPa 에서 자기 이론밀도에 닿는다 · 66 · 135 MPa 의 LPSCl 은 기술 문제로 결측 [인쇄] p.2–3.
- 감압: *"For LPS, the density–pressure curve during unloading closely follows that recorded during compression … In contrast, LPSCl exhibits slightly lower density values upon decompression, suggesting a greater degree of irreversible (plastic) deformation."* [인쇄] p.3.  [우리 산술] 같은 압력 비교 ≈1150 MPa: 가압 1.985 ↔ 감압 1.862 (−6.2 %) · ≈1931 MPa: 가압 보간 ≈2.057 ↔ 감압 1.944 (−5.5 %).

### 3-3. ★ 결정 (격자) 밀도 vs 압력 — SI Fig S2 · Note S1 (SI p.2) [판독]
| p (MPa) | 67 | 136 | 331 | 480 | 822 | 1155 | 1461 | 2552 | 3122 | 3770 | ↓ 1931 | ↓ 1143 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ρ_cryst (g/cm³) | 1.864 | 1.856 | 1.861 | 1.868 | 1.879 | 1.896 | 1.898 | 1.946 | 1.978 | **2.008** | 1.938 | **1.925** |
- Note S1: 136 → 1461 MPa 거의 선형 (흔들림 큼) = 공극 감소 · 접촉 (변형 없음) 단계 · 1461 → 3772 MPa 매우 선형 = 격자 변형 · 최대 **2.01 g/cm³** · *"When decreasing the pressure, the crystallographic density remains higher than that of the pristine sample, indicating some permanent change to the lattice parameter."* [인쇄] SI p.2.
- ⚠ [우리 산술] **흡수 밀도 > 결정밀도** (822 MPa 1.917 > 1.879 · 1154 1.985 > 1.896 · 2554 2.095 > 1.946 · 3770 2.089 > 2.008) — 공극이 음수가 된다 → 흡수 밀도의 절대 보정 (시료 두께 · 조성 가정) 또는 두 측정의 압력 배정이 어긋남.  저자는 이 비교를 하지 않았다 (대신 문헌 이론밀도의 정확도를 의심).
- ⚠ [우리 산술] ED-XRD 결정밀도의 저압 변화 (67 → 822 MPa +0.8 %) 가 NPD 격자 (0 → 630 MPa 부피 −2.4 %, 아래 §3-4) 보다 훨씬 작다 — 압력 교정 (NaCl 관 ↔ 시료) 또는 다공 분말 안 응력 분배 차이 [미확인].

### 3-4. NPD — 격자상수 · Li 자리 · 변형 (Fig 6–7 · SI Table S1–S2 · p.7)
| p (MPa) | 0 | 630 | 1146 | 1699 | 2249 | 2731 | 3809 | 2255 ↓ | 1837 ↓ |
|---|---|---|---|---|---|---|---|---|---|
| a (Å) | 9.85014(32) | 9.76971(118) | 9.70705(110) | 9.65429(146) | 9.60589(144) | 9.57007(150) | 9.48811(165) | 9.60592(143) | 9.64875(146) |
| Li1 x=y | 0.18517(115) | 0.18434 | 0.18408 | 0.18625 | 0.18598 | 0.19450 | 0.19476 | 0.18444 | 0.18554 |
| strain (%) | 0.16(01) | 1.2(01) | 1.4(01) | 1.51(01) | 1.64(01) | 1.68(01) | 1.74(01) | 1.64(01) | 1.517(1) |
- [인쇄] SI Table S1 (R_Bragg 10.2–22.8 % · Rwp 1.54–1.95 % · χ² 1.38–2.77).  0 MPa 정제 구조 (Table S2): Cl/S 자리 섞임 Cl1 0.0169 · S1 0.0266 (4a) / Cl2 0.0266 · S2 0.0169 (4d).
- 본문: *"Increased pressure leads to greater anisotropy in lattice spacings, with these changes fully reversible after unloading."* · 변형은 지수적으로 오르다 ≈1000 MPa 위 평탄 · **3810 MPa 1.75 %** (Faka LPSBr 와 일치) [인쇄] p.7.
- Li⁺ 이동: *"At approximately 2609 MPa, Li+ ions shift 4.9 ± 2.2 % along the x direction in 48h (x,x,z) sites"* — 감압 뒤 제자리 [인쇄] p.7.  ⚠ Table S1 에 2609 MPa 행은 없다 (0 → 2731 MPa 에서 x 가 +5.0 % [우리 산술]).
- ★ [우리 산술 — Table S1, V = a³, 3 차 Birch–Murnaghan]: **K₀ = 22.9 ± 1.0 GPa · K′ = 7.2 ± 0.7** (K′ = 4 고정 2 차: 27.5 ± 0.7 GPa) · 0 → 630 MPa 할선 25.6 GPa ↔ 우리 DFT B₀ **26.23** (comp1) — 같은 자릿수 · 0.1 / 0.3 / 0.5 / 1.0 GPa 의 고체 부피 변화 −0.43 / **−1.24** / −2.0 / −3.7 %.  (이웃 카드 `faka2026_…` Table S3 DAC 할선 ≈27 GPa 와도 맞다.)

### 3-5. ED-XRD 선폭 · WH 변형 (Fig 5 · SI Note S2 · Fig S5–S6)
- Fig 5 압력: 가압 66 · 135 · 331 · 479 · 821 · 1155 · 1461 · 2553 · 3771 MPa → 감압 3120 · 1931 · **1143 MPa** [인쇄 — 범례].  새 상 없음 · ≈331 MPa 에서 30° · 31.5° 반사 세기 역전 (검출기 · 적분 문제 추정, 저자) [인쇄] p.6.
- WH 변형 (Fig S6) [판독, 육안]: 66 → 0.40 % · 135 0.45 · 331 1.03 · 479 1.12 · 821 1.75 · 1155 1.81 · 1461 1.90 · 2553 1.99 · 3771 2.00 → 감압 1931 2.05 · 1143 1.97 %.
- SI Note S2: *"Most of the strain is introduced between 66 MPa and 821 MPa (+ 1.35 %), followed by a comparatively smaller increment (+ 0.25 %) up to 3771 MPa. During decompression, the anisotropic strain remains relatively stable, with values consistently higher than those recorded during compression."* · Faka LPSBr 1.51 % (1.5 GPa) · 2.26 % (10 GPa) 와 같은 크기 [인쇄] SI p.6.
- ⚠ **내부 긴장**: NPD 변형 (Rietveld 이방성, Table S1) 은 감압에서 **완전 가역** (2249 ↔ 2255 released 둘 다 1.64 %) · ED-XRD WH 는 **비가역** — 서로 다른 양 (Fullprof 미세변형 ↔ WH 선폭) 이고, 감압 최저 압력도 다르다 (NPD 1837 · ED-XRD 1143 MPa).

### 3-6. ★ σ_ion vs 압력 — Fig 8 (p.8) [판독]
| p (MPa) | 66 | 135 | 329 | 478 | 682 | 821 | 1013 | 1155 | 1461 | 2554 | 3124 | 3772 | ↓ 1930 | ↓ 1143 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LPSCl (mS/cm) | 2.62 | **3.34** | 3.21 | 2.92 | 2.61 | 2.27 | 1.93 | 1.61 | 1.15 | 0.44 | 0.28 | **0.14** | 0.94 | **2.21** |
| LPS (mS/cm) | 0.120 | 0.166 | 0.220 | **0.239** | 0.220 | 0.198 | — | 0.164 | 0.134 | 0.066 | 0.048 | **0.026** | 0.156 | **0.300** |
- 본문: LPSCl 최대 **3.3 mS/cm @135 MPa** · LPS **0.33 mS/cm @479 MPa** · 3771 MPa 에서 LPSCl **0.14** · LPS **0.06 mS/cm** [인쇄] p.7–8.  ⚠ LPS 두 값은 그림 판독 (0.24 · 0.026) 과 다르다 (§10-3).
- [우리 산술] 감압 > 가압 (같은 압력): ≈1150 MPa LPSCl 2.21 ↔ 1.61 (+37 %) · LPS 0.300 ↔ 0.164 (+83 %) — 초록 *"irreversible conductivity enhancement, attributed to plastic densification and increased structural disorder"*.
- 0 → 135 MPa 의 상승 = *"most likely associated with improved contact between particles rather than intrinsic changes in the LPSCl crystal lattice"* [인쇄] p.9.
- 활성화 부피 (Fig 11 · Note S3, ΔV_a ≈ −k_BT ∂ln(σT)/∂p): **LPSCl 2.32 · LPS 2.17 cm³/mol** (선형 영역 ≈700 → 3800 MPa) · 비교: Na₃PS₄ 1.78 / 2.33 · Faka Li₆PS₅Br 0.6–1.2 · α-Li₂SO₄ 0.6 cm³/mol [인쇄] p.9.  [우리 산술] 판독 기울기 (682 → 3771 MPa) 로 2.34 cm³/mol — 재현.  ⚠ Fig 11 세로축 ln(σT) 값 (LPSCl ≈6.9 @135 MPa) 은 σ 를 mS/cm 로 넣어야 나온다 — 축 단위 표기 "S·K·m⁻¹" 와 어긋남 (기울기 · ΔV 는 무관).
- BVEL (Fig 9–10): Li 자리 에너지 −6.51 → −6.88 eV · 퍼콜레이션 에너지 **0.64 → 0.87 eV** (0 → 3809 MPa) · 감압 점들은 같은 선 [판독] · 저자: BVEL 은 이완을 무시해 활성화 에너지를 과대평가 [인쇄] p.9.  ⚠ Fig 10 캡션은 (a) 퍼콜레이션 · (b) 자리 에너지라 적지만 그림 · 본문은 반대 (a 자리 · b 퍼콜레이션).

### 3-7. 미세구조 (Fig 2–4 · S1)
- CT LPSCl (Fig 2, 1.277 µm): 66 MPa 입계 · **입내** 공극 · 고밀도 불순물 입자 (영상 정합 표지) → 479 MPa 입계 공극 대부분 닫힘 (일부 남음) · 입내 공극 남음 → **1155 MPa 모든 공극 사라짐** (입내 공극 닫힘 = 입자 파쇄 후 재치밀화 또는 큰 응력) → 1150–3800 MPa 변화 없음 (해상도 아래) [인쇄] p.3–4.
- LPS (Fig 3): 70 MPa 큰 입자 (LPSCl 최대 입자의 ≈2 배) · 공극은 입자 둘레 · 입내 공극 없음 · 치밀 LPS 가 더 밝음 (밀도 높음) [인쇄] p.4.
- [판독] CT 의 LPSCl "입자" 는 수십 µm (200 µm 막대 기준) — 추정 입경 5 µm (원문) 와 달라 **응집체**로 보인다.
- 파면 SEM (Fig 4, 3.7 GPa 뒤): LPSCl = **입계 파괴** (입계 강도 < 입자) · *"the pellet exhibited spontaneous fracture several minutes after removal from the Paris–Edinburgh (PE) press. This provides strong evidence of residual stress and strain trapped within the LPSCl sample"* · LPS = 매끈한 파면 + hackle (빠른 취성 파괴) [인쇄] p.4–5.
- 저자 해석: 실온 치밀화는 확산이 없어 입계가 응력을 품은 채 남는다 → 사이클 중 입계 균열 위험 · Cronau 2021 (적층압 200–250 MPa 없으면 결정 LPSCl 입자가 떨어진다) 와 같은 맥락 [인쇄] p.5.

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리

### 4-1. 측정 사슬
분말 → 기밀 셀 (개스킷 · PTFE · 황동) → UToPEC 하중 단계 (하중 → NaCl 교정 곡선으로 압력) → 단계마다 흡수 밀도 · CT · ED-XRD (같은 시료) → 감압 (≈1.15 GPa 까지) / 별도: D20 NPD (0 → 3809 → 1837 MPa) / 별도: 실험실 PE 프레스 EIS (같은 압력 조건) → 3.7 GPa 시료 회수 파면 SEM.
- 공통 측정량이 아닌 것 셋: 흡수 밀도 (거시) · 결정밀도 (Le Bail) · NPD 격자 — 압력 배정 · 시료가 서로 다르다.

### 4-2. ★ 입자 처리
- 실험: 실제 분말 — LPSCl 은 큰 입자가 깨지고 (Korjus 2025 인용) 입내 공극까지 닫히며, 고압에서 격자 수준 변형 · 결함 (WH) · Li 자리 이동 (NPD).  LPS 는 비정질 · 무른 · 깨지지 않고 치밀화 (저자).
- 우리 대응: 300 MPa 는 이 논문의 **1 단계 (입계 공극 닫힘)** 안 — DEM (재배열 · 접촉) · MPM (형상 소성 · 공극 채움) 이 겨누는 영역.  2 단계 (격자 수준 · 결함) 는 둘 다 모델 밖 (MPM 은 J2 소성 · 결정 결함 없음).

### 4-3. 기법 미니 용어집
- **PE (Paris–Edinburgh) 프레스**: 준원뿔 앤빌 + 개스킷 매질로 큰 시료에 수 GPa 를 거는 장치 — 응력 상태는 **준등방**.
- **Beer–Lambert 흡수 밀도**: 감쇠 계수 · 시료 두께 · 조성으로 거시 밀도를 내는 방법 — 공극 + 격자 압축이 섞인 값.
- **Le Bail 결정밀도**: 회절 격자상수에서 계산한 고체 자체 밀도 (공극 무관).
- **WH 변형**: 선폭에서 뽑은 비균일 (이방) 미세변형 — 결함 · 전위 지표.
- **활성화 부피 ΔV_a**: 이온이 안장점으로 갈 때의 부피 변화 = −k_BT ∂ln(σT)/∂p.
- **BVEL**: 결합원자가로 만든 Li 에너지 지형 — 퍼콜레이션 에너지 = 연결 경로가 생기는 최소 에너지.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 흡수 밀도 vs 압력 (LPS · LPSCl, 가압 · 감압, 오차막대) | ★ 거시 밀도 감압 비가역 (LPSCl) · CL-94 산술 재료 (절대 보정 문제 한정) |
| 2 | LPSCl CT 9 단계 (66 → 3771 MPa, 1.277 µm) — 입계 · 입내 공극 · 불순물 표지 | 두 단계 치밀화의 영상 근거 |
| 3 | LPS CT 9 단계 | 비교 |
| 4 | 3.7 GPa 시료 파면 SEM (LPSCl 입계 · LPS hackle) | 잔류 응력 · 입계 파괴 |
| 5 | ED-XRD 반사 (30–32° · 45–48°, 2θ Cu 환산) 가압 · 감압 | ★ 반사 이동 가역 · 선폭 비가역 (Codex 인용 근거) |
| 6 | NPD Rietveld (0 MPa) · a(p) · 변형(p) — 감압 점 같은 선 | ★ 격자 가역 · 체적탄성률 산술 |
| 7 | Li 좌표 (x · z) vs p | Li 자리 이동 |
| 8 | σ_ion vs p (LPSCl 왼축 · LPS 오른축 /10) | ★ 135 MPa 최대 · 감압 비가역 증가 |
| 9 | LPSCl 구조 + Li BVEL (0.64 eV) | 이동 경로 |
| 10 | BVEL 자리 에너지 · 퍼콜레이션 에너지 vs p (캡션 a/b 뒤바뀜) | 고유 σ 압력 의존 근거 |
| 11 | ln(σT) vs p — 활성화 부피 2.32 · 2.17 cm³/mol (자동 추출이 놓쳐 손 크롭) | 고유 σ 압력 의존 크기 |
| 12 | UToPEC 배치 · 기밀 클램프 · 셀 단면 (PEEK · 붕소–에폭시 · 황동 · PTFE) | 장치 |
| S1 | 분말 SEM (LPS · LPSCl) | 입자 형상 |
| S2 | 결정밀도 vs 압력 (가압 · 감압) | ★ 격자 쪽 밀도 · 흡수 밀도와 대조 |
| S3 · S4 | ED-XRD 전체 (LPSCl · LPS) | |
| S5 · S6 | WH 그림 · WH 변형 vs 압력 (감압 고리) | ★ 선폭 비가역 정량 |
| S7 (+S7a) | NPD Rietveld (가압 · 감압 패널) — 두 쪽에 걸쳐 S7a 를 손 크롭 | |
| S8 | 하중–압력 교정 곡선 (NaCl, 이력 고리) | 압력 배정 · 감압 가지 해석 |
| Table S1–S2 | NPD 정제값 · 0 MPa 구조 (래스터 표라 손 크롭) | ★ K₀ 산술 입력 |

## 6. Post-processing ★
- **무엇을**: 흡수 프로파일 → 밀도 (NIST) · CT 재구성 (h5) → ImageJ · Ilastik 분할 · ED-XRD 7 검출기 병합 (자체 Python) → Le Bail 결정밀도 · WH (분할 pseudo-Voigt, 반사 6 개) · NPD Fullprof Rietveld (셀 반사 구간 제외) → 격자 · Li 좌표 · 변형 · BVEL (Bond_STR) · EIS RelaxIS (KK) → ln(σT) 기울기 → ΔV_a.
- **안 한 것**: 공극 % 수치 · Heckel · 두께 회복 · 무하중 감압 · 반복 통계 · 흡수 밀도 ↔ 결정밀도 일관성 점검.
- **우리 후처리 (이 카드)**: Fig 1 · S2 · 8 · S6 판독 · 흡수/결정 밀도 대조 (음의 공극 발견) · NPD BM3 맞춤 (K₀ · K′) · ΔV_a 재현.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · `docs/` 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 응력 상태 | **준등방** (PE 프레스 개스킷) · 0.07–3.8 GPa | 일축 판 압축 (DEM 판 · MPM 플래튼) · 300 MPa · 측방 주기 | 응력 경로 다름 — 밀도 · 회복 수치 전이 금지 |
| 순수 SE 300 MPa 공극 | ≈16 % [우리 산술 — 흡수 1.562 ÷ 결정 1.861 @≈331 MPa] · 문헌 TD 로 12–17 % | MPM 보정 표적 ≈10 % — 출처 철회 (`CL-94`) | §7-3 |
| 회복 · 비가역 | 격자: 가역 (NPD) · 선폭 · σ · 거시 밀도: 비가역 · 감압 ≥1.1 GPa | DEM 언로딩 등록 (ρ_c, P_meas 1 MPa, 판 속도 0.01 mm/s) · MPM 제하 팔 없음 | §7-2 |
| SE 체적탄성률 | [우리 산술] K₀ 22.9 (K′ 7.2) / 27.5 (K′ 4) GPa | DFT B₀ **26.23** · MPM K = E/(3(1−2ν)) = **25.5 GPa** (E 1.53 · ν 0.49) · DEM E_eff 1.35 GPa (연화) | ★ 실험 K₀ 가 DFT · MPM 의 체적 강성과 같은 자릿수 = MPM ν 0.49 선택 (부피는 실물, 전단만 연화) 의 독립 실험 근거 |
| 고유 σ 압력 의존 | ΔV_a 2.32 cm³/mol (> 0.7 GPa) | σ₀ 펠릿 3.0 (봉인) / 보고 1.5 mS/cm — 압력 무관 상수 | 300 MPa 아래는 접촉 지배 영역이라 영향 작음 · 고압 외삽 금지 근거 |
| 두 단계 치밀화 | ≲500 MPa 입계 공극 · 그 위 격자 | DEM · MPM 은 1 단계만 (격자 결함 없음) | 우리 300 MPa = 1 단계 안 |

### 7-2. ★ 언로딩 시험 (ρ_c) — 무엇을 주나 · 무엇을 못 주나
- **못 준다**: 무하중 · 저하중 회복률 (감압은 ≈1.1–1.8 GPa 에서 멈춤) · 두께 · 복합체.
- **준다 (정성)**: ① **격자 탄성은 되돌아간다** (NPD a: 2249 ↔ 2255 released 차 0.00003 Å) — SE 탄성 회복을 0 으로 둘 수 없다 (Codex 판정의 같은 문장) ② 같은 ≈1150 MPa 에서 **거시 (흡수) 밀도는 감압 가지가 6.2 % 낮은데 (1.862 ↔ 1.985) 결정 (격자) 밀도는 감압 가지가 1.5 % 높다 (1.925 ↔ 1.896)** [판독] → 그 차는 고체가 아니라 **공극 · 균열 재개방** 쪽이라는 정성 신호 (오차막대 ±0.03–0.04 g/cm³ · 흡수 밀도 절대 보정 문제 §10-1 한정) ③ 시료가 꺼낸 뒤 **저절로 깨질 만큼 잔류 응력**.
- 우리 DEM 언로딩에서 ①은 접촉 겹침 탄성 회복 (hysteresis 분기) 으로 담기고, ② · ③ (균열 · 입계 분리) 은 SE–SE 결합 · 파괴가 없는 DEM 에 **없다** — 결과 보고 때 "모델에 없는 회복 기구" 로 적을 항목.

### 7-3. ★ CL-94 · V2
- 직접 공극 값은 없고, 두 측정을 엮은 우리 산술 (≈16 % @≈331 MPa) 은 ① 준등방 ② 흡수 밀도 절대 보정 문제 (≥800 MPa 에서 결정밀도 초과) ③ 다른 분말 (NEI 5 µm 추정, 응집체) — **CL-94 후보로 쓰지 않는다** (이웃 카드 lee2025 · faka2026 의 일축 in-die 곡선이 앞선다).
- V2 관점의 가치: **측정량 정의** — 흡수 밀도는 *"porosity + lattice compression"* 을 다 담는다 (저자 명시).  우리 DEM ε (구 부피 합 · 고체 비압축) 과 비교하려면 고체 압축 몫 (NPD BM3: 0.3 GPa 에서 −1.24 %) 을 빼야 한다 — in-die 공극 보정 크기의 **실험 근거**.

### 7-4. E · K — frame[2] 의 3 층과
- 실험 K₀ (22.9–27.5 GPa) ≈ DFT B₀ 26.23 ≈ MPM 의 K 25.5 (ν 0.49) — **"MPM 은 부피 강성을 실물로, 전단만 연화" (CORRECTION 1 · 3D 3-fix 의 ν 0.49)** 가 실험 격자 압축률과 같은 자릿수라는 독립 근거 (단 결정 격자의 K 는 분말 덩어리의 체적 강성이 아니다).
- DEM E_eff 1.35 GPa 는 이 층 (물성) 과 다른 층 (재배열 대리) — 이 논문 값으로 DEM 을 다시 맞추지 않는다 (frame[4]).

### 7-5. frame[5]
- **가진 것**: 순수 SE 의 기계 (거시 · 격자 밀도, CT, 결함) + 수송 (σ, ΔV_a) — 같은 압력 축.
- **없는 것**: 다이 압축 · 무하중 회복 · 복합체 · 접촉 · 모델.

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **Codex 인용 (Thompson) 원문 확인 완료** — 판정문 130 행 문장은 원문과 맞는다 (§0 첫 행).  우리 글에서 쓸 때: *"감압 시 회절 피크 이동은 가역 (탄성 격자 변형), 선폭은 대부분 비가역 (Thompson 2026 §4.1, 감압은 ≈1.1 GPa 까지)"* — 감압 하한을 함께 적는다.
2. **in-die 공극 보정 크기**: 고체 압축 −1.24 % @0.3 GPa (NPD BM3) — lee2025 · faka2026 의 in-die 공극에 ≈+1 %p 를 더해 읽을 근거.
3. **MPM ν 0.49 의 실험 근거** (§7-4) — 3D MPM 보정 문서 · 발표에서 "K 25.5 ≈ 실험 격자 K₀ 23–28 GPa" 로 쓸 수 있다 (출처 = 이 카드 산술 · 결정 K 와 분말 K 구분).
4. **잔류 응력 · 입계 파괴** — 언로딩 뒤 SE 펠릿이 깨질 수 있다 = 실험 두께 측정 (다이 밖) 의 해석 위험 (우리 ps45 실험은 다이 안 측정).
5. **고압 σ 하락 (ΔV_a 2.32)** — 우리 σ₀ 를 고압으로 외삽하지 않는다 · 300 MPa 근처 실험 σ 의 정점 (LPSCl 135 MPa) 은 접촉 지배 효과.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Upon decompression from ≈3.8 GPa (down to ≈1.1 GPa), the diffraction-peak shift of Li₆PS₅Cl is reversible (elastic lattice strain) while the peak broadening is largely irreversible (Thompson et al., *Adv. Funct. Mater.* 2026)."
- "Neutron diffraction lattice parameters of Li₆PS₅Cl from 0 to 3.8 GPa give K₀ ≈ 23 GPa (K′ ≈ 7; our Birch–Murnaghan fit to their Table S1), comparable to the DFT bulk modulus used in our MPM (B₀ = 26.2 GPa)."
- 국문: *"Li₆PS₅Cl 는 3.8 GPa 압밀 뒤 감압해도 거시 밀도 · 선폭 · σ 변화가 남고 (비가역), 셀에서 꺼내면 몇 분 안에 입계로 깨진다 — 잔류 응력이 크다 (Thompson 2026)."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **흡수 밀도 > 결정밀도 (≥800 MPa)** [우리 산술] — 음의 공극.  저자의 "이론밀도의 110–120 %" 해석 (문헌 TD 의심) 보다, 같은 논문 결정밀도 (최대 2.01) 와의 어긋남이 먼저다.  흡수 밀도 절대값 인용 금지 · 경향만.
2. **준등방 ↔ "uniaxial"**: 초록은 "uniaxial compression up to 3700 MPa", 실험편은 "quasi-isostatic compression conditions" — 응력 상태 서술 불일치.
3. **LPS σ 본문 ↔ 그림**: 0.33 mS/cm @479 (본문) ↔ 0.24 (판독) · 0.06 @3771 ↔ 0.026 — LPSCl 값은 본문 · 그림 일치.
4. **감압 하한** — 흡수 · ED-XRD ≈1143–1150 MPa · NPD 1837 MPa · EIS ≈1143 MPa: 모든 "가역 / 비가역" 판정이 GPa 수준 잔류압에서.  하중–압력 교정 자체가 이력을 갖는다 (Fig S8).
5. **결정밀도 저압 변화 ↔ NPD 격자** — ED-XRD 67 → 822 MPa +0.8 % vs NPD 0 → 630 MPa 부피 −2.4 % — 압력 교정 · 시료 응력 분배 [미확인].
6. **본문 · 캡션 소소한 어긋남**: "2609 MPa" Li 이동 (표에 없는 압력) · Fig 10 캡션 (a)/(b) · Fig 11 축 단위 · Fig S8 축 "Pressure (GPa" (값은 MPa) · NPD 의 "0 MPa" = 클램프 체결 뒤 압력 (진짜 0 아님).
7. **입경**: NEI "추정 5 µm" ↔ CT 의 수십 µm 입자 (응집체) — PSD 측정 없음.
8. **반복 · 시료 수 [미확인]** · σ 는 다른 실험 (실험실 PE) 이고 두께 출처 [미확인].
9. **전이 한계**: 순수 SE · 준등방 · GPa 영역 ↔ 우리 복합체 · 일축 · 300 MPa.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 2 | P. Perrenot, A. Fauchier-Magnan, M. Mirolo, et al., *Adv. Funct. Mater.* 34 (2024): 2310739 (Room-Temperature Sintering of Amorphous Li₃PS₄) | 같은 그룹 · 실온 소결 · 형태 ↔ 전기화학 |
| 3 | L. Lin, A. Ayyaswamy, Y. Zheng, et al., *ACS Energy Lett.* 9 (2024): 2387–2393 (Nonintuitive Role of Solid Electrolyte Porosity on Failure) | 공극 ↔ 파괴 |
| 4 | M. Cronau, M. Szabo, C. König, T. B. Wassermann, and B. Roling, *ACS Energy Lett.* 6 (2021): 3072–3077 | 정본 카드 있음 |
| 7 | O. Maus, M. A. Lange, F. Frankenberg, et al., *Adv. Energy Mater.* 15 (2025): 2403291 | 후처리가 Li₅.₅PS₄.₅Cl₁.₅ 구조 · 수송에 주는 영향 |
| 9 | A. Yao, S. Kadota, S. Hiroi, et al., *J. Solid State Electrochem.* 28 (2024): 4401–4407 | Li₃PS₄ in situ 고압 구조 |
| 10 · 11 | V. Faka et al., *Energy Adv.* 2 (2023): 1915–1925 · *J. Am. Chem. Soc.* 146 (2024): 1710–1721 | 활성화 부피 · 압력 유도 전위 (LPSBr) |
| 14 | L. Henry, N. Guignot, A. King, … J.-P. Itie, *J. Synchrotron Radiat.* 29 (2022): 853–861 | PSICHÉ 흡수 밀도 방법 원전 |
| 16 | L. L. Baranowski, C. M. Heveran, V. L. Ferguson, and C. R. Stoldt, *ACS Appl. Mater. Interfaces* 8 (2016): 29573–29579 | Li₃PS₄ 다척도 역학 |
| 17 | A. Sakuda, A. Hayashi, and M. Tatsumisago, *Sci. Rep.* 3 (2013): 2261 | 정본 카드 있음 — 이론밀도 의심의 대상 |
| 20 | O. Korjus, S. Mitra, Q. Berrod, et al., *Energy Storage Mater.* 82 (2025): 104589 | ★ 같은 1저자 그룹 · Li₆PS₅Cl 치밀화 다척도 (큰 입자 파쇄) — 미 digest |
| 36 | T. Famprikis, Ö. U. Kudu, J. A. Dawson, et al., *J. Am. Chem. Soc.* 142 (2020): 18422–18436 | 활성화 부피 비교 (Na₃PS₄) |
| 38 | C. L. Bull, A. Bocian, H. Hamidov, K. V. Kamenev, R. J. Nelmes, and J. S. Loveday, *Rev. Sci. Instrum.* 82 (2011): 076101 | PE 프레스 준정수압 조건 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 13 쪽 · SI 11 쪽 전부 렌더 이미지로 읽고 `pdftotext` 로 인용문 대조 · DOI `10.1002/adfm.75195` = 본문 1 쪽 인쇄 · Codex 인용 문장 (p.6 §4.1 · p.7 NPD · SI Note S1–S2) 을 텍스트 층과 렌더 둘로 확인.
- SI Table S1–S2 는 래스터 표 — 크롭 영상으로 칸마다 읽음 · BM3 맞춤은 Table S1 7 개 가압 점 (scipy curve_fit).
- 판독: Fig 1 · 8 (원 래스터 1000×816 · 1001×711, 눈금 탐지 + 색 표지) · Fig S2 (렌더 1514×769) · Fig S6 (육안).
- 그림 크롭 23 장 = 본문 Figure 1–12 · SI Figure S1–S8 (S7 두 쪽 → 2 장) · Table S1–S2 · **손 크롭 6 장** (fig_11 = 번호 공백으로 누락 · tab_S1 · tab_S2 = 래스터 표 쪽 전체로 잡힘 · fig_S2 앞 문단 혼입 · fig_S8 수식 줄 혼입 · fig_S7a = 두 쪽에 걸친 S7 의 p.7 패널).
- 정본 litdb 중복 확인: DOI · 저자명 (Villevieille · Le Floch) · 제목 낱말 papers/ 전수 grep — 없음.

## 🔗 관련 카드
- 같은 축 (압력 유도 변형 · in situ 치밀화): `faka2026_particle_size_consolidation_strain_lpscl` · `lee2025_heckel_argyrodite_powder_densification_nanoindentation` · `miss2026_insitu_conductivity_porosity_pressure_compaction`.
- 탄성 · 밀도 출처: `deng2016_elastic_superionic_electrolytes_dft` · `sakuda2013_sulfide_mechanical_property` · `adeli2019_halide_substitution_boosting_argyrodite` · `song2025_porous_argyrodite_modulus_fracture_toughness`.
- σ 측정 규약: `cronau2021_stack_pressure_ionic_conductivity` · `ohno2020_interlab_ionic_conductivity_argyrodite`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
