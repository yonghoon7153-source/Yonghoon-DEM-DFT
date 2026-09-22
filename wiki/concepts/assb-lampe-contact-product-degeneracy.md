---
title: "복합양극 동역학 항의 곱 축퇴 — LAM_PE 와 접촉 손실이 A_eff·ε_p/R_s 한 조합으로만 들어간다"
description: "In a published composite-cathode ASSB P2D model the Butler-Volmer denominator sees only the product A_eff x eps_p / R_s, so active-material loss, contact-area loss and particle radius are not separately identifiable from a discharge curve; a second, experimental paper (three-electrode EIS + transmission-line model) stands on the same product and assigns all of it to the exchange current density"
created: 2026-09-22
updated: 2026-09-22
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md, raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md, raw/papers/vadhva2021_eis-for-assb-theory-methods.md, raw/papers/kouhestani2022_phm-solid-state-batteries-perspective.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: theoretical
evidenceScope: multi-source-primary
---

# 복합양극 동역학 항의 곱 축퇴 (`A_eff · ε_p / R_s`)

> `assb` 축의 **다섯 번째** 개념 페이지다. 닻은 [[assb-contact-loss-vs-lampe]].
> 앞의 넷: [[composite-cathode-percolation-utilization]] (`θ_AM`) ·
> [[assb-apparent-capacity-decomposition]] (3 항 분해) ·
> [[assb-pressure-reapplication-separation-test]] (압력 되돌림) ·
> [[assb-stack-pressure-operating-window]] (압력 창).
>
> ★ **이 페이지가 앞 넷과 다른 점**: 앞 넷은 *현상*(접촉 손실이 존재한다)을 다룬다.
> 이 페이지는 *역문제*(그 존재량이 유일하게 정해지는가)를 다루고,
> **그 답이 "아니다" 라는 것을 출판된 모델의 인쇄된 식에서 손으로 보인다.**

## 어디서 왔나

Huo et al. 2025 (*J. Power Sources* **627**, 235830, raw:
`raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md`) 는 이 계보에서
**실험과 파라미터 식별을 한 논문 안에서 잇는 첫 편**이고, 그래서 처음으로
**열화 모드의 지분 자체를 적합으로 정한다** (`ε_p` 하나를 푼다).
그 논문의 Table 1 · Table 3 만으로 아래가 나온다.

## 정의 — 데이터가 보는 조합

원전 Table 1 의 **인쇄된 식**을 그대로 옮기면 (`[인쇄]`):

```
BV 전류밀도    j^p_ct = (I − I^p_dl) / ( A^p_eff · a_{s,p} · A · L_p )
비표면적       a_{s,p} = 3 · ε_p / R_s
```

따라서 (`[해석]`, 이 조합은 원전이 쓰지 않는다):

```
            ★  과전압 η^p_ct 가 보는 것은   A^p_eff · ε_p / R_s   한 조합뿐이다  ★
```

`A^p_eff`(유효 접촉 면적비) · `ε_p`(활물질 부피분율) · `R_s`(입자 반경)
**셋이 동역학 항에서 완전히 축퇴한다.** 세 값을 각각 `c`·`c`·`1` 배 해도,
또는 `1`·`k`·`k` 배 해도 계면 동역학은 **정확히 같다**.

## 축퇴를 깨는 채널은 셋뿐이고, 하나만 강하다

| # | 채널 | `ε_p` 가 들어가는 방식 | 세기 |
|---|---|---|---|
| ① | **용량** `Q_max = ε_p·A·L_p·c^p_max·F·Δθ_p` | `ε_p` 단독 (× `c^p_max`·`Δθ_p`) | **압도적** — 방전곡선의 길이 |
| ② | 고체확산 BC `D_p·∂c_p/∂r|_{R_s} = −I/(a_{s,p}·A·L_p·F)` | `ε_p / R_s` (**`A_eff` 없음**) | 약함 — 농도 분극에만 |
| ③ | `κ_eff = κ_se · ε_se^brug`, `ε_se = 1 − ε_p` | `ε_p` 단독 | 약함 + **정의가 모호**(아래 ⚠) |

`[해석]` **그러므로 방전 V–Q 곡선 하나를 맞추는 절차에서 식별되는 것은 사실상
"용량 ÷ 신품 용량" 이다.** `ε_p` 에 붙은 "positive active material 의 부피분율"
이라는 물리 이름은 **모델이 붙여 준 것**이지 데이터가 가른 것이 아니다.
용량을 같은 만큼 줄이는 어떤 기구든 — 접촉 손실, 균열에 의한 고립, 구조 열화,
코팅 열화, 리튬 재고 손실 — **같은 `ε_p` 를 낸다.**

이것은 [[fitting-degeneracy]] 의 **flat valley** 를 1 차원에서 본 형태다.
액체셀의 `(α_PE, β_PE)` 축퇴와는 **자리가 다르다**: 저쪽은 *용량축 좌표끼리*,
여기는 **용량축 스케일 ↔ 동역학 면적**이다.

## ★ 원전 안에서 이미 9 배로 흔들린다 (`[재현]`)

원전이 인쇄한 값과 원전의 SEM 이 서로를 배반한다.

| | 값 | 출처 |
|---|---:|---|
| `A^p_eff` | **0.4938** | `[인쇄]` Table 3 |
| `ε_p` (fresh) | **0.321** | `[인쇄]` Table 3 · Eq. (2) |
| `R_s` | **9.466 µm** | `[인쇄]` Table 3 |
| `a_{s,p} = 3ε_p/R_s` | **1.017e5 m⁻¹** | `[인쇄]` Table 3 (✓ `[재현]` 검산 일치) |
| **SEM 의 NCM 입자 반경** | **≈1.05 µm** | `[재현]` Fig. 5a 픽셀 계측, 스케일바 0.8 µm = 40 px |

```
표의 조합            A_eff · a_{s,p} = 0.4938 × 1.017e5 = 5.02e4 m⁻¹
SEM 의 R_s 를 쓰면   a_{s,p} = 3×0.321/1.05e-6       = 9.17e5 m⁻¹
같은 곱을 맞추려면   A_eff = 5.02e4 / 9.17e5         = ★ 0.055
```

→ **"유효 접촉 면적비" 가 `0.055` 와 `0.494` 사이를 9 배로 움직인다.**
어느 쪽도 데이터가 배제하지 않는다. 원전은 `[인쇄]` "retaining the **actual
physical significance** of the parameters" 라고 쓴다.

⚠ **한계**: 입자 경계는 저자가 그린 초록 원으로 잡았고 SEM 은 표면 투영이라
최대 단면이 아닐 수 있다. 9 배를 뒤집으려면 원이 실제 입자의 1/9 이어야 한다.
단결정 NCM811 의 통상 크기(2–5 µm)도 SEM 쪽과 일치한다.

## ★ 두 번째 결과 — 열화를 한 노브로 돌리면 LAM 과 율 손실이 섞인다

원전은 노화 단계마다 **`ε_p` 하나만** 다시 적합한다. 그런데 `ε_p` 가 줄면
`a_{s,p} = 3ε_p/R_s` 도 같이 줄어 **분극이 커지고 컷오프에 더 일찍 닿는다.**

`[재현]` (원전 Eq. (2) + Fig. 7c/8c 판독):

| 셀 | `Δε_p/ε_p` | `ΔSOH` | **증폭** |
|---|---:|---:|---:|
| A (125 cyc) | 14.28 % | `[도표]` 22.9 % | **1.60** |
| B (140 cyc) | 7.44 % | `[도표]` 9.8 % | **1.32** |

`[해석]` **원전이 "활물질 손실" 이라 부르는 용량 감소의 ≈37 %(A 기준)는
모델 안에서조차 활물질 손실이 아니라 같은 노브가 만든 율 특성 저하다.**
그리고 증폭이 상수가 아니다(1.60 vs 1.32) — 동작점에 의존한다.

이것은 [[assb-apparent-capacity-decomposition]] 의 3 항 분해
(`Q_apparent = θ_AM · η(i) · Q_material`) 에서 **`θ_AM` 과 `η(i)` 가 한 파라미터에
묶여 버린** 경우다. 2호(Clausnitzer)에서 세운 **율 스윕 분리 시험**이 그대로
처방이 된다: **같은 데이터를 `i → 0` 으로 한 번 더 돌리면 `η` 성분이 사라진다.**

## ⚠ 세 번째 — `ε_se` 의 처리가 어느 쪽이든 모델이 깨진다

원전 신품에서 `ε_p + ε_se = 0.321 + 0.679 = 1.000` (정확). 노화 중 `ε_p` 가 줄 때:

- **`ε_se = 1 − ε_p` 를 유지하면**: `[재현]` `ε_p = 0.2752` → `κ_eff` 가
  `0.3985 × 0.7248^3.67 = 0.1223 S/m` → **신품 0.0963 대비 +27 %**.
  **모델이 "늙을수록 복합양극 이온전도가 좋아진다" 고 말한다** — 원전 자신의
  `[인쇄]` "cracking … **increases the tortuosity** … and **reduces the effective
  conductivity**" 와 정반대다.
- **`ε_se` 를 고정하면**: `ε_p + ε_se = 0.954` → **9.5 vol% 의 유령 공극**.

**원전은 어느 쪽을 택했는지 적지 않는다.** 그리고 어느 쪽이든 ③ 채널이
축퇴를 깨는 데 쓸 수 없게 된다.

## 무엇을 재면 깨지는가 (처방)

축퇴는 **여기(excitation) 부족**에서 온다. 곱을 가르려면 `A_eff` 와 `ε_p` 가
**다르게 반응하는** 자극이 필요하다.

| 처방 | 무엇을 가르나 | 값 |
|---|---|---|
| **율 스윕** (최소 2 율, `i → 0` 포함) | `η(i)` 를 지워 `θ_AM·Q_material` 만 남긴다 | ★ 2호 논지의 재사용 |
| **HPPC / 펄스** | 과전압을 용량과 독립으로 읽는다 → `A_eff·ε_p/R_s` 를 직접 | ★★ **원전이 수집하고 버렸다** |
| **다중 SOC EIS** | 같은 곱의 주파수 분해 | ★ 원전이 100/50/0 % 를 재고 100 % 만 썼다. ⚠⚠ **단독으로는 못 쓴다 — 아래 §"EIS 는 대가를 받는다"** |
| **압력 되돌림** | `θ_AM` 만 (부분) 복원 → 진짜 재료 손실과 분리 | [[assb-pressure-reapplication-separation-test]] |
| **`J^T J` 최소 고유벡터** | 이 곱이 실제로 null 방향인지 수치 확인 | [[fitting-degeneracy]] 의 "그리는 법" |
| ★★★ **`R_CT · C_dl` 짝** (2026-09-22 신설, 16호에서) | **`R_CT·C` 는 접촉 면적이 소거되는 조합**(고유 시상수), **`C` 단독은 접촉 면적에 비례** ⇒ **둘을 같이 보면 `θ` 와 `j₀` 가 갈린다** | ★★ **16호가 두 값을 다 인쇄해 놓고 조합을 안 만든다** (아래 §16호) |

★ **마지막 줄이 우리가 바로 할 수 있는 것이다.** 필요한 입력은 두 가지뿐:
반쪽전지 OCP 두 곡선(원전이 출처를 안 적었다)과 비공개 6 개 파라미터.

## ⚠⚠ EIS 는 대가를 받는다 — 두 번째 축퇴가 따라 들어온다 (2026-09-22, `assb` 10호)

위 처방표의 "다중 SOC EIS" 는 **곱을 주파수로 가르자**는 것이었다. 그런데
`assb` 10호(Vadhva et al. 2021, *ChemElectroChem* 8, 1930 — 이 분야 **유일한 EIS
방법론 리뷰**)를 넣고 보면 **그 통로에 다른 축퇴가 이미 앉아 있다.**

**(가) 같은 저항에 두 기구가 귀속된다.** In|LGPS|LCO 완전지의 SoC 분해 EIS 에서
중주파 **양극 계면 저항**의 증가를 원전이 이렇게 설명하고 리뷰가 그대로 옮긴다:

> `[인쇄]` "attributed to **loss of interfacial contact in the composite cathode
> due to volumetric expansion** **and** the **formation of a decomposition layer
> on exposed LCO**"

`[해석]` **접촉 손실**(우리의 `θ_AM`)과 **계면상 성장**(진짜 화학 열화)이
**하나의 `R_MF` 안에서 합쳐진다.** 가르는 관측은 원전에도 리뷰에도 없다.

**(나) 그리고 EIS 의 역문제도 유일하지 않다.** 같은 리뷰 §2.3 (`[인쇄]`):
- "**As no solution to an EIS spectrum is unique**"
- "**the inclusion of more elements will tend to improve the fit** of the
  equivalent circuit model" → **적합 잔차는 모델 선택의 근거가 못 된다**
- "it is often challenging to **decipher how many time constants are present** …
  their assignment can be **highly subjective**"
- DRT 로 개수를 정하려 해도 `[인쇄]` "data inversion is **mathematically
  ill-posed, requiring regularization methods**" 이고 "**very sensitive to
  experimental errors**"

**(다) 분해 가능한 원소의 개수 자체가 조건의 함수다.** 같은 리뷰가 다섯 곳에서
따로 보인다 — `[도표]` 황화물 5 종 중 **3 종만** 입계가 분해되고(같은 −130 °C),
LGPS 는 **실온에서 원호가 0 개**이며, Li|LLZO|Li 는 **400 MPa 에서 `R_int` 가
사라져야 `GB` 가 보이고**, 폴리머는 **60 °C 위에서 상경계 임피던스가 소멸**하며,
`[인쇄]` LiPON 박막은 **노화가 RQ 를 3 → 4 개로 바꾼다**(새 RQ 의 귀속은
`[인쇄]` "Li|LiPON interface **and/or** in the LCO bulk").

```
        시간·용량 영역 축퇴  ×  주파수 영역 축퇴  =  실제로 풀어야 할 문제
        (A_eff·ε_p/R_s)         (R_MF = 접촉 + 계면상)
```

★ **그러므로 처방표의 EIS 항목은 이렇게 고쳐 읽는다**: **EIS 단독으로는 안 되고,
"한 기구만 되돌리는 개입" 과 짝지어야 한다** — [[assb-pressure-reapplication-separation-test]]
의 `P↑`(접촉만 복원) 또는 상보 **대칭셀 쌍**(전극별 분리). 10호가 드는 유일한
"전극 귀속을 실제로 확정한" 사례도 주파수 추론이 아니라 **대칭셀 둘을 같은 조건으로
잰 것**이다(He 2017, LFP|PEM|LFP ↔ Li|PEM|Li).

★★ **보너스 — `P↑` 는 분해능 연산자이기도 하다.** `[도표]` 400 MPa 에서 `R_int` 가
사라지자 그 뒤에 숨어 있던 `GB` 원호가 드러난다. **압력은 `θ_AM` 을 되돌릴 뿐
아니라 관측 가능한 시상수의 개수를 바꾼다** → [[assb-stack-pressure-operating-window]].

⚠ **10호는 리뷰다** — 1차 측정 0, `contact loss` 0 회(위 인용구가 전부),
`identifiab*`·`uncertaint*` 전수 0 회. **재지 않았다.** 위에서 쓰는 것은 수치가
아니라 **방법론적 주장**이다.

## ★ 이 모델 형태는 9호 고유가 아닐 수 있다 — `A_eff` 의 계보 입구 (2026-09-22, `assb` 12호)

`assb` 12호(Sadegh Kouhestani et al. 2022, *Energies* 15, 6599 — ⚠ **PHM 종설, 1차 측정 0**,
`raw/papers/kouhestani2022_phm-solid-state-batteries-perspective.md`) §3.1.1 이 한 문장으로
같은 형태를 소개한다:

> `[인쇄]` "Tian et al. [60] and Shao et al. [60] introduced **a parameter to describe the
> contact area, which adjusts the current density in the 1-D Newman model**. They found
> that **the capacity drop was correlated with the loss of contact area**, and the optimal
> charging performance could be obtained under medium compressive pressures (0.4–1 MPa)."

`[해석]` "접촉 면적을 기술하는 파라미터가 1D Newman 모델의 **전류밀도를 조정**한다" 는
위 §정의의 `j^p_ct = (I − I^p_dl) / (A^p_eff · a_{s,p} · A · L_p)` 와 **자리가 같다** —
BV 분모의 유효 면적 인자. 즉 이 페이지가 손으로 보인 `A_eff · ε_p / R_s` 곱 축퇴는
**Huo 2025 가 만든 형태가 아니라 2017 년(Tian & Qi, *JES* 164, E3512)부터 있던 형태**일
가능성이 높고, Shao 2022 (*Energy* 239, 121929) 가 거기에 **압력 의존**을 얹었다.

**이것이 이 페이지에 뜻하는 것 둘**:
1. `evidenceScope: single-source` 는 **이때는 유지했다** — 12호는 식을 인쇄하지 않았고,
   원전 둘을 우리가 읽지 않았다. 다만 §"주장하지 않는 것" 의 "P2D 계열에 널리 반복될
   가능성" 이 **한 문장의 문헌 근거**를 얻었다.
   → **2026-09-22 늦게 `multi-source-primary` 로 승격**했다. 근거는 12호가 아니라
   **16호(식을 인쇄한 두 번째 1차 문헌)** 다 — 아래 §"두 번째 출처".
2. ★ Shao 2022 가 정말 `A_eff = A_eff(P)` 를 넣었다면, **압력 되돌림 연산자**
   ([[assb-pressure-reapplication-separation-test]])가 **모델 안에 이미 들어 있는** 첫 사례다
   — 그러면 곱 축퇴를 깨는 "다른 반응을 하는 자극" 이 그 모델에서는 **압력**이 된다.
   확인 전이다.

⚠ **단서**: 12호는 두 저자에 **같은 인용번호 [60]** 을 붙였다(Shao 는 [63] 이어야 한다).
그래서 `0.4–1 MPa` 가 어느 쪽 결과인지 **그 지면으로는 확정되지 않는다.** 이 절의 수치는
쓰지 않고 **형태**만 쓴다. 9호(Huo 2025)가 Tian & Qi 를 인용하는지도 **확인하지 않았다**.

## ★★★ 두 번째 출처, 그리고 **실측 판** — 16호가 같은 곱 위에 서서 한쪽 끝을 고른다 (2026-09-22)

`assb` 16호 (Ramanayagam, Miß, Leier, Duncker, Kirczek, Roling 2026, *Batteries & Supercaps*
**9**, e70315, `raw/papers/ramanayagam2026_stack-pressure-three-electrode-assb-impedance.md`)
는 **3전극 실측 + TLM 적합**이다. 9호가 **모델 논문**이었다면 16호는 **실험 논문**이고,
**같은 구조가 EIS 쪽에서도 나타난다**는 것을 보인다.

### 정의 — 같은 자리, 다른 이름

원전의 **인쇄된 식** (`[인쇄]`):

```
식 (4)   a_V = 3·ε_CAM / r_CAM        캡션: "The area of the CAM particles in CONTACT with the SE
                                       normalized to the cathode volume"   ← 접촉 분율 인자가 없다
식 (5)   R_CT = R·T / (F · j₀)
극한 (i) 얇은 전극:  R_semicircle = R_CT / (a_V · d)
```

`[해석]` 합치면:

```
      ★  측정량이 보는 것 =  R·T·r_CAM / ( 3·F · j₀ · ε_CAM · d )
         ⇒ 식별되는 조합은   j₀ · ε_CAM / r_CAM   하나  ★
```

**9호의 `A_eff · ε_p / R_s` 와 같은 자리다.** 다른 점은 **`A_eff` 가 아예 없다는 것** —
16호는 접촉 분율을 **변수로 두지 않고 1 로 못 박는다.** 그러면서 **그 양에 "접촉 면적"
이라는 이름을 붙인다.**

### ★★★ 배정의 자유 — 같은 데이터, 반대 결론

논문의 배정(`ε_CAM`·`r_CAM` 고정): **`j₀` 0.74 → 1.33 A m⁻² (1.80 배 증가)**
(97 → 389 MPa). 그런데 **같은 Table 2 가 이중층 CPE 계수도 준다**:
**`Q_DL` 0.18 → 0.54 (3.0 배)**, `β` 0.81 → 0.89.

접촉 분율 `θ` 를 넣으면 — **두 양이 같은 가정 면적 `a_V` 로 정규화되므로**:

```
R_CT^meas = R_CT^true / θ         C^meas = θ · C^true
⇒ R_CT^meas · C^meas = R_CT^true · C^true      (★ θ 가 소거된다)
⇒ C^meas 단독은 θ 에 비례                        (★ θ 를 직접 준다)
```

| 배정 | `θ(389)/θ(97)` | `j₀^true(389)/j₀^true(97)` | 원전의 **말**과 |
|---|---:|---:|---|
| **논문 (`θ ≡ 1`)** | 1.0 | **1.80 (증가)** | 수치 결론 |
| **`Q_DL` 을 면적으로 읽음** | **3.0** | `[재현]` **0.60 (감소)** | `[인쇄]` "pressure improves the **interfacial contacts** between SE particles and CAM particles **considerably**" 와 정합 |

`[재현]` 둘째 행: `j₀^true ∝ 1/(θ · R_CT^meas)` ⇒ `(1/3.0) × 1.797 = 0.60`.

★★★ `[해석]` **같은 데이터가 `j₀` 의 증가와 감소를 둘 다 허용한다.** 그리고 원전의
**문장은 둘째 배정을 말하고 숫자는 첫째 배정을 쓴다.** 이것이 이 페이지가 9호에서
**식으로** 보인 것의 **실물**이다.

★ **단서 셋 (전부 우리가 붙인다)**:
1. `β` 가 0.89 ↔ 0.81 로 달라 **두 `Q` 는 엄밀히 차원이 다르다**(F sᵝ⁻¹ m⁻²).
   `[재현]` Brug 류 유효용량(`C = Q^{1/β}·R^{(1−β)/β}`)으로 고치면 비가 **3.0 → ≈5.6** —
   **방향은 그대로이고 세진다.**
2. 이중층 **비용량**이 압력에 무관하다는 가정이 필요하다.
3. `[재현]` **`R_CT·Q` 가 두 압력에서 같지 않다**(1.67 배; 유효용량으로는 3.1 배)
   ⇒ **순수 면적 효과만으로도 설명되지 않는다.** 즉 **세 번째 배정**(면적도 변하고
   고유 동역학도 변한다)이 가장 그럴듯하고, **원전은 세 배정 중 어느 것도 고를 관측을
   갖고 있지 않다.**

### ★★ 그래서 나오는 처방 — `R_CT · C_dl` 채널

> **`R_CT·C_dl` 은 접촉 면적이 소거된 고유 시상수이고, `C_dl` 단독은 접촉 면적에 비례한다.
> 둘을 같이 보고하면 `θ` 와 `j₀` 가 갈린다.**

이것이 위 §처방표의 새 행이다. **원전은 두 값을 다 갖고 있으면서 그 조합을 만들지 않는다.**
⚠ 우리도 **아직 재지 않았다** — 여기 적는 것은 **설계**다. 그리고 CPE(β<1)가 개입하면
변환이 **모형 의존적**이어서, 이 채널을 쓰려면 **`β` 를 압력 간에 고정하거나 유효용량
변환을 명시**해야 한다. 원전 데이터는 `[인쇄]` "available **on request**" 라 재적합 불가.

### ★ 같은 논문 안에서 서사가 전극마다 바뀐다

`[도표]` 16호 **Figure 5**(음극 모식도)는 압력이 바꾸는 것을 **"interphase 를 통하는 칸의
개수"** 로 **그림으로 명시**한다 (저압 통함 3/8 ↔ 고압 5/8). 즉 **음극에서는 면적 서사**다.
그런데 같은 논문의 **양극 TLM 은 면적을 고정**하고 `j₀` 를 움직인다 — **동역학 서사**.
`[해석]` **전극이 바뀌면 같은 현상의 이름이 바뀐다.** 이것은 저자의 실수라기보다
**두 배정이 관측상 구별되지 않기 때문에 생기는 자유**다 — 이 페이지의 논지 그 자체.

### 이 절이 페이지의 `evidenceScope` 에 하는 일

`single-source` → **`multi-source-primary`**. 근거 둘:
① 9호 Huo 2025 — **P2D 모델의 인쇄된 식**(`A_eff·ε_p/R_s`, 방전곡선 적합)
② 16호 Ramanayagam 2026 — **TLM/EIS 의 인쇄된 식**(`j₀·ε_CAM/r_CAM`, 임피던스 적합)
**다른 모델족 · 다른 관측 · 다른 그룹 · 다른 나라**인데 **같은 자리에서 축퇴한다.**
⚠ `confidence` 는 **medium 유지**다 — **두 편 다 축퇴를 재지 않았고**(`identifiab*` 0/0),
우리도 아직 폭을 재지 않았다. 근거 폭이 늘었을 뿐 **측정은 여전히 0 편**이다.

## 이 페이지가 주장하지 않는 것

- **원전의 결론(양극 활물질 손실이 지배적)이 틀렸다고 주장하지 않는다.**
  주장하는 것은 **그 절차가 그것을 가려낸 절차가 아니라는 것**이다.
- **`A^p_eff = 0.4938` 이 틀렸다고 주장하지 않는다.** 단독으로 해석될 수 없다고
  주장한다.
- **축퇴를 수치로 재지 않았다.** 위 관계는 **인쇄된 식에서 손으로 읽은 구조**이고,
  근최적 집합의 **폭**은 아직 재지 않았다 ([[near-optimal-set-width-measurement]]).
- **이 관계가 다른 ASSB 모델에도 있다고 주장하지 않는다.** 근거는 **2 편**이다
  (`evidenceScope: multi-source-primary`, 2026-09-22 승격 — 9호 P2D + 16호 TLM/EIS). 다만 `a_s = 3ε/R` 과 `j = i/(a_s·A·L)` 은
  P2D 계열의 표준형이라 **같은 구조가 널리 반복될 가능성이 높다** — 확인 안 됨.
- ★ **2026-09-22 추가**: 위 §"EIS 는 대가를 받는다" 는 **10호가 이 곱 축퇴를
  확인했다는 뜻이 아니다.** 10호는 `A_eff`·`ε_p`·`R_s` 를 언급조차 하지 않는다.
  주장하는 것은 **"주파수 영역에 별개의 축퇴가 하나 더 있고, 그것이 이 페이지의
  처방 중 한 줄을 약화시킨다"** 는 것뿐이다. 두 축퇴는 **독립이다.**
