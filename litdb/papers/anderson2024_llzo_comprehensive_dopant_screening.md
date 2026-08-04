# Comprehensive Dopant Screening in Li₇La₃Zr₂O₁₂ Garnet Solid Electrolyte — Anderson/McCalla (Adv. Energy Mater. 2024)

> slug `anderson2024_llzo_comprehensive_dopant_screening` · DOI `10.1002/aenm.202304025` · type `exp (HT combinatorial synthesis + PXRD/Rietveld + EIS + DC σ_e + CV-ESW + CCD; 자체 계산 0)` · PDF 본문 `0d1f9207-51.…pdf`(12 pp) + SI `911157c5-51._Sup…pdf`(17 pp) · digested `2026-07-28` · **2차 패스(본문 그림 픽셀 독립 검증) `2026-08-04` → §19** · **3차 패스(SI PDF 직접 재판독, §19.5 확정) `2026-08-04` → §20** · status ✅ (본문 12 pp + SI 17 pp 전수 정독, **3중 검증 완료**)
> elements: Li, La, Zr, O, B, Al, Fe, Zn, Ga, Na, K, Ca, Rb, Sr, Y, Ag, Cs, Ba, Pr, Nd, Sm, Gd, Tb, Dy, Ho, Er, Tm, Yb, Lu, Bi, Mg, Si, P, Sc, Ti, V, Cr, Mn, Co, Ni, Cu, Ge, Se, Nb, Mo, Ru, Rh, Pd, Cd, In, Sn, Ce, Eu, Hf, Ta, W, Re, Ir, Pt, Au, Tl, Pb, Te
> methods: ESW
>
> **저자** Ethan Anderson, Elliot Zolfaghar, Antranik Jonderian, Rustam Z. Khaliullin, **Eric McCalla\*** — Department of Chemistry, **McGill University**, Montreal H3A 0B8, Canada
> Received 2023-11-24 · Revised 2024-01-29 · Published online **2024-04-16** · Adv. Energy Mater. **2024**, 14, 2304025
> **Open Access (CC BY)** · 자금 New Frontiers Research Fund + NSERC Discovery ×2 · 이해상충 없음 선언
> `db/properties/nd_substitution_survey_index.json` **037번** · system_class `garnet_Li`
>
> ⚠⚠ **산화물 가넷(비-argyrodite)이다.** LLZO = Li₇La₃Zr₂O₁₂. 우리는 황화물 argyrodite.
> **절대값·컷 값을 우리 문맥으로 이식 금지.** 이식 가능한 것은 **방법·논증 구조**이지 숫자가 아니다.
> ⚠ **methods 태그가 `ESW` 하나뿐인 것은 실수가 아니다** — 이 논문은 자체 DFT/AIMD/BVSE를 **하나도 하지 않는다**
> (§4.4 참조). 계산은 전부 **문헌 승계**(Miara 2015 결함에너지 · 자체 선행연구의 bond-valence mismatch).
>
> ### 🔴 인용 전 필독 — 2026-08-04 2차(§19)·3차(§20) 패스 결과 요약
> 1. **세 경로가 서로를 독립 검증했다** — ①1차 SI 손전사 · ②2차 본문 그림 픽셀 역판독 ·
>    ③3차 SI PDF 텍스트 레이어 자동 파싱. garnet%/cubic% 잔차 중앙값 0.03/0.15 pp, σ_i 1.06×.
>    이 논문 수치는 우리 litdb에서 **세 경로로 확인된 유일한 데이터셋**이다.
> 2. ✅ **§19.5의 4칸 미해결이 §20에서 전부 확정됐다 — 인용 금지 해제.**
>    - **`Rh`·`Ho`는 애초에 논문 문제가 아니었다** — 1차 digest가 `Ho`를 `Rh`로 잘못 적은 **우리 오타**.
>      그림과 SI는 처음부터 일치한다(Rh 2.58×10⁻⁶ = undoped 1.6× · Ho 1.57×10⁻⁵ = 9.7×).
>    - **`Y`·`Yb`는 논문 자체의 오류** — **Fig 4a·4b가 Y와 Yb 칸을 맞바꿔 실었다**.
>      **Table S5 + Fig 3이 채택**: **Y(La) σ_i 2.46×10⁻⁵ · σ_e 3.14×10⁻⁸ (측정됨) / Yb(La) σ 미측정.**
>      → "고전압 passivation 최강군 Sc·Y·Dy·Er" 서사는 이제 **Y의 σ까지 갖춰 쓸 수 있다**(§20.2).
> 3. 🔧 **§6 교정**: 본문 "36종이 >10×"는 **엄격히는 35종**이고, 36번째는 **Ho(9.7×)를 반올림해 넣은 것**.
>    1차 digest의 36종 목록에서 **Rh를 빼고 Ho를 넣어야 한다**(§20.3).
> 4. 🔧 **§5b 교정 2건**: "선호 site는 대부분 >90 % cubic" → 실측 **42 %뿐**(중앙값 **75.1 %**, 이제
>    그림이 아니라 **SI 표 자체로 확정**) · 미동정 2차상 6종의 **"Ga"는 `Ge` 오기**(§19.3a, §19.6, §20.4).
> 5. ✅ **핵심 긍정 결과는 더 단단해졌다**: 예측 site가 3자리 중 cubic% 1위 = **49/51 (96 %)**.
>    반면 서술자 *크기* 는 cubic%를 전혀 예측 못 한다(**ρ ≈ 0**), BV↔DFT 자리 일치율은 **51 %**(§19.4).
> 6. ✅ **§3e의 "5컷 순차 게이트 → 생존자 0"이 SI 표로 재실행돼 그대로 재현**: 59 → 19 → 6 → **1(Ga)** → **0**(§20.5).

---

## 0. 이 digest를 읽는 법 (우리 캠페인에서의 위치) ★★★

**우리 `tools/cascade/`(argyrodite host × 47 도펀트 다축 스크리닝)의 가넷판이자, 그 *실험* 버전이다.**
문헌 통틀어 "한 host에 수십 종 도펀트를 **동일 합성·동일 측정 조건**으로 넣고 **다축**으로 재본" 사례는
드물고, 그중 우리 설계와 1:1로 대조 가능한 건 사실상 이것뿐이다.

계보 위치:
- `xiao2019_cathode_coating_screening` = 게이트식 HT **계산** 깔때기의 원형 (10⁵종 → 3종)
- `kim2026_hts_li3sc2po43_coating_midni_ncm` = 그 후속 (17,230 → 1종), 우리 cascade의 최근접 계산 대조군
- **이 논문 = 같은 문제(다축 도펀트 선별)를 *실험*으로, 그리고 *깔때기를 쓰지 않고* 푼 사례**

**이 digest의 최대 발견은 §3e다**: 이 논문은 깔때기 숫자를 보고하지 않는다. 그런데
**논문 자신이 SI Table S5 캡션에 명시한 5개 merit 기준을 순차 게이트로 걸어보면 최종 생존자가 0종**이다.
즉 이 논문이 깔때기를 안 쓴 것은 스타일이 아니라 **쓸 수 없어서**다 — 그리고 저자들은 그 대신
전수 매트릭스 + 축별 merit flag + **codoping으로 넘기기**를 선택했다. 우리 가중 score 설계의
가장 강력한 외부 방어 논거이자, 동시에 "우리 G5 하나가 최종을 지배한다"는 우리 자기비판의 거울이다.

---

## 1. 한 줄 요약

**59종 원소를 Li/La/Zr 세 자리에 각각 0.2 atom/f.u. 로 넣은 177개 LLZO 시료를 sol–gel HT 합성으로
한 번에 만들고**, 구조(PXRD/Rietveld) · 이온전도(EIS) · 전자전도(DC) · 고전압/저전압 ESW(CV) ·
CCD(대칭셀) · 1년 대기 안정성을 **동일 조건으로 전수 측정**해서, ① 도펀트를 **문헌 DFT 결함에너지
(또는 훨씬 싼 bond-valence mismatch)가 예측한 최적 자리**에 넣으면 입방상(c-LLZO)이 촉진되고,
② **36종이 undoped 대비 σ >10배**(최대 Ga/Fe 1.2×10⁻³ S/cm), ③ 전자전도는 도핑으로 대체로
**낮아지지만 Co/Ru/Cu/Ir는 올라가 dendrite 위험**, ④ **고전압 한계는 59종 전부 3.8–3.9 V로 사실상 불변**
이고 바뀌는 것은 **분해 전하량(=passivation 품질)**, ⑤ **저전압 한계는 33종이 <0.1 V까지 내려가고**
CCD와 **강하게 상관**(σ_e와는 무상관) — 이라는 6축 지도를 그린 뒤,
**"단일 도펀트로는 전부 못 얻는다 → codoping 지도로 가라"**로 끝맺는다.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자/기관 | Anderson, Zolfaghar, Jonderian, Khaliullin, **McCalla\*** (McGill Univ., Chemistry) |
| 저널 | Adv. Energy Mater. **2024**, 14, 2304025 (12 pp 본문 + 17 pp SI) |
| DOI | 10.1002/aenm.202304025 (Open Access, CC BY) |
| 유형 | **순수 실험 HT 조합 스크리닝**. 자체 DFT/MD **0건**. 계산은 문헌 승계(§4.4) |
| 물질 | **Li₇La₃Zr₂O₁₂ (LLZO)** 가넷. t-LLZO(I4₁/acd, 저전도) ↔ c-LLZO(Ia-3d, 고전도), 일부 I-4̄3d |
| 도펀트 풀 | **59종** (신규 29 + 기보고 30). Fig 1 주기율표 = 노랑(신규)/파랑(기보고)/빨강(host Li·Zr·La·O) |
| 조성 | 도펀트 **0.2 atom/f.u.** 고정, **Li 8.4 dispensed**(=7×1.2, 소결 Li 손실 보상). 자리별 Li8.4/La3/Zr2 · Li8.4/La2.8/Zr2 · Li8.4/La3/Zr1.8 (Table S2) |
| 시료 수 | 59 × 3 자리 = **177** 도핑 시료 (+ 세트별 undoped → PXRD 패턴 **180**장) |
| 측정 6축 | 상(garnet%/cubic%) · σ_i · σ_e · V_max(고전압) & ∫Idt(분해량) · V_min(저전압) · CCD · (+1년 대기) |
| 핵심 질문 | "도펀트 하나하나가 LLZO의 *어느 물성*을 어떻게 바꾸는가"를 **같은 조건에서 전수**로 알면, codoping을 합리적으로 설계할 수 있는가? |
| 선행 대비 | 기존 30종은 "대부분 σ_i만" 보고 + 합성법·농도가 제각각 → **직접 비교 불가**. 이 논문이 처음으로 동일 조건·다축 |

---

## 3. 스크리닝 설계 ★★★ — "깔때기가 없는 스크리닝"

### 3a. 풀: 왜 59종인가 (우리 47종 `pool_provenance`와 정면 대조)

논문의 풀 출처는 **명시적이고 문헌 기반**이다 (Introduction):
- **기보고 30종** — "To date, 30 different dopants have been reported in LLZO."
- **계산 예측 45종** — ref [12] = **Miara/Richards/Wang/Ceder, Chem. Mater. 2015, 27, 4040**이
  "LLZO가 이론적으로 추가 45종을 수용할 수 있다"고 예측. 그 예측 명단이 신규 후보의 원천.
- 실제 실행 = 신규 29 + 기보고 30 = **59**. **Sb는 Fig 1에 표시돼 있으나 실측 제외**(본문 명시).

> 🔑 **우리와의 결정적 차이**: 그들의 풀 = "선행 실험(30) ∪ 선행 DFT 예측(45)"이라는 **문헌 정의 집합**.
> 우리 47 = **사람이 큐레이션한 화학적 후보군**(코팅 문헌·전구체·발란스 다양성)이고, 91→47은
> 물리 게이트가 아니라 **파이프라인 탈락**(`pool_provenance.attrition_is_not_screening`).
> **양쪽 다 "전수 DB 스캔의 잔존군"이 아니다** — 이 점은 같다. 다만 그들은 풀 출처를 한 문장으로
> 방어할 수 있고, 우리는 JSON 블록으로 길게 해명해야 한다. **풀 정의의 문헌적 방어가능성은 그들이 우위.**
> 반대로 **"어디서 왜 몇 종이 빠졌는가"의 회계는 우리만 있다** — 그들은 Sb 제외 사유를 쓰지 않았고,
> σ_i/σ_e 결측 5종(Er·Mo·Tb·Te·Yb)의 사유도 표에 공란으로만 남긴다(§17.9).

### 3b. 치환 자리 — **세 자리 전부, 전수** (우리와 가장 큰 설계 차이)

**Li⁺ · La³⁺ · Zr⁴⁺ 세 자리에 같은 도펀트를 각각 따로 넣어 3벌 만든다.** 자리를 가정하지 않는다.
그다음 "**최적 자리**"를 두 가지 값싼 예측자로 지정하고, 본문의 물성 논의는 **최적 자리 시료만** 쓴다:

1. **DFT 결함에너지** — Fig 3d, ref [12](Miara 2015, Ceder 그룹) **인용값**. 도펀트별 Li/La/Zr 자리
   결함에너지 3점, 최소값을 주는 자리 = 최적 자리. 일부 원소는 산화수 첨자 표기(예 Fe3, V5, Ce4, Ta5;
   figure-read). **Lu는 `n/a`**(ref [12]에 값 없음).
2. **Bond valence mismatch** — Fig 3c, 방법은 ref [35](Jia/…/McCalla, Chem. Mater. 2022, 34, 11047)
   = **자기 선행연구**. 값은 0~5 범위. **⚠ 이것은 우리 BVSE(Li 이동 에너지 지형)가 아니라
   "이 자리에 이 이온을 넣으면 결합가가 얼마나 안 맞는가"의 *자리 적합도* 지표다.** 이름만 비슷하고
   측정 대상이 다르다(§4.4, §20).

**논문의 방법론적 주장**(초록): *"doping on the optimum site predicted from either previous DFT
calculations or the far cheaper bond valence calculations promotes the cubic phase."*
→ **비싼 DFT ≈ 싼 BV mismatch** 로 자리 예측이 대체 가능하다. 단 본문 자인:
*"they have difficulty differentiating between tetrahedral (Li) and octahedral (Zr) site preference."*
(사면체 Li vs 팔면체 Zr 구별은 BV로 안 된다.)

> 🔑 **우리 대비**: 우리 cascade는 도펀트를 **P 자리·간극 등으로 배치 탐색**하되, 자리 결정은
> 도펀트별 배치 앙상블(Nd₂O₃ 342 configs → cfg141, `kb/methodology/dopant_screening_funnel_2026_06_13.md`)
> 로 **내부 최소 에너지**를 찾는다 = "자리를 계산으로 고른다". 그들은 **세 자리를 다 만들어 실험으로 확인**한다.
> 우리는 자리 선택을 **에너지 최소화 1축**에 맡기고, 그들은 **합성 결과(상순도·입방상 함량)**로 검증한다.
> → **우리가 이식할 것: "자리 예측 ≠ 자리 검증"의 분리.** 우리 cfg 선택이 옳았는지 검증하는 독립 관측량
> (그들에겐 c-LLZO 함량)이 우리에겐 없다.

### 3c. 평가 축 — 6축, 각 축의 방법

| 축 | 관측량 | 방법 | 정량/정성 |
|---|---|---|---|
| ① 상/구조 | garnet wt% (c+t), **cubic wt%**, 격자상수 a | Mo-Kα PXRD → **HighScore Plus 자동 batch Rietveld** | 정량 (wt%) |
| ② 이온전도 | **σ_i (total, RT)** | EIS, BioLogic SP-150, 1 MHz–1 Hz, Au 스퍼터 blocking, 등가회로 **(RW)Q**(bulk+Warburg) + **RQ**(GB) | 정량 |
| ③ 전자전도 | **σ_e** | **DC 분극**, 자체제작 pseudo-potentiostat, 0.5 V 스텝 up to 2.5 V, ohmic 구간에서 저항 산출. 검출한계 1 nA ≈ **10⁻¹⁰ S/cm** | 정량 |
| ④ 고전압 안정 | **V_max** + **∫Idt (3.8–4.3 V, mAh/g)** | LLZO 분말 + Super-P + PVDF **복합 전극** CV, **탄산에스터 액체 전해질**(1 M LiPF₆, EC:DMC 50/50), 3.5→5.5 V, 1 V/h, blank 차감 | 정량 |
| ⑤ 저전압 안정 | **V_min** | 같은 복합 전극 CV, 3.0→0.1 V. **시료 전류가 blank 아래로 꺼지는 최고 전압**으로 정의. 핵심 시료는 **이온성 액체**(0.3 M LiTFSI in BMIM(OTf), 60 °C)로 재확인 | 준정량(문턱 판독) |
| ⑥ CCD | mA/cm² | **Li/LLZO/Li Swagelok 대칭셀**, 0.05 mA/cm² 시작 → 매 사이클 +0.05, 반쪽사이클당 **0.10 mAh/cm² 고정**, 10 V 컷오프. 계면에 **소량 액체 전해질**(1 M LiPF₆ DMC/EC) 적심 | 정량(단 18종만) |
| (+) 대기 안정 | 1년 후 PXRD 변화 | RT, **상대습도 30–50 %** 실내 대기 1년 보관 후 재측정, pristine 패턴과 overlay (Fig S5–S8) | **정성만** |

### 3d. 컷 값과 그 근거 ★★★ — **논문의 컷은 SI 캡션에만 있다**

논문 본문에는 "게이트"도 "임계값"도 없다. 유일한 정량 기준은 **SI Table S5 캡션의 볼드 처리 규칙**이다:

> *"Highlighted in bold are values of particular merit (**a high cubic content >94 %**, **an ionic
> conductivity > 5×10⁻⁵ S/cm**, **an electronic conductivity < 2.5×10⁻⁸ S/cm**, **∫Idt < 1.39 mAh/g
> the value for undoped**, and **a CCD of at least 0.4 mA/cm²**)."*

| # | 컷 | 값 | **근거 분류** | 판정 |
|---|---|---|---|---|
| C1 | cubic wt% | **> 94 %** | 미제시 — 분포에서 유도한 흔적도, 문헌 승계 근거도 없음 | 🔴 **자의적** |
| C2 | σ_i | **> 5×10⁻⁵ S/cm** | 미제시. (문맥상 "실용 하한 ~10⁻⁴"과 undoped 1.6×10⁻⁶ 사이의 중간값) | 🔴 **자의적** |
| C3 | σ_e | **< 2.5×10⁻⁸ S/cm** | 미제시. 본문에 "대부분 1–5×10⁻⁸"이라 했으니 **분포 하위 절반 근처** = 사실상 로스터 상대 컷 | 🟡 **분포 유도(암묵)** |
| C4 | ∫Idt | **< 1.39 mAh/g** | ✅ **undoped LLZO 실측값 그 자체** — "host보다 나빠지지 않는가" | 🟢 **host 앵커** |
| C5 | CCD | **≥ 0.4 mA/cm²** | 미제시. 문헌 목표(1–10 mA/cm², ref [9])보다 훨씬 낮은 **자기 데이터 범위 내부** 값 | 🔴 **자의적** |

> 🔑🔑 **C4 = 우리 G1(Δe<0, host 기준)·G3(ox_V ≥ 2.14 V = undoped host onset)과 *정확히 같은 문법*이다.**
> "host 값을 컷으로 쓴다"는 발상은 우리 발명이 아니라 **이 분야의 자연스러운 관행**이라는 외부 증거.
> 반대로 C1·C2·C5는 우리 G5(로스터 median)와 같은 성격의 **자의적 컷**인데,
> **그들은 `arbitrariness_flag`에 해당하는 표시를 하지 않는다**(§14c).

**그리고 논문은 이 5개 컷을 *순차로 걸지 않는다*.** 각 물성을 독립적으로 볼드 처리할 뿐이다.

### 3e. ★★★ 재구성 깔때기 — 논문의 자기 컷을 순차로 걸면 **생존자 0**

> ⚠ **아래는 이 digest가 계산한 재구성이다. 논문에 이런 표는 없다.**
> 재료: Table S5 전 59행 (본 digest가 전수 전사, `scratchpad/tableS5.py`). Ti CCD는 **0.55**
> (Table 1 + Fig S12; Table S5 인쇄값 0.65는 오타 — §18.1).

**순차 깔때기 (C1→C2→C3→C4→C5 순):**

| 단계 | 기준 | in | pass | kill | 생존자 |
|---|---|---:|---:|---:|---|
| 0 | 풀 (도펀트 종) | — | **59** | — | 59종 전부 |
| G-a | cubic > 94 % | 59 | **19** | 40 | Al, B, Ce, Fe, Ga, Gd, Lu, Mg, Nb, Pb, Re, Ru, Sm, Sr, Tm, V, W, Y, Zn |
| G-b | σ_i > 5×10⁻⁵ | 19 | **6** | 13 | Al, Fe, Ga, Gd, Ru, W |
| G-c | σ_e < 2.5×10⁻⁸ | 6 | **1** | 5 | **Ga** |
| G-d | ∫Idt < 1.39 | 1 | **0** | 1 | — (Ga = 1.46 > 1.39) |
| G-e | CCD ≥ 0.4 | 0 | **0** | 0 | — |

**최종 생존자 = 0종.**

**게이트별 단독 선택압 (59종에 각각 단독 적용):**

| 기준 | 단독 통과 | 단독 탈락 | vacuous? |
|---|---:|---:|---|
| cubic > 94 % | 19 | 40 | ✗ (최강) |
| σ_i > 5×10⁻⁵ | 11 | 48 | ✗ |
| σ_e < 2.5×10⁻⁸ | 15 | 44 | ✗ |
| ∫Idt < 1.39 | 18 | 41 | ✗ |
| CCD ≥ 0.4 | 11 | 48 | ✗ (단 **18종만 측정** — 41종은 측정 결측으로 탈락, 물리 탈락 아님) |
| **V_max ≥ 3.9 V** (논문 컷 아님, 가상) | **56** | **3** | 🟡 **거의 vacuous** |
| **V_max ≥ 3.5 V** (가상) | **59** | **0** | 💤 **완전 vacuous** |

> 🔑 **결론 3개:**
> 1. **이 논문에 vacuous 게이트는 "있다" — 다만 게이트로 쓰이지 않았다.** V_max(고전압 열역학 한계)는
>    59종 전부 3.8–3.9 V로 **완전 축퇴**다. 만약 이걸 게이트로 걸었다면 우리 G1/G2와 같은 vacuous 판정이
>    나온다. 저자들은 대신 **∫Idt(kinetic passivation 양)**로 축을 갈아탔다 — 축퇴된 축을 버리고
>    변별력 있는 대리 관측량을 찾는 **정확한 대응**이고, **우리가 배울 점**이다(§16.2).
> 2. **논문이 깔때기를 안 쓴 이유가 데이터에 있다.** 자기 컷 5개를 순차로 걸면 0종이다. 저자들도
>    이걸 알았을 것이고, 그래서 **"단일 도펀트로는 못 한다 → codoping"**으로 결론을 옮겼다.
>    실제로 본문 결론: *"We further propose that the current paper leads to promising paths in terms of
>    codoped samples where one dopant (e.g., Ga, Fe) is used to favor the cubic phase and enhanced ionic
>    conductivity … while a combination of other dopants are used to expand the stability window
>    (e.g., selected from Ti, Sc, Dy) and further doping on the Zr and/or La site … promotes air stability."*
> 3. **이건 우리 가중 score 설계의 가장 강한 외부 방어 논거다.** 순차 boolean 깔때기는 다축 도펀트
>    문제에서 **정보 소실이 치명적**이다(우리 §14a). Xiao(10⁵→3)·Kim(17,230→1)은 **후보 풀이 워낙 커서**
>    깔때기가 성립했고, **풀이 작고 축이 서로 상충하면 깔때기는 공집합을 뱉는다** — 이 논문이 그 증명이다.

---

## 4. 방법 (Experimental Section + SI 전수)

### 4a. 합성 — HT sol–gel (자기 선행연구 ref [21] Solid State Ionics 2022, 388, 116087 승계·개량)

- **citrate sol–gel**. 전구체 수용액: **Li(NO₃)**, **La(NO₃)₃**, **Zr(OAc)₂(OH)₂** + 도펀트 전구체
  (Table S1 전량 59종 — 대부분 질산염; 예외: B(OH)₃/Si(OEt)₄는 EtOH, Ge(Oi-Pr)·Ta(OEt)₅는 무용매,
  BiO(NO₃)는 H₂O 슬러리, 염화물 SnCl₂/HfCl₄/IrCl₃/PtCl₂/TeCl₂/HAuCl₄, 그 외 H₃PO₄·H₂SeO₃·
  (NH₄)₆Mo₇O₂₄·(NH₄)₆H₂W₁₂O₄₀·(NH₄)ReO₄·(NH₄)₂Ti(C₃H₆O₃)₂·(NH₄)Nb(C₂O₄)₂·Tl(OAc)).
  모든 전구체 농도는 **ICP-OES로 확인**.
- 8×8 그리드 **350 µL 스테인리스 컵**에 micropipette 분주(총 ~330 µL), **구연산:금속 = 0.75:1**
  (본문 "0.75:1 ratio of citrate ions to metal ions") 추가.
- 120 °C 하룻밤 건조 → 단단한 foam → 분쇄 → **2단 소성**: ① 1 °C/min → 400 °C, 6 h 유지, 5 °C/min 냉각
  (질산염 분해, 갈색-검정) ② 5 °C/min → 700 °C, 6 h, 5 °C/min 냉각 → 금속산화물 분말.
  smokestack 장치로 분리·가둠.
- 유발 분쇄 ~30 s → **8×8 홈 HT 펠릿 다이**, **400 MPa 60 s** → 지름 **4.8 mm**, 두께 **~1 mm** 펠릿.
- **희생 분말(sacrificial powder)** = 같은 sol–gel로 만든 **Li₇.₅La₃Zr₂O₁₂** 로 위아래를 완전히 덮어
  알루미나판·분위기와 격리. **1050 °C 3 h**, 승온·냉각 5 °C/min.
  > 이전 연구보다 소결 온도를 **높인 것**이 개량점(본문 명시).

### 4b. 구조 — PXRD & Rietveld

- **PANalytical Empyrean**, **Mo 타깃 (60 kV, 40 mA)**, **GaliPIX** 면검출기, **4–30° 2θ**, **10분/스캔**.
- 실리콘 표준으로 보정. **HighScore Plus 자동 batch Rietveld**.
- 정련 변수: **상 함량, 격자상수, peak shape, background, sample zero**.
  ⚠ **"Neither site occupancies nor positions were refined in the garnet phases and no dopant was
  included in the [fits]."** = 일괄 정련에는 **도펀트를 아예 안 넣었다.**
- 검증: Ga(Li)·Ca(La)·W(Zr) **3개 시료만** 도펀트 자리를 명시 정련 (Table S4, Fig S1–S3):

| 시료 | 무-도펀트 GoF | Li1 | Li2 | La1 | Zr1 | **최소 GoF 자리** | a (Å) |
|---|---:|---:|---:|---:|---:|---|---:|
| Ga | 3.219 | **3.145** | 3.291 | — | — | **Li1 ✓** (마진 2.3 %) | 12.9986 |
| W | 2.713 | 3.848 | 3.017 | 2.927 | **2.150** | **Zr1 ✓** (마진 21 %) | 12.9745 |
| Ca | 3.883 | 3.836 | 3.870 | **3.630** | 4.427 | **La1 ✓** (마진 6.5 %) | 12.9853 |

  정련 점유율: Ga 시료 Li1(24) 0.2667 / Li2(96) 0.4667 / **Ga1(24) 0.0667**;
  W 시료 **Zr1 0.9 / W1 0.1**(16 site → 1.6 W/cell = 0.2/f.u. ✓); Ca 시료 **La1 0.9333 / Ca1 0.0667** ✓.
  공간군 전부 **Ia-3d**.
  > ⚠ **Ga의 판별 마진이 2.3 %밖에 안 된다** — "예측한 자리에 들어갔다"의 증거력은 W ≫ Ca > Ga.

### 4c. 전기화학

- **σ_i**: EIS BioLogic SP-150, **1 MHz → 1 Hz**, Au 스퍼터 양면, 8×8 자체제작 셀. 등가회로
  **(RW)Q** (bulk + Li 확산 Warburg) + **RQ** (grain boundary) → 보고값 = **total conductivity** (bulk+GB).
  펠릿 두께는 digital micrometer, 밀도는 **Archimedes**(Table S3: Al 4.619/0.906, Zn 4.557/0.894,
  Fe 4.576/0.897, B 4.717/0.925, Ga 4.672/0.916, Ta 4.609/0.904, Au 4.771/0.936, **Pt 4.870/0.955**;
  undoped 이론밀도 5.1 g/cm³). **상대밀도 89–96 %.**
- **σ_e**: 같은 셀 → 자체제작 pseudo-potentiostat, **0.5 V 스텝 up to 2.5 V**, ohmic 영역에서 저항.
  **1 nA (≈10⁻¹⁰ S/cm) 검출 가능**.
- **ESW (CV)**: 슬러리 = LLZO 52 mg + **Super-P 23.5 mg** + PVDF(4 mL NMP) → **6 mg 분말/60 µL 슬러리**.
  고전압용: 알루미늄 패드 인쇄 PCB 8×8에 4 µL 적하; 저전압용: 니켈 패드. 70 °C 건조 후 Ar 글러브박스.
  대극 **Li foil**, 전해질 **1 M LiPF₆ EC:DMC 50/50**, 유리섬유 분리막.
  **3.5→5.5 V** 및 **3.0→0.1 V**, **0.1 V/h**, RT. **blank(카본+바인더만) 차감.**
  일부 시료는 **Swagelok + Li foil + 0.3 M LiTFSI in BMIM(OTf) 이온성 액체, 60 °C, 3.0→0.1 V**로 재확인.
- **CCD**: **Li/LLZO/Li Swagelok**, 스프링 stack pressure(정량 미보고), Li 디스크 지름 3.4 mm,
  800 grit 샌드페이퍼. **계면에 1 M LiPF₆ DMC/EC 소량 적심**(접촉저항 극복용). Ar 분위기 조립.
  **CCCV, 반쪽사이클당 0.10 mAh/cm²**, 0.05 → +0.05 mA/cm²/cycle. 과전압 10 V 도달 시 그 사이클 종료.
  임계전류에 도달 못 하면 **"신뢰성 있게 공급된 최대 전류"를 하한(>x)으로 보고**(Fig S13/S14 노랑 화살표),
  CCD가 실제 발생하면 빨강 화살표 → 둘 사이면 **구간([a,b])으로 보고**.

### 4d. ★ 계산 — **이 논문의 자체 계산은 0이다**

| 항목 | 출처 | 성격 |
|---|---|---|
| 결함에너지 (Fig 3d) | **ref [12] = Miara, Richards, Wang, **Ceder**, Chem. Mater. 2015, 27, 4040** | **문헌 인용값**. code/functional/셀 크기/U 값 **이 논문에는 전혀 없음** |
| Bond valence mismatch (Fig 3c) | 방법 = **ref [35] = Jia, Yao, Peng, Jonderian, Abdolhosseini, **McCalla**, Chem. Mater. 2022, 34, 11047** (자기 선행연구, Na 양극계) | 값싼 경험식. 이 논문에 식·파라미터 없음 |
| band gap 3.1 eV (Ga-LLZO) | **ref [34] = Han, Zhu, He, **Mo**, C. Wang, AEM 2016, 6, 1501590** | 문헌 인용 |
| "LLZO 계산 ESW ≈3 V" | refs [12,34] | 문헌 인용 |

- **code / functional / pseudo / k-points / ecut / supercell / DFT+U / AIMD / MLIP / 무질서 처리: 전부 n/a.**
  이 논문은 DFT를 하지 않았으므로 "미공개"가 아니라 **해당 없음**이다. (Khaliullin 교수가 공저자인데도
  계산 결과는 없다 — 데이터 해석·논의 기여로 보이나 확인 불가.)
- **⚠ 우리가 이 논문을 "DFT 문헌"으로 인용하면 틀린다.** `nd_substitution_survey_index.json`의
  037번은 `system_class: garnet_Li`이고 실험 논문이다.

### 4e. Post-processing ★

- **Rietveld 정량 상분석** (HighScore Plus, 자동 batch) → wt% garnet / wt% cubic / a.
- **EIS 등가회로 피팅** ((RW)Q + RQ) → total σ_i. **bulk/GB 분리값은 보고하지 않음**.
- **CV blank 차감 + 3.8–4.3 V 전류 적분** → **∫Idt (mAh/g)** = "고전압에서 얼마나 분해됐나"의 스칼라화.
  > 🔑 **이 스칼라화가 이 논문의 방법론적 발명이다.** 축퇴된 축(V_max)을 버리고, 같은 CV에서
  > **면적 적분**이라는 변별력 있는 스칼라를 뽑아냈다.
- **V_min 판독 규칙**: "시료 곡선이 blank 아래로 꺼지는 최고 전압". 각주 `*` = "환원 피크가 매우 작아
  사실상 무시할 만함" (Al 0.7\*, Au 1\*, Ca 2.2\*, Ce 1.8\*, Pt 0.8\*, Ta 1.2\*, V 0.8\*, Zn 0.8\*).
- **CCD 판독 규칙**: 도달 못 하면 하한 `>x`, 발생하면 값, 애매하면 구간 `[a,b]` (Fig S12/S13/S14).
- **1년 aging PXRD overlay** (Fig S5–S8) → **정성 판정만**. 정량 지표 없음.
- 도구: HighScore Plus, BioLogic EC-Lab(추정), Archimedes. **pymatgen/VESTA/LOBSTER 등 계산 도구 없음.**

---

## 5. 결과 §2.1 — 구조 분석 (전 수치)

### 5a. Undoped 기준선

- undoped: **garnet 88.08 wt%**, 그중 **cubic 37.44 wt%** — 즉 대부분(≈60 %)이 저전도 **t-LLZO**.
  불순물 = **Li₂ZrO₃ + La₂Zr₂O₇** ("고온에서 Li 손실 후 나타나는 것으로 알려진 상").
  본문 표현 "≈95 % LLZO by weight"는 Table S5의 88.08과 어긋난다(§18.2).
- 도핑 시료 상대밀도 **>90 %** (Table S3), σ_i는 문헌 최고 수준과 비교 가능.

### 5b. 최적 자리 vs 대체 자리 (Fig 2, Fig 3a·3b)

- **Ga/Fe/Al을 예측 최적 자리(Li)에 넣으면 c-LLZO로 완전 전환**, 불순물 무시할 수준
  (Fig 2b: **Ga on Li → 98.4 % c-LLZO / 0.1 % t-LLZO / 1.4 % Li₂ZrO₃, χ²=2.5**).
- **같은 Ga을 La 자리에 넣으면**: 34.7 % c / **57.6 % t** / 5.2 % Li₂ZrO₃ / 2.4 % LiGaO₂, χ²=1.4.
  **Zr 자리**: 38.7 % c / **59.3 % t** / 2.0 % **LiAlLa₄O₈**, χ²=1.6.
  → 스토이키오메트리 불일치가 만든 불순물이 **Zr-함유 상(La 치환 시)** ↔ **La-함유 상(Zr 치환 시)** 로
  정확히 갈린다. LiAlLa₄O₈은 "Al³⁺ 유사 이온이 들어갈 수 있는 상들의 **placeholder**"이고,
  Ga 시료에서는 실제로 **LiGaLa₄O₈**. (Al 도핑 시료엔 안 나타나므로 기판 Al 오염이 아님을 확인.)
- **Si on Zr → 완전 상분리**: 소량 SiO₂ + undoped와 동일한 LLZO. (Table S5 Si cubic 25.79 %.)
- **일반화 (Fig 3b)**: ~~최적 자리는 **>90 % c-LLZO**가 대다수~~, 비최적 자리는 **c-LLZO 20–40 %**
  (undoped 수준) + 나머지 >50 %가 t-LLZO/불순물.
  > 🔧 **2026-08-04 교정 (§19.3a)**: 앞부분은 본문 문장(*"giving >90 % c-LLZO in most cases"*)을 그대로
  > 옮긴 것인데, Fig 3b 픽셀 실측으로는 **>90 %가 25/59 = 42 %뿐이고 중앙값은 74.9 %**, 오히려
  > **24/59(41 %)가 70 % 미만**이다. "대다수"는 성립하지 않는다. 뒷부분(비최적 20–40 %)은 맞다(67–71 %).
  > 대신 **더 강한 형태로 성립하는 명제**는 이것이다 — **선호 site가 3자리 중 cubic% 1위 = 49/51 (96 %)**.
  > 🔑 저자들의 해석: *"the sites predicted via defect energy do not so much predict the likelihood of
  > the dopants going into the structure, but rather the likelihood of those dopants distorting the
  > materials into the cubic structure."* — **결함에너지는 "들어가느냐"가 아니라 "입방화시키느냐"를 예측한다.**
- **총 garnet 함량은 대체로 >95 %**이고 **최적 자리/대체 자리 차이가 뚜렷하지 않다**(Fig 3a) —
  "많은 도펀트가 세 자리 어디에나 실제로 들어간다. 다만 입방화가 늘 따라오진 않는다."
  > ⚠ **2026-08-04 단서 (§19.3c)**: Fig 3a의 y축은 **80 wt%에서 잘려 있다.** 선호 site 기준
  > **Mo·Rh·Pd·Te** 는 총 garnet <80 %라 패널에 점이 아예 없다(대체 site까지 세면 12종 추가).
  > "대체로 >95 %"는 **잘린 축 위에서 읽힌 인상**이다.
- 미동정 2차상 6종 = **Ge·Re·Ir·Pt·Pd·Au — 전부 Zr 자리** (Fig 3a `*` 표시, 패턴 Fig S4).
  > 🔧 **2026-08-04 교정 (§19.6)**: 1차 digest는 첫 항목을 **Ga**로 적었으나 Fig 3a x축 라벨 확대 결과
  > **`*Ge`** 다. Ga는 Li-site 그룹이라 "전부 Zr 자리"와도 모순이었다 — Ge로 고치면 6종 전부 Zr 자리 ✅.
- 극단 실패: **Te(Zr) garnet 4.70 %**, **Pd(Zr) 26.91 %**, **Mo(Zr) 51.85 %**(대량 LiMoO₂ 형성),
  **Rh(Zr) 65.53 %**, **Au(Zr) 85.13 %**.
- **격자상수 (Fig S9)**: 입방 성분 a = **12.97–13.03 Å**, **모든 도핑 시료가 undoped보다 작다**.
  **σ_i와 상관 없음**(본문 명시). ← 🔑 "격자 팽창 = 빠른 Li"의 순진한 서사를 부정하는 음성 결과.
- **I-4̄3d (질서 입방상)**: Mo-Kα **10.15°** 특성 피크가 **Ga on Li 시료에서만** 보임 (Fig S10).
  Fe on Li·다른 자리엔 없음. refs [19,36]과 일치(0.2 도펀트/f.u.에서 Ga만).
- Samson 리뷰 [6] 최적 구간: a **12.91–12.98 Å**, Li **6.1–6.8/f.u.** — 그 구간 안에서도
  전도도가 **한 자릿수** 흩어진다(= 도펀트 원소 자체가 강한 효과를 갖거나 다른 인자가 있다).

### 5c. 1년 대기 노출 (Fig S5–S8)

- RT, **RH 30–50 %**, 1년. **대다수 시료가 유의하게 열화**. **피크가 저각으로 이동 = 격자 팽창.**
- **열화가 뚜렷하게 억제된 9종**: La 자리 **Ba, Pr, K** / Zr 자리 **Au, Si, Cu, Ti, Mn, Co**.
- 🔑 **이 9종은 전부 (i) Li 자리가 아니고 (ii) c-LLZO 함량이 낮다(≈60 % 이하)**:
  실측 cubic% = Ti 58.21 · Au 48.57 · Mn 47.30 · Cu 45.15 · K 44.37 · Co 44.13 · Pr 42.45 ·
  Ba 30.70 · **Si 25.79**. → **대기 안정 ↔ 입방상(=고전도) 정면 trade-off.**
- 저자 결론: *"codoping is needed to determine to what extent dual substitution will be able to make
  air-stable cubic garnet."* — **가장 명확한 Pareto 긴장인데 정량 지표가 없다**(§17.7).

---

## 6. 결과 §2.2 — 이온전도 (Fig 4a, Table S5)

**undoped σ_i = 1.62×10⁻⁶ S/cm** (본문 1.6×10⁻⁶). 이하 전부 **total(bulk+GB), RT**.

**상위 12종**

| 순위 | 도펀트(자리) | σ_i (S/cm) | vs undoped | cubic % |
|---:|---|---:|---:|---:|
| 1 | **Fe(Li)** | 1.19×10⁻³ | **735×** | 98.07 |
| 2 | **Ga(Li)** | 1.16×10⁻³ | **716×** | 98.43 |
| 3 | **W(Zr)** | 2.73×10⁻⁴ | 169× | 99.38 |
| 4 | **Ta(Zr)** | 2.47×10⁻⁴ | 153× | 70.93 |
| 5 | Co(Zr) | 9.37×10⁻⁵ | 58× | 44.13 |
| 6 | Sn(Zr) | 9.34×10⁻⁵ | 58× | 82.99 |
| 7 | Ni(Zr) | 9.33×10⁻⁵ | 58× | 93.13 |
| 8 | Ru(Zr) | 6.26×10⁻⁵ | 39× | 97.64 |
| 9 | Al(Li) | 6.04×10⁻⁵ | 37× | 98.61 |
| 10 | Gd(La) | 5.52×10⁻⁵ | 34× | 97.03 |
| 11 | Pr(La) | 5.36×10⁻⁵ | 33× | 42.45 |
| 12 | Hf(Zr) | 4.90×10⁻⁵ | 30× | 74.36 |

**하위 (undoped보다 낮은 3종)**: **Ge 1.40×10⁻⁶ · Pt 1.27×10⁻⁶ · Pd 8.25×10⁻⁷**.
그 위 저전도군: P 3.39×10⁻⁶ · **Nd 4.28×10⁻⁶** · Se 4.75×10⁻⁶ · Eu 5.00×10⁻⁶ · Tm 5.81×10⁻⁶.

- **"36종이 >10×"** (= σ_i > 1.62×10⁻⁵) — 🔧 **2026-08-04 3차 패스 교정(§20.3). 엄격히는 35종이다.**
  Table S5를 기계 파싱해 다시 세면 **35종**:
  (Ag, Al, Au, Bi, Ca, Cd, Ce, Co, Cs, Cu, Dy, Fe, Ga, Gd, Hf, In, K, Lu, Mg, Na, Nb, Ni, Pb, Pr,
  Rb, Ru, Sc, Sm, Sn, Sr, Ta, Tl, W, **Y**, Zn).
  **36번째는 Ho(1.57×10⁻⁵ = 9.7×)** — 유효숫자 2자리로 반올림하면 1.6×10⁻⁵ / 1.6×10⁻⁶ = 10×라
  저자들이 넣은 것으로 보인다. **인용할 땐 "35종(엄격) 또는 36종(Ho 반올림 포함)"으로 쓸 것.**
  > ⚠ 이 항목의 **1차 digest 목록에는 `Rh`가 들어 있었는데 이는 `Ho`의 철자 오타**였다
  > (Rh = 2.58×10⁻⁶ = undoped의 1.6×로 근처에도 못 간다). §19.5가 "Rh↔Ho 맞교환"으로 보였던
  > 원인이 바로 이것이고, **논문에는 아무 문제가 없었다**(§20.3).
- **"3종만 더 낮다"는 정확히 3종** ✓ (Pd 8.25×10⁻⁷ · Pt 1.27×10⁻⁶ · Ge 1.40×10⁻⁶) — 재확인.
- **Ga, Fe = 1.2×10⁻³ S/cm** — LLZO 문헌 최고치(1–2×10⁻³) 동급. **HT 합성 시료 품질의 증거.**
- 기존 유효 도펀트(**Al, Ta, W**) 전부 ~10⁻⁴ 재현 ✓. **덜 연구된 Co·Ni·Sn**도 고전도 —
  **Sn은 이전에 전혀 연구된 적 없음**.
- **입방화 없이도 σ가 오른다 (국소 무질서 효과)**: In(cubic 41.5 %, 16×)·**Pr(cubic 42.5 %, 33×)** —
  undoped와 상 조성이 거의 같은데 σ가 오른다 → **도펀트가 만든 국소 무질서 자체가 기여**.
  본문은 이 한계를 *"just over an order of magnitude"*로 쓰고, 결론은 *"30x"*로 쓴다(§18.3).
- **완전 입방화가 아니어도 최고급 σ 가능**: **Ta(Zr) 2.47×10⁻⁴, cubic 70.93 %, t 23.55 %,
  나머지 5.52 %는 저-Li 가넷 Li₅La₃Ta₂O₁₂** — Rietveld 회계가 정확히 맞는다.
- **등가 치환(isovalent) RE는 이득이 작다**: Sm(La) 2.92×10⁻⁵, Gd(La) 5.52×10⁻⁵ — 둘 다 **cubic ≈97 %**
  인데도 Ta(>10⁻⁴)에 크게 못 미침. → **입방화만으로는 부족하고 supervalent 치환이 만드는 Li 공공이 필요.**
  *"the two effects work together to give the highest conductivities."*
- **격자상수·전도도 무상관**(§5b), **결함에너지·BV mismatch가 큰(=더 파괴적인) 도펀트가 오히려 좋은 경우**
  (Ga, Fe) → 저자 speculation: 큰 국소 왜곡 → **I-4̄3d 전환**(Ga만 관측) → 고전도 [refs 19,36].
- **정말 "cubic이면 다 같은가"에 대한 반례**: In-doped c-LLZO는 Tm-doped보다 **4배** 전도 —
  둘 다 같은 입방상(In cubic 41.5 %, Tm cubic 96.25 %)인데. → *"cubic phase are not equally efficient."*

---

## 7. 결과 — 전자전도 (Fig 4b, Table S5)

- **undoped σ_e = 1.66×10⁻⁷ S/cm** (본문 1.7×10⁻⁷; 자기 선행연구 ref [28]의 1.3×10⁻⁷와 같은 계열).
- **대부분의 도핑 시료가 1–5×10⁻⁸ S/cm** = **도핑이 전자전도를 낮춘다**(3–10배).
- **예외 (위험군)**: **Co 1.20×10⁻⁶** (undoped보다 ~7×, 도핑군 대비 ~1자릿수 ↑) ·
  **Ru 2.09×10⁻⁷** · **Cu 1.30×10⁻⁷** · **Ir 1.24×10⁻⁷**. → **dendrite 위험 상승, 후보에서 제외 권고.**
  단 Co는 *"mixed ionic/electronic conductor로 복합 양극(catholyte)에는 오히려 적합할 수 있다"*[ref 11].
- **최저군**: Si 1.68×10⁻⁸ · Ba 1.90×10⁻⁸ · Ga 1.97×10⁻⁸ · In 2.00×10⁻⁸ · **Sc 2.05×10⁻⁸** ·
  Ta 2.16×10⁻⁸ · Zn 2.16×10⁻⁸ · K 2.30×10⁻⁸ · Ca 2.31×10⁻⁸ · P 2.32×10⁻⁸.
- 🔑 **한계 자인**: Han 2019 [ref 9]는 CCD 1 / 10 mA/cm²를 얻으려면 σ_e를 **10⁻¹⁰ / 10⁻¹² S/cm**까지
  낮춰야 한다고 했는데, 도핑으로 도달한 최저는 **1.7×10⁻⁸**.
  → *"this also suggests that there is little room for improving the electronic conductivity."*
  **도핑이라는 레버로는 σ_e를 2–4자릿수 더 낮출 수 없다.**

---

## 8. 결과 — 고전압 안정성 (Fig 5, Table 1/S5) ★★★ 우리 축 ①의 산화물 평행선

### 8a. 방법론 배경 (Introduction + §2.2)

- LLZO의 "실험 ESW 7–9 V" 보고는 **artifact**: 두꺼운 펠릿에 DC 전위를 걸고 전류를 보는 방식은
  **LLZO의 낮은 전자전도 때문에 kinetic하게 제한**되어 **과대평가**된다.
- 이 논문(과 ref [28])의 해법: **LLZO 분말 + 카본블랙 + PVDF 복합 전극**을 만들어 카본으로
  전자 경로를 깔아 kinetic 장벽을 제거한 뒤 CV. 원조 = **Han 2016 [ref 34]**.
- 대조 문헌값: Han [34] Ta-LLZO **0.05–4.0 V**; Benabed [31] LLZO|Au 나노복합 **1.65–3.7 V**(창 2.05 V);
  이 논문 Ga-LLZO **1.0–3.9 V**(창 **2.9 V**) → *"our electrochemical gap of 2.9 V is therefore more
  likely in terms of accuracy than the 2.05 V obtained using the Au-composites"*,
  그리고 밴드갭 기반 기대(3.1 eV [34])와 near-agreement.

### 8b. ★ 핵심 결과 — **V_max는 도펀트에 거의 완전 불변**

| V_max | 종수 | 도펀트 |
|---:|---:|---|
| **3.9 V** | **56 / 59** | 그 외 전부 (+ undoped) |
| 3.8 V | 3 | **Cr, Tb, Zn** |

- 두 번째 redox peak **4.5 V**는 **탄산에스터 전해질(≈4.3 V까지만 안정) 반응**으로 귀속 → **3.9 V 피크만**
  열역학적 상한으로 해석.
- Mn 시료에만 3.4 V 추가 피크 — **LiMnLa₃O₇ 불순물** 탓으로 귀속(V_max 판정은 3.9 유지).

> 🔑🔑 **이것이 우리 `axis_1`(S²⁻-limited onset) 서사의 *산화물판*이다.**
> 우리: comp1 / modelc(Cl-rich) **둘 다 onset 2.256 V로 동일** — 조성을 바꿔도 산화 한계가 안 움직인다.
> 그들: 59개 도펀트 전부 **3.8–3.9 V** — 도펀트를 바꿔도 산화 한계가 안 움직인다.
> **두 계 모두 "산화 한계는 음이온 골격이 pin 한다"**(우리 S 3p, 그들 O 2p + 가넷 골격)는
> [Banik 2022]·[Richards 2016]의 같은 명제. **이 논문은 그 명제의 59-도펀트 실험 규모 확인이다.**
> ⚠ 단 **그들 3.9 V는 CV(액체 전해질·복합 전극) 실측**, 우리 2.256 V는 **0 K grand-potential 열역학**.
> 절대값 비교 금지. 비교 가능한 것은 **"불변성"이라는 구조적 사실**뿐.

### 8c. 바뀌는 것은 **분해량** — ∫Idt (3.8–4.3 V, mAh/g). undoped = **1.39**

**가장 잘 passivate (낮을수록 좋음)**

| 도펀트 | ∫Idt | vs undoped |
|---|---:|---:|
| **Dy(La)** | **−0.05** | ≈0 (blank 이하) |
| **Sc(Zr)** | **0.36** | 0.26× |
| Co(Zr) | 0.46 | 0.33× |
| Ba(La) | 0.48 | 0.35× |
| **Y(La)** | **0.53** | 0.38× |
| Ge(Zr) | 0.55 | 0.40× |
| **Er(La)** | **0.57** | 0.41× |
| Si(Zr) | 0.67 | 0.48× |
| Fe(Li) | 0.71 | 0.51× |

**가장 나쁨 (분해량 폭증)**

| 도펀트 | ∫Idt | vs undoped |
|---|---:|---:|
| **Nd(La)** | **9.30** | **6.7×** |
| Rh(Zr) | 7.12 | 5.1× |
| Tl(Zr) | 6.77 | 4.9× |
| Zn(Li) | 6.60 | 4.7× |
| Ru(Zr) | 6.09 | 4.4× |
| Ca(La) | 5.47 | 3.9× |
| Te(Zr) | 5.38 | 3.9× |
| Lu(La) | 5.21 | 3.7× |
| Mo(Zr) | 5.18 | 3.7× |

- 본문 해석: **Sc·Y·Dy·Er (희토류)가 "best performance"** — 피크 전류가 강하게 억제되고
  3.9 V 피크 **이후 전류가 감소**(= 분해 생성물이 후속 반응을 막는 **passivation**).
  *"Dy shows no oxidation between 4.0 and 4.3 V implying that the products made up to 4.0 V slow down
  the decomposition dramatically."*
- 반대로 **Nd·Ca**는 피크가 크고 고전압으로 확장 = **passivation 실패**.
- 🔑 저자 해석: *"some dopants result in kinetic protection of the electrolyte, rather than significantly
  changing the actual thermodynamic decomposition voltage. This is similar to the role that sacrificial
  additives play in liquid electrolyte formulations."*
  → **"onset은 못 옮기지만 분해 산물의 질을 바꾼다"** — 이게 정확히 우리가
  **Cl-rich 4축**(onset은 같고 분해 *양·산물·계면*이 다르다)에서 말하는 것이다.
- **Fig 5 빨간 화살표**: **Nd = ↑(증가)**, **Y·Dy·Er·Sc = ↓(억제)**.

> ⚠ **본 digest 검증**: "희토류 Sc/Y/Dy/Er이 최고"는 **정렬해보면 관대한 표현**이다 —
> Co(0.46)·Ba(0.48)·Ge(0.55)가 Y(0.53)·Er(0.57) 사이에 끼어 있다. **화학족 서사**이지
> 순위 1–4위가 아니다(Dy 1위, Sc 2위, Y 5위, Er 7위). §17.6.

---

## 9. 결과 — 저전압 안정성 (Fig 6, Fig S11, Table 1/S5)

- **undoped V_min = 1 V** — 저자들 스스로 *"we estimate the low voltage limit to be at least 1.0 V,
  as opposed to many articles that suggest stability against Li metal (0 V vs Li)."*
  ⚠ **자기 선행연구 ref [28]의 "0.1–3.9 V"를 사실상 상향 수정한 것**(§18.4).
- **V_min < 0.1 V (= Li 금속 근처까지 안정) = 33 / 59종** (본 digest 계수):
  Ba, Cd, Co, Cs, Cu, Hf, Ho, In, Ir, Lu, Mg, Mn, Na, **Nd**, Ni, P, Pb, Pd, Pr, Rh, Ru, **Sc**, Se,
  Sm, Sn, Sr, Tb, **Ti**, Tl, Tm, **W**, Y, Yb.
- **나쁨(창이 좁음)**: Ca 2.2\*, Er 2.2, Ce 1.8\*, Nb 1.4, Re 1.3, B 1.2, Rb 1.2, Ta 1.2\*, Ge 1.1,
  **Ga 1 · Fe 1 · Gd 1 · Bi 1 · Cr 1 · Si 1 · Dy 1 · Au 1\***.
  → 🔑 **최고 전도도 3인방 Ga·Fe·Al이 전부 저전압에서 나쁘다**(Ga 1, Fe 1, Al 0.7\*).
- **이온성 액체 재확인 (Fig 6b–d, 60 °C)**: **Ga** = 1 V 근처 확실한 분해 전류 ✓(탄산에스터 결과 확인),
  **Hf** = 1 V에서 전류 훨씬 적음, **Ti** = 거의 완전 안정.
  → **탄산에스터 전해질이 만든 artifact가 아님을 교차 검증.** (👍 방법론적으로 성실한 지점)
- **Ti가 환원 억제 최강** — 1 V 이하 전류가 매우 작음 = 효과적 passivation.

---

## 10. 결과 — CCD (Table 1, Fig S12–S14)

- **18종만 측정** (Swagelok 개별 조립이라 HT 불가). 값 범위 **0.10 – 0.60 mA/cm²**
  (Ti 0.55, Ba 0.60이 최고 실측; 본문 "0.10 to 0.60" ✓).

| 도펀트 | CCD (mA/cm²) | σ_i | σ_e | V_min |
|---|---|---:|---:|---:|
| **Ba(La)** | **0.60** | 1.36×10⁻⁵ | 1.90×10⁻⁸ | <0.1 |
| **Ti(Zr)** | **0.55** | 1.19×10⁻⁵ | 2.66×10⁻⁸ | <0.1 |
| Nd(La) | **[0.55, 0.70]** | 4.28×10⁻⁶ | 2.96×10⁻⁸ | <0.1 |
| Cs(La) | >0.50 | 3.14×10⁻⁵ | 2.62×10⁻⁸ | <0.1 |
| Na(La) | >0.50 | 4.81×10⁻⁵ | 2.88×10⁻⁸ | <0.1 |
| Dy(La) | [0.45, 0.75] | 3.27×10⁻⁵ | 3.85×10⁻⁸ | 1 |
| Hf(Zr) | >0.45 | 4.90×10⁻⁵ | 4.51×10⁻⁸ | <0.1 |
| Ca(La) | [0.40, 0.85] | 2.87×10⁻⁵ | 2.31×10⁻⁸ | 2.2\* |
| Sc(Zr) | >0.40 | 2.46×10⁻⁵ | 2.05×10⁻⁸ | <0.1 |
| Zn(Li) | >0.40 | 2.42×10⁻⁵ | 2.16×10⁻⁸ | 0.8\* |
| **W(Zr)** | **0.40** | **2.73×10⁻⁴** | 3.08×10⁻⁸ | <0.1 |
| Mg(Zr) | >0.30 | 2.37×10⁻⁵ | 2.84×10⁻⁸ | <0.1 |
| Ru(Zr) | >0.30 | 6.26×10⁻⁵ | 2.09×10⁻⁷ | <0.1 |
| In(Zr) | >0.25 | 2.58×10⁻⁵ | 2.00×10⁻⁸ | <0.1 |
| **Al(Li)** | 0.2 | 6.04×10⁻⁵ | 2.65×10⁻⁸ | 0.7\* |
| **Fe(Li)** | 0.2 | 1.19×10⁻³ | 5.40×10⁻⁸ | 1 |
| **Ga(Li)** | **0.1** | 1.16×10⁻³ | 1.97×10⁻⁸ | 1 |
| Co(Zr) | 0.1 | 9.37×10⁻⁵ | 1.20×10⁻⁶ | <0.1 |

### 🔑 두 개의 큰 결론

**(i) 고 σ_i ⟹ 저 CCD** — *"the high ionic conductivity samples (Ga, Fe, and Al) have low CCD values
(0.1–0.2 mA cm⁻²)"*. **정면 Pareto 긴장**. 예외는 **W**(σ_i 2.73×10⁻⁴인데 CCD 0.40) —
그래서 W가 "particularly noteworthy"로 지목된다.

**(ii) CCD ↔ 저전압 안정성은 강상관, CCD ↔ σ_e는 무상관** ★★
- V_min 최고군(**Ti, Ba**)이 CCD 최고(**0.55, 0.60**).
- Zn과 Ca는 저전압 창은 나쁜데(0.8\*, 2.2\*) 환원 피크가 매우 작아 CCD는 개선.
- 예외 2개 자인: **Co**(저전압 좋은데 CCD 0.1 — σ_e 1.2×10⁻⁶의 자가방전으로 시험 실패로 해석),
  **Dy**(양·음극 모두 안정성 나쁜데 CCD ≥0.45 — *"the one anomalous intrinsic property … warrants further study"*).
- **저자들의 결론이 강하다**: *"These observations are in contrast to a recent article where increased
  electronic conductivity is linked to dendrite growth originating within the pellets themselves[9] …
  it appears that instability at the interface is the leading cause of failure and we therefore speculate
  that dendrite growth in fact starts at the interface … and that electronic conductivity in the LLZO
  therefore plays a minimal role in determining the CCD."*
  → **Han 2019(σ_e → dendrite) 패러다임에 대한 18-시료 실증 반론.**

> ⚠⚠ **우리 캠페인에 대한 직접 긴장**: 우리 서사(+B₂O₃ SEI·O-doping·wide-gap LiCl/LiBr 절연 계면)는
> 상당 부분 **"σ_e를 낮추면 dendrite가 준다"**에 기대 있다([li2025_cubr2]·[taklu2021] digest도 σ_e↓ ↔ CCD↑를
> 나란히 보고). **이 논문은 그 인과를 부정한다** — 적어도 LLZO에서, 그리고 σ_e 범위 10⁻⁸–10⁻⁶에서는.
> **다만 반박 가능한 지점이 셋 있다**: (a) 그들 σ_e 스팬이 좁다(대부분 1–5×10⁻⁸ = 한 자릿수 이내;
> Han이 말한 차이는 10⁻⁷→10⁻¹⁰ = 3자릿수), (b) **계면에 액체 전해질을 적셨다** → 계면 화학이
> 고체–고체가 아님 (저자 자인: 과전압 증가 원인), (c) 상대밀도 89–96 %로 가넷치고 낮아 GB/공극
> 경로가 지배할 수 있음. → **"σ_e 무용론"으로 인용하면 over-claim.** 정확한 인용은
> **"σ_e를 10⁻⁸대에서 더 미세조정하는 것보다 계면(저전압) 안정성이 CCD를 지배한다는 실증이 있다"**.

---

## 11. Figure set ★

| Fig | 무엇을 보여주나 | 우리가 참고할 점 |
|---|---|---|
| **1** | 주기율표 위에 59 도펀트 색칠: **노랑=신규 29 · 파랑=기보고 30 · 빨강=host(Li,Zr,La,O)** | **풀 정의를 한 장으로 방어하는 포맷.** 우리 47종 cascade 풀도 이렇게 그리면 `pool_provenance` 해명이 그림 한 장이 된다 (신규/문헌/탈락 3색). **최우선 이식 그림** |
| **2a** | 대표 XRD 5개(c-LLZO tick / Ga·Fe·Al on Li / Si on Zr / undoped / t-LLZO tick) + ρ 표기 | 상 판정의 시각적 정본. 불순물(Li₂ZrO₃·La₂Zr₂O₇·SiO₂) `*` 표기 관례 |
| **2b** | Ga 3자리 Rietveld 3벌 + χ² + 상 조성 wt% | **"같은 도펀트, 자리만 바꾼 3벌"** = 자리 효과 분리 포맷 |
| **3a** | 59×3 전 시료의 **total garnet wt%** 산점 (주황=최적자리, 빨강/파랑=대체) | **전수 매트릭스를 한 장에** — 우리 cascade 47×3농도 산점의 원형 |
| **3b** | 같은 축의 **cubic wt%** | 여기서 최적자리(주황)가 압도적으로 위 = 논문의 1번 주장 그림 |
| **3c** | 도펀트별 **bond valence mismatch** (자리 3색) | 값싼 서술자를 전수로 깔고 실험과 겹쳐보는 포맷 |
| **3d** | 도펀트별 **결함에너지 (ref [12] 인용)** (자리 3색). Lu는 `n/a` | **문헌 계산값을 자기 실험축에 나란히 놓는 방법** — 우리도 BVSE/UMA proxy를 문헌값과 병치 가능 |
| **4a** | **주기율표 히트맵 — RT σ_i** (10⁻⁶~10⁻³ 컬러바), undoped 별도 박스 | 🔑 **주기율표 히트맵**이 이 논문 최고의 전달 장치. 우리 cascade 47 도펀트 점수를 이 포맷으로 그리면 즉시 대조 가능 |
| **4b** | **주기율표 히트맵 — σ_e** (10⁻⁸~10⁻⁶) | 같은 포맷 두 물성 = 시선 이동만으로 trade-off 읽힘 |
| **5** | **59개 고전압 CV 소형 격자**(3.5–4.7 V), blank 차감. 빨강 화살표로 Nd↑ / Y·Dy·Er·Sc↓ | **small-multiples**로 59개를 한 장에. 우리 47 도펀트 ESW 프로파일도 이 포맷 가능 |
| **6a** | 59개 저전압 CV 소형 격자(0–3 V). Ga/Ti/Hf 검은 박스 강조 | 강조 박스로 "다음 그림에서 확대할 것" 예고 |
| **6b–d** | **이온성 액체** 재측정 3종(Ga/Ti/Hf), blank(검정) vs 시료(빨강) | **전해질 교차검증** 서브패널 — 방법 artifact 방어의 모범 |
| **S1–S3** | Ga(Li)·Ca(La)·W(Zr) 자리 정련 Rietveld 전체 도해 | 정련 품질 공개 관례 |
| **S4** | 미동정 2차상 6종(Ga·Re·Ir·Pt·Pd·Au on Zr) 패턴 | **"못 맞춘 것을 그대로 공개"** — 정직성 장치 |
| **S5–S8** | 1년 aging overlay 4세트(빨강=aged, 검정=pristine), 전 59종 | 정성 열화 판정 |
| **S9** | 입방 성분 **격자상수 a** 59종 산점 (12.97–13.03 Å) | **음성 결과 그림**(σ와 무상관)을 SI에 명시 |
| **S10** | Ga/Fe 3자리 확대 — **I-4̄3d 특성 피크 10.15°** (Ga on Li만) | 미세 구조 증거의 확대 제시법 |
| **S11** | 저전압 CV 원자료(blank 미차감) 전 59종 | 원자료 공개 |
| **S12** | CCD 도달 6종 (Co 0.10 / Ga 0.10 / Al 0.20 / Fe 0.20 / **Ti 0.55** / W 0.40), 빨강 화살표 | **판독 규칙을 그림 위에 명시** — 우리 BVSE 채널% 판독 관례와 같은 정신 |
| **S13** | CCD 미도달 6종 (Zn·Sc·Ru·Mg·In·Hf), 노랑 화살표=하한 | **"못 얻은 값을 하한으로"** 정직 보고 |
| **S14** | La 자리 6종(Na·Nd·Dy·Ba·Ca·Cs), 노랑+빨강 화살표 → **구간 보고** | **구간 보고 관례** — 우리 σ 절대값 금지 규율과 같은 계열 |

---

## 12. 우리 cascade 대비 ★★★

### 12a. 설계 1:1

| 축 | **Anderson 2024 (LLZO, 실험)** | **우리 cascade v23 (argyrodite, 계산)** | 판정 |
|---|---|---|---|
| host | Li₇La₃Zr₂O₁₂ (산화물 가넷) | Li₅.₄PS₄.₄Cl₁.₆ / Li₆PS₅Cl (황화물 argyrodite) | ⛔ 화학 다름 — **수치 이식 금지** |
| 풀 크기 | **59 도펀트** | **47 도펀트** | 체급 동일 (조성족 스캔) |
| 풀 출처 | 기보고 30 ∪ **Ceder DFT 예측 45**[12] | 사람 큐레이션(코팅 문헌·전구체·발란스) | **그들 우위** — 문헌 정의 집합이라 한 문장 방어 |
| 풀 탈락 회계 | Sb 제외 사유 없음, 결측 5종 사유 없음 | **91→47 = 파이프라인 탈락임을 명시** | **우리 우위** |
| 치환 자리 | **Li/La/Zr 3자리 전수 (177 시료)** + 최적자리 예측(DFT/BV) | 도펀트별 **배치 앙상블 최소에너지**(Nd₂O₃ 342 cfg) | **설계 철학 다름** — 그들 "다 만들어 본다" vs 우리 "계산으로 고른다" |
| 농도 | **0.2 atom/f.u. 단일 고정** | **x ∈ {0.02, 0.05, 0.10}** 3점 | **우리 우위** (농도 의존성 있음) — 단 우리 게이트마다 농도 규약이 다른 문제는 별개 |
| 축 ① 상/구조 | garnet%·cubic% (Rietveld 정량) | Δe(UMA, host 상대) = G1 | 대응 |
| 축 ② 이온전도 | **σ_i total 실측 (EIS)** | **BVSE proxy** + 챔피언 MLIP-MD | 그들 실측 / 우리 프록시 |
| 축 ③ 전자전도 | **σ_e 실측 (DC)** | **없음** (gap은 진단만) | **그들 우위** — 우리 공백 축 |
| 축 ④ 산화 | **V_max(CV) + ∫Idt(적분)** | grand-potential ox_V = G3, window = G2 | 열역학 vs kinetic — **상보** |
| 축 ⑤ 환원 | **V_min(CV) + 이온성 액체 교차검증** | grand-potential red_V (G2 안에) | 그들 실측, 우리 열역학 |
| 축 ⑥ dendrite | **CCD 실측 (18종)** | **없음** | **그들 우위** |
| 축 ⑦ 기계 | **없음** | **E_VRH + Pugh G/B = G5 (가중 35 %)** | **우리 우위** |
| 축 ⑧ 대기 안정 | **1년 aging PXRD (정성)** | 없음 | 그들 우위 (단 정성) |
| 축 ⑨ 계면 반응성 | 없음 | interface_reactivity (vs LCO) | 우리 우위 |
| **순위화** | **없음** — 축별 볼드 flag만. 단일 점수·가중치·Pareto **전부 없음** | **score = 0.30 ox + 0.25 stable + 0.20 soft + 0.15 ductile + 0.10 window** (min-max) | **정면 대조**(§12d) |
| 조합/codoping | **결론에서 제안만** (계산·실험 없음) | 테마 12+1 + **codoping 교호작용 ML** | **우리 우위** — 그들이 "필요하다"고 한 것을 우리가 실행 |
| 오차막대 | **없음** (전 물성 단일 측정, 반복 없음) | Ea 3-seed ±, 순열 전수 | 양쪽 다 약함, 우리가 조금 나음 |
| 컷 민감도 | **없음** | **전 순열 120개 전수 + 컷 스윕 전축** | **우리 압도** |
| 실험 검증 | **전부 실험** | 없음 (전부 계산) | **그들 압도** |

### 12b. 컷 값 근거 — 나란히

| | **Anderson 2024** | **우리 cascade** |
|---|---|---|
| host 앵커 컷 | **1개**: ∫Idt < 1.39 (= undoped 실측) | **3개**: G1 Δe<0(host) · G3 ox_V ≥ 2.14 V(host onset) · (G2 0.05 V는 db 규약 승계) |
| 분포 유도 컷 | 1개(암묵): σ_e < 2.5×10⁻⁸ | **1개**: G4 BVSE 0.3 (통과자 분포 공백대) — 단 "최대 공백 아닌 3번째"까지 자인 |
| 자의적 컷 | **3개**: cubic >94 % · σ_i >5×10⁻⁵ · CCD ≥0.4 — **표시 없음** | **1개**: G5 median split — **`arbitrariness_flag: true`로 명시** + 컷 지배 경고 |
| 문헌 승계 컷 | **0개** | 0개 (문헌 절대 문턱 이식은 **실패로 기록**) |
| 상속 상수 | 없음(공개된 한) | **1개**: G4 blocking<0.60 — host 앵커도 문헌 대응도 없음을 **폭로** |
| 컷을 순차 적용? | **아니오** (적용하면 0종 — §3e) | 예 (적용하면 1종, 그러나 **"결론 아님" 경고 부착**) |

> 🔑 **양쪽 다 자의적 컷을 갖고 있고, 양쪽 다 그 컷이 결과를 지배한다.**
> 차이는 **우리만 그걸 문서에 적어놨다**는 것이다. 정직성 면에서 우리가 우위이고,
> **데이터의 무게(실측 6축 × 59종 × 3자리)** 면에서는 그들이 압도한다.

### 12c. ★ 우리 정직성 장치 6종 — 대응물 판정 (본문 12 pp + SI 17 pp 전수 정독 후)

| # | 우리 장치 | 이 논문에 대응물? | 판정 근거 |
|---|---|---|---|
| 1 | **vacuous 게이트 표시** (unique_kill=0) | **❌ 없다** | 게이트 구조 자체가 없으니 형식적 대응물은 성립 불가. 다만 **실질적 대응은 있다**: V_max가 59/59 축퇴인 것을 인지하고 **∫Idt로 축을 갈아탔다**. "축퇴를 발견하고 대체 관측량으로 이동" = 우리 vacuous 판정의 *행동적* 등가물. **명시적 라벨은 없음** |
| 2 | **게이트 순서 민감도 전수 계산** (120 순열) | **❌ 없다** | 순차 구조가 없어 개념 자체가 부재 |
| 3 | **컷 지배 경고** (G5 하나가 0↔11 지배) | **❌ 없다** | 컷 민감도 분석 전무. Table S5 캡션 5개 컷의 근거도 미제시 |
| 4 | **상속 상수 폭로** (G4 blocking) | **❌ 없다** | 대신 **더 큰 상속을 한다** — "최적 자리"를 통째로 ref [12] DFT에서 상속하고, 그 DFT의 방법 파라미터를 이 논문에 전혀 옮겨 적지 않았다. **상속을 하되 폭로는 안 한 사례** |
| 5 | **문헌 문턱 이식 실패 기록** | **🟡 부분적** | 문턱 이식은 안 하지만, **문헌 ESW(7–9 V)가 kinetic artifact임을 명시적으로 반박**하고 **Han 2019 σ_e→dendrite 패러다임을 자기 데이터로 반증**한다 = "문헌 기준을 그대로 쓰면 틀린다"의 실증. 형태는 다르나 **정신은 있다** |
| 6 | **풀 출처 정직** (91→47은 물리 게이트 아님) | **🟡 부분적** | 풀 정의(30+45 문헌)는 명확하고 방어 가능 = **우리보다 나은 출처**. 그러나 **탈락 회계는 없다**(Sb 제외 사유 무, 결측 5종 사유 무, 미동정 2차상 6종은 Fig S4로 공개 = 부분 정직) |

**추가로 그들에게 있고 우리에게 없는 정직성 장치 3개** (배울 것):

| # | 그들 장치 | 내용 | 우리 이식안 |
|---|---|---|---|
| H1 | **못 얻은 값을 하한/구간으로 보고** | CCD `>0.45`, `[0.55, 0.70]` (Fig S13/S14 노랑·빨강 화살표 규칙을 그림 위에 명시) | 우리 BVSE 채널%·MLIP σ 비율도 **점추정 대신 구간**으로. 특히 단일시드 값 |
| H2 | **못 맞춘 것을 그대로 공개** | 미동정 2차상 6종 패턴을 Fig S4로 그대로 실음 | 우리 stage-01 실패 44종의 **실패 로그**를 db에 공개 |
| H3 | **방법 artifact 교차검증** | 탄산에스터 CV 결과를 **이온성 액체 + 60 °C**로 재측정(Fig 6b–d) | 우리 BVSE 결과를 **다른 파라미터셋**(R0/b)으로, MLIP 결과를 **다른 모델**로 교차 |

### 12d. 순위화 — 이 논문에는 **없다**

- **단일 점수 없음. 가중치 없음. Pareto 플롯 없음. 랭킹 표 없음.**
- 대신: ① Table S5 축별 볼드 flag, ② 본문에서 **"동시에 여러 축을 개선한 도펀트"를 이름으로 지목**:
  - **W(Zr)** — *"a particularly noteworthy dopant here is W that yields high ionic conductivity,
    stability at low voltage and a relatively high CCD in comparison to the other high conductivity dopants."*
  - **Sc(Zr)** — *"In complement to this is Sc that shows the best combined stability at high and low
    voltage, as well as low electronic conductivity and also improved CCD."*
  ③ 결론에서 **codoping 역할 배분**: 입방화·전도 = Ga/Fe / 창 확장 = Ti·Sc·Dy / 대기안정 = Zr·La 자리의
  Ba·Pr·K·Ti… / *"machine learning algorithms are expected to be needed"*.
- 🔑 **즉 이 논문의 "순위화"는 명시적으로 사람이 읽는 서사(narrative)다.** 그게 약점이자
  (§3e를 감안하면) 정직한 선택이다.

### 12e. ★★ 원소 수렴 — Sc와 W

| 스크린 | 대상 | 최상위 | 이유 |
|---|---|---|---|
| **Anderson 2024** (LLZO, 실험, 59종) | 가넷 도펀트 | **W** (σ_i+저전압+CCD), **Sc** (고·저전압+σ_e+CCD) | 다축 동시 개선 |
| **Kim 2026** (계산, 17,230→8) | NCM 코팅 | **Li₃Sc₂(PO₄)₃** | Li 전도도가 결정타 |
| **우리 cascade v23** (계산, 47종) | argyrodite 도펀트 | **Sc₂O₃ (score 1위 0.813)** · **WO₃ (G1–G5 유일 생존자)** | 산화안정+역학 가중 / 5게이트 통과 |

> 🔑🔑 **서로 다른 host(가넷/인산염/argyrodite), 서로 다른 방법(실험/계산/계산), 서로 다른 축 가중치에서
> 최상위 원소가 Sc와 W로 겹친다.** 우리 결과가 완전히 자의적인 게 아니라는 외부 신호다.
>
> ⚠ **그러나 "같은 이유로 뽑힌 게 아니다"** — 우리 Sc₂O₃ 1위는 **산화안정 0.30 + 역학 0.35 가중합**,
> Anderson의 Sc는 **passivation 품질(∫Idt 0.36) + σ_e 최저군 + CCD**. 우리 WO₃ 생존은
> **자의적 G5 median 컷의 산물**(우리 스스로 "결론 아님"이라 적어둔 것), Anderson의 W는
> **실측 σ_i 2.73×10⁻⁴ + CCD 0.40**. → **원소 일치까지만 말할 것.** 메커니즘 일치 주장 금지.
>
> 🔑 **더 정밀한 수렴 하나**: 우리 G3에서 **host onset을 *올리는* 6종 = B₂O₃·Cr₂O₃·Ga₂O₃·In₂O₃·Sc₂O₃·Y₂O₃**.
> Anderson의 **고전압 passivation 최강군 = Sc·Y·Dy·Er**. **Sc·Y가 양쪽 산화축 상위에 동시 등장.**
> ⚠ 우리 것은 **열역학 onset 이동**, 그들 것은 **kinetic passivation 품질** — 물리가 다르다.
> 그럼에도 "산화축에서 Sc·Y가 반복 등장"은 후속 검토 가치가 있는 신호다(§16.5).

### 12f. ★★ 32/36 — 원소 수준 실험 참조표

**우리 47 도펀트가 담은 양이온 원소 36종 중 32종이 Anderson의 59종 안에 있다.**

- **겹침 32**: Ag, Al, B, Ba, Ca, Co, Cr, Cu, Fe, Ga, Gd, Ge, Hf, In, Mg, Mn, Mo, Na, Nb, Nd, Ni,
  Sc, Si, Sm, Sn, Sr, Ta, Ti, V, W, Y, Zn
- **우리에만**: La, Li, Zr (LLZO에선 host라 도펀트가 될 수 없음), **Sb** (Anderson이 유일하게 제외)
- **그들에만 (27)**: Au, Bi, Cd, Ce, Cs, Dy, Er, Eu, Ho, Ir, K, Lu, P, Pb, Pd, Pr, Pt, Rb, Re, Rh,
  Ru, Se, Tb, Te, Tl, Tm, Yb

> 🔑 **이게 이 논문의 실무적 최대 가치다**: 우리 도펀트 32종 각각에 대해
> **"산화물 host에서 같은 원소를 실험으로 넣으면 어떤 일이 일어나는가"의 6축 실측 참조점**이 생겼다.
> ⛔ **수치 이식은 금지**지만, **부호·경향의 sanity check**로는 쓸 수 있다.
> 예: 우리 G2에서 창이 붕괴한 후기 TM 4종(**Fe₂O₃·CoO·NiO·MnO**)의 원소가
> Anderson에서 각각 σ_e = Fe 5.40×10⁻⁸ · **Co 1.20×10⁻⁶(최악)** · Ni 2.70×10⁻⁸ · Mn 3.15×10⁻⁸ —
> **Co가 전자 누설 최악**이라는 것은 두 host 공통 신호다. Fe는 산화물에선 σ_i 챔피언인데
> 우리 황화물 계산에선 창이 붕괴한다 → **host 의존성이 큰 원소**로 표시해둘 것.

---

## 13. 우리 db 수치 대비 → `../our_dft_baseline.md`

> ⛔ **아래 표는 "같은 표에 넣어 비교"가 아니라 "축이 어떻게 다른가"를 보이는 것이다.**
> LLZO(산화물 가넷) 절대값을 argyrodite 문맥으로 옮기지 말 것.

| 항목 | Anderson 2024 (LLZO) | 우리 (comp1 / modelc) | 비교 가능? |
|---|---|---|---|
| 산화 한계 | **V_max 3.8–3.9 V (59/59 축퇴)**, CV·액체 전해질 | onset **2.256 V** (LiS4 제외) / 2.14 V, **0 K grand-potential** | ❌ 절대값 불가 (방법·화학 둘 다 다름) · ✅ **"조성/도펀트에 불변"이라는 구조적 사실은 비교 가능** |
| 산화 메커니즘 | O 2p / 가넷 골격이 pin | **S 3p (free S²⁻)가 pin** | ✅ 같은 논증 구조 ([Banik]·[Richards]) |
| 도핑이 바꾸는 것 | **분해 *양*(∫Idt 0.26–6.7× undoped)** | **분해 *양·산물·계면*** (Cl-rich 4축) | ✅ **개념 완전 일치** — 그들이 실험으로 스칼라화한 것을 우리는 열역학으로 분해 |
| 환원 한계 | V_min 실측 <0.1 – 2.2 V, undoped 1 V | red_V **1.242 V** (grand-potential) | ❌ 방법 다름 (CV kinetic vs 0 K 열역학) |
| σ_i | **total 실측**, undoped 1.62×10⁻⁶ → 최대 1.2×10⁻³ | **MLIP-MD D**(절대 인용 금지), Ea 0.253/0.224 eV | ⛔ **절대값 인용 금지 양쪽 다.** 비율만 |
| σ_e | **실측** 1.7×10⁻⁷ → 1–5×10⁻⁸ | **없음** (band gap만: comp1 2.066 / modelc 2.099 eV, PBE 과소) | ❌ 우리 공백 |
| CCD | **실측 0.10–0.60 mA/cm²** (18종) | 없음 | ❌ 우리 공백 |
| 기계 | 없음 | E_VRH 22.06 / 27.66 GPa, B₀ 26.23 / 21.71 | ❌ 그들 공백 (우리 우위 축) |
| 무질서 | **Rietveld wt%로 정량**(c/t 상 비율) — 원자 수준 무질서는 미정련 | comp2 disorder ensemble (cfg0/1/2, anneal+relax) | 🟡 층이 다름 (상 수준 vs 자리 점유 수준) |
| band gap | **인용값만** (Ga-LLZO 3.1 eV, ref [34]) | fixed-occ nscf 고유값 (canonical) | ❌ 그들은 계산 안 함 |

**핵심 정합 3점**
1. **"산화 한계는 host 음이온이 pin, 도펀트는 못 옮긴다"** — 우리 axis ①과 완전 동형.
2. **"도펀트가 바꾸는 것은 분해의 *양과 질*"** — 우리 Cl-rich 4축 서사의 실험 평행선.
3. **"고전도와 계면 안정은 상충한다"** — 그들 σ_i↑ ⟹ CCD↓, 우리 G3(onset↑ 6종) ⟹ G4(수송) 전멸.
   **양쪽 다 같은 Pareto 벽에 부딪혔다.** [Xiao] Fig 7(V_ox ↔ Li 함량 trade-off)까지 세 편이 같은 벽.

---

## 14. 적용 인사이트 — **이식할 방법·논증 구조** (숫자 아님) ★

1. **[최우선·발표] 주기율표 히트맵 (Fig 4a/b) 포맷을 우리 cascade에 이식.**
   47 도펀트를 주기율표 칸에 놓고 ① 종합 score ② ox_V ③ BVSE proxy ④ E_young 4장을 같은 포맷으로.
   `tools/figures/house_style.py` 팔레트로. **"어느 화학족이 어느 축에서 이기는가"가 즉시 읽힌다.**
   Origin-ready CSV 동시 출력 (원소 기호, 그룹, 주기, 값).

2. **[최우선·방법] 축퇴 축을 버리고 대체 스칼라로 이동하는 패턴.**
   그들: V_max 59/59 축퇴 → **∫Idt(3.8–4.3 V 전류 적분)** 로 이동.
   우리: **ox_V가 19/47 종에서 2.14 V에 축퇴**(S²⁻-limited) — 우리도 같은 처지다.
   → **우리 판 ∫Idt를 만들 것**: grand-potential 프로파일에서 **onset 이후 μ_Li 구간의
   분해 반응 수 / 누적 분해 에너지 / Li 방출량**을 적분한 스칼라. onset이 축퇴돼도 이건 안 축퇴된다.
   (`kb/open_items.md` 신규 항목 후보.)

3. **[이식] 풀 정의 그림 (Fig 1).** 우리 47종을 주기율표에 3색으로:
   신규/문헌기보고/**파이프라인 탈락 44종**. `pool_provenance` 해명이 그림 한 장이 된다.

4. **[이식] 하한·구간 보고 관례 (H1) + 실패 공개 (H2) + 방법 교차검증 (H3).** §12c 표.

5. **[검토·주의] Sc·Y가 산화축 상위에 반복 등장.**
   우리 G3 onset 상승 6종 ∩ Anderson passivation 최강 4종 = **{Sc, Y}**.
   → **Sc₂O₃·Y₂O₃의 argyrodite 산화 계면을 우선 정밀 검토** 가치. ⚠ 단 우리 것은 열역학,
   그들 것은 kinetic — "같은 현상"이라 쓰면 안 되고 "두 축에서 같은 원소가 나온다"까지만.

6. **[경고·재검토] σ_e → dendrite 인과에 대한 외부 반증이 생겼다.**
   우리 서사(B₂O₃ SEI·wide-gap 절연 계면)를 발표할 때 **Anderson의 반례를 먼저 인용하고 반박**하는 편이
   방어에 유리하다. 반박 논거는 §10의 (a)(b)(c) 세 가지 + 우리 계는 σ_e 스팬이 다를 수 있다는 점.
   **선제적으로 다루지 않으면 리뷰어가 정확히 이 논문을 들고 온다.**

7. **[서사] "단일 도펀트로는 못 한다"의 외부 실증.**
   §3e(그들 자기 컷 → 0종) + 그들 결론(codoping 필요 + *"machine learning algorithms are expected to
   be needed"*) = **우리 codoping 교호작용 ML(`codoping_ml_v2`)의 존재 이유를 문헌이 먼저 요청한 것.**
   → 발표에서 "이 논문이 필요하다고 한 것을 우리가 계산으로 실행했다"로 배치 가능. **강한 서사 카드.**

8. **[검토] "자리 예측 ≠ 자리 검증"의 분리.**
   그들은 예측(DFT/BV)과 검증(c-LLZO 함량 + Rietveld 자리 정련 3건)을 분리한다.
   우리 cfg 선택(Nd₂O₃ 342→cfg141)에는 **독립 검증 관측량이 없다** — 무엇을 검증량으로 삼을지
   (예: 무질서 앙상블 간 BVSE 채널% 일관성, XRD 시뮬레이션) 설계 필요.

---

## 15. 주의 / 한계 / over-claim 위험 목록 ★ (비판적으로)

1. **⛔ 화학이 다르다.** LLZO는 산화물 가넷. **어떤 절대값도 argyrodite로 이식 금지.**
   실증: 우리가 [Xiao]의 V_ox ≥ 4.0 V를 이식했더니 **생존자 0(empty gate)**
   (`literature_absolute_variants`). 같은 실패가 여기서도 재현될 것 — 3.9 V는 황화물에 존재하지 않는다.
2. **단일 농도(0.2/f.u.)·단일 온도(1050 °C)·단일 합성법.** 저자 자인:
   *"For dopants with intermediate amounts of c-LLZO, it is possible that a slightly higher dopant
   concentration would fully convert the sample to cubic."* → **모든 순위가 농도 조건부.**
3. **오차막대 전무.** 59종 × 6물성 전부 **단일 시료·단일 측정**. 반복·표준편차 없음.
   c-LLZO wt% 소수점 둘째 자리까지 인쇄돼 있으나 **그 정밀도는 근거 없음**(Rietveld 통계오차만).
4. **상대밀도 89–96 %** (Table S3, 8종만 측정). 가넷 문헌 최고급(>97 %)에 못 미침 →
   **σ_i(total)에 GB·공극 기여가 크고, CCD 절대값이 낮은 원인일 수 있음.** 8/59만 측정한 것도 약점.
5. **σ_i = total (bulk+GB 미분리).** 등가회로에 GB용 RQ를 넣고도 **분리값을 보고하지 않는다.**
   → **"도펀트가 bulk를 개선했는가 GB를 개선했는가"를 이 논문으로는 답할 수 없다.**
   (우리 [Adeli]/[Kraft] digest에서 반복 지적한 바로 그 함정.)
6. **"희토류 Sc·Y·Dy·Er이 최고"는 관대한 서술.** 실제 ∫Idt 순위 1·2·5·7위이고
   Co(3위)·Ba(4위)·Ge(6위)가 사이에 있다 (§8c).
7. **대기 안정성이 정성뿐.** 1년 aging의 유일한 지표가 "PXRD 피크가 얼마나 변했나"의 **눈대중**.
   질량 변화·H₂ 발생·Li₂CO₃ 정량·전도도 재측정 **전부 없음**. 9종 명단의 재현성 미지.
8. **CCD 셀에 액체 전해질을 적셨다.** 저자 자인: 과전압 성장 원인. → **"고체–고체 계면의 CCD"가 아니다.**
   §10의 σ_e-무용론 결론이 여기에 직접 걸린다.
9. **결측 5종(Er·Mo·Tb·Te·Yb)의 σ_i/σ_e가 공란인데 사유가 없다.** Te(garnet 4.7 %)·Mo(51.9 %)는
   상이 안 만들어져서로 추정되나 Er·Tb·Yb는 상순도 93–96 %인데도 공란 — **판독 불가**.
10. **CCD가 18/59만.** 그런데 CCD는 논문의 가장 강한 주장(§10-ii)의 근거다.
    **주장 강도 대비 표본이 작다.**
11. **ESW를 액체 전해질 안에서 잰다.** 4.5 V 피크를 전해질 탓으로 돌리는 것은 합리적이나,
    **3.9 V 피크에 전해질 기여가 전혀 없다는 보장도 없다.** 이온성 액체 교차검증은 **저전압 쪽만** 했다.
12. **"defect energy가 입방화를 예측한다"의 통계적 검정이 없다.** Fig 3b는 산점도이고
    상관계수·유의성 검정 없음. "orange가 대체로 위"는 눈으로 보는 판정.
13. **batch Rietveld에 도펀트를 안 넣었다.** 검증은 3시료뿐이고 **Ga는 판별 마진 2.3 %**(§4b).
    자리 귀속의 증거력은 W ≫ Ca > Ga.
14. **비용·독성 축 없음.** Sc·Ta·W·Ru·Ir·Pt·Au·Re·Tl 등이 태연히 후보로 남는다.
    (우리 cascade의 `cost_tier` 축이 이 공백을 메운다 — [Xiao]·[Kim]에도 없던 것.)
15. **codoping은 제안만.** 논문의 결론이자 최대 주장인데 **실험도 계산도 0건**.
16. **Khaliullin(계산 전문) 공저인데 자체 계산 0.** 기여 내용 미상 — 이 논문을 "계산 논문"으로
    분류하면 틀린다.

---

## 16. 내부 불일치 목록 (본문 ↔ SI ↔ 그림) — 그림/표 우선 규율 적용

| # | 항목 | 본문 | SI | 그림 | **채택** |
|---|---|---|---|---|---|
| 1 | **Ti CCD** | Table 1: **0.55** | Table S5: **0.65** | **Fig S12 패널: "Ti: CCD = 0.55"** | ✅ **0.55** (그림+본문 표 2:1). 본문 "0.10 to 0.60" 범위 서술과도 정합. **Table S5가 오타** |
| 2 | undoped garnet 함량 | "≈95 % LLZO by weight" (p.3) | Table S5: **88.08** | Fig 3a 최좌측 ≈88 | ✅ **88.08** — 본문 "≈95 %"는 **일반 서술("most samples >95 %")과 혼동된 표현**으로 보임 |
| 3 | 비-입방 전도 이득 한계 | Results: *"just over an order of magnitude"* (In 16×) | — | — | 🟡 **결론의 "30x"는 Pr(33×)** 기준. 두 서술이 다른 시료를 가리킴. 인용 시 **어느 시료인지 명시할 것** (Pr 33× / In 16×) |
| 4 | undoped 저전압 한계 | 이 논문 **1.0 V** | Table S5 Undoped V_min **1** | Fig S11 | ✅ 1.0 V. ⚠ **자기 선행연구 ref [28]의 "0.1–3.9 V"를 상향 수정한 것** — 인용 시 2024 값을 쓸 것 |
| 5 | σ_e–CCD 무상관 예시 | *"Co has an electronic conductivity more than double that of Ga and yet shows a higher CCD"* | Co σ_e 1.20×10⁻⁶ = Ga의 **61배**, **CCD 둘 다 0.1** | — | 🔴 **예시가 Table 1과 안 맞는다.** Hf(σ_e 2.3배, CCD >0.45)면 문장이 정확히 성립 → **"Co"는 Hf 오기로 추정**(확정 불가, digest 추론) |
| 6 | 그림 참조 번호 | p.4 *"defect energy calculations in **Figure 2d**"* | — | 결함에너지는 **Fig 3d** | ✅ **Fig 3d** — 본문 오타 |
| 7 | 시료 수 | "59 dopants … (177 materials)" / "180 PXRD patterns of the doped samples" | Table S2 = **177행 = 59 도판트 × 3자리, Sb 없음**(§20.1 기계 재검) | — | ✅ 177 도핑 + 세트별 undoped 3 = **180 패턴**. "of the doped samples"가 부정확한 표현. **2차 패스의 "Sb 포함 60×3=180" 가설은 기각** — Sb는 Table S2에 아예 없다 |
| 8 | 2차상 표기 | "LiAlLa₄O₈" (Al³⁺-유사 이온용 placeholder; Ga 시료는 실제 LiGaLa₄O₈) | — | Fig 2b "2.0 % LiAlLa₄O₈" | ✅ 본문·그림 일치 |
| **9** | **신규/기보고 도판트 수** (§19.3d → **§20.1 확정**) | "**29 novel**, plus the 30 previously reported" | **Table S2 ∩ Fig 1 노랑 = 30 · ∩ 파랑 = 29**(파랑 중 미합성 = Sb 단 하나) | **Fig 1 픽셀: 노랑 30 / 파랑 30 = 60종**, 캡션 "except Sb" | 🔴 **확정 — 본문의 두 숫자가 뒤바뀌었다.** 스크리닝된 59 = **신규 30 + 기보고 29**. Fig 3/4/5/6 x축도 전부 59종(Sb 없음) |
| **10** | **Fig 3a y축 절단** (§19.3c) | "total LLZO content is generally high (>95 %)" | — | **패널 a 하한 = 80 wt%**, Mo·Rh·Pd·Te(선호 site)가 축 아래로 사라짐 | 🔴 **절단 사실이 본문·캡션 어디에도 없다.** 인용 시 "80 wt% 이상만 표시된 축" 병기 |
| **11** | **선호 site cubic% 서술** (§19.3a → **§20.4 격상**) | ">90 % c-LLZO in **most cases**" | **Table S5 cubic 열: 25/59 = 42 %, 중앙값 75.1 %, 41 %가 70 % 미만** | Fig 3b 픽셀: 25/59 = 42 %, 중앙값 74.9 % | 🔴 **"most cases" 불성립 — 이제 그림이 아니라 저자 자신의 표로 확정.** 대신 "선호 site가 3자리 중 1위 = 49/51(96 %)"이 정확한 형태 |
| **12** | **이온성 액체 재측정 온도** (§19.6) | 본문 p.9 **60 °C** / Experimental **60 °C** | — | **Fig 6 캡션 55 °C** | 🟡 2:1로 **60 °C** 채택하되 캡션 55 °C 병기 |
| **13** | **σ 결측 5종 — `Y` vs `Yb`** (§19.5 → **§20.2 확정**) | — | **Table S5: Y 측정됨(2.46×10⁻⁵) · Yb 공란** | **Fig 4a·4b: 39 Y 회색 · 70 Yb 채색** | ✅ **해결 — 논문 자체 오류.** **Fig 4의 두 패널이 Y·Yb 칸을 맞바꿔 실었다.** 중재 근거: **Fig 3이 59/59 전부 Table S5와 같은 라벨**(cubic% 최대 \|Δ\| 0.44 pp)이라 Table S5+Fig 3 : Fig 4 = 2:1. 또 Fig 4의 "Yb" 값(σ_i 2.75×10⁻⁵ · σ_e 3.37×10⁻⁸)이 **Table S5의 Y 값의 1.12× / 1.07×** = 역판독 오차 안 → **같은 데이터가 다른 칸에 실린 것**. → **채택: Y(La) σ_i 2.46×10⁻⁵ · σ_e 3.14×10⁻⁸ / Yb(La) σ 미측정** |
| **14** | **`Rh` vs `Ho`** (§19.5 → **§20.3 확정**) | — | Table S5: Rh 2.58×10⁻⁶ · Ho 1.57×10⁻⁵ | Fig 4a 픽셀: Rh 2.75×10⁻⁶ · Ho 1.73×10⁻⁵ | ✅ **해결 — 논문은 무결.** 두 값 다 역판독 오차(1.07×/1.10×) 안에서 일치한다. **어긋난 건 1차 digest가 `Ho`를 `Rh`로 잘못 적은 우리 쪽 오타**뿐 (§6 교정 완료) |
| **15** | **">10× 36종" 계수** (§20.3) | "**36** different dopants yield a >10x improvement" | Table S5 기계 파싱: 엄격히 **35종** | Fig 4a 픽셀도 Ho 포함 시 36 | 🟡 **35(엄격) / 36(Ho 포함).** Ho = 1.57×10⁻⁵ = undoped(1.62×10⁻⁶)의 **9.7×** — 두 값을 유효숫자 2자리로 반올림하면(1.6×10⁻⁵ / 1.6×10⁻⁶) 정확히 10×가 된다. **저자의 36은 반올림 계수**로 보는 게 정합적. 인용 시 병기할 것 |
| **16** | **Table S4 Ga1 자리 좌표** (§20.4) | — | Table S4: Ga1 **x = 0.0375**, mult 24 | — | 🟡 **`0.375`의 오타로 판단.** Ia-3d 가넷 Li1(24d) = (0.375, 0, 0.25)이고 Ga1은 **같은 mult 24**로 실려 있다. 같은 표의 Ca1(0.125,0,0.25)=La1(24c)·W1(0,0,0)=Zr1(16a)은 **치환 자리 좌표를 그대로 복사**했다 → Ga1만 자릿수가 하나 밀렸다. **구조 정보 자체엔 영향 없음**(점유율·GoF는 정상) |

---

## 17. 인용 가능 문장 (deck/paper용)

- "Anderson et al. (Adv. Energy Mater. 2024) synthesised **59 dopants on each of the three LLZO sites
  (177 samples)** by high-throughput sol–gel and measured phase content, ionic and electronic
  conductivity, high- and low-voltage stability, CCD and one-year air stability under identical
  conditions — **36 dopants gave >10× the ionic conductivity of undoped LLZO**, with Ga and Fe reaching
  1.2 × 10⁻³ S cm⁻¹."
- "**The oxidative limit of LLZO was 3.8–3.9 V for all 59 dopants**; what changed was the *amount* of
  decomposition (integrated 3.8–4.3 V charge, 0.26–6.7× the undoped value), i.e. dopants provide
  *kinetic* protection rather than shifting the thermodynamic decomposition voltage [Anderson 2024]."
  — **우리 axis ①(S²⁻-limited onset, 조성 불변)의 산화물 평행선.**
- "In the same dataset the **critical current density correlated with low-voltage stability but not with
  electronic conductivity**, leading the authors to argue that dendrite failure starts at the Li‖SE
  interface rather than inside the pellet [Anderson 2024]." — ⚠ 인용 시 §10의 3가지 한계 병기 필수.
- "**Applying the paper's own five merit thresholds (cubic > 94 %, σ_i > 5 × 10⁻⁵ S cm⁻¹,
  σ_e < 2.5 × 10⁻⁸ S cm⁻¹, ∫Idt < 1.39 mAh g⁻¹, CCD ≥ 0.4 mA cm⁻²) as a sequential funnel leaves zero
  survivors among the 59 dopants** — which is precisely why the authors report a full matrix with
  per-axis merit flags and defer the trade-off to codoping." (⚠ **본 digest의 재구성**, 논문에 없는 표)
- "The authors conclude that combining dopants is unavoidable — one for the cubic phase and conductivity
  (Ga, Fe), others to widen the stability window (Ti, Sc, Dy) and to improve air stability (Ba, Pr, K,
  Ti on the La/Zr sites) — and that *'machine learning algorithms are expected to be needed to
  effectively screen codoped materials'* [Anderson 2024]." — **우리 codoping ML의 문헌적 요청.**
- (원소 수렴) "Three independent screens on three different hosts — an experimental 59-dopant garnet
  screen, a 17,230-compound coating screen and our 47-dopant argyrodite cascade — converge on **Sc**
  (and, in the garnet and argyrodite cases, **W**) at the top, although for different reasons."
  ⚠ **원소 일치까지만.**

---

## 18. 기법 용어 미니사전

- **c-LLZO / t-LLZO** — 입방(Ia-3d, 고전도, Li 무질서 3D 네트워크) / 정방(I4₁/acd, 저전도, Li 질서·2D).
  도핑의 1차 목적은 상온에서 입방상을 안정화하는 것.
- **I-4̄3d** — c-LLZO(Ia-3d)의 부분 질서화 하위 공간군. **Mo-Kα 10.15° 특성 피크**로 식별.
  이 논문에서 **Ga on Li 시료에서만** 관측 → Ga/Fe 초고전도의 후보 설명.
- **supervalent 치환** — 자리보다 높은 원자가 이온으로 치환(예 Ga³⁺→Li⁺, Ta⁵⁺→Zr⁴⁺).
  전하 보상으로 **Li 공공**이 생겨 입방상 안정화 + 전도↑. 반대말 **isovalent**(Sm/Gd→La, 이득 작음).
- **defect energy (결함에너지)** — 도펀트를 어느 자리에 넣을 때의 형성에너지. 이 논문은 **직접 계산 없이
  ref [12](Ceder 2015)에서 인용**. 최소값 자리 = "최적 자리".
- **bond valence mismatch** — 결정 자리의 기하로부터 계산한 결합가 합과 이온의 형식 원자가의 차이.
  자리 적합도의 값싼 서술자. ⚠ **우리 BVSE(Li 이동 에너지 지형)와 다른 물건** —
  이쪽은 *자리 적합*, 우리 것은 *경로 장벽*.
- **∫Idt (HV)** — 3.8–4.3 V CV 전류를 시간 적분한 비용량(mAh/g). **분해량의 스칼라 지표**.
  낮을수록 passivation 우수. undoped = 1.39.
- **V_min / V_max** — CV로 판독한 저/고전압 안정 한계. V_min은 "시료 전류가 blank 아래로 꺼지는
  최고 전압"이라는 **조작적 정의**이지 열역학량이 아님.
- **blank 차감** — 카본블랙+PVDF만으로 만든 전극의 CV를 빼서 SE 고유 신호만 남기는 절차.
  이 논문 ESW 축의 핵심 처리.
- **carbon-composite CV ESW** — SE 분말을 카본과 섞어 전자 경로를 깔아 kinetic 제약을 없앤 뒤 CV로
  분해 전압을 재는 방법 (원조 Han 2016 [34]). 두꺼운 펠릿 DC 측정의 "7–9 V" 과대평가를 교정.
  ⚠ 우리 규율: 이건 여전히 **kinetic 측정**이고 0 K grand-potential 창과 직접 비교 불가.
- **CCD (critical current density)** — Li 대칭셀에서 단락(dendrite 관통)이 일어나는 전류밀도.
  이 논문 규약: 반쪽사이클당 0.10 mAh/cm² 고정, 0.05 mA/cm² 스텝, 미도달 시 **하한 `>x`** 보고.
- **sacrificial powder** — 소결 시 시료를 같은 조성 분말로 덮어 Li 증발·오염을 막는 기법.
  여기선 **Li₇.₅La₃Zr₂O₁₂**.
- **Li 과량 dispensed (8.4)** — 소결 중 Li 손실 보상을 위해 명목 조성보다 20 % 많이 넣는 관행.
  → **최종 Li 함량은 미측정**이므로 "Li 7.0 조성"이라 단정 못 함.
- **full-factorial matrix screening** — 깔때기(순차 게이트) 대신 **모든 후보 × 모든 축**을 다 재고
  축별 merit flag만 붙이는 설계. 정보 소실이 없는 대신 **최종 답이 하나로 안 좁혀진다**.
  이 논문의 선택이자, §3e에서 보듯 **그럴 수밖에 없었던 선택**.

---

## 19. 🔴 2차 패스 (2026-08-04) — 본문 그림 픽셀 독립 검증 ★★★

> **왜 다시 했나.** 사용자가 이 논문(inbox `51.`, 분류 폴더 `DFT`)을 다시 먹였다. 그런데 이번 inbox에는
> **본문 12 pp만 있고 SI가 없다**. 1차 digest(2026-07-28)는 SI Table S5를 전수 정독해 썼으므로,
> 같은 걸 반복하는 대신 **SI를 전혀 안 보고 본문 그림만으로 같은 수치를 복원**해서 1차 결과를 교차검증했다.
> 스크립트 `tools/litdb/anderson2024_fig_verify.py` (PIL만, numpy 없음),
> 복원표 `db/properties/anderson2024_llzo_dopant_screening_recovered.csv` (59행).
>
> **방법**: Fig 4는 σ를 연속 컬러맵 주기율표로 그린다 → 컬러바를 LUT로 만들어 셀 채움색을 역변환.
> Fig 3a/3b는 마커를 색(주황=최적자리 / 진홍·남색=대체자리)으로 분리해 y좌표를 wt%로 환산.
> **Table 1에 인쇄된 18종이 그대로 ground truth**라서 역변환 정확도를 자기검증할 수 있다.

### 19.1 역판독 정확도 — 먼저 이것부터 (이게 안 맞으면 아래 전부 무효)

| 대상 | n | 잔차 | 판정 |
|---|---:|---|---|
| σ_i (Fig 4a → Table 1) | 18 | \|Δlog₁₀\| **중앙값 0.024 (=1.06×)**, 최대 0.083 (=1.21×), 편의 +0.002 dex | ✅ |
| σ_e (Fig 4b → Table 1) | 18 | \|Δlog₁₀\| 중앙값 0.086, 최대 0.112, **계통편의 +0.064 dex** → 보정 후 사용 | ✅ |
| garnet wt% (Fig 3a → Table 1) | 18 | \|Δ\| **중앙값 0.03 pp**, 최대 0.10 pp | ✅✅ |
| cubic wt% (Fig 3b → Table 1) | 18 | \|Δ\| **중앙값 0.15 pp**, 최대 0.53 pp | ✅✅ |

**본문에만 있고 Table 1엔 없는 수치와도 독립 일치** (= 역판독이 진짜 맞는다는 4중 확인):

- **Ta**: 픽셀 σ 2.44×10⁻⁴ / cubic **70.9 %** / garnet 94.5 % ↔ 본문 *"2.5×10⁻⁴ … 70 % c-LLZO and 24 % t-LLZO
  along with just under 6 % Li₅La₃Ta₂O₁₂"* — **70.9 + 23.6 = 94.5** 로 회계까지 맞는다.
- **Sm 3.03×10⁻⁵ / Gd 5.44×10⁻⁵** ↔ 본문 2.92×10⁻⁵ / 5.52×10⁻⁵ (오차 4 % / 1.5 %).
- **Tm 6.58×10⁻⁶ vs In 2.58×10⁻⁵ = 3.9배** ↔ 본문 *"Tm … about four times less conductive than In"*.
- **Ga on La / Ga on Zr cubic = 33.6 / 38.7 %** ↔ Fig 2b Rietveld 34.7 / **38.7 %**.
- 1차 digest가 SI에서 옮긴 값들과도 일치: Au garnet 85.08(SI 85.13) · Ti cubic 58.0(58.21) ·
  Co 44.13(44.13) · Ba 30.4(30.70) · Si 25.74(25.79) · Pd 26.8(26.91) · Mo 51.9(51.85) · Te 4.9(4.70).

> 🔑 **즉 1차 digest(SI 기반)와 2차 패스(그림 기반)가 서로를 독립적으로 검증했다.** 이 논문의 수치는
> 우리 litdb 안에서 **두 경로로 확인된 몇 안 되는 데이터**다. 아래 §19.5의 4개 칸만 예외.

### 19.2 ★ 본문 계수 주장 — 전부 재현됨

- *"36 dopants yield a >10× improvement"* → 픽셀에서 **정확히 36종** (기준 undoped 1.6×10⁻⁶,
  측정된 도판트 54종 중). 1차 digest의 Table S5 전수 재현과 **같은 36**.
- *"just three show a lower conductivity than undoped"* → 픽셀에서 **Pd 1.07×10⁻⁶ · Pt 1.48×10⁻⁶ ·
  Ge 1.70×10⁻⁶** (Ge는 1.6×10⁻⁶ 경계 바로 위 — 역판독이 컬러바 하단에서 ~20 % 높게 나오는 것과 정합).
  SI 값 Ge 1.40 / Pt 1.27 / Pd 0.825 ×10⁻⁶ 와 **같은 3종**.
- *"nearly all doped samples have a lower σ_e between 1 and 5×10⁻⁸"* → 픽셀 **44/54 = 81 %** 가 그 구간.
  구간 밖 상위: **Co 9.3×10⁻⁷ · Ru 1.95×10⁻⁷ · Cu 1.33×10⁻⁷ · Ir 1.25×10⁻⁷** — 1차 digest의 위험군과 동일.

### 19.3 🔴 신규 — 본문 진술이 그림과 어긋나는 4건

**(a) "선호 site는 대부분 >90 % cubic" 은 소수파다.**
본문 §2.1: *"the c-LLZO content is nearly uniformly favored for the preferred site giving **>90 % c-LLZO
in most cases**"*. 픽셀 실측 59종 선호-site cubic%:

| | n | 중앙값 | >90 % | 70 % 미만 |
|---|---:|---:|---:|---:|
| **선호(주황)** | 59 | **74.9 %** | **25 (42 %)** | **24 (41 %)** |
| 비선호 A(진홍) | 51 | 26.5 % | 0 | — |
| 비선호 B(남색) | 59 | 30.4 % | 0 | — |

70 % 미만인 24종: Te 5 · Si 26 · Pd 27 · Ba 30 · Pt 35 · In 42 · Pr 42 · Co 44 · K 44 · Cu 45 · Mn 47 ·
Au 49 · Nd 50 · Mo 52 · Rb 54 · Rh 56 · Ho 57 · Tb 57 · Ti 58 · Ir 59 · Ag 60 · P 61 · Sc 62 · Na 68.
→ **"most cases"가 아니라 42 %다.** 1차 digest §5b도 이 문장을 그대로 옮겼으니 **함께 교정**한다.
비선호 site가 20–40 %대라는 쪽은 잘 맞는다(67–71 %가 그 구간).

**(b) 그런데 "예측한 site가 최선"이라는 핵심 주장 자체는 강하게 성립한다** — 두 진술을 분리해야 한다.
3개 site를 다 읽을 수 있는 51종에서 **선호 site가 cubic% 1위 = 49/51 (96 %)**. 꼴찌는 **Mo 하나뿐**
(선호 Zr 52 % < Li 67 % < La 76 %). → *"어느 자리에 넣을지"* 예측력은 진짜고, 틀린 건 *"얼마나 입방화되는지"* 다.
**이게 이 논문에서 우리가 가져갈 가장 단단한 명제다.**

**(c) Fig 3a의 y축은 80 wt%에서 잘려 있다 — 실패 시료가 그림에서 사라진다.**
선호 site 기준 **Mo · Rh · Pd · Te** 4종은 총 garnet < 80 wt%라 패널 a에 **점이 아예 없다**
(대체 site까지 세면 B·Al·Ca·Y·Ba·Nd·Gd·Tm·Lu·Mo·Te·Ta 등 추가). 본문 *"The total LLZO content is
generally high (>95 %) in most samples"* 는 **잘린 축 위에서 읽힌 인상**이다. 축이 잘렸다는 말은 어디에도 없다.

**(d) Fig 1은 도판트를 60종 칠한다 — 본문의 "29 novel"과 안 맞는다.**
픽셀 분류: **노랑(novel) 30 · 파랑(previously reported) 30 = 60종**.

- 노랑 30: Na P K V Cu Se Rh Pd Ag Cd In Sn Cs Lu Re Ir Pt Au Tl Pb Bi Pr Sm Eu Tb Dy Ho Er Tm Yb
- 파랑 30: B Mg Al Si Ca Sc Ti Cr Mn Fe Co Ni Zn Ga Ge Rb Sr Y Nb Mo Ru **Sb** Te Ba Hf Ta W Ce Nd Gd

Fig 1 캡션이 *"all the dopants (yellow and blue, **except Sb**) were tested and screened"* 라 하고,
Fig 3/4/5/6의 x축·칸에도 **Sb가 없다(정확히 59종)**. 즉 **합성 60종 / 스크리닝 59종**이고,
본문의 *"29 novel, plus the 30 previously reported"* 는 **신규가 30, 기보고-스크리닝분이 29**로 뒤바뀐 것이다.
→ 이건 §16 #7(177 vs 180)과 별개 항목이다. ⚠ 다만 **180 패턴의 정체**는 SI Table S2(177행)를 본
1차 판정("177 도핑 + undoped 3")과 이번 Sb 해석("60×3") 중 어느 쪽인지 **SI 없이는 확정 못 한다** —
§19.5의 미해결 목록에 함께 둔다.

### 19.4 ★ DFT/BV 서술자 예측력 — 이 논문의 "DFT" 부분을 정량화

사용자가 이 논문을 `DFT` 폴더로 분류했지만 **자체 DFT는 0건**이고(§4d), DFT는 **ref [12] Miara/Ceder 2015의
결함에너지를 Fig 3d에 옮겨 그린 것**뿐이다. 2차 패스에서 Fig 3c(BV mismatch)·3d(결함에너지)를
site별로 되읽어 그 서술자들의 값어치를 처음으로 수치화했다.

| 질문 | 결과 |
|---|---|
| 저자의 "이론 최적 site" = argmin(결함에너지) 인가 | **38/38 일치** (마커 겹침으로 19종 판정 보류). 정의대로 쓰였다 ✅ |
| argmin(BV mismatch) = argmin(결함에너지) 인가 | **18/35 = 51 %** 만 일치 |
| 불일치의 방향 | **17건 중 15건이 "BV→Li site / DFT→Zr site"** (Cr Cu Hf Ir Mn Mo Nb Ni P Pd Rh Se Ta Ti + Cd·Tl은 La→Zr, Zn만 반대) |
| 서술자 *크기* 가 cubic wt%를 예측하는가 | **BV ρ = −0.05 (n=56) · 결함에너지 ρ = 0.00 (n=54)** — 사실상 무상관 |

> 🔑 본문은 *"[BV calculations] have difficulty differentiating between tetrahedral (Li) and octahedral (Zr)
> site preference"* 라고 **정성적으로만** 말한다. 픽셀로 재보면 그 실패는 **적중률 51 %, 그리고 거의 전부
> 한 방향(Li로 과잉 배정)**이다 — 동전던지기 수준이고, 편향된 동전이다.
>
> 🔑 그리고 **두 서술자 다 크기로는 아무것도 예측 못 한다(ρ≈0)**. 저자들의 Ga/Fe 반례
> (*"Ga and Fe have considerably higher defect energies and bond valence mismatches than … Sn"*)는
> 예외가 아니라 **전체 경향**이었다.

**우리 캠페인에 주는 함의 (`tools/cascade` 설계)**:

1. **자리 선택(site assignment)과 효과 크기(magnitude)는 다른 문제다.** 결함에너지는 앞쪽만 답한다(96 % 적중).
   우리 cascade에서 결함/치환 에너지를 **순위 점수로 쓰면 안 되고 게이트로만** 써야 한다는 근거.
2. **BV mismatch는 결함에너지의 대체재가 아니다** — 51 % 적중, Li/Zr 구분 실패. 우리 BVSE(경로 장벽)와는
   애초에 다른 물건이라는 §18 규율에 더해, **"값싼 자리-적합 서술자" 자체가 못 미덥다**는 실험 증거.
3. 이건 `ren2026`의 Φ=z/r 붕괴(R²=0.065)와 **같은 결의 결과**다: 0-비용 정전기 서술자는
   *사전필터*지 *순위기*가 아니다. → [[ren2026_li2zrcl6_low_ion_potential_doping]] §4.5와 나란히 인용할 것.

### 19.5 ~~🔴🔴 미해결~~ → ✅ **2026-08-04 §20에서 전부 확정됨** (아래는 당시 기록 보존)

> **결론만 먼저**: `Rh↔Ho`는 **1차 digest의 철자 오타**였고(논문 무결), `Y↔Yb`는 **논문의 Fig 4 오류**다
> (Table S5 + Fig 3 채택). **인용 금지 해제** — 근거·중재 과정은 **§20.2·§20.3**.

Fig 4a에서 **σ 결측(회색)인 도판트**와 **>10× 36종 목록**을 1차 digest의 SI Table S5 판독과 대조:

| | 1차 digest (SI Table S5) | 2차 패스 (Fig 4a 픽셀) |
|---|---|---|
| σ 결측 5종 | Er · Mo · Tb · Te · **Yb** | Er · Mo · Tb · Te · **Y** |
| >10× 36종 중 차이 | … **Rh** … **Y** … | … **Ho** … **Yb** … |

**두 목록의 차이가 `Y↔Yb` · `Rh↔Ho` 두 쌍의 맞교환뿐이고, 양쪽 다 정확히 36종이다.**
Fig 4a 픽셀 실측: **Y = 회색(값 없음)**, **Yb = 2.75×10⁻⁵**, **Rh = 2.75×10⁻⁶**, **Ho = 1.73×10⁻⁵**
(란탄족 줄 크롭으로 육안 재확인: Tb·Er 회색, **Yb 분홍**).

원인은 둘 중 하나 — ① 논문 자체가 Fig 4와 Table S5에서 이 두 쌍을 뒤바꿔 실었거나,
② 1차 digest의 SI 전사에서 기호가 뒤바뀌었거나. **SI PDF가 inbox에 없어 확정 불가.**

> ~~⛔ **인용 규율**: 확정 전까지 **Y · Yb · Rh · Ho 4종의 σ_i/σ_e는 어느 쪽 값도 단독 인용 금지.**~~
> ✅ **2026-08-04 해제** — 사용자가 SI PDF를 inbox에 다시 넣었고, Table S5가 **텍스트 레이어**라
> 손 전사 없이 기계 파싱됐다. 결과는 §20.

### 19.6 부수 — 소소한 신규 확인 4건

- **§5b의 "미동정 2차상 6종" 목록 자기교정**: 1차 digest는 **Ga**·Re·Ir·Pt·Pd·Au라 적었는데,
  Fig 3a x축 라벨을 확대해 보면 별표는 **`*Ge` `*Pd` `*Re` `*Ir` `*Pt` `*Au`** 다 → **Ga가 아니라 Ge**.
  (Ga는 Li-site 그룹이라 "전부 Zr 자리"라는 같은 문장과도 모순이었다. Ge로 고치면 6종 전부 Zr 자리 ✅.)
- **Fig 6 캡션은 55 °C, 본문·Experimental Section은 60 °C** — 이온성 액체 저전압 재측정 온도가 어긋난다.
  1차 digest §9는 60 °C를 채택했는데, 캡션 55 °C를 병기해 두는 게 맞다.
- **Te는 Fig 5·Fig 6에도 없다.** 두 CV 그림 모두 undoped + **58종**뿐(Zr 그룹에서 Te만 빠짐).
  garnet 4.7 %라 전극을 못 만든 것으로 보이나 **사유 서술 없음** — §15.9의 "결측 사유 공란" 항목에 Te 추가.
- **Fig 3c/3d에는 Re가 없다** (BV mismatch·결함에너지 둘 다 미제공), **Fig 3d의 Yb 자리는 `n/a`**
  (Miara 2015가 Yb를 안 다룸). 즉 결함에너지가 실제로 존재하는 도판트는 **57종**이다.

### 19.7 재현

```
python tools/litdb/anderson2024_fig_verify.py      # 전체 출력 = litdb/inbox/_51_verify_out.txt
```

> ⚠ **본문 PDF 가 inbox 에 있어야 돈다**(현재 inbox 에는 SI 만 있다). `litdb/inbox/` 는 gitignore
> 대상이라 출력 txt 는 repo 에 남지 않는다 — **결론·수치는 전부 이 §19 본문과
> `..._recovered.csv` 에 있으므로 txt 는 편의용 사본일 뿐**이다.

출력물: `db/properties/anderson2024_llzo_dopant_screening_recovered.csv` (59행).
**`source` 열이 핵심** — `paper Table 1`(인쇄값 18종) vs `pixel readback (Fig 3/4)`(우리 역판독 41종)를
**절대 섞어 인용하지 말 것**. 역판독 정확도 근거는 §19.1.

> ⚠ **이 CSV의 `Y`·`Yb` 행 σ 값은 Fig 4 기준이라 라벨이 뒤바뀐 상태다**(§20.2).
> σ를 쓸 때는 **§20의 `..._tableS5.csv`를 쓸 것.** 구조(garnet%/cubic%)는 두 CSV가 일치하므로 무관.

---

## 20. ✅ 3차 패스 (2026-08-04) — **SI PDF 직접 재판독**, §19.5 확정 ★★★

> **왜 또 했나.** 사용자가 이번엔 **SI PDF(17 pp)** 를 inbox에 넣었다(분류 폴더 `DFT`).
> §19.5가 남긴 4칸을 확정하는 게 목적이었고, 부수적으로 **1차 digest의 SI 손 전사 전체가
> 기계 파싱으로 재검**됐다. Table S5·S2·S3는 래스터가 아니라 **텍스트 레이어**라 그대로 읽힌다
> (Table S1·S4와 Fig S1–S14는 이미지 → 300 dpi 렌더 후 육안 판독).
>
> 스크립트 `tools/litdb/anderson2024_si_tableS5.py` · 출력 `litdb/inbox/_51si_verify_out.txt`
> · 표 `db/properties/anderson2024_llzo_dopant_screening_tableS5.csv` (59행 + undoped).

**이제 이 논문은 세 경로로 검증됐다**: ①1차 SI 손 전사(2026-07-28) · ②2차 본문 그림 픽셀
역판독(SI 미열람) · ③3차 SI 텍스트 기계 파싱. **③은 ①의 독립 재검이자 ②의 정답지**다.

### 20.1 시료 회계 — Table S2로 확정 (§16 #7·#9)

```
조성 행 수 = 177   고유 도판트 = 59   자리/도판트 = 3   Sb 포함? 아니오
Fig 1 노랑(novel) ∩ Table S2 = 30 · 파랑(reported) ∩ Table S2 = 29   (합 59)
파랑 중 미합성 = ['Sb']
```

- **177 = 59 × 3**, Sb는 Table S2에 **아예 없다**. → 본문 "180 PXRD patterns"의 나머지 3은
  **세트별 undoped 3장**이고, 2차 패스가 세워둔 **"Sb 포함 60×3=180" 가설은 기각**된다.
  **1차 digest §16 #7 판정이 맞았다.**
- **스크리닝 59 = 신규 30 + 기보고 29** → 본문 *"29 novel, plus the 30 previously reported"* 는
  **두 숫자가 뒤바뀐 것이 확정**(§16 #9). Fig 1이 파랑을 30개 칠한 건 **문헌에 보고된 도판트 30개**를
  칠한 것이고 그중 Sb만 여기서 안 만들었다 — 그림에 잘못은 없다.

### 20.2 🔑 `Y` vs `Yb` — **논문의 Fig 4가 두 칸을 맞바꿔 실었다**

**Table S5 원문:**

| | site | garnet % | cubic % | σ_i (S/cm) | σ_e (S/cm) | V_max | ∫Idt | V_min |
|---|---|---:|---:|---|---|---:|---:|---|
| **Y** | La | 94.80 | 94.60 | **2.46×10⁻⁵** | **3.14×10⁻⁸** | 3.9 | **0.53** | < 0.1 |
| **Yb** | La | 94.95 | 76.26 | *(공란)* | *(공란)* | 3.9 | 1.87 | < 0.1 |

Fig 4a·4b는 **정확히 반대**다 — 원자번호가 인쇄돼 있어 오독 여지가 없다: **39 Y = 회색(값 없음)**,
**70 Yb = 채색**. (란탄족 줄은 57 La…70 Yb이고 **71 Lu는 본체**에 있다 = 격자 매핑 정상.)

**중재 — Table S5를 채택한 근거 3가지:**

1. **Fig 3이 Table S5 편이다.** Fig 3a/3b 픽셀 복원표와 Table S5를 **59종 전수** 대조하면
   cubic% 최대 \|Δ\| **0.44 pp**(Nb), **2 pp 초과 불일치 0건**. Y·Yb도 각각
   **94.26 ↔ 94.60** / **75.96 ↔ 76.26** 으로 제자리에 있다.
   → **Table S5 + Fig 3 : Fig 4 = 2 : 1.**
2. **Fig 4의 "Yb" 칸 값이 Table S5의 Y 값이다.** σ_i 2.75×10⁻⁵ vs **2.46×10⁻⁵ = 1.12×**,
   σ_e 3.37×10⁻⁸ vs **3.14×10⁻⁸ = 1.07×** — 둘 다 §19.1이 정한 역판독 오차(중앙값 1.06×) 안.
   **없는 데이터가 생긴 게 아니라 같은 데이터가 다른 칸에 실렸다.**
3. **두 패널(a·b)에서 똑같이 어긋난다** → 우연한 렌더링 사고가 아니라 **그림 생성 단계의
   라벨 오배정** 한 번이 두 패널에 전파된 형태.

> ### ✅ 채택값
> **Y(La): σ_i = 2.46×10⁻⁵ S/cm · σ_e = 3.14×10⁻⁸ S/cm (측정됨)**
> **Yb(La): σ 미측정 (결측 5종 = Er · Mo · Tb · Te · Yb)**
>
> 🔑 **§8의 서사가 완성된다.** "고전압 passivation 최강군 **Sc·Y·Dy·Er**"(∫Idt: Dy −0.05 ·
> **Sc 0.36 · Y 0.53** · Er 0.57 ≪ undoped 1.39)의 나머지 축을 이제 다 채울 수 있다:
>
> | | ∫Idt | σ_i (S/cm) | cubic % | σ_e (S/cm) |
> |---|---:|---|---:|---|
> | Dy(La) | **−0.05** | 3.27×10⁻⁵ | 93.83 | 3.85×10⁻⁸ |
> | Sc(Zr) | 0.36 | 2.46×10⁻⁵ | **62.86** | 2.05×10⁻⁸ |
> | **Y(La)** | 0.53 | **2.46×10⁻⁵** | **94.60** | 3.14×10⁻⁸ |
> | Er(La) | 0.57 | *(결측)* | 73.31 | *(결측)* |
>
> → σ가 있는 건 **Dy·Sc·Y 셋**이고(Er만 결측), 그중 **Table S5 캡션의 cubic > 94 % merit 컷을
> 통과하는 건 Y 하나뿐**이다(Dy 93.83으로 아깝게 탈락). 즉 **Y = "산화 억제 상위군 + 고입방화"를
> 동시에 만족하는 유일한 도펀트**. **우리 cascade의 Sc₂O₃ score 1위와 나란히 놓을 때 Y도 후보로
> 올릴 근거**이고, Fig 4만 봤다면 이 칸이 통째로 비어 있었다.

### 20.3 🔑 `Rh` vs `Ho` — **논문 문제가 아니라 우리 오타였다**

```
Rh   Table S5 2.58e-06   Fig 4a 픽셀 2.754e-06   비 1.07×   undoped 대비  1.6×
Ho   Table S5 1.57e-05   Fig 4a 픽셀 1.729e-05   비 1.10×   undoped 대비  9.7×
```

두 값 다 역판독 오차 안에서 **일치**한다 — 맞교환 같은 건 없었다. **Rh는 undoped의 1.6×**라
">10×" 목록 근처에도 못 간다. 그런데 1차 digest §6의 36종 목록엔 Rh가 들어 있었다
→ **`Ho`를 `Rh`로 잘못 적은 철자 오타**(두 기호가 letter-swap이다). §6에서 교정 완료.

**그리고 그 김에 본문의 "36"도 다시 셌다:**

| 기준 | 계수 |
|---|---:|
| σ_i > 10 × undoped(1.62×10⁻⁵) **엄격** | **35종** |
| + Ho (1.57×10⁻⁵ = **9.7×**) | **36종** |

Ho는 유효숫자 2자리로 반올림하면 **1.6×10⁻⁵ / 1.6×10⁻⁶ = 10×** — 저자들이 이렇게 넣은 것으로
보인다. **인용 시 "35종(엄격)/36종(반올림)"으로 병기할 것**(§16 #15).
*"just three show a lower conductivity"* 는 **정확히 3종**(Pd 8.25×10⁻⁷ · Pt 1.27×10⁻⁶ ·
Ge 1.40×10⁻⁶)으로 ✅ 재확인됐다.

### 20.4 SI 표로 재확인된 것 (§19의 나머지 판정은 전부 유지)

| 대상 | 2차 패스(그림 픽셀) | 3차 패스(SI 표) | 판정 |
|---|---|---|---|
| 선호 site cubic% 중앙값 | 74.9 % | **75.1 %** | ✅ |
| 〃 >90 %인 도판트 | 25 / 59 (42 %) | **25 / 59 (42 %)** | ✅ **본문 "most cases" 불성립 확정** |
| 〃 70 % 미만 | 24 (41 %) | **24 (41 %)** | ✅ |
| cubic% 전수 대조 | — | 최대 \|Δ\| **0.44 pp**, >2 pp **0건** | ✅✅ |
| σ_i < undoped | Pd·Pt·Ge | **Pd·Pt·Ge** | ✅ |
| Ti CCD | Table 1 · Fig S12 = **0.55** | Table S5 = **0.65** | ✅ **Table S5 오타**(§16 #1 유지) |

**§16 #11이 격상된다** — "선호 site는 대부분 >90 % cubic"이 틀렸다는 근거가 이제 *우리 픽셀 판독*이
아니라 **저자 자신의 표**다. 인용할 때 방어력이 다르다.

**1차 digest의 SI 손 전사는 전량 무결이었다** — Table S3 밀도 8종, Table S4 GoF·점유율·격자상수,
Table S5 인용 수치, Table S2 177행, Fig S1–S14 캡션까지 **불일치 0건**. (§4b의 Ga/W/Ca GoF 표,
§4c의 CCD 판독 규칙, §3d의 merit 컷 5개 전부 원문과 일치.)

**신규 발견 1건 — Table S4의 Ga1 좌표 오타**(§16 #16): Ga1이 **x = 0.0375**로 실려 있는데
Ia-3d 가넷 **Li1(24d) = (0.375, 0, 0.25)** 이고 Ga1도 **multiplicity 24**다. 같은 표에서
**Ca1 (0.125, 0, 0.25) = La1(24c)**, **W1 (0, 0, 0) = Zr1(16a)** 으로 치환 자리 좌표를 그대로
복사했으므로 **Ga1만 자릿수가 하나 밀린 것**. 점유율·GoF·격자상수는 정상이라 결론엔 영향 없다.

> 📎 **부수 확인 — Ga 모델만 Li를 전하보상했다.** Ga 시료: Li1 24×0.2667 + Li2 96×0.4667 = 51.2
> → **6.4 Li/f.u.** = 7 − 3×0.2 ✓ (Ga³⁺ ↔ 3Li⁺). 반면 **W·Ca 시료는 Li1=Li2=0.4667 = 7.0 Li/f.u.**
> 로 undoped 값을 그대로 뒀다(W⁶⁺면 6.6이어야 함). ⚠ 다만 **Mo-Kα X-선에서 Li는 거의 안 보이므로
> GoF 판별에 실질 영향은 없다** — 판별을 만드는 건 도펀트 자신의 산란 대비다. 그래서 **무거운 W의
> 마진이 21 %로 크고, 가벼운 Ga가 2.3 %로 작다**(§4b의 경고와 같은 결론에 독립적으로 도달).

### 20.5 §3e 깔때기 재실행 — **SI 표로도 생존자 0**

Table S5 캡션의 merit 5컷을 기계로 순차 적용:

```
시작 59종
cubic > 94 %   → 19종   Al B Ce Fe Ga Gd Lu Mg Nb Pb Re Ru Sm Sr Tm V W Y Zn
σ_i > 5e-5     →  6종   Al Fe Ga Gd Ru W
σ_e < 2.5e-8   →  1종   Ga
∫Idt < 1.39    →  0종
CCD ≥ 0.4      →  0종
```

**1차 digest §3e의 59 → 19 → 6 → 1(Ga) → 0 이 정확히 재현된다.** Ga가 ∫Idt = 1.46 > 1.39
(undoped)에서 탈락하는 것까지 같다. → **"이 논문이 깔때기를 안 쓴 게 아니라 쓸 수 없었다"**는
digest의 최대 발견은 **저자 자신의 표를 기계로 돌려도 그대로**다. 우리 cascade 가중 score 설계의
외부 방어 논거로 **인용 가능**(§14).

> ⚠ **정직하게 적어두면, 이 깔때기 결과는 §20.2의 Y/Yb 문제와 무관하게 같다.**
> Y는 1컷(cubic 94.60 > 94)을 통과하지만 2컷(σ_i > 5×10⁻⁵)에서 2.46×10⁻⁵로 탈락하고,
> Yb는 cubic 76.26이라 1컷에서 이미 탈락한다 — **어느 라벨을 쓰든 6종·1종·0종은 그대로**다.
> Y/Yb 확정이 실제로 바꾸는 건 깔때기가 아니라 **§20.2의 merit-flag 그림(Y가 cubic>94를 통과하는
> 유일한 passivation 상위군)** 쪽이다.

### 20.6 재현

```
python tools/litdb/anderson2024_si_tableS5.py   # 출력 = litdb/inbox/_51si_verify_out.txt
```

출력물: **`db/properties/anderson2024_llzo_dopant_screening_tableS5.csv`** (59행 + undoped,
`source` = `paper SI Table S5`). 열: `dopant, substituted_site, garnet_wt_pct, cubic_wt_pct,
sigma_ionic_S_cm, sigma_electronic_S_cm, Vmax_V, HV_integrated_current_mAh_g, Vmin_V, CCD_mA_cm2`.
V_min·CCD는 `< 0.1` · `>0.40,<0.85` 같은 **부등호/구간 표기라 문자열 원문 그대로** 보존했다
(저자들의 하한/구간 보고 관례 = §12c H1).

> **어느 CSV를 쓸 것인가** — σ·V·CCD는 **`_tableS5.csv`(저자 인쇄값)**, 구조(garnet%/cubic%)는
> 둘 중 아무거나(불일치 0건). **`_recovered.csv`는 Table 1에 없는 41종을 그림에서 되읽은 것**이라
> 여전히 유용하지만 **`Y`·`Yb`의 σ 라벨이 Fig 4를 따라 뒤바뀐 상태**임에 주의.
