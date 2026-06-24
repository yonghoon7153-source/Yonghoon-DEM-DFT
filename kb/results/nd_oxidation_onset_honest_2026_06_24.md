# Nd₂O₃ 도핑 — 산화안정성 cost vs SEI passivation 이점 (정직한 정리)

작성 2026-06-24. nd intrinsic ESW staircase(`tools/oxidation/esw_nd_result.txt`)에서 **산화 onset이 2.14→1.92 V로 떨어진** 것을 보고 나온 우려에 대한 정직한 분석. 결론: **숨기면 안 되는 진짜 cost가 맞지만, 보이는 것만큼 나쁘지 않다.** 데이터: `db/properties/oxidation_stability.json`(comp1·modelc·nd_doped), figure `docs/figures/oxidation/decomp_map_3systems.png`.

---

## 0. 한 줄
> **네, intrinsic 산화 onset은 떨어진다(2.14→1.92 V) — 정직한 cost.** 그러나 (1) 1.92 V는 *trace* Nd-황화물일 뿐 **bulk sulfide 산화는 오히려 2.30 V로 더 늦고**, (2) intrinsic 창 ≠ 실제 안정성(셋 다 OCV서 metastable), (3) 이점은 원래 "넓은 창"이 아니라 **wide-gap passivation 산물**, (4) 실제 cathode는 코팅 + **실험이 cycle 개선으로 검증**. → 논문은 "산화안정성 개선"으로 팔지 말고 **전자차단 interphase + cathode passivation**으로 팔 것.

---

## 1. ★ 핵심: 1.92 V는 trace Nd-S, bulk sulfide는 오히려 더 늦게 산화

**분해 양(방출 Li, evolution)**까지 보면 그림이 뒤집힌다:

| | modelc | nd |
|---|---|---|
| **formal 산화 onset** | 2.14 V | **1.92 V** — `0.02 Nd₁₀S₁₉ + 0.16 Li`만 (trace) |
| (다음) | — | 2.00 V: `0.2 NdS₂ + 0.20 Li` (여전히 trace) |
| **bulk 폴리설파이드 산화 (LiS₄, 0.7 Li 방출)** | **2.14 V** | **2.30 V** ← +0.16 V 늦음 |

- nd의 1.92~2.30 V 구간은 **미량 Nd-황화물(누적 ≤0.2 Li)**만 산화. 진짜 골격 산화 **S²⁻→폴리설파이드(0.7 Li)**는 nd 2.30 V vs modelc 2.14 V.
- **같은 분해 extent(0.7 Li)로 비교하면 nd가 +0.16 V 더 안정.** formal onset만 trace Nd-S가 끌어내린 것 → **sulfide backbone은 안 나빠졌다**(오히려 살짝 늦음).
- ⚠ 단 trace Nd-S 선산화(1.92 V)는 *실재하는* 새 feature. "전혀 문제없다"가 아니라 "**미량이고 bulk는 멀쩡**".

## 2. intrinsic ESW ≠ 실제 안정성

- comp1·modelc·nd **셋 다 OCV(1.72 V)서 이미 metastable**(자가분해 ΔG<0, Li 교환 0) — 열역학적으론 다 분해해야 정상. 실전 안정성은 **kinetic + interphase passivation**.
- grand-potential 창은 **비관적 하한**(sulfide는 실제로 창 밖에서도 사이클됨, kinetic passivation 덕). 0.22 V 열역학 onset 이동을 metastable 계에서 과대해석 금지.
- intrinsic 창: nd **0.40 V**(1.52–1.92) vs modelc 0.90 V(1.24–2.14) — 양끝 다 안쪽으로(환원도 1.24→1.52). **narrower는 사실**, 단 위 1·3·4로 완화.

## 3. 이점은 "넓은 창"이 아니라 "산물"

분해가 *일어날 때* 뭐가 생기나가 핵심:
- **nd**: NdPO₄(5.55)·NdCl₃(4.30)·Li₃PO₄(5.73) = **wide-gap → 전자차단 → self-limiting(분해 멈춤)**
- **modelc**: P₂S₇·LiS₄·S·SCl·PCl₅ = **전도성 → 전자누설 → runaway(분해 가속)**

> **낮은 onset + passivating 산물**이 **높은 onset + 새는 산물**보다 실전에서 낫다. 산화 onset 숫자는 이 논리에 안 걸린다.

## 4. 실제 cathode = 코팅 + 실험 검증

- operating V에서 SE/cathode interface reactivity 셋 다 −0.6~−1.6 eV(코팅 필수), **nd ≈ modelc**(OCV −0.3285 vs −0.3308). intrinsic SE onset은 operative limit 아님.
- **실험: cycle 개선 + σ_e 3.45→2.33 ×10⁻¹⁰ mS/cm**(x=0.02) → 1.92 V가 operative였다면 개선 불가. 실험이 "thermodynamic onset이 한계가 아님"을 증명.
- 1.92 V는 **GGA+U(4f) 불확실성** → 절대값 ±(product identity는 robust, voltage는 soft).

---

## 5. ★ SEI 이점 — cost(창 좁아짐)를 상쇄하는 이득 (음극·양극)

위 "창이 좁아진다"는 cost는 **분해 산물이 wide-gap 전자절연체**라는 이득으로 상쇄된다. **convex hull staircase에서 직접 확정된** 산물(`esw_nd_result.txt`):

| 계면 | 전압 | nd 산물 (staircase) | gap(eV) | modelc 대조 |
|---|---|---|---|---|
| **음극(anode)** | V=0 | **Li₂O** + (Li₃P 0.8 잔존) | **5.24** | Li₃P만(0.70, 전도) |
| **벌크/GB** | 0.69–3.06 V | **Li₃PO₄** 전 구간 지속 | **5.73** | 없음 |
| **양극(cathode)** | 2.45 V | **NdPO₄** 등장 | **5.55** | P₂S₇(전도) |
| | 2.62 V | **NdCl₃** 등장 | **4.30** | LiS₄(전도) |
| | 3.08·3.66 V | **LiNd(PO₃)₄·Nd(PO₃)₃** | wide | SCl·PCl₅(전도) |

**음극향(V→0)**: O-유래 **Li₂O(5.24)**가 Li 금속 계면에서 전도성 **Li₃P(0.70)을 (부분) 대체** + 벌크 **Li₃PO₄(5.73)** → **전자누설·dendrite·self-discharge 억제**(Han 2019). (Nd는 음극서 NdP 전도성 = 무익; 음극 이득은 순수 O 효과.) ※ x=0.2서 O dilute → V=0 산물 `0.3 Li₂O + 0.8 Li₃P`(Li₃P 잔존), 전환은 부분·additive(O량 비례).

**양극향(V≥2.45)**: **Nd³⁺ 생존**(Nd⁴⁺ 불가) → O·Cl을 **wide-gap NdPO₄/NdCl₃/Li₃PO₄**로 고정 = **self-limiting passivation**. modelc의 전도성 폴리설파이드(runaway)와 대조. **이게 Nd의 진짜 niche**(이온전도 아님).

**벌크/GB**: **Li₃PO₄(5.73)**가 전 구간 → 입계 전자 percolation 차단 → **유효 σ_e↓**(실험 DC-pol 3.45→2.33 ×10⁻¹⁰ mS/cm @x=0.02).

> **순(net) 평가**: intrinsic 창 −0.50 V(0.90→0.40) **cost** vs 음극/벌크/양극 **wide-gap 전자차단 passivation 이득**. 산화 onset(열역학)은 "산물이 전도냐 절연이냐"를 못 보지만, 실제 cycle 수명을 가르는 건 후자 → **이득이 우세**(실험 cycle↑로 검증). 상세: `kb/results/nd_anode_cathode_sei_formation_2026_06_24.md`, `db/properties/sei_products.json`.

---

## 6. 논문 framing (정직)

**Nd₂O₃를 "산화안정성 개선"으로 팔지 말 것** (실제로 intrinsic 창은 살짝 나빠짐). 대신:
1. **전자차단 interphase** (O-유래 Li₃PO₄/Li₂O가 σ_e↓ → dendrite/self-discharge 억제) — **메인 셀링포인트**
2. **cathode wide-gap passivation 산물** (Nd³⁺ 생존 → NdPO₄/NdCl₃, modelc 전도성 폴리설파이드와 대조)

**intrinsic 창 narrowing은 disclosed cost로 정직하게**: "(i) 주로 *trace Nd-S* 선산화이고 bulk 폴리설파이드는 2.30 V로 오히려 modelc(2.14)보다 늦으며, (ii) 분해 산물의 wide-gap passivation이 보상한다." → 선제 disclosure가 리뷰어 공격을 방어.

---

## caveat
- 모두 **열역학(0-pressure grand-potential)** — kinetic CEI passivation·mechanical constriction(Fitzhugh K_eff>0이면 창 넓어짐) 미포함.
- Nd 함유 상은 GGA+U(4f) → voltage 절대값 ±, product identity robust.
- GB/계면 morphology·연속 차단막 미계산(추론) → XPS depth·SSRM 검증 필요.

**데이터**: `db/properties/oxidation_stability.json`(nd_doped: onset 1.92/red 1.52/창 0.40) · `tools/oxidation/esw_nd_result.txt`(full staircase) · `docs/figures/oxidation/decomp_map_3systems.png`. **연관**: `kb/results/nd_anode_cathode_sei_formation_2026_06_24.md` §3b, `nd2o3_master_findings_2026_06_18.md` §3, `db/properties/sei_products.json`.
