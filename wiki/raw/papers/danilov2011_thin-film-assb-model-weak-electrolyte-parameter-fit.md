---
title: "Danilov D., Niessen R.A.H., Notten P.H.L. 2011 — Modeling All-Solid-State Li-Ion Batteries (J. Electrochem. Soc. 158(3), A215–A222)"
source_url: local-upload/51._Modeling_all-solid-state_Li-ion_batteries.pdf
source_url_note: "본문 PDF 9 쪽(PDF p. 1 = IOP 내려받기 표지 · 지면 A215–A222 = PDF p. 2–9 · PageLabels 1–9 는 인쇄 쪽보다 한 칸 밀림 · 그림 12 · 표 2 · 번호 식 22 · 참고문헌 33) 1,137,644 B · 업로드 접두사 ee00bca9 · 4차 묶음 파일 51 · SI 없음(원문에 보충 언급 0) · 예치 원자료 0 — 자동 크롭 12 + 표 수동 크롭 2 전부 봤다 · 그림 2–8 · 11 · 12 는 PDF 벡터 경로를 눈금 보정해 읽었다(판독 배열 · 재풀이 코드는 커밋 안 함)"
source_doi: 10.1149/1.3521414
source_license: "© 2010 The Electrochemical Society. All rights reserved.(A215 인쇄) — 오픈 액세스 표기 0 · 이 digest 는 인용 · 요약 · 재현 계산만 담는다(그림 크롭은 위키 관례대로 raw/figures 에 — 변형 없는 잘라내기)"
pdf_sha256: e00bb9869bd275ebcfabfdee216a92b6e891a91374a56916350ee2d1419a105c
ingested: 2026-10-02
sha256: e32b93d362b64a68e2d2c74f7ce5465709a7feeb4a29f2b31e84b7f526b46829
---
# 수집 목적

`assb` 섹션 **91호** — **4차 묶음 파일 51**(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 요청 14 편 중 첫 편 · 2026-10-02 사용자 공급 — 사용자 말 "이것도 논문 받아둬서 논문에이전트 진행하게" · 파일 51–64 = 91–104호를 받은 순서대로). 닻은 `questions/assb-contact-loss-vs-lampe.md` — 이 편이 걸리는 축은 **Q4(유일성 · 식별성)** 하나가 중심이고 Q1 · Q5 · Q6 · Q7 은 "해당 없음" 의 이유를 적는 자리다.

Eindhoven 공대 + Philips Research(Notten 연구실)의 *J. Electrochem. Soc.* 2011 모델 논문으로, **평면 박막 전고체 전지(Si/TiO₂/Pt 기판 · LiCoO₂ 320 nm · Li₃PO₄ 1.5 µm · Li 금속 · 공칭 10 µAh · 1 cm²)** 한 개의 **1.6C CCCV 충전 + 1.6–51.2C 정전류 방전 여섯 율** 곡선에, 양극 Butler–Volmer · 양극 Fick 확산 · **전해질 "약전해질" 해리(Li⁰ ⇌ Li⁺ + n⁻) + 두 운반체 Nernst–Planck** 의 1차원 모형을 맞추고(표 II), 과전압을 세 항(전하이동 · 양극 확산 · 전해질 물질전달)으로 나눠 "**전해질 수송 제한이 전체 과전압의 절반 이상**" 이라고 결론 낸 편이다.

들어온 경로: 원장 행(그대로) "★★★ | **Danilov·Niessen·Notten 2011** — *J. Electrochem. Soc.* **158**(3), A215 | 12 · 26 | **2** | **Q4** | 이 모델 계보의 원형 — 파라미터 추정을 한 기계론 모델 (12호 [61] 재인용 · 26호 [15])". 위키 grep(`A215` · `3521414` · `Danilov` · `Niessen`): **26호**(Iwakiri 2024 — 이 편을 [15] 로 인용 · 후속 표 ★★★ · Table 1 "Parameter Estimation Yes" 넷 중 하나) · **12호**(Kouhestani 2022 — [61] 로 **본문에서만** 재인용 · 후속 절 0 — 아래 "지목 수 정정") · 27호(Sinzig 2024 — "이 편이 인용하지 않는 것" 목록에만) · 37호(Li 2024 — Raijmakers 2020 행의 저자 이름으로만). **이 편은 우리 digest 를 하나도 인용하지 않는다**(참고문헌 33 편 전부 2010 년 이전).

이 digest 의 일 (지시):

1. **(a) 매개변수 추정의 실체 (Q4)** — 표 II 행별 출처 층위(측정 · 문헌 · 적합 · 가정) · 무엇에 · 어떻게 맞췄나 · 오차 · 신뢰구간 · 다중 시작 · 상관 · 식별성 어휘 전수 · "외삽 평형 전압" 이 측정인가 모형인가.
2. **(b) 26호 계보 대조** — 이 편 값 ↔ 26호 표(그 "문헌값" = Raijmakers 2020 이라고 26호가 적음)를 같은 이름끼리 · `D_e⁻` 10 자릿수의 시작점인가.
3. **(c) 물리 · 가정** — 전해질 운반체 · "절반 이상" 이 모형 출력인가 · 이중층.
4. **(d) 박막 ↔ 복합 전극 이식성** — `ASSB_TRANSFER_NOTE.md` §2–§4 (읽기만) 에 넘길 것 / 못 넘길 것.
5. **(e) Q1 · Q5 · Q6 · Q7** — 채움표 칸.
6. **(f) 후속 후보** — Notten 계보 · 매개변수 원천 · 식별성 (지목 수는 각 digest 후속 절 grep 값만 · 4차 묶음 13 편은 "도착 · 처리 대기").

⚠ **표기 규약**: `[인쇄]` = 원문이 실제로 쓴 것 · `[도표]` = 그림을 눈으로 읽은 값(판독 폭 표시) · **`[도표·벡터]`** = 이 편 그림이 **PDF 벡터 경로**(PDF p. 4–9 래스터 이미지 0)라 경로 좌표를 **눈금 숫자 중심 위치로 선형 보정**해 읽은 값 — 판독 폭은 그림마다 눈금 보정 잔차(최대값)로 적는다(예: 그림 4 전류 ±0.1 µA cm⁻² · 전압 ±0.6 mV) · 같은 그림 안 두 선의 차이는 보정 오차를 공유하므로 더 좁다 · **저자 원자료가 아니다**(그리기 전 단계 값과 다를 수 있다) · `[도표·화소]` = 래스터 화소 판독 · `[재현]` = 원문 수치 · 식으로 우리가 다시 계산 · `[재현·가정]` = 가정이 붙은 재현(가정을 같이 적는다) · `[재현·외부 값]` = 원문 밖 상수를 쓴 재현 · `[해석]` = 우리 해석. **`[데이터]` 0** — 예치 원자료 없음. 그림 판독 값 · 재현 값은 인쇄 수치와 섞지 않는다.

⚠ **쪽 표기**: PDF p. 1 은 IOP 내려받기 표지("To cite this article" · 추천 논문 셋 · 내려받기 일시 — 지면 아님)라 **인쇄 쪽 A215–A222 = PDF p. 2–9** 다. PDF PageLabels 는 1–9 순번(규칙 하나 · 십진 · 시작 1)이라 **라벨이 인쇄 쪽보다 한 칸 밀린다**(78호 선례). 이 digest 는 "A217(PDF p. 4)" 처럼 둘을 같이 적는다.

---

# 판정 먼저

1. ★★★ **(a) 표 II 12 행의 실체** — 설계 3(`L` 1500 nm · `M` 320 nm · `A` 1 cm² — 각주 a "Design parameters" · 본문은 "determined by scanning electron microscopy" — 그러나 그림 1a SEM 은 축척 막대 0 · LiCoO₂ : Li₃PO₄ 띠 폭 ≈0.97 `[도표·화소]` ↔ 320 : 1500 nm = 0.21 → "an example" 의 다른 셀) · NDP 측정 1(`a₀` 6.01×10⁴ mol m⁻³) · 유도 1(`a_max` 2.33×10⁴ — 각주 c · `[재현·가정]` 공칭 10 µAh ÷ (F · Δx 0.5 · 320 nm · 1 cm²) = **23.32 kmol m⁻³** ✅ — 물질 상수가 아니라 용량 맞춤 유효값 · `[재현·외부 값]` 조밀 LiCoO₂ 격자 Li 밀도 ≈51.6 kmol m⁻³ 의 45 %) · **"model optimization" 7**(`k_r` · `δ` · `D_Li⁺` · `D_n⁻` · `D_Li` · `α` · `k₁ˢ`). **무엇에**: 그림 7 — 1.6C CCCV 충전 + 3.2–51.2C 방전 다섯(1.6C 방전 일치는 지면 0). **어떻게**: 손실 함수 · 알고리즘 · 가중 · 시작점 · 잔차 · 반복 · 불확실성 **인쇄 0**. 식별성 어휘(`identifiab*` · `uniqu*` · `confiden*` · `uncertain*` · `sensitiv*` · `error` · `±` · `residu*` · `correlat*`) **본문 전수 0**(NFKC 전후 같음 — `fit*` 만 0 → 1, "ﬁ" 합자). **평형 전압은 측정이 아니다** — 같은 방전 곡선 네 율(1.6–12.8C · 25.6 · 51.2C 제외)의 회귀 외삽(선형 Q ≤ 8 · 2차 Q ≥ 9.25 µAh cm⁻² · 한 줄 네 점에 2차 = 자유도 1)이고, 우리가 벡터 경로로 저자 붉은 점을 **±2 mV · ±0.0015 µAh cm⁻²** 로 재현했다 — 그리고 **선형 ↔ 2차 선택이 Q 9.25 · 9.5 에서 10 · 28 mV, 가파른 끝 위치를 0.06 µAh cm⁻² 바꾼다**(`[재현]` · 저자 불확실성 0).
2. ★★★★ **(a) 인쇄 표로 저자 그림을 다시 풀면 — `k_r` 이 ×100 어긋난다.** `[재현]` 표 II 값 그대로 전해질 부분계(식 14 · 18–20)를 우리가 다시 풀면 51.2C(512 µA cm⁻²)에서 η_mt 가 15 · 30 · 50.4 · 64.9 s 에 −76 · −103 · −149 · −226 mV — 지면(그림 11 · 8b `[도표·벡터]`) −70 · −86 · −101 · −109 mV 와 RMS 64 mV · 3.2C 정상 −12.8 ↔ 지면 −5.8 mV · 그리고 인쇄 값에서 **정상 한계 전류 ≈257 µA cm⁻²**(`[재현·선형]`)라 51.2C 가 그 두 배다. **`k_r` 하나만 ×100(0.90×10⁻⁶ m³ mol⁻¹ s⁻¹)** 하면 그림 11 의 네 시각 합(RMS **0.8 mV**) · 확산 / 이동 몫(−43.5 / −65.6 ↔ −43.3 / −65.5 mV) · 그림 12 계면 농도 넷(±0.05 kmol m⁻³) · 그림 8a 3.2C 과도(−4.06 · −5.51 · −5.83 ↔ −4.10 · −5.45 · −5.82 mV)가 **한꺼번에** 맞는다(×95–×110 에서 RMS ≤ 2.0 mV · ×1 64 · ×30 29 · ×300 25 mV · 다른 매개변수 조합은 미검사 — 유일성 주장 안 함). 26호의 "문헌값" `k_r` **8.00×10⁻⁷** 과 같은 자릿수다(그 출처는 파일 58 에서 확인).
3. ★★★ **(a) `k₁ˢ` 는 단위 관례 없이 재사용할 수 없다.** 단위 m^2.8 mol^−0.6 s^−1 은 **적합된 α = 0.6 에 묶인 단위**다(`[재현]` 차원: (k₁⁰)^0.4 (k₋₁⁰)^0.6 · 식 8 ✅ — 단 표 I 의 `k₋₁` 단위 "m⁴ mol⁻⁴ s⁻¹" 는 m⁴ mol⁻¹ s⁻¹ 의 오기). 인쇄 단위(mol m⁻³ · m²)로 x = 0.5 의 교환 전류를 내면 **i₀ = 151 A** — 그림 8 이 요구하는 i₀ ≈**0.9–1.0 mA**(그림 8b 0.02 분 η_ct −13.2 mV · 그림 8a −0.9 mV `[도표·벡터]` → `[재현]`)와 ×1.5×10⁵ · kmol m⁻³ 로 읽으면 2.4 mA(×2.4) · mol cm⁻³ + cm² 로 읽으면 0.38 mA(×0.4) — **어느 관례로도 맞지 않는다.** 본문 "charge transfer resistances of the order of 50–100 Ω" 는 그림 8 η_ct / I(26–66 Ω cm² — 평탄 구간 `[도표·벡터]`)와 같은 자릿수이고, 문장의 "total overpotential"(η/I ≈360–420 Ω cm² — 그림 6 `[도표·벡터]`)과는 아니다.
4. ★★★★ **(a) "Good agreement … for all discharge currents"(A220)는 그림 7 의 시간 축 위에서만 성립한다.** `[도표·벡터]` 그림 7(같은 그림 · 같은 보정) — 모형 붉은 선의 3.0 V 도달 1.01 · 2.24 · 4.52 · 9.25 · 18.71 분 ↔ 측정 마지막 점(≥ 3.0 V) 1.32 · 2.46 · 4.83 · 9.47 · 18.76 분(51.2 → 3.2C · 차 0.31 · 0.22 · 0.30 · 0.22 · 0.05 분 · 모형 방전 시작 0.222 분 · 측정 첫 방전 점 0.274 분). 용량으로 옮기면(측정 = 그림 3 끝 Q) **모형 = 측정의 73–78 · 90 · 94–96 · 98 · 99 %**(앞 수 = 그림 7 모형 지속 기준 · 뒤 수 = 우리 재풀이 기준). 우리 재풀이(표 II + `k_r` ×100 + i₀ 1 mA)가 그 모형 선을 다시 낸다(컷오프 0.843 · 2.020 · 4.375 · 9.095 · 18.534 분 ↔ 그림 7 모형 지속 0.79 · 2.02 · 4.30 · 9.03 · 18.49 분 · 그림 8b 끝 0.840 분) → **모형 자체가 51.2C 용량을 22–27 % 못 낸다**(25.6C 10 %). 그림 7 의 65 분 축에서 0.31 분 = 표지 지름(2.6 pt ≈0.81 분)의 0.4 배라 원 배율로는 안 보인다. 그리고 그림 11(전류 1.08 분)은 같은 51.2C 전해질 곡선을 **측정 길이 쪽**까지 그렸다 — 같은 모의의 두 길이(D).
5. ★★★ **(c) "전해질 수송이 전체 과전압의 절반 이상" 은 모형 출력이고, 가정이 만든다.** 독립 측정(EIS · 두께 변화 · 기준극) 0. SE 를 **이원 전해질**(Li⁺ + n⁻ — n⁻ = "nBO 에 묶인 미보상 음전하" 인데 `D_n⁻` 5.10 > `D_Li⁺` 0.90 ×10⁻¹⁵ 로 적합 → `[재현]` t₊ = 0.15 · 전류의 85 % 를 n⁻ 가 나름)으로 두었기에 농도 분극이 생긴다 — 같은 지면이 Li₃PO₄ 를 "conductivity is caused by the transport of Li⁺ ions only" 라 쓴다(`vacanc*` 0 회 — n⁻ 를 Li 공공으로 읽으면 화해되나 지면은 그렇게 쓰지 않는다 · 파일 61 에서 확인). `[재현·벡터]` η_mt 몫 시간 평균 **51.2C 45 % · 3.2C 46 %** — "at least half" 는 51.2C **뒷 절반에서만**(0.49 분부터) 성립하고 초록은 조건을 뗐다; "0.5 mA cm⁻² 이상에서 더 커진다" 는 몫으로는 안 보인다(절대 mV 만 커진다). 그리고 그 몫이 2 번의 `k_r`(×100) 에 매달린다. **이중층 0**(`capacitance` · `double layer` 0 회) — 37호 물음("`c_dl` 이 면적에 비례하는가")에 이 원형은 **항이 없다**로 답한다.
6. ★★★ **우리가 공급하는 식별 경계 (`[재현·가정]` — 지면에 없는 계산)**: 우리 재풀이 모형에서 표 II 의 적합 일곱으로 국소 Fisher 정보(여섯 율 · 컷오프 2–85 % 구간 30 점씩 · σ_V 1 mV 가정)를 내면 **전해질 넷(`k_r` · `δ` · `D_Li⁺` · `D_n⁻`)이 |상관| ≥ 0.98 의 한 묶음**(`δ`–`D_Li⁺` −0.999 · `k_r`–`δ` −0.996)이고 조건수 **9.5×10⁵**, 가장 약한 방향 = (`δ` ↑ · `D_Li⁺` · `D_n⁻` · `k_r` ↓) — 1σ 각 ×1.4–1.9 · 반면 `D_Li` ×1.005 · `α` ×1.03 · i₀ ×1.10. → 본문 "only about 18 % of the Li atoms are mobile" 은 **골짜기 위의 한 좌표**이고 26호 §5-2 ④("전해질 셋 — 전도도형 한 조합", 26호 `[추론]`)에 원형 모형의 수치를 준다.
7. **(d) 이식** — 넘길 것: 과전압 세 항의 골격 · 율 외삽 평형 곡선 **방법과 그 모형 의존 폭** · "인쇄 표 → 그림 재풀이" 검사. 못 넘길 것: **값 전부**(다른 SE · 다른 양극 · 조밀 단일 박막 · 입자 · 기공 · 굴곡도 · 접촉 · 열화 0 · Li 금속 무한 원천) · `a_max`(용량 맞춤 — 복합 양극이면 θ · ε 를 삼키는 자리) · 이원 SE 가정(황화물 단일 이온 전도체와 반대편).
8. **(e) 채움표** — Q1 해당 없음(조밀 평판 · `contact` 0 · 열화 0) · Q2 없다 · Q3 층 하나("각주 셋으로 층위를 단 계보 첫 표 — 적합 일곱의 방법 0 · 인쇄 값 하나가 자기 그림과 ×100 · 평형 곡선 = 같은 데이터 회귀 외삽") · **Q4 0/91 — 여든세 번째 성질** · Q5 해당 없음(Li 금속 · E_Li ≡ 0 · Li 쪽 η_ct "for convenience" 무시) · Q6 해당 없음(`pressure` 3 = 증착 압력) · Q7 해당 없음 + **공백**(Li 층 증착 단계 · 두께 미기재 — 마지막 증착 층 = Co 150 nm) · Q8 층 하나(LiCoO₂ 박막 · 외삽 평형 곡선). **누적 ≈20.0 → ≈20.0 (새 칸 0).**
9. **(b) 26호 계보** — 이 편이 **계보의 첫 매개변수 표**이고, 26호 표와 같은 이름 아홉 중 **같은 값은 0**(다른 셀 · 다른 SE — Li₃PO₄ ↔ LiPON); `a₀` 만 1.7 % 차(6.01×10⁴ ↔ 61 141). **`D_e⁻` 는 이 편에 없다**(양극 = 단일 `D_Li` Fick · 이동항 무시 "screened by the mobile electrons"[28,29]) → **26호의 10 자릿수 표류는 이 편에서 시작되지 않는다** — 이 편에서 시작되는 것은 **인쇄 값의 자릿수 오기(`k_r` ×100)와 단위 관례 미인쇄(`k₁ˢ`)** 다.

---

# 서지

| 항목 | 값 (`[인쇄]` — A215 PDF p. 2 · 표지 PDF p. 1) |
|---|---|
| 제목 | **"Modeling All-Solid-State Li-Ion Batteries"** |
| 저자 · 소속 | **D. Danilov**ᵃ · **R. A. H. Niessen**ᵇ · **P. H. L. Notten**ᵃ,\*,ᶻ — ᵃ Eindhoven University of Technology, Den Dolech 2, 5600 MB Eindhoven, The Netherlands · ᵇ Philips Research Laboratories, High Tech Campus 4, 5656 AE Eindhoven, The Netherlands · \* Electrochemical Society Active Member · ᶻ 교신 p.h.l.notten@tue.nl |
| 저널 | *Journal of The Electrochemical Society* **158**(3) **A215–A222** (2011) · 0013-4651/2010/158(3)/A215/8/$28.00 · **doi 10.1149/1.3521414** |
| 일정 | 투고 2010-08-16 · 수정 2010-11-05 · 온라인 **2010-12-28** |
| 라이선스 | "© 2010 The Electrochemical Society. All rights reserved."(A215) — 오픈 액세스 표기 0 · 이 digest 는 인용 · 요약 · 재현 계산만 담는다(그림 크롭은 위키 관례대로 `raw/figures/` 에) |
| 사사 | Dr. H.T. Hintzen(TU/e) · Dr. I. Kokal · **EU FP7 Superlion project** · "Eindhoven University of Technology assisted in meeting the publication costs of this article." |
| 분량 | 지면 8 쪽(A215–A222) + IOP 표지 1 · 그림 12(1a · b · 8a · b 포함) · 표 2(I 기호 39 줄 · II 매개변수 12 행) · 번호 식 22(1 · 2 · 3a–b · 4a–b · 5a–b · 6–8 · 9a–b · 10–15 · 16a–d · 17a–d · 18–20 · 21a–d · 22) · 참고문헌 **33**(목록 번호 1–33 · PDF A222 에서 직접 셈) |
| 셀 | 평면 박막 · in-house 장비(RF 스퍼터 2 in. 표적 13.56 MHz + 열 / 전자빔 증착 · Ar 글러브박스 · 기저 압력 < 10⁻⁶ mbar · 하드 마스크) · 기판 Si + TiO₂/Pt 50 nm/250 nm · **LiCoO₂ 320 nm**(60 W · 8×10⁻⁶ bar O₂/Ar 4:6 · 800 ℃ 10 min RTA · 60 ℃/min) · **Li₃PO₄ 1.5 µm**(30 W · Li₃PO₄ 표적 · 15×10⁻⁶ bar Ar) · **Co 150 nm 집전체**(전자빔 5 Å/s) · Li 금속 음극(증착 단계 미기재 — G2) · **공칭 10 µAh** · 면적 1 cm²(표 II) |
| 시험 | **CCCV 1.6C → 4.2 V · 30 min 휴지 · CC 방전 1.6 · 3.2 · 6.4 · 12.8 · 25.6 · 51.2C 차례로** · 컷오프 3.0 V(A221 "cutoff voltage of 3.0 V") · Biologic VMP3 8 채널(저전류 · 임피던스 보드) · 25 ℃(모의와 같은 온도) · 셀 **하나**(셀 수 인쇄 0 — "A 10 µAh … battery was deposited") |
| 모형 | 1D · 등온 · 음극 = Li 금속(전위 0 · 전하이동 무시) · 전해질 = 해리 Li⁰ ⇌ Li⁺ + n⁻(식 14) + 두 운반체 Nernst–Planck(식 15–17) → 전기중성으로 확산-반응 식 하나(식 18 · 유도는 [27] Danilov & Notten 2008) · 양극 = Fick(식 21 · 이동항 무시) + BV(식 10–11 · α 적합) · 과전압 = η_ct + η_d + η_mt(식 22) · 평형 전압 = 회귀 외삽(그림 3–5 · [31] Chap. 4) · 이중층 0 · 열화 0 · 부반응 0("Assuming that no side reactions take place") |

**PDF 메타데이터 (직접 읽음 · pymupdf)**: 1,137,644 B · sha256 `e00bb9869bd275ebcfabfdee216a92b6e891a91374a56916350ee2d1419a105c`(호출자 접두 `e00bb9869bd275eb` ✅) · `%PDF-1.4` · 9 쪽 — p. 1 595×842 pt(A4 · IOP 표지) · p. 2–9 657×855 pt · 정보 사전: title · author · subject · keywords **빈 값** · creator **"XPP"** · producer **"Acrobat Distiller 6.0.1 (Windows); modified using iText® 5.5.13.5 ©2000-2026 iText Group NV (IOP Publishing Ltd; licensed version)"** · 생성 **2010-12-28 12:16:00Z**(온라인 날짜와 같은 날) · 수정 **2026-10-02 13:41:27 +01:00**(IOP 내려받기 시각 — 표지의 "downloaded … on 02/10/2026 at 13:41" 과 같다 · 내려받은 IP 는 옮기지 않는다) · 암호 0 · XMP 3,349 B(xmpMM:DocumentID uuid:f4f1cdbb-c0c7-43d6-a565-e6efb0f7da5a · InstanceID uuid:0eba82f4-7b13-4ff8-a3dc-8ec0b6aa567a · dc:title · creator · description 빈 값) · PageLabels 규칙 하나(시작 p. 0 · 십진 · 1 부터) → 라벨 1–9 · 이미지: p. 1 둘(IOP 로고 700×166 · 표지 아래 광고 띠 1640×1061) · p. 2 하나(첫 쪽 왼쪽 위 81×60 pt 머리 장식으로 읽힘 — 확인 안 함) · p. 3 하나(그림 1a SEM 843×394) · **p. 4–9 0**(그림 2–12 는 전부 벡터).

**표지(PDF p. 1)의 IOP 추천 논문 셋**(Pang 외 · Xu & Wang · Farkhondeh & Delacourt)은 지면이 아니다 — 어휘 집계에서 뺐다(표지 `correlat` 1 = 추천 논문 제목).

---

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **최적화의 정체** — 손실 함수(전압 RMS? 율별 가중?) · 알고리즘 · 시작점 · 정지 기준 · 다중 시작 · 경계 · 쓴 곡선 범위(충전 포함인가 · 1.6C 방전 포함인가 · 3.0 V 근처 가중) · 잔차 · 반복 수 · 불확실성 — 전부 0. `[인쇄]` "Figure 7 shows the optimized simulations obtained with the applied model" · "The optimized parameters are listed in Table II" · 표 II 각주 c "All the remaining parameters are obtained from model optimization" 셋뿐 | 일곱 값이 **수렴점인지 · 손으로 맞춘 점인지** 가를 수 없다 — §(a) 5 의 `k_r` ×100 이 "오기" 인지 "다른 점" 인지도 이 공백 때문에 우리가 재풀이로만 가른다 |
| **G2** | **Li 음극 증착 단계 · 두께 · Li 재고** — 실험 절은 LiCoO₂ → Li₃PO₄ → "Finally, 150 nm cobalt was deposited as the current collector" 로 끝난다. 장비 목록에 열 증착(thermal evaporation)이 있으나 Li 를 증착했다는 문장 0 · 그림 1a 는 'Li' 띠를 그리지만 "an example" 의 다른 셀(D1) | Li 를 따로 증착한 셀인지, **첫 충전에 Co 위로 도금되는 Li-free 구성**인지 지면으로 판정 불가 → Q7(재고)과 Li 음극 과전압 무시 가정의 근거가 둘 다 비어 있다 |
| **G3** | **그림 3 · 6 의 색 ↔ 율 대응** — 범례 0 · 캡션의 율 나열 순서로만 읽힌다 | 우리 율별 값(Q 끝 · η/I)은 "빨강 = 1.6C … 검정 = 51.2C" 순서 가정 위 — 끝 용량 단조 순서가 그 가정과 맞는다(10.04 > … > 9.17) |
| G4 | **SEM 두께 측정 그림** — 본문 "The thicknesses of the electrode M and the electrolyte L have been determined by scanning electron microscopy" 인데 표 II 각주는 "Design parameters" · 그림 1a 는 축척 막대 0 + 띠 비 ≈0.97 | `L` · `M` 이 측정인지 설계인지 — 둘이 같은지 — 확인 불가 |
| G5 | **NDP 결과 자료** — `a₀` 6.01×10⁴ mol m⁻³ 하나만 인쇄(깊이 분포 · 불확실성 · 시편 0) | `a₀` 는 표에서 유일한 독립 물질 측정값이다 |
| G6 | **30 min 휴지의 위치** — 본문 · 그림 2 캡션 "relaxation" ↔ 그림 2 · 7 은 4.2 V 평탄 ≈5.5 분 뒤 바로 방전(D2) | 모의의 초기 조건(충전 끝 농도 분포가 이완됐는가)과 그림 7 충전 구간의 의미가 걸린다 |
| G7 | **1.6C 방전 모의** — 그림 7 축(−43 → 20 분)에 1.6C 방전(≈37.6 분)이 없다 · 그림 3 은 측정만 | "all discharge currents" 의 1.6C 몫은 지면에 없다 |
| G8 | **`k₁ˢ` 의 농도 단위 관례 · `k_r` 인쇄 자릿수** — §(a) 5 · 6 | 계보(26 · 37호 · 파일 58)로 값이 옮겨질 때 단위 · 자릿수가 같이 옮겨졌는지 |
| G9 | **E_eq(x) 함수형** — 그림 3 녹색 곡선 하나(식 · 표 0) | 우리 재풀이는 녹색 벡터 경로를 평형 곡선으로 썼다(`[도표·벡터]`) — η_d · 컷오프 시각이 그 곡선에 걸린다 |

---

# 보충 자료 — 받은 것 · 대조

**SI 없음 (원문에 보충 언급 0).** 호출자 대조와 같은 결과를 직접 다시 셌다 — 본문 · 캡션 · 표 · 참고문헌 전문(NFKC 전후)에서 `supplement*` · `appendix` · `data availability` · `supporting information` · `video` · `movie` · `zenodo` · `github` **0 회**. 원자료 예치 0 · 코드 0. 그래서 이 digest 의 재현은 **인쇄 수치 + 그림 벡터 경로** 두 층뿐이다.

---

# 그림 — 자동 12 항목 + 표 수동 2, 실제로 연 것 **12/12 + 표 2/2** (+ 벡터 경로 판독 아홉 · 화소 판독 하나 · 확대 렌더 하나 — 판독용 · 커밋 안 함)

크로퍼(`wiki/tools/extract_figures.py`)가 본문 그림 **12** 를 `fig_1 … fig_12` 로 잡았다(SI 오판 0 — 파일명 `51._Modeling_all-solid-state_Li-ion_batteries` 에 SI 표지 없음 · 첫 실행 뒤 이름을 눈으로 확인). **표 I · II 는 자동 추출이 잡지 않았다**(표 캡션 미인식) → PDF p. 5 · p. 7 을 300 dpi 로 수동 렌더해 `tab_1_manual_p5.png` · `tab_2_manual_p7.png` 로 더했다(`figures.json` `manual: true`). **열네 장 전부 직접 봤다 — 안 본 그림 0.** 그림 2–8 · 11 · 12 는 그림 자체가 PDF 벡터라 경로 좌표를 꺼내 눈금 숫자 중심으로 보정해 읽었다(`[도표·벡터]` · 축별 보정 잔차 = 판독 폭 · 판독 배열은 `scratchpad` 에만). 그림 9 · 10(3D 면)은 수치 판독하지 않았다.

자동 크롭 점검(`figures.json` `note` 에 적음): 열두 장 모두 **라벨 · 축 · 내용 온전 · 잘림 0 · 과대 영역 0**(캡션 · 본문 섞임 0). 캡션 필드 문제 하나 — **괄호 자리에 제어 문자 U+0001 · U+0002**(원 PDF 글꼴 Universal-GreekwithMathP 의 괄호 글리프 — 텍스트 층 그대로 · 열두 캡션 공통 · 고치지 않음). 900 자 잘림 0 · 바닥글 섞임 0.

## Fig. 1 — SEM 단면 + 1D 모식 (A216 · PDF p. 3 · 봤다) ★★ (a) G4 · D1

(a) `[도표]` SEM — 왼쪽부터 'Li' · 'Li₃PO₄' · 'LiCoO₂' 띠, 밝은 경계, 어두운 기판. **축척 막대 0.** `[도표·화소]` 열 평균 밝기 단면으로 띠 폭을 쟀다: Li₃PO₄ ≈233 px · LiCoO₂ ≈225 px(비 ≈0.97 ±0.1) — 인쇄 두께 320 : 1500 nm = **0.21** 과 ×4.6 어긋난다 → 캡션 "**An example** of an SEM image of an as-produced solid-state Li-ion battery" 그대로 **모의한 셀이 아닌 예시 셀**로 읽힌다(`[해석]`). 본문 "The thicknesses … have been determined by scanning electron microscopy" 의 근거 그림은 지면에 없다(G4). (b) 모식 — Li | Li₃PO₄ electrolyte | LiCoO₂ · 좌표 y: 0(Li 계면) · L(양극 계면) · L+M(집전체) · 화살 "Li⁺ → Discharge" · "Li⁺ ← Charge" · 집전체 미표시(본문 "Their influence … negligible").

## Fig. 2 — 측정 전압–시간 (A219 · PDF p. 6 · 봤다 + 벡터 3,177 점) ★★★ (a) · D2 · G6 · G7

`[도표·벡터]`(시간 ±0.13 분 · 전압 ±0.002 V) **충전 곡선 하나**: −41.96 분 3.62 V 에서 시작 → 3.9 V 평탄 → **−5.43 분에 4.195 V**(CC 구간 ≈36.5 분 — `[재현·가정]` 1.6C = 16 µA cm⁻² 면 ≈9.7 µAh cm⁻²) → 4.198 V(−4.6 → −1.5 분) → 4.196 V(−1.5 → +0.10 분) → 방전 다섯. 방전 첫 점 **+0.274 분**(그 앞 마지막 평탄 점 +0.100 분) · 3.0 V 앞 마지막 점 **18.76 · 9.47 · 4.83 · 2.46 · 1.32 분**(3.2 · 6.4 · 12.8 · 25.6 · 51.2C). 데이터 전압이 2.3 mV 계단(4.1959 · 4.1982)으로 양자화돼 보인다(`[해석]` 측정 해상도 또는 출력 반올림).
- ⚠ **D2 — "30 min relaxation" 이 그림에 없다.** 4.2 V 근처 평탄은 ≈5.5 분이고, 30 분 휴지를 그렸다면 −30 분부터여야 한다. 캡션 "CCCV charging (CC = C-rate; V_max = 4.2 V), relaxation and discharging" — 휴지를 잘라 붙였는지 서술 0(G6).
- 캡션 "(CC = C-rate; …)" 의 **숫자 빠짐은 인쇄 그대로**(렌더로 확인 · 본문 "with a 1.6 C-rate").
- 1.6C 방전은 축 밖(G7 — `[재현]` 10.04 µAh cm⁻² ÷ 16 µA cm⁻² = 37.6 분).

## Fig. 3 — 측정 방전 곡선 여섯 + 외삽 평형 곡선 (A219 · PDF p. 6 · 봤다 + 벡터) ★★★ (a) · G3

`[도표·벡터]`(Q ±0.008 µAh cm⁻² · V ±0.001 V) 선 일곱 — **녹색 = 외삽 평형**: Q 0 에서 **4.197 V** → 4.15 V 부근 어깨(Q ≈1) → 3.90 V 평탄(Q ≈6–9.8) → 급락 · **3.0 V 에서 10.10 µAh cm⁻²**. 측정 여섯(빨강 · 남색 · 노랑 · 자홍 · 하늘 점선 · 검정 점선 — **범례 0**, 캡션 순서 1.6 … 51.2C 로 읽음 G3): Q 0 의 전압 4.192 · 4.190 · 4.177 · 4.156 · 4.116 · 4.038 V · **3.0 V 끝 10.04 · 9.95 · 9.86 · 9.76 · 9.57 · 9.17 µAh cm⁻²** → 평형 용량 대비 방전 용량 비 99.4 · 98.5 · 97.7 · 96.6 · 94.8 · **90.8 %**(이 비는 노화 유지율이 아니다 — 같은 신품 셀의 율 의존). `[재현]` Q ÷ (C × 10 µA cm⁻²) = 37.65 · 18.66 · 9.25 · 4.57 · 2.24 · **1.075 분** — 그림 2 의 마지막 점 시각에서 시작 ≈0.25 분을 빼면 맞는다(D 아님 · 그림 2 의 t = 0 이 전류 시작보다 ≈0.1–0.27 분 앞).

## Fig. 4 — V–I 회귀 외삽 (Q_out 여섯) (A219 · PDF p. 6 · 봤다 + 벡터) ★★★ (a)

`[도표·벡터]`(전류 ±0.1 µA cm⁻² · 전압 ±0.6 mV) **측정 점 24 = 전류 15.91 · 32.06 · 63.99 · 128.04 µA cm⁻²**(= 1.6 · 3.2 · 6.4 · 12.8C × 10 µA cm⁻²) × Q_out 0 · 2 · 4 · 8 · 9.25 · 9.50 µAh cm⁻² · 붉은 회귀선 6 · I = 0 붉은 점 **4.1967 · 4.0648 · 3.9767 · 3.9062 · 3.9003 · 3.8957 V**. **25.6 · 51.2C(256 · 512 µA cm⁻²)는 회귀에 없다**(축 0–130 · 제외 이유 서술 0). 위 넷은 직선 · 아래 둘(9.25 · 9.50)은 휘었다(본문 "quadratic regression model"). 기울기(선형) 334 · 402 · 412 · 404 Ω cm²(Q 0–8) — §(a) 3 에서 재현.

## Fig. 5 — Q–I 회귀 외삽 (전압 다섯) (A219 · PDF p. 6 · 봤다 + 벡터) ★★★ (a)

`[도표·벡터]` 측정 점 20 = 같은 네 전류 × V = 3.0 · 3.2 · 3.4 · 3.6 · 3.8 V · 2차 회귀 · I = 0 붉은 점 **10.1138 · 10.0932 · 10.0684 · 10.0354 · 9.9612 µAh cm⁻²** — 평형 곡선의 가파른 끝(3.8 → 3.0 V)이 **0.15 µAh cm⁻² 폭** 안에 놓인다. 3.8 V 줄은 거의 직선, 나머지는 휜다.

## Fig. 6 — 측정 과전압 (A220 · PDF p. 7 · 봤다 + 벡터) ★★★ (a) · (c)

`[도표·벡터]`(Q ±0.007 · η ±0.6 mV) η = 측정 방전 전압 − **외삽** 평형 전압(그림 3 녹색 — "측정 과전압" 의 절반이 회귀 산물). 평탄(Q 2–6 중앙값) **−5.9 · −13.4 · −26.3 · −51.1 · −97.2 · −182.6 mV**(1.6 → 51.2C) → η/I **367 · 419 · 412 · 399 · 380 · 357 Ω cm²** — 율 32 배에 ±8 % 로 **선형**(옴형). Q ≈0.8 의 골은 평형 곡선 어깨 자리. 본문 "51.2 C … plateau at about −0.2 V" ✅(−0.18).

## Fig. 7 — 모형 ↔ 측정 (A220 · PDF p. 7 · 봤다 + 벡터 + 가로 ×8 확대 렌더) ★★★★ (a) · D3 · D4

`[도표·벡터]` 측정 점 = **그림 2 와 같은 3,177 점**(점 단위 |Δt| ≤0.012 분 · |ΔV| ≤0.2 mV — 보정 차) · 모형 붉은 선 5(경로 하나 = 충전 + 방전 · CV 평탄 4.193–4.211 V ↔ 측정 4.196 V). 모형 방전은 **0.222 분**의 수직 낙하로 시작하고 **3.0 V 도달 18.71 · 9.25 · 4.52 · 2.24 · 1.01 분** ↔ 측정 마지막 점 18.76 · 9.47 · 4.83 · 2.46 · 1.32 분(3.2 → 51.2C). 확대 렌더(가로 ×8)로 눈으로도 확인 — 51.2 · 25.6 · 12.8C 에서 붉은 선의 수직 낙하가 남색 점 열보다 왼쪽이다. **표지 지름 2.6 pt ≈0.81 분**이라 원 배율에서 0.2–0.3 분 차는 표지 안에 숨는다(D3). **1.6C 방전은 없다**(D4 · G7). 본문 서술과 어긋난 그림 — "Good agreement … for all discharge currents".

## Fig. 8 — 과전압 성분 (A221 · PDF p. 8 · 봤다 + 벡터 — 판마다 보정) ★★★★ (a) · (c) · D5

`[도표·벡터]` **(a) 3.2C**(본문 — 캡션은 "low-current" 만)(t ±0.01 분 · η ±0.09 mV): t = 0.2 · 1 · 2 · 5 · 10 · 13 · 16 분에 η_d(녹색) −13.7 · −8.6 · −17.2 · −8.2 · −4.3 · −0.9 · −0.9 · η_ct(빨강) −0.9 · −0.9 · −0.9 · −1.1 · −1.5 · −2.1 · −3.9 · η_mt(자홍) −4.1 · −5.4 · −5.8 · −5.8 · −5.8 · −5.8 · −5.8 · 합(검정) −18.6 · −15.1 · −23.9 · −15.1 · −11.7 · −9.0 · −10.7 mV · 끝 18.39(합) · 18.42 · 18.65 · 18.65 분. **(b) 51.2C**(t ±0.001 분 · η ±0.3 mV): t = 0.02 · 0.10 · 0.25 · 0.50 · 0.65 · 0.75 분에 η_d −67 · −120 · −107 · −56 · −24 · −13 · η_ct −13 · −15 · −19 · −27 · −38 · −56 · η_mt −40 · −56 · −70 · −86 · −93 · −97 · 합 −120 · −191 · −197 · −170 · −156 · −166 mV · **끝 0.840(합) · 0.844 · 0.847 · 0.858 분 ≈50 s**. `[재현·벡터]` η_mt / 합 몫: (b) 시간 평균 **0.449** · 앞 절반 0.353 · 뒤 절반 0.542 · 0.487 분부터 ≥0.5 · 최소 0.28 · 최대 0.61 · (a) 시간 평균 **0.458** · 최소 0.19 · 최대 0.65 · ≥0.5 인 시간 36 %. 본문 서술(8a "diffusion … largest at the beginning … mass-transfer … second … dominates in the end" · 8b "at least half … starting from the second half")은 이 그림과 맞는다 — 초록이 조건을 뗐다(D6).

## Fig. 9 — 양극 안 Li 농도 3D (A221 · PDF p. 8 · 봤다 · 판독 안 함) ★ (c)

a_LiCoO₂ [kmol m⁻³] 12–25(오른쪽 축 x 0.5–1.0) × 전극 0–300 nm × 시간 −0.5–2 분 · 51.2C · 계면 쪽에서 ≈1 분에 x → ≈1 봉우리 · 전류 끊은 뒤 x 0.9 대로 평탄(`[도표]` 3D 투시 · 폭 넓음). 본문 "After about 1 min, the current is switched off" — 그림 8b · 12 의 ≈50 s 와 다른 길이(D5).

## Fig. 10 — 전해질 안 Li⁺ 농도 3D (A221 · PDF p. 8 · 봤다 · 판독 안 함) ★ (c)

a_Li⁺ 6–16 kmol m⁻³ × 전해질 0–1.5 µm × 시간 0–3 분 · 평형 ≈10.8(본문 "11 kmol m⁻³" — `[재현]` δ·a₀ = 10.82 ✅) · Li 쪽 증가 · 양극 쪽 감소 · ≈1 분 뒤 이완. 3D 투시라 봉우리 값은 그림 12 와 대조하지 않았다.

## Fig. 11 — 전해질 과전압의 확산 · 이동 몫 (A222 · PDF p. 9 · 봤다 + 벡터) ★★★ (c) · D5 · D7

`[도표·벡터]`(t ±0.003 분 · η ±0.1 mV) 51.2C · 전류 **0 → 1.081 분** · 끝 Diffusion **−43.3** · Migration **−65.5** · Total **−108.7 mV**(본문 "110 mV" ✅) · 0.5 분에 −31.3 · −54.9 · −86.3 · 켠 직후(≈0.02 분) 이동 ≈−35 mV · 합 ≈−40 mV(본문 "a 40 mV voltage drop is instantaneously formed, which is fully carried by the electric field" — `[재현]` t = 0⁺ 순수 옴 강하는 31.5 mV, 0.6 s 에 이미 확산 −4.8 mV 가 붙는다 · D7). **그림 8b η_mt 와 같은 곡선**(0.05–0.84 분 ≤0.5 mV)인데 그림 8b 는 0.84–0.86 분에 끝나고 이 그림은 1.081 분까지 간다(D5).

## Fig. 12 — 전지 전체 농도 단면 (A222 · PDF p. 9 · 봤다 + 벡터) ★★★ (c) · (a) 5

`[도표·벡터]`(y ±0.02 µm · a ±0.013 kmol m⁻³) 왼쪽 전해질(a_Li⁺) · 오른쪽 회색 전극 1.5–1.82 µm(a_LiCoO₂ · 축 "1.82" = L + M ✅). 파랑(방전 전) 10.85 · 11.71 · 빨강(**20 s**) 15.79 → 5.70(평균 10.82) · 전극 18.09 → 13.40(평균 14.92) · 자홍(**50 s**) 17.27 → 3.77(평균 10.73) · 전극 **23.16** → 18.34(평균 19.90) kmol m⁻³. `[재현]` 전극 평균 증가 = I·t/(F·A·M) = 3.32 · 8.29 kmol m⁻³(512 µA cm⁻²) → 예측 15.03 · 20.00 ↔ 그림 14.92 · 19.90(−0.7 · −0.5 %) ✅ — **그림 12 는 512 µA cm⁻² · 20 · 50 s 와 정합**, 그리고 50 s 에 표면이 a_max(23.3)의 99.4 % — 모의 51.2C 는 여기서 끝난다(캡션 "just before the discharge current will be terminated"). 캡션 빨강 "in the middle of the discharge process" ↔ 본문 "20 s after"(50 s 중 20 s).

## 표 I — 기호 목록 (A218 · PDF p. 5 · 수동 렌더 · 봤다) ★★ (a) · D8

기호 39 줄 · 차원 · 설명. **`k₋₁` "m⁴ mol⁻⁴ s⁻¹"** — 식 3b(I_c = F A k₋₁ a_CoO₂ˢ a_Li⁺ˢ)에서 차원은 m⁴ mol⁻¹ s⁻¹ 여야 하고, 같은 표의 `k₁ˢ` "m^2.8 mol^−0.6 s^−1" 도 m⁴ mol⁻¹ s⁻¹ 로만 나온다(`[재현]` (m s⁻¹)^0.4 (m⁴ mol⁻¹ s⁻¹)^0.6) → **오기**(D8). **`r` "mol s⁻¹"** — 식 16a · 18 의 r 은 mol m⁻³ s⁻¹ 이어야 한다(D8). `a_Li` "mol m⁻³" ↔ 본문 "the activity of metallic lithium is considered unity". 음극 상수 셋(`k₂` · `k₋₂` · `k₂ˢ` 전부 "m s⁻¹")은 모형에서 안 쓰여 차원 대조 안 함.

## 표 II — 모형 매개변수 (A220 · PDF p. 7 · 수동 렌더 · 봤다) ★★★★ (a) · (b)

12 행 · 열 머리 "Estimated value"(설계값에도 붙음) · 각주 a "Design parameters"(L 1500 nm · M 320 nm · A 1 cm²) · b "Outcome of NDP analysis"(a₀ 6.01×10⁴ mol m⁻³) · c "Estimated from the design parameters and maximal capacity of the battery. All the remaining parameters are obtained from model optimization."(a_max 2.33×10⁴ mol m⁻³) · 나머지 일곱 — k_r 0.90×10⁻⁸ m³ mol⁻¹ s⁻¹ "Li⁺-ion recombination reaction rate" · δ 0.18 "Fraction of free Li⁺ ions in equilibrium" · D_Li⁺ 0.90×10⁻¹⁵ · D_n⁻ 5.10×10⁻¹⁵ · D_Li 1.76×10⁻¹⁵ m² s⁻¹ · α_LiCoO₂ 0.6 · k₁ˢ 5.1×10⁻⁶ m^2.8 mol^−0.6 s^−1. 오차 · 신뢰구간 · 유효숫자 근거 0. **k_d 는 표에 없다**(본문 식 — kd = kr a₀ δ²/(1−δ)).

## 본문 서술과 어긋난 그림 (요약)

| # | 그림 | 서술 | 어긋남 |
|---|---|---|---|
| D1 | 1a | "thicknesses … determined by SEM" · 320 nm / 1.5 µm | 띠 비 ≈0.97 ↔ 0.21 · 축척 0 — 예시 셀 |
| D2 | 2 · 7 | "followed by a 30 min relaxation period" · 캡션 "relaxation" | 4.2 V 평탄 ≈5.5 분 뒤 바로 방전 |
| D3 | 7 | "Good agreement … for all discharge currents" | 모형 3.0 V 도달이 0.05–0.31 분 이르다 · 51.2C 용량 73–78 % |
| D4 | 7 | 같은 문장 | 1.6C 방전 없음 |
| D5 | 8b · 12 ↔ 9 · 11 | "After about 1 min, the current is switched off"(9 · 10) · 12 "after 50 s … just before discharging will be terminated" | 같은 51.2C 모의가 ≈50 s(8b · 12)와 1.08 분(11) 두 길이 |
| D6 | 8 | 초록 "transport limitations … at least half of the total overpotential" | 그림 8 은 51.2C 뒷 절반에서만 ≥ 절반 · 시간 평균 45–46 % |
| D7 | 11 | "40 mV … fully carried by the electric field" | 순수 옴 강하 31.5 mV(`[재현]`) · 40 mV 는 확산이 붙은 뒤 |

---

# 절별 해체 (본문)

## 초록 (A215 · PDF p. 2)

`[인쇄]` "A mathematical model for all-solid-state Li-ion batteries is presented. The model includes the charge transfer kinetics at the electrode/electrolyte interface, diffusion of lithium in the intercalation electrode, and diffusion and migration of ions in the electrolyte. The model has been applied to the experimental data taken from a 10 µAh planar thin-film all-solid-state Li-ion battery, produced by radio frequency magnetron sputtering. This battery consists of a 320 nm thick polycrystalline LiCoO₂ cathode and a metallic Li anode separated by 1.5 µm Li₃PO₄ solid-state electrolyte." · "The model predictions agree well with the galvanostatically measured voltage profiles. **The simulations show that the transport limitations in the solid-state electrolyte are considerable and amounts to at least half of the total overpotential. This contribution becomes even larger when the current density reaches 0.5 mA cm⁻² or higher.** It is concluded from the simulations that significant concentration gradients develop in both the positive electrode and the solid-state electrolyte during a high current discharge."
- 주어가 "The simulations" — 저자도 **모형 출력**으로 적었다. 그러나 "at least half" 의 조건(51.2C · 뒷 절반 — A220)이 초록에서 빠졌다(D6) · "0.5 mA cm⁻² **or higher**" 의 "or higher" 는 모의 0(가장 높은 율 = 51.2C = 0.512 mA cm⁻² `[재현]`).
- ⚠ 텍스트 층: "µ" 가 MathematicalPi-One 글꼴의 코드 U+0001(다른 글꼴에서는 같은 코드가 괄호)로 들어 있어 추출 텍스트에는 "10 Ah" · "1.5 m" 로 보인다 — 렌더로 확인(10 µAh · 1.5 µm). 그리스 문자(δ · α · η)도 텍스트 층에서 빠진다(표 · 식은 렌더로 읽었다).

## 서론 (A215 · PDF p. 2)

`[인쇄]` 모형 계보 — 다공 전극 이론(Newman[6]) · 리뷰[2–5] · **전자 회로망 모형**(Notten · Bergveld · Kruijt[7–11]) · "the degradation (aging) process of Li-ion batteries has also been addressed.[12,13]" · "However, all these reports did not address thin-film all-solid-state Li-ion batteries." · 목표 "to develop a mathematical model for all-solid-state Li-ion batteries, which includes all important physical and electrochemical characteristics and is capable of describing the basic functionality of these devices under a wide variety of operating conditions."
- ⚠ "Simulating discharge voltage curves of Li-ion batteries already dates back to the early 1980s.[1]" — [1] 은 Doyle · Fuller · Newman **1993**(D9 · 사소).
- 매개변수 추정 · 식별성을 목표로 적지 않았다 — 목표는 "describing the basic functionality".

## 이론 1 — 전기화학 · 전하이동 (A215–A216 · PDF p. 2–3 · 식 1–13)

`[인쇄]` 반응 LiCoO₂ ⇌ Li₁₋ₓCoO₂ + xLi⁺ + xe⁻(0 ≤ x ≤ 0.5 · 식 1) · Li ⇌ Li⁺ + e⁻(식 2) · 부분 전류 I_a = F A k₁ a_LiCoO₂ˢ(식 3a) · I_c = F A k₋₁ a_CoO₂ˢ a_Li⁺ˢ(식 3b) · 속도 상수의 전위 의존(식 4 · [16]) → 평형에서 Nernst(식 7) · 교환 전류 **I⁰_LiCoO₂ = F A k₁ˢ (ā_CoO₂ ā_Li⁺)^α (ā_LiCoO₂)^(1−α)**(식 8 · k₁ˢ = (k₁⁰)^(1−α)(k₋₁⁰)^α) · 표면 / 벌크 활동도 비가 든 일반식(식 10) → "fully kinetically controlled" 에서 Butler–Volmer(식 11). 음극 같은 꼴(식 12–13). "the exchange current density for the metallic lithium electrodes[17] is much larger than that for LiCoO₂[18,19] and because the electrode areas are exactly the same for planar thin-film batteries it is to be expected that η_Li^ct is much smaller than η_LiCoO₂^ct. **For convenience, the charge transfer kinetics of the metallic lithium reaction will therefore be neglected in this work.**"
- `[재현]` 차원: 식 3b 에서 k₋₁ = m⁴ mol⁻¹ s⁻¹ · k₁ = m s⁻¹ → k₁ˢ = m^(0.4+2.4) mol^(−0.6) s⁻¹ = **m^2.8 mol^−0.6 s^−1 — α = 0.6 일 때만**(표 II 단위 ✅ · 표 I k₋₁ "mol⁻⁴" ✗ D8). ⇒ **k₁ˢ 의 단위가 적합된 α 에 묶여 있다**(α 를 바꾸면 단위가 바뀐다 — §(a) 6).
- 음극 무시는 **비교 문장**(교환 전류 값 인쇄 0)이고 "for convenience" 다 — Li | Li₃PO₄ 계면 저항이 있으면 그 몫은 양극 · 전해질 매개변수로 흡수된다(`[해석]`).
- 식 10(농도 비 포함)과 식 11(BV) 중 **모의가 어느 쪽을 썼는지 미인쇄** — 그림 8 캡션 "simulated Butler–Volmer overvoltage" 로만 읽힌다.

## 이론 2 — 전해질 확산 · 이동 (A216–A217 · PDF p. 3–4 · 식 14–20)

`[인쇄]` "The Li₃PO₄-based solid-state electrolyte is a typical ionic conductor in which **the conductivity is caused by the transport of Li⁺ ions only**." · Li₂O–P₂O₅ 유리 · nBO[20–22] · "The 'weak electrolyte' models conclude that Li may reside in the two types of states in the glass matrix and assume that the ionic conduction process is dominated by the ions, thermally populating the higher energy mobile sites.[23–25]" · 식 14 Li⁰ ⇌ Li⁺ + n⁻(k_d s⁻¹ · k_r m³ mol⁻¹ s⁻¹ · "Both constants obey Arrhenius law") — "transfer process of immobile, oxygen-binded lithium (Li⁰) to mobile Li⁺ ions leaving **uncompensated negative charges (n⁻) behind, which are chemically associated with the closest nBO's**.[22]" · 평형: a_Li⁺ = a_n⁻ = δa₀ · a_Li⁰ = (1−δ)a₀ · **k_d = k_r a₀ δ²/(1−δ)** · 두 운반체 Nernst–Planck(식 15) · 물질수지 + 경계(식 16a–d · 17a–d — n⁻ 은 두 경계에서 유속 0) · 전기중성 a = a_n⁻ = a_Li⁺ 로 "It can be shown[27]" → **식 18**: ∂a/∂t = [2D_Li⁺D_n⁻/(D_Li⁺+D_n⁻)] ∂²a/∂y² + r · a(y,0) = δa₀ · ∂a/∂y = I/(2FAD_Li⁺)(두 경계) · 전기장(식 19) · **η_mt = (RT/F) ln[a(L)/a(0)] − ∫₀ᴸ E dy**(식 20 — 첫 항 "diffusion" · 둘째 항 "migration").
- 렌더로 식 18–20 을 읽었다(텍스트 층은 그리스 문자 · 분수 손실). 26호가 옮긴 식 (22) · (23b) · (25) · (26)과 **같은 꼴**(26호 digest 전사 대조 — 원문 비교 아님).
- ⚠ **n⁻ 의 정체**: 본문은 "nBO 에 묶인 미보상 음전하" 라 쓰고(`vacanc*` **0 회**), 표 II 는 그것에 D_n⁻ = 5.10×10⁻¹⁵ m² s⁻¹(**D_Li⁺ 의 5.7 배**)를 준다 → `[재현]` t₊ = D_Li⁺/(D_Li⁺+D_n⁻) = **0.15** — 모형 안에서 전류의 85 % 를 n⁻ 가 나른다. "conductivity is caused by the transport of Li⁺ ions only" 와 같은 지면에 있다. n⁻ 를 **Li 공공**(공공의 이동 = 반대 방향 Li 이동)으로 읽으면 두 문장이 화해되지만 지면은 그렇게 쓰지 않는다(`[해석]` · 원전 파일 61 Danilov & Notten 2008 에서 확인).
- "Both constants obey Arrhenius law" — 온도 한 점(25 ℃)이라 활성화 에너지 0.

## 이론 3 — 양극 확산 · 결합 (A217–A218 · PDF p. 4–5 · 식 21–22 · 표 I)

`[인쇄]` "According to Refs. 28 and 29 Li⁺ ions in LiCoO₂ are screened by the mobile electrons … **This screening implies that the migration term can be neglected.** Assuming, for simplicity reasons, that the rate of phase transition does not play an important role and considering the diffusion coefficients in both phases to be equal" → 식 21 Fick(경계: 계면 D_Li ∂a/∂y = I/(FA) · 집전체 0 유속) · x = a/a_max · **a_max = 23.3 kmol m⁻³** · **η_d = E_eq(x_s) − E_eq(x̄) ≈ (x_s − x̄) ∂E_eq/∂x**([28,30]) · 결합 E_bat^eq = E_LiCoO₂^eq − E_Li^eq · **η = η_ct + η_d + η_mt**(식 22) · "it is indeed assumed that η_Li^ct at the metallic lithium electrode is negligibly low. Table I lists all model parameters."
- 두 상(LiCoO₂ 3.9 V 평탄)을 **고용체 Fick 하나 + 같은 D** 로 둔다 — 상전이 속도 무시(인쇄 가정).
- 표 I 은 "all model parameters" 라 했지만 **값은 표 II** 에, 그리고 표 I 에는 단위 오기 둘(D8).

## 실험 (A218–A219 · PDF p. 5–6)

`[인쇄]` "A 10 µAh planar thin-film all-solid-state Li-ion battery was deposited using an in-house built equipment, comprising a radio frequency sputtering tool with 2 in. targets (13.56 MHz) and thermal/E-beam evaporation, both placed in a glove box containing an inert argon atmosphere." · 기저 < 10⁻⁶ mbar · 하드 마스크 · 기판 Si + TiO₂/Pt(50/250 nm) · LiCoO₂ 60 W · 8×10⁻⁶ bar O₂/Ar(4:6) · 320 nm · 800 ℃ 10 min RTA(60 ℃/min) "in order to obtain the high-T crystalline phase" · Li₃PO₄ 1.5 µm · 30 W · 15×10⁻⁶ bar Ar · "**Finally, 150 nm cobalt was deposited as the current collector** at 5 Å/s via E-beam evaporation." · "constant current constant voltage (CCCV) charging with a 1.6 C-rate till the maximum voltage level of 4.2 V was reached, followed by a 30 min relaxation period and a current constant (CC) discharge. The following discharge rates were successively applied: 1.6, 3.2, 6.4, 12.8, 25.6, and 51.2 C." · Biologic VMP3 · 25 ℃.
- ⚠ **Li 음극 증착 문장 0**(G2) — 마지막 증착 층 = Co 집전체. CV 종료 조건(전류 · 시간) 미인쇄 · 셀 수 · 반복 0 · "Li₃PO₄ target … Ar" — 질소 0 → 이론 절의 "either or not N-doped" 중 **N 없음**(LiPON 아님 — 26호 셀(Raijmakers 데이터)은 LiPON).
- `[재현]` **C-rate 삼각 검사**: 공칭 10 µAh · A 1 cm² → 1C = 10 µA cm⁻² → 51.2C = **0.512 mA cm⁻²** ↔ 초록 "0.5 mA cm⁻²" ✅ · 그림 4 · 5 전류 15.91 · 32.06 · 63.99 · 128.04 µA cm⁻²(`[도표·벡터]`) ↔ 16 · 32 · 64 · 128 ✅ · 측정 평형 용량 10.10 µAh cm⁻²(그림 3) ↔ 공칭 10 µAh(+1 %) ✅ · 그림 12 전극 평균 증가 ↔ 512 µA cm⁻² × 20 · 50 s ✅(−0.5 … −0.7 %) · 부피 용량 10 µAh / (1 cm² × 0.32 µm) = 31.3 µAh cm⁻² µm⁻¹.

## 결과 · 논의 (A219–A222 · PDF p. 6–9 · 그림 2–12 · 표 II)

`[인쇄]` 그림 2 "It is remarkable to see that these thin-film batteries can be discharged with extremely high currents up to 51.2 C-rate." · 그림 3 평형 곡선 "Note that the equilibrium voltage of the battery is equal to that of the positive electrode as the voltage of the metallic Li electrode is 0 V vs Li/Li⁺" · "**The equilibrium voltage has been determined by regression extrapolation (see Chap. 4 in Ref. 31). The regression extrapolation was applied separately on the flat and steep parts of the equilibrium voltage curve.**" · 그림 4 "A linear relationship between the current density and voltage is found for the low Qout values up to 8 µAh cm⁻². At low state-of-charges, a nonlinear dependence is found, which can be well approximated by a quadratic regression model." · 그림 5 "For all voltages, nonlinear dependencies … approximated by a quadratic regression. Qout can then be found by extrapolating toward zero current." · "The difference between the equilibrium voltage and the discharge voltage is the overpotential." · 그림 7 "**Figure 7 shows the optimized simulations obtained with the applied model. Good agreement is obtained between the experimental results (blue dots) and the theoretical prediction (red lines) for all discharge currents. The optimized parameters are listed in Table II.**" · 그림 8a(3.2C) 성분 순서 · 8b "**This overpotential across the electrolyte is responsible for at least half of the total overpotential starting from the second half of the discharge process.**" · "The simulated total overpotential agrees well with the experimentally determined overpotentials plotted in **Fig. 5**: in the case of a 51.2 C-rate discharge simulation, a wide overpotential plateau at about −0.2 V is calculated which is in good agreement with the experimentally determined overpotential in **Fig. 6** (black line)." · "diffusion inside the LiCoO₂ electrode is the leading process, inducing the current interruption at the battery cutoff voltage of 3.0 V." · 그림 9 "The diffusion coefficient for Li in the electrode has been analyzed to be 1.76 × 10⁻¹⁵ m² s⁻¹, which also agrees well with the reported experimental results.[32,33] After about 1 min, the current is switched off" · 그림 10 "equilibrium value of 11 kmol m⁻³" · 그림 11 "a 40 mV voltage drop is instantaneously formed, which is fully carried by the electric field … in total amounting to 110 mV" · "The thicknesses of the electrode (M) and the electrolyte (L) have been determined by scanning electron microscopy (SEM). The total number of Li in the Li₃PO₄ electrolyte has been analyzed by neutron depth profiling (NDP) to be a₀ = 6.01 × 10⁴ mol m⁻³. **The simulations show that, in equilibrium, only about 18% of the Li atoms are mobile and that the Li-ion recombination reaction rate is moderately large (k_r = 0.9 × 10⁻⁸ m³ mol⁻¹ s⁻¹). Both diffusion coefficients are estimated to be of the order of 10⁻¹⁵ m² s⁻¹.**" · 그림 12 · "The simulated total overpotential corresponds to charge transfer resistances of the order of 50–100 Ω at the voltage plateau but obviously increases at the end of discharging. This is also in good agreement with the reported experimental results.[18,19]"
- **k_r 은 표(A220)와 본문(A221) 두 자리에 같은 0.9×10⁻⁸ 로 인쇄**돼 있다 — §(a) 5 의 ×100 은 한 자리 오식이 아니라 두 자리에 같은 값이다(`[해석]` 원인 미상 — 단위 환산 · 코드 단위 · 오기 중 무엇인지 지면으로 못 가른다). `[해석]` "moderately large" 는 ×100 값(반응 이완 ≈46 s)에 더 맞는 말이다 — 인쇄 값이면 이완 ≈77 분이라 51.2C(≈1 분) 동안 반응이 사실상 꺼져 있다(§(a) 5).
- "Fig. 5" → 문맥상 **그림 6**(그림 5 는 Q–I 회귀) — 상호 참조 오기(D10).
- "1.76 × 10⁻¹⁵ … agrees well with the reported experimental results[32,33]" — 문헌값이 인쇄되지 않았다(대조 수치 0).
- "50–100 Ω" — 단위 Ω(면적 1 cm² 이라 Ω cm² 와 같은 수) · 지시 대상 "total overpotential" 인데 그림 6 η/I = 357–419 Ω cm², 그림 8 η_ct/I = 26–66 Ω cm²(`[도표·벡터]`) — 수는 η_ct 쪽과 같은 자릿수(D11).

## 결론 · 사사 (A222 · PDF p. 9)

`[인쇄]` "A one-dimensional model has been applied to simulate the performance of all-solid-state Li-ion batteries. The model describes the electrode, electrolyte, and the interface between those elements. The proposed model provides a detailed information about the various diffusion and migration fluxes, concentration profiles, and the corresponding overpotential contributions, occurring across the electrode and electrolyte. **The model provides good fits with the measurements, including discharge curves with high C-rates.**" — 결론은 "good fits" 하나이고, 매개변수 값 · 전해질 절반 명제는 결론에 다시 오르지 않는다. 사사 EU FP7 Superlion.

---

# ★ (a) 매개변수 추정의 실체 (Q4)

## 1. 표 II 행별 — 출처 층위 (`[인쇄]` 각주 · 본문 → 우리 재현 · 대조)

| # | 이름 | 값 · 단위 `[인쇄]` | 출처 층위 (지면 근거) | 우리 재현 · 대조 |
|---|---|---|---|---|
| 1 | `L` | 1500 nm | **설계**(각주 a) · 본문 "determined by SEM" | 그림 1a 는 예시 셀 · 축척 0(D1 · D14) — 측정인지 설계인지 지면으로 못 가른다 |
| 2 | `M` | 320 nm | **설계**(각주 a) · 본문 "determined by SEM" | 같음 · 그림 12 전극 폭 1.5–1.82 µm ✅ |
| 3 | `A` | 1 cm² | **설계**(각주 a · 하드 마스크) | `[재현]` C-rate 삼각 검사 ✅(실험 절) · 기하 면적 = 반응 면적 가정 |
| 4 | `a₀` | 6.01×10⁴ mol m⁻³ | **측정**(각주 b · NDP — 자료 0 · G5) | `[재현]` Li₃PO₄ 식량 115.79 g mol⁻¹ 로 **밀도 2.32 g cm⁻³** 에 해당 |
| 5 | `a_max` | 2.33×10⁴ mol m⁻³ | **유도**(각주 c "Estimated from the design parameters and maximal capacity") | `[재현·가정]` 10 µAh ÷ (F × Δx 0.5 × 320 nm × 1 cm²) = **23.32 kmol m⁻³** ✅(Δx 0.5 = 식 1 의 0 ≤ x ≤ 0.5) · `[재현·외부 값]` 조밀 LiCoO₂(5.05 g cm⁻³ · 97.87 g mol⁻¹ — 원문 밖 값) 격자 Li ≈51.6 kmol m⁻³ 의 **45 %** → 물질 상수가 아니라 **용량 맞춤 유효값**(본문은 "the maximal activity of Li in LiCoO₂" 라 부름) |
| 6 | `k_r` | 0.90×10⁻⁸ m³ mol⁻¹ s⁻¹ | **적합**("model optimization") · 본문 A221 에도 같은 값 · "moderately large" | `[재현]` 그림 8a · 11 · 12 는 **≈0.90×10⁻⁶(×100)** 으로만 재현(§5) · CRB ×1.40 |
| 7 | `δ` | 0.18 | **적합** · 본문 "The simulations show that … only about 18% of the Li atoms are mobile" | `[재현]` δa₀ = 10.82 kmol m⁻³ ↔ 본문 "11" · 그림 12 파랑 10.85 ✅ · CRB ×1.42 · ρ(δ, D_Li⁺) **−0.999** |
| 8 | `D_Li⁺` | 0.90×10⁻¹⁵ m² s⁻¹ | **적합** · "of the order of 10⁻¹⁵" | CRB ×1.87(일곱 중 가장 약함) |
| 9 | `D_n⁻` | 5.10×10⁻¹⁵ m² s⁻¹ | **적합** | `[재현]` t₊ 0.15 · CRB ×1.36 |
| 10 | `D_Li` | 1.76×10⁻¹⁵ m² s⁻¹ | **적합** · "agrees well with the reported experimental results[32,33]"(값 인쇄 0) | `[재현]` M²/D_Li = **58 s**(51.2C 방전 ≈60 s 와 같은 자릿수) · CRB ×1.005 |
| 11 | `α` | 0.6 | **적합** | CRB ×1.03 · 단위(행 12)를 정한다 |
| 12 | `k₁ˢ` | 5.1×10⁻⁶ m^2.8 mol^−0.6 s^−1 | **적합** · 단위가 α = 0.6 에 묶임 | `[재현]` 인쇄 단위 i₀ = **151 A** ↔ 그림 ≈1 mA(§6) |
| — | `k_d` | 표 없음 | **유도**(식: k_r a₀ δ²/(1−δ)) | `[재현]` 2.14×10⁻⁵ s⁻¹(인쇄 k_r) · 2.14×10⁻³ s⁻¹(×100) |
| — | `T` | 25 ℃ | 실험 조건 = 모의 | 298.15 K 로 계산 |
| — | `E_eq(x)` | 그림 3 녹색(함수형 0) | **같은 데이터의 회귀 외삽**(§3) | 우리 재풀이는 녹색 벡터 경로를 썼다(G9) |

⇒ **12 행 = 설계 3 · 측정 1 · 유도 1 · 적합 7.** 적합 일곱의 **불확실성 · 유효숫자 근거 · 상관 0.** 측정 하나(`a₀`)도 자료 · 불확실성 0.

## 2. 무엇에 · 어떻게 맞췄나

- **무엇에** — 그림 7 이 유일한 적합 그림이다: 측정 **1.6C CCCV 충전**(다섯 번 겹친 곡선 · 모형 선도 충전 구간을 그린다 — CV 평탄 4.193–4.211 V) + **3.2–51.2C 방전 다섯**. **1.6C 방전 모의는 지면 0**(G7). 충전 구간을 손실에 넣었는지 · 3.0 V 근처 가중 · 율별 가중 — 미인쇄.
- **어떻게** — 손실 함수 · 알고리즘 · 시작점 · 다중 시작 · 정지 · 반복 · 잔차 **전부 0**(G1). 지면의 말은 "optimized simulations" · "optimized parameters" · "obtained from model optimization" 셋.
- **잔차가 남긴 흔적**(`[도표·벡터]` §7): 모형의 3.0 V 도달이 **모든 고율에서 이르다**(부호 있는 잔차 — 모형이 끝에서 손실을 **많게** 본다). 26호(같은 계보 · 다른 데이터)의 부호 있는 잔차("Experimental Values are lower than Simulated Values" — 고율에서 모형 손실 **부족**)와 **반대 방향**이다(26호 digest 전사 대조).

## 3. 평형 전압 — 측정인가 모형인가 (그림 3–5 · `[도표·벡터]` → `[재현]`)

**측정에서 나온 회귀값이다 — 전기화학 모형은 쓰지 않았지만, 외삽 함수(선형 / 2차) · 점 선택(네 율)이 가정이고 불확실성 0 이다.** 그리고 그 곡선이 (i) 모형의 E_eq(x) · η_d 정의 · 컷오프에, (ii) 그림 6 "측정 과전압" 의 기준선에 다시 들어간다 — **같은 방전 곡선을 평형 곡선과 과전압 적합에 두 번 쓴다**(`[해석]`).

그림 4(V–I · 전류 15.91 · 32.06 · 63.99 · 128.04 µA cm⁻²):

| Q_out µAh cm⁻² | 측정 V (네 전류) `[도표·벡터]` | 인쇄 붉은 점 | 우리 선형 절편 | 우리 2차 절편 | 선형 − 2차 | 선형 기울기 |
|---|---|---|---|---|---|---|
| 0 | 4.1909 · 4.1897 · 4.1759 · 4.1551 | 4.1967 | 4.1980 | 4.1970 | +1.0 mV | 334 Ω cm² |
| 2 | 4.0567 · 4.0498 · 4.0371 · 4.0115 | 4.0648 | 4.0628 | 4.0631 | −0.3 mV | 402 |
| 4 | 3.9698 · 3.9630 · 3.9490 · 3.9236 | 3.9767 | 3.9761 | 3.9772 | −1.1 mV | 412 |
| 8 | 3.9003 · 3.8947 · 3.8819 · 3.8553 | 3.9062 | 3.9073 | 3.9063 | +1.0 mV | 404 |
| 9.25 | 3.8888 · 3.8749 · 3.8437 · 3.7627 | 3.9003 | 3.9107 | **3.9008** | **+10.0 mV** | (휨) |
| 9.50 | 3.8795 · 3.8576 · 3.8043 · 3.6446 | 3.8957 | 3.9241 | **3.8956** | **+28.4 mV** | (휨) |

그림 5(Q–I · V = 3.0–3.8 V · 2차):

| V | 인쇄 붉은 점 | 우리 2차 절편 | 우리 선형 절편 | 선형 − 2차 |
|---|---|---|---|---|
| 3.0 | 10.1138 | 10.1150 | 10.0535 | −0.061 |
| 3.2 | 10.0932 | 10.0924 | 10.0327 | −0.060 |
| 3.4 | 10.0684 | 10.0670 | 10.0035 | −0.064 |
| 3.6 | 10.0354 | 10.0350 | 9.9752 | −0.060 |
| 3.8 | 9.9612 | 9.9597 | 9.9700 | +0.010 |

- `[재현]` 저자 붉은 점 열한 개를 **±2 mV · ±0.0015 µAh cm⁻²** 로 다시 냈다(Q ≤ 8 은 선형 · 9.25 · 9.5 · 그림 5 는 2차 — 본문 서술과 맞다). 그림 3 녹색 곡선은 그림 4 점과 ≤2.2 mV · 그림 5 점과 −0.012 … −0.017 µAh cm⁻²(보정 폭의 두 배 안).
- **모형 의존 폭**: 2차는 네 점에 매개변수 셋 = **자유도 1** · 가장 높은 두 율(25.6 · 51.2C)은 버렸다(이유 0). 선형 ↔ 2차 선택만으로 Q 9.25 · 9.5 의 평형 전압이 **10 · 28 mV**, 가파른 끝(3.0–3.6 V)의 위치가 **0.06 µAh cm⁻²**(= 가파른 끝 전체 폭 0.15 의 40 %) 움직인다. 저자는 이 폭을 적지 않았다.
- 선형 기울기 334–412 Ω cm²(Q 0–8)와 그림 6 η/I 357–419 Ω cm² 가 같은 자릿수 — "총 저항 ≈0.4 kΩ cm²" 가 데이터가 직접 주는 양이다.

## 4. 오차 · 신뢰구간 · 다중 시작 · 상관 · 식별성 — 어휘 집계 (요약 · 전체는 아래 "어휘 집계")

`identifiab*` · `uniqu*` · `confiden*` · `uncertain*` · `sensitiv*` · `error*` · `±` · `deviation` · `residu*` · `RMS` · `least squares` · `correlat*` **본문 전수 0**(NFKC 전후 같음 · 표지 `correlat` 1 은 IOP 추천 논문 제목). `fit*` 0 → **1**(NFKC 뒤 — "good ﬁts" 의 ﬁ 합자) · `optimi*` 3 · `regression*` 7 · `extrapolat*` 8 · `estimat*` 3 · `agree*` **9**. ⇒ **오차 막대 · 신뢰구간 · 다중 시작 · 상관 · 식별성 언급 0.** 일치는 아홉 번 말했다.

## 5. ★★★★ 재풀이 — 인쇄 표로 저자 그림을 다시 푼다 (`[재현]` · 코드 `scratchpad` · 커밋 안 함)

갈바노스태틱이라 전해질 부분계(식 14 · 18–20)는 양극과 떨어져 혼자 풀린다. 우리는 식 18(앰비폴라 확산 + 반응 r = k_d(a₀ − a) − k_r a² · 경계 ∂a/∂y = I/(2FAD_Li⁺))을 유한체적 300 칸 · BDF 로 풀고 식 19 · 20 으로 확산 · 이동 몫을 냈다(T 298.15 K · A 1 cm² · L 1.5 µm · 512 / 32 µA cm⁻²).

| 비교 (`[도표·벡터]` 지면 ↔ 우리) | 지면 | 표 II 그대로 | `k_r` ×100 |
|---|---|---|---|
| 그림 11 · 8b 전해질 합 @15 s | −70.2 | −76.3 | **−71.4** |
| @30 s | −86.3 | −102.9 | **−86.9** |
| @50.4 s | −100.9 | −149.3 | **−101.4** |
| @64.9 s | −108.7 | −226 | **−109.1** |
| 그림 11 확산 / 이동 @64.9 s | −43.3 / −65.5 | −104 / −122 | **−43.5 / −65.6** |
| 그림 12 a(0) · a(L) @20 s (kmol m⁻³) | 15.79 · 5.70 | 16.63 · 5.01 | **15.82 · 5.65** |
| 그림 12 a(0) · a(L) @50 s | 17.27 · 3.77 | 19.98 · 1.64 | **17.26 · 3.73** |
| 그림 8a 3.2C η_mt @0.2 · 1 · 2 · 10 분 (mV) | −4.10 · −5.45 · −5.82 · −5.82 | −4.24 · −7.04 · −9.04 · −12.77 | **−4.06 · −5.51 · −5.83 · −5.90** |
| 그림 11 네 시각 RMS | — | 64.0 mV | **0.8 mV** |

- 배수 훑기(RMS · 그림 11 네 시각): ×1 64.0 · ×3 59.4 · ×10 47.7 · ×30 28.7 · ×60 13.0 · ×80 6.0 · ×90 3.1 · ×95 1.8 · **×100 0.8** · ×105 1.0 · ×110 2.0 · ×120 4.1 · ×150 9.5 · ×300 24.6 · ×1000 42.0 mV. 대안 하나(D_Li⁺ · D_n⁻ 함께 ×2 · ×4)는 23.2 · 51.7 mV. **다른 매개변수 조합은 훑지 않았다 — 유일성은 주장하지 않는다**(§8 의 골짜기가 있으므로 다른 조합이 맞을 수도 있다; 우리 주장은 "인쇄된 열한 값 중 `k_r` 하나만 바꾸면 그림 셋이 동시에 맞는다" 까지).
- `[재현·선형]` **인쇄 값에서의 정상 한계 전류** ≈ 4FAD_Li⁺δa₀/L ÷ (tanh(κL/2)/(κL/2)) = 250 ÷ 0.975 ≈ **257 µA cm⁻²** < 51.2C 512 µA cm⁻² — 인쇄 값이면 51.2C 에서 양극 쪽 전해질이 ≈65 s 에 고갈된다(우리 풀이 a(L) 0.37 kmol m⁻³ @65 s · 반무한 Sand 근사 69 s). ×100 값이면 κL/2 = 2.82 · 한계 ≈710 µA cm⁻² — 그림 12 50 s 의 3.77 kmol m⁻³ 과 맞는다.
- `[재현]` **반응 이완 시간**(선형): 1/(k_d + 2k_r δa₀) = **4,628 s ≈77 분**(인쇄) ↔ **46 s**(×100). 해리 시간 1/(k_r a₀) = 1,849 s(인쇄) ↔ **18.5 s**(×100) — 26호가 Raijmakers 값으로 낸 "≈20 s" 와 같은 자릿수(26호 §5-2 ④ 전사 대조). 전해질 확산 L²/(π²D_amb) = 149 s(D_amb = 2D_Li⁺D_n⁻/(D_Li⁺+D_n⁻) = 1.53×10⁻¹⁵ m² s⁻¹).
- `[재현]` **전도도 · 옴 강하**: σ = (F²/RT) δa₀ (D_Li⁺ + D_n⁻) = **2.44×10⁻⁶ S cm⁻¹** · R_ohm(1 cm²) = **61.5 Ω** · t₊ = 0.15 · 반응 없는 정상 R = R_ohm/t₊ = 410 Ω — 51.2C 의 t = 0⁺ 순수 옴 강하 **31.5 mV**(본문 "40 mV … fully carried by the electric field" — 우리 풀이 0.6 s 에 합 −39.7 · 이동 −34.9 · 확산 −4.8 mV · D7).
- **해석 경계**: ×100 이 인쇄 오기인지(두 자리 같은 값 — 표 II · A221), 코드의 단위 관례인지, 다른 적합점인지 지면으로 못 가른다. 확정인 것은 **"인쇄 값 그대로는 저자 그림이 재현되지 않고, ×100 이면 재현된다"** 는 비교표 자체다.

## 6. ★★★ `k₁ˢ` → i₀ — 단위 관례 (`[재현]`)

그림이 요구하는 교환 전류(x ≈ 0.5 · a_Li⁺ = δa₀): 그림 8b 0.02 분 η_ct −13.2 mV @512 µA → BV(음극 가지 지수 1−α = 0.4) **i₀ = 1.04 mA** · 그림 8a η_ct −0.906 mV @32 µA(선형) **0.91 mA**. 식 8 · 표 II 값으로 같은 상태의 i₀ 를 세 관례로 내면:

| 관례 | (ā_CoO₂ā_Li⁺)^0.6 (ā_LiCoO₂)^0.4 | i₀ = F A k₁ˢ × (…) | 그림 대비 |
|---|---|---|---|
| 인쇄 단위 — mol m⁻³ · A = 10⁻⁴ m² | 3.07×10⁶ | **151 A** | ×1.5×10⁵ |
| kmol m⁻³ · A = 10⁻⁴ m² | 48.6 | 2.39 mA | ×2.4 |
| mol cm⁻³ · A = 1 cm² | 7.71×10⁻⁴ | 0.38 mA | ×0.4 |

- **어느 관례도 그림의 ≈1 mA 와 맞지 않는다** → `k₁ˢ` 는 단위 관례 미인쇄(G8)로 **재사용 불가** — 옮길 때는 i₀(mA cm⁻² · 기준 x · 기준 전해질 농도)로 옮겨야 한다(`[해석]`). 그리고 단위가 α 에 묶여 있어 **α 가 다른 모형(26호 α 0.5 고정)으로 숫자를 옮길 수 없다.**
- 우리 재풀이(§7)는 i₀ 를 하나의 손잡이(x = 0.5 기준 1.0 mA · 우리가 고른 x · a 의존 꼴)로 두었다 — 그림 8b η_ct 의 시간 모양은 우리 꼴이 지면보다 끝에서 빨리 커진다(0.5 분 −38 ↔ −27 mV) · 지면의 i₀(x) 구현은 미인쇄.
- "charge transfer resistances of the order of 50–100 Ω"(A222): 그림 8 η_ct/I = **26–66 Ω cm²**(평탄 구간 `[도표·벡터]`) · 선형 i₀ ≈1 mA → RT/(F i₀) ≈ **26 Ω cm²** — 같은 자릿수. 문장의 주어 "simulated total overpotential"(η/I 357–419 Ω cm²)와는 아니다(D11).

## 7. ★★★★ 율별 끝 용량 — "good agreement for all discharge currents" 의 범위

| 율 | 측정 Q(3.0 V) 그림 3 `[도표·벡터]` | 측정 3.0 V 앞 마지막 점 그림 7 | 모형 3.0 V 도달 그림 7 | 모형 지속(시작 0.222 분) → Q | 우리 재풀이 컷오프 → Q | 모형 / 측정 |
|---|---|---|---|---|---|---|
| 51.2C | 9.170 | 1.319 분 | 1.010 분 | 0.788 → 6.72 | 0.843 → 7.19 | **73–78 %** |
| 25.6C | 9.567 | 2.461 | 2.239 | 2.017 → 8.61 | 2.020 → 8.62 | **90 %** |
| 12.8C | 9.758 | 4.825 | 4.522 | 4.300 → 9.17 | 4.375 → 9.33 | **94–96 %** |
| 6.4C | 9.862 | 9.473 | 9.251 | 9.029 → 9.63 | 9.095 → 9.70 | 98 % |
| 3.2C | 9.949 | 18.756 | 18.709 | 18.487 → 9.86 | 18.534 → 9.89 | 99 % |
| 1.6C | 10.039 | — | — | 그림 없음 | 37.381 → 9.97 | (99 %) |

- 우리 재풀이 = 표 II(+ `k_r` ×100 · i₀ 1.0 mA · E_eq = 그림 3 녹색 · x₀ = 11.711/23.3 — 그림 12 파랑)의 전 셀 모의 — 그림 7 모형 지속을 0.003–0.075 분 안으로 다시 내고 그림 8b 끝(0.840 분)과 같다. 51.2C 컷오프 순간 **표면 x = 1.000**(그림 12 의 23.16/23.3) — 양극 표면 포화가 끝을 정한다(본문 "diffusion inside the LiCoO₂ electrode is the leading process" ✅).
- ⇒ **모형은 51.2C 에서 측정 용량의 22–27 % 를 못 낸다**(25.6C 10 % · 12.8C 4–6 %). 그림 7 의 65 분 축에서 차 0.2–0.3 분은 표지 지름(≈0.81 분) 안이다. "The model provides good fits with the measurements, including discharge curves with high C-rates"(결론)는 **시간 축 그림의 시각적 일치**이고, 고율 끝 용량 잔차를 적지 않은 판정이다.
- `[해석]` 잔차의 모양(율이 높을수록 커짐 · 표면 포화로 끝남)은 양극 쪽 구조(단일 Fick · 두 상 무시 · a_max 고정 · D_Li 하나)가 고율 끝을 못 따라가는 **모형 구조 오차**의 후보다 — 매개변수가 그 오차를 흡수했는지는 G1 때문에 모른다.

## 8. ★★★ 국소 CRB — 우리가 공급하는 식별 경계 (`[재현·가정]` · 지면에 없는 계산)

**가정**: 우리 재풀이 모형(§7) · 적합 일곱(`k_r` ×100 · `δ` · `D_Li⁺` · `D_n⁻` · `D_Li` · `α` · i₀ — `k₁ˢ` 대신 i₀) · 출력 = 여섯 율 방전 전압 V(t) · 각 율 컷오프 시각의 2–85 % 구간 30 점 · 백색 잡음 σ_V = **1 mV**(낙관적 — 잡음이 5 mV 면 표준편차 ×5) · ln 매개변수 · 중앙차분 ±2 %. **저자가 한 분석이 아니다.**

| 매개변수 | 1σ (ln) | ×배 | 율별 rms ∂V/∂ln θ (1.6 → 51.2C, mV) |
|---|---|---|---|
| `k_r` | 0.338 | ×1.40 | 0.9 · 1.8 · 3.5 · 6.5 · 10.9 · 15.9 |
| `δ` | 0.352 | ×1.42 | 4.0 · 7.9 · 15.7 · 30.9 · 62.0 · 137.7 |
| `D_Li⁺` | **0.626** | **×1.87** | 1.6 · 3.2 · 6.3 · 12.7 · 26.3 · 62.6 |
| `D_n⁻` | 0.305 | ×1.36 | 0.4 · 0.8 · 1.7 · 3.5 · 7.3 · 15.7 |
| `D_Li` | 0.005 | ×1.005 | 4.6 · 10.8 · 22.4 · 32.9 · 43.4 · 64.9 |
| `α` | 0.027 | ×1.03 | 0.6 · 1.3 · 3.0 · 7.5 · 24.2 · 92.7 |
| i₀ | 0.099 | ×1.10 | 0.6 · 1.2 · 2.6 · 5.7 · 13.8 · 33.7 |

- 상관(CRB 공분산): **`δ`–`D_Li⁺` −0.999 · `k_r`–`δ` −0.996 · `k_r`–`D_Li⁺` +0.994 · `D_n⁻`–(`k_r` · `δ` · `D_Li⁺`) |0.98|** · `α`–(전해질 넷) |0.87–0.93| · `D_Li` 와 나머지 ≤0.53.
- Fisher 고유값 1.39 · 104 · 701 · 2.74×10³ · 1.73×10⁴ · 1.09×10⁵ · 1.31×10⁶ → **조건수 9.5×10⁵**. 가장 약한 방향(고유값 1.39 · 1σ ≈ ln 0.85 = ×2.3) = **`D_Li⁺` −0.74 · `δ` +0.41 · `k_r` −0.40 · `D_n⁻` −0.36**(양극 셋 성분 ≤0.06) — δ 를 올리고 세 수송 · 반응 상수를 함께 내리면 전압이 거의 안 변한다. 둘째(104) = i₀ +0.88 · `D_n⁻` −0.41.
- ⇒ **전해질 넷은 한 묶음으로만 정해진다**(전도도 σ ∝ δ(D_Li⁺ + D_n⁻) · 경계 기울기 ∝ 1/D_Li⁺ · 반응 k_r δa₀ — 26호 §5-2 ④ 의 `[추론]` "전도도형 한 조합" 에 원형 모형의 수치). "only about 18 % of the Li atoms are mobile"(`δ`)은 **골짜기 위의 한 좌표**다. 반대로 `D_Li` · `α` · i₀ 는 여섯 율이 국소적으로 잘 정한다(단 `a_max` 를 고정했기에 — 26호 §5-2 ② 의 `D·a_max` 대칭은 각주 c 가 깼다).
- 한계: 국소(한 점) · 우리 모형 꼴(i₀(x) 꼴 · E_eq = 그림 녹색)이 지면과 같다는 보장 0 · 컷오프 근처(85 % 뒤)와 충전 구간을 뺐다 · σ_V 가정.

## 9. 판정 (Q4)

**Q4 0/91 — 여든세 번째 성질.** 기준(10호 이래 — "이 조합은 이 데이터로 유일하게 정해지지 않는다" 를 지면이 계산으로 보였나): **0**. 이 편은 일곱 손잡이를 한 셀의 여섯 율 곡선에 "모형 최적화" 로 맞추고(방법 · 손실 · 잔차 · 불확실성 0), 평형 곡선은 같은 곡선 넷의 회귀 외삽으로 만들었으며(자유도 1 · 모형 의존 폭 미보고), 표에 인쇄한 `k_r` 는 자기 그림과 ×100 어긋나고(그림 값 ≈0.9×10⁻⁶), `k₁ˢ` 는 단위 관례가 i₀ 를 재현하지 않고, 51.2C 끝 용량 22–27 % 미달을 시간 축 그림의 표지 폭 속에 둔 채 "for all discharge currents" 로 읽었다 — 그리고 전해질 넷이 |상관| ≥ 0.98 의 한 묶음이라는 것은 **우리 국소 CRB 가 처음 보인다**(저자 판정 아님 · 칸 이동 근거 아님).
**여든세 번째 성질 = "계보 첫 매개변수 표를 방법 · 잔차 없이 인쇄하고, 그 표의 값 하나가 자기 그림을 재현하지 않으며(×100), 같은 데이터의 회귀 외삽을 평형 곡선으로 되먹인 적합에서 고율 용량 미달을 시간 축의 시각적 일치로 덮는다."**

---

# ★ (b) 26호 계보 대조 — 이 편이 계보의 **첫 매개변수 표**

26호(Iwakiri 2024)는 이 편을 [15] 로 인용하고(Table 1 "Parameter Estimation Yes" 넷 중 하나 · 후속 ★★★), 자기 표의 "문헌값" 은 **Raijmakers 2020**(파일 58)에서 왔다고 적었다(26호 digest — 원문 대조는 파일 58 에서). 같은 이름끼리(26호 값은 26호 digest §3-2 전사 · 원문 재열람 0):

| 이름 (이 편 ↔ 26호) | 이 편 `[인쇄]` 층위 | 26호 "문헌" | 26호 "최적" | 관계 |
|---|---|---|---|---|
| `k_r` ↔ `k_r` | 0.90×10⁻⁸ 적합 (그림 재현 ≈0.90×10⁻⁶ `[재현]`) | 8.00×10⁻⁷ | 8.40×10⁻⁷ | 인쇄 값과 ×89 · **그림 재현 값과 같은 자릿수**(×0.89) |
| `δ` ↔ `δ` | 0.18 적합 | 0.64 | 0.64 | 다름(×3.6) — 다른 SE(Li₃PO₄ ↔ LiPON) |
| `a₀` ↔ `a₀` | 6.01×10⁴ NDP 측정 | 61 141 | 64 198 | **1.7 % 차**(26호에서는 적합 변수) |
| `D_Li⁺` ↔ `D_M⁺` | 0.90×10⁻¹⁵ 적합 | 1.73×10⁻¹⁶ | 1.8165×10⁻¹⁶ | ×0.19 |
| `D_n⁻` ↔ `D_n⁻` | 5.10×10⁻¹⁵ 적합 | 5.69×10⁻¹⁶ | 5.9745×10⁻¹⁶ | ×0.11 |
| `a_max` ↔ `a^max_M⊕` | 2.33×10⁴ 유도(용량 · Δx 0.5) | 3.22×10⁴ | 3.381×10⁴ | ×1.4 — 26호에서는 적합 변수 |
| `D_Li` ↔ `D⁰_M⊕` | 1.76×10⁻¹⁵ 적합(단일 Fick) | 1.21×10⁻¹³ | 1.2705×10⁻¹³ | 다른 모형(26호 = 이온 · 전자 쌍극 확산 × β) |
| `α` ↔ `α` | 0.6 적합 | 0.5 고정 | — | 다름 → `k₁ˢ` 단위가 다르다 |
| `k₁ˢ` ↔ `k¹_s` | 5.1×10⁻⁶ m^2.8 mol^−0.6 s^−1 적합 | 1.53×10⁻¹¹ | 1.60×10⁻¹¹ | 단위 관례가 달라(α) 숫자 비교 불가 — i₀ 로만(26호 §5-2 ⑤ 는 문헌값으로 i₀⁺ ≈0.47 mA cm⁻² 를 냈다) |
| — ↔ `D⁰_e⁻` | **없음**(양극 이동항 무시 — "screened by the mobile electrons"[28,29]) | 5.06×10⁻¹³ | **5.24×10⁻³** | — |
| — ↔ `k²_s` | 없음(음극 동역학 무시) | 1.09×10⁻⁹ | 1.1445×10⁻⁹ | — |

- **같은 값 0 / 9** — 이 편 셀(Li₃PO₄ 1.5 µm · LCO 320 nm · 1 cm² · 10 µAh)과 26호 데이터 셀(LiPON 3.62 µm · LCO 8.08 µm · 3.36 cm² · 0.7 mAh — 26호 digest)이 다르므로 **값의 직접 상속은 없다.** 상속된 것은 **모형 구조**(해리 SE + 두 운반체 · 식 18–20 과 같은 꼴 · BV + Fick · 과전압 합)와 **매개변수 이름 · 적합 관행**이다.
- **`D_e⁻` 10 자릿수 어긋남은 이 편에서 시작되지 않는다** — 이 편에는 `D_e⁻` 가 없다(양극 = 단일 `D_Li` Fick). 그 매개변수는 26호 이전 계보(Raijmakers 2020 의 쌍극 확산 — 파일 58 에서 확인)에서 들어왔다.
- **이 편에서 시작되는 것** — (i) **인쇄 값의 자릿수 문제**(`k_r` ×100 — 그리고 그 그림 재현 값 ≈0.9×10⁻⁶ 이 26호 "문헌" 8.00×10⁻⁷ 과 같은 자릿수라, Raijmakers 의 `k_r` 가 이 편의 **인쇄 값이 아니라 다른 경로**(재적합 · 다른 셀 · 정정된 값)로 왔을 가능성 — 파일 58 에서 확인할 물음), (ii) **단위 관례 미인쇄**(`k₁ˢ` — α 에 묶인 단위), (iii) **용량 맞춤 `a_max`**(물질 상수 이름 · 유효값) — 26호에서 `a_max` 가 적합 변수로 바뀌고 C-rate 분모와 엮인 것(26호 §3-3)의 원형, (iv) **"일치" 를 식별의 근거처럼 쓰는 관행**(이 편 "agrees well" 9 회 · 26호 "consistent with … literature").
- 26호 §5-2 ④(`[추론]` "전해질 셋 `D_M⁺` · `D_n⁻` · `a₀`(+δ · k_r) — 전도도형 한 조합")에 이 편 원형 모형의 수치를 준다 — §8: 넷 |ρ| ≥ 0.98 · 조건수 9.5×10⁵(우리 가정 · 국소).

---

# ★ (c) 물리 · 가정

1. **전해질 운반체** — `[인쇄]` Li⁺(이동) + **n⁻("uncompensated negative charges … chemically associated with the closest nBO's"[22])** · 평형 이동 분율 δ · 해리 / 재결합 k_d · k_r(식 14) · 두 운반체 Nernst–Planck(식 15) · n⁻ 는 두 전극 경계에서 유속 0(식 17c · d) · 전기중성으로 식 18(앰비폴라 확산 + 반응 — 유도 "It can be shown[27]" = Danilov & Notten 2008 · **파일 61 로 도착 · 처리 대기**). "vacancy" · "공공" 에 해당하는 낱말 **0 회** — 26호가 이 계보를 "이온 + 공공" 이라 부른 것은 26호(또는 Raijmakers)의 이름이고 이 편의 이름은 "n⁻ = nBO 의 미보상 음전하" 다(26호 digest 전사 대조). 그 n⁻ 에 **D_n⁻ = 5.10×10⁻¹⁵ > D_Li⁺ = 0.90×10⁻¹⁵**(`[재현]` t₊ 0.15)를 준 것이 "conductivity is caused by the transport of Li⁺ ions only" 와 같은 지면에 있다(D15).
2. **"전해질 수송 제한이 전체 과전압의 절반 이상" — 모형 출력이다.** 독립 측정(EIS · 전해질 두께 변화 · 기준극 · 대칭셀) **0**(VMP3 에 "impedance boards" 가 있었다는 장비 문장만). 지면이 그 몫을 정하는 길은 식 20 의 분해뿐이고, 그 분해의 크기는 세 가정에 걸린다:
   - (i) **이원 SE 가정** — `[재현·가정]` 같은 σ(2.44×10⁻⁶ S cm⁻¹)의 **단일 이온 전도체**(t₊ = 1 · 농도 분극 0)라면 51.2C 의 η_mt = 옴 강하 **31.5 mV 일정** — 그림 11 끝 −108.7 mV 중 **≈71 %(77 mV)가 이원 가정의 몫**(농도 분극 + 그에 따른 이동 몫 증가)이다.
   - (ii) **`k_r`** — 인쇄 값이면 50 s 에 −149 mV(그림 −101 · `[재현]` §(a) 5) — 몫이 반응 상수 하나의 자릿수에 매달린다.
   - (iii) **평형 곡선 외삽 · η_d 정의** — η_d = E_eq(x_s) − E_eq(x̄) 가 회귀 외삽 곡선(§(a) 3)의 기울기를 그대로 쓴다 — 분모(합)가 외삽 폭만큼 움직인다.
   - `[재현·벡터]` 지면 그림 위에서도 "절반 이상" 은 **51.2C 뒷 절반(0.49 분부터)** 에서만이고 시간 평균 몫은 51.2C **45 %** · 3.2C **46 %** — "0.5 mA cm⁻² 이상에서 더 커진다" 는 몫으로는 안 보인다(절대 mV 만 커진다).
3. **이중층 — 없다.** `capacitance` · `double layer` **0 회**, 식에 용량 항 0, 그림 11 의 이완(전류 끊은 뒤 ≈1–2 분)은 순수 확산 · 반응 이완이다. **37호 물음("`c_dl` 이 면적에 비례하는가")에 이 원형은 "항 자체가 없다" 로 답한다** — 이중층 항은 계보 뒤(Raijmakers 2020 — 37호 [14] "integrating the electrical double layer capacitance … geometrical capacitance", 37호 digest 전사)에서 들어왔다. ⚠ 37호 `c^p_dl` = **5.1×10⁻⁶ F**(각주 없음 — 37호 G2)와 이 편 `k₁ˢ` = **5.1×10⁻⁶** m^2.8 mol^−0.6 s^−1 이 같은 숫자다 — 우연인지 판정하지 않는다(`[해석]` 단서 하나 · 파일 58 에서 `c_dl` 값의 출처를 볼 때 같이 본다).
4. **계면** — 양극 / 전해질 BV 하나(α 적합 0.6) · Li / 전해질 전하이동 "for convenience" 0 · 계면층(SEI · 공간전하) 0 · 접촉 0 · 부반응 0. 양극 두 상(3.9 V 평탄)은 같은 D 의 고용체 Fick 로 대체("for simplicity reasons").
5. **온도** — "Both constants obey Arrhenius law"(k_d · k_r) — 실험 · 모의 25 ℃ 한 점이라 활성화 에너지 0.

---

# ★ (d) 박막 ↔ 복합 전극 이식성 (`ASSB_TRANSFER_NOTE.md` §2–§4 를 읽기만 · `[해석]`)

| 이 편의 것 | 우리 복합 양극 ASSB 합성 truth 에서 | 넘기나 |
|---|---|---|
| 과전압 세 항 골격(η_ct + η_d + η_mt · 식 22) | 같은 합 구조 — 단 복합 양극은 깊이 분포(1D 단일 계면 아님) | ✅ 구조만 |
| **율 외삽 평형 곡선**(네 율 · 선형 / 2차) | 하네스의 OCV 입력 — 측정 OCV · GITT 와 다른 층위 | ⚠ **방법 + 모형 의존 폭(10–28 mV · 0.06 µAh cm⁻²)을 같이** — OCV 출처 표기 없이 넘기면 α·β 적합이 외삽 산물을 측정처럼 먹는다 |
| 이원 SE(n⁻ 이동 · 농도 분극 · 해리 반응) | 황화물 SE(Li₆PS₅Cl 등)는 보통 단일 이온 전도로 둔다 | ❌ 선택지로만 — "전해질 절반" 결론을 이 가정이 만든다((치)) |
| 조밀 평판 · `A` = 기하 면적 · 입자 · 기공 · 굴곡도 0 | §2 **A1**(접촉 / 퍼콜레이션 — `LAM_PE ↔ 접촉 손실` 최악의 축퇴) | ❌ A1 을 표현할 자리 없음 — 들어간다면 F·A·`k₁ˢ` 곱(면적 ↔ 속도 상수)과 `a_max`(용량 맞춤)에 흡수(26호 §5-2 ⑥ 의 원형) |
| **`a_max` = 용량 ÷ (F·Δx·M·A)**(유효값 · 조밀 격자의 45 %) | 복합 양극에서 같은 자리가 θ(접촉) × ε_AM × c_max 를 한 수로 삼킨다 | ⚠ **경고로 넘김** — A1 축퇴의 박막판: 용량 손실이 생기면 이 한 수가 LAM 과 접촉을 같이 먹는다 · truth 는 셋을 따로 둬야 한다(개념 `assb-synthetic-truth-contact-loss-requirements` R 조건 쪽) |
| Li 금속 · E_Li ≡ 0 · η_ct,Li 0 · 활동도 1(무한 원천) | §2 **A2**(Li-In 기준 이동) · **A3**(dead Li ↔ SEI Li) · §2-1 **M1–M3**(조립 방향 · 재고 · 원천 검사) | ❌ 자리 0 · 그리고 Li 층 증착 자체가 미기재(G2) |
| 열화 · 이중층 · 압력 · 온도 축 0 | 합성 truth 의 노화 축 · R·C 처방 · 압력 통제 변수(§3 2단계) | ❌ |
| 값(σ 2.44×10⁻⁶ S cm⁻¹ · D_Li 1.76×10⁻¹⁵ · i₀ ≈1 mA cm⁻² · δ 0.18) | 다른 재료(LCO 박막 · Li₃PO₄) | ❌ 값은 안 넘김 — 단 **i₀ ≈1 mA cm⁻²(면적을 아는 평판 계면)** 는 면적 ↔ j₀ 분리의 참고 자릿수 후보([18,19] 측정 대조 전) |
| "인쇄 표 → 저자 그림 재풀이" 검사 · 국소 CRB | §4 하네스("출처를 붙이고 답이 유일한지 잰다") | ✅ **검사 쪽은 그대로 넘긴다** — 문헌 매개변수 표를 truth 입력으로 쓰기 전에(새 판단 거리 세) |

⇒ **넘어가는 것은 "검사" 와 "경고" 이고 값은 아니다.** 이 편이 §3 1단계(식별성 판정 · 셀 0)에 주는 것은 **"모형 문헌의 표 값이 측정처럼 옮겨지는 경로"(26호 '문헌값')의 첫 고리 표본**이다.

---

# ★ (e) Q1–Q8 — 채움표 칸 (닻 카드 수집 지침)

| Q | 이 편 | 칸 |
|---|---|---|
| **Q1 정량** | **해당 없음** — 조밀 평판 박막(입자 · 공극 0) · `A` = 설계 1 cm²(하드 마스크) · `contact` **0 회** · 열화 0. `[해석]` 부분 박리 · 거칠기는 F·A·`k₁ˢ` 곱과 용량 맞춤 `a_max` 에 흡수될 자리(층 하나) | `θ(N)` 0/91 |
| **Q2 독립관측** | **없다** — 열화 0 · 독립 측정은 매개변수용 둘(SEM 두께 — 그림은 예시 셀 · NDP `a₀` — 자료 0) · 분리 관측 아님 | 없다 |
| **Q3 라벨층위** | 칸 없음 · **층 하나: "각주 셋으로 층위를 단 계보 첫 표 — 적합 일곱의 방법 · 잔차 0 · 인쇄 값 하나(`k_r`)가 자기 그림과 ×100 · 평형 곡선 = 같은 데이터 회귀 외삽 · `a_max` = 용량 맞춤 유효값에 물질 상수 이름"** | 층 |
| **Q4 유일성** | **0/91 — 여든세 번째 성질**(§(a) 9) · 식별성 어휘 전수 0 · 우리 국소 CRB(전해질 넷 \|ρ\| ≥ 0.98 · 조건수 9.5×10⁵ — 가정 · 칸 이동 근거 아님) | 0 |
| **Q5 Li-In** | **해당 없음** — Li 금속 박막(증착 미기재 G2) · E_Li^eq ≡ 0 · Li 쪽 η_ct "for convenience" 무시(교환 전류 비교[17] ↔ [18,19] · 값 0) · 기준극 0 · 층 하나: 음극 과전압 0 가정이 양극 · 전해질 매개변수로 흡수될 자리 | 해당 없음 |
| **Q6 압력** | **해당 없음** — 박막(스택 압력 개념 0) · `pressure` 3 회 = 전부 증착(기저 < 10⁻⁶ mbar · 8×10⁻⁶ bar O₂/Ar · 15×10⁻⁶ bar Ar) | 해당 없음 |
| **Q7 dead Li** | **해당 없음**(무음극 아님) — 단 **공백 G2**: Li 층 증착 단계 · 두께 · 재고 미인쇄(마지막 증착 = Co 150 nm) → 별도 Li 증착인지 첫 충전 도금(Li-free)인지 판정 불가 · 모형 Li 활동도 ≡ 1(무한 원천) | 해당 없음 |
| **Q8 화학 · OCP** | **층 하나** — LiCoO₂ 박막(800 ℃ 10 min RTA · 고온상 · 320 nm) · **평형 곡선 = 1.6–12.8C 네 율 회귀 외삽**(`[재현]` 인쇄 점 ±2 mV · 선형 ↔ 2차 10 · 28 mV · 끝 0.06 µAh cm⁻²) · 4.197 V(Q 0) → 4.15 V 어깨 → 3.90 V 평탄 → 9.96–10.11 µAh cm⁻² 급락 · `OCV` · `open circuit` · `GITT` 0 회 | 층 |

**누적 ≈20.0 → ≈20.0 (새 칸 0).**

---

# 어휘 집계 — 텍스트 층 · 줄 끝 하이픈 복원 · 쪽 머리 · 바닥글 제외 · 본문(제목 → 사사 · 캡션 · 표 포함) | 참고문헌 | 표지, NFKC 뒤 (앞과 다른 것만 괄호)

| 낱말 | 본문 | 참고문헌 | 표지 |
|---|---|---|---|
| `identifiab*` · `uniqu*` · `confiden*` · `uncertain*` · `sensitiv*` · `error*` · `±` · `standard deviation` · `deviation*` · `residu*` · `RMS*` · `least squares` | **0** | 0 | 0 |
| `correlat*` | 0 | 0 | 1(IOP 추천 제목) |
| `fit*` | **1**(NFKC 앞 0 — "good ﬁts" 합자) | 0 | 0 |
| `optimi*` · `regression*` · `extrapolat*` · `estimat*` | 3 · 7 · 8 · 3 | 0 | 0 · 0 · 0 · 1 |
| `agree*` | **9** | 0 | 0 |
| `contact*` · `interphase*` · `vacanc*` · `double layer` · `EIS` · `OCV` · `open circuit` · `GITT` | **0** | 0 | 0 |
| `capacit*` | 2("capacity density" · "maximal capacity" — `capacitance` 0) | 0 | 0 |
| `impedance` | 1(장비 "impedance boards") | 0 | 0 |
| `pressure*` | 3(전부 증착) | 0 | 0 |
| `degrad*` · `aging` | 1 · 1(서론 [12,13]) | 0 | 0 |
| `relax*` | 4 | 0 | 0 |
| `temperature*` | 4 | 0 | 0 |
| `NDP` · `SEM` | 3 · 3 | 0 | 0 |
| `LiPON` / `N-doped` | 1("either or not N-doped") | 0 | 0 |
| `weak electrolyte` · `Butler` · `Nernst` | 1 · 2 · 2 | 0 | 0 |
| `limit*` | 1("transport limitations") | 0 | 1 |
| `overpotential*` / `overvoltage*` | **39** | 1 | 0 |
| `supplement*` · `appendix` · `data availability` · `supporting information` · `video` · `movie` · `zenodo` · `github` | **0** | 0 | 0 |

⚠ 텍스트 층 한계: "µ" 는 MathematicalPi-One 글꼴의 U+0001 로 들어 있고(괄호와 같은 코드) 그리스 문자(δ · α · η)는 빠진다 — `µAh` · `δ` 를 세는 어휘 검사는 이 편에서 **렌더 확인 없이 쓸 수 없다**.

---

# 재현 (`[재현]` — 지면 · 그림 벡터 숫자로 우리가 계산 · 가정 · 외부 값 표시)

| # | 무엇 | 결과 | 판정 |
|---|---|---|---|
| R1 | `a_max` ← 10 µAh ÷ (F·0.5·M·A) | 23.32 kmol m⁻³ ↔ 인쇄 23.3 | ✅ `[재현·가정]` Δx 0.5 |
| R2 | `a_max` ↔ 조밀 LiCoO₂ | 51.6 kmol m⁻³ 의 45 % | `[재현·외부 값]` 5.05 g cm⁻³ · 97.87 g mol⁻¹ |
| R3 | δa₀ ↔ "11 kmol m⁻³" · 그림 12 파랑 | 10.82 ↔ 11 · 10.85 | ✅ |
| R4 | `a₀` → Li₃PO₄ 밀도 | 2.32 g cm⁻³ | 계산값(대조 원문 없음) |
| R5 | C-rate 삼각 검사 | 1C = 10 µA cm⁻² · 51.2C = 0.512 mA cm⁻² · 그림 4 · 5 전류 · 평형 용량 10.10 | ✅ |
| R6 | 그림 12 전극 평균 ↔ I·t/(F·A·M) | −0.7 · −0.5 % | ✅ |
| R7 | 그림 3 Q ÷ I ↔ 그림 2 시각 | 시작 ≈0.25 분 보정 뒤 일치 | ✅ |
| R8 | 그림 4 · 5 회귀 외삽 | 붉은 점 11 개 ±2 mV · ±0.0015 µAh cm⁻² · 선형 ↔ 2차 10 · 28 mV · 0.06 µAh cm⁻² | ✅ + 폭 |
| R9 | 그림 6 η/I | 357–419 Ω cm²(±8 %) | 선형 |
| R10 | 그림 8 η_mt 몫 | 시간 평균 45 %(51.2C) · 46 %(3.2C) · ≥ ½ 은 0.49 분부터 | 초록 조건 탈락(D6) |
| R11 | **표 II 그대로 전해질 재풀이** | 그림 8a · 11 · 12 RMS 64 mV · 한계 전류 ≈257 µA cm⁻² | ❌ |
| R12 | **`k_r` ×100** | RMS 0.8 mV · 농도 ±0.05 · 3.2C ±0.1 mV | ✅ (유일성 미검사) |
| R13 | `k₁ˢ` → i₀ 세 관례 | 151 A · 2.39 mA · 0.38 mA ↔ 그림 0.9–1.0 mA | ❌ 단위 관례 미인쇄 |
| R14 | 표 I 차원 | k₋₁ mol⁻⁴ ✗ · r mol s⁻¹ ✗ · k₁ˢ ✅ | D8 |
| R15 | σ · R_ohm · t₊ · 옴 강하 | 2.44×10⁻⁶ S cm⁻¹ · 61.5 Ω · 0.15 · 31.5 mV ↔ "40 mV" | D7 |
| R16 | **전 셀 재풀이 · 율별 끝 용량** | 모형 / 측정 73–78 · 90 · 94–96 · 98 · 99 % · 그림 7 모형 지속 ±0.075 분 · 그림 8b 끝 ✅ | 고율 미달 |
| R17 | 이원 가정의 몫 | 그림 11 끝 −108.7 mV 중 ≈71 % | `[재현·가정]` 같은 σ 단일 이온 |
| R18 | **국소 CRB** | 전해질 넷 \|ρ\| ≥ 0.98 · 조건수 9.5×10⁵ · D_Li ×1.005 · α ×1.03 · i₀ ×1.10 | `[재현·가정]` σ_V 1 mV |
| R19 | 그림 1a 띠 비 | ≈0.97 ↔ 0.21 | `[도표·화소]` 예시 셀 |

---

# 참고문헌 33 — 우리 축에 닿는 것 (번호는 PDF A222 목록에서 직접 확인 · 번호 붙은 1–33)

| [#] | 서지 `[인쇄]` | 이 편의 쓰임 | 우리 축 |
|---|---|---|---|
| [27] | D. Danilov and P. H. L. Notten, *Electrochim. Acta*, **53**, 5569 (2008) | 식 18 유도("It can be shown") — 해리 전해질 두 운반체 → 확산-반응 식 하나 | (c) · `k_r` · δ · n⁻ 정체 — **4차 묶음 파일 61 로 도착 · 처리 대기** |
| [31] | V. Pop, H. J. Bergveld, D. Danilov, P. P. L. Regtien, and P. H. L. Notten, *Battery Management Systems: Accurate State-of-Charge Indication for Battery-Powered Applications*, Philips Research Book Series, Vol. 9, Springer (2008) | **평형 전압 회귀 외삽(Chap. 4)** 방법 원전 | Q8 · (가) · OCV 출처 |
| [18] | Y. Iriyama, T. Kako, C. Yada, T. Abe, and Z. Ogumi, *J. Power Sources*, **146**, 745 (2005) | LiCoO₂ 교환 전류(음극 무시 근거) · "50–100 Ω … in good agreement" | Q3 · i₀ 독립 대조 · 면적을 아는 계면 |
| [19] | I. Yamada, Y. Iriyama, T. Abe, and Z. Ogumi, *J. Power Sources*, **172**, 933 (2007) | 같음 | 같음 |
| [17] | N. Munichandraiah, L. G. Scanlon, and R. A. Marsh, *J. Power Sources*, **72**, 203 (1998) | Li 금속 교환 전류("much larger") | Q5 |
| [32] | J. Xie, N. Imanishi, A. Hirano, M. Matsumura, Y. Takeda, and O. Yamamoto, *Solid State Ionics*, **178**, 1218 (2007) | D_Li "agrees well with the reported experimental results" | Q3 — ⚠ **파일 62(Xie 2008 *SSI* 179, 362)와 다른 편**(같은 연구실 · 저자 순서도 다름) |
| [33] | H. Sato, D. Takahashi, T. Nishina, and I. Uchida, *J. Power Sources*, **68**, 540 (1997) | 같음 | Q3 |
| [14] · [15] | J. B. Bates 외, *J. Power Sources* **43**, 103 (1993) · **54**, 58 (1995) | SE 의 역할("see Bates et al.") | (c) σ 대조(Li₃PO₄ ↔ LiPON) |
| [12] · [13] | Danilov & Notten, IMLB 2004 Abstract 390 · IEEE VPPC 2009 p. 317 | "the degradation (aging) process … has also been addressed" | 노화 모형 계보(액체 · 제목 미인쇄) |
| [28] · [30] · [29] | McKinnon & Haering 1983 · Atlung, West, Jacobsen *JES* **126**, 1311 (1979) · Kang & Ceder *PRB* **74**, 094105 (2006) | η_d 정의 · 이동항 무시(전자 차폐) | 모형 가정 |
| [22]–[25] | Kahnt 1996 · Ingram 외 1980 · Ravaine & Souquet 1977 · Martin & Angell 1986 | "weak electrolyte" · nBO | n⁻ 정체 |
| [7]–[11] · [16] | Kruijt · Notten · Bergveld 1997–2002 · Notten 1995 | 전자 회로망 모형 · 속도 상수 전위 의존 | 계보 |
| [1] | Doyle · Fuller · Newman *JES* **140**, 1526 (1993) | "early 1980s" 의 근거로 인용(D9) | — |

---

# 인용 대조 — 이 편을 인용한 우리 digest 와 그 쓰임

| 호 | 자리 | 그 digest 가 이 편에 매단 것 | 원문 대조 |
|---|---|---|---|
| **26호** Iwakiri 2024 | [15] · Table 1 "Parameter Estimation Yes"(This work · [15] · [17] · [18] 넷) · 후속 ★★★ "이 모델 계보의 원형" · §6 "박막 전고체 계보(Danilov–Notten 2011 → Raijmakers 2020)" | 추정을 한 기계론 모형 · 계보 원형 | ✅ 원형 · 추정 "Yes" 는 맞다 — 단 추정의 **방법 · 불확실성 0** · 표 값 하나 ×100(§(a) 5) · 26호 표의 값과 같은 값 0/9(§(b)) |
| **12호** Kouhestani 2022 | [61] **본문 재인용 셋**(:197 · :230 · :385) — **후속 절(:504–520) 0** | "전해질/전극 계면의 Li⁺ 삽입·탈삽입 · 계면 부반응 무시 · 여러 전류밀도 방전곡선이 실험과 'good agreement'" · "등온, 불완전 해리, PDE 2 개(SE 와 양극의 확산)" · 표 "Electrochemical model [61,62,77] — SSB 열화 데이터 ✗" | ✅ 넷 다 지면과 맞다("Assuming that no side reactions take place" · 25 ℃ · δ 0.18 · 식 18 · 21) — 단 "good agreement" 는 고율 끝 용량 조건부(§(a) 7) |
| 27호 Sinzig 2024 | "이 편이 인용하지 않는 것" 목록 | — | — |
| 37호 Li 2024 | Raijmakers 2020 행에 저자 이름으로만 | — | — |

**지목 수 정정 (원장 행 "12 · 26 | 2")**: 지목은 **각 digest 의 후속 절**에 오른 것만 센다 — 26호 후속 표(:381 ★★★)에는 있고 **12호 후속 절(:504–520 — Tian · Shao · Kim 2019 · Schmidt · Fathiannasab · Pastor · Hu · Cho)에는 없다**(12호는 본문 재인용). ⇒ 이 편의 지목은 **26 하나(1)** 가 맞다 — 원장 행 "12 · 26 | **2**" → "26 | 1" 정정 후보(87호 "25 → 11 · 25 · 29" 와 같은 형식의 정정 · 원장 문서는 호출자 몫).

---

# 곱 축퇴 처방 — 일흔네 번째 적용 ([[assb-lampe-contact-product-degeneracy]])

**실험 데이터가 있다**(자기 셀 하나 · 여섯 율 방전 + 충전) ⇒ 처방을 적용한다. 단 **신품 · 열화 0 · 모형 편**이다.

| 처방 단계 | 필요한 입력 | 91호 | 판정 |
|---|---|---|---|
| **1단계** (16 · 23호) | 같은 상태축 위 `R` · `C` | EIS 0("impedance boards" 장비 문장뿐) · 모형에 용량 항 0 | ❌ 모형 수준에서 봉쇄(26호와 같다) |
| **2단계** (18호) | + 면적을 아는 대조군 | **평판 박막 = 기하 면적 계면**(거칠기 미검사) · 셀 하나 | ⚠ 대조군의 **재료**는 있다 — i₀ ≈1 mA cm⁻²(그림 · `[재현]`)가 면적을 아는 계면의 자릿수(단 [18,19] 측정 대조 전 · 접촉 손실 표본 아님) |
| **3단계-a** (19호) | `Ea` | 25 ℃ 한 점("Arrhenius" 주장만) | ❌ |
| **3단계-b** (19호) | `C` 물리 상한 | `C` 없음 | ❌ |
| **4단계** (20호) | 시간 영역 상한 | 30 min 휴지(그림에 없음 — D2) · 그림 11 이완(모의) | ❌ |
| 처방 표 "율 스윕(최소 2 율, `i → 0` 포함)" | 여러 율 | ✅ **여섯 율 + `i → 0` 외삽** — 그러나 **정적(평형) ↔ 동적 분리**에 썼다(평형 곡선) · 접촉 ↔ LAM 분리 아님 · 25.6 · 51.2C 는 외삽에서 버림 | ⚠ 데이터는 있고 다른 질문에 썼다 |
| 처방 표 "`J^T J` 최소 고유벡터" | 적합점의 야코비안 | 저자 0 · **우리 국소 CRB(§(a) 8)** — 최소 방향 = 전해질 넷 | ⚠ 우리 계산 |

**곱 문장**(`[인쇄]` → `[해석]`): 식 8 "I⁰ = F A k₁ˢ (ā_CoO₂ā_Li⁺)^α (ā_LiCoO₂)^(1−α)" — **면적 `A`(설계) × 속도 상수 `k₁ˢ`** 가 한 곱으로만 전류에 들어간다(박막에서 거칠기 · 부분 박리는 `k₁ˢ` 이름으로 들어갈 자리) · 각주 c "Estimated from the design parameters and maximal capacity" — **용량 스케일(`a_max`) = 측정 용량 ÷ (설계 부피 × Δx)** 라 활성 분율 · 접촉 몫이 있다면 이 한 수에 섞인다. ⇒ 곱 축퇴의 두 자리(`A·j₀` · `θ·Q`)가 **계보의 첫 표에서 이미 "설계값 × 적합값" 꼴**로 있다 — 처방 표에 새 줄은 없다.

---

# 보류 결정 (가)–(히) · (개)–(해) · (게)–(베) — 이 편이 주는 근거 (결정 안 함)

| # | 결정 (요약) | 91호 근거 | 세기 |
|---|---|---|---|
| **(치)** | 모형 결론 옆 "배제 가정" 표기 | "transport limitations in the solid-state electrolyte … at least half"(초록)를 **SE 이원 가정**(n⁻ 이동 · D_n⁻ > D_Li⁺ · t₊ 0.15 `[재현]`)이 구성상 만든다 — 같은 σ 의 단일 이온 SE 면 그림 11 끝 −108.7 mV 중 ≈71 % 가 사라진다(`[재현·가정]`) · 본문은 같은 SE 를 "Li⁺ ions only" 로 씀 · 이중층 0 · Li 쪽 η_ct "for convenience" 0 · 가정 인쇄는 있으나 결론 옆에 붙지 않음 | **강** |
| **(이)** | 모형 값 인용 규칙 | **인쇄 표 값이 자기 그림을 재현하지 않는다**(`k_r` ×100 · RMS 64 ↔ 0.8 mV `[재현]`) · `k₁ˢ` 단위 관례가 i₀ 를 재현 못 함(151 A ↔ ≈1 mA) · `a_max` = 용량 맞춤 유효값에 물질 상수 이름 — 계보(26호 "문헌값")로 옮겨지는 첫 표 | **강** |
| **(주)** | "X-limited" 명제의 판정 기준 표기 | "transport limitations … at least half of the total overpotential" — ① 몫(과전압 비) ② 시간 기준 = 51.2C 뒷 절반(본문) ↔ 초록은 뗌 ③ 조건 51.2C · 0.512 mA cm⁻² — "or higher" 모의 0 · `[재현·벡터]` 시간 평균 45 · 46 % · ⑤ 몫이 `k_r` 자릿수에 매달림 · "diffusion inside the LiCoO₂ electrode is the leading process" — 끝 순간 판정(표면 x → 1 · 우리 재풀이 ✅) | **중** |
| (대) | C-rate 기준 용량 표기 | 기준이 공칭 10 µAh 로 닫힌 쪽 끝 — 삼각 검사 ✅(1C = 10 µA cm⁻² · 그림 4 · 5 전류 · 51.2C = 0.512 ↔ 초록 "0.5 mA cm⁻²" · 평형 용량 +1 %) | 약 |
| (가) | 29호 Q4 +0.5 (정적 ↔ 동적) | 율 외삽으로 정적(평형) 몫을 떼는 2011 원형 — 네 율 · 선형 / 2차 · 자유도 1 · 외삽 모형 선택이 끝에서 10 · 28 mV(`[재현]`) · 공분산 0 — 정적 ↔ 동적 분리의 모형 의존 표본 | 약 |
| (차) | PyBaMM 면적 / j₀ 노브 분리 forward | 면적(`A` 설계)과 j₀(`k₁ˢ`)가 F·A·`k₁ˢ` 곱으로만 들어가는 계보 원형 · `k₁ˢ` 단위가 적합 α 에 묶여 다른 α 모형으로 못 옮김 · 평판 = 면적을 아는 계면(대조군 재료) | 약 |
| (무) | j₀(x) 모양 선택지 | 식 8 의 x 의존 (1−x)^α x^(1−α) — α(적합 0.6)가 모양 지수와 BV 비대칭을 한 손잡이로 정함 · 방전 끝 x → 1 에서 i₀ → 0 이 그림 8 η_ct 급등(3.2C −0.9 → −64 mV)을 만든다 | 약 |
| (루) | SOC 축 신품 j₀(x) 기준선 | 신품 모형에서 j₀(x) 만으로 방전 끝 η_ct ×70(그림 8a `[도표·벡터]`) — 열화 없이 SOC 축에서 움직이는 계면 항의 모형 표본 | 약 |
| (메) | 예치 원자료 교차 폐합 · 중복 검사 | 원자료 없음 → **벡터 그림 사이 폐합**으로 대신: 여섯 쌍 중 다섯 ✅(그림 2 ≡ 7 측정 3,177 점 · 3 ↔ 2 시각 · 4 · 5 ↔ 3 녹색 · 8b η_mt ≡ 11 · 12 ↔ I·t) · 하나 ✗(같은 51.2C 모의 ≈50 s ↔ 1.08 분 — D5) | 약 |
| (다) | 28호 Bizeray 를 ASSB Q4 분모에 | ASSB 추정 계보의 원형도 식별성 도구 0 — 분모에 "ASSB 원형 0" 한 점 · 우리 국소 CRB 가 대신 경계를 냄 | 약 |

나머지 — (라)(마)(바)(사)는 결정 · 반영됨, 그 밖의 글자는 **근거 0**(압력 · 기준극 · 노화 · DRT · LLI 정의 · 예치 자료 축이 이 편에 없다). **결정 안 함.**

## 새 판단 거리 (넷 — 글자는 호출자가 붙인다)

1. **인쇄 매개변수 표의 재풀이 폐합 검사** — 모형 편 매개변수 표(특히 계보 뒤 편이 "문헌값" 으로 가져가는 첫 표)를 카드 · 개념 · 합성 truth 에 옮기기 전에, 인쇄 값으로 저자 그림 하나를 다시 풀어 폐합하는지 보고 결과(배수 · RMS)를 값 옆에 적게 할지 — 91호: `k_r` 인쇄 0.90×10⁻⁸ ↔ 그림 재현 ≈0.90×10⁻⁶(×100 · RMS 64 ↔ 0.8 mV) · 26호 "문헌값" 8.00×10⁻⁷ 과 같은 자릿수 → 파일 58 대조에 이 검사를 걸지 ((이) 의 재풀이판으로 묶어도 됨).
2. **속도 상수의 i₀ 환산 표기** — BV 속도 상수(k_s)를 옮길 때 단위 관례(농도 단위 · 면적 · α)와 기준 상태(x · 전해질 농도)의 i₀(mA cm⁻²)를 같이 적게 할지 — 91호 `k₁ˢ` 5.1×10⁻⁶ m^2.8 mol^−0.6 s^−1(α 0.6 에 묶인 단위) → 인쇄 단위 151 A · kmol 2.4 mA · mol cm⁻³ 0.38 mA ↔ 그림 ≈1 mA · 26호 `k¹_s`(α 0.5 판).
3. **모형 "일치" 주장의 율별 끝 용량 잔차 표기** — 모형 검증("good agreement")을 카드 · 개념으로 옮길 때 율별 끝 용량(컷오프 시각)의 모형 ↔ 측정 비를 같이 적고, 시간 축 그림이면 표지 폭과 견주게 할지 — 91호: 51.2C 모형 = 측정의 73–78 % · 25.6C 90 %(그림 7 · 65 분 축 · 표지 ≈0.81 분) · 1.6C 그림 없음.
4. **평형(OCV) 곡선의 출처 층위 표기** — OCV 를 하네스 입력 · 카드 Q8 칸으로 옮길 때 출처(측정 개회로 · GITT 이완 · 저율 의사 OCV · **율 외삽 회귀** · 문헌 함수)와 외삽이면 점 수 · 함수형 · 버린 율 · 모형 의존 폭을 적게 할지 — 91호: 네 율 · 선형 / 2차(자유도 1) · 25.6 · 51.2C 제외 · 끝 10 · 28 mV · 0.06 µAh cm⁻² · 그 곡선이 다시 η 기준선 · 모형 입력으로 되먹임.

---

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** | 그림 1a SEM 띠 비 ≈0.97 · 축척 0 ↔ 320 : 1500 nm(0.21) · "determined by SEM" | 그림 1 · `[도표·화소]` · A221 |
| **D2** | "followed by a 30 min relaxation period" · 그림 2 캡션 "relaxation" ↔ 그림 2 · 7 의 4.2 V 평탄 ≈5.5 분 뒤 바로 방전 | A219 · 그림 2 · 7 `[도표·벡터]` |
| **D3** | "Good agreement … for all discharge currents" · 결론 "good fits … including … high C-rates" ↔ 모형 3.0 V 도달 0.05–0.31 분 이르다 · 51.2C 용량 73–78 % | 그림 7 · §(a) 7 |
| D4 | 같은 문장 ↔ 1.6C 방전이 그림 7 에 없다 | 그림 7 |
| **D5** | 같은 51.2C 모의가 ≈50 s(그림 8b 끝 0.840–0.858 분 · 그림 12 "after 50 s … just before discharging will be terminated")와 ≈1.08 분(그림 11 전류 0 → 1.081 분 · 본문 "After about 1 min, the current is switched off" · "switched off after 1 min") 두 길이 · 그림 8b η_mt ≡ 그림 11 합(≤0.5 mV) | 그림 8b · 9–12 · A221 |
| **D6** | 초록 "at least half of the total overpotential" · "even larger … 0.5 mA cm⁻² or higher" ↔ 본문 "starting from the second half of the discharge process"(51.2C) · `[재현·벡터]` 시간 평균 45 · 46 % · "or higher" 모의 0 | A215 ↔ A220 · 그림 8 |
| D7 | "a 40 mV voltage drop … fully carried by the electric field" ↔ `[재현]` t = 0⁺ 옴 강하 31.5 mV · 40 mV 는 확산 −4.8 mV 가 붙은 0.6 s 뒤 | A221 · 그림 11 |
| **D8** | 표 I `k₋₁` "m⁴ mol⁻⁴ s⁻¹"(→ mol⁻¹) · `r` "mol s⁻¹"(→ mol m⁻³ s⁻¹) | 표 I ↔ 식 3b · 8 · 16a |
| D9 | "dates back to the early 1980s.[1]" ↔ [1] = 1993 | A215 |
| D10 | "overpotentials plotted in Fig. 5" ↔ 과전압은 그림 6(같은 문장 뒤에서 "Fig. 6 black line") | A220 |
| D11 | "The simulated **total** overpotential corresponds to charge transfer resistances of the order of 50–100 Ω" ↔ 그림 6 총 η/I 357–419 Ω cm² · 그림 8 η_ct/I 26–66 Ω cm² | A222 · 그림 6 · 8 |
| **D12** | `k_r` 0.90×10⁻⁸(표 II · A221 본문 두 자리) ↔ 저자 그림 8a · 11 · 12 는 ≈0.90×10⁻⁶ 으로만 재현 | §(a) 5 `[재현]` |
| **D13** | `k₁ˢ` 5.1×10⁻⁶ m^2.8 mol^−0.6 s^−1 → i₀ 151 A(인쇄 단위) ↔ 그림 8 이 요구하는 ≈1 mA | §(a) 6 `[재현]` |
| D14 | 표 II 각주 a "Design parameters"(L · M) ↔ 본문 "determined by scanning electron microscopy" | A220 ↔ A221 |
| **D15** | "the conductivity is caused by the transport of Li⁺ ions only" ↔ 적합 D_n⁻ 5.10 > D_Li⁺ 0.90(×10⁻¹⁵) → t₊ 0.15 · n⁻ 를 "nBO 에 묶인 음전하" 로 정의 | A216 ↔ 표 II |
| D16 | 그림 8 캡션 "(a) low-current" — 율(3.2C)은 본문에만 | 그림 8 ↔ A220 |
| D17 | 그림 12 캡션 빨강 "in the middle of the discharge process" ↔ 본문 "20 s after"(50 s 중) | 그림 12 ↔ A221 |
| D18 | 표 II 열 머리 "Estimated value" 가 설계값 · NDP 값에도 붙음 · 표 I "Table I lists all model parameters" ↔ 값은 표 II | 표 I · II |

---

# 이 편이 우리 프로젝트에 주는 것 (정리)

1. **26호 계보의 원천 확인** — 계보 첫 매개변수 표는 **값이 아니라 구조와 관행**을 물려줬다(같은 값 0/9). 그리고 그 첫 표에 이미 **자기 그림과 ×100 어긋나는 값(`k_r`)** 과 **단위 관례 없는 속도 상수(`k₁ˢ`)** 가 있다 — 26호의 "문헌값과 5 % 이내" · `D_e⁻` 10 자릿수와 같은 계보에서, 우리가 원전 수치만으로 **다시 풀어서** 찾은 셋째 · 넷째 사례다. 파일 58(Raijmakers 2020)을 읽을 때의 물음이 생겼다: `k_r` 8.00×10⁻⁷ 은 어디서 왔나(이 편 그림 값 ≈0.9×10⁻⁶ 과 같은 자릿수 · 인쇄 값과 ×89).
2. **Q4 — "맞는 곡선 ≠ 맞는 표" 의 원형 표본**: 우리 `degradation-degeneracy/` 가 합성 truth 로 채점하는 실패 모드(맞는 곡선 · 틀린 / 정해지지 않은 매개변수)가 계보 원형에서 두 겹으로 나타난다 — (i) 인쇄 표가 그림과 안 맞고(D12), (ii) 맞는 점에서도 전해질 넷이 한 묶음(우리 CRB). 그리고 "good agreement" 가 고율 끝 용량 22–27 % 미달을 덮는다(D3) — **시각적 일치가 적합 판정 기준일 때 무엇이 빠지는지**의 정량 표본.
3. **OCV 출처** — 이 편의 "평형 전압" 은 율 외삽 회귀다(자유도 1 · 끝 28 mV). 우리 α·β 하네스가 문헌 OCV 를 입력으로 받을 때 **출처 층위 표기**(새 판단 거리 넷째)가 필요하다는 근거.
4. **A1 축퇴의 박막판** — 복합 양극의 접촉 손실이 들어갈 두 자리(`A·k₁ˢ` · 용량 맞춤 `a_max`)가 계보 첫 표에 "설계값 × 적합값" 으로 이미 있다 — 합성 truth 는 `a_max` 를 물질 상수 · 활성 분율 · 부피 분율로 나눠 둬야 한다는 기존 요구(R 조건)의 계보 쪽 근거.

---

# 후속 후보 (원전 우선 — 지목 수는 위키 digest 의 후속 절 grep 으로 센 값)

| 등급 | 서지 (PDF 목록 번호) | 지목 (후속 절) | 왜 | 축 |
|---|---|---|---|---|
| ★★★ | **Danilov D., Notten P.H.L. 2008** — *Electrochim. Acta* **53**, 5569 ([27]) | 26 · **91** = **2** (재지목) | **4차 묶음 파일 61 로 도착 · 처리 대기** — 식 18 의 유도처 · n⁻ 의 정체(공공인가 · 그렇다면 "Li⁺ only" 와 화해) · `k_r` · δ 값과 단위 · 경계 조건(n⁻ 차단) — `k_r` ×100 판정의 둘째 대조처 | (c) · Q4 |
| ★★ | **Pop V., Bergveld H.J., Danilov D., Regtien P.P.L., Notten P.H.L. 2008** — *Battery Management Systems: Accurate State-of-Charge Indication for Battery-Powered Applications*, Philips Research Book Series Vol. 9, Springer ([31]) | 91 = 1 (새) | **평형 전압 회귀 외삽(Chap. 4)의 방법 원전** — 점 수 · 함수형 · 버린 율 · 불확실성을 원전이 어떻게 다뤘나(새 판단 거리 넷째 · (가)) · ⚠ 책(장 단위 입수) | Q8 · (가) |
| ★★ | **Iriyama Y., Kako T., Yada C., Abe T., Ogumi Z. 2005** — *J. Power Sources* **146**, 745 ([18]) | 91 = 1 (새) | 평판 LiCoO₂ 계면 전하이동의 **측정** — 그림 8 이 요구하는 i₀ ≈1 mA cm⁻² · "50–100 Ω" 의 독립 대조 · **면적을 아는 계면**의 j₀(처방 2단계 대조군 재료) · ⚠ 10호 본문 ref 70 "Iriyama 2005" 와 같은 편인지 미확인(10호 digest 에 권 · 쪽 전사 0 · 후속 절 밖) | Q3 · (차) |
| ★★ | **Yamada I., Iriyama Y., Abe T., Ogumi Z. 2007** — *J. Power Sources* **172**, 933 ([19]) | 91 = 1 (새) | 같은 목적의 둘째 측정 | Q3 · (차) |
| ★ | **Munichandraiah N., Scanlon L.G., Marsh R.A. 1998** — *J. Power Sources* **72**, 203 ([17]) | 91 = 1 (새) | Li 금속 교환 전류 — "Li 쪽 η_ct 무시" 의 근거 값 | Q5 |
| ★ | **Xie J., Imanishi N., Hirano A., Matsumura M., Takeda Y., Yamamoto O. 2007** — *Solid State Ionics* **178**, 1218 ([32]) | 91 = 1 (새) | 적합 D_Li 1.76×10⁻¹⁵ 의 "reported experimental" 대조처 · ⚠ **파일 62(Xie 2008 *SSI* 179, 362 — 26호 지목)와 다른 편** | Q3 |
| ★ | **Sato H., Takahashi D., Nishina T., Uchida I. 1997** — *J. Power Sources* **68**, 540 ([33]) | 91 = 1 (새) | 같은 대조처 둘째 | Q3 |
| ☆ | Bates J.B. 외 1993 *JPS* 43, 103 · 1995 *JPS* 54, 58 ([14] · [15]) | 행 없음 | 박막 SE 전도도 — 우리 `[재현]` σ 2.44×10⁻⁶ S cm⁻¹ 대조(Li₃PO₄ 는 N 0) | (c) |
| ☆ | Danilov & Notten 2004 IMLB 요약 390 · 2009 IEEE VPPC p. 317 ([12] · [13]) | 행 없음 | Notten 계보 노화 모형(액체 · 제목 미인쇄 · 학회 자료) | 노화 |
| ☆ | Atlung · West · Jacobsen 1979 *JES* 126, 1311 · McKinnon & Haering 1983 · Kang & Ceder 2006 *PRB* 74, 094105 ([30] · [28] · [29]) | 행 없음 | η_d 정의 · 이동항 무시의 근거 | 모형 |
| ☆ | Kahnt 1996 · Ingram 외 1980 · Ravaine & Souquet 1977 · Martin & Angell 1986 ([22]–[25]) | 행 없음 | "weak electrolyte" · nBO — n⁻ 정체의 물리 근거 | (c) |

**교차 참조 (지목 아님 — 이 편 이후 편)**: Raijmakers · Danilov · Eichel · Notten 2020 *Electrochim. Acta* 330, 135147(**4차 묶음 파일 58 로 도착 · 처리 대기** — `k_r` 8.00×10⁻⁷ · δ 0.64 · a₀ 61 141 · `D_e⁻` · `c_dl` 의 출처) · Kim · Lin · Abbasalinejad · Kim · Chung 2019 *Electrochim. Acta* 317, 663(**파일 59 로 도착 · 처리 대기** — 같은 계보 모형 위의 상태추정) · Iwakiri 2024(26호). 4차 묶음 13 편 중 이 편이 인용하는 것은 **[27] 하나**(파일 61)이고 파일 62(Xie 2008)는 아니다([32] = Xie 2007).

**지목 누락 0** — 이 편의 참고문헌 33 편 중 앞 호 digest 후속 절에 오른 것은 [27](26호 ★★) 하나이고 원장 행이 있다. 12호 · 10호 본문에만 나온 편(Iriyama 2005 후보)은 지목이 아니다.

---

# 이 digest 가 주장하지 않는 것

1. **표 II 의 `k_r` 가 틀렸다고 단정하지 않는다** — 인쇄 값 그대로 우리 재풀이가 저자 그림을 재현하지 않고 ×100 이면 재현한다는 비교표까지가 사실이다. ×100 이 오기 · 코드 단위 · 다른 적합점 중 무엇인지는 모른다(G1 · G8) · 다른 매개변수 조합으로도 맞을 수 있다(골짜기 — §(a) 8).
2. **우리 재풀이가 저자 코드와 같다고 하지 않는다** — 식 18–22 를 인쇄대로 풀었고 E_eq 는 그림 3 녹색 벡터 경로, i₀(x) 꼴은 우리가 골랐다. 전해질 부분은 그림 셋을 RMS 0.8 mV 로 맞추지만 η_ct 시간 모양은 지면과 다르다(§(a) 6).
3. **국소 CRB 를 이 편의 식별성 결과로 옮기지 않는다** — 가정(σ_V 1 mV · 한 점 · 우리 모형 꼴 · 2–85 % 구간)이 붙은 우리 계산이고 Q4 칸을 움직이지 않는다.
4. **"전해질 수송이 중요하지 않다" 고 하지 않는다** — 주장은 "그 몫(절반 이상)은 모형 출력이고 이원 SE 가정 · `k_r` · 외삽 평형 곡선에 걸리며, 지면 그림에서도 51.2C 뒷 절반에서만 성립한다" 까지다.
5. **모형이 고율에서 틀렸다고 일반화하지 않는다** — 그림 7 벡터와 우리 재풀이가 51.2C 끝 용량 22–27 % 미달을 같이 보인다는 것까지이고, 원인(양극 구조 · 매개변수 흡수)은 `[해석]` 후보다.
6. **12호 지목 정정을 확정하지 않는다** — "후속 절만 센다" 규칙을 적용한 결과이고 원장 수정은 호출자 몫이다.
7. **37호 `c_dl` 5.1×10⁻⁶ 과 이 편 `k₁ˢ` 5.1×10⁻⁶ 의 숫자 일치를 인과로 읽지 않는다** — 단서로만 적었다.
