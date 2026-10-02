---
title: "Lu D., Trimboli M.S., Fan G., Wang Y., Plett G.L. 2022 — Nondestructive EIS Testing to Estimate a Subset of Physics-based-model Parameter Values for Lithium-ion Cells (J. Electrochem. Soc. 169, 080504)"
source_url: local-upload/56._Nondestructive_EIS_testing_to_estimate_a_subset_of_physics-based-model_parameter_values_for_lithium-ion_cells.pdf
source_url_note: "본문 PDF 29 쪽(IOP 판 — p. 1 = 내려받기 표지 · 논문 지면 p. 2–29 · 쪽 번호 인쇄 0 · p. 23 가로 쪽) 5,151,189 B · 업로드 접두사 1fe29eab · 4차 묶음 파일 56 · ⚠ 액체셀 도구 논문(ASSB 아님 — 28 · 95호 선례 · 도구 칸) · SI 없음(보충 언급 0 — 부록은 본문 안 p. 22–28) · 자료 · 코드 공개 0 — 자동 크롭 19(그림 1–19 · 표 검출 0) + 수동 10(표 I–X 단독 — 쪽 렌더 300 dpi · 표 VII 250 dpi) = 29 전부 봤다 · 그림 19 개 전부 래스터(벡터 0) — 판독은 화소 좌표 · 식 · 첨자는 쪽 렌더로 확인(판독용 · 커밋 안 함) · p. 1 표지의 내려받기 IP 는 옮기지 않음"
source_doi: 10.1149/1945-7111/ac824a
source_license: "© 2022 The Electrochemical Society(ECS) · Published on behalf of ECS by IOP Publishing Limited(인쇄) · 꼬리말 'All rights, including for text and data mining, AI training, and similar technologies, are reserved.' · CC · 오픈 액세스 표기 0 · 구독본으로 다룬다 — 이 digest 는 인용 · 요약 · 재현 계산만 담는다(그림 크롭은 위키 관례대로 raw/figures 에 — 변형 없는 잘라내기)"
pdf_sha256: ffab9252951dc35adbdc5a4f8246b75cad4d6a75388b830e81136fd7cf7815b8
ingested: 2026-10-02
sha256: f65931378a0d221b5f64dfa33b30f93ddd9f8228934ae74c9e01cadc27a7f44b
---
# 수집 목적

`assb` 섹션 **96호** — **4차 묶음 파일 56**(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 요청 14 편 중 여섯째 · 2026-10-02 사용자 공급 · 파일 51–64 = 91–104호를 받은 순서대로). ⚠ **이 편은 ASSB 논문이 아니다 — 액체 전해질 Li-ion 셀의 EIS 기반 물리 모형 매개변수 추정 도구 논문이다.** 28호(Bizeray 2019 — 액체 SPM · EIS 식별성) · 95호(Khalik 2021 — 액체 DFN 묶음 · 감도) 선례대로 `assb` 번호는 받되 **"ASSB 아님(도구 칸)"** 으로 다루고, 채움표 Q 칸은 도구 칸 규칙(28 · 34 · 36 · 95호 행 형식)대로 적는다. 닻은 `questions/assb-contact-loss-vs-lampe.md` 의 **Q4(유일성 · 식별성)** 이고, 이 편이 더 직접 닿는 곳은 ① 개념 [[drt-peak-count-nonidentifiability]](이 편은 DRT 로 Nyquist 혹 하나를 두 전극 시간 상수로 가른다고 쓴다) ② [[spm-grouped-parameter-identifiability]](28호의 "선형화하면 식별 집합이 줄어든다" 의 DFNe 판 — 이 편 스스로 "nonlinearly identifiable but not linearly identifiable" 을 인쇄한다) ③ 2026-10-02 세미나 3번째 논문 `sun2025_dl-eis-degradation-mode-diagnostics`(같은 EIS 에서 **학습으로** 열화 모드를 읽는 편 — 이 편은 **모형으로** 물리 매개변수를 읽는다)다. 우리 쪽 수치(`degradation-degeneracy/` · `mode-observability`)는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본이고 여기 옮기지 않는다.

University of Colorado Colorado Springs(UCCS) 전기 · 컴퓨터공학과 **Dongliang Lu · M. Scott Trimboli · Gregory L. Plett**(교신)와 Cummins Inc. 연구소 **Guodong Fan · Yujun Wang** 의 *J. Electrochem. Soc.* 2022 편. 본문 첫 문장이 `[인쇄]` "This paper is the **final installment in a series of articles** that collectively shows how to estimate parameter values for lumped-parameter physics-based models of lithium-ion cells **without requiring cell teardown**" 이고, 서론이 그 **일곱 편 연재**(i 식별 가능한 집약 모형 [2] · ii 전극 OCP [3] · iii 셀 OCV · 용량 · 전극 창 [4] · iv 방전 시험으로 양극 OCP 보정 [5] · v 펄스 저항 [6] · **vi EIS(이 편)** · vii 의사 정상 상태 방전으로 ψ̄ [7])를 순서대로 적는다. 이 편이 하는 일: DFN 에 이중층(R̄dl–C̄dl) · MSMR 계면 동역학 · SOC 의존 고체 확산(Darken 항) · CPE 둘을 더한 **DFNe** 의 **집약 매개변수 모형(LPM)** 에 대해 **닫힌 꼴 소신호 전달함수(TF)** 로 셀 임피던스를 계산하고, 실셀 19 SOC(가상 셀 20) × 142 주파수(`[재현]` — 원문은 주파수 격자만 인쇄)의 EIS 를 비선형 최적화(MATLAB particleswarm + fmincon)로 맞춰 **집약 매개변수 13 개 + 갤러리별 반응 속도 상수**를 낸다 — 초기값은 **DRT 봉우리 분리**(Nyquist 혹 → 두 전극 계면 C̄dl · R̄ct)로, 실험실 배선 인덕턴스는 **일반화 DRT(GDRT)** 로 걷어낸다. 검증은 **가상 셀 하나**(같은 모형 + 인덕턴스 + 0.5 % 잡음)와 **실셀 하나**(Panasonic 25 Ah 각형 흑연//NMC — Ford C-MAX Energi PHEV 팩 · 25 °C). **열화 · 노화 · 모드(LLI · LAM) · 접촉 · 압력 · 고체전해질 0.**

들어온 경로: 원장 행(도착 표시 전 원문 그대로) "| ★★★ | **Lu·Trimboli·Fan·Wang·Plett 2022** — *J. Electrochem. Soc.* **169**, 080504 | 27 | 1 | **Q4** | 같은 문장의 두 번째 인용 — **집약(lumped) 파라미터 추정** (공백 1번 후보) |". 위키 grep(`Lu, Trimboli` · `Lu·Trimboli` · `080504` · `Plett` · `Trimboli`): **27호**(Sinzig 2024 — [28] · 후속 표 :376 **★★★★** "같은 문장의 둘째 인용 — (`[추론]` 제목 미인쇄) Plett 계보의 **집약(lumped) 파라미터 추정**, 곱 쌍을 처음부터 묶어 추정하는 쪽 \| **Q4**") · 카드 :5094(27호 Status Log "후속 … 2순위 = Lu, Trimboli, Fan, Wang, Plett 2022") · 92 · 94 · 95호 후속 절의 "4차 묶음 13 편과의 관계" 문장(교차 기록 — 지목 아님) · 95호 후속 표 :727 Jobman 2015 행의 "Plett 계보 = 4차 묶음 파일 56(Lu 2022)의 앞"(교차) · §3-b (다) 의 "닿는 논문" 목록에 이 편 이름. **지목은 27호 후속 절 하나 = 1 — 원장 "27 \| 1" 과 일치**(등급은 27호 ★★★★ ↔ 원장 ★★★ — 표시만). 이 편은 우리 digest **하나**를 인용한다(**51호 Illig 2012 = [27]** — §인용 대조) · 4차 묶음 다른 13 편은 **인용 0**(87 번호 전수 대조).

이 digest 의 일 (지시):

1. **(a) 무엇을 EIS 로 추정하는가** — 집약 매개변수 13 개 + 반응 속도 상수(초록 인쇄)의 목록과 정의 · 연재 앞 편이 이미 정한 것(OCP · 용량 · 창 · 확산 초기값 등)과의 분담 · 닫힌 꼴 주파수 응답(확장 DFN) 맞춤의 비용 · 가중 · 초기값(DRT — 그림 2) · 경계.
2. **(b) 식별성(Q4)** — 13 개가 EIS 로 **유일하게** 정해지는가를 보였는가(신뢰구간 · 상관 · 감도 · 합성 참값) · "a single Nyquist bump can arise from the combination of two (or more) time constants"(그림 2) 를 저자가 어떻게 다루는가 — [[drt-peak-count-nonidentifiability]] 와 대조 · Q4 어휘 전수.
3. **(c) 검증** — 추정값을 독립 측정(해체 · GITT 등)과 대조했는가 · 셀 종류 · 온도 · SOC.
4. **(d) EIS 를 '관측 추가' 로 쓰는 우리 물음** — 세미나 3번째 논문(학습형)과 이 편(모형 기반)이 같은 EIS 에서 다른 것을 읽는다: 이 편 방식이 열화 모드(LLI · LAM)를 가르는 데 쓰일 수 있는가(`[해석]` · 조건 붙여).
5. **(e) 후속 후보** — 연재 앞 편들(우리 위키에 없는 것만 · 액체셀 도구 표시 · 지목 수는 각 digest 후속 절 grep 값만 · 4차 묶음 13 편은 "4차 묶음 파일 NN").

⚠ **표기 규약**: `[인쇄]` = 원문이 실제로 쓴 것 · `[도표]` = 그림을 눈으로 읽은 값(판독 폭 표시) · **`[도표·화소]`** = 래스터 그림의 화소 좌표를 축 눈금 · 격자선으로 보정해 읽은 값(표지 중심 · 곡선 극대 · 점선 위치 — 판독 폭 ≈±0.02(그림 11–13 정규화 축 · 0–3.5 범위) · ±0.002(그림 11–12(d) 0.9–1 축) · ±0.3(그림 13(b) 0–25 축) · ±0.05 decade(그림 6 · 17(f) 로그 축)) · `[재현]` = 원문 수치 · 식으로 우리가 다시 계산 · `[재현·가정]` = 가정이 붙은 재현(가정을 같이 적는다) · **`[재현·대수]`** = 인쇄된 식만으로 한 대수(수치 0) · `[해석]` = 우리 해석 · **"(N호 digest 전사)"** = 이 편이 인용한 원 논문을 이 세션에서 다시 열지 않고 우리 위키 digest 에 전사된 값으로 대조한 것. **`[데이터]` 0** — 이 편은 원자료 · 코드를 예치하지 않았다(공개 진술 0). 그림 19 개가 **전부 래스터**(벡터 0)라 판독은 화소 좌표다.

⚠ **측정 · 인용 · 모형 · 적합 구분**: 이 편 안의 수치는 ① **이 편의 측정**(Panasonic 셀 EIS — 19 SOC · 25 °C · 그림 15 · 17 · 표 IV) ② **연재 앞 편 값의 재사용**(OCP · MSMR 표 V ← [3] · [5] · 창 θ0 · θ100 · Q ← [4] · [5] · 펄스 매개변수 ← [6] · ψ̄ ← [7] PSS 방전 · 펄스 저항 재식별 그림 16 — 자료 출처 [6] 로 읽힘) ③ **모형 값**(가상 셀 참값 표 VIII · IX — 출처 미인쇄 · 그림 3 · 5 · 6 · 9 · 10 · 14 · 18 · 19 는 모형 출력) ④ **적합 값**(표 VI · 그림 11–13 · 15(e–f) · 17(e–f) · 표 II · 표 X 근사) 넷이다. 넷을 섞지 않는다.

⚠ **쪽 표기**: IOP 판 29 쪽 — **p. 1 = IOP 내려받기 표지**(인쇄 지면 아님 · "This content was downloaded from IP address … on 02/10/2026 at 13:45" — IP 주소는 옮기지 않음 · "You may also like" 추천 세 편은 IOP 추천이지 이 편 참고문헌이 아니다), 논문 지면은 p. 2–29(꼬리말 "Journal of The Electrochemical Society, 2022 169 080504" · 쪽 번호 인쇄 0 · PageLabels = PDF 쪽 1–29 · p. 23 은 가로 쪽 — 표 VII). 이 digest 는 PDF 쪽 "p. 14" 로 적는다(94호 선례).

---

# 판정 먼저

1. ★★★★ **(a) EIS 가 추정하는 것 — "13 개 + 반응 속도 상수" 는 `p_EIS^lin` 의 열셋(R_c 포함)과 갤러리 열하나이고, 모드 좌표(Q · θ0 · θ100)와 OCP 는 연재 앞 시험의 입력이다.** `[인쇄]` 초록 "to identify **thirteen lumped parameters plus multiple reaction-rate constants**" ↔ p. 14 "it can identify: `p_EIS^lin = {D̄s,ref^r, n_f^r, C̄dl^r, n_dl^r, k̄0^r, n̄e^r/ψ̄, κ̄D/ψ̄, R_c}`" — `[재현]` 13 = D̄s,ref(n · p) 2 + n_f 2 + C̄dl 2 + n_dl 2 + n̄e/ψ̄(n · s · p) 3 + κ̄D/ψ̄ 1 + **R_c 1**(LPM 밖 — 케이블 ↔ 집전체 접촉 저항 · 각주 d) · k̄0,j = 실셀 표 V 갤러리 흑연 6 + NMC 5 = 11(가상 셀 표 IX 7 + 4 = 11). 분담(표 I · 서론): OCP[3] → U_ocp^n · MSMR{U0j, Xj, ωj}^n · OCV[4] → **Q · U_ocv(z) · θ0^n · θ100^n** · 방전[5] → U_ocp^p · MSMR^p · **θ0^p · θ100^p**(참고 D̄̂s,ref) · 펄스[6] → α^r · κ̄^r · σ̄^r · R̄f^r · R̄dl^r(참고 k̄̂0) · **EIS(이 편)** → D̄s,ref^r · n_f^r · C̄dl^r · n_dl^r · k̄0^r(참고 n̄e^r/ψ̄ · κ̄D/ψ̄) · 방전[7] PSS → ψ̄ · n̄e^r · κ̄D. 비용 = 식 [18] — 실수부 · 허수부 오차를 각 자료 |Z| 로 나눈 **상대 제곱합**(M 주파수 × N SOC 균등 가중 — Strategy 1) / SOC 마다 따로(Strategy 2 · 무번호 식) · 최적화 = particleswarm(전역) + fmincon 혼성 · **48 h 제한** · 실행 하나(MATLAB 기본 시드). 초기값 = **DRT 봉우리 반전**(계면 R̄ct · C̄dl · n_dl → R̄ct(θ) 에 k̄0,j 곁최적화) + 연재 앞 시험값 + 부록 식(κ̄D,0 = 2R(0.363 − 1)(1 + 3)/F = −4.39×10⁻⁴ V K⁻¹ · ψ̄0 = RT/(F²(1 − 0.363)) = 4.18×10⁻⁷ mol S⁻¹ s⁻¹ · n̄e,0 = Q/100 · R̄dl,0 10⁻⁴ Ω · R̄f,0 10⁻⁶ Ω · n 0.95 · σ̄n 10⁸ · σ̄p 10⁶ S · κ̄s,0 5×10³ S · K_κ 0.5 · K_n̄e 1) · 경계 인쇄(부록 — §(a) 3). `[재현]` 초기화 식이 그림 11(e) 초기 X(κ̄D/ψ̄ ≈2.12 `[도표·화소]` ↔ 식 2.13)와 그림 11–12(b) X(n̄e/ψ̄ 0.23 · 0.36 · 0.28)를 닫는다. **DRT 는 초기값 · 인덕턴스 보정 도구**이고 최종 추정은 TF 모형 회귀다.
2. ★★★★ **(b) 식별성 — 구조적 식별성은 인용(학회 판 Ref. 2)으로 주장하고, 소신호 비식별 둘은 손 분석으로 인쇄했으며, 합성 시험은 '같은 모형 · 잡음 실현 하나 · 실행 하나' 이고 그 안에서도 전체 집합의 다섯이 19–64 % 어긋난다 — 신뢰구간 · FIM · 상관 0.** `[인쇄]` "We know from Ref. 2 that all parameters of the PDE version of the LPM are identifiable. However, … not all parameters of the linearized TF model turn out to be identifiable … the LPM is '**nonlinearly identifiable**' but '**not linearly identifiable**'" · "parameters ψ̄, n̄e^r, and κ̄D never appear alone; they always occur as ratios of n̄e^r/ψ̄ and κ̄D/ψ̄"(도출 "some detailed analysis" — 지면 0 · `[재현·대수]` 부록 계수 μ₁ ∝ 1/ψ̄ · μ₂ · τ₂ · Λ₃^s 는 비만 · j = c(−ψ̄κ̄Λ² + n̄e s) 에서 (n̄e, ψ̄, κ̄D) → λ(·) 가 상쇄 ✅) · "the impact of **R_c and 1/κ̄^s** on the full-cell impedance are identical; i.e., they cannot be separated in any linear way". 합성 = 가상 셀 하나(표 VIII · IX) · **같은 TF 모형**(역범죄) + 배선 인덕턴스(GDRT 로 제거) + 곱셈 잡음 ε 0.5 %. `[도표·화소]` **부분 집합**(펄스 매개변수 참값 고정 · 그림 11): 대부분 ±1–5 % · **n̄e^s/ψ̄ 1.48**. **전체 집합**(그림 12 · 13): n̄e^n/ψ̄ 1.20 · **n̄e^s/ψ̄ 0.48** · n̄e^p/ψ̄ 1.25 · κ̄D/ψ̄ 1.19 · **R_c 1.64**(초기 X = 1.0 — 참값에서 출발해 멀어짐) · σ̄^p ≈1.66 · κ̄^p ≈1.44 · κ̄^n ≈1.29 · κ̄^s ≈0.88 · R̄f^n ≈0.4 · k̄0,j^n 0.74–1.19 · **j6 · j7 은 축 밖** — `[재현]` 표 X 근사(초기값)가 참값의 ×12,867 · ×4,107 이고 경계가 "one order of magnitude around their initial values" 라 **참값이 하한의 1/1,287 · 1/411 — 도달 불가** · 출력 잔차 ≲0.04 mΩ(그림 14). ↔ `[인쇄]` 초록 "Parameter estimates found in the simulation study are **highly accurate**" · 결론 "able to find all parameter values of interest with **very good accuracies**". `[해석]` R_c +0.64 mΩ 는 저자가 이름 부른 1/κ̄^s(참 0.17 mΩ — 혼자서는 못 흡수)보다 **R̄f^n −≈0.6 mΩ**(그림 13(b) · 판독 폭 ±0.3) 와 크기가 맞다 — 직렬 저항 셋(R_c · 1/κ̄^s · R̄f^n)이 한 골짜기. **DRT 봉우리 수**: `[인쇄]` "a single Nyquist bump can arise from the combination of two (or more) time constants … The DRT procedure can help uncover the individual time constants" 를 쓰고 바로 "**we are unable to distinguish the ordering of time constants from the two electrodes. Presently, we simply assume** that the smaller time constant … is associated to the negative electrode" — 배정은 가정이다. 저자 자신의 그림이 그 위층을 보여 준다(본문 언급 0): `[도표·화소]` 그림 5(b) **CPE 하나(n_DL 0.9) → γ(τ) 극대 셋** · 그림 6(a) **참 모형 가상 셀(과정 다섯 — 계면 둘 · 전해질 · 고체 확산 둘) DRT 극대 15**(계면 둘 + τ 0.15 s–9.4×10³ s 열셋 · 표 III 격자면 τ_max ≈1.6×10³ s 밖 둘). 어휘(본문 · NFKC — 합자 256 개라 NFKC 전 `identifiab*` 0): `identifiab*` **19** · `uniqu*` 4 · `sensitiv*` 15 · `confiden*` 3(전부 수사) · `Fisher` · `covarian*` · `Hessian` · `Jacobian` · "condition number" · `bootstrap` · `posterior` · `Bayes*` · `uncertain*` **0** ⇒ **ASSB 0/96 — 도구 칸 · 여든여덟 번째 성질**(§(b) 6).
3. ★★★★ **(c) 검증 — 독립 측정 대조 0 · 실셀 하나 · 25 °C 하나 · 임피던스 맞춤뿐이고, 실셀 최종값(표 VI)은 같은 편 부록이 인쇄한 경계 · 물리 범위 밖에 놓인다.** 셀 = 상용 **Panasonic 25 Ah 각형 흑연//NMC**(Ford C-MAX Energi PHEV 팩 · 연재 [3–6] 과 같은 셀 · 이력 · SOH 미인쇄) · **19 SOC** · C/50(≈0.5 A `[재현]`) 정전류 EIS(SOC <10 % 는 혼성 모드) · K–K 검증(Gamry Echem Analyst — 잔차 값 0) · SOC 당 "about a day". 해체 · GITT · 3전극 · 시간 영역 검증 0(`[인쇄]` "A more comprehensive comparison … (such as parameter estimates implemented in time-domain simulations) is **planned for future publications**"). Strategy 1(모든 SOC 한 모형) 맞춤은 저주파 · 저 SOC 에서 어긋나고(저자 가설: SOC 표류 · 창 끝점 오차) Strategy 2(SOC 별)가 더 맞다. ★ `[재현]` **표 VI 이 부록 경계 · 물리 범위와 폐합하지 않는다**: n̄e^n **1.0166 mol > 3Q/14 = 0.200 mol**(×5.1 — Q 0.9328 mol 보다도 크다) · n̄e^s/n̄e^n = **2.000**(K_n̄e 상한) · n̄e^s/n̄e^p 13.7(> 2) · **κ̄D −1.46×10⁻⁸ V K⁻¹**(인쇄 범위 −1.55×10⁻³ … −8.62×10⁻⁵ — 크기 ×1/5,900) · κ̄^p/κ̄^s 0.072 < 2⁻³·⁵ = 0.088 · **R̄dl^n 1.00×10⁻¹⁰ Ω < 하한 1×10⁻⁶** · n_dl^p 0.90 = 하한 · 그리고 **어떤 ψ̄ 도 n̄e^n 과 κ̄D 를 함께 범위에 넣지 못한다**(n̄e^n 은 ψ̄ ≤7.2×10⁻⁸ · κ̄D 는 ψ̄ ≥2.2×10⁻³ 을 요구 — ×3×10⁴). κ̄D/ψ̄ 는 Strategy 1 −0.040 ↔ Strategy 2 SOC 별 19 점 −0.031 … −0.36(**×12 산포** · 평균 −0.097 `[도표·화소]`) ↔ 가상 셀 참 −492 ↔ 인쇄 범위로 만든 비 −5.8×10⁴ … −129 C mol⁻¹ K⁻¹. `[인쇄]` 결론 "achieved **consistent** parameter estimates and good matches to the measured impedance data" — "consistent" 의 정의 · 기준 0.
4. ★★★ **(d) EIS = 관측 추가 — 이 편 방식 그대로는 LLI ↔ LAM 을 가르지 않는다(모드 좌표가 EIS 의 입력이다). 다만 전극별 C̄dl · k̄0 를 따로 내는 구성은 OCV 창과 다른 채널을 연다 — 조건 다섯이 붙는다.** `[해석]` 이 편에서 Q · θ0 · θ100(= LLI · LAM 이 사는 창)은 OCV · 방전 시험[4 · 5]의 값이고 EIS 는 그 창 위에서 동역학 · 수송 · 이중층을 읽는다 — 28호(Q_th · x⁰ 입력)와 같은 쪽 끝. 그러나 LPM 의 C̄dl^r(= a_s A L C_dl — 활성 표면적 비례) · k̄0,j^r(면적 포함) 은 노화 셀에 되풀이하면 **LAM_PE(입자 소실 → C̄dl^p · k̄0^p · Q^p 같이 ↓) ↔ LLI(창 이동 · C̄dl^p 불변) ↔ 표면 접촉 손실(C̄dl^p · k̄0^p 같이 ↓ · Q^p 불변)** 을 다른 서명으로 낼 자리다 — OCV 창 맞춤의 LLI ↔ LAM_PE 축퇴 방향과 직교할 후보. 조건: ① 전극 배정이 τ 순서 **가정** ② C̄dl 은 CPE 계수(실셀 n_dl 0.90–0.92 — 단위는 F·s^(n−1)인데 표 VI 은 "F") ③ SOC 무관 매개변수의 SOC 별 산포 ×12(실셀 κ̄D/ψ̄) ④ SOC 당 ≈하루(19 SOC ≈19 일 `[재현·가정]`) ⑤ 이 편 노화 · 모드 0. 세미나 3번째(Sun 2025 — 학습형)는 같은 EIS 에서 **적합된 LLI/LAM 라벨과의 상관**을 읽고(라벨 축퇴를 물려받음 — sun2025 digest 전사), 이 편은 **물리 매개변수**를 읽되 모드에 잇지 않는다 — 둘 다 "EIS 가 모드를 가르는가" 를 참값으로 시험하지 않았다. 우리가 공급할 수 있는 시험: 합성 truth 에서 LLI ↔ LAM_PE 축퇴 방향을 따라 C̄dl^p · k̄0^p 가 움직이는지(설계 메모만 — 코드는 RUN_SCOPE 밖 별도 승인 · §(d)).
5. **(e) 후속** — ★★★ 연재 앞 편 셋 [4] Lu 2021 *JES* 168, 070533(OCV · 전극 창 — 우리 α·β 창 맞춤의 액체 판 원전) · [2] Plett & Trimboli 2022 EVS-35(구조적 식별성 주장의 유일한 근거 · 학회 판) · [5] Lu 2022 *JES* 169, 070524(셀 안 양극 OCP 보정) · ★★ [3] · [6] · [7] · [10] Chu 2019 Part I(이 편 TF 의 출처 · 95호 ☆ → 2) · [41] Rabissi 2021(EIS 감도 28 매개변수 중 12 둔감) · [28 · 29] Murbach(비선형 EIS) · [69] Danzer 2019 GDRT(**재지목 · 지목 누락 보충** — 11호 ★★★ · 원장 행 0 → 2) · [68] Ciucci & Chen 2015(베이즈 DRT — 체크리스트 C3) · ★ [62] Rodríguez 2018 · [64] Kong 2020 · [76] Oldenburger 2019 · [14] Meddings 2020 · [1] Oca 2021 · [42] Zhang Q. 2022 · [43] Duan 2022 · [50] Verbrugge & Koch 2003(MSMR). 재지목: [8] Jobman 2015(95 · 96 = 2) · [66] Chu 2020 Part II(95 · 96 = 2) · [74] Wan 2015(11 · 84 · 96 = 3). 재지목 안 함(목록 인용): [87] Schmalstieg 2018(아인슈타인 관계 인용처) · [38] Waag 2013 · [71] Hahn 2019 · 지목 누락(재지목 안 함): [34] Schönleber 2014 Lin-KK(18호 ★★ · 원장 행 0). 흡수된 편(교차): [27] = 51호 Illig 2012.
6. **채움표** — Q1 없다(액체 · `θ(N)` 0/96 · 층 하나 `[해석]`: LPM 의 C̄dl · k̄0 가 둘 다 활성 면적 비례 — 전극별로 따로 나오는 구성 = 곱 축퇴 처방 1단계 입력의 액체 완전지판, 단 배정 가정 · 노화 0) · Q2 없다(EIS 하나 · 2전극 · 배정 = 가정) · Q3 층 하나(적합 + 합성 참값 하나 · 실셀 최종값이 같은 편 경계 밖) · **Q4 ★ 있다 — 단 액체(도구 칸) · ASSB 0/96 · 여든여덟 번째 성질** · Q5 해당 없음 · Q6 없다 · Q7 해당 없음 · Q8 층 하나(MSMR OCP — 흑연은 'teardown-based' [3] · NMC 는 셀 안 재보정 [5]). **누적 ≈20.0 → ≈20.0 (새 칸 0).**

---

# 서지

| 항목 | 값 (`[인쇄]` — p. 2 · p. 21 · p. 28 · XMP) |
|---|---|
| 제목 | **"Nondestructive EIS Testing to Estimate a Subset of Physics-based-model Parameter Values for Lithium-ion Cells"** (지면 · 정보 사전 · XMP 같음 — 원장 · 호출자 서지의 대문자 "Physics-Based-Model … Lithium-Ion" 은 표기 차이) |
| 저자 · 소속 | **Dongliang Lu**¹ · **M. Scott Trimboli**¹ · **Guodong Fan**² · **Yujun Wang**² · **Gregory L. Plett**¹,ᶻ — ¹ Department of Electrical and Computer Engineering, University of Colorado Colorado Springs (Colorado Springs, Colorado 80918) · ² Research and Technology, Cummins Technical Center, Cummins Inc (Columbus, Indiana 47201) · ᶻ 교신 Plett(메일 인쇄 — 옮기지 않음) · ORCID 다섯 인쇄(p. 28) |
| 저널 | *Journal of The Electrochemical Society* **169**(8), **080504** (2022) · doi `10.1149/1945-7111/ac824a` · ISSN 1945-7111 · 꼬리말 "1945-7111/2022/169(8)/080504/28/$40.00"(본문 28 쪽) |
| 일정 | Manuscript submitted **May 31, 2022** · revised manuscript received **July 14, 2022** · Published **August 5, 2022** · `[재현]` 투고 → 수정 44 일 · 수정 → 출판 22 일 · PDF 생성 2022-08-04 18:15:19 +05:30(출판 전날) · XMP crossmark MajorVersionDate 2022-08-05 |
| 저작권 | `[인쇄]` "© 2022 The Electrochemical Society ("ECS"). Published on behalf of ECS by IOP Publishing Limited" + 꼬리말 "**All rights, including for text and data mining, AI training, and similar technologies, are reserved.**" · CC · 오픈 액세스 표기 0 · XMP `prism:copyright` 같은 문장 · `xmpRights:Marked` True · `ali:license_ref` iopscience 저작권 쪽 ⇒ **구독본으로 다룬다** — 이 digest 는 인용 · 요약 · 재현 계산만 담고, 그림 크롭은 위키 관례대로 `raw/figures/` 에(변형 없는 잘라내기 — 95호 · sun2025 선례) |
| 자금 | `[인쇄]` "The authors gratefully acknowledge the financial support of **Cummins Inc.**"(공저자 둘이 Cummins 소속) · CRediT · 이해 상충 진술 0 |
| 코드 · 자료 | **공개 진술 0** — MATLAB `particleswarm.m`(Global Optimization Toolbox, hybrid) + `fmincon.m` · 48 h 제한 · DRT = Wan 등[68, 74] 공개 DRT 도구의 "modified version"(수정 내용 미인쇄 — "Our modification allows automatic processing") · Gamry Reference 3000 · Echem Analyst(K–K) · Sequence Wizard(혼성 모드) |
| 키워드(정보 사전 · XMP) | lumped-parameter model · lithium-ion cell model · EIS test · physics-based model · parameter estimation |
| 분량 | 29 쪽(p. 1 표지 · 본문 p. 2–21 · 부록 p. 22–28 · 참고문헌 p. 28–29) · 그림 **19**(전부 래스터) · 표 **10**(I–X — VII 은 가로 쪽 p. 23) · 번호 식 **[1]–[21]**(본문 1–18 · 부록 TF 19–21 — Strategy 2 식 · 부록 정의식은 무번호) · 각주 a–e · 참고문헌 **[1]–[87]**(번호 빠짐 0 — p. 28–29 목록에서 직접 셈 · [49] = [52] 같은 편이 해만 2015 ↔ 2016 으로 두 번 — D) |
| 절 | (머리 없는 서론 — 연재 일곱 단계 · 기여 여섯) · EIS in the Literature · The DFNe Model and Its LPM Form · Physics-Based Cell-Level Impedance Model(Impedance across the particle/film interface · Overall interfacial impedance model) · Initializing Parameter Estimates(Distribution of relaxation times (DRT) · Decomposing full-cell impedance · Understanding the interface model components · Initializing specific model parameter estimates) · Pre-Processing of Laboratory Data(Approach #1: Discrete model fit · Approach #2: generalized DRT (GDRT)) · Application to A Simulated Cell(sub-set · full-set) · Application to A Physical Cell(Data collection and process · Discussion #1: NMC positive-electrode ocp function · Discussion #2: Different parameter-optimization strategies · Estimating PBM parameter values using laboratory data) · One Last Step, Estimating ψ̄ · Summary · Acknowledgments · Appendix(Physics-based model of cell dynamics · Transfer functions · Initializing model parameter estimates · GDRT algorithm) · ORCID · References |

**PDF 메타데이터 (직접 읽음 · pymupdf)**: 5,151,189 B · sha256 `ffab9252951dc35adbdc5a4f8246b75cad4d6a75388b830e81136fd7cf7815b8`(호출자 명시값 ✅ — 직접 재계산) · `PDF 1.7` · 29 쪽(p. 1 595 × 842 pt · p. 2–22 · 24–29 585.4 × 783.3 pt · **p. 23 783.3 × 585.4 pt 가로**) · 암호 0 · 정보 사전: title **"Nondestructive EIS Testing to Estimate a Subset of Physics-based-model Parameter Values for Lithium-ion Cells"** · author **"Dongliang Lu"** · subject **"Journal of The Electrochemical Society, 169(2022) 080504. doi:10.1149/1945-7111/ac824a"** · keywords "lumped-parameter model; lithium-ion cell model; EIS test; physics-based model; parameter estimation" · creator **"IOPP"** · producer **"iTextSharp™ 5.5.13.4 ©2000-2024 iText Group NV (AGPL-version); modified using iText® 5.5.13.5 ©2000-2026 iText Group NV (IOP Publishing Ltd; licensed version)"**(호출자 메모의 "…©2000-" 는 줄임) · 생성 **D:20220804181519+05'30'** · 수정 **D:20261002134502+01'00'**(호출자 메모와 같음 ✅ — 수정 = 내려받기 시각 · p. 1 표지 "on 02/10/2026 at 13:45" 와 같은 분) · XMP **6,012 B**(`dc:creator` 다섯 · `prism:volume` 169 · `number` 8 · `pageRange` 080504 · `startingPage`/`endingPage` "0" · `jav:journal_article_version` **VoR** · `pdfx:robots` noindex · crossmark DOI · `MajorVersionDate` 2022-08-05 · `xmp:CreateDate` 2022-08-04T18:15:19+05:30 · `ModifyDate` = `MetadataDate` 2026-10-02T13:45:02+01:00 · `xmpRights:Marked` True) · **PageLabels**: 1 부터 십진(PDF 쪽 = 표지 포함 쪽 번호) · 래스터: p. 1 표지 둘(700 × 166 · 1640 × 1061 — 로고 · 광고) + **그림 19 전부 래스터**(쪽마다 1–2 · 1215 × 373 … 1822 × 593 — 그림 1 의 180 × 3 조각 하나 포함) · 벡터 그림 0 · `%%EOF` 1(증분 갱신 흔적 0).

⚠ **텍스트 층**: 합자 **256**(`ﬁ` 등 — `identiﬁable` 꼴) — **NFKC 가 `identifiab*` 0 → 19 를 바꾼다**(어휘 집계는 NFKC 뒤 · 줄 끝 하이픈 복원). 식 · 표의 기호는 수식 글꼴 조각으로 흩어져 텍스트로 못 읽는다 — 식 [1]–[21] · 부록 정의 · 경계 · TF 계수는 **쪽 렌더 조각으로 읽었고**(150–170 dpi · 판독용 · 커밋 안 함), 표 I–X 는 300 dpi 수동 크롭으로 읽었다(커밋 — `tab_*_manual_p*.png`).

---

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **셀 설계 · NMC 조성**(두께 · 면적 · 공극 · 적재 · 전해질) 인쇄 0 — "prismatic 25Ah graphite//NMC cell manufactured by Panasonic"(Ford C-MAX Energi PHEV 팩)뿐 · 저자 `[인쇄]` "To compute the scaling factors, we require knowledge of cell internal dimensions which can be found via teardown if desired" | 집약값(C̄dl · k̄0 · κ̄ · n̄e)을 물리 단위(F m⁻² · mol m⁻² s⁻¹ · S m⁻¹ · mol m⁻³)로 옮길 수 없다 — 문헌 대조 · 물리 범위 검사 불가 |
| **G2** | **실셀 α^r** — 펄스 시험[6] 값이 이 편 표 VI 에 0(가상 셀은 표 IX αj 0.5) | 표 VI 의 k̄0,j 로 R̄ct(θ) 를 다시 풀 수 없다 — `[재현·가정]` α 0.5 로 풀면 양극 0.27–0.61 mΩ(θ 0.4–0.9) · 음극 0.001–0.06 mΩ 로 그림 15(f) DRT 초기 추정(음극 ≈0.105–0.14 · 양극 ≈0.02–0.13 mΩ)과 자릿수가 다르다(같은 코드가 가상 셀 그림 18 '참' 은 ±3 % 로 재현) |
| **G3** | **실셀 최적화의 경계 · 초기값**(Strategy 1 · 2) — 부록 경계는 초기화 절에 인쇄됐으나 실셀에 그대로 썼는지 0 | 표 VI 값 넷이 그 경계 밖 · 둘이 경계 위(§(c) 2) — 경계를 바꿨는지 · 표가 다른 정의인지 지면으로 못 가른다 |
| **G4** | **표 VI 의 층위** — 어느 값이 EIS 적합이고 어느 값이 펄스 시험[6](또는 그림 16 재식별) 값인지 미인쇄(σ̄ · κ̄ · R̄f · R̄dl · k̄0) | 가상 셀 전체 집합에서 이 넷이 19–66 % 움직였다(그림 13) — 실셀 값의 출처가 결과 해석을 바꾼다 |
| **G5** | **GDRT 설정** — λ 값("user-selected") · 이산화 기저 · τ 격자 · DRT 도구 수정 내용 · 봉우리 분리 규칙(어느 τ 구간을 '혹' 으로 잘랐나) | DRT 초기값 · 인덕턴스 보정의 재현 불가 · [[drt-peak-count-nonidentifiability]] 체크리스트 C1 · C4 ❌ |
| **G6** | **가상 셀 참값(표 VIII · IX)의 출처** — 연재 앞 편 Panasonic 값인지 · 손으로 고른 값인지 미인쇄(n_f = n_dl = 1 · R̄dl = R̄f^n = 1×10⁻³ Ω · R̄c 1×10⁻³ Ω 같은 둥근 값 다수) | 참값이 경계 위(n = 1) · 경계 밖(k̄0,6/7)에 놓인 설계가 "정확도" 판정에 들어간다 |
| **G7** | **합성 시험의 반복 · 정지 기준** — 잡음 실현 · 최적화 시작 · 무리 크기 · 반복 수 · 정지 허용 오차 · 최종 비용 · 실행 시간(48 h 제한만) · "sensitivity study" 방법 · 결과(두 번 언급) | 실행 하나의 궤적을 정확도로 읽는다 — 산포 · 신뢰구간 0 |
| **G8** | **실셀 SOC 기준 · 표류** — 19 SOC 의 실제 값(그림 17(f) 6.4 … 100 % — 5 % 격자 밖) · 측정 중 전압 · SOC 표류 크기 · 휴지 길이(≥6 h) · 항온조 기록 · K–K 잔차 값 | Strategy 1 맞춤 어긋남의 원인(저자 가설 SOC 표류)을 지면으로 검사할 수 없다 |
| **G9** | **구조적 식별성 증명(Ref. 2 — EVS-35 학회 판)** · 선형 비식별 도출("some detailed analysis") · R_c ↔ 1/κ̄^s 도출 | 지면은 결론 문장뿐 — `[재현·대수]` 로 비 구조 하나만 확인(§(b) 2) |
| **G10** | **ψ̄ 의 PSS 시험(Ref. 7) 실셀 결과** — C/2 방전 자료 · 적합 · 오차 미인쇄(가상 셀 "relative error … of about 40%" 만) | 표 VI 의 n̄e · κ̄D 는 (EIS 비) × ψ̄ — ψ̄ 하나가 둘을 같이 움직인다(§(c) 2 의 ×3×10⁴ 불일치) |
| G11 | **그림 6 · 9 · 15 의 주파수 격자** | τ_max 판정(창 밖 봉우리)에 필요 — 표 III 격자를 쓴 것으로 읽힘 |
| G12 | **Panasonic 셀의 이력 · 상태** — 팩에서 꺼낸 셀의 사용 이력 · SOH · 용량 측정값(Q 0.9328 mol 은 연재 값) | "신품 매개변수" 인지 노화 셀 매개변수인지 |
| G13 | **EIS 진폭 C/50 의 비선형성 검사** — "minimal overall K–K residuals" 로만 고름 | K–K 는 인과 · 정상성 검사이지 비선형 검사가 아니다(84호 단서와 같은 자리) |

---

# 보충 자료 — 받은 것 · 대조

**SI 없음 (원문에 보충 언급 0) — 부록은 본문 안(p. 22–28).** 호출자 대조와 같은 결과를 직접 다시 셌다 — 본문 · 캡션 · 표 · 참고문헌 전문(NFKC · 줄 끝 하이픈 복원)에서 `supplement*` · "supporting information" · "data availab*" · `github` · `zenodo` · `video` · `movie` **0 회** · `appendix` 11 회 = 전부 본문 부록(TF · LPM 표 VII · 초기화 · GDRT 행렬 — 보충 자료 아님) · "Data Availability" 절 0. 원자료 예치 0 · 코드 공개 0. 그래서 이 digest 의 재현은 **인쇄 수치 · 식 + 쪽 렌더 + 래스터 그림 화소 판독 + 우리 digest 전사(51호)** 네 층뿐이다.

---

# 그림 · 표 — 자동 19 항목 + 수동 10, 실제로 연 것 **29/29**

크로퍼(`wiki/tools/extract_figures.py`)가 그림 1–19 를 `fig_1 … fig_19` 로 잡았다(SI 오판 0 — 파일명 `56._Nondestructive_EIS_testing_…` 의 `SI_TAG` False 를 첫 실행 전에 확인 · 실행 뒤 이름을 눈으로 확인). **표 I–X 는 하나도 자동으로 잡히지 않았다** → 10 개 전부 수동 크롭(`tab_N_manual_pP.png` · 300 dpi — 가로 쪽 표 VII 은 250 dpi). 자동 크롭 점검(`figures.json` `note` 에 적음 — 자동 파일은 지우지 않았다):

- **fig_4 위 끝 과대** — 그림 3 캡션의 마지막 줄 '−Φ̃e(3, s)/Iapp(s).' 이 크롭 위에 들어감(캡션 겹침 · 내용은 온전 — 재크롭 불필요).
- **캡션 필드 오염 · 잘림 열** — fig_5 · 7 · 8 · 11 · 12 · 17 · 19 는 본문이 섞이고 900 자에서 잘림 · fig_14 본문 섞임(671 자) · fig_3(115 자 — '(a–b) …' 에서 끊김 · 꼬리가 fig_4 위로) · fig_16(114 자) · fig_18(48 자 — '…the constant C̄dl' 에서 끊김) 은 캡션이 짧게 잘림. 캡션 원문은 PDF 가 정본.
- 나머지(fig_1 · 2 · 6 · 9 · 10 · 13 · 15) 라벨 · 내용 온전 · 과대 0 · 캡션 필드 깨끗.

**29 장 전부 직접 봤다 — 안 본 그림 · 표 0.** (그림이 아닌 래스터 — p. 1 IOP 로고 · 광고 — 는 열지 않았다.) 판독: 그림 6 · 11 · 12 · 13 · 15(e) · 17(f) 는 **화소 좌표**(표지 중심 · 곡선 극대 · 점선 행 · 격자선)를 축 눈금으로 보정해 읽었다(판독 · 재현 코드 · 확대 조각은 `scratchpad` 에만 · 커밋 안 함).

## Fig. 1 — 고체–전해질 계면 회로 (p. 6 · 봤다) ★★ (a)

왼쪽: Φs 에서 전류 F·ṅf+dl 이 **이중층 가지**(C̄dl 과 R̄dl 직렬 · F·ṅdl)와 **패러데이 가지**(U_ocp(θs,0) 원천 → Φ̃s → Z̄s̃ 고체 확산(CPE) → R̄ct)로 갈라 Φsf 에서 만나고, **막 저항 R̄f** 를 거쳐 Φe 로 간다. 오른쪽: MSMR — R̄ct 를 갤러리별 R̄ct,j 의 병렬로 바꾼 것 · 식 `R̄ct = RT/(F²ṅ̄0) = RT/(F²Σṅ̄0,j) = (Σ1/R̄ct,j)⁻¹`. 캡션 "Circuit on the left is analogous to Fig. 1 from Ref. 66" + 본문 `[인쇄]` "The equations imply the circuit; the circuit does not itself define the model equations … the circuit describes the point-wise impedance at the solid/electrolyte interface at any given spatial location in either electrode." — 이 회로는 **한 점의 계면** 임피던스이고, 셀 임피던스는 TF(전극 두께 방향 분포 — 부록 식 19–21)가 이것을 엮는다.

## Fig. 2 — Nyquist ↔ DRT 예시 (p. 8 · 봤다) ★★★ (b)

R1C1 · R2C2 직렬(τ1 < τ2 · f1 > f2) — **작은 반원 둘이 큰 혹 하나로 합쳐진 Nyquist**(0 → R1 + R2 · 반원 위 f = f1 · f2 표지 · `[도표·화소]` R1/(R1+R2) ≈0.63) ↔ DRT **'Ideal'**(τ1 · τ2 에 높이 R1 · R2 화살) · **'Practical'**(넓은 봉우리 둘 — 면적이 R1 · R2). 축 숫자 0(도식). 캡션 "inspired by the work reported by Illig et al.27"(= **51호**). 본문은 이 그림으로 "a single Nyquist bump can arise from the combination of two (or more) time constants whose impedances overlap in the frequency domain. The DRT procedure can help uncover the individual time constants" 를 말한다 — **두 과정 → 봉우리 둘** 의 이상형 하나만 그린다(역방향 — 한 과정이 봉우리 여럿을 낼 수 있음 — 은 그림 5(b) · 6(a) 에 있다).

## Fig. 3 — 전극 · 전해질 TF 성분의 Bode · Nyquist (p. 10 · 봤다 · 80 % SOC · 해석 TF) ★★ (a)

(a–b) +Φ̃s−e^n(0,s)/Iapp — 성분 I^n_f+dl(0,s)/Iapp ≈0 dB(무차원 ≈1 · 삽입 나선 0.9–1) · Z̄se^n(s) −28 → −57 dB · Nyquist 계면 혹 ≈1.43 → ≈1.78 mΩ(파랑) 뒤 확산 꼬리. (c–d) −Φ̃s−e^p(3,s)/Iapp — 혹 ≈0.75 → ≈3.2 mΩ · 높이 ≈1.1 mΩ. (e–f) −Φ̃e^p(3,s)/Iapp = [Φ̃e]₁(≈0.73–0.75 mΩ 상수 — 옴) + [Φ̃e]₂(반원 0 → ≈1.15 mΩ · 모서리 ≈10⁻² Hz) `[도표·화소]`. ★ `[재현]` 표 VIII · IX(α 0.5) · 80 % SOC(θn 0.720 · θp 0.279)에서 Z̄se 혹 시작 = R̄f + R̄ct∥R̄dl = **1.434 · 0.750 mΩ** · 끝 = R̄f + R̄ct = 1.768 · 2.982 mΩ — 그림과 맞는다 ⇒ **R̄f^n(1 mΩ)은 셀 임피던스에 직렬로 그대로 더해진다**(§(b) 4 의 R_c ↔ R̄f^n 교환의 근거). 본문 `[인쇄]` "both … terms have magnitudes close to one … the electrochemical features we observe from a full-cell Nyquist plot … are primarily projections of the solid-electrolyte interface impedances" · 각주 b "computed from the analytic TFs and cannot be obtained experimentally". 주파수 축 10⁻⁶–10⁶ Hz(측정 창 10⁻⁴–10⁵ Hz 밖까지).

## Fig. 4 — 계면 모형 축약 (p. 10 · 봤다) ★ (a)

Z̄se(원 회로) → Z̄se,A(Z̄s̃ 를 병렬 가지 밖으로) → Z̄se,B(Z̄s̃ 삭제) → Z̄se,C(R̄f 삭제 — R̄ct ∥ (C̄dl + R̄dl)). `[인쇄]` "These transformations are not exact equivalents to the original circuit". ⚠ 자동 크롭 위 끝에 그림 3 캡션 꼬리 한 줄.

## Fig. 5 — 축약 모형 비교 · DRT 로 혹 되살리기 · R̄dl 가정의 영향 (p. 11 · 봤다 · 80 % SOC) ★★★★ (a) · (b)

(a) 3D Nyquist: Z̄se ↔ Z̄se,A ↔ Z̄se,B 를 D̄s 10⁻² … 10⁻⁹ s⁻¹ 에 — D̄s ≲10⁻⁶ s⁻¹ 에서 Z̄se ↔ Z̄se,A 가 갈라짐(`[인쇄]` "start to diverge only when D̄s is small (⩽10⁻⁶ s⁻¹)"). (b) "Retrieve Z̄se,C from its DRT" — 삽입 DRT: **n_DL = 1(이상) 은 봉우리 하나** ↔ ★ **n_DL = 0.9(CPE · 점선)는 국소 극대 셋**(작은 하나 + 붙은 둘 · 이상 봉우리보다 큰 τ 쪽 · 훨씬 낮음 — τ 축 숫자 0) `[도표·화소]` · 범례 **"τ = RC ≠ R̄ct C̄dl"** · 재구성 Z̄se,C,meas(0 → R — 실수축 이동이 사라짐) ↔ Z̄se,C(R̄ctR̄dl/(R̄ct + R̄dl) → R̄ct) · SSE = 20 µΩ². 본문은 CPE 의 다봉을 언급하지 않는다 — **한 요소 → 봉우리 여럿**의 저자 자신 그림이다. (c–d) R̄dl 가정값 10⁻¹⁰ … 10⁻² Ω(참 ≈10⁻³ Ω 점선)에 따른 추정/참 비 `[도표·화소]`: 음극 C̄dl ×5.35(가정 ≲10⁻⁶) · ×6.7(10⁻²) · R̄ct ×2.3 · ×2.6 / 양극 C̄dl ×1.8 · ×4.0 · R̄ct ×1.35 · ×2.0 / n_dl ≈1 — `[인쇄]` "if R̄dl is known only approximately, the results still indicate that the final estimates are always within one order of magnitude" 와 일치. 범례 경계 0.01 ≤ C̄dl ≤ 200 · 0.7 ≤ n_dl ≤ 1 · R ≤ R̄ct ≤ 0.01.

## Fig. 6 — 가상 셀 DRT · 계면 봉우리 분리 (p. 12 · 봤다 · 화소 판독) ★★★★ (b)

(a) "Graphite//NMC cell DRT, 80%% SOC"(제목 오타 '%%') — 셀 임피던스 DRT(검정) + 분리 1 Z̄se^n(파랑) · 분리 2 Z̄se^p(주황) · 회색 'Mid-low frequency regions'. `[도표·화소]`(눈금 10⁰ ↔ 화소 x 620.5 · 96 px/decade): **파랑 τ ≈8.7×10⁻³ s · 주황 ≈3.9×10⁻² s** — `[재현]` 표 VIII · IX 의 (R̄ct + R̄dl)·C̄dl = **8.84 · 39.8 ms**(R̄ct·C̄dl 만이면 3.8 · 29.8 ms — 그림 5(b) 범례 "τ = RC ≠ R̄ct C̄dl" 의 뜻) ✅. ★ **검정 국소 극대 13**: 작은 여섯 τ ≈0.15 · 0.4 · 1.0 · 2.3 · 5.0 · 9.1 s + 큰 일곱 ≈21 s(3.3 mΩ) · 41 s(2.0) · 86 s(4.1) · 2.0×10² s(7.4) · 6.2×10² s(20.8) · **2.6×10³ s(2.3) · 9.4×10³ s(3.7)** — **참 모형(계면 둘 · 전해질 확산 · 고체 확산 둘 = 과정 다섯)에 극대 15**. 본문 `[인쇄]` "(Peaks at lower frequencies arise due to electrolyte and solid-diffusion impedance.)" — 열세 개를 묶음으로만 부른다. 그림의 주파수 격자는 미인쇄(G11) — 표 III 격자(f_min 0.1 mHz)면 τ_max = 1/(2π·10⁻⁴) ≈1.6×10³ s 라 **마지막 둘은 창 밖**. (b) DRT 로 되살린 계면 호: 음극 0 → ≈0.35 · 양극 0 → ≈2.22 mΩ — `[재현]` R̄ct − R̄ctR̄dl/(R̄ct + R̄dl) = **0.334 · 2.232 mΩ** ✅ · 삽입 크기 절대 오차 ≈10 µΩ(음극) · 첨두 ≈26 µΩ @≈2 Hz(양극).

## Fig. 7 — 인덕턴스를 잘라 버리면 (p. 13 · 봤다) ★★ (b)

(a) τ_small = 1 ms(R ≈0.1 mΩ) · τ_large = 100 ms(R ≈1 mΩ) 의 R–C 에 직렬 L — 작은 τ 의 혹이 양의 허수부로 찌그러짐. (b) 양의 허수부 자료를 잘라낸 DRT — 큰 τ 0.1 s 그대로 · **작은 τ 봉우리 1.0 → 3.6 ms**(인쇄 "misidentification of the time constant (by 3.6 times)" ✅). **계측 경로(배선 인덕턴스)가 봉우리 위치를 옮긴다** — [[drt-peak-count-nonidentifiability]] ③ '계측 경로' 의 정량 예.

## Fig. 8 — 배선 인덕턴스 모형 둘 (p. 14 · 봤다) ★ (a)

(a) L∞ = 1 µH + 병렬 R–L(L 0.1 µH · R 1 mΩ) — 곡선 셋(실수부 끝 ≈1 · 2 · 3 mΩ — 셋의 차이 설명 0) · (b) Z = (j2πf)ⁿL · L 0.1 µH · n 0.5–1. 두 패널 표지 **'f → −∞'**(f → 0 이어야 — 그림 표기 오기).

## Fig. 9 — GDRT 적합 예 (p. 15 · 봤다) ★★ (b)

(a) 등가회로 모의 — γRL 둘(τ ≈3×10⁻⁵ · 7×10⁻⁵ s · 점선 참) · γRC 계면 둘(≈2×10⁻² · 6×10⁻² s) + 확산 쪽 봉우리 여럿(≈0.5 s … ≈7×10³ s) · 절대 오차 ≲9 µΩ — 표 II 와 짝. (b) 가상 흑연//NMC + 잡음 — γRL ≈4×10⁻⁶ · 8×10⁻⁶ s · γRC 계면 ≈10⁻² s(1.1 mΩ) · ≈4×10⁻² s(5.7 mΩ) + 0.2 s … 10⁴ s 여러 봉우리 · 절대 오차 ≲40 µΩ `[도표·화소]`. 본문 `[인쇄]` "the remaining peaks at low frequencies correlate to the solid-diffusion impedance. Note that since the DRT provides discrete solutions, the peak locations and heights cannot be exact."

## Fig. 10 — 가상 셀 자료 전처리 (p. 15 · 봤다) ★ (b)

95 · 30 % SOC: Clean ↔ Noisy(인덕턴스 + 잡음 — 허수부 −34 mΩ 까지) ↔ Processed(GDRT). |Clean − Processed| ≈33 µΩ(95 %) · ≈14 µΩ(30 %) 최저 주파수 · 나머지 ≲8 µΩ `[도표·화소]` · 고주파 절편 ≈2.7 mΩ.

## Fig. 11 — 부분 집합 추정 궤적 (p. 16 · 봤다 · 화소 판독) ★★★★ (b)

펄스 매개변수 참값 고정 · 정규화 축(추정/참). 그려진 궤적 **13**(D̄s,ref 2 · n̄e/ψ̄ 3 · C̄dl 2 · n_f · n_dl 4 · κ̄D/ψ̄ 1 · R_c 1) ↔ 캡션 "**14** normalized parameter estimates"(D). `[도표·화소]` 최종값: D̄s,ref^p 1.00(^n 겹쳐 ≈1) · n̄e^n/ψ̄ ≈1.05 · **n̄e^s/ψ̄ 1.48**(3.2 → 0.45 → 1.48 로 떠돎) · n̄e^p/ψ̄ 0.95 · C̄dl ≈1 · n_f^p 0.998 · n_dl^n 0.996 · n_dl^p 1.00 · κ̄D/ψ̄ 1.01 · R_c 1.00 · 반복 ≈245. 초기 X: D̄s,ref^n **0.331** · ^p **0.141**(참 = 초기 ×7.1 — 부록 "D̄s,ref,0/5 < D̄s,ref < 5D̄s,ref,0" 의 밖인데 1.0 으로 수렴 · 부록 "within a factor of two or so from the truth" 와도 다름 — D) · κ̄D/ψ̄ ≈2.12(`[재현]` −4.39×10⁻⁴/4.18×10⁻⁷ ÷ (−1.24×10⁻⁴/2.52×10⁻⁷) = **2.13** ✅). 본문 `[인쇄]` "There is some deviation in n̄e^s/ψ̄ and in n_dl^n. A sensitivity study shows that impedance is extremely insensitive to these parameter values … We consider the quality of the estimates … to be more than adequate for parameterizing a LPM"(감도 결과 그림 0).

## Fig. 12 — 전체 집합 추정 궤적 (p. 17 · 봤다 · 화소 판독) ★★★★ (b)

펄스 매개변수도 자유(시작 = [6] 표 II · k̄0 = 표 X). `[도표·화소]` 최종 추정/참: D̄s,ref^p 1.00 · ^n ≈0.95–1(겹침) · **n̄e^n/ψ̄ 1.20 · n̄e^s/ψ̄ 0.48 · n̄e^p/ψ̄ 1.25** · C̄dl^n 1.03 · C̄dl^p ≈0.97–1.0 · n_f^n 0.991 · n_dl^n 1.00 · n_dl^p 0.994 · **κ̄D/ψ̄ 1.19** · **R_c 1.64**(초기 X 1.0 — 참값에서 출발) · 반복 ≈270. 본문 `[인쇄]` "We see some degradation in the quality of parameter estimates for p_EIS … attribute some of this to … a local minimum … Another factor … not all of the combined set of parameters {p_EIS^lin, p_pulse} are linearly identifiable. In particular, the impact of R_c and 1/κ̄^s on the full-cell impedance are identical … one reason we see a lack of convergence of R_c in Fig. 12f."

## Fig. 13 — 전체 집합의 펄스 매개변수 · k̄0,j (p. 18 · 봤다 · 화소 판독) ★★★★ (b)

`[도표·화소]` 최종 추정/참: (a) σ̄^n ≈1.06 · **σ̄^p ≈1.66** · κ̄^n ≈1.29 · κ̄^s ≈0.88 · **κ̄^p ≈1.44** · (b) R̄dl^p ≈1 · R̄dl^n ≲1 · **R̄f^n ≈0.4**(0.2–0.6 — 축 0–25 라 판독 폭 ±0.3) · R̄f^p 가림 · (c) k̄0,j^n j1 ≈1.1 · j2 1.14 · j3 0.74(크게 요동 · 한때 하한) · j4 1.09 · j5 1.19 · ★ **j6 · j7 은 범례에만 있고 궤적이 축(0–2) 안에 없다** — `[재현]` 초기값 = 표 X 근사(참의 ×12,867 · ×4,107) · 경계 = "one order of magnitude around their initial values" ⇒ **참값이 하한의 1/1,287 · 1/411 — 도달 불가** · (d) k̄0,j^p j1 0.92 · j4 0.97 · j2 · j3 ≈1(겹침) — ⚠ (d) 범례 'k̄^n_0,j=1…4'(양극인데 n — D). 본문 `[인쇄]` "impedance is insensitive to the value of k̄0,j^n for some galleries, which makes finding good estimates of those values challenging. (Conversely, we do not require precise estimates to get good predictions from the LPM.)"

## Fig. 14 — 가상 셀 맞춤 (p. 18 · 봤다) ★★★ (b)

SOC 100–5 % Nyquist 점 ↔ 선 — 눈으로 구별 안 됨 · 절대 오차 실수부 ≲0.04 · 허수부 ≲0.03 mΩ(대부분 <0.02 · 저주파에서 큼) `[도표·화소]`. ⇒ **그림 12 · 13 의 19–66 % 매개변수 어긋남과 같은 적합** — 출력은 맞고 매개변수는 다르다(근최적 집합의 폭이 지면에 있다 · 저자는 폭으로 읽지 않는다).

## Fig. 15 — Panasonic 셀 EIS · GDRT · 초기 추정 (p. 19 · 봤다 · 화소 판독) ★★★★ (b) · (c)

(a) 처리된 Nyquist SOC 6–100 % — 고주파 절편 ≈1.70–1.85 mΩ · 혹 높이 ≲0.05 mΩ · 저주파 꼬리 ≈12 mΩ 까지. (b) SOC 별 GDRT — γRL ≈3×10⁻⁶ s(10.5 mΩ) · 계면 대 10⁻⁴–10⁻¹ s(≤0.3 mΩ) · 10²–10⁴ s 큰 봉우리. (c) Raw(허수부 −28 mΩ 까지) ↔ Processed — `[인쇄]` "removing the inductance recovers the expected Nyquist bump, but truncating the impedance would have deleted the bump entirely". (d) 90 % SOC 견본 — 삽입 **A ≈7×10⁻⁴ s(0.24 mΩ) · B ≈4.5×10⁻³ s(0.09) · C ≈3×10⁻² s(0.03)** · Nyquist 호 A 1.735–1.82 · B 1.82–1.85 · C 1.85–1.865 mΩ · 회색 저주파 봉우리 ≈10¹–10⁴ s(최대 ≈10³ s 6.9 mΩ · 마지막 ≈10⁴ s 2.0 — 이름 0 · τ_max ≈1.6×10³ s 밖) `[도표·화소]` · 본문 `[인쇄]` "**We assume that peak A is associated to the negative-electrode, peak B is associated to the positive-electrode, and peak C is associated to the solid-diffusion impedance**". `[해석]` 가상 셀(그림 6)에서는 τ ≈4×10⁻² s 가 **양극 계면** 봉우리였는데 실셀에서는 τ ≈3×10⁻² s(C)가 **고체 확산** 이름을 받는다 — 같은 τ 대에 다른 이름(셀이 달라 단정 못 함 · 배정 규칙은 τ 순서뿐). (e) C̄dl 초기 추정 vs θs: 음극 ≈3–6 F(평균선 ≈4.0 F) · 양극 보이는 16 점 **36.9–123.4 F**(평균선 **77.7 F** — 보이는 16 점 평균 66.4 · 축 위 밖 점 또는 평균 정의 미상) `[도표·화소]`. (f) R̄ct 초기 추정: 음극 ≈0.105–0.14 mΩ · 양극 ≈0.02–0.13 mΩ(θ ≥0.6 에서 오름) + k̄0,j 모형 맞춤. ★ 표 VI 최종값과 견주면 **C̄dl^p 77.7 → 5.38 F(×0.069) · C̄dl^n ≈4.0 → 10 F(×2.5)** — 전극 사이 크기 순서가 뒤집혔다(§(b) 5).

## Fig. 16 — 보정된 NMC OCP 로 펄스 저항 재식별 (p. 20 · 봤다) ★ (c)

SOC 19 · 39 · 59 · 80 % · 펄스 −4 … +4 C · 펄스 저항 ≈1.06–1.14 mΩ(0 C 근처 오차 막대 큼) · MSMR 모형 선 · 3D 예측 면. 본문 `[인쇄]` "This figure is comparable to Fig. 17 in Ref. 6 but now gives a better fit among all SOC setpoints, which gives us more confidence regarding the accuracy for the electrode OCP functions" — 펄스 시험의 재적합이지 EIS 추정의 검증이 아니다. ⚠ 고주파 EIS 절편(≈1.70–1.85 mΩ — 그림 15(a))이 펄스 저항(≈1.1 mΩ)보다 크다 — 표 VI R_c 0.744 mΩ 를 빼면 ≈0.96–1.1 mΩ 로 같은 자릿수(`[해석]` EIS 모형에만 R_c 를 더한 것 — 각주 d "we also need to consider the resistance from elements such as particle binders, current collectors, and cable clamps" — 과 정합 · 펄스 시험 쪽 처리 · '순간 저항' 정의는 [6] 에 있고 이 지면엔 0).

## Fig. 17 — 실셀 맞춤 Strategy 1 · 2 · SOC 별 추정 (p. 21 · 봤다 · 화소 판독) ★★★★ (c)

(a–b) Strategy 1 — 저 SOC(분홍) 저주파 꼬리 · 혹에서 점 ↔ 선 어긋남 · (c–d) Strategy 2 더 가까움 · (e) D̄s^r SOC 별 추정: 음극 ≈4.8×10⁻⁴ … 3.6×10⁻² s⁻¹ · 양극 ≈8.8×10⁻⁴ … 2.1×10⁻² + Darken 모형 맞춤 곡선(점이 곡선에서 ×3–10 벗어나는 곳 있음) · (f) **κ̄D/ψ̄ SOC 별 추정**(로그 축 −10⁻² … −10⁰): `[도표·화소]` **19 점 −0.0305 … −0.362(×11.9)** · 산술 평균 **−0.0965** = 점선 'Average'(≈−0.097) · SOC ≈6.4 · 12.6 · 17.7 · 20.6 · 25.9 · 30.2 · 35.8 · 42.2 · 47.5 · 52.5 · 57.9 · 63.0 · 67.8 · 73.9 · 79.2 · 84.3 · 89.4 · 94.6 · 100 %(5 % 격자 아님 — 표 IV "identical to Table III" 와 어긋남 · 19 ↔ 표 III 20). κ̄D/ψ̄ 는 SOC 와 무관한 전해질 상수(`[인쇄]` 부록 "κ is treated as a constant that is evaluated at the equilibrium concentration θe,0 = 1")인데 SOC 별 추정이 ×12 퍼진다 — **실셀에서 이 매개변수의 실제적 식별 폭의 하한 표본**. 표 VI(Strategy 1) **−0.0399** 와 평균 ×2.4 · 가상 셀 참 −492 와 4 자릿수.

## Fig. 18 — 가상 셀 초기화: DRT 로 C̄dl · R̄ct 근사 (p. 25 · 봤다) ★★★ (a)

(a) C̄dl^n 4.88–5.42 F(평균 ≈5.08) ↔ 참 5 · ⚠ x 축 이름 'θs^p'(음극인데 p — 점 위치는 (c) 의 θs^n 과 같음 — D) · (b) C̄dl^p 9.1–10.6 F(평균 ≈10.05) ↔ 참 10 · (c) R̄ct^n 참 ↔ 추정 0.65–1.55 mΩ · (d) R̄ct^p 1.78–3.0 mΩ + k̄0,j 모형 맞춤 `[도표·화소]`. ★ `[재현]` 표 IX MSMR + k̄0 + α 0.5 로 '참' R̄ct(θ) 를 다시 풀면 음극 θ 0.12 → 1.013 · 0.2 → 0.799 · 0.3–0.5 → 0.68–0.69 · 0.9 → 0.802 mΩ · 양극 θ 0.14 → 2.42 · 0.28 → 2.98 · 0.42 → 1.79 · 0.82 → 2.60 mΩ — 그림 점과 ±3 %(음극 θ ≈0.07 첫 점만 1.80 ↔ ≈1.55 — 가파른 끝). 가상 셀에서는 DRT 초기값이 참에 가깝다(그 위의 전체 집합 최종값은 그림 12 · 13).

## Fig. 19 — 갤러리별 교환 전류율 ṅ0,j(θs) (p. 27 · 봤다) ★★ (a)

k̄0,j = 1 mol s⁻¹ · αj = 0.5 에서: (a) 흑연 **j = 1–6**(범례) — j4 · j6 ≈0(전 구간) · j5 θ ≈0.10–0.42(0.42 에서 수직으로 끊김 — 그림 인공물로 읽힘) · j3 작음 · θ0^n ≈0.00 · θ100^n ≈0.83 점선 · (b) NMC **j = 1–4** — j3 · j4 ≈0 · θ100^p ≈0.18 · θ0^p ≈0.91 점선. ⚠ 본문은 이 그림의 매개변수를 "for the Panasonic cell … listed in Table V" 라 쓰나 표 V 는 NMC **5** 갤러리 · θ100^p 0.2263(그림 점선 ≈0.18) · 가상 셀 표 IX 는 흑연 **7** · NMC 4 · 본문 "six galleries in the (graphite) anode and four in the (NMC) cathode … ten different k̄0,j" — **갤러리 수가 세 가지로 인쇄된다**(D). 본문 `[인쇄]` "The results indicate that k̄0,j in both electrodes should be **observable** because each ṅ0,j is a unique function of θs" ↔ 같은 쪽 "galleries 4 and 6 … orders-of-magnitude [smaller]" · p. 27 "R̄ct^r is extremely insensitive to k̄0,6^n and k̄0,7^n" — `[재현]` 표 IX 참값으로 갤러리 6 · 7 의 ṅ0 몫은 θ 0.03–0.89 에서 **≤1.5×10⁻⁵ · ≈0**(구조적으로 안 보임) · 표 X 근사값(×12,867)이면 갤러리 6 몫이 한 θ 에서 **16 %**.

## Table I — 시험 여섯의 분담 (p. 3 · 봤다 · 수동) ★★★★ (a)

| 시험 | 최종 추정 | 참고 추정 |
|---|---|---|
| OCP[3] | U_ocp^n(θs^n) · {U0j, Xj, ωj}^n | Û_ocp^p(θ̂s^p) |
| OCV[4] | **Q · U_ocv(z) · θ0^n · θ100^n** | **θ̂0^p · θ̂100^p** |
| Discharge[5] | U_ocp^p(θs^p) · {U0j, Xj, ωj}^p · **θ0^p · θ100^p** | D̄̂s,ref^r |
| Pulse[6] | α^r · κ̄^r · σ̄^r · R̄f^r · R̄dl^r | k̄̂0^r |
| **EIS (this paper)** | **D̄s,ref^r · n_f^r · C̄dl^r · n_dl^r · k̄0^r** | **n̄e^r/ψ̄ · κ̄D/ψ̄** |
| Discharge[7] | ψ̄ · n̄e^r · κ̄D | — |

⇒ 모드 좌표(Q · 창)와 OCP 는 EIS 앞에서 끝난다. EIS 행에 R_c 는 없다(표 밖 · p. 14 에서 추가 매개변수로).

## Table II — GDRT 시간 상수 (p. 15 · 봤다 · 수동) ★ (b)

참 ↔ 추정: R∞ 2 ↔ 1.98 mΩ · L∞ 1 ↔ 1 µH · C0 400 ↔ 400 F · τRL1 25 ↔ 26.26 µs · τRL2 75 ↔ 78.80 µs · τRC1 15 ↔ 15.30 ms · τRC2 52 ↔ 52.85 ms — `[재현]` −1.0 · 0 · 0 · +5.0 · +5.1 · +2.0 · +1.6 %.

## Table III — 가상 셀 EIS 설정 (p. 15 · 봤다 · 수동) ★★ (b)

SOC 100 %: −5 %: 5 %(`[재현]` 20 점) · 100 kHz–0.1 Hz 20 ppd · 0.1 Hz–1 mHz 10 ppd · 0.1 mHz(`[재현]` 142 주파수) · 25 °C · 잡음 모형 L0 52 nH · R1 1.2 mΩ τ1 7.1 µs · R2 1.5 mΩ τ2 2.7 µs · **ε = 0.5 % · η′ = η″ = N(0, 0.2) Ω** — 본문 식 [17] Z_meas = (Z_cell + Z_L) + ε\|Z_cell + Z_L\|(η′ + jη″) 와 "η′ and η″ are two independently distributed random variables with **standard normal** distribution and we let both of them equal to N(0, 0.2) Ω" — '표준 정규' ↔ N(0, 0.2) · 곱셈 인자에 Ω 단위(D).

## Table IV — 실셀 EIS 절차 (p. 19 · 봤다 · 수동) ★★ (c)

순서 1(25 °C): 천천히 v_max(100 % SOC)까지 충전 · 휴지 ≥2 h / 순서 2(반복 · T): 0. 항온조 T · 1. **휴지 ≥6 h** · 2. 정전류 EIS 100 kHz–0.1 Hz 20 ppd · 3. 0.1 Hz–1 mHz 10 ppd · 4. 0.1 mHz · 5. 원하는 SOC 까지 천천히 방전 · 6. 반복 · "SOC setpoints, input frequencies are identical to Table III"(↔ 본문 "In total, **nineteen** distinct SOC setpoints" · 그림 17(f) 19 점 5 % 격자 밖 — D). `[재현·가정]` 주파수마다 한 주기씩만 재도 ≈14,905 s = 4.1 h(0.1 mHz 한 주기 10⁴ s 포함 · Gamry 가 주기 수를 자동으로 늘림 — 인쇄 "we are unable to adjust the number of input cycles") + 휴지 ≥6 h → 인쇄 "about a day" 와 정합 · 19 SOC ≈19 일(온도 하나).

## Table V — 실셀 MSMR OCP (p. 20 · 봤다 · 수동) ★★★ (a) · Q8

흑연 **6** 갤러리(U0 0.09024–0.39732 V · X 합 1.00001 `[재현]` · ω 0.091–7.41) · θ0^n 0.0007 · θ100^n 0.8279 / NMC **5** 갤러리(U0 3.654–4.994 V · X 합 0.99999 · ω 1.03–10.77) · θ0^p 0.9144 · θ100^p 0.2263(창 폭 0.688 — 부록 n̄e 경계 유도의 가정 "0.7 to 1" 밖) · **Q 0.9328 mol(`[재현]` ×F/3600 = 25.00 Ah ✅)**. 흑연 값은 연재 [3 · 4] 그대로(`[인쇄]` "the graphite-electrode values are unchanged from Refs. 3, 4") · NMC 는 [5] 의 보정판(`[인쇄]` "did not use the positive-electrode OCP function from that paper since we later discovered that it was not well calibrated").

## Table VI — 실셀 최종 매개변수 (Strategy 1 · 25 °C) (p. 22 · 봤다 · 수동) ★★★★ (c)

| | 단위 | 음극 | 분리막 | 양극 |
|---|---|---|---|---|
| σ̄ | S | 857661 | — | 146685 |
| κ̄ | S | 5831 | 7176 | 515 |
| R̄f | Ω | 1.03×10⁻³ | — | 6.62×10⁻⁹ |
| R̄dl | Ω | **1.00×10⁻¹⁰** | — | 3.98×10⁻⁴ |
| D̄s,ref | s⁻¹ | 2.75×10⁻³ | — | 1.17×10⁻⁴ |
| n̄e | mol | **1.0166** | **2.0332** | 0.1487 |
| C̄dl | F | **10** | — | **5.38** |
| n_f · n_dl | u/l | 0.96 · 0.92 | — | 0.92 · **0.90** |
| k̄0,1 … k̄0,6 | mol s⁻¹ | 1.73×10⁻¹⁰ · 1.01×10⁻² · 2.44×10⁻⁹ · 7.34×10⁻⁶ · 4.57×10⁻¹ · 4.91×10² | — | 6.50×10⁻³ · 3.10×10⁻³ · 6.13 · 1.21×10² · 6.24×10⁴ |
| κ̄D | V K⁻¹ | **−1.46×10⁻⁸** (spans all regions) | | |
| ψ̄ | mol S⁻¹ s⁻¹ | 3.66×10⁻⁷ (spans all regions) | | |
| R_c | Ω | 7.44×10⁻⁴ (spans all regions) | | |

`[재현]` 부록 경계 · 물리 범위와의 폐합 — §(c) 2. 그 밖: α 행 0(G2) · C̄dl 단위 "F" 인데 n_dl < 1(CPE 계수 — F·s^(n−1)) · k̄0 이 갤러리마다 12(음극) · 7(양극) 자릿수에 걸쳐 3 유효숫자로 인쇄(ω 가 큰 갤러리는 그림 19 에서 몫 ≈0 — 그 값의 근거가 지면에 없다) · R_c 0.744 mΩ = 고주파 절편(≈1.70–1.85 mΩ)의 ≈40–44 %. ⚠ k̄0,1^n 1.73×10⁻¹⁰ 은 표 X 의 가상 셀 근사 k̄0,3^n(1.73×10⁻¹⁰)과 같은 숫자다(우연 일치인지 미상 — 표시만).

## Table VII — LPM 식 요약 (p. 23 가로 쪽 · 봤다 · 수동 250 dpi) ★★★ (a)

고체 전하 보존 σ̄ ∂²φs/∂x̃² = Fṅf+dl · 고체 질량 보존 + **D̄s(θs) = D̄s,ref (F/RT) θs(θs − 1) ∂U_ocp/∂θs**(Darken) · 경계 D̄s ∂θs/∂r̃\|₁ = −(\|θ100 − θ0\|/(3Q)) ṅf · 전해질 전하 보존 ∂/∂x̃(κ̄(∂φe/∂x̃ + κ̄D T ∂lnθe/∂x̃)) + Fṅf+dl = 0 · 전해질 질량 보존 **n̄e ∂θe/∂t = ψ̄ ∂/∂x̃(κ̄ ∂θe/∂x̃) + ṅf+dl** · 동역학(단일 BV 꼴 · ṅ0 = k̄0 θe^(1−α)(1 − θss)^(1−α) θss^α — 본문 식 7 이 MSMR 판으로 바꾼다) · 이중층 R̄dl C̄dl F ∂ṅdl/∂t + Fṅdl = C̄dl ∂(φs − φe − FR̄f ṅf+dl)/∂t · θs = cs/cs,max · θe = ce/ce,0 · ṅ = a_s A L j. `[재현·대수]` 전해질 식에 n̄e · ψ̄ 가 나오고(n̄e/ψ̄ 비는 시간 상수), 전하 식에 κ̄D 가 κ̄ 와 곱으로 — 소신호에서 비만 남는 구조의 출발.

## Table VIII — 가상 셀 참값 (p. 24 · 봤다 · 수동) ★★★★ (b)

θ0 0.0299 · 0.8510 · θ100 0.8928 · 0.1360 · Q 0.81639 mol(`[재현]` 21.88 Ah) · σ̄ 612311 · 28957 S · κ̄ 1350 · 5758 · 2438 S · R̄dl 1×10⁻³ · 1×10⁻³ Ω · R̄f 1×10⁻³ · 1×10⁻⁶ Ω · D̄s,ref 3×10⁻⁵ · 7×10⁻⁶ s⁻¹ · n̄e 2.12 · 1.37 · 1.76 ×10⁻² mol · C̄dl 5 · 10 F · **n_f = n_dl = 1**(부록 경계 0.9–1 의 **상한 위**) · κ̄D −1.24×10⁻⁴ V K⁻¹ · ψ̄ 2.52×10⁻⁷ · R̄c 1×10⁻³ Ω — `[재현]` κ̄D/ψ̄ = **−492** · n̄e/ψ̄ 8.41 · 5.44 · 6.98 ×10⁴ S s · n̄e^n/Q 0.026(실셀 1.09 의 1/42) · 모든 값이 부록 경계 안(n 은 경계 위).

## Table IX — 가상 셀 MSMR (p. 25 · 봤다 · 수동) ★★★ (a)

흑연 **7** 갤러리(U0 0.08842–1.19292 V · X 합 1.0000 · ω 0.080–19.92) · k̄0,j 1.74×10⁻⁴ · 1.42×10⁻⁴ · 5.04×10⁻¹⁰ · 2.88 · 8.02×10⁻¹¹ · 2.08×10⁻² · 1.67×10⁻² mol s⁻¹ · NMC 4 갤러리 · k̄0,j 6.82×10⁻⁴ · 1.11×10⁻³ · 0.36 · 2.51 · αj 0.5 — `[재현]` 이 표로 그림 18 '참' R̄ct 를 ±3 % 재현 · 그림 6 봉우리 τ · 호 폭 재현(위).

## Table X — DRT R̄ct 로 근사한 k̄0,j (p. 28 · 봤다 · 수동) ★★★★ (b)

참 ↔ 근사: 흑연 j1–7 1.74×10⁻⁴ ↔ 1.61×10⁻⁴ · 1.42×10⁻⁴ ↔ 1.29×10⁻⁴ · 5.04×10⁻¹⁰ ↔ 1.73×10⁻¹⁰ · 2.88 ↔ 3.13 · 8.02×10⁻¹¹ ↔ 8.63×10⁻¹¹ · **2.08×10⁻² ↔ 267.63 · 1.67×10⁻² ↔ 68.58** / NMC 6.82×10⁻⁴ ↔ 5.08×10⁻⁴ · 1.11×10⁻³ ↔ 1.14×10⁻³ · 0.36 ↔ 0.36 · 2.51 ↔ 2.47 — `[재현]` 비 0.925 · 0.908 · 0.343 · 1.087 · 1.076 · **12,867 · 4,107** · 0.745 · 1.027 · 1.000 · 0.984 · 단위 "mol **S**⁻¹"(표 IX 는 mol s⁻¹ — D). `[인쇄]` "we cannot find satisfying k̄0,j estimates for all galleries, especially k̄0,6^n and k̄0,7^n. This is because R̄ct^r is extremely insensitive to k̄0,6^n and k̄0,7^n. As a result, the boundaries for k̄0,j are set to be one order of magnitude around their initial values".

## 본문 서술과 어긋난 그림 (요약)

| 그림 · 표 | 본문 | 그림 · 표가 보이는 것 |
|---|---|---|
| 초록 · 결론 ↔ 그림 12 · 13 | "highly accurate" · "very good accuracies" | 전체 집합 다섯이 19–64 % · 펄스 매개변수 셋이 29–66 % 어긋남 · k̄0,6/7 은 경계 밖 참값 `[도표·화소]` |
| 그림 11 캡션 ↔ 그림 · 초록 | "14 normalized parameter estimates" | 궤적 13 · 초록 "thirteen" |
| 부록 D̄s,ref 경계 ↔ 그림 11–12(a) | "within a factor of two" · 경계 ×1/5–×5 | 양극 초기값 = 참 ×0.141(경계 밖)인데 1.0 으로 수렴 |
| 표 IV ↔ 본문 · 그림 17(f) | "identical to Table III"(20 SOC · 5 % 격자) | 19 SOC · 6.4 … 100 % |
| 그림 19 ↔ 표 V · IX · 본문 | Panasonic MSMR(표 V) · "six … four" | 흑연 6 · NMC 4 (표 V NMC 5 · 표 IX 흑연 7) · θ100^p 점선 ≈0.18 ↔ 0.2263 |
| 그림 18(a) | 음극 C̄dl | x 축 'θs^p' |
| 그림 13(d) | 양극 k̄0,j | 범례 'k̄^n' |
| 그림 6(a) 제목 | 80 % SOC | '80%% SOC' |
| 그림 8 | f → 0 끝 | 'f → −∞' |
| p. 9 "as previously discussed in Fig. 5" | 앞 그림 | 그림 5 는 p. 11(뒤) — 앞에서 다룬 것은 그림 2 |

---

# 절별 해체 (본문)

## 초록 (p. 2)

`[인쇄]` 연재의 마지막 편 · "we leverage electrochemical impedance spectroscopy (EIS) to find estimates of **all as-yet-unresolved parameter values**" · "regresses the measured cell impedance spectrum to **exact analytic closed-form expressions** of the frequency response of an extended Doyle–Fuller–Newman model to identify **thirteen lumped parameters plus multiple reaction-rate constants**" · "A nonlinear optimization algorithm performs the regression, and so it is important to provide reasonable initial parameter estimates and constraints" · "the **generalized distribution of realization times** technique is used to isolate time constants from the two electrodes as well as to calibrate the laboratory EIS-test data"(⚠ 'realization' — 본문은 내내 'relaxation' — 초록 오기) · "studied on a virtual cell and on a laboratory cell (both having graphite//NMC chemistries). Parameter estimates found in the simulation study are **highly accurate, leading us to have confidence in the values estimated for the physical cell as well**." — `[해석]` 가상 셀 정확도 → 실셀 값의 신뢰로 넘어가는 추론은 같은 모형 · 잡음 하나 위의 시험이 실셀 모형 오차를 말해 주지 않는다는 점에서 이어지지 않는다(95호 H4 — 1.2 mV 모형 오차가 추정을 무작위 수준으로 보냄 — 와 같은 자리).

## 서론 (p. 2–3 · 머리 없음) — 연재 일곱 단계 · 여섯 기여

동기: `[인쇄]` 해체 방식은 "specialized equipment that is out of reach of many battery-management design teams" — 대신 입출력(전류/전압) 자료를 PBM 에 회귀 · "But, is it even possible to estimate all of a PBM's parameter values this way?" · 연재[2–7] 목표 = "estimate the values of **all** parameters needed to evaluate a physics-based lithium-ion cell model tailored to match the dynamics of a specific physical cell". **DFNe** = DFN + (i) 이중층 (ii) MSMR(OCP · 반응 동역학) (iii) SOC 의존 고체 확산 (iv) CPE(이중층 · 고체 확산 — 전극 불균질). **일곱 단계**(논리 순서 · 연대 순서 아님):

| 단계 | 내용 (`[인쇄]` 요약) | 문헌 |
|---|---|---|
| (i) | 식별 가능한 모형 만들기 — "A model is said to be **nonidentifiable if two distinct sets of parameter values produce identical input/output relationships**. The DFNe model is nonidentifiable in this sense" → 식 재정식 + 매개변수 집약 = **LPM** · "The most comprehensive description … is found in Ref. 2" · 앞선 판 [8–10] | [2] Plett & Trimboli EVS-35 2022 · [8] Jobman 2015 · [9] Jobman 학위논문 2016 · [10] Chu 2019 |
| (ii) | 전극 OCP — "**Five teardown-based approaches** to estimating OCP in a … MSMR model format are presented in Ref. 3" · 흑연은 충분히 정확 · 많은 양극은 추가 보정 필요 | [3] Lu 2021 *JES* 168, 070532 |
| (iii) | 셀 OCV · 총 용량 · **전극 화학량론 창** — "five methods to estimate the OCV function and showed how to correlate electrode OCP functions with the OCV estimate to find estimates of the electrode operating boundaries" · 흑연 창은 충분 · 양극 창은 보정 필요 · "also proposed an approach to estimate electrode OCP functions **without requiring cell teardown**" | [4] Lu 2021 *JES* 168, 070533 |
| (iv) | 정전류 방전 시험으로 양극 OCP · 창 보정 — "By the end of this step, the thermodynamics of the cell are completely characterized, and initial estimates of the reference solid diffusivities have been made" | [5] Lu 2022 *JES* 169, 070524 |
| (v) | 초단 전류 펄스 → SOC · 율 의존 순간 저항 함수 → 전도도 매개변수 아홉 + 계면 동역학 매개변수 — "intentionally activates nonlinear dynamics" | [6] Lu 2021 *JES* 168, 080533 |
| **(vi)** | **이 편** — EIS 소신호 응답을 DFNe 의 닫힌 꼴 TF 에 회귀 · "we rely on measuring the cell's impedance at many SOC and frequency setpoints to be able to distinguish between the impacts of many parameter values. This test is able to estimate **all but one** of the remaining LPM parameter values" | — |
| (vii) | 방전 자료를 PSS 모형[7]에 회귀해 ψ̄ → n̄e · κ̄D 의 중간값을 최종값으로 | [7] Guest 2020 *JES* 167, 160546 |

**여섯 기여**(`[인쇄]`): ① 연재의 마무리 — 해체 없이 LPM 의 나머지 값 전부 ② LPM = 이중층 · MSMR · SOC 의존 확산 · CPE 를 가진 완전 P2D DFNe ③ 정확한 해석적 닫힌 꼴 주파수 응답으로 최적화 — "as fast as possible without sacrificing accuracy" ④ 셀 부분들이 전체 임피던스에 기여하는 방식 시각화 ⑤ 초기값 · 경계 계산 제안 — "to improve the likelihood that the optimization will find good solutions" ⑥ 배선 상호 인덕턴스 편향 제거로 실험 자료 보정 — "validated both in simulation (where the true parameters are known, enabling direct evaluation of the quality of the estimates), and applied to a physical graphite//NMC commercial cell". `[해석]` 기여 여섯 중 **식별성 진단(유일성 · 불확실성)을 내세운 것은 0** — ①의 "all … without teardown" 은 (i) 단계의 구조적 식별성(Ref. 2)에 기대고, 이 편의 시험은 정확도(가상 셀) · 맞춤(실셀)이다.

## EIS in the Literature (p. 3–4)

ECM ↔ PBM · Newman 다공 전극[15] → TLM[16–20] · Bisquert[21–24] · de Levie[17, 18, 25] · Randles + Warburg[26, 27]. 비선형 확장(Murbach[28, 29] — 고조파 분산 함수): `[인쇄]` "We believe that this extension holds promise to enable high-magnitude inputs which may help estimate more PBM parameter values; however, that investigation is beyond the scope of this work". 자료 품질 — 인과성 · 선형성 · 안정성 · 유한성[30, 31] · K–K[32–34] · 정전류 ↔ 정전위 · 혼성 EIS[37–40] · `[인쇄]` "the quality of all laboratory cell data used in this work is validated by the Kramers–Kronig test using the Gamry Echem Analyst software"(잔차 값 0). **매개변수 추정 문헌 셋** — ★ `[인쇄]` "Rabissi et al.41 performed a comprehensive sensitivity analysis on 28 physical parameters that characterize cell impedance and found that **40% of the parameters (12 out of 28) have either low sensitivity or are insensitive**. This can be explained by recognizing that physics-based cell impedance models are linearized versions of nonlinear behaviors and consequently **not all parameters are identifiable from the EIS test**"(`[재현]` 12/28 = 42.9 % — 인쇄 '40%' 는 내림) · Zhang[42](SOC 감도 낮은 매개변수 고정 — Strategy 2 의 출처) · Duan[43](Li 금속 반쪽전지 아홉 매개변수 — "consistent parameter estimates") · 결론 "the large number of model parameter values (some of which are nonidentifiable) is the primary limitation for utilizing EIS test results alone in a parameter-estimation strategy". `[해석]` 문헌 쪽 근거로 "EIS 만으로는 다 못 정한다" 를 인정하고, 이 편의 처방은 **다른 시험(OCP · OCV · 방전 · 펄스 · PSS)으로 나머지를 정해 두고 EIS 는 남은 것만** 이다 — 식별성을 시험 분담으로 산다.

## The DFNe Model and Its LPM Form (p. 4–5)

이중층 식 [1](Meyers[47] 단순판 일반화 + R̄dl — "its presence in Eq. 1 was justified in Ref. 6") · `[인쇄]` "**The DFN model is nonidentifiable** in the sense that we can use more than one distinct set of parameter values in the equations and produce identical input/output (current/voltage) simulations. Any parameterization of the DFN model using only input/output data (i.e., without teardown …) will give non-unique solutions. Any of these solutions can describe the input/output relationship well, but **none are guaranteed to have physical meaning**. Physical meaning is a requirement if we wish to use the identified model to predict cell internal electrochemical variables (e.g., to detect the precursors to premature aging and failure), so we must rewrite the DFN model to make it identifiable" → Ref. 2 절차: x → x̃(영역마다 길이 1 — 음극 [0,1] · 분리막 (1,2) · 양극 [2,3]) · r → r̃ · 농도 → 화학량론 θ · 플럭스 j → 몰률 ṅ(LPM 식 = 부록 표 VII). SOC 의존 확산 = Baker 등[48, 49] 식 [2] D̄s(θs) = D̄s,ref (F/RT) θs(θs − 1) ∂U_ocp/∂θs — `[인쇄]` "using this physics-based model of SOC-dependent solid diffusivity **does not add any parameters**". MSMR[48, 50–57]: 갤러리 j 마다 최대 점유 X_j · 현재 x_j · 식 [3] x_j = X_j/(1 + exp(f(U_ocp − U_j⁰)/ω_j)) · 갤러리별 BV — ṅ0,j = k̄0,j x_j^(ω_jα_j)(X_j − x_j)^(ω_j(1−α_j)) θe^(1−α_j) · `[인쇄]` "X_j, U_j⁰, and ω_j are identified by the OCP and OCV tests … the pulse test … can in principle find the k̄0,j and α_j values; however, in that paper we did not collect data at sufficient SOC setpoints to do so reliably. Therefore, in this paper, we will refine these values using data collected via EIS." CPE[58]: Z_c̃(s) = 1/(s^n_dl C) · 0 < n_dl ≤ 1(이중층 · 고체 확산 둘에).

## Physics-Based Cell-Level Impedance Model (p. 5–7)

라플라스 TF: Smith[59](근사 DFN) → Lee[60, 61] → Rodríguez[62, 63](선형화 DFN 과 정확히 일치) → Kong[64](EIS 조건 시간 영역 검증) → **Chu[10](집약 매개변수판) — 이 편이 MSMR 계면으로 고쳐 쓴다**. 필요한 TF 둘 = Φ̃s−e(x̃, s)/Iapp · Φ̃e(x̃, s)/Iapp(경계에서 — 부록 식 19–21) · 식 [4] 셀 임피던스(닫힌 꼴 — "can be readily computed on any programming platform, e.g., MATLAB"). 계면 임피던스: Jacobsen–West TF[65] + MSMR 선형화(Taylor 1 차) → 식 [9] Z̄se(s) — 이중층 C̄dl(CPE n_dl^r) · R̄dl · R̄f · 고체 확산 Z̄s̃(CPE n_f^r) · R̄ct — 적분 동역학을 위한 차단 주파수 ω_dl. 그림 1(회로)은 식이 함의하는 것이지 회로가 식을 정의하지 않는다(위 그림 절).

## Initializing Parameter Estimates (p. 7–12)

`[인쇄]` "it is well known that nonlinear optimization can be very sensitive to initial guesses … **The cost function we aim to minimize exhibits numerous local minima corresponding to suboptimal solutions**, and thus bad initial values may push the model to extreme or unrealistic cases" · "Whenever possible, we prefer to compute initial guesses based on the available cell data rather than an exhaustive search of the literature. Modern battery chemistries often blend multiple materials into the electrode, which can drastically change the physical interpretation of many lumped-parameter values".

- **DRT** — 식 [10](두 R–C) · 식 [11] Z(f) = R∞ + ∫ g(τ)/(1 + j2πfτ) dτ · γ(lnτ) = τg(τ) · `[인쇄]` "Solving Eq. 11 is known to be an **ill-posed problem**, and a proper approach involves two complicated steps: discretization and regularization. In this work, we mainly follow the algorithms developed by Wan et al.68,74 and simply use a **modified version of their open-source DRT toolbox**"(⚠ [68] 은 Ciucci & Chen — "Wan et al.68,74" 저자 귀속 어긋남 · λ · 이산화 미인쇄).
- **Decomposing full-cell impedance** — 그림 3: 두 Φs−e/Iapp 항이 크기 ≈1 → 셀 Nyquist 의 특징은 "primarily projections of the solid-electrolyte interface impedances" · 전해질 TF 는 옴 상수 + 반원 · `[인쇄]` "If the cell impedance data can be decoded (**as previously discussed in Fig. 5**) …"(그림 5 는 뒤 — D).
- **Understanding the interface model components** — 그림 4 · 5: 혹 = Z̄se,B(확산 없는 계면) — `[인쇄]` "In practice, we have found **D̄s^n ≈1×10⁻⁴ s⁻¹ and D̄s^p ≈7×10⁻⁵ s⁻¹** for the physical Panasonic cell"([5] — D̄s 인지 D̄s,ref 인지 미표기 · 표 VI D̄s,ref 2.75×10⁻³ · 1.17×10⁻⁴ · 그림 17(e) SOC 별 D̄s 4.8×10⁻⁴ … 3.6×10⁻² 와 다른 자릿수) · R̄f 는 혹에서 드러나지 않아 Z̄se,C 로 무시 · DRT 봉우리 면적 = 저항이지만 "difficult to evaluate due to the discrete nature of a practical DRT implementation and because peaks are not always clearly separated. Instead, we essentially **invert the DRT function inside an optimization** to find the R̄ct values that reproduce the original bump shape" — 식 [12] 재구성 · 비용 = 재구성 스펙트럼 ↔ 모형 RMSE(무번호) · R̄dl 알면 참값 수렴 · 근사면 "within one order of magnitude"(그림 5(c–d)). ★ 그림 6 · `[인쇄]` "**In practice, we are unable to distinguish the ordering of time constants from the two electrodes. Presently, we simply assume that the smaller time constant (at higher frequency) is associated to the negative electrode and that the larger one (at lower frequency) to the positive electrode.**"
- **Initializing specific model parameter estimates** — 부록으로 · `[인쇄]` "some of the initializations use the DRT method … others are **ad-hoc** and there remains room for improvement. However, we find that even these crude approximations are helpful" · 실셀은 펄스 시험의 최적값으로 EIS 최적화를 시작("We use the latter method when presenting results for the Panasonic cell").

## Pre-Processing of Laboratory Data (p. 12–14)

TF 모형의 Im Z 는 항상 ≤ 0 인데 실측 고주파는 양 — 배선 상호 인덕턴스("moving any part of the wires will cause unpredictable changes … very difficult to eliminate and even to calibrate"[9, 75]) · 잘라 버리면 작은 τ 의 혹이 망가짐(그림 7 — τ ×3.6). **방법 1** 이산 모형 맞춤(그림 8 — 손으로 고른 인덕턴스 모형을 10–100 kHz 에 · "requires user intervention … Whenever the test cables are moved, the model should be also be adjusted"). **방법 2** GDRT(Danzer[69]) — 식 [13] Z = R∞ + jωL∞ + 1/(jωC0) + ∫γRL … + ∫γRC … · 식 [14] 비용 ‖A′x − Z′‖² + ‖A″x − Z″‖² + λxᵀMx · "**λ is a user-selected regularization parameter**" · 식 [15] x = [R∞, L∞, C0, x_RL, x_RC] · 각주 c "the GDRT model Eq. 13 is very sensitive to the highest frequency f_max … It is required to have f_max ≫ (2πτRL)⁻¹, otherwise we will face an under-fitting problem … we can simply adopt the discrete model-fit approach to fit the high-frequency data (e.g., 1 kHz−100 kHz), then manually extrapolate the measured data to even higher frequency regions" · 그림 9(a) · 표 II 검증 · 그림 9(b) 가상 셀 + 잡음(식 [17]).

## Application to A Simulated Cell (p. 14–16)

식 [17] 합성 자료(GDRT 로 인덕턴스 제거 · 그림 10 · 표 III) + 이상 직렬 저항 **R_c**(각주 d) · `[인쇄]` "Note that since we have also emulated measurement noise …, parameter-estimation results are **not expected to be exact**. The primary purpose of studying and analyzing the synthetic data is to **validate the underlying system-identification methods** since no 'truth' values are otherwise available for comparison." 목표 집합 p_EIS · p_pulse(위 그림 절) · ★ 식별성 문단(§(b) 1) · y = ax + b sin(x) 예: 비선형이면 a · b 둘 다 · 선형화하면 (a + b)x 로 합만 — "nonlinearly identifiable" ↔ "not linearly identifiable" · p_EIS^lin · PSS[7] 로 ψ̄.

- **부분 집합**(펄스 참값 고정) — 식 [18] p* = argmin ΣΣ [ℜ(Z − Ẑ)/\|Z\|]² + [ℑ(Z − Ẑ)/\|Z\|]² · `[인쇄]` "Since the magnitudes of cell impedance vary among frequencies, the real/imaginary-part errors are normalized by the magnitudes of the underlying data samples" · "the optimization results are **reproducible since the random number generator in MATLAB is set to be the default seed**" · particleswarm hybrid + fmincon("in some cases, fmincon.m helps yield smaller costs but less accurate parameter estimates") · 48 h · 그림 11.
- **전체 집합** — 펄스 매개변수 시작 = [6] 표 II 의 모의 결과 · k̄0 = 표 X · `[인쇄]` "Since the system TFs are linearized models, **a pulse test is always recommended** in order to expose and understand cell nonlinearities" · 그림 12 · 13 · 14 · "Although the final estimates of many parameters are not exact, it is still difficult to visualize differences in the impedance fitting, showing that we are modeling the impedance well."

## Application to A Physical Cell (p. 16–20)

- **Data collection and process** — Panasonic 셀(연재 [3–6] 과 같은 셀 · Ford C-MAX Energi PHEV 팩 · 각형 25 Ah 흑연//NMC) · Gamry Reference 3000 · 펄스 저항 <2 mΩ 라 정전류 · 고정 배선 · K–K 로 진폭 비교 → **C/50(≈0.5 A)** · 100 % 로 보정 충전 뒤 천천히 방전 · "The impedance measurement at each SOC setpoint takes **about a day** to finish" · Gamry 가 주기 수 자동("we are unable to adjust the number of input cycles manually") · **열아홉 SOC** · "At low cell SOCs, the impedance data are extremely hard to collect because of significant voltage drift. Hence, we use a hybrid mode … at SOCs below 10%" · 그림 15 · 봉우리 A · B · C 배정 가정.
- **Discussion #1: NMC OCP** — "important to have well-calibrated OCP functions, as required when estimating the SOC-dependent D̄s^r and ṅ0,j" · 음극 OCP = [3] · 양극 = [5] 보정판 · 표 V · 그림 16(펄스 재식별 — "gives us more confidence regarding the accuracy for the electrode OCP functions").
- **Discussion #2: Strategies** — `[인쇄]` "In simulation studies, the 'true' values … are known and the impedance data SOC setpoints are exact—the cell is always in an equilibrium state. However, a laboratory process will introduce **SOC drift**, and the impact becomes significant especially at low states of charge. **Unmodeled hysteresis** will also contaminate EIS measurements, especially at low frequencies.76" · Strategy 1(모든 SOC 한 모형 · 식 18) ↔ Strategy 2(SOC 별 모형 · 평균 · D̄s 는 SOC 별 → 한 D̄s,ref 로 다시 맞춤) — "Ideally, Strategy 2 can yield better Nyquist fits … but perhaps less accurate parameter values; while Strategy 1 can find more accurate sets of model parameter values but the model fits … are not as close" · Strategy 2 는 다른 온도에서 초기값 · 경계가 달라 어렵다.
- **Estimating PBM parameter values using laboratory data** — 그림 17 · `[인쇄]` "The agreement is excellent for Strategy 2 results, although the low-frequency fit is slightly skewed due to the optimization method trying to find **insensitive electrolyte components such as n̄e^r**" · "Our hypothesis for the mismatch of using Strategy 1 is that the cell has slight SOC-drift during the frequency-response measurement (especially at low frequencies), and the cell SOC-setpoint we determine from the electrode operating-boundaries are not exact" · 표 VI = Strategy 1 · "Note that we are only able to find n̄e/ψ̄ and κ̄D/ψ̄ (**also assuming ψ̄ = 1 mol S⁻¹ s⁻¹**) rather than n̄e, κ̄D, and ψ̄ individually from the EIS-test."

## One Last Step, Estimating ψ̄ (p. 20–21)

`[인쇄]` "The parameter-estimation strategy presented so far in a series of papers has proposed methods to determine estimates of all LPM parameter values **except for ψ̄**" · 방전 자료 → 단순화 PSS 모형[7] · "In simulation, we find that discharge rates between C/5 and C/2 when collecting the data lead to reasonable results, with **relative error in the estimate of ψ̄ of about 40%**. We used C/2 discharge data with the PSS model to produce the estimate of ψ̄ in Table VI; this value of ψ̄ was also used to compute final values of n̄e^r and κ̄D." — `[해석]` 이 마지막 한 걸음이 표 VI 의 n̄e · κ̄D 둘을 같이 정한다(EIS 비 × ψ̄) — ψ̄ 의 40 % 오차가 둘에 그대로 간다 · 그리고 §(c) 2 의 불일치는 ψ̄ 하나로 풀리지 않는다.

## Summary · Acknowledgments (p. 21)

`[인쇄]` "the final steps required in a comprehensive **nonteardown** process to estimate **all** parameters of a physics-based lumped-parameter model" · "We validated the proposed approach in simulation first, since the true parameter values are known. We found that it was able to find **all parameter values of interest with very good accuracies**. We then applied the approach to a physical graphite//NMC commercial cell, and achieved **consistent** parameter estimates and good matches to the measured impedance data. This gives us confidence that the methodology is providing good estimates of the physical parameters of interest." · ★ `[인쇄]` "To compute the scaling factors, we require knowledge of cell internal dimensions which can be found via teardown if desired. However, scaled lithium concentration in the electrodes (i.e., electrode stoichiometry) and scaled fluxes are sufficient for most applications—**including use as inputs to equations predicting degradation mechanisms**" — 열화 쪽으로 쓰일 수 있다는 유일한 문장(시험 0) · LPM → ROM[78] · 팩[79] · 상태 추정[80] · 급속 충전[81] · 출력 추정[82]. 사사 = Cummins Inc.

## Appendix (p. 22–28)

- **Physics-based model of cell dynamics** — 표 VII(LPM) · MSMR · Darken 항[48, 49] · 표 VIII(모의 매개변수).
- **Transfer functions** — 정의 변수 μ₁^r(s) = 1/(ψ̄Fκ̄^r Z̄se^r(s)) · μ₂^r(s) = (κ̄D T − n̄e^r F s Z̄se^r(s))/(ψ̄κ̄^r F Z̄se^r(s)) · τ₁ · τ₂(n̄e^r s/(ψ̄κ̄^r Z̄se^r)·(1/σ̄^r + 1/κ̄^r)) · Λ₁ · Λ₂ · Λ₃^s = √(n̄e^s s/(ψ̄κ̄^s)) · λ · ω · den · 분리막 · 음극 · 양극 계수 c(A⁻¹) · j(무차원 — 예 j₁^n = c₁^n(−ψ̄κ̄^n(Λ₁^n)² + n̄e^n s)) · `[인쇄]` "all above coefficients are spatially independent; they are functions of input frequency only" · 식 19–21. `[재현·대수]` (n̄e, ψ̄, κ̄D) → (λn̄e, λψ̄, λκ̄D) 에서 μ₂ · τ · Λ · λ · ω · den 은 불변 · μ₁ ∝ 1/λ · c ∝ μ₁ ∝ 1/λ · j = c × (ψ̄ · n̄e 1 차 결합) ∝ λ⁰ ⇒ **셀 임피던스는 이 척도에 불변** — 본문 "never appear alone; they always occur as ratios" 와 정합(전 도출은 미확인 · 인쇄 계수 구조까지만).
- **Initializing model parameter estimates** — C̄dl^r(DRT · 그림 18 — "the average over all SOCs of both are sufficiently close to their actual values") · R̄dl^r · R̄f^r(초기 10⁻⁴ · 10⁻⁶ Ω · "We cannot offer general guidance for how to select the optimization boundaries/constraints for these variables" · **1×10⁻⁶ < R̄dl^r < 1×10⁻¹ Ω · 1×10⁻⁹ < R̄f^r < 1×10⁻¹ Ω**) · κ̄^r · σ̄^r(브루그만 ≈1.5 · σ > κ · 흑연 >100 S m⁻¹ · NMC ≈3.8 S m⁻¹[83–86] · σ̄n 10⁸ · σ̄p 10⁶ S · "inaccurate values of σ̄^r do not significantly impact the impedance-model predictions" · κ̄^s > {κ̄^n, κ̄^p} · **2⁻³·⁵ < κ̄^n/κ̄^s < 1 · 2⁻³·⁵ < κ̄^p/κ̄^s < 1** → K_κ 0.5 · κ̄s,0 5×10³ · **10³ < κ̄^s < 10⁵ S**) · **κ̄D = 2R(t₊⁰ − 1)/F (1 + ∂ln f±/∂ln ce)** — t₊⁰ 0.363 · ∂ln f±/∂ln ce 3 → κ̄D,0 −4.39×10⁻⁴ V K⁻¹ · **0 < t₊⁰ < 0.5 · 0 < ∂ln f±/∂ln ce < 8 → −1.55×10⁻³ < κ̄D < −8.62×10⁻⁵ V K⁻¹** · **ψ̄ = De ce,0/(κ(1 − t₊⁰))** — 아인슈타인 관계[87] → ψ̄0 = RT/(F²(1 − 0.363)) = 4.18×10⁻⁷ · "since the Einstein relation is derived for highly diluted electrolyte … we choose to expand the range" → **2.66×10⁻⁸ < ψ̄ < 6.66×10⁻⁷ mol S⁻¹ s⁻¹** · MSMR αj 0.5 · k̄0,j(그림 19 · 표 X · "boundaries … one order of magnitude around their initial values") · D̄s,ref([5] 초기 · "generally within a factor of two or so from the truth" · **D̄s,ref,0/5 < D̄s,ref < 5D̄s,ref,0**) · **n̄e^r = εe^r ce,0 A L^r/(1 − t₊⁰) · Q_mol = εs^r A L^r cs,max^r \|θ100^r − θ0^r\|** → n̄e^r/Q = (εe/εs)(ce,0/cs,max)(1/(1 − t₊⁰))(1/\|Δθ\|) · εe/εs 2/7–3/4 · ce,0/cs,max 1/50–1/10 · (1 − t₊⁰)⁻¹ 1–2 · \|Δθ\| 0.7–1(각주 e — 흑연 θ0 <0.05 · 0.8 < θ100 < 0.95 · NMC θ0 ≈1 · 0.1 < θ100 < 0.35) ⇒ **Q/175 < n̄e^r < 3Q/14** · n̄e,0 = Q/100 · 분리막 n̄e^s = K_n̄e n̄e^n · **1/4 < K_n̄e < 2** · K0 1 · **n_f · n_dl 초기 0.95 · 경계 0.9–1**.
- **GDRT algorithm** — Danzer[69] 틀을 Wan[74] 계산 틀에 · M 은 γ(lnτ) 의 1 차 도함수 노름 비례 · A′ · A″ 크기 N × (2M + 3) · M 은 (2M + 3) × (2M + 3).

---

# ★ (a) 무엇을 EIS 로 추정하는가 — 열셋 + 갤러리 · 연재 분담 · 비용 · 초기값 · 경계

## 1. 목록과 정의 (`[인쇄]` · 정의식이 없는 것은 그렇게 적는다)

| # | 매개변수 | 단위 | 정의 · 뜻 | 누가 정하나 |
|---|---|---|---|---|
| 1–2 | D̄s,ref^n · D̄s,ref^p | s⁻¹ | 고체 확산 기준값 — D̄s(θs) = D̄s,ref (F/RT) θs(θs − 1) ∂U_ocp/∂θs(Darken · 식 [2]) — D̄s 자체가 D_s/R_s² 꼴의 집약값(입자 크기 흡수) | EIS(초기 = 방전 시험[5]) |
| 3–4 | n_f^n · n_f^p | — | 고체 확산 임피던스의 CPE 지수 | EIS |
| 5–6 | C̄dl^n · C̄dl^p | F | 이중층 용량 집약값 — 정의식 인쇄 0 · 식 [1] 우변 인자 **a_s A L C_dl**(활성 계면 총면적 × 면적당 용량) 꼴 · CPE(n_dl < 1)면 F·s^(n−1) | EIS(초기 = DRT 봉우리) |
| 7–8 | n_dl^n · n_dl^p | — | 이중층 CPE 지수 | EIS |
| 9–11 | n̄e^n/ψ̄ · n̄e^s/ψ̄ · n̄e^p/ψ̄ | S s | **n̄e^r = εe^r ce,0 A L^r/(1 − t₊⁰)**(영역 전해질 Li 함량) ÷ **ψ̄ = De ce,0/(κ(1 − t₊⁰))**(전해질 확산/전도 비) | EIS 는 비만 · ψ̄ 는 PSS[7] |
| 12 | κ̄D/ψ̄ | C mol⁻¹ K⁻¹ | **κ̄D = 2R(t₊⁰ − 1)/F (1 + ∂ln f±/∂ln ce)**(확산 전도 계수) ÷ ψ̄ | EIS 는 비만 · ψ̄ 는 PSS[7] |
| 13 | R_c | Ω | 케이블 ↔ 집전체 접촉 저항(LPM 밖 · 각주 d) — 이상 직렬 저항 | EIS |
| + | k̄0,j^r | mol s⁻¹ | MSMR 갤러리 반응 속도 상수 — R̄ct = RT/(F²Σṅ0,j)(Ω — 전극 전체) 에 들어감 ⇒ 활성 면적 포함 집약값 | EIS(초기 = DRT R̄ct 곁최적화 · 표 X) |
| (EIS 가 안 정함) | Q · θ0^r · θ100^r · U_ocp^r · MSMR{U0, X, ω} | — | 열역학 · 창 = 모드 좌표 | OCP[3] · OCV[4] · 방전[5] |
| (EIS 가 안 정함 — 부분 집합) | α^r · κ̄^r · σ̄^r · R̄f^r · R̄dl^r | — | 전도 · 계면 저항 · 대칭 인자 | 펄스[6](전체 집합 시험에서는 EIS 로 다듬음) |

`[재현]` 셈: 2 + 2 + 2 + 2 + 3 + 1 + 1 = **13** ✅(초록 "thirteen") · k̄0,j 실셀 6 + 5 = 11 · 가상 셀 7 + 4 = 11 · 본문 "six … four … ten"(D). 표 I 의 EIS 행 '최종 추정' 다섯 종(D̄s,ref · n_f · C̄dl · n_dl · k̄0) + '참고 추정' 둘(n̄e/ψ̄ · κ̄D/ψ̄) — R_c 는 표 I 에 없다.

## 2. 비용 · 가중 · 최적화

- **비용** 식 [18]: `p* = argmin Σ_m Σ_n [ℜ(Z − Ẑ)/|Z|]² + [ℑ(Z − Ẑ)/|Z|]²` — 실수부 · 허수부를 **각 자료점의 |Z|** 로 나눈 상대 오차 제곱합 · 주파수 M × SOC N 균등 가중(Strategy 1) / SOC 마다 따로(Strategy 2 — 무번호 식 · 평균 · D̄s 는 SOC 별로 맞춘 뒤 D̄s,ref 하나로). `[해석]` |Z| 정규화는 고주파(|Z| 작음 — 1.7 mΩ 대) 점의 무게를 저주파(|Z| 큼 — 10 mΩ 대)보다 키운다 → 계면 혹 · 직렬 저항 쪽이 강하게, 전해질 · 확산 꼬리가 약하게 맞는다(그림 14 "larger estimation errors at lower frequencies" · 그림 17 "low-frequency fit is slightly skewed" 와 같은 방향 — 가중의 영향 시험은 0).
- **최적화**: MATLAB `particleswarm`(전역 · 무리) hybrid + `fmincon` · 48 h · 기본 시드(실행 하나) · `[인쇄]` "(in some cases, fmincon.m helps yield smaller costs but less accurate parameter estimates)" — **비용이 작아지는데 매개변수가 나빠지는 일**을 저자가 직접 적는다(= 근최적 집합이 넓다는 서명 · 저자는 그렇게 이름 붙이지 않는다).
- **DRT 재구성 곁최적화**(식 [12]): 혹 구간 DRT 봉우리 → (R̄dl 가정) → R̄ct · C̄dl · n_dl(SOC 마다) → R̄ct(θ) 에 k̄0,j 를 맞춤(표 X · 그림 15(f) · 18(c–d)).

## 3. 초기값 · 경계 (부록 · `[인쇄]` — `[재현]` 은 같은 식으로 다시 계산)

| 매개변수 | 초기값 | 경계 | `[재현]` |
|---|---|---|---|
| R̄dl^r · R̄f^r | 10⁻⁴ · 10⁻⁶ Ω | 10⁻⁶–10⁻¹ · 10⁻⁹–10⁻¹ Ω | — |
| σ̄^n · σ̄^p | 10⁸ · 10⁶ S | 미인쇄 | — |
| κ̄^s · K_κ^n · K_κ^p | 5×10³ S · 0.5 · 0.5 | 10³–10⁵ S · 2⁻³·⁵–1 | 2⁻³·⁵ = 0.0884 |
| κ̄D | −4.39×10⁻⁴ V K⁻¹ | −1.55×10⁻³ … −8.62×10⁻⁵ | 2R(0.363 − 1)/F × 4 = −4.391×10⁻⁴ ✅ · 범위 −1.551×10⁻³ … −8.617×10⁻⁵ ✅ |
| ψ̄ | 4.18×10⁻⁷ mol S⁻¹ s⁻¹ | 2.66×10⁻⁸ … 6.66×10⁻⁷ (RT/(10F²) … 2.5RT/F²) | RT/(F²·0.637) = 4.180×10⁻⁷ ✅ · 2.663×10⁻⁸ · 6.657×10⁻⁷ ✅ |
| n̄e^r(n · p) · K_n̄e | Q/100 · 1 | Q/175 … 3Q/14 · 1/4–2 | 비 곱 (2/7·1/50·1·1) … (3/4·1/10·2·10/7) = 1/175 … 3/14 ✅ |
| n_f · n_dl | 0.95 | 0.9–1 | — |
| D̄s,ref | 방전 시험[5] 값 | ×1/5 … ×5 | — |
| αj · k̄0,j | 0.5 · 표 X | k̄0,j: ×1/10 … ×10 | — |
| C̄dl | DRT 봉우리(그림 15(e) · 18(a–b)) | 본 최적화 경계 미인쇄(그림 5 범례 0.01–200 은 DRT 곁최적화) | — |

`[재현]` 초기값 식 ↔ 그림의 초기 X(가상 셀 — 참값으로 정규화): κ̄D/ψ̄ (−4.39×10⁻⁴/4.18×10⁻⁷)/(−1.24×10⁻⁴/2.52×10⁻⁷) = **2.13** ↔ X ≈2.12 ✅ · n̄e/ψ̄ (Q/100)/ψ̄0 = 1.95×10⁴ S s ↔ 참 8.41 · 5.44 · 6.98 ×10⁴ → **0.232 · 0.359 · 0.280** ↔ 그림 12(b) X ≈0.22 · 0.36 · 0.27 ✅ — 초기화 식이 실제로 쓰였다. 반면 D̄s,ref^p 초기 X **0.141**(참 = 초기 ×7.1)은 인쇄 경계 ×5 밖인데 1.0 으로 수렴(그림 11–12(a)) → **인쇄된 D̄s,ref 경계가 그대로 적용되지 않았거나 초기값 기준이 다르다**(D). 그리고 실셀은 `[인쇄]` "also assuming ψ̄ = 1" 로 n̄e · κ̄D 를 맞췄다 — 위 n̄e · κ̄D 경계(물리 단위)를 ψ̄ = 1 인 비에 어떻게 옮겼는지 0(G3).

## 4. DRT 의 자리 — 초기값 도구 (최종 추정 아님)

DRT 가 하는 일은 셋: ① GDRT 로 배선 인덕턴스(R–L 분포 · L∞)를 걷어 냄 ② 혹 구간 봉우리 둘 → 계면 R̄ct · C̄dl · n_dl 초기값 ③ R̄ct(θ) → k̄0,j 초기값 · 경계. 최종값은 TF 모형 회귀(식 18)가 정한다. 그래서 DRT 봉우리 수 · 배정의 비유일성은 **초기값과 경계**를 통해 결과에 들어간다(k̄0,6/7 처럼 참값이 경계 밖으로 밀리는 경로 — §(b) 3).

---

# ★ (b) 식별성 (Q4) — 구조 · 선형 · 실제 · DRT 봉우리

## 1. 구조적 식별성 — 인용으로 주장

`[인쇄]` "We know from Ref. 2 that **all parameters of the PDE version of the LPM are identifiable**" · 서론 "the equations of the DFNe model must be reformulated and the parameters of the equations must be lumped together to form an identifiable lumped-parameter model (LPM). The most comprehensive description of this analytic process is found in Ref. 2". Ref. 2 = Plett & Trimboli, "Process for lumping parameters to enable nondestructive parameter estimation for lithium-ion physics-based models", *Proc. EVS-35* Oslo, June 2022(학회 판 · 미열람). 이 지면에는 그 증명의 식 · 조건 · 가정(무엇을 알려진 입력으로 두는가 — 예: OCP · 창 · Q)이 0. `[해석]` 95호가 원 35 → 24 를 "구성 증명(출력 = 묶음 함수)" 으로 보였어도 24 의 식별성은 증명하지 않았던 것처럼, "lumping makes it identifiable" 은 **같은 출력을 내는 다른 매개변수 조합이 없다**는 명제인데 그 검사는 인용 너머에 있다.

## 2. 선형(소신호) 비식별 — 손 분석으로 둘

- `[인쇄]` "it is important to recognize that not all parameters of the **linearized TF model** turn out to be identifiable. We describe this phenomenon by saying that the LPM is 'nonlinearly identifiable' but 'not linearly identifiable.'" · 예 y = ax + b sin(x) → 선형화 (a + b)x · "It is not at all obvious from a casual glance at the TF equations that such a **redundancy** exists in the TFs. However, some detailed analysis shows that in the model, parameters ψ̄, n̄e^r, and κ̄D **never appear alone; they always occur as ratios** of n̄e^r/ψ̄ and κ̄D/ψ̄."
- `[재현·대수]` 부록에 인쇄된 TF 계수로 확인: μ₂^r = (κ̄D T − n̄e^r F s Z̄se)/(ψ̄κ̄^r F Z̄se) · τ₂^r ∝ n̄e^r/ψ̄ · Λ₃^s = √(n̄e^s s/(ψ̄κ̄^s)) 은 **비만** 담고, μ₁^r = 1/(ψ̄Fκ̄^r Z̄se) 는 1/ψ̄ · 계수 c ∝ μ₁ · j = c(−ψ̄κ̄Λ² + n̄e s) 에서 ψ̄ 가 상쇄 ⇒ (n̄e, ψ̄, κ̄D) → (λn̄e, λψ̄, λκ̄D) 에서 셀 임피던스 불변 — 저자 명제와 정합(인쇄 계수 구조까지 · 전 도출 미확인).
- `[인쇄]` p. 16 "**the impact of R_c and 1/κ̄^s on the full-cell impedance are identical**; i.e., they cannot be separated in any linear way" — 도출 0.
- `[해석]` 이 둘은 [[spm-grouped-parameter-identifiability]] 의 "선형화(한 DoD)" 행 — 28호 식 50("infinite number of pairs" — 두 전극 동역학이 R_ct 하나로) — 과 같은 부류의 **선형화가 만드는 비식별**이다. 28호와 다른 점: 28호는 이것을 식별 집합의 정의로 끝까지 밀었고(θ̃ = 3 개), 이 편은 비 둘을 식별 집합에 넣고 ψ̄ 를 다른 시험(PSS)으로 뺐다 — **식별성을 시험 분담으로 산다.**

## 3. 실제적 식별성 — 합성 참값 시험 (가상 셀 하나 · 같은 모형 · 잡음 하나 · 실행 하나)

설계(`[인쇄]`): 표 VIII · IX 참값 → 식 [4] TF 로 임피던스 + 배선 인덕턴스(L0 52 nH + R–L 둘) + 곱셈 잡음 ε 0.5 %(η ~ N(0, 0.2) — 표준 정규라 쓰고 0.2 를 단 모순 · `[재현·가정]` 0.2 가 표준편차면 상대 잡음 0.1 % · 분산이면 0.22 %) → GDRT 로 인덕턴스 제거 → R_c(1 mΩ) 더함 → 식 [18] 회귀. **역범죄**(같은 TF 가 자료를 만들고 맞춤 — 28 · 95호와 같은 설계) · 잡음 실현 하나 · 최적화 실행 하나(기본 시드) · 참값 하나.

| 매개변수 | 부분 집합 (그림 11 · 펄스 참값 고정) | 전체 집합 (그림 12 · 13) | 비고 |
|---|---|---|---|
| D̄s,ref^n · ^p | ≈1 · 1.00 | ≈0.95–1 · 1.00 | 양극 초기 ×0.141(경계 ×5 밖)에서 수렴 |
| n̄e^n/ψ̄ | ≈1.05 | **1.20** | |
| n̄e^s/ψ̄ | **1.48** | **0.48** | 같은 매개변수가 두 시험에서 반대 방향 ±50 % |
| n̄e^p/ψ̄ | 0.95 | **1.25** | |
| C̄dl^n · ^p | ≈1 · ≈1 | 1.03 · ≈0.97–1.0 | |
| n_f · n_dl | 0.996–1.00 | 0.991–1.00 | **참값 1 = 경계 상한** |
| κ̄D/ψ̄ | 1.01 | **1.19** | |
| R_c | 1.00 | **1.64** | 초기 X = 1.0(참값에서 출발) |
| σ̄^n · σ̄^p | (고정) | ≈1.06 · **≈1.66** | |
| κ̄^n · κ̄^s · κ̄^p | (고정) | ≈1.29 · ≈0.88 · **≈1.44** | |
| R̄dl^n · R̄dl^p · R̄f^n | (고정) | ≲1 · ≈1 · **≈0.4** | 판독 폭 ±0.3 |
| k̄0,j^n j1–5 | (고정) | ≈1.1 · 1.14 · 0.74 · 1.09 · 1.19 | j3 크게 요동 |
| k̄0,6^n · k̄0,7^n | (고정) | **축 밖 — 도달 불가** | 초기 ×12,867 · ×4,107 · 경계 ±1 자릿수 → 참값이 하한의 1/1,287 · 1/411 `[재현]` |
| k̄0,j^p | (고정) | 0.92 · ≈1 · ≈1 · 0.97 | |
| 출력 잔차 | — | ≲0.04 mΩ(그림 14) | 매개변수가 19–66 % 어긋난 같은 적합 |

`[도표·화소]` 판독 · 판독 폭 ±0.02(그림 11–12 정규화 축) · ±0.3(그림 13(b)). ★ **판정**: 부분 집합은 n̄e^s/ψ̄ 하나를 빼면 ±5 % 안이다(저자 서술 "nearly universally the case" 와 맞음 — 그리고 저자가 그 하나를 감도로 설명). **전체 집합은 다섯(n̄e^n/ψ̄ · n̄e^s/ψ̄ · n̄e^p/ψ̄ · κ̄D/ψ̄ · R_c)이 19–64 %, 펄스 셋(σ̄^p · κ̄^p · κ̄^n)이 29–66 % 어긋나고 출력은 ≲0.04 mΩ 로 맞는다** — 이것이 근최적 집합의 폭이다. 초록 "highly accurate" · 결론 "very good accuracies" 는 부분 집합에만 선다(초록 · 결론이 이 조건을 뗐다).

## 4. 직렬 저항 골짜기 — R_c ↔ 1/κ̄^s ↔ R̄f^n (`[해석]` · `[재현]`)

저자가 이름 부른 쌍은 R_c ↔ 1/κ̄^s 다. 그러나 `[재현]` 1/κ̄^s 의 참값은 1/5758 = **0.174 mΩ** 이고 그림 13(a) 의 κ̄^s ≈0.88 은 1/κ̄^s 를 **+0.024 mΩ** 만 바꾼다 — R_c 의 **+0.64 mΩ** 를 혼자 상쇄하지 못한다. 크기가 맞는 것은 **R̄f^n**(참 1 mΩ · 추정 ≈0.4 → **−≈0.6 mΩ**)이다: `[재현]` 그림 3(b) 계면 혹 시작 = R̄f^n + R̄ct∥R̄dl = 1.434 mΩ 로 **R̄f^n 이 셀 임피던스에 직렬로 그대로 더해진다**(양극 0.750 mΩ 도 같은 식). ⇒ `[해석]` 소신호 EIS 에서 R_c · 1/κ̄^s · R̄f^n(· R̄f^p) 는 **직렬 합 하나**로 보이는 골짜기이고, 그 안의 배분은 최적화가 어디서 멈추느냐가 정한다(그림 13(b) 판독 폭 ±0.3 — R̄f^n 0.2–0.6 이면 합 R_c + R̄f^n = 1.84–2.24 ↔ 참 2.0 mΩ). 부분 집합(R̄f · κ̄ 참값 고정)에서는 R_c 가 1.00 으로 정해진다 — **고정된 것이 골짜기를 막는다**. 저자는 R̄f 를 이 쌍에 넣지 않았다(펄스 시험 매개변수로 다룸).

## 5. DRT 봉우리 수 · 전극 배정 — 저자 자신의 그림이 보이는 것

- `[인쇄]` p. 8 "a single Nyquist bump can arise from the combination of two (or more) time constants whose impedances overlap in the frequency domain. **The DRT procedure can help uncover the individual time constants**" · p. 9 "we expect at least two due to the contributions from (at least) the double-layers of both electrodes".
- 그러나 같은 지면이 배정을 가정으로 둔다: `[인쇄]` p. 11 "**In practice, we are unable to distinguish the ordering of time constants from the two electrodes. Presently, we simply assume** that the smaller time constant (at higher frequency) is associated to the negative electrode" · p. 17 "We assume that peak A is associated to the negative-electrode, peak B … positive-electrode, and peak C … solid-diffusion impedance".
- 그림이 보이는 비유일성(본문 언급 0 · `[도표·화소]`): ① 그림 5(b) — **한 요소(CPE R–C · n_DL 0.9) → γ(τ) 극대 셋**(이상 n = 1 은 하나) ② 그림 6(a) — **과정 다섯(계면 둘 · 전해질 확산 · 고체 확산 둘)인 참 모형에서 극대 15**(계면 둘 + τ 0.15 s–9.4×10³ s 열셋 — 본문은 열셋을 "electrolyte and solid-diffusion" 묶음으로만 부름) ③ 그림 7 — 배선 인덕턴스를 잘라 내면 봉우리 τ ×3.6 ④ 그림 15(d) — 실셀 C(≈3×10⁻² s)에 '고체 확산' 이름 · 가상 셀은 같은 τ 대(≈4×10⁻² s)가 양극 계면.
- ★ **배정이 최종 적합에서 유지되지 않은 흔적**: 실셀 DRT 초기 C̄dl 평균선 음극 ≈4.0 F · 양극 77.7 F(그림 15(e)) → 표 VI 최종 **음극 10 F · 양극 5.38 F** — 크기 순서가 뒤집혔다(×2.5 · ×0.069). `[해석]` 최종 회귀가 DRT 배정(A = 음극 · B = 양극)의 C 크기를 그대로 두지 않았다 — 두 전극 계면 매개변수의 맞바꿈(전극 이름표 교환)이 소신호 EIS 에서 거의 대칭인 방향이라면(두 전극을 가르는 것은 OCP 기울기 · MSMR 의 SOC 의존뿐) 이런 이동이 생긴다. 이 편은 이 대칭을 검사하지 않는다(G4).
- ⇒ [[drt-peak-count-nonidentifiability]] 체크리스트(아래 §6 · 개념 페이지 여덟 번째 경보): C1 ❌(λ "user-selected" · 값 0) · C2 ✅ 명명(K–K · 잔차 0) · C3 ❌ · C4 ❌(배정 = τ 순서 가정) · C5 ❌(셀 하나 · SOC 당 측정 하나).

## 6. Q4 어휘 · 판정 (카드 형식)

| 낱말(본문 · NFKC · 줄 끝 하이픈 복원 · 꼬리말 제외) | 수 | 쓰임 |
|---|---|---|
| `identifiab*` | **19**(`nonidentifiab*` 4 포함 · NFKC 전 0 — 합자) | 서론 정의 · LPM 동기 · 선형/비선형 식별 문단 · 부록 K_κ · k̄0 물음 |
| `uniqu*` | 4 | "non-unique solutions" · MSMR "uniquely determines" · "cannot uniquely identify all parameters" · "unique function of θs" |
| `sensitiv*` · `insensitiv*` | 15 · 6 | Rabissi 인용 · "A sensitivity study shows …"(결과 0) · k̄0 · n̄e 둔감 · GDRT f_max 민감 |
| `confiden*` · `reliab*` | 3 · 2 | 전부 수사("gives us confidence") · "reliably"(펄스 시험 SOC 부족) — 통계 구간 0 |
| `Fisher` · `covarian*` · `Hessian` · `Jacobian` · "condition number" · `bootstrap` · `posterior` · `Bayes*` · `uncertain*` · `profile` | **0** | — |
| `redundan*` · `ill-posed` · `regulariz*` | 1 · 1 · 3 | TF 비 중복 · DRT 역변환 · λ |
| `noise` · `error*` · `accura*` · `true/truth` · `synthetic` | 10 · 7 · 14 · 19 · 7 | 합성 시험 |
| `local minim*` · `global` · `initial*` · `bound*` · `constrain*` | 2 · 2 · 37 · 17 · 8 | 초기값 · 경계 절 |
| `validat*` · `verif*` · `consisten*` | 9 · 2 · 2 | "validate the underlying system-identification methods" · Kong[64] · Duan 인용 · 결론 "consistent parameter estimates" |
| `degenera*` | 0 | — |

**판정 — ASSB 0/96 · 도구 칸 · 여든여덟 번째 성질**: "**소신호 EIS 로 집약 매개변수 열셋을 정한다고 하면서 구조적 식별성은 인용(학회 판)으로만 주장하고, 선형 비식별 둘(비 n̄e/ψ̄ · κ̄D/ψ̄ · 직렬 R_c ↔ 1/κ̄^s)은 손 분석 결론만 인쇄하며, 합성 참값 시험(같은 모형 · 잡음 실현 하나 · 실행 하나)에서 전체 집합의 다섯이 19–64 % · 펄스 셋이 29–66 % 어긋나고 두 갤러리의 참값이 경계 밖인 결과를 출력 잔차 ≲0.04 mΩ 와 함께 '매우 좋은 정확도' 로 요약했다 — DRT 봉우리의 전극 배정은 τ 순서 가정이고, 실셀 최종값은 같은 지면이 인쇄한 물리 범위 밖에 놓인다.**" 28호(선형화 SPM · 식별 집합 3 · 등고선)와 95호(DFN 묶음 · 직교화 순위 · 다중 시작 50)에 이은 **셋째 액체 식별성 도구 편** — 셋 다 FIM · 신뢰구간 0 이고, 셋 중 **모드 좌표를 식별 집합에 넣은 것은 95호뿐**(28 · 96호는 입력). 누적 0.5 그대로(ASSB 근거 아님).

---

# ★ (c) 검증 — 무엇과 대조했나 · 실셀 최종값의 자기 폐합

## 1. 대조한 것 · 안 한 것

| 대조 | 이 편 | 판정 |
|---|---|---|
| 독립 측정(해체 · GITT · 3전극 · 기준극) | 0 | ❌ — 연재 목표가 '해체 없음' 이라 설계상 0 · 대신 OCP 는 [3] 의 'teardown-based approaches'(흑연) |
| 시간 영역 예측 | 0 — `[인쇄]` "planned for future publications" | ❌ |
| 가상 셀 참값 복원 | 하나 · 같은 모형 · 잡음 하나 · 실행 하나 | ⚠ §(b) 3 |
| 실셀 임피던스 맞춤 | Strategy 1 어긋남 · Strategy 2 좋음(그림 17) · 수치 잔차 0 | ⚠ 맞춤 = 검증 아님 |
| 두 전략 사이 매개변수 일치 | κ̄D/ψ̄ ×2.4(−0.040 ↔ −0.097) · D̄s SOC 별 ×70 범위 | ⚠ |
| 펄스 시험 재적합(그림 16) | OCP 보정 뒤 더 잘 맞음 | 펄스 시험의 검증 — EIS 추정과 무관 |
| 같은 지면 물리 범위 · 경계와의 폐합 | 이 digest 가 함(§2) | ❌ 넷 밖 · 둘 경계 위 |

셀 · 조건(`[인쇄]`): **Panasonic 25 Ah 각형 흑연//NMC 하나**(Ford C-MAX Energi PHEV 팩에서 꺼냄 · 연재 [3–6] 과 같은 셀 · 이력 · SOH 미인쇄 G12) · **25 °C 하나**(표 IV 는 온도 반복 틀이나 결과는 25 °C 만 · "temperature-dependence is beyond the scope of this paper") · **19 SOC**(그림 17(f) 6.4 … 100 % `[도표·화소]`) · C/50 ≈0.5 A 정전류(SOC <10 % 혼성) · 100 kHz–0.1 mHz(142 점 `[재현]`) · 휴지 ≥6 h · SOC 당 ≈하루.

## 2. ★ 표 VI ↔ 같은 편 부록의 경계 · 물리 범위 (`[재현]`)

| 표 VI 값 | 부록이 인쇄한 범위(초기화 절) | 판정 |
|---|---|---|
| n̄e^n 1.0166 mol | Q/175 = 0.00533 … 3Q/14 = **0.1999** mol(Q 0.9328) | ❌ **×5.1 위** — 셀 가동 Li 재고 Q 보다 크다 · 가상 셀 n̄e^n/Q 0.026 ↔ 실셀 1.09(×42) |
| n̄e^s/n̄e^n = 2.0332/1.0166 = **2.0000** | K_n̄e 1/4 … **2** | ⚠ **상한 위** |
| n̄e^s/n̄e^p = 13.7 | n̄e^p/4 < n̄e^s < 2n̄e^p | ❌ (K 재매개화가 n̄e^n 쪽 제약만 남겼다) |
| n̄e^p 0.1487 mol | 0.00533 … 0.1999 | ✅ |
| κ̄D −1.46×10⁻⁸ V K⁻¹ | −1.55×10⁻³ … −8.62×10⁻⁵ | ❌ **크기 ×1/5,900** |
| ψ̄ 3.66×10⁻⁷ | 2.66×10⁻⁸ … 6.66×10⁻⁷ | ✅ |
| κ̄^s 7176 S · κ̄^n/κ̄^s 0.813 | 10³–10⁵ · 2⁻³·⁵–1 | ✅ |
| κ̄^p/κ̄^s = 515/7176 = **0.0718** | 2⁻³·⁵ = 0.0884 … 1 | ❌ ×0.81 아래 |
| R̄dl^n **1.00×10⁻¹⁰ Ω** · R̄dl^p 3.98×10⁻⁴ | 10⁻⁶ … 10⁻¹ | ❌ **×10⁻⁴ 아래**(정확히 1.00×10⁻¹⁰ — 그림 5(c–d) 스윕 하한과 같은 수) · ✅ |
| R̄f^n 1.03×10⁻³ · R̄f^p 6.62×10⁻⁹ | 10⁻⁹ … 10⁻¹ | ✅ · ✅(하한 ×6.6) |
| n_f 0.96 · 0.92 · n_dl 0.92 · **0.90** | 0.9 … 1 | ✅ · n_dl^p **하한 위** |
| 창 폭 \|θ100^p − θ0^p\| = 0.688(표 V) | n̄e 경계 유도의 가정 0.7 … 1 | ⚠ 약간 밖 |

★ **ψ̄ 하나로 풀리지 않는다** — 표 VI 의 n̄e · κ̄D 는 EIS 비 × PSS ψ̄ 다: n̄e^n/ψ̄ = 2.78×10⁶ S s · κ̄D/ψ̄ = −0.0399 C mol⁻¹ K⁻¹. n̄e^n ≤0.1999 mol 이려면 ψ̄ ≤**7.2×10⁻⁸**, \|κ̄D\| ≥8.62×10⁻⁵ 이려면 ψ̄ ≥**2.2×10⁻³** — **두 조건 사이가 ×3×10⁴** 이고 ψ̄ 의 인쇄 범위(2.66×10⁻⁸ … 6.66×10⁻⁷)는 앞 조건 쪽에 한 끝만 걸친다 ⇒ **EIS 가 낸 두 비가 같은 편의 물리 범위와 함께 맞을 ψ̄ 가 없다.** 인쇄 범위로 만든 κ̄D/ψ̄ 의 허용 범위는 −5.8×10⁴ … −129(가상 셀 참 −492 은 안)인데 실셀 Strategy 1 −0.040 · Strategy 2 SOC 별 −0.031 … −0.36 은 **3–4 자릿수 밖**이다. `[해석]` 저자 문장 "the optimization method trying to find **insensitive** electrolyte components such as n̄e^r" 과 함께 읽으면, 실셀 EIS 는 전해질 묶음(n̄e/ψ̄ · κ̄D/ψ̄)을 **정하지 못했고** 최적화가 물리 범위 밖에서 멈췄다 — 그 값이 표 VI 에 3 유효숫자로 인쇄됐다. 경계를 실셀에 어떻게 적용했는지가 인쇄되지 않아(G3 — 특히 "ψ̄ = 1" 가정 아래 물리 단위 경계의 처리) 저자 오류로 단정하지 않는다(주장하지 않는 것 2).

## 3. "consistent" 의 근거

결론 "achieved **consistent** parameter estimates" — 지면에서 일관성의 근거로 읽히는 것은 ① Strategy 1 ↔ 2 의 값 비교(그림 17(e–f) "Samples of parameter estimates from Strategy 2" — 표 VI 와 수치 대조 0 · 우리 판독으로 κ̄D/ψ̄ ×2.4) ② 그림 16 의 펄스 재식별(다른 시험) 둘뿐이다. 반복 측정 · 다른 셀 · 다른 온도 · 재조립 0.

---

# ★ (d) EIS 를 '관측 추가' 로 — 이 편 방식이 LLI · LAM 을 가르는가 (`[해석]` · 조건 붙임)

## 1. 이 편 그대로는 아니다 — 모드 좌표는 EIS 의 입력이다

LLI · LAM 이 사는 곳 = 전극 창 θ0^r · θ100^r 과 용량 Q(그리고 전극 용량 = Q/\|Δθ\|) — 이 편에서는 OCV[4] · 방전[5] 시험의 **값**이고 EIS 최적화의 **입력**이다(표 I · `[인쇄]` "By the end of this step [iv], the thermodynamics of the cell are completely characterized"). EIS 는 그 창 위에서 계면 · 수송 · 이중층을 읽는다. 따라서 이 편의 출력에는 LLI ↔ LAM 을 가르는 항이 없다 — 28호(Q_th · x⁰ 입력 · 식별 집합에 모드 축 없음)와 같은 쪽 끝이다. 저자도 열화 쪽 쓰임은 한 문장으로만 적는다(`[인쇄]` "scaled lithium concentration in the electrodes … and scaled fluxes are sufficient for most applications—including use as inputs to equations predicting degradation mechanisms").

## 2. 그러나 열리는 채널이 있다 — 전극별 C̄dl · k̄0 · D̄s,ref

LPM 의 C̄dl^r(식 [1] 의 a_s A L C_dl — 활성 계면 총면적 비례)과 k̄0,j^r(R̄ct = RT/(F²Σṅ0,j) — 전극 전체) 은 **OCV 창과 다른 관측 채널**이다. 노화 셀에 되풀이하면(이 편은 안 함) 기구마다 다른 서명이 예상된다(`[해석]` — 모형 정의 위의 대수 · 시험 0):

| 기구 | 창 · Q(OCV 채널) | C̄dl^p | k̄0^p(R̄ct^p) | D̄s,ref^p |
|---|---|---|---|---|
| LLI | 창 이동(θ0 · θ100 같이) · Q^p 불변 | 불변 | 불변(θ 의존은 OCP 위치로만) | 불변 |
| LAM_PE — 입자 통째 소실 · 비연결(ε_s 형) | Q^p ↓(창 폭 넓어짐) | ↓(면적 같이) | ↓(같은 비율) | 불변 |
| LAM_PE — 자리 소실(c_max 형) | Q^p ↓ | 불변 | ≈불변 | ≈불변 |
| 표면 접촉 손실(A_eff ↓ · 입자 연결 유지) | 불변 | ↓ | ↓(같은 비율 — k̄0/C̄dl 불변) | ≈불변 |
| 계면층 성장 | 불변 | ≈불변 | ↓ 또는 R̄f ↑ | — |

⇒ OCV 창 맞춤의 **LLI ↔ LAM_PE 축퇴 방향**(우리 `degradation-degeneracy` 의 물음 — 수치는 RESULTS*.md 가 정본)에 대해, C̄dl^p 는 LLI 에 무감 · LAM_PE(ε_s 형)에 민감한 **직교 후보**다. 그리고 카드의 곱 축퇴(A_eff · k₀)에 대해서는 C̄dl(∝ A_eff) · k̄0(∝ k₀ A_eff) 를 **같이** 내는 것이 처방 1단계("R · C 를 같이") 그 자체다 — 이 편은 그것을 **전극별 · 완전지 · 2전극**으로 낸다(카드 곱 축퇴 일흔아홉 번째 적용).

## 3. 조건 다섯 — 이것이 없으면 채널이 닫힌다

① **전극 배정**: 두 계면 봉우리의 전극 이름은 τ 순서 가정이고(§(b) 5), 실셀 최종 C̄dl 은 DRT 초기 순서와 뒤집혔다 — LAM_PE 서명을 음극에 붙일 위험. ② **C̄dl = CPE 계수**: 실셀 n_dl 0.90–0.92 — 단위가 F·s^(n−1) 이고 n 이 노화로 바뀌면 C̄dl 비교가 무의미해진다(면적 비례성은 n = 1 에서만 깔끔). ③ **산포**: SOC 무관 매개변수(κ̄D/ψ̄)의 SOC 별 추정이 ×12 퍼진다(그림 17(f)) — 노화 추세가 이보다 작으면 묻힌다. ④ **비용**: SOC 당 ≈하루 · 19 SOC ≈19 일(`[재현·가정]`) — RPT 로 반복하기엔 비싸다(세미나 3번째 논문은 충전 또는 방전 뒤 15 분 휴지 · 10 kHz–0.1 Hz 51 점(유도성 빼고 43) 스펙트럼 하나 — 저주파 끝이 이 편 0.1 mHz 보다 3 자릿수 위 · sun2025 digest 전사). ⑤ **식별성**: 같은 모형 합성에서도 펄스 매개변수가 29–66 % 움직였다 — 노화 축 추정의 폭이 노화 신호보다 클 수 있다.

## 4. 세미나 3번째 논문(학습형)과의 대조 — 같은 EIS, 다른 물음

| | Sun 2025 (sun2025 digest 전사) | Lu 2022 (이 편) |
|---|---|---|
| 읽는 것 | EIS 스펙트럼 → **적합된 LLI · LAM_PE · LAM_NE 라벨**(반쪽전지 창 맞춤 — 우리 α·β 와 같은 대수) | EIS → **물리 매개변수**(계면 · 수송 · 이중층) · 모드 좌표는 입력 |
| 모형 | P2D 임피던스 모의 1,000 개 사전학습 + 실험 미세조정 | 닫힌 꼴 LPM TF + 최적화 |
| 열화 | 있음(노화 셀 · 라벨) | 없음 |
| 식별성 | 라벨의 비식별성을 물려받음 · LLI ↔ LAM_PE 주의 패턴이 한 패턴의 부호 반전(r = −0.962) | 선형 비식별 둘 인쇄 · 합성에서 19–64 % · 실셀 범위 밖 |
| 참값 시험 | 라벨이 적합값(참값 아님) | 가상 셀 하나(같은 모형) |

`[해석]` 둘 다 "EIS 가 모드를 가르는가" 를 **참값으로** 시험하지 않았다 — Sun 은 라벨(적합값)과의 상관을, 이 편은 모드 밖 매개변수를 읽었다. 우리가 공급할 수 있는 것: **합성 truth 에서 모드를 알고 EIS 를 같이 만드는 시험** — LLI ↔ LAM_PE 축퇴 방향(OCV 로 안 갈리는 쌍)을 따라 C̄dl^p · k̄0^p · D̄s,ref^p 가 움직이는지, 그리고 그 움직임이 이 편 같은 최적화의 근최적 폭(그림 12–13 수준)보다 큰지. ⚠ 설계 메모일 뿐이다 — 하네스 코드(`degradation-degeneracy/` src · tools · configs · scripts)에 EIS 출력을 더하면 RUN_SCOPE 의 code identity 가 움직인다(별도 승인 · 게이트 대상).

---

# ★ (f) Q1–Q8 — 채움표 칸 (닻 카드 수집 지침)

| Q1 정량 | Q2 독립관측 | Q3 라벨층위 | Q4 유일성 | Q5 Li-In | Q6 압력 | Q7 dead Li | Q8 화학·OCP |
|---|---|---|---|---|---|---|---|
| **없다 — 액체셀.** `contact` 1 = 케이블 ↔ 집전체 접촉 저항 R_c(옴 · 각주 d) · 열화 0 · `θ(N)` **0/96**. 층 하나 `[해석]`: LPM 의 C̄dl^r(a_s A L C_dl — 식 [1]) · k̄0,j^r(전극 전체 교환율) 가 둘 다 활성 계면 면적에 비례 — 표면 접촉 손실 A_eff 는 둘을 같은 비율로(k̄0/C̄dl 불변) · 순수 k₀ 손실은 k̄0 만 · 입자 통째 비연결은 Q · 창 폭 + C̄dl + k̄0 를 같이 움직일 자리 — **전극별로 C̄dl · k̄0 를 따로 내는 첫 액체 완전지 EIS 파이프라인 = 곱 축퇴 처방 1단계 입력의 액체 완전지판**(배정 가정 · CPE · 노화 0) | **없다** (ASSB 관측 0) — EIS 하나 · 2전극 · 두 계면 봉우리의 전극 배정 = τ 순서 **가정**(`[인쇄]` "we simply assume") · 독립 대조 0 | 칸 없음 · **층 하나: "적합(particleswarm + fmincon · 부록 경계 · DRT 초기값) + 합성 참값 복원(가상 셀 하나 · 같은 TF 모형 · 잡음 0.5 % 실현 하나 · 실행 하나) — 불확실성 0 · 실셀 최종값 표 VI 이 같은 편 경계 · 물리 범위 밖(n̄e^n ×5.1 · κ̄D ×1/5,900 · R̄dl^n ×10⁻⁴ · κ̄^p/κ̄^s · 경계 위 둘) · Strategy 1 ↔ 2 κ̄D/ψ̄ ×2.4 · SOC 별 ×12 · 실셀 α 미인쇄"** | **★ 있다 — 단 액체(도구 칸). ASSB 0/96 — 여든여덟 번째 성질**(§(b) 6) — 구조적: 인용(Ref. 2 학회 판) / 선형: 비 n̄e/ψ̄ · κ̄D/ψ̄ · R_c ↔ 1/κ̄^s(손 분석 · `[재현·대수]` 비 구조 ✅ · `[해석]` R̄f^n 도 같은 직렬 골짜기) / 실제적: 같은 모형 합성 하나 — 전체 집합 다섯 19–64 % · 펄스 셋 29–66 % · k̄0,6/7 참값 경계 밖 · 출력 ≲0.04 mΩ · `identifiab*` 19 · FIM · CI · 프로파일 0 · 누적 0.5 그대로 | **해당 없음** — 액체 · 기준극 0 · 전극 배정은 가정 | **없다** (`pressure` 0 · 각형 상용 셀) | **해당 없음** | **층 하나 — 흑연//NMC(조성 미인쇄) MSMR OCP**(표 V — 흑연 6 갤러리 = Ref. 3 의 'teardown-based' 방법 · NMC 5 갤러리 = Ref. 5 방전 시험으로 셀 안 재보정 — 첫 판은 "not well calibrated" 로 버림) · 창 θ0^n 0.0007 · θ100^n 0.8279 · θ0^p 0.9144 · θ100^p 0.2263 · Q 0.9328 mol(`[재현]` 25.00 Ah) · OCP 측정 · 조건은 [3 · 5] 에 미룸 |

**누적 ≈20.0 → ≈20.0 (새 칸 0).** Q1 · Q3 · Q4 · Q8 에 층 하나씩(도구 칸 — ASSB 칸 이동 근거 아님).

---

# 어휘 집계 — 텍스트 층 · NFKC(합자 256 복원) · 줄 끝 하이픈 복원 · 꼬리말("Journal of The Electrochemical Society, 2022 169 080504" · 판권 · TDM 문구) · p. 1 표지 제외 · 본문(초록 → 부록 · 캡션 · 표 포함) | 참고문헌

| 낱말 | 본문 | 참고문헌 |
|---|---|---|
| `identifiab*`(`nonidentifiab*`) · `identif*` · `uniqu*` · `uncertain*` | **19**(4) · 46 · 4 · **0** | 0 · 1 · 0 · 0 |
| `Fisher` · `Bayes*` · `likelihood` · `covarian*` · `Hessian` · `Jacobian` · "condition number" · `bootstrap` · `posterior` · `profile` | **0** · 0 · 1(수사 "improve the likelihood") · 0 · 0 · 0 · 0 · 0 · 0 · 0 | 0 |
| `sensitiv*`(`insensitiv*`) · `correlat*` · `redundan*` · `degenera*` · `ill-posed` · `regulariz*` | 15(6) · 2 · 1 · **0** · 1 · 3 | 0 |
| `noise` · `error*` · `accura*` · `true`/`truth` · `simulat*` · `synthetic` · `consisten*` · `confiden*` · `reliab*` | 10 · 7 · 14 · 19 · 34 · 7 · 2 · 3 · 2 | 0 · 0 · 0 · 1 · 1 · 0 · 0 · 0 · 0 |
| `local minim*` · `global` · `initial*` · `bound*` · `constrain*` · `validat*` · `verif*` | 2 · 2 · 37 · 17 · 8 · 9 · 2 | 0 |
| `teardown` · `nondestructive`/`nonteardown` | 10 · 4 | 0 · 1 |
| `degrad*` · `ag(e)ing` · `fade` · `loss` · `LLI` · `LAM` · `capacit*` | 2(최적화 "degradation in the quality" 1 · "degradation mechanisms" 1) · 1("premature aging") · 0 · 1(DRT "loss process") · **0** · **0** · 16 | 0 |
| `SOC`(대문자) · `temperature` · `°C` · `hysteres*` · `drift` | 55 · 9 · 6 · 1 · 4 | 0 |
| `DRT` · `GDRT` · `Nyquist` · `Kramers`/`K–K` · `inductan*` · `EIS` · `MSMR` · `LPM` · `DFN(e)` · `P2D` | 54 · 26 · 28 · 5 · 27 · 62 · 19 · 27 · 24 · 4 | 0 · 0 · 0 · 0 · 0 · 4 · 0 · 0 · 0 · 0 |
| `contact*` · `pressure` · "solid electrolyte"/all-solid/solid-state · "reference electrode" · `three-electrode` · `half-cell` | 1(R_c) · **0** · **0** · 0 · 0 · 1(Duan 인용) | 0 |
| `graphite` · `NMC` · `Panasonic` · `MATLAB` · `particleswarm` · `fmincon` · `PyBaMM` · `COMSOL` | 17 · 15 · 15 · 5 · 2 · 2 · 0 · 0 | 1 · 1 · 0 · 0 · 0 · 0 · 0 · 0 |
| `supplement*` · "supporting information" · `appendix` · "data availab*" · `github`/`zenodo` · `video`/`movie` | 0 · 0 · 11(본문 부록) · 0 · 0 · 0 | 0 |

⚠ 텍스트 층 한계: ① 식 · 표의 기호(θ · ψ̄ · κ̄ 등)는 조각으로 흩어져 낱말 패턴만 셌다 ② 그림 19 개가 래스터라 그림 안 글자(범례 · 축 이름 — 'True parameter' · 'initial value' · 'Peak isolation' 등)는 셈에 없다 ③ `SOC` 는 대소문자 구별(대소문자 무시면 참고문헌 "Soc." 가 걸림) ④ NFKC 전에는 합자(`ﬁ`) 때문에 `identifiab*` 0 · `insensitiv*` 0 이 된다 — 이 표는 NFKC 뒤 값.

---

# 재현 (`[재현]` — 인쇄 수치 · 식 · 그림 화소로 우리가 계산 · 가정 · 외부 값 표시)

| # | 무엇 | 결과 | 판정 |
|---|---|---|---|
| R1 | 집약 매개변수 셈 | 2 + 2 + 2 + 2 + 3 + 1 + 1 = 13 · k̄0 11(실셀 6 + 5 · 가상 셀 7 + 4) | ✅ 초록 13 · ❌ 그림 11 캡션 '14' · 본문 "six … four" |
| R2 | Q → 용량 | 0.9328 mol × F/3600 = **25.00 Ah**(Panasonic '25Ah' ✅) · 가상 셀 0.81639 → 21.88 Ah | ✅ |
| R3 | 진폭 | C/50 = 25/50 = 0.5 A | ✅ "≈0.5A" |
| R4 | 부록 초기값 · 경계 식 | κ̄D,0 −4.391×10⁻⁴ · 범위 −1.551×10⁻³ … −8.617×10⁻⁵ · ψ̄0 4.180×10⁻⁷ · 범위 2.663×10⁻⁸ … 6.657×10⁻⁷ · n̄e/Q 1/175 … 3/14 · 2⁻³·⁵ 0.0884 | ✅ 인쇄값 전부 |
| R5 | 초기 X ↔ 초기화 식 | κ̄D/ψ̄ 2.13 ↔ X 2.12 · n̄e/ψ̄ 0.232 · 0.359 · 0.280 ↔ X ≈0.22 · 0.36 · 0.27 `[도표·화소]` | ✅ |
| R6 | D̄s,ref 초기 X ↔ 경계 | 초기 0.331 · **0.141** × 참 → 양극 참 = 초기 ×7.1(경계 ×5 밖) · 그래도 1.0 수렴 | ❌ D |
| R7 | 표 IX → 그림 18 '참' R̄ct | MSMR + k̄0 + α 0.5: 음극 0.68–1.01(θ 0.12–0.9) · 양극 1.79–2.98 mΩ ↔ 그림 ±3 %(θ 0.07 첫 점 1.80 ↔ ≈1.55) | ✅ |
| R8 | 그림 6(a) 봉우리 τ | (R̄ct + R̄dl)C̄dl @80 % SOC = **8.84 · 39.8 ms** ↔ `[도표·화소]` 8.7 · 39 ms(R̄ct·C̄dl 만이면 3.8 · 29.8) | ✅ |
| R9 | 그림 6(b) 호 폭 | R̄ct − R̄ctR̄dl/(R̄ct + R̄dl) = **0.334 · 2.232 mΩ** ↔ ≈0.35 · 2.22 | ✅ |
| R10 | 그림 3(b)(d) 혹 위치 | R̄f + R̄ct∥R̄dl = **1.434 · 0.750 mΩ** · R̄f + R̄ct = 1.768 · 2.982 ↔ ≈1.43 · 0.75 · ≈1.78 | ✅ — R̄f^n 직렬 |
| R11 | 갤러리 6 · 7 의 몫 | 참 k̄0 로 ṅ0 몫 ≤1.5×10⁻⁵ · ≈0(θ 0.03–0.89) · 표 X 근사면 갤러리 6 이 한 θ 에서 16 % | 구조적 비관측 |
| R12 | k̄0 경계 ↔ 참값 | 표 X 근사/참 12,867 · 4,107 · 경계 ×1/10 → 참이 하한의 1/1,287 · 1/411 | ❌ 도달 불가 |
| R13 | 표 X 비 | 0.925 · 0.908 · 0.343 · 1.087 · 1.076 · 12,867 · 4,107 · 0.745 · 1.027 · 1.000 · 0.984 | — |
| R14 | 표 VI ↔ 부록 범위 | n̄e^n ×5.09 위 · K_n̄e 2.000 · n̄e^s/n̄e^p 13.67 · κ̄D ×1/5,904 · κ̄^p/κ̄^s 0.0718 · R̄dl^n ×10⁻⁴ · n_dl^p 하한 | ❌ §(c) 2 |
| R15 | ψ̄ 로 화해 가능? | n̄e^n 은 ψ̄ ≤7.20×10⁻⁸ · κ̄D 는 ψ̄ ≥2.16×10⁻³ 요구 — ×3.0×10⁴ | ❌ |
| R16 | κ̄D/ψ̄ 자릿수 | 표 VI −0.0399 · 그림 17(f) 19 점 −0.0305 … −0.362(평균 −0.0965 = 점선) · 가상 셀 −492 · 인쇄 범위 비 −5.8×10⁴ … −129 | ❌ 3–4 자릿수 |
| R17 | 직렬 저항 교환 | R_c +0.64 mΩ ↔ 1/κ̄^s 참 0.174 · 변화 +0.024 mΩ ↔ R̄f^n −≈0.6 mΩ(판독 ±0.3) · 합 1.84–2.24 ↔ 참 2.0 | `[해석]` |
| R18 | (n̄e, ψ̄, κ̄D) 척도 | 부록 계수 구조로 셀 임피던스 불변 `[재현·대수]` | ✅ 저자 명제 |
| R19 | 실셀 R̄ct(θ) 재풀이 | 표 V + 표 VI k̄0 + **α 0.5 가정** → 양극 0.27–0.61 mΩ(θ 0.4–0.9) · 음극 0.001–0.06 mΩ ↔ 그림 15(f) DRT 0.02–0.13 · 0.105–0.14 | ❌ 닫히지 않음 — α 미인쇄(G2) |
| R20 | 주파수 · 측정 시간 | 142 점 · 한 주기씩 합 14,905 s = 4.1 h(+ 휴지 ≥6 h → "about a day") · 19 SOC ≈19 일 | `[재현·가정]` |
| R21 | τ_max | 1/(2π·0.1 mHz) = 1,592 s ↔ 그림 6(a) 극대 2.6×10³ · 9.4×10³ s · 그림 15(d) ≈10⁴ s | 창 밖(격자 미인쇄 — 조건부) |
| R22 | 표 II 오차 | −1.0 · 0 · 0 · +5.0 · +5.1 · +2.0 · +1.6 % | ✅ GDRT 시험 |
| R23 | 잡음 크기 | ε 0.5 % × η(σ 0.2 면 0.1 % · 분산 0.2 면 0.22 %) | 표기 모순(D) |
| R24 | Rabissi 인용 | 12/28 = 42.9 % ↔ "40%" | 내림 |
| R25 | 그림 17(f) SOC 위치 | 19 점 6.4 · 12.6 · 17.7 · 20.6 · … · 94.6 · 100 % | 5 % 격자 아님(D) |
| R26 | 그림 15(e) 평균선 | 양극 77.7 F(보이는 16 점 평균 66.4) · 음극 ≈4.0 F ↔ 표 VI 5.38 · 10 F | ×0.069 · ×2.5 |
| R27 | 일정 | 44 · 22 일 · PDF 생성 출판 전날 | 계산값 |
| R28 | X 합 | 표 V 흑연 1.00001 · NMC 0.99999 · 표 IX 1.0000 · 1.0000 | ✅ |

---

# 참고문헌 87 번호 — 우리 축에 닿는 것 (번호는 PDF p. 28–29 목록에서 직접 확인 · 빠진 번호 0 · [49] = [52] 중복)

| [#] | 서지 `[인쇄]` | 이 편의 쓰임 | 우리 축 |
|---|---|---|---|
| [2] | G.L. Plett, M.S. Trimboli, "Process for lumping parameters to enable nondestructive parameter estimation for lithium-ion physics-based models." *Proc. of EVS-35*, Oslo, Norway, June 2022 | 연재 (i) — LPM 집약 절차의 "most comprehensive description" · "**all parameters of the PDE version of the LPM are identifiable**" 의 유일한 근거 | **Q4 — 구조적 식별성 주장의 원전**(학회 판) |
| [3] | D. Lu, M.S. Trimboli, G. Fan, R. Zhang, G.L. Plett, *J. Electrochem. Soc.* **168**, 070532 (2021)(제목 인쇄 0) | 연재 (ii) — "Five teardown-based approaches to estimating OCP in a … MSMR model format" · 실셀 음극 OCP 출처(표 V) | Q8 · OCP 측정 층위 |
| [4] | D. Lu, M.S. Trimboli, G. Fan, R. Zhang, G.L. Plett, *J. Electrochem. Soc.* **168**, 070533 (2021)(제목 인쇄 0) | 연재 (iii) — OCV 함수 다섯 방법 · "correlate electrode OCP functions with the OCV estimate to find estimates of the electrode operating boundaries" · 해체 없는 OCP 추정 | **모드 좌표(창 · Q) — 우리 α·β 창 맞춤의 액체 판** |
| [5] | D. Lu, M.S. Trimboli, G.L. Plett, "Cell Discharge Testing to Calibrate a Positive-Electrode Open-Circuit-Potential Model for Lithium-Ion Cells." *J. Electrochem. Soc.* **169**, 070524 (2022) | 연재 (iv) — 방전 시험으로 양극 OCP · 창 보정 · D̄s,ref 초기값 · 실셀 NMC OCP 출처 · p. 9 "D̄s^n ≈1×10⁻⁴ · D̄s^p ≈7×10⁻⁵ s⁻¹" | Q8 · [[halfcell-ocp-shape-invariance]](셀 안 OCP 형상 재보정) |
| [6] | D. Lu, M.S. Trimboli, G. Fan, R. Zhang, G.L. Plett, *J. Electrochem. Soc.* **168**, 080533 (2021)(제목 인쇄 0) | 연재 (v) — 초단 펄스 → 순간 저항 → 전도 아홉 + 계면 동역학 · R̄dl 의 정당화 · 전체 집합 시험의 시작값(그 편 표 II) · 그림 16 비교 대상(그 편 그림 17) | Q4(비선형 채널) |
| [7] | B. Guest, M.S. Trimboli, G.L. Plett, *J. Electrochem. Soc.* **167**, 160546 (2020)(제목 인쇄 0) | 연재 (vii) — PSS 모형 → ψ̄(가상 셀 오차 ≈40 %) → 표 VI n̄e · κ̄D | Q4 · 전해질 묶음 |
| [8] · [9] · [10] | R. Jobman, M.S. Trimboli, G.L. Plett, *J. Energy Chall. Mech.* **2**, 45 (2015) · R.R. Jobman 학위논문(UCCS 2016) · Z. Chu, G.L. Plett, M.S. Trimboli, M. Ouyang, *J. Energy Storage* **25**, 100828 (2019) | LPM 의 앞선 판들 · **[10] = 이 편이 쓴 TF 의 출처**("we adopt the TFs from Chu et al., rewritten to accommodate the changes … to the interface model") · 집약 전도도 정의[10, 66] | Q4 · 95호 [25] · [31] 과 같은 편 |
| [66] | Z. Chu, R. Jobman, A. Rodríguez, G.L. Plett, M.S. Trimboli, X. Feng, M. Ouyang, *J. Energy Storage* **27**, 101101 (2020) | 그림 1 회로 "analogous to Fig. 1 from Ref. 66" · 집약 전도도 정의 | Q4 · Q5(액체 기준극) · 95호 [22] |
| [59]–[64] | Smith · Rahn · Wang 2007 *Energy Convers. Manag.* 48, 2565 · Lee · Chemistruck · Plett 2012 *JPS* 220, 430 · Lee 학위논문 2012 · Rodríguez · Plett · Trimboli 2018 *J. Energy Storage* 20, 560 · Rodríguez 학위논문 2017 · Kong · Plett · Trimboli · Zhang · Zheng 2020 *JES* 167, 013539 | DFN 전달함수 계보 — 근사 → 정확 → EIS 조건 시간 영역 검증 | 도구 |
| [27] | J. Illig, M. Ender, T. Chrobak, J.P. Schmidt, D. Klotz, E. Ivers-Tiffée, *J. Electrochem. Soc.* **159**, A952 (2012) = **51호** | 그림 2 "inspired by" · DRT 문헌 목록 · Warburg[26, 27] · "the area under the peak … corresponds to the polarization of the loss process27" | **흡수됨 — 인용 대조 §2** |
| [41] · [42] · [43] | C. Rabissi, A. Innocenti, G. Sordi, A. Casalegno, *Energy Technol.* **9**, 2000986 (2021) · Q. Zhang 외, *J. Energy Storage* **50**, 104182 (2022) · X. Duan, F. Liu, E. Agar, J. Xinfang, *J. Electrochem. Soc.* **169**, 040561 (2022) | EIS 매개변수 추정 문헌 셋 — Rabissi "12 out of 28 … low sensitivity or are insensitive" · Zhang = Strategy 2 출처 · Duan "consistent parameter estimates" | **Q4 — EIS 감도 · 식별** |
| [28] · [29] | M.D. Murbach, V.W. Hu, D.T. Schwartz, *JES* **165**, A2758 (2018) · M.D. Murbach, D.T. Schwartz, *JES* **165**, A297 (2018) | 비선형 EIS(고조파) — "holds promise … may help estimate more PBM parameter values" | Q4 — 선형 비식별을 푸는 비선형 채널 후보 |
| [68] · [72] · [74] · [69] · [71] · [73] · [70] | F. Ciucci, C. Chen, *Electrochim. Acta* **167**, 439 (2015) · M. Saccoccio 외 *EA* **147**, 470 (2014) · T.H. Wan, M. Saccoccio, C. Chen, F. Ciucci, *EA* **184**, 483 (2015) · M.A. Danzer, *Batteries* **5**, 53 (2019) · M. Hahn 외 *Batteries* **5**, 43 (2019) · P. Shafiei Sabet 외 *JPS* **406**, 185 (2018) · M.B. Effat, F. Ciucci *EA* **247**, 1117 (2017) | DRT · GDRT 알고리즘("Wan et al.68,74" — [68] 은 Ciucci & Chen) · GDRT 틀 = Danzer | **DRT 체크리스트 C1 · C3** |
| [30] · [31] · [32]–[34] | J. Illig 학위논문(KIT 2014) · D. Klotz 학위논문(KIT 2012) · Boukamp 1995 *JES* 142, 1885 · Bohren 2010 *Eur. J. Phys.* 31, 573 · M. Schönleber, D. Klotz, E. Ivers-Tiffée, *EA* **131**, 20 (2014) | EIS 자료 유효 기준 · K–K | C2 |
| [76] | M. Oldenburger, B. Bedürftig, E. Richter, R. Findeisen, A. Hintennach, A. Gruhle, *J. Energy Storage* **26**, 101000 (2019) | "Unmodeled hysteresis will also contaminate EIS measurements, especially at low frequencies" | (베) · 측정 상태 |
| [14] · [1] | N. Meddings 외 *JPS* **480**, 228742 (2020) · L. Oca 외 *EA* **382**, 138287 (2021) | 상용 셀 EIS 측정 · 해석 개관 · 해체 매개변수화 개관 | (헤) · 측정 쪽 |
| [37]–[40] · [38] | 혼성 EIS(Wildfeuer 2019 · **Waag · Käbitz · Sauer 2013 *Applied Energy* 102, 885** · Maheshwari 2018 · Schmitt · Maheshwari · Heck · Lux · Vetter 2017 *JPS* 353, 183) | 저임피던스 셀 혼성 측정 목록 | 원장 행 있음(Waag — 목록 인용) |
| [47] · [48]–[57] · [58] · [65] | Meyers · Doyle · Darling · Newman 2000 *JES* 147, 2930 · Baker & Verbrugge 2012 *JES* 159, A1341 · Verbrugge 계열 MSMR([50] Verbrugge & Koch 2003 *JES* 150, A374 등 · [49] = [52] 중복) · Jorcin 2006 CPE · Jacobsen & West 1995 | 이중층 모형 · MSMR · Darken · CPE · 확산 TF | Q8(OCP 형상 모형) · 도구 |
| [83]–[87] | Doyle 1996 · Sakti 2013 · von Lüders 2019 · Keil & Jossen 2020 *JES* 167, 110535 · **Schmalstieg · Rahe · Ecker · Sauer 2018 *JES* 165, A3799** | 전도도 값 · **아인슈타인 관계 인용처[87]** | 원장 행 있음(Schmalstieg — 인용처만) |
| [11]–[26] · [35] · [36] · [44]–[46] · [67] · [75] · [77]–[82] | EIS 교재 · TLM · Bisquert · de Levie · Gamry 응용 노트 · DFN 원전 · 근사 이론 · 케이블 인덕턴스(Kasper 2022) · ROM · 팩 · 상태 추정 응용 | 배경 · 응용 | — |

---

# 인용 대조

## 1. 이 편을 인용한 우리 digest — 그 쓰임

| 호 | 자리 | 그 digest 가 매단 것 | 원문 대조 |
|---|---|---|---|
| **27호** Sinzig 2024 *JES* 171, 120519 | [28] · 후속 표 :376 ★★★★ · 본문 "to fit the parameters" 문장의 둘째 인용 | "Plett 계보의 **집약(lumped) 파라미터 추정**, 곱 쌍을 처음부터 묶어 추정하는 쪽" — `[추론]` 제목 미인쇄 | ✅ **집약 · 곱 쌍 묶음은 맞다** — LPM 이 27호 곱 쌍 셋을 처음부터 묶는다: ① κ·ε/τ → κ̄^r(= κ εe^brug A/L — 부록 비 식) ② D·r² → D̄s,ref(s⁻¹ — 입자 크기 흡수) ③ i₀·A → k̄0,j(mol s⁻¹ — 전극 전체) + C̄dl(같은 면적) · ⚠ "추정" 의 식별성은 부분적 — 소신호 EIS 에서 n̄e/ψ̄ · κ̄D/ψ̄ 비만 · R_c ↔ 1/κ̄^s · 같은 모형 합성에서 19–64 % · 27호 `[추론]` 해소 |

**지목 수 확인**: 지목은 각 digest 의 후속 절만 센다 — 27호 후속 표(:376) 하나 **= 1 — 원장 "27 \| 1" 과 일치(정정 없음)**. 카드 :5094 는 27호 흡수 기록(같은 지목의 전사 — "2순위") · 92 · 94 · 95호의 "4차 묶음 13 편과의 관계" 문장과 95호 Jobman 행의 "Lu 2022 의 앞" 은 교차 기록(지목 아님) · §3-b (다) "닿는 논문" 은 결정 목록. **등급**: 27호 ★★★★ ↔ 원장 ★★★(원장이 내렸거나 다르게 매김 — 표시만).

## 2. 이 편이 인용한 우리 digest — 쓰임 대조 (digest 전사 · 원 논문은 이 세션에서 다시 열지 않음)

| 이 편 [#] | 우리 digest | 이 편의 쓰임 | 대조 |
|---|---|---|---|
| [27] | **51호** Illig 2012 *JES* 159, A952 | ① 그림 2 "inspired by the work reported by Illig et al." ② DRT 문헌 목록 "27,67–74" ③ "the area under the peak … corresponds to the polarization of the loss process27" ④ Warburg[26, 27] | ✅ ①–③ 은 51호의 DRT 사용(봉우리 셋 P1 · P2 · P3 · 면적 = 저항)과 맞다(51호 digest 전사). ★ **그러나 51호가 봉우리를 전극에 붙인 방법은 대칭셀(LFP\|LFP · Li\|Li) 대조라는 측정이었고**(51호 판정 표 "전극 배정 — 측정(대조)" · 저자가 재현성 한계를 인쇄), **이 편은 그 방법을 쓰지 않고 τ 순서 가정으로 대신했다** — 같은 원전을 그림으로는 빌리고 배정 연산자는 빌리지 않았다. 51호도 λ 미인쇄(51호 G2) — 같은 공백을 물려받음 |

**교차 참조(이 편이 인용하지 않음 · 같은 축)**: **28호** Bizeray 2019(선형화 SPM · EIS 전달함수 식별성 — 이 편 "nonlinearly ↔ linearly identifiable" 의 SPM 판 · 식 50 "infinite number of pairs" · 모드 축을 입력으로 — 이 편과 같은 쪽 끝) · **95호** Khalik 2021(DFN 묶음 · 직교화 순위 · 합성 다중 시작 — 모드 좌표를 식별 집합에 넣은 반대쪽 끝 · Plett 계보 [22] · [25] · [31] = 이 편 [66] · [8] · [10] 을 공유) · **10호** Vadhva 2021(EIS 방법론 · DRT ill-posed) · **11호** Yu 2024(DRT 를 실제로 돌린 첫 ASSB 편 — Danzer 2019 를 ★★★ 로 지목 · Wan 2015 1 순위) · **16 · 18 · 19 · 84 · 90호**(DRT 경보 셋째–일곱째 — 전극 배정 · λ · 창 밖 봉우리 · 자동 λ) · **세미나 3번째** sun2025(같은 EIS 에서 학습형으로 모드 라벨 — §(d) 4) · **[[zhang2020-eis-aging-dataset]]**(EIS + ML 의 같은 비식별). 4차 묶음: **13 편 인용 0**(파일 55 Khalik 2021 과는 같은 시기 · 같은 Plett 문헌 셋을 공유 · 서로 인용 0).

---

# 곱 축퇴 처방 — 일흔아홉 번째 적용 ([[assb-lampe-contact-product-degeneracy]])

**적용 불가(액체 · 접촉 0 · 노화 0) — 대신 처방 1단계("R · C 를 같이")를 집약 모형의 전극별 두 매개변수(C̄dl · k̄0)로 이미 하는 구성을 준다 — 전극 배정이 가정이라는 단서와 함께.**

| 처방 단계 | 필요한 입력 | 96호 | 판정 |
|---|---|---|---|
| 1단계(16 · 23호) | `R` · `C` 같이 | **전극별 C̄dl^r · R̄ct^r(k̄0,j^r) · R̄dl^r · R̄f^r 를 한 TF 모형에서 같이** — 19 SOC · 완전지 2전극 · 단 배정 = τ 순서 가정 · C̄dl = CPE 계수(n 0.90–0.92) · 노화 축 0 | ⚠ **구성만** |
| 2단계(18 · 25호) | 면적을 아는 대조군 | 0 — `[인쇄]` "To compute the scaling factors, we require knowledge of cell internal dimensions which can be found via teardown" | ❌ |
| 3단계-a · b(19호) | `Ea` · `C` 상한 | 25 °C 하나 · `C` 값은 있으나 상한 검사 0 | ❌ |
| 4단계(20 · 24호) | 시간 영역 · 같은 시편 | 같은 셀의 펄스[6] · 방전[5 · 7] 이 연재에 있으나 이 편 안 EIS ↔ 시간 영역 교차 0 | ⚠ 연재 단위로만 |
| 율 스윕 · `J^T J` | — | 펄스 시험의 SOC · 율 의존 순간 저항(연재 [6] · 그림 16) — "nonlinearly identifiable" 명제 · J^T J 0 | ⚠ 명제만 |

**곱 문장**(`[인쇄]` → `[해석]`):
- ① `[인쇄]` 그림 1 "R̄ct = RT/(F²ṅ̄0) = RT/(F²Σṅ̄0,j)" — R̄ct 가 전극 전체 교환율의 역수라 **k₀ · A_eff 곱이 k̄0,j 하나로 묶여 있다**(27호 ③ 의 집약판).
- ② `[인쇄]` 식 [1] 우변 인자 "a_sALC_dl" — 이중층 용량도 **같은 활성 계면 총면적**을 곱으로 가진다 ⇒ `[해석·대수]` **k̄0/C̄dl 는 면적에 불변**(k₀/C_dl) · A_eff 손실은 둘을 같은 비율로 · 순수 k₀ 손실은 k̄0 만 · 계면층 성장은 R̄f(또는 k̄0) 만 — 처방 1단계의 집약 모형판. 면적의 **절대값**은 C_dl(면적당)을 모르므로 안 나오고, 노화 축에서 **변화비** C̄dl(N)/C̄dl(0) = A_eff(N)/A_eff(0) 만 나온다(면적당 C_dl 불변 가정 위).
- ③ `[인쇄]` "the impact of R_c and 1/κ̄^s on the full-cell impedance are identical" — 옴 직렬의 **합 축퇴** · `[해석]` R̄f^n 도 같은 골짜기(§(b) 4 — R_c +0.64 ↔ R̄f^n −≈0.6 mΩ).

**⚠ 이것이 곱을 푼 것은 아니다** — ① 이 편에 노화 축이 없어 변화비를 잰 적이 없다 ② 두 계면의 전극 이름이 τ 순서 가정이고 실셀 최종 C̄dl 은 DRT 초기값과 크기 순서가 뒤집혔다(×0.069 · ×2.5) — 전극을 잘못 붙이면 면적 손실이 다른 전극에 배정된다 ③ CPE(n < 1)에서 C̄dl 은 F·s^(n−1) 계수라 면적 비례가 n 과 섞인다. 후보 메모(처방 표로 올리지 않음 · 결정 대기): **"집약 모형 EIS 의 전극별 (C̄dl, k̄0) 쌍은 면적 손실이면 같은 비율로 · k₀ 손실이면 k̄0 만 움직인다 — 처방 1단계의 집약 모형판. 조건: 전극 배정을 측정으로(대칭셀 · 3전극 — 51 · 16 · 18호) · n_dl 고정 또는 함께 보고 · 노화 축 반복 · 같은 SOC."** 처방 표 새 줄 0.

---

# 보류 결정 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(야) — 이 편이 주는 근거 (결정 안 함)

| # | 결정 (요약) | 96호 근거 | 세기 |
|---|---|---|---|
| **(다)** | 28호 Bizeray(액체셀 도구)를 ASSB Q4 분모에 넣을지 | **이 편이 (다) 의 "닿는 논문" 목록에 직접 있다**(Lu 2022) — 셋째 액체 식별성 도구 편: 구조적(인용 Ref. 2 — 지면 0) + 선형(손 분석 — 비 둘 · 직렬 R_c ↔ 1/κ̄^s) + 실제적(같은 모형 합성 하나 — 전체 집합 다섯 19–64 % · k̄0,6/7 참값 경계 밖) · 28호처럼 **모드 좌표(Q · 창)를 입력으로 뺐다** — 액체셀 도구 칸이 세 편이 되고, 모드 좌표를 식별 집합에 넣은 편은 그중 95호 하나 | **강** |
| **(샤)** | 다중 시작 · 합성 참값 시험의 '일관성 ↔ 정확성' 표기 | 이 편은 다중 시작조차 없다 — **실행 하나 · 잡음 실현 하나 · 참값 하나** · 참값이 **경계 위**(n_f = n_dl = 1 · 경계 0.9–1) · **경계 밖**(k̄0,6/7 하한의 1/1,287 · 1/411 · D̄s,ref^p 초기 ×7.1 > ×5) · **초기값 = 참값**(R_c 1.0)에서 출발해 1.64 · 출력 잔차 ≲0.04 mΩ ↔ 매개변수 19–66 % | **강** |
| **(뱌)** | 재매개화 · 묶음의 최소성 표기 | LPM 집약은 "identifiable"(Ref. 2 인용)이라 쓰나 **소신호에서 최소가 아니다** — n̄e · ψ̄ · κ̄D 셋이 비 둘로만(`[재현·대수]` 부록 계수 구조로 척도 불변 확인) · R_c ↔ 1/κ̄^s · `[해석]` R̄f^n — 95호(DFN 24 안 척도 대칭 하나)와 같은 꼴의 Plett 계보판 | **강** |
| **(세)** | 인쇄 매개변수 표의 재풀이 폐합 검사 | 가상 셀 ✅(표 IX → 그림 18 '참' R̄ct ±3 % · (R̄ct + R̄dl)C̄dl → 그림 6 봉우리 τ · 호 폭 · 그림 3 혹 위치) · **실셀 ❌**(표 VI 이 같은 편 부록 범위 넷 밖 · 둘 경계 위 · 어떤 ψ̄ 로도 n̄e^n · κ̄D 가 함께 안 맞음 ×3×10⁴ · α 미인쇄로 R̄ct(θ) 재풀이 불가) | **강** |
| (피) | DRT 창 밖 봉우리 표기 | 그림 6(a) 가상 셀 극대 2.6×10³ · 9.4×10³ s · 그림 15(d) 실셀 ≈10⁴ s — 표 III 격자면 τ_max ≈1.6×10³ s 밖(격자 미인쇄 — 조건부) · 이름 0("electrolyte and solid-diffusion" 묶음) · 실셀 C(≈3×10⁻² s)에는 '고체 확산' 이름 | 중 |
| (베) | 시간분해 EIS 의 측정 상태 표기 | SOC 당 ≈하루 측정 · `[인쇄]` "the cell has slight SOC-drift during the frequency-response measurement (especially at low frequencies)" · SOC <10 % 혼성 모드 · "Unmodeled hysteresis will also contaminate EIS"[76] · 휴지 ≥6 h · 표류 크기 인쇄 0 · 실제 SOC 가 5 % 격자 밖(그림 17(f)) | 중 |
| (테) | 'system identification' 편의 식별 산출물 표기 | 식별값은 인쇄(표 VI — 3 유효숫자) · 불확실도 0 · 경계 인쇄됐으나 결과가 밖 · Strategy 1 ↔ 2 κ̄D/ψ̄ ×2.4 · SOC 별 ×12 · 학습(맞춤) ↔ 검증 구분 0 | 중 |
| (이) | 모형 값 인용 규칙 | 표 VI 의 n̄e^n(>Q) · κ̄D(물리 범위 ×1/5,900) 를 물리 매개변수로 옮기지 않게 — 물리 단위 환산(스케일 인자)도 해체가 필요(G1) | 중 |
| (치) | 모형 결론 옆 "배제 가정" 표기 | "highly accurate" · "very good accuracies" · "consistent" 의 조건: 가상 셀 하나 · 같은 모형 · 잡음 0.5 % 하나 · 실행 하나 · 부분 집합(펄스 참값 고정)에서만 · 25 °C · 실셀 하나 · 시간 영역 0 | 중 |
| (헤) | 측정 입력의 역모형 층위 (measure-don't-fit 판) | 93호와 반대 처방(해체 없이 적합으로)의 표본 — 그런데 실셀 음극 OCP 는 (ii) 단계의 "**Five teardown-based approaches**"(Ref. 3) 출처이고 물리 단위 환산은 해체가 필요하다고 저자가 쓴다 — '비파괴' 의 범위는 EIS 단계와 연재 목표 · 입력 하나는 해체 기반 | 중 |
| (체) | 평형 (OCV) 곡선의 출처 층위 표기 | MSMR OCP(표 V) — 흑연 = [3](teardown-based) · NMC = [5] 방전 시험 셀 안 재보정(첫 판 "not well calibrated" 버림) · 측정 조건은 [3 · 5] 에만 · 가상 셀 MSMR(표 IX)은 출처 0 | 중 |
| (야) | '한쪽 곡선 빌림 · EMF 정의형' 창 무정보 · 배분 오차 표기 | 연재 (iv)[5] 가 흑연 OCP(고정)를 두고 NMC OCP 와 창을 셀 방전으로 보정 — 95호 경우 1(한 전극 빌림 · 다른 전극 정의)에 가까운 구성(`[인쇄]` 서술만 — 원 논문 미열람) · 빌린 쪽 형상 오차가 보정되는 쪽으로 가는 경로가 있다 | 중 |
| (무) | `j₀(x)` 모양 선택지 | MSMR 갤러리별 ṅ0,j = k̄0,j x^(ωα)(X − x)^(ω(1−α)) θe^(1−α)(식 7) — 갤러리 11 개 · 표 VI k̄0 가 12 자릿수에 걸침 · ω 큰 갤러리는 몫 ≈0(구조적 비관측 `[재현]`) — PyBaMM √ 꼴과 다른 구조화된 j₀(x) 선택지의 실례 | 중 |
| (루) | SOC 축 신품 `j₀(x)` 기준선 | 가상 셀 R̄ct^n ×2.3(0.68–1.55 mΩ) · R̄ct^p ×1.7(1.78–2.98) · 실셀 DRT 추정 양극 ×6(0.02–0.13 mΩ) — 신품에서 SOC 만으로 계면 저항이 이만큼 움직인다 | 중 |
| (에) | 속도 상수의 i₀ 환산 표기 | k̄0,j(mol s⁻¹ · 면적 포함 집약) → i₀(A m⁻²) 환산은 a_s A L(해체)이 필요 — 이 편은 환산 0 · 실셀 α 미인쇄 | 중 |
| (차) | PyBaMM 면적 / `j₀` 노브 분리 forward | 집약 모형에서 면적은 C̄dl · k̄0 두 곳에 같이 들어간다 — 면적 노브를 따로 둔 forward 가 만들 서명(둘의 같은 비율 이동)을 이 편 구조가 보여 준다 · 관측으로 가르려면 C 를 같이 재야 함 | 중 |
| (가) | 29호 Q4 +0.5 (정적 ↔ 동적 축) | 액체 표본 — 관측 채널마다 식별 집합이 다르다: 정적(OCV) → 창 · 소신호(EIS) → 비 · 비선형(펄스) → 개별 값("nonlinearly identifiable") · `[인쇄]` "a pulse test is always recommended in order to expose and understand cell nonlinearities" | 약 |
| (페) | '입력 설계' 의 목적 표기 | 진폭 C/50 = "minimal overall K–K residuals" · 격자 20/10 ppd = "compromise to tolerate a suitable test time while maintaining proper resolution" — 목적 = 자료 품질 · 시간 · 정보량(FIM) 기준 0 | 약 |
| (메) | 예치 원자료 교차 폐합 | 예치 0 → 지면 폐합으로 대신: ✅ 다섯(표 IX ↔ 그림 18 · 6 · 3 · 초기 X ↔ 부록 식 · Q ↔ 25 Ah) · ❌ 넷(표 VI ↔ 부록 범위 · 그림 11 캡션 14 ↔ 13 · SOC 19 ↔ 20 · 갤러리 수 셋) | 약 |
| (제) | 모형 "일치" 주장의 잔차 표기 | 가상 셀 절대 오차 ≲0.04 mΩ(그림 14) · 실셀 수치 잔차 0(그림 17 눈으로 · "agreement is excellent") | 약 |
| (냐) | 모형 결론의 회고 인용 — 조건 복원 | 초록 "Parameter estimates found in the simulation study are highly accurate, leading us to have confidence in the values estimated for the physical cell as well" — 부분 집합 조건 · 같은 모형 조건이 떨어진 채 실셀 신뢰로 이어짐 | 약 |
| (먀) | 지목 기구 층위 확인 | 27호 기대 "집약 · 곱 쌍을 처음부터 묶어 추정" ✅(곱 쌍 ①–③ 모두 묶임 — 인용 대조 §1) · "추정" 의 식별성은 부분적 | 약 |
| (케) | 비선형도 지표의 측정 조건 표기 | 진폭 C/50 의 선형성 = K–K 잔차로만 · 비선형(고조파) 채널은 "beyond the scope"(Murbach[28, 29]) | 약 |

나머지 — (라)(마)(바)(사) 결정 · 반영됨, 그 밖의 글자는 **근거 0**(ASSB · 접촉 측정 · 압력 · Li-In · 기준극 · 노화 사이클 · 프로토콜 비교 · LLI 실측 · θ 판정 · 상 분율 · 입도 · 부피 변화가 이 편에 없다). **결정 안 함.**

## 새 판단 거리 (셋 — 글자는 호출자가 붙인다)

1. **"식별 가능" 주장의 층 표기 — 구조적(비선형 PDE) ↔ 선형(소신호) ↔ 실제적(잡음 · 합성)** ((뱌) 의 선형화판으로 묶어도 됨) — 편이 "identifiable" 을 쓸 때 카드 Q4 · 개념 · 합성 truth 로 옮기기 전에 ① 그 주장이 어느 층인지 · 증명이 지면에 있는지 인용뿐인지 ② 실제로 쓴 관측(EIS 소신호 · 펄스 · OCV)에서 남는 비 · 합 축퇴(예 n̄e/ψ̄ · κ̄D/ψ̄ · 직렬 저항 합)를 같이 적게 할지 — 96호: "all parameters of the PDE version of the LPM are identifiable"(Ref. 2 학회 판 · 지면 0) ↔ "nonlinearly identifiable but not linearly identifiable" · 비 둘 · R_c ↔ 1/κ̄^s(`[해석]` + R̄f^n) · 28호 식 50 · 95호 척도 대칭과 같은 축.
2. **최종 매개변수 표 ↔ 같은 편이 인쇄한 경계 · 물리 범위의 폐합 검사 + 합성 참값의 경계 위치 표기** ((세) · (샤) 의 실셀 · 경계판으로 묶어도 됨) — 추정 편의 최종값 표를 옮기기 전에 ① 같은 지면의 초기화 · 경계 · 물리 범위 안인지 ② 경계 위에 붙은 값 ③ 공통 인자(ψ̄ 같은)로 묶인 값들이 함께 범위에 들 수 있는지를 검사하고, 합성 시험이면 참값이 경계 위 · 밖인지 · 초기값이 참값인지를 적게 할지 — 96호: 표 VI n̄e^n ×5.1 · κ̄D ×1/5,900 · κ̄^p/κ̄^s · R̄dl^n ×10⁻⁴ 밖 · K_n̄e 2.000 · n_dl^p 0.90 경계 위 · ψ̄ 화해 불가 ×3×10⁴ · 가상 셀 n = 1 경계 위 · k̄0,6/7 경계 밖 · R_c 초기값 = 참값.
3. **DRT 봉우리 → 전극 배정 규칙 표기 (τ 순서 가정 ↔ 측정 배정) + 최종 적합에서 그 배정이 유지됐는지** ((피) · (베) · [[drt-peak-count-nonidentifiability]] 체크리스트와 묶어도 됨) — DRT 로 계면 봉우리를 전극에 붙인 편을 옮길 때 배정 연산자(τ 순서 가정 · 대칭셀 · 3전극 · 온도 · 구성 교체)를 적고, 그 봉우리로 초기값을 정했으면 최종 전극별 C · R 이 초기 순서를 유지했는지 같이 적게 할지 — 96호: `[인쇄]` "we simply assume that the smaller time constant … negative electrode" · 실셀 C̄dl 초기 음극 ≈4.0 · 양극 77.7 F → 최종 10 · 5.38 F(순서 뒤집힘) · 51호는 같은 그림 계보에서 대칭셀로 배정(측정).

---

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** | 초록 "Parameter estimates found in the simulation study are **highly accurate**" · 결론 "able to find **all parameter values of interest with very good accuracies**" ↔ 그림 12 · 13 전체 집합: n̄e^n/ψ̄ 1.20 · n̄e^s/ψ̄ 0.48 · n̄e^p/ψ̄ 1.25 · κ̄D/ψ̄ 1.19 · R_c 1.64 · σ̄^p ≈1.66 · κ̄^p ≈1.44 · κ̄^n ≈1.29 `[도표·화소]` · k̄0,6/7 참값 경계 밖 — 정확도는 부분 집합(펄스 참값 고정)에서만 | p. 2 · 21 ↔ p. 17–18 |
| **D2** | 표 VI 실셀 값이 부록이 인쇄한 초기화 · 경계 · 물리 범위 밖: n̄e^n 1.0166 mol > 3Q/14(0.200) · κ̄D −1.46×10⁻⁸ ↔ −1.55×10⁻³ … −8.62×10⁻⁵ · κ̄^p/κ̄^s 0.072 < 2⁻³·⁵ · R̄dl^n 1.00×10⁻¹⁰ < 10⁻⁶ · K_n̄e = 2.000(상한) · n_dl^p 0.90(하한) · 어떤 ψ̄ 로도 n̄e^n · κ̄D 동시 불가 `[재현]` | p. 22 ↔ p. 25–27 |
| **D3** | 그림 11 캡션 "Convergence trajectories of **14** normalized parameter estimates" ↔ 그려진 궤적 13 · 초록 "thirteen" · p_EIS^lin 13 | p. 16 ↔ p. 2 · 14 |
| **D4** | 갤러리 수 셋: 본문 "If there are **six** galleries in the (graphite) anode and **four** in the (NMC) cathode, there will be **ten** different k̄0,j" ↔ 표 V(실셀) 흑연 6 · **NMC 5** ↔ 표 IX · X · 그림 13(c)(가상 셀) **흑연 7** · NMC 4 ↔ 그림 19(본문은 "for the Panasonic cell … listed in Table V" 로 소개) 흑연 6 · NMC 4 · θ100^p 점선 ≈0.18 ↔ 표 V 0.2263 | p. 26–27 ↔ p. 20 · 25 · 28 |
| **D5** | 표 IV "SOC setpoints, input frequencies are **identical to Table III**"(100 %: −5 %: 5 % = 20 점) ↔ 본문 "In total, **nineteen** distinct SOC setpoints are measured" ↔ 그림 17(f) 19 점 SOC ≈6.4 · 12.6 · 17.7 · 20.6 … 100 %(5 % 격자 아님 `[도표·화소]`) | p. 19 ↔ p. 17 · 21 |
| **D6** | 부록 "These estimates are generally **within a factor of two** or so from the truth, so the bounds … **D̄s,ref,0/5 < D̄s,ref < 5D̄s,ref,0**" ↔ 그림 11–12(a) 초기 X: D̄s,ref^n 0.331 · ^p **0.141**(참 = 초기 ×7.1 — 경계 밖)인데 1.0 으로 수렴 `[도표·화소]` | p. 27 ↔ p. 16–17 |
| **D7** | 잡음: 본문 "η′ and η″ are two independently distributed random variables with **standard normal** distribution and we let both of them equal to **N(0, 0.2) Ω**" · 표 III 같음 — '표준 정규' ↔ 0.2 · 곱셈 인자(식 17 ε\|Z\|(η′ + jη″))에 Ω 단위 | p. 14 · 15 |
| D8 | 초록 "generalized distribution of **realization** times" ↔ 본문 · 제목 줄 전부 "relaxation" | p. 2 |
| D9 | p. 9 "If the cell impedance data can be decoded (**as previously discussed in Fig. 5**)" ↔ 그림 5 는 p. 11(뒤) — 앞에서 다룬 '분해' 는 그림 2 | p. 9 |
| D10 | "the algorithms developed by **Wan et al.68,74**" ↔ [68] = F. Ciucci, C. Chen *EA* 167, 439 | p. 8 ↔ p. 29 |
| D11 | 참고문헌 **[49] = [52]**(M. Verbrugge, D. Baker, X. Xiao, *JES* 163, A262) — 해만 2015 ↔ 2016 | p. 28–29 |
| D12 | p. 9 "In practice, we have found **D̄s^n ≈1×10⁻⁴ s⁻¹ and D̄s^p ≈7×10⁻⁵ s⁻¹** for the physical Panasonic cell" ↔ 표 VI D̄s,ref 2.75×10⁻³ · 1.17×10⁻⁴ · 그림 17(e) SOC 별 D̄s 4.8×10⁻⁴ … 3.6×10⁻² · 8.8×10⁻⁴ … 2.1×10⁻² — D̄s ↔ D̄s,ref 표기 없이 자릿수 차(Darken 인자로 일부 설명 가능 — 단정 안 함) | p. 9 ↔ p. 21–22 |
| D13 | 그림 표기: 6(a) 제목 "80%% SOC" · 8 표지 "f → −∞"(f → 0) · 13(d) 범례 "k̄^n_0,j"(양극 패널) · 18(a) x 축 "θs^p"(음극 패널) | p. 12 · 14 · 18 · 25 |
| D14 | 단위: 표 X "mol **S**⁻¹" ↔ 표 IX "mol s⁻¹" · 표 VI C̄dl "F" 인데 n_dl 0.90–0.92(CPE — F·s^(n−1)) · p. 15 "LMP"(LPM 오타) | p. 22 · 25 · 28 · 15 |
| D15 | 제목 "Nondestructive" · 첫 문장 "without requiring cell teardown" · 결론 "comprehensive nonteardown process to estimate **all** parameters" ↔ (ii) 단계 "Five **teardown-based** approaches to estimating OCP"(Ref. 3) — 실셀 음극 OCP 는 그 편 것 · 물리 단위 환산은 "can be found via teardown" | p. 2–3 · 21 |
| D16 | 그림 15(e) 양극 C̄dl 평균선 77.7 F ↔ 보이는 16 점 평균 66.4 F `[도표·화소]`(축 위 밖 점이 있거나 평균 정의 다름 — 미상) | p. 19 |
| D17 | Rabissi "**40%** of the parameters (12 out of 28)" ↔ 12/28 = 42.9 % `[재현]`(내림 — 경미) | p. 4 |

표시만(어긋남 아님 — 우연 여부 미상): 표 VI k̄0,1^n **1.73×10⁻¹⁰** = 표 X 가상 셀 근사 k̄0,3^n **1.73×10⁻¹⁰**.

---

# 이 편이 우리 프로젝트에 주는 것 (정리)

1. **EIS 를 관측으로 더할 때 무엇이 열리고 무엇이 안 열리는가의 액체 표본.** 모드 좌표(창 · Q)는 OCV 쪽에서 끝나고 EIS 는 그 위에서 계면 · 수송을 읽는다(이 편 · 28호). 열리는 것은 **전극별 C̄dl · k̄0**(면적 채널) — OCV 창 맞춤의 LLI ↔ LAM_PE 축퇴 방향에 직교할 후보이고 카드 곱 축퇴의 처방 1단계 그 자체다. 조건 다섯(전극 배정 · CPE · 산포 ×12 · 19 일 · 식별 폭)이 붙는다(§(d) 3). 우리 쪽 수치(`degradation-degeneracy/` · `mode-observability`)는 RESULTS*.md 가 정본 — 여기 옮기지 않는다.
2. **관측 채널마다 식별 집합이 다르다** — 정적(OCV) → 창 · 소신호(EIS) → 비 n̄e/ψ̄ · κ̄D/ψ̄ · 직렬 합 · 비선형(펄스) → 개별 값("nonlinearly identifiable"). 우리 4-창 + γ_Si 맞춤이 준정적 OCV 채널 하나로 무엇을 정하고 무엇을 못 정하는지 묻는 것과 같은 축의 액체 판이다(28 · 95호와 셋).
3. **합성 참값 시험 설계의 함정 표본** — 참값이 경계 위(n = 1) · 경계 밖(k̄0,6/7 · D̄s,ref^p 초기 ×7.1) · 실행 하나 · 잡음 하나 · 초기값 = 참값(R_c) — NEW_MODEL_REQUIREMENTS §7-1(유일성 측정 요구 — 읽기만)의 ①(`tol` 있는 폭) · ③(경계 접촉) · ⑤(다중 시작) 를 지키지 않으면 무엇이 보이는지의 반례. 그리고 같은 지면이 **폭의 하한을 공짜로 준다**: 출력 ≲0.04 mΩ 에서 매개변수 19–66 % · 실셀 SOC 별 ×12.
4. **실셀 매개변수 표의 자기 폐합 검사 절차** — 같은 편 부록의 경계 · 물리 범위로 최종 표를 검사하는 것만으로 넷이 밖 · 둘이 경계 위라는 것이 드러났다(새 판단 거리 2). 위키가 문헌 값을 합성 truth 입력으로 옮길 때 쓸 수 있는 값싼 검사다.
5. **DRT 전극 배정의 두 연산자** — 51호(대칭셀 측정)와 이 편(τ 순서 가정)이 같은 그림 계보에서 갈린다 · 이 편의 최종 C 가 초기 순서와 뒤집혔다는 것이 가정 배정의 위험을 수치로 보인다([[drt-peak-count-nonidentifiability]] 여덟 번째 경보).

---

# 후속 후보 (원전 우선 — 지목 수는 위키 digest 의 후속 절 grep 으로 센 값)

| 등급 | 서지 (PDF 목록 번호) | 지목 (후속 절) | 왜 | 축 |
|---|---|---|---|---|
| ★★★ | **Lu D., Trimboli M.S., Fan G., Zhang R., Plett G.L. 2021** — *J. Electrochem. Soc.* 168, 070533 ([4] · 제목 인쇄 0) | **96** = 1 (새) | 연재 (iii) — OCV 함수 다섯 방법 · 전극 OCP 를 OCV 에 맞춰 **전극 창(θ0 · θ100)과 Q** 를 정함 · 해체 없는 OCP 추정 — 우리 α·β 창 맞춤(LLI · LAM 좌표)의 액체 판 원전 후보 · 창의 유일성을 무엇으로 보였는지 확인할 곳 · ⚠ 액체셀 도구 | 모드 좌표 · Q4 · Q8 |
| ★★★ | **Plett G.L., Trimboli M.S. 2022** — "Process for lumping parameters to enable nondestructive parameter estimation for lithium-ion physics-based models", *Proc. EVS-35*, Oslo ([2]) | **96** = 1 (새) | 연재 (i) — LPM 집약 절차 · **"all parameters of the PDE version of the LPM are identifiable" 의 유일한 근거**(이 지면엔 증명 0) — 구조적 식별성의 조건(무엇을 입력으로 두는가)을 확인할 곳 · 학회 판 · ⚠ 액체셀 도구 | Q4 |
| ★★★ | **Lu D., Trimboli M.S., Plett G.L. 2022** — "Cell Discharge Testing to Calibrate a Positive-Electrode Open-Circuit-Potential Model for Lithium-Ion Cells", *J. Electrochem. Soc.* 169, 070524 ([5]) | **96** = 1 (새) | 연재 (iv) — **셀 안에서 양극 OCP 형상 · 창을 방전 시험으로 재보정**(첫 판 "not well calibrated") · 실셀 NMC OCP 출처 · D̄s,ref 초기값 — [[halfcell-ocp-shape-invariance]] · 95호 경우 1(한 전극 빌림)과 같은 축 · ⚠ 액체셀 도구 | Q8 · 모드 좌표 |
| ★★ | **Lu D., Trimboli M.S., Fan G., Zhang R., Plett G.L. 2021** — *J. Electrochem. Soc.* 168, 070532 ([3] · 제목 인쇄 0) | **96** = 1 (새) | 연재 (ii) — "Five teardown-based approaches to estimating OCP in a … MSMR model format" · 실셀 흑연 OCP 출처(표 V) — OCP 측정 층위 · ⚠ 액체셀 도구 | Q8 |
| ★★ | **Lu D., Trimboli M.S., Fan G., Zhang R., Plett G.L. 2021** — *J. Electrochem. Soc.* 168, 080533 ([6] · 제목 인쇄 0) | **96** = 1 (새) | 연재 (v) — 초단 펄스의 SOC · 율 의존 순간 저항 → 전도 아홉 + 계면 동역학 — **비선형 채널이 소신호 비식별을 푸는가**(저자 명제 "nonlinearly identifiable")의 실제 · ⚠ 액체셀 도구 | Q4 |
| ★★ | **Guest B., Trimboli M.S., Plett G.L. 2020** — *J. Electrochem. Soc.* 167, 160546 ([7] · 제목 인쇄 0) | **96** = 1 (새) | 연재 (vii) — PSS 방전 모형으로 ψ̄(가상 셀 오차 ≈40 %) — 표 VI n̄e · κ̄D 의 마지막 인자 · ⚠ 액체셀 도구 | Q4 |
| ★★ | **Chu Z., Plett G.L., Trimboli M.S., Ouyang M. 2019** — *J. Energy Storage* 25, 100828 ([10] · Part I) | 95(☆) · **96** = **2** | **이 편이 쓴 집약 TF 의 출처** · 95호 [31](☆ — 행 없음 관례)에서 올림 · ⚠ 액체셀 도구 | Q4 |
| ★★ | **Rabissi C., Innocenti A., Sordi G., Casalegno A. 2021** — *Energy Technol.* 9, 2000986 ([41]) | **96** = 1 (새) | 임피던스를 정하는 물리 매개변수 28 개의 감도 — "12 out of 28 … low sensitivity or are insensitive" — EIS 식별성의 문헌 쪽 정량 · ⚠ 액체셀 도구 | Q4 |
| ★★ | **Murbach M.D., Hu V.W., Schwartz D.T. 2018** — *JES* 165, A2758 · **Murbach M.D., Schwartz D.T. 2018** — *JES* 165, A297 ([28] · [29]) | **96** = 1 (새) | 비선형 EIS(고조파) — 소신호 비식별을 푸는 채널 후보(저자 "holds promise … beyond the scope") · ⚠ 액체셀 도구 | Q4 |
| ★★ | **Danzer M.A. 2019** — "Generalized distribution of relaxation times analysis for the characterization of impedance spectra", *Batteries* 5, 53 ([69]) | 11 · **96** = **2** (재지목 · **지목 누락 보충** — 11호 후속 ★★★ · 원장 행 0) | GDRT — 인덕턴스 · R–L 분포를 같이 역변환 · 이 편 전처리의 틀 · DRT '계측 경로' 축 | DRT · Q4 |
| ★★ | **Ciucci F., Chen C. 2015** — *Electrochim. Acta* 167, 439 ([68]) | **96** = 1 (새) | 베이즈 · 계층 베이즈 DRT(이 편은 "Wan et al." 로 묶어 인용) — DRT 체크리스트 C3(불확실성)의 원전 후보 | DRT · Q4 |
| ★★★ | Jobman R., Trimboli M.S., Plett G.L. 2015 — *J. Energy Chall. Mech.* 2(2), 45 ([8]) | 95 · **96** = **2** (재지목) | LPM 의 앞선 판 — 연재 (i) "earlier works also presented various evolutionary versions of the LPM" · 원장 행 등급 그대로 | Q4 |
| ★★ | Chu Z., Jobman R., Rodríguez A., Plett G.L., Trimboli M.S., Feng X., Ouyang M. 2020 — *J. Energy Storage* 27, 101101 ([66] · Part II) | 95 · **96** = **2** (재지목) | 그림 1 회로의 원형 · 집약 전도도 정의 | Q4 · Q5 |
| ★ | Wan T.H., Saccoccio M., Chen C., Ciucci F. 2015 — *Electrochim. Acta* 184, 483 ([74]) | 11 · 84 · **96** = **3** (재지목) | 이 편 DRT · GDRT 계산 틀(수정판 — 수정 내용 미인쇄) | DRT |
| ★ | **Rodríguez A., Plett G.L., Trimboli M.S. 2018** — *J. Energy Storage* 20, 560 ([62]) | **96** = 1 (새) | 선형화 DFN 과 정확히 일치하는 TF — 이 편 TF 의 뿌리 | 도구 |
| ★ | **Kong X., Plett G.L., Trimboli M.S., Zhang Z., Zheng Y. 2020** — *JES* 167, 013539 ([64]) | **96** = 1 (새) | EIS 조건에서 TF ↔ 시간 영역 PDE 검증 | 도구 |
| ★ | **Oldenburger M., Bedürftig B., Richter E., Findeisen R., Hintennach A., Gruhle A. 2019** — *J. Energy Storage* 26, 101000 ([76]) | **96** = 1 (새) | 이력이 저주파 EIS 를 오염 — (베) 측정 상태 | (베) |
| ★ | **Meddings N. 외 2020** — *J. Power Sources* 480, 228742 ([14]) | **96** = 1 (새) | 상용 셀 EIS 측정 · 해석 · 검증 개관 | 방법 |
| ★ | **Oca L., Miguel E., Agirrezabala E., … Iraola U. 2021** — *Electrochim. Acta* 382, 138287 ([1]) | **96** = 1 (새) | 해체 기반 매개변수화 개관 — 93호 '재라' 처방의 문헌 쪽 · (헤) | (헤) |
| ★ | **Zhang Q., Wang D., Yang B., Dong H., Zhu C., Hao Z. 2022** — *J. Energy Storage* 50, 104182 ([42]) | **96** = 1 (새) | SOC 감도 기반 EIS 식별 — Strategy 2 의 출처 | Q4 |
| ★ | **Duan X., Liu F., Agar E., Xinfang J. 2022** — *J. Electrochem. Soc.* 169, 040561 ([43] · 저자 표기 인쇄 그대로) | **96** = 1 (새) | Li 금속 반쪽전지 물리 EIS 아홉 매개변수 — "consistent parameter estimates" | Q4 |
| ★ | **Verbrugge M.W., Koch B.J. 2003** — *JES* 150, A374 ([50]) · **Baker D.R., Verbrugge M.W. 2012** — *JES* 159, A1341 ([48]) | **96** = 1 (새) | MSMR OCP · Darken 확산 — 갤러리 구조의 OCP 형상 모형(우리 반쪽전지 OCP 표현의 대안) | Q8 |
| ☆ | [9] Jobman 학위논문 · [61] Lee 학위논문 · [63] Rodríguez 학위논문 · [59] Smith 2007 · [60] Lee 2012 · [65] Jacobsen & West 1995 · [47] Meyers 2000 · [72] Saccoccio 2014 · [73] Shafiei Sabet 2018 · [70] Effat & Ciucci 2017 · [75] Kasper 2022 | 행 없음 | TF 계보 · DRT 알고리즘 · 케이블 인덕턴스 | — |
| ☆ | [11]–[26] · [30]–[33] · [35]–[37] · [39] · [40] · [44]–[46] · [49] · [51]–[58] · [67] · [77]–[86] | 행 없음 | 교재 · TLM · 혼성 EIS · DFN 원전 · MSMR 계열 · 응용 · 전도도 값 | — |

**원장 행이 있으나 재지목 안 함**(이 편 쓰임이 목록 · 인용처): [87] Schmalstieg 2018 *JES* 165, A3799(원장 ★★ 95 \| 1 — 아인슈타인 관계 인용처) · [38] Waag 2013 *Applied Energy* 102, 885(원장 ★★★ 20 · 49 \| 2 — 혼성 EIS 목록) · [71] Hahn 2019 *Batteries* 5, 43(원장 ★★ 84 \| 1 — DRT 목록).

**지목 누락(재지목 안 함)**: [34] **Schönleber M., Klotz D., Ivers-Tiffée E. 2014** *Electrochim. Acta* 131, 20(Lin-KK 원전) — 18호 후속 ★★(DRT 체크리스트 C2 의 정본으로 지목)인데 원장 행 0 · 이 편 쓰임은 K–K 목록 [32–34].

**흡수된 편(교차 — 지목 아님)**: [27] 51호 Illig 2012.

**4차 묶음 13 편과의 관계**: 이 편은 **어느 편도 인용하지 않는다**(87 번호 전수 대조 — Danilov 2011 · Firouz 2020 · Bielefeld 2023 · Schmidt 2024 · Khalik 2021 · Koerver 2018 · Raijmakers 2020 · Kim 2019 · Deng 2021 · Danilov & Notten 2008 · Xie 2008 · Shao 2022 · Ansah 2021) — 파일 55 Khalik 2021 과는 Plett 계보 문헌 셋(이 편 [8] · [10] · [66] = Khalik [25] · [31] · [22])을 공유하고 서로 인용하지 않는다.

**지목 누락 둘** — 이 편 참고문헌 중 앞 호 후속 절에 ★ 이상으로 있었는데 원장 행이 없던 편: Danzer 2019(11호 ★★★ — 이 편이 재지목하며 보충) · Schönleber 2014(18호 ★★ — 이 편 재지목 안 함). 그 밖에 앞 호 후속 절에 있던 이 편 참고문헌(Wan 2015 · Hahn 2019 · Waag 2013 · Schmalstieg 2018 · Jobman 2015 · Chu 2020 · Illig 2012)은 원장 행이 있다.

---

# 이 digest 가 주장하지 않는 것

1. **이 방법이 쓸모없다고 하지 않는다** — 닫힌 꼴 TF · GDRT 인덕턴스 보정 · DRT 초기화 절차는 가상 셀 부분 집합에서 열셋 중 열둘을 ±5 % 안에 두고(그림 11), 초기화 식 · 혹 위치 · 봉우리 τ 는 우리 재현과 맞는다. 걸린 것은 결론 문장의 범위(부분 집합 → "all … very good accuracies") · 전체 집합의 폭 · 실셀 값의 물리 범위 · 배정 가정이다.
2. **표 VI 값이 틀렸다고 단정하지 않는다** — 실셀 최적화에 부록 경계를 그대로 썼는지(특히 "ψ̄ = 1" 가정 아래 물리 단위 경계를 어떻게 옮겼는지) 인쇄되지 않았고, ψ̄ 는 다른 시험(PSS — 가상 셀 오차 ≈40 %)에서 왔다. 우리가 보인 것은 같은 편 부록의 범위와 폐합하지 않는다는 것과, 어떤 ψ̄ 로도 n̄e^n · κ̄D 를 함께 범위에 넣을 수 없다는 것까지다.
3. **R_c ↔ R̄f^n 교환을 확정하지 않는다** — 그림 13(b)(축 0–25 · 판독 폭 ±0.3) 위의 크기 일치와 그림 3 혹 위치 재현(R̄f^n 직렬)까지이고 TF 도출로 확인하지 않았다. 저자가 이름 부른 쌍은 R_c ↔ 1/κ̄^s 다.
4. **C̄dl · k̄0 로 LLI ↔ LAM_PE 를 가를 수 있다고 하지 않는다** — §(d) 의 서명 표는 모형 정의 위의 `[해석]` 이고, 이 편은 노화 · 모드를 다루지 않았으며, 조건 다섯(배정 · CPE · 산포 · 비용 · 식별 폭)이 붙는다.
5. **두 전극 C̄dl 의 순서 뒤집힘이 배정 오류라고 단정하지 않는다** — DRT 초기값(그림 15(e) 평균선)과 최종값(표 VI)의 비교이고, 최종 적합이 옳고 초기 배정이 틀렸을 수도, 그 반대일 수도 있다(검사 수단 — 대칭셀 · 3전극 — 이 지면에 없다).
6. **Panasonic 셀이 특정 조성 · 설계라고 하지 않는다** — "prismatic 25Ah graphite//NMC … Ford C-MAX Energi" 까지가 인쇄이고 NMC 조성 · 두께 · 면적은 미인쇄다.
7. **연재 앞 편의 내용(OCV · 창 · PSS)을 이 편의 결과로 옮기지 않는다** — 그 편들은 이 세션에서 열지 않았고, 서지 · 쓰임은 이 편 서론 · 표 I 의 인쇄 서술까지다.
8. **19 SOC ≈19 일은 측정 기록이 아니라 `[재현·가정]` 이다** — 인쇄 "about a day" × 19 와 주파수 격자 · 휴지로 낸 어림이다(Gamry 의 실제 주기 수 · 방전 시간 미인쇄).
