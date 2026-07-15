# Literature Archive — Dry-Process / Solvent-Free All-Solid-State Battery Electrodes

**Scope:** solvent-free / dry electrode processing for ASSBs (and dry Li-ion as
methodological precedent): PTFE binder fibrillation, carbon-binder domain (CBD)
morphology, sulfide (Li6PS5Cl / argyrodite) + NMC811 composite cathodes,
conductive-additive shape effects (VGCF fibre vs Super-P aggregate), and how dry
vs wet processing changes porosity / tortuosity / σ_ionic / σ_electronic /
contact mechanics.

**Why this archive exists for our project:** our framework is **DEM = transport**
(contact network → σ_ionic/σ_e/σ_thermal via Kirchhoff/Holm) **+ MPM = mechanics**
(plastic SE shape change, morphology, void-fill). Dry-process electrodes are the
real manufacturing target, and the PTFE-fibrillation literature is the closest
external analog to a possible **MPM extension for PTFE fibril drawing** (our
hypothesised `d ∝ √(V/L)` fibril-diameter law: diameter set by the volume of
binder `V` drawn out over a fibril length `L`). The VGCF-vs-Super-P literature
directly bears on our **DEM electronic-bridging** finding (1D fibre additive
percolates at far lower loading than 0D aggregate carbon black).

**Created:** 2026-06-25.
**Method note / data confidence:** the agent proxy blocked most publisher and
repository full-text (HTTP 403 on ScienceDirect, RSC, MDPI, PMC, Nature,
Frontiers, ChemRxiv, Oxford ORA). All quantitative values below are from
**web-search snippets + abstracts + publisher landing pages**. Values are tagged
**[VERIFIED]** when a specific number appeared verbatim in a retrieved
abstract/snippet, or **[BALLPARK]** when paraphrased / approximate. Every paper
is cited with its DOI/URL. Full-text re-extraction is recommended on the user's
machine (where publisher access may differ) for any number that will go into a
paper.

---

## Summary table of papers

| # | Short title | Year | Journal / DOI | System (SE + CAM + additive) | Method | Relevance to our DEM(transport)+MPM(morphology) model |
|---|-------------|------|---------------|------------------------------|--------|--------------------------------------------------------|
| P1 | Solvent-free NMC: unravelling PTFE nano-fibril network (Oxford/Faraday) | 2023 | Front. Energy Res. 11, 1336344 — 10.3389/fenrg.2023.1336344 | NMC622 + PTFE + C65 (Li-ion) | Exp. FIB-SEM / TEM + formation mechanism | ★ Direct PTFE fibril HIERARCHY + diameters; closest external analog to MPM fibril-drawing `d∝√(V/L)` |
| P2 | Multiscale rational design of PTFE fibrillation (FEM+GPR+Bayes) | 2025 | Commun. Mater. 6 — 10.1038/s43246-025-01046-0 | NMC (Li-ion), 10–5 µm bimodal | **Simulation (FEM) + GPR + Bayesian opt.** | ★★ FEM of strain-dependent fibrillation; bimodal + particle-loaded pressure — a *continuum* sibling to our MPM/DEM |
| P3 | Dual-fibrous PTFE thick dry electrode (DDE) | 2025 | Energy Environ. Sci. 18, 8446–8461 — 10.1039/D5EE03240G | NMC (Li-ion), thick | Exp. multi-step grind+knead | PTFE "rope" (intertwined fibres) + fibre hierarchy; 10.1 mAh/cm²; over-binding morphology |
| P4 | Impact of binder content on fracture & microstructure | 2025 | J. Mater. Chem. A — 10.1039/D5TA01950H | NMC + PTFE 0.5–4 wt% (Li-ion) | Exp. FIB-SEM + low-dose TEM of single fibrils | ★ Over-fibrillation → PTFE agglomerate film → pore-blocking; binder>2wt% → particle fracture |
| P5 | Active-material morphology effect on PTFE fibrillation | 2025 | Powder Technol. 451, 120451 — 10.1016/j.powtec.2024.120451 | graphite / LFP / NCM + PTFE (Li-ion) | Exp. + uniaxial compression | Particle shape governs fibrillation rate & film thickness — links AM morphology→CBD (our DEM packing) |
| P6 | Optimization of PTFE fibrillation in dry ASSB cathodes | 2025 | J. Power Sources 17616 — 10.1016/j.jpowsour.2025.17616 | Sulfide ASSB cathode + PTFE | Exp. kneading-time sweep | ★ Optimal vs over-fibrillation trade-off; 195.7 mAh/g; R2R-scalable |
| P7 | Cryo-pulverized PTFE dry-film ASSB | 2024 | Chem. Eng. J. 487, 150221 — 10.1016/j.cej.2024.150221 | Sulfide SE + NMC + PTFE (few-µm) | Exp. | ★ PTFE particle size → both σ_ionic & σ_e (insulating-phase fraction); 188 mAh/g, 90.4% @100cyc |
| P8 | Overcoming binder limitations — solvent-free dry-film sheet cathode | 2019 | Energy Storage Mater. 24, 247 — 10.1016/j.ensm.2019.05.033 | Sulfide SE + NCM + PTFE | Exp. | ★ Binder as low as 0.1 wt%; fibrous PTFE minimizes AM surface coverage → preserves conduction paths; 6.5 mAh/cm² |
| P9 | Long-cycle ASSB by solvent-free SE + cathode films | 2023 | Chem. Eng. J. 451, 138588 — 10.1016/j.cej.2022.138588 | Sulfide SE film + cathode film + PTFE | Exp. | All-dry: 40 µm SE film + 60 µm cathode; 91.4%@100 / 86.4%@1000 cyc |
| P10 | Percolation of sulfide-electrolyte / carbon-additive matrix | 2023 | Batteries 9, 595 — 10.3390/batteries9120595 | Li6PS5Cl + C65 | Exp. (σ_eff vs wt%) | ★ Electronic percolation threshold p_c ≈ 4 wt% C65 — anchor for our DEM σ_e percolation |
| P11 | Conductive-additive morphology & crystallinity (Ni-rich sulfide ASSB) | 2023 | PMC10708284 (Batteries/MDPI family) | Ni-rich CAM + sulfide SE + CNF/CB/CNT | Exp. | ★ High-crystallinity 1D CNF best σ_e & lowest impedance vs 0D CB / CNT |
| P12 | Super-P vs VGCF conductive additives (Li-ion cathodes) | 2015 | RSC Adv. 5, 95073 — 10.1039/C5RA19056H | LiCoO₂/LFP/NMC622 + Super-P / VGCF | Exp. | ★★ Quantifies the 1D-fibre vs 0D-aggregate bridging our DEM SuperP-vs-VGCF finding rests on |
| P13 | Correlation: porosity / mechanics / σ_e / kinetics of dry electrodes (ORNL) | 2023 | J. Power Sources 580, 233422 — 10.1016/j.jpowsour.2023.233422 | NMC811 dry-processed (Li-ion) | Exp. compression sweep | Intermediate porosity ~32% optimal; over-densification → NMC secondary-particle fracture |
| P14 | Dry electrode technology — review (industrialization) | 2022 | Matter 5, 876 — 10.1016/j.matt.2022.01.011 | Review (incl. sulfide ASSB) | Review | Foundational dry-process review; porosity/process landscape |
| P15 | High-loading dry-electrode for ASSB — review | 2025 | Electrochem. Energy Rev. 8 — 10.1007/s41918-025-00240-5 | Review (ASSB) | Review | Nanoarchitectonics + high-loading strategies; ASSB-specific framing |
| P16 | Advances & challenges in dry electrode process for SSBs — review | 2025 | J. Solid State Electrochem. — 10.1007/s10008-025-06518-4 | Review (SSB) | Review | Survey of dry-process challenges; sulfide-solvent incompatibility motivation |
| P17 | Paving the way: dry electrode technology for next-gen ASSBs — review | 2025 | Adv. Mater. — 10.1002/adma.202506123 | Review (ASSB) | Review | Recent ASSB dry-electrode review (Mun et al.) |
| P18 | Dry-film cryo-PTFE / electrochemical stability of SE dry films | 2026 | Adv. Funct. Mater. — 10.1002/adfm.202518517 | Sulfide SE dry film + PTFE | Exp. | Electrochemical stability of dry sulfide SE film (Rosner) — degradation context |

(Supporting / context-only entries continue below the per-topic sections.)

---

## TOPIC 1 — Dry electrode processing & PTFE binder fibrillation

### P1 — Solvent-free NMC electrodes: unravelling the PTFE nano-fibril network ★ KEY
- **Authors / venue:** Oxford / Faraday Institution group. *Frontiers in Energy
  Research* **11**, 1336344 (2023). DOI **10.3389/fenrg.2023.1336344**.
  Preprint: ChemRxiv 10.26434/chemrxiv-2023-1tb6m.
- **System:** Li(Ni0.6Co0.2Mn0.2)O₂ (**NMC622**) + **PTFE** binder + **C65**
  carbon (Li-ion, but the fibril physics transfers directly).
- **KEY quantitative — the fibril HIERARCHY** [VERIFIED from abstract]:
  - **Primary fibrils:** a few **µm in diameter**, **100s of µm in length**.
  - These **branch** into **secondary** fibrils, then into **ever-finer
    fibrils down to 10s of nm in diameter or below** (nano-fibrils).
  - Forms a 3D fibril net that **enmeshes particles**, fibrils "anchored" to
    particle surfaces at numerous points [VERIFIED/BALLPARK].
  - The finest fibrils **survive typical cathode cycling** conditions [VERIFIED].
- **Mechanism:** the paper *presents a formation mechanism for the branch-like
  morphology* of PTFE in solvent-free electrodes [VERIFIED that a mechanism is
  given; the equations/derivation are in the blocked full text].
- **Method:** experimental — FIB-SEM, TEM; slurry-cast vs solvent-free comparison.
- **★ Relevance to our model (MPM fibril drawing `d∝√(V/L)`):** This is the
  **single most relevant external paper**. The hierarchy (µm primary →
  10s-nm nano) is exactly the diameter cascade an MPM/continuum drawing model
  would have to reproduce: each branching event draws a *sub-volume* of binder
  into a thinner, longer fibril. If our `d ∝ √(V/L)` holds (volume conservation
  in a cylinder: `V = π(d/2)²L → d = 2√(V/πL)`), then **going from a primary
  fibril (few µm) to a nano-fibril (10s nm) is a ~100× diameter drop → ~10⁴×
  drop in `V/L`** — consistent with a branch splitting off a tiny binder volume
  and drawing it far. **This paper neither confirms nor contradicts the exact
  √ law** (no closed-form diameter-vs-draw equation in the snippet), but its
  measured diameter cascade is the data any such law must fit. **ACTION:**
  re-fetch full text (ChemRxiv preprint) on user's machine to read the stated
  formation mechanism and check for a quantitative draw/diameter relationship.

### P6 — Optimization of PTFE fibrillation in dry ASSB cathodes ★ KEY (sulfide)
- **Venue:** *Journal of Power Sources* (2025), article S0378775325017616 →
  DOI **10.1016/j.jpowsour.2025.17616** (verify exact article number).
- **System:** **sulfide-based ASSB cathode** + PTFE binder (sulfide SE; specific
  SE/CAM not captured in snippet — likely argyrodite + NMC).
- **KEY quantitative** [VERIFIED]:
  - Fibrillation degree controlled via **kneading time 10 → 120 min**.
  - **Optimized electrode: 195.7 mAh/g** discharge capacity + excellent rate.
  - **Excessive fibrillation weakened tensile strength** (over-fibrillation
    trade-off); optimal fibrillation = best electrochemical performance.
  - Achieved with **only a few calendering cycles** → scalable **roll-to-roll
    (R2R)** (vs lab-scale fold-and-calender).
- **Method:** experimental kneading-time / fibrillation sweep.
- **Relevance:** Confirms a **non-monotonic optimum** in fibrillation degree for
  a *sulfide* system — under-fibrillation = poor binding/network, over-
  fibrillation = mechanical loss (and, per P3/P4, pore-blocking). Directly
  supports treating fibrillation as a tunable morphology variable (MPM) whose
  optimum trades mechanical integrity against transport pore structure (DEM).

### P7 — Cryo-pulverized PTFE dry-film ASSB ★ KEY (sulfide, transport)
- **Authors / venue:** Sungkyunkwan Univ. group. *Chemical Engineering Journal*
  **487**, 150221 (2024). DOI **10.1016/j.cej.2024.150221**.
- **System:** **sulfide SE + NMC** cathode + **PTFE** binder, particle size
  tuned by **cryogenic pulverization**.
- **KEY quantitative** [VERIFIED]:
  - Tuning PTFE particle size to **a few µm** enhanced **BOTH ionic and
    electronic conduction** by **reducing the insulating-component contribution**
    in the composite cathode.
  - **188 mAh/g @ 0.2C**; **90.4% capacity retention after 100 cycles** at
    **3.0 mA/cm²**.
  - Even binder distribution maintained tight component contact after cycling.
- **Method:** experimental.
- **★ Relevance to our model:** Frames PTFE explicitly as an **insulating phase**
  whose *spatial distribution* (set by particle size / fibrillation) controls how
  much it blocks ionic and electronic paths. This is exactly a **DEM transport**
  problem: PTFE = insulating obstacles in the contact network. Smaller/finer PTFE
  → less path-blocking → higher σ. Mirrors our finding that conduction is set by
  the contact-network geometry, not bulk fractions alone.

### P9 — Long-cycle ASSB via all-solvent-free SE + cathode films (sulfide)
- **Venue:** *Chemical Engineering Journal* **451**, 138588 (2023). DOI
  **10.1016/j.cej.2022.138588**.
- **System:** **sulfide SE film + cathode film**, both via fibrillized **PTFE**.
- **KEY quantitative** [VERIFIED]:
  - SE film **~40 µm**, cathode film **~60 µm** (both solvent-free).
  - **91.4% retention @ 100 cycles; 86.4% @ 1000 cycles** (ultra-long life).
  - PTFE fibres bind components, **do not interact with SE/CAM**, electrochemically
    stable at high voltage.
- **Relevance:** Demonstrates dry processing's headline advantage for sulfides
  (no solvent → no SE degradation). Film thicknesses (40/60 µm) are realistic
  targets for matching our compaction/thickness outputs.

### P8 — Overcoming binder limitations: solvent-free dry-film sheet cathode ★ KEY
- **Authors / venue:** Fraunhofer group. *Energy Storage Materials* **24**, 247
  (2019). DOI **10.1016/j.ensm.2019.05.033**.
- **System:** **sulfide SE + NCM** sheet-type cathode + **fibrous PTFE**.
- **KEY quantitative** [VERIFIED]:
  - Binder reduced to **as low as 0.1 wt%** (lowest reported at the time).
  - **Significantly reduced impedance below 0.7 wt%** binder.
  - Free-standing NCM sheets at **6.5 mAh/cm²** match the rate of binder-free
    electrodes at 2.5 mAh/cm².
  - **Fibrous PTFE chosen to reduce AM surface coverage** — binder can "block the
    surface of the active material and cut conduction pathways".
- **★ Relevance to our model:** The explicit physical claim — *binder coverage of
  the AM surface cuts conduction pathways* — is precisely our **coverage / contact
  network** logic (Stage-E coverage of AM by SE; Tabor area). A fibrous (1D) PTFE
  network covers **less** AM surface per unit binding than a film/coating binder,
  preserving the AM–SE and AM–AM contacts our DEM solver needs. This is the
  binder-side analog of the VGCF-vs-CB additive-shape argument (P11/P12).

### P3 — Dual-fibrous PTFE structure (DDE), thick dry electrode
- **Venue:** *Energy & Environmental Science* **18**, 8446–8461 (2025). DOI
  **10.1039/D5EE03240G**. (Cambridge/repository copy exists.)
- **System:** NMC (Li-ion), thick electrode; multi-step grind + knead.
- **KEY quantitative** [VERIFIED]:
  - **Dual-fibrous:** a 2nd kneading step makes a **PTFE "rope"** = multiple
    intertwined PTFE fibres, coexisting with single PTFE fibres → more uniform
    distribution, better σ_e & reaction homogeneity, smoother edge roughness.
  - **10.1 mAh/cm²** areal capacity; **1.2 Ah-class stacked pouch** →
    **349 Wh/kg / 800 Wh/L** (vs Li metal); **80.2% @ 600 cycles** (vs graphite).
- **Relevance:** Introduces a **two-scale fibre architecture** (thin fibres +
  thick ropes). For an MPM fibril model this is a *bimodal fibril-diameter
  distribution* — a thick load-bearing "rope" plus thin networking fibres. Maps
  onto a `d∝√(V/L)` picture with two `V/L` populations (large `V` → rope, small
  `V` → fibre).

### P5 — Active-material morphology effect on PTFE fibrillation
- **Venue:** *Powder Technology* **451**, 120451 (2025). DOI
  **10.1016/j.powtec.2024.120451**.
- **System:** platelet **graphite** / spherical porous **LFP** / spherical
  **NCM** + PTFE (Li-ion).
- **KEY quantitative / findings** [VERIFIED/BALLPARK]:
  - **Graphite (platelet)** *slows* PTFE fibrillation; **LFP (fine particles)**
    *prolongs* fibrillation; **NCM (dense, fast compaction)** *promotes faster*
    fibrillation during mixing.
  - Uniaxial compression: **NCM powders need higher compression stress and form
    thicker films**; graphite needs lower stress, thinner films.
  - **"Hierarchical morphology of the fibrils determines the powder blend
    properties."**
- **Relevance:** Couples **AM particle shape/packing (our DEM geometry input)**
  to **fibrillation outcome (MPM morphology output)**. Dense spherical NCM (our
  CAM) both fibrillates PTFE faster and compacts to thicker/denser films — a
  direct AM-shape→CBD coupling.

---

## TOPIC 2 — Carbon-Binder Domain (CBD) morphology, over-fibrillation, pore-blocking

### P4 — Impact of binder content on particle fracture & microstructure ★ KEY
- **Authors / venue:** Oxford group (ORA + ChemRxiv). *Journal of Materials
  Chemistry A* (2025). DOI **10.1039/D5TA01950H**. ChemRxiv
  10.26434/chemrxiv (article 66c0ba3e...).
- **System:** NMC + **PTFE 0.5 → 4 wt%** (Li-ion). First **single-PTFE-nanofibril**
  analysis by ultra-low-dose TEM.
- **KEY quantitative — the over-fibrillation / pore-blocking transition**
  [VERIFIED]:
  - **< 2 wt% PTFE:** PTFE readily fibrillates into **highly textured crystalline
    nano-fibrils**; NMC particles remain **largely intact**; **open structure**,
    high ionic mobility → **superior performance**.
  - **> 2 wt% PTFE:** microstructure → **compact morphology with PTFE
    agglomerates that BLOCK porosity**, plus **extensive NMC particle fracture**
    during calendering (cracks along grains of polycrystalline particles).
  - So increasing 0.5 → 4 wt% transforms **open nano-fibrillar → closed
    agglomerate (film-like) pore-blocked** structure.
- **★ Relevance to our model:** This is the **direct experimental statement of
  "over-fibrillation → film → pore-blocking"** that the topic brief asks about.
  - For **MPM (morphology):** the open-fibril → agglomerate-film transition is a
    morphological state change with binder volume fraction — exactly what a
    plastic-flow / drawing model would predict (too much binder volume → it can't
    all be drawn into thin fibrils → leftover collapses into films/agglomerates).
  - For **DEM (transport):** "porosity blocked by PTFE agglomerates" = insulating
    obstacles closing pore (ionic) channels → σ_ionic drop. The **< 2 wt%
    threshold** is a usable design bound. Also note the **calendering-induced NMC
    fracture** ties to our **Auerbach/Holm fracture** treatment of CAM.

### CBD context (Li-ion, methodological)
- Slurry electrodes: PVDF binder holds fine carbon (e.g. C65) → **carbon-binder
  domain (CBD)** filling inter-particle space. Dry electrodes replace this with a
  **PTFE fibril web + free carbon (Super-P/VGCF/CB)**, giving a *distinct*
  CBD-equivalent: a fibrous, more open conductive network rather than a
  gel-like CBD phase. (Synthesized from P1, P3, multiple search snippets.)
- Carbon black on conductive-binder-domain (CBD) electronic conduction: Yamada
  et al. type studies — *J. Power Sources* (2023) S0378775323012922,
  "Effect of carbon blacks on electrical conduction and conductive binder domain
  of next-generation Li-ion batteries" (DOI 10.1016/j.jpowsour.2023.232922 —
  verify) — CB structure/aggregate size controls CBD percolation. [context]

---

## TOPIC 3 — Sulfide (Li6PS5Cl / argyrodite) + NMC811 composite cathodes & additive shape

### P10 — Percolation of sulfide-electrolyte / carbon-additive matrix ★ KEY anchor
- **Venue:** *Batteries* **9**, 595 (2023, Dec 15). DOI
  **10.3390/batteries9120595** (open access).
- **System:** **Li6PS5Cl + C65** conducting matrix (the SE+carbon sub-system of a
  composite cathode).
- **KEY quantitative** [VERIFIED]:
  - **Electronic percolation threshold p_c ≈ 4 wt% C65** in the Li6PS5Cl+C65
    matrix.
  - Systematic study of microstructure and **effective conductivity σ_eff** vs
    carbon wt%.
  - Trade-off: low-surface-area carbon ↑ rate capability but ↑ SE decomposition →
    carbon fraction must be balanced.
- **★ Relevance to our model:** This is a **direct external anchor for our DEM
  σ_electronic percolation** in the SAME material (Li6PS5Cl). Our σ_e form has an
  AM-percolation backbone; this paper gives the *carbon-additive* percolation
  threshold (~4 wt% C65) in LPSCl, which is the conductive-network half. Useful
  as an independent percolation-threshold cross-check and to motivate the
  additive-shape term (next).

### P11 — Conductive-additive morphology & crystallinity (Ni-rich sulfide ASSB) ★ KEY
- **Venue:** MDPI/Batteries family, PMC10708284 (2023). (Get exact DOI on user
  machine — "The Effect of Conductive Additive Morphology and Crystallinity on
  the Electrochemical Performance of Ni-Rich Cathodes for Sulfide ASSLIBs".)
- **System:** Ni-rich CAM + **sulfide SE** + conductive additives of differing
  **morphology (1D fibre vs 0D particle) and crystallinity**: **CNF vs CB vs CNT**.
- **KEY findings** [VERIFIED]:
  - **High-crystallinity carbon nanofiber (CNF, 1D)** → **excellent σ_e**,
    suppressed polarization, lowest interfacial impedance.
  - **Carbon black (CB) and CNT** → relatively **lower** performance in sulfide
    ASSB cathodes.
- **★ Relevance to our model (SuperP-vs-VGCF electronic bridging):** **Directly
  supports** our DEM finding that a **1D fibre additive bridges the electronic
  network far more efficiently than a 0D aggregate**. CNF/VGCF (high aspect ratio)
  spans gaps between CAM particles that point-like CB cannot. This is the
  *physics* our DEM contact-network solver encodes (long fibre = many contacts /
  long-range connectivity at low loading).

### P12 — Super-P (CB) vs VGCF conductive additives ★★ KEY (quantitative shape)
- **Authors:** Inseong Cho, Jaecheol Choi, Kyuman Kim, Myung-Hyun Ryou, Yong Min
  Lee. *RSC Advances* **5**, 95073–95078 (2015). DOI **10.1039/C5RA19056H**
  (open-access copy at Monash research repository).
- **System:** Li-ion cathodes **LiCoO₂ / LiFePO₄ / NMC622** + **Super-P** vs
  **VGCF** (also their synergy).
- **KEY quantitative — additive shape** [VERIFIED]:
  - **Super-P:** powdery, **~40 nm** average particle size (0D aggregate).
  - **VGCF:** pillar-like, **~150 nm diameter × ~15 µm length** (1D fibre, aspect
    ratio ~100).
  - **VGCF gives the highest electrical conductivity for LiCoO₂ and LiFePO₄**
    (single-particle CAMs) — the fibre **efficiently connects to active material**.
  - For **NMC622** (µm secondary particles of nano primaries), **VGCF + Super-P
    mixture** is best (synergy: fibre for long-range, CB to fill local gaps).
- **★★ Relevance to our model:** This is the **quantitative backbone of the
  SuperP-vs-VGCF electronic-bridging finding**. It gives real geometry (40 nm CB
  vs 150 nm × 15 µm VGCF) and the rule: **1D fibre wins for large single-particle
  CAM; a fibre+aggregate blend wins for hierarchical secondary-particle CAM**.
  For our DEM σ_e additive-shape term: a high-aspect-ratio fibre should be modeled
  as a long multi-contact bridge (low percolation threshold), whereas CB is a
  short-range point filler. **No contradiction** — fully consistent with our
  finding. Worth using the 40 nm / 150×15000 nm numbers if we add an explicit
  additive-aspect-ratio parameter.

### Related percolation-threshold context (additives)
- "Carbon nanofiber networks have **no theoretical percolation threshold** and
  reach good macroscopic σ_e at **< 1 wt%**, whereas conventional CB needs
  **≥ ~5 wt%**" [BALLPARK, from CNF/CB hybrid-dispersion search snippets, e.g.
  aqueous CB+CNF hybrid PMC9086548]. This is the broad rule behind P11/P12 and
  the additive-shape lever for our DEM transport model.

### Sulfide composite cathode compaction / pressure–porosity–conductivity (context)
- **Cold-pressing / densification of Li6PS5Cl** [VERIFIED from search snippets]:
  - Threshold **~350 MPa** where σ_ionic significantly increases & maximum
    densification for Li6PS5Cl.
  - At **~590 MPa**, porosity drops **50% → 3–12%** (separator-dependent).
  - **Above ~500 MPa, σ_ionic decreases** (lattice contraction, higher Li⁺
    migration barrier).
  - Decompression → **irreversible σ_ionic enhancement** (plastic densification +
    structural disorder). Densification is two-stage: intergranular pore closure
    then intragranular. (Refs: Thompson et al., *Adv. Funct. Mater.*
    10.1002/adfm.75195; "Uni-axial densification of slurry-cast Li6PS5Cl tapes"
    PMC12306411; UCSD Liu group surface-lubrication 2025.)
- **★ Relevance:** These are **independent experimental porosity-vs-pressure
  anchors for Li6PS5Cl** — directly comparable to our DEM/MPM compaction targets
  (our Minnmann anchor ~10% @ 300 MPa sits right in this band; the 350 MPa
  conductivity knee ≈ our Heckel knee P_y ≈ 138 MPa region; >500 MPa σ-decrease
  is a regime our elastic models do *not* capture and should be flagged).
- **DEM simulation of ASSB cathode compaction (coated particles):** *J. Power
  Sources* (2022) S0378775322002968 (DOI 10.1016/j.jpowsour.2022.231464 —
  verify) — DEM of cold-pressing coated CAM particles; frictional interactions
  dominate connectivity/percolation/porosity. [Already in our litdb family;
  related to Bazzoun/Varkey entries.]
- **Contact model for DEM of compaction & sintering of ASSB electrodes:**
  PMC9513599 (2022) — DEM contact-mechanics model, complements our hooke/
  hysteresis + Stage-E. [context, DEM-side]

---

## TOPIC 4 — Dry vs wet processing: porosity / tortuosity / σ / mechanics

### P13 — Correlation of porosity / mechanics / σ_e / kinetics of dry electrodes (ORNL) ★
- **Venue:** ORNL. *Journal of Power Sources* **580**, 233422 (2023). DOI
  **10.1016/j.jpowsour.2023.233422** (OSTI 1994691).
- **System:** **NMC811** dry-processed cathodes (Li-ion).
- **KEY quantitative** [VERIFIED]:
  - **Intermediate porosity ~32%** → **lowest charge-transfer resistance, highest
    σ_e, best rate** (mirrors slurry electrodes).
  - **Reducing porosity (over-compression) → more NMC secondary-particle
    fracture.**
- **★ Relevance to our model:** Gives a **porosity sweet-spot (~32%)** for Li-ion
  dry electrodes and the **over-densification → fracture** failure mode — both
  align with our DEM/MPM picture: too much compaction fractures CAM (Auerbach/
  Holm) and does not keep improving transport. The fracture-vs-porosity coupling
  is exactly our brittle-CAM treatment.

### Dry-vs-wet porosity & tortuosity (synthesized, multiple sources) ★
- **Wet/slurry porosity** without calendering can be **~56%** (solvent
  evaporation leaves voids) [BALLPARK].
- **Dry-process electrodes** avoid solvent-evaporation voids → can reach **lower
  porosity** (dry spray deposition cited as **−4% to −10%** porosity vs slurry)
  [BALLPARK].
- **Tortuosity:** higher porosity → higher ionic tortuosity → worse performance;
  an **appropriate SE volume fraction** is fundamental to reduce electrode ionic
  tortuosity [VERIFIED qualitatively].
- **Sulfide-specific motivation:** sulfide SEs exposed to polar slurry solvents
  **lose σ_ionic to ~1/100 or less** (dissolution/degradation) → dry process is
  *strongly preferred* for sulfides [VERIFIED]. (Refs: dry-process reviews P14–
  P17; "Drying process of sulfide-based ASSB components" Singer 2023 *Energy
  Technol.* 10.1002/ente.202300098; "Influence of slurry composition on thin-film
  components" 2023.)
- **★ Relevance:** Quantifies the dry vs wet porosity gap our compaction models
  could be asked to reproduce, and pins the **SE-volume-fraction ↔ tortuosity**
  link that our σ_ionic percolation form already encodes (φ_eff, τ terms).

### P2 — Multiscale rational design of PTFE fibrillation (FEM + GPR + Bayes) ★★ KEY MODEL
- **Authors / venue:** Sung Beom Cho, Junghyun Choi, Jun Hyuk Kang, ... Patrick
  Joohyun Kim, Taeseup Song, Laisuo Su et al. *Communications Materials* **6**
  (Dec 2025). DOI **10.1038/s43246-025-01046-0**. (Also SSRN preprint
  abstract_id 5293697, titled "...Rational Design of PTFE Fibrillation in Dry
  Electrodes...".)
- **System:** NMC dry electrode (Li-ion); PTFE fibrillation; **10–5 µm bimodal
  particle system**.
- **KEY quantitative / method** [VERIFIED]:
  - **Multiscale framework = FEM simulations + Gaussian Process Regression +
    Bayesian optimization** to engineer PTFE fibrillation.
  - **Captures the strain-dependent fibrillation characteristics of PTFE** and
    microscale particle dynamics.
  - **Optimal:** a **10–5 µm bimodal system with 14 MPa particle-loaded pressure**
    yields the most effective fibrillation.
  - Demonstrated dry electrodes with uniform microstructure and **10 mAh/cm²**.
- **★★ Relevance to our model — this is the closest *simulation* sibling:**
  - It is a **continuum/FEM model of strain-driven PTFE fibrillation**, i.e. the
    *mechanics half* (our MPM territory) of dry-electrode morphology. **A strong
    candidate to compare our (hypothetical) MPM PTFE-drawing model against.**
  - Its "**strain-dependent fibrillation**" is conceptually our **plastic-strain
    field** driving shape change. If our `d∝√(V/L)` law is volume-conservation
    under drawing, their FEM strain-fibrillation relation is the field-level
    version — **re-fetch full text to check whether they report a
    fibril-diameter-vs-strain (or vs draw-ratio) relationship that we can test
    `d∝√(V/L)` against.** This is the **#1 follow-up**: it could directly
    validate or contradict the drawing law.
  - The **bimodal (10–5 µm) + particle-loaded-pressure (14 MPa)** optimum maps
    onto our bimodal CAM/SE packing + compaction-pressure framing (DEM packing
    geometry × applied pressure). 14 MPa here is the *fibrillation/mixing*
    pressure (≪ the 300–600 MPa final *densification* pressure), an important
    distinction to keep.

---

## Reviews & broader context

- **P14 — Dry electrode technology, the rising star in SSB industrialization.**
  *Matter* **5**, 876–904 (2022). DOI 10.1016/j.matt.2022.01.011 (Cell, full text
  also at cell.com S2590-2385(22)00011-X). Foundational dry-process review;
  process/porosity landscape; Tesla/Maxwell PTFE-fibrillation context.
- **P15 — High-loading dry-electrode for ASSB: nanoarchitectonics.** *Electrochem.
  Energy Rev.* **8** (2025). DOI 10.1007/s41918-025-00240-5. ASSB-specific high-
  loading dry-electrode strategies.
- **P16 — Advances & challenges in dry electrode process for SSBs.** *J. Solid
  State Electrochem.* (2025). DOI 10.1007/s10008-025-06518-4.
- **P17 — Paving the way: dry electrode technology for next-gen ASSBs** (Mun et
  al.). *Adv. Mater.* (2025). DOI 10.1002/adma.202506123.
- **P18 — Analysis of electrochemical stability of sulfide SE dry films** (Rosner
  et al.). *Adv. Funct. Mater.* (2026). DOI 10.1002/adfm.202518517.
- **Other recent (2025–2026) dry-electrode / fibrillation mechanism papers seen in
  search** (full details not extracted — candidates for next pass):
  - "Solvent-Free Bonding Mechanisms and Microstructure Engineering in Dry
    Electrode Technology" (Liang et al.), *Adv. Funct. Mater.* 2026,
    10.1002/adfm.202518619 — review of bonding/fibrillation mechanisms.
  - "Dry-film technology employing cryo-pulverized PTFE..." = **P7** (above).
  - "Dry-processed electrodes enabled by PTFE fibrillation for high-performance
    Li-ion batteries," *Prog. Mater. Sci.*-type review 2026, S0079642526000216.
  - "Materials- and process-driven microstructural engineering for scalable
    dry-processed electrode manufacturing," *Mater. Horiz.* 2026,
    10.1039/D5MH02484F.
  - "Sustainable & cost-effective roll-to-roll dry coating," *Chem. Sci.* 2025,
    10.1039/D5SC00059A.
  - "Dry Process for Green Manufacturing: structural evolution of freestanding
    film during R2R," *Int. J. Precis. Eng. Manuf.-Green Tech.* 2026,
    10.1007/s40684-026-00885-7.

### PTFE fibrillation MECHANICS literature (non-battery, for the drawing model) ★
These bear directly on whether our `d ∝ √(V/L)` drawing law is physically grounded:
- **PTFE paste extrusion fibrillation model:** Patil/Seth/Pol et al.,
  "Polytetrafluoroethylene Paste Extrusion: A Fibrillation Model and Its Relation
  to Mechanical Properties," *Int. Polym. Process.* (2011), DOI 10.3139/217.2744;
  and "Constitutive modeling and flow simulation of PTFE paste extrusion,"
  *J. Non-Newtonian Fluid Mech.* (2006/2007), DOI 10.1016/j.jnnfm.2006.11.005 /
  10.1016/j.jnnfm.2007.05.010. **A first-order kinetic structural parameter**
  (fraction fibrillated) evolves with **strain rate and flow-type parameter**
  (strain vs rotation). [VERIFIED from snippet]
- **Shear-activated fibrillation in PTFE** (preprint 2024, Research Square
  10.21203/rs.3.rs-9203898/v1): incremental **extension testing** shows
  **sustained tensile load during progressive separation → fibrillar drawing &
  crystalline "unzipping" rather than elastic fracture** [VERIFIED]. Supports the
  *drawing* picture (fibrils pulled/drawn, conserving material) underlying √(V/L).
- **In-situ fibrillated PTFE composites:** well-dispersed long-aspect-ratio PTFE
  **nanofibrils with diameter < 200 nm**; **shear rate is the key parameter** for
  PTFE morphology evolution [VERIFIED]. (e.g. *Compos. Part B* / *Polymer*
  in-situ-fibrillation studies, 10.1016/j.matdes.2021.110201 — verify.)
- **★ Relevance:** The PTFE-process literature consistently says fibrillation is
  **shear/strain-rate-driven drawing** (not fracture), with diameter shrinking as
  drawing proceeds — qualitatively **consistent with `d∝√(V/L)`** (more draw →
  longer `L` at fixed `V` → smaller `d`). **None of the retrieved snippets give a
  closed-form `d(V,L)` law**, so the √ exponent is *not yet externally confirmed
  or refuted*; the strongest test is P2 (FEM strain-fibrillation) + P1 (measured
  diameter cascade). **FLAG:** treat `d∝√(V/L)` as physically motivated but
  externally **unvalidated on the exponent** until P1/P2 full texts are read.

---

## Direct verdicts on our model's two specific claims

1. **PTFE `d ∝ √(V/L)` fibril-drawing model**
   - **Supporting (qualitative):** P1 (µm→10s-nm diameter cascade via branching),
     P3 (thick rope + thin fibre = bimodal `V/L`), PTFE-extrusion + shear-
     fibrillation mechanics (drawing, not fracture; diameter shrinks with draw).
   - **Neither confirms nor contradicts the √ EXPONENT:** no retrieved source
     gives a closed-form diameter-vs-draw/volume law. **Verdict: physically
     plausible, exponent externally UNVALIDATED.** Best external tests to run:
     **P2** (FEM strain-dependent fibrillation — check for diameter vs strain/draw)
     and **P1/P4** (measured single-fibril diameters vs binder fraction / branch
     generation). No contradicting evidence found.

2. **Super-P (0D) vs VGCF (1D) electronic-bridging finding**
   - **Strongly SUPPORTED, no contradiction:** P12 (VGCF 150 nm×15 µm beats 40 nm
     Super-P for single-particle CAMs; blend best for hierarchical NMC), P11 (1D
     high-crystallinity CNF beats 0D CB and CNT in *sulfide ASSB*), plus the
     general rule (CNF percolates <1 wt% vs CB ≥~5 wt%). P10 gives the LPSCl+C65
     percolation anchor (~4 wt%). **Verdict: our DEM additive-shape/electronic-
     bridging conclusion is corroborated by independent experiment, including in
     the same sulfide material class.** Caveat: for *hierarchical secondary-
     particle* CAM (like real NMC811), a **fibre+CB blend** can beat pure fibre —
     worth representing if we add an explicit additive-morphology term.

---

## Open follow-ups / re-fetch list (publisher 403 blocked these on the proxy)
Priority order for full-text extraction on the user's machine:
1. **P2** Commun. Mater. 2025 (10.1038/s43246-025-01046-0) + SSRN 5293697 —
   FEM strain↔fibrillation; look for diameter-vs-strain/draw law to test √(V/L).
2. **P1** Front. Energy Res. 2023 / ChemRxiv 10.26434/chemrxiv-2023-1tb6m —
   the stated PTFE branch-formation mechanism + exact primary/secondary/nano
   diameters and lengths.
3. **P4** J. Mater. Chem. A 2025 (10.1039/D5TA01950H) / ChemRxiv — single-fibril
   TEM diameters vs binder wt%; the <2 wt% open ↔ >2 wt% film transition data.
4. **P10** Batteries 9, 595 (open access) — full σ_eff(wt%) curve + exact p_c.
5. **P12** RSC Adv. 2015 (Monash OA copy) — full σ_e numbers for CB vs VGCF vs blend.
6. **P6 / P7 / P9** sulfide dry-cathode papers — exact SE/CAM/additive recipes,
   porosity, σ values.

---

*End of archive. Created 2026-06-25 by literature-research agent. All values
search-snippet/abstract level unless a primary full text is later substituted;
re-verify [BALLPARK] tags before paper use.*
