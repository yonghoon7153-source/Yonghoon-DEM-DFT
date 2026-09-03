---
title: Birkl OCV 열화 진단 알고리즘 (2017)
description: "3-parameter OCV fitting for LLI/LAM_PE/LAM_NE: cut-off constraints, the li/de degeneracy the authors themselves state, its lineage from Dubarry 2012, and how it differs from our window model"
created: 2026-09-03
updated: 2026-09-03
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/birkl2017_degradation-diagnostics-ocv.md, raw/papers/dubarry2012_synthesize-degradation-modes.md, raw/papers/marongiu2016_lfp-onboard-capacity-halfcell.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: definition
evidenceScope: multi-source-primary
---

# Birkl OCV 열화 진단 알고리즘 (2017)

## 정의

Birkl, Roberts, McTurk, Bruce, Howey, *J. Power Sources* **341** (2017) 373–386
(doi:10.1016/j.jpowsour.2016.12.011, CC BY) 이 제시한 진단 알고리즘.
**full-cell pseudo-OCV 하나만으로** 세 열화 모드 `[LLI, LAM_PE, LAM_NE]` 를
추정한다. 미분(ICA/DVA)을 쓰지 않는 것이 설계 목표였다.

절차는 **3단계**이고 자유도가 단계마다 다르다 (수식·기호는 raw digest §6):

| 단계 | 대상 | 자유 파라미터 | 목적함수 |
|---|---|---|---|
| 1 | 반쪽셀 OCP → 5상 해석 모델 (Eq. 1) | 전극당 **15** (E₀ᵢ, Δxᵢ, aᵢ × 5상) | 전압 RMSE (Eq. 2) |
| 2 | 기준 full-cell + 두 반쪽셀 동시 재적합 | **30** (PE 15 + NE 15) | 세 RMSE 의 **단순 합** (Eq. 5) |
| 3 | 열화셀 full-cell OCV | **3** = `[LLI, LAM_PE, LAM_NE]` (Eq. 19) | full-cell 전압 RMSE (Eq. 18) |

단계 1–2 는 pristine 기준셀에서 **한 번만** 수행하고 이후 30개를 **고정**한다.
전제: "열화가 개별 상에 서로 다르게 작용하지 않는다."

**핵심 구조 — 컷오프가 자유도를 소거한다.** 모드는 전극 창에 (i) offset(LLI),
(ii) scaling(LAM), (iii) stoichiometric offset `Δx_EoC`/`Δx_EoD` 로 작용한다
(Eq. 7–10). 셋째 항인 `Δx_EoC`/`Δx_EoD` 는 **자유 변수가 아니다** — 고정
컷오프 전압(4.2 V / 2.7 V)이 두 개의 등식(Eq. 11–12)을 주고, 그 선형계를 풀어
결정된다. 이 "imposed voltage limits 가 만드는 stoichiometric offset" 을 모델에
넣은 것이 저자들이 주장하는 문헌 대비 기여다 (30% LLI 에서 ~2% 의 용량 이득).

최적화: MATLAB `fmincon` **active-set** + `MultiStart` **100회**. 경계값과
초기값 목록은 인쇄되지 않았다. 목적함수는 가중치 대신 **하드 마스크**를 쓴다 —
`ΔE_Cell,deg/ΔSoC < 0.1` 구간으로 RMSE 계산을 제한한다 (EoD 쪽 급경사 편향
방지). 단, 논문이 **보고하는** RMSE 는 전 구간(2.7–4.2 V) 기준이라 최소화된
값과 다르다.

## 저자들이 명시한 축퇴 ★

이 페이지가 존재하는 이유. 저자들은 식별 가능성에 **침묵하지 않는다** — 한
종류의 축퇴를 지목하고, 그것을 풀지 않고 **파라미터화를 바꿔 우회한다**
(원문 §4.2, p.382, 전문은 raw digest §7):

> "a combination of e.g. LLI and LAM_NE,de creates the same OCV signature as an
> equal amount of LAM_NE,li. The same holds true for combinations of LLI and
> LAM_PE. **The fractions of lithiated and delithiated LAM can therefore not be
> uniquely identified** if the assumption is that LLI can occur simultaneously,
> resulting from a different mechanism."

따라서 출력 3종은 **동치류에 붙인 좌표**다:
- `LAM_PE`/`LAM_NE` = **총량**(lithiated + delithiated). 하위 귀속 불가.
- `LLI` = **total LLI** = pure LLI (SEI 등) **+** lithiated LAM 안에 갇힌 리튬.
  원문 예시: pure 10% + LAM_NE,li 5% → total LLI 15%.
- 조건부 예외: LAM 이 검출되고 LLI 가 0 이면 그 LAM 은 delithiated 로 유일 식별.

반대 방향의 강한 문장도 같은 절에 있다 — 합성 3점 복원을 두고 "proves the
ability of the diagnostic algorithm to **uniquely identify** the three different
degradation modes". 그러나 그 근거는 **같은 모델로 만든 무노이즈 데이터**
(Fig. 7 의 RMSE 0.0 mV)이므로 inverse crime 이고, 전칭 명제의 증명이 아니다.
파라미터 상관·Hessian·신뢰구간·노이즈 스윕은 논문 전체에 **없다**.

## 계보 — 이 논문 앞에 [[dubarry-mechanistic-mode-synthesis]] 가 있다 ★

**2026-09-03 추가.** 이 논문의 참고문헌 [19] = Dubarry, Truchot, Liaw,
*J. Power Sources* **219** (2012) 204–216 을 흡수해 대조한 결과, **이 페이지가
"우리 절차의 원전" 이라고 부르던 것 중 상당 부분이 Birkl 이 아니라 Dubarry 2012
에서 온다.** 판정 전문은 [[dubarry-mechanistic-mode-synthesis]], 대조표는
`raw/papers/dubarry2012_synthesize-degradation-modes.md` §10.

| 요소 | 어디서 왔는가 |
|---|---|
| α·β **창 파라미터화** (scaling + offset) | **Dubarry 2012** — `LR`(폭)·`OFS`(왼쪽 끝), 식 (2')(3), Fig. 4 의 치수선. **Birkl 본문에는 없다** |
| LAM ↔ scaling 관계 | **Dubarry 2012** 식 (5) — 우리 `α_NE/α_PE = (1−LAM_NE)/(1−LAM_PE)` 와 **동일** |
| LLI ↔ offset 관계 | **Dubarry 2012** 식 (8') |
| `LAM_liPE/dePE/liNE/deNE` **4분류와 명명 규칙** | **Dubarry 2012 §3.1** 이 정의문의 출처. Birkl 은 이것을 물려받아 [19] 로 인용한다 |
| `[LLI, LAM_PE, LAM_NE]` **3-파라미터 역문제** + 컷오프 등식 소거 | **Birkl 2017** (이 페이지) — 이쪽이 고유 기여다 |

`[해석]` 즉 **Birkl 의 기여는 좌표계가 아니라 "그 좌표계를 3개로 줄여 역문제로
푼 것"** 이다. 자유도 계보는 Dubarry **2** → Birkl **3** → 우리 창 모델 **4**.

**축퇴도 계보가 있다.** 이 페이지 아래 "저자들이 명시한 축퇴" 의 명제
(`LLI + LAM_de ↔ LAM_li`)는 **Dubarry 식 (5)+(8') 에서 곧바로 나온다** —
`{LAM_liNE = x}` 와 `{LAM_deNE = x, LLI = LR·x}` 는 `LR` 도 `OFS` 도 같게 만든다.
즉 Birkl §4.2 는 **2012년 식 안에 이미 대수적으로 들어 있던 것을 5년 뒤 말로
쓴 것**이다. Dubarry 자신은 같은 사실을 축퇴가 아니라 **"masking"**(비관측성)
으로 읽었다.

## 왜 중요한가

이 알고리즘은 **[[degradation-degeneracy]] 가 식별 가능성을 판정하는 대상
절차의 원전**이다. 2026-09-02 BML 세미나(김시원) p.3 이 "half-cell OCP 를
full-cell OCV 에 fitting" 이라 적으며 인용한 문헌이 이것이고, 그 세미나의 ML
라벨이 이 계열 절차로 만들어진다 ([[pvs-sev-lli-lampe-separability]] 의
"라벨의 불확실성" Gap).

**우리 절차와 같지 않다** — 이 차이가 실용적 산출물이다:

| 축 | Birkl 2017 | 우리 저장소 문서가 서술하는 창 모델 |
|---|---|---|
| 자유 파라미터 | **3** `[LLI, LAM_PE, LAM_NE]` | α_PE, β_PE, α_NE, β_NE 형태 |
| EoC/EoD | 컷오프 등식으로 **소거** | 자유롭게 따라 움직임 |
| 목적함수 | 전압 RMSE + 기울기 마스크 | 전압 잔차 (+ dQ/dV 항 실험) |

즉 Birkl 원안은 **구조적으로 자유도가 낮고**, 그 대가로 반쪽셀 OCP 의 **절대
전압 정확도**에 직접 의존한다 (Eq. 11–12 가 4.2/2.7 V 를 등식으로 쓴다).
우리가 이미 관측한 "PE 쪽 OCP 를 수 mV 왜곡하면 분해가 무너진다"
([[22p-physics-or-degeneracy]]) 는 이 원안에서 **더 나쁘게** 나타날 개연성이
있다 — 아직 실측하지 않았다.

## 이 위키에서의 적용

- **용어의 정본** (2026-09-03 정정): `LAM_*,li` / `LAM_*,de` 구분을 이 논문 §2.1
  이 쓰는 것은 맞으나, **정의문의 출처는 이 논문이 아니라
  [[dubarry-mechanistic-mode-synthesis]] §3.1** 이다 (Birkl 이 [19] 로 인용).
  우리 격자의 `lam_pe_type`/`lam_ne_type ∈ {de, li}` 는 **의미가 정확히 일치**
  한다 (`src/modes.py` 는 `de` 일 때만 잔여 전극 초기농도를 `c/(1-lam)` 로
  되올린다 = 죽은 물질은 비어 있었다).
- **인용 금지 문장** (이 논문을 근거로 쓸 수 없다):
  - "OCV fitting 이 LAM 의 리튬화/탈리튬화를 가른다" → 원문이 불가능하다고 적음
  - "OCV fitting 의 LLI 는 SEI 등 기생반응 손실이다" → total LLI 다
  - "이 방법은 유일해를 준다" → 근거는 무노이즈 3점
- **가져올 수 있는 실험 두 개** (미실행, [[mode-observability]] 급 비용):
  1. **컷오프 등식 (11)(12) 을 제약으로 추가**했을 때 degeneracy 가 줄어드는가.
     목적함수에 항을 더하는 대신 **제약으로 자유도를 줄이는** 접근이며, dQ/dV
     항 추가가 실패한 전례가 있는 우리에게 값싼 대안이다.
  2. **기울기 마스크 on/off paired 비교.** Birkl 은 급경사(EoD) 구간을 목적함수
     에서 뺀다 — 식별에 가장 유리한 구간을 버리는 선택이며, 그 대가가 얼마인지
     논문은 재지 않았다.
- **인용 확인 — 종결 (2026-09-03)**: `degradation-degeneracy/docs/02_CODE_AUDIT.md`
  와 `docs/04_PROMPTS.md` 의 `LLI = (1−α_PE) + (β_PE − β_NE)` 에 붙은
  "Birkl 2017 부호 규약" 주석은 **틀린 이름이다**. 후보 [19] Dubarry 2012 를
  흡수해 대조한 결과 (판정 전문: [[dubarry-mechanistic-mode-synthesis]] §판정):
  - **α·β 창 좌표계와 li/de 4분류는 Dubarry 2012 가 출처다** → 주석이 가리켜야
    할 이름은 "Dubarry 2012 (LR·OFS) 창 파라미터화".
  - **그러나 저 LLI 식 자체는 두 논문 어디에도 없다.** Dubarry 식 (8') 과
    비교하면 offset 항 **부호가 반대**이고, LAM 항을 **더하며**(Dubarry 는 뺀다),
    그 LAM 항의 전극도 다르다(Dubarry 는 `LAM_liNE`·`LAM_dePE` 만 — `LAM_liPE` 는
    offset 에 들어가지 않는다). → **문서화되지 않은 우리 쪽 (재)유도**로 봐야 한다.
  - 현행 `src/fitting.py:23` 의 `κ·(β_NE − β_PE)` 는 **offset 부호가 Dubarry 와
    일치**한다 — 어긋난 것은 legacy 문서 쪽이다.
  - 이번 세션도 해당 문서를 **읽기만 했고 고치지 않았다** (RUN_SCOPE 밖이지만
    미변경).

## ★ 그 3-파라미터 좌표가 **정확히 무엇의 몫공간인지** 확인됐다 (2026-09-03 추가)

이 페이지는 지금까지 저자들의 산문 진술(`[인쇄]` §4.2 "a combination of e.g. LLI
and LAM_NE,de creates the same OCV signature as an equal amount of LAM_NE,li …
The same holds true for combinations of LLI and LAM_PE") 을 옮겨 적기만 했다.
그 진술이 가리키는 대상이 **닫힌 형태로 확정됐다.**

Birkl 자신이 §3.1 에서 이 이론의 출처로 지목하는 `[26]` (`[인쇄]` "The theory
underlying the proposed degradation modes and their effects on the OCV of cells
and electrodes is well documented in the literature **[19,26,29]**") 이
Marongiu et al. 2016 (*J. Power Sources* **324**, 158–169) 이고, 그 논문이
**모드 5개 → 창 좌표 4개 사상을 식으로 전부 인쇄한다** (식 2–5). 거기서 나오는
정확한 null 2차원 (계산·수치 검증: `raw/papers/marongiu2016_lfp-onboard-capacity-halfcell.md` §5,
계보 표: [[halfcell-window-parametrization-lineage]]):

```
좌표: (ΔLLI, ΔLAM_Pe,Li, ΔLAM_Pe,De, ΔLAM_Ne,Li, ΔLAM_Ne,De),  N = 로딩비
n₁ = ( −N ,  0 ,  0 , +1 , −1 )     ← 이 페이지의 "LLI ↔ LAM_NE,li/de" 진술
n₂ = ( +1 , −1 , +1 ,  0 ,  0 )     ← "The same holds true for … LAM_PE"
```

`[재현]` 이 두 방향을 Birkl 의 세 좌표
`total-LLI = LLI + N·LAM_Ne,Li + LAM_Pe,Li`, `LAM_PE = LAM_Pe,Li + LAM_Pe,De`,
`LAM_NE = LAM_Ne,Li + LAM_Ne,De` 에 넣으면 **전부 정확히 0** 이다.

> `[해석]` **Birkl 의 `[total-LLI, LAM_PE, LAM_NE]` 는 `ℝ⁵/span{n₁,n₂}` 다.**
> 5 − 2 = 3. 저자들이 "the reason for the diagnostic algorithm to be designed in
> this manner" 라고 적은 설계 선택이 **몫공간 좌표의 선택**이었음이 수식으로
> 확인됐다. 이 페이지가 그동안 산문으로만 옮겨 적던 것의 정확한 형태다.

`[해석]` **인용할 때의 함의**: 이 알고리즘의 출력 세 값은 "세 개의 물리량" 이
아니라 **동치류의 대표원**이다. 하위 귀속(li/de)을 주장하는 후속 인용은 물론,
"LLI 가 몇 % 였다" 를 절대량으로 읽는 인용도 `n₁`·`n₂` 위에서 임의로 이동
가능한 값을 인용하는 것이 된다.

## 한계 (raw digest §13 요약)

- 합성 검증은 **inverse crime**: 생성 모델 = 적합 모델, 노이즈 0, 3점뿐.
- 코인셀 검증의 정답은 **제작 설계값**이다 (해체 대조 없음). 오차 막대 5.4% 는
  **제작 재현성**이지 추정 불확실성이 아니다.
- 6셀 중 최소 2셀에서 본문 서술이 그림보다 관대하다 (Fig. 8 패널 d, j).
- 상용 노화셀 적용 없음, 다른 화학종 검증 없음 (저자가 future work 로 인정).
- 검증셀의 열화는 전부 "잘라낸 균일한 조각" 이라, 단계 2 의 핵심 가정(열화가
  개별 상에 다르게 작용하지 않는다)을 **구조적으로 시험할 수 없다**.
- 조판 오식 2건: Table 2 의 LLI 셀 전극 지름 20 mm (본문·Fig. 4 는 15 mm),
  p.381 의 "solving Equation (2)" (Eq. 4 여야 한다).

## 관련
- [[halfcell-window-parametrization-lineage]] — 이 알고리즘의 3-파라미터 좌표가 어느 5-모드 공간의 몫공간인지, 그리고 계보 전체의 자유도·제약 비교
- [[dubarry-mechanistic-mode-synthesis]] — 이 알고리즘이 물려받은 좌표계(LR·OFS)와 li/de 4분류의 출처 (2012)
- [[fitting-degeneracy]] — 이 알고리즘이 답해야 하는 질문 자체의 정의
- [[degradation-degeneracy]] — 이 절차의 식별 가능성을 PyBaMM 합성 truth 로 판정하는 satellite
- [[22p-physics-or-degeneracy]] — 우리 분해가 물리인지 축퇴인지의 질문 카드
- [[pvs-sev-lli-lampe-separability]] — 관측을 늘리면 갈리는가 (이 논문은 관측 하나만 쓴다)
- [[mode-observability]] — 위 "가져올 수 있는 실험 두 개" 의 실행 주체 후보
