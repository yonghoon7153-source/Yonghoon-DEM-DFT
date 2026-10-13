<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = miss2026_insitu_conductivity_porosity_pressure_compaction.md (가압 중 두께 · 공극 · 회복).
     쪽 표기 = 학술지 인쇄 쪽 p.6342–6346 (본문 PDF n 쪽 = 인쇄 6341+n).  SI 는 "SI p.n" (SI PDF 쪽 = SI 인쇄 번호 1–11).
     값 표지: [인쇄] = 본문 · SI · 표 · 그림 안에 숫자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv —
     원 래스터 (Fig 1 836×690 · Fig 2 977×377 px) 에서 눈금 보정 + 색 띠 중앙값) · [우리 산술] = 이 논문 밖 값과 엮은 계산 · [미확인] = 원문 (본문 + SI 전수) 에 없음.
     원문 16 쪽 (본문 5 + SI 11) 은 렌더 이미지로 전부 읽었다.  그림은 전부 래스터. -->
# 분말 다이 압축 (DIC 로 펀치 탄성 뺀 가압 중 높이) 의 Heckel 단계 I–III 로 아지로다이트 SE 의 소성 순위 — Li₆PS₅Cl (상용 · 볼밀 · 합성) · Li₆PS₅Br · BH₄⁻ 치환 2 종: K (stage II) 25.0–41.3 ×10⁻⁴ MPa⁻¹ · 97 % TD 압력 510–725 MPa · 나노압입 H 0.66–1.68 GPa · E 15.6–30.5 GPa · H/E ∝ 1/K · 하중 제거 시 펠릿 탄성 회복 판독 0.23 mm (≈900 MPa 에서) — Lee · Han · Gong · Ahn · Yi · Cho (J. Mater. Chem. A 2025)

> slug `lee2025_heckel_argyrodite_powder_densification_nanoindentation` · DOI `10.1039/d4ta08604j` · type `experiment (in-die 일축 압축 + DIC 높이 · Heckel · 이온밀링 단면 SEM 공극 · 나노압입 Oliver–Pharr · 시뮬레이션 없음)` · PDF `3. Characterization of densification behavior and mechanical properties of solid electrolyte powders for all solid-state batteries.pdf` · SI `3. Sup) Characterization of densification behavior and mechanical properties of solid electrolyte powders for all solid-state batteries.pdf` · digested `2026-10-13` · status ✅
>
> **저자**: Seung-Yong Lee‡ (KIMS) · Ji-Hoon Han‡ (서울대 · KIST) · Hyun-Woo Gong · Jae-pyoung Ahn (KIST 분석센터) · Kyung-Woo Yi (서울대) · **Young Whan Cho\*** (KIST 수소에너지소재) — ‡ 공동 1저자 · *J. Mater. Chem. A* **2025**, 13, 6342–6346 (**Communication**, 본문 5 쪽 + ESI 11 쪽) · 접수 2024-12-04 · 승인 2025-02-06 · 출판 2025-02-17 · **CC-BY-NC 4.0**.
> **이웃 카드 (링크만)**: [`miss2026_insitu_conductivity_porosity_pressure_compaction`](miss2026_insitu_conductivity_porosity_pressure_compaction.md) (가압 중 · 제거 뒤 두께 — Li₅.₅PS₄.₅Cl₁.₅) · [`schneider2023_particle_size_pressure_transport`](schneider2023_particle_size_pressure_transport.md) (본문 ref 31 — Heckel in die, t-Li₇SiPS₈) · [`sakuda2013_sulfide_mechanical_property`](sakuda2013_sulfide_mechanical_property.md) (ref 6) · [`song2025_porous_argyrodite_modulus_fracture_toughness`](song2025_porous_argyrodite_modulus_fracture_toughness.md) · [`deng2016_elastic_superionic_electrolytes_dft`](deng2016_elastic_superionic_electrolytes_dft.md) (ref 25 계열 DFT 탄성).
> **판독 원자료**: `litdb/figures/lee2025_heckel_argyrodite_powder_densification_nanoindentation/digitized.csv` (77 행 — Fig 1c 기준선 · Fig 1d · 2a · 2b).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 상용 Li₆PS₅Cl 분말을 ⌀8 mm 지르코니아 다이에서 **연속 가압** (크로스헤드 1 mm/min) 하며 DIC 로 펀치 탄성 (σL/E) 을 뺀 **가압 중 펠릿 높이**를 재 Heckel 곡선 전체를 준다 — **우리 CL-94 축의 첫 "순수 Li₆PS₅Cl 가압 중 공극 vs 압력" 연속 곡선** (판독 300 MPa ≈15 %) 과
**하중 제거 회복 한 점** (≈900 MPa → 0 에서 펠릿 0.233 mm ≈ 높이의 4.7 %) 이다.  ⚠ 그러나 **이론밀도 (TD) 인쇄값 1.64 g/cm³ 가 결정학 밀도 1.86 보다 12 % 낮다** — 글자 그대로면 공극 절대값이 크게 달라지므로 (§3-4) 앵커 지위는 그 확인 뒤다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① DEM 언로딩 (ρ_c) 의 실험 규모 | **상용 Li₆PS₅Cl 순수 펠릿, 다이 안, ≈900 MPa → 0 (무하중) 회복 = 0.233 mm** (펀치 몫 0.200 mm 뺀 뒤) · 펠릿 높이 ≈5 mm → **≈4.7 %** · 하중 제거 후 수 초 안의 급락 (Fig 1c 시간축) · 저자 해석 = 균열 없는 **탄성 회복** | [판독] Fig 1c (p.6343) · 높이 5 mm [인쇄] SI p.3 · % [우리 산술] |
| ② CL-94 (순수 SE 300 MPa 공극) | **가압 중 (in-die, 하중 아래) 상용 Li₆PS₅Cl ≈15 %** (Fig 1d −ln(1−ρ) 1.90 → 14.9 % · Fig 2a 1.83–1.91 → 14.8–16.1 %) · 합성 Li₆PS₅Cl ≈18 % (Fig 2b, 가려짐) — **TD 1.64 기준** | [판독] · TD [인쇄] SI p.3 |
| ③ V2 (상태 · 측정량 · 원측정 · 불확도) | 상태 = 가압 중 · 연속 하중 · 측정량 = 질량 / (A·h_DIC) ÷ TD · 원측정 = 힘–변위 (SI Fig S4, **합성 시료 4 종만** — 상용 곡선 원자료 없음) · 불확도 = K 의 ± (0.11–0.16) 만 · 반복 수 [미확인] · **고체 자체의 탄성 압축 보정 없음** · TD 출처 불일치 | [인쇄] SI p.2–3 · §3-4 |
| ④ Heckel (DEM 순수 SE P_y 138 MPa) | **K (stage II): 상용 Li₆PS₅Cl 32.3 · 볼밀 34.0 · 합성 Li₆PS₅Cl 29.1 · Li₆PS₅Br 25.0 · BH₄ 37.0 / 41.3 (×10⁻⁴ MPa⁻¹)** → P_y = 1/K = Li₆PS₅Cl **294–344 MPa** [우리 산술] — DEM 138 MPa 보다 2.1–2.5 배 단단 | [인쇄] p.6343 · Table 1 |
| ⑤ E 축 (DEM 1.35 · MPM 1.53 GPa ↔ 실 22–24) | 나노압입 E: Li₆PS₅Cl 27.6 · Li₆PS₅Br 30.5 · BH₄ 15.6 / 19.1 GPa (2.5–7.3 % 공극 펠릿) · H 1.41 / 1.68 / 0.69 / 0.66 GPa | [인쇄] Table 2 |
| ⑥ τ 규약 | **없다** (수송 측정 없음) | — |

⛔ **한정어 (떼지 말 것)**: ① **TD 1.64 (Li₆PS₅Cl) · 1.90 g/cm³ (Li₆PS₅Br)** = 결정학 1.86 · 2.09 보다 12 % · 9 % 낮다 [우리 산술 §3-4] — 같은 논문의 단면 공극 2.5 % 와 글자 그대로의 TD 는 양립하지 않는다 ② 펠릿 **높이 5 mm · ⌀8 mm** (높이/지름 0.63 — 벽 마찰 큰 기하) · 연속 가압 1 mm/min ③ **in-die 값에 고체의 탄성 압축 보정이 없다** — 하중 아래 공극을 p/K 만큼 작게 읽는다 (300 MPa ≈1.2 %p, K 26 GPa 가정 [우리 산술]) ④ 회복은 **한 시료 · 한 압력 (≈900 MPa) · 판독** ⑤ 반복 · 시료 간 산포 [미확인] ⑥ 상용 SE (POSCO JK Solid Solution) 의 입경 [미확인].

---

## 1. 한 줄 요약
DIC 로 상 · 하 펀치의 실제 거리를 실시간 추적하고 펀치 탄성 (L 40 mm · E 180 GPa) 을 빼 **가압 중 펠릿 높이**를 얻은 뒤, Heckel 식 −ln(1 − ρ_rel) = Kσ + A 의 **단계 I (재배열 · 파쇄) · II (선형, 소성 지배) · III (치밀체 탄성)** 을 나눠 **stage II 기울기 K** 로 아지로다이트 SE 들의 소성 용이성을 비교했다.
Li₆PS₅Br < Li₆PS₅Cl < BH₄ 치환 순으로 K ↑ (= 항복 응력 ↓) · 97 % TD 도달 압력은 반대 순 (725 → 510 MPa).  나노압입 (8 mN, Oliver–Pharr) 의 H · E · **H/E (소성 지수)** 가 같은 순위를 정성적으로 준다 → *"the powder compression test is an effective method to evaluate the relative plasticity"* (p.6345).
볼밀한 상용 Li₆PS₅Cl 은 K 는 거의 같지만 (32.3 → 34.0) 단계 II→III 전이가 낮은 압력으로 당겨진다 (97 % TD 650 → 570 MPa) — **K 는 물질 고유 (조성 · 결정구조), 전이 압력은 입경 · 형상** 이라는 해석.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE) | 연구유형 |
|---|---|---|---|---|
| S.-Y. Lee‡ (KIMS) · J.-H. Han‡ (SNU/KIST) · H.-W. Gong · J.-p. Ahn (KIST) · K.-W. Yi (SNU) · **Y. W. Cho\*** (KIST) | J. Mater. Chem. A 13 (2025) 6342–6346 · CC-BY-NC | 10.1039/d4ta08604j | **상용 Li₆PS₅Cl (POSCO JK Solid Solution)** · 같은 분말 볼밀 (진동밀) · **합성 Li₆PS₅Cl · Li₆PS₅Br** (볼밀 + 550 °C 10 h) · **Li₅.₅₅PS₄.₅₅(BH₄)₁.₄₅ · Li₅.₁₅PS₄.₁₅(BH₄)₁.₈₅** (2 단계 볼밀, SI ref 1) — **단일상 SE 분말만 (CAM 없음)** | 실험 — 다이 압축 + DIC · Heckel · IMS-SEM 공극 · 나노압입 |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 장치 · 시료 (SI p.2–4 · p.6342–6343)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 다이 | **지르코니아 몰드 ⌀8 mm** (압축강도 ≈2000 MPa · E > 90 GPa) · 스테인리스 몰드로 해도 *"nearly identical results"* → 다이 변형 영향 무시 | [인쇄] SI p.2 |
| 펀치 · 속도 | 스테인리스 펀치 · **크로스헤드 1 mm/min** (연속 가압) | [인쇄] SI p.2 |
| 높이 측정 | **DIC** (GOM Correlate 2019 · 2752×2200 px 카메라 · 3 fps) — 상 · 하 펀치에 흰 실리카 모래를 탄소 테이프에 붙인 반점 무늬 | [인쇄] SI p.3 · p.6342 |
| 펀치 탄성 보정 | Δd = Δd_elastic + Δh_SE-powder = **σL/E** + Δh (Eq 1) · **L = 40 mm · E ≈180 GPa (DIC 로 실측, 문헌과 비슷)** | [인쇄] p.6343 |
| 상대밀도 | ρ_rel = 압축 펠릿 밀도 ÷ SE 이론밀도 (SI Eq 1) · 펠릿 밀도 = 분말 질량 ÷ 펠릿 부피 | [인쇄] SI p.2–3 |
| 시료량 | *"In order to achieve a height of 5 mm for all the pellets after compression, the amount of powder … was calculated … based on the theoretical density"* → **완전치밀 기준 높이 5 mm** | [인쇄] SI p.3 |
| 이론밀도 (TD) | **Li₆PS₅Cl 1.64 · Li₆PS₅Br 1.90 g/cm³** ("calculated") · BH₄ 치환 = Rietveld 기반 **≈1.45 g/cm³** 가정 | [인쇄] SI p.3 — ⚠ §3-4 |
| 최대 하중 | Fig 1a ≈890 MPa 까지 · SI Fig S4 힘 ≈4500 kgf (축 이름 "Stress (kgf)" 오기) ≈ **878 MPa** (⌀8 mm) · Fig 1c 펀치 몫 0.200 mm ⇒ σ = 0.200·E/L ≈ **900 MPa** | [판독] + [우리 산술] |
| 합성 | Li₂S (99.9 %) · P₂S₅ (99 %) · LiCl · LiBr (99 %) · LiBH₄ (95 %) · 80 mL Si₃N₄ 용기 · ⌀10 mm ZrO₂ 볼 30 개 · **650 rpm 3 h** (5 분마다 5 분 쉼) → **550 °C 10 h Ar** · BH₄ 2 종 = 2 단계 볼밀 (SI ref 1 = Han 2023 Mater. Horiz.) | [인쇄] SI p.2 |
| 상 | 합성 Li₆PS₅Cl XRD ↔ ICSD 131109 (Fig S2a) · Li₆PS₅Br Rietveld **a = 9.97227(10) Å · Rwp 8.81** · 상 정량 Li₆PS₅Br : LiBr : Li₂S = **97.3 : 0.85 : 1.9 %** · 4d/4a Br/S 자리 섞임 0.356 / 0.668 (Table S1) | [인쇄] SI p.6 · p.10 |
| 단면 · 공극 | 이온밀링 (ArBlade 5000, 6 kV · 40° · 1 h) → SEM (Regulus 8230, 5 kV) · 공극 = 영상 이진화 (가장자리 밝은 띠가 있는 검은 점만 공극 — 없는 것은 물질, SI Fig S3) | [인쇄] SI p.3 · p.8 |
| 나노압입 | Hysitron PI-85 (SEM 안, Ar 글러브박스 연결) · **최대 8 mN · 4 s 하중 · 2 s 유지 · 4 s 제하** · Oliver–Pharr · 위치 5 곳 평균 ± 표준편차 | [인쇄] SI p.4 |
| 입경 | **[미확인]** (상용 · 합성 · 볼밀 모두 수치 없음) | 본문 · SI 전수 |

### 3-2. ★ Heckel — Table 1 (p.6344) · 본문 (p.6343)
| 시료 | K (×10⁻⁴ MPa⁻¹) | 97 % TD 압력 (MPa) | P_y = 1/K [우리 산술] | σ_y,eff = P_y/3 [우리 산술 — frame[3] 의 우리 규약] |
|---|---|---|---|---|
| 상용 Li₆PS₅Cl (그대로) | **32.3** | **650** | 310 MPa | 103 MPa |
| 상용 Li₆PS₅Cl (볼밀) | **34.0 (±0.15)** | **570** | 294 MPa | 98 MPa |
| 합성 Li₆PS₅Cl | **29.1 (±0.14)** | **675** | 344 MPa | 115 MPa |
| 합성 Li₆PS₅Br | **25.0 (±0.16)** | **725** | 400 MPa | 133 MPa |
| Li₅.₁₅PS₄.₁₅(BH₄)₁.₈₅ | **37.0 (±0.11)** | **570** | 270 MPa | 90 MPa |
| Li₅.₅₅PS₄.₅₅(BH₄)₁.₄₅ | **41.3 (±0.11)** | **510** | 242 MPa | 81 MPa |

- 97 % 를 고른 이유: *"Because the y-axis of the Heckel plot uses the natural logarithm, the variation in compressive strength increases significantly as the density approaches 100% TD. Therefore, 97% was arbitrarily selected"* (Table 1 캡션) [인쇄].
- 단계 경계 (Fig 2a 판독): stage I/II ≈95–105 MPa · II/III ≈400 MPa (볼밀) · ≈435 MPa (그대로) · 그림 안 글자: **stage I = 상대밀도 ≤70 % · II = 70–90 % · III = ≥90 %** [인쇄 — 그림 안].  Fig 1d (같은 상용 분말) 의 점선 = ≈75 · ≈450 MPa [판독].
- [판독 검산] 판독 곡선의 100 → 400 MPa 기울기: 합성 Li₆PS₅Cl 28.8 (인쇄 29.1) · BH₄ 1.45 42.4 (41.3) · BH₄ 1.85 38.2 (37.0) · Li₆PS₅Br 23.3 (25.0) · 상용 (Fig 1d, 150 → 400) 34.4 (32.3) ×10⁻⁴ MPa⁻¹ — 판독 보정 확인 (±7 %).
- 저자 해석: *"The reciprocal of the K value physically represents a quantity proportional to the yield strength of the powder."* (p.6343) · 볼밀: *"The milled powder approaches the theoretical density at significantly lower stress … while the K is approximately the same"* → K 는 고유 물성 (탄성률 · 소성), 전이 압력은 형상 · 크기 (p.6344).

### 3-3. ★ 가압 중 공극 — Heckel 곡선 판독 (TD 기준 그대로) [판독]
상용 Li₆PS₅Cl — Fig 1d (단일 계열 · 가장 깨끗함): ε = exp(−y)

| σ (MPa) | 10 | 50 | 100 | 150 | 200 | 250 | **300** | 350 | 400 | 500 | 600 | 650 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| −ln(1 − ρ_rel) | 0.75 | 1.06 | 1.24 | 1.41 | 1.58 | 1.74 | **1.90** | 2.07 | 2.27 | 2.75 | 3.42 | 4.12 |
| ε (%) | 47 | 35 | 29 | 24 | 21 | 18 | **14.9** | 12.6 | 10.3 | 6.4 | 3.3 | 1.6 |

- Fig 2a 같은 분말 (두 계열 겹침 — 그대로 = 볼밀 표지 밑에 가려 아래쪽으로 치우침): 300 MPa **그대로 1.83 (16.1 %) · 볼밀 1.91 (14.8 %)** · 650 MPa 그대로 3.52 (3.0 % = 인쇄 "97 % TD @650" 와 맞음).
- Fig 2b (300 MPa): 합성 Li₆PS₅Cl 1.74 (17.7 %, 녹색에 가려 점 2 개) · Li₆PS₅Br 1.67 (18.8 %) · BH₄ 1.45 2.25 (10.5 %) · BH₄ 1.85 2.12 (12.0 %).
- 초기 (σ → 0) −ln(1−ρ) ≈0.6–0.75 → 충전 상대밀도 ≈0.45–0.53 [판독].

### 3-4. ⚠ 이론밀도 (TD) 의 정체 — 공극 절대값을 흔드는 한 줄
- [인쇄] SI p.3: *"The theoretical densities of Li6PS5Cl and Li6PS5Br were calculated to be 1.64 g/cm3 and 1.90 g/cm3, respectively."* — 계산 방법은 안 적었다.
- [우리 산술] 결정학 밀도 = Z·M/(N_A·a³) (Z = 4): Li₆PS₅Cl (M 268.37 g/mol · a 9.8598 Å = 정본 `adeli2019_…` 카드 값) **1.860 g/cm³** · Li₆PS₅Br (M 312.82 · 이 논문 Table S1 의 a 9.97227 Å) **2.095 g/cm³**.  인쇄 TD 는 각각 **12 % · 9 % 낮다**.
- 글자 그대로라면: ρ_rel = 5 mm / h (질량을 TD 로 정했으므로 TD 가 약분된다) — "ρ_rel → 1" 은 펠릿 밀도 1.64 g/cm³ = **결정 기준 공극 ≈12 %** 를 뜻하고, 300 MPa 의 "14.9 %" 는 결정 기준 **≈25 %** 가 된다.  그런데 같은 논문의 **치밀 펠릿 단면 공극은 2.5 %** (Table 2 · Fig 3 · S3) — 글자 그대로의 TD 와 양립하지 않는다.
- ⇒ **둘 중 하나**: (a) 인쇄 TD 가 오기이고 실제 계산은 결정밀도 근처로 했다 → 300 MPa 가압 중 ≈15 % 가 이 논문의 값 / (b) 1.64 를 그대로 썼다 → 모든 공극을 결정 기준으로 다시 계산해야 한다 (≈+10 %p).  원문만으로 가를 수 없다 [미확인] — **CL-94 후보로 쓰기 전 저자 확인 필요**.
- 별개의 계통 편향 [우리 산술]: 하중 아래 고체 자체가 탄성 압축되는데 (체적변형 ≈ p/K, K = B₀ 26.23 GPa = 우리 DFT) 이 논문은 펀치 탄성만 뺐다 → in-die 공극은 **300 MPa 에서 ≈1.2 %p · 600 MPa ≈2.3 %p · 900 MPa ≈3.5 %p 작게** 읽힌다 (miss2026 AMI 카드 §4-4 와 같은 논점 — 그 논문은 보정했다).  stage III 의 가파른 상승 · ρ_rel → 1 흩어짐의 일부가 이 산물일 수 있다 (추정).

### 3-5. ★ 하중 제거 회복 — Fig 1c (p.6343) [판독]
- 순서 (본문): (1) 최대 하중 → (2) 하중 제거 → (3) 총 변위 급락.  *"It can be regarded that the difference between (2) and (3) is the elastic recovery because there is no appearance of irreversible deformation such as cracks on the surface of the pellet."* — 회복은 **펀치 탄성 (Δd_elastic, 검정 화살표)** 과 **펠릿 탄성 (ΔE_SE-powder, 파랑 화살표)** 둘로 나뉜다 [인쇄] p.6343.
- 기준선 판독 (눈금 0.2 mm = 37 px, ±0.005 mm): (1) 6.711 · 중간선 6.511 · (3) 6.278 mm → **Δd_elastic = 0.200 mm · ΔE_SE-powder = 0.233 mm** · 합 0.433 mm.
- [우리 산술] 펀치 몫 0.200 mm = σL/E → σ_max ≈ 0.200 × 180 000 / 40 = **900 MPa** (Fig 1a 끝 ≈890 MPa 와 맞음).  펠릿 높이 (최대 하중) ≈5.0 mm (ρ_rel ≈1 · 설계 높이 5 mm) → **회복 ≈4.7 %** (0.233/5.0).
- 시간: 최대 하중 ≈440 s · 제거 ≈448 s · 무하중 ≈452 s — 회복은 **수 초 안** (3 fps DIC 시간 분해능 안) [판독].
- 비교 [우리 산술]: 치밀 고체의 탄성 변형 p/E = 900 / 27 600 (이 논문 나노 E) = 3.3 % · /22 060 (우리 DFT E_VRH) = 4.1 % → 측정 4.7 % 는 **치밀 고체 탄성 크기의 1.1–1.4 배**.  일축 구속 (측방 변형 0) 이면 축 방향 계수는 M = E(1−ν)/((1+ν)(1−2ν)) ≈1.77E (ν 0.37) 라 순수 고체 탄성만으로는 ≈2.3 % — 나머지 몫 = 접촉 · 남은 공극의 순응 (추정).
- 압력당 회복 [우리 산술 — 두 논문 · 다른 조성 · 다른 프로토콜]: 이 논문 4.7 % / 900 MPa = **0.52 %/100 MPa** · miss2026 AMI (Li₅.₅PS₄.₅Cl₁.₅ 다이 안, 110 kPa 까지) 1.6 % / 300 = 0.53 · 2.8 % / 400 = 0.69 %/100 MPa.

### 3-6. 나노압입 — Table 2 (p.6344) · Fig 3 · S1
| | Li₆PS₅Br | Li₆PS₅Cl | Li₅.₁₅PS₄.₁₅(BH₄)₁.₈₅ | Li₅.₅₅PS₄.₅₅(BH₄)₁.₄₅ |
|---|---|---|---|---|
| H (GPa) | **1.68 (±0.11)** | **1.41 (±0.24)** | 0.69 (±0.07) | 0.66 (±0.05) |
| E (GPa) | **30.5** | **27.6** | 15.6 | 19.1 |
| 단면 공극 (%) | 2.5 (그림 2.49) | 2.5 (2.48) | 7.3 (7.31) | 4.7 (4.68) |
| H/E (×10⁻²) | 5.5 | 5.1 | 4.4 | 3.5 |
- 본문: *"Li6PS5Cl typically exhibits a value of approximately 5.0 × 10−2, which aligns well with our result of 5.1 × 10−2"* · *"It is clear that the H/E is proportional to the inverse of the slope K"* · *"the porosity measured by an image analysis method is not higher than 7%"* [인쇄] p.6344–6345.
- 펠릿 = *"compressed close to the theoretical density, as determined from the Heckel plots"* — 압밀 압력 [미확인].  압입 깊이 (8 mN): Li₆PS₅Cl ≈1.3–1.55 µm · Li₆PS₅Br ≈1.1–1.3 µm · BH₄ ≈1.65–2.05 µm [판독 Fig 3e-f · S1].
- [우리 산술] H/E 와 1/K 의 순위: H/E 5.5 > 5.1 > 4.4 > 3.5 ↔ K 25.0 < 29.1 < 37.0 < 41.3 — **순위 4/4 일치** (n = 4 · 정량 비례 검정 없음).  ⚠ "BH₄ 1.85 의 E 15.6 < BH₄ 1.45 의 19.1" 인데 K 는 1.45 쪽이 더 크다 (H 는 비슷) — 원문이 짚지 않은 부분.
- 비교: 우리 DFT E_VRH **22.06 GPa** (comp1) · Deng 2016 PBEsol 22.1 (정본 `deng2016_…`) · Ning 2023 나노압입 28.0 ± 1.8 (`song2025_porous_…` 카드 경유) · 다공 13 % 펠릿 벌크 굽힘 4.7 ± 1.1 GPa (`song2025_porous_…`).  이 논문 27.6 = **나노압입 층**과 같은 값.
- [우리 산술 · 참고만] Tabor 근사 σ_y ≈ H/3 (금속 관계 — 황화물에 검증 안 됨): Li₆PS₅Cl ≈0.47 GPa · Li₆PS₅Br ≈0.56 GPa — Heckel σ_y,eff (≈0.10–0.13 GPa) 와 **4–5 배 다르다** (같은 양이 아니다: 국부 압입 항복 vs 분말 체적 치밀화).

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리

### 4-1. 측정 사슬
분말 질량 (TD × 면적 × 5 mm) → ⌀8 mm ZrO₂ 다이 → 1 mm/min 연속 가압 (최대 ≈880–900 MPa) → DIC 총 변위 Δd → Eq 1 로 펀치 탄성 σL/E 뺌 → 펠릿 높이 h(σ) → ρ_rel = 질량/(A·h)/TD → −ln(1−ρ_rel) vs σ → stage II 직선 기울기 K · 97 % TD 압력 → (따로) 치밀 펠릿 이온밀링 단면 → SEM 공극 · 나노압입 H · E.
- 안 한 것: 고체의 탄성 압축 보정 · 하중 제거 뒤 (out-of-die) 밀도 · 다른 하중 속도 · 반복 통계 · 수송 (σ) · 입경 분포.

### 4-2. ★ 입자 처리
- 실험 — 실제 분말 (상용 · 볼밀 · 합성).  단계 I = 재배열 · 파쇄, II = 소성 변형 (Heckel 선형), III = 치밀체 탄성 (Heckel 1961 · 제약 분말 문헌 refs 32–37 의 고전 해석).
- 저자의 기전 문장 (p.6343): *"As the voids become smaller than the average particle size, however, particles have to change their shape or even break into smaller ones through plastic deformation or fragmentation"* — **진짜 형상 소성 (MPM 쪽 물리)** + 파쇄 (DEM Auerbach 쪽).
- 우리 대응: DEM = 강체 구 + hooke/hysteresis 접촉 (형상 불변) · MPM = J2 연속체 (형상 소성) — Heckel 의 단계 II (형상 소성 지배) 를 담는 쪽은 MPM, 재배열 (단계 I) 은 DEM.

### 4-3. 기법 미니 용어집
- **in-die Heckel**: 하중 아래 다이 안 높이로 잰 상대밀도 (탄성 포함) ↔ **out-of-die**: 꺼낸 펠릿 (탄성 회복 뒤).
- **K · P_y**: Heckel 기울기 · 그 역수 (평균 항복 압력) — 우리 frame[3] 규약은 σ_y,eff = P_y/3.
- **DIC** (digital image correlation): 반점 무늬를 영상으로 추적해 변위를 재는 비접촉 방법.
- **H/E (소성 지수)**: 압입 경도/탄성률 — 클수록 탄성 쪽 (소성 덜 함).
- **Oliver–Pharr**: 압입 제하 곡선 기울기로 접촉 강성 → E · H 를 내는 표준 해석 (E 가 환산 계수인지 영률인지 원문 미기재 [미확인]).

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a | 상용 Li₆PS₅Cl 총 변위 vs 압축 응력 (0 → ≈890 MPa) + 삽입: DIC 몰드 장치 사진 | 장치 · 전 범위 곡선 |
| 1b | Δd 와 Δh_SE-powder (= Δd − σL/E) vs 시간 — 두 곡선 사이가 펀치 탄성 | ★ 순응도 보정 절차 (펀치 탄성) |
| 1c | 최대 하중 근처 확대: (1) 최대 → (2) 제거 → (3) 무하중 · Δd_elastic (펀치) 과 ΔE_SE-powder (펠릿) 화살표 | ★★ 순수 Li₆PS₅Cl 다이 안 탄성 회복 0.233 mm [판독] — 언로딩 시험 규모 |
| 1d | 상용 Li₆PS₅Cl Heckel 곡선 + 단계 I · II · III (점선 ≈75 · ≈450 MPa) | ★ 가압 중 공극 vs 압력 연속 곡선 (CL-94 후보 — TD 확인 뒤) |
| 2a | 상용 그대로 vs 볼밀 Heckel — 단계 표지 (상대밀도 ≤70 · 70–90 · ≥90 %) | 입경 (볼밀) 이 전이를 당긴다 · K 는 거의 같다 |
| 2b | 합성 Li₆PS₅Cl · Li₆PS₅Br · BH₄ 2 종 Heckel | 조성 (할로겐 · BH₄) 순위 |
| 3 | (a–d) 이온밀링 단면 SEM 공극 (빨강) 2.49 · 2.48 · 4.68 · 7.31 % (3 µm 막대) · (e, f) 압입 곡선 (Li₆PS₅Br · BH₄ 1.45) | 치밀 펠릿 공극 · 압입 깊이 |
| Table 1 | K · 97 % TD 압력 (4 시료) | ★ Heckel 외부 값 |
| Table 2 | H · E · 공극 · H/E (4 시료) | ★ 나노압입 E · H |
| S1 | 압입 곡선 — 합성 Li₆PS₅Cl · BH₄ 1.85 (5 회씩) | 산포 (Li₆PS₅Cl 한 곡선이 따로 놂) |
| S2 | (a) 합성 Li₆PS₅Cl XRD vs ICSD 131109 (b) Li₆PS₅Br Rietveld | 상 확인 |
| S3 | 단면 원영상 + 이진화 공극 (a) Li₆PS₅Cl 2.48 % (b) Li₆PS₅Br 2.49 % (c) BH₄ 1.45 4.68 % (p.7) (d) BH₄ 1.85 7.31 % (p.8) — 가장자리 효과로 공극/물질 판별 | 공극 정의 (영상) |
| S4 | 합성 4 종의 힘 (축 "Stress (kgf)" — 실제는 힘) vs 변위 원자료 (최대 ≈4500 kgf) | V2 원측정의 일부 (상용 시료 원자료 없음) |
| Table S1 | Li₆PS₅Br Rietveld (a 9.97227 Å · 자리 점유 · 상 정량) | 결정밀도 재계산 (§3-4) |

## 6. Post-processing ★
- **무엇을**: 펀치 탄성 제거 (Eq 1) → ρ_rel (SI Eq 1) → Heckel 단계 분할 · stage II 선형 적합 K (± = 적합 오차로 읽힘 [미확인]) · 97 % TD 압력 → 단면 영상 이진화 공극 → 압입 Oliver–Pharr H · E · H/E.
- **도구**: GOM Correlate 2019 (DIC) · Hysitron TriboScan · 이진화 도구 [미확인].
- **우리 후처리 (이 카드)**: 원 래스터 판독 (Fig 1c 기준선 · Fig 1d · 2a · 2b 띠 중앙값) · 판독 기울기로 K 검산 · 결정밀도 재계산 · 회복 % · P_y = 1/K.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · `docs/` 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 시료 | 순수 SE 분말 (Li₆PS₅Cl 상용 · 합성 · Br · BH₄) | ps45 복합체 (NCM PC/SC + Li₆PS₅Cl 81.6 : 18.4 wt) · 순수 SE DEM (E_SE 보정용) | 순수 SE 끼리만 대조 가능 |
| 측정 상태 | **가압 중** (연속 1 mm/min) + 한 번의 **완전 제거** | DEM = 300 MPa 판 정지 + 판 고정 이완 · 언로딩 시험 = P_meas 1 MPa (`docs/reviews/dem_unloading_ps45_prereg_20261009.md`) · 판 속도 0.01 mm/s | 속도 값은 같은 자릿수 (1 ↔ 0.6 mm/min) 지만 시료 높이가 다르다 (분말 ≈11.5 → 5 mm [우리 산술: 설계 5 mm + Fig 1c 펠릿 변위 ≈6.5 mm] ↔ 전극 ≈0.11–0.15 mm) → 변형률 속도는 수십 배 다름 — 비교하지 않는다 |
| Heckel P_y | Li₆PS₅Cl **294–344 MPa** (stage II) | DEM 순수 SE **138 MPa** (E 1.35 · 4 압력 · R² 0.965 — CLAUDE.md frame[3]) | DEM 이 2.1–2.5 배 무르다 — E 연화 (24 → 1.35) 가 정적 치밀화를 맞추려 넣은 대리이므로 Heckel 기울기까지 맞을 이유 없음 (frame[2]) |
| 300 MPa 공극 (순수 SE) | 가압 중 ≈15 % (TD 기준 · §3-4 확인 전) | MPM 보정 표적 ≈10 % — **출처 철회 (원장 `CL-94`, 외부 앵커 없음)** | §7-3 |
| 회복 (순수 SE) | ≈900 MPa → 0: 펠릿 ≈4.7 % [판독 + 우리 산술] | DEM · MPM 제하 팔 = 등록 단계 (복합체) | §7-2 |
| E | 나노 27.6 GPa (Li₆PS₅Cl) | DFT 22.06 (물성) · DEM 1.35 · MPM 1.53 (연화 대리) | 물성 층은 이 논문과 같은 자릿수 · 연화값은 다른 층 (frame[2]) |

### 7-2. ★ 언로딩 시험 (ρ_c) — 규모 감각
- 이 논문 회복 ≈4.7 % 는 **순수 Li₆PS₅Cl · ≈900 MPa → 0 · 다이 안 · 측방 구속** — 우리 시험 (복합체 · 이완 상태 σ_zz 158–175 MPa → 1 MPa · 주기 측방 경계) 과 **다른 조건**이라 표적이 아니다.
- 쓸 수 있는 것 = 크기 감각: 순수 치밀 LPSCl 의 다이 안 회복은 **≈0.5–0.7 % / 100 MPa** (두 논문 · 다른 조성 [우리 산술 §3-5]).  우리 DEM 의 SE 는 E 1.35 GPa 로 연화돼 있어 탄성 회복이 그보다 **훨씬 클 수 있다** (p/E: 170 MPa / 1.35 GPa ≈ 13 % — 접촉 겹침 회복 규칙은 hysteresis 분기가 정하므로 이 비는 상한 감각일 뿐 [우리 산술]).  ⇒ 등록 §7-4 의 한정어 *"연화 SE (E 1.35 GPa) 모델 안 값 — 실제 회복보다 클 수 있다"* 의 **외부 크기 근거 하나**.
- 복합체 회복은 AM 골격이 지배할 수 있다 (miss2026 AMI: pc-NMC622 단일상 7.9 % @300 MPa) — 이 논문 (SE 만) 은 그 몫을 주지 않는다.
- 회복이 **수 초 안**에 끝났다 [판독] — 우리 DEM 의 정상상태 판정 (수치 감쇠) 을 실제 시간으로 읽지 않는다는 Codex 경고 (`docs/reviews/codex_review_springback_loadshare_20261009.md` Q4) 와 별개로, 실험 쪽 순수 SE 회복은 빠른 탄성으로 보인다는 정성 근거.

### 7-3. ★ CL-94 · V2 — 무엇이 서고 무엇이 안 서나
- **선다**: 원문 확인된 **순수 Li₆PS₅Cl (상용) 가압 중 공극–압력 연속 곡선** — 원장 CL-94 의 hold 사유 *"원문 확인된 순수 LPSCl 기공 @ 300 MPa 실측이 생기기 전까지"* 에 대한 첫 후보 (상태 = in-die · 하중 아래).
- **안 선다 (아직)**: ① TD 1.64 의 정체 (§3-4) — 글자 그대로면 ≈+10 %p ② 고체 탄성 압축 미보정 (−1.2 %p @300) ③ 반복 · 시료 간 불확도 없음 ④ 펠릿 5 mm × ⌀8 mm 벽 마찰 (밀도 구배) ⑤ 상용 원측정 (힘–변위) 미공개 (S4 는 합성 시료).  ⇒ Codex V2 판정 (`docs/reviews/codex_review_model_validation_20261008.md` Q3–Q4) 의 요구 — 상태 · 측정량 · 원측정 · 불확실성 · 같은 측정 연산자 — 중 **상태 · 측정량만 충족**.
- 후보 값 정리 (CL-94 원장은 고치지 않는다 · 결정 = 1저자):

| 상태 | 값 (300 MPa) | 표지 |
|---|---|---|
| 상용 Li₆PS₅Cl · 가압 중 · 이 논문 TD 기준 | **14.9 %** (Fig 1d) · 14.8–16.1 % (Fig 2a) | [판독] |
| 같은 · 고체 탄성 압축 보정 (+p/K) | ≈16 % | [우리 산술] |
| 같은 · TD 를 결정밀도 1.86 으로 (글자 그대로 1.64 를 썼다면) | ≈25 % | [우리 산술 — 같은 논문 단면 2.5 % 와 모순 · 가능성 낮음] |
| (참고) miss2026 AMI Li₅.₅PS₄.₅Cl₁.₅ 가압 중 | 7.1–7.6 % | 그 카드 §7-3 |
- 두 논문 차 (≈15 vs ≈7.5 %) 후보 원인 [추정]: 재료 (상용 Li₆PS₅Cl ↔ 550 °C 어닐 Cl-rich) · 프로토콜 (연속 ↔ 단계 + 매 단계 제거) · 기하 (5 mm 높이 ⌀8 ↔ ≈0.6 mm ⌀10 — 벽 마찰 비) · 밀도 기준 · 탄성 보정 — **미분리**.

### 7-4. Heckel ↔ frame[3]
- frame[3] 의 빈칸 *"Experimental multi-pressure Heckel for LPSCl powder is the missing direct validation"* 의 **두 번째 외부 후보** (첫째 = miss2026 AMI 카드 우리 적합 P_y ≈219–243 MPa, Li₅.₅PS₄.₅Cl₁.₅): 이 논문 Li₆PS₅Cl **P_y 294–344 MPa** (저자 적합 stage II · 인쇄 K).
- ⇒ 실험 LPSCl 계열 P_y ≈220–345 MPa ↔ DEM 순수 SE 138 MPa = **DEM 이 1.6–2.5 배 무르다**.  ⚠ 비교 전 규약: ① 적합 구간 (우리 4 압력 vs stage II) ② in-die vs 우리 판 정지 상태 ③ DEM 순수 SE 의 ε_sphere 는 음수 근처로 퇴화하는 영역 (CLAUDE.md 2026-06-06) ④ TD 기준.
- frame[4] 원칙: 이 값으로 DEM E 를 다시 맞추지 않는다 — Heckel 기울기 차이는 **E 연화 대리의 정량 한계** (정보) 로 적는다.

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 순수 SE 의 기계 반쪽 (가압 중 치밀화 곡선 · 한 점 탄성 회복 · 압입 H · E).
- **없는 것**: 수송 (σ) · 복합체 · 접촉 · 미세구조 3D · 모델.  ⇒ MPM (형상 소성 치밀화) 과 DEM (재배열 · 탄성 회복) 의 순수 SE 대조점.

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **CL-94 후보 등록 재료** (§7-3) — 단, TD 1.64 의 계산 방법을 저자에게 확인하거나 같은 분말로 재측정하기 전에는 "앵커" 가 아니라 "후보 (기준 미확인)".
2. **in-die 측정 연산자 체크리스트** (우리 실험 · V2 설계용): 펀치 탄성 (σL/E) 뺌 ✓ · 고체 탄성 압축 (p/K) 보정 · TD 의 근거 (결정 / 피크노미터) · 펠릿 높이/지름 비 · 하중 속도 · 반복 수.
3. **언로딩 크기 감각** — 순수 LPSCl 다이 안 회복 ≈0.5–0.7 %/100 MPa (두 논문) — DEM ρ_c 결과 보고 때 "연화 SE 라 클 수 있다" 한정어의 외부 근거.
4. **Heckel P_y 외부 범위** ≈220–345 MPa (LPSCl 계열, 두 논문) — DEM 138 MPa 와의 배수 (1.6–2.5) 를 E 연화 한계의 정량 기록으로.
5. **볼밀 (입경 ↓) 은 K 를 거의 안 바꾸고 III 전이를 당긴다** — 우리 SE 입경 (r 0.5 µm 생산) 축의 Heckel 감도 해석에 참고 (K = 물질, 전이 = 기하).

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In-die compression with DIC-tracked punch displacement (Lee et al., *J. Mater. Chem. A* 2025) gives Heckel stage-II slopes of 29–34 ×10⁻⁴ MPa⁻¹ for Li₆PS₅Cl powders (P_y = 1/K ≈ 0.29–0.34 GPa), about 2–2.5× stiffer than our DEM pure-SE Heckel fit (P_y = 138 MPa)."
- "On full unloading from ≈0.9 GPa inside the die, a ≈5 mm Li₆PS₅Cl compact recovered ≈0.23 mm (≈4.7 %) after subtracting the punch elastic contribution (read from their Fig. 1c)."
- 국문: *"순수 Li₆PS₅Cl 의 가압 중 공극은 300 MPa 에서 ≈15 % 로 읽히지만 (Lee 2025, 그림 판독), 원문 이론밀도 1.64 g/cm³ 가 결정밀도보다 12 % 낮아 절대값은 기준 확인 전이다."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **TD 1.64 / 1.90 g/cm³ ↔ 결정학 1.86 / 2.09** (§3-4) — 공극 절대값의 가장 큰 불확실성.  원문은 계산 방법을 안 적었다.
2. **고체 탄성 압축 미보정** — in-die 공극이 고압에서 체계적으로 작게 읽힌다 (≈p/K).
3. **Table 1 의 Li₆PS₅Cl (29.1 · 675) 은 합성 시료**, 본문 Fig 2a 의 상용 (32.3 · 650) · 볼밀 (34.0 · 570) 과 다른 시료 — 인용 시 시료 구분 필수.
4. **K 의 ± 의 뜻** (적합 표준오차로 보임) · 반복 시료 수 [미확인] · 볼밀 조건 (진동밀) 상세 [미확인].
5. **회복 0.233 mm 는 그림 주석선에서 읽은 한 값** · 높이 5 mm 는 설계값 (실측 펠릿 높이 미보고).
6. **H/E ∝ 1/K** 는 순위 4/4 일치까지 — 비례 검정 없음 · E 와 K 순위가 BH₄ 두 시료에서 엇갈림.
7. Fig 3c · d 패널 제목의 조성 오기 ("PS5.55" · "PS5.15" — SI Fig S3 은 "PS4.55" · "PS4.15") · SI Fig S4 축 "Stress (kgf)" (힘).
8. 펠릿 기하 (높이 5 mm / ⌀8 mm) 의 벽 마찰 → 평균 밀도 · 밀도 구배 [미확인 정량].
9. **전이 한계**: 순수 SE ↔ 복합체 · 1 mm/min 연속 ↔ 우리 판 속도 0.01 mm/s 계단 시험 · 상용 분말 입경 미상.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 6 | A. Sakuda, A. Hayashi and M. Tatsumisago, *Sci. Rep.*, 2013, 3, 2261 | 정본 카드 있음 — 황화물 유리 밀도–압력 |
| 7 | J.-M. Doux, Y. Yang, D. H. S. Tan, … Y. S. Meng, *J. Mater. Chem. A*, 2020, 8, 5049–5055 | ⚠ 정본 `doux2020_stack_pressure_assb` (Adv. Energy Mater.) 와 **다른 논문** — 황화물 압력 효과, 미 digest |
| 9 | L. L. Baranowski, C. M. Heveran, V. L. Ferguson and C. R. Stoldt, *ACS Appl. Mater. Interfaces*, 2016, 8, 29573–29579 | 황화물 나노압입 원전 계열 |
| 16 | M. Cronau, M. Szabo, C. König, T. B. Wassermann and B. Roling, *ACS Energy Lett.*, 2021, 6, 3072–3077 | 정본 카드 있음 |
| 17 | S. Kalnaus, N. J. Dudney, A. S. Westover, E. Herbert and S. Hackney, *Science*, 2023, 381 | 고체전지 역학 총설 |
| 25 | Z. Deng, Z. Wang, I.-H. Chu, J. Luo and S. P. Ong, *J. Electrochem. Soc.*, 2015, 163, A67–A74 | = 정본 `deng2016_elastic_superionic_electrolytes_dft` (같은 논문 — 온라인 2015-11 · 권호 163 (2016)) — Li₆PS₅Cl DFT E 22.1 GPa |
| 31 | C. Schneider, C. P. Schmidt, A. Neumann, … B. V. Lotsch, *Adv. Energy Mater.*, 2023, 13 | 정본 카드 있음 — Heckel in die |
| 32 | A. Hassanpour and M. Ghadiri, *Powder Technol.*, 2004, 141, 251–261 | Heckel 단계 해석 |
| 35 | R. W. Heckel, *Trans. Metall. Soc. AIME*, 1961, 221, 1001–1008 | Heckel 원전 |
| 42 | O. Tutusaus, J. Hempel, S. Thapa, … Y.-T. Cheng, *PRiME*, 2024 | Li₆PS₅Cl H/E ≈5 ×10⁻² 의 출처 중 하나 (학회) |
| SI 1 | J. H. Han, D. K. Kim, Y. J. Lee, Y. S. Lee, K. W. Yi and Y. W. Cho, *Mater Horiz*, 2023, DOI: 10.1039/d3mh01450a | BH₄ 치환 아지로다이트 합성 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 5 쪽 · SI 11 쪽 전부 렌더 이미지로 읽고 `pdftotext` 로 인용문 대조 · DOI `10.1039/d4ta08604j` = 본문 1 쪽 인쇄.
- Table 1 · 2 는 텍스트 층 + 크롭 영상으로 칸마다 대조 (H/E 를 H ÷ E 로 다시 계산해 네 칸 모두 일치).
- 판독: 원 래스터 (Fig 1 836×690 · Fig 2 977×377 px) 에서 눈금 위치 탐지 + 색 띠 중앙값.  판독 기울기 (100 → 400 MPa) 로 인쇄 K 를 ±7 % 안에서 재현 (§3-2).
- 그림 크롭 12 장 = 본문 Fig 1–3 · Table 1–2 · SI Figure S1–S4 (S3 는 두 쪽) · Table S1 · **손 크롭 5 장** (tab_1 · tab_2 = 자동 bbox 가 쪽 전체 · fig_S1 = SI 절 제목 혼입 · fig_S3abc = 두 쪽에 걸친 S3 의 p.7 패널 (a)–(c) 누락 · tab_S1 = 상 정량 줄 누락) — `figures.json` 의 `recrop` · `manual_crop`.
- 정본 litdb 중복 확인: DOI · 저자명 · 제목 낱말 papers/ 전수 grep — 없음.

## 🔗 관련 카드
- 압밀 · 회복 실측: `miss2026_insitu_conductivity_porosity_pressure_compaction` · `schneider2023_particle_size_pressure_transport` · `sakuda2013_sulfide_mechanical_property` · `doux2020_stack_pressure_assb`.
- SE 탄성 · 파괴: `deng2016_elastic_superionic_electrolytes_dft` · `song2025_porous_argyrodite_modulus_fracture_toughness` · `torii2025_lpscl_mechanical_anisotropy_dft` · `pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament` · `fan2026_sulfide_assb_stability_review_ECERD2600097`.
- 결정밀도 출처: `adeli2019_halide_substitution_boosting_argyrodite`.
- 압밀 이론: `arzt1982_particle_coordination_densification_spheres` · `bouvard2000_hard_soft_powder_densification` · `zunker2025_dem_large_deformation_compaction`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
