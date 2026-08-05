# 📋 §3 리뷰 코멘트 후보 — 소거법 작업용 (ECER-D-26-00097)

> **용도**: 1저자에게 보낼 **§3 (Intrinsic Stability) 리뷰 코멘트**를 소거법으로 고르기 위한 작업 문서.
> 김동석(§2)·배영진(§4)의 제출 형식과 톤을 맞춤 — 각 후보는 **영어 Comment 초안(제출 후보)** + **한국어 근거(왜 넣나/뺄까)**로 병기.
> §3 담당 = 나(배영진 = §4, 김동석 = §2 → §3은 이 문서가 채운다).
>
> **판정 열 표기**
> - 🟩 **STRONG** — 사실/정의 오류 또는 절 간 모순. 넣으면 확실히 반영됨. **우선 채택 후보.**
> - 🟨 **MEDIUM** — 정량 부재·근거 조건 미기재. 배영진 스타일(개선 제안)로 무난. 묶어서 처리 가능.
> - 🟦 **WEAK/HOLD** — 우리 해석에 의존하거나 §3 범위 밖. **소거 1순위.**
> - 🔗 **MERGE** — 다른 후보와 묶어 하나로.
>
> **대조 원칙** — 리뷰 노트(`_ECERD2600097_review_notes.md`)의 A-번호가 근거 원장이다. 여기서는 그 A-번호를
> **제출 코멘트 단위로 재편성**만 한다. 노트에 없던 신규는 ✚ 표시.
>
> ⚠ **미출판 심사 원고** — 인용문 원문 그대로 옮기지 않는다. 우리 db 수치는 절대값으로 넣지 않고 "정성 지목에 정량 대응물 보유"까지만.

---

## 🎯 소거 전 요약표 — 한눈에 보고 지울 것 고르기

| # | 절 | 한 줄 | 급 | 노트 근거 | 제출? |
|---|---|---|---|---|---|
| C1 | §3.1 | S²⁻ soft-base를 **kinetic barrier 저하**로 서술 (HSAB는 열역학 틀) | 🟩 | A2·A4 | ☐ |
| C2 | §3.1 | **polar ↔ polarizable** 혼동 (같은 절에서 두 용어 반대로) | 🟩 | A3 | ☐ |
| C3 | §3.1 | *"moisture **and** oxygen"* 병렬 — H₂O 가수분해가 지배적 | 🟨 | A1 | ☐ |
| C4 | §3.1 | HSEH(Mulks) **① et al. 오기 ② 고체 미적용 유비** | 🟩 | A5·A10·A11 | ☐ |
| C5 | §3.1/3.3 | *"bond energy"*를 핵심 변수로 반복하나 **정의·측정법 부재** | 🟩 | A18 | ☐ |
| C6 | §3.2 | **P⁵⁺ = soft acid** — §3.1(hard 전제)과 HSAB 내 양립 불가 | 🟩 | A7·A9 | ☐ |
| C7 | §3.2 | InF₃ *"lattice bond energy↑/polarizability↓"* — **인과 역인용** | 🟩 | A12·A13 | ☐ |
| C8 | §3.2 | *"irreversibly reacts"*의 근거(열역학/동역학) 미기재 | 🟦 | A8 | ☐ |
| C9 | §3.3 | *"continuous ... network"* — LPSCl은 **고립 PS₄³⁻**, §3.1과 충돌 | 🟩 | A14 | ☐ |
| C10 | §3.3 | **불활성 400–500 °C**를 셀 안전성 우위로 오독 | 🟩 | A15·A23 | ☐ |
| C11 | §3.3 | O 도입(oxysulfide) **σ 대가 미기재** — 저자도 outlook서 인지 | 🟨 | A19·A22 | ☐ |
| C12 | §3.3 | LiNbO₃/Al₂O₃ 코팅 **두 기전(O완충 vs 물리차단) 뭉갬** | 🟨 | A20 | ☐ |
| C13 | §3.4 | *"**true** thermodynamic window"* — 계산도 규약 의존 | 🟩 | A26·A27 | ☐ |
| C14 | §3.4 | 인용 창(1.7–2.1 V) **방법·hull규약·배열 조건 미기재** | 🟨 | A28·A33 | ☐ |
| C15 | §3.4 | 계면 3분류 — **판별 기준·기계축·정적성** 결여 | 🟩 | A29·A30·A31 | ☐ |
| C16 | §3.4 | *"chemical potential gradient가 구동력↓"* — 열역학상 부정확 | 🟩 | A34·A35 | ☐ |
| C17 | §3.4↔5 | 덴드라이트 **두 기전**(전자경로 vs wedge) 연결 없음 + SE 고유 σ_e 누락 | 🟩 | A37·A39 | ☐ |
| C18 | §3.4 | *"low electronic conductivity"* **문턱값 부재** | 🟨 | A38 | 🔗C15 |
| C19 | §3.4 | *"far exceeds"*에 **두 전압값** 없음 + kinetic 서술과 내부 충돌 | 🟨 | A32·A33 | ☐ |
| C20 | §3.5 | *"몰부피가 base와 크게 다르다"* — **정규화 기준·부호 미정** | 🟩 | A41·A42 | ☐ |
| C21 | §3.5 | *"fracture toughness"*를 **탄성량으로 지지** (급 다름) | 🟩 | A40 | ☐ |
| C22 | §3.5 | *"변형에너지 > 파괴인성"* — **차원 불일치** (J vs Pa·m^½) | 🟩 | A53 | ☐ |
| C23 | §3.5 | 환원 산물에 **LiCl 누락** (아지로다이트 표준: Li₃P+Li₂S+LiCl) | 🟩 | A43 | ☐ |
| C24 | §3.5 | *"빈 균열 = 저임피던스 경로"* — **인과 역전** (Li 채운 뒤 성질) | 🟩 | A56·A57 | ☐ |
| C25 | §3.5 | 같은 계면상에 **전자(§3.4)·기계(§3.5) 두 요구** 동시, 명시 안 됨 | 🟩 | A44·A29 | ☐ |
| C26 | §3.5 | 입자미세화(<1 μm)가 **§3.1·3.2 최적크기와 충돌** ✚ | 🟨 | B1 확장 | ☐ |
| C27 | §3.5 | 임계크기 **~3 μm(본문) vs <1 μm(대응)** 내부 수치 불일치 ✚ | 🟨 | (신규) | ☐ |
| C28 | §3.5 | stack pressure **양날**(접촉↑ vs 과압 균열) — 대응서만 인정 ✚ | 🟨 | A46 확장 | ☐ |
| C29 | §3.1~3.5 | outlook이 **소망 목록** — 도달점/간극 미구분 (묶음) | 🟨 | A6·A24 | ☐ |
| C30 | §3.1~3.5 | **축 상충 매트릭스** 부재 — 결합특성이 절마다 다른 부호로 (B1) | 🟩 | B1 | ☐ |
| C31 | §3.3~3.5 | 정량 부재 반복(*significantly*·*far*·수치조건) — 묶음 (B4) | 🟨 | A15·A21·A33·A36 | ☐ |
| C32 | §3.5 | 화학–역학 **되먹임 고리 모식도 1장** 제안 (부가가치 최대) | 🟩 | A59·B6 | ☐ |

**초안 권고 (소거 시작점)**:
- **채택 유력(🟩 10~12개)**: C6, C9, C10, C13, C15, C16, C20/C22(묶음), C23, C24, C30, C32
- **묶어서 1개로**: C18→C15, C31이 C3·C11·C14·C31 흡수, C22+C20+C21 = §3.5 물성 정의 한 덩어리
- **소거 1순위(🟦)**: C8(근거요구 약함), C26·C28(우리 해석 의존도 높음 → 남기려면 순화)

---

## §3.1 Air Stability

### C1 🟩 — HSAB를 kinetic으로 서술 (A2·A4)
**English (draft)**
> Section 3.1 attributes the hydrolysis susceptibility of the soft-base S²⁻ to a *lowered kinetic barrier*. HSAB reasoning, however, describes a thermodynamic preference (the hard-acid P⁵⁺ favoring the hard base O²⁻ over S²⁻), which is distinct from the reaction rate. The actual hydrolysis kinetics depend on surface area, crystallinity (amorphous > crystalline), and composition. The manuscript repeats this thermodynamic/kinetic conflation in the summary sentence ("thermodynamic **and** kinetic susceptibility"), so the point is best raised at the section level: the two axes should be separated throughout §3.1, and the HSAB argument framed as thermodynamic.

**근거(KR)**: HSAB는 두 중심의 짝짓기 선호 = 열역학. "kinetic barrier를 낮춘다"로 옮기면 축이 어긋남. A2가 문장, A4가 요약문 재발 → **개별 문장이 아니라 절 전체 "두 축 분리" 요구로 승급.** 인용할 때 우리 표현은 "S²⁻의 soft-base 특성이 가수분해를 **열역학적으로** 유리하게 만든다"까지만.
**소거 판단**: 채택. 단 C2(polar/polarizable)와 성격이 겹쳐 **한 코멘트로 묶어도 됨**("§3.1의 화학 서술 두 곳 정밀화").

### C2 🟩 — polar ↔ polarizable 혼동 (A3)
**English (draft)**
> Section 3.1 describes the P–S bond as *"highly polar covalent"*, yet the same section elsewhere (and the InF₃ passage in §3.2) correctly identifies *stronger polarizability* as the operative property. These are different quantities: with Δχ(P–S) ≈ 0.4 vs Δχ(P–O) ≈ 1.25, P–S is in fact **less polar and more covalent** than the oxide bond, while being **more polarizable** (a softer electron cloud). Since the argument requires high polarizability rather than high polarity, the two terms should be distinguished consistently.
**근거(KR)**: 원고 자신이 §3.2 InF₃ 문장에서 *"reduces polarizability"*로 옳게 씀 → §3.1의 *"highly polar"*가 **원고 자기 축에서 벗어난 표현**임이 원고 문장으로 확증(A3). 리비전 1순위. 우리 대응물도 ICOHP(공유성)·ELF(국재)로 갈려 있어 실익.
**소거 판단**: 채택. C1과 묶으면 "§3.1 화학 서술 정밀화" 한 코멘트.

### C3 🟨 — moisture and oxygen 병렬 (A1)
**English (draft)**
> Throughout §3.1, moisture and oxygen are listed in parallel as degradation agents. In practice, H₂O-driven hydrolysis is the dominant and faster pathway, whereas dry-O₂ oxidation is much slower — consistent with air-exposure studies using relative humidity as the primary variable. Stating which agent dominates (and under what humidity) would sharpen the mechanism.
**근거(KR)**: "산소랑 물 중 주범?"에 물이 답. O₂는 조연. 배영진 스타일(개선 제안)로 무난하나 급은 MEDIUM.
**소거 판단**: C31(정량/조건 묶음)에 흡수 가능. 단독 제출은 우선순위 낮음.

### C4 🟩 — HSEH (Mulks) 오기 + 고체 미적용 (A5·A10·A11)
**English (draft)**
> The Hard–Soft–Electron–Hole framework is attributed to *"Mulks et al."*, but ref [80] is single-authored (F. F. Mulks, *Chem* 10, 2024). More substantively, that work treats **discrete molecules in the gas phase** — no periodic/slab/surface calculations — and its solid-adjacent case explicitly reduces a crystal to a molecule. The manuscript's claim that HSEH explains *"electronic-structure evolution of the sulfide lattice"* therefore ascribes results the source does not contain. The reference should be corrected to a single author, and HSEH described as a **molecular-scale framework whose extension to solids is an untested analogy**.
**근거(KR)**: A10(et al. 사실오류, 고치기 쉬움), A11(격자 미적용 — 유비 넘어 없는 결과 귀속), A5(이론 자체는 알맹이 있음 → 단순 name-drop 지적은 부적절). 세 개를 **한 코멘트**로: 저자 표기 정정 + 적용범위 한정.
**소거 판단**: 채택. 사실 오류(et al.)가 섞여 있어 반영 확실.

### C5 🟩 — "bond energy" 정의 부재 (A18, §3.1·3.3 공통)
**English (draft)**
> "Bond energy" (and "lattice bond energy") is used repeatedly as the central explanatory variable — for air stability (§3.1), oxysulfide thermal stability (§3.3), and the InF₃ strategy (§3.2) — but is never defined or tied to a measurement. It could mean cohesive energy, bond-dissociation energy, a COHP integral, or a qualitative claim from a cited paper. Defining the quantity once and stating, for each cited value, whether it was measured or computed by that definition would make the mechanism arguments verifiable.
**근거(KR)**: A12(InF₃)·A18(oxysulfide)가 같은 문제. **상위 요구로 올림** — 개별 문장 아니라 리뷰 전반. 우리는 같은 양을 ICOHP로 잰다(접점).
**소거 판단**: 채택. §3 전체 관통이라 무게 있음.

---

## §3.2 Solvent Compatibility

### C6 🟩 — P⁵⁺ = soft acid, §3.1과 모순 (A7·A9) ★최우선
**English (draft)**
> Section 3.2 states, on HSAB grounds, that P⁵⁺ *"belongs to relatively soft Lewis acids"* attacked by polar solvents. This conflicts with §3.1, whose hydrolysis argument requires P⁵⁺ to be a **hard acid** (so that it prefers the hard base O²⁻ over S²⁻, driving Li₃PS₄ + 3H₂O → Li₃PO₄ + 3H₂S). If P⁵⁺ were genuinely soft, it would retain the soft base S²⁻ and the §3.1 driving force would vanish — so this is not a wording slip but two mechanisms that are **mutually inconsistent within HSAB** (Pearson classes P⁵⁺ with Si⁴⁺/Al³⁺ as hard). Moreover, the solvent donor atoms in NMP (amide N, carbonyl O) are hard bases; under the manuscript's own "soft P⁵⁺", HSAB would predict a mismatched, *weaker* attack — the cited theory does not support the stated conclusion. The nucleophilic-attack mechanism is more consistently written as **hard–hard (charge-controlled) substitution** at an electron-deficient P center. Whichever classification is adopted, the other section must be reconciled; if both mechanisms coexist, the governing conditions (aqueous vs non-aqueous; charge- vs orbital-controlled) should be stated.
**근거(KR)**: A7(원문 확인, 두 절 양립 불가)·A9(soft acid + hard base = HSAB상 부조화라 문장의 결론 반박). 원고가 정량손잡이로 쓰는 donor number(SbCl₅ 기준 σ-주개)가 hard basicity라 **DN 상관이 잘 맞는다는 사실 자체가 P⁵⁺=hard의 방증**. 리비전 **지적 최우선**.
**소거 판단**: 반드시 채택. §3 코멘트의 대표작.

### C7 🟩 — InF₃ 인과 역인용 (A12·A13)
**English (draft)**
> The InF₃ passage states that the additive *"enhances lattice bond energy and reduces polarizability"* to preserve conductivity after solvent immersion. Neither phrase appears in the cited work; in that paper, a *lower polarization rate* is given as the reason F⁻ substitution **lowers** ionic conductivity — the sign is reversed here. The cited work (from the corresponding author's own group) also contains single-dopant controls showing In and F act with **opposite signs** on the conductivity and moisture axes, yet the solvent-immersion axis actually cited has only pristine-vs-co-doped points. Restating the effect against the paper's actual basis (reduced H₂O/organic-solvent adsorption energy), and separating which element governs which axis, would remove both the reversed causation and the merged attribution.
**근거(KR)**: A12(인과 역전 — 원 논문에선 σ 낮추는 이유를 장점으로 뒤집음)·A13(단일 도펀트 대조군 실재, 두 축 부호 반대, 인용축엔 대조군 없음). 교신저자 본인 논문이라 반영 부담 적음.
**소거 판단**: 채택. 단 표현 강도는 "정의를 밝혀 달라/원 논문 근거로 바꿔 달라" 수준으로.

### C8 🟦 — "irreversibly reacts" 근거 (A8) — 소거 후보
**English (draft)**
> The claim that NMP *"irreversibly reacts"* with PS₄³⁻/P₂S₇⁴⁻ does not state whether irreversibility is thermodynamic (ΔG<0) or kinetic (a reverse-reaction barrier). Citing the basis (e.g., non-recovery of conductivity after removal, or a computed reaction energy) would support it.
**근거(KR)**: A8. 축 뭉갬(A2·A4 계열)이나 이건 근거 요구라 약함.
**소거 판단**: **소거 1순위.** C1(축 분리)에 이미 포함되는 성격. 단독 제출 불필요.

---

## §3.3 Thermal Stability

### C9 🟩 — "continuous network" 구조화학 오류 (A14)
**English (draft)**
> Section 3.3 attributes high thermal stability to a *"continuous covalent–ionic hybrid bond network"*, grouping LGPS, LPSCl, and Li₇P₃S₁₁ together. Their anion frameworks differ in connectivity: LGPS has (Ge/P)S₄ chains, Li₇P₃S₁₁ has P₂S₇⁴⁻ dimers plus PS₄³⁻, and **LPSCl is fully isolated PS₄³⁻ + free S²⁻ + Cl⁻** — the very "structural units" the manuscript itself invokes in §3.1–3.2. Describing LPSCl as a continuous network contradicts §3.1. Separating the three by anion connectivity (isolated / dimer / chain) and linking thermal stability to connectivity would resolve the conflict.
**근거(KR)**: A14. LPSCl 골격을 §3.1에선 "고립 PS₄³⁻ 공격받음", §3.3에선 "연결망이라 열에 강함"으로 → **원고 자기모순**. 강도 상위.
**소거 판단**: 채택.

### C10 🟩 — 불활성 400–500 °C를 안전성으로 오독 (A15·A23)
**English (draft)**
> Section 3.3 reports that crystalline sulfides retain structure to 400–500 °C **under inert atmosphere**, then concludes thermal resistance *"significantly superior to carbonate liquid electrolytes"*. The condition and conclusion are mismatched: inert-atmosphere decomposition temperature has little bearing on cell safety, where the real hazard is exothermic reaction with charged CAM (lattice-oxygen release) and with Li metal — onset well below 400–500 °C. Carbonate hazard, in turn, is governed by flash point / vapor pressure / thermal runaway, not decomposition temperature (DMC flash point ~18 °C), so comparing decomposition temperatures compares mismatched axes. The inert-atmosphere qualifier should carry to the conclusion, and safety comparison should use DSC exothermic onset / heat release (J/g) under CAM- or Li-coexisting conditions. Defining a *thermal safety margin* as (hazard-onset − max operating temperature) would make this quantitative and remove the misreading.
**근거(KR)**: A15(조건-결론 어긋남 + 축 불일치)·A23(safety margin 정의하면 오독 자동 소거). 강도 상위.
**소거 판단**: 채택. safety margin 정의 제안까지 포함하면 건설적.

### C11 🟨 — O 도입 σ 대가 미기재 (A19·A22)
**English (draft)**
> Oxygen incorporation (oxysulfide) is presented in both §3.1 and §3.3 as raising bond energy and stability, with no cost stated. It is well established — and the manuscript's own §3.3 outlook hints at it (*"while maintaining high ionic conductivity"*) — that O incorporation lowers ionic conductivity. Adding one line on the conductivity penalty where O incorporation is proposed would prevent it being read as a cost-free remedy, and would make it a concrete entry in the trade-off discussion.
**근거(KR)**: A19·A22. 저자가 outlook엔 *while maintaining* 단서를 달면서 본문(Q11)엔 대가 없이 제시 = **알면서 안 씀**. 우리 MD로 Ea 증가 정량 보유(절대값 인용 X). B1(축상충 표)의 대표 사례.
**소거 판단**: 채택 또는 C30(축상충)에 흡수. 저자 자인 근거가 있어 반영 쉬움.

### C12 🟨 — 코팅 두 기전 뭉갬 (A20)
**English (draft)**
> The LiNbO₃/Al₂O₃ coating is described as both *"buffering oxygen evolution"* (chemically binding released lattice oxygen) and *"inhibiting direct contact"* (a physical barrier). These are different actions; the conventional role of these coatings is physical separation plus self-chemical-stability, whereas active absorption of evolved O₂ needs separate evidence. Separating the two mechanisms, and supporting the "buffering" claim, would clarify the strategy.
**근거(KR)**: A20. 급 MEDIUM.
**소거 판단**: 남기면 무난, 지워도 무방. 배영진 코멘트 다수가 이런 "두 서술 화해" 형이라 톤은 맞음.

---

## §3.4 Electrochemical Stability

### C13 🟩 — "true" thermodynamic window (A26·A27)
**English (draft)**
> Section 3.4 contrasts the *"true thermodynamic stability range"* from first principles with the *"apparent"* CV window. The computed window is itself model-dependent — it shifts with (i) the hull convention for metastable SEs (e.g., placing an ordered arrangement at E_hull→0 despite a finite energy), (ii) which configuration is used, and (iii) the phase set included. Labeling it *"true"* leads readers to conclude the experiment is wrong. It should read *"computed (under a given phase set / hull convention)"*, and the two windows should be noted as **measuring different quantities** — the calculation gives the onset of thermodynamic driving force, CV the point of measurable current — with the difference attributable to kinetic overpotential and decomposition-product passivation. The cited source of this method already gives that explanation, so adding it here carries no citation burden.
**근거(KR)**: A26(계산도 규약 의존, "true" 과함 — 우리가 상 집합 변경으로 onset 달라짐 직접 겪음)·A27(불일치 이유를 이 자리에서 안 줌 → 독자가 "실험이 틀렸다"로 오독). 방법 원전([Zhu15])이 이미 설명 제공.
**소거 판단**: 채택. 우리가 정면으로 아는 칸.

### C14 🟨 — 인용 창 값 조건 미기재 (A28·C31로 흡수 가능)
**English (draft)**
> The quoted window (e.g., LGPS ≈ 1.7–2.1 V) is given without stating the method, hull/ordering convention, or phase set from which it derives, and the anodic limit is a μ_Li-referenced computed quantity that must be aligned before being placed beside a cell voltage. One line of (method / convention / source) per quoted window would let readers reproduce it.
**근거(KR)**: A28. 배영진식 조건 명시 요구.
**소거 판단**: **C31(정량 묶음)에 흡수** 권장. 단독 유지 시 MEDIUM.

### C15 🟩 — 계면 3분류: 판별·기계축·정적성 (A29·A30·A31, +A38 흡수)
**English (draft)**
> The three-way interface classification (thermodynamically stable / mixed ion–electron conductive / SEI-like passivated) is valuable but (a) uses only ion/electron transport, omitting the mechanical axis — yet §3.5 and §5.1.3 show volume change and cracking break the interface, so an electronically insulating layer still fails once cracking exposes fresh surface; (b) provides no observable to **distinguish** a thermodynamically stable interface from a passivated one (both look identical if impedance does not grow) or a threshold for what counts as *"low electronic conductivity"*; and (c) is static, whereas §5.1.2's own "band-gap narrowing → electron penetration" implies a passivated→MCI transition over time. Adding a distinguishing observable per type, a σ_e (or band-gap) threshold, a "mechanically retained?" condition, and noting the classification is an **initial** state that can evolve would connect §3.4 with §3.5 and §5.1.
**근거(KR)**: A29(기계축 부재 = B1 실례)·A30(판별 관측량 없음)·A31(정적 → 궤적으로)·A38(문턱값 없음, 여기 흡수). 우리는 gap ≥4/2–4/<2 eV 3구간 판정 보유.
**소거 판단**: 채택. C18(문턱)을 여기 흡수해 하나로.

### C16 🟩 — "chemical potential gradient가 구동력↓" (A34·A35) ★가장 실질적 개선
**English (draft)**
> Section 3.4 states that an oxide buffer coating *"establishes a chemical potential gradient … reducing the driving force for interfacial reactions."* Thermodynamic driving force is set by the chemical potentials of the two end phases and is not reduced by inserting a layer between them. What a coating actually does is (i) block direct contact, (ii) be self-stable against each side, and (iii) block electron transport. If "gradient" means a stepwise division, then each step can still react — which is exactly the practical difficulty of coating selection. The wording is more accurate as **"blocking direct contact + self-stability against both sides."** Relatedly, §4.2.2's ideal-coating criteria (high-voltage stability, σ_ion, minimal σ_e, mechanical compliance) consider only the cathode side, but a coating sits **between** cathode and SE and forms two interfaces; adding **reactivity against the SE** as a fifth criterion would substantially strengthen the materials-selection discussion — in practice, reaction with the SE is a harsher screen than reaction with the cathode.
**근거(KR)**: A34(열역학 구동력은 두 끝 상이 정함 → 층으로 안 줄음)·A35(코팅 자기 분해산물도 3분류로 평가). §4.2.2 5번째 조건 제안. 우리 47종 전수에서 SE축 29/47 탈락이 근거(절대값은 노트에만). **이번 리뷰 최대 실질 개선 제안.**
**소거 판단**: 반드시 채택. §4 배영진 코멘트(코팅 core-shell 전자경로 C8)와도 정합.

### C17 🟩 — 덴드라이트 두 기전 + SE 고유 σ_e 누락 (A37·A39)
**English (draft)**
> Section 3.4 explains dendrite nucleation/growth via an **electronic-pathway** mechanism (electronically conductive decomposition products), while §5.1.1 gives a **mechanical** "wedge-opening" mechanism (Li injected at the crack rear), explicitly stated to differ from the classical tip-stress model. The relationship between the two (nucleation vs propagation, or independent paths) is not connected. In addition, §3.4 names only the decomposition products' σ_e, whereas §5.1.2 also invokes the **SE's own intrinsic σ_e** (recombination of Li⁺+e⁻ within the electrolyte). One sentence noting "nucleation via electronic path, propagation via mechanics, treated in §5.1" and "both product σ_e and intrinsic SE σ_e" would tie §3.4 to §5.1.
**근거(KR)**: A37(절 사이 불일치)·A39(산물만 지목, SE 고유 σ_e 뺌). 우리 계에선 그 산물이 Li₃P(gap≈0.70 eV=conductor)로 특정됨(노트).
**소거 판단**: 채택. 배영진 C3(§4.1.3 세 요인 상대기여)와 같은 "절 내부 정합" 유형이라 톤 일치.

### C19 🟨 — "far exceeds" 값 없음 + 내부 충돌 (A32·A33)
**English (draft)**
> Section 3.4 says the CAM operating voltage *"far exceeds"* the sulfide stability threshold, without the two numbers (layered-oxide operation ~3.0–4.3 V; sulfide anodic limit ~2.0–2.3 V, a μ_Li-referenced quantity). It also sits in tension with the same section's kinetic-stabilization argument: if passivation works, exceeding the thermodynamic threshold is not itself severe degradation (LiNbO₃-coated cells cycle at 4.3 V). Stating both voltages, and one sentence on which regime dominates when, would resolve both.
**근거(KR)**: A32(절 내부 자기모순 — kinetic 안정화 vs 열역학 초과 단정)·A33(숫자 없음 + 기준계 명시). 
**소거 판단**: C13/C31과 성격 겹침. **C13에 "내부 충돌" 한 줄 얹거나 C31에 숫자 흡수**로 처리 가능. 단독 유지 시 MEDIUM.

---

## §3.5 Mechanical Stability

### C20 🟩 — "몰부피 차이" 정규화·부호 (A41·A42)
**English (draft)**
> Section 3.5 states that Li₂S and Li₃P have molar volumes *"significantly different from the base phase"*, driving local expansion. But per-formula-unit molar volumes of Li₂S (3 atoms/f.u.) and Li₆PS₅Cl (13 atoms/f.u.) are not directly comparable — a compositional difference is being read as a volume change, and the sign can invert with the normalization basis (per atom / per anion / per f.u.). The meaningful quantity is **ΔV of a balanced reaction** (per mole of SE consumed, stating whether the Li-metal volume consumed at the anode is included). The reaction and normalization basis should be given together; likewise the **sign of "localized volume expansion" is undetermined until the system boundary is drawn.**
**근거(KR)**: A41(정규화 기준 없음)·A42(부호 미정). 배영진식 정의 요구. 
**소거 판단**: 채택. C22와 묶어 "§3.5 물성 정의" 한 덩어리로.

### C21 🟩 — fracture toughness를 탄성량으로 지지 (A40)
**English (draft)**
> The §3.5 opening sets up *limited fracture toughness* as a cause of mechanical degradation, but what is widely reported for sulfides is **elastic modulus / hardness**, a different class of property from the crack property K_IC. Low stiffness in fact aids contact conformity (cold-press formability), so using modulus as evidence for toughness conflicts with the same section's formability statement. Citing measured K_IC (nanoindentation / microbeam), or otherwise tempering to *"inferred from reported elastic/hardness data"*, would align the property with the claim.
**근거(KR)**: A40. 저강성 = 성형성 유리(냉간압착)이므로 인성 근거로 쓰면 같은 절 성형성 서술과 충돌. **우리도 (i) K_IC 축이 없고 탄성량뿐** → 정직한 코멘트. Pugh caveat 주의(우리 로스터도 취성 근거로 쓰면 같은 혼동).
**소거 판단**: 채택. C20·C22와 §3.5 물성 덩어리로.

### C22 🟩 — 변형에너지 vs 파괴인성 차원 불일치 (A53)
**English (draft)**
> Section 3.5 writes that elastic strain energy *"exceeds the fracture toughness threshold"*, but strain energy has units of J (or J/m³) and fracture toughness K_IC has units of Pa·m^½ — different dimensions. The fracture criterion is **G ≥ G_c** (both J/m²) or **K ≥ K_IC** (both Pa·m^½), and the reference quantity is the energy **release rate per new crack area**, not total stored energy. Replacing *fracture toughness* with **critical energy release rate G_c** fixes it. The underlying size effect is correct (stored energy ∝ d³ vs crack energy ∝ d²), so one line deriving the ~3 μm threshold and its validity conditions (composition, stack pressure, depth of discharge) would let readers transfer the value.
**근거(KR)**: A53(차원)·A54·A55(크기효과 논지는 옳음, 유도·조건만 빠짐). 즉시 수정 가능(단어 교체).
**소거 판단**: 채택. **가장 반박 불가**(차원은 객관). C20·C21과 묶어 §3.5 물성 코멘트 하나로 하면 강력.

### C23 🟩 — LiCl 누락 (A43)
**English (draft)**
> Section 3.5 lists LMA-contact products as *"Li₂S, Li₃P, and related composite phases"*, but the standard grand-potential result for the halide-bearing argyrodite central to this review is **Li₃P + Li₂S + LiCl**. The omitted LiCl is the one phase of the three with a wide band gap, directly relevant to §3.4's target of a *"low-electronic-conductivity passivation layer."* Adding LiCl connects §3.4 and §3.5.
**근거(KR)**: A43. Intro·§3.4에서도 반복된 누락. LiCl이 셋 중 유일 광밴드갭 → §3.4 passivation 논지와 직결.
**소거 판단**: 채택. 쉬운 사실 보강 + 절 연결 효과.

### C24 🟩 — "빈 균열 = 저임피던스" 인과 역전 (A56·A57)
**English (draft)**
> Section 3.5 states that particle fracture creates *"low-impedance pathways"* through which Li penetrates. An empty crack is a pore, so its ionic impedance is in fact infinite; it becomes low-impedance only **after Li metal fills it** — the result is written as the cause's property. Furthermore, §5.1.1's wedge-opening description has the **opposite order** (a crack exists first, then Li is injected at its rear), and the manuscript itself notes this differs from the classical tip-stress model. Rewording to *"a mechanically favorable path and fresh free surface form, which become an electron-conduction path once plated Li fills them"* makes §3.5 and §5.1.1 consistent.
**근거(KR)**: A56(빈 균열은 기공 → 이온 임피던스 무한대)·A57(§5.1.1과 순서 반대). 결과를 원인 성질로 적음.
**소거 판단**: 채택. 절 연결 + 논리 오류라 무게 있음.

### C25 🟩 — 같은 계면상에 전자·기계 두 요구 (A44·A29) = B1 대표사례
**English (draft)**
> Section 3.4 requires the interphase to have *"high σ_ion, low σ_e"*, while §3.5 identifies the **same product set** (notably Li₃P) as the driver of volume mismatch and stress. The requirement that a passivation layer be **simultaneously electronically insulating and volumetrically compatible** is stated nowhere. Since Li₃P is already problematic on the first criterion, one sentence adding the mechanical requirement connects the two sections and is the clearest instance of the cross-axis conflict noted below (C30).
**근거(KR)**: A44(전자·기계 두 요구 미명시)·A29(3분류 기계축 결여). B1 축상충의 최선 실례.
**소거 판단**: 채택, 또는 C30(축상충 상위)에 대표사례로 흡수.

### C26 🟨 ✚ — 입자크기 절 간 충돌 (신규, B1 확장)
**English (draft)**
> Section 3.5 proposes reducing particle size below ~1 μm to distribute reaction-induced volume change and suppress cracking. However, §3.1 and §3.2 tie smaller particles (higher specific surface area) to **faster air/solvent degradation** and higher interfacial resistance. The optimal particle size for mechanical stability therefore conflicts with that for chemical stability, and the manuscript does not discuss the two together. Noting this trade-off — or the regime where each dominates — would prevent a size recommendation in one section from undercutting another.
**근거(KR)**: ✚ 신규(노트 B1 축상충의 미기재 실례). 3.5 "작게" ↔ 3.1·3.2 "작으면 반응↑". 우리 DEM이 절충점 찾는 도구지만 **우리 해석 의존도 있음** → 순화 필요.
**소거 판단**: 남기려면 순화(우리 DEM 언급 빼고 "두 절 요구 충돌"까지만). 소거해도 C30이 커버.

### C27 🟨 ✚ — 임계크기 내부 수치 불일치 (신규)
**English (draft)**
> Section 3.5 uses two different critical particle sizes — cracking becoming significant *above ~3 μm* in one passage and safety secured *below 1 μm* in the mitigation passage. Stating these as a single trend ("smaller is safer") or reconciling the two thresholds with their conditions would remove the apparent inconsistency.
**근거(KR)**: ✚ 신규. 같은 절 안 3 μm(취약 개시)·1 μm(안전 확보) 병존. C22의 "조건 명시"와 함께 처리 가능.
**소거 판단**: **C22에 흡수** 권장(둘 다 임계크기 조건 문제). 단독은 사소.

### C28 🟨 ✚ — stack pressure 양날 (신규, A46 확장)
**English (draft)**
> The manuscript notes that stack pressure aids intimate contact (a benefit) and, in the mitigation discussion, that excessive mechanical constraint accumulates stress (a cost) — implying an optimal pressure window. Stating that window, or the quantity that sets it (contact retention vs crack/short risk), would turn a qualitative caution into actionable guidance.
**근거(KR)**: ✚ 신규(A46 인접). 저자가 대응책에선 "과압 방지"로 인정(§3.3 outlook 자인 패턴). 우리 DEM 압력 시뮬이 최적창 정량 도구.
**소거 판단**: 우리 해석 의존 → 순화하거나 소거. C31/C29 묶음에 흡수 가능.

---

## §3 전반 (묶음 코멘트)

### C29 🟨 — outlook이 소망 목록 (A6·A24)
**English (draft)**
> The section-closing outlooks (§3.1's four "future model requirements", §3.3's three "synergistic dimensions") list desiderata without distinguishing **what is already partly done from what remains open** — e.g., §3.1's "electron–hole coupling" and "solid–gas reaction thermodynamics" are partly addressed by the manuscript's own refs [80] and [84]. Appending, to each requirement, the current state (which reference reaches it) and the remaining gap would turn the outlooks from wish-lists into a roadmap.
**근거(KR)**: A6·A24. §3.1·§3.3 outlook 같은 형태. 우리 좌표 찍는 자로도 유용.
**소거 판단**: 채택(묶음). §3 전반 서술 방식 지적이라 무게 있음.

### C30 🟩 — 축 상충 매트릭스 부재 (B1) ★상위 구조 제안
**English (draft)**
> A single bond characteristic (the covalent–ionic / polarizable P–S bond) is cited with **opposite signs** across sections: as the **weakness** in §3.1 (low bond energy / high polarizability → water attack) and as a **strength** in §3.3 (high decomposition temperature) and §3.5 (low modulus / plastic deformation → good contact). Likewise, several remedies improve one axis at another's expense — oxygen incorporation raises air/thermal stability but lowers ionic conductivity; particle-size reduction aids mechanics but worsens air/solvent stability; polymer compositing raises toughness but dilutes conductivity. Each section's outlook already flags its own trade-off with a *"while maintaining …"* clause. Consolidating these into a **single cross-axis trade-off matrix** (stability axis × remedy, with the sign on each other axis) would convert scattered caveats into the review's most useful synthesis, at no new-data cost.
**근거(KR)**: B1. 결합특성이 절마다 다른 부호로 인용됨(A14 관련). outlook의 *while maintaining* 단서들이 곧 상충 축(A22). **리뷰 부가가치 최대 지점 중 하나.**
**소거 판단**: 반드시 채택. C11·C25·C26을 이 안의 실례로 흡수 가능.

### C31 🟨 — 정량 부재 반복 (A15·A21·A33·A36 = B4)
**English (draft)**
> Several central claims are stated without conditions or numbers — *"significantly"* (heat release, cycling improvement), *"far exceeds"* (voltage), *"400–500 °C"*, *"1.7–2.1 V"* — recurring across §3.3–3.5. At minimum, comparative claims should carry the number and the condition (method, atmosphere, phase set / hull convention, cycle count / capacity retention) so readers can transfer them.
**근거(KR)**: A15·A21·A33·A36. 개별 아니라 **원고 전반 정량 부재**로 묶음. 배영진 Comment 2(high voltage 미정량)와 동형.
**소거 판단**: 채택(묶음). C3·C14·C19·C27의 숫자·조건 요구를 여기 흡수.

### C32 🟩 — 화학–역학 되먹임 고리 모식도 (A59·B6) ★부가가치 최대
**English (draft)**
> The manuscript already contains every piece of the chemo-mechanical feedback loop but never closes it: interface reaction → volume mismatch (§3.5) → tensile stress (§3.5) → cracking/fracture (§3.5) → **passivation breakdown via fresh-surface exposure** (§3.4) · **Li penetration/short** (§3.5, §5.1.1) · **conduction-network disruption** (§3.5). The only missing arrow is **"fresh surface → reaction restart."** Drawing this as a single schematic closes the loop and answers *why degradation accumulates each cycle* (§3.5's *"during cycling"*). It requires no new data — only a reorganization of existing content — so its cost-to-value ratio is the highest available.
**근거(KR)**: A59·B6. 원고가 조각 다 보유, 빠진 화살표 하나("새 표면→반응 재개"). 새 데이터 0. 
**소거 판단**: 반드시 채택. 리뷰어가 줄 수 있는 최고의 건설적 제안.

### (추가 척도 제안, 선택) 🟨 — 네트워크 단절에 측정량 (A58)
**English (draft)**
> Section 3.5's *"disruption of the ionic conduction network"* is stated qualitatively, but it is a measurable quantity (contact-area loss, tortuosity increase, effective-conductivity drop) that particle-scale microstructure models (discrete-element / effective-medium) compute directly. One line and a reference would make §3.5 actionable for both experimental and modeling readers.
**근거(KR)**: A58. 우리 DEM이 정확히 이 값을 냄(접점). 우리 해석 의존 → 순화.
**소거 판단**: C32(모식도)나 C30에 흡수하거나 선택적. 단독은 MEDIUM.

---

## 🗳 소거 시나리오 (참고용 3안)

**A안 — 핵심만 (8개, 강한 것만)**: C6, C9, C10, C13, C15, C16, §3.5물성(C20+C21+C22 묶음), C24 + 구조 2개(C30, C32).
→ 사실/정의 오류·절간 모순·구조 제안만. 반영률 최고, 톤 강경.

**B안 — 균형 (12개)**: A안 + C4, C7, C17, C23, C31(정량 묶음), C11.
→ 두 리뷰어 분량과 비슷(김동석 6·배영진 9). 권장.

**C안 — 전수 (묶음 후 ~16개)**: B안 + C1+C2(묶음), C5, C12, C25, C29, C19(→C13흡수), C26·C27·C28(순화).
→ 다 넣되 묶음으로 압축. 1저자가 직접 소거하도록.

**소거 1순위(어느 안이든 먼저 뺄 것)**: C8, C28, C27(→C22), C18(→C15), C14(→C31).
**절대 빼면 안 됨**: C6(P⁵⁺ 모순), C9(network 모순), C13(true window), C16(chempot gradient), C22(차원), C30·C32(구조).
