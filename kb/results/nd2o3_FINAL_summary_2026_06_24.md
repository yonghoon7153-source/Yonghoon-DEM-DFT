# Nd₂O₃-doped LPSCl1.6 — **최종 종합 (FINAL capstone)**

작성 2026-06-24. Nd₂O₃-도핑 Li₅.₄PS₄.₄Cl₁.₆(modelc) 연구의 **단일 종합 문서**. 이 문서 하나로 전체 스토리 파악 + 모든 근거 파일 연결. 상세 허브: `nd2o3_master_findings_2026_06_18.md`.

- **DFT 조성 (main track, Nd→Li)**: **Li₄.₈Nd₀.₂PS₄.₁O₀.₃Cl₁.₆** = Li₄₈Nd₂P₁₀O₃S₄₁Cl₁₆ (120-atom, net charge 0, x=0.20 과도핑).
- **실험**: x=0.02 (Li₅.₃₄Nd₀.₀₂PS₄.₃₇O₀.₀₃Cl₁.₆), σ_e 최저·cycle 개선. **Nd→P(control)는 less stable로 기각**(modelc_nd_doped.json Track 2).
- O speciation (relaxed, 검증): **1×PS₂O₂ + 1×PS₃O + 8×pristine PS₄**, 3 O 중 **2 O가 P–O–Nd 브리지**.

---

## 0. ★ Executive summary (정직판)

> **Nd₂O₃ 도핑의 cycle 개선 = "전자차단 passivation interphase"가 핵심이고 주역은 대체로 O다.** O-유래 **Li₃PO₄(5.73 eV)**가 벌크/GB 전자망을 항시 차단(σ_e↓), **Li 양극엔 Li₂O(5.24)+LiCl(6.65) 차단막**, **cathode 고전압엔 Nd³⁺ 생존→NdPO₄(5.55)·NdCl₃(4.30) wide-gap passivation**(여기서 Nd 기여). **Nd 단독의 전자·결합·이온 이득은 없다**(oxophilicity≈Li, Nd–X 약·이온, 갭 좁힘, 이온 σ↓); Nd는 **O 운반체·cathode 앵커·aliovalent**. **과도핑(x>0.02) 역효과**. **convex hull staircase로 직접 증명됨.**

| 항목 | 한 줄 판정 |
|---|---|
| 구조/host 결합 | **불변(±4%)** — 안전한 도핑 (O만 강한 P–O, Nd 이온) |
| 전자구조(bulk gap) | **좁아짐**(2.184→1.632) = Nd 5d 비용 (O는 deep spectator, 무해) |
| 이온전도 | **0.52× 손해** (큰 immobile Nd³⁺가 Li 경로 막음; Ea 불변=prefactor) |
| 내재 산화창 | **좁아짐**(0.40 vs 0.90 V) = 비용 (단 trace Nd-S, bulk는 오히려 늦음) |
| **SEI passivation** | **★ 이득** (음극 Li₂O·벌크 Li₃PO₄·양극 NdPO₄/NdCl₃ wide-gap 전자차단) |
| 실험 | σ_e 3.45→**2.33**(x0.02 최저)·cycle↑·E 불변(20.3→20.7) |

---

## 1. 구조 & 결합 — host 불변, O가 actor, Nd는 이온

**ICOHP** (동일 PAW 4.0 Å, LOBSTER 5.1.1 → 비교 valid):

| 결합 (eV/bond) | modelc | nd | nd vs modelc |
|---|---|---|---|
| P–S | −6.00 | **−5.976** | +0.4% (불변) |
| Li–Cl / Li–S | −2.10 / −1.72 | −2.13 / −1.65 | ±4% (불변) |
| **P–O** | — | **−8.43** | nd-only, P–S보다 **+41%** (O 효과) |
| Nd–O/S/Cl | — | **−0.42/−0.44/−0.57** | nd-only, **약·이온** |

**ELF** (5번째 독립 probe): P–S 0.870(공유백본 불변) · P–O 0.838(더 강하나 더 polar=O가 전하 당김) · Nd–X floor 0.13–0.19(약 5d 공유+이온) · Li/Cl 0.018–0.032(강이온).
→ **3-probe 수렴(ICOHP·ELF·oxophilicity): host 백본 불변 · O = 강·polar P–O actor · Nd = 이온 spectator.** [상세 §2b-2d master / `nd_icohp.json` / `docs/figures/nd_elf/`]

## 2. 전자구조 — 갭 좁힘은 Nd 5d, O는 deep spectator

eigenvalue gap **undoped 2.184 → Nd+O 1.632 eV (−0.55)**:
- **VBM = S 3p (host 불변)**; CBM을 **Nd 5d/6s가 끌어내림 → 갭 narrowing** (Nd 비용).
- **O 2p deep (~−3.9 eV) = spectator** (gap edge 아님 → 전자구조에 무해).
- **Nd 4f는 gap 밖** (채워진 4f 깊고 빈 4f는 CB 위) → **host는 clean insulator 유지** (순수 Nd 화합물의 4f→metal 실패와 다름).
→ "갭 좁힘 단점은 Nd 몫, O는 무해." [DFT+U U=8; PBE라 절대값 ~1 eV 과소, trend robust / `electronic.json` / `docs/figures/dos_pdos_smooth/`]

## 3. Nd 4f 물리 — Mott-localized spectator

- Nd³⁺ 4f³ = **Mott-Hubbard 절연** (PBE+U로 Nd 화합물 다루면 metal化 → 문헌값 사용). 4f는 5s5p 차폐로 **결합 안 함**(spectator).
- **partial-occupation 규칙**: 닫힌 d¹⁰ OK / 열린 f^n 실패. **NdS₄ 불가**(크기·전하·배위 — MgS₄ critique와 동일 논리).
- Ce⁴⁺(4f⁰, charge-transfer, 전자 소모성) vs **Nd³⁺(4f³, Mott, 전자 차단·영구적)**. [상세 `kb/physics/nd_4f_doping_consolidated_corrected_2026_06_24.md`]

## 4. 이온전도 — 0.52× 손해, Ea 불변(prefactor 효과)

| | modelc | nd | comp1(ref) |
|---|---|---|---|
| Ea (eV) | 0.2235 | **0.2267** | 0.2532 |
| D₆₀₀ (cm²/s) | 7.90e-6 | **4.905e-6** | 3.09e-6 |
| ratio nd/modelc | — | D **0.62×** / σ300 **0.52×** | — |

→ **Ea 사실상 불변(0.227≈0.224), D는 0.62×** = **장벽이 아니라 prefactor(D₀ 0.65× 지배)** 효과. 큰 immobile Nd³⁺+O@PS₄가 Li 경로를 좁힘. **이온전도는 Nd의 손해** (Cu/Br 도핑이 σ↑인 것과 대조 — Nd niche는 이온 아닌 cathode passivation). ⚠ UMA Nd-4f 미검증 → **ratio·Ea 방향**만 인용, 절대 σ 주의. [`li_transport.json` / `docs/figures/slide09_arrhenius/`]

## 5. ★ SEI / 분해 — convex hull staircase로 직접 증명

nd 조성 intrinsic ESW staircase(`esw_nd_result.txt`, 6원소 hull; modelc 같은 hull 재실행=control 완전일치 → 아티팩트 아님):

| 계면 | 전압 | nd 산물 (staircase 확정) | gap | modelc 대조 |
|---|---|---|---|---|
| **음극** | V=0 | **Li₂O** + Li₃P(0.8 잔존) | **5.24** | Li₃P만(0.70 전도) |
| **벌크/GB** | 0.69–3.06 V | **Li₃PO₄** 전 구간 | **5.73** | 없음 |
| **양극** | 2.45 V | **NdPO₄** 등장 | **5.55** | P₂S₇(전도) |
| | 2.62 V | **NdCl₃** 등장 | **4.30** | LiS₄(전도) |
| | 3.08·3.66 V | **LiNd(PO₃)₄·Nd(PO₃)₃** | wide | SCl·PCl₅(전도) |

- **Nd anode-bad/cathode-good split 확정**: 저전압 NdP/Nd₂S₃(전도)·고전압 NdPO₄/NdCl₃(wide-gap).
- **formation이 산물 선택을 구동**: Nd₂O₃ −1808 kJ/mol(O 잠김)·O@PS₄ −0.67 eV·P–O −8.43 → 분해해도 wide-gap O/Nd상으로.
- **분해 양은 비슷**(interface vs LiCoO₂: nd −0.3285 ≈ modelc −0.3308) → 이점은 "덜 분해"가 아니라 **산물이 전자절연**. [상세 `nd_anode_cathode_sei_formation_2026_06_24.md` / `sei_products.json` / `oxidation_stability.json` nd_doped / `docs/figures/oxidation/decomp_map_3systems.png`]

## 6. 산화안정성 — 정직한 cost (그러나 보이는 것만큼 나쁘지 않음)

- intrinsic 산화 onset **2.14→1.92 V 떨어짐**(정직한 cost), 내재창 0.40 V로 좁아짐.
- **그러나 1.92 V는 trace Nd-S(0.16 Li)** — **bulk 폴리설파이드 산화는 2.30 V로 modelc(2.14)보다 오히려 +0.16 V 늦음**(같은 0.7 Li extent).
- intrinsic 창 ≠ 실제 안정성(셋 다 OCV서 metastable); 이점은 산물 passivation; 실제 cathode는 코팅 + **실험 cycle↑로 검증**.
→ **"산화안정성 개선"으로 팔지 말 것.** [상세 `nd_oxidation_onset_honest_2026_06_24.md`]

## 7. 순(net) 평가 — cost ledger

| | 부호 | 내용 |
|---|---|---|
| host 결합·구조 | ○ 중립 | 불변(안전한 도핑) |
| bulk gap | ✗ cost | 좁아짐(Nd 5d) |
| 이온 σ | ✗ cost | 0.52× |
| 내재 산화창 | ✗ cost | 0.90→0.40 V (단 trace Nd-S, bulk는 늦음) |
| **SEI 전자차단 passivation** | **✓ 이득** | 음극 Li₂O·벌크 Li₃PO₄·양극 NdPO₄/NdCl₃ |
| **σ_e (실험)** | **✓ 이득** | 3.45→2.33 ×10⁻¹⁰ mS/cm |

> **net: bulk(gap·이온·창) 비용 vs interphase(전자차단) 이득.** cycle 수명을 가르는 건 후자 → **이득 우세**(실험 검증). 단 **과도핑 시 비용이 이득을 추월**(x=0.02 최적, σ_e 비단조).

## 8. 논문 framing (정직 novelty)

> "Nd₂O₃ 미량 co-doping(x=0.02)이 ASSB cycle 개선. 기전은 **전자차단 passivation interphase**: O-유래 Li₃PO₄(벌크/GB)·Li₂O(양극)가 σ_e를 낮춰 dendrite/self-discharge 억제, cathode 고전압엔 **Nd³⁺가 NdPO₄·NdCl₃ wide-gap passivation** 형성(modelc 전도성 폴리설파이드와 대조, **convex hull로 직접 증명**). Nd는 **O 운반·cathode 앵커·aliovalent** 역할이며 단독 전자/결합/이온 이득 없음. **bulk gap·이온 σ·내재 산화창은 disclosed cost**(주로 Nd 몫, trace Nd-S), passivation이 보상. 과도핑(x>0.02)은 내재창 좁혀 역효과 → x=0.02 최적." (Nd 과대선전 X — 정직.)

## 9. caveats
- **열역학만**: SEI 산물 종류·양은 계산, **연속 차단막(morphology/percolation)은 추론** → XPS depth·ToF-SIMS·SSRM 검증 필요.
- **Nd 함유 상**: GGA+U(4f) → product identity robust, **갭·voltage 절대값 ±**. 순수 O상(Li₃PO₄·Li₂O)은 확정.
- **DFT x=0.2 = 실험 10×**(과도핑) → 경향·기전 robust, 절대값·dilute 외삽 주의.
- **GB σ_e 기전은 추론**(SEI 산물 갭 + bulk-반대방향 논리; GB 전자수송 직접계산 X).
- in-gap states 0.74→0.014(~50×)는 **matched-condition 아님**(셀/k/window 상이) → matched-k Phase 2 필요.

## 10. 실험 검증 필요
- **XPS depth / ToF-SIMS / SSRM**: NdPO₄·NdCl₃·Li₃PO₄가 실제 **연속 차단층**으로 형성되는지.
- σ_e(x) 비단조 재현 + x=0.02 최적 확인.
- (정량) matched-k in-gap states, dilute(x=0.10 248-atom) 외삽 검증.

---

## 11. 데이터 · figure · 문서 인덱스

**핵심 문서**
| 문서 | 내용 |
|---|---|
| `nd2o3_master_findings_2026_06_18.md` | 상세 허브 (§1-8 + 문헌매핑) |
| `nd2o3_O_effect_transfer_2026_06_24.md` | O 효과 중심 (transfer용) |
| `nd_anode_cathode_sei_formation_2026_06_24.md` | 음극/양극 + formation + staircase §3b |
| `nd_oxidation_onset_honest_2026_06_24.md` | 산화 cost vs SEI 이점 |
| `kb/physics/nd_4f_doping_consolidated_corrected_2026_06_24.md` | Nd 4f 물리 |

**데이터 (db/properties)**: `nd_icohp.json`(P–O −8.43) · `electronic.json`(gap 1.632, Nd 5d) · `li_transport.json`(D 0.62×, Ea) · `oxidation_stability.json`(nd_doped staircase) · `sei_products.json`(SEI gap·oxophilicity·formation·interface 통합) · `db/compositions/modelc_nd_doped.json`(조성·O speciation·formation).

**tools**: `tools/oxidation/{esw_grand_potential,sei_product_gaps,oxophilicity_descriptor,interface_reactivity,plot_decomp_map_3systems}.py` · `esw_nd_result.txt`(staircase log).

**figures (docs/figures)**: `oxidation/decomp_map_3systems.png`(3계 분해도) · `nd_sei/sei_product_gaps_O.png`(SEI gap) · `nd_elf/`(ELF) · `dos_pdos_smooth/`·`nd_dos/`(DOS/PDOS) · `slide09_arrhenius/arrhenius_nd_vs_modelc.png` · `icohp/`(COHP).

> **한 줄**: Nd₂O₃ 도핑 = **O가 만드는 전자차단 passivation interphase**(bulk 비용 감수). Nd는 O 운반·cathode 앵커. convex hull·ICOHP·ELF·DOS·MD·SEI staircase가 모두 수렴, cost는 정직하게 disclosed.
