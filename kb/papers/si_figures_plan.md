# SI Figures Plan — Choi 2025 Analogs

Concrete roadmap mapping our data/tools to Choi 2025 SI structure.
Numbers below are our actual values from `kb/papers/final_report_v2.md`.

## Overview

Choi 2025 SI has **19 figures + 3 tables**. We target a matching 5-part structure:
1. Convergence tests (slab thickness, seed count)
2. MLIP validation (DFT vs UMA energy/force)
3. Interface characterization (side views, gap, strain)
4. Stress / bond analysis (mechanism)
5. Distribution statistics (histogram, paired)

---

## Feasibility Matrix — What We Can Derive NOW

| Our SI item | Choi analog | Tool | Data status |
|-------------|-------------|------|-------------|
| **Fig SI-1** NCM 1L vs 5L Wad | Fig S1 (Cu layer convergence) | `plot_ncm_convergence.py` | ✅ ready |
| **Fig SI-2** Seed running-mean | Fig S5 (SMD param convergence) | `plot_wad_stats.py` | ✅ ready (20 seeds raw) |
| **Fig SI-3** Wad histogram 5 comps | Fig S13/S14 (stress dist) | `plot_wad_stats.py` | ✅ ready |
| **Fig SI-4** Paired Δ(comp2B−comp1) | n/a (our novelty) | `plot_wad_stats.py` | ✅ ready |
| **Fig SI-5** Method comparison | Table S2 (3 construction × 3 stoich) | `plot_method_comparison.py` | ✅ ready |
| **Fig SI-6** Interface snapshots 5 comps | Fig S4/S7 | VESTA (existing `vesta_adhesion_figure_settings.md`) | ✅ ready |
| **Fig SI-7** Interface gap vs Wad | n/a | TODO small script | ✅ data exists |
| **Fig SI-8** Halogen-O bond z-profile | Fig 12 (main text analog) | `analyze_halogen_bonds.py` | 🟡 need xyz on local |
| **Fig SI-9** Li layer partition | Fig S17 | `li_layer_partition.py` | 🟡 need xyz on local |
| **Fig SI-10** DFT vs UMA E trajectory | Fig S3 | 🟡 QE single-point 50 pts × 5 comps (~1 GPU day) |
| **Fig SI-11** DFT vs UMA F scatter | Fig S4 | 🟡 same data, matplotlib hexbin |
| **Fig SI-12** Br-swap ΔWad | Fig S18 / Table S3 | `br_swap_test.py` | 🟡 UMA run (~2 h) |
| **Fig SI-13** Strain coloring | Fig S15/S16 | OVITO modifier | 🟡 manual workflow |
| **Fig SI-14** UMAP training vs ours | Fig S19 | requires UMA training fingerprints | ⏸ high effort |

---

## Our 5-part SI structure (proposed)

### Part 1: Convergence tests
- **SI-1** NCM 1L vs 5L Wad (`ncm_convergence.png`)
  → justifies 1L intentional choice: cross-family only works at 1L (SE density dominates at 5L)
- **SI-2** Seed running mean (10→100) (`wad_seed_convergence.png`)
  → shows n=50 sufficient; 100 used for safety

### Part 2: MLIP validation
- **SI-10** UMA vs DFT energy trajectory (comp1 MD snapshots, 5 comps × ~10 snapshots)
- **SI-11** UMA vs DFT force MAE scatter (Choi benchmark: 0.10–0.22 eV/Å — we target < 0.1)
- Table summarizing: B₀ agreement (UMA 26.9 vs DFT 26.5, 1.5% — better than Choi 2.8–4.6%)

### Part 3: Interface characterization
- **SI-6** Side-view snapshots × 5 comps (VESTA, ~15 Å z-crop around interface)
- **SI-7** Interface gap vs Wad (gap = SE_zmin − O_zmax, scatter 5 comps)
- **SI-13** OVITO strain coloring (atomic equivalent strain, Li5.4 vs Li6)

### Part 4: Mechanism
- **SI-8** Halogen-O bond count z-profile (Cl vs Br, 5 comps)
  → quantifies halogen-specific interfacial bonding
- **SI-9** Li layer partition (1st/2nd/3rd) (fraction of Li within 3 Å of NCM O)
  → vacancy-mediated anchoring evidence
- **SI-12** Br-swap ΔWad (comp1 + 1 Br vs comp2B − 1 Br)
  → causal test of Br polarizability hypothesis

### Part 5: Distribution statistics
- **SI-3** Wad histogram (5 comps, 100-seed density)
- **SI-4** Paired Δ per seed (comp2B − comp1): shows systematic reversal
- Table: mean, std, median, min/max per comp (auto from `wad_summary.json`)

---

## Concrete commands to generate ready items

```bash
# Part 1 & 5 (data already in db/)
python tools/plot_wad_stats.py
python tools/plot_ncm_convergence.py
python tools/plot_method_comparison.py

# Part 3 & 4 (run on V100/KISTI where xyz files are)
python tools/analyze_halogen_bonds.py comp*_v5xy_s*.xyz --plot
python tools/li_layer_partition.py comp*_v5xy_s*.xyz

# Part 4 (one UMA run per swap ~20 min)
python tools/br_swap_test.py comp1_v5xy_s45.xyz --swap Cl_to_Br
python tools/br_swap_test.py comp2B_v5xy_s46.xyz --swap Br_to_Cl
python tools/br_swap_test.py comp3_v5xy_s45.xyz --swap Br_to_Cl
```

---

## Values we already have (for SI tables)

### Table SI-1 — NCM thickness convergence (from Section 5-2, 5-5)
| Comp | Family | 1L mean±std | 5L mean±std |
|------|--------|------------|-------------|
| comp3 | Li5.4 | 2.328±0.490 | 2.826±0.604 |
| comp4 | Li5.4 | 2.250±0.437 | 2.383±0.805 |
| comp5 | Li5.4 | 2.280±0.335 | 2.061±0.824 |
| comp1 | Li6   | 1.151±0.245 | 2.674±0.882 |
| comp2B | Li6  | 1.615±0.417 | 2.718±1.121 |

**Finding:** 1L preserves experimental ordering; 5L reverses it due to SE density mismatch.

### Table SI-2 — Paired Δ (same seed = same registry)
| Pair | ΔWad | SE | n | Significant |
|------|------|----|---|-------------|
| comp3−comp4 | +0.040 | 0.068 | 100 | No |
| comp3−comp5 | +0.048 | 0.059 | 100 | No |
| comp4−comp5 | +0.008 | 0.061 | 100 | No |
| comp1−comp2B | **−0.464** | **0.052** | 100 | **Yes** |

**Finding:** Li5.4 Br-effect = noise. Li6 shows systematic comp2B > comp1 reversal.

### Table SI-3 — Method comparison summary
See `method_comparison.json` (auto-generated).

---

## Priority for advisor meeting

⭐⭐⭐ Show these 4 figures (all ready):
1. `wad_seed_convergence.png` — "100 seeds is plenty, n=50 converged"
2. `wad_histogram.png` — "distribution shape per comp"
3. `ncm_convergence.png` — "why 1L NCM (intentional), not a mistake"
4. `method_comparison.png` — "we tried 4 methods, chose 1L v5"

⭐⭐ After advisor feedback:
5. `wad_paired_deltas.png` — "comp2B>comp1 is NOT noise (100-seed paired)"
6. VESTA side-views × 5 comps — existing settings, 30 min work

⭐ If time allows (new calcs):
7. Halogen-O bond z-profile (~1 h run per comp)
8. Br-swap ΔWad (~2 h total)
9. UMA-DFT trajectory validation (~1 GPU day)
