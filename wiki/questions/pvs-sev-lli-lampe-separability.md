---
title: PVS·SEV 는 LLI 와 LAM_PE 를 가르는가
description: "Do the two physics-inspired features add an independent direction separating LLI from LAM_PE, or do they share one contrast"
created: 2026-09-03
updated: 2026-09-03
type: research-question
tags: [battery, degradation, research]
sources: [raw/papers/2026-09-02-siwon-kim-degradation-mode-ml-seminar.md, raw/transcripts/2026-09-03-voice-memo-007-degradation-mode-ml.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: empirical
evidenceScope: single-source
status: open
feedsInto: "degradation-degeneracy 목적함수 후보 (PVS·SEV 항) + 2026-09-02 세미나 discussion point 1"
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

우리 파이프라인 안에서 값싸게 판정 가능하다 — **본 실행이 필요 없다**:

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
- **LOGO-CV 의 group 정의가 원문에 인쇄되지 않았다.** 셀 단위인지 프로토콜
  단위인지에 따라 p.13 수치의 의미가 갈린다. 프로토콜 식별자가 입력에 있으므로
  group 이 셀이면 같은 프로토콜의 형제 셀로부터 예측하는 구조가 된다.
- **모드 동시 진행 시의 가법성**이 미확인 (원문 p.8 은 단독 스윕만).
- **SEV 의 정량 모드 스윕**이 없다 (p.11 은 모식도).
- LAM_NE 를 Si loss / Gr loss 로 쪼개면(원문 p.15 point 2) **미지수가 4개로
  늘어난다.** p.8 에서 Si loss 와 Gr loss 는 PVS 를 같은 방향(↓)으로 움직이고
  크기만 다르다 — 새 독립 관측 없이 쪼개면 식별성은 반드시 나빠진다. 이
  귀결은 아직 정량화되지 않았다.

## Status Log

- [2026-09-03] open — 2026-09-02 세미나 자료(15쪽)와 구술 메모를 raw 로 흡수하며
  개설. 부호표 대조에서 두 feature 의 패턴이 동일함을 발견한 것이 발단.
  아직 계산은 하나도 하지 않았다 — 위 "답하는 방법" 4단계 전부 미실행이며,
  현재 근거는 **원문 도표 판독 + 정성 논증**뿐이다.
