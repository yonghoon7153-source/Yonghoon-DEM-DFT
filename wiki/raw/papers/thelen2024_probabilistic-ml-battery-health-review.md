---
title: "Thelen, Huan, Paulson, Onori, Hu, Hu 2024 — Probabilistic machine learning for battery health diagnostics and prognostics: review and perspectives (npj Mater. Sustain. 2, 14)"
source_url: local-upload/35._Probabilistic_machine_learning_for_battery_health_diagnostics_and_prognostics_review_and_perspectives.pdf
source_url_note: "Review 33쪽(본문 27 + 참고문헌 233 편), SI 없음. 크로퍼 그림 18장(Fig. 2 · 9 제외 '영역 없음'); Fig. 3 · 4 는 크롭이 잘려 전체를 수동 재렌더(fig_3_full_manual.png · fig_4_full_manual.png). 본 것 5장(Fig. 3 · 4 · 7 · 13 · 15), 안 본 것은 본문 '그림' 절. 인용 원전은 열지 않았다. PDF 는 커밋하지 않는다."
source_doi: 10.1038/s44296-024-00011-1
source_license: "CC BY 4.0 (open access)"
pdf_sha256: 5ab976ae18496b268a8a044bf473fc2931cf51f44a873635bc3dda0cbd127538
ingested: 2026-09-23
sha256: eb4f313d4b5dc8211647e8677e7d75a6040539739720c78f10dd869c63a7b06a
---

# 수집 목적

`assb` 섹션 **36호**, 큐 **35번**. 닻은 `questions/assb-contact-loss-vs-lampe.md` 이고, 큐 문서
(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-d)에는 축이 **"Q3·Q4 — 불확실성 보정"** 으로, 큐 지문 표에는 "★★ 35 번이 이 다섯의 머리다 —
우리 축(열화 모드)과 불확실성 정량을 한 문서에서 같이 쓰는 첫 자료" 로 등록돼 있었다. 들어온 경로는 8호(Li et al. 2026, Frontiers 종설) digest 가 뽑은
원 논문 후보 다섯 편(큐 31~35) 중 마지막 편이다.

이 digest 의 일 (지시):

1. **(a)** aleatory / epistemic 불확실성과 **식별성**(비식별 = 사후분포가 퍼지는 구조적 원인)을 구분하는가. 확률적 ML 의 사후 폭이 우리 **근최적 폭**과 같은 대상인가, 예측 구간(35호 선례)인가.
2. **(b)** 열화 모드 진단(LLI / LAM, 전극 정렬 α·β)을 **확률적으로** 다룬 1차 원전을 제시하는가 — 베이지안 모드 추정 · 물리-정보 ML · 사후 상관(LLI ↔ LAM 축퇴가 사후 상관으로 드러나는가). Q4 와 원장 구조적 공백 1번(ASSB 역문제 · 식별성)의 후보 공급처인가.
3. **(c)** confidence interval ↔ prediction interval 구분 (35호가 넘긴 물음).
4. **(d)** ASSB 언급 여부 (없으면 도구 칸).
5. 곱 축퇴 처방 **열아홉 번째 적용**(종설이면 대상 없음도 기록). 큐 35 번 행 낱말 지문 **전체**를 NFKC · 대소문자 구분 · 낱말 경계로 재집계하고 정규화 전후 차이를 보고.

> ⚠ **형식 — *npj Materials Sustainability* Review 33 쪽(본문 27 쪽 + 참고문헌 233 편).** 1차 측정은 없다. 그림 20 장 중 데이터 그림은
> Fig. 7(합성 1D sine 예제) · Fig. 8 · 9(비공개 데이터, `[인쇄]` "not publicly available due to confidentiality reasons") · Fig. 14(Paulson 2023 재사용)뿐이고
> 나머지는 모식도다. **칸을 움직이는 근거는 1차 원전으로 확인된 명제여야 한다 — 이 편의 요약 문장만으로 칸을 올리지 않는다.**
> `[인쇄]` 는 원문 문장, `[도표]`/`figure-read ≈` 는 그림에서만 읽은 것, `[재현]` 은 원문 재료로 우리가 다시 센 것, `[해석]` 은 우리 판단이다.

# 서지

- **Adam Thelen**¹, Xun Huan², Noah Paulson³, Simona Onori⁴, Zhen Hu⁵, **Chao Hu**⁶ (교신, `chao.hu@uconn.edu`).
  ¹ Iowa State Univ. ME · ² Univ. Michigan ME · ³ Argonne (Data Science and Learning + Applied Materials) · ⁴ Stanford Energy Sci. & Eng. · ⁵ Univ. Michigan-Dearborn IMSE · ⁶ Univ. Connecticut.
- "Probabilistic machine learning for battery health diagnostics and prognostics—review and perspectives", ***npj Mater. Sustain.* 2, 14 (2024)**, `10.1038/s44296-024-00011-1`. **Review**.
- Received 2023-11-01 · Accepted 2024-02-11 · Published online 2024-06-03. **CC BY 4.0**(오픈 액세스). 경쟁 이해 "no competing interests".
- 저자 기여(`[인쇄]`): 확률 ML 방법(GPR · RVM · 앙상블) C.H. · BNN X.H. · 샘플링과 "Understanding and using predictive uncertainty" A.T. · 현장 데이터 S.O. · 조기 예측 N.P. ·
  물리 기반 · 노화 인지 제어 A.T. · 2차 수명 Z.H. + C.H. ⚠ **"Degradation diagnostics" 절(Problem 4)의 담당자는 기여 목록에 없다**(D12).
- 데이터: Fig. 7 은 교신저자에게 요청 · Fig. 8 · 9 는 비공개 · Fig. 14 는 Paulson 2023(ref 87).
- 같은 연구실의 후속 1차 논문 **Navidi, Thelen, Li, Hu 2024** (*Energy Storage Mater.* 68, 103343 — 위키 `raw/papers/navidi2024_piml-degradation-diagnostics-comparison.md`)는
  이 편에 **인용되지 않는다**(`Navidi` 0 회; 이 편 접수 2023-11 이 먼저다).

# 원문에 없어서 확인이 필요한 것

- **식별성 어휘 0**: `identifiab` 0 · `non-identif` 0 · `degenera` 0 · `ill-pos`/`ill-cond` 0 · `Fisher` 0 · `Cram` 0 · `credible` 0 · `inverse` 0 (NFKC 뒤, 본문 + 참고문헌).
  `identif*` 20 회는 전부 일상어("identifying that the anode is degrading", "ML-identified model", "identify the lithium-plating onset").
- **확률적 열화 모드 진단의 1차 원전 0** — "Degradation diagnostics" 절(p. 20)이 드는 아홉 편(Birkl · Tian · Yang · Schmitt · Han · Costa · Dubarry · Thelen 2022 · Ruan) +
  Prosser, 그리고 물리 기반 절(pp. 21–22)의 Lui · Kohtz · Pannala 중 **어느 하나에도** 불확실성 · 사후 · 구간 · 오차 막대 서술이 없다(`[재현]` 해당 두 절 안
  `uncertaint` · `posterior` · `interval` · `Bayes` 0 회). 이 편의 확률 ML 내용은 **전부 SOH 스칼라와 수명 예측**에 붙어 있다.
- **전극 정렬(offset · slippage · stoichiometry) 어휘 0** — `offset` 0 · `slippage` 0 · `stoichiom` 0. 반쪽 곡선의 "relative position and size" 만 한 번(p. 20, Birkl 요약).
- **물리 파라미터의 사후분포 0** — 사후(`posterior` 26 회)는 전부 **ML 모델 가중치** `θ` 또는 **RVM 가중치** `ω` 의 사후다. 물리 파라미터 분포는 Gasper 2021 · 2022(ref 52 · 169)의
  **부트스트랩 파라미터 분포**를 재인용한 두 문장뿐이다(p. 17).
- **ASSB 0** — `solid-state` 3 회 = 차세대 화학 목록 두 번 + 종설 두 편(ref 65 Janek & Zeier 2023 · ref 66 Lewis 2019) 안내. `contact` 1 회 = Fig. 3 상자 "Loss of electric contact". `MPa` 0.
- 원 논문 233 편은 **열지 않았다.** 아래 판정은 이 편 지면과 그림에 인쇄된 것만으로 한다.

# 판정 먼저

| 물음 | 판정 | 한 줄 근거 |
|---|---|---|
| **(a) aleatory/epistemic ↔ 식별성을 가르나 · 사후 폭은 무엇의 폭인가** | **aleatory/epistemic 은 가른다(epistemic 을 다시 model-form · parameter 로). 식별성은 없다 — 그리고 분류가 식별성의 자리를 막는다.** 사후 폭 = **예측 분포**(스칼라 SOH · 수명)의 폭, 또는 ML 가중치의 사후. 우리 근최적 폭과 **다른 대상**이다(35호 선례와 같은 층) | `[인쇄]` p. 18 "Epistemic uncertainty … is thus **reducible**" · "Model parameter uncertainty can be reduced by collecting more training data with better accuracy and under more conditions" · p. 19 "As the sample size approaches infinity, the confidence interval **collapses to the true value**". `[해석]` 구조적 비식별(곱 축퇴 · LLI ↔ LAM)은 **같은 종류의 데이터를 무한히 모아도 줄지 않는** 파라미터 불확실성이다 — 사후는 점이 아니라 **다양체(능선)**로 수렴한다. 이 편의 두 칸(비가역 aleatory · 가역 epistemic) 어디에도 그 자리가 없다. `[인쇄]` p. 18 "it is difficult to individually quantify them in practice. Instead, the predictive uncertainty output … captures the combined effects" — 출력은 **총 예측 불확실성**이다 |
| **(b) 확률적 모드 진단 1차 원전** | **0 편 — 공급처가 아니다.** 모드 진단 원전 13 편을 드는데 전부 **점 추정**으로 소개하고, 이 편 자신의 문제 그림(Fig. 4)도 Problem 4 만 **불확실성 기호 없이** 그린다 | `[도표]` Fig. 4: Problem 1 추정 용량에 **오차 막대**, Problem 2 · 3 · 5 · 6 에 **분포 곡선** — Problem 4 의 `θ̂_d` 는 **기호 하나**(청진기 아이콘, 모자 기호가 빈 상자 글리프로 깨짐). `[인쇄]` p. 20 "Altogether, these methods present a significant leap forward in the ability to non-destructively diagnose unobservable degradation modes" — 불확실성 언급 0. 사후 상관에 가장 가까운 문장은 **Ruan 2022(ref 196)**의 `[인쇄]` "the degradation modes are **inherently correlated**, and these correlations can be exploited to **improve diagnostic accuracy**" — 이것은 **학습 데이터(사전)의 상관**이지 사후 상관이 아니다(`[해석]` 3) |
| **(c) confidence ↔ prediction interval** | **가른다 — 정의 셋(CI · PI · TI)과 그림(Fig. 13)으로. 35호가 넘긴 물음의 답: Roman 의 `μ ± 2σ` 는 이 편 정의로 prediction interval 이다** | `[인쇄]` p. 18–19 CI = "precision of a distribution parameter — typically the mean … captures only the uncertainty in the predicted mean value" · PI = "the range that a single future sample … will fall within … captures both the uncertainty in the model parameters (epistemic) and the data uncertainty (aleatory)" · TI = "present and all future samples … a specified portion of the cell population". Eq. (13) `[PI_l, PI_u] = μ̂ ± Zσ̂`, Z = 1.96. ⚠ 같은 문단이 CI 를 "closely related to the **model-form** uncertainty … useful for assessing model **parameter** uncertainty" 라고도 적는다(D8) |
| **(d) ASSB** | **없다 → 도구 칸** (28 · 31 · 34 · 35호 선례) | `[인쇄]` p. 4 "solid-state batteries face challenges related to degradation of the solid electrode/electrolyte interfaces and the materials themselves" 한 문장 + 종설 안내. `[인쇄]` p. 5 "our review primarily focuses on probabilistic ML modeling methods applied to **standard Li-ion chemistries**" |
| **Q3 라벨 층위** | **칸 없음 · 층 하나: "interval taxonomy printed (CI ⊂ PI ⊂ TI) — predictive only, diagnostics drawn as point"** | 라벨 0(종설). 이 계보에서 **구간의 종류를 정의로 가른 첫 편**. 그러나 그 정의가 붙는 대상은 스칼라 예측이다 |
| **Q4 식별성** | **ASSB 0 — 칸 이동 없음(누적 0.5 = 29호 그대로).** 스물여덟 번째 성질 **"불확실성의 분류학을 세웠는데, 데이터를 더 모아도 줄지 않는 파라미터 불확실성의 칸이 없다"** | 가장 가까운 1차 원전은 **Gasper 2021(ref 52, 재인용)**: `[인쇄]` "model parameter uncertainty can be very large when certain test conditions are left out of the dataset, or when too many fittable parameters are included in the chosen model, making it difficult to identify good values for all model parameters" — **실제적 비식별의 부트스트랩 진단**이다(대수적 수명 모델, 모드 아님, 액체) |
| 채움표 | **≈16.0 → ≈16.0 (새 칸 0)** | 종설 · 1차 측정 0 · ASSB 0 · 확률적 모드 원전 0 |

# §별 해체

## 초록 · 서론 (pp. 1–3)

- `[인쇄]` 초록: "until recently, the research community has focused on deterministic modeling methods, largely ignoring the cell-to-cell performance and aging variability" ·
  "this paper reviews the current state-of-the-art probabilistic machine learning models for health diagnostics and prognostics … with a primary focus on probabilistic machine learning and uncertainty quantification".
- ★ **불확실성의 정의가 첫 쪽에서 정해진다**: `[인쇄]` p. 2 "Here, 'uncertainty' refers to the **predictive uncertainty of an ML model** … for a training/test sample point that is ideally associated with how confident the model is when predicting at this point".
  그리고 "Predictive uncertainty can be confused with prediction error. The former … is thus **known**; in contrast, the latter is **unknown** without access to the ground truth … we expect predictive uncertainty (known) to be a reliable indicator of prediction error (unknown) on a per-sample basis."
  `[해석]` 이 정의가 편 전체의 대상을 고정한다 — **표본 하나의 예측**이 얼마나 틀릴지. 파라미터 해 집합의 모양은 처음부터 대상 밖이다.
- 동기: 셀 간 편차(`[인쇄]` Baumhöfer — 같은 조건 48 셀의 수명이 "a few hundred cycles" 차이), 소표본, 팩의 최약 셀 · 보증, BMS 의 SOC/SOH 불확실성 → 충전 전력 제한.
- `[인쇄]` p. 3 한계: "it does not cover specific challenges related to emerging ML topics, such as **hybrid modeling**, transfer learning, federated learning".

## Battery degradation — modes and mechanisms (pp. 3–5, Fig. 3)

- SEI(√t, Arrhenius) · 전극 균열(`[인쇄]` "researchers found that loss of cathode active material (LAMPE) to be a primary contributor … and was strongly correlated with a cell's eventual lifetime", NCA ref 55 · NMC ref 26, 51) ·
  리튬 도금(차압 검출 Huang ref 57 · CE 스윕 Konz ref 58) · Si 팽창(두께 20 %) · Li 금속 · 고체 · LTO 가스 · Li-S · Li-air.
- ★ **Fig. 3** (`[도표]`, `fig_3_full_manual.png` 로 전체를 다시 렌더해 봤다): Level 1 Effect(Capacity fade · Power fade) / Level 2 Mode(LLI · LAM_NE · LAM_PE) /
  Level 3 Mechanism(SEI growth and decomposition · Graphite exfoliation · **Loss of electric contact** · Electrolyte decomposition · Lithium plating/dendrite formation · Electrode particle cracking) /
  Level 4 Cause(Time · High V/SOC · Low V/SOC · High temperature · Current load · Mechanical stress).
  캡션 `[인쇄]` "showing the relationship between cell use/environment (Level 4), the corresponding degradation mechanisms (Level 3), **their connections to the degradation modes (Level 2)**".
  ⚠ **그림에 연결선이 하나도 없다** — `[재현]` pymupdf `get_drawings()` 로 그림 영역의 선 객체를 세면 **2 개**(왼쪽 수직 축선 · 위 구분선)뿐이다. 원본(Birkl 2017 Fig. 1,
  위키 `raw/papers/birkl2017_degradation-diagnostics-ocv.md` §3.3)은 "Loss of electric contact" 를 **LAM_NE / LAM_PE** 로 잇는다. ⇒ 이 편의 재작도에서 접촉 손실은
  **기구 목록에만 있고 어느 모드에도 배정되지 않는다**(D1). 상자 위치는 LAM_PE 열 아래지만 위치는 연결이 아니다.
- `[인쇄]` p. 5 ASSB 관련 유일한 문장(위 (d)).

## Battery state of health (p. 5)

- `[인쇄]` "More recently … many researchers [have extended] the definition of cell SOH to include the three primary degradation modes … LAMPE, LAMNE, and LLI … provide better insight into the health of the cell's major components than do capacity and resistance".
- `[인쇄]` "While quantifying battery SOH through the various component-level degradation modes is useful in the lab, the same methods are **not necessarily useful nor viable** for cells operating in the field."

## Six problems (pp. 5–6, Fig. 4)

- 진단 = Problem 1(SOH) · 4(Degradation diagnostics), 예측 = 2 · 3 · 5 · 6.
- `[인쇄]` Problem 4: "a sub-problem of SOH estimation focused on diagnosing the degradation modes … aims to estimate **three degradation parameters** … Estimating these three degradation parameters almost always requires access to **high-precision voltage and current measurements during a full charge/discharge cycle**, but workarounds do exist".
- ★ `[도표]` **Fig. 4** (`fig_4_full_manual.png`, 확대 확인): 여섯 패널 중 **Problem 4 만 불확실성 기호가 없다**. Problem 1 의 추정 용량(보라 사각형)에는 **위아래 수염(오차 막대)**, Problem 2 · 5 는 EOL 위 분포 곡선, 3 · 6 은 궤적 띠 + EOL 분포. Problem 4 는 `θ̂_d` 글자 + 청진기 아이콘.
  캡션 `[인쇄]` "^θd denotes an estimated vector of three degradation parameters". 그림의 모자 기호는 빈 상자 글리프로 깨져 있다(D11, 표기 문제).
  `[해석]` 확률 ML 종설의 **자기 문제 지도**에서 모드 진단 칸만 점으로 그려졌다 — 지면 전체의 분포와 같다(아래 "Degradation diagnostics").

## Traditional ML vs deep learning (pp. 6–7, Fig. 5)

- 입력 형식 네 가지(V–t · I–t 특징 / dQ/dV 특징 / dV/dQ 특징 / 조합). `[인쇄]` "the same set of features that works well on a specific battery chemistry and application often does not transfer".
- `[인쇄]` "Traditional ML models are likely to perform better on small training sets (N < 1000)" · "battery aging datasets with less than 100 cells".

## Publicly available datasets (p. 7)

- CALCE · NASA · Stanford/MIT/TRI · Argonne 300 파우치(6 양극) · Sandia · Oxford · Tesla Model 3 셀 360+ · ISU 251 셀/63 조건 · Pozzato · Moy. 팩 공개 데이터 `[인쇄]` "no other publicly available battery module/pack aging datasets exist".

## Probabilistic ML pipeline (pp. 7–8, Fig. 6)

- ★ 검증 설계 권고 `[인쇄]`: "the test dataset should include a decent number (e.g., **≥30%**) of OOD samples" · "one should **avoid randomly assigning samples from the same cell to both training and test** datasets. In most cases, all samples from one cell should be exclusively assigned to a training or test dataset."
  (우리 ML 검증 체크리스트의 group 정의와 같은 방향.)
- 평가 지표 `[인쇄]`: RMSE · MAPE / "expected calibration error, Area Under the Sparsification Error curve (AUSE), and negative log-likelihood (NLL)".

## GPR (pp. 8–11, Fig. 7–9)

- 식 (1)–(6): 가우스 관측 모형 · SE 커널 · RBF-ARD · 예측 평균/분산 `σ*² = k(x*,x*) − k^T(K+σ²I)^{-1}k + σ_ε²`.
- ★ `[도표]` **Fig. 7**(합성 sine, 훈련점 8 개 — `[재현]` 그림에서 셈 8 ✓): "High epistemic uncertainty" 괄호가 **훈련점에서 먼 x 구간**(x < −4 · x ≈ 0 · x > 5)에 붙고, 95 % PI 띠가 x > 7 에서
  `σ*² ≈ σ_f² + σ_ε²` 로 포화(`figure-read ≈` 띠 ±1.3). `[해석]` 이 편의 "epistemic" 은 **입력 공간에서 데이터가 없는 곳**의 불확실성이다 — 같은 입력에서 데이터를 늘리면 사라진다.
  비식별은 **데이터가 있는 곳에서도** 남는다(같은 곡선 · 다른 파라미터). 둘은 다른 축이다.
- 응용: Richardson 2018(ref 72) · Yang(ref 95) SOH, NASA 비교(ref 98), 명시 사전 평균 함수(ref 99–101), 사용 조건 입력(ref 102–104), 하이브리드 셋(Thelen delta learning ref 101 · co-kriging ref 105 · Arrhenius/DoD 합성 커널 ref 106 = `[인쇄]` "physics-informed probabilistic ML approach").
- `[인쇄]` p. 11 delta learning: GPR 초기 RUL 은 "considerably **under-confident**", RF corrector 는 "over-confident on the original dataset, but exhibited better calibration … on the simulated OOD dataset".

## RVM (pp. 11–13, Fig. 10)

- 식 (7) 희소 베이지안 커널 회귀 — 가중치 사후의 대부분이 0 에 뾰족("relevance vectors" 5–20 %).
- `[인쇄]` p. 12 "Few research or benchmarking efforts were made to study the **quality of uncertainty quantification** … most studies worked with small datasets from limited numbers (mostly <100) of cells."

## BNN (pp. 13–14)

- 식 (9) 베이즈 · 식 (10)–(11) VI/ELBO. ★ **사후 푸시포워드 ↔ 사후 예측**의 구분 `[인쇄]`: "The set of neural network predictions represent the **posterior-pushforward** distribution that is solely due to the epistemic uncertainty in the neural network parameters. In contrast, the **posterior predictive** distribution would additionally include the aleatory uncertainty".
- ★ `[인쇄]` p. 13 "such a **mean-field** approach **cannot capture parameter correlations** and tends to **under-predict the uncertainty**". `[해석]` 3 참조 — 축퇴는 사후의 **상관(능선)**으로 나타나므로, 평균장 근사는 그것을 지운 채 좁은 주변분포를 낸다.
- ★ `[인쇄]` p. 14 "More careful analysis of the Bayesian results would be warranted, for example, by diagnosing how close the dropout posterior is to the true posterior p(θ∣x, y). This would require the **probing (at least recognition) of posterior results (not just posterior-predictive results and not just looking at RMSE of the predictions)**".
  `[해석]` 이 편에서 우리 입장("예측이 맞는다 ≠ 파라미터가 정해졌다")에 가장 가까운 문장이다. 단 `θ` 는 **신경망 가중치**이고 물리 파라미터가 아니다.
- 응용 평가 `[인쇄]`: Kim 2022(ref 137) · Xu 2022(ref 138) 는 사전 · 가능도 미기재, "The use of BNN … has been few in number and largely lacked rigorous analysis of its Bayesian uncertainty quantification".

## Neural network ensemble (pp. 14–15, Fig. 11)

- 식 (12) 가우스 혼합. 분산 출력 = aleatory, 멤버 간 차 = epistemic(Lakshminarayanan 2017, ref 143).
- ★ `[인쇄]` p. 15 "We call for coordinated efforts to promote adding the **quality of predictive uncertainty as a standard evaluation criterion** … calibration curves, sparsification curves, and negative log-likelihood … and those established in the PHM community, such as the **α-accuracy zone** and **β probability**14" — 35호(Roman)를 PHM 지표의 예로 든다. ⚠ 이름 충돌(35호 선례): `α_acc` · `β_mass` ≠ 우리 α·β.
- `[인쇄]` p. 15 "studies on SOH forecasting and RUL prediction recognize the importance of uncertainty quantification much better than studies on SOH estimation".

## Sampling methods (pp. 15–17, Fig. 12)

- 배깅 · RF(IJ 아님, 나무 간 퍼짐으로 설명) · 계층(stratified) · leave-out 샘플링.
- 35호 요약 `[인쇄]` p. 16 "Roman et al.14 … found that while the random forest model had the **lowest accuracy** of those tested, it was **overconfident** in its predictions" — ⚠ 35호 digest 대조: Group I 에서는 RF 오차가 가장 컸지만 Group II(Table 3b)에서는 RF 가 **최저 RMSPE 0.14 %** 다. 그룹 의존을 한 문장으로 일반화했다(D7).
- ★★ **Gasper 두 편 재인용** (p. 17): ① Gasper 2022(ref 169) — `[인쇄]` "By repeatedly sampling the aging dataset and fitting reduced-order models, the authors **identified distributions for each model parameter** and used the numerous sets of parameters to simulate many capacity trajectories" ·
  ② Gasper 2021(ref 52) — `[인쇄]` "uncertainty quantification via bootstrapping is an important tool during the **model-form selection** phase. The authors went on to demonstrate how **model parameter uncertainty can be very large when certain test conditions are left out of the dataset, or when too many fittable parameters are included** in the chosen model, making it difficult to identify good values for all model parameters."
  `[해석]` 이 편 전체에서 **물리(에 가까운) 파라미터의 해 집합 폭**을 말하는 유일한 자리이고, 그 도구가 **부트스트랩 파라미터 분포**다 — 우리 근최적 폭과 **같은 종류의 대상**(파라미터 공간의 퍼짐)이다. 단 ① 대수적 수명 모델(`Q = 1 − a·t^b`)의 계수이지 LLI/LAM 이 아니고 ② 액체셀 ③ 이 편은 원전의 수치를 옮기지 않았다. ⇒ **후속 1 순위 후보**(아래 표).
- ★ leave-out 샘플링 `[인쇄]` p. 17 "By repeatedly leaving out different strata and assessing model accuracy … one can map out each stratum's importance to the model fitting process and identify a subset of strata that are **essential for accurate model parameterization**".
  `[해석]` "어느 시험 조건이 파라미터를 정하나" 를 데이터 제거로 묻는 경험적 실험 설계 — 34호의 입력 설계(FIM)와 짝이 되는 **데이터 쪽** 도구다.

## Understanding and using predictive uncertainty (pp. 17–19, Fig. 13)

- ★ 분류 `[인쇄]` p. 18: 총 예측 불확실성 = aleatory + epistemic(Der Kiureghian & Ditlevsen 2009, ref 172).
  **Aleatory** — "irreducible … manufacturing process variability, inconsistency of material properties, and variations in experimental test conditions … testing more cells will not reduce the measured variability".
  **Epistemic** — "arises from an incomplete understanding or model representation of the data and is thus **reducible** … model simplification, model-form selection, computational assumptions like numerical discretization, and model parameter uncertainties" → **model-form** · **parameter** 로 세분.
  "Model parameter uncertainty can be reduced by collecting more training data with better accuracy and under more conditions, or by increasing the fidelity of the data measurements."
- `[인쇄]` "it is difficult to individually quantify them in practice. Instead, the predictive uncertainty output of probabilistic ML models captures the combined effects".
- 방법별 포착 범위 `[인쇄]`: GPR — aleatory 는 잘, "does not capture model-form and parameter uncertainty since the model is non-parametric" · 앙상블 — aleatory + parameter, model-form 은 못 · 대수적 축약 모형 + 샘플링 — model-form + parameter 를 "much better".
- ★ **구간 셋** (위 판정 (c)). `[도표]` **Fig. 13**: OLS 회귀선, 폭 순서 confidence bound(점선, 가운데에서 가장 좁고 양끝에서 벌어짐) < prediction bound(짧은 파선) < tolerance bound(긴 파선) — 본문 서술과 일치.
- Eq. (13) `μ̂ ± 1.96σ̂`; 비모수 구간은 순서 통계(Meeker ref 156).
  ⚠ `[인쇄]` "practically speaking, one can simply increase the number of bootstrap samples to a large number (>1000) to reduce the size of the intervals and achieve higher confidence levels with a narrower interval" (D9).

## Advanced topics — field data (pp. 19–20)

- `[인쇄]` "ML-based SOH algorithms developed exclusively from lab data are likely to fail" · 현장 특징은 운전 습관 의존(Pozzato ref 31) · 도메인 적응(Lu ref 177) · Deng(20 EV) · Zhang(7,296 PHEV).

## ★ Advanced topics — Degradation diagnostics (p. 20)

(이 digest 의 (b) 판정이 서는 절. 문장마다 확인했다.)

- 정의 `[인쇄]`: "the degradation modes come from **grouping degradation mechanisms based on their resulting effects on cell-level performance**".
- **Birkl 2017**(ref 71) `[인쇄]`: "experimentally verified the effects of each degradation mode on the full-cell OCV curve, providing a quantitative link between the two for the first time … the relative position and size of the positive/negative electrode half-cell curves quantify the degradation modes. This work showed that the degradation modes could be **accurately quantified** by examining full-cell OCV data, albeit through a lengthy and cumbersome curve fitting process".
  `[해석]` "accurately quantified" 는 **유일성을 전제한** 요약이다 — 우리 degeneracy 질문은 바로 이 문장이 언제 참인지를 묻는다. 이 편은 조건을 붙이지 않는다.
- OCV 재구성: Tian 2021(ref 190, CNN 으로 부분 충전 → OCV) · Yang 2021 · Schmitt 2023(ref 191–192) — `[인쇄]` "Schmitt et al.192 required **20−70% SOC** in order to guarantee accuracy in the range of **2% error on capacity estimation**" (오차 대상이 **용량**이다).
- 직접 상관: Han 2014(ref 193, dQ/dV 봉우리 면적 → LLI · LAM_NE) · Costa 2022(ref 194, IC/DV 2D 이미지 → CNN, `[인쇄]` "LFP, NMC, and NCA, achieving an average of **2% error**"). `[인쇄]` "Yet, few have studied the transferability of the model to new operating conditions outside the datasets used."
- 합성 데이터: Dubarry 2017(ref 195, 오프라인 OCV 데이터베이스 매칭 — "too large to be implemented onboard") · **Thelen 2022**(ref 81, 실험 + 모의 노화 데이터로 학습한 ML "database", 입력 = 완전지 IC 곡선) ·
  **Ruan 2022**(ref 196) `[인쇄]` "trained a deep learning model from a large body of simulated aging data, demonstrating that the degradation modes are **inherently correlated**, and these correlations can be exploited to **improve diagnostic accuracy**".
- 다른 채널: Prosser 2021(ref 197, 0 차원 발열 모델로 in-operando 모드 진단, 탭 냉각 파우치).
- 결론 `[인쇄]`: "these methods present a significant leap forward in the ability to non-destructively diagnose **unobservable** degradation modes".
- `[재현]` 이 절 안 `uncertaint` · `posterior` · `Bayes` · `interval` · `probabilist` **0 회**. 오차는 전부 **평균 백분율 오차 한 값**(2 %)이다.

## Early life and trajectory prediction (pp. 20–21)

- Fermín-Cueto 2020(SVM Platt 재보정 · RVM + conformal PI) · Gasper/NREL 부트스트랩 · Rieger 2023(RNN 앙상블 — `[인쇄]` "slightly overconfident … correctly assigned high uncertainties to longer-lived cells that were less represented").
- ⚠ `[인쇄]` "the 124 LFP cell fast-charging dataset released by Severson et al. with their pioneering **2021** paper27" — ref 27 은 2019 (D2).

## ★ Future trends — Physics-based diagnostics and prognostics (pp. 21–22, Fig. 15)

- `[인쇄]` "physics-based models … are typically parameterized only on newly manufactured battery cells".
- **Lui 2021**(ref 202) `[인쇄]`: "fit a physics-based half-cell model to the measured full-cell OCV curves to obtain **rough estimates** of the cell's present active masses (LAMPE, LAMNE) and lithium inventory (LLI) … Honkura et al.203 … popularized in later works204,205 … under a very slow charge/discharge rate (e.g., I < C/20) … used bounded empirical capacity fade models to extrapolate the degradation parameter values … many of the degradation parameter trajectories were **nearly linear** but combined to produce nonlinear degradation in the full-cell capacity fade curve".
  `[해석]` "rough estimates" 라고 인쇄하면서 그 거칠기의 크기 · 방향은 0 이다. 그리고 **외삽 대상이 모드 궤적**이다 — 모드 추정이 비유일하면 궤적의 "거의 선형" 은 **어느 분해를 골랐나**에 달린다(분해 선택이 예후로 번진다).
- `[도표]` **Fig. 15**: Degradation parameters(Cathode active mass `m_p` · Anode active mass `m_n` · Lithium inventory indicator `LII`) —(Quantify, 점선 1:1)→ Degradation modes —(Drive)→ Capacity fade.
  Step 1 "Estimate and forecast parameters" · Step 2 "Map parameters to capacity" · Step 3 "Estimate SOH or RUL". **분포 · 구간 기호 0.** `[해석]` 우리 4-파라미터 창 모델(α·β 형 스케일 · 오프셋)과 같은 좌표계의 3-파라미터판이고, 오프셋 축은 `LII` 하나에 들어가 있다.
- Kohtz 2022(ref 206, GPR 두 단: 부분 전압 → SEI 두께 → 용량) · Nascimento(ref 207) · PINN 계열(ref 208–211) · **Pannala 2024**(ref 212) `[인쇄]` "parameterized a single particle model of an NCM111 battery cell and a group of degradation-mode-specific aging models … provides insight into a cell's remaining lithium inventory (LLI) and remaining positive and negative active electrode materials".
- `[인쇄]` "leveraging physics-based models to track and identify battery aging stressors from field data … is a novel idea we have yet to see investigated".

## Second-life (pp. 22–24, Fig. 16–17)

- `[인쇄]` p. 23 "Identifying the primary degradation mechanism in the first life can significantly facilitate the safety assessment" · "The very complicated degradation mechanisms, along with their complex interactions, present substantial hurdles when it comes to degradation modeling and **identification**" — 여기서 identification 은 기구 판별의 일상어다.
- 처방 `[인쇄]`: physics-informed probabilistic ML · Battery passport · digital twins. 2차 수명 RUL 의 불확실성원에 "**degradation mechanism uncertainty**" 를 든다(정량 0).

## Aging-aware control (pp. 24–27, Fig. 18–20)

- Konz 2023(ref 229): P2D 로 도금 전압 한계 → 노화 효과는 `[인쇄]` "simulated loss of active electrode materials (LAMPE, LAMNE) by decreasing the value of the active material fraction parameter … with P2D model parameters **sampled from distributions** spanning the expected range corresponding to cells with between 85 and 100% SOH".
  ★ 이 편의 비판 `[인쇄]`: "aging was simulated by **randomly sampling the P2D model parameters, which largely ignores the path-dependence of aging**". `[해석]` 아래 "우리 프로젝트와의 접점" 2.
- `[인쇄]` p. 26 "A combination of capacity, power, and degradation mode estimation81 is required for characterizing cell SOH and prescribing the proper adjustments to the fast-charging profile."

## Conclusion (pp. 27–28)

- 도전 셋 `[인쇄]`: ① 공개 데이터(팩 · 냉각 · 시변 조건) ② "Hybrid ML and physics-based modeling … physic-informed ML methods that provide greater accuracy and **insight into degradation modes** than exist today" ③ 열 · 전기 · 기계 · 노화 결합 모델 · 디지털 트윈.
- 결론 어디에도 식별성 · 모드 분해의 유일성 · 모드 불확실성은 없다.

# 그림 — 본 것 · 안 본 것

크로퍼(`wiki/tools/extract_figures.py`)가 **18 장**을 잘랐고 Fig. 2(개요)와 Fig. 9(GPR 여섯 스냅샷)는 "영역 없음" 으로 제외했다. 크롭 두 장이 잘려 있어
(Fig. 3 은 Level 1 이 없고, Fig. 4 는 아래 줄만) 원본 쪽을 다시 렌더해 `fig_3_full_manual.png` · `fig_4_full_manual.png` 로 넣었다.

| 그림 | 봤나 | 무엇을 확인했나 | 본문과 어긋남 |
|---|---|---|---|
| **Fig. 3** (메커니즘 → 모드) | ✅ 크롭 + 전체 재렌더 + 선 객체 계수 | 4 층 상자 목록, **연결선 0**(선 객체 2 개 = 축선 · 구분선) | ⚠ **캡션은 "connections" 를 말하는데 그림에 없다**(D1) — 접촉 손실이 모드 미배정 |
| **Fig. 4** (여섯 문제) | ✅ 크롭 + 전체 재렌더 + 두 패널 500 dpi 확대 | Problem 1 오차 막대 · 2/3/5/6 분포 · **Problem 4 점(기호만)** | 모자 기호 깨짐(D11). 본문과 모순은 아니지만 "UQ 가능한 회귀기" 문장과 Problem 4 의 표현이 어긋난다 |
| **Fig. 7** (GPR 1D) | ✅ | 훈련점 8 개 ✓, "High epistemic uncertainty" 세 구간, PI 포화 `figure-read ≈` ±1.3 | 범례 "95% PI" = `μ* ± 2σ*` ↔ Eq. 13 Z = 1.96 (D4, 사소) |
| **Fig. 13** (CI/PI/TI) | ✅ (재렌더) | 폭 순서 CI < PI < TI, CI 는 가운데 가장 좁음 | 없음 |
| **Fig. 15** (물리 기반 모드 경로) | ✅ (재렌더) | `m_p` · `m_n` · `LII` → 모드 → 용량, 불확실성 기호 0 | 없음 |
| Fig. 1 · 2 · 5 · 6 · 8 · 9 · 10 · 11 · 12 · 14 · 16 · 17 · 18 · 19 · 20 | ❌ 안 봤다 | 모식도(BMS · 개요 · 파이프라인 · RVM · 앙상블 · 배깅 · 2차 수명 · 제어) 또는 비공개 데이터 GPR 예시(Fig. 8 · 9) · 재사용 그림(Fig. 14). 우리 축에 걸리는 수치가 없다고 판단 — Fig. 8 · 9 의 PI 폭 변화는 텍스트 서술만 옮겼다 | 판정 안 함 |

# `[해석]` 1 — 이 편의 분류에는 구조적 비식별의 칸이 없다

| | aleatory (이 편) | epistemic (이 편) | **구조적 비식별 (우리)** |
|---|---|---|---|
| 원천 | 제조 · 재료 · 시험 조건의 변동 | 모델 단순화 · 모델 형태 · 파라미터 · 데이터 부족 | **순방향 모델이 다른 파라미터에 같은 관측을 준다**(곱 `A_eff·ε_p/R_s` · LLI ↔ LAM 조합) |
| 데이터를 더 모으면 | 줄지 않는다(크기는 더 정확히 알게 된다) | **줄어든다**(`[인쇄]` "reducible") | **같은 종류의 데이터로는 줄지 않는다** — 사후가 점이 아니라 **능선/다양체**로 수렴 |
| 무엇이 줄이나 | 없음 | 더 많은 · 더 정확한 · 더 다양한 조건의 데이터 | **다른 종류의 관측**(전극 분해 · 기준극 · 임피던스 대역 · 온도) 또는 **모델 재구성**(묶음을 좌표로) |
| CI 의 극한 | — | `[인쇄]` "collapses to the true value" | 붕괴하지 않는다 — 능선 위 한 구간으로 남는다 |

- 이 편의 CI 정의(`n → ∞` 에서 참값으로 붕괴)는 **파라미터가 식별 가능할 때만** 참이다. 곱 축퇴에서는 FIM 이 모든 데이터량에서 특이하고, CI 는 곱 방향으로 **열린 채** 남는다
  ([[constrained-crb-identifiability]] · [[assb-lampe-contact-product-degeneracy]]).
- 이 편의 "parameter uncertainty"(epistemic 의 하위)는 비식별을 **데이터 부족 문제로 읽게** 만든다 — 34호(Liang)가 "식별성을 입력 설계로 살 수 있는 자원" 으로 인쇄한 것과 같은 방향이다.
  Gasper 2021 의 두 조건("test conditions left out" · "too many fittable parameters") 중 **앞의 것은 실제적**(데이터를 더하면 준다), **뒤의 것은 구조적일 수 있다**(파라미터를 줄여야 준다). 이 편은 둘을 한 문장에 묶는다.

# `[해석]` 2 — 사후 폭은 무엇의 폭인가

| 이 편의 "사후/구간" | 대상 | 우리 근최적 폭과 |
|---|---|---|
| GPR 예측 분산 `σ*²` | 입력 `x*` 에서의 **출력**(용량 · RUL) | 다르다 — 출력 공간 |
| RVM · BNN 가중치 사후 `p(ω∣D)` · `p(θ∣D)` | **ML 가중치** | 다르다 — 물리 의미 없는 좌표(가중치 공간의 비식별은 신경망의 대칭으로 원래 크다) |
| 앙상블 · 배깅 퍼짐 | 출력 | 다르다 |
| 사후 푸시포워드 ↔ 사후 예측 | 출력(가중치 불확실성만 ↔ + 관측 잡음) | 다르다 — 단 "**사후 자체를 보라**"(p. 14)는 요구는 우리 입장과 같다 |
| **Gasper 부트스트랩 파라미터 분포**(재인용) | **물리형 모델 계수** | **같은 종류** — 파라미터 공간의 퍼짐. 단 수명 모델 계수이고 이 편은 값을 옮기지 않았다 |

⇒ 35호의 "보정된 예측 구간 ≠ 식별성" 이 이 편에서 **정의 수준**으로 확인된다: 이 편의 불확실성은 첫 쪽부터 "표본 하나의 예측 불확실성" 으로 정의된다.

# `[해석]` 3 — "모드가 상관돼 있어 정확도가 오른다" 는 사전이 비식별을 덮는 모습이다

- Ruan 2022 의 `[인쇄]` 문장(재인용)은 **모의 노화 데이터(학습 분포)에서 모드가 상관**돼 있고, 그 상관을 쓰면 **정확도**가 오른다는 것이다.
- `[해석]` 데이터가 LLI ↔ LAM 조합의 한 방향을 못 가를 때, 학습된 회귀기는 그 방향에서 **학습 분포의 조건부 평균**을 낸다. 학습 분포가 상관돼 있으면 그 평균이
  시험 셀(같은 분포에서 뽑힌)의 참값에 가깝게 떨어진다 — 정확도가 오른다. 그러나 그 정보는 **측정이 아니라 사전**에서 왔다. 분포 밖 셀(다른 노화 경로)에서는
  그 정확도가 사라지고, 점 추정만 보고하면 **어느 몫이 사전인지 보이지 않는다**.
- 평균장 VI 에 대한 이 편의 경고(`[인쇄]` "cannot capture parameter correlations … under-predict the uncertainty")는 같은 일을 **추론 쪽**에서 말한다 — 모드 축퇴는 사후의
  상관으로 나타나는데, 평균장 근사는 그 상관을 지우고 좁은 주변분포를 낸다. ⇒ 확률적 모드 진단이 나오더라도 **공분산(또는 능선)을 보고했는지**를 먼저 본다.

# ML 검증 설계 감사 (종설 — 권고만 점검)

| 항목 | 이 편 | 판정 |
|---|---|---|
| 분할 단위 | `[인쇄]` 셀 단위 배정 권고 | ✓ (group = 셀) |
| OOD 비율 | `[인쇄]` 시험 세트 ≥30 % OOD 권고 | ✓ 권고 |
| 프로토콜 식별자 입력 | `[인쇄]` "inclusion of use condition parameters (e.g., temperature …) in the input … builds condition awareness" 를 **긍정적으로** 소개(RVM · GPR 응용) | ⚠ 조건 인식 입력과 **프로토콜 누설**의 경계를 말하지 않는다(35호의 데이터셋 표지 문제와 같은 자리) |
| 정답 축 | 모드 진단 원전들의 정답이 **measured 인지 fitted 인지** 말하지 않음(Birkl 반쪽 곡선 적합 = fitted 라벨) | ⚠ |
| UQ 평가 | ECE · AUSE · NLL · α-accuracy · β | ✓ 권고, 모드 진단에는 적용 0 |

# 어휘 집계 — NFKC 정규화 후, 대소문자 구분, 낱말 경계

본문(참고문헌 전까지) · 참고문헌 · 뒷부분(Acknowledgements 이후)을 따로 셌다. 패턴은 낱말 **시작** 경계 + 접두(`identifiab` · `uncertaint` · `Bayes` · `posterior` · `calibrat`),
약어는 양쪽 경계(`LLI` · `MPa`), 구는 사이 공백 `\s+` 허용. 추출은 pymupdf `get_text()`.

**정규화 전후 차이**: NFKC 가 바꾼 문자 **684 자** — 합자 `ﬁ` **481** · `ﬄ` 70 · `…` 50 · `ﬂ` 39 · `¼` 34(수식 글꼴의 `=` 자리) · `½` 7 · `ϕ` 2 · `ϵ` 1.
큐 지문 11 열 중 정규화로 값이 바뀌는 열은 **`confidence interval` 하나**(0 → 6)다.

**추출 부산물 둘** — 지문 차이의 실제 원인:
1. **공백 소실(글자 붙음)**: 줄 전체의 공백이 사라진 줄이 있다(예: `QuantifyingpredictiveuncertaintyinML` · `andBayesianme` · `ofposteriorresults` · `suchascalibrationcurves`).
   낱말 경계 규칙은 이것을 **못 센다**. 붙은 사례: `uncertaint` 9 · `posterior` 2 · `Bayes` 1 · `calibrat` 1.
2. **줄끝 하이픈 분철**(`uncer-⏎tainty`): 본문 `uncertaint` +10 · `degradation mode` +3 을 규칙이 놓친다.

| 큐 지문 열 | 큐 값 | 본문 (규칙) | 참고문헌 | 뒷부분 | 정규화 전 (본문) | 부분문자열 전체 | 판정 |
|---|---:|---:|---:|---:|---:|---:|---|
| `identifiab` | 0 | **0** | 0 | 0 | 0 | 0 | ✓ (대소문자 무시도 0) |
| `uncertaint` | 205 | **180** | 14 | 2 | 180 | **205** | ⚠ 큐 = **부분문자열 전체**(붙은 9 포함). 규칙대로 문서 전체 196 · 본문 180. 분철을 이으면 본문 190 |
| `confidence interval` | 0 → 6 | **6** | 0 | 0 | **0** | 6 | ✓ 6 (정규화 전 0 — 여섯 개 전부 `conﬁdence`, pp. 18–19). 대소문자 무시 8(`Confidence intervals` 2) |
| `Bayes` | 53 | **35** | 16 | 1 | 35 | **53** | ⚠ 큐 = 부분문자열(붙은 `andBayesian` 1). 규칙대로 전체 52 |
| `posterior` | 28 | **26** | 0 | 0 | 26 | **28** | ⚠ 큐 = 부분문자열(붙은 2). 규칙대로 26 |
| `calibrat` | 8 | **7** | 0 | 0 | 7 | **8** | ⚠ 큐 = 부분문자열(붙은 1). 규칙대로 7 |
| `LLI` | 5 | **5** | 0 | 0 | 5 | 5 | ✓ |
| `LAM` / `loss of active material` | 5 | **5** | 0 | 0 | 5 | 5 | ✓ 규칙상 — 그러나 **가린 값**이다: 아래 첨자가 붙어 `LAMPE` 7 · `LAMNE` 6 이 되어 `\bLAM\b` 에 안 걸린다. `LAM` 접두로 세면 본문 **18** |
| `degradation mode` | 38 | **38** | 6 | 0 | 38 | 44 | ✓ 본문 38 (분철 +3 → 41; 대소문자 무시 전체 48) |
| `contact loss` | 0 | **0** | 0 | 0 | 0 | 0 | ✓ (`contact` 1 = Fig. 3 "Loss of electric contact") |
| `MPa` | 0 | **0** | 0 | 0 | 0 | 0 | ✓ (`pressure` 2 — 일반 조건 열거) |

**결론**: 35호 digest 가 남긴 "네 열이 다르다(대소문자 · 참고문헌 차이로 보임)" 는 **절반만 맞다** — 참고문헌 포함이 한 원인이고, 나머지는 **대소문자가 아니라 공백 소실로 붙은 낱말**이다.
큐의 `uncertaint` 205 · `Bayes` 53 · `posterior` 28 · `calibrat` 8 은 모두 **부분문자열 · 문서 전체** 수와 정확히 같다(`[재현]` 205 − 196 = 9 = 붙은 수 · 53 − 52 = 1 · 28 − 26 = 2 · 8 − 7 = 1).
⇒ 큐 35 번 행을 규칙값(본문)으로 정정한다: `uncertaint` **180** · `Bayes` **35** · `posterior` **26** · `calibrat` **7** · `confidence interval` **6** · `LAM` **5(가림, 접두 18)** · 나머지 그대로.

추가 열 (본문, NFKC, 분철 이음): `epistemic` 11 · `aleator` 12 · `prediction interval` 9 · `tolerance interval` 4 · `model-form` 7 · `parameter uncertaint` 8 · `covariance` 12 · `mean-field` 5 ·
`prior` 15 · `likelihood` 11 · `correlat` 12 · `OOD`/`out-of-distribution` 10 · `expected calibration` 2 · `sparsification` 2 · `negative log` 4 · `conformal` 1 · `Markov` 1 · `Hamiltonian` 1 · `Hessian` 1 ·
`OCV` 15 · `half-cell` 11 · `physics-informed` 8(+ `Physics-informed` 1) · `impedance` 7 · `solid-state` 3 · `Li-metal`/`Li metal` 3 · `pressure` 2 · `contact` 1 ·
`identif` 20(전부 일상어) · `credible` · `Fisher` · `Cram` · `degenera` · `ill-pos` · `ill-cond` · `stoichiom` · `offset` · `slippage` · `inverse` · `PINN` **0**.

`[해석]` 본문에 `uncertaint` 180 · `posterior` 26 · `epistemic` 11 인데 `identifiab` 0 · `offset`/`stoichiom` 0 이다. **불확실성의 어휘는 이 계보에서 가장 풍부하고, 파라미터 해 집합의 어휘는 0 이다.**
35호가 "불확실성을 재면서 분해의 이름이 없다" 였다면 36호는 **"분해의 이름(`degradation mode` 38)과 불확실성의 이름(180)이 한 문서에 있는데, 한 문장에서 만나지 않는다"** — `[재현]` 모드 진단 절 · 물리 기반 절 안 `uncertaint` 0.

# Q1~Q8 판정 (닻 페이지 수집 지침)

| Q | 판정 | 근거 |
|---|---|---|
| **Q1** 접촉 손실 정량 | **없다 — `θ(N)` 0/36** | `contact` 1 = Fig. 3 상자. ★ 분류 체계 **여섯 번째 표본 "재작도가 연결을 지웠다"** — 원본(Birkl 2017)의 `Loss of electric contact → LAM_NE / LAM_PE` 연결이 이 편 Fig. 3 에서 사라졌고, 캡션은 연결이 있다고 말한다(D1) |
| **Q2** 독립 관측 | **없다** | 종설 · 1차 측정 0. Prosser 2021(발열 모델)이 전기 밖 채널로 소개되나 접촉 ↔ LAM 분리와 무관 |
| **Q3** 라벨 층위 | **칸 없음 · 층 하나: "interval taxonomy printed (CI ⊂ PI ⊂ TI) — predictive only, diagnostics drawn as point"** | 구간의 종류를 정의로 가른 계보 첫 편. 그러나 모드 진단 원전 13 편의 라벨 출처(measured/fitted)와 불확실성은 0 이고, 자기 그림에서도 Problem 4 만 점 |
| **Q4** 유일성·식별성 | **ASSB 0 — 칸 이동 없음(누적 0.5).** **스물여덟 번째 성질 "불확실성의 분류학을 세웠는데, 데이터를 더 모아도 줄지 않는 파라미터 불확실성의 칸이 없다"** | `identifiab` 0. epistemic = reducible 로 정의 · CI 는 참값으로 붕괴 — 구조적 비식별이 들어갈 자리가 정의상 없다(`[해석]` 1). 가장 가까운 것은 재인용된 Gasper 2021 의 부트스트랩 파라미터 분포(실제적 비식별 진단, 액체 · 수명 모델) |
| **Q5** Li-In 기준 전위 | **해당 없음** | 기준극 · Li-In 0 |
| **Q6** 압력 | **없다** (`MPa` 0 · `pressure` 2 = 일반 조건 열거) | 차압 도금 검출(Huang ref 57)은 액체셀 |
| **Q7** dead Li | **해당 없음** | Li 금속은 차세대 목록 한 줄 |
| **Q8** 화학·OCP | **이동 없음** | 화학 목록(LCO · NCA · NMC · LFP · Si-Gr)만, OCP 0 |

# 곱 축퇴 처방 — 열아홉 번째 적용

**적용 불가 — 대상 없음(종설, 물리 모델 0, ASSB 0).** `A_eff·ε_p/R_s` 가 들어갈 식이 이 편에 없다. 처방 단계의 입력 채널을 **이 편이 다루는 도구**로 점검만 한다:

| 처방 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| 1단계 (16호; τ 형 21호) | `R` 과 `C`(또는 τ) | EIS 특징(ref 103 · 138 · 162)이 입력으로만 등장, `C` · τ 0 | ❌ |
| 2단계 (18 · 25호) | 면적을 아는 대조군 | 0 | ❌ |
| 3단계-a (19호 `Ea`) | 여러 온도의 `R` | 온도는 **조건 인식 입력**(Arrhenius 커널 ref 106 은 용량 감쇠율용) | ❌ |
| 3단계-b · 4단계 | `C = τ/R` | 0 | ❌ |
| 31호 `R/k` | 같은 차단의 `R` · √t `k` | 0 | ❌ |

→ 처방 표에 더하는 것은 칸이 아니라 **확률 도구를 쓸 때의 경고 두 줄**(`[해석]` 1 · 3):
① **"곱 방향의 사후 폭은 데이터를 더 모아도 줄지 않는다 — 이 편의 aleatory/epistemic 분류로 그 폭을 읽지 않는다"** (reducible 로 분류하면 "데이터 부족" 으로 오독한다) ·
② **"확률적 모드 진단을 만나면 공분산/능선을 보고했는지 먼저 본다 — 평균장 VI 와 상관된 학습 사전은 둘 다 곱 방향의 폭을 지운다."**

# 어긋남 · 공백

- **D1 Fig. 3 캡션 ↔ 그림** — 캡션 `[인쇄]` "their connections to the degradation modes (Level 2)", 그림의 선 객체 2 개(축 · 구분선)뿐. 원본 Birkl 2017 Fig. 1 은 다대다 연결. **접촉 손실이 모드 미배정으로 남는다.**
- **D2** Severson "pioneering **2021** paper27" (p. 21) ↔ ref 27 *Nat. Energy* 4 (**2019**).
- **D3 절 교차참조** — "RVM applications to battery diagnostics and prognostics SOH estimation" 이 **다섯 곳**에서 다른 절을 가리키는 이름으로 쓰인다(p. 3 항목 2 = 확률 ML 절 전체 · p. 7 = Problems 4–6 이 실제로는 "Advanced topics" · p. 12 · 15 = GPR 절). 편집 자동치환 흔적으로 보인다.
- **D4** Fig. 7 범례 "95% PI" = `μ* ± 2σ*` ↔ Eq. (13) Z = 1.96 (사소).
- **D5** RBF-ARD `[인쇄]` "assigns **N** different length-scale parameters to the **N** dimensions" — N 은 훈련점 수로 정의됐다(차원은 D).
- **D6** SE 커널 `[인쇄]` "stationary and isotropic (**dimension-dependent**)" — isotropic 은 방향 무관이다.
- **D7** 35호 요약 "RF had the lowest accuracy of those tested" — Group I 에서만 참, Group II 는 RF 최저 RMSPE 0.14 %(35호 digest Table 3b).
- **D8** CI 문단 내부 긴장 — "captures only the uncertainty in the predicted mean" 과 "closely related to the **model-form** uncertainty … useful for assessing model **parameter** uncertainty" 가 한 항목에 있고, 바로 다음 항목은 parameter(epistemic) 불확실성을 **PI** 에 배정한다.
- **D9** `[인쇄]` "increase the number of bootstrap samples … (>1000) to reduce the size of the intervals" — `[해석]` 반복 수를 늘리면 **몬테카를로 오차**와 순서 통계의 여유가 줄 뿐, 부트스트랩 분포 자체(데이터가 정하는 불확실성)는 줄지 않는다. 문장이 둘을 구분하지 않는다.
- **D10** 모드 진단 원전의 **오차 대상 혼용** — Schmitt 의 "2 % error" 는 **용량** 오차, Costa 의 "2 % error" 는 모드 오차로 보이나 정의 미기재. 한 절에서 같은 "2 %" 로 병치된다.
- **D11** Fig. 4 의 `θ̂_d` 모자 기호가 빈 상자 글리프로 렌더된다(표기).
- **D12** 저자 기여 목록에 "Degradation diagnostics" 절 담당이 없다(서론은 이 절을 "three researchers actively working" 의 통찰 중 하나로 소개).
- **G1 공백** — 확률적 모드 진단 원전 0 · 모드 라벨의 measured/fitted 구분 0 · 모드 추정 오차의 정의 0.
- **G2 공백** — 물리 모델 파라미터의 사후/식별성 0 (BNN 사후는 가중치).

# 8호 원장과의 대조

8호(Li et al. 2026) digest 는 이 편을 "calibrated uncertainty" 원전 후보로 지목했다. 대조:

| 8호가 기대한 것 | 이 편 | 판정 |
|---|---|---|
| 불확실성 **보정**의 원전 | 보정을 **요구**한다(`[인쇄]` p. 15 "quality of predictive uncertainty as a standard evaluation criterion") · 도구 나열(ECE · AUSE · NLL) — 보정 **절차의 1차 시연은 없다**(35호가 그 원전) | ⚠ 요구의 종설이지 보정의 원전이 아니다 |
| 모드 × 불확실성 | 한 문서에 둘 다 있으나 **한 문장에서 만나지 않는다** | ❌ |

# 우리 프로젝트와의 접점

1. **degradation-degeneracy (22p 물음)** — 이 편은 모드 진단을 "accurately quantified by examining full-cell OCV data"(Birkl 요약)와 "2 % error"(Costa · Schmitt)로 소개한다.
   우리 프로젝트가 재는 것은 **그 문장이 참이 되는 조건**(근최적 집합의 폭이 좁은가)이다 — 이 편이 공급할 수 있는 것은 없고, **우리가 이 편 계보에 공급할 수 있는 것**이 있다:
   "점 추정 2 % 오차" 옆에 놓을 **해 집합의 폭**. 수치의 정본은 `degradation-degeneracy/docs/RESULTS*.md` 이고 여기 옮기지 않는다.
2. **합성 사전의 설계** — 이 편은 Konz 2023 을 "randomly sampling the P2D model parameters … ignores the path-dependence of aging" 으로 비판하고, Ruan 2022 의 "상관된 모드" 를 정확도의 원천으로 칭찬한다.
   `[해석]` 우리 PyBaMM truth 스윕이 모드 파라미터를 **독립으로** 까는 것은 식별성 측정에서는 **옳은 선택**이다 — 상관된 사전은 데이터가 못 가르는 방향을 사전이 대신 정해 **정확도를 올리면서 비식별을 가린다**(`[해석]` 3). 두 목적(현실적 정확도 ↔ 식별성 측정)을 섞지 않는다는 근거로 쓸 수 있다.
3. **α·β 하네스(`bms-balancing/`)** — Fig. 15 의 `m_p` · `m_n` · `LII` 는 우리 창 모델의 3-파라미터판이다(오프셋이 `LII` 하나). 하네스의 근최적 폭은 이 편 분류로는 **어느 칸에도 안 들어간다** — 하네스 문서에서 불확실성을 보고할 때 "aleatory/epistemic" 이 아니라 **"구조적 폭(데이터량 불변) ↔ 잡음 폭(데이터량에 따라 줄어듦)"** 으로 가르는 것이 맞다. 우리 폭 측정기는 잡음 수준을 바꿔 가며 폭이 줄어드는지 보면 둘을 가를 수 있다(`[해석]`, 미실행).
4. **가져올 것** — ① CI/PI/TI 정의(Fig. 13)는 요약·보고서에서 구간을 부를 때의 어휘 표준으로 쓸 수 있다 ② "사후 자체를 보라"(p. 14) 문장은 외부 인용 가능한 **입장 선례** ③ leave-out 샘플링 = "어느 시험 조건이 파라미터를 정하나" 의 경험적 판 — 하네스의 프로토콜 비교와 같은 물음.

# 후속 (인용 원전 — 제목 기준, 미열람)

★ **이 편은 확률적 모드 진단의 1차 원전을 하나도 제시하지 않는다.** 아래는 모드 진단 원전 전체(확률 여부 미확인)와, 파라미터 퍼짐을 다룬 원전이다. 큐 36 · 37 은 인용되지 않는다.

| 서지 | ref | 왜 | 축 |
|---|---|---|---|
| **Gasper, Gering, Dufek, Smith 2021** *JES* 168, 020502 "Challenging practices of algebraic battery life models through statistical validation and model identification via machine-learning" | 52 | ★ 이 편에서 유일하게 **파라미터 불확실성이 커지는 조건**(조건 누락 · 파라미터 과다)을 부트스트랩으로 보인 원전 — 실제적 ↔ 구조적 비식별을 가를 재료가 있는지 | **Q4 도구** |
| **Gasper, Collath, Hesse, Jossen, Smith 2022** *JES* 169, 080518 "Machine-learning assisted identification of accurate battery lifetime models with uncertainty" | 169 | 파라미터 분포 → 궤적 퍼짐 — 폭 측정기의 수명 모델판 | Q4 도구 |
| **Thelen et al. 2022** *Energy Storage Mater.* 50, 668 "Integrating physics-based modeling and machine learning for degradation diagnostics" | 81 | 이 편 저자의 모드 진단 원전 · Navidi 2024(위키에 있음)의 `[30]`. 확률 출력 여부 미확인 — **확률적 모드 진단의 가장 가까운 후보** | Q3 · Q4 |
| **Ruan, Chen, Ai, Wu 2022** *Energy AI* 9, 100158 "Generalised diagnostic framework for rapid battery degradation quantification with deep learning" | 196 | "모드가 상관돼 있다 → 정확도 향상" 의 원전 — 학습 사전의 상관 구조와 비식별 방향의 관계(`[해석]` 3)를 확인할 곳 | **Q4 · 22p** |
| Dubarry et al. 2017 *JPS* 360, 59 "State of health battery estimator enabling degradation diagnosis" | 195 | OCV 데이터베이스 매칭 — 매칭의 다중 해를 보고하는지 | Q4 |
| Costa, Sánchez, Anseán, Dubarry 2022 *J. Energy Storage* 55, 105558 "degradation modes diagnosis via CNN" | 194 | "2 % error" 의 정의 · 합성/실측 라벨 | Q3 |
| Schmitt, Rehm, Karger, Jossen 2023 *J. Energy Storage* 59, 106517 "Capacity and degradation mode estimation … partial charging curves at different current rates" | 192 | 부분 창(20–70 % SOC)에서의 모드 추정 — α·β 하네스의 "창 하나" 하한 질문과 같은 물음 (⚠ 위키의 `schmitt2022_sic-ocp…` 와 다른 편) | Q4 · 하네스 |
| Tian, Xiong, Shen, Sun 2021 *Energy Storage Mater.* 37, 283 "Electrode ageing estimation and OCV reconstruction" | 190 | 부분 충전 → OCV → 전극 노화 | Q4 |
| Lui et al. 2021 *JPS* 485, 229327 "Physics-based prognostics of implantable-grade Li-ion" | 202 | "rough estimates" 의 크기 · 모드 궤적 외삽 (Navidi 2024 digest 의 `[55]` Lui 2021 과 같은 편으로 보인다) | Q3 · 22p |
| Pannala, Movahedi, Garrick, Stefanopoulou, Siegel 2024 *JES* 171, 010532 | 212 | SPM + 모드별 노화 모델 · 두께 채널 — 두께가 LLI ↔ LAM 을 가르는 독립 관측인지 | Q2 도구 |
| Prosser, Offer, Patel 2021 *JES* 168, 030532 "first quantitative in-operando technique for diagnosing degradation modes" | 197 | 발열 채널 — 전기 밖 관측 | Q2 도구 |
| Li et al. 2021 *JPS* 506, 230034 "PINN for electrode-level state estimation" | 208 | 전극 수준 PINN — 사후/식별성 여부 | Q4 |
| Nemani et al. 2023 *MSSP* 205, 110796 "UQ in ML for engineering design and health prognostics: a tutorial" | 34 | 이 편이 방법 상세를 넘기는 튜토리얼(p. 8 · 9 · 12 · 15) — 식별성 절이 있는지 | 어휘 |
| Der Kiureghian & Ditlevsen 2009 *Struct. Saf.* 31, 105 "Aleatory or epistemic? Does it matter?" | 172 | 분류의 원전 — 구조적 비식별을 어디에 두는지 | 어휘 |
| Janek & Zeier 2023 *Nat. Energy* 8, 230 · Lewis et al. 2019 *Trends Chem.* 1, 845 | 65 · 66 | 이 편의 유일한 ASSB 안내 (종설) | 계보 |
