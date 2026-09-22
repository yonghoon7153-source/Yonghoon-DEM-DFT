---
title: "BML 연구세미나 주간보고 (김시원, 2026-09-21) — Si-graphite ‖ NCM811 ICA 모델링: LAM_Si 도입 · Si OCP 이력 · Euclidean loss · 0.5C PVS"
source_url: local-upload/2026.09.21_김시원_연구세미나.pdf
ingested: 2026-09-22
pdf_sha256: 717952aecc84ea3406a5271bfd71163c75c059dcf76c567e76447453d1333657
sha256: 5a6edf73dd50702338b2363b798559564891125b4c8536facb310d72ddce2dbb
---

# 수집 목적

BML 연구세미나 주간 보고 덱(김시원, 2026-09-21, 8쪽; 금주 수행 업무
2026.09.14 ~ 09.20)의 **페이지별 해체분석**. 3주 전 덱
`raw/papers/2026-09-02-siwon-kim-degradation-mode-ml-seminar.md` 의 **직접
후속**이다 — 그 덱 p.15 가 스스로 연 discussion point 3개(① fitting quality
개선 · ② LAM_NE 를 Si loss / graphite loss 로 분리 · ③ dQ/dV 계산 방식에 따른
PVS 변화)에 **전부 착수한 첫 보고**다. 우리 satellite `degradation-degeneracy`
와 **같은 시스템(NCM811 ‖ Si–graphite)·같은 좌표(half-cell OCP fitting, 5번째
파라미터 γ_Si)** 를 다루므로 원문을 좌표로 남긴다.

**표기 규칙**: `[인쇄]` 는 슬라이드에 글자로 있는 것(그림 제목·범례·축 라벨에
인쇄된 글자 포함 — 그 경우 `[도표-인쇄]`), `[도표]` 는 그림에서 눈으로 읽은
것(축 눈금 기준 근사값 `figure-read ≈`, 원 데이터가 아니다), `[해석]` 은 이
문서를 쓰면서 붙인 판단이고 원문의 주장이 아니다. `[해석]` 표시 없는 문장은
전부 덱이 실제로 말한 것이다.

- 원본 파일: 로컬 업로드 PDF 8쪽, `pdf_sha256` 는 frontmatter (저장소에
  바이너리를 넣지 않는다)
- 함께 들어온 것: 사용자가 세미나에서 받아 적은 요지 (§"사용자 메모와 덱의
  어긋남" 에 원문 그대로 인용)
- 크로핑: `raw/figures/2026-09-21-siwon-kim-si-gr-ica-lam-si-gitt-ocp/`
  (`--slides` 모드, 페이지 8장 = `fig_1` ~ `fig_8`). **8장 전부 Read 로 실제로
  봤다.** 이 덱은 p.1 표를 빼면 전부 그림 위주라 안 본 그림이 없다.

---

## 원문에 없어서 확인이 필요한 것 (이 문서의 공백)

1. **셀 식별과 개수.** p.8 은 `#8` 한 셀, p.6 은 "400 cycle knee point 이후
   셀" 한 셀. 09-02 덱의 18 셀(LG18650 MJ1, 3.5 Ah) 중 어느 셀인지, 프로토콜이
   무엇인지 인쇄돼 있지 않다. 이 덱에는 셀 화학·모델명이 **한 번도 나오지
   않는다** (09-02 덱의 연속선상이라는 것은 발표자·주제·좌표계로 추정한
   `[해석]`).
2. **optimizer 설정.** "fitting option ub, lb, initial 수정" 이라고만 있고
   수정 전/후 값이 없다. 사용자 메모의 "fitmincon"(= MATLAB `fmincon`) 은
   구술이며 덱에 인쇄되지 않았다.
3. **목적함수의 미공개 상수.** p.7 식의 스케일 `s`, 가중 `w_pOCV`,
   `w_dV/dQ`, 파라미터 집합 `Θ`(= ub/lb) 의 값이 없다.
4. **"Euclidean loss 적용 시 fitting quality 향상"(p.5) 의 근거 수치가
   없다.** MSE 적합과 Euclidean 적합의 RMSE·파라미터 변화를 나란히 보인
   그림이 **없다** — p.5 는 한 적합(Cycle 1)만, p.7 은 모식도 + 식이다.
5. **LAM_Si · LAM_Gr 의 정의식.** p.6 에 두 곡선이 있으나 γ_Si·α_NE 로부터
   어떻게 계산되는지 인쇄돼 있지 않다.
6. **p.6 의 x축 "Cycle 0 ~ 4" 의 단위.** RPT 인덱스인지 실제 사이클인지,
   "400 cycle knee point 이후" 와 어떻게 대응하는지 없다.
7. **음의 LAM_Si(−20 ~ −23 %) 에 대한 언급이 없다.** 활물질이 늘었다는 값인데
   본문 문장은 "정량화 결과가 LAM_Si 반영" 이다. lb 가 0 이 아니었는지,
   그것이 의도인지 모른다.
8. **0.5C PVS 의 정의.** p.8 에 peak(검은 ▼)·valley(빨간 ▲) 마커가 여럿인데
   어느 쌍이 PVS 인지, 09-02 의 Peak2/Valley2(3.55–3.9 V) 정의를 그대로 쓴
   것인지 없다. "열화모드와 선형성 X" 의 근거인 **상관 산점도가 덱에 없다.**
9. **Si OCP 문헌 8종의 서지.** 성만 인쇄(Bagetto · Friedrich · Jiang · Kunz ·
   Li · Lu · Sethuraman · Wetjen). 어느 논문·어느 재료(결정질 Si / SiO_x /
   박막 / 복합)인지 없다.
10. **음극 GITT-OCV 의 출처와 프로토콜.** 해체 half-cell 인지 3전극인지,
    펄스 크기·휴지 시간·C-rate 가 없다. "Si-graphite" 와 "graphite" 두 전극이
    같은 셀 계열인지도 없다.
11. **γ_Si 값의 불일치(이 문서의 발견, §p.4·p.6).** half-cell GITT-OCV 적합은
    γ_Si `[도표-인쇄]` 25.7 % (Li OCP) / 30.5 % (Lu OCP), full-cell 적합의
    Cycle 0 은 `figure-read ≈` 20.5 %. 같은 양인지, 왜 다른지 설명이 없다.
    (참고: Schmitt 2022 는 같은 MJ1 계열에서 pristine γ_Si = 9.52 % 를 보고
    — `raw/papers/schmitt2022_sic-ocp-shape-change-degradation-modes.md`.
    정의·OCP 출처·셀이 다를 수 있어 직접 비교는 `[해석]`.)
12. **"딥러닝 모델 학습"(p.1 금주·차주)** — 모델·입력·목적이 덱 어디에도
    없다.
13. **이력(hysteresis) 처리 방침.** p.3·p.4 가 충/방전 OCP 가 다르다는 것을
    보인 뒤, **full-cell fitting(p.5·p.6) 에는 어느 방향의 음극 OCP 를 썼는지**
    인쇄돼 있지 않다.
14. **라벨의 불확실성.** 09-02 와 같다 — 오차 막대·초기값 민감도·파라미터
    상관·식별 가능성 진단이 **0**. 이 라벨이 차주 "랜덤 포레스트 기반 열화모드
    진단 모델" 의 **정답 축**이 된다 (p.1).

---

## p.1 — 주간 업무표

`[인쇄]` 연구주제: Battery health 분석.

| 구분 | 금주 수행 업무 (2026.09.14 ~ 09.20) | 차주 수행 계획 (2026.09.21 ~ 09.27) |
|---|---|---|
| 연구 관련 | 1) Si-Gr battery ICA — 음극 potential 에서 Si fraction 정량화 · **Euclidean distance 기반 목적함수 수정** · **LAM_Si 도입** · Si loss fitting 성능 개선 · 딥러닝 모델 학습 | 1) Si-Gr battery ICA — **랜덤 포레스트 기반 열화모드 진단 모델 개발** · 진단 모델 성능 평가 · 딥러닝 모델 학습 |
| 기타 | (빈칸) | (빈칸) |

`[해석]` 이 표가 이 덱의 구조를 준다. 금주 5항목 중 앞 4개가 p.2–p.7 이고,
차주 첫 항목이 09-02 덱 p.12–13 의 Random forest 를 **새 라벨(LAM_Si 포함)로
다시 학습**한다는 뜻이다. 즉 이번 덱에서 바뀐 것은 전부 **라벨 생성기**이고,
그 라벨이 다음 주 ML 의 정답이 된다.

---

## p.2 — 음극 GITT-OCV 정리 ★ (Si 기여가 방향 의존)

`[인쇄]` 음극 GITT-OCV 데이터 정리 · 방전(delithiation) 그래프에서 Si 기여도
두드러짐.

`[도표]` 5패널, 모두 `Voltage (V vs. Li/Li+)` 0–1.0 V 대 `SOC_NE (%)` 0–100.
범례는 `Si-graphite`(파랑 계열) · `graphite`(초록 계열), 각각 연한 색과 진한
색 두 벌.

- **상단 좌** (4곡선): 연한 두 곡선은 SOC 0 에서 `≈0.5–0.6 V` 로 시작해
  SOC 40 % 이전에 `≈0.1 V` 로 내려가 평탄 (= lithiation 방향). 진한 두 곡선은
  SOC 0 에서 `≈0.1 V` 로 시작해 SOC 100 % 에서 `≈1.0 V` 까지 올라간다
  (= delithiation 방향, x 는 통과 전하량으로 읽힌다 — `[해석]`, 축 정의는
  인쇄돼 있지 않다).
- **상단 중** (lithiation 만): Si-graphite 는 SOC 5–60 % 구간에서 graphite
  위에 `figure-read ≈ 0.05–0.1 V` 떠 있다 (Si-graphite 0.2 → 0.1 V, graphite
  0.12 → 0.08 V). 차이가 **작고 넓게 퍼져** 있다.
- **상단 우** (delithiation 만): Si-graphite 는 SOC ≈35 % 부터 graphite 에서
  갈라져 `≈0.15 V`(SOC 35–55 %) 어깨, `≈0.4 V`(SOC 70–90 %) 두 번째 어깨를
  만들고 SOC 100 % 에서 `≈1.0 V` 로 급상승. graphite 는 `≈0.1 → 0.2 V` 를
  유지하다 SOC ≈95 % 이후에만 급상승. **차이가 SOC 35–100 % 에서 최대
  ≈0.3 V.**
- **하단 좌·중**: 진한 곡선이 SOC 0 에서 `≈0.95 V` 로 시작해 내려온다 —
  Si-graphite 는 `≈0.4 V` 평탄(SOC 12–25 %) → 0.15 V(SOC 40 %) → 0.1 V;
  graphite 는 `≈0.2 V` 평탄(SOC 5–18 %) → 0.13 → 0.1 V. `[해석]` 상단 우
  패널을 **x 축 반전**해 lithiation 곡선과 같은 방향으로 겹쳐 놓은 것으로
  읽힌다 (덱은 이를 설명하지 않는다). 하단 중은 그 진한 곡선 둘만.

`[해석]` 이 쪽이 뒤 전체의 전제다 — **Si 의 OCP 기여는 delithiation 가지에서
크고 lithiation 가지에서 작다.** 그래서 발표자는 방전 GITT-OCV 로 γ_Si 를
잡으러 간다(p.4). 그런데 이것은 동시에 **음극 OCP 가 방향에 따라 다른
곡선**이라는 뜻이고, 그 함의는 p.4 에서 터진다.

---

## p.3 — Si OCP 문헌 8종 비교 ★ (전부 이력 루프다)

`[인쇄]` Si OCP 정리 및 비교. 패널 범례(성만): **Bagetto · Friedrich · Jiang ·
Kunz · Li · Lu · Sethuraman · Wetjen**.

`[도표]` 8패널, `Voltage (V vs. Li/Li+)` 0–1.5 V 대 `Normalized capacity`
0–1.0. **8개 모두 닫힌 루프(상·하 두 가지)** 로 그려져 있다 — 위 가지가
delithiation(높은 전위), 아래 가지가 lithiation. 대략의 형상 (`figure-read`):

| 문헌 | 위 가지(delith.) 시작 → 중간 | 아래 가지(lith.) 중간 | 특징 |
|---|---|---|---|
| Bagetto | 1.25 → 0.5 → 0.15 V | ≈0.35 → 0.1 V | 두 가지 간격 ≈0.2 V |
| Friedrich | 1.5 → 0.5 → 0.1 V | ≈0.3 → 0.1 V | 시작 전위 최고 |
| Jiang | 0.9 → **0.55 평탄 → 0.4 에서 계단** → 0.2 V | ≈0.3 → 0.2 → 0 V | 위 가지에 뚜렷한 **계단(2상 형)** |
| Kunz | 1.5 → 0.5 → 0.3 → 0 V | ≈0.3 → 0.25 → 0.05 V | 끝점 0 V |
| **Li** | 0.9 → **≈0.4–0.45 V 평탄 (0.2–0.9)** → 0.95 에서 급락 | ≈0.3 → 0.25 → 0.1 → 0 V | 위 가지가 **가장 평탄**, 말단 급락 |
| **Lu** | 1.15 → 0.5 → 0.25 → 0.05 V | ≈0.3 → 0.25 → 0.05 V | 완만 단조 |
| Sethuraman | 1.2 → 0.5 → 0.4 → 0.1 V | ≈0.3 → 0.2 → 0 V | |
| Wetjen | 1.2 → 0.5 → 0.3 → 0.05 V | ≈0.3 → 0.1 → 0.05 V | 아래 가지가 낮다 |

`[해석]` 셋을 읽어 둔다. (a) **문헌 Si OCP 자체가 예외 없이 두 가지(이력)를
갖는다** — 중간 용량에서 가지 간격 `≈0.1–0.3 V`. "고정 OCP 함수 하나" 라는
electrode-balancing 전제([[halfcell-ocp-shape-invariance]])가 Si 에서는 문헌
입력 단계에서 이미 성립하지 않는다. (b) 8종의 **위 가지 형상 차이**(Li 의
평탄 vs Lu 의 단조 vs Jiang 의 계단)가 그대로 γ_Si 추정치 차이로 간다 (p.4).
(c) 어느 문헌이 어떤 Si(결정질/비정질/SiO_x/박막) 인지 없으므로 대상 셀
(SiO_x 추정, 09-02 덱 MJ1) 과의 재료 정합은 판단 불가.

---

## p.4 — Si OCP 를 이용한 방전 GITT-OCV fitting ★★ (충/방전의 최적 OCP 가 다르다)

`[인쇄]` Si OCP 이용 방전 GITT-OCV fitting · **충/방전 GITT-OCV 의 최적 fit
OCP 가 다름.** 패널 제목: 좌 "**Lu et. Al (Lithiation fitting 시 최적)**", 우
"**Li et. al**".

`[도표-인쇄]` 그림 안에 인쇄된 적합 결과:

| Si OCP 출처 | γ_Si | RMSE | 비고 (인쇄) |
|---|---|---|---|
| Lu et al. | **30.5 %** | **20.36 mV** | lithiation fitting 시 최적 |
| Li et al. | **25.7 %** | **15.23 mV** | (방전 = delithiation 에서 더 좋다) |

`[도표]` 각 패널 상단: `U vs Li/Li+ / V` (0–1.2) 대 `anode SOC / -` (0–1),
`measured blend`(검정 실선) vs `reconstructed`(빨강 점선). 측정 blend 곡선은
SOC 0 에서 `≈1.1 V` → SOC 0.15 에서 `≈0.42 V` → **0.4 V 평탄(SOC 0.15–0.28)**
→ SOC 0.3 에서 `≈0.22 V` → 0.5 에서 0.12 → 0.65 이후 `≈0.08–0.1 V`. 하단:
`dU/dSOC / V` (−30–0).
- **Lu 재구성**: 0.4 V 평탄을 **재현하지 못한다** — 빨강이 SOC 0.1–0.2 에서
  측정 아래(≈0.35 vs 0.42), SOC 0.25–0.3 에서 측정 위로 지나가며 매끈하게
  0.6 → 0.3 으로 내려간다. dU/dSOC 잔차가 SOC 0.05–0.3 에 몰린다.
- **Li 재구성**: 0.4 V 평탄을 따라간다(SOC 0.15–0.28 에서 겹침). SOC 0.25–0.3
  에서 빨강 dU/dSOC 가 `≈−5` 로 측정(≈−3) 보다 깊은 골을 하나 만들고, SOC
  0.05–0.1 에서 측정보다 `≈0.1 V` 낮다.

`[해석]` 이 쪽이 이 덱의 **가장 무거운 그림**이다. 세 가지.
1. **같은 방전 데이터에서 Si OCP 출처만 바꾸면 γ_Si 가 25.7 ↔ 30.5 %, 즉
   ≈4.8 %p 움직인다.** 이것은 노이즈가 아니라 **모델 입력(OCP 함수) 선택에
   대한 라벨 민감도**이며, 발표자가 "최적" 이라 부른 것은 RMSE 5 mV 차이다.
   RMSE 15–20 mV 는 어느 쪽도 Schmitt 2022 가 "좋은 재구성" 으로 부른 full-cell
   pOCV 12 mV 문턱 위다 (좌표가 half-cell 이라 직접 비교는 아니다).
2. **"충/방전의 최적 OCP 가 다르다" = Si OCP 가 경로 의존이다.** lithiation
   데이터는 Lu 가, delithiation 데이터는 Li 가 맞는다는 것은 한 함수로 두 가지를
   다 맞출 수 없다는 뜻이다. 그러면 full-cell pOCV fitting(p.5) 에서 **어느
   방향의 pOCV 를 재느냐에 따라 음극 OCP 함수를 바꿔 넣어야** 하고, 덱은 어느
   것을 썼는지 적지 않는다 (공백 13). 이 위키에는 이미 이웃 명제가 있다 —
   전고체 Ag–C 중간층에서 "방전은 충전의 역이 아니다"(Spencer-Jolly 2023,
   `raw/papers/spencerjolly2023_ag-graphite-interlayer-structural-changes.md`,
   ≈C/68 이라 `i→0` 으로 지울 수 없는 열역학적 이력). 이 덱은 그 명제의
   **액체셀 Si/graphite 판**을 GITT(준평형) 데이터로 보인 것이다 — 단 이 덱은
   그것을 "이력" 이라 부르지 않고 "최적 fit OCP 가 다름" 으로만 적는다.
3. 사용자 메모("음극 lithiation GITT-OCV 와 최적 Si OCP 상이")는 이 쪽과
   일치한다.

---

## p.5 — 정량화 코드 개선 (ub · lb · initial, Euclidean loss)

`[인쇄]` Degradation mode 정량화 코드 개선: fitting option **ub, lb, initial
수정** · **Euclidean loss 적용 시 fitting quality 향상.**

`[도표]` 3패널 (MATLAB 스타일).
- **pOCV (Cycle 1)**: `Voltage` 0–4.5 대 `Capacity` −0.2–1.2 (**정규화 용량**).
  범례: `Experimental`(초록 점선) · `E_PE`(파랑 점선) · `E_NE`(빨강 점선) ·
  `E_PE Fitted`(파랑 실선) · `E_NE Fitted`(빨강 실선) · `Fitted Model`(초록
  실선). full-cell `≈3.0 → 4.2 V`, PE `≈3.55 → 4.25 V`, NE `≈0.55 → 0.05 V`.
  Experimental 과 Fitted Model 이 눈으로는 겹친다.
- **dV/dQ**: 0–3 대 Capacity. Experimental 과 Fitted Model 겹침. `E_PE Fitted`
  는 `≈0.5–1.0` 에서 용량 0.5·0.75 에 봉우리, `E_NE Fitted` 는 용량 0.15–0.3
  에 `≈0.8` 봉우리와 0.6 에 `≈0.45` 봉우리.
- **dQ/dV (Full cell)**: 0–7 대 `Voltage (V)` 2.6–4.2. 봉우리 `figure-read ≈`
  3.45 V (1.4) · 3.65 V (1.4) · 3.9 V (1.4) · **4.1 V (6.5, 날카로움)**.
  Experimental/Fitted 겹침.

`[해석]` (a) 이 그림은 **한 적합(pristine, Cycle 1)** 이고 MSE 적합과의 대조가
없다 — "향상" 의 근거가 이 덱에는 인쇄돼 있지 않다 (공백 4). (b) x 축이
**정규화 용량**이다 → 이 적합은 Lin & Khoo 의 "SOC 정규화 곡선" 좌표에서
돌아간다([[np-lip-ocv-reparametrization]]) — 다만 blend 전극은 그 정리의
전제(OCP 함수 고정)를 γ_Si 로 깬다는 것이 [[halfcell-ocp-shape-invariance]] 에
이미 적혀 있다. (c) 여기서 보이는 것은 **곡선 일치**다. 참값이 없으므로
파라미터 정확도는 이 그림으로 알 수 없다 — 이 구분이 p.6 을 읽는 열쇠다.

---

## p.6 — knee 이후 셀의 모드 정량화 ★★ (LAM_Si 가 음수로 간다)

`[인쇄]` 400 cycle knee point 이후 셀 degradation mode 정량화 · **Degradation
mode 정량화 결과가 LAM_Si 반영.**

`[도표]` 3패널, x 축 `Cycle` 0–4 (단위 미인쇄 — 공백 6).

**Anode components** (`LAM (%)` −30–50):

| Cycle | LAM_Si (파랑 ○) | LAM_Gr (주황 □) |
|---|---|---|
| 0 | 0 | 0 |
| 1 | **≈ −20.5** | ≈ +6 |
| 2 | **≈ −23** | ≈ +5.5 |
| 3 | ≈ −9 | ≈ +2.5 |
| 4 | **≈ +50** | ≈ −0.5 |

**Cell level** (`DM (%)` −5–30):

| Cycle | LAM_NE (파랑 ○) | LAM_PE (주황 □) | LLI (노랑 △) |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 1 | ≈ 0.5 | ≈ −0.2 | ≈ 4.2 |
| 2 | ≈ −0.5 | ≈ 1.5 | ≈ 7.2 |
| 3 | ≈ 0.2 | ≈ 3.3 | ≈ 11.7 |
| 4 | ≈ 9.8 | ≈ 8.2 | **≈ 26.8** |

**Silicon capacity share** (`γ_Si (%)` 10–26): 20.5 → 25.0 → 25.3 → 22.5 →
**11.4**.

(전부 `figure-read ≈`. 오차 막대 없음. 점당 곡선 1개.)

`[해석]` 발표자의 문장("LAM_Si 반영")이 가리키는 것은 Cycle 4 다 — γ_Si 가
20.5 → 11.4 % 로 반토막 나면서 LAM_Si ≈ +50 %, 그런데 LAM_NE 는 ≈ +10 % 에
그친다. 즉 "음극 전체는 조금 잃고 Si 는 많이 잃었다" 는 서술이 가능해졌다.
**그러나 같은 그림의 Cycle 1–3 이 그 서술을 스스로 약화시킨다**:
1. **LAM_Si 가 −20 ~ −23 %** 다. Si 활물질이 20 % 늘었다는 값이고, 같은 시점
   γ_Si 는 20.5 → 25.3 % 로 **오른다**. LAM_Gr 는 +6 % 로 graphite 만 잃는다.
   물리로 읽으면 "knee 이후 Si 가 자라난다" 인데 덱은 이 값에 대해 아무 말이
   없다.
2. 이것이 이 위키가 예측해 둔 것과 정확히 같은 모양이다 — Schmitt 2022 가
   "γ_Si ↓ 와 α_an ↓ 는 full-cell 에 같은 서명을 남긴다" 고 적고 **검사하지
   않은** `(γ_Si, α_NE)` 축퇴([[halfcell-ocp-shape-invariance]] 처방 ③ 의
   대가). 자유도를 4 → 5 로 늘리면 곡선 일치(p.5)는 좋아지지만, 데이터가
   말하지 않는 방향이 하나 생기고 **그 방향 위의 값은 추정기(초기값·ub/lb)가
   고른다**([[nullspace-coefficient-interpretation]]). Cycle 1–2 의 −23 % 는
   그 방향 위에서 추정기가 고른 값일 가능성이 높다 — **단, 이 덱에는 그것을
   판정할 오차 막대·초기값 민감도·목적함수 값이 없으므로 이것은 가설이다.**
3. LAM_PE 가 Cycle 1 에서 −0.2 % (음수), LAM_NE 가 Cycle 2 에서 −0.5 %.
   자릿수는 작지만 **하한(lb) 이 0 이 아니라는 신호**다 — "ub, lb 수정" 이
   음수를 허용하는 방향이었을 가능성 (`[해석]`, 확인 필요).
4. **이 5개 곡선이 차주 랜덤 포레스트의 정답이 된다** (p.1). 09-02 덱 p.13 의
   "Fitted LAM_PE" 축이 이제 "Fitted LAM_Si" 까지 넓어졌고, 그 라벨의 첫 공개
   궤적이 물리적으로 불가능한 값을 포함한다.

---

## p.7 — 목적함수: MSE loss vs Euclidean distance loss (모식도 + 식)

`[인쇄]` 좌 열 제목 "**MSE loss**", 우 열 제목 "**Euclidean distance loss**".

`[도표-인쇄]` 상단 모식도 제목 "Comparison of Loss Functions: RMSE vs
Euclidean Loss". 좌 "RMSE: Vertical Error" — 고정 `x_i^exp` 에서
`Vertical Error = |y_i^exp − y^model(x_i^exp)|`. 우 "Euclidean Loss: Shortest
Distance" — `(x_i^exp, y_i^exp)` 에서 모델 곡선 위 모든 점까지의 거리 중
최소, `min_j sqrt( (x_i^exp − x_j^model)² + ((y_i^exp − y_j^model)/y_scale)² )`,
y 축은 `y/y_scale`. 캡션 `[인쇄]`: "RMSE only measures vertical deviation at
a fixed x-point. Euclidean Loss finds the shortest geometric distance to any
point on the model curve, **making it more robust against sharp peaks**."

`[인쇄]` 식 (인쇄 그대로 옮김):

```
L_MSE        = (1/N) Σ_{i=1}^{N} ( V̂(Q_i) − V_i )²
L_MSE^{dV/dQ} = (1/N) Σ_{i=1}^{N} ( dV̂/dQ|_{Q_i} − dV/dQ|_{Q_i} )²

L_euc        = (1/N) Σ_{i=1}^{N} min_j sqrt( (Q_i − Q̂_j)² + ( (V_i − V̂_j) / s )² )
L_euc^{dV/dQ} = (1/N) Σ_{i=1}^{N} min_j sqrt( (Q_i − Q̂_j)² + ( (1/s) [ dV/dQ|_i − dV̂/dQ|_j ] )² )

θ* = argmin_{θ∈Θ} [ w_pOCV · L_pOCV(θ) + w_dV/dQ · L_dV/dQ(θ) ]
```

**주의 (이 덱을 요약한 상위 메모와의 어긋남)**: 이 쪽에는 "MSE vs Euclidean
비교 그림 6장" 이 **없다**. 모식도 1개(2패널) + 식 5개다. 실제 적합 결과를
두 loss 로 나란히 비교한 그림은 이 덱 어디에도 없다.

`[해석]` 목적함수 교체가 무엇을 바꾸는지를 식에서 직접 읽을 수 있다.
1. **L_euc 는 가로(Q) 오차와 세로(V) 오차를 스케일 `s` 로 섞은 점-대-곡선
   거리**다 (이산화한 직교거리회귀 / ICP 형). 날카로운 dV/dQ 봉우리가 가로로
   δQ 만큼 어긋나면 MSE 는 세로 차이(봉우리 높이 전체)를 물지만 L_euc 는 δQ
   만 문다 — 캡션의 "robust against sharp peaks" 가 정확히 이 뜻이다.
2. **그런데 dV/dQ 특징점의 가로 위치가 바로 모드 신호다.** Birkl 계열·Natterer
   DMA([[reference-electrode-halfcell-dma]])가 LAM·LLI 를 읽는 것은 특징점의
   **가로 위치·간격**이다. 가로 어긋남을 싸게 만드는 손실은 곧 α·β(창의
   스케일·이동) 방향의 목적함수 골을 **더 평탄하게** 만든다. 따라서 예측은:
   **곡선 일치는 좋아지고(p.5 의 "quality 향상"), 근최적 집합은 넓어진다**
   ([[near-optimal-set-width-measurement]]). 이 둘은 상충하지 않는다 — 같은
   변경의 두 얼굴이다. 검증되지 않은 예측이며, 참값이 있는 우리 합성 truth
   위에서만 확인할 수 있다.
3. `min_j` 는 j 가 바뀌는 곳에서 미분 불연속이다. gradient 기반 `fmincon`
   (구술) 에 조각별 목적함수를 주면 국소 최소가 늘 수 있다 — 사용자 메모의
   "PSO, GA 적용 예정" 이 이 문제를 겨눈 것으로 읽힌다 (`[해석]`; 덱에는
   optimizer 계획이 없다).
4. `s`, `w_pOCV`, `w_dV/dQ` 가 없다. `s` 는 Q(정규화 0–1)와 V(≈1 V 범위) 를
   맞추는 상수라 결과가 이 값에 의존한다.

---

## p.8 — 0.5C dQ/dV 에서 PVS 추출 ★ (열화모드와 선형성 X)

`[인쇄]` 0.5C dQ/dV curve 에서 PVS 추출 · **열화모드와 선형성 X.**

`[도표-인쇄]` 그림 제목 "**#8 - cycle 1 cha - dQdV**". `dQ/dV (Ah/V)` 0–14 대
`Voltage (V)` 3.2–4.3. 범례 `rpt 0, 50, 100, …, 700` (15곡선, 색은 보라 →
연두). 마커: **검은 ▼ = peak, 빨간 ▲ = valley** (범례 없음, `[해석]`).

`[도표]` 읽은 것:
- **rpt 0(보라)만 다르다**: 3.63 V 에 `≈4.8 Ah/V` 봉우리, 3.85–3.9 V 에 넓은
  둔덕 `≈5.5`. **rpt 50 이후 14곡선은 촘촘히 겹친다**: 3.65–3.68 V 봉우리
  `≈3.3–3.5`, **3.81 V 주봉우리 `≈5.8`**, 4.13–4.15 V 작은 봉우리 `≈3.8`.
- valley(빨간 ▲): `≈3.72–3.74 V (3.0–3.2)` · `≈4.0–4.05 V (3.2–3.4)` ·
  `≈4.22 V (2.7)`.
- **4.23 V 에 수직 스파이크** (`≈14 Ah/V` 까지) — CC→CV 전환/컷오프. 검은 ▼
  가 이 스파이크 위에 4–14 Ah/V 에 걸쳐 **세로로 줄지어 찍혀 있다** = peak
  검출기가 컷오프 스파이크를 봉우리로 잡는다.
- rpt 50 또는 100 한 곡선에 3.55–3.6 V 어깨(`≈2`) 가 따로 보인다.
- **rpt 0 → 50 사이의 변화(3.63 V 봉우리 4.8 → 3.3, 3.9 V 둔덕 소멸)가 rpt
  50 → 700 전체의 변화보다 크다.**

`[해석]`
1. **PVS 정의가 이 쪽에서 흔들린다.** 09-02 p.7 의 PVS 는 0.05C pOCV ICA 의
   Peak2/Valley2(3.55–3.9 V) 였다. 0.5C 에서는 (a) 봉우리 개수·순서가 rpt 0 과
   그 이후에서 다르고(3.9 V 둔덕이 사라지고 3.81 V 가 주봉우리가 된다), (b)
   컷오프 스파이크가 peak 로 잡히며, (c) 분극으로 전체가 오른쪽으로 밀린다.
   "두 번째 봉우리/골" 로 세는 feature 는 개수가 바뀌면 다른 것을 잰다 —
   [[rate-independent-li-plating-signature]] 에서 적어 둔 PVS 의 정의 취약성이
   여기서는 **C-rate 변화로** 재현된다.
2. **"열화모드와 선형성 X" 의 근거 그림이 없다.** 덱이 보이는 것은 dQ/dV
   겹침만이다. 상관 산점도(PVS vs LLI/LAM)는 인쇄돼 있지 않다 (공백 8). 그리고
   설령 있었더라도 그 x 축(모드)은 p.6 의 fitted 라벨이다 — **PVS 가 모드와
   선형이 아닌 것인지, 라벨이 흔들리는 것인지(p.6 의 −23 %) 이 데이터로는
   가를 수 없다.** 이 판정 불가가 우리 위키가 요구해 온 "라벨 불확실성" 이
   실무에서 필요해지는 첫 자리다.
3. **축이 Ah/V 다** (09-02 p.7 도 0–8 Ah/V). 즉 PVS 는 **절대 용량 축**의
   dQ/dV 에서 계산된다 → [[pvs-sev-lli-lampe-separability]] Status Log (10) 의
   Gap("SOC 정규화인가 Ah 축인가")이 **Ah 축으로 닫힌다.** 결과: Lin 의 2
   자유도 따름정리의 엄밀형(정규화 곡선의 함수는 rank 를 못 늘린다)은 그대로
   적용되지 않고 총용량 정보가 PVS 에 섞인다 — 다만 그 셋째 숫자는 ML 입력에
   이미 SOH 로 들어가 있다.
4. rpt 0 → 50 의 큰 점프는 `[해석]` 초기 형성/안정화 또는 첫 RPT 의 상태
   차이로 읽히며, 0.5C PVS 를 모드 관측으로 쓰면 이 한 걸음이 SOH 축 상관을
   지배할 수 있다.

---

## 사용자 메모와 덱의 어긋남

사용자가 세미나 중 받아 적은 요지 (원문 그대로):

```
3. Si-graphite | NCM811 system ICA 모델링 (김시원)
- Degradation mode 정량화 모델 개선:
  Degradation mode 정량화 코드 fitting option (ub, lb) 수정
  Fitting 성능 개선 확인
  음극 delithiation (셀 방전) GITT-OCV 이용 fitting
  음극 lithiation GITT-OCV와 최적 Si OCP 상이
  fitmincon 외의 optimization algorithm 적용 예정 (PSO, ga 등)
- 0.5C dQ/dV curve의 PVS 추출
- 0.5C PVS의 열화모드/SOH와 상관관계 분석
```

| 메모 | 덱 | 판정 |
|---|---|---|
| "fitting option (ub, lb) 수정" | p.5 "ub, lb, **initial** 수정" | 일치, 메모가 initial 을 뺐다 |
| "Fitting 성능 개선 확인" | p.5 "Euclidean loss 적용 시 fitting quality 향상" — **비교 수치 없음** | 구술로만 확인, 덱에 근거 그림 없음 |
| "음극 delithiation (셀 방전) GITT-OCV 이용 fitting" | p.4 "Si OCP 이용 방전 GITT-OCV fitting" | 일치 |
| "음극 lithiation GITT-OCV 와 최적 Si OCP 상이" | p.4 "충/방전 GITT-OCV 의 최적 fit OCP 가 다름" (Lu ↔ Li) | 일치 |
| "**fitmincon 외의 optimization algorithm 적용 예정 (PSO, ga 등)**" | **덱에 없음.** p.1 차주 계획은 랜덤 포레스트·성능 평가·딥러닝 | **구술 전용** — optimizer 가 `fmincon` 이라는 사실도 여기서만 나온다 |
| "0.5C dQ/dV curve 의 PVS 추출" | p.8 동일 문장 | 일치 |
| "0.5C PVS 의 열화모드/**SOH** 와 상관관계 분석" | p.8 "열화모드와 선형성 X" — SOH 언급 없음, 상관 그림 없음 | 메모가 SOH 축을 더 적었다, 덱은 결론 한 줄만 |
| (없음) | p.1 **LAM_Si 도입** · p.6 LAM_Si/LAM_Gr 궤적 | **메모에 없음** — 이 덱의 가장 큰 변화가 메모에서 빠졌다 |
| (없음) | p.1·p.7 **Euclidean distance 목적함수** (식 인쇄) | 메모에 없음 ("성능 개선" 으로만) |
| (없음) | p.3 Si OCP 문헌 8종 | 메모에 없음 |
| (없음) | p.1 딥러닝 모델 학습 (금주·차주) | 메모에 없음 |
| 제목 "Si-graphite ‖ NCM811 system ICA 모델링" | 덱 제목 "Battery health 분석" / "BMS Health Index 개발 — Health indicators for state-of-the-art commercial LIBs" | 메모의 제목이 세미나 순서표 쪽 표기로 읽힌다 |

---

## 2026-09-02 덱 → 2026-09-21 덱: 무엇이 바뀌었나

| 축 | 09-02 (15쪽, 프레임워크 발표) | 09-21 (8쪽, 주간 보고) |
|---|---|---|
| 모드 좌표 | LLI · LAM_PE · LAM_NE 3개 (P2D 스윕에서만 Si loss / Gr loss 를 따로 그림) | LLI · LAM_PE · LAM_NE **+ LAM_Si · LAM_Gr** (음극 성분 분해) + γ_Si 궤적 |
| 라벨 생성기 | "half-cell OCP 를 full-cell OCV 에 fitting" (Birkl 계열, 상세 없음) | 같은 계열 + **γ_Si 자유 파라미터(blend 합성)** + **ub/lb/initial 수정** + **Euclidean distance loss** + pOCV·dV/dQ 가중합 (식 인쇄) |
| 음극 OCP 입력 | 미언급 | **음극 GITT-OCV 실측(충·방 양방향)** + **Si OCP 문헌 8종**, 방향에 따라 최적 문헌이 다름 |
| 라벨 불확실성 | 없음 | 없음 (변화 없음) |
| feature | PVS(0.05C pOCV ICA) + SEV(CI) | **PVS 를 0.5C dQ/dV 에서** 추출 시도 → "열화모드와 선형성 X" (SEV 언급 없음) |
| ML | Random forest · LOGO-CV · MAE ≤ 0.6 %p (정답 축 Fitted) | **차주 계획**: RF 진단 모델 재학습 + 성능 평가 + 딥러닝 — 결과 없음 |
| 데이터 | 18 셀 MJ1 3.5 Ah, RPT 50 사이클 | 셀 `#8` rpt 0–700 (p.8), "400 cycle knee 이후 셀" 1개 (p.6) — 셀 수·화학 미인쇄 |
| 09-02 p.15 discussion points | ① fitting quality ② LAM_NE → Si/Gr ③ dQ/dV 계산 → PVS | ① p.5·p.7 ② p.6 ③ p.8 — **셋 다 착수**, 셋 다 유일성·불확실성은 안 봄 |

`[해석]` 한 줄로: 09-02 는 **라벨을 소비하는 쪽(ML)** 을 보였고, 09-21 은
**라벨을 만드는 쪽(fitting)** 을 고쳤다. 고친 방향은 전부 **자유도를 늘리고
(γ_Si) 목적함수를 관대하게(Euclidean) 만드는 것**이며, 그 결과로 곡선 일치는
좋아졌다고 말하지만 파라미터의 유일성은 어디에서도 묻지 않는다. 그 라벨의 첫
궤적(p.6)이 −23 % 를 포함한다.

---

## 우리 프로젝트와의 접점 (요약 — 상세는 컴파일 페이지)

- **같은 좌표다.** 우리 `degradation-degeneracy` 의 액체셀 5-파라미터
  `(a_PE, b_PE, a_NE, b_NE, γ_Si)` 와 이 덱의 정량화 코드(4 정렬 + γ_Si)는
  구조가 같다 ([[fitting-degeneracy]]). 우리가 PyBaMM 합성 truth 로 재는
  것이 정확히 "이 5개가 유일하게 정해지는가" 이고, 우리 쪽 수치는 artifact +
  `degradation-degeneracy/docs/RESULTS*.md` 가 정본이다 (여기 복사하지 않는다).
- **우리가 이 발표자에게 되돌려 줄 수 있는 것 둘**: (1) `(γ_Si, α_NE)` 평면의
  근최적 폭 — p.6 의 −23 % 가 축퇴인지 물리인지를 가르는 유일한 수단이고,
  [[22p-physics-or-degeneracy]] 에 미실행 항목으로 이미 등록돼 있다;
  (2) 이력 전제 — Si OCP 가 방향 의존이면 우리 합성 truth(단일 OCP 함수)는
  **이상적 하한**이고 실셀에는 오설정 편향이 더해진다는 유효범위 표기
  ([[halfcell-ocp-shape-invariance]]).
- **가져올 것**: p.7 의 L_euc 식 — 우리 목적함수 비교(2026-08-20 "dQ/dV 항을
  더했더니 나빠졌다") 의 대조군으로, 같은 격자에서 **곡선 일치 vs 근최적 폭**
  을 paired 로 재 볼 수 있다 (미실행).
- **경고를 갱신한다**: [[pvs-sev-lli-lampe-separability]] 의 Gap "LAM_NE 를
  Si/Gr 로 쪼개면 미지수 4개 → 식별성이 반드시 나빠진다(미정량)" 이 이 덱
  p.6 에서 **첫 야생 징후**를 얻었다.

---

## 실제로 본 그림

크로핑 8장(`fig_1` ~ `fig_8`, 페이지 단위) **전부** Read 로 봤다. 본문 서술과
어긋난 그림: (a) p.5 "fitting quality 향상" — 비교 대상 그림이 없다;
(b) p.6 "LAM_Si 반영" — 같은 그림의 LAM_Si 가 3점에서 음수; (c) p.8 "열화모드와
선형성 X" — 상관 그림이 없다; (d) 상위 메모의 "p.7 비교 그림 6장" — 실제는
모식도 1장 + 식 5개. 값을 그림에서만 읽은 곳은 전부 `figure-read ≈` /
`[도표]` 로 표시했고, 그림 안에 인쇄된 값(p.4 의 γ_Si·RMSE, p.8 의 제목·범례)은
`[도표-인쇄]` 로 구분했다.
