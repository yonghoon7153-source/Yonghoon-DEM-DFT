---
title: "Lee (Jieun) et al. 2025 — Halide segregation to boost all-solid-state lithium-chalcogen batteries (Science 388, 724)"
description: "2000 rpm 초고속 혼합 중 LPSCl 에서 Cl 이 기계화학적으로 빠져나와 활물질 표면에 나노 LiCl 층으로 쌓인다는 Argonne 논문 — 밀링을 '분산' 이 아니라 '계면 합성' 으로 재정의하고, 혼합 속도·시간 스캔과 무밀링·가열전용 대조군을 처음으로 다 갖췄다. 활물질은 S8/Se/SeS2/Te 이고 Li2S 양극은 없다. 주의, KIST Lee 의 lee2026 과 다른 Lee 다"
source_url: local-upload/757a00b0-3._halide_segregation_to_boost_all_solid_state_lithium_chalcogen_batteries.pdf
doi: 10.1126/science.adt1882
ingested: 2026-10-02
sha256: 7061e771a497736dc33bf2a56053c1a23c0d64bd2c58612a19f526be0314526d
tags: [assb, sulfide-electrolyte, composite-cathode, mixing-process, carbon, li-in, units]
compare:
  system: "ASSB Li–chalcogen. 활물질 4종 — S8 · Se · SeS2 · Te. **Li2S 양극은 없다** (Li2S 는 XANES 기준물질과 방전 생성물로만 등장). 음극 Li–In 표준(+ Li 금속 fig. S38), 상온 ~25 °C, 운전 스택압 ~70 MPa"
  electrolyte: "할로겐 함유 SE 5종 — Li6PS5Cl(LPSCl, 표준) · Li6PS5Br · Li6PS5Cl0.5Br0.5 · `[인쇄]` Li6PSCl0.9I0.1(LPSClI, 아래첨자 5 누락 오기로 읽힌다) + 할로겐 없는 대조 2종 Li10GeP2S12 · SS7(정의 없음). `[인쇄]` fig. S42 에서 모두 '비슷한 이온전도도'(값 미기재, SI 미확보)"
  cathode: "조성비(활물질:SE:탄소) **본문에 없음** — SI 미확보. 유일한 단서는 `[인쇄]` '황 함량을 32.5 wt % 까지 더 올려도'(fig. S39) 라는 문장으로, 표준 조성의 S wt% 는 32.5 미만이라는 것만 알 수 있다. 바인더 유무·전극 두께·성형압 전부 미기재"
  li2s_source: "해당 없음 — 출발 활물질이 S8/Se/SeS2/Te 이다. 황은 `[인쇄]` 'raw sulfur' 로만 기술되고 입도·순도·제조사 미기재"
  mixing: "★ **one-step UHS(ultrahigh-speed) 혼합 — 생황·LPSCl·도전탄소를 한 번에 2000 rpm 5 h.** 본문 전체에서 'ball'·'mill' 이라는 단어가 한 번도 안 나온다(장비 종류 불명). 스캔: 속도 400 vs 2000 rpm, 시간 1 / 5 / 10 h. 대조: 손혼합(무밀링), 손혼합 + 145 °C 3 h 가열. **BPR·볼 재질/지름/개수·용기 부피·투입 질량·분위기·휴지 주기 전량 미기재**(Materials and Methods 가 통째로 SI, SI 미확보)"
  loading_mg_cm2: "4 (활물질 기준, 표준 — S·Se·SeS2·Te 모두) · 2 (장수명 450사이클용 S)"
  li2s_wt_pct: ""
  anode: "Li–In (표준, 전압 전부 vs Li–In). Li 금속 셀도 있으나 fig. S38(SI 미확보). N/P·Li 재고 미기재. anode-free 아님"
  first_charge: "해당 없음 — 셀이 충전상태(S8/Se/SeS2/Te)에서 시작해 첫 스텝이 방전이다. Li2S 첫 충전 활성화는 이 논문에 없다. `[도표, Fig. 3B]` 전압창 ≈0.4–2.3 V vs Li–In (인쇄된 컷오프 수치 없음)"
  first_discharge_mAh_gS: "1570 — `[재현]` 인쇄값 6.28 mAh cm⁻² ÷ 4 mg cm⁻². 다른 셀 `[인쇄]` 6.35 → 1587.5. 2 mg 셀은 `[재현]` ≈1609(3.00 ÷ 0.932 ÷ 2). 2전자 기준 93.9 % / 94.9 % / 96.3 %"
  first_discharge_mAh_gLi2S: "1095.6 · 1107.8 · 1123.2 — `[재현]` 위 값 ×0.69783 (가상 Li2S 분모 환산. 이 셀의 실제 활물질은 S8 이다)"
  cycle_capacity_mAh_gS: "100사이클 1552.5 (`[인쇄]` 6.21 mAh cm⁻² @4 mg) · 450사이클 1500 (`[인쇄]` 3.00 @2 mg) · 450사이클 1250 (`[도표]` ≈5.0 @4 mg, 1.4 mA cm⁻²). ★ `[도표, Fig. 3A]` 5 h 시료의 **최고점은 30–40사이클의 ≈7.85 mAh cm⁻² = 1962 mAh g⁻¹(S) = 2전자 이론의 117 %** 로, 인쇄된 '초기 6.28' 과 '98.9 % 유지' 는 그 봉우리를 건너뛴 양끝 비교다"
  cycle_capacity_mAh_gLi2S: "1083.4 · 1046.7 · 872.3 · (최고점) 1369.5 — `[재현]` ×0.69783"
  areal_mAh_cm2: "6.28 → 6.21 (100사이클, 98.9 %) @4 mg·0.67 mA cm⁻² · 3.00 (450사이클, 93.2 %) @2 mg·0.67 · 6.35 → `[도표]` ≈5.0 (450사이클, 80 %) @4 mg·1.4 · `[인쇄]` 다른 칼코겐 3–5 · `[도표]` Se 3.7→3.5 · Te 3.0→3.1 · SeS2 4.9→3.9 (100사이클) · `[도표]` LPSClI 최고 ≈7.8 · 할로겐 없는 LGPS/SS7 는 2사이클째부터 ≈1.1"
  cycles: "100 (혼합시간 비교·칼코겐 4종) · 450 (S 장수명 2종) · 50 (SE 5+2종 비교)"
  temperature_C: "25 (전부 상온 — 저자들이 60 °C 문헌과 대비해 강조하는 지점)"
  mechanism: "★ **UHS 혼합의 기계화학 반응으로 할로겐이 SE 에서 분리돼 활물질 표면에 나노 Li halide 층으로 증착된다.** 구동력은 마찰 국부발열(heat striking) + 전단(shear fracturing); 전단은 입자 미세화·균질화만 담당. 증거: cryo-TEM HAADF/EDS 로 Cl/P 가 표면에서 1.0 → 2.45–3.55 (S 계), Br/P 1.78–4.56 (Se/LPSBr 계); EELS 로 Cl-rich = P-deficient = Li-Cl, Cl-deficient = P-rich = Li-P-S; HRTEM+FFT 로 입방 Fm-3m LiCl (d 2.95/2.53 Å) 이 육방 Se 위에 결정상으로 확인; in situ 승온 SXRD 에서 LiCl (111)·(200) 출현과 LPSCl 피크 감소. ★ 황 없이 LPSCl+탄소만 가열해도 같은 LiCl 이 나온다(fig. S14) — 황과의 반응이 아니다. 효과: 복합양극 Li⁺ 확산계수 400 rpm 대비 **196배**(fig. S36, 방법·절대값 미기재) — 단 **벌크 LPSCl 자신의 이온전도도는 UHS 시간에 따라 떨어진다**(수치 미기재). 10 h 는 LPSCl 결정구조 붕괴로 성능이 꺾인다 → 5 h 가 계면 이득과 벌크 손실의 최적점"
  our_axis: "★★ 혼합 공정 축의 정면. 이 위키 24편 중 **속도 스캔(400/2000) + 시간 스캔(1/5/10 h) + 무밀링 대조 + 가열전용 대조**를 모두 갖춘 유일한 논문이고, '밀링이 SE 를 바꾼다' 를 **열화가 아니라 설계 수단**으로 뒤집어 읽는다. H2b 는 부호가 뒤집히지 않고 **둘로 분리된다** — 벌크 SE σ 는 내려가고(H2b For) 복합양극 유효 수송은 올라간다(H2b Against). 이식 불가: Li2S 양극 없음(첫 충전 활성화 무관), anode-free 아님, 2000 rpm 장비 미상, 조성비·BPR·분위기 미기재로 **재현 불가**"
---

# 수집 목적

Jieun Lee, Shiyuan Zhou, Victoria C. Ferrari, Chen Zhao, Angela Sun, Sarah Nicholas, Yuzi Liu,
Chengjun Sun, Dominik Wierzbicki, Dilworth Y. Parkinson, Jianming Bai, Wenqian Xu, Yonghua Du,
**Khalil Amine**, **Gui-Liang Xu**,
**"Halide segregation to boost all-solid-state lithium-chalcogen batteries"**,
*Science* **388** (2025) 724–729 (6748호, 15 May 2025), DOI **10.1126/science.adt1882**
(submitted 2024-09-16 / accepted 2025-03-25) 의 **절별 해체분석**.

> [!warning] ⚠ 동명이인 구분 — 이 위키에는 Lee 논문이 둘이다
>
> | | **이 파일 `leej2025_…`** | **`lee2026_decoupled-sulfur-redox-pathways-initial-chemical-states-assb.md`** |
> |---|---|---|
> | 제1저자 | **Jieun Lee** (Argonne National Laboratory, 현 주소 KIST) | **다른 Lee** (KIST) |
> | 교신 | **Khalil Amine · Gui-Liang Xu** (Argonne + U. Chicago) | KIST 그룹 |
> | 지면 | ***Science* 388 (2025) 724** | ***Chem. Eng. J.* 546 (2026) 179625** |
> | 주제 | **UHS 혼합 중 할로겐 분리 → 계면 LiCl 층** | **출발 화학상태(S8 ↔ Li2S)가 가르는 산화환원 경로** |
> | 활물질 | S8 · Se · SeS2 · Te (**Li2S 없음**) | **S8 와 Li2S 를 나란히 비교** |
> | SE | LPSCl · LPSBr · LPSClBr · LPSClI (+ LGPS·SS7 대조) | LPSCl 자체합성 |
> | 핵심 수 | 2000 rpm 5 h, Cl/P 1.0 → 3.55, 6.28 mAh cm⁻² | 30:20:50 조성, 단쇄 S2–4 |
>
> 둘은 **서로 다른 논문이고 다른 사람**이다. 인용할 때 반드시 slug 로 구분한다 — "Lee 2025/2026"
> 이라고만 쓰면 안 된다. (앞서 Kim 셋 · Wang 넷 · Zhang 둘을 같은 방식으로 갈라 두었다.)
>
> 참고로 **Jieun Lee 의 현 소속이 KIST** 다(각주 ‡ Present address). 그래서 "KIST Lee" 라는
> 호칭으로도 두 논문을 구분할 수 없다. 반드시 slug 를 쓴다.

## 왜 이 논문을 흡수하는가

이 위키의 **혼합 공정 축**([[composite-cathode-mixing-routes]] · [[one-step-vs-two-step-mixing]] ·
[[mixing-equipment-ball-mill-thinky]]) 을 지금까지 들어온 어떤 논문보다 **정면으로** 건드린다.
초록 첫 문장이 이 위키가 2026-09~10 에 걸쳐 23편의 digest 에서 귀납한 것과 같은 말을 한다:

> `[인쇄]` "Mixing electroactive materials, solid-state electrolytes, and conductive carbon to
> fabricate composite electrodes is **the most practiced but least understood process** in
> all-solid-state batteries, which strongly dictates interfacial stability and charge transport."

그리고 그 "이해되지 않은" 부분으로 **기계화학 반응**을 지목한다 — 초고속 혼합 중 SE 자신의
할로겐이 떨어져 나와 활물질 표면에 **나노 Li halide 층**으로 쌓인다는 것이다.

이 위키가 이 논문에 묻는 세 가지:

1. **우리가 세워 둔 여섯째 경로 "반응성 밀링(in-situ 치환)" 의 지위가 바뀌는가.**
   `hao2025`(Li2S + FeCl3 → LiFeS2 + 3LiCl) 와 `feng2026`(Li2S + FeCl3 몰비 0.1) 은 **첨가제를 넣어
   밀링 중에 반응시킨** 사례였다. 이 논문은 **첨가제 없이 SE 자신이 분해된다**고 말한다.
2. **H2b 의 부호가 뒤집히는가.** [[reference-cell-500-600-mahg]] 의 H2b 는 *"밀링을 겪은 SE 가
   아직 superionic 인가"* 다. 이 논문은 같은 현상을 **열화가 아니라 이득**이라 부른다.
3. **"가장 많이 쓰지만 가장 이해되지 않은 공정" 이라고 선언한 논문이 자기 혼합 조건을 다 적었는가.**
   — 이 digest 의 하이라이트는 §2 다. 답부터 적으면 **아니다.**

## 표기 규칙

`[인쇄]` 원문 글자 그대로 · `[도표]` 그림에서 읽은 근사값 · `[해석]` 우리 판단 ·
`[재현]` 원문 값의 산술 환산(식 병기).

단위 규율: 비용량은 `mAh g⁻¹(S)` / `(Li2S)` 를 병기한다. 환산 **(Li2S) = (S) × 0.69783**
(= M(S)/M(Li2S) = 32.06/45.942). 2전자 천장 **1672 (S) / 1166 (Li2S)**, 1전자 천장 **836 / 583**.
★ **활물질이 Se·SeS2·Te 인 셀의 수치는 (S)/(Li2S) 로 환산하지 않는다 — 분모가 Se/SeS2/Te 다.**
전압은 전부 `vs Li–In` 이고 **이 위키에는 Li–In 오프셋의 근거 raw 가 없으므로 vs Li/Li⁺ 로
환산하지 않는다.**

# 원문에 없어서 확인이 필요한 것 (공백표)

★ 이 논문은 **본문 7쪽(실질 6쪽) 짜리 Science Research Article 이고 Materials and Methods 가
통째로 SI 에 있다.** 그리고 **SI 를 확보하지 못했다**(inbox 에 본문 PDF 만 있다). 아래 공백은
"저자가 안 적었다" 와 "SI 에 있는데 우리가 못 봤다" 가 섞여 있다 — 두 가지를 구분해 적는다.
SI 는 `science.org/doi/10.1126/science.adt1882` 의 Figs. S1–S50, Tables S1–S6, Movies S1–S2 다.

| # | 공백 | 왜 중요한가 | 상태 |
|---|---|---|---|
| **G1** | ★★ **혼합 장비가 무엇인가.** 본문 전체에 `ball`·`mill`·`milling` 이라는 단어가 **한 번도 안 나온다**(Fig. 2 캡션의 "balls" 는 원자 모형 구슬이다). "ultrahigh-speed mixing", "UHS mixing", "2000 rpm" 뿐이다 | 2000 rpm 은 **유성볼밀의 전형 범위를 크게 넘는다**(이 위키 23편 최고가 `zhang2026` 의 1400 rpm). 볼밀인지, 비드밀인지, 고속 전단 믹서(Thinky·rotor–stator)인지에 따라 에너지 전달 기전이 다르고 우리 장비로 옮길 수 있는지도 갈린다 | **SI 미확보** |
| **G2** | ★★ **BPR · 볼 재질/지름/개수 · 용기 재질/부피 · 1회 투입 질량** | 이 위키의 ball milling 전수표에서 BPR 을 적은 논문이 23편 중 4편뿐이다. 2000 rpm 은 BPR 없이는 **아무 의미도 복원할 수 없다** | **SI 미확보** |
| **G3** | ★ **혼합 분위기**(Ar/글로브박스/밀폐 여부)와 **휴지 주기**(5 h 연속인가 on/off 인가) | 기전이 "마찰 국부발열" 이라면 휴지 주기가 곧 온도 이력이다. 5 h 연속 2000 rpm 이면 벌크 온도도 상당할 것이다 | **SI 미확보** |
| **G4** | ★★ **복합양극 조성비**(활물질:SE:탄소 wt%) | 본문의 유일한 단서는 `[인쇄]` "with a further increase of sulfur content to 32.5 wt %"(fig. S39) 뿐이다 → 표준 조성의 S 는 **32.5 wt% 미만**이라는 하한만 알 수 있다. **분모를 모르면 mAh g⁻¹(composite) 도, 이론 초과분의 SE 기여 회계도 못 한다** | **SI 미확보** |
| **G5** | **탄소의 종류와 함량**("conductive carbon" 이라고만 쓴다) | fig. S18 에서 `[인쇄]` "microstructures of carbon additives" 가 할로겐 분리를 촉진하는 데 관여한다고 말해 놓고 본문에 종류를 안 적었다. ref 39(Ohno/Zeier)는 **탄소가 황화물 SE 분해를 가속**한다고 한 논문이다 → 탄소 종류가 기전의 일부일 수 있다 | **SI 미확보** |
| **G6** | ★ **성형(펠릿) 압력** — 운전 스택압 ~70 MPa 는 인쇄돼 있으나 **양극·SE 층을 찍은 압력은 본문에 없다** | 이 위키는 두 압력을 반드시 분리해 적는다 (`gao2024` 성형 490 / 운전 50 MPa) | **SI 미확보** |
| **G7** | **셀 형식·면적·SE 분리막 두께·총 셀 질량** | `[인쇄]` fig. S2 에서 "thin SSEs" 로 에너지밀도를 투사한다면서 자기 셀의 SE 두께를 본문에 안 적었다 | **SI 미확보** |
| **G8** | ★★ **Li⁺ 확산계수 196배의 측정법과 절대값** (fig. S36) | 본문은 `[인쇄]` "an increase 196 times greater than that of the 400-rpm cathode" 라고만 쓴다. **GITT 인지 CV 인지 EIS 인지, 분모(400 rpm 시료)의 절대값이 얼마인지 전혀 없다.** 196배라는 수는 분모가 비정상적으로 작으면 쉽게 나온다 | **SI 미확보** |
| **G9** | ★★ **벌크 LPSCl 이온전도도의 실제 수치** — `[인쇄]` "the ionic conductivity of bulk LPSCl SSEs decreased along with the time of UHS mixing" 에 **숫자가 하나도 없다** | 이 문장이 H2b 의 핵심 증거인데 값이 없다. 1 h / 5 h / 10 h 각각 얼마인가 | **SI 미확보** |
| **G10** | ★★ **부피변화 억제의 정량값** — 스택압 측정(fig. S37)도 µ-CT(fig. S50)도 본문에는 **형용사만** 있다("minimum pressure loss", "minimal electrode expansion") | 이 위키의 좌표는 숫자다 (Qu 2025 14–20 µm · Cronk −42 % · Jeong +46.6 %). **ΔV % 도 µm 도 MPa 도 없다** | **SI 미확보** |
| **G11** | **SE 의 할로겐 소모율** — LPSCl 중 몇 %가 LiCl 로 바뀌었는가 | Cl/P 비는 **표면 농축비**이지 전환율이 아니다. 전환율이 없으면 무게 대가도 SE 손실도 회계가 안 된다 (→ §7) | **원문에 없다** (SXRD Rietveld 결과는 tables S2–S5, SI 미확보) |
| **G12** | **LiCl 층의 두께** | Fig. 2D EELS 맵과 Fig. 2F HRTEM 에서 `[도표]` 10–20 nm 급으로 보이지만 **인쇄된 두께 수치가 없다**. Fig. 1D 라인스캔의 Cl-rich 폭은 ≈0.2–0.4 µm 로 자릿수가 다르다(투영 효과 가능) | **원문에 없다** |
| **G13** | ★ **셀 개수 n 과 오차막대** | 본문·그림 어디에도 n 표기, 오차막대, 재현 셀 언급이 **없다**. Fig. 2C·4I 의 "three different regions" 는 **셀이 아니라 한 입자 안의 영역**이다. *Science* 급에서도 이 위키 23편과 같다 | **원문에 없다** |
| **G14** | **"SS7" 이 무엇인가** | Fig. 3F 의 할로겐 없는 대조 SE 인데 본문 어디에도 정의가 없다 | **원문에 없다** (SI 가능) |
| **G15** | `[인쇄]` **"Li6PSCl0.9I0.1(LPSClI)"** — S 아래첨자 5 가 빠져 있다 | 조성식 오기로 읽히지만 원문 글자가 그러하므로 그대로 기록한다 | **원문 오기** |
| **G16** | **Fig. 4B 의 전압축 기준전극** — 3/2/1 V 눈금이고 Fig. 3B(vs Li–In, 0.4–2.3 V)와 범위가 다르다 | in situ Se XANES 셀이 다른 음극인지 다른 기준인지 불명 | **원문에 없다** |
| **G17** | **첫 사이클 CE** | `[도표, Fig. 3A]` 1 h 시료 쪽에 첫 사이클로 보이는 빈 원이 우축 ≈39 % 에 하나 찍혀 있고 ≈93 % 에도 하나 있다. 본문에 CE 수치가 **한 번도 안 나온다** | **원문에 없다** |

## 0. 서지사항

| 항목 | 값 |
|---|---|
| 제목 | Halide segregation to boost all-solid-state lithium-chalcogen batteries |
| 저자 | Jieun Lee†‡, Shiyuan Zhou†, Victoria C. Ferrari, Chen Zhao, Angela Sun, Sarah Nicholas, Yuzi Liu, Chengjun Sun, Dominik Wierzbicki, Dilworth Y. Parkinson, Jianming Bai, Wenqian Xu, Yonghua Du, Khalil Amine*, Gui-Liang Xu* (†공동 1저자, *교신) |
| 소속 | 1 Chemical Sciences and Engineering Division, **Argonne National Laboratory** · 2 NSLS-II, **Brookhaven** · 3 Center for Nanoscale Materials, Argonne · 4 X-ray Science Division, Argonne · 5 **Advanced Light Source, LBNL** · 6 Pritzker School of Molecular Engineering, **University of Chicago**. ‡ Jieun Lee 현 주소 **KIST** Energy Storage Research Center |
| 지면 | *Science* **388**, 6748호, 724–729 (2025-05-15) |
| DOI | 10.1126/science.adt1882 |
| 투고/수리 | 2024-09-16 submitted / 2025-03-25 accepted |
| 자금 | **DOE Vehicle Technologies Office** (Argonne). 빔라인: APS, NSLS-II 28-ID-2·8-BM·8-ID, ALS 8.3.2(µ-CT) |
| 이해상충 | `[인쇄]` G.-L.X., J.L., K.A. 가 **2024-02-13 미국 비가출원 특허 18/440,838** 을 이 연구로 출원했다 |
| 보충자료 | Figs. S1–S50, Tables S1–S6, References 43–68, Movies S1–S2 — **전량 미확보** |
| 분량 | 본문 6쪽 + 표지 1쪽, 본문 그림 4개 |

## 1. 한 문단 요약

생황(또는 Se/SeS2/Te)·Li6PS5Cl·도전탄소를 **2000 rpm 으로 5시간** 한 번에 섞으면, 마찰 국부발열과
전단이 함께 작용해 **LPSCl 에서 Cl 이 떨어져 나와(기계화학 반응) 활물질 입자 표면에 나노결정질
LiCl 층으로 증착된다**. cryo-TEM(HAADF/EDS/EELS/HRTEM)·싱크로트론 XRD/PDF/XANES·µ-CT 로
이것을 보였고, Cl 뿐 아니라 Br 에서도, S 뿐 아니라 Se·SeS2·Te 에서도 같은 일이 일어난다
("universal"). 이 계면 LiCl 층 덕에 복합양극의 **유효 Li⁺ 수송이 올라가고(400 rpm 대비 확산계수
196배)** 부피변화가 억제돼, 상온 25 °C·스택압 ~70 MPa·활물질 로딩 4 mg cm⁻² 에서 첫 방전
**6.28 mAh cm⁻² = `[재현]` 1570 mAh g⁻¹(S) = 1095.6 mAh g⁻¹(Li2S)**(2전자 이론의 93.9 %,
1전자 기준 187.8 %)를 내고 100사이클 98.9 %, 2 mg cm⁻² 에서 450사이클 93.2 %를 유지했다.
할로겐 **없는** SE(LGPS·SS7)로 바꾸면 2사이클째부터 `[도표]` ≈1.1 mAh cm⁻²(275 mAh g⁻¹(S))로
무너진다. 단 **활물질이 Li2S 가 아니라 S8 계열이어서 Li2S 첫 충전 활성화는 이 논문에 없고**,
혼합 조건은 rpm 과 시간 두 개만 본문에 있다.

## 2. ★★ 혼합 조건 전량 — "가장 이해되지 않은 공정" 이라고 선언한 논문이 자기 조건을 적었는가

이 digest 의 하이라이트다. 본문 전체에서 혼합에 관해 **인쇄된 글자를 하나도 빠짐없이** 옮긴다.

### 2.1 본문에 인쇄된 혼합 서술 전문 `[인쇄]`

> "We prepared the optimal composite sulfur cathode by **one-step UHS mixing of raw sulfur, LPSCl,
> and conductive carbon at 2000 rpm for 5 hours**."

> "…a universal halide segregation at interfaces across a series of halogen-containing SSEs and a
> family of high-energy chalcogen (S, Se, SeS2, Te) cathodes enabled by **an ultrahigh mixing speed
> of 2000 rpm**. The synergistic effects of **heat striking and shear fracturing** by the ultrahigh
> speed (UHS) mixing make it feasible to induce mechanochemical reaction…"

> "…no Cl segregation was observed when **lowering the mixing time to 1 hour** (fig. S5) or
> **reducing the mixing speed to 400 rpm** (fig. S6)."

> "The frictional forces between particles **generated localized heat** sufficient to promote the Cl
> segregation, whereas **shear forces contributed to particle size reduction and homogeneous mixing** (34)."

> (Fig. 1E 캡션) "…**hand-mixed** S/LPSCl/C cathode, and hand-mixed S/LPSCl/C cathode after
> **heating at 145 °C for 3 hours**."

> (Fig. 1G 캡션) "In situ SXRD patterns of the hand-mixed S/LPSCl/C cathode during heating from
> **40° to 400 °C with a heating ramp rate of 10 °C min⁻¹**."

> "…with a further increase of **sulfur content to 32.5 wt %** (fig. S39)…"

**이것이 전부다.** 혼합 조건 기재 항목은 **속도(2000 / 400 rpm)와 시간(1 / 5 / 10 h) 두 개**뿐이다.

### 2.2 기재/미기재 체크리스트

| 항목 | 이 논문 | 비고 |
|---|---|---|
| 혼합 **방식**(one-step/two-step) | ✅ **one-step** — 생황·LPSCl·탄소를 한 번에 | 이 위키 24편 중 one-step 은 6편째 |
| **속도** | ✅ **2000 rpm** (+대조 400 rpm) | 이 위키 최고속 — 종전 최고는 `zhang2026` 1400 rpm |
| **시간** | ✅ **5 h** (+스캔 1 h, 10 h) | 시간 스캔을 세 점으로 돌린 논문은 `wangd2025`(6/10/20 h) 에 이어 2편째 |
| **장비 종류/모델** | ❌ **없다 — "ball"·"mill" 이라는 단어조차 본문에 없다** | G1. 이 위키 24편 중 장비를 안 적은 10편째 |
| **BPR** | ❌ 없다 | G2. BPR 기재는 여전히 23편 중 4편(cronk 1:30 · jeong 50:1 · zhang ≈30:1 · gao 20:1) |
| **볼 재질/지름/개수** | ❌ 없다 | G2 |
| **용기 재질/부피** | ❌ 없다 | G2 |
| **1회 투입 질량** | ❌ 없다 | G2 |
| **분위기** | ❌ 없다 — Ar 인지 글로브박스인지 밀폐인지 한 글자도 없다 | G3 |
| **휴지 주기** | ❌ 없다 — "5 hours" 가 벽시계인지 순 가동인지 불명 | G3 |
| **온도(혼합 중)** | ❌ 측정값 없다. 기전이 "국부 발열" 인데 **온도를 재지 않았다**. 대신 **대리 실험**(hand-mix + 145 °C 3 h, in situ 승온 SXRD 40→400 °C)으로 간접 재현했다 | 아래 2.4 |
| **조성비** | ❌ 없다 (32.5 wt% 상한 단서만) | G4 |
| **탄소 종류** | ❌ "conductive carbon" | G5 |
| **밀링 후 XRD 상 확인** | ✅✅ **했다** — SXRD + Rietveld(tables S2–S5) + x-ray PDF + Raman(fig. S19) + XPS(figs. S20–S22) | ★ 이 위키의 "밀링 후 어떤 상이 생겼나" 칸을 **가장 충실히 채운 논문**이다 |

### 2.3 ★ 판정 — 선언과 기재의 괴리

`[해석]` **"가장 많이 쓰지만 가장 이해되지 않은 공정" 이라고 자기 초록에 쓴 논문이, 그 공정을
속도와 시간 두 숫자로만 기술했다.** 이것은 이 위키가 23편에서 발견한 패턴의 **가장 선명한
사례**다 — 혼합이 결과를 지배한다고 말하면서 혼합을 적지 않는다.

변호할 점도 공정하게 적는다:
- Materials and Methods 가 **통째로 SI** 에 있는 것은 *Science* 의 형식이다. SI 에는 적혀 있을
  가능성이 높고, 우리가 SI 를 못 구한 것이 1차 원인이다. **"저자가 안 적었다" 로 단정할 수 없다.**
- 그러나 **본문에서 "2000 rpm" 을 `[재현]` **8회**, "UHS" 를 **47회** 반복하면서 그 숫자가 어떤
  장비의 무엇을 가리키는지는 본문에서 한 번도 말하지 않는다.** 2000 rpm 은 유성볼밀·전단믹서·
  비드밀에서 각각 전혀 다른 에너지 밀도를 뜻한다. `[해석]` **본문만으로는 이 공정을 재현할 수
  없고, 그것이 Science 논문의 본문이라는 점이 문제다.**
- ★ `[해석]` 특히 "ball"·"mill" 이라는 단어를 **의도적으로 피한 것처럼 보인다** — 저자들이 특허를
  출원한 상태(18/440,838)라는 점과 같이 읽으면, 장비 특정을 피한 서술이 우연이 아닐 수 있다.
  **이것은 추정이고 근거는 정황뿐이다.**

### 2.4 ★★ 이 위키 최초 — 혼합 축의 완전 대조군 집합

지금까지 이 위키가 가장 아쉬워한 것이 "밀링이 SE 를 바꾸는가" 를 **가르는 대조군**이었다.
이 논문은 네 종류를 전부 갖췄다. **24편 중 유일하다.**

| 대조 | 조건 | Cl/P (표면) | 결과 |
|---|---|---|---|
| **pristine LPSCl** (혼합 안 함) | — | `[도표, Fig. 1E]` #1 49:51 · #2 50:50 · #3 50:50 → **비 ≈0.96–1.00** | 분리 없음. 본문 `[인쇄]` "atomic ratio of 5:1:1 for S, P, and Cl" |
| **손혼합** (무밀링, 상온) | hand-mixed S/LPSCl/C | `[도표, Fig. 1E]` **50:50 → 1.00** | ★ **분리 없음.** 접촉만으로는 안 생긴다 |
| **손혼합 + 가열** (무밀링, 열만) | 145 °C **3 h** | `[도표, Fig. 1E]` **58:42 → 1.38** | ★★ **부분 분리.** 기계력 없이 **열만으로도** 생긴다 |
| **저속 혼합** | **400 rpm** (시간 미기재, 5 h 추정) | 본문 `[인쇄]` fig. S6 — "no Cl segregation" | 분리 없음 |
| **단시간 혼합** | 2000 rpm **1 h** | 본문 `[인쇄]` fig. S5 — "no Cl segregation" | 분리 없음 |
| **표준 UHS** | **2000 rpm 5 h** | `[도표, Fig. 1E]` #5 78:22 → **3.55** · #6 71:29 → **2.45** · #4(벌크) 48:52 → 0.92 | ★ **표면 2.45–3.55배.** 본문 `[인쇄]` "two to three times increase" |
| **과혼합** | 2000 rpm **10 h** | 본문 `[인쇄]` "still preserved the feature of LiCl segregation but resulted in a **notable crystal structure collapse of LPSCl**"(fig. S35) | 분리는 유지, **SE 붕괴** |
| **황 없는 대조** | LPSCl + 탄소만 **가열** | — | ★★ 본문 `[인쇄]` "Similar results were observed during the heating of LPSCl and conductive carbon **without sulfur**, indicating that the **LiCl segregation was not driven by the reaction with sulfur**"(fig. S14) |

`[해석]` 이 표가 가르는 것:
1. **"접촉만으로" 는 아니다.** 손혼합 상온은 50:50 그대로다 → `park2026` 이 본
   "고에너지 밀링 없이도 PS₄³⁻ 가 움직인다"(Raman 425 → 418 cm⁻¹)와 **같은 현상이 아니다.**
   Park 2026 계는 **Li2S 라는 환원제**가 있었고, 여기는 S8(산화제)·Se·Te 다. 기전이 다르다.
2. **필요조건은 열이다.** 기계력 없이 145 °C 3 h 로 Cl/P 가 1.00 → 1.38 로 움직였다. 전단은
   저자 자신의 말로 "입자 미세화와 균질 혼합" 담당이다.
3. ★ **그러나 "황 없는 대조" 에는 탄소가 남아 있다.** LPSCl **단독** 가열 대조가 없다.
   ref 39(Ohno/Rosenbach/Dewald/Janek/Zeier)가 바로 **탄소가 황화물 SE 분해를 가속한다**고 한
   논문이고 저자들도 그것을 인용한다. 그러면 이 현상은 "할로겐 분리" 가 아니라 **"탄소가 촉진한
   LPSCl 열분해"** 일 수 있고, 저자 자신이 LiCl 을 `[인쇄]` "a major **electrochemical
   decomposition component** of LPSCl (35, 36)" 이라고 쓴다. → §9 비판 1.

### 2.5 이 위키 ball milling 전수 대조표에 추가할 행 (제안)

| 논문 | 경로 | 장비 | rpm | 시간 | BPR | 볼 · 용기 | 분위기 |
|---|---|---|---|---|---|---|---|
| **leej2025** (*Science*, Argonne) | ★ **one-step 삼상** (활물질 S8/Se/SeS2/Te) | ★ **미기재 — 본문에 "ball"·"mill" 이라는 단어 자체가 없다.** "ultrahigh-speed(UHS) mixing" | ★★ **2000** (대조 **400**) — 이 위키 최고속 | **5 h** (스캔 **1 / 5 / 10 h**) | 미기재 (SI 미확보) | 미기재 | 미기재 |

`[해석]` 표에 넣을 때 **"밀링 후 XRD 로 확인한 상" 칸은 이 논문이 유일하게 꽉 찬 칸**이다:
LiCl (111)·(200) 생성 + LPSCl 피크 감소 + LPSCl **격자상수 a 와 결정자 크기 모두 감소**
(fig. S19B) + 황의 결정성 소실(모든 혼합 조건에서 결정질 S 피크 없음) + XPS 로 Li3P 로의
심한 붕괴는 배제.

## 3. 할로겐 분리의 증거 — 무엇을 어떤 분해능으로 보았나 (Fig. 1 · Fig. 2)

### 3.1 측정 수단 전체 목록 `[인쇄]`

| 도구 | 무엇을 보았나 | 공간 분해능 / 깊이 | 정량인가 |
|---|---|---|---|
| **수차보정 cryo-TEM + 저선량 이미징** (figs. S7–S10 에 개발 과정) | LPSCl·복합양극의 표면→벌크 미세구조 | 원자 분해능 (HRTEM 격자면 2.18–3.78 Å 측정) | 정성 + 격자간격 정량 |
| **HAADF-STEM + EDS 맵/라인스캔** | Cl·P·S·Se·Br 의 공간 분포 | `[도표]` 스케일바 50 nm–1 µm. **투영 신호** — 두께 방향 적분 | 반정량 (원자비) |
| **EELS** (S-L2,3 165 · Cl-L2,3 200 · P-L2,3 132 · Li-K 55 eV) | 화학상태(S⁰ vs Sⁿ⁻, LiCl vs Li-P-S) | 나노 영역 지정 | 정성 (표준 KCl 참조) |
| **in situ 승온 SXRD** (NSLS-II) | 가열 중 LiCl 상 생성 | **벌크 평균 — 공간 분해능 없음** | 상 동정 + Rietveld(tables S2–S5, SI) |
| **x-ray PDF** (fig. S19C) | 단거리 구조 | 벌크 평균 | — |
| **Raman** (fig. S19D) | PS₄³⁻ 등 | 벌크/점 | — |
| **XPS** (figs. S20–S22) | LiCl 생성, Li3P 배제 | **표면 ~5–10 nm** (일반값, 원문 미기재) | 반정량 |
| **S K-edge XANES** (2465–2490 eV) | S⁰/Li2S/LPSCl 구별, 폴리설파이드 유무 | **벌크 평균** | 정성 |
| **in situ Se K-edge XANES** (12650–12670 eV) | Se 산화상태 궤적 | 벌크 평균 | 정성 |
| **in situ µ-CT** (ALS 8.3.2) | 전극 팽창·균열·공극 | `[해석]` µ-CT 는 보통 µm 급 복셀 (원문 미기재) | **본문에는 형용사만** |
| **온라인 셀 스택압 측정** | 충방전 중 압력 변화 | 셀 수준 | **본문에는 형용사만** |
| **in situ 가열 TEM** (figs. S16–S17, movies S1–S2) | 가열 중 실시간 변화 | 원자/나노 | 정성 |

★ `[해석]` **공간 분해능은 충분하고(원자급 HRTEM), 깊이 정보는 약하다.** EDS/HAADF 는 투영
신호라 "표면 껍질" 의 두께를 직접 주지 않고, XPS 는 ~10 nm 깊이만 본다. 그래서 **G12(LiCl 층
두께)가 끝까지 수치로 안 나온다.**

### 3.2 Fig. 1 — S/LPSCl/C 계 `[도표 + 인쇄]`

| 패널 | 읽은 것 |
|---|---|
| **1A** pristine LPSCl HAADF + Cl/P/S 맵, 스케일바 **1 µm** | 세 원소가 입자 전체에 균일 |
| **1B** 라인스캔 (폭 ≈5500 nm) | S ≈75 at%, Cl ≈12, P ≈12 로 **평탄** |
| **1C** UHS 2000 rpm 5 h 시료, 스케일바 **500 nm** | ★ Cl 맵에 **고리 모양 테두리**가 뚜렷 — Cl 이 입자 가장자리에 몰려 있다. P·S 는 중앙 |
| **1D** 라인스캔 (폭 ≈1800 nm) | Cl(적) 이 양끝에서 ≈50–60 at% 로 치솟고 중앙은 ≈10. 점선으로 표시된 Cl-rich 구간 폭 `[도표]` **≈200–400 nm** (단, 투영 효과로 과대평가 가능 — G12) |
| **1E** Cl:P 정량 (★ 2.4 표에 전부 옮김) | pristine 0.96–1.00 → UHS 표면 **2.45 · 3.55** → 손혼합 1.00 → 145 °C 3 h **1.38** |
| **1F** EELS S-L2,3 + Cl-L edge | site #7(적) 온셋 **168.6 eV** = `[인쇄]` "S⁰+Cl-rich" · site #8(청) 온셋 **166.6 eV** = "Sⁿ⁻+Cl-deficient". **2 eV 의 화학이동** |
| **1G** in situ SXRD 승온 40→400 °C, 2θ **3.4–4.1°** (싱크로트론 단파장) | **LiCl(111) ≈3.48° · LPSCl(311) ≈3.52° · LPSCl(222) ≈3.65° · LiCl(200) ≈4.00°**. 고온으로 갈수록 LiCl 두 피크가 자라고 LPSCl 두 피크가 줄어든다 |

★ `[해석]` **1F 가 가장 중요한 패널일 수 있다.** Cl-rich 영역의 황이 **S⁰(원소황)** 이고
Cl-deficient 영역의 황이 **Sⁿ⁻(황화물 음이온, 즉 LPSCl 의 PS₄³⁻)** 이라는 뜻이다. 즉
**LiCl 은 "황 입자 쪽" 에, Cl 빠진 Li-P-S 는 "SE 쪽" 에 남는다** — 분리가 공간적으로 방향성이
있다. 저자들은 이 패널을 지나가듯 쓰지만 기전의 핵심이다.

### 3.3 Fig. 2 — 보편성(Se·Br) 과 결정학적 동정 `[도표 + 인쇄]`

| 패널 | 읽은 것 |
|---|---|
| **2A** Se/LPSCl/C, 스케일바 **50 nm** | Se(적)와 Cl(청) 맵이 겹치지 않고 Cl 이 Se 를 둘러싼다. S+P 맵에서 Se 자리가 **검게 비어** 있다 |
| **2B** Se/LPSBr/C, 스케일바 **50 nm** | Br(청) 과 Se(적) 로 같은 구도 |
| **2C** 정량 `[도표]` | Se/LPSCl: I **65:35 = 1.86** · II **64:36 = 1.78** · III **22:78 = 0.28**(벌크). Se/LPSBr: IV **64:36 = 1.78** · V **82:18 = 4.56** · VI **81:19 = 4.26**. 본문 `[인쇄]` "rose by **1.5 to 4.6 times**" ✅ 그림과 일치 |
| **2D** ADF-STEM + EELS 맵, 50 nm / 확대 20 nm | ★ **"LiCl-rich interface"** 가 Se 입자 윤곽을 따라 **띠**로 보인다. `[도표]` 띠 폭 ≈10–20 nm — **Fig. 1D 의 200–400 nm 와 자릿수가 다르다**(G12) |
| **2E** EELS Li-K/P-L/S-L/Cl-L | 영역 VII(적) = **Li-Cl**, P-deficient, Cl-rich · 영역 VIII(청) = **Li-P-S**, P-rich, Cl-deficient. ★ Li-K edge 가 **≈55 eV** 에서 둘 다 뜬다 |
| **2F** HRTEM, 10 nm 바 | **LiCl(111) d ≈2.91 Å** · **Se(100) d ≈3.78 Å** · **C(002) d ≈3.39 Å** — 탄소와 LiCl 이 함께 Se 를 덮는다 |
| **2G** 실측 vs 시뮬레이션 | LiCl [110]: **2.95 Å (1-11) · 2.53 Å (002)** · Se [212]: **3.01 Å (10-1) · 2.18 Å (1-20)** |
| **2H** FFT vs 표준 FFT | 각도 **71°**(LiCl) · **54°**(Se). 입방 **Fm-3m LiCl** · 육방 **P3121 Se** 동정 |

★ `[인쇄]` 중요한 단서 하나: "The composite Se cathodes **did not form similar core-shell
structures as the UHS-mixed composite S cathode** owing to the difference in material properties
between S and Se, such as **melting point and ductility**." → **S 계만 core–shell 이고 Se 계는
아니다.** 그런데 LiCl 분리 자체는 양쪽 다 일어난다. `[해석]` 황의 녹는점(115 °C)이 낮아서
혼합 중 **연화/용융**했다는 뜻으로 읽힌다 — 145 °C 가열 대조가 황 녹는점 위라는 점과 맞물린다.

## 4. 전기화학 성능 (Fig. 3) — 양단위 전량

### 4.1 공통 조건 `[인쇄]`

> "…all-solid-state cells with a **Li-In anode**, areal active material (e.g., S) loading of
> **4 mg cm⁻²**, and a **stack pressure of ~70 MPa**, unless specified otherwise. Moreover, we
> tested all the cells at **room temperature (~25 °C)**…"

| 항목 | 값 | 비고 |
|---|---|---|
| 음극 | **Li–In** (fig. S38 에 Li 금속 셀) | N/P·두께·조성 미기재 |
| 활물질 로딩 | **4 mg cm⁻²** 표준, **2 mg cm⁻²** 장수명 | 활물질 기준(S·Se·SeS2·Te 각각) |
| **운전 스택압** | **~70 MPa** 표준. `[인쇄]` 추가로 **36 MPa · 18 MPa** 평가(fig. S40) | ★ **성형압은 본문에 없다**(G6) — 두 압력을 반드시 분리해 읽는다 |
| 온도 | **25 °C** 전부 | 저자들이 `[인쇄]` 60 °C 문헌과 대비해 강조 |
| 전압창 | `[도표, Fig. 3B]` **≈0.4 → ≈2.3 V vs Li–In** | **인쇄된 컷오프 수치가 없다.** vs Li/Li⁺ 로 환산하지 않는다 |
| 전류밀도 | 0.67 / 1.4 mA cm⁻² (S) · 0.27(Se) · 0.54(SeS2) · 0.56(Te) | C-rate 는 원문에 없다 → `[재현]` 아래 |

**C-rate `[재현]`** (= 전류밀도 ÷ 로딩 ÷ 해당 활물질 2전자 이론용량):

| 셀 | 전류밀도 | 비전류 | C-rate |
|---|---|---|---|
| S, 4 mg cm⁻² | 0.67 mA cm⁻² | 167.5 mA g⁻¹(S) | **0.100 C** |
| S, 4 mg cm⁻² (장수명) | 1.4 mA cm⁻² | 350 mA g⁻¹(S) | **0.209 C** |
| S, 2 mg cm⁻² (장수명) | 0.67 mA cm⁻² | 335 mA g⁻¹(S) | **0.200 C** |
| Se, 4 mg cm⁻² | 0.27 mA cm⁻² | 67.5 mA g⁻¹(Se) | **0.099 C** (이론 678.8) |
| SeS2, 4 mg cm⁻² | 0.54 mA cm⁻² | 135 mA g⁻¹(SeS2) | **0.120 C** (이론 1123.8, 6전자) |
| Te, 4 mg cm⁻² | 0.56 mA cm⁻² | 140 mA g⁻¹(Te) | **0.333 C** (이론 420.1) |

`[해석]` **전부 0.1–0.33 C 의 저율이다.** "extraordinary cycling stability" 는 저율 조건의 것이다.

### 4.2 ★ Fig. 3A — 혼합 시간 1 / 5 / 10 h (4 mg cm⁻², 0.67 mA cm⁻², 100사이클)

| 시료 | 1사이클 | 최고점 | 100사이클 | 비고 |
|---|---|---|---|---|
| **5 h (UHS 표준)** | `[인쇄]` **6.28** mAh cm⁻² (`[도표]` ≈6.35) | ★ `[도표]` **≈7.85 @ 30–40사이클** | `[인쇄]` **6.21** | `[인쇄]` 유지율 **98.9 %** |
| **10 h (과혼합)** | `[도표]` ≈4.4–6.1 (첫 두 점이 흩어진다) | `[도표]` ≈5.75 @ ≈16사이클 | `[도표]` **≈2.3** | 급감 |
| **1 h (미달)** | `[도표]` ≈2.4 | `[도표]` ≈3.05 @ ≈16사이클 | `[도표]` **≈0.55** | 급감 |
| CE | — | — | `[도표]` 전 구간 **≈98–100 %** (첫 사이클만 흩어진다, G17) | 인쇄값 없음 |

**양단위 환산 `[재현]`** (÷4 mg cm⁻², ×0.69783):

| 조건 | mAh g⁻¹(S) | mAh g⁻¹(Li2S) | 2전자 이용률 | (1전자 기준) |
|---|---|---|---|---|
| 5 h 1사이클 `[인쇄]` 6.28 | **1570.0** | **1095.6** | **93.9 %** | (187.8 %) |
| ★ 5 h 최고점 `[도표]` ≈7.85 | **≈1962.5** | **≈1369.5** | ★ **117.4 %** | (234.7 %) |
| 5 h 100사이클 `[인쇄]` 6.21 | **1552.5** | **1083.4** | **92.9 %** | (185.7 %) |
| 10 h 100사이클 `[도표]` ≈2.3 | ≈575 | ≈401 | 34.4 % | (68.8 %) |
| 1 h 1사이클 `[도표]` ≈2.4 | ≈600 | ≈419 | 35.9 % | (71.8 %) |
| 1 h 100사이클 `[도표]` ≈0.55 | ≈137.5 | ≈96 | 8.2 % | (16.4 %) |

★★ `[해석]` **"98.9 % 유지" 는 봉우리를 건너뛴 양끝 비교다.** 5 h 시료는 30–40사이클에서
≈7.85 mAh cm⁻² 까지 **+25 % 올랐다가** 100사이클에 첫 사이클 값으로 **되돌아온** 것이다.
그 봉우리는 **2전자 이론용량의 117 %** 이므로 그 구간의 용량 중 최소 17 %는 황이 낸 것이 아니다
(저자들도 §4.6 에서 SE 기여를 인정한다). 즉 **유지율 98.9 % 는 "황 용량이 안 줄었다" 가 아니라
"황 손실과 SE 기여 증가가 상쇄되다가 둘 다 꺾였다" 로도 읽힌다.** 이 위키의 다른 digest 에서
`[해석]` 로 여러 번 겪은 함정이고, 여기서는 **원문이 스스로 이론 초과를 인정하기 때문에 더 강하다.**
1 h·10 h 시료도 똑같이 10–16사이클에 봉우리를 갖는다 → **"활성화 구간" 이 세 시료 공통**이다.

### 4.3 Fig. 3B — 전압곡선 (5 h 시료, 1/2/20/50/100사이클)

- 축: **Voltage (V vs Li–In)** 0.4–2.3 · Areal capacity 0–8 mAh cm⁻².
- 방전: `[도표]` 평탄역이 **≈1.30 V(1사이클) → ≈1.38 V(100사이클)** 에서 시작해 단조 하강,
  종단 ≈1.1 V 에서 급락. **S8 계라 Li2S 특유의 첫 충전 활성화 돌기가 없다**(셀이 충전상태에서 출발).
- 충전: `[도표]` **≈1.60 V(1사이클) → ≈1.72 V(100사이클)** 에서 시작해 ≈1.9–2.05 V 로 상승.
- ★ `[도표]` **3 mAh cm⁻² 지점의 ΔV: 1사이클 ≈0.65 V → 100사이클 ≈0.80 V (약 +0.15 V, +23 %)**
  (판독 오차 ±0.05 V). 본문은 `[인쇄]` "**minimal** polarization increase" 라고만 쓴다.
  `[해석]` **0.15 V 는 1.3 V 급 셀에서 작지 않다** — "minimal" 은 비교 대상(1 h·10 h) 대비의 말로
  읽어야 한다. ⚠ 이 수는 **ΔV(충방전 분극)** 이고 **활성화 과전위가 아니다** (이 위키가 두 번
  겪은 혼동 — 여기서는 Li2S 첫 충전 자체가 없으므로 활성화 과전위라는 양이 존재하지 않는다).

### 4.4 Fig. 3C·3D — 장수명 450사이클

| 조건 | 1사이클 | 450사이클 | 유지율 | `[재현]` mAh g⁻¹(S) / (Li2S) |
|---|---|---|---|---|
| **2 mg cm⁻², 0.67 mA cm⁻² (0.20 C)** | `[재현]` **≈3.219** (= 3.00 ÷ 0.932) · `[도표]` ≈3.2 | `[인쇄]` **3.00** mAh cm⁻² | `[인쇄]` **93.2 %** (그림 안 글자는 "93 % retention") | 1사이클 **1609.5 / 1123.2** (96.3 %) → 450사이클 **1500.0 / 1046.7** (89.7 %) |
| **4 mg cm⁻², 1.4 mA cm⁻² (0.21 C)** | `[인쇄]` **6.35** (`[인쇄]` "a high sulfur utilization of **95 %**") | `[도표]` **≈5.0** | `[인쇄]` **80 %** | 1사이클 **1587.5 / 1107.8** (94.9 %) → 450사이클 **≈1250 / ≈872** (74.8 %) |

`[해석]` 인쇄된 "95 % utilization" 은 `[재현]` 1587.5 ÷ 1672 = **94.9 %** 로 **2전자 기준이
맞다** — 이 위키 기준과 일치한다. 드물게 단위가 깨끗한 논문이다.
단 **4 mg·2 mg 두 셀 모두 n=1 로 보이고 오차막대가 없다**(G13).

### 4.5 Fig. 3E — 다른 칼코겐 (4 mg cm⁻², 100사이클) ⚠ **(S)/(Li2S) 환산 불가 — 분모가 Se·SeS2·Te 다**

| 활물질 | 1사이클 `[도표]` | 최고점 `[도표]` | 100사이클 `[도표]` | 비용량 1사이클 `[재현]` | 2전자(SeS2 는 6전자) 이론 | 이용률 |
|---|---|---|---|---|---|---|
| **SeS2** (적) | ≈4.9 mAh cm⁻² | ≈5.3 @ ≈20 | ≈3.9 | ≈1225 mAh g⁻¹(SeS2) | 1123.8 | **≈109 %** (최고점 ≈118 %) |
| **Se** (회) | ≈3.7 | ≈3.75 | ≈3.5 | ≈925 mAh g⁻¹(Se) | 678.8 | ★ **≈136 %** |
| **Te** (청) | ≈3.0 | ≈3.15 | ≈3.1 | ≈750 mAh g⁻¹(Te) | 420.1 | ★★ **≈179 %** |
| CE | — | — | `[도표]` ≈98–100 % (우축이 120 까지, 중간 절단) | | | |

본문은 `[인쇄]` "commercial-level areal capacities (**3 to 5 mA·hour cm⁻²**)" 라고 쓴다 — 그림과 일치.

### 4.6 ★★ Fig. 3F — SE 종류 (4 mg cm⁻² S, 0.67 mA cm⁻², 50사이클)

| SE | 할로겐 | 1사이클 `[도표]` | 최고점 `[도표]` | 50사이클 `[도표]` | `[재현]` mAh g⁻¹(S) / (Li2S) (최고점) | 2전자 이용률 |
|---|---|---|---|---|---|---|
| **LPSClI** (녹) | Cl + I | ≈6.7 | ★ **≈7.8 @ 8–22** | ≈5.1 | **≈1950 / ≈1361** | ★ **116.6 %** |
| **LPSBr** (황) | Br | ≈6.1 | ≈7.25 @ ≈22 | ≈5.8 | ≈1813 / ≈1265 | 108.4 % |
| **LPSClBr** (주황) | Cl + Br | ≈7.0 | ≈7.2 @ 3–5 | ≈5.8 | ≈1800 / ≈1256 | 107.7 % |
| **LGPS** (연회) | **없음** | ≈4.9 | — | ★ **≈1.05** | ≈262 / ≈183 | 15.7 % |
| **SS7** (진회, 정의 없음 G14) | **없음** | ≈4.65 | — | ★ **≈1.15** | ≈288 / ≈201 | 17.2 % |

★★ `[해석]` **이것이 이 논문에서 가장 설득력 있는 대조군이다.** 할로겐 없는 SE 두 종은
**첫 사이클에만 4.65–4.9 mAh cm⁻² 를 내고 2사이클째부터 ≈1.1 로 주저앉는다** — 즉 첫 방전은
비슷하게 되는데 **가역성이 없다.** 할로겐 있는 네 종은 전부 5.1–7.8 을 유지한다.
`[인쇄]` 저자들은 fig. S42 에서 "**이온전도도는 다 비슷하다**" 고 밝혀 교란변수를 하나 지웠다
(값은 SI 라 미확보 — G9 와 같은 공백).
⚠ 그러나 **LGPS(= Li10GeP2S12)의 Ge⁴⁺ 는 황/탄소와의 전기화학 안정성이 원래 나쁘다**는 것이
널리 알려져 있어, "할로겐이 없어서" 가 아니라 "그 SE 가 원래 불안정해서" 일 수 있다.
저자들은 그 구분을 하지 않는다 → §9 비판 2.

### 4.7 본문이 인정한 **이론 초과 용량** `[인쇄]`

> "In addition, it was noted that the UHS-mixed composite chalcogen cathodes **exhibit greater
> capacity than their theoretical capacity limits** (table S6), which can be attributed to the
> **capacity contribution of the LPSCl SSE** (36, 38). Although it has been shown that carbon would
> accelerate the decomposition of sulfide SSEs, particularly at high and low potential (39), the
> superior cycling stability … revealed that the interfacial halide segregation **might help
> suppress these side reactions as well** (figs. S44 to S46), **adding extra capacity and energy
> density to the cell without sacrificing stability**."

★★ **이 위키의 "이론 초과" 외부 눈금에 넣을 새 좌표** `[재현]` — 초과분을 **면적용량(mAh cm⁻²)**
으로 환산하면 활물질이 달라도 거의 같다:

| 셀 | 2전자 이론 면적용량 (4 mg cm⁻²) | 관측 최고 `[도표]` | **초과분** |
|---|---|---|---|
| S / LPSCl | 6.688 mAh cm⁻² | ≈7.85 | **≈+1.16** |
| S / LPSClI | 6.688 | ≈7.8 | **≈+1.11** |
| SeS2 / LPSCl (6전자) | 4.495 | ≈5.3 | **≈+0.81** |
| Se / LPSCl | 2.715 | ≈3.75 | **≈+1.04** |
| Te / LPSCl | 1.680 | ≈3.15 | **≈+1.47** |

★★ `[해석]` **초과분이 활물질 종류와 무관하게 ≈0.8–1.5 mAh cm⁻² 로 모인다.** 네 활물질의
이론용량은 420 에서 1124 mAh g⁻¹ 까지 2.7배 차이가 나는데 초과분은 2배 안쪽이다. 이것은
**초과 용량이 활물질이 아니라 모든 셀에 공통인 무엇(= SE, 어쩌면 탄소)에서 나온다는 저자 주장과
정량적으로 맞는다.** ⚠ 단 **복합양극 조성비(G4)를 모르므로 SE 로딩이 셀마다 같은지 확인할 수
없다** — 활물질 로딩만 4 mg cm⁻² 로 맞춰져 있다. 조성이 같다면 SE 로딩도 같을 것이라는 가정
위의 계산이다.
⚠ 그리고 Te 셀은 **용량의 44 %가 활물질에서 온 것이 아니다**(1.47/3.15). 그 셀에 대해
"utilization close to 100 %" 라고 말하는 것은 의미가 없다 → §9 비판 3.

기존 외부 눈금과 나란히: `wangd2025` **4–6 %** · `gao2024` **28–52 mAh g⁻¹(composite)** ·
이 논문 **≈0.8–1.5 mAh cm⁻² (= 4 mg cm⁻² 기준 S 로 치면 200–370 mAh g⁻¹(S) 어치)**.
`[해석]` **이 논문의 SE 기여 추정치가 기존 두 눈금보다 훨씬 크다.** 셋 다 SE·조건이 달라
직접 비교는 못 하지만, **"SE 기여는 수 % 수준" 이라는 종전 감각을 흔든다.**

### 4.8 그 밖에 본문이 한 줄로 언급하고 그림은 SI 인 것

| 주장 | 근거 그림 | 상태 |
|---|---|---|
| Li 금속 음극으로도 우수한 수명 | fig. S38 | **SI 미확보** |
| 황 함량 **32.5 wt %** 로 올려도 고용량·안정 | fig. S39 | **SI 미확보** |
| 스택압 **36 · 18 MPa** 에서도 높은 유지율 | fig. S40 | ★ **SI 미확보** — [[operating-stack-pressure-floor]] 에 직결되는데 수치가 없다 |
| 칼코겐 4종 율속 성능 | fig. S41 | **SI 미확보** |
| 손혼합 + 가열이 황 이용률을 올린다 | fig. S43 | **SI 미확보** — ★ 2.4 의 가열전용 대조의 **전기화학 짝** |
| 할로겐 분리가 SE 부반응도 억제 | figs. S44–S46 | **SI 미확보** |
| 10 h 시료는 1충전 후 Li2S 잔류 | fig. S47 | **SI 미확보** |

## 5. 사후분석 — 반응 경로와 미세구조 (Fig. 4)

### 5.1 S K-edge XANES (Fig. 4A) `[인쇄 + 도표]`

- 기준 스펙트럼 3종: **Sulfur**(황), **Lithium sulfide**(Li2S), **LPSCl**. 에너지 2465–2490 eV.
- `[인쇄]` pristine 복합양극 = S 특징(**2473, 2480 eV**) + LPSCl 특징(**2472 eV**).
- `[인쇄]` **반 방전/반 충전 상태에서 ~2470 eV 피크가 없다 → 가용성 폴리설파이드 생성 없음**(ref 13 기준).
- `[인쇄]` 1차 완전방전 후 LPSCl 피크는 남고 황 피크가 **2473 → 2474 eV** 로 이동, Li2S 기준과 일치.
- `[인쇄]` 1차 완전충전 후 Li2S 피크 소멸 + S 신호가 원위치 복귀. 30번째 방전이 1차 방전과 겹침.
- `[인쇄]` **10 h 시료는 1충전 후 Li2S 가 눈에 띄게 잔류**(fig. S47) → 가역성 저하.

★ `[해석]` 이 위키의 **H6(전자수 제한)** 과의 관계: 이 셀은 S8 에서 출발해 **Li2S 까지 간다**
(XANES 가 Li2S 기준과 겹친다) — 즉 **2전자를 다 쓴다.** 그래서 `kimjt2023` 의 "Li2S2 에서
멈춘다" 와는 다른 결론이다. 단 **분해능이 다르다** — kimjt2023 은 2471.3 eV **어깨**를 보고
판정했고 여기는 2474 eV **주피크 위치**만 말한다. **직접 반증으로 쓸 수 없다.**

### 5.2 in situ Se K-edge XANES (Fig. 4B·4C) `[인쇄 + 도표]`

- `[도표]` 2D 컨투어: x = 12650–12670 eV, y = **시간 0–15 h**(한 사이클 전체), 왼쪽에 전압 프로파일.
  ⚠ **전압축 눈금이 3/2/1 V 로 Fig. 3B(0.4–2.3 V vs Li–In)와 다르다 — 기준전극 불명(G16).**
- `[인쇄]` 방전·충전 전 과정에서 **흡수단 위치가 뚜렷이 이동하지 않고**, 흡수 강도만 방전 중
  점진 감소했다가 충전 끝에 완전 회복. 1차 미분(4C)도 같은 결론.
- `[인쇄]` 이 거동은 **폴리셀레나이드가 안 생기는 카보네이트 전해질**(ref 40)의 경로와 같고,
  폴리셀레나이드 용해도가 큰 에테르계(ref 41)와 정반대.

`[해석]` S 와 Se 양쪽에서 **"가용성 중간체 없음"** 을 보인 것이 이 논문의 두 번째 주장이다.
다만 **"흡수단이 안 움직인다" 는 음성 결과**이고, 분해능·셀 설계(in situ XAS 셀이 Fig. 3 의
셀과 같은지 불명)에 대한 기술이 본문에 없다.

### 5.3 방전 생성물의 미세구조 (Fig. 4D–G) `[도표 + 인쇄]`

| 패널 | 읽은 것 |
|---|---|
| **4D** 1차 방전 후 HAADF, 100 nm 바 | LPSCl 기지(어두움) 안에 밝은 나노입자가 **균일 분산** |
| **4E** SAED, 2 nm⁻¹ 바 | 다결정 고리 |
| **4G** SAED 적분 프로파일 2.5–5.0 nm⁻¹ | `[도표]` (111) ≈2.9 · (200) ≈3.35 · (220) ≈4.72 nm⁻¹ → 입방 **Fm-3m Li2Se** |
| **4F** HRTEM Li2Se [110], 1 nm 바 | `[도표]` **3.4 Å (111) · 3.01 Å (002) · 면각 123.9°**. `[인쇄]` 입자 크기 **약 10 nm** |

`[인쇄]` "The formation of **nanocrystalline discharge products** not only reduces the energy
barriers for nucleation and decomposition of Li2Se, enabling more efficient reactions, but also
mitigates the volume swelling and shrinkage during repeated cycling…" (ref 42 인용)

★★ `[해석]` **이것이 우리 Li2S 축에 가장 직접 걸리는 관측이다.** 방전 생성물이 **≈10 nm
나노결정**이면 역반응(충전)의 핵생성 장벽이 낮다. 우리 pristine Li2S 는 **상용 µm 급**이고
첫 충전에서 바로 그 장벽에 걸린다 — 즉 **"작은 Li2S 가 좋다" 를 생성물 쪽에서 본 사례**다.
단 **활물질이 Se 이고 Li2Se 이며, Li2S 가 아니다.** 저자들이 S 계로 같은 실험을 못 한 이유를
`[인쇄]` "owing to the extreme sensitivity of sulfur and related species, such as Li2S" 라고 밝힌다.

### 5.4 100사이클 후 계면 (Fig. 4H·4I) `[도표]`

| 영역 | Cl : P | 비 |
|---|---|---|
| #1 | 61 : 39 | **1.56** |
| #2 | 57 : 43 | **1.33** |
| #3 | 59 : 41 | **1.44** |

`[인쇄]` "…Cl segregation and deposition at the cathode surface **remains well preserved**, with a
Cl-to-P ratio **close to that of the pristine state** (Fig. 2C)."

⚠ `[해석]` **Fig. 2C 의 pristine Se/LPSCl 값은 1.86 · 1.78 이었다**(벌크 영역 0.28 제외).
100사이클 후는 **1.33–1.56** 이다 → `[재현]` **약 15–25 % 감소**했다. "close to" 가 틀린 말은
아니지만 **단조 감소 방향**이고, 450사이클 셀에서는 어떤지 보지 않았다. **이 층이 소모성인지
자기유지성인지 이 논문은 답하지 않는다.**

## 6. ★ 유효 이온 수송 — σ 를 세 칸 중 어디서 쟀나

본문에 인쇄된 수송 관련 문장은 **두 개뿐**이다:

> `[인쇄]` "Whereas **the ionic conductivity of bulk LPSCl SSEs decreased along with the time of
> UHS mixing**, the **Li⁺ diffusion coefficient of the UHS-mixed composite cathodes increased
> substantially**, with the 5-hour UHS-mixed composite S cathode demonstrating an **increase 196
> times greater than that of the 400-rpm cathode** (fig. S36)."

> `[인쇄]` "Despite **similar ionic conductivities among all the used SSEs** (fig. S42)…"

| 칸 (이 위키 3분법) | 이 논문이 잰 것 | 값 | 방향 |
|---|---|---|---|
| **① 복합체 퍼콜레이션** (10⁻²–10⁻¹ 급) | **Li⁺ 확산계수 D** (σ 가 아니다) | **400 rpm 대비 196배** — 절대값·단위·분모 전부 없음 | ★ **상승** |
| **② SE 상 자신** (10⁻⁸–10⁻³) | **벌크 LPSCl 이온전도도** | **수치 전무** (G9) | ★ **하락** |
| **③ 활물질 입자 자신** | 측정 없음 | — | — |

★★ `[해석]` **이 논문은 ①과 ②를 같은 문장 안에서 반대 방향으로 보고한 첫 논문이다.**
이 위키가 H2b 를 두고 다툰 바로 그 분해를 저자들이 스스로 해 놓았다.

**DC 분극 레시피는 하나도 없다.** 차단전극 재질·적층·인가 전압·유지 시간·면적·두께·성형압 —
전부 본문에 없고 fig. S36 은 미확보다(G8). `[해석]` 그리고 **보고된 양이 σ 가 아니라 D 다** —
D 와 σ 는 Nernst–Einstein 으로 묶이지만 **농도(캐리어 수)가 변하면 비례하지 않는다.**
LiCl 생성으로 LPSCl 의 Li 재고가 바뀌었다면 D 상승이 곧 σ 상승은 아니다.
⚠ 그리고 **분모가 400 rpm 시료**다. 400 rpm 시료는 저자들 자신의 설명으로 **Cl 분리가 없어서
성능이 나쁜 전극**이고, Fig. 3A 의 1 h 시료처럼 1사이클 2.4 mAh cm⁻² 급일 수 있다.
**망가진 대조군을 분모로 쓰면 196배는 쉽게 나온다** — 이 위키가 `hao2025` 에서
≈10 mAh g⁻¹(Li2S) 대조군을 근거로 "개선 배수" 를 깎은 것과 같은 자리다.
`[해석]` **196배는 이 digest 에서 인용하되, 배수가 아니라 "부호(상승)" 만 근거로 쓴다.**

**이 위키 표준과의 대조**: 우리 표준은 전자 ±20 mV / 이온 ±40 mV 다점, 각 1 h 다.
문헌 계보를 타고 **1 V 까지 커진 사례**(황화물 안정창을 넘겨 분해 전류를 전자 전류로 읽는다)가
있었다. 이 논문은 **인가 조건을 본문에 한 글자도 안 적어 그 검증 자체가 불가능하다.**

## 7. ★ 부피변화 억제 — 무엇으로 쟀고 무엇을 안 적었나

| 측정 | 수준 | 인쇄된 내용 | 수치 |
|---|---|---|---|
| **온라인 셀 스택압 측정** (충방전 중) | ★ **셀 수준** | `[인쇄]` "revealed a **minimum pressure loss** in the 5-hour UHS-mixed composite S cathode, indicating that the segregated LiCl layer could also suppress the volume change of sulfur particles during cycling (fig. S37)" | **없음** (MPa 도 % 도) |
| **in situ µ-CT** (ALS 8.3.2, 충방전 중) | ★ **전극 수준** | `[인쇄]` "showed **minimal electrode expansion and no formation of visible cracks or pores** (fig. S50), confirming that the segregated LiCl interfacial layer could well suppress the volume change during cycling" | **없음** (µm 도 % 도) |
| **입자 수준 근거** (간접) | 입자 | `[인쇄]` 방전 생성물이 **≈10 nm 나노결정 Li2Se** → 팽창·수축 완화 (ref 42) | 입자 크기만 |

★★ `[해석]` **셀 수준(스택압)과 전극 수준(µ-CT)을 둘 다 쟀다 — 그 점은 이 위키 기준으로 모범이다**
(`zhangj2026` 에서 두 수준을 섞어 읽는 함정을 겪었다). **그런데 본문에는 숫자가 하나도 없다.**
*Science* 본문이 "부피변화를 억제한다" 를 초록의 핵심 주장으로 걸어 놓고 **형용사 두 개**
("minimum", "minimal")로 끝낸다. 이 위키의 좌표와 나란히 두면 공백이 선명하다:

| 논문 | 수준 | 수치 |
|---|---|---|
| `qu2025` | 전극 | `[인쇄]` 첫 몇 사이클에 **14–20 µm 수축**(절반이 Li2S 첫 충전 한 번) |
| `cronk2026` | — | **−42 %** |
| `jeong2026` | — | **+46.6 %** |
| `zhangj2026` | 셀 / 양극 | **−17.2 → +2.6 %**(셀) vs **+21.4 %**(양극 XCT) |
| **`leej2025`** | 셀 + 전극 둘 다 | ★ **수치 없음 (G10)** |

⚠ 용어 주의: `[인쇄]` "**pressure loss**" 는 **압력이 줄어든 양**이다. 황 → Li2S 전환은 **팽창**
(본문 서두 `[인쇄]` "large volume swelling (~80 %) of sulfur")이므로 방전 중 스택압은 **올라야**
한다. "minimum pressure loss" 가 (a) 사이클 후 **비가역 압력 감소**가 작다는 뜻인지,
(b) 충방전 중 압력 진폭이 작다는 뜻인지 **본문만으로는 가릴 수 없다.** fig. S37 을 봐야 한다.

## 8. ★ 무게 대가 회계 — 첨가제가 아니라 SE 를 깎아 만든 계면층

이 위키는 LiX 계열 첨가제의 **무게 대가**를 축적해 왔다:

| 논문 | 첨가제 | 양 | 대가 (환산 손실) |
|---|---|---|---|
| `wan2021` | LiI·LiBr | **39.9 wt%** | 109.4 mAh g⁻¹(Li2S) |
| `zhang2026` | — | 43.8 wt% | 152 |
| `kwok2023` | — | 40 wt% | 147 |
| `gao2024` | CuI | 42.3 wt% | 102.9 |
| `hong2026` | — | **16.7 wt%** | 34.5–138 |
| `feng2026` | FeCl3 | 26.1 wt% | 43.1 |
| `hao2025` | FeCl3 | 23.5 wt% | 32.4 |

★★ **이 논문은 이 표에 그대로 들어가지 않는다.** LiCl 을 **넣은 것이 아니라 SE 에서 꺼냈기**
때문이다. 회계를 어떻게 해야 하는가 — `[해석]` 세 가지로 나눠 적는다:

1. **복합양극 질량 기준 대가 = 0.** 외부에서 추가된 물질이 없다. 혼합 전후 질량은 (휘발 없다면)
   같다. 그래서 **mAh g⁻¹(composite) 분모가 안 늘어난다** — 첨가제 전략 대비 구조적 이점이고,
   저자들이 `[인쇄]` "no extra components … are required, contributing to substantial cost
   advantages" 라고 주장하는 근거다. **이 주장은 타당하다.**
2. **그러나 SE 가 소모된다.** 대가는 질량이 아니라 **기능(SE 의 이온전도도)** 으로 나타난다.
   저자 자신이 `[인쇄]` 벌크 LPSCl 전도도가 UHS 시간에 따라 떨어진다고 적었고, 10 h 에서는
   `[인쇄]` LPSCl **결정구조가 붕괴**해 성능이 꺾였다. ★ **즉 이 전략의 대가는 "SE 를 얼마나
   태워 쓰는가" 이고, 5 h 는 그 최적점이다.**
3. **상한 계산** `[재현]`: LPSCl 의 Cl 이 **전량** LiCl 로 빠져나가는 극한에서
   `Li6PS5Cl → Li5PS5 + LiCl`, M(LiCl)/M(Li6PS5Cl) = 42.391 / 268.37 = **15.80 wt%**.
   → **LPSCl 질량의 최대 15.8 % 가 LiCl 로 바뀔 수 있고 그 이상은 불가능하다.**
   복합양극에서 SE 가 가령 60 wt% 라면 복합체 기준 최대 **9.5 wt%** 다.
   `[해석]` **상한만 보면 `hong2026` 의 16.7 wt% 첨가제와 같은 자릿수**다 — "첨가제 없는 전략"
   이라고 해서 물질 수지가 공짜인 것은 아니다. 다만 그 질량이 **밖에서 들어오지 않고 안에서
   옮겨간다.**
4. **실제 전환율은 원문에 없다(G11).** Cl/P 비 2.45–3.55 는 **표면 농축비**이지 전환율이 아니다.
   SXRD Rietveld(tables S2–S5)가 LiCl 상분율을 줬을 것이지만 SI 미확보다.
   `[해석]` **이 한 숫자가 이 논문에서 가장 아쉬운 공백이다** — 그것이 있어야 "SE 를 얼마나
   태웠나" 와 "그 대가로 얼마를 벌었나" 를 같은 저울에 올릴 수 있다.

## 9. 비판

### 비판 1 — ★★ "분리(segregation)" 인가 "분해(decomposition)" 인가, 그리고 탄소 대조군의 부재

저자 자신이 LiCl 을 `[인쇄]` "**a major electrochemical decomposition component of LPSCl**
(35, 36)" 이라고 쓴다. 즉 **이 논문이 이득이라 부르는 생성물은 이 분야가 열화 산물이라 불러 온
바로 그 물질이다.** 이름을 "분리" 로 바꾸는 것 자체는 정당할 수 있다 — 자발적 분해가 아니라
공정으로 제어된 위치에 만들어졌다면 설계다. **그러나 그 구분을 뒷받침할 대조군이 하나 빠졌다.**

- 저자들의 "황 없는" 대조는 **LPSCl + 탄소**다(fig. S14). **LPSCl 단독 가열 대조가 없다.**
- 그리고 저자들이 인용하는 ref 39 가 바로 **"탄소가 황화물 SE 분해를 가속한다"**(Ohno/Zeier)다.
- EELS 는 계면에 `[인쇄]` "**Li- and Cl-deficient Li-P-S phase**" 가 생겼다고 말한다 — Cl 만
  빠진 것이 아니라 **Li 도 빠졌다.** 그건 분해의 서술이다.
- XPS 로 `[인쇄]` "severe collapse of LPSCl to form **Li3P**" 는 배제했지만, Li3P 가 없다는 것이
  분해가 없다는 뜻은 아니다.

`[해석]` **필요한 대조는 LPSCl 단독(무탄소·무활물질) 2000 rpm 5 h 다.** 그것 없이는
"할로겐 분리" 와 "탄소가 촉진한 LPSCl 열분해" 를 가를 수 없다. 이 위키에 옮길 때는
**"기전은 둘 중 하나로 아직 못 가른다" 로 적는다.**

### 비판 2 — 할로겐 없는 대조 SE 의 교란

Fig. 3F 가 이 논문의 가장 강한 대조군인데, 고른 할로겐 없는 SE 가 **LGPS(Li10GeP2S12)** 와
**SS7**(정의 없음, G14)이다. LGPS 의 Ge⁴⁺ 가 황화물계에서 전기화학적으로 불안정하다는 것은
별개로 알려져 있다. 저자들은 `[인쇄]` "이온전도도는 비슷하다"(fig. S42)로 **전도도 교란만**
지웠고, **전기화학 안정창 교란은 지우지 않았다.** `[해석]` **"할로겐이 있어서 좋다" 와
"LGPS 가 원래 나쁘다" 가 분리되지 않는다.** 더 좋은 대조는 **같은 아지로다이트 골격의 할로겐
없는 조성**(예: Li7PS6)이었을 것이다.

### 비판 3 — "utilization close to 100 %" 와 "이론 초과 용량" 의 동거

초록은 `[인쇄]` "utilization **close to 100 %**" 라고 쓰고, 본문 §Electrochemical performance 끝은
`[인쇄]` 칼코겐 양극들이 **"greater capacity than their theoretical capacity limits"** 를 낸다고
쓴다. **두 문장이 같은 셀을 말한다.** 이용률이 100 %를 넘으면 그 수는 더 이상 이용률이 아니다.

`[재현]` 우리 계산으로 **Te 셀은 ≈179 %, Se 셀은 ≈136 %, S 셀 최고점은 ≈117 %** 다.
Te 셀은 **용량의 약 44 % 가 활물질 밖에서 온다.** 그 셀을 "high utilization, stable cycling" 으로
요약하는 것은 정보를 잃는 요약이다. `[해석]` 저자들은 이 사실을 **숨기지 않았다**(table S6 로
따로 정리까지 했다) — 그 점은 정직하다. **문제는 초록이 그 단서를 달지 않는다는 것이고,
이 논문을 인용하는 2차 문헌이 "100 % 이용률" 만 가져갈 것이라는 점이다.**

### 비판 4 — 핵심 주장 셋이 전부 숫자 없이 형용사로 끝난다

| 초록의 주장 | 본문의 근거 | 숫자 |
|---|---|---|
| "substantially boost **effective ion transport**" | fig. S36 | **196배** 하나뿐 — 절대값·방법·분모 없음 (G8) |
| "**suppress the volume change**" | figs. S37, S50 | ★ **하나도 없다** (G10) |
| "**extraordinary cycling stability**" | Fig. 3 | 있다 — 다만 n 표기·오차막대 없음 (G13), 전부 0.1–0.33 C |

### 비판 5 — 유지율의 분모와 봉우리 (§4.2 재언급)

`[인쇄]` "98.9 % 유지" 는 **1사이클 6.28 → 100사이클 6.21** 의 양끝 비교다. `[도표]` 그 사이에
**≈7.85 까지 올랐다가 내려온다.** 봉우리 대비로 다시 계산하면 `[재현]` **6.21/7.85 = 79.1 %** 다.
같은 그림의 450사이클 셀(Fig. 3D)이 1사이클 대비 80 % 인 것과 **우연히 같은 수**가 된다.
`[해석]` **용량이 오르는 구간이 있는 셀에서 "1사이클 대비 유지율" 은 과대평가다** —
이 위키가 `zhangj2026` 에서 같은 문제를 이미 적었다(분모가 첫 사이클이 아니라 활성화 후).

### 비판 6 — 재현 가능성

§2 의 결론을 비판으로 다시 적는다. **본문만으로는 이 논문을 재현할 수 없다.** 장비 종류조차
알 수 없다(G1). 혼합이 결과를 지배한다는 것이 논문의 논지인데 그 혼합의 기술이 두 숫자다.
SI 를 확보하면 상당 부분 해소될 수 있으므로 **이 비판은 조건부**로 기록한다.

## 10. 우리 연구와의 접점 — 이식 가능 / 불가

### 10.1 이식 가능

| 가져올 것 | 어떻게 | 왜 값싼가 |
|---|---|---|
| ★★ **혼합 속도·시간 스캔을 "조성 최적화" 와 같은 급의 실험으로 승격** | 우리 one-step 셀에서 **같은 조성·같은 로딩**으로 혼합 시간만 3점(짧게/표준/길게) | 재료비 추가 0. 이 논문은 그 축 하나로 **0.55 → 7.85 mAh cm⁻² (14배)** 를 만든다 |
| ★★ **"혼합 후 XRD/Raman 으로 상을 확인한다" 를 기본 절차로** | 밀링 후 복합분말을 그대로 XRD — LiCl(111)·(200) 과 LPSCl 피크 강도·격자상수 a 를 본다 | 우리는 이미 XRD 를 쓴다. **LiCl 피크를 찾는 눈만 추가하면 된다** |
| ★ **무밀링 손혼합 대조 + 가열전용 대조** | 손혼합 셀과 손혼합 후 145 °C 3 h 셀 | 셀 2개. 이 위키에 **그 대조가 한 번도 없었다** |
| ★ **과혼합 쪽 절벽을 확인** | 표준의 2배 시간 시료 1점 | 10 h 에서 SE 결정구조가 무너진다는 경고 |
| **운전 압력 스캔을 ~70 / 36 / 18 MPa 로** | 이미 [[operating-stack-pressure-floor]] 에 축이 있다 | 이 논문이 세 점을 준다(수치는 SI) |
| **이론 초과 용량이 나오면 SE 기여를 먼저 의심** | 초과분을 **면적용량으로** 환산해 활물질 종류와 무관한지 본다 (§4.7 방법) | 계산만으로 된다 |

### 10.2 이식 불가 — 이 논문이 우리 질문에 답하지 않는 것

| 못 가져오는 것 | 이유 |
|---|---|
| ★★ **Li2S 첫 충전 활성화에 관한 어떤 것도** | 활물질이 S8/Se/SeS2/Te 다. **셀이 충전상태에서 출발**해 첫 스텝이 방전이다. 활성화 과전위·첫 충전 용량·plateau 모양이라는 양이 **존재하지 않는다** |
| **anode-free 관련 어떤 것도** | 음극이 Li–In(또는 Li 금속). N/P·Li 재고 언급 없음 |
| **2000 rpm 공정 자체** | 장비를 모른다(G1). 우리 유성볼밀로 2000 rpm 은 낼 수 없다 |
| **"nanocrystalline Li2Se 10 nm" 를 Li2S 로** | 다른 물질이고, 저자들도 Li2S 로는 같은 TEM 을 못 했다고 밝힌다 |
| **σ·D 수치** | 절대값이 하나도 없다(G8·G9) |
| **부피변화 수치** | 없다(G10) |
| **전압 환산** | 전부 vs Li–In. 이 위키에 오프셋 근거 raw 가 없어 **환산하지 않는다** |

### 10.3 ★ 질문 카드 라우팅 제안 (이 작업 범위에서는 **제안만** — 카드 편집 없음)

**[[reference-cell-500-600-mahg]] — H2b (이온 네트워크: 밀링을 겪은 SE 가 아직 superionic 인가)**

- ★★ **For 와 Against 를 같은 논문이 동시에 준다. 부호는 뒤집히지 않고 질문이 둘로 쪼개진다.**
  - **For**: `[인쇄]` "the ionic conductivity of bulk LPSCl SSEs **decreased** along with the time
    of UHS mixing" — **밀링이 SE 자신의 이온전도도를 떨어뜨린다는 것을 저자들이 명시한다.**
    `[인쇄]` 10 h 에서는 **LPSCl 결정구조가 붕괴**(fig. S35)하고 셀이 100사이클에 ≈2.3 mAh cm⁻²
    로 무너진다. 그리고 SXRD 로 5 h 시료의 **결정자 크기와 격자상수 a 가 둘 다 감소**한다.
    → H2b 가 걱정하는 일은 **실제로 일어나고 측정됐다.**
  - **Against**: 같은 문장 뒤쪽 — **복합양극의 Li⁺ 확산계수는 올라간다**(400 rpm 대비 196배).
    즉 **"SE 상이 나빠진다" 와 "복합양극의 유효 수송이 나빠진다" 는 같은 명제가 아니다.**
  - ★ **그래서 H2b 를 다시 쓸 것을 제안한다**: *"밀링을 겪은 SE 가 아직 superionic 인가"* →
    **"복합양극의 유효 Li⁺ 수송은 (a) SE 상의 벌크 전도도와 (b) 밀링이 만든 계면상의 합이고,
    둘은 혼합 강도에 대해 반대 부호다. 우리 조건은 그 합의 어느 쪽에 있는가"**.
    이 논문은 **합이 최대가 되는 중간점이 존재한다**는 것을 1/5/10 h 세 점으로 보였다.
  - 기존 For 근거(Kim 2025 의 σ_Li⁺ 0.07 → 0.42 mS cm⁻¹ 6배 · Young's modulus 21.98 → 4.63 GPa)와
    **모순되지 않는다** — Kim 2025 도 "혼합 이력이 복합양극 σ 를 바꾼다" 였고 방향이 같다.
- **신뢰도 주의**: 196배는 **분모가 망가진 대조군**일 수 있다(§6). **부호만 쓰고 배수는 쓰지 않는다.**

**[[one-step-vs-two-step-mixing]]**

- ★ **one-step 쪽에 강한 근거를 하나 추가한다.** 이 논문은 **명시적으로 one-step** 이고
  (`[인쇄]` "one-step UHS mixing of raw sulfur, LPSCl, and conductive carbon"),
  **one-step 이기 때문에** SE 와 활물질이 같은 용기에서 갈려 계면층이 만들어진다.
  two-step(SE 를 나중에 mild 하게 넣는 경로)으로는 **이 기전이 작동하지 않을 것**이다.
  → `[해석]` **"two-step 은 SE 를 고에너지에서 보호한다" 는 two-step 의 장점 서술이,
  이 논문 기준으로는 "계면 LiCl 을 포기한다" 는 비용 서술이 된다.** 카드의 가설 비교표에
  이 항을 추가할 것을 제안한다.
- 단 **활물질이 Li2S 가 아니므로** 우리 one-step 셀에 그대로 적용되지 않는다. Li2S 는 **환원제**라
  LPSCl 과의 반응 방향이 S8 과 다르다(`park2026` 의 Raman 425 → 418 cm⁻¹ 가 그 증거).

**[[operating-stack-pressure-floor]]**

- 운전 압력 좌표 **3점 추가**: **~70 MPa(표준) · 36 MPa · 18 MPa**(fig. S40, 수치 미확보).
  `[인쇄]` 저압에서도 "high capacity retention" 이라고만 적혀 있어 **값 없는 좌표**다.
  기존 좌표(0 / 1→75 스캔 / 7 / 15·30·100 / 50×3 / 150 / 200 MPa)에 70 과 36·18 이 들어간다.
- ★ **성형압은 없다(G6).** 이 카드가 요구하는 "성형압 vs 운전압 분리" 를 이 논문은 반만 채운다.

**[[composite-cathode-mixing-routes]]** (comparisons)

- ★★ **여섯째 경로 "반응성 밀링(in-situ 치환)" 의 정의를 넓힐 것을 제안한다.**
  - 지금 정의: *첨가제(FeCl3)를 함께 밀어 활물질을 치환 합성* (`hao2025`·`feng2026`).
  - 이 논문이 보이는 것: **첨가제 없이도, 활물질이 아니라 SE 쪽이 반응한다.**
  - → `[해석]` **"반응성 밀링" 은 예외적 경로가 아니라 one-step 고에너지 혼합의 기본값일 수
    있다.** 다만 **"기본값" 이라고 단정할 근거는 아직 이 한 편**이고, 이 논문의 400 rpm·1 h
    대조는 **임계 에너지 아래에서는 반응이 안 일어난다**는 것도 같이 보인다.
    → 제안 문구: 경로 ⑥을 **"반응성 밀링 — (a) 첨가제 치환형, (b) SE 분해/재증착형"** 으로
    두 갈래로 적고, (b)는 **에너지 임계가 있다**(400 rpm·1 h 에서는 안 생김)고 명시한다.
  - ★ **기록 양식의 "밀링 후 XRD 로 확인한 상" 칸이 왜 필요한지를 입증하는 논문**이다.
- **ball milling 전수 대조표**에 §2.5 의 행을 추가 (24편째).

**[[dc-polarization-conductivity-separation]]** (concept)

- `[해석]` **반례로서 추가할 가치가 있다** — 이 논문은 수송 개선을 주장하면서 **σ 가 아니라 D 를**,
  **절대값 없이 배수로만**, **측정 조건 없이** 보고한다. "무엇을 보고해야 하는가" 의 음성 사례다.

**[[capacity-normalization-li2s-vs-sulfur]]** (concept)

- **이론 초과 용량 사례 추가** (§4.7). ★ 이 위키 최초로 **초과분을 면적용량으로 환산하면
  활물질 종류와 무관하게 ≈0.8–1.5 mAh cm⁻² 로 모인다**는 분석을 제공한다 —
  **SE 기여를 분리하는 새 방법**이다.

**[[interface-quality-not-bulk-conductivity]]** (synthesis)

- ★★ **이 논문은 이 synthesis 의 thesis 를 가장 직접적으로 지지하는 근거다.**
  `[인쇄]` fig. S42 에서 **모든 SE 의 벌크 이온전도도가 비슷한데도** 할로겐 유무로
  셀 성능이 ≈1.1 vs ≈7.8 mAh cm⁻² (7배)로 갈린다. **벌크 전도도가 같은데 성능이 갈린다** —
  이보다 깨끗한 형태의 근거는 드물다. (단 비판 2 의 교란을 함께 적는다.)

### 10.4 가장 값싼 다음 실험 (이 논문에서 나온 것)

1. ★★ **우리 one-step 복합분말을 그대로 XRD 에 걸어 LiCl(200)/LPSCl 피크비를 본다.**
   셀을 만들 필요도 없다. **LiCl 이 이미 생기고 있는지**를 하루 안에 안다.
   `[해석]` 우리 LPSCl 은 전량 밀링을 겪으므로 **생기고 있을 가능성이 높다** — 생기고 있다면
   우리 "열화" 서사의 일부는 "이미 일어난 계면 설계" 일 수 있다.
2. ★ **혼합 시간 3점(½배 / 표준 / 2배) × 같은 조성**으로 셀 3개 + 분말 XRD 3개.
   이 논문의 1/5/10 h 가 보인 **봉우리 모양**이 우리 조건에도 있는지.
3. **손혼합 대조 셀 1개** — 밀링 없이 같은 조성. 우리 셀의 용량 중 얼마가 밀링 덕인지.
4. **라만으로 PS₄³⁻ 위치(425 vs 418 cm⁻¹)를 혼합 시간별로** — `park2026` 의 관측과 이 논문의
   관측이 같은 축에서 만나는지.

## 11. 이 저장소가 가져갈 것 (요약)

1. ★★ **"밀링은 분산 공정이 아니라 계면 합성 공정이다" 가 *Science* 본문의 주장이 되었다.**
   이 위키가 23편에서 귀납한 명제를 외부가 독립적으로 세웠다.
2. ★★ **H2b 는 부호가 뒤집히지 않고 둘로 쪼개진다** — 벌크 SE σ ↓ (For) / 복합양극 유효 수송 ↑
   (Against). **같은 논문, 같은 문장.**
3. ★ **혼합 강도에는 임계와 절벽이 둘 다 있다.** 400 rpm·1 h 아래에서는 아무 일도 안 일어나고,
   10 h 위에서는 SE 가 무너진다. **최적점이 존재한다**는 것이 1/5/10 h 로 보였다.
4. ★ **무밀링·가열전용 대조군의 선례.** 이 위키 24편 중 유일. 우리 실험 설계에 그대로 쓴다.
5. **첨가제 없는 계면 전략의 무게 회계** — 대가는 질량이 아니라 SE 기능이고, 상한은 **LPSCl 질량의
   15.80 %** `[재현]`.
6. **이론 초과 용량의 새 분리법** — 초과분을 면적용량으로 환산해 활물질 무관성을 본다.
7. **반면교사**: 핵심 주장 셋 중 둘(이온 수송·부피변화)이 **본문에 숫자가 없다**.
   우리 보고에서 같은 일을 하지 않는다.

## 12. 그림 판독 기록 — 무엇을 보고 무엇을 안 봤나

| 그림 | 파일 | 실제로 Read 했나 | 이 digest 에서 무엇을 읽었나 |
|---|---|---|---|
| **Fig. 1** (구조 분석) | `fig_1.png` | ✅ **보았다** | 1E 의 Cl:P 정량 6+2 개 전부, 1D 라인스캔 폭, 1F EELS 온셋 166.6/168.6 eV, 1G SXRD 2θ 와 지수 |
| **Fig. 2** (cryo-TEM 보편성) | `fig_2.png` | ✅ **보았다** | 2C 의 Cl/P·Br/P 6개 전부, 2D LiCl-rich 띠 폭, 2F·2G 격자간격 6개, 2H FFT 각도 |
| **Fig. 3** (전기화학) | `fig_3.png` + 600 dpi 재확대(3A·3B·3E·3F) | ✅ **보았다 (가장 꼼꼼히)** | ★ 3A 의 **봉우리 ≈7.85**, 1 h·10 h 궤적, 3B 의 ΔV 변화, 3C·3D 유지율 선, 3E 칼코겐 3종, 3F SE 7종 |
| **Fig. 4** (사후분석) | `fig_4.png` | ✅ **보았다** — ⚠ **최초 크롭이 캡션 앵커 때문에 A–C 를 잘라먹어(2217×571) 페이지 전폭으로 재크롭했다**(1559×1542). `figures.json` 의 `note` 참조 | 4A XANES 적층, 4B·4C in situ Se 컨투어, 4F Li2Se 격자, 4G SAED 적분, 4I 100사이클 Cl:P 3개 |
| **fig. S1–S50 전부** | — | ❌ **못 봤다 — SI 미확보** | 특히 **S36(확산계수) · S37(스택압) · S40(저압) · S42(SE 전도도) · S50(µ-CT)** 가 이 digest 의 핵심 공백이다 |
| **Tables S1–S6** | — | ❌ **못 봤다** | **S6(이론용량 한계)** 와 **S2–S5(Rietveld)** 가 §8 의 전환율 공백을 메울 자리다 |
| **Movies S1–S2** | — | ❌ **못 봤다** | in situ 가열 TEM |

**본문 텍스트는 7쪽 전량을 덤프해 읽었다** (40,105 바이트). 참고문헌 42개, 저자 기여, 자금,
이해상충까지 포함.

### 원문 내부 불일치 / 표기 문제

| # | 내용 |
|---|---|
| 1 | `[인쇄]` **"Li6PSCl0.9I0.1(LPSClI)"** — S 의 아래첨자 5 가 빠져 있다 (G15) |
| 2 | `[인쇄]` 초록 "utilization **close to 100 %**" vs 본문 "greater capacity than their **theoretical capacity limits**" — 같은 셀에 대한 두 서술 (비판 3) |
| 3 | `[인쇄]` "98.9 % 유지" 와 `[도표]` 그림의 봉우리 ≈7.85 mAh cm⁻² (비판 5) |
| 4 | **SS7** 이 Fig. 3F 범례에만 나오고 정의가 없다 (G14) |
| 5 | Fig. 4B 전압축(3/2/1 V)과 Fig. 3B 전압축(0.4–2.3 V vs Li–In)의 기준이 다르거나 불명 (G16) |
| 6 | `[인쇄]` 100사이클 후 Cl/P 가 "pristine 과 close" 라는데 `[도표]` 1.86·1.78 → 1.33–1.56 으로 **15–25 % 감소** (§5.4) |

## 관련 페이지

[[composite-cathode-mixing-routes]] · [[one-step-vs-two-step-mixing]] ·
[[reference-cell-500-600-mahg]] · [[operating-stack-pressure-floor]] ·
[[mixing-equipment-ball-mill-thinky]] · [[dc-polarization-conductivity-separation]] ·
[[capacity-normalization-li2s-vs-sulfur]] · [[interface-quality-not-bulk-conductivity]] ·
[[li2s-assb-composite-cathode]] · [[carbon-dimensionality-electron-network]]
