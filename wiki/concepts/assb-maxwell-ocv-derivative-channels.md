---
title: Maxwell 관측 채널 — OCV 의 온도·압력 편미분을 관측 축으로 (엔트로피메트리 · volumetry)
description: "Oh et al. 2025 (Angew.) — ASSB 셀에서 −F(∂E/∂T)_P = ΔS(x), F(∂E/∂P)_T = ΔV 를 정지 상태에서 재는 비파괴 진단; OCV 적합의 경쟁이 아니라 같은 상태함수 E(x,T,P) 의 관측 추가이며, 우리 쌍(LAM_PE ↔ 접촉 손실)에 대한 새 감도 행의 부호와 그 한계"
created: 2026-09-22
updated: 2026-09-22
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/oh2025_maxwell-protocol-nondestructive-assb-health.md, raw/papers/shi2020_mechanical-degradation-assb-cathode.md, raw/papers/doux2020_stack-pressure-room-temperature-assb-li-metal.md, raw/papers/bielefeld2019_microstructural-modeling-assb-composite-cathode.md, raw/papers/mohtat2019_electrode-soh-estimability-expansion.md]
confidence: low
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: single-source
---

# Maxwell 관측 채널 — OCV 의 온도·압력 편미분을 관측 축으로 (엔트로피메트리 · volumetry)

> `assb` 축 **아홉째 개념**. 앞의 여덟이 *현상*(접촉 손실이 있다)·*역문제*(그 양이 유일하게
> 정해지는가)·*모델 차수*(봉우리 개수가 상태변수다)를 다뤘다면, 이 페이지는 **관측 자체를
> 늘리는 조작**을 다룬다 — 그리고 그것이 우리 쌍(`LAM_PE` ↔ 접촉 손실)에 대해 **어느 방향으로
> 눈을 뜨고 어느 방향으로 눈이 머는가**를 적는다. 근거는 **1 편**(Oh 2025, 실험) —
> `single-source`.

## 정의

**Oh, Kim, Kim, An, Kwon, Choi 2025** (*Angew. Chem. Int. Ed.* 64, e202514910, Hot Paper —
`raw/papers/oh2025_maxwell-protocol-nondestructive-assb-health.md`)가 "Maxwell diagnostic
protocol" 이라 이름 붙인 것은 **OCV 라는 한 상태함수 `E(x, T, P)` 의 두 편미분**이다:

| 채널 | 조건 | 식 `[인쇄]` | 논문의 귀속 | 실측 (NCM811‖LPSCl‖Li) |
|---|---|---|---|---|
| **엔트로피메트리** | 등압 (`dP = 0`, 스택 압력 고정) | (6) `ΔS ≡ (∂S/∂x)_P = −F(∂E/∂T)_P` | 층상 CAM 의 **탈리튬화 비균질**(상전이 봉우리가 OCV 축에서 뭉개짐) | 35→20→35 °C, 5 % SOC 마다; `[도표]` ΔS(OCV) 신품 +3 → **−11** J mol⁻¹ K⁻¹(4.25 V) → 100 사이클 뒤 **+3.5 ~ 0** ("ΔS drop" 13–15 → 5.8–8) |
| **volumetry** | 등온 (`dT = 0`) | (10) `ΔV ≡ (∂V/∂x)_T = F(∂E/∂P)_T` | 복합전극 **void**(ΔP 가 void 로 완화됨) | ΔP = 10→5 MPa 에 `[인쇄]` **2.2 → 1.8 mV**(−18 %) = **42.7 → 34.7 µJ mol⁻¹ Pa⁻¹**; XRM 공극률 4.5 → 9.8 % |

- `[해석]` 엄밀히는 Maxwell 관계(`(∂S/∂P)_T = −(∂V/∂T)_P`)가 아니라 `G(x, T, P)` 의 **혼합
  2계 편미분 대칭성**을 `x` 축에 확장한 것 — 액체셀 엔트로피메트리(Yazami 계보)의 표준
  유도다. 이름이 새롭지 물리가 새롭지 않다.
- **적합이 없다.** `fit*`·`model`·`simulation` 0 회. 관측이 직접 열역학 도함수이고, 그 위에
  "비균질"·"void" 라는 **이름을 가정으로 붙인다**.
- **단위 검토**: `F·(V/Pa) = J mol⁻¹ Pa⁻¹ = m³ mol⁻¹` — 42.7 µJ mol⁻¹ Pa⁻¹ 는 **42.7 cm³
  mol⁻¹**, 몰부피 차원이다. 논문은 "volumetric energy" 라 부르고 기준 부피와 비교하지 않는다.

## 왜 중요한가 — 세 가지

### 1. "OCV 경쟁 접근" 이 아니라 **관측 추가**다

우리 닻([[assb-contact-loss-vs-lampe]])의 물음은 `E(x)` 적합이 `LAM_PE` 와 접촉 손실을
가르는가이다. 이 편은 `E(x)` 를 적합하지 않고 `∂E/∂T`·`∂E/∂P` 를 잰다 — 즉
[[constrained-crb-identifiability]] 의 세 조작(제약 추가 · **관측 추가** · 창 이동) 중
**관측 추가**이며, 감도행렬에 두 행 묶음 `∂(∂E/∂T)/∂θ_j`·`∂(∂E/∂P)/∂θ_j` 가 더해진다.
Mohtat 2019 의 팽창 `Δt_c` 와 같은 자리에 앉는 **첫 ASSB 실험 표본**이다.

이득 조건은 Mohtat 식 39 그대로 — **새 행 ≠ 0 이고 기존 행과 독립**. `[해석]` 우리 쌍에
대해 손으로 부호를 적으면:

| 모드 | ΔS(x) 행 | `dE/dP` 행 | 이유 |
|---|---|---|---|
| **균일 `LAM_PE`** (활물질 균일 소실 = `x` 축 아핀 재조정) | **0** | 불명(격자항 ∝ 활물질량, 그러나 유효 컴플라이언스가 지배) | ΔS 는 **intensive**(몰당) — 모양 불변 |
| **완전 고립 접촉 손실** (입자가 전기적으로 사라짐) | **0** | **≠ 0** (void ↑ — 논문의 주장) | 참여 입자만 남고 그것들은 균질 |
| **부분 접촉 손실 · 계면 저항 상승** (느린 이완, SOC 분산) | **≠ 0** | 부분 | OCV 축에서 봉우리 뭉개짐 |

⇒ `[해석]` **엔트로피메트리는 우리 쌍 둘 다에 눈멀고**(둘 다 아핀), "덜 연결된" 중간 상태에만
민감하다. **volumetry 가 분리 후보 행이다** — 이 편은 반대로 ΔS 를 주 진단(recycle 판정)으로
둔다. ⚠ 실측 0, 우리 명제. 그리고 이 편 스스로 `[인쇄]` ΔS 가 "local physical **contact
loss** … **as well as** an increase in the **interfacial resistance**" 를 한 신호로 받는다고
정의한다 — 우리 쌍을 **합친** 채널이라는 자백이다.

### 2. ★★★ 이 편이 우리 축에 준 가장 직접적인 실측 — **void 가 용량에 안 보인다**

`[인쇄]` 50 사이클 뒤 XRM 공극률 **4.5 → 9.8 %**(10 MPa) ↔ **4.4 → 5.3 %**(20 MPa) 인데 용량
유지율은 **86.0 % ↔ 84.0 %** — void 2 배 셀이 **더 높다**. 논문: "similar … internal voids
may not directly affect the early-cycle performance". `[해석]` [[assb-apparent-capacity-decomposition]]
의 언어로 **`θ_AM` 이 이 창에서 ≈1 로 버틴다** — 1호의 퍼콜레이션 그림(`p_c` 위에서 이용률
≈1)과 정합하고, 4호 Shi(면적 10.4 % ↔ 60 %p)의 **반대쪽 끝**이다. 접촉 손실 → 용량 사상은
**문턱형**이고, 문턱 아래에서 OCV 적합은 `LAM_PE ≈ 0` 을 (정확히) 보고하면서 void 2 배를
**놓친다** — 오독이 아니라 **무감**. 그것을 보는 것이 이 페이지의 두 번째 채널이다.

### 3. 압력이 **관측 변수**가 된다 — 계보 최초의 `E(P)`

4호의 `P↑`([[assb-pressure-reapplication-separation-test]])는 300 MPa · 비가역 · 1 회
(**대신호**). volumetry 의 ΔP = −5 MPa 는 가역 · 반복 가능 · 0.4 mV (**소신호**) — 같은
물리 `θ_AM(P)` 의 **미분**이다. 그리고 계보 최초의 `E(P)` 두 구간이 들어왔다:
`[인쇄]` **2.2 mV / 5 MPa (10→5)** ↔ **2.3 mV / 10 MPa (20→10)**, 둘 다 신품 →
`[재현]` **0.44 ↔ 0.23 mV/MPa, 2 배** — `E(P)` 는 **오목 비선형**이고 논문은 이것을 적지
않는다(Fig. 5e/f 의 y 축 눈금이 달라 가려진다). ⇒ "ΔV" 는 재료 상수가 아니라 **압력
구간과 SOC 의 함수인 유효 컴플라이언스**다. `[재현]` Li 금속 몰부피 항(13.0 cm³ mol⁻¹)
만으로 5 MPa 에 0.67 mV 가 나오는데 실측이 2.2 mV — 격자·금속 몰부피로 설명되는 크기가
아니다.

## 경고 — 원문이 준 한계에서 나온다 (자세히는 raw digest D1–D15 · G1–G14)

1. **역문제가 없어서 유일성 물음이 사라진다 — 그러나 귀속의 유일성은 안 쟀다.** ΔS 변화가
   비균질인가 재료 변화인가: `[재현]` **sum rule** — `∫(dS/dx)dx` 는 상태함수 차이라 비균질만으로는
   안 변하는데 `[도표]` 전 곡선 평균 ≈ −3.5 ↔ 후 ≈ +1.5 J mol⁻¹ K⁻¹ 로 **부호가 바뀐다**. 논문은
   이 뺄셈을 안 한다 (7호·11호와 같은 형태).
2. **전·후 volumetry 의 SOC 가 다르다** — 캡션은 둘 다 "after discharge at 2.5 V" 인데 `[도표]`
   OCV **3.532 ↔ 3.703 V**(S16 도 3.476 ↔ 3.648). `∂V/∂x` 는 `x` 의 함수다.
3. **`dE` 판독 규칙 0** — `[도표]` S16 재가압 뒤 **+0.4 mV 비가역 오프셋** + 감압 중 **+0.5 mV
   표류** = 노화 신호(0.1–0.4 mV)와 같은 자릿수. 5호 이력(`θ(P)` 경로 의존)의 그림자.
4. **음극 상수항** — 식 (6)·(10) 의 Li 금속 항은 0 이 아니라 상수(29 J mol⁻¹ K⁻¹ · 13 cm³
   mol⁻¹)이고, "10 MPa → creep → pore 무시" 는 pore 항 논거일 뿐이다. 100 사이클 뒤 음극
   계면 기여 미검토.
5. **분리 주장은 교차 실험 0** — `(ΔS, ΔV)` 2×2 중 **(1, 0)**(void 없는 순수 화학 열화) 칸이
   실험에도 Fig. 6 에도 없다. 20 MPa 셀은 volumetry 만 쟀다.
6. **"health" 라벨의 문턱값 0**, 오차 막대 0, 3 셀(S3 는 점 2 개), **Fig. 3c "after" 곡선이
   S2 세 셀 어느 것과도 끝점이 다르다**(D2).
7. **Recondition(>300 MPa) 미수행 · 4호 미인용** — Li 금속 셀에 300 MPa 는 5호 상한(75 MPa)의
   4 배.
8. `[인쇄]` "real time" ↔ `[재현]` 1 프로파일 ≈140 h(점당 5 h × ≈28 점).

## 이 위키에서의 적용

- **닻에 붙는 자리**: [[assb-contact-loss-vs-lampe]] Evidence 열한 번째 절 + 새 제약 5 개.
  채움표에 **새 칸은 0**, 층 셋(Q1 비파괴 대리량 · Q6 `E(P)` · Q8 OCV 축 도함수).
- **폭 측정이 붙는 자리 셋** ([[near-optimal-set-width-measurement]]):
  ① volumetry 를 잔차 행으로 넣었을 때 `(a_PE, b_PE) ↔ θ` 폭이 얼마나 주는가 — 단 **`E(P, x)`
  면을 먼저 모델링**(경고 2·3), 상수 `ΔV` 금지.
  ② ΔS(x) 를 [[halfcell-ocp-shape-invariance]] 의 **두 번째 상태함수 검사**로 — 아핀 창이 맞으면
  `E(x)` 와 `∂E/∂T(x)` 가 **같은 (α, β)** 로 재조정돼야 한다. SOC 축 변환이 먼저다(G7).
  ③ sum rule 검사를 S2 세 셀에 — 우리가 그림으로 할 수 있는 뺄셈.
- **13호(Zheng 2026)가 요구한 "pressure sensing"** 을 이 편은 **진단 조작**으로 쓴다 — 13호의
  SOH 2 항(true AM loss ↔ usable capacity)에 **세 번째 축(void)** 이 붙되, 그 축이 **용량에 안
  보인다**(§2)는 것까지.
- **10·11호 EIS/DRT 와의 관계**: `[인쇄]` "overpotential tracking and EIS … limited in their
  ability to elucidate the underlying degradation mechanism" — **모델 차수가 없는 관측**으로
  [[drt-peak-count-nonidentifiability]] 의 문제를 우회하지만, 귀속의 유일성은 같은 상태다.

## 이 페이지가 주장하지 않는 것

- **"volumetry 가 `LAM_PE` ↔ 접촉 손실을 가른다" 고 주장하지 않는다.** §1 의 부호표는 우리
  `[해석]` 이고 실측 0 — 폭 측정기로 검사할 명제다.
- **42.7 µJ mol⁻¹ Pa⁻¹ 를 몰부피로 옮겨 쓰지 않는다.** 압력 구간에 2 배, SOC 에 미지로
  의존한다(§3, 경고 2).
- **"void 는 용량에 안 보인다" 를 일반화하지 않는다.** 50 사이클 · 2 점 · 조건당 셀 1 · 0.5C
  의 것이다. 4호는 같은 자릿수의 void 에서 98 % 손실을 봤다(다른 화학·압력·율).
- **Q4 가 측정됐다고 하지 않는다** — `assb` **0/14 편** 그대로.

## 관련
- [[assb-contact-loss-vs-lampe]] — 닻 질문. 이 페이지가 그 "관측 추가" 후보를 준다.
- [[constrained-crb-identifiability]] — 관측 추가의 정식화(Mohtat 식 39). 이 페이지가 그 ASSB 표본.
- [[assb-pressure-reapplication-separation-test]] — 대신호 `P↑` 연산자. 이 페이지의 volumetry 가 그 **소신호 판**.
- [[assb-stack-pressure-operating-window]] — 압력 창. 계보 최초의 `E(P)` 가 여기 붙는다.
- [[assb-apparent-capacity-decomposition]] — 3 항 분해. **void ≠ `Q_apparent`** 실측이 `θ_AM` 항에 붙는다.
- [[composite-cathode-percolation-utilization]] — `θ_AM ≈ 1 above p_c` 의 실험적 대응(§2).
- [[halfcell-ocp-shape-invariance]] — ΔS(x) 를 두 번째 상태함수 검사로 쓰는 자리.
- [[near-optimal-set-width-measurement]] — 새 행을 넣었을 때 폭이 얼마나 주는지 잴 기계.
- [[drt-peak-count-nonidentifiability]] — 이 편이 밀어내는 EIS 계보; 모델 차수 없는 관측의 대가.
- [[thermo-kinetic-loss-partition]] — 액체셀 축의 같은 형식(외부 변수 T·P·i 를 관측 축으로).
