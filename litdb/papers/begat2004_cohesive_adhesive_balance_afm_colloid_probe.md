<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 이웃 = faka2026_particle_size_consolidation_strain_lpscl.md · 같은 묶음 = johnson1971_jkr_surface_energy_contact_elastic_solids.md.
     원문 = 7 쪽 (본문 6 + 참고문헌) · SI 없음 · 쪽 표기 = 인쇄 쪽 (PDF n 쪽 = p.(1590 + n)).
     그림은 PDF 안에 144 ppi JPEG 로 들어 있다 (원 래스터 480 px 폭) — 크롭은 캡션까지 300 dpi 로 렌더 (그림 자체는 원 해상도 이상 정보 없음).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 인쇄 숫자 / [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv · 원 래스터 픽셀) /
     [우리 산술] = 원문 값으로 한 계산 / [추정] = 우리 해석 / [미확인] = 원문에 없음. -->
# The Cohesive-Adhesive Balances in Dry Powder Inhaler Formulations I: Direct Quantification by Atomic Force Microscopy — AFM 콜로이드 탐침 한 개를 "자기 물질" 결정면과 "상대 물질" 결정면에 번갈아 대어 **떼는 힘의 비 (CAB)** 를 잰다 — 탐침마다 다른 접촉 기하 (R\*) 를 비로 지우고 응집 ↔ 접착 균형만 남기는 법 (budesonide · salbutamol sulfate · α-lactose) — Begat · Morton · Staniforth · Price (Pharm. Res. 2004)

> slug `begat2004_cohesive_adhesive_balance_afm_colloid_probe` · DOI `[미확인]` · type `experiment (AFM colloid-probe pull-off forces on engineered smooth single-crystal substrates · cohesive–adhesive balance (CAB) graph · ternary cross-normalisation)` · PDF `93bb0fa4-36._The_cohesive-adhesive_balances_in_dry_powder_inhaler_formulations_I_direct_quantification_by_atomic_force_microscopy.pdf` · digested `2026-10-13` · status ✅
>
> **서지 (원문 인쇄)**: Philippe Begat¹ · David A. V. Morton² · John N. Staniforth² · Robert Price¹,³\* — ¹ Pharmaceutical Technology Research Group, Dept. of Pharmacy & Pharmacology, University of Bath · ² Vectura Ltd, Chippenham · ³ 교신 (r.price@bath.ac.uk) · *Pharmaceutical Research* **21** (9), 1591–1597, September 2004 · Research Paper · Received 2004-02-20 · accepted 2004-05-18 · 판권 줄 "0724-8741/04/0900-1591/0 © 2004 Springer Science+Business Media, Inc." [인쇄 p.1591].
> ⚠ **DOI 는 PDF 에 인쇄돼 있지 않다** (본문 · 판권 줄 · PDF 메타 검색 0 건) → `[미확인]`.  판권 줄의 "0724-8741/04/0900-1591/0" 은 판권 코드이지 DOI 형식이 아니다.
> ⚠ 제목의 "I" — 연작 1 편이다.  II 편 원문은 받지 않았다 [미확인].
> ★ **이 카드가 맡는 일** — 이종기술 논지 (`docs/hetero_thesis.md`) §2-8 *"AFM 콜로이드 탐침으로 NCM–NCM · NCM–SE · SE–SE 떼는 힘"* 의 **측정 틀 원형**.  CAB 비는 논지의 판가름 수 (F_SE–AM / F_SE–SE) 를 결합 규칙 없이 **직접** 준다.
> **판독 원자료**: `litdb/figures/begat2004_cohesive_adhesive_balance_afm_colloid_probe/digitized.csv` (36 행 — Fig 4–6 막대 27 · Fig 8 점 6 · 그려진 회귀선 기울기 3).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 같은 입자 탐침 하나로 "자기 물질" 과 "상대 물질" 의 매끈한 결정면 (Ra 0.7–2.3 nm) 을 각각 4,096 번 눌렀다 떼어 평균 떼는 힘을 얻고, 그 **비 F_A–A / F_A–B** 를 탐침 여러 개로 그려 (CAB 그래프) 기울기로 응집 ↔ 접착 균형을 정량한다 — 탐침 크기 · 모양 (접촉 반경 R\*) 은 비에서 지워진다는 가정이다 [인쇄 p.1595].
결과: salbutamol sulfate–lactose 는 **접착 우세** (혼합 잘 됨 예측) · budesonide–lactose 는 **응집 우세** (분리 · 불균일 예측) [인쇄 p.1596].

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ★ 무엇을 재나 | **떼는 힘 F (nN)** — 캔틸레버 휨으로 F = −kz · 탐침–기판 한 쌍마다 4,096 곡선 평균 (가우스 분포) · **CAB 비 = F_A–A/F_A–B** (같은 탐침) · γ · W 의 **절대값은 내지 않는다** ("quantification of force measurements was precluded, as it would require normalization through the determination of the probe-substrate contact area") | [인쇄] p.1593 · 1595 |
| CAB 비의 이론 근거 | 식 (3): F_A–A/F_A–B = R\*_A–A[nπW_A–A + (4πγ_water cos θ_A–A + 4πγ_A–water)] / R\*_A–B[nπW_A–B + (…)] — 두 기판의 접촉 반경이 같다고 보면 비는 **물질 성질 (W · 젖음)** 만의 함수 | [인쇄] p.1595 |
| 떼는 힘 모델 | 식 (1) F_vdw = nπR\*W_ad · n = **3/2 (JKR) · 2 (DMT)** · W_ad = "thermodynamic work of adhesion (mJ·m⁻²)" · 식 (2) 모세관 힘 F_c = 4πR\*γ_L cos σ + 4πR\*γ_SL (Fisher & Israelachvili) | [인쇄] p.1591 |
| 시료 조건 | 기판 = 반용매 재결정 단결정 (주결정면) · 거칠기 Ra 0.681 / 2.258 / 1.837 nm (budesonide / salbutamol sulfate / lactose) · 탐침 = 미처리 입자를 무팁 캔틸레버에 에폭시 (**물질당 n = 3**) · k = 0.282 ± 0.039 N/m · **25 °C · 35 % RH** · 누름 40 nN · 2.5 × 2.5 µm 격자 · 4 Hz | [인쇄] p.1593 · Table I |
| ★ 결과 수치 | budesonide–lactose: 응집이 접착의 **3.84 배 (budesonide 탐침) · 2.36 배 (lactose 탐침)** · salbutamol–lactose: 접착이 salbutamol 응집의 **16.88 배** · lactose 응집의 **1.22 배** · 3 원계 교차 정규화 (Table II, salbutamol 응집 = 1.00): lactose 응집 14.13 · budesonide 응집 31.76 | [인쇄] p.1596 · Table II |
| ⚠ 내부 불일치 | Fig 8 인쇄 회귀식 **y = 4.5371x · y = 2.0186x** ↔ 본문 3.84 · 2.36 ↔ 그림의 점 · 그려진 선 [판독] **≈3.87–3.9 · ≈2.37–2.4** — 인쇄 회귀식은 **Table II 비 (31.76/7.00 · 14.13/7.00)** 와 같다 (§10-1) | [인쇄] + [판독] + [우리 산술] |
| ★ 기하평균 결합 규칙이 맞나 | 원문은 시험하지 않는다.  CAB 두 개의 곱 = W_AA·W_BB/W_AB² (같은 기하 가정) 가 1 이면 기하평균 성립 — **budesonide–lactose 9.06 · salbutamol–lactose 0.050** → 기하평균 대비 W_AB 가 **0.33 배 · 4.49 배** | [우리 산술] |
| 공기 민감 황화물에 쓸 수 있나 | 원문 밖.  습도 제어 (35 % RH) 가 모세관 항을 키우는 조건 — 황화물은 건조 · 불활성 분위기 AFM 이 필수 → 모세관 항 0 · 대신 정전기 위험 (원문은 정전기를 "없거나 소산" 가정) · 기판을 고압 펠릿으로 만들면 표면 비정질화 우려 (원문이 바로 그 이유로 결정 기판을 썼다) | [인쇄] p.1591–1592 + [추정] |

⛔ **한정어 (떼지 말 것)**: ① 의약 분말 (유기 분자 결정) · 25 °C · 35 % RH — 무기 산화물 · 황화물과 표면 화학이 다르다 ② 탐침 **3 개**/물질 · 탐침 크기 [미확인] ③ CAB 는 **비** 만 준다 — W 의 절대값 · 표면 에너지 γ 는 없다 ④ "두 기판의 접촉 반경이 같다" 는 가정은 CAB 직선성 (R² 0.85–0.99) 으로 간접 확인했을 뿐 ⑤ Fig 8 · Table II 의 수치 일부는 서로 맞지 않는다 (§10).

---

## 1. 한 줄 요약
흡입 건분말 (carrier lactose + 미분 약물) 의 혼합 · 분리 · 분산은 입자 사이 응집 (같은 물질) 과 접착 (다른 물질) 의 균형이 정한다.  그런데 AFM 콜로이드 탐침의 떼는 힘은 탐침마다 접촉 면적이 달라 절대 비교가 안 된다.
저자들은 ① 기판을 나노미터 평활 단결정 주결정면으로 만들어 기판 쪽 변동을 없애고 ② **같은 탐침**으로 자기 물질 · 상대 물질 기판을 재서 **비** 를 보며 ③ 탐침 여러 개의 (접착, 응집) 점을 원점 지나는 직선으로 맞춰 (CAB 그래프) 기울기 = 균형으로 정량한다.
salbutamol sulfate–lactose 는 접착 우세 (탐침들이 대각선 아래), budesonide–lactose 는 응집 우세 (대각선 위) — 3 원계를 salbutamol 응집 = 1 로 교차 정규화한 행렬 (Table II) 을 낸다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| P. Begat · D. A. V. Morton · J. N. Staniforth · **R. Price\*** (Univ. Bath · Vectura Ltd) | Pharm. Res. **21** (9) 1591–1597 (2004) · 접수 2004-02-20 · 승인 2004-05-18 | `[미확인]` (PDF 미인쇄) | **budesonide** (Sicor, batch 6157/MI) · **salbutamol sulfate** (Becpharm, batch 940077) · **α-lactose monohydrate** (Sorbalac 400, Meggle) — 배터리 소재 아님 | 실험 (AFM 콜로이드 탐침 · 단결정 기판 · SEM · 결정 습성 모사) |

| 원문 구조 | 쪽 | 내용 |
|---|---|---|
| 초록 · Introduction | 1591–1592 | 점착 기전 (반데르발스 · 모세관 · 정전기) · 식 (1)–(2) · 거칠기 · 접촉 면적 문제 · 압밀 기판의 비정질화 우려 |
| Materials and Methods | 1592–1593 | 재결정 (Fig 1) · SEM · SHAPE 습성 모사 · AFM 지형 (Ra · Rq) · 힘 측정 조건 |
| Results | 1593–1594 | SEM (Fig 2) · AFM 지형 (Fig 3 · Table I) · 힘 (Fig 4–6) |
| Discussion | 1594–1596 | CAB 이론 (식 3 · Fig 7) · lactose/budesonide (Fig 8) · lactose/salbutamol (Fig 9) · 교차 정규화 (Table II) |
| Conclusions · References (26) | 1596–1597 | |

- 중복 확인 (2026-10-13): 정본 `litdb/papers/` 전수 목록에 begat 파일 없음 · `git grep -i` "Begat" · "cohesive-adhesive balance" · "cohesive–adhesive balance" 0 건 → 새 카드.

---

## 3. 핵심 수치 (★ 쪽 · 표지 병기)

### 3-1. 시료 · 기판 · 측정 조건 [인쇄]
| 항목 | 값 | 쪽 |
|---|---|---|
| 기판 결정화 | 포화 용액 (budesonide/에탄올 · salbutamol sulfate/물 · lactose/물, 20 °C 12 h 진탕 · 0.22 µm 여과) 한 방울 (≈1 ml) 을 12 × 12 mm 커버슬립에 · 반용매 (budesonide 는 물 · 나머지 둘은 에탄올) 증기 평형으로 **커버슬립 위 불균일 핵생성** (Fig 1) · 시료 전처리 불필요 | 1592 |
| 결정 · 주결정면 | budesonide 사방정 P2₁2₁2₁ (a 8.550 · b 9.406 · c 28.401 Å) · 길쭉한 12 면체, 주면 (012) · (01̄2) / salbutamol sulfate 단사정 Cc (a 28.069 · b 6.183 · c 16.914 Å, β 81.19°) · 바늘, 주면 (200) / α-lactose monohydrate 단사정 P2₁ (a 7.982 · b 21.562 · c 4.824 Å, β 109.57) · 도끼 (tomahawk), 주면 (100) · (11̄0) — SHAPE V7.0 모사 | 1592–1593 |
| 지형 | TM-AFM (Nanoscope IIIa · Multimode · J 스캐너 · OTSP 캔틸레버) · 2.5 × 2.5 µm 에서 Ra · Rq · "no observable modification … over large areas (>20 µm²)" | 1593 |
| **Table I 거칠기** | Rugosity (Ra) **0.681 / 2.258 / 1.837 nm** · RMS (Rq) **0.872 / 3.142 / 2.284 nm** (budesonide / salbutamol sulfate / α-lactose) — "well below 5 nm" | 1594 |
| 탐침 | 입자 (**물질당 n = 3**, 미처리) 를 무팁 V 자 캔틸레버 (DNP-020) 에 에폭시 (Araldite) · 탐침 입자 크기 **[미확인]** ("micron sized") | 1593 |
| 캔틸레버 상수 | 열잡음법 **k = 0.282 ± 0.039 N/m** | 1593 |
| 환경 | 환경 챔버 **25 °C (±0.2)** · **35 % RH (±3)** · 맞춤 관류 장치 + 습도 센서 (Rotronic) | 1593 |
| 힘 곡선 | **n = 4,096** / 탐침–기판 쌍 · 2.5 × 2.5 µm 격자 · 주사 4 Hz · **누름 40 nN** · 전 연구 고정 | 1593 |
| 통계 | 일원 ANOVA + Fisher 쌍별 비교 · 99 % 신뢰 | 1593 |
| 기판 위치 | 각 물질의 **주결정면** · 매 실험 같은 영역에 탐침 | 1593 |

### 3-2. ★ 떼는 힘 (Fig 4–6) [판독 — 원 래스터 막대 높이, ±1.2 nN]
| 탐침 \ 기판 | lactose | salbutamol sulfate | budesonide |
|---|---|---|---|
| budesonide 탐침 1 · 2 · 3 (Fig 4) | 80.0 · 52.2 · 44.0 | 61.4 · 44.0 · 35.9 | **299.0 · 204.0 · 178.5** |
| salbutamol sulfate 탐침 1 · 2 · 3 (Fig 5) | **163.4 · 155.3 · 132.1** | 11.6 · 11.6 · ≈8 (육안) | 67.2 · 61.4 · 51.0 |
| lactose 탐침 1 · 2 · 3 (Fig 6) | 181.9 · 143.7 · 119.4 | **221.4 · 172.7 · 137.9** | 70.7 · 61.4 · 52.1 |
- 본문 판정 (p<0.01): budesonide 탐침 = 응집 (budesonide 기판) 이 압도 · lactose 접착 > salbutamol 접착 / salbutamol 탐침 = 응집이 극히 약함 · lactose 접착 > budesonide 접착 / lactose 탐침 = salbutamol 접착 > lactose 응집 > budesonide 접착 [인쇄 p.1594].
- ⇒ **탐침 사이 산포 (기하 효과) 가 크다** — 같은 물질 탐침 셋이 같은 기판에서 1.2–1.8 배 다르다 [판독 · 우리 산술] — 이것이 저자가 절대값 대신 비를 쓴 이유 (p.1594).

### 3-3. ★ CAB 그래프 (Fig 8 · 9) [인쇄 + 판독]
| 계 · 탐침 | 본문 (p.1596) | 그림 안 인쇄 회귀식 | [판독] 그림의 점 · 그려진 선 | [우리 산술] 막대 (Fig 4–6) 원점 회귀 |
|---|---|---|---|---|
| lactose/budesonide · budesonide 탐침 | 응집 = 접착의 **3.84 배** · R² 0.9873 | **y = 4.5371x** · R² 0.9873 | 점 (43.8, 177.3) · (52.3, 203.0) · (79.2, 301.8) → 3.87 · 선 ≈3.9 | **3.84** |
| lactose/budesonide · lactose 탐침 | **2.36 배** · R² 0.9910 | **y = 2.0186x** · R² 0.991 | 점 (50.6, 118.5) · (61.1, 143.2) · (70.2, 168.8) → 2.37 · 선 ≈2.4 | 2.43 (Fig 6 의 탐침 1 응집 181.9 ↔ Fig 8 점 168.8) |
| lactose/salbutamol · lactose 탐침 | 접착이 lactose 응집의 **1.22 배** · R² 0.9938 | **y = 0.8371x** (= 1/1.195) | — | 0.834 (= 1/1.20) |
| lactose/salbutamol · salbutamol 탐침 | 접착이 salbutamol 응집의 **16.88 배** · R² 0.8537 | **y = 0.0593x** (= 1/16.86) | — | (작은 막대라 불확실) |
- 해석 (p.1596): budesonide–lactose 는 "poor blend homogeneity unless a significant amount of shear energy was introduced … possibly … segregation over time" · salbutamol–lactose 는 "should not require an excessive amount of energy to generate a homogenous blend".

### 3-4. ★ Table II — 3 원계 교차 정규화 (salbutamol sulfate 응집 = 1.00) [인쇄]
| 탐침 \ 기판 | salbutamol sulfate | α-lactose monohydrate | budesonide |
|---|---|---|---|
| salbutamol sulfate | 1.00 ± 0.08 | 16.88 ± 0.85 | 6.59 ± 0.00 |
| lactose | 16.88 ± 1.06 | 14.13 ± 1.06 | 7.00 ± 1.6 |
| budesonide | 6.59 ± 0.32 | 7.00 ± 1.6 | 31.76 ± 1.53 |
- 비대각 원소 ‡ p < 0.01 · *"The coefficient of proportionality with respect to salbutamol sulfate for lactose and budesonide is 14.13 and 31.76"* = **응집의 위계 budesonide > lactose > salbutamol** [인쇄 p.1596].
- [우리 산술] 각 수가 어디서 왔나 (재구성): lactose 응집 14.13 = 16.88 × 0.8371 (Fig 9 두 기울기) ✓ · budesonide 응집 31.76 = 6.59 × **4.82** (4.82 = Fig 4 막대의 budesonide 응집/budesonide–salbutamol 원점 회귀) ✓ · lactose–budesonide 7.00 ± 1.6 ≈ 두 경로 31.76/3.84 = **8.27** 과 14.13/2.36 = **5.99** 의 평균 7.13 · 표준편차 1.61 [추정 — 원문은 산출 경로를 적지 않았다].

---

## 4. ★ 방법 — 측정 사슬 · 식 · 입자 처리

### 4-1. 식 (원문 그대로 · 크롭 `eq_01_02_vdw_capillary.png` · `eq_03_cab_ratio.png`)
- (1) **F_vdw = nπR\*W_ad** — "R\* is the harmonic mean of the particle radii (also called contact radius), W_ad is the thermodynamic work of adhesion (mJ·m⁻²), and n … (n = 3/2 for JKR and n = 2 for the DMT)" [인쇄 p.1591].
- (2) **F_c = 4πR\*γ_L cos σ + 4πR\*γ_SL** — γ_L 물 표면장력 · γ_SL 고–액 계면 자유에너지 · θ 측정 접촉각 (식에는 σ 로 인쇄 — §10-4) [인쇄 p.1591].
- (3) **F_A–A / F_A–B = R\*_A–A[nπW_A–A + (4πγ_water cos θ_A–A + 4πγ_A–water)] / R\*_A–B[nπW_A–B + (4πγ_water cos θ_A–B + 4πγ_A–water)]** — "with constant environmental conditions, the work of adhesion and contact angle are only dependant on the material physical characteristics … the only parameters which are susceptible to vary are the contact radii … Assuming the similarity of the two tailored substrate surface contact radii, the cohesion-adhesion ratios for a number of interacting probes of a specific material should theoretically remain constant" [인쇄 p.1595].

### 4-2. 측정 사슬
재결정 단결정 기판 (주결정면) → TM-AFM 으로 Ra · Rq 확인 → 입자 3 개를 캔틸레버에 붙여 탐침 → k 열잡음 보정 → 25 °C · 35 % RH 챔버 → 탐침–기판 쌍마다 2.5 × 2.5 µm 격자 4,096 곡선 (40 nN 누름 · 4 Hz) → 떼는 힘 분포 가우스 맞춤 → 평균 ± SD (Fig 4–6) → 탐침별 (접착, 응집) 을 CAB 그래프에 → 원점 지나는 선형회귀 기울기 = CAB 비 (Fig 8–9) → salbutamol 응집 = 1 로 교차 정규화한 3 × 3 행렬 (Table II).

### 4-3. ★ 입자 처리 (DEM 판 "무질서 처리")
- **실제 입자 (미처리, 불규칙) 하나 = 탐침** — 형상 · 거칠기 · 접촉점 수는 모른다 (그래서 비를 쓴다).  기판은 원자 수준에 가까운 평판 (Ra < 2.3 nm).
- 따라서 측정되는 것은 "그 탐침의 돌기 기하 × 물질 쌍의 W" 이고, CAB 는 기하를 약분해 **물질 쌍의 W 비 (+ 모세관 항)** 만 남기려는 설계다.
- ⚠ 입자–입자 (구–구) 접촉이 아니라 **입자–평판** 이다 — 실제 혼합에서 작은 입자가 큰 입자에 붙는 곡률 기하 (논지 §2-3 의 R\*) 는 이 측정에 들어 있지 않다.

### 4-4. 기법 미니 용어집
- **콜로이드 탐침 (colloid probe)**: 무팁 캔틸레버 끝에 입자를 붙인 AFM 탐침 — 입자–표면 힘을 직접 잰다 (Ducker 1991, ref 11).
- **떼는 힘 (pull-off / separation force)**: 후퇴 곡선의 최대 인장력 = k × 최대 휨.  lee2026 AFM-FS 의 **W_ad (aJ) = 후퇴 곡선 음의 면적 (에너지)** 과 다른 양이다.
- **CAB 비**: 같은 탐침의 F(자기 물질 기판)/F(상대 물질 기판).  > 1 응집 우세 · < 1 접착 우세.
- **CAB 그래프**: x = 접착력 · y = 응집력 · 탐침마다 한 점 · 대각선 (F_adh = F_coh) 위 = 응집 우세 영역.
- **교차 정규화 (cross-normalisation)**: 공통 원소 (salbutamol 응집) 를 1 로 두고 이진계 기울기들을 곱해 3 원계 행렬을 만든다 — 경로가 여럿이면 **닫힘 (loop closure)** 이 검사가 된다 (§7-3).
- **Ra · Rq**: 중심선 대비 평균 · 제곱평균 높이 편차 (rugosity · RMS).

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 반용매 재결정 장치 (A 포화 용액 방울 · B 유리 슬라이드 · C 반용매 접시 · D 비커) | 평활 기판 만드는 법 — 황화물은 용액 재결정이 어렵다 [추정] |
| 2 | SEM (×400, 10 µm 막대) + SHAPE 모사 습성 · Miller 지수 (budesonide · salbutamol · lactose) | 주결정면 선택 — NCM 단결정 입자의 면 선택에 대응 |
| 3 | TM-AFM 진폭상 (0.5 µm 막대) 세 결정면 | 기판 평활도 확인 절차 |
| 4 | budesonide 탐침 3 개 × 기판 3 (막대 + 오차) — 응집 (budesonide) 178–300 nN | ★ 탐침 사이 기하 산포 1.7 배 — 절대값 비교가 왜 안 되나 |
| 5 | salbutamol 탐침 × 기판 — 응집 ≈ 8–12 nN · lactose 접착 132–163 nN | 접착 우세 극단 (W_AB ≫ W_AA) |
| 6 | lactose 탐침 × 기판 | 세 물질 사이 위계 |
| 7 | CAB 그래프 개념 — 탐침 A 들은 대각선 위 (F_adh ≪ F_coh) · 탐침 B 들은 아래 | ★ 논지 판가름 실험의 그림 문법 |
| 8 | lactose/budesonide CAB — 인쇄 회귀식 4.5371 · 2.0186 (⚠ 점 · 선과 불일치) | ★ 응집 우세 예 · 내부 불일치 사례 (§10-1) |
| 9 | lactose/salbutamol CAB — 0.8371 · 0.0593 | ★ 접착 우세 예 (W_AB > W_AA · W_BB) |
| Table I (1) | 거칠기 Ra · Rq | 기판 요건 (< 5 nm) |
| Table II (2) | 3 원계 CAB 행렬 | ★ 결합 규칙 시험 재료 (§7-2) |
| 식 크롭 | eq (1)–(2) — 반데르발스 (JKR · DMT) · 모세관 | 정의 |
| 식 크롭 | eq (3) — CAB 비 | 기하 약분 가정 |

## 6. Post-processing ★
- **원문**: 4,096 곡선 → 가우스 맞춤 평균 ± SD · ANOVA + Fisher (99 %) · CAB 원점 회귀 + R² · 교차 정규화 (산출 경로 미기술).
- **안 한 것**: 탐침 크기 · 형상 · 접촉 면적 · W 절대값 · 표면 에너지 측정 (IGC · 접촉각) · 습도 변화 · 정전기 확인 · 반복 탐침 수 > 3.
- **이 카드에서 한 것**: Fig 4–6 막대 27 개 · Fig 8 점 6 개 · 그려진 회귀선 기울기 판독 (`digitized.csv`) · 막대로 원점 회귀 재계산 · Table II 재구성 · 결합 규칙 시험 (§7-2).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 쪽 수치는 리포 출처를 병기)

### 7-1. ★ 논지 §2-8 의 판가름 실험으로 옮기면
- 논지의 판가름 수 = 비코팅 NCM 에서 **SE 조각이 SE 에 붙는 힘 vs NCM 에 붙는 힘** (F_SE–AM / F_SE–SE, §2-3 의 3).  CAB 는 이것을 **같은 SE 탐침**으로 SE 평판 · NCM 평판에서 재어 비로 준다: **CAB_SE = F_SE–SE / F_SE–NCM ≈ W_SS / W_SA** (평판 기하 · 같은 탐침 → R\* 약분 가정).
- 같은 방식으로 NCM 탐침: CAB_NCM = W_AA / W_AS.  **결합 규칙 (기하평균) 을 가정하지 않고** W 비 둘을 얻는다.
- 판정 (논지 §2-3 의 매끈한 구 기하를 얹을 때) [우리 산술]: 실제 혼합의 SE→NCM 부착 : SE–SE = 1.8 × (W_SA/W_SS) = 1.8 / CAB_SE (AM_P 기준 · AM_S 는 1.6) ⇒ **CAB_SE > 1.8 (AM_S 1.6) 이면 SE–SE 응집이 살아남는다** (논지 P1 쪽) · 그보다 작으면 SE 가 NCM 쪽으로.  접촉이 돌기 반경 지배면 (JKR 카드 §7-4) 문턱은 **CAB_SE > 1** [추정].
- 이 논문의 두 극단을 같은 문법으로 읽으면: salbutamol (탐침) 은 CAB 0.059 (자기보다 lactose 에 17 배 잘 붙음) = "코팅 / 정렬 혼합" 쪽 극단 · budesonide 는 CAB 3.84 = "자기끼리 응집" 쪽 극단.

### 7-2. ★ 기하평균 결합 규칙의 시험 — 이 논문 자료로 [우리 산술]
- 같은 기하 가정 아래 **CAB_A × CAB_B = W_AA·W_BB / W_AB²** — 기하평균 (W_AB = √(W_AA·W_BB)) 이면 정확히 1.
- budesonide–lactose: 3.84 × 2.36 = **9.06** → W_AB = 기하평균의 **0.33 배** · salbutamol–lactose: 0.0593 × 0.8371 = **0.050** → **4.49 배**.  Table II 로도 lactose–budesonide 7.00/√(14.13 × 31.76) = **0.33** · salbutamol–lactose 16.88/√(1.00 × 14.13) = **4.49** · salbutamol–budesonide 6.59/√31.76 = **1.17**.
- ⇒ 이 계 (유기 결정 · 35 % RH · 친수 ↔ 소수) 에서 **기하평균 규칙이 양방향으로 3–4.5 배 틀린다**.  친수끼리 (salbutamol sulfate–lactose) 는 기하평균보다 강하게, 친수–소수 (lactose–budesonide) 는 약하게 붙는다 — 극성 (산 · 염기 / 수소결합) · 모세관 항의 흔적으로 읽힌다 [추정].
- 우리에게: 논지 §2-1 의 W_ij ≈ 2√(γ_i·γ_j) 와 그 위에 세운 **γ_A/γ_S < 0.31** 문턱은 이 규칙에 기댄다 — **결합 규칙을 가정하지 말고 CAB 를 직접 재는 쪽이 판가름에 맞다** (논지 §2-7 "극성 성분 — 기하평균이 깨질 수 있다" 의 실례).

### 7-3. ★ 믹서 덱 혼합쌍 규칙 (min) 과의 충돌 [우리 산술 · 추정]
- 우리 믹서 덱의 혼합쌍 CED = 두 상 후보 CED 의 **min** (`scripts/make_mixer_deck.py` `ced_matrix` — 겹침 보수 규칙).  같은 E\* · R\* 이면 CED 와 W 는 단조 대응 (JKR 카드 §7-1: W ∝ CED³ R\*/E\*²) 이므로 min 규칙은 대략 **W_AB ≤ min(W_AA, W_BB)** 세계만 표현한다.
- 이 논문의 salbutamol–lactose 는 W_AB = 16.88 > W_LL 14.13 > W_SS 1.00 (Table II) — **접착이 두 응집보다 큰 쌍** 이고, 이것이 바로 "작은 입자가 큰 입자를 덮는" 정렬 · 상호작용 혼합의 조건이다.  min 규칙에서는 이 쌍이 W_SS 수준 (1.00) 으로 **17 배 약하게** 들어간다.
- ⇒ 논지 D2 (결합 규칙) 결정에 주는 것: 측정된 CAB 행렬 → W_ij → **JKR 대응식으로 CED_ij** (johnson1971 카드 §7-1) 로 바로 내려야 하고, min 규칙은 코팅 · 정렬 혼합 상태를 구조적으로 표현할 수 없다.  ⬜ 결정 = 1저자.

### 7-4. 측정 설계 메모 — NCM · 황화물 SE 에 적용하려면 [추정 — 원문 밖]
| 요소 | 이 논문 | NCM ↔ LPSCl 에서 |
|---|---|---|
| 분위기 | 25 °C · 35 % RH (모세관 항 존재) | **건조 · 불활성 (Ar 글러브박스 · 드라이룸) AFM 필수** — LPSCl 은 수분과 반응.  모세관 항 = 0 → 식 (3) 이 W 비로 단순해진다 · 대신 **정전기** 소산을 확인해야 한다 (원문의 전제) |
| 기판 | 용액 재결정 단결정 주결정면 (Ra < 2.3 nm) | NCM: 단결정 입자의 결정면 또는 연마 소결체 · LPSCl: 큰 단결정 확보 어려움 → 연마 펠릿이 현실적이나 원문은 **고압 압밀 기판의 결함 · 비정질 영역이 표면 에너지를 바꾼다** 고 경고 (p.1592) — 황화물은 무르고 밀링 · 압축에 민감 |
| 탐침 | 미처리 입자 · 물질당 3 개 | NCM 2차입자 (≈9 µm) · SE (≈1 µm) — 1 µm SE 를 탐침으로 붙이기는 어렵다 → 큰 SE 입자 사용 (크기 효과 주의) |
| 반복 · 검사 | 탐침 3 · 4,096 곡선 · R² · ANOVA | 탐침 수 확대 · **3 원계 (NCM · SE · 탄소) 닫힘 검사** — 이 논문은 lactose–budesonide 두 경로가 8.27 vs 5.99 (38 % 차) 로 안 닫혔다 |
| 표면 상태 | 결정면 그대로 | NCM 잔류 리튬염 · LPSCl 산화 · 가수분해 층 — **측정 전 이력 기록** (논지 §2-3 ⚠ 와 같은 축) |
| 접촉 시간 · 속도 | 4 Hz 고정 | JKR 원문이 경고한 속도 의존 (johnson1971 카드 §10-6) — 고정 · 기록 |

### 7-5. 기존 정본 카드와의 관계
- `lee2026_mechanical_halogen_argyrodite_drycoating` (사용자 공저): 카드 기록상 (원문 미대조) 그 논문의 AFM-FS 는 **실리콘 팁 ↔ 433 MPa 연마 SE 펠릿**의 F–D 맵 · W_ad = 후퇴 곡선 음의 면적 (aJ) — **팁–SE 접착 에너지**이지 NCM–SE 의 CAB 가 아니다.  NCM–SE 계면의 W_ad (J/m²) 는 그 논문에서 계산 (MLIP) 값이다.  ⇒ CAB 형 측정 (NCM 탐침 · SE 탐침) 은 아직 우리 쪽 근거에 없다.
- `hare2026_dem_pept_dry_mixing_nmc622_eirich` · `lischka2025_dem_eirich_intensive_mixer_dry_mixing`: 그 논문들의 γ 는 분말 유동 보정값 — 이 논문 방식의 직접 측정이 아니다.
- `johnson1971_jkr_surface_energy_contact_elastic_solids`: 식 (1) 의 n = 3/2 원전 · W 규약 (두 표면 합) · CED 대응식.
- `otani2025_dem_se_dispersion_aggregation_compression` (JKR γ 0.1 균일): 같은 γ 를 모든 쌍에 — 이 논문이 보여 준 쌍별 비대칭 (0.33–4.49 배) 을 담지 못한다.

### 7-6. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 입자–평판 떼는 힘의 **물질 쌍 비교 (비)** — 우리 믹서 DEM 의 쌍별 점착 입력 (D2) 에 들어갈 실험 앵커의 형식.
- **없는 것**: 절대 W · γ · 입자–입자 곡률 기하 · 혼합 · 압밀 · 수송.  배터리 소재 자료 없음.

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **판가름 실험의 설계도** — SE 탐침 · NCM 탐침을 SE 평판 · NCM 평판에 대어 CAB_SE · CAB_NCM 을 잰다 (건조 · 불활성).  CAB_SE > 1.8 (매끈한 구 기하) 또는 > 1 (돌기 지배) 이면 논지 P1 쪽.
2. **결합 규칙을 재지 말고 시험하라** — CAB_A × CAB_B = 1 이 기하평균의 검사식이다.  이 논문 계에서는 0.050 · 9.06 으로 양쪽으로 깨졌다.
3. **min 혼합쌍 규칙은 "접착 > 두 응집" 을 못 낸다** — 코팅 · 정렬 혼합을 모델에 넣으려면 쌍별 W 를 직접 넣어야 한다 (D2).
4. **3 원계 닫힘 검사** — 교차 정규화 경로가 여럿이면 서로 맞는지가 "같은 기하" 가정의 품질 검사다 (이 논문은 38 % 어긋남).
5. **압밀 기판 경고** — 황화물 펠릿 표면은 비정질 · 결함 · 반응층으로 표면 에너지가 바뀔 수 있다 (원문 p.1592 의 우려를 그대로 적용) → 기판 이력 · 평활도 (Ra) 기록.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Begat et al. (Pharm. Res. 2004) quantified cohesive–adhesive balances with AFM colloid probes on nanometre-smooth single-crystal substrates (Ra 0.7–2.3 nm), comparing the pull-off force of the same probe on its own material and on a second material, so that the unknown contact geometry cancels in the ratio."
- "In their data the salbutamol sulfate–lactose adhesion exceeded the salbutamol sulfate cohesion 16.9-fold (adhesive-dominant), whereas budesonide cohesion exceeded budesonide–lactose adhesion ≈3.8-fold (cohesive-dominant)."
- 국문: *"CAB 두 개의 곱은 같은 기하에서 W_AA·W_BB/W_AB² 이다 — Begat 2004 자료로는 0.05 와 9.1 로, 기하평균 결합 규칙이 양쪽으로 3–4.5 배 틀린다 (우리 산술)."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. ★ **Fig 8 의 인쇄 회귀식이 그림 · 본문과 안 맞는다**: 인쇄 y = 4.5371x · 2.0186x ↔ 본문 3.84 · 2.36 ↔ 그림의 점 원점 회귀 3.87 · 2.37 · 그려진 점선 기울기 ≈3.9 · ≈2.4 [판독 — 대각선은 1.00–1.03 으로 보정 확인].  인쇄 회귀식 = Table II 의 31.76/7.00 = 4.537 · 14.13/7.00 = 2.019 [우리 산술] — 표에서 거꾸로 계산한 숫자가 그림에 붙은 것으로 보인다 [추정].
2. **Table II 의 lactose–budesonide (7.00 ± 1.6) 는 두 경로 평균으로 보인다** — budesonide 탐침 경로 8.27 · lactose 탐침 경로 5.99 (38 % 차) [우리 산술 · 추정] → "같은 기하" 가정이 3 원계에서 ±20 % 수준으로만 닫힌다.  salbutamol–budesonide 의 "6.59 ± 0.00" (SD 0) 도 설명이 없다.
3. **Fig 6 ↔ Fig 8 한 점 불일치**: lactose 탐침 1 의 응집력 Fig 6 막대 181.9 nN ↔ Fig 8 점 168.8 nN (7 %) [판독].
4. **인쇄 결함**: 식 (2) 의 "cos σ" (본문은 θ) · Fig 8 · 9 캡션 "Comparison between forces of adhesion and force of adhesion" (응집 · 접착이어야) · "R\* is the harmonic mean of the particle radii (also called contact radius)" — R\* = R₁R₂/(R₁+R₂) 는 조화평균의 **절반**이고 접촉 반경 (a) 이 아니다 · ref 13 (JKR) 이 "Jonhson … 324:301–303" 로 인쇄 (실제 301–313 — johnson1971 카드 원문 대조).
5. **탐침 크기 · 형상 · 접촉 면적 [미확인]** · 물질당 탐침 3 개 — CAB 기울기의 통계 기반이 얇다 (R² 0.85 인 salbutamol 탐침 선 포함).
6. **35 % RH** — 모세관 항이 식 (3) 에 들어 있다.  친수 물질 (salbutamol sulfate · lactose) 쌍의 큰 접착에 모세관 몫이 얼마인지 분리 안 됨 → 건조 조건 W 비로 그대로 옮기면 안 된다.
7. **정전기는 가정으로 제외** ("in the absence of any significant electrostatic force or upon complete dissipation") — 측정으로 확인한 서술 없음.
8. **"이론 추정이 실측보다 수 자릿수 크다 · 실제 접촉 면적이 훨씬 작다"** (p.1594–1595) — 인용 (refs 25, 26) 근거의 일반론, 이 논문의 측정 아님.
9. **혼합 예측은 검증되지 않았다** — "poor blend homogeneity" · "homogenous blend" 는 CAB 로부터의 예측이고 실제 혼합 시험은 이 논문에 없다 (II 편 [미확인]).

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 2 | N. M. Ahfat, G. Buckton, R. Burrows, and M. D. Ticehurst. Predicting mixing performance using surface energy measurements. Int. J. Pharm. 156:89–95 (1997). | 표면 에너지 (IGC 계열) 로 혼합 예측 — 논지 §2-8 의 IGC 경로 |
| 3 | D. Cline and R. Dalby. Predicting the quality of powders for inhalation from surface energy and area. Pharm. Res. 19:1274–1277 (2002). | 표면 에너지 × 면적 → 분말 품질 |
| 7 | R. Price, P. M. Young, S. Edge, and J. N. Staniforth. The influence of relative humidity on particulate interactions in carrier-based dry powder inhaler formulations. Int. J. Pharm. 246:47–59 (2002). | 습도 효과 · 콜로이드 탐침 제작 상세 |
| 11 | W. A. Ducker, T. J. Senden, and R. M. Pashley. Direct Measurement of Colloidal Forces Using an Atomic Force Microscope. Nature 353:239–241 (1991). | 콜로이드 탐침 원전 |
| 13 | K. L. Jonhson, K. Kendall, and A. D. Roberts. Surface energy and the contact of elastic solids. Proc. Roy. Soc. London 324:301–303 (1971). | ⚠ 철자 · 쪽 오기 — 정본 `johnson1971_jkr_surface_energy_contact_elastic_solids` |
| 14 | B. V. Deryaguin, V. M. Müller, and Y. P. Toporov. Effect of contact deformations on the adhesion of particles. J. Colloid Interface Sci. 53:314–325 (1975). | 정본 `dmt1975_adhesion_contact_deformation` |
| 15 | L. R. Fisher and J. N. Israelachvili. Direct measurements of the effect of meniscus forces on adhesion … Colloids and Surfaces 3:303–319 (1981). | 모세관 식 (2) 원전 |
| 16 | E. R. Beach, G. W. Tormoen, J. Drelich, and R. Han. Pull-off force measurements between rough surfaces by atomic force microscopy. J. Colloid Interface Sci. 247:84–99 (2002). | 거칠기 ↔ 떼는 힘 |
| 17 | U. Sindel and I. Zimmermann. Measurement of interaction forces between individual powder particles using an atomic force microscope. Powder Technol. 117:247–254 (2001). | 분말 입자 AFM · 압밀 기판 |
| 18 | J. C. Hooton, C. S. German, S. Allen, M. C. Davies, C. J. Roberts, S. J. B. Tendler, and P. M. Williams. Characterization of particle-interactions by atomic force microscopy: Effect of contact area. Pharm. Res. 20:508–514 (2003). | 접촉 면적 정량 (Villarrubia 역상) |
| 25 · 26 | D. M. Schaefer et al. J. Adhes. Sci. Technol. 8:197–210 (1994) · 9:1049–1062 (1995). | 이론 ↔ 실측 수 자릿수 차 · 거칠기 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 7 쪽 전부 쪽 이미지로 읽고 `pdftotext` 로 인용문 대조.  식 (1)–(3) 은 이미지에서 옮겼다 (텍스트층은 그리스 문자가 깨진다).
- Fig 4–6 · 8 은 PDF 원 래스터 (pdfimages, 480 px) 에서 축 눈금을 검출해 판독 — 막대 27 · 점 6 · 그려진 선 기울기 (점선 단일 픽셀 추적, 대각선 1.00–1.03 으로 보정 확인).
- 크롭 13 장 = Fig 1–9 + Table I–II + 식 영역 2 (전부 손 크롭 · 300 dpi · 식 (3) 은 400 dpi).  자동 추출은 Fig 6 · 7 을 한 장으로 묶고 Fig 7 · 표 · 식을 놓쳐 손 크롭으로 통일했다.
- 정본 litdb 중복 확인: 파일 목록 + "Begat" · "cohesive-adhesive balance" `git grep` 0 건.

## 🔗 관련 카드
- 같은 묶음 (점착 · 표면 에너지): `johnson1971_jkr_surface_energy_contact_elastic_solids` · `dmt1975_adhesion_contact_deformation`.
- 우리 쪽 AFM: `lee2026_mechanical_halogen_argyrodite_drycoating`.
- 건식 혼합 DEM (γ 보정): `hare2026_dem_pept_dry_mixing_nmc622_eirich` · `lischka2025_dem_eirich_intensive_mixer_dry_mixing` · `otani2025_dem_se_dispersion_aggregation_compression` · `frankenberg2024_dem_high_intensity_mixer_assb`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
