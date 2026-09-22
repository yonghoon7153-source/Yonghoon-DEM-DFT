---
title: ASSB 스택 압력의 작동 창 — 아래는 접촉 손실, 위는 단락
description: "Stack pressure in ASSBs is a two-sided constraint: too low gives interfacial contact loss, too high drives Li creep into electrolyte pores and shorts the cell. Doux 2020 gives the first measured pressure sweeps (P→impedance, P→time-to-short, P→overpotential) and a hard upper bound"
created: 2026-09-16
updated: 2026-09-22
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/doux2020_stack-pressure-room-temperature-assb-li-metal.md, raw/papers/shi2020_mechanical-degradation-assb-cathode.md, raw/papers/lee2020_ag-c-anode-free-assb.md, raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md, raw/papers/li2026_safety-aware-bms-active-intelligence.md, raw/papers/vadhva2021_eis-for-assb-theory-methods.md]
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
4. ~~**압력 → 용량 곡선은 아직 0 편이다.**~~ Doux 는 저항·수명·과전압을 압력의 함수로
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
