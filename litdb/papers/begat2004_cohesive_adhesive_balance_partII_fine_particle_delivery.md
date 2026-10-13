<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 이웃 = begat2004_cohesive_adhesive_balance_afm_colloid_probe.md (같은 연작 Part I) · hersey1975_ordered_mixing_concept.md.
     원문 = 8 쪽 (본문 + 참고문헌) · SI 없음 · 쪽 표기 = 인쇄 쪽 p.1826–1833 (PDF n 쪽 = p.(1825 + n)).
     텍스트층 = 조판 PDF — 본문 · 표 숫자는 pdftotext 와 쪽 이미지로 대조 (그리스 문자 · 위첨자는 텍스트층에서 깨진다: "102 · 103" = 10² · 10³).
     그림은 PDF 안 래스터 (Fig 1 · 3–6 = 144 ppi JPEG · Fig 2 = 288 ppi 1-bit) — 크롭은 캡션까지 300 dpi 렌더.  판독은 원 래스터 (pdfimages) 의 픽셀에서.
     값 표지: [인쇄] = 본문 · 표 · 그림 안 인쇄 숫자 / [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv) / [우리 산술] = 원문 값으로 한 계산 또는 이 논문 밖 값 (출처 명시) 과 엮은 계산 / [추정] = 우리 해석 / [미확인] = 원문에 없음. -->

# The Cohesive-Adhesive Balances in Dry Powder Inhaler Formulations II: Influence on Fine Particle Delivery Characteristics — Part I 의 AFM 응집 · 접착 비를 **환산 혼합 계수 Λ₁₂ = F^ad₁₂ / F^co₁₁** (1 과 비교) 로 바꿔 실제 혼합과 대조: Λ₁₂ 16.88 인 salbutamol sulfate 는 lactose 위에 고르게 퍼지고 (함량 RSD 4.2 %) 0.22 인 budesonide 는 덩어리로 남는다 (28.1 %) · 약물만의 제형에서는 응집이 센 쪽이 오히려 미세입자 분율이 높다 (큰 덩어리가 받는 항력 ∝ Φ² · 운동에너지 ∝ Φ³) — Begat · Morton · Staniforth · Price (Pharm. Res. 2004)

> slug `begat2004_cohesive_adhesive_balance_partII_fine_particle_delivery` · DOI `[미확인]` · type `experiment (dry powder inhaler blends — cohesive-adhesive balance to reduced intermixing coefficient Λ12 from part-I AFM CAB; Aerosizer de-agglomeration at 1 and 5 psi; twin-stage impinger deposition, Rotahaler vs Turbuhaler; blend SEM and content uniformity; no DEM)` · PDF `c197a5ce-62._The_cohesive-adhesive_balances_in_dry_powder_inhaler_formulations_II_influence_on_fine_particle_delivery_characteristics.pdf` · digested `2026-10-13` · status ✅
>
> **서지 (원문 인쇄)**: Philippe Begat¹ · David A. V. Morton² · John N. Staniforth² · Robert Price¹,³ — ¹ Pharmaceutical Technology Research Group, Department of Pharmacy & Pharmacology, University of Bath, Bath BA2 7AY, United Kingdom · ² Vectura Ltd., Chippenham, SN14 6FH, United Kingdom · ³ 교신 (r.price@bath.ac.uk) · *Pharmaceutical Research* **21** (10), 1826–1833, October 2004 (© 2004) · Research Paper · Received 2004-02-20 · accepted 2004-06-10 · 판권 줄 "0724-8741/04/1000-1826/0 © 2004 Springer Science+Business Media, Inc." [인쇄 p.1826].
> ⚠ **DOI 는 PDF 에 인쇄돼 있지 않다** (본문 · 판권 줄 · XMP 메타데이터 검색 0 건) → `[미확인]`.  판권 줄의 "0724-8741/04/1000-1826/0" 은 판권 코드다.
> ★ **연작의 Part II** — Part I = 정본 카드 [`begat2004_cohesive_adhesive_balance_afm_colloid_probe`](begat2004_cohesive_adhesive_balance_afm_colloid_probe.md) (*Pharm. Res.* 21 (9) 1591–1597).  이 논문의 참고문헌 14 는 Part I 을 **학술지 · 권 · 쪽 없이** 제목만 적는다 [인쇄 p.1832].  두 편의 연결은 §12.
> **이 카드가 서랍에 들어온 이유**: Part I 카드 §10-9 가 *"혼합 예측은 검증되지 않았다 (II 편 [미확인])"* 로 남긴 빈칸 — **Part I 의 CAB 예측을 실제 혼합 (SEM · 함량 균일도) 과 흡입 분산으로 대조한 짝 논문**.  주 리포 읽기 목록 `docs/mixer_coating_reading_list_20261013.md` 의 B4-2 · 순번 7 (*"Part I / II 구분부터 확인"*).
> **판독 원자료**: `litdb/figures/begat2004_cohesive_adhesive_balance_partII_fine_particle_delivery/digitized.csv` (35 행 — Fig 2 점 3 · Fig 3 · 6 막대 32) · 크롭 15 장 `figures.json`.

> ★★ **한 줄로 왜 중요한가**: 이종기술 논지 (`docs/hetero_thesis.md` §2-8) 의 판가름 수 — *"떼는 힘 비 F_SE–AM / F_SE–SE 가 1 보다 작은가"* — 와 **같은 꼴의 수에 이름 (reduced intermixing coefficient Λ₁₂) 과 1 기준의 읽는 법** 이 이미 있다: *"the alacrity (Λ₁₂ > 1) or the reluctance (Λ₁₂ < 1) of the active particles to form an interactive mixture with the carrier particles"* [인쇄 p.1830].  그리고 그 수가 큰 약물은 운반체에 고르게 퍼지고 작은 약물은 **덩어리로 남는다** 는 것을 같은 혼합 조건에서 SEM 과 함량 RSD (4.2 % vs 28.1 %) 로 보인다 — 논지 P1 · P2 의 방향과 같은 제약 분체 사례.
> ⚠ 단 **서로 다른 두 약물의 대비** (같은 분말의 표면을 바꾼 비교가 아니다) · **혼합 조건 하나** · 운반체가 **미세 lactose (중앙 9.29 µm) 라 크기비 ≈ 2–2.5** · Λ 는 Part I 의 **평판 AFM 비** (25 °C · 35 % RH) 에서 왔다.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 같은 미분화 약물 둘 (salbutamol sulfate · budesonide) 을 미세 lactose 와 1 : 1 로 섞어 보니, Part I 의 AFM 비로 만든 Λ₁₂ (접착 ÷ 자기 응집) 가 1 보다 훨씬 큰 salbutamol 은 lactose 표면에 고르게 퍼지고 (RSD 4.2 %), 1 보다 작은 budesonide 는 덩어리째 고르지 않게 붙었다 (RSD 28.1 %) — 그런데 흡입기에서의 미세입자 분율은 이 "혼합 품질" 과 같은 순서가 아니었다 (약물만이면 응집이 센 budesonide 가 고저항 장치에서 63.4 % vs salbutamol 13.7 %) [인쇄 p.1830 · Table IV].

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 논지 §2-8 판가름 수에 이름 · 기준이 있나 | **Λ₁₂ = F^ad₁₂ / F^co₁₁** (식 4, 재료 1 = 약물 · 재료 2 = 운반체) — Rowe 의 reduced spreading coefficient (기질–결합제 접착일 ÷ 결합제 응집일) 를 혼합으로 옮긴 것 · **1 보다 크면 상호작용 혼합물을 잘 만들고 (alacrity) 작으면 꺼린다 (reluctance)** | [인쇄] p.1830 |
| ② 그 수가 혼합 결과를 가르나 | salbutamol (Λ 16.88 ± 0.91) = *"uniform distribution of highly dispersed … particles over the lactose surface"* · budesonide (Λ 0.22 ± 0.21) = *"remain agglomerated and unevenly spread"* · 함량 RSD **4.2 % vs 28.1 %** (≈ 6.7 배) | [인쇄] p.1830 · Fig 5 · [우리 산술] |
| ③ Λ 값은 어디서 왔나 | Part I 의 CAB — Table III 의 여섯 값이 **Part I Table II (salbutamol 응집 = 1 교차 정규화) 를 행의 대각원소로 나눈 값과 소수 둘째 자리까지 같다** (예: budesonide→lactose 7.00 / 31.76 = 0.2204) | [인쇄] Table III · [우리 산술] |
| ④ 응집이 세면 덩어리가 얼마나 큰가 | Aerosizer 저전단 (1 psi) ÷ 고전단 (5 psi) 중앙 공력 지름의 세제곱 = 겉보기 덩어리 부피비: salbutamol **1.86** · lactose **22.4** · budesonide **2556** — Fig 2 는 이것을 응집 비 (그림 판독 1.00 · 14.12 · 31.75 = Part I Table II 대각 1.00 · 14.13 · 31.76) 에 대해 **y = e^0.2471x, R² 0.999** 로 맞춘다 (세 점) | [우리 산술] Table II · [판독] · [인쇄] Fig 2 |
| ⑤ 응집이 세면 분산이 나쁜가 | **아니다 (역설)**: 약물만 — budesonide FPF Rotahaler 14.4 → Turbuhaler 63.4 % · salbutamol 6.2 → 13.7 % — 저자 해석: 큰 덩어리일수록 받는 항력 (∝ Φ², 식 2) · 운동에너지 (∝ Φ³, 식 3) 가 커서 장치 안에서 더 잘 깨진다 · 결합력 = 항력이 되는 **준안정 덩어리 크기** 에서 분산이 멈춘다 | [인쇄] p.1829–1830 · Table IV |
| ⑥ 운반체를 넣으면 | salbutamol + lactose: FPF **두 배** (6.2 → 12.6 · 13.7 → 28.4 %) · 방출 비슷 / budesonide + lactose: Rotahaler 14.4 → 26.3 % (유의) · Turbuhaler 63.4 → 58.9 % (유의차 없음) | [인쇄] Table IV · p.1831 |
| ⑦ FPF 정의 | **본문에 정의가 인쇄돼 있지 않다** — 그림의 2 단 막대 ÷ Table IV 방출량 이 Table IV 의 FPF 와 8 경우 모두 ±1.3 %p (6 경우 ±0.3 %p) 안에서 맞는다 ⇒ FPF ≈ 2 단 침착량 ÷ 방출량 (2 단 = 공력 지름 6.4 µm 미만) | [판독 + 우리 산술 · 추정] |

⛔ **한정어 (떼지 말 것)**: ① 유기 약물 결정 + α-lactose monohydrate — 배터리 소재 아님 ② Λ 는 **Part I 의 평판 AFM 떼는 힘 비** (25 °C · 35 % RH · 탐침 3 개/물질) — 입자–입자 접촉 · 혼합기 안 충돌이 아니다 ③ **서로 다른 두 물질의 대비** (n = 2 계) — 크기 · 모양 · 응집 구조 (salbutamol 성긴 덩어리 vs budesonide 치밀한 덩어리, p.1827) 가 함께 다르다 ④ 혼합 조건 **하나** (Whirlimixer 100 mg 단계 희석 → Turbula 46 rpm 30 min) — 시간 · 강도 변화 없음 ⑤ 운반체 = **미세 lactose** · 약물 : 운반체 = **1 g : 1 g** — 원문이 일부러 고른 조건 (p.1831) ⑥ 함량 균일도 시료 수 · FPF 정의 [미확인].

---

## 1. 한 줄 요약

흡입용 건분말 (DPI) 제형에서 약물 입자끼리의 응집 (cohesion) 과 약물–운반체 접착 (adhesion) 의 균형이 혼합 · 분산을 정한다는 Part I 의 가설을 시험한다.  ① Aerosizer 를 두 전단 (1 · 5 psi) 으로 돌려 약물 · lactose 분말이 얼마나 쉽게 풀리는지 보고 (덩어리 부피비 ↔ Part I 응집 비 = 지수 관계), ② 약물만의 제형을 저저항 (Rotahaler) · 고저항 (Turbuhaler) 흡입기로 쌍단 충돌기 (TSI) 에 쏘아 미세입자 분율 (FPF) 을 재고 (응집이 센 budesonide 가 오히려 높다 = 역설 → 덩어리 크기 · 항력 · 운동에너지 모형), ③ Part I CAB 로 **환산 혼합 계수 Λ₁₂** 를 정의해 lactose 와의 혼합물 SEM · 함량 균일도와 대조하고 (Λ 16.88 → 고른 상호작용 혼합 · Λ 0.22 → 덩어리 · 불균일), ④ 운반체 제형의 FPF 변화를 Λ 와 덩어리 항력으로 해석한다.  결론 = 콜로이드 AFM + CAB 가 제형 거동을 미리 보는 도구가 될 수 있다.

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| P. Begat · D. A. V. Morton · J. N. Staniforth · **R. Price\*** (Univ. Bath · Vectura Ltd) | Pharm. Res. **21** (10) 1826–1833 (October 2004) · 접수 2004-02-20 · 승인 2004-06-10 | `[미확인]` (PDF 미인쇄) | 미분화 **budesonide** (Sicor, batch 6157/MI) · 미분화 **salbutamol sulfate** (Becpharm, batch 940077) · **Sorbalac 400 lactose** (Meggle) — ⚠ 혼합 절은 "Lactochem lactose" 로 적는다 (§10-3) | 실험 (입도 · 비행시간 공력 입도 · HPLC · 함량 균일도 · TSI 침착 · SEM) + 간단한 항력 모형 |

| 원문 구조 | 쪽 | 내용 |
|---|---|---|
| 초록 · Introduction | 1826 | DPI = 거친 운반체 (α-lactose monohydrate) + 미분화 약물 · 접착이 과하면 운반체에서 안 떨어짐 · 응집이 세면 분리 · 덩어리 · Part I (ref 14) 의 CAB 그래프 |
| Materials and Methods | 1826–1827 | 재료 · 혼합 (1 g + 1 g, Whirlimixer → Turbula) · SEM · 레이저 입도 · Aerosizer (1 · 5 psi) · HPLC · 함량 균일도 · TSI (Rotahaler · Turbuhaler, 60 L/min, 5 s) |
| Results and Discussion | 1827–1832 | 물성 (Fig 1 · Table I) · 응집도와 분말 거동 (Table II · Fig 2 · Fig 3 · 식 1–3 · Fig 4) · 약물–부형제 상호작용 (식 4 · Table III · Fig 5 · Fig 6 · Table IV) |
| Conclusions · References (20) | 1832–1833 | |

- 중복 확인 (2026-10-13): 정본 `litdb/papers/` 전수 목록 (433 편) 에 Part II 파일 없음 · `git grep -i` "Begat" · "fine particle delivery" · "intermixing" → Part I 카드와 공용 파일만 걸림 → **새 카드** (Part I 카드는 고치지 않음 — §12 · 정정 후보).

---

## 3. 핵심 수치 (★ 쪽 · 표지 병기)

### 3-1. 재료 · 조건 [인쇄]
| 항목 | 값 | 쪽 |
|---|---|---|
| 혼합물 | 약물 **1 g** + lactose **1 g** 를 **100 mg 씩 단계 희석 (geometric mixing)** · Whirlimixer (Fisons) → **Turbula 46 rpm 30 min** (Glen Creston; 원문 "Longhborough" 오식) | 1826–1827 |
| SEM | Jeol 6310 · **10 keV** · 금 코팅 (Edwards) | 1827 |
| 레이저 입도 | Mastersizer X (Malvern) · 렌즈 원문 "30-0mm" · 시클로헥산 분산 · 초음파 5 min | 1827 |
| 공력 입도 | **Aerosizer + Aerodisperser** (Amherst) · 시료 ≈ 5 mg · 중간 공급 속도 · 180 s · **저전단 1 psi ≈ 6.895 kPa · 고전단 5 psi ≈ 34.474 kPa** (분산 핀–핀 보울 환형 틈의 압력 강하) | 1827 |
| HPLC | salbutamol: Spherisorb 5 µm ODS1 (원문 "Sperisorb") · 메탄올 : 물 60 : 40 + 아세트산 0.1 % · 1.25 ml/min · 276 nm / budesonide: Hypersil MOS C8 5 µm · 물 : 아세토니트릴 60 : 40 · 1.5 ml/min · 248 nm | 1827 |
| 함량 균일도 | **10 mg ± 0.5 mg** 시료의 약물량 · 시료 사이 상대표준편차 (RSD) · 시료 수 **[미확인]** | 1827 |
| 침착 시험 | 쌍단 액체 충돌기 (TSI, Copley) · 1 단 7 ml · 2 단 30 ml 이동상 · **60 L/min · 5 s · n = 3** · 1 단 절단 공력 지름 **6.4 µm** · Turbuhaler 계량실 ≈ **1.5 mg** · Rotahaler 젤라틴 캡슐 **2.5 mg** | 1827 |
| 장치 저항 | Rotahaler (저저항) **0.68 kPa** · Turbuhaler (고저항) **8.5 kPa** — 둘 다 60 L/min 에서의 압력 강하 | Table IV 각주 |

### 3-2. Table I — 레이저 입도 (초음파 분산 · mean ± SD · n = 5) [인쇄 p.1828]
| | lactose | salbutamol sulfate | budesonide |
|---|---|---|---|
| d16 (µm) | 3.00 ± 0.19 | 2.17 ± 0.03 | 2.06 ± 0.02 |
| d50 (µm) | **9.29 ± 1.07** | **4.77 ± 0.13** | **3.75 ± 0.05** |
| d84 (µm) | 20.26 ± 2.36 | 11.58 ± 1.09 | 6.81 ± 0.2 |
- 두 약물 중앙값 < 5 µm (호흡성) · lactose 중앙 ≈ 10 µm (SEM · 공급사 자료와 일치) [인쇄 p.1827].
- [우리 산술] 운반체 : 약물 중앙 지름 비 = **1.95 (salbutamol) · 2.48 (budesonide)** (레이저) · 공력 고전단 기준 3.62 · 4.01 (Table II).

### 3-3. Table II — 비행시간 공력 입도 (고전단 5 psi · 저전단 1 psi · n = 5) [인쇄 p.1829]
| | lactose 고 | lactose 저 | salbutamol 고 | salbutamol 저 | budesonide 고 | budesonide 저 |
|---|---|---|---|---|---|---|
| d16 (µm) | 5.59 ± 0.37 | 18.35 ± 3.53 | 1.89 ± 0.08 | 2.04 ± 0.40 | 1.63 ± 0.20 | 20.65 ± 2.34 |
| d50 (µm) | **10.54 ± 0.70** | **29.70 ± 4.58** | **2.91 ± 0.30** | **3.58 ± 0.88** | **2.63 ± 0.28** | **35.96 ± 3.12** |
| d84 (µm) | 14.47 ± 1.29 | 41.39 ± 6.1 | 4.32 ± 0.86 | 5.33 ± 1.35 | 3.92 ± 0.40 | 49.18 ± 3.1 |
- 고전단 = 좁은 대수정규 · 레이저와 맞춰 보면 **고전단에서 완전히 풀림** · 저전단 = lactose · budesonide 는 크게 이동 (덩어리) · salbutamol 은 아주 조금만 [인쇄 p.1827].
- [우리 산술] 겉보기 덩어리 부피비 (R/r)³ = (d50 저 / d50 고)³: lactose **22.4** · salbutamol **1.86** · budesonide **2556**.

### 3-4. Fig 2 — 덩어리 부피비 vs 응집 비 [인쇄 + 판독]
- 식 (1): **V_agglomerate = n·V_particle + δ_v** (n = 덩어리 안 입자 수 · δ_v = 입자 사이 빈 부피) — 고전단 지름 = 풀린 입자 중앙 · 저전단 지름 = 덩어리 중앙으로 보는 가정 [인쇄 p.1828].
- x = *"cohesive balance dependencies … obtained from the quantitative colloidal AFM measurements undertaken in the first part"* (ref 14) · y 축 인쇄 = *"Apparent agglomerate density (R/r)³"* (log 1–10000) · x 축 인쇄 = *"Cohesion ratio depedency"* (오식) · 맞춤 **y = e^0.2471x · R² = 0.999** [인쇄 Fig 2] · 본문: *"the degree of de-agglomeration decreased exponentially as a function of agglomerate cohesive strength"* [인쇄 p.1828].
- [판독] 점: salbutamol (1.00, 1.9) · lactose (14.12, 27.0; x 오차막대 13.06–15.18) · budesonide (31.75, 2567; 30.21–33.29).
- [우리 산술] x 값 · 오차막대 = **Part I Table II 의 대각원소 1.00 ± 0.08 · 14.13 ± 1.06 · 31.76 ± 1.53 과 같다** · y 의 budesonide · salbutamol 은 Table II 세제곱 (2556 · 1.86) 과 맞고 lactose 판독 27.0 은 Table II 세제곱 22.4 보다 ≈ 20 % 크다 (복제 평균의 비 등 계산 경로 [미확인]).
- [우리 산술] 인쇄 지수 0.2471 = ln(2567)/31.76 = **budesonide 한 점만으로 정해지는 값** (세 점 원점 고정 로그 최소제곱이면 0.245) · 인쇄 R² 0.999 는 선형 y 공간 (budesonide 가 지배) 의 값과 맞고 로그 공간이면 0.993.

### 3-5. Table III — 환산 혼합 계수 Λ₁₂ (mean ± SD · n = 3) [인쇄 p.1830]
| 재료 1 (행) \ 재료 2 (열) | salbutamol sulfate | lactose | budesonide |
|---|---|---|---|
| salbutamol sulfate | — | **16.88 ± 0.91** | 6.59 ± 0.21 |
| lactose | 1.19 ± 0.42 | — | 0.5 ± 0.31 |
| budesonide | 0.21 ± 0.13 | **0.22 ± 0.21** | — |
- 식 (4) **Λ₁₂ = F^ad₁₂ / F^co₁₁** — *"a dimensionless parameter, corresponds to the force ratio between adhesive interactions (F₁₂) and cohesive interactions (F₁₁) of two interacting materials"* [인쇄 p.1830].
- 해석: salbutamol (16.88) = *"can be easily displaced to form an interactive mixture"* · budesonide (0.22) = *"would require an intensive mixing process to form a metastable carrier-based formulation"* [인쇄 p.1830].
- ⚠ budesonide→lactose 0.22 ± 0.21 · lactose→budesonide 0.5 ± 0.31 — **SD 가 평균에 가깝다** (상대 SD 95 % · 62 %) [우리 산술].

### 3-6. ★ 혼합물 — SEM · 함량 균일도 (Fig 5) [인쇄 p.1830]
- salbutamol sulfate–lactose: *"a uniform distribution of highly dispersed salbutamol sulfate particles over the lactose surface"*.
- budesonide–lactose: *"budesonide particles appeared to remain agglomerated and unevenly spread over the lactose carrier"*.
- 함량 RSD **4.2 % (salbutamol) vs 28.1 % (budesonide)** — *"good correlation between the reduced intermixing coefficient and the characteristics of the respective carrier based formulations"* [인쇄 p.1830–1831] · [우리 산술] RSD 비 6.7.

### 3-7. 침착 (Fig 3 · Fig 6 · Table IV) [인쇄 + 판독]
**Table IV (mean ± SD · n = 3)** [인쇄 p.1832]:
| 제형 | Rotahaler FPF (%) | Rotahaler 방출 (%) | Turbuhaler FPF (%) | Turbuhaler 방출 (%) |
|---|---|---|---|---|
| salbutamol sulfate | 6.2 ± 0.6 | 84.9 ± 3.4 | 13.7 ± 0.5 | 81.9 ± 2.1 |
| salbutamol + lactose | 12.6 ± 1.2 | 81.3 ± 3.3 | 28.4 ± 1.5 | 84.2 ± 2.7 |
| budesonide | 14.4 ± 4.9 | 57.7 ± 5.0 | 63.4 ± 3.4 | 64.8 ± 4.6 |
| budesonide + lactose | 26.3 ± 6.2 | 47.7 ± 1.2 | 58.9 ± 7.1 | 66.3 ± 8.0 |

**[판독] Fig 3 · 6 막대 (명목 투여량 대비 %, Rotahaler / Turbuhaler)**:
| 제형 | 장치 | 목 | 1 단 | 2 단 |
|---|---|---|---|---|
| salbutamol (Fig 3A) | 15.2 / 18.6 | 13.2 / 16.8 | 66.6 / 54.2 | 5.4 / 11.4 |
| budesonide (Fig 3B) | 42.5 / 29.5 | 9.3 / 12.9 | 40.6 / 16.6 | 8.3 / 41.9 |
| salbutamol + lactose (Fig 6A) | 18.7 / 16.1 | 9.6 / 19.7 | 61.8 / 41.0 | 10.4 / 24.2 |
| budesonide + lactose (Fig 6B) | 52.3 / 31.1 | 11.4 / 17.9 | 24.1 / 11.9 | 12.7 / 39.6 |
- 각 막대 묶음의 합 100.2–101.0 % [우리 산술 — 판독 일관성 확인].
- 본문 판정 [인쇄 p.1828–1831]: salbutamol 만 = 두 장치 방출 > 80 % · 고저항 장치가 FPF **2 배** (6.2 → 13.7 = ×2.21 [우리 산술]) · 1 단에 많이 남아 덜 풀림 (*"rather surprising"*) / budesonide 만 = 장치에 많이 남음 · 고저항 장치가 탈응집 효율 **4 배** (14.4 → 63.4 = ×4.40 [우리 산술]) / salbutamol + lactose = 방출 비슷 · 1 단 ↓ · 2 단 ↑ (p < 0.05) / budesonide + lactose = Rotahaler 에서 1 단 ↓ · FPF ↑ (p < 0.05) · Turbuhaler 에서는 약물만과 유의차 없음.
- [판독 + 우리 산술] **FPF ≈ 2 단 ÷ 방출량** — Table IV 의 방출량으로 나누면 8 경우 모두 ±1.3 %p 안 (예: salbutamol Rotahaler 5.4 / 84.9 = 6.4 vs 6.2).  ⚠ budesonide 만 · Turbuhaler 의 **장치 막대 29.5 % → 방출 70.5 %** 는 Table IV 64.8 % 와 **≈ 6 %p 어긋난다** (§10-2).

### 3-8. 덩어리 · 항력 모형 (식 2 · 3 · Fig 4) [인쇄 p.1829–1830]
- (2) **F_drag = C_d (π/8) ρ_air Φ_agg² v_flow²** (C_d = 항력 계수 · Φ_agg = 덩어리 유효 지름 · v_flow = 공기 속도).
- (3) **E_c^t0 = (π/12) ρ_agg (Φ_agg^t0)³ v_flow²** (덩어리의 처음 운동에너지).
- ⇒ *"the aerodynamic drag force and kinetic energy differences between a 5 µm and 50 µm object at a constant settling velocity would be 10² and 10³, respectively"* [인쇄] ([우리 산술] (50/5)² = 100 · (50/5)³ = 1000 — 일치).
- 제안: 분산 중 **덩어리 내부 결합력 = 장치 안 항력 (F_coh = F_drag)** 이 되는 상태에 이르면 *"a critical agglomerate size at which suspension of the elutriation process occurs"* — 그 준안정 덩어리의 성질은 장치의 기류 특성과 입자 응집 성질에 달려 있다 [인쇄 p.1830].
- Fig 4 (모식): 약하게 응집한 salbutamol = 작은 덩어리가 빨리 준안정 크기에 도달 → **방출은 높고 미세입자 전달은 낮다** · 강하게 응집한 budesonide = 큰 덩어리 → 관성 · 항력 · 장치 안 충돌이 커서 **분산 효율이 높다** (E_c, F_d vs E′_c, F′_d · Φ^t0 → Φ^tf).

---

## 4. ★ 방법 — 측정 사슬 · 식 · 입자 처리

### 4-1. 측정 사슬
분말 셋 (약물 2 · lactose 1) → SEM (Fig 1) · 레이저 입도 (Table I) → Aerosizer 1 · 5 psi (Table II) → 덩어리 부피비 ↔ Part I 응집 비 (Fig 2) → 약물만 TSI (Fig 3) → 덩어리–항력 모형 (식 1–3 · Fig 4) → Part I CAB 로 Λ₁₂ (식 4 · Table III) → 혼합물 1 g + 1 g 의 SEM · 함량 RSD (Fig 5) → 운반체 제형 TSI (Fig 6 · Table IV) → 해석.

### 4-2. ★ 입자 처리 (DEM 판 "무질서 처리")
- **모사 없음** — 실제 분말 · 실제 장치.  "입자" 는 측정 분포의 중앙값 (d50) 으로만 들어간다.
- 덩어리 = "고전단 지름 (입자) 과 저전단 지름 (덩어리) 의 비" 로 정의한 **겉보기 부피비** — 모양 · 충전율 · δ_v 는 따로 재지 않는다.
- Λ₁₂ = Part I 의 **입자 탐침–결정 평판** 떼는 힘 비 → 실제 혼합의 입자–입자 (약물 4 µm 급 – lactose 10 µm 급) 곡률 기하는 들어 있지 않다 (Part I 카드 §4-3 과 같은 한계).

### 4-3. 기법 미니 용어집
- **DPI (dry powder inhaler)** — 운반체 + 미분 약물 분말을 들숨으로 흩어 폐로 보내는 흡입기.
- **TSI (twin-stage impinger)** — 공력 지름으로 두 단에 나눠 받는 충돌기.  2 단 = 미세 (여기서 6.4 µm 미만).
- **FPF (fine particle fraction)** — 미세입자 분율 (이 논문의 정의 미인쇄 — §3-7).
- **방출 (emission)** — 장치를 떠난 몫.
- **Aerosizer / Aerodisperser** — 비행시간으로 공력 지름을 재는 장치 / 시료를 전단으로 흩는 앞단.  압력 강하 = 전단 세기.
- **환산 혼합 계수 Λ₁₂ (reduced intermixing coefficient)** — 재료 1 이 재료 2 에 붙는 힘 ÷ 재료 1 자기 응집 힘.  > 1 이면 상호작용 혼합물을 잘 만든다.
- **상호작용 혼합물 (interactive mixture)** — 미분이 운반체 표면에 붙은 혼합물 (용어의 원전 쪽 = 같은 날 카드 [`egermann1983_ordered_vs_interactive_mixture_nomenclature`](egermann1983_ordered_vs_interactive_mixture_nomenclature.md)).
- **준안정 덩어리 (metastable agglomerate)** — 결합력과 분산력이 맞서 더 이상 깨지지 않는 덩어리 크기.

---

## 5. Figure set ★ (크롭 15 장 = `litdb/figures/begat2004_cohesive_adhesive_balance_partII_fine_particle_delivery/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | SEM (×1,800 · 10 µm 막대) — A lactose (불규칙 결정 + 잔 조각) · B salbutamol (성긴 덩어리 · 바늘 조각) · C budesonide (**치밀한 덩어리**) · 배너 A · C = 15KV, B = 10KV [판독] | 응집 구조가 물질마다 다르다 — 두 약물 대비의 교락 요인 |
| 2 | 겉보기 덩어리 부피비 (log) vs 응집 비 — 세 점 · y = e^0.2471x | ★ 응집 세기 ↔ 덩어리 크기의 단조 관계 (세 점) — 우리 SE 군집 크기 ↔ SE–SE Bo 관측량의 형식 |
| 3 | 약물만 TSI 침착 (장치 · 목 · 1 단 · 2 단) — A salbutamol · B budesonide | 역설 (응집 센 쪽이 고저항 장치에서 2 단 41.9 %) |
| 4 | 탈응집 · 분산 모식 — 약한 응집 = 작은 준안정 덩어리 · 강한 응집 = 큰 덩어리가 더 깨짐 | ★ "살아남는 덩어리 크기" 개념도 (논지 §2-4) |
| 5 | 혼합물 SEM (×4,000 · 1 µm 막대) — A salbutamol 이 lactose 면에 고르게 · B budesonide 가 덩어리째 고르지 않게 | ★★ 논지 P1 · P2 의 그림 문법 (자유 미분 덩어리 vs 표면에 흩어진 미분) |
| 6 | 운반체 제형 TSI 침착 — A salbutamol + lactose · B budesonide + lactose | 운반체가 FPF 를 바꾸는 방향이 Λ 와 장치에 따라 다르다 |
| Table I | 레이저 입도 d16 · d50 · d84 | 크기비 산술 (≈ 2–2.5) |
| Table II | 공력 입도 고 · 저전단 | 덩어리 부피비 산술 |
| Table III | Λ₁₂ 3 × 3 (대각 제외) | ★ 판가름 수 행렬 — Part I Table II 와의 항등 관계 (§12) |
| Table IV | FPF · 방출 | 하류 성능 지표 |
| 식 크롭 | (1) 덩어리 부피 · (2)–(3) 항력 · 운동에너지 · (4) Λ₁₂ | 정의 |
| 문단 크롭 2 | p.1830 Λ₁₂ 정의 · 해석 (interactive mixture) · p.1830 SEM + 함량 RSD | 인용 문장의 증거 |

## 6. Post-processing ★
- **원문**: 분포의 중앙값 · 16/84 백분위 (대수정규) · 평균 ± SD (n = 3 또는 5) · p < 0.05 (검정 방법 미기재 [미확인]) · Fig 2 지수 맞춤 · Λ 는 Part I 자료에서 계산.
- **안 한 것**: 혼합 시간 · 강도 변화 · 함량 균일도 시료 수 기재 · FPF 정의 · 덩어리 모양 · 충전 · 습도 변화 · 같은 약물의 표면 처리 비교 · 운반체 크기 변화 (고전적 63–90 µm 은 일부러 뺌).
- **이 카드에서 한 것**: Fig 2 점 3 · Fig 3 · 6 막대 32 판독 (`digitized.csv`) · 덩어리 부피비 · 크기비 · 배수 산술 · FPF 정의 역산 · Table III ↔ Part I Table II 항등 확인 · 지수 맞춤의 R² 재계산.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 쪽 수치는 주 리포 출처를 병기)

| 항목 | 이 논문 (Begat 2004 II) | 우리 (믹서 DEM · 논지) | 차이 / 판정 |
|---|---|---|---|
| 가르는 수 | Λ₁₂ = F^ad / F^co (평판 AFM 비) · 기준 1 | 논지 §2-8 판가름 수 F_SE–AM / F_SE–SE (기준 1, 돌기 지배) 또는 γ_A/γ_S < 0.31 (매끈한 구 · 기하평균) | ★ 같은 꼴 — Begat 은 기하를 약분한 비, 논지는 곡률 기하 (1.8 배) 를 따로 곱한다 |
| 혼합 결과 | Λ > 1 → 고르게 (RSD 4.2 %) · Λ < 1 → 덩어리 (28.1 %) | P1 (비코팅 = SE–SE 응집 남음) · P2 (코팅 = 응집 사라짐) | 방향 같음 · **두 다른 물질** 의 대비 (n = 2) |
| 모델 쌍 점착 | (측정 비만) | AM–SE CED = min 규칙 → 같은 γ 기하 환산보다 2.2 배 약함 · SE–SE Bo_code 0.212 (논지 §2-6) | ⚠ Begat 언어로 LC 의 SE 조각은 Λ_힘 ≈ 1.8 / 2.2 ≈ 0.8 — "꺼림" 쪽 [우리 산술 · 추정 — §8-1] |
| 혼합 조건 | Whirlimixer + Turbula 46 rpm 30 min (한 조건) | 회전 드럼 · bin 1 · 3 · 7 (V2 계획) | Begat 은 시간 축 없음 |
| 미분 함량 | 약물 50 wt% (1 g + 1 g) | SE ≈ 18 wt% (믹서 생성기) · V3 = 희박 한 수준 추가 계획 | Begat 은 단층 수용량을 훨씬 넘는 쪽일 가능성 [추정 — 밀도 미인쇄라 산술 불가] |
| 크기비 | 운반체 / 약물 ≈ 2–2.5 (레이저) | AM_P / SE ≈ 9 · AM_S / SE ≈ 4 (믹서 생성기 지름 9 · 4 · 1 µm — `scripts/make_mixer_deck.py`) | Begat 쪽이 더 작다 — "한두 자릿수" 조건 밖에서도 Λ ≫ 1 이면 상호작용 혼합물이 섰다 (SEM 1 장 · RSD) [추정] |
| 하류 지표 | FPF (흡입 분산) — 혼합 품질과 같은 순서가 아님 | P3 = 압축 뒤 SE 경로 (관통 · coverage · f_ion) | ⚠ "잘 섞임 → 하류가 좋음" 은 따로 보여야 한다 |

### 7-1. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 쌍별 점착 비 (Λ) → 혼합 상태 (SEM · 함량 RSD) 의 **실험 대응 한 쌍** · 응집 세기 ↔ 덩어리 크기의 세 점 관계.
- **없는 것**: 모사 · 입자 수준 관측 · 시간 변화 · 압축 · 수송 · 배터리 소재.

---

## 8. ★★ 우리 작업에 주는 것

### 8-1. 믹서 DEM 캠페인 (점착 · Bond 수 · AM–SE 부착)
1. **판가름 수의 이름과 읽는 법을 빌릴 수 있다 — Λ (환산 혼합 계수).**  논지 §2-8 의 F_SE–AM / F_SE–SE 는 Begat 의 Λ₁₂ (재료 1 = SE · 재료 2 = AM) 와 같은 꼴이다.  Begat 은 평판 비 (기하 약분) 로 1 을 기준 삼는다.  우리 매끈한 구 기하를 얹으면 SE→AM 부착 : SE–SE = 1.8 × Λ_평판 (AM_S 1.6 ×) 이므로 **Λ_평판 > 0.56 (AM_S 0.63) 이면 SE 가 AM 쪽** [우리 산술 — 논지 §2-3 의 1.8 · 1.6 사용] · 돌기 지배면 기준 1 (Part I 카드 §7-1 과 같은 결론).
2. **★ 지금 덱의 코팅 팔 (LC) 은 Begat 기준으로 '꺼림' 쪽일 수 있다.**  논지 §2-6: AM–SE 점착은 min 규칙이라 같은 γ 기하 환산 (SE→AM 1.8 배) 보다 2.2 배 약하다 ⇒ LC 에서 SE 조각의 F_SE–AM / F_SE–SE ≈ 1.8 / 2.2 ≈ **0.8** (AM_P 기준 어림 · AM_S 는 따로 확인 필요) [우리 산술 · 추정].  Begat 의 budesonide (0.22) 만큼은 아니지만 1 아래 — **"코팅하면 SE 가 AM 으로 흩어진다" (P2) 가 모델에서 덜 나올 구조적 이유** 를 다른 언어로 다시 확인 (논지 §3-4 · Part I 카드 §7-3 과 같은 결론).  → 논지 D2 (결합 규칙) 결정의 근거 묶음에 추가.
3. **덩어리 크기 ↔ 응집 세기 = 우리 SE 군집 관측량의 형식.**  Begat Fig 2: 응집 비 1 → 14 → 32 에 겉보기 덩어리 부피비 1.9 → 27 → 2567 [판독].  → 믹서 DEV 스캔에서 **SE 군집 크기 분포 (s1 의 연결 성분 크기) 를 SE–SE Bo 에 대해** 그리면, P1 의 "남는 응집" 은 0 이 아닌 **준안정 군집 크기** 로 나타나야 한다 [추정].  지금 덱의 SE–SE (Bo_code 0.212 · 충돌에서 붙는 속도 상한 ≈ 0.16 mm/s, 논지 §2-6) 는 사실상 안 붙는 가루라 그 크기가 생길 수 없다 → D3 (SE–SE 수준 앵커) 가 먼저.  새 관측량이면 **결과 전 등록** 대상.
4. **"F_coh = F_분산" 균형 = 논지 §2-4 ("충돌 에너지보다 접착 에너지가 큰 접촉만 살아남는다") 의 공력판.**  Begat 은 항력 ∝ Φ² · 운동에너지 ∝ Φ³ 로 큰 덩어리가 더 잘 깨진다고 본다 [인쇄].  드럼에서도 덩어리 질량 (∝ Φ³) 에 비례하는 충돌 에너지와 파단면 접촉 수 (∝ Φ²) 에 비례하는 결합의 경쟁이면 **최대 안정 군집 크기** 가 생긴다 [추정 — 형식 유비 · 우리 드럼에서 확인 안 됨].

### 8-2. 믹서 논문 계획 (`docs/mixer_paper_pipeline_draft_20261013.md` — 1저자 검토 전 초안) — V1 · V2 · V3
- **V1 코팅 상태**: 코팅이 바꾸는 것 = Λ_SE→AM (논지: 코팅 → γ_A = γ_S → Λ_평판 = 1).  ⚠ Begat 의 두 약물은 Λ 가 **77 배** (0.22 ↔ 16.88) 차이 나서 RSD 가 6.7 배 갈렸다 — 우리 비코팅 ↔ 코팅의 Λ 차이는 논지 문턱 근처라면 2 배 안팎이다 (Λ_평판 0.56 ↔ 1) [우리 산술] ⇒ **Begat 의 대비 크기를 우리 코팅 대비의 크기로 옮기지 않는다** — V1 의 모델 스캔은 "γ 비 → 지표" 환산표로 (초안 §1-2 P2 행과 같은 방향).
- **V2 혼합 시간**: Begat 은 한 조건뿐 — *"budesonide would require an intensive mixing process"* [인쇄] 는 **강도** 에 관한 예측이고 시간 축은 없다 ⇒ P1 의 *"혼합 시간을 늘려도"* 는 이 논문으로 지지도 반박도 안 된다.  우리 V2 (강도 고정 · bin 1 · 3 · 7) 설계는 그대로.
- **V3 SE 함량**: Begat 의 1 : 1 혼합은 미분 과잉 쪽 (Hersey 의 "남는 미분") 이라 budesonide 의 덩어리에 과잉 미분 몫이 섞였을 수 있다 [추정 — 밀도 미인쇄로 단층 수용량 산술 불가].  → 우리 V3 축이 바로 그 과잉 몫을 정한다 — 코팅 효과 (Λ) 와 과잉 미분 (함량) 을 **같은 조성 하나로 가르지 말 것** (`hersey1975_ordered_mixing_concept` §8 항목 2 와 같은 결론).
- **하류 (P3 · Fig 5 · 6 계획)**: Begat 에서 혼합 품질 (salbutamol 이 더 고름) 과 하류 성능 (약물만이면 budesonide FPF 가 더 높음) 의 순서가 갈렸다 ⇒ **"분산이 좋다 → SE 경로가 좋다" 를 가정하지 말고 압축 · 망으로 직접 보여야 한다** (초안 §1-2 P3 행 · D8 이식의 필요성).

### 8-3. 논지 비준 블록 (`docs/hetero_thesis.md` THESIS:BEGIN ~ END) 과의 대조
| 블록 요소 | 이 논문 | 판정 |
|---|---|---|
| 고정 문장 — *"상 간 표면 에너지 차이로 생기는 혼합 응집(특히 SE–SE)이 줄어 분산이 좋아지고"* | 응집 > 접착 (Λ 0.22) 인 미분은 같은 혼합 뒤 덩어리 · 불균일 (RSD 28.1 %) · 접착 > 응집 (Λ 16.88) 인 미분은 고르게 (4.2 %) [인쇄] | **방향 지지 (제약 분체 사례 · 두 다른 물질 · n = 2)** — 표면 에너지 자체는 재지 않았다 (힘 비) |
| P1 (비코팅 = 혼합 시간을 늘려도 상별 응집이 무작위보다 크게 남는다) | 시간 축 없음 · 무작위 기준 없음 | **시험 안 됨** |
| P2 (코팅 = AM 표면이 SE → 응집 사라짐) | 표면 처리 비교 없음 · 저자는 "계면 에너지를 바꿔 과한 응집 결합을 줄이는" 최적화 방향만 제안 (p.1832) | **개념 일치 · 시험 안 됨** |
| P3 (혼합 상태 차이 → 압축 뒤 SE 경로 차이) | 하류 = 흡입 분산 — 혼합 품질과 하류 순서가 갈림 | **무관 · 경고** (하류 고리는 따로 보여야 한다) |
| ⚠ P1 선행 조건 (비코팅 NCM 과 SE 의 표면 에너지 관계) | Λ₁₂ = 측정 가능한 형식 (AFM 떼는 힘 비) | **측정 형식 제공** (Part I 카드 §7-1 · §7-4) |
- 블록이 *"하지 않는 말"* 로 정한 문장은 이 카드에서 빌리지 않았다.  Begat 의 결과를 코팅 효과의 크기로 옮기지 않는다 (두 다른 약물의 대비다).

---

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
> 아래 영문은 원문 내용을 **우리가 다시 쓴 문장** 이다 (괄호 쪽이 근거).  원문 그대로가 필요하면 마지막 줄의 짧은 원문 구절만 쓴다.
- "Begat et al. (Pharm. Res. 2004, part II) defined a reduced intermixing coefficient Λ12 = F_adhesion(1–2)/F_cohesion(1–1) from AFM colloid-probe force balances; a drug with Λ12 = 16.88 spread uniformly over a fine lactose carrier (content RSD 4.2 %), whereas one with Λ12 = 0.22 remained agglomerated and unevenly distributed (RSD 28.1 %)." [인쇄 p.1830]
- "In drug-only formulations, the more cohesive drug gave the higher fine particle fraction from a high-resistance inhaler (63.4 % vs 13.7 %), which the authors attributed to the larger drag force and kinetic energy acting on larger agglomerates (Begat et al. 2004)." [인쇄 Table IV · p.1829–1830]
- 원문 구절 (그대로): *"the alacrity (Λ12 > 1) or the reluctance (Λ12 < 1) of the active particles to form an interactive mixture with the carrier particles"* (p.1830).
- ⚠ §8 의 우리 덱 산술 (≈ 0.8 · 0.56 · 77 배 ↔ 2 배) 은 [우리 산술 · 추정] — 원문 값으로 인용하지 말 것.

## 10. ⚠ 레드 플래그 (원문 비판 · over-claim 방지)
1. **본문 ↔ 표 숫자 불일치**: 본문 *"The emission efficiency of salbutamol sulfate-lactose formulations (81.9% ± 3.3%)"* (p.1831) ↔ Table IV salbutamol + lactose Rotahaler **81.3 ± 3.3** (81.9 는 salbutamol 만 · Turbuhaler 의 값) [인쇄 대조].
2. **그림 ↔ 표 불일치**: Fig 3B budesonide 만 · Turbuhaler 장치 막대 ≈ 29.5 % → 방출 ≈ 70.5 % [판독] ↔ Table IV **64.8 %** (≈ 6 %p) · Fig 6B Turbuhaler 도 68.9 vs 66.3 (≈ 2.6 %p) — 다른 여섯 경우는 ±0.5 %p 안.
3. **재료 표기 불일치**: Materials = *"Sorbalac 400 lactose from Meggle"* · 혼합 절 = *"1 g of Lactochem lactose"* (p.1826) — 어느 lactose 로 섞었는지 [미확인].
4. **SEM 조건**: 방법 = 10 keV · Fig 1A · C 배너 = 15KV [인쇄 + 판독].
5. **Fig 2 표기 · 맞춤**: y 축 *"density (R/r)³"* ↔ 캡션 *"volume"* ↔ 본문 *"apparent aerodynamic volume ratio"* · x 축 *"depedency"* (오식) · **세 점에 한 매개변수 지수 (원점 고정)** — 인쇄 R² 0.999 는 선형 공간에서 budesonide 한 점이 지배 (로그 공간 0.993) [우리 산술] · lactose 점 27.0 [판독] ↔ Table II 세제곱 22.4 [우리 산술].
6. **Λ 값의 출처가 Part I 본문과 다르다**: budesonide→lactose Λ 0.22 = Part I Table II (7.00/31.76) · Part I 본문 3.84 로 하면 0.26 / lactose→salbutamol 1.19 = Table II · Part I 본문 1.22 [우리 산술] — Part II 는 일관되게 **Table II 값** 을 쓴다 (§12).  Table III 의 SD (예 16.88 ± 0.91) 는 Part I Table II 의 SD (± 0.85 · ± 1.06) 와 다르다 — 전파 방법 [미확인].
7. **문장 ↔ 표**: *"the performance of the carrier-based formulation was analogous to the drug-only formulation"* (salbutamol, p.1831) 인데 Table IV 의 FPF 는 **두 배** (6.2 → 12.6 · 13.7 → 28.4) — 방출 · 침착 양상을 말한 것으로 읽힌다 [추정].
8. **FPF 정의 미인쇄** — 판독 역산으로 2 단 ÷ 방출 [추정].
9. **n 이 작다**: TSI n = 3 · Λ n = 3 (Part I 탐침 3 개) · 함량 균일도 시료 수 [미확인] · 약물 2 종.
10. **조건의 특수성**: 운반체 = 미세 lactose (≈ 10 µm) · 1 : 1 질량 · 35 % RH 의 Part I 비 (모세관 몫 분리 안 됨 — Part I 카드 §10-6) — 고전적 DPI (63–90 µm 운반체 · 약물 소량) 로도 바로 옮길 수 없다.
11. **초록의 "various shear forces"** = 실제로 두 수준 (1 · 5 psi).
12. **참고문헌 14 (Part I) 서지 불완전** (학술지 · 권 · 쪽 없음) · 참고문헌 3 저자명 *"N. M. Concession"* · 7 *"De boer. I. Winter"* 등 인쇄 그대로 [인쇄 p.1832].

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 13 | J. N. Staniforth, J. E. Rees, F. K. Lai, and J. A. Hersey. Interparticle forces in binary and ternary ordered powder mixes. J. Pharm. Pharmacol. 34:141–145 (1982). | 'ordered' 혼합의 입자 간 힘 — 같은 계보 (Hersey) · 카드 없음 |
| 14 | P. Begat, D. A. V. Morton, J. N. Staniforth, and R. Price. The cohesive-adhesive balances in dry powder inhaler formulations I: Direct quantification by atomic force microscopy. | ✅ [`begat2004_cohesive_adhesive_balance_afm_colloid_probe`](begat2004_cohesive_adhesive_balance_afm_colloid_probe.md) (원문 목록은 학술지 · 권 · 쪽 없음) |
| 16 | N. Laitinen and A. M. Juppo. Measurement of pharmaceutical particles using a time-of-flight particle sizer. Eur. J. Pharm. Biopharm. 55:93–98 (2003). | 전단 의존 공력 입도 (덩어리 판정 방법) |
| 17 | W. C. Hinds. Aerosol Technology: Properties, Behaviour and Measurements of Airborne Particles, Wiley, New York, 1999. | 식 (2)–(3) 항력 · 운동에너지 출처 |
| 18–20 | R. C. Rowe. Binder substrate interactions in granulation—a theoretical approach based on surface free-energy and polarity. Int. J. Pharm. 52:149–154 (1989). · R. C. Rowe. Surface free-energy and polarity effects in the granulation of a model system. Int. J. Pharm. 53:75–78 (1989). · R. C. Rowe. Polar non-polar interactions in the granulation of organic substrates with polymer binding-agents. Int. J. Pharm. 56:117–124 (1989). | ★ reduced spreading coefficient (Λ₁₂ 의 원형) — 표면 에너지 → 접착일 비 → 공정 거동의 선례 · 카드 없음 |
| 6 · 11 | X. M. Zeng, G. P. Martin, S. K. Tee, and C. Marriott. The role of fine particle lactose on the dispersion and deaggregation of salbutamol sulphate in an air stream in vitro. Int. J. Pharm. 176:99–110 (1998). · X. M. Zeng, G. P. Martin, S. K. Tee, A. Abu Ghoush, and C. Marriott. Effects of particle size and adding sequence of fine lactose on the deposition of salbutamol sulphate from a dry powder formulation. Int. J. Pharm. 182:133–144 (1999). | 미세 운반체 효과 |

## 12. ★ Part I ↔ Part II 연결 (이 카드의 대조 · Part I 카드는 고치지 않음)

| 항목 | Part I (`begat2004_cohesive_adhesive_balance_afm_colloid_probe`, p.1591–1597) | Part II (이 카드, p.1826–1833) | 연결 |
|---|---|---|---|
| 무엇을 재나 | AFM 콜로이드 탐침 떼는 힘 · 같은 탐침의 자기/상대 평판 비 (CAB) · 3 원계 교차 정규화 Table II | CAB → **Λ₁₂** (식 4) · 혼합 · 분산 실험 | Part II 의 Λ = Part I 의 출력 |
| salbutamol→lactose | Table II 16.88 · Fig 9 기울기 0.0593 (= 1/16.86) | Λ **16.88 ± 0.91** | 같은 값 |
| lactose→salbutamol | 본문 1.22 · Fig 9 기울기 0.8371 (= 1/1.195) · Table II 16.88/14.13 = 1.195 | Λ **1.19 ± 0.42** | Table II · 그림 기울기 쪽 (본문 1.22 아님) |
| budesonide→lactose | 본문 **3.84** (→ Λ 0.26) · Fig 8 인쇄 회귀 4.5371 (→ 0.2204) · Table II 7.00/31.76 = 0.2204 | Λ **0.22 ± 0.21** | Table II · 인쇄 회귀 쪽 (본문 3.84 아님) |
| lactose→budesonide | 본문 **2.36** (→ 0.424) · Fig 8 인쇄 회귀 2.0186 (→ 0.4954) · Table II 7.00/14.13 = 0.4954 | Λ **0.5 ± 0.31** | 같은 패턴 |
| salbutamol↔budesonide | Table II 6.59 (salbutamol 응집 = 1) · 6.59/31.76 = 0.2075 | Λ 6.59 ± 0.21 · 0.21 ± 0.13 | 같음 |
| 응집의 위계 | Table II 대각 1.00 ± 0.08 · 14.13 ± 1.06 · 31.76 ± 1.53 | Fig 2 x 값 · 오차막대 (판독 1.00 · 14.12 (13.06–15.18) · 31.75 (30.21–33.29)) | 같은 값 |
| 혼합 예측 | *"poor blend homogeneity unless a significant amount of shear energy was introduced"* (budesonide) · salbutamol 은 *"homogenous blend"* — 예측만 | SEM + 함량 RSD 4.2 % vs 28.1 % | ★ Part I 예측의 **부분 검증** (n = 2 · 한 혼합 조건) |
- [우리 산술] 정리: **Part II Table III = Part I Table II 의 각 행을 그 행의 대각원소로 나눈 값** — 저자들이 정본으로 쓰는 값은 Part I 의 **교차 정규화 행렬** 이다.  Part I 카드 §10-1 이 [추정] 으로 적은 *"Fig 8 의 인쇄 회귀식은 Table II 에서 거꾸로 계산한 숫자"* 와 같은 방향의 근거.

## 다른 카드 정정 후보 (보고만 — 이 커밋에서 고치지 않음)
1. **`begat2004_cohesive_adhesive_balance_afm_colloid_probe` (Part I) 머리말** *"II 편 원문은 받지 않았다 [미확인]"* → 이 카드로 연결 (교차 링크 한 줄).
2. **같은 카드 §10-9** *"혼합 예측은 검증되지 않았다 … (II 편 [미확인])"* → Part II 가 SEM + 함량 RSD (4.2 % vs 28.1 %) 로 **부분 검증** (두 약물 · 한 조건) — 한정어와 함께 갱신 후보.
3. **같은 카드 §10-1 [추정]** (인쇄 회귀식 = Table II 역산) → Part II Table III 가 Table II 값을 정본으로 쓴다는 근거 추가 후보 (§12).
4. **같은 카드 §7-1** *"budesonide 는 CAB 3.84"* · **§3-3** 본문 값 1.22 → Part II 는 Λ 0.22 (= 1/4.54) · 1.19 를 쓴다 — 두 값 계열 (본문 vs Table II) 을 같이 적는 편이 안전.
5. **`comparison_vs_ours_DEM.md` §H-11** (Part I) → Part II 포인터 한 줄 (공용 파일 — 다른 세션이 한 커밋으로).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 8 쪽 전부 쪽 이미지 (200 · 300 dpi) 로 읽고 `pdftotext` 로 표 · 인용문 대조.  식 (1)–(4) 와 "10² · 10³" 위첨자는 이미지에서 확인 (텍스트층은 "102 · 103" 으로 깨진다).
- Fig 2 = 원 래스터 (960 × 692 · 1-bit) 에서 축 눈금 검출 → 점 중심 · 오차막대 판독 · Fig 3 · 6 = 원 래스터 (480 px JPEG) 에서 막대 윗변 (내부 폭 85 % 이상 채워진 첫 줄) · 오차막대 끝 판독 → Table IV 와 대조 (§3-7).
- 크롭 15 장 = Fig 1–6 + Table I–IV + 식 3 + 문단 2 (전부 손 크롭 · 300 dpi) · 쪽 머리글이 걸린 Fig 5 · 6 은 위 경계를 내려 다시 자름.
- 정본 litdb 중복 확인: 파일 목록 + "Begat" · "fine particle delivery" · "intermixing" `git grep` — Part II 카드 없음.

## 🔗 관련 카드
- 같은 연작: [`begat2004_cohesive_adhesive_balance_afm_colloid_probe`](begat2004_cohesive_adhesive_balance_afm_colloid_probe.md) (Part I — CAB 측정 · 결합 규칙 시험 · min 규칙 충돌).
- 용어 (interactive mixture): [`egermann1983_ordered_vs_interactive_mixture_nomenclature`](egermann1983_ordered_vs_interactive_mixture_nomenclature.md) (같은 날) · [`hersey1975_ordered_mixing_concept`](hersey1975_ordered_mixing_concept.md) · [`pfeffer2001_dry_particle_coating_engineered_particulates`](pfeffer2001_dry_particle_coating_engineered_particulates.md).
- 점착 → 혼합 · 분리: [`jarray2019_cohesion_driven_mixing_segregation_drum`](jarray2019_cohesion_driven_mixing_segregation_drum.md) (한 상만 점착 → 분리) · [`alizadeh2018_dem_adhesion_calibration_segregation_heap`](alizadeh2018_dem_adhesion_calibration_segregation_heap.md).
- 접착 이론: [`johnson1971_jkr_surface_energy_contact_elastic_solids`](johnson1971_jkr_surface_energy_contact_elastic_solids.md) · [`dmt1975_adhesion_contact_deformation`](dmt1975_adhesion_contact_deformation.md).
- SE 코팅 NCM (실물): [`nakamura2020_dry_coating_ncm_li3ps4_core_shell`](nakamura2020_dry_coating_ncm_li3ps4_core_shell.md) · [`kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage`](kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage.md).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
