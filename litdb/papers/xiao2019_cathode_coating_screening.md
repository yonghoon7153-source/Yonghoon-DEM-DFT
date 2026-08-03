# Computational Screening of Cathode Coatings for Solid-State Batteries — Xiao/Miara/Wang/Ceder (Joule 2019)

> slug `xiao2019_cathode_coating_screening` · DOI `10.1016/j.joule.2019.02.006` · type `DFT (HT-screening + NEB, 실험 0)` · PDF **`litdb/inbox/37. Computational Screening of Cathode Coatings for Solid-State Batteries.pdf`(본문 25 pp)** + `7a473fcd-37._Sup1…pdf`(정식 SI 10 pp: Fig S1·Table S1–S6) + **`litdb/inbox/37. Sup2) Computational Screening of Cathode Coatings for Solid-State Batteries.pdf`(35 pp = 본문 25 + SI 10 합본; 신규 내용 0 — 2026-08-03 페이지 단위 실물 대조)** (inbox #37) · **사용자 분류 폴더 `DFT`** · digested `2026-07-28` · **본문 독립 재검증 `2026-08-03`(§14)** · **SI(Table S1–S6) 독립 재검증 `2026-08-03`(§15)** · status ✅
> elements: Li, P, S, Cl, O, F, H, B, Ti, Zr, Nb, Ta, La, Cs, Ba, Ge, Ni, Co, Mn, Fe
> methods: DFT, NEB, ESW
> **저자**: Yihan Xiao¹², Lincoln J. Miara³, Yan Wang³, **Gerbrand Ceder***¹²⁴ — ¹UC Berkeley MSE, ²LBNL Materials Sciences Division, ³**Advanced Materials Lab, Samsung Research America**(3 Van de Graaff Dr, Burlington MA 01803), ⁴Lead Contact · Joule 3, 1252–1275 (Received 2018-11-21 / Revised 2019-02-09 / Accepted 2019-02-19 / **Published 2019-03-21**, 호수 날짜 2019-05-15) · Open Access CC BY-NC-ND · **본문 전문 실물 확인 완료**
> **연구비**: 주 재원 = **Samsung Advanced Institute of Technology(SAIT)**, 보조 = Materials Project Program(KC23MP, DOE BES DE-AC02-05CH11231). 계산자원 NERSC + XSEDE(ACI-1548562). ⚠ SAIT는 **연구비 출처이지 저자 소속이 아님**(Miara·Wang 소속은 Samsung Research America).
> ⚠ 이해상충 명시: "Some of the co-authors have patents filed on some coating compositions."

---

## 0. 이 digest를 읽는 법 (우리 캠페인에서의 위치) ★★
**우리 cascade(47-dopant AI 계산 스크리닝)의 직계 조상 — "게이트식 고처리량 열역학 스크리닝"의 원형 논문이다.** 방법 계보로는 [Zhu15](`zhu2015_esw_grand_potential_origin.md`, ref 31)·Ong 2013(ref 18)·**[Rich16]**(`richards2016_interface_stability_pseudobinary.md`, ref 30 = pseudo-binary ΔE_rxt/Eq 4 원전 — Miara·Wang·Ceder 공저로 인적 연속)·Miara 2015(ref 35)의 grand-potential/반응성 도구를 **10만 규모 DB에 처음 깔때기(funnel)로 돌린 논문**이고, 산출물(폴리음이온 산화물 코팅, O-공유결합 논리)은 [Sundar](ALD 코팅 스크린)·[Son](5 V 차폐 SE)·우리 그룹 [Cha]/[Kang25] 코팅 라인의 상류다. **우리 cascade와 대상이 다름에 주의**: Xiao = *코팅 물질* 발굴(104,082 후보), 우리 = *한 host(argyrodite)의 도판트* 스크리닝(47종) — force-fit 금지, 그러나 게이트 축(상안정 hull·grand-potential ESW·화학 반응성·이온전도 프록시)과 임계값 설계는 1:1 벤치마크 대상 (§7c 표).

## 1. 한 줄 요약
DFT 에너지 DB(ICSD+data-mined) 내 **Li 함유 104,082종**을 ① 전자절연(Eg>0.5 eV)+방사성 제외 ② 상안정(E_hull<5 meV/atom) ③ ESW(V_ox≥4.0 & V_red≤2.7 V) ④ 화학 반응성(|ΔE_rxt|<100 meV/atom vs Li₃PS₄ & 만충 NCM) 4중 게이트로 걸러 **62,437→1,600→302→184종**으로 압축, 이 중 **폴리음이온 산화물 66종**이 최다 생존군임을 보이고(불소·염화물도 다수 생존하나 이온전도 문헌 부재로 보류), 대표 6종의 CI-NEB·gap 분석으로 **LiH₂PO₄·LiTi₂(PO₄)₃·LiPO₃ 3종을 최종 추천**(+붕산염 LiBa(B₃O₅)₃ 계열은 화학안정 최강이나 Li 이동 취약) — 기전은 **"P/B–O 강공유결합이 O 2p를 끌어내려 산화 한계를 올리고(축합 phosphate일수록↑) 동시에 O–S 교환 반응성을 죽인다"**, 단 **Li 함량↑ ⇔ 산화한계↓의 내재 trade-off**가 있어 LiPO₃(Li분율 0.20에서 V_ox 5 V)가 스위트스폿.

## 2. 메타
| 항목 | 내용 |
|---|---|
| 저자/기관 | Xiao(Berkeley/LBNL), Miara·Wang(Samsung Advanced Materials Lab, Burlington MA), Ceder*(Berkeley/LBNL) |
| 저널 | Joule 3, 1252–1275 (2019). Received 2018-11-21 / Published 2019-03-21 (issue 5/15) |
| DOI | 10.1016/j.joule.2019.02.006 (OA, CC BY-NC-ND) |
| 유형 | 순수 계산: HT 열역학 스크리닝(hull·grand-potential·pseudo-binary) + CI-NEB (자체 실험 0) |
| 대상 | 코팅 후보 104,082종(Li-함유) / SSE 4종: **Li₆PS₅Cl(LPSCl=comp1)**, Li₁₀GeP₂S₁₂(LGPS), Li₃PS₄(LPS), LLZO / 양극 4종: NCM(LiNi₁/₃Co₁/₃Mn₁/₃O₂)·LCO·LMO(스피넬)·LFPO(LiFePO₄), 만충+반충(half-lithiated) / 기준 코팅: Li₂ZrO₃·LiNbO₃·LiTaO₃ |
| 핵심 질문 | 이상적 cathode 코팅 4속성(①넓은 ESW ②양극·SSE 양쪽과 저반응성 ③Li 이동성 ④전자절연)을 **동시에** 만족하는 조성을 HT로 찾으면 무엇이 나오나? 왜 그 화학이 이기나? |
| 선행 대비 | Zhu/He/Mo 2016(ref 32)은 소수 산화물 제안(Li₄TiO₄·Li₂TiO₃·Li₈SiO₆·Li₄SiO₄·**Li₅TaO₅**·Li₃TaO₄ — 2026-08-03 본문 재확인, 판독 확정), Aykol 2016(ref 46, Nat. Commun. 7, 13779)은 **액체 전해질용**(HF 포획) HT 스크린 — 본 논문이 처음으로 SSB용으로 **양극+SSE 양쪽 반응성과 이온전도까지** 게이트에 포함 |
| 이온전도를 게이트에 넣은 동기 (본문 명시) | ① Sakuda 2008(ref 47): SiO₂-코팅 vs **Li₂O–SiO₂-코팅 LCO** — 후자의 rate 성능 우위를 "코팅의 Li 전도도"로 귀속 ② **Jung/Kang/정윤석 2018**(ref 44, Chem. Mater. 30, 8190): **Li₃BO₃–Li₂CO₃(LBCO)가 Li₃BO₃(LBO)보다 σ_Li 2 자릿수 높아** 셀 성능이 좋다 — "코팅 = 안정성만이 아니라 전도체" 명제의 실험 근거 |

## 3. 스크리닝 파이프라인 (Figure 1) — 깔때기 전체 ★★★
```
DFT 에너지 DB (ICSD + data-mined 치환 신조성 [Hautier 2010])
   └─ Li 함유만                                   104,082
Filter 1  방사성 원소 제외 + Eg(Kohn–Sham) > 0.5 eV   62,437   (60.0 %)  ← 본문은 "more than 62,000"만; 62,437은 Fig 1 판독값
Filter 2  상안정  E_hull < 0.005 eV/atom (hull 위 5 meV)  1,600   (중복 조성 제거; 1.5 % of 시작)
Filter 3  ESW    V_red ≤ 2.7 V  &  V_ox ≥ 4.0 V           302
Filter 4  화학 반응성 |ΔE_rxt| < 0.1 eV/atom (LPS & 만충 NCM 양쪽)   184   (ICSD 출신 106)
Filter 5  폴리음이온 산화물만                                 66
Filter 6  대표 6종 선별 (V_ox ≥ 4.5 V 군에서: ortho 2·meta 3·borate 1) → CI-NEB·gap 정밀
최종 추천: LiH₂PO₄ · LiTi₂(PO₄)₃ · LiPO₃  (+붕산염 하이라이트)
```
- **게이트 임계값의 근거** (본문 명시):
  - **Eg > 0.5 eV**: 금속/합금 등 "확실히 전자전도"만 1차 배제. KS gap은 과소평가라 **하한(lower bound)**으로만 사용; 점결함/비정질이면 wide-gap도 전도 가능함을 자인(전 결함 계산은 HT에 과비용).
  - **E_hull < 5 meV/atom**: "DFT/온도 오차 이내 안정" — 합성 가능성+shelf-life 대리.
  - **V_ox ≥ 4.0 V**: 양극 작동 상한(2.5–4.5 V)에서 "약간의 kinetic 안정화 여지"를 두고 4.0으로. (LiCoPO₄ 4.19 / LiNiPO₄ 4.22 / LiTi₂(PO₄)₃ 4.59 V처럼 임계 초과 코팅들이 액체계에서 실적 좋음을 방증으로 인용.)
  - **V_red ≤ 2.7 V**: 코팅 창이 **전해질 창과 겹쳐야**(황화물 SE 계산 산화한계 2.2–2.7 V [ref 30]) 코팅/SE 계면에서 Li 이동 구동력이 없음 — 겹침 조건을 환원한계로 번역한 것.
  - **|ΔE_rxt| < 100 meV/atom**: 코팅/양극·코팅/SE 두 새 계면이 원래 양극/SE 계면보다 안정해야 한다는 조건의 정량 컷 (pseudo-binary 최악 혼합비 기준, §5). 본문이 병기한 환산 = **50 meV/atom ≡ 4.8 kJ/mol · 100 ≡ 9.6 · 200 ≡ 19.3 kJ/mol**.
  - ⚠ **논문 내부 필터 번호 불일치**: Table 1 각주는 화학안정 스크리닝을 **filter 4**로, Fig 7A 캡션·p.1267 본문은 같은 66종을 "pass the chemical reactivity screening (**filter 5**)"로 부른다. Fig 1 플로차트가 "폴리음이온 down-selection"을 별도 단계로 세었기 때문으로 보이며, 본 digest는 **F4=반응성(184) / F5=폴리음이온 한정(66)** 규약으로 통일해 적었다.
- **카테고리별 생존표 (Table 1 전량)** — 불소/염화물/옥시불화물/비폴리음이온 산화물/폴리음이온 산화물/기타:

| Filter | F화물 | Cl화물 | 옥시F | 비폴리 산화물 | **폴리음이온 산화물** | 기타 | 합계 |
|---|---|---|---|---|---|---|---|
| 2 상안정 | 229 (14.3 %) | 62 (3.9 %) | 62 (3.9 %) | 397 (24.8 %) | **411 (25.7 %)** | 439 (27.4 %) | 1,600 |
| 3 ESW | 114 (37.7 %) | 39 (12.9 %) | 8 (2.6 %) | 31 (10.3 %) | **109 (36.1 %)** | 1 (0.3 %) | 302 |
| 4 반응성 | 79 (42.9 %) | 31 (16.8 %) | 6 (3.3 %) | 2 (1.1 %) | **66 (35.9 %)** | 0 | 184 |

  - Filter 3 통과율: 폴리음이온 26.5 %(109/411) vs 비폴리 7.8 %(31/397); "기타"(황화물·질화물·인화물 등)는 사실상 전멸(1/439) — 산화한계가 음이온 화학으로 결정된다는 Richards 2016 명제의 대규모 재확인.
  - Filter 4 통과율: 폴리음이온 60.6 %(66/109) vs 비폴리 6.5 %(2/31). **LiCoPO₄·LiNiPO₄는 여기서 탈락**(LPS와 ~150 meV/atom: TM 황화물+인산리튬 형성) — "액체계 실적 ≠ 황화물 SSB 적합"의 상징 사례.
  - **살아남은 "비폴리음이온 산화물 2종"의 정체 (Table S1 실물, 2026-08-03 확인)**: **Li₃V(H₄O₃)₄ (V_red 1.92 / V_ox 4.17 V)** 와 **LiAl₅O₈ (0.85 / 4.09 V)** — 둘 다 V_ox < 4.2 V로 대표 6종 문턱(≥4.5 V)에 못 미치고, 하나는 수화물이라 실용성이 낮다. 즉 **비폴리음이온 산화물 진영은 "2종 생존"이라기보다 사실상 전멸**이며, 이 2종의 정체를 알면 Table 1의 `2`가 얼마나 빈약한 생존인지가 드러난다(본문은 이름을 밝히지 않음).
  - 완전 무반응(0/0) 사례: **LiF·LiCl·LiRbCl₂·LiCsCl₂·LiRb₂Cl₃**(만충 NCM·LPS 양쪽 ΔE_rxt=0) — 할라이드가 안정성으로는 최상위군. F+Cl 합계는 filter 4 통과 184종의 **약 60 %**(79+31=110).
  - **Fig 3B의 정량 진술(본문, 302종 대상)** — "폴리음이온이 이긴다"의 숫자 근거:
    - 비폴리음이온 산화물은 **전부** NCM과 |ΔE_rxt| < **50** meV/atom(4.8 kJ/mol)로 온건하지만, **3/4 이상이 LPS와 ≥ 200** meV/atom(19.3 kJ/mol)로 반응 — *한쪽만 잘하는* 전형.
    - 폴리음이온 산화물은 **60 % 이상이 LPS·NCM 양쪽 모두 ≤ 100** meV/atom(9.6 kJ/mol) — *양쪽 동시* 통과. → 게이트를 "양쪽 AND"로 건 순간 비폴리음이온이 31→2로 붕괴한 이유가 이 한 문장에 있다.
  - 폴리음이온 중 **NCM·LPS 양쪽 ΔE_rxt = 0**인 물질: **LiAlSiO₄(V_ox 4.09) · Li₃PO₄(4.22)** — 반응성은 LiBa(B₃O₅)₃급이나 산화한계가 조금 낮아 대표 6종에서 제외됨. ⚠ **논문 내부 불일치(2026-08-03 SI 대조 발견)**: 본문 p.1265는 두 물질 모두 "zero chemical reactivity with NCM and LPS"라 쓰지만, **Table S1 실측은 LiAlSiO₄ = LPS 0.000 / 만충 NCM −0.009 / 반충 NCM 0.000** — 즉 *엄밀히 삼중 0인 것은 Li₃PO₄뿐*이고 LiAlSiO₄는 만충 NCM과 −9 meV/atom. 인용할 때 "≈0"으로 쓸 것. (Table S1 전수에서 **삼중 0**은 **LiF(6.39) · LiCs(B₃O₅)₂(4.52) · Li₃PO₄(4.22)** 3종뿐 — 붕산염 LiCs(B₃O₅)₂가 §6a borate 목록 중 유일한 완전무반응.)
  - **⚠⚠ 기존 3원 산화물 코팅 3종(Li₂ZrO₃·LiNbO₃·LiTaO₃)은 Table S1에 없다 = 저자 자신의 filter 4를 통과하지 못한다** (2026-08-03 SI 대조 발견). LPS와 각각 **−115 / −164 / −139 meV/atom**로 |100| 컷을 초과하기 때문(§4b). 논문은 이들을 *게이트 통과 후보*가 아니라 **비교 baseline**으로만 쓰는데, 본문이 이 사실을 명시적으로 문장화하지 않아 오독하기 쉽다. 🔑 **인용 가치 최상**: "현행 산업 표준 코팅(LiNbO₃·LiTaO₃·Li₂ZrO₃)조차 황화물 SSE 기준 화학안정 게이트를 못 넘는다 — 그래서 폴리음이온으로 갈아타야 한다"가 이 논문의 *숨은* 가장 강한 논거.
- **왜 최종은 폴리음이온 산화물인가** (Filter 5의 명분): 할라이드(F/Cl)는 안정성 우수하나 **이온전도 문헌이 없거나 낮음** — 염화물 최고 RT σ ~10⁻⁶ S/cm(스피넬계), 예외적으로 Li₃YCl₆ ~10⁻⁴(Asano 2018, ref 61)이 "잠재력" 언급; 무기 불화물 Li 전도체는 보고 자체가 없음. 반면 폴리음이온 산화물은 NASICON ~10⁻⁴·LISICON-phosphate ~10⁻⁴·LiPON ~10⁻⁶ S/cm로 **전도+합성/코팅 공정이 검증됨**. (⚠ 2019년 판단 — 할라이드 SE 붐 직전. §10.)

## 4. 핵심 물성 (수치) — 추천 후보 전량 (Table 2 + Table S1 + Table S6)
### 4a. 대표 6종 + 기준 Li₂ZrO₃ (Table 2 전량)
| 코팅 | ICSD # | **계산 E_m (percolating vacancy NEB, eV)** | 실험 Ea (eV) | 실험 σ_ion (S/cm) | KS gap (eV) | 실험 σ_e (S/cm) |
|---|---|---|---|---|---|---|
| Li₂ZrO₃ (기준) | 31941 | 0.48 | 0.5, 0.68 | ~10⁻⁴ (598 K) | 3.99 | – |
| **LiH₂PO₄** | 100200 | **0.33** | – | – | 6.30 | – |
| **LiTi₂(PO₄)₃** | 95979 | **0.42** | 0.47 | ~10⁻⁶ (333 K) | 2.26 | ~10⁻⁹ |
| LiBa(B₃O₅)₃ | 93013 | 1.96 | – | – | 6.20 | – |
| **LiPO₃** | 51630 | **0.40** | 1.40 (glass 0.72) | 2.5×10⁻⁸ (553 K) | 5.60 | – |
| LiLa(PO₃)₄ | 416877 | 1.39 | 0.92ᵇ | 6.35×10⁻⁸ (553 K) | 5.22 | – |
| LiCs(PO₃)₂ | 62514 | 1.27 | 1.31 | ~10⁻⁸ (573 K) | 5.65 | – |

ᵇ LiLa(PO₃)₄ 실험 Ea는 원저(Mounir)의 Arrhenius 그림과 본문값이 불일치해 **Xiao가 그림에서 재산출**한 값. 참조: LiPON E_m 0.56 eV(문헌).
- **개별 hop 전량 (Table S6)**: Li₂ZrO₃ {0.48, 0.55, 0.58, 0.7, 0.8} / LiH₂PO₄ {0.33, 1.20, 1.24, 1.32, 1.42, 1.99} / LiTi₂(PO₄)₃ {0.42} / LiBa(B₃O₅)₃ {1.96} / LiPO₃ {0.1, 0.25, 0.26, 0.32, 0.36, 0.40, 0.50} / LiLa(PO₃)₄ {1.39, 1.65, 2.60} / LiCs(PO₃)₂ {0.43, 0.84, 1.27, 1.28, 1.54, 1.70}. Table 2의 E_m = **supercell을 관통(percolate)하는 경로의 최저 장벽**(경로는 Fig S1: 예 LiPO₃ 1→2→…→8→1).
- **ESW (Table S1)**: LiCs(PO₃)₂ 2.15–**6.23** / LiLa(PO₃)₄ 2.51–5.03 / LiPO₃ 2.52–**5.01** / LiBa(B₃O₅)₃ 1.30–4.83 / LiTi₂(PO₄)₃ 2.37–**4.59** / LiH₂PO₄ 2.23–**4.58** V. 참조군: Li₃PO₄ 0.71–4.22 / LiAlSiO₄ 1.14–4.09 / LiZr₂(PO₄)₃ 2.06–4.52 / Li₄P₂O₇ 2.33–4.36 V. *(전 12값 2026-08-03 SI 실물 재확인 — §15)*

#### 4a-2. Table S1 전수 구조 — filter-4 통과 **ICSD 106종**의 지도 (2026-08-03 SI 실물 집계) ★
Table S1 정렬 규약 = **음이온군 클러스터 → 군 내부 V_ox 내림차순**, 별표(*) = 정밀연구 6종. 열 = [Type, V_red, V_ox, ΔE_rxt(LPS), ΔE_rxt(만충 NCM), ΔE_rxt(반충 NCM)].

| 군 | n (ICSD 106) | V_ox 범위 (V) | 군 챔피언 |
|---|---|---|---|
| **F** 불화물 | **35** | 4.99 – **7.15** | **LiBF₄ 7.15** / LiCaGaF₆ 6.84 / LiHF₂ 6.81 |
| **P** 폴리음이온 산화물 | **55** | 4.01 – **6.23** | **LiCs(PO₃)₂\* 6.23** / LiGd(PO₃)₄ 5.30 / LiSm(PO₃)₄ 5.19 |
| **OF** 옥시불화물 | 4 | 4.04 – 4.77 | LiB₆O₉F 4.77 / LiKMg₂Si₄(O₅F)₂ 4.58 / LiCrPO₄F 4.52 |
| **Cl** 염화물 | 10 | 4.25 – 4.51 | LiGaCl₄ 4.51 / LiCs₂YCl₆ 4.38 / LiCs₂LuCl₆ 4.36 |
| **NP** 비폴리 산화물 | **2** | 4.09 – 4.17 | Li₃V(H₄O₃)₄ 4.17 / LiAl₅O₈ 4.09 (**전부**) |

- **불화물이 산화한계로는 압도적 1위**(35종 전부 ≥4.99 V, 최고 7.15 V) — 폴리음이온 최고치(6.23)보다 높다. 논문이 이들을 버린 유일한 이유는 **Li 전도 문헌 부재**(§3 Filter 5 명분)이지 안정성이 아니다. ⚠ 이 사실은 본문 Table 1의 개수(F 79 > P 66)만 봐서는 안 보이고 **Table S1의 V_ox 분포를 봐야 드러난다** — "폴리음이온이 이겼다"는 서사의 가장 약한 고리.
- **V_ox ≥ 5.00 V 폴리음이온 = 7종, 전부 meta-phosphate**: LiCs(PO₃)₂ 6.23 · LiGd(PO₃)₄ 5.30 · **LiSm(PO₃)₄ 5.19** · LiK(PO₃)₂ 5.09 · LiLa(PO₃)₄ 5.03 · LiPO₃ 5.01 · **LiAl(PO₃)₄ 5.01** — §6a "meta > pyro > ortho" 축합 위계의 ICSD 실물 확증(예외 0). Xiao가 Fig 7에서 "V_ox≥5 V ⇒ Li분율 ≤0.20"이라 한 것도 **meta-phosphate가 곧 저-Li 조성**이기 때문.
- ⚠ Table S1은 **184종 중 ICSD 출신 106종만** — data-mined 78종은 미공개(§10).
- **SSE·기존 코팅 ESW (Fig 4, figure-read)**: 황화물 3종(LPSCl·LGPS·LPS) 산화한계 **<2.5 V**(막대 ~1.7–2.5 V; LPSCl ≈1.7–2.0 V — [Zhu15] 1.71–2.01과 동일 세대 hull이라 정합), LLZO **2.9 V**(실험 겉보기 ~4.0 V = kinetics, ref 56), 3원 산화물 코팅 Li₂ZrO₃/LiNbO₃/LiTaO₃ **3.4–4.0 V**, 폴리음이온은 **≥4.5 V**, meta-phosphate 3종은 **5 V 이상**(LNMO 4.7 V와 페어링 가능).

### 4b. 화학 반응성 매트릭스 ΔE_rxt (meV/atom, Table S2 만충 / Table S3 반충 전량)
| (코팅·SSE) \ 상대 | NCM | LCO | LMO | LFPO | LPSCl | LGPS | LPS | LLZO |
|---|---|---|---|---|---|---|---|---|
| Li₂ZrO₃ | 0 / −15 | 0 / −30 | −33 / −65 | −66 / −105 | −88 | −90 | −115 | **−4** |
| LiNbO₃ | −4 / 0 | 0 / 0 | 0 / −21 | −23 / −35 | −123 | −126 | −164 | −69 |
| LiTaO₃ | 0 / 0 | 0 / 0 | 0 / −7 | −20 / −24 | −115 | −108 | −139 | −62 |
| LiH₂PO₄ | −58 / −15 | −61 / −24 | −17 / −12 | **0 / 0** | −46 | −35 | **−21** | −130 |
| LiTi₂(PO₄)₃ | −72 / −14 | −58 / −14 | −11 / −4 | **0 / 0** | −71 | −62 | −46 | −186 |
| **LiBa(B₃O₅)₃** | −10 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | **−5** | **−3** | **−1** | −78 |
| LiPO₃ | −89 / −35 | −76 / −31 | −36 / −25 | −10 / −13 | −52 | −43 | −30 | −202 |
| LiLa(PO₃)₄ | −95 / −38 | −80 / −35 | −41 / −28 | −10 / −14 | −63 | −53 | −35 | −218 |
| LiCs(PO₃)₂ | −62 / −13 | −55 / −20 | −6 / −1 | 0 / −14 | −85 | −77 | −63 | −155 |
| **LPSCl(=comp1)** | **−330 / −471** | **−339 / −493** | −421 / −518 | −101 / −143 | — | — | — | — |
| LGPS | −351 / −517 | −362 / −541 | −464 / −564 | −94 / −136 | — | — | — | — |
| LPS | **−422 / −580** | −426 / −606 | −531 / −616 | −84 / −125 | — | — | — | — |
| LLZO | −1 / −44 | −2 / −57 | −63 / −102 | −94 / −137 | — | — | — | — |

(셀 = 만충 / 반충. 코팅 vs SSE 열은 만충 무관.) **읽는 법**: ① 황화물 SSE는 산화물 양극과 −330~−616 = 코팅 없이는 불가(LPS/NCM 422 meV/atom = 40.7 kJ/mol; **반충전이 더 악화**). LFPO만 ~−100로 온건(P가 이미 O와 결합). ② 기존 3원 산화물 코팅은 양극과는 0급이나 **황화물 SSE와 −88~−164로 나쁨**(S/O 교환→PO₄+TM 황화물). ③ 폴리음이온은 양쪽 다 |100| 미만; **반충전 시 코팅/양극 반응성은 오히려 감소**(Li₃PO₄-형성 반응이 양극의 Li를 필요로 하기 때문) — SSE와 정반대 거동. ④ **LiBa(B₃O₅)₃은 전 계면 −10~0**(반충 4양극 전부 0) = 화학안정 챔피언. ⑤ LLZO는 만충 NCM/LCO와 0급이나 반충·고온(973 K La₂CoO₄ 실험)서 반응 — 소결 공정엔 여전히 코팅 필요.

### 4c. 분해 산물 (Table S4·S5 발췌 — 우리 관심 계면)
- **NCM/LPSCl**: 만충 = Ni₃S₂, Li₂SO₄, Li₂S, **LiCl**, MnS, Co₉S₈, **Li₃PO₄** / **반충 = MnS, Li₂SO₄, Ni₃S₂, Li₃PO₄, Li₂O, Co₉S₈, LiCl** — 즉 반충에서 **Li₂O가 등장하고 Li₂S가 사라진다**(2026-08-03 SI 실물 정정; 이전 판의 "반충: +Li₂O"는 Li₂S 소멸을 빠뜨림). 🔑 물리 의미: 양극이 탈리튬될수록 **황이 sulfide(Li₂S)에서 산화된 형태로 더 밀려나고 산소가 Li₂O로 떨어져 나온다** = SOC↑에서 계면이 더 산화적으로 열화한다는 산물 수준 증거. **LCO/LPSCl**: 만충 Li₃PO₄, Li₂S, Co₉S₈, Li₂SO₄, LiCl / 반충 Li₂SO₄, Li₃PO₄, **Li₂O**, Co₉S₈, LiCl — 같은 패턴(Li₂S→Li₂O 치환). 우리 interface_reactivity(vs LCO) 산물과 대부분 겹침 (§7b).
- **LPSCl/LiPO₃**: Li₃PS₄, LiCl, Li₃PO₄ (경미 −52) / **LPSCl/LiH₂PO₄**: **H₂S**, Li₃PS₄, LiCl, Li₃PO₄ (기체 리스크) / **LPSCl/LiTi₂(PO₄)₃**: Li₃PO₄, Ti(PS₃)₂, TiS₃, LiCl, TiS₂ (**Ti 황화물 = 전자전도성 산물** → §6d) / LPSCl/LiBa(B₃O₅)₃: Ba(BS₂)₂ 등 (−5뿐).
- **NCM/LiH₂PO₄ (만충)**: **HCoO₂**(H 삽입 CoO₂), Li₃PO₄, Li₂Mn₃NiO₈, Ni(HO)₂ — **양성자↔Li 교환** 부반응(구동력 ~60 meV/atom; LMO는 4 meV/atom, LFPO는 비자발).
- **LLZO/phosphate 계열**: Li₃PO₄+ZrO₂+LaPO₄(−130~−218) → **phosphate 코팅은 LLZO와 비호환**(Fig 9에서 제외 근거).

## 5. DFT/계산 방법 ★ (Experimental Procedures 전문 요약)
- **code/셋업**: VASP + PAW. **GGA(PBE)/GGA+U 혼합 스킴**(rotationally invariant Hubbard; Jain 2011 혼합 보정) = MP 계열 표준. **ecut 520 eV**, k-grid **≥ 500/n_atom**. "Similar datasets available online as part of the Materials Project" — 즉 **자체(내부) DFT DB**(ICSD 구조 + data-mined 치환 신조성 [Hautier 2010])이며 MP 공개판과 동세대. MP 버전 번호는 명시 없음(2018년 무렵 세대).
- **상안정 (Filter 2)**: 조성 화학공간의 0 K convex hull(**pymatgen**)에서 E_hull 산출; <5 meV/atom 통과. hull 위 상은 "가장 가까운 hull 상(Gibbs triangle)으로 분해한다"는 표준 해석.
- **ESW (Filter 3)** — [Zhu15]와 동일 construction (refs 18, 30, 35):
  - Eq 1: `Φ[c, μ_Li] = E[c] − n_Li[c]·μ_Li` (grand potential)
  - Eq 2/3: `V_red = (μ⁰_Li − μ_red)/e`, `V_ox = (μ⁰_Li − μ_ox)/e` — 조성이 grand-potential hull 위에 머무는 μ_Li 구간 [μ_ox, μ_red]를 전압창으로 번역.
  - metastable 물질(예 LGPS)은 **hull 위에 정확히 올려놓고(E_hull→0)** 평가 — [Zhu15]의 규약 그대로(유한온도 안정화 명분).
- **화학 반응성 (Filter 4)** — Richards 2016(ref 30) pseudo-binary:
  - Eq 4: `ΔE_rxt = min_{x∈[0,1]} { E_pd[x·c_a + (1−x)·c_b] − x·E[c_a] − (1−x)·E[c_b] }` — 두 반응물의 임의 혼합비 x를 스캔해 **가장 음(최악)의 반응에너지**를 취함. E_pd = 그 조성의 hull 평형 에너지. 단위 eV/atom(반응물 원자수 정규화). 게이트 상대 = **LPS(Li₃PS₄) + 만충 NCM**; 정밀 단계에서 4양극×만충/반충 + 4 SSE로 확장 (§4b). ⚠ open-system(grand-potential) 아님 — 닫힌계 혼합; 전압 인가 상태의 계면은 별도(ESW가 담당)라는 분업.
- **이온전도 프록시 (Filter 6)**: **CI-NEB**(climbing image; refs 114–115), **단일 Li vacancy 이동 장벽**. vacancy는 Li 1개 제거 + **균일 배경전하 보상**(산화상태 유지). ecut 400 eV(NEB만). DB 내 최저에너지 결정 구조 사용. **의도적 단순화** (본문 자인): (i) vacancy 형성에너지 불포함 — nm급 코팅은 결함 과다라 intrinsic vacancy 존재 가정, (ii) interstitial 기전 제외 — 고전압에서 Li interstitial 생존 어려움, (iii) GB·비정질 미고려. **BVSE·AIMD·MLIP 아님** — 정적 NEB가 이 논문의 전도 프록시.
- **전자전도 프록시**: KS gap(LDA/GGA 과소 → **하한**으로 사용). 코팅 gap ≥2.2 eV ≫ 만충 NCM 계산 gap 1.5 eV → "코팅 σ_e < NCM σ_e(10⁻²–10⁻⁷ S/cm)" 필요조건 통과. LiTi₂(PO₄)₃ 실험 σ_e ~10⁻⁹로 방증.
- **무질서/비정질 처리**: 없음(전부 결정 질서 모델). 비정질 코팅(σ·Ea 달라짐: LiPO₃ 유리 σ 10⁴×↑, LiNbO₃ 비정질 σ↑)은 논의로만 — "(전기)화학 안정성은 결정과 유사할 것"이라는 가정 명시.
- **자원/기여**: NERSC·XSEDE. Ceder 총괄; Xiao·Miara HT 스크리닝; Xiao·Wang NEB; Xiao 분석·집필.

## 6. 결과 서사 (본문 순서, 전 수치)
### 6a. 왜 폴리음이온인가 — O 공유결합 논리 (Table 3·Figure 6) ★
- 산화 분해는 **O 2p(최고점유준위)에서 전자+Li 추출로 시작** → peroxide/superoxide/O₂ 방출. **비금속 M–O 강혼성(공유결합)이 O 2p를 끌어내려 산화를 방어** — 양극 재료의 anion redox 이해와 동일 논리.
- **Table 3 (동일 양이온 비교)**: Li₂ZrO₃ 3.44 V(→ZrO₂+O₂) vs **LiZr₂(PO₄)₃ 4.52 V**(→Zr₂P₂O₉+ZrP₂O₇+O₂) / LiTa₃O₈ 4.09 vs **Li₂Ta₂(P₂O₇)₃ 5.44** / LiCr₃O₈ 4.26 vs **LiCrP₂O₇ 4.61 V** — phosphate 골격을 씌우면 +0.4~+1.4 V.
- **Figure 6 (violin, filter-2 통과 phosphate 150종 = ortho 31·pyro 23·meta 96)**: 산화한계 중앙값 **meta(PO₃⁻) > pyro(P₂O₇⁴⁻) > ortho(PO₄³⁻)** — 축합(condensation)으로 O/P 비가 줄수록 O–P 혼성↑ → V_ox↑. phosphate 양극의 유도효과(inductive effect)와 동전의 양면.
- **붕산염**: B–O 결합해리에너지 **806 kJ/mol > P–O 597** → LiBa(B₃O₅)₃ 계열(LiSr(B₃O₅)₃, LiH₂B₅O₉, LiCs(B₃O₅)₂, LiB₃O₅, Li₃B₇O₁₂, Li₂Al(BO₂)₅, Li₄B₇O₁₂Cl)이 양극·SSE 전 계면 저반응 — "borates = very promising"이지만 **이온전도 미지**가 단서.
- **LiNbO₃/LiTaO₃의 자리**: 4d/5d 초기 TM의 덜 수축된 d 궤도가 O를 혼성 보호(V_ox 3.9~4.0 V대). Li₃PO₄ 형성이 원천 불가(P 없음)라 **산화물 양극과의 고온 공정에 최적** — 단 황화물 SSE와는 S/O 교환 구동력. **LLZO+산화물 양극 사이 버퍼로 이상적**(고전압 kinetic 안정화가 전제). 실증 근거로 **LiNbO₃-코팅 LCO·LMO가 황화물 SSB에서 효과적**(refs 20, 41)을 인용; 반응성 0급 계면 예시로 **LiTaO₃/NCM·LiNbO₃/LCO**(만충·반충 모두 구동력 없음)를 명시. 또 **Li₂ZrO₃는 LMO/LLZO 계면에서 전 산화물 코팅 중 최고 호환** — "코팅 선택 = 짝 특이적"의 Fig 5 내 사례.

### 6b. 왜 황화물 SSE에 코팅이 필수인가 (Figure 5·Table S2)
- O–S 교환의 열역학: **P–O 597 ≫ P–S 346 kJ/mol**인데 TM은 Co–O 368 ≈ Co–S 343 → S가 P에게 O를 뺏기고 TM이 S를 받는 교환이 대득(NCM/LPS 계면서 P–Oₓ종 실험 관측 인용). LFPO만 P가 이미 만유 O 결합이라 온건.
- SSE/양극 반응은 **반충전에서 더 악화**(LPS/NCM −422→−580) = 충전 중 계면열화 가속의 열역학 근거. 역으로 폴리음이온 코팅/양극은 반충전서 완화 — **코팅의 존재 의의를 SOC 의존성까지 보여준 첫 매트릭스**.
- Li₃PO₄ 형성이 항상 악은 아님: Li₃PO₄ 자체가 V_ox 4.22 V·σ ~10⁻⁷(부분결정)로 코팅/박막 SE 실적 — **자기제한 passivation 후보** ([Zhu15]의 인공 SEI 논리 계승).
- ⚠ **P → 인화물(phosphide) 논쟁을 본문이 미결로 남김**: "일부 모델링 결과는 P의 인화물 환원이 PO₄³⁻ 형성보다 **kinetically preferred**라고 주장하나(ref 33 = Tang & Ong 2018, Chem. Mater. 30, 163 — Na-ion ASSB 계면), **이 예상 밖 결과는 실험 확인이 필요하다**"고 명시적으로 유보. 🔑 우리 LPSCl 분해산물 서사(Li₃PO₄ vs P-환원종)에서 **"열역학 산물 목록 ≠ 실제 관측 산물"**을 인용할 때 쓸 수 있는 원전 문장.
- **코팅 = 두께·조성이 제어된 인공 SEI** (Discussion 도입부): 자연 SEI는 양극·SSE를 임의량 반응시켜 만들어지고 원소 상호확산이 계면에서 **최대 50 nm**까지 뻗어 이온수송을 막는 반면(ref 22), 코팅은 화학·조성·두께를 **1–10 nm** 수준으로 제어 가능 — 이것이 "그냥 SEI 생기게 두지 왜 코팅하나"에 대한 이 논문의 답.

### 6c. Li 함량 ↔ 산화한계 trade-off (Figure 7) ★
- filter-2 폴리음이온 411종 전수: **Li 원자분율↑ ⇒ V_ox↓** (선형 추세). Fig 7B(최대 Li분율 vs V_ox): **V_ox ≥ 5 V이려면 Li분율 ≤ 0.20**; 4 V 위에서 급락.
- 물리 해석 이중: (i) Li 많음 = μ_Li 높음(추출 쉬움), (ii) Li 추출이 O 방출/PO₄ 축합과 동반 — 축합할수록 O 공유결합↑라 처음부터 축합된(=Li 적은) 조성이 유리.
- 저Li분율 = Li–Li 거리↑·배위수↓ = **σ 불리**(Sendek 2017 통계학습 인용) → **"V_ox와 σ는 Li 함량을 사이에 둔 내재 trade-off"**. LiGd(PO₃)₄(V_ox 5.30, Ea 0.96)·LiK(PO₃)₂(5.09, 1.89)·LiDy(PO₃)₄(4.86, 0.96)·LiCs(PO₃)₂(6.23, E_m 1.27)·LiBa(B₃O₅)₃(4.83, 1.96)이 그 증거.
- **LiPO₃ = 스위트스폿**: filter-5 생존 66종 중 V_ox ≥ 4.5 V인 25종에서 **최고 Li분율 0.20** → Li–Li hop 짧아 E_m 0.40 eV(결정)·0.72 eV(유리) — "5 V 안정 + 저장벽" 동시 달성. kinetic 안정화까지 감안하면(예: Li₃PO₄가 5 V서 버티면) Li분율 한도 0.20→0.38.
- 용처 매칭: 4.5 V 이하 컷오프 양극(NCM/LCO)엔 LiH₂PO₄·LiTi₂(PO₄)₃(4.6 V)도 충분 — LiTi₂(PO₄)₃ 코팅이 4.6 V 충전 Li-rich 양극 개선(ref 60), LiPO₃가 LNMO 개선(ref 88) 실적 인용.

### 6d. 한계 자인 + 코팅 전략의 구조적 문제 (Figures 8·9) ★
- **전자전도성 분해산물**: 코팅/황화물 계면의 TM 황화물(TiS₂ 등)은 전자전도 → 혼합전도층 위험 ⇒ **코팅의 TM 함량 최소화 권고** — 황화물 SSE엔 LiTi₂(PO₄)₃보다 **LiH₂PO₄·LiPO₃**가 안전.
- **LiH₂PO₄의 H 리스크**: 일부 산화물/황화물과 H₂O/H₂S 기체(소량; 전처리 어닐/진공건조로 제거 가능 주장) + **LCO/NCM과 H⁺↔Li⁺ 교환**(HCoO₂+Li₃PO₄, ~60 meV/atom; H·Li 모두 RT 이동성 좋아 반응 용이).
- **코팅 패러독스**: 완벽한 전자절연 코팅 = 활물질 redox 차단 → **코팅은 약간의 전자투과 또는 불완전(imperfect) 커버리지가 필요**한데, 불완전하면 노출면에서 SSE 분해 지속(코팅 셀도 임피던스 계속 성장하는 실험의 설명) → 복합양극 형태학 설계 필요 (Fig 8: current collector/SSE·SSE/carbon·불완전 코팅부 등 잔여 계면 도해).
- **"dead space"**: 양극만 코팅하면 SSE/carbon·SSE/집전체 계면 산화는 못 막음 — 전자/Li 이동이 필요 없는 계면이라 즉각 성능 저하는 아니나, 분해층이 SSE 입자 σ_ion을 깎는 내부저항원(정량 미지 자인).
- **결정 vs 비정질**: 스크린은 결정 기준 — 안정성은 유사 예상, σ는 다를 수 있음(비정질이 유리한 사례 다수).
- **Figure 9 최종 권고 매트릭스** (양극×SSE×공정): ① 산화물 양극(NCM)+황화물 SSE(소결/열간/냉간): **붕산염·인산염** ② 산화물 양극+LLZO(소결/열간): **붕산염·산화물**(충전전압 제한 시) ③ LFPO+황화물: 붕산염·인산염 ④ LFPO+LLZO: 붕산염·산화물. 예시 — 붕산염 LiBa(B₃O₅)₃ / 인산염 LiH₂PO₄·LiTi₂(PO₄)₃·LiPO₃ / 산화물 Li₂ZrO₃·LiNbO₃·LiTaO₃. **"코팅 선택은 양극·SSE·공정 3변수 함수"** — 고온 소결이면 화학안정이 지배, 냉간이면 ESW·σ가 지배.

## 7. 우리 DFT/cascade 대비 → `../our_dft_baseline.md` ★★
### 7a. LPSCl(=comp1) 수치 정합
| 항목 | Xiao 2019 | 우리 | 판정 |
|---|---|---|---|
| LPSCl ESW | Fig 4 막대 ~**1.7–2.0 V** (figure-read; 표 없음), 본문 "thiophosphates <2.5 V" | OCV 1.717 / onset **2.14–2.256 V** (MP2026, LiS₄ 제외 시 2.256) | ✓ 동일 세대 계보([Zhu15] 1.71–2.01)와 일치; 우리 +0.13~0.25 V는 hull 세대(MP2020 S-보정) 효과 — **모순 아님** |
| LPSCl/LCO 반응성 | **−339**(만충)/−493(반충) meV/atom; 산물 Li₃PO₄+Li₂S+Co₉S₈+Li₂SO₄+LiCl | interface_reactivity(vs LCO): Li₃PO₄/Li₂SO₄/폴리설파이드/LiCl | ✓ **Li₃PO₄·Li₂SO₄·LiCl 공통**; 그들 Li₂S+Co₉S₈ vs 우리 폴리설파이드 = hull entry 세대 차이. 우리도 ΔE_rxt 절대값(meV/atom)을 산출·병기하면 1:1 비교 완성 |
| LPSCl/NCM 반응성 | −330/−471 meV/atom | (NCM은 우리 hull 밖 — Ni·Mn 부재) | ✗ 우리 공백 (§7c) |
| 산화한계=음이온 화학 | Richards 명제 재확인 (기타군 302 중 1) | S²⁻-limited onset(조성 무관 2.256) = 같은 명제의 argyrodite 내부판 | ✓ 프레임 동일 |
| gap 사용법 | KS gap = 하한·게이트(>0.5 eV)·NCM 1.5 eV 대비 | fixed-occ nscf 고유값·"wide-gap" 수준 비교만 | ✓ 철학 동일(절대 gap 비교 금지) — 그들도 하한으로만 |

### 7b. 방법 계보 (grand-potential: [Zhu15] → 이 논문 → 우리)
- ESW Eq 1–3 = [Zhu15] μ_Li(φ) construction **그대로**(metastable→hull 규약 포함) — 차이는 스케일(14종→1,600종)과 용도(SE 진단→코팅 게이트). 우리 `esw_cascade_batch.py`(pymatgen `get_element_profile`)는 **같은 형식의 3세대 구현** — 즉 우리 cascade ESW의 "HT 게이트화" 선례가 바로 이 논문.
- ΔE_rxt Eq 4 = Richards 2016 pseudo-binary — 우리 `interface_reactivity`(pymatgen `InterfaceReactions`/`GrandPotentialInterfacialReactivity`)와 동일 뿌리([Sundar]도 동일 도구). 우리는 전압분해(grand-potential 버전)까지 쓰는 반면 Xiao의 게이트는 닫힌계 혼합만.
- NEB 프록시의 정직성: 그들 스스로 LiPO₃ 계산 0.40 vs 실험 1.40 eV(결정)·유리 0.72 사례로 "형성에너지·기전·GB·비정질 무시의 대가"를 명시 — **우리가 BVSE(정적 프록시)→MLIP-MD(동역학)로 2단 검증하는 이유**를 원조가 몸소 보여줌. 또 "HT에 ab initio 전도 계산은 과비용"(ref 48–49) 명시 = 우리 UMA-상대 스크리닝이 채우는 바로 그 공백.

### 7c. 게이트 1:1 벤치마크 — Xiao funnel vs 우리 cascade v23 ★★★
| 축 | **Xiao 2019 (순차 boolean 깔때기)** | **우리 cascade v23 (가중 score + 최소 게이트)** | 코멘트 |
|---|---|---|---|
| 대상/풀 | **코팅 물질** 발굴: Li-함유 **104,082**종(ICSD+data-mined) | **host 도판트** 스크리닝: modelc(Cl-rich argyrodite)에 **47종** 산화물/불화물 × x(≤0.25) | 대상 자체가 다름(물질 발굴 vs 격자 개질) — 수치 이식 금지 |
| 전자절연 | Filter 1: **Eg > 0.5 eV** (KS, 하한) + 방사성 제외 | host가 wide-gap(2.1 eV) 전제; 산물 절연성은 sei_products gap 축으로 별도 | 우리는 "분해산물의 gap"까지 분해 — 그들 논문 말미 "전자전도성 산물" 우려의 정량판 |
| 상안정 | Filter 2: **E_hull < 0.005 eV/atom** (DFT-hull 절대) | **stable 0.25 가중치** = de_post_anneal (**UMA 상대**, min-max norm; boolean 아님) | 그들 = 절대 hull(5 meV 강컷: 합성가능 metastable 다수 탈락), 우리 = host 내 상대 안정화(연속) |
| ESW | Filter 3: **V_ox ≥ 4.0 & V_red ≤ 2.7 V** (코팅 창이 양극 상한+SE 창과 겹침) | **ox 0.30 가중치**(grand-potential onset; S-limited라 2.14 V 근방 미세차) + **window > 0.05 V 게이트**(collapse=후기 TM Fe/Co/Ni/Mn 회피) | 같은 grand-potential, 다른 좌표계: 그들은 4 V 절대 문턱(코팅은 넘을 수 있음), 우리는 S-limited host라 절대 문턱 대신 **onset 미세이동+창 붕괴 회피** |
| 화학 반응성 | Filter 4: **&#124;ΔE_rxt&#124; < 0.1 eV/atom vs LPS & 만충 NCM** (pseudo-binary) | (게이트 없음 — interface_reactivity vs LCO는 별도 축, NCM 미보유) | **그들에 있고 우리에 없는 축** ① |
| 화학군 필터 | Filter 5: 폴리음이온 산화물만(66) — σ 문헌 근거 | 도판트 화학군 = 산화물 중심 + F-variant (O/F-degenerate 판정) | 유사한 "화학 상식 컷" |
| 이온전도 | Filter 6: **CI-NEB vacancy E_m** — 대표 **6종만** 정밀 | **BVS proxy 47종 전원**(bvs_li_proxy_score·migration_volume_fraction·tier2 blocking) → 챔피언 MLIP-MD 검증 | 그들 6/66만 계산(비용) vs 우리 전수 프록시+선택 MD — HT 전도 공백을 우리가 프록시로 메움 |
| 기계 | **없음** | **soft 0.20 + ductile 0.15** (E_VRH·Pugh B/G) = 가중 35 % | **우리에 있고 그들에 없는 축** ① |
| 조합/교호작용 | 없음(단일 조성 나열) | 테마 12+1 조합 + **co-doping 교호작용 ML**(codoping_ml_v2) | 우리 추가 축 ② |
| 스코어링 철학 | 순차 hard gate → 통과/탈락 (경계값 근처 정보 소실) | **score = 0.30·ox + 0.25·stable + 0.20·soft + 0.15·ductile + 0.10·window** → 순위+trade-off 보존 (Sc₂O₃ 1위 0.813) | 깔때기의 "정보 소실"을 가중합으로 보완 — 대신 우리는 가중치 자의성 리스크 |
| 힘/에너지 엔진 | DFT-hull **절대**(내부 MP-세대 DB) | **UMA-상대**(MLIP; 절대값 인용 금지 규율) + MP hull(ESW만 절대) | 우리 추가 축 ③ — 47종×x를 돌리는 비용 해법; 절대성은 희생 |
| 산출 | 추천 물질 3종 + 설계 원리(O 공유결합·Li 트레이드오프) | 도판트 랭킹 + 테마 조합 + 예외 도판트(B₂O₃ onset +0.18 V 등) | 그들 "원리" ↔ 우리 "예외 발굴" 상보 |

### 7d. 물리 논리의 재사용 지점
- **O 공유결합→산화방어** = 우리 ICOHP P–O −8.43(P–S −5.98 대비 +41 %)·B–O 강결합·**B₂O₃ 도핑 onset +0.18 V**(cascade 예외 도판트)의 문헌 원리판. Xiao Table 3(동일 양이온 +phosphate → +0.4~1.4 V)는 "음이온 골격을 바꿔야 onset이 움직인다"는 점에서 [Banik](동족 치환 무효)과 상보 — 우리 cascade의 "산화물 도판트가 onset을 소폭 옮기는 예외"는 이 두 명제 사이에 정확히 위치.
- **Li 함량 trade-off**(V_ox↔σ) = 우리 cascade의 stability↔Li-mobility blocking trade-off와 동형 구조(레버만 다름: 그들 조성 Li분율, 우리 도판트 blocking).
- **붕산염 챔피언** = 우리 +B₂O₃ 서사의 코팅판 지지 — 단 **B 3축 분리 필수**: (산화·계면 화학안정 ↑ [Xiao·우리]) vs (Li 이동성 ↓ 위험 [Xiao LiBa(B₃O₅)₃ E_m 1.96 eV]) vs (**가수분해 최악급 [Zhu20]**). "B가 좋다"는 축 명명 없이 말하면 틀림.

## 8. Figure set ★
| Fig | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1 | 깔때기 플로차트(104,082→…→3) + 게이트 임계값 명기 | **cascade 발표용 계보 그림의 원형** — 우리 funnel(47종→테마→챔피언)을 같은 문법으로 그리면 "직계 후속" 서사가 시각화됨 |
| 2 | 필터 2/3/4 생존수 히스토그램(화학군별 색) | 화학군별 생존율 = "음이온 화학이 운명" 한 장 요약 |
| 3A | 1,600종 V_ox vs V_red 산점도 + 게이트 박스(초록) | ESW 게이트의 2D 시각화 — 우리 cascade ox/red 산점도(도판트별)와 동일 포맷 가능 |
| 3B | 302종 ΔE_rxt(LPS) vs ΔE_rxt(NCM) 산점도 + 100 meV 박스(초록) — 본문 판독: 비폴리 산화물 **전량** NCM<50 meV이나 **3/4↑가 LPS≥200 meV**, 폴리음이온은 **60 %↑가 양쪽 ≤100 meV** | **"양쪽 호환" 2축 플롯** — [Cha] dual-compatibility의 스크리닝판; 우리 interface_reactivity 확장 시 재현할 그림. 축 하나만 보면 비폴리가 이기는 것처럼 보이는 **단축 착시**의 교과서적 반례 |
| 4 | ESW 막대: SSE(LPSCl·LGPS·LPS·LLZO) vs 3원 산화물 vs 폴리음이온 6종 | LPSCl ~1.7–2.0 V(figure-read)가 우리 1.717–2.256과 정합; "코팅이 SE 창을 어떻게 덮나" 도해 |
| 5 | ΔE_rxt 히트맵(코팅·SSE × 양극·SSE, 만충) | 우리 sei/interface 매트릭스의 컬러맵 포맷 원형 (Origin-ready로 재현 용이) |
| 6 | phosphate 150종 V_ox violin (ortho/pyro/meta) | **축합도→산화한계** 정량 — 우리 O-doping(PS₃O)·B₂O₃ 논의에 인용 가치 |
| 7A/B | V_ox vs Li분율 산점 + 최대 Li분율 계단 (LiPO₃ 표시) | **trade-off 프론티어 플롯** — 우리 cascade pareto(Y열) 그림의 문헌 원형 |
| 8 | 복합양극 잔여 계면 도해(불완전 코팅·SSE/carbon 등) | 코팅 패러독스·dead-space — [KimICCF] 미세구조 서사와 연결 |
| 9 | 권고 매트릭스(양극×SSE×공정별 코팅 화학군) | "코팅 선택 = 3변수 함수" — deck 결론 슬라이드 포맷 |
| S1 | 7종 결정구조 + percolating vacancy 경로(번호) | NEB 경로 보고 관례(경로 명시) — 우리 BVSE 경로 그림과 대응 |

## 9. Post-processing ★
- **무엇**: convex hull(E_hull) → grand-potential ESW(Eq 1–3) → pseudo-binary ΔE_rxt(Eq 4, 최악 혼합비 스캔) + 분해 phase equilibria 나열 → CI-NEB(단일 vacancy, percolating 경로) → KS gap 표.
- **도구**: VASP + pymatgen(hull·grand-potential·반응 열역학; ref 113) + 내부 DFT DB. NEB는 VASP CI-NEB.
- **수치화·기록 방식**: 물질당 [V_red, V_ox, ΔE_rxt(LPS), ΔE_rxt(만충 NCM), ΔE_rxt(반충 NCM)] 표(Table S1, 106종) + 계면당 [ΔE_rxt, 산물 상 리스트] (Table S2–S5) + NEB 전 hop 배열(Table S6). — **우리 cascade CSV(oxidation_stability_cascade.csv·cascade_v23_ranked.csv)와 사실상 동일한 스키마**; 우리가 없는 열 = ΔE_rxt(양극), 그들이 없는 열 = E/pugh/window·테마.

## 10. 주의/한계 (over-claim 방지) — 비판적으로
- **0 K 열역학 only, kinetics 전무** (자인): LLZO 계산 2.9 V vs 실험 겉보기 4.0 V처럼 kinetic 안정화가 ±1 V급 — V_ox 4.0 게이트 자체가 "kinetic 여유 포함" 절충이라, **게이트 통과/탈락 경계(±0.2 V)의 물질 구분은 물리적 의미 약함**. 분해 "속도·양"은 못 봄([Zuo]류 정량과 별개 축).
- **E_hull < 5 meV/atom 강컷**: 합성 가능한 metastable(비정질 포함) 대량 탈락 — LiPON류·유리 phosphate가 후보군에서 구조적으로 배제(본문도 비정질 σ 우위 인정). 코팅은 실제로 비정질로 증착되는 경우가 많다는 점에서 **깔때기의 가장 자의적인 단계**.
- **NEB 프록시의 검증 실패 사례를 스스로 보고**: LiPO₃ 계산 0.40 vs 실험 1.40 eV, LiLa(PO₃)₄ 1.39 vs 0.92 eV — vacancy 형성에너지·기전(간극형)·GB·비정질 무시의 대가. **Table 2의 E_m으로 σ 순위를 정량 주장하면 안 됨**(그들도 "guidance" 수준으로 한정).
- **ΔE_rxt는 닫힌계 혼합**(전압 미인가): 충전 상태의 계면은 반충 양극으로 근사했을 뿐, open-system(전압 하) 반응성은 아님. 또 **100 meV/atom 컷은 관례적**(passivation 여부·산물 σ_e를 안 봄 — [Sundar]의 "산물 전도도가 진짜 지표" 비판이 정확히 이 지점을 침).
- **DB 스냅샷 의존**: 내부 MP-세대(2018) hull — [Zhu15]→우리(MP2026)에서 본 대로 **산화측 onset·산물은 hull 세대에 민감**(S-보정·신규 entry). Table S1의 V_ox 절대값을 현대 hull 수치와 섞어 쓰지 말 것.
- **Table S1은 184종 중 ICSD 106종만** 수록 — data-mined 78종은 미공개(재현 불가 영역).
- **전자전도 = KS gap 하한**: 점결함·비정질로 wide-gap도 전도 가능함을 자인 — gap 게이트(0.5 eV)는 금속만 거르는 1차 필터일 뿐. (우리 규율과 동일: 절대 gap 비교 금지.)
- **기계·계면 접착·열팽창·비용 축 전무** — 코팅 실용성의 절반(박막 공정성·기계 순응)은 스코프 밖. 우리 cascade가 기계 축(soft/ductile 35 %)을 넣은 것이 정확히 이 공백.
- **2019년 시점성**: "할라이드는 σ 문헌 부재로 보류" — 직후 할라이드 SE 붐(Li₃YCl₆·Li₃InCl₆·Li₂ZrCl₆)이 이 보류를 뒤집음([Cha]의 LZC 코팅이 실증). Filter 5는 지금 다시 하면 다른 결론이 나올 단계.
- **이해상충**: Samsung 자금 + 공저자 코팅 조성 특허 출원 명시 — 추천 물질 해석 시 참고.

## 11. 적용 인사이트 (cascade 벤치마크 발표용)
1. **계보 문장**: "우리 cascade는 Xiao 2019(Joule) 깔때기의 게이트 축 3종 — 상안정·grand-potential ESW·이온전도 프록시 — 을 계승하되, 순차 boolean 깔때기를 **UMA-상대 가중 score(0.30 ox+0.25 stable+0.20 soft+0.15 ductile+0.10 window)**로 바꿔 '탈락' 대신 '순위+trade-off'를 보존한다."
2. **추가 축 문장**: "Xiao가 비워둔 **기계 축(soft/ductile, 가중 35 %)**·**테마 조합·co-doping 교호작용 ML**·**MLIP(UMA) 상대 스크리닝**을 우리가 추가했고, 반대로 Xiao의 **양극(NCM/LCO) 반응성 게이트(&#124;ΔE_rxt&#124;<0.1 eV/atom·만충/반충)**와 **10⁵ 규모 후보 풀**은 우리에 없는 축이다 — 전자는 interface_reactivity의 Ni/Co/Mn chemsys 확장으로 이식 가능."
3. **물리 연속성 문장**: "Xiao의 결론 '비금속–O 공유결합이 O 2p를 끌어내려 산화 한계를 올린다'(meta>pyro>ortho, B–O 806 kJ/mol)는 우리 ICOHP P–O −8.43·B₂O₃ onset +0.18 V와 같은 물리 — 우리는 그 원리를 코팅 물질 선택이 아니라 **host 격자 도핑**으로 옮겨 실행한 것."
4. **실무 후속**: (a) cascade CSV에 **ΔE_rxt(vs LCO, 나중에 NCM) 열 추가**(pymatgen InterfaceReactions; Xiao Table S2가 정답지 — LPSCl/LCO −339 meV/atom 재현부터), (b) 우리 funnel 그림을 Xiao Fig 1 문법으로 제작, (c) 붕산염 3축 분리(산화↑/이동성↓/가수분해↓) 슬라이드에 Xiao·[Zhu20] 병기.
5. **경계 사례 교훈**: Xiao의 LiCoPO₄/LiNiPO₄ 탈락(액체계 스타 → 황화물계 부적합)은 "게이트는 *짝(전해질) 특이적*"의 상징 — 우리 도판트 랭킹도 host(Cl-rich argyrodite)·상대(LCO) 특이적임을 항상 명기.

## 12. 인용 가능 문장 (deck/paper용)
- "Xiao et al. (Joule 2019) screened 104,082 Li-containing compounds through four sequential gates — band gap > 0.5 eV, E_hull < 5 meV/atom, V_ox ≥ 4.0 V with V_red ≤ 2.7 V, and |ΔE_rxt| < 100 meV/atom against both Li₃PS₄ and NCM — leaving 184 candidates, of which polyanionic oxides (66) dominate; LiH₂PO₄, LiTi₂(PO₄)₃ and LiPO₃ were the final recommendations."
- "Their central design rule — covalent non-metal–oxygen bonding lowers the O 2p states and simultaneously raises the oxidation limit and suppresses O–S exchange — is the coating-side statement of the same physics we quantify inside the argyrodite lattice with ICOHP (P–O −8.43 vs P–S −5.98) and the B₂O₃-induced +0.18 V onset shift."
- "Our cascade inherits the Xiao-2019 gate axes (phase stability, grand-potential ESW, ion-mobility proxy) but replaces the sequential boolean funnel with a weighted composite score and adds the axes Xiao lacked — mechanical softness/ductility, theme combinations, co-doping interaction ML — while their cathode-reactivity gate and 10⁵-scale pool remain our to-do."
- (LPSCl 반응성 소환값) "In the same framework, bare Li₆PS₅Cl reacts with LiCoO₂ at −339 meV/atom (fully lithiated; −493 half-lithiated), producing Li₃PO₄, Li₂S/Li₂SO₄, Co₉S₈ and LiCl — the numbers behind 'sulfide SEs need cathode coatings'."
- **(SI 대조로만 나오는 문장, 2026-08-03)** "Notably, the conventional ternary-oxide coatings themselves — Li₂ZrO₃, LiNbO₃ and LiTaO₃ — do not appear among the 106 ICSD compounds that pass Xiao's own chemical-stability filter, since their reaction energies against Li₃PS₄ (−115, −164 and −139 meV/atom) exceed the 100 meV/atom cut-off; the incumbent coatings fail the very gate that selects their replacements."
- **(균형 문장 — 인용 시 함께 쓸 것)** "Fluorides, not polyanionic oxides, top the oxidation-limit ranking in Table S1 (all 35 ICSD fluorides ≥ 4.99 V, LiBF₄ at 7.15 V vs 6.23 V for the best phosphate); they were set aside solely for the lack of reported Li-ion conductivity in 2019, not for any stability deficit."

## 13. 기법 용어 미니사전
- **funnel/tiered screening**: 순차 게이트로 후보를 줄이는 HT 설계 — 각 게이트는 싼 계산부터(속성 조회→hull→ESW→반응성→NEB).
- **grand-potential ESW**: Φ=E−n_Li·μ_Li의 hull로 전압창 산출 ([Zhu15] 원전; Eq 1–3).
- **pseudo-binary ΔE_rxt**: 두 상을 x:(1−x)로 섞어 hull로 떨어지는 최악 반응에너지(Eq 4) — 계면 반응성 프록시(닫힌계).
- **polyanionic oxide**: 비금속-산소 클러스터 음이온(PO₄³⁻·BO₃³⁻·SiO₃²⁻·SO₄²⁻…)을 가진 산화물 — 이 논문의 정의로 LiNbO₃·LiTaO₃·Li₂ZrO₃는 *비*폴리음이온.
- **ortho/pyro/meta-phosphate**: PO₄³⁻ / P₂O₇⁴⁻ / PO₃⁻ — 축합도 순. 축합↑=O/P↓=O–P 공유성↑=V_ox↑.
- **inductive effect**: 폴리음이온의 강한 X–O 공유결합이 TM–O 이온성을 키워 redox 전압을 올리는 효과(phosphate 양극 고전압의 고전 논리) — 여기선 코팅 산화한계로 전용.
- **percolating pathway (NEB)**: 개별 hop을 이어 supercell을 관통하는 vacancy 경로 — 장거리 전도의 최저 필요 장벽.
- **coating paradox**: 완전 절연 코팅=redox 차단, 불완전 코팅=노출면 분해 — 형태학 설계 문제.
- **dead space**: 코팅이 못 덮는 SSE/carbon·SSE/집전체 계면의 분해층 — 이온 수송 저해 잠재 저항원.

## 14. 본문 실물 독립 재검증 로그 (2026-08-03) ★
**대상**: `litdb/inbox/37. Computational Screening of Cathode Coatings for Solid-State Batteries.pdf` (25 pp, 본문 전문). 사용자 분류 폴더 `DFT`.
**방법**: PDF 텍스트 전량 추출 후 digest의 모든 본문 유래 수치·문장을 무편향으로 재대조(2026-07-28 digest 내용을 참조하지 않고 PDF에서 먼저 값을 뽑은 뒤 비교).

### 14a. 판정 — **불일치 0건**
전량 일치 확인 항목: 깔때기 수(104,082 / 1,600 / 302 / 184 / ICSD 106 / 폴리음이온 66) · **Table 1 전 18셀**(수·백분율) · 통과율(F3 26.5 vs 7.8 % / F4 60.6 vs 6.5 %) · 게이트 임계값(Eg>0.5 · E_hull<0.005 eV/atom · V_ox≥4.0 · V_red≤2.7 · |ΔE_rxt|<100 meV/atom · 황화물 창 2.2–2.7 V) · **Table 2 전 7행 전 6열**(ICSD #·E_m·실험 Ea·σ_ion·KS gap·σ_e, 각주 a/b 포함) · **Table 3 전 6행**(3.44/4.52/4.09/5.44/4.26/4.61 V + 분해산물) · Fig 4 판독(황화물<2.5 · LLZO 2.9 · 3원 산화물 3.4–4.0 · 폴리음이온≥4.5 · LiTi₂(PO₄)₃ 4.6 · meta 3종≥5 · LNMO 4.7 V) · Fig 6 표본수(150 = ortho 31 + pyro 23 + meta 96) · Fig 7(LiPO₃ (5 V, 0.20) · 66 중 25종 ≥4.5 V · Li₃PO₄ 4.22 V → 한도 0.38) · 결합해리E(P–O 597 / P–S 346 / Co–O 368 / Co–S 343 / B–O 806 kJ/mol) · LPS/NCM 422 meV/atom(=40.7 kJ/mol) · LiCoPO₄·LiNiPO₄ 탈락(150 meV/atom vs LPS) · 무반응 할라이드 5종 · 액체계 실적값(LiCoPO₄ 4.19 / LiNiPO₄ 4.22 / LiTi₂(PO₄)₃ 4.59) · 고Li·고V_ox 예외군(LiGd(PO₃)₄ 5.30/0.96 · LiK(PO₃)₂ 5.09/1.89 · LiDy(PO₃)₄ 4.86/0.96) · H⁺ 교환 구동력(LCO/NCM ~60 · LMO 4 meV/atom · LFPO 비자발) · NCM 계산 gap 1.5 eV · LiTi₂(PO₄)₃ σ_e ~10⁻⁹ vs NCM 10⁻²–10⁻⁷ · 방법 전량(VASP·PAW·GGA/GGA+U(Jain 2011)·**520 eV**·**k≥500/n_atom**·pymatgen·Eq 1–4·**NEB 400 eV**·균일 배경전하·단일 vacancy·최저에너지 구조만) · 서지(Received 2018-11-21 / Accepted 2019-02-19 / Published 2019-03-21) · COI 문장.
**참조번호 실물 대조도 전량 일치**: ref 18 Ong 2013 / 30 **Richards 2016** / 31 **Zhu 2015** / 32 Zhu-He-Mo 2016 / 33 Tang-Ong 2018 / 35 Miara 2015 / 44 Jung-Kang-정윤석 2018 / 46 Aykol 2016 / 47 Sakuda 2008 / 56 Han 2016 / 60 Wang 2016 / 61 Asano 2018(Li₃YCl₆) / 82 Money 2007 / 88 Chong 2016 / 96 Sendek 2017 / 111 Jain 2011 / 113 pymatgen.

### 14b. 이번에 **새로 반영**한 것 (기존 digest의 오류가 아니라 미수록분)
1. **Fig 3B 정량 3진술** — 비폴리 전량 NCM<50 meV / 3/4↑ LPS≥200 meV / 폴리음이온 60 %↑ 양쪽≤100 meV + 본문 환산(50/100/200 meV ≡ 4.8/9.6/19.3 kJ/mol) → §3, §8.
2. **NCM·LPS 양쪽 ΔE_rxt=0인 폴리음이온**: LiAlSiO₄(4.09)·Li₃PO₄(4.22) — LiBa(B₃O₅)₃급 안정성이나 V_ox가 낮아 대표 6종 제외 → §3.
3. **이온전도를 게이트에 넣은 동기 2건**: Sakuda 2008 Li₂O–SiO₂ 코팅 rate 우위(ref 47) + **정윤석 그룹 LBCO vs LBO σ 2 자릿수**(ref 44) → §2.
4. **P→인화물 kinetic 선호 주장(ref 33)에 대한 저자 유보** — "실험 확인 필요" 원문 → §6b. 우리 분해산물 서사 방어용.
5. **인공 SEI 정량 대비**: 자연 SEI 상호확산 ≤50 nm vs 코팅 제어 두께 1–10 nm → §6b.
6. **LiTaO₃/NCM·LiNbO₃/LCO 만충·반충 모두 0**, LiNbO₃-코팅 LCO·LMO 황화물 SSB 실증(refs 20/41), **Li₂ZrO₃가 LMO/LLZO 최적** → §6a.
7. 서지 정밀화: **SAIT는 연구비(주 재원)이지 소속이 아님**(Miara·Wang = Samsung Research America, Advanced Materials Lab) + Revised 2019-02-09 + MP Program KC23MP → 헤더.
8. Zhu 2016 목록의 **Li₅TaO₅ 판독 확정**(기존 "(판독)" 표기 해제) → §2.
9. **필터 번호 내부 불일치 명시**: Table 1 각주(=F4 화학안정) vs p.1267 본문·Fig 7A 캡션(="filter 5") → §3.
10. 62,437의 출처를 **Fig 1 판독**으로 명기(본문은 "more than 62,000"만) → §3.

### 14c. 이번 회차 스코프 밖 (재검증 안 됨)
- ~~**SI(Table S1–S6·Fig S1)는 이번 inbox 드롭에 없음**~~ → **2026-08-03 Sup2 드롭으로 해소됨. §15 참조.** (당시 기록: §4a 개별 hop 배열·§4a ESW 표·§4b ΔE_rxt 매트릭스 전량·§4c 분해산물은 2026-07-28 SI 정독분이며 재대조 안 됨. 본문이 언급하는 SI 유래 값(LPS/NCM 422·LiCoPO₄ 150·H⁺ 교환 60/4 meV/atom·Li₃PO₄ 4.22·LiAlSiO₄ 4.09)만 교차 확인되어 일치.)
- Fig 1·2·3·5·7·8·9의 그래픽 세부(막대 눈금·색맵 경계)는 텍스트 추출로 재검증 불가 — 기존 figure-read 표기 유지(특히 **LPSCl ESW ~1.7–2.0 V**는 여전히 figure-read).

## 15. SI 실물 독립 재검증 로그 (2026-08-03, Sup2 드롭) ★★
**대상**: `litdb/inbox/37. Sup2) Computational Screening of Cathode Coatings for Solid-State Batteries.pdf` — **35 pp = 본문 p.1–25 + SI p.26–35**. 사용자 분류 폴더 `DFT`.
**동일성 확인**: p.1–25가 본문(#37 25 pp)과 동일, p.26이 "JOUL, Volume 3 / Supplemental Information", p.27 Fig S1, p.28–30 Table S1, **p.31 Table S2**, **p.32 Table S3**, p.33–34 Table S4, p.34–35 Table S5, p.35 Table S6. → **INDEX의 기존 판정 "Sup2 = 본문+SI 합본, 신규 내용 0"이 페이지 단위로 재확인됨.** 다만 **이번 드롭의 실제 가치는 §14c가 남겨둔 SI 공백을 메운 것** — SI 유래 수치가 처음으로 *독립 재대조*됐다.
**방법**: pdftotext 텍스트층은 Table S1·S4·S5에서 **열이 행 단위로 밀리는 정렬 붕괴**가 있어 좌표(word-bbox y-클러스터) 기반으로 행을 재구성; **Table S2·S3은 텍스트층이 없는 래스터 이미지**(p.31 1540×1200 px, p.32 1182×1430 px)라 260 dpi 렌더 후 육안 대조. ⚠ 후속 재검증자 주의: 이 두 표는 grep으로 검증 불가.

### 15a. 판정 — **digest 대비 불일치 0건** (수치 오류 없음)
| SI 항목 | 대조 범위 | 결과 |
|---|---|---|
| **Table S2** (만충 ΔE_rxt) | **전 76셀** (코팅 9종+SSE 4종 × 양극 4·SSE 4) | **전량 일치** — §4b 첫 번째 수 전부 |
| **Table S3** (반충 ΔE_rxt) | **전 52셀** (13행 × 양극 4) | **전량 일치** — §4b 두 번째 수 전부 |
| **Table S1** (ESW·반응성) | 대표 6종 + 참조 4종 = **12개 ESW 값** + 전 106행 집계 | **전량 일치** (LiCs(PO₃)₂ 2.15–6.23 / LiLa(PO₃)₄ 2.51–5.03 / LiPO₃ 2.52–5.01 / LiBa(B₃O₅)₃ 1.30–4.83 / LiTi₂(PO₄)₃ 2.37–4.59 / LiH₂PO₄ 2.23–4.58 / Li₃PO₄ 0.71–4.22 / LiAlSiO₄ 1.14–4.09 / LiZr₂(PO₄)₃ 2.06–4.52 / Li₄P₂O₇ 2.33–4.36; 추가 확인 LiGd(PO₃)₄ 5.30 · LiK(PO₃)₂ 5.09 · LiDy(PO₃)₄ 4.86) |
| **Table S6** (NEB 전 hop) | **7물질 전 hop 배열** | **전량 일치** — §4a 목록과 문자 단위 동일 |
| **Table S4/S5** (분해산물) | 우리 관심 계면 8종 | **전량 일치** (LPSCl/LiPO₃ · LPSCl/LiH₂PO₄ · LPSCl/LiTi₂(PO₄)₃ · LPSCl/LiBa(B₃O₅)₃ · LCO/LPSCl · NCM/LiH₂PO₄ · LLZO/LiPO₃ · LLZO/LiLa(PO₃)₄) — 단 NCM·LCO/LPSCl **반충** 산물 서술을 정밀화(§15b-1) |
| **Fig S1** (경로 캡션) | 7물질 percolating 경로 | **일치** (LiPO₃ 1→2→…→8→1 등) |
| **행수** | Table S1 = 106행 | **일치** (Cl 10 + F 35 + NP 2 + OF 4 + P 55 = 106; 캡션 "106 ICSD out of 184"와 정합) |

→ 2026-07-28 SI 정독분은 **1년 가까이 지난 지금 재대조해도 수치 오류가 없다.** §4b 매트릭스(128셀)는 이제 **육안 이미지 대조로 확정**.

### 15b. 이번에 **새로 반영·정정**한 것
1. **[정정] NCM/LPSCl·LCO/LPSCl 반충 산물** — 기존 "(반충: +Li₂O)"는 불완전. 실제로는 **Li₂O 추가 + Li₂S 소멸**(만충 Li₂S ↔ 반충 Li₂O 치환)이며 두 양극 모두 같은 패턴 → §4c. *수치 오류가 아니라 서술 누락.*
2. **[신규·최상급] 기존 3원 산화물 코팅 3종(Li₂ZrO₃·LiNbO₃·LiTaO₃)이 Table S1에 부재 = 저자 자신의 filter 4 탈락**(LPS와 −115/−164/−139 meV/atom) → §3. 본문이 문장화하지 않은 이 논문의 *숨은* 최강 논거.
3. **[신규] 비폴리음이온 산화물 생존 2종의 정체** = **Li₃V(H₄O₃)₄(1.92–4.17 V) · LiAl₅O₈(0.85–4.09 V)** — 둘 다 V_ox<4.2, 하나는 수화물 → "2종 생존"은 사실상 전멸 → §3.
4. **[신규] Table S1 전수 지도**(군별 n·V_ox 범위·챔피언) + **불화물이 산화한계 최강(35종 전부 ≥4.99 V, LiBF₄ 7.15 V > 폴리음이온 최고 6.23 V)** → §4a-2. **"폴리음이온이 이겼다" 서사의 가장 약한 고리** — 불화물을 버린 근거는 안정성이 아니라 σ 문헌 부재뿐.
5. **[신규] V_ox ≥ 5.00 V 폴리음이온 = 7종 전부 meta-phosphate**(LiSm(PO₃)₄ 5.19·LiAl(PO₃)₄ 5.01 신규 수록) — §6a 축합 위계의 예외 0 확증 → §4a-2.
6. **[신규] 삼중 0 반응성(LPS·만충NCM·반충NCM 모두 0.000) = LiF · LiCs(B₃O₅)₂(4.52) · Li₃PO₄(4.22)** 3종뿐 → §3.
7. **[신규·논문 내부 불일치] 본문 p.1265 "LiAlSiO₄ and Li₃PO₄ … zero reactivity with NCM and LPS" vs Table S1 LiAlSiO₄ = 만충 NCM −0.009 eV/atom** — 엄밀 삼중 0은 Li₃PO₄뿐 → §3. *digest 오류가 아니라 논문 자체의 본문–SI 불일치.*
8. **[신규] 완전 무반응 할라이드 5종 중 LiRb₂Cl₃는 Table S1에 없음** = data-mined 출신(비-ICSD) — 본문 p.1266 문장은 확인됨. 재현 가능한 것은 LiF·LiCl·LiRbCl₂·LiCsCl₂ 4종뿐 → §10 "미공개 78종" 한계의 구체 사례.

### 15c. 이번 회차에도 스코프 밖
- **Fig S1의 구조 그래픽**(다면체·vacancy 위치)은 이미지라 캡션만 대조 — 경로 번호열은 확인, 결정학적 세부는 미검증.
- Table S1의 **나머지 94행 개별 수치**(우리가 인용하지 않는 조성)는 집계·정렬 규약만 확인하고 셀 단위 대조는 안 함.
- 본문 Fig 1–9 그래픽 세부는 §14c와 동일하게 여전히 figure-read (**LPSCl ESW ~1.7–2.0 V** 포함).
