---
source_url: https://doi.org/10.1016/j.joule.2025.101884
ingested: 2026-09-03
sha256: 40b19bef75884156b2f075f1a244f48488e63cab2350b34a9daaabada24035d6
---

# Rhyu et al. 2025 — Systematic feature design for cycle life prediction of lithium-ion batteries during formation

> **서지** J. Rhyu, J. Schaeffer, M. L. Li, X. Cui, W. C. Chueh, M. Z. Bazant,
> R. D. Braatz, "Systematic feature design for cycle life prediction of
> lithium-ion batteries during formation", *Joule* **9** (2025) 101884.
> DOI 10.1016/j.joule.2025.101884. Received 2024-10-08 · Revised 2025-01-14 ·
> Accepted 2025-02-28 · Published online 2025-03-28 · Issue 2025-05-21.
> Lead contact: R. D. Braatz (braatz@mit.edu).
> 소속: MIT ChemE(1) · TU Darmstadt(2) · Stanford MSE(3) · SLAC(4) ·
> Stanford Energy Sci.&Eng.(5) · MIT Math(6).
> 자금: Toyota Research Institute **D3BATT**; J.R. 은 관정이종환재단 지원.
>
> **왜 흡수했나** 2026-09-02 BML 세미나(김시원) p.4 의 두 인용 중 **둘째**가
> 이 논문이다 (`Joule, 2025, 9, 101884`). 첫째는 Wang et al. 2025 리뷰
> (`Adv. Energy Mater. 15, e03067`) 이고, 이 논문은 그 리뷰의 참고문헌 [113]
> 이기도 하다. 세미나가 제안한 PVS·SEV 두 feature 의 **직접적 선행 프레임**
> 으로 지목된 자리다.
>
> **표기 규약** (이 위키 관례) — `[인쇄]` 원문 본문/표에 인쇄된 것 ·
> `[도표]` 그림에서만 읽은 것(= `figure-read ≈`) · `[해석]` 우리 판단.
> `[해석]` 표시가 없는 문장은 전부 원문이 실제로 말한 것이다.

---

## §0. 부속 파일 확인 — mmc2 는 사본이다

사용자가 함께 올린 `mmc2.pdf` (34쪽) 를 열어 대조했다: **1–15쪽이 본문 PDF
(15쪽)와 동일**하고 (1쪽 graphical abstract, 15쪽 참고문헌 84–87 로 끝),
**16–34쪽이 SI (`mmc1.pdf`, 19쪽)와 동일**하다 (16쪽 "Joule, Volume 9 /
Supplemental information", 34쪽 Supplemental references S1–S9). 즉 mmc2 =
본문 + SI 를 이어붙인 **재수록본**이며 고유 내용이 없다. **이 흡수에서는
무시했다.** 인용 좌표는 본문 PDF(1–15쪽)와 SI PDF(1–19쪽)를 쓴다.

---

## §1. 원문에 없어서 확인이 필요한 것 (공백 목록)

이 절을 먼저 둔다 — 아래 본문에서 "n/a" 로 적히는 것들의 목록이다.

1. **데이터 포털의 zip 파일 이름·내용이 원문에 하나도 없다.** `Data and code
   availability` 절 전문은 §11 에 그대로 옮겼다. `zip` 이라는 단어가 본문·SI
   통틀어 **0회**이고, `Systematic_Feature_Design_Framework_Formation_main.zip`
   ·`Features_tsfresh_autoML_fulllist.zip` 라는 문자열도 **0회**다. → **원문
   미제시.** (§11 에 상세)
2. **추정 파라미터의 불확실성이 어디에도 없다.** SI Table S9 의
   전극 이용상태 4개(β_c, β_a, Q_rem/Q_c,total, V_shift)는 **점추정 하나씩**
   이고 신뢰구간·상관·감도가 없다. Fig. 6 의 물리모델 자유 파라미터 5개
   (E_A, k̄₀,c, k̄₀,a, σ_c, σ_a)도 값 하나씩만 인쇄돼 있고 **적합 절차·적합
   오차·불확실성이 없다**.
3. **물리모델과 실험의 정량 일치도 지표가 없다.** 비교는 시각적이다
   (`[인쇄]` "we see striking similarities in the location of the local maxima
   and minima"). RMSE·R² 같은 수치가 n/a.
4. **두 설계 feature 사이의 실제 상관계수가 인쇄되지 않았다.** Algorithm S2 가
   |ρ| > 0.2 를 걸러내므로 상한만 알 수 있다.
5. **Q^B(V) 이외 세 입력 데이터형(V^B(t̃), Q^C(V), V^C(t̃))으로 설계한 feature 의
   예측 성능이 없다.** SI Table S4–S6 은 **어떤 feature 가 뽑혔는지만** 싣고
   MAPE/RMSE 를 싣지 않는다.
6. **cell-to-cell 하한 6% MAPE 의 신뢰도.** Note S10 은 프로토콜당 n_k = 2~3
   셀에서 σ_k 를 추정했다 (Table S7). 표본 2~3 개의 표준편차이므로 이 하한
   자체가 매우 거칠다 — 원문은 이 점을 논하지 않는다.
7. **62 프로토콜의 outer fold 배정이 무작위 셔플 1회**다 (Note S3). 다른 시드로
   반복했을 때 Table 4 의 전압값이 얼마나 흔들리는지 n/a.
8. **왜 하필 fused lasso 인가에 대한 대안 비교가 없다.** total variation 이 아닌
   다른 구조적 정규화(예: group lasso, wavelet)와의 비교 n/a.
9. **설계 feature 가 열화 모드(LLI/LAM)와 어떻게 연결되는지 원문이 말하지
   않는다.** §12·§14 에서 이 공백을 정면으로 다룬다.

---

## §2. ★ 이 흡수가 답해야 할 우선 질문 3개 — 판정

근거 등급 규약: **A** = 원문에 인쇄된 문장/수치로 직접 확인 · **B** = 원문
인쇄에서 기계적으로 도출되지만 원문이 그렇게 말하지는 않음 · **C** = 우리
해석(원문 밖, 반박 가능).

### 질문 ① "systematic feature design" 의 절차가 정확히 무엇인가

**판정: 데이터 우선(data-first) 파이프라인이고, 물리는 두 지점에서만 들어온다
— 앞에서는 "후보를 지우는 가위"로, 뒤에서는 "사후 설명"으로. feature 의
형태(functional form)를 만드는 것은 물리가 아니라 선형모형의 대수다.**
근거 등급 **A**.

절차는 Figure 2 의 6+1 단계이며 (직접 봄), 각 단계의 원문 인쇄는 다음과 같다.

| # | 단계 | 무엇을 하나 | 사람이 넣는 값 |
|---|---|---|---|
| 0 | Extraction of input data candidates | 측정 7종에서 후보 입력 데이터를 만든다 → **6종**: `Q^A(V)`, `t^A(V)`, `Q^B(V)`, `V^B(t̃)`, `Q^C(V)`, `V^C(t̃)` | 도메인 지식으로 후보를 **지운다** (아래) |
| 1 | Input data evaluation (autoML) | tsfresh 로 ~800 feature 자동 추출 → 입력형별 408 모델(총 2,448) → 어느 입력형이 "유망"한지 판정 | p-value 격자 17점, 알고리즘 6종 |
| 2 | Determination of λ | fused lasso 의 λ 를 **예측성·강건성·해석성** 3제약으로 고른다 | DTW ratio < 0.7, path length < 5, 1SE rule |
| 3 | Partitioning of X based on β | β 의 **점프** 위치로 전압축을 구간 분할 | 점프 문턱 `0.001 × (max β − min β)` |
| 4 | Design features (Difference & Mean) | 각 구간에서 **차분**과 **평균** 두 feature 면 충분함을 대수적으로 유도 (Eq. 3–5) | 없음 (유도됨) |
| 5 | Merge sections (Algorithm S1) | 불필요한 경계를 RMSE 기준으로 병합 | `th_merge = 0.01` (≈ 1% 오차) |
| 6 | Feature down-selection (Algorithm S2) | 출력과의 Pearson 상관이 큰 것부터 뽑고, 서로 상관 큰 것은 버린다 | `th_PC,X = 0.2`, `th_PC,y = 0.4` |

**물리가 들어오는 곳 (전부)**

- **앞쪽 — 후보 가지치기 (지우기만 한다).** `[인쇄]` "the current I can be
  discarded because I is constant for most of the process" · "the range for V
  is identical for all formation protocols whereas the range for t and Q within
  each step may vary from cell to cell. Therefore, the t and Q should be
  normalized" · "we may not use t̃ and Q̃ as input variables in step A since a
  single t̃ cannot specify the SoC of the cell whereas a single Q̃ masks the
  impact of C-rate" · "any input data of f(t̃) and f(Q̃) are redundant for the
  CC steps due to Q = It". → 도메인 지식은 **후보 목록을 줄이는 데만** 쓰이고,
  새 물리량을 **만들지는 않는다**.
- **뒤쪽 — 사후 설명.** Figure 5 의 초록 점선(= "missing link")이 그것이다.
  feature 는 이미 정해진 뒤에, 그 feature 가 왜 예측력이 있는지를 반응입자
  앙상블 모형으로 사후 설명한다. `[인쇄]` "we conduct a physics-based
  investigation, **which is guided by the designed features**".

**feature 의 형태를 만드는 것은 물리가 아니다.** Eq. 3–5 가 전부다: β 가 구간
안에서 평평하므로 그 구간의 Q̃^B_i(V) 를 직선 `a_i V + b_i` 로 근사하면
`ŷ_section = a_i C₁ + b_i C₂` 이고, 기울기 `a_i` 는 `Q^B_i(V₂) − Q^B_i(V₁)` 의
아핀 변환, 절편 `b_i` 는 `mean(Q^B_i(V₁–V₂))` 의 아핀 변환이 된다. `[인쇄]`
결론: "**only two features are needed to describe each section**:
Q^B_i(V₂) − Q^B_i(V₁) and mean(Q^B_i(V₁–V₂))". 이것은 전기화학이 아니라
**선형대수**다.

**저자들이 이 프레임을 무엇의 대안으로 놓는지도 명시적이다.** `[인쇄]`
"This framework is especially useful for investigating systems with complicated
physics, such as SEI formation, where automatic feature extraction can be more
effective than **handcrafted features that are limited by the many unknown
aspects of the underlying physics**." 그리고 초록: "requires **minimal domain
knowledge**".

#### ★ 우리 설계(목적함수에 PVS·SEV 항을 얹는 것)는 이 절차의 어디인가

**판정: 이 절차 안에 자리가 없다. 두 가지 이유로 범주가 다르다.** 근거 등급
**B**(첫째) / **C**(둘째).

1. **PVS·SEV 는 이 논문이 명시적으로 대체 대상으로 지목한 "handcrafted
   features" 다** (위 인쇄 인용). 절차상 굳이 대응시키면 **단계 0**(도메인
   지식이 개입하는 유일한 앞단)인데, 이 논문의 단계 0 은 **후보를 지우기만
   하고 새 유도량을 만들지 않는다**. 즉 PVS·SEV 같은 "물리에서 유도한 스칼라"
   를 넣는 문(門)이 이 프레임에는 **없다**. 근거 등급 **B**.
2. **과제의 수학적 종류가 다르다.** 이 프레임은 **지도학습 회귀** `X → y`
   에서 X 의 어느 구간을 쓸지 정하는 것이다 (fused lasso 의 β 는 회귀계수다).
   우리가 하려는 것은 **역문제의 목적함수에 잔차 항을 추가**하는 것 —
   추정 대상이 y 가 아니라 파라미터이고, 최소화하는 것이 예측오차가 아니라
   모형-관측 불일치다. 이 논문의 β 는 우리 문제의 **Jacobian** 자리에 오지
   않는다. 근거 등급 **C**.

**그럼에도 이식 가능한 조각은 있다** (근거 등급 **C**, §14 에서 구체화):
단계 2–5 의 기계장치 — "**fused lasso 로 β 를 얻고, β 의 점프로 전압축을
구간분할하고, 구간마다 차분·평균 두 항만 남긴다**" — 는 우리 목적함수에서
**어느 전압창에 가중치를 줄 것인가**를 정하는 데 그대로 쓸 수 있다. 다만
그때 y 는 cycle life 가 아니라 **모드 파라미터**여야 한다 (질문 ③ 참조).

### 질문 ② identifiability / degeneracy / uncertainty 어휘 전수

**판정: 계보 4편의 "연속 0회" 기록은 깨진다 — 그러나 깨지는 방식이
결정적으로 약하다. 세 어휘의 본문 등장은 여전히 0회이고, 유일한 1회는
참고문헌 목록의 논문 제목이다.** 근거 등급 **A**.

전수 결과 (합자 정규화 `ﬁ`→`fi` 후 대소문자 무시, 본문 15쪽 + SI 19쪽 전체):

| 어휘 | 본문 | SI | 어디에 |
|---|---|---|---|
| `identifiab*` | **1** | 0 | **참고문헌 [30] 의 제목 안** (본문 서술 0회) |
| `degenerac*` / `degenerate` | **0** | **0** | — |
| `uncertain*` | **0** | **0** | — |
| `nullspace` / `null space` | **1** | 0 | **참고문헌 [13] 의 제목 안** (본문 서술 0회) |
| `ill-posed` / `ill-condition*` | 0 | 0 | — |
| `confidence interval` | 0 | 0 | — |
| `error bar` | 2 | 0 | Fig. 4B 캡션 + 본문 1회 (§8) |
| `collinear*` | 1 | 2 | Algorithm S2 근거 1 · SI VIF 검정 2 |
| `leakage` | 2 | 2 | nested CV 설계 근거 |
| `robust*` | 8 | 5 | **β 형상의 fold 간 일관성** 의미 (불확실성 아님) |

**0 이 아닌 것의 맥락을 그대로 옮긴다.**

- **`identifiability` (본문 1회, 참고문헌 [30])** — `[인쇄]`
  "30. Lin, J., and Khoo, E. (2024). **Identifiability study** of lithium-ion
  battery capacity fade using **degradation mode sensitivity** for a minimally
  and intuitively parametrized electrode-specific cell open-circuit voltage
  model. J. Power Sources 605, 234446."
  이 문헌이 본문에서 인용되는 자리는 **딱 한 곳**이고, 그것은 식별 가능성
  때문이 아니다. `[인쇄]` "diagnostic techniques such as **differential voltage
  fitting (DVF),²⁷⁻³⁰** ... were developed for physics-based feature
  extraction during battery operation." → [30] 은 **DVF 기법 4연속 인용의 네
  번째**로만 쓰인다. 논문 어디에서도 그 내용(모드 식별 가능성)이 논의되지
  않는다.
- **`nullspace` (본문 1회, 참고문헌 [13])** — `[인쇄]` "13. Schaeffer, J.,
  Lenz, E., Chueh, W.C., Bazant, M.Z., Findeisen, R., and Braatz, R.D. (2024).
  Interpretation of high-dimensional linear regression: **Effects of nullspace
  and regularization** demonstrated on battery data. Comput. Chem. Eng. 180,
  108471." 이 논문은 **저자 그룹 자신의 것**이고 (Schaeffer·Chueh·Bazant·
  Braatz = 이 논문 공저자 4명), 본문에서 인용되는 자리는 `[인쇄]` "we obtain a
  regression coefficient β that can give insights on **how each portion of the
  input data contributes to the output estimation**.¹³,⁸³" 다. 즉 **"β 는
  해석을 준다" 는 긍정 주장의 근거로만** 인용되고, 그 논문의 경고(고차원 선형
  회귀의 β 는 nullspace 때문에 유일하지 않다)는 **한 문장도 옮겨지지 않는다**.
  `[해석]` 이 논문이 자기 계보의 nullspace 경고를 알고 있으면서 β 해석을
  방법의 중심에 놓았다는 사실은, 이 저자들이 그 위험을 **의식적으로 감수**
  했다는 뜻으로 읽힌다 — 그런데 그 트레이드오프를 본문에서 논하지 않는다.
- **`error bar` (2회)** — 이것이 이 논문에서 불확실성에 가장 가까운 것이다.
  `[인쇄]` "While the best autoML and designed models also have some protocols
  with large deviations, many of them have **large variations within the
  predicted cycle lives (i.e., long error bar)**. These variations indicate that
  **the evaluation of such formation protocols may not be trustworthy**, and
  thus additional cell testing could lead to a better evaluation. **The agnostic
  model cannot give such guidance to the user since it does not capture any
  cell-to-cell variability**."
  `[해석]` 중요한 지점이다. 이 error bar 는 **예측 구간이 아니라 형제 셀
  2~3개의 예측값 min–max 폭**이다 (Fig. 4B 캡션 `[인쇄]`: "Average (dot) and
  **maximum and minimum (error bar)** of true and predicted cycle lives per each
  formation protocol"). 즉 셀 간 산포를 신뢰도 대리(proxy)로 쓴다. 이것은 정식
  UQ 가 아니지만, **모델의 출력이 얼마나 믿을 만한지를 사용자에게 알려야
  한다는 문제의식 자체는 이 계보에서 처음** 나타난 것이다.
- **`robustness`** — 이 논문에서 "강건성" 은 **β 형상의 fold 간 일관성**으로
  조작적 정의된다 (Table S2 `[인쇄]`: DTW distance ratio). 파라미터 불확실성이
  아니다. 이 구분을 흐리면 안 된다.

**계보 대조 (이 위키의 누적 기록)**: Birkl 2017 · Dubarry 2012 · Kim 2023 ·
Su 2024 는 세 어휘 모두 0회였다. Wang 2025 리뷰도 0회였다. Rhyu 2025 는
**참고문헌에서만 1회** — `[해석]` 엄밀히 말하면 "연속 0회" 는 깨졌지만,
**논문이 자기 방법에 대해 식별 가능성을 묻는 문장은 여전히 0개**다. 이번
흡수의 수확은 "Braatz 그룹은 다르다" 가 아니라 **"이 계보에서 가장 방법론적으로
정교한 팀조차, 인접 문헌으로 그 어휘를 알고 있으면서, 자기 추정에는 적용하지
않는다"** 는 더 강한 형태의 확인이다.

### 질문 ③ feature 와 예측 대상의 관계 — cycle life ↔ 열화 모드 분율

**판정: 원문에는 두 과제가 같은 feature 를 쓸 수 있다는 근거가 없다. 오히려
반대 방향의 증거가 원문 안에 있다.** 근거 등급 **A**(사실관계) / **B**(반대
방향 증거의 도출).

**(a) 예측 대상은 오로지 cycle life 다.** `degradation mode` 는 본문 2회
등장하는데 **둘 다 참고문헌 제목 안**이다 ([16] Reniers "degradation models",
[30] Lin&Khoo "degradation mode sensitivity"). `LLI`·`LAM` 이라는 약어는
본문·SI 통틀어 **0회**다. 설계 feature 를 모드 분율에 연결하는 문장은 **없다**.

**(b) 그러나 SI Note S11 은 우리 축의 4-파라미터 적합을 실제로 수행한다.**
이것이 이번 흡수에서 가장 놓치기 쉬운 것이다. `[인쇄, SI p.15]`
"In this model, the system is parameterized by four parameters: **fraction of
cathode capacity 'active' to filling/emptying β_c, fraction of anode capacity
active to filling/emptying β_a, remaining lithium inventory capacity Q_rem,**
and **voltage shift due to external resistances V_shift**. These parameters
consist the system's **utilization state resulting from formation**."
좌표 대응은 명백하다: `1−β_c ↔ LAM_PE`, `1−β_a ↔ LAM_NE`,
`1−Q_rem/Q_c,total ↔ LLI`, `V_shift ↔ 저항성 전압강하`.
결과 (Table S9, 느린 형성 셀 32개 평균):

| 상태변수 | 값 | 단위 |
|---|---|---|
| β_c | **0.911** | – |
| β_a | **0.854** | – |
| Q_rem / Q_c,total | **0.930** | – |
| V_shift | **0.014** | V |

그리고 이 적합 결과를 **모드 언어로 해석한다**. `[인쇄, SI p.16]`
"Interestingly, the learned utilization state indicates that **the effective
capacity lost at each electrode is greater than the lithium inventory lost**,
an indication that further understanding needs to be made into both the
effective active capacity state variable β_j and designing batteries where
these values are maximized."
→ `[해석]` 이것은 **"LAM > LLI 다"** 라는 주장이며, 우리 프로젝트가 판정
대상으로 삼는 바로 그 종류의 진술이다. 그런데 (i) 오차 막대 없음, (ii) 식별
가능성 진단 없음, (iii) 저자 자신이 적합 실패를 인정 (`[인쇄]` "the electrode
utilization captures the broad features of the experimental dataset, but
**still fails to fit the differential capacitance versus voltage curve
perfectly**"), (iv) 셀 개별이 아니라 **32셀 평균 곡선 하나**에 대한 적합이다.

**(c) 두 과제가 같은 feature 를 쓸 수 있다는 근거는 원문에 없고, 원문 안의
증거는 오히려 "이 데이터셋에서는 둘이 분리된다" 쪽이다.** 근거 등급 **B**.

- `[인쇄, 본문 p.9]` "In a post-formation C/20 low-rate test (reference
  performance test [RPT]) across these cells, shown in Figure S12, **the
  differential capacitance and d²Q/dV² electrochemical signatures are nearly
  indistinguishable. This is an indication that the electrode utilization and
  remaining lithium inventory are likely similar across these cells. However,
  the performance, as quantified through cycle life, is not identical across all
  these cells.**"
- Fig. S12(a,b) 를 직접 봤다 — 25 °C~55 °C 로 색이 나뉜 곡선들이 **거의 완전히
  겹친다** (dQ/dV 최저점 ≈ −2.5 [1/V] 부근에서 색 구분이 사실상 불가). `[도표]`
- `[해석/판정]` **느린 형성 32셀에서: 이용상태(≈ 모드 좌표)는 거의 같은데
  cycle life 는 다르다.** 그러면 그 데이터에서 cycle life 를 예측하는 정보는
  모드 좌표 **밖**에 있다. 저자들의 설명도 정확히 그것이다 — 예측력의 출처를
  **미시 입자 저항 분포(동역학)** 로 돌린다. `[인쇄]` "the features contain
  information both on the average resistance of the two electrodes and **the
  underlying resistance heterogeneity from the complex microscopic system
  state**. While the former may be gleaned from simpler features, ... **the
  latter is unique to the designed features**".
- **결론**: 이 논문의 설계 feature 는 **열역학적 모드 좌표가 아니라 동역학적
  불균일성**을 읽는다고 저자들이 말한다. 따라서 "cycle life 예측 feature =
  모드 추정 feature" 는 **원문이 주는 것이 아니라 우리가 유추하는 것이고,
  이 논문 안에는 그 유추에 불리한 관측이 있다.** 흐리지 않고 이렇게 적는다.

---

## §3. SUMMARY (초록) — 전문과 해체

`[인쇄]` 전문:

> Optimization of the formation step in lithium-ion battery manufacturing is
> challenging due to limited physical understanding of solid-electrolyte
> interphase formation and the long testing time (∼100 days) for cells to reach
> the end of life. We propose a systematic feature-design framework that
> requires minimal domain knowledge for accurate cycle life prediction during
> formation. By only using two simple Q(V) features designed from our framework,
> extracted from formation data without any additional diagnostic cycles, we
> achieved an average of **9.87% error** for cycle life prediction. The
> physics-based investigation guided by the two designed features shows that the
> voltage ranges identified by our framework capture the effects of formation
> temperature and microscopic-particle resistance heterogeneity. By designing
> highly predictive, robust, and interpretable features, our approach can
> accelerate industrial battery formation research, leveraging the interplay
> between data-driven feature design and mechanistic understanding.

**Highlights 4줄** `[인쇄]`: ① 형성 중 cycle life 예측을 가능케 하는 체계적
feature 설계 프레임 · ② 데이터 기반 feature 설계와 기구론적 이해의 상호작용
시연 · ③ 설계 feature 가 **온도 효과와 입자 저항 불균일성**을 포착 ·
④ 프레임을 구현한 **오픈소스 소프트웨어** 제공.

`[해석]` **초록의 9.87% 는 Table 6 의 어떤 칸과도 일치하지 않는다.** Table 6
Designed 열의 5-fold MAPE 는 9.20 / 8.91 / 9.13 / 11.93 / 10.05 이고 그 산술평균은
**9.844**, 표에 인쇄된 `mean` 도 **9.84** 다. 9.87 이 어디서 나왔는지 원문이
설명하지 않는다 (셀 수 가중 평균일 가능성이 있으나 원문 미제시). 인용할 때는
**Table 6 의 9.84 를 쓰고 초록값과의 0.03 차이를 각주로 다는 것**이 안전하다.
→ §13 원문 결함 기록에 등재.

---

## §4. INTRODUCTION — 이 논문이 반응하는 선행 문제

`[인쇄]` 얼개:

- 수명 예측 접근 3계열: data-driven(⁵⁻¹³) · physics-based(¹⁴⁻¹⁸) ·
  hybrid(¹⁹⁻²⁶). 진단 기법: **DVF**(²⁷⁻³⁰) · **ICA**(³¹,³²) ·
  **EIS**(¹⁰,³³⁻³⁵) · **HPPC**(³⁶,³⁷).
- 제조 공정 중(= extreme early) 수명 예측 연구는 **공개 제조 데이터가 없어서**
  드물다.
- 형성 프로토콜이 수명을 크게 바꾼다: Weng et al.⁴⁴ 은 fast-formation 이
  baseline 대비 평균 **25% 긴** cycle life (상온·45 °C 양쪽), Cui et al.⁴⁷ 은
  형성 프로토콜만 바꿔 cycle life 가 **2배** 갈린다고 보고.
- 선행 feature: Weng et al.⁴⁴ 의 **저 SOC 저항 R_LS**. `[인쇄]` "achieving ∼8%
  error⁴⁹ (∼15% error for a dummy model)". 각주 49 가 결정적이다 —
  `[인쇄]` "**49. This small value was obtained by Weng et al.⁴⁴ having the
  cells from the same formation protocol in both their 'validation' set and
  'train/test' sets.**"
  `[해석]` **이 논문은 선행 연구의 8% 를 데이터 누출로 명시적으로 깎아내린다.**
  이 계보에서 leakage 를 각주로 못 박는 논문은 처음이다.
- R_LS 의 한계 3가지 `[인쇄]`:
  ① SoC 추정 정확도에 극도로 민감 — 두 프로토콜 간 R_LS 차이가 ~10 mΩ 인데,
  저 SoC 영역에서 SoC 4% 변화에 저항이 ~75 mΩ 움직인다 → **SoC 0.5% 오차만으로
  상관이 뭉개진다**;
  ② 그래서 형성 후 **하루짜리 저율 사이클이 추가로 필요**하다;
  ③ **같은 형성 온도의 셀에만 통한다** (Note S1).
- 그래서 요구되는 새 feature 의 조건 두 가지 `[인쇄]`: "(1) obtainable without
  additional diagnostic cycles and (2) capable of comparing formation protocols
  with **different temperatures**".

---

## §5. METHODS — 데이터셋

`[인쇄]`

- 셀: **단결정 Li[Ni₀.₅Mn₀.₃Co₀.₂]O₂ (SC-NMC532) ‖ 인조흑연(AG) 파우치셀**,
  **186개**, **62개 형성 프로토콜**(프로토콜당 3셀), 노화 프로토콜은 **동일**.
  데이터는 **Cui et al.⁴⁷ (Joule 8, 3072–3087, 2024) 이 생성**한 것.
- 그중 **178셀** 사용 — EOL 도달 + 단락·탭 파손 등 실험 실패 없는 셀.
  **EOL 정의** `[인쇄]`: "having a discharge capacity measured at 0.75 C constant
  current (CC) discharge step **below 80% of its initial value** measured at
  0.75 C CC discharge step".
- **fast-formation 프로토콜 10개** — 2단 충전의 두 C-rate 가 **모두 > 1 C**.
- 변화시킨 6개 파라미터: `CC1`, `CC2`(2단 CC 전류), `CV`(두 CC 단계 사이 컷오프
  전압), `n_ver`(첫 충전과 마지막 방전 사이 사이클 수), `T`(형성 온도),
  `t_OCV`(형성 후 휴지시간). **Latin hypercube sampling (LHS)** 로 선정.
  실제 값은 SI Table S1 에 62행 전부 인쇄 (예: 프로토콜 1 = CC1 0.0048 A,
  CC2 0.0048 A, CV 3.88 V, n_ver 0, T 40 °C, t_OCV 0 s, outer fold 1).
  T 는 25 / 35 / 40 / 45 / 55 °C 가 쓰인다.
- **공통 3단계** (Figure 1, 직접 봄): **step A** = 첫 충전, **step B** = 마지막
  방전, **step C** = 첫 방전. `[인쇄]` "Most variations among the formation
  protocols are encoded in **step A** whereas **steps B and C undergo the
  identical operating protocol at each T**."
- 측정 7종: I, V, Q, E, T, cycle index, step index. 샘플링 `[인쇄]`:
  CC 단계 **3 mV 또는 5 s** 중 빠른 쪽, CV 단계 **3 mA 또는 5 s** 중 빠른 쪽.
- 각 입력 데이터 후보는 `[인쇄, 각주 74]` "processed using interpolation at
  **p = 1,000 uniformly distributed points** along the input variable (x)".

`[해석]` step B/C 가 **모든 프로토콜에서 (온도별로) 동일 조건**이라는 사실이
이 논문 전체를 지탱한다 — 그래서 step B 의 Q(V) 차이는 프로토콜 조작의 직접
흔적이 아니라 **셀이 형성으로 도달한 상태**의 흔적이다. 우리 축으로 옮기면
"공통 진단 프로토콜(RPT)에서 잰 곡선" 과 같은 역할이다.

---

## §6. METHODS — agnostic 기준모형 (프로토콜 파라미터 → 수명)

`[인쇄]`

- 6개 형성 프로토콜 파라미터를 직접 입력으로 쓰는 ML 모형 **52개**를 만든다.
  Table 2 = 3 범주의 조합: 파라미터 집합 2종 (full 6개 / **subset** =
  `CC1, CC2, CV, T` — subset 선정 근거는 Cui et al.⁴⁷ 의 **SHAP** 분석⁷³) ×
  로그변환 출력 2종 × 알고리즘 13종 (선형 RR/EN/PLS/SPLS · 비선형 RF/SVR/XGB ·
  비선형 정량가능 ALVEN/LCEN degree 1,2,3). 2×2×13 = 52 ✓.
- 알고리즘 스위트는 **Smart Process Analytics (SPA)** 소프트웨어⁶³.
  하이퍼파라미터는 Table 1 (RR 1개 … SVR·ALVEN·LCEN 3개).
- **최고 모형 정의** `[인쇄]`: "the best model is defined as the one with the
  **smallest summation of the median and maximum mean absolute percentage error
  (MAPE) among the five outer folds** to consider both average and extrapolation
  performances."
- 최고 agnostic 모형 = subset / 로그변환 / **XGB** → median MAPE **11.06**,
  max MAPE **11.35**, median RMSE **107.10**, max RMSE **124.81**.
- **한계 2가지** `[인쇄]`: ① Cui et al. 의
  `(2단 CC 충전 – n_ver 사이클 – CC 방전 – t_OCV 휴지)` **템플릿을 벗어난
  프로토콜에는 쓸 수 없다** (6개 파라미터를 뽑을 수 없으므로);
  ② **셀-대-셀 변동을 못 잡으므로 개별 셀 품질 진단에 못 쓴다**.

`[해석]` ★ **이것이 이 논문의 방법론적 미덕 중 가장 큰 것이다.** agnostic 모형
= **프로토콜 식별자를 그대로 입력에 넣은 모형**이고, 이 논문은 그것을 숨기지
않고 **명시적 기준선(baseline)으로 세운다**. 우리가 이 계보에서 반복해 지적해
온 병("ML 입력에 프로토콜 식별자가 섞여 있는가")을 **저자들이 먼저 분리해
놓았다.** 2026-09-02 세미나의 `voltage window` 입력이 바로 이 agnostic 축에
해당하는데, 세미나는 그것을 물리 feature 와 **같은 상자에 넣고** permutation
importance 를 계산한다. Rhyu 는 두 상자를 나누고 **이긴다**. 우리가 세미나에
줄 수 있는 구체적 개선안이 여기 있다.

---

## §7. METHODS — 체계적 feature 설계 프레임워크 (핵심)

### 7.1 입력 데이터 후보 6종

§2 질문 ① 표의 단계 0 참조. 결과 6종: `Q^A(V)`, `t^A(V)`, `Q^B(V)`,
`V^B(t̃)`, `Q^C(V)`, `V^C(t̃)`.

### 7.2 입력 데이터의 "유망성" 평가 (autoML/tsfresh)

`[인쇄]`

- **tsfresh**⁷⁶ 로 시계열에서 **약 800개** feature 자동 추출. 절차:
  `tsfresh.extract_features` → **F 통계량 단변량 검정으로 p-value 사전 선별**
  (문턱 격자 17점: `10⁰, 10⁻⁰·⁵, …, 10⁻⁷·⁵, 10⁻⁸`) → 선택적으로
  `tsfresh.select_features` 추가 선별 → **elastic net** 으로 로그 cycle life 에
  회귀.
- Table 3 의 5범주: 입력형 6 × p-value 17 × 추가선별 2 × 로그출력 2 × 알고리즘
  6 (EN, RF, SVR, XGB, ALVEN, LCEN) = **2,448 모형**, 입력형당 **408 모형**.
  `[인쇄]` ALVEN/LCEN 의 degree 는 1로 고정 — "tsfresh package already contains
  various nonlinear transformations".
- **유망성 판정 규칙** `[인쇄]`: "the input data type is **not considered
  promising if none of the autoML models from the input data type outperform the
  best agnostic model in any of the four performance metrics**." (네 지표 =
  median/max × MAPE/RMSE)
- **결과**: step B·C 의 네 입력형은 MAPE 또는 RMSE 에서 최고 agnostic 을 이기고,
  **step A 의 두 입력형은 전부 진다** (Figure S4).
- **왜 step A 가 지는가** — Geslin et al.⁶¹ 을 인용해 설명. `[인쇄]` "the
  features that **encode operational variations** (e.g., features from step A)
  are **less capable of capturing cell-to-cell variability**. This limitation
  arises because the predictive power of such features heavily depends on the
  characteristics of the protocols used for training."
- 62 프로토콜이 LHS 로 설계됐으므로 5개 outer fold 는 **높은 수준의 외삽**이다.
- 이후는 **Q^B(V)** 만 쓴다 (MAPE 기준 최고). 나머지 셋의 설계 결과는 Note S9.

Figure S4 를 직접 봤다 `[도표]`: (a) MAPE 산점도에서 `Q^A(V)`(청록 원)·
`t^A(V)`(갈색 원) 구름이 median MAPE **13–17** 대역에 있고, step B/C 네 종은
**10–12.5** 대역에 뭉쳐 있다. 최고 agnostic(빨간 별)은 (11.06, 11.35),
설계 모형(파란 별)은 **(9.2, 11.9)** — **median 은 가장 좋지만 max 는 agnostic
보다 나쁘다**. (b) RMSE 판에서는 파란 별이 (97.4, 108.5) 부근으로 두 축 모두
가장 좋다.

### 7.3 fused lasso 로 β 얻기

`[인쇄]` Eq. 1:

```
min_{β∈R^p}  (1/2)‖y − Xβ‖²₂ + λ‖Dβ‖₁ ,
D = 인접 계수 차분 행렬 ∈ R^{(p−1)×p}
```

- **표준화 방식이 특이하다** `[인쇄]`: "every column in X is divided by its
  **maximum column-wise standard deviation** (i.e., max_{j=1,…,p} std(X_{:,j})).
  Unlike standardizing each column of the input data, this method **preserves
  the unique characteristic (e.g., trend of column-wise variance) of the raw
  data**." (Eq. 2 가 그 표준화된 Q̃^B_i(V_j) 의 정의)
- 이유 `[인쇄]`: "This model yields sparsity in regression-coefficient difference
  (i.e., **piecewise constant** regression coefficients) roughly in line with
  physical expectations that neighboring regression coefficients should be
  similar and only change at specific locations."

### 7.4 λ 선택 — 3제약 (Note S5, Table S2)

| 기준 | 지표 | 제약 |
|---|---|---|
| Predictiveness | 5 inner fold MAPE 평균 | **1SE rule** |
| Robustness | `max_k DTW(β^(k), mean β^(−k)) / DTW(0, mean β^(−k))` | **< 0.7** |
| Interpretability | `β^(k)` 의 path length 평균 (`Σ|a_j − a_{j+1}|`) | **< 5** |

`[인쇄, Table S2 각주]` "The constraints for robustness and interpretability
were chosen **based on trial and error** to ensure that β from any λ in the blue
region possess each characteristic."
`[인쇄]` 셋을 모두 만족하는 구간(파란 영역) 중 **가장 작은 λ** 를 쓴다 —
"β obtained from smaller λ has a higher chance of capturing index-specific
information".

fold 별 λ `[인쇄, Table S3]`: **0.3603 / 0.3925 / 0.6788 / 0.3631 / 0.5510**.

Figure S5 를 직접 봤다 `[도표]` — 이 흡수에서 가장 중요한 그림 판독이다:
- (a) MAPE vs λ: inner fold 2개(주황·초록)가 작은 λ 에서 **40–60** 까지 치솟는다
  (과적합). 나머지 3개는 평평.
- (e) **λ = 0.3603 에서 5개 inner fold 의 β 를 겹쳐 그린 판**. 3.0–3.4 V 와
  3.7–4.3 V 에서는 다섯 곡선이 잘 겹친다. 그런데 **설계 feature 가 사는 바로
  그 구간 (≈ 3.45–3.60 V) 에서 다섯이 크게 갈리고 부호까지 뒤집힌다**:
  3.48 V 부근에서 β^(2)(청) ≈ **−0.70**, β^(1)(자) ≈ −0.15, β^(5)(적) ≈ **+0.37**
  (근사 판독). 4.37 V 의 큰 점프(+0.5 ~ +1.07)도 fold 마다 크기가 두 배 이상
  다르다.
- `[해석]` **"robustness" 를 DTW 형상 비율로 정의하면 통과하지만, 계수의
  국소 부호는 fold 간에 안정하지 않다.** 그런데 설계 feature 는 바로 그 국소
  구간의 차분이다. 이것은 §2 질문 ② 에서 본 nullspace 경고(참고문헌 [13])가
  **실제로 이 데이터에서 발현되고 있다**는 시각적 증거로 읽힌다. 논문은 이
  그림을 "robustness" 의 증거로 제시한다 (`[인쇄]` "even β from the smallest λ
  possesses high robustness (Figure S5e)").

### 7.5 β 로 구간 분할

`[인쇄]` 점프 판정: `|β_{j+1} − β_j| ≥ 0.001 × (max β − min β)`.
outer fold 1 에서 **19개 경계** (Figure 3A 에 A–S 로 라벨).

### 7.6 feature 형태의 유도 (Eq. 3–5)

§2 질문 ① 에 요약. 결론 `[인쇄]`: 구간마다 **차분** `Q^B_i(V₂) − Q^B_i(V₁)` 과
**평균** `mean(Q^B_i(V₁–V₂))` 두 개면 충분. y절편 대표값으로 평균을 쓰는
이유 `[인쇄]`: "given that β is generally flat in each section".

### 7.7 구간 병합 (Algorithm S1, Note S6)

`[인쇄]` 경계 하나를 뺐을 때의 5 inner fold 평균 RMSE 가 `th_merge = 0.01`
이하이면 제거하고 반복. 로그 출력이므로 `exp(0.01) ≈ 1%` 오차에 해당.
`[인쇄]` outer fold 1 에서 경계 **L** 은 제거됐고, **"neither boundaries J nor K
can be removed although they seem to be very close to each other"** →
"Algorithm S1 is actually **sensitive to the information encoded in specific
voltage ranges**".

### 7.8 feature 하향선별 (Algorithm S2, Note S7)

`[인쇄]` y 와의 Pearson 상관이 가장 큰 feature 를 뽑고, 그것과 상관 >
`th_PC,X = 0.2` 인 feature 들을 제거 — y 와의 상관이 `th_PC,y = 0.4` 를 넘는
feature 가 남지 않을 때까지 반복. 목적은 **multicollinearity 회피**(⁸⁷⁻⁸⁹).

### 7.9 결과 — 설계된 두 feature (Table 4)

| Outer fold | 설계 feature 1 | 설계 feature 2 |
|---|---|---|
| 1 | Q^B(3.57 V) − Q^B(3.60 V) | Q^B(3.60 V) − Q^B(3.66 V) |
| 2 | Q^B(3.58 V) − Q^B(3.61 V) | Q^B(3.61 V) − Q^B(3.64 V) |
| 3 | Q^B(3.57 V) − Q^B(3.61 V) | Q^B(3.61 V) − Q^B(3.64 V) |
| 4 | Q^B(3.58 V) − Q^B(3.60 V) | Q^B(3.60 V) − Q^B(3.67 V) |
| 5 | Q^B(3.57 V) − Q^B(3.60 V) | Q^B(3.60 V) − Q^B(3.64 V) |

`[인쇄]` "Consistency on the designed features among the outer loop (i.e., Q^B(V)
differences between ∼3.57, ∼3.60, and ∼3.66 V) indicates the robustness of the
feature design framework, which is remarkable given the high level of
extrapolation at each outer fold".

`[인쇄]` 세 전압값이 `d²Q^B/dV²` 곡선의 **peak 과 valley** 위치와 일치한다:
"The selected voltage values match with the index for the peak and valley of
d²Q^B/dV²(V) curve in Figure 3D, implying that the designed features capture
some physical meaning."

Figure 3 을 직접 봤다 `[도표]`:
- (A) 학습셋 전 셀의 표준화 Q̃^B(V) 가 수명으로 색칠돼 있고 검은 계단이 β 다
  (오른쪽 축 −1~+1). β 는 3.0–3.25 에서 ≈ +0.15 → −0.25, 3.45–3.55 에서 ≈ −0.5
  까지 내려갔다가 3.57–3.60 에서 ≈ +0.45 로 튀고, **4.37 V 에서 +0.87 로 가장
  크게 점프**한다. 그 4.37 V 경계(S)는 최종 feature 에 **쓰이지 않는다**.
- (B) Q^B(V) 자체는 매끈한 단조 감소 곡선이고 색(수명)에 따른 분리가 육안으로는
  거의 안 보인다.
- (C) dQ^B/dV 는 3.6 V 부근에 −0.55 ×10⁻³ 정도의 최소.
- (D) **d²Q^B/dV² 의 개별 셀 곡선은 ±2×10⁻⁵ 범위에서 완전히 노이즈다.**
  peak/valley 를 알아볼 수 있는 것은 **굵은 검은 선(열 평균)** 뿐이다.
- `[해석]` 따라서 "설계 전압이 d²Q/dV² 극값과 일치한다" 는 주장은 **셀 개별
  곡선이 아니라 앙상블 평균 곡선**에 대한 것이다. 물리적 의미 주장의 무게는
  그만큼 줄어든다. 원문은 이 구분을 명시하지 않는다 (Fig. 3D 캡션이 "the thick
  black solid line in (D) is for the column-wise average" 라고만 적는다).

---

## §8. RESULTS — 세 접근의 성능 비교

**Table 5** `[인쇄]` 최고 모형 3종:

| 모형 | feature 수 | 구성 | 한계 |
|---|---|---|---|
| Agnostic (best) | **4** | subset(CC1,CC2,CV,T) / 로그 / **XGB** | 특정 템플릿에만 적용 가능 · 셀-대-셀 변동 없음 |
| AutoML (best) | **155** | Q^B(V) / 10⁻⁴·⁵ / yes / yes / **SVR** | **해석 가능성 거의 0** |
| Designed (best) | **2** | Table 4 의 feature + **RF** | – |

**Table 6** `[인쇄]` (별표 = 각 행 최소):

| | Agnostic | AutoML | Designed |
|---|---|---|---|
| MAPE fold 1 | 10.55 | 10.21 | **9.20\*** |
| MAPE fold 2 | 11.06 | **8.14\*** | 8.91 |
| MAPE fold 3 | 11.14 | 10.85 | **9.13\*** |
| MAPE fold 4 | 11.35 | **9.72\*** | 11.93 |
| MAPE fold 5 | 10.70 | **9.63\*** | 10.05 |
| MAPE mean | 10.96 | **9.71\*** | 9.84 |
| MAPE HL | 10.95 | 9.72 | **9.59\*** |
| RMSE fold 1 | 108.79 | 120.44 | **98.98\*** |
| RMSE fold 2 | 90.98 | **74.79\*** | 88.51 |
| RMSE fold 3 | 124.81 | 136.92 | **97.33\*** |
| RMSE fold 4 | 107.10 | **86.17\*** | 108.54 |
| RMSE fold 5 | 100.82 | **83.14\*** | 95.90 |
| RMSE mean | 106.50 | 100.29 | **97.85\*** |
| RMSE HL | 107.10 | 101.79 | **97.44\*** |

(HL = Hodges-Lehmann 추정량 = 쌍평균의 중앙값⁹⁰,⁹¹)

`[인쇄]` 요약: "the best designed model that uses only two features (blue star)
has a performance **comparable to** the best autoML model (black cross), while
**outperforming** the best agnostic model (red star) for mean, HL, and median
metrics."

`[인쇄]` 예측오차의 맥락 2가지: (1) 형성 단계 측정만 쓴다, (2) LHS 설계라 각
outer fold 가 **강한 외삽**이다. 그리고 `[인쇄]` "the **best achievable
prediction error based on cell-to-cell variation is ∼6% MAPE**" (Note S10).

Figure 4 를 직접 봤다 `[도표]`:
- (A) 네 판(mean/HL/median/max × MAPE-RMSE). 회색 × 는 autoML-Q^B(V) 수백 개
  구름. mean 판에서 파란 별(designed) ≈ (9.85, 98), 검은 × (autoML) ≈ (9.7, 100),
  빨간 별(agnostic) ≈ (11.0, 106.5). **max 판에서는 순서가 뒤집힌다** —
  파란 별 ≈ (12.0, 110), 빨간 별 ≈ (11.4, 125), 검은 × ≈ (10.9, 135).
- (B) 프로토콜별 실제 vs 예측 (파랑 = fast formation, 빨강 = 55 °C, 검정 = 기타).
  agnostic 판은 수명 800 이상 구간(대부분 fast/55 °C)에서 크게 어긋난다.
  autoML·designed 판의 inset 히스토그램에 250 사이클 점선.

`[인쇄]` 오차 사례: 최고 autoML 은 **fast-formation 프로토콜 2개에서 >250 사이클**
오차(가장 긴 수명 프로토콜에서 **∼350 사이클**) → "it can be **risky to rely on
autoML models** to evaluate fast-formation protocols". 최고 designed 는
프로토콜 34(평균 수명 ∼1,000, fast 도 고온도 아님)에서 ∼250 사이클 오차이나
autoML 도 같은 프로토콜에서 ∼200 → "likely due to the limitation of using only
Q^B(V) data".

`[인쇄]` 성능의 귀속: "The features generated from the autoML approach typically
use either the entire dataset or subset of the dataset that is chosen based on
**simple statistics** (e.g., percentile or arbitrarily chosen thresholds). On
the other hand, the features designed from our framework use the subset that is
determined by **considering the relationship between the input data and the
output**".

`[해석]` **비판 하나**: 저자들이 정의한 "최고 모형" 기준(median + max MAPE 합)을
세 접근에 그대로 적용하면 agnostic 22.41, **autoML 20.57**, **designed 21.13**
이다 — 즉 **자기 기준으로는 autoML 이 이긴다**. 논문은 이 기준을 각 접근
**안에서** 최고를 고르는 데만 쓰고, 접근 **간** 비교는 mean/HL/median 으로
한다. 잘못은 아니지만, 초록의 "9.87%" 만 인용하면 **designed 의 최악 fold
(11.93)가 세 접근 중 가장 나쁘다**는 사실이 사라진다.

---

## §9. RESULTS — 설계 feature 의 물리적 의미

`[인쇄]` 논증의 구조 (Figure 5, 직접 봄):
- **빨강 화살표 (도메인 지식)**: 형성 온도 + 미시 입자 저항 불균일성 → SEI
  품질 → cycle life.
- **파랑 화살표 (feature 설계 결과)**: dQ^B/dV·d²Q^B/dV² → 두 설계 feature →
  cycle life.
- **초록 점선 (빠진 고리, 이 절이 채우려는 것)**: 미시 입자 저항 불균일성 →
  dQ^B/dV·d²Q^B/dV².

`[인쇄]` 정직한 부정문 하나: "the designed features **do not directly correspond
to features in the dataset's average discharge capacity or differential
capacitance curves**, which have been widely used in previous studies as
indicators of lifetime.⁶,⁹²⁻⁹⁴ However, the voltage windows identified from our
framework show a **strong overlap with local maxima and minima in the dataset's
average second derivative of capacity (d²Q/dV²)** data, particularly in the
range of **3.4–3.7 V**".

**느린 형성 부분집합** `[인쇄]`: `CC1 < 0.05 C` 인 **32셀 / 178셀**. 이유 —
"long cycle life performance is physically tied to the formation of a stable SEI
layer under these slow operating conditions. Furthermore, these stable SEI
layers can be viewed as a **fixed amount of lithium loss**, which makes it
easier to investigate by removing the degrees of freedom derived from the
electrode-utilization shift."
`[해석]` **저자들이 자유도를 줄이려고 부분집합을 고른다** — 우리 언어로는
"모드 자유도를 하나 고정하고 나머지를 본다" 이다. 식별 가능성 어휘를 안 쓰면서
식별 가능성 전략을 쓰고 있다.

`[인쇄]` SEI 성장의 두 체제(reaction-limited → diffusion-limited)⁹²·이층
모형⁹⁹,¹⁰¹⁻¹⁰³ 및 최근 증거⁵⁷,⁹³,⁹⁴,¹⁰⁴⁻¹⁰⁶ 을 근거로, 느린 형성에서는
1차 SEI 가 잘 형성되고 "**the total lithium consumed by SEI production is
similar across formation protocols**".

**핵심 관측** `[인쇄]`: 형성 후 C/20 RPT (Fig. S12) 에서 미분용량과 d²Q/dV²
신호가 **거의 구별되지 않는다** → 이용상태·잔여 리튬 재고가 비슷하다는 뜻.
**그런데 cycle life 는 같지 않다.** 특히 **55 °C 형성 셀이 유의하게 좋다**.
반면 형성 데이터 자체(step B) 의 dQ/dV·d²Q/dV² 는 `[인쇄]` "little variation
within cells formed at the same temperature but **large variations across
different formation temperatures**" 이고, 온도가 낮아지면 두 곡선이 **매끄러워
진다**.

**대리 모형 (reactive particle ensemble / distributed resistance)** `[인쇄]`:
- 각 전극을 반응성 입자 앙상블로 근사, 입자마다 rate constant `k₀` 를 분포에서
  뽑는다. 전하전달 저항 `R_CT = k_B T / (e k₀)`.
- Eq. 6 = **ICET**(ion-coupled electron transfer, Bazant 2023¹⁰⁷) 속도식:
  과전압에 대해 대칭 Butler-Volmer, **충전율(filling fraction)에 대해 비대칭**
  (X선 나노입자 영상 학습으로 확인됨¹⁰⁸), 전지수에 **Arrhenius 온도 의존성**
  (활성화 장벽 `E_A`).
- 자유 파라미터 **5개**: `E_A`, `k̄₀,c`, `k̄₀,a`, `σ_c`, `σ_a` (전극별 log-Gaussian).
  값 `[인쇄, Fig. 6 캡션]`: **E_A = 45 kJ/mol, k̄₀,c = 5×10⁻⁷ A/m²s,
  k̄₀,a = 10⁻⁷ A/m²s, σ_c = 1, σ_a = 0.5** (298 K 기준).
- `[인쇄]` 비교 결과: "we see **striking similarities in the location of the
  local maxima and minima** in the d²Q/dV² and their trends with temperature."

Figure 6 을 직접 봤다 `[도표]`: (A,B) 실험 (C,D) 시뮬레이션, 가로축 3.3–3.7 V.
(A) 실측 dQ^B/dV 는 저온(청) 쪽이 매끄럽고 고온(자홍) 쪽이 3.5–3.65 V 에서
구조가 뚜렷하다. (C) 시뮬레이션도 같은 경향. (B)/(D) d²Q/dV² 는 실측이 ±30,
시뮬이 ±60 스케일로 **세로 스케일이 2배 다르다** — 형태는 닮았으나 진폭은
맞지 않는다. (E,F) 시뮬레이션된 입자 R_CT 분포 (log 가로축 10²–10⁶ Ω m²):
온도가 오를수록(청→자홍) 분포가 **왼쪽(낮은 저항)으로 이동**하고 양극(E)은
폭이 넓고(σ_c = 1) 음극(F)은 좁다(σ_a = 0.5).

`[인쇄]` 최종 가설: "we **hypothesize** that the designed model performs better
than the agnostic model because designed features not only encode some of the
agnostic-model parameters, such as **formation temperature**, but also encode an
**underlying heterogeneity in the microscopic-particle resistances** which
varies from cell to cell and translates into the electrochemical signatures
during formation."

`[해석]` 이 절의 논증 등급은 **시각적 유사성**이다. 정량 지표가 하나도 없고
(§1-3), 5개 자유 파라미터의 적합 절차도 없다. 저자들이 "theorize"/"hypothesize"
로 표현을 낮춘 것은 정직하지만, Highlights 3번("설계 feature 가 온도 효과와
입자 저항 불균일성을 포착")은 그보다 강한 어조다.

---

## §10. Conclusions

`[인쇄]` 요지:
- 커뮤니티의 오랜 질문 "how much data are needed to predict cycle life?" 에
  대해, 노화 구간이 아니라 **형성 데이터만으로** 답한다.
- 최소한의 도메인 지식·사용자 입력으로 두 개의 단순 Q(V) feature 를 **마지막
  방전 단계(step B)** 에서 설계한다. 추가 진단 사이클 불필요, 온도가 다른
  프로토콜 간 비교 가능.
- 예측력의 귀속: 형성 온도 + 미시 입자 저항 불균일성이 dQ/dV·d²Q/dV² 에 남기는
  흔적.
- **일반화 주장** `[인쇄]`: "Not being tailored to any specific settings listed
  above, our framework is expected to design predictive features customized to
  each application." 그리고 같은 프레임을 **동일 프로토콜 셀들의 제조 이상치
  탐지**에도 쓸 수 있다.

---

## §11. ★ RESOURCE AVAILABILITY — 데이터·코드 (요청 항목)

`Data and code availability` 절 **전문** `[인쇄, 본문 p.11]`:

> The raw data used in this work, generated by Cui et al.,⁴⁷ can be found at
> **https://data.matr.io/8/**. The code and processed data used in this work
> have been deposited at **Zenodo at https://doi.org/10.5281/zenodo.14916092**
> and are publicly available as of the date of publication.

`Lead contact` `[인쇄]`: "Requests for further information and resources should
be directed to and will be fulfilled by the lead contact, Richard D. Braatz
(braatz@mit.edu)." · `Materials availability` `[인쇄]`: "This study did not
generate new materials."

### zip 파일별 내용 — **원문 미제시**

전수 확인했다: 문자열 `zip` 이 본문 15쪽 + SI 19쪽 통틀어 **0회**.
`Systematic_Feature_Design_Framework_Formation_main`·
`Features_tsfresh_autoML_fulllist`·`fulllist` 도 **각 0회**. `GitHub`·
`repository` 도 0회. 즉:

| 사용자가 받는 파일 | 원문 근거 |
|---|---|
| `Systematic_Feature_Design_Framework_Formation_main.zip` (14.3 MB) | **원문 미제시** — 파일 이름이 논문에 없다 |
| `Features_tsfresh_autoML_fulllist.zip` (9.8 MB) | **원문 미제시** — 파일 이름이 논문에 없다 |

원문이 말하는 것은 **두 저장소의 역할 구분**뿐이다:
- **data.matr.io/8/** = **원시 데이터**, 그리고 그것은 이 논문이 만든 것이
  아니라 **Cui et al. 2024 이 생성**한 것.
- **Zenodo 10.5281/zenodo.14916092** = **코드 + 가공 데이터**.

`[해석]` 파일 이름의 어의(`..._Framework_Formation_main` / `Features_tsfresh_
autoML_fulllist`)와 논문 구조를 대조하면 각각 "프레임워크 구현 코드 + 주
분석" 과 "§7.2 의 tsfresh autoML feature 전체 목록" 으로 **보이지만**, 이것은
**추측이며 원문 근거가 아니다.** 확인하려면 zip 안의 README 를 봐야 하고,
그 확인 결과는 위키에 적을 때 **논문 인용이 아니라 데이터셋 관찰**로 등급을
매겨야 한다. (참고: 위 표의 파일 크기 14.3 MB / 9.8 MB 도 원문에 없다 —
사용자가 포털에서 본 값이다.)

---

## §12. SI 해체 (Note S1 – S11)

### Note S1 — Cui 데이터셋에서 R_LS 의 성능 (Fig. S1)

`[인쇄]` Weng et al. 의 HPPC 는 SoC 4%마다 펄스, Cui et al. 의 HPPC 는 **SoC
20%마다** 펄스 → 보간으로 저항을 추정하면 부정확하므로 **실제 측정된 SoC
값으로 묶어서** 산점도를 그렸다. SoC 정의 `[인쇄, Eq. S1]`:
`SoC = (Q_ch,last pulse − Q_dis,last pulse) / Q_ch,CCCV × 100%`.

`[인쇄]` 결론: "the negative correlation between R_LS and the cycle life
**does not appear** for the dataset in Cui et al. in SoC values spanning from 5%
to 11%. ... This can be explained by (1) **R_LS cannot be used for comparing
formation protocols with different formation temperatures** or (2) much more
careful SoC measurement is required, where either limits using R_LS for
optimizing formation."

Fig. S1 을 직접 봤다 `[도표]` — 9개 패널의 제목에 ρ 가 인쇄돼 있다:
(a) 4.75–5.25% SoC **ρ = −0.11** (점 3개) · (b) 6.75–7.25% **ρ = +0.01** (5개) ·
(c) 7.75–8.25% **ρ = −0.43** · (d) 8.75–9.25% **ρ = −0.16** (∼20개) ·
(e) 9.75–10.25% **ρ = −0.46** (∼20개) · (f) 10.75–11.25% **ρ = −0.38** ·
(g) 8.9–9.1% **ρ = +0.12** (6개) · (h) 9.9–10.1% **ρ = −0.40** (7개) ·
(i) 11–11.2% **ρ = −0.45** (7개). 색은 형성 온도(25/35/40/45/55 °C).
`[해석]` 표본이 패널당 3–20개로 매우 작다. 결론 자체는 그럴듯하지만
**근거의 통계적 무게는 약하다** — 원문은 표본 크기를 논하지 않는다.

### Note S2 — 데이터 심문 (Fig. S2)

`[인쇄]` 6개 프로토콜 파라미터 vs cycle life 에 대해: Pearson 선형상관 vs
**ACE(alternating conditional expectations)** 최대상관 비교 → "The maximal
correlation coefficients are **∼2- to ∼7-fold larger** than the linear
correlation coefficients for the last four parameters, CV, n_ver, T, and t_OCV"
→ 비선형 관계 존재. 이차항 검정 → "the cycle life might be related to **T²**".
쌍선형 검정 → "**CC1 × T and CC2 × T** might be related to the cycle life".
**VIF** ≈ 1 → "the multicollinearity is negligible, which is **due to the Latin
Hypercube Sampling**".

`[해석]` LHS 설계 덕에 **입력 파라미터들끼리는** 공선성이 없다. 이 논문의
공선성 논의는 전부 **입력 공간** 얘기이고, **출력(모드/수명) 쪽의 식별
가능성**은 다루지 않는다 — 우리 문제와 정확히 갈라지는 지점.

### Note S3 — 중첩 교차검증 (Fig. S3, Table S1)

`[인쇄]` 프로토콜 라벨링은 CC1 → CC2 → CV → n_ver → T → t_OCV 오름차순.
NumPy 로 셔플 후 5그룹(outer). agnostic·autoML 은 inner 10-fold **grouped** CV
(하이퍼파라미터), designed 는 먼저 **inner 5-fold grouped CV 로 feature 설계**
(주황 루프) 후 하이퍼파라미터 루프(파랑). `[인쇄]` "The split in the orange
inner loop was **intentionally differentiated from** the split in the blue inner
loop **to avoid information leakage**." 그리고 공정 비교를 위해 outer/blue-inner
분할은 모든 모형에서 동일.

Fig. S3 를 직접 봤다 `[도표]`: 62 프로토콜 → outer 5분할 → outer fold 1 의
training set 이 두 갈래로 (agnostic/autoML 용 파란 10-fold, designed 용 주황
5-fold). **group 단위는 프로토콜**이므로 같은 프로토콜의 형제 셀 3개가 절대
갈라지지 않는다.

`[해석]` ★ **이 계보에서 검증 설계가 가장 엄격한 논문이다.** (i) group =
프로토콜, (ii) feature 설계가 outer training set **안에서** 일어난다,
(iii) feature 설계용 분할과 하이퍼파라미터용 분할을 **일부러 다르게** 잡는다,
(iv) 선행 연구의 leakage 를 각주로 지적한다(각주 49). 2026-09-02 세미나의
LOGO-CV group 정의가 원문에 인쇄되지 않은 것과 대비된다.

### Note S4 — 입력 데이터 유망성 (Fig. S4)

§7.2 에 통합.

### Note S5 — λ 결정 (Table S2, Fig. S5)

§7.4 에 통합.

### Note S6 — 구간 병합 (Algorithm S1, Fig. S6)

§7.7 에 통합. `[인쇄]` 추가: 경계 **I** 도 두 번째로 작은 RMSE 라 제거 가능
("boundaries H and I are close to each other").

### Note S7 — feature 하향선별 (Algorithm S2)

§7.8 에 통합. 의사코드 그대로: 상관행렬 `R` 에서 y 열의 최대값 인덱스를 뽑고,
그 feature 와 상관 > 0.2 인 행/열을 제거, y 상관 > 0.4 가 없어질 때까지 반복.

### Note S8 — 다른 fold 의 분할 결과 (Table S3, Fig. S7)

`[인쇄]` fold 별 λ 와 **최종 경계 전압 목록**. 예 outer fold 1:
`3.00 3.10 3.25 3.37 3.42 3.43 3.48 3.50 3.53 3.56 **3.57 3.60 3.66** 3.74 3.83
4.11 4.22 4.36 4.40` (굵게 = 설계 feature 에 쓰인 값). fold 3 은 경계가 16개로
가장 적고 λ 가 0.6788 로 가장 크다. (Fig. S7 은 미열람 — §15 참조)

### Note S9 — 다른 입력 데이터형의 설계 결과 (Fig. S8–S10, Table S4–S6)

`[인쇄]`

| 입력형 | fold 1 | fold 2 | fold 3 | fold 4 | fold 5 |
|---|---|---|---|---|---|
| `V^B(t̃)` (Table S4) | **없음** (blue region 자체가 없음) | V^B(0.93)−V^B(0.95) | V^B(0.93)−V^B(0.95); mean V^B(0.37–0.46) | mean V^B(0.97–1); V^B(0.55)−V^B(0.65) | V^B(0.91)−V^B(0.94) |
| `Q^C(V)` (Table S5) | Q^C(3.37)−Q^C(3.41) | Q^C(3.00)−Q^C(3.11); mean Q^C(3.11–3.41) | Q^C(3.52)−Q^C(3.62) | Q^C(3.58)−Q^C(3.63) | Q^C(3.00)−Q^C(3.15); mean Q^C(3.43–3.48) |
| `V^C(t̃)` (Table S6) | mean V^C(0.99–1) | mean V^C(0.97–1) | V^C(0.99)−V^C(1) | mean V^C(0.99–1) | mean V^C(0.93–0.95) |

`[해석]` ★ **Q^B(V) 의 fold 간 일관성(≈3.57/3.60/3.64–3.67 V)은 다른 세
입력형에서 재현되지 않는다.** `Q^C(V)` 는 fold 마다 완전히 다른 전압대(3.00–3.15
vs 3.37–3.41 vs 3.52–3.62)를 고르고, `V^B(t̃)` 는 fold 1 에서 **아무 λ 도
제약을 통과하지 못해 feature 가 없다**. 즉 "프레임워크가 강건하다" 는 주장은
**Q^B(V) 라는 한 입력형에서만** 성립한다. 원문은 이 대조를 하지 않는다.
그리고 §1-5 대로 **이 셋의 예측 성능이 인쇄되지 않아** Q^B(V) 선택이 사후적
정당화인지 확인할 수 없다.

### Note S10 — 달성 가능한 최소 예측 오차 (Table S7)

`[인쇄]` 프로토콜 k 의 수명이 `N(μ_k, σ_k)` 를 따른다고 가정하면 최적 예측은
μ_k 이고 `E[APE] ≈ 100 √(2/π) σ_k/μ_k` (Eq. S2), 전체 `E[MAPE]` 는 셀 수
가중 평균 (Eq. S3). Table S7 의 μ_k, σ_k (n_k = 2 또는 3) 를 넣으면 **∼6% MAPE**.

Table S7 발췌 `[인쇄]`: 프로토콜 2 → n=3, μ=1137, σ=37.75 · 프로토콜 10 →
n=3, μ=1077, **σ=172.22**(최대급) · 프로토콜 32 → n=2, μ=648.50, **σ=2.12**
(최소) · 프로토콜 48 → n=3, μ=855, σ=6.08 · 프로토콜 59 → n=3, μ=1172.67,
σ=139.66. 수명 범위는 대략 **513 ~ 1173 사이클**.

`[해석]` σ_k 를 표본 2~3개로 추정한다 (§1-6). σ 가 2.12 에서 172.22 까지
80배 벌어지는 것은 실제 재현성 차이일 수도, 표본 부족의 산물일 수도 있다 —
구분 불가. 따라서 "6% 가 하한" 은 **부드러운 주장**으로 다뤄야 한다.

### Note S11 — 물리 모형 (Fig. S11–S12, Table S8–S9, Eq. S4–S12)

**(a) OCV 표현** `[인쇄]`: 반쪽셀 **C/20** 측정에서 얻은 OCV 를 chemical
potential 로 쓴다 (`V_OCV = −eμ` 가정, 기준전극이 kinetic 제한이 아니라고 가정).
Zhao et al.^{S7,S8} 을 따라 **엔트로피 항(격자 모형) + 엔탈피 항(Legendre 다항식
전개)** 로 분해 (Eq. S4):
`V_OCV(c) = −(k_B T_ref/e) ln(c/(1−c)) + Σ_{i=0}^N a_n P_n(2c−1)`.
계수는 선형회귀로 학습, Table S8 에 인쇄 (양극 NMC532 a₀…a₁₉ = 3.9441, −0.4024,
0.1444, −0.0516, −0.0735, … ; 음극 AG a₀…a₂₄ = 0.1177, −0.0352, 0.0801,
−0.0664, 0.0713, …).

Fig. S11 을 직접 봤다 `[도표]`: (a) 양극 4.6→2.9 V, (b) 음극 1.0→0 V,
실험(파랑 실선)과 시뮬(주황 파선)이 **거의 완전히 겹친다** — OCV 적합 자체는
훌륭하다.

**(b) 전극 이용상태 모형** `[인쇄]`: 수송·속도 제한이 없는 극한. 4 파라미터
(β_c, β_a, Q_rem, V_shift). Eq. S5–S6:
`I/Q_c,total = −(Q_a,total/Q_c,total) β_a ∂c̄_a/∂t = β_c ∂c̄_c/∂t`,
`V_cell = −(1/e)(μ_c(c̄_c) − μ_a(c̄_a)) − V_shift`.
`[인쇄]` "The ratio Q_a,total/Q_c,total in this model is equivalent to the
**N/P ratio** of the battery, which is known to be **1.16** for the cells
investigated in this work.^{S1}"
결과 Table S9: **β_c = 0.911, β_a = 0.854, Q_rem/Q_c,total = 0.930,
V_shift = 0.014 V** (느린 형성 셀 평균).
`[인쇄]` 한계 자인: "the electrode utilization captures the broad features of
the experimental dataset, but **still fails to fit the differential capacitance
versus voltage curve perfectly**. This is likely due to the failure of the
assumption that the process timescale is large enough to neglect the reaction
and transport limitations".

Fig. S12 를 직접 봤다 `[도표]`: (a,b) 실측 — 25~55 °C 색이 **거의 완전히
겹친다** (dQ/dV 최저 ≈ −2.5 [1/V] @ ∼3.63 V; d²Q/dV² 는 ±40 스케일로 3.4–3.65 V
에 뾰족한 구조). (c,d) 유틸리제이션 모형(검정) vs 실험(연보라): **3.5–3.55 V
에서 눈에 띄게 어긋난다** — 시뮬은 ∼3.52 V 에 뚜렷한 봉우리를 만드는데 실험은
더 완만하고, 3.63 V 부근에서 시뮬의 골이 실험보다 훨씬 깊다(축을 벗어난다).
본문의 "fails to fit ... perfectly" 서술과 **그림이 일치**한다.

**(c) 반응입자 앙상블 모형** `[인쇄]`: 전극당 `N_particles` 개의 반응 표면,
입자마다 `k₀` 만 다르다 (`ln k₀^(i) ∼ N(ln k̄₀,j, σ_j)`, Eq. S12).
Eq. S7–S9 (입자별 진화식·ICET 속도식·과전압), Eq. S10 (미시↔거시 연결),
Eq. S11 (전극 SoC = 입자 평균). `R_ct^(i) = k_B T/(e k₀^(i))`.
`[인쇄]` "One way to conceptualize this model is as a **resistance distribution
model**, but where non-linear dynamics are considered solely from the reaction
kinetics."
수치 구현 `[인쇄]`: **forward-Euler**, **C/5 전류 구속**. 스케일 인자
`(ν_a a_V,a)/(e c_ref,c ν_c) = 1`, `a_V,c/(e c_ref,c) = 1` 로 놓음 —
`[인쇄]` "Though this is **likely not true**, they are likely to be of the same
order of magnitude".
초기화 `[인쇄]`: step B 시작 셀전압이 항상 **4.4 V** 이므로 전극별 SoC·전위를
정할 수 있다. 그리고 결정적 자인 —
`[인쇄]` "We assume that **all battery particles start at the same SoC** at the
start. **This is likely a poor assumption** given that the dataset in Step B is
not taken after a voltage or OCV hold where the system is given time to
equilibrate. As we can **neither quantify nor verify the particle SoC
distribution** from the experimental dataset, we leave those investigations for
future works."

`[해석]` 이 자인은 우리 축에서 크다: **입자 SoC 분포는 실험에서 확인 불가능하고,
그런데 저자들의 결론은 "설계 feature 가 저항 불균일성을 읽는다" 이다.**
즉 결론의 대상이 원리적으로 관측되지 않는 양이다. 저자들은 이 긴장을 정직하게
적어 두지만 해소하지 않는다.

---

## §13. 원문 결함·불일치 기록

1. **초록 9.87% vs Table 6 mean 9.84** — 계산 근거 미제시 (§3).
2. **SI Fig. S12 캡션의 표 상호참조 오류** `[인쇄]`: "Designed voltage features
   in **Table 6** are shown as vertical lines". Table 6 은 MAPE/RMSE 표이고,
   설계 feature 는 **Table 4**(본문) / Table S3(SI) 다.
3. **Table 6 각주 a/b/c/d 가 표와 어긋나 보인다** — 각주 a("Weng et al. 이
   같은 프로토콜 셀을 validation 과 train/test 양쪽에 두어 얻은 작은 값"),
   b("하이퍼파라미터 최적화와 성능 평가에 같은 데이터셋"), c("p = 1,000 균등
   보간") 는 각각 본문 참고문헌 49·62·74 의 내용이며 Table 6 본체에 대응하는
   위첨자가 없다. 조판 과정에서 각주가 표에 잘못 붙은 것으로 보인다.
   (d 는 HL 추정량 설명으로 표와 맞다.)
4. **`robustness` 라는 단어가 두 뜻으로 쓰인다** — (i) β 형상의 fold 간 DTW
   일관성(Table S2), (ii) HL 추정량의 통계적 강건성(각주 91). 혼동 소지.
5. **Fig. S4 에 "Designed (best)" 파란 별이 함께 그려져 있다** — 그 그림의
   제목은 "Promisingness of **each input data**" 이고 나머지는 전부 autoML
   모형인데, 설계 모형 하나만 다른 범주로 섞여 있다 `[도표]`. 오해를 부르기
   쉬운 배치다 (본문은 Fig. S4 를 입력형 비교로만 서술한다).

---

## §14. 우리 프로젝트와의 접점 (degradation-degeneracy / mode-observability)

`[해석]` 이 절은 전부 우리 판단이다. 우리 연구 수치는 여기 복사하지 않는다 —
정본은 artifact + `degradation-degeneracy/docs/RESULTS*.md`.

### 14.1 가져올 수 있는 것 (3개)

1. **★ agnostic 기준선 패턴** (§6). "프로토콜 파라미터만으로 target 을 얼마나
   맞히는가" 를 **먼저 세우고**, 물리 feature 모형이 그것을 이기는지로 판정한다.
   2026-09-02 세미나는 `voltage window`(프로토콜 식별자)를 물리 feature 와
   같은 상자에 넣고 permutation importance 를 계산하는데, Rhyu 방식이면 두
   상자를 분리해 **"물리 feature 가 프로토콜 식별자를 넘어서는가"** 를 직접
   물을 수 있다. `[[pvs-sev-lli-lampe-separability]]` 의 Evidence For 2번
   항목(“LAM_PE 분리가 SOH+window 로 설명될 여지”)을 **판정 가능한 실험**으로
   바꾸는 설계다.
2. **feature 설계를 학습 fold 안에 가두는 중첩 CV** (§12 Note S3). 특히
   feature 설계용 inner 분할과 하이퍼파라미터용 inner 분할을 **일부러 다르게**
   잡는 수법. 우리가 라벨 degeneracy 전파를 볼 때도 같은 규율이 필요하다.
3. **fused lasso β → 구간분할 → 차분·평균 두 항** 이라는 기계장치 (§7.3–7.6).
   우리 목적함수의 **전압창 가중**을 정하는 데 이식 가능하다. 단 y 를 cycle
   life 가 아니라 **모드 파라미터**로 바꿔야 하고 (질문 ③), 그러면 β 는 회귀
   계수가 아니라 **감도(Jacobian 행)** 의 정규화된 추정이 된다 — 이 치환이
   맞는지는 우리가 확인해야 한다.

### 14.2 우리가 이 논문에 공급할 수 있는 것 (3개)

1. **★ Table S9 의 4-파라미터 이용상태 추정에 식별 가능성 경계를 붙이는 것.**
   `(β_c, β_a, Q_rem, V_shift)` 는 우리가 판정 대상으로 삼는 `(LAM_PE, LAM_NE,
   LLI, 저항)` 과 좌표가 대응한다 (§2 질문 ③(b)). 이 논문은 그 넷을 C/20
   dQ/dV 하나에 맞추고 **점추정만** 낸 뒤 "전극 용량 손실 > 리튬 재고 손실"
   이라는 물리 결론을 도출한다. 그 결론이 **flat valley 위 임의의 한 점**이
   아니라는 보장이 없다. 우리 합성 truth 격자는 그 보장을 계산할 수 있다.
2. **β 의 fold 간 부호 불안정(Fig. S5e)의 원인 분해.** 이 논문 자신의 계보가
   nullspace 논문(참고문헌 [13])을 갖고 있으면서 그 진단을 적용하지 않는다
   (§2 질문 ②). 우리 쪽에서 "고차원 선형회귀 β 의 국소 부호가 fold 마다 뒤집힐
   때 그것이 데이터 한계인가 최적화 문제인가" 는 이미 `[[fitting-degeneracy]]`
   의 flat-valley vs multimodal 구분과 같은 질문이다.
3. **입자 SoC 분포를 "관측 불가" 로 남긴 자리** (§12 Note S11 자인). 합성
   truth 에서는 그 분포를 **강제로 알 수 있다** — 우리 파이프라인이 원리적으로
   메울 수 있는 공백이다.

### 14.3 우리 축에 불리한 관측 (정직하게 기록)

- §2 질문 ③(c) 의 관측 — **느린 형성 32셀에서 모드 좌표는 거의 같은데 cycle
  life 는 다르다** — 는 "모드 분율만 잘 재면 수명이 설명된다" 는 소박한 기대에
  반대한다. 우리 프로젝트는 수명을 예측하지 않으므로 직접 타격은 아니지만,
  "모드 분해가 왜 중요한가" 를 수명 예측으로 정당화하는 서술을 쓸 때 이
  관측을 반드시 옆에 둬야 한다.
- 이 논문의 예측 성공은 **동역학(저항 분포)** 축에서 나온다. `[[pvs-sev-degradation-mode-features]]`
  의 SEV 가 같은 동역학 축을 노리므로, SEV 쪽에는
  이 논문이 **유리한 선례**다 (동역학 신호가 실제로 셀 간 정보를 갖는다).
  반대로 PVS(열역학 축)에는 Fig. S12(a,b) 가 **불리한 선례**다 — 열역학 신호가
  32셀에서 거의 구별되지 않았다.

---

## §15. 그림 판독 기록 — 무엇을 보고 무엇을 안 봤는가

크로핑 도구(`wiki/tools/extract_figures.py`)가 본문+SI 에서 **23장**을 잘랐고
(그림 15 + 표 8), 캡션 오탐 방지로 **10건을 제외**했다. 제외분 중 **Figure 2**
(프레임워크 도식, p.5)와 **Figure 6**(물리 검증, p.11)은 논문의 뼈대라 **해당
쪽 전체를 170 dpi 로 따로 렌더**해 확보했다
(`fig_2_fullpage-p5.png`, `fig_6_fullpage-p11.png`).

**직접 열어 본 것 (10장)**

| 파일 | 무엇을 얻었나 |
|---|---|
| `fig_2_fullpage-p5.png` | 프레임워크 6단계의 실제 상자 배치와 화살표 방향 (§2 질문 ①) |
| `fig_3.png` | β 계단의 값·19개 경계 라벨 A–S · **d²Q/dV² 개별 곡선이 노이즈**라는 것 (§7.9) |
| `fig_4.png` | max 판에서 designed 가 agnostic·autoML 보다 나쁘다는 것 (§8) |
| `fig_5.png` | 빨강/파랑/초록 화살표 구조 = 논증의 뼈대 (§9) |
| `fig_6_fullpage-p11.png` | 실측/시뮬 d²Q/dV² 의 **세로 스케일이 2배 다름** · R_CT 분포의 온도 이동 (§9) |
| `fig_S1.png` | 9개 패널의 ρ 값과 **표본 크기 3–20** (§12 Note S1) |
| `fig_S3.png` | group 단위가 프로토콜이라는 것 · 주황/파랑 두 inner 루프 (§12 Note S3) |
| `fig_S4.png` | step A 두 종이 median MAPE 13–17 대역, step B/C 가 10–12.5 (§7.2) |
| `fig_S5.png` | **★ β 의 fold 간 부호 불안정** (§7.4) — 이번 흡수의 가장 날카로운 그림 |
| `fig_S11.png` | 반쪽셀 OCV 적합이 사실상 완벽 (§12 Note S11) |
| `fig_S12.png` | 실측 곡선이 온도와 무관하게 겹침 + 유틸리제이션 모형의 3.5 V 부근 미스핏 (§2 질문 ③, §12) |

(위 표는 11행 — `fig_S12` 포함해 **11장**을 봤다.)

**보지 않은 것 (그리고 왜)**

- `fig_1.png` (형성 프로토콜 도식) — Fig. 2 전체쪽 렌더 안에 축소판이 들어
  있어 구조를 확인했고, 본문 서술로 충분.
- `fig_S2.png` (데이터 심문 6패널) — 본문 Note S2 텍스트가 결론을 다 인쇄한다.
- `fig_S6.png` (구간 병합 RMSE 막대) — Note S6 텍스트가 임계값과 결론을 인쇄.
- `fig_S7.png`, `fig_S8.png`, `fig_S9.png`, `fig_S10.png` (fold·입력형별 λ
  결정 3지표) — Table S3–S6 이 결과를 다 인쇄하며, 형태는 fig_S5 로 대표됨.
- 표 이미지 8장 (`tab_1`–`tab_6`, `tab_S2`, `tab_S3`) — PDF 텍스트가 정확하므로
  이미지 판독 생략. 값은 전부 텍스트에서 옮겼다.

**본문 서술과 그림이 어긋난 곳**: 정면 모순은 없었다. 다만 **본문이 그림보다
관대한 곳이 두 군데** 있다 — (i) "robustness of β" (본문) vs Fig. S5e 의
fold 간 부호 뒤집힘, (ii) Highlights 3번의 단정적 어조 vs Fig. 6 의 진폭 불일치.
둘 다 §7.4·§9 에 기록했다.

---

## §16. 다음 흡수 후보 (이 논문이 가리키는 곳)

우선순위 순, 각각 **이 위키의 어느 카드에 걸리는지**를 붙인다.

1. **Lin, J., Khoo, E. (2024). "Identifiability study of lithium-ion battery
   capacity fade using degradation mode sensitivity for a minimally and
   intuitively parametrized electrode-specific cell OCV model." *J. Power
   Sources* 605, 234446.** — 이 계보 6편 중 **제목에 identifiability 가 있는
   유일한 문헌**이고 우리 프로젝트의 정확한 선행 연구다. `[[22p-physics-or-
   degeneracy]]`·`[[fitting-degeneracy]]` 에 직접 걸린다. **최우선.**
2. **Schaeffer, J. et al. (2024). "Interpretation of high-dimensional linear
   regression: Effects of nullspace and regularization demonstrated on battery
   data." *Comput. Chem. Eng.* 180, 108471.** — 이 논문 저자들 자신의 nullspace
   경고. §7.4 의 β 부호 불안정을 해석할 언어를 준다.
3. **Cui, X. et al. (2024). "Data-driven analysis of battery formation reveals
   the role of electrode utilization in extending cycle life." *Joule* 8,
   3072–3087.** — 데이터셋 원전이자 **"electrode utilization"** 을 제목에 건
   논문. Table S9 의 4파라미터가 어디서 왔는지, N/P = 1.16 의 출처.
4. **Geslin, A. et al. (2023). "Selecting the appropriate features in battery
   lifetime predictions." *Joule* 7, 1956–1965.** — "operational variation 을
   인코딩한 feature 는 셀-대-셀 변동을 못 잡는다" 의 원전. agnostic 기준선
   패턴의 이론적 근거.
5. **Weng, A. et al. (2021). "Predicting the impact of formation protocols on
   battery lifetime immediately after manufacturing." *Joule* 5, 2971–2992.** —
   R_LS 의 원전이자 각주 49 leakage 지적의 대상.
6. **Bazant, M. Z. (2023). "Unified quantum theory of electrochemical kinetics
   by coupled ion–electron transfer." *Faraday Discuss.* 246, 60–124.** —
   Eq. 6/S8 의 ICET 속도식 원전. 우리가 PyBaMM 의 Butler-Volmer 를 바꿀 일이
   생기면 여기.
