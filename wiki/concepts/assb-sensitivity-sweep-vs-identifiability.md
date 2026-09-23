---
title: "ASSB 모델 논문의 '민감도 분석' — OAT 스윕은 야코비안의 열이고, 겹쳐 보면 비식별 방향이 보인다"
description: "In the ASSB modelling literature 'sensitivity analysis' means one-at-a-time parameter sweeps of a forward model against design KPIs, not identifiability analysis; when a paper prints both a parameter fit and such sweeps, overlaying the sweep figures exposes parallel or null Jacobian columns, and the first such paper shows a fitted parameter that drifted ten orders of magnitude along a direction its own sweep had found flat"
created: 2026-09-23
updated: 2026-09-23
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/iwakiri2024_new-ssb-model-parameter-estimation-sensitivity.md, raw/papers/zhou2025_tailored-cathode-microstructure-low-pressure-assb.md, raw/papers/stavola2023_lithiation-gradients-tortuosity-thick-nmc111-argyrodite.md, raw/papers/vadhva2021_eis-for-assb-theory-methods.md]
confidence: low
explored: false
verificationStatus: unverified
claimType: interpretive
evidenceScope: single-source
---

# ASSB 모델 논문의 "민감도 분석" — 스윕 ≠ 식별성

> `assb` 축의 개념 페이지. 닻은 [[assb-contact-loss-vs-lampe]] 의 **Q4(유일성·식별성)**.
> 이론 쪽 정의는 [[constrained-crb-identifiability]] · [[fitting-degeneracy]] 에 있고, 이 페이지는 **ASSB 문헌에서 그 낱말이 실제로 무엇을 가리키는가**와
> **그 그림들을 공짜로 식별성 검사에 쓰는 법**을 다룬다. 수치의 정본은 원문 PDF 이고 여기 값은 **사본**이다.

## 정의 — 세 가지 "민감도"를 가른다

| 이름 | 무엇을 흔드나 | 출력 | 식별성을 말하나 |
|---|---|---|---|
| **설계 민감도** (design) | 물질 파라미터 한 개를 대역 배수(×0.1–×500)로 | 방전곡선 · KPI(용량 이용률 · 전압 효율) | **아니다** — "무엇을 올리면 좋아지나" |
| **추정 민감도** (estimation) | 적합점 근방에서 파라미터를 국소로 | **추정 데이터 위의** 잔차/출력의 야코비안 `J` | 절반 — `J` 의 열이 평행하거나 0 이면 비식별 **후보** |
| **식별성** | `J^T J`(FIM) · 조건수 · 프로파일 가능도 · 근최적 폭 | 추정 불확실성 · 조합의 null 방향 | **예** |

`[해석]` 26호(Iwakiri 2024, `raw/papers/iwakiri2024_new-ssb-model-parameter-estimation-sensitivity.md`)의 제목 "sensitivity analysis" 는 **첫 줄**이다.
그 편의 Table 1(ASSB 모델 10 편 비교)에서 "Sensitivity Analysis" 열의 값이 **Several / Temperature / Current / Diffusion / Conductivity** — **무엇을 스윕했나의 목록**이다.
⇒ 이 문헌에서 "sensitivity analysis" 를 보면 **스윕**으로 읽고, 식별성의 증거로 세지 않는다. (근거 한 편의 표 하나 — `single-source`.)

## ★★★★ 그래도 스윕 그림은 공짜 야코비안이다 — 겹쳐 본다

대역 스윕 곡선은 국소 미분이 아니지만, **한 파라미터를 흔든 곡선족의 "모양"** 은 그 파라미터의 민감도 방향을 보여 준다. 그래서:

1. **같은 모양의 그림 쌍 = 평행한 열** — 두 파라미터를 데이터가 한 조합으로만 본다(후보).
2. **반응 없는 그림 = 0 열** — 그 파라미터는 그 출력으로 정해지지 않는다(적어도 그 영역에서).
3. **그 파라미터를 적합표에서 찾아 문헌값과의 비를 본다** — 0 열 파라미터의 적합값은 **아무 데나** 갈 수 있다.

### 26호에서 실제로 나온 것

| 겹친 그림 | 모양 | `[재현]` 구조 | 적합표 |
|---|---|---|---|
| Fig. 5a (`D_e⁻` ×0.1–500) | **0 열** — 네 곡선이 확대창에서도 일치 | 식 (30) `D_p = 2D_M⊕D_e⁻/(D_M⊕+D_e⁻)` 가 `D_e⁻ ≫ D_M⊕` 에서 포화 → **하한만 식별** | ★ `D_e⁻` 최적 **5.24×10⁻³** ↔ 문헌 5.06×10⁻¹³ (**10 자릿수**) |
| Fig. 12a ↔ 12b (`k₁` ↔ `k₂`) | **평행** — 두 판 판별 불가 | `α` = 0.5 두 계면 모두 `asinh(i/2i₀)`, `i₀⁻` SOC 무관 → 몸통에서 합만 | 둘 다 ≈×1.05 |
| Fig. 3 ↔ Fig. 15 (`D_M⊕` ↔ `a_max`, 전류 고정) | **동일 곡선족**(끝 `x` 11 개 일치) | `x` 좌표에서 양극 부분계가 `D_M⊕·a_max/I` 한 조합만 본다(`I⁺₀ ∝ a_max` 만 깬다) | 둘 다 ×1.05 |
| Fig. 6 · 8 · 14 · 16 (전해질 셋 · `a_max`@C 고정) + 12 | **평행 이동 일곱 개** | 몸통의 평탄한 과전압 — 율 사이 곡률(옴 ↔ asinh)만 가른다 | 7/10 이 정확히 문헌 ×1.0500 |

★★★★ **첫 줄이 이 페이지의 이유다**: 26호는 `D_e⁻` 가 곡선을 안 움직인다는 것을 **자기 그림으로 보였고**, 그 파라미터를 **10 자릿수 표류한 값으로 보고**했으며,
그 점에서 본 둔감을 **"느린 종이 지배한다" 는 물리**로 결론에 올렸다. `[재현]` 문헌값이었다면 `D_e⁻` ×0.1 은 `D_p` 를 ×0.365 로 떨어뜨려 곡선이 크게 움직였어야 한다 —
**그림은 적합점에서 그려졌고, 그 둔감은 적합점의 성질이다.**

## 왜 중요한가 — Q4 의 0 과 이 페이지의 관계

- 카드의 Q4 는 **"유일성·식별성을 쟀나"** 다. 스윕은 재지 않은 것이다 — **26호 이후에도 Q4 는 0/26.**
- 그러나 26호는 **추정과 스윕이 같은 모델 · 같은 지면**에 있는 계보 첫 편이라, **원전 수치만으로 비식별을 재현할 수 있었다.** 24호(열일곱 번째 성질)의 재료가
  "측정 ÷ 가정"([[assb-tortuosity-factor-effective-conductivity-split]]), 25호(열여덟 번째)가 "손잡이의 폭" 이었다면 26호의 재료는 **저자 자신의 계산**이다.
- 큐 26(P2D 유효성, Sobol 29 회 · `identifiab` 0 회)은 **둘째 줄 너머(전역 분산 분해)**를 할 것으로 보인다(낱말 지문). 그래도 **Sobol 지수는 분산 기여이지 조합의 null 방향이 아니다** —
  이 페이지의 표로 분류한다. 큐 27(Bizeray 2019, 액체셀 SPM)이 **셋째 줄**의 원전이다.

## 우리 쪽 연결

- `degradation-degeneracy/` 는 **"곡선이 맞는다 ≠ 파라미터가 맞다"** 를 합성 truth 로 채점하는 프로젝트다. 26호의 "RMSD 0.11 → 0.06 V + 문헌과 5 % 이내" 는 그 실패 모드를
  검사하지 않은 검증의 **야생 표본**이고, `D_e⁻` 가 그 실패의 실례다. (우리 쪽 수치는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본 — 여기 옮기지 않는다.)
- 폭 측정기([[near-optimal-set-width-measurement]])를 26호 모델에 걸면 `D_e⁻` 는 **한쪽이 열린 구간**으로 나와야 한다(`[추론]`, 코드 비공개라 미실행).

## 처방 (논문을 읽을 때)

1. 제목·표의 "sensitivity analysis" 를 보면 **위 표의 어느 줄인지** 먼저 적는다(`Fisher`·`Hessian`·`profile`·`confidence`·`identifiab` 지문).
2. 추정 논문이 스윕도 인쇄했으면 **스윕 그림끼리 겹친다** — 평행 · 0 열을 찾는다.
3. 0 열 · 평행 열 파라미터의 **적합값 ÷ 문헌값**을 본다. 여러 좌표가 **같은 비율**이면 시작점 근방 정지 신호(26호 7/10 이 ×1.0500)다.
4. 스윕이 **추정 데이터의 조건**(율 · 온도)에서 돌았는지 본다 — 26호는 1C(추정 데이터에 없음)에서 돌렸다.

## 이 페이지가 주장하지 않는 것

- **대역 스윕이 국소 야코비안이라고 하지 않는다** — 모양 판독은 방향의 **후보**를 주고, 폭·조건수는 주지 않는다.
- **26호의 세 방향이 4 율 동시 적합에서도 전부 비식별이라고 하지 않는다** — 고율 곡선의 asinh 곡률(`[재현]` `i/2i₀` 1.9–2.3 @6C)이 `k` 쪽을 부분적으로 가를 수 있다. 확정된 것은 `D_e⁻` 의 한쪽 비식별(식 30의 극한) 하나다.
- **"sensitivity = sweep" 이 ASSB 문헌 전체의 관행이라고 하지 않는다** — 26호 Table 1 한 표 근거다.

## 관련

- [[assb-contact-loss-vs-lampe]] — 닻(Q4).
- [[constrained-crb-identifiability]] — 셋째 줄의 이론. "민감도 ≠ 식별성" 의 원래 자리.
- [[fitting-degeneracy]] — flat valley 의 일반형.
- [[near-optimal-set-width-measurement]] — 폭을 재는 기계.
- [[assb-lampe-contact-product-degeneracy]] — 곱 축퇴 처방 표. 26호가 **열 번째 적용**이고, 이 페이지의 처방 2·3 이 그 표의 "`J^T J` 최소 고유벡터" 줄의 **공짜판**이다.
- [[assb-tortuosity-factor-effective-conductivity-split]] — 24호, Q4 열일곱 번째 성질의 재료.
