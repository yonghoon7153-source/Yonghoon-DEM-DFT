---
title: 반쪽전지 창 매개화 계보 비교 (자유도와 제약)
description: "같은 4개 창 좌표를 무엇으로 매개화하고 여분을 어떻게 죽이는가 — Dubarry 2012 부터 우리 파이프라인까지"
created: 2026-09-03
updated: 2026-09-04
type: comparison
tags: [battery, degradation, research]
sources: [raw/papers/marongiu2016_lfp-onboard-capacity-halfcell.md, raw/papers/birkl2017_degradation-diagnostics-ocv.md, raw/papers/dubarry2012_synthesize-degradation-modes.md, raw/papers/lin2024_ocv-degradation-mode-identifiability.md, raw/papers/navidi2024_piml-degradation-diagnostics-comparison.md, raw/papers/rhyu2025_systematic-feature-design-formation.md, raw/papers/mohtat2019_electrode-soh-estimability-expansion.md]
confidence: high
explored: false
verificationStatus: unverified
claimType: theoretical
evidenceScope: multi-source-primary
---

# 반쪽전지 창 매개화 계보 비교 (자유도와 제약)

## 비교 이유

우리 파이프라인이 하는 일 — 반쪽전지 곡선 두 개를 **창(window)** 으로 늘이고
밀어 full-cell 을 재구성하고, 그 창에서 LLI/LAM 을 읽는 것 — 은 이 계보 전체가
공유한다. 그런데 **창 좌표는 어디서나 4개**다: 전극 2개 × (폭, 위치).
갈리는 것은 **그 4개를 무엇으로 매개화하고, 남는 여분을 어떻게 죽이느냐**다.

이 페이지가 그 축 하나로 여섯 문헌 + 우리 것을 나란히 놓는다.
[[fitting-degeneracy]] 가 "우리가 본 축퇴의 일부가 좌표 선택에서 오는가" 를
물을 때 봐야 할 표이고, [[np-lip-ocv-reparametrization]] 이 비판하는
`[인쇄]` "non-independent parameters, of which the **redundancy** complicates
their estimation" 의 구체적 목록이다.

## 비교표

| 문헌 | 자유 파라미터 | 개수 | 등식 제약 | 여분 처리 | 관측 |
|---|---|---|---|---|---|
| [[dubarry-mechanistic-mode-synthesis]] 2012 | `LR`, `OFS` | **2** | 0 | 여분 없음 (2→2) | full-cell 곡선 · ICA |
| **Marongiu 2016 (모델)** | `LLI, LAM_Pe,Li, LAM_Pe,De, LAM_Ne,Li, LAM_Ne,De` | **5** | **0** | **없음 → null 2차원** | 평탄역 길이 3개 (Ah) |
| **Marongiu 2016 (실행)** | `LLI, LAM_Ne,De` | **2** | 0 | **나머지 3개 = 0 하드 고정** (사전 믿음) | 평탄역 길이 1~3개 |
| [[birkl-ocv-degradation-diagnostic]] 2017 | `LLI, LAM_PE, LAM_NE` (+`Δx_EoC, Δx_EoD`) | **3** | **2** | **컷오프 전압 등식으로 소거** | full-cell 전압 곡선 |
| **Mohtat 2019 (원전 표기 — 2026-09-04 확인)** | `x_100, y_100, C_n, C_p` | **4** | **1** (`U_p(y₁₀₀) − U_n(x₁₀₀) = V_max` 만) | 등식 1개 → **3**. 셀 용량 `C` 는 제약이 아니라 **추정 후** 식 (27) 로 푼다 | full-cell OCV **+ 셀 팽창(μm)** |
| Mohtat 2019 (구현본: PyBaMM `_ElectrodeSOH`) | `x_100, y_100, x_0, y_0` (+`Q`) | **5** | **2** | 같은 문제의 **다른 장부** → 역시 Ah 축 자유도 **3** | full-cell OCV |
| [[np-lip-ocv-reparametrization]] (Lin 2024) | `r_N/P`, `z₀⁺` | **2** | 0 | **재매개화로 애초에 안 만든다** | SOC 정규화 OCV **형상** |
| Navidi 2024 (부록 A1) | `m_p, δ_p, m_n, δ_n` | **4** | **0** | 여분 없음 (전단사) | full-cell 전압 곡선 |
| [[fused-lasso-feature-design-framework]] SI S11 | `β_c, β_a, Q_rem, V_shift` | **4** | 0 | 여분 없음 | C/20 RPT 곡선 |
| **우리 (`degradation-degeneracy`)** | `α_PE, β_PE, α_NE, β_NE` | **4** | **0** | 여분 없음 (전단사) | full-cell 전압 곡선 (+옵션 dQ/dV) |

## ★ 여분을 죽이는 방법이 세 가지뿐이다

`[해석]` 위 표를 세로로 읽으면 처방이 셋으로 갈린다.

1. **등식으로 죽인다** (Birkl, Mohtat). 컷오프 전압이 방정식을 준다. 값은
   데이터가 정하지만, **반쪽전지 OCP 의 절대 전압 정확도에 민감**해진다
   (등식이 4.2 V / 2.7 V 같은 절대값을 쓴다).
   `[실측 2026-09-04]` 이 처방을 우리 자료에 얹으면 **두 좌표계 모두에서 손해**다.
   창 좌표: 제약 gradient 가 **강한** 특이쌍과 1.5°·2.0° → 여분이 아니라 정보를
   지운다 (Phase 1e). 모드 좌표: 두 등식이 pristine 에서 null 방향과 거의
   직교(84°)해 축퇴를 못 보고, 끝점 2개를 관측에 더해도 σ_min 이 3~6 % 오를
   뿐이다 (Phase 1h). 게다가 **등식이 참값에서 성립하지도 않는다** — 1023 조건에서
   끝점 전압이 127 mV / 54 mV 흔들린다(유한 전류). 정본:
   `mode-observability/results/phase1e/`, `.../phase1h/`.
2. **사전 믿음으로 죽인다** (Marongiu). 5개 모드 중 3개를 0으로 못박는다.
   근거는 데이터가 아니라 **다른 논문의 해체분석**이다. 싸고, 대신 죽인 방향
   위의 값은 **모델러가 고른 값**이 된다 ([[nullspace-coefficient-interpretation]]).
3. **애초에 안 만든다** (Lin, Navidi, Rhyu, **우리**). 창 좌표(또는 그
   재매개화)를 직접 자유 파라미터로 쓰고 모드 층을 만들지 않는다. 모드는
   **사후 변환**으로 얻으며, 그 변환이 곧 **몫공간으로의 사영**이다.

`[해석]` **3번이 축퇴를 없애는 것이 아니다.** 없애는 것은 *모드→창* 사상의
축퇴뿐이고, *창→관측* 의 조건수 문제는 그대로 남는다. 우리 Phase 1d 가 잰
것이 후자다 (σ3/σ1 ≈ 0.05, σ4/σ1 ≈ 0.03 — 수치 정본은
`mode-observability/results/phase1d/`).

## ★ Marongiu 식 (2)–(5) 의 null 을 닫힌 형태로 풀었다

`[해석]` 재료는 전부 `[인쇄]` (원전 식 2–5, 8), 계산은 이 위키가 했다.
상세와 수치 검증은 `raw/papers/marongiu2016_lfp-onboard-capacity-halfcell.md` §5.

`P = Q_Pe,BOL = 1`, `N = Q_Ne,BOL`(로딩비) 로 두고
`(l,a,b,c,d) = (LLI, LAM_Pe,Li, LAM_Pe,De, LAM_Ne,Li, LAM_Ne,De)` 라 하면

```
Q_Ne,start = −b                    Q_Pe,start = −cN − l
Q_Ne,end   = N(1−c−d) − b          Q_Pe,end   = 1 − a − b − cN − l
```

**5 미지수 → 4 좌표**. 관측(평탄역 길이·용량)이 **차이**라 평행이동이 안 보이면
**5 → 3**. 따라오는 정확한 null 2차원:

```
n₁ = ( −N ,  0 ,  0 , +1 , −1 )   ⟺  {LAM_Ne,Li=δ, LLI=l} ≡ {LAM_Ne,De=δ, LLI=l+Nδ}
n₂ = ( +1 , −1 , +1 ,  0 ,  0 )   ⟺  LAM_Pe 를 li→de 로 ε 옮기고 LLI 를 ε 줄이면 불변
```

`[재현]` 두 방향 모두 세 관측과 원전 식 (8) 의 **총용량을 정확히 불변**으로
둔다 (수치 확인).

> **★ 2026-09-04 — `n₁` 을 우리 셀에서 시뮬로 시험했다. 구조는 맞고 계수가 틀렸다.**
> `{LAM_Ne,li = δ}` 와 `{LAM_Ne,de = δ, LLI = N·δ}` 를 PyBaMM 으로 실제 돌리니
> **평균 67.8 mV** 나 다르다 (δ = 0.12). 대조군이 방향을 뒤집는다 — **보정을 안 한
> 쪽이 가장 가깝고**(0.254 mV) 보정을 키울수록 단조롭게 나빠진다.
> `[해석]` **계수는 로딩비 `N` 이 아니다.** `li` 가 `de` 보다 더 빼는 리튬은
> **재료가 제거되는 프레임에서 그 재료가 쥐고 있던 양**이고, 우리 파이프라인은
> 열화를 **완방 프레임**에서 적용하는데 그 프레임에서 음극은 거의 비어 있다
> (`z_gr` = 0.001277). 올바른 계수로 재면 `N·δ` 의 **1/298** 이고, 그 값으로
> 다시 재면 **평균 0.048 mV** — 0 과 구별되지 않는다.
> **계보에 대한 지적**: Dubarry 식 (8') 의 `LR` 은 **재료가 완전 리튬화 상태에서
> 제거된다**는 암묵 가정 위에 있다. **프레임을 적지 않고 계수만 인쇄하면
> 불완전하다** — 프레임이 다르면 계수가 300배 틀린다. 그 축퇴를 진술한 세 편
> (Dubarry · Birkl · Marongiu) 중 **프레임을 명시한 편은 없다.**
> **★ 그리고 `n₂`(PE)가 그 이론을 확증했다.** 프레임 이론은 반증 가능한 예측을
> 낳는다 — 완방에서 양극은 거의 차 있으므로(`y₀ = 0.926088`) PE 계수는 **0.9977**
> 이어야 한다(NE 는 ~0 이었다). 시험 결과 **맞았고, 인쇄된 계수 1 보다 2~7배 더
> 잘 맞는다** (ε=0.04 에서 평균 \|ΔV\| **0.008 mV** vs 계수 1 의 0.054 mV;
> 보정 없음은 19.653 mV). **두 전극이 정반대이고 그 차이를 프레임 점유율이
> 정확히 예언한다.** 덤으로 `ε ≥ 0.08` 에서 보정 없는 짝은 **infeasible** 이다
> (줄어든 PE 가 완방 재고를 수용 못 한다) — `n₂` 는 선택이 아니라 **필연**이다.
> 정본 `mode-observability/results/phase1m/` · `docs/PHASE1M_NOTES.md`.

**이것이 세 원전을 하나로 묶는다:**
- `n₁` 은 [[dubarry-mechanistic-mode-synthesis]] 의
  `{LAM_liNE = x} ≡ {LAM_deNE = x, LLI = LR·x}` 와 **같은 방향**이다.
  ~~계수가 로딩비 `LR = N` 임을 식으로 확인해 준다.~~ → **2026-09-04 정정**:
  방향은 맞지만 **계수는 로딩비가 아니다.** 그것은 재료가 제거되는 **프레임**이
  정한다 (위 Phase 1m 배너). Marongiu 의 유도는 완전 리튬화 제거를 암묵 가정한다.
- `n₁`·`n₂` 는 [[birkl-ocv-degradation-diagnostic]] §4.2 가 산문으로 진술한
  두 축퇴(`pure-LLI + LAM_de ↔ LAM_li`, "the same holds true for … LAM_PE")다.
- **Birkl 의 3-파라미터 좌표 `[total-LLI, LAM_PE, LAM_NE]` 는 정확히
  `ℝ⁵/span{n₁,n₂}` 다** (`[재현]` 두 방향을 그 세 좌표에 넣으면 전부 0).
  5 − 2 = 3. 산문으로 쓴 것과 식으로 쓴 것이 같은 대상이었다.

## 결론

1. **창 좌표 4개는 공통이고, 계보를 가르는 것은 매개화와 여분 처리다.**
2. **모드 층을 만드는 순간 최소 1차원(관측이 차이면 2차원)의 정확한 축퇴가
   구조적으로 생긴다.** Birkl 은 등식으로, Marongiu 는 0-고정으로 죽인다.
3. **우리·Navidi·Rhyu 는 그 층을 만들지 않으므로 이 축퇴를 물려받지 않는다.**
   대신 우리 출력은 처음부터 **몫공간의 값**이며, [[22p-physics-or-degeneracy]]
   가 묻는 것은 **그 몫공간 안에서의 축퇴**다. **두 층을 섞으면 안 된다.**
4. `[해석]` 따라서 "우리가 본 degeneracy 의 일부가 좌표 선택에서 온다" 는
   가설은 **모드→창 층에서는 기각**된다 (그 층이 우리에겐 없다). 남는 것은
   창→관측 층이고, Phase 1d 가 그것을 쟀다.

## 불확실성

- Marongiu 의 `N = Q_Ne,BOL` 은 원전에 **수치가 없다** (`[인쇄]` "normally
  bigger than one" 뿐). 우리 셀에서는 셀 기하로 계산할 수 있고 **N = 0.6785** 다 —
  `[해석]` **1보다 작다.** 우리 셀이 음극 제한이라 그 자체는 모순이 아니지만,
  Marongiu 의 LFP 와는 다른 영역이라는 뜻이다.
  그리고 **`n₁` 의 계수는 `N` 이 아니다** (2026-09-04 Phase 1m — 위 배너).
- ~~Mohtat 2019 행은 원전을 읽지 않았다 — Lin 의 서술을 옮긴 것이다.~~
  → **2026-09-04 원전으로 닫았다** (*J. Power Sources* **427**, 101–111).
  **Lin 이 전한 쪽이 Mohtat 자신의 표기다**: `[인쇄]` 문제 (P) 가
  `θ = [x₁₀₀, y₁₀₀, C_n, C_p]` 를 최소화 대상으로 두고 `subject to,
  U_p(y₁₀₀) − U_n(x₁₀₀) = V_max` **하나만** 건다. 최소 전압 등식은 제약이 아니고
  — `[인쇄]` "the capacity is not included in the above formulation. Hence, **only
  the maximum voltage limit is used in the estimation problem**" — 셀 용량은
  추정 후 식 (27) 로 따로 푼다. 구현본의 "5 − 2" 는 **같은 문제의 다른 장부**이고
  둘 다 Ah 축 자유도 3 이다.
  **정정 하나**: 이 표가 그 4개를 "전극 SOC 한계 4개" 로 적어 온 것은 부정확했다 —
  SOC 한계는 **2개**(`x₁₀₀, y₁₀₀`)이고 나머지 둘은 **전극 용량**(`C_n, C_p`, Ah)이다.
  개수와 자유도는 맞았고 **구성이 틀렸다.**
- **Mohtat 행은 이 표의 축을 하나 벗어난다.** 이 표의 "여분 처리" 세 갈래(등식 /
  0-고정 / 안 만들기)는 전부 **파라미터 쪽** 처방인데, 그의 실제 기여는 **관측 쪽**이다
  — 전압에 **셀 팽창**을 둘째 채널로 더한다 (`expansion` 87회). 그래서 표의
  "관측" 열에만 그 사실을 적고, 처방 분류에는 넣지 않았다.
  기계와 판정은 [[constrained-crb-identifiability]] 에 있다.
- 위 null 계산은 **모델의 성질**이지 데이터의 성질이 아니다. 반쪽전지 곡선이
  노화에 불변이라는 가정 위에 있고, 그 가정은 Marongiu 자신이 LFP 에 대해
  다른 논문을 기각하는 근거로 쓴 것이기도 하다 (raw digest §10 ④).
- 우리 수치(σ3/σ1 등)의 정본은 `mode-observability/results/phase1d/` 이고
  이 페이지의 값은 사본이다 ([[provenance-fail-closed-verification]]).

## 관련
- [[fitting-degeneracy]]
- [[np-lip-ocv-reparametrization]]
- [[birkl-ocv-degradation-diagnostic]]
- [[dubarry-mechanistic-mode-synthesis]]
- [[nullspace-coefficient-interpretation]]
- [[22p-physics-or-degeneracy]]
