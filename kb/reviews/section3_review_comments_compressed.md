# Comments on Section 3 (Intrinsic Stability of Sulfide SEs) — 압축판 v2

> **무엇** — 제출용 §3 리뷰 코멘트. 기존 17개 → **12개**, 분량 약 −30 %.
> 원본: `Review_comment_section_3.docx` (17 comments) · 후보 원장: `section3_review_candidates.md`
> A-번호 원장: `kb/reviews/ECERD2600097_review_notes.md`
>
> ⚠ **미출판 심사 원고** — 원문 그대로 옮기지 않는다. 우리 db 수치는 절대값으로 넣지 않는다.

---

## 🔧 v2 에서 바뀐 것 (원본 대비)

### ⛔ 삭제 — 반박당하는 대목 1건 **(가장 중요)**

**구 Comment 11 의 두 번째 문단** (*"fracture toughness 를 탄성량으로 지지한다"*)을 **통째로 뺐다.**

- **원고 §3.5 는 이미 K_IC = 0.2–0.4 MPa·m^½ 를 refs 123–124 로 인용한다.**
- 원고는 *"낮은 E(10–30 GPa)는 접촉에 유리하나 **낮은 파괴인성**이 취약점"* 으로 **두 물성을 이미 구분**하고,
  완화책으로 **폴리머 복합화 → 파괴인성 ↑** (refs 125–127) 까지 제시한다.
- 즉 *"모듈러스를 인성의 근거로 쓴다"* 는 전제가 성립하지 않는다. **한 줄로 반박된다.**

**대체 지적 (신규, 더 강함)** — K_IC 를 **재료상수처럼** 인용한다. 파괴인성은 탄성계수와 달리
**치밀도·입경·불순물·기존 균열·기공률에 강하게 의존하는 시편 물성**이다.
★ **바로 그것이 ~3 μm 임계 크기에 조건이 안 붙는 이유**다 — K_IC 를 상수로 두면 임계 크기도 상수처럼 보인다.

### ✚ 추가 — 원고 내부 수치 불일치 1건

§3.5 안에 **>~3 μm(파쇄 개시)** 과 **<1 μm(안전 확보)** 두 임계 크기가 병존한다.
후보 문서에서 C27 로 잡아 두고 "소거 1순위"로 분류했으나, 위 삭제로 자리가 비었고
**같은 뿌리(임계 크기의 조건 미기재)** 라 새 Comment 10 에 흡수했다.

### 🔗 병합 4건

| 구 | → 신 | 왜 |
|---|---|---|
| 5 (bond energy 정의) | **5** 에 흡수 | 구 6(InF₃)의 *"lattice bond energy"* 가 이 문제의 실례다. 사실오류(오인용)에 얹으면 반영률이 오른다 |
| 12 (저임피던스 인과역전) + 13 (LiCl 누락) | **9** 로 통합 | 셋 다 **§3.4↔§3.5↔§5.1.1 을 잇는 같은 작업**이다. 따로 내면 잔소리, 묶으면 구조 지적 |
| 14 (정량 부재) | **6** 에 흡수 | 실질 내용은 두 전압값뿐이고, 그 자리는 §3.4 창 논의(구 7)다 |
| 15 (outlook 소망목록) | **11** 에 흡수 | 구 16 자신이 *"outlook 의 while maintaining 단서가 곧 상충 축"* 이라 쓴다. 같은 재료를 두 번 요구하지 않는다 |

### ✂ 단축

구 1·4·8·9 는 논지 유지한 채 문장만 압축했다. 구 16 은 실례(Li₃P 이중 요구)를 유지하되 문단을 갈랐다.

### 📤 §3 밖으로 넘길 것 (여기 넣지 않음)

**Monroe–Newman**: 원고는 Li 침투를 wedge-opening + K_IC 로 서술하고 **전단탄성률 기준을 쓰지 않는다.**
그 전환은 **옳다** — 무기 SE 에서 해당 기준의 부적용이 이론(Ahmad & Viswanathan, *PRL* 2017)과
실험(E ≈ 20 GPa 유리부터 150 GPa 가넷까지 전 구간 Li 성장) 양쪽에서 보고돼 왔다.
다만 원고가 **말없이** 갈아탔고, 저자 그룹의 2023 선행 리뷰는 그 기준을 썼다.
*"버렸다"* 한 문장이면 **의도적 갱신**으로 읽힌다 — 지적이 아니라 선물이다.
→ **§5 담당자에게 전달.** (근거: `review_notes.md` C4)

---

## 제출 본문 (12 comments)

### Comment 1 — P⁵⁺ hard/soft 내부 모순 ★최우선 *(A7·A9)*

Section 3.2 states, on HSAB grounds, that P⁵⁺ "belongs to relatively soft Lewis acids" attacked by
polar solvents. This conflicts with Section 3.1, whose hydrolysis argument requires P⁵⁺ to be a **hard**
acid — only then does it prefer the hard base O²⁻ over S²⁻, driving Li₃PS₄ + 3H₂O → Li₃PO₄ + 3H₂S.
If P⁵⁺ were genuinely soft it would retain S²⁻ and the Section 3.1 driving force would vanish, so this
is not a wording slip but two mechanisms that are mutually inconsistent within HSAB (Pearson groups
P⁵⁺ with Si⁴⁺ and Al³⁺ as hard). Furthermore, the donor atoms of NMP (amide N, carbonyl O) are hard
bases: under the manuscript's own "soft P⁵⁺", HSAB predicts a mismatched and therefore *weaker*
attack, so the cited theory does not support the stated conclusion. The mechanism is more consistently
described as hard–hard (charge-controlled) substitution at an electron-deficient P center. Whichever
classification is adopted, the other section should be reconciled; if both mechanisms coexist, the
governing conditions (aqueous versus non-aqueous, charge- versus orbital-controlled) should be stated.

### Comment 2 — §3.1 화학 서술 2건 *(A2·A4·A3)*

Two chemical descriptions in Section 3.1 would benefit from precision. First, the hydrolysis
susceptibility of the soft base S²⁻ is attributed to a "lowered kinetic barrier", but HSAB describes a
thermodynamic preference, which is distinct from reaction rate; the actual kinetics depend on surface
area, crystallinity (amorphous faster than crystalline), and composition. The same conflation recurs in
the summary sentence ("thermodynamic **and** kinetic susceptibility"), so the two axes are best separated
throughout the section, with the HSAB argument framed as thermodynamic. Second, the P–S bond is called
"highly polar covalent", yet elsewhere — including the InF₃ passage in Section 3.2 — the manuscript
correctly identifies **polarizability** as the operative property. These are different quantities: with
Δχ(P–S) ≈ 0.4 versus Δχ(P–O) ≈ 1.25, P–S is *less* polar and more covalent than the oxide bond while
being *more* polarizable, and the argument requires the latter. Distinguishing the two terms
consistently would remove an internal inconsistency.

### Comment 3 — "continuous network" 구조화학 *(A14)*

Section 3.3 attributes high thermal stability to a "continuous covalent–ionic hybrid bond network",
grouping LGPS, LPSCl, and Li₇P₃S₁₁ together. Their anion frameworks differ in connectivity: LGPS has
(Ge/P)S₄ chains, Li₇P₃S₁₁ contains P₂S₇⁴⁻ dimers together with PS₄³⁻, and **LPSCl is fully isolated
PS₄³⁻ plus free S²⁻ and Cl⁻** — the same "structural units" the manuscript itself invokes in Sections
3.1 and 3.2. Describing LPSCl as a continuous network therefore contradicts Section 3.1. Separating the
three materials by anion connectivity (isolated, dimer, chain) and linking thermal stability to
connectivity would resolve the conflict.

### Comment 4 — 불활성 400–500 °C 를 셀 안전성으로 *(A15·A23)*

Section 3.3 reports that crystalline sulfides retain their structure to 400–500 °C **under inert
atmosphere**, then concludes that their thermal resistance is "significantly superior to carbonate
liquid electrolytes". The condition and the conclusion are mismatched. Inert-atmosphere decomposition
temperature has little bearing on cell-level safety, where the hazard is the exothermic reaction with
charged cathode active material (lattice-oxygen release) and with lithium metal, whose onset lies well
below 400–500 °C. The hazard of carbonate electrolytes, in turn, is governed by flash point, vapour
pressure, and thermal runaway rather than decomposition temperature (dimethyl carbonate flash point
≈ 18 °C), so comparing decomposition temperatures compares mismatched axes. The inert-atmosphere
qualifier should be carried into the conclusion, and the comparison should rest on DSC exothermic onset
and heat release (J g⁻¹) under cathode- or lithium-coexisting conditions. Defining a **thermal safety
margin** as (hazard onset − maximum operating temperature) would make this quantitative and remove the
possible misreading.

### Comment 5 — InF₃ 인용 정확성 + "bond energy" 정의 *(A12·A13·A18)* 🔗흡수

The InF₃ passage in Section 3.2 states that the additive "enhances lattice bond energy and reduces
polarizability" to preserve conductivity after solvent immersion. **Neither phrase appears in the cited
work**; in that study a lower polarization rate is given as the reason F⁻ substitution *lowers* ionic
conductivity, so the sign is reversed here. The cited work also contains single-dopant controls
indicating that In and F act with **opposite signs** on the conductivity and moisture axes, whereas the
solvent-immersion axis actually cited has only pristine-versus-co-doped points. Restating the effect
against the paper's own basis (reduced adsorption energy of H₂O and organic solvent), and indicating
which element governs which axis, would remove both the reversed causation and the merged attribution.
More broadly, "bond energy" (and "lattice bond energy") recurs as a central explanatory variable across
Sections 3.1–3.3 but is never defined or tied to a measurement — it could denote cohesive energy,
bond-dissociation energy, an integrated crystal-orbital overlap population, or a qualitative claim from
a cited work. Defining it once, and stating for each cited value whether it was measured or computed
under that definition, would make these arguments verifiable across sections.

### Comment 6 — 계산 창 "true" + 두 전압값 + 절 내부 충돌 *(A26·A27·A28·A32·A33)* 🔗흡수

Section 3.4 contrasts the "**true** thermodynamic stability range" from first principles with the
"apparent" cyclic-voltammetry window. The computed window is itself model-dependent: it shifts with the
hull convention adopted for metastable electrolytes (for example, placing an ordered arrangement at
E_hull → 0 despite a finite energy), with the configuration chosen, and with the phase set included.
Labelling it "true" leads readers to conclude the experiment is in error. "Computed (under a given phase
set and hull convention)" would be more accurate, and the two windows measure **different quantities** —
the calculation gives the onset of thermodynamic driving force, the voltammogram the point of measurable
current — with the difference attributable to kinetic overpotential and to passivation by decomposition
products; the original source of this method already provides that explanation, so adding it carries no
citation burden. Relatedly, the claim that the cathode operating voltage "far exceeds" the sulfide
threshold would benefit from both numbers (layered oxide ≈ 3.0–4.3 V; sulfide anodic limit ≈ 2.0–2.3 V,
the latter a chemical-potential-referenced computed quantity that must be aligned before being placed
beside a cell voltage). It also sits in tension with the same section's kinetic-stabilization argument:
if passivation operates, exceeding the thermodynamic threshold is not by itself severe degradation, as
coated cells cycling at 4.3 V indicate. One sentence on which regime dominates when would resolve this.

### Comment 7 — 계면 3분류: 판별 관측량·기계 축·시간 전이 *(A29·A30·A31·A38)*

The three-way interface classification (thermodynamically stable, mixed ionic–electronic conductive,
SEI-like passivated) is useful but could be strengthened in three respects. First, it uses only ionic
and electronic transport and omits the **mechanical** axis, yet Sections 3.5 and 5.1.3 show that volume
change and cracking break the interface — an electronically insulating layer still fails once cracking
exposes fresh surface. Second, it provides no observable to **distinguish** a thermodynamically stable
interface from a passivated one (the two appear identical if impedance does not grow), nor a threshold
for what counts as "low electronic conductivity". Third, it is **static**, whereas Section 5.1.2's own
"band-gap narrowing leading to electron penetration" implies a passivated-to-mixed-conductor transition
over time. Adding a distinguishing observable per type, an electronic-conductivity or band-gap
threshold, a "mechanically retained" condition, and a note that the classification describes an *initial*
state that can evolve, would connect Section 3.4 with Sections 3.5 and 5.1.

### Comment 8 — 화학퍼텐셜 구배 + 이상적 코팅의 다섯 번째 조건 ★가장 실질적 *(A34·A35)*

Section 3.4 states that an oxide buffer coating "establishes a chemical potential gradient … reducing
the driving force for interfacial reactions." The thermodynamic driving force is set by the chemical
potentials of the two end phases and is **not** reduced by inserting a layer between them. What a coating
actually does is to block direct contact, to be self-stable against each side, and to block electron
transport; if "gradient" is meant as a stepwise division, then each step can still react — which is
precisely the practical difficulty of coating selection. "Blocking direct contact together with
self-stability against both sides" would be more accurate. Relatedly, the ideal-coating criteria in
Section 4.2.2 (high-voltage stability, ionic conductivity, minimal electronic conductivity, mechanical
compliance) consider only the cathode side, but a coating sits **between** cathode and electrolyte and
forms two interfaces. Adding **reactivity against the solid electrolyte** as a fifth criterion would
substantially strengthen the materials-selection discussion, since in practice reaction with the
electrolyte is a harsher screen than reaction with the cathode.

### Comment 9 — §3.4 ↔ §3.5 ↔ §5.1 을 잇는 세 곳 *(A37·A39·A56·A57·A43)* 🔗통합

Three adjacent statements would connect Sections 3.4, 3.5, and 5.1 if adjusted together. **(i)** Section
3.4 explains dendrite nucleation and growth through an **electronic-pathway** mechanism (conductive
decomposition products), whereas Section 5.1.1 gives a **mechanical** "wedge-opening" mechanism (lithium
injected at the rear of a crack), explicitly stated to differ from the classical tip-stress model; their
relationship — whether they divide nucleation from propagation, or are independent — is not stated.
Section 3.4 also names only the products' electronic conductivity, whereas Section 5.1.2 additionally
invokes the **intrinsic** conductivity of the electrolyte. **(ii)** Section 3.5 states that fracture
creates "low-impedance pathways" through which lithium penetrates; an empty crack is a pore, so its ionic
impedance is effectively infinite, and it becomes low-impedance only *after* lithium fills it — the
result is written as a property of the cause, and the order is opposite to Section 5.1.1's. "A
mechanically favourable path and a fresh free surface form, which become an electron-conduction path once
plated lithium fills them" would align the two. **(iii)** Section 3.5 lists the lithium-contact products
as "Li₂S, Li₃P, and related composite phases"; for the halide-bearing argyrodite central to this review
the standard grand-potential result is **Li₃P + Li₂S + LiCl**, and the omitted LiCl is the one phase of
the three with a wide band gap — directly relevant to the low-electronic-conductivity passivation layer
targeted in Section 3.4.

### Comment 10 — §3.5 의 정의·정규화·임계값 *(A41·A42·A53·A61·A54·A55 + 신규)* 🔧수정

Three quantitative statements in Section 3.5 would benefit from a stated basis. **(i)** Li₂S and Li₃P are
said to have molar volumes "significantly different from the base phase", but per-formula-unit volumes of
Li₂S (3 atoms) and Li₆PS₅Cl (13 atoms) are not directly comparable — a compositional difference is being
read as a volume change, and the sign inverts with the normalization basis. The meaningful quantity is
the volume change of a **balanced reaction** per mole of electrolyte consumed, stating whether the
lithium consumed at the anode is included; the sign of "localized volume expansion" is likewise
undetermined until the system boundary is drawn. **(ii)** Elastic strain energy is said to "exceed the
**fracture toughness** threshold", but strain energy has units of energy while K_IC has units of Pa·m^½.
The fracture criterion is G ≥ G_c or K ≥ K_IC, and the reference quantity is the energy **release rate
per new crack area**, not total stored energy; replacing "fracture toughness" with "critical energy
release rate G_c" corrects this. The underlying size effect is sound (stored energy scales with d³,
crack energy with d²). **(iii)** The quoted K_IC of 0.2–0.4 MPa·m^½ is treated as a material constant,
whereas fracture toughness — unlike elastic moduli — depends strongly on density, grain size,
impurities, pre-existing flaws, and porosity, and is determined per specimen. Giving the specimen
conditions would also supply what the ~3 μm threshold lacks (composition, stack pressure, depth of
discharge): treating K_IC as constant makes the critical size look constant too. Relatedly, the section
uses **two** critical sizes — fracture significant *above* ~3 μm, safety secured *below* 1 μm — which
read as inconsistent unless presented as one trend with their respective conditions.

### Comment 11 — 축 상충 매트릭스 (outlook 로드맵 포함) ★상위 구조 *(B1·A22·A6·A24)* 🔗흡수

A single bond characteristic — the covalent, polarizable P–S bond — is cited with **opposite signs**
across the review: as the weakness in Section 3.1 (low bond energy, high polarizability, water attack)
and as a strength in Section 3.3 (high decomposition temperature) and Section 3.5 (low modulus, plastic
deformation, good contact). Several remedies likewise improve one axis at another's expense: oxygen
incorporation raises air and thermal stability but lowers ionic conductivity; particle-size reduction
aids mechanics but worsens air and solvent stability; polymer compositing raises toughness but dilutes
conductivity. Each section's outlook **already flags its own trade-off** with a "while maintaining …"
clause, so the information is present but dispersed.

Consolidating it into a single **cross-axis trade-off table** (stability axis against remedy, with the
sign on each other axis) would convert scattered caveats into the review's most useful synthesis, at no
additional data cost. In the same spirit, the closing outlooks of Sections 3.1 and 3.3 list desiderata
without distinguishing what is already partly addressed from what remains open; appending the current
state and the remaining gap to each would turn them from wish-lists into a roadmap. One instance ties
both together: Section 3.4 requires the interphase to combine high ionic with low electronic
conductivity, while Section 3.5 identifies the same product set (notably Li₃P) as the driver of volume
mismatch and stress — the requirement that a passivation layer be **simultaneously electronically
insulating and volumetrically compatible** is stated nowhere.

### Comment 12 — 화학–역학 되먹임 고리 모식도 ★부가가치 최대 *(A59·B6)*

The manuscript already contains every element of the chemo-mechanical feedback loop but never closes it:
interface reaction leads to volume mismatch (Section 3.5), then tensile stress (Section 3.5), then
cracking and fracture (Section 3.5), which in turn cause passivation breakdown through exposure of fresh
surface (Section 3.4), lithium penetration and short circuit (Sections 3.5 and 5.1.1), and disruption of
the conduction network (Section 3.5). **The only missing arrow is "fresh surface → reaction restart."**
Drawing this as a single schematic would close the loop and answer directly why degradation accumulates
each cycle, as implied by the phrase "during cycling" in Section 3.5. Because it requires only a
reorganization of existing content rather than new data, its value relative to cost is high.

---

## 📊 압축 결과

| | 원본 | v2 |
|---|---|---|
| 코멘트 수 | 17 | **12** |
| 반박당하는 대목 | 1 (Comment 11 두 번째 문단) | **0** |
| 원고 내부 수치 불일치 지적 | 0 | **1** (3 μm ↔ 1 μm) |
| 절 연결(§3.4↔§3.5↔§5.1) 지적 | 3곳 분산 | **1개로 통합** |

**강도 분포** — 🟩 사실/정의 오류·절간 모순 **8** (1·2·3·5·6·7·9·10) · 구조 제안 **3** (8·11·12) ·
조건 요구 **1** (4). 김동석(§2) 6개 · 배영진(§4) 9개 대비 **§3 이 5개 소절**임을 감안하면 균형이 맞는다.

**절대 빼면 안 되는 것**: Comment 1(P⁵⁺ 모순) · Comment 3(network 모순) · Comment 6("true" 창) ·
Comment 8(chempot gradient) · Comment 10-(ii)(차원 — 객관적이라 반박 불가) · Comment 11·12(구조).

**더 줄여야 한다면 순서**: Comment 4 → Comment 2 → Comment 5 후반부(bond energy).
⚠ Comment 5 전반부(InF₃ 오인용)는 **사실 오류**라 남긴다.
