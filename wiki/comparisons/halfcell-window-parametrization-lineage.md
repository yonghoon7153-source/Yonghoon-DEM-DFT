---
title: 반쪽전지 창 매개화 계보 비교 (자유도와 제약)
description: "같은 4개 창 좌표를 무엇으로 매개화하고 여분을 어떻게 죽이는가 — Dubarry 2012 부터 우리 파이프라인까지"
created: 2026-09-03
updated: 2026-10-02
type: comparison
tags: [battery, degradation, research]
sources: [raw/papers/khalik2021_dfn-grouping-sensitivity-parameter-estimation.md, raw/papers/schmitt2022_sic-ocp-shape-change-degradation-modes.md, raw/papers/marongiu2016_lfp-onboard-capacity-halfcell.md, raw/papers/birkl2017_degradation-diagnostics-ocv.md, raw/papers/dubarry2012_synthesize-degradation-modes.md, raw/papers/lin2024_ocv-degradation-mode-identifiability.md, raw/papers/navidi2024_piml-degradation-diagnostics-comparison.md, raw/papers/rhyu2025_systematic-feature-design-formation.md, raw/papers/mohtat2019_electrode-soh-estimability-expansion.md, raw/papers/lee2020_estimation-error-bound-limited-data-window.md, raw/papers/wang2025_aging-induced-rate-independent-li-plating.md, raw/papers/cui2026_direct-diagnosis-lfp-degradation-modes.md, raw/transcripts/2026-09-14-bms-handoff-width-and-wiki-candidates.md, raw/papers/sun2025_dl-eis-degradation-mode-diagnostics.md]
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
| **[[data-window-identifiability]] (Lee 2020)** | `y₁₀₀, C_p, x₁₀₀, C_n` | **4** | **1** (`V_max` 등식 — 무제약/제약 **둘 다** 보고) | 소거하지 않고 **제약 CRB 로 대가를 잰다** | full-cell OCV, **DOD 구간 `[Q_s, Q_e]` 로 잘라서** |
| [[np-lip-ocv-reparametrization]] (Lin 2024) | `r_N/P`, `z₀⁺` | **2** | 0 | **재매개화로 애초에 안 만든다** | SOC 정규화 OCV **형상** |
| Navidi 2024 (부록 A1) | `m_p, δ_p, m_n, δ_n` | **4** | **0** | 여분 없음 (전단사) | full-cell 전압 곡선 |
| **Schmitt 2022 (2026-09-10 추가)** | `α_cat, β_cat, α_an, β_an` **+ `γ_Si`** | **5** | **0** (단 `β<0` 부호 제약) | **여분을 죽이지 않고 늘린다** — 다섯째는 창이 아니라 **반쪽전지 곡선의 모양**을 매개화 | full-cell C/30 충전 곡선의 **DV** |
| **Wang (Xiong) 2025 (2026-09-11 추가)** | `K_NE, K_PE, S_NE, S_PE` **+ 음극 구간별 `K_NE1..K_NE5`** | **8** | **0** | **여분을 늘린다 (+4)** — 음극 곡선을 DV 극값 4개로 5 구간으로 잘라 구간마다 가로 스케일 (구간 ⑤ = 0 V 이하 도금 구간). GA 적합, 검증은 RMSE < 10 mV 뿐 | full-cell 0.05 C 의사-OCV 충전 곡선 (LFP/graphite) |
| **Cui 2026 (2026-09-11 추가)** | `X1 = C_APE, X2 = C_ANE, X3 = LAM_liNE − LAM_dePE + LLI, X4`(방전 종료 음극 리튬화도) | **4** | **0** — 단 **재조합**: 7 물리량 → 4 (`[인쇄]` "To obtain unique parameter results, the variables in Eq. (1) need to be recombined") | **줄였다가 다시 늘린다** — 사전믿음 등식(입자 파괴 확률 균일 → 격리분 리튬화도 = 순환 구간 중점, 식 9)으로 4 → 7 (li/de 분할) | full-cell C/25 **방전** 의사-OCV (LFP/graphite 20 Ah) + 재료 라벨(코인셀·XRD) |
| **Sun (Xiong) 2025 (2026-10-02 추가)** | `p0, n0, Q_PE, Q_NE` **+ 상수 `R`** | **5** | **0** | 창 4 는 여분 없음 — 다섯째는 창이 아니라 **동역학 한 칸**(전 SOC · 전 노화에서 `IR` 일정). PSO(설정 미인쇄), 검증은 맞춤 RMSE 7.52 · 6.55 mV 뿐. 출력이 그대로 DNN 의 "ground truth" | **1–2 C 사이클 CC 충전 곡선**(pOCV 아님), 창 = 충전 시작 전압 → 4.2 V 컷오프 |
| [[fused-lasso-feature-design-framework]] SI S11 | `β_c, β_a, Q_rem, V_shift` | **4** | 0 | 여분 없음 | C/20 RPT 곡선 |
| **Khalik 2021 (2026-10-02 추가 · ⚠ 액체 DFN)** | `s_n,0%, s_n,100%, s_p,0%, s_p,100%` (+ Q 측정 · 전극 용량 = `3Q/Δs`) | **4** | **0** | 경우 1(셀 EMF 만): 음극 곡선(흑연)을 빌리고 양극을 `U_EMF + U_n` 으로 **정의** → 창 넷이 OCV 채널에서 **정의상 사라진다**(`[인쇄]` "the same EMF-SOC relation can be reached with any choice between 0 and 1") — 교환 전류의 SOC 모양(식 12b)으로만 추정 · 경우 2(분해 OCP): 측정 쌍을 셀 EMF 에 맞추는 창(방법 미인쇄 "minimized in some way") = 우리와 같은 연산 | 동적 전류 · 전압(DFN 적합) + 셀 EMF(측정법 미인쇄) |
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

## ★ 네 번째 축이 있다 — **관측 창의 위치** (2026-09-04, Lee 2020)

위 "여분을 죽이는 세 처방" 은 전부 **파라미터 쪽** 처방이다.
[[data-window-identifiability]] 는 파라미터를 그대로 두고 **관측 구간을 바꾼다** —
`DW = [Q_s, Q_e]`, `Q` 는 `[인쇄]` "the discharge Amp-hours from fully charged
state obtained by **coulomb counting**", `DOD = Q/C`.

`[인쇄]` **Table IV** — 같은 셀·같은 추정기, 창만 다르다:

| DW | 범위 (DOD) | 폭 | `y₁₀₀` | `C_p` | `x₁₀₀` | `C_n` |
|---|---|---:|---:|---:|---:|---:|
| Shallow | `[0.0, 0.2]` | 0.2 | 14.9 | 16.8 | 38.3 | 24.1 |
| **Medium** | `[0.3, 0.7]` | **0.4** | 0.1 | 0.4 | **4.9** | **14.5** |
| **Non-full** | `[0.1, 0.5]` | **0.4** | 0.2 | 0.9 | **10.0** | **24.1** |
| Deep | `[0.0, 0.9]` | 0.9 | 0.0 | 0.8 | 1.6 | 1.8 |

`[해석]` **★ 폭이 같은 두 줄을 나란히 보라.** medium 과 non-full 은 **둘 다 폭
0.4** 인데 NE 파라미터 오차가 **2배 가까이** 다르다 (`x₁₀₀` 4.9 vs 10.0,
`C_n` 14.5 vs 24.1). 곧 **"창은 넓을수록 좋다" 가 아니라 위치가 어느 전극을
보이게 하는지를 고른다.** 원전도 같은 말을 인쇄한다 — `[인쇄]` "the medium case
shows relatively smaller estimation errors especially for the negative electrode
parameters … because the utilization range of the electrode becomes more
informative as the DW gets closer to a deeper discharged area."

`[인쇄]` 그리고 **운용 처방을 수치로** 준다 — p.10(3385): "if the given voltage
error variance σ̂ = **10 mV** and the target error bound is within **10 %** at a
95 % confidence level, the OCV range of **DOD = [0.35, 0.73]** can be one possible
DW." `[해석]` [[constrained-crb-identifiability]] 의 Mohtat 은 **폭**만 준다
(DOD 30 %). 이 편은 **폭 + 위치**를 준다 (폭 38 %, 저 SOC 쪽으로 치우침).

**우리에게 뜻하는 것 (`[해석]`)**: 우리 격자는 창을 고정하고 모드만 흔든다.
이 축은 **우리가 아직 안 흔든 축**이고, Phase 1l 이 찾은 "전압이 못 보는 방향"
과 직교하는 값싼 대안이다 — 센서를 늘리지 않고 **자르는 구간만 바꾼다.**

> **경계 하나 (이 위키가 원문에서 확인).** 이 처방은 **`θ` 좌표의 오차막대**를
> 겨눈다. 식 (10)–(12) 로 `LLI/LAM` 사상을 인쇄해 놓고 **§III-A 이후 쓰지 않으므로**,
> 위 표를 "모드 오차가 창에 따라 이렇게 변한다" 로 읽으면 **틀린다.** 그 변환은
> 아직 아무도 하지 않았다 (`mode-identifiability-unmeasured-lineage` 반론 (g)).

## ★ 다섯 번째 축 — **반쪽전지 곡선 자체를 매개화한다** (2026-09-10, Schmitt 2022)

위 표의 모든 문헌은 창 좌표 `(α, β)` 를 어떻게 다루느냐로 갈렸다. 공통 전제는
**`U_an(·)`, `U_cat(·)` 라는 함수 자체는 고정**이라는 것이다
([[halfcell-ocp-shape-invariance]]).

Schmitt 2022 는 그 전제를 깬다. Si/graphite blend 음극에서 `[인쇄]`
**`γ_Si` = 9.52 % → 5.55 % (488 EFC)** 로 성분 비율이 바뀌면 곡선의 **모양**이
바뀌고, 아핀 변환으로는 표현할 수 없다. 처방은 `γ_Si` 를 **다섯 번째 자유
파라미터**로 두어 4개 정렬 파라미터와 **동시 최적화**하는 것이다.

`[해석]` **이것은 앞의 세 처방과 방향이 반대다.** 등식·사전믿음·재매개화는
전부 자유도를 **줄인다**. 이쪽은 **늘린다** — 줄여야 할 여분이 아니라
**모델이 표현하지 못하는 물리**가 문제였기 때문이다. 그리고 그 대가로 저자
스스로 인정한 새 축퇴가 생긴다 `[인쇄]`: "**both effects would lead to the same
results with regard to the full-cell OCV**" (`γ_Si ↓` 와 `α_an ↓`).
**저자는 그 축퇴를 재지 않았다** — Fig. 7 의 `γ_Si` 는 오차막대 없는 단일 점이다.

`[인쇄]` 재지 않은 대가의 크기 (486 EFC 셀): `α_an` 이 **1.027 ↔ 1.057** 로,
`α_cat` 이 **1.216 ↔ 1.174** 로 갈리는데 OCV 재구성 RMSE 는 **9.9 ↔ 8.2 mV**
밖에 차이나지 않는다. 심지어 "충전 종료를 제한하는 전극" 이라는 **정성적 결론이
뒤집힌다**. → 이 위키의 `mode-identifiability-unmeasured-lineage` 논지의
**야생 실측 두 번째 사례** (첫째는 Marongiu 의 초기값 민감도 6.38 → 14.46 %).

## ★ 여섯 번째 축 — **반쪽전지 곡선을 구간별로 매개화한다** (2026-09-11, Wang (Xiong) 2025)

Schmitt 가 곡선의 **성분 비**(`γ_Si`)를 열었다면, Wang (Xiong) 2025 는 곡선의
**구간 폭**을 연다. `[인쇄]` 음극 과방전 반쪽전지 곡선(0 V 이하 도금 구간 포함)을
DV 봉우리 4개에서 잘라 5 구간으로 나누고, 식 (4) 로 구간마다 다른 가로 스케일
`K_NEi` 를 두어 이어 붙인다: `θn = [K_NE1, K_NE2, K_NE3, K_NE4, K_NE5, K_PE, S_NE, S_PE]`
(식 5). 이유는 무율 리튬 도금이 만든 충전 말단 어깨를 아핀 변환이 못 맞추기 때문이다
(Fig. 4b; [[rate-independent-li-plating-signature]]).

`[해석]` 구조는 **구간별 아핀(piecewise-affine)** 이다 — 각 구간의 전위 값은 고정,
가로 폭만 자유. 새 관측(어깨)에 직접 묶이는 것은 구간 ⑤ 의 폭 하나뿐이고, `K_NE1–4`
는 종래 `K_NE` 하나가 하던 일을 넷이 나눠 갖는다 (합만 구속 → 서로 보상 가능). 검증은
RMSE 2.7–9.1 mV (Table 3) 뿐이며 `uniqu*`·`uncertaint*`·`identifiab*` 전부 **0회**.
**Schmitt 와 같은 방향(늘린다)이고, 같은 침묵이다.** 이 위키의 처방 후보는 반대다:
4-창 좌표에 **도금 구간 폭 1개**만 더한다 (concept 페이지 §적용).

같은 논문에서 이 표의 **관측 창 축(네 번째 축)** 의 야생 실례가 하나 나온다: 음극
0 V 교차점이 노화로 full-cell SOC `[도표]` 1.08 → 0.88 로 **창 밖에서 안으로**
들어오고, 그 경계에서 추정 `Q_NE` 가 계단처럼 떨어진다 (Fig. 11·12). Lee 2020 은
창을 **움직여** 전극 가시성을 바꿨고, 여기서는 **전극 창이 움직여** 들어온다.

## ★ 등식의 새 변종 — **사전믿음 등식으로 다시 가른다** (2026-09-11, Cui 2026)

"여분을 죽이는 세 가지" 의 첫째(등식)는 지금까지 **컷오프 전압 등식**(Birkl) 하나였다.
Cui 2026 은 등식을 **물리 사전믿음**에서 가져온다: `[인쇄]` "Assuming that the
probability of active particle fracture is equal under different lithiation conditions
… the lithiation ratio of the isolated portion after fracture is expected to be
approximately consistent with the average lithiation ratio of the active material during
cycling" → `x_crk = [min(x) + max(x)]/2` (식 9). 이 등식 하나로 OCV 가 못 가르는 li/de
분할을 닫고, `X3` 에서 LLI 를 떼어 낸다.

`[해석]` 순서가 특이하다: **먼저 줄이고**(7 물리량 → `X1–X4`, "unique parameter
results") **다시 늘린다**(사전믿음으로 → 7). 늘린 쪽의 결과는 구성이다 —
`LAM_liNE/LAM_NE ≈ 0.36` 은 순환 구간 `[0, 0.78]` 의 중점 0.39 다. 원문의 XRD 검증은
LAM_NE **총량**으로만 보정되므로 이 분할을 검증하지 못한다. 그리고 이 표의 **LFP 행
셋**(Marongiu · Wang (Xiong) · Cui)이 공유하는 구조가 하나 더 드러난다: 평탄 양극 때문에
양극 창 하단이 관측 창 밖이고, 그래서 `(X1, X3)` 곧 **LAM_PE ↔ LLI 가 `X1 − X3 = Q_EOC`
로만 구속**된다. Cui 에서는 재료 측정(코인셀·XRD)이 LAM_PE ≈ 0 을 확인해 줬기 때문에
해가 없었다 — [[ic-peak-area-direct-mode-readout-lfp]].

## ★ 일곱 번째 축 — **관측을 운용 전류 곡선으로 바꾸고 동역학을 상수 `R` 하나로 흡수한다** (2026-10-02, Sun (Xiong) 2025)

Sun, Xiong, Wang, Li, Sun 2025 (`raw/papers/sun2025_dl-eis-degradation-mode-diagnostics.md` §4) 의 라벨 맞춤은 창 좌표는
우리와 같은 넷(`p0, n0, Q_PE, Q_NE`)이고, 식 (2) `Ũ = E_PE(p) − E_NE(n) + IR` 로 **상수 저항 하나**를 더해 **1–2 C 사이클
CC 충전 곡선**에 직접 맞춘다 (반쪽전지 OCP 는 신품 1/20 C 코인셀 한 번). 이 표의 다른 행은 전부 준평형 곡선(pOCV ·
C/20 · C/30)을 쓴다.

`[해석]` 바뀌는 것은 둘이다 (둘 다 미측정 — 원문은 유일성 · 오차막대를 재지 않는다):

1. **관측 창이 노화와 함께 움직인다** — 창의 시작은 직전 방전이 끝난 전압에서의 충전 시작점(`[도표]` 신품 1 C ≈3.29 V ·
   노화 1 C ≈3.62 V · 2 C ≈3.75–3.79 V), 끝은 `IR` 을 품은 4.2 V 컷오프다. 네 번째 축(관측 창의 위치, Lee 2020)이
   **설계가 아니라 노화의 함수**가 된다.
2. **`R` 이 창 좌표와 같은 서명을 남길 수 있다** — `IR` 은 곡선 전체의 수직 이동이고, 양극 OCP 기울기가 창 안에서 완만하면
   `p0` 의 수평 이동과 거의 같은 잔차를 만든다 → **`R ↔ p0 ↔ LLI` 별칭.** 그리고 `(1,1,1)` 공통 모드를 닫는 유일한 정보인
   CC 창의 Ah 길이([[np-lip-ocv-reparametrization]] 2 자유도)도 `IR` 만큼 짧아진다 → 공통 모드 ↔ `R` 결합.

**가장 값싼 판정**: 봉인된 반쪽전지 OCP 로 식 (1)–(2) 를 1 C · 2 C 에서 계산해 5×5 `JᵀJ` 의 최소 특이벡터에 `R` 성분이
얼마나 실리는지 본다 (digest §17.4 실험 1, 미실행).

## ★ 여덟 번째 축 — **형상 가정이 OCV 채널의 창 정보량을 정한다** (2026-10-02, Khalik 2021 · ⚠ 액체 DFN 도구)

Khalik, Donkers, Sturm, Bergveld 2021 (`raw/papers/khalik2021_dfn-grouping-sensitivity-parameter-estimation.md` §(c)) 은
창 좌표 넷을 DFN 매개변수 추정의 식별 집합 안에 두고, 평형 모형을 두 가지로 짓는다 `[인쇄]`:

| | 경우 1 (분해 불가 — 셀 EMF 만) | 경우 2 (분해 가능) |
|---|---|---|
| 음극 곡선 | 문헌에서 빌림(흑연) | 분해 전극 측정 |
| 양극 곡선 | **정의** `U_p = U_EMF + U_n` | 분해 전극 측정 |
| 창 넷의 OCV 정보 | **0** — 어느 창이든 EMF 정확 일치 | 측정 쌍 ↔ 셀 EMF 잔차를 줄이는 창(방법 미인쇄) |
| 대가 (`[재현·벡터]` 그림 2) | 빌린 곡선의 형상 오차가 다른 전극 곡선으로 1:1 — `U_p` 에 +6 … +54 mV | 쌍 ↔ 셀 EMF 잔차 −9.5 … +13.5 mV |

`[해석]` 이 표의 다른 행은 전부 두 곡선의 **형상을 고정**하고 창으로 맞춘다 — 경우 2 가 그것이고 우리 α·β 도 그것이다.
경우 1 은 **한쪽 형상을 완전히 자유로 둔 극단**이다. [[np-lip-ocv-reparametrization]] 의 2 자유도 정리(형상 고정 → SOC
정규화 OCV 모양이 두 비를 정한다)와 짝지으면, 형상을 고정하면 OCV 가 창의 두 조합을 정하고 한쪽 형상을 풀면 0 조합을
정한다. 다섯 번째 축(Schmitt `γ_Si`)은 그 사이 — 형상을 한 매개변수만큼 연다. ⇒ **형상에 준 자유도만큼 OCV 채널의
창 정보가 줄어든다**는 방향이 같은 구조다(`γ_Si ↓` ↔ `α_an ↓` 같은 서명 — [[halfcell-ocp-shape-invariance]]).

창을 OCV 에서 못 얻은 대가가 이 편 그림에 있다(`[도표·벡터]`): 0 % 끝 둘(`s0,n` · `s0,p`)은 감도 순위 15–21 위라
추정에서 빠져 범위 가운데(β 0.5)에 고정되고, 100 % 끝 둘은 6 · 11–12 위로 추정된다 · 실셀 Cell 1(경우 1)의 22 개 다중
시작에서 창 넷 중 셋의 중앙값이 사전 범위 끝 · 합성 시험(같은 모형 · 무잡음)에 1.2 mV 모형 오차를 넣으면 `s_p,100%`
중앙값이 참 0.418 → 범위 하한 0.22. 이 표의 관측 열로 옮기면 — **창이 OCV 가 아니라 동적 전류 · 전압의 동역학 경로로만
보이는 첫 행**이다.

⚠ 셀 둘 · 회차 하나 · EMF 측정법 미인쇄 · 경우 2 의 창 맞춤 방법 미인쇄([23, 24, 26] 에 미룸) · 열화 0(신품). 우리 쪽 수치는 옮기지 않는다.

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

> **★ 2026-09-04 — Birkl 의 3-파라미터 판을 우리 셀에 실제로 얹었다 (Phase 1n).**
> 계수를 지어 넣지 않고 **규약 16가지를 전수**했다 (PE 방향 × NE 방향 × 식 (8)
> `+1` 의 위치). **4개 통과.**
> **① 원전 쪽 정정**: 우리 [[birkl-ocv-degradation-diagnostic]] 전사대로 풀면
> 근이 **있다**(`Δx_EoD = +1.0`). 다만 그 근은 PE 창을 **폭 2** 로 만들어 반쪽전지
> 표에 넣을 수 없다. 원인은 **식 (8) 의 `+1` 이 식 (10) 에 짝이 없는 비대칭**이고,
> `+1` 을 양쪽에 대칭으로 두면 두 창이 정확히 `[0,1]` 이 된다. `[해석]` 곧
> **조판된 (7)–(10) 에는 짝이 하나 빠져 있거나, 두 식이 서로 다른 기준점을 쓴다.**
> 방향 규약은 무죄다 — 한쪽만 뒤집으면 근이 아예 없고 양쪽 뒤집으면 거울상일 뿐이다.
> **② 축퇴에 관한 실측**: 그 매개화의 3-모드 Jacobian 에서 가장 안 보이는 방향은
> **(1,1,1) 에서 86.13°** 다. 우리 자유 창 좌표(10.56°)와 **정반대**이고, 심판으로
> 쓴 **실제 시뮬 Jacobian 은 11.36°** 다. `[해석]` **Birkl 의 장부로 이 셀을
> 진단하면 (1,1,1) 축퇴가 보이지 않는다** — 그가 §4.2 에서 축퇴를 산문으로만
> 말하고 정량하지 못한 이유의 **후보**다 (증명은 아니다: 그 논문이 이 매개화로
> 축퇴를 찾으려 시도했다는 증거가 우리 digest 에 없다).
> **③ 그러나 분할 판정이다 — 그가 이기는 축이 있다.** 열별로 시뮬과 대조하면
> Birkl 의 `LAM_PE` 열은 **cos +0.969** 로 거의 완벽하고, 같은 열에서 우리
> `modes_to_params` 는 **−0.492** 로 **반대로 움직인다**. `[해석]` 이 계보의
> 매개화들은 **서로 다른 축에서 서로를 이긴다** — "누가 맞았나" 가 아니라
> **"어느 축에서 맞았나"** 가 옳은 질문이다.
> **④ 이 실험이 스스로 신고한 것**: 두 매개화 **모두** 시뮬 Jacobian 과 열
> 상대오차 190~220 %(최적 배율을 빼도 잔차 97 %)이고, 이식 검산 문턱(60 mV)이
> 미분되는 신호(7.66 mV)보다 8배 컸다. 그러므로 ② 가 지지하는 것은
> **"u_min 이 (1,1,1) 근방인가" 라는 이분법뿐**이며 각도의 정확한 값은 아니다.
> 정본 `mode-observability/results/phase1n/` · `docs/PHASE1N_NOTES.md`.

## ★ 구현 계보의 함정 — 좌표를 바꿔 놓고 도함수에 `1/α` 를 안 붙인다 (2026-09-14)

계보의 모든 구현이 전극 좌표를 `sto = (x − β)/α` 로 바꾼다. `dV/dQ` 항을
**해석적으로** 쓰면 연쇄법칙의 `1/α` 가 따라와야 한다.

규진팀 `electrode_balancing_blend.m` 실물 (서브 브랜치가 원본 MATLAB 을 받아 확인):

```matlab
E_cell_model  = @(p, x) E_PE((x - p(2)) / p(1)) - E_NE_blend((x - p(4)) / p(3), p(5));
dv_cell_model = @(p, x) dv_PE((x - p(2)) / p(1)) - dv_NE_blend((x - p(4)) / p(3), p(5));
```

둘째 줄에 `1/p(1)` · `1/p(3)` 이 **없다**. 적합값에서 `α` 가 1.0~1.18 이므로
dV/dQ 항에 **7~15 % 계통 오차**다. 서브의 포팅도 모델을 고치지 않는 원칙에 따라
**일부러 똑같이** 옮겼다.

**`degradation-degeneracy` 에는 이 결함이 없다 — 오늘 실측으로 확인했다.**
본체는 도함수를 해석적으로 쓰지 않는다. `src/objective.py` 가 합성된 곡선을
셀 좌표로 **수치미분**하고 (`np.gradient(smooth(v), x)`), `src/curves.py`
`to_dvdq()` 도 같은 모양이다. 수치미분은 좌표변환을 **이미 통과한** 곡선을
미분하므로 `1/α` 가 자동으로 들어간다.

검증 (α = 0.80, 해석 도함수를 아는 매끈한 `f_ref` 로 대조):

| 대조 대상 | 최대 오차 |
|---|---:|
| `f'(sto)/α` — `1/α` 포함 (옳은 것) | 6.4e-06 |
| `f'(sto)` — `1/α` 누락 (규진팀 모양) | 7.9e-01 |

즉 본체의 `dvdq` 는 `1/α` 를 담고 있다. 이 항목은 **닫힌 신고**다.
`[해석]` 다만 이것이 말해 주는 것은 계보의 일반 교훈이다 — **해석 도함수를
직접 쓰는 구현은 이 자리를 반드시 확인해야 한다.** 원전들은 도함수 식을
인쇄하지 않으므로 논문만 읽어서는 이 결함이 안 보인다.

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
- **Birkl 식 (7)–(10) 의 `+1` 이 짝을 잃었는지, 우리 digest 의 전사가 그것을
  놓쳤는지 이 위키는 가르지 못한다.** Phase 1f 가 전사와 조판본이 부호·항까지
  일치함을 확인했으므로 **전사 오류일 가능성은 낮지만**, 조판본에 인쇄된 것이
  원저자의 의도인지는 별개 문제다. Phase 1n 이 보인 것은 **대칭 가족만 물리적
  창을 준다**는 것뿐이고, 대칭 두 갈래(`+1` 양쪽 / `+1` 없음)는 창이 완전히
  같아 **이 실험이 가르지 못한다.**
- **우리 쪽 도구에 대한 경고 (2026-09-04 Phase 1n).** `modes_to_params()` 로 지은
  Jacobian 은 세 열 모두 시뮬 참값과 **음의 상관**이다(LLI −0.120 · LAM_PE −0.492 ·
  LAM_NE −0.333). 이 함수는 `src/fitting.py` 가 **"진단·시험 전용, 'paper' 규약"**
  이라 못 박은 것이고 **production 경로에는 모드→창 사상이 없으므로** 위 결론 3·4
  는 흔들리지 않는다. 그러나 **창 대수로 지은 Phase 1g·1j·1k 의 절대 각도는 이
  사상을 통과한다** — 그 숫자들을 인용할 때 이 사실을 같이 적어야 한다.
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
- [[rate-independent-li-plating-signature]] — 여섯째 축의 원전 서명과 모드 회계
- [[ic-peak-area-direct-mode-readout-lfp]] — 사전믿음 등식과 LFP 의 `(X1, X3)` 축퇴
- [[piml-physics-injection-points]] — 일곱째 축의 원전(Sun (Xiong) 2025)에서 이 맞춤의 출력이 ML 정답(⑥)이 된다
- [[halfcell-ocp-shape-invariance]] — 여덟째 축(Khalik 2021 경우 1 ↔ 2)이 기대는 형상 가정과 그 잔차
