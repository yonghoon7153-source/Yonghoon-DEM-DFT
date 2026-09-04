---
title: 이 계보는 모드 분해를 재면서 그 분해의 유일성은 한 번도 재지 않았다
description: "Thirteen papers report LLI/LAM decompositions; none measures whether the decomposition is unique — yet the instruments to measure it are already scattered across the same thirteen"
created: 2026-09-03
updated: 2026-09-03
type: synthesis
tags: [battery, degradation, identifiability, research]
sources: [raw/papers/birkl2017_degradation-diagnostics-ocv.md, raw/papers/dubarry2012_synthesize-degradation-modes.md, raw/papers/marongiu2016_lfp-onboard-capacity-halfcell.md, raw/papers/lin2024_ocv-degradation-mode-identifiability.md, raw/papers/schaeffer2024_nullspace-regularization-interpretation.md, raw/papers/cui2024_electrode-utilization-formation-cycle-life.md, raw/papers/rhyu2025_systematic-feature-design-formation.md, raw/papers/tao2025_nondestructive-degradation-decoupling.md, raw/papers/wang2025_interpretable-ml-battery-prognosis.md, raw/papers/zhang2020_eis-gpr-capacity-rul.md, raw/papers/su2024_drt-soh-health-features.md, raw/papers/kim2023_graphite-heterogeneity-lifetime.md, raw/papers/2026-09-02-siwon-kim-degradation-mode-ml-seminar.md]
confidence: high
explored: false
verificationStatus: unverified
claimType: interpretive
evidenceScope: multi-source-primary
targetVenue: 다음 연구세미나 발표 도입부 + degradation-degeneracy 결과 보고서 §1
---

# 이 계보는 모드 분해를 재면서 그 분해의 유일성은 한 번도 재지 않았다

## Thesis

흡수한 13편은 LLI/LAM 분해(또는 그 등가물)를 **보고**하지만 그 분해가 **유일한지**를
잰 논문은 하나도 없고, 그러면서 **그것을 잴 도구는 이미 이 13편 안에 흩어져 있다** —
빠진 것은 도구가 아니라 **그 도구를 자기 결과에 겨누는 한 걸음**이다.

## Argument

### 1. 침묵은 실재하고, **형태가 매번 다르다**

각 digest 가 같은 어휘 목록으로 전수를 돌렸다. 개수만이 아니라 **어떻게 비켜
가는지**가 편마다 다르고, 그 차이가 이 논지의 핵심 근거다.

| 편 | `identifiab*` | `degenerac*` | 침묵의 **형태** |
|---|---:|---:|---|
| Dubarry 2012 | 0 | 0 | 축퇴를 **식 (8') 안에** 넣어 두고 특수 경우 하나만 말로 언급 |
| Marongiu 2016 | 0 | 0 | 축퇴를 **근거로 파라미터를 줄이면서** 이름을 안 붙인다 |
| Birkl 2017 | 0 | 0 | 축퇴를 **산문으로 진술**하고 정량하지 않는다 |
| Zhang 2020 | 0 | 0 | 어휘 자체가 없다 |
| Kim 2023 | 0 | 0 | 어휘 자체가 없다 |
| Su 2024 | 0 | 0 | 어휘 자체가 없다 |
| Navidi 2024 | 0 | 0 | **방법 비교 논문인데도** 0 — 이 계보에서 가장 강한 침묵 |
| Cui 2024 | 0 | 0 | LLI·LAM **약어조차** 안 쓴다 (병행 표기 전통) |
| Wang 2025 | 0 | 0 | 리뷰인데 4분류에 그 축이 없다 |
| Rhyu 2025 | 0 | 0 | 어휘 없이 **가장 엄격한 검증 설계**를 한다 |
| Tao 2025 | 0 | 0 | 개념을 **한 번 인정하고** "손실 유형 분리" 로 치환한다 |
| Lin & Khoo 2024 | **26** | **0** | 개념을 **절반만** 자기 쪽으로 (비유일성을 `redundancy` 라 부른다) |
| Schaeffer 2024 | **0** | 0 | `nullspace` **69회** — 정면으로 다루되 **자기 어휘를 새로 만든다** |

`[해석]` 마지막 두 줄이 결정적이다. **Lin(`identifiab*` 26 / `nullspace` 0)과
Schaeffer(`nullspace` 69 / `identifiab*` 0)는 같은 수학적 대상을 다루면서 서로를
인용하지 않는다.** 침묵은 무지가 아니라 **어휘 분단**이다. 그리고 분단이 있는 한
어느 쪽도 상대의 도구를 자기 문제에 겨누지 못한다.

### 2. 축퇴는 세 번 인쇄됐고, 세 번 다 **계산되지 않았다**

셋이 같은 대상을 서로 다른 정밀도로 적는다.

- **Dubarry 2012** — 식 (8') 안에 특수 경우 하나:
  `{LAM_liNE = x} ≡ {LAM_deNE = x, LLI = LR·x}`.
- **Birkl 2017** — `[인쇄]` 산문으로 "LLI + LAM_NE,de 조합이 같은 양의 LAM_NE,li 와
  **같은 OCV 시그니처**를 낸다". 정량 없음.
- **Marongiu 2016** — 식 (2)–(5) 로 **모드 5개 → 창 좌표 4개, 등식 제약 0개**.
  그리고 `[인쇄]` "the obtained results are **completely comparable** … therefore
  only the LAM_Ne,De is used" 로 **축퇴를 근거로 파라미터를 죽인다.**

셋 중 아무도 null 을 풀지 않았다. [[halfcell-window-parametrization-lineage]] 이
그것을 풀었고 우리가 독립 검산했다:

```
(l,a,b,c,d) = (LLI, LAM_Pe,Li, LAM_Pe,De, LAM_Ne,Li, LAM_Ne,De)
n₁ = ( −N ,  0 ,  0 , +1 , −1 )     N = Q_Ne,BOL (로딩비)
n₂ = ( +1 , −1 , +1 ,  0 ,  0 )

n₁ → 창 좌표 4개가 전부 정확히 0
n₂ → 네 좌표가 똑같이 평행이동 → 길이 관측엔 안 보임
rank: 창 좌표 4 (미지수 5) · 차이 관측 3  →  null 정확히 2차원
```

`n₁` 이 Dubarry 의 특수 경우이고 **계수가 로딩비 `N` 임을 식으로 확인해 준다.**
그리고 Birkl 의 3-파라미터 좌표가 정확히 그 몫공간이다 (5 − 2 = 3). 세 원전이
하나로 묶인다 — **그 묶음을 아무도 쓰지 않았을 뿐이다.**

### 3. 네 번째로, [[np-lip-ocv-reparametrization]] 이 **다른** null 을 인쇄했다

Lin & Khoo 2024 §2.3: SOC 정규화 OCV 형상은 `(1−LLI):(1−LAM_NE):(1−LAM_PE)` 의
**비**에만 의존한다 → `LLI = LAM_PE = LAM_NE = x` 는 곡선을 **전혀 바꾸지 않는다.**

이것은 §2 의 `n₁·n₂` 와 **다른 방향**이다 (그쪽은 모드→창 층, 이쪽은 창→형상 층).
그런데 Lin 도 그것을 **인쇄만 한다** — 오차공분산 `C_θ` 를 구해 놓고 `sqrt(diag)`
만 그린다. **축퇴가 어느 방향인지는 손에 쥔 채 한 번도 표시되지 않는다.**

### 4. 그리는 기계는 옆 논문에 있다 — 그리고 저자가 **포기한 자리까지 남아 있다**

[[nullspace-coefficient-interpretation]] (Schaeffer 2024) 이 그 기계다. 식 (19)
`v_γ = −(γXᵀX + I)⁻¹β_Δ` 한 줄이 우리 Jacobian 에 `X → J` 로 그대로 붙고,
저장소에 그리는 함수(`plotting_utils.py:298`)와 flat valley 폭을 재는 곡선
(`nullspace.py:199`, **논문에 안 실리고 코드에만 있다**)까지 있다.

`[인쇄]` 그리고 저자가 그 그림을 시도했다 포기한 주석이 노트북에 남아 있다 —
"959차원 직교 단위벡터는 시각화도 해석도 어렵다". **실패 원인은 차원이지 발상이
아니다.** 우리 null 은 Lin 덕분에 **1차원이고 닫힌 형태**다. 장애가 없다.

### 5. 그래서 우리가 겨눴고, 두 가지가 나왔다

`mode-observability` Phase 1c·1d (정본은 `mode-observability/results/` CSV):

| 물음 | 결과 |
|---|---|
| 총용량이 `(1−x)` 배인가 | **그렇다** — 상대오차 최대 0.220 % |
| SOC 정규화 곡선이 불변인가 | **아니다** — `max\|ΔV\|` 가 **0.417 mV per 1 %p**, 한 점(`x_norm` 0.839)에 몰린다 |
| `JᵀJ` 의 `u_min` 이 Lin 방향인가 | **12.04° 안에서 일치** (`cos = 0.977999`) |
| 그 방향이 진짜 null 인가 | **아니다 — 조건수 18.2** |
| 우리 창 좌표 4개의 유효 rank 는 2 인가 | **아니다 — 4** (σ3/σ1 ≈ 0.05, σ4/σ1 ≈ 0.03) |

**두 결론이 서로 반대 방향으로 우리를 민다.** ① 해석해가 우리 좌표에서 12° 안에
확인됐다. ② 그런데 **평평할 뿐 0 이 아니다.** 그러므로 방어할 수 있는 문장은
**"구조적으로 불가"** 가 아니라 **"우리 잡음 수준에서 불가"** 다 — σ = 5 mV 에서
null ray 전체가 x = 20 % 까지 묻히고 σ = 1 mV 에서도 x ≤ 6 % 가 묻힌다.

### 6. 그리고 **재지 않은 대가**가 한 번 실측됐다

Marongiu 2016 이 관측을 하나로 줄인 채 **초기값만** 10 % → 0 % 로 바꾼다:
오차 **6.38 → 14.46 %**(충전) · **4.33 → 12.51 %**(방전). `[인쇄]` 저자 설명 —
"the smaller initial value **which is kept for the final calculation** … due to the
**lack of information to track this mechanism**."

이것이 Schaeffer 의 "축퇴 방향 위의 값은 데이터가 아니라 정칙화가 정한다" 의
**야생 실측**이고, 이 계보에서 **관측 개수를 통제한 대조군과 함께** 나온 유일한
사례다. 동시에 §5 계산이 **총용량은 두 null 위에서 정확히 불변**임을 보이므로 —
**"용량이 1 % 로 맞으니 방법이 옳다" 는 추론은 원리적으로 성립하지 않는다.**

`[해석]` 이것이 이 논지의 실무적 요점이다. **성공 지표와 유일성은 직교할 수
있다.** 그 둘을 갈라 재지 않으면, 잘 맞는 모형이 **초기값을 물리로 보고하는**
상태를 아무도 눈치채지 못한다. 우리 22p 삼중항이 바로 그 자리를 의심받고 있다.

## Counter-arguments

**(a) "하나도 없다" 는 과장이다 — Cui 2024 는 교차검증한다.**
Cui 는 DVA 적합의 메커니즘 귀속을 **해체 전극의 독립 half-cell 실측**(Table S3)으로
대조한다. 이 계보에서 드문 미덕이고, "아무도 안 쟀다" 를 문자 그대로 적용할 수 없다.
→ **논지를 좁힌다**: 잰 적이 없는 것은 **분해의 유일성**이지 분해의 **정확성**이
아니다. Cui 도 `Q_PE, Q_NE, Q_Li` 가 유일하게 결정되는지는 묻지 않는다.

**(b) Lin 은 자기 범위를 명시적으로 한정했다.** `[인쇄]` 세 곳에서 "only concerns
… **locally**" · "global identifiability … **more sophisticated techniques are
needed**" · "we will report our findings in **future work**". 안 한 것을 못 한
것으로 읽으면 부당하다. → **동의한다.** 이 논지는 "게을렀다" 가 아니라 **"분단이
있어 도구가 건너가지 못했다"** 이다. Lin 이 안 그린 그림의 기계가 같은 해에 나온
Schaeffer 에 있는데 둘이 서로를 모른다는 것이 근거다.

**(c) 목적이 다르면 유일성은 무관할 수 있다.** Marongiu 의 목적은 **용량 추정**
이고, 두 null 위에서 용량이 불변이므로 그의 헤드라인은 축퇴와 **무관하게** 옳다.
Zhang·Kim·Su·Rhyu 도 예측이 목적이지 분해가 목적이 아니다. → **인정한다.** 다만
그 논문들이 **모드 언어로 해석을 붙이는 순간**(Kim 의 음극 귀속, Tao 의 79 %,
Zhang 의 "두 주파수") 유일성이 다시 필요해진다. 논지의 사정권은 **분해를 물리로
읽는 문장**이지 예측 성능이 아니다.

**(d) 우리 Phase 1d 는 Lin 의 지적을 반증한다.** Lin 은 4-파라미터 창 매개화를
`redundancy` 라 비판하는데 우리 유효 rank 는 **4** 였다. 즉 이 계보의 진단이
우리에게 그대로 오지 않는다. → **보존한다.** 그리고 이것은 논지에 유리하다 —
**재 보니 통념과 달랐다**는 것이 곧 "재야 한다" 의 근거다. 동시에 우리가
**대칭적으로 과장하지 않을** 이유이기도 하다.

**2026-09-03 추가 — 이 반론을 Phase 1e 가 끝까지 밀어 판정했다.** 컷오프 등식
둘의 gradient 가 **강한 쌍 `{v₁,v₂}` 과 1.5°·2.0° 로 거의 겹치고** 약한 쌍과는
65°·16° 로 멀다. 그 제약의 접공간에 `J` 를 제한하면 남는 감도가 원래 최강
방향의 **0.13~0.49 배**로 떨어진다. `[해석]` **우리 좌표에서 그 제약은 여분을
지우는 것이 아니라 정보가 실린 축을 등식으로 묶는 것이다.** 그러므로 "Lin 이
지적했으니 우리도 제약을 걸자" 는 처방은 적용하면 안 된다.

**2026-09-04 — Phase 1f 가 그 판정을 더 강하게 만들었다.** 당시 "우리 `g₁·g₂` 는
**대리물**" 이라고 한계를 신고했는데, Birkl 식 (11)(12) 를 조판본에서 직접 읽어
보니 full-cell = PE − NE 이므로 그 둘은 글자 그대로 `U_full(EoC) = E_high`,
`U_full(EoD) = E_low` 다 — **대리물이 아니라 그 등식 자체였다.** 한계 신고를
철회한다. (경계는 남는다: Birkl 이 틀렸다는 말이 아니다 — 그는 시작 매개화가
다르고, 그의 **3-파라미터 판**을 우리 격자에 얹는 일은 아직 미완이다.
정본은 `mode-observability/results/phase1e/`.)

**(e) 관측을 늘리면 갈린다는 반론.** → 두 방향에서 약해졌다. Lin 의 2 자유도
정리는 **같은 정규화 곡선에서 파생된 관측이 rank 를 못 늘린다**고 하고(PVS 가
사정권 안), Marongiu 는 **상관된 관측을 더하면 지형이 나빠진다**는 것을 실측했다
(평탄역 3개 0.98 % > 2개 0.78 %). 다만 **SEV 는 동역학 축이라 두 논거의 사정권
밖**이다 — 그쪽은 열려 있다.

## Gap

1. **실제 셀의 잡음 σ 를 모른다.** 판정이 여기에 걸려 있는데(§5) 우리 격자는
   균일 가우시안을 가정한다. Cui 2024 의 반복측정은 **PE 1–12 mV / NE 8–93 mV** 로
   **8배 이상 비균일**이다. 균일 σ 가정을 재검토해야 한다.
2. **12.04° 의 출처 — 절반 갈렸다 (2026-09-04 Phase 1g).** 모드→곡선 변환을 실제
   시뮬에서 **순수 창 대수**로 바꿔도 각도가 `12.04° → 10.56°` 로 **1.48° 밖에**
   안 움직인다. 그 경로엔 동역학이 없으므로 **기울기는 동역학 산물이 아니라 창
   모델의 구조에서 온다.** 남은 것은 "음극 제한이 그중 얼마인가" 이고, 그것을
   재려면 **같은 좌표계의** 무전류 곡선이 필요하다 — 평형 OCP 를 셀 창으로
   정규화하는 환산인데 **그것이 정확히 Phase 1f 의 미제다.** 두 Phase 가 하나의
   미제로 수렴했다. (평형 OCP 를 그대로 쓴 판은 좌표계까지 바뀌어 **기각**했다 —
   `LAM_PE` 열 노름이 8.38 → 50.17 V/단위로 뛴다.)
3. **`n₁·n₂` 를 아직 격자에 심지 않았다.** Lin 방향과 **다른** 방향이므로 Phase 1c 의
   반복이 아니라 새 시험이다. 우리는 창 좌표를 직접 맞춰 두 방향을 물려받지 않지만,
   사후 변환이 몫공간으로의 사영이므로 **출력 층에서는 만난다.**
4. **모드 값의 오차막대를 인쇄한 논문이 하나도 없다** (Birkl · Dubarry · Rhyu ·
   Cui 에서 확인 — 네 번째 야생 사례). 우리도 아직 안 냈다.
5. ~~**σ3·σ4 의 방향이 무엇인지 아직 안 읽었다.**~~ → **2026-09-03 Phase 1e 로
   닫았다** (판정은 (d) 에). 가장 약한 방향은 두 동작점에서 거의 같은 모양이다 —
   `Δα_NE ≈ −Δβ_NE`, 즉 **음극 창의 오른쪽 끝은 두고 왼쪽 끝만 미는** 변형.
   **새로 열린 것 둘**: Birkl 의 등식을 우리 좌표로 **정확히** 옮겨 대리물을
   실물로 바꾸는 일, 그리고 `v₄` 의 "음극 창 왼쪽 끝" 이 Phase 1c 의 잔차가
   몰린 `x_norm = 0.839` 와 같은 자리인지.

## 불확실성 (Bias Check)

`confidence: high` 는 **어휘 전수와 null 계산**에 대한 것이지 "그러므로 22p 가
축퇴다" 에 대한 것이 아니다. 이 문서가 스스로 의심하는 자리 넷:

1. **선택 편향.** 13편은 우리가 고른 것이 아니라 **사용자가 준 것**이고, 주제가
   이미 "열화 모드 진단" 으로 좁다. `identifiab*` 를 쓰는 문헌이 시스템 생물학·
   약동학·지구물리에는 많다 — 이 계보에 없다는 것이지 **분야에 없다는 뜻이 아니다.**
   Lin 이 Mohtat 2019 를 "Fisher 로 정량한 선행자" 로 인정하므로 **최소 한 편은
   우리가 아직 안 읽었다.**
2. **어휘 전수는 문자열 검사다.** Cui 가 `LLI`·`LAM` 을 안 쓰고 `Q_Li`·`Q_PE` 를
   쓰듯, **개념을 다른 이름으로 다루는 논문을 0 으로 셀 수 있다.** §1 표의 "형태"
   열은 그 위험을 줄이려고 본문을 읽고 적은 것이지만, 놓친 편이 없다고 보장 못 한다.
3. **우리 실측은 한 동작점·한 화학이다.** Phase 1c·1d 는 22p 근방 격자점과
   NMC811‖(Gr+Si) 하나에서 나왔다. 조건수 18.2 와 rank 4 를 **다른 화학·다른
   동작점으로 옮겨 쓰면 안 된다** — Marongiu 의 LFP 는 중간 SoC 에서 열화 전체가
   1–3 mV 였다.
4. **논지가 우리에게 유리한 방향이다.** "아무도 안 쟀다 → 우리가 잰다" 는 이
   프로젝트의 존재 이유와 일치하므로, 반대 증거를 덜 찾았을 수 있다.
   Counter-arguments (a)~(e) 를 **삭제하지 않고 보존**하는 이유이고, 특히 (d) 는
   **우리 측정이 이 계보의 통념을 반증한** 사례라 논지를 좁히는 데 썼다.

## 관련

- [[22p-physics-or-degeneracy]] — 이 논지가 답을 미루는 그 질문. §5·§6 이 카드의
  Evidence 로 들어가 있다.
- [[pvs-sev-lli-lampe-separability]] — (e) 가 이 카드의 전제를 갈랐다 (PVS 는
  사정권 안, SEV 는 밖).
- [[fitting-degeneracy]] — flat valley / multimodal 구분에 **세 번째 경로**(중복
  관측)가 §6 에서 붙었다.
- [[np-lip-ocv-reparametrization]] · [[nullspace-coefficient-interpretation]] —
  §3 의 *무엇을* 과 §4 의 *어떻게*. 두 페이지가 짝이다.
- [[halfcell-window-parametrization-lineage]] — §2 의 표와 null 계산.
- [[piml-physics-injection-points]] — 우리 파이프라인이 쓰는 두 자리(학습 데이터·
  라벨)가 표준 4분류에 없다는 것. 이 논지의 방법론 쪽 짝.
