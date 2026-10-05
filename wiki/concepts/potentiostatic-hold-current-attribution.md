---
title: 정전위 유지(float · voltage hold) 전류의 귀속 — 가역 이완 · 부반응 · 단락이 한 숫자에 섞인다
description: "A potentiostatic (float / voltage-hold) current is one number carrying at least three things — reversible relaxation, side-reaction (SEI repair) current and, if present, a short — and their mix depends on electrode, potential, time window and cell configuration. Records what each hold-based ageing or fault study in this wiki actually measured, the measured size of the mix, and the sign a short takes in each configuration"
created: 2026-10-02
updated: 2026-10-05
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/zhang2026_si-anode-interphase-calendar-ageing.md, raw/papers/truong2025_calendar-vs-cycle-aging-protocols-drt-assb.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: interpretive
evidenceScope: multi-source-primary
---

# 정전위 유지(float · voltage hold) 전류의 귀속

## 정의

셀(또는 반쪽전지)을 한 전위에 붙들어 두는 동안 흐르는 전류 `I_hold(t)`. 이 숫자 하나에 적어도 셋이 들어간다.

```
I_hold(t) = I_rev(t) + I_side(t) + I_short (+ 잡음 · 표류)
```

1. **가역 이완 `I_rev`** — 앞 CC 단계가 남긴 농도 · 상 경사가 풀리며 더 들어가는(빠지는) 전하. 다음 반대 방향 단계에서 **돌아온다**.
2. **부반응 `I_side`** — 음극 저전위의 SEI 형성 · 보수, 양극 고전위의 전해질 산화 · 계면 분해. **돌아오지 않는다**(재고 손실 · 계면층).
3. **단락 · 누설 `I_short`** — 전위차 ÷ R_s. **부호가 셀 구성에 따라 다르다**(아래 절).

이 위키의 표본 중 이 분해를 **측정으로** 한 편은 없다. 이름("leakage = SEI growth rate" · "float current = 단락")을 붙이는 순간 귀속이 결정된다 — [[fitting-degeneracy]] 의 "다른 원인이 같은 관측을 만든다" 와 같은 모양이다.

## 이 위키의 표본 — 무엇을 쟀고 무엇을 지표로 썼나

| 표본 | 셀 · 전극 · 전위 · 시간 | 유지 전류를 어떻게 썼나 | 섞임의 처리 |
|---|---|---|---|
| **Zhang 2026** *Nat. Energy* (액체 Si — `raw/papers/zhang2026_si-anode-interphase-calendar-ageing.md`) | Li ‖ Si 반쪽전지(2전극) · **음극 0.06 V vs Li** · 180 h · 온도 미인쇄 | **주 지표** — "leakage current @180 h"(창 평균으로 읽힘) = `[인쇄]` "SEI repair/growth rate" · 적분 QL | 가역분: 역분극 시험으로 "~40-60 hours" 뒤 0 이라 보고 180 h 값을 씀 · 단락 논의 0 |
| **Truong 2025** *J. Mater. Chem. A* (`assb` 90호 — `raw/papers/truong2025_calendar-vs-cycle-aging-protocols-drt-assb.md`) | In/InLi \| Li₆PS₅Cl \| NCM83 반쪽전지 · **양극 3.7–4.1 V vs In/InLi** · 48 h · 25 °C | 그렸으나(ESI S11) **지표 아님** — 지표는 RPT 손실 · 시간분해 DRT | 유지 중 통과 전하만(90호 digest 판독 ≈28.5–29.5 mAh g⁻¹ · 컷오프와 거의 무관) · 가역 · 비가역 분해 0 |
| **MSC 응용 문서** (`bms-balancing/docs/MSC_SEMINAR_2026-09-23_APPLICATION.md` §0 · §3 P3 · P7) | 풀셀 CV(float) — 합성 모델 · 가설 | 단락 검출 **후보 신호** | P3: 옴 단락 = V 선형 · 시간 불변 ↔ 부반응 = 지수 · 감쇠 · P7: τ 와 I_∞ 를 나누고 같은 셀의 이전 CV 와 차분 — 그 문서의 합성 수치는 여기 옮기지 않는다 |

## 섞임의 크기 — 실측으로 아는 것 (Zhang 2026 원자료 `[재현]`)

- **가역분이 크다.** 180 h 누적 QL = **9.8–20.1 % of QD**(µ-Si) · 5.3 %(흑연) 중 **59–82 %** 가 다음 탈리튬에서 돌아온다(QL − SEI growth × (1 + QL/QD) — 지표는 여러 셀 평균 · QL 은 시계열 셀 하나 · 크기 검사). 유지 전류의 처음 수십 h 는 부반응보다 이완을 본다.
- **늦은 꼬리는 느리고 바닥이 있다.** 2 h 평균의 `I ∝ t⁻ⁿ`: n = 0.24–0.73(20–180 h) · 0.14–0.62(60–180 h) · 흑연은 60 h 뒤 ≈0.09–0.10 mA/Ah 에서 사실상 평탄 — "부반응 = 감쇠" 가 180 h 창에서는 "거의 일정" 으로 보인다. 저자의 해석 틀(SEI 균열 · 용해 → 보수의 순환)도 바닥을 예측한다.
- **크기가 화학 · 형상으로 흔들린다.** µ-Si 0.088–0.250 mA/Ah(= 8.8×10⁻⁵ – 2.5×10⁻⁴ C · SEI 화학 ×2.8) · 표면적(n-Si) 늦은 기울기 ×1.65–2.5 · 전해액 150 → 500 µl ×1.27(셀 하나씩).
- **잡음이 신호와 같은 자릿수.** 170–181 h 표준편차 = 평균의 0.4–0.7 · ≤0 점 셀당 0.5–23 % · 단일 점 값은 0.045–0.418 mA/Ah 로 흔들린다 → "@t 전류" 는 **창 평균으로만** 의미가 있고 창 정의를 값 옆에 적어야 한다. 로그 축 그림은 ≤0 점을 지우고 잡음의 양(+)쪽만 남긴다.
- **정규화가 비교를 바꾼다.** 유지 직전 용량(QD)으로 나눈 A Ah⁻¹ 는 이미 용량을 잃은 전극의 누설을 질량 기준보다 부풀린다(4M DME ↔ THF: QD 기준 ×2.8 ↔ 질량 기준 ≈×1.8 `[재현·가정]`).

## 단락이 섞일 때의 부호 `[해석]`

- **풀셀 float(예: 4.1 V CV)**: 내부 단락은 셀을 방전시키고 정전위기는 같은 방향(충전)으로 보상한다 → `I_short` 가 `I_side` 와 **같은 부호로 더해진다**. 한 숫자에서 두 원인이 안 갈리는 자리(MSC 문서 §0 F1).
- **Li ‖ 음극 반쪽전지 저전위 유지(예: 0.06 V vs Li)**: 내부 연결은 Li → 음극으로 리튬화 전류(≈0.06 V ÷ R_s)를 만들고 정전위기는 **산화(반대 부호)** 로 보상한다 → 측정 누설을 **줄이거나 음수로** 만든다. 그래서 반쪽전지 유지 전류는 풀셀 단락 검출의 기준선이 될 수 없다.
- **양극 상한 반쪽전지 유지(90호 형식)**: 셀 전압이 수 V 라 단락 전류가 크고 같은 부호(충전 보상)로 더해진다. 90호는 단락을 다루지 않는다.
- **`[모델]` 풀셀 정전위 계단 · 흑연 평탄부 SOC (2026-10-05 · SPMe 합성)**: SOC 0.5 의 ±10 mV 정전위 짝에서 음극 SEI 로 잃은 리튬은 1.4 % 만 전류로 보였고 옴 누설은 제 크기로 보였다 — 정전위기는 셀 전압이 움직일 때만 전류를 내는데, 음극만의 리튬 손실은 흑연 평탄부가 가린다. 그래서 위 첫 줄의 "같은 부호로 더해진다" 는 양극 쪽 · 고전압 부반응에는 맞고 평탄부의 음극 SEI 에는 약하다. 모델 명제 (양극 쪽 부반응 없음 · 실셀 0) — `bms-balancing/docs/MSC_PROTOCOL_DESIGNS_REVIEW_2026-10-05.md` §3-1 · §6 ①.

## 이 개념을 쓸 때의 규칙 (제안)

1. 유지 전류 값 옆에 **전극 · 전위 · 기준극 · 셀 구성(반쪽 · 풀 · 3전극) · 시간 창(평균 구간) · 정규화 · 온도**를 적는다.
2. **가역분을 먼저 뺀다** — 역분극 시험이나 유지 뒤 반대 방향 단계의 회수 전하로. 회수량 없이 "누설 = 부반응" 이라 쓰지 않는다.
3. **같은 셀의 이전 유지 곡선과 차분한다**(MSC 문서 P7 규칙) — 정상 꼬리의 모양 변화와 상수 이동을 가른다.
4. 정전위 유지를 **달력 노화 대리**로 쓸 때는 가속 배율(유지 1 h ↔ 개회로 보관 몇 h)과 그 근거를 적는다 — 이 위키의 두 표본 모두 0(정전위 유지 → 감쇠 예측의 비판적 원전 Schulze 2022 *JES* 169, 050531 은 두 편이 함께 인용하나 위키에 없다 — 후속 ★★★).

## 관련

- [[isc-detection-vs-balancing-masking]] — 정상 자기방전(H2 의 null 방향 경쟁 원인)의 크기 근거가 여기서 간다
- [[thermo-kinetic-loss-partition]] — 같은 편의 "active capacity loss" 가 저율 한 전류에서 η 를 LAM 칸에 섞는 문제
- [[fitting-degeneracy]] — "다른 원인이 같은 관측" 의 같은 모양
- [[drt-peak-count-nonidentifiability]] — 90호가 유지 노화를 읽은 DRT 봉우리 이름의 문제
- [[anode-free-li-inventory-accounting]] — 쿨롱 장부로 LLI 를 세는 반대 끝(재고 0 ↔ 반쪽전지의 재고 무한)
- `bms-balancing/docs/MSC_SEMINAR_2026-09-23_APPLICATION.md` §0 · §3 P3 · P7 (repo-root 상대 경로 · 내용 복사 금지)
- `bms-balancing/docs/MSC_PROTOCOL_DESIGNS_REVIEW_2026-10-05.md` — MSC 복합 진단 설계안 10종 검토 + SPMe 사전 부호표 (repo-root 상대 경로)

## 이 페이지가 주장하지 않는 것

- 유지 전류가 쓸모없다고 하지 않는다 — 섞임을 가르지 않고 이름을 붙였을 때의 귀속 오류를 적었다.
- 정상 SEI 전류와 단락이 원리적으로 갈리지 않는다고 하지 않는다 — 전압 의존 · 온도 · 차분 · 두 장부 채널은 두 표본이 재지 않았다.
- Zhang 2026 의 셀에 단락이 있었다고 하지 않는다 — 원자료의 ≤0 점은 잡음일 수 있다.
- 수치는 사본이다 — 정본은 각 원문 · 원자료(raw digest 참조).
