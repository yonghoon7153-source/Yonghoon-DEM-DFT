<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 이웃 = miss2026_insitu_conductivity_porosity_pressure_compaction.md · 주제 이웃 (양극 코팅) = bong2023_linbo3_thickness_uniformity_ncm523.md · lee2026_lpscl_coating_thickness_ncm811.md.
     쪽 표기 = 학술지 인쇄 쪽 "n of 9" (Adv. Funct. Mater. 2024, 34, 2315701 — 본문 PDF 쪽 = n).  SI 는 "SI p.n" (SI PDF 쪽 1–4).
     값 표지: [인쇄] = 본문 · SI · 그림 범례 · 그림 안 글자 · [판독] = 그림에서 읽은 값 (축 보정, 대략 — TREND 전용) ·
     [우리 산술] = 인쇄값으로 우리가 다시 계산한 값 · 이 논문 밖 우리 값과 엮은 계산 · [추정] = 논문이 말하지 않은 해석 · [미확인] = 본문 + SI 전수에 없음.
     원문 13 쪽 (본문 9 + SI 4) 전부 렌더 이미지로 읽고 pdftotext 로 인용문 대조.  그림 · 표 13 장 = 크롭 13 장 전부 열람. -->
# 단결정 Ni90 (SC-LiNi₀.₉Co₀.₀₅Mn₀.₀₅O₂) 에 **저온 고상 황 처리** (S 0.2 wt% · 150 °C N₂ 6 h) 로 10–20 nm 황화물 피막 — Li₆PS₅Cl / Li₄Ti₅O₁₂ 전고체 (55 °C) 에서 1C 500 사이클 86.9 % · 20C 43 mAh g⁻¹ · 고로딩 (CAM 63.67 mg cm⁻², 0.1C) **11.44 mAh cm⁻²** — Liu · Wang · Chen · Li · Wu (Adv. Funct. Mater. 2024)

> slug `liu2024_sc_ni90_sulfur_coating_sulfide_assb` · DOI `10.1002/adfm.202315701` · type `experiment (단결정 Ni-rich 양극 표면 황 코팅 · XRD/HRTEM/EDS · LTO 상대극 전고체 전기화학 55 °C · CV Randles–Sevcik · EIS — 시뮬레이션 없음)` · PDF `2._High_Capacity_Long_Life_Sulfide_All_Solid_State_Batteries_With_Single_Crystal_Ni_Rich_Layered_Oxide_Cathodes.pdf` · SI `2._Sup_High_Capacity_Long_Life_Sulfide_All_Solid_State_Batteries_With_Single_Crystal_Ni_Rich_Layered_Oxide_Cathodes.pdf` · digested `2026-10-13` · status ✅
>
> **저자**: **Huan Liu** · **Yue Wang** (공동 1저자 — 사사 *"H.L. and Y.W. contributed equally"*) · Liquan Chen · Hong Li · **Fan Wu\*** (Tianmu Lake Institute of Advanced Energy Storage Technologies · USTC Nano Science and Technology Institute · **중국과학원 물리연구소 (IOP CAS)** · UCAS · Yangtze River Delta Physics Research Center · CASOL Energy) · 교신 fwu@iphy.ac.cn · *Adv. Funct. Mater.* **2024**, 34 (26), 2315701 (본문 9 쪽 · **Editor's Choice** · SI 4 쪽) · 접수 2023-12-09 · 수정 2024-01-14 · 온라인 **2024-02-25** · © Wiley-VCH (OA 아님 — 쪽 바닥의 다운로드 표기 = 한양대 도서관 2026-09-29) · 연구비 장쑤성 · NSFC (U1964205 · 51972334) · 베이징 NSF · CAS 등 · 자료 = *"available from the corresponding author upon reasonable request"* [인쇄 p.8].
> **세미나 맥락**: 1저자 논문세미나 (2026-10) 두 편 중 하나 — 짝 카드 = [`kim2026_operando_neutron_thick_nmc811_interior_hotspot`](kim2026_operando_neutron_thick_nmc811_interior_hotspot.md) (후막 NMC811 operando 중성자).
> **정본 litdb 이웃 (링크만)**: 코팅 계열 [`bong2023_linbo3_thickness_uniformity_ncm523`](bong2023_linbo3_thickness_uniformity_ncm523.md) · [`lee2026_lpscl_coating_thickness_ncm811`](lee2026_lpscl_coating_thickness_ncm811.md) · [`kim2025_lto_pald_conformal_coating_nca`](kim2025_lto_pald_conformal_coating_nca.md) · SC/PC [`trevisanello2021_sc_pc_ncm_cracking_diffusion`](trevisanello2021_sc_pc_ncm_cracking_diffusion.md) · [`jung2023_single_crystal_ncm_morphology`](jung2023_single_crystal_ncm_morphology.md) · 공간전하층 [`haruyama2014_space_charge_layer_oxide_cathode_sulfide_se`](haruyama2014_space_charge_layer_oxide_cathode_sulfide_se.md) (= 이 논문 ref [39]).

---

## 0. 결론 먼저 — 우리 질문 (후막 바이모달 PC:SC NMC811–LPSCl · 접촉망 σ · SC vs PC) 에 대한 답

**한 문장**: 단결정 Ni90 분말에 황 분말을 섞어 150 °C 에서 구우면 표면에 **10–20 nm 황화물 층** (HRTEM) 이 생기고, 0.2 wt% S 가 최적 — LPSC/LTO 전고체 (55 °C) 에서 계면 저항 (EIS 반원) 이 가장 작고 (판독 ≈85 → ≈15 Ω, 3 번째 충전) 고율 · 장수명 · 고로딩 성능이 가장 좋다 (0.5 wt% 는 그 사이).
⇒ 우리에게 주는 것 = **"단결정 Ni-rich 양극에서도 계면 (전하이동) 저항이 율속을 지배하고, 수십 nm 피막 하나로 그 저항이 수 배 바뀐다"** 는 정성 증거 + **SE-rich (45 wt%) · 55 °C 조건의 초후막 (CAM 63.67 mg cm⁻²) 면용량 천장** 한 점.  주지 않는 것 = 단결정 ↔ 다결정 비교 (다결정 시료 **없음**) · 복합체 σ_ion/σ_e · 공극률 · 두께 · 피막 상 (phase) 동정 · 실온 성능.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 단결정 (SC) ↔ 다결정 (PC) | **SC 만** — PC 실험 없음 · 서론에서 SC 장점 (입계 없음 · 작은 표면적) 을 문헌으로 서술 | [인쇄] p.1–2 |
| ② SC 입경 | 본문 · SI 에 **수치 없음** · STEM 한 입자 ≈1–2 µm (1.0 µm 막대 기준) | [미확인] · Fig. 2e/n [판독] |
| ③ 코팅 무엇 · 얼마나 | SC-Ni90 + 황 분말 (손 갈기 0.5–1 h) → 150 °C · N₂ · 6 h → *"sulfide coating"* · 0.2 wt% S 에서 **10–20 nm** 층 · EDS 표면 S **0.34 mass%** (0.33 at%) · 상 (phase) 동정 없음 | [인쇄] p.2–3 · p.7 · SI Table S3 |
| ④ 계면 저항 | 1C 셀 EIS 반원 (판독, 셀 면적 0.785 cm²): 3 번째 충전 SC-Ni90 ≈85 · 0.2 %S ≈15 · 0.5 %S ≈90 Ω → 400 번째 ≈255 · ≈65 · ≈225 Ω | Fig. 4e–g [판독] |
| ⑤ 율속 (얇은 전극 3.18 mg cm⁻², 1C = 0.63 mA cm⁻²) | 2C: 109.5 / **137.2** / 126.8 · 10C: 51.2 / **71.3** / 57.7 mAh g⁻¹ (SC-Ni90 / 0.2 %S / 0.5 %S) · 20C ≈29 / ≈43 / ≈30 | [인쇄] p.3 · Fig. 3d [판독] |
| ⑥ 수명 (1C · 55 °C) | 초기 137.4 / **172.8** / 153.4 mAh g⁻¹ · 500 사이클 유지율 68.3 % / **86.9 %** / (≈71 %, 판독) | [인쇄] p.5 · Fig. 4d [판독] |
| ⑦ 초후막 | CAM **38.20 → 76.39 mg cm⁻²** (0.1C · 55 °C): 면용량 천장 = 63.67 mg cm⁻² 에서 9.46 / **11.44** / 10.58 mAh cm⁻² → 76.39 에서 오히려 감소 (≈9.07 / ≈11.23 / ≈10.43) | [인쇄] p.6 · Fig. 5d–f [판독] |
| ⑧ 복합체 조성 · 성형 | 양극 SC-Ni90 : LPSC : VGCF = **50 : 45 : 5** (손 갈기 1 h) · 음극 LTO : LPSC : VGCF = 50 : 40 : 10 · ⌀10 mm · SE 80 mg @ **250 MPa** → 양 · 음극 얹고 **1000 MPa · 2 min** | [인쇄] p.7–8 |
| ⑨ 복합체 σ_ion · σ_e · 공극 · 두께 | **없음** | [미확인] |

**우리 모델과 엮으면 (요약 — 상세 §7)**:
- 피막 두께 10–20 nm 는 우리 DEM (SE 지름 1 µm · 구) · MPM 복셀 (0.15–0.4 µm) 어느 쪽도 해상하지 못한다 — 이 효과는 접촉망 σ_ion · σ_e 가 아니라 **전하이동 (BV i0 · R_ct) 항**에 들어가야 한다 (우리 STEP4 축) [우리 해석].
- 이 논문의 "sulfide coating" 은 **고체전해질 (LPSCl) 선코팅이 아니다** — 황으로 만든 수십 nm 화학 피막 (보호막) 이다.  우리 이종기술 논지 (`docs/hetero_thesis.md` — NCM 에 설파이드 **SE** 선코팅 → 분산 → 3D 이온 경로 · *하지 않는 말: 계면 면적 · 보호막 효과*) 의 근거로 쓰면 안 된다 (세미나 질의에서 혼동 주의).
- 초후막 셀 (CAM 63.67 mg cm⁻²) 은 **SE 45 wt% = AM+SE 고체 부피의 ≈68 %** (우리 덱 밀도 4.8 · 2.0 g cm⁻³ 로 환산) · **55 °C** — 우리 ps45 는 같은 환산으로 SE **≈35 %** (18.4 wt% · AM 고체 64.7–64.9 % 와 일치) · 실온 기준이라 수송 영역이 다르다 [우리 산술].

---

## 1. 한 줄 요약
SC-Ni90 분말을 황 분말과 섞어 150 °C N₂ 에서 6 h 구워 (*"low-temperature solid-phase sulfur coating"*) 표면 황화물 층 (0.2 wt% S → 10–20 nm) 을 만들고, LPSC (자체 합성, 4.4 mS cm⁻¹) · LTO 음극 전고체 셀 (55 °C, 1.3–2.8 V vs LTO) 에서 0 / 0.2 / 0.5 wt% S 를 비교 → **0.2 wt% 가 율속 (20C) · 수명 (1C 500 사이클 86.9 %) · 계면 저항 · 초후막 면용량 (11.44 mAh cm⁻²) 모두 최고**, 0.5 wt% 는 *"thick coating layer hinders the transmission of Li ions"* 로 해석.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| H. Liu, Y. Wang (공동 1저자), L. Chen, H. Li, **F. Wu\*** (IOP CAS · Tianmu Lake 외) | Adv. Funct. Mater. 34 (2024) 2315701 · Editor's Choice | 10.1002/adfm.202315701 | **Li₆PS₅Cl (LPSC)** 자체 합성 (볼밀 50 h 300 rpm → 550 °C 10 h) · **SC-LiNi₀.₉Co₀.₀₅Mn₀.₀₅O₂** (출처 · 입경 [미확인]) + 황 0 / 0.2 / 0.5 wt% · 음극 **Li₄Ti₅O₁₂** · 도전재 VGCF | 실험 — 분말 표면 개질 + 전고체 전기화학 · **시뮬레이션 없음** |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 셀 상수
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 코팅 공정 | SC-Ni90 + 황 분말 → 상온에서 *"about half an hour to one hour"* 갈기 → 알루미나 도가니 · 관상로 **150 °C · N₂ · 6 h** → 식혀 갈기 · S 0.2 · 0.5 wt% | [인쇄] p.7 |
| LPSC 합성 | LiCl (>99 %) · P₂S₅ (99 %) · Li₂S (>99 %) 화학량 → 지르코니아 **볼밀 50 h · 300 rpm** → 펠릿 · 유리관 봉입 → **550 °C · 10 h** | [인쇄] p.7 |
| LPSC 이온전도도 | 80 mg 펠릿 (전극 없이) 14.5 Ω · 두께 **0.05 cm** · 면적 **0.785 cm²** → **4.4 mS cm⁻¹** (RT) · 재계산 0.05/(14.5 × 0.785) = 4.39 ✓ | [인쇄] p.7 · SI Fig. S3 · [우리 산술] |
| ⚠ 그 펠릿의 밀도 | 80 mg / (0.785 × 0.05 cm³) = **2.04 g cm⁻³** > Li₆PS₅Cl 결정밀도 **1.860** (정본 `miss2026_insitu_conductivity_porosity_pressure_compaction` 카드 §3-1 · `adeli2019_halide_substitution_boosting_argyrodite` 격자상수) → 두께 0.05 cm 는 반올림값 (80 mg 이면 ≥0.0548 cm) · 그 두께면 σ ≥ 4.8 mS cm⁻¹ | [우리 산술] |
| 양극 복합체 | **SC-Ni90(-S) : LPSC : VGCF = 50 : 45 : 5** (wt) · 갈기 1 h | [인쇄] p.7 |
| 음극 복합체 | **LTO : LPSC : VGCF = 50 : 40 : 10** · 갈기 1 h | [인쇄] p.7 |
| 셀 성형 | 몰드 ⌀**10 mm** · LPSC 80 mg @ **250 MPa** → 양극 5 mg + 음극 10 mg 양면 → **1000 MPa · 2 min** · 운전 중 스택 압력 [미확인] | [인쇄] p.7–8 |
| 표준 셀 로딩 | 양극 5 mg × 50 % / 0.785 cm² = **3.18 mg_CAM cm⁻²** → 1C = 200 mA g⁻¹ × 3.18 mg = **0.637 mA cm⁻²** (그림 표기 *"1C=0.63 mA cm⁻²"*, *"0.3C=0.19 mA cm⁻²"* 와 일치) · 20C = 12.7 mA cm⁻² | [우리 산술] · Fig. 3d/f [인쇄] |
| 초후막 셀 로딩 | **38.20 · 50.93 · 63.67 (63.66) · 76.39 mg cm⁻²** = 양극 복합체 **60 · 80 · 100 · 120 mg** × 50 % / 0.785 cm² 와 소수 둘째 자리까지 같다 → **같은 50 : 45 : 5 복합체 · 같은 ⌀10 mm 다이** 로 읽힌다 (조성 서술 없음) · Li-In 셀 6.37 mg cm⁻² = 10 mg | [인쇄] Fig. 5 · S4 · [우리 산술] |
| 초후막 양극 두께 | **[미확인]** · 50 : 45 : 5 · 100 mg 이면 AM 63.66 + SE 57.3 mg cm⁻² → 고체만 (VGCF · 공극 제외) **≥0.42 mm** (우리 DEM 덱 밀도 AM 4.8 · SE 2.0 g cm⁻³ — 논문 밖 값) | [우리 산술] |
| 시험 조건 | 정전류 **55 °C** · 1.3–2.8 V (vs LTO) · 명목 비용량 **200 mAh g⁻¹** (1C 정의) · LAND CT-2001A · CV 0.05–0.4 mV s⁻¹ (CHI660E) · EIS (Zennium Pro) = 2.8 V 충전 뒤 **8 MHz–100 mHz** · CV · EIS 온도 [미확인] | [인쇄] p.8 |
| 측정 기기 | XRD XD2 (Beijing Purkinje, Cu 1.54 Å, 36 kV · 20 mA, 4°/min) · TEM JEM-F200 *"acceleration voltage of 800 kV"* (⚠ 기종 이름은 200 kV 급으로 읽힘 — 오기 의심 [추정]) | [인쇄] p.7 |

### 3-2. 구조 · 표면 (Fig. 1 · Fig. 2 · SI Table S1–S3 · Fig. S1–S2)
- XRD: 세 시료 모두 α-NaFeO₂ 층상 R-3m (JCPDS 70-4314) · (003) 이 황 양이 늘수록 낮은 각도로 이동 (판독 ≈18.63° → ≈18.55° → ≈18.52°) → *"diffusion of a small amount of sulfur to the surface lattice during sintering"* · S²⁻ 1.70 Å vs O²⁻ 1.26 Å [인쇄 p.2 · Fig. 1d 판독].
- SI Table S1 [인쇄 SI p.2]:

| 시료 | a (Å) | c (Å) | Vol. (Å³, 인쇄) | c/a (인쇄) | 재계산 √3/2·a²c (Å³) | c/a 재계산 |
|---|---|---|---|---|---|---|
| SC-Ni90 | 2.88 | 14.28 | 410.67 | 4.96 | **102.58** | 4.958 |
| SC-Ni90-0.2%S | "3̄2.88" (⚠ 인쇄 오기) | 14.34 | 412.82 | 4.97 | 103.01 | 4.979 |
| SC-Ni90-0.5%S | 2.88 | 14.36 | 413.10 | 4.98 | 103.15 | 4.986 |

  - ⚠ 인쇄 "Vol." 은 표준 육방 격자 부피 (√3/2)a²c 의 **정확히 4.00 배** → 계산식 오류로 보인다 [우리 산술].  상대 변화 (+0.52 % · +0.59 %) 는 c 증가 (14.28 → 14.34 → 14.36) 에서 온다 · a 는 세 시료 같은 2.88.
- HRTEM: SC-Ni90 표면 격자 0.235 nm = (012) (Fig. 2b–d · SI Fig. S1: 10 간격 2.3499 nm) · SC-Ni90-0.2%S 표면에 **10–20 nm 두께 황화물 층** (*"obviously different structure from the bulk crystalline region"*) · 안쪽 0.204 nm = (104) (Fig. 2k–m · SI Fig. S2: 10 간격 2.0395 nm) [인쇄 p.2–3].
- EDS (SI Table S2–S3, mass% / atom%) [인쇄 SI p.2]:
  - SC-Ni90: Ni 62.72 / 34.82 · Co 3.74 / 2.04 · Mn 3.59 / 2.13 · O 29.94 / 60.98.
  - SC-Ni90-0.2%S: Ni 58.59 / 30.53 · Co 3.47 / 1.80 · Mn 3.35 / 1.86 · O 34.25 / 65.48 · **S 0.34 / 0.33**.
  - Ni / (Ni+Co+Mn) 원자비 = 0.893 (두 시료 같음 · 명목 0.90) [우리 산술] · 저자 판정 *"S distributed uniformly on the surface"* (Fig. 2s).
- 입자 크기: STEM 상 한 입자씩 ≈1–2 µm (Fig. 2e · 2n 의 1.0 µm 막대) [판독] — 분포 · SEM [미확인].

### 3-3. 율속 (Fig. 3 · p.3–4 · 3.18 mg cm⁻² · 55 °C)
| C-rate (사이클) | SC-Ni90 | SC-Ni90-0.2%S | SC-Ni90-0.5%S | 표지 |
|---|---|---|---|---|
| 0.1C | ≈200 | ≈204 | ≈203 | [판독] Fig. 3a–c |
| 1C | ≈133 | ≈160 | ≈152 | [판독] |
| **2C (23rd)** | **109.5** | **137.2** | **126.8** | [인쇄] p.3 |
| 5C | ≈77 | ≈100 | ≈88 | [판독] |
| **10C (33rd)** | **51.2** | **71.3** | **57.7** | [인쇄] p.3 |
| 20C | ≈29 | ≈43 | ≈30 | [판독] Fig. 3d |

- 율속 순서 0.2 %S > 0.5 %S > SC-Ni90 [인쇄 p.4] · *"The disparity … is not pronounced … at 0.1 C"* [인쇄 p.3].
- CV 0.05 mV s⁻¹ (Fig. 3e): H1-M 산화 봉우리 0.2 %S **2.12 V** · 0.5 %S ≈2.18 · SC-Ni90 ≈2.23 V (vs LTO) · M-H2 2.46 / 2.48 · H2-H3 2.66 · 환원 2.14 · 2.42 · 2.57 V [인쇄 숫자 + 색 대응 판독].
- 0.3C (0.19 mA cm⁻²) 100 사이클 (Fig. 3f): 활성화 2 사이클 뒤 ≈170 / ≈187 / ≈183 [인쇄 p.4] → 100 사이클 ≈125 / ≈150 / ≈138 [판독].

### 3-4. 수명 · EIS (Fig. 4 · p.4–5)
- 1C (0.63 mA cm⁻², 55 °C, 0.1C 활성화 2 사이클 뒤): 초기 **137.4 / 172.8 / 153.4** mAh g⁻¹ → 500 사이클 유지율 **68.3 % / 86.9 %** / 0.5 %S 인쇄 없음 (Fig. 4d 판독 ≈153.6 → ≈109 = **≈71 %**) [인쇄 p.5 · 판독 + 우리 산술].  초록 *"87 % capacity retention"* = 86.9 % 의 반올림.
- ⚠ Fig. 4c (0.5 %S) 의 3 번째 사이클 방전 ≈138 · 500 번째 ≈100 mAh g⁻¹ [판독] ↔ Fig. 4d · 본문 153.4 → ≈109 — **같은 시료 두 패널이 ≈15 mAh g⁻¹ 어긋난다** (4a · 4b 는 4d 와 맞음).
- EIS (3 · 200 · 400 번째 충전 뒤, 셀 전체 — 반원 지름 판독, Ω):

| 시료 | 3rd | 200th | 400th |
|---|---|---|---|
| SC-Ni90 | ≈85 | ≈130 | ≈255 |
| SC-Ni90-0.2%S | **≈15** | ≈30 | ≈65 |
| SC-Ni90-0.5%S | ≈90 | ≈105 | ≈225 |

  - 저자 귀속: 반원 = *"charge transfer resistance, primarily stemming from the interfacial resistance between SC-Ni90 cathodes and sulfide SE"* [인쇄 p.5] · 등가회로 맞춤 수치 [미확인] · 면적 환산 (×0.785 cm²) 하면 3rd ≈67 / ≈12 / ≈71 Ω·cm² [우리 산술 · 셀 전체 (LTO 쪽 포함)].
  - 0.5 %S 가 3 번째부터 SC-Ni90 과 비슷 (≈90 Ω) — 저자 해석 *"substantial thickness of the coating layer on SC-Ni90-0.5%S hinders the efficient transmission of Li ions"* (0.5 %S 피막 두께는 **측정 안 함** [미확인]).

### 3-5. 초후막 (Fig. 5 · p.5–6 · 0.1C · 55 °C)
| CAM 로딩 (mg cm⁻²) | 38.20 | 50.93 | 63.67 | 76.39 |
|---|---|---|---|---|
| SC-Ni90 면용량 (mAh cm⁻²) | ≈6.85 | ≈8.6 | **9.46** | ≈9.07 |
| SC-Ni90-0.2%S | ≈8.2 | ≈10.33 | **11.44** | ≈11.23 |
| SC-Ni90-0.5%S | ≈8.0 | ≈9.33 | **10.58** (63.66) | ≈10.43 |
| 0.2%S 비용량 (Fig. 5b) | ≈215 | ≈203 | ≈180 | ≈147 |
| 0.1C 전류밀도 (우리 산술) | 0.76 | 1.02 | **1.27** | 1.53 mA cm⁻² |

- 굵은 값 = [인쇄] p.6 · 나머지 = [판독] (Fig. 5a–f) · 전류밀도 = 0.1 × 200 mA g⁻¹ × 로딩 [우리 산술].
- 본문: 63.67 mg cm⁻² 에서 *"average discharge capacity of 172.8 mAh g⁻¹, compared with 165.7 and 148.4"* [인쇄 p.6] — ⚠ 자기 면용량으로 나누면 11.44/63.67 = **179.7** (0.2 %S) · 10.58/63.67 = 166.2 · 9.46/63.67 = 148.6 → **0.2 %S 만 7 mAh g⁻¹ 어긋나고, 172.8 은 1C 초기값 (Fig. 4d) 과 같은 숫자** — 옮겨 적기 오류로 보인다 [우리 산술 · 추정].  Fig. 5h 의 0.2 %S 10 사이클 ≈180 mAh g⁻¹ [판독] 도 179.7 쪽.
- 첫 사이클 쿨롱효율 (Fig. 5g–i, 판독): ≈75 % / ≈80 % / ≈77 %.
- **면용량 천장**: 세 시료 모두 63.67 → 76.39 mg cm⁻² 에서 면용량이 줄었다 (0.1C · 55 °C 에서도) — 로딩 20 % 증가에 비용량 ≈18 % 감소 (0.2 %S) [판독 + 우리 산술] · 원인 분석 없음.

### 3-6. CV 속도 의존 · Randles–Ševčík (Fig. 6 · p.6–7)
- 식 (1): **i_p = 0.4463 nFAC (nFvD / RT)^½** (렌더 대조) · 기호 정의 [인쇄 p.6] · ⚠ 본문은 *"Figure 4d shows the linear relationship between peak current (i_p) and … v^1/2"* — 실제는 **Fig. 6d** (그림 번호 오기).
- Fig. 6d (판독, 충전 쪽): i_p vs v^½ 기울기 ≈0.043 (SC-Ni90) · ≈0.088 (0.2 %S) · ≈0.068 A/(V s⁻¹)^½ (0.5 %S) → 기울기 비 0.2 %S/SC-Ni90 ≈2.0 → 겉보기 D 비 ≈4 (D ∝ 기울기²) [판독 + 우리 산술].
- **D 절대값은 보고 안 됨** — A (전극 면적 — 복합 전극에서는 실제 반응 면적과 다름) · C (농도) 값이 없어 논문 자료로 계산 불가 [미확인].

### 3-7. SI Fig. S4 — Li-In 음극 셀
- SC-Ni90-0.2%S / LPSC / **Li-In** · **6.37 mg cm⁻²** · 1C · 55 °C · 100 사이클: 0.1C 활성화 ≈204 · ≈209 → 1C ≈153 → ≈164 (6–10 사이클) → 100 사이클 ≈155 mAh g⁻¹ · 첫 쿨롱효율 ≈78 % · 셋째 ≈89 % 뒤 ≈100 % [판독].  1C = 1.27 mA cm⁻² [우리 산술].  본문은 이 그림을 인용하지 않는다.

---

## 4. ★ 방법 — 실험 사슬 · 입자 처리

### 4-1. 코팅 · 합성 (p.7)
- 고상 황 코팅 = **SC-Ni90 + S 분말 혼합 (막자 갈기) → 150 °C N₂ 6 h**.  저자 주장: ALD 보다 싸고 공업적 (*"economically applicable"*) [p.1].
- 생성 피막의 화학 (금속 황화물 · Li₂S · 황산염 등) 은 XPS · Raman · 회절로 **동정하지 않았다** — "sulfide coating layer" 는 HRTEM 대비 + EDS S 신호 + (003) 이동으로 추론 [인쇄 p.2–3 · 동정 [미확인]].

### 4-2. 셀 · 측정 (p.7–8)
- 펠릿 적층 셀 (⌀10 mm) · 건조 아르곤 글러브박스 · SE 250 MPa → 전극 1000 MPa 2 min · LTO 음극 (VGCF 10 wt%) · 55 °C.
- 율속: 0.1 → 20C 각 5 사이클 (3, 8, 13, …, 38 번째를 곡선으로) · 수명: 0.1C 2 사이클 활성화 → 1C 500 사이클 / 0.3C 100 사이클 · 초후막: 0.1C 10 사이클 · CV: 0.05–0.4 mV s⁻¹ · EIS: 2.8 V 충전 뒤 8 MHz–100 mHz.

### 4-3. 입자 처리 ★ · 시뮬레이션 · frame[5]
- **시뮬레이션 없음.**  실제 입자: SC-Ni90 = 각진 단결정 ≈1–2 µm (STEM, 판독) · 표면 10–20 nm 황화물 층 (0.2 wt%) · LPSC = 자체 합성 (입경 [미확인]) · VGCF 5 wt%.
- frame[5]: 이 논문은 **입자 표면 (nm) 의 전기화학**을 다룬다 — 우리 DEM (접촉망 수송) · MPM (형상 · 공극) 둘 다 **그 아래 축척**.  가진 것 = 계면 저항 · 율속 · 수명의 상대 비교.  없는 것 = 미세구조 · 접촉망 · σ_ion/σ_e · 기계.

### 4-4. 기법 미니 용어집
- **SC / PC** — 단결정 (입계 없는 µm 급 1 차입자) / 다결정 (sub-µm 1 차입자가 뭉친 2 차입자).
- **고상 (solid-phase) 코팅** — 용매 없이 분말끼리 섞어 열처리로 표면 피막을 만드는 방법 (여기: 황 + 양극 150 °C).
- **공간전하층 (SCL)** — 산화물 양극과 황화물 SE 의 Li 화학퍼텐셜 차로 계면 SE 쪽에 Li 결핍층이 생긴다는 그림 (ref [39] Haruyama 2014 — 정본 카드 있음).
- **H1-M · M-H2 · H2-H3** — Ni-rich 층상 산화물의 충전 중 상전이 (육방 1 → 단사 → 육방 2 → 육방 3) · H2-H3 가 큰 c 축 수축과 연결된다고 흔히 서술 (이 논문은 이름만).
- **Randles–Ševčík** — 확산 지배 CV 봉우리 전류가 v^½ 에 비례 → 기울기로 겉보기 확산계수 · 복합 전극에서는 면적 · 농도 정의가 모호해 **상대 비교용**.
- **LTO (Li₄Ti₅O₁₂)** — 부피 변화 작은 음극 · 전압 기준이 Li 가 아니라 LTO (그래서 1.3–2.8 V).
- **명목 비용량 200 mAh g⁻¹** — 이 논문의 1C 정의 기준.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | XRD (a) 전 범위 (b) (006)/(012) (c) (108)/(110) (d) (003) — 황 양 ↑ → (003) 저각 이동 | 피막 형성 간접 증거 · ⚠ (b)(c) 의 이중선 분리는 확대 그림에서도 약하다 (*"clear splitting"* 은 후한 표현, 판독) |
| 2 | (a–d) SC-Ni90 TEM · HRTEM 0.235 nm (012) · FFT (e–i) STEM + EDS (Ni · Co · Mn · O) (j–m) 0.2 %S TEM · 표면층 (노란 점선) · 0.204 nm (104) · FFT (n–s) STEM + EDS (S 포함) | ★ 10–20 nm 피막의 유일한 직접 상 · SC 입자 ≈1–2 µm (판독) — 우리 SC 4 µm 대비 |
| 3 | (a–c) 0.1–20C 충방전 곡선 (d) 율속 (1C = 0.63 mA cm⁻², 55 °C) (e) CV 0.05 mV s⁻¹ (상전이 봉우리) (f) 0.3C 100 사이클 | ★ 피막이 고율에서 차이를 키운다 (0.1C 에선 거의 같음) — 계면 율속의 정성 증거 |
| 4 | (a–c) 1C 사이클별 곡선 (d) 1C 500 사이클 (e–g) EIS 3 · 200 · 400 번째 | ★ 계면 저항 (반원) 의 크기 · 성장 — 0.2 %S 가 ≈1/5 · ⚠ 4c ↔ 4d 어긋남 |
| 5 | (a–c) 로딩별 0.1C 곡선 (38.20–76.39 mg cm⁻²) (d–f) 면용량 vs 로딩 (천장 63.67) (g–i) 63.67 mg cm⁻² 10 사이클 | ★★ **초후막 면용량 천장** (55 °C · SE 45 wt% · 0.1C) — 후막 수송 서사의 외부 한 점 |
| 6 | (a–c) CV 속도 0.05–0.4 mV s⁻¹ (d) i_p vs v^½ (충전 · 방전) | 겉보기 확산 상대 비교 (기울기 비 ≈2 → D 비 ≈4, 판독) · D 절대값 없음 |
| Table S1 | 격자상수 a · c · Vol. · c/a | (003) 이동의 수치 · ⚠ Vol. 4 배 계산 오류 · "3̄2.88" 오기 |
| Table S2 · S3 | EDS 원소비 (SC-Ni90 · 0.2 %S) — S 0.34 mass% | 표면 S 양 |
| S1 · S2 | HRTEM 선 단면 (10 간격 2.3499 · 2.0395 nm) | 격자 간격 근거 · S2 캡션 "2m" (실제 격자상 2l) |
| S3 | LPSC 펠릿 Nyquist (14.5 Ω · 0.05 cm · 0.785 cm² · 4.4 mS cm⁻¹) | SE σ₀ 한 점 (⚠ 밀도 > 결정밀도 — §3-1) |
| S4 | 0.2 %S / LPSC / Li-In · 6.37 mg cm⁻² · 1C · 55 °C 100 사이클 | Li-In 상대극 대조 한 점 |

## 6. Post-processing ★
- **무엇을**: XRD 격자상수 (Table S1) · HRTEM FFT/선 단면 (Digital Micrograph) · EDS 원소비 · 정전류 곡선에서 비용량 · 유지율 · 면용량 · CV 봉우리 위치 · Randles–Ševčík 기울기 (Fig. 6d) · EIS 반원 크기 (정성 — 맞춤 회로 · 값 없음).
- **도구**: Digital Micrograph (FFT) · 나머지 [미확인].
- **안 한 것**: 피막 상 동정 (XPS · Raman) · 0.5 %S 피막 두께 · 등가회로 맞춤 · D 절대값 · 반복 셀 · 오차막대 · 실온 시험 · 복합체 σ_ion/σ_e · 후막 단면 (두께 · 공극) · PC 대조.
- **우리 후처리 (이 카드)**: 로딩 ↔ 복합체 질량 역산 · 전류밀도 · Table S1 부피 재계산 · 0.2 %S 평균 비용량 모순 · SE 펠릿 밀도 모순 · Fig. 3–6 판독.

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (우리 수치는 정본 브랜치 밖 `docs/` 출처를 병기)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| CAM | **SC**-Ni90 단독 (≈1–2 µm, 판독) · 0 / 0.2 / 0.5 wt% S 피막 | ps45 = **PC 9 µm + SC 4 µm** (지름) 바이모달 5 조성 · 피막 없음 (`docs/symmetric_cell_ionic_plan_20261013.md` §1) | SC 크기 2–4 배 다름 · PC 대조 없음 → 우리 PC:SC 경향에 쓸 숫자 없음 |
| 양극 조성 | AM : LPSC : VGCF = **50 : 45 : 5** | ps45 NCM : LPSCl = **81.6 : 18.4** · 탄소 없음 | AM+SE 고체 부피 중 SE: 그들 **≈68 %** (다수) ↔ 우리 **≈35 %** (소수 — ps45 README 의 AM 고체 64.7–64.9 % 와 일치) [우리 산술 · 덱 밀도 4.8 · 2.0] |
| 성형압 | 250 MPa (SE) → **1000 MPa · 2 min** (전극) | DEM 300 MPa | 3 배 이상 높은 성형압 |
| 온도 | **55 °C** (정전류 전부) | 우리 σ₀ 보고 기준 1.5 mS cm⁻¹ (실온 문헌 펠릿 범위) | 55 °C 는 SE σ · 동역학을 함께 올린다 — 절대 율속 비교 금지 |
| 후막 | CAM 63.67 mg cm⁻² → **11.44 mAh cm⁻²** (0.1C = 1.27 mA cm⁻²) · 76.39 에서 감소 · 두께 [미확인] (고체만 ≥0.42 mm, 우리 산술) | ps45 **6 mAh cm⁻² · ≈111 µm** | 그들 = 우리의 ≈2 배 면용량 · ≈4 배 두께 급 (조건부 산술) |
| σ_ion · σ_e · tortuosity | **없음** | ps45 Hertz σ_ion 0.0587–0.0893 mS cm⁻¹ · 수송 tortuosity 5.03–7.24 · σ_e (기준 4.1 · PC 인자 끔) 0.375–0.467 (`docs/data/ps45_r45_network_g2_20261007/README.md`) | 비교 불가 — 조성 · 온도 · 측정 없음 |
| 계면 저항 | 피막으로 반원 ≈85 → ≈15 Ω (판독) | DEM 망 = 접촉 협착 (Holm) 만 · 전하이동 (BV i0 · R_ct) 은 STEP4 축 · 우리 SC/PC 앵커 노트: *"R_ct uncoated … → LNO-coated … 코팅이 ~20× 지배"* (Kim 2025 EA, `docs/ncm_sc_poly_electrochem_anchors.md` §3) | 같은 방향 (코팅 → R_ct 수 배 감소) · 우리 i0 SC/PC 분리값은 *"ASSB 문헌에 부재"* (같은 노트) — 이 논문도 분리값을 주지 않는다 |

### 7-2. ★ SC vs PC — 이 논문이 **못** 주는 것과 주는 것
- **못 주는 것**: SC ↔ PC 직접 비교 · SC 의 D_s 절대값 · SC 의 σ_e.  우리 σ_e 모델의 PC 크기 인자 (1/(1 + (r/2 µm)^1.5), *"측정 아님"* · `docs/data/ps45_r45_network_g2_20261007/README.md` σ_e 절) 를 지지하거나 반박할 자료가 없다.
- **주는 것 (정성)**: 단결정 Ni-rich 에서 고율 (2–20C) 차이를 만든 것은 **입자 결정성 (모두 SC) 이 아니라 표면 피막**이었다 — 즉 같은 SC 라도 계면 상태가 율속을 수 배 바꾼다.  우리 내부 앵커 노트의 *"i0 의 SC/PC 분리 정량값은 ASSB 문헌에 부재 · 코팅 (LNO) 지배가 결정계 (SC/PC) 보다 커서 분리 근거로 부적합"* (`docs/ncm_sc_poly_electrochem_anchors.md` §3) 과 같은 방향의 사례 하나 [우리 해석].
- 우리 랩 실측 (같은 노트 §1, Jung 2023): ASSB 에서 5C 유지율 **SC 74.0 % vs PC 41.6 %** — 이 논문 (SC 만) 은 그 대조를 대신하지 못한다.

### 7-3. ★ 후막 수송 — 짝 논문 (Kim 2026) 과 나란히 (조건 다름 — 정성)
| | Kim 2026 (짝 카드) | 이 논문 |
|---|---|---|
| SE 함량 | 16 wt% (+ VGCF 3 · PTFE 1) | **45 wt%** (+ VGCF 5) |
| 온도 | [미확인] | **55 °C** |
| 음극 | Si (N/P ≈1.1) | LTO |
| 면용량 · 전류 | ≈4.6 mAh cm⁻² @ 0.5 mA cm⁻² → ≈2.8 @ 1.0 (충전, 판독) | **11.44 mAh cm⁻² @ 1.27 mA cm⁻²** (0.1C) · 76.39 mg cm⁻² (1.53 mA cm⁻²) 에서 감소 시작 |
| 두께 | ≈150 µm | [미확인] (고체만 ≥0.42 mm, 조건부 산술) |
- 읽기 [추정]: 같은 1 mA cm⁻² 급 전류에서 이 논문의 훨씬 두꺼운 전극이 버틴 것은 **SE 부피 (고체의 ≈68 % — Kim 조성 16 wt% 는 같은 환산으로 소수) + 55 °C** 의 몫으로 보인다 — 후막의 율속 한계가 SE 망 (σ_ion,eff) 에 걸린다는 우리 서사와 같은 방향.  단 둘 다 그 σ 를 재지 않았고, 음극 · 셀 구성 · 온도가 모두 달라 **분리된 증거가 아니다**.
- 우리 ps45 (SE 18.4 wt%) 는 SE 함량으로는 Kim 쪽에 가깝다 → 실온 6 mAh 급에서 C/5 근처부터 이온 경로 제한이 보일 것으로 예상하는 쪽 [추정 — Kim 카드 §7-3 의 R_ion 어림 124–189 Ω·cm²].

### 7-4. 이종기술 논지와의 관계 — **혼동 주의**
- 논지 (`docs/hetero_thesis.md` 비준 블록): *"건식 후막 바이모달 복합양극에서 NCM에 설파이드 SE를 선코팅하면(같은 SE 총량) … 분산이 좋아지고 … 3D 이온전도 패스웨이"* · **하지 않는 말: 계면 면적 · 보호막 효과**.
- 이 논문의 "sulfide coating" = **황 원소로 만든 10–20 nm 화학 피막** (보호막 · 공간전하층 완화 · 계면 반응 억제) — SE (LPSCl) 입자 선코팅이 아니고, 효과 주장도 정확히 논지가 **하지 않겠다고 한** 보호막 쪽이다.
- ⇒ 세미나 · 보고에서 이 논문을 *"설파이드 코팅이 좋다"* 는 근거로 이종기술에 붙이면 **논지가 흔들린다** — 같은 낱말 (sulfide coating) · 다른 대상.  쓸 수 있는 것은 *"계면 화학 피막은 별개 축 (전하이동) 이고, 우리 논지의 축 (분산 → SE 망) 과 분리해 다뤄야 한다"* 는 대비뿐 [우리 해석].

### 7-5. frame[5]
- **가진 것**: nm 표면 개질 → 셀 성능 (율속 · 수명 · 계면 저항 · 면용량 천장) — 실험.
- **없는 것**: 전극 미세구조 · 접촉망 · σ_ion/σ_e · 기계 (DEM · MPM 의 영역 전부) · 피막 상 동정.
- 우리 모델에서 이 효과가 들어갈 자리 = **STEP4 i0 / R_ct** (BV) — 접촉망 σ 가 아니다.

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **STEP4 i0 감도 범위의 외부 한 점** — 같은 SC 양극에서 피막만으로 계면 반원이 ≈5–6 배 (판독, 셀 전체) 달라졌다 → STEP4 의 i0 (또는 R_ct) 스윕 폭을 최소 반 자릿수 이상으로 잡을 근거 (우리 앵커 노트의 LNO ~20 배와 같은 방향) [우리 해석].
2. **후막 면용량 천장의 표적** — SE 45 wt% · 55 °C · 0.1C 에서도 CAM ≈64 mg cm⁻² 근처에 천장 (11.44 mAh cm⁻²).  우리 모델에서 SE 함량 축 (대칭셀 계획 §5 의 "둘째 축") 을 열 때, "SE 다수 조성은 두께 천장이 훨씬 뒤로 밀린다" 를 정성 검증 표적으로 쓸 수 있다 [추정].
3. **세미나 질의 대비** — "SC 가 PC 보다 좋다" 를 이 논문으로 말하지 않는다 (PC 시료 없음).  "sulfide coating" ≠ SE 선코팅 (§7-4).
4. **SE σ₀ 측정 관행의 반면교사** — 펠릿 두께 0.05 cm (반올림) 로 계산한 σ 는 결정밀도를 넘는 밀도가 된다 → 우리 대칭셀 계획 (`docs/symmetric_cell_ionic_plan_20261013.md` §4) 의 *"가압 중 두께와 놓은 뒤 두께 → 공극률"* 기록 요구가 필요한 이유의 사례.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "A solid-state sulfurization of single-crystal LiNi₀.₉Co₀.₀₅Mn₀.₀₅O₂ (0.2 wt% S, 150 °C, N₂) forms a 10–20 nm sulfide surface layer; in Li₆PS₅Cl/Li₄Ti₅O₁₂ cells at 55 °C it raises the 1C capacity retention after 500 cycles from 68.3 % to 86.9 % and the 10C capacity from 51.2 to 71.3 mAh g⁻¹ (Liu et al., *Adv. Funct. Mater.* 2024)."
- "At 0.1C and 55 °C, cathodes with 50:45:5 CAM:Li₆PS₅Cl:VGCF reach 11.44 mAh cm⁻² at 63.67 mg_CAM cm⁻², and the areal capacity decreases again at 76.39 mg cm⁻²."
- 국문: *"단결정 Ni90 에서도 율속 차이를 만든 것은 결정성이 아니라 10–20 nm 표면 피막이었다 (계면 반원 ≈1/5, 55 °C · LTO 상대극 · 얇은 전극)."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **"Single-crystal" 은 변수가 아니다** — 모든 시료가 SC · PC 대조 없음 · 입경 분포 · SEM 없음 (TEM 한 입자씩).  제목의 SC 는 배경이지 시험된 인자가 아니다.
2. **피막의 정체 미동정** — "sulfide coating layer" 는 HRTEM 대비 · EDS S · (003) 이동으로 추론 · XPS/Raman 없음 · 0.5 %S 피막 두께 미측정 → *"thick coating hinders Li transport"* 는 가설.
3. **숫자 모순 둘**: (i) 63.67 mg cm⁻² 의 0.2 %S *"average 172.8 mAh g⁻¹"* ↔ 자기 면용량 11.44 → **179.7** (나머지 두 시료는 맞는다 — 172.8 은 1C 초기값과 같은 숫자) (ii) Fig. 4c (0.5 %S ≈138 → ≈100) ↔ Fig. 4d · 본문 (153.4 → ≈109).
4. **SI Table S1 "Vol." = 표준 (√3/2)a²c 의 4.00 배** · 0.2 %S 의 a "3̄2.88" 오기 · c/a 끝자리 반올림 대신 절삭.
5. **SE 펠릿 밀도 > 결정밀도** (2.04 vs 1.860 g cm⁻³) — 두께 0.05 cm 가 반올림 · σ 4.4 mS cm⁻¹ 의 두께 불확도 ≥10 % [우리 산술].
6. **그림 번호 · 캡션 오기**: 본문 *"Figure 4d shows … i_p … v^1/2"* → Fig. 6d · SI Fig. S2 캡션 "figure 2m" → 격자상은 2l · TEM *"800 kV"* (JEM-F200) [추정 오기].
7. **55 °C · LTO 상대극 · 얇은 전극 (3.18 mg cm⁻²)** — "20C" · "500 사이클" 은 얇은 전극 (1C = 0.63 mA cm⁻²) 결과이고 "11.44 mAh cm⁻²" 는 0.1C 초후막 결과 — **같은 셀이 둘 다 한 것이 아니다**.  실온 · Li 금속/흑연/Si 음극 성능 [미확인].  Li 기준 전압 창 [미확인].
8. **D 는 상대값뿐** — Randles–Ševčík 기울기 비 (판독 ≈2 → D 비 ≈4) · A · C 미기재 · 복합 전극의 면적 정의 모호.
9. **EIS 정량 없음** — 등가회로 · 맞춤값 없음 · 셀 전체 (LTO 쪽 포함) 반원 · 판독값만.
10. **반복 · 오차막대 없음** — 조건마다 셀 1 개로 읽힘.
11. **XRD "clear splitting"** — 확대 그림 (Fig. 1b, c) 에서 (006)/(012) · (108)/(110) 이중선은 약하고 넓다 (판독).
12. **초후막 셀 조성 · 두께 · 공극 미기재** — 50 : 45 : 5 · ⌀10 mm 는 로딩 숫자에서 역산한 추론 [우리 산술].
13. **전이 한계 (우리 쪽)**: SC 입경 ≈1–2 µm (우리 4 µm) · SE 45 wt% (우리 18.4) · 1000 MPa (우리 300) · 55 °C · 피막 = nm 화학층 (우리 모델 축척 밖).

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 24 | S. Culver, R. Koerver, W. Zeier, J. Janek, Adv. Energy Mater. 2019, 9, 1900626 | 황화물 ASSB 양극 계면 총설 |
| 26 | S. Wang, W. Zhang, X. Chen, D. Das, R. Ruess, A. Gautam, F. Walther, S. Ohno, R. Koerver, Q. Zhang, W. Zeier, F. Richter, C. Nan, J. Janek, Adv. Energy Mater. 2021, 11, 2100654 | 계면 안정화 (Janek 그룹) |
| 27 | D. Kitsche, Y. Tang, Y. Ma, D. Goonetilleke, J. Sann, F. Walther, M. Bianchini, J. Janek, T. Brezesinski, ACS Appl. Energy Mater. 2021, 4, 7338 | ALD 코팅 (이 논문이 대비한 비싼 방법) |
| 30 | S. Kim, H. Cha, R. Kostecki, G. Chen, ACS Energy Lett 2023, 8, 521 | SC NCM 장점 근거 |
| 39 | J. Haruyama, K. Sodeyama, L. Han, K. Takada, Y. Tateyama, Chem. Mater. 2014, 26, 4248 | 공간전하층 — 정본 카드 있음 (`haruyama2014_space_charge_layer_oxide_cathode_sulfide_se`) |
| 40 | K. Takada, N. Ohta, L. Zhang, K. Fukuda, I. Sakaguchi, R. Ma, M. Osada, T. Sasaki, Solid State Ion. 2008, 179, 1333 | 산화물 완충층 원전 |
| 41 | R. Koerver, I. Aygün, T. Leichtweiß, C. Dietrich, W. Zhang, J. Binder, P. Hartmann, W. Zeier, J. Janek, Chem. Mater. 2017, 29, 5574 | Ni-rich/황화물 계면 분해 · 용량 손실 |
| 42 | J. Wang, Z. Zhang, J. Han, X. Wang, L. Chen, H. Li, F. Wu, Nano Energy 2022, 100, 107528 | 같은 그룹 — H1-M 상전이 개선 근거 |
| 3 · 4 | W. Yan, … F. Wu, Nat. Energy 2023, 8, 800 · P. Lu, … F. Wu, Nat. Commun. 2023, 14, 4077 | 같은 그룹 황화물 전고체 (셀 기술 배경) |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 9 쪽 · SI 4 쪽 전부 렌더 (100–110 dpi 전 쪽 · 그림 300 dpi) 로 정독 · `pdftotext` 로 인용문 대조 · 식 (1) 은 렌더 (200 dpi) 로 기호 대조 · DOI · 권호 = 본문 1 쪽 + 쪽 바닥.
- 크롭 13 장 = 캡션 13 개 (본문 Figure 1–6 · SI Table S1–S3 · SI Figure S1–S4) 와 번호 대조 · 그림은 임베드 래스터 bbox 그대로 · SI 표는 제목 줄 포함 · S3/S4 래스터가 캡션 윗줄과 겹친 몇 pt 는 렌더로 여백임을 확인 · `figures.json` 캡션의 합자 (ﬁ · ﬀ) 를 풀어 검색되게 함.
- SI Table S2 · S3 가 같은 그림 객체 (표 틀) 를 공유하는 것을 보고 렌더로 대조 — 숫자는 서로 다르다 (복붙 아님).
- 로딩 4 값 = 복합체 60 · 80 · 100 · 120 mg × 0.5 / 0.7854 cm² · Table S1 부피 4.00 배 · 0.2 %S 비용량 179.7 · SE 펠릿 2.04 g cm⁻³ — 전부 재계산.
- 정본 litdb 전수 검색 (papers/ 파일 목록 + DOI · 제목 · 저자 · "Ni90" · "sulfur coating" grep): 같은 논문 카드 없음.

## 🔗 관련 카드
- 양극 코팅: `bong2023_linbo3_thickness_uniformity_ncm523` · `wei2023_linbo3_coating_cutoff_voltage_lco_argyrodite` · `lee2026_lpscl_coating_thickness_ncm811` · `kim2025_lto_pald_conformal_coating_nca` · `lu2024_lowtemp_assb_li2zro3_interface` (LPSCl/Ni90 계면) · `nolan2021_garnet_cathode_coating`.
- SC/PC: `trevisanello2021_sc_pc_ncm_cracking_diffusion` · `jung2023_single_crystal_ncm_morphology` · `sharma2023_nmc_single_crystal_anisotropic_nanoindentation`.
- 계면 이론: `haruyama2014_space_charge_layer_oxide_cathode_sulfide_se` (ref [39]).
- 세미나 짝: `kim2026_operando_neutron_thick_nmc811_interior_hotspot`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
