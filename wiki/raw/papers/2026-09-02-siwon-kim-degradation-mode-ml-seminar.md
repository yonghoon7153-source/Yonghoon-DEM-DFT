---
source_url: local-upload/2026.09.02 김시원 연구세미나.pdf
ingested: 2026-09-03
sha256: a1cc3d4fda037c9bf074777d426a6b3b086832e723765dbd03446da5e2f597c1
---

# 수집 목적

BML 연구세미나 발표자료(김시원, 한양대 신소재공학부, 2026-09-02, 15쪽)의
**페이지별 해체분석**. 이 발표는 우리 satellite 프로젝트
`degradation-degeneracy` 와 **같은 대상(LLI/LAM_PE/LAM_NE 분해)** 을 다루되
경로가 다르다 — 우리는 그 분해가 식별 가능한지를 묻고, 이 발표는 그 분해값을
ML 의 **라벨**로 쓴다. 그래서 원문을 좌표로 남긴다.

**표기 규칙**: `[인쇄]` 는 슬라이드에 글자로 있는 것, `[도표]` 는 그림에서
읽은 것(축 눈금 기준 근사값이며 원 데이터가 아니다), `[해석]` 은 이 문서를
쓰면서 붙인 판단이고 원문의 주장이 아니다.

- 원본 파일: 로컬 업로드 PDF 15쪽 (저장소에 바이너리를 넣지 않는다)
- 함께 들어온 구술: `raw/transcripts/2026-09-03-voice-memo-007-degradation-mode-ml.md`

---

## p.1 — 표지

`[인쇄]` Degradation mode analysis for accurate health prediction of
lithium-ion batteries · September 2, 2026 · Siwon Kim · Division of Materials
Science & Engineering, Hanyang University · siwonkim@hanyang.ac.kr

---

## p.2 — LIB 의 열화 경로 (Introduction)

`[인쇄]`
- LIB 안에서 여러 열화 메커니즘이 동시에 일어난다: SEI growth, Li plating,
  microcracks …
- 열화 경로에 따라 SOH 궤적이 달라진다 — 선형 또는 비선형.
- **여러 열화 경로가 전압 신호 안에서 convolute 되어** 비파괴 진단을 어렵게
  한다.

`[도표]` 셀 모식도에 표시된 항목: Anode 쪽 Li plating · Si cracking · SEI
growth, Cathode 쪽 microcrack, 그리고 양극↔음극 Crosstalk.

`[해석]` 이 슬라이드가 세운 전제 — "메커니즘은 전압 신호 안에서 섞인다" — 는
우리 프로젝트의 출발점과 **같은 문장**이다. 다른 점은 다음 쪽에서 갈린다.

---

## p.3 — 열화 모드의 정량화 (Introduction) ★ 우리 프로젝트와 직접 맞닿는 쪽

`[인쇄]`
- 개별 열화 **메커니즘은 분리되지 않지만**, 측정 가능한 OCV 시그니처를 갖는
  **열화 모드로 묶인다**.
- 정량화 방법: **half-cell OCP 를 측정된 full-cell OCV 에 fitting** 한다.
- → **긴 측정 시간과 half-cell 기준 데이터 의존** (빨간 글씨 = 발표자가 지목한
  문제).
- 출처 표기: J. Power Sources, 2017, 341, 373–386.

`[도표]` 3단 흐름도: Degradation mechanism (구리 용출·SEI·입자 균열·Li
plating·전이금속 용출·구조 무질서화·집전체 부식 등) → Degradation mode
(LLI · LAM_PE · LAM_NE) → Effect (Capacity fade · Power fade).

`[해석]` **이 쪽이 접점이다.** 발표가 "긴 측정 시간 + half-cell 의존" 을
문제로 보고 그것을 ML 로 우회하려는 반면, 우리 프로젝트는 같은 fitting 이
**애초에 유일해를 주는가(식별 가능성)** 를 묻는다. 두 문제는 독립이 아니다 —
뒤 p.13 에서 이 fitting 의 출력이 ML 의 정답 라벨이 되기 때문이다.

---

## p.4 — Physics-inspired feature engineering (Introduction)

`[인쇄]`
- 통상적인 ML 프레임워크 → 모델 해석 가능성이 제한된다.
- Physics-inspired feature engineering: **도메인 지식을 feature space 에
  심는다**.
- 출처 표기: Adv. Energy Mater., 2025, 15, e03067 · Joule, 2025, 9, 101884.

`[구술 보강]` 음성메모: 도메인 지식 기반 feature 설계는 **학습에 필요한 데이터
수를 줄이고 모델 정확도를 올리는 것으로 알려져 있다**.

---

## p.5 — 프레임워크 전체 그림

`[인쇄]` 물리적으로 해석 가능한 feature 를 쓰는 ML 프레임워크로 전극 수준
열화를 예측한다.

`[도표]` 파이프라인:
- 입력 측정 2종 → Pseudo-OCV (pOCV) → **ICA (dQ/dV)** → feature,
  Current interruption (CI) → **DV1s (1초 전압 강하)** → feature
- Combined features → Machine-learning model (**Random forest**)
- 출력: **Macro-level SOH** + **Electrode-level LLI · LAM_PE · LAM_NE**

---

## p.6 — 데이터셋 (상용 원통형 셀)

`[인쇄]`
- 셀: **NCM811 ‖ Si–graphite, LG18650 MJ1, 3.5 Ah**
- 사이클링 프로토콜: **CC–CV, CC, 2-step, partial cycling** — 총 **18 셀**
- RPT(reference performance test) 3종: capacity check · current interruption ·
  pOCV

`[도표]` RPT 3종의 전압-시간 개형(0.5C capacity ~2 h · current interruption
~5 h · pseudo-OCV ~20 h)과 프로토콜 4종 개형. partial cycling 은 Low-SOC /
High-SOC 두 갈래와 Low→High / High→Low 표시.

`[구술 보강]` 음성메모: **50 사이클마다 RPT 를 측정**했다. pOCV 는 **0.05C**.
(전사에 "54이클/스페시티 체크" 등 오인식이 있어 슬라이드 인쇄값을 정본으로
둔다. 전사의 "3.00"·"18,650 mj 원셀" 은 3.5 Ah·18650 MJ1 의 오인식.)

`[해석]` 셀 18개, 50 사이클 간격 RPT 는 전극 수준 라벨을 만들기에는 **셀당
표본이 얇다**. p.13 의 LOGO-CV 설계와 함께 읽어야 한다.

---

## p.7 — ICA 기반 feature: PVS (peak-to-valley slope) ★ 정의

`[인쇄]`
- ICA 의 **Peak2 와 Valley2 (3.55–3.9 V)** 는 **서로 다른 전극**에서 온다:
  **NCM811 상전이(PE)** 와 **graphite 단일상 영역(NE)**.
- PVS 는 mid-SOC 창에서 **두 전극의 시그니처를 모두** 담는다.
- 정의식 (인쇄 그대로):

  ```
  PVS = [ (dQ·dV^-1)_peak2 − (dQ·dV^-1)_valley2 ] / ( V_peak2 − V_valley2 )
  ```

- Peak2: NCM811 상전이 (**H1 → M**)
- Valley2: graphite 단일상 영역 (**stage 2**)

`[도표]` dQ/dV vs V (3.2–4.2 V, 0–8 Ah/V) 위에 Peak2·Valley2 를 잇는 할선
표시. 우측에 PE(NCM811) OCP 와 NE(Si–graphite) OCP 의 dQ/dV 대응.

`[구술 보강]` 음성메모: 이 둘을 고른 이유는 **mid-SOC 에 있어 SOH 가 많이
변한 상황에서도 두 feature 가 유지되기** 때문. 그래서 **peak 은 양극,
valley 는 음극에 더 민감한 신호**다.

`[해석]` PVS 는 스칼라 **하나**다. "두 전극의 시그니처를 모두 담는다" 는 것과
"두 전극을 **가른다**" 는 것은 다른 주장이며, 이 쪽은 전자만 말한다. 후자의
근거는 p.8 이 대야 한다.

---

## p.8 — PVS 의 열화 모드 의존성 ★ 핵심 도표

`[인쇄]`
- 전기화학 시뮬레이션으로 ICA peak·valley 가 열화에 따라 어떻게 변하는지
  확인.
- **PVS 는 열화 모드에 따라 반대 방향으로 움직인다.**

`[도표]` 4패널.
1. 좌상 ICA 대조: Measured vs Calculated dQ/dV (3.2–4.2 V) — 모델이 peak
   위치를 대체로 재현하나 진폭은 과대/과소 구간이 있다.
2. 좌하 전압-용량: 0.05C · 1C, Measured(점선) vs Calculated(실선).
3. **우상 PVS vs Loss (%)** — 각 모드를 0→25 % 단독으로 넣었을 때:

   | 모드 | 0 % | 25 % 부근 | 방향 |
   |---|---|---|---|
   | LLI | −20 | 약 −10 | **증가(↑)** |
   | LAM_PE | −20 | 약 −14 | **증가(↑)** |
   | Si loss | −20 | 약 −25 | 감소(↓, 완만) |
   | Gr loss | −20 | 약 −30 (15 % 이후 평탄) | 감소(↓) |
   | LAM_NE | −20 | 약 −37 | **감소(↓, 최대)** |

4. 우하 PVS vs SOH (%) — 같은 곡선을 SOH 축(100→60 %)으로 다시 그린 것.

`[구술 보강]` 음성메모: **MJ1 셀을 모사한 P2D 모델**을 만들고 각 열화 모듈을
시뮬레이션해 모드별 PVS 변화를 확인했다. "LLI 와 LAM 이 증가하면 PVS 는 양의
방향으로, LAM_NE 가 발생하면 감소한다."

`[해석]` **이 도표가 부호 구조를 확정한다: {LLI, LAM_PE} ↑ vs {LAM_NE, Si
loss, Gr loss} ↓.** PVS 는 음극 그룹과 양극+재고 그룹을 가르지만 **LLI 와
LAM_PE 를 서로 가르지 못한다** — 두 곡선이 같은 부호로 겹쳐 올라간다. 이것은
우리 프로젝트가 말하는 degeneracy 의 부호 구조와 같은 형태다.

---

## p.9 — CI 기반 feature: SEV (scaled EOC ΔV) ★ 정의

`[인쇄]`
- **0.2C 충전 중 주기적 전류 차단 (30 s 완화)**
- **t = 1 s 에서의 전압 완화(ΔV)** 가 **U 자형 SOC 의존성**을 보인다.
- **셀별 min–max 스케일링한 EOC(충전 종료) 값 → SEV**

`[도표]` 전류 파형(0.2C, 주기적 차단) · 전압 파형(3.0–4.5 V, 0–5 h) ·
완화 구간 확대(30 s, 3.73–3.88 V, ΔV 표시) · ΔV(mV) 70–90 의 U 자 곡선 ·
min–max 스케일 후 0–1 축에서 SOC 100 % 지점 값이 **SEV**.

`[구술 보강]` 음성메모: SEV 는 이전 세미나들에서 여러 번 다룬 feature.

---

## p.10 — SEV 의 물리적 근거 (EIS 대조)

`[인쇄]`
- pristine 셀과 **EOL 셀**에 대해 **SOC-sweep EIS** → **DRT 분석으로
  R_ct,PE 추출**
- **R_ct,PE 와 ΔV 가 나란한 U 자형 SOC 의존성**을 보인다
- → **SEV 가 R_ct,PE 의 stoichiometry 의존성을 반영**한다

`[도표]` Nyquist (SOC 0 %→100 %) · R_ct,PE(mΩ) vs SOC 0–60 · ΔV(scaled) vs
SOC. pristine **SEV = 0.21**, EOL **SEV = 1.00**. 양쪽 모두 EOC 부근에서
"Pronounced EOC rise" 표시(EOL 에서 더 두드러짐).

`[구술 보강]` 음성메모: pristine 셀에서는 U 자 거동이 SOC 100 근처에서
비교적 늦게 나타나고, EOL 셀에서는 두드러지게 나타난다.

`[해석]` SEV 의 물리 근거는 **PVS 와 독립적으로** 세워졌다(임피던스 ← → 전압
완화). feature 자체의 정당화는 이 쪽이 PVS 보다 단단하다.

---

## p.11 — SEV 의 열화 모드 의존성 ★ 핵심 도식

`[인쇄]`
- **R_ct,PE 는 전극 stoichiometric window 의 이동과 수축을 반영한다.**
- **LAM_PE, LLI → SEV 증가 · LAM_NE → SEV 감소.**

`[도표]` 4분면 모식도(각각 PE/NE window 막대 + R_ct,PE vs SOC 곡선):
- Pristine: SEV (initial)
- LAM_PE: PE window 가 우측에서 수축(←화살표) → U 자 곡선의 EOC 쪽이 위로 →
  **SEV ↑**
- LAM_NE: NE window 가 수축 → EOC 지점이 곡선 바닥 쪽으로 → **SEV ↓**
- LLI: PE 는 좌로, NE 는 우로 이동(상대 슬립) → **SEV ↑**

`[구술 보강]` 음성메모(중단 직전 대목): "LAM_PE 가 발생하면 양극 용량이 축을
따라 수축하기 때문에 U 자 자체가 수축해 SEV 가 증가한다." — 이후 LLI·LAM_NE
설명은 녹음이 끊겼다.

`[해석]` **부호 구조가 p.8 의 PVS 와 동일하다: {LLI, LAM_PE} ↑ vs {LAM_NE} ↓.**
두 feature 를 더해도 LLI ↔ LAM_PE 를 가르는 **새 방향이 생기지 않는다**.

---

## p.12 — 예측 모델 구성

`[인쇄]`
- 입력: **physics-inspired features + 현재 SOH + 프로토콜** → **Random forest**
- **50 사이클 앞을 예측**: SOH(macro) 와 LAM_PE · LAM_NE · LLI(electrode)
- 프로토콜 인코딩: **voltage window**, **mean(C-rate)**
- 현재 SOH: **0.5C 에서 측정한 방전 용량**
- 검증: **Leave-one-group-out cross-validation (LOGO-CV)**
- 출처 표기: Int. Rev. Financ. Anal., 2022, 81, 102140 · React. Chem. Eng.,
  2022, 7, 1368–1379.

`[해석]` 입력 6종 중 **2종(window, mean C-rate)이 프로토콜 식별자**이고 1종은
SOH 다. 물리 feature 는 PVS·SEV 2종뿐. LOGO-CV 의 **group 이 무엇인지(셀 단위인지
프로토콜 단위인지) 슬라이드에 인쇄되지 않았다** — p.13 해석이 여기 걸린다.

---

## p.13 — 예측 성능 ★ 핵심 결과

`[인쇄]`
- 네 target 모두 **MAE 0.6 %p 이하**
- **PVS 와 SEV 가 전극 수준 예측에 기여** → 해석 가능한 프레임워크

`[도표]` parity plot 4개 + permutation importance + 궤적 1개.

| target | MAE | RMSE | 축 라벨 |
|---|---|---|---|
| SOH | 0.35 %p | 0.54 %p | **True** SOH |
| LAM_PE | 0.30 %p | 0.47 %p | **Fitted** LAM_PE |
| LAM_NE | 0.57 %p | 0.76 %p | **Fitted** LAM_NE |
| LLI | 0.40 %p | 0.61 %p | **Fitted** LLI |

`[도표]` Permutation importance (막대에서 읽은 근사값, 0–0.6 축):

| feature | LLI | LAM_NE | LAM_PE | SOH |
|---|---|---|---|---|
| SOH | ~0.45 | ~0.55 | ~0.56 | — |
| window | ~0.11 | ~0.22 | ~0.36 | ~0.48 |
| mean(C-rate) | ~0.05 | ~0.07 | ~0.07 | ~0.04 |
| min(Vdrop) | ~0.04 | ~0.09 | ~0.02 | ~0.03 |
| **PVS** | ~0.10 | ~0.16 | ~0.06 | ~0.06 |
| **SEV** | ~0.42 | ~0.40 | ~0.26 | ~0.30 |

`[도표]` 우하: 1C CC-CV 셀의 cycle 50→650 에 대한 capacity loss·LAM_PE·
LAM_NE·LLI 궤적 — True/fitted(점) vs Predicted(선), 0→15 % 범위에서 겹침.

`[해석]` 세 가지가 이 쪽에서 읽힌다.
1. **정답 축이 "Fitted"** 다 — 전극 수준 3종의 라벨은 p.3 의 half-cell OCV
   fitting 출력이다. 그 fitting 이 degenerate 하면 MAE 는 **degenerate 한
   라벨을 얼마나 잘 재현하는가**를 재는 값이지 전극 상태의 정확도가 아니다.
2. **PVS 의 permutation importance 가 모든 target 에서 최하위권(~0.06–0.16)**
   이다. 인쇄 문장("PVS 와 SEV 가 기여한다")과 도표의 크기 차이가 크다 —
   기여의 대부분은 SEV 와 SOH·window 다.
3. **LAM_PE 예측은 SOH(0.56) + window(0.36)** 이 지배한다. window 는 프로토콜
   식별자이므로, LAM_PE 는 사실상 "이 프로토콜에서 이만큼 닳았으면 PE 는
   이만큼" 이라는 **그룹 평균 궤적**으로 설명될 수 있다.

---

## p.14 — Future work

`[인쇄]` feature 확장 · 학습 데이터 증강 · 모델 판단의 해석 → 정확도와 물리적
해석 가능성 향상.
- **Additional features**: 추가 ICA peak/valley, **end-of-discharge ΔV(EOD)**,
  **Si lithiation** 관련 신호, **0.05C ICA vs 0.5C ICA** 비교
- **Data augmentation**: **더 높은 C-rate**, **P2D 모델 시뮬레이션 결과를 ML
  학습에 투입**
- **Explainable AI**: **SHAP** 분석 (feature importance, cell index 별
  SHAP value)

---

## p.15 — Discussion points (발표자가 스스로 연 질문 3개)

`[인쇄, 한국어 원문]`
- **Degradation mode fitting quality 개선**
- **Degradation mode: LAM_NE 를 Si loss / graphite loss 로 분리**
- **ICA (dQ/dV) 계산에 따른 PVS 변화**

`[해석]` 세 질문이 모두 우리 프로젝트의 축과 겹친다. 상세 대응은 컴파일
페이지 [[pvs-sev-degradation-mode-features]] 와 질문 카드
[[pvs-sev-lli-lampe-separability]] 에.

---

## 원문에 없어서 확인이 필요한 것 (이 문서의 공백)

1. **LOGO-CV 의 group 정의** — 셀 단위인가 프로토콜 단위인가. 프로토콜
   식별자(window)가 입력에 있으므로 group 정의에 따라 p.13 수치의 의미가
   달라진다.
2. **fitting 라벨의 불확실성** — "Fitted LAM_PE" 에 오차 막대나 식별 가능성
   진단이 붙어 있지 않다.
3. **P2D 단독 모드 스윕의 조합 여부** — p.8 은 모드를 **하나씩** 넣은 곡선만
   보여 준다. 두 모드가 동시에 진행할 때 PVS 가 가법적인지는 미제시.
4. **PVS 의 dQ/dV 평활화 의존성** — 발표자 자신이 p.15 에서 연 질문.
5. **18 셀의 프로토콜별 배분** — 셀 수가 프로토콜 4종에 어떻게 나뉘는지.
