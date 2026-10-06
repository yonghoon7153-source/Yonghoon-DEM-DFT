---
title: "Asheruddin N, Leal De Souza, Holland, Folkson, Offer, Marinescu 2025 — Phantom LAM and LLI: Resistance and Hysteresis Bias in Voltage-Curve Degradation Mode Analysis (arXiv 2512.19773v1 · 사전인쇄)"
source_url: https://arxiv.org/abs/2512.19773v1
source_note: "사용자 업로드 2026-10-06 — 12 쪽 (하이라이트 1 + 본문 11) · 1,239,480 B. PDF 는 저장소에 넣지 않는다 — 해시만 적는다. SI 없음 (본문 언급 0)."
pdf_sha256: 222dcd2d4af4f6ac609f825962941fada745ba3886ee8ae4225b2e6ef5c424b9
ingested: 2026-10-06
sha256: 0de18219c97a62519db3a98aa424a7cfe019f4ceb0114c5d004529acf960842f
---

# Asheruddin N 외 2025 — "유령" LAM · LLI: 전압 곡선 열화 모드 분석의 저항 · 이력 편향 (arXiv 사전인쇄)

> **Mohammed Asheruddin N** (교신) · Matheus Leal De Souza · Thomas Holland · Catherine Folkson · Gregory Offer ·
> Monica Marinescu — 전원 Imperial College London (Exhibition Rd, South Kensington, London SW7 2AZ).
> "Phantom LAM and LLI: Resistance and Hysteresis Bias in Voltage-Curve Degradation Mode Analysis",
> arXiv:2512.19773v1 [physics.chem-ph], 2025-12-22. 쪽 머리 "Preprint submitted to Elsevier" — **동료 심사 전 사전인쇄**.
> 12 쪽 = 하이라이트 1 쪽 + 본문 "Page 1–11 of 11". 그림 9 · 표 0 · 식 13 · 번호 참고문헌 16.
> **SI: 본문 · 그림 어디에도 Supplementary · Supporting Information · SI 언급이 없다 (0 회)** — 미수령 항목 없음.
> 서지 대조 (호출자가 준 검색 결과): 제목 · 저자 여섯 · 순서 일치. 소속은 Imperial College London 하나. 1 저자의 성(姓)은
> 원문 표기상 "N" 이다 (저자 줄 "Mohammed Asheruddin N" · ORCID 줄 "(M.A. N)") — 이 위키 slug 는 검색성을 위해 `asheruddin2025_…` 로 쓴다.
> 자금: Innovate UK (MESM_PA8435) · Faraday Institution Multiscale Modelling (MESM_PB3785). 자료: Zenodo
> `https://zenodo.org/records/10637534` · DMA 도구: PyProBE `https://github.com/ImperialCollegeLondon/PyProBE` (둘 다 이 세션에서 열지 않았다).
> 라이선스 표기: PDF 안에 없음. 원문 PDF 는 저장소에 넣지 않았다 (sha256 은 frontmatter).

**표기 4구분** — `[인쇄]` 원문 본문 · 캡션 · 그림 안 글자로 있는 것 · `[도표]` 그림에서 읽은 것 (`figure-read ≈`; 선 그래프는
LAM 축 ±0.1–0.3 %p · Si 축 ±0.5–1 %p · SoH ±0.2 %p, 색 막대 판독은 ±2 mΩ 수준으로 거칠다) · `[재현]` 원문 값 (또는 `[도표]`
값) 으로 한 이 위키의 산술 — 자료 · 코드 실행이 아니다 (`[재현·가정]` 은 원문에 없는 가정 하나를 넣은 산술, 가정을 그 자리에
적었다) · `[해석]` 이 digest 의 추론. 이 표시가 없는 문장은 원문이 실제로 말한 것이다 (말을 바꿔 적었을 뿐).

**이 digest 의 자리.** 컴파일 개념은 [[pocv-nonequilibrium-mode-bias]] (pOCV 의 비평형 성분이 모드로 새는 경로).
걸리는 위키 축: [[fitting-degeneracy]] (같은 증상 · 다른 원인) · [[halfcell-ocp-shape-invariance]] (Si 방향 의존 · `γ_Si` 처방 ③) ·
[[np-lip-ocv-reparametrization]] (SOC 정규화와 셋째 자유도) · [[pyprobe]] (이 논문이 쓴 도구) · [[22p-physics-or-degeneracy]] ·
[[isu-uconn-lfp-gr-emulated-degradation]] (REIL). **우리 연구 수치는 여기에 옮기지 않는다** — 정본은 artifact +
`degradation-degeneracy/docs/RESULTS*.md` · `docs/09_22P_GAP.md` 이고 이 digest 는 경로만 가리킨다.

---

## 0. 한 문단 요약

저율 전압–용량 곡선으로 LLI · LAM 을 가르는 DMA (degradation mode analysis) 는 OCV 가 아니라 **pOCV (pseudo-OCV)** 를
맞춘다. pOCV 에는 열화가 아닌 성분 둘 — (i) SOC 에 따라 크기가 달라지는 옴 강하, (ii) 충 · 방전 가지 사이의 이력 (특히
흑연–산화규소 C/SiOx 음극) — 이 남아 있고, 저자들은 이것이 **곡선 등록 (curve registration) · 가지 선택 · 전압 창 선택**을 거쳐
"유령 (phantom)" LAM/LLI — 열화가 아닌데 열화로 읽힌 양 — 을 만든다고 주장한다. 실험은 상용 21700 두 종: **LG M50T**
(NMC811 ‖ C/SiOx, "higher resistance", Kirkaldy et al. 자료) 로 IR 효과를, **Molicel P45B** (고 Ni NCA ‖ C/SiOx, "low
resistance") 로 창 · 가지 효과를 본다. ≈50 ms 펄스 첫 전압 계단으로 `R_Ω(SOC)` 를 재서 **옴 성분만** pOCV 에 되돌려 놓고
(IR 보정), Gr/Si blend 반쪽전지 pOCP 두 개를 늘이고 미는 5 매개 적합 (`θ = {ν_NE, ν_PE, σ_NE, σ_PE, φ_Si}` · 전압 + 기울기
잔차) 을 구성마다 다시 돌려 비교한다. M50T: 보정이 방전 pOCV 를 +13–27 mV 들어 올리고, 미보정 분석은 LAM_PE 를 과소
(상대 −0.24 → −8.80 %) · LLI 를 과소 (중앙 −3.07 %) · 흑연 LAM 을 과대 (중앙 +17.68 %) 로 낸다. P45B: 같은 3.0–4.2 V 창에서
충전 가지가 LAM_PE +3.42 pp · LLI +5.36 pp 높게, 방전 가지가 Si-LAM 을 최대 +14.38 pp 크게 낸다; 방전 창 하한을
2.5 → 3.0 V 로 자르면 Si-LAM 이 13.61 pp 줄어든다. 처방: 옴 성분만 보정 · 가지 간 같은 창 · 정량은 방전 가지 · 충전 가지의
음수 구성요소 LAM 은 "할당 인공물 (allocation artefact)" 로 취급.

## 0-1. 이 digest 의 결론

1. **이 논문이 잰 것은 "참값 대비 오차" 가 아니라 "구성 간 차이" 다.** IR 보정 ↔ 미보정, 2.5 ↔ 3.0 V, 충전 ↔ 방전 — 어느
   쪽에도 참값 (해체 · 반쪽전지 재측정 · 기준전극 · 합성 truth) 이 없고 저자도 `[인쇄]` "We do not claim the corrected value
   is the exact thermodynamic truth" 라고 쓴다. 그러므로 "방전이 평형에 더 가깝다 · 전체 창이 Si 손실을 되찾는다" 는 측정
   결론이 아니라 **모델 선택 논증**이다 `[해석]`. 세 실험 모두에서 저자가 '기준' 으로 고른 구성 (보정 · 방전 · 전체 창) 이
   **Si-LAM 을 가장 크게 내는 구성**이라는 점도 같이 적어 둔다 (§14 부호표) — 참값이 없으면 어느 쪽이 유령인지 정해지지 않는다.
2. **효과 크기의 단위가 섞여 있다.** IR (M50T) 은 상대 오차 (%), 창 · 가지 (P45B) 는 %p 다. 그림으로 읽으면 IR 의 마지막 RPT
   절대 차이는 LAM_PE ≈1.0 · LLI ≈0.65 · 흑연 ≈1.2 · Si ≈3.6 %p `[도표]` — 창 · 가지의 2–14 %p 보다 작다. 셀이 달라 직접
   비교도 아니다.
3. **권고 구성 (방전 가지 · 가지 간 공통 창) 이 자기 그림에서 가장 약한 구성이다** `[도표·재현]`: (a) 공통 창은 충전이
   2.5 V 에 못 닿아 3.0–4.2 V 로 잘린 창인데 §3.4 (Fig. 6) 가 바로 그 창이 Si-LAM 을 13.61 pp 과소로 낸다고 보인다;
   (b) 그 창의 방전 값 (Fig. 6 점선 = Fig. 7 실선) 에서 ≈850 · ≈1250 Ah 의 LAM_NE 총량이 LAM_Gr · LAM_Si 사이에 있지 않아,
   원문이 "within numerical tolerance" 라고 쓴 blend 규칙 `Q_NE ≈ (1−φ_Si)Q_Gr + φ_Si Q_Si` 를 어떤 `φ ∈ [0,1]` 로도 만족하지
   못한다 (§2-m); (c) 흑연 LAM 이 ≈6 % 까지 올랐다가 ≈2 % 로 내려간다 (겉보기 '회복'). 원문은 비물리 값을 충전 가지의 음수에
   대해서만 '할당 인공물' 이라 부른다.
4. **식별 가능성은 다루지 않는다.** `identifiab*` 1 회 (IR 측정 보정이 "preserves identifiability" 한다는 근거 없는 한 줄) ·
   `degenera*` · `uniqu*` · `uncertain*` · `error bar` · `confidence` · `multi-start` · `correlat*` 전부 0. 적합 잔차 · 적합
   매개변수 값 (`φ_Si` 포함) · 반복 셀 · 오차 막대도 0. "음수 Si-LAM = blend 안의 과 · 소 보상" 은 **보상 방향 (축퇴) 의 산문
   진술**이지만 재지 않았고, 스스로 권한 "constrained re-fit sensitivity" 도 하지 않았다 `[해석]`.
5. **원문 내부 불일치가 많다** (§2 — 가지 ↔ 전극 과정 · 부호 · `ν` 규약 · 저항 대소 · 그림 ↔ 본문 수치 · 인용 다섯이 참고문헌
   목록에 없음). 사전인쇄 상태 (본문에 마크다운 별표가 인쇄됨) 까지 같이 보면, 수치는 그림과 본문을 대조한 것만 인용한다.
6. **우리에게 쓸모가 크다** (§15): (a) 우리 `ocpbias` 의 PE 오프셋 다리는 이 논문의 "SOC 무관 IR 미보정" 과 **수학적으로 같은
   섭동**이다 (식 3: 기준 곡선 +δ ≡ 측정 곡선 −δ) — 이 논문이 못 한 "참값 대비 오차" 로 그 방향 주장을 시험할 자리;
   (b) 우리 합성 truth 는 이미 이 논문이 권하는 구성 (방전 가지 · 가지 일치 Si 기준 · 0.05 C) 위에 있다 — 그래서 우리 축퇴
   측정은 가지 · IR 편향을 **뺀** 하한이다; (c) REIL 의 C/20 충전 맞춤에는 **방향만** 옮겨진다 (위로 밀린 충전 곡선 → 창 안
   용량 ↓ → 겉보기 LLI ↑ · dV/dQ 목적은 균일 이동에 둔감) — 크기는 옮겨지지 않는다.

---

## 1. 원문에 없어서 확인이 필요한 것 (공백 목록)

1. **반쪽전지 pOCP 의 출처** — M50T · P45B 각각 어느 반쪽전지 (해체? 문헌?) · 어느 율 · **어느 가지** (리튬화/탈리튬화) 인지
   없다. §4 측정 모형은 "branch-specific pseudo-OCPs `U^(b)`" 를 쓰지만 DMA 가 가지별 기준을 썼는지 (→ '이력 편향' 의 뜻이
   달라진다) 는 미기재. Fig. 9 가 가지별 전류 분배를 그리므로 가지별 Si · Gr 기준이 있었던 것으로 보이나 `[해석]` 적합에
   들어갔는지는 알 수 없다.
2. **`φ_Si` 적합값** — 어느 셀 · RPT · 가지에서도 숫자 0 (Fig. 9 제목의 "φ_Si = 0.2" 는 그림용 설정으로 보인다).
   매개변수 값이 인쇄된 곳은 Fig. 8 의 `ν_PE` 두 개뿐이다.
3. **적합 세부** — `λ` 값 · 내부 가중 마스크 · 평활 · 최적화기 · 시작점 · 경계 · 다중 시작이 없다. `[인쇄]` "details of
   smoothing and interior masks follow their setup" 로 Karger et al. 에 미루는데 **Karger et al. 은 참고문헌 목록에 없다**.
4. **적합 품질** — 어떤 구성의 잔차 (RMSE) 도 보고하지 않는다. 그래서 "두 구성이 똑같이 잘 맞는데 답이 다르다" (축퇴) 인지
   "한쪽이 덜 맞는다" (오설정) 인지 원문으로 가를 수 없다.
5. **셀 수** — "Two commercial 21700 cells were studied" · "Each cell underwent five break-in cycles" 로 읽으면 종류당 1 셀.
   반복 · 셀 간 산포 · 오차 막대 0. 수명 시험은 "≤80 % capacity retention" 까지라고 적지만 M50T 그림은 SoH ≈88 % 에서 끝난다
   `[도표]`.
6. **모드 정규화** — 식 (10) 은 `LAM_x = 1 − Q_x` (`Q_FC = 1`) 인데 글자 그대로면 신품에서 LAM ≠ 0 이다 (Fig. 8 의
   `ν_PE` 0.76–0.79 → `Q_PE ≈ 1.3 Q_FC`). 그림의 모든 모드가 RPT-0 에서 0 이고 Fig. 8 산술이 가지마다 다른 신품 기준을
   함의하므로 (§10), 실제로는 **가지 · 창마다 자기 RPT-0 적합으로 나눈 것**으로 보인다 `[도표·재현]`. 그리고 RPT 마다 SOC 를
   자기 방전 용량으로 정규화 (`[인쇄]` "cycle-local SoC") 했다면 셋째 자유도 (공통 인수 — [[np-lip-ocv-reparametrization]]) 를
   무엇으로 닫았는지 (`Q_FC` 를 RPT 의 절대 용량으로 바꿨는지) 미기재. 보고된 LLI 가 SoH 감소와 같은 크기로 자라 (P45B 전체 창
   EOL: LLI ≈19.5 % · SoH 80.57 %) 절대 용량을 쓴 것으로 보인다 `[도표·해석]`.
7. **P45B 분석에 IR 보정을 했는지** — §3.4 · 3.5 · Fig. 6 · 7 어디에도 없다. 저항이 낮다는 근거 (Fig. 3) 는 SoH 0.93 (≈850 Ah)
   까지만 있고 DMA 는 1982.5 Ah (창 안 SoH ≈81–84 %) 까지 간다. 보정을 안 했다면 `[재현·가정]` C/20 · `R` 23–26 mΩ ·
   `Q_FC` ≈4.50 Ah (Fig. 8 산술에서 역산, §10) 로 가지마다 `I·R` ≈5–6 mV, 두 가지 사이 ≈10–12 mV 가 '이력' 에 섞인다 —
   원문이 인용한 흑연 이력 (≈10–30 mV) 과 같은 자릿수이고, Fig. 4a 중간 SOC 가지 간격 (≈60–70 mV `[도표]`) 의 15–20 %.
8. **M50T 의 `R_Ω(SOC)` 가 SOC 30–70 % 밖에서 어떻게 정해졌는지** — Fig. 1 의 점은 SOC ≈30–70 % 에만 있다 `[도표]`.
   본문의 "상단 10 % 에 +20.1 / +26.9 mV" 를 C/10 전류 (원문에 기준 용량 미기재 — Fig. 2a 첫 곡선 ≈4.5 Ah 로 ≈0.45 A,
   공칭이 더 크면 ≈0.5 A) 로 나누면 `R` ≈40–60 mΩ 으로, 측정 범위 (색 막대 18–34 · 본문 최대 31–34 mΩ) 위다 `[재현·가정]` →
   **측정 범위 밖 외삽에서 나온 값**으로 보이며, 원문은 범위 안 보간 (모양 보존 cubic Hermite) 만 서술한다.
9. **Fig. 1 (펄스) 과 Fig. 5 (pOCV) 의 RPT 가 서로 다르다** `[도표]` — Fig. 1 열은 ≈0 · 1270 · 2520 · 3730 · 4980 Ah 에
   SoH 1.00 · 0.99 · 0.97 · 0.95 · 0.94, Fig. 5 는 ≈0 · 700 · 1400 · 2050 · 2700 · 3350 · 4000 Ah 에 SoH 100 · 96 · 94 · 93 ·
   91 · 90 · 88 %. ≈3700 Ah 근처에서 SoH 가 0.95 ↔ ≈0.90 으로 갈린다. 같은 셀인지 · SoH 정의가 같은지 · 각 pOCV RPT 에 어느
   `R_Ω(SOC)` 를 썼는지 (노화 축 보간?) 미기재.
10. **M50T GITT "200 mAh × 25 펄스" ↔ Fig. 1 의 점** — 그림은 RPT 당 21 점 · SOC 2 %p 간격 · 30–70 % 다 `[도표]`. 셀 용량
    ≈4.5 Ah 면 200 mAh 펄스는 ≈4.4 %p 간격이어야 한다 `[재현·가정]`. 그림의 점이 측정점인지 보간값인지 미기재.
11. **이력 띠 합의 계산 축** — §2 의 (j) · (k).
12. **Zenodo 10637534 의 내용** (M50T · P45B 둘 다인지) — 열지 않았다.
13. **참고문헌 목록에 없는 인용 다섯**: "Karger et al." (§2.4 두 번 · §4 "[Karger et al., 2023]" 두 번 — DMA 틀의 원전) ·
    "Kirkaldy et al." (§2.1 · §4 "[Kirkaldy et al., 2024]" — M50T 자료의 원전) · "Kim et al., 2021" · "Berg et al., 2025" (§4 ·
    Fig. 8) · "Beiranvand et al." (Fig. 8 만). `[해석]` 이 위키의 다른 digest 에 Karger 가 공저자인 TUM 문헌 (Schmitt · Rehm ·
    Karger · Jossen 2023, `raw/papers/thelen2024_probabilistic-ml-battery-health-review.md` 의 인용표) 이 있으나 같은 편인지 확인할
    방법이 원문에 없다.
14. **PyProBE 판 · 기능** — 5 매개 blend 적합 · 기울기 잔차 · IR 보정 가운데 무엇이 PyProBE 에 있는지, 어느 판인지 미기재.
    이 위키가 2026-10-01 에 시험한 PyProBE 2.6.0 은 창 4 매개였다 ([[pyprobe]]).

## 2. 원문 내부 불일치 (본문 ↔ 식 ↔ 그림)

- **(a) 가지 ↔ 전극 과정.** §2.1 `[인쇄]` "“Charge” denotes lithiation of the negative electrode; “discharge” denotes
  delithiation" (물리적으로 맞다). 그런데 §3.5 "During charge, the NE delithiates along a higher-potential path", §4 "during
  full-cell charge the NE delithiates … while discharge follows a lower-potential lithiation path", Fig. 9 해설 "on discharge
  (NE lithiation) … on charge (NE delithiation)", §5 "the charge branch (NE delithiation)". Fig. 8 Cause A 는 다시 "Si
  lithiation on charge". → 충전의 음극 과정이 한 논문 안에서 두 가지로 적혀 있다.
- **(b) 부호.** 식 (3) `U_cell = U_PE − U_NE` 에서 음극 전위가 오르면 전지 전압은 내려간다. 그런데 §3.5 · §4 는 "NE … higher-
  potential path → the measured full-cell curve is therefore uplifted", Fig. 8 Cause A 는 "compression raises the anode
  potential U_NE on charge … → charge pOCV sits above", Effect 2 는 "a positive ΔU_NE … you hit 4.2 V earlier". 관측 (충전
  곡선이 위) 은 흔한 것이지만 기전 문장은 자기 식 (3) 과 부호가 반대다 `[해석: 관측과 맞는 기전은 '충전 (음극 리튬화) 에서
  음극 전위가 더 낮다' 쪽]`.
- **(c) `ν` 규약.** 식 (6) · (8) 은 `Q_x = Q_FC/ν_x` — `ν` 가 클수록 전극 용량이 작다 (LAM ↑). §4 · Fig. 8 ("larger ν_PE →
  … over-estimation of LAM_PE" · `ν_PE` 0.788 → `Q_PE` 5.71 Ah < 0.764 → 5.89 Ah) 은 이 규약과 맞다. §3.2 는 반대다 —
  "greater PE scaling (larger effective ν_PE^−1 → more LAM_PE)" · "over-scaling the NE (smaller ν_NE) which DMA reads as
  graphite LAM". 결과의 부호가 아니라 **해설의 매개변수 방향**이 식과 어긋난다.
- **(d) 저항 대소.** 초록 · §2.1 은 M50T "higher resistance", P45B "lower resistance" 로 나누지만 §3.1 수치는 첫 RPT 에서
  M50T 19–22 mΩ < P45B 23–26 mΩ 이다. "well below the LG M50T values" 는 노화 끝 (31–34 mΩ) 에서만 맞다. 율 · 용량을 곱한
  `I·R` 로는 P45B (C/20) 가 작을 수 있으나 `[해석]` 원문은 그 산술을 하지 않는다.
- **(e) P45B 펄스 SOC.** §2.2 "25 %, 50 % and 75 % SoC" ↔ §3.1 · Fig. 3 "≈30, 50 and 70 %".
- **(f) 축 이름.** Fig. 3 세로축 "State of Charge (%)" 인데 눈금은 0.30–0.70 (분율). Fig. 1 색 막대 "Total Resistance (mΩ)" ↔
  본문 "instantaneous ohmic resistance" (캡션은 둘 다 쓴다).
- **(g) 처리량 ↔ SoH** — §1-9.
- **(h) M50T 저항 모양.** 본문은 저항이 "increases with age and toward high SOC" · "largest values above 60 % SOC" 라 쓰지만,
  Fig. 1 은 30–70 % 창 **양끝이 다 높은 U 자**다 (가운데 ≈46–50 % 가 최소 · 마지막 열은 ≈38–40 % 도 ≈30 mΩ 색) `[도표]`.
  첫 RPT 열도 끝단 마커는 ≈26–28 mΩ 색이라 "19–22 mΩ at the earliest RPT" 는 가운데 값에 가깝다 `[도표 — 색 판독]`.
- **(i) IR 끌어올림 크기 ↔ 측정 `R`** — §1-8.
- **(j) 이력 띠 합 ↔ Fig. 4b 막대** `[재현 — 막대 판독 합, ±0.1/막대]`. 막대는 SOC ≈10 % 부터 5 % 폭으로 18 개다. 첫 RPT 의 합은
  10–30 % ≈7.8 · 30–50 % ≈2.9 · 50–80 % ≈13.5 · 80–100 % ≈22.8 · 전체 ≈47.0, 끝 RPT 는 ≈7.5 · ≈2.4 · ≈13.9 · ≈23.5 · ≈47.2.
  본문의 80–100 % (22.759 → 23.474) · 전체 (47.073 → 47.427) · 끝 RPT 0–30 % (7.374) 는 막대와 맞는다. **첫 RPT 0–30 %
  "13.406" 만 맞지 않는다** — 10 % 아래 막대가 없고, 13.406 을 맞추려 숨은 ≈5.6 을 더하면 전체가 ≈52.6 이 되어 본문 47.073 과
  어긋난다. 그러므로 헤드라인 "저 SOC 이력 −45 %" 는 그림이 받치지 않는다 (그림의 10–30 % 는 ≈7.8 → ≈7.5, ≈−4 %).
- **(k) Fig. 4a ↔ 4b 의 크기 · 모양** `[도표]`. 4a 에서 두 가지 간격은 중간 SOC ≈60–70 mV · 80–95 % ≈30–50 mV · 5–10 %
  ≈150–230 mV 로 읽힌다 (확대 판독 ±10 mV). 4b 의 95–100 % 막대 ≈7.5 V·%SOC 는 5 %SOC 폭에서 평균 |ΔV| ≈1.5 V 에 해당한다.
  크기가 수십 배 다르고, 모양도 반대다 (4a 는 저 SOC 끝이 크고 4b 는 고 SOC 끝이 크다). SOC 축을 뒤집으면 모양은 맞지만 크기는
  여전히 수 배 어긋난다 `[재현]`. 적분 변수 · SOC 축 방향 · 단위 중 무엇이 다른지 원문이 주지 않는다.
- **(l) Fig. 8 예시 ↔ Fig. 7 · Fig. 9.** Fig. 8 `[인쇄 — 그림 안 글자]` "At 600 cycles: … LAM_PE^chg (7.0 %) > LAM_PE^dchg
  (0.8 %) (790 % overestimation in charge)" · "LLI^chg (18.8 %) > LLI^dchg (12.3 %) (53 % overestimation in charge)" — Fig. 7
  의 어느 RPT 와도 같지 않다 (충전 LAM_PE 최대 ≈5.75 % · EOL LLI ≈19.1 / ≈13.7 % `[도표]`). 그림 축은 처리량 (Ah) 이고 "600
  cycles" 의 대응이 없다. Effect 1 "more Li goes into Si on charge … +10–12 pp on average, peaks ~27–30 pp [exp observation]"
  은 Fig. 9 · §4 ("on charge … Si participation is suppressed") 와 반대 방향이고, Fig. 9 자체는 기준 곡선에서 계산한 것 (`[인쇄]`
  "derived from the blend templates and local slopes") 이지 실험 관측이 아니다. Fig. 8 이 가리키는 "(1)–(4)" 는 원문 식
  번호와 맞지 않는다 (원문 식 (2) 는 이력 면적).
- **(m) blend 규칙 ↔ 그림 값** `[재현 — 판독값으로 역산]`. 원문 `[인쇄]` "the blend rule Q_NE ≈ (1 − φ_Si)Q_Gr + φ_Si Q_Si
  stays within numerical tolerance". `LAM_NE = (1−φ₀)LAM_Gr + φ₀ LAM_Si` (φ₀ = 신품 Si 몫) 로 판독값에서 φ₀ 를 풀면 —
  전체 창 방전 (Fig. 6 실선): ≈850–1982 Ah 에서 0.226–0.234 로 **일정** · 공통 창 충전 (Fig. 7 점선): 0.27–0.35 ·
  공통 창 방전 (Fig. 6 점선 = Fig. 7 실선): ≈215–430 Ah ≈0.8 · ≈850 Ah ≈1.9 · ≈1250 Ah ≈−0.5 · ≈1630–1982 Ah ≈0.05–0.08.
  ≈850 Ah (LAM_NE ≈2.2 · LAM_Gr ≈6.2 · LAM_Si ≈4.1 %) 와 ≈1250 Ah (≈3.1 · ≈5.6 · ≈10.3 %) 에서는 총량이 두 구성요소 사이에
  있지 않아 **어떤 φ ∈ [0,1] 로도 규칙이 성립하지 않는다**. 그리고 같은 셀의 신품 Si 몫이 가지 · 창마다 다르게 나온다
  (≈0.23 ↔ ≈0.3 ↔ 일관 없음). `[해석]` 잘린 창의 '구성요소 retention' 이 창 안 접근 용량의 비라면, 미끄럼이 창 안 내용을 바꿀
  때 LAM 이 물질 손실 없이 움직인다 — 비단조 흑연 LAM 과 규칙 위반이 같이 설명되는 후보지만 원문으로 확인되지 않는다.
- **(n) 권고 ↔ 창 결과.** 처방 `[인쇄]` "perform quantitative DMA on the discharge branch within a harmonized voltage window"
  (초록: "enforce a harmonized voltage window across branches"). 가지 간 공통 창은 3.0–4.2 V 이고 §3.4 가 그 창이 Si-LAM 을
  13.61 pp 과소로 낸다고 보인다. 두 권고가 함께 성립하는 창이 원문에 없다 `[해석]`.
- **(o) Si 민감 구간의 위치.** §3.2 "Silicon sits on the steep NE segment near the top of discharge" ↔ §3.4 "the omitted 2.5–3.0 V
  band is precisely where the Si-dominated degradation signature resides" (방전 끝) ↔ §4 "As SOC approaches the extremes—where Si
  becomes thermodynamically active".
- **(p) 조판 · 저자 표.** 본문이 "§3.3.2" 를 가리키지만 해당 절은 3.5 · "under-diagnosedif" · "(median ≈ **-3.07 %**)" 가
  별표째 인쇄 (p.5 렌더로 확인) · CRediT 에 저자 Thomas Holland 가 없고 "Asheruddi" · "Lead De Souza" 오자.

---

## 3. 하이라이트 · 초록 (p.0–1)

하이라이트 다섯 `[인쇄]`:
- "“Phantom” LAM/LLI arises when DMA is applied directly to uncorrected pseudo-OCV (pOCV) curves."
- "Instantaneous R_Ω(SOC) from ∼50 ms pulses provides a clean ohmic-only IR correction for DMA."
- "In LG M50T, omitting IR correction suppresses PE-LAM and LLI and inflates apparent graphite loss."
- "In Molicel P45B, hysteresis and voltage-windowing drive large charge–discharge differences in inferred Si loss."
- "A practical prescription: ohmic-only correction, harmonized window, and discharge-branch DMA for robust attribution."

초록의 뼈대: DMA 는 저율 곡선에서 LLI · LAM 을 가른다 → 실측은 pOCV 이고 비열화 성분 둘 (SOC 의존 옴 강하 · 고유 이력,
특히 C/SiOx) 이 남는다 → `[인쇄]` "these effects can dominate DMA attribution and generate phantom LAM/LLI—apparent material loss
created by curve registration, branch choice, and voltage-windowing rather than true degradation" → M50T: IR 보정이 방전 pOCV 를
"approximately +13–27 mV with ageing" 올리고, 무시하면 "PE-LAM is increasingly under-diagnosed (down to −8.80 % relative error
at late life) and LLI is suppressed (median −3.07 %), with compensating inflation of apparent graphite loss" → P45B
"branch-fair 3.0–4.2 V window": EOL 충전 가지 PE-LAM +3.42 pp · LLI +5.36 pp, 방전 가지 Si-LAM 차 +14.38 pp; 하한
2.5 → 3.0 V 로 Si-LAM 13.61 pp 과소 → 처방: "correct only the instantaneous ohmic term, enforce a harmonized voltage window across
branches, and base quantitative attribution primarily on the discharge branch, treating anomalous/negative component LAMs on
charge as allocation artefacts rather than physical recovery".

키워드 `[인쇄]`: DMA · resistance (R_Ω) correction · voltage hysteresis · voltage-window sensitivity · branch selection ·
graphite–silicon oxide (C/SiOx) anode · LLI · LAM.

## 4. 서론 §1 (p.1–2)

- DMA 의 발상 `[인쇄]`: 정해진 온도에서 완전지 서명을 평형 근처의 양 · 음극 전위 차로 읽을 수 있으므로 겹침 · 모양 변화를
  리튬 손실 · 활물질 손실로 사상한다 ([6, 4]).
- 실측은 OCV 가 아니라 "a low-current, finite-rest pseudo-OCV (pOCV)" 이고 평형에서 벗어나는 두 성분이 있다:
  1. 저항/분극 — "a measurement-level translation produced by ohmic drop and mild kinetic/transport losses" · 방전 전압을 내리고
     충전 전압을 올리며 미보정이면 "shifts the entire curve by tens of millivolts" · 이전 관행은 아주 낮은 전류로 무시했고 뒤의
     연구가 명시 보정 (pulse IR · EIS · pulse-relaxation OCV) 을 권했다 ([5, 1, 3]).
  2. 이력 — "intrinsic to the materials’ thermodynamics and persists even after long rests" · 흑연 "a residual ∼10–30 mV OCV
     gap" · Si 함유 음극은 "an order of magnitude larger" · 기계적 팽창 · 소성 · 느린 이완과 결합 ([13, 10, 9]) · blend 에서는
     완전지 pOCV 와 미분 스펙트럼으로 번져 가지 선택이 결과를 바꾼다 · 최근 연구는 펄스–휴지 준평형 pOCV 나 충 · 방전 OCV 를
     따로 쓰는 모형 (또는 compact 이력 모형) 을 권했다 ([8, 15]).
- 두 성분이 고정 창 DMA 와 만나는 방식 `[인쇄]`: "any uniform translation from resistance changes where the curve intersects the
  window (re-registering features and altering apparent plateaus), while branch-dependent hysteresis changes the apparent capacity
  available at a given cut-off and shifts dQ/dV landmarks differently on charge and discharge" → '유령' LAM/LLI.
- 빈 곳 `[인쇄]`: "there is no standardized methodology that (i) corrects the measurement-level resistance translation and (ii)
  manages the thermodynamic branch dependence coherently within DMA".
- 물음 `[인쇄]`: "how do internal resistance and voltage hysteresis, separately and together, bias voltage-curve DMA (V–Q, dQ/dV,
  dV/dQ), and what practical protocol—spanning resistance correction, branch selection, and windowing—yields LLI/LAM attributions
  that best reflect material reality?" — 저항은 분석 전에 보정할 "reversible measurement translation", 이력은 "inherent
  thermodynamic property to be quantified and managed (not “subtracted”)" 로 둔다.
- `[해석]` 물음은 "separately **and together**" 인데 실험은 IR 을 M50T 에서만, 창 · 가지를 P45B 에서만 본다 — 한 셀에서 셋의
  상호작용은 재지 않았다.

## 5. 방법 §2 (p.2–3)

### 5-1. 셀 · 프로토콜 · pOCV (§2.1)

| 항목 | Molicel P45B | LG M50T |
|---|---|---|
| 양극 · 음극 `[인쇄]` | 고 Ni NCA ‖ C/SiOx · "power-oriented, low intrinsic resistance" | NMC811 ‖ C/SiOx · "energy-oriented, higher intrinsic resistance; dataset after Kirkaldy et al." |
| 노화 `[인쇄]` | 2C CC–CV 충전 (CV 를 C/20 까지) · 0.5C 방전 | 0.3C CC–CV 충전 (C/100 까지) · 1C 방전 |
| RPT pOCV `[인쇄]` | **C/20** · 1 s 샘플 | **C/10** · 0.1 s 샘플 |
| 펄스 `[인쇄]` | 1C 펄스 · SoC 25 · 50 · 75 % · 양방향 (그림 · 결과는 ≈30 · 50 · 70 %) | C/2 GITT 방전 · 200 mAh × 25 펄스 · 1 h 휴지 · 2.5 V 까지 ("the full train executed irrespective of reaching cutoff") |
| RPT 처리량 `[도표]` | ≈0 · 215 · 430 · 850 · 1250 · 1630 · 1982.5 Ah (EOL 값은 `[인쇄]`) | pOCV: ≈0 · 700 · 1400 · 2050 · 2700 · 3350 · 4000 Ah · 펄스: ≈0 · 1270 · 2520 · 3730 · 4980 Ah |

공통 `[인쇄]`: 전압 창 2.5–4.2 V · 25 °C 항온 · 길들이기 5 사이클 · 수명 ≤80 % 까지 · "“Charge” denotes lithiation of the
negative electrode; “discharge” denotes delithiation" · SoC 는 그 RPT 의 pOCV 방전 용량 기준 ("cycle-local SoC") · pOCV 는
"approximate equilibrium while retaining path dependence (hysteresis)".

### 5-2. 저항 · IR 보정 (§2.2, 식 1)

```
R_Ω(SoC_k) = ΔV* / I_pulse        (1)   ΔV* = 전류 인가 후 첫 ≈50 ms 전압 계단 · I > 0 방전, I < 0 충전
```
- 1–60 s 이완은 지수 1–2 항으로 맞춰 `τ1, τ2` 를 "kinetic indicators" 로만 보고, `[인쇄]` "these slower contributions were not used
  for baseline correction to avoid importing rate-dependent structure into the pOCV".
- 이산 `R_Ω(SoC_k)` 는 "a shape-preserving cubic Hermite spline" 으로 보간해 연속 `R_Ω(SoC)` 로 만든다 (범위 밖 처리 미기재 — §1-8).
- 보정 연산은 Fig. 2 범례로 "pOCV+IR" — 방전 곡선에 `I·R_Ω(SOC)` 를 더해 올린다.

### 5-3. 이력 지표 · 창 규칙 (§2.3, 식 2)

- 저율 CC 구간만 (CV · 테이퍼 표본 제거) · `[인쇄]` "Branch-fair comparisons require that charge and discharge be analysed over an
  identical voltage range" · 완전한 저율 방전 (4.20 → 2.50 V) 은 CV 충전 뒤 재현성 있게 얻지만 완전한 충전 (2.50 → 4.20 V) 은
  비관행적 CV 방전 없이는 어렵고 유한 전류 방전은 보통 2.50 V 위로 이완한다 → **RPT 마다** 공통 창 `[V_min^com, 4.2 V]` =
  두 가지 전압 영역의 겹침 (희박한 꼬리 · 이상점 정리 후). 경계 민감도는 방전만으로 4.20–2.50 ↔ 4.20–3.00 V 비교.
- SOC 사상: 쿨롱 계수 · 같은 RPT 방전 용량으로 정규화 · 가지마다 SOC 정렬 → 스파이크 · 결측 제거 → 공통 SOC 격자 (≥600 점)
  선형 보간 → 5 % SOC 창으로 묶어 보고.
- `ΔV_s = V_chg(s) − V_dchg(s)` · 이력 크기 `A = ∫|ΔV_s| ds` (식 2, "V·%SOC") · 사다리꼴 · 5 % 창별 `A_i` · 띠 합 (0–30 % ·
  80–100 % · 전체).
- `[해석]` 공통 창이 RPT 마다 다시 정해지므로 RPT 간 띠 합은 서로 다른 SOC 구간 위의 값일 수 있다 — §6 의 "−45 %" 를 읽을 때
  창 변화와 이력 변화가 섞이는 통로.

### 5-4. DMA 틀 (§2.4, 식 3–12 — p.4 렌더로 식 모양 확인)

"as done by Karger et al." (목록 밖). `[인쇄]`:
```
U_meas(z_FC) ≈ U_mod(z_FC; θ) = U_PE(z_PE) − U_NE(z_NE)                               (3)
SOC_NE(U) = φ_Si·SOC_Si(U) + (1 − φ_Si)·SOC_Gr(U)   ("unity at lower cut-off, zero at upper cut-off")   (4)
U_NE(SOC_NE) = [SOC_NE(U)]⁻¹                                                            (5)
z_FC = (z_NE − σ_NE)/ν_NE ,   z_FC = ((1 − z_PE) − σ_PE)/ν_PE                          (6)
θ = {ν_NE, ν_PE, σ_NE, σ_PE, φ_Si}                                                      (7)
Q_NE = Q_FC/ν_NE ,  Q_PE = Q_FC/ν_PE      (Q_FC = 1 로 정규화)                           (8)
Q_LI = Q_FC·( σ_NE/ν_NE + (1 − σ_PE)/ν_PE )                                             (9)
LAM_x = 1 − Q_x (x ∈ PE, NE) ,  LLI = 1 − Q_LI   ("fractions on the analyzed window")    (10)
LAM_NE,Gr = 1 − Q_Gr ,  LAM_NE,Si = 1 − Q_Si   (적합된 φ_Si 와 식 4–6 으로 "over the same window")   (11)
min_θ ‖U_meas − U_mod(θ)‖₂ + λ‖dU_meas/dz_FC − dU_mod(θ)/dz_FC‖₂   (내부 가중 · 끝점 약화)   (12)
```
- `[인쇄]` "As in Karger et al., a small λ stabilizes plateau alignment without overweighting noise; details of smoothing and interior
  masks follow their setup."
- U_PE 는 "positive-electrode pOCP (from half-cell)", U_NE 는 "reconstructed from graphite and silicon references" — 출처 · 가지 미기재.
- `[해석]` (4) 는 **같은 전위에서 두 성분 SOC 를 용량 몫으로 더하는 blend** — 우리 `degradation-degeneracy/src/halfcell.py` 의
  `compute_halfcell_from_ocp` (Gr · Si 평형 분배) 와 같은 구성이다 (읽기만 확인). 다른 점은 이 논문이 `φ_Si` 를 **맞추고** 우리는
  baseline 용량에서 **고정**한다는 것. 전극마다 `(ν, σ)` 는 우리 창 좌표 `(α, β)` 넷과 같은 구조이고, 다섯째 `φ_Si` 는
  [[halfcell-ocp-shape-invariance]] 의 처방 ③ (Schmitt 2022 `γ_Si`) 과 같다 — [[halfcell-window-parametrization-lineage]] 다섯째 축.
- 상대 오차 (§3.2, 식 13) `[인쇄]`: `ε[%] = 100·(Original / IR-corrected − 1)` — 양이면 미보정이 과대, 음이면 과소.

---

## 6. 결과 §3.1 — 저항 · 이력의 변화 (Fig. 1–4)

**M50T 저항 (Fig. 1).** `[인쇄]` 순간 저항이 노화와 고 SOC 로 갈수록 커진다 · SoH 1.00 → 0.94 에서 `R_Ω` "from roughly 19–22 mΩ
at the earliest RPT to 31–34 mΩ at the latest, with the largest values above 60 % SOC" · SOH = 그 RPT 방전 용량 / 첫 RPT.
`[도표]` x 축 처리량 0–≈5000 Ah · 열 다섯 · 위 SoH 1.00 · 0.99 · 0.97 · 0.95 · 0.94 · 열마다 21 점 · SOC ≈30–70 % · 2 %p 간격 ·
마커 크기와 색이 저항 (색 막대 18–34 mΩ) · 모양은 양끝이 높은 U 자 (§2-h).

**IR 보정의 효과 (Fig. 2).** `[인쇄]`:
- V–Q (2a): 첫 사이클 평균 +13.2 mV (중앙 +12.0) · 위 10 % 용량 +20.1 · 아래 10 % +11.4; 마지막 평균 +16.6 (중앙 +15.4) ·
  위 +26.9 · 아래 +17.0 — "These gradients indicate that R_Ω (and any very-fast interfacial component) increases both with aging
  and near the high-SOC end."
- dV/dQ–Q (2b): 보정 ↔ 원본 RMSE 1.6 × 10⁻⁵ (첫) · 2.1 × 10⁻⁵ V (mAh)⁻¹ (끝) · 중앙 절대 차 (5–6) × 10⁻⁶ · IQR −9.1 % · −6.8 %.
- dQ/dV–V (2c): 넓이 (용량) 보존 · |dQ/dV| 무게중심 +12.9 / +16.2 mV · 고 V 골 (∼4.03–4.18 V) +18.0 / +24.8 · 중 V 골
  (∼3.35–3.65 V) +18.7 / +10.4 · 저 V 골 (∼3.05–3.25 V) +19.3 / −4.2 ("small, inconsistent change in the last case").
- 결론 `[인쇄]`: "removing the instantaneous IR largely translates the low-rate curve without materially altering its
  thermodynamic shape."
- `[도표]` 2a 첫 곡선 방전 끝 ≈4500 mAh · 끝 곡선 ≈4050 mAh (≈2.65 V) · 점선 (원본) 이 실선 (보정) 아래.
- `[해석]` dV/dQ 가 거의 안 변하는데 모드가 움직인다는 것은 이 DMA 에서 수직 이동이 **식 (12) 의 전압 항**으로 들어간다는 뜻이다
  — 순수 dV/dQ 목적은 균일 이동에 1 차로 둔감하다 (REIL 의 f3 · f4 와 관련, §15-3).

**P45B 저항 (Fig. 3).** `[인쇄]` ≈30 · 50 · 70 % SoC × RPT 넷 (SoH ≈1.00 · 0.98 · 0.96 · 0.93) 에서 "low and tightly clustered at
23–26 mΩ at 25 °C, with only marginal drift with ageing and weak SoC curvature" → "well suited for isolating hysteresis effects
without confounding polarization artifacts". `[도표]` 처리량 ≈0 · 215 · 430 · 850 Ah (DMA 의 앞 네 RPT 와 같은 자리) · SoC 축
눈금 0.30–0.70 · 점마다 한 값 (충 · 방전 펄스 방향 구분 없음).

**P45B 이력 (Fig. 4).** `[인쇄]` 4a: 충전 (점선) 이 방전 (실선) 위 · 충전 시작이 2.5 V 위 (CV 방전이 없어 0 이 아닌 초기 SoC) ·
"Separation is smallest near mid-SoC and larger toward both ends". 4b 띠 합: 0–30 % **13.406 → 7.374** V·%SoC (Δ −6.032,
−45 %) · 80–100 % **22.759 → 23.474** (Δ +0.715, +3 %, 증가는 ∼90 % 위) · 전체 **47.073 → 47.427** (Δ +0.353, +0.7 %) ·
U 자 유지. 저자 해석: 저 SOC 는 Si 탈리튬화의 음극 열역학 이력이 약해지고, 고 SOC 는 dV/dQ 가 가파른 곳이라 작은 동역학 · 수송
벌점 (SEI 성장 · 표면 손실 · 전해질/기공 변화) 이 큰 전압 간격으로 보인다 → "nearly conserved total hysteresis with
age-dependent reweighting". `[도표]` 4a 간격 ≈60–70 mV (중간 SOC) · 막대 판독과 본문 대조는 §2-j · §2-k (그림이 '−45 %' 를
받치지 않고 4a ↔ 4b 크기가 맞지 않는다).

## 7. 결과 §3.2 — IR 이 DMA 에 주는 편향 (M50T · Fig. 5)

- 설계 `[인쇄]`: 옴 항만 보정 — "the sole component that is rate-proportional and path-independent across our tests" · 동적
  (전하이동 · 농도) 과전압은 이력 · 율 · 온도 의존이고 GITT/펄스의 구배는 pOCV 와 같지 않아 "attempting to “remove” them would
  import path dependence".
- 결과 `[인쇄]`: SoH 는 모든 RPT 에서 불변 ("capacity is taken from low-rate throughput") · ε(LAM_PE) −0.24 % (RPT-1) → −8.80 %
  (RPT-6), 중앙 ≈−5.12 % · ε(LAM_NE) +13.77 → +3.64 %, 중앙 ≈+9.38 % · 흑연 중앙 ≈+17.68 % · Si 중앙 ≈−6.44 % · LLI 중앙
  ≈−3.07 % (수열 −0.37 → −5.43 %).
- 기전 서술 `[인쇄, 요약]`: `R_Ω` 가 고 SOC 에서 크고 노화로 커져 방전 pOCV 꼭대기가 가장 많이 들린다 → 양극 pOCP 가 거기서
  가팔라 최적화기가 PE 배율로 흡수 (§2-c 의 규약 문제) → 미보정은 PE 손실 과소 · 흑연은 긴 계단 평탄부라 균일한 IR 처짐이
  "the plateau voltage appears “too low” at a given SOC" 로 보여 음극 과배율 → 흑연 LAM · Si 는 "the steep NE segment near the
  top of discharge" 에 있어 처짐이 가파름을 숨겨 Si 배율이 덜 필요 → Si-LAM 과소 · LLI 는 겹침으로 정해지는데 방전 곡선을
  누르면 창 경계에서 겹침이 커지므로 IR 을 빼면 LLI 가 오른다. 요약 `[인쇄]` "phantom LAM_Gr, with concomitant
  under-diagnosis of PE and Si losses and suppression of LLI" · "Although IR-corrected DMA remains a proxy (residual kinetic
  polarization at C/10–C/20 persists), it is unequivocally closer to the thermodynamic picture than raw pOCV".

`[도표]` Fig. 5 판독 (RPT ≈0 · 700 · 1400 · 2050 · 2700 · 3350 · 4000 Ah · SoH 100 · 96 · 94 · 93 · 91 · 90 · 88 %, 두 곡선 같음):

| 모드 (%) | IR 보정 (주황 실선) | 원본 (파랑 점선) | EOL 절대 차 | 상대 오차 막대 RPT-1 → 6 |
|---|---|---|---|---|
| LAM_PE | 0 · 4.1 · 6.3 · 7.7 · 9.45 · 10.8 · 12.05 | 0 · 4.1 · 6.05 · 7.4 · 8.9 · 10.05 · 11.0 | ≈−1.0 %p | −0.25 · −3.5 · −4.4 · −5.8 · −6.6 · −8.8 % |
| LLI | 0 · 4.2 · 6.6 · 8.15 · 10.0 · 11.35 · 11.85 | 0 · 4.2 · 6.5 · 7.95 · 9.6 · 10.8 · 11.2 | ≈−0.65 %p | −0.4 · −1.8 · −2.7 · −3.5 · −4.7 · −5.4 % |
| LAM_NE 총 | 0 · 4.4 · 5.95 · 7.9 · 9.8 · 11.25 · 12.4 | 0 · 4.95 · 6.65 · 8.75 · 10.55 · 11.95 · 12.8 | ≈+0.4 %p | +13.8 · +12.1 · +10.5 · +8.1 · +6.2 · +3.6 % |
| LAM_Gr | 0 · 1.5 · 2.9 · 4.5 · 6.0 · 7.5 · 9.0 | 0 · 1.8 · 3.55 · 5.4 · 6.95 · 8.5 · 10.2 | ≈+1.2 %p | (RPT-1 막대 없음) · +22.3 · +19.8 · +15.3 · +13.5 · +13.0 % |
| LAM_Si | 0 · 17.0 · 29.5 · 35.5 · 40.0 · 43.2 · 45.0 | 0 · 16.3 · 27.9 · 33.6 · 37.1 · 39.7 · 41.4 | ≈−3.6 %p | −3.8 · −5.3 · −5.6 · −7.6 · −7.9 · −8.0 % |

- `[재현]` 판독값의 blend 역산 신품 Si 몫 φ₀ ≈0.10–0.12 (RPT-2–6, 보정 곡선) · RPT-1 만 ≈0.19 (작은 차의 판독 오차가 큰 자리).
- `[해석]` Si-LAM 이 첫 RPT (≈700 Ah · SoH ≈96 %) 에 이미 ≈17 % 다 — 'Si 가 음극 열화를 몰고 간다' 는 서사의 숫자이지만 독립
  측정 (해체 · 반쪽전지) 으로 확인된 것이 아니다.

## 8. 결과 §3.3–3.4 — 창 편향 (P45B · Fig. 6)

- §3.3 틀 `[인쇄]`: 이력은 음극 (주로 Si) 의 고유 열역학 성질 · 양극과 흑연의 이력은 "comparatively minor" · 편향을 정하는
  실험 선택 둘 = 창 · 가지 → (a) 창을 맞춰 경계 효과를 떼고 (b) 그 창에서 가지 편향을 잰다.
- §3.4 설계 `[인쇄]`: 같은 방전 pOCV · 같은 적합 설정 · 같은 기준 곡선으로 2.5–4.2 V ↔ 3.0–4.2 V (하한만 다름).
- 결과 `[인쇄]` (EOL = RPT-6 · 1982.5 Ah, 괄호는 RPT-1):

| 양 | 2.5–4.2 V | 3.0–4.2 V | 차 (3.0 − 2.5) | 모드로 읽으면 |
|---|---|---|---|---|
| SoH | 80.57 % | 83.47 % | +2.90 pp (≈+3.6 % 상대) (+0.75) | 더 건강해 보임 |
| Q_NE | 90.25 % | 96.04 % | +5.80 pp (+2.39) | LAM_NE −5.8 pp |
| Q_Si | 59.29 % | 72.91 % | +13.61 pp (+2.23) | Si-LAM −13.6 pp |
| Q_Gr | 99.27 % | 97.95 % | −1.32 pp | 흑연 LAM +1.32 pp ("≈1.8× the full-window graphite loss") |
| Q_PE | 95.40 % | 97.65 % | +2.25 pp (+0.51) | LAM_PE −2.25 pp (≈−49 % 상대) |
| Q_LI | 80.53 % | 86.25 % | +5.72 pp (+1.00) | LLI −5.72 pp (≈−29 %) |

- 저자 해석 `[인쇄]`: 잘린 2.5–3.0 V 띠가 "precisely where the Si-dominated degradation signature resides (deep delithiation under
  stress, isolation and pore/SEI growth)" · Si 지렛대가 빠지면 남은 중간 SOC 곡률을 흑연 배율로 맞춘다 · 창 경계에서 pOCP 겹침이
  커져 양극 · 재고 벌점이 준다 · "boundary selection is a first-order source of diagnostic bias" · "Because these shifts arise
  solely from the voltage span, not from kinetics or noise, all subsequent charge–discharge hysteresis comparisons … are performed
  on the harmonized 3.0–4.2 V window".

`[도표]` Fig. 6 궤적 (RPT ≈0 · 215 · 430 · 850 · 1250 · 1630 · 1982.5 Ah; 각 칸 "2.5–4.2 / 3.0–4.2", EOL 은 본문 값):

| 모드 (%) | 궤적 |
|---|---|
| SoH | 100/100 · 97.8/98.6 · 95.2/96.0 · 91.6/93.2 · 88.0/90.2 · 84.4/87.0 · 80.57/83.47 |
| LAM_PE | 0/0 · 1.0/0.5 · 1.1/0.85 · 1.4/0.9 · 2.8/1.0 · 3.1/1.5 · 4.60/2.35 |
| LLI | 0/0 · 2.4/1.4 · 5.2/1.6 · 8.5/4.5 · 12.5/7.3 · 15.7/9.9 · 19.47/13.75 |
| LAM_NE | 0/0 · 3.05/0.7 · 5.4/0.95 · 6.75/2.2 · 8.0/3.05 · 8.35/3.5 · 9.75/3.96 |
| LAM_Gr | 0/0 · 3.3/3.7 · 5.3/6.05 · 4.75/6.2 · 3.45/5.6 · 1.4/2.8 · 0.73/2.05 |
| LAM_Si | 0/0 · 2.3/0 · 5.6/0 · 13.4/4.1 · 23.6/10.3 · 32.2/18.1 · 40.71/27.09 |

- **흑연 LAM 이 두 창 모두 비단조**다 — 전체 창 ≈5.3 % (≈430 Ah) → 0.73 % (EOL), 잘린 창 ≈6.2 % (≈850 Ah) → 2.05 % `[도표]`.
  원문은 이 '회복' 을 언급하지 않는다 (EOL 차이만 쓴다).
- 잘린 창의 Si-LAM 이 ≈215 · 430 Ah 에서 정확히 0 으로 보인다 `[도표]` — 경계 (`Q_Si ≤ 1`) 일 수 있으나 같은 창 충전 가지에는
  음수가 나오므로 (§9) 설명되지 않는다.
- `[해석]` (1) "not from kinetics" 는 주장이다 — C/20 방전의 저전압 꼬리는 pOCV 에서 확산 분극이 가장 큰 곳이고, P45B 의 IR 보정
  여부도 적혀 있지 않다 (§1-7). (2) "잘린 창이 과소 보고한다" 는 전체 창이 참에 더 가깝다는 가정 위에 있다. (3) 창이 달라지면
  식 (10) 의 모드가 '창 안 접근 용량의 비' 로 정의가 바뀐다 — 창 효과의 일부는 편향이 아니라 **다른 양을 잰 것**이다.

## 9. 결과 §3.5 — 가지 (이력) 편향 (P45B · Fig. 7)

- 설계 `[인쇄]`: 두 가지 모두 같은 3.0–4.2 V 창 → 차이는 "branch-dependent thermodynamics of the Gr/Si negative electrode (NE),
  with only minor residual kinetic contributions at the low rates used". 두 서명: 같은 통과 전하에서 충전 가지가 더 높은 전압 ·
  양극 꼭대기가 가팔라 작은 수직 차가 배율 · 겹침을 크게 바꾼다.
- 결과 `[인쇄]`: EOL (1982.5 Ah) LAM_PE 충전 쪽 +3.42 pp · LLI 충전 쪽 +5.36 pp · 모든 RPT 에서 같은 방향 · 노화로 커짐 ·
  Dis−Chg Si-LAM +1.63 pp (첫 RPT) → +14.38 pp (EOL) · 흑연 Dis−Chg +2.8–6.2 pp (중간) · +3.9 pp (EOL) · LAM_NE 방전 쪽
  ∼0.4–1.9 pp 높음 (중간 이후) · SoH 방전 쪽 +0.7–2.0 pp (이른 RPT 하나 −0.45 pp) — "because the elevated charge voltage reaches
  the upper cutoff with less area under the curve". §4 의 요약: 충전이 LAM_PE 를 ≈2–3.5 pp · LLI 를 ≈1.4–5.8 pp 부풀린다.
- 기전 `[인쇄, 요약 — 부호 문제는 §2-a · §2-b]`: 충전 곡선이 들려 있으니 (i) 4.2 V 근처 양극 곡률을 위해 양극 배율 ↑ → LAM_PE ↑,
  (ii) σ 형 수평 이동으로 겹침 ↓ → LLI ↑, (iii) 중간 SOC 모양을 지키려 음극 안 재가중 → 충전에서 Si ↓ · 흑연에 작은 잔여;
  노화로 Si 지렛대가 짧아지면 충전 쪽 Si 억제 유인이 커져 ΔSi-LAM 이 자란다; 흑연 역할은 일시적이고 충전 쪽 흑연 LAM 이 말기에
  "can even dip slightly negative".
- 음수 LAM `[인쇄]`: "these are not physical capacity gains … the optimizer can achieve the required curvature in 3.0–4.2 V by
  assigning an effective Si retention in that span slightly above the fresh normalization, i.e., Q_Si^charge > 100 % … Two
  consistency checks hold simultaneously: the total NE retention remains plausible and the blend rule … stays within numerical
  tolerance. The “negative” values should therefore be interpreted as under/over-compensation inside the NE decomposition driven
  by hysteresis, not as material rejuvenation."
- 결론 `[인쇄]`: "discharge is closer to equilibrium and consistently recovers the Si-dominated NE loss with smaller cathode and
  inventory penalties" → 정량은 방전, 충전은 "qualitative cross-checks or … where hysteresis itself is the subject of study".

`[도표]` Fig. 7 궤적 (같은 RPT; 각 칸 "방전 / 충전"):

| 모드 (%) | 궤적 |
|---|---|
| SoH | 100/100 · 98.6/97.8 · 96.0/96.6 · 93.1/92.0 · 90.2/89.0 · 87.0/85.8 · 83.5/81.3 |
| LAM_PE | 0/0 · 0.5/2.75 · 0.85/3.5 · 0.92/4.2 · 1.0/4.6 · 1.45/4.85 · 2.35/5.75 |
| LLI | 0/0 · 1.45/2.8 · 1.9/4.7 · 4.5/10.2 · 7.4/13.0 · 9.9/15.7 · 13.7/19.1 |
| LAM_NE | 0/0 · 0.68/0.25 · 0.97/0.57 · 2.2/0.67 · 3.08/1.2 · 3.5/1.85 · 3.95/2.23 |
| LAM_Gr | 0/0 · 3.7/0.93 · 5.85/1.25 · 6.2/−0.05 · 5.6/−0.15 · 2.75/−0.88 · 2.05/−1.85 |
| LAM_Si | 0/0 · 0.05/−1.0 · 0.05/−0.8 · 4.2/2.4 · 10.3/4.8 · 18.2/8.9 · 27.0/12.7 |

- Fig. 7 의 방전 값은 Fig. 6 의 3.0–4.2 V 값과 판독 오차 안에서 같다 (같은 자료 · 같은 창) `[도표]`.
- `[해석]` (1) **두 가지 모두 RPT-0 에서 모든 모드가 0** — 가지마다 자기 신품 적합으로 나눴다. 그러면 '이력 편향' 은 정적 이력이
  아니라 **가지 차이의 노화 의존분**이고, 정적 차이는 가지별 신품 기준 (Si 몫 ≈0.3 ↔ ≈0.23, §2-m) 으로 흡수된다.
  (2) 충전 LAM_PE 가 첫 RPT 에 0 → ≈2.75 % 로 뛴다 (방전 0 → ≈0.5 %) — EOL 가지 차 (3.42 pp) 의 대부분이 첫 RPT 에 이미 있다.
  매끈한 이력 변화보다 적합이 다른 해로 옮긴 모양과도 맞는다 (잔차 · 다중 시작이 없어 가를 수 없다).
  (3) 구성 교차: 충전 (3.0–4.2 V) 의 EOL LLI ≈19.1 % 는 전체 창 방전의 19.47 % 와 거의 같고, 충전 SoH ≈81.3 % 도 전체 창 방전
  80.57 % 에 가깝다. 저자가 가장 완전하다고 본 구성 (전체 창 방전) 에 LLI · SoH 로 더 가까운 것은 권고 구성 (공통 창 방전 13.75 % ·
  83.47 %) 이 아니라 충전 가지다. '충전이 LLI 를 부풀린다' 는 그 자체로 5.72 pp 과소 보고하는 구성 (Fig. 6) 에 견준 말이다.
  (4) "discharge is closer to equilibrium" 의 근거는 Fig. 8 Cause B 의 인용 (Berg et al., 2025; Beiranvand et al. — 목록 밖) 뿐이다.
  이력이 있는 Si 에서 어느 가지도 '평형' 이 아니고, 물음은 **기준 곡선과 측정 가지가 일치하는가**다.

## 10. 논의 §4 — 측정 모형 · 인과 사슬 (Fig. 8) · 전류 분배 (Fig. 9)

- 측정 모형 `[인쇄]`: `U_meas(Q) = U_PE^(b)(z_PE) − U_NE^(b)(z_NE) + η_kin(z, I) + I·R_Ω` ("branch-specific pseudo-OCPs U^(b)
  and an instantaneous ohmic term") · DMA 는 `(ν_NE, ν_PE, σ_NE, σ_PE)` (와 `φ_Si`) 로 `U_PE^(b) − U_NE^(b)` 를 `U_meas` 에 맞춘다 ·
  옴은 1 차로 수직 이동 (방전 음, 충전 양) · 양극 꼭대기 ∂V/∂Q 가 커 "even a modest |I|R_Ω (we observe +13–20 mV early, +16–27 mV
  late after correction) disproportionately alters the fitted ν_PE and pOCP overlap" · "the tiny residual in dV/dQ after IR removal
  confirms that dynamic polarization is small at C/10–C/20 [Kirkaldy et al., 2024] [2]" · "correcting only R_Ω (SOC) measured
  independently—rather than folding history-dependent diffusion overpotentials into the thermodynamic fit—preserves identifiability
  and aligns with DMA best practice [2, 5]".
- `[해석]` 두 문장은 근거가 서지 않는다: dV/dQ 는 **어떤 균일 이동에도** 불변이라 (Fig. 2b 가 그것을 보였다) 남은 동적 분극의 크기를
  재지 못한다; "preserves identifiability" 는 재지 않은 주장이다.
- 이력 문단 `[인쇄]`: Gr/Si 의 이력은 "intrinsically thermodynamic and branch-dependent" · 같은 3.0–4.2 V 창이므로 "the differences
  are therefore hysteresis bias rather than boundary effects" · 충전이 LAM_PE ≈2–3.5 pp · LLI ≈1.4–5.8 pp 부풀림 · Si Dis−Chg
  +1.6 → +14.4 pp · 흑연 +2.8–6.2 pp (중간) · 음수 구성요소 LAM 은 blend 안의 과 · 소 보상 [Karger et al., 2023].

**Fig. 8** (그림 안 글자 — `[인쇄]` 전사):
- Cause A: "Si lithiation on charge → compressive stress. By (2), compression raises the anode potential U_NE on charge (tens–hundreds
  mV GPa⁻¹ scale in Si thin films/particles) → charge pOCV sits above the elastic/equilibrium baseline; discharge relaxes toward
  equilibrium. [Kim et al., 2021; Berg et al., 2025]"
- Cause B: "Thermodynamic hysteresis is direction-asymmetric. Calorimetry/OCV reconstructions: Ueq lies closer to discharge, and most
  hysteresis heat is on charge (stronger for Gr–Si than Gr-only). [Berg et al., 2025; Beiranvand et al.]"
- Effect 1 (partitioning): "At the same SOC/voltage, more Li goes into Si on charge than on discharge (blend is Si-heavier on charge):
  +10–12 pp on average, peaks ~27–30 pp. [exp observation]"
- Effect 2 (top-of-charge penalty → apparent PE-LAM): "With (1) and (3), a positive ΔU_NE forces the cathode to a higher potential
  sooner, i.e., you hit 4.2 V earlier → less Q_PE usable in 4.2→3.0 V: • At 600 cycles: ν_PE charge 0.788 vs discharge 0.764 ⇒
  Q_PE^chg (5.71 Ah) < Q_PE^dchg (5.89 Ah) (~3 %) ⇒ LAM_PE^chg (7.0 %) > LAM_PE^dchg (0.8 %) (790 % overestimation in charge)"
- Effect 3 (whole-window overlap → apparent LLI): "The same uplift acts across 4.2→3.0 V, shrinking the overlap (4): • At 600 cycles:
  ΔQ_LI^chg (0.8 Ah) > ΔQ_Li^dchg (0.5 Ah) ⇒ LLI^chg (18.8 %) > LLI^dchg (12.3 %) (53 % overestimation in charge)"
- `[재현]` Effect 2 의 두 쌍은 `ν_PE × Q_PE` = 0.788 × 5.71 = 4.499 · 0.764 × 5.89 = 4.500 Ah → 식 (8) 그대로 `Q_FC` ≈4.50 Ah
  (3.0–4.2 V 창의 P45B 용량으로 읽힌다). LAM_PE 7.0 · 0.8 % 를 되풀면 신품 `Q_PE` 가 충전 ≈6.14 · 방전 ≈5.94 Ah, LLI 18.8 ·
  12.3 % 는 신품 `Q_LI` ≈4.26 · ≈4.07 Ah — **가지마다 다른 신품 기준**을 함의한다 (§1-6). 불일치는 §2-l.

**Fig. 9** `[도표]` 제목 "Current Fraction (φ_Si = 0.2)" · x `SOC_NE` 0–1 · y 순간 전류 분율. `SOC_NE` ≈0.1–0.4 와 ≈0.55–0.7 에서
`I_gr` ≈0.97–1 (두 가지) · ≈0.46 에 Si '혹' (`I_si` ≈0.22, 두 가지 — 그 자리 `I_gr` ≈0.77) · ≈0.75–0.87 에서 방전 `I_si`
≈0.25–0.32 의 엽 여럿 ↔ 충전 ≈0.03–0.08 · ≈0.94–0.99 에서 방전 ≈0.22–0.26 ↔ 충전이 ≈0.4–0.9 로 급등 · `SOC_NE` → 0 에서 방전
`I_si` 0.5 시작. `[인쇄]` 본문: "derived from the blend templates and local slopes" · ≈10–70 % NE-SOC 에서 흑연 >90 % (`[도표]`
혹 자리에서는 ≈0.77) · 방전은 Si 몫이 넓고 매끈 (∼10–30 %) · 충전은 억제되고 급격 → 방전이 Si 곡률을 지켜 Si-LAM ↑ · PE-LAM/LLI ↓.
`[해석]` 측정이 아니라 고정 `φ_Si` = 0.2 의 기준 곡선 계산이고, 가지별 곡선이 다르다는 것은 가지별 기준이 있었다는 뜻이다 (§1-1).

실천 두 줄 `[인쇄]`: IR 보정 pOCV + 공통 창의 방전 가지로 정량 · 충전은 정성 교차검사 / 충전 가지의 음수 구성요소 LAM 은 할당
인공물로 표시하고 "blend-consistency residuals and, if space allows, a constrained re-fit sensitivity [2] [Karger et al., 2023]" 를
붙인다.

## 11. 결론 §5 (p.10–11)

`[인쇄]` "Degradation-mode analysis (DMA) only reports the physics that the voltage trace allows it to see." · 옴 강하 = "a near-rigid
vertical translator of the pOCV" → 양극 꼭대기가 가팔라 미보정이면 PE-LAM · LLI 과소 · Gr/Si 음극은 "intrinsically hysteretic"
→ 같은 창 적합에서 충전이 PE-LAM · LLI 를 부풀리고 Si-LAM 을 누른다 (때로 음수) · 전류 분배가 기원을 보인다 · 창이 Si 민감 저전압
꼬리를 넣거나 뺀다. 처방: "correct only the ohmic term prior to fitting, perform quantitative DMA on the discharge branch within a
harmonized voltage window, and treat charge-branch component LAMs as allocation artefacts when negative or anomalously small." ·
"Crux: … the most faithful configuration is IR-corrected, discharge-branch DMA on a common window".

## 12. 자료 · 코드 · 저자 기여 · 참고문헌

- 자료 · 코드 `[인쇄]`: Zenodo 10637534 · "The degradation mode analysis (DMA) tools used in this work are available as open-source
  software in the PyProBE repository". 이해충돌 없음 선언.
- CRediT `[인쇄]`: N (구상 · 방법 · 검증 · 분석 · 조사 · 자료 · 초고 · 검토 · 시각화) · Leal De Souza (검증 · 검토 · 시각화) ·
  Folkson (조사 · 자료) · Offer · Marinescu (구상 · 방법 · 검증 · 분석 · 자원 · 검토 · 시각화 · 지도 · 관리 · 자금). **Holland 없음.**
- 번호 참고문헌 16: [1] Barai et al. 2019 *PECS* 72 · [2] Birkl et al. 2017 *JPS* 341 · [3] Bloom et al. 2005 *JPS* 139 · [4] Dubarry &
  Anseán 2022 *Front. Energy Res.* 10 · [5] Dubarry, Truchot, Liaw 2012 *JPS* 219 · [6] Edge et al. 2021 *PCCP* 23 · [7] Gao et al.
  2017 *Nano Lett.* 17 · [8] Jahn et al. 2024 *Commun. Eng.* 3 · [9] Kargl et al. 2022 *JPS* 548 · [10] Mercer et al. 2021 *JMCA* 9 ·
  [11] Olson et al. 2023 *Chem. Mater.* 35 · [12] Oney et al. 2025 *Adv. Energy Mater.* 15 · [13] Ovejas & Cuadras 2019 *Sci. Rep.* 9 ·
  [14] Schott et al. 2017 *JPCC* 121 · [15] Weng, Siegel, Stefanopoulou 2023 *Front. Energy Res.* 11 · [16] Yang et al. 2022 *JMCA* 10.
- 목록 밖 인용 다섯 — §1-13.
- `[해석]` 이 위키와 겹치는 서지: [2] = [[birkl-ocv-degradation-diagnostic]] 원전 · [5] = [[dubarry-mechanistic-mode-synthesis]] 원전 ·
  [12] = `raw/papers/oney2025_dead-slow-overworked-graphite-operando-microxrd.md` · [15] = [[ampworks]] 가 자기 방법의 문헌으로 적은
  편과 같은 서지 (Weng · Siegel · Stefanopoulou 2023). [1] Barai 2019 는 이 위키의 Barai 2018 (내부 저항 측정 시간척도) 과 다른 편이다.

---

## 13. 비판적 평가 `[해석]`

**강점.**
- 실제로 덜 다뤄진 문제에 이름을 붙였다 — DMA 는 OCV 가 아니라 pOCV 를 맞추고, 비열화 수직 성분은 모드 매개변수로 사영된다.
- 옴 성분 (≈50 ms) 과 동적 성분을 가르고, 이력 의존 과전압을 **빼지 않겠다**는 원칙을 명시한다. 이력을 '빼는' 대신 '관리' 대상으로 둔다.
- dV/dQ 불변 (Fig. 2b) 으로 "보정은 이동이다" 를 보였다. 자료 (Zenodo) 와 도구 (PyProBE) 를 공개한다고 적었다.

**약점.**
1. **참값이 없다** — '유령' 은 검증 안 된 기준 구성에 대한 차이로 정의된다. 그리고 그 기준 구성은 세 실험 모두에서 Si-LAM 을 가장 크게
   내는 쪽이다 (§14) — 기준이 틀렸으면 유령의 방향이 뒤집힌다.
2. **불확실성 · 식별성 분석 0** — 잔차 · 매개변수 값 · 다중 시작 · 상관 · 반복 셀 · 오차 막대 없음 (§17).
3. **기전 서술의 내부 불일치** (§2-a · b · c) — 가지 ↔ 전극 과정, 식 (3) 과 반대인 부호, `ν` 규약.
4. **셋을 한 셀에서 보지 않았다** — IR 은 M50T, 창 · 가지는 P45B. 물음의 "together" 는 시험되지 않았다.
5. **P45B 의 IR 보정 여부 미기재 · 저항 자료가 SoH 0.93 에서 끊김** (§1-7) — 가지 차의 ≈10–12 mV 가 IR 일 수 있다.
6. **IR 보정 크기가 측정 범위 밖 외삽에 기댄다** (§1-8) — 기전의 핵심 (꼭대기 들림) 이 바로 그 구간이다.
7. **권고끼리 충돌** (§2-n) · 권고 구성에서 blend 산술이 성립하지 않고 흑연 LAM 이 비단조 (§2-m · §8).
8. **상대 오차** 는 초기 RPT 의 작은 LAM 에서 커진다 · 초록이 상대 (%) 와 절대 (pp) 를 나란히 써 크기 비교를 오도할 수 있다.
9. **인용 다섯이 목록 밖** — DMA 틀 (Karger) · M50T 자료 (Kirkaldy) 의 원전이 서지로 확인되지 않는다.
10. 그림 ↔ 본문 수치 불일치 (§2-j · k · l) — 이력 띠 합의 헤드라인 (−45 %) 과 Fig. 8 예시 수치는 인용하지 않는다.

## 14. 우리 축 (★) 으로 다시 읽기

- **열화 모드 분해**: 반쪽전지 pOCP 맞춤 (DMA) + Gr/Si blend (`φ_Si` 자유) → LLI · LAM_PE · LAM_NE + LAM_Gr · LAM_Si. 라벨의 출처는
  적합 자체 · 불확실성 표기 0 · 식별 가능성 진단 0.
- **관측 · feature**: 저율 pOCV V–Q (dQ/dV · dV/dQ 는 그림과 식 12 의 기울기 항) · 이력 지표 `A = ∫|ΔV|ds`. 귀속: 옴 (열역학 아님 ·
  측정 수준) · 이력 (열역학 · 주로 Si) · 창 (측정 설계).
- **모드별 부호 구조** (`[인쇄]` 부호 · 원문 기준 구성 대비):

| 섭동 (← 원문의 기준) | LAM_PE | LLI | LAM_NE | LAM_Gr | LAM_Si | 셀 |
|---|---|---|---|---|---|---|
| IR 미보정 (← 보정) | ↓ (중앙 −5.12 % 상대) | ↓ (−3.07 %) | ↑ (+9.38 %) | ↑ (+17.68 %) | ↓ (−6.44 %) | M50T |
| 충전 가지 (← 방전, 3.0–4.2 V) | ↑ (+3.42 pp) | ↑ (+5.36 pp) | ↓ (0.4–1.9 pp) | ↓ (2.8–6.2 · EOL 3.9 pp) | ↓ (14.38 pp) | P45B |
| 하한 3.0 V (← 2.5 V, 방전) | ↓ (2.25 pp) | ↓ (5.72 pp) | ↓ (5.80 pp) | ↑ (1.32 pp) | ↓ (13.61 pp) | P45B |

  `[해석]` 세 가지가 보인다. (1) **LAM_PE 와 LLI 가 세 섭동 모두 같은 방향**으로 움직인다 — 비열화 섭동이 (`ν_PE`, `σ`) 부분공간의
  한 방향으로 묶여 흡수된다는 기전 서술과 맞고, 우리가 재는 약방향 ([[fitting-degeneracy]]) 과 같은 꼴의 물음이다.
  (2) **Si-LAM 은 셋 모두 ↓** — 원문이 '기준' 으로 고른 구성이 매번 Si-LAM 최대 구성이다. (3) **PE − NE 격차** 가 비열화 선택만으로
  움직인다: IR ≈−1.45 %p (M50T EOL `[도표]`) · 가지 ≈+5.1 %p (`[도표]`) · 창 +3.55 %p (`[재현]` 본문 Q 값) — 우리 판정선 (2 %p) 과
  같은 자릿수다.
- **모델**: 물리 모델 (PyBaMM/P2D/SPM) 없음 — 반쪽전지 기준 곡선 맞춤 (Karger et al. 틀 · PyProBE 도구).
- **ML**: 해당 없음.
- **데이터셋**: 21700 두 종 · 종류당 1 셀로 보임 · M50T RPT 7 (≈4000 Ah · SoH ≈88 %) · P45B RPT 7 (1982.5 Ah · 창 안 SoH ≈81–84 %) ·
  25 °C. 노화 · RPT 프로토콜은 §5-1.

## 15. 우리 프로젝트와의 접점 `[해석]`

### 15-1. degradation-degeneracy — `docs/22p_gap` 의 OCP 바이어스 실험

- **같은 섭동이다.** 우리 `ocpbias` 는 `pe_offset_mv` 만큼 **기준** PE OCP 를 올린다 (`degradation-degeneracy/src/halfcell.py` 144–148
  행 — 읽기만). 식 (3) 에서 `U_PE + δ` 로 `U_meas` 를 맞추는 것은 `U_PE` 로 `U_meas − δ` 를 맞추는 것과 같으므로, `pe_offset_mv = +δ`
  다리는 **SOC 무관 · 방전 IR 미보정 δ** 와 수학적으로 같다 (다리별 부호는 정본 파일에서 확인할 것). 정본: `degradation-degeneracy/
  docs/09_22P_GAP.md` §7.10 · `docs/22p_gap/bias_pe{1,1p5,2,5,10}mv.txt` (수치는 옮기지 않는다).
- **다른 점 둘**: (i) 이 논문의 IR 은 SOC 의존 (위 10 % ↔ 아래 10 % 차 8.7 · 9.9 mV `[재현]`) 이고 우리 다리는 균일; (ii) 우리 적합은
  음극 Si 몫을 고정하므로 이 논문 M50T 결과를 지배하는 흑연 ↔ Si 재배분이 원리적으로 나올 수 없다. 크기도 이 논문 (≈11–27 mV) 이
  우리 다리 이름의 범위 (≤10 mV) 위다.
- **우리가 공급할 수 있는 것**: 참값 대비 오차. 이 논문의 ε 는 보정 적합 대비이고 참값이 없다. 실행 없이 할 수 있는 대조 — §7.10 표의
  ①' 격차 bias (LAM_PE 오차 − LAM_NE 오차) **부호**가 이 논문의 방향 (미보정 → LAM_PE ↓ · LAM_NE ↑ → 격차 음) 과 같은가. 먼저
  고정할 것: '오차' 의 부호 규약 · 지표 차이 (보정 대비 상대 ↔ 참값 대비 격차) · 우리 0 mV 다리 자체가 0.05 C 동적 곡선이라 이미
  '미보정 pOCV' 라는 점 (`degradation-degeneracy/docs/RESULTS.md` "이 결론이 말하지 않는 것" 의 Phase 1j 과전압 서명 — 수치는 거기).
  이 세션은 대조하지 않았다.
- **이 논문이 새로 권하는 시험** (미실행 · 우리 파이프라인 실행이 필요): SOC 의존 (꼭대기 무거운) 오프셋 다리 · `φ_Si` 자유 5 매개
  적합 (참값을 아는 흑연 ↔ Si 재배분) · 충전 가지 + 탈리튬화 기준 (가지 불일치) 적합.
- **우리 truth 의 가지.** `degradation-degeneracy/configs/base.yaml` 15–17 행 `negative: ["single", "current sigmoid"]` — truth 의
  Si 상은 전류 부호로 리튬화 ↔ 탈리튬화 OCP 를 바꾸는 **방향 의존 OCP** 를 갖는다. 적합은 최종 방전 스텝 곡선 + **탈리튬화 가지**
  기준이다 (`src/halfcell.py` 87–106 · 195–199 행; 195–199 행 주석은 두 가지를 섞었을 때 기준 곡선이 망가진 실측을 적어 둔다).
  즉 우리 파이프라인은 **이 논문이 권하는 구성** (방전 가지 · 가지 일치) 위에 있고, 우리가 잰 축퇴는 가지 불일치 · IR 보정 효과를
  **뺀** 하한이다. (위키 [[22p-physics-or-degeneracy]] 2026-09-22 줄의 "우리 PyBaMM truth 는 방향 의존 OCP 를 갖지 않으므로" 는
  이 코드와 어긋난다 — 정정은 그 카드에.)
- **22p 에 대해**: 22p 셀이 Si/Gr blend 이고 맞춤이 `φ_Si` 를 열었다면 (2026-09-21 덱의 코드는 `γ_Si` 를 다섯째 매개변수로 열고
  음수 LAM_Si 궤적을 보였다 — [[halfcell-ocp-shape-invariance]]), 이 논문은 같은 꼴의 맞춤에서 **가지 · 창 · IR 선택만으로**
  LAM_PE · LLI 가 1–6 pp, Si-LAM 이 최대 14 pp, PE − NE 격차가 1.5–5 %p 움직인다는 실셀 크기를 준다. 22p 맞춤의 가지 · 율 · 창이
  무엇이었는지가 그 삼중항을 읽기 위한 선행 조건이 된다.

### 15-2. PyProBE · ampworks · PyDMA — 논문의 IR 보정 ↔ 적합 R offset

- **PyProBE**: 이 논문이 DMA 도구의 소재로 적은 도구 (같은 기관). 논문의 θ (5 · `φ_Si`) 와 목적 (전압 + 기울기 · 내부 가중) 은 이
  위키가 시험한 2.6.0 의 창 4 매개와 다르다 — 판 · 함수 미기재 (§1-14). 이 위키의 합성 truth 시험에서 범위를 5–10 % 자르면 RMSE 는
  내려가며 답이 1–2 %p 움직였는데 ([[pyprobe]]), 이 논문은 같은 '창' 현상을 실셀에서 더 크게 (Si 13.6 pp) 보인다 — 다만 우리
  시험에는 Si 몫 적합이 없었다.
- **ampworks**: 상수 `iR` 를 다섯째 매개변수로 **맞춘다** (`xn0 · xn1 · xp0 · xp1 · iR`, [[ampworks]]). 그 문헌 Weng · Siegel ·
  Stefanopoulou 2023 이 이 논문의 [15] 다. 이 논문은 `iR` 를 맞추지 않는다.
- **PyDMA** (TUM-EES `tum-ees/PyDMA` — 호출자 전달: 직렬저항 R offset 을 선택적으로 맞추는 `allow_resistance_offset`; **코드는 이
  세션에서 보지 않았다**). 이 논문 원문만으로 대조하면 **같은 것이 아니다**:

| 항목 | 이 논문 (측정 R 사전 보정) | 적합 R offset (PyDMA 옵션 · ampworks `iR` · Sun 2025 `R` · Rhyu 2025 `V_shift`) |
|---|---|---|
| R 의 출처 | ≈50 ms 펄스 첫 계단 측정 (식 1) | 곡선 맞춤의 자유 매개변수 |
| SOC 의존 | 보간한 `R_Ω(SOC)` — 본문 값으로 위 10 % ↔ 아래 10 % 끌어올림 차 8.7 · 9.9 mV `[재현]` | 상수 한 값 — 그 SOC 차를 담지 못한다 |
| 담는 성분 | 순간 옴 (+ 아주 빠른 계면) 만 · 느린 성분은 일부러 뺀다 | 수직 잔차 전부 — 옴 · 동역학 · 이력 반폭 · 기준 곡선 오프셋을 구별 없이 |
| 매개변수 수 | θ 5 그대로 (보정은 전처리) | +1 — 원문의 기전 (수직 이동이 `ν_PE` · `σ` 로 흡수된다) 이 맞다면 오프셋 열은 LAM_PE · LLI 열과 부분 공선 → 새 약방향 후보 |
| 원문이 평가했나 | — | **안 했다** (적합 오프셋과 비교 0) |

  그래서 이 논문으로 PyDMA 옵션의 좋고 나쁨을 판정할 수 없다. 시험 설계는 이미 이 위키에 있다 — [[halfcell-window-parametrization-lineage]]
  일곱 번째 축 (Sun 2025) 의 "5×5 `JᵀJ` 최소 특이벡터에 R 성분이 얼마나 실리는가" 를 우리 합성 truth (SOC 의존 오프셋을 넣은 것) 에서
  계산하면 PyDMA 옵션 · ampworks `iR` 에 같이 답한다 (미실행).

### 15-3. REIL 외부 검증으로 옮기면 (LFP/흑연 · C/20 충전 곡선)

- 범위: 이 논문은 NMC811 · 고 Ni NCA ‖ C/SiOx 21700, pOCV C/10 (M50T) · C/20 (P45B), 25 °C, 셀 종류당 1 개다. **LFP 언급 0 · Si
  없는 음극 0 · 코인셀 0.** REIL ([[isu-uconn-lfp-gr-emulated-degradation]]) 은 LFP/흑연 코인셀의 C/20 **충전** 곡선 (≈2.33 → 3.6 V) 을
  그대로 맞춘다.
- **옮겨지는 것 (방향만)**:
  (i) 충전 곡선은 OCV 보다 `I·R` + 이력만큼 위다 (둘 다 충전에서 양). 고정 창이면 상한에 더 일찍 닿아 창 안 용량이 줄고 (Fig. 7a 충전
  SoH ↓) 겉보기 LLI 가 는다 (Fig. 7c). REIL 의 맞춤 LII 가 사실상 충전 용량을 읽는다면 (엔티티 '논문 digest' 절 — LII ≈ 충전 용량
  ÷ 3.10–3.16 mAh), 셀마다 다른 수직 이동은 LII 를 셀마다 다르게 낮춘다.
  (ii) dV/dQ 는 균일 이동에 1 차로 불변이다 (Fig. 2b) → REIL 목적 f3 · f4 (dV/dQ) 는 IR · 균일 이력 이동에 둔감하고, f1 (끝점 전압) ·
  f2 (QV MSE) 가 그것을 짊어진다.
  (iii) 이 논문의 가지 편향은 **완전지 가지 ↔ 반쪽전지 기준 가지의 불일치**에서 온다 (원문은 기준 가지를 적지 않지만 기전이 그 구조).
  REIL 에서 같은 위험의 통제는 이미 P0 의 방향 대조 (부속 C 재검토 RV2C-N3: 완전지 충전 = PE 탈리튬 · NE 리튬화 ↔ 반쪽전지 기준의
  방향) 다. 이 논문은 그 항목이 왜 결과를 좌우하는지의 실셀 크기 (Gr/SiOx: LAM_PE 2–3.5 pp · LLI 1.4–5.8 pp) 를 준다 — LFP/흑연의
  크기는 주지 않는다.
- **옮겨지지 않는 것**: 수치 전부 · Si 고유 이력 · 21700 ↔ 코인셀 · `I·R` 크기 (REIL 셀 저항은 이 논문 밖). 이 논문의 LAM_PE 기전은
  NMC/NCA 의 가파른 꼭대기에 기대는데 LFP 는 양 끝 외에는 평탄해 수직 이동이 다른 매개변수로 흡수될 것이다 (어디로인지는 이 논문이
  말하지 않는다). REIL 셀은 설계상 원판 지름이 달라 `I·R` 이 셀마다 다를 수 있으므로 공통 모드로 상쇄된다고 가정할 근거도 없다.
- 해석 제한의 꼴 (판단은 REIL 문서 쪽 몫): "반쪽전지 기준 가지 · 율 ≠ 완전지 가지 · 율" 과 "충전 IR 미보정" 을 **이름 붙은 편향
  통로**로 적고, 그것이 만드는 차이를 축퇴 증거로 세지 않는다.

### 15-4. 축퇴 · 동등 적합 · 등록 · 가지 · 창 — 이 논문이 다루는 방식

| 축 | 논문이 하는 것 | 하지 않는 것 |
|---|---|---|
| 축퇴 (non-identifiability) | `identifiab*` 1 회 ("preserves identifiability" — IR 측정 보정의 장점으로, 근거 없이) · 음수 구성요소 LAM 을 "under/over-compensation inside the NE decomposition" 이라 부른다 (보상 방향의 산문 진술) | 잔차 · 다중 시작 · 상관 · Hessian · 프로파일 · 신뢰구간 0 · 권한 "constrained re-fit sensitivity" 도 안 함 |
| 동등 적합 | — | 어떤 구성의 잔차도 보고하지 않아 "똑같이 잘 맞는 다른 답" 인지 판정 불가 |
| 등록 (registration) | 초록 · 서론이 유령의 원천으로 명명 ("curve registration" · "re-registering features") · RPT 마다 SOC 를 자기 방전 용량으로 정규화 · 이력은 공통 SOC 격자 (≥600 점) 위에서 비교 | 등록의 정의 · 식 0 · 정규화가 셋째 자유도를 지우는지 ([[np-lip-ocv-reparametrization]]) 논의 0 |
| 가지 선택 | 같은 창에서 두 가지를 맞춰 비교 · 방전 권고 · 충전의 음수 LAM 을 인공물로 표시 · 전류 분배 그림 | DMA 에 가지별 기준을 썼는지 미기재 · 두 가지 동시 적합 (이력 모형) 안 함 · "방전이 평형에 더 가깝다" 는 목록 밖 인용에 의존 |
| 창 선택 | 하한 2.5 ↔ 3.0 V 비교 · 가지 공정 창 규칙 (RPT 마다 겹침) | 창마다 모드의 뜻이 '창 안 접근 용량' 으로 바뀌는 문제 · 창이 RPT 마다 다시 정해지는 문제 · 권고 창 충돌 (§2-n) |

## 16. 그림 — 본 것 · 안 본 것 · 판독 방법

- 크로퍼 (`wiki/tools/extract_figures.py --clean`) 가 9 장을 캡션 기준으로 잘랐다 (`raw/figures/asheruddin2025_phantom-lam-lli-ir-hysteresis-dma/`,
  SI 0). **9 장 모두 Read 로 봤다** — Fig. 1–9. 확대 (스크래치패드에서 잘라 키움 · 저장소 밖): Fig. 1 왼쪽 세 열 (점 세기) · Fig. 4a (가지
  간격) · Fig. 4b (막대) · Fig. 5 (b–f) · Fig. 6 (d–f) · Fig. 7 (a–f). Fig. 8 은 글자 그림이라 전사했다.
- p.4 오른쪽 단 (식 4–12) 과 p.5 오른쪽 단 (§3.2 의 `ν` 서술 · 별표 인쇄) 은 페이지 렌더로 글자를 확인했다 — 텍스트 추출에서 식 (9) 의
  분수 묶음이 사라졌기 때문 (렌더: `(1 − σ_PE)/ν_PE`).
- 본문과 어긋난 그림: Fig. 4b ↔ 본문 '−45 %' · Fig. 4a ↔ 4b · Fig. 8 ↔ Fig. 7 · 9 · Fig. 1 SOC 범위 ↔ 위 10 % 끌어올림 · Fig. 1 ↔ Fig. 5
  처리량–SoH · Fig. 3 축 이름 · Fig. 1 의 U 자 ↔ "toward high SOC" · Fig. 9 의 Si 혹 (`I_gr` ≈0.77) ↔ ">90 %" · Fig. 6/7 의 blend 산술
  (§2).

## 17. 어휘 전수

본문 (참고문헌 앞까지 · NFKC 정규화 · 줄끝 하이픈 이음 · 그림 안 글자 제외, ≈46,000 자): `identifiab*` **1** · `degenera*` 0 ·
`uniqu*` 0 · `non-unique` 0 · `uncertain*` 0 · `error bar` 0 · `confidence` 0 · `multi-start` 0 · `±` 0 · `correlat*` 0 · `replicat*` 0 ·
`standard deviation` 0 · `ground truth` 0 · `truth` 1 ("We do not claim … exact thermodynamic truth") · `sensitiv*` 7 · `constrain*` 2 ·
`registr*` 2 · `artefact/artifact` 7 · `allocat*` 10 · `compensat*` 5 · `phantom` 10 · `hysteres*` 48 · `residual` 9 · `RMSE` 1 (dV/dQ
비교 — 적합 잔차 아님) · `equilibri*` 11 · `LLI` 47 · `LAM` 85 · `PyProBE` 2 · `Karger` 4 · `Kirkaldy` 2 · Supplementary/SI 0.
`[해석]` 이 위키 계보 ([[mode-identifiability-unmeasured-lineage]]) 의 형태로 적으면: **편향에 '유령' 이라는 이름을 붙이고 구성 간 차이로
재되, 참값 · 잔차 · 다중 시작 없이 '할당 인공물' 로 닫는다.**
