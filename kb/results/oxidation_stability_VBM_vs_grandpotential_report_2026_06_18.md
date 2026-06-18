# 보고서 — 산화안정성: VBM/UPS가 아니라 Grand-Potential 분해창으로 평가 (LPSCl vs LPSCl1.6)

작성 2026-06-18 (rev: nd 제외, 실험(UPS↔CV) 대응 추가). 대상: argyrodite **LPSCl(comp1) vs LPSCl1.6(modelC)**.
출처: db/properties/{oxidation_stability,electronic}.json, db/literature/, tools/oxidation/esw_grand_potential.py.
(발표용 아닌 전수 보고용. 0K DFT 수렴구조 기준.)

---

## 0. 한 줄 요약 (Executive Summary)

> **분해형 고체전해질의 "산화안정성(분해 한계)" 표준 정량값은 VBM(계산)·UPS(실험)가 아니라
> grand-potential 분해창(계산)·CV/LSV(실험)이다.** 밴드엣지(VBM/UPS) 기반 창은 실제 열역학
> 분해창을 2–3배 과대평가한다(재료가 밴드엣지에 닿기 전에 분해하므로). 우리 데이터가 직접 증거:
> **comp1과 modelC는 VBM이 다른데도 산화 onset이 둘 다 2.14 V로 동일**하다 — 산화는 밴드엣지 위치가
> 아니라 S²⁻ 분해화학이 결정한다.

---

## 1. 질문
1. "논문에서는 산화안정성을 VBM 등 정량값으로 보나? 우리도 VBM으로 보고하면 되나?"
2. "그럼 실험에서 **UPS**로 전해질 산화안정성 구하는 건 맞는가?"

## 2. 결론 (층위)
| # | 주장 | 근거 |
|---|---|---|
| L1 | VBM=산화한계는 **분자(액체전해질)** 직관 | HOMO ≈ −IP (Koopmans, 수직 이온화) |
| L2 | **고체에서 깨짐** — 산화 = 전자 1개 제거가 아니라 **상 분해** | 관련 양은 고유값이 아니라 분해 자유에너지 → grand-potential |
| L3 | **절대 VBM은 셀 간 비교 불가** | KS 고유값 기준점이 셀마다 다름(정전포텐셜 정렬 필요·불안정) |
| 표준 | 계산=**grand-potential 분해창**, 실험=**CV/LSV** | Ong08→Mo12→Zhu15/16→Richards16→Schwietert20 |

---

## 3. 왜 "VBM=산화한계" 직관이 생기나 — 분자 vs 고체
| | 분자(액체전해질) | 고체전해질 |
|---|---|---|
| 산화 사건 | 분자에서 전자 1개 제거(HOMO) | 결정이 새 상으로 **분해** |
| 정량값 | E(HOMO) ≈ −IP (수직) | ΔG_decomp (grand potential) |
| 잘 맞나 | **꽤 맞음** | **안 맞음** (분해가 먼저) |
> 분자에서 HOMO가 통하니까 "고체는 VBM 보면 되잖아"가 나온다 — 이게 함정.

## 4. 고체에서 깨지는 두 이유
**(a) 산화 ≠ 전자 빼기 = 분해.** comp1의 산화는 실제로 결정이
`Li₆PS₅Cl → Li₃PS₄ + 0.25 LiS₄(폴리설파이드) + LiCl + 1.75 Li` 로 **분해**되는 사건.
이 한계는 분해 자유에너지(grand potential)로 결정되지, VBM 고유값 하나로 결정되지 않는다.
밴드엣지(전자/정공 주입) 창은 **실제 열역학 창을 2–3배 과대평가**(Schwietert 2020이
"band-gap window"(과대) vs "delithiation/decomposition window"(실제)를 한 논문에서 분리).

**(b) 절대 VBM은 셀 간 비교조차 안 됨.** DFT KS 고유값의 0점은 셀·계산마다 다르다.
comp1(52원자) vs modelC(62원자)의 절대 VBM을 비교하려면 진공준위/평균 정전포텐셜 정렬이
필요한데 bulk 주기계에선 불안정/부정확 → "절대 VBM 트렌드" 자체가 비엄밀.

---

## 5. 그럼 VBM은 논문 어디에 쓰이나 — 용도 구분
| 용도 | VBM 쓰나 | 무엇을 말하나 |
|---|---|---|
| 밴드 정렬(band alignment) | **예** | SE의 VBM/CBM을 전극 Fermi에 맞춰 전자/정공 주입·**계면(전자적) 안정성** |
| UPS/XPS 실험 보고 | **예** | 측정된 VBM 위치(band alignment 용) |
| 상한(upper-bound) 스크리너 | 종종 | "최소 이 전압까진 전자적으로 버틴다"는 낙관적 상한 |
| **산화안정성(분해 한계)** | **아니오** | ← grand-potential(계산)/CV(실험)로 |

---

## 6. ★ 실험 측정법 대응 — UPS ↔ CV/LSV ↔ DFT
**UPS가 실제로 재는 것:** VBM(E_F 기준) + work function(SECO) → **이온화에너지 IE = φ + (E_F−VBM)**,
즉 **수직 이온화 = 밴드엣지**. DFT의 VBM과 **같은 물리량**이다.

| 물리량 | DFT | 실험 | 의미 |
|---|---|---|---|
| 밴드엣지/이온화 | VBM 고유값 | **UPS**(+IPES로 CBM) | 밴드 정렬·전자 안정성 → **과대평가** |
| **분해창(진짜 산화)** | **grand-potential** | **CV / LSV**(전류 onset) | 전기화학 분해 한계 |
| 분해 생성물 | 반응식 | **XPS / ToF-SIMS** | 무엇으로 분해되나 |

**안정성 창 위계(보통):** grand-potential(가장 좁음/보수적) ≤ CV/LSV(passivation으로 약간 넓어짐)
≪ UPS 밴드엣지(가장 넓음/낙관적).

**→ 우리 실험에서 UPS는?**
1. UPS로 VBM 구한 것 **자체는 맞고 유용** — 단 라벨을 "**band alignment / 전자적 계면 안정성**"으로.
2. **"전해질 산화안정성(분해 전압)"으로 쓰려면 UPS 단독은 부적절** — 그건 **CV/LSV**로. (우리 grand-potential 2.14 V의 실험 짝 = CV)
3. caveat: UPS는 **표면 민감(~1–2 nm)**(표면 오염/band bending) + **수직 이온화**라 열역학(adiabatic) 분해와 또 다름.

---

## 6b. ★ band gap의 두 용법 — 산화안정성 ✗ vs 분해억제 ✓ (혼동 금지)
같은 "DOS band gap"이 **두 가지 다른 것**에 쓰이며 섞으면 안 됨:
| 용법 | band gap이 말하는 것 | 맞나 | 올바른 방법 |
|---|---|---|---|
| **(A) 벌크 SE 갭 → 산화안정성** | 분해 onset 전압 | ❌ **아님** | grand-potential 분해창 (§7; 2.14 V) |
| **(B) SEI/분해산물 갭 → 분해 억제** | 전자차단 → self-limiting | ✅ **맞음** | 산물별 band gap (wide=전자차단) |

- 문헌(예: **Li et al., Energy Storage Mater. 77 (2025) 104221**, CuBr₂-doped argyrodite; LiBr/LiCl gap > Li₂S via PDOS)이 *"large bandgap → electronic insulation → blocks the electronic pathway → **prevents further decomposition**"* 라 하는 건 전부 **(B)**. 그들은 일부러 **"분해 억제/전자차단"** 이라 하지 **"oxidation stability"라고는 안 함.**
- 즉 **"band gap → 분해억제"(SEI 전자차단, kinetic, self-limiting)는 맞고**, **"band gap → 산화안정성"(분해 onset, thermodynamic)은 틀림.** (A)는 §3–5(VBM/bulk gap≠산화 onset) 결론과 동일; (B)는 SEI passivation 영역(전자차단 산물: LiCl 6.65·Li₃PO₄ 5.73·Li₂O 5.24 eV).
- ⚠️ 예: Nd₂O₃ 도핑서 bulk 갭이 좁아져도(Nd 5d) "산화 나빠짐"이라 읽으면 안 됨 — 산화 onset은 grand-potential(§7).

> **한 줄: (A) bulk 갭→산화안정성 ✗ / (B) SEI산물 갭→분해억제 ✓. 문헌의 "band gap→분해억제"는 전부 (B)이고, VBM/bulk-gap을 산화 onset으로 읽으면 안 됨(§3–8).**

## 7. 분야 표준 = Grand-Potential 분해창 + 우리 값
| 단계 | 문헌 | 기여 |
|---|---|---|
| 방법 기원 | Ong 2008 | grand-canonical(open w.r.t. Li) 상도 |
| SE 적용 | Mo–Ong–Ceder 2012 | LGPS 전기화학창=상평형 |
| 일반화 | Zhu–He–Mo 2015 | SE 안정성 열역학 |
| 계면 | Richards–Ceder 2016 | 계면 분해 안정성 |
| **결정적** | **Schwietert 2020 (Nat. Mater.)** | **밴드창(과대) vs 분해창(실제) 분리** |

**우리 값 (tools/oxidation/esw_grand_potential.py, MP hull):**
| | comp1 (LPSCl) | modelC (LPSCl1.6) |
|---|---|---|
| OCV 자가분해 | **1.72 V** → Li₃PS₄+Li₂S+LiCl | **1.72 V** → Li₃PS₄+0.4Li₂S+1.6LiCl |
| 환원 한계 | 1.24 V | 1.24 V |
| **산화 onset** | **2.14 V** (S²⁻→LiS₄) | **2.14 V** (S²⁻→LiS₄) |
> Cl⁻는 전기화학적으로 불활성 → 산화는 둘 다 **S²⁻-limited라 동일(2.14 V)**.

---

## 8. ★ 우리 데이터가 직접 증거 — "VBM 달라도 산화 onset 동일"
| | comp1 (LPSCl) | modelC (LPSCl1.6) | Δ |
|---|---|---|---|
| VBM (abs, eV)¹ | 2.128 | 2.445 | **+0.32** |
| 밴드갭 (eV) | 2.066 | 2.099 | +0.033 |
| VBM 성분 | S 3p ~96% | S 3p ~97% | 동일 |
| **산화 onset (V)** | **2.14** | **2.14** | **0 (동일)** |

¹ 절대 VBM은 정렬 미보정(§4b) — 비엄밀. 그래도:
- **VBM을 액면 그대로 믿으면** modelC가 +0.32 eV 높으니 "산화창이 ~0.3 V 다르다"고 예측해야 한다.
- **그러나 실제 산화 onset은 둘 다 2.14 V로 정확히 동일.** 이유: 둘 다 VBM=S 3p이고 산화가
  **S²⁻→폴리설파이드 분해로 S²⁻-limited** → 밴드엣지가 어디 있든 **분해화학이 같아 onset이 같다.**
> **VBM(밴드엣지)이 산화를 결정한다면 +0.32 eV 차이가 onset에 보여야 하는데, 안 보인다.**
> → 산화안정성은 VBM이 아니라 grand-potential(분해화학)로 봐야 함이 **우리 두 시료 비교 안에서 자체 증명.**

---

## 9. 문헌 검증 (우리 grand-potential이 실험·타 계산과 일치)
| 문헌 | 그들 값 | 우리와 비교 |
|---|---|---|
| Gil-González 2022 (constrained-ESW) | LPSCl1.5 안정창 1.70–2.40 V (K_eff=0) | modelC 1.72/2.14 V와 정합 |
| Gil-González 2022 (실험) | LPSCl1.5 ~1.8–2.5 V, LPSCl1.0(=comp1) ~1.3–2.3 V | onset 2.14 V가 실험 범위 내 |
| Zuo 2023 (CV/ToF-SIMS) | 분해식 Eq(1)/(2) | 우리 onset 분해식 거의 그대로 재현 |
> grand-potential은 **실험 CV 창을 정량 재현.** VBM/UPS 절대값으로는 이 실험 정합을 줄 수 없다.

---

## 10. 논문에 쓸 문장 (EN, 그대로 인용 가능)
> *"Electrochemical (oxidation) stability is evaluated from the grand-potential
> decomposition window (Ong 2008; Mo 2012; Schwietert 2020) — and, experimentally, from
> CV/LSV — rather than from the valence-band maximum (UPS), because band-edge–based windows
> overestimate the thermodynamic decomposition limit of a solid electrolyte by 2–3×; the
> VBM/CBM (UPS/IPES) is reported only for electrode band alignment. Consistent with this,
> LPSCl and the Cl-rich LPSCl1.6 share an identical intrinsic oxidation onset (2.14 V vs
> Li/Li⁺, S²⁻→polysulfide) despite differing band-edge positions, confirming that the
> oxidation limit is set by S²⁻ decomposition chemistry rather than by the single-particle
> band edge."*

---

## 11. References
1. S. P. Ong et al., *Chem. Mater.* **20**, 1798 (2008) — grand-potential 상도(방법 기원).
2. Y. Mo, S. P. Ong, G. Ceder, *Chem. Mater.* **24**, 15 (2012) — LGPS 전기화학창.
3. Y. Zhu, X. He, Y. Mo, *ACS Appl. Mater. Interfaces* **7**, 23685 (2015) — SE 안정성 열역학.
4. Y. Zhu, X. He, Y. Mo, *J. Mater. Chem. A* **4**, 3253 (2016) — 계면 안정성.
5. W. D. Richards et al., *Chem. Mater.* **28**, 266 (2016) — 계면 안정성.
6. T. K. Schwietert et al., *Nat. Mater.* **19**, 428 (2020) — 밴드창 vs 분해창 분리 (**핵심**).
7. O. Borodin et al., *J. Phys. Chem. C* **117**, 8661 (2013) — 분자 산화/HOMO (L1 출처 예).
8. R. Gil-González et al. (2022) — constrained-ESW, LPSCl1.5 창 (우리 값 검증).
9. C. Zuo et al. (2023) — Cl-rich argyrodite CV/ToF-SIMS 분해 (우리 onset 재현).

### Caveat (보고 시 명시)
- 절대 VBM 비교는 정전포텐셜 정렬 미보정이라 **비엄밀**(§4b) — "VBM 차이가 있어도 산화는 동일"의 보조 근거로만.
- grand-potential 창은 0 K·0 Pa·MP(GGA/GGA+U) hull 기준 — 절대 onset은 GGA 한계로 ±0.x V; 단 comp1↔modelC **상대 비교·실험 창 정합은 robust**(§9).
- UPS VBM은 **표면·수직** 측정(§6) — bulk·adiabatic 분해와 구분.
