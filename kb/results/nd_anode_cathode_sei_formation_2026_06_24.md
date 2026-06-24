# 음극향·양극향 SEI 이점 — **formation energy로 본 산물 선택** (Nd₂O₃-LPSCl1.6)

작성 2026-06-24. SEI 산물 band gap(MP)을 **이미 계산한 formation/안정성 에너지**와 엮어 **음극(anode)·양극(cathode)** 각각의 이점을 정리.
- 전체 anode/cathode passivation 표·기전: `kb/results/nd2o3_master_findings_2026_06_18.md` §3·§4 — **여기선 중복하지 않고 formation-energy 연결만 추가.**
- O 중심 정리: `nd2o3_O_effect_transfer_2026_06_24.md`. 데이터 store: `db/properties/sei_products.json`(新).

---

## 0. 핵심 논리 한 줄
> **분해 "양"은 도핑해도 비슷(interface ΔE_rxn nd −0.3285 ≈ modelc −0.3308 eV/atom)**. 바뀌는 건 **산물 종류** — formation energy가 **wide-gap O/Nd 상(Li₃PO₄·Li₂O·NdPO₄·NdCl₃)을 선택**하게 만들어 **전자차단 SEI**가 되는 것. 즉 **이점 = "덜 분해"가 아니라 "분해 산물이 절연체"**.

| 질문 | 답 | 근거(이미 계산) |
|---|---|---|
| 얼마나 분해되나? (양) | nd ≈ modelc (거의 동일) | interface ΔE_rxn −0.3285 vs −0.3308 |
| **무엇으로** 분해되나? (종류) | **wide-gap O/Nd 상** | formation energy + SEI gap(MP) |
| 그래서 좋은 이유? | 산물이 **전자절연 → self-limiting** | SEI gap ≥4 eV |

---

## 1. formation energy가 "왜 O/Nd 상이 생기나"를 설명 (산물 선택)

세 개의 **이미 계산한** 에너지가 모두 **"O는 산화물/인산염으로 박혀 나온다"**로 수렴:

1. **Nd₂O₃ 생성에너지 −1808 kJ/mol** (란타나이드 산화물 중 최강 안정군). → O는 **oxide/phosphate로 thermodynamically 잠김**(방출 안 됨). Nd–O ≫ Nd–S (Nd₂S₃ 덜 안정). [`modelc_nd_doped.json`]
2. **O@PS₄ vs free-site −0.67 eV/O** : O가 free 4d 자리보다 **PS₄ 코너 S를 치환**해 **phosphate형(PS₃O·PS₂O₂)** 으로 앉는 게 0.67 eV 더 안정 (500 K AIMD서 P–O 자발형성). → **wide-gap Li₃PO₄ 전구체를 host 안에서 미리 만듦**. [`modelc_nd_doped.json`]
3. **ICOHP P–O −8.43 eV/bond** (P–S −5.98 대비 +41%) : O는 **결합으로도 잠김** → 인산염 유지 강화. [`nd_icohp.json`]

> ⇒ 분해가 일어나면 O는 **반드시 Li₃PO₄(5.73)/Li₂O(5.24)/NdPO₄(5.55)** 같은 **wide-gap 상**으로 간다(전도성 Li₃P/폴리설파이드가 아니라). **formation energy = "절연 산물 선택"의 구동력.**

---

## 2. 음극향 (anode, 환원 V→0) — **O 효과**

| | 도핑 전(modelc) | 도핑 후(Nd₂O₃) | gap(eV) |
|---|---|---|---|
| 주 산물 | **Li₃P 0.70 (전도→누설)** | **Li₂O 5.24 · LiCl 6.65 (절연)** + 벌크/GB **Li₃PO₄ 5.73** | — |
| 전자 | 누설(internal short 위험) | **차단(self-limiting)** | — |

- **이점**: O-유래 **Li₂O(5.24)**가 Li 금속 계면에서 **전도성 Li₃P(0.70)을 대체** → 전자누설·내부 Li⁰ 석출(dendrite)·self-discharge 억제 (Han 2019, Nat. Energy). 벌크/GB의 **Li₃PO₄(5.73)**는 grain 간 전자 percolation을 끊어 **유효 σ_e↓** (실험 DC-pol 3.45→2.33 ×10⁻¹⁰ mS/cm @x=0.02).
- **formation 연결**: §1의 O-locking이 **음극 환원 환경에서도** Li₂O/Li₃PO₄ 형성을 보장 (O가 환원돼 빠져나오지 않음 — −1808 kJ/mol).
- **Nd는 음극에서 무익**: Nd³⁺가 환원돼 **전도성 NdP**가 됨 → 음극 이점은 **순수 O 효과**(Li₂O·Li₃PO₄), Nd 아님.

---

## 3. 양극향 (cathode, 산화 V≥2.45) — **Nd³⁺ 앵커 + O**

| | modelc (O·Nd 없음) | Nd₂O₃-도핑 | gap(eV) |
|---|---|---|---|
| 주 산물 | **P₂S₇·SCl·PCl₅·S·LiS₄ 폴리설파이드 (전도)** | **NdPO₄ 5.55(@~2.45V) · NdCl₃ 4.30(@~2.62V) · Li₃PO₄ 5.73** | — |
| 전자 | 누설 | **wide-gap passivation** | — |

- **이점**: 산화 전위에서 **Nd³⁺ 생존(Nd⁴⁺ 접근불가)** → O·Cl을 **wide-gap NdPO₄/NdCl₃/Li₃PO₄** 형태로 고정. modelc의 **전도성 폴리설파이드**와 대조 → self-limiting CEI.
- **formation 연결**: Nd–O 강안정성(§1-1)·P–O 강결합(§1-3)이 **고전압서도 산화물/인산염을 유지** → 폴리설파이드로 무너지지 않음. **이게 Nd의 진짜 niche**(이온전도 아님 — 이온 σ는 오히려↓).
- **분해 양은 비슷**: voltage-resolved interface(v2)에서도 Cl-rich가 thermodynamic으론 **덜** 반응 → 양극 이점은 "**덜 분해**"가 아니라 **산물의 전자차단성**(§0). [`interface_reactivity_v2_voltage_resolved_2026_06_21.md`]

---

## 3b. ★ 직접 convex hull staircase로 검증됨 (2026-06-24) — 추론 → 증명

nd 조성 자체의 intrinsic ESW staircase를 돌려서(`tools/oxidation/esw_nd_result.txt`, 6원소 hull) **위 음극/양극 스토리를 직접 확인**. modelc를 같은 hull에서 재실행 → 4원소 hull과 breakpoint 완전일치 = **차이는 hull 아티팩트 아니라 진짜 O/Nd 화학**.

| 전압 | nd 산물 (convex hull) | gap |
|---|---|---|
| **0.00 V (음극)** | **0.3 Li₂O** + 0.8 Li₃P + 4.1 Li₂S + 0.2 NdP + 1.6 LiCl | Li₂O **5.24** ✓ |
| 0.69~3.06 V (벌크) | **0.075 Li₃PO₄** 지속 | **5.73** ✓ |
| **2.45 V (양극)** | **0.075 NdPO₄** + 0.4 P₂S₇ + 0.125 NdPS₄ + 1.6 LiCl | NdPO₄ **5.55** ✓ |
| **2.62 V** | NdPO₄ + **0.125 NdCl₃** + P₂S₇ + LiCl | NdCl₃ **4.30** ✓ |
| 3.08·3.66 V | **LiNd(PO₃)₄·Nd(PO₃)₃** + P₂S₇ + SCl | wide-gap phosphate |
| (대조) modelc | P₂S₇·LiS₄·S·SCl·PCl₅ **전부 전도** | — |

**확인**: O→Li₂O(음극)·Li₃PO₄(벌크)·NdPO₄@2.45·NdCl₃@2.62(양극) 전부 식에서 직접 나옴. Nd는 저전압서 NdP/Nd₂S₃(전도)·고전압서 NdPO₄/NdCl₃(wide-gap) = **음극-나쁨/양극-좋음 split 그대로**.

**🔧 수정/정직 (이번 run에서 새로):**
1. **nd intrinsic window는 오히려 좁아짐**: nd 0.40 V(1.52–1.92) < modelc 0.90 V(1.24–2.14). Nd-S/P/O redox가 modelc 창 *안에서* 일어남 → nd가 열역학적으론 **덜 안정**. 이점은 **산물 전자차단(kinetic passivation)**이지 넓은 창이 아님 (= bulk gap 좁아짐과 같은 논리).
2. **x=0.2서 O는 Li₃P를 다 못 바꿈**: V=0서 0.3 Li₂O + **0.8 Li₃P**(여전히 우세). wide-gap화는 **부분·additive**, O량에 비례 (GB/계면 percolation 차단 효과지 bulk 치환 아님). → "Li₂O가 Li₃P 대체" 표현은 "부분 전환"으로 완화.
3. **폴리설파이드는 안 사라짐**: nd도 P₂S₇/SCl/PCl₅ 생김 + NdPO₄/NdCl₃/Li₃PO₄가 **곁들여** 생기는 것. NdPO₄는 2.45 V부터 → passivation은 **≥2.45 V(양극 작동영역)** 효과 (1.92–2.45 V는 Nd-sulfide로 산화).

## 4. caveat
- 산물 **종류·양**(열역학)은 계산했으나 **연속 차단막 여부(morphology/percolation)는 미계산** → XPS depth·ToF-SIMS·SSRM 필요.
- Nd 함유 gap은 MP 4f 하한(실제 더 넓음); **순수 O상(Li₃PO₄·Li₂O)은 확정** → O 메시지는 robust.
- interface ΔE_rxn = LiCoO₂ proxy·열역학(kinetic CEI 미포함); DFT x=0.2(실험 10×) → 경향 robust, 절대값 주의.

**데이터**: `db/properties/sei_products.json`(SEI gap·oxophilicity·interface·formation 통합) · `oxidation_stability.json` · `nd_icohp.json` · `modelc_nd_doped.json`. **figure/CSV**: `docs/figures/nd_sei/sei_product_gaps.csv`·`sei_product_gaps_O.png`.
