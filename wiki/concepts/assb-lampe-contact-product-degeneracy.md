---
title: "복합양극 동역학 항의 곱 축퇴 — LAM_PE 와 접촉 손실이 A_eff·ε_p/R_s 한 조합으로만 들어간다"
description: "In a published composite-cathode ASSB P2D model the Butler-Volmer denominator sees only the product A_eff x eps_p / R_s, so active-material loss, contact-area loss and particle radius are not separately identifiable from a discharge curve"
created: 2026-09-22
updated: 2026-09-22
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md, raw/papers/vadhva2021_eis-for-assb-theory-methods.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: theoretical
evidenceScope: single-source
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

★ **마지막 줄이 우리가 바로 할 수 있는 것이다.** 필요한 입력은 두 가지뿐:
반쪽전지 OCP 두 곡선(원전이 출처를 안 적었다)과 비공개 6 개 파라미터.

## 이 페이지가 주장하지 않는 것

- **원전의 결론(양극 활물질 손실이 지배적)이 틀렸다고 주장하지 않는다.**
  주장하는 것은 **그 절차가 그것을 가려낸 절차가 아니라는 것**이다.
- **`A^p_eff = 0.4938` 이 틀렸다고 주장하지 않는다.** 단독으로 해석될 수 없다고
  주장한다.
- **축퇴를 수치로 재지 않았다.** 위 관계는 **인쇄된 식에서 손으로 읽은 구조**이고,
  근최적 집합의 **폭**은 아직 재지 않았다 ([[near-optimal-set-width-measurement]]).
- **이 관계가 다른 ASSB 모델에도 있다고 주장하지 않는다.** 근거는 **1 편**이다
  (`evidenceScope: single-source`). 다만 `a_s = 3ε/R` 과 `j = i/(a_s·A·L)` 은
  P2D 계열의 표준형이라 **같은 구조가 널리 반복될 가능성이 높다** — 확인 안 됨.
