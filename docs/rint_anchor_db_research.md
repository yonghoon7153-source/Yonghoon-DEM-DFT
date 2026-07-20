# Phase 0 — R_int/EIS/cycling 앵커 조사 결과 (2026-07-20)

워크플로 rint-anchor-db-research(7 agents) 산출.  ⚠ snippet 숫자는 confirmed_snippet(웹검색) 수준 —
PDF 검증(WSL 로컬 egress)은 별도.  프로젝트: docs/project_rint_fullcell_cycling.md Phase 0.

# Anchor-DB Plan for ASSB (NMC811 + LPSCl) R_int / Cycling Modeling

**Scope:** Prioritize open datasets, digitizable literature anchors, and DB tooling for an interfacial-resistance (R_int) / EIS / cycling anchor database to feed the DEM Kirchhoff/Holm transport pipeline, STEP4 discharge modeling, and the cycling-degradation (frame[5] MPM-mechanics) track. All numbers below are quoted **only** from the supplied findings; unverified snippet-level numbers are tagged. Repo hooks already present are noted so this plan builds on, not duplicates, existing code.

**One-line verdict:** No open bulk dataset closes the R_int loop for our exact system. Treat **OBELiX + LiIonML** as the σ_ion (σ_grain) anchor, **CAMP + Mendeley-relaxation** as the NMC811 electrochemical baseline, **Nature Energy 2024 (Zenodo)** as the ASSB cycling/window anchor, and **NASA/CALCE** as EIS-extraction method validation only — then keep a **manual, DOI-linked litdb pipeline** (digitized R_int/EIS per paper) as the authoritative interfacial anchor.

---

## 1. TOP open datasets, ranked by usefulness to us

Ranking is by directness to the NMC811+LPSCl R_int/cycling target (exact-chemistry + open raw > chemistry-matched > method-only).

| # | Dataset | URL | What R_int / EIS / cycling data | Access | Why this rank |
|---|---------|-----|-------------------------------|--------|---------------|
| 1 | **Nature Energy 2024 ASSB reproducibility benchmark** (NMC622-SC / LPSCl / In-Li, 21 labs) | https://www.nature.com/articles/s41560-024-01634-3 · **raw: Zenodo DOI 10.5281/zenodo.15827509** · PDF mirrors https://pure-oai.bham.ac.uk/ws/files/247832371/41560_2024_Article_1634.pdf , https://ora.ox.ac.uk/objects/uuid:96320f7f-f1ea-4f22-bef2-5a2f923ffe4e | Per-cell cycle-dependent specific discharge capacity, CE, polarization voltage, full charge–discharge curves; cycles 1,2,10,20,30,40,50 @0.1C; **initial specific discharge 106–142 mAh/g** inter-lab spread; assembly metadata (P_press, press duration, In:Li). **NO EIS, NO explicit R_int.** | Open, CC-BY; raw CSV on Zenodo | Closest experimental anchor to our system; exact SE+anode, one shared protocol. Directly serves the **PENDING STEP4 discharge-window re-anchor**. Caveat: **CAM = 622-SC, not 811** → tag chemistry for transfer. Terminal V-Q only. |
| 2 | **OBELiX** (599 SSE, RT σ_ion) | https://github.com/NRC-Mila/OBELiX · `pip install obelix-data` · arXiv:2502.14234 · RSC DD 10.1039/D5DD00441A | 599 synthesized SSE w/ measured RT ionic conductivity (S/cm) + composition/space-group/lattice; 321 with CIFs; sulfide/argyrodite families | Fully open, CC-BY-4.0; machine-readable | Primary anchor for LPSCl-family **σ_grain** (our 3.0 mS/cm Cronau value + Cronau(r_SE) factor). Places LPSCl in a measured population. Automated ingestion. |
| 3 | **Liverpool LiIonML** (820 σ_ion entries, T-dependent) | https://github.com/lrcfmd/LiIonML · CSV https://pcwww.liv.ac.uk/~msd30/lmds/LiIonDatabase.html · paper https://www.nature.com/articles/s41524-022-00951-z | 820 entries / 214 sources; AC-impedance σ_ion at stated T (5–873 °C); ~403 unique compositions near RT; **~12% pure sulfides, ~2% halides** | Open (academic-use terms on CSV) | Second independent σ_ion population incl. Li6PS5Cl **with T-dependence** → Arrhenius/thermal anchoring; cross-validates OBELiX. |
| 4 | **CAMP 2023 v3.5** (Argonne, incl. NMC811) | https://acdc.alcf.anl.gov/mdf/detail/camp_2023_v3.5/ · toolkit github.com/ROVI-org/battery-data-toolkit | ~300 cells, 6 chemistries **including NMC811** (graphite anode), ≤1C, ≥100 cycles: capacity, voltage curves, cycle life. **Liquid-cell, not ASSB.** | Open via MDF; standardized files | Best open **NMC811 electrochemical baseline** (chemistry match to CAM). Anchors NMC811 capacity/voltage-shape/rate — the "liquid-cell control" against which ASSB deviations are the solid-interface signature. |
| 5 | **Mendeley NMC811 relaxation/GITT set** | https://data.mendeley.com/datasets/y8nstxmdrg/1 (**DOI 10.17632/y8nstxmdrg.1**) · paper https://www.cell.com/cell-reports-physical-science/fulltext/S2666-3864(23)00599-4 | Commercial NMC811 (+LFP): full MACCOR history, voltage-relaxation series across DoD/rate/T, GITT/ITT. **No EIS.** | Open, CC-BY | Near-equilibrium relaxed V vs SOC → **empirical NMC811 OCP anchor** to replace the Chen2020 graphite-full-cell window (the STEP4 x0/x100 issue). Relaxation-time constants = kinetic priors. |
| 6 | **LiionDB** (DFN parameter DB) | https://github.com/ndrewwang/liiondb · review doi:10.1088/2516-1083/ac692c | Literature OCP functions, D_s, i0 / reaction-rate, transport, geometry with per-paper provenance | Open, MIT | Brackets our STEP4 defaults (D_s 3e-14, i0 2 A/m²) against reported distributions instead of single point-picks. |
| 7 | **Materials Project** (+ computed SSE/interface) | https://materialsproject.org | DFT LPSCl bulk/elastic moduli, NMC/SE interface stability — **not** electrochemical R_int | Open API, CC-BY-4.0 | Material-level priors: LPSCl elastic modulus (feeds E_SE), NMC-SE interfacial thermodynamics (R_int growth context), candidate for the outstanding **E_bind DFT** (SDCP A4′). |
| 8 | **BatteryArchive** (aggregator: SNL, HNEI, …) | https://www.batteryarchive.org · studies /study_summaries.html · SNL https://www.batteryarchive.org/snl_study.html | Harmonized cycling for many studies; **HNEI = 51 NMC-LCO 18650 (2.8 Ah) with periodic EIS**; SNL = 32+ LG 18650HG2 NMC 3Ah over 15/25/35 °C × DoD × C-rate; some EIS. **All liquid, off-chemistry for R_int.** | Open; standardized CSV | Fastest **normalization layer** to pull many NMC cycling sets in one schema; HNEI gives an impedance-vs-SOH template. Trend shapes only, not absolute ASSB R_int. |
| 9 | **NASA PCoE + CALCE** (EIS-vs-aging, LCO) | NASA https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/ · https://data.nasa.gov/dataset/li-ion-battery-aging-datasets · CALCE https://calce.umd.edu/battery-data | 18650/prismatic LCO with periodic EIS (R_e, R_ct) tracked vs aging; NASA "Randomised" = 28 LCO cells w/ EIS | Open (NASA public domain; CALCE academic) | **Method-validation only** (off-chemistry). Clean, documented EIS→R_int template to prototype the equivalent-circuit extraction code path that will later digest ASSB EIS. Tag as non-anchor. |

**Tiering:** #1–3 are true anchors for our exact/adjacent chemistry; #4–6 anchor the NMC811 electrochemical baseline + STEP4 parameters; #7 material priors; #8–9 are normalization + EIS-method scaffolding, explicitly **not** ASSB R_int anchors.

---

## 2. Key literature anchors — R_int pristine vs cycled + EIS components (with numbers found)

Only the four **CONFIRMED** numeric anchors below were captured this session (from search snippets, unverified vs full text). Everything else is a located paper whose per-cycle Ω·cm² table values require **PDF retrieval on WSL** (publisher egress was 403-blocked this session). Treat all snippet numbers as `precision=confirmed_snippet`, not `pdf_verified`.

### 2a. Pristine / good-interface R_int anchors (usable now)

| Anchor | Value | Conditions | Source |
|--------|-------|-----------|--------|
| **Single-crystal NMC / Li6PS5Cl R_int** | **≈ 40 Ω·cm²** (pristine/robust floor) | 2.5 MPa (anode) / 0.2 MPa (cathode) asym. pressure, 30 °C, 8.7 mAh/cm², 210 mAh/g, first-cycle CE >85 % then >99 %, **5.5 % lattice volume change** | ACS AMI 2021 — https://doi.org/10.1021/acsami.1c07952 · open ChemRxiv https://chemrxiv.org/engage/chemrxiv/article-details/60c757e49abda299f5f8e7ee (DOI 10.26434/chemrxiv.14479215) · PMC8397257 |
| **LiPON model interface (benchmark floor)** | **7.6 Ω·cm²** | Low-R reference floor cited in reviews | Reviews incl. Energy Mater. Adv. 2024 https://doi.org/10.34133/energymatadv.0163 ; Chem. Rev. 2024 https://doi.org/10.1021/acs.chemrev.4c00584 (PMC11869192) |

### 2b. Cycled / R_int-growth anchors (usable now)

| Anchor | Value | Conditions | Source |
|--------|-------|-----------|--------|
| ⚠ **CORRECTED (2026-07-20)** — NOT a bare-composite growth law | R_ct **593.8 → 350.9 Ω** = **DECREASES** over 300 cyc | ★ traced to **coated In-cPAN@NCM811, high-T (≥100°C) Li-metal cell** where a good coating *matures* → R_ct falls.  Do **NOT** use as an NMC811/LPSCl bare R_int(N) growth anchor. | Nano-Micro Lett. 2025 — https://doi.org/10.1007/s40820-025-01683-7 (mis-attributed to the Feng 2025 review here previously) |
| **Bare NCM811/LPSCl R_ct (our lab, magnitude anchor)** | 62/72/82 wt% = **453 / 290 / 382 Ω·cm²** (uncoated); **22.4/18.2/17.2** (LNO-coated, ~20× lower); T-sweep 30/45/60°C = 289.9/139.6/67.8 | 3-electrode full cell, 30°C, 250/100 MPa — post-formation snapshot (composition+T, NOT cycle-resolved) | **kim2025 (repo litdb, `pdf_verified`)** — Electrochim. Acta 542 147413, Tables S4/S6 |
| **LPSCl-catholyte / LLZO dual-layer interface-R growth** | **~100 Ω → ~300 Ω (≈3×) on contact loss** | Secondary — separator is LLZO, not the NMC/LPSCl cathode interface | ACS AEM 2025 — https://doi.org/10.1021/acsaem.5c02435 |
| **Collector\|Al contact growth (shape anchor)** | R_contact **≈10 (formation) → ≈30 Ω·cm² @50 cyc** (~3×), first-cycle step + ~linear k·N | liquid LNMO analog (HF passivation + coating delamination) — maps onto our SBE 18→110 / DBE 12→46 / C-SUS 10→30 @1000cyc endpoints | Pritzl 2019 JES — https://doi.org/10.1149/2.0451904jes |

### 2c. Composite-transport reference (the "bulk" R to subtract to isolate R_int)

| Quantity | Value | Source |
|----------|-------|--------|
| LPSCl σ_ion | **1.6 mS/cm (25 °C)** | Bielefeld/Dewald/Janek "Charge Transport Bottlenecks", J. Electrochem. Soc. — https://doi.org/10.1149/1945-7111/abf8d7 |
| LPSCl σ_e | **< 1e-6 S/cm** | same |
| NCM622 electronic partial σ | **≈ 10 mS/cm** | same |
| Optimal matching | **≈ 70:30 NCM:LPSCl** | same |

This directly cross-validates our DEM effective σ_ion/σ_e (frame[4]) and defines the composite-transport term subtracted to isolate the interface contribution.

### 2d. EIS-decomposition anchors (method + components — numbers need WSL)

- **Conforto 2021 (JES), genetic-algorithm impedance fit** — the single most on-target decomposition: NCM811 (SC vs poly) + LPSCl composite, resolves **R_ct (short τ, NCM–SE interface) separated from solid-state Li-diffusion (long τ)** and their pristine→cycled evolution. Per-cycle Ω/Ω·cm² are in fitted-parameter tables → WSL. DOI https://doi.org/10.1149/1945-7111/ac13d2. **→ primary anchor for backlog A11 (pristine R_int) + cycled growth.**
- **Koerver 2017 (Chem. Mater.)** — canonical NCM811 + β-Li3PS4: passivating interphase forms mostly during **first charge**, slow growth after; impedance rise vs cycle correlated with chemo-mechanical contact loss. Defines the "pristine baseline + first-cycle jump" shape. DOI https://doi.org/10.1021/acs.chemmater.7b00931.
- **MDPI Inorganics 2025 14(7):180 — DRT, OPEN ACCESS** — decomposes sulfide composite-cathode impedance into **5 operational resistance components** (LiNbO3-coated Ni-rich AM) with loading dependence (HF components ~constant/rise, mid–low-freq fall). **Best odds of extracting actual component ohms** since it is open. DOI https://doi.org/10.3390/inorganics14070180. → R_ion/R_int/R_w decomposition template.
- **Auvergniot 2017 (Chem. Mater.)** — XPS chemistry of the resistive interphase (LPSCl → S⁰, Li polysulfides, P2Sx, phosphates, LiCl) at uncycled / 2nd / 50th cycle → **why** R_int grows. DOI https://doi.org/10.1021/acs.chemmater.6b04990 · open HAL hal-01530952.
- **ACS AMI 2024 interfacial-impedance formulation** — the recipe to convert raw pellet Ω → **cathode-area Ω·cm² ASR** so heterogeneous literature values merge consistently. DOI https://doi.org/10.1021/acsami.4c01322.

### 2e. Coating / contact-loss / microstructure → R_ct anchors (paired bare-vs-coated; numbers need WSL)

- **Shi 2023 (Adv. Energy Mater.)** — bare vs 2–4 nm cationic-polymer-coated NCM in LPSCl; isolates **mechanical contact-loss vs chemical** contribution to R_int growth (ties to DEM coverage/Stage-E). DOI https://doi.org/10.1002/aenm.202300310 · OA mirror d-nb.info/1378263316/34.
- **Zhou 2025 (ACS Energy Lett.)** — fine vs coarse LPSCl: **R_ct(fine) < R_ct(coarse)** at **2 MPa** stack pressure (validates Stage-E coverage→transport). DOI https://doi.org/10.1021/acsenergylett.4c03256.
- **JMCA 2025 sPPSLi/PVP** — coated vs bare NCM in LPSCl: reduced R_int + shorter Li⁺ transport length over cycling. DOI https://doi.org/10.1039/d4ta07265k.

### 2f. Capacity-retention cycling anchors (digitizable curves for the cycling DB)

| Anchor | Value | Source |
|--------|-------|--------|
| Halide-coated NCM / sulfide | **92 % @100 cyc @0.1C; 72 % @270 cyc** vs matched **LPSCl + untreated NCM 53 % @100 cyc** (worst-case baseline) | ACS AEM — https://doi.org/10.1021/acsaem.2c02774 |
| Modified NCM811-sulfide | **80 % retention @250 cyc @4.3 V** | Feng 2025 review — https://doi.org/10.1002/cssc.202501033 (PMC12665888) |
| LNO-coated NMC811 (imaging) | **116 mAh/g @200 cyc** vs continuous degradation uncoated | Sci. Adv. 2025 (ORNL) — https://doi.org/10.1126/sciadv.ady7189 (PMC12506959) |
| NCM@LPO composite | **90.48 % @200 cyc @0.5C** + in-situ impedance stabilization | J. Power Sources 2024 — https://www.sciencedirect.com/science/article/abs/pii/S0378775324003173 |
| Sheet-type NMC811 / LPSCl catholyte (calendar-aged) | **122.97 mAh/g, 73.1 % retention** after aging | Doux/Nanda — https://www.osti.gov/pages/servlets/purl/3002087 |
| SC NMC83 / LPSCl pressure→retention | **10-cyc retention 99.4 % @2.5 MPa vs 101.1 % @10 MPa** | ChemRxiv 60c757e4 / ACS AMI 1c07952 (as above) |

Mechanistic/no-number anchors for the degradation narrative: Bielefeld JMCA 2020 (contact-loss quantification, https://pubs.rsc.org/en/content/articlelanding/2020/ta/d0ta06985j); KIT 1000146683 (single- vs poly-crystal fracture, https://publikationen.bibliothek.kit.edu/1000146683/150603681); Chem. Sci. 2026 (stack-pressure fracture, non-monotonic, https://pubs.rsc.org/en/content/articlelanding/2026/sc/d5sc09321j); arXiv:2307.00145 (open composite-cathode mechanical degradation, https://arxiv.org/pdf/2307.00145); JACS 2024 atomic-origin (https://doi.org/10.1021/jacs.4c02198).

### 2g. Mechanical / Vegard inputs for the MPM cycling kernel

- **De Biasi operando-XRD** — NMC lattice a,c and cell volume vs SOC; **NMC811 ≈ 12.5 % volume swing** (lithiated↔delithiated), nonmonotonic c-collapse >4 V. Source of the Vegard/partial-molar-volume law. DOI https://doi.org/10.1149/1945-7111/abf262. **Figures only → digitize into β_Vegard(x).** *(Note: distinct from the 5.5 % "lattice volume change" reported for the SC NMC83 cell in §2a — cite each to its own source; do not conflate.)*
- **NMC811 mechanical constitutive** — lithiation-dependent shear strength / elastic constants: JES 2022 https://doi.org/10.1149/1945-7111/ac6244 (E(x), G(x), embrittlement-on-delithiation for the CZM/phase-field crack model).

---

## 3. DB-ification tools & standards to adopt (with why)

The project already has a working convention: provenance-tagged CSVs in `docs/data/` (e.g. `densification_porosity_db.csv` with `source,structure,material_SE,…,precision,note`) plus per-paper `litdb` digests. **Extend that**, do not replace it. The recommended stack layers cleanly on top:

| Layer | Adopt | License | Why |
|-------|-------|---------|-----|
| **Canonical store (cycling/profile raw)** | **battery-data-toolkit (`battdat`)** — Parquet/HDF5 + typed `BatteryMetadata` — github.com/ROVI-org/battery-data-toolkit | Apache-2.0 | Most DB-ready normalizer; fixed column + metadata schema; from the Battery Data Genome effort our CAMP source aligns to. The metadata block is where composition (φ_SE, P:S), pressure, and provenance DOIs attach. |
| **Raw-cycler ingest** | **BEEP** (Arbin/MACCOR/Neware/BioLogic → structured; github.com/TRI-AMDD/beep) + **cellpy** (dQ/dV, relaxation-R; github.com/jepegit/cellpy) | Apache-2.0 / MIT | Cross-cycler schema removes per-instrument column drift; cellpy computes the dQ/dV our ica-msc workflow needs. |
| **Low-level format decode** | **galvani** (BioLogic .mpr/.mpt, Arbin .res) | GPL-3.0 | Needed for raw EIS `.mpr`. **Keep at the import boundary only** (subprocess/optional dep) so the redistributed DB core stays permissive. |
| **EIS → R_int reduction** | **impedance.py** (KK-validation + ECM fit + CIs; github.com/ECSHackWeek/impedance.py) | MIT | Turns raw spectra into the stored anchor: `{raw Z + circuit string + fitted params + KK residual}`. Store the circuit string so fits are reproducible. |
| **Semantic typing / provenance** | **BattINFO** (JSON-LD, CellSpec→Test→Dataset chain; github.com/BIG-MAP/BattINFO) on **EMMO** (units/quantities) | Apache-2.0 / permissive | Machine-linkable IRIs for cell/electrode/EIS-test/dataset → FAIR, and the provenance chain that ties an anchor value back to its source paper AND to a simulation case (our frame[4] crosswalk). |
| **Interchange convention** | **BatteryArchive** column/metadata convention | per-study | Community-recognized names → our DB stays importable/exportable against open corpus. |
| **Optional hosted back end** | **NOMAD + nomad-battery-database plugin** or **Galv** (Postgres+REST) | Apache/MIT | If searchable + DOI-citable hosting is wanted later; Galv is the closest existing "raw files → queryable API" implementation. Not required for Phase 1. |
| **Simulation-side param anchors** | **PyBaMM** parameter sets + **LiionDB** | BSD-3 / MIT | Catalog literature transport/kinetic values next to experimental anchors for model↔experiment rows; already used by `step4_pybamm_anchor.py`. |

**Four things NO standard covers — build a thin custom layer (this is the real work):**
1. **R_int / DCIR / ASR table** — there is no community schema for `{protocol (HPPC/GITT/pulse) → R_int(SOC,T,pulse-width)}`. Define it; make **Ω·cm² (ASR) canonical** to match DEM/MPM σ/ASR outputs (store raw Ω too).
2. **EIS-ECM record** — no FAIR model for `{spectrum + circuit + params + KK residual}`; impedance.py output is the payload, but the schema is ours.
3. **Composite-microstructure descriptors** — none of these tools model φ_SE, P:S, porosity, τ, coverage, CN, or the σ triad. Add a small EMMO/BattINFO-typed domain module.
4. **Sim↔experiment crosswalk** — which computed anchor validates which measured anchor + the residual. BattINFO provenance can host both sides; the crosswalk is ours to design (it is exactly the frame[4] epistemology in data form).

**Pragmatic Phase-1 recommendation:** keep digitized *scalar* anchors (R_int, σ_ion, retention) as **provenance-tagged CSVs in the existing `docs/data/` style** (fast, git-diffable, matches litdb); reserve `battdat` Parquet only for the *raw time-series* sources (CAMP, Nature Energy Zenodo, Mendeley). Adopt impedance.py + BattINFO typing incrementally.

---

## 4. HONEST gaps — what open sources CANNOT anchor (→ needs the user's lab data)

**A. The central gap (no open dataset exists):** measured **R_int or EIS for NMC811 + Li6PS5Cl composite cathodes with paired cycling.** Breakdown, from the findings:
- The one on-material ASSB set (Nature Energy 2024) has **no EIS, no R_int**, and **CAM = 622 not 811**.
- Every open EIS/R_int dataset (NASA, CALCE, HNEI, SNL) is **liquid LCO/NMC** → method validation + order-of-magnitude only.
- SSE conductivity DBs (OBELiX, LiIonML) give **bulk σ_ion of LPSCl**, nothing about the composite/interface.
- Open NMC811 cycling (CAMP, Mendeley) is chemistry-matched but **liquid-cell** → OCP/capacity-shape only.
→ **Consequence:** the ASSB-specific R_int/ASR + EIS anchors must be **digitized per paper into litdb** (Conforto 2021, Koerver 2017, MDPI Inorganics open, Feng review). No bulk download substitutes.

**B. Session-access gap (not a data gap — fetch on WSL):** all scholarly hosts (ACS, IOP, Wiley, RSC, ScienceDirect, Nature, Science, PMC, OSTI, MDPI, arXiv, ChemRxiv, KIT) returned **403 on this session's egress proxy**. Every §2 non-CONFIRMED number is a search snippet, **not verified vs full text**. This is recoverable — see §5.

**C. Genuine content gaps that likely require the user's own cells (lab data):**
1. **Clean pristine → cycled R_int(Ω·cm²) curve for a BARE NMC811 + LPSCl cathode** over defined cycles — values live in Koerver 2017 / Conforto 2021 *figures*; even after WSL digitization these are specific cells, not our composition sweep.
2. **Pressure-resolved R_int sweep** for NMC811/LPSCl — only **spot points** exist (≈40 Ω·cm² @0.2 MPa cathode; Zhou @2 MPa). A systematic R_int-vs-stack-pressure curve is a **lab measurement gap**.
3. **Temperature-resolved R_int / activation energy of the cathode-side interphase** — not surfaced in any open source → lab or targeted PDF dig.
4. **Current-collector-specific ASR (Al / C-coated-Al ↔ cathode) in Ω·cm²** — essentially absent openly. This is the backlog **A11** input; the model currently uses post-cycle collector anchors (bare/DBE/C-SUS, from manuscript Fig6e per backlog A11), and the **pristine** collector interface has **no open anchor** → almost certainly a lab gap. Directly relevant to the collector/σ_apparent code.
5. **True pristine (t=0, pre-formation) R_int** — rarely reported cleanly (most report after ≥1 formation cycle) → the isolated pristine anchor for **A11** may need a first-EIS-before-cycling lab measurement.
6. **Multi-pressure Heckel for LPSCl powder** — still the missing direct compaction validation flagged in CLAUDE.md; no open dataset.
7. **Operando pressure/EIS ASSB with raw files** — studies exist but data is embedded in figures, not deposited.
8. **NMC-vs-Li / Li-In half-cell OCP(x) table** — no purpose-built open anchor; best fix is digitizing the vs-Li-In curve from Nature Energy Zenodo (still a proxy).
9. **AM–SE (NMC/LPSCl) cohesive-zone parameters** (interfacial adhesion energy + traction-separation) — **essentially unmeasured in the open literature**; this is the #1 missing input for the contact-loss/fracture track. (Our SDCP DFT E_bind/γ work is the internal partial answer.)
10. **β_Vegard(x)** exists only as figures (De Biasi) — no packaged CSV; anisotropic a-vs-c strain must be reconstructed.
11. **No machine-readable degraded-microstructure (XCT) volume** deposited openly for LPSCl-NMC → no direct contact-loss-vs-cycle validation array.

**D. Structural limits (not fixable by more data):** every open electrode-scale continuum tool (PyBaMM, MPET, BattMo, DandeLiion) is a **homogenized Bruggeman continuum** — they anchor absolute V(t) and profile *shape* in the uniform limit but by construction **cannot validate the microstructure-heterogeneity deviation** that is our STEP3/STEP4 value-add. Agreement in the uniform limit is the only rigorous cross-check; on the real bed, divergence is the **finding**, not an error. **Do not cross-fit** (frame[4]). Also: **no open array-level through-thickness φ(z)/j(z) dataset** for an LPSCl composite exists — the only φ(z) reference (Oh 2025 Fig 4e, MSE R) is a figure to digitize → STEP3 φ(z) validation stays shape-level.

---

## 5. Concrete next actions — Phase 1 (build anchor DB + wire --r-int)

**Important:** `scripts/step4_dyn.py` **already exposes** the knobs — `--r-int-ohm-cm2` (line ~1166, default 0.0), `--asr-film [Ω·m²]` (line ~1165), plus `--ocp-csv/--params-json/--x0/--x100/--v-min`. So "wire --r-int" is a **data-population + provenance task**, not flag creation. The job is to feed these from a versioned anchor DB with source-tagged values.

**Step 1 — Create the R_int/EIS anchor table (today, no network needed).**
Add `docs/data/rint_eis_anchors.csv` in the existing provenance-tagged style. Suggested columns:
`anchor_id, quantity {R_int|R_ct|R_ion|R_w|sigma_ion|sigma_e|retention}, value, unit {Ohm|Ohm_cm2|mS_cm|pct}, cathode {NMC811|NMC622|NMC83_SC|...}, SE {LPSCl|b-Li3PS4|...}, anode, cycle_n, pressure_MPa, areal_mAh_cm2, temp_C, precision {confirmed_snippet|pdf_verified|figure_digitized}, doi, url, note`.
Seed **only the confirmed numbers**: 40 Ω·cm² (acsami.1c07952), **kim2025 (pdf_verified) bare NCM811/LPSCl R_ct 453/290/382 · LNO-coated 22.4/18.2/17.2 Ω·cm² + T-sweep 289.9/139.6/67.8 (Electrochim. Acta 542 147413)**, 100→300 Ω contact-loss (acsaem.5c02435), LiPON 7.6 Ω·cm², and the Bielefeld transport row (σ_ion 1.6 mS/cm, σ_e <1e-6, NCM622 σ_e 10, 70:30). ⚠ **The old "R_ct 593.8→350.9 @300cyc (cssc.202501033)" is STRUCK** — §2b traced it to a *coated In-cPAN decrease* (Nano-Micro Lett. 2025), mis-attributed to the Feng cssc review; it is NOT a bare-composite growth anchor. Mark everything `precision=confirmed_snippet` until WSL verification. Reuse the existing `interfacial_impedance_formulation.csv` for the Ω→Ω·cm² recipe.

**Step 2 — WSL PDF-fetch + digitize worklist (unblocks §2 numbers).** On the unrestricted WSL machine, download and read the impedance tables of, in priority order:
1. **MDPI Inorganics 14(7):180** (10.3390/inorganics14070180) — OPEN; extract the **5-component R_ion/R_int/R_w/... ohms** → the decomposition template. Also captures backlog-relevant DRT method.
2. **Conforto 2021** (10.1149/1945-7111/ac13d2) — per-cycle R_ct + Li-diffusion → **A11 pristine + cycled growth**.
3. **Koerver 2017** (10.1021/acs.chemmater.7b00931) — pristine baseline + first-cycle step.
4. **Feng 2025 review** (10.1002/cssc.202501033, PMC12665888) — batch-harvest the per-coating R_int/R_ct table.
5. **Nature Energy Zenodo** (10.5281/zenodo.15827509) — V-Q CSVs for the STEP4 window.
Use WebPlotDigitizer for figure-only curves (Koerver/Conforto R_int-vs-cycle; De Biasi β_Vegard(x); Oh 2025 φ(z)). Normalize every value to **Ω·cm²** with the ACS AMI 4c01322 recipe; store both raw Ω and ASR; bump `precision` to `pdf_verified`/`figure_digitized`.

**Step 3 — litdb digests** (canon-branch rule from CLAUDE.md: cards go to `origin/claude/friendly-meitner-lldvar` `litdb/` only; check INDEX first to avoid duplicates). Create digests for Conforto 2021, Koerver 2017, MDPI Inorganics 2025, Shi 2023, Zhou 2025, Auvergniot 2017 — each with its confirmed number and the anchor_id it populates.

**Step 4 — σ_ion population anchor.** Ingest OBELiX (`pip install obelix-data`) + LiIonML sulfide subset → `docs/data/sse_sigma_ion_population.csv`; filter to Li6PS5X; use to sanity-check σ_grain = 3.0 mS/cm and place LPSCl in the measured spread (cross-check vs the Bielefeld 1.6 mS/cm composite value). Machine-readable → automated.

**Step 5 — NMC811 baseline + STEP4 window re-anchor (the PENDING task).** On WSL/V100 (NOT the cloud container — no sklearn/pybamm here): install **PyBaMM + LiionDB**; run `step4_pybamm_anchor.py --export-params` to dump `ocp_nmc811_chen2020.csv` + params JSON into `docs/data`; then build the **vs-Li-In OCP** by digitizing the Nature Energy Zenodo 0.1C discharge curve (+ Mendeley relaxation set as the near-equilibrium NMC811 OCP proxy) to fix `--x0/--x100/--v-min` and the 0.62 V Li-In offset. Bracket D_s/i0 against LiionDB distributions.

**Step 6 — Wire the anchor DB into STEP4.** Add a small loader that resolves a scenario key (e.g. SBE / DBE / collector-C-SUS) to a `value` from `rint_eis_anchors.csv` and passes it to `--r-int-ohm-cm2` (and `--asr-film` for the SEI/CEI film term), with the source DOI logged in the run provenance. Keep the model's existing collector anchors as **separate rows** and add the ~40 Ω·cm² pristine floor as its own row so backlog **A11** can split "initial-contact improvement" vs "degradation-suppression" (pristine vs cycled R_int as two columns, per A11).

**Step 7 — EIS-extraction method validation (parallel, low priority).** Prototype the `impedance.py` ECM record `{raw Z + circuit + params + KK residual}` on the **NASA PCoE / CALCE** `.mat`/CSV EIS (off-chemistry, method only) so the exact code path is proven before it digests ASSB EIS from litdb. Tag these as `non_anchor`.

**Step 8 — Adopt the schema spine incrementally.** Store raw time-series sources (CAMP, Nature Energy, Mendeley) in `battdat` Parquet+metadata; keep scalar/digitized anchors as `docs/data/*.csv`; add BattINFO/EMMO JSON-LD typing to the anchor rows once the CSV schema stabilizes. Keep GPL parsers (galvani) at the import boundary only.

**Deliverable of Phase 1:** a versioned, DOI-provenanced anchor DB whose R_int/EIS/σ_ion/retention rows (a) feed `--r-int-ohm-cm2`/`--asr-film` in STEP4 with source tags, (b) give the group-to-group **variance band** (Nature Energy 106–142 mAh/g) as the uncertainty envelope on any DEM/MPM/STEP4 capacity prediction, and (c) explicitly flag the six lab-only gaps in §4C so the user's own first-EIS / pressure-sweep / collector-ASR measurements are scoped as the loop-closing experiments.

---

### Files & hooks this plan touches (all absolute)
- `/home/user/Yonghoon-DEM-DFT/docs/data/rint_eis_anchors.csv` — **NEW** (Step 1)
- `/home/user/Yonghoon-DEM-DFT/docs/data/sse_sigma_ion_population.csv` — **NEW** (Step 4)
- `/home/user/Yonghoon-DEM-DFT/docs/data/densification_porosity_db.csv` — existing schema pattern to mirror
- `/home/user/Yonghoon-DEM-DFT/docs/data/interfacial_impedance_formulation.csv` — existing Ω→Ω·cm² recipe to reuse
- `/home/user/Yonghoon-DEM-DFT/scripts/step4_dyn.py` — `--r-int-ohm-cm2` / `--asr-film` / `--ocp-csv` / `--x0` / `--x100` already present; add DB-loader (Step 6)
- `/home/user/Yonghoon-DEM-DFT/scripts/step4_pybamm_anchor.py` — `--export-params` for OCP/param anchors (Step 5, run on WSL/V100)
- `/home/user/Yonghoon-DEM-DFT/docs/digest_model_application_backlog.md` — item **A11** (collector pristine↔cycled R_int) is the direct consumer of §2d/§4C-4,5
