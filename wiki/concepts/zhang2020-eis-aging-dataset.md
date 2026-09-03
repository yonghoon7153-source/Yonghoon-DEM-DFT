---
title: 우리가 쓰는 EIS 노화 데이터셋의 정체 (Zhang 2020, Zenodo 3633835)
description: "LiCoO2/graphite 45 mAh Eunicell LR2032 코인셀 12개 · 3온도 · 사이클 안 9시점 EIS(그중 4개는 DC 전류 중). Su 2024 SI 로 입수했으나 원 출처는 Zhang et al. Nat. Commun. 11:1706 (2020) 이며, state I~IX 는 열화 단계가 아니라 한 충방전 사이클 안의 측정 시점이다"
created: 2026-09-03
updated: 2026-09-03
type: concept
tags: [battery, degradation, research]
sources: [raw/papers/zhang2020_eis-gpr-capacity-rul.md, raw/papers/su2024_drt-soh-health-features.md]
confidence: high
explored: false
verificationStatus: verified
verifiedAt: 2026-09-03
verifiedBy: agent
claimType: empirical
evidenceScope: multi-source-primary
---

# 우리가 쓰는 EIS 노화 데이터셋의 정체 (Zhang 2020, Zenodo 3633835)

## 정의

satellite [[mode-observability]] 의 Phase 2(SEV 실측 대조)가 쓰는 EIS 데이터의
**원 출처와 좌표계**. 우리는 이것을 Su 2024 의 SI zip 으로 입수했지만
(`mode-observability/data/su2024/EIS data/`, 176파일 90 MB), **Su 는 이 데이터를
재는 사람이 아니라 재사용한 사람**이다.

**원 출처** (Su 2024 §2.1 + Data availability + 참조 [32] 로 확정 —
근거는 raw digest `raw/papers/su2024_drt-soh-health-features.md` §2.1):

> Y. Zhang, Q. Tang, Y. Zhang, J. Wang, U. Stimming, A. A. Lee,
> *Identifying degradation patterns of lithium ion batteries from impedance
> spectroscopy using machine learning*, **Nature Communications 11:1706 (2020)**,
> DOI **10.1038/s41467-020-15235-7**. (논문번호 1706 은 원전에서 확인)
> 데이터: **Zenodo DOI 10.5281/zenodo.3633835**.

Su 2024 의 Data availability 전문: "We used an **open dataset** at
doi:https://doi.org/10.5281/zenodo.3633835, reference number [32]."

**2026-09-03: 원전을 본문 + SI 로 직접 흡수했다** (digest:
`raw/papers/zhang2020_eis-gpr-capacity-rul.md`, 크롭 그림 8장:
`raw/figures/zhang2020_eis-gpr-capacity-rul/`). 아래 좌표계는 이제 **Su 의
전언이 아니라 원전 인쇄**가 근거다.

## 좌표계 (★ Zhang 2020 Methods + SI Fig. 1 이 인쇄한 것)

| 축 | 값 | 근거 |
|---|---|---|
| 화학 | **LiCoO₂ / graphite** | Zhang Methods `[인쇄]` |
| 셀 형태 | **코인셀 — Eunicell LR2032** (20 mm × 3.2 mm) | Zhang Methods `[인쇄]` (Su 에는 없던 것) |
| 공칭 용량 | **45 mAh** (→ 1C = 45 mA). 단 **실측 초기용량은 34–42 mAh** | Methods `[인쇄]` · SI Fig. 4 `[도표]` |
| 셀 | **12개**: 25 °C **8개**(25C01–08) · 35 °C **2개**(35C01–02) · 45 °C **2개**(45C01–02) | Methods `[인쇄]` + SI Fig. 4 범례 `[도표]` — 명부가 exhaustive 하다 |
| 사이클 | **1C(45 mA) CC–CV 충전 4.2 V** / **2C(90 mA) CC 방전 3.0 V** | Methods `[인쇄]` |
| 선행 이력 | 전 셀 **25 °C 30사이클** 후 온도 분기. EoL = 그 이후 초기값의 **80 %** | Methods `[인쇄]` |
| 측정 주기 | EIS = **짝수** 사이클 · 용량 = **홀수** 사이클 | Methods `[인쇄]` |
| `state I~IX` | **한 충방전 사이클 안의 아홉 측정 시점** (아래 표에 아홉 개 전부) | SI Fig. 1 `[인쇄]`+`[도표]` |
| 열화 축 | 파일 안의 **`cycle number` 열** | state 축과 직교한다 |
| EIS | 정현파 **전류 5 mA** (≈ C/9) · **60 주파수** · **0.02 Hz – 20 kHz** | Methods `[인쇄]`. 우리 실측(4,920행 = 60 × 82 스펙트럼)과 일치 |
| 포맷 | BioLogic EC-Lab (`time/s · cycle number · freq/Hz · Re(Z) · -Im(Z) · |Z| · Phase(Z)`) | 원전도 파일 포맷을 다루지 않는다 |

### ★ state I~IX 아홉 개 전부 (SI Fig. 1)

캡션 `[인쇄]`: "I: Before charging; II: Start charging; III: After 20 minutes
charging; IV: After charging and before resting; V: After 15 minutes rest;
VI: Start discharging; VII: After 10 minutes discharging; VIII: After
discharging and before resting; IX: After 15 minutes rest. The red (green) dots
correspond to **with (without) DC current**."

| state | 시점 | DC 전류 `[도표]` | SOC `[해석] 어림` |
|---|---|---|---|
| I | 충전 전 (3.0 V) | 없음 | 0 % |
| II | 충전 시작 | **있음** | ≈ 0 % |
| III | 충전 20분 후 (CC 중턱) | **있음** | ≈ 40 % |
| IV | 충전 종료·휴지 전 (4.2 V) | 없음 | 100 % |
| V | 15분 휴지 후 (4.2 V) | 없음 | 100 % |
| VI | 방전 시작 | **있음** | ≈ 100 % |
| VII | 방전 10분 후 | **있음** | ≈ 57 % |
| VIII | 방전 종료·휴지 전 (3.0 V) | 없음 | 0 % |
| IX | 15분 휴지 후 (3.0 V) | 없음 | 0 % |

**이것이 Phase 2 설계를 바꾼다** (아래 "왜 중요한가" 2번).

## 왜 중요한가

**1. 인용의 정본이 바뀐다.** 이 데이터로 낸 어떤 수치도 1차 출처는
**Zhang 2020 / Zenodo 3633835** 이고, Su 2024 는 "이 데이터로 무엇을 했는가" 의
**선행연구**로 인용한다. `mode-observability/manifests/README.md` 에 걸려 있던
"출처 확정 전에는 'Su 2024 SI' 로만 적는다" 는 유보는 이것으로 해제됐다.

**2. `state` 축을 오해하면 Phase 2 설계가 통째로 틀린다.** `state I~IX` 를
열화 단계로 읽으면 한 파일 안의 82개 스펙트럼이 무엇인지 설명되지 않는다.
정답은 **state = SOC/시점, cycle = 열화**다. 따라서 두 종류의 스윕이 가능하다:

- (a) **state 고정 → cycle 스윕** = 노화 추적. Su 2024 가 한 것 (state V 만).
- (b) **cycle 고정 → state I~IX 스윕** = SOC/완화 의존성 추적.

**★ 2026-09-03 원전 확인으로 (b) 의 서술을 두 군데 정정한다.**

- ~~"아무도 안 했다"~~ → **틀린 서술이었다.** Zhang 2020 은 state 축을 썼다 —
  다만 **복제 축**으로만 썼다. SI Fig. 2 (직접 봄)는 **state 마다 독립적인
  EIS→용량 GPR 을 아홉 개** 만들어 각각의 R² 를 보고한다. 여전히 아무도 하지
  않은 것은 **state 간 대비를 feature 로 쓰는 것**(한 사이클 안 아홉 스펙트럼을
  나란히 놓는 것)이다. 그쪽은 미개척이 맞다.
- **원전의 per-state R² 는 우리에게 공짜 사전정보다** `[도표]` (SI Fig. 2 +
  본문 Fig. 1a): V **0.88** · VII 0.86 · IX 0.81 · VIII 0.68 · II 0.66 ·
  I 0.61 · IV 0.60 · III 0.53 · **VI 0.28**. 본문은 이를 "similarly positive"
  라고 쓰지만 그림은 그렇지 않다. **state VI 는 쓰지 않는다.**
- **SOC 축의 실제 해상도는 2점이다.** 위 state 표에서 보듯 **전류 없이 잰
  SOC 는 0 %(I·VIII·IX)와 100 %(IV·V) 두 점뿐**이고, 중간 SOC(III ≈40 %,
  VII ≈57 %)는 **DC 전류가 흐르는 중**에 측정된다 — 평형 임피던스가 아니다.
  `[해석]` SEV 는 R_ct 의 **stoichiometry(= SOC) 의존성**을 읽는 feature 이므로
  ([[pvs-sev-degradation-mode-features]]), 이 데이터로 얻을 수 있는 것은
  **SOC 곡선이 아니라 양 끝점 2점 대비**다. Phase 2 는 이 제약을 안고 설계한다.
- **대신 아무도 안 쓴 축이 하나 더 있다**: `IV vs V` 와 `VIII vs IX` 는
  **같은 SOC 에서 휴지 15분 전/후** 쌍이다. SOC 가 아니라 **완화 시간**만 다른
  대비이며, Zhang 은 이 둘을 각각 독립 모델로만 다뤘다.

**3. Su 가 쓴 것은 데이터셋의 일부뿐이다.** 12셀 중 **5셀**(25C01/02/03/05/06),
3온도 중 **25 °C 하나**, 9 state 중 **state V 하나**. 25C04·25C07·25C08 과
35 °C·45 °C 전부, 그리고 state 축 전체가 미사용이다.

**4. `[해석]` 이 데이터셋의 셀 간 편차는 극단적이다 — Phase 2 의 난이도 설정.**
원전의 공개 코드 `RUL.txt` 를 셀 구간으로 자르면 훈련 셀 EoL 이
**12 / 162 / 218 / 234 / 414 사이클**이고, 시험 셀은 Fig. 2 캡션 `[인쇄]` 로
**150 / 120 / 30 / 38**. 즉 **동일 사양·동일 프로토콜의 25 °C 코인셀 8개에서
EoL 이 12~234 사이클, 약 20배로 흩어진다.** 게다가 `[도표]` SI Fig. 4 는
**고온 셀이 더 오래 살고 초기용량도 더 높다**는 것을 보여 준다 (45 °C ≈
40.5–42 mAh vs 25 °C ≈ 34–36 mAh) — Arrhenius 상식과 반대이며 원문은 언급하지
않는다. 온도군이 **배치와 교락**돼 있을 가능성이 크다. → "셀 간에 재현되는가"
를 묻기에는 가혹하지만 **정직한** 무대다.

## 미확인 항목 (Zhang 2020 원문에서 닫아야 할 것)

> **[2026-09-03] 원전(Zhang 2020 본문 + SI)을 직접 흡수해 아래 6개를 판정했다.**
> 항목을 지우지 않고 **닫힘 표시 + 근거**를 단다 (무엇이 언제 어떻게 닫혔는지가
> 기록이다). 근거의 정본은 `raw/papers/zhang2020_eis-gpr-capacity-rul.md` §1.

| # | 항목 | 판정 |
|---|---|---|
| 1 | 셀 형태 | **닫힘** — 코인셀 `Eunicell LR2032` |
| 2 | 셀 목록 | **닫힘** — 12셀, Su 의 열거가 맞다 |
| 3 | 파일 수 176 | **원문 미제시** (정본 개수 120 은 유도됨) |
| 4 | `25C42` 파일 | **부분 닫힘** — 셀 42 는 존재하지 않는다 → 격리 |
| 5 | 사이클링 프로토콜 | **닫힘** — 1C CC–CV 4.2 V / 2C CC 3.0 V |
| 6 | `state I~IX` 정의 | **닫힘 (아홉 개 전부)** + DC 전류 유무까지 |

1. ~~**셀 형태.**~~ → **닫힘.** Methods `[인쇄]`: "12 commercially available
   45 mAh **Eunicell LR2032** Li-ion **coin cells**. The cell chemistry is
   LiCoO₂/graphite." 우리 추정("LIR2032 급 코인셀")은 규격까지 맞았고, 상표만
   LIR 이 아니라 **Eunicell LR2032** 였다.
2. ~~**셀 목록.**~~ → **닫힘. Su 의 열거가 맞다.** Methods `[인쇄]`: "cycled in
   three climate chambers set to **25 °C (25C01–25C08)**, **35 °C (35C01 and
   35C02)** and **45 °C (45C01 and 45C02)**". `[도표]` SI Fig. 4 범례가 12개를
   train/test 표시와 함께 하나도 빠짐없이 그린다. → **"온도별 01–08" 가설
   폐기.**
3. **파일 수 176.** → **원문 미제시.** 논문은 Zenodo 저장소의 파일 이름·개수·
   포맷을 한 글자도 적지 않는다 (Data availability 는 DOI 한 줄). 다만 측정
   설계는 완전히 인쇄돼 있어 **정본 파일 수 = 9 state × 12 cell = 108 EIS +
   12 capacity = 120** 이 유도되고, "한 파일 = 한 (셀, state), 여러 사이클"
   구조도 확정된다 (짝수 사이클마다 측정 `[인쇄]` + 우리 실측 82 스펙트럼 +
   공개 코드의 299행 파일). → **56파일이 설계 밖에 있다.** 확인 경로는 Zenodo
   뿐인데 **2026-09-03 세션에서 egress proxy 가 `zenodo.org`·`doi.org` 를 403
   으로 차단**해 접근하지 못했다. 미해결.
   `[해석]` 저자들의 다른 공개 zip(GitHub `Code-Matlab.zip`)은 `__MACOSX/`
   그림자 항목을 포함해 압축돼 있다(직접 확인). 그림자 가설은 산술이 맞지
   않아(120+120=240 ≠ 176) **단독으로는 설명하지 못한다.**
4. **`EIS_state_VI_25C42.txt`** → **부분 닫힘.** **셀 42 는 이 연구에 존재하지
   않는다** — 셀 명부가 Methods `[인쇄]` 와 SI Fig. 4 범례 `[도표]` 두 곳에서
   exhaustive 하게 확정된다. 파일의 정체(오기? 중복? 업로드 잔여물?)는 원문으로
   알 수 없다. **조치: 13번째 셀로 취급하지 않는다.** Phase 2 매니페스트에서
   격리하고 이 파일의 스펙트럼은 결과에 넣지 않는다.
5. ~~**사이클링 프로토콜.**~~ → **닫힘.** Methods `[인쇄]`: "**1C-rate (45 mA)
   CC–CV charge up to 4.2 V** and a **2C-rate (90 mA) CC discharge down to
   3 V**", EIS 는 **짝수** 사이클·용량은 **홀수** 사이클, SoC 0 %/100 % 에서
   각 15분 개방회로, 전 셀 **25 °C 30사이클** 선행, EoL = 그 후 초기값의 80 %.
   `[해석]` 두 파생 주의: (a) 용량 라벨과 스펙트럼은 **같은 사이클이 아니라
   ±1 사이클** 짝이다(짝짓기 규칙은 원문에 없다), (b) 방전이 **2C 뿐**이므로
   용량 라벨이 그 2C 방전용량이면 **라벨에 동역학이 섞인다**(원문 미제시).
6. ~~**`state I~IX` 의 정확한 정의 / 헤더 유무.**~~ → **정의는 닫힘 (아홉 개
   전부, 위 표).** SI Fig. 1 캡션이 아홉 시점을 모두 인쇄하고, 그림의 적·녹
   점이 **DC 전류 유무**까지 준다 — **II·III·VI·VII 은 전류가 흐르는 중에
   측정된다.** 이것은 우리가 기대하지 않았던 정보이며 Phase 2 설계를 바꾼다.
   (파일 **헤더 유무**가 섞인 이유는 여전히 **원문 미제시** — 원전도 파일
   포맷을 다루지 않는다. 항목 3과 같은 계열이며 Zenodo 로만 닫힌다.)

## 원전이 이 데이터로 한 것 (= 우리가 다시 하지 않아도 되는 것)

Zhang 2020 자신의 작업은 **EIS 스펙트럼 120차원(60주파수 × 실·허) → GPR →
용량 / RUL** 이다. 상세는 raw digest, 요약만:

- 라벨은 **용량(측정)** 과 **RUL(= EoL − cycle, 파생)** 둘뿐. **모드 라벨 없음.**
- 분할은 **셀 단위** (25C01–04 훈련 / 25C05–08 시험; 다온도는 +35C01·45C01).
- ARD 가 고른 것은 `[인쇄]` **17.80 Hz 와 2.16 Hz** — SI Fig. 3(b) 로
  **허수부**임이 확정된다 (예측자 91·100 = Im Z(ω₃₁)·Im Z(ω₄₀)).
- `[해석]` **그 선택은 유일하지 않다.** 저자들의 공개 데이터
  (`EIS_data_35.txt`)로 직접 계산하면 120개 예측자 중 **52개**가 단독으로
  |r(용량)| > 0.95 이고, 91번의 이웃 92번과의 상관이 **0.998** 이다. ARD 가
  집어낸 것은 주파수 하나가 아니라 **공선 대역 하나**이며, 그 안에서 어느
  점이 뽑히는지는 데이터가 정하지 않는다 → [[fitting-degeneracy]] 의 EIS 판
  사례. 원전은 이 가능성을 검토하지 않고 17.80 Hz 에 물리적 의미를 부여한다.

## 이 위키에서의 적용

- [[mode-observability]] Phase 2 의 데이터 층 정본. 매니페스트 문서는
  `mode-observability/manifests/README.md` (living reference, 내용 복사 금지).
- [[pvs-sev-lli-lampe-separability]] 의 SEV 축을 **실측으로** 건드리는 유일한
  통로. 다만 이 데이터셋에는 **LLI/LAM 라벨이 없다** — **[2026-09-03 원전에서
  확정됨]**: `LLI`·`LAM`·`lithium inventory`·`half-cell` 이 Zhang 본문·SI 에
  **각 0회**이고, 모드를 재는 절차(half-cell OCP fitting · ICA/DVA · 해체분석 ·
  모드 시뮬레이션)가 하나도 없으며, Introduction 이 미시 기구 모델링을 명시적으로
  포기한다. 제목의 "degradation **patterns**" 는 **셀마다 다른 감쇠 궤적**을
  뜻한다 (본문 용례 2회 = 제목 + Discussion). 즉 이 데이터로는 "SEV 가 모드를
  가르는가" 를 직접 물을 수 없고, **"SEV 축 자체가 셀 간에 재현되는가"** 만
  물을 수 있다. 그 구분을 흐리지 않는다.
- **Phase 2 의 첫 실험이 구체화된다** `[해석]`: 동일 조건 **8셀**(25C01–08,
  Su 가 쓴 5셀보다 많다)에 대해 **state V(100 %) 와 state IX(0 %)** 의 저주파
  임피던스 대비를 노화축으로 추적하고, Su 2024 Fig. 7 에서 우리가 발견한
  **부호 뒤집힘**이 8셀에서도 나오는지 본다. 이번에는 **DRT 를 거치지 않고**
  원 스펙트럼에서 직접 잴 수 있어 λ 재현 문제를 우회한다.
- Su 2024 의 결과를 **재현 baseline** 으로 쓸 수 있다 (같은 5셀·같은 state).
  단 DRT 설정이 "DRTtools, λ=1E-3, 나머지 default" 로만 인쇄돼 완전 재현은
  어렵다 — Su raw digest §2.3 참조.

## confidence: high 로 올린 근거와 반대해석

`[근거]` 좌표계의 모든 행이 **원전 인쇄**(Methods · SI Fig. 1 캡션)로 확인됐고,
셀 명부는 그림(SI Fig. 4)으로 **독립 교차확인**됐다.
`[반대해석 / 데이터 공백 1줄]` **파일 인벤토리(항목 3·4·헤더)는 여전히 열려
있다** — 우리가 디스크에서 본 176파일이 Zenodo 원본과 같은 집합인지 확인되지
않았고, 그 확인 경로는 이번 세션에 차단됐다. 즉 **"데이터셋의 설계" 는 high,
"우리 손의 바이트가 그 설계와 일치하는가" 는 아직 medium** 이다.

## 관련
- [[mode-observability]] — 이 데이터를 쓰는 satellite
- [[pvs-sev-lli-lampe-separability]] — 이 데이터가 답할 수 있는 질문과 없는 질문
- [[pvs-sev-degradation-mode-features]] — SEV 의 정의와 SOC 의존성 축
- [[fitting-degeneracy]] — ARD 가 고른 "두 주파수" 가 공선 대역 안에서
  비식별적이라는 것이 이 개념의 EIS 판 사례다
- [[interpretable-ml-battery-prognosis-taxonomy]] — Su 2024 가 이 데이터로 한
  작업이 앉는 분류 자리 (§4.4 EIS 유래 physics-inspired feature)
