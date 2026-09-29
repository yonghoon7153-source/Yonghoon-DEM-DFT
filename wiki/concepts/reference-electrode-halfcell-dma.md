---
title: 기준전극 기반 half-cell 분해 DMA
description: "In-situ reference electrode DMA: LAM from DVA feature spacing, LLI from lateral offset — no optimizer, and what it costs"
created: 2026-09-10
updated: 2026-09-29
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/natterer2026_re-halfcell-anode-potential-aging.md, raw/papers/buchberger2015_graphite-nmc111-aging-xrd-ca-li-loss-pgaa-impedance.md, raw/papers/birkl2017_degradation-diagnostics-ocv.md, raw/papers/marongiu2016_lfp-onboard-capacity-halfcell.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: definition
evidenceScope: multi-source-primary
---

# 기준전극 기반 half-cell 분해 DMA

## 정의

셀 안에 **기준전극(RE)** 을 심어 두 전극의 전위를 따로 기록하고, 그 half-cell
곡선의 **DVA 특징점 위치만으로** 열화 모드를 산술로 계산하는 DMA 절차.
정본 사례는 Natterer et al. 2026 (`raw/papers/natterer2026_re-halfcell-anode-potential-aging.md`,
LTO-RE 를 넣은 NMC-811‖Gr 단층 파우치 1000 사이클).

**세 식이 전부다** (원문 식 1–4):

```
Q_LAM,neg = Q_II − Q_III                        (1)   # 한 전극 안 두 feature 사이 거리
LAM_neg   = 1 − Q_LAM,neg / Q_LAM,neg,init      (2)   # 초기 RPT 기준 상대량
ξ_OCP     = ξ_OCP,init · (1 − LAM) · Q_cycle/Q_ref   (3)   # pristine OCP 를 LAM·SoH_C 로 스케일
Δξ_LLI    = ξ_OCP^feature − ξ_meas^feature      (4)   # 스케일된 곡선 대비 가로 이동량
```

LAM_pos 는 (1)–(2) 를 양극 feature 쌍(NMC C1↔C3)에 그대로 적용한다. LLI 는 두
전극 창의 겹침(LI) 변화로 마무리된다.

**핵심 성질**: 한 전극 **안의** 두 feature 사이 거리는 LLI 가 바꾸지 못한다
(LLI 는 두 전극의 **상대 오프셋**만 움직인다). 따라서 `LAM_neg`·`LAM_pos` 는
서로, 그리고 LLI 와 **구조적으로 분리되어** 측정된다.

## 왜 중요한가

이 위키의 모든 DMA 계보([[birkl-ocv-degradation-diagnostic]],
[[dubarry-mechanistic-mode-synthesis]], [[halfcell-window-parametrization-lineage]])는
**같은 4개 창 좌표**를 쓴다. 차이는 그 좌표를 **무엇으로 못 박는가** 뿐이다:

| 방법 | 여분(null)을 죽이는 수단 | 최적화 |
|---|---|---|
| Dubarry 2012 | 매개변수를 애초에 2개만 만든다 | 정방향 합성 |
| Birkl 2017 | 컷오프 전압 **등식 제약** 2개 | `fmincon` + MultiStart |
| Lin & Khoo 2024 | 좌표 자체를 2 자유도로 재매개화 | — (구조 정리) |
| **이 방법** | **관측 채널을 늘린다** (full-cell 1 → half-cell 2) | **없음 (산술)** |

마지막 줄이 이 개념의 전부다. **최적화가 없으면 [[fitting-degeneracy]] 가 말하는
"평평한 골짜기에서 추정기가 미끄러진다" 는 통로 자체가 사라진다.** 축퇴는
목적함수의 성질인데, 목적함수가 없기 때문이다.

그 대신 **다른 종류의 오차로 갈아탄다** — 아래 "대가" 참조. 축퇴가 사라지는 것이
아니라 **불확실성이 최적화 지형에서 특징점 판독으로 이동**한다.

## 대가 (이 절차가 참이려면 참이어야 하는 것)

1. **feature 화학량론 불변** — DVA 극값이 대응하는 전극 화학량론이 수명 내내
   고정. Birkl 의 가정과 동일하며, 이 절차는 그것을 **더 강하게** 쓴다(위치를
   직접 값으로 읽으므로).
2. **저전류 곡선 ≈ OCP** — Natterer 는 RPT 를 **0.2 C** 로 돌린다(보통의 C/20 보다
   훨씬 빠르다). 원문 Fig. 1a 에서 GITT OCP 와 0.2 C 곡선의 차이가 `[도표]`
   10–25 mV 이고 OCP 에 있는 ≈60 mAh 계단이 측정 곡선에는 없다.
3. **pristine OCP 재사용** — 노화된 전극의 OCP 를 다시 재지 않는다. Ni-rich
   양극의 OCP 형상 변화(Rodrigues 의 blending 문제)를 "이 경우엔 불필요" 로
   판정하는데, 그 판정 근거인 Fig. A.1 의 **DVA 재구성은 양극·full-cell 에서
   실제로 어긋난다** (raw digest §9). 이 가정이 무엇이고 어디서 깨지는지는
   [[halfcell-ocp-shape-invariance]] 가 따로 다룬다 — 그 페이지의 Si/Gr blend
   사례와 달리 Natterer 의 셀에는 **Si 가 없고**(순수 graphite), 형상이 흔들리는
   쪽은 **양극(NMC-811)** 이다.
4. **peak 판독 절차** — 평활·미분·창 정의가 원문에 인쇄되지 않았다.
   [[mode-observability]] Phase 1 이 실측한 "valley 정의 하나로 feature 값이
   −20.0 vs −11.3 으로 갈린다" 와 같은 자유도다.
5. **기준전극 위치** — 같은 셀에서 스택 **밖** LTO-RE 와 스택 **안** 금선 RE 가
   `[도표, 원문 Fig. 4]` 0.75 C 에서 **20 mV 이상** 다른 음극 전위를 준다
   (LTO ≈ +18 mV vs GWRE ≈ −5 mV). 저자는 이를 상수 옴 항 `R_GWRE→LTO-RE = 0.35 Ω`
   로 흡수한다.
   → **단, 모드 계산(식 1–4)은 전위의 세로 절대값을 쓰지 않고 특징점의 가로
   위치만 쓴다.** 그래서 이 오차는 **전위 결론**을 위협하지 가로축 기반
   **모드 결론**을 직접 위협하지는 않는다. 두 결론의 신뢰도를 분리해서 다뤄야 한다.
6. **셀 1개** — 원문은 4셀로 시작해 3셀을 잃었다. 셀 간 재현성이 0.

## 이 위키에서의 적용

- **α·β 검증의 독립 근거 "형태"**: [[degradation-degeneracy]] 는 손으로 맞춘 창
  좌표가 맞는지 확인할 외부 근거를 찾고 있다. 이 절차는 그 근거가 **어떤 모양이어야
  하는지**를 보여 준다 — 전극별 관측 채널 + 최적화 없는 산술. 다만 Natterer 의
  데이터 자체는 `[인쇄]` "Data will be made available on request" 라 즉시 쓸 수 없다.
- **판정 기준 하나**: 어떤 논문이 "half-cell 로 검증했다" 고 할 때 물어야 할 것은
  "**최적화가 있었는가**" 와 "**pristine OCP 를 재사용했는가**" 두 개다. 둘 다
  '예' 면 그 half-cell 은 검증이 아니라 **같은 가정의 반복**이다.
- **반사실 대조군이 비어 있다**: 원문의 가장 강한 주장("RE 가 없었으면 양극 저항
  증가가 음극에 오귀속됐을 것")에 대조 실행이 없다. 같은 PyBaMM 모델에서
  half-cell 항만 뺀 적합을 돌리면 값싸게 채울 수 있고, 그것이 곧
  [[fitting-degeneracy]] 의 정량 측정이 된다.

## ★ 구조 채널판 — 사후 XRD 로 방전 끝 양극 Li 재고를 산술로 읽는다 (2026-09-29, `assb` 78호 Buchberger 2015 · 액체 흑연/NMC111)

`raw/papers/buchberger2015_graphite-nmc111-aging-xrd-ca-li-loss-pgaa-impedance.md` (Buchberger · Seidlmayer · … · Gasteiger 2015 *J. Electrochem. Soc.* 162, A2737). 기준전극 대신 **해체 양극의 격자**를 관측 채널로 쓰는
같은 모양의 절차다 — 위 표의 "관측 채널을 늘린다 · 최적화 없음" 줄에 **구조판**으로 붙는다.

```
ΔC_active-Li = 278 mAh g⁻¹ × [ x(c/a)_aged − x_ref ]        x(c/a) = (c/a − 4.9722)/0.3552   (in situ Li/NMC111 반쪽 교정, x 0–0.5)
x_ref = 0.109 (1 C — 표 I)  또는  0.084 (0.1 C ICL — 표 III, 인쇄 없이 바뀜)
```

- `[인쇄]` 흑연/NMC111 Swagelok 풀셀 세 조건 × 두 셀 · 1C/1C · ≤300 사이클 → ΔC_active-Li / ΔC_cycling = 4.2 V · 25 °C 3.6/7.4 · 3.3/6.9 · 4.2 V · 60 °C 57.3/62.0 · 60.9/64.5 · 4.6 V · 25 °C 53.9/119.9 · 58.9/127.5 mAh g⁻¹.
  교차: 해체 양극 반쪽 첫 사이클(방 − 충) ↔ XRD(0.1 C 기준) 4.2 V 넷에서 −3.8 … +3.4 mAh g⁻¹.

**대가 (이 절차가 참이려면 참이어야 하는 것 — 위 여섯에 대응)**

1. **기준 상태가 규약이다** — LLI 가 없을 때의 방전 끝 x 를 재지 않고 전하로 셌다(0.084 · 0.109). 두 기준이 LLI 를 7.0 mAh g⁻¹ 옮기고, 1 C 보정(도출 미인쇄)을 Fig. 11 로 읽으면 0.106–0.129 — 4.2 V · 25 °C 셀 LLI 가 −2 … +4.6.
   같은 교정으로 기준 상태를 읽으면 0.051–0.083(격자 ↔ 전하 눈금 섞임). `[해석]` 위 대가 1(feature 화학량 불변)의 구조판 — 영점을 무엇으로 못 박느냐가 값을 정한다.
2. **방전 끝이 재고 한계여야 한다** — 격자 x 는 양극에 없는 Li 를 센다. 분극 한계 방전(4.6 V 셀 — CV 몫 ≈62 % · EIS ≥235 Ω·cm²)이면 흑연에 남은 Li 가 LLI 로 섞여 **상한**이 된다(`[해석]` — 해체 흑연의 남은 Li 는 안 쟀다).
3. **형성 저장소** — 형성 결손이 "큰 쪽" 규칙(`[인쇄]` NMC ICL 0.27 · 흑연 SEI 0.22 → 풀셀 0.28 mAh)이라 흑연에 ≈4–5 mAh g⁻¹_NMC(1 C 에서 ≈11–12)의 가역 Li 가 남는다 — LLI 는 이것을 먼저 먹고 그동안 용량도 x 도 안 움직인다(`[재현]` · `[해석]`).
   ⇒ 같은 셀의 LLI 가 정의에 따라 갈린다 — **A 1 C 용량 유효(3.6) · B 양극 결손 0.1 C 기준(10.6) · C 재고 손실(≈15)** (4.2 V · 25 °C ①, 용량 손실 7.4).
4. **교정 이송** — 교정은 in situ 반사 · Kα1+2 · 첫 두 사이클, 읽기는 ex situ 투과 · Kα1 · 방전 가지. 원형 대조 인쇄 0 · 가지 · 사이클 몫 x ±0.03 안팎([[nmc-lattice-li-content-calibration]] 78호 절).
5. **LAM 은 재지 않는다** — 반쪽 0.1 C 용량 저하(4.6 V NMC 44–54 %)를 `[인쇄]` "either a substantial loss of active material or substantially increased impedance" 로 두고, TM 용출(PGAA ≤0.77 mol%)만 지워 저항으로 닫았다 —
   균열 · 입자 고립 · 절연 표면층의 LAM 은 열려 있다.
6. **셀 수 · 산포** — 조건당 두 셀(셀별 값) · 교정 셀 1 · 격자 esd · 계수 불확도 0.

**이 위키에서의 적용 (`[해석]`)** — (i) "적합 없는 외부 LLI 근거" 의 **모양**은 여기도 선다: 최적화가 없으니 [[fitting-degeneracy]] 의 골짜기 통로는 없다. 대신 불확실성이 **영점 규약(기준 상태)과 방전 끝 한계 전극**으로 옮겨 간다 —
위 "축퇴가 사라지는 것이 아니라 불확실성이 이동한다" 의 둘째 표본. (ii) 합성 truth 의 LLI(순환 재고)와 이런 실측 LLI 를 대조할 때는 **정의(A · B · C)와 기준을 값 옆에** 적는다 — 경미 열화에서는 정의 차가 신호보다 크다.
(iii) "LLI ≈ 용량 손실" 은 방전 끝 재고 한계 + 저장소 소진 뒤에만 선다(60 °C 셀 92–94 % · 25 °C 셀 48–49 %). ⚠ 액체 NMC111 · 한 연구실 · 조건당 두 셀 — 우리 수치(정본 artifact + `degradation-degeneracy/docs/RESULTS*.md`)와 대조하지 않았다.

## 관련
- [[fitting-degeneracy]]
- [[birkl-ocv-degradation-diagnostic]]
- [[halfcell-window-parametrization-lineage]]
- [[np-lip-ocv-reparametrization]]
- [[22p-physics-or-degeneracy]]
- [[nmc-lattice-li-content-calibration]] — 78호 구조 채널의 교정(격자 → x)과 그 규약
