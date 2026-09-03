---
title: "Tao et al. 2025 — Non-destructive degradation pattern decoupling (Energy Environ. Sci. 18, 1544)"
source_url: local-upload/10._Nondestructive_degradation_pattern_decoupling_for_early_battery_trajectory_prediction_via_physicsinformed_learning.pdf
ingested: 2026-09-03
sha256: 323834e0c0b6cd2665717ee8b7c9a4ca005a365458709fa84354bd2ba0773069
---

# 수집 목적

Shengyu Tao, Mengtian Zhang, Zixi Zhao 외, **"Non-destructive degradation
pattern decoupling for early battery trajectory prediction via
physics-informed learning"**, *Energy & Environmental Science* **18**,
1544–1559 (2025), DOI 10.1039/d4ee03839h 의 **절별 해체분석**.

흡수 동기는 제목의 세 단어다 — **decoupling** · **degradation pattern** ·
**physics-informed**. 이 저장소의 주 연구
(`degradation-degeneracy/`)는 full-cell 관측 하나로 LLI / LAM_PE / LAM_NE 를
가를 수 있는지를 판정한다. 제목만 보면 이 논문은 그 질문에 답한 것처럼 읽히므로,
**이 논문이 "decouple" 한다고 말하는 대상이 우리가 말하는 열화 모드와 같은
것인지**를 확정하는 것이 이번 흡수의 첫 과제였다. 결론부터: **다른 것이다**
(§7). 논문의 "thermodynamic loss" 라는 **한 칸 안에** LLI·LAM_PE·LAM_NE 가 전부
들어 있고, 논문 자신의 Fig. 5b 가 그 셋을 가르는 것을 `[인쇄]` **"Hard to
decouple"** 이라고 적는다.

둘째 동기는 저자들이 **데이터와 코드를 모두 공개**했다는 점이다. 이 계보에서
흡수한 아홉 편 중 원본 데이터·코드가 함께 열려 있는 경우는 드물다
(Zhang 2020 이 유일한 선례). 사용자가 두 저장소를 미리 clone 해 두었으므로,
**논문이 말하는 데이터셋 규모·프로토콜·feature 정의가 실제 파일과 맞는지**를
대조하는 감사(§10)를 이번 digest 의 독립 산출물로 삼았다.

**표기 규칙** (이 위키 관례 3구분 + 저장소 대조용 2종):

- `[인쇄]` — 논문 본문/SI/표/캡션/식에 글자로 있는 것
- `[도표]` — 그림에서 눈으로 읽은 근사값 (원 데이터가 아니다)
- `[코드]` — 저자 공개 저장소의 **파일·코드에서 직접 확인**한 것
- `[데이터]` — 저자 공개 **데이터로 우리가 직접 계산**한 것 (논문의 주장이 아니다)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **논문의 주장이 아니다**

- 원본 파일: 로컬 업로드 PDF 2종 (본문 17쪽 = 표지 1 + 논문 16, SI 75쪽).
  저장소에 바이너리를 넣지 않는다.
- 크로핑 그림: `raw/figures/tao2025_nondestructive-degradation-decoupling/`
  (fig 20장 + tab 2장, `figures.json` 에 캡션 색인). 무엇을 실제로 봤는지는 §14.
- 대조한 저자 저장소 2종 (읽기 전용, 이 저장소에 복사하지 않았다):
  - 데이터: `github.com/terencetaothucb/TBSI-Sunwoda-Battery-Dataset`
  - 코드: `github.com/terencetaothucb/Early-Battery-Degradation-Prediction-via-Chemical-Process-Inference`

---

## 0. 서지사항 (직접 확인)

`[인쇄]` PDF 표지·1쪽 헤더·각주 및 파일 메타데이터에서 확인한 것:

| 항목 | 값 |
|---|---|
| 문서 종류 | **PAPER** (표지 인쇄, 리뷰가 아니다) |
| 제목 | Non-destructive degradation pattern decoupling for early battery trajectory prediction via physics-informed learning |
| 제1저자 | Shengyu Tao (Tsinghua Shenzhen International Graduate School) |
| 공동 제1 | Shengyu Tao, Mengtian Zhang, Zixi Zhao — `[인쇄]` "These authors were of equal contributions." |
| 교신 | Xuan Zhang · Yang Li · Xiaosong Hu · Guangmin Zhou (\* 4인) |
| 저자 수 | 22명 |
| 소속 | Tsinghua SIGS (a) · Tsinghua 베이징 (b) · Aalborg Univ. (c) · Univ. of Groningen (d) · **Sunwoda Mobility Energy Technology Co., Ltd.** (e) · UC Berkeley eCAL (f, Scott Moura) · Chongqing Univ. (g) |
| 학술지 | *Energy & Environmental Science* **2025**, **18**, 1544–1559 (Volume 18, Number 3, 7 Feb 2025) |
| DOI | **10.1039/d4ee03839h** |
| 접수/수락/출판 | Received 25 Aug 2024 · Accepted 23 Dec 2024 · Published 14 Jan 2025 |
| 표지 | `[인쇄]` "As featured in:" — 이 호의 **표지 논문**이다 |
| 이해충돌 | "There are no conflicts of interest to declare." |
| 데이터 공개 | GitHub 2곳 (위) + Zenodo `zenodo.org/uploads/10715209` (raw/processed) |
| SI | Supplementary Figures 1–40 · Tables 1–6 · Notes 1–10 · Discussion 1 (75쪽) |

`[해석]` **셀 제조사가 공저자다** (Sunwoda, e 소속: Yaojun Liu, Wenjun Yu,
Zhongling Xu — Author contributions `[인쇄]` "Y. L., W. Y., and Z. X. provided
the raw data"). 데이터 출처와 논문의 주장(제조 품질 검증) 사이에 이해 관계가
있다는 뜻은 아니지만, "IMV 가 수명을 결정론적으로 좌우한다" 는 주장의 데이터가
**한 제조사의 한 배치**에서 나왔다는 범위 한정을 항상 붙여야 한다.

---

## 1. 원문에 없어서 확인이 필요한 것 (공백 목록) ★

digest 를 쓰기 전에 먼저 밝힌다. 아래는 **논문이 인쇄하지 않은 것**이며, 이
논문을 근거로 이 자리를 메꾸는 문장을 쓰면 그것은 이 논문의 근거가 아니다.
근거는 §12 의 어휘 전수와 각 절의 대조다.

1. **`identifiability`(식별 가능성) 이라는 단어가 본문·SI 에 0회.**
2. **`degeneracy` / `ill-posed` / `non-unique` / `uniqueness` 가 각 0회.**
   역문제의 유일성을 묻는 문장이 하나도 없다.
3. **`cross-validation` 이 0회.** 셀 단위 분할·group 정의·fold 설계에 대한
   서술이 본문에도 SI 에도 없다. 실제 분할은 코드에서만 확인된다 (§10.2).
4. **오차 막대·신뢰구간이 예측에 없다.** `error bar`·`confidence interval` 0회.
   Fig. 4a/b 의 회색 "Deviation" 은 셀 간 산포이지 추정 불확실성이 아니다.
5. **LLI·LAM 을 정량한 적이 없다.** 두 약어는 적잖이 나오지만 (§12 표: LLI
   본문 12 / SI 9, LAM 본문 7 / SI 4)
   **전부 정성 서술**이고, 이 논문이 산출하는 수치 중 LLI 나 LAM 의 크기를
   나타내는 것은 **하나도 없다**. half-cell OCP fitting·해체분석 정량·
   ICA/DVA 기반 모드 분해가 전부 없다 (Fig. 5g 의 ICA 는 화살표 주석뿐).
6. **ΔE 와 η 를 수치로 계산한 적이 없다.** 식 (1)이 논문의 물리적 뼈대인데,
   `U_theoretical(*)`(이론 OCV)를 **어떻게 얻는지 아무 데도 적혀 있지 않고**
   실제로 얻지도 않는다. 52개 feature 중 ΔE 나 η 인 것은 없다 (§4).
7. **"열역학" 구간의 전류가 0 이 아니다.** 식 (1)의 ΔE 는 `[인쇄]` "when zero
   current is applied" 로 정의되는데, 열역학 대표로 쓰이는 Q1·Q9 는 **0.33C**
   구간에서 측정된다 (Table S1). I→0 극한과 0.33C 사이의 간극을 논문이 다루지
   않는다.
8. **RPT 주기가 인쇄되지 않았다.** Fig. S3 이 "RPT 시점 그림" 이라고만 하고
   숫자가 없다. (공개 데이터에서 우리가 역산한 값은 §3.2 — 약 100 사이클.)
9. **셀 제조 배치·전해질 조성·전극 로딩 등 셀 사양이 없다.** NCM811 / 흑연 +
   13 wt% SiO / 1.1 A h 가 전부다.
10. **abstract 의 headline 수치(95.1 % 정확도 = MAPE 4.9 %)를 SI 표에서
    재현할 수 없다.** 본문이 그 수치의 근거로 지목한 Table S4 의 같은 설정
    수치를 평균하면 **1.91 %** 다 (§11.1).
11. **모델 선택 절차가 인쇄되지 않았다.** 코드에서는 **시험 손실로 best
    epoch 를 고른다** (§10.2) — 논문에는 이 문장이 없다.
12. **feature 간 공선성 논의가 0회.** 52개 feature 중 다수가 같은 곡선의
    이웃 구간에서 나온 값인데 상관 구조를 보고하지 않는다.

---

## 2. 논문의 질문과 답 (Abstract · Broader context · Introduction, p.1544–1545)

### 2.1 문제 설정

`[인쇄]` 초록 첫 문장: "Manufacturing complexities and uncertainties have
impeded the transition from material prototypes to commercial batteries, making
their verification a critical quality assessment link. **A fundamental challenge
is to decouple electrochemical interactions for establishing a quantitative
mapping from electrochemical parameters to macro battery performance.**"

문제는 **배터리 시제품 검증(prototype verification)의 시간**이다. `[인쇄]`
"current verification timelines, stretching from months to years". 표준 방법인
capacity calibration 은 EOL 까지 실제로 돌려 봐야 한다.

`[인쇄]` 열화 패턴의 정의가 Introduction 에 한 번 나온다: "The degradation
patterns, including kinetics and thermodynamics, manifest as **impedance
increase, loss of lithium-ion inventory (LLI), and loss of active material
(LAM)**, and are traditionally analyzed by destructive post-mortem methods".

`[해석]` **이 한 문장이 이 논문의 좌표계를 결정한다.** 세 가지(임피던스·LLI·
LAM)를 나열한 뒤, 이후 논문 전체는 그것을 **둘**(kinetics · thermodynamics)로
묶어서 다룬다. 그 묶기가 §7 의 핵심이다.

### 2.2 논문의 답 (초록)

`[인쇄]`:

> "Here, we show that the proposed physics-informed learning model can quantify
> and visualize temporally resolved thermodynamic and kinetic parameters from
> field accessible electric signals, facilitating a non-destructive degradation
> pattern decoupling. **The lifetime trajectory prediction is 25 times faster
> than the traditional capacity calibration test while retaining a 95.1% average
> accuracy across temperatures**, underpinned by projected electrochemical data
> from early cycle observations which have not yet been established."

핵심 주장 4개:

| # | 주장 | 근거 위치 |
|---|---|---|
| A | 초기 50 사이클(수명의 4 %)만으로 **전 수명 궤적**(EOL 점이 아니라)을 예측 | Fig. 4a–f, Table S4 |
| B | 온도 간 전이를 **Arrhenius 기반 전이가능성 지표(AT score)** 로 처리 | Methods 식 (5)–(11), Fig. 2h·2i |
| C | 열화를 **열역학 / 동역학**으로 분해하고 그 비율을 SAGE 로 정량 (79 % / 21 %) | Fig. 4g·4h, Fig. 5e·5h·5i |
| D | 그 분해가 불량 시제품의 **재활용 경로 선택**을 바꾼다 (2060년 197.6억 USD 시장) | Fig. 6 |

`[해석]` "25 times faster" 는 측정된 시간 절감이 아니라 **데이터 비율의 역수**다
(50 사이클 / 약 1250 사이클 = 4 % → 1/0.04 = 25). 논문이 그렇게 적지는 않지만
두 수치가 정확히 맞물린다.

### 2.3 이 논문이 자기 위치를 잡는 방식

`[인쇄]` Broader context: "Although machine learning has been well-documented in
battery R&D, **it fails to decouple electrochemical degradation patterns that
support interpretable decisions.** Here, distinct from purely statistical
modeling, we compute thermodynamic and kinetic degradation parameters …"

`[해석]` 즉 이 논문의 자기 정의는 **"순수 통계 모델과 다르다"** 이고, 그 차별점을
"decoupling" 에 둔다. 그러므로 decoupling 이 무엇인지가 논문의 무게중심이며,
§7 에서 그것을 정면으로 본다.

---

## 3. 데이터 생성 (Results §Data generation, p.1545–1547)

### 3.1 논문이 인쇄한 사양

`[인쇄]`:

| 항목 | 값 |
|---|---|
| 셀 | 삼원계 NCM811 (LiNi₀.₈Co₀.₁Mn₀.₁O₂) 양극 |
| 음극 | 흑연 + **13 wt% silicon oxide** |
| 공칭용량 | 1.1 A h (1C = 1.1 A) |
| 온도 | 25 · 35 · 45 · 55 °C (4 시나리오) |
| 충전 | **9단 다단 충전** 0.33C → 3C, 20분에 SOC 75 % |
| 방전 | 1C 정전류 |
| 종료 | EOL 문턱을 넘겨서 계속 — `[인쇄]` "from 73% to 59% of nominal capacities" |
| 수명 범위 | `[인쇄]` **480 ~ 1025 사이클** (EOL80 정의) |
| 수명 평균 | `[인쇄]` **775 ± 175** 사이클 (EOL80) |
| EOL73 수명 | `[인쇄]` 25/35/45/55 °C 에서 **1218 · 1180 · 958 · 661** 사이클 |
| 셀 개수 | 본문에 없다. **SI Fig. 1·2 캡션**에 `[인쇄]` "9, 9, 7, and 7 battery samples" → **총 32** |

`[도표]` Fig. 2g 의 violin 에 `n=9, n=9, n=7, n=7` 이 인쇄돼 있고 산포 막대는
0.06 / 0.05 / 0.03 / 0.01 (×10³ 사이클) 이다.

### 3.2 다단 충전 프로토콜 (Table S1, 전문)

`[인쇄]` Table S1 (Step 4–12 만 featurization 에 쓴다):

| Step | 전류 | 시간(min) | ΔSOC | 누적 SOC | cut-off |
|---|---|---|---|---|---|
| 1 | Rest | 30.0 | – | | |
| 2 | 0.33C → 2.5 V (방전) | – | | 0 % | |
| 3 | Rest | 30.0 | – | | |
| **4** | **0.33C** | 14.54 | +8.0 | 8.0 % | **U1** |
| **5** | **3.00C** | 2.40 | +12.0 | 20 % | **U2** |
| **6** | **2.90C** | 2.07 | +10.0 | 30 % | **U3** |
| **7** | **2.80C** | 2.14 | +10.0 | 40 % | **U4** |
| **8** | **2.40C** | 2.50 | +10.0 | 50 % | **U5** |
| **9** | **2.00C** | 3.00 | +11.1 | 61.1 % | **U6** |
| **10** | **1.80C** | 3.33 | +10.0 | 71.1 % | **U7** |
| **11** | **1.40C** | 4.29 | +10.0 | 81.1 % | **U8** |
| **12** | **0.33C** | 28.93 | +15.9 | **97 %** | **U9** |
| 13 | Rest | 120.0 | | | |
| 14 | 1C 방전 | 56.40 | −94 % | | (U10) |
| 15 | Rest | 60.0 | | | |

`[인쇄]` "Steps 3 to 14 are repeated 3 times. The mean values of the (U1-U9) are
taken as **cut-off voltages for subsequent cycling**."

`[해석]` **이것이 이 논문에서 가장 중요한 설계 결정이다.** cut-off 전압
U1–U9 는 셀마다 처음 3 사이클에서 한 번 정해지고 **그 후 수명 내내 고정**된다
(§10.1 에서 데이터로 확인: 셀당 표준편차 ~1e-16). 그래서:

- U1–U9 는 "초기 제조 편차(IMV)" 의 정의이자 **셀 고유의 지문**이다.
- 이후 사이클에서 각 단의 SOC 는 더 이상 고정 8/20/30… % 가 아니다 —
  전압이 고정되고 SOC 가 흐른다. 그런데 SI Note 3 의 feature 정의
  (`Q_i = Q(soc = soc_i)`, `soc_i = {8,20,…,97} %`)는 **SOC 가 고정된 것처럼**
  쓰여 있다. 두 서술이 서로 맞지 않는다 (§11.4).

`[데이터]` 공개 `Labels.xlsx` 의 용량 계열에서 **약 100 사이클마다 용량이
계단식으로 회복**한다 (예 B1T25: 사이클 101·301·401·501·601·801·1201 에서
+4 mAh 이상 점프). RPT 주기가 100 사이클 부근임을 시사한다 — 논문에 인쇄되지
않은 값이다.

### 3.3 IMV 와 수명의 관계 (Fig. 2)

`[도표]` Fig. 2f: IMV(같은 온도 셀 간 cut-off 전압 표준편차)는 **2 ~ 12 mV**
범위이고 온도에 대해 **그릇 모양(bowl-shaped)** 이다 — 25 °C 에서 크고 45 °C
에서 최소, 55 °C 에서 다시 커진다. U1 만 예외이며 `[인쇄]` "The minor deviations
of U1 at 25 1C are **noise-sensitive with an mV level signal**".

`[인쇄]` "These trends are consistent across temperatures, affirming that
**initial IMV probing deterministically affects macro capacity.**"

`[해석]` **"deterministically" 는 이 논문이 보여 준 것보다 강한 단어다.**
근거는 (a) IMV 의 온도 의존 곡선과 수명의 온도 의존 곡선이 둘 다 그릇 모양이라는
형태 일치와 (b) SI Fig. 4–6 의 상관이며, 55 °C 에서는 `[인쇄]` 저자 스스로
"unstable correlations" 라고 적는다. 온도가 IMV 와 수명을 **동시에** 움직이는
공통 원인이므로, 온도를 가로지른 형태 일치는 셀 수준 인과의 근거가 되지 못한다.
같은 온도 안의 셀 간 상관은 SI Fig. 5 에 있으나 상관계수가 본문에 인쇄되지 않았다.

`[도표]` Fig. 2h: Arrhenius plot (−ln(aging rate) vs 1/k_BT, 35–39 eV⁻¹) 이
네 점에서 직선이며 오차 막대(±1σ)가 붙어 있다. `[인쇄]` "a consistent line
across 25 to 55 1C indicates **no significant degradation mechanism alteration
under fast charging**".

`[해석]` 이것이 논문의 **유일한** 기구 불변성 검사다. Arrhenius 직선성은
"지배적 활성화에너지가 하나" 라는 필요조건이지 "LLI/LAM 조성이 온도에 걸쳐
같다" 는 뜻이 아니다. 그런데 뒤에서 55 °C 를 source domain 으로 삼아 25 °C 를
예측하는 근거로 이 그림이 쓰인다.

---

## 4. Featurization taxonomy — 52개 feature (SI Note 1–3, Fig. 3)

### 4.1 물리적 뼈대: 식 (1)

`[인쇄]` Methods 식 (1)(2):

```
|U_actual − U_theoretical(*)| = ΔE(SOC, SOH, T) + η(I, SOC, SOH, T)
η = η_act + η_ohm + η_con
```

`[인쇄]` "ΔE is the thermodynamic voltage loss, attributed to the **intrinsic
material change due to aging**" · "η is the current-induced polarization".
SI Note 1: "applied current causes the battery working voltage to deviate from
its OCV and **cannot change the properties of materials, thus solely
influencing η**. In comparison, for the open-circuit state, voltage loss solely
reflects thermodynamic loss contributions."

`[도표]` Fig. 3b 는 이것을 그림으로 준다: 세로축 applied current I, 가로축
electrode voltage offset. I = 0 선에서의 오프셋이 ΔE, 전류가 올라가면서 벌어지는
추가 오프셋이 η. **모식도이며 수치가 없다.**

`[해석]` 식 (1) 은 **정의**이지 측정 절차가 아니다. `U_theoretical(*)` 를 얻는
방법이 논문 어디에도 없고 (§1.6), ΔE·η 가 수치로 산출되는 곳도 없다. 실제로
쓰이는 것은 아래 52개 통계 feature 이며, 식 (1)은 그 feature 들을 **두 상자에
나눠 담는 근거**로만 기능한다.

### 4.2 feature 표 (SI Note 2, 전문 재구성)

| ID | 분류 | 이름 | 정의 (SI Note 3) | 논문이 붙인 물리 의미 |
|---|---|---|---|---|
| 1 | – | T | 운전 온도 | – |
| 2–10 | Prior-cycle | **U1–U9** | 각 단의 지정 SOC 도달 시 전압 | 각 단(SOC 구간)의 charge acceptance |
| 11 | In-cycle (inter) | VC89 | V₉(start) − V₈(end) | ohmic + 전기화학 분극, SEI 성장 (pseudo relaxation) |
| 12 | inter | VD9 | V₉(start) − min(V₉) | 농도 분극 (pseudo relaxation) |
| 13 | inter | tVD9 | VD9 에 걸린 시간 | 농도 분극 회복 시간 |
| 14 | inter | ReVC | V₉(end) − V_re(start) | ohmic + 전기화학 분극 (relaxation) |
| 15 | inter | ReVD | V_re(start) − min(V_re) | 농도 분극 (relaxation) |
| 16 | inter | tReVD | ReVD 에 걸린 시간 | 농도 분극 회복 시간 |
| 17–25 | In-cycle (intra) | **Vg1–Vg9** | mean(∇V_i) | 각 단의 분극 속도 |
| 26 | inter | RVg | Vg2 / Vg1 | – |
| 27–35 | intra | **Q1–Q9** | 지정 SOC 도달 시 충전용량 | 각 단(SOC 구간)의 charge acceptance |
| 36–44 | intra | **RL1–RL9** | (V_i(end) − V_i(start)) / I_i | lumped 저항 (ohmic+전기화학+농도) |
| 45–52 | inter | **RO1–RO8** | (V_{i+1}(start) − V_i(end)) / (I_{i+1} − I_i) | relaxation 유래 ohmic 저항 |

`[인쇄]` "intra-step features are **lumped representations of thermodynamic and
kinetic loss**, while inter-step features are **purely linked to kinetic loss**
by current density switching."

`[인쇄]` "The feature taxonomy aims to **decouple total capacity loss into its
kinetic and thermodynamic components.**"

### 4.3 열역학 / 동역학 배정 규칙 (SI Note 8) ★

이 논문에서 "decoupling" 의 **작동 정의**가 여기 있다. `[인쇄]` SI Note 8:

> "For thermodynamic loss and kinetic loss, **small current stages define a
> dominated thermodynamic loss, while large current stages define a dominated
> kinetic loss.** For thermodynamic loss, we use the summation of the absolute
> value of feature importance for **Q1 and Q9** as the thermodynamic loss
> contribution to the overall capacity loss. For the kinetic loss, we use the
> summation of the absolute value of feature importance for **Q2, Q3, Q4, Q5,
> Q6, Q7, and Q8** as the kinetic loss contribution."

Table S1 과 맞춰 보면: Q1 = Step 4 (0.33C), Q9 = Step 12 (0.33C), Q2–Q8 =
Step 5–11 (1.4 ~ 3.0C).

`[해석]` **즉 "열역학 대 동역학" 의 분해는 물리량 추정이 아니라 충전 단 번호에
따른 배정이다.** 저전류 두 단 = 열역학, 고전류 일곱 단 = 동역학. 이 배정 자체는
물리적으로 합리적인 근사이지만, 그 결과로 얻는 "79 %" 는 **모드의 크기**가
아니라 **feature 그룹의 중요도 점유율**이다 (§7.3).

---

## 5. 세 단계 파이프라인과 "physics-informed" 가 들어오는 지점 (Methods, Fig. S23)

### 5.1 파이프라인

`[인쇄]` "Our approach involves a three-stage machine learning pipeline …
First, we model multi-dimensional chemical processes using early cycle and
guiding sample data; second, we adapt these predictions to specific
temperatures; and third, we use adapted chemical processes to avoid the need for
physical measures in later cycles."

| 단계 | 모델 | 입력 | 출력 | 학습 설정 (논문) |
|---|---|---|---|---|
| 1 | Chemical Process (식 3) | 브로드캐스트된 U 행렬 `U^{(C×m)×10}` | 42개 in-cycle feature `F̂` | 3층 FC (32-64-32), **Leaky ReLU**, Adam, **30 epoch**, lr **1e-4**, 온도별 **75/25 분할** |
| 2 | AT 전이 (식 5–12) | 각 도메인의 노화율 r | 목표 도메인 feature 궤적 | 학습 없음 (해석적 가중) |
| 3 | Degradation Trajectory (식 13) | 예측된 feature `F̂` | 용량 궤적 `D̂` | 3층 FC (32-64-32), Leaky ReLU, Adam, **100 epoch**, lr **1e-3** |

손실함수 `[인쇄]` 식 (4)(14): MSE + λ·Σ|잔차| (λ = 1e-5). — 잔차의 L1.

### 5.2 물리는 어디에 들어오는가 ★ (사용자 질문 2)

논문이 "physics-informed" 라고 부르는 것을 지점별로 분해하면 **네 자리 중 두
자리에만** 물리가 있고, 그중 하나는 코드에서 다른 형태로 구현돼 있다.

| 지점 | 물리가 들어오는가 | 내용 |
|---|---|---|
| **손실항** | **아니오** | 손실은 MSE + L1 뿐. PDE 잔차·보존식·단조성 제약 등 물리 항이 **하나도 없다**. PINN 이 아니다. |
| **입력 feature** | **예 (주된 자리)** | 52개 feature 의 **선정과 이름 붙이기**가 식 (1)에서 나온다. 값 자체는 순수 통계량(전압차·기울기·비)이며, 물리는 "어느 구간을 왜 보는가" 에만 개입한다. |
| **구조** | **예 (Arrhenius 전이)** | 식 (5)–(11): AT score = r_target/r_source = exp(−E_a^s/k_BT_s + E_a^t/k_BT_t) 로 source 도메인 가중치 W_i 를 정한다. 이것이 논문이 "physics-informed" 라고 부르는 핵심 부품이다. **단, 활성화에너지 E_a 를 모르기 때문에** `[인쇄]` "Since the dominating aging mechanism is unknown (characterized by E_a) as a posterior, we **alternatively determine the aging rate by calculating the first derivative** … on the predicted chemical process curve" (식 7–8). |
| **사후 해석** | **예** | SAGE 중요도를 열역학/동역학 상자에 배정해 79 % / 21 % 를 만든다 (§4.3). COMSOL FEA 는 ML 결과를 **재현하도록 파라미터를 맞춘** 사후 시각화다 (§8). |

`[해석]` ★ **가장 중요한 관찰**: 식 (6)의 Arrhenius 형태는 식 (7)–(8)에서
**즉시 폐기된다**. E_a 를 모르니 AT score 를 온도가 아니라 **초기 사이클에서
잰 feature 기울기의 비**로 계산한다. 남는 것은 "노화율 비로 source 를 가중한다"
는 경험적 규칙이고, 온도는 그 안에 들어오지 않는다. 즉 **실제로 계산되는 AT 에는
Arrhenius 가 없다.** 저자들도 식 (9)에서 "기구가 이미 알려진 경우" 에만 온도만으로
계산할 수 있다고 적으며, 그 경로는 이 논문에서 쓰이지 않는다.
`[코드]` 공개 코드는 이 관찰을 더 강하게 확인한다 (§10.3): 구현된 AT 는
**기울기의 로그들의 비**이고, 온도는 하드코딩된 전압 스케일 상수로만 들어온다.

---

## 6. 성능 결과 (Fig. 4, Table S4–S6)

### 6.1 본문 수치

`[인쇄]` 다중 source(25 · 55 °C 접근 가능 → 35 · 45 °C 검증), 목표 셀 수명의
20 % 조기 데이터:

| 대상 | MAPE (표준편차) |
|---|---|
| 35 °C | **1.4 % (0.014)** |
| 45 °C | **0.6 % (0.006)** |

`[도표]` Fig. 4a/4b parity plot: 축 0.75–1.05 A h. **EOL 근처에서 점들이 기준선
아래로 치우친다** (예측 > 실제 = 과대추정) — `[인쇄]` "overestimations occur as
batteries near EOL". 오차 히스토그램은 35 °C 에서 +20 ~ −50 mAh, 45 °C 에서
+15 ~ −15 mAh 이고 **둘 다 이봉(bimodal)** 이다. `[해석]` 이봉 구조는 셀 그룹이
둘로 갈린다는 신호인데 논문은 언급하지 않는다.

`[인쇄]` 수명 단계별 비교 (Fig. 4c): 초기 10 % 에서 우리 방법 **0.24 %**,
model 2 도 0.24 %, model 1 (LSTM) 0.38 %, model 3 (no-transfer) 3.48 %,
model 4 (경험식) 2.82 %. 후기 10 % 에서 우리 방법 **1.53 %** (Fig. 4c 에
인쇄된 중간 10 % 값은 `[도표]` **0.71 %**).

`[도표]` Fig. 4d: EOL 용량 0.9 / 0.85 / 0.8 A h 에 대한 사이클 오차, 우리 방법의
막대에 **19** 와 **33** 이 인쇄돼 있다 (`[인쇄]` "maximum deviation of 33 cycles").

`[도표]` Fig. 4e: 조기 데이터 접근 4.2 % (50 사이클) 에서 MAPE 가 T35 ≈ 1.8 %,
T45 ≈ 0.9 %. Fig. 4f: 55 °C guiding sample 을 1 → 3 → 5 개로 늘리면 MAPE 가
25 %대 → 12 %대 → **3.57 / 2.71 / 0.51 %** (25/35/45 °C) 로 떨어진다.

### 6.2 벤치마크의 정체 (SI Note 4)

| 모델 | 무엇인가 | `[해석]` 논평 |
|---|---|---|
| model 1 | 단층 LSTM, 42차원 feature 를 길이 10 창으로 넣어 다음 용량을 **반복 예측** | 자기회귀 반복이라 오차가 누적된다. Table S4 에서 MAPE **67 ~ 88 %** — 기준선이라기보다 발산한 모델이다. |
| model 2 | 우리 파이프라인에서 IMV(U1–U9)만 뺀 것 | 유일하게 공정한 ablation. Table S4 에서 우리 방법과 **0.5 ~ 1 %p 차이**밖에 안 난다. |
| model 3 | Arrhenius 전이를 뺀 것 | |
| model 4 | 다항식 경험식 + 절편 평행이동 보정 | |

`[해석]` **model 2 가 이 논문의 진짜 대조군이고, 그 격차는 작다.** Table S4 (50
사이클): 45 °C 0.99 vs 1.47, 35 °C 2.11 vs 2.54, 25 °C 2.64 vs 3.69. IMV 를 넣어
얻는 이득은 0.4 ~ 1.1 %p 다. 본문이 강조하는 "5.82 % / 5.62 %" 급 격차는 다른
설정(Fig. 4c 후기 10 %)에서 나온 값이며, 그 문장 자체가 모델 번호를 혼동한다
(§11.2).

### 6.3 단일 feature 실험 (Table S5·S6) ★

`[인쇄]` Table S6, Exp 1–4 (온도 전이 없음, 80/20 분할, `[인쇄]` "toy problems
for model interpretation only"):

| 입력 | 25 °C | 35 °C | 45 °C | 55 °C |
|---|---|---|---|---|
| Q1 하나 | 0.43 | 0.29 | 0.47 | 0.67 |
| Q2 하나 | 0.44 | 0.39 | 0.48 | 0.68 |
| Vg1 하나 | 0.50 | 0.37 | 0.39 | 0.73 |
| Vg2 하나 | 1.02 | 0.62 | 0.83 | 0.93 |

`[해석]` ★ **feature 하나만 넣어도 MAPE 0.3 ~ 0.5 % 다.** 52개 feature 전체를
쓰는 본 모델의 전 수명 MAPE (0.6 ~ 1.4 %) 와 같은 자릿수이거나 더 좋다. 이것은
"이 셀들의 용량 궤적이 거의 매끄러운 단조 함수라서, 같은 방향으로 흐르는
아무 feature 하나로도 회귀가 된다" 는 뜻이다. 논문은 이 표를 "예측력과
전이가능성이 서로 다른 축" 이라는 논지의 재료로만 쓰고, **feature 집합의 중복성**
에 대한 함의를 다루지 않는다. `[해석]` 이 관찰은 §7.3 의 "79 % 는 모드 크기가
아니다" 와 짝을 이룬다 — 서로 강하게 상관된 feature 집합에서 SAGE 중요도의
그룹 점유율은 물리적 기여도가 아니라 **상관 구조가 나눠 가진 몫**이다.

`[인쇄]` Table S5 (단일 source 55 °C, 200 사이클 조기 데이터): 열역학
(Q1+Q9) 로만 → 25/35/45 °C 에서 11.05 / 3.59 / 3.27 %; 동역학(Q2)로만 →
5.32 / 1.10 / 1.12 %. `[해석]` **동역학 feature 하나가 열역학 두 개를 모든
온도에서 이긴다.** 그런데 §7.3 의 79 % 는 열역학이 지배적이라고 말한다. 논문은
이 긴장을 `[인쇄]` "the challenges of prototype verification are **dualistic**"
(설명력 vs 온도 적응력) 으로 봉합한다.

---

## 7. "Decoupling" 이 정확히 무엇인가 ★★ (사용자 질문 1)

### 7.1 논문 자신의 도식 — Fig. 5b

`[도표]` Fig. 5b 는 두 열이다.

```
Degradation mode          Loss type
┌──────────┐
│   LAM    │─────┐
└──────────┘     ├────▶ ┌────────────────────┐
┌──────────┐     │      │ Thermodynamics  ΔE │
│   LLI    │─────┘      └────────────────────┘
└──────────┘   [신경망 글리프]  ← 그 옆에 굵은 글씨로
┌──────────┐        "Hard to decouple"
│ Impedance│────────────▶ ┌────────────────┐
└──────────┘              │  Kinetics    η │
                          └────────────────┘
```

`[인쇄]` (SI Fig. 25 캡션, 같은 내용을 글로): "Loss types can be classified into
thermodynamic and kinetic loss types. **Thermodynamic loss can be related to
loss of active material (LAM), such as LAM at the cathode, LAM at the anode, and
loss of lithium inventory (LLI).** Kinetic loss can be related to impedance
increment."

`[도표]` Fig. 5e 의 범례가 이것을 한 줄로 확정한다:
**"Thermodynamic loss (LAM&LLI)"** · **"Concentration polarization
(Impedance)"**.

### 7.2 우리 축과의 대조 ★

| | 이 논문 | `degradation-degeneracy` |
|---|---|---|
| 분해 대상 | 전압 손실 `|U_actual − U_theoretical|` | 전극 이용상태 (stoichiometric window) |
| 미지수 | **2개** — ΔE(열역학), η(동역학) | **3개** — LLI, LAM_PE, LAM_NE |
| LLI 의 자리 | ΔE 안 | 독립 미지수 |
| LAM_PE 의 자리 | ΔE 안 | 독립 미지수 |
| LAM_NE 의 자리 | ΔE 안 | 독립 미지수 |
| 임피던스 | η (독립 미지수) | 우리 목적함수에 없음 (열역학 전용) |
| 분해 수단 | **충전 전류 크기** (0.33C 대 1.4–3C) | 곡선 형상 적합 |
| 산출물 | 두 그룹의 **중요도 점유율(%)** | 세 모드의 **크기(%)** 와 그 식별 가능성 |

`[해석]` ★ **결론: 이 논문의 "decoupling" 은 우리가 말하는 열화 모드 분리와
다른 축의 분해이며, 우리 문제는 이 논문의 "thermodynamic" 한 칸 **안에**
통째로 들어 있다.** 논문의 두 상자 중 하나가 우리의 세 미지수를 전부 삼킨다.
그러므로:

- 이 논문은 우리 degeneracy 질문에 **답하지 않는다.** 반증도 지지도 아니다.
- 반대로 이 논문은 우리가 답할 수 있는 질문을 **하나 정확히 열어 둔다** —
  `[인쇄]` Discussion: "**Addressing open challenges of electrochemical-level
  decoupling of degradation patterns could further consolidate the statistical
  evidence.**" 저자들이 자기 방법이 닿지 못하는 자리로 명시한 곳이 바로
  우리 축이다.
- 그리고 이 논문의 축(열역학 대 동역학)은 우리 축과 **직교**한다. 우리는
  임피던스를 목적함수에 넣지 않고, 이 논문은 LLI/LAM 을 가르지 않는다.

### 7.3 79 % 라는 수치는 무엇인가 ★

`[인쇄]` 본문: "thermodynamic losses, not kinetic, predominantly affect
degradation with a **79 %** share" · Fig. 5h 캡션: "Proportion comparison of
thermodynamic (**85 %**) and kinetic (15 %) loss types, averaged over all
temperatures. The machine learning insight, i.e., the contribution of
thermodynamic loss (**79 %**) is indicated."

두 수치의 정의를 SI Note 8 에서 따라가면:

- **79 % (ML)** = `Σ|SAGE(Q1)| + |SAGE(Q9)|` / `Σ|SAGE(Q1..Q9)|`
- **85 % (검증 기준)** = `Δ(Q1) + Δ(Q9)` / `Δ(Q1..Q9)`,
  여기서 `Δ(Q_i)` = `[인쇄]` "the absolute value of the difference between the
  feature value at the first and the 800th cycle" (0–1 정규화 후),
  `[인쇄]` "which is **regarded as the truth by manipulating the raw data**".

`[해석]` ★ **두 수치는 같은 9개 숫자(Q1…Q9)에서 나온다.** 하나는 그 9개의 SAGE
중요도 비, 다른 하나는 그 9개의 800 사이클간 변화량 비다. 따라서 79 % ↔ 85 %
일치는 **독립적인 검증이 아니라, 회귀 모델의 중요도가 입력의 변화량 크기를
따라간다는 (거의 자명한) 확인**이다. 논문은 이것을 `[인쇄]` "closely matches"
라고 쓰며 물리적 검증처럼 제시한다.

더 나아가, 어느 쪽도 **LLI·LAM·임피던스를 측정한 값이 아니다.** 둘 다
"저전류 두 단의 충전용량이 고전류 일곱 단보다 많이 변했다" 는 진술의 변형이다.
`[도표]` Fig. 4g 의 극좌표 그림이 이 구조를 그대로 보여 준다 — Q1 이 반경 ≈ 4
(노란색, 최대), Q9 가 ≈ 2, Q2–Q8 이 전부 중심 근처(≈ 0.2–1.5, 보라색). 79/21 은
이 아홉 점의 배분이다.

`[도표]` Fig. 4h 에서 한 가지 더: **RL(lumped resistance) 계열의 SAGE 중요도가
여러 단에서 음수**다 (약 −3×10⁻³ 까지). SAGE 가 음수라는 것은 그 feature 를
넣으면 손실이 커진다는 뜻이다. 논문은 이 그림에서 `[인쇄]` "RL and RO are more
significant" 라고만 쓰고 부호를 언급하지 않는다. 그리고 SI Note 8 의 배분식은
**절댓값**을 쓰므로, 손실을 키우는 feature 도 "기여" 로 집계된다.

### 7.4 논문이 스스로 인정하는 한계

`[인쇄]` (p.1551, Fig. 5a 논의 직후):

> "Despite the streamlined degradation model, **fully separating the degradation
> throughout a battery lifetime remains complex due to the dynamic interactions
> among degradation mechanisms**, see Fig. S25. **The challenge of distinctly
> identifying these mechanisms persists, even with advanced diagnostics** (Fig.
> S26–S29), which struggle to non-destructively elucidate internal aging states
> and their interdependencies, limiting practical utility."

`[해석]` 이것이 논문에서 식별 가능성에 가장 가까운 문장이다. 그러나 (a) 그
어려움을 **정량하지 않고**, (b) 바로 다음 문단에서 `[인쇄]` "Contrary to
bottom-up approaches …, the proposed method employs a **data-driven strategy to
decouple loss types**" 로 넘어간다. 즉 **"기구는 분리 못 한다 → 그러니 손실
유형을 분리한다"** 는 치환이 일어나고, 제목의 "degradation pattern decoupling"
은 그 치환 이후의 대상을 가리킨다. 제목과 §7.1 의 실제 산출물 사이의 거리가
이 논문에서 가장 조심해야 할 지점이다.

### 7.5 ICA 는 어디에 쓰였나

`[도표]` Fig. 5g: 방전 dQ/dV (2.8–4.2 V, −2.5 ~ 0 A h/V), 사이클 1–100(파랑) 대
700–900(빨강). **LAM · LLI · ΔE 라는 화살표 세 개가 손으로 그려져 있다.**
`[인쇄]` "confirms the existence of severe LLI and LAM, evidenced by reduced peak
intensity in low SOC areas (indicating **LAM at the anode**) and peak shifts
(signifying LLI)."

`[해석]` **정성 확인이고 수치가 없다.** peak 높이 감소 → LAM, peak 이동 → LLI
라는 읽기는 이 계보의 표준 관례이지만 (Dubarry/Birkl), 이 논문은 그 관례를
**적용만 하고 정량하지 않는다** — LAM 몇 %, LLI 몇 % 라는 수는 논문 전체에
없다. 게다가 "low SOC 의 peak 강도 감소 = 음극 LAM" 이라는 귀속은 참고문헌
[46] (Xie et al.) 에 기대는 것이지 이 논문이 half-cell 로 확인한 것이 아니다.
`[해석]` **우리 축에서 보면 이것이 이 논문에서 유일하게 LLI/LAM 을 구분하려 한
자리이며, 정확히 우리가 문제 삼는 그 관례(전극 귀속의 자명성)를 검증 없이
쓴다.**

---

## 8. FEA (COMSOL) 의 역할 (SI Note 7, Fig. 5c·5d, Fig. S30–S33, S40)

`[인쇄]` COMSOL Multiphysics 6.1, P2D 골격 (Nernst–Planck + Butler–Volmer +
Fick + Nernst), 노화는 **음극 SEI 성장 부반응 하나**로 모델링:
`S + nLi⁺ + ne⁻ → P_SEI` (식 9), 가속을 위해 화학량론을 τ 배로 재작성 (식 14–15).

★ 이 부분의 인과 방향이 중요하다. `[인쇄]` SI Note 7:

> "In the simulation of the battery aging process, **according to insights gained
> from machine learning**, the dominant contribution to battery capacity loss is
> thermodynamic loss, while the polarization contributing to kinetic loss is
> primarily driven by concentration polarization. Therefore, our simulation
> involves modeling the formation of SEI on the anode … **By adjusting the
> stoichiometric coefficient of LLI in the side reaction of SEI generation and
> the conductivity after SEI generation, we achieve control of the proportion of
> thermodynamic and kinetic loss** … thus aligning with the insights derived from
> machine learning."

`[해석]` ★ **시뮬레이션은 ML 결과를 검증하지 않는다. ML 결과에 맞춰 파라미터를
조정한 것이다.** 저자들이 그렇게 적는다. 따라서 Fig. 5c/5d 와 Fig. S40 의
"decoupled loss type" 은 ML 주장의 **독립 근거가 아니라 시각화**다. §7.3 의
79/85 대조와 합치면, 이 논문에서 열역학 85 % 라는 명제를 뒷받침하는 독립 측정은
**존재하지 않는다**.

`[도표]` Fig. S40: 방전 곡선 세 개(총 손실 빨강 / 열역학 파랑 / 동역학 초록)가
거의 겹치고, 무릎 근처에서만 띠가 벌어진다. 파랑 띠가 초록 띠보다 넓다 —
85/15 와 정성적으로 일치한다.

`[도표]` Fig. 5c: 애노드–분리막–캐소드 방향 Li⁺ 농도 (0.28–4.85 M) 를 S1 / S2–S8
/ S9 세 띠로 나눠 그리고, S1·S9 띠에 "Thermodynamics ΔE", 가운데 띠에
"Kinetics η" 라고 **라벨을 붙였다**. 초기 사이클 대비 1000번째 사이클에서
캐소드 쪽 농도 불균일이 크게 자란다. `[도표]` Fig. 5d: 과전위가 S2–S8 구간에서
노화와 함께 13 → 65 mV 로 자란다 (S1·S9 는 거의 변하지 않는다).

`[해석]` Fig. 5c/5d 는 **"저전류 구간에서는 농도 불균일이 작다"** 를 보여 주며,
이는 §4.3 의 배정 규칙(저전류 = 열역학)에 대한 합리적 근거다. 이 부분은
논문에서 물리적으로 가장 단단한 대목이다 — 단, 위에서 적었듯 파라미터가 ML
결과에 맞춰져 있으므로 **배정 규칙의 타당성**까지만 지지하고 **79 % 라는
수치**는 지지하지 않는다.

---

## 9. 기술경제 분석 (Fig. 6, SI Note 9–10) — 요약만

`[인쇄]` 네 가지 재활용 경로(refined direct = 이 논문의 진단으로 가능해지는
비파괴 리튬 보충 / direct / hydro / pyro)를 SOH 별 단위 이익으로 비교.
Li-naphthalenide 로 리튬만 보충하고 **해체를 건너뛴다**. TIM(Transport Impact
Model)으로 중국 시장을 2020–2060 전망: `[인쇄]` 스크랩 정점 2035년경 **2.3억 kg**,
2060년 스크랩률 **0.38 %**, 누적 이익 **197.6억 USD**. LFP 시제품 단위 수익
15.64 $/kg, 비용 2.37–2.63 $/kg.

`[해석]` 이 절은 우리 축과 무관하다. 다만 논문의 서사 구조에서 이 부분이 결론의
크기를 만든다는 점만 기록한다 — **"임계점 전에는 리튬 보충, 후에는 전극 수리"**
라는 처방(Fig. 5f 의 사각형 표식)은 §7 의 분해가 맞다는 전제 위에 서 있다.

---

## 10. 저자 공개 저장소와의 대조 감사 ★ (사용자 요청)

두 저장소를 읽기 전용으로 대조했다. 논문의 서술과 **맞는 것**과 **어긋나는
것**을 나눠 적는다.

### 10.1 데이터 저장소 — 대체로 맞다

`[코드]` `TBSI-Sunwoda-Battery-Dataset` 구성: `Features.xlsx` (21 MB),
`Labels.xlsx`, MATLAB 스크립트 4종 (`Gen_Feature.m`, `LoadFeature.m`,
`OutData.m`, `calculate_slopes.m`, `Visual_Voltage_Capacity.m`),
`Featurization taxonomy.pdf`, `Featurization formula.pdf`, 다단충전 시각화 영상.
원시/가공 `.mat` 는 Zenodo 에 있다 (저장소에는 없다).

| 논문의 서술 | 저장소 확인 결과 | 판정 |
|---|---|---|
| 셀 32개, 9/9/7/7 (25/35/45/55 °C) | `Features.xlsx`·`Labels.xlsx` 각 **32 시트**, `B1T25…B9T25`(9), `B10T35…B18T35`(9), `B19T45…B25T45`(7), `B26T55…B32T55`(7) | **일치** |
| feature 52개, ID 1–52 | 시트마다 **52열**, 순서·이름이 SI Note 2 의 ID 순서와 **정확히 일치** (T, U1–U9, VC89, VD9, tVD9, ReVC, ReVD, tReVD, Vg1–Vg9, RVg, Q1–Q9, RL1–RL9, RO1–RO8) | **일치** |
| 9단 프로토콜 SOC 배분 | README 표가 Table S1 과 C-rate·시간·SOC 까지 **일치** | **일치** |
| 수명 480–1025, 평균 775 ± 175 (EOL80) | `Labels.xlsx` 에서 0.88 A h 최초 하향 교차로 계산: **481–1025, 평균 775.9, 모표준편차 175.4** | **일치** |
| 온도별 EOL80 평균 (SI Fig. 2: 955/882/692/506) | 계산값 **954.4 / 879.4 / 683.9 / 505.4** | 25·35·55 는 1–3 사이클 차, **45 °C 는 8 사이클 차** |
| 전체 EOL80 평균 (SI Fig. 2e: **779**) | 계산값 **775.9**, 본문은 **775** | **SI 내부 불일치** (SI 779 vs 본문 775) |
| 시험 종료 SOH `[인쇄]` "from 73% to 59%" | 마지막 용량 최소 0.6476 (=SOH 0.589), 최대 0.8039 (=0.731) | **일치** |
| EOL73 수명 1218/1180/958/661 (Fig. 2g) | 0.803 A h 문턱으로 계산: **1197.5 / 1171.1 / 949 / 657.4**. 0.80 A h 문턱이면 1176 / 1181.9 / 959.4 / 662.3 | 35/45/55 는 **재현**(±2 사이클, 0.80 A h 문턱). **25 °C 는 재현 불가** |
| 셀당 기록 길이 | 25·35 °C = **1299** 행, 45 °C = 1099, 55 °C = 899 | 논문에 없음 |

★ **25 °C EOL73 이 재현되지 않는 이유가 구조적이다.** 공개 라벨에서 25 °C 셀
9개 중 **B8T25 는 EOL73 문턱(0.803 A h)에 끝까지 도달하지 않는다** (마지막 값
0.8039). 0.80 A h 문턱이면 3개(B6·B7·B8)가 도달하지 않는다. 그런데 `[도표]`
Fig. 2g 의 25 °C violin 에는 **점이 9개** 있고 `n=9` 가 인쇄돼 있다. 도달하지
않은 셀의 EOL73 을 어떻게 정했는지 논문에 설명이 없다 (외삽으로 보인다).
`[데이터]` 참고로 도달한 8개만의 표준편차는 **61.0** 사이클이고 Fig. 2g 에 인쇄된
25 °C 편차는 `[도표]` **0.06 × 10³ = 60** 이다 — 편차는 맞고 평균만 어긋난다.

`[코드]` README 와 SI Table S1 의 **반복 구간이 다르다**: README `[코드]`
"Steps **2 to 14** are repeated 3 times", Table S1 `[인쇄]` "Steps **3 to 14**
are repeated 3 times". 1단 차이이며 어느 쪽이 맞는지 알 수 없다.

`[데이터]` **U1–U9 는 셀마다 전 사이클에 걸쳐 정확히 상수다** (예 B1T25:
U1 표준편차 4.4e-16 V, 고유값 1개). 즉 Table S1 의 설계대로 초기 3 사이클에서
고정되며, **셀당 10차원 상수 벡터(T 포함 11차원)** 가 된다. 이것이 §10.2 의
해석에 결정적이다.

### 10.2 코드 저장소 — 논문과 어긋나는 곳이 여럿이다 ★

`[코드]` `Early-Battery-Degradation-Prediction-via-Chemical-Process-Inference`
구성: `BattDataLoader.py`, `ChemicalProcessModel.py`,
`DegradationTrajectoryModel.py`, `DomainAdaptModel.py`, `utils.py`, README.
학습 데이터 파일 `raw_data_0920.csv` 와 체크포인트 `.pt` 는 **저장소에 없다** —
공개 코드만으로는 재현 불가다.

| # | 논문의 서술 | 코드의 실제 | 등급 |
|---|---|---|---|
| 1 | Methods `[인쇄]` "Leaky rectified linear unit (Leaky ReLU)" (두 모델 모두) | `utils.py` 세 네트워크 전부 `torch.relu` — **일반 ReLU**. 저자 README 도 본문에는 "Leaky ReLU" 라 쓰고 바로 아래 코드 블록에 `torch.relu` 를 싣는다 | 명백한 불일치 |
| 2 | 식 (4)(14) `[인쇄]` 손실 = MSE + λ·Σ\|F_i − F̂_i\| (**잔차의 L1**) | `add_l1_regularization()` 은 `torch.norm(param, p=1)` — **가중치의 L1**(weight decay 류). λ = 1e-5 는 같지만 대상이 다르다 | 명백한 불일치 |
| 3 | `[인쇄]` "we split the data into **75 % and 25 %** for training and testing" | `BattDataset`: 학습 = **25 °C 와 55 °C 전 사이클 + 35/45 °C 의 첫 200 사이클**, 시험 = 35/45 °C 의 **201 사이클 이후**. 셀 단위 분할이 아니고 75/25 도 아니다 (200/1299 ≈ 15 %) | 불일치 |
| 4 | CP 모델 `[인쇄]` 30 epoch, lr 1e-4 | `train_epochs = 100`, `learning_rates = [3e-4, 1e-4]` 두 개를 모두 돈다 | 불일치 |
| 5 | 궤적 모델 `[인쇄]` lr 1e-3 | `learning_rates = [1e-3, 2e-3, 3e-3]` 루프를 돌지만 옵티마이저는 `lr=0.0001` **하드코딩** — 루프가 무효 | 불일치 + 버그 |
| 6 | 모델 선택 절차 (논문에 없음) | 두 학습 스크립트 모두 **시험 손실이 최저인 epoch 의 가중치를 저장**한다. `valid_dataset` 은 `BattDataset(raw_data, train=True)` 로 **학습셋의 복사본**이다 | 시험셋에 대한 조기종료 = 낙관 편의 |
| 7 | Methods `[인쇄]` 식 (8): start = 100, end = 200, n = 50 | `DomainAdaptModel.py`: `early_cycle_start = 0`, `early_cycle_end = 200`, `sample_size = 20` | 불일치 |
| 8 | 식 (6) `[인쇄]` AT = r_target / r_source | `gradient()` 가 `np.log(abs(grad/rang))` 를 반환하고 `at25 = gradient(real45)/gradient(pre25)` — **로그의 비**이지 비의 로그도, 비도 아니다 | 정의 불일치 |
| 9 | 식 (11)(12) 다중 source 앙상블 W_i·AT_i·r_i 합 | 실제 갱신은 `feature_1[i] = last45[i] + (pre55[i][0]-last55[i][0])*at55[i]` — **55 °C source 하나만** 쓴다. 바로 위에서 계산한 `step1`(25 °C 항)과 `w_at_25` 는 **사용되지 않는다** | 다중 source 주장과 불일치 |
| 10 | 온도 적응은 Arrhenius (식 5–6) | 실제로는 온도별 **하드코딩 곱셈 상수 10개**로 U 벡터를 재척도한다 (예 T35: −12.97, −11.08, …). `[코드]` 주석: "the map matrix is calculated by the average of voltage" | 물리가 아니라 수동 정규화 |
| 11 | 예측은 모델 출력 | `pred_y = model_2(...) **- 0.03**` — 하드코딩된 30 mAh 오프셋 보정 (공칭용량의 2.7 %) | 미기재 보정 |
| 12 | MAPE 식 (18) `Σ|y−ŷ| / Σy` | `utils.mape_loss` 는 `mean(|(y_true−y_pred)/y_true|)` — 점별 상대오차의 평균 | 미세 불일치 |
| 13 | 정답은 측정 용량 | 라벨이 `filter_cap`(필터링된 용량)이고 `cap` 은 그림용(`y_plot`)이다. 보고 MAPE 는 `y_tensor`(=filter_cap) 기준 | 평활된 정답 |
| 14 | 35 °C 셀 9개 | `battery_dict["T35"]` 에 항목이 **7개**뿐이고, 평균도 `battery_num = 7` 로 나눈다 (`test_tmp=="T25"` 일 때만 9) | 2개 셀 미평가 |
| 15 | — | `MyNetwork3.__init__` 이 `super(**MyNetwork1**, self)` 를 호출 — 인스턴스화 시 `TypeError`. `DomainAdaptModel.py` 는 `BattDataset` 에서 5-튜플을 받는데 공개 `BattDataLoader.py` 는 4-튜플을 반환 | 공개 코드가 그대로는 실행 불가 |

★ **가장 무거운 것은 3번과 6번이다.** 시험 대상 셀(35·45 °C)의 **첫 200
사이클이 학습에 들어가고**, 같은 셀의 나머지가 시험이 된다. 셀 단위 hold-out 이
아니다. 게다가 §10.1 에서 확인했듯 **U1–U9 는 셀마다 상수**이므로, CP 모델의
입력 `(T, U1…U9, cyc)` 에서 U 벡터는 **셀 식별자**로 기능한다. 즉 1단계 모델이
학습하는 것은 "이 셀 지문 + 이 사이클 번호 → 이 feature 값" 이며, 시험 구간은
같은 셀의 **사이클 방향 외삽**이다. 그리고 3단계 궤적 모델의 입력 53차원은
`[T, U1…U9, cyc] + 42 feature` 이므로 **사이클 번호와 온도가 용량 예측기에 직접
들어간다.**

`[코드]` 덧붙여 `cyc` 는 온도군마다 다른 상수로 정규화된다 (`T35["cyc"]*1299`,
`T45["cyc"]*1099`) — 즉 입력은 "사이클 / 그 온도군의 기록 길이" 이고, 기록
길이는 그 온도군의 수명과 함께 움직인다.

### 10.3 저장소 대조가 §5.2 에 주는 것

`[해석]` 논문의 "physics-informed" 를 코드로 내려보면 남는 물리는:
(a) feature 를 고를 때의 물리적 동기, (b) "노화율 비로 source 를 가중한다" 는
규칙. Arrhenius 지수식은 **구현되지 않는다.** 온도는 하드코딩 척도 상수와
입력 T 로만 들어온다. 이것은 논문이 스스로 식 (7)–(9)에서 예고한 귀결이지만
(E_a 미지 → 기울기로 대체), 코드는 그 대체가 논문의 서술보다 **더 멀리** 갔음을
보여 준다 (로그의 비, 단일 source, 수동 척도).

### 10.4 값싼 대조 기준선 (우리 계산) ★

`[데이터]` 공개 `Labels.xlsx` 만으로, 논문과 **같은 정보 예산**에서 가장 단순한
기준선을 계산했다 — **대상 셀 자신의 사이클 100–200 용량에 직선을 맞춰 수명
끝까지 외삽**. (논문 Methods 가 노화율 산정에 쓰는 구간이 정확히 100–200 이다.)
MAPE 는 전 궤적(사이클 1 ~ 끝) 기준, 셀별 평균:

| 설정 | 35 °C | 45 °C |
|---|---|---|
| **직선 외삽 (사이클 100–200 적합)** | **1.45 %** | **1.25 %** |
| 논문 (다중 source, 조기 20 %) `[인쇄]` | 1.4 % | 0.6 % |
| 직선 외삽 (사이클 1–50 적합) | 5.10 % | 6.60 % |
| 논문 (단일 source 55 °C, 조기 50 사이클) `[인쇄]` Table S4 | 2.11 % | 0.99 % |
| 직선 외삽 (사이클 1–25 적합) | 19.96 % | 13.49 % |
| 논문 (단일 source 55 °C, 조기 25 사이클) `[인쇄]` Table S4 | 2.52 % | 1.27 % |

`[해석]` ★ 두 갈래 결론이 나온다. **(a) 논문의 headline 설정(200 사이클
= 20 %)에서는, 두 개의 완전한 source 도메인 + 52 feature + 3단 파이프라인이
35 °C 에서 자(ruler)와 사실상 동률이다** (1.4 % vs 1.45 %). 45 °C 에서만 약 2배
낫다. **(b) 반대로 초조기(25–50 사이클) 영역에서는 자가 무너지고(13–20 %)
논문의 방법이 확실히 이긴다.** 즉 이 방법의 실질 가치는 **초조기 영역**에 있고,
Fig. 4a/b 의 대표 수치는 그 가치를 보여 주는 자리가 아니다. 논문은 자기 방법을
LSTM(발산)과 경험식에만 견주고, **단조 외삽 기준선을 두지 않는다.**

주의(이 비교의 한계): (i) 논문 MAPE 의 정확한 사이클 범위가 인쇄되지 않았다,
(ii) 코드 기준 정답은 평활된 `filter_cap` 인데 우리는 원 `Capacity` 를 썼다,
(iii) 우리 기준선은 대상 셀의 100–200 사이클을 쓰므로 "guiding sample 이
전혀 없는" 설정이다 — 논문보다 **적은** 정보를 쓴다.

---

## 11. 원문 내부 불일치 목록

### 11.1 abstract 의 headline 수치를 SI 표에서 재현할 수 없다 ★

`[인쇄]` 초록: "retaining a **95.1 %** average accuracy across temperatures"
(= MAPE 4.9 %). `[인쇄]` 본문 p.1550: "In an ultra-early verification setting …
utilizing the first 50 cycles, our model achieves average MAPEs of **4.9 %**
across 25, 35, and 45 1C, outperforming benchmarks under similar data
limitations (**Table S4**)." `[인쇄]` Discussion: "a modest **4.9 %** error using
just 4 % of total lifetime data (50 cycles)".

그런데 `[인쇄]` Table S4 의 해당 설정("The first 50 cycles are accessible",
Ourwork) 값은 45 °C **0.99**, 35 °C **2.11**, 25 °C **2.64** 이고, 세 값의
평균은 **1.91 %** 다. maxMAPE 평균도 2.82 %, 25 사이클 열의 평균도 2.31 % 로
4.9 % 에 닿지 않는다.

`[해석]` **논문이 자기 표보다 불리한 수치를 초록에 썼다.** 방향은 보수적이지만,
그렇다고 근거가 생기는 것은 아니다 — **4.9 % 의 출처를 논문 안에서 찾을 수
없다.** 인용할 때는 Table S4 의 개별 값을 쓰고, 95.1 % 는 쓰지 않는다.

### 11.2 model 2 / model 3 의 혼동과 두 개의 후기 MAPE

`[인쇄]` p.1550: "Notably, **model 2** worsens in the last 10 % of cycles, with
MAPE of **5.82 %**, underscoring the importance of **temperature
consideration, which model 2 lacks**. Despite initial similarities, IMVs become
crucial in later stages, with **model 2** showing a late-cycle MAPE of
**5.62 %**."

두 문제: (a) 온도 고려가 없는 것은 model 2(No-IMV)가 아니라 **model 3**
(no-transfer)다 — SI Note 4 가 그렇게 정의한다. (b) 같은 model 2 의 후기
MAPE 가 한 문단에서 5.82 % 와 5.62 % 로 두 번 다르게 인쇄된다.
`[도표]` Fig. 4c 후기 10 % 패널을 보면 LSTM ≈ 6.2, No-MV ≈ 6.0, No-transfer
≈ 3.6, Empirical ≈ 11.5 이므로 5.82/5.62 는 **LSTM 과 No-IMV 의 값**으로 보인다
(`[해석]`, 확정 불가).

### 11.3 EOL 정의가 세 개다

`[인쇄]` 데이터셋 서술은 **EOL80**, Fig. 2g 는 **EOL73**, 성능 서술은
`[인쇄]` "Utilizing merely 20 % of the lifetime data under **EOL75** criteria"
(문장이 술어 없이 끊긴다). 세 정의 사이의 환산이 없어 "수명의 20 %" 가 몇
사이클인지 독자가 계산할 수 없다.

### 11.4 SOC 고정 대 전압 고정

SI Note 3 은 `Q_i = Q(soc = soc_i)`, `U_i = V(soc = soc_i)` 로 **SOC 를 고정**해
정의하는데, Table S1 은 첫 3 사이클 이후 **전압 cut-off 를 고정**해 운전한다고
적는다. 노화하면 같은 전압에서 SOC 가 달라지므로 두 정의는 양립하지 않는다.
`[해석]` 실제로는 전압 고정 운전이고 Q_i 는 "그 전압에 도달할 때까지 넣은
전하" 로 보인다 — 그렇다면 Q_i 의 감소는 **charge acceptance 감소**를 재는 것이
맞다. 그러나 SI 의 식은 그 반대로 읽힌다.

### 11.5 Fig. 5f 의 "correlation" 은 거리다

`[인쇄]` Methods: "The correlation between two chemical processes in window Win_i
is defined as their **2nd-order Wasserstein distance**." Fig. 5f 의 세로축
라벨은 `[도표]` "Degradation correlation (a.u.)" 이고 0.5–1.0 범위다. 거리와
상관은 부호도 단위도 다르다. 이 축 위에서 읽어 낸 "임계점"(Fig. 5f 의 원·사각형
표식)이 §9 의 재활용 처방으로 이어지므로, 축의 정의가 흐린 것은 결과에 직접
영향을 준다.

### 11.6 SI Fig. 26–28 의 상호 참조가 하나씩 밀려 있다

`[인쇄]` SI Fig. 26·27·28 캡션이 모두 "…in **Supplementary Figure 24**" 를
가리키는데, 열화 모드–부반응 관계도는 **Fig. S25** 다 (Fig. S24 는 초기 200
사이클 용량 차이 그림). 세 캡션이 같은 방향으로 하나씩 밀렸다.

---

## 12. 어휘 전수 (이 계보 아홉 편째)

본문(16쪽) + SI(75쪽) 텍스트 전체에 대해:

| 어휘 | 본문 | SI | 비고 |
|---|---|---|---|
| `identifiab*` | **0** | **0** | |
| `degenerac*` | **0** | **0** | |
| `ill-posed` | 0 | 0 | |
| `non-unique` / `uniqueness` | 0 | 0 | |
| `cross-valid*` | **0** | **0** | 분할 설계 서술 자체가 없다 |
| `error bar` / `confidence interval` | 0 | 0 | |
| `collinear*` | 0 | 0 | |
| `half-cell` | **0** | **0** | 전극 수준 분해 절차 없음 |
| `teardown` | 0 | 0 | (`post-mortem` 은 본문 2회, 모두 "우리는 안 한다" 맥락) |
| `uncertaint*` | 4 | 0 | 3회는 **제조 불확실성**, 1회는 SAGE 정의의 "reduction of uncertainty in output Y" |
| `LLI` | 12 | 9 | 전부 정성 |
| `LAM` | 7 | 4 | 전부 정성 |
| `OCV` | 0 | 4 | 전부 SI Note 1 의 식 (1) 설명 |
| `open-circuit` | 1 | 4 | 본문 1회는 Methods 의 `U_theoretical` 정의 |

(합자 `ﬁ`/`ﬂ`·하이픈류를 정규화한 뒤 센 값이다.)

`[해석]` 이 계보에서 아홉 편 연속으로 `identifiab*`·`degenerac*` 가 **자기
추정에 적용된 사례가 0** 이다 (Rhyu 2025 의 1회는 참고문헌 제목, Zhang 2020 의
`non-unique` 1회는 경쟁 방법 비판). 이 논문의 특이점은 **개념을 문장으로는
말한다는 것** — `[인쇄]` "The challenge of distinctly identifying these
mechanisms persists" 와 Fig. 5b 의 "Hard to decouple" — **그런데 그 어려움을
정량하지 않고, 제목에는 "decoupling" 을 쓴다.** 지금까지 흡수한 여덟 편이
"어휘가 없다" 였다면, 이 논문은 **"어휘 없이 개념을 인정하고 넘어간다"** 는
새로운 형태다.

---

## 13. 우리 프로젝트와의 접점

### 13.1 걸리는 것

1. **우리 degeneracy 는 이 논문의 한 칸 안에 있다** (§7.2). 이 논문의 산출물은
   우리 판정의 반증도 지지도 아니다. **동시에, 이 논문의 방법을 우리 축으로
   확장하면 즉시 우리 문제에 부딪힌다** — ΔE 를 LLI/LAM_PE/LAM_NE 로 쪼개는
   순간 미지수가 2 → 4 가 되는데 관측은 늘지 않는다.
2. **이 논문은 우리가 채울 자리를 명시적으로 남긴다**: `[인쇄]` "Addressing open
   challenges of **electrochemical-level decoupling** of degradation patterns
   could further consolidate the statistical evidence." (Discussion)
3. **"저전류 구간 = 열역학" 이라는 배정은 우리 관측 설계에 쓸 수 있는 아이디어다.**
   `[인쇄]` SI Note 1 의 논리 — 전류를 바꾸면 ΔE 와 η 의 상대 비중이 바뀌고,
   그것이 곧 **관측 채널을 하나 더 얻는 방법**이다. 우리 파이프라인은 지금
   준평형 곡선 하나만 쓴다. `[해석]` 다만 이 논문은 그 채널로 **열역학 대 동역학**
   만 가르지, 열역학 **안**을 가르지 않는다. 우리에게 유용한 형태로 바꾸려면
   "전류를 바꿔서 얻는 추가 채널이 LLI–LAM_PE 방향에 정보를 주는가" 를 물어야
   하고, 그것은 우리 합성 truth 파이프라인에서 값싸게 답할 수 있다 (모드를 고정한
   채 두 전류에서 곡선을 뽑고 Jacobian 의 두 번째 특이값을 본다).

### 13.2 우리가 이 논문에 공급할 수 있는 것

- **식별 가능성의 경계.** 이 논문은 "LLI 와 LAM 은 함께 열역학" 이라고 **가정**
  하고 넘어간다. 그 가정이 필요한 이유(=full-cell 신호로는 못 가른다)를 우리가
  **정량**으로 줄 수 있다. 그러면 이 논문의 봉합은 회피가 아니라 **근거 있는
  설계 결정**이 된다.
- **단조 외삽 기준선**(§10.4)은 이 계보 전체에 적용 가능한 값싼 감사 도구다.

### 13.3 우리가 이 논문에서 가져올 수 있는 것

- **다전류 관측 채널** (위 3번).
- **AT score 형태의 도메인 가중** — 우리 문제에서 온도가 아니라 SOC 창·C-rate
  간 전이에 같은 형태를 쓸 수 있다. `[해석]` 단, 이 논문의 구현이 Arrhenius 를
  실제로 쓰지 않는다는 점(§5.2, §10.3)을 알고 가져와야 한다.
- **반면교사 두 가지**: (a) 중요도 점유율을 **물리 기여도**로 옮겨 적지 않기,
  (b) 시뮬레이션 파라미터를 ML 결과에 맞춘 뒤 그것을 검증이라고 부르지 않기.

### 13.4 이 논문이 우리 질문 카드에 주는 것

- [[pvs-sev-lli-lampe-separability]] 에: **Evidence 가 아니라 경계 확정 1건.**
  "관측을 늘리면 갈리는가" 의 후보로 **전류 축(다단 충전)** 이 추가된다. 그러나
  이 논문은 그 축으로 LLI↔LAM_PE 를 가르지 않았으므로 H1/H2 어느 쪽에도 무게를
  싣지 않는다.
- [[22p-physics-or-degeneracy]] 에: **직접 닿는 근거 없음.** 이 논문은 22p 와
  같은 좌표(LLI/LAM_PE/LAM_NE 분해값)를 산출하지 않는다.

---

## 14. 무엇을 봤고 무엇을 안 봤는가 (그림 판독 범위)

크로핑 결과: **fig 20장 + tab 2장** (본문 Fig. 1·2·3·5·6 + SI Fig. 1·3·7·8·9·10·
23·26·27·28·30·31·32·40 + Table S4·S5).

- **자동 크롭이 놓친 것 1건**: 본문 **Fig. 4** 의 캡션 블록을 추출기가 잡지
  못했다. 같은 ingest 안에서 p.8 의 이미지 bbox 를 직접 잘라
  `fig_4.png` 로 넣고 `figures.json` 에 `note` 를 달아 표시했다.
- **자동 크롭이 제외한 것 4건** (그래픽 없음 판정): SI Fig. 2·4·5·6. 이 중
  **Fig. S2 의 수치는 SI 텍스트 레이어에서 그대로 읽었다** (Mean/Std 값이
  텍스트로 추출된다) — §10.1 의 대조에 쓴 값이 그것이다.

**실제로 Read 로 본 그림 (7장)**: `fig_1` (전체 구상) · `fig_2` (데이터·프로토콜·
Arrhenius) · `fig_3` (featurization taxonomy) · `fig_4` (성능·feature 중요도) ·
`fig_5` (decoupling — 이 논문의 핵심) · `fig_S23` (파이프라인) · `fig_S40`
(시뮬레이션 손실 분해).

**보지 않은 그림 (13장)**: SI Fig. 1·3·7·8·9·10 (SOH 분포·RPT 시점·온도별 충전
곡선 4장) · SI Fig. 26·27·28 (TEM/SEM) · SI Fig. 30·31·32 (COMSOL 농도·리튬화
가시화) · Table S4·S5 이미지. 표 2장은 PDF 텍스트가 정확하므로 텍스트로 읽었다.
SI Fig. 26–28 은 캡션이 충분히 서술적이고 정량값이 없어 판독 이득이 작다고
판단했다. **SI Fig. 11–22 (feature 별 노화 추세 48장 상당) 는 크로핑 대상에도
들지 않았고 보지 않았다** — 이 digest 는 그 그림들에 대해 아무 말도 하지 않는다.

**본문 서술과 그림이 어긋난 곳** (§11 에 정리): Fig. 4c 대 본문의 model 2/3
혼동, Fig. 5f 의 축 이름(correlation ↔ Wasserstein distance), Fig. 2g 의 25 °C
EOL73 평균이 공개 데이터로 재현되지 않는 것. 그리고 Fig. 4h 에서 **RL 계열
SAGE 가 음수**인데 본문은 부호를 언급하지 않는다.
