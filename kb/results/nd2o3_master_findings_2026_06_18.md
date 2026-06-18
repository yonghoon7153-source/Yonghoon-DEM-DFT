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
| ICOHP (spilling 1.34%) | host 결합 comp1/modelc 대비 **전부 ±4% 불변**(§2b); 새 결합 **P–O −8.43**(O); Nd–X **−0.4~−0.6**(약·이온) | host 손 안 댐; O가 강한 P–O; Nd 이온 spectator |
| oxophilicity (MP) | **Nd 1.75 ≈ Li 1.67**; Al 3.45, Y 2.13 | **Nd 특별한 getter 아님** (≈O 운반체) |
| 이온전도 σ | nd 0.52× modelc | Nd(큰 immobile)가 Li 막음 → **손해** |
| 내재 ESW (x0.2 DFT) | nd **1.52–1.92 V** vs modelc 1.24–2.14 | **과도핑이 창 좁힘**(이른 NdP 환원·Nd₁₀S₁₉ 산화) → x=0.02 최적 이유 |

## 2b. ICOHP 정량 비교 (corrected) — comp1 vs modelc vs nd
전부 **동일 PAW kjpaw_psl 1.0.0, 4.0 Å cutoff, LOBSTER 5.1.1** (basis 동일 → 비교 valid).
| 결합 (eV/bond) | comp1 | modelc | **nd** | **nd vs modelc** |
|---|---|---|---|---|
| P–S | −5.944 | −6.00 | **−5.976** | **+0.4% (불변)** |
| Li–Cl | −1.855 | −2.103 | **−2.132** | **−1.4% (불변)** |
| Li–S | −1.592 | −1.717 | **−1.647** | **+4.1% (≈불변)** |
| S–S | −0.107 | −0.11 | −0.101 | ~0 (둘 다 비결합) |
| **P–O** | — | — | **−8.43** | nd-only (P–S보다 41%↑, **O 효과**) |
| Nd–O / Nd–S / Nd–Cl | — | — | **−0.42 / −0.44 / −0.57** | nd-only (**약·이온**) |

> **결론: Nd₂O₃ 도핑은 host 결합망을 거의 안 바꾼다(±4%) — 구조적으로 안전한 도핑.** 유일한 강결합은 P–O(O), Nd는 이온 spectator. **(참고: comp1→modelc Li–Cl/Li–S +13/+8%는 Cl-rich 효과[FULL report]; 거기 Nd를 더해도 결합은 더 안 변함.)**
> ⚠️ **정정**: 직전 보고의 nd Li–S −2.49(+45%)·Li–Cl −2.27는 **cutoff 아티팩트**(3.2/3.4 Å). 4.0 Å(=comp1/modelc 동일)로 재파싱한 위 값이 정답. db `nd_icohp.json` + `docs/figures/nd_elf/icohp_nd_vs_modelc_comp1.csv` 갱신됨.

## 2c. ELF — 결합 character (ICOHP 교차검증, "5번째 probe")
nd ELF (nd_ELF.cube, pp.x plot_num=8; 공유=midpoint↑ 클수록 공유, 이온=depletion floor↓ 낮을수록 이온):
| bond | ICOHP (세기) | ELF | character |
|---|---|---|---|
| P–S | −5.98 | midpoint **0.870** | 강한 공유 백본 |
| P–O | −8.43 (더 강) | midpoint **0.838 (더 낮음 = 더 polar)** | **강하지만 polar 공유** |
| Nd–O / Nd–S | −0.42 / −0.44 | floor **0.131 / 0.188** | 약한 공유(5d)·대부분 이온 |
| Li–O / Li–S / Li–Cl | 약·이온 | floor **0.032 / 0.024 / 0.018** (매우 낮음) | 강한 이온 |

- **P–O는 ICOHP로 더 강(−8.43)인데 ELF midpoint는 더 낮음(0.838<0.870)=더 polar** → O 전기음성도가 전하를 당겨 **"강하지만 이온성 섞인 공유"** (ICOHP·ELF 교차검증, 단일 probe로는 못 보는 것).
- **Nd–X floor 0.13–0.19 = 순수이온 Li(0.02)보다 높고 공유 P–S(0.87)보다 훨씬 낮음** → **Nd 5d가 약간의 공유성** 부여, 본질은 이온 (앞 "Nd 5d extended → 약한 overlap" 논의와 정합).
- comp1/modelc ELF(별도 계산): **P–S bridge 0.946/0.944 불변 · Li basin 0.072/0.065 강이온** → host 공유백본 불변(§2b ICOHP P–S 불변과 일치).
- ⚠️ nd ELF(0.870)와 comp1/modelc ELF(0.946)는 **다른 ELF 계산(cube grid/sampling 상이)이라 절대값 직접비교 X**; 둘 다 "공유백본 intact"라는 동일 물리만 공유.

> **ELF = 5번째 독립 probe**(ICOHP 세기·Bader 전하·결합길이·BVSE와 함께): **host 공유백본 불변 + O는 강·polar P–O + Nd 약·이온(5d 약간) + Li 강이온** — 한 그림으로 수렴.

## 2d. Nd 결합 효과 = 없음 (3-probe 수렴)
| probe | Nd 판정 |
|---|---|
| **ELF** | Nd–X floor **0.13–0.19** (Li 순수이온 0.02보다↑, 공유 P–S 0.87보다↓↓) = 약한 5d 공유·대부분 이온 |
| **ICOHP** | Nd–X **−0.4~−0.6** (P–S −6.0 대비 미미) |
| **oxophilicity** | Nd **≈ Li** (특별 getter 아님) |
> **세 독립 probe 전부 "Nd는 결합적으로 거의 무익한 이온 dopant"** 로 수렴. 5d가 완전 spectator는 아니나(floor가 Li의 5~10배) 구조·물성엔 무의미. **결합 actor = O (P–O −8.43), Nd = 이온 carrier.**

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

## 4b. 분리막(separator)으로 갔을 때 성능이 좋아진 이유
실험은 Nd₂O₃-LPSCl1.6을 **벌크 분리막**으로 썼고 σ_e↓·cycle↑. **벌크 결정이 좋아져서가 아님**:
1. **벌크 결정 자체는 나빠짐** (DFT): 갭 좁아짐(→grain 내부 전자전도 ↑ 방향), 이온 σ↓.
2. **그런데 측정 σ_e(DC-pol)는 유효/총(percolation)** — grain 내부+입계(GB)+interphase 직렬.
3. **O-유래 wide-gap 상(Li₃PO₄ 5.73·NdPO₄ 5.55)이 입계(GB)에 생겨 grain 간 전자 percolation을 끊음** → 유효 σ_e↓ (전자가 grain은 통해도 GB에서 막힘). + Li 양극 SEI(Li₂O·LiCl) 차단.
4. **σ_e↓ → dendrite(내부 Li⁰ 석출)·self-discharge 억제 (Han 2019) → cycle↑.**
> **핵심: 분리막 개선 = "결정"이 아니라 "입계/계면 전자차단(microstructure)" 효과.** 이온 σ↓는 비용(x=0.02 묽어서 감당). **GB 기전은 추론**(SEI/GB 산물 wide-gap + bulk-반대방향 논리; GB 전자수송 직접계산 X) → SSRM·XPS depth로 검증 필요.

## 4c. 배치 전략 (separator vs catholyte) — DFT 권고
| 용도 | 작동 기전 | 비용 | DFT 평가 |
|---|---|---|---|
| **분리막** | 입계 O-phosphate 전자차단 → dendrite↓ | 이온 σ↓(x=0.02서 감당) | 작동함(실험 검증). 단 이득은 GB, 결정 아님 |
| **catholyte / cathode 코팅** | 고전압서 NdPO₄·NdCl₃·Li₃PO₄ wide-gap passivation | 이온 손실 덜 치명(경로 짧음) | **강점 극대화**(cathode passivation) |
> Nd₂O₃의 **결정·이온·갭 페널티는 분리막에서 더 부담**, **고전압 passivation 강점은 cathode에서 극대화** → **catholyte/cathode 쪽이 DFT상 합리적**. 단 분리막도 GB 차단으로 작동(실험). 과도핑(x>0.02)은 어디서든 역효과.

## 4d. SEI 산물 band gap = 전자차단(분해억제)
- SEI/분해산물이 wide-gap(LiCl 6.65·Li₃PO₄ 5.73·NdPO₄ 5.55·Li₂O 5.24)이면 **전자차단 → 분해 self-limiting → cycle↑** (§3·§4). **Li et al., ESM 77 (2025) 104221**(CuBr₂ argyrodite)도 동일: *"LiBr/LiCl gap > Li₂S(PDOS) → blocks the electronic pathway → prevents further decomposition."* (refs.json NdF₃ 7.69 / BaF₂ 6.59 self-limiting SEI와도 동일.)
- ※ **이건 "분해 억제(전자차단)" 용법**이지 **"oxidation stability"가 아님.** "bulk band gap ≠ 산화안정성 / band gap·VBM을 산화 onset으로 읽으면 안 됨"의 **방법론 구분은 별도 산화안정성 문서**(`kb/results/oxidation_stability_VBM_vs_grandpotential_report_2026_06_18.md` §band-gap 두 용법)로 분리 — 이 Nd 문서엔 안 넣음.

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
- **Li et al., Energy Storage Mater. 77 (2025) 104221** (DOI 10.1016/j.ensm.2025.104221) — **CuBr₂-도핑 argyrodite**(Li₅.₈P₀.₉Cu₀.₁S₄.₅Cl₁.₃Br₀.₂, "LPSC-CB"). **우리와 같은 저널·같은 metal-halide-doping 접근.** 우리 logic 3개를 직접 뒷받침:
  - **(B) band gap→분해억제**: LiBr/LiCl gap > Li₂S(PDOS) → "blocks electronic pathway → prevents further decomposition" (≠ oxidation stability) — 우리 §4d·SEI passivation과 동일.
  - **host 불변**: CuBr₂ 도핑이 "minimal effects on the electron distribution of P (P p-bands 유사, P/S 공유결합 보존)" — 우리 ICOHP P–S 불변·ELF 공유백본 intact·PDOS P-성분 불변을 corroborate.
  - **HSAB cation 도핑**(soft acid Cu) — 우리 Nd³⁺(hard) HSAB 논리와 같은 틀.
  - ⚠️ **대조(중요)**: 그들 Cu+Br는 **이온 σ 10.3 mS/cm로 향상**(Br anion-disorder + soft-acid Cu가 S²⁻ 전하밀도↓→Li 장벽↓). 우리 **Nd₂O₃는 이온 σ↓**(큰 hard Nd³⁺가 Li 막음). → **같은 metal-halide 도핑이라도 양이온 선택이 이온전도를 가른다**(Cu/Br=이온 친화, Nd=이온 손해). Nd의 niche는 이온이 아니라 cathode passivation.
- **Ong 2008 / Mo–Ceder 2012 / Schwietert 2020** — grand-potential 분해창 (산화안정성 방법).
- refs.json: **NdF₃(7.69)/BaF₂(6.59) wide-gap 자기제한 SEI** — 전자차단 passivation 논거 전이.
- (우리) `db/properties/{nd_icohp, oxophilicity, electronic}.json`, `tools/oxidation/{esw_grand_potential, interface_reactivity, sei_product_gaps, oxophilicity_descriptor}.py`.

### caveat 총괄
- DFT x=0.2 (실험 x=0.02의 10×, 과도핑) → 효과 증폭/내재창 narrowing은 과대; **방향·메커니즘 robust, 절대값 주의**.
- Nd-함유 갭은 4f 때문에 MP 하한 (실제 더 넓음).
- 계면 morphology/percolation·GB 전자수송 = **미계산(추론)** → 실험 필수.
