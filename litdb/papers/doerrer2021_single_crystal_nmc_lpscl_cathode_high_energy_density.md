<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 2026-11-10) 에서 꼭 뽑으라고 한 항목.
     본 = kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact.md (같은 종류 = NCM + Li₆PS₅Cl 복합 양극 실험 — 절 번호 체계를 그대로 따랐다) ·
     절 꼴 참고 = var2026_sulfide_se_mechanical_properties_local_indentation_pellet.md · papakyriakou2021_….md (같은 날 카드).
     쪽 표기 = 본문 "p.N" (PDF N 쪽 · 인쇄 쪽 = 37808 + N, 예 p.2 = 37810) · SI "SI p.N" (SI PDF N 쪽 = 인쇄 S-N).
     값 표지: [인쇄] = 본문 · SI · 그림 안에 숫자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 397 행 —
     두 PDF 의 그림이 전부 벡터라 표지 · 곡선의 경로 좌표를 눈금 선에 보정해 읽었다 · 픽셀 판독 없음) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) ·
     [가정] = 원문에 없는 성분 밀도 등을 카드가 넣은 값 · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [정본 카드] = 다른 정본 카드가 원문 확인한 값 ·
     [미확인] = 원문 (본문 7 쪽 + SI 14 쪽 전수) 에 없음.  원문 21 쪽은 글자 층 + 렌더 이미지로 전부 읽었다.
     이 논문에 DEM · MPM · 입자 모델은 없다 — 계산은 셀 벽 마찰을 보는 탄성 FEM (Inventor) 한 장뿐이다. -->
# 단결정 NMC83 (LiNbO₃ 코팅 · D50 3.4 µm) + 자체 밀링 Li₆PS₅Cl (1–5 µm) + Super C65 = 70 : 27.5 : 2.5 wt% 복합 양극을 500 MPa · 상온에서 분리막 분말과 한 번에 눌러 상대밀도 ≈ 0.90 (porosity ≈ 10 %) · 입자 파쇄 없음 — 같은 공정의 다결정 NMC 는 50 / 250 / 500 MPa 에 상대밀도 78 / 82 / 86 % 이고 250 MPa 이상에서 입자가 깨진다 · 순수 LPSCl 분말 25 → 500 MPa 에 0.54 → 0.89–0.90 (판독) · 0.2 MPa 양극 적층압에서 205 mAh g⁻¹ · 8.7 mAh cm⁻² — Doerrer · Capone · Narayanan · Liu · Grovenor · Pasta · Grant (ACS Appl. Mater. Interfaces 2021)

> slug `doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density` · DOI `10.1021/acsami.1c07952` · type `exp (cold-pressed composite cathode 500 MPa RT · SEM cross-section relative density · single-crystal vs polycrystalline NMC particle fracture vs pressing pressure · LPSCl powder pellets EIS impedance vs stack pressure + relative density · galvanostatic cycling at 0.2–50 MPa stack pressure · asymmetric spring cell + elastic FEM (Inventor) of mold-wall friction — no DEM / MPM / particle model)` · PDF `40e3bbdb-16._High_Energy_Density_Single-Crystal_NMCLi6PS5Cl_Cathodes_for_All-Solid-State_Lithium-Metal_Batteries.pdf` · SI `fc7571d7-16._Sup_High_Energy_Density_Single-Crystal_NMCLi6PS5Cl_Cathodes_for_All-Solid-State_Lithium-Metal_Batteries.pdf` · digested `2026-11-10` · 보강 `2026-11-12` (§13 = N-28 · Tron 2023 참고 [13] 인용 대조) · status ✅
>
> **저자**: **Christopher Doerrer\*** · Isaac Capone · Sudarshan Narayanan · Junliang Liu · Chris R. M. Grovenor · Mauro Pasta · **Patrick S. Grant\*** (\* 교신 — 둘 다 Department of Materials, University of Oxford · Grovenor · Pasta · Grant 은 Faraday Institution 겸) · *ACS Appl. Mater. Interfaces* **13** (2021) **37809–37815** · 접수 2021-04-29 · 승인 2021-07-19 · 출판 2021-07-29 · "© 2021 The Authors. Published by American Chemical Society" (첫 쪽 CC 표지) · 연구비 = Faraday Institution SOLBAT (FIRG007) · LG Energy Solution · Nissan · Henry Royce Institute (EP/R010145/1) · 이해 상충 없음 · 기여: C.D. 전 과정 · I.C. DLS · 단면 식각 · S.N. XPS · J.L. · C.R.M.G. EBSD (p.6).
> **이웃 카드 (링크만)**: [`kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact`](kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact.md) (같은 계 · SE 1–5 µm · 계산 기공) · [`minnmann2021_jes_charge_transport_bottlenecks`](minnmann2021_jes_charge_transport_bottlenecks.md) (NCM622 + LPSCl 380 MPa 복합 기공 7.6–17 %) · [`jung2023_single_crystal_ncm_morphology`](jung2023_single_crystal_ncm_morphology.md) (SC ↔ PC 형태) · 본문 ref 18 = [`shi2019_high_am_loading_particle_size_assb`](shi2019_high_am_loading_particle_size_assb.md) (입경비) · ref 28 = [`doux2020_stack_pressure_assb`](doux2020_stack_pressure_assb.md) · ref 30 = [`bielefeld2020_effective_ionic_conductivity_binder`](bielefeld2020_effective_ionic_conductivity_binder.md) · ref 17 = [`kim2021_review_oxide_sulfide_se_interfaces`](kim2021_review_oxide_sulfide_se_interfaces.md) · 순수 LPSCl 압밀 = [`var2026_sulfide_se_mechanical_properties_local_indentation_pellet`](var2026_sulfide_se_mechanical_properties_local_indentation_pellet.md) §7-2 표.
> **판독 원자료**: `litdb/figures/doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density/digitized.csv` (397 행 — Fig. 1b · 1e · 3a · 4a · 4b · 4c · 5b · 5c · 5d · SI Fig. S5 · S8b · S9a · S9c · S10 · S12a · S12b).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 상용 단결정 LiNi₀.₈₃Mn₀.₀₆Co₀.₁₁O₂ (결정 1–2 µm · DLS D50 3.4 µm · LiNbO₃ 습식 코팅) 70 wt% + 직접 볼밀링한 Li₆PS₅Cl "SP" (1–5 µm) 27.5 wt% + Super C65 2.5 wt% 를 유성 볼밀 (140 rpm · 30 min) 로 섞어 상용 Li₆PS₅Cl "LP" (1–20 µm) 분리막 분말과 함께 **PEEK 몰드 · WC 다이에서 500 MPa · 상온** 으로 한 번 누르면, 셀 조립 뒤 단면 SEM 에서 **단결정 입자 파쇄가 없고 상대밀도 ≈ 90 %** 다 (p.2).
같은 공정의 다결정 NMC (D50 5.9 µm) 는 **50 / 250 / 500 MPa 에 "estimated relative densities" 78 / 82 / 86 %** (SI Fig. S6 캡션) 이고 250 MPa 이상에서 입자가 결정립 · 응집 경계로 깨진다.  그 셀이 0.2 MPa (양극) / 2.5 MPa (음극) 적층압에서 205 mAh g⁻¹ (8.7 mAh cm⁻²) 을 낸다.  **압력별 · 조성별 밀도 표는 없다.  모델 (DEM · MPM · 입자) 도 없다.**

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 조성 (wt% · vol%) | **NMC (LiNbO₃ 코팅) 70 · LPSCl-SP 27.5 · Super C65 2.5 wt%** (SI p.2 · SI Table S4) · 바인더 **없음** · vol% **[미확인]** (원문에 없음) → 카드 계산 ≈ **45 : 51 : 4 vol%** (LPSCl 1.64 랩 표준) / 48 : 48 : 4 (LPSCl 1.86) — NMC 밀도 4.78 g/cm³ = SI Table S1 격자로 계산 · C65 2.0 [가정] | [인쇄] SI p.2 · p.12 · [카드 산술] §3-1 |
| ② ★ 활물질 · SE 입도 | 단결정 NMC: 결정 **1–2 µm** (SEM) · DLS **D50 = 3.4 µm** (응집 · EBSD "moderately agglomerated") · 판독 분포 0.51–13.2 µm · 최빈 ≈ 3.9 µm · 다결정 NMC811 대조: **D50 = 5.9 µm** (2차 입자) · SE: **LPSCl-SP 1–5 µm** (자체 볼밀링 · 양극용) · **LPSCl-LP 1–20 µm** (상용 · 분리막용) | [인쇄] p.2 · [판독] Fig. 1b |
| ③ ★ 가압 조건 | **500 MPa · 상온 · 한 단계** (분리막 LP 25 mg (비대칭 셀 50 mg) 위에 양극 혼합물 4 mg (고적재 12 mg) 을 쌓아 함께) · PEEK 몰드 + WC 다이 · 셀 지름 5 mm (단면 19.63 mm²) · **유지 시간 · 가압 속도 [미확인]** · 다결정 대조만 50 / 250 / 500 MPa | [인쇄] p.2 · SI p.2 · SI Table S3 · S4 |
| ④ ★ 압력별 / 조성별 밀도 · 기공 표 | **표 없음.**  있는 것: 단결정 복합 500 MPa ≈ 90 % (한 점) · 다결정 복합 50 / 250 / 500 MPa = 78 / 82 / 86 % ("estimated" · 그림 캡션 안 세 점) · 순수 LPSCl 분말 (아래 ⑥) · 조성 축 없음 (70 wt% 하나) | [인쇄] p.2–3 · SI p.7 · SI p.12 |
| ⑤ ★ 밀도를 어떻게 쟀나 · 분모 | **원문에 없다 [미확인]** — 단결정 90 % 는 *"The SEM cross-section image in Figure 2b shows … an overall relative density of ∼90%"* 문장 안 (단면 SEM 에서 읽은 값으로 보인다 [카드 해석]) · 다결정은 *"estimated relative densities"* · 질량 · 두께 · 이론밀도 · 성분 밀도 미기재 · 상태 = **500 MPa 를 뺀 뒤 · 셀 조립 후 · 사이클 전 · Ar 이온 연마 단면** (Fig. 2 캡션) = 하중 뺀 뒤 · 다이 밖 | [인쇄] p.2 · Fig. 2 · SI Fig. S6 |
| ⑥ ★ 순수 SE 값 | LPSCl 분말 펠릿 (EIS · 스테인리스 차단 전극 두 장 · 적층압별): 상대밀도 **SP 0.54 / 0.86 / 0.87 / 0.89 · LP 0.57 / 0.86 / 0.88 / 0.90 @ 25 / 250 / 375 / ≈500 MPa** [판독] · σ **SP 0.46 → 1.46 · LP 0.36 → 3.10 mS/cm @ 25 → ≈490 MPa** [판독] (본문 *"reaching 1.2 and 3 mS cm−1"* — SP 의 1.2 는 판독 ≈300 MPa 값) · > 500 MPa 에서 임피던스 상승 (SI Fig. S5 · 본문: LPSCl 입자 균열) · 분모 · 측정 상태 [미확인] | [판독] Fig. 1e · S5 · [인쇄] p.2 |
| ⑦ ★ 구조 숫자 (기공 · 두께 · 면적 용량 · 굴곡도) | 적재 14 mg cm⁻² (NMC) = 3 mAh cm⁻² · 고적재 42.42 mg cm⁻² = **8.7 mAh cm⁻² · 두께 ≈ 200 µm** · 양극 상대밀도 0.9 (SI Table S4) · 분리막 1.5 mm (실험) · 굴곡도 · 유효 σ_ion **없음** | [인쇄] p.3 · p.5 · SI Table S4 |
| ⑧ ★ 입자 파괴 (SC ↔ PC) | 가압: SC **파쇄 없음** (500 MPa) ↔ PC **500 · 250 MPa 에서 1차 입자 파쇄 · 50 MPa 에서만 2차 입자 온전** · 충전 뒤: SC 비응집 입자 파쇄 없음 · 계면 접촉 손실 + 응집 결정 분리 ↔ PC 접촉 손실 + 입계 균열 | [인쇄] p.2 · p.4 · SI Fig. S6 · S9b |
| ⑨ ★ DEM 한계 · 소성 | DEM · 입자 모델 **말 없음**.  닿는 문장 = 정성 기전 (p.3): 단단한 NMC 가 움직이며 무른 LPSCl 에 전단을 전하고, **NMC 끼리 닿으면 상대 운동이 막혀 더는 전단이 안 되고 다결정 응집체가 깨지기 시작한다** — 계산 · 값 없음 | [인쇄] p.3 · SI Fig. S7 |
| ⑩ 2D / 3D · 탈압 | 실험 = 3D 실물 · FEM = 펠릿 하나의 탄성 응력 (Inventor · 바깥면 고정 가정) · 2D → 3D 말 없음 · **탈압 회복 · 가압 중 밀도 측정 없음** (밀도는 하중 뺀 뒤 한 상태) | [인쇄] SI p.3 · SI Fig. S13 |
| ⑪ 절대값 전이 | **같은 재료계 (NMC 층상 산화물 + Li₆PS₅Cl) 라 조건을 붙여 견줄 수 있다** — 단 NMC83 · LiNbO₃ 코팅 · C65 2.5 wt% · **500 MPa · 하중 뺀 뒤 단면 추정 · 분모 미기재**.  우리 계획에서 이 값은 맞추는 값이 아니라 **결과 전에 견줄 외부 값 후보** (§7-3) | §7 |

⛔ **한정어 (떼지 말 것)**: ① 상대밀도 ≈ 90 % · 78 / 82 / 86 % 는 **측정법 · 분모 미기재** (앞은 단면 SEM 문장 안의 값 · 뒤는 "estimated") ② **하중 뺀 뒤 · 다이 밖 단면** 상태 — 가압 중 값이 아니다 ③ 단결정 복합은 **500 MPa 한 점** · 압력 축은 다결정 세 점뿐 ④ 압밀은 **분리막 분말과 함께** 한 번 (분리막이 하중 경로의 일부) ⑤ 유지 시간 · 가압 속도 · 반복 시료 수 [미확인] ⑥ vol% 는 카드 계산 (원문에 없음) ⑦ 순수 SE 밀도 · σ 는 그림 판독 · 분모 미기재 · 본문 σ 값 (SP 1.2) 과 그림 끝점 (≈1.46) 이 다르다 ⑧ 다결정 대조는 NMC811 (NMC83 아님 · *"chemically similar"*).

---

## 1. 한 줄 요약
리튬 금속 음극에 맞춰 양극 용량을 키우려면 층상 NMC 와 황화물 SE 의 복합 양극이 필요한데, 다결정 NMC 는 압밀 · 사이클 중 깨지고 계면이 떨어진다.  저자는 (i) **작은 단결정 NMC83** (결정 1–2 µm) 을 고르고 (ii) SE 를 그 크기에 맞게 **직접 볼밀링한 1–5 µm LPSCl** 로 쓰고 (iii) LiNbO₃ 로 코팅하고 (iv) 볼밀 혼합 뒤 **500 MPa 상온 한 번 압밀** 해 단결정은 깨지지 않고 상대밀도 ≈ 90 % 인 양극을 만든다 (다결정은 250 MPa 이상에서 깨지고, 깨지지 않는 50 MPa 에서는 기공이 22 % 로 크다).
그 양극은 첫 사이클 쿨롱 효율 ≈ 85 % · 204–205 mAh g⁻¹ (2.5 · 10 MPa) · 10 MPa 에서 ≈ 210 mAh g⁻¹ 을 내고, 금형 벽 마찰을 이용한 **비대칭 적층압 (음극 2.5 / 양극 0.2 MPa)** 에서도 거의 같은 용량을 낸다 — 고적재 8.7 mAh cm⁻² (≈ 200 µm) 셀이 205 mAh g⁻¹ · 첫 효율 87 % 이고 분리막 20 µm 를 가정한 추정 에너지 밀도는 405 Wh kg⁻¹ · 1069 Wh L⁻¹ 다.  충전 시 격자 부피 −5.5 % (XRD) 로 단결정도 계면 접촉이 일부 떨어지지만 비응집 단결정은 깨지지 않는다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (AM / SE / 도전재) | 연구유형 |
|---|---|---|---|---|
| C. Doerrer\* · I. Capone · S. Narayanan · J. Liu · C. R. M. Grovenor · M. Pasta · P. S. Grant\* (Univ. Oxford · Faraday Institution) | *ACS Appl. Mater. Interfaces* 13 (2021) 37809–37815 · Research Article · 키워드 *solid-state battery, sulfide electrolyte, composite cathode, single-crystal NMC, interfacial contact, volume expansion, stack pressure, pressure dependence* | 10.1021/acsami.1c07952 | **SC LiNi₀.₈₃Mn₀.₀₆Co₀.₁₁O₂** (상용 · 공급사 [미확인]) · 대조 **PC LiNi₀.₈Mn₀.₁Co₀.₁O₂** / **Li₆PS₅Cl** SP (자체 밀링) · LP (상용 · 공급사 [미확인]) / **Super C65** 2.5 wt% · 바인더 없음 · 음극 Li 금속 (≈30 µm) 또는 LTO/LPSCl/CNF | 실험 — 분말 · 압밀 · 단면 SEM/EDX/EBSD · XRD · XPS · EIS · 정전류 · 적층압 · 탄성 FEM (벽 마찰) |

- **1저자 메모와의 대조**: 저자 (Doerrer 외 6) · 제목 *"High Energy Density Single-Crystal NMC/Li6PS5Cl Cathodes for All-Solid-State Lithium-Metal Batteries"* · ACS Appl. Mater. Interfaces 13 (2021) 37809–37815 · DOI 10.1021/acsami.1c07952 — PDF 1 쪽 · 머리글과 **모두 같다** (다른 점 없음).  덧붙임: SI 표지 제목은 하이픈 없이 *"High Energy Density Single Crystal NMC/Li6PS5Cl Cathodes for All-Solid-State Lithium Metal Batteries"* (SI p.1) · 교신 = Doerrer · Grant.
- 글의 꼴: 1. Introduction → 2. Results and Discussion (번호 없는 문단들) → 3. Conclusions — 짧은 논문 (본문 그림 5 + TOC 그림 · 표 0 · 식 0 · 참고문헌 32) · SI = Experimental/Methods (SI p.2–4) + 그림 S1–S13 + 표 S1–S4 + 참고문헌 S1.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 재료 · 조성 · 혼합 (p.2 · SI p.2 · SI Table S1–S2 · S4)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 단결정 NMC | LiNi₀.₈₃Mn₀.₀₆Co₀.₁₁O₂ · 상용 (*"Commercially available SC-NMC powders of small crystal size (1−2 μm)"*) · EDX Ni / Co / Mn = 82.8 / 11.3 / 5.9 % (명목 83 / 11 / 6) · Rietveld R-3m: a 2.8727 Å · c 14.1958 Å (pristine) | [인쇄] p.2 · SI Table S1 · S2 |
| 입도 | DLS (Horiba LA-960 · 탈이온수 분산 · 초음파 1 min) **D50 = 3.4 µm** · EBSD: *"moderately agglomerated particles"* · [판독] 분포 첫 점 0.51 µm (0.16 vol%) → 최빈 ≈ 3.9 µm (8.4 vol%) → 마지막 점 13.2 µm (0.66 vol%) · 그린 점들의 누적 절반 = 2.98–3.41 µm 사이 (D50 3.4 와 맞음) | [인쇄] p.2 · SI p.2 · [판독] Fig. 1b |
| 다결정 대조 | LiNi₀.₈Mn₀.₁Co₀.₁O₂ (*"chemically similar … with PC-NMC morphology, using an identical processing methodology"*) · EBSD 2차 입자 응집 · **D50 = 5.9 µm** | [인쇄] p.2 · SI Fig. S3b |
| NMC 결정 밀도 | **[미확인]** (원문에 없음) → SI Table S1 격자 (a 2.8727 · c 14.1958 Å · Z = 3 · M = 97.43 g/mol) 로 **4.78 g/cm³** [카드 산술 V = (√3/2)a²c = 101.45 Å³] | [카드 산술] |
| LiNbO₃ 코팅 | 습식: NMC 1 g + lithium niobium ethoxide 용액 (Alfa Aesar · 5 % w/v in ethanol) 400 µL + 무수 에탄올 800 µL 1 h 교반 → 진공 50 °C 건조 → 대기 350 °C (10 °C/min · 30 min) · EDX Nb 지도 + XPS 깊이 분석 = Nb 많은 표면 산화물 · 두께 [미확인] | [인쇄] SI p.2 · SI Fig. S4 |
| LPSCl-SP (양극용) | Li₂S · P₂S₅ · LiCl 화학량론 혼합 → 40 mL 그릇 · ZrO₂ 볼 16 × 10 mm · Fritsch P7 **600 rpm 14 h** (열처리 언급 없음 [카드 해석 — 기계화학 합성뿐]) · 입도 **1–5 µm** (SEM) · XRD 에 미반응 Li₂S 흔적 (본문: SP 의 σ 가 낮은 이유로 추정) | [인쇄] p.2 · SI p.2 · Fig. 1c · 1f |
| LPSCl-LP (분리막용) | 상용 (*"for the SSE separator and for convenience, we used commercial LPSCl"*) · **1–20 µm** · 공급사 [미확인] | [인쇄] p.2 · Fig. 1d |
| 도전재 · 바인더 | **Super C65 2.5 wt%** (*"used in all the cathodes"*) · 바인더 **없음** (원문에 바인더 성분이 없다) | [인쇄] p.2 · SI p.2 |
| 혼합 | **70 wt% LiNbO₃ 코팅 NMC + 27.5 wt% LPSCl-SP + 2.5 wt% Super C65** · 유성 볼밀 (Fritsch P7) **140 rpm · 30 min** · 볼 · 그릇 조건 [미확인] · Ar 글러브박스 (O₂ · H₂O < 1 ppm) | [인쇄] SI p.2 |
| 음극 (LTO 셀) | LTO 60 · LPSCl 35 · 탄소 나노섬유 5 wt% (같은 혼합) · 15 mg · LTO 부피 변화 0.2 % (본문이 ref 14 로 인용) | [인쇄] SI p.2 · p.4 |

**vol% (원문 없음 → 카드 계산, 고체 기준)**: 비부피 = 0.7/4.78 + 0.275/ρ_LPSCl + 0.025/2.0 [C65 2.0 가정] →
· ρ_LPSCl **1.64** (랩 표준): NMC **44.8** · LPSCl **51.3** · C **3.8 vol%** · 이론밀도 **3.06 g/cm³** [카드 산술]
· ρ_LPSCl **1.86** (결정학 계열, 다른 정본 카드의 값): NMC 47.7 · LPSCl 48.2 · C 4.1 vol% · 이론밀도 3.26 g/cm³ [카드 산술]
⚠ 원문은 이론밀도 · 성분 밀도를 적지 않았다 — 위 vol% 는 비교용이고 원문 값이 아니다.

### 3-2. ★ 복합 양극 압밀 · 상대밀도 (p.2–3 · SI p.2 · SI Fig. S6 · SI Table S4)
- **공정 (원문 문장)**: *"Active material, LPSCl-SP, and carbon black were mixed in a ball mill and subsequently pressed in a polymer mold at 500 MPa and RT with LPSCl-LP to form a pellet."* (p.2) · SI: *"Stacked layers of 25 mg (50 mg for cells cycled at asymmetric pressure) of LPSCl-LP and then 4 mg (12 mg for the cell with a high loading in Figure 5c) of the composite cathode mixture were pressed in a PEEK mold using a WC die set at 500 MPa."* (SI p.2) — 분리막 분말 위에 양극 혼합물을 쌓아 **한 번** 누른다 (따로 미리 누른다는 말 없음 [카드 해석]).  유지 시간 · 속도 · 하중 제거 방식 [미확인].
- **지름 5 mm** (SI Table S4 · Fig. S8b) · 단면 19.63 mm² (SI Table S3) → 4 mg 혼합물 = 20.4 mg cm⁻² (NMC 14.3 mg cm⁻² ≈ 본문 "14 mg cm−2") · 12 mg = 61.1 mg cm⁻² (NMC 42.8 ↔ Table S4 42.42 mg cm⁻²) [카드 산술 질량 ÷ 0.19635 cm²].
- **단결정 복합 · 500 MPa**: *"The SEM cross-section image in Figure 2b shows that the composite cathode exhibited no signs of the SC-NMC particle fracture despite the high loads used during mixing and pressing. Moreover, there was continuous, intimate contact at the SC-NMC/LPSCl interfaces and an overall relative density of ∼90%."* (p.2) → 기공 ≈ 10 % [카드 산술 1 − d] · SI Table S4 고적재 양극 *"Relative density 0.9"* (그 표 = *"All values were those used/obtained experimentally except the separator thickness"*).
  · **측정 상태 [카드 해석]**: Fig. 2b 캡션 *"cross-section of a SC-NMC/LPSCl composite cathode after cell assembly and before cycling"* · SI: 단면은 Ar 이온 연마 (PECS II) · 진공 이송 → **500 MPa 를 뺀 뒤 · 셀에서 꺼낸 시료** (하중 아래 값이 아니다).  측정법 (영상 분할 · 질량–두께) · 분모 · 반복 수 [미확인].
- **다결정 복합 · 압력 세 점**: SI Fig. S6 캡션 *"PC-NMC/LPSCl cathodes densified at different fabrication pressures. Particle fracture is indicated by the white arrows. Fabrication pressures and estimated relative densities were: (a) 50 MPa, 78% (b) 250 MPa, 82% (c) 500 MPa, 86%."* → 기공 22 / 18 / 14 % [카드 산술] · 본문: *"these lower pressures significantly increased porosity (from ∼14 to ∼22%, Figure S6)"* (p.3) — 같은 수.

| 시료 | 압력 (MPa) | 상대밀도 [인쇄] | 기공 1 − d [카드 산술] | 입자 상태 [인쇄] | 근거 |
|---|---|---|---|---|---|
| SC-NMC/LPSCl-SP/C65 70 : 27.5 : 2.5 | 500 | **≈ 0.90** (Table S4 0.9) | ≈ 10 % | 파쇄 없음 · 계면 연속 | p.2 · Fig. 2b · SI Table S4 |
| PC-NMC/LPSCl-SP (같은 공정) | 50 | **0.78** | 22 % | 2차 입자 온전 | SI Fig. S6a · p.2 |
| 〃 | 250 | **0.82** | 18 % | 파쇄 지속 | SI Fig. S6b · p.2 |
| 〃 | 500 | **0.86** | 14 % | 1차 입자 파쇄 (결정립 · 응집 경계) | SI Fig. S6c · p.2 |

- **같은 압력 500 MPa 에서 SC 0.90 ↔ PC 0.86** — 단결정이 4 %p 더 치밀하다 (두 값 다 측정법 미기재 · 반복 없음 → 차이의 오차 [미확인]).
- **두께 대조 [카드 산술 · 가정 밀도]**: 고적재 양극 60.6 mg cm⁻² (42.42 / 0.7) ÷ 상대밀도 0.9 ÷ 이론밀도 → **220 µm** (분모 3.06 · LPSCl 1.64) · **207 µm** (3.26 · LPSCl 1.86) ↔ 본문 *"thickness ∼200 μm"* (p.5) — 같은 자릿수 (분모를 가르지 못한다).  14 mg cm⁻² 양극은 74 / 69 µm [카드 산술 · 원문에 두께 없음].
- **분리막 두께 대조 [카드 산술]**: LP 50 mg ÷ 0.19635 cm² = 255 mg cm⁻² → 상대밀도 0.9 (SI Table S4 분리막 값) 이면 **1.73 mm (분모 1.64) · 1.52 mm (1.86)** ↔ 원문 *"1.5 mm in the actual experiment"* (SI Table S4 캡션, 고적재 셀 = 비대칭 50 mg) · 25 mg 셀이면 0.86 / 0.76 mm.

### 3-3. ★ 순수 LPSCl 분말 — σ · 상대밀도 vs 적층압 (p.2 · Fig. 1e · SI Fig. S5)
- 원문: *"LPSCl ionic conductivity was measured by electrochemical impedance spectroscopy with two stainless steel blocking electrodes at different stack pressures. Figure 1e shows a monotonic increase in ionic conductivity with relative density and stack pressure, for both SP and LP, up to 500 MPa, reaching 1.2 and 3 mS cm−1, respectively. Stack pressures >500 MPa increased impedance (Figure S5) due to excessive LPSCl particle cracking."* (p.2) · EIS 조건 (SI p.2–3): Gamry Interface-1000 · 10 mV · 1.6 MHz – 0.1 Hz · 상온.
- **[판독] Fig. 1e** (벡터 표지 중심 · 왼축 0–5 mS/cm · 오른축 0.5–1.0):

| 적층압 (판독 위치, MPa) | σ SP (mS/cm) | σ LP (mS/cm) |
|---|---|---|
| 25 | 0.46 | 0.36 |
| 97.6 | 0.75 | 1.31 |
| 195.2 | 0.97 | 2.00 |
| 292.7 | 1.20 | 2.55 |
| 390.3 | 1.36 | 2.91 |
| 487.9 | **1.46** | **3.10** |

| 적층압 (판독 위치, MPa) | 상대밀도 SP | 상대밀도 LP | 기공 SP / LP [카드 산술] |
|---|---|---|---|
| 25 | 0.539 | 0.566 | 46 / 43 % |
| 250.0 | 0.856 | 0.856 | 14.4 / 14.4 % |
| 375.0 | 0.867 | 0.878 | 13.3 / 12.2 % |
| 499.0 | 0.889 | 0.901 | 11.1 / 9.9 % |
| (300 — 선형 보간) | ≈ 0.860 | ≈ 0.865 | ≈ 14.0 / 13.5 % [카드 산술] |

- σ 표지의 가로 위치는 97.6 의 정수배 (97.6 · 195.2 · 292.7 · 390.3 · 487.9) — 명목 100 · 200 · … · 500 MPa 를 다른 단위에서 환산한 값으로 보인다 [카드 해석] (SI Fig. S5 범례는 25 · 100 · … · 700 MPa).  밀도 표지는 25 · 250 · 375 · 500 MPa — **σ 와 밀도의 압력 세트가 다르다.**
- ⚠ **본문 ↔ 그림**: 본문 *"reaching 1.2 … mS cm−1"* (SP) ↔ 그림 SP 최고 압력 점 **1.46 mS/cm** [판독] — 1.2 는 ≈ 300 MPa 표지 (1.20) 의 값이다.  LP 의 *"3"* 는 그림 3.10 과 맞는다.
- **측정 상태 · 분모 [미확인]**: 밀도를 어떻게 쟀는지 (하중 아래 두께인지) · 이론밀도 · 시료 질량 · 지름 · 두께가 원문에 없다.  SI Table S4 의 분리막 상대밀도 0.9 (*"obtained experimentally"*) 는 LP 500 MPa 판독 0.901 과 같은 수다 [판독 대조].
- **[판독] SI Fig. S5 (LPSCl-SP Nyquist, Ω cm²)** — 스파이크가 시작하는 −Z″ 최소점의 Z′ (≈ 시료 전체 면적 저항): **25 MPa 198.4 · 100 120.5 · 200 95.0 · 300 75.8 · 400 67.2 · 500 59.2 · 600 60.4 · 700 61.6** (inset 600 · 700 = 60.39 · 61.55) — 500 MPa 에서 최소 · 그 위에서 조금 오른다 (캡션 *"the resistance slightly increased after 500 MPa"*).  계열 식별 = 범례 표본의 선 색 · 모양 (경로 항목 수) [판독 규칙].
- **[카드 산술 · 같은 시료라는 가정]** σ_SP (Fig. 1e) × R·A (Fig. S5) = 0.091 · 0.090 · 0.093 · 0.091 · 0.091 · 0.087 cm (25 → ≈ 500 MPa) — **압력에 거의 무관한 ≈ 0.9 mm**.  두 그림이 같은 측정이라면 σ 계산에 압력마다 같은 두께를 쓴 것과 맞는다 (같은 질량이면 상대밀도 0.54 → 0.89 에 두께가 ≈ 40 % 줄어야 한다) — 원문은 두께 · 그 측정법을 적지 않았다 [미확인].  ⇒ 이 σ(P) 를 하중 아래 실제 치수의 σ 로 읽지 않는다.
- **"> 500 MPa = 입자 균열"** 은 저자 해석 (그 SEM 근거는 이 논문에 없다 [미확인]).

### 3-4. ★ 입자 파괴 · 변형 관찰 (p.2–4 · Fig. 2b · 3d · SI Fig. S6 · S7 · S9b · S11)
| 단계 | 단결정 NMC | 다결정 NMC | 근거 |
|---|---|---|---|
| 혼합 (볼밀) + 500 MPa 압밀 | *"no signs of the SC-NMC particle fracture despite the high loads used during mixing and pressing"* · 계면 연속 | *"primary particle fracture along grain and/or agglomerate boundaries … with active fragments disconnected from one another and/or the LPSCl"* | [인쇄] p.2 · Fig. 2b · SI Fig. S6c |
| 250 MPa | — | *"the cracking persisted even when the fabrication pressure was lowered to 250 MPa"* | [인쇄] p.2 · SI Fig. S6b |
| 50 MPa | — | *"only at 50 MPa was secondary particle integrity maintained"* (대신 기공 22 %) | [인쇄] p.2–3 · SI Fig. S6a |
| 첫 충전 뒤 (2.5 MPa) | 계면 접촉 손실 (주황 화살표) + **이전에 응집돼 있던 결정의 분리** (흰 화살표, *"due to anisotropic volume change"*) · *"There was no fracture of non-agglomerated SC-NMC particles."* | 계면 접촉 손실 + **입계 균열** · *"larger diameter primary particles … intergranular cracking and dis-aggregation of secondary particles"* | [인쇄] p.4 · Fig. 3d · SI Fig. S9b |

- **압밀 기전 (저자의 정성 설명, p.3 · SI Fig. S7 모식도)**: *"relatively small LPSCl particles will tend to sit in the interstices between larger PC-NMC particles. On application of pressure, there is movement of the hard PC-NMC particles and shear forces are transmitted to the more easily deformed LPSCl. The movement and shearing of the softer LPSCl over the harder NMC surface promotes the required intimate interfacial contact. However, once the PC-NMC particles contact one another, relative motion is inhibited and it is difficult to induce any further shearing of the LPSCl, and the PC agglomerates may start to crack. For the smaller SC-NMC, where the particle diameters are more similar to LPSCl, greater relative motion and shear deformation of the LPSCl is allowed before SC-NMC hard particle contact."* — Fig. S7 의 표지: PC = *"Contact between large PC-NMC particles"* · *"Restricted movement for SSE particles"* · *"High porosity in SSE"* / SC = *"No particle contact"* · *"Particles are able to move"*.  ⚠ 계산 · 측정이 없는 가설 그림이다 (접촉 수 · 응력 · 변위 값 없음).
- 크기 맞춤의 근거: *"a ratio of ≥1 (SSE powder diameter ≤active powder diameter) has been suggested to promote efficient active material utilization"* (ref 18 = Shi 2020 — 정본 `shi2019_high_am_loading_particle_size_assb`) — 이 논문의 SP (1–5 µm) ↔ SC (D50 3.4 µm) 는 비 ≈ 1 · LP (1–20 µm) 는 분리막에만.

### 3-5. ★ 구조 · 전기화학 숫자 (p.3–5 · Fig. 3–5 · SI Fig. S9–S12 · SI Table S4)
| 항목 | 단결정 | 다결정 | 표지 · 쪽 |
|---|---|---|---|
| 적재 · 면적 용량 | 14 mg cm⁻² · 3 mAh cm⁻² · 고적재 42.42 mg cm⁻² · **8.7 mAh cm⁻²** · 두께 **≈ 200 µm** | 14 mg cm⁻² · 2.2 mAh cm⁻² | [인쇄] p.3 · p.5 · SI Fig. S9 캡션 · Table S4 |
| 첫 사이클 (2.5 MPa · 0.2 mA cm⁻² · 30 °C · 4.3–2.5 V) | 방전 **204 mAh g⁻¹** · CE **85 %** · U_C 3.861 V · U_DC 3.823 V · 그림 화살표 "−15%" · [판독] 충전 끝 240.9 · 방전 끝 203.4 (84.4 %) | 방전 **152 mAh g⁻¹** · CE **≈ 70 %** · U_C 3.875 · U_DC 3.793 V · "−30%" · [판독] 217.2 / 152.6 (70.3 %) | [인쇄] p.3–4 · Fig. 3a · S9a · [판독] |
| 계면 저항 (충전 4.3 V · 10 MPa · 30 °C) | **≈ 40 Ω cm²** (*"about half that of its PC-NMC counterpart"*) · [판독] 호 폭 37.1 (Z′ 104.3 → 141.4) | [판독] 호 폭 86.2 (99.1 → 185.3) · 비 0.43 [카드 산술] | [인쇄] p.4 · [판독] SI Fig. S10 |
| 10 사이클 (2.5 · 10 MPa · 6 사이클부터 0.1 mA cm⁻²) | 첫 방전 204 · 205 · 유지 **99.4 · 101.1 %** · 10 MPa 10 사이클 뒤 ≈ 210 mAh g⁻¹ · [판독] 2.5 MPa 203.4 → 202.4 · 10 MPa 204.7 → 207.0 | — | [인쇄] p.4 · [판독] Fig. 4a · 4b |
| LTO 음극 · 10 MPa · 50 사이클 (9 → 58) | **96.3 %** · [판독] 148.5 → 143.0 · 율속 0.2 / 0.5 / 1.0 / 2.0 mA cm⁻² → 205 · 149 · 80–83 · 26–28 mAh g⁻¹ | **92.4 %** · [판독] 112.4 → 103.9 · 율속 → 151–153 · 112–113 · 66–68 · 24–25 | [인쇄] p.4 · [판독] Fig. 4c · SI Fig. S9c |
| 첫 CE vs 적층압 | [판독] 0.2 MPa (비대칭) 82.7 ± 1.3 · 2.5 MPa 83.8 ± 0.5 · 10 MPa 85.0 ± 0.3 % (막대 뜻 · 셀 수 [미확인]) · 본문 0.2 MPa *"∼83%"* · 2.5 · 10 MPa *"∼85%"* · **50 MPa = 첫 충전 중 단락** ([판독] 55.4 mAh g⁻¹ · 3.65 V 에서 급락 → 73.9 mAh g⁻¹ 에 1 V 아래) — 저자: Li 침투 | [판독] 2.5 MPa 70.4 ± 0.3 · 10 MPa 71.4 ± 0.8 % | [인쇄] p.4–5 · [판독] SI Fig. S12 |
| 비대칭 0.2 MPa (양극) / 2.5 MPa (음극) | 14 mg cm⁻²: 5 사이클 [판독] 202.8 → 198.1 (2.5/2.5: 203.4 → 198.6 · 10/10: 204.7 → 201.8) · 고적재 8.7 mAh cm⁻²: 방전 **205 mAh g⁻¹** · CE **87 %** (범례 87.3 % · U_DC 3.674 V) · [판독] 235.0 / 205.5 | — | [인쇄] p.5 · [판독] Fig. 5b · 5c |
| 추정 에너지 밀도 | 분리막 1.5 mm → 20 µm 가정 · Li 50 µm · Cu 10 · Al 15 µm 포함 → **405 Wh kg⁻¹ · 1069 Wh L⁻¹** | — | [인쇄] p.5 · SI Table S4 |
| 충전 격자 부피 | 101.62 → 96.08 Å³ = **−5.5 %** (*"near reversible"*) · H3 상 (≈ 4.2 V 피크) | — | [인쇄] p.4 · Fig. 3b · 3c |

- ⚠ [카드 산술] SI Table S1 의 pristine 격자 (a 2.8727 · c 14.1958 Å) 로 계산한 부피는 **101.45 Å³** (본문 101.62 와 0.17 % 차) · 충전 (2.81354 · 14.0151) 은 96.08 Å³ (본문과 같음) → 표의 값으로는 −5.3 %.
- 굴곡도 · 유효 이온 / 전자 전도도 · 피복률 · 접촉 면적 같은 미세구조 수송 숫자는 **없다**.
- 문헌 대조 그림 (Fig. 5d · [판독]): 이 논문 205.5 @ 0.2 · 210.0 @ 2.5 MPa ↔ NCA (ref 32) 139.5 @ 5 · FCG75 (ref 6) 207 @ 7 (자홍 = 고온 색) · 194 @ 7 · SC-NMC811 (ref 15) 187 @ 25 · SC-NCA (ref 31) 199 @ 70 · NMC85 (ref 7) 193 @ 187.5 MPa — 색 막대 = 온도 30–70 °C.

### 3-6. 적층압 장치 · 벽 마찰 FEM (p.3 · p.5 · SI p.3 · SI Fig. S8 · S13 · Table S3)
- 대칭 적층압 = 나사 + 토크 렌치, 로드셀로 보정 — [판독] SI Fig. S8b (지름 5 mm): 0.2 N·m → 2.5 MPa · 1.0 → 11.25 · 2.0 → 23.5 · 3.0 → 37.0 · 4.0 N·m → 50.0 MPa.
- 비대칭 = 양극 쪽 압축 스프링 (SI Table S3: 전단 탄성률 81 500 MPa · 선 0.4 mm · 평균 지름 4.15 mm · 유효 감김 5 · 강성 0.73 N/mm · 처짐 5 mm → 3.65 N → 19.63 mm² 에 **0.19 MPa**; 로드셀 실측 4 N → 0.2 MPa) + 음극 쪽 보정된 축 하중 2.5 MPa.
- 원리: *"Pressure asymmetry was possible because of the high friction coefficient and contact area between the SSE pellet and the mold wall."* · FEM (SI p.3): *"Geometries and calculations were implemented with Inventor software. It was assumed that the pellet was fixed at the outer surface due to its high friction with the plastic mold."* · SI Fig. S13 그림 안 값 [인쇄]: 바닥 (음극) σ_zz −2.5 MPa · 윗면 (양극) 0 MPa · 윗모서리 −1.32 MPa.  탄성 상수 · 마찰 계수 · 요소 수 · 펠릿 치수 [미확인] (*"under reasonable friction assumptions"* 뿐).

---

## 4. ★ 방법 — 측정 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 사슬
분말 (SC-NMC · PC-NMC · LPSCl-SP 자체 합성 · LPSCl-LP 상용) → DLS · SEM · EBSD (단면, PVDF/NMP 로 Al 박에 펴서 Ar 이온 연마) · XRD (Rigaku MiniFlex · Cu Kα1 · 글러브박스 안 · Profex Rietveld) · EDX (AZtec) · XPS (PHI VersaProbe III · Ar⁺ 1 kV 식각 깊이 분석) → LiNbO₃ 코팅 → 유성 볼밀 혼합 (140 rpm · 30 min) → PEEK 몰드 · WC 다이에 LP 분리막 + 양극 혼합물 적층 → **500 MPa · 상온 한 번** → Li 박 (+ Cu) 또는 LTO 음극 · Al 집전체 → 셀 장치 (토크 렌치 또는 스프링) → EIS · 정전류 (0.1 · 0.2 mA cm⁻² · 4.3–2.5 V · 30 °C) · 충전 뒤 단면 SEM · ex situ XRD.  순수 LPSCl 은 스테인리스 차단 전극 사이에서 적층압별 EIS + 상대밀도.
- 안 한 것: 압력별 단결정 복합 밀도 · 가압 중 높이 · 탈압 회복 · 유지 시간 영향 · 조성 스윕 · 굴곡도 / 유효 σ_ion · 피복률 정량 · 단면 기공 분할의 방법 · 반복 통계 · 입자 모델.

### 4-2. 입자 처리
- 실험 — 실제 분말.  "단결정" = 비응집 결정 (1–2 µm) 이지만 DLS 상 응집이 섞여 D50 3.4 µm · 충전 뒤 응집 결정끼리 떨어진다 (Fig. 3d).  "다결정" = 1차 입자 응집 2차 입자 (D50 5.9 µm).
- 우리 대응: DEM = 구 (AM 단단 · SE 연화 영률) · 접촉 hooke/hysteresis · **입자 파쇄는 후처리 (Auerbach)** · AM 크기 2 종 (PC · SC) — 이 논문의 "PC 는 250 MPa 에서 깨진다" 는 우리 침대에서 파쇄 판정이 걸리는 자리의 실험 쪽 관찰이다 (값 비교 아님).

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말했나** — **말 없음** (본문 · SI 에 DEM · discrete element · particle simulation 이 없다).  계산은 SI Fig. S13 의 펠릿 탄성 FEM 하나뿐이다.
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유와 우회 · 비용** — 계산이 없어 말도 없다.  재료 쪽 진술만 있다: *"sulfides have a relatively low flow stress even at room temperature (RT) and can be manipulated into intimate contact with the active particles by applying an external load during processing and/or service"* (p.1) · *"shear forces are transmitted to the more easily deformed LPSCl"* · *"once the PC-NMC particles contact one another, relative motion is inhibited and it is difficult to induce any further shearing of the LPSCl, and the PC agglomerates may start to crack"* (p.3) · *"Stack pressures >500 MPa increased impedance … due to excessive LPSCl particle cracking"* (p.2) · *"cracking may occur not only during cycling but during manufacture where pressures >100 MPa are frequently used in an effort to reduce or eliminate composite cathode porosity"* (p.1).  ⇒ 우리 재설계 조건 R1 (AM 이 움직이고 하중을 나눔) · R6 (SE 형상 변형) · R7 (AM 파괴) 이 **같은 압밀 안에서 함께 일어난다** 는 정성 진술 (맞춘 값 · 계산 비용 0).
3. **2D 인가 3D 인가** — 실험 3D.  FEM 은 펠릿 하나 (단면 + 위 · 아래 면 그림 · 3D 로 읽힌다 [카드 해석]).  2D → 3D 전이 말 없음.
4. **압력을 뺄 때의 거동** — **다루지 않았다.**  밀도는 500 MPa 를 뺀 뒤 (단면) 한 상태 · 가압 중 높이 · 회복량 없음.  사이클 중 NMC 수축 (−5.5 %) 에 따른 **계면 이탈** 은 관찰했다 (Fig. 3d · S9b) — 기계적 탈압이 아니라 화학–기계 수축이다.  적층압 0.2–50 MPa 는 제조 500 MPa 와 다른 하중 (제조압 ↔ 작동압 분리 — 정본 `doux2020_stack_pressure_assb` 와 같은 틀).

### 4-4. 기법 미니 용어집
- **SC / PC NMC**: 단결정 (비응집 1차 입자) / 다결정 (1차 입자가 뭉친 2차 입자) 층상 니켈 산화물.
- **LPSCl-SP / LP**: 이 논문의 이름 — 직접 볼밀링한 작은 입자 (1–5 µm) / 상용 큰 입자 (1–20 µm) Li₆PS₅Cl.
- **상대밀도**: 겉보기 밀도 ÷ 이론밀도 — 이 논문은 분모 · 측정법을 적지 않았다.
- **비대칭 적층압**: 금형 벽 마찰로 음극 쪽 하중 (2.5 MPa) 이 양극 쪽에 거의 전달되지 않게 하고 양극에는 스프링 0.2 MPa 만 주는 배치.
- **첫 사이클 쿨롱 효율 (CE)**: 첫 방전 ÷ 첫 충전 용량.
- **LiNbO₃ 코팅**: 황화물 SE 와 산화물 양극 사이 부반응을 줄이는 얇은 산화물 껍질.

---

## 5. Figure set ★
| 그림 (크롭 파일) | 내용 | 우리 활용 |
|---|---|---|
| graphical abstract (`fig_GA.png`) | 첫 충방전 곡선 (0.2 MPa) + 셀 그림 + NMC/SE 단면 확대 ">5 vol%" · "13%" 화살표 (캡션 없음 · Fig. 5c 셀과 같은 모양 [카드 해석]) | 논문 요지 |
| Fig. 1 (`fig_1.png`) | (a) SC-NMC SEM (b) DLS 분포 (c) LPSCl-SP SEM (d) LPSCl-LP SEM (e) **σ · 상대밀도 vs 압력 (SP · LP)** (f) XRD | ★ 순수 SE σ(P) · d(P) [판독] · 입도 |
| Fig. 2 (`fig_2.png`) | (a) 공정 모식 (혼합 → 500 MPa 단축 → 셀) (b) **500 MPa 단면 SEM** (c) EDX C · S · Ni | ★ 상대밀도 ≈ 90 % 의 근거 그림 · SE 가 NMC 사이를 메운 모양 |
| Fig. 3 (`fig_3.png`) | (a) 첫 충방전 (b) dQ/dV (c) ex situ XRD (d) 충전 뒤 단면 (접촉 손실 · 응집 분리) | 사이클 화학–기계 (흐름 밖) |
| Fig. 4 (`fig_4.png`) | (a) 2.5 MPa · (b) 10 MPa 10 사이클 (c) LTO 셀 율속 · 58 사이클 | 전기화학 |
| Fig. 5 (`fig_5.png`) | (a) 대칭 ↔ 비대칭 적층압 모식 (b) 0.2 MPa 방전 · 압력 조합 비교 (c) 8.7 mAh cm⁻² 셀 (d) 문헌 대조 (적층압 · 온도) | 저압 작동 · 문헌 지도 |
| SI Fig. S1 (`fig_S1.png`) · Table S1 (`tab_S1.png`) | SC-NMC XRD Rietveld · 격자 (pristine · 충전 · 방전) | NMC 밀도 계산 (§3-1) · 부피 −5.5 % |
| SI Fig. S2 (`fig_S2.png`) · Table S2 (`tab_S2.png`) | EDX 스펙트럼 · 조성 | 재료 확인 |
| SI Fig. S3 (`fig_S3.png`) | (a) SC · (b) PC 단면 SEM · 패턴 품질 · 결정립 지도 (EBSD) | ★ 단결정 ↔ 다결정 형태 |
| SI Fig. S4 (`fig_S4.png`) | LiNbO₃ 코팅: EDX Ni · Nb · XPS survey · 깊이 조성 · 고분해 스펙트럼 | 코팅 확인 |
| SI Fig. S5 (`fig_S5.png`) | LPSCl-SP Nyquist 25–700 MPa · inset (500–700 MPa 저항 상승) | ★ 순수 SE 저항 vs 압력 [판독] |
| SI Fig. S6 (`fig_S6.png`) | **PC-NMC/LPSCl 단면 50 · 250 · 500 MPa** (파쇄 흰 화살표 · 캡션 78 / 82 / 86 %) | ★ 복합 양극 압력 세 점 · 입자 파쇄 문턱 |
| SI Fig. S7 (`fig_S7.png`) | 압밀 중 PC ↔ SC 와 SE 의 상호작용 모식 (세 단계) | ★ 정성 기전 (AM–AM 접촉 → 전단 정지 · 파쇄) |
| SI Fig. S8 (`fig_S8.png`) · Table S3 (`tab_S3.png`) | 셀 장치 · 토크 ↔ 압력 보정 · 스프링 셀 · 스프링 계산 | 적층압 근거 |
| SI Fig. S9 (`fig_S9.png`) | PC-NMC 첫 충방전 · 충전 뒤 단면 (입계 균열) · LTO 셀 사이클 | 대조 |
| SI Fig. S10 (`fig_S10.png`) | 충전 셀 Nyquist SC ↔ PC | 계면 저항 ≈ 40 vs ≈ 86 Ω cm² [판독] |
| SI Fig. S11 (`fig_S11.png`) | 혼합 · 압밀 · 사이클 중 PC ↔ SC 미세구조 변화 모식 | 저자 해석 요약 |
| SI Fig. S12 (`fig_S12.png`) | 첫 CE vs 적층압 · 50 MPa 첫 충전 단락 | 작동압 창 |
| SI Fig. S13 (`fig_S13.png`) | 벽 마찰 FEM — 음극 −2.5 MPa → 양극 0 MPa | ★ 펠릿 벽 마찰이 전달 압력을 끊는다 (마찰 계수 미기재) |
| SI Table S4 (`tab_S4.png`) | 고적재 셀 변수 (조성 · 상대밀도 0.9 · 두께 · 용량 · 지름 5 mm · 압력) | ★ 조성 · 상대밀도의 표 원천 |
| 근거 문단 6 장 (`txt_p1_…` · `txt_p2a_…` · `txt_p2b_…` · `txt_p3_…` · `txt_p4_…` · `txt_S2_…`) | 제조 압력 ↔ 균열 · 입경 맞춤 · σ(P) · 500 MPa 압밀 · 상대밀도 ≈ 90 % · PC 파쇄 · 기공 14 → 22 % · 전단 기전 · 충전 뒤 접촉 손실 · 제조 절차 | 인용 근거 (표가 없어 값이 전부 문장에 있다) |

## 6. Post-processing ★
- **원문**: DLS (Horiba) · Rietveld (Profex) · EDX (AZtec) · XPS (CasaXPS · Gaussian–Lorentzian / Voigt) · EBSD (밴드 대비 · IPF) · 상대밀도 = 방법 미기재 · FEM (Inventor) · 에너지 밀도 = SI Table S4 변수로 (식 미기재) · 스프링 하중 = Stewart 식 (SI ref S1).
- **이 카드**: 그림 16 장 벡터 경로 판독 (`digitized.csv` — 표지 중심 · 곡선 끝 · 오차막대 끝 · Nyquist 계열은 범례 표본의 색 · 모양으로 식별 · inset 뒤에 가려진 본 그림 점은 뺐다) · NMC 결정 밀도 (Table S1) · vol% · 두께 대조 · σ × R·A 대조 · 격자 부피 재계산 · 기공 = 1 − d.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (우리 수치는 CLAUDE.md · `docs/` 의 값을 출처와 함께 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 재료 | NMC83 (SC, LiNbO₃) · NMC811 (PC) + Li₆PS₅Cl + C65 | NCM811 + Li₆PS₅Cl (SE 반지름 0.5 µm 급) · 탄소 첨가제는 일부 계열만 | 같은 재료계 · 조성 · 코팅 · 탄소가 다르다 |
| 입경 | SC D50 3.4 µm (결정 1–2) · PC D50 5.9 · SE 1–5 µm | AM 두 크기 (SC · PC) · SE ⌀1 µm (CLAUDE.md "r_SE 0.5 µm") | SE 가 우리보다 크고 AM 과 비슷 (비 ≈ 1) |
| 가압 | 500 MPa · 상온 · 분리막과 함께 한 번 · 지름 5 mm · 유지 [미확인] | DEM 300 MPa · 판 정지 + 판 고정 이완 (하중 아래) | 압력 · 하중 이력 · 상태가 다르다 |
| 밀도 상태 | **하중 뺀 뒤 · 다이 밖 단면** · 분모 · 방법 미기재 | 하중 아래 · 구 부피 합 (ε_sphere) 규약 · 순수 SE 기준 = 기공 10–13 % · 진밀도 1.64 (1저자 11-10 Q5, CLAUDE.md) | 상태 · 연산자 · 분모가 다 다르다 → §7-3 표로만 견준다 |
| 복합 기공 | SC 500 MPa ≈ 10 % · PC 50 / 250 / 500 MPa = 22 / 18 / 14 % | real_14 DEM 15.6 % (300 MPa · CLAUDE.md SE-DUMP 절 · SE/고체 ≈ 26 vol%) · [DEM 우선 (수영)] 단계 5 = 예측값 (맞추지 않음) | 조성 (SE ≈ 51 vol% ↔ ≈ 26) · 압력 · 상태가 달라 판정 아님 |
| 순수 SE | LPSCl SP · LP: 250 MPa 14.4 % · 375 MPa 13.3 / 12.2 % · ≈500 MPa 11.1 / 9.9 % (분모 미기재 · [판독]) | 랩 표준 10–13 % (1.64 · ≈300 MPa) | 300 MPa 보간 ≈ 14 / 13.5 % = **랩 표준과 다른 문헌 값** (분모를 모르므로 환산하지 않는다) |
| 입자 파괴 | PC: 250 MPa 이상 1차 입자 파쇄 · SC: 500 MPa 에서도 없음 | DEM 파쇄 = Auerbach 후처리 (입자 모양 · 하중 경로는 안 바뀜) · MPM = AM 얼림 | 우리 침대에서 판정이 걸리는 자리의 관찰 — 문턱 값 비교 아님 |
| 압밀 기전 | 정성: AM 이동 → SE 전단 → AM–AM 접촉에서 정지 · 파쇄 | DEM: 재배열 + 겹침 (연화 영률) · MPM: AM 얼린 장애물 · SE 소성 (CLAUDE.md DO-NOT: 얼린 AM 은 하중 0) | 재설계 R1 (AM 이 움직이고 하중을 나눔) 이 왜 필요한지의 실험 쪽 진술 |
| 탈압 | 없음 | 언로딩 시험 (등록 단계) | 대조점 없음 |
| 수송 | 계면 저항 (EIS) · 순수 SE σ(P) | 접촉망 σ · 복셀 σ | 복합 σ_ion · 굴곡도가 없어 수송 대조점 아님 |

### 7-2. ★ 기존 복합 양극 카드와 나란히 (값 · 조건 그대로 · 기존 카드는 고치지 않는다 · 판정하지 않는다)
| 카드 | 계 | 공정 · 압력 | 상태 · 측정 | 그 카드의 값 |
|---|---|---|---|---|
| **이 논문 (SC)** | SC-NMC83 (LiNbO₃) 70 · LPSCl-SP 27.5 · C65 2.5 wt% (≈ 45 : 51 : 4 vol% [카드 산술 · 1.64]) | 볼밀 혼합 · **500 MPa** 상온 · 분리막과 함께 | 하중 뺀 뒤 단면 SEM · 분모 미기재 | 상대밀도 ≈ 0.90 → 기공 ≈ 10 % |
| **이 논문 (PC)** | PC-NMC811 · 같은 공정 | **50 / 250 / 500 MPa** | "estimated" · 분모 미기재 | 0.78 / 0.82 / 0.86 → 22 / 18 / 14 % |
| `minnmann2021_jes_charge_transport_bottlenecks` | NCM622 + LPSCl · CAM 25 / 33 / 42 / 53 / 61 vol% (42 vol% = 70 wt%) | 막자사발 건식 혼합 · **380 MPa** 단축 | (V_meas − V_theo)/V_meas · 측정 두께 × 면적 · 저자 *"errors, as high as 10 %"* [정본 카드] | 7.6 / 13 / 17 / 17 / 15 % (평균 14 %) [정본 카드 · SI Table S1] |
| `minnmann2024_microstructure_porosity_visualization` | (그 카드 — 같은 저자 계보 복합 양극) | **380 MPa** | 토모그래피 분할 기공 (나노 기공 미검출 · *"segmented ≪ geometric"*) [정본 카드] | BM10 ≈ 10 · BM03 ≈ 7.5 · BM01 ≈ 6 % [그 카드 판독] |
| `kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact` | PC-NCM811 + LPSCl 1–5 µm (80 : 20 · 90 : 10 wt%) + CNF 3 wt% | 손 혼합 / 메카노퓨전 · 셀 300 MPa · 1 min (그 카드 p.9) | V_meas 로 낸 계산 기공 (측정법 [미확인] — 그 카드) | 42.4 / 36.6 % [정본 카드] |
| `wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode` | NCM85 3.8 µm 82 wt% + C65 2 · PTFE 0.5 건식 막 | **683 · 800 MPa** | (그 카드) | 16.1–16.3 % · 12.6 / 10.8 % [비교 문서 10-27 줄] |
| `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` | NMC622 : LPSCl : CBD 69 : 27.6 : 3.4 습식 | CUP ≈116 MPa · 상온 ↔ WIP **400 MPa · 80 °C** | 보고 기공 (성분 밀도 미공개) | 25.1 ↔ 10.9 % [비교 문서 11-06 줄] |
| `bazzoun2026_dem_fem_rnm_ionic` | NMC811 + LPSCl 70 : 27.7 wt% (45 : 53 vol%, CNF : PTFE 2 : 0.3) | **400 MPa** | 기공 값은 그 카드에 없다 (σ_eff,ion 0.137 mS/cm) | — (조성 쌍둥이 · 같은 70 wt%) |

- **읽는 법**: 70 wt% 근처 NMC + LPSCl 복합의 압밀 뒤 기공이 카드마다 **≈ 10 % (이 논문 SC 500 MPa) · 14 % (이 논문 PC 500 MPa) · 17 % (Minnmann 380 MPa · 42 vol%) · 36–42 % (Kim 계산값)** 로 흩어진다 — 압력 · 혼합 · 입경 · 분모 · 측정법이 다 다르다.  같은 압력 (500 MPa) · 같은 공정에서 **단결정이 다결정보다 4 %p 치밀** 하다는 것이 이 논문 안에서만 서는 대조다.
- **순수 SE (나란히)**: 이 논문 LPSCl ≈ 500 MPa 0.89–0.90 · 375 MPa 0.87–0.88 [판독 · 분모 미기재] ↔ `ketter2025_…` LPSCl 펠릿 ρ_rel 87.87 ± 0.64 % (370 MPa 3 min → 등방 500 MPa 60 min) [정본 카드] ↔ `var2026_…` ~10 µm 400 MPa 0.78 (1.87 기준 · 하중 뺀 뒤 몰드 안) [정본 카드] — 나머지 순수 LPSCl 압밀 값은 정본 `var2026_…` 카드 §7-2 표 (`lee2025_heckel_argyrodite_powder_densification_nanoindentation` · `faka2026_particle_size_consolidation_strain_lpscl` · `miss2026_insitu_conductivity_porosity_pressure_compaction` · `wang2024_hot_pressed_lpscl_pressure_invariant_conductivity` · `larson2025_hot_pressing_argyrodite_low_stack_pressure_conductivity` · `thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography` · `tron2023_lpscl_ccd_ambient_pressure` · `beutl2024_round_robin_coin_cell_sulfide_assb`).

### 7-3. ★ 결과 전에 견줄 외부 값 후보 — 조건이 우리와 어디가 같고 다른가
우리 계획 ([DEM 우선 (수영)]) 에서 **복합 양극의 기공률은 맞추는 값이 아니라 계산이 예측하는 값** 이다 (순수 SE 10–13 % · 진밀도 1.64 만 기준 · 1저자 11-10 Q5).  아래 값은 결과가 나온 **뒤** 견줄 후보로 결과 전에 적어 둔다 (맞추는 데 쓰지 않는다).

| 조건 | 후보 ① SC 복합 (500 MPa → ≈ 0.90) | 후보 ② PC 복합 (50 / 250 / 500 → 0.78 / 0.82 / 0.86) | 우리 단계 5 (3D 복합 가압 · 계획) | 같음 / 다름 |
|---|---|---|---|---|
| AM | NMC83 단결정 · LiNbO₃ · D50 3.4 µm | NMC811 다결정 · D50 5.9 µm | NCM811 SC · PC 두 크기 | 재료 계열 같음 · 니켈 조성 · 코팅 · 크기 다름 |
| SE | LPSCl 1–5 µm (밀링 · 미반응 Li₂S) | 같음 | LPSCl ⌀1 µm | SE 크기가 다르다 (이 논문 ≈ AM 크기) |
| 탄소 · 바인더 | C65 2.5 wt% · 바인더 없음 | 같음 | 없음 (기본) | 다름 (C65 ≈ 4 vol% [카드 산술]) |
| 조성 | 70 : 27.5 : 2.5 wt% ≈ 45 : 51 : 4 vol% [카드 산술] | 같음 (*"identical processing methodology"*) | 조성 축으로 계산 | 같은 조성 점을 계산에 넣어야 견줄 수 있다 |
| 압력 · 온도 | 500 MPa · 상온 | 50 · 250 · 500 MPa · 상온 | ≈ 300 MPa · 온도 없음 | 압력 다름 (② 는 300 을 사이에 둔다) |
| 하중 이력 | 한 번 · 분리막과 함께 · 유지 [미확인] | 같음 | 판 가압 → (탈압 = 단계 6) | 분리막 동시 압밀 · 유지 시간은 우리에게 없다 |
| 상태 | **하중 뺀 뒤 · 다이 밖** | 같음 | 단계 5 = 하중 아래 · 단계 6 = 뺀 뒤 | **단계 6 (탈압) 결과와 견준다** |
| 측정 연산자 | 단면 SEM 문장 안 값 (방법 미기재) | "estimated" | 계산 기공 (연산자 = 단계 0 에서 결과 전에 정함) | 연산자 미기재 → 낮은 등급 대조 |
| 분모 | 미기재 | 미기재 | 1.64 (LPSCl) + AM 밀도 | 분모가 달라질 수 있다 (±수 %p) |
| 입자 상태 | 파쇄 없음 | 250 · 500 MPa 에서 파쇄 | AM 파괴 (R7) 미구현 | ② 는 파쇄가 섞인 기공 — 파쇄 없는 모델과 견주면 기공 차의 일부가 파쇄 몫일 수 있다 |

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 복합 양극의 공정 → 압밀 뒤 상태 (상대밀도 · 단면 · 입자 파쇄) 의 실험 쪽 관찰과, 순수 LPSCl 의 σ(P) · d(P).
- **없는 것**: 모델 · 접촉망 · 복합 σ_ion · 굴곡도 · 가압 중 곡선 · 탈압 · 조성 축 · 기공의 측정 연산자.  ⇒ DEM (수송) · MPM (형상 소성) 어느 쪽의 검증 표적도 아니고, **결과 전 대조 후보 + 압밀 중 AM 파쇄 · 전단 기전의 정성 관찰** 이다.

---

## 8. 적용 인사이트 (행동)
1. **결과 전 대조 항목으로 등록할 것 (단계 5 · 단계 6)**: ① SC 복합 500 MPa → 상대밀도 ≈ 0.90 · ② PC 복합 50 / 250 / 500 MPa → 0.78 / 0.82 / 0.86 — 꼬리표 "NMC + LPSCl 1–5 µm + C65 2.5 wt% · 70 wt% · 상온 · 분리막 동시 압밀 · **하중 뺀 뒤 단면** · 측정법 · 분모 미기재".  맞추는 데 쓰지 않는다 (frame[4]) · 가압 중 값과 견주지 않고 탈압 (단계 6) 뒤 값과 견준다.
2. **기공률 연산자 (단계 0)**: 문헌 값마다 ⓐ 상태 (가압 중 / 하중 뺀 뒤 · 다이 안 / 다이 밖 · 단면) ⓑ 방법 (질량–두께 / 단면 분할 / "estimated") ⓒ 분모 ⓓ 유지 시간 을 칸으로 둔다 — 이 논문은 ⓑ–ⓓ 가 없어 낮은 등급이다.
3. **AM–AM 접촉 = 전단 정지 · 파쇄 (관측량 제안 · 단계 5 · 후보 A / A′ / B)**: 저자 기전 (p.3) 을 계산에서 볼 수 있는 양으로 옮기면 "AM–AM 접촉 수 · 그 접촉이 받는 하중 몫 ↔ SE 누적 전단 변형 ↔ AM 응력" 이다.  재설계 후보가 이 셋을 함께 내는지가 R1 (AM 이 움직이고 하중을 나눔) 의 확인 항목이 된다 — 이 논문은 정성 그림이라 값 표적은 아니다.
4. **AM 파괴 (R7) 의 실험 쪽 괄호**: 이 조성의 다결정 NMC (D50 5.9 µm) 는 **50 MPa 온전 · 250 MPa 파쇄**, 단결정은 500 MPa 에도 온전 [인쇄] — 우리 Auerbach 판정 (D0) · 앞으로의 AM 파괴 모형이 PC 를 이 구간에서 깨는지의 방향 대조 (입경 · 조성 다름 · 정성).
5. **순수 SE 의 "랩 표준과 다른 문헌 값"**: LPSCl 300 MPa 보간 기공 ≈ 14 / 13.5 % (SP / LP · 분모 미기재) — 랩 표준 (10–13 % · 1.64) 은 그대로 두고 이 값은 나란히만 적는다 (단계 4).  ⚠ σ(P) 는 같은 두께로 계산한 것으로 보인다 (§3-3) → σ 를 하중 아래 치수의 σ 로 쓰지 않는다.
6. **흐름 밖: 펠릿 벽 마찰** — 지름 5 mm 펠릿에서 벽 마찰이 음극 2.5 MPa 를 양극 쪽 ≈ 0 으로 끊는다 (SI Fig. S13 · 마찰 계수 미기재).  우리 DEM · MPM 은 주기 / 마찰 없는 옆면이라 이 하중 감쇠가 없다 — 작은 지름 · 두꺼운 분리막 실험 펠릿 (두께 / 지름 ≈ 0.3) 과 견줄 때 실험 쪽 압력이 층마다 다를 수 있다는 한정어를 단다.
7. **흐름 밖: 사이클 접촉 원장 (A10)** — 충전 −5.5 % 격자 부피 → SC 는 계면 이탈 + 응집 결정 분리 · PC 는 입계 균열 [인쇄] = 우리 `cycle_contact_ledger` 의 SC (계면 debond) ↔ poly (입계 내부 void) 구분과 같은 방향의 관찰 (정량 없음).

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "A single-crystal LiNi₀.₈₃Mn₀.₀₆Co₀.₁₁O₂ / Li₆PS₅Cl / Super C65 (70 : 27.5 : 2.5 wt%) cathode cold-pressed once at 500 MPa showed no particle fracture and an overall relative density of about 90 % in cross-section (Doerrer et al., *ACS Appl. Mater. Interfaces* 2021); the measurement method and theoretical density are not given."
- "With the same processing, a polycrystalline NMC811 cathode reached estimated relative densities of 78, 82 and 86 % at 50, 250 and 500 MPa, but its particles fractured at 250 MPa and above."
- "The authors attribute the difference to particle motion: hard NMC particles shear the softer Li₆PS₅Cl until NMC–NMC contacts stop relative motion, after which polycrystalline agglomerates start to crack (qualitative, no simulation)."
- 국문: *"단결정 NMC + 1–5 µm LPSCl 복합 양극은 500 MPa 상온 압밀 뒤 상대밀도 ≈ 0.9 · 파쇄 없음, 같은 공정의 다결정은 250 MPa 이상에서 깨진다 (Doerrer 2021) — 밀도는 하중을 뺀 단면 값이고 측정법 · 분모가 적혀 있지 않다."*

## 10. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**
1. σ_SP 가 낮은 이유는 *"may be explained by some unreacted Li2S"* (추정) · > 500 MPa 임피던스 상승 = *"excessive LPSCl particle cracking"* (근거 그림 없음) (p.2).
2. 저압 · 고압 적층압의 한계: 1 MPa 음극은 Li 공극 · 높은 압력은 *"may promote particulate cracking and become impractical for larger scale cells or packs"* (p.3) · 50 MPa 는 첫 충전 단락 (p.4).
3. 율속: *"further optimization will be required to enable faster charging/discharging"* (p.4).
4. FEM: *"under reasonable friction assumptions"* (p.5) — 마찰 계수 · 물성 미기재.
5. 에너지 밀도는 분리막 20 µm 가정 (실험 1.5 mm) (SI Table S4).

**카드가 본 한계 · 원문 안 어긋남**
6. **상대밀도의 측정법 · 분모 · 반복이 없다** — "≈ 90 %" 는 단면 SEM 문장 안 · "78 / 82 / 86 %" 는 "estimated".
7. **단결정 복합의 압력 축이 없다** (500 MPa 한 점) — "SC 가 더 잘 치밀화된다" 는 500 MPa 에서 한 쌍 (0.90 ↔ 0.86) 의 대조뿐.
8. **본문 σ_SP 1.2 mS/cm ↔ 그림 최고 압력 점 1.46** [판독] (§3-3) · σ 표지 위치 (97.6 의 배수) ↔ 밀도 표지 위치 (25 · 250 · 375 · 500) 가 다르다.
9. σ × R·A 대조가 압력에 무관한 두께 ≈ 0.9 mm 를 준다 — σ(P) 계산에 쓴 두께가 압력마다 같았을 가능성 (§3-3 · 카드 산술 · 같은 시료 가정).
10. **격자 부피**: Table S1 의 pristine 값은 101.45 Å³ (본문 101.62) [카드 산술].
11. **다결정 대조는 NMC811** (단결정 NMC83 과 니켈 조성 다름) · 입경도 다르다 (3.4 ↔ 5.9 µm) — SC ↔ PC 차이를 형태 하나로 가르지 못한다.
12. **압밀 기전 (p.3 · Fig. S7)** 은 모식도와 단면 SEM 에 기댄 해석이다 — 접촉 수 · 응력 · 전단 변형을 잰 것이 아니다.
13. 오차막대 (SI Fig. S12a) 의 뜻 · 셀 수가 없다 · 다른 그림은 셀 한 개로 보인다 [미확인].
14. **전이 한계**: NMC83 · LiNbO₃ · C65 · SE ≈ AM 크기 · 500 MPa · 하중 뺀 뒤 — 우리 계 (NCM811 · SE ⌀1 µm · 300 MPa · 하중 아래) 와 같은 조건이 아니다.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 6 | Jung, S. H.; Kim, U. H.; Kim, J. H.; Jun, S.; Yoon, C. S.; Jung, Y. S.; Sun, Y. K. Ni-Rich Layered Cathode Materials with Electrochemo-Mechanically Compliant Microstructures for All-Solid-State Li Batteries. Adv. Energy Mater. 2019, 10, 1903360. | FCG75 (Fig. 5d) · 형태 설계 — 카드 없음 (정본 `jung2019_…` 은 다른 논문) |
| 8 | Ruess, R.; Schweidler, S.; Hemmelmann, H.; Conforto, G.; Bielefeld, A.; Weber, D. A.; Sann, J.; Elm, M. T.; Janek, J. Influence of NCM Particle Cracking on Kinetics of Lithium-Ion Batteries with Liquid or Solid Electrolyte. J. Electrochem. Soc. 2020, 167, 100532. | PC 균열 · ASSB 에서 새 표면이 젖지 않음 — 카드 없음 |
| 9 | Yamamoto, M.; Takahashi, M.; Terauchi, Y.; Kobayashi, Y.; Ikeda, S.; Sakuda, A. Fabrication of Composite Positive Electrode Sheet with High Active Material Content and Effect of Fabrication Pressure for All-Solid-State Battery. J. Ceram. Soc. Jpn. 2017, 125, 391−395. | 제조 압력 ↔ 복합 양극 기공 (>100 MPa 문장의 근거) — 카드 없음 · ★ 압력별 기공 원전 후보 |
| 14 | Koerver, R.; Zhang, W.; De Biasi, L.; Schweidler, S.; Kondrakov, A. O.; Kolling, S.; Brezesinski, T.; Hartmann, P.; Zeier, W. G.; Janek, J. Chemo-Mechanical Expansion of Lithium Electrode Materials −on the Route to Mechanically Optimized All-Solid-State Batteries. Energy Environ. Sci. 2018, 11, 2142−2158. | 전극 부피 변화 (LTO 0.2 %) — 카드 없음 |
| 15 | Liu, X.; Zheng, B.; Zhao, J.; Zhao, W.; Liang, Z.; Su, Y.; Xie, C.; Zhou, K.; Xiang, Y.; Zhu, J.; et al. Electrochemo-Mechanical Effects on Structural Integrity of Ni-Rich Cathodes with Different Microstructures in All Solid-State Batteries. Adv. Energy Mater. 2021, 11, 2003583. | SC ↔ PC 구조 안정 (25 MPa 187 mAh g⁻¹) — 카드 없음 |
| 17 | Kim, K. J.; Balaish, M.; Wadaguchi, M.; Kong, L.; Rupp, J. L. M. Solid-State Li−Metal Batteries: Challenges and Horizons of Oxide and Sulfide Solid Electrolytes and Their Interfaces. Adv. Energy Mater. 2021, 11, 2002689. | LiNbO₃ 코팅 근거 — 카드 = `kim2021_review_oxide_sulfide_se_interfaces` |
| 18 | Shi, T.; Tu, Q.; Tian, Y.; Xiao, Y.; Miara, L. J.; Kononova, O.; Ceder, G. High Active Material Loading in All-Solid-State Battery Electrode via Particle Size Optimization. Adv. Energy Mater. 2020, 10, 1902881. | 입경비 ≥ 1 — 카드 = `shi2019_high_am_loading_particle_size_assb` |
| 27 | Li, P.; Zhao, Y.; Shen, Y.; Bo, S.-H. Fracture Behavior in Battery Materials. J. Phys.: Energy 2020, 2, 022002. | 큰 1차 입자의 입계 균열 — 카드 없음 |
| 28 | Doux, J. M.; Nguyen, H.; Tan, D. H. S.; Banerjee, A.; Wang, X.; Wu, E. A.; Jo, C.; Yang, H.; Meng, Y. S. Stack Pressure Considerations for Room-Temperature All-Solid-State Lithium Metal Batteries. Adv. Energy Mater. 2020, 10, 1903253. | 적층압 25 MPa Li 침투 — 카드 = `doux2020_stack_pressure_assb` |
| 30 | Bielefeld, A.; Weber, D. A.; Janek, J. Modeling Effective Ionic Conductivity and Binder Influence in Composite Cathodes for All-Solid-State Batteries. ACS Appl. Mater. Interfaces 2020, 12, 12821−12833. | 미세구조 최적화 — 카드 = `bielefeld2020_effective_ionic_conductivity_binder` |
| 31 | Han, Y.; Jung, S. H.; Kwak, H.; Jun, S.; Kwak, H. H.; Lee, J. H.; Hong, S. T.; Jung, Y. S. Single- or Poly-Crystalline Ni-Rich Layered Cathode, Sulfide or Halide Solid Electrolyte: Which Will be the Winners for All-Solid-State Batteries? Adv. Energy Mater. 2021, 11, 2100126. | SC-NCA (Fig. 5d) · SC ↔ PC — 카드 없음 |
| 32 | Doux, J.-M.; Yang, Y.; Tan, D. H. S.; Nguyen, H.; Wu, E. A.; Wang, X.; Banerjee, A.; Meng, Y. S. Pressure Effects on Sulfide Electrolytes for All Solid-State Batteries. J. Mater. Chem. A 2020, 8, 5049−5055. | 황화물 SE 압력 효과 (Fig. 5d NCA) — 카드 없음 (다른 정본 카드들이 인용) |

## 12. [미확인] 목록 (원문 본문 + SI 전수에 없음)
1. 상대밀도 (단결정 ≈ 90 % · 다결정 78 / 82 / 86 % · 순수 LPSCl Fig. 1e) 의 **측정법 · 이론밀도 · 성분 밀도 · 반복 수**.
2. 압밀 **유지 시간 · 가압 속도 · 하중 제거 방식** · 분리막과 양극을 따로 누르는지 여부 (문장은 함께로 읽힌다).
3. vol% 조성 · 양극 두께 (14 mg cm⁻² 셀) · 다결정 셀의 조성 확인 (*"identical processing"* 뿐).
4. 공급사 (SC-NMC · PC-NMC · LPSCl-LP) · LiNbO₃ 코팅 두께.
5. 순수 LPSCl σ · 밀도 시료의 질량 · 지름 · 두께와 그 측정 (하중 아래인지) · σ 와 밀도의 압력 세트가 다른 이유.
6. FEM 의 물성 · 마찰 계수 · 요소 · 펠릿 치수.
7. 오차막대의 뜻 · 셀 수 (SI Fig. S12a) · 다른 그림의 반복.
8. "> 500 MPa = LPSCl 입자 균열" 의 직접 근거 (단면 영상).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-10)
- 본문 7 쪽 · SI 14 쪽을 글자 층 추출 + 렌더로 읽음.  서지 = PDF 1 쪽 (제목 · 저자 · Cite This 줄 · 접수 / 승인 / 출판 날짜 · © 줄) + 쪽 머리글 · 바닥글 (*ACS Appl. Mater. Interfaces 2021, 13, 37809−37815* · DOI).
- 그림 크롭 **29 장** = 자동 21 (본문 Fig. 1–5 · SI Fig. S1–S13 · SI Table S1–S3) 중 **3 장 다시 자름** (fig_S1 = 위 본문 한 줄 · fig_S3 = 위 Table S2 · fig_S5 = 그림 위쪽 절반이 잘림) · 캡션 정리 2 (f3 쪽 바닥글 · f5 본문 문단) + **손 크롭 8** (graphical abstract · SI Table S4 (도구가 '영역 없음') · 근거 문단 본문 5 + SI 1) — `figures.json` 의 `recrop` · `manual_crop` · `caption_fix`.  29 장 전부 열어 확인 (축 · 범례 · 이웃 문단 혼입 없음).
- 판독: 두 PDF 의 그림이 벡터라 표지 · 곡선 경로 좌표를 눈금 선에 보정 — Fig. 1b 25 점 · 1e 20 점 · 3a / 5c / S9a 곡선 끝 · 4a / 4b / 5b inset · 4c / S9c 58 사이클 · 5d 8 표지 · S5 8 계열 (범례 표본으로 식별 · inset 뒤 가려진 점 제외) · S8b 20 점 · S10 극소 · 극대 · S12a 5 점 + 오차막대 · S12b 곡선.  인쇄값 재현: Fig. 3a CE 84.4 (본문 85) · S9a 70.3 (≈ 70) · 5c 87.4 (범례 87.3) · 4c 50 사이클 96.3 (본문 96.3) · S9c 92.4 (본문 92.4) · S10 호 폭 37.1 (본문 ≈ 40).
- 카드 산술은 전부 본문에 식을 적었다 (NMC 결정 밀도 · vol% · 면적 질량 · 두께 · 분리막 두께 · σ × R·A · 격자 부피 · 기공 = 1 − d).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 + DOI · 제목 낱말 · 저자 이름 전수 grep — 이 논문 카드 없음 (다른 카드 둘에 저자 이름 · 인용으로만 나온다).

## 13. ★ 고른 의도 대조 — N-28 · Tron 2023 참고 [13] 의 2차 인용 (2026-11-12 보탬)

> 계기: 정독 종합의 논문 에이전트 후보 표 N-28.  정본 `tron2023_rational_cathode_composite_optimization_lpscl` (L48 · L128) 이 참고 [13] 을 번호로만 적어 서지를 몰랐다.  **1저자가 Tron 원문 참고문헌 목록에서 [13] = 이 논문 (*"High energy density single-crystal NMC/Li6PS5Cl cathodes for all-solid-state lithium-metal batteries"*) 이라고 확인했다 (2026-11-12).**  Tron 원문 목록은 이 보탬이 직접 보지 못했다 (Tron 카드에 참고문헌 목록 · 크롭이 없고, 원문 사이트가 이 세션 네트워크에서 막힘).
> 고른 의도 (후보 표 '왜' · 질문 d · i): *"AM 끼리 닿아 치밀화가 막힌다는 주장의 측정 근거가 있는지"* — Tron 이 [13] 을 든 자리 둘을 이 논문 원문 (본문 + SI PDF 글자 층 · 2026-11-12 다시 확인) 과 대조했다.

| Tron 카드의 2차 인용 (줄) | 이 논문 원문 | 대조 | 위치 · 조건 |
|---|---|---|---|
| L128 (Tron p.9): *"When less electrolyte is added, the NMC811 particles come in contact with each other, and densification is inhibited"* [13] | p.2–3: *"However, once the PC-NMC particles contact one another, relative motion is inhibited and it is difficult to induce any further shearing of the LPSCl, and the PC agglomerates may start to crack."* · SI Fig. S7 표지 *"Contact between large PC-NMC particles"* · *"Restricted movement for SSE particles"* · *"High porosity in SSE"* | **일부** | ① 원문이 "inhibited" 라고 쓴 것은 **상대 운동** 이다 — *"densification is inhibited"* 라는 문장은 원문에 없다.  치밀화와 닿는 말은 SI Fig. S7 모식 표지 *"High porosity in SSE"* 뿐 ② **정성 가설 · 모식도** — 접촉 수 · 응력 · 변위를 잰 것이 아니다 (§10 12 번) ③ 원문의 축은 **AM 형태 (PC ↔ SC) · 조성 70 wt% 고정** 이다 — Tron 이 쓴 맥락 (**AM:SE 비 · 전해질을 덜 넣을 때**) 은 원문에 없다 (조성 축 없음 · §0 ④) ④ "NMC811" 은 맞다 — 원문 PC 대조 = *"similar LiNi0.8Mn0.1Co0.1O2 powder but with PC-NMC"* (p.2) ⑤ 곁에 놓을 수 있는 숫자 (측정 근거로 쓸 수 있는 최대): 같은 500 MPa 에서 **PC 0.86 (*"estimated"* · SI Fig. S6 캡션) ↔ SC ≈ 0.90 (단면 SEM 문장 안 · p.2)** · PC 는 낮은 압력에서 기공 *"from ∼14 to ∼22%"* (p.3 · SI Fig. S6) — 하중 뺀 뒤 · 측정법 · 분모 미기재 · 반복 수 [미확인] · PC ↔ SC 는 입경 (D50 5.9 ↔ 3.4 µm) 과 형태가 함께 다르다 |
| L48 (Tron p.1–2): *"C65 가 최선 [13,20,25,26]"* (Tron 카드의 요약 — Tron 원문 문장은 카드에 없어 [미확인]) | p.2: *"Carbon black (Super C65, 2.5 wt %) was used in all the cathodes as an electron conductivity aid."* · EDX: *"suggested an acceptable, typical distribution of carbon black to support electron percolation"* (p.2) | **없음** ("최선" 의 근거) | 원문은 C65 **하나만** 쓴다 — 다른 도전재와 견준 실험 · 문장이 없다.  [13] 은 "C65 를 쓴 문헌" 으로만 맞다 |

- **2차 인용 값 대조**: Tron 카드의 두 줄에 이 논문의 숫자는 없다 → 숫자 어긋남 0 건.  어긋남은 **말의 범위** 둘이다 — ① 상대 운동 정지 (PC ↔ SC · 조성 고정) → "치밀화가 막힌다 (AM:SE 비)" ② C65 사용 → "C65 가 최선".  Tron 카드 본문은 고치지 않는다 (카드 문제로 보고 · 그 카드 '관련 카드' 절에 이 절을 가리키는 한 줄만 더했다).
- **우리 계획에 주는 것**: 바뀌지 않는다 — §8 의 3 번 (AM–AM 접촉 = 전단 정지 · 파쇄 → 계산 관측량) 이 그대로 답이다.  "AM 이 서로 닿으면 치밀화가 막힌다" 를 우리 문서 (재설계 R1 · 단계 5) 에 쓰며 이 논문을 들 때는 **"정성 가설 (SI Fig. S7) + 같은 500 MPa 의 PC ↔ SC 밀도 한 쌍 (하중 뺀 뒤 · 측정법 · 분모 미기재)"** 한정어를 붙인다.  **AM:SE 비에 따른 치밀화 저하의 측정 근거로는 쓰지 않는다** (원문에 그 축이 없다) — 그 축은 Tron 자신의 AM:SE 비 계열 (Tron 카드 §3e · 전기화학 값 · 밀도 아님) 이나 다른 카드에서 찾는다.

## 🔗 관련 카드
- 이 논문을 인용한 정본 카드: [`tron2023_rational_cathode_composite_optimization_lpscl`](tron2023_rational_cathode_composite_optimization_lpscl.md) (참고 [13] · 그 카드 L48 · L128 의 인용 대조 = 위 §13).
- 복합 양극 압밀 · 기공: `minnmann2021_jes_charge_transport_bottlenecks` · `minnmann2024_microstructure_porosity_visualization` · `kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact` · `wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode` · `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` · `bazzoun2026_dem_fem_rnm_ionic`.
- SC ↔ PC · 입경: `jung2023_single_crystal_ncm_morphology` · `shi2019_high_am_loading_particle_size_assb` · `stallard2022_cathode_mechanical_properties_review`.
- 순수 LPSCl 압밀: `var2026_sulfide_se_mechanical_properties_local_indentation_pellet` (§7-2 표) · `ketter2025_resistor_network_models_predict_transport_properties` · `doux2020_stack_pressure_assb`.
- 강체 + 무른 입자 압밀 (재설계 유비): `cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd` · `bouvard2000_hard_soft_powder_densification`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
