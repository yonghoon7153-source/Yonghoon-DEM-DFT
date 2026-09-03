---
title: "Navidi et al. 2024 — 열화 진단용 PIML 네 방법 비교 (ESM 68, 우리 4-파라미터 창 모델과 좌표가 일치하는 첫 문헌)"
source_url: https://doi.org/10.1016/j.ensm.2024.103343
ingested: 2026-09-03
sha256: d71f0cb9f92de1bc8702fc7398c35e8a0471fe64068fd29d2d4cb3e7d8434d1a
---

# Navidi 2024 — 열화 진단용 PIML 네 방법의 비교

> **Sina Navidi, Adam Thelen, Tingkai Li, Chao Hu**,
> "Physics-informed machine learning for battery degradation diagnostics:
> A comparison of state-of-the-art methods",
> *Energy Storage Materials* **68** (2024) 103343.
> doi:10.1016/j.ensm.2024.103343 · 접수 2023-08-25 / 개정 2024-03-06 /
> 게재 2024-03-18. University of Connecticut · Iowa State University.
> 본문 27쪽 (부록 A 포함, 별도 SI 없음).

**표기 3구분** — `[인쇄]` 원문 본문/캡션에 글자로 있는 것 · `[도표]` 그림에서
눈으로 읽은 것 (`figure-read ≈` 는 눈금 사이 보간) · `[해석]` 이 digest 의
추론. 이 표시가 없는 문장은 전부 원문이 실제로 말한 것이다.

---

## 0. 한 문단 요약

전기화학 반쪽전지 모델(half-cell model)로 셀을 진단하되, **초기 수명 데이터만
가지고 말기 수명의 열화 상태를 예측**하는 문제를 놓고, "물리를 기계학습에
집어넣는 네 가지 방식" — **PINN · co-kriging · delta learning(elastic net) ·
data augmentation** — 을 같은 데이터셋에서 견준다. 데이터는 이식형 등급
LCO‖graphite 24셀 · 4년 이상 · 6개 조건군. 예측 대상은 `[Q, m_p, m_n, LII]`
넷이고, 정답(ground truth)은 **사람이 손으로 맞춘 4-파라미터 반쪽전지 창
모델**의 값이다. 결론은 "네 PIML 이 각자의 순수 데이터 기반 기준선보다 낫고,
그중 PINN 이 가장 좋다"이며, 방법 선택 지침을 Table 5(정성 10축)로 준다.

**이 digest 의 결론 한 줄**: 제목의 "comparison of state-of-the-art methods" 는
**열화 진단 방법의 비교가 아니라, 하나의 진단 모델(반쪽전지 창 적합)을 흉내
내는 기계학습 배관 네 개의 비교**다. 네 방법은 입력(dQ/dV 곡선)·물리
모델(반쪽전지)·정답(사람의 수동 적합)을 **전부 공유**하므로, 그 공유된 축에
비유일성이 있으면 **비교가 그것을 검출할 수 없다.** 그럼에도 이 논문은
부록 A2 에서 **우리 파이프라인과 글자 그대로 같은 자동 적합을 5회 다중시작으로
돌려 그 산포를 그린 유일한 문헌**이며, 그 그림(Fig. 15)이 이 계보에서 우리가
찾던 야생 실측 정박점이다.

---

## 1. 원문에 없어서 확인이 필요한 것 (공백 목록)

이 절을 먼저 읽는다. **아래 항목에 대해 이 논문은 아무 값도 주지 않는다.**

| # | 없는 것 | 왜 문제인가 |
|---|---|---|
| G1 | **본문에 성능 수치가 단 하나도 인쇄돼 있지 않다** | RMSPE 표가 없다. 모든 비교 주장이 막대그래프를 눈으로 읽어야 검증된다. 아래 §3 의 숫자는 전부 `[도표]` 다 |
| G2 | **전압 잔차·측정 잡음의 크기** | `mV` 라는 문자열이 27쪽 전체에 **0회**. 반쪽전지 적합의 전압 잔차 RMSE 가 없다 → 우리 σ=1/5 mV 문턱과 **직접 비교 불가** |
| G3 | **정답(수동 적합)의 불확실성** | 사람이 맞춘 `m_p, m_n, δ_p, δ_n` 에 오차·재현성·작업자 간 변동이 없다. 두 번 맞추면 같은 값이 나오는지 모른다 |
| G4 | **파라미터 상관·Hessian·조건수·Fisher** | 각 0회. 네 창 파라미터끼리 얼마나 얽혀 있는지 재지 않는다 |
| G5 | **자동 적합의 목적함수 값** | Fig. 15 는 파라미터 산포만 그린다. 5개 다중시작 해의 **잔차가 서로 같은지**(flat valley) **다른지**(multimodal) 를 판별할 수 없다 |
| G6 | **기준선(elastic net·data augmentation)의 하이퍼파라미터 탐색** | PINN(손실 가중, Fig. 12)과 co-kriging(커널, Fig. 14) 에만 민감도 스윕이 있다. elastic net 의 `α`·`l1_ratio` 는 언급조차 없다 |
| G7 | **PIML 끼리의 직접 비교표** | 네 패널이 각각 "PIML vs 그 자신의 기준선" 이다. 네 PIML 을 한 축에 놓은 표가 없다 (Fig. 8 에서 독자가 직접 만들어야 한다 — §3.2 에서 만들었다) |
| G8 | **LAM_PE / LAM_NE / LLI 라는 퍼센트 출력** | 예측 대상은 `m_p, m_n, LII` 의 **잔량**이다. `1 − m/m_ini` 로 환산은 되지만 pristine 기준값이 셀별로 인쇄돼 있지 않다 |
| G9 | **자동 적합의 초기값 5개가 무엇이었는지** | "each starting at a different initial guess" 뿐. 분포·범위·경계 없음 |
| G10 | **Fig. 15 두 셀의 조건 표기가 Table 1·§3.1 과 어긋난다** | 아래 §7 「원문 내부 불일치」 참조. 어느 쪽이 맞는지 원문으로 판정 불가 |
| G11 | **코드·데이터 공개 진술 없음** | Data availability 절이 없다 |

---

## 2. 사용자 질문 6개 — 각각 원문 인쇄를 근거로

### 질문 1. 비교 대상 방법이 정확히 무엇무엇인가

`[인쇄, §5]` "These PIML methods are (1) physics-informed neural networks
(PINN), (2) data augmentation, (3) delta learning with kriging (a.k.a.,
multi-fidelity co-kriging), and (4) delta learning with the elastic net."

**여기에 기준선 3종과 부록의 적합 방식 2종을 더하면 실제로 표 위에 오른 것은
아홉 개다.**

| # | 이름 | 무엇인가 | 물리가 들어가는 곳 | 우리 위키에 |
|---|---|---|---|---|
| 1 | **PINN** | 얕은 NN (은닉 2층·뉴런 30·학습가능 2,274개) 가 dQ/dV 100점 → `[m_p,m_n,δ_p,δ_n]`, 그 뒤 반쪽전지 **대리모델** `f_hc` 가 `(Q, LII, V_peak1, V_peak2)` 로 사상 | **손실항 2개 + 구조** | **없다** (Wang 2025 4분류의 2번 칸에 이름만 있었다) |
| 2 | **Data augmentation** | elastic net 을 **반쪽전지 모의 데이터로 증강한** 학습셋에 적합 | **학습 데이터** | **없다** |
| 3 | **Delta learning (elastic net)** | 모의 데이터로 추정기 elastic net 학습 → 초기수명 실측으로 **보정기** elastic net 학습 → 합산 | **학습 데이터(저충실도)** | **없다** |
| 4 | **Co-kriging (delta learning + GPR)** | 2단 다충실도 GPR. `f_H(x) = ρ f_L(x) + f_Δ(x)`, Matérn 3/2 커널, 사후 평균·분산 (식 8·9) | **학습 데이터(저충실도) + 공분산 구조** | GPR 자체는 [[zhang2020-eis-aging-dataset]] 계열에 있으나 **다충실도 co-kriging 은 없다** |
| 5 | 기준선 NN | 같은 구조의 얕은 NN 이 dQ/dV → `[Q,m_p,m_n,LII]` **직접** (Fig. 6a) | 없음 | — |
| 6 | 기준선 kriging (GPR) | 초기수명 실측만으로 학습한 단일 충실도 GPR | 없음 | — |
| 7 | 기준선 elastic net | 초기수명 실측만 | 없음 | — |
| 8 | **수동 반쪽전지 적합 (manual fitting)** | **사람이** dV/dQ 봉우리를 맞추고 QV 끝점을 맞춘다. 부록 A1 에 절차 인쇄 | 물리 그 자체 | [[birkl-ocv-degradation-diagnostic]] 계열이나 **"사람이 맞춘다" 는 절차는 새것** |
| 9 | **자동 반쪽전지 적합 (automatic fitting)** | 이중목적 비선형 최적화 — QV 끝점 일치 + 전체 RMSE 최소화. 초기값 다른 5회 실행 | 물리 그 자체 | **★ 이것이 우리 파이프라인이다** |

**★ 이 표에서 우리 축에 걸리는 다음 흡수 후보** (`[해석]`):
- **PINN 을 반쪽전지 창 파라미터에 적용한 원전** — `[51]` Navidi et al.
  (IDETC 2023) 과 `[30]` **Thelen et al., *Energy Storage Mater.* 50 (2022)
  668–695**. 후자가 이 논문의 직계 선행이고 `[인쇄, §1]` "developed a
  lightweight PIML model to estimate cell degradation modes without relying
  on late-life aging data" 로 소개된다. **우리 4-파라미터 창 좌표를 쓰는
  기계학습 계보의 뿌리**다.
- `[55]` **Lui et al., *J. Power Sources* 485 (2021) 229327** — 이 논문의
  수동 적합 절차와 해체 검증의 출처. `[인쇄, §3.1]` "experimentally validated
  in [31]" 및 "Manual fitting was often preferred … compared to automatic
  fitting **[55]**".
- **co-kriging / 다충실도 GPR** — 우리가 합성 truth(저충실도)와 실측(고충실도)를
  섞을 때 쓸 수 있는 **유일하게 불확실성을 뱉는** 방법. 이 위키에 개념이 없다.

**★ 그리고 비교표에 **없는** 것을 명시한다** (`[해석]` — 이것이 "우리가 안 읽은
방법" 질문의 진짜 답이다):

이 논문은 **열화 진단 방법을 비교하지 않는다.** EIS/DRT · ICA/DVA 봉우리
기반 진단 · P2D/SPM 전기화학 모델 역산 · 칼만 필터 계열 · 파손 해체 —
`[인쇄, §1]` 도입부에서 **선행 연구로 열거만 하고 실험에 올리지 않는다**.
비교 축은 오직 **"같은 반쪽전지 모델을 흉내 내는 배관 네 개"** 다.
그러므로 이 논문에서 "우리가 안 읽은 방법"으로 건질 수 있는 것은
**진단 물리가 아니라 ML 배관**뿐이다.

---

### 질문 2. 비교의 공정성

**(a) 같은 데이터인가 — 그렇다.** 24셀 전부, 4-fold, 같은 분할.

**(b) 같은 지표인가 — 그렇다.** RMSPE (식 14), 파라미터별 `t = Q, m_p, m_n, LII`
4개 각각. `[인쇄, §6.2]` "Note that a recent study on degradation diagnostics
directly relevant to this work used 'RMSE%' in place of 'RMSPE' [30]." (지표
이름의 계보를 밝히는 것은 정직한 서술이다.)

**(c) 같은 학습량인가 — 아니다.** `[인쇄, Table 2]`

| 방법 | 학습점 | 시험점 |
|---|---|---|
| PINN | **212** | 200 / 192 |
| Data Augmentation | **212** | 200 / 192 |
| Delta Learning | **964** | 200 / 192 |
| Baseline Methods | **180** | 200 / 192 |

`[해석]` 기준선 180 = 18 학습셀 × 초기 10점. PINN·증강은 +32 모의점, delta
learning 은 **+784 모의점**이다. 즉 **delta learning 은 다른 PIML 보다 모의
데이터를 24배 더 받는다.** 그런데 Fig. 8 에서 delta learning 이 `m_p` `m_n`
에서 가장 나쁜 축에 속한다 — 이것은 "모의 데이터 양이 문제가 아니다" 라는
증거지만 원문은 이 표를 성능 해석에 **한 번도 연결하지 않는다.** 그리고
co-kriging 은 Table 2 에 **행 자체가 없다** (delta learning 에 포함되는지
불명 — G-공백).

**(d) 하이퍼파라미터를 누가 어떻게 정했는가 — 비대칭이다. 이것이 이 비교의
가장 약한 고리다.**

| 방법 | 하이퍼파라미터 | 어떻게 정했나 |
|---|---|---|
| PINN (**저자 신규**) | 은닉층 2, 뉴런 30, lr 0.005–0.01, epoch 1000–2000, batch 200 (Table 3) · 손실 가중 `λ1, λ2` | `[인쇄, §5.1]` "empirically determined" + **Fig. 12 전용 민감도 스윕(r1,r2,r3 각 5점)** |
| Co-kriging (**저자 신규**) | 길이척도 5258.770 / 1.000, 신호분산 0.015 / 0.006–0.008, ν=3/2 (Table 4) | **Fig. 14 전용 커널 6종 스윕** |
| Delta learning (elastic net) | `α`, `l1_ratio` | **언급 없음** |
| Data augmentation (elastic net) | 같음 + 증강 규칙 | **언급 없음** ("filtered to include only the highest degradation values" 라는 정성 규칙만) |
| 기준선 3종 | 〃 | **언급 없음** |

`[해석]` **자기 방법만 튜닝하는 함정에 정확히 걸린다.** 저자가 새로 제안한
두 방법(PINN, co-kriging)에만 전용 민감도 그림이 하나씩 붙고, 나머지 다섯
모델의 하이퍼파라미터는 **선택 절차가 서술되지 않는다.** 특히 elastic net 은
`α`(정칙화 세기)에 성능이 크게 좌우되는 모형인데 값이 없다. 결론
`[인쇄, §7.2.1]` "the PINN methodology demonstrated superior accuracy" 는
**이 비대칭 위에서 나온 것**이다.

**다만 공정한 쪽도 적어야 한다** — 저자들은 다음을 **했다**:
- `[인쇄, §6.3]` "To ensure a fair comparison, we performed ten cross-validation
  runs for each model and computed the mean and standard deviation of the
  RMSPE across these runs." (Fig. 8 의 오차 막대)
- `[인쇄, §6.3]` 그 오차 막대의 의미를 **스스로 좁힌다**: "the increased width
  of the error bars reflects **greater variability in performance across
  different training runs, rather than solely indicating elevated predictive
  uncertainty** within the trained models." — 이 계보에서 오차 막대의 의미를
  명시적으로 한정한 두 번째 사례다 (첫째는 Birkl 2017 §4.3 의 코인셀 제작
  재현성).
- `[인쇄, §5.1 / 6.6.1]` PINN 의 증강 데이터는 **다른 PIML 과 일치시키려고**
  넣었다고 밝히고, Fig. 13 에서 그 기여를 분리해 보인다 (ablation).

**(e) 셀 단위 분할인가 — 그렇다. 그러나 프로토콜 단위는 아니다.**

`[인쇄, §6.1]` "we divided the dataset into four mutually exclusive folds,
**with each fold including one battery cell from each group in the test set**."

`[해석]` 셀 누출은 없다 — 시험 셀의 데이터는 학습에 전혀 안 들어간다. **그러나
시험 셀과 같은 조건군(같은 온도·전류·컷오프)의 형제 셀 3개가 학습에 들어
있다.** 즉 leave-one-cell-out 이지 **leave-one-protocol-out 이 아니다.**
[[fused-lasso-feature-design-framework]] (Rhyu 2025) 이 프로토콜 group CV 를
쓴 것과 대조된다 — 이 계보에서 검증 설계의 엄격도는 **Rhyu > Navidi > 나머지**
순이다. 그리고 시험 집합은 시험 셀의 **전 생애 점**(≈33점)이므로 초기수명
내삽과 말기수명 외삽이 하나의 RMSPE 에 섞여 있다.

**(f) 입력에 프로토콜 식별자가 섞였는가 — 아니다 (이 계보에서 드문 청정함).**
`[인쇄, §4]` 입력은 dQ/dV(V) 곡선 위 **100점뿐**이고, "Using the differential
capacity curve as input is common practice and **eliminates the need for
manual feature selection**". 온도·전류·군 번호가 입력에 없다. `[해석]`
그러므로 우리가 다른 논문에서 반복해 지적한 "프로토콜 식별자 누출" 은
**이 논문에 없다.**

---

### 질문 3. physics-informed 가 정확히 어느 지점에 들어가는가 (4분류 적용)

이 위키가 [[interpretable-ml-battery-prognosis-taxonomy]] 에서 정리한 축
(**손실항 / 입력 feature / 구조 / 사후해석**) 을 그대로 적용한다. (원 4분류는
Wang et al. 2025 리뷰의 것이고 Tao 2025 의 것이 아니다 — 이 위키의 출처는
`raw/papers/wang2025_interpretable-ml-battery-prognosis.md`.)

| 자리 | PINN | Co-kriging | Delta (Enet) | Data Aug |
|---|---|---|---|---|
| **① 손실항** | **★ 있다 — 두 개** | 없다 | 없다 | 없다 |
| **② 입력 feature** | **없다** (원시 dQ/dV 100점) | 없다 | 없다 | 없다 |
| **③ 구조** | **★ 있다** (2단: 창 파라미터 → 대리모델) | △ 다충실도 자기회귀 구조 `f_H = ρf_L + f_Δ` | △ 추정기+보정기 2단 | 없다 |
| **④ 사후해석** | 없다 | 없다 | 없다 | 없다 |
| **⑤ (분류 밖) 학습 데이터** | 있다 (말기 20 % 모의) | **★ 유일한 통로** | **★ 유일한 통로** | **★ 유일한 통로** |
| **⑥ (분류 밖) 라벨 그 자체** | **네 방법 전부** — 정답이 반쪽전지 적합값 | 〃 | 〃 | 〃 |

**① 손실항 — 정확히 두 개.** `[인쇄, 식 4]` `L_total = L1 + λ1·L2 + λ2·L3`
- `L1` (식 1) — 데이터 기반. `y = [m_p, m_n, δ_p, δ_n]^T` 의 MSE.
  **물리가 아니다.**
- `L2` (식 2) — `[인쇄]` 대리모델 `f_hc` 를 통과시킨 `[Q̂, LÎI]` 와 참값
  `[Q, LII]` 의 MSE. 목적은 `[인쇄, §5.1]` "verifying that the
  network-predicted half-cell model parameters lead to simulated curves with
  **endpoints that closely match those of the true fitted curves**".
  `[해석]` **끝점 일치 제약**이다 — [[np-lip-ocv-reparametrization]] 이
  말하는 컷오프 등식 제약의 부드러운(penalty) 판이다.
- `L3` (식 3) — `[인쇄]` 모의 dQ/dV 곡선과 실측 dQ/dV 곡선의 **주요 봉우리 두
  개의 전압 위치** 차이의 MSE. 봉우리 검출은 prominence·distance·height·width
  기준, y값 내림차순 상위 2개.

**② 입력 feature — 명시적으로 없다.** 이것이 [[fused-lasso-feature-design-framework]]
(Rhyu 2025)·[[pvs-sev-degradation-mode-features]] 계열과의 결정적 차이다.
저자들은 feature 설계를 **거부**하고 곡선 전체를 넣는다.

**③ 구조 — 이 논문의 진짜 기여로 읽힌다.** `[인쇄, §5.1]` "we adopt a
two-step process of **first predicting the half-cell model parameters and then
mapping them into the capacity and a degradation parameter** …, rather than
directly predicting the health parameters, as implemented in a baseline neural
network". `[도표, Fig. 6]` 확인함 — (a) 기준선은 출력이
`[Q̂, m̂_p, m̂_n, LÎI]` 4개, (b) PINN 은 출력이 `[m̂_p, m̂_n, δ̂_p, δ̂_n]` 4개이고
`Q, LII` 는 **대리모델이 계산한다**. 저자는 이 둘을 `[인쇄, §6.3]` Pateras
et al. `[66]` 의 어휘로 **observational bias**(데이터)와 **inductive
bias**(구조)라 부른다.

**④ 사후해석 — 0.** SHAP·PDP·permutation importance·attention 전무.

**⑤ 분류 밖의 다섯째 자리 — "학습 데이터".** Wang 2025 의 4분류에 이 칸이
없다. 그런데 이 논문에서 **네 방법 중 셋은 오직 이 칸으로만 물리를 넣는다.**
`[해석]` **우리 4분류를 이 논문에 적용한 결과의 첫째 소득은, 4분류에 칸이
하나 모자란다는 것이다.** 그리고 이 논문이 **그 칸의 효과를 직접 잰다** —

`[도표, Fig. 13]` (직접 봄. 막대 4종 × 파라미터 4개, RMSPE %)

| | Q | m_p | m_n | LII |
|---|---|---|---|---|
| Baseline NN | ≈5.7 | ≈14.1 | ≈16.2 | ≈7.3 |
| Baseline NN **+ 증강** | ≈5.1 | ≈12.6 | ≈12.5 | ≈5.3 |
| **PINN (증강 없이)** | ≈2.5 | ≈4.2 | ≈6.0 | ≈3.5 |
| **PINN + 증강** | ≈1.3 | ≈4.7 | ≈5.6 | ≈1.6 |

`[인쇄, §6.6.1]` "improved extrapolation capability can be **mainly attributed
to customizing the loss function** with known physics." — **도표가 이 문장을
지지한다**: 증강만으로는 10–23 % 상대개선, 손실항으로는 55–70 % 개선.
`[해석]` **우리 4분류 축에 실측 순위가 처음 붙었다 — 손실항(①) ≫ 학습
데이터(⑤).** 다만 이 실험은 PINN 하나에서만 돌았고, 증강 단독 효과는 delta
learning·data augmentation 쪽에서 별도로 측정되지 않았다.

**⑥ 분류 밖의 여섯째 자리 — "라벨 그 자체". 원문이 한 번도 이름 붙이지
않는다.** `[인쇄, §6.2]` "the corresponding ground truth values, **which were
the degradation parameters obtained by fitting the half-cell model to
experimental full-cell curves**". `[해석]` 즉 물리는 손실항·구조·데이터보다
**먼저** 라벨에 들어가 있고, 네 방법 모두 그것을 상속한다. 4분류의 어느
칸에도 이 자리가 없다 — **분류 자체의 사각지대**다.

---

### 질문 4. degeneracy · identifiability 를 다루는가

**어휘 전수 — 이 계보 열두 편째** (합자 정규화 후, 본문+참고문헌 138,573자):

| 검색어 | 횟수 | 비고 |
|---|---|---|
| `identifiab*` | **0** | |
| `degenerac*` / `degenerat*` | **0** | (`degradation` 은 다수, 별개) |
| `nullspace` / `null space` | **0** | |
| `non-unique` / `nonunique` / `uniqueness` | **0** | |
| `collinear*` | **0** | |
| `ill-posed` | **1** | 참고문헌 [43] 인용 문맥, 자기 문제에 대한 진술 아님 |
| `Hessian` · `Fisher` · `condition number` · `singular value` · `profile likelihood` · `CRLB`/`Cramér` | **각 0** | |
| `correlat*` | 13 | **전부 GPR 커널의 데이터점 간 상관** — 파라미터 상관 0 |
| `cross-valid*` | **5** | 4-fold CV·커널 선택 |
| `uncertaint*` | **21** | **이 계보 최다.** 그러나 §7.1.10 한 절과 참고문헌에 집중 |
| `error bar` | **2** | Fig. 8(학습 실행 변동) · Fig. 15(다중시작 산포) |
| `confidence interval` | 1 | 참고문헌 [86] 제목 안 |
| `noise` | **3** | **전부 "모형이 잡음을 외운다"(overfitting)** — 측정 잡음 모델 0 |
| `LLI` / `LAM` | 18 / 20 | 정의·서술용. **수치 산출 없음** (출력은 `m_p, m_n, LII` 잔량) |
| `half-cell` | **99** | 논문의 뼈대 |
| `mV` / `millivolt` | **0** | |

**답: 비유일성을 정면으로 묻지 않는다. 그러나 이 계보에서 처음으로 그
현상을 실험으로 그린다.**

**(a) 물어야 했는데 안 물은 자리 — Table 5.** `[인쇄, Table 5]` 는 열 개 축으로
네 방법을 정성 등급(High/Medium/Low)한다: Model Flexibility · Data
Requirements · Ease of Implementation · Computational Cost · Generalization
Capability · Interpretability · Prediction Accuracy · **Uncertainty
Quantification Capability** · Scalability · Applicability. `[해석]`
**"어느 방법이 라벨의 비유일성에 강한가" 라는 축이 없다.** 가장 가까운
`Uncertainty Quantification Capability` 는 §7.1.10 이 정의하듯 **예측
불확실성**이지 파라미터 식별 가능성이 아니며, 등급은
`PINN=Medium-low · Co-kriging=High · Delta=Low · DataAug=Low` 로 **전부
정성**이고 그 등급을 뒷받침하는 계산이 논문 안에 없다 (co-kriging 은 식 9 로
사후 분산을 계산할 수 있는데 **그 분산을 그린 그림이 없다**).

**★ 비교 논문에서 이 침묵은 다른 열한 편의 침묵과 등급이 다르다.** 개별
논문이 자기 방법의 식별 가능성을 안 재는 것과, **열 개 축으로 네 방법을
등급 매기는 표를 만들면서 그 축을 안 넣는 것**은 다르다. 후자는 그 축이
**선택지 목록에 없었다**는 뜻이다.

**(b) 그런데 현상은 관측하고 이름만 다르게 붙인다 — 부록 A2.**

`[인쇄, 부록 A2, 첫째 불릿]`
> "First, the optimization problem for automatic fitting **has multiple local
> minima, leading to run-to-run variability in optimal active mass parameters
> depending on the initial guess**. We illustrated this variability by
> presenting the mean and error bars (spread) derived from **five optimization
> runs, each starting at a different initial guess**."

`[해석]` **이것은 [[fitting-degeneracy]] 의 두 실패 모드 중 multimodal 가지를
정확히 서술한 것이다** — "multiple local minima" 라는 진단명까지 같다.
그러나 그들은 **flat valley 와 구별하지 않는다**: 5개 해의 **목적함수 값이
서로 같은지** 보고하지 않으므로 (G5), 데이터가 못 가르는 것인지 최적화가
못 찾는 것인지 이 논문으로는 판정 불가다. **우리 저장소의 paired multi-start
진단이 정확히 이 구별을 위해 설계됐다.**

**(c) Fig. 3b 는 축퇴 그림인데 저자가 그렇게 읽지 않는다.**

`[도표, Fig. 3]` (직접 봄)
- **(a)** 단독 모드 20 % 스윕 3종. Fresh 대비: `20 % LAM_PE`(파랑)는 3.79 V
  봉우리를 **≈4.7 → ≈8.4 V⁻¹ 로 키우고** 3.70 V 봉우리를 3.68 V 로 밀어
  ≈1.9 로 낮춘다. `20 % LAM_NE`(주황)도 **같은 3.79 V 봉우리를 ≈6.6 으로
  키운다**. `20 % LLI`(초록)는 전 구간을 눌러 3.71 V 에 ≈3.5, 3.8–3.9 V 에
  ≈1.9 의 완만한 언덕만 남긴다.
- **(b)** 2모드 조합 2종. `20 % LAM_PE + 20 % LLI`(파랑 점쇄)와
  `20 % LAM_NE + 20 % LLI`(주황 점쇄)가 **3.4–3.72 V 구간에서 사실상 겹치고**,
  3.72–3.90 V 에서만 갈린다 (파랑은 3.78 V 근처에 ≈2.6 의 어깨, 주황은
  3.84 V 근처에 ≈3.1 의 봉우리). 두 곡선의 차이는 **각자가 Fresh 와 갖는
  차이보다 훨씬 작다.**

`[인쇄, §3.1]` 원문의 읽기는 공통점뿐이다: "a loss of either active material
combined with a loss of lithium inventory **significantly reduces the magnitude
of the peaks** in the incremental capacity curve, especially the larger peak
around 3.8 V."

`[해석]` **원문은 "둘 다 봉우리를 낮춘다"고 적고 멈춘다. 그런데 이 논문의
모든 기계학습 입력이 바로 이 dQ/dV 곡선이다.** 즉 Fig. 3b 는
"LAM_PE+LLI 와 LAM_NE+LLI 를 곡선으로 가르기 어렵다" 는 그림이고, 그
어려움이 §6.3 의 실측 — `[인쇄]` "the degradation trends of the negative and
positive active mass parameters (m_p and m_n) were generally **more complex and
challenging to predict** compared to the capacity and lithium inventory" —
과 정확히 같은 방향인데, **저자는 그 어려움을 "물리·화학 과정이 복잡해서"
라고 설명하고 (§6.3: "solid-state diffusion, phase transformations, and
mechanical stresses") 관측 가능성 문제로 읽지 않는다.**

**(d) 그리고 Fig. 8 이 그 축퇴의 크기를 재고 있다** — 아래 §3.

---

### 질문 5. 잡음·불확실성 처리 — 우리 1 mV / 5 mV 문턱과 비교 가능한가

**결론 먼저: 전압 단위 값은 하나도 없다 (`mV` 0회). 따라서 σ=1/5 mV 와의
직접 비교는 불가능하다. 대신 파라미터 단위(정규화 활물질)의 산포가 있고,
그것은 우리 `tol = 2 %p` 판정선과 직접 비교된다.**

**(a) 각 방법이 라벨 불확실성을 다루는가 — 넷 다 안 다룬다.** 정답 `y` 는
점추정이고, 네 손실함수 어디에도 라벨 분산·가중이 없다. §7.1.10 의 UQ 논의는
**예측** 불확실성이고, 그나마 `[인쇄]` "**should be considered**" (PINN),
"it **is possible to** introduce" (delta/augmentation) 라는 **미래 시제**다 —
이 논문에서 실행되지 않았다. 실행된 UQ 는 co-kriging 의 사후 분산(식 9)
하나인데 **그리지 않는다**.

**(b) 측정 잡음 모델 — 없다.** `noise` 3회 전부 과적합 문맥. 잡음 스윕 없음.

**(c) 그런데 파라미터 산포는 있다 — Fig. 15. 이 계보에서 반쪽전지 창 적합의
다중시작 산포를 그린 첫 그림이다.**

`[도표, Fig. 15]` (네 패널 전부 확대해 직접 봄. y축 = Normalized active mass,
눈금 0.5 / 0.67 / 0.83 / 1. 주황 사각 = 자동 적합 **평균 ± 5회 산포**,
검정 원 = 수동 적합, 초록 삼각 = PINN, 자홍 마름모 = 해체 실측 2점.
**오차 막대는 자동 적합에만 있다.**)

자동 적합 다중시작 산포 (반폭, figure-read ≈):

| 패널 | day 0 | ~300 | ~660 | ~1000 | ~1300 |
|---|---|---|---|---|---|
| G2C1 `m_p` | **±0.075** | ±0.045 | ±0.05 | ±0.035 | ±0.05 |
| G2C1 `m_n` | **±0.10** | ±0.03 | **±0.10** | ±0.07 | **±0.11** |
| G1C3 `m_p` | ±0.05 | **±0.085** | ±0.02 | ±0.055 | ±0.035 |
| G1C3 `m_n` | ±0.05 | **±0.08** | ±0.015 | ±0.055 | ±0.03 |

**★ 우리 문턱과의 대조** (`[해석]`): 우리 판정 임계는 `tol = 2 %p` 다.
위 산포는 **±1.5 ~ ±11 %p** 이고 중앙값이 대략 ±5 %p 다. 즉
**초기값만 바꿔도 나오는 활물질 추정값의 흔들림이 우리 판정선의 1~5배**다.
이것은 σ=1/5 mV 와 같은 축의 값이 아니지만 (전압 잡음이 아니라 파라미터
산포), **우리가 "degenerate" 라고 부르는 사건이 야생의 실측 셀에서 실제로
그 크기로 일어난다**는 첫 외부 정박점이다.

**(d) 그리고 그 산포가 오차를 크게 과소평가한다** — 해체 실측과 대조:

`[도표, Fig. 15]` day ≈1300–1400 시점의 네 값 (figure-read ≈):

| 패널 | 해체 실측(2점) | 수동 | PINN | 자동(±산포) | 실측 대비 최대 편차 |
|---|---|---|---|---|---|
| G2C1 `m_p` | **0.635, 0.625** | 0.66 | 0.72 | **0.885** ±0.05 | 자동 **+0.25** |
| G2C1 `m_n` | **1.00, 0.93** | 0.875 | 0.845 | 0.82 ±0.11 | 자동 **−0.15** |
| G1C3 `m_p` | **1.00, 0.92** | 0.895 | 0.875 | **0.765** ±0.035 | 자동 **−0.20** |
| G1C3 `m_n` | **0.825, 0.805** | 0.895 | 0.89 | **0.765** ±0.03 | **수동 +0.08** |

세 가지가 따라 나온다 (`[해석]`):

1. **자동 적합의 다중시작 산포(±0.03–0.11)가 실제 오차(0.15–0.25)를 담지
   못한다.** G2C1 `m_p` 에서 자동 적합의 5개 해가 전부 0.835–0.935 안에
   있는데 참값은 0.63 이다. **다중시작 산포는 정확도의 하한조차 아니다** —
   우리 저장소가 multi-start 산포를 degeneracy 증거로 쓸 때 이 경고가 붙어야
   한다. (이 위키가 이미 아는 형태: [[nullspace-coefficient-interpretation]]
   의 "낮은 잔차 ⇒ 참에 가깝다" 반증과 같은 계열.)
2. **네 패널 중 3개에서 수동 적합이 가장 가깝지만, 4번째(G1C3 `m_n`)에서는
   자동 적합이 이긴다.** `[인쇄, 부록 A2]` "Both methods generally agreed
   better with experimental validation than automatic fitting" 은 **자기
   그림의 넷째 패널과 어긋난다** (아래 §7).
3. **두 패널(G2C1 `m_n`, G1C3 `m_p`)에서는 세 방법 전부가 해체 실측 두 점의
   바깥에 있다.** 해체 실측이 0.92–1.00(거의 손실 없음)을 말하는데 세 적합은
   0.765–0.895(10–24 % 손실)를 말한다. **원문은 이 불일치를 논의하지 않는다.**

**(e) 정답 자체의 재현성** (`[도표]`, figure-read ≈): 해체 실측 마름모가
전극당 2점이고 그 간격이 **G2C1 PE 0.01 · G2C1 NE 0.07 · G1C3 PE 0.08 ·
G1C3 NE 0.02** 다. `[해석]` 즉 **"실험 정답" 자체가 1–8 %p 흔들린다.**
[[np-lip-ocv-reparametrization]] 에 등재한 Cui 2024 Table S3 의
"PE 1–12 mV / NE 8–93 mV 비균일 재현성" 과 **단위는 다르지만 같은 성질**
(반쪽전지 재조립 실측의 전극별 비균일 재현성)의 두 번째 사례다.

---

### 질문 6. 우리가 채택할 것과 반증해야 할 것

**★ 우리 파이프라인이 이 비교표의 어디에 놓이는가 — 정확히 표 밖의 9번,
"automatic fitting" 이다. 그리고 이 논문은 그것을 시험대에 올려 놓고
기각한다.**

좌표 대응부터 확정한다 (`[인쇄, 부록 A1 식]`):

```
Navidi:  V_c(Q) = V_p( (Q − δ_p)/m_p ) − V_n( (Q − δ_n)/m_n )
우리  :  v_full  = V_PE( (Q − β_PE)/α_PE ) − V_NE( (Q − β_NE)/α_NE )
        m_p ↔ α_PE ·  δ_p ↔ β_PE ·  m_n ↔ α_NE ·  δ_n ↔ β_NE
```

- **자유 파라미터 4개**, **컷오프 등식 제약 없음** — [[birkl-ocv-degradation-diagnostic]]
  의 3개(등식 소거)와 다르고 **우리 창 모델과 같다.** 이 계보 열두 편 중
  **우리 fitting 모델과 구조가 글자 그대로 일치하는 첫 문헌**이다.
- **LII 정의**: `[인쇄, §3]` `LII = Q_p − (δ_p − δ_n)`, `Q_p = m_p q_p`.
  `[해석]` 손실 형태로 바꾸면 `1 − LII/LII_ini` 가 우리 저장소 문서의
  `LLI = (1 − α_PE) + (β_PE − β_NE)` 와 **같은 구조**다 (`(1−α_PE)` ↔
  `Q_p` 감소분, `(β_PE − β_NE)` ↔ `(δ_p − δ_n)` 이동분, 둘 다 `Q_p,ini`
  단위). **[[22p-physics-or-degeneracy]] Status Log (2)·(3) 에서 "Birkl
  2017 부호 규약" 주석의 출처를 못 찾고 종결했던 항목에 대해, 같은 형태의
  식이 실재하는 자리가 처음 확인됐다.** 다만 **인용 경로의 증거는 아니다** —
  Navidi 2024 는 2024년이고 우리 주석보다 뒤이며, 이 식의 계보는 이 논문이
  `[30]`(Thelen 2022)·`[55]`(Lui 2021)로 돌린다. **후속 확인 항목으로
  등재하되 우리 문서는 고치지 않았다.**

**채택할 것 (근거 등급 순)**

| # | 무엇 | 왜 | 비용 |
|---|---|---|---|
| A1 | **다중시작 산포 그림을 우리 논문에 그대로 넣는다** — Fig. 15 형식(평균 + 산포 막대, 시간축) | 이 계보에 선례가 **이것 하나**뿐이고, 우리는 참값을 안다. 그들이 못 그린 "산포 vs 실제 오차" 를 우리는 그릴 수 있다 | 이미 있는 산출물 재집계 |
| A2 | **"다중시작 산포는 오차의 하한이 아니다" 를 명시 경고로 넣는다** | §5(d)1 의 실측이 근거. 우리 자신의 진단이 오해될 통로를 막는다 | 문장 |
| A3 | **손실항 ≫ 학습 데이터 라는 순위** (Fig. 13) | 우리 4분류에 처음 붙은 실측 순위. [[interpretable-ml-battery-prognosis-taxonomy]] 갱신 | 문장 |
| A4 | **4분류에 "학습 데이터"·"라벨" 칸을 추가** | 이 논문 네 방법 중 셋이 첫째 칸으로만, 넷 다 둘째 칸으로 물리를 넣는다 | 개념 페이지 갱신 |
| A5 | **`L3`(dQ/dV 봉우리 전압 위치) 손실항** | 우리가 2026-08-20 에 시험한 것은 **dQ/dV 곡선 항**이고 개선이 없었다. **봉우리 *위치*만 쓰는 것은 다른 항이다** — 곡선 전체가 아니라 2개 스칼라. Fig. 12 `r3=0` 에서 `m_p` 가 6.6 으로 가장 나빠지므로 **PE 정보를 이 항이 나른다** | 값싼 추가 실험 |
| A6 | **co-kriging / 다충실도 GPR** | 합성 truth(저충실도) + 실측(고충실도)를 섞는 유일하게 사후 분산을 뱉는 방법. 우리에겐 아직 개념조차 없다 | 새 개념 흡수 |

**반증해야 할 것**

| # | 주장 | 어떻게 반증/한정하는가 |
|---|---|---|
| B1 | `[인쇄, §6.3]` "**all the PIML methods exhibited improved error rates** compared to their data-driven counterparts" | **자기 Fig. 8 이 반례를 인쇄한다** — co-kriging `Q` **1.37** vs 기준선 kriging **0.93**. 우리 서술에 인용하면 안 되는 문장 |
| B2 | `[인쇄, §7.2.2]` co-kriging 의 "capacity prediction … exhibited a **near-zero error rate**" | `[도표, Fig. 8]` co-kriging `Q` = **1.37 %**, 기준선 kriging = **0.93 %**. "near-zero" 는 **기준선** 쪽 값이다 |
| B3 | `[인쇄, §7.2.1]` PINN 이 "superior accuracy … specifically in … `m_p` and `m_n`" | `[도표, Fig. 8]` `m_p`: **Data Augmentation 3.68 < PINN 4.52**. `m_n` 은 PINN(5.56)이 맞다. **절반만 맞다** |
| B4 | `[인쇄, 부록 A2]` 수동·PINN 이 "generally agreed better with experimental validation than automatic fitting" | `[도표, Fig. 15]` G1C3 `m_n`: 실측 0.805–0.825, 자동 0.765, 수동 0.895. **자동이 이긴다.** 4패널 중 1패널에서 반례 |
| B5 | 수동 적합을 정답으로 쓰는 것이 정당하다는 전제 | 논문 자신이 정당화를 시도한다(부록 A2, Fig. 15) — 그러나 **셀 2개 · 전극당 실측 2점**이고 그중 2패널은 세 방법 전부가 실측 바깥이다. 이 정당화는 우리 합성 truth 격자가 하려는 일을 **훨씬 작은 표본으로** 한 것 |
| B6 | "자동 적합은 국소최소가 많아 못 쓴다" | **우리 저장소가 이 주장을 정면으로 시험 중인 대상이다.** 반증 형태: 그들이 안 나눈 flat valley ↔ multimodal 를 나누고, warm start·예산·restart 예산을 통제하면 산포가 얼마나 줄어드는지 보인다. 그들은 목적함수 값을 보고하지 않으므로 **이 구별을 안 해 본 채로 기각했다** |

**★ 이 논문이 우리에게 주는 가장 큰 것** (`[해석]`): 우리 프로젝트의 위치가
"남이 안 한 것을 한다" 에서 **"남이 해 보고 못 쓴다고 결론 내린 것을,
그 결론이 근거로 삼은 구별(데이터 한계 vs 최적화 난이도)을 실제로 수행해
재판정한다"** 로 선명해진다. Fig. 15 는 우리 문제 서술의 **인용 가능한 문헌
근거**이고, 동시에 우리 방법을 기각한 **가장 구체적인 반대 진술**이다.

---

## 3. 성능 수치 — 전부 그림에서 읽었다

**원문 본문에는 성능 숫자가 하나도 없다.** 아래는 `[도표, Fig. 8]` 의 막대
위에 **인쇄된 숫자**를 직접 읽은 것이다 (막대 높이 보간이 아니라 글자).

### 3.1 원문이 그리는 대로 — 각 PIML vs 자기 기준선 (RMSPE %)

| 패널 | | Q | m_p | m_n | LII |
|---|---|---|---|---|---|
| ① | 기준선 NN | 5.72 | 14.07 | 16.17 | 7.27 |
| | **PINN** | **1.31** | **4.52** | **5.56** | **1.51** |
| ② | 기준선 Kriging | **0.93** | 9.58 | 9.85 | 2.13 |
| | **Co-kriging** | 1.37 ⚠ | **4.29** | **8.68** | **1.74** |
| ③ | 기준선 Elastic Net | 1.02 | 5.49 | 7.06 | 3.87 |
| | **Delta Learning** | **0.55** | **5.04** | **6.63** | **2.13** |
| ④ | 기준선 Elastic Net | 1.02 | 5.49 | 7.06 | 3.87 |
| | **Data Augmentation** | **0.77** | **3.68** | **6.59** | **1.45** |

⚠ **co-kriging 의 `Q` 는 기준선보다 나쁘다** (1.37 vs 0.93). 본문
`[인쇄, §6.3]` "all the PIML methods exhibited improved error rates compared to
their data-driven counterparts" 의 **직접 반례이며 원문은 언급하지 않는다.**

### 3.2 원문이 그리지 않는 표 — 일곱 모델을 한 축에 (이 digest 가 만든 것)

`[해석]` 같은 Fig. 8 값을 재배열했다. 괄호는 순위.

| 모델 | Q | m_p | m_n | LII | **평균 순위** |
|---|---|---|---|---|---|
| **Data Augmentation** | 0.77 (2) | **3.68 (1)** | 6.59 (2) | **1.45 (1)** | **1.50** |
| PINN | 1.31 (5) | 4.52 (3) | **5.56 (1)** | 1.51 (2) | 2.75 |
| Delta Learning | **0.55 (1)** | 5.04 (4) | 6.63 (3) | 2.13 (4) | 3.00 |
| Co-kriging | 1.37 (6) | 4.29 (2) | 8.68 (5) | 1.74 (3) | 4.00 |
| 기준선 Elastic Net | 1.02 (4) | 5.49 (5) | 7.06 (4) | 3.87 (6) | 4.75 |
| 기준선 Kriging | 0.93 (3) | 9.58 (6) | 9.85 (6) | 2.13 (4) | 4.75 |
| 기준선 NN | 5.72 (7) | 14.07 (7) | 16.17 (7) | 7.27 (7) | 7.00 |

**세 가지가 나온다** (`[해석]`):

1. **가장 단순한 방법(elastic net + 모의 데이터 증강)이 종합 1위다.** 물리가
   들어가는 통로가 학습 데이터 하나뿐이고, Table 5 에서 Interpretability
   **Low** · Generalization **Medium** 으로 가장 낮게 등급된 방법이다.
   그런데 논문의 서사는 PINN 을 민다.
2. **PINN 의 극적인 개선(§6.3 의 서사)은 상당 부분 기준선 선택의 결과다.**
   PINN 은 **가장 나쁜 기준선(NN, 평균순위 7위)** 과 짝지어져 있다. 같은 Q
   에서 PINN(1.31)은 **정칙화 선형모형(elastic net 1.02)에게도 진다.**
3. **`Q` 는 아무 방법이나 잘 맞히고(0.55–1.37, NN 제외), `m_p`·`m_n` 은
   아무 방법도 잘 못 맞힌다(3.7–9.9).** 이 대비가 이 논문의 진짜 신호다.
   `[인쇄, §6.3]` 저자도 적는다 — "the degradation trends of the negative and
   positive active mass parameters … were generally **more complex and
   challenging to predict** compared to the capacity and lithium inventory."
   `[해석]` **전극별 분해가 어렵고 총량은 쉽다** — 이 위키가
   [[np-lip-ocv-reparametrization]]·[[fitting-degeneracy]] 에서 예측한 형태
   그대로다 (형상 2 자유도 + 총용량 1). 다만 이것은 **정황이지 증명이 아니다**:
   `m_p, m_n` 이 어려운 이유가 관측 가능성인지 궤적의 비단조성인지 이 논문은
   가르지 않는다.

### 3.3 학습 표본 크기 (Fig. 9)

`[인쇄, §6.4]` `n_exp` = 90 / 180 / 270 (셀당 5 / 10 / 15 특성화점 = 3 / 8 /
12개월). 결론: `[인쇄]` 90→180 에서 큰 개선, 180→270 에서 `[인쇄]` "does not
significantly impact the model's performance". PINN 만 `[인쇄]` "relatively
consistent performance with slight improvements". 기준선 kriging 은
`[인쇄]` "maintained consistent accuracy, regardless of the number".
`[해석]` **8개월이 포화점이라는 이 결론은 우리에게 직접 쓸 수 없다** —
우리 격자는 사이클 수 축이지 달력 축이 아니고, 셀 화학·프로토콜이 다르다.
(그림 9 는 직접 보지 않았다 — §6 참조.)

### 3.4 외삽 (Fig. 10·11) — 보지 않음

`[인쇄, §6.5]` Fig. 10 은 시험셀 G2C2(C/24, 55 °C)에 대해 열화도 축에서
버블 크기 = `C1 + C2 × RMSE([m̂_p, m̂_n, LÎI], [m_p, m_n, LII])` (식 15).
**`C1`, `C2` 는 "constants" 라고만 하고 값이 없다** — 버블 크기를 수치로
환산할 수 없다. Fig. 11 은 G3C3(C/3, 37 °C)의 네 파라미터 궤적.
`[해석]` 두 그림 다 정성 비교이고 §3.1 의 표를 넘어서는 수치를 주지 않아
읽지 않았다. Fig. 16–19(부록, 전체 셀 궤적 4장)도 같은 이유로 읽지 않았다.

---

## 4. 절별 해체

### §1 서론
- 세 모드 정의: `[인쇄]` LAM_PE · LAM_NE · LLI, 참고문헌 [30–35].
- **파괴 검증의 정의를 정확히 적는다**: LAM 은 `[인쇄]` "cycling half-cells
  built using the aged electrodes" 로 정량. **LLI 는 다르다** — `[인쇄]`
  "Measuring the LLI is **more subjective** since it depends on the upper
  voltage limit the cell is run at. … the aged full-cell can be cycled to the
  maximum upper voltage limit which is typically **beyond the real use-case
  upper voltage limit**. However, doing so can **significantly damage the
  cathode material**". `[해석]` **"LLI 의 참값" 이 프로토콜 의존적이고 그것을
  재는 행위가 셀을 망가뜨린다는 진술** — 이 계보에서 LLI 정답의 주관성을
  이렇게 명시한 문장은 처음이다. 우리 합성 truth 격자의 존재 이유를 남의
  말로 적어 놓은 셈이다.
- 선행 비파괴 방법 열거: Han `[33]`(dQ/dV 봉우리 아래 면적 → LLI·LAM_NE),
  **Birkl `[31]`**(= [[birkl-ocv-degradation-diagnostic]]), Tian `[35]`(충전
  프로파일 조각 → CNN), 전기화학 모델 역산 `[38–42]`.
- PIML 선행: Karniadakis `[43]`, Storey/Aykol `[45]`, Huang MINN `[46]`,
  Wen `[47]`, Xue `[49]`, Hofmann `[50]`, Navidi `[51]`, Thelen `[30]`.

### §2 데이터셋
- **24셀 · 이식형 등급 LCO‖graphite · 4셀씩 6군 · 약 5년.**
- `[인쇄, Table 1]`

| 군 | 충전 | 방전 | 온도 | 상한 컷오프 | 셀 수 |
|---|---|---|---|---|---|
| G1 | C/3 | C/24 | 37 °C | 4.075 V | 4 |
| G2 | C/3 | C/24 | **55 °C** | 4.075 V | 4 |
| G3 | C/3 | C/3 | 37 °C | 4.075 V | 4 |
| G4 | C/3 | C/3 | **55 °C** | 4.075 V | 4 |
| G5 | C/3 | C/10 | 37 °C | 4.075 V | 4 |
| G6 | C/3 | C/24 | 37 °C | **4.175 V** | 4 |

- 하한 3.4 V. 충전은 C/3 CC-CV, 컷오프 전류 C/50.
- **RPT**: 첫 3개월 2주마다, 이후 4주마다. 절차 — ① C/3 CC-CV 로 4.075 V 까지,
  CV 컷오프 C/50 → ② **C/50 CC 방전 + C/50 CC 충전** (각각 30분 휴지) →
  ③ C/10 방전, SOC 10 % 마다 1시간 휴지. **RPT 전 챔버를 40 °C 로 맞춘다.**
- `[해석]` **반쪽전지 적합에 쓰는 곡선은 ②의 C/50 곡선**이다 (`[인쇄, §3.1]`
  "manually fitting the half-cell model parameters … to the measured C/50
  voltage curves obtained from each RPT"). 신선 전극 반쪽전지 데이터도
  C/50 으로 맞췄다. 우리 격자는 PyBaMM DFN 유한 전류이므로 **동역학 포함
  정도가 다르다.**

### §3 반쪽전지 모델 — 우리 창 모델과의 대응
- 식 (부록 A1): `V_c(Q) = V_p((Q−δ_p)/m_p) − V_n((Q−δ_n)/m_n)`,
  `dV_c/dQ = (1/m_p)·dV_p/dq_p − (1/m_n)·dV_n/dq_n`.
- `[도표, Fig. 2]` (직접 봄) — (a) `m_p q_p`, `m_n q_n` 이 각 반쪽전지 QV
  곡선의 **가로 폭**. x축 정규화 용량 −0.25 ~ 1.6 범위. (b) `δ_p`, `δ_n` 이
  각 곡선 좌단에서 `Q_c = 0` 까지의 **수평 거리**. (c) `Q_c` = 3.4–4.075 V 창
  안의 사용 가능 용량, **`LII` 는 `Q_c` 보다 넓고 PE 곡선 우단까지 뻗는다.**
- `[인쇄, §3]` `LII = Q_p − (δ_p − δ_n)`.
- `[인쇄, §3]` 저주파 근사 근거: "At low rates (≪C/10), kinetic and thermal
  effects … have minimal impact".
- **수동 적합 절차** `[인쇄, 부록 A1]`: ① dV/dQ 봉우리 정렬 ② QV 끝점 + 전체
  형상 일치. 순서가 정해져 있다 — "**First, m_n and δ_n are adjusted** to
  match the peaks on dV/dQ(Q) curves **since the negative electrodes contribute
  major peaks** in the OCV. After tuning the half-cell curve of the negative
  electrode, **m_p and δ_p are used to adjust peak magnitudes** … and line up
  the endpoints of QV curves. This fitting process is **repeated**."
  `[해석]` **사람이 좌표를 두 블록으로 나눠 번갈아 푸는 것**이며, 이것은
  좌표하강(block coordinate descent)에 사람의 사전지식으로 순서를 준 것이다.
  우리 optimizer 는 4개를 동시에 푼다. **이 순서 부여 자체가 우리가 관측하는
  degeneracy 를 그들이 덜 겪는 이유의 후보다** (미검증, 값싸게 시험 가능:
  블록 교대 최적화를 우리 격자에 붙여 보면 된다).
- **해체 검증 대상 셀** `[인쇄, §3.1]`: "For groups G1 and G3, cells C1 and C2
  were removed for analysis at **day 573**, and for groups G2 and G4, cells C3
  and C4 were removed at **day 484**." (⚠ Fig. 15 와 어긋난다 — §7)
- **Fig. 3** — §2 질문 4(c) 참조.

### §4 문제 정의
- `[인쇄]` 입력 = 측정 dQ/dV(V) 곡선, 출력 = `Q, LAM_PE, LAM_NE, LLI` 의 상태.
  실제 회귀 대상은 `[Q, m_p, m_n, LII]`.
- `[인쇄]` 학습 = 초기수명 실측 + 반쪽전지 모의 / 시험 = 말기수명 실측.

### §5 네 방법
- **PINN** — §2 질문 3 참조. 식 1–4.
- **Data augmentation** — `[인쇄]` "sampled from the entire design space of
  health parameters" 또는 "filtered to include only the highest degradation
  values". **어느 쪽을 본 실험에 썼는지 명시가 흐리다** (§6.3 은 "trained on
  data encompassing the entire simulated parameter range" 라고 적는다).
- **Delta learning (elastic net)** — 추정기(모의 데이터) + 보정기(초기수명
  실측이 학습한 편향). 최종 = 합.
- **Co-kriging** — 식 5(Matérn) · 6(`f_H = ρ f_L + f_Δ`) · 7(조건부 공분산 0
  가정) · 8·9(사후 평균·분산) · 10·11(공분산) · 12(로그주변우도). Algorithm 1
  에 5단계. `[인쇄]` "we can consider the co-kriging implementation in this
  study as a **special case of delta learning**."

### §6 결과 — §3 참조. §6.6.1 손실항 민감도:
`[도표, Fig. 12]` (직접 봄. 범례 확인: ● Q · ■ m_p · ▲ m_n · ◆ LII, y = RMSPE %)

| `r_i` | 0 (그 항 **제거**) | 0.33 (등가중) | 0.5 | 0.66 | 1 (그 항 **단독**) |
|---|---|---|---|---|---|
| `r1` (데이터항 L1) | Q2.1 · m_p7.4 · m_n7.9 · LII2.0 | **1.3 / 3.7 / 4.7 / 1.3** | 1.7/4.8/5.3/1.7 | 1.8/2.9/4.8/1.9 | 3.2/4.2/10.7/4.3 |
| `r2` (반쪽전지 대리모델항 L2) | 2.4 / 5.0 / 7.1 / 2.9 | **1.2 / 3.6 / 4.6 / 1.3** | 1.7/4.9/5.8/1.7 | 1.3/3.4/6.8/1.4 | 2.4/7.7/9.1/2.2 |
| `r3` (봉우리 위치항 L3) | 1.8 / **6.6** / 5.3 / 1.8 | **1.2 / 3.7 / 4.4 / 1.2** | 1.7/4.6/6.0/1.7 | 1.9/4.9/5.9/1.8 | 5.3/10.8/11.7/4.9 |

(값은 figure-read ≈, 눈금 4단위 사이 보간)

`[해석]` 읽을 것 셋:
- **어느 항이든 단독으로 쓰면 나빠진다** (`r_i = 1` 열이 모두 최악). 물리항
  하나만으로는 안 된다는 뜻.
- **`r3 = 0`(봉우리 위치항 제거)에서 `m_p` 가 6.6 으로 가장 크게 악화된다.**
  다른 두 항을 뺐을 때 `m_p` 는 7.4·5.0 이므로 절대적 최악은 아니지만,
  **등가중(3.7) 대비 78 % 악화**로 `m_p` 의 상대 손실이 가장 크다.
  `[해석]` **PE 정보를 dQ/dV 봉우리 *위치*가 나른다** — 우리가 아직 안 써 본
  형태의 관측이다 (우리는 dQ/dV **곡선 전체**를 목적함수에 더해 봤다).
- **`r1 = 0` — 지도학습 손실을 **완전히 빼도** `Q`·`LII` 가 ≈2 % 로 유지된다.**
  즉 물리 제약 두 개만으로 총량계 두 개는 거의 결정된다. `m_p`·`m_n` 은
  7.4·7.9 로 무너진다. `[해석]` **다시 같은 대비** — 총량은 물리가 결정하고
  전극별 분해는 라벨이 결정한다.

### §7 논의 — Table 5(정성 10축) + 방법 선택 지침. §2 질문 4(a) 참조.
- Table 5 의 **Prediction Accuracy 행은 네 방법 전부 "High"** 다.
  `[해석]` 즉 이 논문의 요약표는 **정확도로 네 방법을 구별하지 않는다.**
  구별하는 축은 구현 난이도·유연성·해석 가능성·UQ 뿐이며 전부 정성이다.

### §8 결론 + 부록 A1–A5
- 부록 A2(자동 vs 수동 적합) — §2 질문 5·6 참조. **이 논문에서 우리에게 가장
  중요한 절이다.**
- 부록 A5 + `[캡션, Fig. 20]` "Training half-cell surrogate model."
  `[인쇄]` 대리모델 `f_hc` 학습용 데이터는 각 파라미터를 **15 % 범위에서
  표준정규 표집으로 섭동**해 만든다. `[인쇄]` "train a surrogate neural
  network (f_hc) **with perfect accuracy** in mapping these values."
  `[해석]` "perfect accuracy" 에 수치가 없다 (G-공백). 그리고 **±15 % 밖으로
  네트워크 예측이 벗어나면 대리모델이 외삽 영역에 들어간다** — 말기수명
  20 % 열화를 다루면서 섭동 범위가 15 % 라는 점은 검토되지 않는다.

---

## 5. 어휘 전수 — 이 계보 열두 편째

절차: `pymupdf.get_text()` 27쪽 전체 → 합자 정규화(ﬀﬁﬂﬃﬄ, soft hyphen) →
NFKC → 소문자 → 부분문자열 계수. 전체 표는 §2 질문 4 상단.

**이 계보에서의 자리** (`[해석]`):

| 논문 | `identifiab*` | `degenerac*` | `nullspace` | `uncertaint*` | 형태 |
|---|---|---|---|---|---|
| Dubarry 2012 | 0 | 0 | 0 | 0 | 어휘 없음 · `ambigu` 3회로 축퇴 인정 |
| Birkl 2017 | 0 | 0 | 0 | 0 | 어휘 없음 · §4.2 로 축퇴 명시 |
| Wang 2025 (리뷰) | 0 | 0 | 0 | 0 | 분류 체계에 칸 없음 |
| Rhyu 2025 | 1 (참고문헌) | 0 | 1 (참고문헌) | 0 | 자기 그룹 논문을 긍정 근거로만 인용 |
| Tao 2025 | 0 | 0 | 0 | — | 제목엔 "decoupling", 정량 없음 |
| **Lin & Khoo 2024** | **26** | 0 | 0 | — | 절반만 자기 쪽으로 |
| **Schaeffer 2024** | 0 | 0 | **69** | 0 | 개념은 주제, 어휘는 자작 |
| Cui 2024 | 0 | 0 | 0 | 0 | `LLI`/`LAM` 자체를 안 씀 |
| **Navidi 2024 (이 논문)** | **0** | **0** | **0** | **21** | **★ 새 형태 — 아래** |

**★ 열두 편째의 새 형태: 불확실성 어휘는 이 계보 최다(21회)인데 그 전부가
"예측 불확실성" 이고, 식별 가능성 어휘는 0 이다.**

`[해석]` 앞의 세 형태 — ① 어휘가 통째로 없다(Dubarry·Birkl·Wang·Cui),
② 절반만 자기 쪽으로 돌린다(Lin: 추정 정밀도는 있고 비유일성은 없다),
③ 개념을 정면으로 다루며 어휘를 새로 만든다(Schaeffer) — 와 또 다르다.
이것은 **④ 불확실성 어휘를 갖췄으되 그것을 전부 출력 쪽에 쓰고 입력(라벨)
쪽에 한 번도 쓰지 않는 형태**다. `uncertainty` 21회 중 라벨·파라미터의
불확실성을 가리키는 것은 **0회**다.

**그리고 비교 논문이므로 이 침묵의 등급이 다르다** (`[해석]`): 열 개 축으로
네 방법을 등급 매기는 표(Table 5)를 만들면서 "비유일성에 대한 강건성" 축을
넣지 않았다는 것은, 개별 논문이 자기 방법을 안 잰 것과 달리 **그 축이
선택지 목록 자체에 없었다**는 뜻이다. 이 계보에서 가장 강한 형태의 침묵이라는
사용자의 예상은 **맞다 — 단, 한 가지를 빼고**: 부록 A2 가 그 현상을
**실험으로 그린다.** 즉 이 논문은 **개념 없이 현상을 만난 사례**다.

---

## 6. 그림 정직성 — 무엇을 보고 무엇을 안 봤는가

크로핑 산출물: `wiki/raw/figures/navidi2024_piml-degradation-diagnostics-comparison/`
(본문 그림 20장 `fig_1`–`fig_20` + 표 5장 `tab_1`–`tab_5`, 총 25장.
캡션 색인은 같은 폴더 `figures.json`.)

**직접 열어 본 것 — 7장** (+ 원 PDF 14쪽 하단 재렌더 1회):

| 그림 | 왜 봤나 | 본문과 어긋났나 |
|---|---|---|
| `fig_2` | 창 파라미터 기하 — 우리 α·β 대응 확정용 | 일치 |
| `fig_3` | 단독/2모드 dQ/dV 스윕 — 우리 축퇴 축 | **본문이 공통점만 서술** (§2 Q4c) |
| `fig_6` | PINN vs 기준선 구조 — 4분류 ③ 판정용 | 일치 |
| `fig_7` | 학습/시험 분할 — 공정성 판정용 | 일치 |
| `fig_8` | **본문에 없는 유일한 성능 수치** | **★ 반례 2건** (§3.1, B1·B3) |
| `fig_12` | 손실항 민감도 — 4분류 ① 정량 (범례는 PDF 재렌더로 확인) | 일치 |
| `fig_13` | 증강 vs 손실함수 ablation — 4분류 ①vs⑤ | 일치 |
| `fig_15` | **자동 적합 다중시작 산포 + 해체 검증** — 이 논문의 핵심 | **★ 반례 1건 + 미논의 불일치 2건** |

**안 본 것 — 13장.** `fig_1`(용량 감소 곡선 개요) · `fig_4`(PIML 진단 개요
도식) · `fig_5`(네 방법 도식) · `fig_9`(표본 크기) · `fig_10`(외삽 버블) ·
`fig_11`(궤적 비교) · `fig_14`(커널 민감도) · `fig_16`–`fig_19`(부록 전 셀
궤적 4장) · `fig_20`(대리모델 학습 도식). 사유: 도식 4장은 본문 서술로 충분,
성능 그림 4장은 §3.1 표를 넘어서는 수치를 주지 않으며 축이 정성이고, 부록
궤적 4장은 같은 내용의 셀별 반복이다.
**표 5장(`tab_*.png`)은 이미지로 읽지 않았다** — PDF 텍스트가 정확하다.

### 원문 내부 불일치 (원문끼리 어긋나는 것 — 우리가 판정할 수 없는 것)

| # | 어디 | 무엇 |
|---|---|---|
| I1 | `[인쇄, §3.1]` vs `[도표, Fig. 15 제목]` | §3.1 은 해체 셀이 **G1·G3 의 C1·C2 (573일)**, **G2·G4 의 C3·C4 (484일)** 이라고 적는다. Fig. 15 는 **G2C1** 과 **G1C3** 을 **1300–1400일** 지점에서 검증한다. 셀 번호도 날짜도 어긋난다 |
| I2 | `[인쇄, Table 1]` vs `[도표, Fig. 15 제목]` | Table 1 은 G2 = **55 °C**. Fig. 15 의 G2C1 패널 제목은 **"(C/24, 37 °C)"** |
| I3 | `[인쇄, §6.3]` vs `[도표, Fig. 8]` | "all the PIML methods exhibited improved error rates" ↔ co-kriging `Q` 1.37 > 0.93 |
| I4 | `[인쇄, §7.2.2]` vs `[도표, Fig. 8]` | co-kriging 용량 예측 "near-zero error rate" ↔ 1.37 % (기준선이 0.93 %) |
| I5 | `[인쇄, §7.2.1]` vs `[도표, Fig. 8]` | PINN 이 `m_p`·`m_n` 에서 우월 ↔ `m_p` 는 Data Augmentation(3.68)이 낫다 |
| I6 | `[인쇄, 부록 A2]` vs `[도표, Fig. 15]` | 수동·PINN 이 자동보다 실측에 가깝다 ↔ G1C3 `m_n` 에서 자동이 가장 가깝다 |
| I7 | `[인쇄, §6.6.1]` vs `[도표, Fig. 13]` | "PINN vs PINN + Augmentation … only marginal **increases** in error rates" ↔ `m_p` 는 증강을 빼면 4.7 → 4.2 로 **감소** |

`[해석]` I1·I2 는 표기 오류로 보이지만 **어느 쪽이 맞는지 원문으로 정할 수
없다** — Fig. 15 가 이 논문의 유일한 독립 검증이므로 그 셀의 정체가 불확실한
것은 가벼운 문제가 아니다. I3–I7 은 전부 **본문이 자기 그림보다 낙관적인**
방향이며, 예외 없이 한 방향이다.

---

## 7. 우리 프로젝트와의 접점 (요약 — 상세는 §2 질문 6)

### 우리 좌표와의 정확한 대응

| 대상 | Navidi 2024 | 우리 | 같은가 |
|---|---|---|---|
| 재구성식 | `V_p((Q−δ_p)/m_p) − V_n((Q−δ_n)/m_n)` | `V_PE((Q−β_PE)/α_PE) − V_NE((Q−β_NE)/α_NE)` | **같다** |
| 자유 파라미터 | 4 (`m_p, δ_p, m_n, δ_n`) | 4 (`α_PE, β_PE, α_NE, β_NE`) | **같다** |
| 컷오프 등식 제약 | **없다** (연성 penalty `L2` 만) | 없다 | **같다** |
| 리튬 재고 지표 | `LII = Q_p − (δ_p − δ_n)` | `LLI = (1−α_PE) + (β_PE − β_NE)` | **구조 같다** (잔량 vs 손실) |
| 곡선 | 실측 C/50 RPT (LCO‖Gr, 24셀) | PyBaMM DFN 합성 (NMC811‖Gr+Si) | 다르다 |
| 정답 | **사람의 수동 적합** (+ 해체 실측 2셀) | **합성 truth (설계값)** | **다르다 — 이것이 우리 기여의 자리** |
| 최적화 | 비선형 최적화, 초기값 5종 | multi-start, paired fixed-budget | 같은 계열 |
| 진단 | 산포 막대만 (목적함수 값 없음) | flat valley ↔ multimodal 구분, `\|err\|` 기반 판정 | **우리가 더 간다** |

### 이 논문이 우리 열린 질문에 하는 일

- **[[22p-physics-or-degeneracy]]** — Evidence For 도 Against 도 아닌
  **경계 확정 + 방법론 정박점**. 이유: (a) 셀 화학·좌표·동작점이 달라 22p 세
  숫자에 직접 닿지 않고, (b) 대신 **우리 판정 대상(4-파라미터 자동 적합)이
  야생에서 어떻게 행동하는지** 를 실측으로 준다. 그리고 Fig. 15 는 우리
  다중시작 진단의 **한계**(산포가 오차의 하한이 아니다)를 동시에 준다.
- **[[pvs-sev-lli-lampe-separability]]** — **약한 Evidence For(H1 쪽)**.
  이유: 이 논문은 관측을 **곡선 전체(dQ/dV 100점)** 로 최대한 늘린 극단
  사례인데, 그렇게 해도 `m_p`·`m_n` 은 3.7–9.9 % 로 남고 `Q`·`LII` 는
  0.55–2.1 % 로 갈린다. 곡선 안에서 관측을 늘리는 것으로는 전극별 분해가
  총량계 수준으로 좋아지지 않는다. **범위 한정 2개**: (a) 이 논문의 정답이
  사람의 적합이므로 "어렵다"의 일부는 사람의 재현성일 수 있다(G3),
  (b) `m_p`·`m_n` 궤적이 실제로 더 비단조일 수 있으므로 관측 가능성과
  궤적 복잡도가 갈리지 않는다.
- **[[fitting-degeneracy]]** — **multimodal 가지에 야생 실측 사례 1건 추가.**
  단, 목적함수 값이 없어 flat valley 와 구별되지 않는다.
- **[[interpretable-ml-battery-prognosis-taxonomy]]** — 4분류에 **칸 두 개가
  모자란다**(학습 데이터 · 라벨)는 것과, ① 손실항 ≫ ⑤ 학습 데이터 라는
  **실측 순위**.

### 값싼 후속 실험 3개 (미실행)

| # | 무엇 | 왜 | 어디서 |
|---|---|---|---|
| N1 | 우리 다중시작 해들의 **산포 vs 실제 오차** 산점도 | Fig. 15 가 우연히 드러낸 "산포는 오차의 하한이 아니다" 를 참값을 아는 곳에서 정량 | 기존 artifact 재집계 |
| N2 | **블록 교대 최적화** (`(m_n, δ_n)` → `(m_p, δ_p)` 반복, 부록 A1 순서) | 그들이 자동 적합보다 낫다고 주장하는 수동 절차의 기계판. degeneracy 가 좌표 갱신 순서에 의존하는지 판정 | `mode-observability` |
| N3 | **dQ/dV 봉우리 *위치* 2개만** 목적함수에 추가 (곡선 전체가 아니라) | 2026-08-20 의 "dQ/dV 항 추가는 개선 없음" 은 **곡선 항**이었다. Fig. 12 `r3=0` 이 위치 항은 다르다고 시사 | `degradation-degeneracy` 밖(RUN_SCOPE 불변) — `mode-observability` 에서 재구현 |

---

## 8. 비판 요약 (인용 시 반드시 붙일 것)

1. **제목이 약속하는 것보다 좁다.** "state-of-the-art methods" 는 **열화 진단
   방법**이 아니라 **하나의 진단 모델을 흉내 내는 ML 배관** 네 개다.
   EIS/DRT·전기화학 모델 역산·ICA 봉우리 진단은 도입부 열거뿐이다.
2. **정답이 사람의 적합이다.** RMSPE 는 물리적 정확도가 아니라 **사람과의
   일치도**다. 예외는 셀 2개의 해체 검증(Fig. 15)이고, 그중 2패널에서는
   세 방법 전부가 실측 바깥이다.
3. **본문에 성능 수치가 하나도 없다.** 비교 논문으로서 심각한 형식 결함이며,
   본문 서술이 자기 그림보다 낙관적인 곳이 **한 방향으로 5건**(I3–I7)이다.
4. **자기 방법에만 하이퍼파라미터 스윕이 있다.** 기준선 elastic net 의 정칙화
   세기조차 적혀 있지 않다.
5. **셀 단위 분할은 맞지만 프로토콜 단위가 아니다.** 시험 셀의 형제 3개가
   같은 조건으로 학습에 들어간다.
6. **비유일성 축이 비교표에 없다.** 열 축 중 어느 것도 "라벨의 비유일성에
   대한 강건성" 이 아니며, `identifiab*`·`degenerac*`·`nullspace`·
   `collinear*` 가 각 0회다. 그러면서 부록 A2 는 그 현상을 실험으로 그린다.
7. **인용해도 되는 것과 안 되는 것**:
   - ✅ 인용 가능 — 부록 A2 의 다중시작 서술과 Fig. 15 의 산포 크기,
     Fig. 13 의 손실항 vs 증강 순위, Fig. 12 의 항별 기여, 좌표 대응.
   - ❌ 인용 금지 — "모든 PIML 이 기준선보다 낫다", "co-kriging 의 용량
     예측이 near-zero", "PINN 이 `m_p` 에서 우월", "수동·PINN 이 자동보다
     항상 실측에 가깝다". **넷 다 자기 그림이 반증한다.**

## 관련 위키 페이지
- [[fitting-degeneracy]] · [[np-lip-ocv-reparametrization]] ·
  [[nullspace-coefficient-interpretation]] · [[birkl-ocv-degradation-diagnostic]] ·
  [[dubarry-mechanistic-mode-synthesis]] · [[interpretable-ml-battery-prognosis-taxonomy]] ·
  [[fused-lasso-feature-design-framework]] · [[22p-physics-or-degeneracy]] ·
  [[pvs-sev-lli-lampe-separability]] · [[degradation-degeneracy]] · [[mode-observability]]
