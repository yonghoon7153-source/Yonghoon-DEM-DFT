---
title: Ag–C 중간층의 리튬 경로 — 충전과 방전이 다른 길을 간다
description: "In an anode-free Ag-carbon interlayer the Li goes electrochemically into the carbon first and only then chemically into the Ag; on discharge the phase sequence is different (a LiAg polymorph appears that never exists on charge). Spencer-Jolly 2023 resolves the sequence operando and shows Ag leaves the layer on charge and returns within one cycle"
created: 2026-09-16
updated: 2026-09-16
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md, raw/papers/lee2020_ag-c-anode-free-assb.md]
confidence: low
explored: false
verificationStatus: unverified
claimType: interpretive
evidenceScope: multi-source-primary
---

# Ag–C 중간층의 리튬 경로 — 충전과 방전이 다른 길을 간다

> `assb` 축의 **여섯 번째** 개념 페이지다. 닻은 [[assb-contact-loss-vs-lampe]].
> 바로 앞 페이지 [[anode-free-li-inventory-accounting]] 가 **"무음극에서 `LLI` 를
> 무엇으로 세는가"** 였다면, 이 페이지는 **"센 Li 가 어느 그릇에 어떤 순서로
> 들어가고 나오는가"** 다.
>
> 수치의 정본은 원문 PDF 이고 여기 값은 **사본**이다 — 인용 근거로 쓰지 않는다.
> ⚠ **모집단**: Spencer-Jolly 2023 = **Ag:흑연 = 1:3 (무게), 5.7 vol% Ag, 5 µm** /
> Li₆PS₅Cl 펠릿 / **상대극 Li 금속 (반쪽전지)** / **상온 30 µA cm⁻²** (고율은 60 °C) /
> **2 MPa** / **1 사이클** / **셀 수 미상**. Lee 2020 은 **카본블랙**·완전지·1000 사이클.
> **탄소가 다르면 이 경로가 성립할 이유가 없다** — 논문 자신이 그렇게 적는다.

## 경로 — 전기화학이 먼저, 화학이 나중

`raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md`
(`assb` 7호, Bruce 그룹 / Oxford, *Joule* 7, 503–514).

```
충전:  Li⁺ + e⁻  --(전기화학)-->  LiC_x        (흑연)
                 --(화학)------>  Li_xAg → LiAg → Li₉Ag₄ → Li₁₀Ag₃
       그리고 남은 Li 는 집전체 계면에 Li 금속으로 도금
```

★ **Ag 는 전기화학적으로 리튬화되지 않는다.** `[인쇄]` "As Ag occupies only **5.7 %**
of the interlayer volume, there is very little direct contact between Ag and the
Li₆PS₅Cl electrolyte, and **direct electrochemical alloying of Ag is not expected**."
대신 **리튬화된 흑연이 Ag 를 화학적으로 리튬화**한다.

★★ **그 화학반응에 문턱이 있다.** 전기화학을 뺀 ex situ 혼합 실험(Fig. 2):
LiC₂₄·LiC₁₈·LiC₁₂ + Ag → **Li_xAg 고용체까지만**. **LiC₆ + Ag 에서만 LiAg 가 나온다.**
`[인쇄]` "**Only LiC₆ has a sufficiently high chemical potential (low voltage) to form
LiAg.**"
→ `[해석]` **중간층 안에 열역학적 사다리가 있다.** 흑연이 다 차야 Ag 가 깊이 리튬화된다.

## ★★★ 방전은 충전의 역이 아니다 — 구조적 이력

`[인쇄]` "The structural changes on discharge are **not simply the reverse** of those
on charge." 그리고 결정적으로:

> `[인쇄]` "LiAg undergoes a phase transition from the **CsCl to the UPb structure**.
> The latter is **more stable than the former when it is Li deficient**, and it is
> likely that this explains why this structural form **only appears on discharge**."

| | 충전 (`[도표]` Fig. 1 상 막대) | 방전 (`[도표]` Fig. 3 상 막대) |
|---|---|---|
| Li–흑연 | Li_xC → LiC₂₄ → LiC₁₈ → LiC₁₂ → **LiC₆** | LiC₆ → LiC₁₂ → LiC₁₈ → LiC₂₄ → Li_xC |
| Li–Ag | Ag → Li_xAg → LiAg**(CsCl)** → Li₉Ag₄ → **Li₁₀Ag₃** | Li₁₀₋ₓAg₃ → Li₉₋ₓAg₄ → LiAg(CsCl) → ★ **LiAg(UPb)** → Ag |
| Li 금속 | 충전의 ≈1/3 지점부터 끝까지 | 방전 **앞 30 %** 만 |

★★★ **충전 경로에 존재하지 않는 상이 방전 경로에 있다.** 그리고 논문은 그것을
**열역학적 안정성**으로 설명한다 — 동역학이 아니다. 율은 **C/68**(30 µA cm⁻², 상온)다.
→ **`i → 0` 으로 지울 수 있는 이력이 아니다.**

⚠ 정량은 없다 — `Rietveld` 는 참고문헌 제목에만 1 회. **상 분율·격자상수·Δ2θ 수치 0.**
상 막대는 **존재/부재만** 준다.

## ★ Ag 의 공간 이동 — 6호의 미결에 대한 답

| 질문 | Lee 2020 (`assb` 6호) | **Spencer-Jolly 2023 (7호)** |
|---|---|---|
| Ag 가 어디로 가나 | `[인쇄]` "continuously moves … **does not return**" (100 사이클 관찰) | `[도표]` Fig. 6 D→E→F: 충전에 **층 밖 → 집전체 계면의 균일막**, 방전에 **다시 층 안의 불연속 군집**. `[인쇄]` 캡션 "a **return to a near-pristine state**" |
| 단면 증거 | 없음 | `[도표]` SI Fig. S4: pristine 에 층 안 Ag 점 2–3 개 → **충전 후 Ag 신호가 층 위 "Li/Ag" 띠로 옮겨 가고 층 안에는 거의 안 남는다** |
| 정량 | 없음 | **없음** (복귀율 수치 0) |
| 사이클 축 | 100 · 1000 사이클 | ★ **없음 — 1 사이클** |

> ★★ **두 관측은 모순이 아니다.** 7호는 **한 사이클 안의 가역성**을, 6호는
> **100 사이클 누적**을 본다. 사이클당 잔류가 작아도 쌓인다.
> ⚠ **그리고 아무도 그 사이클당 잔류를 재지 않았다** — 7호는 "near-pristine" 이라는
> 형용사 한 마디다.
> `[해석]` → [[assb-apparent-capacity-decomposition]] 의 **"어느 칸이 시간에 따라
> 움직이나" 는 여전히 미정**이다. 7호가 준 것은 **칸 사이의 화살표(경로)이지 그
> 시간 도함수가 아니다.**

## 율이 경로를 바꾼다 — `η(i)` 가 상 조성을 건드린다

`[인쇄]` 2 · 4 mA cm⁻²(60 °C, 싱크로트론): "**No change is evident in the Ag peaks**,
indicating that the rapid insertion of Li into graphite … is significantly **faster
than the reaction of lithiated graphite with the Ag** nanoparticles."
4 mA cm⁻² 에서는 `[인쇄]` "**clear evidence of Ag persisting throughout charging**".

`[재현]` 과전압: **2 mA cm⁻² 에서 ≈−0.09 V 가 3 h 내내 평평** ↔ **4 mA cm⁻² 에서
−0.16 → −1.15 V 로 계속 자라다 ≈0.72 h(≈2.9 mAh cm⁻²)에 단락**.
→ **전류 2 배에 과전압 ≈12 배.**

`[해석]` **음극 쪽에서 `Q_material` 자체가 율 의존이다** — 고율에서는 Ag 가 Li 를
못 받으므로 같은 전하가 **다른 상 분포**를 만든다. 3호(Liu 2024)가 양극에서 보인
"`Q_material` 도 율 의존" 의 **음극 판**이다 → [[assb-apparent-capacity-decomposition]].

## 우리 축에 걸리는 곳

1. ★★★ **[[halfcell-ocp-shape-invariance]] 에 구조적 반례다.** 반쪽전지 OCP
   템플릿 하나로 충·방전을 같이 적합하는 설계는 **이 음극에서 원리적으로 못 쓴다**
   — 충전에 없는 상이 방전에 있고, 그것이 **열역학적**이다.
   ⚠ 모집단은 **ASSB 음극 중간층**이다. 액체셀 흑연으로 옮기지 않는다.
2. ★★ **용량축이 "늘어나는" 기구가 상으로 설명된다.** `[인쇄]` "The load curve
   resembles that of graphite **but with the capacity stretched** … due to reaction of
   the LiC_x with Ag." → 겉보기 용량이 재료량과 1:1 이 아닌 이유가 **음극 쪽 화학
   반응**이다. `Q_apparent` 3 항 분해가 상대해야 할 것이 음극에도 있다.
3. ★ **흑연이 완충기다.** `[인쇄]` 방전 초반에 "as Li is electrochemically extracted
   from LiC₆, it reacts sufficiently rapidly with the Li and Li₁₀Ag₃ at the current
   collector **to retain LiC₆**" → **겉보기 음극 조성이 통과 전하와 1:1 대응하지
   않는다.** 전하 축에서 상 축으로의 사상이 단사가 아니다.
4. ★ **전하 수지의 나머지가 크다** — `[재현]` 첫 사이클 비가역분 **≈0.79 mAh cm⁻²
   (통과 전하의 39 %)**. 상세와 가정은 [[anode-free-li-inventory-accounting]].

## 이 페이지가 주장하지 않는 것

- **Lee 2020 이 틀렸다고 주장하지 않는다.** 탄소가 다르고(흑연 ↔ 카본블랙), 셀이
  다르고(반쪽 ↔ 완전), 사이클 수가 **1 ↔ 1000** 이다.
- **이 상 순서를 카본블랙 계로 옮기지 않는다.** 카본블랙은 층간삽입 상(LiC₁₂/LiC₆)을
  만들지 않으므로 **"LiC₆ 여야 LiAg 가 된다" 는 문턱이 그대로 성립할 이유가 없다.**
  논문 자신이 `[인쇄]` "the **type of carbon chosen will have a significant impact**"
  라고 적는다.
- **Ag 가 쓸모없다고 주장하지 않는다.** 논문이 말하는 것은 **임계전류를 못 올린다**
  (`[인쇄]` 흑연 단독과 **같은 failure point**, 둘 다 2.5 mA cm⁻² 에서 단락)는 것이고,
  **균질성은 올린다**고 같은 논문이 적는다.
- **상 분율을 주장하지 않는다.** 정량 상분석이 없다 (Rietveld 0).

## 관련
- [[assb-contact-loss-vs-lampe]] — 닻 질문. 이 페이지는 그 **음극 축**에 붙는다
  (양극 `LAM_PE` ↔ 접촉 손실에는 입력을 주지 않는다).
- [[anode-free-li-inventory-accounting]] — 같은 셀 계열의 `LLI` 계정. 이 페이지가
  **그릇(상)** 을, 저 페이지가 **총량(전하 수지)** 을 맡는다.
- [[assb-apparent-capacity-decomposition]] — `Q_apparent = θ · η(i,P) · Q_material`.
  이 페이지가 **음극 쪽 `Q_material` 도 율 의존**임을 더한다.
- [[halfcell-ocp-shape-invariance]] — 이 페이지의 상 이력이 그 가정의 반례다.
- [[assb-stack-pressure-operating-window]] — 같은 논문의 압력 축(제작 400 MPa 일축 ·
  운전 2 MPa 원뿔 스프링, 스윕 0).
