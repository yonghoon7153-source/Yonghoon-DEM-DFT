---
title: Fused-lasso 체계적 feature 설계 프레임워크 (Rhyu 2025)
description: "형성 데이터에서 cycle life 를 예측하는 두 개의 Q(V) feature 를 자동 설계하는 7단계 절차 — 물리가 들어오는 지점과 들어오지 않는 지점"
created: 2026-09-03
updated: 2026-09-03
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/rhyu2025_systematic-feature-design-formation.md, raw/papers/wang2025_interpretable-ml-battery-prognosis.md, raw/papers/2026-09-02-siwon-kim-degradation-mode-ml-seminar.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: single-source
---

# Fused-lasso 체계적 feature 설계 프레임워크 (Rhyu 2025)

## 정의

Rhyu et al., *Joule* **9** (2025) 101884 이 제안한, **회귀 문제에서 예측력 있고
해석 가능한 feature 를 자동으로 설계하는** 절차. 2026-09-02 BML 세미나(김시원)
p.4 가 [[interpretable-ml-battery-prognosis-taxonomy]] 와 나란히 인용한 둘째
문헌이며, 세미나의 수작업 feature([[pvs-sev-degradation-mode-features]])와
**정확히 반대 방향의 설계 철학**이다.

적용 사례: SC-NMC532‖인조흑연 파우치셀 178개(62 형성 프로토콜)의 **형성 단계
데이터만으로** cycle life 를 예측 — 추가 진단 사이클 없이 MAPE 평균 9.84
(원문 초록은 9.87).

### 절차 7단계

| # | 단계 | 사람이 넣는 값 |
|---|---|---|
| 0 | 입력 데이터 후보 추출 → 6종 (`Q^A(V) t^A(V) Q^B(V) V^B(t̃) Q^C(V) V^C(t̃)`) | 도메인 지식으로 **후보를 지운다** |
| 1 | 입력형 유망성 평가 — tsfresh autoML 2,448 모형 | p-value 격자 17점, 알고리즘 6종 |
| 2 | fused lasso 의 λ 결정 — 예측성·강건성·해석성 3제약 | DTW ratio < 0.7, path length < 5, 1SE rule |
| 3 | β 의 **점프**로 전압축 구간분할 | 점프 문턱 `0.001 × range(β)` |
| 4 | 구간마다 **차분·평균** 두 feature (Eq. 3–5 로 유도) | 없음 — 대수적으로 유도됨 |
| 5 | 구간 병합 (Algorithm S1) | `th_merge = 0.01` (≈1% 오차) |
| 6 | feature 하향선별 (Algorithm S2, 공선성 회피) | `th_PC,X = 0.2`, `th_PC,y = 0.4` |

산출물은 5개 outer fold 에서 일관되게 **`Q^B(3.57 V) − Q^B(3.60 V)` 와
`Q^B(3.60 V) − Q^B(3.66 V)` 꼴의 두 용량 차분** (전압값은 fold 마다 ±0.01–0.03 V).

## 물리가 들어오는 곳은 두 군데뿐이고, feature 의 형태를 만들지 않는다

이 페이지의 핵심 판정이다.

- **앞쪽 (단계 0) — 지우기만 한다.** `[인쇄]` "the current I can be discarded
  because I is constant for most of the process" 처럼 도메인 지식은 후보를
  **줄이는 데만** 쓰이고 새 물리량을 만들지 않는다.
- **뒤쪽 (본문 §"Physical meaning") — 사후 설명이다.** feature 가 정해진 뒤에
  반응입자 앙상블 모형으로 왜 예측력이 있는지를 설명한다. `[인쇄]` "a
  physics-based investigation, **which is guided by the designed features**".
- **형태를 만드는 것은 선형대수다.** β 가 구간 안에서 평평 → Q̃(V) 를 직선
  근사 → 기울기·절편이 각각 차분·평균의 아핀 변환. `[인쇄]` "only two features
  are needed to describe each section".
- 저자들이 대체 대상으로 지목하는 것이 명시적이다. `[인쇄]` "automatic feature
  extraction can be more effective than **handcrafted features that are limited
  by the many unknown aspects of the underlying physics**".

## 왜 중요한가

### ① agnostic 기준선을 세우는 패턴 — 이 위키에서 가장 이식 가치가 높다

이 논문은 **프로토콜 파라미터(CC1, CC2, CV, n_ver, T, t_OCV)만 입력으로 쓰는
"agnostic" 모형 52개**를 먼저 만들어 기준선으로 세운 뒤, 설계 feature 모형이
그것을 이기는지로 판정한다. 그리고 agnostic 의 한계를 스스로 인쇄한다:
특정 프로토콜 템플릿에만 적용 가능 · **셀-대-셀 변동을 못 잡음**.

우리가 이 계보에서 반복해 지적해 온 병 — **ML 입력에 프로토콜 식별자가 섞여
있는가** — 을 저자들이 먼저 분리해 놓았다. 2026-09-02 세미나의 `voltage window`
입력이 정확히 이 agnostic 축인데, 세미나는 그것을 물리 feature 와 같은 상자에
넣고 permutation importance 를 계산한다.
→ [[pvs-sev-lli-lampe-separability]] 의 Evidence For 2번을 **판정 가능한
실험 설계**로 바꾸는 방법이 여기 있다.

### ② 검증 설계가 이 계보에서 가장 엄격하다

- group 단위 = **형성 프로토콜** (형제 셀 3개가 절대 갈라지지 않는다)
- **feature 설계가 outer training set 안에서** 일어난다 (SI Fig. S3 의 주황 루프)
- feature 설계용 inner 분할과 하이퍼파라미터용 inner 분할을 **일부러 다르게** 잡는다
  (`[인쇄]` "intentionally differentiated ... to avoid information leakage")
- 선행 연구의 leakage 를 각주로 못 박는다. `[인쇄, 각주 49]` Weng et al. 의 8%
  는 "having the cells from the same formation protocol in both their
  'validation' set and 'train/test' sets" 에서 나온 값이다.

### ③ 그러나 "minimal domain knowledge and user input" 은 과장이다

사람이 넣는 문턱이 최소 6개다 (위 표) — 그중 둘은 `[인쇄, Table S2 각주]`
"chosen **based on trial and error**". 도메인 지식은 줄었지만 **하이퍼파라미터
지식으로 옮겨간 것**에 가깝다.

## 이 프레임워크가 말하지 않는 것 (경계)

- **예측 대상은 오로지 cycle life 다.** `LLI`·`LAM` 이 본문·SI 통틀어 0회,
  `degradation mode` 2회는 둘 다 참고문헌 제목 안. **설계 feature 를 열화 모드
  분율에 연결하는 문장이 없다.**
- **오히려 반대 증거가 원문 안에 있다.** 느린 형성 32셀에서 형성 후 C/20 RPT 의
  dQ/dV·d²Q/dV² 가 `[인쇄]` "nearly indistinguishable" 인데 cycle life 는 다르다
  → 그 데이터에서 수명을 예측하는 정보는 **열역학적 모드 좌표 밖**(저자들의
  귀속: 미시 입자 저항 불균일성 = 동역학)에 있다.
- **fold 간 강건성은 `Q^B(V)` 한 입력형에서만 성립한다.** `Q^C(V)` 는 fold 마다
  전혀 다른 전압대를 고르고, `V^B(t̃)` 는 fold 1 에서 제약을 통과하는 λ 가
  아예 없다 (SI Table S4–S6). 원문은 이 대조를 하지 않는다.
- **β 의 국소 부호가 fold 간에 안정하지 않다** (SI Fig. S5e, 직접 봄):
  설계 feature 가 사는 3.45–3.60 V 에서 다섯 inner fold 의 β 가 −0.70 ~ +0.37
  로 갈리고 부호가 뒤집힌다. 논문은 이 그림을 **강건성의 증거**로 제시한다
  (강건성이 DTW 형상 비율로 정의되기 때문이다).
  이 위키의 언어로는 [[fitting-degeneracy]] 의 flat-valley 문제와 같은 계열이며,
  이 논문 자신의 계보가 그 진단 도구를 갖고 있는데도(참고문헌 [13] =
  Schaeffer et al. 의 nullspace 논문, 저자 4명 겹침) 적용하지 않는다.

## 이 위키에서의 적용

- **가져올 것**: agnostic 기준선 패턴(위 ①) · feature 설계를 학습 fold 안에
  가두는 중첩 CV(②) · `fused lasso β → 구간분할 → 차분·평균` 기계장치를
  **우리 목적함수의 전압창 가중**에 이식하기. 셋째는 y 를 cycle life 가 아니라
  **모드 파라미터**로 바꿔야 성립하며, 그러면 β 는 회귀계수가 아니라 정규화된
  **감도(Jacobian 행)** 가 된다 — 이 치환의 타당성은 미확인.
- **공급할 것**: 이 논문 SI Table S9 의 4-파라미터 이용상태 추정
  `(β_c = 0.911, β_a = 0.854, Q_rem/Q_c,total = 0.930, V_shift = 0.014 V)` 은
  우리의 `(LAM_PE, LAM_NE, LLI, 저항)` 과 좌표가 대응하는데 **점추정만** 있고
  거기서 "전극 용량 손실 > 리튬 재고 손실" 이라는 물리 결론을 도출한다.
  [[degradation-degeneracy]] 의 합성 truth 격자가 그 결론에 식별 가능성 경계를
  붙일 수 있다.

## 불확실성

- 이 페이지는 **단일 원전**(rhyu2025 digest)에 기반한다 — `evidenceScope:
  single-source` 이므로 `confidence: high` 로 올리지 않는다.
- 프레임워크의 일반화 주장(`[인쇄]` "expected to design predictive features
  customized to each application")은 이 데이터셋 하나에서만 검증됐다.
- Zenodo 코드(10.5281/zenodo.14916092)를 읽지 않았다. 절차 서술은 논문 본문 +
  SI 기준이며 구현과 어긋날 수 있다.

## 관련
- [[pvs-sev-degradation-mode-features]] — 정반대 철학(수작업 물리 feature)
- [[interpretable-ml-battery-prognosis-taxonomy]] — 이 논문이 리뷰 [113] 로 실린 곳
- [[fitting-degeneracy]] — β 부호 불안정이 걸리는 우리 쪽 개념
- [[pvs-sev-lli-lampe-separability]] — agnostic 기준선 패턴이 답을 바꾸는 카드
