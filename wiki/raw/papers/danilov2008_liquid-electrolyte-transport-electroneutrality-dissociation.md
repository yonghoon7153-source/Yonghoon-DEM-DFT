---
title: "Danilov D., Notten P.H.L. 2008 — Mathematical modelling of ionic transport in the electrolyte of Li-ion batteries (Electrochim. Acta 53, 5569–5578)"
source_url: local-upload/61._Mathematical_modelling_of_ionic_transport_in_the_electrolyte_of_Li-ion_batteries.pdf
source_url_note: "본문 PDF 10 쪽(Electrochim. Acta 53 (2008) 5569–5578 · 인쇄 쪽 = PageLabels 5569 부터 · 그림 12 — 전부 ≈200 dpi JPEG 래스터 · 표 1 · 식 (1)–(47) · 참고문헌 18) 1,996,390 B · 업로드 접두사 e83153cd · 4차 묶음 파일 61 · SI 없음(보충 언급 0 · 임베디드 파일 0) · 원자료 · 코드 공개 0 · ⚠ ASSB 아님 — 액체(유기) 전해질 LiPF₆ 수송 모형 원전 · 자기 측정 그림 하나(그림 9 — in-house Lithylene 셀 · 기준극 쌍)"
source_doi: 10.1016/j.electacta.2008.02.086
source_license: "0013-4686/$ – see front matter © 2008 Elsevier Ltd. All rights reserved.(인쇄) · OA 표기 0 — 구독본으로 다룬다 — 이 digest 는 인용 · 요약 · 재현 계산만 담는다(그림 크롭은 위키 관례대로 raw/figures 에 — 변형 없는 잘라내기)"
pdf_sha256: f427e8738b49cb4193e0b8f50b6572456d248431fd29cf3a147122288edf14a5
ingested: 2026-10-03
sha256: 6eed292b1952714c85e941bcf3ebca7b4b49b71baae83077a8e884fac64e2a7f
---
# 수집 목적

`assb` 섹션 **101호** — **4차 묶음 파일 61**(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 요청 14 편 중 열한째 · 2026-10-02 사용자 공급 · 파일 51–64 = 91–104호를 받은 순서대로). ⚠ **ASSB 아님 — 액체(유기) 전해질 LiPF₆ 의 Nernst–Planck 수송 모형 원전**(95 · 96호의 "ASSB 아님" 칸 규칙 — 다만 이 편은 추정 도구가 아니라 **모형 원전**). 이 편이 직접 닿는 곳은 ① **26호**(Iwakiri 2024 — §11 후속 표 [20] ★★ "해리 전해질 수송(이온 + 공공)의 원전 — 'SE 에 농도 구배' 가정의 출처" · 26호 digest 가 옮긴 Iwakiri 식 (22) · (23b) · (25) · (26) 이 이 편 식의 꼴) ② **91호**(Danilov · Niessen · Notten 2011 — [27] "It can be shown[27]" = 식 18 의 유도처 · n⁻ 의 정체 · k_r · δ 의 대조처로 지목) ③ **98호**(Raijmakers 2020 — [28] 식 (23)–(24) · (31) "see Refs. [11,28]") ④ **100호**(Deng 2021 — [26] 식 (9) η_mt · 식 (10) 전기장) ⑤ **99호**(Kim 2019 — 이 편을 인용하지 않지만 99호 D1 "그림의 전체 모형에 Nernst 항이 없다" 의 원형 식이 이 편 식 (30)) ⑥ 개념 [[assb-synthetic-truth-contact-loss-requirements]] · [[assb-lampe-contact-product-degeneracy]] · [[spm-grouped-parameter-identifiability]] 다. 우리 쪽 수치(`degradation-degeneracy/`)는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본이고 여기 옮기지 않는다.

Eurandom(Eindhoven) + Eindhoven University of Technology + Philips Research Laboratories — **D. Danilov**(Eurandom) · **P.H.L. Notten**(교신 · TU/e + Philips Research · ISE 회원 각주) 의 *Electrochim. Acta* 2008 편. `[인쇄]` 초록이 스스로 적는다: "The ionic conductivity of the organic electrolyte in Li-ion batteries has been modelled. The classical one-dimensional Nernst–Planck approach results in a system of two non-linear parabolic second-order partial differential equations. It is shown that under electro-neutrality conditions this complex system of equations can be reduced to simple diffusion equations with modified diffusion coefficient, facilitating the efficient use of numerical methods. As a result, detailed information about transient and steady-state behaviour of the electrolyte is revealed, including potential gradients and the diffusion and migration fluxes for both Li+ and PF6− ions. Furthermore, an extension of the basic model is presented, taking into account salt dissociation in the electrolyte. … Some of the numerical simulations are compared with recently reported experimental results." 이 편이 실제로 한 것은 **LiCoO₂ | LiPF₆ 유기 전해질 | 흑연(LiC₆) 셀의 전해질 한 층(두께 L)을 두 운반체(Li⁺ · PF₆⁻) 1D Nernst–Planck 로 두고, 전기중성(c_Li⁺ = c_PF₆⁻)으로 확산 방정식 하나(수정 확산계수 D = 2D₊D₋/(D₊ + D₋) · 두 경계 기울기 I/(2FAD₊))와 전기장의 닫힌 꼴(식 19 · 21)로 줄인 뒤, Li⁺ 전기화학 퍼텐셜 차로 전해질 과전압 η = (RT/F) ln[c(L)/c(0)] − ∫E dy(식 27 · 30)를 정의해 첫 항을 'diffusion' · 둘째 항을 'migration' 성분으로 부르고, 표 1 의 Sony CGR17500(720 mAh — 값은 "all taken from Ref. [11]")로 1C 50 min 충전 + 이완을 MATLAB pdepe(공간 L/200)로 풀어 켜는 순간 · 정상 · 끄는 순간의 닫힌 꼴(식 31–42 — η_down/η_ss = t₊)을 내고, 중성 이온쌍 LiPF₆ 의 해리 · 재결합 + 확산(식 43–47)으로 확장해 해리도 δ 1–0.6569 의 과전압(그림 10–12)을 계산하고, in-house Lithylene 300 mAh 셀의 기준극 쌍 측정 하나(그림 9)에 겹친 모형 원전**이다. **고체 전해질 · 공공 · 단일 이온 전도체 0**(`solid` · `vacanc*` · `glass` · `single-ion` 본문 · 참고문헌 0 회) · 매개변수 추정 0 · 열화 · 접촉 · 압력 0.

들어온 경로: 원장 행(도착 표시 전 원문 그대로) "| ★ | **Danilov·Notten 2008** — *Electrochim. Acta* **53**, 5569 | 26 | 1 | 모델 | 해리 전해질 수송(이온+공공) 원전 — "SE 에 농도 구배" 가정의 출처 |". 위키 grep(`Danilov` · `Notten 2008` · `Danilov & Notten` · `Danilov·Notten` · `Danilov, Notten` · `Danilov D., Notten` · `5569` · `53 (2008)` · `53(17)` · `electacta.2008.02.086` · "ionic transport in the electrolyte" · "Mathematical modelling of ionic")으로 각 digest 의 **후속 절**을 다시 셌다: **26호 §11(:382 · ★★ · [20]) · 91호 후속 표(:606 · ★★★ · [27]) · 98호 후속 표(:695 · '도착' 행 · [28]) · 100호 후속 표(:580 · '도착' 행 · [26]) = 4 — 원장 "4"(2026-10-03 원장 L289)와 일치**(정정 없음 · 원장 등급 ★ ↔ 26호 digest ★★ · 91호 digest ★★★ — 91호가 '상향 후보' 로 적어 둠). 교차 기록(지목 아님): 99호 :419 · 92 · 93 · 94 · 95 · 96 · 97호 "4차 묶음 13 편과의 관계" 문장(인용 0) · 100호 :17 · :450 · 98호 :17 · :569 관계 문장 · 91호 :61 · :195 · :391 · :495(본문 · 참고문헌 표) · 26호 :133(본문) · 카드 · 로그의 26 · 91 · 98 · 100호 항(digest 후속 절 아님). 이 편은 우리 digest 를 **인용하지 않는다**(2008 편 — 18 번호 전수 대조) · 4차 묶음 다른 13 편도 인용 0(전부 이 편보다 뒤 — Xie 2008 은 같은 해 · 인용 0).

이 digest 의 일 (지시):

1. **(a) 이 편의 전해질 모형** — 운반체(Li⁺ · PF₆⁻) · 전기중성 가정 → 수정 확산계수 · 해리 확장(초록) · 표 1 매개변수의 출처.
2. **(b) 26호가 이 편에서 가져간 가정('SE 에 농도 구배' · 이온 + 공공)** 이 이 편 지면에 실제로 있는가 — 고체 전해질(단일 이온 전도체 · 공공 기구)로 옮기는 근거가 이 편에 있는가, 아니면 91 · 98 · 26호 쪽의 이식인가 — 판정(조건 붙여).
3. **(c) Q4** — 해당 없음이면 그렇게.
4. **(d) 후속 후보**(있으면 액체셀 표시).
5. **★ 중심 표** — 지목 넷(26 · 91 · 98 · 100호)이 이 편에서 가져간 식 · 가정 ↔ 이 편 지면에 실제로 있는가(✅ / 부분 / ❌).
6. **계보 의문** — 99호 그림의 '전체 모형' 은 Nernst 항 없이(99호 D1) · 100호 재풀이는 그 항을 넣어야 그림과 맞음 · 98호 이원 가정 몫 ≈8 % ↔ 91호 ≈71 % — 원전의 전해질 과전압 · 농도 과전압 정의(전기중성 · 수정 확산계수 · 해리)가 그 식들의 원형인지, 그 항이 어떤 꼴로 인쇄돼 있는지.

⚠ **표기 규약**: `[인쇄]` = 원문이 실제로 쓴 것 · `[도표]` = 그림을 눈으로 읽은 값(판독 폭 표시) · **`[도표·화소]`** = 원본 래스터(≈200 dpi JPEG)를 PDF 에서 꺼내 축 눈금 화소로 보정해 읽은 값(그림 8 0.74 mV/px · 그림 9 0.053 mV/px · 그림 11 ≈0.9 mV/px((D) 10.8) · 그림 12 1.25 mV/px · 선 두께 2–3 px — 저자 원자료가 아니다) · `[재현]` = 원문 수치 · 식으로 우리가 다시 계산(T 298.15 K = 표 1 의 25 °C · R 8.314462618 · F 96485.33212 · 우리 유한체적 재풀이 300 칸 · BDF) · `[재현·가정]` = 가정이 붙은 재현(가정을 같이 적는다) · `[재현·대수]` = 인쇄된 식만으로 한 대수 · `[해석]` = 우리 해석 · **"(N호 digest 전사)"** = 이 세션에서 그 원문을 다시 열지 않고 우리 digest 의 전사로 대조한 것. **`[데이터]` 0** — 예치 원자료 · 코드 공개 진술 0.

⚠ **측정 · 인용 · 모형 · 적합 구분**: 이 편 안의 수치는 ① **측정 하나** — 그림 9(in-house 300 mAh Lithylene 셀 · 0.4C ≈30 min 충전 + 이완 · "two spatially separated in-situ Li micro-reference electrodes" 사이 전압 — "measured continuously" · 표지로 표시) ② **인용** — 표 1 CGR17500 값 전부("The relevant parameter values for this battery type are all taken from Ref. [11]" — Bergveld · Kruijt · Notten 2002 책) · Lithylene 행(출처 각주 0) · "LiPF6 in PC is only dissociated for about 80% [18]"(학회 요약) · "recently reported results [13]" ③ **모형 출력** — 그림 2–8 · 10–12 · R₀ ≈0.0506 · R_ss 0.1950 Ω("simulated") · x 0.9017 ④ **선택 값** — k_a 10⁻⁵ · D_LiPF6 2×10⁻¹¹ · δ 0.80 / 0.85 / 0.70 / 0.6569("some additional parameter values have to be chosen") ⑤ **적합 0** 이다.

⚠ **쪽 표기**: PDF 10 쪽 = 인쇄 쪽 **5569–5578**(카탈로그 `/PageLabels` 가 십진 5569 부터 — PDF 쪽 = 인쇄 쪽 − 5568). 이 digest 는 인쇄 쪽 **"p. 5572"** 로 적는다.

⚠ **기호**: 이 편의 **y 는 음극(LiC₆) 계면 = 0 · 양극(LiCoO₂) 계면 = L**(그림 1 — 오른쪽에서 왼쪽으로) · 그림 2–7 · 10 의 y 축은 무차원(0–1.0) · **δ** = 염의 평형 해리 분율(91 · 98 · 100호의 δ — SE 의 이동 Li 분율 — 와 같은 자리 · 다른 물리) · **t₊ = D₊/(D₊ + D₋)**(식 20 — 확산계수 비로 정의한 묽은 용액 운반수) · 이 편의 **'diffusion overpotential'** = 식 (30) 첫 항 (RT/F) ln[c(L)/c(0)](99 · 100호 digest 의 'Nernst 항' 과 같은 항 — 이 편 본문의 `Nernst` 3 회는 전부 'Nernst–Planck') · **'migration overpotential'** = 둘째 항 −∫E dy = φ(L) − φ(0) · c = c_Li⁺ = c_PF₆⁻(전기중성) · D₊ = D_Li⁺ · D₋ = D_PF₆⁻ · D_amb = 2D₊D₋/(D₊ + D₋)(이 편의 D) · x = IL/(4FAc₀D₊)(식 38 앞 — 이 편 글자). 텍스트 층에서 η · μ 는 제어 문자, δ 는 'ı' 로 깨진다(아래 텍스트 층).

---

# 판정 먼저

1. ★★★★ **(b) 'SE 에 농도 구배 · 이온 + 공공' 은 이 편 지면에 없다 — 이 편은 액체 유기 전해질의 중성 이온쌍(LiPF₆ ⇌ Li⁺ + PF₆⁻) 모형이고, 고체로 옮기는 근거는 0 이다. 옮겨진 것은 식의 꼴(전기중성 → 수정 확산계수 · D₊ 만 든 경계 · 전기장 닫힌 꼴 · η 정의)이고, 고체 판의 물리(n⁻ = nBO 미보상 전하 · 고정 Li⁰ · 공공 · 국소 닫음)는 91 · 98호의 이식이다.** `[인쇄]` `solid` · `vacanc*` · `glass` · `polymer` · `LiPON` · `Li3PO4` · `ceramic` · `single-ion` 본문 · 참고문헌 **0 회** · 운반체 "Li+ and PF6− ions" · 해리 "The dissociation reaction of LiPF6 in an organic solvent"(식 43) · 확장의 동기 "LiPF6 in PC is only dissociated for about 80% [18]" · 결론 "simulate the ionic conductivity of organic electrolytes in Li-ion batteries" · 다른 계 언급은 "planar electro-chromic devices [14]" 하나(고체 전해질 아님). ⇒ 26호 §11 의 지목 이유("해리 전해질 수송(이온 + 공공)의 원전")는 **절반만** 맞다 — 해리 · 두 운반체 · 전기중성 식의 원전 ✅ · '공공' ❌(98호 Raijmakers 원문의 이름 — "uncompensated negative charge associated with a vacancy formed in the LiPON matrix" · 98호 digest 전사 · 91호 원문은 `vacanc*` 0 — 91호 digest 전사) · 'SE 에 농도 구배' 의 근거 ❌(이 편의 농도 구배는 액체에서만 — 그림 2 · 식 33). ★ 그리고 `[재현·가정]` **SE 판에서 농도 구배의 크기는 원전이 아니라 이식의 중성종 닫음이 정한다**: 이 편 표 1 + δ 0.8 · k_a 10⁻⁵ · 50 min 에서 이 편 닫음(중성 LiPF₆ 의 확산 PDE — 식 46)은 확산(농도) 항 **74.0** · 이동 86.1 · 합 **160.1 mV** · 98호식 국소 닫음(c₀ = c_Li⁰ + c_n — 98호 digest 전사)으로만 바꾸면 **7.4 · 46.3 · 53.6 mV**(농도 항 ×0.10) · 중성종을 고정하면(91호 "immobile, oxygen-binded lithium" 쪽 극한 — 91호 digest 전사) 50 min 한계 δ 가 0.604 → **0.897**(표 1 L). ⚠ 조건: 이 편 액체 매개변수에 닫음만 바꾼 반사실 계산이다 — SE 값이 아니다.
2. ★★★★ **(중심 표) 지목 넷이 가져간 것 — 식은 ✅, 물리는 ❌.** 26호(Iwakiri 식 22 · 23b · 25 · 26 의 꼴 ✅ · '이온 + 공공' ❌ · 'SE 농도 구배' 근거 ❌) · 91호(식 18 · 19 · 20 · n⁻ 차단 경계 · 평형 관계 ✅ · n⁻ 의 정체 ❌(원전 음이온은 PF₆⁻ — 답하지 않는다) · k_r 대조처 ❌(원전 k_a 는 '선택 값' · 액체) · Li⁰ 고정 ❌(원전 중성종은 확산한다)) · 98호(식 23–24 ✅ · 식 31 부분(원전은 염의 두 이온 — 양극 이온 · 전자 쌍으로의 이식은 98호) · 국소 닫음 ❌) · 100호(식 9 ✅ Nernst 항 포함 · 식 10 ✅). 표는 아래 **중심 표**.
3. ★★★★ **99 · 100호 의문 — Nernst 항은 원전 정의의 일부다.** `[인쇄]` 식 (26)–(27) "The difference in electrochemical potentials between both electrode/electrolyte interfaces represents the concentration polarization across the electrolyte": η = (1/z_Li⁺F)[μ̄_Li⁺(L) − μ̄_Li⁺(0)] = (RT/F) ln[c_Li⁺(L)/c_Li⁺(0)] + (φ(L) − φ(0)) · 식 (30) · 그림 8 은 첫 항(곡선 b · "diffusion")과 둘째 항(곡선 c · "migration")을 따로 그리고 합(곡선 a)을 총 과전압으로 쓴다. `[재현]` 우리 PDE 재풀이(표 1)가 그림 8 의 세 곡선을 0.3–50 min 에서 **±1 mV**(이동 ±0.3 mV · `[도표·화소]`)로 다시 낸다 — **원전은 두 항을 다 넣고 계산했다**. ⇒ 100호 원 PDE(Nernst 항 포함 — 100호 digest 전사)가 원전 정의를 따른 구현이고, 99호 그림(둘째 항만 — 99호 D1)은 원전의 η 가 아니라 정전 전위 차 φ(L) − φ(0) 다(`[해석]`). 그리고 `[인쇄]` 정상 상태에서 두 항은 같다(식 35–36 · "the diffusion and migration contributions are balanced and both are equal to (RT/F)ln(c(L)/c(0))") — **둘째 항만 쓰면 정상 η 의 정확히 절반**(완전 해리 · 이상 묽은 용액 · 일정 D 조건 · D₊ · D₋ 값과 무관) — 99호 '플랜트가 전해질 분극의 ≈절반(300 s 에서 18.4 / 37.6 mV)을 빼고 계산됐다'(99호 digest 전사 — 해리 SE · 300 s 에서도 0.49)와 같은 자리다. ⚠ 해리 확장(그림 11 · 12)에서는 두 항이 같지 않다(이동 > 확산 — δ 0.70 에서 132.7 ↔ 110.2 mV `[도표·화소]`). ⚠ 이름: 이 편은 첫 항을 'Nernst' 라 부르지 않는다 — 'Nernst 항' 은 99 · 100호 digest 의 이름이고 98호 원문은 'Nernstian · Galvanic'(98호 digest 전사).
4. ★★★★ **성분 이름은 정의 분할이다 — 같은 지면 안의 측정 분할과 다르다.** `[인쇄]` 끄는 순간 낙차 η_down = 2t₊(RT/F) ln[c(L)/c(0)](식 41) · η_down/η_ss = t₊(식 42 — "Elegantly, this ratio is exactly given by the Li+ transference number") — 순간에 사라지는 것은 'migration' 성분(정상 (RT/F) ln = 절반)이 아니라 t₊ 에 비례하는 몫이다. `[재현]` 표 1(t₊ 0.4): 정상 η_ss **137.26 = 확산 68.63 + 이동 68.63 mV**(정의 분할 1 : 1) ↔ 끄는 순간 낙차 **54.90** · 남는 **82.35 mV**(측정 분할 0.4 : 0.6 — `[재현·대수]` 묽은 용액 전도도 κ = F²c(D₊ + D₋)/RT 로 옴 강하를 적분하면 2t₊(RT/F) ln 이 나와 Newman 형 '옴 ↔ 농도' 분할과 같은 값) · 그림 8 곡선 (d) `[도표·화소]` 82.0 mV ✅. ⇒ **같은 총 과전압에 성분 이름이 두 벌**이다 — 'migration overpotential' 은 전류를 끊는 실험으로 재는 양이 아니다(`[해석]`). 우리 degeneracy 물음("곡선이 맞는다 ≠ 분해가 맞다")의 원전 층 표본 — 카드 · truth 에서 'Nernst · diffusion · migration · ohmic' 을 옮길 때 분할 규약을 같이 적어야 한다(새 판단 거리 2).
5. ★★★★ **표 1 은 지면의 그림을 다 닫지 않는다 — 두 매개변수 상태가 섞였다(인쇄 0).** `[재현]` 표 1 CGR17500 값(L 2.8×10⁻⁴ m)으로 x = IL/(4FAc₀D₊) = **0.8706** ↔ 인쇄 "x is calculated to be 0.9017" — 0.9017 은 **L = 2.900×10⁻⁴ m** 이면 넷째 자리까지 나온다. (i) **표 1 로 닫히는 것** — 그림 8(재풀이 ±1 mV) · 그림 11(A)(RMS 0.96 mV) · 그림 3 바닥 "about −1200 V/m"(−1235 · L 2.9×10⁻⁴ 이면 −1625) · "almost two times higher"(그림 4 · 1.92 · L 2.9×10⁻⁴ 이면 2.05) — 정상 플럭스 값("about −18 × 10⁻⁵" · "28 × 10⁻⁵" ✅)은 L 과 무관해 두 상태를 가르지 못한다 (ii) **L 2.9×10⁻⁴ 로만 닫히는 것** — 인쇄 x 0.9017 · "61% of the tLi+ value"(0.609 ↔ 표 1 0.652) · 그림 11(B)(C)(RMS 1.06 · 0.83 mV ↔ 표 1 이면 15.5 · 34.3 mV) · 그림 12 전 구간(δ 0.70–0.997 ±3 mV — δ→1 끝 `[도표·화소]` 151.6 ↔ 152.4 · 표 1 이면 137.4) · 한계 δ "0.6569"(재풀이 0.6576 ↔ 표 1 이면 0.6037) (iii) **어느 쪽도 아닌 것** — R_ss 0.1950 Ω(표 1 0.1906 · L 2.9×10⁻⁴ 0.2114 — x 0.8778 에 해당) (iv) **표 1 Lithylene 행만으로 안 닫히는 것** — 그림 9(아래 6). ⇒ **한 그림(11) 안에서도 (A) 와 (B)–(D) 가 다른 L 이다.** ★ 그리고 완전 해리의 정상 값은 x 묶음(I·L/(A·c₀·D₊)) 하나의 함수라(식 37) 그 차이가 묶음 안의 어느 매개변수인지 안 갈린다 — **해리 판 그림 11(C) 의 시간 경과(5–49.5 min)가 가른다**: 같은 x 를 주는 한 매개변수 변경 넷 중 **L 만 RMS 0.83 mV** · I/A 5.49 · c₀ 6.92 · D₊ 5.86 mV(`[재현]` 재풀이 ↔ `[도표·화소]` ±0.9 mV/px) — 시간 척도 L²/D_amb 가 정상 묶음을 깬다(곱 축퇴 처방 4단계의 원전 안 표본 · 아래 §곱 축퇴).
6. ★★★ **그림 9 '실험 검증' — 측정 하나 · 기준극 위치 미인쇄 · 표 1 행만으로는 안 닫힌다.** `[인쇄]` "The presented model has been experimentally verified. A typical example is shown in Fig. 9. The experiment relates to an in-house prepared 300 mAh Lithylene battery [17] … The voltage drop across the electrolyte was measured by using two spatially separated in-situ Li micro-reference electrodes [13]. … continued for about 30 min with a constant-current of 0.4 C. … Good agreement between the experiment and model is found during both the current flowing and current interruption periods. A more detailed comparison … will be presented in a separate publication." `[도표·화소]` 선 정상 **9.95 ± 0.1 mV** · 켬 ≈0 min(눈금 보정 ±0.4 min) · 끔 ≈31.6 min · 끈 직후 ≈5.0–5.2 mV 로 수직 하강 · 표지(회색 타원)는 선 위에 겹침 · 잔차 · 오차 표기 0. `[재현]` 표 1 Lithylene 행(D₊ = D₋ 1.07×10⁻¹¹ · L 9.5×10⁻⁵ · c₀ 1000 · I 0.12 A = 300 mAh 의 0.4C · A 8.9×10⁻³ · t₊ 0.5)으로 전 두께를 풀면 정상 **32.96 mV(×3.3)** · 켜는 순간 15.94 mV. `[재현·가정]` 두 기준극이 전해질 가운데 **29.6 µm 구간**(두께의 0.311)에 있다고 두면 선이 상승 ±0.15 · 감쇠 ±0.4 mV 로 닫힌다(같은 정상값을 전 두께 · 전류 ×0.311 로 주면 끈 뒤 값이 그림의 0.6–0.7 배 — ✗). 그리고 선의 끈 직후 낙차 / 정상 ≈0.48–0.50 ≈ t₊ 0.5 — 식 (42) 처방을 이 그림에 쓸 수 있는데 지면은 하지 않았다. ⇒ '실험으로 검증' 은 셀 하나 · 그림 하나 · 위치 미인쇄 입력에 기대고, CGR17500(그림 2–8 · 11 · 12 · R₀ · R_ss 의 셀)의 실험은 지면에 0 — "the ohmic resistance is simulated to be R0 ≈0.0506 (Ω), which is in the good agreement with experimental results" 의 실험값 · 출처 0.
7. ★★★ **(a) 해리 확장의 결론은 중성 이온쌍의 확산에 매달린다 — 그리고 식 (42) 는 해리 경우에 깨진다.** `[인쇄]` "Simulations have been performed with δ = 0.85 (B), 0.70 (C) and 0.6569 (D). The later value corresponds to situation when 1 C-rate becomes a limiting current." · "Migration is, however, most responsible for the explosive nature of the overpotential increase and hence of major importance of poorly dissociated electrolytes." `[재현]`(L 2.9×10⁻⁴ 상태) 한계 δ **0.6576** ✅ — 중성 LiPF₆ 를 고정(D_LiPF6 → 0)하면 같은 50 min 한계 δ 가 **0.923**(표 1 L 이면 0.604 → 0.897): 해리도 0.66 까지 1C 를 버티는 것은 중성 염이 고갈된 음극 쪽으로 확산해 다시 해리하기 때문이다(`[해석]` — 지면은 이 기구를 말하지 않는다). 그리고 식 (42) 의 유도 전제(정상에서 두 성분 같음 — 식 36)는 해리 확장에서 깨진다 — `[재현]` δ 0.8 · 50 min: 낙차 / 정상 = 71.3 / 160.1 = **0.445**(L 2.9×10⁻⁴ 이면 0.441) ↔ t₊ 0.4. 지면은 식 (42) 를 해리 경우에 쓰지 않았지만 결론은 조건 없이 "this facilitates the way to perform simple experiments to determining the transference numbers" 라 쓴다.
8. ★★★ **(c) Q4 — 해당 없음(액체 모형 원전 · 매개변수 추정 0) · 식별 쪽 문장 둘.** `[인쇄]` `identif*` · `estimat*` · `uncertain*` · `error` · `sensitiv*` · `fit` · `optimi*` 본문 0 회 · 식별 쪽 문장은 둘 — 식 (42) 뒤 "delivers a nice tool to obtain this value experimentally" · 식 (37) 뒤 "In contrast to η0 (Eq. (32)), ηss (Eq. (37)) only depends on DLi+ and is independent on DPF6−. It should, however, be noted that DPF6− certainly affects the overpotential in the transition region" — 정상 관측만으로는 D₋ 가 안 보인다는 구조 문장(`[해석]` 식별 어휘 없이 인쇄된 비식별 방향). `[재현·대수]` 관측 ↔ 묶음: η₀ ↔ I·L/(A·c₀·(D₊ + D₋))(전도도) · η_ss ↔ x = I·L/(4F·A·c₀·D₊) · η_down/η_ss ↔ t₊ · 과도 시간 ↔ L²/D_amb · 그리고 완전 해리 모형의 모든 출력은 I/(A·c₀) 로만 — **면적(전류 밀도) ↔ 염 농도 정확 대칭**. ⇒ **ASSB 0/101 — 아흔세 번째 성질**(아래 §(c)) · 누적 0.5 그대로.
9. **채움표** — Q1 해당 없음(`θ(N)` 0/101 · 액체 · 전극 0) · Q2 없다(ASSB 관측 0 — 액체 셀 하나의 기준극 쌍 전해질 전압 · 위치 미인쇄) · Q3 층 하나("모형 원전 — 표 1 = [11] 책 값 · 지면 그림은 두 매개변수 상태(표 1 ↔ x 0.9017 · 인쇄 0) · 성분 이름 = 정의 분할(측정 분할 2t₊ : 2(1−t₊)) · 실험 = 다른 셀 그림 하나") · **Q4 해당 없음 — ASSB 0/101 · 아흔세 번째 성질** · Q5 해당 없음(액체 · 기준극 = 전해질 안 Li 미세 기준극 쌍 · η = Li⁺ 전기화학 퍼텐셜 차라는 정의 하나) · Q6 해당 없음(`pressure` 0) · Q7 해당 없음 · Q8 해당 없음(OCV 0 — 전해질만 · δ 80 % = [18] 학회 요약). **누적 ≈20.0 → ≈20.0 (새 칸 0).**

---

# ★ 중심 표 — 지목 넷이 이 편에서 가져간 것 ↔ 이 편 지면 (✅ 있다 · 부분 · ❌ 없다)

지목은 각 digest 후속 절의 지목(26 · 91 · 98 · 100호)만이다. 99호는 이 편을 인용하지 않지만 같은 식을 쓰므로 맨 아래 교차 행으로 둔다. 둘째 열은 그 digest 의 전사(원문 재열람 0), 셋째 열은 이 편 지면(`[인쇄]` — 식은 쪽 렌더로 확인).

| 지목 호 (참고 번호 · 후속 행) | 가져간 것 (그 digest 전사) | 이 편 지면 | 판정 |
|---|---|---|---|
| **26호** Iwakiri 2024 ([20] · §11 ★★ :382) | Iwakiri 식 (22) ∂a/∂t = [2D_M⁺D_N⁻/(D_M⁺ + D_N⁻)] ∂²a/∂y² + r | 식 (47.1) ∂c/∂t = D ∂²c/∂y² + r · D = 2D_Li⁺D_PF₆⁻/(D_Li⁺ + D_PF₆⁻)(식 14 아래) | ✅ 꼴 같음 |
| 〃 | Iwakiri 식 (23b) ∂a(0,t)/∂y = I⁻/(2D_M⁺AzF) — "경계는 D_M⁺ 만" | 식 (14.3)–(14.4) · (47.3)–(47.4) ∂c/∂y = I(t)/(2FAD_Li⁺) — 식 (9.3) × D_PF₆⁻ + (10.3) × D_Li⁺ 에서 나옴(식 12–13) | ✅ |
| 〃 | Iwakiri 식 (25) E = (RT/F)(1/a){−I/(2FAD_M⁺) + [(D_M⁺ − D_N⁻)/(D_M⁺ + D_N⁻)][∂a/∂y − I/(2FAD_M⁺)]} | 식 (19) 글자 그대로(렌더 확인) · 해리 확장에서도 "The intensity of the electric field in the electrolyte is again described by Eq. (19)" | ✅ |
| 〃 | Iwakiri 식 (26) η_mt = (RT/F) ln[a(J)/a(0)] − ∫E dy | 식 (30) — 정의는 식 (26)–(27)(Li⁺ 전기화학 퍼텐셜 차) | ✅ |
| 〃 | "이 모델의 SE 에는 농도 구배가 있다(이온·공공 쌍, Danilov & Notten 2008 계열)"(:133) · 후속 이유 "해리 전해질 수송(이온 + 공공)의 원전 — 'SE 에 농도 구배' 가정의 출처" | 운반체 = Li⁺ · PF₆⁻(유기 액체 전해질) · 해리 = 중성 LiPF₆ 이온쌍(식 43) · `solid` · `vacanc*` · `single-ion` 0 회 · 농도 구배는 액체에서만(그림 2 · 식 33) | **❌**(공공 · 고체 · 고체로 옮길 근거) · 해리 이원 수송의 원전 ✅ |
| **91호** Danilov 2011 ([27] · 후속 ★★★ :606) | 식 18 "It can be shown[27]" — 해리 이원 전해질 두 운반체 → 확산-반응 식 하나 · 경계 ∂a/∂y = I/(2FAD_Li⁺) · a(y,0) = δa₀ | 식 (44)–(45) → (47.1)–(47.4) · 초기 δc₀(식 47.2) · 유도는 "Rearranging Eqs. (44)–(45) under the electro-neutrality condition" | ✅ |
| 〃 | 식 19 전기장 · 식 20 η_mt = 확산("diffusion") + 이동("migration") | 식 (19) · (30) · 이름도 같음(그림 8 · 11 · 12 캡션) | ✅ |
| 〃 | n⁻ 의 두 경계 유속 0(식 17c · d) | PF₆⁻ 유속 0(식 5.3–5.4 · 7.3–7.4) | ✅ |
| 〃 | 평형 a_Li⁺ = a_n⁻ = δa₀ · a_Li⁰ = (1 − δ)a₀ · k_d = k_r a₀δ²/(1 − δ) | c^eq_Li⁺ = c^eq_PF₆⁻ = δc₀ · c^eq_LiPF₆ = (1 − δ)c₀ · k_d/k_a = c₀δ²/(1 − δ)(p. 5575) | ✅ 꼴 · 이름만 다름(k_a ↔ k_r) |
| 〃 | n⁻ 의 정체("uncompensated negative charges … nBO's" · `vacanc*` 0 — 공공으로 읽으면 "Li⁺ only" 와 화해 — "원전 파일 61 에서 확인") | 음이온 = PF₆⁻(액체 염의 음이온) · 공공 · 미보상 전하 · 유리 · nBO 0 | **❌** — 원전은 이 물음에 답하지 않는다(물리가 다름) |
| 〃 | k_r · δ 값과 단위 — "k_r ×100 판정의 둘째 대조처" | k_a = 10⁻⁵ m³ mol⁻¹ s⁻¹(단위 같음) · δ 0.80 — "some additional parameter values have to be chosen"(선택 값 · 액체 · 출처 0) | **❌** 대조처 못 됨 — `[재현]` δ 0.8 에서 k_d 0.048 s⁻¹ · 반응 이완 τ = 1/(k_d + 2k_aδc₀) 13.9 s · 반응층 λ = √(D_amb τ) 18.3 µm(L 의 6.5 %) |
| 〃 | Li⁰ = "immobile, oxygen-binded lithium"(91호 식 14) · 91호 digest 재풀이 닫음 r = k_d(a₀ − a) − k_r a² | 중성종 LiPF₆ 는 **확산한다**(식 46 · D_LiPF₆ 2×10⁻¹¹ · 두 경계 유속 0 — "the un-dissociated salt is not consumed") | **부분** — 반응 꼴 ✅ · 중성종 수송 ❌(이식은 91호 쪽) |
| **98호** Raijmakers 2020 ([28] · '도착' 행 :695) | 식 (23)–(24) "see Refs. [11,28]" — 해리 확산-반응 + 경계 · 전기장 | 식 (47) · (19) | ✅ |
| 〃 | 식 (31) 양극(LiCoO₂) 전기장 — 이온 Li⊕ + 전자 쌍에 같은 꼴 · D⁰_p = 2D_Li⊕D_e⁻/(D_Li⊕ + D_e⁻) | 염의 두 이온(Li⁺ · PF₆⁻)만 — 혼합 전도체 · 전자 운반체 0 | **부분** — 수학 꼴만 · 이온–전자 쌍으로의 이식은 98호 |
| 〃 | n⁻ = 공공("vacancy formed in the LiPON matrix") · 국소 닫음 c₀ = c_Li⁰ + c_n("the total lithium concentration in the electrolyte … must be constant") | 공공 0 · 중성종 확산 PDE(식 46) — 총 염은 전역 보존(경계 유속 0)이지 국소 상수가 아니다 | **❌** — `[재현·가정]` 닫음만 바꿔도 농도 항 74.0 → 7.4 mV(δ 0.8 · 50 min) |
| **100호** Deng 2021 ([26] · '도착' 행 :580) | 식 (9) η_mt = (RT/F) ln[c(L_e)/c(0)] − ∫E dx "[26]" — 100호 원 PDE 는 Nernst 항 포함(재풀이 ±0.05 mV) | 식 (30) · 그림 8 은 두 항을 다 계산(`[재현]` ±1 mV) | ✅ — 100호 구현 = 원전 정의 |
| 〃 | 식 (10) 전기장 닫힌 꼴 "[26]" | 식 (19) | ✅ — 100호 식 (28) 'D_e' 자리 = 이 편 비 (D₊ − D₋)/(D₊ + D₋)(100호 D6 의 원형) |
| (교차 · 지목 아님) **99호** Kim 2019 (인용 0) | 99호 식 (14) η_mt = (RT/F) ln[c(L)/c(0)] − ∫E dy · 식 (15) 전기장(전류 부호 관례 반대) — 그림은 둘째 항만(99호 D1) | 식 (30) · (19) — 정의는 두 항의 합 | 식 ✅ · 그림 구현은 원전 정의와 다름(`[해석]`) |

**셈**: 지목 넷이 가져간 열일곱 줄 중 **✅ 11 · 부분 2 · ❌ 4**(❌ = 26호 '공공 · SE 농도 구배' · 91호 'n⁻ 의 정체' · 91호 'k_r 대조처' · 98호 '국소 닫음' · 부분 = 91호 'Li⁰ 고정' · 98호 '식 (31) 이온–전자 쌍'). 식은 원전에 있고, 고체로 옮기는 물리(무엇이 n⁻ 인가 · 중성종이 움직이는가 · 무엇이 보존되는가)는 원전에 없다.

---
# 서지

| 항목 | 값 (`[인쇄]` — p. 5569 · p. 5578 · 정보 사전) |
|---|---|
| 제목 | **"Mathematical modelling of ionic transport in the electrolyte of Li-ion batteries"**(지면 — 정보 사전 title 은 "doi:10.1016/j.electacta.2008.02.086") |
| 저자 · 소속 | **D. Danilov** — a Eurandom, Den Dolech 2, 5600 MB Eindhoven · **P.H.L. Notten**(교신 · ¹ "Member of the International Society of Electrochemistry") — b Eindhoven University of Technology, Den Dolech 2, 5600 MB Eindhoven · c Philips Research Laboratories, High Tech Campus 4, 5656 AE Eindhoven(전화 · 팩스 · 메일 인쇄 — 옮기지 않음) · Danilov = 91 · 98호 공저자 · Notten = 91 · 98호 공저자(91 · 98호 digest 전사) |
| 저널 | *Electrochimica Acta* **53**, **5569–5578**(2008) · doi `10.1016/j.electacta.2008.02.086` · "0013-4686/$ – see front matter" |
| 일정 | Received **22 November 2007** · revised **15 February 2008** · accepted **21 February 2008** · available online **2 March 2008** · `[재현]` 접수 → 수락 **91 일** · 수락 → 온라인 10 일 |
| 저작권 | "© 2008 Elsevier Ltd. All rights reserved." · OA 표기 0 ⇒ **구독본으로 다룬다** — 이 digest 는 인용 · 요약 · 재현 계산만 담고 그림 크롭은 위키 관례대로 `raw/figures/`(변형 없는 잘라내기) |
| 키워드 | Li-ion battery · Ionic transport · Organic electrolytes · **"Nernst–Plank equations"**(인쇄 그대로 — 오자) · Electro-neutrality |
| 자금 · 감사 | 자금 진술 0 · 이해 상충 진술 0 · 감사: H.T. Hintzen(TU/e) · J. Zhou · L.F. Feiner(Philips Research Eindhoven) "for valuable discussions" |
| 코드 · 자료 | **공개 진술 0** · "standard MATLAB pdepe solver and applying discretization steps with a space variable of L/200 and adaptive time steps" |
| 분량 | 10 쪽(본문 9 쪽 + 참고문헌 1 쪽) · 그림 **12**(전부 ≈200 dpi JPEG 래스터 — 회색 1 · 8 · 9 · 11 · 12 · RGB 2–7 · 10) · 표 **1** · 번호 식 **(1)–(47)**(하위 번호 4.1–4.4 · 5.1–5.4 · 6.1–6.4 · 7.1–7.4 · 9.1–9.4 · 10.1–10.4 · 14.1–14.4 · 46.1–46.4 · 47.1–47.4) · 참고문헌 **[1]–[18]**(빠진 번호 0 — p. 5578 목록에서 직접 셈) |
| 절 | 1. Introduction · 2. Theoretical considerations(2.1 Model set-up · 2.2 Electro-neutrality condition · 2.3 Overpotentials) · 3. Results and discussion(3.1 Concentration profiles, electric field and ionic fluxes · 3.2 Overpotentials and resistances · 3.3 Salt dissociation) · 4. Conclusions · Acknowledgements · References |
| 셀 | **모형 셀** — Sony **CGR17500** 원통형(720 mAh · LiCoO₂ ‖ 흑연 · LiPF₆ — 표 1 첫 행 · 값은 [11]) · **실험 셀** — in-house **Lithylene** 300 mAh("based on conventional Li-ion chemistry" · [17] · 표 1 둘째 행) · 셀 제작 · 측정 조건(온도 · 기준극 위치)은 그림 9 캡션 · 본문 몇 줄뿐 |
| 모의 | 1C 정전류 충전 50 min + 이완(80 min 까지 — 그림 2–8 · 10 · 11) · 0.1C(문장 — 식 38 비) · δ 1 · 0.85 · 0.70 · 0.6569(그림 11) · δ 0.65–1.00 의 50 min 값(그림 12) · Lithylene 0.4C ≈30 min + 이완(그림 9) |
| 모형 | 1D · 등온 25 °C · **전해질만**(전극 · 전하이동 · 부반응 0 — "Since no side reactions are considered to take place in the present model") · 대류 0("it is assumed that no convection takes place") · 두 운반체 Nernst–Planck(식 3) · 경계 = 두 계면의 전류(식 4.3–4.4 · 5.3–5.4) · 전기중성(식 8 — Maxwell 방정식 대신 "a simplifying assumption is furthermore required") → D_amb 확산 하나(식 14) + 전기장 닫힌 꼴(식 19 · 21) · 운반수 = 확산계수 비(식 20) · 이상 묽은 용액 화학 퍼텐셜(식 26 — 활동도 · 열역학 인자 0) · η = Li⁺ 전기화학 퍼텐셜 차(식 27 · 30) · 해리 확장 = LiPF₆ ⇌ Li⁺ + PF₆⁻(k_d · k_a — 식 43) + 중성종 확산(식 46) |

**PDF 메타데이터 (이 실행에서 직접 읽음 · pymupdf)** — **1,996,390 B** · sha256 `f427e8738b49cb4193e0b8f50b6572456d248431fd29cf3a147122288edf14a5`(호출자 명시값 ✅ — 직접 재계산) · 헤더 `%PDF-1.7` · 10 쪽 전부 595.30 × 793.79 pt · 암호 0 · 정보 사전: title **"doi:10.1016/j.electacta.2008.02.086"** · author **""**(빈 값) · subject **""** · keywords "" · creator **"Elsevier"** · producer **"Acrobat Distiller 7.0 (Windows)"** · 생성 **D:20080429182246Z** · 수정 **D:20080429190135+05'30'**(호출자 메모와 같음 ✅ — 생성 · 수정이 온라인 게재(3 월 2 일) 뒤 4 월 29 일 — 권호 조판본으로 읽힘 · 판정 안 함) · 트레일러 ID [5E8D790AE03D90FAC8E3D93C9982C5D5 · 6F33CD8F72E1AF4CB1F7A93755701DD5] · XMP **3,531 B**(`pdf:Producer` · `xap:CreatorTool` Elsevier · `xap:CreateDate` 2008-04-29T18:22:46Z · `xap:ModifyDate` 2008-04-29T19:01:35+05:30 · `dc:title` = doi · `dc:creator` 빈 항목 하나 · `xapMM:DocumentID` uuid:a31d2c3c-3dc9-4fcd-827d-d8a3fbc25934 · `InstanceID` uuid:48879362-75f8-4221-b68b-f098f7beb183 · CrossMark · prism 0) · 카탈로그 `/PageLabels`(십진 5569 부터 — 인쇄 쪽과 같음) · `/Outlines` · `/Threads` · `/Names` → `/Dests` 만(**EmbeddedFiles 0** · `embfile_count()` 0) · `%%EOF` 1 · `startxref` 1(증분 저장 흔적 0) · 래스터 **14**: p. 5569 의 RGB JPEG 둘(Elsevier 로고 166×182 · 학술지 표지 158×199 — 그림 아님) + 그림 1–12 의 JPEG 열둘(그림 1 667×510 회색 · 2 671×458 · 3 664×459 · 4 667×464 · 5 649×900 · 6 670×916 · 7 640×925 · 8 568×424 회색 · 9 588×457 회색 · 10 671×459 · 11 983×770 회색 · 12 584×490 회색 — 놓인 크기로 모두 ≈200 dpi) · 벡터 그리기: p. 5575 의 373 개 중 354 개가 쪽 상자 밖(y > 793 pt — 제작 부산물) · 나머지 쪽은 괘선 · 분수선 수준.

⚠ **텍스트 층**: 합자 **116**(ﬁ 74 · ﬂ 42 — NFKC 로 복원 · NFKC 가 바꾸는 글자 132 = 합자 116 + ϕ 12 + ¯ 4) · **η 가 U+0005(34 회) · μ · 괄호 · 적분 기호 등이 제어 문자 U+0002–U+0010(합 36)** 로 · **δ 가 'ı'(21 회)** 로 깨진다(그림 8 캡션 필드의 'η_down' 도 U+0005 · 그림 12 캡션의 '(δ)' 도 '(ı)') — 식 (4)–(6) · (16)–(21) · (27)–(30) 과 표 1 은 **쪽 렌더 조각으로 읽었다**(170–300 dpi · 판독용 · 커밋 안 함 — 표 1 은 수동 크롭으로 커밋) · 나머지 식은 텍스트 층 + 앞뒤 대수로 복원(아래 절별 해체에 꼴을 적음) · 줄 끝 하이픈은 Elsevier 분철(복원 뒤 셈) · 어휘 집계는 NFKC · 분철 복원 · 쪽 머리(저널 줄 · 쪽 번호) 제외 · 본문(제목 → 감사) ↔ 참고문헌을 갈라 셈.

---

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **그림 9 의 기준극 위치 · 간격** — "two spatially separated in-situ Li micro-reference electrodes [13]" · "spatially spaced micro-reference electrodes in the electrolyte" 뿐 · 모형선이 어느 구간의 과전압인지 미인쇄 | `[재현]` 표 1 Lithylene 행 전 두께면 정상 32.96 mV ↔ 그림 9.95 mV(×3.3) · `[재현·가정]` 가운데 29.6 µm 구간이면 ±0.15–0.4 mV 로 닫힘 — 위치가 '검증' 의 입력이다(D7) |
| **G2** | **L · D 의 정체** — 표 1 L 2.8×10⁻⁴ m(CGR17500) · 9.5×10⁻⁵ m(Lithylene)가 분리막 두께인지 · 다공 전극을 포함한 유효 길이인지 · D 가 벌크인지 유효(굴곡 · 공극 포함)인지 미인쇄 · "all taken from Ref. [11]" 뿐 | `[해석]` 원통형 셀 분리막으로는 280 µm 가 두껍고 D 2–3×10⁻¹¹ m² s⁻¹ 는 작은 편이라 유효값으로 읽히나 지면은 말하지 않는다 — 원전 수치를 다른 셀 · 다른 계로 옮길 때 층위가 정해지지 않는다 |
| **G3** | **x 0.9017 · '61 %' · 그림 11(B)–(D) · 12 · δ 0.6569 의 매개변수** — 표 1 과 다른 값(`[재현]` L 2.9×10⁻⁴ 이면 전부 닫힘)을 썼다는 진술 0 | 같은 지면 그림들이 두 상태 — 그림을 비교 기준으로 쓸 때 그림별로 상태를 가려야 한다(D1 · D3) |
| **G4** | **R₀ · R_ss 'simulated' 의 계산 시각 · 방법** — R₀ ≈0.0506 · R_ss 0.1950 Ω — 첫 시간 단계인지 · 50 min 인지 · 해석식인지 미인쇄 | `[재현]` 해석식(표 1) 0.0497 · 0.1906 — R₀ 차 +1.8 % 는 첫 단계 확산 몫으로 설명되나 R_ss 차 +2.3 % 는 정상 아래로 다가가는 과도로는 설명 안 됨(D2) |
| **G5** | **그림 12 곡선 (d) 'migration residual'** — 캡션에만 · 본문 정의 0 | `[재현]` 식 (40)(끈 직후 남는 이동 몫) 값과 δ 0.70–0.997 에서 ±1.3 mV — 정의로 읽힘(D6) |
| **G6** | **해리 매개변수의 근거** — k_a 10⁻⁵ m³ mol⁻¹ s⁻¹ · D_LiPF₆ 2×10⁻¹¹ m² s⁻¹ = "some additional parameter values have to be chosen" · δ 80 % = "LiPF6 in PC"([18] 학회 요약 — 이 편 셀의 용매 미인쇄) | 해리 결론(그림 11 · 12 · 한계 δ)이 이 선택 값에 매달린다 — `[재현]` 중성종 고정이면 한계 δ 0.66 → 0.92 |
| **G7** | **pdepe 설정** — 시간 출력 · 허용오차 · 해리 PDE 셋의 결합 방식 미인쇄(공간 L/200 만) | 우리 재풀이(유한체적 300 · BDF)가 그림 8 · 11 · 12 를 ±1–3 mV 로 내 실질 영향은 작다 |
| **G8** | **Lithylene 셀과 실험 조건** — 전해질 · 용매 · 염 농도(표 1 c₀ 1000) · 온도 · 셀 수 · 반복 · 측정 잡음 · 기준극 안정성 미인쇄([17] · [13] 에 미룸) | '검증' 의 측정 몫이 그림 하나의 표지로만 지면에 있다 |
| **G9** | **R₀ "in the good agreement with experimental results" 의 실험값 · 출처** — CGR17500 측정 0 | CGR17500 의 모든 그림은 실험 대조가 지면에 없다(D15) |
| **G10** | **활동도 · 열역학 인자 · 농도 의존 D** — 어휘 0(`activit*` · `thermodynamic factor` · `concentrated solution` 0 회) · 식 (26) 은 이상 용액 | 1500 mol m⁻³ 의 농축 전해질에서 'diffusion' 항의 크기는 열역학 인자에 비례해 달라진다(`[해석]`) — 이 편 결론("exactly balanced")은 이상 가정 위 |
| **G11** | **전기중성 편차 계산** — "calculated to be smaller than ten orders of magnitude" — 유전율 · 방법 미인쇄 | `[재현·가정]` ε_r 30 이면 y = 0 정상 ≈1×10⁻¹⁰ — 문장 뜻("10 자릿수 작다")과 맞는다(D14) |
| **G12** | **식별 · 불확실성** — 매개변수 추정 · 감도 · 오차 막대 · 반복 0 | Q4 칸이 움직이지 않는 이유 — 관측 ↔ 묶음 대응은 우리 `[재현·대수]` 다 |

---

# 보충 자료 — 받은 것 · 대조

**SI 없음 (원문에 보충 언급 0).** 호출자 대조와 같은 결과를 이 실행에서 직접 다시 셌다 — 본문 · 캡션 · 참고문헌 전문(NFKC · 분철 복원 뒤)에서 `supplement*` · `supporting information` · `appendix` · `data availab*` · `video` · `movie` · `code` **0 회**(`MATLAB` 1 · `pdepe` 1 — 도구 이름). PDF 안 임베디드 파일 0. 원자료 예치 0 · 코드 0 ⇒ 이 digest 의 재현은 **인쇄 수치 · 식 + 원본 래스터 화소 판독 + 우리 재풀이(완전 해리 · 해리 · 닫음 바꿈 · Lithylene 구간)** 세 층뿐이다.

---

# 그림 · 표 — 자동 13 항목 + 수동 1, 실제로 연 것 **14/14**

크로퍼(`wiki/tools/extract_figures.py`)가 본문 그림 1–12 를 `fig_1` … `fig_12`, 표 1 을 `tab_1` 로 잡았다(SI 판별 ✅ — 파일명 `61._Mathematical_modelling_of_ionic_transport_in_the_electrolyte_of_Li-ion_batteries` 의 `SI_TAG` False · 실행 뒤 이름을 눈으로 확인 · `fig_S…` 0). 수동 크롭 1(300 dpi · `tab_1_manual_p4.png` — 파일명의 p 숫자는 PDF 쪽): **표 1 단독**. 자동 크롭 점검(`figures.json` `note` 에 적음 — 자동 파일은 지우지 않았다):

- **과대 둘** — `fig_1`(위쪽에 식 (4.1) 한 줄 — 그림 내용 온전이라 수동 안 함) · `tab_1`(쪽 전체 — 본문 두 단 · 그림 2 · 3 · 식 27–30 → 수동 표 단독).
- **캡션 필드 오염 · 잘림 넷** — `fig_3`(캡션 뒤에 오른쪽 단 본문 'is close to zero, and reaches …' ~ 'Fig. 4 illustrates … acro' 가 붙고 900 자에서 잘림) · `fig_7`(55 자 'PF−' 에서 잘림 — PF₆ 아래첨자 줄바꿈) · `fig_8`('η_down' 이 U+0005) · `fig_12`('(δ)' 가 '(ı)') · `tab_1`(표 머리 글자가 붙고 '… DPF6' 에서 잘림) — 캡션 원문은 PDF 가 정본.
- **원문 오기(크롭 문제 아님)** — 그림 2–7 · 10 의 y 눈금 "1.0 · 0.8 · 0.4 · 0.4 · 0.2 · 0"(0.6 자리에 0.4 — D13) · 그림 1 캡션 "electolyte".
- 나머지 라벨 · 내용 온전 · 잘림 0.

**14 장 전부 이 실행에서 직접 열었다 — 안 본 그림 · 표 0.** 판독: 그림 8 · 9 · 11 · 12(2D 선 그림)는 PDF 에서 원본 JPEG 를 꺼내 **축 눈금 화소로 보정**했다(그림 8 y 0.20/0.15/0.10/0.05/0/−0.05 V = 8.5/75.5/144.0/211.0/279.5/346.5 행 · x 0/20/40/60/80 min = 122.5/230.5/340.5/449.5/554.5 열 / 그림 9 y 15/10/5/−5 mV = 8.0/102.0/196.0/384.5 행 · x 0/15/30/45/60 min = 115.5/226.5/344.5/456.5/577.5 열(눈금 잔차 ±3 px) / 그림 11 판 넷의 틀 · 눈금 — (A) y 0.25…0 V = 6…289 행 · x 0…80 min = 102.5…469.5 열 등 / 그림 12 y 0.5…0 V = 8…407 행 · x δ 0.65…1.00 = 79…565.5 열) — 선 색(검정 · 진회색 · 연회색)으로 곡선을 가르고 라벨 글자 런은 위치로 걸러 냈다. 그림 2–7 · 10 은 3D 면이라 원근 때문에 판독 폭이 넓다(`[도표]` 만). 판독 · 재현 코드 · 렌더 조각은 `scratchpad` 에만(커밋 안 함).

## Fig. 1 — 셀 도식 (p. 5570 · 봤다 · 회색 래스터 · 자동 과대(식 4.1)) ★ (a)

Positive Electrode **LiCoO₂**(왼쪽) | **LiPF₆ electrolyte** | Negative Electrode **LiC₆**(오른쪽) · 아래 축 y — 오른쪽 0(음극 계면)에서 왼쪽 L(양극 계면)로 화살 · Li⁺ 화살: **Charge = 오른쪽(음극 쪽 · −y)** · **Discharge = 왼쪽**. ⇒ 충전 중 Li⁺ 플럭스는 음수(−y)여야 한다 — 식 (6.3)–(6.4) · 그림 5 의 음수와 맞고 식 (4.3)–(4.4) 의 부호와는 반대다(D4).

## Fig. 2 — c(y,t) 면 (p. 5572 · 봤다 · RGB 래스터 3D) ★★ (a)

c [mol/m³] 0–3000 · y 0–1.0 · t 0–80 min. `[도표]` 초기 1500 평탄 → y = 1(양극) 쪽 ≈2800 · y = 0 쪽 ≈200 아래로 → 50 min 에 끔 → ≈80 min 평탄. `[재현]` 표 1 정상 c(0) **194.1** · c(L) **2805.9** mol m⁻³(식 33 · L 2.9×10⁻⁴ 이면 147.5 · 2852.5 — 이 원근에서는 못 가름). ⚠ y 눈금 0.4 중복(D13).

## Fig. 3 — E(y,t) 면 (p. 5572 · 봤다 · RGB 래스터 3D · 캡션 필드 오염) ★★ (a) · D1

E [V/m] 0 … −1250. `[도표]` 정상 y = 0 바닥 ≈ −1200(본문 "about −1200 V/m") · t = 0 ≈ −130 균일 · 끈 뒤 ≈0. `[재현]` 식 (31) E(y,0) **−127.8** · 식 (34) E_ss(0) **−1235**(표 1) ↔ L 2.9×10⁻⁴ 이면 −1625 V/m — 그림은 표 1 쪽. ⚠ 본문 "which coincides with the high electric field in Fig. 3b"(그림 3 은 판 하나 — D12).

## Fig. 4 — φ(y,t) 면 (p. 5573 · 봤다 · RGB 래스터 3D) ★★ (a) · D12

축 이름 **φ [V]** 0–0.08 — 위치별 전위 φ(y,t)(식 28)의 면이다(캡션 "migration overpotential … calculated according to Eq. (30)" 은 스칼라 η 의 식 · 본문은 "Galvany potential difference … (Eq. (28))"). `[도표]` y = 1 에서 t = 0 ≈0.036 · 정상 ≈0.07 V. `[재현]` η₀ **35.79** · 정상 이동 몫 **68.63 mV**(표 1 · 비 1.92 = 본문 "almost two times higher as the initial overpotential at y = 1") ↔ L 2.9×10⁻⁴ 이면 37.07 · 76.11(비 2.05).

## Fig. 5 — Li⁺ 확산 · 이동 플럭스 (p. 5573 · 봤다 · RGB 래스터 3D) ★ (a)

(a) J_dif · (b) J_mig ×10⁻⁴ mol m⁻² s⁻¹(0 … −2.0). `[도표]` 정상 둘 다 ≈ −1.85 · 이동 초기 ≈ −1.5. `[재현]` −I/(2FA) = **−1.866×10⁻⁴**(본문 "about −18 × 10⁻⁵" ✅ · L 무관) · 초기 −t₊I/(FA) = −1.49×10⁻⁴ — "the migration flux grows somewhat further"(×1/(2t₊) = 1.25) ✅.

## Fig. 6 — PF₆⁻ 확산 · 이동 플럭스 (p. 5573 · 봤다 · RGB 래스터 3D) ★ (a)

(a) J_dif(0 … −3.0) · (b) J_mig(0 … 3.0) ×10⁻⁴. `[도표]` 정상 ±≈2.8 · 이동 초기 ≈ +2.2. `[재현]` ±(D₋/D₊)·I/(2FA) = **2.798×10⁻⁴**(본문 "28 × 10⁻⁵" ✅) · 초기 t₋I/(FA) = 2.239×10⁻⁴.

## Fig. 7 — 총 플럭스 (p. 5574 · 봤다 · RGB 래스터 3D · 캡션 필드 잘림) ★ (a) · D10

(a) J_tot,Li⁺(0 … −4.0) · (b) J_tot,PF₆⁻(−2.5 … 2.5) ×10⁻⁴ — t · y 축을 바꿔 그림(본문 명시). `[도표]` 정상 Li⁺ ≈ −3.7 · PF₆⁻ 0 · 켤 때 PF₆⁻ ≈ +2.2 · 끌 때 ≈ −2.2. `[재현]` −I/(FA) = −3.731×10⁻⁴ · 켤 때 +t₋I/(FA) = +2.239×10⁻⁴ · 끌 때 −2t₊D₋(∂c/∂y) = −2.239×10⁻⁴(같은 크기 반대 부호). 본문 "As expected, PF6− does not contribute to the overall ionic conductivity" ↔ 같은 쪽 "it clearly contribute to the ionic conductivity in the electrolyte, especially under the most dynamic, current on/off switching, conditions" — 정상 ↔ 과도 조건이 문장에 없다(D10).

## Fig. 8 — 총 · 확산 · 이동 과전압 + 끈 직후 전압 (p. 5574 · 봤다 · 회색 래스터 · `[도표·화소]`) ★★★★ (a) · 판정 3 · 4 · 5

η [V] −0.05–0.20 · t 0–80 min · 곡선 (a) 총(연회색) · (b) 확산(검정) · (c) 이동(진회색) · (d) 끈 직후 전압(검정 파선). `[도표·화소]` 50 min 직전 **(a) 137.8 · (b) = (c) 68.7 · (d) 82.0 mV** · (c) 0.3 min 37.7 · (a) 5 · 10 · 20 · 30 min 82.8 · 107.1 · 130.4 · 135.9 mV · 50.4–55 min (c) 8.1 → 3.0 mV(끈 뒤 빠르게 0). `[재현]` 표 1 PDE 재풀이: (a) 81.3 · 106.6 · 130.7 · 136.1 · 137.2 / (c) 0.3 min 37.35 → 68.61 / (b) → 68.61 / (d) 해석 82.35 — **±1 mV**(이동 ±0.3 · 0.3 min 의 총은 −3.9 mV — 기울기 큰 자리) · L 2.9×10⁻⁴ 이면 152.1 · 76.1 · 91.3 ✗. ⇒ 원전은 식 (30) 두 항을 다 계산했다 · 정상에서 (b) = (c) · (d) = η_ss − η_down(t₊ 0.4).

## Fig. 9 — Lithylene 실측 ↔ 모형 (p. 5575 · 봤다 · 회색 래스터 · `[도표·화소]`) ★★★★ 판정 6 · G1 · D7

η [mV] −5–15 · t −5–60 min · 선 = 모의 · 회색 타원 = 측정. `[도표·화소]` 선: 켬 ≈0 min(눈금 보정 ±0.4 min) · 켬 뒤 +0.45 · 0.71 · 0.97 · 1.23 · 1.75 · 2.27 · 4.22 · 6.17 min 에 5.51 · 6.31 · 6.71 · 7.48 · 8.25 · 8.83 · 9.63 · 9.82 mV · 정상 **9.95 ± 0.1** · 끔 ≈31.6 min · 수직 하강 → ≈5.0–5.2 · 끈 뒤 +0.58 · 0.84 · 1.10 · 1.62 · 2.01 · 3.05 · 4.09 · 5.0 · 6.04 min 에 4.24 · 3.81 · 3.04 · 2.33 · 1.61 · 0.73 · 0.39 · 0.15 · 0.12 mV. 측정 표지는 선 위에 겹쳐 그려져 잔차를 읽을 수 없다 · 오차 막대 · 셀 수 0. `[재현]` 표 1 Lithylene 행 전 두께: 정상 32.96 · 켜는 순간 15.94 mV(×3.3 — ✗) · `[재현·가정]` 가운데 29.6 µm 구간: 상승 5.58 · 6.25 · 6.86 · 7.37 · 8.15 · 8.70 · 9.63 · 9.87 / 감쇠 4.01 · 3.36 · 2.80 · 1.95 · 1.48 · 0.71 · 0.34 · 0.18 · 0.09 mV — 선과 ±0.15 · ±0.4 mV ✅ · 전 두께 · 전류 ×0.311 로 같은 정상값을 주면 끈 뒤 2.69 · 2.23 · 1.86 … mV(✗ — 그림의 0.6–0.7 배).

## Fig. 10 — 중성 LiPF₆ 단면 (p. 5576 · 봤다 · RGB 래스터 3D) ★★ (a)

c_LiPF₆ [mol/m³] 0–1000 · δ 0.80. `[도표]` 초기 300 평탄(= (1 − δ)c₀ ✅) · y = 1 쪽 정상 ≈800–950(3D 원근 — 판독 폭 넓음) · y = 0 쪽 0 가까이 · "The steady-state profile is formed after approximately 30 min" ✅(재풀이 30 → 50 min 변화 0.4 %). `[재현]` 50 min s(L) 790(표 1 L) · 812(L 2.9×10⁻⁴) — 이 그림으로는 판정 안 함 · c_Li⁺ 단면 "slightly concave" ✅(재풀이 가운데가 직선보다 +91 mol m⁻³ 위).

## Fig. 11 — 해리도 넷의 과전압 (p. 5576 · 봤다 · 회색 래스터 · `[도표·화소]`) ★★★★ 판정 5 · 7 · D3 · D5

(A) 100 % · (B) 85 % · (C) 70 % · (D) 65.69 % · 곡선 (a) 총 · (b) 확산 · (c) 이동(캡션). `[도표·화소]` 49.5 min — (A) 137.4 · (b)(c) 69.3 · (B) **172.4 · (c) 91.8 · (b) 82.0** · (C) **240.5 · 131.8 · 110.1** mV · (D) 40 min 446 · 50 min 가까이 ≈3 V 폭주 · (B)(C) 5 · 10 · 20 · 30 · 40 min 총 90.0 · 117.5 · 155.6 · 168.9 · 172.4 / 100.5 · 134.1 · 192.5 · 225.5 · 237.8 mV. `[재현]` (A) = 표 1(RMS 0.96 mV) · (B)(C) = **L 2.9×10⁻⁴**(RMS 1.06 · 0.83 mV — 표 1 이면 15.49 · 34.28) · (D) 20 · 30 min 217.5 · 297.9 ↔ 215.1 · 295.7(그 뒤는 특이점 근처라 δ 0.0007 차에도 크게 움직임). 그림 배치는 캡션과 같다(정상 (c) > (b)) — 본문 (ii) · (iv) 의 곡선 글자는 뒤바뀌었다(D5).

## Fig. 12 — 50 min 과전압 ↔ δ (p. 5577 · 봤다 · 회색 래스터 · `[도표·화소]`) ★★★★ 판정 5 · D3 · D6

η_ss [V] 0–0.5 · δ 0.65–1.00 · (a) 총 · (b) 확산 · (c) 이동 · (d) "migration residual". `[도표·화소]` δ 0.997: (a) **151.6** · (b)(c) 76.3 · (d) 14.9 / 0.90: 164.1 · 80.1 · 85.1 · 16.1 / 0.85: 174.1 · 81.3 · 91.4 · 16.1 / 0.80: 185.4 · 85.1 · 98.9 · 16.1 / 0.75: 205.5 · 93.9 · 110.2 · 18.6 / 0.70: 243.1 · 110.2 · 132.7 · 21.1 mV · 곡선 시작 δ ≈0.658. `[재현]` L 2.9×10⁻⁴ · 50 min: 152.4/76.1/76.3/15.2 · 163.9/78.9/85.0/15.8 · 172.7/81.7/91.0/16.3 · 184.9/86.1/98.8/17.2 · 203.7/93.7/110.0/18.7 · 240.1/109.8/130.3/22.0 ✅(±3 mV) · 표 1 이면 0.997 137.4 · 0.85 151.8 · 0.70 189.8 ✗. ⇒ δ → 1 끝 ≈152 mV 는 그림 8 · 11(A) 의 137 mV 와 다른 '완전 해리' 값이다(D3). (d) 는 본문 정의 0 — 식 (40) 값(끈 직후 이동 몫 |−(RT/F)(t₊ − t₋) ln[c(L)/c(0)]|)과 맞는다(D6).

## Table 1 — 매개변수 (p. 5572 · 봤다 · 자동 과대 → 수동 단독) ★★★★ (a) · 판정 5 · D1

열 Battery type · D_Li⁺ · D_PF₆⁻ (m² s⁻¹) · L (m) · c₀ (mol m⁻³) · I (A) · A (m²) · T (°C). **CGR17500**: 2×10⁻¹¹ · 3×10⁻¹¹ · **2.8×10⁻⁴** · 1500 · 0.72 · 2×10⁻² · 25 / **L Lithylene**: 1.07×10⁻¹¹ · 1.07×10⁻¹¹ · 9.5×10⁻⁵ · 1000 · 0.12 · 8.9×10⁻³ · 25. 표 안 출처 각주 0 — 본문 "all taken from Ref. [11]"(CGR17500) · Lithylene 행 출처 0. `[재현]` t₊ 0.4 · 0.5 · D_amb 2.4×10⁻¹¹ · 1.07×10⁻¹¹ · I/A 36 · 13.5 A m⁻² · x **0.8706**(인쇄 0.9017) · 0.3102.

## 본문 서술과 어긋난 그림 · 표 (요약)

- **그림 11 · 12 · 인쇄 x · '61 %' · 한계 δ ↔ 표 1**: L 2.9×10⁻⁴ 상태로만 닫힌다(그림 8 · 11(A) 는 표 1) — D1 · D3.
- **그림 9 ↔ 표 1 Lithylene 행**: 전 두께면 ×3.3 — 기준극 구간 미인쇄(D7).
- **그림 11 본문 (ii) · (iv)**: 곡선 글자 (b) ↔ (c) 가 캡션 · 그림과 반대(D5).
- **그림 4 캡션 ↔ 축**: 'Eq. (30) 의 η' ↔ φ(y,t) 면 · 본문 "Fig. 3b"(D12).
- **그림 12 (d)**: 본문 정의 0(D6).
- **그림 2–7 · 10 y 눈금**: 0.4 중복(D13).
- 나머지(그림 1 · 5 · 6 · 7 · 8 · 10)는 본문 서술과 맞다.

---

# 절별 해체 (본문)

## 초록 · 1. Introduction (p. 5569)

`[인쇄]` 동기: "Advanced batteries are a growing 50 billion-$-a-year business" · "Simulating discharge curves of Li-ion batteries already dates back to the early 1980s [1]"(**[1] = Doyle · Fuller · Newman 1993** — 연대 어긋남 · 91호 서론에 같은 문장 · 같은 어긋남(91호 D9 — 91호 digest 전사) · D16) · 종설 [2–5] · 다공 전극 이론 [6] · 전자 회로망 모형 [7–11] · 노화 [12] · "In the case of Li-ion batteries the ionic transportation properties of the organic electrolyte has been described in detail, including the diffusion and migration processes [11]. However, a detailed analysis of the various contributions is still lacking." · "Recent experimental results showed that the energy losses in Li-ion batteries might be substantial due to the limited ionic conductivity of the electrolyte, thereby negatively influencing the overall battery performance [13]." · "all presented models are based on the assumption that the dissolved salt in the organic electrolyte is completely dissociated. It has, however, been reported that this is not the case for all organic solvent-based battery electrolytes."(이 문장 번호 0 — 근거는 3.3 절 [18]) · "This not only yields interesting information for rechargeable batteries but also for other electrochemically based systems, such as planar electro-chromic devices [14]." — 고체 전해질 · 박막 전지 언급 0.

## 2.1 Model set-up (p. 5569–5570 · 식 1–7 · 그림 1)

- `[인쇄]` 반응 (1) LiCoO₂ ⇌ Li₁₋ₓCoO₂ + xLi⁺ + xe⁻(0 ≤ x ≤ 0.5) · (2) C₆ + zLi⁺ + ze⁻ ⇌ Li_zC₆(0 ≤ z ≤ 1) · "The electrolyte in Li-ion batteries is based on a dissociated Li-salt, e.g. LiPF6 or LiClO4, which cannot be considered as a well ionic-conductive medium. The ions in the electrolyte are transported both by diffusion and migration".
- (3) Nernst–Planck J_j = −D_j ∂c_j/∂y − (z_jF/RT) D_j c_j ∂φ/∂y · "Herewith it is assumed that no convection takes place in the electrolyte" · E = −∂φ/∂y.
- (4.1)–(4.4) Li⁺ 물질수지 · 초기 c₀ · 경계 **J_Li⁺(0,t) = −I_LiC₆(t)/(z_Li⁺FA) · J_Li⁺(L,t) = I_LiCoO₂(t)/(z_Li⁺FA)** · (5.1)–(5.4) PF₆⁻ 물질수지 · 두 경계 유속 0 · 부호: "Considering the charging process, the reduction current at the negative electrode is defined as negative while the oxidation current at the positive electrode is defined positive. Since no side reactions are considered … I(t) = I_LiCoO₂(t) = −I_LiC₆(t)."
- (6.1)–(6.4) · (7.1)–(7.4) — (3) 을 (4) · (5) 에 넣은 꼴(z_Li⁺ = −z_PF₆⁻ = 1) · 경계 **(6.3) D_Li⁺ ∂c(0,t)/∂y − D_Li⁺(F/RT)c(0,t)E(0,t) = I(t)/(FA)** — 좌변이 −J_Li⁺(0) 이라 J_Li⁺(0) = −I/(FA) · (4.3) 은 +I/(FA) — **부호 반대**(렌더 확인 · D4). 계산 · 그림 5(충전 중 Li⁺ 플럭스 음수 = 음극 쪽 −y)는 (6.x) 쪽이다.

## 2.2 Electro-neutrality condition (p. 5570–5571 · 식 8–25)

- `[인쇄]` "In general it is necessary to consider the Maxwell equations to determine E(y,t) [16] and all currents (fluxes). The resulting system is, however, far too complicated to yield an analytical solution. Therefore a simplifying assumption is furthermore required, which can be offered by the electro-neutrality condition" · (8) c = c_Li⁺ = c_PF₆⁻.
- (9.1) × D_PF₆⁻ + (10.1) × D_Li⁺ → **(11) ∂c/∂t = [2D₊D₋/(D₊ + D₋)] ∂²c/∂y²** · 경계도 같은 곱으로 (12)–(13) 2D₊ ∂c/∂y = I/(FA) → **(14)** "Obviously, the complex set of Eqs. (9) and (10) can now be reduced to a much simpler problem" · D = 2D₊D₋/(D₊ + D₋) "or 2/D = 1/D₊ + 1/D₋". `[재현·대수]` 세 줄 모두 확인 ✅(경계에는 D₊ 만 남는다 — PF₆⁻ 차단 경계의 귀결).
- (10.1) − (9.1) → (15) → 적분 (16) · (10.3) 에서 (17) F/RT c(0)E(0) = −∂c(0)/∂y → (18) → **(19) E = (RT/F)(1/c){−I/(2FAD₊) + [(D₊ − D₋)/(D₊ + D₋)][∂c/∂y − I/(2FAD₊)]}** · (20) **t_Li⁺ = D₊/(D₊ + D₋) · t_PF₆⁻ = D₋/(D₊ + D₋)** · (21) = (19) 에 (20) 대입(렌더 확인). `[재현·대수]` (19) 는 전류 밀도 i = F(J₊ − J₋) = I/A 를 E 에 대해 푼 것과 같다 ✅.
- (22)–(25) 플럭스 — (24) "Evidently, the total diffusion flux can then be expressed by" J_tot,Li⁺ · (25) "and the total migration flux by" J_tot,PF₆⁻ — 실제로는 각 이온의 총 플럭스(이름 오기 · D9).

## 2.3 Overpotentials (p. 5571–5572 · 식 26–30)

- `[인쇄]` (26) μ̄_Li⁺ = μ⁰_Li⁺ + RT ln(c_Li⁺/c^ref_Li⁺) + z_Li⁺Fφ — "c^ref_Li⁺ is the reference concentration of 1 molar" · (27) η(t) = (1/z_Li⁺F)[μ̄_Li⁺(L,t) − μ̄_Li⁺(0,t)] = (RT/F) ln(c_Li⁺(L,t)/c_Li⁺(0,t)) + (φ(L,t) − φ(0,t)) — "The difference in electrochemical potentials between both electrode/electrolyte interfaces represents the concentration polarization across the electrolyte" · "This overpotential is solely attributed to the transport limitations of the electrolyte and excludes the overpotential contributions of both charge transfer reactions." · (28) φ(y,t) = −∫₀ʸ E dy · (29) · **(30) η(t) = (RT/F) ln(c(L,t)/c(0,t)) − ∫₀ᴸ E(y,t) dy**(렌더 확인). 활동도 계수 · 열역학 인자 0(이상 묽은 용액).

## 3.1 Concentration profiles, electric field and ionic fluxes (p. 5572–5574 · 그림 2–7 · 표 1)

- `[인쇄]` "calculated (Eq. (14)), using the standard MATLAB pdepe solver and applying discretization steps with a space variable of L/200 and adaptive time steps). The model parameters used in this paper are all based on a cylindrical CGR17500 Li-ion battery of Sony having a storage capacity of 720 mAh and using dissociated LiPF6 as ionic-conducting salt. The relevant parameter values for this battery type are all taken from Ref. [11] and can be found in the Table 1. Unless indicated, the battery charge current applied in all simulations corresponds to 1 C-rate. Constant-current charging is applied during 50 min after which the current was switched off."
- 그림 2 "the initial concentration value is equal to 1500 (mol m−3) … to become linear after approximately 30 min" · 그림 3 "reaches a value of about −1200 V/m. This high electric field region is, however, quite narrow and its overall contribution to the total overpotential are therefore rather moderate" · "in order to build up non-uniform electric field … ionic charge separation is required. However, the degree of deviation from electro-neutrality is calculated to be smaller than ten orders of magnitude with respect to the equilibrium electrolyte concentration"(방법 · ε_r 미인쇄 — G11 · D14) · 그림 4 "the overpotentials are almost two times higher as the initial overpotential at y = 1" · 그림 5 "Here, both the diffusion and migration fluxes are the same and amounts, in this example, to about −18 × 10−5 mol m−2 s−1" · "at the beginning of the charging process when the concentration profile is flat, the ionic current in the electrolyte is solely carried by migration, while under steady-state conditions the diffusion and migration contributions are equal" · 그림 6 "The fluxes amount to 28 × 10−5 mol m−2 s−1 under steady-state conditions" · 그림 7(D10).

## 3.2 Overpotentials and resistances (p. 5574–5575 · 식 31–42 · 그림 8 · 9)

- `[인쇄]` 켜는 순간 (31) E(y,0) = −t_Li⁺ (RT/(Fc₀)) I/(FAD₊) · (32) **η₀ = (RT/(Fc₀)) IL/(FA(D₊ + D₋))** — "the diffusion coefficient of both Li+ and PF6− ions has an influence on the initial migration overpotential".
- 정상 (33) c(y) = (I/(2FAD₊))(y − L/2) + c₀ · (34) E(y) = −(RT/F)(1/c(y)) I/(2FAD₊) · (35) 이동 몫 = (RT/F) ln(c(L)/c(0)) · (36) **η_ss = 2(RT/F) ln(c(L)/c(0))** · (37) η_ss = (2RT/F) ln[(c₀ + IL/(4FAD₊))/(c₀ − IL/(4FAD₊))] · "In contrast to η0 (Eq. (32)), ηss (Eq. (37)) only depends on DLi+ and is independent on DPF6−. It should, however, be noted that DPF6− certainly affects the overpotential in the transition region (see Fig. 8). For a given DLi+, smaller values of DPF6− result in longer transition periods".
- 비 (38) **η₀/η_ss = 2t_Li⁺ x / ln((1 + x)/(1 − x))** · x = IL/(4FAc₀D₊) · "If x < 1, i.e. when I < 4FAc0DLi+/L … η0/ηss ≤ tLi+. For the considered Li-ion (CGR17500) battery and given charging current, x is calculated to be 0.9017 and η0/ηss therefore amounts to only 61% of the tLi+ value of 0.4 adopted in these simulations (see Ref. [11]). This agrees well with the simulation result shown in Fig. 8." · "for a low charging current of 0.1 C-rate, η0/ηss deviates less than 1% from tLi+".
- 끄는 순간 (39) E = (RT/F)(1/c)(t₊ − t₋) ∂c/∂y · (40) 이동 몫 = −(RT/F)(t₊ − t₋) ln(c(L)/c(0)) · (41) **η_down = 2t_Li⁺(RT/F) ln(c(L)/c(0))** · (42) **η_down/η_ss = t_Li⁺** — "Elegantly, this ratio is exactly given by the Li+ transference number and delivers a nice tool to obtain this value experimentally."
- 그림 9 실험(판정 6) · "Dividing η0 in Eq. (32) by the applied current I, the ohmic resistance (R0) of the electrolyte can be calculated. For the considered Li-ion battery (CGR17500) the ohmic resistance is simulated to be R0 ≈0.0506 (Ω), which is in the good agreement with experimental results. … The steady-state resistance of the electrolyte Rss, can be obtained from Eq. (37) and Rss = ηss/I. For the present Li-ion battery Rss amounts to 0.1950 (Ω) in the simulations."

## 3.3 Salt dissociation (p. 5575–5577 · 식 43–47 · 그림 10–12)

- `[인쇄]` "It is known from literature that the degree of dissociation of Li-salts dissolved in organic solvents is incomplete. For example, LiPF6 in PC is only dissociated for about 80% [18]." · (43) LiPF₆ ⇌(k_d · k_a) Li⁺ + PF₆⁻ · c^eq_Li⁺ = c^eq_PF₆⁻ = δc₀ · c^eq_LiPF₆ = (1 − δ)c₀ · k_d/k_a = c₀δ²/(1 − δ) · "Assuming that kd and ka are concentration-independent" · r = k_d c_LiPF₆ − k_a c_Li⁺ c_PF₆⁻ · (44)–(45) 두 이온 PDE + r · **(46) ∂c_LiPF₆/∂t = D_LiPF₆ ∂²c_LiPF₆/∂y² − r · 두 경계 유속 0** — "Since LiPF6 is uncharged, migration does not contribute to the transportation of these species. Obviously, the un-dissociated salt is not consumed as is evidenced by the boundary conditions" · (47) ∂c/∂t = D ∂²c/∂y² + r · 초기 δc₀ · 경계 (14) 와 같음 · "The intensity of the electric field in the electrolyte is again described by Eq. (19)."
- 선택 값: "some additional parameter values have to be chosen. The simulation shown in Fig. 10 are performed with a moderate degree of salt dissociation of δ = 0.80 and with an association rate constant of ka = 10−5 (m3 mol−1 s−1). The diffusion coefficient for LiPF6 is taken DLiPF6 = 2 × 10−11 (m2 s−1). The other parameters are the same as used in Section 4."(4 절 = 결론 — D8) · 그림 10 · "the concentration profile for Li+ ions is not exactly linear, but slightly concave under steady-state" · 그림 11 (i)–(iv)(D5 · D11) · 그림 12 "Migration is, however, most responsible for the explosive nature of the overpotential increase and hence of major importance of poorly dissociated electrolytes."

## 4. Conclusions (p. 5577)

`[인쇄]` "For the concentrated electrolytes of Li-ion batteries the electro-neutrality condition holds and the complex system of PDEs could be reduced to a much simpler initial-boundary problem" · "it was found that for fully dissociated salts the diffusion and migration contribution to the total overpotential were exactly balanced. The calculated overpotentials have been experimentally verified by means of in-situ reference electrode measurements [13] and match the experimental results well." · "It has been derived that the transference number of Li-ions only determines the instantaneous voltage drop and this facilitates the way to perform simple experiments to determining the transference numbers and other important ionic conductivity characteristics."(D17) · "for non-ideal dissociated electrolytes the concentration profiles were, in general, non-linear and the overpotentials were found to be larger than for ideal electrolytes … The present simulations clearly showed that migration is of major importance in poorly dissociated electrolytes."

---

# ★ (a) 이 편의 전해질 모형 — 운반체 · 전기중성 · 수정 확산계수 · 해리 · 표 1 출처

| 층 | 이 편 (`[인쇄]`) | 가정 · 조건 |
|---|---|---|
| 운반체 | Li⁺ · PF₆⁻(+ 해리 확장에서 중성 LiPF₆) | 유기 액체 용매 · 염의 두 이온 — 고정 틀 · 공공 · 전자 운반체 0 |
| 수송 | Nernst–Planck(식 3) · 대류 0 · D 일정 | 활동도 · 열역학 인자 · 농도 의존 D 0(이상 묽은 용액 — 식 26) · 1500 mol m⁻³ 에서도 같은 꼴 |
| 경계 | Li⁺ = 계면 전류(식 4 · 6) · PF₆⁻ 차단(식 5 · 7) · LiPF₆ 차단(식 46) | 계면 동역학 · 이중층 · 부반응 0 — 전해질만 |
| 전기중성 | c_Li⁺ = c_PF₆⁻(식 8) — Maxwell 방정식 대신 | `[인쇄]` 편차 "smaller than ten orders of magnitude" — 계산 방법 미인쇄 |
| 축약 | ∂c/∂t = D_amb ∂²c/∂y² · D_amb = 2D₊D₋/(D₊ + D₋) · 경계 ∂c/∂y = I/(2FAD₊)(식 14) | 경계에 D₊ 만 — 차단된 음이온의 귀결 |
| 전기장 | 식 (19) · (21) — 국소 c · ∂c/∂y · I 의 닫힌 꼴 | 운반수 = D 비(식 20) — Nernst–Einstein 형 |
| 과전압 | η = Li⁺ 전기화학 퍼텐셜 차(식 27) = 'diffusion' (RT/F) ln[c(L)/c(0)] + 'migration' −∫E dy(식 30) | 전하이동 과전압 제외 · 정의 분할(측정 분할은 식 41) |
| 해리 | LiPF₆ ⇌ Li⁺ + PF₆⁻ · r = k_d c_LiPF₆ − k_a c₊c₋ · 중성종 확산 D_LiPF₆(식 43–47) | k_d · k_a 농도 무관 · 중성종 = 움직이는 이온쌍 · 총 염은 전역 보존 |
| 매개변수 | 표 1 CGR17500 "all taken from Ref. [11]"(Bergveld · Kruijt · Notten 2002 책) · Lithylene 행 출처 0 · δ 80 % = [18](LiPF₆ in PC · 학회 요약) · k_a · D_LiPF₆ = 선택 값 | 측정 · 적합 · 문헌 구분 표기 0 · `[재현]` t₊ 0.4(CGR17500) · 0.5(Lithylene) |

`[재현]` 표 1 의 수치 층(우리 계산): C-rate ↔ 전류 ↔ 면적 — CGR17500 720 mAh · 0.72 A = 1C ✅ · A 200 cm² → **3.6 mA cm⁻²** · 면적 용량 3.6 mAh cm⁻² / Lithylene 300 mAh · 0.12 A = 0.4C ✅(그림 9 캡션 · 본문과 같음) · A 89 cm² → **1.35 mA cm⁻²** · 3.37 mAh cm⁻² · c₀ 1500 · 1000 mol m⁻³ = 1.5 · 1.0 mol L⁻¹. 시간 척도 τ₁ = L²/(π²D_amb) = **5.52 min**(CGR17500 — "linear after approximately 30 min" ✅ · 30 min 에서 e^(−30/5.52) = 0.4 %) · **1.42 min**(Lithylene) · 정상 한계 전류 4FAc₀D₊/L = 0.827 A(= 1.149 × 1C — x < 1 조건 ✅).

---

# ★ (b) 26호가 가져간 가정('SE 에 농도 구배' · 이온 + 공공)은 이 편에 있는가 — 판정

## 1. 이 편에 있는 것 (`[인쇄]`)

- **두 운반체 · 전기중성 · 수정 확산계수 · D₊ 만 든 경계 · 전기장 닫힌 꼴 · η 의 두 항** — 식 (8)–(21) · (27)–(30). 26 · 91 · 98 · 100호가 옮긴 식은 전부 이 꼴이다(중심 표 ✅ 11).
- **해리 + 재결합** — 식 (43)–(47) · 평형 관계 k_d/k_a = c₀δ²/(1 − δ). 91호 식 14 · 98호 식 17 과 꼴이 같다(이름 k_a ↔ k_r · 91 · 98호 digest 전사).
- **농도 구배** — 액체 염에서 정상 기울기 I/(2FAD₊)(식 33) · 해리 확장에서 오목한 단면(그림 10 · 본문).

## 2. 이 편에 없는 것 (`[인쇄]` 어휘 0 · 지면 0)

- **고체 · 유리 · 단일 이온 전도체** — `solid` · `glass` · `polymer` · `LiPON` · `Li3PO4` · `ceramic` · `single-ion` 0 회.
- **공공 · 고정 음전하 · 미보상 전하** — `vacanc*` 0 · PF₆⁻ 는 용매 속 움직이는 음이온이다.
- **고정된 중성종 · 국소 보존** — 이 편의 중성종 LiPF₆ 는 확산하고(식 46) 총 염은 경계 유속 0 으로 **전역** 보존된다 · 국소 '총 Li 일정'(98호 c₀ = c_Li⁰ + c_n — 98호 digest 전사) · '고정 Li⁰'(91호 "immobile, oxygen-binded lithium" — 91호 digest 전사)은 이 편에 없다.
- **고체로 옮기는 근거 문장** — 0. 이 편이 다른 계로 넓히는 문장은 "planar electro-chromic devices [14]" 하나다.

## 3. 그러면 이식은 어디서 — 그리고 무엇을 바꿨나 (91 · 98 · 26호 digest 전사)

| 단계 | 편 | 바꾼 것 | 이름 |
|---|---|---|---|
| 액체 원전 | **101호**(2008) | — | Li⁺ · PF₆⁻ · 중성 LiPF₆(확산) |
| 첫 이식 | **91호**(2011 · 같은 저자) | 음이온 → n⁻("uncompensated negative charges … chemically associated with the closest nBO's" — 유리 'weak electrolyte' 모형 [23–25]) · 중성 이온쌍 → **고정** Li⁰ · D_n⁻ 5.1×10⁻¹⁵ > D_Li⁺ 0.9×10⁻¹⁵(t₊ 0.15 `[재현]`) · "conductivity is caused by the transport of Li⁺ ions only" 와 같은 지면 | n⁻ = 미보상 전하(`vacanc*` 0) |
| 둘째 이식 | **98호**(2020 · 같은 연구망) | n⁻ = **공공**("vacancy formed in the LiPON matrix") · **국소 닫음** c₀ = c_Li⁰ + c_n · 같은 꼴을 양극 이온–전자 쌍(식 26–32)에도 | '공공' 이름의 출처 |
| 차용 | **26호**(Iwakiri 2024) | 98호 표 · 이름을 따름 · "SE 에는 농도 구배가 있다(이온·공공 쌍, Danilov & Notten 2008 계열)" | 계보를 이 편에 매닮 |

⇒ **판정**: 'SE 에 농도 구배' 와 '이온 + 공공' 은 **이 편이 아니라 91 · 98호의 이식**이다. 이 편은 그 이식이 쓴 **식의 원전**(✅)이지 **고체 물리의 원전**(❌)이 아니다. ⚠ 조건: 이 판정은 이 편 지면에 대한 것이다 — 91 · 98호가 SE 에 해리 이원 모형을 쓴 근거(유리 'weak electrolyte' 모형 · nBO · LiPON 공공)는 그 편들의 몫이고, 이 편으로 정당화되지도 반증되지도 않는다.

## 4. ★ 이식이 결론을 바꾸는 크기 (`[재현·가정]` — 이 편 표 1 · 해리 선택 값에 **닫음만** 바꾼 반사실)

| 닫음 (δ · 50 min · 표 1 L) | 확산(농도) 항 | 이동 항 | 총 | 같은 σ 단일 이온 옴(η₀/δ) | 이원 가정 몫 1 − 옴/총 | c(0) · c(L) mol m⁻³ |
|---|---|---|---|---|---|---|
| **이 편** — 중성 LiPF₆ 확산(식 46) · δ 0.80 | **74.0** | 86.1 | **160.1** | 44.7 | 72 % | 117 · 2091 |
| 중성종 고정(D_LiPF₆ = 0 — 91호 Li⁰ 쪽 극한) · δ 0.80 | — | — | 고갈(c(0) < 0 — 50 min 전에 한계) | 44.7 | — | — |
| **국소 닫음**(c₀ = c_Li⁰ + c_n — 98호 인쇄 닫음) · δ 0.80 | **7.4** | 46.3 | **53.6** | 44.7 | 17 % | 1028 · 1369 |
| 이 편 · δ 0.95 | 69.0 | 71.9 | 140.9 | 37.7 | 73 % | 177 · 2595 |
| 중성종 고정 · δ 0.95 | 84.7 | 84.7 | 169.4 | 37.7 | 78 % | 100 · 2712 |
| 국소 닫음 · δ 0.95 | 3.0 | 38.3 | 41.3 | 37.7 | 9 % | 1341 · 1509 |

반응 이완 τ = 1/(k_d + 2k_aδc₀) · 반응층 λ = √(D_amb τ): δ 0.80 → 13.9 s · 18.3 µm · δ 0.95 → 3.3 s · 9.0 µm(L 280 µm). 50 min 한계 δ(c(0) → 0): 이 편 닫음 0.604(표 1 L) · **0.658**(L 2.9×10⁻⁴ — 인쇄 0.6569 ✅) ↔ 중성종 고정 0.897 · 0.923.

⇒ `[해석]` 같은 식(47 · 19 · 30) · 같은 매개변수에서 **중성종을 어떻게 닫느냐**만으로 농도(Nernst) 항이 ×0.1 · 이원 가정 몫이 72 % → 17 %(δ 0.95 면 9 %)로 움직인다. 국소 닫음은 벌크를 평형 농도에 묶어 농도 분극을 두 계면의 λ 층에 가둔다 — 98호가 본 '농도 분극은 두 계면 47 nm 층에 갇히고 벌크는 평탄' · '이원 가정 몫 ≈8 %'(98호 digest 전사)의 기구와 같은 쪽이다. 91호 ≈71 %(91호 digest 전사)와 98호 ≈8 % 의 차이는 원전 식의 범위 안에서 **닫음 · 반응 속도(k_r — 91호 ×100 문제) · 두께 대 반응층(L/λ)** 이 정한다고 읽힌다(`[해석]` — 91 · 98호의 실제 계산 조건은 그 digest 들의 몫 · 여기서 다시 풀지 않음). ⚠ 우리 표는 액체 매개변수의 반사실이다 — SE 의 몫을 주장하지 않는다.

## 5. 단일 이온 극한 — 이 틀은 정상 상태에서 단일 이온 전도체가 되지 못한다 (`[재현·대수]`)

`[인쇄]` 식 (37) η_ss 는 D₋ 에 무관하고 "smaller values of DPF6− result in longer transition periods". ⇒ D₋ → 0(음이온이 거의 안 움직이는 쪽)으로 가도 **정상 η_ss 와 농도 구배(기울기 I/(2FAD₊))는 그대로**이고, 바뀌는 것은 정상에 닿는 시간(L²/D_amb → ∞)뿐이다. 단일 이온 전도체의 옴 강하는 이 틀에서 **켜는 순간 값 η₀**(식 32 — D₋ → 0 이면 (RT/F)·IL/(F·A·c₀·D₊) = 같은 σ 의 옴 강하)로만 나타난다. `[해석]` 즉 '이원 + 차단 경계' 틀에 음전하 운반체를 하나라도 움직이게 두면(D > 0) 정상 상태에 농도 구배가 **구성상** 생긴다 — 'SE 에 농도 구배' 는 이 틀을 고른 순간 정해지는 것이지 SE 에 대해 밝혀진 것이 아니다.

---

# ★ Nernst 항 — 99 · 100호 의문에 원전이 답하는 것

| 물음 | 원전 (`[인쇄]` → `[재현]`) | 99 · 100호 (digest 전사) |
|---|---|---|
| 첫 항(농도 · 'Nernst')은 η 의 정의에 있는가 | ✅ 식 (27) — η = Li⁺ 전기화학 퍼텐셜 차 = (RT/F) ln[c(L)/c(0)] + φ 차 · 식 (30) | 99호 식 (14) · 100호 식 (9) 같은 꼴 ✅ |
| 원전 그림은 첫 항을 넣고 계산했는가 | ✅ 그림 8 (b) · (c) 를 따로 그림 · 재풀이 ±1 mV | 99호 그림 = 둘째 항만(D1) · 100호 원 PDE = 포함(±0.05 mV) |
| 그 항의 이름 | **'diffusion overpotential'**(그림 8 · 11 · 12 캡션 · 본문) — `Nernst` 단독 0 | 99 · 100호 digest 'Nernst 항' · 98호 원문 'Nernstian' |
| 정상에서 크기 | 첫 항 = 둘째 항 = (RT/F) ln[c(L)/c(0)](식 35–36) — 둘째 항만이면 정상 η 의 **정확히 절반**(완전 해리 · 이상 · 일정 D) | 99호 '≈절반'(300 s · 해리 SE) — 같은 방향 |
| 해리가 있으면 | 이동 > 확산(그림 11 · 12) — δ 0.70 132.7 ↔ 110.2 mV(`[도표·화소]`) · 반이 아니다 | 91 · 98 · 99 · 100호 SE 는 해리 모형 — 몫은 닫음 · k_r 에 매달림(§(b) 4) |
| 전류를 끊으면 사라지는 몫 | 이동 항이 아니라 2t₊(RT/F) ln(식 41) — 표 1 정상 54.90 / 137.26 mV = t₊ | 'Nernst 항 없는 플랜트' 는 끊는 실험으로 재는 양과도 다르다(`[해석]`) |

⇒ `[해석]` 원전 정의로는 **100호 구현이 맞고 99호 그림은 η 가 아니라 φ 차**다. 그리고 φ 차(이동 항)는 전류를 끊는 실험으로 재는 양(낙차 2t₊(RT/F) ln)과도 다르다 — 'Nernst 항을 넣느냐' 는 구현 선택이 아니라 η 의 정의 문제다. 우리 쪽에서는 전해질 성분을 라벨 · truth 로 쓸 때 **(정의 분할 ↔ 측정 분할)** 을 같이 적어야 한다(새 판단 거리 2).

`[재현]` **이원 가정 몫의 원형** — 이 편 식 (32) η₀ 은 정확히 '같은 σ(Nernst–Einstein κ = F²c₀(D₊ + D₋)/RT)의 단일 이온 옴 강하' 이고, 식 (38) 에서 정상 이원 몫 1 − η₀/η_ss ≥ 1 − t₊(작은 x 에서 등호): 표 1(t₊ 0.4 · x 0.871) **73.9 %** · Lithylene(t₊ 0.5 · x 0.310) 51.6 % · δ 0.8 해리 72 %. 91호 '그림 11 끝 −108.7 mV 중 ≈71 %(77 mV)가 이원 가정의 몫'(같은 σ 단일 이온 대비) · 98호 '이원 가정 몫 ≈8 %'(91 · 98호 digest 전사)는 이 계산의 SE 판이다 — 원전 꼴(완전 해리 · 정상)에서는 몫이 **1 − t₊ 보다 작을 수 없다**(91호 t₊ 0.15 면 하한 85 % · 98호 t₊ 0.233 이면 77 % — `[재현·대수]`). 두 SE 값이 모두 그 하한 아래인 것은 정상이 아니거나(91호 51.2C 끝) 해리 · 재결합과 닫음이 농도 분극을 가둔 결과로 읽힌다(§(b) 4 · `[해석]`).

---

# ★ 표 1 ↔ 계산 — 지면의 두 매개변수 상태 (`[재현]` · `[도표·화소]`)

| 지면 값 · 그림 | 표 1 (L 2.8×10⁻⁴) | L 2.9×10⁻⁴ (x 0.9017) | 지면 (`[인쇄]` · `[도표·화소]`) | 닫히는 쪽 |
|---|---|---|---|---|
| x = IL/(4FAc₀D₊) | **0.8706** | 0.9017 | 0.9017 | L 2.9 |
| η₀/η_ss = t₊ · 2x/ln((1+x)/(1−x)) | 0.2607(t₊ 의 65 %) | 0.2435(61 %) | "61%" · "agrees well with … Fig. 8" | 문장 L 2.9 · 그림 8 은 0.26(표 1) |
| E_ss(0) | −1235 V/m | −1625 | "about −1200" · 그림 3 바닥 ≈ −1200 | 표 1 |
| 그림 4 비 η_mig,ss/η₀ | 1.92 | 2.05 | "almost two times higher" | 표 1 |
| 그림 8 정상 (a) · (b)=(c) · (d) | 137.2 · 68.6 · 82.4 | 152.1 · 76.1 · 91.3 | 137.8 · 68.7 · 82.0 | **표 1**(±1 mV 전 시간대) |
| R₀ = η₀/I | 0.0497 Ω | 0.0515 | 0.0506 "simulated" | 사이(표 1 + 첫 단계 확산 몫으로 설명 가능) |
| R_ss = η_ss/I | 0.1906 | 0.2114 | 0.1950 "in the simulations" | **어느 쪽도 아님**(x 0.8778) |
| 그림 11(A) δ 1 · 5–49.5 min | RMS **0.96** mV | 11.30 | 137.4 … | **표 1** |
| 그림 11(B) δ 0.85 | 15.49 | RMS **1.06** | 172.4 … | **L 2.9** |
| 그림 11(C) δ 0.70 | 34.28 | RMS **0.83** | 240.5 … | **L 2.9** |
| 그림 12 δ 0.70–0.997 | 189.8 … 137.4 | 240.1 … 152.4(±3) | 243.1 … 151.6 | **L 2.9** |
| 한계 δ (50 min) | 0.6037 | 0.6576 | "0.6569" | **L 2.9** |

**x 묶음 가르기** — 같은 x 0.9017 을 주는 한 매개변수 변경 넷을 그림 11 시간 경과(5–49.5 min)로 견줬다(`[재현]` 재풀이 ↔ `[도표·화소]`):

| 변경 | (B) RMS mV | (C) RMS mV | (C) 49.5 min 총 mV |
|---|---|---|---|
| **L 2.8 → 2.9×10⁻⁴** | **1.06** | **0.83** | 240.0 |
| I/A ×1.0357(I 0.7457 A 또는 A ÷1.0357) | 1.75 | 5.49 | 244.6 |
| c₀ ÷1.0357 | 1.82 | 6.92 | 247.0 |
| D₊ ÷1.0357 | 1.49 | 5.86 | 230.3 |
| (표 1 그대로) | 15.49 | 34.28 | 189.8 |

⇒ **완전 해리라면 정상 값은 x 하나의 함수**라(식 37) 넷이 같다 — `[재현]` 그림 11(A) 조건(δ 1)에서 넷 모두 49.5 min 152.1–152.2 mV. 해리 판((B) · (C))에서는 해리 평형 · t₊ · D_amb 로 c₀ · D₊ 가 따로 들어가 49.5 min 값도 230–247 mV 로 갈리고, **시간 경과 전체(5–49.5 min · L²/D 척도)는 L 만 0.83 mV 로 닫는다**. `[재현·대수]` 그리고 완전 해리 모형의 모든 출력은 I/(A·c₀) 로만 들어가므로 **I/A(면적) ↔ c₀(염 농도)는 정확 대칭**이다(그림 11(A) 에서 두 변경의 RMS 가 12.14 로 같다) — 해리 확장에서만 평형 관계 k_d ∝ c₀ 가 그 대칭을 조금 깬다((C) 5.49 ↔ 6.92). ⚠ 조건: 다른 매개변수(k_a · D_LiPF₆ · 동시 변경)는 시험 안 함 — '바뀐 것은 L' 은 한 매개변수 변경 넷 사이의 비교이고 저자가 무엇을 바꿨는지는 인쇄 0 이다.

---

# ★ (c) Q4 — 해당 없음(액체 모형 원전) · 아흔세 번째 성질

## 1. 이 편이 세운 것 (`[인쇄]` → `[재현·대수]`)

- 관측 ↔ 묶음 지도(닫힌 꼴): **η₀**(켜는 순간) ↔ I·L/(A·c₀·(D₊ + D₋)) · **η_ss**(정상) ↔ x = I·L/(4F·A·c₀·D₊) 하나 · **η_down/η_ss** ↔ t₊ = D₊/(D₊ + D₋) · **과도 시간** ↔ L²/D_amb · **완전 해리 모형 전체** ↔ I/(A·c₀) · L · D₊ · D₋(A ↔ c₀ 정확 대칭).
- 비식별 쪽 문장 하나: "ηss … only depends on DLi+ and is independent on DPF6−" — 정상 관측만으로 D₋ 0 정보.
- 측정 처방 하나: "this ratio is exactly given by the Li+ transference number and delivers a nice tool to obtain this value experimentally"(식 42).

## 2. 이 편이 하지 않은 것 (`[인쇄]`)

- 매개변수 추정 · 감도 · 불확실성 0 · 표 1 은 책 값 · 해리 값은 선택 값.
- 식 (42) 를 자기 측정(그림 9)에 적용 0 — `[재현]` 그림 9 선의 끈 직후 낙차 / 정상 ≈0.48–0.50 ≈ 표 1 Lithylene t₊ 0.5.
- 식 (42) 의 해리 경우 0 — `[재현]` δ 0.8 에서 0.445(t₊ 0.4 · +11 %).
- 그림들의 매개변수 상태 표기 0(표 1 ↔ x 0.9017).

## 3. 어휘 (NFKC · 분철 복원 뒤 · 쪽 머리 제외 · 본문 = 제목 → 감사 · 캡션 포함 | 참고문헌)

`identif*` 0 | 0 · `estimat*` 0 | 0 · `uncertain*` 0 | 0 · `error` 0 | 0 · `sensitiv*` 0 | 0 · `fit` 0 | 0 · `optimi*` 0 | 0 · `experiment*` 14 | 0 · `reference electrode` 3 | 0 · `transference` 4 | 0 · `dissociat*` 38 | 0 · `electro-neutral*` 8 | 0 · `Nernst` 3 | 0(전부 'Nernst–Planck/Plank') · `Newman` 1 | 3 · `Maxwell` 1 | 0 · `activit*` · `thermodynamic factor` · `concentrated solution` · `Poisson` · `double layer` 0 | 0 · `solid` · `vacanc*` · `glass` · `polymer` · `LiPON` · `Li3PO4` · `ceramic` · `single-ion` 0 | 0 · `degrad*` 1 | 0 · `ageing` 1 | 0 · `contact` · `pressure` 0 | 0 · `MATLAB` 1 · `pdepe` 1 · `conductivit*` 6 · `resistance` 4 · `ohmic` 2 · `diffusion` 40 · `migration` 45 · `overpotential` 46 · `temperature` 1 · `Arrhenius` 0.

## 4. 판정 — Q4 해당 없음 · ASSB 0/101 · 아흔세 번째 성질

**해당 없음**(액체 모형 원전 · 매개변수 추정 0) — 셈은 이어 간다: **ASSB 0/101 — 아흔세 번째 성질 "모형 원전 — 측정할 수 있는 비 둘(η₀/η_ss · η_down/η_ss)을 닫힌 꼴로 내고 '식 (42) 가 t₊ 를 실험으로 얻는 도구' 라 인쇄했으나, 같은 지면의 자기 측정(그림 9)에는 적용하지 않았고 같은 지면의 해리 확장에서는 그 유도 전제(정상에서 두 성분 같음)가 깨진다 — 그리고 지면의 그림들은 한 매개변수 표로 닫히지 않는데(표 1 ↔ x 0.9017 상태 · 인쇄 0), 완전 해리의 정상 값(식 37)만으로는 그 차이가 x 묶음 안의 어느 매개변수인지 갈리지 않고 시간 경과가 가른다(우리 재풀이)"** · 누적 0.5 그대로(액체 원전 — 칸 이동 근거 아님).

---

# (e) Q1–Q8 — 채움표 칸 (닻 카드 수집 지침)

| Q | 칸 | 이 편 |
|---|---|---|
| Q1 정량 | **해당 없음 — `θ(N)` 0/101** | 액체 전해질만 · 전극 · `contact` 0 · 층 하나 `[재현·대수]`: 전해질 출력은 I/(A·c₀) 로만 — 면적(전류 밀도) ↔ 염 농도 정확 대칭 · 완전 해리의 정상 과전압은 x = I·L/(4F·A·c₀·D₊) 한 묶음(면적 손실 ↔ 두께 ↔ 염 손실 ↔ D₊ 가 정상에서 안 갈림 — 시간 척도 L²/D 가 L 만 가름) |
| Q2 분리 관측 | **없다 — ASSB 관측 0** | 액체 셀 하나에서 전해질 과전압을 기준극 쌍(in-situ Li 미세 기준극 둘 · [13])으로 따로 잰 측정 하나(그림 9 — 위치 미인쇄 · 표지가 선에 겹침) · 전극 몫 0 |
| Q3 라벨 층위 | **칸 없음 · 층 하나** | "모형 원전 — 매개변수 = [11] 책 값(표 1 · 측정 · 적합 구분 0) · 해리 값 = 선택 · 지면 그림은 두 매개변수 상태(표 1 → 그림 2–8 · 11(A) / L 2.9×10⁻⁴ → x 0.9017 · 61 % · 그림 11(B)–(D) · 12 · 한계 δ — 인쇄 0) · R_ss 0.1950 는 어느 쪽도 아님 · 성분 이름 = 정의 분할(측정 분할 2t₊ : 2(1−t₊)) · 실험 = 다른 셀 그림 하나(기준극 구간 미인쇄)" |
| Q4 유일성 | **해당 없음 — ASSB 0/101 · 아흔세 번째 성질** | 위 §(c) 4 · 식 (42) 처방 · 식 (37) D₋ 무관 문장 · 누적 0.5 그대로 |
| Q5 기준 전위 | **해당 없음** | 액체 · 기준극 = 전해질 안 Li 미세 기준극 쌍([13]) · η = Li⁺ 전기화학 퍼텐셜 차(식 27)라는 정의 하나 — Li 가역 기준극 쌍이 읽는 양과 같은 정의(`[해석]`) |
| Q6 압력 | **해당 없음** | `pressure` 0 |
| Q7 Li 재고 | **해당 없음** | 전극 · 재고 0 · 총 염은 전역 보존(식 46 경계) |
| Q8 OCP · 평형 곡선 | **해당 없음** | OCV · OCP 0 — 전해질만 · δ 80 % = [18] "LiPF6 in PC"(학회 요약 · 용매 다름) |

**누적 ≈20.0 → ≈20.0 (새 칸 0).**

---

# 재현 (`[재현]` — 인쇄 수치 · 식 · 그림 화소로 우리가 계산 · 가정 표시 · 스크립트는 `scratchpad` 에만)

| # | 무엇 | 입력 | 결과 | 대조 |
|---|---|---|---|---|
| R1 | 표 1 기본량 | 표 1 CGR17500 · T 298.15 K | t₊ 0.4 · D_amb 2.4×10⁻¹¹ · I/(FA) 3.731×10⁻⁴ mol m⁻² s⁻¹ · g = I/(2FAD₊) 9.328×10⁶ mol m⁻⁴ · **x 0.8706** | 인쇄 x 0.9017 = L 2.9000×10⁻⁴(넷째 자리) 또는 I 0.7457 A · D1 |
| R2 | 정상 · 켤 때 · 끌 때 플럭스(식 22–25 · 39) | R1 | Li⁺ 확산 = 이동 −1.866×10⁻⁴ · PF₆⁻ ∓2.798×10⁻⁴ · 켤 때 Li⁺ 이동 −1.493×10⁻⁴ · PF₆⁻ +2.239×10⁻⁴ · 끌 때 PF₆⁻ 총 −2.239×10⁻⁴ | "about −18 × 10⁻⁵" · "28 × 10⁻⁵" · 그림 5–7 ✅(L 무관) |
| R3 | 켜는 순간(식 31–32) | R1 | E(y,0) −127.8 V/m · **η₀ 35.79 mV** · R₀ 0.0497 Ω(L 2.9×10⁻⁴: 37.07 · 0.0515 · L 2.85×10⁻⁴ 이면 0.0506) | 인쇄 R₀ ≈0.0506 "simulated" — 재풀이 0.3 min 이동 37.35 mV(첫 단계 확산 몫) · D2 |
| R4 | 정상(식 33–37) | R1 | c(0) 194.1 · c(L) 2805.9 · E(0) −1235 · E(L) −85.4 V/m · **η_ss 137.26 = 68.63 + 68.63 mV** · R_ss 0.1906 Ω(L 2.9×10⁻⁴: 147.5 · 2852.5 · −1625 · 152.22 · 0.2114) | 인쇄 R_ss 0.1950 = x 0.8778 · D2 · 그림 3 "about −1200" ✅(표 1) |
| R5 | 비(식 38) | R1 | 2x/ln((1+x)/(1−x)) 0.652 → η₀/η_ss 0.2607(표 1) · 0.609 → 0.2435(x 0.9017) · 0.1C 편차 0.25 % | "61 %" = x 0.9017 · "agrees well with … Fig. 8" ↔ 그림 8 0.26(표 1) · "less than 1%" ✅ |
| R6 | 끄는 순간(식 39–42) | R4 | η_down 54.90 · 남는 (d) 82.35 · 끈 직후 이동 13.73 mV · η_down/η_ss = 0.400 | 그림 8 (d) `[도표·화소]` 82.0 ✅ |
| R7 | 시간 척도 · 한계 전류 | R1 | τ₁ = L²/(π²D_amb) 5.52 min(Lithylene 1.42) · L²/D_amb 54.4 min · 30 min 에서 잔여 0.4 % · 4FAc₀D₊/L 0.827 A(1.149 × 1C) | "linear after approximately 30 min" ✅ |
| R8 | 완전 해리 PDE 재풀이(유한체적 300 · BDF · 표 1) | 식 (14) · (19) · (30) | 총 0.3 · 1 · 2 · 5 · 10 · 15 · 20 · 25 · 30 · 40 · 50 min **44.9 · 53.0 · 61.2 · 81.3 · 106.6 · 122.4 · 130.7 · 134.5 · 136.1 · 137.1 · 137.2** · 이동 37.35 … 68.61 · 확산 7.55 … 68.61 mV | 그림 8 `[도표·화소]` (a) 48.8 · 53.9 · 62.1 · 82.8 · 107.1 · 122.3 · 130.4 · 134.1 · 135.9 · 137.1 · 137.8 · (c) 37.7 … 68.7 · (b) 8.5 … 68.7 — ±1 mV(0.3 min 총 −3.9) · 판정 3 |
| R9 | 해리 재풀이(식 44–47 · k_a 10⁻⁵ · D_LiPF₆ 2×10⁻¹¹ · 50 min) | L 2.9×10⁻⁴ | δ 0.997 · 0.95 · 0.90 · 0.85 · 0.80 · 0.75 · 0.70 총 152.4 · 157.3 · 163.9 · 172.7 · 184.9 · 203.7 · 240.1 / 확산 76.1 · 77.2 · 78.9 · 81.7 · 86.1 · 93.7 · 109.8 / 이동 76.3 · 80.2 · 85.0 · 91.0 · 98.8 · 110.0 · 130.3 / (d) 15.2 · 15.4 · 15.8 · 16.3 · 17.2 · 18.7 · 22.0 mV | 그림 12 `[도표·화소]` ±3 mV ✅ · 표 1 L 이면 137.4 · 140.9 · 145.7 · 151.8 · 160.1 · 171.8 · 189.8 ✗ · D1 · D3 · D6 |
| R10 | 그림 11 시간 경과(5–49.5 min) | R8 · R9 | (A) 표 1 RMS 0.96 · (B) L 2.9 1.06 · (C) L 2.9 0.83 mV ↔ 표 1 이면 (B) 15.49 · (C) 34.28 | 판정 5 · D1 |
| R11 | x 묶음 가르기 | 같은 x 0.9017 의 한 매개변수 변경 넷 | (C) RMS L 0.83 · I/A 5.49 · c₀ 6.92 · D₊ 5.86 mV · (B) 1.06 · 1.75 · 1.82 · 1.49 · δ 1 조건 49.5 min 넷 모두 152.1–152.2 mV(I/A ↔ c₀ 는 δ 1 에서 RMS 12.14 = 12.14 — 정확 대칭) | §표 1 ↔ 계산 · 곱 축퇴 |
| R12 | 한계 δ(50 min · c(0) → 0.5 mol m⁻³) | R9 · N 300 · 600 | L 2.9×10⁻⁴ **0.6576**(N 600 같음) · 표 1 L 0.6037 · 중성종 고정 0.9227 · 0.8969 | 인쇄 0.6569 ✅(L 2.9) · 판정 7 |
| R13 | 닫음 비교(δ 0.80 · 0.95 · 50 min · 표 1 L) | 이 편 · 고정 · 98호식 국소 | 0.80: 74.01/86.08/160.10 · 고갈 · 7.35/46.28/53.63 / 0.95: 69.01/71.90/140.91 · 84.69/84.69/169.38 · 3.02/38.28/41.30 mV(확산/이동/총) · 이원 몫 0.721 · — · 0.166 / 0.733 · 0.778 · 0.088 · λ 18.3 · 9.0 µm · τ 13.9 · 3.3 s | §(b) 4 · 판정 1 |
| R14 | 식 (42) 의 해리 판 | R13 이 편 닫음 | δ 0.8 낙차 = 이동 − 끈 직후 이동 = 86.08 − 14.80 = 71.28 · 낙차/정상 **0.445**(L 2.9: 0.441) | t₊ 0.4 · 판정 7 |
| R15 | 이원 가정 몫(같은 σ 단일 이온 대비) | 식 (32) · (38) | 표 1 정상 **73.9 %** · Lithylene 51.6 % · δ 0.8 72.1 % · 하한 1 − t₊(작은 x) | 91호 ≈71 % · 98호 ≈8 %(digest 전사) · §Nernst 항 |
| R16 | 그림 9 | 표 1 Lithylene · 켬 → 끔 31.85 min | 전 두께 정상 32.96 · 켜는 순간 15.94 · 낙차 16.48 mV · 가운데 구간 f 0.3112(29.6 µm) → 상승 5.58 · 6.25 · 6.86 · 7.37 · 8.15 · 8.70 · 9.63 · 9.87 / 감쇠 4.01 · 3.36 · 2.80 · 1.95 · 1.48 · 0.71 · 0.34 · 0.18 · 0.09 mV · 전 두께 + 전류 ×0.311(0.0373 A = 0.124C)이면 감쇠 2.69 · 2.23 · 1.86 · 1.29 · 0.98 mV | 그림 9 `[도표·화소]` 선 ±0.15 · ±0.4 mV(가운데 가정) · D7 · G1 |
| R17 | 전기중성 편차 | `[재현·가정]` ε_r 30(미인쇄) · R4 | y = 0 정상 ∂E/∂y 5.9×10⁷ V m⁻² → Δc/c₀ ≈1.1×10⁻¹⁰ | "smaller than ten orders of magnitude" — 뜻 '10 자릿수 작다' 로 읽으면 ✅ · D14 |
| R18 | 해리 평형 | δ 0.80 · k_a 10⁻⁵ | k_d = k_a c₀δ²/(1 − δ) 0.048 s⁻¹ · 평형 c 1200 · c_LiPF₆ 300 mol m⁻³ | 그림 10 초기 300 ✅ |
| R19 | C-rate ↔ 전류 밀도 ↔ 면적 용량 | 표 1 | CGR17500 1C 0.72 A · 3.6 mA cm⁻² · 3.6 mAh cm⁻² / Lithylene 0.4C 0.12 A · 1.35 mA cm⁻² · 3.37 mAh cm⁻² | 본문 "1 C-rate" · "0.4 C" ✅ |
| R20 | 일정 | 2007-11-22 → 2008-02-21 | 91 일 · 수정 85 일 · 온라인 2008-03-02 · PDF 생성 2008-04-29 | — |

---

# 참고문헌 18 번호 — 우리 축에 닿는 것 (번호는 PDF p. 5578 목록에서 직접 확인 · 빠진 번호 0)

| 번호 | 서지(지면 그대로 요약) | 이 편에서 쓰인 자리 | 우리 축 |
|---|---|---|---|
| [11] | Bergveld H.J., Kruijt W.S., Notten P.H.L., *Battery Management Systems, Design by Modelling*, Philips Research Book Series vol. 1, Kluwer Academic Publishers, Boston, 2002 | **표 1 CGR17500 값 전부의 출처**("all taken from Ref. [11]") · t₊ 0.4 "(see Ref. [11])" · "ionic transportation properties of the organic electrolyte has been described in detail … [11]" | 원장 ★(95 \| 1 — L315) · **재지목**(⚠ 액체 · 책) |
| [13] | Zhou J., Danilov D., Notten P.H.L., *Chem. Eur. J.* 12 (2006) 7125 | 서론 "energy losses … due to the limited ionic conductivity of the electrolyte [13]" · 그림 8 정상 성분 일치 "in good agreement with recently reported results [13]" · 그림 9 측정 방법(기준극) · 결론 "experimentally verified by means of in-situ reference electrode measurements [13]" | **새 ★**(⚠ 액체셀 · 기준극 쌍 실측 원전) |
| [17] | Notten P.H.L., Ouwerkerk M., van Hal H., Beelen D., Keur W., Zhou J., Feil H., *J. Power Sources* 129 (2004) 45 | in-house 300 mAh Lithylene 셀 | ☆ |
| [18] | Lee S.-Y., Hang Yong H., Kim S.K., Lee Y.J., Ahn S., Abstract 378, 206th ECS Meeting, Honolulu, Hawaii, 2004 | "LiPF6 in PC is only dissociated for about 80%" | ☆(학회 요약) |
| [12] | Danilov D., Notten P.H.L., Abstract 390, XII IMLB conference, Nara, Japan, 2004 | "the degradation (ageing) process of Li-ion batteries has also been addressed [12]" | ☆(91호 [12] ☆ 와 같은 편 — 91호 digest 전사) |
| [1]–[6] | Doyle · Fuller · Newman *JES* 140 (1993) 1526 · Pals · Newman *JES* 142 (1995) 3274 · Song · Evans *JES* 147 (2000) 2086 · Botte · Subramanian · White *EA* 45 (2000) 2595 · Gomadam · Weidner · Dougal · White *JPS* 110 (2002) 267 · Newman *Electrochemical Systems* 1991 | 서론 배경(P2D · 종설 · 다공 전극) — [1] 은 "early 1980s" 자리(D16) | ☆ |
| [7]–[10] | Kruijt · Notten · Bergveld *JES* 145 (1998) 3764 · Notten · Kruijt · Bergveld *JES* 145 (1998) 3774 · Bergveld · Kruijt · Notten *JPS* 77 (1999) 143 · Kruijt · de Beer · Notten · Bergveld ECS Paris 1997 Abstract 104 | 전자 회로망 모형 | ☆ |
| [14]–[16] | Granqvist *Handbook of Inorganic Electrochromic Materials* 1995 · Bard · Faulkner *Electrochemical Methods* 1980 · Landau · Livshitz *Electrodynamics* 1982 | 전기변색 · Nernst–Planck 식 (3) · Maxwell 방정식 | ☆ |

---

# 인용 대조

## 1. 이 편을 지목 · 인용한 우리 digest — 그 쓰임 ↔ 이 편이 실제로 주는 것

| digest | 쓰임(digest 전사) | 이 편 | 판정 |
|---|---|---|---|
| **26호** Iwakiri 2024 [20] | §11 ★★ "해리 전해질 수송(이온 + 공공)의 원전 — 'SE 에 농도 구배' 가정의 출처" · 본문 :133 "이 모델의 SE 에는 농도 구배가 있다(이온·공공 쌍, Danilov & Notten 2008 계열)" | 식 꼴 ✅(중심 표 넷) · 공공 · 고체 · SE 농도 구배 근거 ❌ | **절반** — 지목 이유를 "해리 이원 액체 전해질 수송 식의 원전(SE 판 물리는 91 · 98호 이식)" 으로 고쳐 적을 후보((먀)) |
| **91호** Danilov 2011 [27] | 후속 ★★★ "식 18 의 유도처 · n⁻ 의 정체(공공인가 · 그렇다면 'Li⁺ only' 와 화해) · k_r · δ 의 값과 단위 · 경계 조건(n⁻ 차단) — k_r ×100 판정의 둘째 대조처" | 유도처 ✅ · 차단 경계 ✅ · 평형 관계 ✅ · n⁻ 정체 ❌(원전 음이온 = PF₆⁻) · k_r 대조 ❌(k_a 선택 값 · 액체) | 다섯 중 셋 ✅ — 'n⁻ = 공공' 화해는 원전에서 확인되지 않는다(원전은 그 물음 밖) |
| **98호** Raijmakers 2020 [28] | '도착' 행 "식 (23)–(24) · (31) 유도처('see Refs. [11,28]')" | (23)–(24) ✅ · (31) 부분(이온–전자 쌍 이식은 98호) | ✅ |
| **100호** Deng 2021 [26] | '도착' 행 "식 (9) η_mt · 식 (10) 전기장의 유도처" · 원 PDE Nernst 항 포함 | ✅ · 원전 정의 = 두 항의 합 | ✅ — 100호 구현이 원전 정의 |
| 99호 Kim 2019 | (인용 0 — 교차) | 99호 식 (14) · (15) = 이 편 (30) · (19) 꼴 · 그림 = 둘째 항만(99호 D1) | 원전 정의와 다른 구현(`[해석]`) |

## 2. 이 편이 인용한 우리 digest

**0** — 18 번호 전수 대조(2008 편 · 우리 digest 는 전부 이 편보다 뒤이거나 다른 편). 4차 묶음 다른 13 편(Danilov 2011 · Firouz 2020 · Bielefeld 2023 · Schmidt 2024 · Khalik 2021 · Lu 2022 · Koerver 2018 · Raijmakers 2020 · Kim 2019 · Deng 2021 · Xie 2008 · Shao 2022 · Ansah 2021)도 인용 0(Xie 2008 은 같은 해 · 나머지는 뒤).

---

# 곱 축퇴 처방 — 여든네 번째 적용 ([[assb-lampe-contact-product-degeneracy]])

⚠ 이 편은 **액체 전해질만의 모형 원전**이다 — 접촉 · LAM · 전극 0. 처방의 입력 점검은 대부분 ❌ 이고, 남는 것은 **정상 묶음(x)을 시간 경과가 깨는 원전 안 표본**이다.

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계**(16호) | `R` 과 `C` 를 같이 | 이중층 · 축전기 0 | ❌ |
| **2단계**(18 · 25호) | + 면적을 아는 대조군 | A = 2×10⁻² · 8.9×10⁻³ m²(표 1 설계값) 하나씩 | ❌ |
| **3단계-a**(19호) | `Ea` | 25 °C 한 점 | ❌ |
| **3단계-b**(19호) | `C` 물리 상한 | — | ❌ |
| **4단계**(20 · 24호) | 시간 영역 | 켬 · 끔 과도(식 31–42 · 그림 8 · 11) · 액체 측정 하나(그림 9) | ✅ 모의 · `[재현]` 그림 11(C) 시간 경과가 x 묶음 안 L 을 I/A · c₀ · D₊ 와 가름(RMS 0.83 ↔ 5.49 · 6.92 · 5.86 mV) |
| 처방 표 "율 스윕" | 여러 율 | 1C(그림) · 0.1C(식 38 문장) · 0.4C(그림 9 — 다른 셀) | ⚠ |
| 처방 표 "`J^T J` 최소 고유벡터" | 적합점 야코비안 | 적합 0 | ❌ |

## ★ 곱 문장 — 셋 (`[인쇄]` → `[재현·대수]` → `[해석]`)

- ① `[인쇄]` 식 (37) η_ss 는 x = IL/(4FAc₀D₊) 하나의 함수 · "independent on DPF6−" ⇒ `[재현·대수]` 완전 해리 모형의 **모든 출력은 I/(A·c₀) · L · D₊ · D₋ 로만** 들어간다 — **면적(전류 밀도) ↔ 염 농도 정확 대칭**(그림 11(A) 조건 두 변경 RMS 12.14 = 12.14) · 정상 값은 x 한 묶음. `[해석]` 접촉(면적) 손실이 전해질 쪽에 '국소 전류 밀도 ↑' 로만 들어가는 모형이라면, 정상 전해질 과전압에서 그 손실은 두께 ↑ · 염 농도 ↓ · D₊ ↓ 와 갈리지 않고, 과도 시간으로도 염 농도 ↓ 와는 갈리지 않는다.
- ② `[재현]` 같은 x 의 네 변경을 그림 11(C)(해리 판) 시간 경과가 가른다 — 시간 척도 L²/D_amb 는 L 만 움직이기 때문이다(L 0.83 ↔ I/A 5.49 · c₀ 6.92 · D₊ 5.86 mV RMS) · I/A ↔ c₀ 는 해리 평형(k_d ∝ c₀)으로만 조금 갈린다((C) 5.49 ↔ 6.92 · (B) 1.75 ↔ 1.82). ⇒ 처방 4단계(시간 영역)가 정상 묶음을 깨는 원전 안 표본이고, 남는 대칭(A ↔ c₀)은 시간 영역으로도 안 깨진다.
- ③ `[인쇄]` 식 (32) η₀ ∝ IL/(A·c₀·(D₊ + D₋)) · 식 (42) η_down/η_ss = t₊ — 켜는 순간 · 끄는 순간 값은 정상 묶음과 **다른 묶음**(전도도 · 운반수)을 본다 ⇒ `[재현·대수]` 세 관측(η₀ · η_ss · η_down)이면 c₀ · L · A 를 알 때 D₊ · D₋ 를 가른다(완전 해리 · 이상 · 정상 도달 조건 — 해리 판에서는 식 42 가 0.445 ↔ t₊ 0.4 로 깨짐).
- ⇒ 처방 표에 **새 줄은 없다**. 후보 메모 하나(처방 표로 올리지 않음 · 결정 대기): **"정상 묶음이 같은 두 가설을 과도(켜고 끄는 순간값 · 이완 시간 척도)로 가르는 시험 — 101호 그림 11 이 x 묶음 안의 L ↔ I/A · c₀ · D₊ 를 시간 척도로 가른 원전 안 표본 · 단 면적 ↔ 염 농도 같은 정확 대칭은 시간 영역으로도 안 깨진다"**.

## ⚠ 이것이 곱을 푼 것은 아니다

- 액체 · 접촉 · 열화 0 인 모형 원전이다 — 위 자리는 **구조**이고 측정이 아니다. x 묶음 가르기는 그림 화소 판독 위의 우리 재풀이이고, 저자가 무엇을 바꿨는지는 인쇄 0 이다.

---
# 보류 결정 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(햐) · (겨)–(펴) — 이 편이 주는 근거 (결정 안 함)

| # | 결정 (요약) | 101호 근거 | 세기 |
|---|---|---|---|
| **(먀)** | '모형 원전' 지목 때 기구 층위 확인 | 26호 '해리 전해질 수송(이온 + 공공)의 원전 — SE 농도 구배 가정의 출처' ↔ 원전 = 액체 LiPF₆ 이온쌍(`solid` · `vacanc*` · `single-ion` 0) · 식 꼴 ✅ · 공공 · 고체 근거 ❌(이식 = 91 · 98호) · 91호 'n⁻ 정체 · k_r 대조처' 도 원전 밖 · `[재현·가정]` 닫음만 바꿔 농도 항 74.0 → 7.4 mV | **강** |
| **(냐)** | 모형 결론의 회고 인용 — 조건 복원 | 91 · 98 · 100호가 "It can be shown[27]" · "see Refs. [11,28]" · "[26]" 로 SE 식의 근거를 이 편에 매달되 원전 조건(액체 · 움직이는 중성 이온쌍 · 이상 묽은 용액 · 일정 D · 전역 보존)을 붙이지 않음 · 26호 '이온·공공 쌍, Danilov & Notten 2008 계열' | **강** |
| **(치)** | 모형 결론 옆 '배제 가정' 표기 | "for fully dissociated salts the diffusion and migration contribution … were exactly balanced"(완전 해리 · 이상 · 일정 D · 정상 — 해리 판에서 깨짐) · "the transference number of Li-ions only determines the instantaneous voltage drop … simple experiments to determining the transference numbers"(식 42 — δ 0.8 에서 0.445 ↔ 0.4) · "migration is of major importance in poorly dissociated electrolytes"(중성종 확산 · 선택 값 k_a · D_LiPF₆ — 고정이면 한계 δ 0.66 → 0.92) | **강** |
| **(세)** | 인쇄 매개변수 표의 재풀이 폐합 검사 | 표 1 로 그림 8(±1 mV) · 11(A)(0.96 mV) 폐합 ↔ 그림 11(B)–(D) · 12 · x 0.9017 · '61 %' · 한계 δ 는 L 2.9×10⁻⁴ 로만(±3 mV · 0.6576) · R_ss 0.1950 은 어느 쪽도 아님 · 그림 9 는 표 1 Lithylene 행 전 두께면 ×3.3(기준극 구간 가정으로만 닫힘) | **강** |
| **(여)** | 표에 적힌 값 ↔ 계산에 쓰인 값 + 출처 번호 | 표 1 L 2.8×10⁻⁴ ↔ 해리 절 계산 L 2.9×10⁻⁴(x 0.9017 넷째 자리 · 시간 경과로 L 만 닫힘) · 표 1 출처 = [11] 책(측정 · 적합 구분 0) · Lithylene 행 출처 0 · "The other parameters are the same as used in Section 4"(4 절 = 결론) | **강** |
| **(셔)** | 인쇄 식 ↔ 그림의 항 폐합 | 원전 그림 8 은 식 (30) 두 항을 다 계산(재풀이 ±1 mV · (b) · (c) 따로) — 100호 구현(포함)이 원전 정의 · 99호 그림(둘째 항만)은 정의와 다름 · 그림 12 (d) 'migration residual' 은 정의 0 이나 식 (40) 값과 ±1.3 mV · 식 (4.3)–(4.4) ↔ (6.3)–(6.4) 부호(계산은 (6.x)) | **강** |
| **(탸)** | 요약 수치 ↔ 같은 편 표 · 그림 | "x is calculated to be 0.9017"(표 1 0.8706) · "61% of the tLi+ value … agrees well with the simulation result shown in Fig. 8"(그림 8 = 0.26 = 65 %) · R_ss 0.1950(0.1906 · 0.2114) · "about −1200 V/m" ✅ · "about −18 × 10⁻⁵" ✅ · "28 × 10⁻⁵" ✅ · "almost two times higher" ✅(1.92) | **강** |
| (펴) | 출력에 안 보이는 성분의 표기 | 같은 총 η 에 성분 이름 두 벌 — 정의 분할('diffusion' : 'migration' = 1 : 1 정상 · 식 36) ↔ 측정 분할(끊는 순간 낙차 2t₊ : 남는 2(1−t₊) · 식 41) · 이동 항(φ 차)은 끊는 실험으로 재는 양이 아니다 · 그림 8 (d) 82.0 ↔ (c) 68.7 mV | 중 |
| (쟈) | '식별 가능' 주장의 층 표기 | 식 (42) "delivers a nice tool to obtain this value experimentally" — 구조적(닫힌 꼴 · 이상 · 완전 해리 · 정상) 주장 · 자기 측정 적용 0 · 해리 판에서 깨짐(0.445 ↔ 0.4) · 식 (37) D₋ 무관 = 정상 관측의 구조적 비식별 문장 | 중 |
| (뱌) | 재매개화 · 묶음의 최소성 | `[재현·대수]` 완전 해리 출력 = I/(A·c₀) · L · D₊ · D₋ — A ↔ c₀ 정확 대칭 · 정상 = x 하나 · 켜는 순간 = 전도도 묶음 · 비 = t₊ · 시간 = L²/D_amb — 지면은 묶음을 말하지 않음 | 중 |
| (녀) | 계면 반응 방향(부호 규약)의 재풀이 폐합 | 원전에서 이미 경계 부호가 두 판 — 식 (4.3)–(4.4) J = +I/(FA) ↔ (6.3)–(6.4) J = −I/(FA) · 계산 · 그림 5 는 물리 쪽((6.x) · 충전 중 Li⁺ 플럭스 음수) — 98호 D2 · D3 경계 부호 문제(98호 digest 전사)의 계보 앞 표본 | 중 |
| (햐) | '계산 ↔ 실험 일치' 의 측정 몫 · 비교 축 | 그림 9 "Good agreement" — 측정 셀 하나 · 표지가 선에 겹침 · 잔차 0 · 모형선은 기준극 구간(미인쇄)에 매달림 · R₀ "in the good agreement with experimental results" 실험값 0 · 그림 8 성분 일치 "[13]" | 중 |
| (텨) | '실험 검증' 그림의 자료 경로 표기 | 그림 9 = in-house Lithylene([17]) · 측정법 [13] · 그 그림에만 쓴 입력(Lithylene 행 · 기준극 위치 — 위치 미인쇄) · CGR17500 실험 0 | 중 |
| (며) | 'validated' 의 자료 층위 | "The presented model has been experimentally verified. A typical example is shown in Fig. 9" · 결론 "experimentally verified by means of in-situ reference electrode measurements [13]" — 측정 하나 · 다른 셀 · "A more detailed comparison … in progress" | 중 |
| (뎌) | '문헌값 일치' 의 자료 독립성 | 그림 8 정상 성분 일치 "in good agreement with recently reported results [13]"(같은 저자 연구망 측정) · R₀ 실험 일치(값 · 출처 0) | 중 |
| (대) | C-rate 의 기준 용량 표기 | 720 mAh · 0.72 A = 1C · 300 mAh · 0.12 A = 0.4C — 전류 ↔ C-rate 폐합 ✅ · `[재현]` 3.6 · 1.35 mA cm⁻² | 약 |
| (다) | 액체 도구를 ASSB Q4 분모에 | 액체 모형 원전 한 편 더(ASSB 0/101) — 도구 아님 · 식별 처방 하나(식 42) | 약 |
| (에) | 속도 상수의 i₀ 환산 표기 | 해리 k_a 10⁻⁵ m³ mol⁻¹ s⁻¹(91호 k_r 과 같은 단위 · 선택 값) · `[재현]` k_d 0.048 s⁻¹ · τ 13.9 s · λ 18.3 µm — 91호 k_r ×100 판정의 대조처는 못 된다 | 약 |
| (이) | 모형 값 인용 규칙 | 표 1 = [11] 책의 모형 입력 · Lithylene 행 출처 0 — SE 계보는 이 편에서 값이 아니라 식만 가져갔다 | 약 |
| (헤) | 측정 입력의 역모형 층위 | L · D · c₀ 의 층위(분리막 ↔ 유효 · 벌크 ↔ 유효) 미인쇄(G2) | 약 |
| (갸) | '단순성' 근거 명제의 척도 | "reduced to simple diffusion equations with modified diffusion coefficient, facilitating the efficient use of numerical methods" — 척도 = 식 수 · 대가(이상 용액 · 일정 D · 전기중성)는 지면에 조건으로 없음 | 약 |
| (쳐) | 축약 · 근사 모형 오차 주장의 지표 · 조건 | 전기중성 근사의 오차 "smaller than ten orders of magnitude"(지표 · 계산 방법 · ε_r 미인쇄 — `[재현·가정]` ε_r 30 이면 ≈10⁻¹⁰) | 약 |
| (마) | 37호 "ASSB truth 5조건" — **결정 · 반영(2026-09-23)** | R 목록에는 근거 0 — 개념 페이지 '목록 밖 메모'(전해질 수송 모형 · 닫음 표기 — 결정 아님)만 | — |

나머지 — (라)(바)(사) 결정 · 반영됨(이 편 근거 0), 그 밖의 글자는 **근거 0**(압력 · 기준 전위(In) · 3전극 · 노화 사이클 · LLI 실측 · θ 판정 · 상 분율 · 입도 · 피복률 · 프로토콜 비교 · 원자료 예치 · DRT · 축전기 · OCV 곡선 · 상태 추정 · 주파수 차수가 이 편에 없다). **결정 안 함.**

## 새 판단 거리 (넷 — 글자는 호출자가 붙인다)

1. **새1 — 이식된 수송 식의 원전 계 · 닫음 표기** ((먀) · (냐) 의 이식판으로 묶어도 됨) — 유도처가 다른 계(액체 이온쌍)인 식을 SE 모형 · 합성 truth · 카드로 옮길 때 ① 원전의 운반체와 중성종 닫음(확산 PDE ↔ 고정 ↔ 국소 보존) ② 이식 편이 바꾼 것(무엇이 음전하 운반체인가 · 무엇이 보존되는가) ③ 그 바꿈이 결론(농도 항 · 이원 가정 몫 · 한계 전류)에 주는 크기를 같이 적게 할지 — 101호 `[재현·가정]` δ 0.8 · 50 min: 이 편 닫음 농도 항 74.0 · 합 160.1 mV ↔ 98호식 국소 닫음 7.4 · 53.6 mV · 중성종 고정이면 50 min 한계 δ 0.60 → 0.90.
2. **새2 — 과전압 성분 이름의 정의 분할 ↔ 측정 분할 표기** ((펴) 의 정의판으로 묶어도 됨) — 'diffusion · migration · Nernst · ohmic' 성분을 truth · 라벨 · 카드로 옮길 때 그 분할이 정의(μ̄ = μ + zFφ 의 화학 ↔ 정전 부분)인지 측정(전류 차단 순간 낙차 ↔ 이완)인지 적게 할지 — 101호: 정상에서 정의 분할 1 : 1(식 36) ↔ 측정 분할 2t₊ : 2(1−t₊)(식 41 — t₊ 0.4 면 40 : 60) — 같은 합 · 다른 성분 · 99호 '둘째 항만' 플랜트는 둘 중 어느 쪽도 아니다.
3. **새3 — 한 지면 그림들의 매개변수 상태 일관성 검사 (표 하나 ↔ 그림 여럿)** ((세) · (여) 의 그림판으로 묶어도 됨) — 모형 편의 그림을 truth · 비교 기준 · 개념으로 옮길 때 그림마다 같은 표로 닫히는지 확인하고, 다른 상태가 섞였으면 그림별로 적게 할지 — 101호: 그림 2–8 · 11(A) = 표 1(L 2.8×10⁻⁴) ↔ 그림 11(B)–(D) · 12 · x 0.9017 · '61 %' · 한계 δ = L 2.9×10⁻⁴(인쇄 0) · R_ss 0.1950 은 어느 쪽도 아님 — 한 그림(11) 안에서도 갈림.
4. (선택) **새4 — 닫힌 꼴 '측정 비 → 매개변수' 처방의 조건 표기** ((쟈) 의 닫힌 꼴판으로 묶어도 됨) — 'X/Y = t₊' 같은 닫힌 꼴을 측정 처방으로 옮길 때 ① 성립 조건(완전 해리 · 정상 도달 · 이상 · 일정 D) ② 같은 지면 확장에서 성립하는지 ③ 자기 자료에 적용했는지를 적게 할지 — 101호 식 (42): 해리 판 δ 0.8 에서 0.445 ↔ t₊ 0.4(+11 %) · 그림 9 에 적용 0(`[재현]` 선 낙차 / 정상 ≈0.48–0.50).

---

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** ★★★ | 표 1 L 2.8×10⁻⁴ ↔ 인쇄 x 0.9017 · "61 %" · 그림 11(B)–(D) · 12 · 한계 δ 0.6569(= L 2.9×10⁻⁴ 상태 — 인쇄 0) · "This agrees well with the simulation result shown in Fig. 8"(그림 8 의 비 0.26 = 표 1 의 65 %) | R1 · R5 · R9 · R10 · R12 |
| **D2** ★★ | R_ss "0.1950 (Ω) in the simulations" ↔ 표 1 해석 0.1906 · L 2.9×10⁻⁴ 0.2114 · 그림 8 정상 137.8 mV / 0.72 A = 0.1914 — 어느 쪽도 아님(x 0.8778) · R₀ 0.0506 ↔ 해석 0.0497(+1.8 % — 첫 단계 확산 몫으로 설명 가능) | R3 · R4 |
| **D3** ★★ | 같은 '완전 해리' 가 두 값 — 그림 8 · 11(A) 정상 137 mV ↔ 그림 12 δ → 1 끝 152 mV | R8 · R9 |
| **D4** ★★ | 식 (4.3)–(4.4) J_Li⁺ = −I_LiC₆/(FA) = +I/(FA) ↔ 식 (3) 을 넣은 (6.3)–(6.4) 는 J = −I/(FA) — 부호 반대(렌더 확인) · 그림 1 · 5 는 (6.x) 쪽 | 쪽 렌더 · 그림 1 · 5 |
| **D5** ★★ | 그림 11 본문 (ii) "initial migration overpotential η0 also grows … (curves (b) in Fig. 11)" · (iv) "The migration component (curves (b)) is always larger than the diffusion component (curves (c))" ↔ 캡션 · (iii) "(b) 확산 · (c) 이동" · 그림 배치(정상 (c) > (b)) | 그림 11 `[도표·화소]` |
| **D6** ★★ | 그림 12 곡선 (d) "migration residual" — 본문 정의 0(식 40 값과 ±1.3 mV) | R9 |
| **D7** ★★ | "The parameter values used in the simulations can be found in Table 1"(그림 9) ↔ 표 1 Lithylene 행 전 두께면 정상 32.96 mV(그림 9.95 · ×3.3) — 기준극 구간 미인쇄 · 가운데 29.6 µm 가정이면 닫힘 | R16 · G1 |
| **D8** ★ | "The other parameters are the same as used in Section 4"(해리 절) — 4 절은 결론 · 표 1(3.1 절)을 가리키는 것으로 읽힘 | p. 5576 |
| **D9** ★ | 식 (24) "the total diffusion flux" · 식 (25) "the total migration flux" — 실제로는 Li⁺ · PF₆⁻ 각각의 총 플럭스 | p. 5571 |
| **D10** ★ | "As expected, PF6− does not contribute to the overall ionic conductivity" ↔ 같은 쪽 "it clearly contribute to the ionic conductivity in the electrolyte, especially under the most dynamic, current on/off switching, conditions" — 정상 ↔ 과도 조건이 문장에 없음 | p. 5573 · 그림 7 |
| **D11** ★ | "(ii) … From Eq. (32) it can be concluded that the resulting reduction factor is exactly 1/δ. This decrease is entirely attributed to reduction in the dissociated salt concentration." — η₀ 은 1/δ 배 **증가**(같은 문단 첫 문장 "grows") | p. 5577 |
| **D12** ★ | 그림 4 캡션 "migration overpotential … calculated according to Eq. (30)" ↔ 축 φ(y,t) · 본문 "Galvany potential difference … (Eq. (28))" · 본문 "the high electric field in Fig. 3b"(그림 3 은 판 하나) · "at y = 1"(무차원 y — 그림 축에서만 정의) | 그림 3 · 4 |
| **D13** ★ | 그림 2–7 · 10 y 눈금 "1.0 · 0.8 · 0.4 · 0.4 · 0.2 · 0"(0.6 자리 0.4) | 그림 |
| **D14** ★ | "the degree of deviation from electro-neutrality is calculated to be smaller than ten orders of magnitude with respect to the equilibrium electrolyte concentration" — 뜻은 '10 자릿수 작다' 로 읽힘 · 계산 방법 · ε_r 미인쇄 | R17 · G11 |
| **D15** ★ | "R0 ≈0.0506 (Ω), which is in the good agreement with experimental results" — CGR17500 실측값 · 출처 0(그림 9 는 다른 셀) | G9 |
| **D16** ★ | "already dates back to the early 1980s [1]" ↔ [1] = Doyle · Fuller · Newman 1993(91호 서론 같은 문장 · 같은 어긋남 — 91호 D9 digest 전사) · 오자 — 키워드 "Nernst–Plank" · 그림 1 캡션 "electolyte" · "Galvany" · "inital" · "The later value" | p. 5569 · 5577 |
| **D17** ★ | 결론 "the transference number of Li-ions only determines the instantaneous voltage drop" ↔ 식 (41) η_down = 2t₊(RT/F) ln(c(L)/c(0)) — 낙차 자체는 t₊ 와 농도 비(D₊ · I · L · A · c₀)에 같이 매임 · t₊ 하나만 정하는 것은 비 η_down/η_ss(식 42 — 완전 해리 · 정상) | p. 5577 |

---

# 이 편이 우리 프로젝트에 주는 것 (정리)

- **계보 원전의 범위** — ASSB 박막 모형 다섯(26 · 91 · 98 · 99 · 100호)의 전해질 수송 식은 이 액체 이온쌍 원전의 꼴이다. 'SE 에 농도 구배' 는 원전이 아니라 이식(n⁻ 을 움직이게 둠 · 중성종 닫음)의 선택이다 — 합성 truth 에 SE 전해질 모형을 넣으면 그 선택(이원 ↔ 단일 이온 · 닫음)을 적어야 한다(우리 반사실: 닫음만 바꿔 농도 항 ×0.1 · 이원 가정 몫 72 → 17 %).
- **성분 이름은 정의 의존** — 같은 총 과전압에 'diffusion/migration'(정의 1 : 1) ↔ '옴/농도'(측정 2t₊ : 2(1−t₊)) 두 벌. 우리 `degradation-degeneracy/` 의 물음("곡선이 맞는다 ≠ 분해가 맞다")의 원전 층 표본 — 성분 라벨을 쓰는 쪽은 분할 규약을 같이 적는다(우리 수치는 `degradation-degeneracy/docs/RESULTS*.md` 정본 — 옮기지 않음).
- **99 · 100호 구현 판정의 기준** — 원전 정의 η = Li⁺ 전기화학 퍼텐셜 차(Nernst 항 포함) · 원전 그림도 두 항을 계산 → 100호 = 원전 · 99호 그림 = φ 차.
- **원전 그림의 매개변수 상태 혼재** — 표 1 ↔ x 0.9017(L 2.9×10⁻⁴) · R_ss 는 어느 쪽도 아님 — 원전 그림을 truth 비교 기준으로 쓰기 전에 그림별 폐합이 필요하다.
- **정상 묶음 ↔ 시간 경과** — x 묶음 안 L 을 시간 척도가 가른다 · 면적(전류 밀도) ↔ 염 농도는 정확 대칭(시간으로도 안 깨짐) — 곱 축퇴 처방 4단계의 원전 안 표본과 그 한계.
- **이 편이 주지 않는 것**: 고체 전해질 · 접촉 · 열화 · LAM · LLI · OCV · 전극 · 매개변수 추정 · 식별성 계산 · 원자료 · 코드 — 그리고 101 편 누적 `θ(N)` 0.

---

# 후속 후보 (원전 우선 — 지목 수는 위키 digest 의 후속 절 grep 으로 센 값)

| 등급 | 서지 (PDF 목록 번호) | 지목 (후속 절) | 왜 | 축 |
|---|---|---|---|---|
| ★ | Zhou J., Danilov D., Notten P.H.L. 2006 — *Chem. Eur. J.* **12**, 7125([13]) | **101** = 1(새) | ⚠ **액체셀** — 전해질 안 in-situ Li 미세 기준극 쌍으로 전해질 과전압을 따로 잰 실측 원전 · 이 편 그림 9 측정 방법 · 기준극 위치(이 편 G1)의 확인처 · 그림 8 정상 성분 일치 "in good agreement with recently reported results [13]" 의 근거 · 결론 "experimentally verified by means of in-situ reference electrode measurements [13]" | Q2 · Q5(액체 판) · (햐) |
| ★ | Bergveld H.J., Kruijt W.S., Notten P.H.L. 2002 — *Battery Management Systems, Design by Modelling*, Philips Research Book Series vol. 1, Kluwer([11]) | 95 · **101** = **2**(재지목) | ⚠ **액체 · 책** — 표 1 CGR17500 값 전부의 출처 · t₊ 0.4 · L 2.8×10⁻⁴ · D 의 층위(분리막 ↔ 유효 — 이 편 G2) · x 0.9017 상태(L 2.9×10⁻⁴?)의 대조처 · 95호 이유(EMF 결정 기법 개관)와 같은 책 | 모델 · (여) |
| ☆ | Notten 외 2004 *JPS* 129, 45([17] — Lithylene 셀) · Lee S.-Y. 외 2004 ECS 요약 378([18] — LiPF₆ in PC 80 %) · Danilov & Notten 2004 IMLB 요약 390([12] — 91호 ☆) · Doyle · Fuller · Newman 1993([1]) · Pals · Newman 1995([2]) · Song · Evans 2000([3]) · Botte 외 2000([4]) · Gomadam 외 2002([5]) · Newman 1991 책([6]) · Kruijt · Notten · Bergveld 1997–1999([7]–[10]) · Granqvist 1995([14]) · Bard · Faulkner 1980([15]) · Landau · Livshitz 1982([16]) | 행 없음 | 서론 배경 · 일반 교재 · 학회 요약 | — |

**지목 누락 0**(이 편 18 번호 중 ★ 이상인데 원장 행이 없던 편이 앞 호 후속 절에 있는 경우 — 없음 · [11] 은 원장 L315 행 있음). 등급 칸 없는 옛 후속 표에만 있던 편 0. **흡수된 편(교차)**: 0. **4차 묶음 도착 편**: 0(이 편이 인용하는 4차 묶음 편 없음).

---

# 이 digest 가 주장하지 않는 것

- **이 편의 모형이 틀렸다고 하지 않는다** — 축약(식 11–14) · 전기장(식 19) · 닫힌 꼴(식 31–42)은 우리 대수와 맞고, 그림 8 · 11 · 12 는 우리 재풀이와 ±1–3 mV 로 닫힌다. 걸린 것은 그림들의 매개변수 상태 표기 · R_ss · 그림 9 의 입력 · 결론 문장의 조건 탈락 · 경계 부호 · 곡선 글자다.
- **이 편을 SE 에 해리 이원 모형을 쓰면 안 된다는 근거로 쓰지 않는다** — 이 편은 고체에 대해 아무것도 말하지 않는다. 91 · 98호의 이식 근거(유리 'weak electrolyte' 모형 · nBO · LiPON 공공)는 그 편들의 몫이고 여기서 판정하지 않는다.
- **닫음 비교표(§(b) 4)를 SE 의 값으로 쓰지 않는다** — 이 편 액체 매개변수에 닫음만 바꾼 반사실이다. 91 · 98호의 실제 몫(≈71 · ≈8 %)은 그 digest 들의 계산이다.
- **저자가 L 을 2.9×10⁻⁴ 로 바꿨다고 확정하지 않는다** — x 0.9017 이 넷째 자리까지 맞고 그림 11(C) 시간 경과가 한 매개변수 변경 넷 중 L 만 0.83 mV 로 닫는다는 것까지다(다른 변경 · 동시 변경 미시험 · 코드 미공개).
- **그림 9 의 기준극이 가운데 29.6 µm 구간에 있었다고 확정하지 않는다** — 그 가정이면 선이 닫힌다는 것까지다(위치 미인쇄 · [13] 미열람).
- **'migration overpotential' 이 쓸모없는 양이라고 하지 않는다** — 정의 분할로는 일관되고 해리 판 해석(이동이 폭주를 이끈다)에 쓰인다; 주장은 측정 분할(전류 차단)과 다른 이름이라는 것까지다.
- **이 편을 Q4 · Q1 칸 이동 근거로 쓰지 않는다** — 액체 원전 · 식별성 계산 0 · 열화 0.
- **원 참고문헌(26 · 91 · 98 · 99 · 100호 인용분)을 다시 열지 않았다** — 대조는 각 digest 전사로 했다.
