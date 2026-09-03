---
title: interpretable ML 4분류 — 그리고 그 분류가 묻지 않는 것
description: "Wang et al. 2025 리뷰의 white box / PIML / physics-inspired feature engineering / post-hoc 4분류, PVS·SEV 가 앉는 자리, 그리고 이 분류 체계에 identifiability·uncertainty 어휘가 통째로 없다는 전수 확인"
created: 2026-09-03
updated: 2026-09-03
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/wang2025_interpretable-ml-battery-prognosis.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: single-source
---

# interpretable ML 4분류 — 그리고 그 분류가 묻지 않는 것

## 정의

Wang, Liu, Peng, Liu, *Adv. Energy Mater.* **15**, e03067 (2025) 이 배터리
prognosis 용 interpretable ML 을 나누는 4분류. 기준은 하나 —
**해석 가능성이 어디서 주입되는가** ("Based on whether the interpretability is
introduced by the model, the feature or the post-training analysis").

| # | 분류 | 도구 (리뷰 Table 1) | 리뷰가 적은 한계 |
|---|---|---|---|
| 1 | **White box model** | linear regression, symbolic regression | 비선형 과제에 약함; 수작업 feature 설계 필요 |
| 2 | **PIML** (physics-informed ML) | PINN, physics-guided loss | 강한 사전지식 요구; 구조 복잡; **알려진 물리에 한정** |
| 3 | **Physics-inspired feature engineering** | **IC/DV peaks; ECM parameters** | 전문가 지식 의존; **신규 발견 어려움** |
| 4 | **Post-hoc analysis** | SHAP, PDP, ALE, LRP, saliency map, attention | 데이터 편향에 민감; 방법마다 결과가 다름; **인과 이해 제한** |

리뷰는 이 넷을 **위계가 아니라 도구상자**라고 명시한다 ("Rather than forming a
hierarchy, they constitute an integrative and flexible toolbox").

## PVS·SEV 가 앉는 자리

[[pvs-sev-degradation-mode-features]] 의 두 feature 를 이 분류에 넣으면:

- **PVS** = 3번(physics-inspired feature engineering) 의 **§4.2 IC/DV 계열**.
  가장 가까운 선례는 Kim et al. 2023 (*ACS Energy Lett.* 8, 2946) 의
  **DV peak intensity** — 리뷰 Fig. 5c 를 직접 보면 그 "peak intensity" 가
  실제로는 **peak−valley 진폭**이다. PVS 는 여기에 전압 간격을 분모로 넣어
  기울기로 만든 것에 해당한다.
- **SEV** = 분류상 **새 자리**. 리뷰에 `current interruption` 범주는 없고,
  SEV 는 §4.3(relaxation curves)의 측정 방식과 §4.4(EIS/DRT 의 R_ct 귀속)의
  물리 해석을 절반씩 쓴다.
- **PVS/SEV 를 함께 쓰는 설계(열역학 축 + 동역학 축)** 의 선행 프레임은
  Tao et al. 2025 (*EES* 18, 1544) — 전압 손실을 **열역학 ΔE / 동역학 η** 로
  분해한다 (리뷰 Fig. 5a). 리뷰는 이를 "effectively decoupled" 라고만 적고
  두 성분이 서로 다른 **모드**를 가르는지는 묻지 않는다.

## 이 분류가 묻지 않는 것 (전수 확인) ★

리뷰 본문(p.1–16, 참고문헌 제외)을 합자 정규화 후 전수 검색한 결과
(절차와 전체 표는 raw digest §9):

| 검색어 | 횟수 |
|---|---|
| `identifiab` · `degenerat` · `uncertain` · `noise` · `error bar` · `confidence interval` · `Bayesian` · `ill-posed` · `cross-valid` | **각 0** |
| `OCV` · `open circuit` · `half-cell` · `post-mortem`/`teardown` | **각 0** |
| `collinear` | 1 (SHAP 한계 — **feature importance 귀속**이 부정확해진다) |
| `highly correlated` (predictors) | 1 (PDP 한계 — ALE 로 대체 권고) |
| `ground truth` | 1 ("**feature importance** 에는 보편적 ground truth 가 없다") |

세 가지가 따라 나온다.

1. **"라벨의 불확실성" 은 이 분야의 자기 서술에 존재하지 않는 범주다.**
2. **상관/공선성은 "사후 해석 도구의 신뢰도" 문제로만 등장한다** — "feature 가
   공선이면 **모델이 target 을 결정하지 못한다**" 는 진술은 없다. 두 진술은
   다르다.
3. **`Parameter identification` 이라는 그림 상자(Fig. 4b)를 실으면서
   `identifiability` 는 한 번도 쓰지 않는다.** 식별을 *수행하는* 언어는
   풍부하고 식별이 *가능한지* 묻는 언어는 없다.

## 왜 중요한가

이 위키의 두 satellite 가 묻는 것([[degradation-degeneracy]]: full-cell OCV
하나로 모드를 가를 수 있는가 / [[mode-observability]]: 관측을 늘리면 갈리는가)
은 위 표의 **0 이 찍힌 칸**에 정확히 들어간다. 즉 우리 결과의 참신성은 개별
논문 대비가 아니라 **분야 리뷰 대비**로 평가된다.

동시에 이 분류는 **경계선**도 준다. 리뷰의 3번 분류를 떠받치는 문장이
"features with physical meanings … **the validity of the model can be
ensured**" 인데, 이는 물리적 *해석 가능성*과 물리적 *분해 가능성*을 혼동한
비약이다. [[fitting-degeneracy]] 가 말하는 문제는 정확히 그 비약이 감추는
자리에 있다.

## 이 위키에서의 적용

- **prognosis target 의 지형**: 리뷰가 다루는 target 은 전부 macro
  (SOH·RUL·SOC·cycle life·knee·열폭주 지표·형성 결과)다. Fig. 1 의 두 패널
  모두 Targets 이 `SOH, RUL, SOC…` 로 같다. **전극 수준(LLI/LAM)을 예측
  target 으로 삼는 사례는 이 리뷰에 하나도 없다** — 2026-09-02 세미나가 하는
  일은 이 지형의 빈 칸이다.
- 전극 수준 양이 "true value" 를 갖는 것으로 나오는 유일한 자리는 Navidi
  et al. 2024 (*Energy Stor. Mater.* 68, 103343) 의 손실함수
  ("true values of battery capacity, **lithium inventory**, and dQ/dV curves")
  이고, 리뷰는 그 참값의 출처를 적지 않는다.
- 이 분류를 [[birkl-ocv-degradation-diagnostic]] 계열과 나란히 놓으면 두
  계보가 서로를 안 본다는 것이 보인다 — 리뷰에 `OCV`·`half-cell` 이 0회다.

## 관련
- [[pvs-sev-degradation-mode-features]] — 두 feature 가 이 분류의 어디에 앉는가
- [[pvs-sev-lli-lampe-separability]] — 이 분류가 묻지 않는 질문을 대신 묻는 카드
- [[birkl-ocv-degradation-diagnostic]] — 라벨을 만드는 반대편 계보
- [[fitting-degeneracy]] — "해석 가능 ≠ 분해 가능" 의 정확한 형태
