<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 이웃 = faka2026_particle_size_consolidation_strain_lpscl.md · 같은 묶음 = johnson1971_jkr_surface_energy_contact_elastic_solids.md · begat2004_cohesive_adhesive_balance_afm_colloid_probe.md · mohammadijam2014_inverse_gas_chromatography_review.md.
     원문 = 11 쪽 (p.46–56) · SI 없음 · 쪽 표기 = 인쇄 쪽 (PDF n 쪽 = p.(45 + n)).
     태생 디지털 PDF — SEM · 사진 그림은 300 ppi 내장 이미지, Fig 7–9 · 11–13 은 벡터 도표.  크롭은 전부 캡션까지 300 dpi.
     값 표지: [인쇄] = 본문 · 표 · 그림 안 인쇄 숫자 / [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv — 벡터 도표는 PDF 경로 좌표, 막대는 래스터) /
     [우리 산술] = 원문 값으로 한 계산 / [추정] = 우리 해석 / [미확인] = 원문에 없음. -->
# A study of particle adhesion for cohesive powders using a novel mechanical surface energy tester — 분말 단층 (≤ 20 mg) 을 ⌀40 mm 원판에 뿌려 떨어뜨리고, 멈출 때의 **감속도**와 그때 **떨어져 나간 질량 분율**을 잰다 · "Bond 수" = 50 % 가 떨어지는 감속도의 g 배수 (+1) · γ^d (FD-IGC, Schultz) 로 JKR/DMT 와 대조 — Deng · Garg · Bradley (Powder Technology 2021)

> slug `deng2021_mechanical_surface_energy_tester_bond_number` · DOI `10.1016/j.powtec.2021.06.002` · type `experiment (drop-impact detachment "mechanical surface energy tester" for cohesive powders · 15 pharmaceutical/mineral powders on powder tablets and 4 standard substrates · granular Bond number Bo = F_ad/mg · FD-IGC dispersive surface energy (Schultz) · JKR/DMT comparison)` · PDF `3065876f-45._A_study_of_particle_adhesion_for_cohesive_powders_using_a_novel_mechanical_surface_energy_tester.pdf` · digested `2026-10-13` · status ✅
>
> **서지 (원문 인쇄)**: Tong Deng\* · Vivek Garg · Michael S.A. Bradley — Wolfson Centre for Bulk Solids Handling Technology, Faculty of Engineering & Science, University of Greenwich, Chatham, UK · \* 교신 (t.deng@gre.ac.uk) · *Powder Technology* **391** (2021) 46–56 · 접수 2021-05-19 · 수정 2021-06-03 · 승인 2021-06-05 · 온라인 2021-06-08 · https://doi.org/10.1016/j.powtec.2021.06.002 · 0032-5910/© 2021 Elsevier B.V. [인쇄 p.46].  PDF 메타의 DOI 도 같다.
> 핵심어 (원문): Particle adhesion · Bond number · Cohesive powders · Surface energy tester.  장치 원전 = ref [11] (Ermis 2011 Greenwich 박사논문) — 받지 않았다 [미확인].
> ★ **이 카드가 맡는 일** — 이종기술 논지 (`docs/hetero_thesis.md`) §2-8 · D3 (SE–SE 점착 앵커) 의 **측정법 후보 하나를 판정**한다: 이 장치가 재는 양은 무엇인가 · 우리 Bond 수 (Bo_code · Bo_po) · CED 와 같은 양인가 · γ_A/γ_S < 0.31 질문에 답할 수 있는가.
> **판독 원자료**: `litdb/figures/deng2021_mechanical_surface_energy_tester_bond_number/digitized.csv` (162 행 — Fig 7 벡터 점 76 + 50 % 보간 15 · Fig 12 벡터 30 · Fig 13 벡터 30 (MCC JKR 빈 칸 1 포함) · Fig 10 막대 11).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 이 장치는 입자 하나의 점착력을 재지 않는다 — 재는 것은 **원판이 받침에 부딪혀 멈출 때의 감속도 a** 와 그때 **떨어진 질량 분율** 이고, "점착력" 과 "Bond 수" 는 50 % 가 떨어지는 감속도 a₅₀ 에 **공급 분말 D50 의 구 한 개 질량**을 곱해 **계산**한 값이다 [인쇄 p.48 · 52 · 54].  Table 2 의 Bond 수 15 개는 전부 **1 + a₅₀/g** 와 ±0.01 안에서 같다 [우리 산술] — 크기 · 밀도 · 점착 법칙이 하나도 들어가지 않은 감속도의 g 배수다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ★ 무엇을 재나 | 1 차 측정량 = **감속도 a (m/s²)** (가속도계) 와 **떨어진 질량 / 증착 질량 (% w/w)** (저울 0.1 mg).  점착력 F_ad = m·a (식 6) · Bo = F_ad/mg (식 2) 는 **계산값** — m = 공급 분말 D50 구 한 개 (Table 1 밀도).  γ · W · 떼는 힘 한 쌍은 이 장치로 재지 않는다 (γ^d 는 따로 FD-IGC) | [인쇄] p.47–48 · 52 · 54 |
| ★ Bo 의 실체 | Table 2: Eskal 2 a₅₀ 98.24 → Bo 11.01 = 1 + 98.24/9.81 · Lactose 230 56.26 → 6.73 = 1 + 56.26/9.81 · 15/15 행이 같은 식 (끝자리 ±0.01) — **m 이 약분**돼 Bo 는 a₅₀ 만의 함수.  식 (6) 은 F = −ma 로 g 가 없는데 표는 m(a + g) 로 계산했다 — 입자가 판 **아래**에 매달린 배치 (Fig 1 · 2) 라 관성 + 무게가 같은 방향 [추정] | [인쇄] Table 2 · 식 (6) + [우리 산술] |
| 측정 창 | 실험한 감속도 단계 43–105 m/s² (Fig 7 · 9 · 11 벡터) → Bo 는 구조상 **≈ 5.4–11.7** 밖으로 못 나간다 · 실측 5.89–11.01.  같은 논문의 γ^d 로 JKR (매끈한 구 · 평판, W = γ) Bo 를 계산하면 **245 (Lactose 230) – 2.2×10⁶ (Eskal 2)** — 장치 값은 그 **5×10⁻⁶ – 0.03 배** | [판독 벡터] · [우리 산술] |
| ★ 기판 효과 | 같은 분말 정제 · 스테인리스 · TIVAR-88 · 유리 · 연강 — 유당 4 종 × 8 기판 점착력 변동 **최대 ≈ 2.5 % · 나머지 1.5–1.7 %** → 저자: "the substrate material has little influence" · "particle adhesion … is more likely subject to the particle properties and the particle deposition status on the surface, rather than the surface materials" | [인쇄] p.46 · 53 · Fig 10 |
| 시료 조건 | 증착 **≤ 20 mg** (단층 — 무작위 SEM 으로 확인) · 기판 ⌀40 mm (같은 분말 수 g 으로 만든 정제 또는 표준재) · 공기 분산기 (Malvern G3 부속) **1.5 bar** · 4 시료 동시 · 상온 · **RH 40–60 %** · FD-IGC 는 건조 분말 **≈ 1.2 g** (유리관 300 mm × 내경 4 mm · 건조 He 10 ml/min) | [인쇄] p.48 · 50 · 55 |
| 불확도 | a₅₀ 의 ± 0.43–7.95 m/s² (평균의 0.8–10 %) · γ^d ± 2–5 mJ/m² (3–12 %) · 가속도계 허용차 ±1.5 dB = 진폭 **−16 / +19 %** [우리 산술] — 기판 변동 2.5 % 는 반복성이지 정확도가 아니다 · 반복 횟수 [미확인] | [인쇄] Table 2 · 3 · p.48 + [우리 산술] |
| ★ γ^d (FD-IGC, Schultz) | CaCO₃ **54 ± 4** · 유당 **44 ± 4** · TiO₂ **58 ± 2** · 파라세타몰 **44 ± 2** · 이부프로펜 **42 ± 5** · MCC **42 ± 3** mJ/m² — 분산 성분만 · 덮임률 · 온도 [미확인] · 같은 물질이면 크기와 무관하다고 보고 물질당 한 값 | [인쇄] Table 3 · p.55 |
| ★ JKR/DMT 대조 | Fig 13 의 모형값은 (3/2)π·(D50/2)·γ 와 2π·(D50/2)·γ 에 **D50 을 µm · γ 를 J/m² 로 넣은 수** — 그 곱의 단위는 µN 인데 축은 nN (벡터 좌표로 3–4 자리 일치) → 모형값이 **10³ 배 작게** 그려졌다.  단위를 바로 하면 JKR 이 장치값보다 **36 배 (Lactose 230) – 2×10⁵ 배 (Eskal 2) 크다** — 원문 결론 ("measured … a power of 3 more significant than that the models give") 과 **방향이 반대** · 맞춘 지수 0.330 ≈ 1/3 은 D³ (장치) 대 D (모형) 의 산물 · R² 0.997 은 둘 다 D50 의 함수라서 | [판독 벡터] · [인쇄] p.55 + [우리 산술] |
| 기하평균 결합 규칙 | 원문은 다루지 않는다 (다른 물질 쌍 W 계산 · 시험 없음).  같은 물질 쌍에 γ^d 를 그대로 W_A 로 넣었다 — JKR 원정의로는 같은 물질 W = 2γ (johnson1971 카드) | [인쇄] p.55 + [우리 산술] |
| 공기 민감 황화물 | 원문 밖 — 대기 · RH 40–60 % · 공기 분산 · Au/Pd 코팅 SEM.  낙하 · 감속도 · 질량이라는 원리는 글로브박스에 들어갈 크기다 [추정].  FD-IGC 는 mohammadijam2014 카드 §7-2 의 위험 (극성 탐침 반응 · 칼럼 충전) 그대로 | [인쇄] p.48–51 + [추정] |
| ★ 논지 판가름 (γ_A/γ_S < 0.31) · Bo · CED | **판가름 측정으로 못 쓴다** — 기판 (A 냐 S 냐) 에 눈먼 측정이고 (≤ 2.5 %), Bo 는 장치 창에 묶였다.  얻는 것 = ① 화학이 다른 6 분말의 γ^d 가 **42–58 mJ/m² 좁은 띠** (§7-2) ② DEM 으로 1:1 흉내 낼 수 있는 **낙하 탈착 실험 형식** (§7-3) | [추정] |

⛔ **한정어 (떼지 말 것)**: ① 의약 · 광물 분말 (CaCO₃ · 유당 · MCC · 파라세타몰 · 이부프로펜 · TiO₂) — 배터리 소재 아님 ② 대기 · **RH 40–60 %** (모세관 힘 미분리) ③ 점착력 · Bo 는 a₅₀ 에서 **계산한** 값 — 1 차 입자 점착의 측정이 아니다 ④ 반복 횟수 · 가속도 파형 (피크 · RMS) · 충격 시간 [미확인] ⑤ 숫자 · 단위 · 크기 기준 불일치 여럿 (§10).

---

## 1. 한 줄 요약
제약 공정에서 분말 흐름 · 혼합 균일성과 묶이는 "입자 점착" 을 벌크 시료 수준에서 재려고, Greenwich Wolfson Centre 가 만든 작은 낙하식 "기계적 표면 에너지 시험기" 로 15 분말 (탄산칼슘 4 등급 · 유당 4 · 이부프로펜 4 · MCC · 파라세타몰 · TiO₂) 을 시험했다.
분말을 원판에 단층으로 뿌리고 (≤ 20 mg) 시료대를 여러 높이에서 떨어뜨려 받침에서 멈추게 하면 일부가 떨어진다 — 떨어진 질량 분율을 감속도에 대해 그려 (Fig 7) 50 % 탈착 감속도를 Bond 수로 바꾼다 (Table 2).  기판을 같은 분말 정제에서 스테인리스 · TIVAR-88 · 유리 · 연강으로 바꿔도 값이 1.5–2.5 % 만 변한다 (Fig 10) 고 보고, FD-IGC γ^d 로 계산한 JKR · DMT 값과 R² 0.99 의 상관을 보인다 (Fig 13).  큰 입자의 점착력이 크게 나오는 것은 응집성과 맞지 않으므로, Bond 수가 응집성 지표로 낫다고 결론짓는다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| T. Deng\* · V. Garg · M. S. A. Bradley (Univ. Greenwich, Wolfson Centre for Bulk Solids Handling Technology) | Powder Technol. **391** 46–56 (2021) | 10.1016/j.powtec.2021.06.002 | 탄산칼슘 Eskal 2 · 4 · 10 · 15 (KSL Staubtechnik) · 유당 70 · 140 · 200 · 230 (MEGGLE) · 이부프로펜 · 25 · 50 · 50 제트밀 (BASF) · MCC (KP Snacks) · 파라세타몰 (AstraZeneca) · TiO₂ (MegaChem) — 배터리 소재 아님 | 실험 (낙하 충격 탈착 · 레이저 회절 PSD · 질소 비중병 밀도 · SEM · FD-IGC) + 해석 대조 (JKR · DMT) |

| 원문 구조 | 쪽 | 내용 |
|---|---|---|
| 초록 · 1 Introduction | 46–47 | AFM · 원심법의 한계 · 벌크 거동과의 연결 · Bond 수 |
| 2 Theory and apparatus | 47–48 | 식 (1)–(5) 점착 이론 · 식 (2) Bo · 2.3 장치 (Fig 2) · 식 (6) |
| 3 Experimental methodology | 48–51 | 분말 (Table 1 · Fig 3) · 기판 (Fig 4–5) · 절차 · SEM (Fig 6) |
| 4 Results and discussion | 51–55 | 4.1 정제 기판 (Fig 7–8) · 4.2 표준 기판 (Fig 9–11) · 4.3 점착력 · Bo (Table 2 · Fig 12) · 4.4 JKR/DMT (Table 3 · Fig 13) |
| 5 Conclusions · 감사 · 참고문헌 (24) | 55–56 | 요약 1)–5) · EPSRC EP/P006965/1 · Imperial College 가 표면 에너지 자료 제공 |

- 중복 확인 (2026-10-13): 정본 `litdb/papers/` 전수 목록에 같은 논문 없음 (deng 접두 3 장은 SE DFT · 황산염 층 카드) · `git grep -i` "powtec.2021.06.002" · "surface energy tester" 0 건 → 새 카드.

---

## 3. 핵심 수치 (★ 쪽 · 표지 병기)

### 3-1. 분말 (Table 1) [인쇄 p.48] + span 검산 [우리 산술]
레이저 회절 (부피 %) · 고체 밀도 = 질소 비중병 [인쇄 p.49].

| 분말 | D10 (µm) | D50 | D90 | span (인쇄) | (D90−D10)/D50 [우리 산술] | 밀도 (kg/m³) |
|---|---:|---:|---:|---:|---:|---:|
| Eskal 2 (CaCO₃) | 1.1 | 2.0 | 34 | 16.47 | 16.45 | 2800 |
| Eskal 4 | 2.0 | 4.0 | 13 | 2.76 | 2.75 | 2800 |
| Eskal 10 | 5.5 | 10 | 17.7 | **5.54** | **1.22** | 2800 |
| Eskal 15 | 9.6 | 15 | 26.1 | **9.63** | **1.10** | 2800 |
| Ibuprofen | 22.4 | 70 | 174.7 | 2.18 | 2.18 | 1118 |
| Ibuprofen 25 | 2.6 | 13 | 33.5 | 2.37 | 2.38 | 1132 |
| Ibuprofen 50 | 5.3 | 26 | 75.8 | 2.71 | 2.71 | 1110 |
| Ibuprofen 50_Jet milled | 1.3 | 4.0 | 9.0 | 1.92 | 1.93 | 1113 |
| Lactose 140 | 31 | 150 | 244 | 1.42 | 1.42 | 1558 |
| Lactose 200 | 48 | 200 | 330 | 1.41 | 1.41 | 1558 |
| Lactose 230 | 61 | 230 | 380 | 1.39 | 1.39 | 1558 |
| Lactose 70 | 19.3 | 90 | 118.6 | 1.10 | 1.10 | 1558 |
| Microcrystalline Cellulose | 8.3 | 22.7 | 45.7 | 1.65 | 1.65 | 1590 |
| Paracetamol | 8.0 | 49 | 97 | 1.82 | 1.82 | 1280 |
| Titanium Dioxide | 2.0 | 68 | 84 | 1.21 | 1.21 | 4475 |

- 13/15 행은 span 식과 맞고, **Eskal 10 · 15 의 인쇄 span (5.54 · 9.63) 은 식 (1.22 · 1.10) 과 다르다** — 각 행 D10 (5.5 · 9.6) 과 비슷한 숫자라 칸 밀림으로 보인다 [추정].
- ⚠ Eskal 2 는 D50 2.0 µm 인데 D90 34 µm — 부피 기준 질량의 대부분이 큰 입자 · 응집체에 있다 (Fig 3a 의 응집체) [인쇄 · 추정].

### 3-2. ★ Bond 수 (Table 2) [인쇄 p.54] — 검산 [우리 산술]
F_입자 = (π/6)·ρ·D50³·(a₅₀ + g) (g = 9.81) — Fig 8 · 12 · 13 의 "measured" 점착력과 같은 값 (§3-5 벡터 대조).  JKR (SI) = (3/2)π·(D50/2)·γ^d (원문과 같은 W = γ 가정).

| 분말 | D50 (µm) | a₅₀ ± (m/s²) [인쇄] | Bo [인쇄] | 1 + a₅₀/g | F_입자 (nN) | γ^d (mJ/m²) [인쇄 Table 3] | JKR (nN, SI) | Bo_JKR = JKR/mg |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Eskal 2 | 2.0 | 98.24 ± 1.06 | 11.01 | 11.01 | 1.27×10⁻³ | 54 | 254 | 2.2×10⁶ |
| Eskal 4 | 4.0 | 75.03 ± 1.78 | 8.65 | 8.65 | 7.96×10⁻³ | 54 | 509 | 5.5×10⁵ |
| Eskal 10 | 10 | 53.13 ± 1.95 | 6.41 | 6.42 | 0.0923 | 54 | 1272 | 8.9×10⁴ |
| Eskal 15 | 15 | 50.45 ± 2.55 | 6.14 | 6.14 | 0.298 | 54 | 1909 | 3.9×10⁴ |
| Lactose 70 | 90 | 85.23 ± 2.63 | 9.69 | 9.69 | 56.5 | 44 | 9331 | 1.6×10³ |
| Lactose 140 | 150 | 76.49 ± 7.95 | 8.80 | 8.80 | 238 | 44 | 1.56×10⁴ | 576 |
| Lactose 200 | 200 | 59.98 ± 1.93 | 7.11 | 7.11 | 456 | 44 | 2.07×10⁴ | 324 |
| Lactose 230 | 230 | 56.26 ± 0.43 | 6.73 | 6.73 | 656 | 44 | 2.38×10⁴ | 245 |
| Titanium dioxide | 68 | 89.44 ± 1.01 | 10.12 | 10.12 | 73.1 | 58 | 9293 | 1.3×10³ |
| Paracetamol | 49 | 89.46 ± 1.95 | 10.12 | 10.12 | 7.83 | 44 | 5080 | 6.6×10³ |
| Ibuprofen | 70 | 88.04 ± 1.44 | 9.97 | 9.97 | 19.6 | 42 | 6927 | 3.5×10³ |
| Ibuprofen 25 | 13 | 60.62 ± 0.75 | 7.18 | 7.18 | 0.0917 | 42 | 1286 | 1.0×10⁵ |
| Ibuprofen 50 | 26 | 54.61 ± 0.47 | 6.57 | 6.57 | 0.658 | 42 | 2573 | 2.6×10⁴ |
| Ibuprofen 50_Jet milled | 4.0 | 70.11 ± 5.03 | 8.15 | 8.15 | 2.98×10⁻³ | 42 | 396 | 1.1×10⁶ |
| MCC | 22.7 | 48.02 ± 0.48 | 5.89 | 5.90 | 0.563 (그림은 4.60 — §3-5) | 42 | 2246 | 2.3×10⁴ |

- ⇒ **Bo (인쇄) = 1 + a₅₀/g** 가 15/15 (Eskal 10 · MCC 는 끝자리 반올림 차) [우리 산술].  Bo 에 D50 · ρ 가 들어가지 않는다 — **크기가 다른 분말의 Bo 차이 = 50 % 탈착 감속도의 차이**일 뿐이다.
- ⇒ Table 2 의 D50 15 개가 **Table 1 의 공급 분말 D50 과 전부 같다** — 본문 (p.52) 의 "the size is calculated using the detached particles" 와 맞지 않는다 [인쇄 대조].
- ⇒ 매끈한 구 JKR 로는 Bo 가 크기에 따라 **10²–10⁶** (∝ 1/D²) 이어야 하는데, 장치 Bo 는 D50 2 → 230 µm (115 배) 에서 11.0 → 6.7 (1.6 배) 로만 움직인다 [우리 산술].  같은 계열 안에서도 Eskal 2 → 15 (7.5 배) 에 1.8 배 · 유당 90 → 230 µm (2.6 배) 에 1.44 배 (1/D² 이면 56 배 · 6.5 배).

### 3-3. ★ 표면 에너지 (Table 3, FD-IGC · Schultz γ^d) [인쇄 p.54–55] + 다른 방법과 [우리 산술]
| 물질 | γ^d (mJ/m²) [인쇄] | 같은 물질 · 다른 방법 (정본 카드) | 비 |
|---|---:|---|---|
| 탄산칼슘 | 54 ± 4 | — | — |
| 유당 | 44 ± 4 | — | — |
| TiO₂ | 58 ± 2 (결정형 [미확인]) | Fowkes 1964: 루틸 139–148 · 아나타제 89–92 (`fowkes1964_attractive_forces_interfaces_dispersion`) | Deng/Fowkes = 0.39–0.42 (루틸) · 0.63–0.65 (아나타제) [우리 산술] |
| 파라세타몰 | 44 ± 2 | — | — |
| 이부프로펜 (4 등급 공통) | 42 ± 5 | — | 제트밀 등급도 같은 값을 씀 (§10) |
| MCC | 42 ± 3 | — | — |
| (참고) 석영 | — | IGC 리뷰: 52.76 (Schultz, 5 % 덮임) (`mohammadijam2014_inverse_gas_chromatography_review`) | 같은 띠 |

- ★ 6 물질의 γ^d 가 **42–58 mJ/m²** — 산화물 (TiO₂) 과 유기 결정의 비가 **0.72–0.76** (가장 큰 비대칭) [우리 산술].
- 측정: SMS 사 FD-IGC · 건조 분말 ≈ 1.2 g · 유리관 300 mm × 내경 4 mm · 양 끝 유리솜 · 두드려 빈틈 제거 · n-알칸 + 극성 탐침 · 건조 He 10 ml/min · Schultz 법 [인쇄 p.55].  ⚠ 덮임률 · 온도 · 탐침 목록 · 사전 건조 조건 [미확인] · Schultz 법의 인용 [24] 은 만니톨 유동성 논문 (§10).

### 3-4. ★ 탈착 곡선 (Fig 7, 정제 기판) [판독 — 벡터 좌표] + 50 % 보간 [우리 산술]
| 분말 | 감속도 단계 (m/s²) | 탈착 분율 범위 (% w/w) | a₅₀ 보간 [우리 산술] | a₅₀ Table 2 [인쇄] |
|---|---|---|---:|---:|
| Eskal 15 | 51 · 65 · 70 · 86 · 91 | 48.1–84.2 | 52.3 | 50.45 |
| Eskal 10 | 53 · 65 · 72 · 91 · 94 | 48.1–80.8 | 54.5 | 53.13 |
| Eskal 4 | 56 · 68 · 86 · 95 · 103 | 40.4–71.2 | 75.2 | 75.03 |
| Eskal 2 | 43 · 53 · 62 · 86 · 101 | 17.3–52.0 | 97.5 | 98.24 |
| Ibuprofen | 51 · 64 · 82 · 93 · 95 | 21.6–54.9 | 91.8 | 88.04 |
| Ibuprofen 25 | 43 · 53 · 62 · 94 · 101 | 39.0–76.1 | 61.2 | 60.62 |
| Ibuprofen 50 | 43 · 53 · 62 · 94 · 101 | 43.3–83.7 | 54.9 | 54.61 |
| Ibuprofen 50_Jet milled | 43 · 53 · 62 · 94 · 101 | 36.6–67.4 | 67.0 | 70.11 |
| Lactose 230 | 54 · 65 · 74 · 86 · 96 | 47.6–78.0 | 56.5 | 56.26 |
| Lactose 140 | 43 · 53 · 62 · 91 · 97 · 105 | 38.0–64.5 | 78.0 | 76.49 |
| Lactose 70 | 43 · 53 · 62 · 93 · 99 | 25.0–57.8 | 87.1 | 85.23 |
| Lactose 200 | 56 · 62 · 75 · 86 · 94 | 45.2–72.7 | 59.5 | 59.98 |
| MCC | 43 · 49 · 63 · 86 · 91 | 45.2–72.7 | 48.4 | 48.02 |
| Paracetamol | 59 · 68 · 87 · 95 · 96 | 21.7–54.9 | 94.1 | 89.46 |
| Titanium dioxide | 52 · 80 · 84 · 94 · 97 | 21.7–54.9 | 92.9 | 89.44 |

- 보간 a₅₀ 은 Table 2 와 −3.1 … +4.7 m/s² 안 — 표는 그림 곡선의 50 % 지점으로 보인다 (여러 번 반복의 평균 ± 이면 더 맞을 것) [추정].
- ★ 가장 작은 감속도 (43 m/s² ≈ 4.4 g) 에서 이미 **17–45 %** 가 떨어지고, 105 m/s² (≈ 10.7 g) 까지 **52–84 %** 에 머문다 — 모든 분말의 탈착 분포가 이 좁은 창 안에 놓인다.  1 차 입자 점착이라면 (§3-2 의 Bo_JKR 10²–10⁶) 이 창에서 거의 떨어지지 않아야 한다 [우리 산술 · 추정].
- ⚠ **Ibuprofen · Paracetamol · TiO₂ 세 계열의 다섯 y 값이 0.03 %p 안에서 같다** (21.7 · 25.5 · 33.7 · 52.0 · 54.9 %) — x (감속도) 만 다르다 [판독 벡터].  서로 다른 분말이 같은 탈착 분율 다섯 개를 냈다는 뜻이라 원자료 확인이 필요하다.
- 관찰: 76 개 y 값이 전부 ≈ 0.481 %p 격자 위에 놓인다 (y/0.4808 의 소수부 0.01–0.17) [우리 산술] — 저울 0.1 mg / 증착 ≈ 20.8 mg 의 양자화로 보인다 [추정].

### 3-5. ★ "점착력" 막대와 거듭제곱 (Fig 8 · 12) [판독 벡터 · 우리 산술]
- Fig 12 의 점 15 개 = §3-2 의 F_입자 와 1 % 안에서 같다 (로그축 판독 · 예: Lactose 230 659 ↔ 656 nN · Eskal 2 1.27×10⁻³ nN) — 그림의 "measured" 점착력은 **m(D50)·(a₅₀ + g) 계산값**이다.
- ★ 인쇄 거듭제곱 **y = 1E-04x^2.9149 (R² 0.9871)** [인쇄 Fig 12] — 지수 2.91 은 질량식의 D³ 에 Bo · 밀도의 약한 크기 의존 (합쳐 ≈ D^−0.09) 이 겹친 것이고, 계수 10⁻⁴ 는 (π/6)·ρ·(a + g) 를 nN · µm 로 쓴 크기 (밀도 1110–4475 kg/m³ · a + g 58–108 m/s² 이면 0.3–2.3×10⁻⁴) 와 같은 자릿수 [우리 산술] — **점착 물리가 아니라 정의**에서 나온 곡선이다.
- ⚠ **MCC 점은 D = 45.7 µm** (= Table 1 의 **D90**) 에 그려졌다 — Fig 8 의 "Size at D50" 점 · Fig 12 의 x · Fig 13 의 x (4.6 nN) 모두 [판독 벡터] ↔ Table 1 · 2 의 D50 = 22.7 µm.  45.7 µm 로 계산하면 F = 4.60 nN = 그림값 [우리 산술].
- 저자 해석: "Two trends for the Bond numbers … indicates that the surface energies of the particles cause the difference" [인쇄 p.54] — 두 화살표 무리 ([판독] 가파른 쪽 = D50 ≤ 46 µm 의 Eskal · 이부프로펜 25/50/제트밀 · MCC ↔ 완만한 쪽 = D50 ≥ 49 µm 의 파라세타몰 · TiO₂ · 이부프로펜 · 유당 · Eskal 2 는 어느 쪽인지 그림만으로 모호) 의 γ^d 가 겹친다 (42–54 ↔ 42–58, 이부프로펜은 양쪽) → **표면 에너지로 가를 근거가 Table 3 에 없다** [우리 대조] · 무리는 크기로 갈린다.

### 3-6. ★ 기판 효과 (Fig 9–11) [인쇄 · 판독]
| 유당 분말 | 8 기판 점착력 (nN) | 인쇄 변동 | 판독 · 산술 |
|---|---|---:|---|
| Lactose 230 | 5536 · 5491 · 5491 · 5513 · 5393 · **5174** · 5536 · 5476 (유당 70 · 140 · 200 · 230 정제 · 스테인리스 · **TIVAR-88** · 유리 · 연강) | 2.5 % | [판독 ±25] · 표본 표준편차/평균 **2.2 %** · TIVAR 가 평균보다 −5.1 % [우리 산술] |
| Lactose 200 | 3750–3940 | 1.7 % | [판독 ±40] |
| Lactose 140 | 2150–2240 | 1.5 % | [판독 ±40] |
| Lactose 70 | 520–560 | 1.6 % | [판독 ±40] |

- ⚠ **Fig 10 값이 같은 분말 · 같은 정제 기판의 Fig 8 값의 8.3–9.4 배** (Lactose 230: 5513 ↔ 656 · Lactose 200: ≈ 3800 ↔ 456 · Lactose 140: ≈ 2200 ↔ 238 · Lactose 70: ≈ 530 ↔ 56.5) [판독 · 우리 산술] — 캡션이 "at an average size of D50 in mass detached" 라 다른 크기 기준을 쓴 것으로 보인다 (F ∝ D³ 이면 탈착 입자 D50 ≈ 공급 D50 의 2.0–2.1 배) [추정] · 어느 크기인지 [미확인].
- Fig 9: 유당 4 종 × 5 기판 (정제 · 스테인리스 · TIVAR-88 · 유리 · 연강) — 감속도 43 · 53 · 62 · 86 · 91 m/s² 에서 크기별로 갈리고 기판별로는 겹친다 [판독].
- Fig 11: 이부프로펜 25 를 7 기판 (이부프로펜 25 · 50 · 50 제트밀 정제 + 연강 · 유리 · 스테인리스 · TIVAR) 에 — 50 % 탈착 ≈ 61 m/s² 에서 겹친다 → Table 2 의 60.62 [판독 · 인쇄].
- 기판 표면 거칠기 "0.1 mm to 0.6 μm" [인쇄 p.50 — 단위 오기로 보인다] · 기판들의 표면 에너지 [미확인].

### 3-7. ★ JKR/DMT 대조 (Fig 13) [판독 벡터 · 우리 산술]
| 분말 | 장치값 (nN, x) | JKR 그림값 | DMT 그림값 | (3/2)π(D50/2)γ — µm · J/m² 의 수 | JKR (SI, nN) |
|---|---:|---:|---:|---:|---:|
| Lactose 230 | 655.5 | 23.84 | 31.79 | 23.85 | 2.38×10⁴ |
| Lactose 200 | 455.3 | 20.73 | 27.64 | 20.73 | 2.07×10⁴ |
| Lactose 140 | 237.4 | 15.55 | 20.73 | 15.55 | 1.56×10⁴ |
| TiO₂ | 72.9 | 9.30 | 12.39 | 9.29 | 9293 |
| Lactose 70 | 56.4 | 9.33 | 12.44 | 9.33 | 9331 |
| Ibuprofen | 19.5 | 6.93 | 9.24 | 6.93 | 6927 |
| Paracetamol | 7.75 | 5.09 | 6.78 | 5.08 | 5080 |
| MCC | 4.49 | (점 없음) | 6.03 | 4.52 (D 45.7) | 2246 (D50 22.7) |

- ⇒ 그림의 모형값 = **D50 을 µm, γ 를 J/m² 로 넣은 수** (단위 µN) 를 nN 으로 표시 [우리 산술 — 3–4 자리 일치].  올바른 nN 값은 10³ 배 크다 → JKR/장치 = **36 (Lactose 230) – 2.0×10⁵ (Eskal 2)** [우리 산술].
- ⇒ 맞춘 곡선 **y = 2.6283x^0.3302 (JKR) · 3.5132x^0.3303 (DMT)** [인쇄 Fig 13] 의 계수 비 1.337 ≈ 4/3 (DMT/JKR = 2/1.5) · 지수 ≈ 1/3 = 모형 (∝ D) 대 장치 (∝ D³) [우리 산술].  본문의 "R² 0.993 for the DMT model" 은 그림의 DMT R² 0.9971 과 다르다 [인쇄 대조].
- ⇒ 본문 "a power of 3 more significant" (p.55 §4.4) 와 결론 "There is a three times difference in values" (p.55) 는 서로 다른 말이고, 단위를 바로 하면 둘 다 성립하지 않는다 [우리 산술 · 인쇄 대조].
- JKR 점이 14 개 · DMT 점이 15 개 — MCC 의 JKR 점이 없다 [판독 벡터].

---

## 4. ★ 방법 — 측정 사슬 · 식 · 입자 처리

### 4-1. 식 (원문 그대로 · 크롭 `eq_01_adhesion_sum.png` · `eq_02_bond_number.png` · `eq_03_05_vdw_dmt_jkr.png` · `eq_06_detachment.png`)
- (1) F_ad = F_vw + F_e + F_cf — 반데르발스 · 정전기 · 모세관 [인쇄 p.47]
- (2) B_o = F_ad / F_g = F_ad / mg — "at the size of d" (Fig 1) [인쇄 p.47]
- (3) F_ad = H_a·D\* / (12 z₀²) — z₀ 분리 거리 · H_a Hamaker 상수 · D\* 등가 지름 (평판이면 입자 지름) [인쇄 p.47]
- (4) F_ad = 2πR·W_A (DMT) · (5) F_ad = (3/2)πR·W_A (JKR) — R = 구–평판이면 입자 반경 · 두 구면 환산 반경 · W_A = "equilibrium work of adhesion" [인쇄 p.47]
- (6) F_ad = −F_de = −m·a — a = 탈착 감속도 · m = 떨어진 입자 질량 [인쇄 p.48]
- 원문 문장: Bo > 1 이어야 입자가 평판에 붙어 있으므로 "for any non-cohesive powders which particle adhesion could be less than its weight, the Bond number needs to be determined by other traditional methods" [인쇄 p.47] — **Bo < 1 은 원리상 못 잰다**.

### 4-2. 측정 사슬
분말 ≤ 20 mg 을 공기 분산기 (1.5 bar) 로 기판 원판 (⌀40 mm) 에 단층 증착 → SEM 으로 단층 확인 → 시료대 (기판판 아래 수집판, Fig 2 단면) 를 주판에 끼워 4 개를 동시에 정해진 높이에서 떨어뜨림 → 받침 (stopper) 의 완충재에서 멈춤 → 주판에 붙은 가속도계 (Castle GA 2002, 0.1–100 g, ±1.5 dB) 로 감속도 → 떨어진 입자를 수집판에서 저울 (0.1 mg) 로 · Malvern G3 영상으로 크기 · 개수 → 높이를 바꿔 반복 → 탈착 분율 vs 감속도 (Fig 7) → 50 % 감속도 a₅₀ → F = m·a₅₀ (m = D50 구 한 개) · Bo [인쇄 p.48 · 50–52 · 54].
- 감속도가 피크인지 · 충격 펄스 시간 · 가속도계 대역폭 [미확인].  "The force to detach the adhered particles is believed to correlate with the force to deposit the particles" [인쇄 p.48] — 증착 상태가 결과를 정한다는 저자 전제.

### 4-3. ★ 입자 처리 (DEM 판 "무질서 처리")
- 실물: 크기 분포 (span 1.1–16.5) · 불규칙 형상 (Fig 3) · 응집체 (미분 탄산칼슘 · 이부프로펜) 를 그대로 증착.
- 계산: 분말마다 **D50 구 하나** (MCC 는 그림에서 D90) · 비중병 밀도 → 입자 하나 질량.  분포 · 형상 · 응집체 보정 없음.  탈착은 **질량** 분율 — 부피 가중이라 큰 입자 · 응집체가 지배 [추정].
- ⇒ "입자 하나의 점착력" 이라는 출력은 **D50 단일 구 대리 (surrogate)** 위의 값이다 — DEM 의 단일 크기 구로 다분산 분말을 대신하는 것과 같은 축약이고, 그보다 강하다 (측정 쪽이 다분산 · 응집체인데 계산 쪽만 단일 구).

### 4-4. 기법 미니 용어집
- **입상 Bond 수 (granular Bond number)**: 입자 사이 인력 ÷ 입자 무게 — >1 응집성 · <1 자유 흐름 (원문 p.47).  혼합물로 넓힌 것 = 다성분 Bond 수 (ref [10] Capece 2015 · [23] Giraud 2021) [인쇄 목록].
- **낙하 충격 탈착 (이 장치)**: 체적력 (관성) 으로 떼어 내는 법 — 원심법 (ref [3] · [15]) 과 같은 계열, 원심 대신 충돌 감속.
- **FD-IGC (finite dilution inverse gas chromatography)**: 탐침 주입량을 늘려 덮임률별 γ^d 분포를 재는 IGC — `mohammadijam2014_inverse_gas_chromatography_review` §4-3.
- **Schultz 법**: RT·ln V_N 을 a·√γ_L^d 에 대해 그린 n-알칸 직선의 기울기로 γ_S^d (같은 카드 §3-1).
- **TIVAR-88**: 상품명 — 재질은 원문에 없다 [미확인].

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | Bo 정의 — 평판 **아래** 매달린 입자 · 위로 점착력 · 아래로 무게 · "B_o = F_ad/mg at the size of d" | Table 2 의 +1 (관성 + 무게 같은 방향) 의 배치 근거 [추정] |
| 2 | 장치 — 원통 축 · 주판 (시료대 4) · 시료대 단면 (기판판 위 · 수집판 아래) · 받침 · 금속 받침판 · 가속도계 사진 | ★ DEM 가상 낙하 시험의 기하 · 경계조건 (§7-3) |
| 3 | 15 분말 SEM (50 · 100 µm 막대) — 미분 탄산칼슘 · 이부프로펜 응집체 · 파라세타몰 극단 형상 · TiO₂ 조밀 구형 | 떨어지는 것이 1 차 입자가 아닐 수 있다는 근거 |
| 4 | 기판 원판 5 종 사진 (⌀40 mm) · 연강 · 유당 정제 SEM (×300) | 기판 표면 상태 |
| 5 | TIVAR 기판 증착 전 (×50) · 유당 증착 뒤 (×180) | 단층 증착 확인의 형식 |
| 6 | 유당 정제 위 입자 SEM · 3D 표면 형상 (증착 전 500 µm 창 · 입자 있음 · 탈착 뒤 2.5 mm 창) | 탈착 확인의 형식 — 창 크기가 달라 직접 비교는 안 됨 |
| 7 | ★ 15 분말 탈착 질량 분율 vs 감속도 (정제 기판) · 43–105 m/s² · 17–84 % | ★ DEM 재현 표적은 Bo 가 아니라 이 **곡선** (§7-3) · 세 계열 y 값 동일 (§3-4) |
| 8 | ★ 점착력 막대 (로그 0.001–1000 nN) + D50 점 | 점착력 = m(D50)·(a₅₀ + g) 계산값 · MCC = 45.7 µm (§3-5) |
| 9 | 유당 4 종 × 5 기판 탈착 분율 vs 감속도 | 기판 무관 주장의 원자료 |
| 10 | ★ 유당 4 종 × 8 기판 점착력 막대 · 변동 2.5 · 1.7 · 1.5 · 1.6 % | ★ 기판에 눈먼 측정 → W_AS ↔ W_SS 판가름 불가 (§7-2) · Fig 8 의 8.3–9.4 배 (§3-6) |
| 11 | 이부프로펜 25 · 7 기판 · 50 % 탈착 감속도 ≈ 61 m/s² 읽기 | Bo 산출 절차 |
| 12 | ★ 점착력 (로그) · Bo vs D50 · y = 1E-04x^2.9149 · Bo 두 추세 화살표 | ★ 2.91 = 질량식의 D³ · Bo 압축 11.0 → 6.7 (§3-5) |
| 13 | ★ JKR · DMT 모형값 vs 장치값 · y = 2.6283x^0.3302 · 3.5132x^0.3303 | ★ 단위 10³ · 지수 1/3 · 방향 반대 (§3-7) |
| Table 1 | 15 분말 D10 · D50 · D90 · span · 밀도 | §3-1 · span 두 행 불일치 |
| Table 2 | 15 분말 D50 · a₅₀ ± · Bo | ★ Bo = 1 + a₅₀/g (§3-2) |
| Table 3 | FD-IGC γ^d 6 물질 | ★ γ^d 좁은 띠 42–58 (§3-3 · §7-2) |
| 식 크롭 | 식 (1) · (2) — 힘의 합 · Bo 정의 | 정의 |
| 식 크롭 | 식 (3)–(5) — Hamaker · DMT · JKR | W_A 를 γ 로 씀 (§10) |
| 식 크롭 | 식 (6) — F_ad = −ma | g 없음 ↔ Table 2 의 +1 (§3-2) |
| 본문 크롭 | p.55 §4.4 — FD-IGC 방법 · "a power of 3 more significant than that the models give" | 근거 원문 (§3-7) |
| 본문 크롭 | p.55 요약 — R² 0.993 (DMT) · 0.997 (JKR) · "three times difference in values" | 근거 원문 (그림 R² 0.9971 과 불일치) |

## 6. Post-processing ★
- **원문**: 탈착 질량 분율 곡선 (Fig 7 · 9 · 11) · 50 % 탈착 감속도 선택 (Fig 11 의 점선 읽기) · 식 (6) · (2) 로 F · Bo · 엑셀식 추세선 (거듭제곱 · R²) · 기판 변동 % (정의 [미확인]).
- **안 한 것**: 반복 수 · 오차 전파 · 가속도 파형 · 탈착 입자 크기 분포의 사용 (G3 로 쟀다고 적었으나 Table 2 는 공급 D50) · 습도 변화 · 정전기 확인 · 기판 표면 에너지 · 다른 물질 쌍의 W 계산.
- **이 카드에서 한 것**: Fig 7 · 12 · 13 의 **PDF 벡터 경로 좌표**를 그림 자체의 격자선으로 축 보정해 판독 (`digitized.csv`) · Fig 10 막대 (300 ppi 래스터 · 색 맞춘 윤곽) · Table 1 · 2 · 3 재계산 (span · 1 + a/g · m(a + g) · JKR SI · Bo_JKR) · Fig 7 → a₅₀ 보간 · y 값 양자화 검사.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 쪽 수치는 리포 출처를 병기)

### 7-1. ★ 측정량 ↔ 우리 Bond 수 · CED [우리 산술]
- 원문 식 (2) Bo = F_ad/mg 는 jarray2019 의 Bo_g · 우리 믹서의 Bo_code 와 같은 꼴 (인력 ÷ 자기 무게).  우리 덱은 두 정의를 가른다 — **Bo_code = F_eq/W** (SJKR 평형 겹침 힘) · **Bo_po = F_po/W** (떼는 힘) · Bo_code = 6.75·Bo_po (Codex HB-02 · `johnson1971_jkr_surface_energy_contact_elastic_solids` §7-1).
- 이 장치는 체적력 (관성 + 무게) 으로 **떼어 내는** 시험 → 대응하는 것은 **Bo_po (평판 벽 접촉)** 쪽이다.  SJKR 로 쓰면 평판 위 입자 하나의 판정식: m(a + g) ≥ F_po,wall = (2/3)π³R\*²CED_w³/E\*_w² (R\* = 입자 반경 · 벽 쌍별 E\*) ⇔ **1 + a_det/g = Bo_po,wall**.  JKR 로는 1 + a/g = (3/2)π·W·r/(mg).
- ⇒ **장치 Bo 를 우리 덱 Bo 에 그대로 대입하지 않는다**: ① 장치 Bo 는 측정 창 (≈ 5.4–11.7) 에 묶인 50 % 탈착 감속도의 g 배수이고 ② 덱 Bo (LC SE–SE 0.213 · LA AM_P 3.0 · LH AM_P 38.4 — johnson1971 카드 §7-1 표 · 생성기 식) 는 **parcel 규모 · 쌍 접촉** 값이라 숫자가 우연히 같은 자릿수여도 같은 양이 아니다 [추정].
- 이 장치는 원리상 **Bo < 1 을 못 잰다** (p.47) — 우리 LC 의 SE–SE 처럼 약한 점착 영역은 다른 방법 (안식각 · 드럼) 몫이다.

### 7-2. ★ 논지 §2-8 (γ_A/γ_S < 0.31 · AM_S 0.39) 에 주는 것
- **기판에 눈먼 측정은 판가름에 못 쓴다**: 논지의 판가름 수는 SE 가 NCM (A) 에 붙는 힘 vs SE (S) 에 붙는 힘이다.  이 장치는 기판을 같은 분말 정제 ↔ 금속 ↔ 유리 ↔ TIVAR-88 로 바꿔도 2.5 % 안에서 같다 (Fig 10).  기하평균 규칙에서도 W_12 ∝ √γ₂ 라 기판 γ 가 2 배 다르면 W 는 1.41 배 달라야 한다 [우리 산술] — 2.5 % 는 그보다 한 자릿수 작다.  ⚠ 원문에 기판들의 γ 가 없어 정량 반증은 아니다 [미확인]; 저자 자신이 결과를 "particle properties and the particle deposition status" 로 해석한다 [인쇄 p.53].
- **γ^d 좁은 띠**: FD-IGC γ^d 가 산화물 (TiO₂ 58) · 탄산염 (54) · 유기 결정 (42–44) 에서 **42–58 mJ/m²** — 가장 큰 비 0.72 [우리 산술].  NCM · LPSCl 의 γ^d 도 이런 띠 안에 든다면 분산 성분만의 비는 0.7–1.4 로 0.31 에서 멀다 → 논지의 비코팅 SE–SE 우세가 성립하려면 **극성 (산·염기) 성분 · 표면 오염층 · 거칠기**가 일을 해야 한다 [추정] (`vanoss1988_lifshitz_vdw_acid_base_interfacial` — 산화물 · 황화물 = 비대칭 극성).
- **같은 물질 · 다른 방법 = 1.5–2.6 배**: TiO₂ γ^d 58 (이 논문 FD-IGC, 공기 중 분말) ↔ 89–148 (Fowkes 1964, 탈기 분말) [우리 산술] — **A 와 S 를 같은 방법 · 같은 표면 상태 · 같은 덮임률**로 재야 비가 뜻을 가진다 (IGC 카드 §7-3 과 같은 결론).
- 판가름 측정의 정답 쪽은 여전히 **같은 탐침 CAB** (`begat2004_cohesive_adhesive_balance_afm_colloid_probe` §7-1) — 기판을 바꿨을 때 값이 바뀌는 것이 그 측정의 존재 이유다.

### 7-3. ★ D3 (SE–SE 점착 앵커) 후보로서 — 가상 낙하 시험 [추정]
- **장점**: mg 시료 · 평판 · 단층 · 감속 펄스라는 **경계조건이 단순**해서 DEM 으로 1:1 흉내 낼 수 있다 — 판 위 단층 입자 (실측 PSD) + 판 감속 펄스 → 탈착 질량 분율 곡선.  비교 대상은 Bo 한 숫자가 아니라 **Fig 7 꼴의 곡선 전체** (감속도 단계 · 분율).
- **단점**: 장치 창 (a ≲ 105 m/s²) 에서 µm 1 차 입자는 매끈한 구 JKR 기준으로 떨어지지 않는다 (§3-2 의 Bo_JKR 10⁴–10⁶ 급, 비슷한 D50 의 Eskal · 이부프로펜 제트밀) → 실제로 떨어지는 것은 응집체 · 겹쳐 쌓인 입자 · 느슨한 증착 · 돌기 접촉일 것 [추정] → DEM 재현은 **증착 상태 · 응집체 · 거칠기**까지 넣어야 뜻이 있다.
- ⇒ D3 앵커로는 `geldart2006_powder_flowability_angle_of_repose_tester` (안식각 · Hausner) · `jarray2019_cohesion_driven_mixing_segregation_drum` (미세저울 떼는 힘 · 드럼 각도) · `alizadeh2018_dem_adhesion_calibration_segregation_heap` (단일 성분 더미 보정) · `nase2001_granular_bond_collision_number_wet_cohesion` (정지 계 Bo_g ≈ 1 전이 · 드럼은 Co) 보다 **해석 사슬이 길다**.  특히 정지 계의 응집 문턱이 Bo_g ≈ 1 근처인데 (nase2001) 이 장치는 원리상 Bo < 1 을 못 재고 실제 창이 ≈ 5.4–11.7 이라 **그 문턱 자체를 짚을 수 없다** [우리 산술].  쓰려면 (가) 불활성 · 건조 (나) 반복 ≥ 3 · 감속도 파형 기록 (다) 탈착 입자 크기 분포 (라) 같은 펄스의 DEM 곡선과 대조 — 4 개가 같이 있어야 한다.

### 7-4. 황화물 (LPSCl) · NCM 에 적용하려면 [추정 — 원문 밖]
- 글로브박스 (Ar) 안에 낙하대 · 저울 · 분산기 (건조 Ar) · 시료 밀봉 이송 (SEM) — 원문은 대기 · RH 40–60 % · Au/Pd 코팅 SEM.
- 기판 = 냉간 압착 SE 펠릿 · NCM 펠릿 (우리 실험실 일상 공정) — 단 펠릿 표면은 비정질 · 결함 · 반응층 (begat2004 카드 §8 의 압밀 기판 경고).
- 가속도계는 진동계 (vibration meter) 대신 충격용 · 대역폭 명시 — ±1.5 dB (−16/+19 %) 를 줄여야 a₅₀ 비교가 뜻을 가진다.
- 판가름 (A ↔ S) 에 쓰기 전에 **기판 감도 검정**: 표면 에너지가 크게 다른 두 기판 (예: 저에너지 고분자 ↔ 금속 산화물) 에서 같은 분말의 a₅₀ 가 달라지는지부터 — 이 논문 결과로는 달라지지 않는다.

### 7-5. 기존 정본 카드와의 관계
- `johnson1971_jkr_surface_energy_contact_elastic_solids`: 식 (5) 의 원전.  원문 γ 정의 (두 면 합 · 같은 물질 W = 2γ) 로 보면 이 논문은 γ^d 를 W_A 로 넣어 2 배 작게 잡았다 (§10) · 거칠기 경고 (p.312) 는 이 장치 값이 매끈한 구 JKR 보다 자릿수로 작은 한 설명 후보.
- `dmt1975_adhesion_contact_deformation`: 식 (4) 원전 (서지 314–326 이 두 카드에서 일치).
- `mohammadijam2014_inverse_gas_chromatography_review`: FD-IGC · Schultz 법 · 덮임률 의존 (석영 66 → 38 mJ/m², 0.5–50 %) — 이 논문 Table 3 의 덮임률 미기재가 왜 문제인지.
- `fowkes1964_attractive_forces_interfaces_dispersion`: TiO₂ γ^d 89–148 ↔ 이 논문 58 (§3-3).
- `begat2004_cohesive_adhesive_balance_afm_colloid_probe`: 쌍 (A–A · A–B) 을 가르는 측정 — 이 장치가 못 하는 것.
- `jarray2019_cohesion_driven_mixing_segregation_drum` (Bo_g = 떼는 힘 / 무게, mm 유리구 0.38–1.74) · `alizadeh2018_dem_adhesion_calibration_segregation_heap` (응집수 = 에너지 불변량 ↔ Bond 수 = 힘 불변량) · `geldart2006_powder_flowability_angle_of_repose_tester` (안식각 · Hausner 비) — D3 의 다른 길.
- `hersey1975_ordered_mixing_concept`: 운반 입자 표면의 미분 부착 — 이 장치의 "판 위 단층 탈착" 은 정렬 혼합 단위체의 안정성 시험과 같은 꼴 (ref [3] 원심법이 바로 그 용도) [추정].
- `lee2026_mechanical_halogen_argyrodite_drycoating` (사용자 공저): SE 펠릿 위 AFM-FS W_ad (aJ) — 황화물 쪽 점착의 실측 형식.  `hare2026_dem_pept_dry_mixing_nmc622_eirich` · `otani2025_dem_se_dispersion_aggregation_compression`: 건식 혼합 DEM 의 γ 입력 — 이 장치 값으로 γ 를 정하는 길은 §7-1 · §7-3 의 한정 때문에 막혀 있다.

### 7-6. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 분말 단위의 **벌크 탈착 통계** (mg · 4 시료 동시 · 감속도 단계별 질량 분율) · γ^d 6 물질 (FD-IGC).
- **없는 것**: 입자 한 쌍의 점착 (W · 떼는 힘) · 쌍별 (A–S) 구분 · 접촉 역학 · 혼합 · 압밀 · 수송.

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **"Bond 수를 측정했다" 는 문헌 값은 정의부터 확인한다** — 이 논문의 Bo 는 1 + a₅₀/g 이고 크기 · 점착 법칙이 들어가지 않는다.  우리 Bo_code · Bo_po 와 숫자를 맞대기 전에 같은 양인지 (힘 기준 · 접촉 기하 · 규모) 를 먼저 본다.
2. **기판에 눈먼 측정은 이종기술 판가름에 못 쓴다** — 판가름 측정의 조건 = 기판을 바꾸면 값이 바뀌어야 한다 (CAB).
3. **γ^d 는 화학이 달라도 좁은 띠** (42–58 mJ/m²) — 0.31 같은 큰 비대칭은 분산 성분에서 나오기 어렵다 → 극성 성분 · 표면층 · 거칠기를 같이 재는 설계 (IGC 극성 탐침 · 접촉각 세 액체 · AFM CAB).
4. **같은 실험을 DEM 으로** — 장치 결과를 DEM 입력으로 "변환" 하지 말고, 장치의 경계조건 (판 · 단층 · 감속 펄스) 을 DEM 으로 흉내 내 **곡선끼리** 비교한다 (D3 · frame[4]: 각자 실험에 보정 · 비교는 교차검증).
5. **단위 · 크기 기준 검산을 습관으로** — 이 논문은 그림 하나 (Fig 13) 의 단위 하나로 결론의 방향이 뒤집혔다.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Deng et al. (Powder Technol. 2021) dropped substrates carrying a powder monolayer (≤ 20 mg) onto a stopper and recorded the deceleration at which half of the deposited mass detached (48–98 m s⁻² for 15 powders); the Bond numbers they report equal 1 + a₅₀/g for every powder (our arithmetic), i.e. 5.9–11.0 for D50 = 2–230 µm."
- "Their finite-dilution IGC dispersive surface energies spanned only 42–58 mJ m⁻² across calcium carbonate, lactose, titanium dioxide, paracetamol, ibuprofen and microcrystalline cellulose (Schultz method; coverage not stated)."
- 국문: *"낙하 감속도로 얻은 Bond 수 (5.9–11.0) 는 같은 논문의 γ 로 계산한 매끈한 구 JKR Bond 수 (10²–10⁶) 의 10⁻⁵–10⁻² 배다 — 이 장치는 1 차 입자의 점착이 아니라 느슨하게 붙은 꼬리를 본다 (우리 산술 · 추정)."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. ★ **Bo = 1 + a₅₀/g (15/15)** [우리 산술] — Table 2 는 m(a + g) 로 계산했는데 식 (6) 에는 g 가 없다 · Bo 에 크기 · 밀도가 들어가지 않는다 · 측정 창 (≈ 5.4–11.7) 밖의 Bo 는 원리상 안 나온다.
2. ★ **Fig 13 단위** — 모형값 = µm · J/m² 의 수 (µN) 를 nN 으로 그림 → 10³ 배 작게 [우리 산술 · 벡터 3–4 자리 일치].  바로 하면 JKR > 장치값 36–2×10⁵ 배 — "measured … a power of 3 more significant" · "three times difference" 둘 다 방향이 반대.  지수 0.33 = D 대 D³ · R² 0.997 은 둘 다 D50 의 함수라서.  본문 DMT R² 0.993 ↔ 그림 0.9971.
3. ★ **"점착력" 은 계산값** — m(D50 구)·(a₅₀ + g).  Fig 12 의 F ∝ D^2.91 은 질량식 D³ · "large particles have a big adhesion" 은 정의의 결과.
4. **MCC 크기 기준 불일치** — Fig 8 · 12 · 13 은 45.7 µm (Table 1 D90) · Table 1 · 2 는 D50 22.7 µm [판독 벡터].
5. **Table 2 D50 = 공급 분말 D50 (15/15)** ↔ 본문 "the size is calculated using the detached particles" (p.52) · Fig 10 은 Fig 8 의 8.3–9.4 배 (다른 크기 기준 [미확인]).
6. **Fig 7 세 계열 (Ibuprofen · Paracetamol · TiO₂) 의 y 값 다섯 개가 같다** (0.03 %p 안) [판독 벡터] — 원자료 확인 필요.
7. **"두 추세 = 표면 에너지 차" 는 Table 3 로 뒷받침되지 않는다** — 두 무리의 γ^d 가 겹치고 이부프로펜은 양쪽 [우리 대조].
8. **Table 1 span 두 행** (Eskal 10 · 15) 이 정의식과 다르다 (5.54 · 9.63 ↔ 1.22 · 1.10) [우리 산술].
9. **W_A = γ^d** — JKR 정의로는 같은 물질 W = 2γ (분산 성분만이면 W^d = 2γ^d) → 모형값이 또 2 배 작다 · 극성 성분 무시.  "the surface energy for powders is regardless of particle size" 라며 제트밀 이부프로펜에도 같은 42 를 썼다 — 밀링이 표면 에너지를 바꾼다는 자기 인용 [17] (Shah 2015, milling temperature → surface energy) 과 긴장 [추정].
10. **γ^d 의 조건** — 덮임률 · 온도 · 탐침 · 사전 건조 [미확인] · Schultz 법 인용 [24] 은 만니톨 유동성 (온도 · 습도) 논문이지 Schultz 원전이 아니다 [인쇄 목록].
11. **가속도계 ±1.5 dB (−16/+19 %)** ≫ 보고된 기판 변동 2.5 % — 반복성과 정확도를 구분해야 한다 · 진동계로 충격을 잰 것 · 파형 · 대역폭 [미확인] [우리 산술 · 추정].
12. **RH 40–60 % 미제어** — 모세관 힘 (식 1 의 F_cf) 이 섞여 있다 · 정전기 확인 없음.
13. **인쇄 결함** — 거칠기 "0.1 mm to 0.6 μm" · Au/Pd "5-mm layer" (nm 일 것) · SEM 기종이 본문 JSM-5510 (JEOL) 인데 그림의 정보 띠는 "UoG-SU8030" [인쇄 · 판독] · Fig 13 축 제목 "Adhesin" · MCC 공급처 "KP Snacks".
14. **반복 수 · 통계 방법 미기재** — Table 2 의 ± 가 무엇의 표준편차인지 [미확인].

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 3 | D.T. Tran, R. Bittner, P. Zámostný, Adhesion force measurement by centrifuge technique as tool for predicting interactive mixture stability, Chem. Eng. Res. Des. 165 (2021) 467–476. | 원심 탈착 → 정렬 (상호작용) 혼합물 안정성 — SE 를 NCM 에 붙인 혼합물의 안정성 시험 형식 |
| 5 | A. Castellanos, The relationship between attractive interparticle forces and bulk behaviour in dry and uncharged fine powders, Adv. Phys. 54 (4) (2005) 263–376. | ★ 건조 미분의 입자간 힘 ↔ 벌크 거동 (Bond 수) — D3 의 이론 바탕 |
| 9 | S.T. Nase, W.L. Vargas, A.A. Abatan, J.J. McCarthy, Discrete characterization tools for cohesive granular material, Powder Technol. 116 (2–3) (2001) 214–223. | 정본 `nase2001_granular_bond_collision_number_wet_cohesion` — Bo_g = F_c/W 정의 · 정지 더미 · 호퍼는 Bo_g ≈ 1 에서 급변 · 드럼은 충돌 수 Co |
| 10 | M. Capece, R. Ho, J. Strong, P. Gao, Prediction of powder flow performance using a multi-component granular Bond number, Powder Technol. 286 (2015) 561–571. | ★ 혼합물 (다성분) Bond 수 — 이종 혼합 (AM + SE) 의 Bo 정의 |
| 11 | E. Ermis, Establishment of a Repeatable Test Procedure for Measuring Adhesion Strength of Particulates in Contact with Surfaces, Doctoral dissertation University of Greenwich, UK, 2011. | 장치 원전 · 감속도 측정 상세 |
| 15 | G.R. Salazar-Banda, M.A. Felicetti, J.A.S. Gonçalves, J.R. Coury, M.L. Aguiar, Determination of the adhesion force between particles and a flat surface, using the centrifuge technique, Powder Technol. 173 (2) (2007) 107–117. | 체적력 탈착의 다른 방식 (원심) |
| 16 | M.A.S. Quintanilla, J.M. Valverde, A. Castellanos, Adhesion force between fine particles with controlled surface properties, AICHE J. 52 (5) (2006) 1715–1728. | 표면 상태를 제어한 미분 점착력 실측 |
| 17 | U.V. Shah, Z. Wang, D. Olusanmi, A.S. Narang, M.A. Hussain, M.J. Tobyn, J.Y. Heng, Effect of milling temperatures on surface area, surface energy and cohesion of pharmaceutical powders, Int. J. Pharm. 495 (1) (2015) 234–240. | 밀링 → 표면 에너지 · 응집 — 우리 SE 밀링 이력 · 건식 혼합 에너지 |
| 20 | K.L. Johnson, K. Kendall, A. Roberts, Surface energy and the contact of elastic solids, Proc. R. Soc. Lond. A Math. Phys. Sci. 324 (1558) (1971) 301–313. | 정본 `johnson1971_jkr_surface_energy_contact_elastic_solids` |
| 21 | B.V. Derjaguin, V.M. Muller, Y.P. Toporov, Effect of contact deformations on the adhesion of particles, J. Colloid Interface Sci. 53 (2) (1975) 314–326. | 정본 `dmt1975_adhesion_contact_deformation` |
| 23 | M. Giraud, S. Vaudez, C. Gatumel, J. Nos, T. Gervais, G. Bernard-Granger, H. Berthiaux, Predicting the flowability of powder mixtures from their single components properties through the multi-component population-dependent granular bond number; extension to ground powder mixtures, Powder Technol. 379 (2021) 26–37. | ★ 단일 성분 성질 → 혼합물 유동성 (분포 의존 Bond 수) — D2 · D3 를 잇는 형식 |
| 24 | H. Salehi, V. Karde, H. Hajmohammadi, S. Dissanayake, S.H. Larsson, J.Y. Heng, M. Bradley, Understanding flow properties of mannitol powder at a range of temperature and humidity, Int. J. Pharm. 596 (2021) 120244. | ⚠ 원문이 "Schultz approach" 의 출처로 인용 — 실제 내용 확인용 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 11 쪽 전부 텍스트층 (`pdftotext` · PyMuPDF) 과 쪽 이미지로 읽었다.  표 1–3 은 배치 보존 텍스트로 칸 대조 · 식 (1)–(6) 은 크롭 이미지로 옮겼다.
- Fig 7 · 12 · 13 은 **PDF 벡터 경로**의 표지 중심 좌표를 그림 자신의 격자선 위치로 축 보정해 읽었다 (Fig 13: x 0 → 176.27 pt · 700 → 430.15 pt · y 0 → 264.97 · 35 → 57.65) — 계열은 표지 모양 · 색으로 가렸다.  Fig 10 은 300 ppi 내장 이미지라 막대 윤곽색으로 읽었다 (±25 nN).
- §3-2 · §3-7 의 재계산 (1 + a/g · m(a + g) · JKR SI · 단위) 은 Table 1–3 인쇄값만 썼다.
- 크롭 22 장 = Fig 1–13 + Table 1–3 + 식 영역 4 + 본문 2 (전부 손 크롭 · 300 dpi).  자동 추출은 Fig 7 · 13 · Table 1 · 2 를 놓치고 Fig 8 · 9 · 11 · 12 를 잘라 먹어 손 크롭으로 통일했다.  본문 크롭 하나는 앞 문단 글자 아랫부분이 들어가 다시 잘랐다.
- 정본 litdb 중복 확인: 파일 목록 + DOI · "surface energy tester" `git grep` 0 건.

## 🔗 관련 카드
- 같은 묶음 (점착 · 표면 에너지 측정): `johnson1971_jkr_surface_energy_contact_elastic_solids` · `dmt1975_adhesion_contact_deformation` · `begat2004_cohesive_adhesive_balance_afm_colloid_probe` · `mohammadijam2014_inverse_gas_chromatography_review` · `fowkes1964_attractive_forces_interfaces_dispersion` · `vanoss1988_lifshitz_vdw_acid_base_interfacial`.
- D3 (점착 앵커) 의 다른 길: `geldart2006_powder_flowability_angle_of_repose_tester` · `jarray2019_cohesion_driven_mixing_segregation_drum` · `alizadeh2018_dem_adhesion_calibration_segregation_heap`.
- 정렬 혼합 · 건식 코팅: `hersey1975_ordered_mixing_concept` · `pfeffer2001_dry_particle_coating_engineered_particulates`.
- 황화물 점착 실측 · 건식 혼합 DEM: `lee2026_mechanical_halogen_argyrodite_drycoating` · `hare2026_dem_pept_dry_mixing_nmc622_eirich` · `otani2025_dem_se_dispersion_aggregation_compression`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
