---
title: "Deng Z., Hu X., Lin X., Xu L., Li J., Guo W. 2021 — A Reduced-Order Electrochemical Model for All-Solid-State Batteries (IEEE Trans. Transp. Electrif. 7(2), 464–473)"
source_url: local-upload/60._A_reduced-order_electrochemical_model_for_all-solid-state_batteries.pdf
source_url_note: "본문 PDF 10 쪽(IEEE Trans. Transp. Electrif. 7(2) (2021) 464–473 · 인쇄 쪽 464–473 · PageLabels 1 부터 · 그림 9 — 전부 벡터(그림 5 · 6 의 PDE 선 일부는 1-bit 마스크) · 표 5 — 벡터 글리프 · 식 (1)–(29) · 참고문헌 31) 3,180,760 B · 업로드 접두사 eaa8e755 · 4차 묶음 파일 60 · SI 없음(보충 언급 0 · 임베디드 파일 하나는 Distiller 작업 설정) · 원자료 · 코드 공개 0 · 자기 실험 0(모형 · 축약 편 — 실험 곡선 셋은 [7] 인용)"
source_doi: 10.1109/TTE.2020.3026962
source_license: "2332-7782 © 2020 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission.(인쇄) · OA 표기 0 · 쪽 바닥 'Authorized licensed use limited to: Hanyang University. Downloaded on October 02,2026 … from IEEE Xplore' — 구독본으로 다룬다 — 이 digest 는 인용 · 요약 · 재현 계산만 담는다(그림 크롭은 위키 관례대로 raw/figures 에 — 변형 없는 잘라내기)"
pdf_sha256: c811ace7de53d07aefd28431364c23709a67d561bef8bceace2d4664c6192cb3
ingested: 2026-10-03
sha256: 34d93cbf3f97facc89c4b615b7cae6e148bec0b170d72f6d2c017fc71c79133f
---
# 수집 목적

`assb` 섹션 **100호** — **4차 묶음 파일 60**(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 요청 14 편 중 열째 · 2026-10-02 사용자 공급 · 파일 51–64 = 91–104호를 받은 순서대로). 닻은 `questions/assb-contact-loss-vs-lampe.md` 의 **Q4(유일성 · 식별성)** 와 원장 §2 **구조적 공백 1번**("역문제 · 식별성을 다루는 ASSB 논문" — 후보 목록의 "Deng 2021")이고, 이 편이 직접 닿는 곳은 ① **99호**(Kim 2019 — 이 편이 축약한 원 모형 · 그림 1 의 출처 [9] · 공저자 X. Lin) ② **26호**(Iwakiri 2024 — 이 편을 "축약 모델 = 파라미터 식별 대상이 되는 형태 — 식별성 논의 여부 미확인" 으로 지목) ③ **37호**(Li 2024 — "ASSB 축약 모델(ROM) — `A_eff` 형 손잡이가 있는지" · 원장 문구 "축약 모델이 θ 를 ε_p 와 따로 두는가" — 37호 자신도 3차 Padé · Ts 1 s 축약을 쓴다(37호 digest 전사)) ④ **91호**(Danilov 2011 — 그림 9 실험 곡선의 출처 [7] · 매개변수 계보) · **98호**(Raijmakers 2020 — [11] · 같은 계보 2020 판) ⑤ 개념 [[assb-sensitivity-sweep-vs-identifiability]] · [[spm-grouped-parameter-identifiability]] · [[assb-lampe-contact-product-degeneracy]] · [[assb-synthetic-truth-contact-loss-requirements]] 다. 우리 쪽 수치(`degradation-degeneracy/`)는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본이고 여기 옮기지 않는다.

Chongqing University(자동차공학과) + Ontario Tech University(자동차 · 메카트로닉스공학과) + Shanghai Jiao Tong University(기계공학) — **Z. Deng** · **X. Hu**(교신) · **X. Lin**(교신 · 99호 공저자) · **L. Xu** · **J. Li** · **W. Guo** 의 *IEEE Trans. Transp. Electrif.* 2021 편. `[인쇄]` 초록이 스스로 적는다: "a series of model reduction methods are applied to obtain a reduced-order model (ROM) for ASSBs. First, analytical solutions of the partial differential equations (PDEs) are derived by the Laplace transform. Then, the Padé approximation method is used to convert the transcendental transfer functions into lower order fractional transfer functions. Next, the concentration distributions in electrodes and electrolytes are approximated by parabolic and cubic functions, respectively. … Compared with the original PDE-based model, the voltage errors of the proposed ROM are less than 2.6 mV. Compared with the voltage response of experimental data, a good agreement can be observed for the ROM under three large C-rates discharging conditions. The calculation time of ROM per step is within 0.2 ms, which means that it can be integrated into a battery management system." 이 편이 실제로 한 것은 **99호 계열 Li | Li₃PO₄ 1.5 µm | LiCoO₂ 320 nm · 1 cm² 박막 1D 모형(COMSOL 5.4a)을 '원 PDE 모형' 으로 두고, 양극 확산과 (생성 · 재결합 r 항을 버린) 전해질 확산을 Laplace 로 풀어 3차 Padé 전달함수로 줄이고, 양극 · 전해질 농도 단면을 포물선 · 삼차식으로 근사해 η_d · η_mt · η_ct(α_pos 0.5) · V 를 Δt 1 s 로 계산한 축약 모형(ROM)을, 같은 매개변수 한 벌(표 I)의 PDE 와 10C 정전류 · 축척 UDDS(두 번 반복) · 1–10C(표 V)에서 비교하고, [7](91호 Danilov 2011)의 실험 방전 곡선 셋(6.4 · 12.8 · 25.6C)에 겹친 모형 편**이다. **자기 실험 0** · 매개변수 추정 0 · 열화 · 접촉 · 압력 축 0(`contact*` · `degrad*` · `pressure` 본문 0 회).

들어온 경로: 원장 행(도착 표시 전 원문 그대로) "| ★★ | **Deng·Hu·Lin·Xu·Li·Guo 2021** — *IEEE Trans. Transp. Electrif.* **7**(2), 464 | 26 · 37 | **2** | Q4 | 축약 ASSB 모델 — 식별 대상이 되는 형태. 식별성을 다루는지 미확인 (공백 1번 후보) · 37호: 축약 모델이 θ 를 ε_p 와 **따로** 두는가 |". 위키 grep(`Deng` · `Transp. Electrif` · `TTE.2020.3026962` · `3026962` · `7(2), 464` · "Reduced-Order Electrochemical Model" · `Deng·Hu` · `Deng 2021` · `Deng, Hu`)으로 각 digest 의 **후속 절**을 다시 셌다: **26호 §11(:383 · ★★★ · [16]) · 37호 §14(:413 · [29] — 등급 칸 없는 후속 표 · 98 · 99호가 Raijmakers · Kim 2019 를 셀 때와 같은 처리 — 원장 행이 37호 때 세운 지목) = 2 — 원장 "2" 와 일치**(정정 없음). 교차 기록(지목 아님): 99호 :546 "(이 편 이후 편 · 인용 0)" · 75호 :777 의 원장 §2 행 전사 · 93 · 94 · 95 · 96 · 98 · 99호 "4차 묶음 13 편과의 관계" 문장 · 카드 · 로그의 26 · 37호 항(digest 후속 절 아님). 이 편은 우리 digest **셋**을 인용한다([7] = 91호 · [9] = 99호 · [11] = 98호) · 4차 묶음 다른 13 편 중 **[7](파일 51) · [9](파일 59) · [11](파일 58) · [26](파일 61 Danilov & Notten 2008)** 넷을 인용한다(31 번호 전수 대조 — 나머지는 이 편보다 뒤이거나 인용 0).

이 digest 의 일 (지시):

1. **(a) 축약 단계** — Laplace 해 → Padé 차수 선택(그림 2–3 · 3차 선택 근거) → 포물선 · 삼차식 농도 근사 · PDE 대비 오차('2.6 mV' 인쇄)의 조건(전류 · 프로파일).
2. **(b) 실험 대조 · 매개변수 출처** — "three large C-rates" 실험 자료의 출처(셀 · 저자 · 이 편 측정인가 인용인가) · 매개변수가 99호 표 1 과 같은가 · 99호에서 나온 것(그림의 Nernst 항 부재 · D_n⁻ 표기 · k_pos 관례 · '9 %' 편향)을 물려받았는가.
3. **(c) 식별 대상으로서의 ROM (Q4)** — 매개변수 묶음 · 식별성 언급 여부(원장 "식별성을 다루는지 미확인 — 공백 1번 후보" 판정) · Q4 어휘 전수 · "n 번째 성질".
4. **(d) θ ↔ ε_p** — 접촉 · 활물질 분율을 따로 두는가(37호 물음).
5. **(e) 후속 후보.**

⚠ **표기 규약**: `[인쇄]` = 원문이 실제로 쓴 것 · `[도표]` = 그림을 눈으로 읽은 값(판독 폭 표시) · **`[도표·벡터]`** = PDF 벡터 경로 좌표를 축 프레임 · 눈금 선으로 보정해 읽은 값(그림 2–9 — 저자 원자료가 아니다 · 경로 꼭짓점은 선 중심 · 선 폭 ≈0.6–1 pt = 그림 7(a) ≈0.6–1.0 mV · 그림 7(d) ≈17–28 mV · 그림 9 ≈16 mV 이나 꼭짓점 좌표는 그보다 훨씬 곱다 · 그림 2 · 3 의 표지는 도형 상자 중심이라 ±1 dB · ±1° 오프셋) · `[재현]` = 원문 수치 · 식으로 우리가 다시 계산 · `[재현·가정]` = 가정이 붙은 재현(가정을 같이 적는다) · `[재현·대수]` = 인쇄된 식만으로 한 대수(기호 계산 포함) · `[재현·외부 값]` = 원문 밖 값을 쓴 재현(91호 digest 전사 값 — Danilov 외삽 EMF 11 점 · 측정 용량 · 모형선 시각) · `[해석]` = 우리 해석 · **"(N호 digest 전사)"** = 이 세션에서 그 원문을 다시 열지 않고 우리 digest 의 전사로 대조한 것. **`[데이터]` 0** — 예치 원자료 · 코드 공개 진술 0.

⚠ **측정 · 인용 · 모형 · 적합 구분**: 이 편 안의 수치는 ① **측정 0** — 이 편이 잰 것은 실행 시간(표 V · 노트북 i7-8565U)뿐이다 ② **인용**(표 I 의 값 열여섯 — 머리 출처 "[9], [27]" · 본문 "a complete set of model parameters obtained from a thin-film ASSB … The validity of the parameters has been verified by many existing references [7], [9], [27]" — 91호 표 II 의 설계 · NDP · 적합 값이 99호 표 1 을 거쳐 온 것(91 · 99호 digest 전사) + k_neg · α_neg 새 값 · 식 (14) 평형 전위 = "[10]" Fabre 의 "fit from experimental data" 유리함수(99호 식 22 와 같은 계수) · 그림 9 의 실험 곡선 = [7] Danilov 의 측정(이 편이 재측정하지 않음 · 옮긴 방법 미인쇄)) ③ **모형 출력**(그림 2–9 · 표 IV · V 의 PDE · ROM 값 전부 계산) ④ **적합 0**(매개변수 추정 0) 넷이다.

⚠ **쪽 표기**: PDF 10 쪽 = 인쇄 쪽 464–473(머리 쪽 번호 · "IEEE TRANSACTIONS ON TRANSPORTATION ELECTRIFICATION, VOL. 7, NO. 2, JUNE 2021" / "DENG et al.: REDUCED-ORDER ELECTROCHEMICAL MODEL FOR ASSBs" — PageLabels 는 1 부터라 인쇄 쪽이 아니다). 이 digest 는 인쇄 쪽 **"p. 467"** 로 적는다(PDF 쪽 = 인쇄 쪽 − 463).

⚠ **기호 충돌**: 이 편의 **θ** 는 양극 정규화 농도 c_Lis/c_Lis,max(식 12 — θ_s 표면 · θ̄ 벌크)이고 카드 · 개념의 **`θ`(접촉 · 활성 분율)** 와 다른 양이다. 이 편의 **D_e** 는 식 (21) 에서 D_Li⁺D_n⁻/(D_Li⁺ + D_n⁻)(확산 계수)로 정의되고 식 (28) 에서는 무차원 비 (D_Li⁺ − D_n⁻)/(D_Li⁺ + D_n⁻) 자리에 같은 글자가 쓰였다(D6). 이 digest 는 식 (5) 의 계수 2D_Li⁺D_n⁻/(D_Li⁺ + D_n⁻) 를 **D_amb** 라 부른다(그림이 쓴 값 — D3).

---

# 판정 먼저

1. ★★★★ **(c) Q4 — 이 편은 식별 대상이 되는 꼴(전달함수 계수 = 매개변수 묶음)을 ASSB 에 처음 세웠지만 식별성은 다루지 않는다.** `[재현·대수]` 표 II · III 의 계수는 전부 묶음 다섯으로만 쓰인다 — 양극 **1/(A·F·L_p)**(용량 극) · **L_p²/D_Lis**(확산 시간) · 전해질 **L_e/(4A·F·D_Li⁺)**(직류 이득) · **L_e²/D**(시간) · 그리고 식 (7) 의 **A·k_pos**(교환 전류). 그러나 `[인쇄]` 본문 · 캡션에 `identif*` 는 남의 편 소개 한 번(Fabre — "to identify some model parameters")뿐이고 `observab*` · `estimab*` · `sensitiv*` · `uniqu*` · `confiden*` · `uncertain*` · `±` · `correlat*` · `Fisher` · `Gramian` · `covarian*` · `noise` **0** · 매개변수 추정 0 · 묶음 목록 0("The coefficients of the transfer functions can be explicitly derived from the electrochemical parameters" · "a lumped-parameter model" 두 문장뿐). 검증은 **같은 매개변수 한 벌의 PDE 대비 오차**와 다른 편 실험 곡선 셋이고, 'SOC · SOH 오차 < 4 %' 는 추정기를 돌리지 않고 액체셀 문헌 [14] · [31] 에서 옮긴 문장이다(같은 모형 계열의 ASSB 상태 추정 [9] = 99호 의 9 % · 5 % 는 언급 0). ⇒ **Q4 0/100 — 아흔두 번째 성질**(아래 §(c) 4) · 원장 §2 공백 1번 후보 목록의 마지막 ASSB 편 Deng 2021 은 **식별성 편이 아니다** — 후보 목록의 ASSB 편 넷(Naik 75 · Firouz 92 · Kim 99 · Deng 100호)이 모두 같은 판정으로 닫힌다(Khalik · Lu 는 액체 도구 칸 95 · 96호 · Forman 2012 미수령).
2. ★★★★ **(a) '2.6 mV' 는 오차의 상한이 아니라 UDDS 의 RMSE 이고, 비교 대상은 같은 매개변수 한 벌의 PDE 다.** `[인쇄]` 표 IV — UDDS V_t RMSE **2.60** · MaxAE **40.5 mV**(본문 "occurs at the end of discharge") · 10C RMSE **0.54** · MaxAE **4.60 mV** · 초록 "the voltage errors of the proposed ROM are less than 2.6 mV"(결론은 "RMSE … 0.54 and 2.6 mV" 로 바르게 씀 — D1). 조건: **UDDS = 두 번 반복 축척 프로파일**(`[도표·벡터]` 2,742 s · 자기상관 지연 1,370 s · −3.88 … +8.65C · 평균 1.29C · 순 0.979 Q — 축척 방법 미인쇄) · Δt 1 s · α_pos 0.5 · r 항 무시 · 기준 = COMSOL 5.4a('normal' 메시). `[도표·벡터]` 그림 8 ROM − PDE 의 최대는 V 36.7 mV @2,722 s · η_d 36.0 mV @2,713 s — 방전 끝 몇십 초다. 그리고 ★ **같은 10C 실행에서 V_t 최대 오차 4.6 mV 와 η_d 최대 오차 76.3 mV 가 함께 있다** — `[재현·대수]` 식 (16) 둘째 줄 V_t = Eeq(θ_s) + η_ct,pos − η_ct,neg + η_mt 이라 **전압은 표면 θ_s 만 보고 벌크 θ̄ 는 보지 않는다**: η_d 의 오차는 Eeq(θ̄) 의 같은 크기 반대 부호 오차로 상쇄돼 전압에 안 나온다. **출력이 맞는다 ≠ 성분 분해가 맞다** 의 지면 안 표본이다(`[해석]` — 우리 프로젝트 물음의 모형 층 판). `[재현]` 그리고 ROM 의 'r 항 무시' 는 인쇄 k_r(91호가 ×100 어긋난다고 본 값)에서만 싸다: 10C r 항 제거 오차 RMS **0.40 · 최대 0.75 mV**(인쇄 k_r) → **14.85 · 23.94 mV**(k_r ×100 — 91호 그림 일치 값) — ROM 이 보고한 RMSE 0.54 mV 의 ≈27 배.
3. ★★★★ **(a) Padé 차수는 계수가 맞고 근거 그림이 틀렸다 — 그림 3 의 'PDE' 곡선은 식 (22) 의 응답이 아니고, 인용한 2.5 Hz 기준은 고른 3차가 못 맞춘다.** `[재현·대수]` 표 II(y = L_p · y = 0) · 표 III 의 1–3차 계수는 √u coth √u · √u / sinh √u · tanh z / z 의 Padé 그대로다(y = 0 2차 분자 부호 하나만 오기 — D9). `[도표·벡터]` 그림 2 의 PDE = 정확한 coth 응답 ±0.13 dB · ±0.06° · 표지 = 표 II Padé ±0.75 dB · ±0.34°. 그러나 **그림 3 의 PDE 곡선은 정확한 tanh 응답이 아니다**: ω 10⁻³ rad/s 위상 −3.9°(정확 −7.0 · 1차 표지 −6.9) · 0.1 rad/s 142.5 dB(정확 137.1) · 1 rad/s 142.9 dB(127.1) · 632 rad/s **499 dB(99.0)** · 위상 −32° 골 뒤 +87°(1.58 rad/s)로 올라갔다가 들쭉날쭉 — 정확한 응답은 크기가 단조 감소하고 위상이 −45° 로 간다. 본문은 이것을 "The results are a little surprising. The magnitude response of the PDE-based model diverges … its phase response oscillates" 로 읽고 "after comprehensively considering the magnitude and phase responses" 3차를 골랐다(D2 · 원인 미확정). 그리고 `[재현]` 1 dB · 5° 기준 3차의 유효 대역은 양극 **1.18 rad/s(0.19 Hz)** · 전해질 **0.35 rad/s(0.056 Hz)** — 본문 기준 "90% of the signal power of typical driving cycles have frequencies of less than 2.5 Hz [19]"(15.7 rad/s)에서 3차는 양극 −6.1 dB · −40° · 전해질 −11.2 dB · −43.5° 어긋난다(그림 축은 rad/s · 실행 Δt 1 s 의 Nyquist 0.5 Hz 에서도 −23° · −38° — D4).
4. ★★★★ **(a)(b) 인쇄 식 다섯 자리가 계산과 다르다 — 그림은 고친 꼴로만 닫힌다(코드 미공개라 구현 확정은 아님).** `[도표·벡터]` + `[재현]` ① 식 (21) · 표 III 의 D_e = D_Li⁺D_n⁻/(D_Li⁺ + D_n⁻) ↔ 그림 3 표지 · 그림 5(c) ROM 표지는 **D_amb = 2D_e** 로 계산(1차 위상 −45° @8.19×10⁻³ rad/s → D 1.535×10⁻¹⁵ · 그림 5(c) ±50 mol m⁻³ — D_e 면 6.5 dB · 19.5° · 400–870 mol m⁻³ 어긋남 — D3) ② 식 (27) a₂ 둘째 항 3i/(2L_e²FAD_Li⁺)(차원 불일치) ↔ 그림 5(d) ROM 삼차식은 **L_e** 꼴(RMS 2–38 mol m⁻³ · 인쇄 꼴이면 3.6×10⁹ — D5) ③ 식 (28) 'D_e' 자리 ↔ 그림 7(a) ROM η_mt 는 **비 (D_Li⁺ − D_n⁻)/(D_Li⁺ + D_n⁻)** 로 계산(±0.08 mV · D_e 그대로면 13.7 mV — D6) ④ 식 (18)–(20) 분모 AFβ√D_Lis ↔ 표 II · 그림 2 는 **AFD_Lisβ**(D7) ⑤ 식 (6) 둘째 지수의 − 부호 빠짐(D10). ★ 반대로 **원 PDE 는 인쇄 식 (9) 그대로 Nernst 항을 넣고 계산됐다**: 우리 재풀이(표 I · SOC₀ 1.0 · T 298.15 K)가 그림 7(a) η_mt 를 1–330 s **±0.05 mV** 로 다시 내고, Nernst 항을 빼면 최대 **19.3 mV** 어긋난다(300 s −38.30 ↔ 그림 −38.35 mV) — 99호 그림의 '전체 모형'(Nernst 항 없음 — 99호 D1)과 다른 구현이다.
5. ★★★ **(b) 그림 9 의 실험은 [7](91호 Danilov 2011)의 측정을 옮긴 것이고, 모형은 식 (14) 가 아니라 [7] 의 외삽 EMF 로 계산된 것으로 읽힌다(인쇄 0) — 그리고 '실험' 곡선의 끝이 원 측정보다 짧다.** `[인쇄]` "The experimental data come from [7], and the same model parameters in the reference are also used in this article." `[재현·외부 값]` 표 I + 식 (14) 로 6.4 · 12.8 · 25.6C 를 풀면 t = 1 s 전압이 그림 PDE 보다 **+74 … +92 mV** 높다 — [7] 의 외삽 EMF(91호 digest 전사 11 점 · 선형 보간)로 바꾸면 **−2.0 … +2.6 mV** · 대부분 ±7 mV(EMF 보간 마디 근처 ≤22 mV). `[도표·벡터]` 실험 첫 표지 4.173 · 4.151 · 4.111 V = 91호 측정 Q = 0 전압 4.177 · 4.156 · 4.116 V(91호 digest 전사) ✅ · 그러나 실험 점선의 끝 **546.4 · 266.6 · 124.2 s** 는 91호 측정 용량 9.86 · 9.76 · 9.57 µAh cm⁻²(÷ C · 10 µA cm⁻² = 554.6 · 274.5 · 134.6 s)의 **×0.985 · 0.972 · 0.924** 이고, PDE 끝 543.1 · 262.1 · 122.0 s 는 Danilov **자기 모형선**(91호 전사 541.7 · 257.9 · 121.1 s)과 같은 자리다 — 91호가 "모형이 25.6C 용량을 10 % 못 낸다" 고 본 자리가 이 그림에서는 '일치' 로 보인다(옮긴 방법 · 시간 원점 미인쇄 — 디지타이즈 오차일 수 있다 · D12). 그리고 그 EMF 자체가 같은 방전 곡선의 율 외삽 회귀다(91호) — 비교의 측정 몫이 입력에 들어가 있다(`[해석]`).
6. ★★★ **(b) 99호에서 물려받은 것과 아닌 것.** ✅ 고침: D_n⁻ 표 I **5.1×10⁻¹⁵**(99호 표 1 의 2.1 ↔ 그림 5.1 — 이 편 그림 5 · 7 이 5.1 로 닫힘) · c_Lis,max **2.33×10⁴** · c_Lis,min **1.165×10⁴** 인쇄(99호 공백 G1 — 91호 a_max · a_max/2 와 같음 → 1C = 9.99 µA). ✅ 다름: 원 PDE 에 Nernst 항 있음(위 4). ⚠ 물려받음: k_pos **5.1×10⁻⁴ m³ mol⁻¹ s⁻¹**(91호 k₁ˢ 의 ×100 · 다른 단위 — 식 (7) F·A·k_pos 차원 불일치 그대로 · 수치(A m²)로 그림 7(c) η_ct 를 ±0.2 mV 로 재현) · k_r **0.9×10⁻⁸**(91호 ×100 문제 — 그림 7(a) 는 인쇄 값으로 닫힘) · 평형 곡선 = 같은 Fabre 유리함수 · α_pos 0.5 단순화 · T 미인쇄(298.15 K 로 닫힘). ❌ 무시: 99호의 SOC 오차 9 % · 5 %(OCV 평탄 증폭 편향)는 인용 0 — 대신 "batteries are usually operating at the range of 100%–10% SOC" 와 '< 4 %'(액체 문헌). 그리고 "The results of [9] suggest that ignoring the r term will not cause a large voltage error" 는 99호 표 2 결론을 조건(인쇄 k_r · 10C)을 떼고 옮긴 것이다.
7. ★★★ **(d) 37호 물음 — 이 축약 모형은 θ 도 ε_p 도 두지 않는다: 면적 A 하나가 용량 극 1/(A·F·L_p) · 전해질 이득 L_e/(4A·F·D_Li⁺) · 교환 전류 F·A·k_pos 에 같은 값으로 들어간다.** '접촉만 줄고 용량은 그대로' 를 표현할 자리가 없다 — 37호(같은 3차 Padé · Ts 1 s 계열)가 A_eff 를 BV 분모에만 넣은 것은 이 편 뒤의 추가이고, 그때도 A_eff ↔ k_p 곱 대칭이 남는다(37호 digest 전사). `[재현·대수]` 양극 묶음 셋(A·L_p · L_p²/D_Lis · A·k_pos)은 (A, L_p, D_Lis, k_pos) → (λA, L_p/λ, D_Lis/λ², k_pos/λ) 에서 모두 그대로다 — **양극 쪽 출력만으로는 '면적 손실' 과 '두께(활물질) 손실' 이 한 방향으로 묶이고**, 그 방향은 전해질 이득 · 시간(A·D_Li⁺ · L_e²/D)이 전해질 수송 계수와 곱으로만 잡는다(91호에서 전해질 넷은 \|상관\| ≥ 0.98 한 묶음 — 91호 digest 전사). 원장 R1(용량에 곱해지되 ε_p 와 별개인 θ — [[assb-synthetic-truth-contact-loss-requirements]])의 또 하나의 위반 표본이다.
8. **채움표** — Q1 해당 없음(`θ(N)` 0/100 · 층 하나: 면적 A 한 값이 용량 극 · 수송 이득 · i₀ 에 · 양극 묶음의 면적 ↔ 두께 축척 대칭) · Q2 없다(전압 하나 · 실험 = 인용 곡선 셋) · Q3 층 하나("PDE 기준 = 인쇄 식 그대로(Nernst 항 포함 — 재풀이 ±0.05 mV) · ROM 은 인쇄 식 다섯 자리를 고친 꼴로 계산 · 표 I = 99호 표 1 계보(D_n⁻ 고침 · c_max/c_min 인쇄 · k_r · k_pos 그대로) · 그림 9 = [7] 측정 + [7] EMF(인쇄 0)") · **Q4 0/100 — 아흔두 번째 성질** · Q5 해당 없음(Li 금속 · η_ct,neg 10C "lower than 0.1 mV" 인쇄 · `[재현]` 0.05–0.06 mV) · Q6 해당 없음(`pressure` 0) · Q7 해당 없음 + 공백 하나 채움(c_max · c_min 인쇄 · SOC₀ 1.0 = c_min) · Q8 층 둘(식 (14) Fabre 유리함수 + 그림 9 의 [7] EMF — 한 지면에 평형 곡선 둘 · 표기 0). **누적 ≈20.0 → ≈20.0 (새 칸 0).**

---
# 서지

| 항목 | 값 (`[인쇄]` — p. 464 · p. 472–473 · XMP) |
|---|---|
| 제목 | **"A Reduced-Order Electrochemical Model for All-Solid-State Batteries"**(지면 · 정보 사전 · XMP 같음) |
| 저자 · 소속 | **Zhongwei Deng** · **Xiaosong Hu**(Senior Member, IEEE) · **Xianke Lin**(Member, IEEE) · **Le Xu** · **Jiacheng Li** · **Wenchao Guo** — Deng · Hu · Xu · Li: Department of Automotive Engineering, Chongqing University, Chongqing 400044 · Lin: Department of Automotive and Mechatronics Engineering, Ontario Tech University, Oshawa, ON L1G0C5 · Guo: School of Mechanical Engineering, Shanghai Jiao Tong University · 교신 X. Hu · X. Lin(메일 인쇄 — 옮기지 않음) · X. Lin = 99호 둘째 저자(99호 소속 표기 'University of Ontario Institute of Technology' · 같은 주소 Oshawa L1G 0C5 — 99호 digest 전사) |
| 저널 | *IEEE Transactions on Transportation Electrification* **7**(2), **464–473**, June 2021 · doi `10.1109/TTE.2020.3026962` · ISSN 2332-7782(첫 쪽 바닥 저작권 줄) |
| 일정 | Manuscript received **15 May 2020** · revised **11 August 2020** · accepted **19 September 2020** · date of publication **28 September 2020** · date of current version **10 May 2021** · `[재현]` 접수 → 수락 **127 일** |
| 저작권 | "2332-7782 © 2020 IEEE. Personal use is permitted, but republication/redistribution requires IEEE permission." · OA 표기 0 · 쪽마다 바닥 "Authorized licensed use limited to: Hanyang University. Downloaded on October 02,2026 at 12:47:51 UTC from IEEE Xplore. Restrictions apply." ⇒ **구독본으로 다룬다** — 이 digest 는 인용 · 요약 · 재현 계산만 담고 그림 크롭은 위키 관례대로 `raw/figures/`(변형 없는 잘라내기) |
| 키워드 | Control-oriented model · electrochemical model · lithium-ion battery · reduced-order model (ROM) · solid-state battery(Index Terms · XMP `dc:subject` 같음) |
| 자금 | National Natural Science Foundation of China 51875054 · Chongqing Natural Science Foundation for Distinguished Young Scholars cstc2019jcyjjq0010 · for Postdoctor cstc2020jcyj-bsh0040 · "Engineering Research Council of Canada" RGPIN-2018-05471(인쇄 그대로) · 이해 상충 진술 0 |
| 코드 · 자료 | **공개 진술 0** · 원 PDE = "COMSOL Multiphysics 5.4a"(유한요소 · 메시 'normal') · ROM · 원/단순 PDE 의 유한차분판 = MATLAB(ode45 · 마디 10 + 10) · PC "Intel Core i7-8565U CPU 1.8 GHz and 7.85-GB RAM available" |
| 분량 | 10 쪽(본문 9 쪽 + 저자 약력 1 쪽) · 그림 **9**(전부 벡터 — 그림 5 · 6 의 (a)(c)/(b)(c) PDE 선은 1-bit 마스크 조각) · 표 **5**(I–V · 전부 벡터 글리프 — 텍스트 층에 없음) · 번호 식 **(1)–(29)** · 참고문헌 **[1]–[31]**(빠진 번호 0 — p. 472–473 목록에서 직접 셈) |
| 절 | I. Introduction · II. PDE-Based Model · III. Reduced-Order Model Derivation(A. Electrode Concentration Approximation · B. Electrolyte Concentration Approximation · C. Battery Terminal Voltage) · IV. Results and Analysis(A. Verification of Li⁺ Ion Concentration · B. Verification of Overpotentials and Voltage · C. Verification of Performance) · V. Conclusion · References · 저자 약력 여섯 |
| 셀 | **모형만** — Li 금속 | Li₃PO₄ L_e **1500 nm** | LiCoO₂ L_p **320 nm** · A **1 cm²**(표 I · 그림 1) = 91 · 99호 셀 기하(91호 digest 전사: 공칭 10 µAh) · 셀 제작 · 측정 0 · `[재현]` 표 I 의 c_max − c_min 로 Q = F·A·L_p·(c_max − c_min) = **9.99 µAh** · 1C = **9.99 µA** |
| 모의 | 원 PDE(COMSOL) · 원 PDE · 단순 PDE(r 무시)의 MATLAB 유한차분판 · ROM(MATLAB · Δt 1 s) — 10C 정전류(그림 5 · 7 · 표 IV) · 축척 UDDS(그림 6 · 8 · 표 IV) · 1 · 2 · 5 · 10C 방전 + UDDS(표 V) · 6.4 · 12.8 · 25.6C(그림 9 — [7] 실험과 겹침) |
| 모형 | 1D · 등온(T 미인쇄) · 음극 = Li 금속(전위 0 V · BV η_ct,neg — 식 8 · k_neg) · 전해질 = Li⁰ ⇌ Li⁺ + n⁻ 해리(r — 식 4) + 이원 확산(식 5 · 계수 2D_Li⁺D_n⁻/(D_Li⁺ + D_n⁻)) · 양극 = Fick(식 1) + BV(식 6–7 · α_pos 0.6) · η_mt = (RT/F) ln[c(L_e)/c(0)] − ∫E dx(식 9 — **Nernst 항 포함**) · η_d = Eeq(θ_s) − Eeq(θ̄)(식 11) · V_t = Eeq(θ̄) + η_d + η_ct,pos − η_ct,neg + η_mt = Eeq(θ_s) + η_ct,pos − η_ct,neg + η_mt(식 16) · Eeq(θ) = [10] Fabre 의 유리함수(식 14 — 99호 식 22 와 같은 계수) · ROM = 식 (1) · (5)(r 무시)의 Laplace 해(식 17–22) → 3차 Padé(표 II · III) + 포물선(식 23–25) · 삼차식(식 26–28) + α_pos 0.5 의 asinh 꼴(식 29) · 열화 · 이중층 · 축전기 0 |

**PDF 메타데이터 (이 실행에서 직접 읽음 · pymupdf)** — 3,180,760 B · sha256 `c811ace7de53d07aefd28431364c23709a67d561bef8bceace2d4664c6192cb3`(호출자 명시값 ✅ — 직접 재계산) · 헤더 `%PDF-1.4` · 10 쪽 전부 612 × 792 pt(US Letter) · 암호 0 · 정보 사전: title **"A Reduced-Order Electrochemical Model for All-Solid-State Batteries"** · author **""**(빈 값) · subject **"IEEE Transactions on Transportation Electrification;2021;7;2;10.1109/TTE.2020.3026962"** · keywords "" · creator **"Aspose Ltd."** · producer **"Aspose.Pdf for .NET 8.3.0; modified using iText® 7.1.1 ©2000-2018 iText Group NV (AGPL-version)"** · 생성 **D:20210428172906+05'30'** · 수정 **D:20210510043430-04'00'**(호출자 메모와 같음 ✅ — 수정일 = 지면 'date of current version May 10, 2021' 과 같은 날 · 판정 안 함) · 트레일러 ID [AA9BBDCBD3301A1B6887A448816FC0C0 · 084A261126DAEAC4263A6B83824AA908] · XMP **3,386 B**(`dc:format` application/pdf · `dc:publisher` IEEE · `dc:description` = subject 와 같은 문자열 · `dc:subject` 키워드 다섯 · `prism:publicationName` · `prism:startingPage` 464 · `prism:endingPage` 473 · `prism:coverDisplayDate` "  June 2021"(앞 공백 둘) · `prism:issueIdentifier` 2 · `prism:volume` 7 · `prism:doi` — `dc:creator` 없음 · CrossMark 없음) · 카탈로그 `/PageLabels`(십진 1 부터 — 인쇄 쪽 아님) · `/Names /EmbeddedFiles` **1 개 — "01-Web-res setting-web-IEEE.joboptions"**(Adobe Distiller 작업 설정 · 복원 6,526 B — 제작 부산물 · 보충 자료 아님 · pymupdf `embfile_count()` 는 0 으로 셈(이름 트리가 Kids 아래라)) · `%%EOF` 1 · 래스터: p. 465–468 의 1×1 1-bit 조각(분수선 · 괄호용 — 그림 아님) · p. 469 1-bit 마스크 넷(그림 5 (a)(c) PDE 선) · p. 470 1-bit 마스크 여섯(그림 6 (b)(c) PDE 선) · p. 473 저자 사진 여섯(RGB) · 그림 1–9 · 표 I–V 는 벡터(눈금 글자도 글리프 경로).

⚠ **텍스트 층**: 합자 **84**(ﬁ 79 · ﬂ 5 — NFKC 로 복원 · NFKC 가 바꾸는 글자 87) · 표 I–V 의 글자 · 그림 안 글자는 벡터 글리프라 **텍스트 층에 없다**(어휘 집계 밖 — 표는 쪽 렌더로 읽음) · 식은 수식 글리프가 줄마다 흩어진다(예: 식 (7) 'i0,pos = −FAkpos' 이후 괄호 · 지수가 떨어져 나옴) — 식 (1)–(29) · 표 I–V · 쪽 머리는 **쪽 렌더 조각으로 읽었다**(220–300 dpi · 판독용 · 커밋 안 함) · 줄 끝 하이픈은 IEEE 분철(복원 뒤 셈).

---

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **온도 T** — RT/F 가 식 (2) · (6) · (9) · (10) · (28) · (29) 에 들어가는데 값 0 | `[재현·가정]` 298.15 K 로 그림 7 이 닫힌다(η_mt ±0.05 mV · V ±1.4 mV) — 다른 T 면 η_mt · η_ct 가 비례로 움직인다 |
| **G2** | **초기 SOC · 컷오프 전압** — "the battery SOC decreases from 100% to 0%"(10C · UDDS) 문장뿐 · 컷오프 0 · 표 V 는 지속 시간(3574 · 1777 · 699 · 340 · 2742 s)만 · ROM 흐름도(그림 4)의 끝 판정은 t ≥ t_max 하나 | `[재현]` SOC₀ 1.0(= c_Lis,min — i₀,pos 가 0 인 점에서 출발)이어야 그림 7 끝(339.01 s · 3.350 V)이 닫힌다(재풀이 3.35 V 도달 339.61 s · SOC₀ 0.995 · 0.99 는 끝이 15–45 mV 어긋남) · 그 순간 SOC 는 0 이 아니라 **0.057**(10C) · UDDS 순 통과 0.979 Q → **0.021** |
| **G3** | **ROM 의 시간 이산화** — 연속 전달함수(표 II · III)를 Δt 1 s 로 어떻게 이산화했는지(영차 유지 · 쌍일차 · 상태 공간) · 전달함수 상태의 초기값 미인쇄 | 우리 연속 시간 계단 응답(`scipy.signal.lsim`)이 그림 5(c) ROM 표지를 ±50 mol m⁻³ 로 다시 내지만, UDDS(1 s 마다 바뀌는 입력)의 끝 오차(40.5 mV)가 이산화에서 얼마인지 가를 수 없다 |
| **G4** | **UDDS 축척** — "extracted from a commercial electric vehicle and is then scaled down for the battery" 만 · 최대 C-rate · 평균 · 반복 수 · 회생 처리 0 | `[도표·벡터]` 그림 6(a): 2,742 s · UDDS 두 번(자기상관 지연 1,370 s · r 0.985) · −3.88 … +8.65C · 평균 1.29C · 순 0.979 Q(방전 1.076 · 회생 0.098) — '2.6 mV' 의 조건이 그림에만 있다 |
| **G5** | **그림 9 의 계산 조건** — "the same model parameters in the reference are also used in this article" 한 문장 · 어느 값(표 I ↔ [7] 표 II) · 평형 곡선(식 14 ↔ [7] EMF) · 초기 SOC · 실험 곡선을 옮긴 방법(원자료 ↔ 그림 디지타이즈) · 시간 원점 미인쇄 | `[재현·외부 값]` 식 (14) 로는 시작 전압이 +74 … +92 mV 어긋나고 [7] EMF 로는 ±7 mV — 지면이 쓰지 않은 평형 곡선 교체(D11) · 실험 끝이 원 측정보다 1.5–7.6 % 짧음(D12) |
| **G6** | **기준 PDE 의 수치 설정** — COMSOL '메시 normal' 외 요소 수 · 시간 단계 · 허용오차 · r 항 처리(원 PDE 에 포함으로 읽힘) · MATLAB 원 PDE 가 r 항을 넣었는지('Original PDE (MATLAB)' — 포함으로 읽힘) | 표 V 'Original PDE (MATLAB)' RMSE 0.08–0.50 mV 가 이산화 오차인지 r 처리 차인지 못 가른다 |
| **G7** | **표 IV 의 두 α 행의 정의** — "η_ct,pos(α = 0.5)" · "(α = 0.6)" 이 각각 무엇 ↔ 무엇의 차인지 · RMSE 표본 시각(1 s?) · MaxAE 를 잰 끝 시각 미인쇄 | 본문 "The additional error by assuming α = 0.5 is insignificant" 로 읽으면 (α = 0.5) = ROM(asinh) ↔ PDE · (α = 0.6) = ROM(근 찾기) ↔ PDE — 그 차 5.60 ↔ 0.68 mV(10C 최대)가 'insignificant' 인지는 끝 시각에 매달린다 |
| **G8** | **k_neg · α_neg 의 출처** — 표 I 머리 "[9], [27]" 인데 [9](99호)에는 음극 동역학이 없다(99호 digest 전사: "The value of charge transfer at the negative electrode is neglected") · [27] Tian & Qi 미열람 | k_neg 1×10⁻² m³ mol⁻¹ s⁻¹ → `[재현]` 수치 i₀,neg ≈0.041(A · 식 8 F·A·k_neg(c/c₀)^½) · η_ct,neg 10C 0.05–0.06 mV — 값이 어디서 왔든 결과에 거의 안 들어간다 |
| **G9** | **식별성 · 불확실성** — 매개변수 묶음 목록 · 감도 · 관측성 · 오차 막대 · 다중 실행 0 | Q4 칸이 움직이지 않는 이유 — 묶음 다섯 · 양극 축척 대칭은 우리 `[재현·대수]` 다 |
| **G10** | **그림 3 'PDE' 곡선의 계산 방법** — 해석식 (22) 를 직접 계산했는지 · 수치(COMSOL 주파수 영역 · 시간 영역 FFT)인지 미인쇄 | 그 곡선이 식 (22) 의 정확한 응답과 다르다(D2) — 원인을 가를 수 없다 |
| **G11** | **'SOC and SOH … error less than 4%' 의 근거 계산** — 추정기 실행 0 · [14] · [31] 은 액체셀 편 | 같은 모형 계열 ASSB 상태 추정 [9](99호)의 9 % · 5 %(OCV 평탄 증폭 편향 — 99호 digest 전사)와 맞지 않는다(D13) |

---

# 보충 자료 — 받은 것 · 대조

**SI 없음 (원문에 보충 언급 0).** 호출자 대조와 같은 결과를 이 실행에서 직접 다시 셌다 — 본문 · 캡션 · 참고문헌 · 약력 전문(NFKC · 줄 끝 분철 복원 뒤)에서 `supplement*` · `supporting information` · `appendix` · `data availab*` · `video` · `movie` · `zenodo` · `github` · `code` **0 회**(본문 `COMSOL` 7 · `MATLAB` 6 — 도구 이름). PDF 안 임베디드 파일 하나("01-Web-res setting-web-IEEE.joboptions")는 Distiller 작업 설정이라 보충 자료가 아니다. 원자료 예치 0 · 코드 0 ⇒ 이 digest 의 재현은 **인쇄 수치 + 벡터 경로 + 우리 재풀이(PDE · ROM) + 91호 digest 전사 값** 네 층뿐이다.

---

# 그림 · 표 — 자동 9 항목 + 수동 8, 실제로 연 것 **17/17**

크로퍼(`wiki/tools/extract_figures.py`)가 본문 그림 1–9 를 `fig_1` … `fig_9` 로 잡았다(SI 판별 ✅ — 파일명 `60._A_reduced-order_electrochemical_model_for_all-solid-state_batteries` 의 `SI_TAG` False · 실행 뒤 이름을 눈으로 확인 · `fig_S…` 0). **표 I–V 는 자동 0**(표 캡션 'TABLE I' … 'TABLE V' 를 못 잡음 — 표 글자가 벡터 글리프). 수동 크롭 8(300 dpi · `*_manual_p*.png` — 파일명의 p 숫자는 PDF 쪽): **표 I–V 단독 다섯 · 그림 2 · 그림 3 단독 · 그림 4 전체**. 자동 크롭 점검(`figures.json` `note` 에 적음 — 자동 파일은 지우지 않았다):

- **과대 둘** — `fig_2`(위쪽에 표 II 의 3차 열 조각 — 왼쪽 열 잘림) · `fig_3`(위쪽에 표 III 왼쪽 조각 + 오른쪽 본문 단 글자) → 그림만 수동 둘 + 표 단독 수동 둘.
- **잘림 하나** — `fig_4`(흐름도 오른쪽 전해질 가지 상자 셋의 오른쪽 반) → 수동 하나.
- **표 누락 다섯** — 표 I–V → 수동 다섯(표 I 은 첫 렌더가 바닥 행 α_neg 를 잘라 영역을 넓혀 다시 렌더).
- **캡션 필드 오염 · 잘림** — `fig_6`(캡션이 '(c) c+' 에서 끊김 — 인쇄 '(c) c_Li⁺ evolution over time.') · `fig_7`(캡션 끝에 바로 아래 표 머리 'TABLE IV' 가 붙음) · `fig_5`('c+ Li' = c_Li⁺ — 아래첨자 순서) — 캡션 원문은 PDF 가 정본.
- 나머지(`fig_1` · `fig_5` · `fig_6` · `fig_7` · `fig_8` · `fig_9`) 라벨 · 내용 온전 · 잘림 0 · 과대 0.

**17 장 전부 이 실행에서 직접 열었다 — 안 본 그림 · 표 0.** (p. 473 사진 여섯은 저자 약력이라 그림이 아니다.) 판독: 그림 2–9 는 전부 **벡터 경로 좌표**(축 프레임 선 · 눈금 선 위치로 보정 — 그림 2 x 338.45–552.95 pt = 10⁻³–10³ rad/s · 크기 y 245.33 = 180 · 313.13 = 60 dB · 위상 357.35 = −45 · 416.63 = −90° / 그림 3 x 78.61–287.77 · 크기 178.78 = 500 · 255.64 = 0 dB · 위상 283.35 = 100 · 351.7 = −100° / 그림 5(d) x 433.27 = 0 · 553.21 = 1400 nm · y 163.39 = 1.5×10⁴ · 241.03 = 0.7×10⁴ / 그림 6(a) x 76.84 = 0 · 289.66 = 2700 s · y 115.48 = 0 · 104.8 = 2C / 그림 7 x 336.9–554.7 = 0–350 s · (a) y 62.08 = 0 · 100.0 = −40 mV · (d) 256.66 = 4.2 · 292.24 = 3.2 V / 그림 8 x 74.04 = 0 · 291.3 = 2700 s · (d) 257.13 = 4.2 · 289.29 = 3.4 V / 그림 9 x 336.77 = 0 · 556.68 = 600 s · y 61.8 = 4.2 · 135.01 = 3.0 V) — 범례 견본 선 · 표지는 상자 좌표로 걸러 냈다. 판독 · 재현 코드 · 렌더 조각은 `scratchpad` 에만(커밋 안 함).

## Fig. 1 — 셀 도식 (p. 465 · 봤다 · 벡터) ★ (b)

Li metal (Anode) | Li₃PO₄ (Solid electrolyte) | LiCoO₂ (Cathode) · x = 0 · x = L_e(전해질) · y = L_p(계면) · y = 0(양극 뒷면) · 방전 중 Li → Li⁺ · Li⁺ → Li_s · Load · 전류 i(왼쪽 화살) · e⁻. 캡션 "reprinted from [9], with permission from Elsevier" ↔ 본문 "which is modified based on the work of Kim et al. [9]" — 99호 그림 1 의 좌표(L · M · y = 0 · 1500 · 1820 nm — 99호 digest 전사)를 전해질 x · 양극 y(계면이 y = L_p) 두 좌표로 바꾼 판(D16). 면적 · 집전체 · 접촉 표시 0.

## Fig. 2 — 양극 전달함수 주파수 응답 (p. 467 · 봤다 · 자동 과대 → 수동 · 벡터 판독) ★★★ (a) · D4

(a) 크기 [dB] · (b) 위상 [deg] · x 'Frequency [rad/s]' 10⁻³–10³ · PDE(검정 실선) · 1st–4th(파랑 □ · 주황 ◇ · 초록 △ · 빨강 ▽). `[도표·벡터]` PDE 곡선 = 정확한 C_Lis(L_p, s)/I(s) = coth(L_p√(s/D))/(F·A·√(sD)) **±0.13 dB · ±0.06°** · 표지 = 표 II(y = L_p 행) Padé **±0.75 dB · ±0.34°**(4차는 표에 없음 — 우리 [3/3] 과 같은 자리 · 범례 표지 제외) · 저주파 170 dB @10⁻³ rad/s = 1/(A·F·L_p·ω) ✅ · PDE 위상 −90° → −45°(≈0.1 rad/s 부터) · 1차 = 순수 적분(−90° 고정). `[재현]` 1 dB · 5° 기준 유효 대역 2차 0.19 · **3차 1.18** · 4차 3.83 rad/s — 그림에서도 3차(초록) 위상이 ≈1 rad/s 부터 PDE 에서 떨어진다. 본문 "90% of the signal power … less than 2.5 Hz [19]. Based on the results of Fig. 2, the third-order transfer function can be selected" — 2.5 Hz = 15.7 rad/s 에서 3차는 −6.1 dB · −40°(D4).

## Fig. 3 — 전해질 전달함수 주파수 응답 (p. 468 · 봤다 · 자동 과대 → 수동 · 벡터 판독) ★★★★ (a) · D2 · D3

같은 꼴 · x = 0 의 C_Li⁺(0, s)/I(s). `[도표·벡터]` **표지는 D_amb = 2D_Li⁺D_n⁻/(D_Li⁺ + D_n⁻) = 1.53×10⁻¹⁵ m² s⁻¹ 로 계산한 표 III Padé** — 1차 위상 −45° @8.19×10⁻³ rad/s → D = L_e²ω/12 = 1.535×10⁻¹⁵ · 1차 · 2차 최적 D 1.553 · 1.542×10⁻¹⁵ · 인쇄 정의 D_e(0.765×10⁻¹⁵) 그대로면 6.5 dB · 19.5° 어긋남(D3). 저주파 152–153 dB = L_e/(4·A·F·D_Li⁺) ✅(D_Li⁺ 0.9×10⁻¹⁵ · A 1 cm²). ★ **PDE 곡선은 식 (22) 의 정확한 응답이 아니다**: | ω (rad/s) | 그림 PDE | 정확(D_amb) | — 10⁻³: 위상 −3.9° ↔ −7.0°(1차 표지 −6.9°) · 10⁻²: 149.9 ↔ 148.1 dB · 위상 −30.1 ↔ −41.8° · 0.1: 142.5 ↔ 137.1 dB · 위상 −11.7 ↔ −45.0° · 1: 142.9 ↔ 127.1 dB · 위상 +60.1 ↔ −45.0° · 10: 167.5 ↔ 117.1 dB · 100: 266.2 ↔ 107.1 dB · 632: **499.3 ↔ 99.0 dB** — 정확한 tanh z/z 응답은 크기가 단조로 줄고(고주파 −10 dB/decade) 위상이 −45° 로 간다(z = √(jωτ) 는 tanh 의 극(순허수)을 지나지 않는다). 그림의 곡선은 10⁻³ 에서 이미 자기 근사식(표지)과 다르고, 위상 −32° 골(≈0.016 rad/s) 뒤 +87°(1.58 rad/s)로 올라갔다가 −77°(2 rad/s) 아래로 떨어져 10–600 rad/s 에서 들쭉날쭉하다. 본문은 이것을 PDE 의 성질로 읽고("The results are a little surprising …") 차수를 골랐다(D2 — 원인 미확정 · G10).

## Fig. 4 — ROM 계산 흐름도 (p. 469 · 봤다 · 자동 잘림 → 수동 전체) ★ (a)

"Start: Set initial SOC, calculate the bulk concentration" → 양극 c_Lis(0, t) · c_Lis(L_p, t) · 전해질 c_Li⁺(0, t) · c_Li⁺(L_e, t)(전달함수) → 벌크 c_Lis,avg(t) · η_ct(t) · 전기장 분포 E(x, t) → Eeq(θ̄(t)) · η_d(t) · η_mt(t) → V_t(t) → "t ≥ t_max" 이면 End · 아니면 "Set: t = t + Δt". **전압 컷오프 판정 상자 0**(G2) · η_ct 상자는 양극 · 전해질 두 갈래를 다 받는다(i₀ 의 c_Li⁺).

## Fig. 5 — 10C 정전류 농도 (p. 469 · 봤다 · 벡터 + 1-bit 마스크) ★★★★ (a) · D3 · D5

(a) c_Lis(y = L_p · y = 0) 시간 (b) 양극 단면 1 · 10 · 50 · 100 · 300 s (c) c_Li⁺(x = 0 · x = L_e) 시간 (d) 전해질 단면 · PDE = 선 · ROM = 표지. `[도표·벡터]` (d) PDE 300 s c(0) 14,592 · c(L_e/2) 10,813 · c(L_e) 7,068 mol m⁻³ · 초기 10,818(= δc₀) · `[재현]` 재풀이(표 I · D_amb · r 항 포함 · 유한체적 120 + 60)가 다섯 시각 다섯 위치에서 **±10 mol m⁻³**(x = L_e 끝 −24 … −38 — 경계 외삽 차) · (b) 양극 단면 −17 … −39 mol m⁻³(일정 오프셋 · 300 s 160 nm 한 점 +557 은 판독 짝짓기 오류로 봄). ROM: (c) 표지 = 우리 3차 Padé(D_amb) 계단 응답 **±50 mol m⁻³**(D_e 면 400–870) · (d) 1 s 표지의 골(≈1.01×10⁴ @≈350 nm) · 마루(≈1.15×10⁴ @≈1,150 nm) 를 포함한 다섯 단면 = 우리 삼차식(식 27 의 둘째 항 **L_e** 꼴) **RMS 2–38 mol m⁻³** — 인쇄 L_e² 꼴이면 3.6×10⁹(D5). 본문 "the concentration distributions approximated by the polynomials have noticeable errors for both cathode and electrolyte at the beginning" ✅ — 1 s 의 S 자 삼차식은 두 끝 기울기 a₁ = −i/(2FAD_Li⁺) 를 강제한 결과다.

## Fig. 6 — UDDS 농도 (p. 470 · 봤다 · 벡터 + 1-bit 마스크) ★★★ (a) · G4

(a) 전류 C-rate — `[도표·벡터]` **2,742 s · UDDS 두 번**(자기상관 지연 1,370 s · r 0.985) · 최대 **+8.65C** · 최소 **−3.88C** · 평균 1.29C · 순 ∫ = 0.979 Q(방전 1.076 · 회생 0.098 Q) (b) c_Lis 1.2 → 2.32×10⁴ + 확대 삽도(1,530–1,700 s — y = L_p 가 y = 0 을 계단처럼 앞섬) (c) c_Li⁺ x = 0 1.08–1.21×10⁴ · x = L_e 0.96–1.05×10⁴. PDE 선(흐린 점선 — 마스크)이 ROM 표지와 거의 겹친다(본문 "remain very close").

## Fig. 7 — 10C 과전압 · 전압 (p. 470 · 봤다 · 벡터) ★★★★ (a) · (b) · 판정 4

(a) η_mt [mV] (b) η_d [V] (c) η_ct,pos [mV] (d) V_t [V] · PDE(파랑) · ROM(빨강 일점쇄선). `[도표·벡터]` PDE η_mt 1.06 s −8.22 · 9 s −12.34 · 50 s −20.76 · 100 s −26.89 · 200 s −34.43 · 300 s −38.35 · 339 s −39.30 mV · η_d 1 s −20.24 · 18 s −47.30(골) · 150 s −22.78 · 255 s −3.33 · 300 s −21.09 · 339 s −426 mV · η_ct 1 s −6.61 · 100 s −3.23 · 300 s −7.60 · 339 s −65.5 mV · V 1 s 4.2524 · 100 s 3.9876 · 200 s 3.8746 · 300 s 3.8173 · 끝 **339.01 s 3.3502 V**. ★ `[재현]` 재풀이(표 I · SOC₀ 1.0 · T 298.15 K · 식 (9) 그대로) — η_mt **±0.05 mV**(1–330 s) · Nernst 항을 빼면 최대 **19.3 mV**(300 s −19.54 ↔ −38.35) · V ±1.4 mV(1–300 s) · η_d ±0.9 mV(≤300 s) · η_ct ±0.2 mV · 3.35 V 도달 339.61 ↔ 339.01 s. ROM η_mt = 우리 ROM(3차 Padé D_amb · 식 27 L_e 꼴 · 식 28 비 꼴 · Nernst 항) ±0.08 mV · ROM − PDE η_mt RMSE 0.38 · 최대 0.67–0.69 mV ↔ 표 IV 0.38 · 0.66 ✅. η_d: ROM 이 t ≈0 에서 +3.4 mV 로 출발해 ≈10 s 에 PDE 와 붙고 끝에서 −362 ↔ −426 mV(≈64 mV — 표 IV 최대 76.3) — 같은 순간 V 차는 표 IV 최대 4.6 mV.

## Fig. 8 — UDDS 과전압 · 전압 (p. 471 · 봤다 · 벡터) ★★★ (a) · D1

(a) η_mt 0 … −14 mV (b) η_d — 끝(≈2,700 s) −210 mV 스파이크 (c) η_ct,pos −13 … +6 mV (d) V_t 4.29 → ≈3.45 V. `[도표·벡터]` ROM − PDE(대시 꼭짓점 기준 — 균일 1 s 아님 · 범례 견본 선은 뺌) V 최대 **36.7 mV @2,722 s** · η_d 최대 **36.0 mV @2,713 s** ↔ 표 IV 40.5 · 35.9 mV — 최대 오차는 방전 끝 몇십 초에 있다(본문 "which occurs at the end of discharge" ✅).

## Fig. 9 — [7] 실험 · PDE · ROM (p. 471 · 봤다 · 벡터) ★★★★ (b) · D11 · D12

6.4 · 12.8 · 25.6C · Experiment(검정 점선 + ■) · PDE(파랑) · ROM(빨강) · 0–600 s · 3.0–4.2 V. `[도표·벡터]` 실험 첫 표지 4.173 · 4.151 · 4.111 V(91호 측정 Q = 0 전압 4.177 · 4.156 · 4.116 V — 91호 digest 전사 ✅) · 실험 점선 끝 **546.4 · 266.6 · 124.2 s**(3.06 · 3.05 · 3.12 V) ↔ 91호 측정 용량 9.86 · 9.76 · 9.57 µAh cm⁻² ÷ (C · 10 µA cm⁻²) = **554.6 · 274.5 · 134.6 s**(×0.985 · ×0.972 · ×0.924) · PDE 끝 **543.1 · 262.1 · 122.0 s** ↔ Danilov 자기 모형선 3.0 V 도달 − 방전 시작 = 541.7 · 257.9 · 121.1 s(91호 digest 전사). `[재현·외부 값]` 표 I + 식 (14) 재풀이는 끝(3.4 V 도달 541.40 · 260.55 · 120.09 ↔ 그림 540.27 · 260.21 · 120.23 s)은 맞추지만 t = 1 s 전압이 +92 · +86 · +74 mV 높다 — **[7] 의 외삽 EMF(91호 전사 11 점 · 선형)로 바꾸면 +2.6 · +1.0 · −2.0 mV · 대부분 ±7 mV**(EMF 보간 마디 근처 ≤22 mV — 6.4C 60 s · 300 s · 25.6C 60 s). PDE − 실험(SOC 100–10 % 창 · 점 배정 뒤) 중앙값 −8.1 · −8.7 · −4.8 mV(6.4 · 12.8 · 25.6C). 본문 "most errors occur at the end of the discharging process" · "batteries are usually operating at the range of 100%–10% SOC. At this range, good agreement" — 창 안의 일치는 그림에 선다(중앙 ≤9 mV) · 끝의 일치는 옮긴 실험 곡선의 끝에 매달린다(D12).

## Table I — 매개변수 (p. 466 · 봤다 · 수동 단독) ★★★★ (b)

머리 "Set of Model Parameters for ASSBs **[9], [27]**" · 열 'Parameters · **Estimated value** · Dimension' · 16 행: A 1 cm² · L_e 1500 nm · L_p 320 nm · c_Li⁺,0 6.01×10⁴ mol m⁻³ · δ 0.18 · **c_Lis,max 2.33×10⁴ · c_Lis,min 1.165×10⁴ mol m⁻³** · D_Lis 1.76×10⁻¹⁵ · D_Li⁺ 0.9×10⁻¹⁵ · **D_n⁻ 5.1×10⁻¹⁵** m² s⁻¹ · k_r 0.9×10⁻⁸ · k_pos 5.1×10⁻⁴ · **k_neg 1×10⁻²** m³ mol⁻¹ s⁻¹ · α_pos 0.6 · **α_neg 0.5**. 없는 것: T(G1). §(b) 1 에 99호 표 1 · 91호 표 II 와 행별 대조.

## Table II — 양극 근사 전달함수 (p. 467 · 봤다 · 수동 단독) ★★★ (a) · (c) · D9

C_Lis(L_p, s)/I(s) · C_Lis(0, s)/I(s) 의 1st(1/(AFL_p s)) · 2nd · 3rd — 3rd(y = L_p) = [1/(AFL_p) + 4L_p s/(9AD_Lis F) + L_p³s²/(63AD_Lis²F)] / [s + L_p²s²/(9D_Lis) + L_p⁴s³/(945D_Lis²)] · 3rd(y = 0) = [1/(AFL_p) − 13L_p s/(396AD_Lis F) + 5L_p³s²/(11088AD_Lis²F)] / [s + 53L_p²s²/(396D_Lis) + 551L_p⁴s³/(166320D_Lis²)]. `[재현·대수]` 모든 계수가 1/(AFL_p) 과 u = L_p²s/D_Lis 로만 쓰이고, √u coth √u · √u / sinh √u 의 [1/1] · [2/2] Padé 와 같다 — 단 y = 0 2차 분자 "+ L_p s/(20AD_Lis F)" 는 −L_p s/(20AD_Lis F) 이어야 한다(D9 — 3차 행은 맞음).

## Table III — 전해질 근사 전달함수 (p. 468 · 봤다 · 수동 단독) ★★★ (a) · (c) · D3

C_Li⁺(0, s)/I(s) 1st L_e/(4AD_Li⁺F(1 + L_e²s/(12D_e))) · 2nd · 3rd = [L_e/(4AD_Li⁺F) + L_e³s/(132AD_eD_Li⁺F) + L_e⁵s²/(31680AD_e²D_Li⁺F)] / [1 + 5L_e²s/(44D_e) + L_e⁴s²/(792D_e²) + L_e⁶s³/(665280D_e³)]. `[재현·대수]` tanh z / z(z² = L_e²s/(4D_e))의 [0/1] · [1/2] · [2/3] Padé 와 같다 — 그러나 그림 3 · 5 의 ROM 은 D_e 자리에 D_amb(= 2D_e)를 썼다(D3).

## Table IV — 과전압 · 전압 오차 통계 (p. 470 · 봤다 · 수동 단독) ★★★★ (a) · D1

RMSE · MaxAE(mV) — 10C: η_mt 0.38 · 0.66 · η_d 6.60 · **76.30** · η_ct,pos(α = 0.5) 0.48 · 5.60 · η_ct,pos(α = 0.6) 0.06 · 0.68 · V_t **0.54 · 4.60** / UDDS: η_mt 0.12 · 0.53 · η_d 2.90 · 35.90 · η_ct,pos(α = 0.5) 0.09 · 2.10 · (α = 0.6) 0.08 · 1.80 · V_t **2.60 · 40.5**. 두 α 행의 정의 미인쇄(G7).

## Table V — 모형별 정확도 · 계산 시간 (p. 472 · 봤다 · 수동 단독) ★★★ (a)

조건(지속) 1C(3574 s) · 2C(1777) · 5C(699) · 10C(340) · UDDS(2742) × COMSOL 실행 11 · 6 · 3 · 2 · 104 s / 원 PDE(MATLAB) 1.64 · 0.84 · 0.40 · 0.25 · 1.21 s · RMSE 0.08 · 0.14 · 0.19 · 0.23 · 0.50 mV / 단순 PDE(MATLAB · r 무시) 0.87 · 0.50 · 0.27 · 0.17 · 0.68 s · 0.24 · 0.41 · 0.46 · 0.50 · **2.20** / ROM(MATLAB) 0.44 · 0.23 · 0.11 · 0.07 · 0.34 s · 0.24 · 0.41 · 0.48 · 0.54 · **2.60** mV. `[재현]` 단계당(Δt 1 s) 0.123 · 0.129 · 0.157 · **0.206** · 0.124 ms(D14) · ROM ÷ 단순 PDE 실행 시간 0.41–0.51(본문 "around half" ✅) · 지속/명목(3600/C) 0.993 · 0.987 · 0.971 · 0.944. ★ UDDS 에서 단순 PDE(r 무시 · 유한차분)가 이미 2.20 mV — ROM 의 2.60 중 큰 몫이 축약(Padé · 다항식) 전 단계에 있다(`[재현·가정]` 독립 가정 제곱합으로 r 무시 몫 ≈2.1 · 축약 몫 ≈1.4 mV).

## 본문 서술과 어긋난 그림 · 표 (요약)

| 자리 | 서술 | 그림 · 표 | 판정 |
|---|---|---|---|
| 초록 "less than 2.6 mV" ↔ 표 IV | 오차 < 2.6 mV | UDDS RMSE 2.60 · MaxAE 40.5 · 10C MaxAE 4.6 | ❌ 지표 탈락(D1) |
| 본문 "magnitude … diverges … phase … oscillates" ↔ 그림 3 | PDE 의 성질 | 식 (22) 정확 응답은 단조 · −45° 수렴(10⁻³ 에서 이미 −3.9 ↔ −7.0°) | ❌ 계산 산물(D2) |
| 식 (21) · 표 III D_e ↔ 그림 3 · 5 | D_Li⁺D_n⁻/(D_Li⁺ + D_n⁻) | 그림은 2D_e(1.535×10⁻¹⁵) | ❌ 정의에 2 빠짐(D3) |
| 본문 "less than 2.5 Hz … Based on the results of Fig. 2 … third-order" ↔ 그림 2 | 3차로 충분 | 3차 위상이 ≈1 rad/s 부터 이탈 · 2.5 Hz 에서 −40° | ⚠ 기준 미달(D4) |
| 식 (27) · (28) ↔ 그림 5(d) · 7(a) | 인쇄 꼴 | 고친 꼴로만 닫힘(RMS 2–38 · ±0.08 mV) | ❌ 오기(D5 · D6) |
| "the same model parameters in the reference" ↔ 그림 9 | 같은 매개변수 | 식 (14) 로는 시작 +74 … +92 mV · [7] EMF 로 ±7 mV | ⚠ 평형 곡선 교체 미인쇄(D11) |
| 그림 9 'Experiment' 끝 ↔ [7] 측정 용량(91호 전사) | [7] 자료 | ×0.985 · 0.972 · 0.924 | ⚠ 끝이 짧음(D12) |
| "calculation time … per step is within 0.2 ms" ↔ 표 V | ≤0.2 ms | 10C 0.206 ms | ⚠ 반올림(D14) |
| "SOC decreases from 100% to 0%" ↔ 그림 7 · 6 | 0 % 까지 | 3.35 V 에서 0.057 · UDDS 끝 0.021(`[재현]`) | ⚠ 문장(D15) |
| 그림 1 캡션 "reprinted" ↔ 본문 "modified" | — | 좌표 이름 바뀜 | ⚠ 표기(D16) |

---
# 절별 해체 (본문)

## 초록 · I. Introduction (p. 464–465)

`[인쇄]` 동기: 액체 LIB 의 열 폭주 → ASSB("better thermal stability, longer cycle life, and higher energy density [3], [4]") · 박막 ASSB 1D 모형 계보 다섯 — [7] Danilov("1-D mathematical model for the thin-film solid-state battery Li|Li3PO4|LiCoO2 … Butler–Volmer … Fick's second law … Nernst–Planck") · [10] Fabre("further simplify the abovementioned model to reduce the number of model parameters and use the galvanostatic intermittent titration technique and electrochemical impedance spectroscopy to identify some model parameters. Finally, the model is validated under galvanostatic and potentiostatic conditions") · [8] Kazemi("fit the diffusion coefficient as a function of lithium-ion concentration … high accuracy even at a current density of 5 mA/cm2") · [11] Raijmakers("double-layer capacitance … ion migration process in the cathode … geometric capacitance … high accuracy in both time and frequency domains") · "the potential in the anode is assumed to be uniform and equal to 0 V [7], [9]". 문제: "numerical methods require a lot of computing sources and are difficult to run in real time" · 상태(SOC [9], [12] · SOH [13], [14] · SOP [15]) 추정에 정확한 모형이 필요 · 액체 LIB 축약 방법 목록(Laplace [19], [20] · residue grouping [21] · Padé [22], [23] · polynomial [18], [24] · DRA [25]) · ASSB 는 [9] 하나: "Kim et al. [9] simplify the PDE-based model by assuming the charge transfer coefficient equal to 0.5 and ignoring the diffusion dynamics of the electrolyte, and a set of ordinary differential equations (ODEs) is used to implement the extended Kalman filter algorithm. This study ignores the unimportant components of the model but does not convert the complex PDEs into control-oriented model forms, such as transfer functions." — 99호의 SOC 오차(9 % · 5 %)와 '약한 관측성'(99호 digest 전사)은 소개하지 않는다. 기여 = "a series of sophisticated approximation methods from the conventional lithium-ion battery field is employed to obtain a reduced-order model (ROM) for ASSBs, and a better tradeoff is made between model fidelity and computational complexity." 서론에 식별성 · 관측성 · 열화 낱말 0.

## II. PDE-Based Model (p. 465–466 · 그림 1 · 표 I · 식 1–16)

`[인쇄]` "the variables x and y are defined in the regions of electrolyte and cathode, respectively" · (1) ∂c_Lis/∂t = D_Lis ∂²c_Lis/∂y² · 경계 D_Lis ∂c_Lis(L_p, t)/∂y = i(t)/(FA) · ∂c_Lis(0, t)/∂y = 0 ("i is the load current with a positive sign for the discharging process") · (2) Nernst–Planck J_j = −D_j ∂c_j/∂y − (z_jF/RT)D_jc_jE(전해질인데 ∂/∂y — D17) · (3) ∂c_Li⁺/∂t = −∂J_Li⁺/∂y + r · (4) **r = δ²k_r c_Li⁺,0(c_Li⁺,0 − c_Li⁺)/(1 − δ) − k_r c²_Li⁺** — `[재현·대수]` r(δc₀) = 0 ✅(99호 식 (8) γ 의 c₀ 하나 빠짐(99호 D5)이 여기서는 맞게 인쇄됨) · (5) ∂c_Li⁺/∂t = [2D_Li⁺D_n⁻/(D_Li⁺ + D_n⁻)] ∂²c_Li⁺/∂x² + r · c(x, 0) = δc_Li⁺,0 · 두 끝 ∂c/∂x = −i(t)/(2FAD_Li⁺) · "δ is the fraction of free Li in equilibrium" · (6) i = i₀(e^{αFη_ct/RT} − e^{(1−α)Fη_ct/RT})(둘째 지수의 − 부호 빠짐 — D10) · (7) **i₀,pos = −FAk_pos[(c_Lis,max − c_Lis)c_Li⁺/((c_Lis,max − c_Lis,min)c_Li⁺,0)]^α_pos [(c_Lis − c_Lis,min)/(c_Lis,max − c_Lis,min)]^(1−α_pos)**(앞 − 부호 — 음의 교환 전류 관례 · 99호 식 (16)–(17) 은 BV 앞에 −) · (8) i₀,neg = FAk_neg(c_Li⁺/c_Li⁺,0)^α_neg · (9) **η_mt = (RT/F) ln[c_Li⁺(L_e, t)/c_Li⁺(0, t)] − ∫₀^{L_e} E(x, t)dx**("can be calculated as follows [26]") · (10) E = (RT/F)(1/c)[i/(2FAD_Li⁺) + ((D_Li⁺ − D_n⁻)/(D_Li⁺ + D_n⁻))(∂c/∂x + i/(2FAD_Li⁺))]("an analytical expression … is derived [26]") · (11) η_d = Eeq(θ_s) − Eeq(θ̄)("[7], [9]") · (12) θ_s = c_Lis(L_p, t)/c_Lis,max · θ̄ = c_Lis,avg/c_Lis,max · (13) 평균 · "The nonlinear function Eeq is fit from experimental data and expressed as [10] (14)" — (14) Eeq(θ) = (−219.027 + 322.003θ² − 198.242θ⁴ + 354.911θ⁶ − 467.807θ⁸ + 207.168θ¹⁰)/(−44.337 + 36.643θ² − 3.430θ⁴ + 113.081θ⁶ − 182.567θ⁸ + 80.3097θ¹⁰)(99호 식 (22) 와 같은 계수 · 99호는 "[11]" = 같은 Fabre) · (15) SOC = (c_Lis,max − c_Lis,avg)/(c_Lis,max − c_Li,min)(분모 'c_Li,min' — D17) · (16) V_t = Eeq(θ̄) + η_d + η_ct,pos − η_ct,neg + η_mt = Eeq(θ_s) + η_ct,pos − η_ct,neg + η_mt · "In this article, a complete set of model parameters obtained from a thin-film ASSB is used and listed in Table I. The validity of the parameters has been verified by many existing references [7], [9], [27]."

## III. Reduced-Order Model Derivation (p. 466–469 · 표 II · III · 그림 2–4 · 식 17–29)

**A. 양극.** `[인쇄]` (17) sC_Lis − D_Lis ∂²C_Lis/∂y² = 0 · "The Laplace transform does not change its boundary conditions" · (18) C_Lis(y, s)/I(s) = exp(β(L_p − y))(1 + exp(2βy))/(AFβ√D_Lis(−1 + exp(2L_pβ))) · β = (s/D_Lis)^{1/2} · (19) C_Lis(0, s)/I(s) = 2exp(2L_pβ)/(AFβ√D_Lis(−1 + exp(2L_pβ))) · (20) C_Lis(L_p, s)/I(s) = (1 + exp(2L_pβ))/(AFβ√D_Lis(−1 + exp(2L_pβ))). `[재현·대수]` 경계값 문제를 다시 풀면 C(y, s)/I = cosh(βy)/(F·A·D_Lis·β·sinh(βL_p)) — 분자는 (18) 과 같고 분모는 **AFD_Lisβ(= AF√(sD_Lis))** 다; 인쇄 'AFβ√D_Lis' 는 √D_Lis 가 하나 모자라 차원이 맞지 않는다(D7) · (19) 분자는 (18) 에 y = 0 을 넣으면 2exp(L_pβ)(인쇄 2exp(2L_pβ) — D8). 표 II · 그림 2 는 맞는 꼴의 값이다(저주파 1/(AFL_p s) · R2). "However, the above equations are transcendental transfer functions with infinite differentiability … the Padé approximation method [22], [23] is employed … The coefficients of the transfer functions can be explicitly derived from the electrochemical parameters." · 차수: "only higher-order transfer functions can maintain accurate responses at higher frequencies. For vehicle applications, 90% of the signal power of typical driving cycles have frequencies of less than 2.5 Hz [19]. Based on the results of Fig. 2, the third-order transfer function can be selected" · "so only the response at y = L_p is analyzed and the order of transfer function at y = 0 can be chosen as the same as y = L_p."

**B. 전해질.** `[인쇄]` "Since the r term in (5) is a quadratic function of the Li⁺ ion concentration, the diffusion dynamics in the electrolyte become nonlinear. To derive an analytical solution for (5), the contribution of the r term is ignored to obtain a linear PDE similar to (1). The results of [9] suggest that ignoring the r term will not cause a large voltage error in the considered models." · (21) C_Li⁺(x, s)/I(s) = (exp(γ(L_e − x)) − exp(xγ))/(2AFγD_Li⁺(1 + exp(L_eγ))) · **γ = (s/D_e)^{1/2}, D_e = D_Li⁺D_n⁻/(D_Li⁺ + D_n⁻)** · (22) C_Li⁺(0, s)/I(s) = (exp(γL_e) − 1)/(2AFγD_Li⁺(1 + exp(L_eγ))) = −C_Li⁺(L_e, s)/I(s). `[재현·대수]` 식 (5)(r 없음)의 해를 다시 풀면 (21) 의 꼴이 그대로 나오되 γ² = s/(**2**D_Li⁺D_n⁻/(D_Li⁺ + D_n⁻)) 이다 — 인쇄 D_e 정의에 2 가 빠졌다(D3 · 그림은 2 를 넣은 값). "The results are a little surprising. The magnitude response of the PDE-based model diverges as the frequency increases, and its phase response oscillates at high frequencies. To obtain a high-accuracy model with a low computational cost, the third approximate transfer function is finally selected after comprehensively considering the magnitude and phase responses."(D2)

**C. 단자 전압.** `[인쇄]` (23) c_Lis(y, t) = a₀ + a₁y + a₂y² · (24) a₀ = c_Lis(0, t) · a₁ = 0 · a₂ = i/(2FAL_pD_Lis) · (25) c_Lis,avg = iL_p/(6FAD_Lis) + c_Lis(0, t)(`[재현·대수]` ✅) · "its boundary conditions at two ends are identical, which will result in a quadratic coefficient equal to zero when the concentration is assumed to follow a parabolic distribution. For high accuracy, the concentration distribution across the electrolyte is assumed to be a cubic curve" · (26) c_Li⁺ = a₀ + a₁x + a₂x² + a₃x³ · (27) a₀ = c_Li⁺(0, t) · a₁ = −i/(2FAD_Li⁺) · a₂ = 3(c_Li⁺(L_e, t) − c_Li⁺(0, t))/L_e² + 3i/(2L_e²FAD_Li⁺) · a₃ = −2a₂/(3L_e) — `[재현·대수]` 두 끝 기울기 · 끝값에서 a₂ = 3(c(L_e) − c(0))/L_e² + 3i/(2**L_e**FAD_Li⁺)(인쇄 L_e² 는 차원 불일치 — D5) · (28) E(x, t) = (RT/F)[D_e(3a₃x² + 2a₂x) − a₁]/(a₀ + a₁x + a₂x² + a₃x³) — `[재현·대수]` 식 (10) 에 (26)–(27) 을 넣으면 D_e 자리는 (D_Li⁺ − D_n⁻)/(D_Li⁺ + D_n⁻)(D6) · "Although the integral of (28) has no analytical solution, numerical integration methods (such as the trapezoidal integration) can be used" · (29) η_ct = (2RT/F) asinh(i/(2i₀))(α_neg 0.5) · "when the coefficient α_pos is not equal to 0.5, the charge transfer overpotential of the positive electrode η_ct,pos cannot be directly calculated and needs a root-finding method … α_pos is assumed to be 0.5, and the errors due to this assumption will be evaluated" · 흐름도(그림 4) · "it is assumed that the battery is in steady-state, so the Li⁺ ion concentration is uniform across the cathode and can be calculated from the specified initial SOC."

## IV. Results and Analysis (p. 469–471 · 그림 5–9 · 표 IV · V)

`[인쇄]` "the original PDE-based model is simulated by the commercial software COMSOL Multiphysics 5.4a … The accuracy of COMSOL simulations has been verified by many researchers [8], [9], [18], [25], [29], [30], and the simulation results can be used as a benchmark for comparative analysis." · "A personal computer (Intel Core i7-8565U CPU 1.8 GHz and 7.85-GB RAM available) is used to simulate these models with the sampling period set to 1 s." · "the voltage responses of experimental data under three large C-rates are also presented to validate the accuracy of the models."

**A. 농도.** 그림 5(10C) · 그림 6(UDDS) — "The third-order transfer functions can effectively estimate the evolutions of concentrations over time, and the errors are negligible both for the cathode and electrolyte. Compared with the electrolyte, the concentration variation of the cathode in the region is not obvious because it has a small thickness but a large diffusion coefficient."(`[재현]` 확산 시간 L_p²/D_Lis 58.2 s ↔ L_e²/D_amb 1,471 s — 차이는 두께에서 온다: D_Lis 1.76 ↔ D_amb 1.53×10⁻¹⁵) · "the concentration distributions approximated by the polynomials have noticeable errors for both cathode and electrolyte at the beginning … as time goes by, the errors decrease quickly" · "The current profile of the UDDS cycle is extracted from a commercial electric vehicle and is then scaled down for the battery."

**B. 과전압 · 전압.** 그림 7 · 표 IV(10C) — "In this discharge process, the battery SOC decreases from 100% to 0%. Since the charge transfer overpotential of the negative electrode is much smaller (lower than 0.1 mV), its results are not compared." · "the diffusion overpotential has a larger error than other overpotentials, its root-mean-square error (RMSE) reaches 6.6 mV, and its maximum absolute error (MaxAE) is about 76.3 mV at the end of discharge … The additional error by assuming α = 0.5 is insignificant; thus, the time-consuming root-finding method can be replaced by the inverse hyperbolic sine function. The terminal voltage … its RMSE is only 0.54 mV, and its MaxAE is only 4.6 mV. It should be noted that the error of diffusion overpotential is much larger than the error of voltage, and it mainly occurs at the end of the discharge process. At that time, the equilibrium potential decreases sharply and causes a large error in the diffusion overpotential." — `[해석]` 그 설명(평형 전위가 가파르다)은 η_d 오차의 크기를 말하고, 그것이 전압에 안 나오는 이유(V 는 θ_s 만 본다 — 식 16 둘째 줄)는 말하지 않는다. 그림 8 · 표 IV(UDDS) — "The RMSE of voltage is only 2.6 mV, and the MaxAE of voltage is about 40.5 mV, which occurs at the end of discharge … the approximated concentration distributions have larger errors under transient excitations … The inaccurate concentration distribution of the cathode causes a large error in the equilibrium potential and, finally, leads to a larger voltage error." · "By comparing the states estimation results in the literature [14], [31], it can be found that by using the proposed ROM and mature model-based algorithms, the SOC and SOH can be obtained with an error less than 4%, which can meet the requirement of practical applications." · 그림 9 — "the voltage responses of experimental data, the PDE-based model, and the ROM under three large C-rates (6.4, 12.8, and 25.6 C) … The experimental data come from [7], and the same model parameters in the reference are also used in this article. It can be found that the outputs of the PDE-based model and the ROM are very close to the measurement data of the real battery, and most errors occur at the end of the discharging process. For practical applications, batteries are usually operating at the range of 100%–10% SOC. At this range, good agreement with the experimental results can be observed for both the PDE-based model and the ROM."

**C. 성능.** 표 V — "The original PDE-based model is solved by COMSOL and MATLAB … by ignoring the r term, a simplified PDE-based model can be obtained … By using the finite difference method to discretize (1) and the simplified (5), a set of ODEs can be derived and can be easily solved by ode45 in MATLAB. The mesh is set as normal by default for COMSOL, while the number of discretization is set to 10 both in cathode and electrolyte for MATLAB. For the proposed ROM, the PDEs are reduced to transfer functions and polynomial functions, which makes it a lumped-parameter model." · "ignoring the r term can reduce the computational time but also reduce the model accuracy. It is noted that the ROM can obtain an accuracy comparable to the simplified PDE-based model, and its computational time is around half of the latter one. Besides, for the analytical solutions (ROM), mature frequency-domain analysis methods can be used … such as power prediction and charging optimization. Since the simulation timestep is set to one second for ROM, its calculation time per step is within 0.2 ms."

## V. Conclusion (p. 472)

`[인쇄]` "By analyzing the frequency response of the transfer functions, a third-order Padé approximation is chosen to achieve better accuracy with a low computational cost." · "The errors of the concentrations over time are negligible, and only a few errors exist for the concentration distributions at transient excitations. The RMSE of voltage under 10-C discharge condition and the dynamic UDDS cycle are only 0.54 and 2.6 mV, respectively. Besides, compared with the voltage response of experimental data, a good agreement can be observed for the ROM under three large C-rates discharging conditions. Based on a regular laptop, the calculation time of ROM per step is within 0.2 ms. These results demonstrate that the proposed ROM in this article has high computational efficiency and provides excellent prediction accuracy; therefore, it can be applied to an embedded BMS for real-time applications." — 결론은 'RMSE' 를 적는다(초록과 다름 — D1). 미래 과제 문장 0 · 한계 문장 0.

---
# ★ (a) 축약 단계 — Laplace → Padé → 다항식 · 오차의 조건

## 1. 단계별 — 인쇄 근거 ↔ 우리 재현

| 단계 | 인쇄 근거 | `[재현]` | 판정 |
|---|---|---|---|
| ① Laplace 해 (식 17–22) | 경계값 문제의 닫힌 해 · "The Laplace transform does not change its boundary conditions" | 양극 C(y)/I = cosh(βy)/(F·A·D_Lis·β·sinh βL_p) · 전해질 tanh(γL_e/2)/(2F·A·D_Li⁺·γ) — 인쇄 식은 (18)–(20) 분모 √D 하나 모자람 · (19) 분자 지수 · (21) D_e 정의(2 빠짐) 세 자리가 다르고, 표 · 그림은 맞는 꼴 | ✅ 방법 · ⚠ 인쇄 오기 셋(D3 · D7 · D8) |
| ② Padé (표 II · III) | "low-order and fractional transfer functions" · 계수가 매개변수에서 바로 나온다 | 기호 계산(`sympy`) — 표 II 의 [1/1] · [2/2](두 끝) · 표 III 의 [0/1] · [1/2] · [2/3] 계수 전부 일치 · y = 0 2차 분자 부호 하나 오기 | ✅(D9 하나) |
| ③ 차수 선택 (그림 2 · 3) | 양극: 2.5 Hz 기준[19] + 그림 2 · 전해질: "a little surprising … diverges … oscillates" → "comprehensively considering" 3차 | 3차 유효 대역(1 dB · 5°) 양극 1.18 rad/s(0.19 Hz) · 전해질 0.35 rad/s(0.056 Hz) · 4차 3.83 · 0.98 rad/s · 2.5 Hz 에서 3차 −6.1 dB · −40° / −11.2 dB · −43.5° · Δt 1 s Nyquist(π rad/s)에서 −23° / −4.3 dB · −38° · 그림 3 PDE 곡선 ≠ 식 (22) | ❌ 근거 그림 · 기준이 3차를 받치지 않는다(D2 · D4) — 다만 실행이 Δt 1 s 라 쓸 수 있는 대역 자체가 0.5 Hz 아래다 |
| ④ 양극 포물선 (식 23–25) | a₁ = 0 · a₂ = i/(2FAL_pD_Lis) · c_avg = c(0) + iL_p/(6FAD_Lis) | 대수 ✅ · 준정상(포물선)은 확산 시간 L_p²/D_Lis 58.2 s(첫 모드 5.9 s) 뒤에만 맞다 — 그림 5(b) 1 s · 10 s 단면 오차 · 표 IV η_d 최대 76.3 mV(방전 끝) | ⚠ 벌크 θ̄ 의 오차가 η_d 에만 남는다(아래 3) |
| ⑤ 전해질 삼차식 (식 26–28) | 두 끝 경계가 같아 포물선은 2차 계수 0 → 삼차 · E 는 사다리꼴 적분 | 그림 5(d) ROM = 식 (27) L_e 꼴(RMS 2–38 mol m⁻³) · 그림 7(a) ROM η_mt = 식 (28) 비 꼴 + Nernst 항(±0.08 mV) | ✅ 계산 · ❌ 인쇄 오기 둘(D5 · D6) |
| ⑥ α_pos 0.5 (식 29) | 근 찾기 대신 asinh — "errors … will be evaluated" | 표 IV 10C η_ct 최대 5.60(α 0.5) ↔ 0.68 mV(α 0.6) · UDDS 2.10 ↔ 1.80 | ⚠ 'insignificant' 의 기준 미인쇄(G7) · 99호 표 2 모형 3(r 무시 + α 0.5) 10C 최대 23.3 mV(99호 digest 전사)보다 작다(끝 시각 · 컷오프 차) |
| ⑦ r 항 무시 (식 5 → 21) | "The results of [9] suggest that ignoring the r term will not cause a large voltage error" | 10C r 항 제거 오차 RMS · 최대: k_r 0.9×10⁻⁸(인쇄) 0.40 · 0.75 → 0.9×10⁻⁷ 3.47 · 6.41 → 8.0×10⁻⁷(98호 값) 14.22 · 23.12 → 0.9×10⁻⁶(91호 그림 일치) **14.85 · 23.94 mV** · 표 V 단순 PDE RMSE 0.24–0.50(정전류) · 2.20(UDDS) | ⚠ 인쇄 k_r 에서만 싸다(91호 ×100 문제 상속) — 99호 결론을 조건 없이 재인용(D-냐) |

## 2. '2.6 mV' 의 조건 (`[인쇄]` 표 IV · V · 본문 → `[도표·벡터]` · `[재현]`)

| 축 | 값 |
|---|---|
| 지표 | **RMSE**(초록은 'errors … less than' — D1) · 같은 행 MaxAE 40.5 mV · 표본 시각 · 개수 미인쇄 |
| 비교 대상 | ROM(MATLAB · Δt 1 s) ↔ 원 PDE(COMSOL 5.4a · 메시 'normal') — **같은 매개변수 한 벌**(표 I) · 같은 평형 곡선(식 14) — 매개변수의 옳고 그름은 이 오차에 안 들어간다 |
| 프로파일 | UDDS **두 번**(2,742 s) · 축척: `[도표·벡터]` −3.88 … +8.65C · 평균 1.29C · 순 0.979 Q · 축척 방법 미인쇄(G4) |
| 초기 · 끝 | SOC₀ 1.0(`[재현]` — G2) · 끝 = 시간 2,742 s(컷오프 판정 0 · 끝 SOC ≈0.02) |
| 오차의 자리 | `[도표·벡터]` V 최대 36.7 mV @2,722 s · η_d 최대 36.0 mV @2,713 s — 방전 끝 몇십 초(본문 "which occurs at the end of discharge" ✅) |
| 오차의 성분 | 표 V: 원 PDE(MATLAB) 0.50 · 단순 PDE(r 무시) **2.20** · ROM 2.60 mV — `[재현·가정]` 독립 오차 제곱합으로 r 무시 몫 ≈2.1 · 축약 몫 ≈1.4 mV(정전류 10C 는 0.44 · 0.20 mV) |
| 10C 판 | RMSE 0.54 · MaxAE 4.60 mV(표 IV) · η_d RMSE 6.60 · MaxAE **76.30** mV |

## 3. ★ 출력이 맞는다 ≠ 성분이 맞다 — V 는 θ_s 만 본다 (`[재현·대수]` → `[해석]`)

식 (16) 의 두 줄은 같은 식이다: Eeq(θ̄) + η_d = Eeq(θ̄) + [Eeq(θ_s) − Eeq(θ̄)] = Eeq(θ_s). 그래서 **전압에는 양극 표면 농도 θ_s 와 η_ct · η_mt 만 들어가고, 벌크 θ̄(= SOC — 식 15)는 들어가지 않는다.** ROM 에서 θ̄ 는 포물선 가정(식 25)으로 따로 계산되고 그 오차는 η_d 와 Eeq(θ̄) 에 같은 크기 반대 부호로 나뉘어 상쇄된다. 그래서 같은 10C 실행에서 V 최대 오차 4.6 mV 와 η_d 최대 오차 76.3 mV 가 함께 선다(표 IV). `[해석]` 우리 축으로 옮기면 — **전압 곡선을 4.6 mV 로 맞춘 모형도 그 전압의 성분 분해(확산 과전압 ↔ 평형 전위 ↔ SOC)는 76 mV 어긋날 수 있다.** 본문은 이 차이를 "the equilibrium potential decreases sharply" 로 설명한다 — 크기의 이유는 맞지만 전압에 안 보이는 이유(관측 사상)는 말하지 않는다. 같은 구조가 우리 `degradation-degeneracy/` 의 물음("곡선이 맞는다 ≠ 매개변수 · 분해가 맞다")의 모형 층 표본이다(우리 쪽 수치는 `RESULTS*.md` 정본 — 옮기지 않음).

## 4. 재풀이 폐합 (`[재현]` — 우리 수치 풀이 · 저자 코드 아님 · 스크립트는 scratchpad)

입력: 표 I 그대로 · T 298.15 K · SOC₀ 1.0 · 1C = F·A·L_p·(c_max − c_min)/3600 = **9.9916 µA** · i₀ = 식 (7) 수치(A m² · c_Li⁺/c_Li⁺,0 의 분모 = 총 농도 6.01×10⁴ — 99호 R8 관례) · 전해질 유한체적 120 칸 · 양극 60 칸 · BDF · **η_mt = 식 (9) 그대로(Nernst 항 포함)**.

| 시각(10C) | V 재풀이 ↔ 그림 7(d) | η_mt ↔ 그림 7(a) | η_d ↔ 그림 7(b) | η_ct ↔ 그림 7(c) |
|---|---|---|---|---|
| 1.06 s | 4.2522 ↔ 4.2524 | −8.27 ↔ −8.22 | −20.64 ↔ −20.25 | −6.77 ↔ −6.61 |
| 10 s | 4.2026 ↔ 4.2019 | −12.65 ↔ −12.65 | −44.50 ↔ −43.90 | −4.58 ↔ −4.36 |
| 50 s | 4.0943 ↔ 4.0939 | −20.76 ↔ −20.75 | −44.91 ↔ −44.76 | −3.62 ↔ −3.51 |
| 100 s | 3.9889 ↔ 3.9876 | −26.86 ↔ −26.90 | −35.47 ↔ −34.62 | −3.43 ↔ −3.23 |
| 200 s | 3.8737 ↔ 3.8746 | −34.37 ↔ −34.42 | −10.65 ↔ −10.09 | −3.97 ↔ −3.93 |
| 300 s | 3.8188 ↔ 3.8174 | −38.30 ↔ −38.35 | −21.34 ↔ −21.04 | −7.54 ↔ −7.59 |

3.35 V 도달 339.61 ↔ 그림 끝 339.01 s(3.3502 V) · 320–338 s 의 가파른 끝은 수 mV–수십 mV 차(끝의 기울기 · 판독 시각 차). **Nernst 항을 빼면** η_mt 1 s −7.02 · 100 s −14.73 · 300 s −19.54 mV(그림과 최대 19.3 mV) — 그 값들은 99호 그림 3 의 η_mt(1 · 100 · 300 s −6.99 · −14.73 · −19.55 — 99호 digest 전사)와 같다. ⇒ **같은 모형 · 같은 표의 두 편이 η_mt 를 다르게 계산했다 — 99호는 식의 둘째 항만, 이 편은 식 그대로.** SOC₀ 0.995 · 0.99 로 돌리면 η_mt 는 같고 V 끝이 15.6 · 44.8 mV 어긋난다(SOC₀ 1.0 이 그림의 출발점).

---

# ★ (b) 실험 대조 · 매개변수 출처 — 99호에서 무엇을 물려받았나

## 1. 표 I 행별 — 출처 층위 (`[인쇄]` 표 I ↔ 99호 표 1 · 91호 표 II(digest 전사) ↔ 이 편 그림이 요구하는 값(`[재현]`))

| 행 | 표 I(이 편) | 99호 표 1 | 91호 표 II(층위) | 그림이 요구하는 값 | 판정 |
|---|---|---|---|---|---|
| A · L_e · L_p | 1 cm² · 1500 · 320 nm | 같음 | 같음 · 설계 | 같음(그림 5 · 7) | 설계값 상속 |
| c_Li⁺,0 · δ | 6.01×10⁴ · 0.18 | 같음 | NDP 측정 · 적합 | 그림 5(d) 초기 10,818 = δc₀ ✅ | 상속 |
| c_Lis,max · c_Lis,min | **2.33×10⁴ · 1.165×10⁴** | 미인쇄(99호 G1) | a_max 2.33×10⁴ — 용량 맞춤 유도 | SOC₀ 1.0 출발 · 그림 5(a)(b) 초기 ≈1.165–1.19×10⁴ | ✅ 채움(= 91호 a_max · a_max/2) |
| D_Lis | 1.76×10⁻¹⁵ | 같음 | 적합 | 그림 7 η_d · V ±0.9 · ±1.4 mV | 상속 |
| D_Li⁺ | 0.9×10⁻¹⁵ | 같음 | 적합 | 그림 3 직류 이득 152–153 dB · 그림 5 | 상속 |
| **D_n⁻** | **5.1×10⁻¹⁵** | 2.1(그림은 5.1 — 99호 D2) | 5.10×10⁻¹⁵ | 그림 7(a) η_mt ±0.05 mV · 그림 3 D_amb 1.535×10⁻¹⁵ | ✅ 고침 |
| k_r | 0.9×10⁻⁸ | 같음 | 적합 — 91호 재풀이: Danilov 자기 그림은 ×100 | 그림 7(a) 가 인쇄 값으로 닫힘(×100 이면 η_mt(300 s) −18.6 ↔ 그림 −38.35) | ⚠ 상속 — ROM 의 r 무시가 여기 걸림 |
| k_pos | 5.1×10⁻⁴ m³ mol⁻¹ s⁻¹ | 같음 | k₁ˢ 5.1×10⁻⁶ m^2.8 mol^−0.6 s⁻¹ | 식 (7) F·A·k_pos 수치(A m²)로 그림 7(c) η_ct ±0.2 mV | ⚠ 상속(×100 · 단위 · 차원 — 99호 D3 · D4) |
| **k_neg · α_neg** | **1×10⁻² m³ mol⁻¹ s⁻¹ · 0.5** | 없음(음극 무시) | 음극 동역학 "for convenience" 무시 | `[재현]` i₀,neg 수치 0.041 → η_ct,neg 10C 0.05–0.06 mV(인쇄 "lower than 0.1 mV" ✅) | 새 값 · 출처 미인쇄(G8) |
| α_pos | 0.6 | 같음 | 적합 | 그림 7(c) ±0.2 mV | 상속 |
| T | 미인쇄 | 미인쇄 | 25 ℃ 측정 | 298.15 K 로 닫힘 | 공백 그대로(G1) |
| 평형 곡선 | 식 (14) — **[10] Fabre** | 식 (22) — [11] Fabre(같은 계수) | 같은 셀 네 율 외삽 EMF | 그림 5–8: 식 (14) ✅ · **그림 9: [7] EMF**(±7 mV · 식 14 면 +74 … +92 mV) | ⚠ 한 지면에 두 곡선 · 표기 0(D11) |
| 머리 출처 | "[9], [27]" | "[15]"(= Tian & Qi) | — | — | 99호 표의 출처 번호 문제를 '[9] + Tian & Qi' 로 옮김 |

## 2. 99호에서 나온 것 — 물려받았나 (`[재현]` · 99 · 91호 digest 전사)

| 99호에서 나온 것 | 이 편 | 판정 |
|---|---|---|
| 그림의 '전체 모형' 은 인쇄 식 (14) 의 Nernst 항 없이 계산됨(99호 D1) | 원 PDE(COMSOL 5.4a — 99호는 5.3a)는 **Nernst 항 포함** — 그림 7(a) 재풀이 ±0.05 mV · 빼면 19.3 mV | **물려받지 않음** — 같은 표 · 같은 식 · 다른 구현 |
| 표 1 D_n⁻ 2.1 ↔ 그림 5.1(99호 D2) | 표 I 5.1 | **고침** |
| k_pos 5.1×10⁻⁴ = 91호 k₁ˢ ×100 · 다른 단위 · 식 (17) 차원 불일치 | 같은 값 · 식 (7) 같은 꼴 | **물려받음** |
| 인쇄 k_r(91호 ×100 문제) — 99호 표 2 의 '단순화 (1) 무시 가능' 을 만듦 | 같은 값 · ROM 이 r 을 버린 근거로 "[9]" 를 인용 | **물려받음 + 조건 탈락**(k_r ×100 이면 10C RMS 14.85 mV) |
| c_max · c_min 미인쇄(99호 G1) | 인쇄 | **채움** |
| 99호 '9 %' = 모형 불일치가 OCV 평탄 기울기로 증폭된 SOC 편향(99호 판정 1) | 인용 0 · 대신 'SOC · SOH < 4 %'(액체 [14] · [31]) · "100%–10% SOC" 운용 창(평탄 0.1–0.4 를 포함) | **무시** — 같은 공저자(X. Lin)의 ASSB 결과와 반대 방향의 일반화(D13) |
| 'PDE 대비 2.6 mV' | 같은 매개변수 한 벌의 ROM ↔ PDE — 표 I 의 상속 문제(k_r · k_pos)는 둘에 같이 들어간다 | 이 오차는 **매개변수 검증이 아니다**(축약 오차만) |

## 3. 그림 9 의 실험 — 출처 · 경로 (`[인쇄]` → `[도표·벡터]` · `[재현·외부 값]`)

- **출처**: "[7]" = Danilov · Niessen · Notten 2011 *JES* 158, A215(91호) — 같은 셀(Li | Li₃PO₄ | LiCoO₂ 박막 · 공칭 10 µAh · 1C = 10 µA cm⁻² — 91호 digest 전사)의 1.6C CCCV 충전 뒤 방전 다섯(3.2–51.2C) 중 셋. **이 편의 측정이 아니다** · 옮긴 방법(원자료 ↔ 그림 디지타이즈) · 시간 원점 미인쇄(G5).
- **시작 전압**: 실험 첫 표지 4.173 · 4.151 · 4.111 V ↔ 91호 측정 Q = 0 4.177 · 4.156 · 4.116 V ✅(91호 digest 전사).
- **끝**: 실험 점선 마지막 점 546.4 · 266.6 · 124.2 s ↔ 91호 측정 용량 환산 554.6 · 274.5 · 134.6 s(**×0.985 · 0.972 · 0.924**) · 91호 그림 2 의 마지막 점 − 첫 방전 점(9.47 · 4.83 · 2.46 − 0.274 분) = 551.8 · 273.4 · 131.2 s(91호 digest 전사)와도 5–7 s 짧다(D12).
- **모형**: PDE 끝 543.1 · 262.1 · 122.0 s ↔ Danilov 자기 모형선(91호 전사 541.7 · 257.9 · 121.1 s) · `[재현]` 표 I 재풀이 3.4 V 도달 541.40 · 260.55 · 120.09 s — 91호가 "모형 = 측정의 90 %(25.6C) · 94–96 %(12.8C) · 98 %(6.4C)" 로 본 용량 결손(91호 digest 전사)이 이 편 모형에도 그대로 있고, 짧아진 실험 끝과 만나 '일치' 로 보인다.
- **평형 곡선**: 표 I + 식 (14) 재풀이는 끝 시각을 ±1.1 s 로 맞추지만 t = 1 s 전압이 +92 · +86 · +74 mV 높다 → [7] 외삽 EMF(91호 그림 4 · 5 의 I = 0 점 11 개 · 선형 보간)로 바꾸면 +2.6 · +1.0 · −2.0 mV · 6.4C 100 · 200 · 500 s +1.8 · +2.7 · +1.2 mV · 12.8C 200 s +1.2 mV — **그림 9 는 [7] EMF 로 계산된 것으로 읽힌다**("the same model parameters in the reference" 의 실제 내용 — 인쇄 0 · D11). 그 EMF 는 같은 방전 곡선 네 율(1.6–12.8C)의 회귀 외삽이다(91호) — 실험 곡선 일부가 모형 입력이 되어 다시 실험과 비교됐다(`[해석]` — (햐) 의 측정 몫).
- **25.6C 의 전해질**: `[재현]` 표 I 값의 정상 한계 전류 4FAD_Li⁺δc₀/L_e = 250.5 µA = **25.1C** — 25.6C 는 그 바로 위다(122 s 안에는 고갈 전 — 10C 선형 외삽으로 c(L_e, 120 s) ≈3.7×10³ mol m⁻³). "three large C-rates" 의 가장 큰 율이 이 모형 전해질의 정상 한계 근처다(`[해석]` — 91호 51.2C 가 한계의 두 배였던 것과 같은 축).

---

# ★ (c) 식별 대상으로서의 ROM — Q4

## 1. 이 편이 세운 것 (`[인쇄]` → `[재현·대수]`)

| 묶음 | 자리 | 무엇이 들어 있나 |
|---|---|---|
| **K_s = 1/(A·F·L_p)** | 양극 전달함수 적분기(용량 극) · 표 II 모든 행 | 면적 × 두께(× F) — c_max − c_min 과 함께 용량 Q = F·A·L_p·(c_max − c_min) |
| **τ_s = L_p²/D_Lis** | 표 II 의 u = τ_s·s · 식 (25) 의 iL_p/(6FAD_Lis) = i·K_s·τ_s/6 | 두께² ÷ 확산 계수 |
| **K_e = L_e/(4·A·F·D_Li⁺)** | 표 III 직류 이득 · 식 (27) a₁ = −i/(2FAD_Li⁺) | 두께 ÷ (면적 × 양이온 확산) |
| **τ_e = L_e²/D**(D = D_amb — 그림이 쓴 값) | 표 III 의 시간 | 두께² ÷ 쌍극 확산 |
| (D_Li⁺ − D_n⁻)/(D_Li⁺ + D_n⁻) · δc₀ | 식 (10) · (28) 전기장 · 식 (9) Nernst 항의 농도 | 확산 계수 비 · 자유 Li 농도 |
| **A·k_pos** · c_max · c_min · α | 식 (7) i₀,pos | 면적 × 속도 상수 한 곱 |
| c_max | 식 (12) θ = c/c_max · 식 (14) | 평형 곡선의 눈금 |

"The coefficients of the transfer functions can be explicitly derived from the electrochemical parameters" · "which makes it a lumped-parameter model" — 묶음 목록 · 묶음 수 · 어느 묶음이 자료로 정해지는지는 인쇄 0. `[재현·대수]` 양극 쪽 출력은 K_s · τ_s · A·k_pos(+ c_max · c_min · α)로만 쓰이므로 **(A, L_p, D_Lis, k_pos) → (λA, L_p/λ, D_Lis/λ², k_pos/λ) 가 양극 묶음 셋을 모두 보존**한다 — 전해질 쪽 K_e · τ_e 가 A 를 D_Li⁺ 와의 곱으로 따로 보지만, 그 방향을 고정하려면 전해질 수송(D_Li⁺ · D_n⁻)을 알아야 한다(91호: 전해질 넷 \|상관\| ≥ 0.98 한 묶음 · 조건수 9.5×10⁵ — 91호 digest 전사).

## 2. 이 편이 하지 않은 것 (`[인쇄]`)

- 매개변수 추정 0 · 실측 전압에 맞춤 0(그림 9 는 [7] 의 매개변수 · EMF 로 돌린 forward).
- 식별성 · 감도 · 관측성 · 불확실성 0 — 아래 어휘표.
- 상태 추정 0 — "SOC and SOH can be obtained with an error less than 4%" 는 [14] · [31](둘 다 액체셀 — 서지 제목 기준)을 근거로 한 문장 · 같은 모형 계열 ASSB 추정 [9] 의 9 % · 5 %(99호 digest 전사) 무언급.

## 3. 어휘 (NFKC · 줄 끝 분철 복원 뒤 · 쪽 머리 · 바닥 제외 · 본문 = 제목 → 결론 · 초록 · 캡션 포함 | 참고문헌 | 약력 · 표 I–V · 그림 안 글자는 벡터라 셈 밖)

| 낱말 | 본문 | 참고문헌 | 쓰임 |
|---|---|---|---|
| `identif*` | **1**(+ 'Digital Object Identifier' 1 은 뺌) | 1 | Fabre 소개 "to identify some model parameters" 하나 · 참고문헌 [23] 제목 "multi-parameters identification" · 약력 둘('parameter identification' — 연구 관심) |
| `observab*` · `estimab*` · `sensitiv*` · `uniqu*` · `confiden*` · `uncertain*` · `±` · `correlat*` · `Fisher` · `Hessian` · `Gramian` · `rank` · `variance` · `bias` · `Monte` · `covarian*` · `noise` · `Jacobian` | **0** | 0 | — |
| `error*` · `RMSE` · `MaxAE` · `accura*` | 28 · 5 · 4 · 26 | 0 · 0 · 0 · 1 | ROM ↔ PDE 오차 |
| `validat*` · `valid*` | 4 · 5 | 0 | "validity of the parameters has been verified by many existing references [7], [9], [27]" · "validate the model accuracy" · "validated under galvanostatic and potentiostatic conditions"(Fabre 소개) |
| `experiment*` · `measur*` · `simulat*` | 9 · 2 · 22 | 0 · 0 · 3 | 실험 = [7] 곡선 · "fit from experimental data"(식 14) · "cannot be directly measured"(상태) · "measurement data of the real battery"(그림 9) |
| `fit` · `parameter` | 2 · 8 | 0 · 1 | "Eeq is fit from experimental data" · Kazemi "fit the diffusion coefficient" · 'lumped-parameter model' |
| `Padé` · `Laplace` · `frequency` · `UDDS` · `COMSOL` · `MATLAB` | 8 · 10 · 10 · 10 · 7 · 6 | 1 · 0 · 0 · 0 · 0 · 0 | 방법 |
| `Kalman` · `SOC` · `SOH` | 1 · 9 · 2 | 0 · 7 · 1 | "[9] … extended Kalman filter" · '< 4 %' |
| `contact*` · `degrad*` · `ag(e)ing` · `pressure` · `capacity` · `plateau` | **0** · 0 · 0 · 0 · 0 · 0 | 1(Tian & Qi 제목) · 0 · 0 · 0 · 1 · 0 | 열화 · 접촉 · 평탄 축 0 |
| `temperature` · `thermal` | 2 · 3 | 0 · 1 | 서론 열 폭주 · 기호 정의 'T is the temperature'(값 0) |
| `real-time` · `lumped` | 3 · 1 | 0 · 0 | 실시간 · 'lumped-parameter model' |

## 4. 판정 — Q4 0/100 · 아흔두 번째 성질 · 공백 1번 후보 마지막 ASSB 편

- 원장 행 물음 "식별성을 다루는지 미확인" 의 답: **다루지 않는다** — 식별성 낱말은 남의 편 소개 하나 · 계산 0 · 묶음 목록 0. 26호가 본 "식별 대상이 되는 형태" 는 맞다(계수 = 묶음 · 닫힌 꼴) — 그러나 그 꼴을 세운 편이 그 꼴로 아무것도 식별하지 않았다.
- **아흔두 번째 성질** = **"축약 모형(ROM)을 ASSB 에 처음 세운 편 — 전달함수 계수가 매개변수 묶음(1/(A·F·L_p) · L_p²/D_Lis · L_e/(4A·F·D_Li⁺) · L_e²/D · A·k_pos)으로만 쓰여 식별 대상이 되는 꼴인데 식별성 · 감도 · 불확실성 어휘 0 · 매개변수 추정 0 — 검증은 같은 매개변수 한 벌의 PDE 대비 RMSE(10C 0.54 · UDDS 2.6 mV — 최대 4.6 · 40.5 mV)와 다른 편 실험 곡선 셋(그 편의 외삽 EMF 로 계산된 것으로 읽힘)이고, SOC · SOH '< 4 %' 는 액체 문헌의 외삽이다 — 그리고 같은 지면에서 출력(전압)이 4.6 mV 로 맞을 때 성분(η_d)은 76.3 mV 어긋났다(V 는 θ_s 만 본다)."** — 99호 아흔한 번째 성질("관측성을 이름 붙였으나 재지 않았다")의 축약 모형판: 식별할 꼴을 세웠으나 식별하지 않았다.
- **원장 §2 공백 1번 — 후보 목록의 Deng 2021 은 식별성 편이 아니다**(75호 Naik · 92호 Firouz · 99호 Kim 닫음과 같은 형식): 축약 모형 · 매개변수 추정 0 · 식별성 계산 0 · 열화 손잡이 0 → Q4 0/100(분모 +1 · 채움 0). 후보 목록의 ASSB 편은 이로써 모두 확인됐다 — 공백 1번은 ASSB 1차 계산 편으로 여전히 비어 있고(29호 반 칸 그대로), 남은 후보는 액체 도구(Khalik · Lu — 95 · 96호 흡수 · Forman 2012 미수령)뿐이다(wiki 밖 — 호출자 몫).
- 누적 0.5 그대로.

---

# ★ (d) θ ↔ ε_p — 37호 물음

| 손잡이 | 이 편 축약 모형의 자리 | 판정 |
|---|---|---|
| **활물질 분율 ε_p** | 없음 — 조밀 박막(다공 전극 이론 불필요 "the porous electrode theory is no longer needed") · 양극 용량 = A·L_p·(c_max − c_min) | **자리 0** |
| **접촉 θ(A_eff)** | 없음 — 면적 A 하나가 용량 극 1/(A·F·L_p) · 전해질 이득 L_e/(4A·F·D_Li⁺) · 식 (27) 기울기 −i/(2FAD_Li⁺) · 교환 전류 F·A·k_pos 에 같은 값 | **자리 0** — '접촉만 줄고 용량은 그대로' 를 표현할 곳이 없다 |
| A 를 줄이면(`[재현·대수]`) | 용량 극 ↑(같은 전류에 농도가 빨리 움직임 = 용량 ↓) · 전해질 이득 ↑ · i₀ ↓ — 셋이 함께 | 접촉 손실 · LAM · 동역학 저하가 한 손잡이에 묶임 |
| L_p 를 줄이면 | 용량 극 ↑ · τ_s ↓ · i₀ 그대로 | 두께(활물질) 손실은 A 와 다른 서명 — 그러나 양극 묶음만으로는 (A, L_p, D_Lis, k_pos) 축척 한 방향이 남는다(§(c) 1) |
| 37호(같은 3차 Padé · Ts 1 s 계열 · 37호 digest 전사) | A_eff 를 BV 분모(식 8)에만 · ε_p 는 용량 극 1/(ε_p A L_p F) | 이 편 뒤의 추가 — A_eff ↔ k_p 정확 대칭(37호) · 그 곱의 뿌리 = 이 편 식 (7) 의 F·A·k_pos |

⇒ **37호 물음의 답: 따로 두지 않는다 — 둘 다 없고, 면적 A 하나에 용량 · 수송 · 동역학이 묶인다.** 원장 문구("축약 모델이 θ 를 ε_p 와 따로 두는가")와 37호 원문 물음("`A_eff` 형 손잡이가 있는지") 둘 다 '없다'. 카드 물음(OCV 맞춤이 LAM_PE 와 접촉 손실을 가르는가)의 축약 모형 층 표본: 이 꼴 위에서 '접촉 손실' 을 넣으려면 A 를 어느 이득에 줄일지(용량 극 · 수송 · i₀) 먼저 정해야 하고, 그 선택이 답을 미리 정한다([[assb-synthetic-truth-contact-loss-requirements]] R1 의 또 하나의 위반 표본 — `[해석]` · 이 편은 열화를 다루지 않는다).

---

# (e) Q1–Q8 — 채움표 칸 (닻 카드 수집 지침)

| Q | 칸 | 이 편 |
|---|---|---|
| Q1 정량 | **해당 없음 — `θ(N)` 0/100** | 조밀 박막 · 열화 0 · `contact*` 본문 0 · 층 하나: 면적 A 한 값이 용량 극 · 수송 이득 · i₀(F·A·k_pos)에 · 양극 묶음의 면적 ↔ 두께 축척 대칭(`[재현·대수]`) |
| Q2 분리 관측 | **없다** | 관측 = 전압 하나(+ 모형 내부 농도 · 과전압) · 실험 = [7] 의 전압 곡선 셋(인용) · 관측 추가 0 |
| Q3 라벨 층위 | **칸 없음 · 층 하나** | "PDE 기준 = 인쇄 식 그대로(Nernst 항 포함 — 재풀이 ±0.05 mV · 99호 그림과 다른 구현) · ROM 은 인쇄 식 다섯 자리(식 18–21 · 27 · 28)를 고친 꼴로 계산 · 표 I = 99호 표 1 계보(D_n⁻ 고침 · c_max/c_min 인쇄 · k_r · k_pos 상속 · k_neg 새 값 출처 미인쇄) · 그림 9 = [7] 측정(끝 ×0.92–0.99) + [7] 외삽 EMF(인쇄 0) · 실험 0" |
| Q4 유일성 | **0/100 — 아흔두 번째 성질** | 위 §(c) 4 · 축약 모형 = 식별할 꼴 · 식별 0 · 원장 §2 공백 1번 후보 Deng 2021 확인(식별성 편 아님) · 누적 0.5 그대로 |
| Q5 기준 전위 | **해당 없음** | Li 금속 · "the potential in the anode is assumed to be uniform and equal to 0 V [7], [9]" · η_ct,neg(식 8 · k_neg 새 값) 10C "lower than 0.1 mV"(`[재현]` 0.05–0.06 mV) |
| Q6 압력 | **해당 없음** | 박막 · `pressure` 0 |
| Q7 Li 재고 | **해당 없음 + 공백 하나 채움** | Li 금속 무한 원천 · c_Lis,max · c_Lis,min 인쇄(99호 G1 = 91호 a_max · a_max/2) · SOC₀ 1.0 = c_min(i₀,pos = 0 에서 출발) |
| Q8 OCP · 평형 곡선 | **층 둘** | 식 (14) = [10] Fabre 유리함수(99호 식 22 와 같은 계수 · 그림 5–8) + 그림 9 의 [7] 외삽 EMF(`[재현·외부 값]` ±7 mV · 인쇄 0) — 한 지면에 평형 곡선 둘 · 출처 층위 표기 0 |

**누적 ≈20.0 → ≈20.0 (새 칸 0).**

---
# 재현 (`[재현]` — 인쇄 수치 · 식 · 그림 좌표로 우리가 계산 · 가정 · 외부 값 표시 · 스크립트는 `scratchpad` 에만)

| # | 무엇 | 입력 | 결과 | 대조 |
|---|---|---|---|---|
| R1 | 표 II · III 의 Padé | 기호 계산 — √u coth √u · √u / sinh √u · tanh z / z | 표 II [1/1] · [2/2](두 끝) · 표 III [0/1] · [1/2] · [2/3] 계수 전부 일치 · y = 0 [1/1] 분자 −1/20(인쇄 +) | D9 |
| R2 | 그림 2 PDE · 표지 | 벡터 경로 · 정확 coth 전달함수 · 표 II | PDE ±0.13 dB · ±0.06° · 표지 ±0.75 dB · ±0.34°(4차 = 우리 [3/3]) | ✅ |
| R3 | 그림 3 표지의 D | 벡터 · 표 III Padé · D 최적 | 1차 −45° @8.19×10⁻³ rad/s → D 1.535×10⁻¹⁵ · 1 · 2차 최적 1.553 · 1.542×10⁻¹⁵ = D_amb(1.53×10⁻¹⁵) · D_e(0.765×10⁻¹⁵) 면 6.5 dB · 19.5° | D3 |
| R4 | 그림 3 PDE ↔ 식 (22) | 벡터 · 정확 tanh 응답(D_amb · D_e) | 10⁻³: −3.9 ↔ −7.0° · 0.1: 142.5 ↔ 137.1 dB · 1: 142.9 ↔ 127.1 · 632 rad/s 499.3 ↔ 99.0 dB · 위상 −32° 골 → +87° → 들쭉날쭉 ↔ −45° 수렴(D_e 로도 안 맞음) | D2 |
| R5 | 3차 유효 대역 | 정확 ↔ Padé · 1 dB / 5° | 양극 2차 0.19 · 3차 1.18 · 4차 3.83 rad/s · 전해질 2차 0.083 · 3차 0.354 · 4차 0.98 rad/s · 2.5 rad/s 3차 −18.9° · −35.8°(−3.35 dB) · π rad/s −23.1° · −37.6°(−4.28 dB) · 15.7 rad/s −6.13 dB · −40.2° / −11.18 dB · −43.5° | D4 |
| R6 | 원 PDE 재풀이 ↔ 그림 7 | 표 I · SOC₀ 1.0 · T 298.15 K · 식 (9) 그대로 · 유한체적 120 + 60 · BDF | η_mt ±0.05 mV(1–330 s) · Nernst 항 빼면 최대 19.3 mV · V ±1.4 mV · η_d ±0.9 · η_ct ±0.2(≤300 s) · 3.35 V 339.61 ↔ 339.01 s · SOC₀ 0.995 · 0.99 면 끝 15.6 · 44.8 mV | 판정 4 · §(a) 4 |
| R7 | 그림 5(d)(b) PDE 단면 | 같은 재풀이 | 전해질 ±10 mol m⁻³(x = L_e 끝 −24 … −38) · 양극 −17 … −39 | ✅ D_amb · δc₀ |
| R8 | 그림 5(c) ROM 표지 | 표 III 3차 Padé · `lsim` 계단(99.9 µA) | D_amb ±50 mol m⁻³ · D_e 400–870 | D3 |
| R9 | 그림 5(d) ROM 삼차식 | R8 의 c(0) · c(L_e) + 식 (27) | L_e 꼴 RMS 2 · 32 · 38 · 4 · 11 mol m⁻³(1 · 10 · 50 · 100 · 300 s) · 인쇄 L_e² 꼴 3.6×10⁹ | D5 |
| R10 | 그림 7(a) ROM η_mt | R8 · R9 + 식 (28) · Nernst 항 · 사다리꼴 2,001 점 | 비 (D_Li⁺ − D_n⁻)/(D_Li⁺ + D_n⁻) ±0.08 mV(13 점) · 'D_e' 그대로 13.7 mV | D6 |
| R11 | r 항 제거의 k_r 감도 | 재풀이 r 있음 ↔ 없음 · 10C 0–330 s | V 차 RMS · 최대: 0.9e-8 0.40 · 0.75 · 0.9e-7 3.47 · 6.41 · 8.0e-7 14.22 · 23.12 · 0.9e-6 14.85 · 23.94 mV · η_mt(300 s, r 있음) −38.30 → −18.59 | 판정 2 · (져) |
| R12 | 그림 9 평형 곡선 | 표 I + 식 (14) ↔ `[재현·외부 값]` [7] EMF(91호 전사 11 점 · 선형) · SOC₀ 1.0 | 식 (14): t = 1 s +92.1 · +86.2 · +74.7 mV(6.4 · 12.8 · 25.6C) · 끝 541.40 · 260.55 · 120.09 ↔ 540.27 · 260.21 · 120.23 s / EMF: +2.6 · +1.0 · −2.0 mV · 대부분 ±7(마디 근처 ≤22) | D11 |
| R13 | 그림 9 실험 끝 | 벡터 점선 · `[재현·외부 값]` 91호 측정 용량 | 546.4 · 266.6 · 124.2 ↔ 554.6 · 274.5 · 134.6 s(×0.985 · 0.972 · 0.924) · 91호 그림 2 마지막 점 기준 551.8 · 273.4 · 131.2 s · PDE 끝 543.1 · 262.1 · 122.0 ↔ Danilov 모형선 541.7 · 257.9 · 121.1 | D12 |
| R14 | 그림 9 창 안 일치 | 표지 · 점선 → 곡선 배정 · SOC 100–10 % 창 | PDE − 실험 중앙 −8.1 · −8.7 · −4.8 mV(6.4 · 12.8 · 25.6C) | 본문 "good agreement" ✅(창 안) |
| R15 | 표 IV ↔ 그림 7 · 8 벡터 | ROM 대시 꼭짓점 − PDE 보간 | 그림 7 η_mt RMSE 0.38 · 최대 0.67 ↔ 0.38 · 0.66 ✅ · 그림 8 V 최대 36.7 @2,722 s · η_d 36.0 @2,713 s ↔ 40.5 · 35.9(끝) | D1 |
| R16 | UDDS 프로파일 | 그림 6(a) 벡터 2,286 점 | 2,742 s · 지연 1,370 s(r 0.985) · −3.88 … +8.65C · 평균 1.285C · 순 0.979 Q · 방전 1.076 · 회생 0.098 Q | G4 |
| R17 | 용량 · C-rate | 표 I c_max − c_min | Q 9.99 µAh · 1C 9.9916 µA · 10C 3.35 V 에서 SOC 0.057 · UDDS 끝 SOC 0.021 · 표 V 지속/명목 0.993 · 0.987 · 0.971 · 0.944 | D15 |
| R18 | 계산 시간 | 표 V | 단계당 0.123 · 0.129 · 0.157 · 0.206 · 0.124 ms · ROM ÷ 단순 PDE 0.41–0.51 | D14 |
| R19 | η_ct,neg | 식 (8) · k_neg 1×10⁻² · 수치 A m² | i₀,neg 0.041(수치) · 10C 0.054–0.063 mV · 25.6C 0.14–0.16 mV | 인쇄 "lower than 0.1 mV"(10C) ✅ |
| R20 | 양극 묶음 축척 대칭 | 표 II · 식 (7) · (25) | (A, L_p, D_Lis, k_pos) → (λA, L_p/λ, D_Lis/λ², k_pos/λ) 가 1/(AFL_p) · L_p²/D_Lis · A·k_pos 보존 · 전해질 K_e = L_e/(4AFD_Li⁺) 는 A·D_Li⁺ 로만 | §(c) 1 · (d) |
| R21 | 정상 한계 전류 | 4FAD_Li⁺δc₀/L_e | 250.5 µA = 25.1C(99호 R13 과 같은 값) · 그림 9 최고 율 25.6C | §(b) 3 |
| R22 | 일정 | 2020-05-15 → 09-19 | 127 일 · 온라인 09-28 · 현재판 2021-05-10(= PDF 수정일) | — |

---

# 참고문헌 31 번호 — 우리 축에 닿는 것 (번호는 PDF p. 472–473 목록에서 직접 확인 · 빠진 번호 0)

| 번호 | 서지(지면 그대로 요약) | 이 편에서 쓰인 자리 | 우리 축 |
|---|---|---|---|
| [7] | Danilov D., Niessen R., Notten P., "Modeling all-solid-state Li-ion batteries", *J. Electrochem. Soc.* 158(3), A215–A222, 2011 | 박막 1D 모형 원형 · 음극 0 V · 그림 9 실험 자료 · "the same model parameters in the reference" | **91호 = 4차 묶음 파일 51**(흡수) |
| [8] | Kazemi N., Danilov D.L., Haverkate L., Dudney N.J., Unnikrishnan S., Notten P.H.L., "Modeling of all-solid-state thin-film Li-ion batteries: Accuracy improvement", *Solid State Ionics* 334, 111–116, Jun. 2019 | 농도 의존 D(5 mA/cm² 고율 정확도) · "accuracy of COMSOL simulations has been verified" 인용 묶음 | 원장 ★★★(98 \| 1) · **재지목** |
| [9] | Kim Y., Lin X., Abbasalinejad A., Kim S.U., Chung S.H., "On state estimation of all solid-state batteries", *Electrochim. Acta* 317, 663–672, Sep. 2019 | 그림 1 출처 · 표 I 머리 · BV 식 출처 · "ignoring the r term will not cause a large voltage error" · 서론의 유일한 ASSB 제어 지향 선행 | **99호 = 4차 묶음 파일 59**(흡수) |
| [10] | Fabre S.D., Guy-Bouyssou D., Bouillon P., Le Cras F., Delacourt C., "Charge/discharge simulation of an all-solid-state thin-film battery using a one-dimensional model", *J. Electrochem. Soc.* 159(2), A104–A115, **2011**(인쇄) | **식 (14) 평형 곡선의 출처** · "GITT and EIS to identify some model parameters" | 원장 ★★(98 · 99 \| 2 — 원장 행 연도 2012 · 같은 권 · 쪽) · **재지목** |
| [11] | Raijmakers L.H.J., Danilov D.L., Eichel R.-A., Notten P.H.L., "An advanced all-solid-state Li-ion battery model", *Electrochim. Acta* 330, 135147, 2020 | 서론 계보(이중층 · 기하 축전기) | **98호 = 4차 묶음 파일 58**(흡수) |
| [13] | Hu X., Xu L., Lin X., Pecht M., "Battery lifetime prognostics", *Joule* 4(2), 310–346, 2020 | SOH 인용(서론) | 12호 후속 ★(Fig. 6 'LAM ⊃ contact loss' 정의의 원전) · 원장 행 0 → **지목 누락 — 이 편이 재지목하며 보충** |
| [14] | Hu X., Yuan H., Zou C., Li Z., Zhang L., "Co-estimation of state of charge and state of health for lithium-ion batteries based on fractional-order calculus", *IEEE Trans. Veh. Technol.* 67(11), 10319–10329, 2018 | **'SOC · SOH < 4 %' 의 근거 둘 중 하나** | 새 ★ |
| [18] · [31] | Han X., Ouyang M., Lu L., Li J., "Simplification of physics-based electrochemical model for lithium ion battery on electric vehicle. Part I / Part II", *J. Power Sources* 278, 802–813 · 814–825, 2015 | 다항식 근사 · COMSOL 정확도 인용 · **'< 4 %' 근거 둘째([31])** | 새 ★(묶음) |
| [19] | Marcicki J., Canova M., Conlisk A.T., Rizzoni G., "Design and parametrization analysis of a reduced-order electrochemical model of graphite/LiFePO4 cells for SoC/SOH estimation", *J. Power Sources* 237, 310–324, 2013 | Laplace 축약 · **'2.5 Hz' 대역 기준의 출처** | 95호 ☆(행 없음) → 새 ★★(매개변수화 분석 = 축약 모형의 식별 쪽 원전 후보 · 액체) |
| [20] · [21] | Smith K.A., Rahn C.D., Wang C.-Y., *Energy Convers. Manage.* 48(9), 2565–2578, 2007 · *J. Dyn. Syst. Meas. Control* 130(1), 011012, 2008 | Laplace · 잔류 묶음(residue grouping) 축약의 원형 | 새 ★(묶음 · 액체 · [20] 은 96호 참고문헌 표 [59]–[64] 에도 — 후속 절 밖) |
| [22] | Forman J.C., Bashash S., Stein J.L., Fathy H.K., "Reduction of an electrochemistry-based Li-ion battery model via quasi-linearization and pade approximation", *J. Electrochem. Soc.* 158(2), A93–A101, 2010(인쇄) | **Padé 축약의 방법 출처** | 새 ★(같은 연구실 Forman 2012 FIM 은 원장 ★★★ 다른 편) |
| [23] · [24] | Deng Z., Deng H., Yang L., Cai Y., Zhao X., "Implementation of reduced-order physics-based model and multi-parameters identification strategy for lithium-ion battery", *Energy* 138, 509–519, 2017 · Deng Z., Yang L., Deng H., Cai Y., Li D., "Polynomial approximation pseudo-two-dimensional battery model for online application in embedded battery management system", *Energy* 142, 838–850, 2018 | Padé · 다항식 — **같은 첫 저자의 액체 판 둘 · [23] 은 축약 모형 위 '다중 매개변수 식별'** | [23] 새 ★★(Q4 — 이 편의 꼴 위에서 실제로 식별한 편 · 액체) · [24] 새 ★ |
| [25] | Lee J.L., Chemistruck A., Plett G.L., "Discrete-time realization of transcendental impedance models, with application to modeling spherical solid diffusion", *J. Power Sources* 206, 367–377, 2012 | DRA 축약 · COMSOL 정확도 인용 | 새 ★(액체 · Plett 계보 — 96호 참고문헌 표 [59]–[64] 묶음의 Lee · Chemistruck · Plett 2012 *JPS* 220, 430 과 다른 편 · 그 표는 후속 절 밖) |
| [26] | Danilov D., Notten P.H.L., "Mathematical modelling of ionic transport in the electrolyte of Li-ion batteries", *Electrochim. Acta* 53(17), 5569–5578, 2008 | **식 (9) η_mt · 식 (10) 전기장의 유도처** | 원장 ★(26 · 91 · 98 \| 3) · **4차 묶음 파일 61**(도착 · 101호 예정) · **재지목** |
| [27] | Tian H.-K., Qi Y., "Simulation of the effect of contact area loss in all-solid-state Li-ion batteries", *J. Electrochem. Soc.* 164(11), E3512–E3521, 2017 | **표 I 머리 출처**("[9], [27]") · "validity of the parameters has been verified by … [27]" | 원장 ★★★(6) · **재지목** |
| [28] | Yuan S., Jiang L., Yin C., Wu H., Zhang X., *J. Power Sources* 352, 245–257, 2017 | 전달함수 + Padé(수정 경계) | 새 ★(액체) |
| [29] · [30] | Rahimian S.K., Rayman S., White R.E., *JPS* 224, 180–194, 2013 · Lee J.L., Aldrich L.L., Stetzel K.D., Plett G.L., *JPS* 255, 85–100, 2014 | "accuracy of COMSOL … verified by" 묶음 | ☆ |
| [1]–[6] · [12] · [15]–[17] | Liu J. 외 2019 *Nat. Energy* · Feng X. 외 2018 *Energy Storage Mater.* · Kim J.G. 외 2015 *JPS* 282 종설 · Albertus 외 2018 *Nat. Energy* · Doyle · Fuller · Newman 1993 *JES* · Fuller · Doyle · Newman 1994 *JES* · Deng 외 2020 *Energy*(GPR) · Yang 외 2020 *Appl. Energy*(SOP) · Hu 외 2019 *RSER*(종설) · Deng 외 2016 *Energy* | 서론 · 배경 · 상태 추정 일반 | ☆ |

---

# 인용 대조

## 1. 이 편을 지목 · 인용한 우리 digest — 그 쓰임 ↔ 이 편이 실제로 주는 것

| digest | 쓰임(digest 전사) | 이 편 | 판정 |
|---|---|---|---|
| **26호** Iwakiri 2024 [16] | §11 ★★★ "축약 모델 = 파라미터 식별 대상이 되는 형태 — **식별성 논의 여부 미확인**(원장 '구조적 공백 1번' 후보)" | 전달함수 계수 = 묶음 다섯(닫힌 꼴) ✅ · 식별성 논의 0 · 매개변수 추정 0 | 형태 ✅ · 논의 **0** — 공백 1번 후보 확인으로 닫음 |
| **37호** Li 2024 [29] | §14(등급 칸 없음) "ASSB 축약 모델(ROM) — `A_eff` 형 손잡이가 있는지" · 37호 자신도 Laplace + 3차 Padé · Ts 1 s(37호 digest 전사) | A_eff 0 · ε_p 0 · 면적 A 하나가 모든 이득 · i₀ 에 | 답: **없다** — 37호의 A_eff(BV 만)는 이 꼴 위의 뒤 추가 |
| 99호 Kim 2019 | 후속 표 "도착 — (이 편 이후 편 · 인용 0)" · "이 편 공저자 X. Lin 의 후행 축약 모형(서지 표기 일치만 · 미확인)" | 저자 X. Lin 같음 ✅ · [9] 로 99호를 인용(그림 1 · 표 I · r 무시 근거) · 99호의 SOC 결과는 인용 0 | 99호 쪽 서술 ✅(교차 — 지목 아님) |

## 2. 이 편이 인용한 우리 digest

- **[7] = 91호**(흡수됨) — 이 편의 쓰임: 모형 원형 · 음극 0 V · **그림 9 의 실험 자료 · "the same model parameters in the reference"**. 91호가 찾은 것(k_r ×100 · 고율 끝 용량 결손 · EMF 의 회귀 외삽 — 91호 digest 전사)은 이 편에 그대로 들어와 있다(R11 · R12 · R13).
- **[9] = 99호**(흡수됨) — 그림 1(좌표 바꿈) · 표 I 머리 · 식 (6)–(7) BV 출처 · r 항 무시 근거. 99호의 Nernst 항 부재는 이 편 PDE 에 없다(R6) · 99호 D_n⁻ 표기 오류는 고쳐졌다 · 99호 SOC 오차(9 % · 5 %)는 인용 0.
- **[11] = 98호**(흡수됨) — 서론 한 문장.
- 4차 묶음 13 편 중 인용: **[7](파일 51 · 91호) · [9](파일 59 · 99호) · [11](파일 58 · 98호) · [26](파일 61 Danilov & Notten 2008 · 101호 예정)** 넷 — 나머지 아홉(Firouz 2020 · Bielefeld 2023 · Schmidt 2024 · Khalik 2021 · Lu 2022 · Koerver 2018 · Xie 2008 · Shao 2022 · Ansah 2021) 인용 0(31 번호 전수 대조 — Bielefeld · Schmidt · Lu · Shao · Khalik · Ansah 는 이 편보다 뒤 · Firouz 2020 · Koerver 2018 · Xie 2008 은 앞이나 인용 0).

---

# 곱 축퇴 처방 — 여든세 번째 적용 ([[assb-lampe-contact-product-degeneracy]])

⚠ 이 편은 접촉 · 노화 0 인 신품 박막 모형의 **축약** 편이다 — 처방의 입력 점검은 대부분 ❌ 이고, 남는 것은 **곱의 자리가 축약 모형(전달함수 계수) 안에서 어떻게 되는가** 다.

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계**(16호) | `R` 과 `C` 를 같이 | 축전기 · 이중층 0 | ❌ |
| **2단계**(18 · 25호) | + 면적을 아는 대조군 | 평판 박막 기하 면적 A = 1 cm²(설계) 하나 | ❌ |
| **3단계-a**(19호) | `Ea` | T 미인쇄 · 등온 | ❌ |
| **3단계-b**(19호) | `C` 물리 상한 | — | ❌ |
| **4단계**(20 · 24호) | 시간 영역 | 축척 UDDS 두 번(모의) · 주파수 응답(모의) | ⚠ 모의만 — A·k_pos 를 수송과 가르는 시험 0 |
| 처방 표 "율 스윕" | 여러 율 | 1 · 2 · 5 · 10C(모의 · 표 V) + 6.4 · 12.8 · 25.6C(인용 실험) | ⚠ 모의 + 인용 |
| 처방 표 "`J^T J` 최소 고유벡터" | 적합점 야코비안 | 적합 0 | ❌ |

## ★ 곱 문장 — 셋 (`[인쇄]` → `[해석]`)

- ① `[인쇄]` 식 (7) "i₀,pos = −FAk_pos(…)" · 표 II "1/(AFL_p)" · 표 III "L_e/(4AD_Li⁺F)" — 면적 A 가 교환 전류의 곱 **A·k_pos** 와 용량 극 · 수송 이득에 **같은 값**으로 들어간다 ⇒ `[해석]` 이 꼴에서 접촉 면적 손실은 'A 를 줄인다' 로만 쓸 수 있고, 그러면 용량 · 수송 · 동역학이 함께 움직인다 — 접촉만의 손잡이는 없다(99호 식 17 · 91호 식 8 · 98호 식 9 와 같은 자리의 축약판).
- ② `[재현·대수]` 양극 묶음 셋(1/(AFL_p) · L_p²/D_Lis · A·k_pos)은 (A, L_p, D_Lis, k_pos) → (λA, L_p/λ, D_Lis/λ², k_pos/λ) 에서 그대로다 — **면적 손실(A ↓)과 두께 · 활물질 손실(L_p ↓)이 양극 출력에서 한 방향으로 묶인다**. 그 방향을 고정하는 것은 전해질 쪽 이득 L_e/(4AFD_Li⁺)(A·D_Li⁺ 곱)뿐이라 전해질 수송을 따로 알아야 한다.
- ③ `[인쇄]` 37호(같은 3차 Padé 계열 — 37호 digest 전사)는 A_eff 를 BV 분모에만 넣었다 ⇒ `[해석]` 그 A_eff ↔ k_p 정확 대칭(37호)은 이 편 식 (7) 의 A·k_pos 한 곱을 BV 쪽으로 옮긴 것이다 — 축약 모형 계보에서 '접촉 손잡이' 는 붙인 자리(용량 극 · 수송 · BV)를 적지 않으면 정의되지 않는다.
- ⇒ 처방 표에 **새 줄은 없다**. 후보 메모 하나(처방 표로 올리지 않음 · 결정 대기): **"축약 모형(전달함수 계수)에서 곱을 볼 때 면적 A 가 어느 이득에 들어가는지(용량 극 · 수송 · 교환 전류)와, 두께 L_p 가 용량 극과 확산 시간에 함께 들어가 면적 ↔ 두께 축척 방향이 남는지를 적는다 — 'A_eff 손잡이' 를 붙인 편이면 붙인 자리를 적는다."**

## ⚠ 이것이 곱을 푼 것은 아니다

- 열화 · 접촉 · 온도 · 면적 대조가 모두 0 인 신품 모형의 축약 편이다 — 위 자리는 **구조**이고 측정이 아니다. 축척 대칭은 인쇄 식 · 표 위의 우리 대수(`[재현·대수]`)이고, 이 편은 그것을 말하지 않는다.

---
# 보류 결정 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(햐) · (겨)–(져) — 이 편이 주는 근거 (결정 안 함)

| # | 결정 (요약) | 100호 근거 | 세기 |
|---|---|---|---|
| **(세)** | 인쇄 매개변수 표의 재풀이 폐합 검사 | 표 I + SOC₀ 1.0 + T 298.15 K 로 그림 7 η_mt ±0.05 mV · V ±1.4 mV · 그림 5 단면 ±10 mol m⁻³ 폐합(R6 · R7) · ROM η_mt ±0.08 mV(R10) · c_max · c_min 이 인쇄돼 99호 때 필요했던 외부 값 없이 닫힘 · 그림 9 는 표 I + [7] EMF 로만 ±7 mV(식 14 면 +74 … +92 mV — R12) | **강** |
| **(셔)** | 인쇄 식 ↔ 그림의 항 폐합 | 원 PDE 는 식 (9) 그대로 — Nernst 항 포함(빼면 19.3 mV · R6) — 99호(둘째 항만)와 반대 방향의 같은 계열 표본 · ROM 은 인쇄 식 다섯 자리를 고친 꼴로만 그림이 닫힘(식 21 D_e ×2 · 27 L_e · 28 비 · 18–20 √D · 19 지수 — R3 · R8–R10 · D3 · D5–D8) | **강** |
| **(여)** | 표 값 ↔ 계산 값 + 출처 번호 | 표 I D_n⁻ 5.1 = 그림 값(99호 2.1 정정) · 머리 "[9], [27]"(Tian & Qi = 접촉 면적 손실 모의) · k_neg · α_neg 새 값 출처 미인쇄 · 그림 9 "the same model parameters in the reference" 의 실제 내용 = [7] 의 EMF(인쇄 0) | **강** |
| **(져)** | 축약 모형 검증의 흔들지 않은 매개변수 · 배제 영역 | 매개변수 흔들기 0(표 I 한 벌) · r 무시의 근거 = "[9]"(인쇄 k_r) · `[재현]` k_r ×100(91호 그림 일치 값)이면 r 무시만으로 10C RMS 14.85 · 최대 23.94 mV(ROM 보고 RMSE 0.54 의 ≈27 배 — R11) | **강** |
| **(치)** | 모형 결론 옆 '배제 가정' 표기 | "voltage errors … less than 2.6 mV" · "SOC and SOH … less than 4%" · "can be applied to an embedded BMS" — 배제: 매개변수 한 벌 · 인쇄 k_r · α 0.5 · 지표 = RMSE · 방전 끝 최대 40.5 mV · 운용 창 100–10 % 가 OCV 평탄(0.1–0.4)을 포함 | **강** |
| **(탸)** | 요약 수치 ↔ 같은 편 표 · 그림 | 초록 'less than 2.6 mV' ↔ 표 IV MaxAE 40.5 · 4.6 mV · 'within 0.2 ms' ↔ 10C 0.206 ms · 'SOC … to 0%' ↔ 0.057 · 0.021(R17) | **강** |
| **(햐)** | '계산 ↔ 실험 일치' 의 측정 몫 · 비교 축 | 그림 9 실험 = [7] 측정(인용 · 옮긴 방법 미인쇄) · 모형 평형 곡선 = [7] 의 율 외삽 EMF(같은 방전 곡선의 회귀 — 측정 몫이 입력에 들어감 · 91호) · 그림 5–8 · 표 IV · V = 계산 ↔ 계산 | **강** |
| **(제)** | 모형 '일치' 의 율별 끝 용량 잔차 | 실험 끝 ×0.985 · 0.972 · 0.924(91호 측정 용량 대비 — R13) · PDE 끝 ≈ Danilov 모형선 · 그림 9 축 600 s 에서 7–10 s = 2.6–3.7 pt — 표지(≈2.1 pt)보다 조금 크다(눈으로는 끝 꺾임 위치 차) | **강** |
| **(체)** | 평형(OCV) 곡선의 출처 층위 | 식 (14) = Fabre "fit from experimental data"(측정 방법 · 범위 미인쇄 · 99호와 같은 계수) · 그림 9 = [7] 외삽 EMF(인쇄 0) — 한 지면에 평형 곡선 둘 | **강** |
| **(며)** | 'validated' 의 자료 층위 | "The validity of the parameters has been verified by many existing references [7], [9], [27]" — [9] 는 [7] 적합값을 쓴 계산 편 · [27] 은 접촉 모의 · "validate the accuracy of the models"(그림 9 = [7] 자료 + [7] EMF) | **강** |
| (냐) | 모형 결론 회고 인용 — 조건 복원 | "The results of [9] suggest that ignoring the r term will not cause a large voltage error" — 99호 표 2 결론(인쇄 k_r · 10C · 99호 플랜트 — 99호 digest 전사)을 조건 없이 · 초록 2.6 mV 의 지표 탈락 | 중 |
| (벼) | '관측성 · 관측 불가' 주장의 산출물 표기(상태 추정판) | "SOC and SOH can be obtained with an error less than 4%" — 추정기 실행 0 · 근거 = 액체 [14] · [31] · 같은 모형 계열 [9] 의 9 % · 5 %(OCV 평탄 증폭 편향 — 99호) 무언급 | 중 |
| (겨) | 처방 효과의 측정 여부 | "it can be integrated into a battery management system" · '< 4 %' — 측정 · 실행 0 | 중 |
| (대) | C-rate 의 기준 용량 표기 | 표 I c_max · c_min 으로 1C = 9.99 µA 확정(99호 공백 채움) · 그림 9 C-rate = [7] 의 10 µA cm⁻² 기준 · UDDS 축척 미인쇄 · 표 V 지속 = 명목의 0.944–0.993 | 중 |
| (뎌) | '문헌값 일치' 의 자료 독립성 | 매개변수 타당성 근거 [7] · [9] · [27] — [9] 는 [7] 적합값의 재사용이라 독립 근거가 아니다 | 중 |
| (이) | 모형 값 인용 규칙 | 표 I 'Estimated value' = 91호 적합값(99호 경유) + 새 k_neg · α_neg | 중 |
| (에) | 속도 상수의 i₀ 환산 표기 | k_pos 5.1×10⁻⁴ · k_neg 1×10⁻² m³ mol⁻¹ s⁻¹ — F·A·k × 무차원 비의 차원 불일치 그대로 · 수치 i₀,neg 0.041 · η_ct,neg 0.05–0.06 mV(R19) | 중 |
| (뱌) | 재매개화 · 묶음의 최소성 | 전달함수 계수 = 묶음 다섯(1/(AFL_p) · L_p²/D_Lis · L_e/(4AFD_Li⁺) · L_e²/D · A·k_pos) — 지면은 묶음 목록 0('lumped-parameter model') · `[재현·대수]` 양극 축척 대칭 한 방향(R20) | 중 |
| (먀) | '모형 원전' 지목 때 기구 층위 확인 | 26호 '식별 대상이 되는 형태' ✅ · 논의 0 · 37호 'A_eff 형 손잡이' → 없다(A 하나) | 중 |
| (갸) | '단순성' 근거 명제의 척도 | "a better tradeoff between model fidelity and computational complexity" — 척도 = 단계당 0.2 ms · 차수 3 · 대가(UDDS 끝 40.5 mV · 3차 대역 0.19 · 0.056 Hz)는 같은 지면에 | 중 |
| (무) | j₀(x) 모양 선택지 | α_pos 0.6 ↔ 0.5 — 10C 최대 0.68 ↔ 5.60 · UDDS 1.80 ↔ 2.10 mV(표 IV) | 약 |
| (녀) | 계면 반응 방향(부호 규약)의 재풀이 폐합 | 식 (6) 둘째 지수 − 부호 빠짐 · 식 (7) 음의 i₀ 관례 — 그림 7(c) 는 표준 BV 로 ±0.2 mV(방향 문제는 아님) | 약 |
| (루) | SOC 축 신품 j₀(x) 기준선 | SOC₀ 1.0 = c_min → i₀,pos = 0 에서 출발(식 7 의 (c − c_min)^(1−α)) · 그림 7(c) 1 s −6.61 mV(SOC₀ 0.99 의 99호 −5.97 보다 큼 — 99호 digest 전사) | 약 |
| (차) | PyBaMM 면적 / j₀ 노브 분리 forward | 면적 A 하나가 모든 이득 + i₀ — 축약 꼴에서 두 노브를 가를 자리 0 · 37호가 A_eff 를 BV 에만 붙인 계보 | 약 |
| (다) | 28호 액체 도구를 ASSB Q4 분모에 | ASSB 축약 모형 편도 식별성 0 — 분모에 ASSB 한 점 더 | 약 |
| (쟈) | '식별 가능' 주장의 층 표기 | 식별 주장 0 — 'lumped-parameter model' 이름만 | 약 |
| (가) | 29호 Q4 +0.5(정적 ↔ 동적) | V 는 θ_s 만 본다 — 정적(Eeq(θ̄)) ↔ 동적(η_d) 분할이 전압에 안 보이는 구조 표본(표 IV η_d 76.3 ↔ V 4.6 mV) — 결정 재료 아님 | 약 |
| (리) | 요구치 계보의 남은 다리 요청 묶음 | Tian & Qi 2017 재지목 → 7(표 I 머리 [27] · "validity … verified by … [27]") | 약 |
| (헤) | 측정 입력의 역모형 층위 | L_e · L_p · A = 91호 설계값 · c₀ = NDP — 측정 입력은 남의 셀 것 · 이 편 측정 0 | 약 |
| (페) | '입력 설계' 의 목적 표기 | UDDS 축척 두 번 = "mimic the real driving conditions" — 정보 설계 아님 · 주파수 응답은 모의 | 약 |
| (마) | 37호 "ASSB truth 5조건" — **결정 · 반영(2026-09-23)** | (마) 의 닿는 논문에 Deng 2021 이 적혀 있다 — R1(ε_p 와 별개 θ)의 위반 표본 하나 더(면적 A 하나 · θ · ε_p 0) · 출처 추가만 | — |

나머지 — (라)(바)(사) 결정 · 반영됨(이 편 근거 0), 그 밖의 글자는 **근거 0**(압력 · 기준극 · 3전극 · 노화 사이클 · LLI 실측 · θ 판정 · 상 분율 · 입도 · 피복률 · 프로토콜 비교 · 원자료 예치 · DRT · 축전기 · 상태 추정 실행이 이 편에 없다). **결정 안 함.**

## 새 판단 거리 (넷 — 글자는 호출자가 붙인다)

1. **축약 · 근사 모형 오차 주장의 지표 · 위치 · 조건 표기** ((탸) · (냐) 의 축약 모형판으로 묶어도 됨) — ROM · 근사 모형의 'error less than X' 를 카드 · 개념 · 하네스로 옮길 때 ① 지표(RMSE ↔ 최대) ② 최대의 자리(방전 끝 · 켜는 순간) ③ 프로파일(축척 · 반복 · 끝 SOC) ④ 비교 대상이 같은 매개변수 한 벌의 원 모형인지(그러면 축약 오차일 뿐 매개변수 검증이 아님) ⑤ 성분별 오차(출력에 안 보이는 성분 포함)를 같이 적게 할지 — 100호: 초록 'less than 2.6 mV' = UDDS RMSE(최대 40.5 mV @방전 끝 · `[도표·벡터]` 36.7 mV @2,722 s) · 10C V 최대 4.6 ↔ η_d 76.3 mV.
2. **차수 · 대역 선택 근거 그림의 기준 곡선 검사 + 인용 대역 기준 ↔ 실제 표본 주기** ((셔) 의 주파수판으로 묶어도 됨) — 축약 차수를 정한 편의 주파수 응답 그림을 옮기거나 그 차수를 하네스에 쓰기 전에, 그림의 '원 모형' 곡선이 인쇄 해석식의 정확한 응답인지 다시 계산하고 고른 차수의 유효 대역(예: 1 dB · 5°)을 인용 기준과 실행 표본 주기에 견줘 적게 할지 — 100호: 그림 3 PDE 곡선 ≠ 식 (22)(632 rad/s 499 ↔ 99 dB · 위상 진동 ↔ −45°) · 3차 대역 0.19 · 0.056 Hz ↔ 기준 2.5 Hz ↔ Δt 1 s.
3. **'실험 검증' 그림의 자료 경로 표기 — 인용 실험 곡선 · 그 그림에만 쓴 입력 · 끝 용량 대조** ((햐) · (제) · (며) 의 인용 자료판으로 묶어도 됨) — 모형 편이 다른 편의 실험 곡선으로 '검증' 할 때 ① 자료 출처와 옮긴 방법(원자료 ↔ 디지타이즈 · 시간 원점) ② 그 그림에만 쓴 입력(평형 곡선 · 초기 SOC — 특히 원 편이 같은 곡선에서 뽑은 EMF) ③ 옮긴 곡선의 끝 용량 ↔ 원 편 인쇄 용량을 적게 할지 — 100호: [7] 곡선 · [7] EMF(인쇄 0 · `[재현·외부 값]` ±7 mV) · 끝 ×0.985 · 0.972 · 0.924.
4. (선택) **출력에 안 보이는 성분의 표기 — '전압 일치' 에서 성분 분해 라벨로 넘어갈 때** ((쟈) · (뱌) 의 성분판으로 묶어도 됨) — 모형의 과전압 성분 · 벌크 상태(η_d · Eeq(θ̄) · SOC)를 라벨 · truth · 카드로 옮길 때 그 성분이 관측(전압)에 들어가는 식 경로를 적고, 출력 사상에서 상쇄되는 쌍(η_d ↔ Eeq(θ̄))이면 성분 오차를 출력 오차와 따로 적게 할지 — 100호: V = Eeq(θ_s) + η 라 η_d 오차 76.3 mV ↔ V 4.6 mV(표 IV · 10C) — 우리 degeneracy 물음("곡선이 맞는다 ≠ 분해가 맞다")의 모형 층 판.

---

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** ★★★ | 초록 "the voltage errors of the proposed ROM are less than 2.6 mV" ↔ 표 IV UDDS MaxAE 40.5 · 10C MaxAE 4.6 mV(η_d 76.3) — 2.6 = UDDS **RMSE**(결론은 'RMSE … 0.54 and 2.6 mV' 로 바르게 씀) | 표 IV · R15 |
| **D2** ★★★ | 그림 3 'PDE' 곡선 ≠ 식 (22) 의 정확한 응답(10⁻³ rad/s 에서 이미 위상 −3.9 ↔ −7.0° · 632 rad/s 499 ↔ 99 dB) — 본문은 PDE 의 성질("diverges … oscillates")로 해석해 차수 선택 근거로 씀 | R4 · G10 |
| **D3** ★★★ | 식 (21) · 표 III D_e = D_Li⁺D_n⁻/(D_Li⁺ + D_n⁻) ↔ 식 (5) 계수 2D_Li⁺D_n⁻/(D_Li⁺ + D_n⁻) ↔ 그림 3 표지 · 그림 5(c) ROM = 2D_e | R3 · R8 |
| **D4** ★★ | 차수 근거 "90% … less than 2.5 Hz [19]" ↔ 그림 2 의 3차 유효 대역 ≈0.19 Hz(그림 축은 rad/s) · 2.5 Hz 에서 3차 −6.1 dB · −40° · 실행 Δt 1 s(Nyquist 0.5 Hz) | R5 |
| **D5** ★★ | 식 (27) a₂ 둘째 항 3i/(2L_e²FAD_Li⁺) — 차원 불일치(L_e 이어야) · 그림 5(d) = L_e 꼴 | R9 |
| **D6** ★★ | 식 (28) 'D_e' 자리 = (D_Li⁺ − D_n⁻)/(D_Li⁺ + D_n⁻)(식 10) — 식 (21) 의 D_e 와 같은 글자 · 그림 7(a) ROM = 비 꼴(±0.08 mV · D_e 그대로면 13.7 mV) | R10 |
| **D7** ★★ | 식 (18)–(20) 분모 AFβ√D_Lis — AFD_Lisβ(= AF√(sD_Lis)) 이어야(차원) · 표 II · 그림 2 는 맞는 꼴 | R1 · R2 |
| **D8** ★ | 식 (19) 분자 2exp(2L_pβ) — 식 (18) 에 y = 0 이면 2exp(L_pβ) | 대수 |
| **D9** ★ | 표 II y = 0 2차 분자 "+ L_p s/(20AD_Lis F)" — [1/1] Padé 는 − | R1 |
| **D10** ★★ | 식 (6) i = i₀(e^{αFη/RT} − e^{(1−α)Fη/RT}) — 둘째 지수의 − 부호 빠짐(α 0.5 면 i ≡ 0) · 식 (7) i₀,pos 앞 '−'(음의 교환 전류 관례) — 식 (29) asinh 꼴은 표준 BV 에서만 나온다 | 쪽 렌더 · R6 |
| **D11** ★★ | "the same model parameters in the reference are also used in this article" ↔ 그림 9 는 식 (14) 가 아니라 [7] 의 외삽 EMF 로 계산된 것으로 읽힘(표 I + 식 14 면 시작 전압 +74 … +92 mV) — 평형 곡선 교체 인쇄 0 | R12 |
| **D12** ★★ | 그림 9 'Experiment' 끝 546.4 · 266.6 · 124.2 s ↔ [7] 측정 용량(91호 전사) 554.6 · 274.5 · 134.6 s(×0.985 · 0.972 · 0.924) · PDE 끝 ≈ Danilov 자기 모형선 | R13 |
| **D13** ★★ | "the SOC and SOH can be obtained with an error less than 4%" — 근거 [14] · [31](액체) · 추정기 실행 0 · 같은 모형 계열 ASSB 상태 추정 [9] 의 9 % · 5 %(99호 digest 전사) 무언급 | 본문 · 99호 |
| **D14** ★ | "its calculation time per step is within 0.2 ms" ↔ 표 V 10C 0.07 s / 340 = 0.206 ms | R18 |
| **D15** ★ | "the battery SOC decreases from 100% to 0%"(10C · UDDS) ↔ 3.35 V 에서 SOC 0.057 · UDDS 끝 0.021(`[재현]`) | R17 |
| **D16** ★ | 그림 1 캡션 "reprinted from [9]" ↔ 본문 "modified based on the work of Kim et al. [9]" — 좌표 이름(x · y · L_e · L_p)이 99호 그림 1(L · M · y)과 다름 | 그림 1 |
| **D17** ★ | 좌표 · 기호: 식 (2) · (3) 전해질에 ∂/∂y(정의는 x — "x and y are defined in the regions of electrolyte and cathode") · 식 (15) 분모 'c_Li,min'(c_Lis,min) · 'D_e' 두 뜻(D6) | 쪽 렌더 |
| **D18** ★ | 참고문헌 [10] Fabre "vol. 159, no. 2, … 2011"(원장 행 2012 — 같은 권 · 쪽 · 99호 D19 와 같은 표기) · 자금 "Engineering Research Council of Canada"(인쇄 그대로) | p. 472 · p. 464 |

---

# 이 편이 우리 프로젝트에 주는 것 (정리)

- **출력이 맞는다 ≠ 성분이 맞다 — 지면 안의 수치 표본.** 같은 10C 실행에서 V 최대 오차 4.6 mV 와 η_d 최대 오차 76.3 mV 가 함께 있다(표 IV) — 전압이 θ_s 만 보기 때문이다(식 16). 우리 `degradation-degeneracy/` 의 물음("곡선이 맞는다 ≠ 매개변수 · 분해가 맞다")에 축약 모형 층 표본을 준다(우리 수치는 `degradation-degeneracy/docs/RESULTS*.md` 정본 — 옮기지 않음).
- **축약 모형 = 묶음** — 축약 모형을 하네스 forward 로 쓰면 식별 단위는 원 매개변수가 아니라 묶음 다섯(1/(AFL_p) · L_p²/D_Lis · L_e/(4AFD_Li⁺) · L_e²/D · A·k_pos)이고 양극 쪽에는 면적 ↔ 두께 축척 한 방향이 남는다([[spm-grouped-parameter-identifiability]] 의 박막 판). '접촉 손잡이' 는 붙인 자리를 적지 않으면 정의되지 않는다(37호 A_eff 는 BV 만).
- **합성 truth 구현 경고 둘** — ① 같은 모형 · 같은 표의 두 편이 η_mt 를 다르게 계산했다(99호 = 식의 둘째 항만 · 100호 = 식 그대로 · 차 ≤19.3 mV @10C 300 s) — truth 로 이식할 때 어느 쪽인지 적어야 한다 ② 인쇄 식 다섯 자리가 계산과 다르다 — 구현은 인쇄 식이 아니라 그림 폐합으로 확인한다.
- **'실험 검증' 의 자료 경로** — 같은 곡선에서 뽑은 EMF 로 그 곡선을 '검증' 하는 구성(그림 9)은 독립 관측이 아니다 — 우리 쪽 검증 기준(독립 관측 · 보류 자료)의 반례 표본.
- **계보 매개변수 오류의 전파** — 91호의 k_r ×100 문제가 99호의 '단순화 (1) 무시 가능' 을 거쳐 이 편 ROM 의 r 무시 정당화가 됐다(조건 탈락 · k_r ×100 이면 10C RMS 14.85 mV).
- **이 편이 주지 않는 것**: 실험(자기) · 열화 · 접촉 · 압력 · LLI · LAM · 매개변수 식별 · 관측성 · 상태 추정 실행 · 원자료 · 코드 — 그리고 100 편 누적 `θ(N)` 0.

---

# 후속 후보 (원전 우선 — 지목 수는 위키 digest 의 후속 절 grep 으로 센 값)

| 등급 | 서지 (PDF 목록 번호) | 지목 (후속 절) | 왜 | 축 |
|---|---|---|---|---|
| ★★★ | Tian H.-K., Qi Y. 2017 — "Simulation of the effect of contact area loss in all-solid-state Li-ion batteries", *J. Electrochem. Soc.* **164**(11), E3512–E3521([27]) | 12 · 81 · 94 · 97 · 98 · 99 · **100** = **7**(재지목) | **표 I 머리 출처**("[9], [27]") · 'validity … verified by … [27]' — 새 값 k_neg 1×10⁻² · α_neg 0.5 의 출처 후보 · 그 편이 접촉 면적 손실을 i₀ = F·A·k 의 A 로 넣는지(이 계열 '면적 하나' 의 원전) | Q1 · Q6 · 곱 · (b) |
| ★★★ | Kazemi N., Danilov D.L., Haverkate L., Dudney N.J., Unnikrishnan S., Notten P.H.L. 2019 — *Solid State Ionics* **334**, 111–116([8]) | 98 · **100** = **2**(재지목) | 같은 계보 가운데 편 — 농도 의존 D 로 고율(5 mA cm⁻²) 정확도를 올린 편 · 이 편이 'COMSOL 정확도' 인용 묶음에 넣고 ROM 에는 쓰지 않은 개선(고율 끝 용량 결손 — 그림 9) | Q4 · Q3 |
| ★★ | Fabre S.D., Guy-Bouyssou D., Bouillon P., Le Cras F., Delacourt C. — *J. Electrochem. Soc.* **159**(2), A104–A115(인쇄 2011 · 원장 2012)([10]) | 98 · 99 · **100** = **3**(재지목) | **식 (14) 평형 곡선의 원전**(99 · 100호 연속) · "GITT and EIS to identify some model parameters" — 계보 안에서 실제로 매개변수를 식별한 편 후보 | Q8 · Q4 · (체) |
| ★★ | Marcicki J., Canova M., Conlisk A.T., Rizzoni G. 2013 — "Design and parametrization analysis of a reduced-order electrochemical model of graphite/LiFePO4 cells for SoC/SOH estimation", *J. Power Sources* **237**, 310–324([19]) | 95(☆) · **100** = **2**(☆ 에서 올림 — 96호 Chu 2019 선례) | **'2.5 Hz' 대역 기준의 출처** · 축약 모형의 '매개변수화 분석' — 축약 모형 위 식별(어느 묶음이 자료로 정해지는가)의 액체 원형 후보 | Q4 · 방법 |
| ★★ | Deng Z., Deng H., Yang L., Cai Y., Zhao X. 2017 — "Implementation of reduced-order physics-based model and multi-parameters identification strategy for lithium-ion battery", *Energy* **138**, 509–519([23]) | **100** = 1(새) | 같은 첫 저자의 **축약 모형 + 다중 매개변수 식별**(액체) — 이 편의 꼴을 실제 식별에 쓴 편 · 식별성 진단 여부 확인처 | Q4 · 방법 |
| ★ | Hu X., Xu L., Lin X., Pecht M. 2020 — "Battery lifetime prognostics", *Joule* **4**(2), 310–346([13]) | 12 · **100** = **2**(**지목 누락 보충**) | 12호 ★ 이유 그대로 — 12호 Fig. 6 'LAM ⊃ contact loss' 정의의 원전(그 정의가 원전에도 그렇게 있는지) · 이 편은 SOH 인용 · 저자 셋이 이 편과 겹침 | Q3 · 라벨 |
| ★ | Hu X., Yuan H., Zou C., Li Z., Zhang L. 2018 — *IEEE Trans. Veh. Technol.* **67**(11), 10319–10329([14]) | 100 = 1(새) | **'SOC · SOH < 4 %' 근거 첫째** — 어느 셀 · 어떤 오차 정의인지 | (벼) · Q4 |
| ★ | Han X., Ouyang M., Lu L., Li J. 2015 — Part I · Part II, *J. Power Sources* **278**, 802–813 · 814–825([18] · [31]) | 100 = 1(새) | 다항식 근사 · **'< 4 %' 근거 둘째**([31]) | 방법 · (벼) |
| ★ | Forman J.C., Bashash S., Stein J.L., Fathy H.K. — *J. Electrochem. Soc.* **158**(2), A93–A101(인쇄 2010)([22]) | 100 = 1(새) | Padé 축약 원전(같은 연구실의 Forman 2012 FIM 은 원장 ★★★ 다른 편) | 방법 |
| ★ | Smith K.A., Rahn C.D., Wang C.-Y. 2007 · 2008 — *Energy Convers. Manage.* **48**, 2565 · *J. Dyn. Syst. Meas. Control* **130**, 011012([20] · [21]) | 100 = 1(새) | Laplace · 잔류 묶음 축약의 원형(액체) | 방법 |
| ★ | Deng Z., Yang L., Deng H., Cai Y., Li D. 2018 — *Energy* **142**, 838–850([24]) | 100 = 1(새) | 다항식 근사 P2D(같은 첫 저자) | 방법 |
| ★ | Lee J.L., Chemistruck A., Plett G.L. 2012 — *J. Power Sources* **206**, 367–377([25]) | 100 = 1(새) | DRA 축약 | 방법 |
| ★ | Yuan S., Jiang L., Yin C., Wu H., Zhang X. 2017 — *J. Power Sources* **352**, 245–257([28]) | 100 = 1(새) | 전달함수 + Padé(수정 경계) | 방법 |
| 도착 | **Danilov D., Notten P.H.L. 2008** — *Electrochim. Acta* **53**, 5569([26]) | 26 · 91 · 98 · **100** = **4**(재지목) | **4차 묶음 파일 61 로 도착 · 처리 대기(101호 예정)** — 식 (9) η_mt · 식 (10) 전기장의 유도처("[26]") | 모형 |
| 도착 | **Danilov D., Niessen R., Notten P. 2011** — *J. Electrochem. Soc.* **158**, A215([7]) | — | **91호로 흡수됨**(4차 묶음 파일 51) — 교차 · 그림 9 자료 | 모형 |
| 도착 | **Kim Y., Lin X., Abbasalinejad A., Kim S.U., Chung S.H. 2019** — *Electrochim. Acta* **317**, 663([9]) | — | **99호로 흡수됨**(4차 묶음 파일 59) — 교차 | Q4 |
| 도착 | **Raijmakers L.H.J., Danilov D.L., Eichel R.-A., Notten P.H.L. 2020** — *Electrochim. Acta* **330**, 135147([11]) | — | **98호로 흡수됨**(4차 묶음 파일 58) — 교차 | 모형 |
| ☆ | Liu J. 외 2019([1]) · Feng X. 외 2018([2]) · Kim J.G. 외 2015 종설([3] — 99호 ☆) · Albertus 외 2018([4]) · Doyle · Fuller · Newman 1993([5]) · Fuller · Doyle · Newman 1994([6]) · Deng 외 2020([12]) · Yang 외 2020([15]) · Hu 외 2019 종설([16]) · Deng 외 2016([17]) · Rahimian 외 2013([29]) · Lee · Aldrich · Stetzel · Plett 2014([30]) | 행 없음 | 서론 · 배경 · 상태 추정 일반 · COMSOL 정확도 인용 | — |

**지목 누락 하나 — 이 편이 재지목하며 보충**: Hu · Xu · Lin · Pecht 2020 *Joule*(12호 후속 ★ 7 · 원장 행 0). 등급 칸 없는 옛 후속 표에만 있던 편 0(Marcicki 2013 은 95호 ☆ — ☆ 는 행 없음 관례라 누락 아님 · 이 편이 ★★ 로 올림). **흡수된 편(교차)**: [7] = 91호 · [9] = 99호 · [11] = 98호. **4차 묶음 도착 편**: [26] = 파일 61(새 요청 행 아님).

---

# 이 digest 가 주장하지 않는 것

- **이 편의 ROM 이 쓸모없다고 하지 않는다** — 계수는 정확한 Padé 이고 그림 5–8 은 우리 재현과 닫히며 정전류 축약 오차는 작다(RMSE ≤0.54 mV); 걸린 것은 초록의 지표 탈락 · 차수 근거 그림 · 인쇄 식 오기 · 실험 검증의 자료 경로 · 상속 매개변수(k_r · k_pos) · '< 4 %' 외삽이다.
- **그림 3 PDE 곡선의 원인을 주장하지 않는다** — 식 (22) 의 정확한 응답과 다르다는 것(R4)까지다(계산 방법 미인쇄 · 코드 미공개).
- **인쇄 식 오기 다섯(D3 · D5–D7 · D10)을 구현의 사실로 확정하지 않는다** — 그림이 고친 꼴로만 닫힌다는 것(벡터 판독 위의 재현)까지다.
- **그림 9 가 [7] EMF 로 계산됐다고 확정하지 않는다** — 91호 digest 전사 11 점 선형 보간으로 ±7 mV 가 맞고 식 (14) 로는 +74 … +92 mV 라는 것까지다; 실험 끝이 짧은 이유(디지타이즈 · 시간 원점)도 확정하지 않는다.
- **양극 축척 대칭을 이 편의 명제로 옮기지 않는다** — 인쇄 식 · 표 위의 우리 대수(`[재현·대수]`)이고, 이 편은 묶음을 말하지 않는다.
- **'V 는 θ_s 만 본다' 를 이 편의 오류로 쓰지 않는다** — 모형 구조의 사실이고 저자의 η_d 설명도 크기로는 맞다; 우리 물음의 표본으로만 쓴다.
- **이 편을 Q4 · Q1 칸 이동 근거로 쓰지 않는다** — 식별성 계산 0 · 열화 0.
- **원 참고문헌(26 · 37 · 91 · 98 · 99호 인용분)을 다시 열지 않았다** — 대조는 각 digest 전사로 했다.
