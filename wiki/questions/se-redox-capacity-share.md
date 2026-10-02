---
title: 우리 셀 용량 중 황화물 SE 가 내는 몫은 얼마인가
description: "digest 24편 중 8편이 이론용량을 초과해 보고하고 넷이 SE 리독스를 본문에서 정면 인정하는데, 그 몫을 측정한 논문은 둘뿐이고 둘 다 불완전하다. 외부 눈금이 4–6 %에서 면적용량 1.5 mAh cm⁻² 까지 흩어져 있어 우리 분모를 문헌에서 빌릴 수 없다"
created: 2026-10-02
updated: 2026-10-02
type: research-question
tags: [units, sulfide-electrolyte, composite-cathode, li2s, assb]
sources: [raw/papers/cronk2026_highly-utilized-practical-li-s-positive-electrode-assb.md, raw/papers/kim2025_high-areal-capacity-sulfur-cathode-dual-phase-electrolyte-assb.md, raw/papers/kimjt2023_mixed-discharge-products-li2s2-li2s-asslsb.md, raw/papers/wangd2025_overcoming-conversion-limitation-tpb-mixed-conductors.md, raw/papers/gao2024_cu-i-codoping-activating-li2s-redox-kinetics-assb.md, raw/papers/leej2025_halide-segregation-assb-lithium-chalcogen.md, raw/papers/wangx2026_dual-conductivity-optimization-high-rate-ultralong-life-asslsb.md, raw/papers/feng2026_anode-free-asslsb-fe-stabilized-polysulfides.md, raw/papers/zhangj2026_strain-coordination-long-cycling-assb.md, raw/papers/park2026_low-pressure-operation-carbon-coated-current-collector-asslsb.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: empirical
evidenceScope: multi-source-primary
status: open
feedsInto: "[[reference-cell-500-600-mahg]] H4 의 분모 · [[capacity-normalization-li2s-vs-sulfur]] 의 이용률 계산 · [[reference-cell-experiment-plan]] 0단계"
---

# 우리 셀 용량 중 황화물 SE 가 내는 몫은 얼마인가

## 질문

**우리 `Li2S : LPSCl : AB = 30:50:20` 셀에서, 측정된 용량 중 얼마가 Li2S 가 아니라 LPSCl 에서 오는가.**

부속 질문 둘:
- **(a) 그 몫은 가역인가** — 첫 사이클 한 번인가, 사이클마다 계속 내놓는가.
- **(b) 전압창에 어떻게 의존하는가** — 특히 **활성화 컷오프 구간**에서.

## 왜 중요한가 — 이 질문이 닫히지 않으면 "이용률" 이 성립하지 않는다

이 위키가 24편을 읽는 동안 가장 자주 부딪힌 벽이다. 분모가 정해지지 않으면
**"Li2S 이용률 몇 %" 라는 문장 자체가 쓸 수 없다.** 그런데:

- **digest 24편 중 8편이 이론용량을 초과해 보고한다** (아래 표).
- **넷이 SE 리독스를 본문에서 정면 인정한다** — 그리고 **넷 다 그 몫을 측정하지 않는다.**
- **측정을 시도한 논문은 둘뿐이고 둘 다 불완전하다.**
- **외부 눈금이 `[재현]` 4–6 % 에서 면적용량 1.5 mAh cm⁻² 까지 흩어진다** — 같은 자에 올려놓을 수가 없다.

그래서 이것은 "나중에 확인할 것" 이 아니라 **[[reference-cell-experiment-plan]] 의 0단계**다.

### 이론 초과를 보고한 8편 (`[재현]` 2전자 천장 대비)

| digest | 초과율 | 조건 |
|---|---|---|
| **Kim 2025** (Φc) | **137.6 %** | S8, LPSCl dual-phase |
| **Cronk 2026** | **129 %** | 첫 CE, 우리와 같은 30:50:20 |
| **Yu 2024** | **124 %** | 60 °C |
| **Feng 2026** | **116 %** | ★ **풀셀** — 반쪽셀(868)보다 크다 |
| **Zhang 2026** | **114 %** | anode-free |
| **Wang 2026** | **111 %** | LGPS, DABDT |
| **Park 2026** | **105.6 %** | C/20, 하한 컷오프 1.0 V |
| **Lee 2026** | **101–107 %** | 무가압 코인셀 |

★ **1전자 천장(836 (S) / 583 (Li2S))으로 보면 전부 두 배가 된다** — Cronk 258 % · Kim 2025 275 % 등
([[capacity-normalization-li2s-vs-sulfur]]). **즉 Li2S2 가설은 이 문제를 설명하지 않고 두 배로 키운다.**

### SE 기여를 본문에서 인정한 넷 — 그리고 넷 다 안 쟀다

| digest | 무엇이라고 썼나 |
|---|---|
| **Kim 2025** | **가장 정면** — `[인쇄]` LPSCl 산화분해물의 **S–S bridging/cleavage 리독스**로 명시 귀속하고, 2차 방전이 1차 충전과 일치함으로 가역성을 보인다. `[재현]` 1차 충전 초과분 468.4 mAh g⁻¹(S) = 충전의 **27.3 %** |
| **Kim JT 2023** | `[인쇄]` *"these values include capacity contribution that comes from sulfide SSE decomposition"* / *"The decomposition products of LGPS are electrochemically active, and contribute to the reversibility capacity"* — **본문에 두 번** |
| **Lee (Jieun) 2025** | `[인쇄]` 이론용량 초과를 **"capacity contribution of the LPSCl SSE"** 로 귀속(table S6) |
| **Zhang (Jiaxu) 2026** | `[인쇄]` 사이클 중 용량 상승을 **"LPSC reduction to Li2S by VGCF and Fe particles"** 로 귀속 |

## 가설

- **S1 (첫 사이클 한 번)**: SE 분해는 초기 몇 사이클에 끝나고 그 뒤에는 기여하지 않는다.
  그렇다면 분모는 **첫 사이클만** 보정하면 된다.
- **S2 (계속 가역으로 기여)**: 분해생성물이 전기화학적으로 활성이어서 **사이클마다 용량을 보탠다.**
  Kim 2025 와 Kim JT 2023 이 그렇게 주장한다. 그렇다면 **모든 사이클의 분모가 틀렸다.**
- **S3 (전압창 의존)**: 기여는 **활성화 컷오프 구간과 깊은 하한**에서 집중된다. 우리 운전창을
  좁히면 몫이 줄어든다.
- **S4 (탄소가 촉진)**: SE 단독이 아니라 **탄소 접촉이 분해를 가속**한다. 그렇다면 대조셀은
  `LPSCl` 단독이 아니라 **`LPSCl + AB`** 여야 한다.
- **S5 (초과의 일부는 SE 가 아니다)**: 음극 Li 재고가 양극으로 넘어오는 **별도 경로**가 있다.

## Evidence

### ★ 측정을 시도한 둘 — 둘 다 불완전하다

| 논문 | 무엇을 했나 | 왜 불완전한가 |
|---|---|---|
| **Cronk 2026** | **`LPSCl`-only 대조셀**로 SE 몫을 분리 — 이 위키 최초 | 우리와 같은 30:50:20 이라 가장 가깝다. ⚠ 그래도 **탄소 유무를 가르지 않았다**(S4) |
| **Wang (XinXu) 2026** | `[인쇄]` LPSCl 의 용량 기여를 같은 전압창·전류에서 평가해 "무시할 만하다" | ⚠ **수치를 인쇄하지 않았다** · **LPSCl 단독인지 탄소+LPSCl 인지 구별 안 된다** · ★★ **대조 전압창 3.0 V 가 자기 활성화 컷오프 3.7–3.8 V 를 덮지 못한다** — 그 셀 첫 충전이 천장을 `[재현]` 107.4 % 넘는데도 **활성화 구간에서 SE 가 무엇을 했는지는 미측정**이다 |

→ **그래서 우리 0단계는 반드시 활성화 컷오프까지 올려서, 그리고 하한까지 내려서 돌린다.**

### ★★ 외부 눈금이 세 개이고 서로 맞지 않는다

| 출처 | 값 | 단위·방법 |
|---|---|---|
| **Wang (Daiwei) 2025** | `[재현]` **4–6 %** | 복합양극 용량 대비 비율 |
| **Gao 2024** | `[재현]` **28–52 mAh g⁻¹(composite)** | ICE 85.22 % 역산 (= 98–181 mAh g⁻¹(Li2S)) |
| **Lee (Jieun) 2025** | `[재현]` **0.8–1.5 mAh cm⁻²** | 아래 ★ 설계로 분리 |
| Kim JT 2023 에서 요구되는 값 | `[재현]` **237.9 mAh g⁻¹(composite)** = 594.8 mAh g⁻¹(LGPS) | 250사이클 초과분을 전부 SE 로 돌리면 |

★ **마지막 줄이 이 질문의 날카로운 지점이다.** Kim JT 의 간판 셀 초과분을 SE 로 설명하려면
Gao 눈금의 **4.6–8.5 배**가 필요하다. 그것이 비현실적이라는 것이 **"그 셀은 사실 2전자 전환을
거의 완결했다"** 는 우리 판정의 근거였다 ([[capacity-normalization-li2s-vs-sulfur]]).
→ **눈금이 정해지면 그 판정이 확정되거나 뒤집힌다.**

### ★★★ Lee (Jieun) 2025 가 새 분리 설계를 준다 — 활물질을 바꾸고 **면적용량**으로 본다

같은 SE·탄소·로딩에서 활물질만 **S8 / SeS2 / Se / Te** 넷으로 바꿨다. **이론용량이
420 ~ 1124 mAh g⁻¹ 로 2.7배 다른데** 초과분을 `mAh cm⁻²` 로 환산하면:

| 활물질 | 이론 면적용량 (4 mg cm⁻²) | 관측 최고 `[도표]` | **초과분** |
|---|---|---|---|
| S | 6.688 | ≈7.85 | **+1.16** |
| SeS2 | 4.495 | ≈5.3 | **+0.81** |
| Se | 2.715 | ≈3.75 | **+1.04** |
| **Te** | **1.680** | ≈3.15 | **+1.47** |

★★ **≈0.8–1.5 mAh cm⁻² 로 모인다** → **초과 용량이 활물질에 비례하지 않고 모든 셀 공통인
것(SE, 어쩌면 탄소)에서 온다.** **Te 셀은 용량의 `[재현]` ≈44 %가 활물질 밖**이다.
⚠ 단 그 논문은 **조성비를 적지 않았다** — SE 로딩 동일 가정 위의 계산이다.

### S4 의 근거 — 탄소가 분해를 가속한다

`leej2025` 가 인용하는 ref 39(Ohno/Zeier)가 **"탄소가 황화물 SE 분해를 가속한다"** 이고,
그 논문의 **"활물질 없는" 대조도 `LPSCl + 탄소`** 였다(LPSCl 단독 대조는 없다).
→ **우리 대조셀을 `LPSCl` 단독과 `LPSCl + AB` 둘로 나눠야 할 근거**다.

### S5 의 근거 — 초과 경로가 둘이다

**Feng 2026** 의 **풀셀 첫 사이클이 2전자 천장의 116 %** 이고 ★ **풀셀이 반쪽셀(868)보다 크다.**
그 셀은 음극을 **Li 박으로 프리리튬화**했으므로 `[해석]` **그 Li 재고가 양극으로 넘어온 것**이
유력하다(저자 무언급). → **SE 리독스가 아닌 별도 경로**이고, **0단계가 SE 몫만 분리해도
초과가 다 설명되지 않을 수 있다.**

관련 서명: **CE > 100 %** 가 그 경로의 지표다 — Yu 2024 **110–113 %** · Feng 2026 의 pristine
대조셀 `[도표]` **108 · 112 · 117 %, 1.5 C 구간엔 축 상단 120 % 를 넘어 잘린다** ·
Kim JT 2023 의 60 °C 셀 `[재현]` **≈112 %** · Park 2026 은 **첫 방전이 첫 충전의 1.5–1.6배**.

### Evidence Against — 몫이 작을 수도 있다

- **Hao 2025 가 첨가제 기여를 실제로 배제했다** (Fe K-edge XAS 4상태 불변, `[재현]` 상한 4.6 %).
  **방법이 있고 작동한다**는 증거다 — SE 쪽에도 같은 분광을 쓸 수 있다(P·S 의 산화상태 추적).
- **Wang XinXu 2026** 이 "무시할 만하다" 고 보고한다(수치 없음).
- **이론 초과가 없는 digest 도 16편이다.** 초과가 보편 현상은 아니고 **조건 의존**이다.

## 답하는 방법 (설계)

**1. 대조셀 넷을 돌린다 — 활물질 없음.** `LPSCl` 단독 / **`LPSCl + AB (80:20)`** / (첨가제를
검토한다면) `LPSCl + AB + LiI`. ★ **우리 운전 전압창 전체**(활성화 컷오프까지 올리고 하한까지
내려서)에서, 그리고 **10 사이클 이상** 돌려 S1 vs S2 를 가른다.
→ 판정: `LPSCl + AB` 가 `LPSCl` 단독보다 크면 **S4**. 2사이클 이후 기여가 0 으로 가면 **S1**,
계속 나오면 **S2**.

**2. 전압창을 좁혀 본다 (S3).** 1 의 대조셀에서 상한·하한을 각각 좁혀 몫이 줄어드는지 본다.
비용이 거의 0 이다 — 같은 셀로 전압창만 바꾼다.

**3. ★ 교차검증 — 활물질만 바꾼다 (Lee J 2025 설계).** 같은 SE·탄소·로딩에서 활물질을
**Li2S ↔ S8** 로 바꿔 두 셀을 돌리고, **초과분을 `mAh cm⁻²` 로 환산해 같게 나오는지** 본다.
같으면 그 값이 SE 몫이고, 다르면 **활물질–SE 상호작용**이 있다는 뜻이다.
→ 1 이 직접 측정, 3 이 독립 교차검증이다. **둘이 맞으면 분모가 확정된다.**

**4. 분광으로 보강 (비용 거의 0, 0단계와 같은 시료).** ⚠ **우리 양극은 `[재현]` 총 황의
58.8 %가 LPSCl 에서 온다** — S 2p XPS·S K-edge XANES 를 찍으면 **신호의 과반이 활물질이
아니다.** 1 의 `LPSCl + AB` 시료를 **같은 조건·같은 날**에 함께 찍어 배경으로 쓴다.
P 2p 의 산화상태 변화가 분해의 직접 지표다.

**5. CE 를 S5 의 지표로 읽는다 (비용 0).** **CE > 100 %** 가 나오면 그만큼을 **음극 재고
손실**로 가정하고 적는다 — SE 몫과 섞지 않는다.

## Status Log

- [2026-10-02] open — 카드 개설. 근거는 digest 24편(그중 이론 초과 8편 · SE 기여 정면 인정 4편 ·
  측정 시도 2편). 이 질문은 지금까지 [[reference-cell-500-600-mahg]] 의 **H4 안에 들어 있었는데**,
  (i) 참조 빈도가 가장 높고 (ii) 결정 실험이 H1·H2 와 다르고 (iii) 외부 눈금이 세 개로 흩어져
  **자기 Evidence 축적이 필요해서** 분리했다. H4 는 "단위 착시" 쪽에 남는다.
  현재 판정: **몫의 크기를 문헌에서 빌릴 수 없다.** 4–6 % 와 1.5 mAh cm⁻² 사이가 너무 넓고,
  Kim JT 의 초과를 설명하려면 Gao 눈금의 4.6–8.5 배가 필요하다. **우리가 재야 한다.**
  다음 행동은 **대조셀 넷 + 전압창 좁히기** 이고 [[reference-cell-experiment-plan]] 0단계에 있다.

## 관련
- [[reference-cell-500-600-mahg]]
- [[capacity-normalization-li2s-vs-sulfur]]
- [[reference-cell-experiment-plan]]
- [[additive-classification-and-mass-penalty]]
- [[interface-quality-not-bulk-conductivity]]
