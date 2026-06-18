# 보고서 — 고체전해질 산화안정성: VBM이 아니라 Grand-Potential 분해창으로 평가하는 근거

작성 2026-06-18. 대상: argyrodite LPSCl(comp1) / LPSCl1.6(modelC) / Nd₂O₃-doped(nd).
출처: db/properties/{oxidation_stability,electronic}.json, db/literature/, tools/oxidation/esw_grand_potential.py.
(발표용 아닌 전수 보고용.)

---

## 0. 한 줄 요약 (Executive Summary)

> **VBM·밴드엣지는 "전자(밴드)·계면 정렬 안정성"의 지표로 논문에 쓰이지만, 분해형 고체전해질의 "산화안정성(분해 한계)" 표준 정량값은 VBM이 아니라 grand-potential 분해창이다.** 밴드엣지 기반 창은 실제 열역학 창을 2–3배 과대평가한다(재료가 밴드엣지에 닿기 전에 분해하므로). 우리 데이터가 직접 증거: comp1·modelc는 VBM이 다른데도 산화 onset이 둘 다 2.14 V로 동일하고, nd는 갭이 좁아지는데도 산화가 좋아진다 → **VBM/갭 트렌드 ≠ 산화 트렌드.**

---

## 1. 질문
"논문에서는 산화안정성을 VBM 등 정량값으로 안 보나? 우리도 VBM으로 보고하면 안 되나?"

## 2. 결론 (3개 층위)
| # | 주장 | 근거 |
|---|---|---|
| L1 | VBM=산화한계는 **분자(액체전해질)** 직관 | HOMO ≈ −IP (Koopmans, 수직 이온화) |
| L2 | **고체에서는 깨짐** — 산화=전자제거가 아니라 **상 분해** | 관련 양은 단일입자 고유값이 아니라 분해 자유에너지 |
| L3 | 게다가 **절대 VBM은 셀 간 비교 불가** (진공/정전포텐셜 정렬 필요·불안정) | KS 고유값 기준점이 셀마다 다름 |
| 표준 | 분야 표준 = **grand-potential 분해창** | Ong 2008 → Mo 2012 → Zhu 2015/16 → Richards 2016 → Schwietert 2020 |

---

## 3. 왜 "VBM=산화한계" 직관이 생기나 — 분자(액체)
| | 분자(액체전해질) | 고체전해질 |
|---|---|---|
| 산화 사건 | 분자에서 전자 1개 제거 (HOMO) | 결정이 새 상으로 **분해** |
| 정량값 | E(HOMO) ≈ −IP (수직, Koopmans) | ΔG_decomp (grand potential) |
| 잘 맞나 | **꽤 맞음** (HOMO↔산화, LUMO↔환원) | **안 맞음** (분해가 먼저) |
| 대표 | 전해액 스크리닝(Borodin 2013 등) | Mo/Zhu/Schwietert |
> 분자에서 HOMO가 통하니까 "고체는 VBM 보면 되잖아"가 나온다. 이게 함정.

## 4. 고체에서 깨지는 두 이유
**(a) 산화 ≠ 전자 한 개 빼기 = 분해.** S²⁻가 전자를 잃는 "산화"는 실제로는 결정이
`Li₃PS₄ + LiS₄(폴리설파이드) + LiCl + Li`로 **분해**되는 사건. 이 한계는 분해반응
자유에너지(grand potential)로 결정되지, VBM 고유값 하나로 결정되지 않는다.
밴드엣지(전자/정공 주입) 창은 **실제 열역학 창을 2–3배 과대평가**한다(Schwietert 2020:
"band-gap window" vs "delithiation/decomposition window"를 한 논문에서 명시적으로 분리).

**(b) 절대 VBM은 셀 간 비교조차 안 된다.** DFT KS 고유값의 0점(기준)은 셀·계산마다 다르다.
서로 다른 셀(comp1 52원자 vs modelc 62원자 vs nd)의 절대 VBM을 비교하려면 진공준위 또는
평균 정전포텐셜 정렬이 필요한데, bulk 주기계에서는 이 정렬이 불안정/부정확하다.
→ "comp1 2.128 vs modelc 2.445" 같은 절대 VBM **트렌드 자체가 rigorous하게 정의되지 않음.**

---

## 5. 그럼 VBM은 논문에 어디 쓰이나 — 용도 구분
| 용도 | VBM 쓰나? | 무엇을 말하나 |
|---|---|---|
| 밴드 정렬(band alignment) | **예** | SE의 VBM/CBM을 전극 Fermi에 맞춰 전자/정공 주입·**계면(전자적) 안정성** |
| UPS/XPS 실험 보고 | **예** | 측정된 VBM 위치 (band alignment 용) |
| 상한(upper-bound) 스크리너 | 종종 | "최소 이 전압까진 전자적으로 버틴다"는 낙관적 상한 |
| **산화안정성(분해 한계)** | **아니오** | ← 이건 grand-potential 분해창으로 |
> 즉 VBM은 정량값으로 **쓰이긴 하나 다른 물리량(전자/계면 안정성)** 이고, **분해 산화한계의 표준값이 아님.**

---

## 6. 분야 표준 = Grand-Potential 분해창 (우리가 쓴 방법)
| 단계 | 문헌 | 기여 |
|---|---|---|
| 방법 기원 | Ong 2008 (Chem. Mater. 20, 1798) | grand-canonical(open w.r.t. Li) 상도 |
| SE 적용 | Mo–Ong–Ceder 2012 (Chem. Mater. 24, 15) | LGPS 전기화학창 = 상평형으로 |
| 일반화 | Zhu–He–Mo 2015 (ACS AMI 7, 23685) | "outstanding stability의 기원" 열역학 |
| 계면 | Richards–Ceder 2016 (Chem. Mater. 28, 266) | 계면 분해 안정성 |
| **결정적** | **Schwietert 2020 (Nat. Mater. 19, 428)** | 황화물에서 **밴드창(과대)** vs **분해창(실제)** 분리 |

**우리 값 (tools/oxidation/esw_grand_potential.py, MP hull):**
| | comp1 | modelC |
|---|---|---|
| OCV 자가분해 | **1.72 V** → Li₃PS₄+Li₂S+LiCl | **1.72 V** → Li₃PS₄+0.4Li₂S+1.6LiCl |
| 환원 한계 | 1.24 V | 1.24 V |
| **산화 onset** | **2.14 V** (S²⁻→LiS₄) | **2.14 V** (S²⁻→LiS₄) |
> Cl⁻는 전기화학적으로 불활성 → 산화는 둘 다 **S²⁻-limited라 동일**(2.14 V).

---

## 7. ★ 우리 데이터가 직접 증거 — "VBM/갭 트렌드 ≠ 산화 트렌드"
| 시스템 | VBM(abs, eV)¹ | 밴드갭(eV) | **산화 onset(V)** | 산화안정성 경향 |
|---|---|---|---|---|
| comp1 (LPSCl) | 2.128 | 2.066 | **2.14** | 기준 |
| modelC (LPSCl1.6) | 2.445 (**+0.32**) | 2.099 | **2.14 (동일)** | 내재 동일·구속/계면서 유리 |
| nd (Nd₂O₃-doped) | 3.081 (**+0.95**) | 1.632 (**−0.43, 좁아짐**) | (O로) **향상** | O-도핑이 산화 개선 |

¹ 절대 VBM은 정렬 미보정(§4b) — 트렌드 자체가 비엄밀. 그래도 "단조 증가"인데:
- **VBM은 2.128→2.445→3.081로 단조 증가**, **갭은 2.066→2.099→1.632(nd서 좁아짐)** 인데,
- **산화 onset은 comp1=modelc로 불변(2.14 V)이고 nd는 오히려 향상.**
> **만약 VBM(또는 갭)이 산화안정성을 결정한다면 이 셋이 다 달라야 한다. 실제로는 산화 트렌드가
> VBM/갭과 따로 논다.** → 산화안정성은 VBM이 아니라 grand-potential(분해 화학)로 봐야 함이 **우리
> 계산 안에서 자체 증명**된다.

---

## 8. 문헌 검증 (우리 grand-potential 값이 실험·타 계산과 일치)
| 문헌 | 그들 값 | 우리 값과 비교 |
|---|---|---|
| Gil-González 2022 (constrained-ESW) | LPSCl1.5 안정창 1.70–2.40 V (K_eff=0) | 우리 modelc 1.72/2.14 V와 정합 |
| Gil-González 2022 (실험) | LPSCl1.5 ~1.8–2.5 V, LPSCl1.0 ~1.3–2.3 V | 우리 onset 2.14 V가 실험 범위 내 |
| Zuo 2023 (CV/ToF-SIMS) | 분해식 Eq(1)/(2) | 우리 onset 분해식을 거의 그대로 재현 |
> 즉 grand-potential은 **실험 창을 정량 재현**한다. VBM 절대값으로는 이런 실험 정합을 줄 수 없다.

---

## 9. 논문에 쓸 문장 (EN, 그대로 인용 가능)
> *"Electrochemical (oxidation) stability is evaluated from the grand-potential
> decomposition window (Ong 2008; Mo 2012; Schwietert 2020), not from the valence-band
> maximum, because band-edge–based windows overestimate the thermodynamic decomposition
> limit of a solid electrolyte by 2–3×; the VBM/CBM is reported only for electrode band
> alignment. Consistent with this, comp1 and the Cl-rich variant share an identical
> intrinsic oxidation onset (2.14 V vs Li/Li⁺, S²⁻→polysulfide) despite differing
> band-edge positions, confirming that the oxidation limit is set by S²⁻ decomposition
> chemistry rather than by the single-particle band edge."*

---

## 10. References (full)
1. S. P. Ong et al., *Chem. Mater.* **20**, 1798 (2008) — Li–Fe–P–O₂ grand-potential phase diagram (방법 기원).
2. Y. Mo, S. P. Ong, G. Ceder, *Chem. Mater.* **24**, 15 (2012) — LGPS 전기화학창(상평형).
3. Y. Zhu, X. He, Y. Mo, *ACS Appl. Mater. Interfaces* **7**, 23685 (2015) — SE 안정성 열역학.
4. Y. Zhu, X. He, Y. Mo, *J. Mater. Chem. A* **4**, 3253 (2016) — 계면 화학/전기화학 안정성.
5. W. D. Richards et al., *Chem. Mater.* **28**, 266 (2016) — 계면 안정성.
6. T. K. Schwietert et al., *Nat. Mater.* **19**, 428 (2020) — 밴드창 vs 분해창 분리 (**핵심**).
7. O. Borodin et al., *J. Phys. Chem. C* **117**, 8661 (2013) — 분자 산화/HOMO (L1 출처 예).
8. R. Gil-González et al. (2022) — constrained-ESW, LPSCl1.5 창 (우리 값 검증).
9. C. Zuo et al. (2023) — Cl-rich argyrodite CV/ToF-SIMS 분해 (우리 onset 재현).

### Caveat (보고 시 명시)
- 절대 VBM 비교는 정전포텐셜 정렬 미보정이라 **비엄밀**(§4b) — 본 보고선 "트렌드도 산화와 무관"을 보이는 보조 근거로만 사용.
- grand-potential 창은 0 K·0 Pa·MP(GGA/GGA+U) hull 기준 — 절대 onset은 GGA 한계로 ±0.x V; 단 comp1↔modelc **상대 비교와 실험 창 정합은 robust**(§8).
