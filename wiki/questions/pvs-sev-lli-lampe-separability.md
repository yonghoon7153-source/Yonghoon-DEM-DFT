---
title: PVS·SEV 는 LLI 와 LAM_PE 를 가르는가
description: "Do the two physics-inspired features add an independent direction separating LLI from LAM_PE, or do they share one contrast"
created: 2026-09-03
updated: 2026-09-03
type: research-question
tags: [battery, degradation, research]
sources: [raw/papers/2026-09-02-siwon-kim-degradation-mode-ml-seminar.md, raw/transcripts/2026-09-03-voice-memo-007-degradation-mode-ml.md, raw/papers/birkl2017_degradation-diagnostics-ocv.md, raw/papers/wang2025_interpretable-ml-battery-prognosis.md, raw/papers/kim2023_graphite-heterogeneity-lifetime.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: empirical
evidenceScope: single-source
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
- **[2026-09-03] SEV 축에 대한 문헌 전례: LLI 와 LAM 이 R_ct 를 같은 방향으로
  민다.** 분야 리뷰([[interpretable-ml-battery-prognosis-taxonomy]] 가 정리한
  Wang et al. 2025) §4.4 가 인용하는 Su et al. 2024 의 DRT 관찰을 리뷰가
  이렇게 인쇄한다 — "the variation trends of typical DRT peaks and valleys
  during battery aging aligned with the increase in charge transfer resistance
  **caused by LLI and LAM**". 두 모드가 **같은 하나의 물리량(R_ct)을 같은
  방향으로** 올린다는 진술이며, SEV(= R_ct,PE 의 stoichiometry 의존성)로
  두 모드를 가르려는 설계에 직접 불리하다. 원전 미확인 — 리뷰의 요약을
  거친 진술이므로 인용 전에 Su 2024 를 직접 봐야 한다.

## Evidence Against (H2 지지 / H1 반대)

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

## 이 질문에 답하는 방법 (설계, 미실행)

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
- **LOGO-CV 의 group 정의가 원문에 인쇄되지 않았다.** 셀 단위인지 프로토콜
  단위인지에 따라 p.13 수치의 의미가 갈린다. 프로토콜 식별자가 입력에 있으므로
  group 이 셀이면 같은 프로토콜의 형제 셀로부터 예측하는 구조가 된다.
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
