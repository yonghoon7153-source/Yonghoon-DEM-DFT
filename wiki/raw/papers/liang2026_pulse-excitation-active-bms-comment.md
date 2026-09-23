---
title: "Liang, Tao, Shi, Lyu, Ji, Dong, Mo 2026 — Pulse excitation for active battery management systems (npj Clean Energy 2, 16) — Comment"
source_url: local-upload/33._Pulse_excitation_for_active_battery_management_systems.pdf
source_url_note: "5쪽 Comment (본문 pp. 1-4 + 참고문헌 32편 pp. 4-5). **SI 없음 · 데이터 없음** ('No datasets were generated or analysed'). 그림 Fig. 1 한 장 — 크로퍼가 벡터 그림이라 0장 추출, 300 dpi 수동 크롭 1장, **1/1 장 봤다**. 식 0 · 표 0 · 1차 측정 0. 인용 원전 미열람(제목만)."
source_doi: 10.1038/s44406-026-00040-w
source_license: "CC BY-NC-ND 4.0 (The Author(s) 2026)"
pdf_sha256: 30e679dc37e5e7d1233bd48436eb29488522faf1713be1530bbf197e90ced7a4
ingested: 2026-09-23
sha256: 2b88ce8fe53328a44fe72f245714bdd0a9c0cc4ebe6d6901a8d71d7ef984374e
---

# 수집 목적

`assb` 섹션 **34호**, 큐 **33번**. 닻은 `questions/assb-contact-loss-vs-lampe.md` 이고, 큐 문서
(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-d)에는 축이 **"Q4 설계 축 — 우리 폭 측정기의 역방향"** 으로 등록돼 있었다.
들어온 경로는 8호(Li et al. 2026) digest 가 Table 3 의 "active bounded pulse" 채널 원전으로 이 편을 추천한 것인데, 큐 문서가 이미
`[인쇄]` "1 차 측정이 없는 전망 논평이다 … 근거로는 08 번과 같은 급" 이라고 정정해 두었다.

이 digest 의 일 (지시):

1. **펄스 응답(순간 강하 R · 이완 시상수 · 확산 꼬리)이 곱 축퇴 처방의 어느 단계를 온보드로 실현한다고 쓰는가** — 1단계(R·C 분리, 16호),
   4단계(시간 영역 `C = τ/R` 상한 검사, 20호), 31호가 후보로 넣은 `R/k ∝ √D/j₀` 면적 소거 조합. 펄스 한 번으로 `C` 또는 면적 소거 조합을
   얻는다고 쓰는가, 아니면 **R 합만**인가(31호 `R_ICI` 선례).
2. **LLI/LAM 분리(우리 α·β)와의 관계** — 펄스가 OCV 기반 용량 분해(dQ/dV · 전극 정렬)를 대체/보완한다고 주장하는가. 식별성(Q4) 명제.
3. **ASSB 적용** 여부(없으면 도구 칸 — 28·31호 선례) · 32호 "양극성 스택 → 셀별 OCV 못 봄" 과의 관계.
4. 인용 1차 원전에서 칸을 움직일 근거를 찾되 **요약 문장 자체로 칸을 올리지 않는다**. 곱 축퇴 처방 **열일곱 번째 적용**.
5. 큐 낱말 지문을 **NFKC 정규화 후 · 대소문자 구분 · 낱말 경계**로 재집계, 정규화 전후 차이 보고.

> ⚠ **형식 — npj Clean Energy "Comment" 5 쪽(본문 pp. 1–4 + 참고문헌 32 편 pp. 4–5), 1차 측정 0, 식 0, 표 0, 그림 1 장(개념 모식도).**
> `[인쇄]` "Data availability: **No datasets were generated or analysed during the current study.**" 따라서 이 digest 의 `[인쇄]` 는
> 8·10·12·13·32·33호와 같은 뜻 — **"이 지면에 이렇게 적혀 있다"** 이지 "실측됐다" 가 아니다.
> **이 편의 요약 문장은 채움표 칸을 올리지 않는다** — 칸을 움직일 수 있는 것은 1차 원전으로 거슬러 확인된 명제뿐이고, 이 digest 는 1차 원전을
> 열람하지 않았다(참고문헌 제목만 읽었다).
>
> 표기: `[인쇄]` 본문 명시 · `[도표]` 그림에서만 읽은 값 (`figure-read ≈`) · `[재현]` 우리가 지면의 숫자로 계산·대조한 값 ·
> `[해석]` 우리 해석. `[해석]` 표시 없는 문장은 원문이 실제로 말한 것.

# 서지

- Chen Liang¹·⁶, **Shengyu Tao**²·⁶ (교신), Hao Shi¹, **Ziyang Lyu**¹ (교신), JC Ji³, Daoyi Dong⁴, **Huadong Mo**⁵ (교신).
  ¹ UNSW Sydney 수학·통계 · ² **Chalmers** 전기공학 · ³ UTS 기계 · ⁴ UTS Australian AI Institute · ⁵ UNSW Canberra. ⁶ 공동 1저자.
- "Pulse excitation for active battery management systems", ***npj Clean Energy* (2026) 2:16**, `10.1038/s44406-026-00040-w`. **Comment**.
- Received 2026-04-06 · Accepted 2026-06-11. **CC BY-NC-ND 4.0**. 경쟁 이해 "none" 선언.
- 연구비: MSCA-PF BLESS(Tao) · 호주 Economic Accelerator(퇴역 EV 전지 건강 추정) · ACT Energy Innovation Fund · ARC Linkage.
- ⚠ **자기 인용**: 참고문헌 32 편 중 **8 편**에 이 편 저자가 있다(`Tao, S` 6 — refs 14·15·18·19·25·27 · `Liang, C` 2 — refs 4·5) `[재현]`.
  핵심 수치 주장("20 % 이하")의 인용 세 편 중 하나(ref 15)가 Tao 1저자다.

# 원문에 없어서 확인이 필요한 것

- **어떤 데이터도 없다.** 셀 화학 · 펄스 진폭/폭/주기 · 샘플링 주파수 · 모델 · 성능 지표 — 전부 0. `[인쇄]` "No datasets were generated or analysed".
- **이중층 용량 · 시상수 · 이완**이라는 낱말이 없다: `capacitan*` 0 · `double layer` 0 · `time constant` 0 · `relaxation` 0 (본문, 대소문자 무시).
  → 펄스로 `C` 를 얻는다는 명제는 **이 지면에 없다**. 면적 소거 조합(`R·C`, `R/k`)도 없다.
- **식별성을 잰 적이 없다** — FIM · CRLB · D-optimality 를 **처방으로** 인쇄하지만 계산값 0, 조건수 0, 사례 0.
- **LLI · LAM · 열화 모드 분해** 어휘 0 (`LLI` 0 · `LAM` 0 · `degradation mode` 0 · `loss of active material` 0; 유일한 인접 = "active material loss" 1 회, 열화 경로 열거).
- **전고체 0**: `solid-state` 0 · `all-solid` 0 · `ASSB`/`SSB` 0 · `pressure` 0 · `MPa` 0. `solid electrolyte` 1 회는 "solid-electrolyte interphase (SEI)" 의 일부.
- **팩 · 모듈 · 직렬 · 스택** 0 (`pack` 0 · `module` 0 · `series` 0 · `stack` 0) — 펄스를 어디에 걸고 전압을 어디서 재는지 미기재.
- **샘플링 요구** 0 (`sampl*` 본문 0; 참고문헌 제목에만 "10 Hz sampling rate", ref 21).
- 인용 수치 셋("20 % 이하"[15–17] · "2.4 배"[28] · 재구성 EIS/IC[21–24])의 원전은 **열람하지 않았다** — 제목만 대조했다.

# 판정 먼저

| 물음 | 판정 | 한 줄 근거 |
|---|---|---|
| **펄스가 처방 어느 단계를 온보드로 실현하나 (논문 명제)** | **어느 단계도 아니다 — "대역 이름표 셋 + 학습 재구성"** | `[인쇄]` 옴(>10³ Hz) · 계면 분극(10⁰–10³ Hz) · 확산 개시(<10⁻¹ Hz) 세 대역을 **이름으로만** 두고, 값 · `C` · 시상수 · 조합 0. 등가 EIS 는 "deep learning and online identification of equivalent-circuit parameters" 로 **재구성**(refs 21·22). 31호 `R_ICI`(합, 값 있음)보다 **한 층 아래**다 — 값도 없다 |
| **같은 물음 (`[해석]`, 우리 대수)** | **1단계(τ 형) · 4단계 · 31호 `R/k` 가 모두 "한 펄스의 이완" 위에 선다 — ABMS 는 처방의 자연 하드웨어다** | 단일 RC + √t: `τ = R_p·C ∝ c_dl/j₀`(면적 약분) · `C = τ/R_p ∝ A` · `R_p/k ∝ √D/j₀`(면적 약분). ⚠ 조건 넷 — 샘플링(≥ 10/τ) · 2전극 합 · `C ∝ A` 전제(18·19호에서 두 번 깨짐) · √t 창 분리(31호) |
| 펄스가 OCV 용량 분해를 대체/보완한다고 쓰나 | **대체 쪽 — 단 "재구성"으로** | `[인쇄]` IC · DV 는 "lack sufficient information density"(ref 6) → 펄스 응답에서 IC · DV · 등가 EIS 를 **신경망으로 재구성**(refs 23·24). ★ `[인쇄]` 전기화학 불변량 예시에 **"active material stoichiometric limits"** — 우리 α·β 가 푸는 바로 그 양 — 을 넣는다. 근거 0 |
| **Q4 식별성** | **ASSB 0 — 칸 이동 없음 (누적 0.5 = 29호 그대로).** 스물여섯 번째 성질 **"식별성을 입력 설계로 살 수 있는 자원으로 인쇄했다"** | `identifiab*` NFKC 뒤 **3**(정규화 전 **0**) + `unidentifiable` 1 · FIM 2 · CRLB 1 · D-optimality 1 · PE 3 — **위키 전체에서 D-optimality · PE · OED 를 처방으로 인쇄한 첫 편**(`grep`: 기존 digest 에는 Mohtat 2019 의 "`D-optimal` 0회" 기록뿐). 그러나 계산 0 · **구조적 ↔ 실제적 비식별 구분 0** · `[인쇄]` "observability is redefined as a **controllable resource** rather than an intrinsic system constraint" |
| Q2 독립 관측 | **없다** | 1차 측정 0. 제안 채널(펄스)도 모드를 **가르는** 용도로 제시되지 않는다 |
| **ASSB 적용** | **없다 → 도구 칸** (28·31호 선례) | 전고체 어휘 0 · 압력 0. 화학은 일반 "lithium-ion", 복원 사례는 Si 음극(ref 29) · Li 금속(ref 28) |
| 32호 "양극성 스택 → 셀별 OCV 못 봄" | **무관 — 그리고 이름 충돌 하나** | 이 편의 "**bipolar** pulse sequences"(ref 30) 는 **양·음 교대 펄스**이지 32호 Fig. 3 의 **bipolar 적층**이 아니다. 스택/직렬 어휘 0. `[해석]` 펄스는 **입력** 설계이고 32호의 결손은 **출력**(셀별 전압) 관측이라 펄스가 그 결손을 메우지 않는다 |
| 채움표 | **≈16.0 → ≈16.0 (새 칸 0)** | Comment · 1차 측정 0 · ASSB 0 |

# §별 해체

## 초록 (p. 1)

`[인쇄]` "Active battery management systems (ABMS) transform battery diagnostics from passive monitoring to active, information-centric sensing.
By applying active pulse excitations over **millisecond-to-second timescales**, they elicit multi-scale electrochemical responses, enabling efficient,
high information-density feature extraction and **enhanced mechanistic observability**." — "forward-looking perspective" 임을 스스로 밝힌다.

## §1 Transforming battery management from passive monitoring to active sensing (pp. 1–2)

**수동 BMS 의 병목 셋** `[인쇄]`: 낮은 효율(장기 사이클 의존) · 제한된 정확도 · 약한 일반화. 셋 다 "insufficient information acquisition and utilization"
에서 온다고 묶는다.

- **정확도 병목의 제어이론 서술** `[인쇄]`: "reliable online parameter estimation requires the **persistence of excitation (PE)** where the input signals are
  sufficiently rich in frequency to excite all internal dynamics. Under passive conditions, batteries are excited only within narrow operating conditions,
  resulting in low-frequency, narrow-band signals that often fail to satisfy the PE requirement. Consequently, key electrochemical processes remain
  **weakly observable or even unidentifiable**".
- **IC · DV 에 대한 판정** `[인쇄]`: "Consequently, commonly used features, such as incremental capacity (IC) and differential voltage (DV) curves, **lack
  sufficient information density to support high-precision state estimation**⁶." (ref 6 = Kim et al. *Joule* 2026, "anode spatial degradation").
  `[해석]` 우리 α·β 하네스는 **바로 이 곡선들(반쪽전지 OCP → 완전지 OCV 정렬)** 을 입력으로 받는다. 이 편은 그 입력의 정보 부족을 **식별성
  낱말로** 말하는 첫 BMS 쪽 문장이지만, "high-precision state estimation" 의 상태가 SOC/SOH 인지 전극 정렬인지 적지 않는다.
- **고충실 진단의 비용** `[인쇄]`: EIS⁷ · 초음파⁸ · 변형률⁹ · in-situ 센서¹⁰ 는 "richer mechanistic insights but rely on costly instrumentation".
- **펄스의 대역 배정** `[인쇄]` (p. 1, 렌더로 확인 — 텍스트 층은 `10⁻¹` 의 음부호를 잃고 "101Hz" 로 뽑힌다):
  "the **ohmic response (> 10³ Hz)**, **interfacial polarization (10⁰ − 10³ Hz)**, and the **onset of transient diffusion (< 10⁻¹ Hz)**. While full steady-state
  diffusion requires longer observation windows, the transient response within these short windows provides high sensitivity for parameter identification
  and state estimation⁷."
  - `[재현]` 대역 사이 **10⁻¹–10⁰ Hz 한 자릿수가 비어 있다**(어느 과정에도 배정되지 않음).
  - `[재현]` "확산 개시 < 10⁻¹ Hz" 는 주기 ≥ 10 s(`τ = 1/(2πf)` ≥ 1.6 s) — **자기 창 "millisecond-to-second" 의 위 끝 밖**이다. 저자는 "full
    steady-state diffusion" 만 창 밖이라 하고 "onset" 은 창 안이라 쓰는데, 그 onset 의 대역이 창 밖에 적혀 있다(D2).
  - `[해석]` 계면 분극 대역 10⁰–10³ Hz 의 시상수는 ≈0.16 ms–0.16 s — 이것을 시간 영역에서 분해하려면 샘플링이 **수 kHz** 여야 한다. 이 편은 샘플링을
    한 번도 말하지 않는다.
- **OED** `[인쇄]`: "this approach aligns with the principles of **Optimal Experimental Design (OED)**¹¹·¹² … where the excitation signal is numerically
  optimized to maximize the information sensitivity of the system's output with respect to its internal parameters. By framing pulse design as an optimal
  control problem, ABMS **can ensure that the resulting system identification is robust against measurement noise and structural uncertainties**."
  - ⚠ 같은 편 마지막 절은 `[인쇄]` "pulse design **must evolve from empirical templates** toward information-optimal excitation" — 즉 **현재는 경험적
    템플릿**이다. 앞 절의 "can ensure" 는 현재형 능력 서술, 뒤 절은 미래 과제 — 서로 다른 시제(D8).
  - `[해석]` "robust against … **structural** uncertainties" 는 OED 가 주지 않는 것이다 — FIM 기반 설계는 **주어진 모델 구조 안의 국소** 정보량을
    최대화한다. 구조 불확실성(모델이 틀림)과 **구조적 비식별**(모든 입력에서 FIM 특이) 둘 다 FIM 최대화로 풀리지 않는다(아래 §해석 2).
- `[인쇄]` "Fundamentally, it improves state observability and **parameter identifiability through input signal design**".
- 시스템 차원 주장(수명 연장 · 폐기 감소 · 2차 사용) — 수치 0.

## §2 Overcoming long-cycle testing constraints through rapid pulse excitation (p. 3)

- `[인쇄]` 제조 선별 · 온라인 진단 · 2차 사용 분류가 "**tens to hundreds of full charge-discharge cycles** … weeks to months".
- ★ `[인쇄]` 수치 주장 하나: "reducing **lifecycle prediction times to 20% or even less** of conventional methods¹⁵⁻¹⁷, while incurring **negligible energy
  overhead**." — refs 15(Tao 2024, 빠른 펄스 + RF, 재활용 전처리) · 16(Ran 2022, 짧은 펄스 + GPR, 잔존 용량) · 17(Li·Wang·West·Preindl 2022, 펄스 주입 +
  ML). **원전 미열람** — 20 % 가 어느 편의 어느 표에서 오는지 이 지면에서 알 수 없다(G1).
- `[인쇄]` "the true bottleneck of conventional passive BMS is not time itself, but inefficient information acquisition under passive observation."

## §3 Overcoming information-limited accuracy through information reconstruction (p. 3)

- ★ **CRLB 문장** `[인쇄]`: "estimation accuracy is fundamentally bounded not by model capacity alone, but by the information content of observed signals and
  measurement noise¹⁸⁻²⁰. This bound is formally described by the **Cramer-Rao Lower Bound (CRLB), which is the inverse of the Fisher Information Matrix
  (FIM)**." — refs 18(Su·Tao 2026 IC 특징 선택) · 19(**Jiang·Tao·Lee·Moura 2026 *Joule* "Defining an accuracy limit in battery state estimation"**) ·
  20(Su 2025 데이터 충분성).
  - `[해석]` "CRLB = FIM⁻¹" 은 **FIM 이 정칙일 때**만 선다. 구조적 비식별(곱 축퇴)에서는 FIM 이 특이해 역이 없고 하한이 **무한**이다 —
    우리 위키 [[constrained-crb-identifiability]] 의 판정 규칙 1층(이분법)이 바로 그 자리다. 이 편은 그 경우를 말하지 않는다(D5).
- `[인쇄]` "Therefore, increasing data volume or cycling duration does not necessarily translate into higher accuracy. Instead, the objective should be to
  maximize information density within a limited observation time." — ⚠ 같은 문단 앞에서 "the objective should be to maximize information density within
  a limited observation time" 가 **거의 그대로 한 번 더** 나온다(D1).
- ★ **재구성** `[인쇄]`: "Through **deep learning and online identification of equivalent-circuit parameters**, short-duration pulse responses can be
  **reconstructed** into high-level features with explicit physical meaning, including **equivalent EIS**²¹·²², **IC curve**²³·²⁴, and **DV curves**."
  "pulse-based reconstruction enables equivalent mechanistic information to be obtained **within seconds**".
  - refs 21(Tang 2023 *iScience* "Predicting battery impedance spectra from **10-second pulse tests under 10 Hz sampling rate**") · 22(Gao·Onori 2026 LFP
    SOC, 짧은 사인 펄스 EIS) · 23(Gao·Onori 2025 LFP SOC, dQ/dV + 짧은 펄스) · 24(**Li·West·Preindl 2023 *JPS* 580 "Characterizing degradation in
    lithium-ion batteries with pulsing"**).
  - ★ `[해석]` ref 21 의 제목이 적은 **10 Hz 샘플링의 나이퀴스트 한계는 5 Hz** 다. 이 편이 계면 분극에 배정한 10⁰–10³ Hz 중 **5 Hz 위(≈2.3
    자릿수)** 는 그 샘플로는 **관측되지 않는다** — 그 대역의 "등가 EIS" 는 측정이 아니라 **학습된 사상의 사전(prior)** 이 채운다. 이것이 참이면
    재구성 EIS 의 반원에서 읽은 `C` 는 처방 1단계의 **입력이 될 수 없다**(원전 미열람 — 방법 확인 필요, G2).
  - `[인쇄]` "this marks a transition **from model fitting to mechanism-driven information acquisition**".
- `[인쇄]` "observability is redefined as a **controllable resource** rather than an intrinsic system constraint. From a control-theoretic perspective, ABMS
  employs optimal pulse design to ensure the PE, thereby simultaneously enhancing the observability of fast-varying internal states (e.g., **electrode
  overpotentials**) and the **identifiability of previously hidden electrochemical parameters (e.g., kinetic and diffusion constants)**."

## §4 Enabling cross-condition generalization through invariant feature learning (pp. 3–4)

- `[인쇄]` 열화 경로 = "coupled mechanisms such as **lithium plating, solid-electrolyte interphase (SEI) growth, and active material loss**²⁶" — 이 편에서
  LAM 에 가장 가까운 유일한 구절. 모드별 정량 · 분리 0.
- ★★ **"전기화학 불변량"** `[인쇄]`: "high-dimensional pulse responses can be nonlinearly disentangled in latent space²⁷ … This process enables the extraction
  of **electrochemical invariants**, fundamental physical properties such as **reaction kinetic constants, active material stoichiometric limits, and
  interface charge-transfer parameters that remain constant across varying operating regimes**." — 반대편에 "transient, condition-dependent signals (e.g.,
  **temperature-sensitive voltage or resistance**)".
  - ★★ `[해석]` **"active material stoichiometric limits" 는 우리 α·β 가 푸는 양이다** — 전극 정렬(각 전극이 사용하는 화학량론 구간의 양 끝)은
    `LLI` 와 `LAM_PE`·`LAM_NE` 가 **움직이는** 바로 그 좌표다. 그런데 `[도표]` Fig. 1b 는 불변 사상의 **"Different domains"** 로 **Temperature · Rate ·
    Degradation** 세 아이콘을 둔다 ⇒ 이 편의 틀에서 화학량론 한계는 **열화 도메인에 대해 불변이어야 할 특징**이면서 동시에 **열화가 바꾸는
    양**이다 — 자기 긴장(D3). 본문 문장은 "operating regimes" 에 대한 불변이라 열화를 뺀 해석도 가능하지만, 그림은 열화를 도메인에 넣는다.
  - ★ `[해석]` 그리고 화학량론 한계는 **ms–s 펄스 한 번이 지나가는 SOC 구간(≈0)** 에서 관측되는 양이 아니다 — 한계는 전 구간 곡선의 **양 끝**
    이다. 펄스 응답에서 그것을 얻는다면 학습 사상이 SOC–응답 관계를 **사전으로** 들고 있어야 한다. 이 편은 이것을 말하지 않는다.
  - `[해석]` "reaction kinetic constants … remain constant" 와 "temperature-sensitive … resistance" 의 대비: 속도 상수는 온도의 함수(Arrhenius)이므로
    불변량은 상수가 아니라 `Ea` 여야 한다 — 이 편은 `Arrhenius` 0 회.
- **UQ** `[인쇄]`: "models learn conditional probability distributions rather than point estimates … Bayesian Neural Networks, Gaussian Process Regression,
  or Evidential Deep Learning to distinguish between **aleatoric** … and **epistemic uncertainty** … By employing **inverse UQ**, ABMS can propagate observed
  response variances back to the underlying electrochemical invariants, providing a **probabilistic confidence interval rather than a deterministic value**."
  - `[해석]` 방향은 우리 요구서의 "LAM 분할은 점추정이 아니라 폭과 함께" 와 **같다**. 그러나 **비식별 파라미터의 사후 분포는 사전이 정한다** —
    곱 축퇴 방향에서 BNN/GPR 의 신뢰구간은 좁게 나올 수도 있다(사전·정규화가 방향을 고정). 역 UQ 가 식별성 진단을 대신하지 않는다 — 우리
    근최적 폭 측정([[near-optimal-set-width-measurement]])은 **사전 없이** 그 방향의 폭을 잰다.

## §5 The mechanism of diagnosis-restoration synergy (p. 4)

- `[인쇄]` "high-frequency pulse signals have been shown to regulate lithium-ion concentration gradients and stabilize the SEI, preventing the localized
  overpotential that triggers lithium plating²⁸. This active intervention prevents the localized overpotential that triggers detrimental lithium plating,
  **extending the cell lifetime by over 2.4 times** compared to conventional methods." — 같은 내용 두 문장 반복(D1). ref 28 = Li·Tan·Li·Lu·He 2017
  *Sci. Adv.* "…pulse current charging for stable **lithium-metal** batteries". `[해석]` 제목상 Li 금속 음극 논문인데 본문은 흑연 Li 이온의 "lithium
  plating" 방지 어휘로 옮긴다 — Li 금속에서 도금은 정상 반응이다. 2.4 배의 조건은 미열람(D6 · G3).
- ★ `[인쇄]` "specific transient voltage pulses can even facilitate **capacity recovery in silicon-anode batteries** by modulating the mechanical stress and
  **interfacial contact of active materials**²⁹." — ref 29 = **Yang et al. 2024 *Science* 386, 322–327**. 이 편 본문에서 `contact` 가 나오는 **유일한 곳**.
  - `[해석]` 카드 물음으로: **"접촉을 되돌리는 조작 → 용량 회복"** 은 4호(Shi 2020) 300 MPa 재가압과 **같은 부류의 분리 시험**(되돌릴 수 있으면 물질은
    그대로)이다. 이 편은 그 해석을 하지 않고, 원전은 **액체 Si 음극**이다 — 양극 · 고체 쪽 1차 근거가 아니다. 후속 후보로만 둔다.
- `[인쇄]` "the ABMS evolves into a **battery therapist**".

## §6 Active battery management systems with high information density and enhanced observability (p. 4)

과제 셋 `[인쇄]`:
1. "pulse design must evolve from empirical templates toward information-optimal excitation strategies rooted in OED principles. Adaptive pulse protocols
   should be numerically optimized, utilizing criteria such as the **FIM or D-optimality**, to jointly tune amplitude, duration, and sequence structure. This
   optimization ensures **maximum parameter identifiability across various chemistries and aging stages** while maintaining safety boundaries." — 바로 뒤에
   "Adaptive pulse protocols, exemplified by **bipolar pulse sequences**³⁰, that jointly optimize amplitude, duration, and sequence structure are needed …"
   가 같은 내용을 되풀이(D1). ref 30 = Li·Berecibar·Preindl 2024 *IEEE TIE* "Nonlinear Characterization … With **Bipolar Pulsing**".
2. ★ "**explicit mappings between pulse responses and electrochemical subprocesses must be established**. Bridging transient features with diffusion kinetics,
   interfacial reactions, and phase transitions will transform pulse excitation from heuristic diagnostics into physics-grounded sensing" — `[해석]` **저자
   스스로 펄스 특징 ↔ 하위 과정 사상이 아직 없다고 인쇄한다.** 판정 표 첫 줄("어느 단계도 아니다")의 가장 직접적 근거.
3. 복원 프로토콜은 "remains in its infancy".

"pulse-sensing-inference-control-feedback" 틀 · 스마트 충전³² · V2G("energy transfer itself serves as a high-bandwidth information channel"). 새 수치 0.

## 그림 — Fig. 1 (p. 2, 유일한 그림)

크로퍼가 벡터 그림이라 영역을 못 잡아(0 장 추출) **300 dpi 수동 크롭** `fig_1_manual_p2.png`. **1/1 장 봤다.**

- **1a** `[도표]` 수동 BMS(Voltage · Current · Temperature 파형, "Passive listening", "**Days-Weeks**") → "System observability · Upgrade" → 능동 BMS(펄스 →
  Current/Voltage 계단 파형 → "Feature" → "Mechanism" 아이콘, "**Milliseconds-Seconds**"). ★ Mechanism 아이콘에 **"Inactive Li"** 와 "Li+" 라벨 —
  본문 `inactive` 0 · `dead` 0. 그림 속 펄스 열은 **양·음 교대**(bipolar pulse) 모양.
  ⚠ 본문은 수동 진단 기간을 "weeks to months" 로 쓰고 그림은 "Days-Weeks"(D7).
- **1b** `[도표]` 세 칸 — Temporal efficiency("Long-term cycling · Weeks" → "Rapid pulse excitation · Seconds") · **Information-rich accuracy**("Transient
  response" 전압–시간 → **Neural network** → "Reconstructed features" = **EIS** 곡선 + **IC** 곡선) · Cross domain generalization("Different domains":
  **Temperature · Rate · Degradation** → "Invariant features"). ★ 재구성 화살표가 **신경망 하나를 지난다** — 그림 수준에서 재구성은 학습 사상이다.
- **1c** `[도표]` "Adaptive pulse design"(Amplitude · Duration · Sequence) · ★ "**Physical-consistent mapping**" = 단일 펄스 전압 응답 모식도: 전류
  계단에서 **수직 점프**(라벨 "Ohmic resistance"), 이어지는 **휘어진 상승**(점 마커, 라벨 "Interfacial polarization" 은 시간축 위), 펄스 끝의 수직
  하강 뒤 **감쇠 꼬리**(라벨 "Diffusion"). 축 눈금 · 값 · 시상수 표시 0 · **`C` 표시 0**. · "Diagnosis-**regulation** synergy"(Unhealthy → Healthy).
  하단 폐루프 Pulse → Sensing → Inference → Control → Feedback · Smart charging ↔ V2G.
  ⚠ 그림 라벨 "Physical-consistent mapping" · "Diagnosis-regulation synergy" ↔ 캡션 "physics-consistent mapping" · "diagnosis-restoration synergy"(D4).
- `[해석]` 1c 의 모식도가 이 편에서 **처방에 가장 가까운 지면**이다 — 순간 강하(`R₀`) · 이완(`R_p`, τ) · 꼬리(√t, `k`) 세 성분을 **한 펄스 위에
  그렸다.** 20호(Chang 2020)의 3시상수 분해(`R₀`·`R_ct`·`R_p`)와 같은 모양이고, 31호 ICI 의 `R`·`k` 를 품는다. 그러나 **값 · 시상수 · 조합은 그리지
  않았다.**

# `[해석]` 1 — 한 펄스의 이완에서 처방 단계가 어떻게 서는가 (우리 대수, 원문 명제 아님)

단일 RC(계면) + 옴 + 반무한 확산 근사, 전류 계단 `I`:

```
V(t) − V₀ ≈ I·[ R₀ + R_p·(1 − e^{−t/τ}) ] + I·k·√t        (펄스 중)
R_p ∝ 1/(A·j₀)     C = c_dl·A     ⇒  τ = R_p·C ∝ c_dl/j₀        (A 약분)
                                     C = τ/R_p ∝ A              (면적 서명)
k ∝ 1/(A·√D)  (31호 식 19 구조)   ⇒  R_p/k ∝ √D/j₀              (A 약분 — 31호 후보)
```

| 처방 단계 | 한 펄스에서 필요한 것 | 이 편 | 온보드 조건 (`[해석]`) |
|---|---|---|---|
| **1단계** (16호 `R·C`; 21호 τ 형) | `R_p` 와 τ(또는 `C`) | 대역 이름 "interfacial polarization" 만, τ · `C` 0 | τ 가 샘플 간격의 수 배 이상. 10⁰–10³ Hz 대역 τ ≈0.16 ms–0.16 s ⇒ **kHz 급 샘플링**. ref 21 형 10 Hz 로는 τ ≳ 1 s 인 호만 |
| **2단계** (18·25호) | + 면적을 아는 대조군 | 0 | 온보드에서는 **같은 셀의 신품 기준**이 유일한 대조군 후보 — 면적이 알려진 것이 아니라 **변화분**만 |
| **3단계-a** (19호 `Ea`) | 여러 온도의 `R(T)` | **반대 방향** — 온도 의존을 "transient, condition-dependent" 로 **지울 대상**에 둔다(불변 사상) | 운전 온도 분포 위의 펄스 `R` 을 모으면 `Ea` 가 공짜로 나온다 — **불변 학습이 그 채널을 버린다** |
| **3단계-b** (19호 `C` 상한) · **4단계** (20호 `C = τ/R`) | τ, `R_p` 로 `C` 를 만들어 상한 검사 | 0 | 펄스는 4단계의 **본래 영역**(시간 영역). 20·21호처럼 "전하이동" 호가 상한을 넘으면 그 성분은 이중층이 아니다 |
| **31호 `R/k`** | 같은 펄스의 `R_p` 와 √t 기울기 `k` | "onset of transient diffusion" 대역 이름만 | 31호는 1–5 s 차단에서 `k` 를 뽑았다 — "ms–s" 창 안. ⚠ 이 편은 그 대역을 **<10⁻¹ Hz(≥10 s)** 에 적는다(D2). √t 창이 RC 와 분리돼야(31호 실패 조건) |

**조건이 셋 더 있다** (`[해석]`):
- ★ **2전극 합** — BMS 는 셀 단자 전압만 본다. `R₀` · `R_p` · τ 는 양극 + 음극(+ ASSB 면 SE 입계) 호의 **합**이다. 17·20·25호가 ASSB 에서 **상대극 기여가
  양극과 같은 자릿수이거나 더 클 수 있다**는 것을 보였다(17호 겉보기 `LAM_PE` = 상대극 · 20호 상대극이 용량을 끊음 · 25호 자기 적합에서 전압 하강 ≈80 % Li 계면) — 단자 펄스의 "계면 분극" 을 양극 접촉에 배정할 근거가 없다(Q5 의 펄스 판).
- ★ **`C ∝ A` 전제** — 18·19호에서 두 번 깨졌다(처방 3단계-b). 펄스가 `C` 를 줘도 전제 검사 없이는 면적이 아니다.
- **"재구성" 경로는 처방 입력이 아니다** — 이 편이 권하는 경로(펄스 → 신경망 → 등가 EIS)에서 나온 `C` 는 학습 사상의 출력이다. 처방이 요구하는
  것은 **적합된 `τ` 와 `R`** 이지 재구성된 반원이 아니다.

# `[해석]` 2 — OED 는 우리 폭 측정기의 역방향이다, 단 구조적 축퇴 앞에서는 멈춘다

큐가 적은 "우리 폭 측정기의 역방향" 은 맞다: 근최적 폭 측정([[near-optimal-set-width-measurement]])은 **주어진 데이터가 못 정하는 방향의 폭**을 재고,
OED 는 **그 폭이 줄도록 입력을 고른다**. 둘은 한 쌍이다. 그러나:

- **D-optimality 는 `det FIM(u)` 를 입력 `u` 에 대해 최대화한다.** 모델 출력이 두 파라미터에 **곱으로만** 의존하면(`y(u; A·j₀)`) 모든 `u` 에서 FIM 이
  특이하고 `det = 0` 이다 — **어떤 펄스도 그 곱을 가르지 못한다.** 곱을 가르는 것은 입력의 풍부함이 아니라 **모델 구조에 곱과 다르게 반응하는
  항(`C_dl ∝ A`)이 있고, 그 항이 보이는 대역을 샘플링하는 것**이다. 즉 이 편의 "PE 를 만족시키면 식별된다" 는 **실제적 비식별**(정보가 약함)에만
  맞고 **구조적 비식별**(정보가 0)에는 틀리다. 이 편은 둘을 가르지 않는다.
- **FIM 은 국소량이다.** 설계점 근방의 곡률로 입력을 고르므로, 다봉 · 평탄 계곡의 폭은 **설계 뒤에 전역으로 다시 재야** 한다 — 우리 폭 측정기가
  OED 의 **사후 검증**이 된다.
- 액체셀 계보는 이미 같은 도구를 **OCV 창 선택**에 썼다: Lin 2024(`raw/papers/lin2024_ocv-degradation-mode-identifiability.md`, "Informative SOC
  windows … by Fisher information") · Mohtat 2019(FIM → 제약 CRB). 이 편은 같은 도구를 **펄스 입력**에 처방한다 — 대상이 OCV 에서 과도 응답으로
  옮겨 간 판이다. ⚠ 이 편은 둘 다 인용하지 않는다.

# 어휘 집계 — NFKC 정규화 후, 대소문자 구분, 낱말 경계 (본문 pp. 1–4 캡션 포함, 참고문헌 열 병기)

**정규화 전후 차이**: NFKC 가 바꾼 문자 **76 자** — 합자 `ﬁ` **67** · `ﬂ` 6 · `…` 2 · 비분리 하이픈 `‑` 1.
★★ **이 편에서는 합자가 큐 지문 열 둘을 가린다** — 33호(Zhang)와 반대 결과다:

| 큐 지문 열 | 큐 값 | 재집계 (NFKC · 대소문자 구분 · 낱말) | 정규화 전 | 판정 |
|---|---:|---:|---:|---|
| `identifiab` | 0 | **3** (낱말 시작 경계; + 줄끝 하이픈 분절 "iden-/tiﬁability" 1 → **4**; + 낱말 안 "unidentiﬁable" 1) | **0** | ❌ **큐 값 틀림 — 합자 `ﬁ`** |
| `uncertaint` | 3 | **3** (대문자 "Uncertainty Quantification" 포함하면 4) | 3 | ✓ |
| `confidence interval` | 0 | **1** ("probabilistic conﬁdence interval", p. 3–4) | **0** | ❌ **큐 값 틀림 — 합자 `ﬁ`** |
| `Bayes` | 1 | **1** ("Bayesian Neural Networks") | 1 | ✓ |
| `posterior` | 0 | **0** | 0 | ✓ |
| `calibrat` | 0 | **0** | 0 | ✓ |
| `LLI` | 0 | **0** | 0 | ✓ |
| `LAM` / `loss of active material` | 0 | **0** (인접 변형 "active material loss" **1** — 열화 경로 열거) | 0 | ✓ |
| `degradation mode` | 0 | **0** | 0 | ✓ |
| `contact loss` | 0 | **0** (`contact` 1 — "interfacial contact of active materials", ref 29 Si 음극) | 0 | ✓ |
| `MPa` | 0 | **0** | 0 | ✓ |

**큐 지문 11 열 중 9 열 일치 · 2 열 불일치(`identifiab` 0 → 3, `confidence interval` 0 → 1)** — 둘 다 **정규화 전 원시 텍스트 층에서 세면 0** 이 나오는
합자 가림이다. 큐 문서의 `[인쇄]` "**`identifiab` 은 다섯 편 전부 0 회**" 는 이 편에 대해 **틀리다**.
`[재현]` 같은 검사를 큐 31·32·34·35 원본 PDF 에 걸어 보면 `identifiab` 은 넷 다 전후 0 → 0 이고, **35 번은 `confidence interval` 0 → 6** 이다
(34 번 본문 10 → 10 · 35 번 `calibrat` 7 → 7). ⇒ 큐 지문 표의 35 번 행도 합자에 가려져 있다 — 35 번 digest 에서 재집계할 것.

큐의 보조 검사 "`Cramér`/`Fisher` 는 33 번만 2 회" — **일치**(`Cramer` 1 · `Fisher` 1; 원문 표기는 악센트 없는 "Cramer-Rao").

추가 열 (본문, NFKC · 대소문자 구분, 괄호는 대소문자 무시): `observab*` **12** · `identif*` 9(+ 하이픈 분절 1) · `unidentifiab*` 1 · `FIM` 2 · `CRLB` 1 · `OED` 2 ·
`D-optimal*` 1 · `persistence of excitation` 1 · `PE` 3 · `pulse*`(49) · `information`(42) · `invarian*`(10) · `EIS` 3 · `IC` 4 · `DV` 2 · `incremental capacity` 1 ·
`differential voltage` 1 · `stoichiometr*` 1 · `ohmic`(2) · `diffusion`(5) · `overpotential`(3) · `resistance`(2) · `impedance`(1) · `kinetic`(3) · `charge-transfer`(1) ·
`equivalent`(4) · `ECM` 1 · `neural`(3) · `generative`(1) · `temperature`(7) · `safety`(5) · `noise`(3) · `lithium plating`(3) · `SEI` 2 · `SOH` 1 · `SOC` 1 ·
`capacitan*`(**0**) · `double layer`(**0**) · `time constant`(**0**) · `relaxation`(**0**) · `DRT` 0 · `OCV` **0** · `open circuit`(0) · `half-cell`(0) · `cathode`(0) ·
`anode`(1) · `electrode`(1) · `solid-state`(**0**) · `all-solid`(0) · `pressure`(**0**) · `stack`(0) · `pack`(0) · `module`(0) · `series`(0) · `balanc*`(0) ·
`area`(0) · `sampl*`(0) · `Arrhenius` 0 · `uniqu*`(0) · `inactive`(0) · `dead`(0) · `bipolar`(1) · `silicon`(1) · `structural`(1).

`[해석]` 본문 ≈4 쪽에 **`observab*` 12 · `identif*` 10** 인데, 그 옆에 `capacitan*` · `time constant` ·
`relaxation` · `OCV` · `area` 가 **전부 0** 이다 — **식별성을 목표로 말하면서 그것을 줄 물리량의 이름이 없다.**

# Q1~Q8 판정 (닻 페이지 수집 지침)

| Q | 판정 | 근거 |
|---|---|---|
| **Q1** 접촉 손실 정량 | **없다 — `θ(N)` 0/34** | `contact` 1 회(ref 29 Si 음극 복원), 복합양극 · `θ` 자리 0 |
| **Q2** 독립 관측 | **없다** | 1차 측정 0. 펄스 채널은 **제안**이고 모드를 **가르는** 용도로 쓰이지 않는다. `[해석]` ref 29 형 "접촉 복원 펄스 → 용량 회복" 은 4호 재가압과 같은 부류의 **조작** 후보(액체 Si) |
| **Q3** 라벨 층위 | 칸 없음 · **층 하나 (제안형): "learned-reconstruction features"** | IC · DV · 등가 EIS 를 **신경망 재구성**으로 얻어 진단 입력으로 쓰자는 처방 — 그 위에서 적합한 라벨은 fitted-on-reconstructed 가 된다. + `[인쇄]` 역 UQ 로 "probabilistic confidence interval rather than a deterministic value" — **요구만**, 사례 0 |
| **Q4** 유일성·식별성 | **ASSB 0 — 칸 이동 없음 (누적 0.5).** **스물여섯 번째 성질 "식별성을 입력 설계로 살 수 있는 자원으로 인쇄했다"** | `identifiab*` 3–4(NFKC) · FIM · CRLB · D-optimality · PE — 계보에서 **처방 도구가 가장 완비된 어휘**. 그러나 ① 계산 0 ② **구조적 ↔ 실제적 비식별 구분 0**("CRLB = FIM⁻¹" — 특이 FIM 무언급) ③ `[인쇄]` "observability is redefined as a controllable resource" ④ `[인쇄]` "explicit mappings between pulse responses and electrochemical subprocesses **must be established**" — 사상이 아직 없다고 스스로 적는다. 8호(`identifiab*` 5 · "Unidentifiable pulse response" 를 **실패 모드**로)와 **반대 방향** — 8호는 펄스 응답이 비식별일 수 있다고, 이 편은 펄스가 식별성을 만든다고 |
| **Q5** Li-In 기준 전위 | **해당 없음** (Li-In · 기준극 0) — `[해석]` 펄스 판 경고 하나: 단자 펄스의 분극은 상대극 호를 품는다(17·20·25호) |
| **Q6** 압력 | **없다** (`pressure` 0 · `MPa` 0) |
| **Q7** dead Li | **해당 없음** — `[도표]` Fig. 1a 아이콘 "Inactive Li" 뿐, 본문 `inactive`·`dead` 0 |
| **Q8** 화학·OCP | **없다** — 화학 미지정 "lithium-ion", OCV 0 회. 참고문헌 제목에 LFP 2(refs 22·23) |

# 곱 축퇴 처방 — 열일곱 번째 적용

**적용 불가 — 데이터 0.** 그러나 32 · 33호의 "대상 없음" 과 성질이 다르다: 이 편은 **처방이 서는 입력(한 펄스의 이완)을 온보드 채널로 제안**하고,
동시에 그 채널에서 처방 입력을 **지우는 두 설계 선택**을 권한다 (`[해석]`):
1. **재구성 경로** — 펄스 → 신경망 → 등가 EIS. 1단계가 요구하는 것은 **적합된** `R_p` · τ 이지 재구성된 반원이 아니다. 저샘플링(ref 21 제목 10 Hz)이면
   계면 대역의 대부분이 **사전**에서 온다.
2. **불변 학습** — 온도를 "condition-dependent signal" 로 지운다. 3단계-a(`Ea`, 면적 불변 채널)는 **바로 그 온도 의존**에서 나온다.

→ 처방 표(`concepts/assb-lampe-contact-product-degeneracy.md`)에 **"한 펄스 이완 = 1·4단계 + `R/k` 의 공통 입력"** 을 온보드 번역으로 적는다.

# 어긋남 · 공백

- **D1 반복 문장 셋** — "the objective should be to maximize information density within a limited observation time"(p. 3, 한 문단 안 2 회) ·
  "prevent(s/ing) the localized overpotential that triggers (detrimental) lithium plating"(p. 4, 연속 2 문장) · "Adaptive pulse protocols … jointly (tune/optimize)
  amplitude, duration, and sequence structure"(p. 4, 연속 2 문장). 편집 잔재.
- **D2 대역 ↔ 창** — "onset of transient diffusion (< 10⁻¹ Hz)" 는 주기 ≥ 10 s 로 "millisecond-to-second" 창 밖. 10⁻¹–10⁰ Hz 무배정. (텍스트 층에서
  `10⁻¹` 의 음부호가 빠져 "101Hz" 로 추출된다 — 기계 판독 주의.)
- **D3 불변량 ↔ 열화 도메인** — "active material stoichiometric limits" 를 불변량으로 두면서 Fig. 1b 는 Degradation 을 불변 사상의 도메인으로 둔다.
- **D4 그림 ↔ 캡션 라벨** — "Physical-consistent mapping" ↔ "physics-consistent mapping" · "Diagnosis-regulation synergy" ↔ "diagnosis-restoration synergy".
- **D5 CRLB 정의** — "CRLB, which is the inverse of the FIM" — 정칙 FIM · 비편향 추정량 조건 무언급. 특이 FIM(구조적 비식별)에서는 성립하지 않는다.
- **D6 ref 28 문맥** — Li 금속 펄스 충전 논문(제목)을 Li 이온 "lithium plating 방지 · 수명 2.4 배" 로 인용. 원전 미열람.
- **D7 기간 표기** — 본문 "weeks to months" ↔ Fig. 1a "Days-Weeks".
- **D8 시제** — p. 1 OED 로 "can ensure … robust" (현재 능력) ↔ p. 4 "must evolve from empirical templates" (미래 과제).
- **G1** "20 % or even less"(refs 15–17) 원전 미열람 — 셋 중 하나가 저자 1저자. **G2** ref 21 의 재구성 방법(샘플링 · 대역 · 사전) 미열람.
  **G3** ref 28 의 2.4 배 조건 미열람. **G4** ref 24("Characterizing degradation … with pulsing") 가 모드 분해를 하는지 미확인.

# 우리 프로젝트와의 접점

- **α·β 하네스(`bms-balancing/`)** — 입력이 반쪽전지 OCP + 완전지 OCV 곡선이다. 이 편은 그 입력을 "정보 밀도 부족"(ref 6)으로 판정하고 펄스 재구성
  IC/DV 로 **대체**를 권한다. `[해석]` 재구성 곡선을 α·β 에 넣으면 폭 측정에 **재구성 불확실성**이 한 항 더 붙는다 — 하네스가 지금 재는 폭은 그 항을
  0 으로 둔 **하한**이 된다. 그리고 화학량론 한계(= α·β 가 푸는 양)를 펄스 불변량으로 뽑는다는 명제는 근거 0.
- **degradation-degeneracy (22p 물음)** — 이 편은 모드 분해를 하지 않는다. `[해석]` OED 로 **실제적** 비식별(LAM_PE ↔ LAM_NE 가 약하게 갈리는 경우)은
  줄일 여지가 있고, **구조적** 비식별(`LAM_NE ↔ γ_Si` 류)은 입력 설계로 안 풀린다 — 이 둘을 가르는 것이 우리 폭 측정의 몫이다. 수치의 정본은
  `degradation-degeneracy/docs/RESULTS*.md` 이고 여기 복사하지 않는다.
- **공급할 수 있는 것** — ① "펄스 대역별로 어느 파라미터 조합이 **구조적으로** 비식별인가" 의 목록(곱 축퇴 페이지의 약분표) ② OED 설계 뒤 **전역 폭**
  사후 검증.

# 후속 (인용 원전 — 제목 기준, 미열람)

| 서지 | ref | 왜 | 축 |
|---|---|---|---|
| Jiang, Tao, Lee, Moura 2026 *Joule* 10, 102342 "Defining an accuracy limit in battery state estimation" | 19 | CRLB 로 상태 추정 정확도 한계를 **정의** — Q4 도구 원전 후보(액체 가능성 높음) | Q4 |
| Li, West, Preindl 2023 *J. Power Sources* 580, 233328 "Characterizing degradation in lithium-ion batteries with pulsing" | 24 | 펄스 → 열화 특성화 — 모드 분해 여부 확인 필요 | Q2·Q4 |
| Tang et al. 2023 *iScience* 26, 106821 "Predicting battery impedance spectra from 10-second pulse tests under 10 Hz sampling rate" | 21 | 재구성 EIS 의 대역 · 사전 의존 — 1단계 `C` 가 측정인가 | 처방 1단계 |
| Yang et al. 2024 *Science* 386, 322–327 "Capacity recovery by transient voltage pulse in silicon-anode batteries" | 29 | **접촉 복원 조작 → 용량 회복** — 4호 재가압과 같은 부류(액체 Si) | Q2 조작 |
| Tao et al. 2025 *EES* 18, 1544 "Non-destructive degradation pattern decoupling … physics-informed learning" | 14 | "degradation pattern decoupling" — 모드 분해인지 확인 | Q2·Q3 |
| Li, Berecibar, Preindl 2024 *IEEE TIE* 71, 12983 "Nonlinear Characterization … With Bipolar Pulsing" | 30 | 비선형(진폭 의존) 펄스 — `j₀` 를 BV 비선형으로 떼는 채널 후보 | 처방 |
| Kim et al. 2026 *Joule* 102343 "anode spatial degradation" | 6 | "IC/DV 정보 부족" 판정의 원전 | α·β 입력 |
| Zhou et al. 2025 *Joule* 9, 102099 "Batch diagnosis of batteries within one second" | 7 | 1 초 진단 — 무엇을 식별하나 | Q4 |
