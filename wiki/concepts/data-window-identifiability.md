---
title: 관측 창(data window)이 정하는 식별 가능성
created: 2026-09-04
updated: 2026-09-04
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/lee2020_estimation-error-bound-limited-data-window.md, raw/papers/mohtat2019_electrode-soh-estimability-expansion.md, raw/papers/marongiu2016_lfp-onboard-capacity-halfcell.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: theoretical
evidenceScope: multi-source-primary
---

# 관측 창(data window)이 정하는 식별 가능성

## 정의

반쪽전지 OCV 적합에서 **어느 구간의 데이터를 썼는가**가 파라미터 추정
불확실성을 정하는 축. Lee et al. 2020 의 표기가 이 축의 표준형이다:

```
DW = [Q_s, Q_e]          Q = 완충 상태에서의 방전 Ah (coulomb counting)
DOD = Q / C              C = V_max·V_min 로 정의된 셀 용량
```

**전압 구간도 SOC 라벨도 아니고 DOD(전하 처리량) 구간**이다. 창은 **폭**과
**위치** 두 자유도를 가지며, 둘이 하는 일이 다르다.

`[인쇄, Lee 2020 §IV-B]` "It is found that **the half-cell potential slopes
(α and β) drive the identifiability of the electrode parameters**." — 즉 창이
식별 가능성을 정하는 경로는 **창 안에 어떤 반쪽전지 국소 기울기가
들어오는가**다. 감도행렬 `χ_ij = ∂V_oc(Q_i)/∂θ_j` 의 행은 창 안의 점들이므로,
창을 옮기면 **행 집합이 통째로 바뀐다** — 관측을 더하는 것도, 제약을 거는
것도 아닌 **세 번째 조작**이다.

## 무엇이 실측됐나

| 문헌 | 창의 좌표 | 인쇄된 판정 |
|---|---|---|
| **Lee et al. 2020** | `DW = [Q_s, Q_e]`, DOD | 창 전수 삼각지도(`Q_s × Q_e`, 0.5 % 간격). 처방: `[인쇄]` σ̂ = 10 mV·목표 10 %·95 % → **DOD = [0.35, 0.73]**. 상한 사례: DW-shallow `[0, 0.2]` 에서 제약 CRB 막대가 `C_n` **5e3 %** |
| **Mohtat et al. 2019** | DOD 폭 | `[인쇄]` "DOD required for observability is **reduced to 30 %**" (셀 팽창 관측을 더했을 때) |
| **Marongiu et al. 2016** | 차량에서 실제로 얻히는 부분 곡선 | 창이 좁을 때 **초기값만 바꿔 오차 6.38 → 14.46 %** (재지 않은 축퇴의 대가) |

## 세 가지 사실 (Lee 2020 에서)

1. **폭보다 위치가 셀 수 있다.** 같은 폭 40 % 인 두 창의 실측 오차
   `[인쇄, Table IV]`: medium `[0.3,0.7]` → `x₁₀₀` 4.9 % · `C_n` 14.5 %;
   non-full `[0.1,0.5]` → `x₁₀₀` 10.0 % · `C_n` 24.1 %. 반대로 PE 는 높은 SOC
   쪽(non-full)이 유리하다. **어느 전극이 보이는지를 창 위치가 고른다.**
2. **상전이 봉우리가 문턱이다.** dV/dQ 의 `P1`(graphite 상전이,
   `[인쇄]` DOD = 0.4)·`P2`(`[인쇄]` NE 전이는 DOD ≈ 0.7 부터) 를 창이 삼키는
   순간 막대가 계단식으로 떨어진다. `[인쇄]` "data taken from regions that
   include **phase transitions** … improve the identifiability."
3. **비단조가 있다.** `[도표, Fig. 5]` `y₁₀₀` 의 무제약 막대는 shallow
   `[0,0.2]` ≈ 14.2 % 인데 medium `[0.3,0.7]` 은 ≈ 25.1 % 로 **더 나쁘다** —
   창을 넓혀도 완충 근처를 버리면 PE 창 끝점이 뜬다. "창은 넓을수록 좋다" 는
   단조 직관이 깨지는 자리다.

## 왜 중요한가 (`[해석]`)

이 위키가 추적하는 처방은 지금까지 둘이었다
([[constrained-crb-identifiability]]):

| 조작 | `S = χ` 에 하는 일 | 예 |
|---|---|---|
| 제약 추가 | 열공간을 nullspace `U` 로 사영 (정보 불변) | 컷오프 전압 등식 |
| 관측 추가 | **행을 덧붙인다** (독립이면 정보 증가) | 셀 팽창 `Δt_c` |
| **창 이동** | **행을 갈아 끼운다** (같은 개수여도 다른 정보) | Lee 2020 DW |

셋째가 우리에게 특히 값싼 이유: **새 센서도 새 가정도 필요 없고 프로토콜만
바꾸면 된다.** 그리고 Lee 2020 은 창을 전수로 스캔하는 표현(삼각지도)을
이미 만들어 두었다 — 다만 그 지도는 **전극 파라미터 좌표**에 있고
**대각 성분만** 색칠한다. 같은 지도를 `(LLI, LAM_PE, LAM_NE)` 좌표에서,
**상관을 포함해** 그리는 것이 비어 있는 칸이다.

## 한계

- **국소·불편 전제**를 그대로 물려받는다. 막대가 `5e3 %` 로 나오는 창에서는
  선형화 자체가 무의미하고, Lee 2020 도 그 창에서는 MC 검증을 하지 않았다.
- **창은 공짜가 아니다.** 깊은 방전 창은 셀을 실제로 깊이 방전시켜야 얻어지며
  그 자체가 열화를 만든다 (`[인쇄, Lee 2020]` PHEV 하한이 30 % SOC 로 설계되는
  이유). 즉 이 축은 **식별 가능성 ↔ 사용 조건**의 교환이다.
- **열화된 셀에서 다시 재야 한다.** Lee 2020 의 지도는 fresh 공칭값 한 점에서
  그려졌다. `α`·`β` 가 놓이는 자리가 열화로 이동하면 지도도 이동한다.

## 관련
- [[constrained-crb-identifiability]] — 창 이동과 구분되는 두 처방(제약·관측)
- [[np-lip-ocv-reparametrization]] — 같은 창 좌표를 최소 매개화로 다시 쓴 계보
- [[birkl-ocv-degradation-diagnostic]] — 창 끝점을 컷오프 등식으로 죽이는 처방
- [[fitting-degeneracy]] — 창이 좁을 때 드러나는 축퇴 그 자체
- [[pvs-sev-lli-lampe-separability]] — "무엇을 더하면 갈리는가" 의 열린 질문
