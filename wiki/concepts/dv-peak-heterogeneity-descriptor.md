---
title: DV peak intensity — 흑연 리튬화 불균일성 descriptor
description: "dV/dQ 의 stage-II ridge 절대 높이를 셀 등급화·수명 예측에 쓰는 Kim 2023 의 descriptor, 그 정의·물리 귀속의 근거·PVS 와의 관계"
created: 2026-09-03
updated: 2026-09-03
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/kim2023_graphite-heterogeneity-lifetime.md, raw/papers/wang2025_interpretable-ml-battery-prognosis.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: single-source
---

# DV peak intensity — 흑연 리튬화 불균일성 descriptor

Kim, Kim, Kim, Choi, *ACS Energy Lett.* **2023**, 8, 2946−2953
(DOI 10.1021/acsenergylett.3c00695) 가 제안한, **첫 사이클 dV/dQ 곡선의 극값
하나**로 상용 셀의 수명을 예측·등급화하는 descriptor.
원문 해체분석은 `raw/papers/kim2023_graphite-heterogeneity-lifetime.md`.

## 정의 (★ 두 개를 혼동하지 않는다)

대상: **LFP‖graphite 원통형 셀(IFR18500, 공칭 1 Ah / 3.2 V)** 의 **충전**
`dV dQ⁻¹` vs 용량 곡선. 첫 RPT 의 **세 번째 0.2C 사이클**에서 뽑는다.

```
ΔPeak_S2 = dV/dQ|ridge(≈0.6 Ah)  −  dV/dQ|valley(≈0.4 Ah)   ← 진폭. 폐기됨
Peak_S2  = dV/dQ|ridge(≈0.6 Ah)                              ← 절대값. ★ 실제 사용
```

SI 의 인쇄 문장이 정본이다 — "**The Peak_S2 intensity is the absolute value at
the ridge.**"

**진폭 쪽은 저자들이 버렸다.** 이유는 물리가 아니라 측정 노이즈다: `[인쇄]`
"because of the **fluctuation in the valley** near 0.4 Ah, which is attributed
to the limited resolution of voltage detection when the voltage plateaued at
the transition from stage III to stage II." 그리고 버린 결과 상관이
**ρ 0.75 → 0.82 로 올랐다.**

미분 방식·평활화·격자·ridge 탐색 알고리즘은 본문과 SI 어디에도 없다.

## 물리 귀속과 그 근거

주장: `Peak_S2` 는 **흑연 음극으로의 Li 삽입의 공간적 불균일성**을 반영한다.
국소 SOC 가 분산되면 stage 전이가 용량축으로 번지고, 전압곡선의 계단이
완만해져 dV/dQ 의 ridge 가 낮아진다.

근거를 강한 순서로 (원전 §9.2):

| 근거 | 종류 | 한계 |
|---|---|---|
| 선행문헌 Lewerenz/Sauer 2017 (**LFP\|Gr 원통형**): "the sharpness of the peak on the DV profile reflects the homogeneity of Li intercalation in the Gr anode" | 인용 | **귀속의 실질적 출처**. 이 논문이 세운 것이 아니다 |
| 기구론 도식 (Fig. 1a–c) | 개념도 | 데이터가 아니다 |
| XRM 구조 상관: 진원도 오차 0.21 vs 0.64 mm, cathode overhang | 실측 **n = 2** | 재는 것이 **조립 기하**이지 리튬화 균질성이 아니다 |
| 운전조건 경향 (저온·고율 → descriptor 하락) | 실측, 조건당 1셀 | **모드 조합 변화와 구분 불가** |
| 해체 SEM/ToF-SIMS/DMC 색 | 실측 | 대상이 descriptor 실험군이 아니라 조건 비교군 |

**없는 것**: half-cell·3전극(어휘 0회), 전기화학 시뮬레이션(`simulat` 0회),
공간분해 Li 측정, **양극 기여의 검토**. 양극은 배제된 것이 아니라 **논의되지
않는다**.

## 성능과 대조군

| 모델 (univariate ridge regression) | test RMSE (cycles) | test MAPE (%) |
|---|---|---|
| Dummy regressor | 93 | 28.5 (4.8) |
| **Peak_S2 intensity** | **51** | **13.5 (2.4)** |
| Var(ΔQ₁₀₀₋₁₀(V)) — Severson 2019 | 60 | 15.6 (2.8) |
| first IR / first Q | 94 / 94 | 28.5 / 28.6 |

77셀, ρ(Peak_S2, cycle life) = **0.82**; ρ(1st capacity) = 0.14,
ρ(1st DCIR) = **0.01**.

**주의 두 가지**: (1) 원문은 Severson descriptor 대비 "significantly smaller"
라고 쓰지만 13.5 (2.4) vs 15.6 (2.8) 은 **각각의 표준편차 안에서 겹친다** —
유의성 검정 없음. 방어되는 주장은 "더 정확하다" 가 아니라 "**같은 정확도를
100 사이클이 아니라 첫 RPT 하나로**" 다. (2) 정답 축(cycle life)이 100 사이클
간격 용량점의 **다항 회귀 보간값**이고 그 오차가 보고되지 않는다.

## PVS 와의 관계 — 충돌이 아니라 다른 대상 (★)

[[pvs-sev-degradation-mode-features]] 의 PVS 와 이 descriptor 는 한동안
"같은 기하량에 다른 물리 귀속" 으로 위키에 기록돼 있었다. 원전을 읽은 결과
**전제가 거짓이다**:

1. **양이 다르다** — Peak_S2 는 valley 를 쓰지 않는다. PVS 는 peak−valley 를
   전압 간격으로 나눈 할선 기울기다.
2. **화학이 다르다** — LFP 는 2상 평탄 OCP 라 dV/dQ 기여가 미미하다. 즉 이
   논문의 음극 단일 귀속은 **그 화학에서 강제된 것**이고 NCM811 로 일반화되지
   않는다.
3. **좌표를 맞추면 오히려 일치한다** — `dQ/dV = 1/(dV/dQ)` 이므로 dV/dQ 의
   **ridge** ↔ dQ/dV 의 **valley**. Kim 의 Peak_S2 는 세미나의
   `Valley2`(graphite stage-2 단일상)와 같은 종류의 특징이며 **둘 다 음극
   귀속**이다. 세미나가 양극(NCM811 H1→M)에 붙이는 `Peak2`(dQ/dV 의 peak =
   dV/dQ 의 valley)는 이 논문이 **쓰지 않는** 쪽이다.
   (원문은 DV↔IC 대응을 논하지 않는다 — 이 항은 우리 해석이다. Q 축과 V 축의
   매개변수화가 다르므로 극값의 **존재**는 대응해도 폭·높이 스케일은 다르다.)

## 이 위키에서의 적용

- **[[pvs-sev-lli-lampe-separability]]**: 위 판정으로 "물리 귀속 충돌" Gap 을
  닫았다. 대신 **새 Gap** 을 열었다 — 원전 Fig. S2a 는 **같은 SOH 80 % 에서**
  사이클 조건에 따라 ΔPeak_S2 가 0.083 ~ 0.253 (약 3배) 로 갈리는 것을 보인다.
  DV/IC 극값 진폭이 **열화 모드 분율 이외의 상태변수**를 싣는다는 실측이며,
  PVS 를 모드 관측으로 쓰는 설계에 귀속 논쟁보다 무거운 위협이다.
- **[[mode-observability]]**: Phase 1 이 관측한 PVS 의 valley 정의 민감도에
  **문헌 전례**가 생겼다. 대조 관측으로 **valley 를 쓰지 않는 변형**(peak
  절대 높이)을 넣을 근거이며, 계산이 값싸다 (기존 곡선, 새 프로토콜 불필요).
- **[[degradation-degeneracy]] 가 이 논문에 공급할 수 있는 것**: Fig. S2a 의
  3배 변동 중 **열화 모드로 설명되는 몫의 상한**. 원전은 시뮬레이션을 한 번도
  돌리지 않으므로(`simulat` 0회) 스스로 할 수 없는 계산이다.
- [[interpretable-ml-battery-prognosis-taxonomy]] 의 §4.2 (IC/DV 유래 feature)
  분류에서 이 descriptor 가 대표 사례로 인용된다. **그 리뷰의 단어
  ("peak intensity") 는 정확하다** — 부정확했던 것은 리뷰 Fig. 5c 의 화살표를
  대표 descriptor 로 읽은 우리 쪽 추론이었다.

## 불확실성

- 물리 귀속의 실질적 출처는 Lewerenz/Sauer 2017 (*J. Power Sources* 368, 57)
  이며 **미확인**이다. "peak sharpness ↔ 흑연 균질성" 을 그 논문이 어떻게
  세웠는지 확인하기 전에는 귀속을 인용하지 않는다.
- 원전의 "불균일성" 해석과 "열화 모드 조합" 해석이 **데이터로 구분되지
  않는다**. 이 페이지의 표는 원전의 주장을 옮긴 것이지 검증한 것이 아니다.
- 원전 안에 표기 불일치가 3건 있다 (Peak_S4 vs ΔPeak_S4, SI 의 ridge/valley
  위치 서술, MPE vs MAPE). S4 계열 인용 시 주의.
- 식별 가능성·불확실성 어휘는 본문·SI 통틀어 **0회** (`identifiab` `uniqu`
  `degenerat` `collinear` `uncertain` `confidence` 각 0). 이 계보에서 네 편
  연속 같은 패턴이다.
