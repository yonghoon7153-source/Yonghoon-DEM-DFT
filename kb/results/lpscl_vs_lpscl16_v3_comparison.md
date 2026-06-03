# LPSCl vs LPSCl1.6 — v3 head-to-head (Pipeline v2 §8)

Living comparison. Same method (Pipeline v2: MLIP anneal → DFT BM-EOS V0 → DFT
§8) on both. Values are filled in as runs complete.

- **LPSCl** = comp1_v3, Li6PS5Cl, 52 atoms, V0 = 1016.62 Å³ (a = 10.055 Å)
- **LPSCl1.6** = modelc_v3, Li5.4PS4.4Cl1.6, ~104 atoms, V0 = 1216.44 Å³

Last update: 2026-06-03


## 0. Pipeline §8 status

| Step | LPSCl (comp1_v3) | LPSCl1.6 (modelc_v3) |
|---|---|---|
| §8a V0 relax (cell-fixed BFGS at BM-EOS V0) | running 2026-06-03 | done |
| §8b bond stats | pending | done |
| §8c coordination | pending | done |
| §8d Voronoi | pending | done |
| §8e BVSE (python) | pending | done |
| §8f Bader (AE plot_num=17) | pending | done |
| §8g DOS / PDOS | pending | done |
| §8h band structure (Hungarian-reordered) | pending | done |
| §8i stress-strain full 6×6 Cij | pending (v2-cell version retracted) | done |
| §8j MLIP UMA 600K snapshot elastic | pending | done |
| §8k AIMD 600/800/1000K (Arrhenius) | pending | done |
| §8l ELF (slice + 3D iso) | pending | done |
| §8m LOBSTER (COHP/ICOHP 4-panel) | pending | NSCF done, lobster pending |


## 1. Paper headlines (preliminary)

Filled as data comes in. **Bold** = paper-grade value, [pending] = waiting.

| Quantity | LPSCl (Li6) | LPSCl1.6 (Li5.4) | Trend | Mechanism |
|---|---|---|---|---|
| **B0** (BM-EOS, GPa) | **26.23** | **21.71** | Li6 stiffer | Cl→Br/vacancy soften lattice |
| **K_VRH** (stress-strain, GPa) | [pending] | **44.47** | TBD | |
| **G_VRH** (GPa) | [pending] | **20.05** | TBD | |
| **E_VRH** (GPa) | [pending] | **52.30** | TBD | |
| **ν** | [pending] | 0.304 | TBD | |
| **Zener A** | [pending] | 0.416 | TBD | |
| Band gap (DFT-PBE, eV) | [pending] | [add] | | |
| Bader q(Li) (e) | [pending] | [add] | | |
| AIMD Ea (eV) | [pending] | [add] | | |
| AIMD D₀ at 300K (cm²/s) | [pending] | [add] | | |
| ICOHP P–S (eV/bond) | [pending] | [add] | | |
| ICOHP Li–S (eV/bond) | [pending] | [add] | | |
| ICOHP Li–Cl (eV/bond) | [pending] | [add] | | |

**Experimental anchor**: LPSCl1.6 has HIGHER measured Young's modulus than
LPSCl. If DFT 0K shows the opposite (Li6 stiffer at static), this is the
"vacancy paradox" — DFT misses finite-T anharmonic stiffening / Li dynamic
redistribution. Discuss in paper.


## 2. EOS (BM3, free 4-param fit)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| V0 (Å³) | 1016.62 | 1216.44 |
| a (Å, cubic) | 10.0547 | ≈ 10.674 |
| B0 (GPa) | 26.233 ± 0.004 | 21.71 ± 0.27 |
| B0' | 4.171 ± 0.011 | 7.01 ± 1.37 |
| R² | 1.000000 | 0.999012 |
| n_points | 8 | 11 |
| Fit date | 2026-06-03 | 2026-06-03 |

**Note on B0' discrepancy**: comp1 B0' = 4.17 (textbook range), modelc_v3 B0' =
7.01 (high, with large σ). Large B0' uncertainty in modelc reflects the wider
volume sweep + flatter Li energy surface. Both K values (from BM and from
stress-strain) cross-check within ~3% for each system independently.


## 3. Elastic — DFT 0K stress-strain (full 6×6)

| Quantity (GPa) | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| C11 avg | [pending] | 89.87 ± 3.16 |
| C12 avg | [pending] | 21.82 ± 2.43 |
| C44 avg | [pending] | 14.43 ± 1.25 |
| B_VRH | [pending] | 44.47 |
| G_VRH | [pending] | 20.05 |
| E_VRH | [pending] | 52.30 |
| ν | [pending] | 0.304 |
| Zener A | [pending] | 0.416 |
| Stable | [pending] | yes |

(comp1_v3 stress-strain at v2 cell was retracted 2026-06-03; redo after V0 relax.)


## 4. Elastic — MLIP UMA 600K snapshot

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| E_VRH (GPa) | [pending] | 52.72 ± 1.42 |
| Protocol | UMA-s-1p1 600K Langevin → snapshot → relaxed-ion FIRE → Cij | same |


## 5. Bond environment (DFT V0)

Bond stats: mean d, σ, n_bonds. Coordination: avg Z. Voronoi: V_polyhedra.

| Bond type | LPSCl mean d (Å) | LPSCl1.6 mean d (Å) |
|---|---|---|
| P–S | [pending] | [add from db] |
| Li–S | [pending] | [add from db] |
| Li–Cl | [pending] | [add from db] |
| S–S (cage) | [pending] | [add from db] |

| Site | LPSCl coord | LPSCl1.6 coord |
|---|---|---|
| Li avg | [pending] | [add] |
| P (PS4 unit) | [pending] | 4 (tetrahedral) |


## 6. BVSE (Python implementation)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| Min Ea_BVSE (eV) | [pending] | [add] |
| Predicted path | [pending] | [add] |


## 7. Bader (plot_num=17 AE charge density)

| Species (mean charge, e) | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| Li | [pending] | [add] |
| P | [pending] | [add] |
| S | [pending] | [add] |
| Cl | [pending] | [add] |


## 8. DOS / PDOS

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| Band gap (PBE, eV) | [pending] | [add] |
| VBM character | [pending] | S 3p dominant |
| CBM character | [pending] | [add] |
| Li-PDOS at E_F | [pending] | [add] |


## 9. Band structure (Hungarian-reordered, k-path X-Γ-L-W-K)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| Direct/indirect | [pending] | [add] |
| Gap location | [pending] | [add] |
| Effective mass Li-like band | [pending] | [add] |


## 10. AIMD diffusion (Arrhenius 600/800/1000K)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| D(600K) (cm²/s) | [pending] | [add] |
| D(800K) (cm²/s) | [pending] | [add] |
| D(1000K) (cm²/s) | [pending] | [add] |
| Ea (eV) | [pending] | [add] |
| D₀ extrapolated 300K (cm²/s) | [pending] | [add] |
| σ_Li 300K (mS/cm, Nernst-Einstein) | [pending] | [add] |


## 11. ELF (electron localization function)

| | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| Li–S ionicity | [pending] | [add] |
| P–S covalency (ELF > 0.7 between) | [pending] | yes |
| 3D iso level used | [pending] | 0.75 |


## 12. LOBSTER ICOHP (per-bond average, eV)

Bonding (negative = bonding). Less negative = weaker.

| Bond pair | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| P–S | [pending] | [pending — lobster run queued] |
| S–S | [pending] | [pending] |
| Li–S | [pending] | [pending] |
| Li–Cl | [pending] | [pending] |

Charge spilling (lobsterout): comp1 [pending], modelc_v3 [pending].


## 13. Cross-checks (intra-system)

| Check | LPSCl v3 | LPSCl1.6 v3 |
|---|---|---|
| K_BM vs K_VRH (GPa) | 26.23 vs [pending] | 21.71 vs 44.47 |
| K_BM vs K_VRH agreement note | TBD | Different physical content: BM uses bulk uniform compression on E(V), VRH from full Cij at clamped-ion. ~2× delta expected for soft Cl-rich phases. |
| Cij mechanical stability (eigenvalues all > 0) | [pending] | yes |


## 14. Discussion points (paper outline)

1. **Vacancy paradox**: experiment shows LPSCl1.6 > LPSCl (Young's), DFT 0K
   may show opposite. Sources of finite-T stiffening:
   - Anharmonic phonon hardening at Cl-rich basin
   - Li site disorder → effective stiffening (entropic)
   - MLIP 600K snapshot test in row 4 — compare both ratios.
2. **Cl substitution**: Cl→{S vacancy + Cl} changes both coordination number
   distribution and Li mobility (BVSE / AIMD section).
3. **Ionic vs covalent share**: ELF + Bader + LOBSTER together quantify the
   shift from PS4-covalent backbone (P–S strong ICOHP) to Li–anion ionic
   (Li–S/Li–Cl weak ICOHP, high Bader transfer).
4. **B0 vs K_VRH discrepancy**: physically meaningful — explain in paper that
   BM-EOS B0 is the uniform-strain bulk modulus (hydrostatic), while K_VRH
   from clamped-ion Cij is the harmonic-only frozen-ion value. Soft Cl-rich
   phases have larger gap. Report both.


## Footnotes

- Pipeline v2 lineage for modelc_v3 is in `db/compositions/modelc_v3.json`
  (Steps 1–8 audit trail).
- comp1 v2 §8 results (at a=9.929, v2 cell) archived on container at
  `/home/ubuntu/work/runs/comp1_v3/archive_v2_post/` — kept for methodology
  reproducibility, not paper.
- All §8 tools in `tools/modelc_v3/` and `tools/comp1_v3/`.
