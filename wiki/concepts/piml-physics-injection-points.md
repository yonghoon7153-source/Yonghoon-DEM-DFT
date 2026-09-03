---
title: 물리가 ML 파이프라인에 들어가는 여섯 자리
description: "Where exactly physics enters a PIML pipeline — loss, input feature, architecture, post-hoc, and the two slots the standard taxonomy omits: training data and the label itself"
created: 2026-09-03
updated: 2026-09-03
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/navidi2024_piml-degradation-diagnostics-comparison.md, raw/papers/wang2025_interpretable-ml-battery-prognosis.md, raw/papers/rhyu2025_systematic-feature-design-formation.md, raw/papers/tao2025_nondestructive-degradation-decoupling.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: multi-source-primary
---

# 물리가 ML 파이프라인에 들어가는 여섯 자리

## 정의

"physics-informed" 라는 라벨은 **물리가 어디로 들어가는지**를 말하지 않는다.
[[interpretable-ml-battery-prognosis-taxonomy]] (Wang et al. 2025) 의 4분류는
그 자리를 **손실항 / 입력 feature / 구조 / 사후해석** 넷으로 나눈다. 이
페이지는 그 넷에 **두 자리를 더한다** — 근거는 Navidi et al. 2024
(*Energy Storage Mater.* **68**, 103343) 이 네 PIML 방법을 같은 데이터에서
견주면서 드러낸 것이다.

| # | 자리 | 무엇이 물리인가 | 검사법 |
|---|---|---|---|
| ① | **손실항** | 목적함수의 penalty 항 | 항을 빼고 재학습(ablation) |
| ② | **입력 feature** | 물리에서 유도한 스칼라 (IC/DV 봉우리, ECM 파라미터) | feature 를 빼고 재학습 |
| ③ | **구조** | 출력 층·중간 표현이 물리 파라미터 | 구조를 평평하게 하고 재학습 |
| ④ | **사후해석** | SHAP·PDP 등 학습 후 설명 | 학습에 영향 없음 (검사 불필요) |
| ⑤ | **★ 학습 데이터** | 물리 모형이 생성한 합성 표본 | 증강을 빼고 재학습 |
| ⑥ | **★★ 라벨 그 자체** | **정답이 물리 모형의 적합값이다** | **검사 불가 — 파이프라인 안에서는 보이지 않는다** |

⑤·⑥ 이 4분류에 없다. 그런데 Navidi 2024 의 네 방법 중 **셋(co-kriging ·
delta learning · data augmentation)은 오직 ⑤ 로만** 물리를 넣고,
**넷 전부가 ⑥ 을 공유한다.**

## ★ 자리마다 크기가 다르다 — 첫 실측 순위

Navidi 2024 Fig. 13 (`[도표]`, 직접 확인. RMSPE %, 낮을수록 좋음) 이
① 과 ⑤ 를 같은 모형에서 분리한다:

| | Q | m_p | m_n | LII |
|---|---|---|---|---|
| 기준선 NN (물리 없음) | ≈5.7 | ≈14.1 | ≈16.2 | ≈7.3 |
| + ⑤ 학습 데이터만 | ≈5.1 | ≈12.6 | ≈12.5 | ≈5.3 |
| + ① 손실항만 (증강 없이) | ≈2.5 | ≈4.2 | ≈6.0 | ≈3.5 |
| + ① + ⑤ | ≈1.3 | ≈4.7 | ≈5.6 | ≈1.6 |

`[인쇄]` 원전의 결론도 같다 — "improved extrapolation capability can be
**mainly attributed to customizing the loss function** with known physics."

**따라오는 순위** (`[해석]`, 단일 논문·단일 모형이므로 잠정):
**① 손실항 (55–70 % 상대개선) ≫ ⑤ 학습 데이터 (10–23 %).**
④ 사후해석은 정의상 0 이다.

**⑥ 은 이 순위에 넣을 수 없다** — 빼는 실험이 불가능하기 때문이다.
라벨을 물리 모형에서 떼면 지도학습 문제 자체가 사라진다.

## ★★ 여섯째 자리가 왜 위험한가

`[인쇄, Navidi §6.2]` "the corresponding **ground truth** values, which were
the degradation parameters obtained by **fitting the half-cell model** to
experimental full-cell curves". `[인쇄, 부록 A1]` 그 적합은 **사람이 손으로**
한다.

`[해석]` 세 가지가 따라온다.

1. **성능 지표가 물리적 정확도가 아니라 "적합값과의 일치도" 다.** Navidi 의
   RMSPE 는 네트워크가 사람의 적합을 얼마나 잘 흉내 내는지를 잰다.
2. **라벨이 축퇴 방향 위에 있으면 모든 방법이 같은 편향을 상속하고, 방법 간
   비교는 그것을 검출할 수 없다.** 비교 실험의 구조적 맹점이다 — 축퇴는
   **공통 인자**이므로 차이에서 소거된다.
3. **그러므로 ⑥ 을 검사하는 유일한 길은 파이프라인 밖의 독립 정답이다** —
   합성 truth([[degradation-degeneracy]]) 또는 해체 실측. Navidi 2024 는
   후자를 시도하는데 **셀 2개 · 전극당 실측 2점**이고, 네 패널 중 두 곳에서
   세 적합 방법 전부가 실측 두 점의 **바깥**에 있다 (raw digest §2 질문 5).

이 자리는 이 위키가 이미 여러 번 만난 것의 일반형이다 —
[[fused-lasso-feature-design-framework]] SI Note S11 의 4-파라미터 점추정,
[[birkl-ocv-degradation-diagnostic]] Fig. 8, Dubarry 2012, Cui 2024 Figure 8
([[np-lip-ocv-reparametrization]] 참조). **다섯 편이 같은 형태로 오차막대
없는 적합값에서 물리 결론을 뽑는다.**

## 이 위키에서의 적용

- **[[interpretable-ml-battery-prognosis-taxonomy]]** 의 4분류에 칸 두 개를
  더한다. 그 리뷰가 `uncertain*`·`identifiab*` 를 각 0회 쓰는 것과 ⑥ 칸이
  없는 것은 같은 사각지대의 두 표현이다 (`[해석]`).
- **[[pvs-sev-degradation-mode-features]]** 는 ② 자리다. Rhyu 2025 의 fused
  lasso 도 ② 이되 feature 형태를 선형대수가 만든다.
- **[[thermo-kinetic-loss-partition]]** (Tao 2025) 은 ③ 에 가깝다.
- **우리 파이프라인은 ⑥ 을 뒤집은 자리에 있다** — 라벨이 물리 모형의 적합값이
  아니라 **설계된 합성 truth** 다. 그래서 ⑥ 을 검사할 수 있는 소수의 설계다.
- **[[fitting-degeneracy]]** — ⑥ 의 라벨을 만드는 절차가 곧 이 페이지가
  판정하려는 적합이다. 두 페이지는 앞뒤로 붙어 있다.

## 한계

- 실측 순위(① ≫ ⑤)의 근거는 **논문 하나 · 모형 하나 · 데이터셋 하나**다.
  다른 화학·다른 물리 모형에서 뒤집힐 수 있다.
- Navidi 2024 의 ablation 은 PINN 에서만 돌았다. co-kriging·delta learning
  에서 ⑤ 를 빼는 실험은 하지 않았다 (그 방법들은 ⑤ 가 전부이므로 뺄 수 없다).
- ③ 구조의 기여는 ① 과 분리되지 않았다 — PINN 의 2단 구조와 두 손실항이
  같은 실험 안에 묶여 있다.

## 관련
- [[interpretable-ml-battery-prognosis-taxonomy]]
- [[fitting-degeneracy]]
- [[fused-lasso-feature-design-framework]]
- [[pvs-sev-degradation-mode-features]]
- [[22p-physics-or-degeneracy]]
