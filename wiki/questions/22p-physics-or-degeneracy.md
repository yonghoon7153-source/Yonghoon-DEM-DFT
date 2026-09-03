---
title: 22p 결과는 물리인가 fitting degeneracy 인가
description: "Is the seminar 22p LLI/LAM decomposition (LAM_PE=LAM_NE=13%, LLI=17%) real physics or an artifact of non-identifiability"
created: 2026-08-11
updated: 2026-09-03
type: research-question
tags: [battery, degradation, research]
sources: [raw/repositories/degradation-degeneracy-audit.md, raw/papers/birkl2017_degradation-diagnostics-ocv.md, raw/papers/rhyu2025_systematic-feature-design-formation.md]
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
