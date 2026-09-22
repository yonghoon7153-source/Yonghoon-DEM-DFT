---
title: Fitting Degeneracy (LLI/LAM 분리가능성)
description: "full-cell 곡선 하나로 LLI·LAM_PE·LAM_NE 를 가를 수 있는가 — flat valley(데이터 한계)와 multimodal(최적화 난이도)의 구분"
created: 2026-08-11
updated: 2026-09-22
type: concept
tags: [battery, degradation, research]
sources: [raw/repositories/degradation-degeneracy-audit.md, raw/papers/lin2024_ocv-degradation-mode-identifiability.md, raw/papers/schaeffer2024_nullspace-regularization-interpretation.md, raw/papers/navidi2024_piml-degradation-diagnostics-comparison.md, raw/papers/marongiu2016_lfp-onboard-capacity-halfcell.md, raw/papers/vadhva2021_eis-for-assb-theory-methods.md, raw/papers/yu2024_drt-time-resolved-aging-sulfide-assb-fullcell.md]
confidence: high
explored: false
verificationStatus: unverified
model: claude-fable-5
effort: high
claimType: mixed
evidenceScope: multi-source-primary
---

# Fitting Degeneracy (LLI/LAM 분리가능성)

## 정의
full-cell 전압 곡선 하나를 alpha-beta 반쪽셀 재구성으로 fitting 할 때, 서로 다른
열화 조합 (LLI, LAM_PE, LAM_NE) 이 **구분 불가능하게 같은 곡선**을 만드는 현상.
degeneracy 가 있으면 fitting 이 낸 분해값은 물리가 아니라 최적화 우연이다 —
[[22p-physics-or-degeneracy]] 의 핵심 전제.

## 두 실패 모드 (처방이 정반대)
- **flat valley** — 같은 목적함수 값(J)인데 해가 서로 멀다. 데이터가 그 조합을
  구분하지 못한다는 **직접 증거**. 초기값을 잘 줘도 사라지지 않고, 측정 방식을
  바꿔야 줄어든다.
- **multimodal** — J 가 다른 국소최소가 여럿. degeneracy 가 아니라 **최적화
  난이도**. 좋은 초기값(warm start)으로 사라진다.
- 이 구분을 위해 multi-start 진단은 무작위 restart 끼리만, 공정 비교는 같은
  restart 예산·index 집합으로 한다 ([[degradation-degeneracy]] 의 paired 설계).

## ★ 닫힌 형태로 알려진 null 방향 하나 (2026-09-03 추가)

지금까지 이 페이지의 flat valley 는 **수치로 발견되는 것**이었다. 그런데
[[np-lip-ocv-reparametrization]] (Lin & Khoo 2024, *J. Power Sources* 605,
234446) 이 그중 한 방향을 **해석적으로** 인쇄한다.

SOC 로 정규화한 full-cell OCV 곡선의 **형상**은 두 비(比)에만 의존한다
(`[인쇄]` "the shape of an OCV curve … is **only governed by two degrees of
freedom**"). 그 두 비는 세 모드의 **1 마이너스 값의 비**로만 결정되므로
(원전 식 16):

```
(1−LLI, 1−LAM_NE, 1−LAM_PE) → c·(1−LLI, 1−LAM_NE, 1−LAM_PE)   ⟹ 곡선 형상 불변
특히 pristine 에서:  LLI = LAM_PE = LAM_NE = x  ⟹ 곡선이 pristine 과 완전히 동일
```

즉 **세 모드가 같은 비율로 진행하면 SOC 정규화 곡선에는 아무 흔적도 남지 않고,
총용량만 `1−x` 배가 된다.** 이 방향은 노이즈·최적화와 무관한 모델 자체의 성질이라
국소가 아니라 **구조적**이며, 격자에 truth 쌍으로 **직접 심어 시험할 수 있다**
(수치로 찾은 방향과 검증력이 다르다). 원전 자신은 이것을 축퇴라고 부르지 않고
표기법상의 `[인쇄]` "redundancy" 라고 부른다.

**주의 — 완전한 축퇴는 아니다**: 총용량은 이 방향을 따라 변하므로
**형상 2 + 측정 총용량 1 = 3** 으로 원리적 복원은 가능하다. 남는 문제는
유일성이 아니라 **조건수**이고, 원전 Fig. 9 가 그 조건수가 대부분의 SOC 창과
대부분의 regime 에서 매우 나쁘다는 것을 CRLB 로 보여 준다.

## ★ 그 방향을 **그리는** 법 (2026-09-03 추가)

위 절이 "무엇을 그릴지" 를 주었다면, [[nullspace-coefficient-interpretation]]
(Schaeffer et al. 2024, *Comput. Chem. Eng.* 180, 108471) 이 **어떻게 그릴지**를
준다. 두 문헌은 짝이고, 서로를 인용하지 않는다 (어휘가 달라서 —
Lin 은 `nullspace` 0회, Schaeffer 는 `identifiability` 0회).

**동치 관계** (`[해석]`, 재료는 `[인쇄]`): 선형 최소제곱의 Hessian 은 정확히
`2XᵀX` 이고 `𝒩(X) = 𝒩(XᵀX)` 이며, 등분산 가우시안이면 Fisher 는 `XᵀX/σ²` 다.
즉 **Schaeffer 의 `𝒩(X)` 와 Lin 의 `C_θ⁻¹` 의 영/최소 고유공간은 같은 대상**
이다. 우리 비선형 문제에서는 `X` 자리에 **Jacobian `J(θ)`** 가 들어간다.

**절차 (미실행, 값이 싸다)** — 원전 식 (19)·(23) 을 그대로 옮긴 것:

```
1. 동작점 θ₀ 에서 J = ∂(모델 곡선)/∂θ 를 수치 미분으로 구한다
2. JᵀJ 를 고유분해 → 최소 고유벡터 u_min 과 고유값 스펙트럼
   ⟹ 예측: u_min 이 위 절의 (1−LLI, 1−LAM_NE, 1−LAM_PE) 방향과 정렬해야 한다
      (해석해의 수치 검증. 이 위키가 그 방향을 인쇄만 하고 확인한 적이 없다)
3. θ₀ ± t·u_min 을 따라 곡선을 그려 겹쳐 보인다 (원전 Fig. 1b 의 우리 판)
   대조군으로 θ₀ ± t·u_max 도 함께 그린다
4. t 를 로그로 쓸며 목적함수 증가량을 그린다 → flat valley 의 폭을 물리 단위로
5. 원전 식 (23) 의 허용 손실 c 를 우리 잡음 수준에서 잡으면
   "측정 잡음 안에서 구별 불가능한 열화 조합의 집합" 이 직접 나온다
```

**왜 정확 사영(원전 식 14)이 아니라 완화판(식 19)인가**: 원전은 `p ≫ n` 이라
`𝒩(X)` 가 **정확히** 959차원인 반면, 우리는 미지수 3~4개에 관측이 곡선 전체라
`𝒩(J)` 가 일반적으로 `{0}` 이다. 즉 **우리 축퇴는 정확 null 이 아니라 근사
null(작은 특이값)** 이고, 식 (19) `v_γ = −(γ JᵀJ + I)⁻¹ θ_Δ` 는 `JᵀJ` 가
정칙이어도 정의되며 특이값 크기에 따라 "데이터가 말이 없는 방향" 을 연속적으로
골라낸다. 덤으로 `XXᵀ` 역행렬을 피한다 (`[재현]` 원전 데이터에서 열 평균중심 후
`cond(XXᵀ) ≈ 2.1e17` — 원전 식 (14) 의 전제가 원전 자신의 전처리로 깨진다).

**★ 이 그림이 이 계보에 없다는 것도 확인됐다.** Schaeffer 저장소 노트북에
`scipy.linalg.null_space` 로 기저를 그려 본 셀이 있고, 바로 아래 저자 주석이
`[인쇄]` "It's **difficult to interpret when visualized this way** … orthogonal
unit vectors which can be difficult to visualize (and interpret)" 다. 실패
원인은 **차원(959)** 이지 발상이 아니다 — 우리 null 방향은 1차원이므로 그
장애가 없다.

## ★ 야생 실측 1건 — 그리고 "산포는 오차의 하한이 아니다" (2026-09-03 추가)

이 페이지의 **multimodal 가지**가 실측 셀에서 관측된 사례가 하나 나왔다.
Navidi et al. 2024 (*Energy Storage Mater.* **68**, 103343, raw:
`raw/papers/navidi2024_piml-degradation-diagnostics-comparison.md`) 은
**우리 창 모델과 좌표가 글자 그대로 같은** 4-파라미터 반쪽전지 적합
(`m_p ↔ α_PE, δ_p ↔ β_PE, m_n ↔ α_NE, δ_n ↔ β_NE`, 컷오프 등식 제약 **없음**)
을 실측 LCO‖Gr 셀에 돌리고, 부록 A2 에서 이렇게 적는다:

> `[인쇄]` "the optimization problem for automatic fitting **has multiple local
> minima, leading to run-to-run variability in optimal active mass parameters
> depending on the initial guess**. We illustrated this variability by
> presenting the mean and error bars (spread) derived from **five optimization
> runs, each starting at a different initial guess**."

`[도표, Fig. 15]` 그 산포는 정규화 활물질 단위로 **±1.5 ~ ±11 %p**, 중앙값
≈ ±5 %p 다 — 우리 판정 임계 `tol = 2 %p` 의 **1~5배**.

**★ 그런데 같은 그림이 이 진단의 한계도 준다.** 같은 셀의 해체 실측(자홍
마름모)과 대조하면 `[도표]`: G2C1 의 `m_p` 에서 자동 적합 5개 해가 전부
0.835–0.935 안에 있는데 **해체 실측은 0.63** 이다. 즉

> **다중시작 산포는 실제 오차의 하한조차 아니다.** 다섯 해가 서로 가깝다고
> 해서 참값 근처라는 뜻이 아니다.

`[해석]` 이것은 [[nullspace-coefficient-interpretation]] 의 "낮은 잔차 ⇒
참에 가깝다" 반증과 **같은 계열의 두 번째 형태**다 (거기는 잔차, 여기는
해의 산포). 우리 저장소가 multi-start 산포를 degeneracy 증거로 쓸 때
반드시 붙어야 할 경고이며, 우리는 참값을 알기 때문에 **산포 vs 실제 오차**
산점도를 그려 이 관계를 직접 정량할 수 있다 (미실행, 기존 artifact 재집계).

**원전이 못 한 구별을 우리는 한다**: 그들은 5개 해의 **목적함수 값을 보고하지
않으므로** flat valley 인지 multimodal 인지 판별할 수 없다. 그럼에도 그
결론으로 자동 적합을 기각하고 **사람의 수동 적합**을 정답으로 삼는다.
그 수동 절차는 `(m_n, δ_n)` → `(m_p, δ_p)` **블록 교대**다 (부록 A1) —
좌표 갱신 순서가 degeneracy 를 줄이는지는 값싸게 시험 가능하다 (미실행).

## ★ 닫힌 형태 null 방향 **둘** 더 — 그리고 그것이 모드 층에만 있다는 것 (2026-09-03 추가)

위 절의 Lin 방향이 **관측(곡선 형상)** 쪽 축퇴라면, 이번 것은 **매개화** 쪽
축퇴다. Marongiu et al. 2016 (*J. Power Sources* **324**, 158–169, raw:
`raw/papers/marongiu2016_lfp-onboard-capacity-halfcell.md`) 이 모드 5개 →
창 좌표 4개 사상을 **식으로 전부 인쇄한다** (식 2–5). 거기서 null 이 손으로
풀린다 (`[해석]` 계산은 이 위키가 했다. 상세·수치 검증은 raw digest §5,
계보 표는 [[halfcell-window-parametrization-lineage]]):

```
좌표: (ΔLLI, ΔLAM_Pe,Li, ΔLAM_Pe,De, ΔLAM_Ne,Li, ΔLAM_Ne,De),  N = 로딩비 Q_Ne,BOL/Q_Pe,BOL
n₁ = ( −N ,  0 ,  0 , +1 , −1 )
n₂ = ( +1 , −1 , +1 ,  0 ,  0 )
```

`[재현]` 두 방향 모두 네 창 좌표(및 평행이동 불변 관측 셋)와 **총용량을 정확히
불변**으로 둔다. `n₁` 은 [[dubarry-mechanistic-mode-synthesis]] 가 준
`{LAM_liNE = x} ≡ {LAM_deNE = x, LLI = LR·x}` 의 계수까지 확인해 주고,
둘을 합치면 **[[birkl-ocv-degradation-diagnostic]] 의 3-파라미터 좌표가 정확히
`ℝ⁵/span{n₁,n₂}`** 다 (`[재현]` 두 방향을 그 세 좌표에 넣으면 전부 0).

**★ 우리에게 중요한 것은 이 축퇴가 어디에 있느냐다.** `n₁·n₂` 는 **모드 →
창** 층의 성질이다. 우리 파이프라인은 창 좌표 4개를 **직접** 맞추고 모드 층을
만들지 않으므로 **이 두 방향을 물려받지 않는다.** 그러나 사후 변환
(`LAM_PE = 1 − α_PE·r` 등)이 **몫공간으로의 사영**이므로 **우리 출력도 처음부터
몫공간의 값**이다. [[22p-physics-or-degeneracy]] 가 묻는 것은 **그 몫공간
안에서의** 축퇴이고, 두 층을 섞어 인용하면 안 된다.

## ★ 세 번째 실패 모드 후보 — 중복 관측이 최적화를 **방해**한다 (2026-09-03 추가)

같은 원전이 이 페이지의 flat valley / multimodal 2분법에 안 들어가는 현상을
하나 인쇄한다. `[인쇄]` 관측(평탄역 길이) 셋 중 둘이 비례한다 — "if during the
battery lifetime the length of one of the two plateaus decreases, **the other one
will decrease proportionally**" — 즉 **관측의 유효 rank 가 3이 아니라 2**다.
그런데 그 중복 관측을 넣었을 때 결과가 **더 나빠졌다**:

| 시나리오 | 충전 오차 평균 / % | 방전 / % |
|---|---|---|
| 평탄역 **3개** | 0.98 | 1.10 |
| 평탄역 **2개** | **0.78** | **0.70** |

`[인쇄]` 저자의 설명: "the change of one of the degradation modes can generate a
reduction of the error related to a single plateau but **the increase of the
other ones** … the algorithm can **enter a closed loop and converge to an
imprecise solution**."

`[해석]` 이것은 flat valley(데이터 한계)도 multimodal(국소최소 다수)도 아니다 —
**중복 관측이 목적함수 지형을 나쁘게 만드는** 세 번째 경로다. ⚠ 그 원전의
목적함수는 `L^∞`(또는 합 — 원문 안에서 불일치, raw digest §10 ③)이고 우리는
`L²` 이므로 **메커니즘을 그대로 옮길 수 없다.** 그럼에도 우리 2026-08-20
dQ/dV 결과(항을 더했더니 나빠졌다)에 대해 [[np-lip-ocv-reparametrization]] 의
점검 B2("자유도를 못 늘린다")와 **경쟁하는 두 번째 설명**을 준다. 우리는 참값과
목적함수 값을 둘 다 저장하므로 이 페이지의 flat valley ↔ multimodal 구분으로
**갈라낼 수 있다** (미실행).

## ★ 초기값이 답을 지배하는 것을 통제 대조군으로 본 사례 (2026-09-03 추가)

같은 원전이, 관측을 **일부러 줄여** 축퇴를 키운 상태에서 초기값 하나만 바꾼
대조를 인쇄한다 (`[인쇄]`, 원전 Table 5):

| 평탄역 1개만 | 충전 오차 / % | 방전 / % |
|---|---|---|
| `LAM_start = 10 %` | 6.38 | 4.33 |
| `LAM_start = 0 %` | **14.46** | **12.51** |

`[인쇄]` 저자의 설명: "the smaller initial value of the LAM_Ne **which is kept
for the final calculation** … due to the **lack of information to track this
mechanism**."

`[해석]` [[nullspace-coefficient-interpretation]] 의 일반 명제("축퇴 방향 위의
값은 데이터가 아니라 정칙화가 고른다")의 **야생 실측**이며, 이 계보에서 처음으로
**관측 개수를 통제한 대조군**과 함께 나타났다. 우리는 참값을 알므로 같은 설계로
"초기값 → 실제 오차" 를 정량할 수 있다 (기존 artifact 재집계, 미실행).

## 판정 방법 (요약)
정답을 아는 합성 격자에서 복원 오차 |err| 와 tol(2%p) 기반 degenerate 판정,
clean 바이어스 보정, 복원가능군 한정 집계. PE·NE 가 같은 부호로 묶이는
flat 방향의 비율이 "LAM_PE ≈ LAM_NE 는 수학" 가설의 직접 증거 후보.

## 인접하지만 다른 분해 (혼동 주의)
- [[thermo-kinetic-loss-partition]] — 전압 손실을 **열역학 ΔE / 동역학 η** 로
  가르는 분해 (Tao 2025). 이름이 "degradation pattern decoupling" 이라 이 카드와
  같은 문제처럼 읽히지만 **미지수 정의가 다르다**: LLI·LAM_PE·LAM_NE 가 **전부
  ΔE 한 칸 안**에 들어간다. 즉 그 분해가 완벽해도 이 페이지의 질문은 그대로
  남는다. 원전 자신이 그 셋을 가르는 것을 "Hard to decouple" 이라고 인쇄한다.

- [[piml-physics-injection-points]] — 위 Navidi 2024 처럼 **정답 자체가 이
  적합의 산물**인 파이프라인이 이 계보에 다섯 편 있다. 그 여섯째 자리(라벨)는
  방법 간 비교로는 원리적으로 검출되지 않는다.

## 한계
- 판정은 tol 임계와 guard-feasible 모집단에 조건부다.
- 위 "그리는 법" 은 **국소**다 (`J` 는 `θ₀` 에서만 정의된다). 멀리 떨어진 두
  해가 같은 곡선을 내는 **전역** 축퇴는 여전히 격자 스캔이 있어야 한다.
- 수치는 위키에 복사하지 않는다 — 정본은 artifact 와
  `degradation-degeneracy/docs/RESULTS*.md` ([[provenance-fail-closed-verification]]).

## 전고체에서는 같은 축퇴가 아니다 (2026-09-16)

여기 적힌 축퇴는 **액체셀 5-파라미터**(`a_PE b_PE a_NE b_NE γ_Si`)의 것이다.
전고체는 음극(Li-In·Li 금속·무음극)의 OCP 가 평탄해서 `a_NE`·`b_NE`·`γ_Si` 셋의
민감도가 **정확히 0** 이 된다 — 축퇴가 심해지는 게 아니라 **파라미터가 3 개로 줄고
이 페이지의 최악 축퇴가 사라진다.** 대신 `LAM_PE ↔ 접촉 손실`이 그 자리를 차지한다.
물음과 수집 지침은 [[assb-contact-loss-vs-lampe]], 실측은
`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §1.

## ★★ 다른 관측 영역에서 같은 축퇴가 **분야의 공식 문장**으로 인쇄돼 있다 (2026-09-22)

이 페이지의 계보(OCV·용량 영역)는 [[mode-identifiability-unmeasured-lineage]] 가
정리했듯 **축퇴를 세 번 인쇄하고도 한 번도 null 을 풀지 않았다.**
**EIS 영역은 다르다** — `assb` 10호(Vadhva et al. 2021, *ChemElectroChem* 8, 1930,
`raw/papers/vadhva2021_eis-for-assb-theory-methods.md`)는 그 분야의 **방법론 리뷰**
이고, **비유일성을 명제로 적어 둔다** (전부 `[인쇄]`):

> "**As no solution to an EIS spectrum is unique**, and **the inclusion of more
> elements will tend to improve the fit** of the equivalent circuit model (ECM),
> standard scientific modelling practice should be adhered to, i.e., **using the
> simplest ECM with the fewest elements possible** and ensuring that physical and
> chemical meaning is maintained."

> "it is often challenging to **decipher how many time constants are present** in
> a given dataset and their assignment can be **highly subjective**."

> "**The non-uniqueness of an ECM solution** to an impedance spectrum means that
> **information theory** can be used to rank various ECMs against each other, for
> example, by the **Akaike information criterion (AIC)**."

★ **세 가지가 이 페이지의 어휘와 정확히 대응한다**:

| 이 페이지의 개념 | EIS 쪽의 같은 것 |
|---|---|
| **flat valley** (데이터가 방향을 구속 못 함) | **중첩된 시상수** — 원호 하나에 `R_b + R_gb`, 또는 `R_MF` 에 접촉 손실 + 계면상 |
| **null 방향을 그려서 보인다** | **DRT** — 단 `[인쇄]` "mathematically **ill-posed**, requiring **regularization**" |
| **모델 선택을 잔차로 하지 않는다** | `[인쇄]` "more elements **will tend to improve the fit**" → **AIC** |
| **여기(excitation)를 늘려 깬다** | **저온으로 시상수 벌리기 · 가압으로 큰 항 제거 · 대칭셀 쌍 · 다변수(온도·압력·SoC) 시험** |

`[해석]` **그러므로 "축퇴를 문헌이 아예 모른다" 는 진술은 영역 의존이다.**
용량·OCV 영역(이 페이지, 액체셀 17/17 편)에서는 아무도 쓰지 않았지만,
**EIS 영역에서는 표준 문장이 있다 — 다만 거기서도 누구도 재지 않았다**
(10호에 `identifiab*`·`uncertaint*`·`confidence`·`condition number`·`error bar`
**전수 0 회**, `assb` **10/10 편이 0**). ★ **AIC 조차 `[인쇄]` "only recently been
applied to simulated immittance data" 이고 ASB 실험 적용은 0 이다.**
→ 축퇴를 어디에서 어떻게 깨는지는 [[assb-lampe-contact-product-degeneracy]] ·
[[assb-contact-loss-vs-lampe]].

### ★★★ 갱신 (2026-09-22, `assb` 11호 Yu et al. 2024) — 그 표준 문장을 실제로 돌리면 무슨 일이 나는가

10호는 **리뷰**였다. `assb` **11호(Yu et al. 2024, *J. Power Sources* 597, 234116)**
가 그 처방(DRT)을 실제로 돌린 첫 편이고, **위 표의 두 번째 줄이 데이터로 나타난다.**

★★ **축퇴가 한 층 위에 있다는 것이 확인됐다.** 이 페이지는 지금까지 **파라미터
값**(`X1 ↔ X3`, `LAM_NE ↔ γ_Si`)의 축퇴를 다뤘다. 11호가 보여 주는 것은
**모델 차수 자체가 정해지지 않는다**는 것이다 — 분해되는 DRT 봉우리 수가
`[도표]` **노화로 늘고(3 사례) · 개입으로 줄고(1 사례) · 배선으로 바뀐다(1 사례).**
전용 페이지: **[[drt-peak-count-nonidentifiability]]**.

★★★ **그리고 이 계보에서 처음으로 "축퇴의 폭" 을 잴 재료가 지면에 있다** —
`[도표]` Fig. S3 가 **같은 셀에서 계측 경로만 바꿔** DRT 봉우리를 **−15 % ~ +69 %**
움직인다. 그런데 **같은 논문 본문의 개입 효과가 −10 ~ −25 %** 로 **그 폭 안**이다.
`[해석]` 우리 어휘로는 **nuisance 하나에 대한 근최적 폭의 1 점 표본**이고
([[near-optimal-set-width-measurement]]), **논문은 그것을 "폭" 이라고 부르지도,
본문의 점추정 옆에 놓지도 않는다** (`uncertaint*`·`uniqu*`·`regulariz*`·
`Kramers` 본문 + SI **전수 0 회**).
⚠ **단서**: 배선 변화의 일부는 진짜 물리이고, 두 측정의 대역이 **1 MHz ↔ 2 MHz**
로 다르며, SI 가 "같은 셀" 을 명시하지 않는다 → **69 % 는 상한이다.**

★ **provenance 층위에 칸 하나를 더한다**: **`inverted-nonunique`** — 라벨이
**ill-posed 역변환의 출력**이고 그 **정규화 설정이 보고되지 않은** 경우.
9호(Huo 2025)의 `fitted-single-parameter` 위층이다.

⚠ **Q4 계보의 다섯 번째 형태**: 안 쟀다(1–7호) → 이름이 로드맵 실패 모드에(8호) →
지문이 자기 표 안에(9호) → 방법의 비유일성이 분야의 공식 문장(10호) →
**잴 재료를 SI 에 인쇄해 놓고 뺄셈을 안 했다(11호).**
**"쟀다" 는 여전히 `assb` 0 / 11 편이다.**

## 모양이 같고 물리량이 다른 이웃 — 팩 결함 검출 (2026-09-22)

[[isc-detection-vs-balancing-masking]] (`pack-fault` 섹션의 닻) 은 **이 페이지의 축퇴가
아니다** — 미지수가 LLI/LAM 이 아니라 **한 셀의 누설 전류**다. 그런데 문제의 **모양**이
같다: 두 원인(누설 vs 자기방전·용량 편차)이 같은 관측을 만들고, 그 위에 **조작(균등화)**
이 겹치며, 유일성을 아무도 재지 않았다. 그쪽 1호(Lai 2025)의 Fig. 7 은 이 페이지 어휘로
**nuisance(SoH) 한 방향의 근최적 폭**이다. 이 페이지에 `pack-fault` 태그는 붙이지 않는다
(SCHEMA 경계 ②) — 링크만 둔다.

## 이 개념이 속한 논지

[[mode-identifiability-unmeasured-lineage]] — 이 계보가 축퇴를 세 번 인쇄하고도
(Dubarry 식 · Birkl 산문 · Marongiu 식) 한 번도 null 을 풀지 않았다는 것, 그리고
위 "그리는 법" 의 기계가 옆 논문에 있는데 **두 논문이 서로를 인용하지 않는다**는 것.
