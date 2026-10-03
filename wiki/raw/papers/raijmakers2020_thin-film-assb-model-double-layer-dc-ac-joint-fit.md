---
title: "Raijmakers L.H.J., Danilov D.L., Eichel R.-A., Notten P.H.L. 2020 — An advanced all-solid-state Li-ion battery model (Electrochim. Acta 330, 135147)"
source_url: local-upload/58._An_advanced_all-solid-state_Li-ion_battery_model.pdf
source_url_note: "본문 PDF 19 쪽(Electrochimica Acta 330 (2020) 135147 · 인쇄 쪽 1–19 · 그림 11 — 래스터 6 · 벡터 5 · 표 3 · 식 (1)–(32) + 부록 (A.1.1)–(A.14) · 참고문헌 42) 3,754,525 B · 업로드 접두사 e5b2203a · 4차 묶음 파일 58 · SI 없음(보충 언급 0 — 부록 A 는 본문 안) · 원자료 · 코드 공개 0 · 2026-10-03 재개 작업(중단된 앞 작업을 이어받아 원문 · 식 렌더 · 그림 17 장 · 재풀이를 이 실행에서 다시 확인)"
source_doi: 10.1016/j.electacta.2019.135147
source_license: "© 2019 Elsevier Ltd. All rights reserved.(인쇄) · CC · 오픈 액세스 표기 0 · 구독본으로 다룬다 — 이 digest 는 인용 · 요약 · 재현 계산만 담는다(그림 크롭은 위키 관례대로 raw/figures 에 — 변형 없는 잘라내기)"
pdf_sha256: e21931c869c01649cef0468021d5b55ac2365cfa429c2e9b42cda3a3e1b93018
ingested: 2026-10-03
sha256: 14a949ea0048fc449c3545cc0ba5a4af704bf0341bcad3b43be121676f5ba652
---
# 수집 목적

`assb` 섹션 **98호** — **4차 묶음 파일 58**(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 요청 14 편 중 여덟째 · 2026-10-02 사용자 공급 · 파일 51–64 = 91–104호를 받은 순서대로). 닻은 `questions/assb-contact-loss-vs-lampe.md` 의 **Q4(유일성 · 식별성)** 와 **Q3(라벨 층위)** 이고, 이 편이 직접 닿는 곳은 ① **26호**(Iwakiri 2024 — 데이터 · "문헌값" · 평형 곡선 · `β` 를 전부 이 편에서 가져왔다고 적은 편) ② **37호**(Li 2024 — 이 편을 "이중층 항의 조상" 으로 매단 복합양극 모형) ③ **91호**(Danilov 2011 — 같은 연구실 계보의 첫 매개변수 표) ④ 개념 [[assb-sensitivity-sweep-vs-identifiability]] · [[spm-grouped-parameter-identifiability]] · [[assb-synthetic-truth-contact-loss-requirements]] 다. 우리 쪽 수치(`degradation-degeneracy/` · `mode-observability`)는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본이고 여기 옮기지 않는다.

Forschungszentrum Jülich(IEK-9) + TU Eindhoven + RWTH Aachen + UTS Sydney(**L.H.J. Raijmakers** · **D.L. Danilov** · **R.-A. Eichel** · **P.H.L. Notten**(교신))의 *Electrochim. Acta* 2020 편. `[인쇄]` 초록이 스스로 적는다: "A new advanced mathematical model is proposed to accurately simulate the behavior of all-solid-state Li-ion batteries. The model includes charge-transfer kinetics at both electrode/electrolyte interfaces, diffusion and migration of mobile lithium ions in the electrolyte and positive electrode. In addition, electrical double layers are considered, representing the space-charge separation phenomena at both electrode/electrolyte interfaces. … Both galvanostatic discharge and impedance simulations have been experimentally validated with respect to 0.7 mAh Li/LiPON/LiCoO2 thin film, all-solid-state, batteries. The model shows good agreement with galvanostatic discharging, voltage relaxation upon current interruption, and impedance measurements. From the performed AC and DC simulations it can be concluded that the overpotential across the LiPON electrolyte is most dominant and is therefore an important rate-limiting factor." 이 편이 실제로 한 것은 **상용 박막 셀(0.7 mAh · Li | LiPON 3.62 µm | LiCoO₂ 8.08 µm | Pt · 3.36 cm² · 셀 수 미인쇄)의 일곱 율 방전 + 이완 + 한 상태(3.9 V) EIS 에, 91호 모형을 넓힌 1D 모형(양극 이온 · 전자 쌍극 Nernst–Planck + 공통 `β(y,t)` · 두 계면 BV + 이중층 축전기 · 셀 전체 기하 축전기 · 직렬 저항)을 "단일 매개변수 한 벌" 로 맞춘 것**이다. 열화 · 접촉 · 압력 · 온도 축은 0 이다(`[인쇄]` "the aging-related processes, such as decomposition of electrolyte and electrode materials as well as contact losses due to electrode deformation are beyond the scope of this work").

들어온 경로: 원장 행(도착 표시 전 원문 그대로) "| ★★★ | **Raijmakers·Danilov·Eichel·Notten 2020** — *Electrochim. Acta* **330**, 135147 | 26 · 37 | **2** | Q4·Q3 | 26호의 **데이터·"문헌값"·평형 곡선·β 함수가 전부 이 한 편**에서 온다. 26호 적합 변수 10개 중 7개가 정확히 문헌값 ×1.0500 이고 `D_e⁻` 가 10 자릿수 벗어났다 — 문헌값이 **측정인지 적합인지** 여기서만 확인된다 · 37호: 복합양극 모델 **이중층 항의 조상** — `c_dl` 이 면적에 비례하는가 (37호 `c_dl` 은 면적 무관 전극 상수 → R·C 처방 전제가 truth 에서 거짓) |". 위키 grep(`Raijmakers` · `135147` · `electacta.2019.135147` · `Eichel` · "An advanced all-solid-state")으로 각 digest 의 **후속 절**을 다시 셌다: **26호 §11(:380 · "왜" 칸 ★★★★ · [10]) · 37호 §14(:412 · [14] — 등급 칸 없는 후속 표) = 2 — 원장 "2" 와 일치**(정정 없음). 교차 기록(지목 아님): 91호 :618 "교차 참조 (지목 아님 — 이 편 이후 편)" · 92 · 93 · 94 · 95 · 96호 "4차 묶음 13 편과의 관계" 문장(인용 0) · 27호 "이 편이 인용하지 않는 것" 목록. 이 편은 우리 digest **하나**를 인용한다([11] = 91호) · 4차 묶음 다른 13 편 중 **[11](파일 51) · [28](파일 61 Danilov & Notten 2008) · [31](파일 62 Xie 2008)** 셋을 인용한다(42 번호 전수 대조).

⚠ **재개 작업**: 이 digest 는 앞 에이전트가 컨테이너 재시작으로 끊긴 작업을 2026-10-03 에 이어받아 끝냈다. 앞 에이전트의 상태 메모 · 본문 조각은 **근거로 쓰지 않았다** — PDF 메타데이터 · 본문 전문 · 식 렌더 · 그림 17 장 · 재풀이 스크립트를 이 실행에서 다시 열고 다시 돌린 값만 적었고, 메모와 다른 값은 이 실행의 값으로 고쳤다(그림 9 의 1C 판독 · 그림 11c 의 표지 중심 · 그림 3 잔차 RMS 의 몸통 정의 · 그림 4 이완 잔차 · 따옴표 순서 하나 — 보고서에 목록).

이 digest 의 일 (지시):

1. **(a) 매개변수 표의 출처 층위** — 표 3 21 행마다 측정 · 문헌 · 적합 · 가정 · 26호 표와 같은 이름끼리 나란히(×1.0500 관계가 이 편 값 기준으로 성립하는가 · `D_e⁻` 의 원래 값).
2. **(b) 이중층(공간 전하) 항** — 정의 · 면적 의존(기하 면적 ↔ 실제 계면) · `c_dl` 값의 출처 → 37호 물음.
3. **(c) 검증** — 정전류 방전 · 전류 차단 이완 · 임피던스와의 대조가 한 벌로 되는가 · 맞춘 것과 예측한 것.
4. **(d) 91호와의 계보** — 2011 → 2020 에서 바뀐 물리 · 값.
5. **(e) Q4** — 식별성 · 불확실도 어휘 전수 · "n 번째 성질".
6. **(f) 후속 후보.**

⚠ **표기 규약**: `[인쇄]` = 원문이 실제로 쓴 것 · `[도표]` = 그림을 눈으로 읽은 값(판독 폭 표시) · **`[도표·벡터]`** = PDF 벡터 경로 좌표를 축 상자 · 눈금 글자로 보정해 읽은 값(그림 3 · 5 · 8 — 저자 원자료가 아니다) · **`[도표·화소]`** = 래스터 그림(4 · 6 · 7 · 9 · 10 · 11)의 화소 좌표를 축 상자 · 눈금 글자로 보정해 읽은 값(1 화소 = 그림 4 2.48 mV · 그림 9 1.863 mV · 그림 11c 0.11 Ω cm² · 11a · b 0.63–0.64 Ω cm² — 선 두께 · 표지 크기 · 선 겹침만큼 넓다 · 표지는 중심으로) · `[재현]` = 원문 수치 · 식으로 우리가 다시 계산 · `[재현·가정]` = 가정이 붙은 재현(가정을 같이 적는다) · `[재현·대수]` = 인쇄된 식만으로 한 대수 · `[재현·외부 값]` = 원문 밖 상수를 쓴 재현 · `[해석]` = 우리 해석 · **"(N호 digest 전사)"** = 이 세션에서 그 원문을 다시 열지 않고 우리 digest 의 전사로 대조한 것. **`[데이터]` 0** — 예치 원자료 · 코드 공개 진술 0.

⚠ **측정 · 인용 · 모형 · 적합 구분**: 이 편 안의 수치는 ① **측정**(일곱 율 방전 · 이완 · 한 상태 EIS — 그림 3 · 4 · 11a 의 표지 · 표 3 의 T · A(각주 a) · L · M(각주 b SEM — SEM 그림 0)) ② **유도**(표 3 `c_max` "Calculated from the EMF voltage curve" · EMF 곡선 자체 = 같은 방전 곡선 묶음의 "mathematical extrapolation") ③ **사전 고정**(αp · αn 0.5 · `c_Li` 7.64×10⁴) ④ **적합**(표 3 무각주 13 행 — 본문 "The optimized model parameters are listed in Table 3" · 그림 5 의 `D(x)` 곡선 = `β(x)`) ⑤ **모형 출력**(그림 6 · 7 · 9 · 10 · 11b · c 의 분해 · 농도장 · 전기장 · 과전압 몫) 다섯이다. 섞지 않는다. 인용 값 비교는 둘뿐이다(Put [40] "estimated value of 40 kmol m⁻³" · [12, 35] "in agreement" — 값 미인쇄).

⚠ **쪽 표기**: PDF 19 쪽 = 인쇄 쪽 1–19(바닥 "L.H.J. Raijmakers et al. / Electrochimica Acta 330 (2020) 135147" + 쪽 번호 · 논문 번호 135147). 이 digest 는 **"p. 8"** 로 적는다(PDF 쪽 = 인쇄 쪽 · PageLabels 도 1 부터).

---

# 판정 먼저

1. ★★★★ **(a) 표 3 의 층위 — 21 행 = 직접 측정 2 · SEM 2 · 사전 고정 3 · EMF 유도 1 · 무각주 13("optimized") 이고, 26호의 "문헌값" 10 개는 이 표의 숫자와 자릿수까지 같으며 그중 9 개가 이 편의 적합값이다 — 26호 G4("문헌값이 적합값인가")는 '예' 로 닫힌다.** `[인쇄]` 각주 "a Identified by direct measurements. b Measured with Scanning Electron Microscope. c Predefined (non-optimized) parameters. d Calculated from the EMF voltage curve." · 본문 "The optimized model parameters are listed in Table 3" · "The optimized parameter values are reported in Table 3"(c₀ · δ). 무각주 13 = `k_r` 8.00×10⁻⁷ · `k₁ˢ` 1.53×10⁻¹¹ · `k₂ˢ` 1.09×10⁻⁹ · `D⁰_Li⊕` 1.21×10⁻¹³ · `D⁰_e⁻` 5.06×10⁻¹³ · `D_Li⁺` 1.73×10⁻¹⁶ · `D_n⁻` 5.69×10⁻¹⁶ · `c₀` 61141 · `δ` 0.64 · `ρ_s` 18.3 Ω cm² · `c^p_dl` 5.30×10⁻⁷ · `c^n_dl` 1.74×10⁻⁸ · `c_geo` 3.24×10⁻⁹ F cm⁻²(쪽 렌더로 지수 부호 확인). **같은 0.7 mAh 셀 계열의 DC 일곱 율 + EIS 한 상태를 이중층 · 기하 용량 · 직렬 저항이 있는 모형으로 동시에 맞춘 값**이다(목적 함수 · 알고리즘 · 잔차 · 불확실성 0 — G1). 26호(26호 digest §3-2 전사)는 이 가운데 9 개를 "문헌값" 으로 적고 적합했고, 10 번째 `a^max` 는 이 편의 **EMF 유도값**(각주 d)이다. `[재현]` ×1.0500 관계는 이 편 인쇄값 기준으로 그대로 선다(8.00 → 8.4000 · 1.09 → 1.1445 · 1.21 → 1.2705 · 1.73 → 1.8165 · 5.69 → 5.9745 · 3.22 → 3.3810 · 61141 → 64198.05 · `k₁ˢ` ×1.04575 · `δ` ×1 · `D⁰_e⁻` 5.06×10⁻¹³ → 5.24×10⁻³ ×1.036×10¹⁰). **`D_e⁻` 의 원래 값 5.06×10⁻¹³ 은 이 편의 적합값**(`D⁰_Li⊕` 의 ×4.18 — 공통 `β` 라 비가 상수)이다. 26호가 고정한 `ρ_Li+Pt` 18.3 Ω cm² 도 이 편에서는 무각주 적합값이다. ⇒ **26호 "문헌과 5 % 이내" = 같은 셀 · 같은 곡선에 대한 두 적합의 일치**(원 편은 AC 와 이중층까지 넣은 적합). ★ 그리고 `[재현·대수]` **같은 이름 ×1.05 뒤에서 모형이 실제로 보는 조합은 움직였다**: 양극 쌍극 확산 `D⁰_p = 2D_Li⊕D_e⁻/(D_Li⊕+D_e⁻)` 는 이 편 1.953×10⁻¹³ ↔ 26호 최적 2.541×10⁻¹³(**×1.30** — `D_e⁻` 10 자릿수 표류로 `2D_Li⊕` 극한) · 양극 두 경계의 중성 Li 공급 분배(전해질 쪽 : 집전체 쪽 = `D_e⁻ : D_Li⊕`) 80.7 : 19.3 → **100 : 0** · 전해질 전도도 `σ ∝ δc₀(D₊ + D₋)` ×1.1025(벌크 저항 326 → 296 Ω cm²) · i₀ ×1.08(음극) · ×1.13(양극).
2. ★★★★ **(c) 재풀이 폐합 — 전해질 · 양극 계면 · 호 지름은 인쇄 표 그대로 저자 그림이 나온다(91호의 ×100 과 반대). 그러나 음극 계면은 인쇄 식 (12) · (16) 을 글자 그대로(두 계면에 같은 `j_bat` — 식 (8) 규약으로 방전 중 음수) 푼 계산과만 맞고, 물리 방향(방전 중 Li 산화 — 수송 경계 (18.3) · 본문 p. 10 "Li⁺ ions are inserted into the electrolyte at 0")과는 맞지 않는다 — 서로 독립인 서명 셋이 정량으로 그렇다.** `[재현]` 표 3 값 그대로 식 (23)–(25) 를 다시 풀면 1C: Nernst −3.82 · Galvanic −70.02 · 합 **−73.84 mV** ↔ 그림 6c `[도표·화소]` −3.3 · −69.8 · **−73.4** / 4C: −15.92 · −280.81 · **−296.73** ↔ 6f −13.7 · −280.7 · **−295.1** · 계면 농도 42.07 · 36.15(1C) · 50.66 · 26.97 kmol m⁻³(4C) ↔ 그림 6a · d 의 두 끝 · `k_r` 만 ×0.1 이면 1C 합 −87.2 mV · 4C 에서 양극 쪽 고갈(풀이 실패) — **인쇄 `k_r` 8.00×10⁻⁷ 이 자기 그림을 닫는다**. 벌크 σ = 1.110×10⁻⁶ S cm⁻¹ → L/σ = **326.2 Ω cm²** ↔ 그림 11b Z_mt^LiPON 호 끝 ≈327 · R_ct^n = RT/(F i₀ⁿ) **43.9** ↔ 11c 자홍 호 축 교차 ≈44.0 · R_ct^p 67.1(x 0.80) ↔ 청록 호 ≈67.3 · 합 18.3 + 326.2 + 43.9 + 67.3 = **455.7** ↔ Z_bat 극소 ≈457(측정 ≈446–450). 양극 BV(인쇄 식 (8) — 표면 농도비 포함) 방전 중간 −15.5 · −63.1 mV ↔ 그림 9e 청록(4C) −61.1 ✅(1C 는 선 겹침으로 ≈−17). ★ **음극**: ① 4C 방전 중간 그림 9e 자홍 **−23.9 mV**(`[도표·화소]` ±1 mV — 선이 안 겹친 띠) ↔ 물리 방향(인쇄 식 (10) 을 방전 중 산화로) η_ct^n +36.8(기여로 그리면 −36.8) · 농도비 없이 34.0 · 글자 그대로(같은 `j_bat` — 환원으로 계산) **−23.8** ✅ — 1C 는 노랑 · 자홍 · 청록 선이 겹쳐(−8 … −10 mV) 물리 10.6 ↔ 글자 6.9 를 가르지 못한다. ② 4C 이완 삽도(그림 9f): 자홍이 차단 순간 ≈−24 → **≈+5 mV(0 위 · ±1.3)** 로 부호가 바뀌고 ≈0.15 분(≈τ_r 8.5 s)에 0 — 글자 그대로 방향의 영전류 값 +(RT/F) ln(c(0)/c̄) = +6.2–6.5 mV 와 같은 부호 · 크기 ↔ 물리 방향을 기여(−η)로 그리면 −6.5(0 아래)이고 그대로 그리면 방전 중이 양수다 — **두 그림 방식 어느 것도 물리 방향으로는 (방전 음수 · 이완 양수) 쌍을 못 만든다**. ③ 그림 11c 자홍 유도성 고리: `[재현·대수]` 소신호 Gerischer(반응층 λ 47 nm · τ_r 8.46 s — 입력 전부 표 3)로 글자 그대로 방향은 축 아래 최저 (38.1, −3.2) · 10 mHz 끝 (35.6, −2.1) ↔ 그림 최저 ≈(38.3, −3.4) · 끝 Z_re ≈35.6 ✅ ↔ 물리 방향이면 고리가 축 **위**(용량성)로 (52.3, +2.1) 에서 끝난다. ⇒ 본문이 물리로 읽은 "an uncommon (inductive) semicircle in the low frequency range for the negative electrode" 는 **인쇄 식 묶음의 반응 방향 문제와 같은 서명**이다(`[재현·대수]` — 코드 미공개라 구현 확정은 못 함 · D1). 그리고 측정 스펙트럼에서 음극 호는 LiPON · 기하 축전기 호와 겹친다(`[재현]` τ_n = 0.76 µs ↔ τ_LiPON = R_bulk·c_geo 1.06 µs · 비 0.72) — **적합이 이 차이를 볼 수단이 없었다**. 성능 결론에 주는 크기는 작다(4C η_bat −440 mV 중 음극 계면 몫 차 ≈13 mV).
3. ★★★★ **(c) 맞춘 것 ↔ 예측한 것 — 지면의 측정 대조는 전부 같은 한 벌 적합의 자료이고, "validated" 는 표본 안 일치다.** `[인쇄]` "The model parameter values have been optimized such that both DC and AC model simulations are in a good agreement with measurements"(결론) · "Since both DC and AC impedance measurements are used for model validation, it is to be expected that the model parameters can be determined much more accurately"(p. 2) · "when only the DC simulations are used for parameter optimization, the impedance simulations do not agree with the impedance measurements. It is therefore important that both the AC and DC behavior are simulated"(p. 15) · 초록 "Both galvanostatic discharge and impedance simulations have been experimentally validated". 보류 자료 0 · 이완 곡선이 목적 함수에 들어갔는지 미인쇄(G9) · 목적 함수 · 가중 · 알고리즘 · 잔차 · 불확실성 0. `[도표·벡터]` 그림 3 몸통(측정 끝 용량의 5–80 %) 잔차 RMS **1.2 · 1.8 · 2.0 · 5.1 · 19.1 · 47.6 mV**(0.1 · 0.5 · 1 · 2 · 4 · 6C — 0.2C 는 표지가 선 경로에 합쳐져 제외) — 4C · 6C 는 **첫 1–2 분에 측정이 모의보다 45–103 mV 낮고**(10–80 % 창이면 5.1 · 25.0 mV) · 끝 용량 모의/측정 0.996 · 1.005 · 0.998 · 0.989 · **0.972 · 0.972** · `[도표·화소]` 이완(그림 4a) 0.2C 측정 − 모의 **≈+22 → ≈+12 → ≈+9 → +2.5–6 mV**(0.07 → 0.13–0.19 → 0.24–0.30 → 0.35–1 h · 한 방향) · EIS 호 꼭대기 측정 ≈157 ↔ 모의 ≈171 Ω cm²(+9 % · 측정은 더 눌린 호 · 본문 "reasonable agreement"). **같은 매개변수 한 벌이라는 것은 맞다 — 그것은 결합 적합이지 교차 검증이 아니다.** 예측(모의만)은 그림 10 의 D 를 바꾼 두 경우뿐이고, 그중 D_Li⊕ > D_e⁻ 판(그림 10e 삽도)은 ≈0.246 mAh cm⁻² · ≈3.74 V 에서 컷오프 없이 끊긴다(D9).
4. ★★★ **(b) 이중층 — 조상은 '단위 기하 면적당' 축전기다: `c_dl` 은 F cm⁻²(표 2 "Double layer capacity per unit area of electrode i" F m⁻²) · 모든 전류는 전류 밀도(= 전류 ÷ 직접 측정한 기하 면적 3.36 cm²) · 실제 계면 ↔ 기하 면적 구분 0.** 그래서 숨은 면적 인자(거칠기 · 부분 접촉) 하나가 `k`(→ i₀)와 `c_dl` 에 같은 배수로 곱해지고 **R_ct·C_dl 은 면적 불변**이다(`[재현·대수]`) — 16호 처방 전제("C ∝ 면적 · R·C 면적 불변")를 **형식상 만족하되 시험할 수 없는**(면적 하나 · 열화 0) 꼴. 값의 출처는 **DC + AC 동시 적합**(무각주) · `[인쇄]` "both the electrical double layers and the geometric capacitance are modelled as electric capacitors in order to reduce the model complexity" — 공간전하 물리가 아니다. `[재현·가정]` `c^n_dl` = `c_geo` ×5.4 · 등가 유전체 두께 0.67–2.2 µm(ε_r 를 `c_geo` 에서 13.2–42.8 로 역산) — 공간전하층 값으로 읽을 수 없다 · `c^p_dl` 등가 22–72 nm. "space-charge layers … do not have a large influence on the static (DC) discharge curves" 의 근거는 **주파수 대역 논증**(c_dl 을 흔든 그림 0)과 남의 결론 둘([26, 42])이다 — 37호 G12(같은 결론 · 근거 그림 0)의 조상도 같다. **37호의 `c_dl`(F · 전극 전체)과 `A_eff` 를 패러데이 항에만 둔 꼴은 조상에 없는 변형**이고, 37호 값(기하 면적당 6.49 · 0.166 µF cm⁻²)은 이 편 값(0.530 · 0.0174)의 ×12.2 · ×9.5 — **수치 상속 0**(37호 digest 전사 대조) · 91호가 물은 "37호 `c^p_dl` 5.1×10⁻⁶ ↔ 91호 `k₁ˢ` 5.1×10⁻⁶" 의 5.1 은 이 편 표 어디에도 없다.
5. ★★★ **(a) C-rate · 용량 기준 — 1C = 0.7 mA(공칭) 인데 같은 지면의 EMF 용량은 1.172 mAh(×1.67)다; 26호 "1C" 가 Q_ideal 기준이면 데이터 1C 의 ×1.76 이다.** `[인쇄]` "Commercial all-solid-state thin-film batteries with a capacity of 0.7 mAh" · "CC-charging was performed at 1 C-rate (0.7 mA)". `[도표·벡터]` 그림 3 EMF 끝 **0.3489–0.3493 mAh cm⁻²** × 3.36 cm² = **1.172–1.174 mAh** · 0.1C 측정 마지막 표지 0.3244(3.149 V) → ≥1.09 mAh. `[재현]` 1C 방전 시간 0.2468 ÷ 0.2083 mA cm⁻² = **71.1 분** ↔ 그림 6c · 7b 끝 ≈71.6 · ≈71 분 `[도표·화소]` · 4C **13.0 분** ↔ ≈13.1 · ≈13 분 ✅ — 실험 C-rate 의 기준은 공칭 0.7 mAh 다(26호 G2 의 전제 "실험 1C = 0.7 mA" 가 데이터 쪽에서 선다). 26호 `Q_ideal` 1.23 mAh(26호 digest §3-3 `[재현]`)는 이 편 EMF 용량 × 1.05(a^max ×1.05)와 같다 ⇒ 26호가 C-rate 를 `Q_ideal` 기준으로 전류로 바꿨다면 적합 전류는 데이터의 **≈1.76 배**다(26호 G2 · D4 — 26호 구현은 26호 지면으로 미확정).
6. ★★★ **(d) 계보 2011 → (2019) → 2020 — 바뀐 물리 일곱 · 같은 값 0 · 이 편에서 인쇄 표의 폐합과 단위 관례가 회복되고, 용량 스케일 · 평형 곡선의 '같은 데이터 유도' 관행은 그대로다.** 91호 → 이 편: 양극 단일 Fick → **이온 · 전자 쌍극 + 공통 β(x)**(사이에 Kazemi 2019 [18] — "extended with an ionic concentration-dependent diffusion coefficient") · 음극 계면 무시 → **BV + 이중층** · 양극 α 적합 0.6 → **0.5 고정 + 이중층** · **기하 축전기 · 직렬 ρ_s 신설** · n⁻ = "nBO 에 묶인 음전하"(91호) → **"uncompensated negative charge associated with a vacancy"**(그림 2b 'Vacancy') · 자료 여섯 율 → **일곱 율 + 이완 + EIS** · 셀 자체 제작 10 µAh → **상용 0.7 mAh**. 값: `k_r` 0.90×10⁻⁸(인쇄 · 그림은 ×100) → **8.00×10⁻⁷(인쇄 = 그림 폐합)** · `δ` 0.18 → 0.64 · `a₀` NDP 6.01×10⁴ → `c₀` 61141(무각주) · `k₁ˢ` 단위 α 0.6 판(i₀ 재현 불가) → **α 0.5 판 · 식 (9) 와 차원 폐합**(i₀ 0.470 mA cm⁻² @x 0.51) · t₊ 0.15 → 0.233. "전해질 지배" 결론의 성격이 바뀌었다: 91호는 이원 가정 몫 ≈71 %(91호 digest 전사) ↔ 이 편은 `[재현·가정]` 같은 σ 의 단일 이온이어도 1C 68.0 mV(= 326.2 Ω cm² × j) — **이원 가정 몫 ≈8 %**, 나머지는 EIS 호 지름이 닻을 내린 벌크 옴이다.
7. ★★ **(e) Q4 0/98 — 아흔 번째 성질.** 식별성 어휘: `identif*` 4(그중 식별성 뜻 하나 — "Since ρPt and ρLi cannot be separately identified, they are replaced by ρs" — 직렬 합의 올바른 구조적 묶음) · `uniqu*` · `uncertain*` · `confiden*` · `±` · `error*` · `residu*` · `RMS` · `correlat*` · `Fisher` · `Hessian` **본문 0** · `sensitiv*` 1("a small sensitivity study" — 그림 10 의 D 바꾸기) · 본문(초록 · 캡션 · 표 포함) `optimi*` 16 · `validat*` 5 · `agree*` **13** · `accura*` 5. "DC 만으로 맞추면 AC 가 안 맞는다" 는 **비유일성 증상의 문장**이고(그림 · 값 0), 처방은 "much more accurate parameter estimation since more measurement information has been made available" 의 선언이다(측정 0). **아흔 번째 성질 = "DC 단독 적합이 AC 를 못 맞춘다는 비유일성의 증상을 한 문장으로 인쇄하고(그림 · 값 0), 처방을 'DC + AC 한 벌 동시 적합 = 더 정확한 추정' 으로 선언한 뒤 같은 자료를 'validated' 라 불렀다 — 그 한 벌(무각주 13 행 + 함수형 미인쇄 β(x) · 같은 율 묶음 외삽 EMF)이 하류에서 '문헌값' 이 됐고, 측정 스펙트럼에서 LiPON 호와 겹치는 음극 계면 항은 반응 방향까지 자료가 보지 못했다."**
8. **채움표** — Q1 해당 없음(`θ(N)` 0/98 · 층 하나: 숨은 면적 인자가 k · c_dl 에 같이 곱해지는 자리) · Q2 없다(층 하나: DC + AC 를 한 벌에 같이 쓴 "관측 추가" 의 ASSB 원형 — 모드 분리 아님 · 성분 분해는 모형 배정) · Q3 층 하나("각주 넷 표 — 무각주 13 = 같은 셀 DC + AC 동시 적합 · β(x) 함수형 미인쇄 · 하류 '문헌값' · 재풀이 폐합 ✅ 전해질 · 양극 / 음극은 인쇄 식 묶음 그대로의 반대 방향") · **Q4 0/98 — 아흔 번째 성질** · Q5 해당 없음(층 하나: 음극 계면 항이 모형에 들어왔으나 측정에서 LiPON 호와 겹쳐 배정이 모형뿐 · 방향 문제) · Q6 해당 없음(`pressure` 0) · Q7 해당 없음 + 공백(Li 두께 N · 재고 미인쇄) · Q8 층 하나(상용 LCO 박막 · EMF = 일곱 율 외삽 · 끝 기울기 ≈−72 V/단위 x 가 방전 끝 η_d 를 정함). **누적 ≈20.0 → ≈20.0 (새 칸 0).**

---

# 서지

| 항목 | 값 (`[인쇄]` — p. 1 · p. 16 · p. 18–19 · XMP) |
|---|---|
| 제목 | **"An advanced all-solid-state Li-ion battery model"**(지면 · 정보 사전 · XMP 같음) |
| 저자 · 소속 | **L.H.J. Raijmakers**ᵃ · **D.L. Danilov**ᵃ,ᵇ · **R.-A. Eichel**ᵃ,ᶜ · **P.H.L. Notten**ᵃ,ᵇ,ᵈ,\* — ᵃ Forschungszentrum Jülich (IEK-9), D-52425 Jülich · ᵇ Eindhoven University of Technology · ᶜ RWTH Aachen University · ᵈ University of Technology Sydney · 교신 Notten(메일 인쇄 — 옮기지 않음) |
| 저널 | *Electrochimica Acta* **330** (2020) **135147** · doi `10.1016/j.electacta.2019.135147` · ISSN 0013-4686 · XMP `prism:coverDate` 2020-01-10 |
| 일정 | Received **22 June 2019** · revised **23 August 2019** · Accepted **24 October 2019** · online **31 October 2019** · `[재현]` 접수 → 수락 124 일 |
| 저작권 | "© 2019 Elsevier Ltd. All rights reserved." · CC · OA 표기 0 ⇒ **구독본으로 다룬다** — 이 digest 는 인용 · 요약 · 재현 계산만 담고 그림 크롭은 위키 관례대로 `raw/figures/`(변형 없는 잘라내기) |
| 키워드 | All-solid-state batteries · Modelling · Impedance · Mixed ionic/electronic diffusion · Electrical double layers |
| 자금 · 감사 | Horizon 2020 **DEMOBASE** project (Grant No. 769900) · Dongjiang Li · Chunguang Chen · Lei Zhou(FZ Jülich) "for the helpful discussions" · 이해 상충 진술 0 |
| 코드 · 자료 | **공개 진술 0**(원자료 · 데이터 가용성 · 저장소 0) · 구현 "Matlab"(2 회 — 부록 A 는 양극 확산의 유한차분만) |
| 분량 | 19 쪽 · 그림 **11**(래스터 6 = 그림 4 · 6 · 7 · 9 · 10 · 11 / 벡터 5 = 그림 1 · 2 · 3 · 5 · 8) · 표 **3**(약어 · 기호 · 매개변수) · 번호 식 **(1)–(32)**(가지 번호 18.1–18.4 · 19.1–19.4 · 23.1–23.4 · 28.1–28.4 · 29.1–29.4 · 30.1–30.4 포함) + 부록 **(A.1.1)–(A.14)** · 참고문헌 **[1]–[42]**(번호 빠짐 0 — p. 18–19 목록에서 직접 셈) |
| 절 | 1. Introduction · 2. Theoretical considerations(2.1 Electrochemical description · 2.2 Charge transfer kinetics and electrical double layers · 2.3 Diffusion and migration in the electrolyte · 2.4 Diffusion and migration in the LiCoO2 electrode) · 3. Experimental · 4. Results and discussion(4.1 Total battery · 4.2 Electrolyte · 4.3 Positive electrode · 4.4 Overpotential contributions · 4.5 Influence of diffusion coefficients · 4.6 Impedance simulations) · 5. Conclusions · Acknowledgements · Appendix A · References |
| 셀 | **상용** 박막 전고체("Commercial all-solid-state thin-film batteries with a capacity of 0.7 mAh" — 제조사 · 모델명 · 셀 수 미인쇄) · Pt 기판 위 LiCoO₂ **8.08 µm** · LiPON **3.62 µm** · Li 금속 · 면적 **3.36 cm²** |
| 시험 | Maccor 2300 · 활성화 다섯 사이클 · CCCV 1C(0.7 mA) → 4.2 V · CV 컷 0.1C(0.07 mA) · 방전 **0.1 · 0.2 · 0.5 · 1.0 · 2.0 · 4.0 · 6.0C** · 컷오프 3.0 V · 충 · 방전 뒤 이완 **2 h** · EIS: Autolab PGSTAT302N · **정전위 3.9 V** · **50 점 로그 10 mHz–800 kHz** · 가진 **10 mV** · 전부 **20 °C**(모의 293 K) |
| 모형 | 1D(Li \| LiPON \| LCO \| Pt) · 양극 BV(식 8–9 · α 0.5) · 음극 BV(식 10–11 · α 0.5) · 두 계면 이중층 축전기(식 12–13 · 15–16) · 셀 기하 축전기(식 14 — `U*_bat` 에 걸림) · 전해질 해리 이원(Li⁺ + n⁻ · 식 17–25) · 양극 이온 · 전자 쌍극 Nernst–Planck + 공통 β(식 26–32) · 직렬 ρ_s · 열화 0 · 온도 고정 · `[인쇄]` "not an equivalent circuit model" |

**PDF 메타데이터 (이 실행에서 직접 읽음 · pymupdf)** — 3,754,525 B · sha256 `e21931c869c01649cef0468021d5b55ac2365cfa429c2e9b42cda3a3e1b93018`(호출자 명시값 ✅ — 직접 재계산) · 헤더 `%PDF-1.7` · 19 쪽 전부 595.3 × 793.7 pt · 암호 0 · 정보 사전: title **"An advanced all-solid-state Li-ion battery model"** · author **"L.H.J. Raijmakers"** · subject **"Electrochimica Acta, 330 (2020) 135147. doi:10.1016/j.electacta.2019.135147"** · keywords "" · creator **"Elsevier"** · producer **"Acrobat Distiller 8.1.0 (Windows)"** · 생성 **D:20191205221006+05'30'** · 수정 **D:20191205221059+05'30'**(호출자 메모와 같음 ✅ — 생성 53 초 뒤 · 온라인 2019-10-31 보다 한 달 뒤 = 권 · 쪽 확정판으로 읽힘 · 판정 안 함) · XMP **7,068 B**(`dc:creator` 넷 · `dc:subject` 키워드 다섯 · `dc:publisher` Elsevier Ltd · `prism:volume` 330 · `pageRange` = `startingPage` 135147 · `coverDisplayDate` 10 January 2020 · `prism:copyright` "© 2019 Elsevier Ltd. All rights reserved." · crossmark `MajorVersionDate` **2010-04-23**(이 편 일정과 무관한 날짜 — Elsevier 틀 값으로 읽힘) · `CrossmarkDomainExclusive` true · `jav:journal_article_version` VoR · `pdfx:robots` noindex · `xapRights:Marked` True · `xap:CreateDate` 2019-12-05T22:10:06+05:30 · `ModifyDate` = `MetadataDate` 22:10:59 · `xapMM:DocumentID` uuid:132d6e51-2b23-4839-bf7b-ebf0ba38a727 · `InstanceID` uuid:d82616ae-e69f-4013-95b0-e3bf542d8a2f) · 카탈로그 `/StructTreeRoot`(태그 PDF) · `/Threads` · `/Outlines` · `/PageMode /UseOutlines` · `/PageLayout /SinglePage` · **PageLabels 십진 1 부터**(= 인쇄 쪽) · `%%EOF` 1 · 래스터: p. 1 셋(CrossMark 단추 120×119 · Elsevier 로고 254×278 · 저널 표지 237×299 — 그림 아님) + **그림 4 · 6 · 7 · 9 · 10 · 11**(1777×1938 · 1777×1992 · 1777×2667 · 1954×2205 · 2131×1094 · 1033×2186) · 벡터 그림 다섯(그림 1 · 2 · 3 · 5 · 8 — 경로 · 글리프).

⚠ **텍스트 층**: 합자 **154**(NFKC 로 복원 — NFKC 전에는 `fit*` · `identif*` · "thin film" 이 0 으로 나온다) · 빼기 부호가 U+0001 · 빈칸으로 빠진다("8.00 , 10\x017" = 8.00 · 10⁻⁷ — 표 3 지수 부호는 쪽 렌더로 확인) · 그리스 문자 대체(ρ → "r" · η → "h" · β → "b" · δ → "d" · α → "a") · ⊕ 가 "4" 로("Li4" = Li⊕) · µ 가 "m" 으로("3.62 mm" = 3.62 µm · 렌더 확인) · "þ" = "+" · "¼" = "=" · 범위 대시가 "e" 로("[1e3]" = [1–3] · "(aec)" = (a–c)) · 줄 끝 하이픈은 Elsevier 분철(복원할 때 진짜 하이픈 낱말은 문맥을 찍어 손으로 셌다). 식 (5) · (8)–(16) · (18.2)–(18.4) · (23.1)–(25) · (27)–(30.4) · 표 3 은 **쪽 렌더 조각으로 읽었다**(150–300 dpi · 판독용 · 커밋 안 함).

---

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **최적화의 정체** — 목적 함수(DC · AC 의 가중 · 이완 구간 포함 여부 · 율별 가중) · 알고리즘 · 시작점 · 경계 · 반복 · 잔차 · 불확실성 · 다중 시작 **전부 0**. 지면의 말은 "optimized simulated (lines)" · "The optimized model parameters are listed in Table 3" · "The model parameter values have been optimized such that both DC and AC model simulations are in a good agreement" 셋 | 무각주 13 행이 수렴점인지 · 손으로 맞춘 점인지 가를 수 없다 — 26호가 이 값들을 "문헌값" 으로 쓰면서 "not fed into the optimization algorithm" 이라 적은 근거도 여기서 확인되지 않는다 |
| **G2** | **β(x) 의 함수형 · 자유도** — 그림 5 의 곡선 둘("Optimized diffusion coefficients")뿐 · 식 · 표 · 매개변수 수 0 · D⁰ 의 정규화 기준 미인쇄(`[도표·벡터]` β = D/D⁰ 최대 0.65 · 최소 0.025 — 작동 창 어디에서도 1 이 아니다) | 자유 매개변수 수가 표 3 의 13 보다 많다(β 의 자유도만큼) · 26호 G5("β … extracted from the same paper")가 이 편에서도 그림으로만 닫힌다 — 26호가 무엇을 디지털화했는지 미상 |
| **G3** | **EMF 외삽의 정체** — "On the basis of this set the EMF voltage curve was determined by mathematical extrapolation, of which the details can be found in previous publications [32,33]" — 쓴 율 · 점 수 · 함수형 · 버린 율 · 불확실성 0 · EMF 표 · 식 0(그림 3 · 8 뿐) · [32,33] 은 C6/LiFePO₄ 노화 편 둘 | 모형의 몸통(U^p)이고 `c_max` 의 출처(각주 d)이며 방전 끝 η_d 를 정하는 가파른 끝(`[도표·벡터]` 기울기 ≈−72 V/단위 x)이 외삽 영역이다 — 91호와 같은 '같은 데이터 외삽 → 평형 곡선 → 과전압 기준선' 되먹임 |
| **G4** | **EIS 모의 상태 · 신호** — 측정은 "Potentiostatic … at a voltage of 3.9 V" · 모의는 "an AC current has been applied with a zero DC bias" — 모의의 x · 전류 진폭 · 주기 수 · 푸리에 창 · 측정 전 휴지 미인쇄 | `[도표·벡터]` EMF 3.900 V = x 0.864 ↔ `[재현]` 그림 11c R_ct^p ≈67.3 Ω cm² 는 x ≈0.80(EMF 3.910 V) — 평탄 구간이라 "3.9 V" 가 x 를 0.80–0.87 로만 정하고, R_ct^p(x) 는 그 안에서 67 → 78 Ω cm² 움직인다(D8) |
| **G5** | **셀 정체 · 수 · 반복** — 제조사 · 모델 · 로트 · 측정 셀 수 · 셀 간 산포 0("batteries" 복수형만) | 매개변수 한 벌이 셀 하나의 것인지 · 셀 간 평균인지 모른다 · 26호 "남의 데이터" 의 셀 수도 같이 모른다 |
| **G6** | **두께 · 면적의 측정 근거** — 각주 b "Measured with Scanning Electron Microscope"(L · M) · 각주 a "Identified by direct measurements"(T · A) — SEM 그림 · 방법 · 오차 0 | 상용 셀의 SEM 은 파괴 측정인데 같은 셀인지 · 같은 로트의 다른 셀인지 미상 · M 은 c_max(각주 d)의 분모 |
| **G7** | **Li 두께 N · Pt 두께 K · Li 재고** — 표 2 에 기호만 · 값 0 · `c_Li` 7.64×10⁴ "Predefined" | Q7(재고) 칸의 바탕 · 음극은 무한 원천으로 다뤄진다 |
| **G8** | **수치 구현** — 격자 n · Δt(부록 A 는 명시적 전진 차분 — 안정 조건 미인쇄) · LiPON PDE(식 23) 해법 · 계면 ODE(식 15 · 16) 결합 방식 · 시간 → 주파수 변환 · **두 계면 전류의 부호 처리**(식 12 · 16) | 그림 6b · e 의 계면 전기장 봉우리(`[재현]` 1C 37.5 · 43.6 kV m⁻¹ · 경계층 두께 47 nm)가 그림에서 ≈28 kV m⁻¹ 로 보이는 것이 격자 해상도인지 못 가른다 · D1 의 확정이 여기 걸린다 |
| **G9** | **이완 곡선이 적합 자료였는지** — 그림 4 "Measured … and simulated … discharge and relaxation curves" 만 | 이완이 표본 밖 예측인지 · 안 일치인지 못 가른다(그림 4a 0.2C 의 한 방향 잔차 ≈+22 → +2.5–6 mV) |
| **G10** | **`c₀` 61141 의 출처** — 무각주(= optimized) 인데 다섯 자리 · 91호 NDP 측정 6.01×10⁴ 와 1.7 % · LiPON 조성 · 밀도 미인쇄 | 다른 전해질(Li₃PO₄ ↔ LiPON)의 측정값에서 출발해 적합이 조금 움직였는지 · 독립 적합인지 모른다(`[해석]`) |
| **G11** | **부호 규약** — 식 (12) · (15) · (16) 두 계면에 같은 `j_bat − j_geo` · (8) · (10) 둘 다 산화 양 · (18.3) J(0) = −j^n_ct/F ↔ (18.4) J(L) = +j^p_ct/F · (5)(6) "− η^LiPON_mt − η^n_ct" ↔ 그림 9 의 모든 과전압이 더해 쌓임 · (28.3) · (29.4) ↔ (30.3) · (30.4) 의 `j` 부호 반대 | 그림 9 · 11c 의 음극 계면 거동이 어느 규약의 산물인지(D1) — 코드 없이 확정 못 함 |
| **G12** | **이중층 결론의 근거** — "space-charge layers in this particular ASSB do not have a large influence on the static (DC) discharge curves" 의 근거가 "The high-to middle-frequency range is the range where the double layer capacitors play a role" 와 남의 결론([26, 42]) 뿐 · c_dl 을 흔든 그림 · 표 0 · 축전기 값의 물리 범위 대조 0 | 37호 G12 와 같은 결손을 조상이 먼저 가졌다 — "작은 영향" 은 시험된 결론이 아니라 τ 논증 |

---

# 보충 자료 — 받은 것 · 대조

**SI 없음 (원문에 보충 언급 0).** 호출자 대조와 같은 결과를 이 실행에서 직접 다시 셌다 — 본문 · 캡션 · 표 · 참고문헌 전문(NFKC · 줄 끝 분철 복원 뒤)에서 `supplement*` · `supporting information` · `data availab*` · `video` · `movie` · `zenodo` · `github` · `code` **0 회** · `appendix` 3 회(전부 본문 안 부록 A — "In Appendix A the finite difference approximation …" · 절 머리 · "In this Appendix …") · `Matlab` 2 회(구현 언어만). 부록 A(p. 16–18 · 식 A.1.1–A.14 — 양극 평판 확산의 유한차분)는 본문 안이다. 원자료 예치 0 · 코드 0 ⇒ 이 digest 의 재현은 **인쇄 수치 + 벡터 경로 + 래스터 화소** 세 층뿐이다.

---

# 그림 · 표 — 자동 13 항목 + 수동 4, 실제로 연 것 **17/17**

크로퍼(`wiki/tools/extract_figures.py`)가 본문 그림 1 · 3–11 을 `fig_1` · `fig_3 … fig_11` 로, 표 1–3 을 `tab_1 … tab_3` 로 잡았다(SI 판별 ✅ — 파일명 `58._An_advanced_all-solid-state_Li-ion_battery_model` 의 `SI_TAG` False · 실행 뒤 이름을 눈으로 확인 · `fig_S…` 0). **그림 2(p. 6 LiPON 망 도식)는 자동에서 빠졌다**(글자 · 선으로 된 벡터 도식 — 크로퍼가 영역을 못 잡음). 수동 크롭 4(300 dpi · `*_manual_p*.png`): **그림 2 · 표 1 · 표 2 · 표 3 단독**. 자동 크롭 점검(`figures.json` `note` 에 적음 — 자동 파일은 지우지 않았다):

- **누락 하나** — 그림 2 → 수동.
- **과대 셋** — `tab_1`(p. 2 쪽 전체 — 본문 두 단 + 그림 1 + 표 1) · `tab_2`(p. 3 쪽 전체 — 쪽 머리 포함 · 표 2 가 쪽 대부분) · `tab_3`(p. 8 쪽 전체 — 본문 · 식 (27)–(30.4) · 그림 3 · 표 3) → 표만 수동 셋.
- **캡션 필드 오염 · 잘림** — `tab_1`(표 1 글자 전부가 캡션에 섞임) · `tab_2`(표 2 글자가 섞이고 900 자에서 잘림) · 그림 캡션 열에 텍스트 층의 대체 문자("Li4" = Li⊕ · "Liþ" = Li⁺ · "\x01" = − · "¼" = "=" · "(aec)" = (a–c) · "(hp d)" = (η^p_d)) · 그림 3 "func- tion" 분철 — 캡션 원문은 PDF 가 정본.
- 나머지(`fig_1` · `fig_3`–`fig_11`) 라벨 · 내용 온전 · 잘림 0 · 과대 0(그림 4 · 6 · 7 · 9 · 10 · 11 은 래스터 그 자체).

**17 장 전부 이 실행(2026-10-03 재개)에서 직접 열었다 — 안 본 그림 · 표 0.** (p. 1 래스터 셋은 로고 · 표지 · CrossMark 라 그림이 아니다.) 앞 에이전트의 "봤다" 기록은 근거로 쓰지 않았다. 판독: 그림 3 · 5 · 8 은 **벡터 경로 좌표**(축 상자 · 눈금 글자 중심으로 보정 — 그림 3 은 축 상자 보정과 눈금 글자 보정이 ≤0.0004 mAh cm⁻² · ≈3 mV 차라 판독 폭을 ±3 mV 로 적는다), 그림 4 · 6 · 7 · 9 · 10 · 11 은 **화소 좌표**(축 상자 · 눈금 글자로 보정 · 선은 색 마스크 띠의 가운데 · 표지는 고리 중심 — 선에 잘린 고리 조각은 합쳐서)다. 판독 · 재현 코드 · 확대 조각은 `scratchpad` 에만(커밋 안 함).

## Fig. 1 — 셀 도식 (p. 2 · 봤다 · 벡터) ★★★ (b)

Position 축 −N · 0 · L · L+M · L+M+K · y(왼 → 오른) · Name: Li | LiPON | LCO | Pt · (n) · (p) · Process: e⁻ ← (Li) · Li⁺ → (LiPON) · Li⊕ → · e⁻ ← (LCO) · e⁻ ← (Pt) · 계면 둘(점선 겹줄)에 노란 굽은 화살(전하이동) · `j^n_ct` · `j^p_ct` · **이중층 축전기 둘(`c^n_dl` · `c^p_dl`)이 각 계면을 가로질러** · **`c_geo` 가 Li 전극 쪽에서 Pt 집전체까지(LiPON + LCO 전체)를 가로질러** · 외부 회로 U_bat(e⁻ → 외부로). ⇒ `[인쇄]` 본문과 같다 — `c_geo` 의 유전체는 LiPON 과 LCO 둘이다("the LiPON and LCO can be considered as a dielectric between two electronic conductors"). 도식에 직렬 ρ_s · 면적 표시 0.

## Fig. 2 — LiPON 망 · 이온화 (p. 6 · 봤다 · 수동 크롭 · 벡터) ★★ (d)

(a) 인산 사슬(P–O) · 교차 질소(N, 초록 — 3 배위 · 2 배위) · 활성 종 Li_o(빨강) · (b) 같은 망에 "Li⁺ goes to interstitial"(빨강 점선 화살 · 남은 자리 'V' 보라 원 "Vacancy") · 오른쪽 위 "Li⁺ hopping to vacancy"(빨강 곡선 화살)와 반대 방향 **n⁻**(하늘색 곡선 화살) · 범례 Active species · **"Chairs of Phosphates"**(인쇄 그대로 — 본문 0 회 · Chains 의 오기로 읽힘 · D14) · Cross-linking nitrogen · Vacancy · **Uncompensated negative charge**. ⇒ **n⁻ = 공공의 미보상 음전하**(본문 "n⁻ is a notation for the uncompensated negative charge associated with a vacancy formed in the LiPON matrix at the place where lithium was originally located") — 91호 D15(n⁻ = "nBO 에 묶인 미보상 음전하" · `vacanc*` 0 회)의 이름 문제에 이 편이 공공 해석을 인쇄했다(91호 digest 전사 대조). 축 · 수치 0(도식).

## Fig. 3 — 일곱 율 방전 + EMF (p. 8 · 봤다 · 벡터 판독) ★★★★ (c) · (a)

`[도표·벡터]`(판독 폭 ±0.001 mAh cm⁻² · ±3 mV) — EMF(검정) ≈4.19 V → 3.000 V @**0.3489–0.3493 mAh cm⁻²** · 모의 선 시작(Q = 0) ≈4.18 · 4.17 · 4.14 · 4.10 · 4.01 · 3.83 · 3.65 V(0.1 → 6C) · 모의 3.0 V 도달 **0.3231 · 0.3068 · 0.2759 · 0.2468 · 0.2156 · 0.1805 · 0.1555** · 측정 마지막 표지 0.3244 @3.149 V(0.1C) · (0.2C 표지는 선 경로에 합쳐져 따로 못 셈) · 0.2746 @3.101 · 0.2473 @3.005 · 0.2180 @3.020 · **0.1858 @3.013 · 0.1600 @3.025** · 몸통(측정 끝 용량의 5–80 %) 잔차 RMS **1.2 · 1.8 · 2.0 · 5.1 · 19.1 · 47.6 mV**(0.1 · 0.5 · 1 · 2 · 4 · 6C) · 10–80 % 창이면 4C 5.1 · 6C 25.0 mV · 첫 표지(Q = 0) 측정 − 모의 −1.7 · −4.7 · −7.3 · −13.3 · −26.9 · −63.6 mV · 4C Q 0.0024 · 0.0118 에서 −59.0 · −45.4 mV(≤0.85 분) · 6C Q 0.0019–0.0257 에서 −103.0 · −102.4 · −50.2 mV(≤1.2 분). ⇒ 본문 "the agreement between the measurements and simulations is good across the wide range of investigated C-rates" — 2C 이하 몸통 ≤5 mV 는 맞고, **4C · 6C 의 첫 1–2 분과 끝 용량(0.97)은 단서 없이 같은 문장에 들어간다**(D11). "at a discharge rate of 6C less than half of the full discharge capacity can be extracted" ✅(0.1555 ÷ 0.3489 = 45 %).

## Fig. 4 — 방전 + 이완, 여섯 율 (p. 9 · 봤다 · 래스터 화소) ★★★ (c)

여섯 판(0.2 · 0.5 · 1 · 2 · 4 · 6C — **0.1C 판 없음**) · 각 판 왼쪽 방전(Extracted charge) · 오른쪽 이완(Time **0–1 h** — 본문 "relaxation period of 2 h" 의 앞 절반) · 측정 파랑 원 · 모의 빨강 선. `[도표·화소]`(y 80.5 px / 0.2 V = 2.48 mV/px · 빨강 선에 잘린 원 조각을 합쳐 중심 · 판독 폭 ±3 mV): 0.2C 이완 측정 − 모의 **≈+22 mV(0.07 h) → ≈+12(0.13–0.19 h) → ≈+9(0.24–0.30 h) → +2.5–6 mV(0.35–1 h)** · 끝 ≈3.86 V · 1C · 6C 는 이완 시작 몇 점 뒤 판독 폭 안(끝 ≈3.90 · ≈3.93–3.94 V). ⇒ 이완 끝 전압은 벌크 x 의 EMF 와 맞는다(`[재현]` 1C 벌크 0.867 → EMF 3.899) · **0.2C 는 측정이 모의보다 빨리 회복하고 1 h 내내 위에 있다(한 방향)** — "in good agreement … during the entire relaxation time under all conditions" 의 조건(판독 폭 안 · 밖)이 율마다 다르다(D10).

## Fig. 5 — 적합 D_Li⊕(x) · D_e⁻(x) (p. 10 · 봤다 · 벡터 판독) ★★★★ (a) · G2

`[도표·벡터]`(판독 폭 ±3 % in D): D_Li⊕ **≈7.9×10⁻¹⁴**(x 0.50–0.60) → ≈7.4×10⁻¹⁴(0.65) → ≈6.7×10⁻¹⁴(0.70) → ≈4.9×10⁻¹⁴(0.75) → ≈2.1×10⁻¹⁴(0.80) → ≈9.8×10⁻¹⁵(0.85) → ≈5.5×10⁻¹⁵(0.90) → ≈3.6×10⁻¹⁵(0.92) → **≈3.0×10⁻¹⁵**(1.00) · D_e⁻ ≈3.3×10⁻¹³ → ≈1.3×10⁻¹⁴ · **비 D_e⁻/D_Li⊕ ≈4.1–4.3**(표 3 비 5.06/1.21 = 4.18 — 식 (27) 공통 β ✅) · `[재현]` **β = D/D⁰ = 0.65(최대) → 0.025(최소)** — D⁰_Li⊕ 1.21×10⁻¹³ 은 작동 창 어느 x 의 D 도 아니다(표 2 "Diffusion scaling constants") · x 0.75 → 0.92 감소 **≈×13.5**(본문 "decrease more than one order of magnitude" ✅) · 꺾임 x ≈0.75 · ≈0.92(본문 "second hexagonal phase [34]" · "two-phase coexistence region (0.75 ≤ x ≤ 0.92)").

## Fig. 6 — LiPON 의 Li⁺ 농도 · 전기장 · 과전압 (p. 11 · 봤다 · 래스터 화소) ★★★★ (c)

(a) 1C 농도(z 36–42 kmol m⁻³ · 위치 0–4 µm · 0–100 분) — 벌크 ≈39 · y = 0 끝 ↑(≈42) · y = L 끝 ↓(≈36) · 전류 끊으면 복귀 · (b) 1C 전기장(0–40 kV m⁻¹) — 벌크 ≈18–20 · 두 끝 봉우리 · (c) 1C 과전압 `[도표·화소]`: **Total −73.4 · Nernstian −3.3 · Galvanic −69.8 mV** · 평탄 끝 **≈71.6 분** · (d)(e)(f) 4C: 농도 z 25–50(y = 0 ≈50 · y = L ≈27) · 전기장 0–200(벌크 ≈75 · L 쪽 봉우리 큼) · **Total −295.1 · Nernstian −13.7 · Galvanic −280.7 mV** · 끝 **≈13.1 분**. 범례 Total(파랑) · Nernstian(초록 점선) · Galvanic(빨강 파선) — 본문 "dominated by migration (dashed red lines), while the diffusive component (dotted green lines)" 와 같다. `[재현]` 표 3 그대로 식 (23)–(25) 재풀이(판정 2): −73.84 · −3.82 · −70.02 / −296.73 · −15.92 · −280.81 mV · 벌크 장 18.8 · 75.1 kV m⁻¹ ✅ · 계면 장(경계층 두께 47 nm) 37.5 · 43.6(1C) · 124 · 234 kV m⁻¹(4C)은 그림의 봉우리(1C ≈28 · 4C ≈95–130)보다 크다 — 3D 면 그림의 위치 격자 해상도 문제로 읽힘(판정 안 함 · G8).

## Fig. 7 — LCO 농도 · 표면 / 벌크 x · 전기장 · 과전압 (p. 12 · 봤다 · 래스터 화소) ★★★ (c)

(a)(e) 농도장(15–35 kmol m⁻³ · 위치 ≈3.6–11.7 µm) · (b)(f) `[도표·화소]` x: 시작 **0.510**(두 율) · 1C 벌크 끝 **≈0.869** · 표면 정점 **≈1.0 @≈71 분** · 이완 뒤 ≈0.868 · 4C 벌크 끝 **≈0.776** · 표면 ≈0.995 @≈13 분 · 이완 뒤 ≈0.775 · (c)(g) 전기장 봉우리(방전 끝 · ≈45 · ≈120 kV m⁻¹) · (d)(h) 과전압: 1C 확산 ≈−0.01 → 끝 **≈−0.59 V** · 전하이동 ≈−0.015 → ≈−0.2 · 물질전달 0 → ≈−0.08 / 4C 확산 ≈−0.05 → ≈−0.03 → ≈−0.28 · 전하이동 ≈−0.06 → ≈−0.07 → ≈−0.25 · 물질전달 → ≈−0.085. `[재현]` 벌크 x 기울기 j/(F·c_max·M) = 0.004979 · 0.019918 min⁻¹ ↔ 그림 ≈0.00505 · ≈0.0204(**≈+1.4 · ≈+2.6 %** — 판독 폭 ±0.003 x · D7 과 같은 방향).

## Fig. 8 — EMF vs x · 방전 끝 표면 / 벌크 (p. 13 · 봤다 · 벡터 판독) ★★★★ (c) · Q8

`[도표·벡터]`(판독 폭 ±0.001 x · ±3 mV): EMF **x 0.510 → 1.000 · ≈4.19 → 3.0 V** · EMF(0.60) ≈4.058 · (0.70) ≈3.960 · (0.80) ≈3.910 · (0.85) ≈3.903 · (0.90) ≈3.893 · (0.95) ≈3.865 · (0.99) ≈3.704 · (0.994) ≈3.641 · (0.998) ≈3.35 · **EMF 3.900 V @x 0.864** · 표지(채운 도형 중심): 벌크 1C (0.867, 3.900) · 표면 1C (**0.998**, 3.310) · 벌크 4C (0.775, 3.916) · 표면 4C (**0.994**, 3.629) → η_d^p **−0.590 · −0.287 V**(그림 7d · h 와 같다) · 끝 기울기 ≈−16(0.990–0.994) · **≈−72**(0.994–0.998) V/단위 x(가파른 끝이라 보간 민감 ±2). ⇒ 본문의 "Remarkably, the diffusion overpotential at 1C-rate … is larger at the end of discharging than at 4C-rate" 는 **표면 x 0.004 차 × 외삽 EMF 끝 기울기**로 정해진다(G3).

## Fig. 9 — 과전압 분해 · 이완 (p. 14 · 봤다 · 래스터 화소) ★★★★ (c)

(a)(d) EMF 아래 색 띠 누적(η_s · +η_mt^LiPON · +η_d^p · +η_ct^p · +η_ct^n · +η_mt^p — 범례가 전부 **더한다**) · (b)(e) 성분별 · (c)(f) 이완 성분(삽도 1 분 · 0.5 분). `[도표·화소]`(판 b · e 축 상자 +0.1 ↔ −1.0 V = 590.5 px · 1 화소 1.863 mV · 선 폭 ≈5 px): **4C**(Q ≈0.08 · 선이 서로 안 겹침) η_s **−15.5**(`[재현]` ρ_s j −15.25) · η_mt^LiPON **−294.9** · η_d^p **−40.6** · η_ct^p **−61.1** · η_ct^n **−23.9** · η_mt^p −4.3 · 합 −440.3 ↔ η_bat **−440.2** ✅ / **1C**(Q 0.08–0.12) η_mt^LiPON **−74.2** · η_bat **−112.4** · 위쪽 셋(노랑 η_mt^p · 자홍 η_ct^n · 청록 η_ct^p)은 선이 겹쳐 띠 가운데로만 ≈−1 … −3 · ≈−8 … −10 · ≈−16 … −18 mV(파랑 η_s · 빨강 η_d^p 는 가려 따로 못 읽음). ★ **이완 삽도(f, 4C)**: 자홍 η_ct^n 이 차단 순간 ≈−24 → **≈+5 mV(0 위 · ±1.3)** 로 뛰고 ≈0.15 분에 0 — 청록 η_ct^p 는 계속 음수(본문 "pre-exponential concentration fractions … unequal to 1 during relaxation"). `[재현]` η_s = ρ_s j 3.81 · 15.25 mV ✅ · η_ct^p(인쇄 식 8 · 표면 · 벌크 x 는 그림 7 판독) −15.5 · −63.1 ↔ 4C −61.1 ✅ · **η_ct^n — 판정 2 ★(D1)**. 본문 "the electrolyte overpotential (green area) has the largest contribution" ✅(1C 66 % · 4C 67 % of η_bat) · "The charge-transfer overpotential at p is larger than at n because the reaction rates are faster at n" — `[재현]` i₀ⁿ/i₀ᵖ 는 1.22(x 0.51)–1.53(x 0.80)뿐이고 그림의 n ↔ p 차의 일부는 D1 의 방향 문제다(D13).

## Fig. 10 — D 를 같게 · 뒤집어 (p. 15 · 봤다 · 래스터 · 확대 판독) ★★★ (c) · 처방

(a)(b) 적합 경우(D_Li⊕ < D_e⁻ — 그림 5 와 같음 · 삽도 1C 측정 ↔ 모의가 ≈0.248 에서 함께 3.0 V) · 농도 단면(LiPON 39 · LCO 시작 16.5 → 중간 ≈22.5–22.0 → 끝 32 @L → ≈27.2 → 27.3 @L+M) · (c)(d) D_e⁻ 를 D_Li⊕ 로 낮춤(같게): `[도표]` 삽도 모의 3.0 V 도달 **≈0.27 mAh cm⁻²**(측정 0.248 · +9 %) · LCO 끝 단면 좌우 대칭(32 · ≈28 · 32) · (e)(f) 뒤집음(D_Li⊕ > D_e⁻): 단면 거울(끝 27.3 @L · 32.2 @L+M) · ★ **삽도 모의 선이 ≈0.22 에서 꺾여 ≈0.246 mAh cm⁻² · ≈3.74 V 에서 끝난다 — 3.0 V 컷오프에 닿지 않는다**(확대 판독 · 판독 폭 ±0.003 · ±0.01 V · 본문 언급 0 · D9 — 끝 용량이 측정 1C 끝과 같은 자릿수라 시간 제한 모의로 읽히나 판정 안 함). `[재현·대수]` 식 (30.3) · (30.4) 경계 기울기 비 D_e⁻ : D_Li⊕ 로 **중성 Li 공급이 전해질 쪽 80.7 % · 집전체 쪽 19.3 %**(t_e = D_e⁻/(D_Li⊕ + D_e⁻) — 공통 β 라 상수) → 같게 하면 50 : 50(대칭 · 표면 포화 지연 → 용량 ↑) · 뒤집으면 19.3 : 80.7(거울) — 그림 (b)(d)(f) 의 모양이 이 분배다 · 쌍극 확산은 같게 할 때 오히려 ×0.62(1.614 D_Li⊕ → D_Li⊕) — **용량 증가는 D_p 가 아니라 경계 분배에서 온다**.

## Fig. 11 — 임피던스 측정 ↔ 모의 · 성분 (p. 16 · 봤다 · 래스터 화소) ★★★★ (b) · (c)

(a) 측정(파랑 네모) · 모의(검정 원) · 800 kHz · 10 mHz 화살 · (b) 모의 성분 Z_s · Z_d^p · Z_ct^n · Z_bat · Z_mt^LiPON · Z_ct^p · Z_mt^p · (c) 작은 성분 확대(두 축 같은 척도). `[도표·화소]`(표지 중심 · a 1.593 · b 1.562 · c 9.086 px / Ω cm² · 판독 폭 a · b ±3 · c ±0.5 Ω cm²): (a) 측정 호 꼭대기 **≈157 @Z_re ≈239** · 모의 **≈171 @≈192**(+9 %) · 극소 측정 ≈446–450 ↔ 모의 ≈456–457 · 800 kHz 측정 ≈(34, 42) ↔ 모의 ≈(27, 37) · 10 mHz 측정 ≈(510, 27) ↔ 모의 ≈(503, 23) · (b) Z_mt^LiPON 호 축 닿음 **≈327**(그 뒤 작은 용량성 저주파 고리 → ≈350) · Z_bat 극소 **≈457** · (c) Z_s **18.25**(점) · Z_ct^p 호 축 교차 **≈67.3** · 꼭대기 ≈32.5 @Z_re ≈33.6(순수 RC 반원) · 저주파 꼬리 → ≈(82, 7.6) · Z_ct^n 호 축 교차 **≈44.0** · 꼭대기 ≈18.3 @≈24.4(순수 RC 의 22 보다 낮다 — `[해석]` 같은 대역 ≈200 kHz 에서 c_geo 가 전류를 나눠 갖는 몫으로 읽히나 성분 정의 미인쇄) · **유도성 고리 최저 ≈(38.3, −3.4) → 끝(10 mHz) Z_re ≈35.6** · Z_d^p · Z_mt^p 45° 선(≤8.6 · ≤5.6). `[재현]` 판정 2 — 지름 넷 ✅ · Z_ct^n 저주파 고리: 글자 그대로 방향(축 아래 · 끝 35.6) ↔ 물리 방향(축 위 · 끝 52.3) — **그림은 앞쪽**(D1). ⚠ 본문 p. 15 "Impedance measurements (blue) and simulations (red)" ↔ 그림의 모의는 **검정**(같은 쪽 다음 문단은 "simulated (black line)" — D12).

## Table 1 · 2 — 약어 · 기호 (p. 2 · 3 · 봤다 · 수동 단독 크롭) ★★ (b)

표 1: 약어 열셋(AC … PDE · NDP 포함). 표 2: 기호 · 설명 · 차원 — **`c^i_dl` "Double layer capacity per unit area of electrode i" F m⁻²** · `c_geo` "Geometric capacitance per unit area" F m⁻² · `q^i_dl` "Charge per unit area in the double layer" **Ah m⁻²** · `A` "Geometrical surface area" m² · `ρ_i` "Geometrical-area resistance of material i" Ω m² · `D⁰_i` "Diffusion scaling constants" · `K` · `N`(Pt · Li 두께 — 값 0) · `V` Vacancy · `β` "Common time- and space-dependent factor for the diffusion coefficients" · `δ` "Fraction of Li in LiPON that resides in the mobile state" · 임피던스 Ω m²(그림 11 은 Ω cm²) · 아래첨자 목록에 "Li⁰"(본문 · 그림 2 는 Li_o — D16).

## Table 3 — 매개변수 (p. 8 · 봤다 · 수동 단독 크롭 · 렌더로 지수 확인) ★★★★ (a)

21 행 — §(a) 표. 각주 a · b · c · d · **무각주 13**. ⚠ 37호 표 1 의 각주 다섯 중 셋("Measured with Scanning Electron Microscope." · "Identified by direct measurements." · "Predefined (non-optimized) parameters.")이 이 표의 각주와 **글자 그대로 같다**(37호 digest 전사 대조 — 37호는 a · b 순서만 바꿈) — 표 틀의 상속 · 값의 상속 0.

## 본문 서술과 어긋난 그림 · 표 (요약)

- **그림 9e · 9f 삽도 · 11c 의 음극 계면** ↔ 인쇄 식 (10) 의 물리 방향 — 인쇄 식 (12) · (16) 을 글자 그대로 푼 계산과만 맞는다(D1).
- **그림 11c R_ct^p(≈67 · x ≈0.80)** ↔ "3.9 V"(EMF 3.900 = x 0.864 → 78 Ω cm²) — 모의 상태 미인쇄(D8).
- **그림 10e 삽도** — 컷오프 전 끊긴 모의(D9).
- **그림 4** — 이완 축 1 h(본문 2 h) · 0.1C 판 없음 · 0.2C 한 방향 잔차(D10).
- **그림 3** ↔ "good agreement … across the wide range" — 4C · 6C 첫 1–2 분 45–103 mV · 끝 용량 0.97(D11).
- **그림 11a 의 모의 색(검정)** ↔ 본문 "simulations (red)"(D12).
- **그림 2 범례 "Chairs of Phosphates"**(D14).
- **그림 3 EMF 용량 1.172 mAh** ↔ "0.7 mAh"(D6) · **그림 7 · 8 x 범위 0.510–1.000** ↔ `c_max` 의 Δx 0.5(D7).
- 그림 1 · 5 · 6 · 7 · 8 · 표 1–3 은 본문 서술과 맞는다(그림 6 은 우리 재풀이와 ±0.5 % 로 맞는다).

---

# 절별 해체 (본문)

## 초록 · 1. Introduction (p. 1–2)

- `[인쇄]` 문제 설정: "Although several efforts [11–13] have been made to mathematically describe ASSB this research is, however, not so well developed in comparison to liquid-based battery systems. For example, a detailed mathematical model for joined DC and AC simulations with a single set of parameters is still lacking." · "Recent reports on mathematical ASSB modelling focus on numerical simulations of the electrochemical-mechanical interaction [14] and the effect of contact area losses between the electrodes and electrolyte [15], leading to battery degradation." · "Earlier work … in which moderately good agreement between the measurements and simulations has been reported [11,12]."
- 계보: "Recently, the model developed by Danilov et al. [11] has been extended with an ionic concentration-dependent diffusion coefficient in the positive electrode [18]. Their model simulations have been experimentally validated." — 91호(2011) → Kazemi 2019([18]) → 이 편. 확장 넷: "(i) mixed ionic/electronic conductivity in the positive electrode, (ii) electrical double layers occurring at both electrode/electrolyte interfaces, (iii) variable ionic and electronic diffusion coefficients that depend on the lithium concentration inside the positive electrode, and (iv) including an as-denoted geometric capacitance, which is essential for accurate, high frequency, impedance simulations."
- ★ 검증 · 추정의 겹침을 저자가 스스로 쓴다: "After a detailed model description, the simulations are validated with DC voltage discharge curves at various C-rates and AC impedance measurements. It should be emphasized that a single parameter set is used for both the DC and AC simulations. **Since both DC and AC impedance measurements are used for model validation, it is to be expected that the model parameters can be determined much more accurately.**" — 같은 측정이 '검증' 이자 '결정' 의 자료다(판정 3).
- 범위 밖: "the aging-related processes, such as decomposition of electrolyte and electrode materials as well as contact losses due to electrode deformation are beyond the scope of this work. It is well known that commercial ASSB demonstrate remarkable longevity, with a typical cycle life of many thousands of cycles [21]. Therefore, the changes occurring with the battery on a relatively short-time scale are considered negligible."
- 초록 끝 "The present model is generally applicable to all-solid-state batteries where combined ionic and electronic transport takes place" — 시험된 셀은 한 종류(상용 LiPON 박막)다(D19 — 일반화 문장).

## 2.1 Electrochemical description (p. 2–4 · 그림 1 · 식 1–7)

- 반응 (1) "LiCoO2 ⇌ Li1−xCoO2 + xLi⁺ + xe⁻, (0 ≤ x ≤ 0.5)" · (2) "Li ⇌ Li⁺ + e⁻" — 순방향 = 산화(양극은 충전 방향 · 음극은 방전 방향). ⚠ 여기 x 는 **뽑아낸 양**(0–0.5)이고 그림 5 · 7 · 8 의 x 는 "x in LixCoO2"(0.5–1.0) — 한 지면 두 뜻(D15).
- 좌표 "the direction of the y-axis is from n towards p" · 원점 = Li | LiPON 경계 · 두께 N(Li) · L(LiPON) · M(LCO) · K(Pt).
- (3) U_prim = U^p(c^s_LiCoO2) − U^n(c^s_Li) · (4) η_bat = U_bat − U_eq("during charging η_bat is positive and during discharging η_bat is negative") · ★ (5) `[인쇄 · 렌더 확인]` "U*_bat = U_prim + η^p_ct + η^p_mt − η^LiPON_mt − η^n_ct = U^p(c^eq) + η^p_d + η^p_ct + η^p_mt − η^LiPON_mt − η^n_ct − U^n(c^eq)" · (6) U_bat = U*_bat + η_Li + η_Pt · (7) η_Pt = ρ_Pt j_bat · η_Li = ρ_Li j_bat.
- ★ 이 편의 유일한 식별성 문장: "**Since ρPt and ρLi cannot be separately identified, they are replaced by ρs = ρPt + ρLi**, which represents the total Ohmic series resistance of the battery." — 같은 전류가 흐르는 직렬 옴 둘의 합만 보인다는 올바른 구조적 묶음(`[해석]` 96호 R_c ↔ 1/κ̄^s 와 같은 '합' 축퇴의 처리판).
- `[해석]` 식 (5) 의 부호 "− η^LiPON_mt − η^n_ct" 는 식 (25) 가 정의하는 η^LiPON_mt(방전 중 음수 — 그림 6c · f)와 함께 쓰면 전해질 과전압이 전압을 **올린다**. 그림 9 는 모든 과전압을 같은 부호로 **더해** 쌓는다(범례 "η_s + η^LiPON_mt + η^p_d + η^p_ct + η^n_ct + η^p_mt"). 인쇄 식 (5) · (6) ↔ 그림 9 의 합산 규약이 어긋난다(D4).

## 2.2 Charge transfer kinetics and electrical double layers (p. 4–5 · 식 8–16)

- (8) `[인쇄 · 렌더 확인]` j^p_ct = j^p_0 [ (c^s_LiCoO2/c̄_LiCoO2) e^(α^p F η^p_ct/RT) − (c^s_CoO2 c^s_Li⁺ / c̄_CoO2 c̄_Li⁺) e^(−(1−α^p) F η^p_ct/RT) ] — 산화(충전) 양 · 앞인자 농도비 "When the pre-exponential concentration fractions are equal to 1, i.e. under full kinetically-controlled conditions, Eq. (8) can be simplified to the classical Butler-Volmer equation."
- (9) j^p_0 = F k₁ˢ c^max (1 − c̄/c^max)^α^p (c̄/c^max)^(1−α^p) c̄_Li⁺^α^p — `[재현]` 단위 k₁ˢ [m^2.5 mol^−0.5 s^−1] × c^max × c_Li⁺^0.5 × F = A m⁻² 로 **차원이 닫힌다**(91호 α 0.6 판과 달리) · x 0.51 에서 0.470 mA cm⁻².
- (10) `[인쇄 · 렌더 확인]` j^n_ct = j^n_0 [ (c^s_Li/c̄_Li) e^(α^n F η^n_ct/RT) − (c^s_Li⁺/c̄_Li⁺) e^(−(1−α^n) F η^n_ct/RT) ] = j^n_0 [ e^(α^n F η^n/RT) − (c^s_Li⁺/c̄_Li⁺) e^(−(1−α^n) F η^n/RT) ] — **Li 산화(방전 방향) 양** · (11) j^n_0 = F k₂ˢ c̄_Li⁺^α^n c̄_Li^(1−α^n) · "For a full derivation of the charge-transfer kinetics we refer to the paper of Danilov et al. [11]."
- 이중층: "An electrical double layer, also sometimes called space-charge layer, is present at the interface between (solid-state) electrolyte and electrodes … [20,23–26]. At the negative electrode/electrolyte interface of solid-state batteries, this layer is formed by mobile Li⁺ ions in the electrolyte and at the electrolyte/p interface by Li⁺ vacancies [23]."
- ★ (12) `[인쇄 · 렌더 확인]` "**j^i_ct + j^i_dl = j_bat − j_geo**, where superscript i indicates either the p or n electrode" — **두 계면에 같은 우변**. (13) j^i_dl = dq^i_dl/dt = c^i_dl dη^i_ct/dt · (14) j_geo = c_geo dU*_bat/dt · (15) · (16) 계면 ODE 가 둘 다 "= j_bat(t) − c_geo dU*_bat(t)/dt" 로 끝난다(렌더 확인).
- `[재현·대수]` 식 (8) 규약(산화 양)이면 방전 중 j_bat < 0 이고, 그것을 식 (16) 의 우변에 그대로 넣으면 식 (10) 은 음극을 **환원(Li⁺ + e⁻ → Li)** 으로 푼다 — 물리 방전(음극 Li 산화)과 반대 방향. 수송 경계 (18.3) 는 Li⁺ 가 y = 0 에서 전해질로 **들어간다**고 쓰고(아래), 본문 p. 10 도 그렇게 쓴다. 인쇄 식 묶음 안에서 음극의 '수송 방향' 과 '동역학 방향' 이 갈린다 — 그림 9 · 11c 는 이 글자 그대로의 계산과 정량으로 맞는다(D1 · 판정 2).
- 축전기 처리: "In the present work, both the electrical double layers and the geometric capacitance are modelled as electric capacitors in order to reduce the model complexity. However, it is obvious that it is also possible to apply more advanced mathematical models to simulate the space-charge layer formation [20,25,26]." · 기하 축전기: "Since the LiPON solid-state electrolyte is an ionic conductor rather than an electronic conductor, it can be considered as an electronic insulator. Assuming that the LCO electrode is also a relatively poor electronic conductor, then the LiPON and LCO can be considered as a dielectric between two electronic conductors."

## 2.3 Diffusion and migration in the electrolyte (p. 5–7 · 그림 2 · 식 17–25)

- 해리 (17) Li_o ⇌ Li⁺ + n⁻(k_d · k_r) · n⁻ = "uncompensated negative charge associated with a vacancy formed in the LiPON matrix at the place where lithium was originally located" · "Note that Lio is not a lithium metal and the movement of uncompensated negative charge (n−) does not contribute to electronic conductivity" · 평형 c^eq_Li⁺ = c^eq_n = δc₀ · k_d = k_r c₀ δ²/(1 − δ).
- (18.1)–(18.4) `[인쇄 · 렌더 확인]` J_Li⁺(0, t) = **−** j^n_ct/(z F) = −(j_bat − j_geo − j^n_dl)/(z F) · J_Li⁺(L, t) = **+** j^p_ct/(z F) = (j_bat − j_geo − j^p_dl)/(z F) — 같은 우변(식 12)에 **반대 부호** → 정상 상태 보존(J(0) = J(L))과 맞지 않는다(D2). (19.3) · (19.4) n⁻ 플럭스 0.
- (20)–(22) c₀ = c_Lio + c_n · 전기중성 c_n = c_Li⁺ · "the total lithium concentration in the electrolyte … must be constant".
- (23.1) ∂c/∂t = [2D_Li⁺D_n⁻/(D_Li⁺ + D_n⁻)] ∂²c/∂y² + r · (23.3) `[인쇄 · 렌더 확인]` ∂c(0,t)/∂y = j^n_ct/(z F) = (j_bat − j_geo − j^n_dl)/(2F D_Li⁺) · (23.4) 같은 꼴 at L — 가운데 항 j/(zF) 는 **플럭스 차원**(mol m⁻² s⁻¹)이지 기울기(mol m⁻⁴)가 아니다(D3) · 마지막 항은 두 끝 **같은 부호**(보존과 맞음 · j_bat < 0 이면 c(0) > c(L) — 물리 방향).
- (24) E(y,t) = (RT/F)(1/c){ −j/(2FD_Li⁺) + [(D_Li⁺ − D_n⁻)/(D_Li⁺ + D_n⁻)] [∂c/∂y − j/(2FD_Li⁺)] } — `[재현·대수]` 정리하면 E = [−j/F + (D_Li⁺ − D_n⁻)∂c/∂y]/[(D_Li⁺ + D_n⁻)(F/RT)c] 로 이동 · 확산 전류 합과 같다(j_bat < 0 규약에서) ✅ · (25) η^LiPON_mt = (RT/F) ln[c(L)/c(0)] − ∫E dy — "Nernstian" + "Galvanic".
- `[재현]` 반응층 두께 λ = √(D_amb/(k_d + 2k_r δc₀)) = **47 nm** · 재결합 시간 τ_r = **8.46 s** · 벌크 확산 시간 L²/D_amb = **13.7 h** — 농도 분극은 두 계면 47 nm 층에 갇히고 벌크는 평탄(그림 6a · d 와 같다).

## 2.4 Diffusion and migration in the LiCoO2 electrode (p. 7–9 · 식 26–32)

- (26) 이온 Li⊕ 와 전자 각각 Nernst–Planck · (27) "D_Li⊕(y,t) = D⁰_Li⊕ β(y,t) and D_e⁻(y,t) = D⁰_e⁻ β(y,t)" — "This leads to constant transport numbers as a function of lithium concentration." · β 의 함수형은 지면 어디에도 없다(그림 5 만 · G2).
- (28.3) J_Li⊕(L,t) = (j^p_ct + j^p_dl)/(z F) · (29.4) J_e⁻(L+M,t) = (j_bat − j_geo)/(z_e F) · (30.3) ∂c(L,t)/∂y = (j_bat − j_geo)/(2 D_Li⊕(L,t) F) · (30.4) ∂c(L+M,t)/∂y = −(j_bat − j_geo)/(2 D_e⁻(L+M,t) F)(전부 렌더 확인). `[재현·대수]` 전기중성 아래 (28.3) · (29.4) 에서 (30.3) · (30.4) 를 유도하면 둘 다 **반대 부호**가 나온다 — p 안에서는 함께 뒤집혀 분배 · 비는 일관하지만 j 의 부호 규약이 식 묶음 사이에서 바뀐다(D5).
- D⁰_p = 2D⁰_Li⊕D⁰_e⁻/(D⁰_Li⊕ + D⁰_e⁻) · "In Appendix A the finite difference approximation for flat solid-state diffusion in p is described, which has been used for the implementation in Matlab." · (31) 양극 전기장 · (32) η^p_mt.

## 3. Experimental (p. 9–10)

- "Commercial all-solid-state thin-film batteries with a capacity of 0.7 mAh were used for the experiments." · LCO 8.08 µm on Pt · LiPON 3.62 µm · Li 금속 · "The surface area of the deposited electrodes is 3.36 cm²." · Maccor 2300 · "five activation cycles" · "CC-charging was performed at 1 C-rate (0.7 mA) up to a voltage of 4.2 V, followed by CV-charging at 4.2 V, using a cut-off current of 0.1 C-rate (0.07 mA)" · 방전 0.1–6.0C · 컷오프 3.0 V.
- ★ EMF: "On the basis of this set the EMF voltage curve was determined by mathematical extrapolation, of which the details can be found in previous publications [32,33]." — [32] · [33] = Li D. 외 2016 *Electrochim. Acta* 190 · 210 의 C6/LiFePO₄ 노화 편(방법 원전 · 미열람).
- "After both charging and discharging a relaxation period of 2 h was applied." · EIS "Potentiostatic … at a voltage of 3.9 V for 50 logarithmically distributed frequencies in the range of 10 mHz–800 kHz … The applied AC excitation voltage was set to 10 mV in order to obtain a good signal-to-noise ratio and a linear response." · "temperature-controlled condition of 20 °C, which is also the temperature used in the simulations."
- 셀 수 · 반복 · 제조사 0(G5) · SEM 방법 0(G6).

## 4.1 Total battery (p. 10 · 그림 3 · 4 · 5)

- "Fig. 3 shows the measured (symbols) and optimized simulated (lines) discharge curves … It can be seen that the agreement between the measurements and simulations is good across the wide range of investigated C-rates. The optimized model parameters are listed in Table 3." — `[도표·벡터]` 몸통 RMS 1.2–5.1 mV(≤2C) · 19.1 · 47.6 mV(4C · 6C — 첫 1–2 분) · 끝 용량 0.972(4C · 6C).
- "From these results it can be concluded that the simulations are not only in good agreement during constant current discharging but also after current interruption during the entire relaxation time under all conditions." — 그림 4 0.2C 한 방향 잔차(D10).
- 그림 5: "the magnitude of the electronic diffusion coefficient is higher than that of the ionic diffusion coefficient, indicating that ionic diffusion is a limiting factor" · "(0.5 ≤ x ≤ 0.75), representing the so-called second hexagonal phase [34]" · "two-phase coexistence region (0.75 ≤ x ≤ 0.92) … decrease more than one order of magnitude" · ★ "The optimized diffusion coefficient for Li⊕ is in agreement with measurement and simulation results published in the literature for similar ASSB [12,35]" — 문헌 값 미인쇄 · 그리고 전자 쪽은 "electronic conductivity is proportional to the diffusion coefficient … [20,36]" 로 LCO 전도도 문헌 [37–39] 의 x 의존과 "good agreement"(정성).

## 4.2 Electrolyte (p. 10–11 · 그림 6)

- "The mobile Li⁺ concentration in the bulk of the electrolyte is about 39 kmol m⁻³, which is in close agreement with the estimated value of 40 kmol m⁻³ reported by Put et al. [40]. This value depends on the maximal concentration (c₀) and the fraction of Li⁺ that resides in the mobile state (δ). The optimized parameter values are reported in Table 3." — `[재현]` δc₀ = 39.13 kmol m⁻³ · 이 편 유일한 '문헌 값 ↔ 적합 값' 수치 대조(c₀ · δ 는 곱으로만 이 대조에 들어간다).
- ★ "At position 0 (interface with n in Fig. 1), the concentration of mobile Li⁺ is higher than at position L (interface with p) **as Li⁺ ions are inserted into the electrolyte at 0 and removed from the electrolyte at L during discharge**." — 수송은 물리 방향(D1 의 한쪽).
- "The electric field immediately develops when the current is applied and quickly reduces to zero if the current is switched off" · 비대칭 "from the 1/c_Li⁺(y,t) term in Eq. (24)" · "the overpotentials are dominated by migration (dashed red lines), while the diffusive component (dotted green lines) only has a minor contribution."

## 4.3 Positive electrode (p. 11–13 · 그림 7 · 8)

- 표면 · 벌크 x(그림 7b · f) · "Due to the low diffusion coefficients at the end of discharging (Fig. 5), the concentrations at the surface largely increase with respect to the bulk, especially at the 4C discharge rate." · "In general, the charge-transfer overpotential at p/electrolyte interface is most dominant."
- "Remarkably, the diffusion overpotential at 1C-rate (Fig. 7d) is larger at the end of discharging than at 4C-rate (Fig. 7h)." → 그림 8: "the surface concentrations at the end of discharging are about the same (x≈1). However, because the EMF curve is almost vertical at the end of discharging (Fig. 8), small changes in concentration can lead to large changes in voltage." — `[도표·벡터]` 표면 x 0.998 ↔ 0.994 × EMF 끝 기울기 ≈−72 V/단위 x(G3 의 외삽 영역).

## 4.4 Overpotential contributions (p. 13–14 · 그림 9)

- "the electrolyte overpotential (green area) has the largest contribution. Other important overpotential contributions … are caused by the charge-transfer losses (cyan) at the p/electrolyte interface (η^p_ct) and by the diffusion losses inside p (η^p_d) (red)." · "The remaining overpotentials, due to the Ohmic series resistance (blue area representing η_s) and charge-transfer at the n/electrolyte surface (magenta area representing η^n_ct) have the smallest contributions. **The charge-transfer overpotential at p is larger than at n because the reaction rates are faster at n.**"(D13)
- "Based on the overpotential analysis, it can be concluded that the electrolyte is the dominating factor in the performance limitations of ASSB." — 셀 하나 · 화학 하나의 모형 분해에서 'ASSB' 일반으로(D19 와 같은 일반화).
- 이완: "the voltage relaxation of the investigated batteries is mainly caused by the processes in p" · "Although the applied current is interrupted, the charge-transfer overpotential can still be identified in the relaxation process. The reason is because the pre-exponential concentration fractions (Eq. (8)) are unequal to 1 during relaxation."

## 4.5 Influence of diffusion coefficients (p. 13–15 · 그림 10)

- "In order to investigate the influence of both the ionic and electronic diffusion coefficients, **a small sensitivity study** is performed" — 이 편 유일한 `sensitiv*` · 대상은 출력(용량 · 농도 단면)이고 식별성이 아니다(개념 [[assb-sensitivity-sweep-vs-identifiability]] 첫 줄 — 설계 KPI 스윕).
- "Note again the excellent agreement between the simulation and experiment."(그림 10a 삽도) · D_Li⊕ = D_e⁻: "the concentration profile in the LCO electrode has become fully symmetric … no electric field development … absence of a mass-transfer overpotential … more capacity can therefore be extracted" · "These simulation results show that if both the ionic and electronic diffusion coefficients are identical, the battery performance increases significantly" — 측정 0 의 처방 효과(`[해석]` (겨) 와 같은 축).
- D_Li⊕ > D_e⁻: "An interesting, but rather rare situation … The concentration profiles in Fig. 10f are mirrored … Similar unusual concentration profiles have indeed been demonstrated experimentally in LiFePO4 powder electrodes in recent Neutron Depth Profiling (NDP) studies [41]." — 그림 10e 삽도 모의가 컷오프 전 끊긴 것(D9)은 언급 0.

## 4.6 Impedance simulations (p. 15–16 · 그림 11)

- "Impedance measurements (blue) and simulations (red) are shown in Fig. 11."(D12) · "The impedance simulations are performed with exactly the same model and parameter set (Table 3) that was used for the DC simulations. However, instead of applying a DC current to the ASSB an AC current has been applied with a zero DC bias. The resulting time-domain signals have then been transformed to the frequency domain by Fourier transformation" — 측정 상태(3.9 V 정전위) ↔ 모의 상태(x 미인쇄 · G4).
- ★ "**Performing impedance simulations in addition to DC simulations results in much more accurate parameter estimation since more measurement information has been made available. Moreover, it should be noted that when only the DC simulations are used for parameter optimization, the impedance simulations do not agree with the impedance measurements. It is therefore important that both the AC and DC behavior are simulated.**" — 비유일성 증상 한 문장(그림 · 값 0) + 처방 선언(판정 7).
- "There is a reasonable agreement between the measurement and simulation along the entire frequency range." · "the total battery impedance (Z_bat) at the highest frequencies is lower than the electrolyte impedance … because the geometric capacitance (c_geo) 'short-circuits' the battery at high frequencies".
- ★ "At low frequencies in the p and n impedance, another semicircle appears due to the changing ionic concentrations. The pre-exponential concentration fractions in Eqs. (8) and (10) are responsible for this behavior. **Apparently, the (interface) concentrations develop in such a way that this leads to a reduction in impedance and to an uncommon (inductive) semicircle in the low frequency range for the negative electrode.**" — `[재현·대수]` 물리 방향이면 이 농도 항은 저항을 **늘린다**(축 위 고리 · 끝 52.3) · 글자 그대로 방향이면 **줄인다**(축 아래 · 끝 35.6) — 그림은 뒤쪽(D1).
- ★ "The high-to middle-frequency range is the range where the double layer capacitors play a role. This suggests that the space-charge layers in this particular ASSB do not have a large influence on the static (DC) discharge curves and, thus, on the overall performance, which has also been concluded by others [26,42]. However, this might be different for ASSB that are used in, for example, applications in which mid-to-high frequency dynamic loads are applied, such as microelectromechanical systems (MEMS) [16]."(G12)
- "The diffusion (Z^p_d) and mass-transfer (Z^p_mt) impedances in p … show the typical diffusive line with an angle of approximately 45°."

## 5. Conclusions (p. 16)

- "The model describes all relevant processes occurring in the electrodes, electrolyte, and at the interfaces." · "double layer capacitors are applied at both electrode/electrolyte interfaces to describe the space-charge effect. The model parameter values have been optimized such that both DC and AC model simulations are in a good agreement with measurements on 0.7 mAh Li/LiPON/LiCoO2 all-solid-state batteries. It should be emphasized that the parameter set for the DC simulations is exactly equal to that of the AC simulations." · "Charge-transfer, including electrical double layer losses at the positive electrode/electrolyte interface, and diffusion in the positive electrode are causing the second major losses in the battery." · "the simulations suggest that the space-charge layers in this particular ASSB do not have a large influence on the static discharge curves" · "the battery performance increases significantly if the ionic and electronic diffusion coefficients are identical."

## 부록 A (p. 16–18 · 식 A.1.1–A.14)

- 식 (30) 의 유한차분: 균일 격자 n 점 · h = L/(n − 1) · 시간 전진 차분 Δt · β 는 반점 평균 · 경계는 2h 중심 차분 + 가상점 · 행렬꼴 (A.12) c^{j+1} = c^j + D⁰_p Δt/h² H^j c^j + D⁰_p Δt/h b^j · 상수 β 면 (A.14) 삼중대각. ⚠ 부록에서 L 은 LCO 두께 자리(본문 M)에 다시 쓰였고(같은 기호 L 이 본문 LiPON 두께 — 표기만), n · Δt 값 · 안정 조건 · 전해질(식 23) · 계면 ODE(식 15 · 16)의 이산화는 부록 밖(G8).

---

# ★ (a) 매개변수 표의 출처 층위 — 표 3 21 행 · 26호 표와 같은 이름끼리

## 1. 중심 표 (`[인쇄]` 표 3 · 각주 · 26호 열은 26호 digest §1 · §2 · §3-2 전사)

| # | 이 편 기호(→ 26호 이름) | 이 편 값 `[인쇄]` | 각주 → 층위 | 26호 "문헌" | 26호 최적 | 최적 ÷ 이 편 | 메모 |
|---|---|---|---|---|---|---|---|
| 1 | T | 293 K | a → 직접 측정 | 293 고정 | — | — | "temperature-controlled condition of 20 °C" |
| 2 | L(→ J) | 3.62 µm | b → SEM | 3.62 고정 | — | — | SEM 그림 · 방법 0(G6) |
| 3 | M(→ H) | 8.08 µm | b → SEM | 8.08 고정 | — | — | c_max 의 분모 |
| 4 | A | 3.36 cm² | a → 직접 측정 | 3.36 고정 | — | — | 모든 전류 · 용량 · 축전기의 면적 기준(기하) |
| 5 | k_r | 8.00×10⁻⁷ m³ mol⁻¹ s⁻¹ | 무각주 → **적합** | 8.00e-7 | 8.4000e-7 | **1.0500** | `[재현]` 인쇄 값이 그림 6 을 닫는다(×0.1 이면 1C −87.2 mV · 4C 고갈) |
| 6 | k₁ˢ(→ k¹_s) | 1.53×10⁻¹¹ m^2.5 mol^−0.5 s⁻¹ | 무각주 → **적합** | 1.53e-11 | 1.6000e-11 | 1.04575 | i₀ᵖ 0.470 mA cm⁻²(x 0.51) · 식 (9) 차원 폐합 · 26호 단위 표기 "mol^0.5"(26호 digest 전사 — 부호 다름) |
| 7 | k₂ˢ(→ k²_s) | 1.09×10⁻⁹ m s⁻¹ | 무각주 → **적합** | 1.09e-9 | 1.1445e-9 | **1.0500** | i₀ⁿ 0.575 mA cm⁻² · R_ct^n 43.9 ↔ 그림 11c ≈44.0 |
| 8 | α^p | 0.5 | c → 사전 고정 | 0.5 고정 | — | — | 91호는 0.6 적합 |
| 9 | α^n | 0.5 | c → 사전 고정 | 0.5 고정 | — | — | |
| 10 | D⁰_Li⊕(→ D⁰_M⊕) | 1.21×10⁻¹³ m² s⁻¹ | 무각주 → **적합**(+ 함수 β(x)) | 1.21e-13 | 1.2705e-13 | **1.0500** | β = D/D⁰ 0.65–0.025 — D⁰ 는 작동 창 어느 x 의 D 도 아님 |
| 11 | D⁰_e⁻ | 5.06×10⁻¹³ m² s⁻¹ | 무각주 → **적합** | 5.06e-13 | **5.2400e-3** | **1.036×10¹⁰** | D_e⁻/D_Li⊕ = 4.18(공통 β) — **`D_e⁻` 의 원래 값** |
| 12 | D_Li⁺(→ D_M⁺) | 1.73×10⁻¹⁶ m² s⁻¹ | 무각주 → **적합** | 1.73e-16 | 1.8165e-16 | **1.0500** | t₊ = 0.233 |
| 13 | D_n⁻ | 5.69×10⁻¹⁶ m² s⁻¹ | 무각주 → **적합** | 5.69e-16 | 5.9745e-16 | **1.0500** | D_amb 2.65×10⁻¹⁶ |
| 14 | c^max_LiCoO2(→ a^max_M⊕) | 3.22×10⁴ mol m⁻³ | d → **EMF 유도** | 3.22e4 | 3.3810e4 | **1.0500** | `[재현]` EMF 용량 1.172 mAh ÷ (F·A·M·Δx 0.5) = 3.222×10⁴ ✅ · 그림 7 · 8 의 x 0.510 → 1.000(Δx 0.490)이면 3.29×10⁴(D7) |
| 15 | c^s_Li = c̄_Li(→ a_M) | 7.64×10⁴ mol m⁻³ | c → 사전 고정 | 고정(26호 digest "a_M 고정") | — | — | `[재현·외부 값]` Li 금속 밀도 0.534 g cm⁻³ ÷ 6.941 g mol⁻¹ = 7.69×10⁴ — 0.7 % 차 |
| 16 | c₀(→ a₀) | 61141 mol m⁻³ | 무각주 → **적합**(본문 "The optimized parameter values are reported in Table 3") | 61141 | 64198 | 1.049999 | 91호 NDP 6.01×10⁴ 와 1.7 %(G10) |
| 17 | δ | 0.64 | 무각주 → **적합** | 0.64 | 0.64 | 1.000 | δc₀ = 39.13 kmol m⁻³ ↔ Put [40] "estimated value of 40 kmol m⁻³"(본문 "close agreement" — 곱으로만 대조) · 26호 G6 고정 표시 없음 |
| 18 | ρ_s(→ ρ_Li+Pt) | 18.3 Ω cm² | 무각주 → **적합** | **18.3 고정**(26호 digest §1) | — | — | "Since ρPt and ρLi cannot be separately identified, they are replaced by ρs" |
| 19 | c^p_dl | 5.30×10⁻⁷ F cm⁻² | 무각주 → **적합** | 없음(26호 가정 2 — 이중층 0) | — | — | §(b) |
| 20 | c^n_dl | 1.74×10⁻⁸ F cm⁻² | 무각주 → **적합** | 없음 | — | — | §(b) — c_geo ×5.4 |
| 21 | c_geo | 3.24×10⁻⁹ F cm⁻² | 무각주 → **적합** | 없음 | — | — | ε_r 역산 13.2(LiPON) · 42.8(LiPON + LCO) |
| + | β(x) | 그림 5 곡선 둘 | 함수형 미인쇄 → **적합**(그림만) | "extracted from the same paper [10]"(26호 G5) | — | — | 자유도 미상(G2) |
| + | U^p(x) = EMF | 그림 3 · 8 곡선 | **같은 율 묶음 외삽**([32, 33] — 방법 미인쇄) | "Nernst curve … extracted from the same paper"(26호 G5) | — | — | c_max(14)의 출처이기도(G3) |

**집계**: 21 행 = 직접 측정 2(T · A) · SEM 2(L · M) · 사전 고정 3(α^p · α^n · c_Li) · EMF 유도 1(c_max) · **무각주 = 적합 13** + 함수 둘(β(x) 적합 · EMF 외삽). 26호 "문헌" 열 10 개 = 이 편 적합 9(5 · 6 · 7 · 10 · 11 · 12 · 13 · 16 · 17) + EMF 유도 1(14) — **측정값 0**.

## 2. ×1.0500 관계 — 이 편 인쇄값 기준으로 선다 (`[재현]`)

- 정확히 ×1.0500(인쇄 유효숫자 전부): k_r · k₂ˢ · D⁰_Li⊕ · D_Li⁺ · D_n⁻ · c_max · c₀(61141 × 1.05 = 64198.05 → 64198) — **일곱**(26호 digest 의 셈과 같다). k₁ˢ ×1.04575(×1.05 면 1.6065) · δ ×1 · D⁰_e⁻ ×1.036×10¹⁰.
- ⇒ 26호의 시작점 · 정지 해석(26호 §3-2 `[추론]` "시작점 = 문헌 × 1.05")은 이 편 값으로 바뀌지 않는다 — 이 편이 확인하는 것은 **그 '문헌' 이 무엇인가**(같은 셀 · 같은 곡선 묶음의 적합)다.

## 3. 같은 이름 ×1.05 뒤에서 모형이 실제로 보는 조합 (`[재현·대수]` — 인쇄 식 (9) · (11) · (23) · (27) · (30) 그대로)

| 조합 | 식 | 이 편 | 26호 최적 | 비 | 뜻 |
|---|---|---|---|---|---|
| 양극 쌍극 확산 D⁰_p | 2D_Li⊕D_e⁻/(D_Li⊕+D_e⁻) | 1.953×10⁻¹³ | 2.541×10⁻¹³ | **×1.301** | D_e⁻ → ∞ 극한 = 2D_Li⊕ — 26호 §5-2 ② 의 `D_M⊕·a_max/I` 한 조합으로 접힘 |
| 경계 공급 분배 t_e(전해질 쪽 몫) | D_e⁻/(D_Li⊕+D_e⁻) | **0.807** | **1.000** | — | 집전체 쪽 공급 19.3 % → 0 — 그림 10 의 단면 모양을 정하는 양이 사라짐 |
| 전해질 전도도 σ | (F²/RT) δc₀ (D_Li⁺+D_n⁻) | 1.110×10⁻⁶ S cm⁻¹ | 1.224×10⁻⁶ | ×1.1025 | 벌크 저항 L/σ 326.2 → 295.9 Ω cm²(26호는 EIS 0 이라 이 값을 볼 관측이 없다) |
| t₊ | D_Li⁺/(D_Li⁺+D_n⁻) | 0.233 | 0.233 | ×1 | |
| 반응층 λ · τ_r | √(D_amb τ_r) · 1/(k_d+2k_r δc₀) | 47 nm · 8.46 s | 46 nm · 7.67 s | ×0.976 · ×0.907 | |
| i₀ᵖ | F k₁ˢ c_max √(x(1−x)) √(δc₀) | 0.470 mA cm⁻²(x 0.51) | 0.529 | ×1.125 | |
| i₀ⁿ | F k₂ˢ √(δc₀ c_Li) | 0.575 mA cm⁻² | 0.619 | ×1.076 | c_Li 고정 |
| 용량 스케일 | c_max · A · M · Δx · F | 1.172 mAh | 1.230 mAh | ×1.05 | 26호 Q_ideal · C-rate 분모(판정 5) |

⇒ **"7 / 10 이 ×1.05" 는 이름 단위의 정지이고, 모형이 보는 조합 단위로는 D⁰_p ×1.30 · 경계 분배 0.81 → 1.00 · σ ×1.10 · i₀ ×1.08–1.13 이 움직였다.** 26호의 "문헌과 5 % 이내" 는 이름 표에서만 선다.

## 4. `D_e⁻` 의 원래 값

`[인쇄]` D⁰_e⁻ = **5.06×10⁻¹³ m² s⁻¹**(무각주 · 적합) · `[도표·벡터]` 그림 5 의 D_e⁻(x) ≈3.3×10⁻¹³ → ≈1.3×10⁻¹⁴ · 비 D_e⁻/D_Li⊕ = 4.18(식 (27) 공통 β — x 무관). 이 편 안에서 D_e⁻ 를 따로 정하는 관측은 **경계 분배 t_e**(그림 10 단면 · 표면 x)와 **양극 물질전달 과전압 η^p_mt**(식 32 — 그림 7d · h · 9 노랑 · 11c 노랑 45° 선)이다 — 둘 다 작은 몫(η^p_mt 4C −4.3 mV `[도표·화소]`)이라 26호의 DC 네 곡선이 이 방향을 못 본 것과 맞는다(26호 D5 의 이 편 쪽 근거 — 이 편 지면에서 이 방향의 감도 · 폭은 인쇄 0).

---

# ★ (b) 이중층(공간 전하) 항 — 정의 · 면적 · 값의 출처 · 37호 물음

## 1. 정의 (`[인쇄]` 식 12–16 · 표 2)

- 계면 전류 분할: j^i_ct + j^i_dl = j_bat − j_geo(두 계면) · j^i_dl = c^i_dl dη^i_ct/dt — **축전기가 전하이동 과전압 η_ct 에 걸린다**(전위 강하 전체가 아니라). 기하 축전기 j_geo = c_geo dU*_bat/dt 는 셀 전체(옴 강하 뺀 전압)에 걸린다.
- 물리 귀속: "this layer is formed by mobile Li⁺ ions in the electrolyte [n 쪽] and at the electrolyte/p interface by Li⁺ vacancies [23]" — 그러나 구현은 "modelled as electric capacitors in order to reduce the model complexity" — 공간전하층 모형([20, 25, 26])은 "also possible" 로만.
- 단위: 표 2 `c^i_dl` "Double layer capacity **per unit area** of electrode i" F m⁻² · `c_geo` "Geometric capacitance per unit area" F m⁻² · `q^i_dl` "Charge per unit area" Ah m⁻² · 표 3 F cm⁻².

## 2. 면적 — 기하 면적 하나, 실제 계면 구분 0

- `A` "Geometrical surface area" = 3.36 cm²(각주 a "Identified by direct measurements") · 모든 j 는 이 A 로 나눈 밀도 · `ρ_i` 도 "Geometrical-area resistance". 거칠기 · 실제 접촉 면적 · 부분 박리를 나타내는 변수 0.
- `[재현·대수]` 숨은 면적 인자 f_A(실제 계면 ÷ 기하) 가 있으면 j₀ ∝ f_A k(식 9 · 11 에 곱으로) · c_dl ∝ f_A 이고 R_ct = RT/(F j₀) ∝ 1/f_A · **τ_dl = R_ct c_dl 은 f_A 무관** — 이 편의 적합 k · c_dl 은 'f_A × 물질 상수' 두 곱이고, 이 편 자료(면적 하나 · 신품 · 온도 하나)로는 f_A 를 따로 정할 수 없다.
- ⇒ **37호 물음 "`c_dl` 이 면적에 비례하는가"** 에 조상은 **"기하 면적에 비례하는 꼴(F cm⁻² × A)이지만 실제 계면 면적은 모형에 없다"** 로 답한다. 16호 처방 전제(C ∝ 면적 · R·C 면적 불변)를 **형식상 만족하되 시험할 수 없는** 꼴이고, 37호의 `c_dl`(F · 전극 전체 상수)과 `A_eff` 를 패러데이 항에만 둔 구성은 **조상에 없는 변형**이다(37호 digest 전사 대조).

## 3. 값의 출처 · 물리 범위

- 출처: 무각주 = DC 일곱 율 + EIS 한 상태 동시 적합(목적 함수 미인쇄). 측정(예: 축전기 법 · 고주파 C 판독) 0 · 문헌 0.
- `[재현·가정]` 물리 범위 — c_geo = ε₀ε_r/d 로 ε_r 를 역산하면 d = L 일 때 **13.2** · d = L + M 일 때 **42.8**. 같은 ε_r 로 c_dl 의 등가 유전체 두께 d = ε₀ε_r/c_dl: c^n_dl → **0.67–2.2 µm**(LiPON 두께 3.62 µm 의 ⅕–⅗) · c^p_dl → **22–72 nm**. ⇒ c^n_dl 은 nm 척도 공간전하층의 값으로 읽을 수 없다 — **고주파 호 모양을 흡수한 유효 매개변수**다(`[해석]`). c^n_dl = c_geo × 5.4 라 두 축전기가 같은 대역에 앉는다(아래 τ).
- `[재현]` 시간 상수: τ_n = R_ct^n c^n_dl = **0.764 µs(208 kHz)** · τ_LiPON = R_bulk c_geo = **1.057 µs(151 kHz)** · τ_p = R_ct^p(x 0.80) c^p_dl = **35.6 µs(4.47 kHz)** — τ_n/τ_LiPON = 0.72 ⇒ **측정 스펙트럼에서 음극 호와 LiPON · 기하 축전기 호가 겹친다**(그림 11a 측정은 큰 호 하나 + 꼬리). 그림 11c 의 음극 호 꼭대기가 순수 RC(22)보다 낮은 ≈18.3 인 것도 같은 대역 겹침과 맞는다(`[해석]` — 성분 정의 미인쇄).

## 4. "이중층 영향 작다" 결론의 근거 (G12)

`[인쇄]` "The high-to middle-frequency range is the range where the double layer capacitors play a role. This suggests that the space-charge layers in this particular ASSB do not have a large influence on the static (DC) discharge curves … which has also been concluded by others [26,42]." — 근거 = 대역 논증 + 남의 결론 둘(de Klerk & Wagemaker 2018 · Haruta 2015 — 미열람). c_dl 을 흔든 모의 · 그림 · 표 0. `[재현·대수]` τ 가 µs 라 DC(분 단위)에서 축전기 전류는 전류 계단 직후 µs–ms 에만 흐른다 — "DC 곡선에 작은 영향" 은 **이 축전기 모형 안에서는 구성상 참**이고, 공간전하층이 계면 저항 · 농도(Li⁺ 고갈층)를 바꾸는 물리는 축전기 모형에 처음부터 없다 — 결론은 모형 선택의 귀결이지 시험이 아니다(37호 G12 와 같은 구조 — 37호 digest 전사).

## 5. 37호와의 대조 (37호 digest 전사)

| 항목 | 이 편(조상) | 37호 Li 2024 |
|---|---|---|
| 단위 · 면적 | F cm⁻² × 기하 A | **F(전극 전체)** — 면적 무관 상수 |
| 면적 손잡이 | 없음(기하 A 하나) | `A_eff` 가 패러데이 항에만 |
| 값(기하 면적당) | c^p_dl 0.530 · c^n_dl 0.0174 µF cm⁻² | 6.49 · 0.166 µF cm⁻²(÷ 0.7854 cm²) — **×12.2 · ×9.5** |
| 출처 각주 | 무각주(적합) | 무각주(37호 G2) |
| "작은 영향" 결론 | 대역 논증 + [26, 42] | 같은 결론 · 근거 그림 0(37호 G12) |
| 표 각주 글자 | a "Identified by direct measurements." · b "Measured with Scanning Electron Microscope." · c "Predefined (non-optimized) parameters." | 다섯 중 셋이 **글자 그대로 같다**(a · b 순서만 바꿈) |

⇒ **표 틀 · 결론 문장은 상속, 값 · 면적 규약은 상속 0.** 91호가 단서로 남긴 "37호 `c^p_dl` 5.1×10⁻⁶ F ↔ 91호 `k₁ˢ` 5.1×10⁻⁶" 의 5.1 은 이 편 표 3 어디에도 없다 — 이 편을 거친 상속으로는 설명되지 않는다(우연인지 판정 안 함).

---

# ★ (c) 검증 — DC · 이완 · EIS 가 한 벌인가 · 맞춘 것 ↔ 예측한 것

## 1. 자료와 그 쓰임

| 자료 | 측정 | 적합에 들어갔나 | 근거 |
|---|---|---|---|
| 정전류 방전 일곱 율(0.1–6C) | ✅ 그림 3 | ✅ | "optimized simulated (lines)" · "The optimized model parameters are listed in Table 3" |
| EMF | 같은 일곱 율의 외삽 | 모형 입력(U^p) · c_max 유도 | p. 10 · 각주 d |
| 이완 2 h(그림은 1 h · 여섯 율) | ✅ 그림 4 | **미인쇄**(G9) | "Measured … and simulated … relaxation curves" 만 |
| EIS 한 상태(3.9 V · 10 mHz–800 kHz) | ✅ 그림 11a | ✅ | "optimized such that both DC and AC model simulations are in a good agreement" · "when only the DC simulations are used for parameter optimization, the impedance simulations do not agree" |
| D 바꾸기 둘(그림 10c–f) | ✗ 모의만 | — | 이 편 유일한 '예측' — 측정 대조 0 |

⇒ **"validated" 의 자료 = 적합 자료**. 보류 율 · 보류 셀 · 다른 상태 EIS · 다른 온도 0. 초록의 "experimentally validated" 와 "The model shows good agreement with … voltage relaxation upon current interruption" 는 표본 안 일치이고, 이완은 적합 여부가 미인쇄라 표본 밖이라고도 할 수 없다.

## 2. 잔차 (`[도표·벡터]` · `[도표·화소]`)

- 방전(그림 3): 몸통 RMS 1.2 · 1.8 · 2.0 · 5.1 · 19.1 · 47.6 mV(0.1 · 0.5 · 1 · 2 · 4 · 6C) · 4C · 6C 첫 1–2 분 −45 … −103 mV · 끝 용량 모의/측정 0.996 · 1.005 · 0.998 · 0.989 · 0.972 · 0.972.
- 이완(그림 4a): 0.2C 측정 − 모의 ≈+22 → ≈+12 → ≈+9 → +2.5–6 mV(한 방향 · 1 h 내내).
- EIS(그림 11a): 꼭대기 ≈157 ↔ ≈171 Ω cm²(+9 %) · 극소 ≈446–450 ↔ ≈456–457 · 10 mHz 끝 ≈(510, 27) ↔ ≈(503, 23) — 본문 "reasonable agreement".

## 3. 재풀이 폐합 — 인쇄 표 그대로 저자 그림이 나오는가 (`[재현]` — 우리 수치 풀이 · 저자 코드 아님)

| 부분계 | 우리 재풀이(표 3 그대로) | 저자 그림 | 판정 |
|---|---|---|---|
| 전해질 1C (식 23–25 · 정상 상태) | Nernst −3.82 · Galvanic −70.02 · 합 −73.84 mV · c(0) 42.07 · c(L) 36.15 kmol m⁻³ · 벌크 장 18.8 kV m⁻¹ | 그림 6c −3.3 · −69.8 · −73.4 · 6a 두 끝 ≈42 · ≈36 · 6b 벌크 ≈18–20 | ✅ ±0.5 % |
| 전해질 4C | −15.92 · −280.81 · −296.73 · c(0) 50.66 · c(L) 26.97 · 벌크 75.1 | 6f −13.7 · −280.7 · −295.1 · 6d ≈50 · ≈27 · 6e ≈75 | ✅ |
| k_r 감도 | ×0.1 → 1C −87.2 mV · 4C c(L) < 0(고갈) | — | **인쇄 k_r 이 그림을 닫는다**(91호 ×100 과 반대) |
| 벌크 옴 | σ 1.110×10⁻⁶ S cm⁻¹ → L/σ 326.2 Ω cm² | 그림 11b Z_mt^LiPON 호 축 닿음 ≈327 | ✅ |
| 양극 계면 R_ct^p(x 0.80) | RT/(F i₀ᵖ) 67.1 Ω cm² | 11c 청록 ≈67.3 | ✅(x 는 G4) |
| 음극 계면 R_ct^n | 43.9 Ω cm² | 11c 자홍 축 교차 ≈44.0 | ✅ |
| 직렬 | ρ_s 18.3 | 11c Z_s 18.25 | ✅ |
| 합 | 18.3 + 326.2 + 43.9 + 67.3 = 455.7 | Z_bat 극소 ≈457 | ✅ |
| 양극 BV 방전 중간(식 8 · 농도비 포함 · x 는 그림 7 판독) | 1C −15.5 · 4C −63.1 mV | 9e 청록 4C −61.1(1C 겹침 ≈−17) | ✅ |
| **음극 BV 방전 중간** | 물리 방향 +36.8(4C) · 농도비 없이 34.0 · **글자 그대로 −23.8** | 9e 자홍 **−23.9** | **글자 그대로와만 ✅** |
| **음극 이완 영전류 값** | ±(RT/F) ln(c(0)/c̄) = 6.2–6.5 mV(부호는 그리는 규약과 방향에 따라) | 9f 삽도 자홍 **≈+5 mV(0 위)** · 방전 중은 음수 | **글자 그대로와만 ✅** |
| **음극 저주파 고리(소신호 Gerischer)** | 물리: 축 위 · 끝(10 mHz) (52.3, +2.1) · 극한 53.1 / **글자 그대로: 축 아래 · 최저 (38.1, −3.2) · 끝 (35.6, −2.1) · 극한 34.8** | 11c 자홍 유도성 고리 최저 ≈(38.3, −3.4) · 끝 ≈35.6 | **글자 그대로와만 ✅** |

## 4. ★ 음극 계면의 방향 (D1) — 무엇이 확정이고 무엇이 아닌가

- **확정(인쇄)**: 식 (10) 은 Li 산화를 양으로 쓴다 · 식 (12) · (16) 은 두 계면 ODE 의 우변을 같은 `j_bat − j_geo` 로 쓴다 · 식 (8) 규약(산화 양)이면 방전 중 j_bat < 0 · 수송 경계 (18.3) 와 본문 p. 10 은 방전 중 Li⁺ 가 y = 0 에서 **들어간다**고 쓴다(음극 산화).
- **확정(`[재현]` · `[도표·화소]`)**: 그림 9e(방전 중간 크기) · 9f 삽도(이완 부호) · 11c(저주파 고리의 방향 · 최저 · 끝) 셋이 **식 (12) · (16) 을 글자 그대로 넣어 음극을 환원으로 푼 계산**과 정량으로 맞고, 물리 방향과는 셋 다 안 맞는다. 셋은 서로 다른 관측(정상 과전압 크기 · 영전류 부호 · 소신호 위상)이라 판독 우연으로 함께 맞기 어렵다(`[해석]`).
- **확정 못 함**: 저자 코드가 실제로 그렇게 구현됐는지(코드 미공개 · G8 · G11) — 다른 구현(예: 이 효과를 내는 다른 부호 조합)이 같은 세 그림을 낼 가능성은 배제하지 않는다.
- **크기**: 성능 결론에는 작다 — 4C 방전 중간 음극 몫 차 13 mV(η_bat −440 mV 의 ≈3 %) · 1C 3.7 mV(판독 폭 안). 그러나 **해석은 뒤집힌다**: 본문이 "the (interface) concentrations develop in such a way that this leads to a reduction in impedance and to an uncommon (inductive) semicircle" 로 물리를 읽은 자리가 이 방향 문제와 같은 서명이고, 물리 방향이면 음극 계면 저주파 응답은 **저항을 키우는 용량성 고리**다(`[재현·대수]`).
- **왜 적합이 못 봤나**: 측정 스펙트럼에서 음극 호는 LiPON · 기하 축전기 호와 같은 대역(τ 비 0.72)에 겹치고, 저주파 고리(±9 Ω cm² · ≈0.01–0.1 Hz — 특성 1/(2πτ_r) 0.019 Hz)는 양극 확산 · 전해질 저주파 고리와 같은 대역이다 — DC 곡선에서는 음극 계면 몫이 작다(4C ≈5 %). 데이터가 이 항의 방향을 갈라 볼 관측이 없다(Q4 · Q5).

---

# ★ (d) 91호와의 계보 — 2011 → (2019) → 2020

`[인쇄]` "we therefore extend our previously developed ASSB model [11,18]" · "Recently, the model developed by Danilov et al. [11] has been extended with an ionic concentration-dependent diffusion coefficient in the positive electrode [18]" — 가운데 편 Kazemi 2019 *Solid State Ionics* 334, 111([18] · 미열람)은 이 위키에 digest 0. 91호 열은 91호 digest 전사.

| 축 | 91호 Danilov 2011 | 이 편 2020 | 바뀜 |
|---|---|---|---|
| 셀 | 자체 제작 평면 박막 · Li₃PO₄ 1.5 µm · LiCoO₂ 320 nm · 공칭 10 µAh · 1 cm²(설계) | **상용** · LiPON 3.62 µm · LiCoO₂ 8.08 µm · 0.7 mAh · 3.36 cm²(직접 측정) | 셀 · 전해질 · 두께 × ≈25 |
| 자료 | 1.6–51.2C 방전 여섯 · 25 ℃ | 0.1–6C 일곱 + 이완 + **EIS 한 상태** · 20 ℃ | AC 추가 |
| 양극 수송 | 단일 Fick D_Li 1.76×10⁻¹⁵ | **쌍극(Li⊕ · e⁻) Nernst–Planck + 공통 β(x)** · D⁰ 1.21 · 5.06 ×10⁻¹³ | 물리 둘 추가(전자 · x 의존) |
| 양극 동역학 | α **0.6 적합** · k₁ˢ 5.1×10⁻⁶ m^2.8 mol^−0.6 s⁻¹(인쇄 단위로 i₀ 151 A — 재현 불가) | α **0.5 고정** · k₁ˢ 1.53×10⁻¹¹ m^2.5 mol^−0.5 s⁻¹(차원 폐합 · i₀ 0.470 mA cm⁻²) | 단위 관례 회복 |
| 음극 동역학 | 무시("for convenience") | **BV** k₂ˢ 1.09×10⁻⁹ + 이중층 | 신설(그리고 방향 문제 — D1) |
| 축전기 | 0(`capacitance` · `double layer` 0 회) | **c^p_dl · c^n_dl · c_geo** | 신설 |
| 직렬 옴 | 항 언급 0(91호 digest 전사 범위) | **ρ_s = ρ_Pt + ρ_Li**("cannot be separately identified") | 신설 |
| 전해질 운반체 | Li⁺ + n⁻("nBO 에 묶인 미보상 음전하" · `vacanc*` 0) | Li⁺ + n⁻(**"associated with a vacancy"** · 그림 2b) | 91호 D15 의 이름 문제에 공공 해석 인쇄 |
| k_r | 0.90×10⁻⁸ 적합(인쇄 · 그림은 ×100 ≈0.90×10⁻⁶) | **8.00×10⁻⁷**(인쇄 = 그림 폐합) | 인쇄 표 폐합 회복 |
| δ · a₀(c₀) | 0.18 적합 · 6.01×10⁴ **NDP 측정** | 0.64 · 61141 **둘 다 무각주(적합)** | 측정 → 적합(1.7 % 차) |
| D_Li⁺ · D_n⁻ · t₊ | 0.90 · 5.10 ×10⁻¹⁵ · 0.15 | 1.73 · 5.69 ×10⁻¹⁶ · 0.233 | 같은 값 0 |
| 용량 스케일 | a_max 2.33×10⁴ = 측정 용량 ÷ (설계 부피 · Δx 0.5) | c_max 3.22×10⁴ = **EMF 용량** ÷ (A · M · Δx 0.5) | 같은 '용량 맞춤' 관행 |
| 평형 곡선 | 네 율(1.6–12.8C) 회귀 외삽(선형 / 2차) | 일곱 율 "mathematical extrapolation"([32, 33] · 방법 미인쇄) | 같은 '같은 데이터 외삽' 관행 · 방법 기술은 줄었다 |
| 식별성 어휘 | 0(NFKC 전후) | `identif*` 4(뜻 있는 것 하나 — ρ 직렬 합) | 한 문장 |
| "전해질 지배" 결론 | "at least half"(이원 가정 몫 ≈71 % — 91호 digest 전사) | LiPON 66–67 % of η_bat(`[도표·화소]`) · `[재현·가정]` 이원 가정 몫 ≈8 % | 결론의 근거가 벌크 옴(EIS 호 지름)으로 이동 |

⇒ **같은 값 0 · 바뀐 물리 일곱(쌍극 · β(x) · 음극 BV · 이중층 둘 · 기하 축전기 · 직렬 옴) · 회복 둘(인쇄 k_r 의 그림 폐합 · k₁ˢ 단위 관례) · 유지 둘(용량 스케일 맞춤 · 같은 데이터 외삽 평형 곡선) · 새로 생긴 것 하나(인쇄 식 (12) · (16) 의 두 계면 같은 우변 — 음극 방향 문제).** 26호는 이 편의 구조를 거의 그대로 이름만 바꿔 썼고(26호 식 (5)–(7) "I_bat = I⁺ = I⁻" — 26호 digest 전사), 이중층 · 기하 축전기는 버렸다(26호 가정 2).

---

# ★ (e) Q4 — 식별성 · 불확실도 어휘 전수 · 아흔 번째 성질

## 1. 어휘 (NFKC · 줄 끝 분철 복원 뒤 · 쪽 머리 · 바닥 제외 · 본문 = 제목 → 사사 앞 · 초록 · 캡션 · 표 포함 | 부록 | 참고문헌)

| 낱말 | 본문 | 부록 | 참고문헌 | 쓰임 |
|---|---|---|---|---|
| `identif*` | 4 | 0 | 0 | ρ_Pt · ρ_Li "cannot be separately identified"(식별성 뜻 하나) · 질소 결합 "can be identified" · 각주 a "Identified by direct measurements" · 이완 중 "the charge-transfer overpotential can still be identified" |
| `uniqu*` · `uncertain*` · `confiden*` · `±` · `residu*` · `RMS` · `correlat*` · `covarian*` · `Hessian` · `bootstrap` · `standard deviation` · `fit*` | **0** | 0 | 0(`Fisher` 2 = 인명) | — |
| `error*` | 0 | 0 | 1(인명 아님 · [17] 제목 "error analysis") | — |
| `sensitiv*` | 1 | 0 | 0 | "a small sensitivity study"(그림 10 — D 바꾸기 둘) |
| `optimi*` | 16 | 0 | 0 | "optimized" 매개변수 · 곡선 · 표 각주 "(non-optimized)" · 초록 "allows for optimizing" |
| `validat*` | 5 | 0 | 0 | 초록 "experimentally validated" · 서론 셋 · "used for model validation" |
| `agree*` | 13 | 0 | 0 | "good agreement" 류(초록 1 · "close" 1 · "reasonable" 1 · "excellent" 1 · "do not agree" 1) |
| `accura*` | 5 | 0 | 1 | "accurately simulate" · "more accurate parameter estimation" · "determined much more accurately" |
| `estimat*` | 2 | 0 | 0 | Put [40] "estimated value" · "parameter estimation" |
| `contact*` | 2 | 0 | 1 | "contact area losses" [15] · "contact losses due to electrode deformation … beyond the scope" |
| `double layer` · `space-charge` · `capacit*` | 21 · 5 · 24 | 0 | 0 · 2 · 1 | — |
| `vacanc*` | 9 | 0 | 0 | n⁻ = 공공 |
| `pressure` · `EIS` · `OCV` · `degrad*`(본문 2 — 서론) · `aging` 1(범위 밖 문장) | 0 · 0 · 0 · 2 · 1 | | | |
| `EMF` · `extrapolat*` · `relax*` | 15 · 3 · 16 | | | |

## 2. 판정 — Q4 0/98 · 아흔 번째 성질

- 이 편의 식별성 내용은 **세 문장**이다: ① ρ_Pt · ρ_Li 직렬 합(올바른 구조적 묶음 — 같은 전류의 직렬 옴은 합만 보인다) ② "when only the DC simulations are used for parameter optimization, the impedance simulations do not agree with the impedance measurements"(비유일성의 **증상** — DC 적합의 해 집합이 AC 와 맞지 않는 점을 포함한다는 관찰 · 그림 · 값 0) ③ "Performing impedance simulations in addition to DC simulations results in much more accurate parameter estimation since more measurement information has been made available"(처방 **선언** — 폭 · 불확실성 · 조건수 0). 셋 다 Q4 의 기준(이 조합이 이 데이터로 유일하게 정해지지 않음을 **계산으로** 보인 편 — 10호 이래)에 닿지 않는다.
- 비식별을 보인 것은 이 편이 아니라 **우리 `[재현]`** 이다: ① 숨은 면적 인자 f_A 가 k · c_dl 에 같은 배수(R·C 불변) ② 음극 호가 LiPON 호와 같은 대역(τ 비 0.72) — 그 항의 **반응 방향**까지 자료가 못 봤다(D1) ③ 26호 쪽에서 D_e⁻ 가 10 자릿수 표류한 방향(D⁰_p · t_e 조합)은 이 편 자료로도 작은 몫(η^p_mt 4C ≈−4 mV).
- **아흔 번째 성질** = **"DC 단독 적합이 AC 를 못 맞춘다는 비유일성의 증상을 한 문장으로 인쇄하고(그림 · 값 0), 처방을 'DC + AC 한 벌 동시 적합 = 더 정확한 추정' 으로 선언한 뒤 같은 자료를 'validated' 라 불렀다 — 그 한 벌(무각주 13 행 + 함수형 미인쇄 β(x) · 같은 율 묶음 외삽 EMF)이 하류에서 '문헌값' 이 됐고(26호), 측정 스펙트럼에서 LiPON 호와 겹치는 음극 계면 항은 반응 방향까지 자료가 보지 못했다."** — 26호 열아홉 번째 성질("평탄을 스스로 계산해 놓고 평탄 위의 점을 값으로 인쇄")의 **원천 쪽 짝**: 26호가 '문헌과 일치' 로 쓴 그 문헌이 같은 곡선의 적합이다.
- 누적 0.5 그대로.

---

# (f) Q1–Q8 — 채움표 칸 (닻 카드 수집 지침)

| Q | 칸 | 이 편 |
|---|---|---|
| Q1 정량 | **해당 없음 — `θ(N)` 0/98** | 조밀 평판(입자 · 공극 0) · 열화 0 · `contact` 2(범위 밖 · [15] 소개) · 층 하나: 숨은 면적 인자(실제 계면/기하)가 k₁ˢ · k₂ˢ(→ i₀)와 c^p_dl · c^n_dl 에 같은 배수로 곱해져 R_ct·C_dl 면적 불변 — 박리 · 거칠기가 들어갈 자리는 '기하 면적당' 상수 이름뿐 |
| Q2 분리 관측 | **없다** | 열화 0 · DC + AC 를 한 벌에 같이 쓴 '관측 추가' 의 ASSB 원형(이중층 · 기하 축전기 포함) — 모드 분리 아님 · 성분 분해(그림 9 · 11b–c)는 모형 배정이고 측정 스펙트럼에서 음극 호는 LiPON 호와 겹친다 |
| Q3 라벨 층위 | **칸 없음 · 층 하나** | "각주 넷 표 — 무각주 13 = 같은 셀 DC 일곱 율 + EIS 한 상태 동시 적합(목적 함수 · 잔차 · 불확실성 0) · β(x) 함수형 미인쇄 · EMF = 같은 율 묶음 외삽 → 하류(26호) '문헌값' · 재풀이 폐합 ✅ 전해질 · 양극 계면 · 호 지름 / 음극 계면은 인쇄 식 (12) · (16) 글자 그대로의 반대 방향(그림 9e · 9f 삽도 · 11c 셋이 정량 일치)" |
| Q4 유일성 | **0/98 — 아흔 번째 성질** | 위 §(e) · 식별성 문장 하나(ρ 직렬 합 — 올바른 묶음) · 누적 0.5 그대로 |
| Q5 기준 전위 | **해당 없음** | Li 금속 음극(기준극 0 · E_Li 기준) · 층 하나: 음극 계면 항(BV + 이중층)이 모형에 처음 들어왔으나 측정 스펙트럼에서 LiPON · 기하 축전기 호와 같은 대역(τ 비 0.72)이고 계산 방향이 인쇄 식 묶음에서 뒤집혔다 — 음극 몫 배정은 모형뿐 |
| Q6 압력 | **해당 없음** | 박막(스택 압력 개념 0) · `pressure` 0 |
| Q7 Li 재고 | **해당 없음 + 공백** | Li 두께 N · 재고 미인쇄 · c_Li 7.64×10⁴ "Predefined"(무한 원천 · 음극 활동도 1) |
| Q8 OCP · 평형 곡선 | **층 하나** | 상용 LCO 박막 · EMF = 일곱 율 "mathematical extrapolation"([32, 33] — 방법 미인쇄) · c_max 가 그 EMF 용량에서 유도(Δx 0.5 — 그림의 x 범위는 0.510–1.000) · 끝 기울기 ≈−72 V/단위 x(0.994–0.998)가 방전 끝 η_d^p 를 정함 · `OCV` · `GITT` 0 |

**누적 ≈20.0 → ≈20.0 (새 칸 0).**

---

# 어휘 집계 — 위 §(e) 1 표가 전부다

텍스트 층 · NFKC(합자 154 복원) · 줄 끝 분철 복원 · 쪽 머리 · 바닥("L.H.J. Raijmakers et al. / Electrochimica Acta 330 (2020) 135147" + 쪽 번호) 제외. `Fisher` 2 회는 참고문헌 [23] · [24] 저자(C.A.J. Fisher)다. `fit*` 0 은 NFKC 뒤 값(NFKC 전 텍스트 층에서는 합자 때문에 `identif*` 도 0 으로 나온다). 앞 에이전트 메모의 "15+1 · 4+1 · 12+1 · 4+1"(본문 + 초록) 셈은 이 실행의 초록 포함 셈 16 · 5 · 13 · 5 와 같다.

---

# 재현 (`[재현]` — 인쇄 수치 · 식 · 그림 좌표로 우리가 계산 · 가정 · 외부 값 표시 · 스크립트는 `scratchpad` 에만)

| # | 무엇 | 입력 | 결과 | 대조 |
|---|---|---|---|---|
| R1 | c_max 유도 | EMF 용량 0.3489 mAh cm⁻² × 3.36 cm² · F · A · M 8.08 µm · Δx 0.5 | **3.222×10⁴** mol m⁻³ | 표 3 3.22×10⁴ ✅ · Δx 0.490 이면 3.29×10⁴(D7) |
| R2 | C-rate ↔ 시간 | 1C = 0.7 mA ÷ 3.36 cm² = 0.2083 mA cm⁻² · 모의 끝 0.2468 · 0.1805 | **71.1 · 13.0 분** | 그림 6c ≈71.6 · 6f ≈13.1 · 7b ≈71 · 7f ≈13 분 ✅ |
| R3 | 용량 기준 | EMF 용량 · 0.1C 끝 표지 | **1.172 · ≥1.09 mAh**(공칭 0.7 의 ×1.67 · ×1.56) | 26호 Q_ideal 1.23 = ×1.05 → 26호 '1C' ×1.76(G2 · D4) |
| R4 | 26호 비 · 조합 | 표 3 ↔ 26호 표 3(digest 전사) | §(a) 2 · 3 | 7/10 ×1.0500 ✅ |
| R5 | 전해질 재풀이 | 식 (23)–(25) · 표 3 · 1C · 4C 정상 상태(유한체적 · 벽 밀집 격자 · BDF) | −3.82 · −70.02 · −73.84 / −15.92 · −280.81 · −296.73 mV · c(0) 42.07 · 50.66 · c(L) 36.15 · 26.97 | 그림 6 ✅ ±0.5 % |
| R6 | k_r 감도 | 같은 풀이 · k_r ×0.1 · ×0.01 | 1C −87.17 · −141.99 mV · 4C 고갈(c(L) < 0) | 인쇄 값이 그림을 닫는다 |
| R7 | 전도도 · 옴 | σ = (F²/RT)δc₀(D_Li⁺ + D_n⁻) | 1.110×10⁻⁶ S cm⁻¹ · L/σ **326.2** Ω cm² · t₊ 0.233 · 1C 옴 68.0 mV | 그림 11b ≈327 ✅ |
| R8 | 반응층 | λ = √(D_amb/(k_d + 2k_r δc₀)) · τ_r · L²/D_amb | **47 nm · 8.46 s · 13.7 h** | 그림 6 의 두 끝 얇은 층 · 9f 이완 ≈0.15 분 |
| R9 | i₀ · R_ct | 식 (9) · (11) | i₀ᵖ 0.470 → 0.376 → 0.094 mA cm⁻²(x 0.51 · 0.80 · 0.99) · R_ct^p 53.7 → 67.1 → 270 Ω cm² · i₀ⁿ 0.575 · R_ct^n 43.9 | 그림 11c ≈67.3 · ≈44.0 ✅ · x(R_ct^p 67.3) = 0.801 · R_ct^p(0.864) 78.3(D8) |
| R10 | 음극 BV 방전 중간 | 식 (10) · α 0.5 · c(0)/c̄ 1.0751(1C) · 1.2947(4C) | 물리 +10.6 · +36.8 · 농도비 없이 9.1 · 34.0 · 글자 그대로 −6.9 · **−23.8** mV | 그림 9e −23.9 ✅(글자 그대로) |
| R11 | 양극 BV 방전 중간 | 식 (8) · x 표면 · 벌크 = 그림 7 판독 · c(L) 재풀이 | −15.5 · −63.1 mV | 그림 9e −61.1 ✅ |
| R12 | 음극 이완 영전류 | j = 0 → e^(fη) = c(0)/c̄ | ±6.5 mV(4C 차단 직후 · 0.5 s 뒤 ≈6.2) | 9f 삽도 ≈+5 ✅(글자 그대로 부호) |
| R13 | 음극 소신호 Gerischer | Z = R_ct ± Z_c/√(1 + iω τ_r) · Z_c = R_ct j₀ (dc/dj)/c̄ = 9.155 Ω cm² | 물리: 극한 53.1 · 10 mHz (52.3, +2.1) / 글자 그대로: 극한 34.8 · 최저 (38.1, −3.2) · 10 mHz (35.6, −2.1) | 그림 11c ≈(38.3, −3.4) · ≈35.6 ✅(글자 그대로) |
| R14 | τ | R·C | τ_n 0.764 µs(208 kHz) · τ_LiPON 1.057 µs(151 kHz) · τ_p 35.6 µs(4.47 kHz) | 음극 호 ↔ LiPON 호 겹침 |
| R15 | 축전기 물리 범위 | c = ε₀ε_r/d | ε_r 13.2 · 42.8 · c^n_dl 등가 0.67–2.2 µm · c^p_dl 22–72 nm | §(b) 3 |
| R16 | 경계 분배 · 쌍극 확산 | 식 (30.3) · (30.4) · D⁰_p | t_e 0.807 · D⁰_p 1.953×10⁻¹³ · 같게 하면 ×0.62 · 26호 ×1.30 · t_e 1.00 | 그림 10 단면 |
| R17 | 이원 가정 몫 | 같은 σ 단일 이온 | 1C 68.0 ↔ 73.84 mV → **≈8 %** · 4C 271.8 ↔ 296.73 → ≈8 % | 91호 ≈71 %(91호 digest 전사) |
| R18 | 벌크 x 기울기 | j/(F c_max M) | 0.004979 · 0.019918 min⁻¹ | 그림 7b · f ≈+1.4 · ≈+2.6 %(D7) |
| R19 | 그림 3 잔차 | 벡터 표지 ↔ 모의 선 보간 | 몸통 RMS 1.2 · 1.8 · 2.0 · 5.1 · 19.1 · 47.6 mV · 끝 비 0.996 … 0.972 | §(c) 2 |
| R20 | 그림 4a 이완 잔차 | 화소 · 잘린 고리 합침 | ≈+22 → +2.5–6 mV | 한 방향 |
| R21 | Li 금속 농도 | 밀도 0.534 g cm⁻³ · 6.941 g mol⁻¹ `[재현·외부 값]` | 7.69×10⁴ | 표 3 7.64×10⁴(−0.7 %) |
| R22 | 6C 용량 몫 | 0.1555 ÷ 0.3489 | 45 % | 본문 "less than half" ✅ |

---

# 참고문헌 42 번호 — 우리 축에 닿는 것 (번호는 PDF p. 18–19 목록에서 직접 확인 · 빠진 번호 0)

| 번호 | 서지(지면 그대로 요약) | 이 편에서 쓰인 자리 | 우리 축 |
|---|---|---|---|
| [11] | Danilov D.L., Niessen R.A.H., Notten P.H.L., *J. Electrochem. Soc.* 158 (2011) A215 | 계보 원형 · BV 유도("For a full derivation … [11]") · n⁻ Nernst–Planck 가정 · E 식 유도 | **91호 = 4차 묶음 파일 51**(흡수됨) |
| [12] | Fabre S.D. 외, *J. Electrochem. Soc.* 159 (2012) A104 | "moderately good agreement" · 농도 의존 D · "[12,35] in agreement"(D_Li⊕) | Q3 · 후속 |
| [15] | Tian H.-K., Qi Y., *J. Electrochem. Soc.* 164 (2017) E3512 | "the effect of contact area losses between the electrodes and electrolyte [15], leading to battery degradation" — 범위 밖 소개 | 원장 ★★★ · 재지목 |
| [16] · [17] | Teichert K., Oldham K. 2017 *JES* 164, A360 · *J. Energy Storage* 14, 94 | 동적 부하 · MEMS — "this might be different for … MEMS [16]" | (b) |
| [18] | Kazemi N., Danilov D.L., Haverkate L., Dudney N.J., Unnikrishnan S., Notten P.H.L., *Solid State Ionics* 334 (2019) 111 | 계보 가운데 편 — "extended with an ionic concentration-dependent diffusion coefficient" | **후속 ★★★** |
| [20] | Landstorfer M., Funken S., Jacob T., *PCCP* 13 (2011) 12817 | 이중층 · 공간전하 고급 모형 후보 | ☆ |
| [21] | Dudney N.J., *Mater. Sci. Eng. B* 116 (2005) 245 | "remarkable longevity … many thousands of cycles" — 노화 무시의 근거 | ☆ |
| [23] · [24] | Aizawa Y. 외 2017 *Ultramicroscopy* 178, 20 · Yamamoto K. 외 2010 *Angew. Chem.* 49, 4414 | 이중층 물리 귀속(n 쪽 이동 Li⁺ · p 쪽 Li⁺ 공공 [23]) — 전자 홀로그래피 전위 측정 | (b) · 후속 ★ |
| [25] | Braun S., Yada C., Latz A., *JPCC* 119 (2015) 22281 | 공간전하층 열역학 모형 | (b) · 재지목(54호) |
| [26] | de Klerk N.J.J., Wagemaker M., *ACS Appl. Energy Mater.* 1 (2018) 5609 | "also been concluded by others [26,42]" — 공간전하 작다 | (b) · G12 |
| [28] | Danilov D., Notten P.H.L., *Electrochim. Acta* 53 (2008) 5569 | 식 (23)–(24) · (31) 유도("see Refs. [11,28]") | **4차 묶음 파일 61**(101호 예정) |
| [29] | Xia H., Lu L., Ceder G., *J. Power Sources* 159 (2006) 1422 | 고체 확산의 국소 환경 의존 [29–31] | Q3 · 후속 ★ |
| [31] | Xie J., Imanishi N., Matsumura T., Hirano A., Takeda Y., Yamamoto O., *Solid State Ionics* 179 (2008) 362 | 같은 자리 [29–31] | **4차 묶음 파일 62**(102호 예정) |
| [32] · [33] | Li D., Danilov D.L., Xie J., Raijmakers L., Gao L., Yang Y., Notten P.H.L. 2016 *EA* 190, 1124(calendar) · Li D., Danilov D., Gao L., Yang Y., Notten P.H.L. 2016 *EA* 210, 445(cycling) — "Degradation mechanisms of C6/LiFePO4 batteries" | **EMF 외삽 방법의 출처**("details can be found in previous publications [32,33]") | Q8 · (체) · **모드 축(LFP 노화)** — 후속 ★★★ |
| [34] | Reimers J.N., Dahn J.R., *JES* 139 (1992) 2091 | "second hexagonal phase [34]" — 그림 5 꺾임 | 원장 ★ · 재지목 |
| [35] | Larfaillou S., Guy-Bouyssou D., Le Cras F., Franger S., *J. Power Sources* 319 (2016) 139 | "[12,35] in agreement"(D_Li⊕) | 10호 ★ · 지목 누락 보충 |
| [37]–[39] | Molenda 1989 *SSI* 36, 53 · Menetrier 1999 *J. Mater. Chem.* 9, 1135 · Imanishi 1999 *SSI* 118, 121 | LCO 전자 전도도 x 의존 — D_e⁻(x) 정성 대조 | ☆–★ |
| [40] | Put B., Vereecken P.M., Stesmans A., *J. Mater. Chem. A* 6 (2018) 4848 | "estimated value of 40 kmol m⁻³" — δc₀ 대조 | (a) · 후속 ★ |
| [41] | Zhang X., Verhallen T.W., Labohm F., Wagemaker M., *Adv. Energy Mater.* 5 (2015) 1500498 | 그림 10f 거울 단면 "demonstrated experimentally"(LFP NDP) | (c) · 후속 ★ |
| [42] | Haruta M. 외, *Nano Lett.* 15 (2015) 1498 | 공간전하 작다(실험 쪽) | (b) · 후속 ★★ |
| [1]–[10] · [13] · [14] · [19] · [22] · [27] · [30] · [36] | 종설 · 일반 모형 · Vetter 교과서 · LiPON 전자 전도도 · LixCoO2 삽입 · SE 종설 | 서론 · 배경 | ☆ |

---

# 인용 대조

## 1. 이 편을 인용한 우리 digest — 그 쓰임 ↔ 이 편이 실제로 주는 것

| digest | 쓰임(digest 전사) | 이 편 | 판정 |
|---|---|---|---|
| **26호** Iwakiri 2024 [10] | 데이터(네 율 · 98 점) · "문헌값" 10 · 평형 곡선 · β 의 단일 출처 · "consistent with … literature" · "not fed into the optimization algorithm" | 데이터 ✅(일곱 율 중 넷) · 문헌값 = 적합 9 + EMF 유도 1 · 평형 곡선 · β = 그림뿐 | **"문헌과 일치" = 같은 자료 두 적합의 일치** · 26호 G4 '예' · G5 그림으로만 · G2 의 데이터 쪽 전제(1C = 0.7 mA) 확인 · 26호 ρ 18.3 고정 = 이 편 적합값 |
| **37호** Li 2024 [14] | "이중층 항의 조상(`[인쇄]` 'integrating the electrical double layer capacitance … geometrical capacitance')" · 후속 "c_dl 이 면적에 비례하는가" | 조상 = 기하 면적당 축전기 · 실제 계면 0 · 값 적합 | 표 각주 글자 셋 상속 · 값 · 면적 규약 상속 0 · 37호 F 꼴은 변형 |
| 91호 Danilov 2011 | 교차 참조(지목 아님) — "`k_r` 8.00×10⁻⁷ · δ 0.64 · a₀ 61 141 · `D_e⁻` · `c_dl` 의 출처" · "Raijmakers 의 `k_r` 가 이 편의 인쇄 값이 아니라 다른 경로" · "37호 c^p_dl 5.1×10⁻⁶ ↔ k₁ˢ 5.1×10⁻⁶ — 파일 58 에서 같이 본다" | k_r · δ · c₀ = 이 편 셀의 적합 · c_dl 적합 · 5.1 없음 | 91호의 물음 둘이 닫힌다: k_r 은 다른 셀 · 다른 전해질의 재적합(인쇄 = 그림) · 5.1 은 이 편 경유 상속 아님 |
| 92–96호 · 27호 | "4차 묶음 13 편과의 관계" · "인용하지 않는 것" 목록 | — | 언급만 |

## 2. 이 편이 인용한 우리 digest

- **[11] = 91호**(흡수됨) — 이 편의 쓰임: BV 유도 · n⁻ Nernst–Planck 가정 · E 식 유도 · 계보 원형("we therefore extend our previously developed ASSB model [11,18]"). 91호의 D15(n⁻ 이름)에 이 편이 공공 해석을 인쇄했고, 91호 `k_r` 인쇄 ×100 문제는 이 편 표에서 반복되지 않는다(91호 digest 전사 대조).
- 4차 묶음 13 편 중 인용: **[11](파일 51 · 91호) · [28](파일 61 Danilov & Notten 2008) · [31](파일 62 Xie 2008)** — 나머지 열(Firouz · Bielefeld · Schmidt · Khalik · Lu · Koerver 2018 · Kim 2019 · Deng 2021 · Shao 2022 · Ansah 2021) 인용 0(42 번호 전수 대조 — 대부분 이 편보다 뒤).

---

# 곱 축퇴 처방 — 여든한 번째 적용 ([[assb-lampe-contact-product-degeneracy]])

⚠ 이 편은 접촉 · 노화 0 인 신품 모형 편이다 — 처방의 입력 점검은 대부분 ❌ 이고, 남는 것은 **곱의 자리가 계보 모형에 어떻게 박혀 있는가** 다.

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계**(16호) | `R` 과 `C` 를 같이 | ✅ 형식 — 두 계면 R_ct(BV) + c_dl · EIS 한 상태와 DC 를 한 벌로 | ⚠ c_dl 은 **기하 면적당 적합값** · 음극 호는 측정에서 LiPON · 기하 축전기 호와 겹친다(τ 비 0.72) · 면적 변화 · 노화 0 → 'C ∝ 면적' 을 시험할 자료 없음 |
| **2단계**(18 · 25호) | + 면적을 아는 대조군 | 평판 박막 = 기하 면적 계면(3.36 cm² 직접 측정 · 거칠기 미검사) · 셀 수 미인쇄 | ⚠ 재료만 — i₀ᵖ 0.470 mA cm⁻²(x 0.51) · c^p_dl 0.53 µF cm⁻² 이 '면적을 아는 평판' 의 적합 자릿수(측정 아님) |
| **3단계-a**(19호) | `Ea` | 20 °C 한 점 | ❌ |
| **3단계-b**(19호) | `C` 물리 상한 | c_dl 값만 · `[재현·가정]` 등가 유전 두께 c^n_dl 0.67–2.2 µm · c^p_dl 22–72 nm | ⚠ 우리 계산 — c^n_dl 이 공간전하층 범위 밖 |
| **4단계**(20 · 24호) | 시간 영역 | 이완 2 h(그림 1 h) · 6 율 — 적합 자료였는지 미인쇄 | ⚠ |
| 처방 표 "율 스윕" | 여러 율 | 일곱 율 — 외삽 EMF(정적)에 씀 | ⚠ 다른 질문 |
| 처방 표 "`J^T J` 최소 고유벡터" | 적합점 야코비안 | 0 | ❌ |

## ★ 곱 문장 — 셋 (`[인쇄]` → `[해석]`)

- 식 (9) "j^p_0 = F k₁ˢ c^max (…)" · 식 (11) "j^n_0 = F k₂ˢ (…)" — 전류는 **기하 면적 A**(각주 a 직접 측정)로 나눈 밀도이고 실제 계면 면적 변수는 없다 → 거칠기 · 부분 박리는 **k₁ˢ · k₂ˢ 의 이름으로** 들어간다(26호 §2-2 `[추론]` 과 같은 자리 · 91호 식 8 의 `A·k₁ˢ` 와 같은 곱).
- 표 2 "c^i_dl — Double layer capacity **per unit area** of electrode i" — 같은 숨은 면적 인자가 c_dl 에도 곱해진다 → **R_ct·C_dl 면적 불변**(`[재현·대수]`) — 처방 1단계가 면적 손실을 'R ↑ · C ↓ 같은 비' 로 읽으려면 c_dl 이 실제 계면 면적에 비례한다는 **truth 쪽 전제(R5)** 가 필요하고, 이 조상은 그 전제를 형식으로만 갖는다(기하 면적 하나).
- 각주 d "Calculated from the EMF voltage curve" — 용량 스케일 c_max = EMF 용량 ÷ (F·A·M·Δx 0.5)(`[재현]` 3.222×10⁴) → 활성 분율 · 접촉 몫이 있으면 이 한 수에 섞인다(`θ·Q` 자리 — 91호 a_max 와 같은 관행).
- ⇒ 처방 표에 **새 줄은 없다**. 후보 메모 하나: "축전기 항의 면적 기준(기하 · 실제 계면 · 전극 전체)과 물리 범위(등가 유전 두께)를 값 옆에 적는다" — 새 판단 거리 셋째로 넘긴다.

## ⚠ 이것이 곱을 푼 것은 아니다

- 열화 · 접촉 · 온도 · 면적 대조가 모두 0 이다 — 위 자리는 **모형 구조**이고 측정이 아니다. 등가 두께는 ε_r 를 c_geo 에서 역산한 가정(LiPON 만 ↔ LiPON + LCO) 위의 `[재현·가정]` 이다.

---

# 보류 결정 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(햐) · (겨) — 이 편이 주는 근거 (결정 안 함)

| # | 결정 (요약) | 98호 근거 | 세기 |
|---|---|---|---|
| **(세)** | 인쇄 매개변수 표의 재풀이 폐합 검사 | 계보 뒤 편(26호)이 '문헌값' 으로 가져간 **바로 그 표**를 재풀이: ✅ 전해질(1C · 4C ±0.5 %) · k_r 인쇄 = 그림(91호 ×100 과 반대) · 벌크 옴 · R_ct 둘 · 직렬 · 합 / ❌ 음극 계면 방향 — 인쇄 식 (12) · (16) 글자 그대로의 계산과 그림 셋이 정량 일치(D1) · 그리고 크기 폐합만으로는 못 잡고 **부호 · 저주파 위상** 대조에서 잡혔다 | **강** |
| **(먀)** | 다른 편 현상의 '모형 원전' 지목 때 기구 층위 확인 | 37호 "이중층 항의 조상" → 조상은 기하 면적당 축전기(실제 계면 0 · 값 적합) · 37호 F(전극 전체) 꼴은 변형 · 수치 상속 0 · 각주 글자 셋만 상속 / 26호 "데이터 · 문헌값 · β" → 9 적합 + 1 EMF 유도 · 측정 0 | **강** |
| **(체)** | 평형(OCV) 곡선의 출처 층위 표기 | EMF = 일곱 율 "mathematical extrapolation"([32, 33] · 방법 미인쇄) · c_max 가 그 EMF 에서 유도 · 26호 "Nernst curve … extracted from the same paper" · 끝 기울기 ≈−72 V/단위 x 가 방전 끝 η_d 를 정함(외삽 영역) | **강** |
| **(제)** | 모형 "일치" 주장의 율별 끝 용량 잔차 표기 | "good agreement … across the wide range" ↔ 끝 용량 0.996 · 1.005 · 0.998 · 0.989 · **0.972 · 0.972** · 4C · 6C 첫 1–2 분 −45 … −103 mV · 몸통 RMS 1.2–47.6 mV | **강** |
| **(대)** | C-rate 기준 용량 표기 | 1C = 0.7 mA(공칭) ↔ EMF 1.172 mAh(×1.67) · 0.1C ≥1.09 mAh · 시간 폐합(71.1 · 13.0 분)으로 데이터 1C 확정 · 26호 Q_ideal 기준이면 ×1.76 | **강** |
| **(햐)** | '계산 ↔ 실험 일치' 의 측정 몫 · 비교 축 | 'validated' 의 비교 축 = 적합 자료 ↔ 같은 자료(표본 안) · 26호 '문헌과 일치' 의 비교 축 = 같은 자료 두 적합 | **강** |
| (에) | 속도 상수의 i₀ 환산 표기 | k₁ˢ 단위 m^2.5 mol^−0.5 s⁻¹(α 0.5 · 식 (9) 차원 폐합) → i₀ᵖ 0.470 · 0.376 · 0.094 mA cm⁻²(x 0.51 · 0.80 · 0.99) · k₂ˢ → i₀ⁿ 0.575 · 26호 단위 표기 "mol^0.5"(26호 digest 전사) · 91호 α 0.6 판과의 대조 | 중 |
| (이) | 모형 값 인용 규칙 | 표 3 무각주 13 = 모형 입력이 측정이 아니라 같은 셀 적합 · 26호가 '문헌값' 으로 입력 | 중 |
| (치) | 모형 결론 옆 '배제 가정' 표기 | "LiPON 지배" — 이원 가정 몫 ≈8 %(벌크 옴이 EIS 로 닻) · "공간전하 작다" — 축전기 모형 선택의 귀결(대역 논증) · "D 같으면 성능 ↑" — 공통 β 가정 위 | 중 |
| (냐) | 모형 결론 회고 인용 — 조건 복원 | 26호가 이 편 값을 조건(같은 셀 · AC 포함 적합 · 이중층 포함 모형) 없이 '문헌값' 으로 · 37호가 '조상' 으로(면적 규약 변경 무언급) | 중 |
| (뱌) | 재매개화 · 묶음의 최소성 표기 | 항등으로 줄인 것: ρ_Pt + ρ_Li → ρ_s(인쇄 — 직렬 합) / 가정으로 줄인 것: D_Li⊕ · D_e⁻ 공통 β(식 27 — 비 상수) · α 0.5 고정 / 남은 곱: 면적 × k · 면적 × c_dl(`[재현·대수]`) | 중 |
| (쟈) | '식별 가능' 주장의 층 표기 | 구조적: ρ 직렬 합(인쇄 · 올바름) · 실제적: "DC 만으로는 AC 안 맞음"(관찰 문장 · 값 0) · 선형 소신호: EIS 를 썼으나 식별 분석 0 | 중 |
| (챠) | 최종 매개변수 표 ↔ 물리 범위 폐합 | c^n_dl 등가 유전 두께 0.67–2.2 µm(공간전하층 범위 밖) · β 는 작동 창 어디서도 1 아님(D⁰ 는 어느 x 의 D 도 아님) · c_Li 7.64×10⁴ ↔ 밀도 7.69×10⁴ ✅ · 경계 · 초기화 인쇄 0 | 중 |
| (베) | 시간분해 EIS 의 측정 상태 표기 | EIS "3.9 V" 정전위 ↔ 모의 무바이어스 · x 미인쇄 · R_ct^p 67.3 ↔ x 0.80(EMF 3.910) · EMF 3.900 = x 0.864(78 Ω cm²) — 평탄 구간이라 같은 '3.9 V' 가 R_ct^p 를 15 % 흔든다 | 중 |
| (루) | SOC 축 신품 j₀(x) 기준선 | R_ct^p(x) 53.7 → 67.1 → 270 Ω cm²(x 0.51 → 0.80 → 0.99 · ×5) — 노화 없이 측정 상태만으로 계면 저항이 이만큼 움직인다는 박막 표본 | 중 |
| (겨) | 처방 효과의 측정 여부 표기 | "the battery performance increases significantly if the ionic and electronic diffusion coefficients are identical"(결론) — 모의만(그림 10c 삽도 ≈+9 %) · 측정 0 | 중 |
| (다) | 28호 액체 도구를 ASSB Q4 분모에 | ASSB 추정 계보의 가운데 편도 식별성 도구 0 — 분모에 'ASSB 계보 0' 한 점 더 | 약 |
| (차) | PyBaMM 면적 노브 / j₀ 노브 분리 forward | DC 만이면 면적 × k 한 곱 · EIS 를 더해도 c_dl 이 같은 면적 인자를 받아 R·C 불변 — 두 노브를 가르는 둘째 서명은 'c_dl 이 실제 계면에 비례' 라는 truth 전제에서만 생긴다 | 약 |
| (무) | j₀(x) 모양 선택지 | √(x(1−x)) 꼴(α 0.5 고정 · k 만 적합) — PyBaMM `Chen2020` 계열과 같은 꼴의 박막 표본 하나 | 약 |
| (탸) | 요약 수치 ↔ 같은 편 표 · 축 | 초록 · 실험 절 "0.7 mAh" ↔ 그림 3 EMF 1.172 mAh — 공칭 표기와 측정 용량을 한 지면이 대조하지 않음 | 약 |
| (가) | 29호 Q4 +0.5(정적 ↔ 동적) | 율 외삽 EMF 로 정적을 정의 — 91호와 같은 관행(약한 표본) | 약 |
| (피) | DRT 창 밖 봉우리 | DRT 0 · 음극 유도성 고리의 τ_r 8.46 s(0.019 Hz)는 창 안이나 10 mHz 끝에서 고리가 덜 닫힘(35.6 ↔ 극한 34.8) | 약 |
| (캬) | DRT 봉우리 → 전극 배정 | 호의 전극 배정이 모형 성분 분해뿐(그림 11b · c) · 음극 호와 LiPON 호 τ 비 0.72 | 약 |
| (헤) | 측정 입력의 역모형 층위 | T · A "Identified by direct measurements" · L · M SEM(그림 0) · c_max = EMF 용량의 역모형(Δx 0.5 가정) | 약 |
| (메) | 예치 원자료 교차 폐합 | 예치 0 → 지면 폐합: ✅ R1 · R2 · R5 · R7 · R9 · R16 · R21 · R22 / 방향 문제 R10 · R12 · R13 | 약 |
| **(마)** | 37호 "ASSB truth 5조건" 개념 분리 — **결정 · 반영(2026-09-23)** | **이 편이 (마) 의 '닿는 논문' 목록에 직접 있다(Raijmakers 2020)** — R5 의 조상 쪽 근거(기하 면적당 c_dl · 실제 계면 0) | 결정 유지 — 근거 추가 |

나머지 — (라)(바)(사) 결정 · 반영됨(이 편 근거 0), 그 밖의 글자는 **근거 0**(압력 · 기준극 · 3전극 · 노화 사이클 · LLI 실측 · θ 판정 · 상 분율 · 입도 · 피복률 · 프로토콜 비교 · 원자료 예치 · 다중 시작이 이 편에 없다). **결정 안 함.**

## 새 판단 거리 (넷 — 글자는 호출자가 붙인다)

1. **계면 반응 방향(부호 규약)의 재풀이 폐합** ((세) 의 부호판으로 묶어도 됨) — 모형 편의 식 묶음 · 성분 분해를 카드 · 개념 · 합성 truth 로 옮기거나 구현하기 전에, 각 계면 동역학이 수송 경계와 같은 반응 방향으로 풀리는지(두 계면에 같은 `j` 를 쓰는 식 · 산화 양 규약)를 확인하고, 재풀이 대조를 크기뿐 아니라 부호(이완 영전류 값) · 저주파 위상(용량성 ↔ 유도성)까지 해 결과를 적게 할지 — 98호: 인쇄 식 (12) · (16) 이 두 계면에 같은 `j_bat` → 음극이 방전 중 환원으로 계산 · 그림 9e(−23.9 ↔ −23.8 mV) · 9f 삽도 이완 부호 · 11c 유도성 고리(최저 · 끝) 셋이 정량 일치 · 저자는 그 고리를 물리("uncommon (inductive) semicircle")로 읽음.
2. **'문헌값 일치' 의 자료 독립성 표기** ((냐) · (햐) · (이) 의 하위로 묶어도 됨) — 추정 편의 "문헌값과 일치 · 문헌 범위 안" 을 식별 · 검증 근거로 옮기기 전에, 그 문헌값이 같은 자료(같은 셀 · 같은 곡선)의 적합인지 · 측정인지 · 다른 셀의 적합인지를 원 편 각주 · 본문으로 확인하고, 같은 자료면 "같은 자료 두 적합의 일치" 로 표시하게 할지 — 98호: 26호 '문헌값' 10 중 9 = 이 편 무각주 적합(같은 셀 · DC 일곱 율 + EIS) · 1 = 같은 율 묶음 외삽 EMF 의 유도 · 26호 ρ 18.3 고정 = 이 편 적합값.
3. **축전기 항(이중층 · 기하)의 면적 기준 · 물리 범위 · 출처 표기** ((차) · (마) R5 의 하위로 묶어도 됨) — c_dl · c_geo 를 합성 truth · 처방 1단계로 옮길 때 면적 기준(기하 면적당 · 실제 계면당 · 전극 전체)과 등가 유전 두께(ε_r 가정 포함) 같은 물리 범위 대조, 출처 층위(측정 · 적합)를 값 옆에 적게 할지 — 98호: c_dl 기하 면적당 F cm⁻² · 숨은 면적 인자가 k · c_dl 에 같은 배수(R·C 불변) · c^n_dl 등가 0.67–2.2 µm · 무각주 적합 · 37호 F(전극 전체) 꼴은 조상에 없는 변형.
4. (선택) **"validated" 의 자료 층위 표기** ((제) · (햐) 의 하위로 묶어도 됨) — 모형 편의 'validated · validation' 을 카드 · 개념으로 옮길 때 그 자료가 적합에 들어갔는지(맞춘 자료 ↔ 보류 자료 · 이완 · 다른 상태)를 같이 적게 할지 — 98호: "Since both DC and AC impedance measurements are used for model validation, it is to be expected that the model parameters can be determined much more accurately" — 같은 자료가 검증이자 결정 · 보류 자료 0 · 이완의 적합 여부 미인쇄.

---

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** ★★★★ | 음극 계면 반응 방향 — 식 (10)(Li 산화 양) · (18.3) · 본문 p. 10(방전 중 Li⁺ 가 y = 0 에서 들어감) ↔ 식 (12) · (16)(두 계면 같은 `j_bat − j_geo`) → 글자 그대로면 방전 중 음극을 환원으로 계산 · 그림 9e · 9f 삽도 · 11c 셋이 글자 그대로의 계산과 정량 일치 · 본문은 유도성 고리를 물리로 읽음 | §(c) 3–4 · R10 · R12 · R13 |
| **D2** ★★ | (18.3) J_Li⁺(0) = −j^n_ct/(zF) ↔ (18.4) J_Li⁺(L) = +j^p_ct/(zF) — 같은 우변(식 12)에 반대 부호 → 정상 상태 보존(J(0) = J(L))과 안 맞음 | 식 렌더 |
| **D3** ★ | (23.3) · (23.4) 가운데 항 j/(zF) 는 플럭스 차원 — 기울기 식의 중간 등호가 차원으로 성립하지 않음(마지막 항 j/(2FD) 는 맞음) | 식 렌더 |
| **D4** ★★ | (5) · (6) "− η^LiPON_mt − η^n_ct" ↔ (25) 의 η^LiPON_mt(방전 중 음수 — 그림 6c · f) · 그림 9 는 모든 과전압을 더해 쌓음 — 인쇄 합산 규약과 그림 규약이 다름 | 식 (5) 렌더 · 그림 9 범례 |
| **D5** ★ | (28.3) · (29.4) 에서 유도한 (30.3) · (30.4) 의 부호가 인쇄와 반대 — p 안에서 둘이 함께 뒤집혀 분배는 일관하나 `j` 의 부호 규약이 식 묶음 사이에서 바뀜 | 쪽 8 렌더 · `[재현·대수]` |
| **D6** ★★ | "capacity of 0.7 mAh" · 1C = 0.7 mA ↔ 같은 지면 EMF 용량 1.172 mAh · 0.1C ≥1.09 mAh — 공칭 ↔ 측정 용량을 지면이 대조하지 않음 | 그림 3 · R3 |
| **D7** ★ | c_max 의 Δx 0.5(식 (1) "0 ≤ x ≤ 0.5" · `[재현]` 3.222×10⁴) ↔ 그림 7 · 8 의 x 0.510–1.000(Δx 0.490 → 3.29×10⁴) · 벌크 x 기울기 그림 ≈+1.4 · +2.6 % | R1 · R18 |
| **D8** ★★ | EIS "Potentiostatic … at a voltage of 3.9 V" ↔ 그림 11c R_ct^p ≈67.3 = x ≈0.80(EMF 3.910 V) · EMF 3.900 V = x 0.864 → 78 Ω cm² · 모의 상태 미인쇄 | R9 · G4 |
| **D9** ★★ | 그림 10e 삽도 모의 선이 ≈0.246 mAh cm⁻² · ≈3.74 V 에서 끝남(컷오프 0) · 본문 언급 0 | 그림 10 확대 |
| **D10** ★ | 그림 4 이완 축 1 h ↔ 본문 2 h · 0.1C 판 없음 · "in good agreement … during the entire relaxation time under all conditions" ↔ 0.2C 한 방향 잔차 ≈+22 → +2.5–6 mV | 그림 4 · R20 |
| **D11** ★★ | "the agreement … is good across the wide range of investigated C-rates" ↔ 4C · 6C 첫 1–2 분 −45 … −103 mV · 끝 용량 0.972 | 그림 3 · R19 |
| **D12** ★ | p. 15 "Impedance measurements (blue) and simulations (red)" ↔ 그림 11a 모의 = 검정(같은 쪽 다음 문단 "simulated (black line)") | 그림 11a |
| **D13** ★ | "The charge-transfer overpotential at p is larger than at n because the reaction rates are faster at n" ↔ `[재현]` i₀ⁿ/i₀ᵖ 1.22–1.53 뿐 · 그림의 n ↔ p 차의 일부는 D1 의 방향(농도비가 n 쪽 |η| 를 줄임) | R9 · R10 |
| D14 | 그림 2 범례 "Chairs of Phosphates"(Chains 의 오기로 읽힘) | 그림 2 |
| D15 | x 두 뜻 — 식 (1) "(0 ≤ x ≤ 0.5)"(뽑아낸 양) ↔ 그림 5 · 7 · 8 "x in LixCoO2"(0.5–1.0) | 식 (1) · 그림 |
| D16 | 표 2 아래첨자 목록 "Li⁰" ↔ 본문 · 그림 2 "Li_o" | 표 2 |
| D17 | 부록 A 에서 L(본문 LiPON 두께)이 LCO 영역 길이로 · c₀(본문 LiPON 자리 농도)가 초기 농도로 재사용 | 부록 A |
| D18 | 표 2 단위 F m⁻² · Ω m² ↔ 표 3 · 그림 11 F cm⁻² · Ω cm² — 표기(값 오류 아님) | 표 2 · 3 |
| D19 ★ | 초록 "generally applicable to all-solid-state batteries" · 4.4 "the electrolyte is the dominating factor in the performance limitations of ASSB" ↔ 시험은 상용 LiPON 박막 한 종(셀 수 미인쇄) | 초록 · p. 13–14 |

---

# 이 편이 우리 프로젝트에 주는 것 (정리)

- **26호 '문헌과 일치' 의 정체가 닫혔다** — 같은 셀 · 같은 곡선의 이 편 적합(아홉) + 같은 율 묶음 외삽 EMF 의 유도(하나). '문헌값과의 일치' 는 식별의 독립 근거가 아니라는 우리 `degradation-degeneracy/` 의 물음("곡선이 맞는다 ≠ 매개변수가 맞다")의 **계보 원천 쪽 표본**이다(우리 수치는 `degradation-degeneracy/docs/RESULTS*.md` 정본 — 옮기지 않음).
- **"관측 추가(DC + AC)" 의 ASSB 원형** — 이 편은 EIS 를 더하면 추정이 더 정확해진다고 **선언**했지만 식별 분석은 0 이고, 더한 관측(EIS)이 실제로 가른 것(벌크 옴 → 전해질 결론)과 못 가른 것(음극 계면 — LiPON 호와 같은 대역 · 방향까지)을 우리 재풀이가 갈랐다. 우리 쪽 '관측을 더해 축퇴를 푸는가' 물음의 한 사례 — **더한 관측이 같은 대역에 겹치면 그 항은 여전히 모형 배정이다**.
- **합성 truth 구현 경고** — 계보 모형을 truth 로 이식할 때 인쇄 식 (12) · (16) 을 글자 그대로 옮기면 음극 반응 방향이 뒤집힌다(D1). 크기 폐합 검사로는 1C 에서 안 보이고 4C · 이완 부호 · 저주파 위상에서 보인다 — 새 판단 거리 1.
- **37호 R·C 처방 전제(R5)의 조상** — 조상은 c_dl 을 기하 면적당으로 두고 실제 계면 면적을 모형에 두지 않았다 → 'C ∝ 실제 접촉 면적' 은 조상에서도 시험되지 않은 전제다. 처방 1단계를 합성 자료로 시험하려면 truth 쪽에서 c_dl 을 실제 계면 면적에 묶어야 한다(R5 그대로 · 근거 추가).
- **C-rate 기준** — 데이터 1C = 0.7 mA(공칭)가 시간 폐합으로 확정 · EMF 용량은 ×1.67 — 26호 구현이 Q_ideal 기준이면 전류 ×1.76(26호 지면으로 미확정).
- **이 편이 주지 않는 것**: 노화 · 접촉 · 압력 · LLI · LAM · 기준극 · 셀 수 · 원자료 · 코드 — 그리고 98 편 누적 `θ(N)` 0.

---

# 후속 후보 (원전 우선 — 지목 수는 위키 digest 의 후속 절 grep 으로 센 값)

| 등급 | 서지 (PDF 목록 번호) | 지목 (후속 절) | 왜 | 축 |
|---|---|---|---|---|
| ★★★ | **Kazemi N., Danilov D.L., Haverkate L., Dudney N.J., Unnikrishnan S., Notten P.H.L. 2019** — "Modeling of all-solid-state thin-film Li-ion batteries: accuracy improvement", *Solid State Ionics* **334**, 111–116 ([18]) | 98 = **1**(새 — 12호 본문 · 37호 [13] "Kazemi" 는 후속 절 밖 · 37호 [13] 이 같은 편인지 서지 미전사) | 계보 **가운데 편**(91 → 2019 → 98) — 농도 의존 D 를 처음 넣은 편 · 그 매개변수 표 · 자료(같은 상용 셀인가) · 적합 방법 — 26호 '문헌값' 계보의 바로 앞 단계 | Q4 · Q3 |
| ★★★ | **Li D., Danilov D.L., Xie J., Raijmakers L., Gao L., Yang Y., Notten P.H.L. 2016** — "Degradation mechanisms of C6/LiFePO4 batteries: experimental analyses of calendar aging", *Electrochim. Acta* **190**, 1124–1133 ([32]) + **Li D., Danilov D., Gao L., Yang Y., Notten P.H.L. 2016** — "… cycling-induced aging", *Electrochim. Acta* **210**, 445–455 ([33]) | 98 = **1**(새 · 두 편 한 행) | **EMF "mathematical extrapolation" 의 방법 원전**(G3 · (체)) — 그리고 같은 연구실의 **LFP 노화 열화 모드 실험 분석** 둘 — 우리 주 프로젝트(LLI · LAM 모드 식별)와 직접 닿는 액체셀 편 | Q8 · (체) · 모드 |
| ★★ | **Larfaillou S., Guy-Bouyssou D., Le Cras F., Franger S. 2016** — "Comprehensive characterization of all-solid-state thin films commercial microbatteries by Electrochemical Impedance Spectroscopy", *J. Power Sources* **319**, 139–146 ([35]) | 10 · 98 = **2**(**지목 누락 보충** — 10호 §15 ★ · 원장 행 0) | "[12,35] in agreement"(D_Li⊕)의 대조처 · 상용 박막 마이크로배터리 EIS(이 편 셀 계열과 같은지 미확인) · 10호: 노화가 RQ 를 3 → 4 로 | Q3 · Q4 · EIS |
| ★★ | **Fabre S.D., Guy-Bouyssou D., Bouillon P., Le Cras F., Delacourt C. 2012** — "Charge/Discharge simulation of an all-solid-state thin-film battery using a one-dimensional model", *J. Electrochem. Soc.* **159**, A104 ([12]) | 98 = **1**(새 — 12호 본문 [42] "Fabre 2011" 은 후속 절 밖) | 박막 1D 모형의 둘째 계보(CEA) · 농도 의존 D · "[12,35] in agreement" 의 모형 쪽 | Q3 · Q4 |
| ★★ | **de Klerk N.J.J., Wagemaker M. 2018** — "Space-charge layers in all-solid-state batteries; important or negligible?", *ACS Appl. Energy Mater.* **1**, 5609–5618 ([26]) | 98 = **1**(새 — 93호 참고문헌 목록에만) | "space-charge … small influence" 의 남의 결론 하나(G12 · R5) | (b) · R5 |
| ★★ | **Haruta M., Shiraki S., Suzuki T., Kumatani A., Ohsawa T., Takagi Y., Shimizu R., Hitosugi T. 2015** — "Negligible 'negative space-charge layer effects' at oxide-electrolyte/electrode interfaces of thin-film batteries", *Nano Lett.* **15**, 1498–1502 ([42]) | 98 = **1**(새) | 같은 결론의 실험 쪽(박막 계면) | (b) · R5 |
| ★★ | **Braun S., Yada C., Latz A. 2015** — "Thermodynamically consistent model for space-charge-layer formation in a solid electrolyte", *J. Phys. Chem. C* **119**, 22281–22288 ([25]) | 54 · 98 = **2**(재지목 — 54호 §13 은 등급 칸 없는 후속 표 · 원장 행 0 — 누락으로 단정하지 않음) | 축전기 대신 쓸 공간전하층 모형("more advanced mathematical models … [20,25,26]") | (b) |
| ★ | Aizawa Y. 외 2017 *Ultramicroscopy* **178**, 20([23]) · Yamamoto K. 외 2010 *Angew. Chem. Int. Ed.* **49**, 4414([24]) | 98 = 1(새 · 한 행) | 이중층 물리 귀속([23] — n 쪽 이동 Li⁺ · p 쪽 Li⁺ 공공)의 측정 근거 — 전자 홀로그래피 전위 지도 | (b) |
| ★ | Put B., Vereecken P.M., Stesmans A. 2018 *J. Mater. Chem. A* **6**, 4848([40]) | 98 = 1(새) | δc₀ "estimated value of 40 kmol m⁻³" — 이 편 유일한 수치 문헌 대조 | (a) |
| ★ | Xia H., Lu L., Ceder G. 2006 *J. Power Sources* **159**, 1422([29]) | 98 = 1(새) | LCO 박막 D(x) 측정 — 그림 5 적합 D(x) 의 독립 대조 | Q3 |
| ★ | Zhang X., Verhallen T.W., Labohm F., Wagemaker M. 2015 *Adv. Energy Mater.* **5**, 1500498([41]) | 98 = 1(새) | 그림 10f 거울 단면 "demonstrated experimentally"(LFP NDP) | (c) |
| ★ | Teichert K., Oldham K. 2017 *J. Electrochem. Soc.* **164**, A360([16]) | 98 = 1(새) | 동적(축전성) 부하 — "might be different for … MEMS [16]" | (b) |
| 도착 | **Danilov D., Notten P.H.L. 2008** — *Electrochim. Acta* **53**, 5569([28]) | 26 · 91 · **98** = **3**(재지목) | **4차 묶음 파일 61 로 도착 · 처리 대기(101호 예정)** — 식 (23)–(24) · (31) 유도처("see Refs. [11,28]") | 모형 |
| 도착 | **Xie J., Imanishi N., Matsumura T., Hirano A., Takeda Y., Yamamoto O. 2008** — *Solid State Ionics* **179**, 362([31]) | 26 · **98** = **2**(재지목) | **4차 묶음 파일 62 로 도착 · 처리 대기(102호 예정)** — "solid-state diffusion depends strongly on the local electrochemical environment [29–31]" | Q3 |
| ★★★ | Tian H.-K., Qi Y. 2017 — *J. Electrochem. Soc.* **164**, E3512([15]) | 12 · 81 · 94 · 97 · **98** = **5**(재지목) | "the effect of contact area losses between the electrodes and electrolyte [15], leading to battery degradation"(이 편은 범위 밖으로 소개만) | Q6 · Q1 · 곱 |
| ★ | Reimers J.N., Dahn J.R. 1992 — *J. Electrochem. Soc.* **139**, 2091([34]) | 62 · 97 · **98** = **3**(재지목) | "second hexagonal phase [34]" — 그림 5 꺾임 x 0.75 · 0.92 의 상 근거 | Q8 |
| ☆ | Molenda 1989 · Menetrier 1999 · Imanishi 1999([37]–[39]) · Landstorfer 2011([20]) · Becker-Steinberger 2010([19]) · Bates 2015([13]) · Behrou & Maute 2017([14]) · Teichert & Oldham 2017 *J. Energy Storage*([17]) · Dudney 2005([21]) · Le Van-Jodin 2018([27]) · Barker 1996([30]) · Bachman 2016([36]) · 종설 [1]–[10] · Vetter 1967([22]) | 행 없음 | 배경 · LCO 전자 전도도 정성 대조 · 공간전하 고급 모형 · 노화 무시 근거 | — |

**지목 누락 하나 — 이 편이 재지목하며 보충**: Larfaillou 2016(10호 §15 ★ · 원장 행 0). 등급 칸 없는 옛 후속 표에만 있던 편(Braun · Yada · Latz 2015 — 54호 §13)은 누락으로 단정하지 않는다. **흡수된 편(교차)**: [11] = 91호. **4차 묶음 도착 편**: [28] = 파일 61 · [31] = 파일 62(새 요청 행 아님).

---

# 이 digest 가 주장하지 않는 것

- **이 편의 모형 · 결론(LiPON 지배)이 틀렸다고 하지 않는다** — 인쇄 표 그대로 재풀이하면 전해질 · 양극 계면 · 호 지름이 저자 그림과 ±0.5 % 로 닫힌다. 걸린 것은 음극 계면 방향 · 검증의 표본 안 성격 · 용량 기준 · 이중층 값의 물리 범위다.
- **음극 계면 방향 문제(D1)를 구현의 사실로 확정하지 않는다** — 코드 미공개다. 확정인 것은 인쇄 식 (12) · (16) 이 글자 그대로 그 방향을 준다는 것과 그림 셋(9e · 9f 삽도 · 11c)이 그 계산과 정량으로 맞고 물리 방향과는 안 맞는다는 것(`[재현·대수]` · `[도표·화소]` — 판독 폭 안)까지다. 1C 는 판독 폭 안이라 가르지 못했다. 성능 결론에 주는 크기는 작다(4C ≈3 %).
- **26호의 적합이 틀렸다고 하지 않는다** — 이 편이 보이는 것은 26호의 '문헌과 일치' 가 독립 근거가 아니라는 것(같은 자료 두 적합)과 26호 데이터 쪽 C-rate 기준(1C = 0.7 mA)까지다. 26호가 실제로 어느 전류로 모의했는지는 26호 지면 문제로 남는다.
- **c_dl · c_geo 값이 틀렸다고 하지 않는다** — 적합 모형 안에서 고주파 호를 맞춘 유효 매개변수로는 쓸 수 있다. 주장은 그 값을 공간전하층의 물리값 · 실제 계면 면적 비례의 근거로 읽을 수 없다는 것까지이고, 등가 두께는 ε_r 를 c_geo 에서 역산한 가정 위의 `[재현·가정]` 이다.
- **그림 판독 값을 저자 원자료로 쓰지 않는다** — 벡터 판독(그림 3 · 5 · 8)은 경로 좌표, 화소 판독은 선 · 표지 중심이고 판독 폭을 각 자리에 적었다. 그림 9 의 1C 값은 선 겹침 때문에 범위로만 적었다.
- **이 편을 Q4 · Q1 칸 이동 근거로 쓰지 않는다** — 식별성 계산 0 · 열화 0. 비식별 방향(면적 인자 · 음극 호 겹침)은 우리 재현이다.
- **원 참고문헌(26 · 37 · 91 · 10 · 54호 인용분)을 다시 열지 않았다** — 대조는 각 digest 전사로 했다.
