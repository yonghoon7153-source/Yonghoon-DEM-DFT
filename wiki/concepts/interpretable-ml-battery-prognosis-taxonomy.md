---
title: interpretable ML 4분류 — 그리고 그 분류가 묻지 않는 것
description: "Wang et al. 2025 리뷰의 white box / PIML / physics-inspired feature engineering / post-hoc 4분류, PVS·SEV 가 앉는 자리, 그리고 이 분류 체계에 identifiability·uncertainty 어휘가 통째로 없다는 전수 확인"
created: 2026-09-03
updated: 2026-09-03
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/wang2025_interpretable-ml-battery-prognosis.md, raw/papers/su2024_drt-soh-health-features.md, raw/papers/rhyu2025_systematic-feature-design-formation.md, raw/papers/navidi2024_piml-degradation-diagnostics-comparison.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: multi-source-primary
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

## ★ 이 분류에 칸이 두 개 모자란다 (2026-09-03 추가)

Navidi et al. 2024 (*Energy Storage Mater.* **68**, 103343) 이 **같은 데이터에서
네 PIML 방법을 견주는** 비교 실험을 제공하면서 이 분류의 빈칸이 드러났다.
그 네 방법 중 **셋은 물리를 오직 "학습 데이터"로만** 넣고, **넷 전부가
"라벨 그 자체"** 를 공유한다 — 둘 다 위 4분류에 자리가 없다.

상세와 실측 순위(**손실항 ≫ 학습 데이터**, 55–70 % vs 10–23 % 상대개선)는
[[piml-physics-injection-points]] 로 분리했다.

`[해석]` **여섯째 자리(라벨)가 없다는 것과 위 표에서 `uncertain*`·
`identifiab*` 가 각 0회라는 것은 같은 사각지대의 두 표현이다.** 정답이
물리 모형의 적합값일 때, 그 적합의 불확실성을 묻는 언어가 없으면 여섯째
자리는 애초에 보이지 않는다.

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

## ★ 이 리뷰의 요약에 붙는 정정 (2026-09-03, 원전 대조)

이 리뷰의 raw digest(`raw/papers/wang2025_interpretable-ml-battery-prognosis.md`)
는 불변층이라 고칠 수 없다. **정정은 이 페이지가 보유한다.**

**정정 1 — §4.4 의 참조 [127] (Su et al. 2024).** 리뷰 p.10 이 인쇄한 문장:

> "An example of extracting interpretable features from DRT was provided by
> Su et al., **who observed that** the variation trends of typical DRT peaks
> and valleys during battery aging aligned with the increase in charge
> transfer resistance **caused by LLI and LAM**. [127]"

원전(Su et al., *J. Energy Storage* 90 (2024) 111770, digest:
`raw/papers/su2024_drt-soh-health-features.md`) 을 직접 확인한 결과:

| 리뷰가 함의하는 것 | 원전의 실제 상태 |
|---|---|
| Su 가 **관찰**했다 | Su 는 자기 DRT 추세를 **다른 논문의 진술로 해석**했다. 원문 문장은 "These trends are **in line with the fact that** … **[20]**" 이고, **[20] = Jiang et al., *Appl. Energy* 322 (2022) 119502** 다. **진짜 원전은 Jiang 2022** |
| LLI·LAM 이 근거로 쓰였다 | Su 는 **LLI 도 LAM 도 한 번도 재지 않는다.** 두 약어는 본문에 네 번 나오고 전부 수치 없는 서술이다. half-cell OCP fitting·ICA/DVA·해체분석·모드 시뮬레이션 전부 없음 |
| 전하전달 저항이 **증가**한다 | Su 가 "charge transfer" 로 이름 붙인 peak(**p₂**)은 5셀 중 **4셀에서 노화와 함께 감소**한다 (Fig. 5, Fig. 7). 증가하는 것은 저자가 "확산" 이라 부른 **p₃** 다. **원전 안에서 어긋난다** |
| DRT feature 가 **해석 가능**하다 | peak↔과정 대응은 **근거 없이 선언**된다 — 대칭셀·기준전극·half-cell·온도 스윕 어느 것도 없고, 전극 귀속(PE/NE)은 아예 없다 |

`[해석]` 리뷰는 문면상 크게 왜곡하지 않았지만 **증거 등급을 한 단계 올려
옮겼다**(상속된 해석 → 저자의 관찰). 이 페이지가 정리한 "이 분류는
identifiability 를 묻지 않는다" 는 진단과 같은 뿌리다 — **feature 에 물리적
이름이 붙어 있는지**는 확인하지만 **그 이름이 근거를 가졌는지**는 확인하지
않는 것이 이 리뷰의 요약 방식이다. 그 결과가 §4.4 의 이 칸이다.

**정정 2 — §4.2 의 참조 [113] (Rhyu et al. 2025).** 리뷰 표가 인쇄한 요약:
"형성 공정 중의 **dQ/dV, d²Q/dV² 관련 feature 를 자동 생성** (`Q(V)`) …
cycle life, **MAPE 9.2%**". 원전(raw:
`raw/papers/rhyu2025_systematic-feature-design-formation.md`, 컴파일:
[[fused-lasso-feature-design-framework]]) 대조:

| 리뷰가 적은 것 | 원전의 실제 상태 |
|---|---|
| dQ/dV·d²Q/dV² **feature** 를 자동 생성 | 설계된 feature 는 **용량 차분** `Q^B(3.57 V) − Q^B(3.60 V)` 꼴이다. dQ/dV·d²Q/dV² 는 feature 가 **아니라** 선택된 전압값을 **사후 해석**하는 데 쓰인다. 원문은 오히려 부정문을 인쇄한다 — `[인쇄]` "the designed features **do not directly correspond to** features in the dataset's average discharge capacity or **differential capacitance** curves" |
| MAPE **9.2%** | 9.2 는 designed 모형의 5 outer fold **중앙값**(= fold 1 값)이다. 원문 초록의 대표값은 **9.87%**, Table 6 의 `mean` 은 **9.84**, **최악 fold 는 11.93** 이고 그것은 세 접근(agnostic 11.35 / autoML 10.85 / designed 11.93) 중 **가장 나쁘다**. 리뷰는 어느 통계량인지 밝히지 않고 가장 유리한 값을 옮겼다 |
| 물리 귀속: 온도 민감도 + 입자 저항 불균일성 | 원전 서술과 일치하나, 그것은 `[인쇄]` "we **hypothesize**" / "allow us to **theorize**" 로 표현된 가설이고 근거는 **시각적 유사성**뿐이다 (정량 일치도 지표 없음) |

`[해석]` 정정 1 과 같은 병이다 — **feature 에 물리적 이름이 붙어 있는지는
확인하고 그 이름의 근거·통계량의 정체는 확인하지 않는다.** 다만 이번에는
원전이 훨씬 정직했다 (부정문을 스스로 인쇄하고, 가설임을 명시한다).

`[해석]` **인용 규칙**: 이 리뷰의 §4.2·§4.4 물리 귀속 열은 **2차 요약**으로
취급하고, 우리 문서에 옮길 때는 반드시 원전을 먼저 본다. 이번이 세 번째
사례다 (첫 번째는 §4.2 의 Kim 2023 — [[dv-peak-heterogeneity-descriptor]],
그때는 리뷰가 아니라 **우리 판독의 추론**이 틀렸다. 세 번째가 위 정정 2).

## 관련
- [[pvs-sev-degradation-mode-features]] — 두 feature 가 이 분류의 어디에 앉는가
- [[pvs-sev-lli-lampe-separability]] — 이 분류가 묻지 않는 질문을 대신 묻는 카드
- [[birkl-ocv-degradation-diagnostic]] — 라벨을 만드는 반대편 계보
- [[fitting-degeneracy]] — "해석 가능 ≠ 분해 가능" 의 정확한 형태
- [[dv-peak-heterogeneity-descriptor]] — §4.2 의 대표 사례, 원전 대조 1회차
- [[fused-lasso-feature-design-framework]] — 참조 [113] 의 원전, 원전 대조 3회차
- [[zhang2020-eis-aging-dataset]] — §4.4 의 [127] 이 쓴 데이터의 진짜 출처
