---
title: "Khalik Z., Donkers M.C.F., Sturm J., Bergveld H.J. 2021 — Parameter estimation of the Doyle–Fuller–Newman model for Lithium-ion batteries by parameter normalization, grouping, and sensitivity analysis (J. Power Sources 499, 229901)"
source_url: local-upload/55._Parameter_estimation_of_the_Doyle_Fuller_Newman_model_for_Lithium-ion_batteries_by_parameter_normalization_grouping_and_sensitivity_analysis.pdf
source_url_note: "본문 PDF 11 쪽(Elsevier 판 — PDF 쪽 = 인쇄 쪽 1–11) 3,574,085 B · 업로드 접두사 6a611bdd · 4차 묶음 파일 55 · ⚠ 액체셀 도구 논문(ASSB 아님 — 28호 선례 · 도구 칸) · SI 없음(원문에 보충 언급 0) · 자료 · 코드 공개 0 — 자동 크롭 12(그림 1–8 · 표 1–4 — f4 · f8 왼쪽 잘림 · t1 = t2 바이트 동일 쪽 전체 · t3 · t4 쪽 전체) + 수동 6(그림 4 · 8 전폭 · 표 1–4 단독) 전부 봤다 · 그림 2–8 은 벡터 경로 판독 · 표 1 · 3 의 식 · 지수는 쪽 렌더로 확인(판독용 · 커밋 안 함)"
source_doi: 10.1016/j.jpowsour.2021.229901
source_license: "© 2021 Published by Elsevier B.V.(인쇄) — CC · 오픈 액세스 표기 0 · 구독본으로 다룬다 — 이 digest 는 인용 · 요약 · 재현 계산만 담는다(그림 크롭은 위키 관례대로 raw/figures 에 — 변형 없는 잘라내기)"
pdf_sha256: 24ba9143297b6f819d5f004a9aa7d9e2e7f228ee169332036a0fde36bddb0165
ingested: 2026-10-02
sha256: ce935a9eabb2b5026c345a026c61f2a2512dd0f675d46636913fa4c0c22ab27c
---
# 수집 목적

`assb` 섹션 **95호** — **4차 묶음 파일 55**(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 요청 14 편 중 다섯째 · 2026-10-02 사용자 공급 · 파일 51–64 = 91–104호를 받은 순서대로). ⚠ **이 편은 ASSB 논문이 아니다 — 액체 전해질 Li-ion 셀의 DFN(P2D) 매개변수 추정 도구 논문이다.** 28호(Bizeray 2019 — 액체셀 SPM 식별성) 선례대로 `assb` 번호는 받되 **"ASSB 아님(도구 칸)"** 으로 다루고, 채움표 Q 칸은 도구 칸 규칙(28 · 34 · 36호 행 형식)대로 적는다. 닻은 `questions/assb-contact-loss-vs-lampe.md` 의 **Q4(유일성 · 식별성)** 이고, 이 편이 더 직접 닿는 곳은 우리 `degradation-degeneracy` 의 물음(**OCV 맞춤의 유일성** — 창 네 좌표가 곡선으로 정해지는가)과 `mode-observability` Phase 1c · 1d · 1k(창 대수의 유효 자유도 · null 방향 · 축퇴가 사는 층)다 — 이 편의 매개변수 표에 **창 네 끝점(`s_n,0%` · `s_n,100%` · `s_p,0%` · `s_p,100%`)이 추정 대상으로 들어 있기** 때문이다(우리 쪽 수치는 `degradation-degeneracy/docs/RESULTS*.md` · `mode-observability` 결과 폴더가 정본 — 여기 옮기지 않는다).

Eindhoven 공대(TU/e) 전기공학과 **Zuan Khalik · M.C.F. (Tijs) Donkers · H.J. (Henk Jan) Bergveld**(+ NXP Semiconductors) 와 TU München 전기에너지저장기술연구소(EES) **Johannes Sturm** 의 *J. Power Sources* 2021 편. BMS 용 DFN 을 **① 정규화 · 묶음으로 재매개화(원 35 → 24) ② 범위 정규화(β ∈ [0, 1]) 위의 국소 감도 순위(유한차분 감도 행렬의 피벗 QR — Lund & Foss 2008) ③ 순위 위쪽 매개변수만 비선형 최소제곱(`lsqnonlin` · trust-region-reflective)** 으로 맞추는 절차를 내고, 실셀 둘(**Cell 1** — 셀 EMF 만 · 전류/전압 자료 셋 [38] · **Cell 2** — 분해로 잰 전극 평형 전위 [24, 39] · 자료 하나)과 **합성 셀**(범위 안 무작위 매개변수의 같은 DFN · 다중 시작 50 · 인공 모형 오차 둘)로 "추정 매개변수 수 · 추정 자료 길이 · 모형 오차" 의 영향을 본다. **열화 · 접촉 · 압력 · 고체전해질 · 온도 0** — 셀 화학도 본문에 없다(참고문헌 제목에만).

들어온 경로: 원장 행(도착 표시 전 원문 그대로) "| ★★★ | **Khalik·Donkers·Sturm·Bergveld 2021** — *J. Power Sources* **499**, 229901 | 27 | 1 | **Q4** | "P2D 파라미터를 실험에 맞춘다" 의 두 인용 중 하나 — DFN **파라미터 그룹화** 도구 후보 (공백 1번 후보, 액체셀) |". 위키 grep(`Khalik` · `229901` · `Donkers` · `Bergveld` 대소문자 무시): **27호**(Sinzig 2024 — [27] · 후속 표 :375 **★★★★** "이 편이 'P2D 파라미터를 실험에 맞추는 연구' 로 인용한 둘 중 하나 — (`[추론]` 제목 미인쇄, 원장 확인 필요) DFN 파라미터 **정규화 · 그룹화 · 민감도**로 식별 가능한 조합을 만드는 계보. **곱 쌍(①–③)을 그룹으로 묶는 도구의 원전 후보** \| **Q4**") · 카드 :5073(27호 Status Log "후속 1순위 = **Khalik 2021**") · `log.md` :2103(27호 항 "★★★★ 1") · 92호 :568((다) 표 — 그 결정의 "닿는 논문" 목록에 이 편 이름) · 92 · 93 · 94호 후속 절의 "4차 묶음 13 편과의 관계" 문장(지목 아님 — 교차 기록). **지목은 27호 후속 절 하나 = 1 — 원장 "27 \| 1" 과 일치**(등급은 27호 ★★★★ ↔ 원장 ★★★ — 표시만). 이 편은 우리 digest **하나**를 인용한다(**28호 Bizeray 2019 = [13]** — §인용 대조) · 4차 묶음 다른 13 편은 **인용 0**(Lu 2022 = 파일 56 은 이 편보다 뒤).

이 digest 의 일 (지시):

1. **(a) 재매개화(정규화 · 묶음)의 결과** — 원 DFN 매개변수 수(표 1(a) — 인쇄 35) → 묶은 뒤 수(표 3) · 각 묶음의 정의 · **구조적 식별성**을 증명했는가(출력이 묶음만의 함수임을 보임) · 아니면 감도로 고른 것인가(**실제적 식별성**) · 카드 형식 Q4 어휘 전수.
2. **(b) 강조문 다섯(Highlights)** 을 인쇄 그대로 옮기고 각각의 근거 절 · 그림을 단다.
3. **(c) 평형 전위 곡선 보정(그림 2)** — 반쪽전지 OCP 를 어떻게 "보정" 했는가(이동 · 늘림 · 창) · 우리 α·β 창 맞춤과 같은 연산인가 · [[halfcell-ocp-shape-invariance]] 가정을 쓰는가.
4. **(d) 추정 자료 길이 · 과적합 · 모형 오차 편향** — 무엇으로 보였는가(합성 자료인가 실셀인가 · 참값이 있는가).
5. **(e) 우리 것에 주는 것** — 우리 4-창 + γ_Si 맞춤(`bms-balancing/docs/NEW_MODEL_REQUIREMENTS.md` §7 유일성 측정 요구 — 읽기만)에 이식할 수 있는 절차(정규화 · 묶음 · 감도 순위 · 자료 길이 규칙)와 못 하는 것.
6. **(f) 후속 후보** — DFN 식별성 · 매개변수 추정 계보(우리 위키에 없는 것만 · 액체셀이면 "액체셀 도구" 표시 · 지목 수는 각 digest 후속 절 grep 값만 · 4차 묶음 13 편은 "4차 묶음 파일 NN").

⚠ **표기 규약**: `[인쇄]` = 원문이 실제로 쓴 것 · `[도표]` = 그림을 눈으로 읽은 값(판독 폭 표시) · **`[도표·벡터]`** = 그림의 벡터 경로 좌표를 축 눈금으로 보정해 읽은 값(곡선 꼭짓점 · 상자 그림 중앙값 선 · 줄기 끝 · 판독 폭 ≈±0.3 mV(그림 5) · ±1 mV(그림 2 · 6) · ±0.005 β(그림 7) · ±0.02 decade(그림 4)) · `[재현]` = 원문 수치 · 식으로 우리가 다시 계산 · `[재현·벡터]` = 벡터 판독 값 위의 계산 · `[재현·가정]` = 가정이 붙은 재현(가정을 같이 적는다) · **`[재현·대수]`** = 인쇄된 식만으로 한 대수(수치 0) · `[해석]` = 우리 해석 · **"(N호 digest 전사)"** = 이 편이 인용한 원 논문을 이 세션에서 다시 열지 않고 우리 위키 digest 에 전사된 값으로 대조한 것. **`[데이터]` 0** — 이 편은 원자료를 예치하지 않았다(자료 · 코드 공개 진술 0). ⚠ **측정 · 인용 · 모형 · 적합 구분**: 이 편 안의 수치는 ① **측정 자료의 재사용**(Cell 1 전류 · 전압 · EMF ← [38] · Cell 2 자료 · 전극 평형 전위 ← [24, 39] — 이 편에서 새로 잰 것인지 미인쇄) ② **인용 값**(매개변수 범위 표 3 ← [23, 24, 26, 35–37] · 흑연 U_n ← [23]) ③ **적합 값**(추정 매개변수 — 값 표는 인쇄 0 · 그림 7 의 정규화 β 상자 그림뿐) ④ **모형 출력**(합성 셀 — 참값 · 상태 · 표 4) 넷이다. 넷을 섞지 않는다.

⚠ **쪽 표기**: Elsevier 판 11 쪽 — 표지 0 · PDF 쪽 = 인쇄 쪽 번호 1–11(머리말 "Journal of Power Sources 499 (2021) 229901" · 쪽 번호 · "Z. Khalik et al." · PageLabels = PDF 쪽 1–11). 이 digest 는 "p. 5" 로 적는다.

---

# 판정 먼저

1. ★★★★ **(a) 재매개화 — 35 → 24 는 구성상 증명된 축소(출력이 24 묶음의 함수)이지만, 24 의 식별성은 증명하지 않았고 실제로 성립하지 않는다; 무엇을 추정할지는 국소 감도 순위(실제적 · 한 점)로 골랐다.** `[인쇄]` "the total number of parameters of the DFN model as formulated in Table 1(a) amounts to **35**" · "The total number of parameters of the reparameterized model is **24**" · 정규화 `r̂ = r/R_s` · `x̂`(식 16) · 묶음(표 3 — 예 `D̂_s = D_s/R_s²` · `D̂_e = D_e F A c_e,0/(1 − t₊⁰)` · `p̂ = ε_e^p/δ` · `σ̂ = σε_s A/δ` · `κ̂ = κA` · `R̂_f = R_f R_s/(3Aδε_s)` · `R̂_cc = R_cc/A` · `k̂₀ = k₀c_e,o^α_a/(R_s F)` · `ε̂_e = ε_e F A δ c_e,o/(1 − t₊⁰)`) — 표 1(b) 식 (8)–(14)는 **묶음만으로 쓰여 있다** ⇒ 원 35 의 **적어도 11 방향은 구조적으로 비식별**(구성 증명 — 그 방향을 따라 출력이 글자 그대로 같다). 그러나 ① `[재현]` 35 = 표 2 의 "a"(considered) 표시 **34** + 표시 없는 `A`(활성 면적) · 24 = `Q`(측정) + 창 넷 + 19 · 추정 22 = 24 − `Q` − `R̂_f,p`(범위 **[0, 0]**) ② **축소 하나는 가정이다** — 식 (12a) · (12b) 가 `α_c` 자리에 `1 − α_a` 를 쓴다(본문 언급 0 · `[재현·대수]` 이 가정이 없으면 `k̂₀` 묶음에 `(3ε_sFAδ)^(1−α_a−α_c)` 가 남아 `ε_s · A · δ` 가 동역학 묶음에서 빠지지 않는다 — **묶음이 정확하려고 필요한 가정**) ③ ★ **24 안에 정확한 척도 대칭 하나가 남는다** `[재현·대수]` — 식 (9a) 는 `D̂_e p̂`, (11a) 는 `κ̂ p̂` 곱으로만 쓰므로 `(D̂_e, κ̂, p̂_n, p̂_p, p̂_sep) → (D̂_e/λ, κ̂/λ, λp̂_n, λp̂_p, λp̂_sep)` 가 출력 불변 ⇒ 식별 가능한 조합은 **많아야 23**(전해질 수송 다섯 → 넷) — 사전 상자는 이 대칭을 `κ̂` 범위(×2.86 · 선형 척도)로 자를 뿐 없애지 않는다 ④ ★ **경우 1(셀 EMF 만 앎 — Cell 1)에서 창 네 끝점은 평형 채널에 정의상 보이지 않는다** — `[인쇄]` "**the same EMF-SOC relation can be reached with any choice between 0 and 1** for the parameter values of s_n,0%, s_n,100%, s_p,0%, s_n,100% [sic], these parameters also affect the dynamics of the cell through the (ĉ_s,max − ĉ_s,e)^α_a term in (12b)". 고른 방법 = 감도 행렬 `S = ∂V̂/∂β`(유한차분 · 추정 전류 프로파일)의 **피벗 QR 순위** — `[인쇄]` "in order to avoid solving an ill-conditioned optimization problem" — 국소 · 한 점(계산점 미인쇄 G6) · 범위 정규화 의존 · 문턱 0 · `[재현]` 그림 4 의 `|r₁₁|/|r_kk|` 는 고른 12 개 감도 부분행렬 조건수의 **하한** ≥10^2.98(Cell 1) · 10^3.00(Cell 2) · 22 개 ≥10^6.20 · 10^6.46 `[도표·벡터]`. 어휘(본문 · 머리말 제외): `identifiab*` **7** · `uniqu*` 1(초록 "the difficulty of **uniquely** determining all model parameters") · `sensitiv*` 40 · `Fisher` · `covarian*` · `Hessian` · `Jacobian` · `condition number` · `bootstrap` · `posterior` · `noise` **0** · `ill-condition*` 1 ⇒ **ASSB 0/95 — 도구 칸 · 여든일곱 번째 성질**(§(a) 6).
2. ★★★★ **(b) 강조문 다섯 — 셋은 그림으로 뒷받침되고, 둘은 조건이 떨어진 채 인쇄됐다.** ① "Parameters obtained from input/output data are not necessarily physically meaningful." ← §4.4–4.5 · 그림 7 · 8 · 표 4 — `[도표·벡터]` 무잡음 · 같은 모형(이상적)인데도 합성 참값이 상자(IQR) 밖인 매개변수 **14/22**(첫 10 중 6) · β RMSE 0.30 ↔ 무작위 0.43 — **모형 오차 없이도** 물리 의미가 보장되지 않는다(저자는 주원인을 모형 오차로 읽는다) ② "Estimating all DFN model parameters is not necessary to obtain an accurate model." ← §4.2 · 그림 5(a) — "accurate" = **출력 RMSE**(Cell 1 Data 1 12 개 3.50 ↔ 22 개 3.54 mV `[도표·벡터]`) — 유일성과 다른 명제(저자도 ① 로 가른다) ③ "The length of estimation data should be carefully selected to avoid overfitting." ← §4.3 · 그림 5(b) · 6 — 실셀 둘 · 참값 없음 · 단일 회차 · **"과적합" 근거 = Cell 1 90 → 100 % 에서 Data 2 · 3 +0.42 · +0.78 mV** `[도표·벡터]` — 같은 곡선의 다른 구간 요동(30 → 40 % Data 1 +0.54 · 10 → 20 % Data 2 +0.41 mV)과 같은 크기 · 마지막 10 % 는 SoC 0.282 → 0.214 구간 `[재현·가정]` ④ "Modeling errors can lead to a large bias and variability of the estimated parameters." ← §4.4 · 그림 7 · 8 · 표 4 — 합성 셀 + 인공 오차 둘(EMF 3 mV 정현 · `D̂_s,pos` 농도 의존 창 안 ×23 `[재현]`) — 참값 있음 · 매개변수 RMSE 0.43 · 0.44 ↔ 무작위 0.43 ⑤ "Ideally, parameters should be determined using both cell teardown and estimation." ← §4.5 · 결론 — **권고**이고 시험 0: 그림 6 의 분해 매개변수 모형(Sturm 2019 — 일부는 문헌값) 오차와 그림 7 의 "범위가 좁으면 일관성 ↑"(Cell 1 · 참값 없음)만 · 결론의 "this bias and variability can be reduced by determining tighter parameter ranges" 중 **편향 감소는 참값 있는 시험이 없다**(D).
3. ★★★★ **(c) 그림 2 의 "보정" 은 이동 · 늘림(우리 α·β)이 아니라 — 빌린 음극 곡선으로 양극 곡선을 정의한 뒤(경우 1), 0–10 % SOC 구간의 양극 모양을 직선으로 갈아 끼우고 음극을 EMF 로 되계산한 것이다.** `[인쇄]` 경우 1 "assuming the negative equilibrium potential U_n from literature, from which U_p can be determined" · "it is ensured that the modeled EMF coincides exactly with the measured EMF (**by definition**)" · 보정 "we replace the values of U_p from 0% to 10% SOC with a linear function … the slope is chosen as the mean of the slope of the calculated U_p curve between 10% and 40% SOC … U_n = U_p − U_EMF". `[도표·벡터]` 계산 U_p 최솟값 SOC 0.0994 · 3.622 V(인쇄 "≈10 %" ✅) · 그려진 직선 기울기 0.545 V/SOC ↔ 규칙대로 0.564(−3 %) · 보정 전후 `U_p − U_n` 이 전 구간 같다(정의 ✅). ★ **빌린 곡선의 형상 오차는 다른 전극으로 1:1 간다** — (계산 − 측정) U_p = (가정 − 측정) U_n ±0.01 V · SOC 0.1–1 에서 **+6 … +54 mV(평균 +26)** — 보정은 0–10 % 만 고치고 이 오프셋은 그대로 둔다. ★ **분해 측정 전극 쌍([24])도 셀 EMF 와 −9.5 … +13.5 mV(SOC 0.03–1 · rms 5.8 mV)** 어긋난다 `[재현·벡터]` — 이 편 합성 시험에서 매개변수 추정을 무작위 수준으로 보낸 EMF 오차(진폭 3 mV · RMS 2.1 mV)보다 크다. 우리 대응: **경우 2(분해 OCP 를 창으로 맞춤 — 방법은 [23, 24, 26] 에 미룸)가 우리 α·β 와 같은 연산**이고 [[halfcell-ocp-shape-invariance]] 가정(분해 전극 곡선이 셀 안에서도 같은 모양)을 깐다 · **경우 1 은 한쪽 형상을 빌리고 다른 쪽 형상을 자유로 둔 극단 — 창이 OCV 채널에서 사라지는 판**이다. ⚠ 그림 2 의 EMF(`U_p − U_n`)는 그림 3 의 Cell 2 EMF 보다 SOC 0.2–1 에서 **21–59 mV** · ≤0.1 에서 113–313 mV 높다 `[재현·벡터]` — 본문 "U_p is calculated from the EMF function shown in Fig. 3" 과 맞지 않는다(D2).
4. ★★★★ **(d) 자료 길이 · 과적합은 실셀(참값 없음 · 단일 회차)로, 모형 오차 편향은 합성 셀(참값 하나 · 같은 모형 · 무잡음)로 보였다 — 둘 다 조건이 좁다.** 실셀: `[재현·벡터]` Cell 1 용량 ≈10.4–10.6 Ah(미인쇄 — 그림 3 전류 적분 7.81 · 7.75 · 7.38 Ah ÷ 그림 6 SoC 폭 0.741 · 0.732 · 0.710 · 세 자료가 1 % 안에서 맞음 · 시작 전압이 EMF 와 ±4 mV) · Data 1 첨두 24.6 A ≈2.3C · 평균 8.3 A ≈0.8C · Cell 2 자료 1,700 s(= 510 s/0.30 = 1,105 s/0.65 `[재현]`) · **그림 6 ↔ 그림 5(b) 폐합 ✅**(Cell 2 30 % 24.4 ↔ 24.38 · 65 % 5.0 ↔ 4.99 · Cell 1 60 % 3.69 · 3.42 · 3.71 ↔ 3.68 · 3.38 · 3.77 mV) → 그림 5(b) 도 **14 개 추정**(미인쇄 G9) · Cell 2 "검증" 은 추정 구간을 포함 · 90 % · 12 개는 **검증 RMSE 로 고른 값**(검증 자료가 모형 선택에 쓰였다). 합성: 50 시작 · 22 개 · Data 1 입력(⚠ 그림 8 시간 축 76.7 분 ↔ Data 1 56.7 분 — D7) · `[재현]` 표 4 "Random parameters" 0.43 · 0.38 = 균등 무작위 β 의 기대 RMS 0.427 · 0.36 ✅ · 무잡음 · 같은 모형인데 출력 RMSE 중앙값 **0.13 mV ≠ 0** → 회차 절반 이상이 전역 최소(잔차 0)에 못 닿았다 — **다중 시작 산포는 근최적 폭과 수렴 실패가 섞인 값**(잔차 문턱 인쇄 0) · 모형 오차 1.2 mV(표 4 1.19 · 1.17) ↔ 실셀 잔차 3.4–3.7 mV(그림 6 위 `[재현·벡터]`) = **×0.32–0.35**(인쇄 "in the same range" — D). ★ 세 수정 모두에서 **양극 창 끝 `s_p,100%` 의 중앙값이 사전 범위 하한 0.22 로 간다**(참 0.418 `[도표·벡터]`) · 그림 8 `s_p(L)` 띠가 참값 밖(t = 0 ≥0.105 아래).
5. ★★★★ **(e) 우리 것 — 이식할 것 셋 · 못 할 것 셋.** 이식: ① **피벗 QR 순위 + `|r₁₁|/|r_kk|` 조건수 하한** — NEW_MODEL_REQUIREMENTS §7-1 ②(조건수 — 미구현)의 값싼 첫 판(단 한 점 · 범위 정규화 의존 · 하한) ② **합성 참값 + 인공 모형 오차 주입 + 무작위 기준(β RMSE)** — 우리 하네스에 반쪽전지 형상 오차(수 mV)를 넣어 창 · 모드가 경계로 가는지 보는 시험 설계 ③ **경계 접촉 + 범위 확장 시험**(β −0.3 … 1.3) — §7-1 ③ 의 인쇄 선례(Cell 1 경계 10/22 · 확장하면 `s100,n` 이 0.2–1.3 으로 퍼짐). 못 함: ① "12 개면 충분" · "자료 70–90 %" 같은 **수치 규칙**(한 셀 · 한 회차 · 출력 RMSE 기준 · 동적 자료) ② **경우 1 구성**(EMF 로 한 전극 곡선을 정의)은 우리 창을 정의상 비식별로 만든다 — 우리는 경우 2(형상 고정) ③ **다중 시작 산포 = 폭** 으로 읽기(§7-1 ① · ⑤ — `tol` 없는 폭은 폭이 아니다).
6. **(f) 채움표** — Q1 없다(액체 · 접촉 0 · `θ(N)` 0/95 — 층 하나 `[해석·대수]`: 정규화 DFN 에서 표면 접촉 손실은 `k̂₀`(× `A_eff`) · `R̂_f`(÷ `A_eff`) 두 동역학 묶음으로, 입자 통째 비연결(= `ε_s` 형 LAM 과 같은 자리)은 창 폭(용량) · `R̂_f` · `σ̂` 로 · `c^max` 형 LAM 은 창 폭 하나 — 양극은 `R̂_f,p` 범위 [0, 0] 이라 둘째 서명이 꺼져 있다) · Q2 없다(ASSB 관측 0 · 분해 전극 OCP 는 방법 쪽) · Q3 층 하나(적합 + 합성 참값 복원 — 같은 모형 · 무잡음 · 참값 하나 · 추정값 표 0 · 경계 접촉 10/22) · **Q4 ★ 있다 — 단 액체(도구 칸) · ASSB 0/95 · 여든일곱 번째 성질** · Q5 해당 없음 · Q6 없다(`pressure` 0) · Q7 해당 없음 · Q8 층 하나(화학 미인쇄 · EMF 측정법 미인쇄 · 빌린 U_n 형상 오차 → U_p · 두 EMF 21–59 mV). **누적 ≈20.0 → ≈20.0 (새 칸 0).**
7. **(f) 후속** — ★★★ [24] **Sturm, Rheinfeld, Zilberman, Spingler, Kosch, Frie, Jossen 2019 *JPS* 412, 204**(새 — Cell 2 분해 매개변수 · 측정 Si-흑연 U_n · Ni-rich U_p — 우리 γ_Si 축 · 액체셀 도구) · ★★★ [25] **Jobman, Trimboli, Plett 2015 *J. Energy Chall. Mech.* 2(2), 45**(새 — 묶음 원형 24 · Plett 계보 = 4차 묶음 파일 56 Lu 2022 의 앞) · ★★ [23] Ecker 2015 *JES* 162, A1836(**재지목 28 · 93 · 95 = 3** — 범위 원전 + 빌린 U_n 의 출처) · ★★ [30] Lund & Foss 2008 *Automatica* 44, 278(새 — 직교화 순위 원전) · ★★ [18] Jin · Danilov · Van den Hof · Donkers 2018(새 — 묶음 없는 판 · 91호 저자) · ★★ [22] Chu … Plett … Ouyang 2020 *J. Energy Storage* 27, 101101(새 — 기준극 기반 식별) · ★★ [27] Ramadesigan 2011 *JES* 158, A1048(새 — 노화 축 추정 · 원장의 Ramadesigan 2012 리뷰와 다른 편) · ★★ [26] Schmalstieg 2018 *JES* 165, A3799(새) · ★ [38] Beelen 2018 · [34] Bergveld · Kruijt · Notten 2002 · [17] Zhou & Huang 2020 · [16] Schmidt A.P. 2010 *JPS* 195, 5071 · [39] Sturm 2019b(새). 재지목 안 함(목록 인용): [11] Santhanagopalan 2007(원장 28 \| 1) · [33] Smith & Wang 2006(원장 49 · 92 묶음 행). 꼬리만: [19] **Forman 2011 ACC 판** — 원장 Forman 2012 *JPS* 행과 **다른 편**(같은 저자 · 학회 판 · Fisher 분석 이전) · 이 편의 "identifiability of the DFN model is poor" 두 문장이 이 판을 가리킨다.

---

# 서지

| 항목 | 값 (`[인쇄]` — p. 1 · p. 10 · XMP) |
|---|---|
| 제목 | **"Parameter estimation of the Doyle–Fuller–Newman model for Lithium-ion batteries by parameter normalization, grouping, and sensitivity analysis"** |
| 저자 · 소속 | **Z. Khalik**ᵃ,\* · **M.C.F. Donkers**ᵃ · **J. Sturm**ᶜ · **H.J. Bergveld**ᵃ,ᵇ — ᵃ Department of Electrical Engineering, Eindhoven University of Technology · ᵇ NXP Semiconductors(Eindhoven) · ᶜ Institute for Electrical Energy Storage Technology (EES), Technical University of Munich · \* 교신 Khalik(메일 넷 인쇄 — 옮기지 않음) |
| 저널 | *Journal of Power Sources* **499**, **229901** (2021) · doi `10.1016/j.jpowsour.2021.229901` · ISSN 0378-7753 · XMP `prism:coverDate` 2021-07-01("1 July 2021") · 연구 논문 |
| 일정 | Received **12 January 2021** · revised **16 March 2021** · Accepted **4 April 2021** · Available online **3 May 2021** · `[재현]` 투고 → 수정 63 일 · 수정 → 채택 19 일 · 채택 → 온라인 29 일 · 온라인 → 권호 59 일 · PDF 생성 2021-05-12(온라인 9 일 뒤) |
| 저작권 | `[인쇄]` "0378-7753/© 2021 Published by Elsevier B.V." — CC · 오픈 액세스 표기 0 · XMP `prism:copyright` "© 2021 Published by Elsevier B.V." · `xmpRights:Marked` True ⇒ **구독본으로 다룬다** — 이 digest 는 인용 · 요약 · 재현 계산만 담고, 그림 크롭은 위키 관례대로 `raw/figures/` 에(변형 없는 잘라내기) |
| 자금 | Horizon 2020 — **EVERLASTING-713771**(BMS) · **AutoDrive-737469** · 사사: Ishaan Mahashabde(IEC AIR TOOLS, Pune — 예비 연구) |
| CRediT | Khalik — 착상 · 방법 · 소프트웨어 · 검증 · 분석 · 조사 · 자원 · 자료 · 초고 / Donkers — 착상 · 방법 · 자원 · 검토 · 지도 · 자금 / **Sturm — 조사 · 자원 · 검토**(Cell 2 자료 · [24, 39] 저자) / Bergveld — 착상 · 방법 · 자원 · 검토 · 지도 · 자금 · 경쟁 이익 없음 |
| 코드 · 자료 | **공개 진술 0** — 계산 도구는 `[인쇄]` "the **lsqnonlin** function in **MATLAB** with the trust-region-reflective algorithm" · 모형 구현은 자기 [28](Khalik 2021 *JPS* 488 — "battery modeling toolbox") · Cell 1 자료 [38] · Cell 2 자료 [24, 39] |
| 키워드(정보 사전 · XMP) | Battery parameter estimation · Doyle–Fuller–Newman model parameters · Doyle–Fuller–Newman model parameter estimation |
| 분량 | 11 쪽(본문 p. 1–10 · 참고문헌 p. 10–11) · 그림 **8**(래스터 1 — 그림 1 · 벡터 7 — 글자까지 외곽선) · 표 **4** · 번호 식 **1–22**(표 1 안 1–14 · 15 · 16 · 17 · 18a–b · 19a–b · 20 · 21 · 22) + 번호 없는 수정식 둘(4.4 절) · 참고문헌 **[1]–[40]**(번호 빠짐 0 — p. 10–11 목록에서 직접 셈) |
| 절 | Highlights · Abstract · 1. Introduction · 2. Battery modeling(2.1 DFN model equations · 2.2 Parameter normalization and grouping) · 3. Model parameterization approach(3.1 Equilibrium potential model · 3.2 Ranges of the grouped parameters · 3.3 Sensitivity analysis of the grouped parameters · 3.4 Estimating the grouped parameters) · 4. Results and validation(4.1 Sensitivity analysis · 4.2 Influence of the number of estimated parameters on the accuracy · 4.3 Influence of the length of estimation data · 4.4 Consistency and accuracy of the estimated parameters · 4.5 Consistency and accuracy of the internal states) · 5. Conclusions · CRediT · Declaration · Acknowledgments · References |

**PDF 메타데이터 (직접 읽음 · pymupdf)**: 3,574,085 B · sha256 `24ba9143297b6f819d5f004a9aa7d9e2e7f228ee169332036a0fde36bddb0165`(호출자 명시값 ✅ — 직접 재계산) · `PDF 1.7` · 11 쪽(전부 595.3 × 793.7 pt) · 암호 0 · 정보 사전: title **"Parameter estimation of the Doyle–Fuller–Newman model for Lithium-ion batteries by parameter normalization, grouping, and sensitivity analysis"**(전문 — 호출자 메모의 "…grouping, an" 은 줄임) · author **"Z. Khalik"** · subject **"Journal of Power Sources, 499 (2021) 229901. doi:10.1016/j.jpowsour.2021.229901"** · keywords **"Battery parameter estimation,Doyle–Fuller–Newman model parameters,Doyle–Fuller–Newman model parameter estimation"** · creator **"Elsevier"** · producer **"Acrobat Distiller 8.1.0 (Windows)"** · 생성 **D:20210512235150Z** · 수정 **D:20210513013726Z**(호출자 메모와 같음 ✅) · XMP **5,367 B**(`dc:creator` 넷 · `prism:volume` 499 · `prism:pageRange` 229901 · `prism:coverDate` 2021-07-01 · `jav:journal_article_version` **VoR** · `pdfx:robots` noindex · crossmark 도메인 elsevier.com · sciencedirect.com · `crossmark:MajorVersionDate` 2010-04-23(조판 틀 값으로 읽힘 — 이 편 날짜 아님) · `xmp:CreateDate` 2021-05-12T23:51:50 · `ModifyDate` 2021-05-13T01:37:26 · `pdf:CreationDate--Text` "13th May 2021") · **PageLabels**: 1 부터 십진(PDF 쪽 = 인쇄 쪽) · 래스터 **4**(p. 1 저널 로고 238 × 298 · 표지 248 × 272 · crossmark 119 × 119 / p. 2 **그림 1** 860 × 366) · 그림 2–8 은 **벡터**(텍스트 층에 눈금 숫자 0).

⚠ **텍스트 층**: 합자 0(`ﬁ` · `ﬂ` 0) · NFKC 가 바꾸는 것은 수식 이탤릭 기호 42 종과 줄임표뿐 — **낱말 셈은 NFKC 전후 같다**. 표 1 · 3 의 식 · 묶음 · 지수(예 `D̂_s,pos` 의 `10^(−4+8(s_p−0.5)²)`)는 텍스트 층에서 위첨자가 사라져 **쪽 렌더로 읽었다**(수동 크롭 tab_1 · tab_3 · tab_4 — 판독용 렌더는 커밋 안 함).

---

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **Cell 1 · Cell 2 의 정체** — 화학 · 형식 · 용량 · 제조사 인쇄 0(`silicon` · `nickel` · `NMC` · `LFP` 본문 0 — 참고문헌 제목 [24] "18650 nickel-rich, silicon-graphite" · [39] 같음) · Cell 1 은 "[38]" 뿐 | `[재현·가정]` Cell 1 ≈10.4–10.6 Ah(전류 적분 ÷ SoC 폭) · Cell 2 용량은 재현 근거 0 — C-rate · 결과의 일반성 |
| **G2** | **온도** — `temperature` · `°C` **0** · 등온 가정 문장도 0 | 동적 프로파일(첨두 ≈2.3C)의 발열 · 분해 매개변수 모형([24])과의 비교 조건 |
| **G3** | **EMF 측정법**(두 셀) — 인쇄 0("There are several techniques available to determine the EMF, where an overview can be found in [34]") | 그림 2 ↔ 그림 3 의 Cell 2 EMF 가 21–59 mV(SOC 0.2–1) 다르다 `[재현·벡터]` — 어느 것이 추정에 쓰였는지 · 의사 OCV 인지 |
| **G4** | **경우 1 의 창 값**(Cell 1 · 그림 2) · **창을 추정할 때 U_p 를 매번 EMF 로 다시 정의하는지** — 인쇄 0 | "어느 창이든 EMF 정확 일치" 가 추정 중에도 유지되는지 — 유지되면 창은 동역학으로만 · 아니면 OCV 채널이 창을 본다 |
| **G5** | **0–10 % 직선 보정을 Cell 1 에도 썼는지** — 인쇄 0(그림 2 는 Cell 2 자료로 한 예시) | Cell 1 자료는 SoC 0.214–0.976 이라 0–10 % 는 자료 밖 — 창 사상만 바뀐다 |
| **G6** | **감도 행렬의 계산점(β)** · 유한차분 간격 · 정규화 순서 — 인쇄 0(계산 프로파일 = 추정 프로파일만 인쇄) | 순위 · `\|r_kk\|` 가 한 점의 성질 — Cell 1 추정값 10/22 가 범위 끝인데 순위는 어디서 쟀나 |
| **G7** | **추정된 매개변수 값**(물리 단위 · β) — Cell 1 · Cell 2 모두 표 0(그림 7 상자 그림만 · Cell 2 는 그림도 0) | 재풀이 · 문헌 대조 · 경계 접촉 판정 불가 |
| **G8** | **합성 셀의 설계** — 참값 벡터(그림 7 의 β 점뿐) · 잡음(`noise` 0 → 무잡음으로 읽힘) · 입력(인쇄 "the same input data used for simulation" ↔ 그림 8 시간 축 76.7 분) · 무작위 시작의 분포 · `lsqnonlin` 허용 오차 · 회차별 잔차 | 다중 시작 산포가 근최적 폭인지 수렴 실패인지(출력 RMSE 중앙값 0.13 mV ≠ 0) |
| **G9** | **그림 5(b) 의 추정 매개변수 수** — 인쇄 0 | `[재현·벡터]` 그림 6(14 개)과 점 값이 같아 14 개로 읽힌다 |
| **G10** | **분해 매개변수 모형([24])의 조건** — 온도 · 초기 SoC · EMF · 어느 매개변수가 측정이고 어느 것이 문헌인지 | 그림 6 의 −37 mV 부호 고정 오프셋이 무엇에서 오는가 — "measured parameters 는 출력을 못 맞춘다" 의 근거 |
| G11 | **[25] Jobman 2015 의 24 묶음** — "also 24 … effectively two parameters less" 대조 | 원전 미열람 — 차이 둘(R_cc · α_a = α_c = 0.5) 만 인쇄 |
| G12 | **Data 1 · 2 · 3 의 자료 출처 · 측정 조건** — [38](Beelen 2018 — 등가회로 실험 설계) 미열람 | 드라이브 사이클인지 · 휴지 포함인지 · 같은 셀인지 |
| G13 | **"both of the modifications"** — 그림 7 · 8 의 "both" 판 결과 수치(표 4 열 없음) | 본문 "the MRMSE of the parameters with both of the modifications is almost equal to …" 가 어느 열인지 |

---

# 보충 자료 — 받은 것 · 대조

**SI 없음 (원문에 보충 언급 0).** 호출자 대조와 같은 결과를 직접 다시 셌다 — 본문 · 캡션 · 표 · 참고문헌 전문(NFKC 전후 같음)에서 `supplement*` · `supporting information` · `appendix` · `video` · `movie` · `github` · `zenodo` **0 회** · "data availab*" **1 회** = 본문 문장("one set of experimental data **availab**le for parameterization" — 공개 진술 아님) · "Data Availability" 절 0. 원자료 예치 0 · 코드 공개 0. 그래서 이 digest 의 재현은 **인쇄 수치 · 식 + 쪽 렌더 + 그림 벡터 경로 + 우리 digest 전사** 네 층뿐이다.

---

# 그림 · 표 — 자동 12 항목 + 수동 6, 실제로 연 것 **18/18**

크로퍼(`wiki/tools/extract_figures.py`)가 그림 1–8 을 `fig_1 … fig_8` 로, 표 1–4 를 `tab_1 … tab_4` 로 잡았다(SI 오판 0 — 파일명 `55._Parameter_estimation_of_the_Doyle_Fuller_Newman_model_…` 의 `SI_TAG` False 를 첫 실행 전에 확인 · 실행 뒤 이름을 눈으로 확인). 자동 크롭 점검(`figures.json` `note` 에 적음 — 자동 파일은 지우지 않았다):

- **fig_4 왼쪽 잘림** — 벡터 그림은 x 41.8 pt 부터인데 bbox 가 60.8 pt 에서 시작 → y 축 이름 "Normalized magnitude [-]" 과 로그 눈금 10⁰ · 10⁻² · 10⁻⁴ · 10⁻⁶ 의 "10" 이 잘려 "0 · -2 · -4 · -6" 조각만 남음 → **수동 `fig_4_manual_p7.png`**(전폭).
- **fig_8 왼쪽 잘림** — 맨 왼 패널 y 축 이름 "s_n(0) [−]" 과 눈금 앞자리가 잘림(벡터 x 41.0 pt ↔ bbox 58.9 pt) → **수동 `fig_8_manual_p9.png`**.
- **tab_1 · tab_2 바이트 동일**(md5 `ad1c19ee…`) — 둘 다 **p. 3 쪽 전체**(bbox [32.6, 31.3, 563.3, 750.1]: 표 1 · 표 2 · 2.1 절 끝 · 2.2 절 · 식 16 · 17) · tab_2 캡션 필드에 표 2 본문(기호 · 단위)이 섞임(649 자) → **수동 `tab_1_manual_p3.png` · `tab_2_manual_p3.png`**.
- **tab_3 쪽 전체**(p. 4 — 표 3 + 2.2 절 끝 · 3 · 3.1 절) · 캡션 필드에 표 본문 섞임(233 자) → **수동 `tab_3_manual_p4.png`**.
- **tab_4 쪽 전체**(p. 9 — 그림 8 · 4.4 절 · 표 4 · 4.5 절 머리) → **수동 `tab_4_manual_p9.png`**.
- 나머지(fig_1 · 2 · 3 · 5 · 6 · 7) 라벨 · 내용 온전 · 과대 0 · 캡션 필드 깨끗(fig_6 은 캡션 자체가 493 자).

**18 장 전부 직접 봤다 — 안 본 그림 · 표 0.** (그림이 아닌 래스터 — p. 1 저널 로고 · 표지 · crossmark — 는 열지 않았다.) 판독: 그림 2 · 3 · 4 · 5 · 6 · 7 · 8 은 **벡터 경로**(곡선 꼭짓점 · 상자 그림의 상자 · 중앙값 선 · 참값 표지 · 줄기 끝 · 축 눈금)를 축으로 보정해 읽었다(판독 · 재현 코드 · 중간 렌더는 `scratchpad` 에만 · 커밋 안 함).

## Fig. 1 — DFN 모식 (p. 2 · 봤다) ★ 모형 정의

음극(입자 셋) · 분리막 · 양극(입자 둘 · 반경 `R_s`) · `δ_n` · `δ_p` · `x = 0 … L` · 충전 중 Li⁺ 이동(전해질 수평 화살 · 입자 안 화살) · 양 끝 전자. 캡션 "where the depicted cell is being charged". 모형 그림일 뿐 수치 0.

## Fig. 2 — 평형 전위 보정 (p. 5 · 봤다 · 벡터 판독) ★★★★ (c)

x = "SOC Cell [-]" 0–1 · 왼축 U_n 0–1.5 V · 오른축 U_p 3.4–4.4 V · 곡선 여섯: **Measured U_n**(검정 실선 — [24]) · **Assumed U_n**(검정 파선 — [23] 흑연) · **Corrected U_n**(검정 점선) · **Measured U_p**(빨강 실선 — [24]) · **Calculated U_p**(빨강 파선 — 경우 1: EMF + 가정 U_n) · **Corrected U_p**(빨강 점선). `[도표·벡터]`:

| SOC | 측정 U_n | 가정 U_n | 보정 U_n | 측정 U_p | 계산 U_p | 보정 U_p |
|---|---|---|---|---|---|---|
| 0 | 0.803 | 1.239 | 0.929 | 3.565 | 3.883 | 3.573 |
| 0.02 | 0.418 | 0.586 | 0.452 | 3.575 | 3.718 | 3.584 |
| 0.05 | 0.279 | 0.360 | 0.292 | 3.585 | 3.668 | 3.600 |
| 0.10 | 0.206 | 0.224 | 0.230 | 3.612 | 3.622 | 3.628 |
| 0.30 | 0.118 | 0.164 | 0.164 | 3.723 | 3.766 | 3.766 |
| 0.50 | 0.108 | 0.130 | 0.130 | 3.836 | 3.855 | 3.855 |
| 0.70 | 0.078 | 0.117 | 0.117 | 4.007 | 4.045 | 4.045 |
| 0.90 | 0.068 | 0.089 | 0.089 | 4.184 | 4.196 | 4.196 |
| 1.00 | 0.039 | 0.090 | 0.090 | 4.250 | 4.293 | 4.293 |

- 계산 U_p 의 최솟값 **SOC 0.0994 · 3.622 V** — 그 아래로 SOC 0 까지 **+0.26 V 오른다**(3.883 V) = 인쇄 "around 10% SOC, the calculated U_p rises significantly" ✅.
- 보정 U_p 는 SOC 0 → ≈0.094 직선(기울기 **0.545 V/SOC** · 절편 3.573 V) ↔ 인쇄 규칙 "mean of the slope of the calculated U_p curve between 10% and 40% SOC" 대로면 **0.564 V/SOC**(끝점 · 국소 기울기 평균 둘 다) — 3 % 얕고, 이음점에서 보정 U_p 가 계산 U_p 보다 6 mV 위(SOC 0.1) · 규칙대로 계산 U_p(0.1) 에서 그으면 SOC 0 에서 3.566 V ↔ 그림 3.573 V(7.5 mV) — **대체로 맞음(±8 mV)**.
- **(계산 U_p − U_n 가정) ≡ (보정 U_p − U_n 보정)** 전 구간(0.1 mV 안) — 보정은 EMF 를 정확히 보존한다(정의) ✅.
- ★ **(계산 − 측정) U_p ≈ (가정 − 측정) U_n** ±0.01 V — SOC 0.1–1 에서 U_p 쪽 **+6 … +54 mV(평균 +26 · rms 29)** · U_n 쪽 +13 … +53 mV(평균 +30) · 보정은 0–10 % 만 바꾸므로 이 오프셋은 그대로 남는다(§(c) 3).
- ★ **측정 전극 쌍 EMF(U_p − U_n · [24]) − 이 그림의 EMF** = SOC 0.03–1 에서 **−9.5 … +13.5 mV** · 0.1–1 rms 5.8 mV · SOC 0 에서 +118 mV(§(c) 4).
- 측정 U_n([24] — 참고문헌 제목 "silicon-graphite")은 SOC ≈0–0.1 에서 0.80 → 0.21 V 로 가파르게 내려오고 0.1 위에서는 가정 흑연 곡선보다 13–53 mV 낮다 — `[해석]` 가정 곡선의 SOC 사상(창)이 인쇄되지 않아(G4) 이 차를 Si 몫으로 읽을 수 없다.

## Fig. 3 — 실험 자료 (p. 6 · 봤다 · 벡터 판독) ★★★ (d)

패널 아홉: **EMF**(Cell 1 검정 · Cell 2 빨강 vs SoC 0–1) · **Cell 1 data 1 (estimation)** 전류 · 전압(0–56.7 분) · **data 2 (validation)**(0–150 분) · **data 3 (validation)**(0–158.3 분) · **Cell 2 data (estimation/validation)**(0–28.3 분). `[도표·벡터]` · `[재현·벡터]`:

| 자료 | 길이 | 전류 범위 | 순 전하(적분) | 시작 · 끝 전압 |
|---|---|---|---|---|
| Cell 1 data 1 | 56.67 분 | −24.6 … +11.0 A(평균 −8.27 · RMS 9.48) | **−7.81 Ah**(충 0.09 · 방 −7.90) | 4.112 → 3.421 V |
| Cell 1 data 2 | 150.0 분 | −13.2 … +11.6 A(평균 −3.10) | **−7.75 Ah** | 4.133 → 3.494 V |
| Cell 1 data 3 | 158.3 분 | −21.0 … +9.3 A(평균 −2.80) | **−7.38 Ah** | 4.138 → 3.580 V |
| Cell 2 data | 28.33 분 = **1,700 s** | −5.79 … +2.62 A(평균 −1.07) | **−0.507 Ah** | 4.190 → 3.907 V |

- EMF: Cell 1 SoC 0 → 1 = 2.700 → 4.179 V · Cell 2 2.332 → 4.168 V.
- ★ Cell 1 세 자료의 시작 전압(전류 0)이 그림 6 의 시작 SoC 에서 읽은 Cell 1 EMF 와 **±4 mV** 안(4.112 ↔ 4.113 · 4.133 ↔ 4.137 · 4.138 ↔ 4.141) — 그림 3 의 EMF 눈금 보정이 맞다는 독립 확인.
- ⚠ Cell 2: 시작 전압 4.190 V(전류 0)가 이 그림의 Cell 2 EMF 최댓값(4.168 V @ SoC 1)보다 높고, **그림 2 의 EMF 보다 SOC 0.2–1 에서 21–59 mV · ≤0.1 에서 113–313 mV 낮다**(§(c) 5 · D2).

## Fig. 4 — 감도 순위 (p. 7 · 봤다 · 자동은 왼쪽 잘림 → 수동 전폭 · 벡터 판독) ★★★★ (a)

y = "Normalized magnitude [-]"(로그 · 10⁰ … 10⁻⁶ — 수동 판에서 확인) · x = Ranking 1–22 · 패널 Cell 1 · Cell 2 · 줄기 + 원 표지 + 매개변수 이름. 줄기 끝 = 값(순위 1 이 10⁰ 격자선에 정확히 닿음). `[도표·벡터]` log₁₀ 값:

| 순위 | Cell 1 | log₁₀ | Cell 2 | log₁₀ |
|---|---|---|---|---|
| 1–3 | p̂_n · p̂_p · R̂_f,n | 0 · −0.86 · −0.97 | p̂_n · p̂_p · D̂_e | 0 · −0.81 · −1.03 |
| 4–6 | D̂_e · D̂_s,p · **s100,n** | −1.50 · −1.60 · −1.69 | D̂_s,p · ε̂_e,p · **s100,n** | −1.06 · −1.61 · −1.65 |
| 7–9 | ε̂_e,p · D̂_s,n · k̂_0,n | −2.06 · −2.37 · −2.43 | R̂_f,n · ε̂_e,n · D̂_s,n | −1.91 · −2.18 · −2.40 |
| 10–12 | ε̂_e,n · κ̂ · **s100,p** | −2.53 · −2.70 · −2.98 | κ̂ · **s100,p** · k̂_0,n | −2.58 · −2.86 · −3.00 |
| 13–15 | k̂_0,p · t₊⁰ · **s0,n** | −3.37 · −3.44 · −3.64 | t₊⁰ · k̂_0,p · σ̂_p | −3.22 · −3.31 · −3.48 |
| 16–18 | **s0,p** · σ̂_p · R̂_cc | −3.77 · −3.79 · −4.00 | p̂_sep · ε̂_e,sep · R̂_cc | −3.67 · −3.87 · −3.99 |
| 19–21 | α · p̂_sep · ε̂_e,sep | −4.08 · −4.17 · −4.29 | **s0,p** · α · **s0,n** | −4.04 · −4.11 · −4.40 |
| 22 | σ̂_n | −6.20 | σ̂_n | −6.46 |

- 순위가 본문 지시와 맞다: Cell 1 순위 5 = D̂_s,pos · 6 = s100,n · 8 = D̂_s,n(§4.4 "parameter 6 (s100,n) and 8 (D̂s,n)" · "parameter 5 (D̂s,pos)") ✅.
- ★ 창 넷: `s100,n` 6 위(두 셀) · `s100,p` 12 · 11 위 · **`s0,n` · `s0,p` 15 · 16 위(Cell 1) · 21 · 19 위(Cell 2)** — "12 개 추정" 에서 **0 % 끝 둘은 빠지고 β 0.5(범위 가운데)에 고정**된다(§3.4).
- `[재현]` 피벗 QR 에서 `σ_max(S) ≥ |r₁₁|` · 앞 k 열 블록의 `σ_min ≤ |r_kk|` ⇒ **cond(S_k) ≥ |r₁₁|/|r_kk|** — 고른 12 개 ≥10^2.98 · 10^3.00 · 22 개 ≥10^6.20 · 10^6.46(β 좌표 · 계산점 미인쇄).

## Fig. 5 — 추정 매개변수 수 · 자료 길이 (p. 7 · 봤다 · 벡터 판독) ★★★★ (b) · (d)

(a) RMSE [mV] vs 추정 매개변수 수 1–22(Cell 1 Data 1 · 2 · 3 / Cell 2 Estimation · Validation) · (b) RMSE vs 추정에 쓴 자료 %(Cell 1 10–100 % — Data 1 비율을 바꿈 · Cell 2 10–100 %). `[도표·벡터]`:

| (a) 매개변수 수 | 1 | 4 | 8 | 12 | 14 | 15 | 22 |
|---|---|---|---|---|---|---|---|
| Cell 1 Data 1 | 15.69 | 10.72 | 5.34 | **3.50** | 3.50 | 3.54 | 3.54 |
| Cell 1 Data 2 | 10.15 | 8.24 | 6.06 | 3.68 | 3.39 | 3.53 | 3.59 |
| Cell 1 Data 3 | 17.94 | 8.76 | 7.79 | 4.22 | 3.95 | 3.99 | 3.88 |
| Cell 2 추정 | 25.49 | 9.19 | 5.74 | 4.24 | 4.04 | 4.03 | 3.57 |
| Cell 2 검증 | 26.19 | 8.67 | 6.42 | 4.44 | **4.16** | **4.60** | 3.78 |

| (b) 자료 % | 10 | 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|
| Cell 1 Data 1 | 5.71 | 5.25 | 4.22 | 4.76 | 5.16 | 3.68 | 3.50 | 3.50 | 3.42 | **3.18** |
| Cell 1 Data 2 | 3.58 | 3.99 | 3.52 | 3.58 | 3.84 | **3.38** | 3.39 | 3.42 | 3.42 | **3.84** |
| Cell 1 Data 3 | 4.20 | 4.01 | 3.83 | 3.84 | 3.90 | **3.77** | 3.95 | 4.03 | 4.06 | **4.84** |
| Cell 2 | 14.2 | 15.8 | **24.4** | 23.3 | 19.6 | 10.1 | 4.05 | — | 4.00 | 3.89 |

(Cell 2 꼭짓점은 10 · 20 · 30 · 40 · 50 · **55**(15.7) · 60 · **65**(**5.0**) · 70 · **75**(4.03) · 90 · **95**(3.99) · 100 % — 80 · 85 % 점은 없다.)
- 인쇄 "after about 12 parameters the RMSE for all data sets does not significantly change" ✅ · "the validation RMSE with 14 estimation parameters is lower than with 15" ✅(4.16 ↔ 4.60).
- ★ "과적합" 근거(90 → 100 %): Data 1 −0.24 · Data 2 **+0.42** · Data 3 **+0.78 mV** — 같은 곡선의 다른 요동(Data 1 30 → 40 % +0.54 · 40 → 50 % +0.40 · Data 2 10 → 20 % +0.41 mV)과 같은 크기. 검증 두 자료는 **60 % 에서 가장 작다**(3.38 · 3.77) — 고른 90 % 는 3.42 · 4.06.
- ★ Cell 2 는 **10 %(14.2) < 30 %(24.4)** — 자료를 늘렸는데 나빠지는 구간(본문 무언급 · 저자 "non-convex … multiple local minima" 와 양립).
- 그림 5(b) 의 추정 매개변수 수는 인쇄 0 — 그림 6 과 점 값이 같아 **14 개**로 읽힌다(G9 · 아래).

## Fig. 6 — 출력 오차 (p. 8 · 봤다 · 벡터 판독) ★★★ (d)

위: Cell 1 `V_meas − V_sim` [mV] vs SoC(Data 1 · 2 · 3 — 캡션 "60% of Data 1 … with 14 estimated parameters") · 아래: Cell 2 vs Time [s] 0–1,700 — "Estimated parameters from using 30 % of the data" · "… 65 % …" · "**Parameters from Sturm et al (2019)**". `[도표·벡터]` · `[재현·벡터]`:

- 위: SoC 범위 Data 1 0.2138–0.9547 · Data 2 0.2411–0.9727 · Data 3 0.2660–0.9757 · RMS **3.69 · 3.42 · 3.71 mV** = 그림 5(b) 60 % 점 3.68 · 3.38 · 3.77 ✅ · Data 1 은 SoC 0.21–0.24 에서 ±21 mV(SoC ≥0.25 만이면 RMS 2.67) — 인쇄 "for Data 1 there are significantly larger errors at the beginning, between 0.2 and 0.25 SoC" 의 "beginning" 은 **축의 왼끝**(방전 자료의 **시간상 끝**).
- 아래: 30 % 추정 RMS **24.4 mV**(= 그림 5(b) 24.38 ✅ · 0–510 s 2.3 · 800–1,700 s 33.3 · 1,105–1,700 s 38.9 · 최대 +68.9 @ ≈1,120 s) · 65 % **5.0 mV**(= 4.99 ✅) · **Sturm 2019 매개변수 RMS 40.4 · 평균 −37.4 · 최대 +0.2 mV — 전 구간 음수**(동적 몫 √(40.4² − 37.4²) ≈15 mV · t = 0 에서 ≈0).
- ⚠ 캡션 "**60%** of Data 1 for **simulation**" ↔ 본문 4.2 절 "only **90%** of Data 1 has been used for estimation"(D4) · "for simulation" 은 추정의 오기로 읽힌다.

## Fig. 7 — 추정 매개변수의 산포 · 정확도 (p. 8 · 봤다 · 벡터 판독) ★★★★ (a) · (d)

y = "Normalized parameter value β [-]" · x = 매개변수 식별자 1–22(그림 4 순위 — Cell 1) · 패널 여섯: **Cell 1**(β 0–1) · **Cell 1 increased range**(β −0.3 … 1.3) · **Synthetic cell** · **Synthetic cell with a nonlinearity in D_s,pos** · **Synthetic cell with an error in the EMF** · **Synthetic cell with both modifications** · 상자(IQR) · 중앙값(빨강) · 수염 · 이상치(+) · 참값(파란 원 — 합성 넷). 각 패널 50 회차(인쇄). `[도표·벡터]`(β 중앙값 · 참값):

| # | 이름 | Cell 1 | 확장 | 합성 | 비선형 | EMF | 둘 다 | 참값 |
|---|---|---|---|---|---|---|---|---|
| 1 | p̂_n | 0.37 | 0.42 | 0.52 | **0.95** | 0.50 | **0.98** | 0.39 |
| 2 | p̂_p | 0.33 | 0.39 | 0.54 | 0.56 | 0.69 | 0.53 | 0.40 |
| 3 | R̂_f,n | **0.01** | 0.03 | 0.50 | 0.43 | **0.04** | 0.21 | 0.58 |
| 4 | D̂_e | 0.08 | −0.05 | 0.57 | 0.51 | 0.21 | 0.17 | 0.78 |
| 5 | D̂_s,p | 0.13 | 0.22 | **0.113** | 0.044 | 0.22 | 0.114 | **0.111** |
| 6 | s100,n | **1.00** | 1.05 | 0.36 | 0.35 | 0.34 | 0.69 | 0.34 |
| 7 | ε̂_e,p | 0.87 | 0.70 | 0.20 | 0.00 | 0.21 | 0.25 | 0.17 |
| 8 | D̂_s,n | **0.015** | 0.03 | 0.26 | 0.74 | 0.93 | 0.97 | 0.37 |
| 9 | k̂_0,n | 0.80 | 0.87 | 0.42 | 0.40 | 0.41 | 0.24 | 0.35 |
| 10 | ε̂_e,n | **0.00** | −0.20 | 0.00 | 0.78 | 0.34 | 0.99 | 0.02 |
| 11 | κ̂ | 0.65 | 0.65 | 0.59 | 0.90 | 0.80 | 0.91 | 0.96 |
| 12 | **s100,p** | **0.99** | 0.77 | 0.73 | **0.00** | **0.03** | **0.00** | **0.90** |
| 13 | k̂_0,p | **0.99** | 0.91 | 0.70 | 0.39 | 0.06 | 0.32 | 0.82 |
| 14 | t₊⁰ | **0.00** | −0.28 | 0.09 | 0.75 | 0.00 | 0.93 | 0.10 |
| 15 | s0,n | **0.02** | 0.13 | 0.34 | 0.11 | 0.00 | 0.11 | 0.49 |
| 16 | s0,p | 0.13 | 0.86 | 0.64 | 0.24 | 0.91 | 0.37 | 0.49 |
| 17 | σ̂_p | 0.84 | 0.94 | 0.71 | 0.37 | 0.54 | 0.56 | 0.94 |
| 18 | R̂_cc | **0.01** | −0.04 | 0.40 | 0.39 | 0.37 | 0.23 | 0.06 |
| 19 | α | 0.66 | 0.12 | 0.09 | 0.39 | 0.38 | 0.79 | 0.24 |
| 20 | p̂_sep | 0.82 | 0.69 | 0.50 | 0.54 | 0.16 | 0.65 | 0.24 |
| 21 | ε̂_e,sep | **0.00** | −0.10 | 0.44 | 0.37 | 0.74 | 0.80 | 0.04 |
| 22 | σ̂_n | 0.68 | 0.72 | 0.53 | 0.10 | 0.45 | 0.44 | 0.13 |

- ★ **Cell 1 중앙값이 범위 끝(±0.02) 10/22**(Cell 1 열의 굵게 — 다른 열의 굵게는 본문 강조) — 창 넷 중 셋(s100,n β 1.00 → s 0.890 · s100,p 0.99 → 0.437 · s0,n 0.02 → 0.002). 확장 범위에서 중앙값이 [0, 1] 밖 6/22 · IQR 이 원 범위 끝을 넘는 것 14/22.
- ★ **합성(무잡음 · 같은 모형)에서도 참값이 IQR 밖 14/22**(첫 10 중 6 — #1 · 2 · 3 · 4 · 8 · 9) · 첫 9 개 |중앙값 − 참값| 평균 0.088 · IQR 중앙값 0.12(나머지 0.37). 수정 셋: 참값 IQR 밖 17 · 17 · 16/22.
- ★ **#12 s100,p**: 참값 β 0.90(s 0.418) ↔ 중앙값 합성 0.73(0.381) · **비선형 0.00 · EMF 0.03 · 둘 다 0.00(= 사전 범위 하한 s 0.22)**.
- #5 D̂_s,p 는 합성에서 참값 0.111 ↔ 0.113(인쇄 "the most identifiable parameter" ✅) — 그러나 그것을 비선형으로 만든 패널에서는 0.044(편향).
- ⚠ "**Synthetic cell with both modifications**" 패널은 본문 · 표 4 에 따로 서술되지 않는다(D5) · 본문 "especially for the first 10 parameters, the estimated parameters are close to the true parameters" ↔ 첫 10 중 6 이 참값을 IQR 밖에 둔다(D6).

## Fig. 8 — 상태의 상하한 (p. 9 · 봤다 · 자동은 왼쪽 잘림 → 수동 전폭 · 벡터 판독) ★★★ (d)

위 줄 **Synthetic cell** · 아래 줄 **Synthetic cell with both modifications** · 패널 `s_n(0) [−]` · `s_p(L) [−]` · `φ_s(0) − φ_e(0) [V]` · `c_e/c_e,0 [−]` · 빨강 = x = 0 상태의 50 회차 상하한 · 파랑 = x = L · 검정 파선 = 참값. `[도표·벡터]`:

- 시간 축 **0–76.7 분**(눈금 0 · 20 · 40 · 60 — 25.8 pt/20 분 · 곡선이 축 끝까지) ⚠ 맨 왼 패널만 "**Time [s]**" · 나머지 "Time [min]"(D7) · 합성 입력이 "the same input data"(Data 1 = 56.7 분)라면 길이가 안 맞는다(D7).
- 위 줄: 참값이 띠 안(인쇄 ✅) · `s_p(L)` 띠 t = 0 [≤0.335(축 잘림), 0.461] ↔ 참값 0.441 · `c_e/c_e,0`(x = L) 띠 최저 ≈0.81 ↔ 참값 0.84.
- 아래 줄: `s_p(L)` 띠 **t = 0 [≤0.249(축 잘림), 0.335] ↔ 참값 0.440**(띠 위끝도 0.105 아래) · 끝 [0.721, 0.798] ↔ 0.806 · `c_e/c_e,0`(x = L) 띠 최저 **≤0.54(축 잘림) ↔ 참값 최저 0.84** · `s_n(0)` 시작 ≈0.80–0.83 ↔ 참값 ≈0.76 · `φ_s − φ_e` 는 띠가 참값을 덮는다.
- 인쇄 "the estimated s_p and c_e in the positive electrode deviate substantially from their respective true states" ✅ · "the constraint would be activated conservatively, since the estimated positive electrode c_e varies much more in magnitude than the true c_e" ✅.

## Table 1 — 원 식 ↔ 재매개화 식 (p. 3 · 봤다 · **수동** — 자동은 쪽 전체) ★★★★ (a)

(1a)–(7) 원 DFN(고체 확산 · 전해질 확산 · 고체 전위 · 전해질 전위 · BV · i₀ · 표면 농도 · 과전압 · 단자 전압 · **최대 가역 용량 제약 (7) `Q = AFδ_i ε_s,i c^max_s,i (s_i,100% − s_i,0%)`**) ↔ (8a)–(14) 재매개화(`r̂ ∈ [0, 1]` · `x̂ ∈ [0, 3]` · **(14) `3Q = ĉ^max_s,i (s_i,100% − s_i,0%)`**). 읽은 것:
- **(12a) `ĵ_n = î₀(exp(α_aFη/RT) − exp(−(1−α_a)Fη/RT))`** · **(12b) `î₀ = k̂₀ ĉ_e^α_a (ĉ^max_s − ĉ_s,e)^α_a ĉ_s^(1−α_a)`** — 원 (5a) · (5b) 의 `α_c` 자리에 `1 − α_a`(본문 언급 0 · D9) · (12b) 끝 인자가 `ĉ_s,e` 아닌 `ĉ_s`(표기).
- **(9a) `ε̂_e ∂ĉ_e/∂t = ∂/∂x̂(D̂_e p̂ ∂ĉ_e/∂x̂) + ĵ_n`** · **(11a) `∂/∂x̂(κ̂p̂ ∂φ_e/∂x̂ + κ̂p̂(t₊⁰ − 1)(2RT/F) ∂ln ĉ_e/∂x̂) = −ĵ_n`** — `D̂_e` · `κ̂` 는 `p̂` 와의 곱으로만(§(a) 3).
- (7) 은 양극에서 `s_p,100% < s_p,0%` 라 우변이 음수 — 절댓값 표기 0(표기 · D10).

## Table 2 — 기호 (p. 3 · 봤다 · **수동**) ★★ (a)

기호 · 설명 · 단위 + 각주 a "Considered parameters of the DFN model" · b `k₀` 단위 [C/s·(m/mol)^(1+3α_c)]. `[재현]` "a" 표시 **34**(c_e,0 · c^max 둘 · D_e · D_s 둘 · k₀ 둘 · L · p 셋 · R_cc · R_f 둘 · R_s 둘 · s 넷 · t₊⁰ · α_a · α_c · δ 둘 · ε_e 셋 · ε_s 둘 · κ · σ 둘) + 표시 없는 **A** = 본문 35. ⚠ 단위: `D_e` "**[m²]**" · `D_s` "**[m/s]**"(둘 다 m² s⁻¹ 이어야 — D11).

## Table 3 — 재매개화 매개변수 24 (p. 4 · 봤다 · **수동**) ★★★★ (a)

| 매개변수 | 묶음 | 범위 `[인쇄]` | 척도 `[재현]` |
|---|---|---|---|
| Q | Q | N/A [C] | 측정 |
| s_n,0% · s_p,0% · s_n,100% · s_p,100% | 그대로 | [0.002, 0.04] · [0.86, 0.97] · [0.75, 0.89] · [0.22, 0.44] | 로그 · 선형 · 선형 · 선형 |
| D̂_s,n · D̂_s,p | D_s/R_s² | [0.00013, 0.0016] · [0.0004, 0.63] s⁻¹ | 로그 · 로그 |
| D̂_e | D_e F A c_e,0/(1 − t₊⁰) | [4.1·10⁻⁷, 7.9·10⁻⁶]Q [C s⁻¹] | 로그 |
| p̂_n · p̂_p · p̂_sep | ε_e^p/δ · ε_e,sep^p/(L − δ_n − δ_p) | [50, 5700] · [58, 4100] · [3700, 31000] [–] | 로그 · 로그 · **선형** |
| t₊⁰ | t₊⁰ | [0.26, 0.38] | 선형 |
| σ̂_n · σ̂_p · κ̂ | σε_s A/δ · κA | [1.2, 170]Q · [0.011, 8.3]Q · [7·10⁻⁶, 2·10⁻⁵]Q [Ω⁻¹] | 로그 · 로그 · **선형** |
| R̂_f,n · R̂_f,p · R̂_cc | R_f R_s/(3Aδε_s) · R_cc/A | [20, 330]/Q · **[0, 0]/Q** · [32, 170]/Q [Ω] | 로그 · 고정 · 선형 |
| α_a | α_a | [0.48, 0.52] | 선형 |
| k̂_0,n · k̂_0,p | k₀c_e,o^α_a/(R_s F) | [5.7·10⁻⁵, 0.00078] · [7.9·10⁻⁵, 0.001] | 로그 · 로그 |
| ε̂_e,n · ε̂_e,p · ε̂_e,sep | ε_e F A δ c_e,o/(1 − t₊⁰) | [0.017, 0.76]Q · [0.01, 0.14]Q · [0.0049, 0.083]Q [C] | 로그 · 로그 · 로그 |

`[재현]` 범위 비 > 10 → 로그 **14** · 선형 **8** · 고정 1(R̂_f,p) + Q 측정 = 24. ⚠ `p̂` 단위 "[–]" ↔ `ε^p/δ` 는 m⁻¹(그래서 `D̂_e` 의 C s⁻¹ · `κ̂` 의 Ω⁻¹ 도 실제로는 · m 가 붙는다 — 곱 `D̂_e p̂` · `κ̂ p̂` 만 표기와 맞다 · D11).

## Table 4 — 합성 시험 요약 (p. 9 · 봤다 · **수동**) ★★★★ (d)

| 중앙값 | Synthetic cell | Nonlinearity in D̂_s,pos | Error in EMF | Random parameters |
|---|---|---|---|---|
| RMSE V_est − V_true | 0.13 | 1.19 | 1.17 | 36.2 |
| RMSE β_est,22 − β_true | 0.30 | 0.43 | 0.44 | 0.43 |
| RMSE β_est,9 − β_true | 0.14 | 0.22 | 0.34 | 0.38 |

단위 인쇄 0(본문 "approximately 1.2 mV" — mV 로 읽힘). `[재현]` 무작위 β(균등 [0, 1]) ↔ 그림 7 참값의 기대 RMS **0.427 · 첫 9 개 0.36**(Monte Carlo 중앙값 0.425 · 0.358) — 표 "Random parameters" 0.43 · 0.38 ✅(그림 7 참값 판독 · "Random" 의 정의도 함께 확인). "Both modifications" 열은 없다(D5).

## 본문 서술과 어긋난 그림 (요약)

- **그림 2 ↔ 그림 3** — 그림 2 의 EMF 가 그림 3 의 Cell 2 EMF 보다 21–59 mV(SOC 0.2–1) 높다 · 본문 "calculated from the EMF function shown in Fig. 3"(D2).
- **그림 6 캡션 "60% … for simulation"** ↔ 본문 90 % 추정(D4).
- **그림 7 "both modifications" 패널** ↔ 본문 · 표 4 무서술(D5) · "first 10 … close to the true" ↔ 첫 10 중 6 이 IQR 밖(D6).
- **그림 8 시간 축 76.7 분 · 첫 패널 "Time [s]"** ↔ Data 1 56.7 분 · "the same input data"(D7).
- **그림 2 보정 직선 기울기 0.545** ↔ 규칙 0.564(−3 % — 판독 폭 밖이나 작다).

---

# 절별 해체 (본문)

## Highlights · 초록 (p. 1)

강조문 다섯은 §(b) 표에 원문 그대로. 초록 `[인쇄]`: "Using electrochemistry-based battery models in battery management systems remains challenging due to the difficulty of **uniquely determining all model parameters**. This paper proposes a model parameterization approach of the Doyle–Fuller–Newman (DFN) model, by first reparameterizing the DFN model through normalization and grouping, followed by a sensitivity analysis and a parameter estimation procedure." · "the model with parameters obtained using the proposed parameterization approach is compared to a model whose parameters have been obtained using cell teardown" · "the consistency and accuracy of the parameter estimation procedure is analyzed by applying the estimation routine to a **synthetic cell**, represented by a DFN model with randomly chosen parameters" · "the parameter estimation approach using current/voltage data can lead to a significantly better output accuracy, while it **might not lead to physically meaningful parameters**. This motivates the need for an approach that combines both and where cell tear-down can assist the parameter estimation". `[해석]` 초록이 이미 "출력 정확도 ↔ 물리 의미" 를 가른다 — 이 편의 결론 문장들이 유일성 대신 **출력**을 잣대로 쓴다는 것을 저자가 알고 쓴다.

## 1. Introduction (p. 1–2)

- 동기: BMS 의 SOC · SOH · 급속 충전에 등가회로 대신 전기화학 모형 — 그러나 "many parameters need to be determined". 단순 모형(SPM [10])의 시간 영역 매개변수화 [11–16] · 선형 주파수 영역 [17](⚠ [13] Bizeray = 28호는 주파수 영역 전달함수 편인데 "time domain [11–16]" 목록에 든다 — `[해석]` 분류 느슨함) · DFN 매개변수화 [18–27] · 효율 구현 [28, 29].
- 정하는 길 셋: 제조사 정보 · **분해(teardown) + 실험 [23, 24, 26]** · 입출력 추정 [18–22, 27]. 추정은 다시 둘: 동시 추정 [18, 19, 21, 27] — `[인쇄]` "**Since the identifiability of the DFN model is poor [19]**, a sensitivity analysis can be done to determine the parameters to which the model output is most sensitive, in order to select a smaller set of parameters for estimation [18]" / 실험 설계로 묶음별 추정 [14, 20, 22] — `[인쇄]` "often, there is no justification given for this approach [14,20], or the approach is justified with the intuition that identifying too many parameters simultaneously may lead to unexpected uncertainty and errors [22]. However, this intuition has not yet been verified."
- 이 편의 위치 `[인쇄]`: 감도 분석은 [18](Jin 2018 — [30] 절차를 **묶지 않은** DFN 에) 와 같고, 정규화 · 묶음은 [25, 31](Jobman 2015 · Chu 2019 — 감도 분석 없음) 과 같다 — **둘을 합친 편**. 두 경우(전극 평형 전위를 앎 — 자료 하나 / 셀 EMF 만 — 자료 셋) · 추정 수 · 자료 길이 · 합성 셀.

## 2. Battery modeling (p. 2–4)

### 2.1 DFN equations (p. 2–3 · 표 1(a) · 표 2)

식 (1)–(6) 은 [28](자기 툴박스)의 정식화 · **(7) 최대 가역 용량 제약 `Q = AFδ_i ε_s,i c^max_s,i (s_i,100% − s_i,0%)`** 추가 · U 는 표면 농도의 사전 함수 · 영역별 매개변수(식 15). `[인쇄]` "the total number of parameters of the DFN model as formulated in Table 1(a) amounts to **35**. Note that depending on how the DFN model is formulated, and what kind of assumptions are made, this number can vary." · R_f 와 R_cc 를 **둘 다** 둔 이유 `[인쇄]` "as both these parameters can be linked to a physical phenomenon, we consider both of these effects … as having separate parameters, in order to study the sensitivity of the output to these parameters" — `[해석]` 둘 다 옴형 전압 강하라 **서로 거의 평행한 열**이 될 것이 예상되는 쌍을 일부러 넣었다(그림 4 Cell 1: R̂_f,n 3 위 ↔ R̂_cc 18 위 — 직교화 순위가 뒤쪽을 눌렀다).

### 2.2 Parameter normalization and grouping (p. 3–4 · 표 1(b) · 표 3)

- 원리 `[인쇄]`: "the variation of certain parameters leads to the same physical effect. For example, by decreasing the diffusion coefficient D_s and increasing the particle size R_s accordingly, the diffusion dynamics in the solid phase remain unchanged. Thus, intuitively speaking, this means that one of these parameters is **redundant**" → `r̂ = r/R_s`, `D̂_s = D_s/R_s²` · `x̂`(식 16 — 영역마다 0–1 · 1–2 · 2–3) · 변수 재정의(식 17) `ĵ_n = 3ε_sFAδ_i j_n/R_s` · `ĉ_e = c_e/c_e,o` · `ĉ_s/3 = ε_sFAδ_i c_s`.
- 결과 `[인쇄]`: "**The total number of parameters of the reparameterized model is 24.** While the total number of parameters of the reparameterized model presented in [25] is also 24, it has to be considered that we have an additional parameter (R_cc), and in [25] a further assumption is made that α_a = α_c = 0.5 … Thus, the reparameterized model proposed here has effectively two parameters less." · 차이 둘: [25] 는 유효 계수(`D_e^eff = D_eε_e^p`)를 원 매개변수로 · 이 편은 비유효 계수 → "an effectively lower amount of parameters" · 제약 (7) 로 `c^max` 둘을 Q 에서 정함 → 하나 더 줄임.
- `[해석]` 문장에 없는 축소 하나: 표 1(b) 의 `α_c → 1 − α_a`(§(a) 3).

## 3. Model parameterization approach (p. 4–6)

### 3.1 Equilibrium potential model (p. 4–5 · 그림 2)

`U_EMF(s_c) = U_p(s_p) − U_n(s_n)`(18a) · `s_i = ĉ_s/ĉ^max_s,i`(18b) · 창 넷 + U_n · U_p + Q = 평형 모형. 핵심 `[인쇄]`: "**while the same EMF-SOC relation can be reached with any choice between 0 and 1 for the parameter values of s_n,0%, s_n,100%, s_p,0%, s_n,100%, these parameters also affect the dynamics of the cell through the (ĉ_s,max − ĉ_s,e)^α_a term in (12b). Therefore, these parameters should be considered in the parameter estimation routine, rather than assuming their values from literature**" · "in principle, the equilibrium potential curves of the electrodes cannot be determined individually from input/output data". 경우 둘 — (1) 분해 불가: 문헌 U_n 을 가정하고 U_p 를 EMF 로 정의("Since the negative electrode is generally the same or similar (usually a graphite-based composite) across different types of battery chemistries, and the negative electrode equilibrium potential U_n is relatively small compared to U_p, we propose to take U_n from literature") · (2) 분해 가능: 전극 곡선을 화학량론에 대해 재고 창을 "such that the difference between the measured U_p−U_n and the measured U_EMF is minimized in some way [23,24,26]". 경우 1 을 권하는 이유 `[인쇄]`: "since the EMF can vary even between individual cells that were made in the same factory … Deviations of the modeled EMF from the measured EMF can significantly impact the identifiability of the model parameters, as also shown in [13]. Therefore, even if the chemistry of the electrode materials is known, it may still be preferable to use the approach described in the first case". 보정(그림 2)은 §(c).

### 3.2 Ranges of the grouped parameters (p. 5 · 표 3 · 식 19)

`[인쇄]` "These parameter ranges have been obtained by gathering a set of values for each of the parameters from various papers, i.e., [23,24,26,35–37], where **largely actual measurements** have been done … (rather than using parameter estimation techniques)" · 용량 관련 인자(A · L · ε_s)를 품은 묶음은 **Q 로 척도**(표 3 표지 a) · "**the range of R̂_f,p is [0, 0]**, since we could not find any non-zero values for R̂_f,p in the prior-mentioned literature" · 정규화 `θ_i = β_iθ̄_i + (1 − β_i)θ_i`(19a — 비 ≤10) · log 판(19b — 비 >10).

### 3.3 Sensitivity analysis (p. 5 · 식 20–21)

`V̂ = g(θ(β), i_app, x₀)` · `S = ∂V̂/∂β ∈ R^{n×m}`(n 시간 표본 · m 매개변수 · **유한차분**) · 피벗 QR `SP = QR` · 순위 `Π_ranked = Π_init P` · 크기 `M_s = |diag(R)|` — `[인쇄]` "a parameter sensitivity ranking is obtained by **orthogonalization** of the sensitivity matrix of a model" ([30] Lund & Foss 2008 · [18] Jin 2018) · "the sensitivity matrix … and therefore the parameter ranking Π_ranked, depend on the chosen input profile as well as the initial conditions". 목적 `[인쇄]` "to select the appropriate (most sensitive) estimation parameters, in order to avoid solving an **ill-conditioned** optimization problem".

### 3.4 Estimating the grouped parameters (p. 5–6 · 식 22)

`β̂_s = argmin Σ(V_exp(t_i) − V̂(θ(β), t_i))²` · "any nonlinear least-squares algorithm" · 감도 낮은 것은 β = 0.5(범위 가운데)로 고정(인쇄 "in (18)" — 식 19 의 오기 · D8).

## 4. Results and validation (p. 6–10)

### 4 머리 (p. 6 · 그림 3)

Cell 1(EMF 만 · 자료 셋 — [38]) · Cell 2(전극 평형 전위 · 자료 하나 — [24, 39]) · [24] 의 분해 모형("some of the parameters have been determined experimentally, and others have been assumed as values obtained from literature")과 비교 · 합성 셀 — `[인쇄]` "Note that measurements cannot be used here, since measured parameters and states are not available from current–voltage measurements." · Cell 1 은 자료 1 로 추정 · 2 · 3 으로 검증 · **Cell 2 는 한 자료로 추정과 검증을 다 한다**.

### 4.1 Sensitivity analysis (p. 6 · 그림 4)

추정 프로파일로 S 계산 · `[인쇄]` "since we assume that the reversible capacity Q is measurable and because the range of R̂_f,p in Table 3 was determined to be [0, 0], the remaining number of parameters to be estimated is **22**" · 두 셀 순위가 "roughly in the same order".

### 4.2 Influence of the number of estimated parameters (p. 6 · 그림 5(a))

`lsqnonlin` trust-region-reflective · 경계 = 표 3 · 초기값 β = 0.5 · Cell 1 은 Data 1 의 90 %(그림 5(b) 근거) · Cell 2 는 앞 70 % 로 추정하고 **전체로 검증** · `[인쇄]` "after about 12 parameters the RMSE for all data sets does not significantly change. This seems to indicate that **12 estimation parameters is a fair selection**" · 요동은 "non-convex … multiple local minima".

### 4.3 Influence of the length of estimation data (p. 7 · 그림 5(b) · 6)

`[인쇄]` "validating a model with the exact same data as the model has been estimated with, does not give much confidence" · "the choice for the length of the estimation data is not obvious, as having less estimation data can lead to a worse estimate, while having less validation data can lead to false conclusions" · "choosing **at least around 70%** of the estimation data is required to obtain a good model fit" · Cell 1 은 10 % 로도 작다 ↔ Cell 2 는 65 % 전까지 크다 — "more unmodeled behavior showing up in the experimental voltage of Cell 2" · 그림 6 아래: 30 %(앞 510 s)는 800 s 뒤 커지고 65 %(1,105 s)는 전 구간 작음 · [24] 매개변수는 "a clear deviation … even larger than when using 30%" → "by estimating some of the parameters, rather than relying on experiments and values from literature, a significantly more accurate model output can be obtained. However, we may still question whether the internal states … are still physically meaningful." · Cell 1 100 %: "a sharp rise in the RMSE of Data 2 and Data 3 … **overfitting** of the parameters when using 100% of the estimation data" — 원인 = SoC 0.2–0.25 의 큰 오차.

### 4.4 Consistency and accuracy of the estimated parameters (p. 8–9 · 그림 7 · 표 4)

`[인쇄]` "If the identifiability of the parameters is sufficiently large, the estimated parameters should correspond to physically meaningful parameters. However, identifiability has been a key issue for the DFN model [19]" · "due to modeling errors … **a smaller output validation error from a particular DFN model does not necessarily imply a better representation of the internal states**" · Cell 1 — 22 개 · 90 % · **50 random initial conditions** · "most parameters can be estimated consistently. However … many of the estimated parameters are at the **extremal values**, e.g., parameter 6 (s100,n) and 8 (D̂s,n)" — 원인 후보 둘(비모형 거동 · 범위가 좁음) → 확장 범위(β −0.3 … 1.3): "the variability … increases … parameter 6 … now varies between around 0.2 and 1.3 … the median is still around β = 1" · "by extending the ranges, the number of combinations of parameters that achieves a local minimum increases". 합성 셀 — "parameters … chosen randomly (within the specified ranges) … the estimation model is now exactly the same as the system … considered to be the ideal scenario" · 산포는 Cell 1 보다 큼(참값이 범위 안이라서 — 저자 해석) · "parameter 5 (D̂s,pos) seems to be the most identifiable parameter". 수정 둘: `D̂_s,pos(s_p) = 5.705 × 10^(−4+8(s_p−0.5)²)`(지수 — 쪽 렌더로 확인) · "the scaling 5.705 is chosen such that D̂s,pos((s100,p + s0,p)/2) is equal to the originally chosen parameter value" · `U_EMF(s_c) = Ū_EMF + 0.003 sin(4πs_c)` · "chosen such that the RMSE between the original model output and the modified model output after parameter estimation is approximately **1.2 mV** … in the same range as the errors shown in the upper plot of Fig. 6" · 결과 "when adding an error in U_p, the estimates deviate significantly more from the true values than when adding a nonlinearity" · 표 4 → "the MRMSE of the parameters with both of the modifications is almost equal to the MRMSE using a random set of parameters" · "**EMF modeling errors affect the identifiability of the parameters significantly more than neglecting the concentration-dependency of parameters. Therefore, when designing experiments for the parameter estimation routine, it is critical that EMF modeling errors are minimized.**"

### 4.5 Consistency and accuracy of the internal states (p. 9–10 · 그림 8)

관심 상태 = 전극 화학량론 · `φ_s − φ_e`(음극 부반응) · `c_e`(급속 충전 제약 [3–6]) · 합성: 참값이 띠 안 / 수정: `s_p` · 양극 `c_e` 가 크게 어긋남 → `[인쇄]` "**identifiability of the parameters is in principle not a large issue** when the desire is to obtain parameters that lead to a good representation of the considered states. Rather, the bigger issue in this case are **modeling errors which lead to a biased estimate** of the parameters" · 급속 충전 제약이 보수적으로(또는 반대로) 작동할 위험 · 결론 단락 "using only input/output measurements can lead to a model that does not sufficiently represent the internal states … by measuring the parameters, the obtained model does not sufficiently represent the output … both these approaches … combined" · "determining **tighter parameter ranges** leads to more consistent parameter estimates, while at the same time limits the deviation … experimentally determining parameters … is thus especially useful in defining tighter parameter ranges".

## 5. Conclusions · CRediT · 사사 (p. 10)

`[인쇄]` "estimating **12 out of all 22** model parameters is sufficient to obtain an accurate model (with respect to the output voltage)" · "the length of the identification data should be carefully selected to avoid overfitting of the parameters to modeling errors" · "modeling errors, and in particular EMF modeling errors, can lead to a large bias and variability in the estimated parameters. **We have further shown that this bias and variability can be reduced by determining tighter parameter ranges**, which can be done through cell teardown" — ⚠ 편향 감소는 참값 있는 좁은 범위 시험이 없다(D12) · CRediT · 경쟁 이익 없음 · 사사(Horizon 2020 둘 · IEC AIR TOOLS) — §서지.

---

# ★ (a) 재매개화의 결과 — 35 → 24 → 22 → 12, 구조적인가 실제적인가

## 1. 인쇄된 셈과 `[재현]`

| 단계 | 수 | 무엇이 빠지나 | 근거 |
|---|---|---|---|
| 원 DFN(표 1(a)) | **35** | — | `[인쇄]` p. 3 · `[재현]` 표 2 "a" 표시 34 + 표시 없는 `A` |
| 재매개화(표 1(b) · 표 3) | **24** | 정규화 · 묶음 · 제약 (7)(`c^max` 둘 → Q) · **`α_c = 1 − α_a`(식 12a · b — 본문 언급 0)** | `[인쇄]` p. 4 · `[재현]` 표 3 행 24 = Q + 창 4 + 19 |
| 추정 대상 | **22** | Q(측정) · `R̂_f,p`(범위 [0, 0]) | `[인쇄]` §4.1 |
| 권고 | **12** | 순위 13–22 를 β 0.5 에 고정 | `[인쇄]` §4.2 · 결론 — 기준 = 출력 RMSE 평탄 |

`[재현]` 정규화 척도: 로그 14(s_n,0% · D̂_s 둘 · D̂_e · p̂_n · p̂_p · σ̂ 둘 · R̂_f,n · k̂₀ 둘 · ε̂_e 셋) · 선형 8(s_p,0% · s_n,100% · s_p,100% · p̂_sep · t₊⁰ · κ̂ · R̂_cc · α_a) · 고정 1.

## 2. 무엇이 구조적으로 증명됐나 — "출력은 24 묶음의 함수" (구성)

표 1(b) 식 (8)–(14)는 원 매개변수를 하나도 따로 쓰지 않는다 — 고체 확산은 `D̂_s` 하나(`R_s` 흡수) · 전해질은 `ε̂_e` · `D̂_e p̂` · `κ̂ p̂` · 고체 전위는 `σ̂` · 반응은 `k̂₀`(반응 면적 `3ε_s/R_s` · `A` · `δ` 가 정규화에서 약분 — `[재현·대수]` 아래 3) · 막 · 집전체 저항은 `R̂_f` · `R̂_cc` · 용량은 `Q` 와 창(식 14 `ĉ^max = 3Q/(s_100% − s_0%)`). ⇒ **원 35 차원 매개변수 공간에서 출력이 글자 그대로 같은 11 차원 이상의 방향이 존재한다 — 구조적 비식별의 구성 증명**이다(저자는 "redundant" 로 부른다 · `identifiab*` 낱말은 이 절에 0).

## 3. 무엇이 증명되지 않았나 — 24 의 식별성 (`[재현·대수]` 둘 · `[인쇄]` 하나)

1. **남은 정확한 척도 대칭**: (9a) 는 `D̂_e p̂_i`, (11a) 는 `κ̂ p̂_i` 로만 쓰므로 임의의 `λ > 0` 에 대해 `(D̂_e, κ̂, p̂_n, p̂_p, p̂_sep) → (D̂_e/λ, κ̂/λ, λp̂_n, λp̂_p, λp̂_sep)` 가 모든 식 · 경계 · 영역 경계 플럭스 연속을 그대로 둔다 ⇒ 전해질 수송 다섯 매개변수는 **넷**(`D̂_e p̂_n` · `D̂_e p̂_p` · `D̂_e p̂_sep` · `κ̂/D̂_e`)만 정해진다 · **식별 가능한 조합은 많아야 23**. 사전 상자는 이 직선을 `κ̂` 범위(선형 · ×2.86) · `p̂_sep` 범위(선형 · ×8.4) 안으로 자를 뿐 없애지 않는다(구간 안에서는 정확한 평탄). `[해석]` 저자가 [25] 대비 "effectively lower amount of parameters" 라 쓴 선택(비유효 `D_e` · `κ` + Bruggeman 지수 묶음 `p̂`)이 바로 이 여분을 만든다 — 두 수송 계수가 같은 Bruggeman 인자를 공유한다는 물리 제약은 들어갔지만(유효 계수 여섯 → 넷), 그것을 다섯 매개변수로 적었다. 그림 4 에서 p̂_n · p̂_p 가 1 · 2 위 · D̂_e 4 · 3 위 · κ̂ 11 · 10 위 · p̂_sep 20 · 16 위 — 직교화가 이 다섯 중 하나의 독립 몫을 눌렀을 것이 예상되나(`[해석]`) 유한차분 · 혼합 척도(로그 · 선형)라 0 으로 나오지는 않는다(p̂_sep 10^−4.17 · 10^−3.67).
2. **가정 축소 `α_c = 1 − α_a`**: (12a) · (12b) 에만 있다. `[재현·대수]` (5b) `i₀ = k₀c_e^α_a(c^max − c_s,e)^α_a c_s,e^α_c` 를 `ĉ_s = 3ε_sFAδc_s` 로 바꾸면 `(3ε_sFAδ)^(−α_a−α_c)` 가 나오고 `ĵ_n` 정의의 `3ε_sFAδ` 와 지워지려면 **`α_a + α_c = 1` 이 필요**하다 — 일반 `α_c` 면 `k̂₀` 에 `(3ε_sFAδ)^(1−α_a−α_c)` 가 남아 `ε_s · A · δ` 가 동역학 묶음에서 안 빠진다. ⇒ **35 → 24 의 하나는 항등이 아니라 모형 제한**이고, 그것이 다른 묶음(`k̂₀`)의 정확성을 받친다.
3. **창 넷 — 경우 1 에서 평형 채널에 정의상 무정보**(`[인쇄]` §3.1 "any choice between 0 and 1 … same EMF-SOC relation"). 창이 출력에 닿는 인쇄 경로는 (12b) 의 `(ĉ_s,max − ĉ_s,e)^α_a` 하나(교환 전류의 SOC 모양) — 그림 4 에서 `s0,n` · `s0,p` 는 10^−3.6 … 10^−4.4 로 뒤쪽이다. `[해석·대수]` 경우 1 에는 둘째 경로가 있다 — 빌린 `U_n^lit(s_n)` 의 SOC 기울기가 창 폭 배로 바뀌어 두 전극 표면 SOC 차에 곱해진다(유한 전류에서만). 둘 다 동역학 경로라 약하고, 빌린 곡선 형상에 매달린다.

## 4. 감도 순위 = 국소 · 직교화 (둘째 줄) — 그리고 공짜 조건수 하한

[[assb-sensitivity-sweep-vs-identifiability]] 의 표로 이 편의 도구는 **둘째 줄(추정 민감도 — 추정 자료 위 야코비안)의 직교화판**이다: 평행 열은 피벗 순서에서 뒤로 밀리고 크기가 줄어든다(Lund & Foss — 26호식 스윕보다 한 단계 위). 그러나 ① **한 점**(계산점 미인쇄 G6 — Cell 1 추정값 10/22 가 범위 끝인데 순위는 아마 β 0.5) ② **범위 정규화 의존**(β 1 단위 = 사전 범위 폭 — `s_p,0%` 는 [0.86, 0.97] 0.11 폭 · `D̂_s,p` 는 세 자릿수 — 순위가 물리 감도와 문헌 범위 폭의 곱이다) ③ 문턱 0("12" 는 그림 5(a) 의 출력 RMSE 로 정함) ④ FIM · 공분산 · 신뢰구간 · 프로파일 0. `[재현]` 그래도 그림 4 에서 수치 하나는 꺼낼 수 있다 — 피벗 QR 에서 `σ_max(S) ≥ |r₁₁|`, 앞 k 열 블록의 `σ_min ≤ |r_kk|` 이므로 **cond(S_k) ≥ |r₁₁|/|r_kk|**: 고른 12 개 ≥10^2.98(Cell 1) · 10^3.00(Cell 2) · 22 개 ≥10^6.20 · 10^6.46(β 좌표 · 하한). 이 편은 이 값을 조건수로 읽지 않는다.

## 5. 27호의 기대 대조 — "곱 쌍(①–③)을 그룹으로 묶는 도구의 원전 후보"

27호 digest §6-3 의 세 곱 쌍(27호 digest 전사): ① `κ` · `ε_el/τ_el`(유효 이온 전도도) ② `D` · `r²`(확산 시간) ③ `i₀` · `A`(반응 면적 — 면적 · 용량 · 이용률 "세 겹 짐").

| 쌍 | 이 편 | 판정 |
|---|---|---|
| ② `D · r²` | `D̂_s = D_s/R_s²`(표 3) — 저자 예시 그대로("decreasing the diffusion coefficient … increasing the particle size") | ✅ 묶었다 |
| ③ `i₀ · A` | `k̂₀ = k₀c_e,o^α_a/(R_sF)` — 반응 면적 `3ε_s/R_s` · `A` · `δ` 가 약분(`α_c = 1 − α_a` 아래) · **27호의 "세 겹 짐" 중 용량 몫은 Q · 창(식 14)으로, 면적 몫은 `k̂₀` 로 갈라 둔다** | ✅ 묶었다(가정 하나 위) |
| ① `κ · ε/τ` | `ε_e^p/δ` 를 `p̂` 로 묶었으나 `κ̂` · `D̂_e` 를 따로 두어 `κ̂ p̂` · `D̂_e p̂` 곱 — **정확한 척도 대칭 하나가 남는다**(위 3-1) | ⚠ 반만 |

⇒ 27호의 지목 이유는 **② · ③ 에서 맞고 ① 에서 절반**이다 — "원전 후보" 로는 맞다(묶음 + 감도의 계보 · [25] Jobman 2015 가 묶음의 더 앞선 원전).

## 6. Q4 어휘 · 판정 (카드 형식)

| 낱말(본문 · 머리말 제외 · NFKC 전후 같음) | 수 | 쓰임 |
|---|---|---|
| `identifiab*` | **7** | 서론 1("poor [19]") · §3.1 1("as also shown in [13]") · §4.4 4(정의 문장 · "key issue [19]" · "most identifiable parameter" · "EMF modeling errors affect the identifiability") · §4.5 1("in principle not a large issue") |
| `uniqu*` | 1 | 초록 "uniquely determining" |
| `uncertain*` · `confiden*` · `reliab*` | 1 · 2 · 2 | [22] 인용 문장 · 검증 신뢰 · "found reliably" — 통계 구간 0 |
| `Fisher` · `covarian*` · `Hessian` · `Jacobian` · `condition number` · `profile`(가능도) · `bootstrap` · `posterior` · `Bayes*` · `noise` | **0** | `profile` 7 은 전부 전류 프로파일 |
| `sensitiv*` · `rank*` · `orthogonal*` · `QR` | 40 · 13 · 2 · 2 | 전부 §3.3 절차와 그 결과 |
| `consisten*` · `bias*` · `variab*` · `random*` · `synthetic` · `true` | 13 · 5 · 15 · 13 · 14 · 20 | §4.4–4.5 다중 시작 · 합성 |
| `ill-condition*` · `non-convex` · `local minim*` | 1 · 1 · 3 | 목적 · 요동 설명 |
| `overfit*` · `validat*` · `verif*` | 4 · 18 · 1(직관이 "not yet been verified") | §4.3 |
| `degenera*` · `calibrat*` · `inverse` | 0 | — |

**판정 — ASSB 0/95 · 도구 칸 · 여든일곱 번째 성질**: "**묶음으로 원 35 매개변수의 구조적 비식별 11 방향을 구성상 지우고, 국소 직교화 순위로 고른 12 개면 출력이 맞는다는 것을 보였으나, 남은 24 의 식별성은 증명하지 않았고(인쇄 식에 정확한 척도 대칭 하나 · 가정 축소 하나), 모드 좌표인 창 네 끝점은 경우 1 에서 평형 채널에 정의상 보이지 않으며, 같은 모형 · 무잡음 합성 시험에서도 참값이 상자 밖인 매개변수가 14/22 이고, 1.2 mV 모형 오차가 매개변수 추정을 무작위 수준으로 — 양극 창 끝을 사전 범위 끝으로 — 보냈다.**" 28호(액체 SPM — 용량 스케일은 입력 · 식별 집합에 모드 축 없음)와 반대쪽 끝: **이 편은 모드 좌표(창)를 식별 집합 안에 넣었고, 그 좌표가 가장 약하다는 것을 그림으로 보였다**(저자는 창을 따로 논하지 않는다). 누적 0.5 그대로(ASSB 근거 아님).

---

# ★ (b) 강조문 다섯 — 원문과 근거

| # | `[인쇄]` 강조문(p. 1) | 근거 절 · 그림 | 무엇으로 보였나 | 판정 |
|---|---|---|---|---|
| H1 | "Parameters obtained from input/output data are not necessarily physically meaningful." | §4.4–4.5 · 그림 7 · 8 · 표 4 · Cell 1 경계 | 합성(참값 있음) — 이상적 경우에도 β RMSE 0.30 ↔ 무작위 0.43 · 참값 IQR 밖 14/22 `[도표·벡터]` · 실셀 — 범위 끝 10/22(참값 없음) | ✅ 선다 — 그리고 **모형 오차 없이도** 선다(저자는 주로 모형 오차에 돌림 · "identifiability … in principle not a large issue" 는 **상태** 기준 문장) |
| H2 | "Estimating all DFN model parameters is not necessary to obtain an accurate model." | §4.2 · 그림 5(a) · 결론 "12 out of all 22" | 실셀 둘 · 출력 RMSE 가 12 개 뒤 평탄(Cell 1 Data 1 3.50 → 3.54 · Cell 2 검증 4.44 → 3.78 mV `[도표·벡터]`) | ✅ **출력 기준으로만**("accurate" = RMSE) — 유일성 · 물리 의미와 다른 명제(H1 이 그것을 말한다) · 회차 하나씩 · 순위는 한 점의 국소 순위 |
| H3 | "The length of estimation data should be carefully selected to avoid overfitting." | §4.3 · 그림 5(b) · 6 | 실셀 둘(참값 없음) · Cell 1 90 → 100 % 에서 검증 +0.42 · +0.78 mV · Cell 2 65 % 미만에서 오차 큼 | ⚠ **약하다** — 회차 하나 · 같은 곡선의 다른 요동과 같은 크기 · 마지막 10 % = SoC 0.282 → 0.214(비모형 거동 구간 — 길이가 아니라 **SoC 창** 선택) · Cell 2 는 10 % < 30 %(비단조) · 90 % 와 12 개를 **검증 RMSE 로 골라** 검증이 선택에 쓰였다 |
| H4 | "Modeling errors can lead to a large bias and variability of the estimated parameters." | §4.4 · 그림 7 · 8 · 표 4 | 합성 + 인공 오차 둘(EMF 진폭 3 mV 정현 · `D̂_s,pos` 창 안 ×23 `[재현]`) · 참값 하나 · 50 회차 | ✅ 선다(이 편에서 가장 단단한 명제) — 조건: 참값 하나 · 무잡음 · 오차 꼴 둘 · 입력 하나 · 1.2 mV = 실셀 잔차의 ×0.32–0.35 |
| H5 | "Ideally, parameters should be determined using both cell teardown and estimation." | §4.5 끝 · 결론 | 시험 0 — 근거 둘: 그림 6 분해 매개변수 모형 RMS 40.4 mV(부호 고정 −37.4) · 그림 7 확장 범위에서 산포 ↑(Cell 1 · 참값 없음) | ⚠ **권고** — "tighter ranges … bias … can be reduced" 의 편향 쪽은 참값 있는 좁힘 시험이 없다(D12) · 분해 쌍 OCP 도 셀 EMF 와 ±10 mV 어긋난다(§(c) 4) |

---

# ★ (c) 평형 전위 곡선 보정 (그림 2) — 무엇을 했나 · 우리 α·β 창 맞춤과 같은 연산인가

## 1. 두 경우 (`[인쇄]` §3.1)

| | 경우 1(분해 불가 — Cell 1) | 경우 2(분해 가능 — Cell 2) |
|---|---|---|
| U_n | **문헌에서 빌림**(흑연 — "generally the same or similar … usually a graphite-based composite") | 분해 전극을 화학량론에 대해 측정 |
| U_p | **정의 `U_p = U_EMF + U_n`** — 창을 먼저 골라야 정의된다 | 분해 전극을 측정 |
| 창 넷 | 평형 채널에 **무정보**("same EMF-SOC relation … any choice between 0 and 1") → 동역학으로 추정 | "chosen such that the difference between the measured U_p−U_n and the measured U_EMF is minimized **in some way** [23,24,26]" — 방법 인쇄 0 |
| EMF 일치 | **정의상 정확** | 잔차가 남는다(아래 4) |
| 저자 권고 | **이쪽**("it may still be preferable … since … the modeled EMF coincides exactly with the measured EMF (by definition)") | 화학을 알아도 셀 사이 EMF 차 때문에 덜 권함 |

## 2. 보정의 정체 — 이동 · 늘림이 아니라 0–10 % 형상 교체 + 음극 되계산 (`[재현·벡터]`)

경우 1 로 Cell 2 의 U_p 를 만들면 SOC 0.1 아래에서 계산 U_p 가 **오른다**(최솟값 SOC 0.0994 · 3.622 V → SOC 0 에서 3.883 V — 방전 끝 양극 전위가 오르는 비물리 모양). 처방 `[인쇄]`: 0–10 % 의 U_p 를 직선으로 갈고(기울기 = 10–40 % 평균 기울기) `U_n = U_p − U_EMF` 로 음극을 되계산 — EMF 는 그대로. `[도표·벡터]` 그려진 직선 기울기 0.545 V/SOC ↔ 규칙 0.564(−3 %) · 이음점 ≈0.094 · 보정 전후 `U_p − U_n` 은 전 구간 0.1 mV 안에서 같다 ✅. ⇒ **창(가로 좌표)은 건드리지 않고, EMF 의 저 SOC 곡률을 양극에서 음극으로 옮겨 놓는 수작업 배정**이다 — "physically intuitive"(양극 단조)라는 사전믿음으로 한 배정이고, 그 배정의 근거 자료는 같은 그림의 측정 U_p 하나다.

## 3. 빌린 곡선의 형상 오차는 다른 전극으로 1:1 간다 (`[재현·벡터]`)

`(계산 − 측정) U_p = (가정 − 측정) U_n` ±0.01 V — SOC 0.1–1 에서 **+6 … +54 mV(평균 +26 · rms 29 mV)** · U_n 쪽 +13 … +53 mV(평균 +30). 보정은 0–10 % 만 고치므로 이 오프셋은 **양극 곡선 전체에 남는다**(SOC 0.6 에서 +52 mV · 0.3 에서 +43 mV). `[해석]` 경우 1 의 평형 모형은 셀 EMF 를 정확히 맞추면서 **두 전극 곡선을 각각 수십 mV 틀리게** 둔다 — 동역학 적합에서 창 · `k̂₀`(12b 의 SOC 모양) · `D̂_s`(표면 화학량론) 가 이 틀린 모양에 맞춰 움직일 자리다. 이 편 합성 시험의 EMF 오차(진폭 3 mV)보다 열 배 크다(다만 그 시험은 EMF 자체의 오차이고, 이것은 EMF 를 지키는 전극별 배분 오차 — 같은 양이 아니다).

## 4. 분해 측정 쌍 ↔ 셀 EMF 잔차 — 경우 2 의 바닥 (`[재현·벡터]`)

그림 2 의 측정 쌍([24])으로 만든 EMF(`U_p − U_n` 측정)와 이 그림의 셀 EMF(계산 U_p − 가정 U_n = 셀 EMF 정의) 의 차: SOC 0.03–1 에서 **−9.5 … +13.5 mV** · 0.1–1 rms **5.8 mV** · SOC 0 에서 +118 mV. ⇒ 분해 전극 곡선을 창으로 놓은 결과(그림의 가로 좌표가 이미 창 정렬 뒤)가 셀 EMF 를 ±10 mV 로만 재현한다 — **이 편이 "식별성을 가장 크게 해친다" 고 보인 EMF 오차(진폭 3 mV · RMS 2.1 mV)보다 크다**. 저자의 경우 1 권고는 이 관찰과 정합한다(경우 2 로는 EMF 가 안 맞는다) — 그러나 경우 1 은 위 3 의 전극별 배분 오차를 대가로 낸다.

## 5. 그림 2 ↔ 그림 3 — 두 "EMF" 가 다르다 (D2 · `[재현·벡터]`)

본문은 "U_p is calculated from the EMF function shown in Fig. 3" 라 하지만, 그림 2 의 EMF(계산 U_p − 가정 U_n)는 그림 3 의 Cell 2 EMF 보다 SOC 0.2 · 0.5 · 0.7 · 0.9 · 1.0 에서 **+59 · +42 · +24 · +21 · +35 mV** · SOC 0.1 · 0.05 · 0 에서 +113 · +169 · +313 mV 높다(그림 3 EMF 눈금은 Cell 1 세 자료의 시작 전압으로 ±4 mV 안에서 독립 확인). 그림 2 의 EMF 는 오히려 [24] 측정 쌍 EMF 와 ±13.5 mV 로 가깝다. 또 Cell 2 자료의 시작 전압(전류 0) 4.190 V 는 그림 3 의 Cell 2 EMF 최댓값 4.168 V 보다 높다. `[해석]` 그림 3 의 Cell 2 "EMF" 가 저율 방전 의사 OCV(과전압 몫만큼 낮음 — 저 SOC 에서 더 낮음)일 가능성과 양립 — 측정법 미인쇄(G3)라 가를 수 없다. **어느 쪽 EMF 가 Cell 2 추정에 쓰였는지 미인쇄**(경우 2 의 Cell 2 는 측정 쌍을 썼을 것으로 읽힌다).

## 6. 우리 연산과의 대응 — 경우 2 = 우리 α·β · 경우 1 = 형상 자유의 극단

- **우리 4-창 + γ_Si 맞춤**은 반쪽전지 OCP 두 곡선의 모양을 고정(γ_Si 로 음극 혼합만 매개화)하고 **창(늘림 · 이동)으로 셀 OCV 를 맞춘다** — 이 편 **경우 2 와 같은 연산**이고 [[halfcell-ocp-shape-invariance]](분해 · 반쪽전지 곡선이 셀 안 · 노화 뒤에도 같은 모양) 가정을 깐다. 경우 2 의 방법을 이 편은 [23, 24, 26] 에 미뤘고, 남는 잔차가 위 4 의 ±10 mV 다.
- **경우 1 은 한쪽 형상을 빌리고 다른 쪽 형상을 완전히 자유로 둔 극단** — 그러면 창 네 좌표는 OCV 채널에서 **정의상 사라지고**(인쇄 명제), 모양 정보 전부가 "자유 곡선" 에 흡수된다. [[np-lip-ocv-reparametrization]] 의 2 자유도 정리(형상 고정 · SOC 정규화 OCV 모양은 두 자유도)와 짝: 형상을 고정하면 OCV 가 창의 두 조합을 정하고, 형상 하나를 풀면 0 조합을 정한다 — **형상 가정이 OCV 채널의 창 정보량을 정한다**(`[해석]`).
- 빌린 곡선이 흑연 · 대상이 Si-흑연이면(이 편 Cell 2 — [24] 제목 기준) γ_Si 몫의 모양이 경우 1 에서는 양극 곡선으로 넘어가고, 경우 2 형상 고정에서는 창으로 흡수된다 — 우리 γ_Si 축(halfcell-ocp-shape-invariance 의 "γ_Si ↓ 와 α_an ↓ 가 같은 서명")의 다른 판(`[해석]` · 이 편은 Si 를 언급 0).

---

# ★ (d) 자료 길이 · 과적합 · 모형 오차 편향 — 무엇으로 보였나

## 1. 실셀 둘 — 참값 없음 · 회차 하나 (`[재현·벡터]` · `[재현·가정]`)

- **Cell 1 의 규모**(미인쇄 G1): 그림 3 전류 적분 7.81 · 7.75 · 7.38 Ah ÷ 그림 6 SoC 폭 0.741 · 0.732 · 0.710 = **10.54 · 10.59 · 10.39 Ah**(세 자료가 1 % 안 — 가정: 그림 6 SoC = 쿨롱 계수) · 시작 전압이 Cell 1 EMF 와 ±4 mV · Data 1 첨두 24.6 A ≈**2.3C** · 평균 8.3 A ≈0.8C · Data 1 = SoC 0.955 → 0.214 방전 위주 동적 프로파일.
- **"90 %" 의 정체**: Data 1 의 앞 90 %(51.0 분) = SoC 0.955 → **0.282** · 마지막 10 % = SoC 0.282 → 0.214 — 그림 6 의 ±21 mV 구간(0.21–0.24)이 바로 거기다. ⇒ "자료 길이" 선택은 이 자료에서 **추정 SoC 창의 아래 끝 선택**과 같다([[data-window-identifiability]] 의 축 — 길이가 아니라 창의 위치).
- **Cell 2**: 1,700 s(= 510/0.30 = 1,105/0.65 `[재현]` ↔ 그림 3 28.33 분 ✅) · 순 방전 0.507 Ah(Cell 2 용량 미인쇄 — SoC 폭 재현 불가) · "검증" = 전체(추정 70 % 포함).
- **그림 6 ↔ 그림 5(b) 폐합 ✅**: Cell 2 30 % 24.4 ↔ 24.38 · 65 % 5.0 ↔ 4.99 · Cell 1 60 % 3.69 · 3.42 · 3.71 ↔ 3.68 · 3.38 · 3.77 mV ⇒ **그림 5(b) 는 14 개 추정**(그림 6 캡션 · G9).
- **"과적합" 근거의 크기**: Cell 1 90 → 100 % 에서 Data 2 · 3 +0.42 · +0.78 mV(Data 1 −0.24) — 같은 곡선 10–50 % 구간의 요동(Data 1 +0.54 · +0.40 · Data 2 +0.41 mV)과 같은 크기 · 회차 하나(다중 시작 0) · 저자가 같은 쪽에서 "non-convex … multiple local minima" 를 요동의 원인으로 든다 ⇒ **"100 % 에서 과적합" 과 "다른 국소 최소로 갔다" 를 이 자료로 가를 수 없다**(`[해석]`). 검증 두 자료는 60 % 에서 가장 낮고(3.38 · 3.77) 90 % 는 3.42 · 4.06.
- **모형 선택에 검증 자료가 쓰였다**: 12 개(그림 5(a) — 검증 RMSE 포함) · 90 %(그림 5(b) — 검증 RMSE) · 70 %(Cell 2 — 전체 RMSE) ⇒ 보고된 검증 RMSE 는 독립 검증이 아니다(Cell 2 는 추정 구간까지 포함). 저자도 "validating a model with the exact same data … does not give much confidence" 를 인쇄한다.

## 2. 합성 셀 — 참값 하나 · 같은 모형 · 무잡음 (역범죄)

- 설계 `[인쇄]`: 범위 안 무작위 매개변수 하나 · "the estimation model is now exactly the same as the system that is to be estimated, which is considered to be the ideal scenario" · 같은 입력 · 50 무작위 시작 · `noise` 0 회(무잡음으로 읽힘). 28호(Bizeray — 같은 선형화 SPM · 무잡음)와 같은 **역범죄** 설계다(28호 digest 전사).
- `[재현]` 표 4 "Random parameters" 행 = 균등 무작위 β 의 기대 RMS(0.427 · 0.36 ↔ 인쇄 0.43 · 0.38 ✅) — 이 기준 대비 합성 셀 0.30(22 개 — 무작위의 70 %) · 0.14(첫 9 개 — 37 %).
- ★ **무잡음 · 같은 모형인데 출력 RMSE 중앙값 0.13 mV ≠ 0** — 전역 최소는 잔차 0 이므로 **회차 절반 이상이 그 최소에 못 닿았다**. 회차별 잔차 · 문턱이 인쇄되지 않아(G8) 그림 7 의 합성 산포는 **근최적 집합의 폭(같은 잔차의 다른 매개변수)과 수렴 실패(더 큰 잔차의 국소 최소)가 섞인 값**이다 — [[near-optimal-set-width-measurement]] 가 요구하는 `tol` 이 없다.
- `[도표·벡터]` 참값이 IQR 밖 **14/22**(첫 10 중 6) — 저자 문장 "especially for the first 10 parameters, the estimated parameters are close to the true parameters" 는 중앙값 거리(첫 9 평균 0.088 β)로는 맞고 IQR 로는 아니다(D6).

## 3. 모형 오차 둘 — 크기와 결과 (`[재현]` · `[도표·벡터]`)

| 오차 | 꼴 `[인쇄]` | 크기 `[재현]` | 결과 |
|---|---|---|---|
| `D̂_s,pos` 농도 의존 | `5.705 × 10^(−4+8(s_p−0.5)²)` · 창 가운데에서 원래 값 | 참 창 s 0.418–0.914 에서 6.5×10⁻⁴ … **1.34×10⁻²**(×23 · 최솟값 5.7×10⁻⁴ @ s 0.5) · 가운데 값 9.47×10⁻⁴ ↔ 그림 7 참값 9.06×10⁻⁴(×1.05 — 지수 판독 확인) | 출력 1.19 mV · β RMSE 0.43(= 무작위) · 첫 9 개 0.22 · #1 p̂_n β 0.39 → 0.95 · #8 D̂_s,n 0.37 → 0.74 · #5 자신 0.111 → 0.044 |
| EMF 오차 | `Ū_EMF + 0.003 sin(4πs_c)` | 진폭 3 mV · 두 주기 · RMS 2.12 mV(전 SOC) · 2.13(Data 1 창) | 출력 1.17 mV(`[재현·가정]` 오차 분산의 ≈70 % 를 매개변수가 흡수) · β RMSE 0.44 · 첫 9 개 0.34(무작위 0.38 에 가깝다) |
| 둘 다 | 그림 7 · 8 에만 | — | 표 4 열 없음(D5) · 그림 8 `s_p(L)` · 양극 `c_e` 가 띠 밖 |

★ **세 수정 모두에서 #12 `s_p,100%` 중앙값이 사전 범위 하한(β 0 → s 0.22)으로 간다** — 참 0.418(β 0.90) · 합성 0.381. ⇒ 1.2 mV 출력 오차를 맞추는 동안 **양극 창 끝(모드 좌표 — 양극 이용 범위의 위끝)이 범위 폭 전체만큼 이동**했다(`[도표·벡터]` · 저자는 창을 따로 논하지 않음). 그림 8 아래 줄 `s_p(L)` 띠가 t = 0 에서 참값보다 ≥0.105 아래인 것이 같은 일의 상태판이다.

`[재현·벡터]` **오차 크기 비교**: 주입 모형 오차의 출력 RMSE 1.2 mV ↔ 실셀(Cell 1 · 60 % · 14 개) 잔차 RMS 3.42–3.71 mV = **×0.32–0.35** — 인쇄 "in the same range as the errors shown in the upper plot of Fig. 6" 는 너그럽다(D3). 실셀의 비모형 거동이 주입 오차보다 크다면 실셀 추정의 편향은 합성 시험보다 클 수 있다(`[해석]`).

## 4. 일관성 ≠ 정확성 — 그리고 "경계 접촉" 이 Cell 1 의 첫 서명이다

Cell 1(참값 없음) 상자는 좁고(`[인쇄]` "most parameters can be estimated consistently") 중앙값 10/22 가 범위 끝이다 — 확장 범위에서 중앙값 6 개가 [0, 1] 밖 · IQR 14 개가 원 범위 끝을 넘는다 `[도표·벡터]`. 합성 셀은 참값이 범위 안이라 산포가 더 크다(저자 해석). `[해석]` **좁은 상자 + 범위 끝 = 정확해서가 아니라 경계에 눌려서 일관된 것**이고, 이 편 자신의 합성 결과(모형 오차가 있으면 창 끝이 범위 끝으로 간다)가 Cell 1 의 경계 접촉을 "실셀 비모형 거동의 흔적" 으로 읽을 근거를 준다 — 저자도 원인 후보로 "unmodeled behavior … or … the ranges chosen for the parameters are too small" 둘을 인쇄했다.

## 5. 분해 매개변수 모형 비교 (그림 6 아래) — 오차 꼴 (`[재현·벡터]`)

"Parameters from Sturm et al (2019)" 의 `V_meas − V_sim`: RMS 40.4 · 평균 −37.4 · 최대 +0.2 mV(**전 구간 음수** — 모형 전압이 늘 높다) · 동적 몫 ≈15 mV · t = 0 ≈0(휴지 시작은 맞음). `[해석]` 부호 고정 오프셋은 과전압 과소(저항 · 동역학) · EMF · 온도 · 초기 SoC 어긋남과 양립하고, 비교 조건(온도 · [24] 모형의 EMF · 어느 값이 문헌인지)이 미인쇄다(G10) — "by measuring the parameters, the obtained model does not sufficiently represent the output" 은 **어느 분해 매개변수가 틀렸는지 가르지 않은 채** 쓴 문장이다.

---

# ★ (e) 우리 것에 주는 것 — 이식할 것 · 못 할 것

`bms-balancing/docs/NEW_MODEL_REQUIREMENTS.md` §7-1(산출이 같이 내야 하는 것 — ① 근최적 집합 폭 ② 조건수 ③ 경계 접촉 ④ 부호 식별 ⑤ 허용 `tol`)과 §7-2(있다: 폭 측정기 · 경계 난간 · 부호 / 없다: **조건수** · γ 직접 적합 증인 · 공유 가능값 증인 · held-out)에 맞춰 본다(읽기만 · 우리 쪽 수치는 옮기지 않는다).

| 이 편의 절차 | §7 대응 | 이식 | 단서 |
|---|---|---|---|
| **피벗 QR 순위 + `\|r_kk\|`**(§3.3 · 그림 4) | ② 조건수(미구현) | ✅ **값싼 첫 판** — 우리 4-창 + γ_Si 야코비안(정규화 좌표)에 피벗 QR 을 걸면 순위 + `\|r₁₁\|/\|r_kk\|` = 조건수 하한이 공짜로 나온다 | 한 점 · 정규화(범위 폭) 의존 · **하한**(참 조건수는 SVD) · 평행 열의 몫은 뒤 순위로 숨는다 — 우리 Phase 1d 의 특이값과 같은 대상의 거친 판 |
| **범위 정규화 β + 로그/선형 규칙**(식 19) | — | ✅ 좌표 선택 기록용 | 순위가 "문헌 범위 폭 × 물리 감도" 의 곱이 된다 — 범위를 적어야 순위가 읽힌다 |
| **묶음 · 정규화**(§2.2) | ② 의 전 단계 | ⚠ 대상이 다르다 — 우리 OCV 대수의 정확한 null(1,1,1)은 [[np-lip-ocv-reparametrization]] 이 이미 닫힌 형태로 준다 | 교훈만: **남은 곱 쌍 · 가정 축소를 확인**(이 편 24 에 대칭 하나 · α_c 가정 하나) |
| **합성 참값 + 인공 모형 오차 주입 + 무작위 기준**(§4.4 · 표 4) | 하네스 설계 | ✅ **시험 설계** — 우리 합성 truth 에 반쪽전지 형상 오차(수 mV 정현 · 음극 혼합 모양 · γ_Si 모양)를 넣고 창 · 모드 추정이 경계로 가는지 · β RMSE 가 무작위 기준(≈0.41–0.43)에 닿는지 | 이 편은 참값 하나 · 무잡음 · 잔차 문턱 0 — 우리는 `tol` 과 함께(①⑤) |
| **경계 접촉 + 범위 확장 시험**(그림 7 · β −0.3 … 1.3) | ③ 경계 접촉 | ✅ **인쇄 선례** — Cell 1 경계 10/22 · 확장 시 s100,n 0.2–1.3 · "the number of combinations of parameters that achieves a local minimum increases" | 확장 범위 결과도 다중 시작 산포(tol 0) |
| "12 개면 충분" · "자료 ≥70 % · 90 %" | — | ❌ **수치 규칙으로 못 옮긴다** — 한 셀 · 한 회차 · 출력 RMSE 기준 · 동적 드라이브 사이클 | 우리 물음은 OCV 유일성 — 출력이 맞는 매개변수 수가 아니다 |
| **경우 1 평형 모형**(EMF 로 한 전극 곡선 정의) | — | ❌ **쓰면 안 된다** — 우리 창 네 좌표가 OCV 채널에서 정의상 비식별이 된다 | 우리는 경우 2(형상 고정 + 창) — 대신 경우 2 의 잔차(이 편 ±10 mV)를 truth 설계의 형상 오차 크기 참고로 |
| 다중 시작 상자 그림 = 폭 | ① · ⑤ | ❌ **폭으로 읽지 않는다** — 무잡음 · 같은 모형에서도 출력 RMSE 중앙값 0.13 mV(수렴 실패 섞임) | 우리 폭 측정기(근최적 합집합 · `width_is_lower_bound`)가 이 자리 |

`[해석]` 한 줄: **이 편은 §7 의 ③(경계 접촉)과 ②(조건수 — 하한판)를 DFN 매개변수 추정에서 실제로 보여 준 액체셀 선례이고, ①⑤(tol 있는 폭)는 없다** — 그리고 그 경계 접촉이 모드 좌표(창 끝)에서 일어났다는 것을 그림 7 이 보인다.

---

# ★ (f) Q1–Q8 — 채움표 칸 (닻 카드 수집 지침)

| Q1 정량 | Q2 독립관측 | Q3 라벨층위 | Q4 유일성 | Q5 Li-In | Q6 압력 | Q7 dead Li | Q8 화학·OCP |
|---|---|---|---|---|---|---|---|
| **없다 — 액체셀.** `contact` 1 = "Current collector contact resistance"(옴) · 열화 0 · `θ(N)` **0/95**. 층 하나 `[해석·대수]`: 정규화 DFN 에서 **표면 접촉 손실 `A_eff`** 는 `k̂₀ × A_eff` · `R̂_f ÷ A_eff`(두 동역학 묶음 — `k̂₀R̂_f` 불변) · **입자 통째 비연결 `u`**(= `ε_s` 형 LAM — 물질 소실과 같은 자리)는 창 폭(용량 `3Q/Δs`) · `R̂_f`(÷u) · `σ̂`(×u) · **`c^max` 형 LAM**(입자는 남고 자리만 줄어듦)은 창 폭 하나 — 양극은 `R̂_f,p` 범위 [0, 0] 이라 둘째 서명이 범위 선택으로 꺼져 있다 | **없다** (ASSB 관측 0). 분해 전극 OCP([24] — Cell 2)는 방법 쪽 입력 · 그 쌍이 셀 EMF 와 −9.5 … +13.5 mV | 칸 없음 · **층 하나: fitted(`lsqnonlin` · 범위 경계 · β 0.5 시작 + 다중 시작 50) + 합성 참값 복원(같은 모형 · 무잡음 · 참값 하나 · 인공 오차 둘)** — 불확실성 = 다중 시작 상자 그림(잔차 문턱 0) · 추정값 표 0 · Cell 1 범위 끝 10/22 · 검증 자료로 모형 선택 | **★ 있다 — 단 액체(도구 칸). ASSB 0/95 · 여든일곱 번째 성질**(§(a) 6) — 구조적: 35 → 24 구성 증명(출력 = 묶음 함수) · 24 는 미증명(척도 대칭 1 · `α_c` 가정 · 경우 1 창 무정보) / 실제적: 국소 직교화 순위 · `[재현]` cond ≥10^2.98 · 합성 다중 시작(참값 IQR 밖 14/22 · 모형 오차 1.2 mV → β RMSE = 무작위 · s_p,100% 범위 끝) · `identifiab*` 7 · FIM · CI · 프로파일 0 · 누적 0.5 그대로 | **해당 없음** — 액체 · 기준극 0(`reference electrode` 은 [22] 제목에만) · 방법 쪽: 경우 2 는 분해 반쪽전지(기준극 판의 액체 이식) | **없다** (`pressure` 0 · 셀 형식 미인쇄 — [24] 제목 "18650") | **해당 없음** | **층 하나 — 화학 미인쇄**(본문 silicon · nickel · NMC 0 · [24] 제목 "18650 nickel-rich, silicon-graphite") · **EMF 측정법 미인쇄** · 경우 1 U_n = 문헌 흑연([23]) · U_p = EMF + U_n(0–10 % 직선 교정) · `[재현·벡터]` 빌린 U_n 형상 오차 +13–53 mV → U_p · 그림 2 ↔ 3 EMF 21–59 mV |

**누적 ≈20.0 → ≈20.0 (새 칸 0).** Q3 · Q4 · Q8 에 층 하나씩(도구 칸 — ASSB 칸 이동 근거 아님).

---

# 어휘 집계 — 텍스트 층 · 줄 끝 하이픈 복원 · 머리말(저널 · 쪽 번호 · "Z. Khalik et al.") · p. 1 판권 머리 제외 · 본문(강조문 → 사사 · 캡션 · 표 포함) | 참고문헌, NFKC 전후 같음

| 낱말 | 본문 | 참고문헌 |
|---|---|---|
| `identifiab*` · `identif*` · `uniqu*` · `uncertain*` | **7** · 17 · 1 · 1 | 1(Bizeray 제목) · 7 · 0 · 0 |
| `Fisher` · `Bayes*` · `likelihood` · `covarian*` · `Hessian` · `Jacobian` · "condition number" · `bootstrap` · `posterior` · `noise` | **0** | 0 |
| `sensitiv*` · `rank*` · `orthogonal*` · `QR` · `ill-condition*` | 40 · 13 · 2 · 2 · 1 | 1 · 1 · 1 · 0 · 0 |
| `consisten*` · `bias*` · `variab*` · `random*` · `synthetic` · `true` | 13 · 5 · 15 · 13 · 14 · 20 | 0 |
| `fit*` · `overfit*` · `validat*` · `verif*` · `estimat*` · `error*` · `optimi*` · `minim*` · "local minim*" · `non-convex` | 5 · 4 · 18 · 1 · 148 · 34 · 6 · 7 · 3 · 1 | 0 · 0 · 1 · 0 · 9 · 0 · 2 · 1 · 0 · 0 |
| `normaliz*` · `group*` · `reparameteriz*` · `parameter*` · `assum*` · "physically meaningful" | 15 · 18 · 14 · 335 · 10 · 8 | 0 · 0 · 0 · 20 · 0 · 0 |
| `teardown`/`tear-down`/`tear down` · `measur*` · `experiment*` | 12 · 42 · 18 | 0 · 0 · 4 |
| `EMF`(첨자 포함 33 · 낱말 27) · `OCP` · `OCV`/open circuit · "equilibrium potential" · `stoichiom*` · `balanc*` · `window` · `shift`/`stretch` · `hysteres*` | 27 · 4 · 1 · 26 · 10 · 1 · **0** · **0** · 0 | 0 |
| `SOC`/`SoC`/state of charge · `GITT` · `impedanc*`/`EIS` · `temperature`/`°C` | 13 · 0 · 0 · **0** | 2 · 0 · 1 · 0 |
| `degrad*` · `ag(e)ing` · `cycl*` · `fade` · `loss` · `LAM` · `LLI` | **0** · 0 · 1 · 0 · 0 · **0** · **0** | 1 · 2 · 1 · 1 · 1 · 0 · 0 |
| `contact*` · `pressure` · "solid electrolyte"/all-solid | 1(R_cc 이름) · **0** · **0** | 0 |
| `silicon` · `graphite` · nickel/`NMC`/LFP · `reference electrode` · `half-cell` | **0** · 1 · **0** · 0 · 0 | 2 · 3 · 4 · 1 · 0 |
| `DFN` · `P2D`/pseudo-two · `SPM`/single-particle · `Butler` · `PyBaMM` · `MATLAB`/`lsqnonlin` | 44 · 1 · 2 · 1 · 0 · 2 | 0 · 0 · 6 · 0 · 0 · 0 |
| `supplement*` · "supporting information" · `appendix` · "data availab*" · `github`/`zenodo` · `video`/`movie` | 0 · 0 · 0 · 1(본문 문장) · 0 · 0 | 0 |

⚠ 텍스트 층 한계: ① 표 1 · 3 의 기호 · 지수는 조각으로 흩어져 낱말 패턴만 셌다 ② 그림(그림 1 래스터 · 2–8 벡터 외곽선) 안 글자는 셈에 없다 — 그림 2 범례("Measured U_n" …) · 그림 4 매개변수 이름 · 그림 7 "True parameter value" · 그림 8 "Estimated state bounds" ③ 합자 0 · NFKC 는 수식 이탤릭 42 종 · 줄임표만 바꾼다(낱말 셈 같음).

---

# 재현 (`[재현]` — 인쇄 수치 · 식 · 그림 벡터로 우리가 계산 · 가정 · 외부 값 표시)

| # | 무엇 | 결과 | 판정 |
|---|---|---|---|
| R1 | 매개변수 셈 | 35 = 표 2 "a" 34 + `A` · 24 = Q + 창 4 + 19 · 22 = 24 − Q − R̂_f,p · 로그 14 · 선형 8 · 고정 1 | ✅ 인쇄 35 · 24 · 22 |
| R2 | 남은 척도 대칭(식 9a · 11a) | `(D̂_e, κ̂, p̂_i) → (D̂_e/λ, κ̂/λ, λp̂_i)` 출력 불변 `[재현·대수]` · 상자 안 도달 폭 = κ̂ 범위 ×2.86 · p̂_sep ×8.4 | 24 는 최소가 아니다(≤23) |
| R3 | `α_c = 1 − α_a` 의 역할 | `k̂₀` 묶음에 `(3ε_sFAδ)^(1−α_a−α_c)` 가 남지 않으려면 필요 `[재현·대수]` | 가정 축소(D9) |
| R4 | β 확장 | `s_n,100%` β 1.3 → 0.932 · β −0.3 → 0.708 | ✅ "still physically meaningful … < 1" |
| R5 | Cell 2 자료 길이 | 510/0.30 = 1,105/0.65 = **1,700 s** ↔ 그림 3 28.33 분 | ✅ |
| R6 | Cell 1 용량(`[재현·가정]` 그림 6 SoC = 쿨롱 계수) | 7.81/0.741 = 10.54 · 7.75/0.732 = 10.59 · 7.38/0.710 = 10.39 Ah · 시작 전압 ↔ EMF ±4 mV | 1 % 안 일치(G1) |
| R7 | Data 1 의 자료 % ↔ SoC | 60 % = 34.0 분 → SoC 0.532 · 90 % = 51.0 분 → 0.282 · 100 % → 0.214 | 마지막 10 % = 그림 6 의 ±21 mV 구간 |
| R8 | 그림 6 ↔ 그림 5(b) | Cell 2 30 % 24.4 ↔ 24.38 · 65 % 5.0 ↔ 4.99 · Cell 1 60 % 3.69 · 3.42 · 3.71 ↔ 3.68 · 3.38 · 3.77 mV | ✅ → 그림 5(b) = 14 개 추정(G9) |
| R9 | 분해 매개변수 모형 오차(그림 6) | RMS 40.4 · 평균 −37.4 · 최대 +0.2 mV · 동적 몫 ≈15 mV · t = 0 ≈0 | 부호 고정(G10) |
| R10 | 그림 2 보정 규칙 | 계산 U_p 최솟값 SOC 0.0994 · 3.622 V · 직선 0.545 ↔ 규칙 0.564 V/SOC · 보정 전후 EMF 동일 | ✅(−3 %) |
| R11 | 빌린 U_n 형상 오차 → U_p | (계산 − 측정) U_p ≈ (가정 − 측정) U_n ±0.01 V · SOC 0.1–1 +6 … +54 mV(평균 +26) | §(c) 3 |
| R12 | 분해 쌍 ↔ 셀 EMF | −9.5 … +13.5 mV(SOC 0.03–1) · rms 5.8 mV(0.1–1) | §(c) 4 |
| R13 | 그림 2 EMF ↔ 그림 3 Cell 2 EMF | +21 … +59 mV(SOC 0.2–1) · +113 … +313 mV(≤0.1) | ❌ D2 |
| R14 | 그림 4 → 조건수 하한 | `\|r₁₁\|/\|r_kk\|`: 12 개 10^2.98 · 10^3.00 · 22 개 10^6.20 · 10^6.46 | 하한(G6) |
| R15 | 표 4 무작위 기준 | 균등 β ↔ 그림 7 참값 기대 RMS 0.427 · 첫 9 개 0.36(MC 0.425 · 0.358) ↔ 인쇄 0.43 · 0.38 | ✅ |
| R16 | `D̂_s,pos(s_p)` | 창 가운데(0.666) 9.47×10⁻⁴ ↔ 그림 7 참 D̂_s,p 9.06×10⁻⁴(×1.05) · 창 안 ×23(6.5×10⁻⁴ … 1.34×10⁻²) | ✅ 지수 판독 |
| R17 | EMF 오차 크기 | 진폭 3 mV · RMS 2.12(전 SOC) · 2.13 mV(Data 1 창) → 추정 뒤 출력 1.17 mV(`[재현·가정]` 분산 ≈70 % 흡수) | — |
| R18 | 주입 오차 ↔ 실셀 잔차 | 1.2 ↔ 3.42–3.71 mV = ×0.32–0.35 | D3 |
| R19 | 그림 7 판독 | Cell 1 범위 끝 10/22 · 확장 [0, 1] 밖 중앙값 6 · 합성 참값 IQR 밖 14/22 · 수정 17 · 17 · 16 · s_p,100% → 0.226 · 0.220 · 0.220(하한 0.22) ↔ 참 0.418 | `[도표·벡터]` |
| R20 | 그림 8 판독 | 아래 줄 s_p(L) t = 0 [≤0.249, 0.335] ↔ 0.440 · c_e(L) 최저 ≤0.54 ↔ 0.84 · 시간 축 76.7 분 | D7 |
| R21 | 일정 | 63 · 19 · 29 · 59 일 · PDF 생성 온라인 9 일 뒤 | 계산값 |

---

# 참고문헌 40 번호 — 우리 축에 닿는 것 (번호는 PDF p. 10–11 목록에서 직접 확인 · 빠진 번호 0)

| [#] | 서지 `[인쇄]` | 이 편의 쓰임 | 우리 축 |
|---|---|---|---|
| [13] | A.M. Bizeray, J.-H. Kim, S.R. Duncan, D.A. Howey, *Trans. Control Syst. Technol.* **27**(5), 1862–1877 (2019) = **28호** | 서론 시간 영역 목록 [11–16] · §3.1 "Deviations of the modeled EMF … impact the identifiability … as also shown in [13]" | **Q4 도구 · 흡수됨** |
| [19] | J.C. Forman, S.J. Moura, J.L. Stein, H.K. Fathy, "Genetic parameter identification of the Doyle-Fuller-Newman model from experimental cycling of a LiFePO4 battery", *Am. Control Conf.*, 2011, pp. 362–369 | "**Since the identifiability of the DFN model is poor [19]**" · "identifiability has been a key issue for the DFN model [19]" | Q4 — ⚠ 원장 Forman 2012 *JPS* 210, 263 과 **다른 편**(학회 판) |
| [18] | N. Jin, D.L. Danilov, P.M. Van den Hof, M. Donkers, *Int. J. Energy Res.* **42**(7), 2417–2430 (2018) | 감도 순위([30])를 묶지 않은 DFN 에 — 이 편의 직전 판 | Q4 도구 |
| [25] | R. Jobman, M.S. Trimboli, G.L. Plett, *J. Energy Chall. and Mech.* **2**(2), 45–55 (2015) | 정규화 · 묶음 원형(24 · α_a = α_c = 0.5 · R_cc 0) | Q4 도구 · Plett 계보 |
| [30] | B.F. Lund, B.A. Foss, *Automatica* **44**(1), 278–281 (2008) | 직교화 순위 원전 | Q4 도구 |
| [22] · [31] | Z. Chu, R. Jobman, A. Rodríguez, G.L. Plett, M.S. Trimboli, X. Feng, M. Ouyang, *J. Energy Storage* **27**, 101101 (2020)(Part II — 기준극 기반 식별) · Chu, Plett, Trimboli, Ouyang *J. Energy Storage* **25**, 100828 (2019)(Part I) | 묶음별 실험 설계 "intuition … unexpected uncertainty and errors [22]" · 묶음 [31] | Q4 · Q5(액체) |
| [23] | M. Ecker, T.K.D. Tran, P. Dechent, S. Käbitz, A. Warnecke, D.U. Sauer, *J. Electrochem. Soc.* **162**(9), A1836–A1848 (2015) | 분해 매개변수화 · 범위 원전 · **그림 2 가정 U_n(흑연)** · 창 맞춤 방법 | Q8 · Q3 |
| [24] · [39] · [40] | J. Sturm, A. Rheinfeld, I. Zilberman, F.B. Spingler, S. Kosch, F. Frie, A. Jossen, *J. Power Sources* **412**, 204–223 (2019)("18650 nickel-rich, silicon-graphite") · Sturm … Jossen *JPS* **436**, 226834 (2019) · Sturm … Jossen *JES* **167**, 130505 (2020) | Cell 2 자료 · 측정 전극 평형 전위 · 분해 모형(그림 6) · "the battery voltage mostly depends on the EMF, see [40]" | **Q8 · γ_Si 축** |
| [26] | J. Schmalstieg, C. Rahe, M. Ecker, D.U. Sauer, *J. Electrochem. Soc.* **165**(16), A3799 (2018) | 분해 매개변수화 · 범위 · 창 맞춤 | Q3 |
| [27] | V. Ramadesigan, K. Chen, N.A. Burns, V. Boovaragavan, R.D. Braatz, V.R. Subramanian, *J. Electrochem. Soc.* **158**(9), A1048 (2011) | DFN 동시 추정 | Q4 · 노화 축 — 원장 Ramadesigan 2012(*JES* 159, R31 리뷰)와 다른 편 |
| [11] · [33] | Santhanagopalan, Guo, White *JES* **154**, A198 (2007) · K. Smith, C.-Y. Wang *JPS* **161**(1), 628–639 (2006) | 목록 인용 — [11] 시간 영역 목록 · [33] "assuming their values from literature … as done in, e.g., [18,33]" · U_n 문헌 가정 [16, 18, 33] | Q4 · Q8 |
| [16] | A.P. Schmidt, M. Bitzer, A.W. Imre, L. Guzzella, *J. Power Sources* **195**(15), 5071–5080 (2010) | 경우 1 관행(U_n 문헌) 예 | Q8 |
| [17] · [20] · [21] · [12] · [14] · [15] | Zhou & Huang 2020 *J. Energy Storage* 31, 101629 · Marcicki 2013 *JPS* 237, 310 · Zhang L. 2014 *JPS* 270, 367 · Masoudi 2015 *JPS* 291, 215 · Namor 2017 *J. Energy Storage* 12, 138 · Pang 2019 *EA* 307, 474 | 매개변수화 목록 | Q4 주변 |
| [34] | H.J. Bergveld, W.S. Kruijt, P.H.L. Notten, *Battery Management Systems: Design by Modeling*, Kluwer 2002 | EMF 결정 기법 개관 | Q8 · OCV 측정 |
| [38] | H.P.G.J. Beelen, H.J. Bergveld, M.C.F. Donkers, *Conf. Control Technol. and Appl.*, IEEE 2018, 1526–1531 | **Cell 1 자료 원전**(등가회로 실험 설계) | 자료 |
| [28] · [29] · [32] · [35]–[37] | Khalik 2021 *JPS* 488, 229427(툴박스) · Subramanian 2009 · Xia 2017 *Appl. Energy* · Arora 2000 · Doyle & Fuentes 2003 · Reimers 2013 | 모형 구현 · 범위 | — |
| [1]–[10] | Moura 2017 · Zou 2015 · Klein 2011 · Suthar 2014 · Perez 2016 · Khalik 2020 ACC · Liaw 2004 · Plett 2015 책 · Doyle 1993 · Li 2017 | 서론 배경(BMS · 급속 충전 · DFN 원전) | — |

---

# 인용 대조

## 1. 이 편을 인용한 우리 digest — 그 쓰임

| 호 | 자리 | 그 digest 가 매단 것 | 원문 대조 |
|---|---|---|---|
| **27호** Sinzig 2024 *JES* 171, 120519 | [27] · 후속 표 :375 ★★★★ · 본문 "to fit the parameters"(:395) | "DFN 파라미터 **정규화 · 그룹화 · 민감도**로 식별 가능한 조합을 만드는 계보. **곱 쌍(①–③)을 그룹으로 묶는 도구의 원전 후보**" — `[추론]`(27호 지면에 제목 없음 · :396 "확인 전") | ✅ **정규화 · 묶음 · 감도는 제목 그대로 맞다**(27호 `[추론]` 해소) · 곱 쌍: ② `D·r²` ✅ · ③ `i₀·A` ✅(가정 `α_c = 1 − α_a` 위) · ① `κ·ε/τ` ⚠ 반만(척도 대칭 남음 — §(a) 5) · ⚠ "식별 가능한 조합" — 24 의 식별성은 증명 0 · 조합 하나가 아직 비식별 |

**지목 수 확인**: 지목은 각 digest 의 후속 절만 센다 — 27호 후속 표(:375) 하나 **= 1 — 원장 "27 \| 1" 과 일치(정정 없음)**. 카드 :5073 · `log.md` :2103 은 27호 흡수 기록(같은 지목의 전사) · 92 · 93 · 94호의 "4차 묶음 13 편과의 관계" 문장은 교차 기록(지목 아님) · 92호 :568 은 §3-b (다) 의 "닿는 논문" 목록 전사. **등급**: 27호 ★★★★ ↔ 원장 ★★★(원장이 내렸거나 다르게 매김 — 표시만).

## 2. 이 편이 인용한 우리 digest — 쓰임 대조 (digest 전사 · 원 논문은 이 세션에서 다시 열지 않음)

| 이 편 [#] | 우리 digest | 이 편의 쓰임 | 대조 |
|---|---|---|---|
| [13] | **28호** Bizeray 2019 | ① 서론 "simplified models in the **time domain** [11–16]" 목록 ② §3.1 "Deviations of the modeled EMF from the measured EMF can significantly impact the identifiability of the model parameters, as also shown in [13]" | ① ⚠ 28호의 식별성 분석은 **주파수 영역 전달함수**(선형화 SPM · EIS) — 시간 영역은 검증(그림 9 · ×0.78 보정)뿐(28호 digest 전사) · 분류 느슨 ② ✅ 정신은 맞다 — 28호는 식별성이 **OCV 기울기 `β = dU/dQ`(기준극 입력)** 에 매달리고(평탄 OCV → 비식별) 시간 영역에서 OCV 기울기 ×0.78 사후 보정으로 맞췄다 — "EMF 오차가 식별성을 해친다" 의 선례로 읽힌다 · 단 28호가 보인 것은 **기울기**(형상) 의존이지 EMF 절대 오차가 아니다 |

**교차 참조(이 편이 인용하지 않음 · 같은 축)**: **26호** Iwakiri 2024(ASSB 매개변수 추정 + "sensitivity analysis" = OAT 스윕 — 이 편의 직교화 순위보다 아래 줄) · **27호** Sinzig 2024(이 편을 인용 — 위) · **29호** Yanev 2024(ASSB 적합 dependency — 둘째 줄의 수치판) · **31호** Chien 2023(액체 ICI — 상수 입력 고지) · **34호** Liang 2026(입력 설계로 식별성 — 처방만) · **36호** Thelen 2024(확률적 ML — 파라미터 불확실성 칸 없음) · **74호** Park 2021 *Nat. Mater.*(Bayes 비교 · 최적 k 가 사전 범위 경계 — 이 편 Cell 1 경계 접촉과 같은 서명) · **91호** Danilov 2011(ASSB 박막 모형 매개변수 표 — 같은 Eindhoven 연구망 · [18] 공저자 Danilov) · **92호** Firouz 2020(블록 지향 "system identification") · **93호** Bielefeld 2023("측정하라 · 적합하지 마라" — 이 편은 반대로 **둘을 합치라** 하고, 측정 매개변수 모형이 출력을 못 맞춘다는 표본(그림 6)을 낸다) · 액체 모드 계보: Lin 2024([[np-lip-ocv-reparametrization]]) · Lee 2020([[data-window-identifiability]]) · Mohtat 2019 · Schmitt 2022([[halfcell-ocp-shape-invariance]] — Si/흑연 γ_Si) · [[pyprobe]](전극 OCP 로 셀 OCV 맞춤 — 경우 2 연산). 4차 묶음: **13 편 인용 0**(파일 56 Lu 2022 는 이 편보다 뒤 — 같은 Plett 계보의 [25] Jobman 2015 · [22] · [31] Chu 를 인용).

---

# 곱 축퇴 처방 — 일흔여덟 번째 적용 ([[assb-lampe-contact-product-degeneracy]])

**적용 불가(액체 · 접촉 0 · 열화 0) — 대신 곱을 "묶음" 으로 선언하는 처방의 원형과, 그 묶음 위에서 카드 물음이 어디로 가는지의 대수를 준다.**

| 처방 단계 | 필요한 입력 | 95호 | 판정 |
|---|---|---|---|
| 1단계(16 · 23호) | `R` · `C` 같이 | EIS 0 · DFN 에 이중층 0 | ❌ |
| 2단계(18 · 25호) | 면적을 아는 대조군 | 0 | ❌ |
| 3단계-a · b(19호) | `Ea` · `C` 상한 | 온도 0 | ❌ |
| 4단계(20 · 24호) | 시간 영역 · 같은 시편 | 동적 전류 · 전압은 있으나 `C` 0 | ❌ |
| 율 스윕 · `J^T J` | — | **추정 자료 위 감도 행렬 `S` 의 피벗 QR**(직교화 순위 — "`J^T J` 최소 고유벡터" 줄의 순위판) · 그러나 면적 · `k₀` 는 이미 한 묶음 | ⚠ 도구만 |

**곱 문장**(`[인쇄]` → `[해석]`):
- ① `[인쇄]` "by decreasing the diffusion coefficient D_s and increasing the particle size R_s accordingly, the diffusion dynamics in the solid phase remain unchanged … one of these parameters is redundant" — **곱(비) 축퇴를 문장으로 인쇄하고 그것을 한 매개변수(`D̂_s = D_s/R_s²`)로 바꿔 끝낸다** — 확산 쪽의 곱 원형(27호 ② 의 액체 판).
- ② `[재현·대수]` `k̂₀ = k₀c_e,o^α_a/(R_sF)` — 반응 면적 `3ε_s/R_s` · `A` · `δ` 가 정규화에서 약분(`α_c = 1 − α_a` 아래) ⇒ **표면 접촉 손실 `A_eff` 는 `k̂₀ × A_eff` 와 `R̂_f ÷ A_eff`(막 저항은 국소 플럭스에 걸리므로) 두 묶음으로만 산다** — `k̂₀ R̂_f` 는 `A_eff` 에 불변 · 순수 `k₀` 손실은 `k̂₀` 하나 · 막 성장은 `R̂_f` 하나. 원리상 두 묶음의 **같이 움직임(곱 일정)** 이 면적 손실의 서명이다.
- ③ `[인쇄]` "the range of R̂_f,p is [0, 0]" ⇒ **양극에서는 그 둘째 서명이 범위 선택으로 꺼져 있다** — 양극 면적 손실은 `k̂₀,p` 하나로만 가고(순수 곱 축퇴), 입자 통째 비연결 `u` 는 창 폭(`3Q/Δs` — LAM 과 같은 자리) · `σ̂_p`(×u · 감도 17 위 10^−3.8)로만 간다 ⇒ **이 묶음에서 양극 `u` 는 `LAM_PE` 와 사실상 같은 매개변수**(`ε_s` 형 LAM 과는 항등 · `c^max` 형과는 `σ̂_p` 하나 차이)(28호 SPM 판의 "항등" 이 DFN 에서도 범위 선택 덕에 거의 그대로 — 음극은 `R̂_f,n` 이 자유라 근사 축퇴).

**⚠ 이것이 곱을 푼 것은 아니다** — 묶음은 곱을 **선언하는** 처방이다: 곱을 한 매개변수로 바꾸면 그 묶음은 식별되지만 곱의 두 인자(`D ↔ R²` · `k₀ ↔ A_eff`)는 영영 입력 쪽으로 넘어간다 — 카드 물음(`A_eff` · `u` ↔ `LAM_PE`)은 **그 넘어간 쪽**에 있다. 후보 메모(처방 표로 올리지 않음 · 결정 대기): **"정규화 DFN 의 `(k̂₀, R̂_f)` 쌍은 면적 손실이면 곱 일정 · `k₀` 손실이면 `k̂₀` 만 · 막 성장이면 `R̂_f` 만 움직인다 — 두 묶음을 노화 축으로 같이 추정하면 면적 손실의 서명이 될 수 있으나, 막 저항 범위를 [0, 0] 으로 두면(이 편 양극) 그 채널이 처음부터 없다."** 처방 표 새 줄 0.

---

# 보류 결정 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(먀) — 이 편이 주는 근거 (결정 안 함)

| # | 결정 (요약) | 95호 근거 | 세기 |
|---|---|---|---|
| **(다)** | 28호 Bizeray(액체셀 도구)를 ASSB Q4 분모에 넣을지 | **이 편이 (다) 의 "닿는 논문" 목록에 직접 있다**(Khalik 2021) — 둘째 액체 식별성 도구 편: 구조적(35 → 24 구성 증명) + 실제적(직교화 순위 · 합성 다중 시작) · 28호와 달리 **모드 좌표(창 넷)를 식별 집합 안에 넣었고**, 그 좌표가 가장 약하다(경우 1 평형 채널 무정보 · Cell 1 범위 끝 · 합성 모형 오차 1.2 mV 에서 s_p,100% 가 범위 하한) — 분모에 넣든 안 넣든 "액체셀 도구 칸" 이 두 편이 된다 | **강** |
| **(체)** | 평형(OCV) 곡선의 출처 층위 표기 | EMF 측정법 인쇄 0(G3) · **Cell 2 의 두 EMF 가 21–59 mV(SOC 0.2–1) · 113–313 mV(≤0.1) 다르다**(그림 2 ↔ 3 `[재현·벡터]`) · 경우 1 = 문헌 흑연 U_n([23]) + EMF 정의형 U_p + 0–10 % 직선 교정 — 빌린 형상 오차 +6 … +54 mV 가 U_p 로 1:1 · 분해 쌍 ↔ 셀 EMF −9.5 … +13.5 mV | **강** |
| (헤) | 측정 입력의 역모형 층위 (measure-don't-fit 판) | 93호와 반대 처방의 표본 — "측정 매개변수" 모형(Sturm 2019 — 일부는 문헌값 · `[인쇄]`)이 출력 RMS 40.4 mV(부호 고정 −37.4)로 가장 나빴고, 분해 측정 OCP 쌍도 셀 EMF 를 ±10 mV 로만 재현 — **측정 입력에도 잔차 · 역모형(창 맞춤)이 있다** · 저자 결론 = "combine" | 중 |
| (세) | 인쇄 매개변수 표의 재풀이 폐합 검사 | 추정값 표 0 → 재풀이 불가 · 대신 지면 폐합: 표 4 무작위 기준 ✅(0.427 ↔ 0.43) · 그림 6 ↔ 그림 5(b) ✅(→ 14 개) · 그림 2 ↔ 3 EMF ❌ · 그림 8 ↔ 3 자료 길이 ❌(76.7 ↔ 56.7 분) | 중 |
| (치) | 모형 결론 옆 "배제 가정" 표기 | 결론 셋("12 of 22 sufficient" · "length … carefully selected" · "EMF modeling errors … large bias")의 조건: 셀 둘 · 회차 하나 · 출력 RMSE 기준 · 참값 하나 · 무잡음 · 같은 모형 · 오차 꼴 둘 · 입력 하나 · 온도 0 · 순위는 한 점 | 중 |
| (테) | 식별 편의 식별 산출물 표기 | 블록 지향은 아니나 같은 결손 — ① 식별된 값 · 불확실도 인쇄 0(β 상자 그림뿐) ② 검증 자료로 매개변수 수 · 자료 길이를 골랐고 Cell 2 검증은 추정 구간 포함 ③ 다중 시작 산포에 잔차 문턱 0 | 중 |
| (이) | 모형 값 인용 규칙 | 범위 = 문헌 값 묶음(대부분 측정 · Q 척도 가정) · Cell 1 추정값 10/22 가 범위 끝 — **범위가 정한 값**을 매개변수로 옮기지 않게(경계 접촉 표기) | 중 |
| (갸) | "단순성(입력 수)" 근거 명제의 척도 · 출력 유일성 | "12 out of all 22 … sufficient" = 출력 RMSE 평탄 기준 · 저자 스스로 출력 정확도 ↔ 물리 의미를 가른다(H1 · H2) — 척도 = 추정 매개변수 수 · 유일성 검사는 다중 시작(문턱 0)뿐 | 중 |
| (무) | `j₀(x)` 모양 선택지 | 경우 1 에서 창이 출력에 닿는 인쇄 경로가 **(12b) 의 `(ĉ_s,max − ĉ_s,e)^α_a ĉ_s^(1−α_a)` 하나** — `j₀(x)` 모양 선택이 곧 창 식별성을 정하는 구성 · `α_c = 1 − α_a`(본문 언급 0)가 그 모양과 묶음 정확성을 같이 정한다 | 중 |
| (차) | PyBaMM 면적 / `j₀` 노브 분리 forward | `[재현·대수]` 정규화 DFN 에서 반응 면적(`3ε_s/R_s` · A · δ)이 `k̂₀` 로 약분 — 면적 · `k₀` 는 한 묶음 · 갈리는 둘째 서명은 `R̂_f`(÷ `A_eff`)뿐이고 양극은 범위 [0, 0] — 면적 노브를 따로 둔 forward 는 이 묶음을 다시 푸는 것 | 중 |
| (가) | 29호 Q4 +0.5 (정적 ↔ 동적 축) | 액체 표본 — 경우 1 에서 정적(EMF) 채널은 창에 무정보 · 창은 동적 채널로만 · "EMF modeling errors affect the identifiability … significantly more than neglecting the concentration-dependency" | 약 |
| (페) | "입력 설계" 의 목적 표기 | 설계 처방이 FIM 이 아니라 "**EMF modeling errors are minimized**" · 자료 길이를 검증 RMSE 로 고름 · Cell 1 자료 원전 [38] = 등가회로 실험 설계(미열람) | 약 |
| (러) | 합성 truth `θ → LAM_PE` 결합 항 | `[해석·대수]` 정규화 DFN 에서 입자 통째 비연결 · `ε_s` 형 LAM 은 창 폭 + `R̂_f`(÷u) + `σ̂`(×u) 를 같이 · `c^max` 형 LAM 은 창 폭 하나 — 결합이 묶음 수준에서 자동으로 생기는 경로(양극은 R̂_f,p 고정으로 꺼짐) | 약 |
| (먀) · (냐) | 지목 기구 층위 확인 · 회고 인용 조건 복원 | 27호 기대("곱 쌍 ①–③ 묶음 도구 원전") — ② · ③ ✅ ① 반만(§(a) 5) · 결론의 "bias … reduced by tighter ranges" 가 시험 범위를 넘는다(D12) | 약 |
| (메) | 예치 원자료 교차 폐합 | 예치 0 → 그림 사이 폐합으로 대신: 둘 ✅(그림 6 ↔ 5b · 표 4 ↔ 그림 7) · 둘 ❌(그림 2 ↔ 3 · 그림 8 ↔ 3) | 약 |
| (제) | 모형 "일치" 의 잔차 표기 | 검증 = 출력 RMSE 하나 · 율별 끝 용량 0 · Cell 2 검증 = 추정 구간 포함 | 약 |
| (에) | 속도 상수의 i₀ 환산 표기 | `k̂₀` 단위가 α_a 에 묶임([s⁻¹·(m/mol)^(3(1−2α_a))] — α_a 0.48–0.52 에서 지수 ±0.12) · i₀ 환산 0 | 약 |

나머지 — (라)(마)(바)(사) 결정 · 반영됨, 그 밖의 글자는 **근거 0**(ASSB · 접촉 · 압력 · Li-In · 기준극 · 노화 사이클 · DRT · EIS · LLI 실측 · 압력 시계열 · 프로토콜 비교 · 비선형 진단이 이 편에 없다). **결정 안 함.**

## 새 판단 거리 (셋 — 글자는 호출자가 붙인다)

1. **재매개화 · 묶음의 최소성 표기** ((세) · (테) 의 묶음판으로 묶어도 됨) — 모형 · 추정 편이 "원 N 개를 묶어 M 개로" 를 쓸 때, 카드 · 개념 · 합성 truth 로 옮기기 전에 ① 남은 묶음이 식에 단독으로 나오는지(곱으로만 나오는 쌍 = 남은 정확한 대칭) ② 가정으로 줄인 것(`α_c = 1 − α_a` 등)과 항등으로 줄인 것 ③ 범위 [0, 0] · 측정 고정(Q)을 갈라 적게 할지 — 95호: 35 → 24(구성 증명) · (9a) `D̂_e p̂` · (11a) `κ̂ p̂` → 척도 대칭 1(≤23 `[재현·대수]`) · `α_c = 1 − α_a` 는 식 (12a) · (12b) 에만 · 그 가정이 `k̂₀` 묶음 정확성에 필요 · R̂_f,p [0, 0].
2. **다중 시작 · 합성 참값 시험의 '일관성 ↔ 정확성' 표기 (잔차 문턱 · 경계 접촉 · 무작위 기준)** — 추정 편의 다중 시작 산포 · 합성 참값 복원을 Q4 · 개념 · 합성 truth 로 옮길 때 ① 회차별 잔차와 문턱(근최적 집합 ↔ 수렴 실패) ② 범위 끝 몫 ③ 참값이 IQR 안인 몫 ④ 무작위 기준(균등 β RMSE ≈0.41–0.43) ⑤ 주입 모형 오차 ↔ 실셀 잔차 비 ⑥ 잡음 · 참값 개수를 같이 적게 할지 — 95호: 무잡음 · 같은 모형인데 출력 RMSE 중앙값 0.13 mV ≠ 0 · Cell 1 범위 끝 10/22 · 합성 참값 IQR 밖 14/22 · 1.2 ↔ 3.4–3.7 mV · 참값 하나 · NEW_MODEL_REQUIREMENTS §7-1 ①③⑤ 와 같은 축.
3. **"한쪽 전극 곡선을 빌리고 다른 쪽을 EMF 로 정의" 하는 평형 모형의 창 무정보 · 배분 오차 표기 + 분해 쌍 ↔ 셀 EMF 잔차 표기** ((체) 의 창 맞춤판으로 묶어도 됨) — 이런 구성(경우 1)의 창 · LLI · LAM 값을 옮길 때 "창은 OCV 채널에서 정의상 무정보(어느 창이든 EMF 정확 일치)" 와 빌린 곡선의 형상 오차가 다른 전극 곡선으로 1:1 간다는 것을, 분해 측정 쌍으로 창을 맞춘 구성(경우 2)은 쌍 ↔ 셀 EMF 잔차를 값 옆에 적게 할지 — 95호: `[인쇄]` "any choice between 0 and 1 … same EMF-SOC relation" · 빌린 흑연 U_n ↔ 측정(Si-흑연 — [24] 제목) +13–53 mV → U_p · [24] 쌍 ↔ 셀 EMF −9.5 … +13.5 mV · 그림 2 ↔ 3 EMF 21–59 mV · 우리 4-창 + γ_Si 는 경우 2.

---

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** | §3.1 의 창 목록 "s_n,0%, s_n,100%, s_p,0%, **s_n,100%**" 가 **세 번**(주의 문장 · 경우 1 · 경우 2) 같은 오기 — 넷째는 `s_p,100%` | p. 4 |
| **D2** | "U_p is calculated from the **EMF function shown in Fig. 3**" ↔ 그림 2 의 EMF(계산 U_p − 가정 U_n)가 그림 3 Cell 2 EMF 보다 +21 … +59 mV(SOC 0.2–1) · +113 … +313 mV(≤0.1) `[재현·벡터]` · 그림 2 EMF 는 [24] 쌍 EMF 와 ±13.5 mV · Cell 2 시작 전압 4.190 V > 그림 3 Cell 2 EMF 최댓값 4.168 V | p. 5 ↔ p. 6 |
| **D3** | 주입 오차 "approximately **1.2 mV** … **in the same range** as the errors shown in the upper plot of Fig. 6" ↔ 그림 6 위 RMS 3.42–3.71 mV `[재현·벡터]`(×0.32–0.35) | p. 9 ↔ p. 8 |
| **D4** | 그림 6 캡션 "obtained from using **60%** of Data 1 for **simulation** with 14 estimated parameters" ↔ §4.2 "only **90%** of Data 1 has been used for estimation" · "for simulation" 은 추정의 뜻으로 읽힘 | p. 8 ↔ p. 6 |
| **D5** | 그림 7 여섯째 · 그림 8 아래 줄 "**both modifications**" ↔ 본문은 수정 하나씩만 서술 · 표 4 에 열 없음 · "the MRMSE of the parameters with both of the modifications is almost equal to …" 가 어느 값인지 불명(두 단일 수정 열 0.43 · 0.44 로 읽힘) | p. 8–9 |
| **D6** | "especially for the **first 10 parameters**, the estimated parameters are close to the true parameters, with a relatively small variability" ↔ 그림 7 합성 패널에서 첫 10 중 **6**(#1 · 2 · 3 · 4 · 8 · 9)의 참값이 IQR 밖 `[도표·벡터]`(중앙값 거리로는 작음 — 첫 9 평균 0.088) | p. 9 ↔ 그림 7 |
| **D7** | 그림 8 시간 축 **0–76.7 분** · 첫 패널만 "**Time [s]**" ↔ 합성 입력 "with the same input data used for simulation"(Data 1 = **56.7 분** — 그림 3 · 그림 6 SoC 폭으로 자기 정합) | p. 9 ↔ p. 6 · 8 |
| **D8** | "by setting β_i = 0.5 **in (18)**" · "β_i = −0.3 **in (18)**" · "β_i = 1.3 **in (18)**" ↔ (18) 은 EMF 식 — 정규화는 **(19)** | p. 6 · 8 |
| **D9** | 표 1(b) (12a) · (12b) 가 `α_c` 자리에 `1 − α_a` ↔ 본문 · 표 3 은 이 가정을 적지 않음(표 3 에 `α_a` 만) · [25] 의 "further assumption … α_a = α_c = 0.5" 는 적으면서 자기 가정은 안 적음 — `[재현·대수]` 이 가정이 `k̂₀` 묶음 정확성에 필요 | p. 3 ↔ p. 4 |
| D10 | (7) `Q = AFδε c^max(s_i,100% − s_i,0%)` — 양극은 `s_p,100% < s_p,0%`(표 3 범위) 라 우변 음수 · 절댓값 표기 0 · (12b) 끝 인자 `ĉ_s^(1−α_a)`(표면 `ĉ_s,e` 여야) | p. 3 |
| D11 | 단위: 표 2 `D_e` "[m²]" · `D_s` "[m/s]"(m² s⁻¹ 여야) · 표 3 `p̂` "[–]"(ε^p/δ = m⁻¹) · `D̂_e` "[Cs⁻¹]" · `κ̂` "[Ω⁻¹]"(각각 · m 이 붙어야 — 곱 `D̂_e p̂` · `κ̂ p̂` 만 표기와 맞음) | p. 3–4 |
| D12 | 결론 "We have further shown that this **bias** and variability can be reduced by determining tighter parameter ranges" ↔ 참값 있는 좁힘 시험 0(합성은 원 범위만 · 범위 비교는 Cell 1 — 참값 없음 · 넓힐 때 산포 ↑ 만) | p. 10 ↔ p. 8 |
| D13 | 서론 "simplified models in the **time domain** [11–16]" 에 [13] Bizeray(= 28호 — 식별성은 주파수 영역 전달함수 · 28호 digest 전사) | p. 2 |
| D14 | §4.5 "**identifiability of the parameters is in principle not a large issue** when the desire is to obtain parameters that lead to a good representation of the considered states" ↔ 같은 지면 표 4 합성(모형 오차 0) β RMSE 0.30 ↔ 무작위 0.43 · 참값 IQR 밖 14/22 — 문장은 **상태** 기준이나 "identifiability" 를 상태 재현으로 바꿔 쓴다 | p. 10 ↔ p. 9 |
| D15 | 그림 2 보정 직선 기울기 0.545 V/SOC ↔ 인쇄 규칙(10–40 % 평균 기울기) 0.564 `[도표·벡터]`(−3 % · SOC 0 에서 7.5 mV) · "MRSE" 오기(p. 9) · 표 4 단위 0 | p. 5 · 9 |

---

# 이 편이 우리 프로젝트에 주는 것 (정리)

1. **모드 좌표(창)가 식별 집합 안에 든 액체 DFN 추정의 실측 · 합성 표본 — 그리고 그 좌표가 가장 약하다.** 창 끝 넷은 경우 1 에서 평형 채널에 정의상 무정보이고(인쇄), 실셀 Cell 1 에서 셋이 범위 끝에, 합성 모형 오차 1.2 mV 에서 `s_p,100%` 가 범위 하한에 붙는다 `[도표·벡터]`. 우리 `degradation-degeneracy/` 가 합성 truth 로 채점하는 "맞는 곡선 ≠ 맞는 성분 분할" 의 DFN 판이다 — 출력 RMSE 가 1.2 mV 로 맞는 동안 양극 이용 범위 위끝이 사전 범위 폭만큼 움직였다(우리 쪽 수치는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본 — 여기 옮기지 않는다).
2. **형상 가정이 OCV 채널의 창 정보량을 정한다**(`[해석]`) — 경우 2(형상 고정 · 우리 α·β)는 OCV 가 창 조합을 정하고([[np-lip-ocv-reparametrization]] 2 자유도), 경우 1(한쪽 형상 자유)은 0 을 정한다. 우리 γ_Si 는 그 사이(음극 형상을 한 매개변수로 연다) — γ_Si 를 풀수록 창의 OCV 정보가 줄어드는 방향이 같은 구조다.
3. **분해 반쪽전지 쌍의 셀 EMF 잔차 ±10 mV**(`[재현·벡터]` · Ni-rich ‖ Si-흑연 18650 — [24] 제목) — 형상 불변 가정의 잔차 크기 참고값 하나(액체 · 한 셀 · 측정법 미인쇄). 우리 합성 truth 의 형상 오차 주입 크기를 고를 때의 근거 후보.
4. **NEW_MODEL_REQUIREMENTS §7 의 둘을 값싸게** — ② 조건수: 피벗 QR `|r₁₁|/|r_kk|` 하한(한 점 · 정규화 의존) · ③ 경계 접촉: 범위 끝 몫 + 범위 확장 시험. ①⑤(`tol` 있는 폭)는 이 편에 없다 — 다중 시작 산포를 폭으로 읽지 않는다.
5. **곱을 "선언" 하는 처방의 원형** — 묶음은 곱의 두 인자를 입력 쪽으로 넘긴다; 카드 물음(`A_eff` · `u` ↔ `LAM_PE`)은 넘어간 쪽에 있다 — 정규화 DFN 에서 양극 `u` 는 창 폭(LAM 자리)으로, `A_eff` 는 `k̂₀,p` 로 간다(양극 `R̂_f,p` [0, 0]).

---

# 후속 후보 (원전 우선 — 지목 수는 위키 digest 의 후속 절 grep 으로 센 값)

| 등급 | 서지 (PDF 목록 번호) | 지목 (후속 절) | 왜 | 축 |
|---|---|---|---|---|
| ★★★ | **Sturm J., Rheinfeld A., Zilberman I., Spingler F.B., Kosch S., Frie F., Jossen A. 2019** — *J. Power Sources* 412, 204 ([24]) | **95** = 1 (새) | Cell 2 분해 매개변수화 — 측정 Si-흑연 U_n · Ni-rich U_p(그림 2) · 분해 모형(그림 6 RMS 40 mV · 부호 고정) · 제목 "inhomogeneities … nickel-rich, silicon-graphite … fast charging" — 우리 γ_Si 축의 측정 반쪽전지 곡선 원전 후보 · ⚠ 액체셀 도구 | Q8 · γ_Si |
| ★★★ | **Jobman R., Trimboli M.S., Plett G.L. 2015** — *J. Energy Chall. Mech.* 2(2), 45 ([25]) | **95** = 1 (새) | 정규화 · 묶음의 원형(24 · α_a = α_c = 0.5 · 유효 계수 정식화 — 이 편의 남은 척도 대칭이 거기에도 있는지) · Plett 계보 = 4차 묶음 파일 56(Lu 2022)의 앞 · ⚠ 액체셀 도구 | Q4 |
| ★★ | **Ecker M., Tran T.K.D., Dechent P., Käbitz S., Warnecke A., Sauer D.U. 2015** — *J. Electrochem. Soc.* 162, A1836 ([23]) | 28 · 93 · **95** = **3** (재지목) | 범위의 원전 · **그림 2 의 빌린 흑연 U_n** · 분해 창 맞춤 방법 — 이 편 §(c) 3 의 +13–53 mV 배분 오차의 출발 곡선 · ⚠ 액체셀 도구 | Q8 · Q3 |
| ★★ | **Lund B.F., Foss B.A. 2008** — *Automatica* 44, 278 ([30]) | **95** = 1 (새) | 직교화 순위의 원전 — §7-1 ② 조건수의 하한판 · 일반 도구 | Q4 도구 |
| ★★ | **Jin N., Danilov D.L., Van den Hof P.M., Donkers M. 2018** — *Int. J. Energy Res.* 42, 2417 ([18]) | **95** = 1 (새) | 같은 그룹(TU/e)의 직전 판 — 두 단계 절차 + 직교화 순위를 **묶지 않은** 모형에 · 91호 저자 Danilov 공저 · ⚠ 액체셀 도구 | Q4 |
| ★★ | **Chu Z., Jobman R., Rodríguez A., Plett G.L., Trimboli M.S., Feng X., Ouyang M. 2020** — *J. Energy Storage* 27, 101101 ([22]) | **95** = 1 (새) | 기준극 기반 묶음 식별(Part II) — Q5 의 액체 쪽 · "too many parameters … unexpected uncertainty" 직관의 출처 | Q4 · Q5 |
| ★★ | **Ramadesigan V., Chen K., Burns N.A., Boovaragavan V., Braatz R.D., Subramanian V.R. 2011** — *J. Electrochem. Soc.* 158, A1048 ([27]) | **95** = 1 (새) | 재정식 모형으로 매개변수 추정 + **용량 감쇠 분석** — 매개변수의 노화 축 추적(모드 축의 시간판) · 원장의 Ramadesigan 2012(*JES* 159, R31 리뷰)와 **다른 편** | Q4 · 노화 |
| ★★ | **Schmalstieg J., Rahe C., Ecker M., Sauer D.U. 2018** — *J. Electrochem. Soc.* 165, A3799 ([26]) | **95** = 1 (새) | 분해 전 셀 매개변수화 · 범위 · 창 맞춤("minimized in some way" 의 방법 쪽) | Q3 · Q8 |
| ★ | **Beelen H.P.G.J., Bergveld H.J., Donkers M.C.F. 2018** — *CCTA*, IEEE, 1526 ([38]) | **95** = 1 (새) | Cell 1 자료 원전 + 등가회로 실험 설계(34호 입력 설계 줄) | 자료 · Q4 |
| ★ | **Bergveld H.J., Kruijt W.S., Notten P.H.L. 2002** — *Battery Management Systems: Design by Modeling*, Kluwer ([34]) | **95** = 1 (새) | EMF 결정 기법 개관(이 편 G3 의 근거 문헌) — 91호 후속의 Pop 2008 책(★★)과 같은 연구망 · 다른 책 | Q8 · OCV |
| ★ | **Zhou X., Huang J. 2020** — *J. Energy Storage* 31, 101629 ([17]) | **95** = 1 (새) | 임피던스로 물리 매개변수 식별(다출력 RVR) | Q4 · Q2 |
| ★ | **Schmidt A.P., Bitzer M., Imre A.W., Guzzella L. 2010** — *J. Power Sources* 195, 5071 ([16]) | **95** = 1 (새) | 실험 주도 매개변수화 · 경우 1 관행(U_n 문헌) — kouhestani2022 후속의 Schmidt 2010 *JPS* 195, **7634** 와 **다른 편** | Q8 |
| ★ | **Sturm J. … Jossen A. 2019** — *J. Power Sources* 436, 226834 ([39]) | **95** = 1 (새) | 같은 Cell 2 — 임베디드용 물리 모형 적합성 | 자료 |
| ☆ | Forman J.C., Moura S.J., Stein J.L., Fathy H.K. 2011 *ACC* 362–369([19]) | 행 없음 — 원장 Forman 2012 *JPS* 행에 꼬리만 | 학회 판 · 이 편 "identifiability of the DFN model is poor" 두 문장의 근거 | Q4 |
| ☆ | Marcicki 2013([20]) · Zhang L. 2014([21]) · Masoudi 2015([12]) · Namor 2017([14]) · Pang H. 2019([15]) · Chu 2019 Part I([31]) | 행 없음 | 매개변수화 목록 | — |
| ☆ | [1]–[10] · [28] · [29] · [32] · [35]–[37] · [40] | 행 없음 | 배경 · 구현 · 범위 | — |

**원장 행이 있으나 재지목 안 함**(이 편 쓰임이 목록 인용): [11] Santhanagopalan · Guo · White 2007 *JES* 154, A198(원장 28 \| 1 — 시간 영역 목록 [11–16]) · [33] Smith & Wang 2006 *JPS* 161, 628(원장 49 · 92 묶음 행 — "as done in, e.g., [18,33]").

**흡수된 편(교차 — 지목 아님)**: [13] 28호 Bizeray 2019.

**4차 묶음 13 편과의 관계**: 이 편은 **어느 편도 인용하지 않는다**(40 번호 전수 대조 — Danilov 2011 · Firouz 2020 · Bielefeld 2023 · Schmidt 2024 · Lu 2022(파일 56 — 이 편보다 뒤) · Koerver 2018 · Raijmakers 2020 · Kim 2019 · Deng 2021 · Danilov & Notten 2008 · Xie 2008 · Shao 2022 · Ansah 2021) — 파일 51 Danilov 2011 과는 같은 Eindhoven 연구망([18] Danilov 공저 · [34] Notten 공저)이고 파일 56 Lu 2022 와는 같은 Plett 계보([22] · [25] · [31])다.

**지목 누락 0** — 이 편 참고문헌 중 앞 호 후속 절에 ★ 이상으로 있던 편은 Ecker 2015(28 · 93 — 원장 행 있음) · Santhanagopalan 2007(28 — 행 있음) · Smith & Wang 2006(49 — 등급 칸 없는 옛 후속 표 · 묶음 행 있음)뿐이다. Forman 2012 *JPS*(28호 ★★★★ — 행 있음)는 이 편이 인용한 판(2011 *ACC*)과 다른 편.

---

# 이 digest 가 주장하지 않는 것

1. **이 방법이 쓸모없다고 하지 않는다** — 묶음은 (`α_c = 1 − α_a` 아래) 정확하고, 12 개로 출력 RMSE 가 평탄해지는 것은 그림에 선다. 걸린 것은 24 의 식별성 증명 0 · 남은 척도 대칭 · 경우 1 창 무정보 · 결론의 조건(셀 둘 · 회차 하나 · 참값 하나 · 무잡음)이다.
2. **남은 척도 대칭이 저자 구현에도 그대로 있다고 단정하지 않는다** — 인쇄 식 (9a) · (11a) 위의 대수이고, 저자 툴박스([28])가 영역 경계 · 이산화에서 `p̂` 를 따로 쓰는지는 미확인이다. 사전 상자는 그 대칭을 `κ̂` 범위(×2.86)로 자른다.
3. **그림 2 ↔ 그림 3 의 EMF 차가 저자 계산 오류라고 단정하지 않는다** — 서로 다른 측정(의사 OCV ↔ 전극 쌍)일 수 있고, 측정법이 미인쇄라는 것까지다(21–59 mV 는 벡터 판독 `[재현·벡터]`).
4. **분해 매개변수 모형(Sturm 2019)이 틀렸다고 하지 않는다** — 부호 고정 오프셋(평균 −37 mV)의 원인(EMF · 온도 · 초기 SoC · 저항 · 문헌값 몫)은 지면에서 가를 수 없고, 비교 조건이 미인쇄다.
5. **Cell 1 이 ≈10.5 Ah 라고 확정하지 않는다** — 그림 6 의 SoC 가 쿨롱 계수라는 가정 위의 `[재현·가정]` 이다(세 자료 1 % 일치 · 시작 전압 ±4 mV 는 그 가정과 정합).
6. **Cell 2 가 특정 상용 셀이라고 하지 않는다** — "18650 nickel-rich, silicon-graphite" 는 참고문헌 [24] 제목이고 본문은 화학 · 형식을 적지 않는다. [[halfcell-ocp-shape-invariance]] 의 같은 계열 셀과 같은 셀인지는 모른다.
7. **"100 % 에서 과적합" 이 틀렸다고 하지 않는다** — 다른 국소 최소로 간 것과 이 자료로 가를 수 없다는 것까지다(회차 하나 · 같은 크기의 요동).
8. **Forman 2011 *ACC* 가 Forman 2012 *JPS* 와 다른 편이라는 판단은 서지(학회 · 쪽 · 제목)로만** 한다 — 두 원문 다 미열람이고, 이 편의 "identifiability … poor [19]" 가 2011 판의 어느 결과를 가리키는지는 원문으로만 닫힌다.
