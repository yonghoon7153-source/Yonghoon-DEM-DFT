---
title: "Sun, Xiong, Wang, Li, Sun 2025 — A deep learning approach for enhanced degradation diagnostics of NMC lithium-ion batteries via impedance spectra (J. Energy Chem. 107, 894–907)"
source_url: local-upload/3._A_deep_learning_approach_for_enhanced_degradation_diagnostics_of_NMC_lithium-ion_batteries_via_impedance_spectra.pdf + 3._Sup_A_deep_learning_approach_for_enhanced_degradation_diagnostics_of_NMC_lithium-ion_batteries_via_impedance_spectra.pdf
source_url_note: "본문 14 쪽 (그림 12 · 표 2 · 식 18 · 참고문헌 [1]–[37]) + SI 5 쪽 (Supplementary Note 1–6 · 표 S1–S2 · 그림 S1–S6 · 참고문헌 R1; Word 변환판, PDF 작성 2026-10-02). 2026-10-02 논문 세미나 3번째 논문 (사용자 공급) · assb 아님 (액체 NMC/graphite). 크로핑 자동 21 + 수동 5 = 26, 전부 봄. 본문 그림은 벡터라 판독은 벡터 좌표 (도표·벡터 표기)."
source_doi: 10.1016/j.jechem.2025.05.014
source_license: "© 2025 Science Press and Dalian Institute of Chemical Physics, Chinese Academy of Sciences. Published by Elsevier B.V. and Science Press. All rights are reserved, including those for text and data mining, AI training, and similar technologies. — CC 아님"
pdf_sha256: 7b80ada48e9a92a29abfee889ec805805475acdd7635c02b866aaf35a9b64967
si_sha256: 5987ae8be8448339020a92c184d3656ba0162c29299843f437c25fd24b1bfc90
ingested: 2026-10-02
sha256: 1ba7f1194fbeda84872550e8729af6dd109b8728c2b25a491ffa0d4e686f789d
---

# 수집 목적

Yue Sun, Rui Xiong (교신), Peng Wang, Hailong Li, Fengchun Sun, **"A deep learning approach
for enhanced degradation diagnostics of NMC lithium-ion batteries via impedance spectra"**,
*Journal of Energy Chemistry* **107** (2025) 894–907 (특집 'AI4Batteries') 와 그 보충자료(SI
5 쪽)의 **절별 해체분석**.

**2026-10-02 논문 세미나의 3번째 논문** (사용자 공급, 업로드 파일명 번호 "3"). ⚠ **`assb`
논문이 아니다** — 액체 전해질 NMC/graphite 셀(형식은 PDF 에 없다, G1)의 열화 모드 진단
논문이다. 그래서 `assb` 번호 · 태그 · 채움표를 쓰지 않고, 2026-09-03 ~ 09-11 에 흡수한 액체셀
열화 모드 계열(Birkl 2017 · Dubarry 2012 · Lin 2024 · Mohtat 2019 · Wang (Xiong) 2025 ·
Cui 2026 · Zhang 2020 · Su 2024 …)과 같은 자리에 둔다.

사용자의 물음 (그대로): "이건 3번쨰논문이고 우리 열화 정량화랑 많이 맞는거 같은데
차근차근 정리해주고 다되면 나한테 브리핑해줘 / 관련해서 우리꺼에 적용가능한지 /
누락된 논문있음 얘기해줘". 그래서 이 digest 는 일반 절별 해체에 더해 **§17 "우리 열화
정량화(α·β 창 맞춤 → LLI/LAM_PE/LAM_NE)에 적용 가능한가"** 와 **§19 "누락된 논문 — 후속
후보 표"** 를 별도 절로 둔다.

이 저장소가 이 편을 흡수하는 이유는 셋이다.

1. **`mode-observability` Phase 3 의 구조를 그대로 가진 실셀 사례다.** Phase 3 은 "fitted
   라벨로 학습한 모드 예측 ML 이 라벨의 비식별성을 어떻게 물려받는가" 를 묻는다
   (`mode-observability/README.md` Phases 표). 이 편은 **반쪽전지 OCP 창 맞춤으로 만든
   LLI/LAM_PE/LAM_NE 라벨**(= 적합값)을 "ground truth" 로 쓰고, **P2D 임피던스 시뮬레이션
   1,000 개로 사전학습**한 뒤 실험 자료로 미세조정한다 — [[piml-physics-injection-points]]
   의 ⑤(학습 데이터) + ⑥(라벨 그 자체) 가 동시에 들어 있다.
2. **"EIS 를 더하면 모드가 갈리는가" 의 실셀 시험대로 보인다** — 그러나 §9 에서 보이듯
   이 편의 주의(attention) 결과는 LLI 와 LAM_PE 에 대해 **한 패턴의 부호 반전**이고
   (`[재현·벡터]` r = −0.962), LAM_PE 와 LAM_NE 는 **같은 대역**에 앉는다. 이 편은
   [[pvs-sev-lli-lampe-separability]] 의 "관측을 늘리면 갈리는가" 질문에 **분리의 근거가
   아니라 상관 학습의 사례**로 들어온다.
3. **라벨 맞춤이 우리 α·β 창 맞춤과 거의 같은 대수다** — 창 좌표 4 개(`p0, n0, Q_PE,
   Q_NE`) + 상수 저항 `R` 하나. 다른 점은 관측이 **pOCV 가 아니라 사이클 전류(1·2 C) CC
   충전 곡선**이라는 것이다. 우리 합성 truth 격자 · null 방향 진단을 이 5-매개 맞춤에
   걸면 **이 편 라벨 오차의 방향**이 나온다 — 우리가 이 편에 공급할 수 있는 것이다
   (§17).

그림은 PDF 가 **벡터 그래픽**이라(본문 3·6·9·10·11 쪽 래스터 0) 축 눈금으로 환산한
**벡터 좌표 판독**(`[도표·벡터]`)을 했다. 그 판독이 표 2 의 RMSE · MAX 를 0.01–0.02 안에서
재현한다(§8.4) — 판독 절차 자체의 검산이다.

## 표기 규약

- `[인쇄]` — 본문 · SI 가 실제로 쓴 문장 · 수치 · 식 (식은 **쪽 렌더 이미지를 보고** 옮겼다;
  텍스트 층은 식 기호를 대부분 잃는다).
- `[도표]` — 그림을 눈으로 읽은 값, 판독 폭을 단다.
- `[도표·벡터]` — PDF 벡터 경로의 좌표를 그 그림의 축 눈금(tick) 위치로 환산한 값. 좌표
  정밀도는 축 범위의 ≈0.1 % 이하이고, 계열 귀속은 채움 색으로 판정했다(범례 표식은 뺐다).
- `[재현]` — 인쇄된 수치로 이 digest 가 다시 계산한 값 (스크립트는 커밋하지 않은 scratch).
- `[해석]` — 이 digest 의 판단. 원문이 말한 것이 아니다.
- 퍼센트에는 반드시 "유지" · "감쇠" · "손실" · "LAM %" · "LLI %" · "%p" 를 붙인다. 원문은
  "capacity degrades to 60 % of the initial capacity" 처럼 **유지율**을 "degrades to" 로
  쓴다 — 원문 그대로 옮기고 뜻(= 용량 **유지** 60 %, 감쇠 40 %)을 `[해석]` 으로 단다.
- 원문 수치의 층위를 매번 가른다: **측정**(셀 전압 · 용량 · 임피던스) / **인용**(참고문헌의
  주장) / **모형값**(COMSOL 시뮬레이션 출력) / **적합값**(반쪽전지 창 맞춤 출력 = 이 편의
  "ground truth") / **DNN 추정값**.

# 원문에 없어서 확인이 필요한 것 (읽기 전에 먼저 본다)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| G1 | **셀 형식 · 제조사 · 전극 조성이 없다.** "24 LiBs with a nominal capacity of 2.4 Ah … LiNi1−x−yCoxMnyO2/Graphite (NMC) … 3 to 4.2 V" 뿐. `cylindrical`·`18650`·`pouch`·`prismatic` **0회**(`[재현]` 전수). | 원통형이라는 것은 추정일 뿐이다. 양극 Ni 함량을 모르면 OCP 기울기 · 상전이 구조를 모른다. |
| G2 | **라벨 맞춤에 쓴 충전 곡선의 조건이 명시돼 있지 않다** — "match the collected charging curves"(§2) · "under constant-current charging conditions"(§3.2). RPT · check-up · 저율 곡선 언급 **0회**. | §4.1 에서 그림 대조로 **사이클 전류(1 C · 2 C) CC 충전 곡선**이라고 판정했다(`[해석]`). 저율이 아니므로 분극이 크다. |
| G3 | **PSO 설정이 한 문장이다** — 입자 수 · 반복 · 탐색 범위 · 초기 범위 · 수렴 기준 · 반복 실행 여부 전부 없음. `bound*` 0 · `multi-start`/`initial guess` 0 · `uniqu*` 0 · `uncertain*` 0 · `error bar` 0 · `confidence` 0 (§14). | 라벨의 유일성 · 오차막대를 판정할 근거가 원문에 하나도 없다. |
| G4 | **맞춤에 쓴 전압 창 · 샘플 수 `N` 이 없다.** 식 (3) 은 `t1–tN` 을 "the duration of the charging process" 로만 정의한다. | 창이 CC 구간 전체라면 시작 전압(1 C 신품 ≈3.29 V · 2 C ≈3.75–3.79 V · 노화 1 C ≈3.62 V, `[도표]`)이 노화와 율에 따라 움직인다 → 관측 창이 노화에 따라 바뀐다. |
| G5 | **1 C · 25 °C 군에서 `Q_NE` 가 자유였는지 고정이었는지 없다.** 그 군은 LAM_NE 를 "minimal" 이라며 추정 대상에서 뺀다(참고문헌 [34] 인용). | 고정이면 **사전지식 주입**이고, 자유였다면 맞춤이 낸 LAM_NE 값을 버린 것이다 — 어느 쪽인지에 따라 LLI · LAM_PE 라벨의 의미가 달라진다. |
| G6 | **반쪽전지 OCP 를 충전 · 방전 중 어느 쪽(또는 평균)으로 썼는지 없다** — "Low-rate charge/discharge tests at 1/20 C". 해체한 신품 셀이 몇 개인지도 없다("The fresh NMC battery … was first discharged …" 단수). | 1/20 C 반쪽전지 곡선은 OCP 가 아니라 히스테리시스 · 분극을 품은 곡선이다. 방향 선택이 창 좌표를 옮긴다. |
| G7 | **COMSOL 모형 매개변수가 하나도 인쇄되지 않았다.** SI Note 4 는 AC 섭동 식 두 줄과 경계조건뿐(§5.2). 맞춤한 매개변수 목록 · 최적화기 이름 · OCP 출처 · 막(film) 저항 · 이중층 용량 · 비표면적 정의 전부 없음. | 시뮬레이션 재현 불가. LAM 을 부피분율로 내릴 때 계면 면적이 같이 줄어드는지(§5.3) 판정 불가. |
| G8 | **LLI 를 바꾼 "stoichiometric coefficient" 가 어느 전극 · 어느 변수인지 없다.** 시뮬레이션 스펙트럼을 계산한 상태(만충?)가 노화 조합마다 어떻게 정의됐는지도 없다. | 고정 셀 상태에서 화학량론을 옮기면 무엇이 바뀌는지(§5.4)를 원문으로 확인할 수 없다. |
| G9 | **DNN 입력 스펙트럼이 충전 후 · 방전 후 중 어느 것인지 없다.** EIS 는 "after a 15-min relaxation period following the completion of charging **or** discharging". | 그림 1c 의 "SOC = 100 %" 와 "SOC = 0 %" 는 아크 크기가 크게 다르다. 그리고 CC 전용 사이클에서 그 끝점의 실제 SOC 는 노화와 함께 움직인다(§9.5). |
| G10 | **학습 · 시험 셀이 몇 개 · 어느 셀인지 명시가 없다.** "split in a ratio of 1:3" · "25 % of the training dataset reserved for validation" · "The test dataset contains data from other cells". | §7.2 의 셀 단위 독해(군마다 학습 2 · 시험 6)는 `[해석]` 이다. 그림 7 범례(Cell #1–#6)와 맞는다. |
| G11 | **시험 표본 수가 모드마다 다른데 설명이 없다** — `[도표·벡터]` 25 °C@2C: LLI 163 · LAM_PE 152 · LAM_NE 116, 35 °C@2C: 289 · 238 · 212 (§8.4). | 같은 셀 · 같은 사이클이면 모드마다 같아야 한다. 일부 라벨을 걸렀다면 그 기준이 라벨 품질 판정이다. |
| G12 | **DNN 초매개변수 대부분이 없다** — GRU 은닉 크기 · 드롭아웃 비율 · 학습률 · 미세조정 epoch · 동결 층 여부 · 사전학습 정규화(μ, σ)를 다시 계산했는지. `[인쇄]` 있는 것: 합성곱 32 개(크기 2) · 밀집 32/16 · 배치 128 · 1,000 epoch · Adam. | 재현 불가. |
| G13 | **SOH 정의가 없다.** 그림 11 색막대가 "SOH 0.6–1" 인데 본문은 SOH 를 정의하지 않는다(용량 유지율로 보인다 — `[해석]`). | |
| G14 | **데이터 · 코드 공개 문장이 없다.** "Data availability" 절 없음. `[인쇄]` "Supplementary data to this article can be found online at https://doi.org/10.1016/j.jechem.2025.05.014." 이 전부. | §18. |
| G15 | **K-K 검정은 신품 스펙트럼만**(군마다 하나, SI 그림 S1). 노화 스펙트럼(학습 · 시험 자료의 대부분)은 검정 기록이 없다. | 15 분 휴지 뒤 저주파 비정상성(§18) 을 걸러냈는지 알 수 없다. |
| G16 | **그림 1f 의 25 °C@2C LLI 궤적(최대 ≈61.6 %)이 어느 셀인지 없다** — 같은 조건 시험 셀의 라벨 최대(≈30.9 %)의 두 배(§13 불일치 2). | |

## 0. 서지사항 (직접 확인)

| 항목 | 내용 (`[인쇄]`, PDF 1 · 14 쪽 · SI) |
|---|---|
| 저자 | Yue Sun ᵃ, Rui Xiong ᵃ,⁎ (교신, rxiong@bit.edu.cn), Peng Wang ᵃ, Hailong Li ᵇ, Fengchun Sun ᵃ |
| 소속 | ᵃ National Engineering Research Center for Electric Vehicles, School of Mechanical Engineering, Beijing Institute of Technology, Beijing 100081, China · ᵇ School of Business, Society and Engineering, Mälardalen University, Västerås 72123, Sweden |
| 서지 | *Journal of Energy Chemistry* **107** (2025) 894–907 · doi 10.1016/j.jechem.2025.05.014 · ISSN 2095-4956 · ✩ "This article is part of a special issue entitled: 'AI4Batteries' published in Journal of Energy Chemistry." |
| 이력 | Received 10 March 2025 · Revised 7 May 2025 · Accepted 8 May 2025 · Available online 19 May 2025 |
| 키워드 | Lithium-ion battery · Degradation diagnostics · Impedance spectra · Integration strategy · Deep learning |
| 라이선스 | "© 2025 Science Press and Dalian Institute of Chemical Physics, Chinese Academy of Sciences. Published by Elsevier B.V. and Science Press. **All rights are reserved, including those for text and data mining, AI training, and similar technologies.**" — CC 아님 |
| 연구비 | National Key R&D Program of China (2024YFB2505003) |
| CRediT | Yue Sun: Writing – original draft, Methodology, Conceptualization · Rui Xiong: Writing – review & editing, Supervision, Investigation, Conceptualization · Peng Wang: Writing – review & editing, Conceptualization · Hailong Li: Writing – review & editing, Supervision · Fengchun Sun: Writing – review & editing, Supervision |
| 이해충돌 | "The authors declare that they have no known competing financial interests or personal relationships …" |
| 분량 | 본문 14 쪽 (§1–5 · 그림 12 · 표 2 · 식 18 · 참고문헌 [1]–[37]) + SI 5 쪽 (Supplementary Note 1–6 · 표 S1–S2 · 그림 S1–S6 · 참고문헌 [R1]) |

**PDF 메타데이터 (직접 읽음, `pymupdf`)**

| | 본문 | SI |
|---|---|---|
| 파일 | `475d1950-3._A_deep_learning_…_impedance_spectra.pdf` · 2,296,734 B · sha256 `7b80ada4…a9b64967` | `69045ee7-3._Sup_A_deep_learning_…_impedance_spectra.pdf` · 515,965 B · sha256 `5987ae8b…1bfc90` |
| format · 쪽 · 쪽 크기 | PDF 1.7 · 14 · 595.28 × 793.70 pt | PDF 1.7 · 5 · 595.32 × 841.92 pt (A4) |
| title | "A deep learning approach for enhanced degradation diagnostics of NMC lithium-ion batteries via impedance spectra" | (빈 값) |
| author | "Yue Sun" | "杜晓伟" |
| subject | "Journal of Energy Chemistry, 107 (2025) 894-907. doi:10.1016/j.jechem.2025.05.014" | (빈 값) |
| keywords | "Lithium-ion battery,Degradation diagnostics,Impedance spectra,Integration strategy,Deep learning" | (빈 값) |
| creator · producer | "Elsevier" · "Acrobat DC" | "Microsoft® Word LTSC" · "Microsoft® Word LTSC" |
| 작성 · 수정 | 2025-06-30 16:40:22 +05'30' · 2025-07-24 15:08:56 +05'30' | **2026-10-02 20:32:28 +09'00'** (둘 다) |
| 암호화 | 없음 | 없음 |

`[해석]` SI 는 **업로드 직전에 Word 문서를 PDF 로 바꾼 판**으로 보인다(작성 시각 = 수정
시각 = 2026-10-02 20:32 KST, 저자 필드가 논문 저자 명단에 없는 이름). 출판사가 배포한 원본
SI 의 형식과 같은지는 이 자료로 확인할 수 없다 — 사실만 적는다. SI 의 그림은 래스터,
본문 그림은 벡터다.

## 1. 한 문단 요약

24 개의 NMC/graphite 셀(공칭 2.4 Ah, 3–4.2 V)을 세 조건(25 °C·1 C · 25 °C·2 C · 35 °C·2 C,
군당 8 셀, CC 충방전)에서 수명 끝(초기 용량의 60 % **유지**)까지 돌리며 충전 또는 방전 완료 +
15 분 휴지 뒤 EIS(10 kHz–0.1 Hz, 51 점)를 잰다. 모드 라벨은 **신품 셀 하나를 해체해 1/20 C
코인 반쪽전지로 한 번 잰 OCP 곡선**을 고정하고, **사이클 충전 곡선**에 `p0, n0, Q_PE, Q_NE,
R` 다섯 개를 PSO 로 맞춘 값이다(식 1–4; 맞춤 RMSE 신품 7.52 · 노화 6.55 mV). 이 라벨을 고주파
유도성 점을 지운 43 주파수 스펙트럼(실 · 허 2 채널)으로 회귀하는 CNN–GRU–attention–dense
DNN 을 만들고, **COMSOL 6.1 P2D 임피던스 모형**(신품 만충 스펙트럼에 맞춤, RMSE 0.76 mΩ)으로
LLI · LAM_PE · LAM_NE 를 각각 0–90 % 10 단계로 쓸어 만든 **1,000 개 합성 스펙트럼으로
사전학습**한 뒤 실험 자료로 다시 학습한다("integration strategy"). 군마다 셀 2 개의 수명 앞
50 %(용량 ≈80 % 유지까지)로 학습하고 나머지 6 셀의 전 수명으로 시험해, 적합 라벨 대비 RMSE
**LLI · LAM_PE < 3 %p, LAM_NE < 4 %p**, 실험만으로 학습한 기준선 대비 최대오차 **42.92–66.30 %
감소**를 보고한다. 주의 가중치로 "LLI ↔ 고주파(SEI) + 저주파(확산)", "LAM ↔ 중주파(전하
이동) + 저주파(확산)" 을 읽는다. `[해석]` **모든 정확도는 적합 라벨에 대한 일치도**이고,
라벨의 식별성은 재지 않았으며, 주의 결과는 두 모드를 가르는 독립 채널이 아니라 **한 노화
패턴의 부호 반전**이다(§9).

## 2. p.1–2 — 초록 · §1 서론

### 2.1 초록에서 뽑은 명제 `[인쇄]`

- "EIS falls short in quantitatively determining the degree of specific degradation modes."
- "The proposed method can automatically determine the most relevant frequency ranges for each
  degradation mode, which can link impedance characteristics to battery degradation."
- "To overcome the limitation of scarce labeled experimental data, simulation results derived
  from mechanistic models are incorporated into the model."
- "root mean square errors below 3% for estimating loss of lithium inventory and loss of active
  material of the positive electrode, and below 4% for estimating loss of active material of the
  negative electrode while requiring only **25% of early-stage experimental degradation data**."
- "a reduction in **maximum estimation error** ranging from **42.92% to 66.30%** across different
  temperatures and operating conditions compared to the baseline model trained solely on
  experimental data."

`[해석]` 초록의 "RMSE below 3 %" 는 **%p** 다(라벨이 % 단위). 정답 축은 §4 의 적합값이다 — 초록은
그것을 말하지 않는다. "25 %" 와 §3.5 의 "initial 50 %" 의 관계는 §7.2.

### 2.2 §1 문헌 지도 — 이 위키와 겹치는 것 `[인쇄]`

- EIS 해석 세 갈래: ECM [10] — "various electrochemical processes with similar time constants
  are coupled, making it challenging to distinguish them [11]"; 메커니즘 모형 — "susceptible to
  overfitting under conditions of insufficient experimental data [12]"; DRT — "highly sensitive
  to the selection of regularization parameters [13,14]". `[해석]` 셋 다 이 위키의 축퇴 어휘로
  옮기면 "같은 시상수의 과정이 하나로 묶인다" · "자유도가 자료보다 많다" · "정칙화가 답을
  고른다"([[drt-peak-count-nonidentifiability]] · [[nullspace-coefficient-interpretation]]) 다.
- EIS → 용량 · RUL 데이터 기반 [15–20]: Zhang 외 [17] (GPR, R² 0.68–0.96 — 이 위키
  [[zhang2020-eis-aging-dataset]] 의 원전), Xiong 외 [18](라벨 없는 스펙트럼 활용, RMSE 50.66 %
  감소), Kim 외 [19](InfoGAN 잠재변수 + GPR, < 1.87 mAh / 45 mAh), Liu 외 [20](VAE + 양방향 GRU,
  1.43 mAh / 45 mAh).
- "Capacity is the high-level metric that is influenced by fundamental degradation modes [21]."
  · "The commonly reported degradation modes include LLI, LAM_NE and LAM_PE [23]." · "Current
  methods for extracting the degree of degradation modes from impedance spectra primarily rely
  on ECM fitting [24]."
- ★ "**Deep-level electrode degradation modes that contribute to capacity fade cannot be
  accurately diagnosed solely based on the impedance spectra of full cells [11].**" · "The
  mapping between various frequency ranges of the impedance spectrum and the underlying
  degradation modes remains poorly understood [25]."

`[해석]` 마지막 두 문장은 이 편이 **스스로 인용한 반대 전제**다 — 완전지 임피던스만으로는
전극 수준 모드를 정확히 진단할 수 없다는 진술([11] = 같은 그룹의 Tian · Xiong · Shen · Sun
2020). 이 편은 그 한계를 "DNN + 시뮬레이션 통합" 으로 넘었다고 주장하지만, 넘었는지를 재는
대조(단일 모드 시험 · 상관을 깬 시험)는 하지 않았다(§9.6).

## 3. p.2–4 — §2 데이터 생성 · 그림 1 (직접 봄)

### 3.1 셀 · 프로토콜 `[인쇄]`

- 24 셀, 공칭 2.4 Ah, LiNi1−x−yCoxMnyO2/Graphite, 3–4.2 V. 세 군 × 8 셀.
- 군 1: CC **1 C (= 2.4 A)** 충방전 · 25 °C. 군 2: CC **2 C** · 25 °C. 군 3: CC **2 C · 35 °C**
  (§2 본문 그대로 — SI 표 S1 과 그림 10 캡션의 "1 C" 는 §13 불일치 1).
- "the temperatures mentioned refer to the **external ambient temperature** of the battery,
  which is controlled by placing the battery inside a programmable temperature chamber."
- 전류 · 전압 1 Hz 샘플링.
- EIS: "measured after a **15-min relaxation period** following the completion of charging or
  discharging, using Gamry Interface 5000P" · 정전류 모드 진폭 **0.1 A** · **10 kHz – 0.1 Hz,
  10 points per decade** · "Each impedance spectrum ultimately records data across **51**
  frequencies."
- K-K: "Given that each group of batteries underwent identical cycling protocols, the impedance
  spectra of **fresh cells** from each group were selected to perform the K-K test." 상대잔차
  "all within 1% [25]".
- CV 단계 · RPT(기준 성능 시험) · check-up 언급 **0회** (`[재현]` 전수).

`[재현]` 1 C = 2.4 A 는 **공칭 2.4 Ah** 에 대한 정의다. 2 C = 4.8 A. 그런데 SI 표 S1 의 "초기
용량"(= 각 율의 충전 전류 적분, `[인쇄]` 각주)은 군 평균 **1.947 / 1.727 / 1.804 Ah** = 공칭의
**81.1 / 72.0 / 75.2 %** 다(군 1 / 군 2 / 군 3, 셀 간 변동계수 1.15–1.58 %). 그 실사용 용량으로
전류를 다시 나누면 ≈1.23 C · ≈2.78 C · ≈2.66 C 다. 수명 끝 기준(초기의 60 % **유지**)은 군 평균으로
1.168 / 1.036 / 1.082 Ah, 학습 경계(≈80 % **유지**)는 1.558 / 1.382 / 1.443 Ah 다.
`[해석]` CC 만으로 1–2 C 에서 4.2 V 에 닿으면 공칭 용량의 70–80 % 만 쓰인다 — **이 편의 "1 C" 는
공칭 기준이지 실제 사용 용량 기준이 아니다.**

### 3.2 그림 1 (직접 봄 + 벡터 판독)

- **(a) 신품 스펙트럼, 25 °C vs 35 °C.** `[도표·벡터]` 유도성 구간까지 포함한 **원 스펙트럼**(축 안
  표식 25 °C 51 점 · 35 °C 50 점 — 한 점은 −Im 축 하한 −10 mΩ 밖으로 보인다)이다. 실축 교차
  **25 °C 16.46 mΩ · 35 °C 15.82 mΩ**. 25 °C 아크 꼭대기 (22.25, 3.45) · 아크 끝 극소 (29.41, 0.99) mΩ;
  `[도표]` 35 °C 아크 끝 극소 ≈(22, 0.6) mΩ. 그림 안 표시: "Conduction process"
  (실축 교차 부근) · "SEI and charge transfer process"(아크 하나) · "Diffusion process"(꼬리).
  `[해석]` **SEI 아크와 전하이동 아크가 따로 보이지 않는다** — 하나의 눌린 아크다.
- **(b) 충전 곡선** 범례 "25℃@2C · 35℃@2C · 25℃@1C" (★ 셋째 군 = **35 °C@2C**). `[도표]` 4.2 V
  도달 용량 ≈1.60 / ≈1.68 / ≈1.91 Ah (±0.02), 시작 전압 ≈3.79 / ≈3.75 / ≈3.30 V.
- **(c) 신품 SOC = 100 % vs 0 %**: `[도표]` 0 % 쪽 아크가 Re ≈35 mΩ 까지(100 % 는 ≈29 mΩ).
  `[인쇄]` "the impedance in the mid-frequency region increases significantly at lower SOC
  levels". `[해석]` CC 전용 사이클이라 "SOC = 100 %" 는 **명목값**(1–2 C CC 로 4.2 V 에 닿은
  상태)이다.
- **(d) 방전 곡선**(범례 없음, 선 모양은 (b)와 같음): `[도표]` 3.0 V 도달 ≈1.77 / ≈1.85 /
  ≈1.91 Ah (25 °C@2C / 35 °C@2C / 25 °C@1C).
- **(e) 25 °C 노화 스펙트럼**(어느 율인지 미표기): `[도표]` 실축 교차 ≈16 → ≈20.5 mΩ, 아크 끝
  ≈37 mΩ, 꼬리 끝 ≈44 mΩ (±0.5).
- **(f) LLI vs 사이클** (라벨 = 적합값): `[도표·벡터]` **25 °C@2C 82 점(사이클 2–83), LLI 2.78 →
  61.6 %**; **35 °C@2C 66 점(사이클 2–67), 0.37 → 33.9 %**; 25 °C@1C 점선(사이클 ≈1–196), −0.2 →
  34.1 %. 1 C 궤적에 **계단 하강 두 번** — 사이클 ≈97–100 (≈13.9 → ≈12.3 %, −1.6 %p) · ≈146–149
  (≈24.1 → ≈21.2 %, −2.9 %p).
  `[인쇄]` "the increase in LLI is slower with lower charge–discharge rates" · "LLI at 35 °C is
  less pronounced compared to 25 °C as the battery ages, suggesting that elevated operating
  temperatures may mitigate LLI to some extent."
  `[해석]` 계단 하강은 그림 7a 의 시험 셀 다섯에서도 같은 사이클대(≈142 → 149)에 보인다 —
  **모든 셀에 동시에 걸린 프로토콜 사건**(중단 · 휴지 등)이 적합 LLI 를 되돌린 것으로 읽힌다.
  §9.4 의 "확산 지배 리튬 가둠은 회복될 수 있다" 와 같은 방향이다 — 즉 **이 LLI 라벨에는 가역
  성분이 섞여 있다.**

## 4. p.4–6 — §3.2 라벨 생성: 반쪽전지 창 맞춤 · 식 (1)–(4) · 그림 3–4

### 4.1 절차 `[인쇄]` (그림 3 직접 봄 — 자동 크롭이 놓쳐 수동 크롭)

- "The quantification of the degradation modes in this study is based on the **assumption that
  battery degradation does not asymmetrically affect the individual phase transitions of the
  electrode materials [3]**. Accordingly, the OCP curves of the positive and negative electrodes
  are **measured only once under the fresh-cell condition [26]**."
- "The fresh NMC battery described in Section 2 was first discharged to the lower cutoff voltage
  and then transferred into an argon-filled glovebox … rinsing with dimethyl carbonate (DMC) …
  assembled into coin cells using lithium metal foil. **Low-rate charge/discharge tests at 1/20 C**
  were performed to acquire the OCP curves." · "A cubic spline interpolation is then applied to
  construct continuous SOC-OCP mappings."
- 그림 3: 왼쪽 "Acquisition of the OCP curve"(해체 → 전극 회수 → Li 대극 코인셀 → OCP 시험),
  오른쪽 "Matching of charging curves"(식 (2) 로 노화 상태별 충전 곡선 재구성 → **Particle swarm
  optimization** → 식 (3) 최소화로 `p0, n0, Q_PE, Q_NE, R` 식별 → "Compared to the fresh
  battery" → LLI · LAM_PE · LAM_NE 계산).

### 4.2 식 (1)–(4) — 쪽 렌더 이미지로 확인 `[인쇄]`

```
(1)  p(t) = p0 − I t / Q_PE ,   n(t) = n0 + I t / Q_NE        (I > 0 during charging)
(2)  Ũ(t) = E_PE(p(t)) − E_NE(n(t)) + I R
(3)  U_RMSE = sqrt( (1/N) Σ_{t=t1}^{tN} ( U(t) − Ũ(t) )² )
(4)  LAM_PE = (1 − Q_PE / Q_PE,f) × 100%
     LAM_NE = (1 − Q_NE / Q_NE,f) × 100%
     LLI    = (1 − (p0 × Q_PE + n0 × Q_NE) / (p0,f × Q_PE,f + n0,f × Q_NE,f)) × 100%
```

"where p0 and n0 denote the SOC levels for the positive and negative electrodes at the beginning
of charging … I is the current, which is positive during charging … R denotes the battery
resistance … the subscript f denotes the parameters of the fresh cell."

`[재현]` **식 (4) 의 LLI 정의는 식 (1) 의 부호 규약과 맞는다.** 식 (1) 에서 `d/dt (p·Q_PE + n·Q_NE)
= −I + I = 0` 이므로 `p0·Q_PE + n0·Q_NE` 는 충전 중 보존되는 리튬 재고(Ah)다. 단 이것은 **`p` 가
양극의 리튬화 분율(stoichiometry)일 때만** 성립한다 — 원문은 `p` 와 `n` 을 모두 "SOC levels"
라 부르는데, 양극 SOC 를 관례대로 탈리튬 정도로 읽으면 식 (1) 의 부호와 식 (4) 가 둘 다
틀린다. `[해석]` 원문의 "SOC" 는 두 전극 모두 **리튬화 분율**의 뜻으로 써야 앞뒤가 맞는다.

### 4.3 그림 4 (직접 봄 + 확대)

- **(a) "Schematic diagram of potential matching"**: 가로 "Battery SOC" −0.2–1. 양극 OCP(≈3.3 →
  ≈4.35 V)가 −0.1–0.9, 음극 OCP(≈1.6 → ≈0.08 V)가 0–1 에 놓이고, 화살표 `Q_PE → LAM_PE`(−0.1–0.9)
  · `Q_LI → LLI`(0–0.9) · `Q_NE → LAM_NE`(0–1). 모식도다(수치 판독 대상 아님).
- **(b) 재구성 vs 측정 충전 곡선**: 범례 "Reconstruction-Fresh · **Ground truth-Fresh** ·
  Reconstruction-Aged · **Ground truth-Aged**". `[도표]` 신품 3.29 V → ≈4.18 V @ ≈1.86 Ah, 노화
  3.62 V → 4.20 V @ ≈1.10 Ah (±0.02 Ah). 0.1–0.7 Ah 어깨 구간에서 재구성 원이 측정 선의 위 · 아래로
  번갈아 수 mV 씩 벗어난다(인쇄 RMSE 와 같은 크기).
  `[인쇄]` "achieving a RMSE of **7.52 mV** for the fresh battery and **6.55 mV** for the aged
  battery."
- `[해석]` 신품 곡선의 시작 전압 3.29 V 와 끝 용량 ≈1.86 Ah 가 그림 1b 의 25 °C@1C 곡선(3.30 V ·
  ≈1.91 Ah)과 맞는다 → 그림 4b 는 **1 C 사이클 충전 곡선**으로 보인다. 노화 곡선은 1.10/1.86 ≈
  0.59 → **수명 끝 근처**(60 % 유지).
- ★ `[해석]` **"Ground truth" 가 이 그림에서는 측정 전압 곡선을, 그림 8–9 · 본문에서는 적합
  라벨을 가리킨다.** 같은 낱말이 측정과 적합값을 모두 덮는다 — 이 편의 라벨 층위를 흐리는
  어휘 사용이다(본문 "ground truth" 4 회는 전부 적합 라벨, §14).

### 4.4 ★ 판정 (a) — 라벨 층위

**판정: 이 편의 "ground truth"(= "target values" = `Dtru`)는 측정이 아니라 적합값이다** —
근거 셋:

1. `[인쇄, §2]` "By applying the half-cell model introduced in Section 3.2 to match the collected
   charging curves, **the target values for the degree of degradation modes can be obtained**."
2. `[인쇄, 식 (18)]` "`Desm,i` and `Dtru,i` refer to the estimated and **target values** of the degree
   of degradation modes" — 성능 지표(RMSE · MAE · R² · 최대오차)는 전부 이 `Dtru` 대비다.
3. `[인쇄, 그림 3 · 식 (4)]` LLI · LAM 은 PSO 로 찾은 `p0, n0, Q_PE, Q_NE` 의 함수다. 해체 ·
   코인셀 · XRD 같은 **독립 측정으로 라벨을 검증한 문장은 0** — 반쪽전지 측정은 신품 OCP
   곡선 하나를 얻는 데만 쓰였다.

따라서 **"RMSE < 3 %" 는 DNN 출력과 적합 라벨 사이의 차이**다(단위 %p). 참 열화 대비 오차 =
(DNN − 라벨) ⊕ (라벨 − 참값) 인데 이 편은 **첫째 항만** 잰다. 둘째 항(라벨 오차)은 오차막대 ·
다중 시작 · 유일성 점검 · 독립 측정 어느 것으로도 재지 않았다(§14 어휘 전수 0).

**이 라벨 맞춤 vs 우리 α·β 창 맞춤** (`[해석]` 대조, 우리 쪽은 `degradation-degeneracy/docs/RESULTS.md`
와 `docs/07_LAM_LLI.md` 참조 — 수치는 옮기지 않는다):

| 축 | 이 편의 라벨 맞춤 | 우리 α·β 창 맞춤 |
|---|---|---|
| 자유도 | **5** — 창 4 (`p0, n0, Q_PE, Q_NE`) + 동역학 1 (상수 `R`) | 4 — 창 4 (`α_PE, β_PE, α_NE, β_NE`), 동역학 0 |
| 관측 | **사이클 전류(1 C = 2.4 A · 2 C = 4.8 A) CC 충전 곡선** V(t), 1 Hz | 준평형 pOCV 곡선(+ 옵션 dV/dQ · dQ/dV) — RESULTS "이 결론이 말하지 않는 것"(운용 범위가 한 점) |
| 관측 창 | 충전 시작 전압(율 · 노화에 따라 ≈3.29–3.79 V, `[도표]`) → 4.2 V CC 컷오프. 창의 양 끝이 **율 · 저항 · 노화의 함수** | 고정 컷오프 쌍 사이 전 구간 |
| 동역학 처리 | 상수 `R` 하나가 전 SOC 의 분극을 흡수 — 확산 과전압의 SOC 의존 · 이완 과도는 모형 밖 | 저율이라 과전압이 작다는 가정 (RESULTS 가 "pOCV 급 상한" 으로 명시) |
| 반쪽전지 곡선 | 신품 셀 1 개 해체 · 1/20 C 코인셀 · 한 번만 · 큐빅 스플라인 (형상 불변 가정 [3]) | truth 를 만든 같은 OCP (모델 오차 0 층 — `docs/09_22P_GAP.md` §0 의 경고) |
| 최적화 | PSO, 설정 미인쇄 (G3) | 다중 시작 + optimizer 정책 (RESULTS "multi-start 진단") |
| 식별성 | **안 잼** — 유일성 · 오차막대 · 다중 시작 · 반복 0 | 합성 truth 로 복원 채점 + `mode-observability` Phase 1c · 1i 의 `JᵀJ` |
| 정답 | 없음 — 맞춤값이 곧 "ground truth" | 설계된 합성 truth |

**우리 `mode-observability` 1c · 1i 가 이 편 라벨에 예언하는 것** (`[해석]`, 우리 수치는
`mode-observability/docs/PHASE1C_NOTES.md` · `PHASE1I_NOTES.md` 참조):

- 1c 는 우리 창 맞춤의 가장 약한 방향이 **`(1,1,1)/√3` — 세 모드가 같이 움직이는 방향** 근처임을
  보였고, 1i 는 22p 삼중항의 **오차 분산이 그 한 축에 몰린다**는 것을 보였다. 이 편의 라벨은
  같은 창 대수(식 1–2) 위에 있으므로 **세 라벨의 오차는 서로 독립이 아니라 한 방향으로 같이
  움직일 것**이다 — 표 1 의 모드별 RMSE 셋을 세 개의 독립 정확도로 읽으면 안 된다.
- 그 방향은 형상만으로는 안 보이고 **절대 용량(Ah) 하나로만 닫힌다**
  ([[np-lip-ocv-reparametrization]] 의 2 자유도 정리; 2026-10-01 PyProBE 형상만 시험,
  [[22p-physics-or-degeneracy]] Evidence For). 이 편에서 그 Ah 척도는 **1–2 C CC 충전이 4.2 V 에
  닿을 때까지의 용량**인데, 그 용량은 상수 `R` 이 키우는 `IR` 만큼 짧아진다 → **`(1,1,1)` 공통
  모드와 `R` 이 같은 관측(곡선 길이)을 나눠 갖는다.** 게다가 NMC 양극 OCP 가 창 안에서 완만한
  기울기를 가지면 `IR` 의 수직 이동은 `p0` 의 수평 이동과 거의 같은 서명을 남긴다 →
  **`R ↔ p0 ↔ LLI` 별칭(aliasing)** 이 예언된다. (미검증 — §17.4 실험 1 이 값싸게 잰다.)
- 이 편 자신의 라벨 궤적이 그 방향 근처를 달린다: `[도표·벡터]` 2 C 두 군에서 시험 표적의
  최대가 LLI 30.9 · LAM_PE 28.9 · LAM_NE 32.5 % (25 °C), 33.5 · 38.9 · 32.7 % (35 °C) 로 세 모드가
  모두 30–39 % 범위이고, 그림 7a · b(1 C)에서도 셀마다 LLI 와 LAM_PE 추정이 나란히 ≈23–31 % 까지
  간다. `[해석]` **세 모드가 함께 자란다.** 참 궤적이 그렇다면 맞춤이 가장 덜 보는 방향으로
  열화가 진행된 것이고, 맞춤 오차가 그 방향으로 새면 전압 잔차(6.55–7.52 mV)로는 걸러지지 않는다.

**라벨 불연속의 징후** — `[도표·벡터]` 그림 9b(35 °C@2C, LAM_PE)에서 시험 표적이 **6.09 % 다음
14.40 %** 로 건너뛴다(시험 셀 전체를 묶은 238 표본 중 그 사이 표적 0 개). 같은 그림에서 DNN 예측은
표적 4–6.1 % 구간에서 4.96–12.21 %, 14.4–17 % 구간에서 8.47–13.52 % 로 **간극을 가로질러 연속**이다.
`[해석]` 간극을 건넌 셀이라면 그 셀의 라벨은 **연속한 두 표본 사이에 ≥8.3 %p 뛴 것**이고, 예측(=
스펙트럼의 함수)은 그 사이를 매끄럽게 잇는다 — 맞춤이 두 골짜기 사이를 갈아탄(PSO 의 basin 전환)
징후로 읽힌다. 물리적 LAM_PE 가 한 표본 간격에 8 %p 이상 계단으로 뛰었다는 다른 근거는 원문에 없다.

## 5. p.5–6 — §3.3 시뮬레이션 자료 · 그림 5 · SI Note 4–5

### 5.1 원문 `[인쇄]`

- "The simulation in this study is conducted using the lithium-ion module in **COMSOL
  Multiphysics 6.1**. The diffusion of lithium ions within the solid-phase is modeled using **Fick's
  second law**, while the charge transfer process … by the **Butler-Volmer** equation. The impedance
  spectra are obtained by applying a small-amplitude sinusoidal voltage perturbation (**10 mV**)".
- "an optimization algorithm is employed to fit the simulated impedance spectrum to the
  experimentally measured spectrum **at the fully charged state of a fresh battery**." · RMSE
  **0.76 mΩ**.
- "certain fine-scale features in the experimental data may not be fully reproduced … These
  discrepancies are considered acceptable within the context of generating pre-training data
  and are further corrected through incremental learning with experimental data."
- "Specifically, the **volume fraction** of the positive electrode active material is varied from
  **100% to 10%** of its initial value to simulate the changes in LAM_PE ranging from 0% to 90%.
  Similarly, the volume fraction of the negative electrode active material is varied to simulate
  the changes in LAM_NE, while the **stoichiometric coefficient** is adjusted to simulate the changes
  in LLI. By traversing the combinations … a simulation dataset containing **1,000** impedance spectra
  is ultimately generated [27,28]."
- "As shown in Fig. 5c, **significant changes** in the impedance spectra are observed with varying
  degrees of degradation modes".

### 5.2 SI Note 4 — 인쇄된 것 전부 (렌더 확인)

```
n = n0 + Re{ ñ · e^{2πf·it} }        ("n denotes the variable, n0 … the initial value …")
Z̃ = φ̃ / ( n · j̃ )                    (φ potential, n normal vector, j current density)
```

"A one-dimensional model consisting of three domains with different thicknesses: the negative
electrode, the separator and the positive electrode." · "The boundary of the positive current
collector is subjected to a sinusoidal perturbation with a 10 mV amplitude, whereas the boundary
of the negative current collector is grounded at 0 V."

**매개변수 표 · 맞춤한 매개변수 목록 · 최적화기 · OCP 출처 · 막 저항 · 이중층 용량 · 비표면적
정의 · 전극 두께 · 입자 반경 — 전부 없음**(G7). `[재현]` 어휘 전수: `film resistance` 0 ·
`double layer` 0 · `specific surface`/`surface area` 0 (본문 · SI).

### 5.3 그림 5 (직접 봄 + 벡터 판독) — ★ 시뮬레이터가 실제로 바꾼 것

- **(a) 측정 vs 시뮬레이션(신품 만충)**: `[도표·벡터]` 두 계열 각 **43 점**. 고주파 첫 점 측정
  (16.47, 0.53) vs 시뮬 (17.38, 1.45) mΩ · 아크 꼭대기 측정 (21.37, 3.28) vs 시뮬 (22.53, 3.83)
  · 아크 끝 극소 측정 (27.49, 0.92) vs 시뮬 (27.11, 0.56) · 저주파 끝 측정 (29.88, 2.65) vs 시뮬
  (28.67, 2.35).
  `[재현·벡터]` 43 점의 복소 거리 RMS = **0.755 mΩ** → 인쇄값 **0.76 mΩ** 재현(정의가 "점별
  |Z_sim − Z_meas| 의 RMS" 임을 확인). SI 그림 S4(Bode, 직접 봄): `[도표]` 위상 극소가 시뮬
  ≈ −9.7° @ ≈100 Hz vs 측정 ≈ −8.9° @ ≈250 Hz — **주 아크의 시상수가 ≈2.5 배 어긋난다**.
- **(b) 설계 공간**: LLI · LAM_PE · LAM_NE 각각 0, 10, 20, …, 80, 90 % 를 선으로 잇는 도식.
  `[재현]` 10 × 10 × 10 = **1,000** → **완전 요인(full factorial) 격자**이고 모드끼리 **상관 0**
  인 설계다(실험 자료의 동시 성장과 대조, §9).
- **(c) 여러 조합의 시뮬레이션 스펙트럼**: `[도표·벡터]` 그려진 것은 **1,000 개 중 64 개**(43 점씩
  64 색; 18 개짜리 회색 한 벌은 눈금 표식). 64 개를 같은 주파수 번호끼리 겹쳐 보면:
  - 아크 구간(고주파 쪽 0–20 번 점): Re 폭 **≤0.48 mΩ**(전체가 수평으로 평행 이동), **−Im 폭
    ≤0.10 mΩ**(아크 높이 ≈3.8 mΩ 의 ≈2 %);
  - 아크 끝 · 꼬리(30–42 번 점): −Im 폭이 0.93 → **8.32 mΩ**(0.1 Hz)까지 커진다.
  즉 **그려진 64 개 조합에서 모드는 아크(전하이동 영역)를 거의 안 바꾸고, 저주파 꼬리(확산)와
  작은 수평 이동만 바꾼다.**

### 5.4 ★ 판정 (b) — "LAM ↔ 중주파 전하이동" 은 물리 발견인가, 시뮬레이터의 각인인가

`[해석]` 단계별로:

1. **P2D 에서 LAM 을 부피분율 `ε_s` 로 내리면 무엇이 자동으로 따라오는가.** 비표면적이
   `a = 3ε_s / r_p` 로 정의돼 있으면 계면 면적이 같이 줄어 `R_ct ∝ 1/(a·L·i0)` 는 커지고 이중층
   용량 `a·C_dl` 은 작아진다(시상수 `R_ct·C_dl` 은 거의 그대로, **아크 지름만 커진다**). 이
   경로라면 "LAM ↔ 중주파 아크" 는 **시뮬레이터가 LAM 을 매개화한 방식의 각인**이 된다.
2. **그런데 그림 5c 는 그 각인을 보이지 않는다** — 그려진 64 조합에서 아크의 −Im 은 0.1 mΩ 안에서
   고정이다. 가능한 설명은 셋이고 원문으로 가를 수 없다(G7): (i) 64 개가 강한 LAM 조합을 포함하지
   않는다; (ii) 모형의 비표면적이 `ε_s` 와 독립인 입력값이라 LAM 이 계면을 안 건드린다; (iii) LAM 이
   용량 · 화학량론만 바꾼다.
3. **최종 모형은 실험 자료로만 다시 학습됐다**(`[인쇄, §3.5]` "retraining the secondary deep
   learning model exclusively with experimental data yields more accurate estimation results").
   따라서 그림 11–12 의 "LAM ↔ 중주파" 주의 패턴은 **시뮬레이터의 매핑에서 왔다고 볼 근거가 없고**
   (그려진 시뮬레이션에서는 아크가 안 움직인다), **실험 자료 안의 상관**(노화와 함께 LAM 라벨도
   커지고 아크도 커진다)과 주의 기계 자체(§9.3)에서 온 것으로 읽는 것이 원문 자료와 맞는다.
4. **LLI 를 "화학량론 계수" 로 바꾸면** — 고정된 셀 상태(만충)에서 두 전극의 리튬화가 옮겨
   가므로, 모형상 교환전류 `i0 ∝ c_s^0.5 (c_max − c_s)^0.5` 와 고상 확산 임피던스(OCP 기울기
   `dU/dc` 에 비례)가 바뀐다. 그림 5c 에서 바뀌는 것이 주로 저주파 꼬리라는 것은 **OCP 기울기
   경로**와 맞는다. 어느 전극의 어느 변수를 옮겼는지는 없다(G8).
5. **SEI 막 저항이 모형에 있는가 — 인쇄된 근거 0.** 없다면 모형에는 SEI 아크가 없고, "LLI ↔
   고주파 SEI(319.60–1598.01 Hz)" 연결은 **실험 자료의 상관(사이클과 함께 R_SEI 도, 적합 LLI 도
   자란다)에서만** 온다. ★ 같은 편의 SI 그림 S5(직접 봄)가 시사적이다 — **시뮬레이션 스펙트럼에
   ECM 을 맞춰도 "R_SEI" 가 ≈9.5 mΩ 로 나온다**(`[도표]` 막대 둘 다 ≈9.5–9.6 mΩ; 그림에 범례가
   없어 어느 막대가 시뮬인지는 모르지만 둘 다 같은 크기다). 모형에 막 저항이 없다면 ECM 의
   "R_SEI" 요소는 SEI 가 아닌 무언가(다공 전극 · 다른 전극의 전하이동)를 담는다 — 그 조건 아래서는
   **ECM 요소의 이름이 과정의 이름이 아니라는 것을 이 편 SI 가 스스로 보인다.**

**판정 (b)**: "LAM ↔ 중주파 전하이동" 은 **이 편 안에서 물리 발견으로 지지되지 않는다.** 시뮬레이터의
각인으로도 확인되지 않는다(그려진 시뮬레이션에서는 아크가 안 움직이므로) — **실험 자료 안의 동시
성장 상관 + 주의 가중치의 상보 구조(§9.3)** 로 설명되는 것이 가장 경제적이다. 시뮬레이터 매개화
(비표면적 정의 · 막 저항)가 인쇄되지 않아 그 이상은 판단 불가.

## 6. p.6–8 — §3.4 DNN 구조 · 식 (5)–(17) · 그림 2 · 6 · SI 그림 S6

### 6.1 구조 `[인쇄]`

- 표준화 입력 → **합성곱층(32 커널, 크기 2)** → **GRU** → **attention** → **밀집 2 층(32, 16, ReLU,
  각 층 뒤 dropout)** → 출력층(활성화 없음; "The number of neurons in this layer aligns with the
  dimensionality of the predicted data").
- 식 (5) 합성곱, (6)–(9) GRU, (10)–(13) attention, (14)–(15) 밀집 · ReLU. 렌더로 확인한 것:
  - (8) `H̃_t = tanh(w_h [r_t ⊙ h_{t−1}, X_t] + b_h)`, "⊙ denotes element-wise multiplication".
  - (9) `h_t = (1 − z_t) ⊙ h_{t−1} + z_t ⊙ H̃_t`.
  - (11) `α_t(i) = exp(h_tᵀ(N) h_s(i)) / Σ_{j=1}^{N} exp(h_tᵀ(N) h_s(j))`, "**where N denotes the
    number of frequencies contained in the impedance spectrum**".
  - (12) `c_t = Σ_{i=1}^{N} α_t(i) h_t(i)` · (13) `h̃_t = tanh(w_c [c_t ; h_t(N)])`.

### 6.2 ★ GRU 의 "sequence" 축은 무엇인가

`[인쇄]` 두 곳에서 "the GRU is employed to capture **long-term dependencies in battery
degradation**"(§3.1) · "the GRU captures long-term dependencies during battery degradation"(§3.4.1).

`[인쇄]` 그런데 식 (11) 의 `N` 은 **한 스펙트럼의 주파수 개수**이고, 그림 2(직접 봄)는 입력을
`Z′(f_i)`, `Z″(f_i)` 두 채널로, GRU 은닉상태를 `h_1 … h_N` 으로 그린다.

`[재현·벡터]` 그림 11c · d 의 주의 가중치 곡선은 43 개 이상적 격자 주파수에서 표본화하면 **합이
1.000** 이고(신품 · 최대 노화 곡선 각각), LLI 신품 곡선은 0.0223–0.0241 로 거의 균일하다(1/43 =
0.0233).

**판정**: GRU 의 시퀀스 축은 **노화 시점이 아니라 한 스펙트럼의 43 주파수**다. 입력 한 개 = 스펙트럼
한 개 = (43 × 2), 출력 = 그 시점의 모드 값. 모형은 **노화 이력을 보지 않는다** — "long-term
dependencies in battery degradation" 은 실제 입력 모양과 맞지 않는 서술이다(`[해석]`).
(소소한 것: SI 그림 S6 은 갱신 게이트를 식 (9) 와 반대로 — `z_t` 를 `h_{t−1}` 쪽에, `1 − z_t` 를
`H̃_t` 쪽에 — 그리고 `⊙` 를 "Matrix multiplication" 으로 적는다. 두 규약 모두 쓰이는 GRU 표기지만
같은 편 안에서 어긋난다.)

### 6.3 전처리 · 학습 `[인쇄]`

- "the **high-frequency inductive effects from cables and current collectors are removed**. After
  the preprocessing, the impedance from **43 frequencies** is retained [32]."
- 식 (16) Z-점수: `Z′_{n,i} = (Z′_i − μ_re)/σ_re`, `Z″_{n,i} = (Z″_i − μ_im)/σ_im`, "μ and σ denote
  the mean and standard deviation calculated from the training data". `[인쇄]` `μ`, `σ` 에 주파수
  첨자 `i` 가 없다 → **실부 전체 · 허부 전체에 하나씩**(주파수별 정규화 아님). 사전학습과
  재학습에서 다시 계산했는지는 없다(G12).
- 식 (17) MSE, 배치 `n = 128`, Adam [33], **1,000 epoch**, Keras/TensorFlow, 노트북 i7-12700H, CPU.

`[재현]` 51 = 5 decade × 10 + 1 → 지운 고주파 점 **8 개**. 이상적 격자 `10^(4 − k/10)` 이면 남는 최고
주파수는 `10^3.2` = 1584.9 Hz 이고 원문의 범위 끝값 1598.01 Hz(§9)는 계측기 실제 주파수로 보인다.
그림 11c · d 의 곡선 가로 범위(`[도표·벡터]` ≈0.100 – ≈1,600 Hz)와 그림 12 의 패널당 표식 129–134 개
(= 스펙트럼 3 개 × 43)가 이 43 점과 맞는다. 단 그림 12 의 고주파 끝 점 몇 개는 −Im < 0(유도성 쪽)이다
— `[해석]` 제거가 −Im 부호 기준이 아니었고, 고주파 쪽 고정 개수(8 점)를 지운 것과 맞는다.

## 7. p.8–9 — §3.5 통합 전략 · 그림 6

### 7.1 원문 `[인쇄]`

- "In this study, **when the battery capacity degrades to 60% of the initial capacity, it is
  considered to be replaced.** Only the **initial 50% of battery degradation data** from cycling
  experiments is used for training." `[해석]` = 용량 **유지** 60 %(감쇠 40 %)가 수명 끝.
- "the training dataset includes the first 50% of the full lifecycle degradation data, where the
  capacity has approximately **degraded to 80% of its initial value**. The test dataset contains
  data from **other cells** that have degraded 60% of their initial capacity." `[해석]` = 학습은
  ≈80 % **유지**까지, 시험은 다른 셀의 60 % **유지**까지.
- "The design space of the simulation data **should not be overly dense**, as excessive noise from
  the simulation could prevent the DNN from correctly learning the degradation trends from the
  experimental data."
- "By using only 25% of the experimental data for training, accurate estimations can be obtained".
- 통합: 시뮬레이션으로 사전학습(그림 6c) → "the deviations … are corrected using a secondary deep
  learning model" → 미세조정 vs 공동학습(joint training) 비교 → "**retraining the secondary deep
  learning model exclusively with experimental data** yields more accurate estimation results".
  [21] 인용.
- 그림 6(직접 봄): (a) Conv → GRU → Attention → Dense 블록(텐서 모양 표기 없음) · (b) 기준선
  exp → DNN → DM · (c) sim → DNN → DM ··· DNN(이차) ← exp, 첫 DNN 에서 이차 DNN 으로 곡선 화살표
  (가중치 이전). 동결 층 · 학습률 표기 없음.

### 7.2 셀 단위 독해 — "25 %" 와 "50 %" `[재현]` + `[해석]`

- 24 셀 / 3 군 = 군당 8 셀. 학습 : 시험 = 1 : 3 을 **셀 단위**로 읽으면 **학습 2 · 시험 6**
  (그림 7a · b 범례 "Cell #1–#6" 과 일치 — 시험 셀 6). 표본 단위로는 읽을 수 없다 — 학습 셀은
  수명 앞 50 % 만 쓰므로 표본 수 비가 1 : 3 이 되지 않는다.
- "25 % of the training dataset reserved for validation" — 학습 셀이 2 개라 셀 단위(0.5 셀)일 수
  없다 → **표본 단위** 검증 분할이다(무작위 표본 분할이면 같은 셀의 인접 사이클이 학습 · 검증에
  같이 들어간다).
- 초록의 "**25 %** of early-stage experimental degradation data" = 셀 25 %(2/8). 그 셀들에서도 수명
  앞 50 % 만 쓰므로 **전체 셀-수명 자료의 12.5 %** 가 학습에 들어간다(`[재현]`).
- 시험 표적이 정확히 0(신품)인 표본 수가 패널마다 4–6 개다(`[도표·벡터]` 8a 5 · 8b 6 · 8c 6 · 9a 6 ·
  9b 6 · 9c 4) → 시험 셀 6 과 맞는다(라벨이 **각 셀 자기 신품 기준** 상대값이라 신품이 정확히 0;
  모자란 칸은 겹친 표식으로 보인다).

### 7.3 `[해석]` 설계 자체가 말하는 것

- 학습 · 시험이 **같은 조건 안**에서만 갈린다 — 조건 간 일반화(25 °C 로 학습 → 35 °C 시험)는 없다.
- 사전학습 설계(완전 요인 격자, 모드 간 상관 0)와 재학습 자료(모드가 함께 자라는 실험 궤적)의
  **상관 구조가 정반대**다. 최종 모형은 후자로만 다시 학습됐으므로, 모드 간 상관을 깬 입력에
  대한 반응은 시험된 적이 없다(§9.6).
- 사전학습 라벨(설계값 — 부피분율 · 화학량론의 정확한 값)과 재학습 라벨(창 맞춤 적합값)은 **정의가
  다른 두 양**이다: 시뮬 LAM = `1 − ε/ε₀`, 실험 LAM = `1 − Q/Q_f`(맞춤 용량); 시뮬 LLI = 화학량론
  이동, 실험 LLI = 식 (4). 개념상 같은 것을 가리키지만 같은 척도인지 점검한 문장은 없다.

## 8. p.9–11 — §4.1 모드 정량 결과 · 표 1–2 · 그림 7–10

### 8.1 지표 `[인쇄, 식 (18) — 렌더 확인]`

```
Error_i = D_esm,i − D_tru,i
RMSE    = sqrt( (1/N_s) Σ (D_esm,i − D_tru,i)² )
MAE     = (1/N_s) Σ |D_esm,i − D_tru,i|
R²      = 1 − Σ (D_esm,i − D_tru,i)² / Σ (D_esm,i − D̄)²      ("D̄ refers to the average of the target values")
```

`[해석]` 인쇄된 R² 의 분모는 `Σ(D_esm,i − D̄)²`(**추정값**과 표적 평균의 차)다 — 표준 정의는
`Σ(D_tru,i − D̄)²` 다. 인쇄 오류인지 실제 계산이 그랬는지는 알 수 없다(§13 불일치 5).

### 8.2 표 1 (수동 크롭으로 열 머리 확인) `[인쇄]`

| 조건 | 25 °C@1 C | | 25 °C@2 C | | | 35 °C@2 C | | |
|---|---|---|---|---|---|---|---|---|
| 모드 | LLI | LAM_PE | LLI | LAM_PE | LAM_NE | LLI | LAM_PE | LAM_NE |
| RMSE (%) | 2.87 | 2.09 | 1.98 | 2.73 | 3.82 | 1.76 | 2.12 | 3.01 |
| MAE (%) | 2.25 | 1.67 | 1.63 | 2.09 | 3.15 | 1.44 | 1.69 | 2.51 |
| R² | 0.93 | 0.96 | 0.96 | 0.89 | 0.93 | 0.99 | 0.97 | 0.91 |

(열 머리의 조건 이름은 **렌더에는 있고 텍스트 층에는 없다** — 텍스트 추출만 보면 조건이 사라진다.)

### 8.3 표 2 (수동 크롭) `[인쇄]` — 오차 (%p)

| 조건 | 모드 | 지표 | Developed | Baseline | FCNN | SVM | GPR |
|---|---|---|---|---|---|---|---|
| 25 °C@1 C | LLI | RMSE / MAX | 2.87 / 7.51 | 4.64 / 14.36 | 4.27 / 12.98 | 5.07 / 14.49 | 7.30 / 21.21 |
| | LAM_PE | RMSE / MAX | 2.09 / 5.42 | 5.64 / 16.09 | 3.76 / 6.75 | 5.50 / 11.69 | 7.04 / 19.41 |
| 25 °C@2 C | LLI | RMSE / MAX | 1.98 / 5.11 | 3.90 / 10.52 | 6.35 / 14.55 | 3.23 / 9.26 | 4.07 / 11.87 |
| | LAM_PE | RMSE / MAX | 2.73 / 7.77 | 5.24 / 14.00 | 6.94 / 20.26 | 3.88 / 11.64 | 4.29 / 12.69 |
| | LAM_NE | RMSE / MAX | 3.82 / 7.97 | 5.75 / 15.15 | 5.86 / 13.28 | 7.09 / 26.12 | 6.78 / 15.17 |
| 35 °C@2 C | LLI | RMSE / MAX | 1.76 / 4.55 | 3.58 / 10.59 | 4.64 / 10.54 | 3.22 / 10.85 | 2.78 / 9.79 |
| | LAM_PE | RMSE / MAX | 2.12 / 6.26 | 3.83 / 10.97 | 7.13 / 19.57 | 6.25 / 17.67 | 5.83 / 16.78 |
| | LAM_NE | RMSE / MAX | 3.01 / 7.53 | 6.25 / 16.95 | 9.98 / 14.69 | 5.02 / 22.86 | 6.57 / 18.25 |

### 8.4 표 ↔ 본문 ↔ 그림 대조 `[재현]` · `[재현·벡터]`

- 표 1 RMSE 8 개 = 표 2 Developed RMSE 8 개 = 본문(§4.1) 수치 — 일치. RMSE/MAE 비 1.20–1.31.
- 초록 "RMSE < 3 % (LLI · LAM_PE), < 4 % (LAM_NE)": 최대가 2.87 · 2.73 · 3.82 → 성립.
- **"42.92 %–66.30 %" 는 최대오차(MAX) 감소율이다**: `(Baseline MAX − Developed MAX)/Baseline MAX`
  가 8 칸에서 47.70 · 66.31 · 51.43 · 44.50 · 47.39 · 57.03 · **42.94** · 55.58 % → 범위
  **42.94–66.31 %**(인쇄 42.92–66.30, 반올림 전 값으로 계산한 차이로 보인다). §4.1 의 "estimation
  accuracy improves by 47.72 % for LLI and 66.30 % for LAM_PE" 도 MAX 감소율(47.70 · 66.31)이다 —
  "accuracy" 라 부르지만 최대오차다. 같은 비교를 RMSE 로 하면 감소율 **33.57–62.94 %**.
- **기준선(같은 구조, 시뮬 없음)이 단순 방법에 지는 칸이 있다**(RMSE): 25 °C@1C LLI(FCNN 4.27 <
  4.64) · LAM_PE(FCNN 3.76 · SVM 5.50 < 5.64) · 25 °C@2C LLI(SVM 3.23 < 3.90) · LAM_PE(SVM 3.88 · GPR
  4.29 < 5.24) · 35 °C@2C LLI(SVM 3.22 · GPR 2.78 < 3.58) · LAM_NE(SVM 5.02 < 6.25). `[해석]` 비교
  방법들은 "trained using the same dataset applied to the developed model" 인데, 그것이 시뮬
  사전학습을 포함하는지 불명이다. 포함하지 않는다면 "Developed > FCNN/SVM/GPR" 는 **구조의 우위가
  아니라 시뮬 자료의 몫**이고, 구조만 보면(기준선) 단순 방법과 우열이 갈리지 않는다. "FCNN +
  시뮬 사전학습" 같은 절제(ablation)는 없다.
- `[재현·벡터]` **그림 8–9 의 산점이 곧 시험 집합이다** — 벡터 좌표로 다시 계산한 (Integration,
  Baseline) RMSE · MAX 가 표 2 와 0.01–0.02 안에서 맞는다: 25 °C@2C LLI 1.98/5.11 · 3.91/10.52,
  LAM_PE 2.73/7.76 · 5.24/14.00, LAM_NE **3.73**/7.97 · 5.77/15.14; 35 °C@2C LLI 1.78/4.55 ·
  3.58/10.59, LAM_PE 2.12/6.26 · 3.83/10.97, LAM_NE 3.01/7.53 · 6.25/16.94. 유일한 어긋남은 그림 8c
  Integration RMSE 3.73 vs 표 3.82(겹친 표식이 가려졌을 가능성).
- 그 시험 집합의 크기(`[도표·벡터]`): 25 °C@2C **LLI 163 · LAM_PE 152 · LAM_NE 116**, 35 °C@2C
  **289 · 238 · 212** — 같은 조건에서 모드마다 다르다(G11). 그림 7c · d(1 C)의 Integration 막대
  합은 ≈1,079(LLI) · ≈1,048(LAM_PE)로 시험 셀 6 × 사이클 ≈180 과 같은 크기다(겹친 막대 때문에
  근사). 그림 1f 의 라벨은 사이클마다 하나다.

### 8.5 그림 7 (1 C · 25 °C, 직접 봄 + 벡터)

- (a) LLI · (b) LAM_PE 추정 궤적, 시험 셀 6 개(Cell #1–#6). `[도표·벡터]` (b) 표식 간격 **7 사이클**,
  셀 수명 끝 사이클 155–190; 마지막 표식 값 LLI 23.0–28.7 %, LAM_PE 27.1–31.3 %.
- (b) LAM_PE 는 초기 ≈1–2 % 로 평탄하다가 셀마다 다른 시점(사이클 ≈22–64)에 **한 표식 간격(7
  사이클)에 +3.0–5.1 %p 씩 뛰는** 구간이 있다(`[도표·벡터]`). `[인쇄]` "Regarding the LAM_PE, it
  remains negligible in the early stages of aging and increases gradually as the battery ages."
  `[해석]` 이것은 **추정값**이지만 표적을 따라가도록 학습된 값이다 — 그림 9b 의 표적 간극과 같은
  종류의 "늦은 출현 + 계단" 이다.
- (c) LLI · (d) LAM_PE |오차| 히스토그램. ★ `[도표·벡터]` **Baseline 막대 폭 ≈1 %, Integration
  막대 폭 ≈0.5 %** — 막대 높이를 직접 비교하면 Integration 이 반쯤 낮아 보인다. 같은 폭(0–1 %)으로
  다시 묶으면 LLI 는 Baseline ≈306 vs Integration ≈148 + 143 = 291(**오차 < 1 % 칸은 기준선이 약간
  더 많다**), LAM_PE 는 ≈326 vs ≈208 + 201 = 409. Integration 의 이득은 **꼬리를 자르는 것**이다(최대
  7.51 · 5.42 % — 표 2 와 일치).
- `[인쇄]` "the LLI increases almost linearly as the battery ages, suggesting that the batteries
  primarily experience the SEI growth, without showing nonlinear degradation due to lithium plating."
  `[해석]` 적합 LLI 의 선형성에서 기구(SEI vs 도금)를 읽는 것은 라벨의 정확성을 전제한다.

### 8.6 그림 8 (2 C · 25 °C) · 그림 9 (2 C · 35 °C) — 직접 봄 + 벡터

- 산점 = (적합 표적, 예측). 기준선은 표적 ≈20 % 이상에서 포화(그림 8a ≈20 · 8b ≈15 · 8c ≈17 ·
  9a ≈23 · 9b ≈28 · 9c ≈16 %, `[도표]`). Integration 은 대각선을 따르되 큰 값에서 아래로 굽는다
  (8a 표적 ≈30 → 예측 ≈26; 8b · 9c 에 두 갈래).
- 그림 8b: `[도표·벡터]` 표적 정확히 0 인 6 점의 Integration 예측이 0.90–**7.77 %** — **표 2 의
  Integration 최대오차 7.77 %p 가 신품 시험 셀에서 나온다**(신품 스펙트럼 하나가 노화 셀처럼
  읽혔다). `[해석]` 셀 간 신품 산포가 오차의 최대 원천이 될 수 있다는 뜻이다(§13 불일치 12 의
  신품 스펙트럼 차이와 같은 축).
- 그림 9b: 표적 간극 6.09 → 14.40 % (§4.4 라벨 불연속).
- (d) 상자그림(|오차|): 수염 · 이상점 최대가 표 2 MAX 와 일치(`[도표]`).
- `[인쇄]` "In the advanced stages of aging, where LLI and LAM_PE exceed 20% and LAM_NE surpasses 15%,
  the estimation results of the baseline model diverge substantially from the ground truth."

### 8.7 그림 10 (직접 봄)

- 세 패널 (a) 25 °C@1C · (b) 25 °C@2C · (c) "1 C … at 35 °C"(캡션) — 가로 RMSE, 세로 최대 |오차|.
  범례 "The proposed method(*) · **ANN**(◇) · SVM(○) · GPR(□)" (본문 · 표 2 는 "FCNN").
- `[도표]` 표식 좌표가 표 2 와 맞는다 — 특히 (c) 의 제안 방법 LLI (≈1.75, ≈4.5) · LAM_PE (≈2.1,
  ≈6.2) · LAM_NE (≈3.0, ≈7.5) 는 표 2 의 **35 °C@2 C** 블록(1.76/4.55 · 2.12/6.26 · 3.01/7.53)이다
  → **캡션 (c) 의 "1 C" 는 오기**(§13 불일치 1).
- 기준선(Baseline)은 그림 10 에 없다.

## 9. p.11–13 — §4.2 민감 주파수 · 그림 11–12 · ★ 판정 (c)

### 9.1 원문 `[인쇄]`

- 그림 11(1 C · 25 °C, 시험 셀 하나 — "Since the conclusions are consistent across all batteries in
  the test dataset, only the results for one cell are shown"): LLI 는 "the highest weights are
  concentrated in two frequency ranges: **319.60–1598.01 Hz and 0.32–9.91 Hz**." "The high frequency
  range … mainly corresponds to SEI growth" · 0.32–9.91 Hz 는 "diffusion processes, which in
  themselves do not directly result in LLI" → **리튬 가둠(lithium trapping)** [36,37] 으로 설명:
  "this diffusion-controlled lithium trapping induced capacity loss arises primarily from an
  imbalance between lithiation and delithiation efficiencies. This portion of the capacity loss
  **can be mitigated or even recovered** by adjusting the charging and discharging conditions."
- LAM_PE 는 "the frequency range with the highest weights is **0.1–0.32 Hz**, followed by the range
  of **12.40–251.1 Hz**" — 확산 · 전하이동.
- 그림 12(2 C, 25 · 35 °C): "LLI is influenced by the high-frequency SEI growth process and the
  low-frequency diffusion process, while **LAM_PE and LAM_NE are primarily associated with the
  mid-frequency charge transfer process and the low-frequency diffusion process**."
- §5 한계: "**a one-to-one correspondence between frequency features and specific degradation causes
  has not yet been established.**"

### 9.2 그림 11 (직접 봄 + 벡터)

- (a) LLI · (b) LAM_PE: 초기 · 중기 · 말기 Nyquist 세 개를 가중치 색으로. (c) · (d): 가중치 vs 주파수,
  곡선 색 = SOH 1 → 0.6. `[도표·벡터]` 곡선 경로 ≈50(LLI) · ≈47(LAM_PE) 색 = 그 셀의 노화 시점 수.
- `[도표·벡터]` (c) LLI: 신품(색막대 SOH 1 쪽 끝 색) 0.0223–0.0241 (거의 균일, 1/43 = 0.0233), 가장 노화한
  곡선(색막대 하단 쪽 색) 0.0143(0.1 Hz) · 0.0293(2 Hz) · 0.0161(50 Hz) · 0.0321(1 kHz).
- `[도표·벡터]` (d) LAM_PE: 신품 0.0283(0.1 Hz) · 0.0133(2 Hz) · 0.0356(100 Hz) · 0.0166(1.6 kHz) —
  신품에서도 균일하지 않다; 가장 노화한 곡선 **0.0554**(0.1 Hz) · 0.0045(2 Hz) · 0.0474(50 Hz) · 0.0038(1.6 kHz).

### 9.3 ★ 두 모드의 "민감 주파수" 는 한 패턴의 부호 반전이다 `[재현]` · `[재현·벡터]`

- **인쇄된 네 범위가 43 점 축을 빈틈없이 나눈다** — 이상적 격자로 LAM_PE 저 0.1–0.32 Hz **6 점**,
  LLI 저 0.32–9.91 Hz **16 점**, LAM_PE 중 12.40–251.1 Hz **14 점**, LLI 고 319.60–1598.01 Hz **8 점**,
  합집합 = **43 / 43**(0.32 Hz 한 점만 공유). LLI 와 LAM_PE 의 "가장 민감한 대역" 은 겹치지도 비지도
  않는 **상보 분할**이다.
- **노화에 따른 가중치 변화(최대 노화 − 신품)의 상관 r = −0.962**(43 점) — LLI 의 가중치가 오르는
  곳에서 LAM_PE 는 내리고, 그 반대도 같다.
- **부호가 바뀌는 마디(node)가 같은 격자 구간에 있다**: LLI 0.316–0.398 · 7.94–10.0 · 251–316 Hz,
  LAM_PE 0.316–0.398 · 10.0–12.6 · 251–316 Hz. 인쇄된 범위의 경계(0.32 · 9.91/12.40 · 251.1/319.60
  Hz)가 바로 이 마디다.

`[해석]` softmax 주의는 합이 1 로 묶여 있어 한 곳이 오르면 다른 곳이 내린다. 두 모드의 가중치
변화가 −0.96 으로 거울상이고 마디까지 같다는 것은 **두 모드가 서로 다른 스펙트럼 서명을 쓴다는
증거가 아니라, 같은 노화 변화를 반대 부호로 읽는다는 증거**에 가깝다. 출력층 차원이 "예측 자료의
차원"(§6.1)인데 그림 11 은 모드마다 다른 가중치를 보이므로, 모드별 모형(또는 모드별 주의)이었던 것으로
보인다 — 독립으로 학습된 두 모형이 거울상 패턴에 이른 이유는 원문으로 확인할 수 없다.

### 9.4 그림 12 (직접 봄)

- 색막대에 **숫자가 없다**("Low ··· Weights ··· High") — 크기 비교 불가.
- `[도표]` (a) LLI 25 °C: 빨강 · 주황이 **말기 스펙트럼의 최고주파 끝 한두 점**(≈18 mΩ, −Im ≈ −0.6 —
  유도성 쪽 · ≈0.2)에만 있고 나머지는 파랑. (d) LLI 35 °C: 빨강이 **저주파 꼬리 끝**. → LLI 의 최고 가중치 위치가 온도에 따라 고주파
  끝 ↔ 저주파 끝으로 바뀐다. 본문 요약("high-frequency SEI + low-frequency diffusion")은 두 패널을
  합친 것이다.
- `[도표]` **(b) LAM_PE ≈ (c) LAM_NE** (25 °C, 둘 다 아크 꼭대기 빨강) · **(e) LAM_PE ≈ (f) LAM_NE**
  (35 °C, 둘 다 꼬리 끝 빨강 + 아크 꼭대기 주황) — 두 LAM 의 주의 지도가 사실상 같다. 35 °C 에서는
  **LLI(d) 도 꼬리 끝이 가장 빨갛다** → 셋 모두 같은 자리.

### 9.5 `[해석]` EIS 측정 끝점의 문제

EIS 는 "충전(또는 방전) 완료 + 15 분 휴지" 뒤에 잰다. 1–2 C **CC 전용** 사이클에서 그 끝점은 고정 SOC
가 아니라 **전압 컷오프에 닿은 상태**이고, 노화로 `R` 이 크고 창이 움직이면 그 상태의 두 전극
화학량론이 함께 움직인다. 모형의 `i0` · OCP 기울기 · 확산 임피던스는 화학량론의 함수이므로, EIS 가
보는 노화 변화의 일부는 **"끝점에서 전극들이 어디에 앉아 있는가"**, 곧 창 맞춤이 보는 것과 같은
근원의 정보다. 그림 1c(SOC 100 % vs 0 % 의 큰 차이)는 이 경로의 크기가 작지 않음을 보인다. EIS 가 창
정보와 **독립인 채널**을 더하는지는 이 편으로 가를 수 없다.

### 9.6 ★ 판정 (c) — EIS 는 우리 축퇴를 깨는 새 관측인가

| 물음 | 이 편 안의 근거 | 판정 |
|---|---|---|
| (i) LLI ↔ LAM 을 가르는 **반대로 움직이는 채널**을 주는가 | 주의 패턴이 한 노화 변화의 부호 반전(r = −0.962, 마디 공유, 43 점 상보 분할, §9.3). 라벨이 함께 자란다(§4.4). 단일 모드 시험 · 상관을 깬 시험 · 조건 간 시험 0. 사전학습은 상관 0 격자였지만 최종 모형은 실험 자료로만 재학습 | **이 편으로는 판단 불가** — 독립 채널의 증거는 0 이고, 동시 진행 상관을 학습한 것과 구별하는 대조가 없다 |
| (ii) LAM_PE ↔ LAM_NE 를 가르는가 | 그림 12 b ≈ c, e ≈ f; SI 표 S2 가 둘 다 "Related to R_ct and Y0"; 결론이 "LAM exhibits sensitivity to …" 로 묶는다 | **이 편 근거로는 불성립** — 같은 대역에 앉는다 |
| 시뮬 통합(기준선 대비)으로 정확도가 오른 것은 무엇 때문인가 — 두 모형 모두 같은 EIS 입력 | 비교는 "적합 라벨 대비" 이고, 이득의 대부분은 수명 후반 **외삽 범위**를 시뮬 자료가 채운 것(기준선 포화, §8.6) | 축퇴 해소가 아니라 **표적 범위 확장**의 효과로 읽힌다 |

**결론 (c)**: 이 편은 "EIS 가 full-cell 곡선의 모드 축퇴를 깬다" 를 **보이지 않는다.** 이 편이 보이는
것은 "같은 조건 · 같은 상관 구조 안에서, 시뮬 사전학습이 적합 라벨의 외삽 범위를 넓힌다" 까지다.
EIS 가 독립 채널인지 판정하려면 §17.4 의 실험 3 같은 **상관을 깬 합성 시험**이 필요하다.

## 10. p.13–14 — §5 결론 · 한계 `[인쇄]`

- 주장: "Minute-level impedance spectrum tests are utilized to estimate the degree of degradation
  modes across different aging stages, eliminating the need for destructive disassembly of the
  battery." · "its design based on impedance spectra ensures **inherent generalizability across
  various battery chemistries and formats**" · "indicating its potential to adapt to fast-charging
  scenarios and high/low temperatures." `[해석]` 화학 · 형식 일반화는 시험된 적이 없다(NMC 한 종,
  같은 조건 안 분할).
- 한계: 임피던스 모형에 SEI 성장 · 리튬 도금 · 전해질 분해 · 가스 · 입자 균열을 넣어야 한다; "it does
  not explicitly differentiate the specific physical mechanisms underlying these degradation modes";
  "a one-to-one correspondence between frequency features and specific degradation causes has not yet
  been established"; "the degradation dataset only for NMC batteries is currently being developed."
- `[해석]` **라벨의 불확실성 · 식별성은 한계 목록에도 없다.**

## 11. SI 대조 — Note 1–6 · 표 S1–S2 · 그림 S1–S6 ↔ 본문 (전부 열어 봄)

| SI 항목 | 내용 (`[인쇄]` / `[도표]`) | 본문 참조 · 대조 |
|---|---|---|
| Note 1 · 표 S1 | 군 × 셀 #1–#8 초기 용량(Ah). "Group 1: 25 ℃ @ 1 C" 1.905–1.991 · "**Group 2**: 25 ℃ @ 2 C" 1.694–1.771 · "**Group 2: 35 ℃ @ 1 C**" 1.778–1.827. 각주 "integrating the current over the charging process under different current rates" | §2 "Supplementary Note 1". ⚠ 셋째 행의 군 번호 · 율이 본문과 다르다(§13 불일치 1) |
| Note 2 · 그림 S1 | K-K: Metrohm Autolab **Nova** 소프트웨어, 상대잔차 `Δ_Re(f) = (Z′(f) − Ẑ′(f)) / abs(Z(f))`, `Δ_Im(f) = (Z″(f) − Ẑ″(f)) / abs(Z(f))`(원문 분모는 측정 임피던스의 크기 절댓값 기호) [R1 Schönleber 2014]. 그림 S1 (a)–(c) K-K 맞춤 Nyquist, (d)–(f) 잔차. `[도표]` 잔차 (d) 1 C/25 °C ±0.3 % · **(e) 2 C/25 °C 최저 ≈ −0.95 %**(≈2.5 Hz, 허부) · (f) 2 C/35 °C ±0.3 %. 캡션은 "(a)…(c) … (b)…(e) … (c)…(f)" | §2 "within 1%" 성립, 단 (e) 는 한계 바로 안. ⚠ 캡션 패널 문자 오류(c 두 번 · d 없음). 신품만 |
| Note 3 · 그림 S2 · S3 · 표 S2 | ECM `R_s − (R_SEI ∥ CPE_SEI) − ((R_ct + W) ∥ CPE_ct)`. 그림 S3: 2 C 두 군, 셀 하나, 사이클 0–80 (10 간격 9 점). `[도표]` (a) 25 °C: R_s 13.3 → 15.7 · R_SEI 10.5 → 13.0 · R_ct 8.6 → ≈12 (50 사이클 뒤 포화) · Y0 2.8 → 1.4 × 10⁵. (b) 35 °C: R_s **8.8** → 9.1 · R_SEI 9.3 → 11.6 · R_ct 5.5 → 8.3 · Y0 3.0 → 1.6 × 10⁵ (mΩ · Mho·s^½). 표 S2: ECM 정성 — LLI "Related to R_SEI", **LAM_PE · LAM_NE 둘 다 "Related to R_ct and Y0"**; 제안 방법 정량 ✓ ✓ ✓. "The ECM-based diagnostic method can only provide qualitative evolution trends of the LLI and LAM for the full-cell." | §2 "Supplementary Note 3" — "a clear upward trend … in the SEI resistance, charge transfer resistance and diffusion resistance" 와 맞다. ⚠ 35 °C 의 R_s ≈8.8 mΩ 은 같은 조건 Nyquist 의 고주파 실축 교차(그림 1a 15.82 mΩ `[도표·벡터]`)보다 ≈7 mΩ 낮다 — `[해석]` ECM 맞춤이 R_s 와 R_SEI 사이로 저항을 옮긴 것으로 보인다(ECM 요소 분할의 비유일성) |
| Note 4 | COMSOL AC 섭동 식 두 줄 + 경계조건(§5.2). 매개변수 0 | §3.3 "The corresponding equations are presented in Supplementary Note 4" — "equations" 는 있으나 **값은 없다** |
| Note 5 · 그림 S4 · S5 | S4 Bode: 시뮬 vs 측정(§5.3). S5: ECM 매개변수 막대 둘(시뮬 · 측정) — `[도표]` R_s 10.0 / 9.6 · R_SEI 9.5 / 9.6 · R_ct 7.9 / 7.5 mΩ. **범례 없음** | §3.3 "Bode plots in Supplementary Note 5" · "extracted key parameters are provided in Supplementary Note 5" — 어느 막대가 시뮬인지 SI 에 없다 |
| Note 6 · 그림 S6 | GRU 셀 도식 — 갱신 게이트 배치가 식 (9) 와 반대, `⊙` = "Matrix multiplication" | §3.4.1 "The structure of the GRU can be seen in Supplementary Note 6" |

## 12. 재현 · 산술 정리 `[재현]` (scratch 스크립트, 입력은 전부 인쇄값 · 벡터 좌표)

| # | 대상 | 결과 |
|---|---|---|
| R1 | 1 C ↔ 전류 | 1 C = 2.4 A(공칭 2.4 Ah), 2 C = 4.8 A. 표 S1 군 평균 1.947 / 1.727 / 1.804 Ah = 공칭의 81.1 / 72.0 / 75.2 % |
| R2 | 셋째 군 율 | 표 S1 평균 순서 1.947(25 °C·1 C) > **1.804(셋째)** > 1.727(25 °C·2 C). `[해석]` 35 °C·1 C 라면 ≥ 25 °C·1 C 여야 한다(높은 온도 = 작은 분극; 본문도 "The capacity charged and discharged at 35 °C is higher than that at 25 °C" 를 인쇄). 사이에 있는 것은 **35 °C·2 C** 와 맞는다 |
| R3 | 셀 분할 | 군당 8 → 학습 2 : 시험 6(셀 단위), 검증 25 % = 표본 단위, 학습 자료 = 전체 셀-수명의 12.5 % |
| R4 | 주파수 점 | 51 = 5 × 10 + 1, 지운 점 8, 남는 최고 10^3.2 = 1584.9 Hz (인쇄 1598.01) |
| R5 | 민감 대역 | 6 + 16 + 14 + 8 = 43 점 상보 분할 (§9.3) |
| R6 | 표 1 ↔ 표 2 ↔ 본문 | RMSE 8 개 일치 |
| R7 | "42.92–66.30 %" | MAX 감소율 42.94–66.31 % (반올림 차); RMSE 감소율 33.57–62.94 % |
| R8 | 식 (1) ↔ (4) | 리튬 재고 보존 성립 — `p` 가 리튬화 분율일 때만 |
| R9 | 그림 5a RMSE | 벡터 43 점 복소 거리 RMS 0.755 mΩ ≈ 인쇄 0.76 |
| R10 | 그림 8–9 산점 | 12 계열 중 11 개가 표 2 RMSE · MAX 를 0.01–0.02 안에서 재현 |
| R11 | 그림 11 가중치 | 신품 · 최대 노화 곡선 합 1.000(43 점); 변화의 상관 −0.962; 마디 공유 |

## 13. 내부 불일치 · 서술 오류 (판정 (f))

1. **셋째 군의 율** — 본문 §2 · §4.1 · 그림 9 캡션 · 그림 12 캡션 · 표 1 · 표 2 열 머리 · 그림 1b · 1f 범례 ·
   SI 그림 S1 · S3 캡션은 **"2 C, 35 °C"**; SI 표 S1 은 **"Group 2: 35 ℃ @ 1 C"**(군 번호 "Group 2" 가 두
   번), 그림 10 캡션 (c) 는 **"1 C … at 35 °C"**. **판정: 35 °C@2 C 가 맞다** — 근거 셋: (i) 그림 10c 의 수치
   = 표 2 의 35 °C@2 C 블록(§8.7), (ii) 표 S1 용량 순서(R2), (iii) 그림 1b · 1f 범례. 표 S1 의 "1 C" · 두 번째
   "Group 2" 와 그림 10 캡션은 오기다.
2. **그림 1f ↔ 그림 8a 의 25 °C@2C LLI** — 그림 1f 궤적 최대 **61.6 %**(사이클 83, `[도표·벡터]`) vs 같은
   조건 시험 셀 표적 최대 **30.9 %**(그림 8a). 두 배다. 그림 1f 의 셀이 학습 셀이면 같은 조건 · 같은 초기
   용량(표 S1 변동계수 1.6 %)의 셀 사이에서 적합 LLI 가 두 배 차이 난다는 뜻이고, 표기 · 정규화가 다른
   것이라면 원문에 설명이 없다. 원문으로 해소 불가(G16). (35 °C 는 그림 1f 33.9 % ↔ 그림 9a 33.5 % 로 맞는다.)
3. **그림 1b ↔ 표 S1 ↔ 그림 1d 의 용량** — `[도표]` 그림 1b 2 C 충전 용량(≈1.60 · ≈1.68 Ah)이 표 S1 의
   같은 군 범위(1.694–1.771 · 1.778–1.827)보다 작은데, 표 S1 은 "충전 과정의 전류 적분" 이다. 그리고 그림
   1d 의 2 C 방전 용량(≈1.77 · ≈1.85)이 그림 1b 의 충전 용량보다 크다. `[해석]` 두 곡선이 같은 사이클이
   아니거나, 충전에 원문에 없는 CV 단계가 있다(본문은 CC 만 말한다; CV 0 회).
4. **그림 10 범례 "ANN"** ↔ 본문 · 표 2 "FCNN".
5. **식 (18) R² 의 분모** `Σ(D_esm,i − D̄)²` — 표준 정의(`Σ(D_tru,i − D̄)²`)와 다르다.
6. **식 (9) ↔ SI 그림 S6** — 갱신 게이트 배치 반대; `⊙` 를 본문은 element-wise, SI 는 "Matrix
   multiplication".
7. **"ground truth" 의 이중 사용** — 그림 4b 범례에서는 측정 전압, 그림 8–9 · 본문에서는 적합 라벨.
8. **GRU 의 "long-term dependencies in battery degradation"** ↔ 식 (11) · 그림 2 의 주파수 시퀀스(§6.2).
9. **"25 %" ↔ "initial 50 %"** — 셀 25 % × 수명 50 % 로만 양립; 초록은 둘을 하나로 합쳐 쓴다(§7.2).
10. **"estimation accuracy improves by 47.72 % … 66.30 %"** — 최대오차 감소율이다(R7).
11. **그림 5c 의 "significant changes"** — 그려진 64 개에서 변화는 저주파 꼬리에 몰리고 아크는 −Im 0.1 mΩ
    안에서 고정(§5.3).
12. **신품 35 °C 스펙트럼이 그림마다 다르다** — 그림 1a 실축 교차 15.82 mΩ(`[도표·벡터]`) · 아크 끝
    ≈22 mΩ(`[도표]`) ↔ 그림 S1c 시작 ≈17.5 · 아크 끝 ≈25.8 mΩ(`[도표]`, 래스터 ±0.3). 본문은 "35 °C shifts leftward relative to
    25 °C" 인데 그림 S1 에서는 35 °C(≈17.5)가 25 °C(≈16.5)보다 오른쪽이다. 셀 표기가 없어 셀 간 차이인지
    판정 불가 — 그 크기(수 mΩ)는 노화 변화(그림 1e)에 견줄 만하다.
13. **SI 그림 S1 캡션 패널 문자** — "(a)…relative residual (c)" 로 시작해 (c) 가 두 번, (d) 가 없다.
14. **그림 7c · d 의 막대 폭이 다르다** — Baseline ≈1 %, Integration ≈0.5 % (§8.5).
15. **시험 표본 수가 모드마다 다르다** — 163/152/116 · 289/238/212, 본문은 "all batteries in the test
    dataset"(G11).
16. **SI 그림 S5 범례 없음** — 시뮬 · 측정 막대 구별 불가.
17. **표 1 열 머리의 조건 이름이 텍스트 층에 없다**(렌더에만) — 텍스트 기반 인용 시 조건이 사라진다.

## 14. 어휘 전수 (합자 U+FB01/FB02 와 줄끝 하이픈을 푼 뒤, 본문 참고문헌 제외)

본문 PDF 에 합자 글리프 **97 개**가 있다(SI 0) — 풀지 않으면 `identiﬁab` · `ﬁtting` · `conﬁdence`
류가 통째로 0 이 된다([[mode-identifiability-unmeasured-lineage]] 의 셋째 함정). 그림 속 글자는 벡터
윤곽이라 텍스트 층에 없다(세지 않았다).

| 어휘 | 본문 | SI | 비고 |
|---|---|---|---|
| `identifiab*` | **0** | 0 | |
| `degenera*`(degradation 제외) | **0** | 0 | |
| `uniqu*` | **0** | 0 | |
| `uncertain*` | **0** | 0 | |
| `error bar` · `confidence` | **0** · **0** | 0 | |
| `multi-start` · `initial guess` | **0** | 0 | "initial value" 3 회는 전부 "% of its initial value" |
| `bound*` · `repeat*` · `cross-validation` | 0 · 0 · 0 | 0 | |
| `standard deviation` | 1 | 0 | 식 (16) Z-점수 정규화 |
| `particle swarm` | 2 | 0 | 설정 0 |
| `ground truth` | 4 | 0 | 전부 적합 라벨(본문); 그림 4b 범례는 측정 전압(그림 글자, 미계수) |
| `target value` | 5 | 0 | 전부 적합 라벨 |
| `half-cell` · `OCP` | 3 · 10 | 0 | |
| `sensitiv*` · `interpretab*` · `attention` | 11 · 6 · 30 | 0 | |
| `overfit*` | 3 | 0 | 메커니즘 모형 · dropout · 통합 전략 문맥 |
| `film resistance` · `double layer` · `specific surface` | 0 · 0 · 0 | 0 | 시뮬레이터 매개화 공백(G7) |
| `volume fraction` · `stoichiometr*` | 2 · 1 | 0 | §3.3 |
| `Kramers` | 1 | 0 | |
| `lithium plating` | 5 | 0 | |

`[해석]` [[mode-identifiability-unmeasured-lineage]] 표의 "침묵의 형태" 로 적으면 — **적합값에
"ground truth" 라는 이름을 붙여 침묵을 지운다.** 라벨의 비유일성 문제가 어휘 수준에서 아예 생기지
않는 구성이다. PSO 로 5 매개를 맞추면서 `uniqu*` · `uncertain*` · `error bar` · `multi-start` 가 전부
0 인 것은 같은 그룹의 Wang (Xiong) 2025(GA, 8 매개, 전부 0)와 같은 형이다.

## 15. Xiong 그룹 계열 · 자기 인용 (판정 (g))

`[재현]` 참고문헌 목록에서 직접 센 값(37 편 파싱 확인):

| 저자 | 편수 | 번호 |
|---|---|---|
| **R. Xiong** (교신) | **9 / 37 (24.3 %)** | [2] · [5] · [9] · [10] · [11] · [18] · [26] · [28] · [29] |
| Y. Sun (제1저자) | 3 | [2] · [10] · [29] |
| F. Sun | 4 | [10] · [11] · [18] · [26] |
| W. Shen | 5 | [5] · [9] · [11] · [18] · [26] |
| J. Tian | 5 | [2] · [11] · [18] · [26] · [29] |
| H. Li | 4 | [2] · [10] · [28] · [29] (Mälardalen 의 Hailong Li 와 같은 사람인지 목록으로는 확인 불가) |

- 라벨 절차의 출처 **[26] = J. Tian, R. Xiong, W. Shen, F. Sun, *Energy Storage Mater.* 37 (2021)
  283–295** (`[인쇄]` 목록 그대로; 제목은 이 편 목록에 없다 — 이 위키의 thelen2024 digest 가 Thelen
  2024 리뷰 목록에서 옮긴 제목은 "Electrode ageing estimation and OCV reconstruction").
- "완전지 임피던스만으로는 전극 수준 모드를 정확히 진단할 수 없다" 의 출처 **[11]** 도 같은 그룹
  (Tian · Xiong · Shen · Sun 2020 *Sci. China Technol. Sci.* 63, 2211–2230).
- 시뮬레이션 EIS 자료 생성의 출처 [27, 28] 중 **[28] = Y. Tian, C. Lin, X. Meng, X. Yu, H. Li, R. Xiong,
  *eScience* 5 (2025) 100325** 도 같은 그룹.

**19 번(Wang, Xiong, Shen, Sun 2025 *Applied Energy* 393, 126094 —
`raw/papers/wang2025_aging-induced-rate-independent-li-plating.md`)과의 방법 공유** `[해석]`:
- 공통: 반쪽전지 OCP + 창 좌표(전극 용량 · 오프셋) 맞춤을 **메타휴리스틱**(19 번 GA · 이 편 PSO)으로
  돌리고, **유일성 · 불확실성 어휘 0**; 교신 Xiong; **Peng Wang** 이 19 번 제1저자이자 이 편 제3저자.
- 차이: 19 번은 **0.05 C 의사-OCV** 를 맞추고 음극 곡선을 구간별로 늘려 **자유도 4 → 8**, 반쪽전지를
  과방전까지 쟀다. 이 편은 **1–2 C 사이클 충전 곡선**에 **창 4 + 상수 R** 을 맞추고 OCP 는 신품 한 번.
  19 번이 이 편의 [26] 을 인용하는지는 19 번 digest 에 기록이 없다(확인 필요).
- `bms-balancing/docs/LIT_19_20_FOR_NEW_MODEL.md` §1 이 19 번에서 가져온 구분 시험(T1–T5)은 저율 곡선
  전제라 이 편 라벨(1–2 C)에는 그대로 걸리지 않는다.

## 16. 판정 요약 (a)–(c)

| | 판정 | 핵심 근거 |
|---|---|---|
| (a) 라벨 층위 | **적합값** — "ground truth" = 반쪽전지 창 5-매개 PSO 맞춤 출력. "RMSE < 3 %" = DNN ↔ 적합 라벨 (%p). 라벨 식별성은 안 잼 | §2 · 식 (18) · 그림 3; 어휘 0; 그림 9b 라벨 간극 6.09 → 14.40 % |
| (b) 시뮬레이션 층 | "LAM ↔ 중주파 전하이동" 은 이 편 안에서 **물리 발견으로도, 시뮬레이터 각인으로도 확인되지 않는다** — 그려진 64 개 시뮬 스펙트럼에서 아크는 고정; 최종 모형은 실험 자료로만 재학습. 막 저항 · 비표면적 정의 미인쇄 | 그림 5c 벡터; §3.5; SI Note 4 |
| (c) EIS 가 새 관측인가 | (i) LLI ↔ LAM: **판단 불가**(독립 채널 증거 0, 상관 학습과 가르는 대조 0) · (ii) LAM_PE ↔ LAM_NE: **불성립**(같은 대역) | §9.3 r = −0.962 · 그림 12 · 표 S2 |

## 17. ★ 우리 열화 정량화에 적용 가능한가 (판정 (d), 전부 `[해석]`)

우리 열화 정량화 = full-cell 곡선(pOCV · dV/dQ · dQ/dV)의 **α·β 창 맞춤 → LLI/LAM_PE/LAM_NE**, PyBaMM
합성 truth 격자로 복원 채점(`degradation-degeneracy/docs/RESULTS.md` "질문" · "핵심 결론";
`docs/07_LAM_LLI.md`; `docs/09_22P_GAP.md` §0).

### 17.1 ① 가져올 수 있는 것

| 항목 | 이 편의 형태 | 우리 쪽에서의 쓸모 | 조건 |
|---|---|---|---|
| EIS 를 관측으로 더하는 설계 | 충전 · 방전 끝 + 15 분 휴지, 0.1 A 진폭, 10 kHz–0.1 Hz 10 점/decade, 유도성 8 점 제거 → 43 점 | `mode-observability` Phase 2 의 실측 대조 층(Zhang 2020 의 state V · IX 와 같은 "끝점 + 15 분 휴지" 구조 — [[zhang2020-eis-aging-dataset]]) 에 **두 번째 실셀 형식**으로 | 데이터 비공개(§18) — 형식만 가져온다 |
| 합성 사전학습 → 실측 미세조정 | 완전 요인 격자 1,000 개 사전학습, 실험으로 재학습(미세조정 > 공동학습) | Phase 3 의 학습 설계 **견본** — 우리는 합성 쪽에 참값이 있으므로 "사전학습만" · "재학습 뒤" 를 **참값 대비**로 채점할 수 있다(이 편은 못 한다) | 사전학습 라벨과 재학습 라벨의 정의를 맞춘다 |
| 주의 가중치 | 43 점 softmax | 해석 도구로는 **가져오지 않는다**(§9.3 의 상보 분할); 대신 **두 모드의 가중치 변화 상관**을 진단 지표로 — 거울상이면 "같은 신호의 부호 반전" 경보 | |
| 데이터 분할 | 셀 단위 학습 2 : 시험 6, 수명 앞 50 % 만 학습 | 우리 Phase 3 에 **셀(조건) 단위 분할 + 외삽 시험**을 기본으로; 이 편이 안 한 **조건 간 분할**을 더한다 | |

### 17.2 ② 우리가 이 편에 공급할 수 있는 것

- **라벨 식별성 점검.** 이 편의 라벨 모형은 우리 창 대수에 `R` 하나를 더한 것이다(식 1–2). 우리 합성
  truth 격자에서 1 C · 2 C CC 충전 곡선을 만들고(PyBaMM 은 이미 율을 바꿔 돌릴 수 있다) **식 (1)–(4)
  그대로** 5 매개를 다중 시작으로 맞추면, (i) 라벨 오차가 **어느 방향**으로 새는지(`(1,1,1)` 공통 모드?
  `R ↔ p0 ↔ LLI`?), (ii) 그 크기가 이 편의 DNN RMSE(2–4 %p)와 견줘 얼마인지가 나온다. 라벨 오차가 DNN
  오차와 같은 자릿수라면 **표 1 의 정확도는 라벨 잡음 바닥 아래를 재고 있는 것**이다.
- **null 방향 진단** — Phase 1c 의 `JᵀJ` 를 5 매개 판으로. `R` 열이 창 열들과 얼마나 평행한지가 곧 "사이클
  전류 곡선을 써도 되는가" 의 답이다. 우리 RESULTS 가 스스로 "pOCV 급 상한" 이라 적은 그 바깥(운용 율)을
  이 실험이 처음으로 채운다.
- **OCP 오차 문턱** — 우리 `degradation-degeneracy/docs/09_22P_GAP.md` §0 · §7.10 은 우리 셋업에서 PE/NE 를
  가르는 **유일한 조합**(전 범위 반쪽전지 기준 + pocv · dV/dQ · dQ/dV)조차 PE OCP 계통 오프셋이 **mV 한 자리
  수**에 이르면 무너진다고 보고한다(수치는 그 문서). 이 편의 맞춤 잔차 6.55–7.52 mV 는 모형 불일치(OCP 오차 +
  상수 `R` 로 못 잡는 동역학)가 그 자릿수라는 뜻이고, OCP 는 1/20 C 코인셀 곡선 하나(충 · 방전 중 무엇인지
  미상, G6)다 → **LAM_PE ↔ LAM_NE 라벨 분할은 우리 기준으로 믿을 수 있는 영역 밖에 있을 공산이 크다.**
  (조건: 이 편의 잔차가 OCP 오차인지 동역학 오차인지는 구분되지 않는다 — 비교는 자릿수 수준이다.)

### 17.3 ③ 그대로 쓰면 안 되는 것

1. **적합 라벨을 정답처럼** — 이 편의 RMSE · R² · 최대오차는 전부 적합 라벨 대비다. 인용할 때 반드시
   "적합 라벨 대비" 를 붙인다. 표 1 의 모드별 값 셋을 독립 정확도로 쓰지 않는다(§4.4).
2. **합성 각인** — 시뮬레이터 매개화가 인쇄되지 않았고, 그려진 시뮬 스펙트럼은 아크를 안 바꾼다. 이 편의
   "LAM ↔ 중주파" · "LLI ↔ SEI 고주파" 를 우리 Phase 2 의 **사전 가설**로 가져오지 않는다.
3. **군 간 조건 불일치** — 셋째 군의 율이 SI · 캡션에서 엇갈린다(§13-1). 이 편의 35 °C 수치를 쓸 때 "35 °C@2 C
   (본문 · 표 기준)" 로 적는다.
4. **주의 가중치를 기구 귀속 근거로** — §9.3.
5. **"25 % 자료로 충분"** — 같은 조건 안의 외삽일 뿐 조건 간 일반화가 아니다.
6. **용량 표기** — "1 C" 는 공칭 2.4 Ah 기준인데 실사용 용량은 그 72–81 %; 수명 끝 "60 %" 는 **유지율**.

### 17.4 가장 값싼 검증 실험 (제안만 — 실행 · 코드 변경 없음. RUN_SCOPE · 위성 코드는 건드리지 않는다)

`mode-observability` 의 언어로:

| # | 실험 | 무엇을 재나 | 비용 | 판정 기준 |
|---|---|---|---|---|
| 1 | **Phase 3-0 "라벨 맞춤의 식별성"** — 봉인된 반쪽전지 OCP 캐시로 이 편의 식 (1)–(2) 를 1 C · 2 C 에서 계산(창 대수, 동역학은 상수 `R`)하고 5×5 `JᵀJ` 를 낸다. 같은 격자를 PyBaMM 1 C · 2 C 로 돌린 곡선에 5 매개 다중 시작 맞춤도 한다 | 최소 특이벡터의 (LLI, LAM_PE, LAM_NE, R) 성분 — **`R ↔ p0 ↔ LLI` 별칭**과 `(1,1,1)` 공통 모드의 결합; 다중 시작 산포 | 창 대수 판 초 단위, PyBaMM 판 분 단위 (Phase 1c · 1j 의 기존 경로 재사용) | 최소 특이벡터에 `R` 성분이 크면 "사이클 전류 곡선 + 상수 R" 라벨은 LLI 를 R 과 섞는다 |
| 2 | **Phase 3-1 "라벨 상속"** — 같은 합성 격자에서 (i) 참 라벨, (ii) 실험 1 의 5 매개 맞춤 라벨을 만든다. 같은 입력(Phase 1–2 의 feature 또는 합성 스펙트럼)으로 회귀기(README 계획대로 RF/GBM)를 두 번 학습 | 모형 출력 − 참값 오차를 (1,1,1) · 실험 1 의 null 방향에 사영한 성분 — **적합 라벨로 학습하면 오차가 null 방향으로 몰리는가** | sklearn · 분 단위 | 라벨 맞춤 null 방향 성분이 "참 라벨 학습" 대비 유의하게 크면 상속 |
| 3 | **Phase 2-EIS "상관을 깬 시험"** — 선형화 SPM 전달함수(Bizeray 2019 형, [[spm-grouped-parameter-identifiability]])로 프로토콜 끝점(1–2 C CC 4.2 V 도달 + 휴지) 임피던스의 모드 Jacobian 을 계산하고, 모드가 **함께 자라는** 조합으로 학습한 회귀기를 **반대로 움직이는**(LLI↑ · LAM↓) 조합으로 시험 | (i) EIS 의 모드 감도를 OCV 창 맞춤의 null 방향(`(1,1,1)` 근처)에 사영한 크기, (ii) 동시 성장 상관을 깬 시험에서 오차가 터지는가 | 해석적 전달함수면 새 의존성 없이 분 단위. P2D 임피던스(PyBaMM EIS 등)는 **새 의존성 → 승인 사항** | (i) 그 사영이 0 에 가까우면 EIS 는 그 축퇴를 못 깬다([[constrained-crb-identifiability]] 의 "새 감도 열 ≠ 0" 조건); (ii) 터지면 이 편 형식의 정확도는 상관 학습이다 |

## 18. 데이터 · 재현성 (판정 (e))

- **데이터 · 코드 공개: 없음.** "Data availability" 절이 없고, 공개 문장은 "Supplementary data to this article
  can be found online at https://doi.org/10.1016/j.jechem.2025.05.014." 하나뿐(SI = 이 5 쪽).
- **K-K 는 신품만**(군당 1 스펙트럼, 그림 S1) — 학습 · 시험의 대부분인 노화 스펙트럼은 검정 기록 없음. 그리고
  2 C/25 °C 신품의 허부 잔차가 ≈ −0.95 % 로 1 % 기준 바로 안이다(`[도표]`).
- **15 분 휴지 스펙트럼의 비평형 가능성** `[해석]` — 1–2 C CC 직후 15 분은 고상 농도 구배가 다 풀리기에 짧을
  수 있고, 0.1 Hz 부근(측정에 수십 초)은 이완 중의 표류를 같이 잰다. 그 저주파 점들이 **LAM_PE 의 최고 가중치
  대역(0.1–0.32 Hz)** 이자 시뮬 스펙트럼이 가장 크게 변하는 자리다. 노화 셀은 확산 저항이 커서(그림 S3 Y0
  감소) 이완이 더 느리다. 원문은 이를 논의하지 않는다.
- **온도는 챔버 주변 온도**(`[인쇄]` "external ambient temperature") — 2 C 에서 셀 내부 온도는 더 높다(측정 0).
- **재현에 필요한데 없는 것**: 셀 형식(G1) · PSO 설정(G3) · 맞춤 창(G4) · COMSOL 매개변수(G7) · 입력 스펙트럼
  선택(G9) · 셀 배정(G10) · 초매개변수(G12).
- 측정 장비 `[인쇄]`: Gamry Interface 5000P (EIS) · K-K 는 Metrohm Autolab Nova 소프트웨어 · 학습은 Keras/
  TensorFlow · i7-12700H CPU.

## 19. ★ 누락된 논문 — 후속 후보 표 (판정 (h))

참고문헌 [1]–[37] 중 우리 축(라벨 식별성 · EIS ↔ 모드 · 합성 사전학습 · 열화 모드 ML · DRT 정칙화 · Li
trapping)에 닿는 것을 이 위키에서 grep 했다(저자 · 저널 · 권 · 쪽 · 번호 여러 형태, 2026-10-02 기준). 원문 참고문헌은 **제목을 인쇄하지 않는다**(Elsevier 번호 형식) — 아래 제목은 이 위키의 다른
digest 가 옮긴 경우에만 적고 출처를 단다.

**있는 것**: [3] Birkl 2017 *JPS* 341, 373 — `raw/papers/birkl2017_degradation-diagnostics-ocv.md`;
[17] Zhang 2020 *Nat. Commun.* 11, 1706 — `raw/papers/zhang2020_eis-gpr-capacity-rul.md` ·
[[zhang2020-eis-aging-dataset]].

**없는 것** (★ 순; "언급만" = 다른 digest 의 인용 행으로만 있고 digest 없음):

| ★ | 번호 · 서지 (`[인쇄]` 목록 그대로) | 이 편에서 무엇의 근거로 인용됐나 | 위키 상태 | 왜 우리에게 필요한가 |
|---|---|---|---|---|
| ★★★ | **[26]** J. Tian, R. Xiong, W. Shen, F. Sun, *Energy Storage Mater.* **37** (2021) 283–295 | "OCP … measured only once under the fresh-cell condition [26]" — **라벨 절차의 원전** | 언급만 (thelen2024 digest 후속 표, 제목 "Electrode ageing estimation and OCV reconstruction") | Xiong 그룹 창 맞춤의 원형 — 유일성 · 불확실성 · 해체 검증을 했는지, PSO 설정이 있는지. 이 편 라벨의 신뢰도가 여기서 정해진다 |
| ★★★ | **[21]** A. Thelen, Y.H. Lui, S. Shen, S. Laflamme, S. Hu, H. Ye, C. Hu, *Energy Storage Mater.* **50** (2022) 668–695 | "Capacity is the high-level metric … [21]" · "Simulation data is integrated … through the incremental learning approach as shown in Fig. 6c [21]" — **통합 전략의 원전** | 언급만 (navidi2024 digest `[30]`, thelen2024 digest 후속 표 "확률적 모드 진단의 가장 가까운 후보", 제목 "Integrating physics-based modeling and machine learning for degradation diagnostics") | Phase 3 의 직접 선행 — 시뮬 + ML 모드 진단에서 **라벨이 적합값인지 합성 참값인지**, 이 위키 코퍼스가 세 번째로 가리키는 편 |
| ★★★ | **[34]** B.-R. Chen, M.A. Cody, S. Kim, M.R. Kunz, T.R. Tanim, E.J. Dufek, *Joule* **6** (2022) 2776–2793 | "Under the 1 C … at 25 °C, the NMC battery shows minimal degradation in the negative electrodes [34]" — **1 C 군에서 LAM_NE 를 빼는 유일한 근거** | 없음 | 사전지식 주입의 근거가 어느 셀 · 조건에서 잰 것인지(G5) — 이식 가능성 판정 |
| ★★ | **[23]** M. Dubarry, N. Costa, *Nat. Commun.* **14** (2023) 3138 | "The commonly reported degradation modes include LLI, LAM_NE and LAM_PE [23]" | 없음 (thelen2024 digest 의 "Costa" 는 Costa 2022 *J. Energy Storage* 55 — 다른 편) | 우리 α·β 좌표의 원전 저자(Dubarry 2012)의 후속 — 모드 정의 · 합성 모드 자료의 현행판 |
| ★★ | **[27]** X. Chen, Y. Hu, S. Li, …, Y. Yang, *J. Power Sources* **498** (2021) 229884 · **[28]** Y. Tian, C. Lin, X. Meng, X. Yu, H. Li, R. Xiong, *eScience* **5** (2025) 100325 | "This process generates a synthetic impedance spectroscopy dataset that reflects different degradation modes [27,28]" — **시뮬레이터 매개화의 출처** | 없음 | 판정 (b) 의 열쇠 — LAM 을 부피분율로 내릴 때 비표면적 · 막 저항을 어떻게 두는지 |
| ★★ | **[11]** J. Tian, R. Xiong, W. Shen, F. Sun, *Sci. China Technol. Sci.* **63** (2020) 2211–2230 | "Deep-level electrode degradation modes … cannot be accurately diagnosed solely based on the impedance spectra of full cells [11]" · "similar time constants are coupled [11]" | 없음 | **EIS 만으로는 모드를 못 가른다**는 같은 그룹의 인쇄 진술 — 그 근거가 무엇인지 |
| ★★ | **[35]** M. Gaberšček, *Nat. Commun.* **12** (2021) 6513 | 43 점 스펙트럼이 "SEI growth, charge transfer and diffusion processes" 를 담는다 [35] | 언급만 (yu2024 digest ref [7] — "overlaps of neighboring semi-circles are often misled …") | EIS 과정 귀속의 표준 경고 — 판정 (c) |
| ★★ | **[13]** Y. Lu, C. Zhao, J. Huang, Q. Zhang, *Joule* **6** (2022) 1172–1198 · **[14]** A. Maradesa, B. Py, J. Huang, …, F. Ciucci, *Joule* **8** (2024) 1958–1981 | "DRT … highly sensitive to the selection of regularization parameters [13,14]" | 없음 | [[drt-peak-count-nonidentifiability]] 의 정칙화 축 — DRT 기준 · 벤치마크 |
| ★★ | **[15]** P.K. Jones, U. Stimming, A.A. Lee, *Nat. Commun.* **13** (2022) 4806 | EIS → 용량 · RUL 매핑 [15,16] | 없음 | Zhang 2020 과 같은 그룹(Lee) — 우리 EIS 데이터셋 계열의 후속 |
| ★ | **[24]** E. Teliz, C.F. Zinola, V. Díaz, *Electrochim. Acta* **426** (2022) 140801 | "ECM fitting, where model parameters are correlated with degradation modes [24]" | 없음 | EIS → 모드의 ECM 선행 — 상관을 귀속으로 읽는 같은 구조인지 |
| ★ | **[36]** F. Lindgren, D. Rehnlund, …, L. Nyholm, *Adv. Energy Mater.* **9** (2019) 1901608 · **[37]** D. Rehnlund, Z. Wang, L. Nyholm, *Adv. Mater.* **34** (2022) 2108827 | 확산 지배 리튬 가둠 — 회복 가능한 용량 손실 [36,37] | 없음 (schlenker2020 digest 의 "Rehnlund" 는 다른 맥락) | 우리 LLI 정의에 **가역 성분**이 들어오는가(그림 1f 계단 하강) |
| ★ | **[25]** W. Hu, Y. Peng, Y. Wei, Y. Yang, *J. Phys. Chem. C* **127** (2023) 4465–4495 | K-K 1 % 기준 · "mapping … remains poorly understood [25]" | 없음 | EIS 품질 기준의 출처 |
| ★ | **[18]** R. Xiong, J. Tian, W. Shen, J. Lu, F. Sun, *J. Energy Chem.* **76** (2023) 404–413 | 라벨 없는 스펙트럼 활용 용량 추정 | 없음 | 같은 그룹의 EIS 학습 선행 |
| ★ | **[32]** X. Wang, X. Wei, J. Zhu, H. Dai, Y. Zheng, X. Xu, Q. Chen, *eTransportation* **7** (2021) 100093 | 43 주파수가 핵심 과정을 담는다 [32] | 없음 | 전처리 근거 |

## 20. 그림 판독 기록 (무엇을 보고 무엇을 안 봤는가)

크로핑: `raw/figures/sun2025_dl-eis-degradation-mode-diagnostics/` — 자동 **21**(본문 그림 11 · 표 2 · SI 그림 6 ·
SI 표 2) + 수동 **5**(그림 3 · 표 1 · 표 2 · 표 S1 · 표 S2) = 26 파일. **전부 열어 봤다.**

- **본문 그림 12 장 전부 봄**: 1 · 2 · 3(수동) · 4 · 5 · 6 · 7 · 8 · 9 · 10 · 11 · 12. 확대 렌더로 1b · 1d · 1f · 4b · 5c 를
  다시 봤고, 벡터 좌표 판독은 1a · 1f · 5a · 5c · 7a–d · 8a–c · 9a–c · 11c–d · 12 에서 했다.
- **본문 표 2 장**: 수동 크롭으로 봄(조건 열 머리는 렌더에만 있다). 자동 `tab_1.png` · `tab_2.png` 는 **쪽 전체**
  (과대 영역)라 열어서 확인만 했다.
- **SI**: 그림 S1–S6 전부 봄, 표 S1 · S2 는 수동 크롭으로 봄(자동 `tab_S1.png` 은 Note 2 까지, `tab_S2.png` 는 그림 S3 를
  품은 과대 영역).
- **식**: (1)–(4) · (8)–(9) · (11)–(13) · (16)–(18) · SI Note 2 · Note 4 의 식을 쪽 렌더로 확인.
- **본문 서술과 어긋난 그림**: 그림 1f(25 °C@2C LLI 61.6 % ↔ 그림 8a 30.9 %) · 그림 5c("significant changes" ↔
  아크 불변) · 그림 7c · d(막대 폭 불일치) · 그림 10 캡션 (c)(1 C ↔ 수치는 2 C 블록) · 그림 12(LLI 최고 가중치가
  온도마다 다른 끝) · SI 표 S1(35 °C@1 C) · SI 그림 S1 캡션 문자 · SI 그림 S5(범례 없음) — §13.
