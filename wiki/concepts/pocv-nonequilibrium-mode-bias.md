---
title: "pOCV 의 비평형 성분이 모드로 새는 경로 — IR · 이력(가지) · 창"
description: "A low-rate pseudo-OCV still carries ohmic drop, branch hysteresis and window boundaries, and an electrode-balancing fit projects them onto LLI/LAM parameters (phantom modes). Same symptom as fitting degeneracy, different cause. Two ways to treat IR (measured R(SOC) pre-correction vs a fitted constant offset), where our synthetic truth sits, and what transfers to the REIL charge-curve fits"
created: 2026-10-06
updated: 2026-10-06
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/asheruddin2025_phantom-lam-lli-ir-hysteresis-dma.md, raw/papers/schmitt2022_sic-ocp-shape-change-degradation-modes.md, raw/papers/2026-09-21-siwon-kim-si-gr-ica-lam-si-gitt-ocp.md, raw/papers/sun2025_dl-eis-degradation-mode-diagnostics.md, raw/papers/rhyu2025_systematic-feature-design-formation.md, raw/papers/li2026_half-cell-fitting-multiobjective-benchmark.md, raw/repositories/2026-10-05-ampworks-on-synthetic-truth.md, raw/repositories/2026-10-01-pyprobe-dma-on-synthetic-truth.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: multi-source-mixed
---

# pOCV 의 비평형 성분이 모드로 새는 경로 — IR · 이력(가지) · 창

## 정의

electrode balancing (DMA) 은 OCV 를 맞춘다고 말하지만 실제 입력은 **저율 · 유한 휴지의 pOCV** 다. Asheruddin N 외 2025
(arXiv 2512.19773 사전인쇄, raw `raw/papers/asheruddin2025_phantom-lam-lli-ir-hysteresis-dma.md`) 의 측정 모형 `[인쇄]`:

```
U_meas(Q) = U_PE^(b)(z_PE) − U_NE^(b)(z_NE) + η_kin(z, I) + I·R_Ω        (b = 충전 / 방전 가지)
```

적합 모형은 `U_PE − U_NE` (반쪽전지 기준 곡선을 늘이고 민 것) 뿐이므로 나머지 — 옴 강하 `I·R_Ω`, 동역학 `η_kin`, 그리고 **측정 가지와
기준 곡선 가지의 불일치** — 는 잔차로 남거나 **모드 매개변수 (창 배율 · 이동 · blend 몫) 로 사영된다.** 사영된 몫이 그 논문이 부르는
"phantom" LAM/LLI — 열화가 아닌데 열화로 읽힌 양 — 이다. 셋째 통로는 **창**이다: 같은 곡선이라도 맞추는 전압 구간이 바뀌면 모드가
'창 안 접근 용량의 비' 로서 다른 양이 된다.

한 줄 항등식 `[해석]` — 식 `U_mod = U_PE − U_NE` 에서 **기준 곡선을 +δ 올려 맞추는 것 ≡ 측정 곡선을 −δ 내려 맞추는 것**. 그래서
"반쪽전지 OCP 오프셋 (모델 오차)" 과 "IR 미보정 (측정 오차)" 은 같은 섭동이고, 우리 `ocpbias` 실험 (아래) 이 곧 SOC 무관 IR 미보정이다.

## 세 통로 — 실셀 크기 (원문 · 참값 없음 · 구성 간 차이)

| 통로 | 곡선에 남기는 것 | 모드로 가는 방향 (원문 기준 구성 대비) | 크기 (`[인쇄]` · 셀) |
|---|---|---|---|
| **옴 (IR)** | 방전은 아래로 · 충전은 위로의 거의 강체 이동 — SOC 에 따라 크기가 다름 (꼭대기가 큼) | 미보정 방전: LAM_PE ↓ · LLI ↓ · 흑연 LAM ↑ · Si-LAM ↓ | C/10 에서 +13–27 mV 이동 → 상대 오차 LAM_PE 최대 −8.80 % · LLI 중앙 −3.07 % · 흑연 중앙 +17.68 % (M50T NMC811 ‖ C/SiOx) — 절대로는 EOL 에서 LAM_PE · LLI · 흑연 ≈0.6–1.2 %p · Si ≈3.6 %p `[도표]` |
| **이력 (가지)** | 충전 곡선이 방전 위 — Si 함유 음극에서 큼 · 노화로 모양이 바뀜 | 충전 가지: LAM_PE ↑ · LLI ↑ · Si-LAM ↓ (초기 음수) · 흑연 ↓ (말기 음수) | 같은 3.0–4.2 V 창에서 LAM_PE +3.42 pp · LLI +5.36 pp · Si-LAM 차 +14.38 pp (P45B NCA ‖ C/SiOx, C/20) |
| **창** | 하한을 올리면 Si 민감 저전압 꼬리가 빠진다 | 하한 2.5 → 3.0 V: SoH ↑ · LAM_PE ↓ · LLI ↓ · Si-LAM ↓ · 흑연 ↑ | Si-LAM −13.61 pp · LLI −5.72 pp · LAM_PE −2.25 pp · SoH +2.90 pp (P45B 방전) |

`[해석]` 세 섭동 모두에서 **LAM_PE 와 LLI 가 같은 방향**으로 움직이고, **PE − NE 격차**가 ≈1.5–5 %p 움직인다 (IR ≈−1.45 · 가지 ≈+5.1 ·
창 +3.55 %p — raw §14). 이 크기는 [[22p-physics-or-degeneracy]] 의 판정선 (2 %p) 과 같은 자릿수다. 그리고 원문이 '기준' 으로 둔 구성
(보정 · 방전 · 전체 창) 이 세 실험 모두에서 **Si-LAM 을 가장 크게 내는 구성**이라, 참값이 없으면 어느 쪽이 유령인지 정해지지 않는다.

## 왜 축퇴와 같은 증상인가 — 그리고 어디서 만나는가

- [[fitting-degeneracy]] 는 *모델은 맞고 데이터가 방향을 못 정하는* 것이고, 여기는 *모델이 틀린* 것 (오설정) 이다 —
  [[halfcell-ocp-shape-invariance]] 의 Schmitt `γ_Si` 와 같은 "적합은 그대로인데 매개변수가 움직인다" 증상 · 다른 원인.
- **만나는 자리** `[해석]`: 오설정 δ 가 매개변수로 사영되는 양은 1 차로 `Δθ ≈ (JᵀJ)⁻¹Jᵀδ` 다. 작은 특이값 방향 (약방향) 이 그것을 가장
  크게 키운다. 즉 **유령 모드의 크기는 축퇴 구조가 정한다** — 위 표의 'LAM_PE · LLI 동부호' 가 그 모양과 맞고, 그 방향을 재는 것이
  우리 파이프라인의 일이다.
- 원문은 이것을 재지 않았다 — 적합 잔차 · 매개변수 값 · 다중 시작 · 상관 0, `identifiab*` 1 회 (근거 없는 "preserves identifiability").
  음수 구성요소 LAM 을 "under/over-compensation inside the NE decomposition" 이라 부르는 것이 보상 방향의 산문 진술의 전부다.

## IR 을 다루는 두 방식

| | **측정 R 사전 보정** (Asheruddin N 2025) | **적합 상수 오프셋** (ampworks `iR` · Sun 2025 `R` · Rhyu 2025 `V_shift` · PyDMA `allow_resistance_offset`) |
|---|---|---|
| R 의 출처 | ≈50 ms 펄스 첫 전압 계단 (`R_Ω = ΔV*/I`) | 곡선 맞춤의 자유 매개변수 |
| SOC 의존 | 보간 `R_Ω(SOC)` — 원문 값으로 꼭대기 ↔ 바닥 10 % 끌어올림 차 8.7 · 9.9 mV `[재현]` | 상수 한 값 |
| 담는 성분 | 순간 옴만 — 느린 성분은 "would import path dependence" 라며 일부러 뺀다 | 수직 잔차 전부 (옴 · 동역학 · 이력 반폭 · 기준 오프셋) 를 구별 없이 |
| 식별성 | 매개변수 수 그대로 | +1 — 원문의 기전 (수직 이동이 `ν_PE` · `σ` 로 흡수) 이 맞다면 오프셋 열이 LAM_PE · LLI 열과 부분 공선 → 새 약방향 후보 `[해석]` |
| 함정 | 측정 SOC 범위 밖은 외삽 — M50T 의 꼭대기 10 % 끌어올림은 측정 최대 R 을 넘는 값을 함의한다 `[재현·가정]` | 오프셋이 이력 · 기준 오차까지 먹어 '저항' 이라는 이름이 물리를 보장하지 않는다 |

- **같은 것이 아니다.** 둘 다 수직 이동을 다루지만 하나는 측정 · SOC 의존 · 전처리, 다른 하나는 적합 · 상수 · 동시 추정이다. 원문은 적합
  오프셋과 비교하지 않았으므로 PyDMA 옵션의 좋고 나쁨을 그 논문으로 판정할 수 없다. PyDMA 의 설명은 2026-10-06 호출자 전달이고 **코드는
  이 위키가 보지 않았다.**
- 시험 설계는 이미 있다 — [[halfcell-window-parametrization-lineage]] 일곱째 축 (Sun 2025) 의 "5×5 `JᵀJ` 최소 특이벡터에 R 성분이 얼마나
  실리는가". SOC 의존 오프셋을 넣은 합성 truth 에서 계산하면 ampworks `iR` ([[ampworks]]) · PyDMA 옵션에 같이 답한다 (미실행).

## 이 위키에서의 적용 — 우리 파이프라인의 자리

- **우리 truth 는 이미 원문의 권고 구성 위에 있다** (코드 읽기 · 실행 0): `degradation-degeneracy/configs/base.yaml` 15–17 행
  `negative: ["single", "current sigmoid"]` → truth 의 Si 상은 전류 부호로 리튬화 ↔ 탈리튬화 OCP 를 바꾸는 **방향 의존 OCP** 다. 적합은
  0.05 C `charge_first` 의 최종 **방전** 스텝 곡선을 **탈리튬화 가지** 기준으로 맞춘다 (`src/halfcell.py` 87–106 · 195–199 행 — 주석이
  가지를 섞었을 때 기준 곡선이 망가진 실측을 적어 둔다). ⇒ 우리가 잰 축퇴는 가지 불일치 · IR 보정 효과를 **뺀** 하한이다.
- **우리 0 mV 다리도 '미보정 pOCV' 다** — 0.05 C DFN 동적 곡선이고 과전압 서명이 0 이 아니다 (`degradation-degeneracy/docs/RESULTS.md`
  "이 결론이 말하지 않는 것" · Phase 1j — 수치는 거기).
- **셀 계열이 겹친다.** 우리 매개변수 집합 `Chen2020_composite` 는 PyBaMM 원본의 함수 이름 · 주석이 'LG M50' 이다 (`nmc_LGM50_ocp_Chen2020` ·
  `graphite_LGM50_…` · `silicon_LGM50_…` — 설치된 PyBaMM 의 `input/parameters/lithium_ion/Chen2020_composite.py` 를 읽기만 함). 원문의 IR
  실험 셀은 LG **M50T** (NMC811 ‖ C/SiOx) — 같은 계열 이름이지만 같은 판 · 같은 전극인지는 확인하지 않았다. 확인되면 원문 §3.2 는 우리
  합성 truth 셀 계열의 실셀 대응물이다.
- **`ocpbias` PE 오프셋 다리 = SOC 무관 IR 미보정의 합성 truth 판** (`src/halfcell.py` 144–148 행 · 정본 `docs/09_22P_GAP.md` §7.10 ·
  `docs/22p_gap/bias_pe{1,1p5,2,5,10}mv.txt`). 원문이 못 한 **참값 대비 오차**를 이미 갖고 있다. 원문과 다른 점: 균일 오프셋 (원문은
  꼭대기가 무겁다) · 음극 Si 몫 고정 (원문은 `φ_Si` 자유 — 흑연 ↔ Si 재배분이 우리 적합에서는 원리적으로 안 나온다).
- **값싼 대조**: P1 (**완료 2026-10-06 — 아래 "P1 결과"**) — §7.10 표의 ①' 격차 bias **부호**를 원문의 방향 (미보정 → LAM_PE ↓ · LAM_NE ↑ → 격차 음)
  과 대조 (먼저 '오차' 부호 규약과 지표 차이 — 보정 대비 상대 ↔ 참값 대비 격차 — 를 고정). P2 — 꼭대기 무거운 SOC 의존 오프셋 다리.
  P3 — `φ_Si` 자유 5 매개 적합 (참값을 아는 Gr ↔ Si 재배분). P4 — 충전 가지 + 탈리튬화 기준 (가지 불일치) 적합. P5 — 위 R 열 각도.
- 관측을 늘리는 쪽 ([[mode-observability]]) 에서 보면 충전 · 방전 두 가지는 같은 전극 상태의 **관측 둘**이다 — 가지별 기준 (이력 모형) 이
  있으면 정보가 늘고, 없으면 원문처럼 한 가지를 버린다. 원문은 동시 적합을 하지 않았다.

### P1 결과 — 격차 bias 부호 대조 (2026-10-06 · 실행 0 · 정본 표 재집계)

**부호 규약 (코드로 확인):** `ocpbias` 는 **기준** PE OCP 를 올린다 — `u_pe = u_pe + pe_offset_mv/1000` (`degradation-degeneracy/src/halfcell.py`
143–145 행 · truth 불변). 모델 `V = U_PE(+δ) − U_NE` 가 데이터보다 δ 높으므로 "데이터가 참 OCV 보다 δ 낮다" 와 같다 = 원문의 **미보정 방전
pOCV** (`V_meas = OCV − IR`) 방향. 오차 = 추정 − 참값. `①' 격차 bias` = 동작점 근방 (|LLI − 17 %| ≤ 2 %p · |평균 LAM − 13 %| ≤ 2 %p · noise 0) 의
`(LAM_PE 오차 − LAM_NE 오차)` 평균 (`degradation-degeneracy/tools/diagnose_pini_transition.py` `gap_stats`). 원문의 비교는 "보정 대비 상대" 이므로
같은 격자의 0 mV 다리를 뺀 **증분 Δ** 를 맞댄다.

대상 다리 (원점 건강만 — §7.10 의 오염 다리는 제외): PE 1 · 1.5 mV (dense) · PE 2 · 5 · 10 mV (seed_101) · 대조 NE +2 mV · PE+2 · NE+2 (dense).
Δ = 그 다리의 `①' 격차 bias` − 같은 격자 0 mV 다리의 값. **수치는 정본 `degradation-degeneracy/docs/09_22P_GAP.md` §7.10 표 (와 그 아래 NE · 공통 모드 표) 에서만
읽는다** — 이 위키에는 옮겨 적지 않는다 (위키 규칙: 연구 수치는 참조만).

**판독:** 원점이 건강한 PE 오프셋 다리 다섯 모두 Δ 가 **+** (LAM_PE 가 LAM_NE 보다 상대적으로 **과대** 쪽) 이고, 1–5 mV 다리의 Δ 는 판정선 2 %p 아래 · 10 mV 다리만 판정선 위다. 원문의 IR 방향 (미보정 →
LAM_PE 과소 · 흑연 LAM 과대 → 격차 −) 과 **반대 부호**다. NE 오프셋 대조는 Δ 가 작은 음수, PE+NE 공통 모드 대조는 Δ = 0 (상쇄) 이라 부호 규약이 뒤집히지 않았음을 받친다.

**이 대조가 말하지 않는 것 (반대 부호를 모순으로 읽지 않는다):**
- 원문에는 **참값이 없다** — "미보정이 LAM_PE 를 과소" 는 원문이 고른 보정 구성 대비이고, 그 구성의 참값 오차는 모른다. 우리 Δ 는 참값 대비 오차의 증분이다.
- 섭동 모양이 다르다 — 우리는 SOC 무관 **균일** 오프셋 · 원문은 꼭대기가 무거운 R(SOC) (원문 그림 1 의 측정 범위 밖 외삽 포함). 균일 오프셋은 dV/dQ 를 거의
  바꾸지 않아 (원문 그림 2 도 같음) 적합이 다른 경로로 흡수할 수 있다 → P2 (꼭대기 무거운 오프셋) 가 맞대는 시험.
- 셀 · 매개변수가 다르다 — 원문 M50T (NMC811 ‖ 흑연 + SiOx · `φ_Si` 자유 · LAM 을 흑연 / Si 로 나눔) ↔ 우리 `Chen2020_composite` (Si 몫 고정 · LAM_NE 하나). 원문의
  "흑연 LAM 과대" 와 우리 "LAM_NE 오차" 는 같은 양이 아니다 → P3.
- **성분별 부호 (LAM_PE · LAM_NE · LLI 각각) 는 이 컨테이너에서 볼 수 없다** — 바이어스 다리의 원 fit (`results/fit_22p_*`) 이 여기 없고, 정본 표는 격차 bias 만 싣는다.
  원문의 "LLI 과소" 와의 대조는 미확인.
- 크기는 맞대지 않는다 — 원문의 IR 크기 · 셀 · 지표가 달라 (원문 수치는 raw digest 참조).

## REIL 로 옮기면 — 방향만, 크기는 아니다

[[isu-uconn-lfp-gr-emulated-degradation]] 은 LFP/흑연 코인셀의 C/20 **충전** 곡선을 맞춘다. 원문은 LFP · Si 없는 음극 · 코인셀을 다루지 않는다.

1. 충전 곡선은 `I·R` + 이력만큼 OCV 위다 → 고정 창에서 상한에 일찍 닿아 창 안 용량 ↓ · 겉보기 LLI ↑ (원문 Fig. 7a · 7c 의 방향). REIL
   맞춤 LII 가 사실상 충전 용량을 읽으므로 셀마다 다른 수직 이동은 LII 를 셀마다 다르게 낮춘다. 원판 지름이 셀마다 달라 (설계) 공통 모드
   상쇄를 가정할 근거가 없다.
2. dV/dQ 는 균일 이동에 1 차로 불변 (원문 Fig. 2b) → REIL 목적 f3 · f4 는 둔감하고 f1 (끝점 전압) · f2 (QV MSE) 가 그것을 짊어진다.
3. 가지 편향의 원천은 **완전지 가지 ↔ 반쪽전지 기준 가지 불일치**다 — REIL 의 P0 방향 대조 (부속 C 재검토 RV2C-N3) 가 그 통제다. 원문은
   그 항목이 왜 결과를 좌우하는지의 Gr/SiOx 크기만 준다.
4. 원문의 LAM_PE 기전은 NMC/NCA 의 가파른 꼭대기에 기댄다. LFP 는 양끝 외에는 평탄해 수직 이동이 다른 매개변수로 갈 것이고, 어디로인지는
   원문이 말하지 않는다. 판단 (해석 제한으로 적을지) 은 REIL 문서 쪽 몫이다.

## 실셀 DMA 를 읽을 때 체크리스트

1. **가지 · 율 · 휴지** — 그리고 반쪽전지 기준 곡선의 가지 · 율이 같은가.
2. **IR** — 보정했나 · 측정 `R(SOC)` 인가 적합 상수인가 · 측정 SOC 범위 밖은 어떻게 (외삽)?
3. **창** — 하한 · 상한 · RPT 마다 다시 정하나? 모드가 창 안 접근 용량의 비라면 창 변화가 LAM 으로 보인다.
4. **blend** — `φ_Si` 를 열었나 · 값과 일관성 잔차 (`Q_NE` vs `(1−φ)Q_Gr + φQ_Si`) 를 보고했나 · 비단조 · 음수 구성요소 LAM 을 표시했나
   (원문은 공통 창 방전에서 규칙이 성립하지 않는 값을 낸다 — raw §2-m).
5. **정규화** — SOC 를 RPT 마다 정규화했다면 셋째 자유도 (공통 인수) 를 무엇으로 닫았나 ([[np-lip-ocv-reparametrization]]).
6. **구성 간 차이를 '오차' 로 읽지 않는다** — 참값이 없으면 어느 구성이 유령인지 정해지지 않는다.

## 반대 해석 / 데이터 공백

- 근거의 본체가 **사전인쇄 한 편 · 셀 종류당 1 개 · 참값 0 · 잔차 0** 이고, 원문 안에 가지 ↔ 전극 과정 · 부호 · `ν` 규약 · 그림 ↔ 본문
  수치 불일치가 여럿이다 (raw §2). 위 표의 크기는 '원문이 인쇄한 값' 이지 검증된 효과 크기가 아니다.
- 항등식 (기준 +δ ≡ 측정 −δ) 은 **균일** 이동에서만 정확하다. 원문의 IR 은 SOC 의존이고 dQ/dV 무게중심도 약간 움직인다 — 우리 균일
  다리와 1:1 이 아니다.
- 원문의 기준 구성 (보정 · 방전 · 전체 창) 자체가 편향일 가능성 — 셋 다 Si-LAM 최대 쪽이다.
- PyDMA 는 호출자 설명뿐 (코드 미확인) · Karger et al. (원문 DMA 틀의 원전) 은 원문 참고문헌 목록에 없다.

## 관련
- [[fitting-degeneracy]] — 같은 증상 · 다른 원인, 그리고 사영 크기를 정하는 약방향
- [[halfcell-ocp-shape-invariance]] — Si 방향 의존 (세 번째 파괴 방식) · `γ_Si` 처방 ③
- [[halfcell-window-parametrization-lineage]] — 일곱째 축 (상수 `R`) 과 이 페이지의 측정 보정 대조
- [[np-lip-ocv-reparametrization]] — SOC 정규화와 셋째 자유도
- [[data-window-identifiability]] — 창이 어느 전극 (성분) 을 보이게 하는가
- [[thermo-kinetic-loss-partition]] — `η_kin` 쪽 분해
- [[pyprobe]] · [[ampworks]] — 같은 계열 도구 (원문이 쓴 도구 · 적합 `iR`)
- [[22p-physics-or-degeneracy]] · [[degradation-degeneracy]] · [[mode-observability]] · [[isu-uconn-lfp-gr-emulated-degradation]]
