---
title: 22p 결과는 물리인가 fitting degeneracy 인가
description: "Is the seminar 22p LLI/LAM decomposition (LAM_PE=LAM_NE=13%, LLI=17%) real physics or an artifact of non-identifiability"
created: 2026-08-11
updated: 2026-09-04
type: research-question
tags: [battery, degradation, research]
sources: [raw/repositories/degradation-degeneracy-audit.md, raw/papers/birkl2017_degradation-diagnostics-ocv.md, raw/papers/rhyu2025_systematic-feature-design-formation.md, raw/papers/lin2024_ocv-degradation-mode-identifiability.md, raw/papers/schaeffer2024_nullspace-regularization-interpretation.md, raw/papers/cui2024_electrode-utilization-formation-cycle-life.md, raw/papers/navidi2024_piml-degradation-diagnostics-comparison.md, raw/papers/marongiu2016_lfp-onboard-capacity-halfcell.md]
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
- **[2026-09-03, 원전 흡수]** 이 절차의 원전
  ([[birkl-ocv-degradation-diagnostic]], Birkl et al. 2017) 이 **자기 방법의
  축퇴를 명시적으로 진술한다** — "a combination of e.g. LLI and LAM_NE,de
  creates the same OCV signature as an equal amount of LAM_NE,li. … The
  fractions of lithiated and delithiated LAM can therefore **not be uniquely
  identified**" (§4.2, p.382). 저자들의 대응은 축퇴를 푸는 것이 아니라
  `[total-LLI, LAM_PE, LAM_NE]` 라는 **동치류 좌표로 옮기는 것**이다. 즉
  이 계열 방법의 출력은 처음부터 **몫공간의 값**이며, 원전이 그렇게 설계했다고
  적는다.
- **[2026-09-03] 원전에 식별 가능성 진단이 하나도 없다.** 파라미터 상관·Hessian·
  신뢰구간·노이즈 스윕이 전무하고, 국소최소 대응은 `fmincon` + MultiStart 100회
  뿐이며 그 100개 해의 분포도 보고되지 않는다. Fig. 8 의 오차 막대는 **코인셀
  제작 재현성(5.4%)** 이지 추정 불확실성이 아니다 — 논문이 §4.3 에서 명시한다.
  즉 이 카드의 질문은 원전이 **비워 둔 자리**이지, 이미 답이 있는데 우리가
  모르는 것이 아니다.

- **[2026-09-03 (5)] ★★ 이 가설의 방향이 닫힌 형태로 예측돼 있었다 — 그리고 22p
  의 세 숫자가 그 방향 바로 옆에 있다.** [[np-lip-ocv-reparametrization]]
  (Lin & Khoo 2024, *J. Power Sources* **605**, 234446) 은 SOC 정규화 full-cell
  OCV 의 **형상이 두 자유도뿐**임을 증명하고 (`[인쇄]` "the shape of an OCV curve
  … is **only governed by two degrees of freedom**"), 그 둘이 세 모드의
  **1 마이너스 값의 비**로만 결정된다고 적는다 (식 16). 따라오는 결과 둘:
  1. **정확한 null 방향**: pristine 에서 `LLI = LAM_PE = LAM_NE = x` 인 모든 `x`
     에 대해 곡선 형상이 **글자 그대로 pristine 과 같다** (총용량만 `1−x` 배).
     이 카드의 가설이 말하는 "PE·NE 가 같은 부호로 묶이는 flat 방향" 의
     **3차원 일반형**이며, 격자에 truth 쌍으로 직접 심어 시험할 수 있다.
  2. **22p 삼중항의 형상 정보는 스칼라 하나다.** 세미나 22p 값
     (LAM_PE ≈ LAM_NE ≈ 13 %, LLI ≈ 17 %) 을 식 (16) 에 넣으면
     `r_N/P / r_ini = (1−0.13)/(1−0.13) = **1.000**` (N/P 가 pristine 에서 한 발짝도
     안 움직였다), `z₀⁺ / z₀,ini = (1−0.17)/(1−0.13) = **0.954**`.
     `[해석]` **세 개의 독립된 물리량처럼 읽히는 값이 곡선 형상 자유도로는 한 개다.**
     세 숫자 중 둘(LAM_PE, LAM_NE)은 서로를 정확히 상쇄해 형상에 흔적을 남기지
     않았고, 남은 정보는 "Li/P 가 4.6 % 줄었다" 뿐이다. 이것은 **degeneracy 의
     증명이 아니라** — 형상 2 + 측정 총용량 1 = 3 이므로 원리적 복원은 가능하다 —
     "이 삼중항이 놓인 자리가 null 방향에 얼마나 가까운가" 를 처음으로 **좌표로**
     보여 준 것이다.
  (세미나 값의 정본은 이 카드이고, 우리 파이프라인 수치의 정본은 artifact +
  `degradation-degeneracy/docs/RESULTS*.md` 다. 여기서는 환산만 했다.)
- **[2026-09-03 (5)] 이 논문이 우리 방법의 구조적 약점을 이름 붙여 지목한다.**
  `[인쇄, p.13]` "A straightforward approach is to devise an estimator and
  calibrate the estimation error by feeding measurements coming from a known
  ground truth **[3,19]**. The drawback of this approach is that it **entangles
  the identifiability intrinsic to the problem with the error incurred by the
  estimator itself**." — `[3]` 이 [[birkl-ocv-degradation-diagnostic]] 이고, 우리
  파이프라인이 정확히 그 계열이다. `[해석]` 우리는 이 얽힘을 이미 알고 설계했다
  ([[fitting-degeneracy]] 의 flat valley ↔ multimodal 구분, 무작위 restart 끼리만
  비교하는 multi-start 진단). **그들은 회피했고 우리는 분해하려 한다** — 이 카드의
  질문이 왜 남의 CRLB 계산으로 닫히지 않는지의 근거이기도 하다.

- **[2026-09-03 (6)] ★ 축퇴 방향 위의 값은 데이터가 아니라 *추정기가* 정한다 —
  일반 명제가 인쇄됐다.** [[nullspace-coefficient-interpretation]] (Schaeffer
  et al. 2024, *Comput. Chem. Eng.* **180**, 108471) 은 선형 모형에서
  `X(β + w) = Xβ, w ∈ 𝒩(X)` 이므로 **데이터가 계수를 부분공간 하나만큼
  결정하지 못하고 그 안의 점은 오직 정칙화가 고른다**는 것을 증명·시연한다
  (`[인쇄]` "The vectors in the nullspace **affect only the regularization
  term** in the objective function"). 그리고 그 선택이 답을 바꾼다는 것을
  같은 데이터에서 보인다 — `[도표]` Fig. 1b: 모양이 9배 다른 두 계수 벡터
  (포물선 vs 상수)의 NRMSE 가 **0.105 % 대 0.105 %**.
  `[해석]` **이 카드에 주는 것**: 우리 fitting 에는 명시적 정칙화가 없지만
  **암묵적 정칙화**(초기값·경계·optimizer 경로·좌표 정규화)가 그 자리를
  대신한다. 즉 축퇴 방향 위에서 22p 삼중항이 놓인 자리는 **데이터가 고른
  값이 아닐 수 있고, 목적함수 값은 그것을 구별하지 못한다.** 이것은
  2026-08-20 실측 "half-cell 기준의 좌표 원점이 격자마다 다른 국소해로 수렴
  하고 그 원점 차이가 붕괴율 차이와 같이 움직인다" 와 **같은 현상의 일반형**
  이며, 그 관찰에 문헌 근거를 붙인다.
  **범위 한정 3개** (과대 인용 방지): (a) 원전은 **선형**이고 우리는 비선형
  이다 — 다리는 Jacobian 이며 그 nullspace 는 **국소**다. (b) 원전은
  `LLI`·`LAM`·`half-cell` 을 **각 0회** 쓰고 열화 모드를 재지 않는다. 따라서
  이것은 22p 수치에 대한 증거가 아니라 **메커니즘에 대한 증거**다.
  (c) 원전에서 `𝒩(X)` 는 `p ≫ n` 이라 **정확히** 비어 있는 방향이지만,
  우리는 미지수 3개에 관측이 곡선 전체라 **근사 null**(작은 특이값)이다 —
  "구별 불가능" 이 아니라 "조건수가 나쁘다" 가 정확한 진술이다.

- **[2026-09-03 (6)] "목적함수 값이 낮은 해가 참에 가깝다" 가 반증됐다
  (그림판).** 같은 원전 `[도표]` Fig. 4a·4b·5a·5b 범례의 NRMSE 순서:
  Fig. 4b 에서 PLS **0.108 %** < nullspace 보정 **0.118 %** < **참계수
  0.127 %**. 참계수가 **가장 나쁘다** (적합 모형이 잡음을 먹었기 때문).
  `[해석]` 이 카드가 다루는 22p 분해도 목적함수 최소점에서 읽은 값이다.
  **낮은 잔차는 참에 가깝다는 증거가 아니다** — 우리 파이프라인이 `|err|`
  (복원 오차)로 판정하도록 설계된 이유이기도 하다.

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
- **[2026-09-03, 원전 흡수] 원전의 실험 검증이 이 카드가 받은 가장 강한 반대
  근거다.** Birkl 2017 은 열화를 **공학적으로 제작한 코인셀 6종**(디스크 지름
  → LAM, 조립 SoC → LLI)에서 지배 모드를 대체로 맞혔다 (raw digest §8.2 표).
  정답이 fitting 이 아니라 **독립적인 제작 설계값**이라는 점에서, 이 카드가
  지금까지 받은 근거 중 유일하게 "적어도 큰 신호에서는 분해가 실물을 되짚는다"
  는 방향이다. **다만 무게는 제한적이다**: (a) 정답 6점뿐, (b) 오차 막대가
  추정 분산이 아니고, (c) 잃은 활물질이 "가위로 잘라낸 균일한 조각"이라 원전의
  핵심 가정(열화가 개별 상에 다르게 작용하지 않는다)을 구조적으로 시험하지
  못하며, (d) 6셀 중 4셀에서 **없어야 할 LAM_PE 가 일관되게 6–10%p 새어
  나온다** — 저자는 셀별 제작 아티팩트로 설명하지만 "LAM_PE 방향이 잘 안
  갈린다"는 축퇴 해석도 같은 데이터를 설명하고, 원전은 그 대안을 검토하지
  않는다.
- **[2026-09-03] 합성 검증은 반대 근거로 세지 않는다.** 원전 Fig. 7 의 3점
  완전 복원(RMSE 0.0 mV)은 **생성 모델 = 적합 모델, 노이즈 0** 의 inverse crime
  이다. 저자의 "proves … uniquely identify" 문장은 그 설계가 지지하는 범위를
  넘는다.

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
    왜곡이 수 mV 수준에서 분해를 무너뜨린다. (★ 여기 있던 "NE·stoichiometry
    축은 훨씬 둔감" 은 20차에 철회했다 — 축 순위는 폐기 다리를 분자에 쓴
    비교였다: 철회[AXIS_RANK].) (b) **최적화 예산** — 예산이 부족하면 좌표
    원점이 오염될 수 있다. 한때 "왜곡의 상전이" 로 읽었던 현상이 실제로는
    (b)였다. (★ "예산을 늘리면 회복된다" 도 격하했다 — 근거는 세 축이 엉킨
    n=1 pilot 하나다: 철회[R20_RX].)
  - 따라서 이 카드의 질문은 **"분해가 물리인가"에서 "어떤 측정·모델 정확도와
    어떤 최적화 예산에서 분해가 의미를 갖는가"로 좁혀졌다.** 남은 실험 7개는
    `docs/09_22P_GAP.md` §10.
  - 수치는 이 카드에 옮기지 않는다 — 정본은 artifact + `docs/RESULTS*.md`
    ([[provenance-fail-closed-verification]] 원칙).
- **[2026-09-03]** 인접 질문이 하나 갈라져 나왔다:
  [[pvs-sev-lli-lampe-separability]]. 이 카드가 "full-cell OCV **하나**로
  가를 수 있는가" 를 묻는 데 비해, 그쪽은 "**관측을 늘리면** 갈리는가" 를
  묻는다 — 2026-09-02 세미나가 제안한 [[pvs-sev-degradation-mode-features]]
  두 개가 그 늘린 관측의 구체적 후보다. 두 카드는 같은 축의 앞뒤이고, 그쪽
  답이 이 카드의 "어떤 측정에서 의미를 갖는가" 에 직접 들어온다.
  이 카드의 상태는 바뀌지 않는다 (`active` 유지) — 새 근거는 아직 없고,
  갈라진 질문만 등록했다.
- **[2026-09-03 (2)]** 이 절차의 **원전**을 흡수했다 —
  [[birkl-ocv-degradation-diagnostic]] (raw:
  `raw/papers/birkl2017_degradation-diagnostics-ocv.md`). status 는 `active`
  유지. 이 카드에 실제로 달라진 것 셋:
  1. **"저자들이 식별 가능성에 침묵하는가"에 답이 나왔다 — 침묵하지 않는다.**
     한 종류의 축퇴(pure-LLI + LAM_de ↔ LAM_li)를 정확히 지목하고, 3-파라미터
     출력이 그 **동치류 좌표**임을 설계 이유로 적는다. 다만 3-파라미터 공간
     **안에서의** 식별 가능성(우리가 재는 것)에 대한 진단은 전혀 없다.
     → 후속 인용자가 이 문단을 인용하지 않는 것이 문제이지 원전이 숨긴 것이
     아니다. 우리 기여의 자리는 "원전이 말한 축퇴"가 아니라 "원전이 안 잰
     축퇴"다.
  2. **★ 우리가 재는 절차가 원전과 같지 않다.** Birkl 원안은 자유 파라미터가
     **3개**이고 `Δx_EoC`/`Δx_EoD` 를 **컷오프 전압 등식(Eq. 11–12)으로
     소거**한다. 우리 저장소 문서가 서술하는 창 모델(α_PE, β_PE, α_NE, β_NE)은
     그 제약이 없다. **우리가 관측한 degeneracy 의 일부가 원전에 없는
     자유도에서 올 수 있다** — 검증 가능한 가설이며, 답이 이 카드의 "어떤
     조건에서 분해가 의미를 갖는가" 에 직접 들어온다. 반대로 원안은 절대
     전압을 등식으로 쓰므로 우리가 이미 관측한 **OCP 수 mV 왜곡 민감도**가 더
     나쁘게 나타날 개연성이 있다. 둘 다 미실측.
  3. **인용 확인 항목 하나 열림**: `degradation-degeneracy/docs/02_CODE_AUDIT.md`
     와 `docs/04_PROMPTS.md` 의 `LLI = (1−α_PE) + (β_PE − β_NE)` 에 붙은
     "Birkl 2017 부호 규약" 주석은 **이 논문 본문으로 확인되지 않는다**
     (본문에 α·β 창 파라미터가 없다). 다른 문헌([19] Dubarry 2012, [26]
     Marongiu 2016)이거나 유도 결과일 수 있다. 이번 세션은 그 문서를 **읽기만
     하고 고치지 않았다**.

- **[2026-09-03 (3)]** 그 원전의 **앞 세대**를 흡수했다 —
  [[dubarry-mechanistic-mode-synthesis]] (Dubarry/Truchot/Liaw 2012, raw:
  `raw/papers/dubarry2012_synthesize-degradation-modes.md`). status `active` 유지.
  이 카드에 달라진 것 셋:
  1. **식별 가능성 어휘 전수 확인 (합자 정규화 후, 13쪽 61,578자)**:
     `identifiab` **0** · `degenerat` **0** · `non-unique` **0** · `ill-posed` **0** ·
     `collinear` **0** · `confidence` **0** · `inverse` **0**. `uniqu` 7회는
     **전부 "unique/novel technique"** 의 자화자찬 어휘이고 수학적 유일성 주장이
     아니다. **정량 진단(상관·Hessian·신뢰구간·노이즈 스윕)은 0개.**
     → Birkl 때와 같은 결론: **원전 계열은 식별 가능성을 정량으로 재지 않는다.**
     다만 Birkl 과 마찬가지로 **부정하지도 않는다** — `ambigu` 3회가 전부 축퇴
     논의이고, 저자들은 **LAM_liPE ↔ LLI 를 이름 붙여 구별 불가로 인정**한다
     ("it is difficult to distinguish between LAM_liPE and LLI unambiguously",
     원인은 LFP 의 평탄 plateau). 유일 식별 가능한 것은 LAM_deNE 뿐이라고 적는다.
  2. **★ 우리가 재는 축퇴가 2012년 식 안에 해석적으로 예측돼 있다.** Dubarry
     식 (5)+(8') 은 세 모드(`LAM_liNE`,`LAM_dePE`,`LLI`)를 **단 하나의 스칼라
     offset 에 덧셈으로** 넣는다. 여기서 곧바로
     `{LAM_liNE = x} ≡ {LAM_deNE = x, LLI = LR·x}` 가 나온다 (두 시나리오가
     `LR`·`OFS` 를 모두 같게 만든다). 지금까지 우리가 본 축퇴는 **수치적으로
     발견된 것**인데, 이것은 **닫힌 형태로 예측된 축퇴 방향**이다 — 격자에 그
     방향의 truth 쌍을 심어 **직접** 시험할 수 있다. 검증력이 다르다. 미실행.
  3. **자유도 계보가 이 카드의 가설 하나를 더 선명하게 만든다**: Dubarry **2**
     (`LR`,`OFS`) → Birkl **3** (`[LLI,LAM_PE,LAM_NE]`) → 우리 창 모델 **4**
     (α_PE,β_PE,α_NE,β_NE). "우리가 관측하는 degeneracy 의 일부가 원전에 없는
     자유도에서 온다"는 가설의 좌표가 이제 셋 다 인쇄됐다. 여전히 미실측.
  - 부수 확인 (이 카드 밖): 2026-09-03 (2) 에서 열어둔 **인용 확인 항목이
    종결됐다** — 상세는 [[dubarry-mechanistic-mode-synthesis]] 및
    [[birkl-ocv-degradation-diagnostic]] "인용 확인 — 종결". 요지는
    **좌표계 계보는 Dubarry 2012 이고, legacy LLI 식은 두 원전 어디에도 없다.**
    이번 세션도 그 문서들을 **읽기만 하고 고치지 않았다.**

- **[2026-09-03 (4)]** 인접 계보의 다섯 번째 원전을 흡수했다 —
  [[fused-lasso-feature-design-framework]] (Rhyu et al., *Joule* 9 (2025)
  101884, raw: `raw/papers/rhyu2025_systematic-feature-design-formation.md`).
  status `active` 유지 — **우리 22p 수치에 직접 닿는 근거는 없다.** 그러나
  이 카드의 축에 걸리는 것 셋이 나왔다:
  1. **★ 야생에서 발견된 또 하나의 무-불확실성 모드 적합.** 이 논문 SI
     Note S11 은 형성 후 C/20 RPT 곡선에 **4-파라미터 전극 이용상태**를
     맞춘다: `[인쇄]` "the system is parameterized by four parameters:
     fraction of cathode capacity 'active' to filling/emptying **β_c**,
     fraction of anode capacity active to filling/emptying **β_a**,
     **remaining lithium inventory capacity Q_rem**, and **voltage shift due
     to external resistances V_shift**." 좌표가 우리 축과 대응한다
     (`1−β_c ↔ LAM_PE`, `1−β_a ↔ LAM_NE`, `1−Q_rem/Q_c,total ↔ LLI`).
     결과는 Table S9 의 **점추정 넷**(0.911 / 0.854 / 0.930 / 0.014 V) 이고
     오차 막대·상관·감도가 **없다**. 그런데 거기서 물리 결론을 뽑는다:
     `[인쇄]` "the learned utilization state indicates that **the effective
     capacity lost at each electrode is greater than the lithium inventory
     lost**". 저자 스스로 적합 실패를 인정하면서도 (`[인쇄]` "still **fails to
     fit** the differential capacitance versus voltage curve perfectly")
     결론의 방향은 유지한다.
     `[해석]` **이 카드가 22p 에 대해 묻는 것과 정확히 같은 형태의 주장이
     다른 논문에서 반복되고 있다.** 우리 합성 truth 격자가 그 주장에 경계를
     붙일 수 있는 자리다 — 다만 그쪽은 노화가 아니라 **형성 직후** 상태이고
     셀 화학(SC-NMC532‖AG)·관측(C/20 RPT, 32셀 평균곡선 1개)이 다르다.
  2. **식별 가능성 어휘 전수 (여섯 편째)**: `degenerac*` **0** ·
     `uncertain*` **0** · `identifiab*` **1** (참고문헌 [30] 제목 안) ·
     `nullspace` **1** (참고문헌 [13] 제목 안). 본문 서술은 여전히 0회.
     특기할 점은 [13] 이 **저자 그룹 자신의 nullspace 논문**(공저자 4명 겹침)
     인데 본문에서 "β 는 해석을 준다" 는 **긍정 근거로만** 인용된다는 것이다.
  3. **★ 다음 흡수 최우선 후보가 확정됐다**: 그 참고문헌 [30] —
     **Lin, J. & Khoo, E. (2024), "Identifiability study of lithium-ion battery
     capacity fade using degradation mode sensitivity for a minimally and
     intuitively parametrized electrode-specific cell open-circuit voltage
     model", *J. Power Sources* 605, 234446.** 이 계보에서 제목에
     identifiability 가 있는 **유일한** 문헌이며, 이름만으로도 이 카드의
     선행 연구다. 다음 세션의 1순위.
  - 우리 쪽 수치는 이 카드에 옮기지 않는다 — 정본은 artifact +
    `docs/RESULTS*.md`.

- [2026-09-03 (9)] active 유지 — 제목에 "degradation pattern **decoupling**" 이
  들어간 논문을 흡수했지만 **이 카드에 직접 닿는 근거는 없다**
  (`raw/papers/tao2025_nondestructive-degradation-decoupling.md`, Tao et al.,
  *Energy Environ. Sci.* 18 (2025) 1544). 이유를 명시적으로 적는다 — 제목만으로
  이 카드의 선행 연구로 오인하기 쉽기 때문이다:
  1. **좌표계가 다르다.** 그 논문의 미지수는 2개(열역학 ΔE / 동역학 η)이고
     LLI·LAM_PE·LAM_NE 는 **전부 ΔE 한 칸 안**이다
     ([[thermo-kinetic-loss-partition]]). 22p 와 같은 형태의 분해값
     (LAM_PE / LAM_NE / LLI 각각의 %)을 **산출하지 않는다.**
  2. **LLI·LAM 을 정량한 적이 없다.** 두 약어가 본문 12 / 7 회 나오지만 전부
     정성 서술이고, half-cell OCP fitting·해체분석 정량이 없다. 유일하게 모드를
     구분하려 한 자리는 Fig. 5g 의 ICA 화살표 주석(peak 강도 ↓ = LAM,
     peak 이동 = LLI)이며 **수치가 없고** 그 귀속은 참고문헌에 기댄다.
  3. **그럼에도 한 줄이 이 카드 편에 선다**: `[인쇄]` "**The challenge of
     distinctly identifying these mechanisms persists, even with advanced
     diagnostics** …, which struggle to non-destructively elucidate internal
     aging states and their interdependencies." 즉 이 계보의 논문이 **모드
     식별의 어려움을 자기 방법의 설계 이유로 인쇄**한 사례가 하나 더 늘었다
     (Birkl 2017 §4.2 와 같은 형태). 다만 그 어려움을 **정량하지 않고**
     제목에는 "decoupling" 을 쓴다.
  - 식별 가능성 어휘 전수 (아홉 편째): `identifiab*` **0** · `degenerac*` **0** ·
    `cross-valid*` **0** · `half-cell` **0** (본문 16쪽 + SI 75쪽).

- **[2026-09-03 (10)]** `active` 유지 — **예약해 둔 1순위 문헌을 흡수했다**
  ([[np-lip-ocv-reparametrization]], Lin & Khoo, *J. Power Sources* **605** (2024)
  234446, raw: `raw/papers/lin2024_ocv-degradation-mode-identifiability.md`).
  2026-09-03 (4) 에서 "이 계보에서 제목에 identifiability 가 있는 **유일한**
  문헌" 으로 지목했던 그것이다. 이 카드에 달라진 것 다섯:
  1. **Evidence For 2건 추가** (위): 닫힌 형태 null 방향 + 22p 삼중항의 좌표 환산,
     그리고 우리 검증 방식의 구조적 약점을 원전이 이름 붙여 지목한다는 것.
  2. **★ 어휘 전수에서 연속 0회가 깨졌다 — 그러나 반쪽만.** 합자 정규화 후 본문
     77,217자에서 `identifiab*` **26** (열 편 중 처음으로 0이 아니다) ·
     `sensitivit*` 46 · `Fisher` 12 · `error covariance` 4. 그런데
     `degenerac*` **0** · `non-unique` **0** · `collinear*` **0** · `ill-posed`
     **0** · `nullspace` **0** · `Hessian` **0** · `singular value` **0** ·
     `condition number` **0** · `profile likelihood` **0** · `noise` **0**(!) ·
     `error bar` **0** · `cross-valid*` **0** · **파라미터 상관 언급 0**.
     `[해석]` **"파라미터를 얼마나 정확히 재는가"(추정 정밀도) 어휘는 갖췄지만
     "서로 다른 조합이 같은 관측을 내는가"(비유일성) 어휘는 여전히 없다.**
     §2.3 에서 그 비유일성을 닫힌 형태로 인쇄해 놓고 그것을 표기법상의
     "redundancy" 라고 부른다. 열 편째의 새 형태 — **개념을 절반만 자기 쪽으로
     돌린다.**
  3. **이 카드의 질문에 그들이 답하지 **않은** 세 자리가 확정됐다.**
     (a) `[인쇄]` "any statements based on sensitivity gradients are **only valid
     locally**" — 전역 축퇴는 `[인쇄]` "we will report our findings in **future
     work**", (b) **추정기를 한 번도 돌리지 않는다** (Fig. 8·9 는 참값에서 평가한
     CRLB 이고 복원 오차·국소최소 분포가 없다), (c) **오차공분산 `C_θ` 를
     계산해 놓고 `sqrt(diag)` 만 그린다** — 축퇴의 **방향**(비대각·최소 고유벡터)을
     손에 쥔 채 한 번도 표시하지 않는다. **우리 프로젝트가 서 있는 자리가 정확히
     이 셋이다.**
  4. **점검 항목 2건이 새로 열렸다** (미검증, `[해석]`):
     - **B1**: 우리 목적함수의 x축이 `[코드 주석]` "각 셀 자기 용량" 정규화이므로
       (`src/fitting.py` 헤더) pOCV 항은 Lin 의 `U_OCV(z)` 에 해당하고 **형상
       자유도가 2개뿐**인데 우리는 **α_PE·β_PE·α_NE·β_NE 4개**를 맞춘다. 재구성이
       양 끝 컷오프 전압을 근사적으로 맞추면 제약 2개가 소모되어 유효 자유도가 2로
       떨어진다 — **Lin 이 Birkl/Mohtat 매개화를 비판한 바로 그 구조**
       (`[인쇄]` "non-independent parameters, of which the **redundancy**
       complicates their estimation"). 2026-09-03 (2) 에서 열어 둔 "우리가 관측한
       degeneracy 의 일부가 원전에 없는 자유도에서 온다" 가설의 **정확한 좌표**다.
       사영 대응: `z₀⁺ ↔ (β_NE−β_PE)/α_PE`, `r_N/P ↔ α_NE/α_PE`.
     - **B2**: **dQ/dV 항을 더해도 개선이 없었던 2026-08-20 결과가 이 논문으로
       설명될 수 있다.** `dQ/dV` 는 **같은 정규화 곡선의 함수**이므로 그 곡선이
       가진 자유도를 늘릴 수 없고, 국소 null 방향은 재가중에 **불변**이다.
       `[해석]` 논문은 이 말을 하지 않는다 — 2 자유도 진술에서 따라오며 값싸게
       확인 가능하다. 확인되면 그 실험 결과는 "우연" 이 아니라 **구조적 필연**이
       된다.
  5. **경험적 결론 하나가 해석식과 만났다.** `degradation-degeneracy/docs/
     07_LAM_LLI.md` 는 우리 셀을 NE-limited 로 기술하며 "**양극 활물질이 조금
     줄어도 전체 용량은 거의 안 변하므로, LAM_PE는 full-cell 곡선에 흔적을 거의
     남기지 않는다**" 고 적는다. Lin 식 (47) `∂Q̂max/∂Q̂⁺_max = z⁺_max λ⁺_l −
     z⁺_min λ⁺_u` 가 그 문장의 **일반 판정식**이다 (`λ⁺_l → 0` 이면 0으로 간다).
     `[해석]` 그리고 한 가지를 더 준다 — **`λ⁺_l` 은 SOH 에 따라 움직인다.**
     "LAM_PE 가 안 보인다" 는 이 셀의 고정된 성질이 아니라 `(r_N/P, z₀⁺)` 의 위치에
     따라 켜지고 꺼지는 성질이며, 우리 격자 안에서 그 전환이 일어나는지는 값싸게
     계산 가능하다. 미실행.
  - **다음 흡수 후보 2건 확정**: `[11]` **Mohtat et al. 2019** (*J. Power Sources*
    427, 101–111) 과 `[15]` **Lee et al. 2020** (*IEEE Trans. Ind. Inform.* 16(5),
    3376) — Lin 이 `[인쇄]` "They also derive the gradient … and **use Fisher
    information to quantify the parametric identifiability**" 라고 적는다. 즉
    **Fisher 를 이 문제에 처음 쓴 것은 Lin & Khoo 가 아니다.** 그리고 그 모델이
    `[인쇄]` "**has been incorporated in PyBaMM**" 이므로 우리 도구와 직접 닿는다.

- **[2026-09-03 (11)]** `active` 유지 — 이 위키가 **두 번 지목해 둔** 문헌을
  흡수했다 ([[nullspace-coefficient-interpretation]], Schaeffer et al.,
  *Comput. Chem. Eng.* **180** (2024) 108471, raw:
  `raw/papers/schaeffer2024_nullspace-regularization-interpretation.md`).
  2026-09-03 (4) 항목 2 에서 "저자 그룹 자신의 nullspace 논문인데 본문에서
  긍정 근거로만 인용된다" 고 적었던 Rhyu 2025 의 참고문헌 `[13]` 이 이것이다.
  이 카드에 달라진 것 넷:
  1. **Evidence For 2건 추가** (위): 축퇴 방향 위의 값은 추정기가 정한다는
     일반 명제 · "낮은 잔차 ⇒ 참에 가깝다" 의 그림판 반증.
     **Evidence Against 에는 아무것도 붙지 않는다** — 이 논문은 22p 분해가
     물리라는 쪽 근거를 하나도 주지 않는다 (열화 모드를 재지 않으므로).
  2. **★ 이 카드의 방법론에 도구가 하나 들어왔다.** 지금까지 이 카드는
     격자 스캔(전역)으로만 축퇴를 봤는데, 원전 식 (19)
     `v_γ = −(γ JᵀJ + I)⁻¹ θ_Δ` 를 쓰면 22p 동작점에서 **국소 축퇴 방향과
     valley 폭을 직접 계산**할 수 있다. 절차는 [[fitting-degeneracy]] 의
     "그 방향을 그리는 법" 절. **본 실행이 필요 없고 값이 싸다.**
     그 계산이 곧 (10) 항목 4 의 점검 항목 **B1** (우리 4-파라미터 창 모델의
     유효 자유도가 정말 2로 떨어지는가) 을 판정하는 방법이기도 하다 —
     `J` 의 특이값 스펙트럼에서 셋째 값이 얼마나 작은지를 보면 된다.
  3. **어휘 전수 (이 계보 열한 편째) — 새 형태다.** 본문 44,379자 + SI
     8,826자에서 `nullspace` **69/9회**로 비유일성을 **논문 전체의 주제**로
     다루는데, `identifiab*` **0** · `degenerac*` **0** · `non-unique`/`unique`
     **0** · `ill-posed` **0** · `Hessian` **0** · `Fisher` **0** ·
     `uncertaint*` **0** · `error bar` **0** · `confidence` **0**.
     `[해석]` 아홉 편의 "어휘가 없다", 열 편째의 "절반만 자기 쪽으로 돌린다"
     와 또 다르다 — **개념을 정면으로 다루면서 자기 어휘를 새로 만들고 표준
     어휘를 안 쓴다.** 그 결과 Lin & Khoo 2024 와 이 논문은 같은 수학적
     대상을 다루면서 **서로를 인용하지 않는다.**
  4. **이 논문 자신의 자기모순을 기록한다** (우리 서술의 반면교사):
     §1 에서 `[인쇄]` "such an interpretation can lead to misleading
     conclusions", §4.1 에서 `[인쇄]` "From the data alone, it is not possible
     to state whether 𝐲 was constructed from constant or parabolic
     coefficients" 라고 적은 뒤, §4.2.2 에서는 **참계수를 모르는 실측 응답**의
     계수 봉우리에 철 반사이트 결함 형성에너지(0.55 eV)까지 붙여 해석한다.
     그리고 `[재현]` 그 물리 해석이 가장 조밀한 3.0–3.3 V 가 **nullspace
     자유도가 가장 큰 구간**이다 (raw digest §12.3). `[해석]` 우리가 축퇴
     방향을 그린 뒤에도 정직하게 주장할 수 있는 것은 **"어디까지가 데이터
     인지 선을 긋는 것"** 까지다.
  - **다음 흡수 후보가 하나 늘었다**: `[인쇄]` §4.2.2 가 데이터 누수 회피
    근거로 인용하는 **Geslin et al. 2023**, "Selecting the appropriate features
    in battery lifetime predictions", *Joule* **7**, 1956–1965.

- [2026-09-03 (11)] **active 유지 — 해석해를 우리 좌표에서 처음 수치로 쟀다.
  그리고 판정이 "구조" 에서 "잡음" 으로 옮겨갔다.**

  satellite `mode-observability` Phase 1c (`docs/PHASE1C_NOTES.md`, 정본은
  `results/phase1c/` CSV · 아래는 사본 · 입력은 `grid_curves_v4` **읽기 전용**
  이라 RUN_SCOPE 와 봉인 산출물은 움직이지 않았다).

  **무엇을 쟀나.** [[np-lip-ocv-reparametrization]] 이 인쇄해 둔 null 방향
  (pristine 에서 `(1,1,1)/√3`)이 우리 격자에서 실제로 가장 평평한 방향인지,
  그리고 **얼마나** 평평한지. 절차는 [[nullspace-coefficient-interpretation]]
  에서 가져온 `JᵀJ` 최소 고유벡터다.

  | 결과 | 값 |
  |---|---|
  | 총용량 `(1−x)` 배 예측 | 상대오차 최대 **0.220 %** — 사실상 성립 |
  | 곡선 불변 예측 | **깨진다.** `max\|ΔV\|` = **0.417 mV per 1 %p** (x 에 비례) |
  | 깨짐의 방향 | **하나로 고정.** `ΔV/x` 상관 **0.9911↑**, `x_norm 0.839` (3.2785 V) 한 점 |
  | `u_min` vs `(1,1,1)/√3` | **12.04°** (`cos 0.977999`) |
  | 조건수 | **18.2** (특이값 0.689 / 2.786 / 12.571) |

  **이 카드에 대한 함의 — Evidence For 도 Against 도 아니다. 물음의 형태를
  바꾼다.**

  1. `[해석]` **"곡선이 원리적으로 못 가른다" 는 이 격자에서 성립하지 않는다.**
     조건수 18.2 는 ill-conditioned 라고 부를 값이 아니고, 1차 신호가
     0.417 mV/%p 로 남아 있다. 즉 **degeneracy 는 구조가 아니라 잡음·추정기의
     문제**다. 이것은 이 카드의 읽기 B 를 **약화**시키지 않는다 — 읽기 B 를
     **다른 문장으로 바꾼다**: "정보가 없다" 가 아니라 "정보가 잡음보다 작다".
  2. `[해석]` **그리고 그 잡음 문턱이 우리 격자 안에 있다.** σ = 5 mV 에서
     null ray 전체가 x = 20 % 까지 묻히고, σ = 1 mV 에서도 x ≤ 6 % 는 묻힌다.
     22p 삼중항은 x ≈ 13~17 % 구간이므로 **σ = 5 mV 에서 묻히고 σ = 1 mV 에서
     2σ 내외**다. 실제 셀의 잡음이 어느 쪽인지가 22p 판정을 **직접** 지배한다 —
     이것이 이 카드에 필요한 **새 입력**이고, 지금 우리에게 없다.
  3. `[해석]` **12.04° 의 틈이 B1 점검의 첫 단서다.** `u_min` 이 `(1,1,1)` 에서
     LAM_NE 쪽으로 기울었다(0.395 vs 0.577). 유한 전류와 음극 제한이 함께
     작용한 것으로 읽히지만 **몫이 갈리지 않는다.** 무전류 OCV 곡선으로 같은
     계산을 하면 갈린다 (Phase 1c 다음 단계 1번).

  **연결하지 않은 관찰**: Schaeffer 2024 의 LFP 에서 nullspace 자유도가 가장
  컸던 구간이 3.0–3.3 V, 우리 잔차 봉우리가 3.2785 V 다. **화학이 다르므로
  (LFP vs NMC811‖Gr+Si) 우연이며 증거가 아니다.** 좌표만 적어 둔다.

  **아직 아무도 안 그린 그림**: `θ₀ ± t·u_min` 을 따라 곡선을 겹쳐 그리는 것
  (Schaeffer Fig. 1b 의 우리 판). Lin 은 `C_θ` 를 쥐고 대각선만 그렸고,
  Schaeffer 는 959차원에서 포기했다. 우리는 1차원이고 기존 곡선만 쓴다.

- [2026-09-03 (12)] **active 유지 — 점검 B1 을 돌렸다. 부분만 맞다.**

  `mode-observability` Phase 1d (`docs/PHASE1D_NOTES.md`, 정본은
  `results/phase1d/` CSV · 아래는 사본 · 입력 읽기 전용).

  **물음.** 우리 fitting 은 창 좌표 `[α_PE, β_PE, α_NE, β_NE]` **4개**를
  맞추는데 컷오프 등식 제약이 없다. [[np-lip-ocv-reparametrization]] 에 따르면
  형상 자유도는 2 다. 그러면 우리가 본 degeneracy 의 일부는 **물리가 아니라
  좌표 선택**인가 — 판정은 `∂v_full/∂p` 의 특이값 스펙트럼이다.

  **결과 (pristine, 스텝 셋으로 확인).**

  | | σ1 | σ2 | σ3 | σ4 | σ3/σ1 | σ4/σ1 |
  |---|---|---|---|---|---|---|
  | 스텝 2e−3 | 49.47 | 12.82 | 2.567 | 1.661 | 0.0519 | 0.0336 |
  | 스텝 1e−2 | 42.26 | 12.36 | 2.323 | 1.174 | 0.0550 | 0.0278 |

  `[해석]` **"자유도가 2로 붕괴" 는 아니다.** Lin 의 redundancy 지적이 그대로
  오면 σ3·σ4 가 거의 0 이어야 하는데 **σ3/σ1 ≈ 0.05 · σ4/σ1 ≈ 0.03** 이고,
  스텝을 5배 흔들어도 유지된다 — 수치 잡음이 아니라 모델의 실제 성질이다.
  **유효 rank 는 4 이고 2 가 아니다.** 그러므로 **우리가 본 degeneracy 를
  "좌표 선택이 만든 것" 으로 돌릴 수 없다.**

  동시에 **비용은 실재한다** — 선행 방향 대비 3~5 % 밖에 안 보이는 방향이 둘
  있고 그것이 최적화가 헤맬 여지를 만든다. Lin 의 지적은 **틀린 것이 아니라
  크기가 과장된 것**으로 읽힌다.

  **⚠ 하면 안 되는 비교를 명시한다.** Phase 1c 의 조건수 18.2(모드 좌표 3개)와
  위 30~36(창 좌표 4개)을 **직접 비교하면 안 된다** — 두 좌표계의 단위가 다르고
  (α ≈ 1 무차원비 · β ≈ 0 이동량 · 모드는 분율손실), 조건수는 파라미터 스케일에
  따라 움직인다. 비교 가능한 것은 **같은 공간 안의 비율과 그 안정성**뿐이고 위
  판정은 그것만 썼다. 공통 물리 단위로 정규화하는 것이 다음 단계다.

  **부수 발견 — `src/fitting.py` 헤더의 경고를 실측이 반쯤 뒤집었다.** 그 헤더는
  33p 의 `lb = [1.00, …]` 하한에 최적화가 붙으면 "LAM_PE ≈ LAM_NE ≈ 용량손실" 이
  자동으로 나오므로 22p 패턴이 그것일 수 있다고 적는다. 실측: **pristine 참값이
  `α = 1.00000` 으로 정확히 하한에 얹혀 있고, 22p 근방(0.16, 0.12, 0.12)에서는
  `α = 1.05247` 로 떨어져 있다.** `[해석]` 그러므로 **22p(300 사이클) 동작점
  자체에서는 그 가설이 성립하지 않는다** — 거기서 참값은 하한이 아니다. 대신
  이 경고는 **저열화 영역(100·200 사이클 행)** 에 걸린다. 그쪽 fitting 결과의
  bound active 검사를 따로 집계해야 한다 (파이프라인이 이미 `_bound_active` 로
  재고 있으므로 집계만 남았다).

- **[2026-09-03 (13)]** `active` 유지 — 이 계열의 **마지막(13번째) 문헌**을
  흡수했다 ([[fused-lasso-feature-design-framework]] 의 데이터셋 원전,
  Cui et al., *Joule* **8** (2024) 3072–3087, raw:
  `raw/papers/cui2024_electrode-utilization-formation-cycle-life.md`). Rhyu 2025
  가 참고문헌 [47] 로 인용하는 바로 그 186셀·62프로토콜 데이터셋을 만들고 처음
  분석한 논문이다. 이 카드에 준 것 셋:
  1. **★ 잡음 문턱에 처음으로 실측 정박점이 생겼다.** DVA(differential voltage
     analysis) 적합 잔차 `[인쇄, SI Fig. S15 캡션]` "root mean squared error
     below **6 mV**" — 우리 σ = 5 mV 문턱과 같은 자릿수다(잔차이지 raw 잡음이
     아니므로 상한으로만 쓴다). 그리고 SI Table S3(반쪽전지 harvested-electrode
     반복측정, 원문 표에서 우리가 직접 계산)이 **전극별로 갈리는 재현성**을
     준다: **PE 전압 재현성 1–12 mV**(σ=1/5 mV 사이·근방), **NE 전압 재현성
     8–93 mV**(훨씬 나쁨 — NE 가 이 SOC 대역에서 평평해 작은 SOC 차이가
     컷오프 근처 전압으로 크게 증폭). `[해석]` 우리 Phase 1c/1d 가 가정한
     "전압 전체 창에 균일한 σ" 가 지나치게 단순할 수 있다는 첫 실측 근거다 —
     **Evidence 어느 쪽도 아니다, 다음 실측(전극별·SOC별 σ)의 입력값으로
     등재한다.**
  2. **이 논문 자신도 4-파라미터 DVA 적합에 오차막대가 없다** (Figure 8,
     `[Q_NE, Q_PE, SOC_NE,0, SOC_PE,0]`, optimizer 1종, 반복 시작점 비교 없음) —
     Rhyu SI Note S11·Birkl 2017·Dubarry 2012 와 같은 패턴의 **네 번째 야생
     사례**. 다만 이 논문은 half-cell 곡선이 **실측(해체 전극)**이라 Rhyu 의
     범용 OCV 다항식 모델보다 물리적으로 더 직접적이고, **Table S3 의 독립
     반쪽전지 측정**(DVA 적합이 아니라 별도 실측)이 DVA 가 추론한 방향과
     일치한다는 교차검증이 있다 — Birkl 2017 의 코인셀 검증과 같은 계열의
     **드문 사례**.
  3. **형성이 우리 격자의 시작점을 어디에 놓는지에 대한 실측 단서.** N/P 는
     셀 설계로 고정(`[인쇄, Table 1]` 1.16)이고 형성 프로토콜이 움직이는 것은
     `Q_Li`(∝ Li/P, Lin 의 `z0+` 방향) 하나뿐이다. `[해석]` 이것은 **`(1,1,1)`
     null 방향과는 다른 방향** — 형성 직후 상태는 이 카드가 다루는 flat
     direction 위가 아니라 z0+ 축(주로 LLI) 위에 있을 가능성을 시사한다.
     검증은 미실행이며, 값싸게 확인 가능하다(형성-유사 초기조건을 LLI 만 민
     지점으로 놓고 22p 류 분해를 재현).
  - 상세·근거 등급(A/B/C)·양쪽 원문 대조는 raw digest §2(사용자 질문 6개)·
    §11(우리 프로젝트 접점) 참조. 이 카드의 status 는 바뀌지 않는다(`active`
    유지) — 새 근거는 방법론적 패턴 확인과 잡음 정박점이지, 22p 수치 자체에
    대한 직접 증거는 아니다.

- **[2026-09-03 (14)]** `active` 유지 — **누락분 흡수. Evidence 어느 쪽도
  아니고 「경계 확정」이다** (Navidi et al., *Energy Storage Mater.* **68**
  (2024) 103343, raw:
  `raw/papers/navidi2024_piml-degradation-diagnostics-comparison.md`).
  사용자가 준 13편 중 digest 없이 빠져 있던 것. 제목이 "battery degradation
  diagnostics 의 state-of-the-art 방법 비교" 이지만, **실제 비교 축은 열화
  진단 방법이 아니라 하나의 진단 모델을 흉내 내는 ML 배관 네 개**다
  (PINN · co-kriging · delta learning(elastic net) · data augmentation).
  이 카드에 달라진 것 다섯:

  1. **★★ 우리 fitting 모델과 좌표가 글자 그대로 같은 첫 문헌이다.**
     `[인쇄, 부록 A1]` `V_c(Q) = V_p((Q−δ_p)/m_p) − V_n((Q−δ_n)/m_n)` —
     자유 파라미터 **4개**, **컷오프 등식 제약 없음**. 대응은
     `m_p ↔ α_PE · δ_p ↔ β_PE · m_n ↔ α_NE · δ_n ↔ β_NE` 다.
     [[birkl-ocv-degradation-diagnostic]] 의 3개(등식 소거)와 다르고
     **우리 창 모델과 같다.** 그리고 `[인쇄, §3]` `LII = Q_p − (δ_p − δ_n)`
     이 우리 문서의 `LLI = (1−α_PE) + (β_PE − β_NE)` 와 **구조가 같다**
     (잔량 vs 손실 표기 차이). `[해석]` 2026-09-03 (2)·(3) 에서 출처를 못
     찾고 종결했던 "legacy LLI 식" 에 대해, **같은 형태의 식이 실재하는
     자리가 처음 확인됐다.** ⚠ **인용 경로의 증거는 아니다** — 이 논문은
     2024년이고 그 식의 계보를 `[30]` Thelen 2022 · `[55]` Lui 2021 로
     돌린다. **후속 확인 항목으로만 등재하고 우리 문서는 고치지 않았다.**

  2. **★ 이 카드가 판정하려는 자동 적합을, 이 논문이 시험대에 올려 기각한다.**
     `[인쇄, 부록 A2]` "the optimization problem for automatic fitting **has
     multiple local minima, leading to run-to-run variability in optimal
     active mass parameters depending on the initial guess**. We illustrated
     this variability by presenting the mean and error bars (spread) derived
     from **five optimization runs, each starting at a different initial
     guess**." — 그리고 그 결론으로 **사람의 수동 적합**(부록 A1 의
     `(m_n,δ_n)` → `(m_p,δ_p)` 블록 교대)을 정답으로 채택한다.
     `[해석]` 그러므로 이 카드(와 우리 프로젝트)의 자리는 **"남이 안 한 것"이
     아니라 "남이 해 보고 못 쓴다고 결론 내린 것을, 그 결론이 근거로 삼은
     구별을 실제로 수행해 재판정하는 것"** 이다. 그들은 5개 해의 **목적함수
     값을 보고하지 않으므로** [[fitting-degeneracy]] 의 flat valley ↔
     multimodal 를 **구별하지 않은 채** 기각했다.

  3. **★ 그런데 같은 그림이 우리 진단의 한계도 준다 — 새 경고 1건.**
     `[도표, Fig. 15]` 자동 적합 다중시작 산포는 정규화 활물질 단위로
     **±1.5 ~ ±11 %p**(중앙값 ≈ ±5 %p, 우리 `tol = 2 %p` 의 1~5배)인데,
     같은 셀 해체 실측과 대조하면 **G2C1 `m_p` 에서 5개 해가 전부
     0.835–0.935 안에 있고 참값은 0.63** 이다. 즉 **다중시작 산포는 실제
     오차의 하한조차 아니다.** [[nullspace-coefficient-interpretation]] 의
     "낮은 잔차 ⇒ 참에 가깝다" 반증과 같은 계열의 두 번째 형태이며,
     우리는 참값을 알기 때문에 **산포 vs 실제 오차 산점도**로 직접 정량할
     수 있다 (미실행, 기존 artifact 재집계로 충분).

  4. **어휘 전수 (이 계보 열두 편째) — 또 새 형태다.** 본문+참고문헌
     138,573자에서 `identifiab*` **0** · `degenerac*` **0** · `nullspace`
     **0** · `non-unique`/`uniqueness` **0** · `collinear*` **0** ·
     `Hessian`·`Fisher`·`condition number`·`singular value` **각 0** ·
     `mV` **0**. 그런데 `uncertaint*` **21회로 이 계보 최다**이고,
     **그 21회 전부가 예측 불확실성이며 라벨·파라미터의 불확실성은 0회**다.
     `noise` 3회는 전부 "모형이 잡음을 외운다"(과적합). `[해석]`
     **불확실성 어휘를 갖췄으되 전부 출력 쪽에 쓰고 입력(라벨) 쪽에 한 번도
     안 쓰는 형태.** 그리고 **비교 논문이므로 침묵의 등급이 다르다** —
     `[인쇄, Table 5]` 는 열 개 축으로 네 방법을 등급 매기는데
     **"비유일성에 대한 강건성" 축이 없다.** 개별 논문이 자기 방법을 안 잰
     것과 달리, 그 축이 **선택지 목록 자체에 없었다**는 뜻이다.

  5. **정황 하나 — 총량은 쉽고 전극별 분해는 어렵다** (`[도표, Fig. 8]`,
     본문에는 수치가 **하나도 인쇄돼 있지 않다**): 일곱 모델 전부에서
     `Q` 는 0.55–1.37 % (기준선 NN 제외), `LII` 는 1.45–3.87 % 인데
     `m_p`·`m_n` 은 **3.68–9.85 %** 다. `[해석]` 이 위키가
     [[np-lip-ocv-reparametrization]] 에서 예측한 형태(형상 2 + 총용량 1)와
     같은 방향이지만 **증명이 아니다** — `m_p, m_n` 이 어려운 이유가 관측
     가능성인지 궤적의 비단조성인지 이 논문은 가르지 않고, 정답이 사람의
     적합이라 "어렵다"의 일부는 사람의 재현성일 수 있다.

  - **인용 금지 4건** (전부 자기 그림이 반증한다 — raw digest §7 표 I3–I7):
    ① `[인쇄, §6.3]` "all the PIML methods exhibited improved error rates" ↔
    co-kriging `Q` **1.37 vs 기준선 0.93**. ② `[인쇄, §7.2.2]` co-kriging
    용량 예측 "near-zero error rate" ↔ 1.37 %. ③ `[인쇄, §7.2.1]` PINN 이
    `m_p` 에서 우월 ↔ Data Augmentation **3.68 < PINN 4.52**.
    ④ `[인쇄, 부록 A2]` 수동·PINN 이 자동보다 실측에 가깝다 ↔ G1C3 `m_n`
    에서 **자동이 가장 가깝다**.
  - **후속 실험 3개** (전부 미실행·값싸다): 산포 vs 실제 오차 산점도 ·
    블록 교대 최적화(부록 A1 순서의 기계판) · **dQ/dV 봉우리 *위치* 2개만**
    목적함수에 추가(2026-08-20 에 시험한 것은 dQ/dV **곡선** 항이고,
    `[도표, Fig. 12]` `r3=0` 에서 `m_p` 가 등가중 대비 78 % 악화되므로
    위치 항은 다른 물건이다). 셋 다 RUN_SCOPE 밖(`mode-observability`)에서.
  - 우리 쪽 수치는 이 카드에 옮기지 않는다 — 정본은 artifact +
    `docs/RESULTS*.md`.

- **[2026-09-03 (15)]** `active` 유지 — **사용자가 준 13편의 마지막 누락분을
  흡수했다. Evidence 어느 쪽도 아니고 「경계 확정」이다** (Marongiu, Nlandi,
  Rong, Sauer, *J. Power Sources* **324** (2016) 158–169, raw:
  `raw/papers/marongiu2016_lfp-onboard-capacity-halfcell.md`). 제목에
  **half-cell curves** 가 들어간 유일한 편이고, 2026-09-03 (2) 항목 3 이
  legacy LLI 식의 출처 후보로 지목해 둔 **Birkl 참고문헌 [26] 이 이것**이다.
  이 카드에 달라진 것 다섯:

  1. **★★ 이 계보의 축퇴가 처음으로 닫힌 형태로 풀렸다 — 그리고 그것이 우리
     층에 없다는 것이 확정됐다.** 이 논문은 **모드 5개 → 창 좌표 4개** 사상을
     식으로 전부 인쇄한다 (`[인쇄]` 식 2–5, 부호는 조판본 400 dpi 재렌더링으로
     직접 확인). 등식 제약이 **0개**이므로 null 이 손으로 풀린다 —
     관측이 평탄역 **길이**(=차이)라 평행이동이 안 보이면 **null 2차원**:
     ```
     좌표: (ΔLLI, ΔLAM_Pe,Li, ΔLAM_Pe,De, ΔLAM_Ne,Li, ΔLAM_Ne,De), N = 로딩비
     n₁ = ( −N ,  0 ,  0 , +1 , −1 )
     n₂ = ( +1 , −1 , +1 ,  0 ,  0 )
     ```
     `[재현]` 두 방향 모두 네 창 좌표·세 관측·원전 식 (8) 의 **총용량을 정확히
     불변**으로 둔다. `n₁` 은 [[dubarry-mechanistic-mode-synthesis]] 의
     `{LAM_liNE = x} ≡ {LAM_deNE = x, LLI = LR·x}` 이고, 둘을 합치면
     **[[birkl-ocv-degradation-diagnostic]] 의 `[total-LLI, LAM_PE, LAM_NE]` 가
     정확히 `ℝ⁵/span{n₁,n₂}`** 다 (`[재현]` 두 방향을 그 셋에 넣으면 전부 0).
     계보 표: [[halfcell-window-parametrization-lineage]] (신설).
     `[해석]` **이 카드에 대한 함의**: 우리는 창 좌표 4개를 **직접** 맞추고
     모드 층을 만들지 않으므로 `n₁·n₂` 를 **물려받지 않는다.** 2026-09-03 (2)
     항목 2 에서 열어 둔 가설("우리가 관측한 degeneracy 의 일부가 원전에 없는
     자유도에서 온다")은 **모드→창 층에 대해서는 방향이 반대**임이 확인됐다 —
     원전 쪽에 여분이 더 많다. 남는 것은 창→관측 층이고 Phase 1d 가 그것을
     쟀다. **다만 우리 사후 변환(`LAM_PE = 1 − α_PE·r` 등)은 몫공간으로의
     사영이므로 우리 출력도 처음부터 몫공간의 값**이다 — 두 층을 섞으면 안 된다.

  2. **★ 성공 지표와 이 카드의 질문이 직교할 수 있다는 것이 증명됐다.**
     원전의 헤드라인은 `[인쇄]` "an error of approx. 1%" (용량)인데, 위 계산이
     **총용량이 두 null 방향 위에서 정확히 불변**임을 보인다. 즉 그 1 % 는
     모드 식별 가능성에 대해 **원리적으로 아무 말도 하지 않는다.** 저자들도
     그렇게 적는다: `[인쇄, p.165]` "The correct determination of all the
     degradation mechanisms which physically perfectly mirror the actual
     battery aging state **is out of the goal of this work**."
     `[해석]` 이 계보 열세 편 중 **가장 정직한 문장**이고, 동시에 우리가
     인용에서 절대 하면 안 되는 추론의 이름표다 — **"half-cell 재구성이 잘
     되더라" 는 분해가 물리라는 근거가 아니다.**
     (⚠ 같은 논문 §4.2.2 에는 이와 모순되는 `[인쇄]` "assures correctness of
     the tracked aging mechanisms" 가 있다. raw digest §10 ⑤.)

  3. **초기값이 답을 지배하는 것을 처음으로 통제 대조군에서 봤다.**
     `[인쇄, Table 5]` 관측을 평탄역 1개로 줄인 상태에서 `LAM_start` 만
     10 % → 0 % 로 바꾸면 용량 오차가 **6.38 → 14.46 %**(충전),
     **4.33 → 12.51 %**(방전). `[인쇄]` 저자 설명: "the smaller initial value
     … **which is kept for the final calculation** … due to the **lack of
     information to track this mechanism**." `[해석]`
     [[nullspace-coefficient-interpretation]] 의 일반 명제(축퇴 방향 위의 값은
     정칙화가 고른다)의 **야생 실측**이며, 관측 개수를 통제한 대조군과 함께
     나온 것은 이 계보에서 처음이다. 우리는 참값을 알므로 같은 설계로
     "초기값 → 실제 오차" 를 정량할 수 있다 (기존 artifact 재집계, 미실행).

  4. **관측을 늘렸더니 나빠졌다 — dQ/dV 결과에 경쟁 설명이 생겼다.**
     `[인쇄, Table 5]` 평탄역 **3개**(0.98 / 1.10 %) 가 **2개**(0.78 / 0.70 %)
     보다 나쁘다. 원인은 관측 중복 — `[인쇄]` 평탄역 VA 와 IIA 가 "decrease
     **proportionally**" 하므로 관측의 **유효 rank 는 2**이고, 남는 셋째가
     `[인쇄]` "the algorithm can **enter a closed loop**" 를 만든다.
     `[해석]` 2026-08-20 의 "dQ/dV 항을 더했더니 나빠졌다" 에 대해
     [[np-lip-ocv-reparametrization]] 점검 B2("자유도를 못 늘린다")와
     **경쟁하는 두 번째 설명**이다 — 전자는 정보 상한, 후자는 수렴 경로.
     우리는 목적함수 값을 저장하므로 [[fitting-degeneracy]] 의
     flat valley ↔ multimodal 로 **갈라낼 수 있다** (미실행).
     ⚠ 그 논문의 노름은 `L^∞`(또는 합 — 원문 안에서 불일치, raw §10 ③),
     우리는 `L²` 이므로 메커니즘을 그대로 옮기면 안 된다.

  5. **인용 계보 항목이 닫혔다.** 2026-09-03 (2) 항목 3 의 남은 후보 `[26]`
     을 확인했다. Birkl §3.1 이 `[인쇄]` "The theory underlying the proposed
     degradation modes and their effects on the OCV … is well documented in
     the literature **[19,26,29]**" 로 이 논문을 지목한다. 결과:
     **창 기하의 계보는 Dubarry 2012 → {Marongiu 2016, Birkl 2017} 로
     확정**되고, **legacy 식 `LLI = (1−α_PE) + (β_PE − β_NE)` 는 이 논문에도
     없다** (여기서 따라오는 것은 `β_NE − β_PE = LLI + N·LAM_Ne,Li −
     LAM_Pe,De` 로, `α` 항이 없고 부호가 반대다). 즉
     `degradation-degeneracy/docs/02_CODE_AUDIT.md` 의 2026-09-03 정정이
     **옳다.** 다만 현행 `src/fitting.py` 의 `κ·(β_NE − β_PE)` **부호 규약은
     이 논문 식 (4) 와 일치**한다 (Dubarry 에 이은 두 번째 확인).
     **이번 세션도 `degradation-degeneracy/` 를 읽기만 했고 고치지 않았다.**

  - **LFP 라는 화학이 준 부수 정박점 하나** (이 카드에 직접 닿지는 않는다):
    `[도표, Fig. 8c]` 신선셀 vs 노화셀(SoH 77–89 %)의 OCV 차이가
    **SoC 45–65 % 에서 1–3 mV** 이고 양 끝에서만 32–38 mV 다. 즉 LFP 에서는
    열화 전체가 중간 SoC 에 거의 전압 흔적을 안 남긴다 — 우리 σ = 5 mV 층이면
    통째로 묻힌다. **화학이 다르므로 우리 NMC811 격자에 옮겨 쓰면 안 되고**,
    "평탄한 화학에서 전압 관측이 얼마나 죽는가" 의 첫 실측 크기로만 등재한다.
  - 우리 쪽 수치는 이 카드에 옮기지 않는다 — 정본은 artifact +
    `docs/RESULTS*.md`.

- [2026-09-04] **active 유지 — 이 카드에 직접 닿는 실측 넷.** 정본은
  `mode-observability/results/phase1{e,g,h}/` 의 CSV. (`degradation-degeneracy/`
  는 이번에도 읽기만 했다.)

  1. **★ 22p 동작점에서 `u_min` 이 Lin 의 `(1,1,1)/√3` 와 4.61° 다** (Phase 1h,
     스텝 0.02). pristine 의 12.04° 보다 **더 가깝다.** `u_min` =
     `[0.5686, 0.5225, 0.6354]`, 조건수 16.31.
     `[해석]` **22p 의 축퇴는 Lin 의 닫힌 형태 축퇴와 사실상 같은 방향**이라는
     뜻이고, 그러므로 Lin 의 정리를 이 카드에 적용할 근거가 pristine 근방
     분석보다 **강하다.** 위 [2026-09-03 (11)] 이 "국소 분석이라 22p 에서
     회전할 수 있다" 고 유보한 자리가 닫혔다 — 회전하고, **Lin 쪽으로** 회전한다.

  2. **다만 "12.04°" 를 점 추정으로 인용하면 안 된다** (Phase 1h 훑기). 동작점
     8개 × 전방차분 스텝 2개에서 각이 **4.61° ~ 21.89°** 에 흩어지고, 같은
     pristine 에서 스텝만 0.02 → 0.04 로 바꿔도 **12.04° → 18.62°** 다.
     격자 간격이 0.02 라 더 작은 스텝은 이 자료로 못 잡는다. 위 표의 12.04° 는
     **한 점 추정**으로 읽어야 한다.

  3. **컷오프 등식을 얹어도 이 카드의 판정은 안 바뀐다** (Phase 1h). Birkl·Mohtat
     계열이 여분을 죽일 때 쓰는 두 등식 `U_full(x=0)=V_max`, `U_full(x=1)=V_min`
     의 gradient 가 pristine 에서 `(1,1,1)` 과 **83.95°·83.59°** (Lin 의 정리가
     예언하는 90° 근처)이고, 22p 에서 직교가 깨져도(`g₂` 44.16°) 두 끝점을
     관측에 더한 효과가 **σ_min +3.16 % / +5.95 %** 에 그친다. 그리고 그 두
     점은 애초에 **우리가 이미 맞추는 곡선의 양 끝**이다.
     덧붙여 **그 등식은 우리 참값에서 성립하지도 않는다** — 1023 조건에서 끝점
     전압이 **127 mV · 54 mV** 흔들린다(유한 전류 과전압).
     `[해석]` "제약을 걸어 자유도를 줄이면 22p 가 갈릴 것" 이라는 처방은
     **이 격자에서 기각**된다. 창 좌표에서도 같은 결론이었다 (Phase 1e: 제약이
     **강한** 특이쌍과 1.5°·2.0° → 여분이 아니라 정보를 지운다).

  4. **위 [2026-09-03 (11)] 3번의 "무전류 OCV 로 몫을 가른다" — 절반 갈렸다**
     (Phase 1g). 모드→곡선 변환을 시뮬에서 **순수 창 대수**로 바꿔도 각이
     `12.04° → 10.56°` 로 **1.48°** 밖에 안 움직인다. 그 경로엔 동역학이 없으므로
     **12° 는 동역학 산물이 아니라 창 모델의 구조에서 온다.** "음극 제한이 그중
     얼마인가" 는 여전히 미제이고, 그것을 재려면 평형 OCP 를 **셀 창으로**
     정규화하는 환산이 필요한데 그것이 Phase 1f 의 미제와 같은 것이다.

  **이 카드에 대한 함의**: 읽기 B("degeneracy 다")를 지지하지도 반박하지도
  않는다. 대신 **"제약을 더 걸면 갈린다" 는 출구가 하나 닫혔고**, 22p 가 놓인
  방향이 Lin 의 해석적 null 과 4.61° 라는 것이 새로 확정됐다. 판정을 지배하는
  것은 여전히 **실제 셀의 잡음 σ** 이고 그 입력은 아직 없다.

### 이 카드가 속한 논지 (2026-09-03)

이 질문이 왜 아직 열려 있는가를 계보 전체로 넓혀 방어한 문서:
[[mode-identifiability-unmeasured-lineage]] — **13편 중 분해의 유일성을 잰 편이
하나도 없다.** 이 카드의 Evidence 는 그 논지의 §5·§6 으로 들어가 있고, 거기
Counter-arguments (a)~(e) 가 보존돼 있다.
