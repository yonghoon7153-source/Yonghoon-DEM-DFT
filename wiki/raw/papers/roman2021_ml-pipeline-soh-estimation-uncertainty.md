---
title: "Roman, Saxena, Robu, Pecht, Flynn 2021 — Machine learning pipeline for battery state-of-health estimation (Nat. Mach. Intell. 3, 447-456)"
source_url: local-upload/34._Machine_learning_pipeline_for_battery_stateof-health_estimation.pdf
source_url_note: "본문 10쪽 + SI 18쪽(34._Sup_…pdf). 공개 데이터(CALCE·NASA·TRI·Oxford)와 zenodo 코드(10.5281/zenodo.4390152)는 열지 않았다. 크로퍼 그림 18장 + 표 11장; 본문 Fig. 2·4·5 는 크로퍼가 놓쳐 수동 크롭, Fig. 1 은 재크롭. 본 것 9장(본문 Fig. 1–5 전부 · SI Fig. 4·8·10 · SI Table 2 쪽), 안 본 것은 본문 '그림' 절. PDF 는 커밋하지 않는다."
source_doi: 10.1038/s42256-021-00312-3
source_license: "(c) The Author(s), under exclusive licence to Springer Nature Limited 2021 — 오픈 액세스 아님"
pdf_sha256: efab9d462848d75f158e71aef2bd16c62ded07db5be15caa05c5642dc8347549
si_pdf_sha256: b856d5919e0a8b6ad9997c8d899c1f6b0a0a0b263c23d6b44fe9dd5330169ddc
ingested: 2026-09-23
sha256: cc274c87fc34b125761486b97b7aec4b26fdae61ae5ea5298ede120947252811
---

# 수집 목적

`assb` 섹션 **35호**, 큐 **34번**. 닻은 `questions/assb-contact-loss-vs-lampe.md` 이고, 큐 문서
(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-d)에는 축이 **"Q3 — 08 Table 2 여덟 행 중 유일하게 신뢰구간을 보고"** 로 등록돼 있었다.
들어온 경로는 8호(Li et al. 2026, Frontiers 종설) digest 가 Table 2 의 `Uncertainty output` 열에서 **"Confidence interval reported" 한 행**의
원전으로 이 편을 지목한 것이다(8호 digest 후속 표 6번). 33·34호 에이전트가 "34번이 실제 Q3 논문" 이라고 다시 짚었다.

이 digest 의 일 (지시):

1. **(a)** SOH(용량) 스칼라 하나만 추정하는가, 열화 모드(LLI/LAM)를 가르는가. 스칼라면 우리 문제(모드 분할)와 **차원이 다름**을 명시.
2. **(b)** 특징이 α·β(전극 스케일·오프셋)의 함수인가 — 특징 공간에서 LLI ↔ LAM 이 축퇴하는지 논문이 다루는가.
3. **(c)** 불확실성 표현이 **식별성(Q4) 명제**인가, **예측 오차 보정**인가 — 구분해서 판정.
4. **(d)** 학습·검증 데이터가 합성인가 실측인가, 역범죄(같은 모델로 만든 데이터) 여부 — Q3 층(28호 '역범죄' 선례).
5. ASSB 여부(없으면 도구 칸). 곱 축퇴 처방 **열여덟 번째 적용**. 큐 낱말 지문을 **NFKC 뒤 · 대소문자 구분 · 낱말 경계**로 재집계.
6. 큐 지문 표 **35번 행 `confidence interval`** 을 35번 PDF 에서 직접 재확인(34호 에이전트 발견: 0 → 6).

> ⚠ **형식 — *Nature Machine Intelligence* Article 10 쪽 + SI 18 쪽.** 1차 **실험은 없다** — 공개 데이터 네 묶음(CALCE · NASA · TRI · Oxford)을
> 다시 쓴 **ML 방법 논문**이다. 셀은 전부 **액체 전해질 상용 셀**(LCO · LFP · LCO/NMC)이다. 이 digest 의 `[인쇄]` 는 원문 문장,
> `[도표]`/`figure-read ≈` 는 그림에서만 읽은 값, `[재현]` 은 원문 숫자로 우리가 다시 계산한 값, `[해석]` 은 우리 판단이다.

# 서지

- **Darius Roman**¹ (교신, `dvr1@hw.ac.uk`), Saurabh Saxena²·⁴, Valentin Robu¹·³·⁵, **Michael Pecht**², David Flynn¹.
  ¹ Heriot-Watt Univ. Smart Systems Group · ² Univ. Maryland **CALCE** · ³ TU Delft Algorithmics · ⁴ 현 Argonne · ⁵ 현 CWI Amsterdam.
- "Machine learning pipeline for battery state-of-health estimation", ***Nat. Mach. Intell.* 3, 447–456 (May 2021)**, `10.1038/s42256-021-00312-3`. **Article**.
- Received 2020-05-18 · Accepted 2021-01-28 · Published online 2021-04-05. © Springer Nature (exclusive licence) — **오픈 액세스 아님**.
- 연구비: Lloyd's Register Foundation · EPSRC (CDT Embedded Intelligence, CESI) · Baker Hughes · InnovateUK ReFlex. 경쟁 이해 "no competing interests".
- 코드: 모델링 코드 zenodo `10.5281/zenodo.4390152`(**열지 않았다**) · 데이터 처리 코드는 "available … upon request".
- ⚠ **자기 데이터**: 네 데이터 묶음 중 CALCE 셋은 공저자 소속(Pecht · Saxena = CALCE)의 공개 자료다. 저자 스스로 새로 측정한 셀은 0.

# 원문에 없어서 확인이 필요한 것

- **열화 모드 어휘 0**: `LLI` 0 · `LAM` 0 · `loss of active material` 0 · `degradation mode` 0 (본문 + SI, NFKC 뒤). `stoichiom*` 0 · `OCV`/`open circuit` 본문 1(참고문헌 제목뿐) · SI 0.
  → 이 편은 **용량 하나**를 추정한다. 무엇이 용량을 줄였는지(리튬 손실 · 활물질 손실 · 저항)는 **묻지 않는다**.
- **식별성 어휘 0**: `identifiab` 0 · `Fisher`/`Cramér`/`Hessian`/`profile` 0. `identif*`(대소문자 무시) 3 회 = "identified in the Group I dataset" 1 + 참고문헌 제목 2.
- **라벨 불확실성 0** — 정답(`True capacity`)은 전 사이클 방전 용량의 **측정값**이고 그 측정 오차를 쓰지 않는다. 훈련 라벨만 RANSAC 으로 **이상치 제거**(SI Note 4), 시험 라벨은 그대로.
- **온도 0** — 입력에도 없다. `[인쇄]` "Temperature variations during charging could further introduce uncertainty … Possible mitigation includes the use of temperature as an input" (향후 과제).
- **데이터셋 밖 시험 0** — 모든 시험 셀이 훈련 셀과 **같은 데이터 묶음·같은 조건군** 안에 있다(`extrapolat*` · `out-of-distribution` 0). 전이 학습은 "can be used" 로 **제안만**.
- **합성 데이터 0** — P2D 합성 데이터는 `[인쇄]` "we believe future work must incorporate synthetic data" 로 **제안만**.
- **셀별 시험 결과표 0** — 그룹 평균(Tables 2b·3b·4b)과 "무작위로 고른" 셀 하나씩(38 · 1 · 5)만 인쇄. Group I 시험 셀 18–19 개, Group II 51 개의 분포는 없다.
- 네 원 데이터 묶음과 zenodo 코드는 **열지 않았다**. 아래 판정은 지면 + SI 에 인쇄된 것만으로 한다.

# 판정 먼저

| 물음 | 판정 | 한 줄 근거 |
|---|---|---|
| **(a) 무엇을 추정하나** | **용량(Ah) 스칼라 하나 — 모드 분할 0. 우리 문제와 차원이 다르다(1 ↔ ≥3)** | `[인쇄]` "This work focuses on the battery's **capacity** as its health indicator" · 식 (1) `SOH = C_i/C_1` · SI Table 2 `Target variable = Discharge Capacity [Ah]`. 그림 축도 전부 `Capacity (Ah)`. `LLI`·`LAM`·`degradation mode` **0**. 우리 물음(LLI · LAM_PE · LAM_NE 분할의 유일성)은 **이 편의 목표 변수 안에 자리가 없다** — 세 모드가 같은 용량 감소를 내면 이 편에게는 **같은 정답**이다 |
| **(b) 특징이 α·β 의 함수인가 · 특징 공간 축퇴를 다루나** | **`[해석]` 그렇다(충전 상단 0.3 V 구간의 범함수) — 그러나 논문은 다루지 않는다** | 특징 30 개 = 충전 CC 전압 구간 `[V_l, V_h]`(`ΔV = 0.3 V`, SI Note 2) · CV 전류 구간 `[I_l, I_h]`(40 % 강하) 의 **시간 · 에너지 · 기울기 · 왜도 · 첨도 · 엔트로피 · Hausdorff · Fréchet** + 이력(누적 방전 용량·에너지) + 셀 식별값(정격 용량 · 충전 전류). `[해석]` 완전지 곡선 상단 구간이므로 **양극 α·β 와 음극 α·β 의 함수**이고 분극(`R·I`)이 겹친다. 저자의 물리 귀속은 SI Note 1 의 **"가설"** — 흑연 음극 분극 · 리튬 도금 → CCCT 감소 · CVCT 증가. 모드 축퇴 · 전극 귀속 검사 **0**. ⚠ **이름 충돌**: 이 편의 "α-accuracy · β" 는 **예측 정확도 띠(±1.5 %)와 그 띠 안의 확률 질량**이지 우리 전극 스케일·오프셋이 아니다 |
| **(c) 불확실성은 식별성 명제인가** | **아니다 — 예측 오차 보정이다(그것도 계보 첫 "보정 절차 + held-out 적중률 검사")** | 산출 = 예측 분포 `N(μ, σ²)` · 표시 = `μ ± 2σ`("95 % quantile"). 보정 = **보정 전용 셀**(5 · 10 · 1 개)에 isotonic regression · 평가 = 시험 셀의 **90 % 구간 적중률 `C_score`** + sharpness · α-accuracy · β · PEP. 불확실성의 대상은 **스칼라 예측**의 오차이고, 파라미터 · 분해 · 조합의 **비유일성**은 대상이 아니다. `[해석]` 분해가 없으니 식별성이 물을 자리 자체가 없다. 35번(Thelen 2024) 정의로는 이 편의 "confidence interval" 이 기능상 **prediction interval** 이다(측정 라벨의 산포까지 덮도록 보정) |
| **(d) 데이터 · 역범죄** | **전부 실측 공개 데이터 — 역범죄 없음. 대신 다른 층의 누설 둘** | CALCE CS2/CX2/PL · NASA 5/11 · TRI(Severson) · Oxford(Birkl). 분할 단위 = **셀**(훈련 · 보정 · 시험 셀이 겹치지 않음 — Group II 목록 `[재현]` 교집합 0). ⚠ ① **셀·데이터셋 식별값이 입력**: Group I 선택 특징 18 개에 `Nominal Capacity [Ah]` · `Charge Current [A]` — 다섯 데이터 묶음이 섞인 Group I 에서 이 둘은 **데이터셋 표지**다. ② **이력 특징 = 과거 측정 라벨의 합**: `Lagged Cumulated Discharge Capacity` 는 시험 셀 자신의 **이전 사이클 측정 용량의 누적**이다 — Stage 2 의 `[인쇄]` "under the assumption that the battery cell has **unknown capacity**" 와 긴장. Group III 선택 5 개 중 **3 개가 이력**. 합성 augmentation 은 FGSM 적대 예(특징 범위의 1 %) 뿐 |
| **Q3 라벨 층위** | **칸 이동 없음 · 층 하나: "measured scalar label + held-out-recalibrated predictive interval (coverage audited)"** | 라벨 = 측정 방전 용량(훈련만 RANSAC 세척) · 오차 막대 = 모델 예측 구간, **보정 셀에서 맞추고 시험 셀에서 적중률을 잰다**. 계보에서 **오차 막대가 맞는지를 held-out 데이터로 검사한 첫 편**. 그러나 라벨 자체의 불확실성 0 · 모드 라벨 0 · ASSB 0 → 카드 Q3(접촉 손실 ↔ LAM 라벨)의 칸은 못 채운다 |
| **Q4 식별성** | **ASSB 0 — 칸 이동 없음(누적 0.5 = 29호 그대로).** 스물일곱 번째 성질 **"불확실성을 보정했다 — 분해가 없는 스칼라 위에서"** | 계보에서 불확실성을 **가장 제대로** 다룬 편(보정 · 적중률 · 날카로움 · 조기 예측 비율)인데, 그 모든 도구가 **목표가 스칼라일 때만** 닫힌다. 적중률 90 % 는 "용량 예측이 맞는다" 이지 "용량을 줄인 원인이 정해진다" 가 아니다 |
| **ASSB** | **없다 → 도구 칸** (28 · 31 · 34호 선례) | `solid` 1 회 = 참고문헌 저널명 "Electrochem. Solid State Lett." · `pressure` 0 · `MPa` 0 |
| **8호 Table 2 대조** | ★★ **8호 원장 두 곳이 이 원전과 어긋난다** | ① 8호 `[재현]` "보정된 불확실성 **0/8** · 신뢰구간 보고(보정 여부 불명) 1/8" → 원전은 **isotonic 재보정 + 보정 전용 셀 + 적중률 표**를 인쇄한다. **보정된 불확실성은 1/8** 이다. ② 8호 "RMSE 0.45 % (best fast-charge deployment)" → 0.45 % 는 **RMSPE** 이고 **dNNe** 의 값이다. 같은 표의 최저는 **RF 0.14 %**(Table 3b). 초록의 "the best model" 부터 어긋난다(D2) |
| 채움표 | **≈16.0 → ≈16.0 (새 칸 0)** | 모드 0 · ASSB 0 · 식별성 0. Q3 은 층 하나 |

# §별 해체

## 초록 (p. 447)

`[인쇄]` "we design and evaluate a machine learning pipeline for estimation of battery **capacity fade**—a metric of battery health—on **179 cells**
cycled under various conditions. The pipeline estimates battery SOH with an associated **confidence interval** by using **two parametric and two
non-parametric** algorithms. Using segments of charge voltage and current curves, the pipeline engineers **30 features**, performs automatic
feature selection and **calibrates** the algorithms. When deployed on cells operated under the fast-charging protocol, **the best model achieves a
root-mean-squared error of 0.45%**."

- "two parametric and two non-parametric" — 본문에서 네 알고리즘은 BRR · GPR(베이지안) · RF · dNNe(빈도주의 앙상블)로 나뉜다. 어느 둘이 모수형인지는 본문이 다시 말하지 않는다.
- ⚠ "best model … 0.45 %" — D2 참조. 그 값은 **dNNe** 의 **RMSPE** 이고 Group II 최저는 RF 0.14 % 다.

## 서론 (pp. 447–448)

- SOH 정의: `[인쇄]` "SOH is a parameter that quantifies the general condition of a battery … measured as **capacity or impedance** … This work focuses
  on the battery's capacity". → 임피던스 쪽 SOH 는 **버렸다**.
- 기존 방법 분류: 등가회로 · 전기화학 · 데이터 기반. ECM 파라미터 추출에는 `[인쇄]` "pulse discharging and electrochemical impedance
  spectroscopy is typically necessary … not a viable solution for online applications".
- **IC/DV 비판**: `[인쇄]` "The differentiation of the capacity−voltage curve … amplifies noise … restricted to low charge current rates (1/5 to 1/25
  C-rate)" → 미분 없이 **원 곡선 구간**에서 특징을 뽑겠다는 동기. IC/DV 를 "a method developed for the analysis of cell ageing mechanisms"(ref 23,
  Birkl 2017)라고 적는다 — **그 방법이 원래 모드 분해용이었다는 것을 알고, 목표를 용량으로 좁혔다.**
- GPR 비판(Richardson 2018 ref 32): 느리고 입력 구간 선택에 민감. SVR(Wang ref 36): 불확실성 없음.
  `[인쇄]` "SOH assessment without corresponding measures of uncertainty … does not provide sufficient information to form a decision" — 이 편의 동기 문장.
- 기여 주장: `[인쇄]` "BHUMP is more accurate than conventional methods as the battery ages, uses a set of engineered features **capable of capturing
  battery intrinsic degradation**, and is capable of estimating cell SOH in **under 15 min** at any point in its life cycle." → "intrinsic degradation" 을
  **무엇으로** 검증했는지는 지면에 없다(SI Note 1 은 "hypothesis").

## Machine learning pipeline approach (p. 448)

- 문제 설정: `[인쇄]` "a multivariate supervised regression problem". 두 단계 — Stage 1 오프라인(특징 · augmentation · 선택 · 학습 · **불확실성 보정**),
  Stage 2 온라인(`[인쇄]` "under the assumption that the battery cell has **unknown capacity**").
- 특징: 도메인 지식 기반 수작업 특징. `[인쇄]` "We also provide a **hypothesis** for the underlying physical degradation quantified by the selected
  segments … in Supplementary Note 1." → 물리 귀속의 층위는 **가설**이다.
- 선택: RF-RFE-CV (Guyon 2002 의 SVM 을 RF 로 바꿈), 30 → 18 / 5 / 5.
- **augmentation**: FGSM 적대 예 + weight decay. 동기 `[인쇄]` "to **ameliorate the differences in battery design or chemistry** … robust to outliers,
  prevents overfitting and **reduces distribution variance around the estimated mean**". `[인쇄]` "Synthetic data generation generated from
  electrochemical models like the pseudo-two-dimensional model … can also be regarded as a data augmentation policy … we believe future work must
  incorporate synthetic data as well."
- 네 알고리즘: RF(infinitesimal jackknife 신뢰구간, ref 49) · dNNe(Lakshminarayanan 2017 deep ensemble, ref 50) · BRR · GPR.
- 하이퍼파라미터: random search, **"batch cross-validation … where each batch is represented by one cell"** — 셀 단위 묶음 CV(= leave-one-cell-out 형).
- 평가: 먼저 **재보정**, 그 다음 MAPE · RMSPE · 불확실성 지표.

## Dataset (p. 449, Table 1)

| 데이터 | 그룹 | 제조사 | 양극(`[인쇄]` "Information from manufacturer, not verified") | 폼팩터 | 셀 | 충전 | 방전 |
|---|---|---|---|---|---:|---|---|
| CALCE CS2 | I | Unknown | LiCoO₂ | Prismatic | 6 | CC−CV | 2 regimes |
| CALCE CX2 | I | Unknown | LiCoO₂ | Prismatic | 6 | CC−CV | 2 regimes |
| CALCE PL | I | Unknown | LiCoO₂ | Pouch | 2 | CC−CV | 1 regime |
| NASA 5 | I | LG Chem | LiCoO₂ | 18650 | 8 | CC−CV | 2 regimes |
| NASA 11 | I | LG Chem | LiCoO₂ | 18650 | 25 | CC−CV | 7 regimes |
| TRI | **II** | A123 | LiFePO₄ | 18650 | 124 | **Fast-charging** | 1 regime |
| Oxford | **III** | Kokam | LiCoO₂/LiNiMnCoO₂ | Pouch | 8 | **CC** | 1 regime |

합계 47 + 124 + 8 = **179** `[재현]` ✓. ⚠ 같은 쪽 본문 첫 문장은 Group II = CC(124), Group III = 2-step fast-charging(8) 으로 **뒤바꿔** 적는다(D1).
이후 본문 · Table 1 · SI 는 전부 II = TRI 급속충전, III = Oxford CC 다.

## Group I (pp. 449–450, Fig. 2, Table 2)

- 선택 특징 **18/30**(SI Fig. 8a · Table 3). 임계 `V_h = 4.2 V`, `V_l = 3.9 V`.
- 예시 셀 **38**: `[인쇄]` "a randomly chosen **pouch** cell battery, cell number 38 … cycled in full depth of discharge between 4.2 V and 2.7 V at a
  discharge C-rate of **0.5 C (or 0.55 A)** with a CC−CV charging protocol at a current value of 0.5 C-rate". ⚠ D5.
- `[인쇄]` "all figures display a confidence level equivalent to a **95% quantile, that is μ ± 2σ**".
- Table 2 (전사):

| | MAPE | RMSPE | `C_score` | Sh | α-accuracy | β | PEP |
|---|---:|---:|---:|---:|---:|---:|---:|
| **a 셀 38** BRR | 1.52 | 2.49 | 84.49 | 0.021 | 70.00 | 0.57 | 68.92 |
| GPR | 1.49 | 2.24 | 92.23 | 0.025 | 65.00 | 0.48 | 71.76 |
| RF | 0.72 | 0.91 | **100** | 0.046 | 92.00 | 0.29 | 95.29 |
| dNNe | 0.65 | 0.92 | 88.01 | 0.0082 | 93.00 | 0.93 | **97.71** |
| **b Group I 평균** BRR | 4.65 | 5.54 | **89.16** | 0.104 | 25.76 | 0.25 | 36.57 |
| GPR | 3.70 | 4.51 | 83.62 | 0.089 | 32.04 | 0.29 | 60.07 |
| RF | **2.17** | **2.70** | 54.70 | 0.093 | 35.94 | 0.36 | 65.47 |
| dNNe | 3.30 | 4.26 | 86.28 | 0.043 | 32.14 | 0.58 | 63.26 |

- `[재현]` **Group I 평균 α-accuracy 는 26–36 %** — 예측의 **3 분의 2 이상이 ±1.5 % 띠 밖**이다. 평균 RMSPE 2.7–5.5 %. 초록의 0.45 % 는 Group II 다.
- `[인쇄]` "RF achieves, on average, a **low calibration error of 54.70%**" → 그 다음 문장에서 "it does not output well-calibrated predictions" (D8).
- `[인쇄]` "the dNNe outputs a well-calibrated model, with on average **less than 4% below the ideal calibration score**" — `[재현]` 90 − 86.28 = 3.72 ✓.
  ⚠ 그런데 같은 표에서 **BRR 89.16 이 90 에 가장 가깝다**(D21).

## Group II (pp. 450–451, Fig. 4, Table 3)

- 124 셀 전부 **4 C 방전**, 72 개 급속충전 정책(SI Note 4). 특징은 80 % SOC 이후의 CC−CV 구간(SI Fig. 2). 선택 **5/30**
  (Table S4: CC 구간 에너지 · 에너지 차 · Hausdorff · Shannon 엔트로피 · Fréchet). `[인쇄]` "We believe this is caused by the fact that the dataset
  incorporates only one discharge profile as well as just a single battery type."
- 예시 셀 1: `[인쇄]` "We selected cell 1 … when there is a **high number of outliers** in capacity data".
- Table 3 (전사):

| | MAPE | RMSPE | `C_score` | Sh | α-accuracy | β | PEP |
|---|---:|---:|---:|---:|---:|---:|---:|
| **a 셀 1** BRR | 0.72 | 0.90 | 65.49 | 0.005 | 89.00 | 98.00 | 20.70 |
| GPR | 1.23 | 1.63 | 69.94 | 0.011 | 65.00 | 85.00 | 22.16 |
| RF | 0.23 | 0.43 | 87.42 | 0.002 | 98.00 | 100 | 42.81 |
| dNNe | 0.34 | 0.48 | 71.31 | 0.002 | 98.00 | 100 | 31.50 |
| **b Group II 평균** BRR | 0.45 | 0.76 | 91.72 | 0.005 | 97.31 | 99.19 | 62.86 |
| GPR | 1.00 | 1.91 | 93.14 | 0.012 | 90.43 | 83.74 | 63.21 |
| RF | **0.11** | **0.14** | 79.72 | 0.001 | 99.84 | 99.96 | 58.77 |
| dNNe | 0.23 | **0.45** | **91.02** | 0.002 | 99.53 | 99.50 | 53.41 |

- `[인쇄]` "All models are able to estimate the SOH with less than 2% **RMPSE**" (오탈자) · "In terms of calibration error, dNNe achieves the closest score to a
  90% confidence interval, with 91.02%" — `[재현]` |91.02 − 90| = 1.02 < BRR 1.72 < GPR 3.14 < RF 10.28 ✓.
- ⚠ β 는 Table 2 에서 **분율**(0.57), Table 3 에서 **백분율**(98.00) 이다(D10).

## Group III (pp. 451–452, Fig. 5, Table 4)

- Oxford Kokam 740 mAh 8 셀, ARTEMIS 주행 사이클, **100 사이클마다 특성화(C/18.5 = 40 mA 완전 CC 충방전)** — 특징과 라벨은 **특성화 사이클**에서만.
  CV 없음 → 특징 18 개, 선택 **5/18**(Table S5). `[인쇄]` "This dataset incorporates the **lowest variability** … owing to the identical
  charge/discharge conditions."
- 분할: 훈련 3 셀(1–3) · **보정 1 셀(4)** · 시험 4 셀(5–8).
- Table 4 (전사):

| | MAPE | RMSPE | `C_score` | Sh | α-accuracy | β | PEP |
|---|---:|---:|---:|---:|---:|---:|---:|
| **a 셀 5** BRR | 0.11 | 0.15 | 95.55 | 0.89 | 100 | 100 | 31.11 |
| GPR | 0.16 | 0.19 | 71.11 | 1.21 | 100 | 100 | 15.55 |
| RF | 0.17 | 0.21 | 97.77 | 2.01 | 100 | 100 | 24.44 |
| dNNe | 0.20 | 0.25 | **100.00** | 2.93 | 100 | 100 | 6.67 |
| **b Group III 평균** BRR | **0.26** | **0.32** | 68.11 | 1.20 | 100 | 100 | 23.54 |
| GPR | 0.52 | 0.65 | 42.42 | 2.37 | 90.50 | 97.25 | 23.22 |
| RF | 0.36 | 0.44 | 72.62 | 2.16 | 88.5 | 100 | 25.44 |
| dNNe | 0.30 | 0.39 | **91.17** | 2.01 | 98.25 | 99.75 | 27.95 |

- ⚠ **Sh 단위가 바뀐다** — Group I·II 는 0.001–0.1(Ah), Group III 는 0.89–2.93. SI Fig. 17–19 의 Group III 축이 **mAh** 이므로 `[해석]` Group III 의 Sh 는 mAh 다(D10).
- `[인쇄]` "As argued in ref. 53, linear regression outperforms considerably more complex algorithms … when dealing with small sample sizes exhibiting little variance."

## Discussion · Conclusion (pp. 452–453)

- `[인쇄]` "BHUMP can complement battery management systems … and **replace the traditional equivalent circuit models altogether**."
- `[인쇄]` "prediction **without knowledge of battery design, chemistry and operating temperature**" — ⚠ 그러나 Group I 선택 특징 1번이 **`Nominal Capacity [Ah]`** 다.
- `[인쇄]` "RF-RFE-CV selects a subset of input features, indicating that **features must be selected on the basis of the intended application, battery
  design and charge protocol**" — 그룹마다 특징 집합이 다르다는 것을 저자가 인정한다. 공통 특징은 **CC 구간 에너지 하나뿐**(`[재현]` Tables S3–S5 교집합).
- `[인쇄]` "unsupervised feature selection algorithm (RF-RFE-CV)" — 지도 선택이다(D11).
- `[인쇄]` "At the expense of an average increase in MAPE of **0.43%** and RMSPE of **0.97%**, dNNe generally achieves a better calibration score" — D3.
- `[인쇄]` "we argue that despite achieving low errors, **any algorithm must undergo uncertainty quantification checks before deployment** in the field."

## Methods (pp. 453–454)

- **특징 공학**: CC 충전 전압을 `[V_l, V_h]` 로, CV 전류를 `[I_l, I_h]` 로 자른다. `V_h = V_cut-off`. `I_h` = 충전 전류, `I_l` = `I_h` 에서 **40 % 강하**.
  2-step 급속충전(Group II)은 80 % SOC 이후의 CC−CV 부분만.
- **특징 선택**: RF 700 그루, CV 폴드 수 = 특징 선택용 셀 수. `[인쇄]` "We perform feature selection … based on **a subset of the training data** to avoid
  introducing optimistically biased performance estimates" → 선택용 셀 ⊂ 훈련 셀(`[재현]` Group II 37 ⊂ 63 ✓, Group III {1,3} ⊂ {1,2,3} ✓).
- **식 (1)** `SOH = C_i / C_1` — `C_1` 은 첫 사이클 완전 충방전 용량. ⚠ 그러나 **모델의 목표와 그림은 Ah** 다(D19).
- **식 (2)** `y = f(x; θ) + ε`, `ε ~ N(0, Σ)`.
- **augmentation 식 (3)** `x_adv = x + γ·sign(∇_x l(θ, x, y))`, `γ` = 각 특징 범위의 **1 %**. `[인쇄]` "a ridge-regularized model in combination with the fast
  gradient sign method was able to **reduce the confidence interval** around the estimated mean" · "the effect of data augmentation on model performance
  is **beyond the scope** of the present work". → `[해석]` augmentation 이 **구간을 좁혔다**는 것은 정보가 늘었다는 뜻이 아니다. 그 효과를 떼어 잰
  실험(ablation)이 없다고 저자가 스스로 적는다.
- **BRR** (scikit-learn, 감마 사전) · **GPR** (RBF 커널, 커널 선택 영향 "not explore") · **RF** (1,500 그루, IJ 분산) · **dNNe** (은닉 2 층, 50 % 씩 축소,
  입력 < 10 이면 4·3 뉴런; ReLU → Leaky ReLU → sigmoid 출력; Adam 1e-3; **배치 = 셀 하나의 사이클 수**; 평균 · 분산 두 출력, NLL). 앙상블 개수는 **인쇄 안 됨**.
- **식 (7)–(8)** MAPE · RMSPE. **식 (9)** 신뢰 수준 `p_m` 마다 경험 적중 비율 `p̂_m`(Kuleshov 2018, ref 62) → **isotonic regression 재보정**(ref 63).
- **식 (10)** `C_score` = 90 % 신뢰 수준에서의 관측 적중률(지면의 식은 조판이 깨져 "1/N Σ p̂_m = 90%" 로 보인다). **식 (11)** Sh = 예측 σ 의 평균.
- **α-accuracy · β · PEP** (Saxena 2008 prognostics 지표, ref 64): α = ±1.5 % 띠, α-accuracy = 띠 안 예측의 빈도, β = 예측 PDF 가 띠 안에 둔 확률 질량의 평균,
  PEP = `[인쇄]` "percentage of early predictions (estimates residing **below the true label**, the red line in Fig. 5)". ⚠ 이 세 곳 모두 "Fig. 5" 를 가리키는데
  해당 그림은 **Fig. 3** 이다(D7).
- **Data availability**: 네 공개 저장소 URL. **Code availability**: 데이터 처리 = 요청 시, 모델 = zenodo.

## SI — Supplementary Note 1 (특징의 물리 설명, "hypothesis")

- `[인쇄]` "Any charging protocol finishes with both electrodes materials at their most extreme potential." 흑연 음극에서 삽입과 **리튬 도금**이 공존(Zhang 2006
  3전극 셀 · Zhou & Notten 2008 미세 기준극 인용). `[인쇄]` "It is known that the duration of the CC captures the polarisation phenomenon. Therefore, as the
  battery ages, the **constant current charge time (CCCT) decreases** … With aging, the **constant voltage charge time (CVCT) increases**."
- 방전 쪽 특징은 **하나** — `[인쇄]` "pseudo linear resistance" = 부하 인가 직후 전압 강하 ÷ 부하 전류(Saxena 2012), **한 사이클 지연**해 사용.
- `[해석]` 물리 귀속이 **전부 음극 분극 · 도금**이다. 열역학적 원인(리튬 재고 · 활물질 · 전극 정렬)은 한 줄도 없다. 그리고 Group II 는 **LFP**, Group III 는
  LCO/NMC 인데 귀속 논거는 LCO/흑연 3전극 문헌이다.

## SI — Supplementary Note 2 (전압 임계 · 정규화)

- `V_l = V_h − ΔV`, **`ΔV = 0.3 V`**. `[인쇄]` "The recorded curve between `V_l` and `V_h` … is then **normalised on the interval [0, 1]** by subtracting the minimum
  value and dividing by the resulted maximum value … This allows for training different batteries types and designs on the same training dataset **provided
  they underwent the same charging protocol**." SI Fig. 4·5 는 **시간 축과 전압(전류) 축 둘 다** [0, 1] 로 그린다.
- 높은 `V_l` 의 이유: 방전 후 휴지 전압 상승(SI Fig. 9) 회피 · 기록 시간 단축 · 부분 방전 수용.

## SI — Supplementary Note 3 (특징 30 개, SI Table 2)

SI Table 2 는 **렌더로 배치를 확인했다**(텍스트 층만으로는 "Discharge Capacity" 가 특징인지 목표인지 갈리지 않는다): 오른쪽 열 **Target variable = Discharge
Capacity [Ah]**, 왼쪽 30 행이 특징 `[재현]` 3 + 2 + 2 + 23 = 30 ✓.

| 묶음 | 특징 |
|---|---|
| **Battery specific data** (3) | `Nominal Capacity [Ah]` · `Charge Current [A]` · `Discharge Current [A]` |
| **Cumulative (historical)** (2) | `Cumulated Discharge Capacity [Ah]` · `Cumulated Discharge Energy [Wh]` (SI Fig. 6 라벨은 "**Lagged** Cumulated …") |
| **1 Cycle Lagged** (2) | `Lagged Cycle Time [s]` · `Lagged Pseudo Resistance [Ω]` |
| **Instantaneous charge** (23) | 충전 시작 단자 전압 · CC 구간 시간 · CV 구간 시간 · 평균 2 · 기울기 2 · 에너지 2 · 에너지 비 · 에너지 차 · 곡선 엔트로피 2 · Shannon 엔트로피 2 · 왜도 2 · 첨도 2 · Fréchet 2 · Hausdorff 2 |

- 곡선 엔트로피(식 8) `EC = log₂(2L/D) / log₂(N−1)` (Balestrino 2009). Hausdorff(식 6)는 **방향성**(곡선 → 기준선만). 기준선 = `y = mx + c`, 30–40 점.
  `figure-read ≈` SI Fig. 4 의 기준선은 정규화 CC 곡선의 **현(chord)이 아니다** — (0, 0.6) 에서 (0.4, 1.0) 로 곡선 위쪽에 떨어져 있다. 기준선 선택 규칙은 인쇄 안 됨.
- 표 오기: "Mean current during CC segment [A]"(CC 에서 전류는 상수) · "Mean voltage during CV segment **[A]**" · "Entropy of CCCV-CCCT" **두 번**(한쪽은 CVCC 일 것) (D13).

## SI — Supplementary Note 4 · 5 (데이터 · 분할)

- **RANSAC 이상치 제거는 훈련 데이터만**: `[인쇄]` "Training data that contains a significant percentage of gross errors in capacity … is removed … **test data has
  not been processed for outliers** to simulate a realistic deployment scenario."
- CALCE: 0.5 C CC 충전 → 4.2 V CV → 0.05 C, 방전 0.5 C / 1 C 에서 2.7 V. NASA: CC 1.5 A → 4.2 V → 0.02 A, NASA 11 은 무작위 방전(0–5 A), 라벨은 **주기 특성화**
  (2 A CC 방전)에서. TRI: 72 개 급속충전 정책, 4 C 방전 3.6 → 2.0 V. Oxford: 2 C CC 충전 · ARTEMIS · 100 사이클마다 C/18.5 특성화.
- **분할** (인쇄 ↔ `[재현]`, SI Tables 6–10 을 셀 단위로 셌다):

| 그룹 | 훈련(그중 선택용) | 보정 | 시험 | 인쇄 |
|---|---|---:|---:|---|
| I | **24 (11)** | 5 | **18** | 23 (10) · 5 · 19 — **한 셀씩 어긋남**(D4) |
| II | 63 (37) | 10 | 51 | 일치 · 네 집합 서로소 · 합 124 ✓ |
| III | 3 (2) | **1** | 4 | 일치 |

- `[인쇄]` "Note that the calibration dataset is neither used in training nor testing to prevent overfitting." ✓ (세 그룹 모두 서로소 `[재현]`).

# 그림 — 본 것 · 안 본 것

크로퍼 출력 그림 18 장(본문 2 + SI 16) + 표 11 장. 크로퍼가 **본문 Fig. 2 · 4 · 5 를 놓쳤다**("영역 없음") — 이 편의 핵심 그림이라 220 dpi 로 **수동 크롭**했고
(`fig_2_manual_p4.png` · `fig_4_manual_p6.png` · `fig_5_manual_p7.png`), 크로퍼의 `fig_1.png` 는 위가 잘려 `fig_1_manual_p3.png` 로 다시 뽑았다.
**본 것 9 장**: 본문 Fig. 1(수동) · 2 · 3 · 4 · 5 전부, SI Fig. 4 · 8 · 10, SI Table 2 쪽(= SI Fig. 3 포함, 배치 확인용).
**안 본 것**: SI Fig. 1(흐름도, 텍스트로 대조) · 2 · 5 · 6 · 7 · 9 · 11 · 12 · 14 · 15 · 17 · 18 (크로퍼가 SI Fig. 13 · 16 · 19 는 "그래픽 없음" 으로 제외). 표 이미지는
PDF 텍스트로 전사했다(SI Table 2 만 예외).

- **Fig. 1 (p. 449)** — CC−CV 모식도 + 파우치 셀 한 개의 추출 구간. `figure-read ≈` (c) 전압 구간이 **≈3.91 → 4.00 V**(폭 ≈0.09 V), 시간 ≈1,250–1,750 s ·
  (d) CV 전류 ≈0.74 → ≈0.44 A(= 40 % 강하 ✓), 시간 ≈360–600 s · (e) 사이클 1 · 223 · 669 · 893. ⚠ (c) 의 구간 폭은 SI Note 2 의 `ΔV = 0.3 V` 와 맞지 않는다(D12).
  (c) 의 길이 순서: **첫 사이클(짙은 파랑)이 가장 길고(≈1,700 s), 보라(초중기)가 가장 짧고(≈1,250 s), 노랑(후기)은 그 사이** — `figure-read ≈`, 단조 감소가
  아니다. SI Note 1 의 "CCCT decreases" 는 이 그림에서 **초기 구간만** 선다. (d) 는 후기일수록 길다(CVCT 증가 ✓, 노랑 한 가닥 ≈600 s 가 튄다).
- **Fig. 2 (p. 450) — Group I 셀 38, dNNe.** (a) `figure-read ≈` 참 용량 **≈1.36 → ≈0.65 Ah**, ≈1,440 사이클. 사이클 0 의 예측 ≈1.19 Ah 에 ±2σ 가 ≈1.0–1.37 로 크다
  — 본문 "the error bars capture this variability well" 과 부합. (b) 보정 전 곡선은 대각선 **위**(적중률 > 기대 = **과소 확신**, 구간이 너무 넓음), 보정 뒤 대각선에
  거의 붙는다. (c) 예측이 ±α 띠 안. (d) 오차 히스토그램 `figure-read ≈` 대부분 −0.015 … +0.015(점선 = ±α), 0 을 중심으로 **좌우 대략 반씩**.
  ⚠⚠ Table 2a 는 이 셀 dNNe 의 **PEP = 97.71 %**("estimates residing below the true label") 를 인쇄한다 — **히스토그램으로는 ≈50 % 안팎**이다(D6).
  ⚠ 초기 용량 ≈1.36 Ah 는 본문 "0.5 C (or 0.55 A)" 가 함의하는 1.1 Ah 와 24 % 어긋난다(D5).
- **Fig. 3 (p. 451)** — α 띠(±α, 초록) · 예측 `ŷ* ± 2σ` · 띠 안 확률 질량 β(주황) 모식도. 정의 그림이고 값 없음. ⚠ Methods 는 이 그림을 "Fig. 5" 로 부른다(D7).
- **Fig. 4 (p. 452) — Group II 셀 1, dNNe.** (a) `figure-read ≈` 1.075 → 0.91 Ah, ≈1,700 사이클, **사이클 ≈400–700 에 아래로 튀는 이상치 무리**와 그 자리의
  넓은 ±2σ. (b) ★ **보정 전은 대각선 위(과소 확신), 보정 뒤는 대각선 아래(과대 확신)** — 기대 90 % 에서 `figure-read ≈` 보정 전 ≈92 % → 보정 뒤 ≈74 %.
  보정이 이 셀에서는 **적중률을 90 % 에서 멀어지게** 했다. Table 3a 의 dNNe `C_score` 71.31 과 방향이 맞다. (d) 오차 대부분 0 ~ +0.01 로 **양(과대 예측) 쪽**
  — PEP 31.50 과 부합.
- **Fig. 5 (p. 453) — Group III 셀 5, dNNe.** (a) x 축 "Cycle" 0–44 = **특성화 번호**(100 주행 사이클 간격), 0.735 → 0.605 Ah. (b) 보정 전은 기대 ≈30 % 에서 이미
  관측 100 %(극단적 과소 확신), 보정 뒤도 **대각선 위** — 기대 90 % 에서 관측 ≈100 % → Table 4a `C_score` **100.00** 은 "완벽" 이 아니라 **과소 확신**이다(D9).
  (d) 오차 **전부 ≥ 0**(≈0 ~ +0.005) — 체계적 과대 예측, PEP 6.67 과 부합. 보정 곡선을 맞춘 보정 셀은 **1 개**(셀 4).
- **SI Fig. 4** — 정규화 CC 전압 곡선(두 축 [0, 1])과 기준선. 기준선이 곡선의 현이 아니다(위 SI Note 3).
- **SI Fig. 8 (RF-RFE-CV)** — (a) Group I: `figure-read ≈` 음의 MSE 가 특징 **≈5–22 개에서 −0.020 ~ −0.024 로 평평**, 삼각형(선택점)은 **≈19** 에 찍혀 있다
  (본문·Table S3 은 18, D15). `[재현]` −0.02 Ah² = **RMSE ≈0.14 Ah** 수준이다(선택용 셀 교차검증, 용량 1.1–2 Ah 셀). (b) Group II: 특징 4–12 개가 ≈−1.3 ~ −1.6 × 10⁻⁵
  로 평평, 선택 5. (c) Group III: 축이 −75 ~ −375 → **mAh² 단위**, 선택 5 인데 `figure-read ≈` 7 개 점이 같은 높이(≈−78). `[해석]` 세 곡선 모두 **최적 부분집합이
  평평한 골짜기 위의 한 점**이다 — 특징 선택 자체가 비식별이다(선택된 목록을 "물리적으로 의미 있는 특징" 으로 읽으면 안 된다).
- **SI Fig. 10 (RANSAC)** — 빨강 = 제거된 훈련 점. ⚠ 캡션 (a) "A123 LFP … Group II" ↔ 그림 (a) 는 **893 사이클 · 1.13–1.45 Ah**, 캡션 (b) "Pouch LCO … Group I" ↔ 그림 (b) 는
  **1,850 사이클 · 0.88–1.54 Ah**. `[재현]` 눈금 대조 — Fig. 1e(파우치, 사이클 1 · 223 · 669 · **893**) ↔ 패널 (a), SI Fig. 2e(TRI 급속충전, 1 · 462 · 1387 · **1850**) ↔ 패널 (b).
  **캡션 a/b 가 뒤바뀌었다**(D14). 패널 (b)(= TRI)에서 제거된 점은 사이클 ≈300–850 의 **아래로 처진 무리** — Fig. 4a 의 시험 셀에 남아 있는 것과 같은 형태다.
  `[해석]` 훈련에서는 지우고 시험에서는 두는 설계라, Group II 의 적중률은 그 무리에 대해 **학습하지 않은 채** 평가된 것이다(저자 의도와 일치).

# `[해석]` 1 — 특징이 보는 것: α·β 로 옮기면

우리 α·β 하네스(`bms-balancing/`) 의 언어로 완전지 충전 곡선은 두 전극 OCP 를 각자의 스케일(α — 활물질 양)과 오프셋(β — 정렬 · 리튬 재고)으로 늘이고 민
차이에 분극이 더해진 것이다. 이 편의 특징 원천은 그 곡선의 **상단 0.3 V 창**(CC)과 **CV 꼬리**(40 % 강하)다.

1. **창 안 시간 · 에너지(CCCT · `Energy during CCCV-CCCT`)** — 창 안에 들어간 전하량 ÷ 전류. 창 안 전하량은 두 전극의 α 에 비례해 늘고, β 가 창에 걸리는
   OCP 구간을 바꾸면 모양째 바뀐다. → **LLI(β 이동)와 LAM(α 축소)이 둘 다 같은 스칼라를 움직인다.** 이 스칼라 하나로는 둘이 갈리지 않는다.
2. **정규화된 모양 특징(왜도 · 첨도 · 엔트로피 · Hausdorff · Fréchet · 정규화 기울기)** — 두 축을 [0, 1] 로 자르기 때문에 **창 전체에 균일한 시간 스케일링에는
   불변**이다. 모든 전극이 같은 비율로 α 를 잃는 경우(창 안 모양이 그대로 늘어나는 경우)는 이 특징들에 **0 의 감도**로 들어온다. 반대로 β 이동이나
   **전극 간 α 비의 변화**는 창에 걸리는 OCP 구간을 바꿔 모양을 바꾼다. 그러니 모양 특징은 **오프셋 · 상대 스케일**에, 비정규화 시간 · 에너지는
   **절대 스케일**에 더 민감하다 — 원리상 **분리의 재료가 있다**. 그러나 이 편은 그 재료를 **용량 하나로 다시 접는다**.
3. **분극이 창을 덮는다** — CC 전류 0.5 C ~ 6 C(Group II 는 80 % SOC 이후 1 C). 창 안 모양은 OCP 만이 아니라 `R·I` 와 확산 과전압을 품는다. 저자 자신의 물리 귀속
   (SI Note 1)이 **분극 · 도금** 쪽이다. 우리 식으로는 α·β 를 풀기 전에 **분극 몫을 빼야** 하는 곡선이다(Group III 의 C/18.5 특성화만 준평형에 가깝다).

⇒ (b) 판정: **특징은 α·β 의 함수다. 특징 공간에서 LLI ↔ LAM 이 축퇴하는지는 이 편이 다루지 않는다** — 목표가 스칼라라서 축퇴가 있어도 **벌점이 없다**.
LLI 가 만든 −5 % 와 LAM_PE 가 만든 −5 % 는 같은 정답이고, 모델은 둘을 같은 점으로 보내도록 학습된다. 이것이 SOH 회귀와 모드 분해가 **다른 물음**인 이유다.

# `[해석]` 2 — 보정된 예측 구간 ≠ 식별성

| | 이 편이 잰 것 | Q4 가 묻는 것 |
|---|---|---|
| 대상 | 스칼라 예측 `ŷ` 의 오차 분포 | 파라미터 벡터(LLI · LAM_PE · LAM_NE · 접촉 분율)의 **해 집합** |
| 도구 | isotonic 재보정 · 90 % 적중률 · 날카로움 · β | FIM 조건수 · 프로파일 · 근최적 집합의 폭 |
| 참이면 말하는 것 | "이 구간은 90 % 의 경우 측정 용량을 덮는다" | "데이터에 맞는 해가 하나뿐이다(또는 폭이 이만큼이다)" |
| 서로에게 | 적중률이 완벽해도 해 집합의 폭은 모른다 | 폭이 넓어도 스칼라 예측은 정확할 수 있다(축퇴 방향이 용량과 직교하면) |

- 곱 축퇴(`A_eff·ε_p/R_s`)나 LLI ↔ LAM 축퇴는 **데이터가 같은 값을 내는 방향**이다. 그 방향에서 용량 예측은 **변하지 않으므로**, 예측 불확실성은
  그 방향의 폭을 **볼 수 없다**. 보정된 SOH 구간이 좁다는 것은 모드 분해가 정해졌다는 증거가 **구조적으로 될 수 없다**.
- 이름 문제: 35번(Thelen 2024, 큐 35, 아직 digest 전 — pp. 18–19 문장만 확인)은 `[인쇄]` "the confidence interval … captures only the uncertainty in the predicted
  mean value … the prediction interval is wider than the confidence interval because it captures both" 으로 둘을 가른다. 이 편의 `μ ± 2σ` 는 dNNe 의 분산 출력
  (자료 잡음)과 앙상블 분산을 합쳐 **측정 라벨의 적중률**로 보정되므로 기능상 **prediction interval** 이다. 이 편은 전부 "confidence interval" 이라 부른다.

# `[해석]` 3 — 목표 주도 특징 선택은 분리 채널을 버린다

- 30 개 중 **저항에 해당하는 유일한 채널**은 `Lagged Pseudo Resistance [Ω]`(방전 개시 `ΔV/I`)다. SI Tables 3–5 의 선택 목록 세 개 어디에도 **없다**(`[인쇄]` 표).
- RF-RFE-CV 의 점수는 **용량 예측 MSE** 다. 접촉 손실 ↔ LAM 을 가르는 정보(저항 · 용량성 · 시상수)는 정의상 **용량 변화와 직교하는 방향**에 있다 —
  두 기구가 같은 용량 감소를 낼 때 그 둘을 가르는 신호는 용량을 예측하는 데 **쓸모가 없다**. ⇒ 용량을 목표로 한 특징 선택은 **분리 채널을 가장 먼저
  버리도록** 설계돼 있다.
- 34호(Liang)의 "불변 학습이 처방 채널을 지운다" 와 같은 계열의 두 번째 표본이다 — 그쪽은 **사상**이, 이쪽은 **선택**이 지운다.

# ML 검증 설계 감사 (이 저장소의 체크리스트)

| 항목 | 이 편 | 판정 |
|---|---|---|
| 분할 단위 | **셀** — 훈련 · 보정 · 시험 서로소(`[재현]`), 하이퍼파라미터 CV 도 "each batch is represented by one cell" | ✓ |
| 프로토콜/데이터셋 식별값이 입력에 | **있다** — Group I 선택 특징에 `Nominal Capacity` · `Charge Current`. 다섯 묶음이 섞인 그룹에서 둘 다 묶음 표지 | ⚠ 그룹 내 성능이 **묶음 판별 + 묶음 내 궤적**으로 부풀 수 있다 |
| 과거 라벨이 입력에 | **있다** — `Lagged Cumulated Discharge Capacity`(= 이전 사이클 측정 용량의 누적) · `Lagged Cumulated Discharge Energy`. Group I 18 중 2, Group III 5 중 2(+ `Lagged Cycle Time`) | ⚠ "unknown capacity" 가정과 긴장 · 15 분 진단 주장과 긴장(전 생애 쿨롱 기록 필요) |
| 정답 축 | **측정 용량**(fitted 아님) | ✓ — 단 훈련 라벨만 RANSAC 세척 |
| 보정 집합 크기 | 5 · 10 · **1** 셀 | ⚠ Group III 는 한 셀로 isotonic 곡선을 맞췄다 |
| 시험 분포 | 같은 묶음 · 같은 조건군 안 | ⚠ 데이터셋 밖 일반화 0 |
| 성능 보고 | 그룹 평균 + 예시 셀 하나(나머지 셀 분포 0) | ⚠ Group I 평균 α-accuracy 26–36 % 가 초록에 없다 |
| ablation | augmentation 효과 "beyond the scope" · 특징 선택 효과 0 | ⚠ |

# 어휘 집계 — NFKC 정규화 후, 대소문자 구분, 낱말 경계

본문(참고문헌 전까지, 그림 · 표 텍스트 포함) · 참고문헌 · SI 를 따로 셌다. 패턴은 낱말 **시작** 경계 + 접두(`identifiab` · `uncertaint` · `calibrat` · `Bayes` ·
`posterior`), 약어는 양쪽 경계, 구는 사이 공백 `\s+` 허용.

**정규화 전후 차이**: 본문 PDF 에서 NFKC 가 바꾼 문자 **124 자** — 얇은 공백 `U+2009` 59 · 합자 `ﬃ` 40 · `¼` 17(수식 글꼴의 `=` 자리) · `U+200A` 4 · `ϵ` 2 · `½` 2.
SI 는 **86 자** — `ﬁ` 35 · `ﬀ` 24 · `ﬃ` 9 · NBSP 5 · `ϵ` 5 · `ﬂ` 3 · `¯` 3 · `Ω` 1. **큐 지문 11 열은 정규화 전후가 전부 같다**(33 · 35 번과 달리 이 편의 핵심 낱말
`confidence` · `calibrat` · `identif` 는 합자 없이 조판됐다; SI 의 `ﬁ` 는 "Offline" · "verification" · "specific" 등).

| 큐 지문 열 | 큐 값 | 본문 (NFKC · 구분 · 낱말) | 참고문헌 | SI | 정규화 전 | 판정 |
|---|---:|---:|---:|---:|---|---|
| `identifiab` | 0 | **0** | 0 | 0 | 같음 | ✓ |
| `uncertaint` | 26 | **24** | 2 | 0 (대문자 `Uncertaint` 2) | 같음 | ✓ (본문 + 참고문헌 = 26) |
| `confidence interval` | 10 | **10** | 0 | 0 | 같음 | ✓ |
| `Bayes` | 9 | **6** | 3 | 1 | 같음 | ✓ (본문 + 참고문헌 = 9) |
| `posterior` | 0 | **0** | 0 | 0 | 같음 | ✓ (`Posterior` 1 — "Posterior inference") |
| `calibrat` | 39 | **35** | 1 | 27 | 같음 | ⚠ **대소문자 구분이면 본문 + 참고문헌 = 36**. 큐의 39 = 대소문자 무시(그림 범례 "Calibrated" 3 회 더함) |
| `LLI` | 0 | **0** | 0 | 0 | 같음 | ✓ |
| `LAM` / `loss of active material` | 0 | **0** | 0 | 0 | 같음 | ✓ |
| `degradation mode` | 0 | **0** | 0 | 0 | 같음 | ✓ |
| `contact loss` | 0 | **0** | 0 | 0 | 같음 | ✓ (`contact` 0) |
| `MPa` | 0 | **0** | 0 | 0 | 같음 | ✓ |

**큐 지문 11 열 중 10 열 일치 · 1 열은 규칙 차이**(`calibrat` 39 는 대소문자 무시 수; 규칙대로면 36). 합자 가림은 **없다**.

**35 번 재확인** (지시 항목, 원본 `b8e64f97-35._Probabilistic_…pdf` sha256 `5ab976ae…` 에서 pymupdf 텍스트 → NFKC → 같은 패턴):
`confidence interval` — **정규화 전 0 · NFKC 뒤 6**. 여섯 개 모두 원시 텍스트에서 `conﬁdence interval`(합자 `ﬁ`) 로 조판돼 있고, 위치는 **pp. 18–19 의 통계 구간 설명
한 문단**(confidence ↔ prediction ↔ tolerance interval 정의)이다. ⇒ 큐 지문 35 번 행 `conf.interval` **0 → 6** 이 맞다. 같은 검사에서 35 번의 다른 열은
`uncertaint` 196(본문 180 · 참고문헌 16) · `Bayes` 52(35 · 17) · `posterior` 26 · `calibrat` 7 · `LLI` 5 · `LAM` 5 · `degradation mode` 본문 38(+ 참고문헌 6) — 큐 값
(205 · 53 · 28 · 8 · 5 · 5 · 38)과 `LLI` · `LAM` · `degradation mode` 는 맞고 네 열이 다르다(본문/참고문헌 경계는 pymupdf 텍스트의 "References" 줄로 잘랐다). 대소문자 · 참고문헌 포함 여부의 차이로 보이며 **35 번 digest 에서 재집계**할 일로 남긴다(이 digest 는 `confidence interval` 만 고친다).

추가 열 (본문, NFKC, 괄호는 대소문자 무시; SI 는 `/` 뒤): `SOH` (27) / 5 · `state of health` (8) / 4 · `confidence` 22 · `adversarial` (9) / 1 · `sharp*` (7) / 0 ·
`isotonic` (2) / 1 · `jackknife` (3) · `transfer learning` (2) · `incremental capacity` (6) · `differential voltage` (2) · `impedance` (7) / 1 · `resistance` (1) / 6 ·
`temperature` (6) / 2 · `electrode` (2) / 9 · `anode` 0 / 7 · `cathode` (1) / 3 · `graphite` 0 / 4 · `plating` 0 / 4 · `polari[sz]*` 0 / 3 · `synthetic` (2) / 0 ·
`pseudo-two-dimensional` 1 · `mechanism` (3) · `physic*` (4) / 1 · `stoichiom*` 0 · `OCV` 0 · `open circuit` 참고문헌 1 · `epistemic`/`aleatoric` 0 ·
`extrapolat*`/`out-of-distribution` 0 · `solid` 참고문헌 1 · `pressure` 0 · `identif*` (3; 본문 1 = "identified").

`[해석]` 본문에 `calibrat` 35 · `uncertaint` 24 · `confidence` 22 인데 `electrode` 2 · `mechanism` 3 · `LLI`/`LAM` 0 이다. **불확실성의 어휘는 완비돼 있고, 그 불확실성이
무엇에 대한 것인지(어느 전극, 어느 기구)의 어휘는 없다.** 34호가 "식별성을 말하면서 물리량의 이름이 없다" 였다면, 35호는 "불확실성을 재면서 분해의 이름이 없다" 다.

# Q1~Q8 판정 (닻 페이지 수집 지침)

| Q | 판정 | 근거 |
|---|---|---|
| **Q1** 접촉 손실 정량 | **없다 — `θ(N)` 0/35** | `contact` 0. 액체 상용 셀 |
| **Q2** 독립 관측 | **없다** | 1차 측정 0. 저항 채널(`Lagged Pseudo Resistance`)은 있었으나 세 그룹 모두 특징 선택에서 탈락 |
| **Q3** 라벨 층위 | **칸 없음 · 층 하나: "measured scalar label + held-out-recalibrated predictive interval (coverage audited)"** | 라벨 = 측정 방전 용량(훈련만 RANSAC) · 오차 막대 = 예측 구간, 보정 셀(5 · 10 · 1)에서 isotonic 재보정 → 시험 셀에서 90 % 적중률(`C_score`). 계보 첫 **"오차 막대가 맞는지를 held-out 에서 검사"**. ⚠ 적중률은 예측의 성질이지 라벨의 성질이 아니고, 셀 단위 적중률은 크게 흩어진다(Fig. 4b 보정 뒤 ≈74 %) |
| **Q4** 유일성·식별성 | **ASSB 0 — 칸 이동 없음(누적 0.5).** **스물일곱 번째 성질 "불확실성을 보정했다 — 분해가 없는 스칼라 위에서"** | `identifiab` 0 · 식별성 도구 0. 불확실성 도구는 계보에서 가장 완비(보정 · 적중률 · 날카로움 · β · PEP). 그러나 목표가 스칼라라 **축퇴 방향이 예측에 보이지 않는다**(`[해석]` 2). 8호의 요구("estimate + calibrated uncertainty + validity flag")를 **처음 셋 중 둘** 채운 원전이지만, 그 셋 어디에도 모드 분해는 없다 |
| **Q5** Li-In 기준 전위 | **해당 없음** | 기준극 0, 흑연/LCO · LFP 액체 셀 |
| **Q6** 압력 | **없다** (`pressure` 0 · `MPa` 0) | 파우치 셀 포함 · 구속 압력 미기재 |
| **Q7** dead Li | **해당 없음** | 무음극 아님. SI Note 1 의 리튬 도금은 **가설 문장**(측정 0) |
| **Q8** 화학·OCP | **이동 없음** — LCO · LFP · LCO/NMC(`[인쇄]` "not verified"), OCP 0 | 화학은 **입력으로도 쓰지 않는다**("without knowledge of … chemistry") — 대신 정규화로 화학 차이를 지우려 한다(SI Note 2) |

# 곱 축퇴 처방 — 열여덟 번째 적용

**적용 불가 — 물리 모델 0 · 면적 자리 0.** 이 편에는 `A_eff·ε_p/R_s` 가 들어갈 식이 없다. 입력 점검만 한다:

| 처방 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| 1단계 (16호; τ 형 21호) | `R` 과 `C`(또는 τ) | `Lagged Pseudo Resistance` = `ΔV/I`(방전 개시, **합**) — `C` · τ **0** · 그리고 **선택에서 탈락** | ❌ |
| 2단계 (18 · 25호) | 면적을 아는 대조군 | 0 | ❌ |
| 3단계-a (19호 `Ea`) | 여러 온도의 `R` | 온도 입력 0(향후 과제) | ❌ |
| 3단계-b · 4단계 | `C = τ/R` | 0 | ❌ |
| 31호 `R/k` | 같은 차단의 `R` · √t `k` | 0 (CV 전류 꼬리의 **모양 통계**는 있으나 √t 해석 0) | ❌ |

→ 처방 표에 더하는 것은 칸이 아니라 **경고 한 줄**(`[해석]` 3): **"SOH 를 목표로 학습한 파이프라인의 특징 선택 목록에서 처방 입력을 찾지 않는다 — 분리 채널은
용량과 직교하므로 선택 단계가 먼저 버린다."** 34호(재구성 · 불변 학습이 입력을 **지운다**)에 이어, 데이터 기반 BMS 가 처방 채널을 잃는 **두 번째 경로(선택)** 다.

# 어긋남 · 공백

- **D1 그룹 ↔ 프로토콜 뒤바뀜** — p. 449 첫 문장 "the 2-step fast-charging protocol in **Group III** (8 cells), and the CC protocol in **Group II** (124 cells)" ↔ Table 1 ·
  이후 본문 · SI(II = TRI 급속충전 124, III = Oxford CC 8).
- **D2 초록 "the best model … 0.45%"** — Group II 최저 RMSPE 는 **RF 0.14 %**(Table 3b). 0.45 % 는 dNNe 이고, 결론은 "the best **dNNe** model achieved a RMSPE of 0.45%" 로
  정정해 적는다. 초록의 "root-mean-squared error" 도 지표는 **RMSPE**(퍼센트). 8호 Table 2 는 초록 문장을 그대로 옮겼다.
- **D3 결론 "RMSPE 0.97 %"** — `[재현]` 세 그룹의 (dNNe − 최저) 차이: MAPE 1.13 · 0.12 · 0.04 → 평균 **0.43** ✓ · RMSPE 1.56 · 0.31 · 0.07 → 평균 **0.65**. 0.97 은
  합(1.94) ÷ **2** 와 같다.
- **D4 Group I 분할** — 인쇄 "23 cells for training (out of this 10 … feature selection), 5 … calibration and remaining 19" ↔ `[재현]` SI Tables 6–8 을 세면 **24 (11) · 5 · 18**.
- **D5 셀 38 의 정체** — 본문 "**pouch** cell … 0.5 C (or **0.55 A**)" ↔ SI Table 6 에 "38" 은 **CS2-38**(1 C 방전, 시험) · **CX2-38**(0.5 C, 시험) 두 개, 둘 다 **prismatic**
  (파우치 PL 은 11 · 13 뿐) ↔ `figure-read ≈` Fig. 2a 초기 용량 ≈1.36 Ah(0.55 A = 0.5 C 면 1.1 Ah). 세 서술이 한 셀로 모이지 않는다.
- **D6 PEP ↔ Fig. 2d** — Table 2a dNNe PEP **97.71 %**("estimates residing below the true label") ↔ 히스토그램은 0 좌우로 `figure-read ≈` 반씩. p. 450 의 다른 정의
  ("the number of capacity estimates lower than the true label **residing in the α-accuracy zone** should exceed the number … above it") 로도 97.71 은 재현되지 않는다.
  Group II · III 예시 셀(PEP 31.50 · 6.67)은 히스토그램과 부합한다 → 이 한 칸의 문제로 보인다.
- **D7 그림 번호** — Methods 의 α 띠 · β · PEP 설명이 "see Fig. 5" · "see Fig. 5" · "the red line in Fig. 5" — 정의 그림은 **Fig. 3**.
- **D8 "low calibration error of 54.70%"** — `C_score` 54.70 은 90 % 구간이 **55 % 만 적중** = 과대 확신. "low calibration **error**" 가 아니다(바로 다음 문장이 "does not output
  well-calibrated predictions").
- **D9 `C_score` 100 을 좋은 값으로** — Table 2a RF 100 · Table 4a dNNe 100.00. 목표가 90 % 이므로 100 은 **과소 확신**(Fig. 5b 보정 뒤 곡선이 대각선 위). 본문은
  "high calibration score" 를 칭찬으로 쓴다. `C_score` 의 좋고 나쁨은 90 과의 **거리**다.
- **D10 단위** — β: Table 2 분율(0.57) ↔ Tables 3 · 4 백분율(98.00). Sh: Groups I · II ≈10⁻³–10⁻¹(Ah) ↔ Group III 0.89–2.93(**mAh**, SI Fig. 17 축). 그룹 간 Sh 비교 불가.
- **D11 "unsupervised feature selection algorithm (RF-RFE-CV)"** (p. 453) — RF 회귀 · 음의 MSE 점수 = **지도** 선택.
- **D12 Fig. 1c 창 폭** — `figure-read ≈` 3.91 → 4.00 V(≈0.09 V) ↔ SI Note 2 `ΔV = 0.3 V`, Group I `V_h = 4.2 V`, `V_l = 3.9 V`. 그림의 셀이 어느 데이터의 어느 셀인지 캡션에
  없다("a Li-ion pouch cell").
- **D13 SI 특징 표** — Table 5(Group III 선택)의 "Capacity during CCCV-CCCT segment [Ah]" 가 SI Table 2 의 30 개 목록에 **없다** · "Mean current during CC segment [A]"(CC 전류는 상수)
  · "Mean voltage during CV segment **[A]**" · "Entropy of CCCV-CCCT" 가 **두 번**. SI Table 3 은 `Terminal Voltage @ Start of charge` 를 "1 Cycle Lagged Data" 칸에 둔다.
- **D14 SI Fig. 10 캡션 a/b 뒤바뀜** — 위 그림 절(`[재현]` 사이클 눈금 대조).
- **D15 SI Fig. 8a 선택점** — `figure-read ≈` 19 ↔ 18.
- **D16 SI Fig. 3 캡션** — "CCCT=constant **voltage** charge time".
- **D17 오탈자** — "RMPSE" · "BHMUP" · "Kokham"(Table 1 "Kokam") · "Savitsky−Golay".
- **D18 "unknown capacity" ↔ 이력 특징** — `[해석]` Stage 2 가정과 선택된 `Lagged Cumulated Discharge Capacity`(이전 사이클 측정 용량의 합)가 긴장한다. 온라인 BMS 가
  쿨롱 적산으로 이 값을 가질 수는 있으나, 그러면 **"15 분 구간만으로"** 가 아니라 **전 생애 기록 + 15 분 구간**이다.
- **D19 SOH 정의 ↔ 목표** — 식 (1) `SOH = C_i/C_1` ↔ 목표 `Discharge Capacity [Ah]`, 모든 그림 축 Ah. 모델이 추정하는 것은 **용량**이고 그 용량 스케일은
  `Nominal Capacity` 입력이 알려 준다.
- **D20 "under 15 min at any point"** — Group III 의 특징 · 라벨은 C/18.5(40 mA) **완전 충방전 특성화**에서 나온다. `[재현]` 740 mAh ÷ 40 mA ≈ 18.5 h 의 충전 중 0.3 V 창만
  쓰더라도 그 창이 15 분 안이라는 근거는 지면에 없다.
- **D21 "dNNe generally achieves a better calibration score"** — Group I 평균에서 90 에 가장 가까운 것은 **BRR 89.16**(dNNe 86.28). 세 그룹 중 두 그룹(II · III)에서만 선다.
- **G1** zenodo 코드 · 원 데이터 미열람. **G2** dNNe 앙상블 개수 · FGSM 이 적용된 모델(ridge)의 하이퍼파라미터 미인쇄. **G3** 시험 셀별 결과 없음(Group I 18–19, Group II 51).
  **G4** 특징 선택 · augmentation · 재보정 각각의 기여(ablation) 없음.

# 8호 원장과의 대조 (Table 2 Roman 행)

| 8호 digest 가 적은 것 | 원전 | 판정 |
|---|---|---|
| "RMSE 0.45 % (best fast-charge deployment)" | 0.45 % = **dNNe RMSPE**, Group II 최저는 RF 0.14 % | ⚠ 8호가 초록의 D2 를 물려받았다 |
| "179 Li-ion cells" | 179 ✓ — 단 **시험 셀은 73–74**(18/19 + 51 + 4), 나머지는 훈련 · 선택 · 보정 | ✓(숫자) · 맥락 누락 |
| "V/I 충전 구간" 입력 | ✓ + 정격 용량 · 충전 전류 · 누적 방전 용량(이력) | 부분 |
| `Uncertainty output` "Confidence interval reported" · `[재현]` "보정 여부 불명" | **isotonic 재보정 + 보정 전용 셀 + 90 % 적중률 표** | ❌ **8호의 "보정된 불확실성 0/8" 은 1/8 이다** |
| Validation level "Cell" | ✓ — 팩 0, 데이터셋 밖 0 | ✓ |

# 우리 프로젝트와의 접점

- **degradation-degeneracy (22p 물음)** — 이 편은 우리 축퇴 질문의 **반대편 극**이다: 모드를 풀지 않고 스칼라 하나를 맞히므로, 모드 축퇴가 아무리 넓어도
  이 편의 오차 · 적중률 지표는 **영향을 받지 않는다**. 우리가 공급할 수 있는 것은 "**같은 용량 · 다른 모드**" 합성 쌍(PyBaMM truth)이다 — 그 쌍을 이 편의 특징
  30 개에 넣으면 특징 공간에서 두 모드가 **몇 개의 특징으로 갈리는지**(정규화 모양 특징이 β 이동에 감도를 갖는지)를 잴 수 있다(`[해석]` 1, 미실행).
  수치의 정본은 `degradation-degeneracy/docs/RESULTS*.md` 이고 여기 옮기지 않는다.
- **α·β 하네스(`bms-balancing/`)** — 입력이 반쪽전지 OCP + 준평형 완전지 곡선이다. 이 편의 상단 0.3 V 창 특징은 **α·β 의 국소 범함수**라, 하네스의 폭 측정기로
  "창 하나(3.9–4.2 V)만 보이면 α·β 폭이 얼마나 넓어지나" 를 잴 수 있다 — 부분 충전 BMS 데이터에서 모드 분해가 얼마나 가능한지의 **하한 질문**이다. ⚠ 이름 충돌:
  이 편의 "α-accuracy · β" 는 예측 지표다. 하네스 문서 · 위키에서 이 편을 인용할 때 **`α_acc` · `β_mass`** 로 적어 섞이지 않게 한다.
- **가져올 것** — ① **보정 전용 셀 + isotonic 재보정 + 적중률 표**는 우리 폭 측정기 결과(근최적 집합의 폭)를 사람에게 보고할 때 붙일 수 있는 **외부 선례**다 —
  단 대상이 다르다(폭 ≠ 예측 구간). ② `C_score` 를 "90 과의 거리" 로 읽는 규율(D8 · D9).
- **공급할 것** — "보정된 SOH 구간이 좁아도 모드 분해는 정해지지 않는다" 를 **합성 truth 로 보이는** 한 장(같은 용량 · 다른 모드 쌍의 SOH 예측이 같다는 것).

# 후속 (인용 원전 — 제목 기준, 미열람)

| 서지 | ref | 왜 | 축 |
|---|---|---|---|
| Birkl, Roberts, McTurk, Bruce, Howey 2017 *JPS* 341, 373 "Degradation diagnostics for lithium ion cells" | 23 | 이 편이 IC/DV 의 **모드 분해 원전**으로 인용 — 위키에 이미 있음(`raw/papers/birkl2017_degradation-diagnostics-ocv.md`) | 연결만 |
| Richardson, Birkl, Osborne, Howey 2018 *IEEE TII* 15, 127 "GPR for in situ capacity estimation" | 32 | 이 편의 직접 비교 대상(원 곡선 구간 + GPR) — 같은 Oxford 데이터 | Q3 |
| Kuleshov, Fenner, Ermon 2018 "Accurate uncertainties for deep learning using calibrated regression" | 62 | 적중률 곡선 · isotonic 재보정의 **방법 원전** | Q3 도구 |
| Lakshminarayanan, Pritzel, Blundell 2017 NIPS "deep ensembles" | 50 | dNNe 원전 — 분산 출력 = 자료 잡음, 앙상블 = 모델 불확실성 | Q3 도구 |
| Wager, Hastie, Efron 2014 *JMLR* "Confidence intervals for random forests" | 49 | RF 의 과대 확신(D8)이 IJ 의 성질인지 | Q3 도구 |
| Saxena et al. 2008 PHM "Metrics for evaluating performance of prognostic techniques" | 64 | α-accuracy · β 의 원 정의(이름 충돌의 근원) | 어휘 |
| Severson et al. 2019 *Nat. Energy* 4, 383 | 14 · SI 21 | Group II 원 데이터 — 모드 라벨 없음 | 데이터 |
| Birkl 2017 박사논문 (Oxford) | SI 22 | Group III 원 데이터 — 같은 저자의 모드 분해와 같은 셀일 수 있음 | Q3 · 연결 |
