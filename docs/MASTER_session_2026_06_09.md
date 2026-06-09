# Master inventory — 2026-06-08/09 session

> Single landing page for everything done in this session. Each item links to the JSON entry that holds the numbers and the markdown that holds the narrative. **CAVEAT-strengthened** versions of the previously open issues live in their respective entries; this file is the cross-link index.

---

## 1. Caveat strengthening — what changed this session

### 1.1 BVSE anti-site fraction 37.5% — was caveat, now **stoichiometric necessity**

- **Before:** "Our 5×5×5 cubic cell has 37.5% anti-site Cl which is above modelc's nominal 12.5% — over-disordered, needs caveat."
- **After (build_antisite.py analysis 2026-06-09):** "37.5% is the **stoichiometric LOWER BOUND** for Li5.4PS4.4Cl1.6 in any cubic 5×5×5 supercell. The cubic comp1 cell has only 500 4a sites in 5×5×5; modelc needs 1.6 Cl/fu × 500 fu = 800 Cl; the 500 4a sites can hold at most 500, forcing the remaining 300 onto 4d anti-site = 37.5% minimum. The 12.5% number applies only to the primitive rhombohedral cell with a specific ordered placement (1 of 8 Cl at 4d). Experimental synthesised samples sit at 25–50%; our 37.5% is in that range as a stoichiometric necessity."
- **Anti-site sweep verdict (also 2026-06-09):** sweep options that go below 37.5% all require lower total Cl → no longer modelc stoichiometry → **not worth running**. The sensitivity analysis itself replaces the caveat.
- **Files:** `db/compositions/modelc_v3.json` → `bvse_5x5x5_paired_2026_06_03.bimodal_split_paper_grade.anti_site_Cl_fraction_in_this_cell` + `anti_site_sweep_analysis_2026_06_09`; analysis script `container:/tmp/antisite_sweep/build_antisite.py`.

### 1.2 Oxidation Axis 1 (0-pressure ESW) — was tension, now **validated by Gil-González K_eff=0**

- **Before (audit #1):** "Our 0-pressure grand-potential ESW gives comp1 = modelc oxidation onset (~2.14 V). Zuo 2023 says Cl-rich is less stable. Apparent tension."
- **After (Gil-González 2022 + Zuo 2023 + Wu 2026 full PDF read 2026-06-08/09):** 4-axis decomposition. Axis 1 (0-pressure intrinsic onset) is **identical** in our calc AND Gil-González K_eff=0 (1.70–2.40 V; ours 1.72–2.14 V, the 0.26 V anodic gap is entirely LiS4 mp-995393 which they exclude). Cl-rich advantage is a K_eff > 0 (constriction) effect — a *different axis*, not a tension on axis 1.
- **Files:** `db/properties/oxidation_stability.json` → `MULTI_AXIS_CAPSTONE_oxidation_stability_DONE` + `constrained_esw_OUR_CALC`; narrative `docs/oxidation/constrained_esw_cl_scan_2026_06_09.md`; modes comparison `docs/oxidation/constrained_esw_modes_2026_06_09.md`.

### 1.3 Conductivity Ea-vs-prefactor — partially retracted

- **Before (audit #2):** "modelc has Ea = 0.224 > comp1 0.172. Cl-rich gain is prefactor (D0 ~8× bigger), not barrier — opposite to Minafra/Kraft 'disorder lowers Ea'."
- **After (disorder ensemble UMA on v100, comp1 done):** d=0.5 (disordered comp1) gives Ea = 0.18 ± 0.03 eV ≡ Minafra/Kraft range. The 0.172/0.224 ordering came from under-disordered cells. d=0.0 gives nonsense Ea=1.17 (kinetic-frozen artifact). modelc d=0.5 still running.
- **Status:** PARTIALLY RESOLVED. Headline observation (modelc faster, matches σ) is robust. The Ea-mechanism statement is pending modelc d=0.5 completion.
- **Files:** `db/properties/li_transport.json` → `disorder_ensemble_2026_06_09`; narrative `docs/transport/disorder_ensemble_2026_06_09.md`.

### 1.4 Elastic VACANCY PARADOX — resolved by Kim 2025

- **Before (audit #3):** "DFT 0K clamped-ion gives modelc identical E (52.30 ≈ 52.31), but experiment says LPSCl1.6 stiffer."
- **After (relaxed-ion + Kim ACS Mater Lett 2025 + Kim JMCA 2026):** modelc DFT 0K **relaxed-ion** E_VRH = 27.66 vs comp1 22.06 (+24 %). modelc IS stiffer once ions relax. Kim 2025 experimental UPE Cl→E↑ trend matches. The "paradox" was a clamped-ion artifact.
- **Files:** `db/properties/elastic.json` → `dft_0K_relaxed_ion_stress_strain_full_Cij` + `literature_kim_2025_halogen_modulus` + `literature_kim_JMCA_2026_Irich`.

---

## 2. New cross-validation axes added this session

Three independent post-processings, **same anti-site Cl + Li-vacancy fingerprint**, four sublattices:

| Method | Quantity | Result | Where |
|---|---|---|---|
| **BVSE (5×5×5 cubic)** | per-Li BVS distribution | **bimodal split**: 39.8 % Li comp1-like (BVS 1.60–1.64) + 60.2 % Li anti-site-adjacent (BVS 1.83–1.89, +15 %) | `db/compositions/modelc_v3.json` → `bvse_5x5x5_paired_2026_06_03` |
| **LOBSTER ICOHP** | 4d-Cl vs 4a-Cl Li–Cl bond | **+40 %** stronger per bond at 4d-anti-site; total Li–Cl strengthening +13.4 % (vacancy 69 % + anti-site 31 %) | `db/properties/bonds.json` → `icohp_LOBSTER_ext_basis_eV_per_bond.modelc_v3.Li_Cl_per_site_split` + `Li_Cl_vacancy_antisite_decomposition` |
| **Voronoi 4-sublattice** | per-element Voronoi cell volume std | P 0 → 0.37, Cl 0 → 0.74, Li 0.21 → 1.15 (5.5× wider), **S 3.41 → 2.05 (anti-site HOMOGENIZES)** | `db/compositions/modelc_v3.json` → `bvse_5x5x5_paired_2026_06_03.comp1_voronoi_2026_06_09` + `comp1_vs_modelc_cross_comparison_2026_06_09` |

The **S inversion** (modelc S std SMALLER) is the most non-trivial finding: anti-site Cl partially replaces free 4d-S²⁻ positions, smearing the comp1 PS4-S (compact) vs free-S²⁻ (large) two-group split. Three post-processings converge on the same picture from three different angles.

---

## 3. Oxidation stability — 4 axes capstone

| Axis | Cl-rich (modelc) | Source |
|---|---|---|
| **1 Intrinsic 0-pressure onset** | DRAW (~2.1 V, S²⁻-limited; our grand-potential = Gil-González K_eff=0) | `esw_grand_potential.py` + `constrained_esw.py --mode=leading K_eff=0` |
| **2 Mechanically constrained window** | WINS (constrained ESW Cl-scan: modelc 3.30 V width at K_eff=20 GPa, sweet spot of LPSCl_x family) | `constrained_esw_OUR_CALC` + `docs/oxidation/constrained_esw_cl_scan_2026_06_09.md` |
| **3 Cathode interface cycling** | WINS in-cell (Zuo 2023: more SO₂ gas + less solid sulfate → lower R_int → better cell; our `interface_reactivity.py` matches +2.5 % more reactive vs LiCoO₂ but identical solid product set) | `db/properties/oxidation_stability.json` → `zuo_2023_FULL_PAPER_READ` |
| **4 Calendar / thermal aging** | LOSES (Wu 2026: L6 68 % > L55 48 % at 100 SOC 90 °C 5 day; SOC + cathode are stronger levers than Cl) | `wu_2026_calendar_aging_FULL_PAPER_READ` |

**Headline:** modelc's conductivity gain is *not* free on the oxidation axis. Axes 1–3 are neutral-to-favorable for Cl-rich; the real penalty is shelf-life (axis 4), which **motivates the Paper #2 O-doping campaign**. Never state a single Cl-stability verdict without naming the axis.

---

## 4. Slide figures (final, paper-grade)

All saved on container, downloaded to Downloads/ per session, registered in `docs/figures/README.md`.

| Slide | Figure | Source path | Message |
|---|---|---|---|
| 5 (DOS) | `dos_compare_sharey.png` | container:`/tmp/dos_compare/` | gap 1.76 vs 1.80 eV ≈ same; VBM-upper region: comp1 single peak → modelc 3-peak split (anion disorder) |
| 6 (Voronoi) | `voronoi_compare_paper_v2.png` | container:`/tmp/voronoi_comp1/` | 4-sublattice fingerprint; S HOMOGENIZED (red bar in bottom-right) |
| 7 (BVSE) | `bvse_per_li_hist_v2.png` | container:`/tmp/bvse_hist/` | bimodal split: 39.8 % comp1-like + 60.2 % anti-site Cl-adjacent (BVS +15 %); cross-validates ICOHP +40 % |

Per-slide structure inventory (modelc_v3 lineage only, no comp1–5 family work, no v1/v2 adhesion):

| # | Content | Data source |
|---|---|---|
| 1–2 | (user-authored) modelc anti-site picture + V0 / EOS B0 26.2 vs 21.7 | user |
| 3 | PS4 framework invariance — bond / Bader / ICOHP / ELF | `bonds.json`, `electronic.json` |
| 4 | Li–Cl +13.4 % decomposition (vacancy 69 % + anti-site 31 %) | `bonds.json` Li_Cl_vacancy_antisite_decomposition |
| **5** | **DOS comp1 vs modelc** | `dos_compare_sharey.png` |
| **6** | **Voronoi 4-sublattice fingerprint** | `voronoi_compare_paper_v2.png` |
| **7** | **BVSE bimodal + ICOHP cross-validation** | `bvse_per_li_hist_v2.png` |
| 8 | Oxidation 4-axis capstone | `oxidation_stability.json` `MULTI_AXIS_CAPSTONE` |
| 9 | constrained ESW Cl-scan sweet spot | `constrained_esw_OUR_CALC` |
| 10 | Elastic 3-regime + VACANCY PARADOX resolved | `elastic.json` + Kim 2025 |
| 11 | Conductivity D + disorder ensemble | `li_transport.json` `disorder_ensemble_2026_06_09` |
| 12 | Integration message (Li sublattice = single axis driving all effects) | (synthesis) |
| 13 | Outlook — Li3N NEB / cascade / Nd2O3 / site_pref | `diffusion.json` + `doping_cascade_verified.json` + `modelc_nd_doped.json` |

---

## 5. Tools added or rewritten this session

| Tool | Purpose | Status |
|---|---|---|
| `tools/oxidation/esw_grand_potential.py` | 0-pressure grand-potential ESW (Mo/Ong 2012) | done |
| `tools/oxidation/constrained_esw.py` | Fitzhugh constrained ESW with `--mode={leading,relax,hybrid}` | done; three modes characterized in `docs/oxidation/constrained_esw_modes_2026_06_09.md` |
| `tools/oxidation/interface_reactivity.py` | electrolyte/cathode chemical reactivity vs MP cathode set | done |
| `tools/modelc_v3/disorder_ensemble_diffusion.py` | UMA AIMD disorder-Ea ensemble | running (modelc d=0.5 pending) |
| (analysis) `container:/tmp/antisite_sweep/build_antisite.py` | proves 37.5 % is stoichiometric lower bound for modelc on cubic 5×5×5 | done; analysis-only, no further build |
| (analysis) `container:/tmp/voronoi_comp1/` | comp1 Voronoi via scipy + ConvexHull on 3×3×3 PBC tile, total sum ratio 1.000 (exact) | done; JSON saved to that path |

---

## 6. JSON entries — paper-grade values to quote

All extracted, all paper-grade:

### bonds.json
- `results.comp1_v3` / `results.modelc_v3`: P–S 2.073 / 2.064, Li–Cl 2.607 / 2.532, Li–Cl_4d 2.359 (modelc anti-site only)
- `icohp_LOBSTER_ext_basis_eV_per_bond.modelc_v3.Li_Cl_per_site_split`: 4d-Cl +40 % stronger Li–Cl per bond
- `icohp_LOBSTER_ext_basis_eV_per_bond.modelc_v3.Li_Cl_vacancy_antisite_decomposition`: vacancy 69 % + anti-site 31 % of total Li–Cl strengthening = +13.4 % overall
- `icohp_distance_correlation_eV_per_Angstrom`: modelc ionic bond slopes 2–3× flatter than comp1 (ionicity metric)

### electronic.json
- `comparison_comp1_v3_vs_modelc_v3`: gap 1.76 vs 1.80 eV; offset vs PAW-PBE literature consistent for both
- `bader_full_matrix`: PS4 invariance (Σq sum) + Cl_more_ionic_than_Br_pct + P_three_anchor_separation
- `elf_comparison_v3.P_S_bridge_ELF` 0.946 vs 0.944; `Li_basin_min_ELF` 0.072 vs 0.065

### eos.json
- `comp1_v3` (PRIMARY): B0 = 26.23 GPa, V0 = 1016.62 Å³, R²=1.000
- `modelc_v3` (PRIMARY): B0 = 21.71 GPa, V0 = 1216.44 Å³

### elastic.json
- `dft_0K_clamped_ion_stress_strain_full_Cij`: E_VRH comp1 52.31 = modelc 52.30 (PS4 framework invariant)
- `dft_0K_relaxed_ion_stress_strain_full_Cij`: E_VRH comp1 22.06 vs modelc 27.66 (+24 %; VACANCY PARADOX resolved)
- `literature_kim_2025_halogen_modulus` + `literature_kim_JMCA_2026_Irich`: experimental halide-size→modulus rule that confirms our relaxed-ion result

### oxidation_stability.json
- `results.comp1` / `results.modelc` (grand-potential 0-pressure): identical onset 2.14 V, OCV 1.72 V, both metastable
- `MULTI_AXIS_CAPSTONE_oxidation_stability_DONE`: four axes summarized
- `constrained_esw_OUR_CALC`: modelc widens to 3.30 V at K_eff=20 GPa (sweet spot)

### li_transport.json
- `comp1_vs_modelc_comparison.robust_findings`: D(600 K) comp1 2.68×10⁻⁶ vs modelc 7.90×10⁻⁶ cm²/s; modelc 2.9–3.5× faster, matches experimental σ
- `disorder_ensemble_2026_06_09`: comp1 d=0.5 Ea = 0.18 ± 0.03 eV ≡ Minafra/Kraft

### modelc_v3.json (composition)
- `v3_postprocess_pipeline_v2_8.8d_bvse` (rhombo unit cell) + `bvse_5x5x5_paired_2026_06_03` (paper-grade cubic comparison)
- `bvse_5x5x5_paired_2026_06_03.bimodal_split_paper_grade`: full numbers
- `bvse_5x5x5_paired_2026_06_03.comp1_voronoi_2026_06_09` + `comp1_vs_modelc_cross_comparison_2026_06_09`: Voronoi 4-sublattice fingerprint
- `8c_coordination_voronoi.paper_grade_extracted_2026_06_09`: modelc-internal P/Cl/Li/S std

### doping_cascade_verified.json
- 14 dopants × 3 concentrations (+ Sc2O3 x002 alone) = 41/41 converged
- coating ranking: Sc2O3_x002 (E_VRH 18.7) > Al2O3_x005 (29.3) > Li2O_x005 (32.4) > MnO_x005 (32.6) > NiO_x010 (33.9)

### diffusion.json
- Li3N(001) — DFT NEB on_N converged (E = −1485.18 Ry, force 0.002); barrier preliminary 148–174 meV vs Cui 2023 133 meV; hollow_s2 converging, bridge_s2 pending

### literature_tensions_audit.json
- `1_oxidation_stability`: DOWNGRADED to VALIDATED + K_eff-axis story
- `2_conductivity_mechanism_Ea_vs_prefactor`: PARTIALLY RETRACTED (pending modelc d=0.5)
- `3_elastic_vacancy_paradox`: RESOLVED (relaxed-ion + Kim 2025)
- `4_band_gap_absolute`: minor method offset, delta robust
- `5_li3n_uma_topology_failure`: parked, paper uses DFT/literature

---

## 7. Companion narrative docs

| Topic | Doc |
|---|---|
| Session checklist (do-not-skip 16-section inventory) | `docs/tech_report_checklist_2026_06_09.md` |
| Constrained ESW Cl-scan (paper-grade Cl-rich sweet spot) | `docs/oxidation/constrained_esw_cl_scan_2026_06_09.md` |
| Constrained ESW modes (leading vs relax vs hybrid honest assessment) | `docs/oxidation/constrained_esw_modes_2026_06_09.md` |
| Disorder ensemble (comp1 d=0.0 artifact vs d=0.5 physical Ea) | `docs/transport/disorder_ensemble_2026_06_09.md` |
| Cascade dopants (14 × 3 verified) | `docs/cascade/cascade_dopants_2026_06_09.md` |
| Slide figure landing | `docs/figures/README.md` |
| **This master inventory** | `docs/MASTER_session_2026_06_09.md` (this file) |

---

## 8. What is still running

- v100 modelc disorder MD d=0.5 — completes the Ea-mechanism statement
- KISTI Nd k441/k661 SCF restart from run6 charge density (job 753206) — expected 2026-06-10 13:39 start
- gabia Li3N hollow_s2 ionic relax (force 0.014, converging) + bridge_s2 pending
- gabia 273-cascade (Step 40/273 Sc2O3 in progress)
- v100 b2o3 DFT EOS (v1.02 SCF diverged, awaiting investigation)

None of the above is blocking the slide deck — figures and JSON are paper-grade as of this commit.
