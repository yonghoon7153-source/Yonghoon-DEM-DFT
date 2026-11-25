<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = kaiser2018_ion_transport_limitations_assb_sulfide_electrodes.md · cronau2021_stack_pressure_ionic_conductivity.md (같은 Roling 그룹).
     쪽 표기 = 학술지 인쇄 쪽 (본문 PDF n 쪽 = 인쇄 32829+n · p.32830–32836).  SI 는 "SI p.n" (SI PDF 쪽 = SI 인쇄 번호 1–7).
     값 표지: [인쇄] = 본문 · SI · 그림 범례에 숫자로 적힌 값 · [재계산] = 인쇄값 (표 S1 · S2) 으로 우리가 다시 계산한 값 ·
     [판독] = 그림에서 읽은 값 (재현 = tools/litdb/miss2026_digitize.py → litdb/figures/<slug>/digitized.csv) ·
     [우리 산술] = 이 논문 밖 우리 값 · 다른 카드 값과 엮은 계산 · [미확인] = 원문 (본문 + SI 전수) 에 없음.
     원문 14 쪽 (본문 7 + SI 7) 은 전부 렌더 이미지로 읽었다.  텍스트 추출은 그리스 문자 · 식 기호가 깨지므로 식은 렌더로 대조했다. -->
# 가압 중 (in situ) 두께로 잰 Conductivity–Porosity–Pressure 관계 — µc-Li₅.₅PS₄.₅Cl₁.₅ SE · pc-NMC622 CAM 단일상 powder 펠릿: 가압↔제거 두께 표 (SE 회복 0.3–2.8 % · CAM 0.7–8.6 %) · 두 공극 영역 (ε > 0.2 접촉 지배 ↔ ε < 0.17 공극 지배, MWBH) — Miß · Lange · Staubitz · Roling (ACS Appl. Mater. Interfaces 2026)

> slug `miss2026_insitu_conductivity_porosity_pressure_compaction` · DOI `10.1021/acsami.6c03789` · type `experiment (in situ 가압 셀 — 마이크로미터 두께 + impedance (EIS) · 단일상 powder 펠릿 SE · CAM · 시뮬레이션 없음)` · PDF `1. Experimental Setup for In Situ Determination of Conductivity-Porosity-Pressure Relationships.pdf` · SI `1. Sup) Experimental Setup for In Situ Determination of Conductivity-Porosity-Pressure Relationships.pdf` · digested `2026-10-09` · status ✅
>
> **저자**: Vanessa Miß · Fabio Lange · Stefan Staubitz · **Bernhard Roling\*** (Department of Chemistry and Marburg Center for Quantum Materials and Sustainable Technologies (mar.quest), University of Marburg) · *ACS Appl. Mater. Interfaces* **2026**, 18, 32830–32836 (Research Article, 본문 7 쪽 + SI 7 쪽) · 접수 2026-02-26 · 수정 05-15 · 승인 05-21 · 출판 **2026-06-05** · **CC-BY 4.0** · 연구비 DFG RO 1213/20-1 · RO 1213/14-2.
> **같은 그룹 카드 (링크만 — 내용 베끼지 않음)**: [`cronau2021_stack_pressure_ionic_conductivity`](cronau2021_stack_pressure_ionic_conductivity.md) (본문 ref 17) · [`cronau2022_wet_milling_particle_size_ionic_conductivity`](cronau2022_wet_milling_particle_size_ionic_conductivity.md) (같은 조성 Li₅.₅PS₄.₅Cl₁.₅) · [`ohno2020_interlab_ionic_conductivity_argyrodite`](ohno2020_interlab_ionic_conductivity_argyrodite.md) (ref 18) · [`hlushkou2018_void_space_ion_transport_assb_cathode`](hlushkou2018_void_space_ion_transport_assb_cathode.md) · [`kaiser2018_ion_transport_limitations_assb_sulfide_electrodes`](kaiser2018_ion_transport_limitations_assb_sulfide_electrodes.md) · [`minnmann2021_jes_charge_transport_bottlenecks`](minnmann2021_jes_charge_transport_bottlenecks.md).  SI ref 1 (ρ₀ 출처) = [`adeli2019_halide_substitution_boosting_argyrodite`](adeli2019_halide_substitution_boosting_argyrodite.md).
> **판독 원자료**: `litdb/figures/miss2026_insitu_conductivity_porosity_pressure_compaction/digitized.csv` (94 행) · 재현 `python3 tools/litdb/miss2026_digitize.py --pdf <본문> --si <SI> --check` (표 S2 재계산만은 `--check-only`, PDF 불요).

---

## 0. 결론 먼저 — 우리 질문 (ps45 실험 ↔ DEM 공극 차이의 가설 (a) = 하중 제거 뒤 스프링백) 에 대한 답

**한 문장**: 이 논문은 황화물 SE 와 다결정 NMC 를 **각각 단일상**으로 다이 안에서 눌렀다 놓으며 두께를 잰 표 (Table S2) 를 준다.
300 MPa 에서 놓았을 때 다이 안 두께 회복은 **SE 1.6 % · pc-NMC622 7.9 %** [재계산] 이고, 우리 차이를 스프링백만으로 메우려면 필요한
**7.4–13.0 %** (1저자 산술) 와 견주면 — **스프링백은 차이의 일부 (≈1–6 %p) 를 설명할 크기이지만, 10:0 · 0:10 의 9.2–9.3 %p 를
다 덮지 못한다** (CAM 같은 위쪽 끝에서도 ≥3.5 %p 남는다).  복합 전극 자료는 **없다** (*"The application of this method to composite
cathodes will be the subject of future work."* p.32835).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 장치 순응도 (다이 · 펀치 탄성) 보정 | **피스톤 압축만 보정**: 시료 없이 피스톤 길이 d_pistons(p) 를 압력별로 재고 d_sample(p) = d(p) − d_pistons(p) (Eq. 1, Fig. 2b).  교정값 자체는 안 실림.  **다이 (PEEK 하우징) 의 반경 방향 순응 · 벽 마찰은 언급 없음** | [인쇄] p.32832 · 교정값 [미확인] |
| ② 공극 계산식 | ε = 1 − m / (π r² (d_sample(p) + Δd_elastic(p)) ρ₀) (Eq. 2) · Δd_elastic = −d_0.11 MPa · p/E (Eq. 3–4) · ρ₀ = 결정밀도 1.87 (SE, Adeli 2019) · 4.48 g/cm³ (NMC622, Hua 2020) · E 67 GPa (Munsif 2023 DFT 인용) · 180 GPa (Liu 2024 인용) · m 80.2 · 80.0 mg | [인쇄] p.32833 · Table S1 |
| ⚠ 그 식의 두 인쇄 결함 | (i) Table S1 의 "Diameter 0.5 cm" 를 지름으로 넣으면 ε = −1.8 (불가능) — **반지름 0.5 cm (지름 10 mm) 라야** 본문 "≈0.30 @10 MPa" 가 나온다.  (ii) **Fig. 4a 의 가압 중 공극은 인쇄된 Eq. 2 와 반대 부호 (d + \|Δd\|) 로 계산됐다** — 판독 − 재계산 평균 +0.0008 (반대 부호) vs +0.0079 (인쇄 부호), p ≥ 100 MPa 7 점 | [재계산] + [판독] §4-4 |
| ③ 300 MPa 에서 놓았을 때 다이 안 두께 회복 | **SE (µc-Li₅.₅PS₄.₅Cl₁.₅) 1.62 %** (0.5880 → 0.5975 mm) · **pc-NMC622 7.90 %** (0.2769 → 0.2988 mm) · 전 압력 범위 SE −0.3…+2.8 % · NMC +0.7…+8.6 % | [재계산] Table S2 인쇄 두께 · 본문 "0.3−2.8 %" [인쇄] p.32832 |
| ④ 다이 밖 (밀어낸 펠릿, 400 MPa 뒤) | SE **+6.5 %** (가압 중 400 대비) · NMC **+1.7 %** — ⚠ NMC 는 다이 안 제거 값보다 **5 % 얇다** (모순, 저자 무언급) | [판독] Fig. 3a · S4a (인쇄 두께로 보정, 잔차 ≤0.5 µm) |
| ⑤ 순수 SE 300 MPa 공극 (CL-94 후보) | 가압 중 **7.1–7.6 %** · 놓은 뒤 (다이 안) **8.6 %** · 400 MPa 뒤 다이 밖 9.5 % — **본문은 10 MPa "≈0.30" · 400 MPa "≈0.04" 만 인쇄** | [재계산] · Fig. 4a [판독] 0.076 / 0.087 |
| ⑥ 두 공극 영역 | ε > 0.2 = 계면 접촉 지배 (σ 가 MWBH 보다 최대 ≈4 배 낮음) · ε < 0.17 = 공극 지배 (MWBH σ₀(1−ε)^1.5 를 따름) · σ₀ 적합 **4.1** (SE) · **18.2 mS/cm** (NMC) | [인쇄] p.32834–32835 · 범례 · 배수 [판독] |

**가설 (a) 산술** (1저자 숫자 · 이 논문 단일상 회복을 그대로 씌운 상·하한 — 복합체 값이 두 상 사이에 있다는 것 자체가 **가정**):

| P:S | 실험 ε | DEM ε | 차이 | 필요 회복 (두께) | SE 같은 1.6 % 이면 | pc-CAM 같은 7.9 % 이면 | SE 진밀도 2.0 → 1.87 이면 |
|---|---|---|---|---|---|---|---|
| 10:0 | 26.2 % | 16.9 % | +9.3 %p | 12.6 % (≈15 µm) | −1.2 %p → 8.1 남음 | −5.8 %p → **3.5 남음** | −1.8 %p |
| 7:3 | 22.2 | 16.5 | +5.7 | 7.4 % (≈9 µm) | −1.3 → 4.4 | −6.2 → **0 (다 설명)** | −1.9 |
| 5:5 | 24.5 | 17.7 | +6.8 | 9.1 % (≈11 µm) | −1.2 → 5.6 | −6.0 → 0.8 | −1.8 |
| 3:7 | 25.6 | 18.7 | +6.9 | 9.3 % (≈12 µm) | −1.2 → 5.7 | −5.9 → 1.0 | −1.8 |
| 0:10 | 29.8 | 20.6 | +9.2 | 13.0 % (≈17 µm) | −1.1 → 8.1 | −5.6 → **3.7 남음** | −1.7 |

[우리 산술] Δε = (1 − ε_exp) × 회복률 (같은 고체 부피) · 두께 µm = t_exp − t_exp(1−ε_exp)/(1−ε_DEM) · 진밀도 열 = −φ_SE (2.0/1.87 − 1), φ_SE 는 DEM 침대 질량비 81.6 : 18.4 (`docs/data/ps45_r45_union_20260929/README.md`) 를 실험에도 가정 · 1저자의 "필요 회복" 은 우리 재계산과 ±0.1 %p 안에서 같다 (반올림).

⛔ **한정어 (떼지 말 것)**: ① 재료가 다르다 — 이 논문 SE = Cl-rich **Li₅.₅PS₄.₅Cl₁.₅** (550 °C 어닐한 µc) ↔ 우리 Li₆PS₅Cl · CAM = **다결정 NMC622** (MSE Supplies) 단독 ↔ 우리 NCM 은 PC (r 4.5 µm) + **SC** (r 2.0 µm) — **SC 자료는 없다** ② **단일상 ↔ 복합체** — 복합체 회복이 두 상 사이에 온다는 근거 없음 ③ 이 논문은 10 → 400 MPa 를 **단계마다 놓았다 다시 누른다** (Fig. S3, 300 MPa 에 닿기 전 SE 10 회 · NMC 5 회) ↔ 우리 단조 가압 ④ NMC 의 다이 안 회복 7.9 % 는 다이 밖 (+1.7 %) 과 모순 — **위쪽 끝 자체가 부풀었을 수 있다** (§10-②) ⑤ SE 회복 9.5 µm 은 저자가 밝힌 불확도 ("기호 크기 이하" ≈ 5–6 µm, [우리 산술]) 의 2 배 남짓 ⑥ 진밀도 열과 회복 열을 **같이 쓰면 미측정 손잡이 둘로 차이를 메울 수도 넘길 수도 있다** — Codex 10-01 판정 (`docs/reviews/codex_ps45_porosity_verdict_20261001.md` §3) 의 비식별성 경고 그대로.
⇒ **판별 실험 (값싼 것)** = 우리 5 조성을 **이 논문 방식** (가압 중 두께 + 같은 다이 안 제거 뒤 두께 + 피스톤 교정) 으로 재는 것.  135 µm 전극에서 두께 1 µm ≈ 공극 0.56 %p [우리 산술] 라서 **두께 정밀도 ≲1 µm** 가 필요하다 (이 논문의 마이크로미터 1 회 정밀도는 5 µm).

---

## 1. 한 줄 요약
분말을 **스프링 하중 (일정압) 셀**에 넣고 압력을 단계적으로 올리며 **매 단계마다 가압 중 두께 · 최소압 (110 kPa) 으로 놓은 뒤 두께 · 임피던스**를
같은 다이 안에서 잰다 → 두께를 피스톤 압축으로 교정하고 (Eq. 1) 입자 탄성 변형을 보정해 (Eq. 2–4) **가압 중 공극**을 내는 시험대 (저자: *"This novel approach"* p.32831).
µc-Li₅.₅PS₄.₅Cl₁.₅ 는 10 → 400 MPa 에서 ε 0.30 → 0.04 (치밀화 대부분 **비가역**), pc-NMC622 는 0.34 → 0.14 (치밀화 **상당 부분 가역**),
σ(ε) 는 두 영역 — 고공극 (ε > 0.17–0.2) 은 **입자 형상 변화가 계면 접촉을 개선**해 σ 가 MWBH 보다 가파르게 오르고, 저공극은 **공극 감소만** 남아 MWBH 를 따른다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| V. Miß, F. Lange, S. Staubitz, **B. Roling\*** (Univ. Marburg, mar.quest) | ACS Appl. Mater. Interfaces 18 (2026) 32830–32836 · CC-BY 4.0 | 10.1021/acsami.6c03789 | **µc-Li₅.₅PS₄.₅Cl₁.₅** (자체 합성, 550 °C 6 h 어닐) · **pc-LiNi₀.₆Mn₀.₂Co₀.₂O₂** (상용 MSE Supplies) — **각각 단일상 펠릿 (복합체 아님)** | 실험 — 장치 개발 + 압력별 in situ 두께 · EIS · FIB-SEM.  **시뮬레이션 없음** |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 셀 상수 (Table S1 · 본문)
| 항목 | µc-Li₅.₅PS₄.₅Cl₁.₅ | pc-NMC622 | 표지 · 쪽 |
|---|---|---|---|
| 펠릿 1 개의 입자 질량 m | **80.2 mg** | **80.0 mg** | [인쇄] Table S1 (SI p.6) |
| "Diameter of the pellet d" | 0.5 cm (⚠ **반지름으로 읽어야 재현** — §4-4) | 0.5 cm | [인쇄] Table S1 · 해석 [재계산] |
| 입자 밀도 ρ₀ ("crystal density", 본문) | **1.87 g/cm³** (SI ref 1 = Adeli 2019) | **4.48 g/cm³** (SI ref 5 = Hua 2020) | [인쇄] Table S1 · p.32833 |
| 영률 E (탄성 보정용) | **67 GPa** (SI ref 6 = Munsif 2023, DFT Li₆PS₅X) | **180 GPa** (SI ref 7 = Liu 2024) | [인쇄] Table S1 |
| 결정밀도 대조 (adeli2019 카드 격자상수로) | 1.878 (Li₅.₅PS₄.₅Cl₁.₅, a 9.8061 Å, Z 4) · Li₆PS₅Cl 은 **1.860** (a 9.8598 Å) | — | [우리 산술] — 우리 SE 2.0 보다 7.5 % 낮다 |
| 입경 · 입도분포 | **[미확인]** (본문 · SI 수치 없음).  SEM (Fig. 5 위) 판독: 각진 조각 ~1–15 µm (한 시야, 대략) | **[미확인]**.  SEM: 구형 2차입자 ~8–11 µm (5 µm 막대 기준, 한 시야 대략) | [판독] 정성 |
| 결정성 · 순도 | XRD = Li₅.₅PS₄.₅Cl₁.₅ 기준과 일치 (Fig. S2) — 별표 4 개 = 소량 **LiCl · γ-Li₃PS₄** 반사 (본문은 "successful synthesis" 만, 불순물 무언급) | 상용 (분석 없음) | [인쇄] p.32832 · 별표 [판독] |
| 측정 온도 | **[미확인]** | **[미확인]** | 본문 · SI 전수 |

### 3-2. ★ 가압 중 ↔ 최소압 (110 kPa) 두께 — Table S2 전수 (SI p.6) + 우리 재계산

**µc-Li₅.₅PS₄.₅Cl₁.₅** (d 인쇄값 mm · 회복 = d_min/d_load − 1 [재계산] · Δd_strain = 인쇄 / 우리 재계산 d_min·p/E)

| p (MPa) | 가압 중 d | 최소압 d | **회복** | Δd_strain 인쇄 | 재계산 |
|---|---|---|---|---|---|
| 10 | 0.77875 | 0.778125 | −0.08 % | −0.000116 | 0.000116 |
| 20 | 0.736875 | 0.744375 | +1.02 % | −0.000222 | 0.000222 |
| 30 | 0.71625 | 0.718125 | +0.26 % | −0.000322 | 0.000322 |
| 40 | 0.701875 | 0.7 | −0.27 % | −0.000418 | 0.000418 |
| 50 | 0.680625 | 0.6875 | +1.01 % | −0.000513 | 0.000513 |
| 70 | 0.66375 | 0.669375 | +0.85 % | "−0-000700" (인쇄 오타) | 0.000699 |
| 100 | 0.6475 | 0.66 | +1.93 % | −0.000985 | 0.000985 |
| 150 | 0.620625 | 0.634375 | +2.22 % | −0.001421 | 0.001420 |
| 200 | 0.604375 | 0.6175 | +2.17 % | −0.001844 | 0.001843 |
| 250 | 0.5925 | 0.603125 | +1.79 % | −0.002251 | 0.002250 |
| **300** | **0.588** | **0.5975** | **+1.62 %** | −0.002671 | **0.002675** (⚠ 끝자리 반올림을 넘는 불일치는 이 행만 · 0.15 %) |
| 350 | 0.575625 | 0.588125 | +2.17 % | −0.003072 | 0.003072 |
| 400 | 0.566875 | 0.5825 | **+2.76 %** | −0.003478 | 0.003478 |

**pc-NMC622**

| p (MPa) | 가압 중 d | 최소압 d | **회복** | Δd_strain 인쇄 | 재계산 |
|---|---|---|---|---|---|
| 50 | 0.343125 | 0.345625 | +0.73 % | −0.000096 | 0.000096 |
| 100 | 0.32625 | 0.33375 | +2.30 % | −0.000185 | 0.000185 |
| 150 | 0.311875 | 0.321875 | +3.21 % | −0.000268 | 0.000268 |
| 200 | 0.29625 | 0.31125 | +5.06 % | −0.000346 | 0.000346 |
| 250 | 0.285625 | 0.304375 | +6.57 % | −0.000423 | 0.000423 |
| **300** | **0.276875** | **0.29875** | **+7.90 %** | −0.000497 | 0.000498 |
| 350 | 0.26875 | 0.291875 | **+8.61 %** (최대) | −0.000567 | 0.000568 |
| 400 | 0.264375 | 0.283125 | +7.09 % | −0.000629 | 0.000629 |

- 본문 요약: *"After releasing the respective applied pressure to the minimum pressure, the sample thickness increases by 0.3−2.8%."* [인쇄] p.32832 — ⚠ 표에는 **음수 두 칸** (10 MPa −0.6 µm · 40 MPa −1.9 µm) 이 있다 = 불확도 안 (아래).
- **불확도**: *"The uncertainties of the thickness and pressure data are of the order of the symbol size or lower."* [인쇄] p.32832 → Fig. 3a 기호 ≈ 0.005–0.006 mm [우리 산술, 축 보정].  마이크로미터 정밀도 *"5 µm"* [인쇄] p.32832.
  ⇒ SE 회복 (300 MPa 9.5 µm) 은 불확도의 약 2 배 · NMC 회복 (21.9 µm) 은 약 4 배.
- 관찰 (추정): 인쇄 두께가 **300 MPa SE 가압 중 0.588 한 칸만 빼고 전부 0.000625 mm (= 5 µm / 8) 의 배수** → 5 µm 눈금을 8 회 평균한 것으로 보인다 (서술 없음).  그 한 칸은 Δd 재계산도 0.15 % 어긋난다 → 전사 단계의 미세 오기 의심 (판정 무영향 — 회복 1.5–1.6 % 범위 안).

### 3-3. ★ 공극 — Eq. 2 를 세 규약으로 다시 계산 vs Fig. 4a 판독 (r = 0.5 cm)

**µc-Li₅.₅PS₄.₅Cl₁.₅** — 가압 중 [인쇄 Eq. 2 그대로 (d + Δd, Δd < 0) · 탄성 보정 없음 · **d + \|Δd\| (그림 규약)**] · 놓은 뒤 · 판독

| p | 인쇄 Eq. 2 | 보정 없음 | **d + \|Δd\|** | Fig. 4a ● 판독 | 놓은 뒤 (재계산) | Fig. 4a □ 판독 |
|---|---|---|---|---|---|---|
| 10 | 0.2987 | 0.2988 | 0.2989 | 0.3016 | 0.2982 | (겹침) |
| 100 | 0.1554 | 0.1567 | **0.1579** | 0.1581 | 0.1726 | (겹침) |
| 150 | 0.1181 | 0.1201 | **0.1221** | 0.1234 | 0.1392 | 0.1396 |
| 200 | 0.0937 | 0.0965 | **0.0992** | 0.0999 | 0.1157 | 0.1161 |
| 250 | 0.0749 | 0.0784 | **0.0819** | 0.0826 | 0.0946 | 0.0960 |
| **300** | 0.0671 | 0.0713 | **0.0755** | **0.0764** | **0.0861** | **0.0874** |
| 350 | 0.0463 | 0.0514 | **0.0564** | 0.0579 | 0.0715 | 0.0729 |
| 400 | 0.0308 | 0.0367 | **0.0426** | 0.0430 | 0.0626 | 0.0629 |

- p ≥ 100 MPa 7 점: 판독 − 재계산 = **+0.0079** (인쇄 Eq. 2) · +0.0043 (보정 없음) · **+0.0008 (d + \|Δd\|)** — rms 0.0085 · 0.0046 · 0.0009 [판독 vs 재계산].
  본문 *"about 0.04 at 400 MPa"* [인쇄] p.32833 도 0.043 (반대 부호) 쪽이다 (인쇄 Eq. 2 면 0.031).  ⇒ §4-4.
- **pc-NMC622** (세 규약 차가 ≤0.004 라 부호 판별 불가 — d + \|Δd\| 로 적음): 가압 중 50 → 400 MPa = 0.3376 · 0.3035 · 0.2716 · 0.2334 · 0.2052 · **0.1803** (300) · 0.1558 · 0.1420 / 놓은 뒤 0.3422 · 0.3188 · 0.2936 · 0.2695 · 0.2530 · **0.2389** (300) · 0.2210 · 0.1969 [재계산] — 판독 □ 와 ≤0.003 (Fig. 4a).
- 본문 인쇄값: SE *"from about 0.30 at 10 MPa to about 0.04 at 400 MPa"* · NMC *"from values of about 0.34 at 50 MPa to about 0.14 at 400 MPa"* (p.32833) · SEM 문맥 *"50 MPa (corresponding to ε_void = 0.33)"* · *"200 MPa (… 0.23)"* · *"200 to 400 MPa (… 0.14)"* (p.32834).
- 저자 해석: 고압 공극이 *"much lower than the porosity of a dense packing of spheres, even if these spheres are polydispersive"* (ref 31) → SE 는 **강한 비가역 입자 변형**, NMC 는 **1차입자 접촉 파괴 · 재배열 (2차입자 형상 변화)** (p.32833–32834).

### 3-4. ★ 다이 밖 (밀어낸 펠릿) 두께 — 400 MPa 뒤 한 번 [판독]
| | 가압 중 400 MPa | 다이 안 놓은 뒤 | **다이 밖** [판독] | 다이 밖 / 가압 중 | 다이 밖 / 놓은 뒤 | 다이 밖 공극 [재계산] |
|---|---|---|---|---|---|---|
| SE | 0.566875 | 0.5825 | **0.6036 mm** | **+6.5 %** | +3.6 % | 0.095 |
| NMC622 | 0.264375 | 0.283125 | **0.2689 mm** | **+1.7 %** | **−5.0 %** | 0.155 |

- 판독 보정: 두께 축을 **인쇄 두께** (SE 23 점 · NMC 15 점) 로 맞춤 — 최대 잔차 0.48 µm · 0.18 µm.  Fig. 3b · S4b 의 파란 σ 가 바로 이 두께를 썼다 (σ_파랑/σ_검정 = d_밖/d_가압 이 판독에서 ≤1 % 로 성립) → **저자 자신이 쓴 다이 밖 두께**와 같다.
- SE: 다이 밖 > 다이 안 놓은 뒤 (본문 *"Removal of the pellet … leads to a further increase in the sample thickness"* p.32832–32833).  **NMC: 다이 밖 < 다이 안 놓은 뒤 — 저자 무언급** (§10-②).

### 3-5. 전도도 (Fig. 3b · S4b) · MWBH 적합 (Fig. 4b) · 우리 tau2
- SE σ_ion (in situ 두께) [판독]: 10 MPa 0.58 · 20 1.03 · 50 1.86 · 100 3.14 · 150 3.47 · 200 3.55 · 250 3.74 · **300 3.85** · 350 3.90 · 400 3.89 mS/cm.
  본문: *"converge to a constant value of about 4 mS cm−1 at pressures above 300 MPa"* · *"increase … by about 1 order of magnitude"* [인쇄] p.32833 (판독 비 ≈6.8 배).
- 같은 SE 를 **다이 밖 두께 하나로** 계산하면 [판독] 10 MPa 0.45 (−22 %) … 200 MPa 3.55 (≈0) … 400 MPa 4.14 (**+6.5 %**) — *"do not converge … misleading information about the pressure dependence"* [인쇄] p.32833.
- NMC622 σ_e (in situ) [판독]: 50 MPa 1.85 · 100 4.46 · 150 7.12 · 200 9.73 · 250 11.87 · **300 12.87** · 400 15.86 mS/cm.  SI: σ_e 증가는 **비가역**, 놓을 때 σ_e 는 거의 일정 (*"except at very low pressures, at which sample/electrode interfacial resistances become relevant"*) — 근거는 그들 이전 논문 (SI ref 4 = Miß 2025 ACS Mater. Lett.) · **이 논문에는 놓은 뒤 σ 자료가 안 실림** [인쇄] SI p.4.
- **MWBH 적합** (Eq. 5, σ = σ₀ (1 − ε)^(3/2)): 범례 **σ₀ = 4.1 mS/cm (SE) · 18.2 mS/cm (NMC)** [인쇄 — 그림 범례] · σ₀ = *"conductivity of a void-free pellet"* (p.32834).
- **데이터 / MWBH 비** (우리 산술 — ε 는 d + \|Δd\| 재계산, σ 는 판독): SE 10 MPa **0.24** · 20 0.39 · 50 0.63 · 70 0.73 · **100 0.99** · 150–400 1.01–1.06 / NMC 50 MPa **0.19** · 100 0.42 · 200 0.80 · 250 0.92 · 300 0.95 · 350–400 1.02–1.10.
- **우리 이름의 수송 tortuosity** tau2 = φ·σ₀/σ_eff (φ = 1 − ε, σ₀ = 위 MWBH 적합값 — ⚠ 독립 측정 아님) [우리 산술]:
  SE 10 MPa **5.0** · 20 3.0 · 30 2.2 · 50 1.8 · 70 1.5 · **100 1.10** · 150–400 **0.98–1.04** (MWBH 자체 = (1−ε)^−½ = 1.02–1.07) / NMC (전자 채널) 50 MPa 6.5 · 100 2.8 · 200 1.4 · 300 1.16 · 400 0.98.
  ⛔ 우리 복합 전극 tau2 (수 단위) 와 **같은 표에 놓지 않는다** — 단일상 펠릿 · σ₀ 정의 (적합값) · 상 분율이 다르다.

### 3-6. 두 공극 영역 · SEM (Fig. 4 배경 · Fig. 5 · Fig. 6 · Fig. S5)
- 경계: Fig. 4 캡션 *"(i) blue: ε_void > 0.2; (ii) yellow: ε_void < 0.17. The shaded area marks the transition"* · 결론 *"ε_void > 0.17−0.2 … ε_void < 0.17−0.2"* [인쇄] p.32833 · p.32835.
- SE: *"data … at porosities ε_void ≤ 0.17 … are well described by the MWBH theory … ε_void > 0.17 … deviate strongly … interfacial contact effects at pressures below 100 MPa"* [인쇄] p.32834.
- NMC: 50 MPa (ε 0.33) 거의 구형 · 접촉부 약간 변형 → 200 MPa (ε 0.23) 2차입자 형상 크게 변하고 계면 **평평해짐** (흰 선) → 200–400 MPa (ε 0.14) 는 *"mainly … a reduction of the void space"* [인쇄] p.32834.
- SE: 50 MPa 조각 사이 공극 → 100 MPa 계면 맞물림 → 400 MPa 치밀 (흰 선 = 형상 변화로 개선된 계면) [인쇄 캡션 + 판독].
- Fig. S5 (판독, 본문 무언급): NMC 50 MPa 단면에 **2차입자 중심 공동 + 방사형 균열** · 2차입자 내부의 작은 기공 점들 (Fig. 5 · S5 전부) · 200 MPa 에서 2차입자 사이 1차입자 파편.
- Fig. 6 모식: hard oxidic (NMC) vs soft sulphidic (LPSCl) — (i) 저압 = 형상 변화로 계면 접촉 개선 → (ii) 고압 = 공극 감소.

### 3-7. 가역 · 비가역 치밀화 (우리 산술)
본문 판정: *"the major fraction of the densification of μc-LPSCl is irreversible, while a significant fraction of the densification of pc-NMC622 is reversible"* [인쇄] p.32834.
크기 [재계산]: 첫 단계 → 400 MPa 치밀화 중 400 MPa 에서 놓을 때 되돌아오는 몫 = **SE 7.8 %** (ε 0.299 → 0.043, 놓으면 0.063) · **NMC 28.1 %** (0.338 → 0.142, 놓으면 0.197).  ⚠ 기준이 첫 측정 단계 (SE 10 · NMC 50 MPa) 이지 헐거운 분말이 아니다.

### 3-8. Heckel — 논문은 안 했다, 우리 적합 [우리 산술 — 재계산 공극으로 ln(1/ε) = K·p + A]
| 시료 · 상태 | 범위 | K (1/GPa) | P_y = 1/K | R² |
|---|---|---|---|---|
| SE 가압 중 (d + \|Δd\|) | 10–400 MPa (13 점) | 4.57 | **219 MPa** | 0.984 |
| SE 가압 중 (d + \|Δd\|) | 100–400 MPa (7 점) | 4.11 | **243 MPa** | 0.985 |
| SE 가압 중 (보정 없음) | 10–400 · 100–400 | 4.88 · 4.54 | 205 · 220 MPa | 0.987 · 0.983 |
| SE 놓은 뒤 | 10–400 · 100–400 | 3.80 · 3.34 | 263 · 300 MPa | 0.978 · 0.991 |
| NMC 가압 중 | 50–400 · 100–400 | 2.56 · 2.61 | **391 · 384 MPa** | 0.998 · 0.998 |
| NMC 놓은 뒤 | 50–400 | 1.52 | 658 MPa | 0.995 |
- ⚠ **단계 하중 · 반복 제거 이력**의 in-die 값 (단조 Heckel 과 다를 수 있음) · ρ₀ 선택이 ε 를 비균일하게 바꿔 K 를 움직인다.

---

## 4. ★ 방법 — 장치 · 측정 사슬 · 입자 처리

### 4-1. 측정 셀 · 시험대 (Fig. 1 · Fig. 2a · p.32831–32832)
- 셀 = **경화강 피스톤 2 개** (*"to avoid any warping of the pistons at high pressures"*) + **PEEK 밀폐 하우징** (글러브박스 밖 불활성 측정) · 실링 링 6 · 양쪽 뚜껑 2 (피스톤 기울어짐 방지).  도식 (Fig. 1a) 상 시료를 감싸는 벽 = PEEK 몸체 — **별도 슬리브 서술 없음** [미확인].
- 피스톤 바깥 끝에 **마이크로미터 오목부** + 가운데 **홈** (Fig. 1c) → 마이크로미터 (Mitutoyo, 측정 부리) 를 같은 자리에 재현 위치.  *"micrometer screw is preferable to a caliper due to the higher precision … (5 µm)"*.
- 시험대 (Fig. 2a): 가이드 레일 (셀 기울어짐 방지) · **스프링 4 개**로 일정압 · 중앙 나사 + 토크 렌치로 하중, **스프링 길이 변화 (캘리퍼, Holex)** 로 힘을 잰다.

### 4-2. 두께 측정 · 순응도 보정 (Eq. 1 · Fig. 2b)
- 측정량 d(p) = 피스톤 둘 길이 + 시료 두께 (마이크로미터).  **시료 없이** 피스톤 길이 d_pistons(p) 를 압력별로 교정 → **d_sample(p) = d(p) − d_pistons(p)** (Eq. 1, p.32832).
- 이것이 이 논문의 **유일한 장치 순응도 보정** — 피스톤 (경화강) 축 방향 탄성만.  교정 곡선 값 · 반복성 [미확인] · PEEK 하우징 반경 팽창 · 벽 마찰 [미확인].

### 4-3. 압력 · 프로토콜 (Fig. S1 · Fig. S3 · p.32831–32832 · SI p.2–3)
- 스프링 (Febrotec; 내경 20 · 외경 40 · 길이 102 mm): ≤250 MPa 는 연한 것 (공칭 **170.3 N/mm**, SI "170 ± 10 %"), 그 위는 단단한 것 (**762 N/mm**).  실측 기울기 (Fig. S1 범례) 연 173.2 · 182.6 · 183.4 · 188.3 · 강 754.1 · 743.5 · 741.0 · 742.6 N/mm — 전부 공차 안 [인쇄 SI p.2].
- 최소압 ≈ **110 kPa** = 위 피스톤 무게 + 대기압 (p.32832).
- **프로토콜** (Fig. S3): SE = 10 · 20 · 30 · 40 · 50 · 70 · 100 · 150 · 200 · 250 · 300 · 350 · 400 MPa (13 단계) · NMC = 50 · 100 · … · 400 (8 단계) — **매 단계 일정압에서 두께 + 임피던스 → 최소압으로 놓고 두께 + 임피던스 → 다음 단계**.  400 MPa 뒤 밀어내 다이 밖 두께 (p.32832).
- 유지 시간 · 하중 속도 [미확인].  스프링 강성 ≈ "some 100 N/mm" → *"changes in pressure due to changes in sample thickness are negligible"* [인쇄] (우리 산술: 강한 스프링 4 개 ≈2980 N/mm 면 10 µm 압축 → 30 N = 300 MPa 하중의 0.13 %).

### 4-4. 공극 계산 (Eq. 2–4) — ⚠ 인쇄 결함 둘
- Eq. 2: ε_void(p) = 1 − ρ(p)/ρ₀ = 1 − m / (π r² × (d_sample(p) + Δd_elastic(p)) × ρ₀) · Eq. 3: Δd_elastic(p)/d_sample(p=0) = −p/E · Eq. 4: Δd_elastic = −d_0.11 MPa × p/E (최소압 두께를 d(p=0) 로 근사) [인쇄] p.32833.
- **결함 (i) 지름 ↔ 반지름**: Table S1 *"Diameter of the pellet d / cm = 0.5"* 를 지름으로 넣으면 10 MPa ε = **−1.805** (밀도 5.2 g/cm³ > ρ₀) → 불가능.  r = 0.5 cm (지름 10 mm) 면 **+0.299** = 본문 "≈0.30" · 그리고 Fig. 4a □ 전부를 ≤0.0015 로 재현 [재계산].  (합성 단계 펠릿도 *"diameter of 10 mm"* p.32831 — 측정 셀 보어 지름은 따로 안 적힘.)
- **결함 (ii) 탄성 보정 부호**: Eq. 2 그대로 (d + Δd, Δd < 0) 면 가압 중 공극이 **작아지는** 쪽인데, Fig. 4a 닫힌 점은 **d − Δd (= d + d_0.11 MPa·p/E ≈ d(1 + p/E))** 로 계산한 값과 맞는다 (§3-3).  물리적으로는 그림 쪽이 맞다 — 하중 아래 입자가 탄성 압축되면 고체 밀도가 올라가 **공극이 커지는** 보정이어야 한다.  ⇒ 인쇄된 식의 부호 오기로 판단 (저자 확인 전 · 추정).
- 부수: 본문은 탄성 보정값이 *"given in Table S1 of the SI"* 라 하나 실제로는 **Table S2** (Table S1 은 E 값) · 캡션 "MWHB" ↔ 본문 "MWBH" 표기 불일치 (사소).
- E 선택: SE **67 GPa** (DFT 인용) 은 우리 DFT E_VRH **22.06 GPa** 의 3 배이고 Fan 2026 §3.5 밴드 10–30 GPa (`fan2026_sulfide_assb_stability_review_ECERD2600097`) 밖 → 보정 크기가 1/3 로 작게 들어갔다 (300 MPa: 0.45 % vs E 22 면 1.36 %) [우리 산술].  보정이 공극에 주는 몫은 300 MPa 에서 0.4 %p (E 67) · 1.3 %p (E 22) 급.

### 4-5. 전도도 측정 (EIS · p.32831)
- **NEISYS** Potentiostat/Galvanostat/EIS Base Unit (Novocontrol) · **1 MHz – 0.1 Hz · 10 mV_rms** · 해석 **RelaxIS** (rhd instruments).  SE = 이온 σ · NMC = 전자 σ (둘 다 임피던스).
- 등가회로 · 전극 (피스톤이 전극으로 읽힘 — 명시 없음) · 온도 [미확인].  σ = d/(R·A) 의 d 를 in situ 두께로 쓴 것이 핵심 (Fig. 3b).

### 4-6. 합성 · 분석
- **µc-LPSCl** (2 g 배치, Ar 글러브박스 H₂O · O₂ < 1 ppm): Li₂S (99.9 %, Alfa Aesar) · P₂S₅ (Sigma-Aldrich) · LiCl (≥99.98 %, Sigma) 마노 유발 10 분 → **⌀10 mm · 196 MPa · 1 분** 펠릿 (P/O/Weber, 연마 스테인리스 압출다이) → 석영 앰플 진공 봉입 → **550 °C (0.5 °C/min, 6 h)** → 서랭 → 마노 유발 분쇄 (p.32831).  ⇒ "µc" = 어닐 고결정 (cronau2021 카드 §µC 정의와 같은 계열).
- **pc-NMC622**: 상용 (MSE Supplies, Tucson) — 입경 · 비표면적 [미확인].
- XRD: STOE STADI MP, Cu Kα, Debye–Scherrer (Ar 밀봉 모세관).  FIB-SEM: Zeiss Crossbeam 550 · 불활성 이송 (Semilab 셔틀) · 단면 폭 20 µm × 깊이 15 µm · Ga 30 kV 3 단계 (3 nA → 700 pA → 100 pA) · SEM 5 kV · 100 pA · SE 검출기 · **무가압 상태에서 촬영** (p.32831).

### 4-7. 입자 처리 ★ · 시뮬레이션 · frame[5]
- **시뮬레이션 없음.**  실제 입자: SE = 각진 µc 조각 (구 아님) · CAM = 1차입자 응집 구형 2차입자.
- 변형 양식 (SEM 근거): SE = **진짜 입자 형상 소성** (계면 평탄화 · 400 MPa 치밀 — MPM 쪽 물리) · CAM = 2차입자 **재배열 · 1차입자 접촉 파괴 · 내부 균열** (DEM 파괴 쪽 물리) + **큰 가역 몫** (탄성 · 구조).
- frame[5]: 이 논문은 단일상에서 **기계 반쪽 (공극 · 두께, 가압 중 + 놓은 뒤)** 과 **수송 반쪽 (σ_ion · σ_e)** 을 같은 시료에서 동시에 잰다.  없는 반쪽 = 복합체 · 접촉 수 · 접촉 면적 · 3D 미세구조 · 모델.

### 4-8. 기법 미니 용어집
- **in situ 두께** = 하중 아래에서 잰 두께 (이 논문) ↔ **ex situ 두께** = 측정이 끝나고 꺼낸 펠릿 두께 (Cronau 2021 등 기존 관행 — cronau2021 카드 §S-3a).
- **순응도 보정 (compliance)** = 기계 (피스톤 · 다이) 자체의 탄성 변형을 빼는 것 — 여기서는 시료 없는 피스톤 교정 (Eq. 1).
- **탄성 보정 (Eq. 3–4)** = 하중 아래 입자 자체의 탄성 압축을 공극 계산에 반영 — 고체 부피가 줄어든 만큼.
- **MWBH** (Maxwell–Wagner–Bruggeman–Hanai, ref 32) 유효매질식 σ = σ₀(1 − ε)^(3/2): 절연 공극이 전도 매질에 흩어진 그림 = Bruggeman 지수 1.5 · 우리 tau2 로는 (1 − ε)^(−1/2).
- **Heckel** ln(1/ε) = K·p + A · P_y = 1/K (우리 frame[3] 의 거시 교차검증 축).
- **활성화 부피 ΔV** σ(p) = σ(0)·exp(−pΔV/RT) — 물질 고유 σ 의 압력 의존 (ref 30 Faka 2023: 아지로다이트 0.6–1.1 cm³/mol → 0 → 400 MPa 에서 −10–20 % [인쇄 p.32833]).
- **pc / sc** = 다결정 2차입자 / 단결정 CAM.  **µc / gc** = 어닐 미세결정 / 유리-세라믹 SE.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | (a) 밀폐 측정 셀 단면 — 경화강 피스톤 2 + PEEK 하우징 + 실링 링 + 뚜껑 (b) 셀 + 마이크로미터 기술도 (c) 피스톤 오목부의 홈 (마이크로미터 재현 위치) | 우리 실험의 다이 안 두께 측정 설계 참고 — 재현 위치 · 경화강 피스톤 |
| 2 | (a) 시험대: 스프링 4 + 가이드 레일 + 중앙 나사 (b) 측정 원리 (1) 시료 없이 d_pistons(p) (2) d(p) = d_pistons + d_sample | ★ 순응도 보정 절차 (Eq. 1) — 우리 5 조성 두께 측정에 그대로 이식 가능 |
| 3a | SE 두께 vs p: 가압 중 ● · 110 kPa 로 놓은 뒤 ■ · 다이 밖 ◆ (400 MPa 뒤 하나) — 값 = Table S2 | ★ 가설 (a) 의 SE 쪽 회복 (300 MPa 1.6 %) · 다이 밖 +6.5 % [판독] |
| 3b | SE σ_ion vs p: in situ 두께 ● vs 다이 밖 두께 ◆ — in situ 는 ≥300 MPa ≈3.9 로 수렴, ex situ 는 수렴 안 함 | 우리 σ₀ 3.0 (Cronau ex situ 두께) 의 두께 규약 편향 크기 (−22 % … +6.5 %) · τ 메모 §3-8 ③ 의 실측 예 |
| 4a | 공극 vs p: SE 검정 · NMC 보라 · 닫힘 = 가압 중 · 열림 = 놓은 뒤 · 배경 = 두 영역 (파랑 ε > 0.2 · 노랑 ε < 0.17 · 빗금 = 전이) | ★ CL-94 후보 (300 MPa 0.076 / 0.087 [판독]) · 우리 Heckel 적합 · Eq. 2 부호 판별의 근거 |
| 4b | σ vs ε (로그) + MWBH 적합선 (σ₀ 4.1 · 18.2 mS/cm, 범례) · 화살표 (i) 접촉 개선 · (ii) 공극 감소 | 두 영역 ↔ 우리 접촉망 Holm 협착 / 복셀 CF 가지 · tau2 산출 |
| 5 | SEM: 분말 (맨 위) + FIB 단면 — NMC 50 · 200 · 400 MPa (왼쪽) · SE 50 · 100 · 400 MPa (오른쪽) · 흰 선 = 형상 변화로 개선된 계면 | SE 형상 소성 = MPM 쪽 물리의 정성 증거 · NMC 2차입자 파쇄 · 내부 기공 |
| 6 | 모식: hard oxidic (NMC) vs soft sulphidic (LPSCl) — (i) 저압 접촉 개선 → (ii) 고압 공극 감소 | frame[5] 그림 언어 (접촉 지배 ↔ 공극 지배) 와 대응 |
| S1 | 스프링 4 개씩 힘–변위 (연 · 강, 공칭 170.3 · 762 N/mm 대비) | 압력 정확도 (±10 % 공차 안) |
| S2 | µc-LPSCl XRD vs 기준 (Li₅.₅PS₄.₅Cl₁.₅ · LiCl · γ-Li₃PS₄) — 별표 = 불순물 반사 (본문 무언급) | 시료 순도 한정어 |
| S3 | 압력 프로토콜: (a) SE 13 단계 (b) NMC 8 단계 — 단계마다 최소압으로 놓기 | ⚠ 단계 하중 · 반복 제거 — 우리 단조 가압과 다름 |
| S4 | (a) NMC 두께 가압 중 · 놓은 뒤 · 다이 밖 (b) σ_e — in situ vs 다이 밖 두께 | ★ CAM 회복 7.9 % (300 MPa) · 다이 밖 +1.7 % [판독] 의 모순 |
| S5 | 추가 SEM — NMC 50 · 200 MPa · SE 50 MPa | NMC 2차입자 중심 공동 · 방사형 균열 · 내부 기공 (판독) — PC 내부 공극 후보 (DEM AM = 꽉 찬 구) 의 정성 근거 |
| Table S1 | 질량 80.2 · 80.0 mg · "지름" 0.5 cm (⚠ 반지름으로 읽어야 재현) · ρ₀ 1.87 · 4.48 · E 67 · 180 GPa | 공극 재계산 입력 · E 선택 비판 (§4-4) |
| Table S2 | 압력별 가압 중 · 최소압 두께 + Δd_strain (SE 13 · NMC 8 단계) | ★ 가설 (a) 핵심 숫자 — 전수 §3-2 |

## 6. Post-processing ★
- **무엇을**: 두께 (마이크로미터, 피스톤 교정 뺌) → 공극 (Eq. 2, 탄성 보정 Eq. 3–4) · 임피던스 → R → σ = d/(R·A) (in situ 두께 vs 다이 밖 두께 두 판) · σ(ε) 를 MWBH (Eq. 5) 에 적합해 σ₀ 와 두 영역 경계 판정 · FIB-SEM 단면으로 형상 변화 정성 확인.
- **도구**: RelaxIS (EIS) · Zeiss FIB-SEM · 그림 도구 [미확인].  적합 방법 (σ₀ 를 어떤 점들로 · 가중) [미확인] — 범례에 σ₀ 숫자만.
- **안 한 것**: Heckel · 퍼콜레이션 문턱 적합 · 오차막대 · 반복 시료 (n = 1 로 읽힘) · 놓은 뒤 σ 공개 · 복합체.
- **우리 후처리 (이 카드)**: 표 S2 재계산 (세 규약 · 회복률 · 가역 몫 · Heckel) · 그림 판독 (인쇄값 보정) · tau2 · 가설 (a) 산술 — 전부 `tools/litdb/miss2026_digitize.py` 와 §3 표로 재현 가능.

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · `docs/` 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 측정 상태 | **가압 중** + **다이 안 놓은 뒤 (110 kPa)** + 다이 밖 (400 MPa 뒤) | ps45 실험 = 다이 안 · 300 MPa 뒤 **하중 제거 후** (3 회 평균 · 경향 맞는 3 개 선택) · DEM = 300 MPa **판 정지 + 판 고정 이완** (= 가압 중 두께) | ⚠ 우리 실험 ↔ DEM 비교는 **놓은 뒤 ↔ 가압 중** — 이 논문이 그 사이의 크기를 단일상으로 준다 |
| 공극 규약 | 결정밀도 ρ₀ (1.87 · 4.48) + 질량 + in situ 두께 + 탄성 보정 | 실험 = 질량 + 두께 + 진밀도 AM 4.8 · SE 2.0 / DEM = 구 부피 합 (ε_sphere) | SE 밀도 2.0 ↔ 1.87 (결정 1.86–1.88, 우리 산술) — 실험 공극에 −1.7…−1.9 %p 차이 |
| 회복 (스프링백) | SE 1.6 % · CAM 7.9 % (300 MPa, 다이 안) · 다이 밖 6.5 % · 1.7 % (400 뒤) | **DEM · MPM 둘 다 제하 팔이 없다** (`comparison_vs_ours_DEM.md` F-SB1) | 이 논문 = 우리 release 팔의 첫 실험 표적 |
| 순수 SE 300 MPa 공극 | 7.1–7.6 % (가압 중) · 8.6 % (놓은 뒤) [재계산] | MPM 보정 표적 ≈10 % — **출처 철회 (원장 `CL-94`, 외부 앵커 없음)** | 후보 (§7-3) |
| Heckel P_y (순수 SE) | **≈220–245 MPa** (우리 적합, 가압 중) | DEM 순수 SE **138 MPa** (E 1.35, 4 압력, R² 0.965 — CLAUDE.md frame[3]) | DEM 이 1.6–1.8 배 무르다 — **조성 · 프로토콜 다름** (§7-6) |
| σ(ε) 영역 | ε > 0.17–0.2 접촉 지배 (MWBH 의 ≤0.24 배까지) · 아래는 MWBH | 접촉망 = 접촉당 Holm 협착 (DEM) · 복셀 FV = 계면 저항 0 인 CONTACT_FREE 가지 (`CL-81`) | 같은 물리의 두 끝 — §7-4 |
| σ₀ 기준 | MWBH 무공극 σ₀ 4.1 (Li₅.₅PS₄.₅Cl₁.₅) — 펠릿 평탄 3.9 의 1.05 배 | σ₀ 3.0 = Cronau 2021 SI S2c µC-Li₆PS₅Cl 펠릿 평탄 하단 (ex situ 두께) | §7-5 |
| 재료 | Li₅.₅PS₄.₅Cl₁.₅ · pc-NMC622 · **각각 단일상** | Li₆PS₅Cl + NCM (PC r 4.5 + SC r 2.0), AM:SE 81.6 : 18.4 복합체 | ⛔ 절대값 전이 금지 — 크기 · 방향 · 영역만 |
| 전달 채널 | σ_ion (SE) · σ_e (CAM) 각각 | σ_ion · σ_e · σ_thermal 삼중항 (복합체 망) | 우리가 넓다 · 그들은 측정 |

### 7-2. ★ 가설 (a) — 무엇이 서고 무엇이 안 서나
- **선다**: 단일상 다이 안 회복의 크기 = SE 1.6 % · pc-CAM 7.9 % (300 MPa) — 우리 필요량 7.4–13.0 % 와 **같은 자릿수의 위 끝 (CAM)** 과 **한 자릿수 아래 (SE)**.  ⇒ 스프링백이 차이의 **일부**인 것은 그럴듯하다 (≈1.1–6.2 %p, §0 표).
- **안 선다**: 10:0 · 0:10 의 9.2–9.3 %p 를 스프링백만으로 — 이 논문 어느 상의 300 MPa 값으로도 ≥3.5 %p 남는다.  0:10 (전부 SC) 은 이 논문에 **SC 자료가 없다**.
- **위 끝이 흔들린다**: CAM 의 다이 안 회복 7.1 % (400 MPa) 가 다이 밖에서는 +1.7 % 만 남았다 (§3-4).  SI 가 *"at very low pressures … sample/electrode interfacial resistances become relevant"* 라고 적듯 110 kPa 에서 **시료–피스톤 접촉이 불완전**할 수 있고 (추정), 그러면 단단한 CAM 의 "놓은 뒤 두께" 에 계면 틈이 섞인다.  ⇒ **우리 실험도 다이 안에서 재므로 같은 함정에 노출된다** — 놓은 뒤 두께를 작은 하중 (예: 수 MPa) 에서 다시 재 보는 대조가 필요하다.
- **SE 의 회복은 대부분 고체 탄성으로 읽힌다** (우리 해석): 300–400 MPa 회복 1.6–2.8 % 는 p/E (E 22 GPa → 1.4–1.8 %) 와 같은 자릿수 (측정이 1.2–1.5 배 · 불확도 ≈1 % 안) — 공극이 다시 열린다기보다 치밀한 고체가 탄성으로 늘어나는 크기.  100–250 MPa 에서는 회복 (1.8–2.2 %) 이 p/E (0.5–1.1 %) 보다 커 공극 쪽 가역 몫이 있을 수 있다 (불확도 ≈1 % 라 판정 약함).  CAM 은 p/E (E 180 → 0.17 %) 의 약 50 배 → 구조적 회복 (다공 2차입자 · 접촉).
- **다른 후보와의 크기 비교** (우리 산술): SE 진밀도 규약 −1.7…−1.9 %p (전 조성 비슷) · PC 내부 기공 (Fig. 5 · S5 에 보임, 수치 없음 — PC 많은 조성에만) · 두께 정밀도 (5 µm ≈ 2.8 %p) · 선택 편향 (3 개 선택).

### 7-3. ★ CL-94 후보 — 순수 SE 300 MPa 공극 (원장 · 다른 문서는 고치지 않는다)
| 상태 | 값 | 표지 |
|---|---|---|
| 가압 중 — 그림 규약 (d + \|Δd\|, E 67) | **7.55 %** | [재계산] (Fig. 4a 판독 0.076) |
| 가압 중 — 탄성 보정 없음 | 7.13 % | [재계산] |
| 가압 중 — 인쇄 Eq. 2 그대로 | 6.71 % | [재계산] |
| 가압 중 — E 22 GPa 로 보정했다면 | 8.4 % | [우리 산술] |
| 다이 안 놓은 뒤 (110 kPa) | **8.61 %** | [재계산] (판독 0.087) |
| 다이 밖 | 300 MPa 값 없음 · 400 MPa 뒤 9.5 % | [재계산 + 판독 두께] |
- ⇒ 옛 "≈10 %" (출처 철회) 는 이 범위의 **위 끝 (다이 밖) 근처**.  후보로만 — 한정어: Cl-rich **Li₅.₅PS₄.₅Cl₁.₅** (Li₆PS₅Cl 아님) · 550 °C µc · **단계 하중 (300 MPa 전 10 회 놓기)** · ρ₀ 1.87 (Adeli 결정밀도) · r = 0.5 cm 는 우리 추론 · 본문에 300 MPa 숫자 **인쇄 안 됨**.
- 규모 감각만 (결정 = 1저자): 우리 3D MPM σ_y 스윕 (ν 0.49, settled: 0.20 → 6.7 % · 0.25 → 9.0 % · 0.30 → 10.0 %, CLAUDE.md) 에 가압 중 7.1–7.6 % 를 표적으로 넣으면 σ_y ≈ 0.21–0.22 (선형 보간) — MPM 공극 규약 (union) ↔ 이 논문 규약 대조 전이다.

### 7-4. 두 공극 영역 ↔ 우리 두 σ 솔버
- **고공극 (ε > 0.17–0.2)**: σ 가 MWBH 의 0.24–0.73 배 (SE 10–70 MPa) = 계면 **협착**이 지배 → 우리 **DEM 접촉망 Holm 1/(2σa)** 가 담는 물리 · Stage-E Tabor/Physics 면적 보정이 겨누는 "형상 변화로 접촉 개선" (Fig. 5 흰 선) 의 정성 증거.
- **저공극 (ε < 0.17)**: 데이터 ≈ MWBH (0.99–1.06) → 접촉 몫 ≲5 % [우리 산술] = **계면 저항 0 인 복셀 CONTACT_FREE 가지가 근사로 맞는 영역** (치밀 순수 SE 한정).
- ⛔ 이 배수 (최대 ≈4) 를 우리 `R_brug_over_full` 4.04 / 6.69 와 **나란히 놓지 않는다** — 그 배수는 같은 접촉망 안의 CF/FULL 민감도다 (원장 `SELF-24` · `L2-07` 인용 금지 규약).
- **열린 질문 (이 논문이 못 가른다)**: 우리 복합체에서는 SE 가 AM 골격에 가려 덜 눌린다 (DEM 복합체 SE 겹침 1.75 % vs 순수 SE 11–12 %, CLAUDE.md 2026-06-06) → 복합체 SE 망이 300 MPa 에서도 **접촉 지배 영역**에 머물 수 있다.  복합체 in situ 자료가 나오면 판별된다.

### 7-5. 우리 σ₀ = 3.0 과의 관계 (판정 아님 — 정량 재료)
- 3.0 은 Cronau 2021 SI S2c µC-Li₆PS₅Cl 평탄의 하단이고 그 논문은 두께를 **측정 뒤 한 번 (ex situ)** 쟀다 (cronau2021 카드 §S-3a).  같은 그룹의 이 논문이 그 규약의 편향을 실측했다: 다이 밖 두께로 계산하면 10 MPa **−22 %** · 200 MPa ≈0 · 400 MPa **+6.5 %** [판독, Li₅.₅PS₄.₅Cl₁.₅] — **부호가 압력에 따라 바뀐다**.
- 펠릿 평탄 σ 에는 잔류 공극 벌점이 이미 있다 [우리 산술 — MWBH (1 − ε)^1.5 를 그대로 적용]: 이 논문 **in situ 치밀 상태** (300–400 MPa, ε 0.043–0.076) = **6–11 %** (데이터 / 적합 σ₀ 비로는 3.85/4.1 = 0.94 → 6 %) · 이 논문 **다이 밖** (400 MPa 뒤, ε 0.095) = 14 % · [Cronau 2021 SI S3] **다이 밖 밀도**를 결정밀도로 바꾸면 µC-Li₅.₅PS₄.₅Cl₁.₅ 16–19 % · **µC-Li₆PS₅Cl 25–30 %** (1.47 · 1.54 g/cm³ @195 · 292 MPa 제작 → ε 0.21 · 0.17, ρ₀ 1.860 = adeli2019 카드 격자상수로 계산).
  ⇒ CLAUDE.md `CL-91` 의 "펠릿 잔류기공 ↔ STEP3 명시 기공 부분 이중계상 (크기 미상)" 에 **첫 크기 범위 ≈6–30 %** — 폭을 정하는 것은 **σ₀ 3.0 을 잰 순간 (적층압 아래) 의 공극이 in situ 쪽이냐 다이 밖 쪽이냐**이고, 그 값은 어느 논문에도 없다 (Li₅.₅PS₄.₅Cl₁.₅ → Li₆PS₅Cl 전이도 미검증).
- 같은 조성 교차 확인: 이 논문 in situ 평탄 ≈3.9 ↔ [Cronau 2021 SI S2d] µC-Li₅.₅PS₄.₅Cl₁.₅ 3.97 (389 MPa 제작 · ~97 MPa 적층, 판독) ↔ [Cronau 2022] 3.97 (판독) — 같은 그룹 · 다른 프로토콜에서 ≈4 로 맞는다.
- [Cronau 2021 SI S3] µC-Li₅.₅PS₄.₅Cl₁.₅ 펠릿 밀도 1.59 · 1.63 · 1.66 g/cm³ (195 · 389 · 487 MPa 제작, 판독) 를 이 논문 ρ₀ 1.87 로 바꾸면 공극 15.0 · 12.8 · 11.2 % [우리 산술 — cronau2021 카드가 "다른 출처 결정밀도를 끌어오면 우리 산수" 라고 경고한 바로 그 계산] ↔ 이 논문 다이 밖 (400 MPa 뒤) 9.5 % — **단일 가압 · 다이 밖** 이 **단계 가압 · 다이 밖** 보다 1.7–3.3 %p 성기다 (프로토콜 효과 후보, 미분리 — 장비 · 시료 · 판독기도 다르다).

### 7-6. Heckel ↔ frame[3]
- frame[3] 이 비워 둔 *"Experimental multi-pressure Heckel for LPSCl powder is the missing direct validation"* 의 **첫 외부 후보**: µc-Li₅.₅PS₄.₅Cl₁.₅ 가압 중 P_y ≈ **219–243 MPa** (R² 0.98) [우리 적합] ↔ 우리 DEM 순수 SE 138 MPa ↔ 참고 [Schneider 2023] t-Li₇SiPS₈ 0.95 / 1.65 GPa (stated, 훨씬 단단한 다른 SE).
- ⚠ DEM 의 순수 SE 는 ε_sphere 가 음수 · 0 근처로 퇴화하는 영역 (CLAUDE.md 2026-06-06) 이라 P_y 비교는 **규약 대조 뒤에만** 판정 · 조성 · 단계 하중 · ρ₀ 차이 그대로.

### 7-7. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 단일상 기계 (가압 중 + 놓은 뒤 공극 · 가역 몫) + 수송 (σ_ion · σ_e 의 두 영역) — **실험**.
- **없는 것**: 복합체 · 3D 미세구조 · 접촉 수 · 면적 · 모델.  ⇒ DEM (접촉망 수송 · 패킹) 과 MPM (형상 소성 · 공극 채움) 의 **실험 대조점**을 각각 하나씩 준다 — 스프링백 축은 **둘 다 비어 있다** (F-SB1).

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **가설 (a) 의 판별 실험 설계** — 이 논문 Eq. 1 방식 (시료 없는 피스톤 교정) + 같은 다이에서 **300 MPa 가압 중 두께**와 **놓은 뒤 두께**를 우리 5 조성 각각 (반복 ≥3, 선택 없이 전부 보고).  두께 정밀도 ≲1 µm (135 µm 에서 1 µm ≈ 0.56 %p).  놓은 뒤 두께는 **두 하중 (≈0.1 MPa · 수 MPa)** 에서 재 계면 틈 효과를 가른다 (§7-2).
2. **DEM · MPM 제하 (release) 팔의 첫 실험 표적** — SE 1.6 % (300) · 2.8 % (400) · pc-CAM 7.9 % (300) · 8.6 % (350) 다이 안 · 다이 밖 SE 6.5 % · CAM 1.7 % (400 뒤).  F-SB1 의 기존 표적은 액체계 LIB · 압입 · DEM 산출뿐이었다.
3. **SE 진밀도 규약 정리** — 우리 2.0 ↔ 결정 1.86 (Li₆PS₅Cl) / 1.87–1.88 (Li₅.₅PS₄.₅Cl₁.₅): 실험 공극 −1.7…−2.1 %p.  DEM 침대도 2.0 으로 SE 질량을 넣으므로 **같은 질량비면 SE 부피가 7 % 작게** 들어간다 — 침대 쪽 효과는 재생성 없이는 미정.
4. **CL-94 후보** (§7-3) — 채택 · 표적 재보정은 1저자 결정.
5. **Heckel 외부 후보** (§7-6) — frame[3] 의 빈칸.
6. **σ₀ 규약 재료** (§7-5) — ex situ 두께 편향 (−22 … +6.5 %) · 잔류 공극 벌점 (치밀 in situ 6–11 % ~ 다이 밖 밀도 기준 16–30 %) 의 첫 크기 — CL-91 재해석 (저자 결정) 의 입력.
7. **τ 메모 §3-8 ③ (springback)** — kaiser2018 카드 §10-1 의 제안 *"부호는 R 측정 하중과 두께 측정 상태에 따라 갈린다"* 의 **첫 실측 예** (Fig. 3b: 같은 펠릿 · 같은 R 에 다이 밖 두께를 쓰면 σ 편향이 저압 −22 % · 고압 +6.5 %).  메모 수정은 하지 않는다.
8. **Stage-E (Tabor) 방향의 정성 근거** — 저압에서 형상 변화가 접촉을 개선하는 것이 σ 상승의 주인이라는 SEM + σ(ε) 증거 (Fig. 4b · 5).  정량 면적은 없다.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In situ thickness measurements in a spring-loaded cell (Miß et al., *ACS AMI* 2026) show that on release from 300 MPa to ~0.1 MPa inside the die a µc-Li₅.₅PS₄.₅Cl₁.₅ pellet recovers ~1.6 % of its thickness and a polycrystalline NMC622 pellet ~7.9 % (recomputed from their Table S2)."
- "Both single-phase pellets show two conductivity–porosity regimes: above ε ≈ 0.17–0.2 the conductivity is governed by interfacial contacts and lies up to ~4× below the Maxwell–Wagner–Bruggeman–Hanai (MWBH) prediction (digitized), below ε ≈ 0.17 it follows MWBH (σ₀ = 4.1 mS cm⁻¹ for the SE, 18.2 mS cm⁻¹ for NMC622)."
- 국문: *"단일상 펠릿의 다이 안 회복 (SE 1.6 % · 다결정 NMC 7.9 %, 300 MPa) 은 우리 실험–DEM 공극 차이의 일부만 설명할 크기다 (복합 전극 자료 없음 · 재료 다름)."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **Eq. 2 부호 ↔ Fig. 4a** (§3-3, §4-4): 인쇄 식대로면 가압 중 공극이 400 MPa 0.031 인데 그림 · 본문은 0.043 — 그림이 반대 부호로 계산됐다 (물리적으로는 그림이 맞다).  인용 시 **어느 규약인지 병기**.
2. **NMC 다이 안 회복 ↔ 다이 밖 모순**: 놓은 뒤 0.2831 mm [인쇄] > 다이 밖 0.2689 mm [판독] (−5 %).  저자 무언급.  저압 계면 저항 언급 (SI p.4) 과 함께 보면 110 kPa 에서 시료–피스톤 틈이 "회복" 에 섞였을 가능성 (추정).  ⇒ CAM 의 7.9 % 는 **위 끝 · 불확실**.
3. **Table S1 "지름 0.5 cm"** = 반지름이어야 재현 (§4-4) · 본문 "Table S1" 참조 = 실제 Table S2 · 70 MPa 행 "−0-000700" · 300 MPa 행 (0.588 · Δd) 미세 불일치.
4. **E = 67 GPa (DFT 인용)** — 우리 E_VRH 22.06 · 문헌 10–30 GPa 밖.  탄성 보정이 1/3 크기로 들어갔다.  치밀 펠릿 겉보기 E 는 더 낮을 수 있다 (`song2025_porous_argyrodite_modulus_fracture_toughness`: 13 % 다공 Li₆PS₅Cl 4.7 GPa — 다른 양).
5. **"물질 고유 σ 의 압력 의존 무시 가능" 은 이 자료로 입증되지 않는다** [우리 산술]: 300 → 400 MPa σ 판독 +1.0–1.3 % ↔ MWBH 공극 항 예상 +5.4 % → 남는 −4 % 는 Faka 활성화 부피 0.6–1.1 cm³/mol 이 주는 100 MPa 당 −2.4…−4.3 % (25 °C 가정 — 측정 온도 미기재) 와 **같은 크기** (판독 정밀도 ≈±1 %).  저자 근거는 "감소 징후가 없다" 뿐.
6. **반복 · 오차 없음** — 시료 1 개로 읽힘 · 불확도 = "기호 크기 이하" 한 문장 · SE 회복 (≈2 배 불확도) 은 약한 신호.
7. **단계 하중 · 반복 제거** (Fig. S3) — 단조 가압 · 단일 제거와 공극 · 회복이 다를 수 있다 (분리 실험 없음).
8. **ρ₀ (NMC622 4.48) 의 성격 미기재** (결정 / 입자 / 피크노미터) — CAM 공극 절대값이 ρ₀ 에 민감 (우리 AM 4.8 로 바꾸면 같은 두께에서 +4–6 %p, 우리 산술) → "조밀 충전보다 낮다 → 비가역 입자 변형" 논거의 크기가 이 값에 걸린다.  회복률 (두께 비) 은 ρ₀ 무관 — 우리 가설 (a) 산술은 영향 없음.
9. **MWBH σ₀ 는 적합값** (독립 무공극 측정 아님) · 적합 방법 미기재 · tau2 는 그 σ₀ 에 기댄다.
10. **PEEK 하우징의 반경 순응 · 벽 마찰 미논의** (Eq. 1 은 축 방향 피스톤만).  측정 온도 · 유지 시간 · 등가회로 · 입경 · 피스톤 교정값 [미확인].
11. (경미, 우리 산술) 250 MPa 를 연한 스프링으로 걸면 스프링당 ≈4.9 kN → 변위 ≈26–28 mm 로 Fig. S1a 교정 범위 (≈24.5 mm, 판독) 를 조금 넘는다 — 균등 분담 · ⌀10 mm 가정.
12. XRD 별표 (LiCl · γ-Li₃PS₄) 본문 무언급 — "successful synthesis" 의 순도 한정어.
13. **전이 한계**: Li₅.₅PS₄.₅Cl₁.₅ ≠ Li₆PS₅Cl · pc-NMC622 ≠ 우리 NCM (PC + SC) · 단일상 ≠ 복합체 · 약 0.3–0.8 mm 두꺼운 펠릿 ≠ 우리 ≈0.13–0.15 mm 전극 (벽 마찰 비 다름).

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 17 | Cronau, M.; Szabo, M.; König, C.; Wassermann, T. B.; Roling, B. *ACS Energy Lett.* **2021**, 6, 3072–3077 | 정본 카드 있음 — ex situ 두께 규약 · σ₀ 3.0 출처 |
| 18 | Ohno, S.; … Zeier, W. G. *ACS Energy Lett.* **2020**, 5 (3), 910–915 | 정본 카드 있음 — 실험실 간 σ 산포 |
| 19 | Larson, K.; … Albertus, P. *ACS Appl. Energy Mater.* **2025**, 8 (6), 3754–3763 (hot pressing argyrodite, > 2 mS/cm @20 °C · < 1 MPa) | 가압 의존을 없애는 길 (열간 가압) — 우리 SE 상태의 대조 |
| 20 | Wang, Y.; … Kozen, A. C. *ChemSusChem* **2024**, 17 (21), e202400718 (hot-pressed Li₆PS₅Cl, operating-pressure-invariant σ) | 우리 SE 와 같은 Li₆PS₅Cl 의 압력 불변 σ |
| 21 | Kalyk, F.; Pescara, L.; Drüschler, M.; Vargas-Barbosa, N. M. *Adv. Funct. Mater.* **2025**, 36, e09479 | 황화물 σ 측정 견고화 — σ₀ 규약 |
| 22 | Diallo, M. S.; … Ceder, G. *Nat. Commun.* **2024**, 15, 858 | SE 펠릿 밀도 ↔ 파괴 |
| 23 | Doux, J.-M.; … Meng, Y. S. *J. Mater. Chem. A* **2020**, 8, 5049–5055 (Pressure Effects on Sulfide Electrolytes) | ⚠ 정본 `doux2020_stack_pressure_assb` (Adv. Energy Mater.) 와 **다른 논문** — 미 digest |
| 25 | Hamann, T.; … Wachsman, E. *Adv. Funct. Mater.* **2020**, 30 (14), 1910362 (constriction factor · geometric tortuosity) | 우리 협착 · τ_geo 축 |
| 26 | Otani, K.; … Inoue, G. *J. Energy Storage* **2023**, 58, 106279 (composite σ reduction factors) | 복합 전극 σ 환원 인자 — 우리 망과 대조 |
| 29 | Miß, V.; Seus, S.; … Roling, B. *ACS Mater. Lett.* **2025**, 7 (6), 2262–2269 | CAM σ_e 의 압력 · 형상 · 코팅 · 열처리 — "놓을 때 σ_e 일정 (비가역)" 의 원 자료 |
| 30 | Faka, V.; … Zeier, W. G. *Energy Adv.* **2023**, 2, 1915–1925 | 활성화 부피 — §10-5 |
| 31 | Farr, R. S.; Groot, R. D. *J. Chem. Phys.* **2009**, 131 (24), 244104 | 다분산 구 충전 밀도 (그들의 "조밀 충전보다 낮다" 기준) |
| 32 | Chelidze, T. L.; Gueguen, Y. *Geophys. J. Int.* **1999**, 137 (1), 1–15 | MWBH 유도 |
| SI 1 · 5 · 6 · 7 | Adeli 2019 (정본 카드) · Hua 2020 *Chem. Mater.* 32, 4984 · Munsif 2023 *Phys. B* 661, 414932 · Liu 2024 *PRX Energy* 3, 013012 | ρ₀ · E 의 출처 — 특히 E 67 GPa (DFT) 재검토 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-09)
- 본문 7 쪽 · SI 7 쪽 전부 렌더 이미지로 정독 · `pdftotext -layout` 로 인용문 대조 · DOI `10.1021/acsami.6c03789` = 매 쪽 바닥 인쇄.
- Table S2 는 SI 텍스트 층에서 옮기고 `tab_S2.png` 와 칸마다 대조 (26 + 16 값) · Eq. 4 재계산이 300 MPa SE 한 칸 (0.15 %) 빼고 전부 인쇄값과 같다.
- r = 0.5 cm 판정 · Eq. 2 부호 판정 · 다이 밖 두께 판독 · σ 판독 · Heckel · tau2 = 전부 `tools/litdb/miss2026_digitize.py --check` 로 재현.
- 그림 크롭 13 장 = 캡션 13 개 (본문 Figure 1–6 · SI Figure S1–S5 · Table S1–S2; 본문에 표 없음) 와 번호 대조 · **5 장 손 재크롭** (fig_5 왼쪽 본문 글자 혼입 · fig_S1 · fig_S4 x 축 제목 잘림 · fig_S2 절 제목 "Results" 혼입 · fig_S5 아래 테두리 잘림 → 래스터 경계 + 2 pt) · `figures.json` 의 `recrop` · `auto_bbox`.
- 정본 litdb 전수 검색: 황화물 SE · NMC 펠릿의 **실측** 가압↔제거 두께 = 처음 (kaiser2018 "원문은 다루지 않는다" · Weitze 2024 · So 2022 = 시뮬레이션).

## 🔗 관련 카드
- 같은 그룹: `cronau2021_stack_pressure_ionic_conductivity` · `cronau2022_wet_milling_particle_size_ionic_conductivity` · `ohno2020_interlab_ionic_conductivity_argyrodite` · `hlushkou2018_void_space_ion_transport_assb_cathode` · `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` · `minnmann2021_jes_charge_transport_bottlenecks`.
- 재료 상수 출처: `adeli2019_halide_substitution_boosting_argyrodite` (ρ₀ · 격자상수) · 비교 E: `deng2016_elastic_superionic_electrolytes_dft` · `sakuda2013_sulfide_mechanical_property` · `song2025_porous_argyrodite_modulus_fracture_toughness` · `fan2026_sulfide_assb_stability_review_ECERD2600097`.
- 압밀 · 스프링백 축: `zunker2025_dem_large_deformation_compaction` · `hong2026_cbd_viscoelasticity_springback` · `zhang2026_xct_dem_cathode_calendering_peel_calibration` · `ngandjong2021_dem_calendering_digital_twin` · `schneider2023_particle_size_pressure_transport` (Heckel in die) · `doux2020_stack_pressure_assb`.
- CAM: `wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni` · `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` · `trevisanello2021_sc_pc_ncm_cracking_diffusion`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
