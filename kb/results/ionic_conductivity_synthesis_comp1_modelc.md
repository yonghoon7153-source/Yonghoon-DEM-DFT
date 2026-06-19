# Ionic conductivity: LPSCl (comp1) vs LPSCl1.6 (modelC) — full synthesis

**Headline:** σ(LPSCl1.6) ≈ 4× σ(LPSCl); Ea 0.253 → 0.224 eV (matches experiment
0.25/0.22). Cause = **anti-site Cl flattens the Li site-energy landscape (Ea↓)** +
**Cl-induced Li vacancies raise the carrier prefactor (D0↑)** — roughly equal
contributions. Probed by three independent, mutually consistent methods.

---

## Three probes (all point the same way)

### 1. Static structure (geometry / valence / bonding)
| descriptor | comp1 LPSCl | modelc LPSCl1.6 | tool |
|---|---|---|---|
| free-anion (cage) Cl fraction | 0.50 | **0.80** | `cage_jump_descriptors.py` |
| Li on Cl-coordinated sites | 0 % | **55.6 %** | (Li delocalisation) |
| occupied cages | 4 | 8 | |
| BVSE Li population | single (BVS 1.60–1.64) | **bimodal** 39.8% LPSCl-like + 60.2% **+15%** (BVS 1.83–1.89, adjacent to anti-site Cl) | BVSE 5×5×5 |
| static low-BVSE channel | 8.75 % | 7.4 % (**−15%**) | BVSE |
| ICOHP per Li–Cl bond | baseline | **+40%** at anti-site | LOBSTER |

→ The **4d-Cl anti-site** is the structural actor: it splits the Li environment
into two populations (bimodal BVS), raising ~60% of Li to a less-stable (+15% BVS)
state. "BVS +15% ↔ ICOHP +40% per-bond" = same anti-site seen by two probes.

### 2. Dynamic quantitative (AIMD-MLIP, UMA-s-1p1, 600/800/1000 K)
| | comp1 LPSCl **4fu** | modelc LPSCl1.6 5fu |
|---|---|---|
| D(600 K) cm²/s | 3.09e-6 | 7.90e-6 |
| D(800 K) | 1.03e-5 | 2.05e-5 |
| D(1000 K) | 2.20e-5 | 4.55e-5 |
| **Ea (eV)** | **0.2532** | **0.2235** |
| D0 cm²/s | 4.11e-4 | 5.75e-4 |
| σ_NE(300 K) mS/cm | 3.35 | 13.96 |

(Source `db/properties/li_transport.json`; modelc independently reproduced by
`msd_origin.py` → Ea 0.2235, D600 7.90e-6, D300 1.01e-7 — exact match, tool validated.)

**Dual mechanism decomposition** (σ ratio ≈ 4×):
- **Ea effect** exp[(0.253−0.224)/kT] ≈ **1.75×** @600K — per-hop barrier ↓ from anti-site landscape flattening.
- **D0 effect** 5.75e-4 / 4.11e-4 ≈ **1.41×** — vacancy carrier density ↑.
- 1.75 × 1.41 ≈ 2.5× @600K, widening to ~4× @300K (Ea term grows at low T).

### 3. Dynamic visual (AIMD)
- **Li⁺ probability-density isosurface** (`li_density_cube.py` → VESTA) = the
  *dynamic twin* of the static BVSE channel map (Gil-González ESM 2022 f1/f2/f3
  style). modelc cube validated: ∫ρ = 27.000 = n_Li (correct normalisation).
- **van Hove Gs(r,Δt)** + cage-resolved hop stats (`aimd_jump_stats.py`):
  jump-distance distribution (doublet / intra-cage / inter-cage).

---

## Why Ea drops (the mechanism, precisely)

**Dominant — energy-landscape flattening.** Anti-site Cl on the 4d site raises the
energy of neighbouring Li sites (bimodal BVS: 60% of Li pushed +15%). A higher (less
stable) site = a **shallower well** = a smaller well-to-saddle barrier → Ea↓. This is
the Minafra/Kraft/Schlem "disorder lowers Ea" effect, made visible here by the BVSE
bimodal split.

**Secondary — percolation / alternative routes.** Macroscopic Ea = the lowest-barrier
*percolating* (inter-cage) route. Vacancies + disorder open lower-barrier detours, so
the effective barrier (min over routes) drops. This is the "more paths" intuition —
but note it is **dynamic (vacancy-enabled)**, NOT static: the static BVSE channel
actually *shrinks* (−15%), so "more channels" is wrong in the geometric sense.

**Separate from Ea — carriers raise D0.** Aliovalent Cl⁻-for-S²⁻ creates Li vacancies
→ more mobile carriers → larger prefactor (D0 ×1.41). This boosts σ but is not an Ea
effect.

**Static-vs-dynamic reconciliation (key):** static BVSE channel −15% but σ ×4 is NOT a
contradiction — BVSE ignores Li vacancies, which are the actual driver (lower barrier +
more carriers). AIMD sees the vacancies; BVSE does not. The two are complementary
(static landscape + dynamic transport).

---

## Tools (all numpy-only, in `tools/ionic/`)
- `cage_jump_descriptors.py` — static cage Cl-fraction + Li delocalisation.
- `msd_origin.py` — MSD/Arrhenius → Origin CSVs (3-panel: Li MSD vs t / Arrhenius / per-element MSD).
- `aimd_jump_stats.py` — van Hove Gs(r,Δt) + cage-resolved inter-cage hop rate + MSD/D.
- `li_density_cube.py` — Li⁺ probability density → Gaussian .cube (VESTA isosurface).

## Figure plan (ionic-conductivity axis)
1. **MSD 3-panel** (Origin, `msd_origin.py` CSVs) — comp1 vs modelc.
2. **Arrhenius** Ea 0.253 vs 0.224 (= panel b; matches exp exactly).
3. **van Hove / inter-cage hop** — dynamic intra/inter-cage barrier evidence (the Ea↓ proof).
4. **Li density isosurface** (VESTA) — dynamic channel, comp1 vs modelc, same level/orientation.
5. (existing) **BVSE bimodal + ICOHP +40%** — static anti-site evidence.

## Status
- **modelc**: complete + validated (MSD CSVs, Li cube ∫ρ=27, Ea 0.2235).
- **comp1**: must use **4fu natural cell** (5fu = artificial-supercell artifact, Ea 0.172;
  `db/properties/li_transport.json`). 4fu trajectory was transient on gabia (cleaned) →
  **re-running on V100** (`~/mlmd_4fu_comp1_rerun`, `aimd_mlip.py`, same protocol). When
  done: run `msd_origin.py` + `aimd_jump_stats.py` + `li_density_cube.py` → comp1 side.

## Caveats
- UMA-s-1p1 overestimates absolute D ~3–5× for LPSCl family → quote **Ea + ratio**, not
  absolute σ. (σ_NE H_R=1 is conservative; bulk-vs-pellet also raises calc above expt.)
- comp1 MUST be 4fu (cubic F-43m natural); 5fu cubic supercell is artificial → Ea artifact.
- A single-Li static-lattice NEB barrier would overestimate Ea ~3× (cf. Ma JMCA 2024
  0.87–0.98 vs expt 0.25–0.29) → for quantitative Ea use AIMD, NEB only for trend/mechanism.

## Key references
- Gil-González et al., *Energy Storage Mater.* **45**, 484 (2022) — Cl-substitution synergy (σ + stability), Li-density channel maps.
- Ma et al., *J. Mater. Chem. A* **12**, 27011 (2024) — intra/inter-cage NEB barriers.
- Taklu et al., *Nano Energy* **90**, 106542 (2021) — doublet/intra/inter-cage geometric descriptors.
- Schlem 2020 / Minafra / Kraft — disorder-lowers-Ea narrative; LPSCl Ea ~0.25, Cl-rich ~0.22.
