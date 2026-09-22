---
title: DRT 봉우리 개수는 데이터가 정하지 않는다 — 상태·조작·장비·정규화의 함수
description: "The number of resolvable DRT peaks (and hence the order of any equivalent circuit fitted downstream) is not determined by the impedance data alone: it moves with cycle number, with interventions, with the measurement wiring, and with the unreported regularization strength"
created: 2026-09-22
updated: 2026-09-22
type: concept
tags: [assb, battery, degradation, research, eis]
sources: [raw/papers/yu2024_drt-time-resolved-aging-sulfide-assb-fullcell.md, raw/papers/vadhva2021_eis-for-assb-theory-methods.md, raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md, raw/papers/su2024_drt-soh-health-features.md, raw/papers/kouhestani2022_phm-solid-state-batteries-perspective.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: interpretive
evidenceScope: multi-source-primary
---

# DRT 봉우리 개수는 데이터가 정하지 않는다

> `assb` 축의 **네 번째** 개념 페이지이고, 닻은 [[assb-contact-loss-vs-lampe]] 다.
> 앞의 셋은 [[composite-cathode-percolation-utilization]] ·
> [[assb-apparent-capacity-decomposition]] ·
> [[assb-pressure-reapplication-separation-test]].
> 수치의 정본은 원문 PDF 이고 이 페이지의 값은 **사본**이다 — 인용 근거로 쓰지 않는다.
>
> **왜 이 페이지를 만드는가**: 이 위키가 재는 것은 **"답이 하나로 정해지는가"** 다
> ([[fitting-degeneracy]] · [[near-optimal-set-width-measurement]]). EIS 계열
> 논문 세 편이 들어오면서, **파라미터 값의 축퇴보다 한 층 위에 "모델 차수 자체의
> 축퇴" 가 있다**는 것이 드러났다. 그것을 여기에 모은다.

## 정의

임피던스 스펙트럼 `Z(ω)` 를 이완시간 분포 `γ(τ)` 로 역변환한 것이 **DRT** 다:

```
Z(ω) = R₀ + ∫₀^∞  γ(τ) / (1 + jωτ)  dτ        (Yu 2024 SI Eq. 7)
```

`γ(τ)` 의 **국소 극대(봉우리) 개수**가 관례적으로 "이 셀에 물리적으로 구별되는
과정이 몇 개인가" 로 읽히고, 그 개수가 **뒤에 붙는 등가회로의 차수**를 정한다.

**이 페이지의 주장**: 그 개수는 **데이터만으로 정해지지 않는다.** 최소 네 개의
것에 달려 있다 — **① 노화 상태 ② 가한 조작 ③ 계측 경로 ④ 정규화 강도**.
따라서 **"봉우리 N 개 ⇒ RC N 개" 는 측정이 아니라 선택**이다.

## 왜 중요한가 — 세 논문이 세 층에서 같은 말을 한다

### 층 1 — 방법론: 역변환이 ill-posed 다 (Vadhva 2021, `assb` 10호)

`[인쇄]` "it is limited in that the data must be bounded (**via somewhat
arbitrary data preprocessing**) and data inversion is **mathematically
ill-posed, requiring regularization methods**. DRT analysis is also **very
sensitive to experimental errors**."
그리고 ECM 쪽에 대해 `[인쇄]` "**As no solution to an EIS spectrum is unique**,
and **the inclusion of more elements will tend to improve the fit**" ·
"it is often challenging to decipher **how many time constants are present** in
a given dataset and their assignment can be **highly subjective**."
⚠ **10호는 λ(정규화 파라미터) 선택 규칙을 주지 않는다** (digest G4).

#### 층 1 의 이웃 — PHM 종설이 액체셀 ECM 맥락에서 같은 말을 재인용으로 인쇄 (Kouhestani 2022, `assb` 12호)

`raw/papers/kouhestani2022_phm-solid-state-batteries-perspective.md` §3.1.2 (`[인쇄]`,
⚠ 재인용, ref [84] = Cho et al. 2012, *Comput. Chem. Eng.* 41, 1):
"the aging or temperature change of the LIB will cause the internal impedance
characteristics of the battery to change **from a single impedance arc to a double
impedance arc**, which significantly impacts the accuracy of the battery model."
→ **"분해 가능한 원호 개수 = 노화·온도의 함수" 의 세 번째 독립 인쇄**(10호 Larfaillou
재인용 · 11호 1차 DRT · 12호 액체셀 ECM 재인용). 그런데 같은 종설은 `identifiab*` **0 회**이고,
이 문장을 **"1차 RC 모델의 정확도가 떨어진다"** 는 실무 문제로만 적는다 — **차수가 정해지지
않는다는 문제로는 읽지 않는다.** ⚠ 원전 [84]가 실제로 그것을 보였는지는 확인 전이다.

### 층 2 — 실측: 개수가 상태·조작·장비로 움직인다 (Yu 2024, `assb` 11호)

10호가 처방한 DRT 를 실제로 돌린 첫 `assb` 논문이다. **우리가 그림을 열어 센 것**
(전부 `[도표]`, 세로 판독 오차 ±1–3, 가로 ≈1/4 자릿수):

| 무엇이 바뀌면 | 개수가 어떻게 | 좌표 |
|---|---|---|
| **사이클 4 → 48** (완전지) | 국소 극대 **2–3 → 5**. P3 가 **어깨 → 봉우리** | Fig. 2(a) |
| **사이클 3 → 29** (micro-SE 반쪽) | 중주파 극대 **1 → 2**. 그리고 cy 3 의 극대(≈9 kHz)가 이후 P2(≈18 kHz)로 **자리를 옮긴다** | Fig. 3(c) |
| **사이클 3 → 133** (graphite 반쪽) | **P4 가 없던 평탄(≈1.5)에서 생긴다**(≈10 Hz, 5.5) | Fig. 6(c) |
| **재가압 >500 MPa** (완전지) | **4 → 3**. P3 의 독립 극대가 **사라진다** | Fig. 7(d) |
| **배선 교체** (같은 셀) | ≈2 × 10⁴ Hz 의 **분해된 어깨가 있다 ↔ 없다** | Fig. S3 |

★ 그리고 **높이도 배선으로 움직인다** — 같은 셀, Arbin+Gamry ↔ Gamry 직결:
≈3 kHz 봉우리 **78 → 66 (−15 %)**, ≈3 × 10⁻² Hz 봉우리 **45 → 76 (+69 %)**.
⚠ **공정하게**: 배선이 바뀌면 인덕턴스·접촉저항이 실제로 변하고, 두 측정의 최고
주파수가 **1 MHz ↔ 2 MHz** 로 다르며, SI 가 "같은 셀" 이라고 **명시하지 않는다.**
**그러므로 69 % 는 상한이지 확정값이 아니다.**

★★★ **그런데 같은 논문의 본문이 물리로 해석한 변화가 그 폭 안에 있다** —
재가압이 P3 **−16 %** · P1 **−11 %** · P2 **−10 %** · P4 **−25 %**.
**논문은 두 숫자를 나란히 놓지 않는다.**

### 층 3 — 하류: 그 개수가 열화 지분으로 흘러간다 (Huo 2025, `assb` 9호)

9호는 **분해 가능한 원호 1 개**에 `R_b` + (`R_SEI`∥CPE) + (`R_ct`∥CPE) + `W`
= `[재현]` **자유 파라미터 9 개**를 맞추고, 그 `R_SEI` 분해를 노화 서사의 기둥으로
썼다. 그 결과 `R_SEI` 가 **동일 화학·공정·프로토콜 두 셀에서 +37.1 % / −79.7 %**
로 **부호까지 어긋났고**, 논문은 `[인쇄]` "장비 정확도 · **적합 과정이 넣은 오차** ·
열평형" 탓으로 넘어갔다.

★ **11호는 그 "적합 오차" 의 크기에 독립 근거를 준다** — 셀을 건드리지도 않았을
때(배선만 교체) 봉우리가 **−15 % ~ +69 %** 움직인다.
⚠ 두 양은 **같은 양이 아니다**(9호는 ECM 파라미터·두 셀, 11호는 DRT 봉우리
높이·한 셀 두 배선). **자릿수가 같다는 것까지만** 말한다.

## ★ 이름표의 불확정성이 이름표 간격보다 크다 — 가장 날카로운 형태

11호 한 편 안에서 **P3 의 보고 위치**:

| 좌표 | 값 |
|---|---|
| `[인쇄]` §3.1 (완전지) | **~500 Hz** |
| `[인쇄]` §3.1 (NMC 반쪽) | 10³–10² Hz |
| `[인쇄]` §3.2 | **10⁴–10³ Hz** |
| `[인쇄]` §3.3 | ~1 kHz |
| `[인쇄]` Table 1 | ~10³ Hz |
| `[도표]` Fig. 7(d) | **0.9 kHz** |
| `[도표]` Fig. 4(d) | **1.3 kHz** |
| `[도표]` Fig. 3(c) | ≈2.8 kHz |

`[재현]` **범위 = 500 Hz – 10 kHz = 1.3 자릿수.**
`[재현]` **P2 ↔ P3 실제 간격 = 0.8 자릿수** (`log₁₀(6000/900) = 0.82`,
Fig. 7d; `log₁₀(8000/1300) = 0.79`, Fig. 4d).

★★★★ **1.3 > 0.8** — 즉 **"이것이 P2 인가 P3 인가" 를 논문 자신의 기준으로
결정할 수 없다.** 그리고 `[인쇄]` Table 1 은 **P2 = 화학적 접촉(SEI/CEI)**,
**P3 = 기계적 접촉**이다 ⇒ **화학 열화와 기계 열화의 분리가 바로 이 자리에서
무너진다.**

## ★★ 두 개의 추가 경보

**(1) 전극 귀속이 애초에 없다.** `[도표]` 11호 Fig. 8(결론 지도)이
**P2 와 P3 에 `Cathode`(빨강)와 `Anode`(파랑)를 둘 다 찍고**, **P4(음극 전하이동,
넓음)와 P5(양극 전하이동, 좁음)를 ≈10 Hz 에서 겹쳐 그린다.**
→ **논문 자신이 축퇴를 그림으로 인쇄한다.** 완전지 스펙트럼 하나로는 전극을
가를 수 없고, 11호는 **반쪽전지 두 개를 따로 만들어서** 가른다 — 즉 **분해가
관측이 아니라 설계**다.

**(2) 봉우리가 측정 대역 밖에 선다.** 11호의 EIS 하한은 `[인쇄]` **0.1 Hz** 인데,
`[도표]` Fig. 1(b) 는 ≈**2 × 10⁻² Hz** 에 **두 번째로 큰 봉우리(77 Ω)** 를 놓고,
Fig. 4(d)·Fig. S3 도 ≈3 × 10⁻² Hz 에 봉우리를 놓는다. x 축은 **10⁻³ Hz 까지**
그려져 있다. `[해석]` **대역 끝 정규화 인공물의 전형**이고, 라벨이 없어서
본문·Table 1·Fig. 8 어디에도 나타나지 않는다.
⚠ 반대쪽도 같다 — `[도표]` Fig. 8 의 **(P1′) 은 회색 점선**이다: 측정 대역
(2 MHz) 위에 있어 **못 본 봉우리를 지도에 그려 넣은 것**이다.

## 이 위키에서의 적용

### 1. 진단 — "개수를 쟀는가" 를 묻는 체크리스트

EIS/DRT 를 쓴 논문을 받을 때 **이 다섯 개를 먼저 찾는다.** 없으면 "없다" 고 적는다.

| # | 질문 | 11호 | 10호 |
|---|---|---|---|
| C1 | **λ(정규화 강도)** 값 또는 선택 규칙(L-curve·GCV·CV) | ❌ 0 회 | ❌ 처방 없음 |
| C2 | **K–K / Lin-KK** 사전 검증 | ❌ 0 회 | ✅ 처방 (`essential`) |
| C3 | **DRT 불확실성** (Bayesian DRT · 오차막대 · 봉우리 폭) | ❌ 0 회 | ⚠ 원 논문으로 넘김 |
| C4 | **개수 선택 규칙** (AIC 등) | ❌ 0 회 | ✅ 명명, 미적용 |
| C5 | **반복/산포** (같은 셀·같은 조건 재측정) | ⚠ **1 점** (Fig. S3, 배선 교체 — 본인은 이렇게 부르지 않는다) | ⚠ 삼중 측정 **권고** |

### 2. 우리 폭 측정기가 붙는 자리 — 구체적으로 하나

[[near-optimal-set-width-measurement]] 의 기계는 **"답이 하나로 정해지는가"** 를
재고, 화학·방법에 무관하다. DRT 에 붙이면 절차가 이렇게 된다:

```
λ 를 격자로 흔든다  →  각 λ 에서  (봉우리 개수, 위치, 높이) 를 기록
                    →  "근최적" 을 잔차 기준으로 정의
                    →  그 안에서 각 양의 폭을 보고한다
```

`[해석]` 이것이 **11호의 Fig. S3(nuisance 1 점)을 곡선으로 바꾸는 최소 절차**이고,
**"DRT 로 잰 저항 증가분" 에 폭을 붙이는 최소 절차**다.
⚠ 우리가 아직 **하지 않았다** — 여기 적는 것은 **설계**이지 결과가 아니다.

### 3. 보고 규율 — 점추정 금지가 여기에도 적용된다

`bms-balancing/` 갈래가 도달한 결론은 **"LAM 분할은 점추정으로 보고할 수 없고
폭과 함께 보고해야 한다"** 였다. **같은 규율이 DRT 봉우리 높이에 적용된다** —
그리고 11호는 자기 SI 에 **폭의 하한을 인쇄해 놓고 본문에서 점추정을 쓴다.**

### 4. 라벨 층위에 칸 하나 추가

[[fitting-degeneracy]] 가 쓰는 provenance 층위에 **`inverted-nonunique`** 를
더한다 — **라벨이 ill-posed 역변환의 출력이고, 그 역변환의 정규화 설정이
보고되지 않은 경우.** 9호의 `fitted-single-parameter` 위층이다.

## ⚠ 이 페이지가 주장하지 않는 것

- **"DRT 가 쓸모없다" 고 하지 않는다.** 11호는 DRT 덕분에 **Nyquist 의 한 원호
  안에서 P2 와 P3 를 갈라 보였고**, 그것이 입도 스윕·재가압과 짝을 이뤄
  **접촉 손실 대리량을 처음으로 주파수에 국소화**했다. 문제는 **개수와 높이에
  폭이 안 붙는다**는 것이지 도구 자체가 아니다.
- **"11호의 봉우리가 인공물이다" 고 하지 않는다.** 우리가 말하는 것은
  **인공물의 상한이 본문 효과보다 크다** 까지다 (위 단서 셋).
- **"올바른 개수" 를 제시하지 않는다.** 이 페이지의 요지는 정반대다 —
  **개수를 고르는 규칙이 문헌에 없다**는 것이고, 후보(AIC)는 10호가 `[인쇄]`
  "only recently applied to **simulated** data" 로 열어 두었으며 **11호도
  쓰지 않았다**.
- **Q4 가 측정됐다고 하지 않는다.** `assb` **0 / 11 편**이다.
- 수치는 전부 **사본**이다. 그림에서 읽은 것은 `[도표]` 이고 판독 오차가 붙는다.

## 관련
- [[assb-contact-loss-vs-lampe]] — 닻. Q4 의 다섯 번째 변신이 기록돼 있다
- [[fitting-degeneracy]] — 파라미터 값의 축퇴. **이 페이지는 그 위층(모델 차수)이다**
- [[near-optimal-set-width-measurement]] — 폭을 재는 기계. §"적용 2" 가 이식 설계
- [[assb-lampe-contact-product-degeneracy]] — 곱 축퇴. `R_MF`/`P3` 가 같은 문제의 EIS 판
- [[assb-pressure-reapplication-separation-test]] — 압력 연산자. 11호가 **비직교성 반례**를 붙였다
- [[zhang2020-eis-aging-dataset]] — EIS + ML 쪽에서 같은 비식별이 나타난 자리
