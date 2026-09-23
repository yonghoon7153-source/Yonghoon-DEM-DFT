---
title: ASSB 스택 압력의 작동 창 — 아래는 접촉 손실, 위는 단락
description: "Stack pressure in ASSBs is a two-sided constraint: too low gives interfacial contact loss, too high drives Li creep into electrolyte pores and shorts the cell. Doux 2020 gives the first measured pressure sweeps (P→impedance, P→time-to-short, P→overpotential) and a hard upper bound"
created: 2026-09-16
updated: 2026-09-23
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/doux2020_stack-pressure-room-temperature-assb-li-metal.md, raw/papers/zhang2025_low-pressure-assb-challenges-strategies-review.md, raw/papers/shi2020_mechanical-degradation-assb-cathode.md, raw/papers/lee2020_ag-c-anode-free-assb.md, raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md, raw/papers/li2026_safety-aware-bms-active-intelligence.md, raw/papers/vadhva2021_eis-for-assb-theory-methods.md, raw/papers/zheng2026_assb-grid-realistic-appraisal.md, raw/papers/oh2025_maxwell-protocol-nondestructive-assb-health.md, raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md, raw/papers/yanev2024_li-in-alloy-anode-kinetic-limitations.md, raw/papers/fukunishi2023_ncm523-three-electrode-impedance-degradation.md, raw/papers/zhou2025_tailored-cathode-microstructure-low-pressure-assb.md]
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

33호에 재수록된 정변위 지그 원자료(`[도표]`): 흑연 ± LGPS [59] ≈0.7–0.8 MPa · μ-Si ‖ LTO [88] ≈0.5–1.0 MPa(기저 ≈45) · Sb ‖ Li [90] ≈1.2–2.3 MPa(기저 ≈20) ↔ LCO/NCM 양극 [58] ≈0.05–0.07 MPa · 스프링(정압) 지그 [19] ≈5 → 5.21 MPa(+4 %). ⇒ **상대극 호흡의 ΔP 가 요구치(≤2 MPa)와 같은 자릿수**다 — 산업 조건에서 스택 압력은 사이클 안에서 ≈100 % 움직이는 **상태변수**(8호 "coupled state/control variable" 의 숫자판). §"세 개의 결과" 3 의 `P↑` 연산자에 **"양극에 걸리는 압력 = 지그 + 상대극 ΔP(SOC)"** 조건이 붙는다. ⚠ 기저가 고압(20–45 MPa)이라 저압 기저의 진동 크기는 미상.

### 4. 이 편이 이 페이지에 **안 준 것**

압력의 함수 — `θ(P)` · `R(P)` · 용량(P) · 감쇠(P) 어느 것도 원전 서술로 없다. 가장 가까운 재수록은 Fig. 3I(70 / 7 / 2 MPa 첫 사이클 곡선, 캡션 [63] ↔ 본문 [78] 로 출처 갈림, `figure-read` 2 MPa Pristine ≈−10 %)와 Fig. 7B(2 MPa 한 점, 컷오프만 바꿈). **Sakka 2022**(`θ(P)` CT 측정 후보)는 [120] 으로 인용되지만 "3D 접촉 · 압력 방향" 명제에만 붙는다 — 25호가 같은 원전에서 옮긴 "50 ↔ ≤12 MPa 접촉 면적 분율" 은 이 지면에 없다.

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
- **압력이 `LAM_PE` 와 접촉 손실을 가른다고 주장하지 않는다.** Doux 는 양극 열화를
  다루지 않는다 — 이 페이지의 기여는 **연산자의 사용 조건**이지 분리 자체가 아니다.
- **Doux 의 저밀도 토모그래피 구조가 Li 금속이라고 단정하지 않는다** — 같은 논문이
  `[인쇄]` "Li 금속 덴드라이트는 XRD 로 직접 검출되지 않는다" 고 적고, 같은 대비를
  다른 그림에서 "severe cracking" 이라 부른다 (5호 digest D6).

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
