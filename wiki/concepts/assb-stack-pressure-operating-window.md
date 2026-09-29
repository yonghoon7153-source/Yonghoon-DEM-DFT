---
title: ASSB 스택 압력의 작동 창 — 아래는 접촉 손실, 위는 단락
description: "Stack pressure in ASSBs is a two-sided constraint: too low gives interfacial contact loss, too high drives Li creep into electrolyte pores and shorts the cell. Doux 2020 gives the first measured pressure sweeps (P→impedance, P→time-to-short, P→overpotential) and a hard upper bound"
created: 2026-09-16
updated: 2026-09-29
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/wang2024_fast-kinetics-hierarchical-catholyte-anode-design-ssb.md, raw/papers/xu2024_pressure-effects-countermeasures-ssb-review.md, raw/papers/okasinski2020_edxrd-profiling-coin-cell-uneven-compression-lateral-gradients.md, raw/papers/minnmann2021_charge-transport-bottlenecks-tlm-ncm622-lpscl.md, raw/papers/nam2018_dry-vs-slurry-mixed-electrodes-binder-gitt-coverage.md, raw/papers/zhang2017_interfacial-eis-cathode-composition-lco-lgps-assb.md, raw/papers/zhang2017_in-situ-pressure-electrochemical-expansion-assb.md, raw/papers/masias2019_elastic-plastic-creep-mechanical-properties-lithium-metal.md, raw/papers/zhang2025_pressure-free-si-li21si5-double-layer-anode-assb.md, raw/papers/li2025_stack-pressure-critical-importance-perspective.md, raw/papers/oh2025_mgsigr-overcharge-low-np-ratio-low-pressure-assb.md, raw/papers/sakka2022_pressure-3d-structure-composite-cathode-xct.md, raw/papers/doux2020_stack-pressure-room-temperature-assb-li-metal.md, raw/papers/zhang2025_low-pressure-assb-challenges-strategies-review.md, raw/papers/shi2020_mechanical-degradation-assb-cathode.md, raw/papers/lee2020_ag-c-anode-free-assb.md, raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md, raw/papers/li2026_safety-aware-bms-active-intelligence.md, raw/papers/vadhva2021_eis-for-assb-theory-methods.md, raw/papers/zheng2026_assb-grid-realistic-appraisal.md, raw/papers/oh2025_maxwell-protocol-nondestructive-assb-health.md, raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md, raw/papers/yanev2024_li-in-alloy-anode-kinetic-limitations.md, raw/papers/fukunishi2023_ncm523-three-electrode-impedance-degradation.md, raw/papers/zhou2025_tailored-cathode-microstructure-low-pressure-assb.md]
confidence: low
explored: false
verificationStatus: unverified
claimType: empirical
evidenceScope: multi-source-primary
---

# ASSB 스택 압력의 작동 창 — 아래는 접촉 손실, 위는 단락

> `assb` 축의 **네 번째** 개념 페이지다. 닻은 [[assb-contact-loss-vs-lampe]].
> 앞의 셋: [[composite-cathode-percolation-utilization]] (`θ_AM`) ·
> [[assb-apparent-capacity-decomposition]] (3 항 분해) ·
> [[assb-pressure-reapplication-separation-test]] (`P↑` 분리 연산자).
> 이 페이지는 **그 연산자에 상한을 붙인다.**
>
> 수치의 정본은 원문 PDF 이고 여기 값은 **사본**이다 — 인용 근거로 쓰지 않는다.
> **모집단**: Doux 2020 = Li 금속 / Li₆PS₅Cl 냉간압착 펠릿(상대밀도 ≈82 %) /
> 대칭셀 **75 µA cm⁻²** / 상온 / **조건당 셀 1 개**. 다른 전해질·전류밀도로
> 옮기면 숫자가 그대로 가지 않는다.
>
> **2026-09-16 갱신 (`assb` 6호 Lee 2020 — 첫 무음극·첫 Ah 급 파우치)**:
> ★★★ **압력이 하나의 축이 아니다.** 아래 §"제작 압력 ↔ 운전 압력" 을 먼저 읽는다.
> 이 페이지의 Doux 수치는 전부 **운전 압력**이고, Lee 는 **제작 압력 490 MPa** 를
> 쓰면서 **운전 압력은 2 MPa** 로 내리고 심지어 **0 으로도 돌린다.**

## ⚠ 2026-09-22 (`assb` 8호 Li et al. 2026, **Mini Review**) — 창 **전체가 산업 요구치 위**에 있다

> ⚠⚠ **재인용이다.** 8호는 1 차 측정이 0 인 종설이고, 아래 값은 그 안의 재인용이다.
> **설계 입력으로 쓰기 전에 원전(Xu 2024)을 받아야 한다.**
>
> ✅ **2026-09-29 (81호 Xu 2024 = 8호가 가리킨 원문, 3차 묶음 파일 43)**: 값은 원문에 있다 — `[인쇄]` 초록 "far exceed the current industrial requirement **(< 1 MPa)**" —
> 그러나 **인용 0 · 본문 재진술 0 · 제조사 · 셀 형식 · 조건 0**("approximately" 는 8호가 더한 말). 8호의 인용은 맞고, 가닥은 **출처 없는 초록 한 줄에서 끝난다**(아래 §81호).

`[인쇄]` §6.1: "Reviews emphasize that many laboratory solid-state cells **still rely on
high external pressure**, whereas practical targets are moving toward **much lower
operating pressure**; **Xu et al. (2024) note industrial requirements below approximately
1 MPa**, and recent low-pressure reviews identify **pressure reduction as a central
commercialization problem** (Zhang et al., 2025)."

`[재현]` 8호 12 쪽 전수에서 `MPa` 는 **1 회**뿐이고 그 값이 **1** 이다.
이 페이지가 모은 실측과 나란히 놓으면:

| 출처 | 압력 | 역할 |
|---|---|---|
| 6호 Lee 2020 | **490 MPa** (WIP 등방) | 제작 — 계면을 만든다 (비가역) |
| 7호 Spencer-Jolly 2023 | 400 MPa (일축) | 제작 |
| 4호 Shi 2020 | **300 MPa** | 개입 — `θ_AM` 재가압 회복 |
| 5호 Doux 2020 | **75 MPa** 에서 도금 전 기계적 단락 | Li 금속 셀의 **위 벽** |
| 5호 (권고 운전) | 5 MPa (>1000 h 무단락) | 운전 |
| 6호·7호 (운전) | **2–4 MPa** | 운전 |
| **8호 (산업 요구치, 재인용)** | **< ≈1 MPa** | **위 전부보다 아래** |
| **★ 16호 Ramanayagam 2026** | **389 MPa 제작 = 389 MPa 운전**, 그리고 **97 MPa 운전** | **제작과 운전이 같은 첫 표본** (아래 §16호) |

★ `[해석]` **결과 둘**:
1. [[assb-pressure-reapplication-separation-test]] 의 `P↑` 연산자는 **산업 셀에서
   더더욱 쓸 수 없다** — 4호의 300 MPa 는 이 요구치의 **≈300 배**다.
2. 거꾸로 **`θ_AM` 의 시간 변화가 산업 조건에서 더 크고 더 빠를 것**이라는 방향이
   생긴다. 우리 분리 시험의 **운전 압력 기준점**은 실험실 값(2–5 MPa)이 아니라
   이쪽이어야 한다.

★★ 그리고 8호는 **압력을 BMS 상태변수로 올리자고 처음 제안한다**:
`[인쇄]` "stack pressure becomes a **coupled state/control variable**" ·
"A solid-state BMS may therefore need **pressure or force sensing**,
**pressure-dependent impedance models**, and diagnostics capable of **distinguishing
contact loss from ordinary electrochemical aging**."
→ `[해석]` 5호가 로드셀로 압력을 **실험실에서** 쟀다면, 8호는 그것을
**차량 안의 센서**로 올리자고 한다. ⚠ 구현·정확도·비용은 하나도 적혀 있지 않다.
⚠ Table 4 장기 실패 모드에 "**pressure/contact failure**" 가 올라 있지만 **측정법은 0**.

## 정의

ASSB 의 스택 압력 `P` 는 **한쪽으로만 좋은 변수가 아니다.** 두 방향으로 벌이 있다:

```
P 가 낮으면  →  계면 접촉이 안 되고 (음극 void · 양극 디본딩)  →  θ ↓ , R ↑
P 가 높으면  →  Li 가 항복강도(≈0.8 MPa)를 넘어 크리프하고
                 전해질 기공망을 따라 흘러 전자 경로를 만든다   →  단락
```

따라서 운전 가능한 구간은 **창(window)** 이고, 그 창의 두 벽은 **다른 물리**다:
아래 벽은 **접촉/이온 수송**, 위 벽은 **Li 소성 + 전해질 공극 퍼콜레이션**.

> ⚠ **2026-09-28 정정 (61호 Masias 2019 = 5호 ref 15, 항복 ≈0.8 MPa 의 원전)**: 위 도식의 "항복강도(≈0.8 MPa)를 **넘어** 크리프" 는 원전이 주지 않는다 —
> 원전은 creep 을 **항복 아래(0.2–0.6 MPa)** 에서 쟀고 거기서 `n` = 6.56 의 멱법칙이 나왔다(`[인쇄]` "studied at loads below the 0.8 MPa yield point"). 항복은 creep 의
> 문턱이 아니라 눈금 하나다: **creep 속도가 σ^6.56 로 커져 항복 근처에서 1 % 변형이 초 단위가 된다**(`[재현]` 0.2 MPa ≈14 h · 1 MPa ≈1 s). 위 벽의 "크리프 관통" 은
> 이 원전의 눈금으로 **power-law breakdown 영역(> 2.83 MPa)** 의 일이고, 원전의 압축 값(0.8–2.4 MPa)은 마찰 · 배럴링이 지배해 재료 법칙이 아니다(아래 §61호 · [[li-metal-yield-creep-vs-stack-pressure]]).

⚠ **이 창은 보편 상수가 아니다.** 위 벽은 `f(음극 재료, 전해질 공극률, 전류밀도)`
이고 아래 벽은 `f(표면 거칠기, 압착 이력)` 이다 — 아래 §"이력" 참조.

## 실측 — Doux et al. 2020 (`assb` 5호, UCSD / Y. S. Meng)

`raw/papers/doux2020_stack-pressure-room-temperature-assb-li-metal.md`.
**이 계보 최초의 압력 스윕**이다 (1–4 호는 압력이 0 회 또는 각 1 점).

### 위 벽 — 압력 → 단락까지의 시간 (Li 대칭셀, 75 µA cm⁻², 1 h/1 h)

| 스택 압력 | 단락까지 | 층위 | Li 항복강도(0.8 MPa) 대비 |
|---:|---:|---|---:|
| **75 MPa** | **0 h** (도금 전 **기계적** 단락) | `[인쇄]` | ≈94 × |
| **25 MPa** | **≈48 h** (전류가 있어야 죽는다) | `[인쇄]` | ≈31 × |
| **20 MPa** | **190 h** | `[인쇄]` | 25 × |
| **15 MPa** | **272 h** | `[인쇄]` | ≈19 × |
| **10 MPa** | **474 h** | `[인쇄]` | ≈13 × |
| **5 MPa** | **>1000 h**, 단락 없음 (중단) | `[인쇄]` | ≈6 × |
| (2 MPa) | **>163 h** — **SI Fig. S3 에만 있고 본문·Methods 에 없다** | `[도표]` | 2.5 × |

★ **기구가 둘로 갈린다**: 75 MPa 는 **전류 없이도** 죽고, 25 MPa 는 `[인쇄]`
무전류로는 죽지 않는다 → **(i) 순수 크리프 관통** vs **(ii) 크리프 씨앗 + 도금 성장**.
후자는 자기촉매다 — `[인쇄]` 돌기가 생기면 국소 과전압이 낮아 그 자리가 우선
도금 자리가 된다.

### 아래 벽 — 압력 → 임피던스 (Li | Li₆PS₅Cl | Li 대칭셀, Fig. 4c)

| 압력 | `[인쇄]` 값 | `[재현]` 25 MPa 바닥(32 Ω) 대비 계면 과잉 |
|---:|---:|---:|
| 1 MPa | **"exceeds 500 Ω"** (⚠ y 축 상한에 **잘림**) | >468 Ω |
| 5 MPa | ≈110 Ω | 78 Ω |
| 10 MPa | ≈50 Ω | 18 Ω |
| 15 MPa | ≈40 Ω | 8 Ω |
| 20 MPa | 35 Ω | 3 Ω |
| 25 MPa | 32 Ω | 0 (기준) |
| **5 MPa 로 되돌림** | **≈50 Ω** | **18 Ω** |

`[재현]` 같은 계의 DC 과전압(Fig. S4)에서 계면 ASR 을 뽑으면
**5 MPa ≈25 Ω cm² → 25 MPa ≈8 Ω cm²** (펠릿 벌크 ≈44 Ω cm² 를 뺀 뒤 2 로 나눈 값).

## 세 개의 결과 — 이것이 우리에게 하는 일

### 1. ★★ 정보는 **저압**에 있고, 위험은 **고압**에 있다
`[재현]` 계면 과잉이 15 MPa 에서 8 Ω, 20 MPa 에서 3 Ω 다 → **20 MPa 위로는 벌크가
전부**라 압력을 더 올려도 저항이 안 움직인다. 움직이는 것은 **수명뿐**이다.
`[해석]` **압력 축을 관측으로 쓸 때 고압 쪽은 정보가 없고 벌만 있다.**
[[near-optimal-set-width-measurement]] 에 압력 2 점을 넣는다면 **(5, 25) 가 아니라
(1–2, 10–15)** 가 정보량이 크다.

### 2. ★★ 이력 — `θ(P)` 는 함수가 아니라 **경로 의존 상태**다
처녀 5 MPa **110 Ω** ↔ 25 MPa 를 한 번 찍고 내려온 5 MPa **≈50 Ω**.
`[재현]` 계면 과잉의 **(78−18)/78 = 77 % 가 영구히 지워진다.**
`[인쇄]` 설명: 25 MPa 에서 Li 가 크리프해 거친 전해질 표면에 **정합**하고 계면
기공을 메운다 — 압력을 내려도 그 형상이 남는다.
→ **전방 모형에서 `θ_AM(P)` 을 단일값 함수로 쓰면 이력을 버리는 것이다.**
→ 압력 스윕 실험은 **스윕 방향과 이력을 반드시 기록**해야 한다.
(같은 뿌리의 경고가 [[assb-pressure-reapplication-separation-test]] 경고 3:
재가압은 일회성 조작이다.)

### 3. ★★★ `P↑` 분리 연산자에 **상한 파라미터가 붙는다**
[[assb-pressure-reapplication-separation-test]] 의 `ΔQ_mech ≡ Q(P_high) − Q(P_low)`
는 4호(Shi 2020)의 **300 MPa** 재가압 1 점에서 왔다. 5호는 **같은 황화물 계열
전해질 + Li 금속 음극**에서 **75 MPa 이면 도금 전에 이미 죽는다**고 실측한다 —
**4호가 쓴 압력의 1/4 이다.**

```
P_low  <  P_high  <  P_short(음극 재료, 전해질 공극률, 전류밀도)
```

⚠ **모집단이 다르다는 점을 반드시 붙인다**: 4호는 **In 금속 음극**(크리프 문턱이
Li 보다 훨씬 높다), 5호는 **Li 금속**. → **상한은 음극 재료의 함수**이고,
무음극·Li 금속 셀로 갈수록 **연산자를 쓸 수 있는 여지가 좁아진다.**

## 압력이 작용하는 **전극** — 4호의 귀속 문제를 가른다

★★ **Doux 의 Fig. 4c 셀에는 양극이 없다** (Li | SE | Li 대칭셀). 그런데 압력
1 → 25 MPa 에서 임피던스가 **>15 배** 움직인다.
→ **압력이 되돌리는 접촉의 큰 몫이 음극/전해질 계면에 있다는 것이 독립적으로 확인된다.**

이것이 [[assb-pressure-reapplication-separation-test]] **경고 2** 를 보강한다:
4호는 300 MPa 재가압 후 회복률이 `[도표]` **`R_LF`(음극) ≈65 % vs `R_MF`(양극)
≈23 %** 였는데도 초록·결론을 **양극 접촉 손실**로 돌렸다.
`[해석]` **두 논문을 합치면: `ΔQ_mech` 를 통째로 양극 `θ_AM` 회복으로 읽으면
과대평가다.** 분리 시험에 **전극 분해 관측**(3전극 또는 대칭셀 짝)이 필요하다.

## 이 창이 3 항 분해에 하는 일

[[assb-apparent-capacity-decomposition]] 의 `Q_apparent = θ_AM · η(i) · Q_material`
은 압력을 **`θ_AM` 에만** 들여놓았다. Doux 의 Fig. S4 는 **과전압 자체가 압력
함수**임을 보인다 (`[도표]` 5 MPa 7.0 mV ↔ 25 MPa 4.5 mV, 같은 전류밀도).

```
η = η(i, P)      ← 율만의 함수가 아니다
```

`[해석]` → **율 연산자와 압력 연산자가 직교하지 않는다.** `i→0` 으로 `η` 를
지우는 처방은 **압력을 고정한 채로만** 성립한다. 두 축을 같이 흔들면 `η` 와 `θ`
가 다시 섞인다.

## ★★★ 제작 압력 ↔ 운전 압력 — 6호(Lee 2020)가 쪼갠 축

`raw/papers/lee2020_ag-c-anode-free-assb.md`. **무음극 Ag–C / Li₆PS₅Cl / LZO-NMC(Ni 90)
6.8 mAh cm⁻² / 60 °C / 0.6 Ah 파우치 bi-cell.**

| | **5호 Doux** (Li 금속 펠릿) | **6호 Lee** (무음극 Ah 급 파우치) |
|---|---|---|
| **제작 압력** | 370 MPa(펠릿) / 25(Li) · 120(Li–In) MPa | **490 MPa 온간 등방압(WIP, Kobelco Sr. CIP)**, ⚠ `[인쇄]` **대기 중** |
| **운전 압력** | **1–75 MPa 스윕** (로드셀 실계측) | **2 / 3 / 4 MPa** (지그) **+ 무압 대조** |
| 운전 상한 | `[인쇄]` **75 MPa 도금 전 기계적 단락** | `[인쇄]` **">4 MPa 에서 단락 확률 증가"** ⚠ **데이터 0** |
| 저압에서 | 1 MPa → 임피던스 **>500 Ω** | `[도표]` **무압 0.1 C 가 2 MPa 와 구별 안 됨** |
| 압축의 가역성 | 임피던스 이력 (`[재현]` 계면 과잉의 77 % 영구 제거) | **두께 이력** — `[인쇄]` Table S2: 644.5 ± 2.9 → **609.0 ± 2.4 µm**, **7 일 무압에 609.8 ± 2.6** (복원 +0.8 µm, 산포 안) |

`[도표]` 6호 SI Fig. 11: 운전 압력 2/3/4 MPa 에서 율특성(1.0C/0.33C)이
**94.0 / 95.1 / 95.5 %** — 단조 증가하지만 **폭이 1.5 %p** 이고, 300 사이클 유지율
곡선 셋이 **겹친다**(≈94 %@300).
`[도표]` 6호 SI Fig. 12 (무압, 0.1C/0.1C): 충전 **≈235** · 방전 **≈217 mAh g⁻¹** —
2 MPa 셀(SI Fig. 7: ≈233 / ≈214)과 **사실상 같다.**
그리고 `[인쇄]` **5 Ah 10-적층 셀도 무압**으로 0.05 C 에서 5,870 mAh · 942 Wh l⁻¹.

★★★ `[해석]` **두 논문은 모순이 아니다.** Doux 의 셀은 **제작 압력이 낮아서**
운전 압력이 계면을 만들어야 했고, Lee 의 셀은 **490 MPa 가 이미 만들어 놓아서**
운전 압력이 **할 일이 남아 있지 않다.**

```
창의 아래 벽 위치  =  f(제작 압력 이력)        ← 6호가 추가한 의존성
창의 위 벽 위치    =  f(음극 재료, 전해질 공극률, 전류밀도, 셀 형상)
```

★★ **그리고 운전 축의 위 벽이 훨씬 낮다**: 4 MPa vs 75 MPa — **1/19**.
모집단이 다르지만(Ah 급 파우치 적층 ↔ 펠릿) 방향은 **무음극·대면적으로 갈수록
운전 압력 창이 좁아진다.**
→ **[[assb-pressure-reapplication-separation-test]] 의 `P↑` 연산자는 이 셀에 적용
불가**다: 4호가 쓴 **300 MPa 는 이 셀 운전 상한의 75 배**다.

⚠⚠ **단 6호의 상한은 주장이지 측정이 아니다.** `[인쇄]` "the probability of
short-circuiting increased upon application of high pressures exceeding 4 MPa" —
**4 MPa 초과 점이 본문·SI 어디에도 없고**, 단락 횟수도 셀 수도 없다 (6호 digest D3).

★ **좋은 소식 하나**: Table S2 의 **비가역 치밀화**는 5호가 임피던스로 준
`θ(P)` 이력(§"이력") 의 **독립 확인**이다 — 채널이 다르고(기하 vs 전기) 결론이 같다.
`[해석]` **압축은 상태에 영구히 남고, 그래서 제작 압력은 "한 번 치르는 비용" 이다.**

## ⚠ 2026-09-16 (`assb` 7호 Spencer-Jolly 2023) — 두 축 구조는 재현, **스윕은 후퇴**

`raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md` 도
압력이 **둘**이다 — 그리고 6호와 **같은 구조**다:

| | 제작 | 운전 |
|---|---|---|
| **6호 (Lee 2020)** | **490 MPa 등방 (WIP, 대기 중)** | 2 MPa 지그 (+2/3/4 스윕, 무압 대조) |
| **7호 (Spencer-Jolly 2023)** | **400 MPa 일축** (Li₆PS₅Cl 분말에 중간층을 압착) | **2 MPa 원뿔 스프링** |

→ ★ **독립 연구실에서 "제작 수백 MPa · 운전 2 MPa" 가 다시 나온다.** 이 자릿수
분리는 한 그룹의 관행이 아니라 **황화물 펠릿 계의 공통 설계점**으로 보인다.
⚠ **그러나 7호는 압력 축에서 아무것도 더 주지 않는다**: 스윕 **0** · 로드셀 계측
**0** · 무압 대조 **0** · 압력→용량 **0**. `pressure` 5 회 · `MPa` **2 회**뿐이다.
⚠ 그리고 **도금으로 스택이 두꺼워질 때 스프링이 눌리는데 그 변화가 보고되지 않는다**
— 6호 digest 의 **G12(정압인가 정변위인가)** 가 그대로 남는다. 7호는 `[인쇄]`
"**conical spring**" 이라고 적어 **정하중 쪽**임을 시사하지만 계측값이 없다.

`[해석]` **압력→용량 곡선은 `assb` 7/7 편이 여전히 0 이다.**

## ★★ 2026-09-22 (`assb` 10호 Vadhva 2021, **방법론 리뷰**) — 이력의 **독립 재현**과 **새 역할**

`raw/papers/vadhva2021_eis-for-assb-theory-methods.md` 는 압력을 **본체로 다루지
않는다** (`MPa` 본문 **2 회**). 그런데 재인용 두 자리가 이 페이지에 정확히 걸린다.

**(가) 이력(hysteresis)의 산화물 독립 재현.** Krauskopf 2019 (*ACS AMI* 11, 14463)
의 Li|LLZO|Li 대칭셀에 대해 `[인쇄]`:
> "with careful surface preparation and handling under inert gas to avoid Li₂CO₃
> formation, **sufficient applied pressure reduced the interfacial impedance to a
> negligible value (<1 Ω cm²)**, **which remained after the pressure was removed**."

`[해석]` 5호(Doux 2020)가 **황화물**에서 잡은 "처녀 5 MPa 110 Ω ↔ 25 MPa 를 찍고
내려온 5 MPa ≈50 Ω" 과 **같은 현상이 산화물에서 나온다.** 서로 다른 전해질 계·
다른 연구실이므로 **`θ(P)` 가 함수가 아니라 경로 의존 상태**라는 이 페이지의 결론
②가 **단일 출처에서 벗어난다.** ⚠ 단 10호는 **재인용**이고 원전(ref. 28)을 받아야
한다 — 이 페이지의 수치로 `<1 Ω cm²` 를 쓰지 않는다.

**(나) ★★★ 압력의 세 번째 역할: 관측 분해능 연산자.**
`[도표]` Fig. 11a (Krauskopf 재수록, Li|LLZO|Li, 축 Ω cm²): 저압에서는
**Bulk 원호(0 → ≈400)** 와 **Int 원호(≈400 → ≈950, 즉 `R_int` ≈550 Ω cm²)** 둘만
보인다. "Increasing force" 화살표를 따라 Int 가 줄고, **인셋의 400 MPa 에서는
`R_int` 가 사실상 사라지면서 그 뒤에 숨어 있던 `GB` 원호(≈410 → 437, 약 27 Ω cm²)가
드러난다.**

```
   저압:   [ Bulk ][      Int (거대)      ]        → 분해되는 RC 2 개
   400 MPa:[ Bulk ][GB]                           → 분해되는 RC 2 개, 그러나 GB 가 새로 보인다
```

`[해석]` **압력은 `θ_AM` 을 되돌릴 뿐 아니라 관측 가능한 시상수의 개수를 바꾼다.**
→ [[assb-pressure-reapplication-separation-test]] 의 `P↑` 연산자에 **두 번째 용법**이
붙는다: 큰 시상수를 지워서 **그 뒤의 것을 식별 가능하게 만든다.**
이것은 10호가 다른 곳에서 든 "저온으로 `R_gb` 를 벌려 동정한 뒤 실온 적합의 구속으로
되가져온다"(Bron 2016)와 **같은 조작의 압력 판**이고,
[[assb-lampe-contact-product-degeneracy]] 가 요구하는 "여기를 늘려 축퇴를 깬다" 의
실물 사례다.

**(다) ⚠ 상한은 여전히 재료의 함수다.** Fig. 11a 의 **400 MPa** 는 5호의
`[인쇄]` "75 MPa 도금 전 기계적 단락"(Li|황화물)의 **5.3 배**다. **LLZO 는 강성
세라믹**이고 5호는 **무른 황화물**이다 — 이 페이지의 기존 경고("상한은 음극·전해질
재료의 함수")와 **일치**하며, 두 숫자를 같은 축에 놓고 비교하면 안 된다.

**(라) 그리고 리뷰가 압력을 ECM 구축의 표준 축으로 올린다.** `[인쇄]` 제언 2:
"Further development and consistent adoption of DRT analysis, **in addition to
multi-variable (temperature, pressure and SoC) testing for equivalent circuit
modelling**."
`[해석]` 8호(Li 2026)가 BMS 쪽에서 `[인쇄]` "pressure-dependent impedance models" 을
요구한 것과 **같은 요구가 측정 방법론 쪽에서도 나온다.**

⚠ **압력 → 용량 곡선은 `assb` 10/10 편이 여전히 0 이다.**

## ★★ 2026-09-22 (`assb` 13호 Zheng 2026, **그리드 appraisal · Perspective, 1차 측정 0**) — 위 벽이 **둘**이 되고, 압력이 **제어변수**가 된다

`raw/papers/zheng2026_assb-grid-realistic-appraisal.md` (*Energy* 345, 140229). 수요 측(전력
연구원 + 전지 제조사) 저자들이 **그리드 용도의 압력 요구**를 적은 첫 편. 데이터 0 — 전부
`[인쇄]` "이 지면에 이렇게 적혀 있다".

### 1. 요구치 — 세 번째 독립 인쇄, 원전은 셋 다 다르다

| 편 | 요구치 | 근거 층위 | 원전 |
|---|---|---|---|
| 8호 Li 2026 | `<≈1 MPa` | 재인용 (산업 요구) | Xu 2024 (미수령) |
| 12호 Kouhestani 2022 | `0.4–1 MPa` | 재인용 (모델 최적) | Tian & Qi 2017 / Shao 2022 (중복 번호, 미확정) |
| **13호 Zheng 2026** | **`<5 MPa`** ×2 | **1 차 주장** — §3 "finite expansion [Si] drastically reduces the required stack pressure (<5 MPa)" [35] · §5 "A low-pressure threshold of <5 MPa enables simplified, passive mechanical constraints" [45] | [35] Li Menglin *AFM* 2025 · [45] Zhang *Nat. Commun.* 2025 (둘 다 미수령; **"5" 를 주는지 미확인**) |

⇒ **≈1–5 MPa 가 세 종설·세 원전에서 독립 수렴**. 이 페이지의 실측 창(5호 5–75 MPa · 6호
운전 2–4 MPa · 11호 20 MPa · 4호 ~2 MPa) 중 **6호·4호만** 그 안에 있다.

> ⚠ **2026-09-28 정정 (59호 Li Q. 2025 = 13호 [23])**: 위 "독립 수렴" 은 서지 않는다 — "Q6 요구 창의 정본 후보" 였던 [23] 이
> 요구치를 `<0.1 MPa`(인용 0)로 적고 1–5 MPa 는 요구치로 인쇄하지 않는다. 계보는 **일곱 편 · 0.1–5 MPa · 확인된 원전 0**(아래 §59호).
>
> ⚠ **2026-09-28 둘째 정정 (60호 Zhang 2025 = 13호 [45])**: [45] 도 "5" 를 주지 않는다 — 요구치 · 문턱 인쇄 0, 본문 `MPa` 값은 0.8 · 1.51 · 70 · 350 · 370 · 600 · 700 이고
> "5 MPa" 는 Table S2 의 5호 Doux 2020 운전 조건 한 칸이다. 13호 `<5` 의 인용 다리 둘([23] · [45])이 모두 비었고 남은 확인처는 [35] Li Menglin *AFM* 2025(미수령 · 원장 §1 에 없음)뿐(아래 §60호).
>
> ⚠ **2026-09-28 셋째 주석 (61호 Masias 2019)**: 계보의 "≈1 MPa" 에 **가장 이른 인쇄(2018 온라인)** 가 있다 — `[인쇄]` "stack pressures in the 1.0 MPa range are necessary to achieve
> low and stable cell resistance [9, 10]"(원전 [9] Sharafi … Sakamoto 2016 *JPS* 302 · [10] Wang & Sakamoto 2018 *JPS* 377 — 같은 실험실, 미열람)와 **같은 지면**의 "How much
> compressive stress is not known … We believe 1 MPa was sufficient". 여덟 편 · 띠 0.1–5 MPa · 확인된 원전 0 그대로. 그리고 그 띠는 Li 의 눈금으로 확산 creep(< 0.28) · 멱법칙(0.2–0.6) ·
> 항복(0.73–0.81) · power-law breakdown(> 2.83 MPa) 을 가로지른다 — **수렴했더라도 한 눈금이 아니었다**(아래 §61호).
>
> ⚠ **2026-09-29 넷째 주석 (81호 Xu 2024 = 표 첫 줄의 "Xu 2024 (미수령)")**: 열었다 — `< 1 MPa` 는 **초록 한 줄 · 인용 0 · 본문 재진술 0** 이다. 8호는 이 편의 재인용이라
> 독립 인쇄가 아니다 ⇒ **아홉 편(독립 인쇄 여덟) · 여섯 값(0.1 · 0.4–1 · < 1 · 1 · 2 · 5) · 띠 0.1–5 MPa · 확인된 원전 0 그대로**(아래 §81호).

★ 그리고 `[도표]` **Fig. 2 가 본문에 없는 클래스별 창 다섯을 준다** (레이더 축 라벨):
**Oxides ≥30 MPa · Sulfides 5–20 · Halides 2–10 · Polymers "No or compliant" · Composites
1–10 MPa**. ⚠ 산정 규칙·출처 0 (13호 G8). ⚠⚠ 본문이 권하는 두 클래스(Halides·Composites)의
**상단 10 MPa 가 본문 문턱 `<5` 의 2 배** — 논문은 조정하지 않는다 (13호 D4). 이 다섯 값은
`[도표]` 로만 두고 **창의 값으로 쓰지 않는다.**

### 2. ★★ 위 벽의 두 번째 형태 — 단락이 아니라 **피로**

이 페이지의 위 벽은 5호(Doux)의 **단락**이었다: Li 크리프가 전해질 공극으로 밀려 들어가
`[인쇄]` 75 MPa 에서 도금 전에 단락 — 시간 스케일 **시간(h)**.
13호가 다른 위 벽을 적는다 (§5, 1 차 주장, 데이터 0):
`[인쇄]` "high, constant stack pressure can induce detrimental long-term effects: **creep and
stress relaxation** in softer components (e.g., polymer binders) and **fatigue-driven micro-crack
initiation** in brittle ceramics, gradually degrading interfacial contact, increase impedance,
and accelerate overall cell degradation."
— 시간 스케일 **년**, 기구 **기계 피로**, 대상 **바인더·세라믹 전해질**(Li 금속 아님).
`[해석]` 두 위 벽은 **다른 축**이다: 5호 것은 "지금 단락하는가", 13호 것은 "20 년 뒤 접촉이
남는가". 한 숫자로 합치지 않는다. 13호는 `[인쇄]` "dearth of data on the 'mechanical fatigue'
of solid electrolytes" 라 스스로 적는다 — **이 벽의 위치는 아무도 모른다.**

### 3. ★★ 압력이 관측 + 제어변수가 된다 — 그리고 정책까지

- **관측**: `[인쇄]` "piezoelectric or thin-film pressure sensors within the cell stack to monitor
  the distribution and **decay of interfacial contact pressure** over time" + `[인쇄]` "decay of
  interfacial contact pressure — **a primary driver of impedance growth**". 인과 방향이 명시됐다:
  `P(t) ↓ → R(t) ↑`. (9호 Huo 2025 가 힘 시계열을 **재고도 모델에 안 넣은** 자리다.)
- **제어**: `[인쇄]` "**active stress management** … the BMS would not merely monitor but act …
  apply **higher pressure during high-rate cycling** to maintain electrical contact and then
  deliberately **reduce pressure during extended rest periods or as the cell ages** to minimize
  the creep of soft components and the mechanical fatigue of brittle electrolytes".
  8호의 `[인쇄]` "coupled state/control variable" 에 **정책(율↑→P↑ · 휴지/노화→P↓)** 이 붙었다.
  인용 0 · 데이터 0.
- `[해석]` 이 정책은 이 페이지 §"이력" 과 정면으로 만난다: `θ(P)` 가 **경로 의존**이면
  (5호: 처녀 5 MPa 110 Ω ↔ 25 MPa 를 찍고 내려온 5 MPa 50 Ω) 압력을 오르내리는 제어는
  **상태를 매번 다른 가지에 올린다**. 13호는 이력을 모른다 (`hysteresis` 1 회는 전압 이력).
  → [[assb-pressure-reapplication-separation-test]] 의 분리 연산자를 **BMS 가 주기적으로
  실행하는 것**과 같은 조작이 되고, 그 조작이 상태를 바꾼다.

### 4. 이 편이 이 페이지에 **안 준 것**
압력 → 용량 (**11/11 → 12/12 편 0** — 13호는 데이터 0) · 스윕 0 · 이력 0 · 계측 0 ·
`MPa` 본문 2 회. **창의 값은 하나도 움직이지 않았다.** 움직인 것은 **창의 구조**(위 벽 둘,
압력 = 제어변수)와 **요구치의 자릿수 수렴**이다.

## ★★ 2026-09-22 (`assb` 14호 Oh 2025, **실험 · Hot Paper**) — 압력이 **관측 변수**가 되고, 계보 최초의 **`E(P)`** 가 들어온다

`raw/papers/oh2025_maxwell-protocol-nondestructive-assb-health.md` → [[assb-maxwell-ocv-derivative-channels]].
NCM811‖LPSCl‖**Li 금속**, 제작 100(SE)/350(스택) MPa, 운전 **10 / 20 MPa**(스프링 하우징 ·
디지털 프레스), 진단 **ΔP = −5 / −10 MPa**(≤0.01 MPa), 처방 **>300 MPa**(미수행).

1. ★ **압력 → OCV — 이 페이지에 없던 관측량.** 5호는 `Z(P)`, 6호는 `Q(P)` 1.5 %p, 14호는
   **`E(P)` 의 기울기**: `[인쇄]` 신품 **2.2 mV / 5 MPa (10→5)** · **2.3 mV / 10 MPa (20→10)**
   ⇒ `[재현]` **0.44 ↔ 0.23 mV/MPa — 2 배, 오목 비선형** (논문 무언급; Fig. 5e/f 눈금이 달라
   가려진다). `[해석]` 접촉 역학(Hertz 형)이 OCV 에 얹힌 모양 — 압력 창의 **아래쪽일수록
   OCV 가 압력에 민감**하다는 뜻이고, 산업 요구치(<≈1–5 MPa)에서는 더 가파를 것이다.
2. ★ **압력 → 용량 2 점 (13/13 → 14호)**: `[인쇄]` 50 사이클 유지율 **10 MPa 86.0 % ↔ 20 MPa
   84.0 %** — 그리고 공극률은 **9.8 ↔ 5.3 %**. **역상관**(void 적은 쪽이 용량 낮다). 논문은
   "similar" 로 덮는다. ⚠ 조건당 셀 1.
3. ★ **위 벽 대조**: 5호 Li 금속 **20 MPa → 190 h 단락**. 14호는 20 MPa 에서 50 사이클 0.5C
   (`[재현]` ≈225 h) 를 돌리고 **단락 보고 0** — 다른 설계(스프링·펠릿 ∅10 mm)·전류밀도
   (로딩 미기재)라 직접 비교 불가이지만, **5호 상한이 보편값이 아니라는 세 번째 표본**
   (6호 4 MPa · 10호 400 MPa 에 이어).
4. **이력의 그림자**: `[도표]` S16 재가압(10→20 MPa) 뒤 OCV 가 초기보다 **+0.4 mV 높게**
   안착, 감압 유지 중 **+0.5 mV 표류** — 노화 신호(0.1–0.4 mV)와 같은 자릿수. 5호 `θ(P)`
   경로 의존의 소신호 판. 논문은 `dE` 판독 규칙을 안 적는다.
5. **"10 MPa 는 Li creep 을 일으키기에 충분"** `[인쇄]` (ref [70] LePage 2019) — 음극 pore
   무시의 근거. 5호의 Li 항복강도 ≈0.8 MPa 와 같은 방향.
6. ⚠ **>300 MPa recondition 은 Li 금속 셀에 5호 상한(75 MPa)의 4 배** — 수행도 인용(4호)도
   없다. 로드셀 명시 0(프레스 "sensing" 만), 스윕 0(2 구간), 압력 시계열 0.

## ★★★ 2026-09-22 (`assb` 16호 Ramanayagam 2026, **실험 · 3전극**) — **제작 = 운전**, 그리고 압력 → 용량의 폭

`raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md`.
NMC83|6|11(단결정, LiNbO₃ 1 wt%) ‖ Li₅.₃PS₄.₃ClBr₀.₇ ‖ **In/InLi**, ∅12 mm(A = 1.13 cm²),
양극 두께 **26–219 µm 5 점**, **0.1 C · SOC50 · 2 번째 사이클 · 셀 12 개 · 조건당 n = 1**.
`pressure` **49 회 — 이 계보 최대**(13호 24 회를 넘는다).

### 1. ★★ 이 페이지의 두 축(제작 ↔ 운전)이 **처음으로 겹친다**

6호(Lee)가 쪼갠 두 축 — 제작 490 MPa / 운전 2 MPa — 은 **서로 다른 장비**의 압력이었다.
16호는 **CompreDrive 전기화학 프레스 (active force control)** 안에서 제작하고
**그대로 그 압력에서 측정**한다.

| | 제작 | 운전(측정) |
|---|---|---|
| 분리막 선압축 | **97 MPa / 3 min** | — |
| 셀 압착 | **389 MPa / 3 min** | — |
| 측정 | — | **389 MPa** 또는 **97 MPa** |

★★★ `[해석]` **결과: 97 MPa 점은 처녀 상태가 아니라 389 MPa 에서 내려온 점이다.**
5호(Doux)의 이력(처녀 5 MPa 110 Ω ↔ 25 MPa 를 찍고 내려온 5 MPa 50 Ω)이 참이면
**이 편의 97 MPa 데이터는 전부 하강 분기**다. **논문은 이 사실을 한 번도 말하지 않고**
(`hysteres*` **0 회**) 두 압력을 **대칭적인 두 조건**처럼 비교한다.
⇒ **5호의 `θ(P)` 이력 물음에 답하지 않는다. 대신 그 물음이 왜 중요한지를 보여 준다** —
이 계보에서 이력을 명시적으로 잰 편은 **여전히 5호 하나뿐**이다 (10호가 재인용으로 재현).

### 2. 압력 → 임피던스 — **1 차 측정, 그리고 전극별로 갈라서**

| 관측 | **389 MPa** | **97 MPa** | 비 | 층위 |
|---|---:|---:|---:|---|
| 완전지 반원합 (얇은 양극) | **23 Ωcm²** | **85 Ωcm²** | 3.7 | `[인쇄]` |
| 완전지 반원합 (두꺼운 양극) | **11 Ωcm²** | **23 Ωcm²** | 2.1 | `[인쇄]` |
| **양극** 중주파 반원 (3E) | **≈10 Ωcm²** | **≈20 Ωcm²** | 2.0 | `[인쇄]` |
| **음극** 중주파 반원 (3E) | **≈4 Ωcm²** | **≈9 Ωcm²** | 2.25 | `[인쇄]` |
| TLM `R_CT` (계면 면적 기준) | `[재현]` 193 Ωcm² | `[재현]` 347 Ωcm² | **1.80** | `[재현]` (식 5 + Table 2) |
| TLM `R_ion` (d = 200 µm) | `[도표]` ≈64.5 | `[도표]` ≈74 | 1.15 | `[도표]` = `[재현]` 64.9/74.2 |

★ `[재현]` **양극(2.0)과 음극(2.25)이 거의 같은 배율로 움직인다.** 논문은 두 전극에 다른
기구를 붙이는데(양극 = 전하이동 개선, 음극 = interphase 통로 수 증가) **배율이 같다.**
`[해석]` 두 계면이 **같은 기하 인자(접촉 면적)를 공유한다**는 쪽을 가리킨다 —
[[assb-lampe-contact-product-degeneracy]] 의 논거.

★★ **그리고 5호와 자릿수가 완전히 다르다**: 5호는 **1 → 25 MPa 에서 >500 → 32 Ω (>15 배)**,
16호는 **97 → 389 MPa 에서 2–3.7 배**. `[해석]` **모순이 아니라 같은 포화 곡선의 다른 구간**이다 —
**저압 구간에 정보가 있고 고압 구간은 평평하다**는 이 페이지의 §1 이 **네 자릿수 위에서 재확인**된다.

### 3. ★★★ 압력 → 용량 — **세 번째 표본, 그리고 폭이 압도적**

| 편 | 압력 구간 | 용량 차 | 층위 |
|---|---|---|---|
| 6호 Lee 2020 | 2 / 3 / 4 MPa (+무압) | 율특성 **1.5 %p** | `[도표]` |
| 14호 Oh 2025 | 10 / 20 MPa | 50 사이클 유지율 **2 %p** (역상관) | `[인쇄]` |
| **16호 (이 편)** | **97 / 389 MPa** | **1 사이클 방전 +9 … +59 %** | `[도표]` (SI Fig. S2) |

`[도표]` 두께 쌍별 1 사이클 방전용량(mAh g⁻¹, ±5): 26↔31 µm **181 ↔ 120** ·
58↔54 **157 ↔ 123** · 80↔81 **159 ↔ 134** · 104↔106 **164 ↔ 103** · 207↔219 **93 ↔ 85**.
**모든 쌍에서 389 MPa 이 크다.**

⚠⚠ **그런데 논문은 용량을 한 번도 읽지 않는다** — `capacity` **본문 1 회**이고 그것도
서론의 "energy storage capacity" 다. **이 표는 전부 SI 그림에서 우리가 읽은 것이다.**
⚠ 셀이 다르고 각 점 **n = 1**, 97 MPa 쪽은 두께 의존이 **비단조**(81 µm 최대)라
셀 간 산포가 작지 않다.

★★★ `[해석]` **세 편을 나란히 놓으면 압력 → 용량 감도가 구간에 따라 두 자릿수 다르다**:
2–4 MPa 에서 1.5 %p, 10–20 MPa 에서 2 %p, **97–389 MPa 에서 9–59 %**.
**산업 요구치(<≈1–5 MPa)는 가장 평평한 쪽에 있다** ⇒ **압력을 진단 여기(excitation)로 쓰려는
계획은 산업 셀에서 신호가 가장 약한 구간을 쓴다.** ⚠ 셀·화학·전류가 전부 달라 **한 곡선으로
잇지 않는다** — 세 점은 **같은 곡선 위의 점이 아니다.**

### 4. ★ 압력 → 공극률 — **기하는 둔하고 계면은 예민하다**

`[인쇄]` in situ 공극률–압력 장치 [34] 로: **97 MPa 에서 12.9 %**, **389 MPa 에서 11.2 %**.
⇒ `[재현]` **압력 4 배에 공극률 1.7 %p (상대 13 %)** 움직이는 동안
**`R_CT` 는 1.8 배 · 음극 DRT 는 최대 15 배** 움직인다.

★★ `[해석]` **같은 압력 구간에서 두 관측의 감도가 한 자릿수 이상 다르다.**
14호(Oh)가 **volumetry**(부피·void)를 비파괴 분리 후보로 민 것과 **긴장 관계**에 있다 —
volumetry 가 보는 양은 **압력 여기에 대해 가장 둔한 채널**일 수 있다.
⚠ 두 논문의 압력 구간(10–20 ↔ 97–389 MPa)·화학·측정이 달라 **직접 비교가 아니다.**
후속에서 확인할 좌표로 남긴다.
⚠⚠ 그리고 이 공극률의 출처 [34] 는 **심사 전 chemRxiv 프리프린트**이고, 이 편의
**두께 전부(26–219 µm)** 가 거기에 걸려 있다.

### 5. 이 편이 이 페이지에 **안 준 것**

**스윕**(2 점뿐) · **이력**(같은 셀 재가압·감압 0) · **로드셀 시계열 0** ·
**사이클 중 압력 변화 0**(2 번째 사이클에서 끝난다) · **상한·단락 0**(In 음극이라 Li 도금
단락 기구가 없다) · **열화 0**. **창의 위 벽·아래 벽 값은 하나도 움직이지 않았다.**
움직인 것은 **창의 폭**(운전 압력 최댓값이 75 → **389 MPa**, ⚠ 화학이 다르다)과
**압력 → 용량 감도의 구간 의존성**이다.

## ⚠ 2026-09-22 (`assb` 17호 Yanev 2024, **실험 · 3전극**) — 한 점, 그리고 **압력이 데이터 없이 설명 변수로 쓰인 첫 사례**

`raw/papers/yanev2024_li-in-alloy-anode-kinetic-limitations.md`.
제작 `[인쇄]` **500 MPa / 1 min**(2전극 분리막·음극·양극 전부; 3전극 분리막만 **375 MPa**),
운전 `[인쇄]` **ca. 50 MPa**(2전극, 30 °C) / **50 MPa**(3전극, 실온, rhd CompreDrive).
`pressure` **7 회** · `MPa` **13** · `stack pressure` **2** · **`hysteres*` 0**.
**스윕 0 · 이력 0 · 계측 0 · 압력 → 용량 0 · `E_CE(P)` 0.**

### 1. ⚠ 이 페이지에 **값을 더하지 않는다** — 그러나 새 경고를 준다

★ 17호는 **자기와 정반대 결론의 논문**(ref 28, Wang 2023, `[인쇄]` **14.3 at% Li 가 최적**)
과의 불일치를 이렇게 넘긴다:

> `[인쇄]` "We **suspect** that methodic differences could explain the differing
> findings, since our study was done with **considerably higher rates and lower stack
> and assembly pressure**."

⚠⚠ **상대의 압력값을 적지 않고, 자기 압력은 한 점이다.**
`[해석]` **`assb` 계보에서 압력이 설명 변수로 동원되면서 데이터가 0 인 첫 사례다.**
(4·5·6·11·14·16호는 최소한 2 점 이상을 갖고 말했다.)
⇒ **이 페이지의 규율 하나**: 문헌이 불일치를 "압력 차이" 로 넘길 때 **그 압력값이
인쇄돼 있는지 먼저 본다.** 17호에서는 없다.

### 2. ★★★ 그래도 **16호와의 대질**이 하나 생긴다 (`[해석]`, 미검증)

**두 편이 같은 In 계 음극을 쓰는데 음극 임피던스가 한 자릿수 다르다**:

| | **16호** (Ramanayagam 2026) | **17호** (Yanev 2024, foil) |
|---|---|---|
| 운전 압력 | **97 / 389 MPa** | **50 MPa** |
| 음극 출발 | **순수 In 박** → 셀 안에서 리튬화 | **Li 박 + In 박 압착**(기계적) |
| LiIn 이 생기는 곳 | **분리막 쪽** (Li 가 거기서 들어온다) | **집전체 쪽** (`[인쇄]` "do not reach the separator side") |
| `x_Li` | **0.05–0.28** | 0.40 |
| 음극 임피던스 | `[인쇄]` **4 ↔ 9 Ω cm²** | `[재현]` **≥66 Ω cm²**, 100 mHz 미폐 |

`[해석]` **두 설명이 경쟁한다**:
① **압력**(2–8 배) — 이 페이지의 축 ·
② **LiIn 상의 위치**(17호의 논지) — 압력과 무관한 제조 기하.
**17호는 압력을 안 흔들었고 16호는 제조법을 안 흔들었으므로 둘을 가를 수 없다.**
⚠ SE·조성·전류·SOC·전극 두께도 전부 다르다.
⇒ **이 페이지에 새 빈칸**: **`Z_anode(P)` 를 제조법 고정하고 재는 편이 0 편이다.**
(16호가 2 점을 줬지만 **다른 셀**이고 **둘 다 389 MPa 제작 뒤**라 하강 분기다.)

### 3. ⚠ 압력이 아닌 축 하나가 여기서 새로 걸린다 — **기준 전위**

17호가 보인 것은 **압력이 아니라 제조법만으로 음극 전위가 0.74 V 움직인다**는 것이다
([[assb-li-in-reference-potential-window]]). 그리고 이 페이지에는 **`E(P)` 가 하나 있다** —
14호의 `[인쇄]` 2.2 mV / 5 MPa (Li 금속).
`[해석]` **두 크기가 300 배 차이다.** 압력이 전위에 주는 영향(mV 자릿수)은 제조법이
주는 영향(수백 mV)에 묻힌다. ⇒ **`E_CE(P)` 를 재려면 제조법을 고정해야 하고,
그것이 위 §2 의 실험이다.**

## ⚠⚠ 2026-09-22 (`assb` 18호 Fukunishi 2023, **실험 · 3전극 · 열화**) — **압력이라는 낱말이 없는 열화 논문**

`raw/papers/fukunishi2023_ncm523-three-electrode-impedance-degradation.md`
(*J. Power Sources* **564** (2023) 232864).

**어휘 집계 결과가 이 편의 Q6 전부다**: `pressure` **본문 0 회** ·
`stack pressure` **0** · `hysteres*` **0** · `MPa` **2 회뿐** —
`[인쇄]` 3전극 셀을 "pressed at **110 MPa**", 대칭셀을 "pressuring at **150 MPa**".
**운전 압력은 값도 장치도 문장도 없다**: 셀은 PET 관(φ10 mm) 안에 눌린 뒤
`[인쇄]` "Ar-filled **polystyrene container**" 에 들어가고 단자로만 측정된다.

⚠⚠ **그런데 이 편의 두 열화 기구 중 하나가 정확히 `void formation` 이다**
(`void` **7 회** — 이 계보 실측 편 최다):
- `[인쇄]` 결론 — "the **void formation** seen in the LPSI system that causes the increase
  in R4 and the diffusion-related resistance … leads to the **capacity loss**"
- `[인쇄]` 그리고 LPSCl 의 추가 고주파 반원(`R1′`)도 **void 로 설명된다** —
  "Young's modulus of LPSCl (22.1) lower than that of LPSI (30) … adhesions … **less
  sufficient** … leading to **void formation** to generate capacitive components"
  (⚠ 단위 없음, ref 는 **제일원리 계산**인데 LPSI 는 glass-ceramic)

⇒ ★★★ **압력에 가장 민감한 양(입자 간 공극)을 주인공으로 삼으면서 압력을 통제하지
않은 첫 실측 편이다.** 계보 비교: **16호 `pressure` 49 회 · 17호 7 회 · 18호 0 회.**

`[해석]` **이 페이지가 받는 것은 값이 아니라 빈칸의 형태다** — 지금까지 이 페이지의
빈칸은 "스윕이 없다 · 이력이 없다 · 계측이 없다" 였다. **18호는 그 앞 단계의 빈칸을
보인다: 열화 기구를 void 로 지목하고도 압력을 변수로 *인식하지 않는* 논문이 있다.**
⇒ **`θ(N)` 을 문헌에서 모으려는 시도가 왜 계속 막히는지의 한 이유**이기도 하다 —
**같은 셀을 다른 압력에서 늙혔을 때 void 가 어떻게 다른가를 물은 편이 0 편**이다.

⚠ 그리고 **제작 압력 축에는 값이 하나 더 붙는다**: **110 MPa**(3전극 셀) ·
**150 MPa**(대칭셀). ⚠ **같은 논문 안에서 두 셀의 제작 압력이 36 % 다르고**,
그 대칭셀이 **`R2`(집전체 전자 접촉) 귀속의 유일한 독립 근거**다.

## ★★★ 2026-09-23 (`assb` 25호 Zhou 2025, **실험 · 2전극 Li 금속 · 운전 압력 3 점 × SE 입도 2**) — **양극 쪽 첫 요인 설계, 그리고 위 벽의 반례 후보**

`raw/papers/zhou2025_tailored-cathode-microstructure-low-pressure-assb.md` (*ACS Energy Lett.* 10, 966−974, UCSD + LG Energy Solution — **5호와 같은 캠퍼스, 5호 인용 0**).
NCM811–Li₆PS₅Cl 복합양극을 **SE 입도만** 바꿔(coarse ↔ fine) **운전 30 · 10 · 2 MPa** 에서 100 사이클. 18호 절의 빈칸 "**같은 셀을 다른 압력에서 늙혔을 때 무엇이 다른가를 물은 편이 0 편**"
을 채우는 **첫 편**이다(셀은 조건마다 다르다).

### 1. ★★★★ 압력 × 미세구조 — 초기는 공통 모드, 상호작용은 감쇠에만 (`[재현]` Fig. 2c 벡터 판독)

| | coarse | fine |
|---|---|---|
| 30 → 2 MPa, 2 사이클 방전 손해 | −26.5 mAh g⁻¹ | −30.7 |
| 2 → 100 사이클 감쇠 @30 / 10 / 2 MPa | −33 / −38 / **−64** | −26 / −27 / **−22** |
| `R_SSE/NCM` 1 사이클 뒤 @30 / 10 / 2 (`[도표]`) | ≈65 / 110 / 125 Ω | ≈62 / 105 / 115 |
| `R_SSE/anode` 1 사이클 뒤 | ≈210 / 350 / 380 | ≈208 / 345 / 355 |

⇒ **압력은 1 사이클까지 두 미세구조를 같이 깎는다**(용량·양극 계면·Li 계면 셋 다). 미세구조가 바꾸는 것은 **감쇠의 압력 의존**뿐이고, fine 의 감쇠는 **압력에 무관**하다.
30 ↔ 10 MPa 초기 용량은 거의 같다 ⇒ **아래 벽의 문턱이 2–10 MPa 사이**(5호의 "정보는 저압에" 와 같은 모양).
⚠ "저압 장수명" 은 **유지율**의 참이다 — fine 도 2 MPa 에서 30 MPa 대비 ≈26 mAh g⁻¹(−17 %)를 100 사이클 내내 잃는다.

### 2. ★★★ 위 벽 — 5호와 맞지 않는다

5호: Li 금속 대칭셀 **25 MPa 에서 ≈48 h 단락** · Li 금속 완전지 **25 MPa 2 사이클째 실패**. 25호: Li 금속 완전지 **30 MPa 100 사이클 ≈1500–1700 h**(`[재현]`, 1C ≡ 200 mAh g⁻¹ 가정)
단락 보고 0, 평균 CE 99.86 %(`[도표·벡터]`); 전류(≈0.106 ↔ 0.075 mA cm⁻²)·도금 두께(≈4.9 ↔ 0.36 µm/스텝)는 25호가 더 가혹하다.
화해 후보(`[추론]`, 전부 지면 밖): 분리막 ≈1.4 mm ↔ ≈1 mm · **압력 장치 미기재**(정변위면 실제 압력이 이완했을 수 있다) · Li 부착 30 ↔ 25 MPa.
⇒ **위 벽(≥25 MPa 단락)은 모집단 경계가 있는 결론이다 — 반례 후보 하나.** 검증 불가: 25호는 로드셀·토크·스프링이 **0 회**다.

### 3. 이력 · 요구치

- 모든 셀이 **양극 375 MPa · Li 30 MPa** 제조 뒤 운전 압력으로 간다(내린 절차 미기재) ⇒ 10 · 2 MPa 셀은 §이력의 **하강 분기**. "저압" 은 **저압 운전 · 고압 제조**다.
- `[인쇄]` "industry generally aims to operate at or below **5 MPa**" — **출처 없음**. 8호의 Xu 2024 "<≈1 MPa" 와 다른 **네 번째 인쇄 요구치**.

### 4. 이 편이 이 페이지에 **안 준 것**

압력 계측·장치 · 압력 이력 · 조건당 반복(같은 지면의 다른 셀이 2 MPa fine 에서 ≈30 mAh g⁻¹ 더 준다 — 효과와 같은 크기) · 접촉 분율의 압력 함수(SEM 한 시야, 정성) ·
2 MPa "1 사이클 뒤" EIS 기준점(`[재현]` 그 두 스펙트럼이 30 MPa "100 사이클 뒤" 와 ≤0.8 Ω 로 같다).

## ⚠ 2026-09-23 (`assb` 33호 Zhang 2025, **저압 종설 · 1차 측정 0**) — 제조 ↔ 운전 분리는 종설이 받아 적었고, **요구치는 다섯 번째 값**, 압력의 함수는 0

`raw/papers/zhang2025_low-pressure-assb-challenges-strategies-review.md` (*Adv. Mater.* 37, 2413499, EIT Ningbo + USTC + UWO; 22 쪽, 참고문헌 124). 큐 32 — 8호가 "pressure reduction = central commercialization problem" 을 매단 편(그 명제는 선다).

### 1. 이 페이지의 두 축(제작 ↔ 운전)을 종설이 명시적으로 가른다 — 계보 종설 첫

`[인쇄]` §2.1 "fabrication pressure and operation pressure" 두 범주 + Table 1 이 **두 열을 따로** 인쇄(10 행). `[재현]` 제조가 인쇄된 8 행 중 7 행 **360–500 MPa**, 운전 10 행 중 9 행 **≤5 MPa**(예외 [58] Koerver 2018: 445 / 70). ⇒ 종설이 모은 **"저압 ASSB" 는 전부 "고압 제조 · 저압 운전"** 이다 — 6호(490 / 2) · 25호(375 / 2–30)와 같은 모양, 16호(제작 = 운전)가 예외로 남는다. ⚠ 각 행은 **압력 한 점 · 용량 한 점**이고 같은 전극의 압력 스윕은 **0 행**이다.

### 2. 요구치 — 다섯 번째 인쇄값, 원전 0

| 편 | 요구치 | 원전 |
|---|---|---|
| 8호 | < ≈1 MPa | Xu 2024 (재인용, **확인 편 0**) |
| 12호 | 0.4–1 MPa | Tian & Qi 2017 / Shao 2022 (미확정) |
| 13호 | < 5 MPa | [35] |
| 25호 | ≤ 5 MPa | 없음 |
| **33호** | **< 2 MPa**(Fig. 1) · **≤ 2 MPa, OEM 마다 약간 다름**(p.4) | **없음** — `[인쇄]` "To our knowledge" |

33호는 Xu 2024 를 [11] 로 인용하되 `[인쇄]` "often reaching hundreds of megapascals" 에만 붙이고 **"<≈1 MPa" 를 옮기지 않는다.** ⇒ 이 페이지 머리의 "산업 요구치 < ≈1 MPa" 는 **0.4–5 MPa 띠 · 원전 0** 으로 읽는다. 그리고 33호 Fig. 1 의 `[인쇄]` "most labs 50–600 MPa"(운전)는 출처가 없고, 이 페이지가 모은 운전 압력 표본(대부분 ≤30 MPa, ≥50 MPa 는 16 · 17 · 23호 + 5호 75 MPa 점)과 맞지 않는다 — 600 MPa 는 **제조** 대역이다.

### 3. ★★ `[해석]` 사이클당 압력 진동 ≈ 요구치 — 운전 압력은 상수가 아니다

33호에 재수록된 정변위 지그 원자료(`[도표]`): 흑연 ± LGPS [59] ≈0.7–0.8 MPa · μ-Si ‖ LTO [88] ≈0.5–1.0 MPa(기저 ≈45) · Sb ‖ Li [90] ≈1.2–2.3 MPa(기저 ≈20) ↔ LCO/NCM 양극 [58] ≈0.05–0.07 MPa · 스프링(정압) 지그 [19] ≈5 → 5.21 MPa(+4 %). ⇒ **상대극 호흡의 ΔP 가 요구치(≤2 MPa)와 같은 자릿수**다 — 산업 조건에서 스택 압력은 사이클 안에서 ≈100 % 움직이는 **상태변수**(8호 "coupled state/control variable" 의 숫자판). §"세 개의 결과" 3 의 `P↑` 연산자에 **"양극에 걸리는 압력 = 지그 + 상대극 ΔP(SOC)"** 조건이 붙는다. ⚠ 기저가 고압(20–45 MPa)이라 저압 기저의 진동 크기는 미상. (→ 2026-09-28 62호: **이 관찰의 원형 표본** — In ‖ LCO 충전 ΔP 원시 +1.0–1.13 · 보정 1.25 MPa ↔ LTO ‖ LCO ≈0.067 MPa(상대극 몫 `[재현]` ≈90–95 %), 기저 ≈61.8 MPa 는 역시 ESI 그림 축에만. 크기는 기저선 규약 · 지그 순응이 정한다 — [[assb-operando-pressure-signal-attribution]] · 62호 절.)

### 4. 이 편이 이 페이지에 **안 준 것**

압력의 함수 — `θ(P)` · `R(P)` · 용량(P) · 감쇠(P) 어느 것도 원전 서술로 없다. 가장 가까운 재수록은 Fig. 3I(70 / 7 / 2 MPa 첫 사이클 곡선, 캡션 [63] ↔ 본문 [78] 로 출처 갈림, `figure-read` 2 MPa Pristine ≈−10 %)와 Fig. 7B(2 MPa 한 점, 컷오프만 바꿈). **Sakka 2022**(`θ(P)` CT 측정 후보)는 [120] 으로 인용되지만 "3D 접촉 · 압력 방향" 명제에만 붙는다 — 25호가 같은 원전에서 옮긴 "50 ↔ ≤12 MPa 접촉 면적 분율" 은 이 지면에 없다.

## ★★★ 2026-09-23 (`assb` 39호 Sakka 2022, **실험 · CT + 동시 EIS · 제조 가압 0 → 단조 0–100 MPa**) — **아래 벽의 구조판: 압력 → 공극률 · 접촉 피복 · `R_ct` 가 한 장치에서, 단 그 압력은 제조 압력이다**

`raw/papers/sakka2022_pressure-3d-structure-composite-cathode-xct.md` (*J. Mater. Chem. A* 10, 16602, 리쓰메이칸 + Toyota + SPring-8). NCM111(LiNbO₃)/LGPS/In–Li, Ø 1 mm, 로드 트랜스듀서 감시 · 나사 가압.
33호 절이 "이 페이지에 안 준 것 — 압력의 함수" 로 남긴 빈칸을 **1차 원전으로** 채우는 첫 편이다(원장 최상위였던 이유).

### 1. ★★★ 압력의 함수 — 같은 장치, 5 점 (`[인쇄]` 라벨 / `[도표]` 판독)

| P / MPa | 0 | 6 | 12 | 50 | 100 |
|---|---:|---:|---:|---:|---:|
| 복합층 공극률 % (인쇄 라벨) | 44 | 42 | 39 | 31 | 23 |
| SE 층 공극률 % (`[도표]`) | ≈53 | ≈41 | ≈39 | ≈15 | ≈4.3 |
| 접촉 피복 `φ` % (`[도표]`) | ≈78.3 | ≈74.9 | ≈77.9 | ≈84.3 | ≈82.7 |
| `R_ct` ×10⁵ Ω (`[도표]`, 2전극) | — | ≈8.7 | ≈4.1 | ≈1.6 | ≈0.62 |
| 겉보기 전도도 ×10⁻⁵ S cm⁻¹ (`[도표]`) | — | ≈7.8 | ≈8.0 | ≈9.1 | ≈9.7 |
| 첫 방전 mAh g⁻¹ (다른 셀, `[도표]`) | — | ≈27 | — | ≈39 | ≈44 |

⇒ **아래 벽의 문턱이 12–50 MPa 사이**로 읽힌다(`φ` · 공극률 차이가 ≤12 ↔ ≥50 로 갈린다; `[인쇄]` "improvement in the contact area fraction stopped when the pressure reached 50 MPa"). 25호의 "2–10 MPa"(운전 압력, 375 MPa 제조 뒤)와 **다른 양의 문턱**이다 — 아래 2.

### 2. ★★★★ 그 압력은 제조 압력이다 — 이 페이지의 두 축 중 어느 쪽인가

`[인쇄]` 서론이 두 양을 정의로 가르고("The former is the fabrication pressure and the latter is the stack pressure"), 결과에서 **자기 실험은 제조 가압이 없으므로 "the pressure shown in this study corresponds to the previously reported fabrication pressure"** 라고 적는다.
`[인쇄]` SI Fig. S14: 50 MPa → 0 MPa 로 풀어도 "No clear changes … with respect to the void"(정성 1 장).
⇒ 이 편의 표는 **최대 압력(= 제조 압력)의 함수**다. 16호(제작 = 운전)와 같은 부류이고, 25 · 33호가 모은 "고압 제조 · 저압 운전" 의 **운전 압력 문턱으로 옮기면 안 된다.** 제조 뒤 되돌림의 전기화학(`R_ct` · 용량)은 0 점이다.

### 3. 요구치 — 여섯 번째 인쇄, **처음으로 원전이 지목된다**

`[인쇄]` "Based on the literature, the upper limit of the stack pressure is suggested to be **1 MPa practically**,[22]" — ref 22 = **Wang, Kazyak, Dasgupta, Sakamoto, *Joule* 2021, 5, 1371–1390**.
위 33호 절 표(8호 <≈1 · 12호 0.4–1 · 13호 <5 · 25호 ≤5 · 33호 <2 MPa, **확인된 원전 0**)에 여섯 번째 값이 붙고, **원전 지목이 하나 생긴다**(미열람 — 확인 편 여전히 0).

### 4. ⚠ 정정 — 25호 digest 의 "모델상 25 MPa" 는 이 편의 명제가 아니다

25호 digest(`raw/`, 불변)가 "Sakka 2022 — … 모델상 **25 MPa 면 안정 접촉**" 으로 적었다. Sakka 에는 **모델이 없고** "25 MPa" 는 SI Fig. S3 범례의 가압 단계뿐이다. Zhou 원문에서 그 문장은 ref 12 **다음 문장이며 인용 번호가 없다** — 인접 문장을 우리가 붙였다. 이 페이지의 25호 절은 그 문장을 쓰지 않았으므로 결론 변화는 없다.

### 5. 이 편이 이 페이지에 **안 준 것**

운전 압력(되돌림) 의 함수 · 위 벽(단락 · Li 금속 0) · 사이클 뒤 구조 · 반복(점당 n = 1, 같은 조건 다른 셀의 첫 방전 ≈27 ↔ ≈35 mAh g⁻¹) · 전극별 저항(2전극 — 상대극 In–Li 계면도 같은 나사 압력을 받는다). 같은 셀 단계 가압(SI S3, 6 → 12 → 25 → 50 → 100 MPa, 두 사이클씩)의 "용량 향상" 은 **사이클 번호와 교락**되고 절대 방전은 12 → 100 MPa 에서 준다(≈21 → ≈14 mAh g⁻¹).

## ★★ 2026-09-23 (`assb` 52호 Oh 2025, **실험 · N/P < 1 과충전 음극 · 운전 20 · 3 MPa + 파우치 3 MPa**) — **운전값은 명시, 비교는 교락: 저압의 "지배 인자" 는 압력이 아니라 음극을 바꿔서 얻었다**

`raw/papers/oh2025_mgsigr-overcharge-low-np-ratio-low-pressure-assb.md` (*Adv. Energy Mater.* 15, 2404817, 서울대 + HMG-SNU JBRC + 현대차 — **14호와 같은 연구실**).
LiNbO₃-NCM811 \| LPSCl \| MgSiGr(Mg 200 nm 위 SiGr, 과충전 Li 도금) · 25 °C · 2전극.

### 1. 제조 ↔ 운전 — 이 페이지의 두 축이 다시 갈린다

| | 값 (`[인쇄]`) | 장치 |
|---|---|---|
| 제조 | SE 150 · 셀 380 MPa(펠릿) · **WIP 450 MPa · 75 °C · 15 min**(파우치) | 프레스 · 등방압 |
| 운전 — 펠릿 | **20 MPa**(N/P 0.15 · 양극 20 mg cm⁻²) · **3 MPa**(N/P 0.66 · 6 mg cm⁻²) | 스프링 — "specific spring constant", **상수 · 변위 · 계측 0** |
| 운전 — 파우치 20 × 20 mm² | **3 MPa**(N/P 0.6) | PEEK 판 + 볼트 넷 3.5 N·m — 변환 0 |
| 운전 — 반쪽전지 | **미인쇄** | — |

`[재현]` 표준 체결식(K ≈ 0.2)이면 M6–M10 볼트 넷의 체결력은 전극 면적 4 cm² 기준 **≈17–29 MPa** — 3 MPa 는 판 전체 면적 기준이거나 따로 교정했어야 한다(볼트 규격 · 판 면적 미인쇄, 우리 계산). 5호(로드셀)와 대비되는 **압력 계측 0** 편이다.

### 2. ★★★ 두 압력은 교락된다 — 압력 → 용량의 표본이 아니다

20 → 3 MPa 에서 양극 적재 ×1/3.3 · N/P ×4.4 · 음극 Li 몫 0.85 → 0.34 가 같이 바뀐다. `[도표]` 0.2C 첫 방전 ≈170 → ≈115 mAh g⁻¹(−32 %) — 양극이 얇아졌는데도 준다는 방향은 25호(30 → 2 MPa 공통 −26.5 ↔ −30.7)와 같다. 그러나 **같은 3 MPa · 같은 양극에서 Li 10 µm 가 ≈140** 을 내므로 비용의 일부는 MgSiGr 음극 자신이다. 유지율 83.7 %(20 MPa) ↔ 64.7 %(3 MPa)도 같은 교락 위에 있다.
⇒ **저자의 "most critical factor" = 음극 계면 안정성은 3 MPa 고정 음극 교체(SiGr · Li · MgSiGr)로 얻은 명제다** — 압력을 움직인 측정이 아니다. MgSiGr 저압 감쇠의 원인 문장("volume changes during overcharging, especially under low stack pressure")은 측정 0.

### 3. ★★ 아래 벽의 증상이 CE 로 나타난다 — 그리고 CE 는 적재로 정규화해야 한다

`[도표]` 3 MPa MgSiGr CE ≈85–97 %(본문 무언급) ↔ 20 MPa 평균 99.2 %(`[인쇄]`). `[재현]` 면적당 결손으로 바꾸면 ≈0.046 ↔ ≈0.025 mAh cm⁻² 사이클⁻¹ — **×≈1.8**; CE 로 본 ×≈7 의 대부분은 양극 적재 차다. 3 MPa 누적 결손(≈575 mAh g⁻¹)은 양극 Li 재고의 ≈2 배라 **Li 손실이 아니다** — 저압 쪽 결손은 누설(저자 S17 의 연성 단락 병렬 경로) · 부반응 쪽이다([[anode-free-li-inventory-accounting]] 52호 절). `[해석]` 저압이 아래 벽(접촉 손실)만이 아니라 **단락 누설**로도 나타날 수 있다는 후보 — 5호가 위 벽(고압)에서 본 단락과 다른 자리.

### 4. 요구치 · 이력

- 3 MPa 는 33호 띠(0.4–5 MPa) 안 · 33호 산업 "< 2 MPa" 위 · 25호 2 MPa 보다 위 — **띠의 아래 끝을 새로 내리지 않는다.** 요구치 인쇄는 없다("impractically high stack pressure" · "practically viable conditions" — 값 0).
- 380 MPa 제조 → 운전으로 내린 절차 미기재 — 25호와 같은 **하강 분기**.

### 5. 이 편이 이 페이지에 **안 준 것**

압력 스윕 · 압력 계측 · 사이클 중 압력(20 MPa 셀은 `[재현]` 사이클당 도금 ≈15 µm) · 반쪽전지 압력 · 양극 쪽 어떤 관측 · 조건당 반복.

## ★★ 2026-09-28 (`assb` 59호 Li Q. 2025, **Perspective · 1차 측정 0 · Source Data = Fig. 1b 원자료**) — **"정본 후보" 가 요구치를 `<0.1 MPa` 로 적어 "≈1–5 MPa 수렴" 이 무너지고, 창 전체를 CE 한 곡선(CSP)으로 그리지만 수치는 0 이다**

`raw/papers/li2025_stack-pressure-critical-importance-perspective.md` (*Nat. Energy* 10, 1064–1073, 북경이공대 — 13호 [23], **3차 묶음 파일 21**).
13호 절(§1)이 "Q6 요구 창의 정본 후보" 로 남긴 편이다.

### 1. 요구치 — 일곱 번째 인쇄, 원전 0 ⇒ 13호 절의 "독립 수렴" 은 서지 않는다

| 편 | 요구치 | 원전 |
|---|---|---|
| 8호 | < ≈1 MPa | Xu 2024 (확인 편 0) |
| 12호 | 0.4–1 MPa | Tian & Qi 2017 / Shao 2022 (미확정) |
| 13호 | < 5 MPa | [35] · [45] (미열람 — [45] 는 3차 묶음 파일 22) |
| 25호 | ≤ 5 MPa | 없음 |
| 33호 | < 2 / ≤ 2 MPa | 없음 ("To our knowledge") |
| 39호 | 1 MPa | Wang · Kazyak · Dasgupta · Sakamoto *Joule* 2021 (미열람) |
| **59호** | **< 0.1 MPa** — `[인쇄]` "driven by practical considerations (typically requiring a pressure of <0.1 MPa)" | **없음** |

- 이 편은 1–5 MPa 를 **요구치로** 인쇄하지 않는다. `[인쇄]` SSB 실험실 필요치 = "several to hundreds of MPa" · "at least 20 MPa"(Li 석출 공극률 · 비활성 Li) ·
  "above 10 MPa … limit practical viability"(입계 덴드라이트, Albertus 2021). 5 MPa 는 인용 프로토콜 "25 MPa SSE/Li interfacial formation pressure before
  reducing to 5 MPa for cycling"[36] 한 번. 그리고 `[인쇄]` "0.1 to a few MPa" 는 이 편 지도에서 **액체 LMB** 대역이다.
- ⇒ **일곱 편 · 여섯 값(0.1 · 0.4–1 · ≈1 · 1 · 2 · 5) · 확인된 원전 0 · 띠 0.1–5 MPa(×50).** "원전 셋" 중 처음 열어 본 다리([23])가 띠 밖이고 그 자신도
  원전이 아니다. 13호 자신은 `<5` 에 [35] · [45] 를 달았다 — 13호 오귀속이 아니고, [23] 을 요구치 원전 줄에 같이 적었던 것은 우리 13호 digest 대조표다.
- `[해석]` `<0.1 MPa` 는 이 편 자기 원자료의 **LIB 범주(0.01–0.1 MPa)** 와 겹친다 — "실용" = LIB 모듈 수준 압력으로 정의한 것으로 읽힌다.
  Fig. 1b 의 "Future target — Low or zero pressure" 별표도 `[도표]` ≈0.03 MPa.

### 2. ★★ 문헌 운전 압력 원자료 — 계보 첫 수록, 단 그림 점은 원자료와 다르다

Source Data xlsx(시트명 'Figure 5' · 머리 셀 "Figure. 1b" — **Fig. 5 원자료는 없다**) `[데이터]`:

| 범주 | n (출처 편) | 범위 · 중앙 (MPa) | 메모 |
|---|---|---|---|
| LIBs | 7 (6) | 0.01–0.1 · 0.05 | 파우치 압축 · 팽창 문헌 |
| Liquid-state LMBs | 9 (8) | 0.69–1.4 · 1.1 | 무음극 파우치 포함 |
| Solid-state LMBs | 13 (13) | 5–400 · 45 | ≥50 MPa 6 · ≤5 MPa 1 · 1–2 MPa 0. 제목상 Li 금속이 드러나지 않는 행 6(Ni-rich 양극 · Li-In/Sn 음극 · 시뮬 1 포함) — 사실상 SSB 전반 |

- ⚠ `[도표]` 화소 판독한 Fig. 1b 의 점은 이 원자료와 **다르다** — 액체 LMB ≈0.34–2.5 MPa(원자료 0.69–1.4), 고체 가운데 순위 −25 … −33 % (59호 D1).
  **값은 원자료로만 옮긴다.**
- `[해석]` 33호 D4("most labs 50–600 MPa", 출처 0)와 대조: 59호 원자료의 고체 13 값 중앙은 **45 MPa**, `[도표]` Fig. 5b 의 Li 전체 상자는 ≈1–34 MPa(위 수염 ≈75) —
  59호의 집계도 "대부분 50 MPa 이상" 을 받치지 않는다. 다만 원자료에 시뮬 편 · 비-Li 금속 편이 섞여 있고 Fig. 5 는 원자료가 없다.
- 운전 압력 표본(이 페이지)에 붙는 것: Koerver 2018 *EES* 가 **143 MPa**(59호 원자료) ↔ **70 MPa**(33호 Table 1) — 같은 원전의 두 인쇄값, 원전 미열람.

### 3. ★★ CSP — 창 전체를 CE 한 곡선으로, 수치 0

- `[인쇄]` "Based on our statistical analysis, we propose a CSP empirical model" — 액체 LMB: L1(상승) → CSP_L → L2(평탄 = 최적) → L3(실패);
  고체 LMB: **S0**(작동 개시에 필요한 높은 초기 압력, CSP_S1) → S1(상승) → CSP_S2 → S2(평탄 = 최적) → S3(실패). `[도표]` Fig. 5c 두 축 **눈금 0**.
- 이 페이지의 틀로 옮기면: S0/S1 = **아래 벽**(접촉 손실), S3 = **위 벽**(이 편은 집전체 파단 · 전극 균열 · 분쇄 · Li 변형 · SSE 피로 · 덴드라이트 단락을 한 줄로
  나열 — Fig. 4), S2 = 창. ⚠ 그러나 **창의 값이 하나도 없고**(CSP_L · CSP_S1 · CSP_S2 수치 0), 경험 근거라는 Fig. 5a/b 는 CE · 압력의 **주변 분포**라
  CE(P) 를 주지 않는다. "validation" 인용 둘은 양극 압력 **모델**(Naik 2024)과 **Na** 계(Spencer Jolly 2019).
- `[인쇄]` 측정법 "continuously measuring the Coulombic efficiency … while gradually increasing the stack pressure, the minimum stack pressure that yields the
  highest Coulombic efficiency" — `[해석]` §"이력"(5호: 처녀 5 MPa 110 Ω ↔ 25 MPa 를 찍고 내려온 5 MPa 50 Ω) 아래서 이 "최소 압력" 은 **가압 분기의 값**이다.
  감압 분기(고압 형성 뒤 운전 — 25 · 33 · 52호의 "고압 제조 · 저압 운전" 모양)의 최소 압력은 더 낮을 수 있다. 그리고 CE 는 Li 재고 손실 · 양극 고립 · 누설
  (41 · 52호)을 한 비로 합친다 — 창의 아래 끝을 CE 로 정하면 **무엇이 막혔는지**가 사라진다.
- 인용 기준 하나(`[인쇄]` "stack pressure (P)/current density (I) > 25 MPa cm⁻² mA⁻¹", **SSE/양극 계면**, [27] 모델): `[재현]` 단위를 MPa cm² mA⁻¹ 로 읽으면
  1 mA cm⁻² 에 25 MPa · 13호 그리드 5 mA cm⁻² 에 125 MPa · 이 편 실용 목표 0.1 MPa 에서 허용 0.004 mA cm⁻² — **이 편의 두 명제가 서로 맞지 않는다**(조정 0).

### 4. ★★ 위 벽 "피로" 의 하중 형태 — 계보 안에서 반대로 적힌다

| | 59호 (13호 [23]) | 13호 (§5 · §4) |
|---|---|---|
| 피로를 만드는 하중 | `[인쇄]` "**fluctuations** in stack pressure at the MPa level can induce mechanical fatigue in the SSE"[39] · Fig. 4m "continued pressure fluctuation" | `[인쇄]` "**high, constant** stack pressure can induce … fatigue-driven micro-crack initiation" |
| 처방 | 압력 **일정 유지**(Fig. 6c "Maintain constant", Now 진동 → Future 평평) + 압력 **신호로 운전 조절**(`[인쇄]` "Battery operation can therefore be dynamically regulated adaptively from the feedback of stack pressure") | 압력을 **조작 변수**로 — 율↑ → P↑ · 휴지 · 노화 → P↓ |
| 근거 | [39] = **5호 Doux 2020** — 5호 digest 의 균열은 75 MPa **정압** "severe cracking", `fatigue` · `fluctuat` 명제 없음(digest 기준) | 인용 0 · 데이터 0 |

`[해석]` 59호의 기구(요동 → 피로)를 받으면 13호의 변조 정책은 피로의 구동 하중을 **늘린다**. 두 편 모두 근거가 비어 있으므로 이 페이지의 두 번째 위 벽은
**"피로, 하중 형태 미정"** 으로 둔다. 그리고 §"압력 진동"(33호 — 상대극이 만드는 사이클당 ≈0.7–2.3 MPa)은 59호 기구가 맞다면 운전 중 **저절로** 가해지는 요동이다.

### 5. 이 편이 이 페이지에 **안 준 것**

압력의 함수 — `θ(P)` · `R(P)` · 용량(P) · CE(P) 어느 것도 1차 자료 0(CE(P) 는 개념 곡선) · 이력 0(`hysteres*` · `histor*` 0) · 압력 계측 장치의 정확도 0 ·
공간 분포 실측 0(식 (2)(3)만 — 범위 정규화라 척도 불변, `[재현]` 한 점 +10 MPa 핫스팟이 "균일" 판정; 59호 digest D8). **창의 값은 하나도 움직이지 않았다.**
움직인 것은 **요구치 띠의 폭**(0.4–5 → 0.1–5 MPa)과 **"수렴" 판정**(반박)이다.

## ★★ 2026-09-28 (`assb` 60호 Zhang 2025, **Article · Si 이중층 음극 · 운전 외압 0 · Source Data 14 시트**) — **13호 `<5 MPa` 의 마지막 인용 다리가 "5" 를 주지 않고, "외압 0" 은 프레임을 뺐다는 뜻이며, 정변위면 Si 팽창이 ≈1.5 MPa 를 스스로 만든다**

`raw/papers/zhang2025_pressure-free-si-li21si5-double-layer-anode-assb.md` (*Nat. Commun.* 16, 1013, 샤먼대 — 13호 [45], **3차 묶음 파일 22**).

### 1. 요구치 — 여덟 번째 인쇄값이 아니라 "인쇄값 0"

- `[인쇄]` 본문 `MPa` 15 회 = 70(Li 금속 "suitable", [7–9]) · 370(Si "required", [10–13]) · 600 · 370 · 350(제조) · 0.8 · 1.51(정변위 지그). SI 8 회 = 100–700(S3 제조 스윕) + Table S2 열. **요구치 · 문턱 · 창 0.**
- Table S2 "External pressure (Mpa)" 열 `[인쇄]`: 20 · 2 · 70 · 20 · 75 · 20 · 2 · **5**(ref 22 = 5호 Doux 2020, Li/NCA · 0.05 mA cm⁻² · 0.5 mAh cm⁻² · 100 사이클 · 25 °C) · **0**(Chen 2018, Si/garnet · 0.008 mA cm⁻²) · 50 · 50 · 50 · 15 · **0**(this work).
- ⇒ 계보 표는 **일곱 편 · 여섯 값 · 0.1–5 MPa · 확인된 원전 0** 그대로. 13호 `<5` 의 세 인용 중 둘이 비었다:

| 13호 인용 | 편 | "5" 를 주는가 |
|---|---|---|
| [23] | 59호 Li Q. 2025 | ❌ `<0.1 MPa`(인용 0) |
| [45] | **60호 Zhang 2025** | ❌ 인쇄 0 · Table S2 의 5 = 5호 조건 |
| [35] | Li Menglin *AFM* 2025 | 미수령 — 원장 §1 에 없음 |

### 2. ★★ 제작 압력 ↔ 운전 압력 — 실험 편 두 번째 "운전 외압 0" 표본, 그러나 경계조건이 없다

| | 제조 | 운전 | 조건 | 결과 |
|---|---|---|---|---|
| 6호 Lee 2020 | 490 MPa(WIP) | 2 · 3 · 4 · **0** | 0.1 C(0 은 0.1 C 만) | 300 사이클 |
| **60호 Zhang 2025** | **600**(음극 냉간압착 소결) · **370**(이중 SE) · **350**(셀) | **외압 0**(S1b 프레임 없는 다이 셀) | **2.5 mA cm⁻² · 2.8 mAh cm⁻² · 45 °C · N/P 6.7** | `[데이터]` 1000 사이클 −45 %(1 사이클 기준; 인쇄 "54.9 %" 는 2 사이클 기준) · EIS ×3.2 |

- ⚠ **G1 — 운전 중 구속 미명시**: 플런저가 자유(정하중 ≈ 자중)인지 캡으로 두께가 고정(정변위)인지 Methods 에 없다. 6호 G12 · 11호(볼트 · 너트 "constant")와 같은 구멍이 **세 번째**다.
- **같은 편의 S14 가 그 구멍의 크기를 보인다**: 별도 정변위 지그(`[인쇄]` "minimum pressure load (0.8 MPa) … to limit the thickness")에서 첫 충전 **+1.51 MPa**(`[인쇄]`), 이후 0.56 mA cm⁻² 4 사이클 `[도표]` ≈1.2 → 1.05 MPa, 방전 말 기저 복귀(래칫 0, 5 사이클). ⇒ 본편 셀이 정변위였다면 자체 압력 ≈1–1.5 MPa 아래서 돈 것이고, 자유였다면 두께가 늘며 돈 것이다 — **지면이 갈라 주지 않는다**.
- `[해석]` §"압력 진동"(33호 — 상대극이 만드는 ≈0.7–2.3 MPa/사이클)의 **Si 완전지 1 차 표본**. 진폭이 줄어드는 것은 가역 팽창 감소 · 지그 순응 · SEI 성장 어느 것인지 5 사이클로 못 가른다.

### 3. 아래 벽의 정성 표본 — 무압 · 45 °C 에서 Li 금속 음극은 2 사이클에 soft short

`[도표]` S13: Si–Li₂₁Si₅ 75 wt%(ICE 73.4 %) · Li₂₁Si₅(82.99 %) · **Li 금속(89.27 %)** 셋 다 2 사이클 충전이 4.0 V 평탄으로 달린다(2.8 mAh cm⁻² · 45 °C · 무외압). 5호 아래 벽(저압 → 접촉 손실 → 덴드라이트)과 같은 방향이지만 압력 값이 없어 창에 놓지 않는다. 이중층만 살아남는 것이 이 편의 명제 — 단 압력 대조군이 없어 "압력 대신 설계" 의 등가는 보이지 않았다(G2).

### 4. 압력 함수 — 제조 축만

S3: Li₂₁Si₅ 분말 100 → 700 MPa 냉간압착에서 면저항 **4.71 · 1.15 · 0.35 · 0.25 · 0.11 · 0.05 · 0.05 Ω/sq**(전자 전도, 소결). 운전 압력 → `θ` · `R` · 용량 · CE 함수 **0** · 이력 0 · 계측(본편 셀) 0. 이 페이지의 창 값은 **하나도 움직이지 않았다**.

### 5. 이 편이 이 페이지에 **안 준 것**

압력 대조군(같은 음극의 가압 판은 자기 인용 Zhang 2024 *EES* 50 MPa 뿐, 미열람) · 운전 중 압력 계측(본편 셀) · 경계조건 · 요구치 · 양극 쪽 어떤 관측.

## ★★★ 2026-09-28 (`assb` 61호 Masias 2019, **재료 실측 · 벌크 Li 원통 · 실온 · 셀 0**) — **창의 두 벽 사이(0.1–5 MPa)가 Li 의 눈금으로는 확산 creep · 멱법칙 creep · 항복 · power-law breakdown 을 가로지르고, "항복을 넘어 creep" 은 이 편이 주지 않는다**

`raw/papers/masias2019_elastic-plastic-creep-mechanical-properties-lithium-metal.md` (*J. Mater. Sci.* 54, 2585–2600, Ford/미시간 Sakamoto — 21호 ref 49 · 5호 ref 15, **3차 묶음 파일 23**).
이 페이지 §정의의 "항복강도(≈0.8 MPa)" 와 §5호 표의 "Li 항복강도 대비" 열이 기대는 원전이다. 수치의 정리는 [[li-metal-yield-creep-vs-stack-pressure]].

### 1. 요구치 — 여덟 번째 인쇄값, 그리고 계보에서 가장 이른 것(2018)

| 편 | 요구치 | 원전 |
|---|---|---|
| **61호 Masias 2019** | **"stack pressures in the 1.0 MPa range are necessary to achieve low and stable cell resistance"**(서론) · "0.8–2.4 MPa … anticipated stack pressures that are required"(방법) · **"How much compressive stress is not known … We believe 1 MPa was sufficient"**(결과) | **[9] Sharafi … Sakamoto 2016 *JPS* 302, 135 · [10] Wang & Sakamoto 2018 *JPS* 377, 7**(미열람 — 같은 실험실) |
| 8 · 12 · 13 · 25 · 33 · 39 · 59호 | (§59호 표) | |

- ⇒ **여덟 편 · 여섯 값(0.1 · 0.4–1 · ≈1 · 1 · 2 · 5) · 띠 0.1–5 MPa 그대로 · 확인된 원전 0 그대로.** 새것: 가장 이른 인쇄 · "necessary" 와 "not known" 이 같은 지면(61호 D10) · 원전이 **자기 실험실 두 편**.
- `[해석]` "≈1 MPa" 가닥(이 편 · 39호 Wang 2021 *Joule* · 8호 재인용)이 Sakamoto 실험실 2016–2021 **한 뿌리**일 가능성 — 원전 넷 중 열어 본 것이 이 편뿐이라 가설. 46호(Schlenker 2020)는 [10] 을
  "Li 항복 2 MPa" 로 전사했고 이 편은 0.73–0.81 — 같은 실험실의 두 인쇄값이 2.5× 다르다(원전 미열람).

### 2. ★★★ 창의 재료 눈금 — 이 페이지의 값들을 Li 위에 놓는다

`[인쇄]` E 7.82 · G 2.83 GPa · ν 0.381 · 항복 **0.73–0.81 MPa**(인장 0.2 % 오프셋; 압축 변곡 0.81 ± 0.10) · 인장 creep **0.2–0.6 MPa(항복 아래)** 에서 power-law `n` = **6.56**(Table S1: 2.0×10⁻⁷ → 3.89×10⁻⁴ s⁻¹) ·
[32] 지도 경계 σ/G 10⁻⁴(확산 creep) · 10⁻³(power-law breakdown) → `[재현]` **0.28 · 2.83 MPa**.

| 이 페이지의 값 | MPa | Li 눈금 | `[재현]` 멱법칙 1 % 변형 시간 |
|---|---:|---|---|
| 59호 요구치 | 0.1 | 확산 영역(시험 밖) | ≈55 일(하한) |
| 61호 인장 creep | 0.2–0.6 | 측정 | 14 h → 26 s |
| **항복** | **0.73–0.81** | | ≈10 → 5 s(외삽) |
| 60호 지그 예압 · 61호 압축 하한 | 0.8 | 항복 자리 | |
| 61호 기준값 · 8호 · 39호 · 5호 아래 벽 최저점("exceeds 500 Ω") | 1 | "we believe sufficient" · 항복 바로 위 | ≈1 s(외삽) |
| 4호 · 33호 · 6호 | 2–4 | 압축 시험 범위(0.8–2.4) 안팎 | ms(외삽) |
| 60호 첫 충전 총 | ≈2.3 | 압축 상한 근처 | |
| **breakdown 경계** | **2.83** | σ/G = 10⁻³ | (그 위 외삽 무효) |
| 5호 운전 · "optimal" · 13호 <5 | 5 | breakdown · 항복 6× | |
| 5호 위 벽 | 10–75 | 항복 13–94× | |

- `[재현]` 0.1 → 5 MPa 는 멱법칙으로 creep 속도 ×1.4×10¹¹; 외삽이 유효한 0.28–2.83 만 잡아도 ×3.8×10⁶. **압력 ×50 이 Li 시간 척도 6–11 자릿수**다.
- `[해석]` 이 페이지의 아래 벽(5호 1 → 5 MPa 에서 임피던스 > 500 → 110 Ω)은 Li 가 항복 바로 위에서 압축 시험 범위를 지나 breakdown 경계로 넘어가는 구간과 겹친다 — 접촉이 "creep 으로 만들어진다" 는
  읽기가 가능한 자리이지만, 5호 셀은 Li₆PS₅Cl 이고 이 편은 SE 0 이다. 위 벽(10–75 MPa)은 전부 breakdown 영역 — 5호가 잰 단락 시간(474 h → 0 h)은 멱법칙으로 설명할 범위 밖이다.

### 3. ⚠ 정정 — "항복강도를 넘어 크리프" 는 이 편이 주지 않는다

- §정의 · 5호 digest :205 "항복강도 ≈0.8 MPa, 그 위에서 크리프 시작" ↔ 이 편 `[인쇄]` "Tension creep performance was studied at loads **below** the 0.8 MPa yield point between 0.2 and 0.6 MPa" — creep 은
  항복 아래에서 쟀고 `n` = 6.56 도 거기서 나왔다. 정정: **"creep 속도가 σ^6.56 로 커진다 — 항복(0.8) 근처에서 1 % 변형이 초 단위가 된다"**(§정의 아래 주석).
- 항복 위(0.8–2.4 MPa)의 시간 의존 변형은 이 편에서 **마찰 · 배럴링이 지배**(응력 ↑ 에 속도 ↓ — 0.8 → 2.4 MPa 에서 12 분 속도 ×0.21, Fig. 9)해 재료 법칙이 아니다(저자 인정) — 위 벽의 "creep 관통" 을
  이 편의 압축 값으로 정량화할 수 없다.

### 4. ★★ 시간 축 — 압력은 걸고 얼마 뒤에 잰 값인가

- `[인쇄]` 압축 시험의 세 시각 12 · 60 · 120 분 = "a LMSSB charged or discharged in 12, 60, and 120 min" — 같은 응력에서 속도가 720 → 7200 s 에 ×1/15–1/21. `[해석]` 셀에서는 이것이 **재가압 뒤
  유지 시간**의 문제다: [[assb-pressure-reapplication-separation-test]] D1 에 유지 시간 · 회복 시간 곡선을 붙인다(61호 절). §"압력 진동"(33호 — 사이클당 ≈0.7–2.3 MPa)은 이 편의 눈금으로
  **항복을 매 사이클 넘나드는** 진동이다 — 피로 · 래칫은 이 편에 0(61호 G10).

### 5. 이 편이 이 페이지에 **안 준 것**

셀 · SE · 계면 저항 · `θ(P)` · 이력 · 온도 의존(`Qc` 0) · 반복 하중 · 접착 계수 · 도금 Li. **창의 값은 하나도 움직이지 않았다** — 움직인 것은 §정의의 기구 문장(정정)과 값들의 **눈금**이다.

## ★★ 2026-09-28 (`assb` 62호 Zhang W. 2017, **실험 · In ‖ LGPS ‖ LCO + LTO 대조 · in situ 압력 · 운전 기저 ≈62 MPa**) — **운전 중 압력 변화의 첫 실측은 창의 값을 주지 않는다: 운전 압력은 본문에 없고, ΔP 는 기저선 · 지그 · 음극이 정한다**

`raw/papers/zhang2017_in-situ-pressure-electrochemical-expansion-assb.md` (*J. Mater. Chem. A* 5, 9929–9936, JLU Giessen(Zeier · Janek) + HZB — 22호 ref 18 · 23호 ref 40 · 33호 [89] · 59호 ref 23, **3차 묶음 파일 24**).
신호의 분해(음극 지배 · 강성 곱 · 기저선 규약)는 [[assb-operando-pressure-signal-attribution]].

### 1. 요구치 — 인쇄 0

- `[인쇄]` "external confinement is of paramount importance in preventing cell bending and maintaining cathode/SE contact" — 값 0. 본문 `MPa` **1 회**("1.25 MPa" — ΔP) · `stack pressure` **0**. ⇒ 요구치 띠(여덟 편 · 0.1–5 MPa) · 확인된 원전 0 **그대로**.

### 2. ★★★ 운전 압력 — 창의 표본으로 쓸 수 없는 이유

- 운전 기저는 `[도표]` ESI S7 세로축 **≈61.8 MPa**(61.83 → 60.63 MPa / 110 h)에만 있다 — 본문 0. 같은 연구망 22호(55 MPa) · 23호(≈70 / 64 MPa)와 같은 자릿수다. 조립은 3.5 t · 1.5 t(`[재현]` ∅10 mm 로 437 · 187 MPa) ·
  CT/XRD 펠릿은 등방 4000 bar.
- 무가압 대조(딜라토미터 · X-CT)는 **다른 셀**이다 — 이용률 `[재현]` ≈8 %(무가압, 11.4 mAh g⁻¹) ↔ ≈85 %(≈62 MPa, 116.7 mAh g⁻¹) 는 SE 두께 · In 지름 · 전류(28 ↔ 146 µA cm⁻²) · 장치가 같이 바뀐 대조다 —
  창의 아래 벽 표본으로 옮기지 않는다.

### 3. ★★★ §압력 진동의 원형 — 그러나 크기는 셀의 성질이 아니다

- In ‖ LCO: 원시 충전 상승 `[도표]` +1.07 → +1.13(0.1 C) · +1.00–1.05(0.25 C) MPa · 보정 1.25(인쇄) ↔ LTO ‖ LCO ≈0.067 ⇒ 상대극 몫 `[재현]` ≈90–95 %. 33호 재수록 표본(상대극 ≈0.5–2.3 · 양극 ≈0.05–0.07 MPa)과 같은
  그림 — 그리고 같은 관행(기저는 본문에 없다).
- `[재현]` ΔP 를 셀 탄성만으로 내려면 유효 길이 ≈22–36 mm(인쇄 SE 탄성률 18–25 GPa · ESI ⅓ 규칙 두께) ⇒ 크기는 지그 순응 · 공극 압밀이 정한다 — 60호 S14(+1.51 @ 0.8 MPa)와 **같은 눈금이 아니다**.
- 원시 기저 표류 **−1.2 MPa / 110 h**(한 사이클 진폭과 같은 크기) — 시간당 ≈0.02 → 0.009 MPa h⁻¹ 로 준다. §이력(5호)과 같은 종류의 경로 의존이 **운전 중에** 있다는 표본 — 원인(압밀 · In 흐름 · 장치 이완)은
  가를 대조가 없다. 이 편은 방전 말 골을 잇는 기저선을 빼 이 표류를 그림에서 지웠다.

### 4. 61호 눈금으로

- 기저 ≈61.8 MPa = Li 항복(0.73–0.81)의 ≈80× · σ/G ≈2.2×10⁻²(breakdown 영역) — 이 셀은 In 이라 Li 눈금 밖이다. 이 편의 "Li 금속이면 ≈2.2 µm" 는 ⅓ 규칙을 평면 석출에 곱한 값(`[재현]` 6.7–9.4 µm).

### 5. 이 편이 이 페이지에 **안 준 것**

요구치 · 운전 압력 값(본문) · 지그 강성 · 기저선 정의 · 압력 스윕 · 압력 → 용량(구속 셀 1 점 — 무가압 셀은 다른 셀) · 셀 수. **창의 값은 하나도 움직이지 않았다** — 움직인 것은 §압력 진동의 원형 표본과,
ΔP 를 옮길 때 붙일 단서 셋(**기저 · 구속 형식 · 기저선 규약**)이다.

## ★ 2026-09-28 (`assb` 63호 Zhang W. 2017 *ACS AMI*, **실험 · In ‖ LGPS ‖ LNTO-LCO · 23호의 방법 원전 · 62호 [27]**) — **운전 구속은 나사 토크 10 N·m 하나이고 MPa 는 없다: 23호의 64 / 70 MPa 는 이 편 값이 아니다**

`raw/papers/zhang2017_interfacial-eis-cathode-composition-lco-lgps-assb.md` (*ACS Appl. Mater. Interfaces* 9, 17835–17845 — 22호 ref 16 · 23호 ref 29 · 24 · 39 · 41 · 42호, **3차 묶음 파일 25**).

### 1. 요구치 — 인쇄 0

`pressure` 4 회 · `MPa` **0 회**(본문 · SI). 요구치 · 문턱 0 ⇒ 띠(0.1–5 MPa) · 확인된 원전 0 **그대로**.

### 2. ★★ 운전 압력 — 토크만 있다

- `[인쇄]` "constant pressure was applied to the cell using the screw … of the aluminum framework with 10 N m torque, which was kept constant during the electrochemical tests" · S3 "Screw fixed with 10 Nm torque" · 하중계 · 스프링 0.
- `[재현]` `F = T/(K·d)` — K 0.15–0.25 · M8–M12 가정이면 **3.3–8.3 kN = 42–106 MPa**(0.785 cm²). 23호가 같은 절차를 "previously described" 로 빌리며 적은 "5 kN (64 MPa)" · "approximately 70 MPa" 는 K·d = 2 mm(예: K 0.2 · M10)면 맞지만 **23호 자신의 값**이다. 52호(스프링/파우치 토크 — 교정 근거 없음)와 같은 부류.
- ⚠ 같은 지면이 "kept constant" 와 "The pressure change of the model SSB during cycling has been in situ observed"([43] = 62호)를 둘 다 적는다 — 나사 고정은 변위 구속이고, 62호의 같은 모델 셀은 운전 중 ≈1–1.3 MPa 로 움직였다.
- 제조 3.5 t · 1.5 t × 2 min(`[재현]` 437 · 187 MPa) · X-CT 하우징은 Al 프레임 없음(구속 0).

### 3. 이 편이 이 페이지에 **안 준 것**

요구치 · MPa · 스윕 · 압력 → 용량. 창의 값은 움직이지 않았다 — 움직인 것은 같은 연구망 셀들의 운전 압력 계보가 **"토크 · 힘 · 기저 중 하나만 인쇄"** 로 한 줄 더 채워졌다는 것이다(22호 55 MPa · 23호 5 kN(64) / ≈70 MPa · 62호 ≈61.8 MPa(그림 축) · 63호 10 N·m).

## ★ 2026-09-28 (`assb` 65호 Nam, Oh, Jung, Jung 2018 *JPS*, **실험 · 반쪽 PEEK ∅13 mm · 펠릿 · 파우치 80 × 60 mm²**) — **압력은 제조값 셋뿐이고 운전 압력은 0 이다: 파우치는 492 MPa 제조 뒤 사진에서 바인더 클립 둘로 집혀 있다**

`raw/papers/nam2018_dry-vs-slurry-mixed-electrodes-binder-gitt-coverage.md` (*J. Power Sources* 375, 93–101 — 22 · 39 · 57호 지목, **3차 묶음 파일 27**).

### 1. 요구치 — 인쇄 0

`pressure` **0 회** · `MPa` 3 회(전부 제조). 요구치 · 문턱 0 ⇒ 띠(0.1–5 MPa) · 확인된 원전 0 **그대로**.

### 2. ★ 운전 압력 — 없다

- `[인쇄]` 제조: SE 전도도 펠릿 370 MPa · 반쪽 · 펠릿 완전지 "all the assembled components were pressed at 370 MPa in a PEEK (polyether ether ketone) mold (diameter of 13 mm)" · 파우치 "sealing … in a pouch, and pressing subsequently at 492 MPa". 운전 구속(지그 · 토크 · 하중) 서술 **0**.
- `[도표]` Fig. 8c(가위로 자른 파우치가 LED 를 켠다)와 초록 그래픽의 파우치는 **바인더 클립 둘**로 집혀 있다 — 가압 정량 0. Fig. 8d(111 °C 핫플레이트)에는 클립이 안 보인다. `[해석]` 이 파우치를 "무가압 운전" 으로도 "가압 운전" 으로도 인용할 수 없다 — 안전 시연(절단 · 가열)도 압력 조건 없이 인쇄됐다.

### 3. 이 편이 이 페이지에 **안 준 것**

요구치 · 운전 MPa · 스윕 · 압력 → 용량. 창의 값은 움직이지 않았다 — 움직인 것은 "제조 압력만 인쇄하고 운전은 사진이 대신한다" 는 한 줄이다(63호 "토크만" · 64호 "≈70 MPa 한 값" 에 이어).

## ★ 2026-09-28 (`assb` 73호 Minnmann 2021 *JES* 168, 040537, **실험 · 차단 셀 EIS + In/(InLi)ₓ 반쪽 · PEEK ∅10 mm · 무탄소 NCM-622 \| Li₆PS₅Cl**) — **측정 압력 ≈40 MPa 를 힘 센서 + 스프링(이완 보상) 장치로 인쇄한 표본 — 사이클 셀의 구속 형식은 없고, 압력 스윕 · 압력 → 전도도 · 용량은 0**

`raw/papers/minnmann2021_charge-transport-bottlenecks-tlm-ncm622-lpscl.md` (24 · 50 · 56호 지목 · 02호 Fig. 3 원자료, **3차 묶음 파일 35**).

### 1. 요구치 — 인쇄 0

`pressure` 8 회 · `MPa` 6 회(380 · 100 · 40 MPa). 요구치 · 문턱 0 ⇒ 띠(0.1–5 MPa) · 확인된 원전 0 **그대로**.

### 2. ★ 제조 ↔ 측정 · 운전 — 값은 있고 스윕은 없다

- `[인쇄]` 제조: 복합체 100 mg "380 MPa for 3 min at room temperature" · 이온 전도도 셀은 그 펠릿을 풀어 SE ≈60 mg 씩 더하고 "again compacted with a uniaxial pressure of 380 MPa for 3 min"(**두 번 압착** — 전자 셀과 같은 L · 같은 공극 가정을 두 측정에 쓴다) · 반쪽 셀 분리막 100 MPa · 이층 380 MPa × 3 min.
- `[인쇄]` EIS 측정 "A constant pressure of approx. 40 MPa was applied to the pellets during the measurements. A specially designed cell setup comprising a force sensor to adjust the force (and thus the pressure) and a spring to compensate for pressure relaxation caused by elastic deformations of individual components was used" — **정하중(이완 보상) 쪽 구속의 인쇄 표본**(`[해석]` 63호 셀 틀의 나사 토크 서술과 다른 장치 — 이 편은 그 장치의 원전을 달지 않는다; ref 36 = 63호는 PEEK ∅10 mm 셀 케이스에 붙는다).
- `[인쇄]` 사이클 "During cycling, a pressure of about 40 MPa was applied." — 구속 형식(정하중 / 정변위) 미인쇄.
- `[해석]` 24호가 "이 편 방법" 을 따른 EIS 셀은 50 · 150 MPa(제조) — 같은 방법 이름 아래 시편 제조 압력이 다르다([[assb-tortuosity-factor-effective-conductivity-split]] 처방 2).

### 3. 이 편이 이 페이지에 **안 준 것**

요구치 · 압력 스윕 · 압력 → σ · τ² · 용량 · 운전 중 압력 변화. 창의 값은 움직이지 않았다 — 움직인 것은 운전 압력 계보에 "측정 셀은 힘 센서 + 스프링 ≈40 MPa · 사이클 셀은 값만" 이라는 한 줄이다(보류 (하) ① D4 구속 형식의 약한 근거 — 결정 안 함).

## ★★ 2026-09-29 (`assb` 80호 Okasinski 2020 *PCCP* 22, 21977, **실험 + 모형 · 액체 NCM523/흑연 CR2032 코인셀 여덟 구성 · in situ EDXRD 로 두 전극 경계 측면 주사 · ASSB 아님**) — **스택 하중의 면 분포를 기하로 잰 첫 표본 — 코인셀 ≈0.1–0.2 MPa 에서 바닥 전극 판 휨 δ 3.5–15.8 µm · 원인은 설계(오목 캔 위 단순 지지 스페이서) · 요구치 0**

`raw/papers/okasinski2020_edxrd-profiling-coin-cell-uneven-compression-lateral-gradients.md` (24호 ref 36 · SI ref 16 지목 · **3차 묶음 파일 42**).

### 1. 요구치 — 인쇄 0

`pressur` 3 회 · `MPa` 2 회(0.14 · 0.185 — 둘 다 코인셀 하중 추정). 요구치 · 문턱 0 ⇒ 띠(0.1–5 MPa) · 확인된 원전 0 **그대로**. (코인셀 하중이 띠 아래 끝과 같은 크기라는 것은 기록만 — 액체셀 값이다.)

### 2. ★★★ 면 분포 — 값 하나가 아니다

- `[인쇄]` 원인: 바닥 캔이 오목(가운데 간극 <15–30 µm · 셀 1 다이얼 게이지 18 µm) · 바닥 스페이서는 가장자리 접촉선에서만 받친 판 · 스프링 하중에 오목하게 휜다 · "The bottom electrode follows this curvature, while the top electrode remains relatively flat; this causes nonuniform compression of the electrode assembly. The porous separator is pinched near the edge and dilated at the cell center".
- `[인쇄]` 하중 두 추정 0.14 MPa(판 식 · δ ≈10 µm) · 0.185 MPa(스프링 K ≈110 N/mm × Δ 0.27 mm) ↔ `[재현]` 인쇄 식 · 인쇄 값으로 K **92.0 N/mm → 0.157 MPa**(80호 D3) · 스프링 자유 높이는 인쇄 1.4 mm 가 아니라 ≈1.65 mm 에서 "∼16% compression" 과 셀 내부 높이 닫힘이 함께 맞는다(D2).
- `[인쇄]` 표 1 δ **3.5–15.8 µm**(여덟 구성) — `[재현]` 그림 적합이 δ 와 `±` 까지 재현 · 간극 가장자리 16.5–25.2 ↔ 가운데 23–36 µm · 가운데 대비 15–44 %. ⚠ **절대 압축은 셀 절반에서만** — 가장자리 간극이 분리막 공칭 20 µm 아래인 셀은 4 · 6(16.8 · 16.5 µm)이고 7 · 8 은 공칭 크기(19.6 · 19.8), 셀 1 · 2 · 3 은 20.5–25.2 µm 로 공칭보다 넓다(셀 5 는 표 역산 20.1 ↔ 그림 적합 17.8 로 갈린다).
- ★★ **구속 형식 대조**(보류 (하) ① 의 액체판) — 같은 바닥(SS 0.5 mm)에서 스프링(유한 강성 — 정하중 쪽) δ 6.1 · 10.8 ↔ 스페이서 넷(강체 적층 — 정변위 쪽) 3.9 · 6.2 µm · 쐐기는 스페이서 쪽이 크다(`[인쇄]` "it was difficult to avoid wedging of the electrodes") · 스페이서 쪽 하중 추정은 인쇄 0.
- ★ 구성별 판 식 예측(`[재현]`): Al 0.41 mm 스페이서는 판 식 37–44 µm ↔ 측정 15.8 µm(캔 간극에 닿은 쪽 `[해석]`) · 링 심(셀 8)은 판을 가운데 가까이 받쳐 3.5 µm(판 식 밖) · 두꺼운 Al 은 `[인쇄]` "the spring became over compressed".

### 3. ★ 국소 SOC 로 — 측면 `η(r)`

흑연 가장자리 ≈2 mm 띠(면적 50 %)가 ≈0.95C 충전에서 늦고 휴지 수 시간 뒤에도 남는다(다상 — [[assb-apparent-capacity-decomposition]] 80호 절) · 저자 기구 = 가장자리 분리막 공극률 ↓ → 측면 저항 ↑(측정 0 · 모형 Ξ 0.75 가정) · 빠른 충전에서 가장자리 안쪽 고리형 도금(ESI S6 사진 · 모형 그림 10c). `[해석]` ASSB 로 옮기는 것은 크기(코인셀 0.1–0.2 ↔ ASSB 운전 5–62 MPa · ×25–600)가 아니라 **측정 방법**(경계 적합으로 곡률 · 쐐기 · 기울기 분리)과 **사슬 모양**(면 압축 불균일 → 측면 저항 → 측면 `η(r)`)이다 — ASSB 에서는 판 휨 대신 금형 벽 마찰 · 램 기울기 · 펠릿 두께 불균일 · 가장자리 무구속(76호 관찰 면)이 후보다.

### 4. 이 편이 이 페이지에 **안 준 것**

요구치 · 압력 스윕 · 압력 → 용량 · 압력 → 국소 저항 · 분리막 자신의 두께 윤곽 · 반복(구성당 셀 1 · 같은 구성 두 셀 δ ×1.8). 창의 값은 움직이지 않았다 — 움직인 것은 운전 압력을 **값 하나가 아니라 면 분포 · 구속 형식 · 하중 경로로 적어야 한다**는 표본 한 줄이다(보류 (하) 근거 — 결정 안 함).

## ★★ 2026-09-29 (`assb` 81호 Xu 2024 *Adv. Energy Mater.* 14, 2303539, **Review(Editor's Choice) · 1차 측정 0 · 참고문헌 171**) — **8호 "<≈1 MPa" 의 원문: 값은 초록에 있고 출처는 없다 · 이 편의 창은 Li 금속 음극 쪽 두 벽의 재수록이고, 창의 수치는 하나도 정하지 않는다**

`raw/papers/xu2024_pressure-effects-countermeasures-ssb-review.md` (8호 §6.1 · 25호 ref 11 · 33호 [11] 지목 · **3차 묶음 파일 43**). 압력을 **제조 · 조립 · 운전** 세 단계로 나눈 종설이다.
이 편 자신의 압력 서술은 넷(< 1 MPa 요구 · 제조/조립 "hundreds of MPa" ↔ 운전 "dozens of MPa" · "exceeding 10 MPa" · 밀도 98 % — 표 1 요약 행까지 세면 다섯 줄)뿐이고, 나머지 70 행은 전부 재인용이다(digest §(b)).

### 1. 요구치 — 값은 있고 원전은 없다 ⇒ 계보는 독립 인쇄 여덟

- `[인쇄]` 초록 p. 1 "the pressure parameters that are currently employed in laboratory-scale research lack consistency and far exceed the current industrial requirement **(< 1 MPa)**" — 초록은 인용 번호를 달지 않고,
  본문 어디에도 같은 명제 · 출처 · 제조사 · 셀 형식 · 조건이 다시 나오지 않는다(`< 1 MPa` 류 전수 2 적중 — 다른 하나는 Fuchs [140] 한 실험의 조건 "low stack pressure of <1 MPa").
- 8호의 인용은 맞다(값 · 뜻 일치 · "approximately" 는 8호 추가) — 무너진 것은 8호가 아니라 그 아래(이 편 초록)의 근거다.
- `[재현]` 참고문헌 171 편에 계보의 다른 원전 후보 Sharafi 2016 · Wang & Sakamoto 2018(61호 [9] · [10]) · Wang · Kazyak · Dasgupta · Sakamoto 2021 *Joule*(39호 [22]) **0** — Sakamoto 실험실 편
  여덟([7] · [68] = 61호 등)은 인용되지만 "< 1 MPa" 문장에는 붙지 않는다. 61호 절의 "한 뿌리" 가설은 8호 가닥으로는 이어지지 않고, 가설 자체는 열린 채다.

| 편 | 요구치 | 원전 상태 |
|---|---|---|
| 8호 | < ≈1 MPa | **→ 81호의 재인용**(독립 인쇄 아님) |
| 12호 | 0.4–1 MPa | Tian & Qi 2017 / Shao 2022 미열람 — Tian & Qi 2017 은 81호 [71] 로도 인용된다(값 0) |
| 13호 | < 5 MPa | [45] = 60호 ❌ · [35] 미열람 |
| 25 · 33 · 59호 | ≤ 5 · < 2 / ≤ 2 · < 0.1 MPa | 인용 0 |
| 39호 | 1 MPa | Wang 2021 *Joule* 미열람 |
| 61호 | 1.0 MPa range · 1 MPa sufficient | Sharafi 2016 · Wang & Sakamoto 2018 미열람 |
| **81호** | **< 1 MPa** | **초록 · 인용 0 — 출처 없음** |

⇒ **아홉 편(독립 인쇄 여덟) · 여섯 값(0.1 · 0.4–1 · < 1 · 1 · 2 · 5) · 띠 0.1–5 MPa(×50) · 확인된 원전 0 그대로.** 인용 없이 인쇄한 편 넷(25 · 33 · 59 · 81) · 끝까지 열어 보니 빈 다리 셋
(8 → 81 · 13 → 59 · 13 → 60) · 남은 열린 다리 넷(12 · 13 [35] · 39 · 61 — 13 [35] Li Menglin 2025 *AFM* 은 이미 받음(3차 묶음 49-2) · ingest 대기).

### 2. ★★ 압력 값의 지도 — 재인용 70 행, 창의 새 수치 0

- 제조 · 조립: 125–504 MPa(표 1 17 행 · 밀도 83–99 %) · 50–370 MPa(Doux [26] σ 0.99 → ≈2.28 mS/cm) · 0–100 MPa(= 39호 굴곡도) · LGPS 78–467 MPa 압착 @ 3 MPa 시험(시험 압력은 그림 범례에만).
- 운전(실험): 5 · 25 · 75 MPa(= 5호) · 11 / 45 MPa(Hänsel [10] — Fig. 1 패널의 단락 `[도표]` ≈63 · ≈123 MPa 는 본문 0) · 7.4 · 13 MPa(Chang [15]) · 0.1 ↔ 7 MPa(Ning [104] 단락 용량 `[재현]` ×4.86) ·
  12.5 · 7.5 · 0.6–3.6 · 5 · 2.5 MPa(각 한 점).
- 모형(아래 벽): ≈0.4(Wang [7] — `[도표]` 두 변형률 교차 ≈0.64–0.67 · 공극 봉우리 ≈0.25, digest D8) · 1 부족 / 3 충분(Tu [74]) · > 12(FSI [76]) · < 10 / > 20(Zhang X. [8]) · 50 / 100 MPa(MD [75] — 전류
  `[재현]` 4×10⁴ A/cm² · 그림은 W 0.25 에 ≈160–175 MPa, D7).
- 표 2 "recently reported low-pressure SSBs" 14 행: `[재현]` < 1 MPa 7 행(0.1 × 6 · 0.4 × 1) · 0.1 여섯 중 둘은 같은 지면이 대기압 / 무가압 · 양극 적재 ≥10 mg/cm² 세 행은 전부 2–4 MPa ⇒ `[해석]` 초록 요구치를
  만족하는 완전지는 저적재 · 60 °C · 자기 인용 편뿐 · **같은 전극의 압력 스윕 0 행**(33호 표 1 과 같다). 같은 원전에 두 압력이 붙은 행 셋([12] 0.1 ↔ 2–4 · [130] 4 ↔ 8 · [143] 2 ↔ 무가압 ↔ 0.1, D5).

### 3. 창 명제 — 틀은 같고, 이 편은 창을 버리는 처방을 낸다

- 두 벽(Fig. 2 이득 ↔ Fig. 9 곤경)은 이 페이지의 틀(아래 = 접촉 손실 · 위 = 단락)과 같다. `[해석]` 모형이 "필요" 라 한 압력(3 · 12 · 20 MPa)과 실험이 "해롭다" 고 한 압력(7 · 7.4 · 11 · 13 MPa)이 같은 자릿수로
  **겹친다**(조건은 다르다 — 0.1 mA/cm² · 결함 곁 ↔ 4 mA/cm² · 다른 SE). 이 편은 겹침을 말하지 않고 "pressure-insensitive / pressure-independent SSBs" 로 **창 자체를 버리는 처방**(SSE 계면 · 구조 공학 · 전극 설계)을 낸다.
- **창은 Li 금속 음극 쪽이다** — 위 벽 전부 · 아래 벽 대부분이 Li\|SE. 양극 쪽 값은 Sakka(제조형 50 MPa) · Shi(재가압 300) · Doerrer 2.5 / 0.2 · Zou 6 · Kwon 2(또는 무가압) MPa 뿐이고 압력 스윕 0.
- 세 단계 분류(조립 압력을 따로 부름)는 이 페이지의 두 축(제작 ↔ 운전)을 한 단계 더 가른다 — 단 정의 뒤 `assembly pressure` 3 회 · `manufacturing pressure` 6 회로 거의 쓰이지 않는다.
- `[재현]` Wang [7] 식 (6)(7) 을 같게 두면 σ_c ∝ (j/l₀)^(1/m) — 재수록 점 기울기 m ≈3.9–5.1 로 0.1 → 1 → 4 mA/cm² 에 σ_c ≈0.64 → ≈1.0–1.2 → ≈1.3–1.7 MPa · 그림의 전류 변형률에서 l₀ ≈0.72 mm.
  초록 요구치(< 1 MPa)에 닿는 모형 값은 이 하나(저전류 · 평탄 계면 · Li 두께 규격화)뿐이고, [[li-metal-yield-creep-vs-stack-pressure]] 의 항복 0.73–0.81 MPa 바로 아래다.

### 4. §압력 진동 · §이력의 재수록 표본

62호 두 패널(In ≈1.2 · LTO ≈0.065 MPa — **떼어** 싣고 LTO 패널을 "LCO + In-Li" 로 서술, D3) · Ham [93] 기저 ≈4.9 ↔ ≈7.0 MPa(진폭 ≈40 %) · 합금 음극 1.28–2.25 MPa [91] · Liang [92] 응력 센서 ≈1.67 → 1.76 MPa / 3300 h ·
Lee [45] **개방 회로 이완 30 → 27.6(LPSC) · 24.8 MPa(LSPS) / 20 h**(`[도표]` · 본문 "from 5.2 to 2.3 MPa" 는 두 재료의 하강 폭, D2) · Zhang X. [8] 4.5 MPa 에서 접촉 0 / 1 / 5 h 확장(모형).
⇒ 운전 압력이 상수가 아니라는 §33호 3 의 관찰에 재수록 표본이 더해진다 — 이 편 자신은 이력 · 이완을 서술하지 않는다(`hysteres` 는 전압 이력 1 회 · `relax` 는 공공 이완 1 회). [[assb-operando-pressure-signal-attribution]] 81호 주석.

### 5. 이 편이 이 페이지에 **안 준 것**

요구치의 출처 · 같은 전극의 압력 스윕 · 양극 쪽 `θ(P)` · `R(P)` · 용량(P) · 감쇠(P) · 압력 계측 · 구속 형식(로드셀 · 스프링 · 정변위 구분 0) · "low pressure" 의 정의(표 2 0.1–4.9 MPa ↔ 초록 < 1).
창의 값은 움직이지 않았다 — 움직인 것은 계보 한 줄(8호 가닥의 끝)과 재수록 표본의 목록이다.

## ★ 2026-09-29 (`assb` 85호 Wang Y. · Li X. 2024 *Adv. Mater.* 36, 2309306, **실험 · 황화물 완전지 · Li 박 + Si(–SE) 음극 · 성형 400 MPa → 운전 50 MPa 한 점 · 스윕 0**) — **창의 값은 움직이지 않는다: 50 MPa 에서 3–5 C 4000 사이클 단락 0(RT) · 15 C 40.5 mA cm⁻² 1100 사이클 단락 0(55 °C) — 단락 벽을 넘지 않은 표본이고, 캡션에만 있는 "pouch cell 10 MPa · 75 µm" 는 패널 · 실험 절 · 데이터가 없다**

`raw/papers/wang2024_fast-kinetics-hierarchical-catholyte-anode-design-ssb.md` (25호 ref 16 지목 · **3차 묶음 파일 47**).

- **압력 서술 셋**: `[인쇄]` "pressed together in a homemade pressurized cell at 400 MPa and kept at 50 MPa during testing" · 그림 3 캡션 "b) Cycling performance in pouch cell at 10 MPa external pressure … separator thickness of 75 um"(패널 없음 — 85호 D5) · 서론 "comparable separator layer thickness and stack pressure of pressurized coin cells"(값 0). 구속 형식(정하중 / 정변위) · 압력 계측 · 온도 통제(RT 22–30 °C 무통제) 미인쇄.
- **단락 벽 쪽 표본**: 임계 C-rate(단락의 첫 율) 4–11 C(18 mg cm⁻² · 2.7 mAh cm⁻² → 10.8–29.7 mA cm⁻²) — 음극 구성의 함수로 인쇄(표 S3 26 행) · 압력은 한 점이라 `j_crit(P)` 는 없다 · 중앙층 LGPS ↔ LPSCl-I 가 수명을 ×2–4 움직임(그림 4g · 셀 하나씩) — 단락은 압력 밖의 손잡이(분리막 · 음극 구조)에도 걸린다는 표본.
- **아래 벽(접촉) 쪽**: 50 MPa 한 점 · 접촉 관측 0 — 이 페이지에 값 0.
- **분리막 두께**: 120 mg SE · 면적 미인쇄 → `[재현]` 363–817 µm(A 1.77–0.785 cm² 가정 · ρ 1.87) — "comparable … thickness" 의 실체는 두꺼운 펠릿 급(`[해석]`) · 파우치 75 µm 는 캡션뿐.
- 이 편이 이 페이지에 **안 준 것**: 압력 스윕 · `θ(P)` · `R(P)` · 용량(P) · 구속 형식 · 계측 · 파우치 자료.

## 경고 (전부 원문이 준 한계에서 나온다)

1. **점당 셀 1 개, 오차 막대 0.** 압력–수명 6 점 전부 N=1 이다.
   ★ 예외: Table S2 가 펠릿 **4 개**의 상대밀도를 준다 (80.2 / 84.9 / 80.3 / 83.0 %;
   `[재현]` s ≈2.3 %p → **공극률 15.1–19.8 %**). 퍼콜레이션은 문턱 현상이라
   이 폭이 `t_short(P)` 로 **증폭**되는데 논문은 전파하지 않는다.
2. **전류밀도 한 점(75 µA cm⁻²)** 이다. 실용 전류는 1–2 자릿수 높고, 위 벽의 기구
   (도금이 돌기를 키운다)는 명백히 전류 의존이다. **창의 위 벽이 전류로 얼마나
   내려오는지 모른다.**
3. **하한이 탐색되지 않았다.** 논문은 "optimal 5 MPa" 라고 쓰지만 SI Fig. S3 이
   **2 MPa 에서 163 h 무단락 · 과전압 거의 동일**을 보여주고 본문은 그 실험을
   **언급조차 하지 않는다.**
4. ~~**압력 → 용량 곡선은 아직 0 편이다.**~~ (→ 16호가 **세 번째이자 가장 넓은 표본**을 줬다: §16호 3) Doux 는 저항·수명·과전압을 압력의 함수로
   주지만 **완전지 용량은 압력 1 점(5 MPa)** 뿐이다. 4호도 각 1 점이었다.
   → ✅ **2026-09-16: 6호(Lee)가 처음 줬다** — `[도표]` 율특성 **2/3/4 MPa = 94.0/95.1/95.5 %**
   + 300 사이클 유지율 3 곡선 + **무압 대조**. ⚠ 단 **폭이 1.5 %p** 라 정보량이 거의
   없고(이 셀은 이미 490 MPa 로 눌러 놓았다), **4 MPa 위가 없다.**
5. ★ **6호의 압력이 사이클 중 유지되는지 알 수 없다.** 충전 때 도금 Li 25–30 µm 가
   생겨 셀이 두꺼워지는데, 지그가 **정압인지 정변위인지** 적혀 있지 않다 (6호 G12).
   5호가 **로드셀로 실계측**한 것과 대비된다.
5. **1 MPa 점이 축에 잘려 검열**돼 있고, 6 점이 **같은 셀의 순차 가압**으로 보이는데
   논문이 그 구분을 하지 않는다 → 각 점이 앞 점의 이력을 업고 있다(§이력).

## 이 페이지가 주장하지 않는 것

- **75 MPa 를 보편 상한으로 옮기지 않는다.** 모집단은 Li 금속 / Li₆PS₅Cl 82 % /
  75 µA cm⁻² / 상온이다. **6호의 4 MPa 도 마찬가지다** — 그리고 그쪽은 **데이터도 없다.**
- **"운전 압력은 필요 없다" 고 주장하지 않는다.** 6호의 무압 운전은 **0.1 C**
  (그리고 적층셀은 0.05 C)에서만 보였다. 같은 논문이 `[인쇄]` "pressurization is
  **unavoidable for high-current operations**" 라고 적는다.
- **"5 MPa 가 최적" 을 받아들이지 않는다** (경고 3).
- **산업 요구치를 한 값으로 옮기지 않는다** (2026-09-23, 33호) — 계보 다섯 편이 ≈1 · 0.4–1 · 2 · 5 MPa 를 인쇄했고 확인된 원전은 0 이다.
- **요구치 띠를 "수렴" 으로 적지 않는다** (2026-09-28, 59호) — 일곱 편이 0.1 · 0.4–1 · ≈1 · 1 · 2 · 5 MPa 를 인쇄했고(×50) 확인된 원전은 0 이다. 13호 절의 "≈1–5 MPa 독립 수렴" 은 59호에서 반박됐다.
- **59호 Fig. 1b 의 그림 점 · Fig. 5 의 상자그림을 운전 압력 표본으로 쓰지 않는다** (2026-09-28) — 그림 점은 자기 원자료와 다르고(D1), Fig. 5 는 원자료가 없다. 쓸 수 있는 것은 Source Data 의 29 값(시뮬 편 · 비-Li 금속 편 포함)뿐이다.
- **39호의 제조 압력 5 점을 운전 압력 문턱으로 옮기지 않는다** (2026-09-23) — 제조 가압이 없는 셀의 단조 가압이고, 되돌림 뒤 전기화학은 0 점이다. 그리고 `φ` 판독값은 CT 0.5 µm 화소 판정 · 분할 문턱 미인쇄 위의 값이다.
- **압력이 `LAM_PE` 와 접촉 손실을 가른다고 주장하지 않는다.** Doux 는 양극 열화를
  다루지 않는다 — 이 페이지의 기여는 **연산자의 사용 조건**이지 분리 자체가 아니다.
- **Doux 의 저밀도 토모그래피 구조가 Li 금속이라고 단정하지 않는다** — 같은 논문이
  `[인쇄]` "Li 금속 덴드라이트는 XRD 로 직접 검출되지 않는다" 고 적고, 같은 대비를
  다른 그림에서 "severe cracking" 이라 부른다 (5호 digest D6).
- **60호의 "외압 0" 을 "압력 0" 으로 옮기지 않는다** (2026-09-28) — 프레임을 뺐다는 것까지이고, 운전 중 구속(정하중/정변위)은 인쇄돼 있지 않다; 같은 편의 정변위 지그는 첫 충전에 +1.51 MPa 를 보였다. 그리고 **Table S2 의 문헌 압력 13 값을 창의 표본으로 쓰지 않는다** — 계측 방식 · 사이클 정의 규약이 없다.
- **61호의 멱법칙 외삽값(1 % 변형 시간)을 셀의 값으로 옮기지 않는다** (2026-09-28) — 벌크 인장 · AR 4 · 실온 · 단조 하중의 외삽이고, 0.28 MPa 아래는 하한 · 2.83 MPa 위는 무효다. 그리고 **"Li 가 항복을 넘어 creep 한다" 를 다시 쓰지 않는다** — 원전은 creep 을 항복 아래에서 쟀다(§61호 3). 61호의 압축 값(0.8–2.4 MPa)은 응력 순서가 역전된 장치 값이라 위 벽의 정량에 쓰지 않는다.
- **62호의 ΔP(1.25 MPa)를 운전 압력 요구치나 창의 표본으로 옮기지 않는다** (2026-09-28) — ≈61.8 MPa 기저(ESI 그림 축) 위 · 기저선 보정 · 지그 순응이 정한 값이다(원시 +1.07). 그리고 **무가압 셀(딜라토 · X-CT)의 낮은 용량을 "압력 0 의 효과" 로 옮기지 않는다** — 압력 말고도 SE 두께 · In 지름 · 전류 · 장치가 다르다.
- **63호의 토크(10 N·m)를 MPa 로 옮기지 않는다** (2026-09-28) — 나사 규격 · 마찰이 인쇄되지 않아 `[재현]` 42–106 MPa 의 띠만 선다. 그리고 **23호의 64 / 70 MPa 를 63호의 값으로 인용하지 않는다** — 23호가 같은 절차를 빌리며 자기 셀에 적은 값이다.
- **65호 파우치를 무가압 셀로도 가압 셀로도 인용하지 않는다** (2026-09-28) — 사진의 바인더 클립 둘은 정량 0 이고 운전 압력 서술이 없다.
- **73호의 ≈40 MPa 를 운전 압력 요구치나 창의 표본으로 옮기지 않는다** (2026-09-28) — 측정 · 사이클 조건의 한 값이고 스윕이 없다. 사이클 셀의 구속 형식(정하중 / 정변위)은 인쇄 0 이다.
- **80호의 코인셀 하중(≈0.1–0.2 MPa)을 창의 표본이나 요구치로 옮기지 않는다** (2026-09-29) — 액체 코인셀의 두 추정(판 식 · 스프링 — 스프링 식은 인쇄 값으로 재현 안 됨)이고, 판 휨 · 간극 수치는 오목 캔 · 단순 지지 스페이서라는 설계의 값이다. 가장자리 분리막 기공 폐쇄가 측면 구배의 원인이라는 것도 저자 배정이다(절대 간극은 셀 절반에서 공칭 이상).
- **81호의 "< 1 MPa" 를 산업 요구치의 원전으로 인용하지 않는다** (2026-09-29) — 초록 한 줄 · 인용 0 · 본문 재진술 0 이다. 8호의 "<≈1 MPa" 는 그 재인용이라 독립 인쇄로 세지 않는다. 그리고 **81호 표 2 의 "0.1 MPa" 행을 저압 운전 표본으로 쓰지 않는다** — 여섯 중 둘은 같은 지면이 대기압 / 무가압이고 하나는 본문 126 kPa 이며, 압력 계측 · 구속 형식은 전부 미인쇄다.
- **85호의 "pouch cell 10 MPa" 를 운전 압력 값으로 세지 않는다** (2026-09-29) — 캡션 한 줄 · 패널 · 실험 절 0 이다. 50 MPa 4000 사이클 단락 0 을 창의 위 벽 값으로도 쓰지 않는다 — 한 점 · 벽을 넘지 않은 표본이다.

## 관련
- [[assb-pressure-reapplication-separation-test]] — `P↑` 분리 연산자. **이 페이지가 그 상한을 준다.**
- [[assb-apparent-capacity-decomposition]] — 3 항 분해. `η = η(i, P)` 로 넓혀야 한다.
- [[composite-cathode-percolation-utilization]] — `θ_AM`. 압력이 되돌리려는 양(단, 이 페이지의 실측은 **음극** 계면이다).
- [[assb-contact-loss-vs-lampe]] — 닻 질문. 압력은 그 질문의 **우회로에 붙는 안전 조건**이다.
- [[near-optimal-set-width-measurement]] — 압력 2 점을 어디에 놓을지(§1)가 이 기계의 설계 입력이다.
- [[ag-c-interlayer-lithium-phase-path]] — 7호(Spencer-Jolly 2023)의 본체. 압력 축은 위 절이 전부다.
- [[anode-free-li-inventory-accounting]] — 같은 논문(Lee 2020)의 **음극 인벤토리 축**.
  이 페이지가 그 논문의 압력을, 그 페이지가 그 논문의 `LLI` 를 받는다.
- [[assb-maxwell-ocv-derivative-channels]] — 압력을 **관측 변수**로 쓰는 편(14호). 계보 최초의 `E(P)` 와 그 비선형.
- [[li-metal-yield-creep-vs-stack-pressure]] — 이 창의 **재료 눈금**(61호 Masias 2019): 항복 0.73–0.81 MPa · creep `n` 6.56 · 영역 경계 0.28 / 2.83 MPa. §정의의 "항복을 넘어 creep" 정정의 원전.
- [[assb-operando-pressure-signal-attribution]] — 압력을 **관측 신호**로 쓸 때의 분해(62호 Zhang W. 2017 원형): 음극 지배 · 강성 곱 · 기저선 규약 — §압력 진동의 값을 옮길 때 붙일 단서.
