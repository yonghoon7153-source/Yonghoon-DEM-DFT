# Scalable AI-accelerated design of dual-doped LGPS electrolytes for next-generation solid-state batteries — Jung *et al.* (*eTransportation* 2026)

> slug `jung2026_scalable_ai_dual_doped_lgps` · DOI `10.1016/j.etran.2026.100570` · type `mixed (MLIP relax + ML surrogate + DFT + AIMD)` · PDF `litdb/inbox/14. eTransportation_2026_Jung_Scalable_AI_dual_doped_LGPS_MAIN.pdf` (+ SI) · digested 2026-09-22 · status ✅
> elements: Li, Ge, P, S, O, Cl, Br, I, F, Se, N, Ga, Y, Si, Sn, Be, B, C, Zr, Zn, Mn, Sc, Ti, Nb, V, Cr, Co, Ni, Cu, Mo, Te, Pb, Sb, As, Bi, Al, Na, Ca, Sr, Ba, Rb, Ag
> methods: DFT, AIMD, MLIP, ESW, elastic
>
> 🎤 **관련 발표**: 해당 없음 — `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `talks/lee2026_skku_mlip_materials_design.md` 하나뿐이고 그 대기열에 이 논문은 **없다**. 역링크 대상 없음.
>
> 🏷 인용 태그 **`[Jung26LGPS]`**
>
> 🔴 **이 digest 의 1순위 목적은 선점 확인이다.** 판정은 §1-A 에 있고, 근거는 §12(도펀트 공간 전수 대조)·§13(dual-doped 정의 해부)·§14(파이프라인 단계별 대조)에 있다.
> 📌 **경위**: 이 논문은 `papers/park2026_ml_framework_stable_interfaces_assb.md` §15 의 후속 확보 목록 #5 (**Park ref 37**)로 *"우리 도핑 축의 최근접일 수 있다 — 제목만으로는 판정 불가"* 라고 올라 있던 편이다. **이제 판정됐다.**

---

## 1. 한 줄 요약

LGPS(Li₁₀GeP₂S₁₂) 에 **40종 도펀트 × 4개 자리(Li/Ge/P/S) × 자리쌍 9종 템플릿**으로 만든 **2,550개 "이원도핑" 조성**을, **CHGNet 완화 → coGN/coNGN 대리모형(E_form·E_hull·E_gap·G_VRH·K_VRH) → DFT 대분배포텐셜 ECW → AIMD σ** 의 4단 깔때기로 훑어 **21종 → 최종 4종**을 남기고, 그중 **Li₉P₃OS₁₁ 이 300 K 외삽 σ = 17.28 mS/cm (Ea 209 meV)** 로 *"pristine LGPS 의 약 2배"* 라고 주장하는 편이다.

**그러나 그림을 직접 보면 헤드라인이 흔들린다.** `Fig. 4a` 에서 **21종 전부와 pristine LGPS 의 환원전위 V_red 가 정확히 1.717 V 로 같고**, ECW 개선은 **오직 산화쪽 V_ox 2.296 → 2.356 V = +60 mV** 뿐이다 — 즉 논문이 초록에서 내건 문제(*"Li 금속 음극에 대한 심각한 전기화학적 불안정"*)는 **한 종도 개선하지 못했다**. 그리고 `Fig. 5b` 를 보면 **실제로 시뮬레이션한 700–1300 K 구간에서 Li₉P₃OS₁₁ 은 4종 중 최하위~중위**이고, 1위는 **300 K 로 외삽하는 과정에서만** 생긴다.

---

## 1-A. 🎯 선점 판정 (**이 작업의 본론**)

### 판정 한 문장

> 🟡 **인접하다 — 구별선을 그어야 한다.**
> 계(LGPS ≠ 아지로다이트)·도펀트 공간(**Nd 를 포함한 란타나이드 전부 부재**)·"이원도핑" 정의(**한 염 내부 전하중성 vs 독립 2원소 + Li 보정**)·보고량 규율이 갈려 **우리 Nd/O 아지로다이트 서사 자체는 선점되지 않았다.** 다만 ***"ML 대리모형 → DFT ECW → AIMD σ 로 황화물 SSE 의 이원도핑 조성공간을 훑는다"는 파이프라인 프레임***과 ***"S 자리 최적 도펀트는 Cl 과 O 다"*** 라는 결론은 **선점됐다** — 이 둘은 앞으로 *발견*이 아니라 *선행연구*로 인용해야 한다.

### 항목별 겹침 대조 (요청 1번에 대한 답)

| 축 | [Jung26LGPS] | 우리 | 판정 |
|---|---|---|---|
| **계(structure family)** | **LGPS** Li₁₀GeP₂S₁₂, tetragonal **P4₂/nmc**, ICSD-**188887** (Kuhn 2013 단결정 XRD). 골격 = 모서리 공유 (Ge/P)S₄ + PS₄, Li1–Li4 4자리, **c축 1D 채널** | **아지로다이트** Li₆PS₅Cl / Li₅.₄PS₄.₄Cl₁.₆, cubic **F-43m**. 골격 = 고립 PS₄ + 자유 S²⁻/Cl⁻ 4a/4d, **3D 케이지-점프** | 🟢 **다른 구조족 — 이게 제일 강한 방패다.** `Fig. 2c` 의 도핑 자리(Li1–4·4d Ge/P·S)는 우리 계에 **대응물이 없다**. 그들의 핵심 서사(*"강체 GeS₄/PS₄ 골격을 안 깨는 양이온 + S 자리 음이온"*)는 아지로다이트에서 **4a/4d 음이온 무질서**라는 완전히 다른 레버로 갈린다. ⚠ 단 "황화물 SSE" 라는 상위 범주는 같아서 **리뷰어는 같은 문단에 놓는다** |
| **도펀트 원소 공간** | **40종** (`Fig. 2b`·§12 전수). Li자리 8 · Ge자리 19 · P자리 13 · S자리 7 | **43종** (cascade `composition_*` 열 실측, 102개 도펀트 염) | 🟡 **32종이 겹친다** (Ag Al As B Ba Br Ca Cl Co Cr Cu F Ga Ge I Mn Mo N Na Nb Ni O Sb Sc Si Sn Sr Ti V Y Zn Zr). **우리에만**: Fe **Gd Hf In La Mg Nd Sm** Ta W (10종). **그들에만**: Rb Be C Pb Te P Bi (7종) |
| **★ Nd 가 있나?** | ⛔ **없다. `Nd` 본문·SI 출현 0회** (grep 실측). `Fig. 2b` 주기율표에서 **`57-71 La-Lu` 칸이 통째로 회색 = 란타나이드 전부 제외** | **Nd₂O₃ · NdCl₃ · NdF₃** 가 우리 서사의 핵심 | 🟢 **우리 Nd 축은 손 안 댔다.** 란타나이드가 **한 종도** 없다 ⇒ `[Park26ML]`(M pool 에 란타나이드 6종이 있어 🟠 였던 것)보다 **훨씬 안전하다** |
| **★ O 는 있나?** | 🔴 **있고, 그것이 챔피언이다.** O 는 S자리 7종 중 하나이고 **survival rate 2위(≈50.5 %, `Fig. S4b` figure-read)**, 최종 챔피언 **Li₉P₃OS₁₁ 이 O 치환체**다. 기전도 우리와 같은 언어 — *"작은 이온반경·높은 전기음성도 → 짧고 강한 P–O → PS₂O₂ 다면체 → 국소 왜곡 → Li⁺ 이동 촉진"* (`Fig. S6`) | O 도핑(B₂O₃ · Nd₂O₃ · 각종 산화물 염) | 🔴 **여기가 제일 아프다.** *"황화물 SSE 에서 S 를 O 로 부분치환하면 국소 왜곡으로 Li 수송이 좋아진다"* 를 **우리 발견으로 쓰면 안 된다.** ⚠ 단 그들의 O 는 **PS₄ 사면체 안의 S 를 치환**(PS₂O₂)이고, 우리 Nd₂O₃/B₂O₃ 는 **4a/4d 자유 음이온 자리 + 별도 양이온**이라 **기전의 자리가 다르다** — 구별선은 여기다 |
| **★ Cl 은 있나?** | 🔴 **있고, S자리 survival 1위(≈53.5 %)**. Cl 치환 후보가 최종 21종 중 **Li₉GaP₂Cl₂S₁₀ · Li₉YP₂Cl₂S₁₀ · Li₉SiP₂ClS₁₁ · Li₈.₅Ca₁.₅GeP₂Cl₂S₁₀** | Cl-rich (modelc Li₅.₄PS₄.₄Cl₁.₆) 가 우리 제2 축 | 🟡 **결론 방향은 같고 계가 다르다.** 그들의 Cl 은 **LGPS 의 S 를 치환**(Cl₂S₁₀), 우리 Cl-rich 는 **아지로다이트 4a/4d 재배분**. ⇒ *"Cl 이 황화물에서 좋다"* 는 이제 **우리 결과로 못 판다** |
| **★ "dual-doped" 의 정의** | **자리 2개에 도펀트 2종** (또는 같은 자리에 2원소). `Fig. 2c` 9개 템플릿 = Li+Li′ / Li+Ge / Li+P / Li+S / Ge+Ge′ / Ge+P / Ge+S / P+S / S+S′. **전하 보정은 Li 를 더하거나 빼서** 한다 (예: Ge⁴⁺→Co³⁺ 시 Li₁₀→**Li₁₀.₅**) | **한 염(salt)이 두 도펀트를 운반** — Nd₂O₃ = 양이온 Nd³⁺ + 음이온 O²⁻ 가 **염 내부에서 전하중성** | 🟡🔴 **여기서 성격이 갈린다. 두 방향 다 정직하게 적는다.** ⛔ **불리한 쪽**: 그들의 템플릿 4·7·8(Li+S, Ge+S, P+S)은 **양이온+음이온 동시 치환**이고, 최종 21종에 실제로 `Li₁₀Ge₀.₅Zr₀.₅P₂O₂S₁₀`(Zr+O) · `Li₁₁.₅GeP₁.₅Zn₀.₅OS₁₁`(Zn+O) · `Li₉Ge₀.₅Mn₀.₅P₂FS₁₁`(Mn+F) 가 들어 있다 ⇒ **"양이온+음이온 공치환" 자체는 그들 공간 안에 있다.** ✅ **유리한 쪽**: 그들은 **두 도펀트를 독립적으로 넣고 Li 로 전하를 맞춘다** ⇒ **도펀트 정체와 Li 함량이 구조적으로 교락된다** (Li₈.₅ ~ Li₁₁.₅ 까지 움직인다). 우리는 **염 내부에서 중성**이라 Li 를 안 건드린다. ⇒ **구별선은 "이원"이 아니라 "전하중성을 어디서 닫느냐"** 다 |
| **스크리닝 파이프라인** | 4단: ① **ML** E_form<0 & E_hull<0.025 (2550→2065) ② **ML** E_gap>2.0 eV (→987) ③ **ML** G_VRH>8.4 GPa & G/K<0.7 (→873) ④ **DFT** ECW≥0.58 V (→**21**) ⑤ **AIMD** σ (**4종만**). 계면 축 **없음**(저자 자인), 대기안정 축 **없음**, 합성 제약 **없음**(저자 자인) | cascade: 안정성 → 격자/무질서 → BVSE 이동도 → anneal → EOS/elastic → **ESW(대분배)** → **계면 5상대 전수** → **대기안정(ΔE_H₂S)** → MLIP-MD σ | 🟡 **①–③ 은 같은 일을 한다 (우리가 DFT/MLIP, 그들이 ML 대리모형).** 🟢 **④ 이후가 다르다** — 우리에게 있고 그들에게 **없는 축**: (a) **계면**(T9: 양극 만충/반충·SE·Li 음극·LNO 5상대 47종 전수), (b) **대기안정**(T11 ΔE_H₂S), (c) **BVSE 채널%**, (d) **보고량 카드/사전등록**. 🔴 그들에게 있고 우리에게 **없는 것**: **ML 대리모형으로 2,550종을 훑는 규모** (우리 cascade 는 302종) |
| **보고량 (estimand)** | **σ(300 K) 절대값** + Ea. **오차막대 = 4 온도 상대표준편차의 평균을 네 물질에 동일 적용** ⇒ `Fig. 5c` 의 ± 가 **네 물질 전부 정확히 값의 50 %** (2.56±1.28 · 1.24±0.62 · 17.28±8.64 · 0.61±0.31). **시드 1개 · 온도당 궤적 1개 · 100 ps** | **상대차만** (1저자 정책 2026-09-18: σ·D 뿐 아니라 **Ea 도 계 간 상대차로만**). 멀티시드(600 K 3-seed) · MSD 창 2–50 ps 고정 | 🟢 **우리가 낫고, 그 차이가 구별선이 된다.** 그들의 ± 는 **물질을 가르는 정보가 0** 이다(전부 50 %). 그리고 **pristine LGPS 의 AIMD σ 를 자기 손으로 계산하지 않았다** ⇒ *"2배"* 의 분모가 **실험 문헌값**이라 **방법이 섞인 비율**이다 (§10-2) |

### 그래서 무엇이 남았나 (🔴 선점된 것 / 🟢 남은 것)

**🔴 선점됐다 — 앞으로 우리 것으로 못 쓴다**
1. *"ML 대리모형(GNN)으로 수천 개 도핑 조성을 걸러 DFT ECW 와 AIMD σ 로 마감하는 프레임을 황화물 SSE 이원도핑에 적용한다"* — **프레임 자체.**
2. *"황화물 SSE 의 음이온 자리 최적 도펀트는 Cl 과 O 다"* — **결론 자체** (`Fig. S4b` S자리 1·2위).
3. *"S 를 O 로 부분치환하면 국소 왜곡이 Li⁺ 수송을 돕는다"* — **기전 서술 자체** (`Fig. S6` PS₂O₂).
4. *"Ge/P 자리는 산화수 유사 원소로 골격을 보존하고, 음이온 자리에서 이득을 본다"* — **설계 원칙 문장 자체** (§3.4 마지막 문단 = 그들의 conclusion 문장).

**🟢 남았다 — 우리 자리**
1. **란타나이드 축 전부** (Nd·Gd·La·Sm). 이 논문은 한 종도 안 봤다.
2. **아지로다이트 계** — 구조족이 다르고, 4a/4d 음이온 무질서라는 레버가 그들 공간에 없다.
3. **"한 염 내부 전하중성" 이라는 도핑 설계 규율** — 그들은 Li 로 보정해 **Li 함량 교락**을 만든다. 이건 우리가 *구별선*으로 명시해야 하고, 실제로 **그들 데이터가 그 교락을 보여준다**(Li₄.₅ ~ Li₁₁.₅).
4. **계면 축 · 대기안정 축** — 저자들이 §4 Future directions 에서 **스스로 없다고 쓴다**: *"the current screening framework does not evaluate electrolyte–electrode interfaces"*, *"does not evaluate synthesis-related constraints such as dopant volatility, toxicity…"*. ⇒ **원고 intro gap 문장으로 직접 인용 가능** (`[Park26ML]` 과 같은 용법).
5. **보고량 규율** — 상대차·멀티시드·MSD 창 고정. 그들의 50 % 일괄 오차막대와 **비교 우위가 명확**하다.
6. **산화 onset 의 축퇴(degeneracy)를 *진단*하는 것** — 그들은 `Fig. 4a` 에 그려놓고 **논평하지 않는다**. 우리 `cascade_screening_funnel.json` 은 이미 *"onset 축퇴(19종이 정확히 2.14 V) 탓에 완전한 계단 함수다"* 라고 **진단해 뒀다** (§7-C). **이 진단이 우리 것이다.**

---

## 2. 메타

| 항목 | 값 |
|---|---|
| **저자** | **Yerim Jung**ᵃ, **Jiwon Sun**ᵃ·ᵇ, **Juo Kim**ᶜ, **Woojin Shin**ᶜ, **Kyoungmin Min**\*ᶜ |
| **소속** | ᵃ **숭실대(Soongsil Univ.) 기계공학부** (서울 상도로 369) · ᵇ **Northwestern Univ.** MSE (Evanston, IL) · ᶜ **연세대(Yonsei Univ.) 기계공학부** (서울 연세로 50) |
| **교신** | Kyoungmin Min — `kmin.min@yonsei.ac.kr` |
| **저널/권호** | ***eTransportation* 28 (2026) 100570**, Elsevier, ISSN 2590-1168 |
| **DOI** | `10.1016/j.etran.2026.100570` |
| **일정** | 접수 2025-09-12 / 개정 2026-02-06 / 수락 2026-02-23 / 온라인 2026-02-24 |
| **분량** | 본문 12 pp (`Fig. 1`–`5` + `Table 1`–`2`), SI 10 pp (`Fig. S1`–`S6` + `Table S1`–`S3`), refs **111** |
| **조성** | **Li₁₀GeP₂S₁₂ (LGPS) 모체** + 2,550 이원도핑 유도체. 최종 4종: **Li₉P₃OS₁₁ · Li₉GaP₂Cl₂S₁₀ · Li₉GaP₂I₂S₁₀ · Li₉YP₂Cl₂S₁₀** |
| **연구유형** | 순수 계산 (실험 0). MLIP 완화 + GNN 대리모형 + DFT + AIMD |
| **지원** | NRF (MSIT) **RS-2025-23525537 · RS-2025-23523906** · KISTI 국가슈퍼컴 **KSC-2025-CRE-0128** · 연세대 연구비 2025-22-0165 |
| **데이터 공개** | ⛔ **없다.** *"The database used in this study will be available upon request"* — 2,550 목록·873 결과·21 후보 좌표 **전부 미공개**. 코드 공개 **없음** |
| **라이선스** | © 2026 Elsevier B.V. All rights reserved (**OA 아님**) |

### ⚠ 저자 관계 (요청 5번에 대한 답)

- **한국 그룹 맞다** — 숭실대 + 연세대. 교신저자 **Kyoungmin Min** 은 **연세대 기계공학부**(SI 표지 기준; 본문 각주도 동일).
- **litdb 안의 직접 중복·협업 없음**: 우리 litdb 어느 digest 에도 `Kyoungmin Min` · `Yerim Jung` · `Jiwon Sun` · `Juo Kim` · `Woojin Shin` **0회** (grep 실측).
- ⚠ **"연세대" 표기 주의** — 우리 litdb 의 연세 트랙(`litdb/yonsei_dtbl_lab_triage_2026.md`, 이용민 DTBL 화공생명)과 **다른 학과·다른 그룹**이다. `hyun_han_argyrodite_moisture_degradation_design_principles.md` 머리에 이미 같은 주의가 달려 있다. **혼동 금지.**
- 🔗 **간접 연결 2건 (사실만)**:
  1. **ref [51] = Park T, Kim J, Jung Y, Sun J, Min K**, *J. Energy Chem.* **107**, 103 (2025) — **이 논문 저자들 자신의 직전 작업**(Na-ion 층상 양극 도펀트 고속스크리닝). 본문 intro 에서 *"2,550 doped LTMOs were generated without DFT"* 로 인용한다. ⚠ **숫자 2,550 이 두 논문에서 똑같다** (§10-9).
  2. **ref [34] = Do Lee B, Gavali DS, … Park WB, Sohn K-S**, *JMCA* **13**, 10462 (2025) — Na-아지로다이트 4,375종을 **같은 coGN/coNGN** 으로 훑은 편. 우리 litdb 에 **같은 그룹(Sohn/Park, 세종대)의 자매편**이 있다: `papers/cho2025_multicompositional_argyrodite_experimental_active_learning.md`. ⇒ **coGN/coNGN 기반 SSE 스크리닝은 국내에 최소 2개 그룹의 계보가 있다.**

---

## 3. 핵심 물성 (수치)

> ⛔ **전부 소환값.** 우리 db 절대값과 같은 표에 놓지 않는다. 특히 σ 는 **AIMD 700–1300 K → 300 K 외삽 + Nernst–Einstein(Haven=1)** 이고 **pristine LGPS 의 같은-방법 기준값이 이 논문에 없다**.

### 3-1. 최종 4종 (`Fig. 5c` 정본 — 본문에는 17.28 하나만 있다)

| 물질 | **Ea (meV)** | **σ(300 K) (mS/cm)** | 도핑 내용 | ECW (V) | V_red / V_ox (V) |
|---|---|---|---|---|---|
| **Li₉P₃OS₁₁** | **209** | **17.28 ± 8.64** | **P→Ge자리 + O→S자리** | **0.639** | 1.717 / 2.356 |
| Li₉GaP₂Cl₂S₁₀ | 283 | 2.56 ± 1.28 | Ga→Ge자리 + Cl₂→S자리 | 0.639 | 1.717 / 2.356 |
| Li₉GaP₂I₂S₁₀ | 308 | 1.24 ± 0.62 | Ga→Ge자리 + I₂→S자리 | 0.639 | 1.717 / 2.356 |
| Li₉YP₂Cl₂S₁₀ | 337 | 0.61 ± 0.31 | Y→Ge자리 + Cl₂→S자리 | 0.606 | 1.717 / 2.323 |
| **Li₁₀GeP₂S₁₂ (LGPS)** | **n/a (미계산)** | **n/a (미계산)** — 본문은 실험 문헌 **1–10 mS/cm** 를 쓴다 | — | 0.579 | 1.717 / **2.296** |

⚠ **± 는 네 물질 전부 정확히 값의 50 %** (1.28/2.56 · 0.62/1.24 · 8.64/17.28 · 0.31/0.61 = 0.500·0.500·0.500·**0.508**). 본문은 *"relative uncertainties remain between 40 and 60 %"* 라고 쓰지만 **실제로는 단일 스칼라를 네 물질에 곱한 것**이다 — **물질을 가르는 정보가 0** (§10-3).

### 3-2. 최종 4종의 ML 예측 물성 — ⚠ **`Table 2`(본문) 와 `Table S3`(SI) 가 어긋난다**

| 물질 | E_form (eV/atom) | E_gap (eV) | G_VRH (GPa) | G/K | E_hull ML | **E_hull DFT** |
|---|---|---|---|---|---|---|
| **Li₉P₃OS₁₁** — `Table S1`… **`Table S3` 값 (정본)** | **−1.354** | **2.645** | **9.156** | **0.448** | 0 | **0.034** |
| Li₉P₃OS₁₁ — `Table 2` 값 (⛔ 오배정) | −1.470 | 2.555 | 9.964 | 0.472 | 0.000 | — |
| Li₉P₃O₂S₁₀ — `Table S3` | **−1.47** | **2.555** | **9.964** | **0.472** | 0 | 0.041 |
| Li₉GaP₂Cl₂S₁₀ | −1.354 | 2.524 | 9.590 | 0.467 | 0.004 | 0.089 |
| Li₉GaP₂I₂S₁₀ | −1.220 | 2.238 | 9.327 | 0.483 | 0.019 | 0.074 |
| Li₉YP₂Cl₂S₁₀ | −1.495 | 2.448 | 10.334 | 0.457 | 0 | 0.085 |
| **LGPS** (`Table S3` 에선 `Li₁₀Ge₀.₅P₂Ge₀.₅S₁₂`) | −1.277 | 2.384 | 10.658 | 0.434 | 0 | 0.023 |

🔴 **`Table 2` 의 Li₉P₃OS₁₁ 행은 `Table S3` 의 Li₉P₃O₂S₁₀ 행 값이다** (E_form·E_gap·G·G/K 네 칸 모두 정확히 일치). **`Fig. 4b`·`Fig. 4c` 가 `Table S3` 손을 들어 준다** — `Fig. 4b` 의 ECW 0.639 짜리 파란 점 4개가 x = **2.524 / 2.555 / 2.626 / 2.645 eV** 에 찍혀 있고 화살표가 가장 오른쪽(2.645)을 **Li₉P₃OS₁₁** 으로 지목한다. ⇒ **`Table S3` 를 쓴다. `Table 2` 의 Li₉P₃OS₁₁ 행은 인용 금지.**

### 3-3. ECW 그룹 평균 (`Table 1`)

| 그룹 | E_form (eV/atom) | E_gap (eV) | E_hull (eV/atom) | G_VRH (GPa) | G/K | ECW (V) |
|---|---|---|---|---|---|---|
| **HECW** (상위 132종, ECW ≥ 0.4231 V) | −1.363 | 2.337 | 0.002 | **11.326** | 0.456 | **0.474** |
| **MECW** (195종, 0.1582 ≤ ECW < 0.4231 V) | −1.327 | 2.336 | 0.002 | 10.409 | 0.462 | 0.277 |
| **LECW** (나머지 546종, ECW < 0.1582 V) | −1.328 | 2.285 | 0.001 | 10.468 | 0.463 | **0.094** |

저자 결론: *"ECW is not strongly correlated with other properties"* — E_form·E_gap 차이가 미미하다. ✅ **동의한다.** 그룹 평균 E_gap 이 2.285–2.337 eV 로 **52 meV 안**이다.

### 3-4. 깔때기 통과 수

| 단계 | 기준 | 남은 수 | 탈락률 |
|---|---|---|---|
| 시작 | — | **2,550** | — |
| ① 열역학 (ML) | E_form < 0 **AND** E_hull < 0.025 eV/atom | **2,065** | 19.0 % |
| ② 밴드갭 (ML) | E_gap > 2.0 eV | **987** | 52.2 % |
| ③ 탄성 (ML) | G_VRH > 8.4 GPa **AND** G_VRH/K_VRH < 0.7 | **873** | 11.5 % |
| ④ **ECW (DFT)** | ECW ≥ 0.58 V | **21** | **97.6 %** ← 압도적 게이트 |
| ⑤ σ (AIMD) | — (비용 제약) | **4** | — |

🔑 **④ 가 깔때기 전체를 결정한다** — 우리 `kb/open_items.md` T10 기록 *"발견 깔때기(Kim 2026은 ECW에서 94.3 % 제거)"* 와 **같은 구조**다. 여기선 **97.6 %**.

### 3-5. ML 모델 성능 (`Table S1`, `Table S2`)

| 모델 | 타깃 | MAE (본 연구) | MAE (Matbench 최고) | Max error (본/Matbench) |
|---|---|---|---|---|
| coGN | E_form (eV/atom) | **0.0176** | 0.0170 | 4.0514 / 3.8249 |
| coGN | E_gap (eV) | **0.1597** | 0.1559 | 7.4431 / 7.3352 |
| coNGN | G_VRH (log GPa) | **0.0682** | 0.0670 | 1.1475 / 1.1760 |
| coNGN | K_VRH (log GPa) | **0.0502** | 0.0491 | 1.6792 / 1.6329 |

황(S) 함유 부분집합만 (`Table S2`): coGN E_form MAE **0.0171 eV/atom** (R² 0.9947) · E_gap MAE **0.1861 eV** (R² 0.9361) · coNGN G_VRH **0.0690** (R² 0.8895) · K_VRH **0.0532** (R² 0.9299). 본문 주장: *"E_gap MAE 가 0.0264 eV 만 늘었다"* (0.1597 → 0.1861).

---

## 4. DFT/계산 방법 ★

| 항목 | 값 | 우리 대비 비고 |
|---|---|---|
| **code** | **VASP** (버전 미기재) | 우리 QE. PAW 데이터셋·에너지 기준이 달라 **총에너지 이식 불가** |
| **functional** | **PBE-GGA** | 같음 |
| **vdW** | ⛔ **없음** — 명시 배제. 근거: *"van der Waals interactions are expected to play a minor role in determining the bulk energetics of LGPS-type solid electrolytes"* [72] | 우리도 D3 미사용 |
| **pseudo / PAW** | 기재 없음 ("MP 기본설정" 으로만 암시) | ⚠ 재현 불가 구간 |
| **E_cut** | **520 eV** (정적/ECW) · **500 eV** (AIMD) | MP 표준 520 eV |
| **k-points** | **2×2×1 Monkhorst–Pack** (정적) · **Γ점만** (AIMD) | ⚠ 2×2×1 은 c축(12.5 Å)이 1점 — LGPS 의 **1D Li 채널이 c축**이라 하필 그 방향이 가장 성기다 |
| **수렴 임계** | *"following the default settings of Materials Project"* | 수치 미기재 |
| **supercell / nat** | **미기재.** §2.2 에서 *"20 Li and 24 S atoms per supercell"* 이라고만 — 이는 LGPS **Z=2 통상셀 = 50원자**. ⇒ **Li₉P₃OS₁₁ 은 18 Li + 6 P + 2 O + 22 S = 48원자** (**우리 유도, 논문 미보고**) | 🔴 우리 modelc 는 nat 120. **그들은 50 원자에 Li 18–23개로 MSD 를 낸다** |
| **DFT+U** | ⛔ **없음** — 명시 배제. 근거: *"intended for consistent, relative stability across a large number of compositions"* | ⚠ Co·Cr·V·Mn·Ni·Cu·Fe 계 도펀트의 E_form·E_hull 이 **계통적으로 틀릴 수 있다**. 마침 그 원소들이 survival 0 % 군이다 (§10-6) |
| **AIMD ensemble** | **NVT · Nosé–Hoover** [73] | 우리는 **Langevin NVT** (friction 0.02) |
| **AIMD T** | **700 / 900 / 1100 / 1300 K** 4점 | 우리 600/800/1000 K 3점 |
| **AIMD dt / 길이** | **dt 2.0 fs** · 평형 5,000 step (**10 ps**) · 생산 50,000 step (**100 ps**) | dt 같음. 우리 평형 5 ps / 생산 **200 ps** |
| **시드/복제** | ⛔ **1개.** 온도당 궤적 1개, 시드 언급 0회 | 우리 600 K **3-seed** |
| **MSD 창** | ⛔ **미기재.** 창·시간원점·절편 규약 **없음** | 우리 **2–50 ps 고정 · 자유절편 OLS** |
| **σ 환산** | **Nernst–Einstein** [74]. Haven 비 언급 0회 ⇒ **H_r = 1 암묵 가정** | 우리도 Haven=1 **가정**하되 **절대값 인용 금지** 규율을 건다 |
| **불확도** | *"propagating the relative standard deviation of the diffusivity obtained from MSD fitting at each temperature, and using the **average relative uncertainty across the four AIMD temperatures**"* [74 = He 2018] | 🔴 **평균을 취하는 순간 물질별 정보가 사라진다** — 그래서 네 값이 전부 50 % 다. `[He18]` 의 요지(**물질·온도마다 다르다**)를 정면으로 거스른다 |
| **MLIP** | **CHGNet** [53] — 구조 완화 전용. 최대 **10,000 step**, **full cell relaxation**. 학습셋 = MP 완화 궤적 | 우리 **UMA-s-1p1(omat)** — 우리는 MD 까지, 그들은 **완화만** |
| **★ 무질서 처리** | 🔴 **정의되지 않았다.** §2.2 는 `²⁰C₆ × ²⁴C₄ = 411,793,760` 조합을 제시하고 *"therefore, the CHGNet was employed"* 로 끝낸다 — **조성당 몇 개 배열을 만들었는지 · 어떻게 뽑았는지(무작위/SQS/enumerate) · 어떤 기준으로 골랐는지 한 줄도 없다.** SI 에도 없다 | 🔴 **우리 대비 최대 약점.** 우리는 배열 앙상블(disorder ensemble)·다시드를 명시한다. ⇒ **Li₉P₃OS₁₁ 의 PS₂O₂ 기전 전체가 "이름 없는 단일 배열" 위에 서 있다** (§10-5) |
| **ECW** | **대분배포텐셜 상도(GPPD)** · `pymatgen.analysis.phase_diagram` [76] · μ_Li(φ) = μ_Li,0 − eφ · ECW = V_ox − V_red · **873종 전수 DFT** | ✅ **우리 `get_element_profile` 과 같은 계열.** 상 집합(phase set)·MP 스냅샷 **미기재** — 우리는 LiS4/SCl₃/Li₅PS₄Cl₂ 제외를 명시한다 |

---

## 5. Figure set ★

> 🔎 **본 그림 / 안 본 그림 (정직 고지)** — 크로핑 **11장**(본문 `fig_1`–`5` · SI `fig_S1`–`S6`) + 표 5장.
> **실제로 Read 로 본 것 7장**: `Fig. 1` · `Fig. 2` · `Fig. 3` · `Fig. 4` · `Fig. 5` · `Fig. S4` · `Fig. S6`.
> **안 본 것 4장**: `Fig. S1`(ML 산점도 — 수치가 `Table S1` 에 전부 있음) · `Fig. S2`(황 부분집합 산점도 — `Table S2`) · `Fig. S3`(공간군 히스토그램 — SI 텍스트에 목록 있음) · `Fig. S5`(ECW–G_VRH — `Fig. 4c` 의 G/K 판과 정보 중복).
> 표 `tab_*.png` 5장은 **PDF 텍스트가 정확해서 이미지로 안 봤다** (관례).

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1 | 4단 파이프라인 도식: (a) 구조생성 ICSD XRD → LGPS → 도펀트 선택 → **MLIP-based structure generation** → 2,550 (b) ML coGN→E_form/E_hull/E_g, coNGN→G/K (c) DFT **GPPD → [V_red, V_ox] → ECW** (d) AIMD MSD → D vs 1000/T. **(d) 패널이 300 K 점을 빨간 점 + `extrapolation at 300K` 로 명시** | **우리 cascade 의 "문헌 대응 파이프라인" 슬라이드 1장.** ⭐ 도식 자체가 **300 K 가 외삽임을 자백**한다 — 우리가 §10-1 비판을 걸 때 *"저자도 그림에 그렇게 썼다"* 로 받칠 수 있다 |
| 2a | 깔때기 숫자판: 2,550 → 2,065(coGN) → 987(coGN) → 873(coNGN) → 21(DFT) → 4(AIMD). 각 단계에 **어느 모델이 판정하는지** 라벨 | 우리 Stage 00–12 와 **1:1 대응표** 만들 때 그대로 쓴다 (§14) |
| 2b | **40종 도펀트 주기율표** — 노랑 Li자리 8 · 파랑 Ge/P자리 · 진회색 S자리. **`57-71 La-Lu` 칸이 회색 = 란타나이드 전부 제외** | 🔴 **선점 판정의 1차 증거.** Nd 부재를 눈으로 확인한 곳이 여기다 |
| 2c | LGPS 구조(Li1–Li4 자리, (Ge/P)S₄·PS₄ 사면체) + **9개 도핑 템플릿 표** + 비율: A,A′ ∈{0,1.5,3.0} · B,B′ ∈{0,0.5,1} · **D,D′ ∈{0,0.25}** · X,X′ ∈{0,1.0,2.0} | 🔴 **"dual-doped" 정의의 정본** (§13). ⚠ **D 비율이 본문(0.5)과 그림(0.25)에서 다르다** (§10-8) |
| 3a | 873종의 E_hull(0–0.02, **로그 counts, 0 에 거대 스파이크**) · E_gap(1.9–2.8 eV, 봉우리 2.25–2.35) · G_VRH(7–16 GPa, 봉우리 ~11) · G/K(0.42–0.7, **0.44–0.46 에 스파이크**) 분포 + 누적% | **우리 cascade 의 같은 4장 분포를 나란히 놓는 그림**의 문헌 대응. ⭐ E_gap 이 **2.0–2.7 eV 안에 전부** 들어온다 = LGPS 유도체의 gap 이 사실상 안 움직인다 |
| 3b | **873종 ECW 분포(0–0.7 V)** + LECW/MECW/HECW 띠 + 0.58 V 빨간 점선 + `21 materials` | 🔴 **축퇴의 시각 증거** — 0 근처 ~340종, 0.42–0.44 에 ~103종 스파이크. **연속분포가 아니라 계단이다.** 우리 *"onset 축퇴 = 완전한 계단 함수"* 진단과 **같은 현상** (§7-C). ✅ 띠 경계가 **0.16·0.42** 에 그어져 **본문 값(0.1582/0.4231)을 지지**하고 **캡션(1.5/3.0 V)을 반박**한다 |
| 3c | **17종 대표 물질의 [V_red, V_ox] 절대 막대** (x축 1.6–2.4 V vs Li). **모든 막대의 왼쪽 끝이 ≈1.71 V 이상** — 1.71 V 아래로 내려가는 후보가 **하나도 없다** | 🔴🔴 **이 논문 최대의 반증이 여기 있다.** 873종 어디에도 **pristine LGPS 보다 환원에 강한 조성이 없다.** 초록의 문제제기(Li 금속 반응성)를 **한 종도 못 풀었다.** ⭐ 우리 §B 서사에 직접 인용 가능 |
| 3c (추가) | 개별 읽기: `Li₉GaP₂Cl₂S₁₀` ≈1.72–2.355 · `Li₁₀Ge₀.₅Zr₀.₅P₂O₂S₁₀` ≈1.71–1.94 (**Zr+O 공치환인데 ECW 는 LECW/MECW급**) · `Li₈.₅Rb₁.₅Ge₀.₅Ti₀.₅P₂S₁₂` 은 **폭 ≈0** | ⚠ **양이온+O 공치환이 자동으로 좋지 않다는 반례** — 우리 Nd₂O₃ 서사를 과대주장하지 않게 붙잡아 주는 자료 |
| 4a | **21종 ECW 정렬 막대** (x축 1.717 부터 브레이크). **21종 + LGPS 전부 V_red = 1.717 V 고정**, V_ox 만 **2.296 / 2.310 / 2.323 / 2.356 V** 네 값 | 🔴🔴 **선점 판정과 §7-C 의 핵심 그림.** ECW 전체 개선폭 = **+60 mV**. 11종이 LGPS 와 **동률**(0.579), 10종만 상회 |
| 4b | ECW vs E_gap (21종). ECW 0.639 짜리 파란 점 4개 x = 2.524/2.555/2.626/2.645 eV | ✅ **`Table 2` vs `Table S3` 충돌의 심판** — Li₉P₃OS₁₁ = **2.645 eV** 확정 (§3-2) |
| 4c | ECW vs G_VRH/K_VRH (21종). LGPS 가 **최좌단 ≈0.433**, Li₉P₃OS₁₁ 과 Li₉P₃S₁₂ 가 **≈0.448 에 겹침** | 🔴 **본문의 *"Li₉P₃OS₁₁ 이 21종 중 G/K 최저"* 주장을 반박한다** — 최저는 LGPS(0.433)와 Li₉.₅Ge₀.₅P₂.₅S₁₂(0.433) (§10-4) |
| 5a | 4종 × 4온도 **MSD(t) 100 ps**. Li₉GaP₂Cl₂S₁₀ 1300 K 가 ~800 Å², Li₉P₃OS₁₁ 1300 K 는 ~490 Å² | ⚠ **700 K 곡선이 4종 모두 거의 평평**(50–100 Å²) — 저온 점의 통계가 가장 약한데 **Arrhenius 기울기를 그 점이 좌우한다** |
| **5b** | **Arrhenius D vs 1000/T (0.7–1.5)**. `figure-read ≈`: **1300 K** — 검정(GaCl₂) ≈1.2e-4 > 초록(YCl₂) ≈1.1e-4 > 빨강(GaI₂) ≈0.95e-4 > **파랑(P₃OS₁₁) ≈0.75e-4 (최하위)**. **700 K** — **파랑 ≈1.5e-5 (최상위)** > 검정 ≈1.2e-5 > 빨강 ≈1.05e-5 > 초록 ≈0.85e-5. **선들이 ~900–1100 K 에서 교차한다** | 🔴🔴 **헤드라인 반증.** 챔피언은 **실제로 시뮬레이션한 온도에서 1등이 아니다** — 1등은 **외삽에서 생긴다** (§10-1). ⭐ 우리 *"Ea 도 상대차로만"* 정책의 외부 근거 |
| 5c | **Ea·σ 표 (정본)**: 283/2.56±1.28 · 308/1.24±0.62 · **209/17.28±8.64** · 337/0.61±0.31 | ± 가 **전부 값의 50 %** = 일괄 스칼라 (§10-3) |
| S4a | **40종 전체 survival rate 내림차순**. `figure-read ≈`: Ge 62.5 · Si 62.5 · Sn 61.5 · B 59.5 · Ga 59.5 · Nb 58 · Ca 56 · Na 55.5 · Zr 55 · Al 54 · **Cl 53.5** · Ti 53 · Bi 52.5 · Be 51 · P 50 · **O 50** · Sr 49.5 · Sc 49 · Zn 45 · Y 44 · Se 39 · Ba 38.5 · I 38.5 · Br 36 · F 36 · Rb 26 · Ag 18 · Pb 15 · Sb 14 · As 9.5 · C 9 · Te 6 · Mn 3.5 · Cu 1.5 · Mo 1 · **Ni Cr Co V N = 0** | 🟡 **우리 47종 tier 와 대조할 유일한 문헌 순위표** — 단 **분모가 정의돼 있지 않다** (§10-7). 순위만 쓰고 % 는 인용 금지 |
| S4b | **자리별** survival. **S자리: Cl ≈53.5 > O ≈50.5 > Se ≈39.5 > I ≈39 > Br ≈36 ≈ F ≈36 > N ≈24.5** · Li자리: Ca 56 > Na 55.5 > Al 54 > Sr 49 > Ba 39 > Rb 26 > Ag 18 > **Ni 0** · Ge자리: Si 61.5 > Sn 60.5 > Ga 59 > Zr 55 > Ti 53 > Be 51 > Sc 49.5 > Sr 49 > B 45 > Y 44.5 > P 34 > C 23 > Pb 15 > Te 6 > Mn 3.5 > Mo 1.5 > **Co V Cr 0** · P자리: Si 61.5 > Sn 60.5 > Nb 58 > Bi 52.5 > Zn 45 > Ge 37.5 > Sb 14.5 > As 10 > Mn 3.5 > Cu 1.5 > Mo 1 > **Cr V 0** | 🔴 **"S자리 최적은 Cl 과 O" 의 원본.** ⚠ **(a) 와 (b) 가 서로 안 맞는다** — N: (a) **0** vs (b) **≈24.5**; Ge: (a) 62.5 vs (b) P자리 37.5; B: (a) 59.5 vs (b) Ge자리 45; P: (a) 50 vs (b) 34; C: (a) 9 vs (b) 23 (§10-7) |
| S6 | **Li₉P₃OS₁₁ 구조** (VESTA류, 노랑 S · 빨강 O · 초록/보라 다면체) + **PS₂O₂ 사면체 확대**(P 중심, S 2 + O 2) | 🔴 **O-치환 기전의 유일한 구조 근거.** ⚠ 조성상 셀에 O 가 **2개**뿐인데 둘 다 **같은 P 에 붙어야** PS₂O₂ 가 된다 ⇒ 대안 배열(PS₃O 두 개)은 **검토 흔적이 없다** (§10-5) |
| Table S1 | coGN/coNGN vs Matbench MAE·max error | 우리가 대리모형을 도입한다면 **기대 MAE 기준선** |
| Table S2 | 황 함유 부분집합 MAE·MSE·R² | ⭐ *"산화물 편중 MP 로 학습해도 황화물에서 안 나빠진다"* 의 정량 근거 — **우리 UMA(omat) 를 황화물에 쓰는 것의 간접 방어** |
| Table S3 | **20종 ML 물성 + DFT E_hull** | 🔴 `Table 2` 오배정의 심판 + **ML E_hull 과대안정화의 증거** (§10-10) |

---

## 6. Post-processing ★

- **무엇**: ① **대분배포텐셜 상도(GPPD)** → V_red·V_ox·ECW (873종 전수) ② **MSD → D → Arrhenius → Nernst–Einstein σ(300 K)** ③ **dopant survival analysis** (자체 정의, 분모 미기재) ④ ML 예측값의 DFT 검증 (E_hull **20종만**).
- **도구**: **pymatgen** `analysis.phase_diagram` (GPPD) · **VASP** (DFT·AIMD) · **CHGNet** (완화) · **KGCNN** (coGN/coNGN 그래프: `KNNAsymmetricUnitCell` 24-NN + 10⁻⁹ Å 여유 / `VoronoiAsymmetricUnitCell` 12-NN + 10⁻⁶ Å) · 구조 그림은 VESTA 계열로 보이나 **미기재**.
- **수치화·플롯·기록**: `Fig. 3a` 는 **히스토그램 + 누적%** 이중축 (E_hull 만 로그 counts). `Fig. 4a` 는 **x축 브레이크 + 절대전압** — ⭐ **이 양식이 좋다**: ECW 를 폭(스칼라)이 아니라 **[V_red, V_ox] 구간**으로 그려서 *"어느 쪽이 움직였나"* 가 한눈에 보인다. **우리 ESW 그림도 이렇게 바꿀 가치가 있다** (§8-③).
- ⛔ **안 한 것**: NEB 0 · COHP/ICOHP 0 · Bader 0 · DOS/PDOS 0 (E_gap 은 **전부 ML 예측값**, DFT DOS 를 한 번도 안 그린다) · ELF 0 · phonon 0 · BVSE 0 · 계면 슬랩 0 · 실험 0.

---

## 7. 우리 DFT 대비 (comp1 / modelc) → `litdb/our_dft_baseline.md`

### 7-A. 물성 대조표

| 항목 | [Jung26LGPS] | 우리 (comp1 / modelc) | 차이 / 이유 · 판정 |
|---|---|---|---|
| **계** | Li₁₀GeP₂S₁₂ (P4₂/nmc) | Li₆PS₅Cl / Li₅.₄PS₄.₄Cl₁.₆ (F-43m) | **다른 구조족.** 값 1:1 대응 금지 |
| **V_red** | **1.717 V** — 21종 + LGPS **전부 동일** | **OCV 1.717 V** (comp1 = modelc, 불변) | 🔵🔵 **소수점 셋째 자리까지 같다.** 서로 다른 두 황화물에서 같은 값이 나온 것은 **우연이 아니라 MP hull 의 공통 Li–P–S 환원 화학**(Li₃P/Li₂S 생성)이 둘 다를 지배하기 때문으로 보인다 — **우리 유도, 양 논문 모두 미논평**. ⚠ 우리 표의 *"환원 한계 1.242 V"* 와는 **다른 양**이다. 라벨을 섞지 말 것 |
| **V_ox (host)** | **2.296 V** (pristine LGPS) | **2.256 V** (comp1·modelc, LiS4 제외 phase set) / **2.14 V** (LiS4 포함, cascade 앵커) | 🔵 **40 mV 차이.** 같은 pymatgen 대분배포텐셜인데 **상 집합이 다르고 그들은 자기 집합을 안 밝혔다** ⇒ **이 40 mV 를 "LGPS 가 아지로다이트보다 산화에 강하다" 로 읽으면 안 된다** |
| **★ V_ox (최고)** | **2.356 V** (Li₉P₃OS₁₁·Li₉GaP₂Cl₂S₁₀·Li₉GaP₂I₂S₁₀·Li₉P₃O₂S₁₀·Li₉P₃S₁₂) | **2.356 V** — 우리 cascade 에서 **Cr₂O₃ · Ga₂O₃ · In₂O₃ · Sc₂O₃** 가 정확히 이 값으로 올린다 (`db/properties/cascade_screening_funnel.json`). 무도핑 host 도 −Li−S+Cl 4회면 2.356 V 로 점프 (`our_dft_baseline.md` §비교 주의) | 🔴🔴 **같은 숫자가 양쪽에서 나온다.** 그들의 "이원도핑 ECW 개선" 종착점과 **우리가 이미 본 kink 가 동일**하다 ⇒ **2.356 V 는 도펀트 고유 성질이 아니라 Li–P–S(–Cl/O) 화학의 공통 계단이다.** ⭐ 그리고 **Ga 는 양쪽에서 같은 역할**을 한다 — 그들의 챔피언 Ga 화합물 2종이 2.356 V, 우리 Ga₂O₃ 도 2.356 V |
| **ECW 개선폭** | **+0.060 V** (0.579 → 0.639), V_red 기여 **0** | 우리 cascade: host 2.14 V 앵커 ±0.2 V, onset 을 올리는 소수(B₂O₃ 2.317 · Cr₂O₃/Ga₂O₃/In₂O₃/Sc₂O₃ 2.356 · Y₂O₃ 2.282) | 🔵 **같은 크기의 레버다.** 양쪽 다 **수십~수백 mV** 이고 **계단이다** |
| **E_gap** | **ML 예측** 2.0–2.7 eV (873종), LGPS 2.384 eV, 챔피언 2.645 eV. **DFT 로 한 번도 검증 안 함** | **DFT PBE fixed-occ nscf VBM/CBM**: comp1 **2.066** / modelc **2.099** eV | ⚠ **비교 금지 — 방법이 다르다.** 그들은 coGN 예측(MAE 0.16–0.19 eV), 우리는 고유값. ✅ **"둘 다 wide-gap 절연체" 수준만.** ⭐ 다만 **문턱 설계는 배울 만하다**: 그들은 *"PBE 가 1–2 eV 과소평가하므로 문턱을 2.0 eV 로 둔다"* 고 **명시**한다 — 우리 밴드갭 규율과 같은 정신 |
| **기계 (G_VRH)** | **ML 예측** 9.16–12.11 GPa (21종), LGPS 10.658 GPa. 문턱 **>8.4 GPa** (Monroe–Newman) | **DFT elastic (C_ij)**: E_VRH comp1 **22.06** / modelc **27.66** GPa · B₀ 26.23 / 21.71 GPa | ⚠⚠ **비교 금지 — 양이 다르다** (그들 전단 G, 우리 영률 E + 체적 B). 게다가 그들은 **ML 예측**이고 **DFT 로 한 번도 검증 안 했다** |
| **Pugh (G/K)** | 문턱 **<0.7**. 실제 873종은 **0.42–0.7 에 갇혀** 있고 21종은 **0.433–0.484** | 우리 cascade `elastic_pugh_GoverB` 열 존재 | 🔵 **문턱이 vacuous 하다** — `Fig. 3a` 의 G/K 분포가 이미 0.44–0.46 에 몰려 있어 **0.7 컷이 거의 아무도 안 자른다**. (③단계 탈락 11.5 % 는 대부분 G>8.4 GPa 쪽) ⇒ **우리 T10 "E_hull 필터가 무력" 과 같은 종류의 무력 게이트** |
| **Ea** | **209–337 meV** (AIMD 700–1300 K, 4점, 단일 궤적) | comp1 **0.253** / modelc **0.224** eV (MLIP-MD 600/800/1000 K, 단일 궤적) / modelc 3-seed **0.197 ± 0.032** | ⚠ **절대값 비교 금지** (힘 계산 축이 다르다: AIMD-PBE vs UMA). ⭐ **범위는 놀랍도록 겹친다** — 209 meV(그들 최고) vs 197–224 meV(우리 modelc). 하지만 계·방법이 다 달라 **우연 일치로 취급** |
| **σ** | **17.28 / 2.56 / 1.24 / 0.61 mS/cm** (300 K 외삽) | 🚫 **우리는 σ 절대값을 인용하지 않는다** (1저자 정책) | 🔴 **같은 표에 놓지 않는다.** §17 에서 A축 편입을 **거부**한다 |
| **무질서 처리** | 🔴 **미정의** (조성당 배열 수·선정 규칙 없음) | 배열 앙상블 · 다시드 · 명시된 창 | ✅ **우리가 명백히 낫다.** 이것이 **가장 방어하기 쉬운 구별선**이다 |
| **불확도** | **일괄 50 %** | 3-seed 실측 ±0.032 eV | ✅ 우리가 낫다 |
| **계면 축** | ⛔ 없음 (저자 자인) | T9 5상대 47종 전수 | 🟢 **우리만 있다** |
| **대기안정 축** | ⛔ 없음 (저자 자인: *"dopant volatility, toxicity, … outside the scope"*) | T11 ΔE_H₂S 47종 | 🟢 **우리만 있다** |

### 7-B. 🔴 우리에게 불리한 결론 (그대로 적는다)

1. **O 로 S 를 치환해 국소 왜곡을 만들어 Li 수송을 돕는다** — 이제 **황화물 SSE 에서 출판된 결론**이다. 우리가 이걸 *새로운 통찰*로 쓰면 리뷰어가 이 논문을 던진다. **인용하고 넘어간 뒤, 우리 기여를 "자리(4a/4d vs PS₄ 내부)와 전하중성 방식"에서 찾아야 한다.**
2. **Cl 이 황화물 음이온 자리 최적 도펀트다** — 같은 이유로 **우리 발견이 아니다.**
3. **"ML 대리모형으로 수천 조성을 걸러 DFT+AIMD 로 마감" 프레임** — 선점. 우리 cascade 의 *구조*를 신규성으로 내세울 수 없다. 신규성은 **축의 구성**(계면·대기·보고량 규율)과 **계**(아지로다이트 + 란타나이드)에 있다.
4. **규모에서 진다** — 그들 2,550 종 vs 우리 302 종. *"우리가 더 넓게 봤다"* 고 쓸 수 없다. ⚠ 단 그들의 2,550 은 **ML 예측**이고 우리 302 는 **대부분 실계산**이라 **깊이로 맞선다**.

### 7-C. 🟢 우리에게 유리한 결론 (근거 있는 것만)

1. **산화 onset 축퇴를 진단한 것은 우리다.** `Fig. 3b`·`Fig. 4a` 가 축퇴를 **보여주지만** 저자는 한 줄도 논평하지 않는다. 우리 `cascade_screening_funnel.json` 은 *"onset 축퇴(19종이 정확히 2.14 V) 탓에 완전한 계단 함수다 — 컷을 0.05 V 만 올리면 코어 생존자가 11 → 0"* 이라고 **명시적으로 진단해 뒀다**. ⇒ **같은 현상을 두 계에서 독립 관측**했고, **해석은 우리 쪽에만 있다.**
2. **산화안정 ↔ 수송 trade-off 를 우리가 먼저 적었다.** 우리 기록: *"예외적으로 onset 을 올리는 소수(…)는 G4 에서 탈락해 코어에 남지 않는다 = 산화안정과 수송의 정면 trade-off."* 그들 데이터도 **같은 방향**이다 — onset 최고군 중 **Ga·Y 계열이 σ 하위**(2.56 / 1.24 / 0.61 mS/cm). 그런데 본문은 *"we initially hypothesized that materials with enhanced ECWs would show lower conductivities. However, three out of the four candidates exhibited conductivities within the LGPS range"* 라며 **trade-off 를 부인**한다 — 그 부인은 `Fig. 5c` 가 받쳐주지 않는다 (§10-11).
3. **V_red 불변**이 두 계에서 모두 관측된다 — 우리 comp1·modelc 도 **환원/OCV 1.242/1.717 불변**이고, 그들 21종 + LGPS 도 **전부 1.717 V**. ⇒ ***"황화물의 환원 한계는 도핑으로 거의 안 움직인다"*** 는 **두 독립 계·두 독립 그룹의 일치**다. 우리 §B 서사에 **외부 근거로 붙일 수 있다** (단 *"안 움직인다"* 가 아니라 *"이 0 K 대분배포텐셜 잣대에서는 안 움직인다"* 로 축을 명명).

---

## 8. 적용 인사이트 (내 연구에 어떻게)

- **① `Fig. 4a` 양식을 우리 ESW 그림에 이식한다.** ECW 를 **폭 스칼라**로 그리면 "개선됐다"로 읽히지만, **[V_red, V_ox] 절대 구간 막대 + x축 브레이크**로 그리면 *"어느 쪽이 얼마나 움직였나"* 가 즉시 보인다. 이 논문은 그 그림 덕에 **자기 헤드라인을 스스로 약화**시켰다 — 우리는 같은 그림으로 **정직하게** 같은 것을 보여줄 수 있다. (하우스 스타일: `tools/figures/house_style.py`, Origin-ready CSV 동시 출력)
- **② "ML 대리모형 층" 은 우리 cascade 의 *앞단*으로만 붙일 가치가 있다.** 그들의 ④단계(DFT ECW)가 **97.6 %** 를 자른다 = **ML 3단(①②③)이 자른 것은 65.8 % 뿐**이고, 그 3단은 전부 ML 이라 **틀릴 수 있다**(E_hull 20종 중 6종이 DFT 와 0.05 eV/atom 이상 차이, §10-10). ⇒ **ML 을 쓰려면 "싸게 넓히는" 용도이지 "판정" 용도가 아니다.** 우리 다중충실도 규율(J-12/J-13)과 정확히 같은 결론.
- **③ Pugh 문턱(G/K < 0.7)과 Monroe–Newman 문턱(G > 8.4 GPa)은 우리 계에서 vacuous 할 가능성이 높다.** 그들 873종이 G/K **0.42–0.7** 안에 전부 들어왔다. **우리 cascade 에 같은 문턱을 붙이기 전에 분포부터 본다** — T10(E_hull 필터 무력) 의 재판이 될 수 있다.
- **④ `Table S2` 를 우리 UMA(omat) 방어에 쓴다.** *"산화물 편중 MP 학습셋이 황화물 예측을 악화시키지 않는다"*(E_gap MAE +0.0264 eV, R² 0.9361)는 **아키텍처는 다르지만 같은 걱정에 대한 외부 정량 근거**다. ⚠ coGN 은 **구조→물성 회귀**이고 UMA 는 **힘장**이라 **직접 이식 금지** — *"같은 걱정에 대한 다른 증거"* 수준.
- **⑤ 🔴 원고 Related work 에 이 논문을 **반드시** 넣고, 구별선 4개를 한 문장씩 박는다**: (i) 구조족(아지로다이트 3D 케이지 vs LGPS 1D c축 채널), (ii) 란타나이드 축(그들 0종), (iii) **전하중성을 염 내부에서 닫아 Li 함량 교락을 없앤다**(그들은 Li 로 보정), (iv) **계면·대기안정 축을 갖는다**(그들 자인 부재). ⇒ 이 네 문장이 없으면 *"LGPS 에서 이미 했다"* 로 반려당한다.
- **⑥ 그들의 §4 Future directions 를 gap 문장으로 직접 인용한다** — `[Park26ML]` 과 같은 용법. 특히 *"the current screening framework does not evaluate electrolyte–electrode interfaces"* 와 *"does not evaluate synthesis-related constraints"* 두 줄.

---

## 9. 인용 가능 문장 (deck/paper 용)

- *"High-throughput AI screening of 2,550 dual-doped LGPS compositions narrowed the space to 21 candidates whose electrochemical windows exceed that of the pristine host, yet the reduction limit remained pinned at **1.717 V vs Li/Li⁺ for every candidate**, with the entire window gain (**+60 mV**) appearing on the oxidation side alone [Jung26LGPS, `Fig. 4a`]."* ← ⭐ **우리 §B 서사에 가장 값어치 있는 한 줄**
- *"Dopant survival analysis across 40 candidate elements identified **Cl and O as the two most robust anion-site substituents** in the LGPS framework [Jung26LGPS, `Fig. S4b`]."* ← 우리 음이온 선택의 **외부 지지**이자 **선행연구 표시**
- *"Both AI-accelerated LGPS screening [Jung26LGPS] and our argyrodite cascade converge on the same discrete oxidation kink at **2.356 V**, indicating that this limit reflects shared Li–P–S(–Cl/O) decomposition chemistry rather than dopant-specific stabilization."* ← **우리 유도, 양쪽 논문 모두 미보고. 인용 시 반드시 (본 연구 대조) 표기**
- *"Recent AI-driven LGPS screening explicitly leaves electrode–electrolyte interfaces and synthesis constraints outside its scope [Jung26LGPS, §4], a gap our interface- and air-stability axes are designed to close."* ← intro gap 문장
- ⛔ **쓰면 안 되는 문장**: *"Li₉P₃OS₁₁ achieves twice the conductivity of LGPS"* — 분모가 **실험 문헌값**이고 분자가 **AIMD 외삽값**이다 (§10-2). 인용하려면 반드시 *"…relative to the experimentally reported 1–10 mS cm⁻¹ range, without a same-method AIMD baseline for the pristine host"* 를 붙인다.

---

## 10. 주의/한계 · 비판 ★ (over-claim 방지)

> 아래 13건은 **전부 논문 내부 자료(본문·SI·그림)만으로 검증한 것**이다. 외부 수치를 들여오지 않았다.

**10-1. 🔴🔴 헤드라인 1위가 "외삽에서만" 생긴다.**
`Fig. 5b` 를 직접 보면 (figure-read) **1300 K 에서 Li₉P₃OS₁₁ 의 D 가 4종 중 최하위**(≈0.75×10⁻⁴ vs 검정 ≈1.2×10⁻⁴)이고, **700 K 에서만 최상위**(≈1.5×10⁻⁵ vs 초록 ≈0.85×10⁻⁵)다. 선들이 **~900–1100 K 에서 교차**한다.
**우리 계산** (논문 미보고): 실측 최저온 700 K 에서 챔피언/최하위 D 비 ≈ **1.8배**(1.5e-5 / 0.85e-5) → 300 K 외삽에서 **28.3배**(17.28/0.61). **외삽이 격차를 ≈16배 증폭한다.** 챔피언/2위도 700 K 에서 ≈**1.25배** → 300 K 에서 **6.75배**(≈5.4배 증폭).
⇒ ***"Li₉P₃OS₁₁ 이 제일 빠르다" 는 600–1000 K 만큼의 외삽에 의존한다.*** 그들이 §4 에서 스스로 걱정한 *non-Arrhenius* 위험이 하필 여기에 걸린다.

**10-2. 🔴🔴 *"pristine LGPS 의 약 2배"* 에 같은-방법 분모가 없다.**
**LGPS 자신의 AIMD σ 를 이 논문은 계산하지 않았다** — `Fig. 5c` 는 4행 전부 도핑체고, `Table 2` 에도 σ 열이 없다. 분모는 intro 의 **실험 문헌값 1–10 mS/cm** 다. ⇒ **AIMD 외삽값 ÷ 실험값** 이라는 **방법 혼합 비율**이다. 게다가 *"약 2배"* 라면 분모가 ~8.6 mS/cm 인데 **그 값을 어디서 가져왔는지 쓰지 않는다**(1–10 범위 중 어느 점?). **우리 규율상 인용 금지 대상.**

**10-3. 🔴 오차막대가 물질을 가르지 못한다.**
`Fig. 5c` 의 ± 는 **네 물질 전부 값의 50 %** — §2.4 대로 *"네 온도 상대불확도의 **평균**"* 이라는 **단일 스칼라**를 곱했기 때문이다. 본문은 *"40–60 % 범위"* 라고 쓰지만 표는 50 % 하나다. ⇒ 이 ± 는 **물질별 통계가 아니다.** ⚠ 그들이 근거로 댄 `[He18]`(He, Zhu, Epstein, Mo, *npj Comput. Mater.* 4, 18)의 요지는 **불확도가 물질·온도마다 크게 다르다**는 것이라, **인용과 사용이 어긋난다.**

**10-4. 🔴 본문 주장이 자기 그림과 어긋난다 (G/K 최저).**
§3.4: *"Li₉P₃OS₁₁ also displayed the lowest G_VRH and G_VRH/K_VRH ratio among the 21 screened candidates."*
→ **G_VRH 는 맞다** (`Table S3` 9.156 GPa 로 20종 중 최저). **G/K 는 틀렸다** — `Table S3` 에서 Li₉P₃OS₁₁ = **0.448** 인데 LGPS **0.434** · Li₉.₅Ge₀.₅P₂.₅S₁₂ **0.433** 이 더 낮다. **`Fig. 4c` 를 보면 LGPS(분홍)가 최좌단에 있고 Li₉P₃OS₁₁ 은 3–4번째**다. ⇒ *"연화(softening)가 전도를 낳았다"* 는 기전 서술의 한쪽 다리가 빠진다.

**10-5. 🔴 무질서(배열) 처리가 정의되지 않았고, 핵심 기전이 거기에 걸려 있다.**
§2.2 는 `²⁰C₆ × ²⁴C₄ = 411,793,760` 을 제시하고 *"CHGNet 을 썼다"* 로 끝난다. **조성당 배열 수·표본 추출법·선정 기준이 본문·SI 어디에도 없다.** 그런데 챔피언의 기전(**PS₂O₂**)은 *"셀 안의 O 2개가 하필 같은 P 에 붙는"* **특정 배열**을 전제한다 — 대안(PS₃O 2개)은 **언급조차 없다**. ⇒ **Li₉P₃OS₁₁ 의 σ·Ea·기전 전체가 이름 없는 단일 배열 위에 있다.** 우리 규율(배열 앙상블)로 보면 **보고량이 정의되지 않은 상태**다.

**10-6. 🟠 DFT+U 부재가 하필 survival 0 % 군과 겹친다.**
U 를 안 쓴 이유는 *"상대 안정성의 일관성"* 인데, 정작 **Ni·Cr·Co·V(+Mn·Cu·Mo 저위)** 가 전부 탈락했다. GGA(무 U)는 **전이금속 산화/황화물의 E_form 을 계통적으로 과안정/과불안정화**시키는 것으로 알려져 있고, 그 계통오차가 **탈락 판정 자체를 만들었을 가능성**을 논문은 검토하지 않는다. ⚠ 단 ①②③ 단계는 **ML 예측(MP=GGA+U 혼합 학습)** 이라 DFT+U 부재와 직접 연결되진 않는다 — **두 층의 일관성이 오히려 더 불분명하다.**

**10-7. 🔴 "survival rate" 가 정의돼 있지 않고, `Fig. S4a` 와 `S4b` 가 서로 안 맞는다.**
분모(무엇 중 몇 %인가)가 본문·SI 에 **한 줄도 없다** (grep 실측: `survival` 5회, 전부 결과 서술).
그리고 두 패널이 **같은 원소에서 다른 값을 준다** (figure-read):
| 원소 | `Fig. S4a` | `Fig. S4b` (자리별) | 비고 |
|---|---|---|---|
| **N** | **0 %** | **≈24.5 %** (S자리) | 본문은 *"N exhibited 0 % survival"* 이라고 **(a) 를 따른다** |
| **Ge** | ≈62.5 % (1위) | ≈37.5 % (P자리) | Ge 는 P자리 전용 도펀트 |
| **B** | ≈59.5 % | ≈45 % (Ge자리) | B 는 Ge자리 전용 |
| **P** | ≈50 % | ≈34 % (Ge자리) | P 는 Ge자리 전용 |
| **C** | ≈9 % | ≈23 % (Ge자리) | C 는 Ge자리 전용 |
한 자리에만 쓰이는 원소는 두 패널 값이 **같아야 한다**. ⇒ **두 패널의 분모가 다르고, 어느 쪽도 정의돼 있지 않다.** **% 수치는 인용 금지, 순위만.**

**10-8. 🟠 도핑 비율이 본문과 그림에서 다르다.**
§2.2 본문: *"**0 and 0.5 atoms for P sites**"*. `Fig. 2c` 표: ***"D, D′: 0, 0.25"***. `Table S3` 의 실제 조성(Li₉.₅Ge₀.₅P₂.₅S₁₂ = P 자리 0.5 치환)은 **본문 쪽**을 지지한다. ⇒ 그림 표가 틀렸거나, **같은 자리에 두 도펀트를 넣는 템플릿에서만 0.25** 라는 설명이 빠졌다.

**10-9. 🟠 `2,550` 이라는 숫자가 다른 시스템에서도 똑같이 나온다.**
intro §1: *"Park et al. … As a result, **2,550 doped LTMOs** were generated without DFT [51]."* — ref [51] 은 **이 논문 저자들 자신의 직전 작업**(Na-ion 층상 양극)이고, 완전히 다른 화학·다른 자리인데 **개수가 소수점까지 같다**. 우연일 수도 있으나 **2,550 이 이 계의 조합 계산 결과라는 신뢰를 깎는다.**
**우리 재구성 (논문 미보고)**: 자리별 비영 조합수 = Li 8×2=16 · Ge 19×2=38 · P 13×1=13 · S 7×2=14. 교차자리 쌍 = 16·38 + 16·13 + 16·14 + 38·13 + 38·14 + 13·14 = **2,248**. 동일자리 쌍 = C(8,2) + C(19,2) + C(21,2 → S는 C(7,2)) = 28 + 171 + 21 = **220**. 합 **2,468**. 여기에 **단일도핑 81종**(16+38+13+14) **+ 무도핑 LGPS 1종** = **정확히 2,550**. ✅ **숫자는 재구성된다** — 다만 그러려면 *"dual-doped"* 집합에 **단일도핑 81종과 pristine 1종이 섞여 있다**는 뜻이고, 논문은 그것을 **말하지 않는다**(초록·제목은 전부 "2,550 dual-doped"). `Table S3` 의 `Li₉.₅Ge₀.₅P₂.₅S₁₂`·`Li₉P₃S₁₂` 가 실제로 **단일자리 치환**이라 이 재구성을 뒷받침한다.

**10-10. 🟠 ML E_hull 이 계통적으로 과안정화되고, 저자도 인정한다.**
`Table S3`: ML E_hull 이 **20종 중 16종에서 정확히 0**, 나머지도 0.004–0.019. **DFT 로 다시 계산하면 0.02–0.089 eV/atom** 로 전부 올라간다. 본문 자인: *"six out of twenty candidates show deviations larger than 0.05 eV/atom from the DFT values"* — 그리고 **0.05 eV/atom 이 DFT–실험 전형 불확도**라고 스스로 쓴다. ⇒ **①단계 문턱(E_hull < 0.025)은 ML 값으로 판정됐고, 그 값이 DFT 로는 절반 이상 문턱을 넘는다.** 챔피언 Li₉P₃OS₁₁ 의 DFT E_hull = **0.034 eV/atom** 으로 **자기 문턱을 초과한다.** ⚠ 그런데 **재선별은 하지 않았다.**

**10-11. 🟠 trade-off 부인이 자기 데이터와 어긋난다 + 산술이 틀렸다.**
§3.4: *"three out of the four candidates exhibited conductivities **within the LGPS range**"* (LGPS 범위 = 1–10 mS/cm). `Fig. 5c` 실제: 2.56 ✓ · 1.24 ✓ · 17.28 ✗(초과) · **0.61 ✗(미달)**. ⇒ **2/4 이지 3/4 이 아니다.** 그리고 ECW 최고군(0.639) 4종 중 **Ga 계 2종이 σ 하위 2·3위**, ECW 2위군(0.606)인 Y 계가 **σ 꼴찌** ⇒ **데이터는 오히려 trade-off 쪽**이다.

**10-12. 🟠 `Fig. 3` 캡션이 두 군데 틀렸다.**
① 캡션: *"HECW, ECW **≥3.0 V**; MECW **1.5–3.0 V**; LECW **<1.5 V**"* — 본문은 **0.4231 / 0.1582 V**, `Table 1` HECW 평균은 **0.474 V**, `Fig. 3b` 의 띠 경계도 **≈0.16·0.42**. **873종 중 ECW ≥ 1.5 V 는 0종**이므로 캡션대로면 전원 LECW 다. ⇒ **캡션 수치 인용 금지.**
② 캡션: *"**Blue, red, and green** bars denote HECW, MECW, and LECW"* — `Fig. 3c` 는 **파랑 세 단계 농담**만 쓴다. 빨강·초록 없음.

**10-13. 🟠 최종 21종에 중복이 있다.**
`Table S3` + `Fig. 4a` 대조: **`Li₉.₅Ge₀.₅P₂.₅S₁₂` 와 `Li₉.₅P₂.₅Ge₀.₅S₁₂` 가 조성·물성 6칸 전부 동일**(−1.266 / 2.471 / 10.139 / 0.433 / 0 / 0.579, DFT E_hull 0.02). 그리고 **`Li₁₀Ge₀.₅P₂Ge₀.₅S₁₂`(= `Fig. 4a` 의 "Li₁₀GeP₂S₁₂ (Ge↔P)")의 물성이 LGPS 와 완전히 동일** — 즉 **LGPS 가 21종 안에 두 번 들어 있다**. ⇒ **파이프라인에 중복 제거가 없다.** 실제 구별되는 조성은 **19종**이고, 그중 **LGPS 초과는 10종**뿐이다.

**10-14. 🟠 재현성 자료가 없다.**
2,550 목록 · 873 결과 · 21종 좌표 · MP 스냅샷 · GPPD 상 집합 · CHGNet 배열 선정 규칙 · AIMD 입력 — **전부 미공개**("upon request"). 코드 0. ⇒ **어떤 수치도 독립 재계산으로 검증할 수 없다.**

---

## 11. 절별 상세 (논문 전체 재구성)

### §1 Introduction — 서사의 뼈대
전동화 → EV 배터리 3요구(에너지밀도·안전·급속충전) → Li 금속 음극(3860 mAh/g)의 덴드라이트/열폭주 → ASSB → 황화물 SSE → **LGPS**(Kamaya 2011 [25]) 의 1–10 mS/cm 는 *"상호연결된 GeS₄·PS₄ 사면체 골격"* 에서 나온다 → **그러나 ECW 가 좁고(~0.58 V) 공기 중 H₂S 를 낸다** → 해법은 코팅과 **도핑**.
도핑 선례로 든 것: **Cl 도핑 Na₇.₇₅SiS₅.₇₅Cl₀.₂₅ ECW 0.427 V** (Na-아지로다이트 통상 0.3 V) [34] · **Sr 치환이 ECW 0.48 → 0.91 V** [36] · **Sn–Se 이원도핑이 σ 1.80 → 2.7~5 mS/cm (53 %↑)** [37] ⚠ 원문에 `"2.7 selen5 mS cm−1"` 이라는 **조판 깨짐**이 있다 (53 % 로 역산하면 **2.75**) · **Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃ (LSiPSCl) > 25 mS/cm** [40 = Kato 2016].
**고엔트로피(다도펀트) 를 명시적으로 기각**하는 문단이 있다 — *"severe configurational disorder, structural instability, and reduced interpretability"* [41–44] ⇒ **이원(dual) 이 "해석 가능한 최대 복잡도" 라는 논리**. 🔑 **이 논리는 우리도 쓸 수 있다** (우리가 한 염 두 도펀트를 고른 이유와 같은 계열).
차별화 주장: 선행 이원도핑(Sn–Se)이 *"각 도펀트 20–40 at% 만"* 봤다면, 본 연구는 **최소·최대 도핑 한계를 정하고 3단계 비율로 나눠 조합 전수**를 본다.

### §2 Methods
- **§2.1 구조**: ICSD-**188887** (Kuhn/Köhler/Lotsch 2013 단결정 XRD [52]) → **CHGNet** 로 완화 (max **10,000 step**, **full cell relaxation** — *"복잡한 도핑 구조의 충분한 에너지 수렴"* 명분).
- **§2.2 도펀트·자리·비율**: 40종 (Li 8 / Ge 19 / P 13 / S 7). 비율 Li {0, 1.5, 3.0} · Ge {0, 0.5, 1.0} · P {0, 0.5} · S {0, 1.0, 2.0}. **전하보정은 Li 가감** — 명시 예시: Ge⁴⁺ → Co³⁺ 시 `Li₁₀GeP₂S₁₂ → Li₁₀.₅Ge₀.₅Co₀.₅P₂S₁₂`.
- **§2.3 ML**: coGN (E_form **132,752** 항목 / E_gap **106,113** 항목, KGCNN `KNNAsymmetricUnitCell`, 24-NN, +10⁻⁹ Å, batch 32, **800 epoch**) · coNGN (G/K **10,987** 항목, `VoronoiAsymmetricUnitCell`, 12-NN, +10⁻⁶ Å, batch 32, 800 epoch). 둘 다 **5-fold CV, 5개 모델 예측 평균**. 황화물 검증 = `Fig. S2`/`Table S2`. G_VRH 최대오차 50종의 공간군 분포 = `Fig. S3` (**Pm-3m, Fm-3m, I4/mmm, Fd-3m, R-3, C2/m 등에 분산 — LGPS 의 P4₂/nmc 는 0건**).
- **§2.4 DFT/AIMD**: §4 표 참조.
- **§2.5 ECW**: GPPD, μ_Li(φ) = μ_Li,0 − eφ, ECW = V_ox − V_red, pymatgen. ⚠ **V_red/V_ox 의 정의가 §2.5 안에서 두 번 서로 다르게 쓰였다** — 앞: *"V_red is the **lowest** voltage at which the material remains stable upon Li insertion … V_ox is the **highest** voltage prior to decomposition"*; 뒤: *"V_red is defined as the **highest** voltage at which the material remains stable during lithium insertion, and V_ox is the **lowest** voltage at which the material remains stable during lithium extraction."* **정의가 뒤집혀 있다.** (결과 해석에는 영향 없음 — 뒤쪽이 표준 정의)

### §3.1 Screening process — 문턱과 근거
| 문턱 | 값 | 저자 근거 |
|---|---|---|
| E_form | < 0 eV/atom | 원소 대비 열역학적 유리 |
| E_hull | < 0.025 eV/atom | *"분해 구동력 최소화"* [79] |
| **E_gap** | **> 2.0 eV** | 전자 누설·자가방전 억제 [80], Li⁺ 전달수 [81]. ⭐ ***"PBE 가 E_gap 을 ~1–2 eV 과소평가하므로 이 문턱은 그 계통편향에 견고하도록 골랐다"*** [82] |
| **G_VRH** | **> 8.4 GPa** | **Monroe–Newman** 기계적 안정성 [83,84] — 덴드라이트 억제 |
| **G/K** | **< 0.7** | Pugh 비 — 취성파괴 회피 연성 [85 = Min 2021, **교신저자 자기인용**] |
| **ECW** | **≥ 0.58 V** | pristine LGPS 값. 비교군: Li₃YCl₆ 0.62–4.21 V · Li₃YBr₆ 0.59–3.15 V · LLZO ~5 V [87,88] |

### §3.2 열역학·밴드갭·탄성
`Fig. 3a` 4분포. 저자 자인 3건: ① **coGN 은 E_hull 에 대해 SOTA 가 아니다** (E_form·E_gap 만) ② ML E_hull 이 **0 쪽으로 쏠린다(over-stabilization)** ③ 상안정성 ML 벤치마크의 전형 F1 ≈ 0.7 [90 = Riebesell *Matbench Discovery*].
**Dopant survival** (`Fig. S4`): 최고 **Ge·Si·Sn (>61 %)** — *"산화수와 이온반경이 Ge⁴⁺ 에 가까워 격자 왜곡이 작다"*. **0 %**: Co·Cr·V (Ge/P자리) · Ni (Li자리) · N (S자리).
자리별 생존자: Ge자리 **Si·Sn·B·Ga** · P자리 **Ge·Si·Sn** · **S자리 Cl·O 압도**.
결론 문장: *"dual-doping strategies involving chemically compatible elements for the Ge site and halogen dopants for the S site represent the most promising approach"*.

### §3.3 ECW
873종을 HECW(132종, ≥0.4231 V) / MECW(195종, 0.1582–0.4231) / LECW(546종, <0.1582) 로 3분.
관찰: **HECW 는 Ge+S 이원도핑이 다수**, **LECW 는 Li 자리 도핑이 다수**. *"Li 이온이 연속 확산경로를 유지하는 역할과 관련될 수 있다 — 부적절한 Li 자리 치환은 전자 불균형이나 구조 왜곡을 부른다."* **Ti·Rb 가 LECW 에 자주 등장.**
`Table 1` 로 그룹 평균 제시 후 **저자 스스로 상관 부재를 인정**: *"ECW is not strongly correlated with other properties."*
최종 문턱 0.58 V → **21종** (`Fig. 4a`). 그중 **10종만 LGPS 초과**.
4종 선정 논리: `Fig. 4b`(ECW–E_gap)에서 **ECW 넓고 gap 큰 파란 점 4개**(Li₉GaP₂Cl₂S₁₀ · Li₉P₃O₂S₁₀ · Li₉P₃S₁₂ · Li₉P₃OS₁₁) → 뒤 셋이 **도펀트 원소가 겹치므로 Li₉P₃OS₁₁ 만** 남기고 → **Li₉GaP₂I₂S₁₀**(높은 G/K) 추가 → **Li₉YP₂Cl₂S₁₀**(ECW 0.606 로 낮지만 G_VRH 최고) 추가.
⚠ **Li₉P₃S₁₂ 는 도펀트가 P 하나뿐**(Ge자리 전부 P) = 사실상 **단일도핑**인데 "이원도핑 후보" 안에 있다 (§10-9 와 연결).

### §3.4 이온전도도
설계 논리: Ge/P 자리는 **강체 골격 보존** → 산화수 유사 원소. S 자리는 **이온반경 차이로 GeS₄/PS₄ 를 약간 왜곡** → 전도 ↑, 기계 ↓ [92,98]. 낮은 산화수 도펀트는 **Li 침입형 + 협동 확산** [61] 과 **paddle-wheel** [100].
결과: **Li₉P₃OS₁₁ 17.28 mS/cm** — *"P 와 O 의 Ge·S 자리 공치환"*. `Fig. 4a` 의 파란 무리가 도펀트를 공유한다는 점에서 **P–O 상관의 중요성** 주장.
기전 (`Fig. S6`): **PS₄ 의 S 일부를 O 가 치환 → PS₂O₂ 형성**. O 의 작은 반경·높은 전기음성도 → **짧고 강한 P–O**, 더 치밀한 다면체 → **대칭 붕괴 + 동적 격자 요동 증가 → Li⁺ 이동 촉진.**
확장 해석: MSD·D 증가는 *"국소 진동이 아니라 빈번한 자리간 hopping"* [101] · 격자 연화가 이동장벽을 낮춘다 [102] · **연화가 균일하지 않고 공간적으로 불균일한 국소환경을 만든다** · 이종 Li 배위환경이 **퍼콜레이션 경로**를 만든다 [103] · 이원도핑이 기계강건성과 이동도를 **협동적으로** 조율한다 [104].
최종 설계 원칙 (conclusion 과 동일): ***"Ge·P 자리에는 산화수 호환 원소로 골격 유지, S 자리에는 저산화수·소반경 음이온으로 확산 기전 활성화."***

### §4 Future directions (저자 자인 한계 — ⭐ 우리 gap 문장 원천)
① **합성 제약 미평가** (도펀트 휘발성·독성·원소 상용성·분위기 제어) ② **Arrhenius 단일기전 가정** — 황화물의 비-Arrhenius 거동 [105 = Winter & Gómez-Bombarelli, *"MLIP 로 LGPS 의 비-Arrhenius 기전을 규명"*] 을 **스스로 인용하면서** 채택 ③ **시뮬레이션 시간·슈퍼셀 크기 의존성 미검토** (*"left for future investigations"*) ④ **계면 미평가** — *"performing interface construction and reaction pathway analysis lies outside the scope of this bulk-focused study"*, MLIP 계면 [107,108] 은 future work.

### §5 Conclusions
2,550 → 21 (ECW ≥ LGPS) → Li₉P₃OS₁₁ 17.28 mS/cm (~2×). PS₂O₂ 기전. **도펀트들이 이미 황화물 SSE 에서 연구된 원소라 실험적으로 접근 가능한 조성공간** [109 = Ito 2022 Li₃PS₄ 액상합성, 110 = **Kim & Martin 2019, Li₁₀SiP₂S₁₂₋ₓOₓ — O 치환 실물 선례**]. 프레임의 일반화 조건 2개 명시: (i) 도핑 자리는 대상 결정화학에 맞춰 재정의, (ii) 타깃 물성·문턱은 용도에 맞춰 조정.

---

## 12. 도펀트 공간 전수 대조 (우리 43 vs 그들 40)

> 우리 쪽 출처: `db/properties/cascade_all_302_2026_08_25.csv` 의 `dopant` 열 **102개 염** → 원소 분해 **43종** (Li 제외). 그들 쪽: 본문 §2.2 + `Fig. 2b`.

**공통 32종** — Ag · Al · As · B · Ba · Br · Ca · **Cl** · Co · Cr · Cu · F · Ga · Ge · I · Mn · Mo · N · Na · Nb · Ni · **O** · Sb · Sc · Si · Sn · Sr · Ti · V · Y · Zn · Zr

**우리에만 10종** — Fe · **Gd** · Hf · In · **La** · Mg · **Nd** · **Sm** · Ta · W
  → 🟢 **란타나이드 4종(Nd·Gd·La·Sm)이 전부 우리 쪽에만 있다.** 이것이 선점 방패의 핵심.

**그들에만 7종** — Rb · Be · C · Pb · Te · **P** · Bi
  → ⚠ **P** 는 우리 host 원소라 "도펀트" 개념이 안 맞지만, 그들은 **P 를 Ge 자리에 넣어 챔피언을 만들었다**(Li₉P₃OS₁₁ = Ge → P). 우리 계에는 대응 조작이 없다(아지로다이트에 Ge 자리가 없다).

**그들의 S자리 7종 vs 우리 음이온 축**: 그들 {Cl, O, I, Br, Se, F, N} / 우리 염이 운반하는 음이온 {O, S, Cl, Br, I, F, N}. ⇒ **거의 동일하다.** 차이는 **Se(그들만)** 하나.

**교차 검증되는 화학** (양쪽에서 같은 방향):
| 원소 | 그들 결과 | 우리 결과 | 일치? |
|---|---|---|---|
| **Cl** | S자리 survival **1위** (≈53.5 %) | Cl-rich modelc 가 D 2.6× ↑, Ea ↓ | ✅ 방향 일치 |
| **O** | S자리 survival **2위** (≈50.5 %), 챔피언 조성 | B₂O₃·Nd₂O₃ 등 산화물 염 중심 축 | ✅ 방향 일치 |
| **Ga** | ECW 최고군 2종(Ga–Cl, Ga–I) V_ox **2.356 V** | **Ga₂O₃ 가 onset 을 2.356 V 로** (cascade funnel) | ✅✅ **같은 숫자** |
| **Sc** | Ge자리 survival ≈49.5 % (중위) | **Sc₂O₃ onset 2.356 V** | ✅ 같은 숫자 |
| **Y** | ECW 0.606 (2위군), **σ 꼴찌 0.61 mS/cm** | **Y₂O₃ onset 2.282 V**, G4 에서 탈락 | ✅✅ **같은 trade-off** |
| **Cr** | Ge·P자리 survival **0 %** | **Cr₂O₃ onset 2.356 V 이나 G4 탈락** | 🟡 다른 축에서 탈락 |
| **N** | S자리 **0 %** ((a)기준) / ≈24.5 % ((b)기준) | Li₃N·AlN·GaN·Ca₃N₂·Mg₃N₂ — **UMA 는 Li₃N 사용 금지 판정** | 🟡 양쪽 다 N 은 문제가 있다 |

---

## 13. "dual-doped" 정의 해부 (요청 1-c 의 정밀 답)

### 그들의 정의 — `Fig. 2c` 9개 템플릿 (정본)

| # | 템플릿 | 자리 조합 | 성격 |
|---|---|---|---|
| 1 | Li₁₀₋ₓ₋y**A**ₓ**A′**yGeP₂S₁₂ | Li + Li | 같은 자리 2원소 (양이온) |
| 2 | Li₁₀₋ₓ**A**ₓGe₁₋y**B**yP₂S₁₂ | Li + Ge | 양이온 + 양이온 |
| 3 | Li₁₀₋ₓ**A**ₓGeP₂₋y**D**yS₁₂ | Li + P | 양이온 + 양이온 |
| 4 | Li₁₀₋ₓ**A**ₓGeP₂**X**yS₁₂₋y | Li + S | **양이온 + 음이온** |
| 5 | Li₁₀Ge₁₋ₓ₋y**B**ₓ**B′**yP₂S₁₂ | Ge + Ge | 같은 자리 2원소 |
| 6 | Li₁₀Ge₁₋ₓ**B**ₓP₂₋y**D**yS₁₂ | Ge + P | 양이온 + 양이온 |
| 7 | Li₁₀Ge₁₋ₓ**B**ₓP₂**X**yS₁₂₋y | Ge + S | **양이온 + 음이온** |
| 8 | Li₁₀GeP₂₋ₓ**D**ₓ**X**yS₁₂₋y | P + S | **양이온 + 음이온** |
| 9 | Li₁₀GeP₂**X**ₓ**X′**yS₁₂₋ₓ₋y | S + S | 같은 자리 2음이온 |

⇒ **"dual" = 치환 사건이 2개**. 양이온쌍·음이온쌍·양음 혼합이 **모두 포함**된다. **P+P 템플릿은 없다.**

### 우리 정의와 어디가 같고 어디가 다른가

| 축 | 그들 | 우리 | 판정 |
|---|---|---|---|
| 양이온+음이온 동시 도핑을 보나 | ✅ 템플릿 4·7·8. 실제 후보에 Zr+O, Zn+O, Mn+F 존재 | ✅ Nd₂O₃, B₂O₃ 등 | 🔴 **겹친다** |
| **전하중성을 어디서 닫나** | **Li 를 가감해서** (Ge⁴⁺→Co³⁺ ⇒ Li₁₀ → **Li₁₀.₅**). 실제 후보 Li 지수가 **4.5 ~ 11.5** 로 움직인다 | **염 내부에서** (Nd₂O₃ 자체가 중성; Li 를 안 건드리는 설계가 기본) | 🟢🟢 **여기가 구별선이다** |
| 그 결과 생기는 교락 | **도펀트 정체 ↔ Li 함량**이 구조적으로 교락. `Fig. 3c` 의 `Li₄.₅Ba₃GeP₁.₅Si₀.₅S₁₂` 는 Li 가 **절반 이하**다 — ECW·σ 차이를 도펀트 탓으로 못 돌린다 | Li 함량 고정(또는 명시 변주) | 🟢 **우리가 낫다** |
| 도펀트 쌍의 "출처" | 개념 없음 — 원소 2개를 독립적으로 배치 | **한 염(precursor)** = 실험 합성 경로와 1:1 | 🟢 **우리가 실험 이식성에서 낫다.** ⚠ 단 그들은 §5 에서 *"조성이 실험적으로 탐색된 공간 안에 있다"* 고 별도 방어한다 |
| 농도 격자 | 자리별 3수준(0/중/최대) | 연속·다수준 | 🟡 비슷 |

**결론**: *"dual-doped"* 라는 **단어는 겹치지만 의미가 다르다.** 그들은 **자리-쌍 조합론**, 우리는 **염-단위 공도핑**. 원고에서는 반드시 ***"salt-level co-doping (charge-balanced within a single precursor)"*** 같은 표현으로 **우리 것을 재명명**해야 혼동을 막는다.

---

## 14. 파이프라인 단계별 대조 (요청 1-d)

| 단계 | [Jung26LGPS] | 우리 cascade | 판정 |
|---|---|---|---|
| **0. 구조 생성** | ICSD XRD → **CHGNet full-cell 완화** (10,000 step) | MP/실험 구조 → UMA 완화 · `enumerate_anion.py` 등 | 🟡 같은 일. **그들은 조성당 배열 수를 안 밝힌다** |
| **1. 열역학** | **ML(coGN)** E_form + E_hull (2,550 → 2,065) | `convex_hull_ehull.py` · `ehull_check.py` — **실DFT/MLIP** | 🟢 **우리가 깊다.** ⚠ 우리 T10: 이 필터가 **우리 풀에선 무력**(탈락 0종). 그들 풀에선 19 % 자른다 — **풀의 성격 차이**(그들은 가상조성, 우리는 흔한 안정 이성분) |
| **2. 전자구조** | **ML(coGN)** E_gap > 2.0 eV (→987, **52 % 탈락 — 두 번째로 센 게이트**) | fixed-occ nscf 고유값 (소수 계만) | 🔴 **그들만 대규모로 한다.** 우리는 gap 을 **게이트로 안 쓴다** — 대신 그들도 **DFT 검증을 한 번도 안 했다**(§10) ⇒ 무승부 |
| **3. 기계** | **ML(coNGN)** G_VRH > 8.4 & G/K < 0.7 (→873, 11.5 %) | `b2o3_dft_eos.py`·elastic C_ij (실DFT) + EOS B₀ | 🟢 **우리가 깊다.** 🔵 **문턱 설계는 배울 것**(Monroe–Newman + Pugh) — 단 vacuous 위험 확인 필요 (§8-③) |
| **4. 이동도 예비** | ⛔ **없다** | **BVSE 채널 %** (`bvse_proxy.py`, softBV R₀ S 2.105 / Cl 2.249 / O 1.466) · `li_mobility_score` | 🟢 **우리만 있다.** 그들은 873 → 21 을 **오직 ECW 로** 자른다 |
| **5. 산화/환원 (ESW)** | **DFT GPPD 873종 전수** → 21 (**97.6 % 탈락**) | `esw_check.py` grand-potential + phase set 명시 | 🟡 **같은 방법.** 🟢 우리는 **상 집합(LiS4/SCl₃/Li₅PS₄Cl₂ 제외)과 kink 전체**를 기록. 🔴 그들은 **873종 전수**로 규모가 크다 |
| **6. anneal / metastability** | ⛔ 없다 | `run_anneal.py` · `rank_anneal.py` · `anneal_delta_E_meV` | 🟢 **우리만** |
| **7. 계면** | ⛔ **없다 (저자 자인)** | T9 5상대 47종 전수 · `run_cathode_interface.py` · `cascade_product_gaps.json` | 🟢🟢 **우리만. 가장 큰 차별점** |
| **8. 대기안정** | ⛔ **없다 (저자 자인)** | T11 pseudo-binary ΔE_H₂S 47종 · `cascade_air_axis_lit_vs_tier.csv` | 🟢🟢 **우리만** |
| **9. 수송 (σ)** | **AIMD 4종**, 700–1300 K × 100 ps × **시드 1** → 300 K 외삽 | **MLIP-MD** UMA-s-1p1, 600/800/1000 K × 200 ps × **3 seed**, 창 2–50 ps | 🟢 **통계는 우리가 낫다** (시드·길이·창 규약). 🟡 힘 계산은 그들이 **ab initio**, 우리는 **MLIP** — **서로 다른 약점** |
| **10. 보고량 규율** | ⛔ 없음. σ 절대값 + 일괄 50 % | **보고량 카드 사전등록** · `decisions.json` · 상대차만 · 인용위험 원장 | 🟢🟢 **우리만.** 이것이 방법론 논문급 차별점 |
| **규모** | **2,550 → 873 → 21 → 4** | 302 (cascade_all) | 🔴 **그들이 8배 넓다** |

**한 줄 요약**: *"그들은 넓고 얕다(ML 3단 + DFT 1단 + AIMD 4종). 우리는 좁고 깊다(전 단계 실계산 + 계면·대기 축 + 보고량 규율)."* 이 대비가 **우리 원고의 positioning 문장**이 된다.

---

## 15. AI/ML 계보에서 이 논문의 자리 (요청 3)

### 모델·데이터·검증 (사실)

| 항목 | 내용 |
|---|---|
| **MLIP (구조)** | **CHGNet** [53, Deng/Ceder 2023] — 전하정보 범용 NNP. **완화 전용**, MD 미사용. 학습셋 = MPtrj(MP 완화 궤적) |
| **대리모형 (물성)** | **coGN / coNGN** [64, Ruff/Reiser/Friederich 2023 arXiv:2302.14102] — 연결성 최적화 (nested) graph network. **Matbench 리더보드 SOTA** (E_form·E_gap·G_VRH·K_VRH) [65] |
| **학습 데이터** | MP: **E_form 132,752** · **E_gap 106,113** · **G/K 10,987** 항목. ⇒ 대리모형의 "큰 데이터"는 **MP 그 자체**이고 이 논문이 만든 라벨은 **0개**다 |
| **검증** | ① Matbench 5-fold CV vs 리더보드 (`Table S1`) ② **황 함유 부분집합 오차** (`Table S2`·`Fig. S2`) ③ G_VRH 최대오차 50종의 공간군 분포 (`Fig. S3`) ④ **E_hull 20종만 DFT 재계산** (`Table S3`) |
| **DFT/AIMD** | 873종 DFT ECW + **4종 AIMD** |
| **공개** | ⛔ 코드 0 · 데이터 0 (요청 시) |

### litdb 계보 안에서의 위치

| 논문 | 무엇을 하나 | [Jung26LGPS] 와의 관계 |
|---|---|---|
| **`[Park26ML]`** `park2026_ml_framework_stable_interfaces_assb` (KIST, *Adv. Sci.* 2026) | MP 총에너지 → pseudo-binary 반응에너지 → 비지도 군집 → **XGB/HGBR 대리모형**으로 코팅재 809/521종 순위 | 🔗 **이 논문을 ref 37 로 인용하는 쪽**. 둘 다 **자체 DFT 없이 대리모형으로 조성공간을 넓힌다**는 점이 같으나, Park 은 **DFT 0 · 실험 0** 이고 Jung 은 **873종 DFT + 4종 AIMD 를 실제로 돌린다** ⇒ **Jung 이 한 층 더 깊다.** 축은 다르다(Park=계면반응, Jung=벌크 ECW+σ) |
| **`[Wu26MLIF]`** `wu2026_ml_driven_electrolyte_interface_design_review` | ML 기반 전해질/계면 설계 리뷰 | 🔗 이 논문이 리뷰가 그리는 **"GNN 대리모형 → DFT 검증" 표준 워크플로의 교과서적 실례**. Jung 은 그 워크플로를 **황화물 도핑에 처음 규모로 적용한 사례**로 인용될 위치 |
| **`[Wang25DPA]`** `wang2025_pretrained_deep_potential_sulfide_sse` | 황화물 SSE 전용 사전학습 DP | 🔀 **대체 경로**. Jung 은 AIMD 4종에서 멈췄는데, DP/MLIP-MD 였다면 **21종 전부**를 돌릴 수 있었다. 저자도 §4 에서 *"Extended AIMD or MLIP-based MD"* 를 future work 로 적는다 ⇒ **Jung 의 한계를 Wang 계열이 메운다** |
| **`[He18]`** `he2018_statistical_variances_diffusional_aimd` | AIMD 확산계수의 통계 분산 정량화 | ⚠ **Jung 의 ref [74] 가 바로 이것인데, 사용법이 어긋난다** — He 의 요지는 *"불확도가 물질·온도마다 다르다"* 인데 Jung 은 **네 온도 평균을 네 물질에 일괄 적용**했다 (§10-3) |
| **`[Jiang22Se]`** `jiang2022_se_doped_lpscl_high_throughput_dft` | **LPSCl** Se 도핑 고속 DFT | 🔗 **가장 가까운 "우리 계 + 고속스크리닝" 선례.** Jung 이 LGPS 에서 한 일의 아지로다이트 판. **우리 원고는 Jiang 과 Jung 을 나란히 인용해 "두 계 모두에서 했다" 는 배경을 만든다** |
| **`[Muy25Dop]`** `muy2025_li7ps6_dopant_engineering_conductivity` | Li₇PS₆ 도펀트 엔지니어링 | 🔗 같은 축(도펀트→σ), 다른 계 |
| **`[Ren26]`** `ren2026_li2zrcl6_low_ion_potential_doping` | Li₂ZrCl₆ 저이온전위 도핑 | 🔗 할라이드 판 |
| `cho2025_multicompositional_argyrodite_experimental_active_learning` (Sohn/Park, 세종대) | 실험 능동학습 아지로다이트 | 🔗 **ref [34] 의 자매 그룹.** coGN/coNGN 이 국내 SSE 스크리닝에서 **두 그룹 이상의 공통 도구**임을 보여준다 |

**계보 판정**: 이 논문은 ***"파운데이션 MLIP(CHGNet)로 구조를 만들고, Matbench-SOTA GNN 대리모형으로 물성을 걸러, DFT/AIMD 로 소수만 마감한다"*** 는 **2024–2026 표준 워크플로의 황화물 도핑판**이다. **새 모델을 만들지 않았고, 새 라벨을 만들지 않았고, 새 벤치마크를 세우지 않았다.** 기여는 **적용 대상(LGPS 이원도핑)과 규모(2,550)** 에 있다.

---

## 16. 우리가 유도한 값 (논문 미보고 — 전부 **(우리 유도, 논문 미보고)**)

1. **ECW 개선폭의 분해**: ΔECW = +0.060 V, 그중 **ΔV_red = 0.000 V (0 %)**, **ΔV_ox = +0.060 V (100 %)**. `Fig. 4a` 21종 전수.
2. **V_ox 가 취하는 값의 개수**: 21종이 **딱 4개 값**만 갖는다 — **2.296 / 2.310 / 2.323 / 2.356 V** (= 0.579/0.593/0.606/0.639 + 1.717). ⇒ **ECW 는 연속 변수가 아니라 4계단 이산 변수**다.
3. **21종의 ECW 분포**: 0.579 **11종**(LGPS 포함, 그중 LGPS 는 **2번 중복**) · 0.593 **4종** · 0.606 **1종** · 0.639 **5종**. ⇒ *"21 candidates"* 의 실질은 **LGPS 초과 10종 / 동률 11종**.
4. **외삽 증폭률**: 챔피언/최하위 D 비 = 700 K **≈1.8배**(figure-read) → 300 K **28.3배**(보고값) ⇒ **≈16배 증폭**. 챔피언/2위 = ≈1.25배 → 6.75배 ⇒ **≈5.4배 증폭**.
5. **Nernst–Einstein 자기정합 검산 (✅ 통과)**: LGPS 통상셀 V ≈ 952 Å³, Li 18개 ⇒ n ≈ 1.89×10²² cm⁻³, σ = 1.17×10⁵ · D [S/cm, D in cm²/s].
   - Li₉P₃OS₁₁: σ 17.28 mS/cm ⇒ **D(300 K) ≈ 1.48×10⁻⁷ cm²/s**. Arrhenius(Ea 209 meV, D(700 K) figure-read 1.5×10⁻⁵)로 독립 환산하면 **1.47×10⁻⁷** ⇒ **0.7 % 일치**.
   - Li₉YP₂Cl₂S₁₀: σ 0.61 mS/cm ⇒ D(300 K) ≈ **5.2×10⁻⁹**; Arrhenius(337 meV, 0.85×10⁻⁵) ⇒ **4.9×10⁻⁹** ⇒ **6 % 일치**.
   ⇒ **Haven = 1 가정 확인**되고, 내 `Fig. 5b` figure-read 도 검증된다.
6. **2,550 의 재구성**: 2,248(교차자리 쌍) + 220(동일자리 쌍) + 81(단일도핑) + 1(pristine) = **2,550 정확 일치**. ⇒ *"2,550 dual-doped"* 중 **82종은 이원도핑이 아니다** (§10-9).
7. **nat 추정**: LGPS 통상셀 Z=2 = **50원자**(20 Li + 2 Ge + 4 P + 24 S, §2.2 의 "20 Li and 24 S" 로부터). Li₉P₃OS₁₁ = **48원자**(18 Li + 6 P + 2 O + 22 S). ⇒ **MSD 통계가 Li 18개 × 100 ps × 1 궤적**.
8. **깔때기 단계별 기여**: ML 3단 합산 탈락 **65.8 %**(2550→873), DFT ECW 1단 탈락 **97.6 %**(873→21). ⇒ **판정력의 거의 전부가 DFT 단계에 있다.**
9. **`Table 2` ↔ `Table S3` 행 오배정 확정**: `Fig. 4b` 의 E_gap 좌표(2.524/2.555/2.626/2.645)가 `Table S3` 와 일치하고 `Table 2` 와 불일치 ⇒ **`Table S3` 채택**.
10. **우리 cascade 와의 숫자 일치**: **V_ox = 2.356 V** 가 그들 최고 후보 5종과 우리 Cr₂O₃/Ga₂O₃/In₂O₃/Sc₂O₃ 에서 동일. **V_red = 1.717 V** 가 그들 21종 전부와 우리 comp1·modelc OCV 에서 동일. ⚠ **phase set 이 다를 수 있으므로 "같은 kink 로 보인다" 까지만.**

---

## 17. 물성 4축(A–D) 편입 판정 (요청 4)

> 원칙: 이 논문은 **물성값이 있다**(σ·Ea·ECW·G·E_gap). 따라서 `🔧 방법 원전` 전용이 아니다. 그러나 **계가 다르고 방법이 갈리는 칸이 있으므로 축별로 따로 판정한다.**

| 축 | 편입? | 조건·근거 |
|---|---|---|
| **A. 이온전도 (σ·Ea·D)** | ⛔ **편입 금지** | 4가지 이유가 겹친다: ① **계가 다르다**(LGPS ≠ 아지로다이트) ② **같은-방법 host 기준값이 없다**(LGPS AIMD σ 미계산) ③ **오차막대가 일괄 스칼라**라 물질을 못 가른다 ④ **300 K 가 외삽**이고 `Fig. 5b` 에서 **실측 온도의 순위가 뒤집힌다**. ⇒ **A축 표에 행을 만들지 않는다.** 대신 `🔧 방법 원전` 블록에 **"외삽 증폭" 경고 사례**로만 둔다 |
| **B. 산화안정 (4축 중 B①)** | ✅ **편입 (조건부)** | **가장 강한 편입 근거**: 같은 **pymatgen 대분배포텐셜**, 같은 μ_Li(φ) 정의, 그리고 **V_red 1.717 V · V_ox 2.356 V 가 우리 값과 글자 그대로 같다.** ⇒ **값 비교가 아니라 *구조* 비교**로 넣는다: (i) **V_red 부동성**, (ii) **onset 축퇴/계단성**, (iii) **개선폭 스케일(수십 mV)**. **조건 3개 명기**: ⓐ 계가 다름, ⓑ **그들 phase set 미기재** ⇒ 40 mV 차이를 물질 비교로 읽지 말 것, ⓒ **축 이름을 반드시 B①(0 K grand-potential onset)로 명명** — B③(닫힌계 양극 접촉)과 섞지 말 것 |
| **C. 기계** | 🟡 **편입 (조건부, 값 비교 아님)** | **양이 다르다**(그들 G_VRH/Pugh, 우리 E_VRH/B₀) + **그들은 ML 예측이고 DFT 검증 0**. ⇒ **수치 행 금지.** 넣는 것은 **문턱 설계 선례**뿐: Monroe–Newman **G > 8.4 GPa**, Pugh **G/K < 0.7**, 그리고 **우리 계에서 vacuous 할 위험**(그들 873종이 0.42–0.7 에 전부 들어옴) |
| **D. 전자구조 (밴드갭)** | 🟡 **편입 (조건부, 값 비교 아님)** | 그들 E_gap 은 **coGN 예측**(MAE 0.16–0.19 eV)이고 **DFT DOS 를 한 번도 안 그렸다**. 우리 규율(fixed-occ nscf 고유값)과 **등급이 다르다**. ⇒ **"둘 다 wide-gap"** 수준 + **문턱 설계 선례**(*"PBE 가 1–2 eV 과소평가하니 문턱을 2.0 eV"*)만. **2.384 / 2.645 eV 를 우리 2.066 / 2.099 eV 와 나란히 쓰지 않는다** |
| **🔧 방법 원전** | ✅ **추가** | (a) **AIMD 300 K 외삽의 위험** 실측 사례 (§10-1·§16-4) (b) **`[He18]` 불확도 전파의 잘못된 사용례** (c) **coGN/coNGN 성능 기준선** (`Table S1`/`S2`) (d) **`Fig. 4a` [V_red,V_ox] 절대구간 막대 양식** (e) **ML E_hull 과대안정화 정량**(`Table S3`) |

**총평**: **B① 에 1행 · C 와 D 에 각 1행(문턱 선례) · A 는 거부 · 🔧 방법 원전 블록 1개.** §J 는 **선점 판정 축**으로 별도 신설 — **§J-30 으로 배정됨** (병합 2026-09-22).

---

## 18. 기법 미니사전

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **coGN** (connectivity-optimized Graph Network) | CGCNN 계열 결정 GNN 을 **비대칭 단위셀(asymmetric unit cell)** 로 다듬어, 대칭 등가 노드를 지워 그래프를 줄인 것. 정확도 유지 + 메모리·속도 이득 | E_form · E_hull(간접) · E_gap 예측. 24-NN |
| **coNGN** (nested Graph Network) | coGN 에 **선그래프(line graph)** 를 겹쳐 **결합각·이면각** 같은 고차 기하를 담는다 | G_VRH · K_VRH 예측. Voronoi 12-NN |
| **Matbench** | 결정 물성 예측 ML 의 표준 벤치마크 + 리더보드 | coGN/coNGN 이 E_form·E_gap·G·K 에서 SOTA 라는 근거 [65] |
| **CHGNet** | **전하 정보를 담은** 범용 MLIP (MPtrj 학습) | 2,550 구조의 **완화**에만 사용 (MD 아님) |
| **E_hull** (energy above hull) | 해당 조성에서 **경쟁 안정상 조합** 대비 초과 에너지. 0 이면 바닥상 | 문턱 **< 0.025 eV/atom**. ⚠ ML 예측이 **0 으로 쏠린다** |
| **G_VRH / K_VRH** | Voigt–Reuss–Hill 평균 **전단(G)·체적(K) 탄성률** — 다결정 등방 평균 | 문턱 G > 8.4 GPa |
| **Pugh 비 (G/K)** | **연성/취성** 지표. 낮을수록 연성 | 문턱 < 0.7 |
| **Monroe–Newman 기준** | 고체전해질의 **전단탄성률이 Li 금속의 ~2배**면 덴드라이트를 기계적으로 억제한다는 선형안정성 해석 | G > 8.4 GPa 의 출처 [83] |
| **GPPD** (grand potential phase diagram) | Li 화학퍼텐셜 μ_Li 를 **전압으로 바꿔** 넣고 그린 상도. 전압을 걸었을 때 어떤 상으로 분해되는지를 본다 | **우리 `esw_check.py` 와 같은 계열**. μ_Li(φ) = μ_Li,0 − eφ |
| **V_red / V_ox / ECW** | 각각 **환원 한계 / 산화 한계 / 그 폭** | 이 논문의 **핵심 반전**: V_red 가 21종 전부 1.717 V 로 고정 |
| **Nernst–Einstein** | D 를 σ 로 바꾸는 관계 σ = n q² D / (k_B T). **Haven 비 H_r = 1 가정** | Haven 언급 0회 ⇒ H_r=1 암묵. **우리 규율과 같은 가정이지만 우리는 절대값 인용을 금지한다** |
| **paddle-wheel** | 다면체 음이온(PS₄ 등)의 **회전**이 Li 이동과 결합해 확산을 돕는 기전 | 기전 서술에서 인용 [100 = Zhang & Nazar] |
| **survival rate** (이 논문 자체 정의) | 어떤 도펀트가 스크리닝 단계를 **살아남는 비율** | ⛔ **분모가 정의돼 있지 않고 두 패널이 안 맞는다** (§10-7) |
| **PS₂O₂** | PS₄ 사면체의 S 2개가 O 로 치환된 국소 단위 | 챔피언의 기전 (`Fig. S6`). ⚠ **단일 배열 가정** |

---

## 19. 후속 확보 목록 (우선순위)

1. 🔴 **Kim K-H, Martin S W**, *"Structures and properties of oxygen-substituted Li₁₀SiP₂S₁₂₋ₓOₓ solid-state electrolytes"*, *Chem. Mater.* **31**, 3984 (2019) — **ref [110]**. **황화물 SSE 의 O 치환 실험 선례**. 우리 O 도핑 서사의 **실험 선행연구**가 될 가능성이 가장 높다. **최우선.**
2. 🔴 **Do Lee B, Gavali D S, … Park W B, Sohn K-S**, *"Discovering virtual Na-based argyrodites as solid-state electrolytes using DFT, AIMD, and machine learning"*, *JMCA* **13**, 10462 (2025) — **ref [34]**. **같은 coGN/coNGN 을 아지로다이트에 적용한 편** ⇒ **우리 계에 대한 선점 위험이 이 논문보다 높다.** 확보 필수.
3. 🟠 **Park T, Kim J, Jung Y, Sun J, Min K**, *J. Energy Chem.* **107**, 103 (2025) — **ref [51]**, **같은 저자들의 직전 작업**. 2,550 숫자의 출처 확인 + 이 그룹의 파이프라인 계보 파악.
4. 🟠 **Choi Y, Jeong J, … Scanlon D O, Chung K Y, Lee J**, *"Li-ion transport mechanisms in **Ge/Cl dual-doped** Li₁₀GeP₂S₁₂"*, *Carbon Energy* **6** (2024) — **ref [61]**. **제목에 "dual-doped" 가 있는 실험+MLIP 편.** Jung 보다 먼저 나온 이원도핑 LGPS 이므로 **"dual-doping" 용어의 선행 정의**를 확인해야 한다.
5. 🟠 **Winter G, Gómez-Bombarelli R**, *"Simulations with machine learning potentials identify the ion conduction mechanism mediating **non-Arrhenius** behavior in LGPS"*, *J. Phys. Energy* **5**, 024004 (2023) — **ref [105]**. Jung 이 **자기 Arrhenius 가정의 반례로 인용**한 편. 우리 외삽 비판(§10-1)의 정본이 될 수 있다.
6. 🟡 **Zhang Y, Luo J-D, Yao H-B, Jiang B**, *"Size dependent lithium-ion conductivity of solid electrolytes in machine learning molecular dynamics"*, *Artif. Intell. Chem.* **2**, 100051 (2024) — **ref [106]**. **슈퍼셀 크기 의존성** — 그들이 미검토라고 자인한 축. 우리 nat 120 vs 그들 ~50 의 의미를 판정할 자료.
7. 🟡 **Ruff R, Reiser P, Stühmer J, Friederich P**, arXiv:2302.14102 — **ref [64]**, coGN/coNGN 원전. 우리가 대리모형을 도입한다면 1차 자료.
8. 🟡 **Min K**, *J. Electrochem. Soc.* **168**, 030541 (2021) — **ref [85]**, 교신저자 자기인용. **Pugh 0.7 문턱의 출처**. 우리가 그 문턱을 쓰려면 근거를 봐야 한다.

---

## 20. 한 줄 마감

> 이 논문은 **우리를 선점하지 않았다 — 계도 다르고 Nd 도 없다.** 그러나 ***"황화물 SSE 이원도핑을 AI 로 훑는다"*** 는 프레임과 ***"음이온 자리 최적은 Cl 과 O"*** 라는 결론은 **가져갔다.** 우리가 지켜야 할 것은 **구조족(아지로다이트) · 란타나이드 축 · 염 내부 전하중성 · 계면/대기 축 · 보고량 규율** 다섯이고, 다행히 그 다섯은 **이 논문이 하나도 건드리지 않았다.** 그리고 이 논문이 자기 `Fig. 4a` 에서 **V_red 를 한 칸도 못 움직였다**는 사실은, 우리 §B 서사에 **공짜로 얻은 가장 좋은 한 줄**이다.
