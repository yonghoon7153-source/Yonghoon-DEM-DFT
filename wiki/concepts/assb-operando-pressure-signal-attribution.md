---
title: 운전 중 압력 · 두께 신호의 귀속 — 음극 지배, 강성 곱, 기저선 규약
description: "What an in-operando stack-pressure (or dilatometric height) signal measures in an ASSB: a stiffness-weighted sum of electrode swelling plus a drifting baseline. The prototype (Zhang W. et al. 2017, JMCA 5, 9929) shows the In-anode share is about 90–95 %, the amplitude-to-capacity ratio rises over cycling, and the printed ΔP is baseline-corrected while the ~62 MPa operating pressure appears only on an ESI axis"
created: 2026-09-28
updated: 2026-09-28
type: concept
tags: [assb, battery, degradation, research]
sources: [raw/papers/ishidzu2016_ncm-ni-fraction-lattice-volume-change-cycle-fade.md, raw/papers/kondrakov2017_ncm111-ncm811-lattice-strain-particle-shrinkage-cracking.md, raw/papers/kondrakov2017_ncm811-charge-transfer-lattice-collapse-xrd-xas-dft.md, raw/papers/debiasi2017_ncm-ni-content-operando-xrd-lattice-volume-energy-density.md, raw/papers/zhang2017_interfacial-eis-cathode-composition-lco-lgps-assb.md, raw/papers/zhang2017_in-situ-pressure-electrochemical-expansion-assb.md, raw/papers/zhang2025_pressure-free-si-li21si5-double-layer-anode-assb.md, raw/papers/zhang2025_low-pressure-assb-challenges-strategies-review.md, raw/papers/li2025_stack-pressure-critical-importance-perspective.md, raw/papers/huo2025_assb-cathode-lampe-coupled-aging-model.md]
confidence: low
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: multi-source-mixed
---

# 운전 중 압력 · 두께 신호의 귀속 — 음극 지배, 강성 곱, 기저선 규약

> `assb` 축의 개념 페이지. 닻은 [[assb-contact-loss-vs-lampe]] — 그 카드의 Q2("독립 관측") 칸에 압력 센서가 되풀이해 올라온다(9 · 60 · 62호).
> 압력의 **작동 창**은 [[assb-stack-pressure-operating-window]], 압력을 **조작**으로 쓰는 연산자는 [[assb-pressure-reapplication-separation-test]], 압력을 **소신호 도함수**로 쓰는 편은
> [[assb-maxwell-ocv-derivative-channels]]. 이 페이지는 압력을 **관측 신호**로 쓸 때 그 신호가 무엇의 합인지를 다룬다.
> 원형은 `assb` **62호**(Zhang W. … Zeier · Janek 2017 *J. Mater. Chem. A* 5, 9929 — 이 계보에서 가장 이른 운전 중 압력 실측, `raw/papers/zhang2017_in-situ-pressure-electrochemical-expansion-assb.md`).
> 비교 표본은 60호 S14 · 33호에 재수록된 원자료 다섯 · 9호 힘 시계열 · 59호(Perspective). 식은 전부 우리 정리(`[해석]`)이고 수치는 각 digest 의 표기(`[인쇄]` · `[도표]` · `[재현]`)를 따른다.

## 정의 — 신호를 한 식으로 (`[해석]`)

정변위에 가까운 구속(지그 · 유압 · 볼트)에서의 압력과 무가압 딜라토미터의 높이를 같은 틀로 적는다.

```
P(t) = P_base(t) + k_eff(N) · Σ_e Δh_e(q)        # 압력 신호
h(t) = h_base(t) +            Σ_e Δh_e(q)        # 높이 신호(딜라토미터)
Δh_e ∝ (전극 e 에서 실제로 Δx 를 겪은 활성 부피) · (Δx 당 몰부피 변화)
```

| 항 | 무엇 | 62호(원형)에서 | 원전이 인쇄했나 |
|---|---|---|---|
| `P_base(t)` 기저 · 표류 | 운전 스택 압력 + 시간 표류(압밀 · 소성 흐름 · 장치 이완 · 온도) | `[도표]` S7 원시 **61.83 → 60.63 MPa / 110 h** — 시간당 ≈0.02 → 0.009 MPa h⁻¹, 율을 올린 구간에도 시간에 따라 준다 | **본문 0** — ESI 그림 축에만 |
| `k_eff(N)` 강성 | 셀 밖(지그 · 유압 기둥 · 게이지)과 셀 안(공극 압밀 · 소성 흐름) 순응의 역수 | `[재현]` 관측 ΔP 를 셀 탄성만으로 내려면 유효 길이 ≈22–36 mm(인쇄 SE 탄성률 18–25 GPa · ESI ⅓ 규칙 두께 ≈1.5 µm) ↔ 셀 적층 ≲1.3 mm ⇒ 변위의 대부분은 셀 탄성 밖 | **0** |
| `Σ Δh_e` 전극 합 | 양극 + 음극 팽창(부호 포함) | 충전에 **둘 다 팽창**(LCO c 축 · In → InLi) · 음극 몫 `[재현]` ≈90–95 %(LTO 교체) | 전극 몫은 음극 교체로만 |

⚠ **2026-09-28 (66호) 주석 — 둘째 인자 "Δx 당 몰부피 변화" 는 상수가 아니다.** 66호(de Biasi 2017 *JPCC* — 액체 반쪽 · NCM 여섯 조성 operando 격자, 표 S1)에서 `[재현]` NCM811 dV/dδ 가 3.99–4.05 V ≈−4 → 4.24–4.32 V ≈−30 Å³ per δ(×7)로
올라 4.5 V 까지 ≈−28 로 유지되고, NCM622 는 δ 0.93–0.45 에서 −2…−4 · δ 0.30–0.18 에서 −19…−21 Å³ per δ 다. NCM 은 **충전 수축**(`[인쇄]` "a large decrease in unit cell volume upon charging") — In · Si 음극의 충전 팽창과 부호가 반대라
양극 몫은 합에서 음극 몫을 깎는다. ⇒ 같은 용량 진폭이라도 **SOC 창(컷오프)에 따라 양극 몫이 다르고**, 같은 용량에서 θ 가 작으면 활성 입자의 Δx 가 커져 몫이 비선형으로 바뀐다([[nmc-lattice-li-content-calibration]] 함정 6).
⚠ **2026-09-28 (67호) 주석** — 67호(Kondrakov 2017 *JPCC* — NCM811 · 전처리 셀 operando)에서도 같은 모양이다: `[재현]` `V` 변화의 **76.8 %** 가 x ≤0.5(≈4.06–4.6 V, 67호 축)에서 일어나고, 4.2 V 까지 −2.5…−2.8 % · 4.3 V −4.9…−5.4 % · 4.6 V + 1 h −7.02 %(기준 = 전처리 셀 충전 첫 점). 다만 67호의 x 축 규약이 66호와 0.10 다르므로(`x₀` 1.00 ↔ 0.90) 두 편의 `dV/dx` 를 겹칠 때는 x 가 아니라 전압으로 맞춘다([[nmc-lattice-li-content-calibration]] 67호 절).
⚠ **2026-09-28 (69호) 주석 — 양극 몫의 크기는 층위에 따라 ×1.5 다르다.** 69호(Kondrakov 2017 *JPCC* 121, 3286 — 액체 반쪽 · 신품 셀)에서 NCM811 4.3 V + 1 h 격자 `ΔV/V` −5.0…−5.1 %(원형 기준 ·
첫 충전 · XRD) ↔ **2차 입자 −(7.8 ± 1.5) %**(광학 + DIC · 둘째 사이클 · 선형 배경 뺌) · NCM111 −1.16 ↔ −(3.3 ± 2.4) %. 격자 부피 변화의 ≈69 % 가 4.04 V 위(방전 용량 ≈25 %)이고, 광학 입자 부피는
정전압 중에 −8.2 → ≈−6 % 로 먼저 회복한다(격자는 최저 유지). ⇒ 두께 · 압력 신호의 양극 몫을 격자 `dV/dx` 로 추정하면 입자 · 전극 층위의 수축을 과소평가할 수 있다(`[해석]` — 광학 방법이 그
차이를 가르지 못한다: 2D 투영 · 입자 수 · 식 부호 미인쇄). 첫 충전 앞머리 Δx ≈0.12–0.18 은 격자를 움직이지 않는다 — 신품 셀 첫 충전의 양극 몫은 그 구간에서 ≈0 이다.
62호 원형은 LCO(충전 팽창)라 이 비선형의 표본이 아니다.
⚠ **2026-09-28 (72호) 주석 — 양극 몫은 조성 · 상한 전압에 더해 연구실 · 사이클로도 흔들린다.** 72호(Ishidzu 2016 *SSI* 288, 176 — 액체 반쪽 · 여섯 조성 · 첫 충전으로 읽힘 · 2.5–4.5 V · 0.05 C)에서 4.5 V 격자 `ΔV/V` 가 Ni 1/3 → 0.7 에 2.24 → 5.76 %(×2.6 · `[도표]` 벡터 좌표)이고, NCM111 부피 변화의 ≈47 % 가 `c` 최대(x ≈0.59) 뒤 Δx 21 % 에 몰린다(`[재현]` dV/dx ≈2.0 → 9.6 Å³ per x). 같은 조성 · 같은 4.5 V 에서 66호 표 S1 보다 +0.4…+1.0 %p(×1.1–1.5) — 격자 층위 안의 이 폭이 69호 층위 몫(입자/격자 ×1.5)과 같은 크기다. ⇒ 두께 · 압력 신호의 양극 몫을 한 교정 곡선의 `dV/dx` 로 추정할 때 조성 · 상한 전압 · 교정 셀(사이클 번호 · 율 · 로트)을 값 옆에 적는다(`[해석]`).

## 왜 중요한가 — 카드 Q2 · Q1 에서 이 신호를 쓸 때의 함정 다섯

1. ★★★ **음극 지배.** Li-In · 합금 · Si 음극 셀의 압력 신호는 대부분 음극이다. 62호: In ÷ LTO 진폭 **×18.9** · 용량당 **×14.7** · 둘째 충전 기울기 **≈×17**(`[재현]`) · 논문 자신의 두께 계산
   In 1.56 : LCO 0.163 µm. 33호 재수록: 상대극(흑연 ± LGPS · μ-Si · Sb) **≈0.5–2.3 MPa** ↔ 양극 [58] **≈0.05–0.07 MPa**. ⇒ 카드 물음(양극 `LAM_PE` ↔ 접촉 손실)에 압력은 **거의 상대극
   채널**이다. 양극 몫을 보려면 무변형 상대극(LTO)으로 바꿔야 하고, 그 신호는 62호에서 ≈0.067 MPa · 잡음 ≈±0.005(S/N ≈15).
2. ★★★ **강성 곱 — 편 간 ΔP 는 같은 눈금이 아니다.** ΔP = `k_eff` · Δh 이고 `k_eff` 는 지그마다 · 사이클마다 다르다. 62호 면적 용량당 ΔP ≈1.0(보정) · ≈0.86(원시) ↔ 60호 S14 ≈0.52 MPa per
   mAh cm⁻²(`[재현]`) — 기저(×77) · 음극 · 지그 · 온도가 다 다르다. 62호 한 셀 안에서도 진폭/용량 비가 11 사이클에 **+14 %(보정) · +29 %(원시)** 오른다 — 압밀로 셀이 굳었다는 저자 서사와 양립한다.
3. ★★★ **입자 고립과 `LAM_PE` 는 같은 서명.** 전자/이온으로 고립된 입자와 구조 열화된 입자는 **둘 다 Δx 를 멈춘다** ⇒ 양극 몫 `Δh_ca` 는 `θ·ε_p` 곱을 **용량과 같은 방식**으로 본다. 압력이 용량과
   다르게 보는 것은 (i) Δx 없는 전하(부반응 · 누설 — 용량에 들어가고 압력에 안 들어간다) (ii) `k_eff` 변화뿐이다 ⇒ **압력 채널은 관측 하나와 미지수(`k_eff`) 하나를 같이 더한다** — `k_eff` 를 따로
   재기 전(예: 사이클 사이 작은 하중 계단 — 제안)에는 곱 축퇴에 대한 순 식별 이득이 0 이다([[assb-lampe-contact-product-degeneracy]] 처방 표 경고 행).
4. ★★ **기저선 규약이 정보를 지운다.** 62호는 방전 말 골을 잇는 선을 빼 "방전 말 ΔP = 0" 을 만들었다 — 원시 표류(−1.2 MPa / 110 h)가 한 사이클 진폭과 같은 크기다. 59호는 Li 금속 셀에서 기저
   **상승**을 `[인쇄]` "residual solid electrolyte interphase and isolated lithium" 의 누적으로 적었다(분리 불가 인쇄). In 셀에서 방전 말 음극에 남은 Li(재고 손실의 한 몫)는 잔류 팽창이라 기저를 **올려야**
   하는데 압밀 · 이완은 **내린다** — 둘이 같은 자리에서 상쇄되고, 기저선 제거는 둘을 한꺼번에 지운다.
5. ★ **기저(절대) 압력이 본문에 없는 관행.** 62호(≈61.8 MPa, ESI S7 축) · 33호 재수록 [88](≈45 MPa, 그림에만) · [90](≈20 MPa, 그림에만) — 세 편 모두 ΔP 는 인쇄, 기저는 그림 축이다.
   60호는 예압(0.8 MPa)을 인쇄하고 그림은 0 에서 시작한다.

## 표본 표 — 이 위키에 들어온 운전 중 압력 신호

| 편 | 셀 · 상대극 | 구속 · 기저 | 충전 ΔP · 추이 | 기저선 처리 | 원전이 인쇄한 것 |
|---|---|---|---|---|---|
| **62호** Zhang W. 2017(원형) | In ‖ LGPS ‖ LCO(LNTO) · 대조 LTO ‖ LGPS ‖ LCO | hot-press 유압 + 바닥 게이지 · `[도표]` 기저 ≈61.8 MPa / LTO 는 air-tight casing · 25 °C 캐비닛 | +1.25(보정, 인쇄) · +1.07(원시) → 보정 1.152 · 원시 +1.10(11 사이클) / LTO ≈0.067 평탄 | 방전 말 골을 잇는 선 — 제거 | "1.25 MPa" · "20 times smaller" · "60%" · 요구치 0 |
| **60호** Zhang Z. 2025 S14 | Li₂₁Si₅/Si–Li₂₁Si₅ ‖ Li₆PS₅Cl ‖ Li₃InCl₆ ‖ LCO | 정변위 · 예압 0.8 MPa · 45 °C · 공기 < 10 % RH · 사양 0 | +1.51 → ≈1.2 · 1.15 · 1.1 · 1.05(`[도표]`) · 방전 말 복귀 | 그림은 예압 위 증가분 | "+1.51 MPa" · "0.8 MPa" |
| 33호 재수록 [59] | 흑연 ± LGPS | 정변위 | ≈0.7–0.8 | — | (재수록 그림) |
| 33호 재수록 [88] Ji 2022 | μ-LiₓSi ‖ SSE ‖ LTO | 정변위 · 기저 ≈45 MPa(그림에만) | ≈1.0 → 0.5(5 사이클) | — | "≈0.7 MPa" |
| 33호 재수록 [90] Han 2021 | Sb:LPSC | 기저 ≈20 MPa(그림에만) | 첫 충전 ≈+2.3 → 20.5–21.8 진동 | — | "2.25 MPa" |
| 33호 재수록 [58] Koerver 2018 | LCO/NCM 양극 | — | ≈0.05–0.07 | — | — |
| 33호 재수록 [19] | (스프링 = 정압 지그) | 5 MPa | 5 → 5.21(+4 %) | — | — |
| 9호 Huo 2025 | NCM811 ‖ 황화물 ‖ Li-Si | 예압 · 수압 면적 0 | 12 사이클 힘 시계열 — **단위 Kg** · MPa 환산 · 교정 0 | — | — |

⚠ 33호 재수록 값은 33호 digest 의 그림 판독이고 원전 미열람이다. 62호 LTO 자료 제공자(R. K.)와 [58] Koerver 2018 이 같은 측정 계열인지는 **미확인**이다.

⚠ **2026-09-28 (63호) 정정 둘.** (i) 62호 LTO 셀의 "air-tight cell casing designed by our group27" 은 63호 SI Fig. S3 케이스다 — **나사 10 N·m 토크 · Al 프레임 · 하중계 없음**. 62호 Fig. 4 의 In ↔ LTO 비교는 hot-press 셀 ↔ 나사 케이스 셀의 비교였을 수 있고(62호가 LTO 셀 압력을 어떻게 쟀는지는 여전히 0), 함정 1 의 음극 몫 ≈90–95 %(`[재현]`, 같은 `k_eff` 가정)는 **조건부**다. (ii) 62호 ESI S3("stable electrochemical performance")의 셀은 63호 Fig. 9 셀 C 이고 63호 방법상 **Li 박 1:60 장기 셀**이다 — 62호 압력 셀과 다른 셀 · 다른 Li 재고.

## 이 위키에서의 적용

- **카드 [[assb-contact-loss-vs-lampe]] Q2** — 압력 센서를 "독립 관측" 으로 셀 때, (i) 상대극이 평탄 · 무변형인가 (ii) 원시 신호(기저 포함)가 있는가 (iii) `k_eff` 또는 지그 형식이 적혔는가를 같이 적는다.
  셋 다 없으면 압력은 용량의 사본에 가깝다(함정 3).
- **Q1(`θ(N)`)** — 압력 진폭 시계열은 접촉 손실 시계열의 후보가 아니다(62호: 진폭/용량 비가 오르고, 원인 배정은 무가압 셀의 추론).
- **[[assb-pressure-reapplication-separation-test]] D1** — "사이클 해상 압력 계측" 에 붙일 후보(결정은 사용자 몫): 원시 압력(기저 제거 전) · 기저선 규약 · 무전류 유지로 잰 표류를 같이 신고한다.
- **[[assb-stack-pressure-operating-window]] §압력 진동** — 상대극 ΔP ≈ 요구치 크기라는 관찰의 원형 표본이 62호다(In 셀 ≈1.0–1.3 MPa · 양극 몫 ≈0.07). 단 기저 ≈62 MPa 위의 값이다.
- **합성 truth([[assb-synthetic-truth-contact-loss-requirements]])** — 운전 압력을 넣을 때 기저(절대) · 구속 형식 · 기저선 규약 셋을 같이 적는다(60호 · 61호 새 제약에 62호가 둘을 더한다).

## 이 페이지가 주장하지 않는 것

- **압력 채널이 접촉 손실을 원리적으로 못 본다고 하지 않는다** — `ΔP_ca` 로는 입자 고립과 `LAM_PE` 가 같은 서명이라는 것(우리 대수)까지다. 입자가 Δx 를 멈추지 않고 접촉만 잃는 기구(예: 부분 피복으로 속도만
  느려짐)라면 저율에서 압력 · 용량이 같이 회복될 수 있다 — 검사하지 않았다.
- **"지그 순응이 ΔP 를 정한다" 를 측정으로 주장하지 않는다** — 62호 인쇄 탄성률 · ESI ⅓ 규칙 · 셀 두께 상한 위의 `[재현]` 이다. 강성 실측은 어느 편에도 없다.
- **62호의 기저 표류가 압밀이 아니라고 하지 않는다** — 후보를 가를 대조가 없다는 것까지다.
- **33호 재수록 값 · 9호 힘 시계열을 MPa 눈금에서 62호와 나란히 비교하지 않는다** — 재수록 판독 · 단위 Kg · 기저 미인쇄가 섞여 있다. 표는 **무엇이 인쇄됐는가**의 대조다.
- **`evidenceScope: multi-source-mixed` · `confidence: low`** — 1차 측정은 62호 · 60호 둘이고 나머지는 재수록 · Perspective 다.

## 관련
- [[assb-contact-loss-vs-lampe]] — 닻. Q2 칸의 압력 센서 항목이 이 페이지의 함정 다섯에 걸린다.
- [[assb-stack-pressure-operating-window]] — 압력의 작동 창 · §압력 진동(33호) · 62호 절.
- [[assb-pressure-reapplication-separation-test]] — 압력을 조작으로 쓰는 연산자 · 설계 조건 D1–D5.
- [[assb-lampe-contact-product-degeneracy]] — 곱 축퇴 처방 · 마흔다섯 번째 적용의 경고 행("압력 · 두께 진폭을 활성 분율 대리로 쓸 때").
- [[assb-maxwell-ocv-derivative-channels]] — 압력을 관측 변수로 쓰는 다른 형식(14호 `E(P)`).
- [[li-metal-yield-creep-vs-stack-pressure]] — Li 금속 음극이면 기저 압력이 어느 creep 영역인지(62호 기저 ≈61.8 MPa = σ/G ≈2.2×10⁻², breakdown 영역).
- [[nmc-lattice-li-content-calibration]] — 양극 몫 `Δh_ca` 의 둘째 인자 `dV/dx`(66호 NCM 여섯 조성 원자료 · Δx 에 비선형).
