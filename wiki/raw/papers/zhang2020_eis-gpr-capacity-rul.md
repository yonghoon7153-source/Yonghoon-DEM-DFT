---
title: "Zhang et al. 2020 — EIS + GPR 로 용량·RUL 예측 (Nat. Commun. 11:1706); 우리 EIS 데이터셋의 원전"
source_url: local-upload/9IDENT1.PDF + 9SUPI1.PDF (Nature Communications 11:1706, DOI 10.1038/s41467-020-15235-7)
ingested: 2026-09-03
sha256: 1ee6654c62a742d3b251324188f586d4abddf2c52245d6d0a84c1dbbb4403b35
---

# 수집 목적

Yunwei Zhang¹²⁶, Qiaochu Tang²³⁴⁶, Yao Zhang⁵, Jiabin Wang²³⁴,
Ulrich Stimming²³⁴⁷, Alpha A. Lee¹²⁷,
**"Identifying degradation patterns of lithium ion batteries from impedance
spectroscopy using machine learning"**,
*Nature Communications* **11**:1706 (2020),
DOI **10.1038/s41467-020-15235-7** — 본문 6쪽 + SI 6쪽 전문의 절별 해체분석.

소속: ¹Cavendish Laboratory, University of Cambridge · ²The Faraday Institution
(Harwell) · ³Chemistry, School of Natural and Environmental Sciences, Newcastle
University · ⁴North East Centre of Energy Materials (NECEM), Newcastle ·
⁵DAMTP, University of Cambridge. ⁶ 공동 1저자 (YW.Z., Q.T.) · ⁷ 공동 교신
(U.S., A.A.L.). Received 2019-08-05 / Accepted 2020-02-17. CC BY 4.0 (OPEN).
자금: EPSRC EP/S003053/1.

이 논문은 **우리가 이미 쓰고 있는 데이터의 원전**이라 다른 흡수와 성격이
다르다. 흡수 동기는 셋이다.

**① 위키의 "미확인 항목" 6개를 닫는 것.**
`wiki/concepts/zhang2020-eis-aging-dataset.md` 와
`mode-observability/manifests/README.md` 에는 Su 2024 원문으로 닫히지 않아
열어 둔 항목이 6개 있다 (셀 형태 · 셀 목록 · 파일 수 176 · `25C42` 파일 ·
사이클링 프로토콜 · `state I~IX` 의 정확한 정의). 이 논문이 그 데이터를
**생산한** 논문이므로 여기서 닫히거나, 여기서도 안 닫히면 "원문 미제시" 로
확정된다. **결과: 6개 중 4개 닫힘, 2개 원문 미제시** (§1 의 표).

**② 제목의 "identify degradation patterns" 이 우리 축에서 무엇인가.**
우리 프로젝트는 "그 identify 가 애초에 식별 가능한가" 를 묻는다. 라벨이
무엇인지, 사상의 유일성을 저자들이 묻는지, GPR 불확실성이 무엇의 불확실성인지를
확정한다.

**③ Phase 2 설계에 직접 쓸 수 있는 것.** 특히 우리가 "아무도 안 했다" 고 적어 둔
축 — **cycle 고정 → state I~IX 스윕** — 을 원전이 어떻게 다뤘는가.

**④ 공개 코드 저장소** (`github.com/YunweiZhang/ML-identify-battery-degradation`)
를 실제로 받아 무엇이 들어 있는지 확인.

## 서지 확인 (사용자 추정 대조)

사용자가 준 서지는 **전부 맞다**. 원문 인쇄로 확인한 것과 보탠 것:

| 항목 | 사용자 추정 | 원문 `[인쇄]` |
|---|---|---|
| 저자 | Zhang, Tang, Zhang, Wang, Stimming, Lee | 동일 (Y. Zhang 과 Q. Tang 이 **공동 1저자**, Stimming 과 Lee 가 **공동 교신**) |
| 저널·권 | Nature Communications 11 (2020) | 동일 — **논문번호 1706** (6쪽) |
| DOI | 10.1038/s41467-020-15235-7 | 동일 |
| 데이터 | Zenodo 10.5281/zenodo.3633835 | 동일 (Data availability 절) |
| 코드 | github.com/YunweiZhang/ML-identify-battery-degradation | 동일 (Code availability 절) |

원문에만 있는 서지 사실 하나를 덧붙인다 — `[인쇄]` Peer review information:
"Nature Communications thanks **Richard Braatz**, and the other anonymous
reviewer(s) for their contribution to the peer review of this work."
`[해석]` 이 계보에서 의미가 있다: Braatz 는 Severson 2019 (본문 참조 [18],
이 논문의 비교 기준선)와 Rhyu 2025 ([[fused-lasso-feature-design-framework]])의
공저자다. 즉 **우리가 지금까지 흡수한 계보에서 방법론적으로 가장 엄격한 팀이
이 논문의 심사자였다**. 그럼에도 아래 §5 의 어휘 전수 결과는 0회다.

## 표기 규약

이 digest 에서 네 종류를 구분한다.

- `[인쇄]` — 본문 또는 SI 에 **글자로** 있는 것. 인용은 원문 그대로.
- `[도표]` — 그림에서 **눈으로 읽은** 것. 수치는 `figure-read ≈` 로 표시하며
  원문 도표가 정본이다.
- `[코드]` — 저자들의 공개 GitHub 저장소 파일에 **있는** 것 (이번 세션에
  실제로 clone 해서 확인). 논문 본문에는 없다.
- `[해석]` — 우리 판단·계산. 원문이 말한 것이 아니다.

# 원문에 없어서 확인이 필요한 것 (먼저 적는다)

1. **Zenodo 저장소의 파일 구성.** 논문은 파일 이름·개수·포맷을 한 글자도
   적지 않는다. 우리 실측의 176파일과 `EIS_state_VI_25C42.txt` 는 **이 논문으로
   닫히지 않는다**. 확인 경로는 Zenodo 뿐인데, 이번 세션에서는 egress proxy 가
   `zenodo.org` 와 `doi.org` 를 모두 403 으로 막아 접근하지 못했다
   (`curl: (56) CONNECT tunnel failed, response 403`).
2. **EIS 장비·셀 홀더·4단자 여부.** 임피던스 절대값 재현에 필요한데 원문에
   없다 (여기 없으면 `R_∞` 의 셀 간 차이가 셀의 것인지 접촉의 것인지 못 가른다).
3. **주파수 격자의 정의.** "60 frequencies in the range of 0.02 Hz–20 kHz"
   `[인쇄]` 만 있고 로그 등간격인지, 오름/내림인지, 지점당 적분 시간·반복 수가
   없다. 우리가 §4 에서 공개 데이터로 **역산**했지만 그것은 `[해석]` 이다.
4. **셀의 이력.** "All cells underwent 30 cycles at room temperature of 25 °C
   before different temperatures were set" `[인쇄]` — 이 30 사이클의 프로토콜이
   본 사이클과 같은지(1C CC-CV / 2C CC), 그동안 EIS 를 쟀는지 없다.
5. **capacity 측정 방법.** "The loss in capacity is determined after every
   odd-numbered cycle" `[인쇄]` 뿐 — 어느 전류로 잰 방전용량인지(2C 방전
   그대로인지 별도 저율 RPT 인지) 없다. 2C 방전용량이면 **동역학 성분이 라벨에
   섞여 있다**.
6. **초기용량 편차의 원인.** 공칭 45 mAh 인데 실측 초기용량은 34~42 mAh 이고
   (`[도표]` SI Fig. 4) 온도군마다 계통적으로 다르다. 배치 차이인지 형성
   차이인지 원문에 없다 (§6 의 confound 논의).
7. **SI Fig. 2 가 어느 셀인지.** 캡션은 `[인쇄]` "for **25C02** cell" 인데
   25C02 는 **훈련 셀**이다. 본문은 Fig. 1a 를 25C05 로 적고 "results at other
   states … shown in Supplementary Fig. 2" 라고 잇는다. 둘 중 하나가 오기다.
8. **비교 기준선(방전곡선 feature)의 구체.** `[인쇄]` "following recent
   work18" 한 줄뿐 — feature 목록도 전처리도 없다. SI Table 1 은 재현 불가능하다.

---

# 1. ★ 위키의 미확인 항목 6개 — 닫기

이 절이 이번 흡수의 최우선 과제다. 결론 표를 먼저 놓고, 근거를 아래에 편다.

| # | 항목 | 판정 | 근거 |
|---|---|---|---|
| 1 | **셀 형태** | **닫힘** — 코인셀. `Eunicell LR2032` | Methods `[인쇄]` |
| 2 | **셀 목록** | **닫힘** — 12셀 = 25 °C 8 + 35 °C 2 + 45 °C 2. Su 의 열거가 맞다 | Methods `[인쇄]` + SI Fig. 4 범례 `[도표]` (12개 전부 이름과 함께) |
| 3 | **파일 수 176** | **원문 미제시** — 논문은 파일 구성을 기술하지 않는다. 다만 설계상 정본 파일 수는 **108 EIS + 12 capacity = 120** 임이 확정된다 | Methods `[인쇄]` + `[해석]` |
| 4 | **`EIS_state_VI_25C42.txt`** | **부분 닫힘** — 셀 42 는 **이 연구에 존재하지 않는다**. 셀 명부가 exhaustive 임이 두 곳에서 확정되므로, 이 파일은 데이터가 아니라 **격리 대상**이다 | Methods `[인쇄]` + SI Fig. 4 `[도표]` |
| 5 | **사이클링 프로토콜** | **닫힘** — 1C(45 mA) CC–CV 충전 4.2 V / 2C(90 mA) CC 방전 3 V, 전 셀 25 °C 30사이클 선행 | Methods `[인쇄]` |
| 6 | **`state I~IX` 의 정확한 정의** | **닫힘 (아홉 개 전부)** — 게다가 **넷은 DC 전류가 흐르는 중에 측정**된다는 결정적 사실이 추가된다 | SI Fig. 1 캡션 `[인쇄]` + 그림 `[도표]` |

## 1.1 셀 형태 — 닫힘

Methods, Data generation 첫 문장 `[인쇄]`:

> "The experiment is carried out by applying a continuous charge–discharge
> cycle on **12 commercially available 45 mAh Eunicell LR2032 Li-ion coin
> cells**. The cell chemistry is LiCoO₂/graphite."

우리 추정("45 mAh 규모와 명명으로 보아 LIR2032 급") 은 **규격까지 맞았다** —
단 상표는 LIR 이 아니라 **Eunicell LR2032** 다. 2032 = 지름 20 mm × 두께
3.2 mm 코인셀.

`[해석]` 이것은 데이터 해석에 무겁다. 코인셀은 (a) 전극 면적이 작아 접촉저항의
상대 기여가 크고, (b) 셀 간 제작 편차가 파우치/원통보다 크며, (c) 참조전극이
없다. §6 에서 보는 셀 간 EoL 20배 편차와 임피던스 오프셋은 이 형태와 무관하지
않다.

## 1.2 셀 목록 — 닫힘 (Su 의 열거가 맞다)

Methods `[인쇄]`:

> "The cells are cycled in three climate chambers set to **25 °C
> (25C01–25C08)**, **35 °C (35C01 and 35C02)** and **45 °C (45C01 and 45C02)**,
> respectively."

`[도표]` SI Fig. 4 (직접 봄) 의 범례가 **12개를 하나도 빠짐없이** 열거하며
train/test 를 함께 표시한다: `25C01-train, 25C02-train, 25C03-train,
25C04-train, 25C05-test, 25C06-test, 25C07-test, 25C08-test, 35C01-train,
35C02-test, 45C01-train, 45C02-test`.

→ **"온도별 01–08" 가설은 폐기된다.** 25 °C 만 8셀이고 35/45 °C 는 각 2셀이다.
우리 위키가 Su 로부터 옮겨 적은 좌표계가 원전과 일치한다.

## 1.3 파일 수 176 — 원문 미제시 (그러나 정본 개수는 확정된다)

논문은 Zenodo 저장소의 **파일 구성을 기술하지 않는다**. Data availability 절
전문이 `[인쇄]` "Experimental data generated during the study is available in a
public repository at https://doi.org/10.5281/zenodo.3633835." 한 문장이다.

다만 측정 설계는 완전히 인쇄돼 있으므로 **정본 파일 수를 유도할 수 있다**
`[해석]`:

- EIS: 9 state × 12 cell = **108** 계열. 한 계열은 그 셀의 짝수 사이클 전부를
  담는다 (아래 근거).
- capacity: 셀당 1 계열 = **12**.
- 합 **120**.

"한 파일 = 한 (셀, state), 여러 사이클" 이라는 구조는 원문 설계와 우리 실측이
맞물려 확정된다: Methods `[인쇄]` "EIS is measured at nine different stages of
charging/discharging **during every even-numbered cycle**" 이고, 우리 실측
파일 하나가 4,920행 = 60주파수 × **82 스펙트럼** 이었다 → 82 짝수 사이클 =
사이클 2~164. `[도표]` SI Fig. 4 에서 25C07·25C08 이 각각 ≈ 180·170 사이클에서
끝나므로 그 셀의 파일이 82 스펙트럼인 것과 정합한다. 공개 코드의
`EIS_data_35.txt` 가 **299행**인 것도 같은 구조다 (35 °C 셀이 598 사이클까지
돌았으므로 299 짝수 사이클) `[코드]`.

→ 176 − 120 = **56파일이 논문이 기술한 설계 밖에 있다.** 이 차이는 이 논문으로
닫히지 않는다. 확인 경로(Zenodo)는 이번 세션에 차단됐다.

`[해석]` 가설 하나만 근거와 함께 남긴다 (검증 전에는 쓰지 않는다): 저자들의
다른 공개 zip — GitHub 의 `Code-Matlab.zip` — 은 **`__MACOSX/` 그림자 항목을
포함해서 압축돼 있다** (이번 세션에 `unzip -l` 로 직접 확인:
`__MACOSX/Code-Matlab/._ARD_GPR.m` 등). 즉 이 저자들의 패키징 습관은 macOS
그림자 파일을 남긴다. 우리 스캐너(`mode-observability/tools/eis_ingest.py:203`)
는 `DATA.glob("*.txt")` 로 **같은 폴더의 모든 `.txt`** 를 세므로, 풀린
`._*.txt` 그림자 파일이 같은 폴더에 섞이면 그대로 계수된다. 다만 176 = 120 + 56
이 그림자 가설의 산술(120 + 120 = 240)과 맞지 않으므로 **이 가설만으로는
설명되지 않는다.** 미해결로 둔다.

## 1.4 `EIS_state_VI_25C42.txt` — 부분 닫힘 (셀 42 는 없다)

셀 42 는 **이 연구에 존재하지 않는다**. 셀 명부가 exhaustive 라는 것이 두 곳에서
독립적으로 확정되기 때문이다:

1. Methods `[인쇄]` 가 12셀을 **괄호 안에 이름까지** 열거한다 (§1.2 인용).
2. `[도표]` SI Fig. 4 의 범례가 12개를 전부 그린다 — 13번째 곡선은 없다.

→ **판정: `25C42` 는 이 연구의 셀이 아니다.** 파일명 오기(예: `25C04` 의 변형),
중복 사본, 또는 Zenodo 업로드 시의 잔여물일 수 있으나 어느 쪽인지는 원문으로
알 수 없다. **조치**: 이 파일을 13번째 셀로 취급하지 않는다. Phase 2 의
매니페스트에서 격리하고, 이 파일에서 나온 스펙트럼은 결과에 넣지 않는다.
(이 조치는 "정체를 모른다" 와 별개로 지금 확정할 수 있다 — 이것이 이 항목을
"부분 닫힘" 으로 두는 이유다.)

## 1.5 사이클링 프로토콜 — 닫힘

Methods `[인쇄]`, 세 문장을 그대로 옮긴다:

> "Each cycle consists of a **1C-rate (45 mA) CC–CV (constant current–constant
> voltage) charge up to 4.2 V** and a **2C-rate (90 mA) CC (constant current)
> discharge down to 3 V**."
>
> "EIS is measured at nine different stages of charging/discharging **during
> every even-numbered cycle** in the frequency range **0.02 Hz–20 kHz** with an
> **excitation current of 5 mA**, following a **15-min open circuit at SoC 0%
> and SoC 100%**. … **The loss in capacity is determined after every
> odd-numbered cycle.**"
>
> "All cells underwent **30 cycles at room temperature of 25 °C** before
> different temperatures were set. The battery is cycled until its **end of
> life (EoL), which is defined as when capacity drops below 80% of its initial
> value after undergoing these 30 cycles**."

정리하면:

| 축 | 값 |
|---|---|
| 충전 | 1C = 45 mA, CC–CV, 상한 **4.2 V** |
| 방전 | **2C = 90 mA**, CC, 하한 **3.0 V** (CV 없음) |
| 휴지 | SoC 0 % 와 100 % 에서 각 **15분** 개방회로 |
| EIS 주기 | **짝수** 사이클마다 · 9 state |
| capacity 주기 | **홀수** 사이클마다 |
| EIS 여기 | 정현파 **전류 5 mA** (≈ C/9), 0.02 Hz–20 kHz, 60점 |
| 선행 이력 | 전 셀 **25 °C 30사이클** 후 온도 분기 |
| EoL | 30사이클 후 용량 기준 **80 %** 이하 |

`[해석]` 세 가지가 눈에 띈다. (a) **방전이 2C** 로 비대칭이다 — 45 mAh 코인셀에
2C 는 가혹하고, 이것이 아래 §6 의 극단적 수명 편차의 배경이다. (b) 용량은
**홀수** 사이클, EIS 는 **짝수** 사이클에 재므로 한 스펙트럼과 짝지어지는 용량
라벨은 **같은 사이클의 것이 아니라 ±1 사이클의 것**이다 (원문은 이 보간/짝짓기
규칙을 적지 않는다). (c) 방전이 2C CC 뿐이므로, 용량 라벨이 그 2C 방전용량이면
**라벨 자체가 동역학을 싣는다** — "capacity 를 예측한다" 가 순수 열역학량의
예측이 아니다. 원문은 어느 쪽인지 밝히지 않는다 (위 "확인이 필요한 것" 5번).

## 1.6 ★ `state I~IX` — 아홉 개 전부 닫힘, 그리고 넷은 DC 전류 중 측정

SI Fig. 1 캡션 `[인쇄]` 전문:

> "Supplementary Figure 1 – EIS data are collected at nine different states
> (representing as I-IX) during constant current-constant voltage (CC-CV)
> charging and discharging: **I: Before charging; II: Start charging; III:
> After 20 minutes charging; IV: After charging and before resting; V: After 15
> minutes rest; VI: Start discharging; VII: After 10 minutes discharging;
> VIII: After discharging and before resting; IX: After 15 minutes rest.**
> The red (green) dots correspond to **with (without) DC current**."

`[도표]` SI Fig. 1 을 직접 봤다 (`fig_S1.png`). 전압-시간 모식도 위에 구간이
`CC → CV → Rest → CC → Rest` 로 표시되고, 아홉 점의 색과 전압 위치가 다음과
같다:

| state | 시점 | 전압 위치 `[도표]` | DC 전류 `[도표]` | SOC `[해석]` |
|---|---|---|---|---|
| I | 충전 전 | 3.0 V | **없음** (녹색) | 0 % |
| II | 충전 시작 | 3.0 V | **있음** (적색) | ≈ 0 % |
| III | 충전 20분 후 | CC 구간 중턱 | **있음** (적색) | ≈ 40 % (어림) |
| IV | 충전 종료·휴지 전 | 4.2 V (CV 끝) | **없음** (녹색) | 100 % |
| V | 15분 휴지 후 | 4.2 V | **없음** (녹색) | 100 % |
| VI | 방전 시작 | 4.2 V | **있음** (적색) | ≈ 100 % |
| VII | 방전 10분 후 | 방전 곡선 중턱 | **있음** (적색) | ≈ 57 % (어림) |
| VIII | 방전 종료·휴지 전 | 3.0 V | **없음** (녹색) | 0 % |
| IX | 15분 휴지 후 | 3.0 V | **없음** (녹색) | 0 % |

SOC 어림의 근거 `[해석]`: III 은 1C(45 mA)로 20분 → 15 mAh 주입, 실측 가용용량
34~42 mAh 대비 ≈ 36~44 %. VII 은 2C(90 mA)로 10분 → 15 mAh 방출, 100 % 에서
≈ 57~64 % 로 내려온다. **±10 %p 수준의 어림이며 원문에 SOC 수치는 없다.**

`[해석]` **이것이 이번 흡수에서 Phase 2 설계에 가장 크게 영향을 주는 사실이다.**
우리는 `state I~IX` 를 "SOC 스윕" 으로 읽고 그것을 SEV 의 실측 대응물 후보로
지목했다. 원전을 보면 그 읽기는 **절반만 맞다**:

1. **전류 없는 상태의 SOC 는 두 점뿐이다** — 0 %(I, VIII, IX) 와 100 %(IV, V).
   중간 SOC 인 III(≈40 %)·VII(≈57 %)은 **DC 전류가 흐르는 중에** 측정된다.
2. DC 전류 중의 EIS 는 정상성·선형성 가정을 위반한다 (동작점이 측정 중에
   이동한다). 이 네 state(II, III, VI, VII)의 스펙트럼은 평형 임피던스가 아니라
   **바이어스된 임피던스**다.
3. 따라서 이 데이터셋으로 "R_ct 의 stoichiometry 의존성"(= SEV 의 정의축)을
   재려 하면, **평형 조건에서는 SOC 2점**밖에 없고 중간 SOC 를 쓰려면 DC
   바이어스를 감수해야 한다.

이것은 우리 위키가 `state V` 하나만 알던 때보다 훨씬 구체적인 제약이다. §7 에서
Phase 2 설계로 옮긴다.

---

# 2. 절별 해체분석

## 2.1 Abstract

`[인쇄]` 전문의 주장 네 개:

> "we build an accurate battery forecasting system by combining
> electrochemical impedance spectroscopy (EIS)—a real-time, non-invasive and
> information-rich measurement that is hitherto underused in battery
> diagnosis—with Gaussian process machine learning."
>
> "**Over 20,000 EIS spectra** of commercial Li-ion batteries are collected at
> different states of health, states of charge and temperatures—**the largest
> dataset to our knowledge of its kind**."
>
> "Our Gaussian process model takes the **entire spectrum as input, without
> further feature engineering**, and automatically determines which spectral
> features predict degradation."
>
> "Our model accurately predicts the remaining useful life, **even without
> complete knowledge of past operating conditions** of the battery."

`[해석]` "20,000 스펙트럼" 의 산술을 확인해 둔다: `[도표]` SI Fig. 4 의 사이클
길이를 눈으로 합하면 12셀 총 ≈ 4,700 사이클 → 짝수 ≈ 2,350 → × 9 state
≈ 21,000. 원문 주장과 정합한다. **다만 독립 표본 수는 12(셀)이지 20,000이
아니다.** 한 셀의 인접 사이클 스펙트럼은 거의 같은 물체의 반복 측정이다.
"largest dataset" 는 스펙트럼 개수 기준의 주장이며, 통계적 자유도의 주장이
아니다.

"without complete knowledge of past operating conditions" 는 §2.5 에서
**온도 하나**를 모르는 경우로 축소된다. C-rate·프로토콜은 전 셀 동일하다.

## 2.2 Introduction — 이 논문이 스스로 놓는 자리

논지 전개 `[인쇄]` 요약:

1. 열화 예측이 안 되면 교체 시점도 second-life 판정도 못 한다.
2. 기존 접근 = 미시 기구 모델링(SEI 성장⁵⁶ · 리튬 도금⁷⁸ · **active material
   loss**⁹¹⁰). 그러나 `[인쇄]` "characterising and simulating every degradation
   mechanism is **unscalable**".
3. 그래서 데이터 주도. 그 어려움은 `[인쇄]` "defining a set of physically
   informative inputs, and building a robust statistical model".
4. 지금까지의 입력은 대부분 충방전 곡선 유래 (참조 13–18). EIS 는 정보가 많지만
   고차원이라 안 쓰인다.
5. **기존 EIS 축약법 두 갈래를 비판한다** `[인쇄]`:

   > "the spectrum is either interpreted by fitting to an equivalent circuit
   > model19,22–28 (recent work employed machine learning to aid the fit29)—
   > **the fit is often non-unique** and it is questionable whether a purely
   > electrical model can capture the physical, chemical and materials
   > properties and processes of a battery—or focusing only on handpicked
   > frequencies30–32."

6. 대안: 스펙트럼 전체를 넣고 모델이 고르게 한다 (ARD).

`[해석]` **5번이 이 논문 전체에서 유일한 비유일성 진술이다** (§5 어휘 전수 참조).
그리고 그것은 **경쟁 방법(등가회로 fitting)에 대한 비판**이지 자기 사상에 대한
질문이 아니다. 논증 구조가 이렇다: "ECM fitting 은 비유일하다 → 그러니
해석하지 말고 스펙트럼을 통째로 회귀에 넣자." 비유일성이 **제거된 것이 아니라
질문 대상에서 빠진 것**이다. 회귀는 스펙트럼 → 용량 방향이므로 역문제가 아니게
되지만, 그 대가로 **"무엇이 열화했는가" 를 물을 수 없게 된다**. 제목의
"identifying degradation **patterns**" 이 실제로 무엇을 뜻하는지는 §6 에서
확정한다.

## 2.3 Results — Capacity estimation (Fig. 1)

설계 `[인쇄]`:

> "We first consider a setting where the user wants to estimate the capacity of
> a battery using the EIS of the current cycle, **with the knowledge of the
> temperature**, which is kept constant throughout, **and the SoC (state I–IX
> shown in Supplementary Fig. 1)**."
>
> "We train the EIS-Capacity GPR model on **four cells** cycled at room
> temperature of 25 °C (marked as **25C01–25C04**), and test it on the **other
> four cells** (marked as **25C05–25C08**)."

`[해석]` **분할이 셀 단위다.** 이것은 이 계보에서 칭찬할 점이다 — Su 2024 는
셀 **안** 40/60 무작위 분할을 썼고(그 이유를 스스로 "battery consistency" 라고
인쇄했다), Zhang 은 셀을 통째로 뺐다. 다만 첫 문장이 중요하다: 모델은 **온도와
state 를 이미 안다**. 즉 이 "capacity estimation" 은 (온도, state) 조건부
회귀이며, state 마다 별도 모델이다 (SI Fig. 2 가 그 아홉 모델이다).

결과 `[인쇄]`:

> "Figure 1a shows the result of 25C05 cell for the state V (15 min resting
> after fully charging); the results at other states are **similarly positive**
> and shown in Supplementary Fig. 2. Out of all the states of I–IX, the model
> is **most accurate at electrochemically stable states** (i.e. the state V/IX,
> which is fully charged/discharged after resting), where electrochemical
> measurements on cells are more consistent."

한계의 자백 `[인쇄]`:

> "We note that all testing cells are charged and discharged the same way as
> the training cells; **the ability of our model to estimate the cells cycled
> at different operating charge/discharge rates needs to be investigated by
> further experiments.**"

ARD 해석 `[인쇄]`:

> "Interestingly, the model finds that **only two salient frequencies, out of
> the 120 possibilities** in the range of 0.02 Hz–20 kHz, are sufficient to
> estimate capacity … The selected frequencies of **17.80 and 2.16 Hz** are
> located in the low-frequency region, suggesting that it is the **change in
> the interfacial properties** that underpins degradation for these batteries;
> this is consistent with the results obtained in previous works35 …"

`[해석]` 세 가지를 지적한다.

**(a) "120 possibilities" 는 주파수가 아니라 예측자다.** Methods `[인쇄]` 가
입력을 `x = [Zre(ω1)…Zre(ω60), Zim(ω1)…Zim(ω60)]ᵀ` 로 정의하므로 **주파수는
60개**, 예측자가 120개다. Fig. 1c 캡션의 "the pink points correspond to the 120
frequencies" 는 틀린 서술이다. 공개 코드가 이를 확정한다 —
`covfunc = @covSEard; hyp.cov = log(ones(**121**,1))` `[코드]` (=120 길이척도
+ 1 신호분산). 그리고 SI Fig. 3(b) 캡션 `[인쇄]` 이 "**The imaginary part** of
the salient frequencies show a positive linear correlation with the cycle
number" 라고 못 박으므로, 91·100번 예측자는 **허수부**다. §4 에서 우리가 이를
수치로 확인했다.

**(b) "similarly positive" 는 SI 가 반증한다.** `[도표]` SI Fig. 2 의 8개
패널 R² 는 아래와 같다 (직접 봄):

| state | I | II | III | IV | (V) | VI | VII | VIII | IX |
|---|---|---|---|---|---|---|---|---|---|
| R² `[도표]` | 0.61 | 0.66 | 0.53 | 0.60 | **0.88** (Fig. 1a) | **0.28** | 0.86 | 0.68 | 0.81 |

state VI 는 **0.28** 이다. 아홉 중 하나는 사실상 실패이고, 중앙값은 0.66 이다.
"similarly positive" 는 성립하지 않는다.

**(c) 저자의 설명("electrochemically stable states 가 제일 정확하다")도 자기
SI 와 부분적으로 어긋난다.** 순위는 V(0.88) > **VII(0.86)** > IX(0.81) >
VIII(0.68) > II(0.66) > I(0.61) > IV(0.60) > III(0.53) > VI(0.28) 이다.
2위 VII 은 **2C 방전 10분 경과 시점, DC 전류가 흐르는 중** 이다 — 아홉 중 가장
"electrochemically stable" 하지 않은 축에 속한다. 반대로 IV(100 % SOC, 전류
없음)는 0.60 에 그친다. 즉 "정지 상태가 좋다" 는 서술은 V·IX 만 보고 만든
것이고, VII 과 IV 를 설명하지 못한다.

## 2.4 Results — RUL prediction (Fig. 2, SI Table 1)

`[인쇄]`:

> "Figure 2 shows that the EIS-RUL GPR model accurately predicts the RUL of all
> four testing cells cycled at 25 °C **only from EIS measurements at the
> current cycle, without requiring EIS measurements from previous cycles**."

기준선 비교 `[인쇄]`:

> "we benchmark our method against features extracted from the discharging
> curve, following recent work18. We feed those discharging curve features to
> the same machine-learning method (GPR model) and using the same training-test
> split. We observe that our method achieves a lower predictive error (cf.
> Supplementary Table 1)."

`[도표]` Fig. 2 (직접 봄): 네 패널의 R² = **0.96 / 0.73 / 0.68 / 0.81**
(25C05/06/07/08). 캡션 `[인쇄]`: "The end of life (EoL) of these four testing
cells is **150, 120, 30 and 38**, respectively". 음영은 ±1 표준편차.

`[인쇄]` SI Table 1 (자동 크롭이 "거의 백지" 로 오판해 제외했으므로 SI 6쪽을
직접 렌더해 읽었다 — 값은 표에 인쇄된 것):

| 입력 | 25C05 | 25C06 | 25C07 | 25C08 |
|---|---|---|---|---|
| **EIS (ours)** | **8.57** | **18.19** | **5.25** | **5.03** |
| Capacity and voltage curves | 43.22 | 34.28 | 38.14 | 73.20 |

단위는 표에도 캡션에도 **없다** (RUL 이므로 사이클로 읽는 것이 자연스럽다).

`[해석]` 네 가지.

**(a) 기준선이 망가져 있다.** 25C08 의 RUL 범위 전체가 0–38 사이클인데 기준선의
RMSE 가 **73.20** 이다 — 타깃 범위의 **1.9배**. 25C07 도 범위 0–30 에 RMSE
38.14. 상수 예측(평균값 예측)조차 RMSE 는 범위의 30 % 수준에 머문다. 즉 이
기준선은 "방전곡선 feature 가 EIS 보다 약하다" 를 보이는 것이 아니라
**구현·튜닝이 되지 않았음**을 보인다. feature 목록이 인쇄되지 않아 재현도
불가능하다. **이 비교는 인용에 쓸 수 없다.**

**(b) RUL 은 사이클 번호의 결정론적 함수다.** RUL = EoL − cycle 이고 EoL 은
셀 상수다. 그리고 §4 에서 확인하듯 임피던스의 유효 예측자는 사이클에 대해
단조롭다. 따라서 "RUL 예측" 은 사실상 **"스펙트럼에서 사이클 번호를 읽고 그
셀의 EoL 상수에서 뺀다"** 이고, 어려움 전부가 **EoL 상수를 맞히는 것**에 있다.
per-cell R² 는 그 어려움을 재지 않는다 — 한 셀 안에서 실제 RUL 이 직선이므로
단조 예측이면 R² 가 높게 나온다.

**(c) 오차가 가장 큰 곳이 하필 EoL 근처다.** `[도표]` Fig. 2b 에서 actual
RUL = 0 일 때 예측 RUL ≈ **15 사이클**, Fig. 2c 에서 ≈ 2.5, Fig. 2a 에서 ≈ 9.
`[도표]` Fig. 4b(다온도 모델)에서는 actual RUL = 0 에서 예측 ≈ **45 사이클**,
Fig. 4c 에서 ≈ 40. **수명이 다한 셀에게 "아직 40~45 사이클 남았다" 고 말한다.**
안전 판정 용도라면 이 방향의 오차가 가장 비싸다. 논문은 이 지점을 언급하지
않는다.

**(d) 예측 구간이 음수로 내려간다.** `[도표]` Fig. 2c/2d 의 ±1σ 하단이 actual
RUL ≈ 0 근방에서 **0 아래**로 내려간다. RUL 은 음수일 수 없으므로 사후분포가
타깃의 지지집합을 존중하지 않는다 (GP 회귀의 알려진 성질이며 논문이 다루지
않는다).

## 2.5 Results — 다온도 (Fig. 3, Fig. 4)

문제 설정 `[인쇄]`:

> "we explore a simpler toy problem: rather than considering a variation of
> cycling temperature over time, we ask the question whether the model can
> still predict RUL, based on the EIS measured at the current cycle, **without
> knowledge of the cycling temperature** except that it is constant over
> cycles. We make a further simplification that the temperature is either 25,
> 35 or 45 °C. We combine the training data acquired at three different
> temperatures (i.e. **25C01–25C04, 35C01 and 45C01** cells), and in effect
> **forcing GPR to learn features of the EIS that only depends on capacity but
> not temperature**."

ARD 결과 `[인쇄]`:

> "Similarly, each model finds that **only one salient frequency** is
> sufficient to estimate capacity. The selected frequency, **17.80 Hz**, is
> located in the low-frequency region …"

`[도표]` Fig. 3 (직접 봄):

- **(a) 35C02, R² = 0.81.** 예측(적)이 측정(청)보다 **계통적으로 위**에 있다.
  사이클 ≈ 30–200 구간에서 측정 곡선이 **±1σ 음영 밖**에 있다
  (figure-read ≈: 사이클 100 에서 측정 ≈ 0.875, 예측 ≈ 0.905, 음영 하단
  ≈ 0.885).
- **(b) 45C02, R² = 0.72.** 예측이 사이클 0→60 사이에 0.97 → **1.01 로
  상승**한다 (측정은 단조 감소). 사이클 ≈ 20–200 에서 측정이 음영 밖, 사이클
  450 이후에는 반대로 예측이 측정보다 아래로 내려가 다시 벗어난다.
- **(c)(d) ARD.** 91번 예측자 하나만 가중치 **1.0**, 나머지 119개는 **정확히
  0** 으로 보인다.

`[도표]` Fig. 4 (직접 봄): 세 시험 셀의 RUL, R² = **0.87 / 0.75 / 0.92**,
캡션 `[인쇄]` 의 EoL = **150, 252, 396** (25/35/45 °C).

`[해석]` 두 가지.

**(a) ±1σ 구간이 보정돼 있지 않다.** Fig. 3a/3b 에서 측정값이 예측 ±1σ 밖에
**연속 100 사이클 이상** 머문다. 정규 가정이면 ±1σ 밖 확률은 32 % 이고 그것도
무작위로 흩어져야 하는데, 여기서는 **계통 편의(bias)** 다. 논문에는 coverage
통계도 보정 그림도 없고, `calibrat*` 어휘가 본문·SI에 **0회**다 (§5).
즉 **불확실성은 그려졌으나 검증되지 않았다.**

**(b) 온도가 배치와 교락(confound)돼 있다.** `[도표]` SI Fig. 4 에서 초기용량이
온도군마다 계통적으로 다르다: 45 °C 셀 ≈ 40.5–42 mAh, 35 °C 셀 ≈ 39–39.5 mAh,
25 °C 셀 ≈ 34–36 mAh. 게다가 **고온 셀이 더 오래 산다** — 45C01/45C02 는 500
사이클에서도 ≈ 31–32 mAh 인 반면 25 °C 셀들은 170–450 사이클에서 20–25 mAh 로
끝난다. Arrhenius 상식과 반대 방향이며 **논문은 이것을 한 줄도 언급하지 않는다.**
공개 코드가 이를 절대값으로 확인해 준다 `[코드]`: 다온도 훈련 라벨
`Capacity_data.txt` 를 셀 경계로 자르면 각 셀의 시작 용량이
**37.20 / 36.77 / 35.06 / 35.53 / 40.11 / 42.31 mAh** 이고 마지막 두 개(35C01,
45C01)가 뚜렷이 높다.
→ "온도를 모르는 채 용량을 맞힌다" 는 주장은, 온도군이 **절대 용량 범위로 이미
분리돼 있는** 데이터에서 얻어진 것이다. 모델이 배운 것이 "용량에만 의존하고
온도에는 의존하지 않는 feature" 인지, 아니면 **배치 식별자**인지 이 설계로는
가를 수 없다. 게다가 고온군은 **훈련 1셀 / 시험 1셀**이다.

## 2.6 Discussions

`[인쇄]` 전문의 주장:

> "we show that our GPR models accurately estimate the capacity and predict the
> RUL using EIS spectra of cells with **different degradation patterns** cycled
> at various temperatures but **under constant charge/discharge rates**."
>
> "Predictions from our model can be **attributed back to the impedance
> spectra**, yielding the observation that the low-frequency region of the EIS
> spectrum is the most predictive."
>
> "one might **not need to perform a full sweep** over a broad range of
> frequencies to obtain signals relevant to degradation."
>
> "We anticipate that our observation … can be extended to consider more
> challenging and realistic settings, such as variations in cycling temperature
> over time or variations in charge/discharge rate. **However, a significantly
> larger training set is required** … We defer consideration of those aspects
> to future work."

`[해석]` **"degradation patterns" 이라는 말은 본문에 딱 두 번 나온다 — 제목과
이 문장이다.** 그리고 이 문장에서의 뜻은 명백히 **"셀마다 다른 용량 감소
궤적/속도"** 이지 열화 **모드**가 아니다. §6 에서 확정한다.

## 2.7 Methods — Gaussian process regression

`[인쇄]` 요점만:

- 입력 `xi = [Zre(ω1), …, Zre(ω60), Zim(ω1), …, Zim(ω60)]ᵀ`, 60 주파수,
  0.02 Hz–20 kHz, **현재 사이클의 스펙트럼**. 출력 `yi` 는 용량.
- `[인쇄]` "The inputs are normalised using the mean and standard deviation of
  **the training data**." (누설 방지 측면에서 옳은 처리다.)
- `yi = f(xi) + εi`, `εi ~ N(0, σ²)` i.i.d. 가우시안 잡음. `f ~ N(0, K)`.
- 예측 분산 식 (3) 뒤에 `[인쇄]` "**which is a measure of uncertainty**".
- 용량 모델: zero mean + **SE-ARD** 공분산, GPML toolbox³⁷.
  `[인쇄]` "The ARD covariance function allows the model to **downweight and
  prune irrelevant frequencies** from the input by setting σm to be large. …
  We define the importance of the mth frequency as **wm = exp(−σm)**, with
  0 < wm < 1."
- RUL 모델: zero mean + **선형(LIN)** 공분산 `kLIN(xi,xj) = Σ xᵢₘᵀxⱼₘ`.
- `[인쇄]` "Although GPR has been used in the literature in the context of
  Li-ion batteries17,33,34, we depart from those pioneering works by employing
  **impedance spectra as input**, as well employing **ARD** to shed light on
  salient frequencies."

`[해석]` 방법론적으로 지적할 것 셋.

**(a) 하이퍼파라미터를 주변우도 최대화로만 정한다.** 검증 분할도, 사전분포도,
재시작(restart)도 인쇄돼 있지 않다. 120차원 ARD 길이척도를 6셀(다온도) 또는
4셀(25 °C) 데이터로 최대우도 적합하면 **극단적 희소 해로 빠지기 쉽다** — 이것이
Fig. 3c/d 의 "하나만 1.0, 나머지 전부 0" 모양과 무관하지 않다.

**(b) `wm = exp(−σm)` 은 정의로서 임의적이다.** σm 은 차원이 있는 길이척도인데
지수 안에 그대로 들어간다. 게다가 공개 코드는 이 식을 **그대로 쓰지 않는다**
(§4 (c)).

**(c) 잡음 σ² 는 관측 잡음 모형이다.** 식 (3) 의 "uncertainty" 는
**"학습 데이터를 조건으로 한 GP 사후 예측 분산"** — 즉 (i) 가정한 i.i.d. 관측
잡음과 (ii) 커널이 표현하는 함수 불확실성의 합이다. **라벨(용량·RUL) 자체의
불확실성도, 셀 간 변동도, 모형 오설정도 포함하지 않는다.** §6 에서 우리 축과
대조한다.

## 2.8 Data / Code availability

`[인쇄]` 두 문장 (§1.3, §4 에서 이미 인용).

---

# 3. 그림별 판독 — 무엇을 보고 무엇을 안 봤는가

크롭 8장 (`wiki/raw/figures/zhang2020_eis-gpr-capacity-rul/`, 본문 4 + SI 4).
**8장 전부 실제로 Read 로 열어 봤다.** 추가로 자동 크롭이 "거의 백지" 로 오판해
제외한 **SI Table 1** 은 SI 6쪽을 직접 렌더해서 읽었다 (그 PNG 는 위키에 넣지
않았고, 값은 §2.4 에 전사했다).

| 파일 | 무엇 | 이 digest 에 준 것 |
|---|---|---|
| `fig_1.png` | 용량 추정 (a 25C05 시계열 · b 예측-측정 산점도 · c ARD) | R²=0.88 · ±1σ 폭 · 셀별 계통 편의 · ARD 두 첨두 |
| `fig_2.png` | 25 °C 시험 4셀 RUL | R² 4개 · EoL 근처 낙관 편의 · 음수 구간 |
| `fig_3.png` | 다온도 용량 (a 35C02 · b 45C02) + ARD (c 35 °C · d 45 °C) | **±1σ 미보정의 결정적 증거** · 예측 초기 상승 |
| `fig_4.png` | 다온도 RUL 3셀 | R² 3개 · actual RUL 0 에서 예측 40–45 |
| `fig_S1.png` | **state I~IX 정의 모식도** | **①-6 을 닫는 그림.** 색으로 DC 전류 유무까지 |
| `fig_S2.png` | state 별 용량 추정 8패널 | **"similarly positive" 반증** (R² 0.28~0.86) |
| `fig_S3.png` | 91·100번 예측자의 사이클 의존 | 허수부 확정 + 단조 상승 |
| `fig_S4.png` | 12셀 용량 유지 곡선 | **①-2 를 닫는 그림** + 온도·배치 교락 |

**본문 서술과 어긋난 그림이 있었는가 — 있다, 세 건.**

1. **SI Fig. 2 vs 본문**: 본문은 "similarly positive", 그림은 R² 0.28~0.86.
2. **SI Fig. 2 캡션 vs 본문**: 캡션은 "**25C02** cell", 본문 흐름은 25C05.
   25C02 는 훈련 셀이므로, 캡션이 맞다면 그 R² 들은 **in-sample** 이다.
3. **Fig. 1c 캡션 vs Methods**: 캡션 "the 120 **frequencies**" vs Methods
   "60 frequencies × (실·허)". 캡션이 틀렸다.

**세부 판독값** (figure-read ≈, 원문 도표가 정본):

- `fig_1a`: 사이클 300 에서 측정 ≈ 0.74, 예측 ≈ 0.755, ±1σ 음영 ≈ 0.665–0.845.
  **음영 폭(≈0.18)이 전체 열화 폭(1.00 → 0.74 = 0.26)의 69 %** 다.
- `fig_1b`: 항등선이 그려져 있지 않다. 네 셀이 서로 다른 곡선을 그리고
  (25C07 보라별이 가장 아래), 측정 0.72–0.80 구간에서 예측이 0.78–0.80 에
  **뭉쳐 포화**한다 — 저용량 쪽 과대예측·고용량 쪽 과소예측의 S자 편의.
- `fig_1c`: 91번 ≈ 0.53, 100번 ≈ 0.43, 40번 근처에 작은 혹 ≈ 0.03, 나머지 ≈ 0.
- `fig_S3b`: 25C01 state V 에서 −Im(17.80 Hz) 가 사이클 0→300 동안
  ≈ 0.157 → 0.222 Ω, −Im(2.16 Hz) 가 ≈ 0.063 → 0.096 Ω 로 **둘 다 단조 상승**.
- `fig_S4`: 초기용량 25 °C ≈ 34–36 · 35 °C ≈ 39–39.5 · 45 °C ≈ 40.5–42 mAh.
  y축 라벨이 `Capacity (mA/h)` 로 **단위 오기** (mAh 여야 한다).

---

# 4. ★ 공개 코드 저장소 — 받아서 확인했다

`https://github.com/YunweiZhang/ML-identify-battery-degradation` 를 이번 세션에
**실제로 clone 했다** (성공). 구성 `[코드]`:

```
README.md
Code-Matlab.zip
  └ Code-Matlab/
      ARD_GPR.m                     ← Fig. 3(c) 재현
      Multi_T_EIS_Capacity_GPR.m    ← Fig. 3(a) 재현
      Multi_T_EIS_RUL_GPR.m         ← Fig. 4(b) 재현
      Readme.txt
      EIS_data.txt          1358 × 120   (다온도 용량모델 훈련 입력)
      Capacity_data.txt     1358 × 1
      EIS_data_RUL.txt       525 × 120   (RUL 모델 훈련 입력)
      EIS_data_RUL_norm.txt  525 × 120   (미사용)
      RUL.txt                525 × 1
      EIS_data_35.txt        299 × 120
      Capacity_data_35.txt   299 × 1
      EIS_data_35C02.txt     299 × 120
      capacity35C02.txt      299 × 1
      rul35C02.txt           127 × 1
      gpml-matlab-v4.2-2018-06-11/   (GPML 툴박스 통째 + Capacity_data_45.txt)
      __MACOSX/ 그림자 항목 다수
```

`[코드]` `Readme.txt` 전문 요지: "The scripts test the models to reproduce the
corresponding result on the **35C02 cell**. The original results in the main
manuscript are shown in **Fig. 3(a), Fig. 4(b) and Fig. 3(c)**, respectively."

즉 **전처리 코드는 없다.** 원시 EIS 파일 → `EIS_data*.txt` 행렬로 가는 경로
(주파수 정렬, 실/허 배치, 사이클 짝짓기, 용량 라벨 결합)가 저장소에 **없다**.
공개된 것은 "이미 만들어진 행렬 + GPR 3개 + 그림 그리기" 다.

## 4.1 코드에서 확정되는 것

**(a) 입력 차원 120 = 60 주파수 × (실, 허).**
`[코드]` `ARD_GPR.m`: `covfunc = @covSEard; hyp.cov = log(ones(121,1));`
→ 121 = 120 길이척도 + 1 신호분산.

**(b) 주파수 격자와 91·100번 예측자의 정체 — 우리가 역산해 확정.**
`[해석]` 20 kHz 에서 0.02 Hz 까지 60점 로그 등간격을 가정하면
`ω_n = 20000 × 10^(−6(n−1)/59)` Hz 이고, `ω₃₁ = 17.79 Hz`, `ω₄₀ = 2.16 Hz` 로
**원문의 17.80·2.16 Hz 와 일치한다.** 91 − 60 = 31, 100 − 60 = 40 이므로
**예측자 91 = Im Z(17.80 Hz), 예측자 100 = Im Z(2.16 Hz)** 다. SI Fig. 3(b)
캡션의 "imaginary part" `[인쇄]` 와도 일치한다. 공개 데이터로 직접 확인:
`EIS_data_35.txt` 의 1–60열은 모두 양수(≈0.39–1.5 Ω, 실수부), 61열부터 0 근처에서
부호가 바뀐다(허수부).

**(c) ARD 가중치 식이 논문과 다르다.**
논문 `[인쇄]`: `wm = exp(−σm)`.
코드 `[코드]` (`ARD_GPR.m`):

```matlab
sigmaL = hyp_ARD.cov(1:end-1);
sigmaL(1:120) = 10.^sigmaL(1:120);
weights = exp(-sigmaL);
weights = weights/sum(weights);
```

GPML 규약에서 `hyp.cov(1:D) = log(ℓ_d)` 이므로 `10.^hyp.cov` 는 `ℓ_d` 가 아니라
`ℓ_d^(ln 10) = ℓ_d^2.303` 이다. 즉 실제로 그려진 것은
`w_m ∝ exp(−ℓ_m^2.303)` 이고, 그 뒤 합으로 정규화된다.
`[해석]` `hyp.cov` 에 대해 단조이므로 **순위는 논문 식과 같다.** 그러나
`exp(−(큰 수))` 가 순식간에 언더플로하므로 **"나머지 119개가 정확히 0" 이라는
시각적 인상은 변환이 만든 것**이다 (Fig. 3c/d 에서 한 점만 1.0). 희소성의
강도를 이 그림에서 읽으면 안 된다.

**(d) 다온도 용량 모델은 ARD 를 쓰지 않는다.**
`[코드]` `Multi_T_EIS_Capacity_GPR.m`: `covfunc = @covSEiso;` — **등방
SE 커널**이다. Methods `[인쇄]` 는 "EIS-capacity GPR model" 을 SE-**ARD** 로
기술한다. 즉 Fig. 3(a) 의 예측 모델과 Fig. 3(c) 의 ARD 해석 모델은 **서로 다른
모델**이며, 논문 본문은 이를 구분하지 않는다. RUL 모델은
`covfunc = @covLINiso;` 로 논문과 일치한다.

**(e) ★ ARD 해석이 시험 셀 자신의 데이터로 적합돼 있다.**
`[코드]` md5 로 확인한 사실:

```
61891814fd18df15980d0794258097bf  EIS_data_35.txt
61891814fd18df15980d0794258097bf  EIS_data_35C02.txt
0d6472fecf88cd91afd20dbe5bc23d33  Capacity_data_35.txt
0d6472fecf88cd91afd20dbe5bc23d33  capacity35C02.txt
```

`EIS_data_35.txt` 와 `EIS_data_35C02.txt` 는 **바이트 동일**하고, 용량 파일도
그렇다. 그런데 `ARD_GPR.m` 의 주석은 `[코드]` "EIS_data_35 is the EIS data of
the cell cycled at 35 °C" 이고, `Multi_T_EIS_Capacity_GPR.m` 은 같은 내용의
`EIS_data_35C02.txt` 를 **시험 입력**으로 쓴다. `Readme.txt` 는 `ARD_GPR.m` 이
**Fig. 3(c)** 를 재현한다고 적는다.

→ `[해석]` **Fig. 3(c) 의 35 °C ARD 는 (공개 코드대로 실행하면) 시험 셀 35C02
한 셀의 데이터에 적합된다.** 성능 수치가 아니라 해석(ARD)이므로 "시험셀 누설로
정확도가 부풀었다" 는 주장은 성립하지 않는다. 그러나 두 가지가 남는다:
(i) 논문의 핵심 **해석적** 주장("17.80 Hz 하나면 된다")이 **단일 셀 in-sample
적합**에서 나왔고 셀 간 재현이 확인된 적이 없다, (ii) 훈련/시험 파일의 이름과
내용이 어긋나 있어 **어느 셀이 어디에 쓰였는지 코드만으로는 신뢰할 수 없다**.
(참고로 `Capacity_data_45.txt` 의 시작값 42.31 mAh 는 다온도 훈련 행렬의 6번째
셀 구간 시작값과 일치하므로 **훈련 셀 45C01** 이다 — 35 쪽은 시험 셀, 45 쪽은
훈련 셀로 **비대칭**이다.)

**(f) 훈련 라벨에서 읽히는 EoL 분포.**
`[코드]` `RUL.txt` (525행) 를 2씩 감소하는 구간으로 자르면 시작값이
**234, 162, 12, 218, 414** 인 5개 구간이 나온다 (길이 118, 82, 7, 110, 208).
`[해석]` 즉 다온도 RUL 모델의 훈련 셀 EoL 은 **12 사이클짜리 셀부터 414
사이클짜리 셀까지** 걸쳐 있고, EoL = 12 인 셀은 **스펙트럼 7개**만 기여한다.
훈련 셀 6개 중 5개 구간만 있으므로 한 셀은 RUL 학습에서 빠졌다.
`[해석]` 시험 셀 EoL 30·38 (Fig. 2) 과 합치면 **25 °C 코인셀 8개의 EoL 이
12~234 사이클, 약 20배로 흩어진다.** 동일 사양·동일 프로토콜에서다. 이 데이터로
"RUL 을 예측한다" 는 것은 **제조 편차를 예측한다**는 뜻에 가깝다.

## 4.2 우리가 공개 데이터로 직접 계산한 것 — ARD 선택은 유일하지 않다

`[해석]` (계산 대상: 공개 저장소의 `EIS_data_35.txt` 299×120 과
`Capacity_data_35.txt`. 우리 계산이며 논문의 주장이 아니다.)

- 예측자 91 과 용량의 상관 **r = −0.994**, 사이클과의 상관 **+0.991**
  (SI Fig. 3b 의 "positive linear correlation" 재현).
- **그러나 그 이웃들이 사실상 같은 정보를 싣는다**:
  corr(예측자 91, 예측자 92) = **0.998**, corr(91, 93) = 0.996,
  corr(91, 100) = 0.984.
- **120개 예측자 중 52개**가 단독으로 |r(용량)| > 0.95 이다
  (실수부 38–62번 = 저주파 실수부, 허수부 87–111번 등).
  |r| > 0.99 인 것만도 **5개**(예측자 90–94 = Im Z at 22.5, 17.8, 14.1, 11.1,
  8.8 Hz)이고 그 다섯의 |r| 은 0.9920~0.9941 로 **소수 셋째 자리에서 갈린다.**

→ `[해석]` **"120개 중 두 개만 중요하다" 는 참이지만, "왜 하필 그 두 개인가" 는
데이터가 정하지 않는다.** ARD 가 고른 것은 **주파수 하나가 아니라 대역
하나**이고, 그 대역 안에서 어느 점이 뽑히는지는 거의 동률인 상관 중 최적화가
어디에 착지했는지의 문제다. 이것은 정확히 우리가 다루는 종류의 비유일성 —
**공선 방향에 대한 해의 비식별성** — 이며, 논문은 이 가능성을 검토하지 않고
17.80 Hz 에 **물리적 의미(계면 물성 변화)** 를 부여한다.

이 판정은 저자들 자신의 데이터로 재현 가능하고, 반증하려면 "다른 셀·다른
온도에서도 91번이 다시 뽑히는가" 를 보이면 된다. Fig. 3(c)(d) 가 둘 다 91번을
가리키므로 그 방향의 증거가 **있는 것처럼 보이지만**, (e) 에서 보았듯 3(c) 는
단일 셀 적합이고 3(d) 는 다른 셀이며, 셀 간 재현 실험은 논문에 없다.

---

# 5. 어휘 전수 (합자 정규화 후, 본문 6쪽 + SI 6쪽 전체)

`ﬁ ﬂ ﬀ ﬃ ﬄ` 를 풀고 NFKC 정규화한 뒤 전수 계수했다.

| 어휘 | 본문 | SI | 비고 |
|---|---|---|---|
| `degenerac*` | **0** | **0** | |
| `degenerat*` | **0** | **0** | |
| `identifiab*` | **0** | **0** | 제목의 `Identifying` 은 동사형이며 별건 |
| `ill-posed` | 0 | 0 | |
| `uncertaint*` | **1** | **0** | 식 (3) 뒤 "which is a measure of uncertainty" 단 한 번 |
| `non-unique` | **1** | 0 | **등가회로 fitting 에 대한 비판** (§2.2) |
| `collinear*` · `confound*` · `ambigu*` | 0 | 0 | |
| `calibrat*` | **0** | 0 | 불확실성 보정 검사 없음 |
| `cross-valid*` | **0** | 0 | 교차검증이라는 말 자체가 없다 (셀 분할은 1회 고정) |
| `error bar` | 0 | 0 | (그림의 음영은 ±1 s.d. 로만 표기) |
| `LLI` · `LAM` | **0** | **0** | |
| `lithium inventory` · `loss of lithium` | **0** | 0 | |
| `active material` | 1 | 0 | Introduction 에서 **선행 연구 열거**로만 ("active material loss9,10") |
| `half-cell` | **0** | 0 | |
| `incremental capacity` | 2 | 0 | **참고문헌 13·14 의 제목 안** |
| `differential voltage` | 0 | 0 | |
| `equivalent circuit` | 1 | 0 | 비판 대상으로 |
| `standard deviation` | 5 | 1 | 그림 캡션의 "±1 standard deviation" + Methods |
| `degradation pattern(s)` | **2** | 0 | **제목 1 + Discussion 1** (§2.6) |

`[해석]` **이 계보 여덟 편째의 확인이다.** 지금까지 흡수한 일곱 편
(세미나 · Birkl 2017 · Dubarry 2012 · Wang 2025 리뷰 · Kim 2023 · Su 2024 ·
Rhyu 2025) 에서 `degenerac*` 은 연속 0회였고 `identifiab*` 은 Rhyu 의 **참고문헌
제목 안 1회**가 유일했다. **Nature Communications 이고 케임브리지 물리/ML
그룹이며 심사자가 Braatz 인 이 논문에서도 둘 다 0회다.**

다만 이 논문은 앞의 일곱 편과 **한 가지가 다르다**: 비유일성을 **말한다**.
`[인쇄]` "the fit is often non-unique". 그런데 그 문장은 (a) 자기 방법이 아니라
**경쟁 방법**을 향하고, (b) 그것을 **자기 방법을 정당화하는 근거**로 쓴다
("그러니 fitting 하지 말고 회귀하자"). `[해석]` 즉 이 계보에서 비유일성 어휘가
처음 등장한 자리는 **자기 진단이 아니라 타 방법 기각**이며, 이는 "그 개념이
없어서 안 쓴 것이 아니라, 자기 쪽으로 돌리지 않은 것" 이라는 더 강한 형태의
확인이다.

---

# 6. ★ 우리 축으로의 판정

## 6.1 무엇을 예측하는가 — 라벨의 확정

**라벨은 두 개뿐이다. 둘 다 셀 수준 스칼라다.**

| 모델 | 입력 | 출력(라벨) | 라벨의 출처 |
|---|---|---|---|
| EIS-Capacity GPR | 스펙트럼 120차원 (특정 state, 특정 온도) | **용량** (mAh; 그림에서는 초기값으로 정규화) | **측정** — 홀수 사이클의 방전용량 `[인쇄]` |
| EIS-RUL GPR | 같은 스펙트럼 | **RUL** (사이클) | **측정 유래 파생값** — EoL(용량 80 % 도달 사이클) − 현재 사이클 |

**열화 모드(LLI/LAM_PE/LAM_NE) 라벨은 없다.** 근거는 세 겹이다:

1. `LLI` · `LAM` · `lithium inventory` · `loss of lithium` · `half-cell` 이
   본문·SI 에 **각 0회** (§5).
2. 모드를 재는 어떤 절차도 없다 — half-cell OCP fitting 없음, ICA/DVA 없음,
   해체분석 없음, 물리 모델 시뮬레이션 없음.
3. `[인쇄]` Introduction 이 미시 기구 모델링을 **명시적으로 포기**한다
   ("characterising and simulating every degradation mechanism is
   unscalable") — 즉 모드 분해는 이 논문의 설계상 **범위 밖**이다.

→ **우리 위키의 판단("이 데이터셋에는 LLI/LAM 라벨이 없다")은 원전에서
확정됐다.** 이제 이 문장은 "Su 도 (확인 필요하나) Zhang 도" 라는 유보 없이
쓸 수 있다.

**제목의 "identifying degradation patterns" 의 실제 의미**: Discussion 의 유일한
용례가 `[인쇄]` "EIS spectra of cells with **different degradation patterns**
cycled at various temperatures" 이므로, **"셀마다 다른 용량 감소 궤적"** 이다.
그리고 본문에서 `identify` 계열이 쓰이는 유일한 자리는 `[인쇄]` "GPR with an
ARD kernel allows us to **identify important features** amid many irrelevant
ones" — **주파수를 고르는 것**이다. `[해석]` 즉 제목이 약속하는 "열화 패턴
식별" 은 **열화 모드 식별이 아니라 (i) 서로 다른 감쇠 곡선을 가진 셀들에 대해
용량/RUL 을 맞히는 것 + (ii) 그 예측에 쓰인 주파수를 지목하는 것**이다.
우리 축에서 이 논문은 **모드 식별 논문이 아니다.**

## 6.2 사상의 유일성을 저자들이 묻는가 — 전수 결과

**묻지 않는다.** "서로 다른 열화 상태가 같은 스펙트럼을 낼 수 있는가" 를 다루는
문장은 본문·SI 에 **없다** (§5 의 `degenerac*` 0 · `identifiab*` 0 ·
`ambigu*` 0 · `collinear*` 0 · `confound*` 0). 유일한 비유일성 문장은 등가회로
fitting 을 향한 것이다.

`[해석]` **그런데 이 논문의 설계 자체가 사상이 일대일이 아님을 이미 인정하고
있다.** 세 가지가 그 증거다:

1. **state 별로 모델이 따로다.** 같은 용량의 같은 셀이 **아홉 개의 다른
   스펙트럼**을 낸다. 그래서 모델 입력에 "SoC(state)를 안다" 를 전제로 깔았다
   `[인쇄]`. 즉 스펙트럼 → 용량 사상은 **state 조건부**로만 함수다.
2. **C-rate 를 고정해야 한다.** `[인쇄]` "the ability of our model to estimate
   the cells cycled at different operating charge/discharge rates **needs to be
   investigated**". 프로토콜이 바뀌면 사상이 바뀐다는 뜻이다.
3. **셀별 오프셋이 그림에 남아 있다.** `[도표]` Fig. 1b 에서 네 시험 셀이 서로
   다른 궤적을 그린다 — 같은 측정 용량에 대해 셀마다 다른 예측이 나온다.

→ `[해석]` **이 논문은 우리 질문의 EIS 판에 "답하지 않은" 것이 아니라,
"조건을 좁혀서 회피한" 것이다.** (온도, state, C-rate) 를 전부 고정하거나 입력에
넣은 뒤 남은 잔여 사상만 회귀했다. 우리 프로젝트의 언어로 말하면, **식별
가능성을 확보한 것이 아니라 조건부화(conditioning)로 문제를 바꾼 것**이고,
그 조건들이 바로 우리가 "프로토콜 식별자" 라고 부르는 것들이다. 다만 공정하게
적자면 — 이 논문은 그 식별자를 **feature 로 몰래 섞은 것이 아니라 설계
전제로 명시**했고, 한계도 명시했다. Rhyu 2025 를 제외하면 이 계보에서 가장
정직한 축에 든다.

## 6.3 GPR 불확실성 — 보고하는가, 무엇의 불확실성인가

**보고한다.** 식 (3) 의 사후 예측 분산을 계산하고 `[인쇄]` "a measure of
uncertainty" 라 부르며, Fig. 1a · Fig. 2 · Fig. 3a,b · Fig. 4 **전부에 ±1
표준편차 음영**을 그린다. 이 계보에서 **불확실성을 그림으로 보여 주는 첫
논문**이다 (Birkl 2017 · Kim 2023 · Su 2024 · Rhyu 2025 · 세미나 모두 없었다).

**무엇의 불확실성인가** `[해석]`: 식 (1)–(3) 의 구조상
`Δ² = K(x*,x*) − K(x*,X)(K(X,X)+σ²I)⁻¹K(X,x*)` 는
**(i) 가정한 i.i.d. 관측잡음 σ² 와 (ii) 커널이 표현하는 함수 불확실성**의 합이다.
포함되지 **않는** 것:

- **라벨의 불확실성** — 용량 측정 자체의 오차, EoL 정의의 임의성(80 %),
  홀짝 사이클 짝짓기 오차.
- **셀 간 변동** — 훈련 셀 4~6개로부터의 일반화 오차. GP 는 훈련 입력 근방이면
  분산을 작게 준다. 시험 셀이 훈련 셀들과 **다른 셀**이라는 사실은 커널이
  모른다.
- **모형 오설정** — 커널·평균함수·정상성 가정이 틀렸을 가능성.

**그리고 검증되지 않았다.** `[도표]` Fig. 3a/3b 에서 **측정 곡선이 ±1σ 음영
밖에 연속 100 사이클 이상** 머문다 (계통 편의). coverage 통계도, 보정 그림도,
NLL/CRPS 같은 확률적 점수도 없고 `calibrat*` 는 0회다.

→ `[해석]` **"불확실성을 보고했다" 와 "불확실성이 맞다" 는 다른 주장이고, 이
논문은 앞의 것만 했다.** 우리 프로젝트가 라벨에 오차 막대를 붙일 때 이 사례를
반면교사로 삼는다: **구간을 그리면 반드시 그 구간의 coverage 를 함께 보고한다.**

## 6.4 이 논문의 ML 을 우리 판정 기준으로 채점

우리가 다른 논문에 적용해 온 세 축으로 채점한다.

| 축 | 판정 |
|---|---|
| **fitted 라벨을 ground truth 로 쓰는가** | **아니다 — 이 계보에서 드물게 깨끗하다.** 라벨(용량)은 **측정값**이다. fitting 으로 만든 라벨이 없다. 단 RUL 은 EoL 정의(80 %)에 의존하는 **파생값**이고, 용량이 2C 방전용량이면 동역학이 섞인다(미확인) |
| **프로토콜 식별자가 입력에 섞였는가** | **입력에는 안 섞였다. 그러나 설계 전제로 고정돼 있다.** state 와 온도는 모델 밖에서 조건화되고(단일온도 모델), C-rate 는 전 셀 동일. 다온도 모델은 온도를 빼지만 **온도군이 절대 용량 범위로 분리돼 있어** 교락된다 (§2.5) |
| **검증 설계** | **셀 단위 분할 — 이 축에서는 합격.** 다만 (a) 분할이 **1회 고정**이고 반복·교차검증이 없다, (b) 다온도의 고온군은 **훈련 1셀 / 시험 1셀**, (c) 하이퍼파라미터를 훈련 전체의 주변우도로 정하고 내부 분할이 없다, (d) 정규화는 훈련 통계로 — 이건 옳다 |
| **단독 스윕만으로 분리 가능을 주장하는가** | 해당 없음 (모드 분해를 하지 않으므로) |

`[해석]` 종합하면 **이 논문은 "라벨이 깨끗하고 검증 분할이 셀 단위인" 드문
사례**이며, 우리가 다른 논문에 던지는 비판 대부분이 여기엔 안 붙는다. 대신 붙는
비판은 다른 종류다: **표본 수(12셀)에 비해 주장의 폭이 크고, 해석(ARD)이
비유일하며, 불확실성이 보정되지 않았고, 기준선이 망가져 있다.**

---

# 7. ★ Phase 2 에 직접 쓸 수 있는 것

`mode-observability/README.md` 의 Phase 2 는 "PyBaMM P2D 로 SEV 를 합성" 이고,
`wiki/concepts/zhang2020-eis-aging-dataset.md` 는 이 데이터셋을 그 **실측 대조**
자리에 놓았다. 원전 확인으로 셋이 바뀐다.

## 7.1 "cycle 고정 → state 스윕은 아무도 안 했다" 를 정정한다

우리 위키는 이렇게 적어 두었다: "(b) cycle 고정 → state I~IX 스윕 = SOC 의존성
추적. **아무도 안 했다.**"

**정정**: Zhang 은 state 축을 썼다 — 다만 우리가 상상한 방식은 아니다.
`[도표]` SI Fig. 2 + `[인쇄]` 본문이 보여 주는 것은 **state 마다 독립적인
EIS→용량 모델을 아홉 개 만들고 각각의 R² 를 보고한 것**이다. 즉 state 축은
**복제(replication) 축**으로 쓰였다. 저자들은
(i) **한 사이클 안에서 아홉 스펙트럼을 나란히 비교한 적이 없고**,
(ii) **state 간 차이를 feature 로 쓴 적이 없으며**,
(iii) SOC 라는 말도 state 를 가리킬 때만 쓴다.

→ **우리 아이디어(state 간 대비를 feature 로 쓰기)는 여전히 미개척이다.**
그러나 "아무도 state 축을 건드리지 않았다" 는 틀린 서술이므로 위키에서 고친다.
그리고 Zhang 의 per-state R² 는 우리에게 **공짜 사전정보**다:
state V(0.88) · VII(0.86) · IX(0.81) 이 정보가 많고 **VI(0.28) 은 쓸모없다.**

## 7.2 SOC 축의 실제 해상도 — 설계 제약으로 등록한다

§1.6 에서 확정한 것을 Phase 2 언어로 옮긴다.

- **전류 없는 SOC 는 0 % 와 100 % 두 점뿐**이다 (I·VIII·IX / IV·V).
- 중간 SOC(III ≈40 %, VII ≈57 %)는 **DC 전류가 흐르는 중** 측정 —
  평형 임피던스가 아니다.
- SEV 는 R_ct 의 **stoichiometry 의존성**을 읽는 feature 이므로, 이 데이터로
  얻을 수 있는 것은 **2점 대비**(0 % vs 100 %)이지 곡선이 아니다.

`[해석]` **Phase 2 의 실측 대조는 "SOC 곡선 대조" 가 아니라 "SOC 양 끝점
대비의 셀 간 재현성" 으로 축소된다.** 이것은 나쁜 소식이지만 **정확한** 제약이며,
합성(PyBaMM) 쪽 설계에도 반영된다 — 실측과 비교할 지점을 0 %/100 % 두 곳으로
맞추면 대조가 성립한다.

한편 **새로 열리는 자원**도 있다: state IV vs V, 그리고 VIII vs IX 는
**같은 SOC 에서 휴지 15분 전/후** 쌍이다. 이 쌍의 차이는 SOC 가 아니라
**완화(relaxation)** 만 다르다. `[해석]` 즉 이 데이터셋에는 **SOC 스윕이 아니라
완화 시간 대비**라는, 아무도 안 쓴 축이 하나 더 있다 (Zhang 은 IV/V 와 VIII/IX 를
각각 독립 모델로만 다뤘다).

## 7.3 "SEV 축이 셀 간에 재현되는가" 를 이 데이터로 묻는 법 — 실행 가능해졌다

질문 카드 `wiki/questions/pvs-sev-lli-lampe-separability.md` 는 Su 2024 흡수 후
Phase 2 의 첫 물음을 "SEV 가 모드를 가르는가" 에서 **"SEV 축이 셀 간에
재현되는가"** 로 바꿨다. 원전 확인으로 그 실험이 구체화된다:

1. **동일 조건 8셀**(25C01–25C08)이 있다 — Su 가 쓴 5셀보다 많다.
2. 각 셀에 **state V(100 %, 휴지 후)와 state IX(0 %, 휴지 후)** 의 스펙트럼
   시계열이 있다 → **SOC 양 끝점의 저주파 임피던스 대비**를 셀마다 노화축으로
   추적할 수 있다.
3. 노화 축의 정본 라벨(용량)이 **측정값**으로 함께 있다.
4. 셀 간 EoL 이 12~234 사이클로 흩어져 있으므로 (**§4.1(f)**), "재현되는가" 는
   가혹한 조건에서 검사된다.

`[해석]` 판정 기준도 명확해진다: Su 2024 에서 우리가 발견한 **부호 뒤집힘**
(전하전달 peak 상관이 5셀 중 1셀에서 부호 반전, R_pol 은 2셀)을 **8셀에서 다시
재는 것**이 Phase 2 의 첫 실험이 될 수 있다. 그리고 이번에는 **Su 의 DRT 를
거치지 않고** 원 스펙트럼에서 직접 잴 수 있다 — DRT 정규화 파라미터(λ)가
재현되지 않는 문제(Su digest §2.3)를 우회한다.

## 7.4 우리가 이 논문에 공급할 수 있는 것

`[해석]` 세 가지가 명확하다.

1. **ARD 선택의 비식별성 정량화.** §4.2 에서 52개 예측자가 |r|>0.95 로 거의
   동률임을 보였다. 우리 쪽에서 값이 싼 후속: **부트스트랩/셀 제외 재적합으로
   ARD 가 고르는 예측자 인덱스의 분포**를 내는 것. 만약 셀을 하나 빼면 91번이
   87번이나 95번으로 옮겨간다면, "17.80 Hz 가 계면 물성을 가리킨다" 는 물리
   해석이 무너진다. 이것은 우리 프로젝트의 정확한 장기(degeneracy 진단)이며
   **남의 공개 데이터로 재현 가능**하다.
2. **불확실성 보정 진단.** 이 논문은 ±1σ 를 그렸지만 coverage 를 보고하지
   않았다. `[도표]` Fig. 3a/b 만 봐도 미보정이다. 우리가 라벨 불확실성을
   설계할 때 **coverage 를 필수 산출로 넣는** 근거 사례가 된다.
3. **모드 라벨의 부재를 메우는 쪽.** 이 데이터셋의 최대 결손은 모드 라벨이다.
   우리 합성 truth 파이프라인은 **모드를 알고** 스펙트럼/곡선을 만들 수 있으므로,
   "이 대역의 임피던스 변화가 어느 모드에서 오는가" 를 **강제로 아는** 상태에서
   검사할 수 있다. 실측(Zhang)과 합성(우리)의 역할 분담이 여기서 갈린다.

---

# 8. 한 문단 요약 (마지막에 놓는다)

Zhang 등은 LiCoO₂/graphite **45 mAh Eunicell LR2032 코인셀 12개**를 25/35/45 °C
에서 **1C CC–CV 충전(4.2 V) / 2C CC 방전(3.0 V)** 으로 EoL 까지 돌리고, 짝수
사이클마다 한 사이클 안 **아홉 시점(state I–IX, 그중 넷은 DC 전류 중)** 에서
0.02 Hz–20 kHz **60주파수** EIS 를 재어 2만 스펙트럼 이상을 모았다. 이 스펙트럼
120차원(실·허)을 **전처리 없이** GPR 에 넣어 **용량**(SE-ARD 커널)과
**RUL**(선형 커널)을 예측했고, 셀 단위 분할에서 R² 0.68–0.96 을 얻었으며,
ARD 가 **17.80 Hz 와 2.16 Hz 의 허수부** 두 개만 고른다는 것을 해석으로 제시했다.
**열화 모드는 재지 않는다** — 제목의 "degradation patterns" 는 셀마다 다른 감쇠
궤적을 뜻하고, `LLI`·`LAM`·`half-cell`·`identifiab*`·`degenerac*` 은 본문·SI 에
전부 0회다. 우리 축에서 이 논문의 값어치는 (a) **우리 데이터의 좌표계를 확정해
준 것**(셀 형태·명부·프로토콜·state 정의), (b) **모드 라벨이 없음을 원전에서
확정해 준 것**, (c) **ARD 해석이 공선 대역 안에서 비식별적이라는, 저자 자신의
공개 데이터로 재현되는 반례를 준 것**이다. 반대로 이 논문에서 가져오면 안 되는
것은 SI Table 1 의 기준선 비교(타깃 범위의 2배 RMSE — 망가진 기준선)와
±1σ 음영의 신뢰(보정 검사 없음, Fig. 3 에서 명백히 미보정)다.
