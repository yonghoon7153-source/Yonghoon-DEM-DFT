---
title: N/P·Li/P 재매개화와 2 자유도 정리
description: "The SOC-normalized full-cell OCV shape is governed by exactly two ratios, so LLI/LAM_PE/LAM_NE enter it only projectively — Lin & Khoo 2024"
created: 2026-09-03
updated: 2026-09-03
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/lin2024_ocv-degradation-mode-identifiability.md, raw/papers/birkl2017_degradation-diagnostics-ocv.md, raw/papers/dubarry2012_synthesize-degradation-modes.md, raw/papers/schaeffer2024_nullspace-regularization-interpretation.md]
confidence: high
explored: false
verificationStatus: unverified
claimType: theoretical
evidenceScope: multi-source-primary
---

# N/P·Li/P 재매개화와 2 자유도 정리

## 정의

전극별 OCP 두 개를 붙여 full-cell OCV 를 만들 때, 전하 보존은 두 전극 SOC 를
**직선 하나**로 묶는다 (Lin & Khoo 2024, 식 7):

```
z⁺(z⁻) = z₀⁺ − r_N/P · z⁻
     r_N/P = Q̂⁻_max / Q̂⁺_max        (N/P 비 — 기울기)
     z₀⁺   = Q̂^Li_max / Q̂⁺_max      (Li/P 비 — 절편)
```

세 SOH 파라미터 `(Q̂^Li_max, Q̂⁻_max, Q̂⁺_max)` 는 각각 LLI · LAM_NE · LAM_PE 와
`X = 1 − Q̂/Q̂_ini` 로 1:1 대응한다 — **이 저장소
(`degradation-degeneracy/docs/07_LAM_LLI.md`)의 정의와 같은 형태다.**

이 매개화의 성질 셋 (`[인쇄]`, 원전 §2.2–2.3):
- **컷오프 전압 무관** — `r_N/P`, `z₀⁺` 를 정의하는 데 `U_min`·`U_max` 가 안 쓰인다.
- **pristine 무관** — 초기 셀 상태를 몰라도 정의된다 (퍼센트 표기와 정반대).
- **독립** — [[birkl-ocv-degradation-diagnostic]] 의 4개 전극 SOC 한계 + 제약 2개,
  Mohtat 2019 의 4개 + 제약 1개와 달리 제약이 없다. 원전은 그 제약된 매개화들을
  `[인쇄]` "non-independent parameters, of which the **redundancy** complicates
  their estimation" 이라고 비판한다.

## ★ 2 자유도 정리 (이 페이지의 핵심)

`[인쇄]` 원전 §2.3: "the shape of an OCV curve, or the SOC-based OCV, is **only
governed by two degrees of freedom** … a certain ratio LLI ∶ LAM⁻ ∶ LAM⁺ **does
not correspond to a unique shape of OCV** … it is the ratio
(1−LLI) ∶ (1−LAM⁻) ∶ (1−LAM⁺) … which will **uniquely determine** the OCV shape."

식 (16) 이 다리다:

```
r_N/P = r_N/P,ini · (1 − LAM_NE)/(1 − LAM_PE)
z₀⁺   = z₀⁺,ini   · (1 − LLI)  /(1 − LAM_PE)
```

**따라오는 정확한 null 방향** (`[해석]` — 재료는 전부 `[인쇄]`):

> 임의의 `c > 0` 에 대해 `(1−LLI, 1−LAM_NE, 1−LAM_PE) → c·(1−LLI, 1−LAM_NE, 1−LAM_PE)`
> 는 `r_N/P` 와 `z₀⁺` 를 동시에 불변으로 두므로 **SOC 정규화 full-cell OCV 곡선을
> 글자 그대로 동일하게** 만든다.
>
> 특히 pristine 에서 출발하면: **`LLI = LAM_PE = LAM_NE = x` 인 모든 `x` 에 대해
> 곡선 형상이 pristine 과 완전히 같다.** 달라지는 것은 총용량뿐이며 정확히 `1−x` 배다.

이것은 노이즈·최적화와 무관한 **모델 자체의 성질**이므로 국소가 아니라 구조적이다
— [[fitting-degeneracy]] 가 말하는 flat valley 의 **닫힌 형태 한 방향**이다.
[[dubarry-mechanistic-mode-synthesis]] 가 준 `{LAM_liNE = x} ≡ {LAM_deNE = x,
LLI = LR·x}` 와 같은 계보이되 더 일반적이다.

**축퇴가 아닌 부분도 적어야 한다**: 총용량 `Q̂max` 은 이 방향을 따라 변하므로,
**형상 2 + 측정 총용량 1 = 3** 으로 세 모드가 원리적으로는 복원 가능하다.
문제는 원리가 아니라 **조건수**이고, 원전 Fig. 9 가 그것이 대부분의 조건에서 매우
나쁘다는 것을 보여 준다.

### 이 방향을 그리는 법은 다른 문헌에 있다 (2026-09-03 추가)

원전은 이 방향을 **인쇄만 하고 그리지 않는다** (오차공분산 `C_θ` 를 계산해
놓고 `sqrt(diag)` 만 그린다). 그 그림을 그리는 기계는
[[nullspace-coefficient-interpretation]] (Schaeffer et al. 2024) 에 있다 —
식 (19) 의 `γ`-완화 사영과 "직교 성분 대조" 그림. **두 페이지는 짝이다:
여기가 *무엇을* 그릴지, 저기가 *어떻게* 그릴지.** 절차는
[[fitting-degeneracy]] 의 "그 방향을 그리는 법" 절에.

`[해석]` 두 문헌은 서로를 인용하지 않는다. 어휘가 갈라져 있기 때문이다 —
Lin 은 `identifiab*` 26회 / `nullspace` **0회**, Schaeffer 는 `nullspace`
69회 / `identifiab*` **0회**. 같은 수학적 대상의 두 이름이다.

## 파생 도구 — 전극 DV fraction `λ±`

```
λ⁺ = (dU⁺/dQ̂⁺) / (dU⁺/dQ̂⁺ + dU⁻/dQ̂⁻) ∈ [0,1],   λ⁻ = 1 − λ⁺
```

full-cell 미분전압에 대한 **PE 의 기여 비율**. 컷오프에서의 값 `λ⁺_l`(방전 종료)
`λ⁺_u`(충전 종료) 가 **모든 감도 gradient 의 공통 인자**로 들어간다 (식 31).
`λ⁺_l ≈ 1` ⇔ PE-limited discharging, `≈ 0` ⇔ NE-limited discharging.

`[해석]` **`λ±` 는 관측 가능한 feature 가 아니다** — 반쪽전지 OCP 를 알아야
계산되는 모델 내부량이다. full-cell 곡선만으로 계산되는
[[pvs-sev-degradation-mode-features]] 의 PVS 와 혼동하면 안 된다.

## 네 regime (Highlight 4)

`Li/P` 와 `Li/N` 이 각각 1 보다 큰지로 나뉜다. 총용량의 세 감도가 극한값을 갖는다
(식 47, Table 4·5):

| regime | 조건 | 이상 `Q_max` | `∂Q̂max/∂Q̂^Li` | `∂Q̂max/∂Q̂⁻` | `∂Q̂max/∂Q̂⁺` |
|---|---|---|---|---|---|
| Ⅰ Li 과잉 | Li > N, P | `N+P−Li` | **→ −1** | → 1 | → 1 |
| Ⅱ NE 과잉 | N > Li > P | `P` | → 0 | → 0 | → 1 |
| Ⅲ PE 과잉 | P > Li > N | `N` | → 0 | → 1 | → 0 |
| Ⅳ Li 부족 **(전형)** | Li < N, P | `Li` | **→ 1** | → 0 | → 0 |

regime Ⅰ 의 `−1` 은 `[인쇄]` "loss of lithium inventory … will,
**counterintuitively, increase the total capacity**" — 리튬이 너무 많으면 움직일
자리가 없다. 원전은 이 regime 을 `[인쇄]` "a normal cell **rarely falls into**"
라고 적는다 (사전리튬화 셀에서만).

**⚠ 인용 주의**: 이 표는 **총용량의 감도**이지 식별 가능성 지도가 아니다. 원전
Table 4 캡션은 "**only** identifiable" 이라고 쓰는데 같은 문장의 본문판(§2.7)은
"**highly** identifiable" 이다. 원전 Fig. 9(d) 에서 `∂Q̂max/∂Q̂⁻ → 0` 인 regime 인데도
`Q̂⁻` 가 넓게 식별 가능하다 — **곡선 형상이 준 정보**다. 표는 필요조건도
충분조건도 아니다.

## 이 위키에서의 적용

- **[[fitting-degeneracy]]** 에 닫힌 형태 null 방향 하나를 공급한다 (수치로 찾던
  것의 해석해).
- **[[22p-physics-or-degeneracy]]** — 22p 세 값을 식 (16) 에 넣으면 형상 정보가
  스칼라 하나로 축소된다. 그 카드 Evidence For 참조.
- **[[pvs-sev-lli-lampe-separability]]** — "관측을 늘리면 갈리는가" 에 대해,
  **같은 정규화 곡선에서 파생된 관측은 2 자유도를 넘을 수 없다**는 상한을 준다.
- 우리 창 좌표와의 사영 대응 (`[해석]`, 미검증):
  `z₀⁺ ↔ (β_NE − β_PE)/α_PE`, `r_N/P ↔ α_NE/α_PE`.

## 한계 (원전이 스스로 적은 것)

- 반쪽전지 OCP 가 **노화에 불변**이라는 가정. 결정구조 변화·리튬 플레이팅 미포함.
- **복합전극(Si/Gr)을 명시적으로 범위 밖에 둔다** — 우리 셀의 기본 구성이다.
- **동역학 없음.** 총용량 `Q̂max`(열역학)과 충·방전 용량(동역학+프로토콜)의 구분을
  §1 에서 강조하며, 후자와 혼동하지 말라고 적는다.

## 관련
- [[nullspace-coefficient-interpretation]]
- [[fitting-degeneracy]]
- [[birkl-ocv-degradation-diagnostic]]
- [[dubarry-mechanistic-mode-synthesis]]
- [[22p-physics-or-degeneracy]]
- [[pvs-sev-lli-lampe-separability]]
