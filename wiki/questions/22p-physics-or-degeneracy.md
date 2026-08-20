---
title: 22p 결과는 물리인가 fitting degeneracy 인가
description: "Is the seminar 22p LLI/LAM decomposition (LAM_PE=LAM_NE=13%, LLI=17%) real physics or an artifact of non-identifiability"
created: 2026-08-11
updated: 2026-08-20
type: research-question
tags: [battery, degradation, research]
sources: [raw/repositories/degradation-degeneracy-audit.md]
confidence: medium
explored: false
verificationStatus: unverified
model: claude-fable-5
effort: high
claimType: empirical
evidenceScope: multi-source-primary
status: active
feedsInto: "세미나 재발표 결론 + degradation-degeneracy/docs/RESULTS.md 결론 1~3"
---

# 22p 결과는 물리인가 fitting degeneracy 인가

## 질문
2026-08-05 세미나 22p 의 열화 분해(LAM_PE ≈ LAM_NE ≈ 13%, LLI ≈ 17%)는 실제
물리인가, full-cell 곡선 하나로는 두 전극을 가를 수 없어 생긴
[[fitting-degeneracy]] 인가?

## 왜 중요한가
이 분해값이 세미나·후속 연구의 근거로 인용된다. degeneracy 라면 "PE 와 NE 가
같은 비율로 열화했다"는 서사 자체가 수학적 우연이고, 측정·목적함수를 바꿔야 한다.

## 가설
LAM_PE ≈ LAM_NE 는 물리가 아니라 **flat valley 방향에서 두 전극이 같은 부호로
묶이는 degeneracy** 의 산물이다 (귀무: 실제로 대칭 열화).

## Evidence For (가설 지지)
- (방향성 관측, 인용 금지 등급) 이전 coarse/이전-세대 실행에서 grid 기준 fitting
  의 상당 비율이 degenerate 로 판정되고, flat 방향에서 PE·NE 동부호 결합이
  관찰됨 — 정확한 비율은 clean 본 실행 후 확정.
- **[2026-08-20, 본 실행 후]** 22p 동작점 근방의 참 격차 0 칸에서 **거짓 분리가
  실제로 관측**된다. 즉 두 전극이 같다고 복원되는 것이 자동으로 물리는 아니고,
  반대로 다르다고 복원되는 것도 참 격차의 증거가 아니다. 비율은
  `docs/09_22P_GAP.md` 와 artifact 가 정본.
- **[2026-08-20]** half-cell 기준의 좌표 원점(Case 1 `p_ini`)이 **격자마다 다른
  국소해로 수렴**할 수 있고, 그 원점 차이가 붕괴율 차이와 같이 움직인다.
  분해 결과가 데이터가 아니라 최적화 경로에 의존하는 통로가 실재한다는 뜻 —
  진단 도구 `tools/diagnose_pini_transition.py`, 절차적 함의는 아래 Status Log.

## Evidence Against
- (방향성 관측, 인용 금지 등급) half-cell 기준(Case 1)과 dQ/dV 항 추가가 복원
  오차를 줄이는 방향 — 조건에 따라 분리가 가능할 수 있음.
- **[2026-08-20, 본 실행 후] 이 방향은 뒤집혔다** — 단 **protocol 조건부**다.
  paired fixed-budget 정본(`warm_start=False`)에서 dQ/dV 를 더한 목적함수가 더
  나빴고, "dQ/dV 가 분리 능력을 더한다"는 잠정 근거는 철회한다.
- **[2026-08-20, 21차 리뷰 후 재정정]** 위 문장은 처음에 "모든 noise 층에서
  더 나빴다" 였는데, 그 범위는 **`warm_start=False` protocol 에 한정**된다.
  같은 조건집합·같은 예산에서 warm 만 켜면 열세가 크게 줄고 한 층에서는
  방향이 **뒤집힌다**. 또 metric 에 따라서도 방향이 갈린다. 인용 가능한
  형태는 "사전 지정한 aggregate raw-degeneracy endpoint 에서는 개선이 관측되지
  않았다" 까지다 — 수치·층별 표는 원장 §20.4 와 §29.2 (정본은 옮겨 적지 않는다).
- 남아 있는 반대 근거는 좁다: 붕괴가 **전 조건에서 일어나지는 않는다**. 다만 그
  낮은 사건률의 상당 부분이 임계 설정(판정선 간격 대 실측 격차오차)의 결과라
  원장이 명시하므로, 이것을 "물리다"의 근거로 쓸 수 없다.

## Status Log
- **[2026-08-05]** 세미나 22p 발표 — 질문 성립.
- **[2026-08-11]** 판별 파이프라인이 13차 게이트 리뷰 대기
  ([[degradation-degeneracy]], [[gate-review-loop]]). 본 실행(grid v4, 10h) 전 —
  위 Evidence 는 전부 잠정. GO 후 artifact 수치로 이 카드를 갱신한다.
- **[2026-08-20]** 19차까지 진행, 본 실행 완료. **status 는 아직 `active`** —
  질문이 닫히지 않았다. 실행이 준 것은 답이 아니라 **답의 조건**이다:
  - 파이프라인이 낸 결론 1은 **철회**, 2는 모집단 **한정**, 3은 축소됐다. 즉
    "22p 는 degeneracy 다"도 "물리다"도 지금 근거로는 단정할 수 없다.
  - 새로 드러난 축 둘: (a) **모델 오차 민감도** — half-cell OCP 의 PE 쪽 전압
    왜곡이 수 mV 수준에서 분해를 무너뜨린다(NE·stoichiometry 축은 훨씬 둔감),
    (b) **최적화 예산** — restart 예산이 부족하면 좌표 원점이 오염되고, 예산을
    늘리면 회복된다. 한때 "왜곡의 상전이"로 읽었던 현상이 실제로는 (b)였다.
  - 따라서 이 카드의 질문은 **"분해가 물리인가"에서 "어떤 측정·모델 정확도와
    어떤 최적화 예산에서 분해가 의미를 갖는가"로 좁혀졌다.** 남은 실험 7개는
    `docs/09_22P_GAP.md` §10.
  - 수치는 이 카드에 옮기지 않는다 — 정본은 artifact + `docs/RESULTS*.md`
    ([[provenance-fail-closed-verification]] 원칙).
