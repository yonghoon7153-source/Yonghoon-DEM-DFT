<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 이웃 = roessler2019_dem_cohesive_aor_cylinder_lift_calibration.md.
     쪽 표기 = "p.N" (PDF N 쪽 = 인쇄 103+N · China Particuology 4(3–4) 104–107).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 인쇄 식 · [판독] = 그림에서 읽은 값 · 귀속 (litdb/figures/<slug>/digitized.csv) · [우리 산술] = 인쇄 식 · 값으로 다시 한 계산 · [미확인] = 원문 (본문 전수) 에 없음 · [추정] = 우리 해석.
     원문 = 본문 4 쪽 (SI 없음) — 텍스트 층 전수 · 그림 11 · 표 1 = 크롭 12 장 전부 열람. -->

# **안식각 (AOR) 으로 분말 유동성을 재는 소량 시험기** — Powder Research Ltd. Mark 4 (진동 경사판 → 깔때기 → 뒤판에 반원뿔 · 100 g) · AOR 과 Hausner 비 (HR) 가 직선 상관 (θ = 36.2 HR − 13.4 · 29.8 HR − 5.4, R² 0.97) · 7 µm 미분을 섞을수록 AOR · HR 이 Sauter 지름의 거듭제곱으로 오른다 (θ ∝ d_sv^−0.25) · Carr 분류 (< 30° 좋음 · 30–45° 약간 점착 · 45–55° 점착 · > 55° 매우 점착) — Geldart · Abdullah · Hassanpour · Nwoke · Wouters (China Particuology 2006)

> slug `geldart2006_powder_flowability_angle_of_repose_tester` · DOI `10.1016/S1672-2515(07)60247-4` (PDF 메타데이터 제목에 적힌 값 · 본문 쪽에는 DOI 인쇄 없음) · type `exp (powder flowability characterization — dynamic angle-of-repose tester, Hausner ratio; cohesive powder; no DEM)` · PDF `5a6475a4-44._Characterization_of_powder_flowability_using_measurement_of_angle_of_repose.pdf` · digested `2026-10-13` · status ✅
>
> **원제**: *Characterization of powder flowability using measurement of angle of repose* (p.1)
> **저자**: D. Geldart¹\* (prfgeldart@aol.com) · E. C. Abdullah² · A. Hassanpour³ · L. C. Nwoke³ · I. Wouters⁴ — ¹ Dept. of Chemical Engineering, Bradford · Leeds · Birmingham · Heriot-Watt Universities & Powder Research Ltd. (원문 표기 'Herriot-Watt') · ² University of Malaya · ³ University of Leeds · ⁴ Total Petroleum (p.1)
> *China Particuology* **4**(3–4) (2006) 104–107 · 접수 2005-12-14 · 승인 2006-04-02 (p.4).
> **판독 원자료**: `litdb/figures/geldart2006_powder_flowability_angle_of_repose_tester/digitized.csv` · 크롭 12 장 `figures.json`.
> **이 카드가 서랍에 들어온 이유**: 이종기술 논지 **D3** — "SE 분말 유동성 (안식각 · Hausner 비) 실험 앵커" 의 **측정 쪽 원전**.  같은 날 카드 [`roessler2019_dem_cohesive_aor_cylinder_lift_calibration`](roessler2019_dem_cohesive_aor_cylinder_lift_calibration.md) (같은 앵커의 DEM 보정 쪽) 와 짝 · 1저자 읽기 목록 `docs/mixer_coating_reading_list_20261013.md` B5-3 · §2 읽는 순서 9.

> ★★ **한 줄로 왜 중요한가**: 공기에 민감하고 비싼 SE 분말로 **유동성 앵커** 를 잡으려면 **시료가 적게 들고 (100 g, 50 g 도 시험) · 재현성 있고 (5 회 표준편차 0.3–2.0°) · 점착 분말에도 쓸 수 있는** 시험이 필요하다.  이 논문은 그런 시험기와, 그것이 **Hausner 비와 직선으로 맞는다** 는 것, 그리고 **AOR 은 측정 방법마다 값이 달라 서로 비교할 수 없다** 는 것을 보인다.
> ⚠ 단 **시험기 치수가 원문에 없다** (DEM 으로 재현하려면 장치를 직접 재야 한다) · 시료 = FCC · 수산화알루미늄 (7–79 µm) 혼합물 — µm SE 는 이 상관식의 범위 밖 (외삽 금지).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 진동하는 45° 경사판으로 분말을 흘려 깔때기 · 짧은 경사판을 거쳐 수직 뒤판 앞에 **반원뿔** 을 쌓고, 그 높이와 평균 반지름으로 **동적 AOR** 을 읽는 Mark 4 시험기 (100 g 권장) 로 FCC (구형 · 다공) 와 FRF (각진 수산화알루미늄) 에 7 µm 미분을 1–90 wt% 섞어 재니, AOR · HR 이 둘 다 Sauter 지름에 대해 거듭제곱으로 떨어지고 (AOR 55 → 27°, HR 1.85 → 1.1 [판독]), **AOR 은 HR 에 대해 직선** (R² 0.97) 이며, 시료를 200 · 150 g 에서 100 g 으로 줄이면 AOR 이 1–2° 오르지만 50 g 까지는 더 변하지 않았다 [인쇄 Fig 5–7 · Table 1].

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① **D3** — SE 유동성을 무엇으로 재나? | **동적 AOR (Mark 4) + Hausner 비 (탭 밀도 ÷ 통기 밀도)** — 둘이 같은 계열에서 직선 상관.  저자는 AOR 을 선호 (재기 쉽고 공정처럼 분말이 움직인다) | [인쇄] p.2 · p.4 |
| ② 판정 기준? | **Carr (1965 · 1970) · Raymus (1985)**: AOR < 30° 좋은 유동 · 30–45° 약간 점착 · 45–55° 점착 · > 55° 매우 점착 · 유동 매우 제한.  **40°** 를 자유 흐름 ↔ 점착 경계로 (Geldart 1990 · Antequera 1994) · **Geldart 분류**: HR < 1.25 = A · B · D 군 · 1.25–1.4 반점착 · > 1.4 점착 (C 군, 유동화 어려움) — 그런 분말의 AOR ≈ 40° | [인쇄] p.1 · p.3 |
| ③ 시료 양 (SE 는 적고 비싸다)? | **100 g 권장** (±1 g) · 50–150 g 에서 AOR 변화 작음 (avicel 38.4 · 38.3 · 37.0°) · 200 → 100 g 에서 starch +2.2° · "100 g 이 안 되면 **항상 같은 양**" | [인쇄] p.2 · p.4 · Table 1 |
| ④ AOR 값을 다른 논문 · 다른 시험과 **비교** 해도 되나? | **안 된다** — 정적 · 동적 AOR 측정법이 최소 8 가지이고 값이 서로 다르다 ("published values … seldom comparable", Brown & Richards 1970).  ⇒ 같은 날 카드들의 AOR (Jarray 드럼 동적 35–49° · Alizadeh 더미 31–57° · Roessler 원통 40–84°) 을 **한 축에 놓지 말 것** | [인쇄] p.1 |
| ⑤ 미분 함량 · 입경과의 관계? | θ ∝ d_sv^−0.25 (FCC: θ = 79.7 d_sv^−0.25 · FRF: 88.3 d_sv^−0.26) · HR ∝ d_sv^−0.2 (FCC 2.77 d_sv^−0.21 · FRF 2.65 d_sv^−0.19) [인쇄 식 · 곡선 귀속 판독].  AOR 40° 가 되는 d_sv ≈ **16 µm (FCC) · 21 µm (FRF)** [우리 산술] | [인쇄] Fig 5 · 6 |
| ⑥ µm SE 에 그 식을 쓸 수 있나? | **없다** — 맞춤 범위 7–79 µm.  1 µm 로 외삽하면 AOR 80–88° · HR 2.7–2.8 [우리 산술 · 외삽] = 이 시험이 다루는 범위 밖 · Roessler 2019 가 보인 "점착이 강하면 AOR 이 재현 안 됨" 영역일 수 있다 [추정] | [우리 산술] |
| ⑦ DEM 보정에 바로 쓸 수 있나? | **시험기 치수가 없다** (경사판 · 깔때기 · 뒤판 · 낙하 높이) → DEM 재현 장치를 만들려면 실물을 재야 한다 [미확인].  진동 (주파수 · 진폭) 조건도 미기재 | [미확인] |

⛔ **한정어 (떼지 말 것)**: ① 시료 = **FCC 촉매 · 수산화알루미늄 (7–79 µm)** + 소다회 · 중탄산나트륨 · 젖당 · starch · avicel — 황화물 SE · NCM 아님 ② **동적 AOR (반원뿔)** — 다른 방법의 AOR 과 값 비교 금지 ③ 상관식 = **이 두 재료 · 이 범위** 의 경험식 (재료마다 기울기 다름) ④ 시험기 치수 · 진동 조건 미기재.

---

## 1. 한 줄 요약

**산업 현장에서 "오늘 분말이 어제보다 잘 흐르나" 를 빠르게 재려고, 진동 경사판으로 분말을 흘려 뒤판 앞에 반원뿔을 쌓는 소량 (100 g) 동적 AOR 시험기 (Powder Research Ltd. Mark 4) 를 소개하고, FCC · FRF 에 7 µm 미분을 1–90 wt% 섞은 계열에서 AOR 이 Hausner 비와 직선으로 (R² 0.97) · Sauter 지름과 거듭제곱으로 맞음을 보인 짧은 방법 논문.**  여러 재료를 한 그래프에 모으려면 AOR 을 반원뿔 벌크 밀도로 나눈 "가중 AOR" (AOR/ρ_ba) 을 Sauter 지름에 대해 그린다.  시료 양은 100 g 이 표준편차가 가장 작았다.

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| D. Geldart (교신) · E. C. Abdullah · A. Hassanpour · L. C. Nwoke · I. Wouters | *China Particuology* 4(3–4) 104–107 (2006) | 10.1016/S1672-2515(07)60247-4 (PDF 메타데이터) | FCC (구형 다공 촉매 · 79 µm 기준) · FRF (각진 비다공 수산화알루미늄 · 63 µm 기준) + 7 µm 점착 미분 · 소다회 · 중탄산나트륨 · 젖당 · starch · avicel | **실험 방법** (유동성 시험기 · Hausner 비) — DEM 없음 |

> ★ **계보**: Geldart 분류 (1973, 유동화 거동의 A · B · C · D 군) 의 저자.  Bradford 대학에서 대형 화학회사 (소다회 공장) 와 함께 개발 · 공장 운전 경험과 대조 (p.2).  선행 = Geldart, Mallet & Rolfe 1990 (*Powder Handling & Proc.* 2(4) 341 — AOR 로 유동성 평가) · Abdullah & Geldart 1999 (*Powder Technol.* 102, 151 — 벌크 밀도 지표).  공저자 Hassanpour = 같은 날 카드 [`alizadeh2018_dem_adhesion_calibration_segregation_heap`](alizadeh2018_dem_adhesion_calibration_segregation_heap.md) 의 교신.

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. AOR 정의 · 분류 (§2 · Fig 1 · p.1–2)
| 항목 | 내용 | 표지 |
|---|---|---|
| 종류 | **정적 · 동적** 두 갈래 · 측정법 **최소 8 가지** · 값이 서로 달라 **문헌값은 거의 비교 불가** (Brown & Richards 1970) | [인쇄] p.1 |
| 흔한 네 방법 (Fig 1) | I **고정 높이 원뿔** (깔때기 높이 고정) · II **고정 바닥 원뿔** (깔때기를 올림) · III **기울이는 판** · IV **회전 원통** | [인쇄] p.2 · Fig 1 |
| I · II 의 한계 | 점착 분말은 작은 깔때기를 못 빠져나갈 수 있고, 공정처럼 **통기 (aerated)** 되지 않음 · 각도를 정확히 재기 어렵다 | [인쇄] p.2 |
| III · IV 의 한계 | 저마찰 축 · 베어링에 장착해 미끄러질 때까지 기울여야 · 청소 때 분해 → 느림 · 각 측정 어려움 | [인쇄] p.2 |
| **Carr · Raymus 기준** | **< 30° 좋은 유동 · 30–45° 약간 점착 · 45–55° 점착 · > 55° 매우 점착 · 유동 매우 제한** | [인쇄] p.1 |
| 40° 기준 | 자유 흐름 ↔ 점착 (Geldart 1990 · Antequera 1994, Brown & Richards 자료 근거) | [인쇄] p.1 |
| 설계 표준 부재 | "가장 좋은 설계 · 크기 · 시험 방법 · 최적 분말 양에 대한 합의가 없다" (Geldart 1990) | [인쇄] p.1 |

### 3-2. Mark 4 시험기 · 절차 (§2 · Fig 2 · p.2)
| 항목 | 내용 | 표지 |
|---|---|---|
| 구성 (Fig 2 모식) | **진동 경사판 (45°)** + 진동기 → **깔때기 (hopper)** → 짧은 **아래 경사판 (chute)** → **수직 뒤판 (backplate)** 앞 **받침판 (baseboard)** 에 **반원뿔** | [인쇄] Fig 2 |
| 시료 | **100 g 권장 · ±1 g** · 금속 비커에 계량 | [인쇄] p.2 |
| 자유 흐름 분말 | 위 수렴 경사판에 천천히 · 약 **20 s** 에 걸쳐 붓기 | [인쇄] p.2 |
| 점착 분말 | **진동기 켬** → 위 경사판 → 깔때기 → 아래 경사판 → 뒤판 쪽으로 · 깔때기에 쌓이지 않게 | [인쇄] p.2 |
| 판독 | 반원뿔의 **높이 · 평균 반지름** → 동적 AOR (계산 또는 표) · 꼭짓점이 날카로워야 · 너무 빨리 부어 꼭짓점이 '너덜하면' 천천히 다시 | [인쇄] p.2 |
| 검증 | 대형 **소다회 공장** 운전 경험과 대조 · 비숙련 현장 · 학부 실험에서도 신뢰 | [인쇄] p.1–2 |
| ⚠ 치수 · 진동 | 판 길이 · 깔때기 지름 · 낙하 높이 · 뒤판 크기 · 진동 주파수 · 진폭 **미기재** | [미확인] |

### 3-3. Hausner 비 (§2 · p.2)
- **HR = 탭 벌크 밀도 ÷ 통기 벌크 밀도** (Grey & Beddow 1969) — 점착 · 반점착 분말 특성화에 흔히 쓰는 또 하나의 간단한 방법.
- **Geldart 분류 (1973)** 대응: HR < 1.25 → A · B · D 군 (유동화 쉬움) · HR 1.25–1.4 반점착 · HR > 1.4 점착 · 유동화 어려움 (C 군) — 그런 분말의 AOR ≈ 40° (p.3).

### 3-4. 재료 (§3 · Fig 3 · 4 · p.2–3)
- **FCC**: 구형 · 다공 유동 접촉분해 촉매 · 기준 **79 µm** (Fig 3).
- **FRF**: 각진 · 비다공 수산화알루미늄 (난연 충전재) · 기준 **63 µm** (Fig 4).
- **7 µm 점착 미분** 을 질량% **1 · 2 · 5 · 10 · 20 · 40 · 50 · 60 · 70 · 80 · 90** 로 섞어 평균 입경 계열을 만듦.
- 이 계열의 실험 시료 양 = **200 g** (p.4).

### 3-5. 결과 (§4 · Fig 5–9 · p.3–4)
| 그림 | 결과 | 표지 |
|---|---|---|
| Fig 5 HR vs d_sv | 고운 쪽 두 재료 HR 비슷 (≈ 1.85) · 입경 ↑ → HR ↓ (점착 ↓).  **FRF: HR = 2.65 d_sv^−0.19 (R² 1.00) · FCC: HR = 2.77 d_sv^−0.21 (R² 0.99)** · 점선 HR 1.4 · 1.25 | [인쇄 식] · [판독 귀속] |
| Fig 6 AOR vs d_sv | AOR 55 → 27° 로 감소 · **FRF: θ = 88.3 d_sv^−0.26 · FCC: θ = 79.7 d_sv^−0.25 (R² 0.97 둘 다)** · 점선 40° | [인쇄 식] · [판독] |
| Fig 7 AOR vs HR | **FRF: θ = 36.2 HR − 13.4 · FCC: θ = 29.8 HR − 5.4 (R² 0.97)** — "거의 완전한 직선 → 둘 다 좋은 유동성 지표" | [인쇄] p.3 |
| Fig 8 AOR vs HR (다른 재료) | 소다회 · 중탄산나트륨 · 젖당 · FCC — 같은 경향 · 점이 많아 직선성은 Fig 7 보다 약간 덜 뚜렷 | [인쇄] p.3 |
| Fig 9 가중 AOR | **AOR/ρ_ba (반원뿔 벌크 밀도로 나눔) vs Sauter 지름** 으로 모든 재료를 한 그래프에 — y 단위 degree · g⁻¹ · cm³ | [인쇄] p.3 |
| 앞선 연구 | 소다회 · 중탄산나트륨 · 젖당에서 같은 경향 | [인쇄] p.3 |

### 3-6. 시료 양 (§4 · Fig 10 · 11 · Table 1 · p.4)
| 시료 (g) | Avicel 평균 AOR (°) | Avicel SD (°) | Starch 평균 AOR (°) | Starch SD (°) |
|---|---|---|---|---|
| 50 | 38.4 | 0.33 | 36.91 | 1.98 |
| 100 | 38.3 | 0.32 | 36.91 | 0.47 |
| 150 | 37.0 | 1.02 | NA | NA |
| 200 | NA | NA | 34.75 | 0.74 |

[인쇄] Table 1 (각 5 회).  200 · 150 g → 100 g 에서 AOR **상승** (starch +2.16° · avicel +1.3°) · 50 g 까지는 변화 없음 · **100 g 이 표준편차 최소** → 권장 · 100 g 이 안 되면 **같은 양을 항상** (p.4).

### 3-7. 우리 산술 [인쇄 식으로]
- AOR 40° 가 되는 d_sv: **FCC ≈ 15.8 µm · FRF ≈ 21.0 µm**.  HR 1.4 가 되는 d_sv: FCC ≈ 25.8 · FRF ≈ 28.7 µm · HR 1.25: FCC ≈ 44 · FRF ≈ 52 µm.
- Fig 7 두 직선은 **HR 1.25 에서 똑같이 31.85°** 로 만난다 · HR 1.4 에서 36.3 (FCC) · 37.3° (FRF) · AOR 40° ↔ HR 1.52 (FCC) · 1.48 (FRF) — 저자 서술 "HR > 1.4 분말의 AOR ≈ 40°" 와 정합.
- **외삽 (쓰지 말 것)**: d_sv 1 µm 에 식을 그대로 넣으면 AOR 80–88° · HR 2.7–2.8 — 맞춤 범위 (7–79 µm) 밖이고 측정 가능한 AOR 상한 근처.  ⇒ µm 황화물 SE 의 유동성은 **이 식이 아니라 직접 측정** 으로.

---

## 4. ★ 방법 — 시험 · 지표 · 입자 처리

### 4-1. 시험 절차 — §3-2 표.
### 4-2. 지표
- **동적 AOR** (반원뿔) · **HR** (탭 ÷ 통기 밀도) · **가중 AOR** = AOR/ρ_ba (반원뿔 벌크 밀도).
- **Sauter 평균 지름 d_sv = D(3,2)** (표면적 · 부피 평균) 을 입경 축으로.
### 4-3. ★ 입자 처리 (우리 축 언어로)
- 실험 전용 — 입자 모델 없음.  분말의 **점착 수준을 거시 각도 · 밀도비로 요약** 하는 측정 쪽 앵커.
### 4-4. 기법 미니 용어집
- **정적 · 동적 AOR** — 정지 더미 사면각 · 흐르는 (또는 막 흐른) 분말이 만든 사면각.
- **Hausner 비** — 탭 밀도 ÷ 통기 (가장 느슨한) 밀도 · 클수록 점착.
- **Geldart 분류** — 기체 유동화 거동으로 분말을 A (통기성) · B (기포) · C (점착) · D (분출) 군으로.
- **Carr 지수 · 기준** — 안식각 · 압축도 등으로 유동성을 점수화한 분류 (이 논문은 AOR 구간만 인용).
- **Sauter 지름 d_sv** — 부피 ÷ 표면적 비로 정한 평균 지름 (비표면적과 직결).

---

## 5. Figure set ★ (크롭 12 장 = `litdb/figures/geldart2006_powder_flowability_angle_of_repose_tester/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 흔한 AOR 네 방법 (고정 높이 · 고정 바닥 · 기울이는 판 · 회전 원통) | ★ "AOR 은 방법에 묶인 양" 의 그림 |
| 2 | Mark 4 시험기 사진 + 모식 (진동 경사판 45° · 깔때기 · 아래 경사판 · 받침판 · 뒤판) | ★ D3 시험기 후보 — 치수 미기재 |
| 3 | FCC 입자 (구형) | — |
| 4 | FRF 입자 (각진) | — |
| 5 | HR vs Sauter 지름 (인쇄 맞춤식 · HR 1.25 · 1.4 선) | ★ 미분 함량 ↔ HR |
| 6 | AOR vs Sauter 지름 (인쇄 맞춤식 · 40° 선) | ★ 미분 함량 ↔ AOR |
| 7 | AOR vs HR (두 직선 · R² 0.97) | ★★ 두 앵커의 상호 변환 (재료별) |
| 8 | AOR vs HR — 소다회 · 중탄산나트륨 · 젖당 · FCC | 재료 의존 |
| 9 | 가중 AOR (AOR/ρ_ba) vs Sauter 지름 — 재료 모음 | 재료 간 비교 변수 |
| 10 | starch AOR vs 시료 양 | 시료 양 의존 |
| 11 | avicel AOR vs 시료 양 | 시료 양 의존 |
| Table 1 | 시료 양별 평균 · SD (5 회) | ★ 재현성 · 소량 시험 근거 |

## 6. Post-processing ★
- **무엇을**: 반원뿔 높이 · 반지름 → AOR · 탭 · 통기 밀도 → HR · Sauter 지름 · 거듭제곱 · 직선 맞춤 (R²) · 5 회 평균 · SD.
- **안 한 것**: 시험기 치수 · 진동 조건 · 측정 오차 전파 · 다른 방법 (전단 셀) 과의 교차 · 습도 조건.
- **우리 후처리 (이 카드)**: §3-7 (AOR 40° · HR 1.25 · 1.4 의 d_sv · 두 직선 교점 · 외삽 경고) · 맞춤식의 곡선 귀속 판독 (digitized.csv).

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태)

| 항목 | 이 논문 (Geldart 2006) | 우리 (믹서 DEM · 논지 D3) | 차이 / 판정 |
|---|---|---|---|
| 역할 | **측정 앵커** (유동성) | DEM CED · Bo 는 **실험 앵커 없음** (내부 기준점) | ★ D3 의 측정 쪽을 이 시험 (또는 HR) 이 채울 수 있다 |
| 시료 | 7–79 µm 무기 분말 · 100–200 g | (계획) LPSCl · NCM — 1 µm SE · 4 · 9 µm NCM · 소량 · 글러브박스 [추정] | 입경 범위 밖 · 공기 민감 — HR (탭 · 통기 밀도) 이 글러브박스에서 더 쉬울 수 있다 [추정] |
| DEM 재현 | 없음 (치수 미기재) | 보정 런 = 같은 기하 필요 | ★ 장치 치수를 우리가 재야 · 아니면 Roessler 원통 (치수 공개) 이나 단순 더미 · 회전 드럼 동적 AOR (Jarray 2019) 로 |
| AOR 비교 | 방법마다 다른 값 | 같은 날 카드 셋의 AOR (드럼 · 더미 · 원통) | ★ 한 방법을 골라 그 방법만 DEM 으로 재현 |

### 7-1. frame[5]
측정 방법 논문 — 모델 반쪽 없음.  우리 파이프라인에서는 **D3 입력 앵커** 자리.

---

## 8. ★★ 우리 연구에 주는 insight (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

1. **두 앵커를 같이 재라 — AOR + HR.**  두 양이 같은 재료 계열에서 직선 (R² 0.97) 이지만 **기울기가 재료마다 다르다** (36.2 vs 29.8).  → SE · NCM 각각에서 둘 다 재면 (i) 서로 검증 (ii) DEM 보정에서 **하나는 맞추고 하나는 검증** 으로 쓸 수 있다 (frame[4] — 보정과 검증을 분리).  HR 은 탭 밀도계만 있으면 되어 **글러브박스 안** 에서 더 쉬울 수 있다 [추정].
2. **AOR 은 방법에 묶인 양.**  같은 날 카드의 AOR 셋 (Jarray 회전 드럼 동적 35–49° · Alizadeh 깔때기 더미 31–57° · Roessler 원통 인양 40–84°) 을 같은 축에 놓지 말 것.  → D3 등록 때 **측정 방법 하나를 정하고 그 기하 그대로 DEM 런** 을 만든다.  치수가 공개된 방법 (Roessler 원통 · 회전 드럼) 이 DEM 재현에 유리하고, Mark 4 는 치수를 직접 재야 한다.
3. **소량 시험의 근거.**  50–100 g 에서 AOR 이 안정 (avicel 38.4 · 38.3°) · 100 g 이 SD 최소.  → SE 분말 양이 제약이면 **양을 고정** (예: 50 g) 하고 반복 5 회 · SD 보고 — 이 논문 규약 그대로.
4. **미분 함량이 유동성을 지배한다 — 우리 혼합물의 시작 상태.**  7 µm 미분 몇 %만으로 AOR · HR 이 크게 오른다 (Fig 5 · 6).  우리 침대에서 SE (1 µm) 는 수 기준 다수 · NCM 은 4–9 µm — **혼합물 유동성은 SE 가 정할 가능성** 이 크다 [추정].  → D3 앵커를 **SE 단독 · NCM 단독 · 혼합물** 셋으로 재면 "혼합물 유동성 = 미분 (SE) 지배" 인지 확인할 수 있다.
5. **Carr · Geldart 기준은 보고 언어.**  측정 결과를 "45–55° = 점착 · HR > 1.4 = C 군" 으로 분류해 보고하면, 우리 DEM Bo 수준 (LC 0.212 · LA 3.0 · LH 38.4) 이 실제 분말의 어느 칸에 해당하는지 **보정 뒤** 말할 수 있다 — 보정 전에는 말하지 않는다 (논지 §3 · 같은 날 카드 `roessler2019_…` §8-4).

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Published angles of repose are seldom comparable because at least eight measuring methods exist (Brown & Richards 1970, as cited by Geldart et al., China Particuology 2006)." [인쇄 p.1]
- "With a vibrating-chute dynamic angle-of-repose tester using a 100 g sample, the angle of repose correlated linearly with the Hausner ratio (θ = 36.2 HR − 13.4 and θ = 29.8 HR − 5.4, R² = 0.97) for two powder series." [인쇄 Fig 7]
- "Angle-of-repose classes (Carr; Raymus): below 30° good flowability, 30–45° some cohesiveness, 45–55° true cohesiveness, above 55° very high cohesiveness." [인쇄 p.1]
- ⚠ 맞춤식 (Fig 5 · 6) 을 7–79 µm 밖으로 외삽하지 말 것.

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **시험기 치수 · 진동 조건 미기재** — 재현 · DEM 모사 불가 (실물 측정 필요).
2. **재료 범위** — 7–79 µm 무기 분말 · 음식 · 약품 첨가제 — 황화물 · µm 분말 아님.
3. **맞춤식은 재료별 경험식** — 기울기 · 지수가 재료마다 다르다 · R² 만 보고 (잔차 · 오차 없음).
4. **곡선 귀속** — 그림의 맞춤식이 어느 재료 것인지는 화살표 · 선 모양으로만 표시 (판독).
5. **시료 양 효과의 일관성** — "200 · 150 → 100 g 에서 AOR 상승 · 50 g 은 무변화" 는 재료 둘 · 수준 셋씩 (표의 NA 칸).
6. **"AOR 선호" 는 저자 의견** — 재기 쉽고 분말 움직임이 공정과 비슷하다는 이유 (정량 비교 없음).
7. **주저자 = 장비 회사 (Powder Research Ltd.) 관련** — 이해상충 서술 없음 [추정 · 소속 표기에서].
8. **소속 표기 'Herriot-Watt'** (원문 오기) · 'LeedsLS29JT' · '50603Kuala Lumpur' 띄어쓰기 누락.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|
| Abdullah, E. C. & Geldart, D. (1999). The use of bulk density measurements as flowability indicators. Powder Technol., 102, 151−165. | 벌크 밀도 지표 (HR) — 카드 없음 |
| Brown, R. L. & Richards, J. C. (1970). Principles of powder mechanics. Oxford: Pergamon Press. | AOR 측정법 다양성 · 40° 기준의 자료 — 카드 없음 |
| Carr, R. L. (1965). Classifying flow properties of solids. Chem. Eng., 1, 69−72. | Carr 기준 원전 — 카드 없음 |
| Geldart, D. (1973). Types of gas fluidization. Powder Technol., 7, 285−292. | Geldart 분류 — 카드 없음 |
| Geldart, D., Mallet, M. F. & Rolfe, N. (1990). Assessing the flowability of powders using angle of repose. Powder Handling & Proc., 2(4), 341−346. | 시험기 선행판 · 40° 기준 — 카드 없음 |
| Grey, R. O. & Beddow, J. K. (1969). On the Hausner Ratio and its relationship to some properties of metal powders. Powder Technol., 2, 323−326. | HR 정의 — 카드 없음 |
| Jenike, A. W. (1964). Storage and flow of solids (Bulletin no.123). Utah Engineering Experiment Station. | 전단 시험 (ffc) — 카드 없음 (같은 날 카드 `alizadeh2018_…` 가 ffc 사용) |
| McGlinchey, D. (ed.), (2005). Characterisation of Bulk Solids. Oxford: Blackwell Publishing. | 유동성 측정법 총설 — 카드 없음 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 본문 4 쪽 텍스트 층 전수 (pdftotext raw · layout) · 그림 안 맞춤식 = 렌더 판독 · 곡선 귀속 = 화살표 · 선 모양.
- 그림 11 · 표 1 = 크롭 12 장 (래스터 4 = 원본 139–204 dpi 를 300 dpi 로 · 벡터 그래프 7 = 그리기 요소 합집합 + 축 제목) · 첫 판 축 제목 잘림 5 장 + 본문 줄 끼임 1 장 = 재크롭 (`figures.json` 의 `recrop`).
- DOI 는 PDF 메타데이터 제목 (`doi:10.1016/S1672-2515(07)60247-4`) 에서 — 본문 쪽에는 인쇄되지 않았다.
- 정본 litdb 중복 확인: 'Geldart' · 'S1672-2515' · 제목 낱말로 `litdb/` 전수 grep — 없음.

## 🔗 관련 카드
- D3 짝: [`roessler2019_dem_cohesive_aor_cylinder_lift_calibration`](roessler2019_dem_cohesive_aor_cylinder_lift_calibration.md) (DEM 보정 쪽 · 점착 분말 AOR 의 한계) · [`alizadeh2018_dem_adhesion_calibration_segregation_heap`](alizadeh2018_dem_adhesion_calibration_segregation_heap.md) (단일 성분 AOR 보정 · Jenike ffc) · [`coetzee2017_dem_calibration_review`](coetzee2017_dem_calibration_review.md).
- 점착 분말 이론: [`molerus1975_theory_of_yield_cohesive_powders`](molerus1975_theory_of_yield_cohesive_powders.md).
- 드럼 동적 AOR: [`jarray2019_cohesion_driven_mixing_segregation_drum`](jarray2019_cohesion_driven_mixing_segregation_drum.md).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->
