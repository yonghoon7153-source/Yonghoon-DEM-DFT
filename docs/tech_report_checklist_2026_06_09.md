# Technical Report Checklist (2026-06-09)

> **Purpose.** Inventory of every result, caveat, file location, and cross-link that should appear in the Paper #1 (LPSCl vs LPSCl1.6) + Paper #2 (Nd / cascade doping) technical report. **Do not skip items below.** Each entry lists: what to claim, what to NOT claim, where the numbers live, and which results connect.

---

## 0. Cells, conventions, common references

- **comp1 / comp1_v3** = Li6PS5Cl (LPSCl), 52-atom cubic. EOS V0 = 1016.62 Å³, a = 10.055 Å. `db/properties/eos.json` `comp1_v3` (PRIMARY_paper_value, R²=1.000).
- **modelc / modelc_v3** = Li5.4PS4.4Cl1.6 (LPSCl1.6), 62-atom rhombohedral. EOS V0 = 1216.44 Å³, a=b=7.007 Å, c=35.036 Å. `db/properties/eos.json` `modelc_v3`.
- Structures of record:
  - comp1: `db/structures/comp1_V0_k444.cif/.xyz` (4×4×4 k = kxL 40). DEPRECATED `lpscl_relaxed_conv_52atoms.cif` was BROKEN_PS4 — do NOT cite.
  - modelc: see eos.json entry.
- DFT pseudo / k-mesh defaults are recorded per-property; do not assume same across properties (e.g. ICOHP comp1 k=4×4×4, modelc k=6×6×3 each at kxL ~40–42).
- Naming policy: cells `cas/uma/qe` etc. all refer to UMA-s-1p1 unless tagged.

---

## 1. Bonding / electronic structure (Paper #1)

### Must report
- **PS4 framework invariance** comp1 ↔ modelc:
  - Bond length P–S 2.073 vs 2.064 Å (`db/properties/bonds.json`).
  - Bader PS4 charge −2.82 / −2.60 (`db/properties/electronic.json`).
  - ICOHP P–S −5.94 / −6.0 eV/bond (`db/properties/electronic.json` and `bonds.json` LOBSTER section).
  - ELF P–S bridge 0.946 / 0.944 (`db/properties/electronic.json` `elf_comparison_v3`).
- **Li / Cl sub-lattice changes** (Cl-rich + vacancy):
  - 4d-Cl anti-site fraction in modelc = 12.5 % (`bonds.json` `Li_Cl_per_site_split` headline). NOT the synthetic Minafra/Schlem level — see §4 disorder caveat.
  - ICOHP-distance slope flatter for modelc Li–Cl, Li–S (more ionic, `bonds.json` `icohp_distance_correlation_eV_per_Angstrom`).
  - Wilkening 3-way correlation: Bader q × distance ↔ ICOHP same coupling for both (one Coulombic axis underlies bond, COHP, ELF).
- **Band gap**:
  - USPP-PBE + DOS-threshold: comp1 1.76 eV, modelc 1.82 eV (modelc gap slightly larger; same VBM = S 3p).
  - Method offset vs PAW-PBE literature (~2.2–2.5 eV) is consistent for both — quote the delta, caveat the absolute.
  - `db/properties/electronic.json` `comparison_comp1_v3_vs_modelc_v3.absolute_vs_literature`.

### Must caveat
- ELF / Bader / ICOHP **single-crystal 0 K**; no GB / interface / kinetic effects.
- USPP gap underestimate ~0.3–0.4 eV (consistent for both; delta robust).

### Cross-links
- PS4 invariance → §3 oxidation onset identical at 0 GPa; §2 clamped-ion elastic identical; §4 conductivity prefactor story.

---

## 2. Mechanical (Paper #1, three regimes)

### Must report (within-method only)
- **DFT 0 K clamped-ion**: comp1 vs modelc E_VRH 52.31 ≈ 52.30 GPa (**identical**, ±2 %). `db/properties/elastic.json` `dft_0K_clamped_ion_stress_strain_full_Cij`.
  - Zener_A 1.07 vs 0.42 → comp1 isotropic, modelc highly anisotropic (vacancy + 4d-Cl anti-site).
- **DFT 0 K relaxed-ion**: comp1 E_VRH = 22.06, modelc 27.66 (+24 %). G_VRH 8.13 → 10.4 (+28 %). Modelc stiffer in Young / shear. **B_VRH 25.5 → 23.4 (modelc slightly softer in bulk).** `db/properties/elastic.json` `dft_0K_relaxed_ion_stress_strain_full_Cij`.
- **MLIP 600 K** (UMA-s-1p1, same script): comp1 E_VRH 59.71±0.82, modelc 52.72±1.42 → comp1 stiffer at 600 K. `db/properties/elastic.json` `mlip_600K_snapshot_v3`.
- **VACANCY PARADOX RESOLVED** (`elastic.json` line 144 headline + `literature_kim_2025_halogen_modulus`):
  - Apparent paradox = clamped-ion identical, but experiment says LPSCl1.6 stiffer.
  - Resolution = relaxed-ion DFT already gives modelc +24 %, matching Kim 2025 ACS Mater Lett Cl→E↑ trend. Kim's mechanism: smaller Cl → higher ion-packing density → stiffer.
- **Mechanism (db-internal):** modelc's Cl-rich vacancy + 4d-Cl anti-site jams a soft collective Li-sublattice shear mode that comp1 keeps. 0 K identical because frozen framework can't lose the soft mode. Ions relax → mode collapses → modelc stiffer.

### Must caveat
- **No cross-method magnitude compare.** Do NOT put UMA 600 K E=59 next to DFT 0 K E=52 in the same plot without an asterisk; UMA absolute scale ≠ QE absolute scale.
- 600 K MLIP entry is **demoted to SI / supporting only** (`elastic.json` `mlip_600K_snapshot_v3._USAGE_2026_06_08`). Headline = 2-regime DFT (clamped + relaxed).
- modelc relaxed-ion C44 = 14.43 close to MLIP 600 K (12.9) → modelc_v3 captures Li-disorder basin, not the perfect ordered 0 K minimum (`vs_modelc_v1_DFT_clamped_ion.interpretation`).
- Pellet vs single-crystal: our DFT relaxed-ion E 22–28 GPa is single-crystal upper bound; group AFM gives 14.9 (LPSCl1.6) / 15.8 (NdO-LPSCl1.6) pellet; Kim UPE 15–22. Trend (Cl-rich stiffer in E/G) consistent across all three.

### Cross-links
- §1 PS4 invariance ↔ clamped-ion identical.
- §3 Cl-rich oxidation widening ↔ same volume/strain physics as relaxed-ion stiffening (Gil-González "the SAME volume / strain physics gates both axes").
- §6 Kim ACS 2025 + Kim JMCA 2026 confirm halide-size → modulus rule.

### Files / tools
- DFT stress-strain: `tools/modelc_v3/elastic_static.py` (or equivalent). MLIP 600 K: `tools/modelc_v3/elastic_mlip_600K.py`.

---

## 3. Oxidation stability — 4 axes (Paper #1)

### Must report — axis by axis

**Axis 1 — Intrinsic 0-pressure window (grand-potential):**
- `tools/oxidation/esw_grand_potential.py` (pymatgen `get_element_profile`, MP GGA_GGA+U, Li-P-S-Cl).
- comp1 = modelc identical: OCV self-decomp 1.72 V → Li3PS4 + Li2S + LiCl; oxidation onset 2.14 V → polysulfide (with LiS4 included).
- `db/properties/oxidation_stability.json` `results.comp1` / `results.modelc`.
- **Validated by Gil-González K_eff=0 LPSCl1.5 1.70–2.40 V** — our 1.72–2.14 matches the cathodic edge exactly; 0.26 V anodic gap = our inclusion of LiS4 which they exclude.

**Axis 2 — Mechanical-constriction window:**
- `tools/oxidation/constrained_esw.py` (strain-explicit Fitzhugh leading-order, LiS4/SCl3/Li5PS4Cl2 excluded).
- comp1 vs modelc pair (`constrained_esw_OUR_CALC` block in `oxidation_stability.json`):
  - K_eff=0 identical (1.24–2.26 V), K_eff=10 modelc 0.53–2.69 (w 2.16) vs comp1 0.63–1.97 (w 1.34), K_eff=20 modelc −0.18–3.11 (w **3.30**) vs comp1 0.02–1.68 (w 1.66).
  - **Modelc anodic limit RISES 2.26 → 3.11 V** under K_eff=20; comp1 drops. Driven by oxidation onset ε_RXN: modelc +0.023 (bulky LiCl) vs comp1 −0.036 (dense Li3PS4+LiCl+S).
- Cl-content scan `docs/oxidation/constrained_esw_cl_scan_2026_06_09.md` + `constrained_esw_cl_scan.json` (gabia):
  - LPSCl0.5 → LPSCl1.0 → LPSCl1.5 → modelc(1.6) → LPSCl2.0: width at K_eff=20 = 1.09 / 1.66 / 2.81 / **3.30** / 2.60.
  - **modelc sits at the sweet spot** of the constriction-induced oxidation optimum.
  - LPSCl2.0 turn-over: P2S7-bearing path, ε_RXN drops back to −0.019 (matches Gil-González orthorhombic LPSCl2.0 distinction).

**Axis 3 — Cathode-interface cycling:**
- `tools/oxidation/interface_reactivity.py` (pymatgen `InterfacialReactivity`, use_hull_energy, MP).
- vs LiCoO2: comp1 −0.323, modelc −0.331 eV/atom (modelc +2.5 % more reactive).
- Same solid oxygenated set (Co9S8 + 0.113 Li2SO4 + 0.258 Li3PO4) for both; modelc trades 0.155 Li2S for extra LiCl.
- vs C: BOTH 0.0 — Zuo's carbon-interface effect is electrochemical, not chemical.
- KEY LIMITATION: closed solid hull can NOT capture gas-diversion (SO2). Zuo Fig 4 ToF-SIMS: phosphate (PO_x) + sulfate (SO_x) LOWER for Cl-rich, polysulfide HIGHER. The beneficial part (less solid resistive byproduct → lower R_int) needs gas-phase chempots, not in our calc.

**Axis 4 — Calendar / thermal aging:**
- Wu et al. *Nano Energy* 2026 calendar aging FULL READ. NCM811/LiIn 100 SOC 90 °C 5 day retention: L6 68 % > L53 59 % > L55 48 %.
- **Cl-rich loses on this axis.** SOC (100 vs 0) and cathode (LCO > NCM811, H3/lattice-O) are STRONGER levers than Cl content.
- `db/properties/oxidation_stability.json` `wu_2026_calendar_aging_FULL_PAPER_READ`.

**Capstone:** `oxidation_stability.json` `MULTI_AXIS_CAPSTONE_oxidation_stability_DONE` + `seminar_message_rev3`.

### Must caveat
- Closed solid hull thermodynamics; no gas; chemical (zero-bias) interface reactivity only; intrinsic bulk window (does NOT include practical cell decomposition with bias, kinetics, passivation quality).
- Constrained ESW Cl-scan = leading-order edge shift; absolute V differs from Gil-González (their full Lagrange re-min gives ~4.3 V at K=20 LPSCl1.5; ours ~2.66). Qualitative trend matches.
- modelc as composition (no MP entry); Li5.4PS4.4Cl1.6 treated via hull-equilibrium at the composition.

### Must NOT claim
- Do NOT say "Cl-rich more/less oxidation stable" without naming the axis.
- Do NOT cite our intrinsic 0-pressure window numbers as cell-level performance.

### Cross-links
- Axis 1 ↔ §1 ELF/COHP/DOS (S 3p VBM same).
- Axis 2 ↔ §2 same volume/strain physics that governs elastic relaxed-ion stiffening (UNIFIED VOLUME/STRAIN AXIS).
- Axis 3 ↔ Zuo 2023 (db) decomposition reactions match our grand-potential chemistry (electron count 1 vs 2, LiCl 1.6 vs 1.0).
- Axis 4 ↔ motivates Paper #2 O-doping campaign.

### Files / tools
- `tools/oxidation/esw_grand_potential.py`, `tools/oxidation/constrained_esw.py`, `tools/oxidation/interface_reactivity.py`.
- Run artifacts on gabia `/data/work/repo/esw_*.json`, `constrained_esw_*.json`, `interface_reactivity_results.json`.

---

## 4. Li conductivity (Paper #1) — disorder caveat is the centerpiece

### Must report
- **Robust observed fact:** modelc D > comp1 D over 600–1000 K window (`db/properties/li_transport.json` `comp1_vs_modelc_comparison.robust_findings`).
  - D(600 K): comp1 2.68e-6 vs modelc 7.90e-6 cm²/s (modelc ~2.9× faster).
  - σ(LPSCl1.6) > σ(LPSCl) experimentally; our result agrees.
- **Disorder-ensemble study (`docs/transport/disorder_ensemble_2026_06_09.md`):**
  - comp1 d=0.00 (fully ordered): Ea = 1.171 eV = **kinetic-frozen artifact** (D(600 K) = −3.7e-7 cm²/s = below MSD noise floor). NOT a physical barrier value.
  - comp1 d=0.50: Ea = 0.177 ± 0.027 eV (n=3 configs). Matches Minafra/Kraft / Schlem experimental LPSCl Ea = 0.16–0.25.
  - The previous 0.172 (comp1) / 0.224 (modelc) "physical inversion" was an artifact of cells with different residual disorder. comp1's earlier 0.172 came from a thermally pre-annealed cell that already had effective disorder.
- modelc d=0.5 still running on v100 (12/24 MDs at 2026-06-09 13:15). Decides barrier-vs-prefactor for the Cl-rich gain.

### Must caveat
- UMA absolute D overestimates ~3–5× vs experiment. Report Ea + 600–1000 K D values; do NOT over-interpret 300 K extrapolation.
- 3-point Arrhenius extrapolation to 300 K is uncertain.
- comp1 d=0.00 Ea = 1.17 is **NOT** the activation energy of ordered Li6PS5Cl. It is a low-T statistics artifact. Cite only as "ordered limit kinetically inaccessible".
- The d=0.00 negative D is "below noise floor", not a software error.

### Must NOT claim (currently partially retracted)
- The "comp1 Ea < modelc Ea, gain is prefactor not barrier" framing in `comp1_vs_modelc_comparison.mechanism_interpretation` (line 87–91 of li_transport.json) is **partially retracted** pending modelc d=0.5 result.

### Cross-links
- §1 PS4 invariance: explains why bonding doesn't change but Li sublattice (where disorder lives) does.
- §3 Axis 2: same Cl-rich + vacancy that shifts oxidation under K_eff also changes Li sublattice statics.
- Audit `db/properties/literature_tensions_audit.json` `2_conductivity_mechanism_Ea_vs_prefactor`.

### Files
- comp1 / modelc earlier Arrhenius: `db/properties/li_transport.json`.
- Disorder ensemble tool: `tools/modelc_v3/disorder_ensemble_diffusion.py`.
- Per-T data: `container:/home/ubuntu/work/runs/comp1_v3/disorder_diffusion/ensemble_results.json`.

---

## 5. Literature tensions audit — what is still open

`db/properties/literature_tensions_audit.json`:

1. **Oxidation stability (1_oxidation_stability)** — VALIDATED + K_eff-axis story (Gil-González K_eff=0 matches our 0-pressure; Cl-rich advantage is K_eff>0 effect).
2. **Conductivity Ea-vs-prefactor (2_conductivity_mechanism_Ea_vs_prefactor)** — PARTIALLY RESOLVED, retracted. d=0.5 comp1 Ea = 0.177 matches Minafra/Kraft. modelc d=0.5 pending → will close.
3. **Elastic vacancy paradox (3_elastic_vacancy_paradox)** — RESOLVED. Relaxed-ion DFT already gives modelc stiffer, matching Kim 2025 ACS Mater Lett.
4. **Band gap absolute (4_band_gap_absolute)** — minor, method underestimate, delta valid.
5. **Li3N UMA topology failure (5_li3n_uma_topology_failure)** — MLIP model failure, parked; paper claim uses DFT/literature (see §8 below).

---

## 6. Literature inventory (read 2026-06-08 / 06-09)

### Oxidation stability (db'd)
- **Gil-González, Ye, Wang, Shadike, Xu, Hu, Li**, *Energy Storage Mater.* 2022, 45, 484–493. Constrained-ensemble ESW Fitzhugh formalism. `oxidation_stability.json` `gil_gonzalez_2022_FULL_PAPER_READ`.
- **Zuo, Walther, Teo, Rueß, Wang, Rohnke, Schröder, Nazar, Janek**, *Angew. Chem.* 2023, 62, e202213228. Interface degradation comp1 vs LPSCl1.5. `zuo_2023_FULL_PAPER_READ`.
- **Wu, Zhang, Wu, Xu, Zhou, Li, Chen, Wu**, *Nano Energy* 2026, 147, 111576. Calendar aging. `wu_2026_calendar_aging_FULL_PAPER_READ`.

### Mechanical (db'd)
- **Kim, Nahm, Lee, Kim** (Hyoungchul Kim group), *ACS Mater. Lett.* 2025, 7, 724–729. Halogen-rich modulus. `db/properties/elastic.json` `literature_kim_2025_halogen_modulus`.
- **Kim, Nahm, Kim, Lee, Kim** (Hyoungchul Kim group), *J. Mater. Chem. A* 2026, 14, 9939–9947. I-rich (Cl→I) modulus. `literature_kim_JMCA_2026_Irich`.

### Conductivity narrative
- **Minafra, Kraft et al.** (Zeier group) "Enhanced ion conduction by enforcing structural disorder in Li6−xPS5−xCl1+x", *Solid State Ionics* 2020. Cited in §4 + tension audit #2. Web-fetched abstract + figures; full read TBD if needed.

### Group internal context
- 2026-06-08 group weekly report (AFM measurements: LPSCl1.6 14.9 GPa, NdO-LPSCl1.6 15.8 GPa; Halogen-rich argyrodites refs 1/2/3 = Zuo/Gil-González/Wu; mechanical refs 1/2 = Kim 2025/2026).
- `runs/nd_doped_modelc/...` Nd2O3 doping plan: 5 paper targets (e-conductivity, Li-SE interface decomp, SEI gap, atomic bonding, Young's modulus), see `db/compositions/modelc_nd_doped.json`.

---

## 7. Cascade doping verification (Paper #2 inputs)

### Must report
- **41 champions across 14 dopants × 3 concentrations + Sc2O3 x002 alone, all converged.** `docs/cascade/cascade_dopants_2026_06_09.md` + `db/properties/doping_cascade_verified.json`.
- **Site preference unambiguous:** 38/41 → Li_24g, 3/41 → Li_48h (chemistry signal: self-similar Li2O all; small monovalent Cu+, Ag+ tie-breakers), **0/41 → P_4b**. Site-preference review (with literature-evidence tags) was a separate codebase task — see §9 + audit notes if reviewer asks about Y@P, etc.
- **Coating candidates (low E_VRH, weekly-report goal):**
  1. **Sc2O3 x=0.02** (E_VRH 18.7, dE −0.974) — softest + strongest formation.
  2. Al2O3 x=0.05 (29.3, −0.809).
  3. Li2O x=0.05 (32.4, −0.531) — softest monovalent.
  4. MnO x=0.05 (32.6, −0.662) — low ΔV.
  5. NiO x=0.10 (33.9, −0.551) — direction matches earlier NiO db entry (0.81/0.85/0.70).
- **Top by formation energy:** Sc2O3 > Al2O3 > Mn/Co/Ca/Ba > rest.
- **+Clrich variants winning:** Sc2O3 x002, Al2O3 x010, MgO x002/x005. Cl-enrichment synergy with these oxide dopants.

### Must caveat
- UMA-s-1p1 cascade ABSOLUTE elastic / EOS values run high vs AFM/UPE. **Within-cascade comparison only.**
- 3 EOS B0 fit failures (MnO_x002, CoO_x010, ZnO_x010) — Cij still good, B0 row ignored for those.
- Sc2O3 has only x=0.02; x=0.05 and 0.10 follow-up needed (probably worth GPU time given headline).
- gabia-local; vm has Al2O3 champion `xyz` only, rest pending PAT sync. `doping_cascade_verified.json` is the vm-queryable snapshot.

### Cross-links
- §10 Nd2O3 plan: same cascade-style screen but with DFT+U + ISPIN=2 for 4f.
- Group weekly report coating layer goal: low modulus + high oxidation stability.

---

## 8. Li3N anode (Paper #2 supporting, parked MLIP)

### Must report
- **UMA Li3N(001) adsorption topology FAILS** — UMA-s-1p1 (oc20/omat) inverts well; prefers hollow/bridge, misses Li+–N3- on-top charge-transfer well. Gives 0.237 eV hollow route vs DFT/paper 0.133 eV on-N. `db/properties/diffusion.json`.
- **Recovery:** DFT NEB nspin=2 confirms on_N as minimum (E = −1485.18 Ry, force 0.0018 ✓ at 2026-06-09 09:49). Barrier(hollow − on_N) preliminary = **+148 meV vs Cui 2023 133 meV (+11 %)**. hollow_s2 still iterating to converge; bridge_s2 (final saddle) pending.
- Paper claim falls back to DFT/literature: Li3N(on-N) 0.133 vs lithiated carbon (LiC6) ~0.24–0.30 → ~2× faster Li adatom diffusion, NOT the original 10⁴× / 5.9× claim.

### Must caveat
- The 5.9× / 10⁴× claim in `db/properties/diffusion.json` `paper_claim` is RETRACTED — based on thin-slab UMA result that did not survive the proper 6-layer N-exposed slab. Caveats already in JSON.
- Same-protocol comparison is the robust paper claim, not absolute values.

---

## 9. Site-preference codebase review (separate workstream)

(historical, but still required for any reviewer question about Y@P, Si@P, Ge@P, etc.)
- Three review cycles (`reviewer_prompt_site_preference_v1/v2/v3_signoff.md`) → APPROVED.
- Evidence-graded literature override: `KNOWN_SUBSTITUTIONS` dict in `scripts/doping/site_preference.py` with `EVIDENCE_LEVELS` and `_LIT_SCORE_FLOOR` {dft_exp:0.60, exp:0.55, analog:0.50, rietveld:0.42}. Y→P_4b tagged 'rietveld' (weak).
- Two-codebase reconciliation: `scripts/doping/` (assistant's reviewed) vs `tools/doping/` (cascade-side); cascade uses tools/doping/. Both patched (d_min interstitial 1.8→2.0; Y@P literature override added to tools/doping/site_preference.py on kserver — gabia-local).
- Acceptor charge compensation now real (Li interstitial finder, cKDTree + farthest-first).

---

## 10. Nd2O3-doped modelc (Paper #2 main track)

### Status & db
- Structure FINAL (run6, E=−3566.20971 Ry, force 0.0044, etot 1e-4 converged). Composition Li48P10Nd2S41O3Cl16, 120 atoms, x=0.20. `db/compositions/modelc_nd_doped.json`.
- Track 1 (Nd→Li, primary) vs Track 2 (Nd→P, control to demonstrate instability) — Track 1A (O@16e PS4 corner) winner by 0.67 eV/O over Track 1B (O@4d free site).
- HSAB mechanism: Nd³⁺ 4f³ anisotropic polarization on adjacent O²⁻ strengthens Nd–O AND P–O (`track1A_vs_1B_HSAB_mechanistic_insight`). One-line: Nd 4f³ vs Ce 4f⁰ = mechanistic distinction.
- Zhao 2025 Ce/O critique (Park BML challenge): SI doesn't support P-site; Ce likely at Li-site analogous to our Nd. `db/literature/zhao2025_critique.md`.
- AFM x=0.02 group data: LPSCl1.6 20.3±0.2 GPa adhesion 356, Nd2O3 20.7±0.2 adhesion 300 — within error.

### Current compute (k-test stuck)
- 3_dft_eos_v7 / pair01 / v0_champion: run6 = 2×2×1 converged (E = −3566.20971 Ry). 4×4×1 k-test SCF iter#1225 acc 1e-5, did NOT converge — jammed in DIFFERENT magnetic basin (E=−3566.162 = HIGHER than 2×2×1, energetically impossible if same basin). 6×6×1 had `diago_david_ndim` namelist error (fixed). Both restarted with run6 charge-density seed (`startingpot/wfc='file'`, prefix copied to `nd_pair01_v0_k441.save/`), conv_thr relaxed to 2e-6 / 2e-5. NEW job 753206 PENDING (start 2026-06-10 13:39, 24 h queue).
- `db/compositions/modelc_nd_doped.json` `DFT_settings`: U(Nd 4f) = 6 eV planned; ACTUAL run6 input uses **U = 8 eV** (user choice). Note discrepancy in any methods section.

### Must follow (pipeline order)
1. k-test (k441 / k661) finishes from restart → ΔE/atom < 1 meV ⇒ keep 2×2×1, > 1 meV ⇒ adopt larger mesh.
2. Tight relaxation at chosen k-mesh (+U + ISPIN=2 + force conv tighter).
3. 5-target post-proc (`paper_goals_5_targets`): Nd 4f PDOS, SEI decomp hull (LiCoO2-style), SEI phase gaps, COHP Nd-S/Nd-O/P-O, Cij + thermal anneal.
4. EOS (DFT) for B0 with chosen k-mesh. UMA gave B0=18.9±1.4 GPa already (directional only, f-electron unreliable).

### Caveats
- f-electron UMA reliability LOW; directional only.
- B0 from EOS is k-robust (curvature cancels systematic k-error) — for B0 alone, 2×2×1 is sufficient even if k-test shows >1 meV.

---

## 11. Tools & scripts inventory (where the code lives)

- `tools/oxidation/esw_grand_potential.py` — 0-pressure grand-potential ESW.
- `tools/oxidation/constrained_esw.py` — Fitzhugh strain-explicit (rewritten 2026-06-09; previous augmented-hull version discarded as composition-blind).
- `tools/oxidation/interface_reactivity.py` — pymatgen InterfacialReactivity for chemical (zero-bias) electrolyte/cathode reactivity.
- `tools/modelc_v3/disorder_ensemble_diffusion.py` — UMA disorder-vs-Ea ensemble.
- `tools/modelc_v3/elastic_mlip_600K.py` — UMA 600 K snapshot elastic.
- `tools/modelc_v3/aimd_mlip.py` — basic UMA AIMD per-T Arrhenius.
- `tools/modelc_v3/plot_elf_3d_iso.py`, `plot_elf_slice.py` — ELF figures (label arg added 2026-06-08 so comp1 vs modelc plot don't share modelc_v3 title).
- `tools/modelc_v3/fit_bm_eos.py` — BM3 EOS fit (used for both comp1/modelc PRIMARY).
- `scripts/doping/site_preference.py`, `substitute_struct.py`, `analyze_screening.py` — reviewed doping codebase (with evidence-graded floor).
- `tools/doping/site_preference.py`, `substitute_compound.py`, `master_batch_273.sh` — cascade-side (gabia-local patches).
- `tools/doping/register_cascade_to_db.py` — registers cascade runs to `db/properties/doping_cascade.json` (gabia-local, NOT pushed to vm; we have `doping_cascade_verified.json` snapshot instead).
- `tools/oxidation/esw_check.py` (parked) — qualitative competing-phase span; do NOT call it "real ESW". Tier_cascade.sh:271–273 caveat.

---

## 12. Machines / artifacts that are NOT in the vm repo

| | machine | what's there |
|---|---|---|
| EOS / elastic / ELF cube / Bader / COHP raw | v100 container (915bdbbd37ca) | `/home/ubuntu/work/runs/{comp1_v3,modelC_v3}/...` |
| Disorder MD per-T results | v100 | `comp1_v3/disorder_diffusion/`, `modelC_v3/disorder_diffusion/` |
| Cascade run dirs + champion xyz + tier scripts | gabia (kserver116-27) | `/data/work/runs/multi_category_2026_05_26_v23/`, `/data/work/repo/...` |
| Nd2O3 DFT (run5/run6, k-test, EOS v7) | KISTI (glogin01) | `/scratch/x3430a02/kgy/nd_doped_modelc/...` |
| Li3N DFT NEB (current on_N done, hollow/bridge running) | gabia | `/data/work/.../li3n_dft/...` |
| MP key + pymatgen environment | gabia (set) ; v100 (pymatgen present, no key) | use gabia for ESW/interface_reactivity |
| UMA fairchem env | v100, gabia, KISTI | all three have UMA-s-1p1 |
| 273 cascade master orchestrator | gabia | `tools/doping/master_batch_273.sh` (3 bugs fixed 2026-06: uma env, BATCH_DIR=05_26, backtick) |

---

## 13. Provenance / verification status

| Result | Status | Source of truth |
|---|---|---|
| Paper#1 EOS (comp1 B0=26.23, modelc 21.71) | ✅ confirmed | `db/properties/eos.json` PRIMARY entries |
| Paper#1 clamped-ion elastic (52.31/52.30 identical) | ✅ confirmed | `db/properties/elastic.json` dft_0K_clamped |
| Paper#1 relaxed-ion elastic (22.06/27.66, +24%) | ✅ confirmed | dft_0K_relaxed_ion |
| Paper#1 600 K MLIP elastic (comp1 stiffer) | ✅ confirmed (demoted SI) | mlip_600K_snapshot_v3 |
| Paper#1 bonding (ELF/COHP/Bader identical PS4) | ✅ confirmed | `db/properties/electronic.json`, `bonds.json` |
| Paper#1 oxidation Axis 1 grand-potential | ✅ confirmed (matches Gil-González K_eff=0) | `oxidation_stability.json` |
| Paper#1 oxidation Axis 2 constrained ESW | ✅ comp1 vs modelc; Cl-scan reproduces Gil-González trend | constrained_esw_OUR_CALC; constrained_esw_cl_scan.json |
| Paper#1 oxidation Axis 3 interface | ✅ confirmed (matches Zuo direction; gas limitation noted) | interface_reactivity_results.json |
| Paper#1 oxidation Axis 4 calendar | external (Wu 2026 read) | wu_2026_calendar_aging_FULL_PAPER_READ |
| Paper#1 conductivity Ea (paper-grade headline) | PARTIALLY RETRACTED | li_transport.json mechanism_interpretation pending modelc d=0.5 |
| Paper#1 disorder-ensemble Ea | comp1 ✅, modelc pending | docs/transport/disorder_ensemble_2026_06_09.md |
| Paper#1 VACANCY PARADOX RESOLVED | ✅ Kim 2025 backs relaxed-ion | elastic.json vacancy_paradox_resolved + literature_kim_2025 |
| Paper#2 cascade 14 dopants | ✅ all 41 converged | docs/cascade/cascade_dopants_2026_06_09.md |
| Paper#2 Nd2O3 structure | ✅ FINAL run6 | KISTI run6 |
| Paper#2 Nd2O3 5 paper-targets | NOT STARTED | pending k-test → tight relax |
| Paper#2 Li3N barrier | PRELIMINARY DFT (148 meV, Cui 133) | gabia li3n; bridge_s2 pending |

---

## 14. Anti-list (do NOT do these things in the report)

- Quote UMA absolute elastic / EOS / D side by side with QE/DFT absolute values without an explicit method note. UMA scale ≠ QE scale.
- Quote comp1 d=0.00 Ea = 1.17 eV anywhere as "the ordered Li6PS5Cl Ea". It is a low-T statistics artifact.
- Quote comp1 d=0.00 D(600 K) = −3.7e-7 cm²/s as "negative diffusion". It is below-noise diffusion.
- Cite the `mlip_600K_snapshot_v3` row as a headline number. It is supporting / SI only after 2026-06-08 demotion.
- Cite the 5.9× / 10⁴× Li3N vs LiC6 ratio. Retracted; use ~2× from literature.
- Cite `esw_check.py` as "ESW". It is a qualitative competing-phase-energy-span hint.
- Cite the BROKEN `lpscl_relaxed_conv_52atoms.cif` for any comp1 figure. Use `comp1_V0_k444.cif` instead.
- Treat 0-pressure window numbers as cell-level performance. They are intrinsic bulk thermodynamics.
- State "Cl-rich more/less oxidation stable" without naming the axis (1/2/3/4).
- Quote our Nd absolute B0 / E from UMA as exact. f-electron UMA reliability LOW.
- Push to GitHub without `git config user.email noreply@anthropic.com && --reset-author` (Stop-hook will block).

---

## 15. Open compute (running / pending)

| Job | Machine | ETA |
|---|---|---|
| Nd k441 + k661 SCF (from run6 charge density seed) | KISTI 753206 | start 2026-06-10 13:39 |
| Nd 273 cascade (Sc2O3 step 40/273) | gabia | continuous |
| Li3N DFT NEB (hollow_s2 converging, bridge_s2 next) | gabia | hours |
| comp1 / modelc disorder MD (modelc 12/24 done) | v100 | hours |
| b2o3 DFT EOS (v100, v1.02 SCF DIVERGE pending) | v100 | hours |

---

## 16. Files / locations for the report writer

```
db/properties/
  bonds.json
  electronic.json
  eos.json
  elastic.json                  + literature_kim_2025_halogen_modulus
                                  + literature_kim_JMCA_2026_Irich
  li_transport.json             + disorder_ensemble_2026_06_09 block
  diffusion.json                (Li3N + adatom paths)
  oxidation_stability.json      + 4 literature blocks + 4-axis capstone
  doping_cascade_verified.json  (Al2O3 + 13 more verified 2026-06-09)
  literature_tensions_audit.json (5 tensions, status per item)

db/compositions/
  modelc_nd_doped.json          (Paper #2 main, full plan)

db/structures/
  comp1_V0_k444.cif/.xyz        AUTHORITATIVE comp1
  doping/Al2O3_*_champion.xyz   Al2O3 champions (only these are vm-side)

db/literature/
  refs.json
  lpscl_doping_precursor_compounds_review.md
  sundar_2025_lpscl_coating.md
  zhao2025_critique.md          (Ce/O critique, refutation)

docs/
  transport/disorder_ensemble_2026_06_09.md
  cascade/cascade_dopants_2026_06_09.md
  oxidation/constrained_esw_cl_scan_2026_06_09.md
  tech_report_checklist_2026_06_09.md  (this file)

tools/
  oxidation/{esw_grand_potential,constrained_esw,interface_reactivity}.py
  modelc_v3/{disorder_ensemble_diffusion,aimd_mlip,elastic_mlip_600K,
             fit_bm_eos,plot_elf_*}.py
  doping/                       (cascade-side; gabia-local for runs)
  neb_diffusion/                (Li3N + adatom)

reviewer_prompt_site_preference_v{1,2,3_signoff}.md   (site-preference review trail)
```

---

End of checklist.
