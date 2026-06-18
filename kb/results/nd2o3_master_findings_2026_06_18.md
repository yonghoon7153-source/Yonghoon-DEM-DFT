# Nd₂O₃-LPSCl1.6 — 종합 결과 + 메커니즘 (master findings, 문헌 매핑)

작성 2026-06-18. 대상: Nd₂O₃-doped Li₅.₄PS₄.₄Cl₁.₆ (modelc). 실험 deck(Nd2O3Cl1.6_DFT.pdf) + 우리 DFT 종합.
조성: Li₅.₄₊₂ₓP₁₋ₓNdₓS₄.₄₋₁.₅ₓO₁.₅ₓCl₁.₆ — **실험 최적 x=0.02** (Li₅.₄₄P₀.₉₈Nd₀.₀₂S₄.₃₇O₀.₀₃Cl₁.₆). **DFT는 x=0.2**(과도핑 영역, 효과 증폭용).

---

## 0. 한 줄 결론 (정직판)
> **Nd₂O₃ 도핑의 cycle 개선은 "전자차단 passivation interphase"가 핵심이고, 그 주역은 대체로 O다.** O-유래 **Li₃PO₄(5.73 eV)** 가 벌크/GB 전자망을 항시 차단(σ_e↓)하고, **Li 양극엔 Li₂O+LiCl(O-유래) 차단막**, **cathode 고전압엔 Nd³⁺가 생존해 NdPO₄(5.55)·NdCl₃(4.3) wide-gap passivation**(여기서 Nd가 기여). **Nd 단독의 전자·결합·이온 이득은 없다**(oxophilicity≈Li, Nd–X 약함, 갭 좁힘, 이온↓); Nd는 **O 운반·cathode 앵커 + aliovalent**. **과도핑(x>0.02)은 역효과**.

---

## 1. 실험 사실 (PDF)
| 항목 | 값 | 비고 |
|---|---|---|
| σ_e (DC-pol, ×10⁻¹⁰ mS/cm) | undoped 3.45 → **x0.02 2.33(최저)** → x0.04 3.67 → x0.08 5.32 | **비단조, x=0.02 최적** |
| cycle | 개선 | (PI 보고) |
| Young's modulus (AFM) | 20.3±0.2 → 20.7±0.2 | **오차내, 사실상 불변** |
| adhesion | 356→300 aJ | 감소 |

## 2. DFT 결과 요약
| 물성 | 결과 | 판정 |
|---|---|---|
| 밴드갭 (eigenvalue) | undoped 2.184 → Nd+O(x0.2) 1.632 (−0.55) | **Nd 5d가 CBM↓** (O 2p는 deep spectator). 갭 narrowing은 Nd, 전해질엔 단점 |
| ICOHP (spilling 1.34%) | **P–O −8.43 > P–S −5.98**(host 불변); **Nd–O −0.42 / Nd–S −0.44 / Nd–Cl −0.57**(약·이온) | P–O 공유 강함=**O 효과**; Nd 결합 약함=이온 dopant |
| oxophilicity (MP) | **Nd 1.75 ≈ Li 1.67**; Al 3.45, Y 2.13 | **Nd 특별한 getter 아님** (≈O 운반체) |
| 이온전도 σ | nd 0.52× modelc | Nd(큰 immobile)가 Li 막음 → **손해** |
| 내재 ESW (x0.2 DFT) | nd **1.52–1.92 V** vs modelc 1.24–2.14 | **과도핑이 창 좁힘**(이른 NdP 환원·Nd₁₀S₁₉ 산화) → x=0.02 최적 이유 |

## 3. ★ SEI passivation — anode vs cathode (grand-potential)
| 계면 | wide-gap 차단상 | 전도성(누설) 산물 | Nd 기여 |
|---|---|---|---|
| **Li 양극** (환원, V→0) | **Li₂O(5.24)+LiCl(6.65)** [O-유래] | **Li₃P(0.70)·NdP·Li₂S** | ❌ Nd→NdP(전도성) |
| **벌크/GB** (항시) | **Li₃PO₄(5.73)** [O-유래] | — | ❌ (O 효과) |
| **Cathode** (산화, V≥2.45) | **NdPO₄(5.55)@2.45·NdCl₃(4.30)@2.62·LiNd(PO₃)₄·Li₃PO₄** | P₂S₇·LiS₄(폴리설파이드) | ✅ **Nd³⁺ 생존→NdPO₄/NdCl₃** |
| (대조) modelc cathode | 없음 | P₂S₇·SCl·PCl₅·S | (O·Nd 없음→전도성 폴리설파이드) |

- SEI 산물 갭(MP): LiCl 6.65 · Li₃PO₄ 5.73 · NdPO₄ 5.55* · Li₂O 5.24 · NdOCl 4.77* · NdCl₃ 4.30* · LiNdO₂ 4.21* · Li₂S 3.90 · Nd₂O₃ 3.81* · Nd₂S₃ 1.79* · Li₃P 0.70 · **NdS 0.00(금속)** (*Nd=4f 하한값, 실제 더 넓음)
- interface vs LiCoO₂: nd −0.3285 ≈ modelc −0.3308 (**분해 양은 비슷**, 산물만 wide-gap화).

## 4. 메커니즘 (cycle↑ 인과사슬)
1. **벌크/GB**: O-유래 Li₃PO₄ 등 wide-gap이 전자 percolation 차단 → **σ_e↓**(DC-pol). (bulk 갭은 오히려 좁아짐 → σ_e↓는 interphase/microstructure 효과, **bulk 아님**.)
2. **σ_e↓ → 전자누설·내부 Li⁰ 석출(dendrite)·self-discharge 억제** (Han 2019).
3. **Cathode 고전압**: modelc는 전도성 폴리설파이드로 분해, nd는 **wide-gap passivation(NdPO₄/NdCl₃/Li₃PO₄)** → self-limiting, 전자차단.
4. → **cycle·CE 개선.** (양극계면 반응 "양"은 nd≈modelc → 개선은 분해 "양"이 아니라 산물의 **전자차단성**.)

**caveat**: 1·3은 **추론**(GB 전자수송·계면 미세구조 직접계산 안 함; SEI 산물 갭 + bulk-반대방향 논리 기반). 절대 갭은 4f-U 민감(경향 robust). σ_e(x) 비단조는 [interphase 차단(↓) vs bulk 갭 narrowing(↑)] 경쟁 → x=0.02 최적.

## 5. "passivation 여러 상 = 더 좋은가?" → 자동 아님 (조건부)
- **좋으려면**: 생기는 wide-gap 상(Li₃PO₄·NdPO₄·NdCl₃·Li₂O·LiCl)이 **연속 차단층**을 이루고 **Li⁺는 통과**시켜야 함.
- **나쁜 경우**: 그 중 **전도성 상(Li₃P·NdP·폴리설파이드·Co₉S₈)이 percolate**하면 전자 누설 → passivation 깨짐. 우리 산물엔 **항상 전도성 상이 섞여 있음**(양극 Li₃P/NdP, 산화 LiS₄).
- **여러 상 = 이종(heterogeneous)** → interphase 내부 경계 多 → (a) Li⁺ 빠른길(good) or (b) 전자누설·균열(bad). **이상적 SEI는 균일 단일상**(LiF형)에 가까움.
- **결론**: "여러 개 생김" 자체는 중립. **NET 전자차단(전도상 미연결) + Li⁺ 전도 + 균일·치밀**이어야 좋음. 우리 열역학 계산은 **산물 종류·양**만 주지 **morphology/percolation은 모름** → "wide-gap 상 생긴다"까진 말하되 "연속 차단막"은 **실험(XPS depth·ToF-SIMS·SSRM)** 필요.

## 6. 정직한 노벨티 (논문 프레임)
> "Nd₂O₃ 미량 co-doping(x=0.02)이 ASSB cycle을 개선. 기전은 **전자차단 passivation interphase**: O-유래 Li₃PO₄(벌크/GB)·Li₂O(양극)가 σ_e를 낮춰 dendrite/self-discharge 억제, **cathode 고전압에선 Nd³⁺가 NdPO₄·NdCl₃ wide-gap passivation을 형성**(modelc의 전도성 폴리설파이드와 대조). Nd는 **O 운반·cathode 앵커·aliovalent** 역할이며, 과도핑(x>0.02)은 내재창을 좁혀 역효과 → x=0.02 최적." (Nd 단독 전자/결합/이온 이득 주장 X — 정직.)

## 7. 검증 필요 (실험)
- **XPS depth / ToF-SIMS / SSRM**: SEI에 NdPO₄·NdCl₃·Li₃PO₄가 실제로, **연속 차단층**으로 형성되는지 (열역학은 형성가능성만).
- σ_e(x) 비단조 재현 + x=0.02 최적 확인.

## 8. 참고문헌 (claim ↔ 문헌)
- **Han et al., Nat. Energy 2019** — 전자전도도↑ → SE 내부 Li⁰ 석출/dendrite (cycle↓ 기전).
- **Electrochimica Acta 535 (2025) 146619** — La-doped LPSC: **LaCl₃/LiCl SEI**로 dendrite 억제 (Nd 직접 유사사례; La=Nd의 4f⁰ analog).
- **Nano Energy 142 (2025) 111176** — Li/SE 계면 분해 AIMD + 단위별 분해 ΔG·COHP (page-3 template).
- **Chem. Eng. J. 507 (2025) 160455** — 계면에너지 + SEI 산물 band gap / Li⁺ barrier.
- **Energy Storage Mater. 76 (2025) 104125** — MgO 도핑: ELF·sp hybridization·결합.
- **Ong 2008 / Mo–Ceder 2012 / Schwietert 2020** — grand-potential 분해창 (산화안정성 방법).
- refs.json: **NdF₃(7.69)/BaF₂(6.59) wide-gap 자기제한 SEI** — 전자차단 passivation 논거 전이.
- (우리) `db/properties/{nd_icohp, oxophilicity, electronic}.json`, `tools/oxidation/{esw_grand_potential, interface_reactivity, sei_product_gaps, oxophilicity_descriptor}.py`.

### caveat 총괄
- DFT x=0.2 (실험 x=0.02의 10×, 과도핑) → 효과 증폭/내재창 narrowing은 과대; **방향·메커니즘 robust, 절대값 주의**.
- Nd-함유 갭은 4f 때문에 MP 하한 (실제 더 넓음).
- 계면 morphology/percolation·GB 전자수송 = **미계산(추론)** → 실험 필수.
