---
title: PVS·SEV 는 LLI 와 LAM_PE 를 가르는가
description: "Do the two physics-inspired features add an independent direction separating LLI from LAM_PE, or do they share one contrast"
created: 2026-09-03
updated: 2026-09-03
type: research-question
tags: [battery, degradation, research]
sources: [raw/papers/2026-09-02-siwon-kim-degradation-mode-ml-seminar.md, raw/transcripts/2026-09-03-voice-memo-007-degradation-mode-ml.md, raw/papers/birkl2017_degradation-diagnostics-ocv.md, raw/papers/wang2025_interpretable-ml-battery-prognosis.md, raw/papers/kim2023_graphite-heterogeneity-lifetime.md, raw/papers/su2024_drt-soh-health-features.md, raw/papers/rhyu2025_systematic-feature-design-formation.md, raw/papers/zhang2020_eis-gpr-capacity-rul.md, raw/papers/tao2025_nondestructive-degradation-decoupling.md, raw/papers/lin2024_ocv-degradation-mode-identifiability.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: empirical
evidenceScope: multi-source-primary
status: open
feedsInto: "[[mode-observability]] Phase 1–2 + 2026-09-02 세미나 discussion point 1"
---

# PVS·SEV 는 LLI 와 LAM_PE 를 가르는가

> [!question] [[pvs-sev-degradation-mode-features]] 의 두 feature 를 함께 쓰면
> LLI 와 LAM_PE 가 **서로** 분리되는가, 아니면 둘 다 같은 하나의 대비
> (양극+재고 그룹 vs 음극)만 재고 있는가?

## 왜 중요한가

2026-09-02 세미나의 프레임워크는 **전극 수준** 3종(LLI·LAM_PE·LAM_NE)을
예측한다고 주장한다. 그런데 물리 feature 두 개가 같은 대비만 잰다면, 전극
수준 출력 중 LLI ↔ LAM_PE 의 분리는 **물리 feature 가 아니라 다른 입력**
(현재 SOH · 프로토콜 식별자)에서 나온다. 그렇다면 "physics-inspired →
해석 가능" 이라는 주장의 사슬이 그 지점에서 끊긴다.

같은 질문이 우리 쪽에도 되돌아온다. [[degradation-degeneracy]] 는 full-cell
OCV 하나로 세 모드를 가를 수 있는지를 판정하는데, **관측을 늘리면 갈리는가**
가 이 프로젝트의 자연스러운 다음 질문이다. PVS·SEV 는 그 "늘린 관측" 의 구체적
후보이므로, 이 카드의 답이 곧 우리 목적함수 확장의 근거가 된다.

## 가설

- **H1 (주가설)**: 두 feature 는 `{LLI, LAM_PE}` vs `{LAM_NE}` 라는 **하나의
  대비**만 재고, LLI ↔ LAM_PE 방향에는 거의 정보가 없다. 따라서 두 feature 를
  더해도 그 방향의 [[fitting-degeneracy]] 는 닫히지 않는다.
- **H2 (귀무)**: 부호는 같아도 **크기 비(比)** 가 모드마다 달라
  `(PVS, SEV)` 2차원이 실제로 두 방향을 준다. 즉 LLI 와 LAM_PE 가 PVS–SEV
  평면에서 서로 다른 기울기의 궤적을 그린다.

H2 가 참일 수 있음에 주의한다 — 부호가 같다고 벡터가 평행한 것은 아니다.
이 카드는 **부호표만으로 H1 을 확정할 수 없다**는 것을 명시적으로 안고 간다.

## Evidence For (H1 지지)

- **[2026-09-03] 부호 패턴이 두 feature 에서 동일하다.** 원문 p.8(PVS, P2D
  단독 모드 스윕)과 p.11(SEV, stoichiometric window 모식도)에서 LLI ↑,
  LAM_PE ↑, LAM_NE ↓ 로 같다. 부호표는
  [[pvs-sev-degradation-mode-features]] 에.
- **[2026-09-03] permutation importance 가 물리 feature 를 뒤로 민다.**
  원문 p.13 도표에서 읽은 근사값 기준, **PVS 는 네 target 모두에서 최하위권**
  (~0.06–0.16)이고 LAM_PE 예측은 **SOH(~0.56) + voltage window(~0.36)** 가
  지배한다. window 는 프로토콜 식별자다 — 즉 LAM_PE 분리는 물리 신호가 아니라
  "이 프로토콜에서 이만큼 닳았으면" 이라는 그룹 궤적으로 설명될 여지가 크다.
  (수치는 도표에서 눈으로 읽은 것이며 원문 도표가 정본이다.)
- **[2026-09-03] 원문이 반대 근거를 제시하지 않는다.** p.8 은 모드를 **하나씩**
  넣은 단독 스윕만 보여 주고, 두 모드를 동시에 넣었을 때 두 feature 가
  분리되는지에 대한 도표가 없다.
- ~~**[2026-09-03] SEV 축에 대한 문헌 전례: LLI 와 LAM 이 R_ct 를 같은 방향으로
  민다.**~~ → **[2026-09-03 (6)] 철회.** 원전([[zhang2020-eis-aging-dataset]] 을
  쓴 Su et al. 2024, *J. Energy Storage* 90, 111770, DOI 10.1016/j.est.2024.111770)
  을 직접 확인한 결과 **이 항목은 H1 의 근거가 되지 못한다**. 세 가지가 드러났다:
  - **(a) Su 는 LLI 도 LAM 도 재지 않는다.** 본문 전체에서 두 약어는 네 번
    나오고 **전부 수치 없는 서술**이다. half-cell OCP fitting·ICA/DVA 분해·
    해체분석·모드 시뮬레이션 어느 것도 없다.
  - **(b) 문제의 문장은 상속된 인용이다.** Su 원문
    `[인쇄, p.6]`: "These trends are **in line with the fact that** the loss of
    stock (LLI) and loss of active material (LAM) in the electrode makes the
    charge transfer process more difficult with the battery aging **[20]**."
    → 진짜 원전은 **Jiang et al., *Appl. Energy* 322 (2022) 119502** 이고,
    Su 는 자기 DRT 추세를 그 진술로 **해석**했을 뿐이다. 리뷰는 이것을
    "Su et al. … **observed**" 로 옮겨 **증거 등급을 한 단계 올렸다**.
  - **(c) Su 자신의 그림이 그 문장과 어긋난다.** Su 가 "charge transfer" 로
    이름 붙인 peak 은 **p₂** 인데, Fig. 5 에서 p₂ 는 5셀 중 4셀에서 노화와
    함께 **감소**한다 (Fig. 7 의 γ(lnτ_p₂) 대 SOH 상관이 4셀에서 **양수**).
    증가하는 것은 저자가 "확산" 이라 부른 **p₃** 다. τ↔f 환산으로는 p₃ ≈
    5–16 Hz 로 오히려 전하전달 대역이어서, 가장 정합적인 재해석은
    **저자의 peak 귀속이 한 칸 밀렸다**는 것이다. 어느 쪽이든 이 논문의
    peak↔과정 대응은 인용에 쓸 수 없다.
  → **결론: 이 문헌 근거는 H1 을 지지하지 않는다.** SEV 설계에 불리한
  문헌 근거는 (적어도 이 경로로는) 존재하지 않는다. 남은 확인 대상은
  **Jiang 2022** 이며, 그것을 보기 전에는 "문헌이 LLI·LAM 의 R_ct 동부호를
  말한다" 고 쓰지 않는다.

- **[2026-09-03 (10)] ★★ PVS 는 "늘린 관측" 이 아니다 — 구조적 상한이 증명된다.**
  [[np-lip-ocv-reparametrization]] (Lin & Khoo 2024) 의 2 자유도 정리:
  `[인쇄]` "the shape of an OCV curve, or the SOC-based OCV, is **only governed by
  two degrees of freedom**, i.e., the N/P and Li/P ratio."
  `[해석]` 여기서 **한 줄 따름정리**가 나온다 —
  > **같은 정규화 곡선에서 파생된 임의의 스칼라 함수(functional)는 모드→관측
  > 사상의 rank 를 늘릴 수 없다.** 곡선이 두 조합 `(r_N/P, z₀⁺)` 만의 함수라면
  > 그 곡선의 어떤 함수도 그 둘만의 함수이고, 곡선이 갖지 않은 null 방향은
  > 그 함수도 갖지 않는다.

  PVS 는 full-cell 곡선의 dQ/dV 에서 계산되는 스칼라다 — 즉 **새 채널이 아니라
  같은 채널의 재가중**이다. 따라서 "PVS 를 목적함수에 더하면 축퇴가 닫히는가" 의
  답은 **곡선의 자유도 관점에서는 아니오**이고, 이것은 부호표나 permutation
  importance 가 아니라 **모델 구조에서** 나온다.

  **같은 논리가 우리 쪽 실측 하나를 설명한다**: [[22p-physics-or-degeneracy]] 의
  2026-08-20 결과 "dQ/dV 항을 더한 목적함수가 더 나빴다" 는 우연이 아니라
  **구조적 필연일 수 있다** (그 카드 Status Log (10) 의 점검 항목 B2. 미검증).

  **범위 한정 3개 — 이 항목을 과대 인용하지 않기 위해 명시한다**:
  (a) 정리는 **SOC 로 정규화된** 곡선에 대한 것이다. PVS 를 **Ah 축** dQ/dV 에서
  계산하면 총용량 정보가 섞여 들어와 셋째 숫자를 실을 수 있다 — 세미나가 어느
  축을 썼는지 원문에 인쇄돼 있지 않다 (**새 Gap**).
  (b) rank 를 못 늘린다는 것과 **조건수를 못 고친다**는 것은 다르다. 재가중은
  노이즈 대비 유효 정보를 바꿀 수 있다 — 다만 null 방향은 못 바꾼다.
  (c) **SEV 에는 적용되지 않는다.** SEV 는 동역학(전하전달 저항) 축이고 Lin 의
  모델에는 동역학이 아예 없다 (`[인쇄]` "we have only discussed inferring
  degradation modes from **OCV measurements**"). `[해석]` 그러므로 이 정리는
  **"두 후보 중 원리적으로 새 채널일 수 있는 것은 SEV 뿐" 이라는 형태로 이 카드를
  좁힌다** — PVS 와 SEV 를 한 묶음으로 다루던 이 카드의 전제가 갈라진다.

## Evidence Against (H2 지지 / H1 반대)
- **[2026-09-03 (10)] ★ 잃어버리는 방향은 LLI↔LAM_PE 가 아니다 — 구조적으로는
  두 모드가 갈린다.** 같은 정리(식 16)를 로그로 쓰면:
  ```
  log r_N/P − log r_ini = log(1−LAM_NE) − log(1−LAM_PE)
  log z₀⁺  − log z₀,ini = log(1−LLI)    − log(1−LAM_PE)
  ```
  `[해석]` 이 2×3 사상의 **kernel 은 `log(1−·)` 공간의 (1,1,1) 방향 하나뿐**이다
  (= 세 모드가 같은 비율로 진행하는 방향). **LLI 와 LAM_PE 는 서로 다른 방식으로
  들어간다** — LLI 는 `z₀⁺` 에만, LAM_NE 는 `r_N/P` 에만, LAM_PE 는 둘 다에
  음부호로. 즉 **SOC 정규화 곡선은 원리적으로 LLI 와 LAM_PE 를 구별한다.**
  H1("두 feature 가 하나의 대비만 잰다")이 참이라면 그것은 **곡선의 구조 때문이
  아니라 조건수·노이즈·feature 선택 때문**이라는 뜻이다 — 이 카드의 논쟁 무대를
  구조에서 실용으로 옮긴다.
  **단, 실용 쪽은 원전이 곧바로 나쁜 소식을 준다**: `[인쇄]` "**estimating 𝑟_N/P
  is harder than estimating 𝑧₀⁺** in most cases here" (Fig. 8). `r_N/P` 는
  LAM_NE 가 사는 유일한 통로이므로, 실측에서 먼저 무너지는 것은 **LAM_NE 방향**
  이라는 예측이 따라온다. 우리 격자에서 확인 가능하고 미실행.

- **[2026-09-03] 두 feature 의 물리 경로가 다르다.** PVS 는 **열역학적**
  신호(OCV 미분의 형상), SEV 는 **동역학적** 신호(charge-transfer 저항)다.
  물리 경로가 다르면 같은 부호라도 모드별 **감도 비**가 다를 개연성이 있고,
  그러면 2차원이 실제로 두 방향을 준다. 이 반론은 아직 반증되지 않았다.
- **[2026-09-03] SEV 의 permutation importance 는 낮지 않다.** LLI(~0.42)와
  LAM_NE(~0.40)에서 SOH 다음가는 크기다. 물리 feature 전체가 무력하다는 강한
  주장은 근거가 없다 — 약한 쪽은 PVS 다.
- **[2026-09-03] 원문 p.13 의 MAE 는 실제로 작다** (0.30–0.57 %p). H1 이
  참이어도 이 수치는 설명되어야 한다. 다만 정답 축이 "Fitted" 이므로 이
  반론의 무게는 라벨 자체의 식별 가능성에 달려 있다 (아래 Gap).
- **[2026-09-03 (7)] ★ 동역학 축이 열역학 축과 독립된 셀-대-셀 정보를 실은
  실측 사례.** Rhyu et al. 2025 ([[fused-lasso-feature-design-framework]],
  raw: `raw/papers/rhyu2025_systematic-feature-design-formation.md`) 의 느린
  형성 32셀에서: 형성 후 C/20 RPT 의 미분용량·d²Q/dV² 가 `[인쇄]` "nearly
  indistinguishable" 인데 (→ 이용상태·잔여 리튬 재고가 거의 같다는 뜻)
  cycle life 는 유의하게 다르다. 저자들은 그 차이를 **미시 입자 전하전달
  저항 분포**(동역학)에 귀속시키고, `[인쇄]` "While the former [평균 저항] may
  be gleaned from simpler features … **the latter [저항 불균일성] is unique to
  the designed features**" 라고 적는다.
  `[해석]` **SEV 쪽에 유리한 근거다.** 열역학 신호가 포화·불변인 상황에서도
  동역학 신호가 셀 간 차이를 실었다는 뜻이며, "PVS 와 SEV 는 물리 경로가
  달라 감도 비가 다를 수 있다" 는 위 반론에 **실측 한 건**을 붙인다.
  **주의 (범위 한정)**: 그 32셀은 (a) 노화 셀이 아니라 **형성 직후** 셀이고,
  (b) SC-NMC532‖AG 이며, (c) LLI/LAM 라벨이 없다(그 논문은 두 약어를 한 번도
  쓰지 않는다). 따라서 이것은 "**SEV 축이 정보를 가질 수 있다**" 까지만
  말하고 "**SEV 가 LLI 와 LAM_PE 를 가른다**" 는 말하지 않는다.

## 이 질문에 답하는 방법 (설계, 미실행)

**[2026-09-03 (9)] 후보 관측이 하나 늘었다 — 전류 축.** 아래 세 경로(PVS·SEV·
제약 추가) 밖에 **네 번째**가 있다: 같은 셀을 **서로 다른 전류**에서 관측하는
것. 근거는 [[thermo-kinetic-loss-partition]] (Tao 2025) — 전류를 바꾸면 ΔE 와 η
의 비중이 바뀌므로 채널이 하나 늘어난다. **주의**: 그 논문은 이 채널로
`{LLI+LAM_PE+LAM_NE}` 대 `{임피던스}` 만 갈랐고 **열역학 안을 가른 적이 없다.**
따라서 이것은 답이 아니라 **새 후보**이며, 판정 절차는 아래 2–3번과 동일하다
(모드 고정 → 두 전류에서 곡선 → 2×3 Jacobian 의 둘째 특이값).

실행 주체는 satellite [[mode-observability]] (Phase 1–2). 우리 파이프라인의
코드를 읽기 전용으로 재사용해 값싸게 판정 가능하다 — **본 실행이 필요 없다**:

1. 합성 truth 격자에서 각 격자점의 곡선으로부터 **PVS 와 SEV 를 계산**한다
   (PVS 는 기존 dQ/dV 경로 재사용, SEV 는 CI 프로토콜 시뮬레이션이 필요).
2. 관측 벡터 `(PVS, SEV)` 의 모드 파라미터에 대한 **Jacobian** 을 수치로
   구한다.
3. **2×3 Jacobian 의 특이값**을 본다. 두 번째 특이값이 첫 번째보다 크게 작으면
   H1, 같은 수준이면 H2. LLI–LAM_PE 방향의 성분을 따로 본다.
4. 기존 OCV 목적함수에 두 항을 더했을 때 **degeneracy 지표가 개선되는지**를
   같은 예산·같은 protocol 로 paired 비교한다 (dQ/dV 항을 더했을 때의 전례가
   [[22p-physics-or-degeneracy]] 에 있다 — 그때는 개선이 관측되지 않았다).

**주의**: 3번까지는 관측의 **국소** 식별 가능성만 말한다. 전역 degeneracy(멀리
떨어진 두 해가 같은 곡선을 내는 것)는 격자 스캔이 있어야 한다 — 우리 쪽 기존
방법론이 그대로 적용된다.

**[2026-09-03 (10)] 위 3번 설계의 정정**: `(PVS, SEV)` 의 2×3 Jacobian 을 그냥
계산하면 안 된다. PVS 는 곡선의 함수이므로 그 행은 **구조적으로
`span{∇r_N/P, ∇z₀⁺}` 안에 갇힌다** (위 Evidence For 의 따름정리). 따라서
- PVS 행만으로는 둘째 특이값이 작게 나오는 것이 **자명**하고 그것은 H1 의 증거가
  아니다 — 좌표계가 만든 결과다.
- 의미 있는 판정은 **`(r_N/P, z₀⁺)` 좌표에서** 하는 것이다: PVS 가 그 2차원 안의
  **어느 방향**을 재는지(단위벡터)를 구하고, `∂/∂LLI` 와 `∂/∂LAM_PE` 가 그
  평면에서 이루는 각과 비교한다. 두 모드 방향이 PVS 축에 거의 평행하게 사영되면
  H1, 크게 벌어지면 H2.
- **SEV 만이 그 평면 밖으로 나갈 수 있는 후보**다 (동역학 축). Phase 2 의 우선순위
  근거가 하나 더 생겼다.
- 추가로 **Fisher/CRLB 를 하한 기준선으로 병기**한다. 우리가 재는 복원 오차가
  문제 고유의 한계인지 추정기 탓인지를 가르는 직접적 도구이고, 계산식이 원전
  식 (36)·(40)·(52)·(56)–(58) 에 전부 인쇄돼 있다.

## Gap (아직 빈 근거)

- **라벨의 불확실성이 원문에 없다.** p.13 의 "Fitted LAM_PE" 에 오차 막대도
  식별 가능성 진단도 붙어 있지 않다. 라벨이 degenerate 하면 MAE 는 "degenerate
  한 라벨을 얼마나 잘 재현했는가" 를 재는 값이다. 이 공백을 메우는 것이 원문
  p.15 discussion point 1("fitting quality 개선")이고, 우리 프로젝트가 직접
  기여할 수 있는 자리다.
  - **[2026-09-03] 이 공백은 세미나가 만든 것이 아니라 원전에서 상속된 것이다.**
    세미나 p.3 이 인용한 라벨 생성 절차의 원전
    ([[birkl-ocv-degradation-diagnostic]], Birkl et al. 2017) 에도 추정값의
    신뢰구간·파라미터 상관·노이즈 스윕이 **전무하다**. 원전의 유일한 오차
    수치 5.4% 는 **코인셀 제작 재현성**이지 추정 불확실성이 아니며, 논문이
    §4.3 에서 그렇게 명시한다. 즉 이 계열의 라벨은 **한 번도 오차 막대를 가진
    적이 없다** — 세미나에 요구할 것이 아니라 우리가 만들어 공급할 것이다.
  - **[2026-09-03 (2)] 이 공백은 ML 쪽 분야 리뷰도 인지하지 못한다.**
    [[interpretable-ml-battery-prognosis-taxonomy]] (Wang et al. 2025,
    *Adv. Energy Mater.* 15, e03067 — 세미나 p.4 가 인용한 바로 그 리뷰) 본문
    전체에서 `uncertainty` `noise` `error bar` `confidence interval`
    `identifiability` `degeneracy` 가 **각 0회**다. 상관·공선성은 SHAP/PDP 라는
    **사후 해석 도구의 신뢰도** 문제로만 두 번 나오고, "feature 가 공선이면
    모델이 target 을 결정하지 못한다" 는 진술은 없다. 저자들이 미해결로 두는
    세 challenge(해석의 깊이 · 해석의 검증 · 데이터 양과 질) 중 **라벨의
    적절성 축은 없다**. 즉 이 Gap 은 한 발표의 누락이 아니라 **두 계보
    (전기화학 진단 / ML 예후)가 만나는 지점의 구조적 공백**이며, 이 카드의
    무게는 그만큼 커진다.
- ~~**[2026-09-03] PVS 의 물리 귀속이 문헌과 어긋난다.**~~ → **[2026-09-03 (5)]
  닫힘.** 원전([[dv-peak-heterogeneity-descriptor]], Kim et al. 2023,
  *ACS Energy Lett.* 8, 2946, DOI 10.1021/acsenergylett.3c00695) 을 본문 + SI
  로 직접 확인한 결과 **전제가 거짓이었다**. 셋 다 다르다:
  (a) **양이 다르다** — 그 논문의 대표 descriptor `Peak_S2` 는 SI 가
  "**the absolute value at the ridge**" 로 정의하는 **절대 peak 높이**이고,
  peak−valley 진폭(`ΔPeak_S2`)은 valley 노이즈 때문에 **버려진 변형**이다
  (ρ 0.75 → 0.82). 리뷰 Fig. 5c 에 그려진 화살표는 그 버린 쪽이다.
  (b) **화학이 다르다** — LFP‖Gr(2상 평탄 OCP) 이라 dV/dQ 극값 구조가 사실상
  흑연의 것이다. 음극 단일 귀속은 그 화학에서 강제된 것이지 일반 법칙이 아니다.
  (c) **좌표를 맞추면 오히려 일치한다** — dV/dQ 의 **ridge** 는 dQ/dV 의
  **valley** 이므로, Kim 의 `Peak_S2` 는 세미나의 `Valley2`(graphite stage-2
  단일상)와 **같은 종류의 특징**이고 둘 다 음극에 귀속된다. 세미나가 양극에
  붙이는 `Peak2`(dQ/dV 의 peak)는 Kim 이 쓰지 않는 쪽이다.
  → **이 Gap 은 H1/H2 판정에 무게를 싣지 않는다.** 대신 아래 새 Gap 이 열린다.
- **[2026-09-03 (5)] ★ DV/IC 극값 진폭이 열화 모드 이외의 상태변수를 싣는다.**
  같은 원전 Fig. S2a(직접 봄): **같은 SOH 80 % 에서** 사이클 조건에 따라
  ΔPeak_S2 가 **0.083 ~ 0.253 V Ah⁻¹ (약 3배)** 로 갈린다 (1C@45 °C 는 오히려
  증가, 2C@25 °C 는 급감). 저자는 이것을 "공간적 리튬화 불균일성" 으로 읽지만,
  같은 데이터는 "**열화 모드 조합이 다르다**"로도 설명된다 — 그 논문은 LLI/LAM
  을 한 번도 재지 않으므로(약어 0회) 둘을 구분할 수 없다. **PVS 에 대한 함의**:
  세미나 p.8 의 모드 스윕은 1D P2D(전극면 방향 분산 없음) 위에서 계산된 것이고,
  실측 셀의 PVS 에는 이 성분이 섞여 들어온다. 즉 PVS 를 모드 관측으로 쓸 때의
  위협은 "어느 전극인가" 가 아니라 "**모드 이외의 상태변수가 같은 축을
  흔든다**" 쪽이다. 이 성분의 크기는 아직 아무도 정량하지 않았고, 우리 합성
  truth 파이프라인은 **모드를 고정한 채** 그 상한을 계산할 수 있다.
- **[2026-09-03 (5)] valley 를 쓰는 feature 의 노이즈 취약성 — 문헌 전례 확보.**
  같은 원전이 valley 를 쓰는 변형을 **실전에서 폐기**했다: `[인쇄]` "because of
  the **fluctuation in the valley** near 0.4 Ah, which is attributed to the
  limited resolution of voltage detection when the voltage plateaued". PVS 는
  valley 를 분자에도 분모에도 쓴다. [[mode-observability]] Phase 1 이 관측한
  valley 정의 민감도(인접 −20.0 vs 창내 전역 최소 −11.3)와 **같은 병**이며,
  대조군으로 **valley 를 쓰지 않는 변형**(peak 절대값)을 넣을 근거가 생겼다.
- **[2026-09-03 (6)] ★ SEV 의 전제(임피던스 유래 feature 의 노화 부호가 안정하다)
  가 실측에서 성립하지 않는 사례가 있다.** Su 2024 Fig. 7 (히트맵을 직접 봄,
  수치는 그림에 인쇄된 값) — 동일 화학·동일 온도(25 °C)·동일 프로토콜의
  **5셀**에서:
  - **전하전달 peak 높이 γ(lnτ_p₂)** 의 SOH 상관이 cell1 **−0.687** 인데
    cell2 **+0.934** / cell3 +0.844 / cell5 +0.751 / cell6 +0.869 —
    **1/5 에서 부호가 뒤집힌다.**
  - **분극저항 R_pol** 은 cell1 −0.965 / cell5 −0.918 인데 cell2 **+0.864** /
    cell6 **+0.854**, cell3 는 −0.397 로 거의 무상관 — **2/5 에서 뒤집히고
    1/5 에서 무의미하다.** "노화하면 분극저항이 오른다" 는 통념이 셀 수준에서
    지켜지지 않는다.
  - 둘 다 저자의 0.75 문턱을 통과하지 못해 **health feature 에서 탈락**했다.
    저자는 상관계수의 **절대값**만 보므로 이 부호 뒤집힘을 진단하지 못하고,
    "cell consistency 차이" 로만 부른다.
  - 원인의 일부가 Su Fig. 1 에 그림으로 보인다: cell1/cell5 는 **R_∞ 증가
    주도**(스펙트럼 평행이동), cell3 는 **반원 성장 주도**(R_∞ 고정),
    cell2/cell6 는 **둘 다 거의 안 변한다** — 같은 조건에서 임피던스 열화
    경로가 셋으로 갈린다.
  `[해석]` **이것은 H1/H2 판정이 아니라 그 두 가설이 다투는 무대 자체에 대한
  경고다.** SEV 는 R_ct 의 **부호 구조**(LLI↑, LAM_PE↑, LAM_NE↓)를 읽어 모드를
  가르려 한다. 부호 구조를 쓰는 feature 는 부호가 셀 간에 안정할 때만 작동한다.
  **Phase 2 는 "SEV 가 모드를 가르는가" 이전에 "SEV 축이 셀 간에 재현되는가"
  를 먼저 물어야 한다.** (데이터·좌표계는 [[zhang2020-eis-aging-dataset]].)
- **[2026-09-03 (6)] DRT peak 을 특정 전극에 귀속시키는 것이 자명하지 않다 —
  실물 사례.** Su 2024 는 셀 수준 EIS 를 DRT 로 풀지만 `positive electrode`/
  `negative electrode` 가 방법·결과부에 **0회**이고, R_ct,PE 라는 양이 등장하지
  않는다. peak↔과정 대응(p₁=SEI, p₂=전하전달, p₃=확산)은 **근거 없이 선언**되며
  (대칭셀·기준전극·half-cell·온도 스윕 전부 없음) 위에 적었듯 자기 데이터와
  어긋난다. `[해석]` SEV 가 "DRT 로 R_ct,PE 를 얻는다" 고 할 때 **그 한 걸음이
  공짜가 아니다.** DRT 는 시간상수를 가르지 전극을 가르지 않는다. 이 공백은
  우리 합성 truth 파이프라인이 메울 수 있는 자리다 (모드를 고정한 채 어느 τ
  대역이 어느 전극인지를 강제로 알 수 있다).
- **[2026-09-03 (6)] 임피던스 유래 feature 는 셀 고유 오프셋을 크게 싣는다.**
  Su Fig. 8 (직접 봄): 같은 feature 값이 셀마다 다른 SOH 에 대응한다 — 예
  γ(lnτ_p₃) = 0.30 이 cell1 에서는 SOH ≈ 95 %, cell3 에서는 SOH ≈ 78 %.
  SOH 70 % 에서 γ(lnτ_p₃) 가 cell3 ≈ 0.50 vs cell5 ≈ 0.25 로 **2배** 벌어진다.
  저자들이 셀 간 학습/시험을 포기하고 셀 **안** 무작위 40/60 분할을 쓴 이유를
  스스로 밝힌다 `[인쇄, p.14]`: "**This is due to the significant difference in
  battery consistency**, not only in terms of initial capacity and decay, but
  also in the EIS." `[해석]` SEV 를 실측에 쓰려면 절대값 대비가 아니라 **같은
  셀 안의 상대 변화**만 써야 할 가능성이 높은데, 모드를 가르는 설계는 **절대적
  부호·크기 구조**에 의존한다 — 두 요구가 긴장 관계다.
- **LOGO-CV 의 group 정의가 원문에 인쇄되지 않았다.** 셀 단위인지 프로토콜
  단위인지에 따라 p.13 수치의 의미가 갈린다. 프로토콜 식별자가 입력에 있으므로
  group 이 셀이면 같은 프로토콜의 형제 셀로부터 예측하는 구조가 된다.
  - **[2026-09-03 (7)] 이 Gap 을 닫는 표준이 같은 줄에 인용돼 있었다.**
    세미나 p.4 의 둘째 인용(Rhyu 2025)은 group = **형성 프로토콜**로 잡고,
    **feature 설계 자체를 outer training set 안에서** 수행하며, feature 설계용
    inner 분할과 하이퍼파라미터용 inner 분할을 `[인쇄]` "**intentionally
    differentiated** … to avoid information leakage" 로 **일부러 다르게** 잡는다
    (SI Fig. S3, 직접 봄). 게다가 선행 연구의 leakage 를 각주로 못 박는다
    (`[인쇄, 각주 49]` Weng et al. 의 8% 는 "having the cells from the same
    formation protocol in **both** their 'validation' set and 'train/test'
    sets"). 즉 이 계보에 **이미 더 엄격한 전례가 있고 세미나가 그것을
    인용하고 있다** — 요구할 근거가 생겼다.
- **[2026-09-03 (7)] ★ agnostic 기준선이 없다 — 그리고 그것을 만드는 법이
  같은 인용 안에 있다.** 세미나 p.13 은 `voltage window`(프로토콜 식별자)를
  물리 feature 와 **같은 상자**에 넣고 permutation importance 를 잰다. 그러면
  "물리 feature 가 프로토콜 식별자를 **넘어서는가**" 를 물을 수 없다.
  [[fused-lasso-feature-design-framework]] 는 프로토콜 파라미터만 쓰는
  **agnostic 모형 52개**를 별도 기준선으로 세우고, 설계 feature 모형이 그것을
  이기는지로 판정한다 — 그리고 agnostic 의 구조적 한계를 스스로 인쇄한다
  (`[인쇄]` 특정 템플릿에만 적용 가능 · "**no cell-to-cell variability**").
  `[해석]` **이 카드의 Evidence For 2번(“LAM_PE 분리가 SOH + window 로 설명될
  여지가 크다”)을 판정 가능한 실험으로 바꾸는 설계가 이것이다**: 프로토콜
  파라미터만 쓴 기준 모형의 LAM_PE MAE 를 먼저 재고, 물리 feature 를 넣었을 때
  그것이 줄어드는지를 **paired** 로 본다. 우리 쪽에서도 값이 싸다.
- **[2026-09-03 (7)] 창(window) 기반 feature 의 계수 부호가 fold 간에
  뒤집힌 사례.** 같은 논문 SI Fig. S5e (직접 봄): 5개 inner fold 의 fused-lasso
  계수 β 가 **설계 feature 가 사는 3.45–3.60 V 구간에서만** 크게 갈리고 부호가
  뒤집힌다 (β^(2) ≈ −0.70 vs β^(5) ≈ +0.37, 근사 판독). 논문은 이 그림을
  **강건성의 증거**로 제시하는데, 그 "robustness" 는 곡선 형상의 DTW 비율
  (< 0.7) 로 정의돼 있어 **국소 부호 안정성을 재지 않는다**.
  `[해석]` PVS 와 SEV 도 **특정 전압창/특정 SOC 지점**의 대비를 쓰는 feature
  이므로 같은 취약성을 공유한다. [[mode-observability]] Phase 1 이 이미 본
  valley 정의 민감도와 같은 계열이며, **"feature 값이 안정한가" 와 "그 feature
  의 회귀 계수 부호가 안정한가" 는 다른 질문**이라는 것을 이 사례가 보여 준다.
  덧붙여, 이 논문 저자들의 계보는 그 진단 도구를 갖고 있다 — 참고문헌 [13] 이
  Schaeffer et al. 의 **nullspace** 논문이고 공저자 4명이 겹친다 — 그런데
  본문에서 그것을 "β 는 해석을 준다" 는 **긍정 근거로만** 인용한다.
- **[2026-09-03 (8)] ★ 관측 "선택" 자체가 공선 대역 안에서 비식별적이다 —
  실측 사례.** [[zhang2020-eis-aging-dataset]] 의 원전(Zhang 2020)은 ARD 로
  120 예측자 중 **두 개**(Im Z at 17.80·2.16 Hz)만 남기고 그것에 물리적 의미를
  부여한다. 그런데 저자들의 **공개 데이터로 우리가 직접 계산**하면 120개 중
  **52개**가 단독으로 |r(용량)| > 0.95 이고, 선택된 91번과 이웃 92번의 상관이
  **0.998** 이다. `[해석]` **"대역이 정보를 갖는다" 와 "그 안의 특정 점이 특정
  물리에 대응한다" 는 다른 주장이며, 후자는 이 데이터로 지지되지 않는다.**
  SEV 는 특정 시간상수/주파수 대역의 값을 R_ct 로 읽는 feature 이므로 같은
  취약성을 공유한다 — [[fitting-degeneracy]] 의 EIS 판이다. 값싼 후속: 셀 제외
  재적합으로 ARD 선택 인덱스의 분포를 내는 것 (남의 공개 데이터로 재현 가능).
- **[2026-09-03 (8)] 불확실성 구간을 그리는 것과 그것이 맞는 것은 다른 주장이다.**
  Zhang 2020 은 이 계보에서 처음으로 ±1 s.d. 음영을 그리지만 보정 검사가 없고
  (`calibrat*` 0회), `[도표]` Fig. 3a/3b 에서 측정 곡선이 그 음영 **밖에 연속
  100 사이클 이상** 머문다. 우리가 라벨에 오차 막대를 공급할 때 **coverage 를
  필수 산출로 넣는** 근거 사례.
- **모드 동시 진행 시의 가법성**이 미확인 (원문 p.8 은 단독 스윕만).
- **SEV 의 정량 모드 스윕**이 없다 (p.11 은 모식도).
- LAM_NE 를 Si loss / Gr loss 로 쪼개면(원문 p.15 point 2) **미지수가 4개로
  늘어난다.** p.8 에서 Si loss 와 Gr loss 는 PVS 를 같은 방향(↓)으로 움직이고
  크기만 다르다 — 새 독립 관측 없이 쪼개면 식별성은 반드시 나빠진다. 이
  귀결은 아직 정량화되지 않았다.
  - **[2026-09-03] 이 패턴의 문헌 전례가 있다.**
    [[birkl-ocv-degradation-diagnostic]] 은 LAM 을 lithiated/delithiated 로
    쪼개려다 정확히 이 벽에 부딪혔고 — "The fractions of lithiated and
    delithiated LAM can therefore **not be uniquely identified** if the
    assumption is that LLI can occur simultaneously" (§4.2) — **쪼개기를
    포기하고 총량 + total-LLI 로 되묶는 것을 알고리즘의 설계 이유로 삼았다.**
    같은 관측(full-cell OCV)을 유지한 채 LAM 을 하위 분할하면 식별성이
    무너진다는 것이 이미 한 번 문서화된 셈이다. Si/Gr 분할이 다른 결과를
    내려면 **새 독립 관측**이 필요하다는 이 카드의 논지를 지지한다.

## Status Log

- [2026-09-03] open — 2026-09-02 세미나 자료(15쪽)와 구술 메모를 raw 로 흡수하며
  개설. 부호표 대조에서 두 feature 의 패턴이 동일함을 발견한 것이 발단.
  아직 계산은 하나도 하지 않았다 — 위 "답하는 방법" 4단계 전부 미실행이며,
  현재 근거는 **원문 도표 판독 + 정성 논증**뿐이다.
- [2026-09-03 (2)] open 유지 — [[mode-observability]] Phase 1 첫 실측 (방향성
  관측, 인용 금지 등급 — 정본은 `mode-observability/results/phase1/pvs.csv` 와
  `mode-observability/docs/PHASE1_NOTES.md`):
  - **22p 동작점 근방에서 ∂PVS/∂모드 세 개가 동부호** → 거기서 PVS 는
    LLI↔LAM_PE 방향을 주지 않는다 (H1 쪽 근거 하나).
  - 단, pristine 에서는 LLI 와 LAM_PE 가 **반대 부호**로 나와 세미나 p.8 과
    다르다 — 부호 구조가 동작점 의존이고, LLI 단독 스윕이 비단조라 feature
    tracking 실패 가능성을 먼저 배제해야 한다 (검증 전 인용 금지).
  - PVS 값이 valley 정의(인접 −20.0 vs 창내 전역 최소 −11.3)에 민감 —
    세미나 p.15 discussion point 3 이 실측으로 확인된 셈.
  - LAM_PE ≥ 0.08 에서 peak 이 창을 벗어나 NaN — PVS 류의 구조적 커버리지
    한계.
- [2026-09-03 (3)] open 유지 — 라벨 절차의 **원전**을 흡수
  ([[birkl-ocv-degradation-diagnostic]]). 이 카드에 준 것은 새 증거가 아니라
  **Gap 두 개의 출처 확정**이다 (위 Gap 절의 2026-09-03 항목 둘): 라벨
  불확실성 공백이 세미나가 아니라 원전에서 상속된 것이라는 점, 그리고 LAM 을
  하위 분할하려다 식별성이 무너진 문헌 전례가 있다는 점.
  **이 카드의 축에 새로 붙는 설계 하나**: 이 카드는 지금까지 "관측을 늘리면
  갈리는가" 만 다뤘는데, Birkl 은 **관측을 늘리는 대신 제약을 더한다** —
  컷오프 전압 2개를 등식(Eq. 11–12)으로 걸어 stoichiometric offset 2 자유도를
  소거한다. **제약 추가**는 위 "답하는 방법" 4단계에 없는 세 번째 경로이고,
  값이 싸다 (새 프로토콜 시뮬레이션이 필요한 SEV 와 달리 기존 곡선으로 된다).
  단, 이 논문의 관측은 **순수 열역학**(저자가 §1 에서 kinetics 를 명시적으로
  범위 밖에 둔다)이므로 SEV(동역학 축)와는 직교하며 서로를 대체하지 않는다.
- [2026-09-03 (4)] open 유지 — 세미나 p.4 가 인용한 **분야 리뷰**를 흡수
  ([[interpretable-ml-battery-prognosis-taxonomy]], Wang et al. 2025). 이 카드에
  준 것 셋:
  - **Evidence For 1건 추가** (SEV 축): "LLI 와 LAM 이 **함께** R_ct 를 올린다"
    는 DRT 관찰이 리뷰에 인쇄돼 있다. SEV 로 두 모드를 가르려는 설계에 불리한
    문헌 근거이며, 원전(Su 2024) 확인 전에는 인용하지 않는다.
  - **Gap 1건 추가**: PVS 와 같은 기하량에 대해 문헌이 **음극 단일 귀속**을
    준다 (Kim 2023). 물리 귀속이 미결이면 부호 구조 논증의 전제가 흔들린다.
  - **Gap "라벨 불확실성" 의 무게 상향**: 이 공백이 원전(Birkl)뿐 아니라
    **ML 쪽 분야 리뷰에도** 있다는 전수 확인 (`uncertainty` 0회 등).
  **이 리뷰가 다루지 않는 것도 함께 기록한다** — 이 리뷰는 (a) 전극 수준
  (LLI/LAM)을 예측 target 으로 삼는 사례를 하나도 싣지 않고, (b) 역문제의
  유일성·축퇴·라벨 불확실성을 다루는 절이 없으며, (c) `OCV`·`half-cell` 이
  본문에 0회다. 즉 **이 카드의 질문에 대한 답을 이 리뷰에서 찾을 수는 없다.**
  이 리뷰가 준 것은 답이 아니라 **좌표계와 공백의 확정**이다.

- [2026-09-03 (5)] open 유지 — 리뷰가 PVS 의 선례로 든 **원전**을 본문 + SI 로
  흡수 ([[dv-peak-heterogeneity-descriptor]], Kim et al. 2023). 이 카드에 준 것 셋:
  - **Gap 1건 닫음**: "PVS 의 물리 귀속이 문헌과 어긋난다" 는 **전제가 거짓**
    이었다. (a) 그 논문의 대표 descriptor 는 peak−valley 진폭이 아니라 **ridge
    절대 높이**이고 진폭 변형은 valley 노이즈 때문에 폐기됐다, (b) 셀이
    **LFP‖Gr** 이라 음극 단일 귀속이 화학에 의해 강제된다, (c) `dQ/dV = 1/(dV/dQ)`
    로 좌표를 맞추면 그 descriptor 는 세미나의 **Valley2**(음극)에 대응해
    **오히려 일치**한다. 세미나의 양극 귀속(Peak2)은 그 논문이 쓰지 않는 쪽이다.
    → 이 Gap 은 H1/H2 어느 쪽에도 무게를 싣지 않는다.
  - **새 Gap 2건**: (1) DV/IC 극값 진폭이 **모드 이외의 상태변수**를 싣는다
    (같은 SOH 80 % 에서 조건에 따라 3배 변동, 원전 Fig. S2a 직접 봄) —
    귀속 논쟁보다 무거운 위협이다. (2) valley 를 쓰는 feature 의 노이즈
    취약성에 **문헌 전례**가 생겼다 (원전은 valley 를 버리는 쪽을 택했고 그래서
    성능이 올랐다).
  - **우리가 공급할 것이 하나 늘었다**: 원전은 시뮬레이션을 한 번도 돌리지
    않으므로(`simulat` 0회) Fig. S2a 의 3배 변동 중 **모드로 설명되는 몫의
    상한**을 스스로 계산할 수 없다. 우리 합성 truth 파이프라인은 모드를 고정한
    채 그 상한을 줄 수 있다.
  **이 흡수의 방법론적 교훈**: 이전 라운드에서 우리는 리뷰 Fig. 5c 를 **직접
  보고** "intensity = peak−valley 진폭" 이라고 적었다. 그림 판독 자체는
  정확했고(그 화살표는 실제로 진폭이다), 틀린 것은 "그림에 그려진 것 = 논문이
  쓴 descriptor" 라는 **한 단계의 추론**이었다. 그림은 본문 서술을 교정하지만
  **본문·SI 를 이기지는 않는다**.

- [2026-09-03 (6)] open 유지 — 리뷰가 SEV 축의 불리한 근거로 든 **원전**을
  흡수 (`raw/papers/su2024_drt-soh-health-features.md`, Su et al. 2024,
  *J. Energy Storage* 90, 111770). 이 카드에 준 것 넷:
  - **Evidence For 1건 철회**: "LLI 와 LAM 이 함께 R_ct 를 올린다" 는
    (a) Su 의 측정이 아니라 **Jiang 2022 [20] 에서 상속된 해석 한 문장**이고,
    (b) Su 는 LLI/LAM 을 **한 번도 재지 않으며**, (c) Su 자신의 Fig. 5/Fig. 7 이
    그 문장과 **부호가 어긋난다**(전하전달로 이름 붙인 p₂ 가 노화와 함께
    **감소**). → **H1 의 문헌 근거가 아니다.** Wang 리뷰가
    "Su et al. … observed" 로 옮기며 등급을 올린 것이 오해의 출처다.
    (리뷰 digest 는 raw 불변층이라 고칠 수 없으므로 **정정은 이 카드와
    [[interpretable-ml-battery-prognosis-taxonomy]] 가 보유한다**.)
  - **Gap 3건 추가** (위 Gap 절): SEV 부호 구조의 셀 간 재현성 실패 사례 ·
    DRT→전극 귀속이 자명하지 않다는 실물 사례 · 임피던스 feature 의 셀 고유
    오프셋. 세 번째와 첫 번째는 Phase 2 의 **첫 물음을 바꾼다** —
    "SEV 가 모드를 가르는가" 이전에 "**SEV 축이 셀 간에 재현되는가**".
  - **데이터 출처 확정**: Phase 2 가 쓰는 EIS 는 Su 가 잰 것이 아니라
    **Zhang et al. 2020, *Nat. Commun.* 11 (Zenodo 3633835)** 의 재사용이다.
    좌표계와 미확인 항목은 [[zhang2020-eis-aging-dataset]] 에.
  - **주의 한 줄**: 그 데이터셋에는 **LLI/LAM 라벨이 없다.** 따라서 Phase 2 는
    이 카드의 질문에 직접 답할 수 없고, **전제(축의 재현성·귀속 가능성)만**
    검증할 수 있다. 이 구분을 흐리면 안 된다.

- [2026-09-03 (7)] open 유지 — 세미나 p.4 의 **둘째 인용**을 본문 + SI 로 흡수
  ([[fused-lasso-feature-design-framework]], Rhyu et al., *Joule* 9 (2025)
  101884, raw: `raw/papers/rhyu2025_systematic-feature-design-formation.md`).
  이 카드에 준 것 넷:
  - **판정 (계보 위치)**: 이 논문은 PVS·SEV 의 **선례가 아니라 대척점**이다.
    자기 프레임을 `[인쇄]` "handcrafted features that are limited by the many
    unknown aspects of the underlying physics" 의 대안으로 놓는다. 절차 안에
    PVS·SEV 같은 유도 스칼라를 넣을 자리가 없다 — 도메인 지식이 개입하는
    유일한 앞단(입력 후보 선정)은 후보를 **지우기만** 한다. 이 판정 자체는
    H1/H2 어느 쪽에도 무게를 싣지 않는다.
  - **Evidence Against 1건 추가**: 동역학 축(입자 저항 분포)이 열역학 축이
    사실상 포화·불변인 상태에서도 셀-대-셀 정보를 실은 실측 사례 — SEV 쪽에
    유리하다. 단 **형성 직후 셀 · LLI/LAM 라벨 없음**이라는 범위 한정을 함께
    적었다.
  - **Gap 3건 추가**: (1) group 정의 Gap 을 닫는 **표준 설계**가 같은 인용
    안에 있었다 (프로토콜 group + feature 설계를 학습 fold 안에 가둠 + 두 inner
    분할을 일부러 다르게), (2) **agnostic 기준선**을 세우면 Evidence For 2번이
    판정 가능한 실험이 된다, (3) 창 기반 feature 의 **회귀 계수 부호가 fold
    간에 뒤집힌** 문헌 사례 (SI Fig. S5e, 직접 봄).
  - **어휘 전수 (이 계보 여섯 편째)**: 합자 정규화 후 본문 15쪽 + SI 19쪽
    전체에서 `degenerac*` **0** · `uncertain*` **0** · `identifiab*` **1** —
    그 1회는 **참고문헌 [30] 의 제목 안**이고 (Lin & Khoo 2024,
    "**Identifiability study** of lithium-ion battery capacity fade using
    **degradation mode sensitivity** …"), 본문에서 그 문헌은 **DVF 기법 4연속
    인용의 넷째**로만 쓰인다. `nullspace` 1회도 참고문헌 [13] 제목 안이다.
    `[해석]` "연속 0회" 는 형식상 깨졌지만 **논문이 자기 추정의 식별 가능성을
    묻는 문장은 여전히 0개**다. 이번 수확은 "Braatz 그룹은 다르다" 가 아니라
    **"이 계보에서 방법론적으로 가장 정교한 팀조차, 그 어휘를 인접 문헌으로
    알고 있으면서 자기 추정에는 적용하지 않는다"** 는 더 강한 형태의 확인이다.
  - **다음 흡수 최우선 후보 확정**: **Lin, J. & Khoo, E. (2024), *J. Power
    Sources* 605, 234446** — 이 계보에서 제목에 identifiability 가 있는 **유일한**
    문헌이고, 우리 프로젝트의 정확한 선행 연구다.

- [2026-09-03 (8)] open 유지 — Phase 2 가 쓰는 **EIS 데이터의 원전**을 본문 + SI
  로 흡수 ([[zhang2020-eis-aging-dataset]] 갱신, raw:
  `raw/papers/zhang2020_eis-gpr-capacity-rul.md`, Zhang et al.,
  *Nat. Commun.* **11**:1706 (2020), DOI 10.1038/s41467-020-15235-7).
  이 카드에 준 것 넷:
  - **주의 한 줄이 확정으로 바뀌었다.** (6) 에서 "그 데이터셋에는 LLI/LAM 라벨이
    없다" 를 Su 원문 근거로 적었는데, 이제 **원전에서 확정**됐다: Zhang 본문 +
    SI 전체에서 `LLI`·`LAM`·`lithium inventory`·`half-cell` 이 **각 0회**이고,
    모드를 재는 절차가 하나도 없으며, Introduction 이 미시 기구 모델링을
    `[인쇄]` "unscalable" 하다며 명시적으로 포기한다. 제목의 "degradation
    **patterns**" 는 **셀마다 다른 감쇠 궤적**을 뜻한다 (본문 용례 2회 = 제목 +
    Discussion). → **Phase 2 는 이 카드의 질문에 직접 답할 수 없다**는 제약이
    한 단계 더 단단해졌다.
  - **Phase 2 의 SOC 축이 2점으로 축소된다** (설계 정정). SI Fig. 1 (직접 봄)
    이 state I~IX 아홉 개를 전부 정의하고 **적·녹 점으로 DC 전류 유무**까지
    준다: **II·III·VI·VII 은 전류가 흐르는 중에 측정**된다. 따라서 평형
    임피던스로 쓸 수 있는 SOC 는 **0 %(I·VIII·IX) 와 100 %(IV·V) 두 점뿐**이고,
    중간 SOC(III ≈40 %, VII ≈57 %)는 DC 바이어스 상태다. SEV 는 R_ct 의
    **stoichiometry 의존성**을 읽는 feature 이므로 이 데이터로는 **곡선이 아니라
    양 끝점 대비**만 얻는다. 대신 `IV vs V`·`VIII vs IX` 라는 **완화 시간 대비**
    축이 새로 보인다 (아무도 안 썼다).
  - **Gap 1건 추가 — 관측 선택 자체의 비식별성 (SEV 축에 직접 걸린다).**
    원전의 ARD 는 120 예측자 중 `[인쇄]` "**only two salient frequencies**"
    (17.80 · 2.16 Hz, SI Fig. 3b 로 **허수부** 확정) 만 남기고 그것에
    **물리적 의미**(계면 물성 변화)를 부여한다. 그런데 저자들의 **공개 데이터로
    직접 계산하면** 120개 중 **52개**가 단독으로 |r(용량)| > 0.95 이고,
    91번과 이웃 92번의 상관이 **0.998**, |r| > 0.99 인 다섯 개(예측자 90–94 =
    Im Z at 22.5/17.8/14.1/11.1/8.8 Hz)의 |r| 은 0.9920~0.9941 로 **소수 셋째
    자리에서 갈린다**. `[해석]` ARD 가 고른 것은 **주파수가 아니라 공선 대역**
    이며, 그 안의 어느 점이 뽑히는지는 데이터가 정하지 않는다. **이것이 SEV
    설계에 직접 걸린다** — SEV 도 "특정 주파수/시간상수 대역의 값" 을 물리량으로
    읽는 feature 이므로, **"그 대역이 정보를 갖는가"(참일 수 있다)와 "그 안의
    특정 점이 특정 물리에 대응하는가"(별개의, 대개 미검증인 주장)** 를 분리해야
    한다. 우리가 값싸게 공급할 수 있는 것: 셀 제외 재적합으로 **ARD 선택
    인덱스의 분포**를 내는 것.
  - **불확실성 보고의 전례 하나 + 반면교사 하나.** 이 논문은 이 계보에서
    **처음으로 예측 불확실성을 그림에 그린다** (GPR 사후 분산, ±1 s.d. 음영,
    Fig. 1a·2·3a,b·4). 그러나 그것은 **가정한 i.i.d. 관측잡음 + 커널 함수
    불확실성**일 뿐 라벨 불확실성도 셀 간 변동도 아니며, **보정 검사가 없다** —
    `calibrat*` 0회이고 `[도표]` Fig. 3a/3b 에서 **측정 곡선이 ±1σ 음영 밖에
    연속 100 사이클 이상** 머문다 (계통 편의). `[해석]` 이 카드의 Gap "라벨
    불확실성이 없다" 에 짝을 이루는 교훈: **구간을 그리는 것과 그 구간이 맞는
    것은 다른 주장이고, 우리가 오차 막대를 공급할 때는 coverage 를 필수 산출로
    넣는다.**
  - **어휘 전수 (이 계보 여덟 편째)**: 합자 정규화 후 본문 6쪽 + SI 6쪽 전체에서
    `degenerac*` **0** · `identifiab*` **0** · `uncertaint*` **1**(식 (3) 뒤
    "a measure of uncertainty") · `calibrat*` **0** · `cross-valid*` **0**.
    다만 **`non-unique` 가 1회 있다** — `[인쇄]` "the fit is often non-unique",
    **등가회로 fitting**(경쟁 방법)에 대한 비판이며 그것을 **자기 방법의
    정당화 근거**로 쓴다 ("그러니 fitting 하지 말고 회귀하자").
    `[해석]` 이 계보에서 비유일성 어휘가 처음 나온 자리가 **자기 진단이 아니라
    타 방법 기각**이라는 것은, "개념이 없어서 안 쓴 것이 아니라 자기 쪽으로
    돌리지 않은 것" 이라는 **더 강한 형태의 확인**이다. 심사자가 Braatz 였다는
    사실(`[인쇄]` Peer review information)이 이 관찰의 무게를 더한다.

- [2026-09-03 (9)] open 유지 — 제목에 "degradation pattern **decoupling**" 이
  들어간 논문을 본문 + SI + **저자 공개 저장소 2종**으로 흡수
  (`raw/papers/tao2025_nondestructive-degradation-decoupling.md`, Tao et al.,
  *Energy Environ. Sci.* **18** (2025) 1544, DOI 10.1039/d4ee03839h).
  이 카드에 준 것 셋:
  - **판정 (경계 확정, Evidence 아님)**: 그 논문의 "decoupling" 은 **우리 축이
    아니다.** 미지수가 2개(열역학 ΔE / 동역학 η)이고, **LLI·LAM_PE·LAM_NE 가
    전부 ΔE 한 칸 안**에 들어간다 — 논문 자신의 Fig. 5b 가 LAM·LLI 두 상자를
    한 화살표로 묶으며 그 옆에 `[인쇄]` **"Hard to decouple"** 을 인쇄하고,
    Fig. 5e 범례가 `[인쇄]` "Thermodynamic loss (**LAM&LLI**)" 다. 좌표계는
    [[thermo-kinetic-loss-partition]] 에. **H1/H2 어느 쪽에도 무게를 싣지 않는다.**
  - **후보 관측 1건 추가 (위 "답하는 방법")**: 전류 축. 다단 충전(0.33C ↔ 3C)이
    ΔE/η 비중을 바꾸므로 채널이 하나 늘어난다. 단 그 논문은 그 채널로 열역학
    **안**을 가른 적이 없다.
  - **우리가 공급할 자리를 그 논문이 명시적으로 남긴다**: `[인쇄]` Discussion
    "Addressing open challenges of **electrochemical-level decoupling** of
    degradation patterns could further consolidate the statistical evidence."
    즉 이 카드의 질문은 그 논문이 스스로 비워 둔 자리다.
  - **어휘 전수 (이 계보 아홉 편째)**: 본문 16쪽 + SI 75쪽에서 `identifiab*`
    **0** · `degenerac*` **0** · `cross-valid*` **0** · `half-cell` **0** ·
    `error bar` **0**. 이 논문의 특이점은 **어휘 없이 개념을 인정하고 넘어간다**
    는 것 — `[인쇄]` "The challenge of distinctly identifying these mechanisms
    persists, even with advanced diagnostics" 라고 적은 **뒤에** 제목에
    "decoupling" 을 쓴다. 여덟 편의 "어휘가 없다" 와는 다른 형태다.

- [2026-09-03 (10)] open 유지 — (7) 에서 **다음 흡수 1순위로 예약해 둔** 문헌을
  흡수했다 ([[np-lip-ocv-reparametrization]], Lin & Khoo, *J. Power Sources*
  **605** (2024) 234446, raw:
  `raw/papers/lin2024_ocv-degradation-mode-identifiability.md`).
  이 카드에 준 것 넷:
  - **★ 이 카드의 전제 하나가 갈라졌다 — PVS 와 SEV 를 한 묶음으로 다룰 수 없다.**
    2 자유도 정리의 따름정리에 따라 **PVS 는 새 관측 채널이 아니라 같은 곡선의
    재가중**이다 (Evidence For 새 항목). 반면 **SEV 는 동역학 축이라 이 정리의
    사정권 밖**이고, 원전은 동역학을 명시적으로 범위 밖에 둔다. 즉 "관측을 늘리면
    갈리는가" 라는 이 카드의 질문에 대해 **두 후보의 지위가 다르다.**
  - **Evidence Against 1건 추가**: 구조적으로 잃는 방향은 **LLI↔LAM_PE 가 아니라
    세 모드 공통 스케일 방향**이다. 곡선은 원리적으로 LLI 와 LAM_PE 를 구별한다 →
    H1 이 참이라면 그 이유는 구조가 아니라 **조건수**다. 무대가 옮겨졌다.
  - **판정 절차 정정 1건** ("답하는 방법" 3번): PVS 의 Jacobian 행은 구조적으로
    2차원 평면 안에 갇히므로 특이값 검사가 자명하게 통과한다 — `(r_N/P, z₀⁺)`
    좌표에서 **방향각**을 비교해야 한다.
  - **어휘 전수 (이 계보 열 편째)**: `identifiab*` **26** — **연속 0회가 처음으로
    깨졌다.** 그러나 `degenerac*` **0** · `non-unique` **0** · `collinear*` **0** ·
    `nullspace` **0** · `Hessian` **0** · `singular value` **0** · `noise` **0** ·
    `error bar` **0** · `cross-valid*` **0** · **파라미터 상관 언급 0**.
    `[해석]` 열 편째의 새 형태는 **"개념을 절반만 자기 쪽으로 돌린다"** 이다 —
    추정 정밀도(CRLB)는 재고, 비유일성은 §2.3 에 닫힌 형태로 인쇄해 놓고
    "redundancy" 라 부르고 지나간다. 그리고 오차공분산의 **비대각을 계산해 놓고
    `sqrt(diag)` 만 그린다** — 축퇴의 방향을 손에 쥔 채 표시하지 않는다.
    **우리가 값싸게 공급할 수 있는 것이 바로 그 그림이다.**
  - **새 Gap 1건**: 세미나가 PVS 를 **SOC 정규화 곡선**에서 계산했는지 **Ah 축**
    에서 계산했는지가 원문에 인쇄돼 있지 않다. 이 구분이 위 따름정리의 적용
    여부를 가른다 (Ah 축이면 총용량 정보가 섞여 셋째 숫자를 실을 수 있다).
