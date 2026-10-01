---
title: Li2S 첫 충전 활성화
description: "절연체 Li2S 의 첫 탈리튬화 장벽 — 첫 충전에서 활성화한 만큼만 이후 용량이 된다(Kim 2023 Fig. S1), 3.2 V 단조 plateau 와 직접 전환, 활성화를 정하는 요인"
created: 2026-09-11
updated: 2026-10-02
type: concept
tags: [activation, li2s, carbon, liquid-electrolyte, assb, sulfide-electrolyte]
sources: [raw/papers/kim2023_reinforced-electrical-networking-high-loading-li2s-cathode.md, raw/transcripts/2026-09-11-li2s-wiki-kickoff-session.md, raw/papers/wan2021_lii-libr-catalyst-solid-state-li2s-s-reactions.md, raw/papers/zhang2026_anode-free-assb-nanocrystalline-amorphous-li2s-na-collector.md, raw/papers/cronk2026_highly-utilized-practical-li-s-positive-electrode-assb.md, raw/papers/lee2026_decoupled-sulfur-redox-pathways-initial-chemical-states-assb.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: empirical
evidenceScope: multi-source-primary
---

# Li2S 첫 충전 활성화

## 정의

Li2S 는 전자·이온 모두 절연에 가깝고(`[인쇄]` ~10⁻¹³ S cm⁻¹, Kim 2023 도입부가 refs 21·22 를
인용), 첫 충전(탈리튬화)에 높은 활성화 에너지가 필요하다. **"첫 충전에서 활성화된 Li2S 가
이후의 에너지밀도와 사이클 용량을 지배한다"** — Kim et al. 2023 이 도입부에 명시하고 Fig. S1
로 보인 명제 (`raw/papers/kim2023_…` §2.2, §9.1).

## 근거 (Kim 2023 — 액체 에테르 전해질, Li 금속 반쪽셀)

1. **Fig. S1 (★)**: 첫 충전 용량을 25/50/75/100 % 로 제한한 네 셀의 이후 방전 용량이
   `[도표]` ≈ 270 / 530 / 730 / 930 mAh g⁻¹(S) 로 **20 사이클 동안 네 층 그대로** 유지된다.
   활성화 안 된 Li2S 는 뒤 사이클에서 자발적으로 깨어나지 않았다.
2. **곡선 모양**: Gr/CNT 양극의 첫 충전은 `[도표]` ~3.4 V 스파이크 후 **3.15–3.2 V 에서 시작해
   완만히 상승**하며 3.6 V 컷오프까지 이어진다. 통상의 Li2S 곡선(초기 고전압 → LiPs 가 redox
   mediator 로 작동하며 전압 하강)과 달리 **내려가지 않는다** — 저자는 이를 LiPs 없는
   **직접 전환 Li2S → S8** 의 서명으로 읽고 in situ Raman(S8 12 % SoC 조기 출현, LiPs 밴드 부재)·
   in situ OM(노란 LiPs 없음)·cryo-TEM(50 % SoC 에 β-S8 + Li2S 공존)으로 뒷받침한다.
3. **활성화를 늘린 요인** (저자 귀속): 2D 그래핀의 큰 접촉면적, 소량 CNT 의 네트워크(전기적
   고립부 제거), 1 GPa compact geometry, 고압 성형으로 생긴 준안정 orthorhombic Li2S.
   → [[carbon-dimensionality-electron-network]].

## ★ 활성화 전위 사다리 (2026-10-02 — 고체계 digest 4편)

이 개념의 중심 질문이 2026-09-30 에 바뀌었다. **"얼마나 활성화되나" 가 아니라 "활성화를 끝내는
전위가 SE 가 견디는 전위보다 높은가" 다** ([[reference-cell-500-600-mahg]] H1). 그 전위를 낮추려는
네 가지 시도를 digest 에서 꺼내 나란히 놓으면 사다리가 된다:

| 논문 | 활성화 전위 | 수단 | **무게 대가** | 사후 기여 분해 |
|---|---|---|---|---|
| **Cronk 2026** | **2.4 V** `[인쇄]` | 밀링이 만든 thiophosphate 계면상, `[인쇄]` **"촉매 없이"** | **0** | ✓ dQ/dV 4영역 + XANES LCF |
| **Wan 2021** | ≈**2.80 V** `[도표]` | LiI–LiBr 할로겐화물 | **39.9 wt%** `[재현]` | ✗ 사후 분석 0건 |
| **Zhang 2026** | 2.87 V | PI3 → in-situ LiI | **43.8 wt%** `[재현]` | ✗ |
| **Lee 2026** | — (컷오프 **3.62 V** vs Li/Li⁺) | 없음 — 전위를 올려서 끝낸다 | 0 | ✗ (대가는 이론 초과 용량 101–107 %) |

`[해석]` 두 가지가 읽힌다.
1. **요오드 경로는 2.8 V 아래로 내려가지 못한다.** 두 논문이 독립적으로 2.80·2.87 V 에 머문다.
2. **무촉매파(Cronk)가 더 낮은 전위를 무게 대가 0으로 달성한다.** 그리고 **기여 분해를 한 것도
   Cronk 뿐이다.** 우리 30:50:20 에는 39.9 wt% 짜리 첨가제가 들어갈 자리가 없으므로,
   이식 가능성에서도 Cronk 쪽이 앞선다.

### 첨가제가 없으면 plateau 자체가 없다 (Wan 2021 Fig. 2a)

같은 셀에서 Li2S 양극을 직접 대조한 `[도표]` 관측이 이 개념의 가장 선명한 그림이다:

| | Li2S@LiI–LiBr | **첨가제 없는 Li2S** |
|---|---|---|
| 첫 충전 | ≈1165 mAh g⁻¹(Li2S) = 이론의 ≈100 % | ≈900 = **77 %** |
| 첫 충전 **plateau** | **≈2.80 V 평탄** | **plateau 가 없다** — 2.5 → 3.5 V 단조 상승 |
| 첫 방전 | ≈835 (Li2S) = `[재현]` ≈1196 (S) | ≈510 = `[재현]` ≈731 |

→ **plateau 의 유무 자체가 활성화 경로가 열렸는지의 지표다.** 우리 첫 충전 곡선에서 가장 먼저
볼 것이 이것이다 (평탄한가, 컷오프까지 끌려가는가).

### ⚠ "촉매" 인지 "매개체" 인지 이 위키는 아직 모른다

Wan 2021 digest 의 가장 날카로운 관측: **2.80 V plateau 는 Li2S 산화치고 너무 평탄하고 너무
길다**(이론용량 거의 전부). 그건 전형적인 **매개체(mediator) 반응의 모양**이고 후보는 I⁻/I₃⁻ 다.
**그 논문은 "catalyzer" 를 10회 쓰면서 "mediator" 를 한 번도 쓰지 않는다.**

그리고 **Wan 2021 도 Zhang 2026 도 할로겐화물 자신의 용량 기여를 분리하지 않았다.**
`[재현]` LiI 1 e⁻ 몫은 Wan 쪽 **109.4**, Zhang 쪽 **152 mAh g⁻¹(Li2S)** — 같은 급이다. 빼면
Wan 의 "이용률 100 %" 가 **≈90.5 %** 로 내려간다.
→ 그래서 이 위키는 이것을 **"촉매" 라 부르지 않고 "할로겐화물 첨가제"** 라고 적는다.
판정하려면 **`LiI + LPSCl + AB`(활물질 없음) 대조셀**이 필요하고, **두 논문 다 그것을 빠뜨렸다.**

### 우리 노선에 대한 반례 (같은 digest)

`[인쇄]` **Li2S@LiI–LiBr 30사이클 유지 79.7 % < MoS2@LiI–LiBr 94.7 %** — 첨가제 비율이 더 높은
Li2S 쪽이 **더 빨리 죽는다**. 할로겐화물이 첫 충전은 열어주되 수명은 보장하지 않는다는 뜻이다.
(단 Wan 2021 의 주 활물질은 MoS2 이고 그 Li2S 는 MoS2 분해로 **in-situ 나노 생성**된 것이라
우리 상용 분말과 태생이 다르다 — 이식 한계.)

## 활성화를 정하는 변수 (이 위키의 작업 목록)

| 변수 | Kim 2023 에서 | 우리 ASSB 에서 |
|---|---|---|
| 전자 접촉·네트워크 | Gr 접촉 + CNT 3 wt% 네트워크 | AB 20 wt%; 탄소 차원 분리 미시도 |
| 입자 크기 | micro 1–5 µm 그대로 | ball milling 으로 나노화 시도 ([[composite-cathode-mixing-routes]]) |
| 이온 접근 | 액체 전해질이 어디든 닿음 | **LPSCl 이 Li2S 표면에 닿아야만** 반응 — 삼상 계면 |
| 전압 컷오프 | 3.6 V vs Li/Li⁺ | SE 산화 한계 안에서 — 값은 ingest 후 (미검증) |
| C-rate | 0.1 C (활성화), 0.05 C(파우치) | 미결 Q3 |
| 매개체 | LiNO3 0.8 M (고농도), LiPs 미형성 | 고체라 LiPs 매개 없음 — 직접 전환이 **기본 경로** |

`[해석]` 마지막 줄이 핵심이다: 액체계에서 "특이" 하다고 보고된 직접 전환이 고체계에서는
**유일한 경로**다. 따라서 Kim 2023 의 in situ 관측은 우리 활성화 과정의 **정성적 모델**로
쓸 수 있다 (다만 LiNO3·에테르가 만든 환경은 뺀 채로).

## 이 위키에서의 적용

- [[reference-cell-500-600-mahg]] 의 H1(활성화 제한) 이 이 개념 위에 선다: 우리 셀의 **첫 충전
  용량 vs 이후 방전 용량** 관계를 Fig. S1 방식으로 찍어 보는 것이 가장 값싼 진단이다.
- [[anode-free-li2s-assb]] 에서는 활성화량 = Li 재고 상한.

## 한계·불확실성

- 근거가 논문 하나(액체계)뿐이다 — `single-source`, confidence 는 medium 을 넘기지 않는다.
- Fig. S1 의 셀 조건(어느 양극·로딩)이 캡션에 없다.
- ASSB 에서 같은 "활성화 후 층 유지" 가 성립하는지는 **미검증** — ingest 대상.
