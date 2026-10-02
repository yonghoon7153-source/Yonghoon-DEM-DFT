---
title: DRT 봉우리 개수는 데이터가 정하지 않는다 — 상태·조작·장비·정규화의 함수
description: "The number of resolvable DRT peaks (and hence the order of any equivalent circuit fitted downstream) is not determined by the impedance data alone: it moves with cycle number, with interventions, with the measurement wiring, and with the unreported regularization strength"
created: 2026-09-22
updated: 2026-10-02
type: concept
tags: [assb, battery, degradation, research, eis]
sources: [raw/papers/truong2025_calendar-vs-cycle-aging-protocols-drt-assb.md, raw/papers/oruemendizabal2023_multiconfiguration-geis-drt-nmc622-lpscl-li-interfaces.md, raw/papers/yu2024_drt-time-resolved-aging-sulfide-assb-fullcell.md, raw/papers/vadhva2021_eis-for-assb-theory-methods.md, raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md, raw/papers/su2024_drt-soh-health-features.md, raw/papers/kouhestani2022_phm-solid-state-batteries-perspective.md, raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md, raw/papers/fukunishi2023_ncm523-three-electrode-impedance-degradation.md, raw/papers/yoshida2024_four-electrode-assb-cell-li-transport.md]
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

## ★★★ 세 번째 경보 — **부분의 합이 전체가 아니다** (2026-09-22, `assb` 16호)

`raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md`.
16호는 **3전극으로 양극·음극·완전지 임피던스를 같은 셀에서 따로 재고**, 셋을 **같은 λ·같은
소프트웨어**로 DRT 변환한다. 그래서 이 계보에서 처음으로 **DRT 분해의 가법성을 직접 검사할
수 있는 자료**가 생겼다. **결과는 어긋난다.**

`[도표]` **Fig. 3(b), 389 MPa · 양극 117 µm** (γ(τ) / Ωcm²):

| 봉우리 | 완전지(보라) | 양극(파랑) | 음극(빨강) |
|---|---:|---:|---:|
| τ ≈ 1·10⁻⁴ s | **1.55** | **0 (없다)** | 0.22 (τ≈4·10⁻⁴) |
| τ ≈ 4·10⁻³ s | **3.1** | **4.6** (τ≈8·10⁻³) | ~0 |
| τ ≈ 3·10⁻¹ s | 2.15 | 0.88 (τ≈5·10⁻¹) | 1.45 (τ≈2.5·10⁻¹) |

★★★ **세 가지가 동시에 깨진다**:
1. **완전지의 가장 빠른 봉우리(γ≈1.55)가 양극·음극 어느 스펙트럼에도 없다.**
   그런데 본문은 `[인쇄]` "작은 시상수 **2 개**는 **양극**에 배정" 이라 쓰고,
   Fig. 4 는 그 봉우리를 **양극–집전체 계면**이라 부른다.
2. **부분이 전체보다 크다** — 양극 단독 4.6 > 같은 대역 완전지 3.1.
   **Nyquist 에서는 합이 맞는다**(`[인쇄]` 2E = 3E 합, 10 kHz 아래).
3. **봉우리 위치가 옮겨 간다** — 양극 단독 τ≈8·10⁻³ ↔ 완전지 τ≈4·10⁻³ (**2 배**).

그리고 `[도표]` **Fig. 3(d), 97 MPa** 에서는 **양극의 느린 봉우리(τ≈2 s, γ≈1.1)가
완전지에 없다.** 논문은 **음극의 작은 봉우리가 완전지에 없다는 사례만** 적는다
(`[인쇄]` "too low to be resolved").

★★★ `[해석]` **이것이 이 페이지의 논지가 실측으로 나타난 가장 깨끗한 형태다.**
11호는 "같은 봉우리의 **이름표**가 흔들린다" 였고, **16호는 "분해 자체가 변환 단계에서
다시 깨진다"** 다. **전기화학적으로 분해(3전극)한 뒤에도 수학적 분해(DRT)가 그것을
보존하지 않는다.**

원인 후보 셋 (**논문은 셋 다 검토하지 않는다**):
- (ㄱ) **세 스펙트럼의 채택 주파수 대역이 다르다** — `[도표]` Fig. 3(a) 에서 완전지는
  ~2·10⁴ Hz 까지 채워져 있고 양극은 ~5·10³ Hz 까지다 (속 빈 마커 = 제외점).
  **대역 끝 인공물**은 이 페이지 §"추가 경보 (2)" 에서 이미 본 기구다.
- (ㄴ) 정규화가 **스펙트럼 전체 크기에 상대적으로** 작동한다 (λ 가 절대값이면
  크기가 다른 세 스펙트럼에 다른 강도로 걸린다).
- (ㄷ) 3전극 인공물 — `[인쇄]` "nonideal positioning … cannot be avoided completely".

★★ **우리 폭 측정기가 붙는 두 번째 자리 (구체적)**:
```
λ 를 격자로 흔든다  →  각 λ 에서  D(λ) ≡ ‖ DRT(양극) + DRT(음극) − DRT(완전지) ‖
                    →  D(λ) 의 최소값과 그 위치를 보고한다
```
`[해석]` **이것은 "DRT 분해의 재현 가능한 오차" 를 처음으로 숫자로 만드는 절차**이고,
11호의 nuisance 1 점(배선 교체)과 달리 **정답이 알려진 검사**다 (합은 보존돼야 한다).
⚠ 16호 원시 데이터는 `[인쇄]` "available **on request**" 라 **지금은 못 돌린다.**

## ★★★★ 네 번째 경보 — **주파수 → 전극 규칙은 양극 미세구조의 함수다** (2026-09-22, `assb` 18호 ↔ 16호)

이 페이지는 지금까지 **"봉우리 개수"** 를 다뤘다. 18호와 16호를 맞대면 **그 앞 단계 —
"어느 봉우리가 어느 전극인가" — 도 데이터가 정하지 않는다**는 것이 보인다.

| 편 | 양극 | 저주파(≲1 Hz) 반원 |
|---|---|---|
| **16호** Ramanayagam 2026 | **단결정** NMC 83\|6\|11 | **없다** → `[인쇄]` 결론 "저주파 = 주로 **음극**" |
| **18호** Fukunishi 2023 | **다결정** NCM523 (2차 입자) | **있다** — `R4` ≈1 Hz, `[인쇄]` **2차 입자 내 1차 입자 간 전하이동** = **양극** |

★ **두 편이 서로를 인용하며 동의한다.** 16호는 `[인쇄]` "Fukunishi 는 **저주파 반원을
하나 더** 봤고 그것을 **2차 입자의 전하이동**으로 돌렸다. 이 논문은 **단결정**을 써서
그 반원이 없다" 고 적고, 18호는 `[인쇄]` "The existence of **R4 is apparent when the
three-electrode cell is applied to separate the Li-In component**, which significantly
affects the low-frequency behavior" 라고 적는다.

⇒ `[해석]` **같은 화학(In-Li 음극 + 황화물 + 층상 양극)에서도 양극 활물질의 형태가
"저주파 = 음극" 규칙을 깬다.** 10호(Vadhva)가 **화학**으로 보인 것
(`[인쇄]` In–Li 셀과 Li 금속 셀은 귀속이 반대, "**system-by-system basis**")에
**미세구조**라는 축이 하나 더 붙는다.

★★ **그리고 이것이 하류에 무엇을 하는가**: 18호의 `R4` 는 노화에서 **9.3 배**(LPSI)
자라고 논문이 **용량 손실의 원인**으로 지목하는 성분이다. 만약 3전극이 없었다면
그 성분은 **음극 기여와 같은 대역에 묻혔을 것**이고 — 논문 자신이 그렇게 말한다 —
**"음극이 열화했다" 로 읽혔을 것이다.**
⇒ **DRT 봉우리에 전극 이름표를 붙이는 유일하게 안전한 길은 전극을 물리적으로
분리하는 것**이고, 그것조차 16호에서 **DRT 단계에서 다시 깨진다**(세 번째 경보).

⚠ **두 편 다 이 함의를 "규칙이 없다" 로 일반화하지 않는다** — 16호는 자기 셀에 그
반원이 없다는 관찰로, 18호는 있다는 관찰로 끝낸다.

## ★★★★ 다섯 번째 경보 — **상대극이 전 대역에 걸쳐 있다, 그리고 저자가 그렇게 인쇄한다** (2026-09-22, `assb` 19호)

`raw/papers/yoshida2024_four-electrode-assb-cell-li-transport.md`
(Yoshida, Ikezawa, Okajima, Arai, *Electrochim. Acta* **497** (2024) 144523, **CC BY**;
18호와 같은 연구실). ⚠ **이 편은 DRT 를 쓰지 않는다**(`DRT`·`Kramers`·`regulariz*`
**0 회**) — 등가회로만 쓴다. 그런데 이 페이지에 들어오는 이유가 있다.

19호는 **Li-In 상대극 자신의 임피던스를 3전극으로 따로 잰다**(Fig. S5: WE = 왼쪽 Li-In,
RE = 왼쪽 R-LTO, CE = 오른쪽 Li-In). 결과:

> `[인쇄]` "the Li-In electrode showed semicircles in the frequency ranges **overlapping
> with P1 (above ca. 1 kHz) and P2 (ca. 1 kHz to 0.1 Hz)**."
> `[인쇄]` "the impedance spectra of the Li-In electrodes … **does not match well, showing
> poor reproducibility of the InLi impedance**."
> `[인쇄]` "These results show that **P1 and P2 are difficult to extract from the impedance
> measured with the two-electrode system with InLi counter electrodes**."

`[도표]` **같은 공칭 Li-In 박(Li : In = 25 : 75 at%)의 전극 저항이 39 / 172 / 54 Ω —
4.4 배 (n = 3).**

★★★★ **이것이 계보의 다섯 번째이자 가장 아래 층이다.**

| 층 | 편 | 무엇이 흔들리는가 |
|---|---|---|
| 1 | 10호 Vadhva | 역변환이 **ill-posed**, 귀속이 **화학의 함수** |
| 2 | 11호 Yu | 봉우리 **이름표가 상태·배선·조작**으로 (−15 … +69 %) |
| 3 | 16호 Ramanayagam | 전극별 DRT 의 **합이 완전지 DRT 가 아니다** |
| 4 | 18호 Fukunishi | **양극 미세구조**(단결정 ↔ 다결정)가 "저주파 = 음극" 을 깬다 |
| **5** | **19호 Yoshida** | ★ **음극 자체가 1 MHz – 0.1 Hz 전 대역에 걸쳐 있다** |

⇒ ★★★ `[해석]` **4 층과 충돌이 아니라 보강이고 한 층 아래다** — 18호는 "양극을 바꾸면
저주파가 바뀐다" 고 했고, 19호는 "**양극을 바꿔도 음극은 그대로 거기 있다**" 고 말한다.
⇒ **주파수만으로 성분을 전극에 배정하는 모든 절차는, 같은 셀 안에서 배선으로
검증되기 전까지 가설이다.**

★★★★ **그리고 19호는 해법이 알고리즘이 아니라 배선임을 보인다.**
`[인쇄]` Fig. S1 이 셋을 나란히 놓는다: **4전극 = 계면 구간만** · **3전극 = + 작업전극
분극** · **2전극 = + 상대극 분극**. `[재현]` 그 대가의 크기: **상대극 가지의
`ΔE/ΔI` 가 44 / 221 / 83 Ω 로 같은 셀 계면 저항(21.5 / 12 / 29.3 Ω)의 2–18 배**다.
⇒ **분해가 어려운 것이 아니라, 2전극에서는 분해할 정보가 애초에 섞여 들어온다.**

⚠⚠ **다만 19호 자신의 성분 귀속도 같은 병을 앓는다.**
- **`P3`** 는 `[인쇄]` "we **deduce** … the ion transport at the **crack**" 으로만
  정체가 붙는다 — 근거는 **시상수 위치**와 **셀마다 크기가 다르다**는 것뿐이고,
  균열의 직접 관찰은 **0**(`crack` 본문 1 회). `[도표]` 그 크기가 **4.8 Ω ↔ ≈35 Ω (7 배)**
  로 흔들리고 **`P2` 바로 옆 주파수**에 있는데, **`P2` 적합의 `P3` 민감도 검사가 0** 이다.
- **`P1`** 의 꼭짓점이 `[재현]` **측정 상한(7 MHz) 밖**이다(Table 2 의 특성 주파수
  2.4×10⁷ · 9.4×10⁶ Hz — 인쇄값은 지수 부호가 틀렸다) ⇒ **`R₁` 은 외삽값**이고,
  `[도표]` 한 셀은 원호 208 Ω 중 **26 %** 만 측정됐다.
- 그리고 **"RE artifact 가 아니다" 의 근거가 진폭 비의존성**이다 —
  **선형성을 보지 기원을 보지 않는다**(18호의 K–K 잔차와 같은 구조).
  ⇒ **체크리스트 C2 에 "K–K 를 돌렸나" 뿐 아니라 "무엇을 주장하는 데 썼나" 를 같이 본다.**

## ★★★ 여섯 번째 경보 — **창 밖 봉우리가 이름을 얻는다 · 같은 이름표의 τ 띠가 그림마다 움직인다 · γ 정규화 미인쇄** (2026-09-29, `assb` 84호)

`raw/papers/oruemendizabal2023_multiconfiguration-geis-drt-nmc622-lpscl-li-interfaces.md`
(Orue Mendizabal, Cheddadi, Tron, Beutl, López-Aranguren, *ACS Appl. Energy Mater.* **6** (2023) 11030, CC BY-NC-ND 4.0;
NMC622 \| Li₆PS₅Cl \| Li 금속 · 네 구성(Li\|Li · Li\|In · NMC\|Li · NMC\|In) · 2전극 · 전류 인가 중 EIS 1 MHz–0.1 Hz · DRTtools · 25호 ref 23).

11호의 추가 경보 (2) 는 측정 하한(0.1 Hz) 밖 봉우리가 **이름 없이** 서 있었고, 19호 P1 은 **고주파 끝 밖**(측정 상한 위 꼭짓점 → `R₁` 외삽)이었다. 84호는 저주파 끝 밖 봉우리에 **이름과 기구를 붙이고, 표에서는 창 안 주파수로 인쇄한다.**

- **창 밖 봉우리.** 저자 자신의 규약(`[인쇄]` "R3 (10−3−10−1 s) and R3\* (1−10 s) … correspond to 2−200 Hz and 20−200 mHz" — f = 1/(2πτ))으로 최저 0.1 Hz 는 **τ_max ≈1.6 s** 다. `[도표·화소]` 완전지 R3\* ≈3.8 s · R4\* ≈9.5 s 는 창 밖이고, DRT τ 축은 10²–10³ s 까지 그려진다. 표 S3 는 R3\* · R4 · R4\* 를 모두 "0.1 – 0.2 Hz"(τ 0.8–1.6 s)로 인쇄 — R4\* 의 그림 자리(≈0.017 Hz)와 ×6–12 어긋난다. `[재현]` 3.41 V 곡선 면적의 ≈18 % 가 창 밖이다.
- **이름이 창 밖 봉우리에 붙는다.** R4 · R4\* = 공간전하층(`[인쇄]` "we could tentatively ascribe these peaks to a SCL process" — DFT [61] · STEM [62] 인용) · R3\* = 본문 "additional diffusive processes" ↔ 표 S3 "Grain boundary effect". 그리고 SOC 배정이 걸린 방전 끝(<3.5 V)은 드리프트 조건(`[인쇄]` "5−10 times lower than the AC amplitude (at voltages above 3.5 V)") 밖이다.
- **같은 이름표의 τ 띠가 그림마다 1–2 자릿수 움직인다**(`[도표]`): R2 — 그림 2e ≈1.5–8×10⁻⁵ · 4d ≈2×10⁻⁵–2×10⁻⁴ · S2b ≈10⁻⁴–10⁻³ s · R3 — 2e ≈2×10⁻³–5×10⁻² · 4d 10⁻³–10⁻¹ · 3e ≈10⁻²–10 · S2b ≈1.5×10⁻²–60 s. **이름은 회로 순서를 따르고 τ 는 따르지 않는다** — 위 §"이름표의 불확정성이 이름표 간격보다 크다"(11호 P3 1.3 자릿수)의 한 편 · 여러 그림 판.
- **γ 정규화 미인쇄.** 축 단위 "Ω·decade⁻¹"(면적 정규화 · 로그 밑 미인쇄) · 오프셋 · 축척("scale 1:2 / 1:3") 캡션 없음. `[재현]` 그림 2e 는 "Ω·cm² per decade" 또는 "Ω per ln τ" 해석에서 같은 상태 적합 합과 맞고, 그림 5c 는 같은 스펙트럼 5a 와 "Ω per decade(면적 정규화 없음)" 해석에서만 맞는다 — **두 그림이 한 정규화로 함께 맞지 않는다** ⇒ 봉우리 **크기**를 그림 사이에서 비교하지 않는다(판독 · 가정 위).
- **두 전극 CT 가 같은 τ 에 겹친다고 문장으로 인쇄한다.** `[인쇄]` "The signals for both cells are within the same relaxation time for the (RQ)1, (RQ)2, and (RQ)3 processes" — 11호 추가 경보 (1)(P4 음극 · P5 양극 CT 를 ≈10 Hz 에 겹쳐 그림)의 문장판이고, 11호처럼 **설계**(대칭 셀 빼기 · 상대극 교체)로 가른다.

⇒ ★★ `[해석]` 다섯 번째 경보의 층 표에 한 줄을 더하면: **6 · 84호 Orue Mendizabal — 측정 창 밖(저주파) 봉우리와 그림 사이 τ 띠가 이름표를 흔든다.** 체크리스트에 "봉우리 τ 가 τ_max = 1/(2π f_min) 안인가" 를 칸으로 올릴지는 **결정하지 않았다**(84호 digest 새 판단 거리 2).
⚠ 이 편의 **가장 단단한 배정**은 DRT 모양이 아니라 **전류 방향 연산자**다 — Li\|SE R2 가 한 스텝 안에서 자라고 역전류에서 초깃값 쪽으로 돌아간다(`[도표·화소]` 그림 2c). 개수 · 모양이 흔들려도 이름을 붙이는 다른 채널이 있다는 것이 이 경보의 반대쪽 단서다.

## ★★★ 일곱 번째 경보 — **λ 를 고르지 않는 역변환 위에서도 이름표는 τ 창이 정한다 · 지배 봉우리가 다른 이름의 창으로 넘어가도 연속성이 이름을 유지한다 · 같은 τ 대역에 정전용량이 세 자릿수 다른 두 요소가 산다** (2026-10-02, `assb` 90호)

`raw/papers/truong2025_calendar-vs-cycle-aging-protocols-drt-assb.md`
(Truong, Whang, Huang J., Sandoval, Zeier, *J. Mater. Chem. A* **13** (2025) 17261, CC BY 4.0;
In/InLi \| Li₆PS₅Cl \| NCM83 : Li₆PS₅Cl 반쪽 · 48 h 정전위 유지(매 시간 EIS · 유지 전위) ↔ ≈48 h 1C 사이클(두 사이클마다 EIS · 방전 끝 30 분 휴지 뒤) · 7 MHz–50 mHz · 10 mV rms · hybrid-drt · **예치 원자료**(시간분해 DRT 261 + 형성 · RPT)).

11호(DRTtools · λ 미인쇄) · 84호(DRTtools · 창 밖 봉우리 이름)와 달리 이 편은 **λ 를 사람이 고르지 않는다** — `[인쇄]` ESI "we apply the self-tuning DRT inversion algorithm implemented in the python package hybrid-drt by Huang et al. This uses a hierarchical Bayesian model to obtain the maximum a posteriori estimates of the DRT without manual parameter tuning" · K–K 통과 인쇄 · τ 기저를 측정 창 밖으로 1 자릿수씩 확장. 사전 · 초모수 · 불확실성 출력은 미인쇄(λ 는 "수동 0" 이지 "없음" 이 아니다). 그러나 **이름표 층은 그대로다.**

- **이름 = 문헌 τ 창.** `[인쇄]` P_SE ∼10⁻⁸ · P_C1 10⁻³–10⁻² · P_C2 10⁻²–10⁻¹ · P_A 10⁻¹–1 · P_D ∼10 s — 근거는 문헌[31,33,34]이고 대칭셀 · 3전극 · 구성 교체 · 온도 · 정전용량 대조는 0. [33] = 11호인데 11호 양극 봉우리 P3 ≈500 Hz 는 `[재현]` τ ≈3.2×10⁻⁴ s — 이 편 P_C1 창의 3–30 배 짧은 쪽이다(다른 셀 · 상태 · 압력 — [33] 은 이 편 τ 대역의 값 근거가 못 된다 `[해석]`).
- **창을 넘는 이동은 연속성이 덮는다.** `[데이터]` 3.9 · 4.1 V 유지 48 h 의 지배 봉우리 τ 0.19 · 0.54 s 는 **P_A 창(10⁻¹–1 s) 안**인데(1 h 에는 5.4 · 17 ms) 2D DRT 의 연속 이동으로 "P_C" 이름을 유지한다.
- ★ **정전용량 검사가 처음 값을 낸다** — 저자 `C` 인쇄 0, 우리 `[재현]` C_eff = τ_peak ÷ 골–골 ∫γ d ln τ: calendar 지배 봉우리 **1.6–2.5 µF 로 평탄**(τ ×5.7–35 · R ×4.2–27.6) → 같은 요소의 R 성장 — 연속성 이름 유지가 **지지된다**. 같은 τ 대역의 cycle P_A 는 **≈1.5–3.3 mF**(기하 면적당 이중층 ≈10 µF cm⁻² 의 ×190–520) — **같은 창에 세 자릿수 다른 두 요소**가 산다. τ 창만으로는 둘을 가를 수 없고 C 가 가른다.
- **창 밖 몫.** `[데이터]` τ 격자 284 점(2.1×10⁻¹¹–3.4×10³ s) · 전형 DRT(그림 4)의 측정 하한(τ_max 3.18 s) 밖 몫 257 / 970 Ω(**26 %**) — P_D(τ ≈10.5 s)가 창 밖인데 "solid-state lithium diffusion process within the cathode electrode" 이름을 얻는다(저자 스스로 `[인쇄]` "the relaxation of PSE and PD occurs largely out of the measured frequency range") — 84호(창 밖 R3\* · R4\*)에 이은 둘째 표본.
- **개수.** `[인쇄]` "The DRT in this work generally indicates five main peaks" ↔ `[데이터]` 전형 DRT 의 국소 극대 다섯 중 하나는 이름 없는 작은 봉우리(7.9×10⁻⁷ s · 4.4 Ω)이고 **P_C2 는 극대가 아니라 어깨**다 — 이름표 다섯과 극대 다섯이 같은 집합이 아니다.
- **상태 · 기준선.** 시간분해 EIS 는 calendar = 유지 전위(고 SOC — 1 h 스펙트럼부터 R_tot 0.81 · 3.5 · 9.3 kΩ) · cycle = 1C 방전 끝(사이클마다 표류) · RPT = 0.1C 방전 끝이고, 그림 6 "before aging" 은 한 셀 스펙트럼을 여섯 셀 공통 기준으로 쓴다(신품 저주파 Re 산포 694–1019 Ω `[도표·화소]` S4) — 자기 셀 기준이면 cycle 셀 저주파 Re 는 −40 · −30 · −4 Ω.

⇒ ★★ `[해석]` 다섯 번째 경보의 층 표에 한 줄을 더하면: **7 · 90호 Truong — 역변환 설정(λ)을 자동화해도 이름표 층(τ 창 · 연속성)은 그대로이고, 같은 τ 창에 C 가 세 자릿수 다른 요소가 공존한다.** 체크리스트에 "τ 창을 넘는 봉우리의 C_eff 연속성" 을 칸으로 올릴지는 **결정하지 않았다**([[assb-lampe-contact-product-degeneracy]] 일흔세 번째 적용의 후보 줄과 같은 내용).
⚠ 이 편의 강점도 적는다 — K–K 검사 인쇄 · λ 수동 조율 0 · **원자료 예치**(그래서 우리가 C_eff 를 낼 수 있었다). 11 · 84호에는 없던 것이다. 다만 예치 자료 자체에 그림 사이 불폐합 · 복사 구간이 있어(90호 D1 · D15) 시간분해 DRT 파일도 재현 입력으로 쓰기 전에 교차 검사가 필요하다.

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

★★ **2026-09-22 추가 — 16호(Ramanayagam 2026)가 C1 을 처음으로 통과한다.**

| # | 16호 |
|---|---|
| **C1** | ★ **✅ 계보 최초** — `[인쇄]` "**regularization parameter of λ = 0.05**", Gaussian RBF 이산화, 페널티 = **2 차 도함수**, **shape factor 0.5**, RelaxIS |
| C2 | ❌ K–K / Lin-KK **0 회** |
| C3 | ❌ DRT 불확실성 **0 회** |
| C4 | ❌ 봉우리 개수 선택 규칙 **0 회** (개수는 Nyquist 반원 개수와 맞춰 사후 확인) |
| C5 | ❌ 반복 **0** (조건당 셀 1) |

★★★★ **2026-09-22 추가 — 18호(Fukunishi 2023)가 C1 과 C2 를 동시에 통과하고,
바로 그 통과가 이 페이지의 논지를 가장 선명하게 예시한다.**

| # | 18호 |
|---|---|
| **C1** | ✅ **λ 값 둘 다 인쇄** — `[인쇄]` LPSI **λ = 6.0 × 10⁻²**, LPSCl **λ = 8.5 × 10⁻⁴**. ⚠⚠ **70 배 다르다** |
| **C2** | ★ **✅ 계보 최초** — `[인쇄]` "proven to satisfy the **Kramers-Kronig** … using **Lin-KK tools** (KIT [30]), and **residuals were less than 0.40**" (SI Fig. S1·S2 에 잔차 6 패널) |
| C3 | ❌ DRT 불확실성 0 |
| C4 | ❌ 개수 선택 규칙 0 — ⚠ 그 반대다(아래) |
| C5 | ❌ 반복 0 (`n =` 0 회) |

★★★★ **C4 가 단순한 ❌ 가 아니라 반대 방향이다 — 개수가 λ 의 목표다.**
`[인쇄]` "the independent components of R2 to R4 are **confirmed by using λ = 8.5 × 10⁻⁴**
as the regularization parameter" · `[인쇄]` "We were able to **confirm the independent
components of R2, R3 and R4, by applying adequate regularization parameters**".
⇒ **λ 를 골라서 원하는 개수가 나오는지 확인한다.** 그리고 그 개수가 하류로 흐르는
사슬이 같은 지면에 인쇄돼 있다:

> `[인쇄]` "First, the **time constants obtained from the DRT analysis were fixed** and the
> other parameters were refined. Then, all the valuable parameters in the equivalent circuit
> were refined."
>
> ⇒ **λ → 봉우리 개수·위치 → 등가회로의 차수와 고정 시상수 → `R3`/`R4` 의 값 →
> "열화의 주 원인" 판정.**

`[해석]` 11호는 λ 를 **안 적었고**, 16호는 **적었고**, **18호는 적은 뒤 그것으로 개수를
확인한다** — 세 편이 같은 축의 세 지점이다. **가장 투명한 편이 동시에 가장 명시적으로
이 문제를 겪는다**는 것이 요점이다.

★★ **그리고 λ 의 차이가 재료의 차이와 구별되지 않는다.** `[도표]` SI Fig. S1(LPSI,
λ = 6.0×10⁻²)은 **완만한 혹 3 개**(신품에서는 골/마루 비가 **1.3–1.7** 에 불과하다),
SI Fig. S2(LPSCl, λ = 8.5×10⁻⁴)는 **날카로운 봉우리 4 개**(≈10⁶ Hz 에 높이 190 의 첨봉
`P_R1′` 포함)를 보인다. 논문은 그 추가 봉우리를 **재료 탓**으로 돌린다 —
`[인쇄]` LPSCl 의 낮은 Young 계수(22.1 ↔ 30, **단위 없음**, 제일원리 계산값) → 입자 간
접착 부족 → **void** → 용량성 성분.
⚠ **λ 를 같게 두고 비교한 그림이 없다** ⇒ **"봉우리가 하나 더 있다" 와 "정규화가 70 배
약하다" 가 이 지면에서 구별되지 않는다.**

⚠ **C2 의 통과에도 단서가 둘**: ① `[도표]` 잔차 축 라벨이 **"Residuals / −"(무차원)** 인데
값이 저주파에서 **±0.2 … ±0.4** 까지 간다 — Lin-KK 관례(% 단위, |Δ| < 1 %)와 자릿수가
다르다. ② 그 잔차를 `[인쇄]` **"suggest the stability of the reference electrodes"** 의
근거로 쓴다 — **K–K 는 스펙트럼의 선형·인과·정상성을 보는 검사이고 기준극의 DC 전위를
보지 않는다.** ★ `[해석]` **C2 를 통과하는 것과 그 결과를 옳게 쓰는 것은 다른 일이다.**

⚠ **그리고 C1 의 통과가 부분적이다**(16호): λ 값은 있는데 **선택 규칙(L-curve·GCV·CV)도,
λ 민감도도 없다.** `[인쇄]` 저주파(확산)·유도성·인공물 데이터를 "**제외**" 했다고만 적고,
**어느 점을 뺐는지는 Fig. 3 의 속 빈 마커로만** 표시된다 (좌표 미인쇄).
`[해석]` **λ 를 적는 것은 재현의 최소 조건이지 유일성의 근거가 아니다.**

★★ **2026-09-29 추가 — 84호(Orue Mendizabal 2023 *ACS Appl. Energy Mater.*)는 C2 만 명명 수준에서 통과하고, 봉우리 배정을 개수 규칙 대신 구성 교체 · 전류 방향으로 한다.**

| # | 84호 |
|---|---|
| C1 | ❌ **0** — `[인쇄]` "DRTtools code based on Tikhonov regularization"(인용 [32] Wan 2015 · [33] Clematis 2021) 한 문장 · λ · 이산화 · 도함수 차수 · τ 격자 0 |
| C2 | ✅ 명명 — Lin-KK · `[인쇄]` "within the limit of 1%" — 잔차 그림 · 대상 스펙트럼 목록 0 |
| C3 | ❌ "within the uncertainties of the DRT and EC methods"(수치 0) |
| C4 | ❌ — 띠를 그림마다 손으로 긋고, R3\* · R4 · R4\* 는 저주파 끝에 더한 이름(위 여섯 번째 경보) |
| C5 | ❌ 셀 수 미인쇄 |

`[해석]` 개수 대신 **배정 연산자 넷**(구성 차 · 전류 방향 · SOC · 문헌 `C` 대역)이 봉우리에 이름을 붙인다 — 온도(`Ea`)는 0. ⚠ 18호 단서("C2 를 통과하는 것과 그 결과를 옳게 쓰는 것은 다른 일")가 여기도 선다: 진폭 20–50 mV 는 RT/F 와 같은 자릿수이고 `[재현]` AC 전류가 DC(0.08 mA cm⁻²)의 ×0.9–5 다 — Lin-KK 는 인과 · 정상성 검사이지 비선형 검사가 아니다.

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
- **Q4 가 측정됐다고 하지 않는다.** `assb` **0 / 16 편**이다 (2026-09-22 갱신).
- ★ **16호가 λ 를 인쇄했다고 해서 그 DRT 가 유일하다고 하지 않는다.** C1 하나만 통과했고
  C2–C5 는 ❌ 다. 그리고 **같은 논문에서 가법성이 깨진다** — λ 보고는 **재현의 최소 조건**이지
  유일성의 근거가 아니다.
- ★ **16호의 가법성 파탄이 어느 원인(대역·정규화·3전극 인공물)인지 단정하지 않는다.**
  우리가 확인한 것은 **파탄 자체와 그 크기**(완전지에 없는 봉우리 2 개, 부분 > 전체)까지다.
- 수치는 전부 **사본**이다. 그림에서 읽은 것은 `[도표]` 이고 판독 오차가 붙는다.
- ★ **84호의 창 밖 봉우리(R3\* · R4\*)가 인공물이라고 하지 않는다** (2026-09-29) — 측정 창 밖이고 이름 · 주파수 표기가 표 S3 와 그림에서 어긋난다는 것까지다. 공간전하층 · 확산 과정이 없다는 뜻이 아니다. γ 정규화 판독(그림 2e ↔ 5c)은 우리 `[재현]` · 가정 위다.
- ★ **90호의 cycle P_A 가 음극 계면이 아니라고 하지 않는다** (2026-10-02) — 이름표가 τ 창 가정 위이고 C(≈mF)가 이중층 "전하 이동" 상한을 넘는다는 것까지다(합금 화학 용량 등 다른 해석은 이 편 자료로 가를 수 없다). 그리고 **C_eff 를 저자 값으로 인용하지 않는다** — 예치 DRT 위 우리 판독(골–골 적분 · 창 경계 ±≈30 % · 기하 면적)이다. hybrid-drt 의 자동 λ 가 개수 · 높이의 폭을 준다고도 하지 않는다 — 사전 · 불확실성 출력이 미인쇄다.

## 관련
- [[assb-contact-loss-vs-lampe]] — 닻. Q4 의 다섯 번째 변신이 기록돼 있다
- [[fitting-degeneracy]] — 파라미터 값의 축퇴. **이 페이지는 그 위층(모델 차수)이다**
- [[near-optimal-set-width-measurement]] — 폭을 재는 기계. §"적용 2" 가 이식 설계
- [[assb-lampe-contact-product-degeneracy]] — 곱 축퇴. `R_MF`/`P3` 가 같은 문제의 EIS 판
- [[assb-pressure-reapplication-separation-test]] — 압력 연산자. 11호가 **비직교성 반례**를 붙였다
- [[zhang2020-eis-aging-dataset]] — EIS + ML 쪽에서 같은 비식별이 나타난 자리
