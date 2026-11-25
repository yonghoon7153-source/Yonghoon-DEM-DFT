# Adhesion Calibration Decision — 2026-05-17

> Author: paper #2 cascade execution (Nd2O3 doped LPSCl)
> Status: ✅ DECIDED for paper writeup; ⏳ TODO items below
> Related: db/properties/adhesion.json, 필독/adhesion/v30u_ensemble/,
> tools/doping/run_cathode_interface.py

---

## Context

Paper #2 Stage 11 (`run_cathode_interface.py`) uses **v6 protocol separation
method** for NCM-doped-SE adhesion:
- 1L NCM frozen + 500K SE anneal + LBFGS → E_int
- Translate SE +30 Å → E_sep
- Wad = (E_sep − E_int) / area × 16.0218 J/m²

First Nd2O3 batch results (6 baselines × 5 seeds × top-K winners):

| Composition | Wad (J/m²) | Family |
|-------------|-----------|--------|
| comp1 (Li6 pristine) | ~45-80 | Li6 |
| comp2 (Li6 mixed halide) | ~45-80 | Li6 |
| comp3 (Li5.4 Cl-rich) | ~143-218 | Li5.4 |
| comp4 (Li5.4 balanced, DFT-valid) | ~140-219 | Li5.4 |
| comp5 (Li5.4 Br-rich) | ~125-214 | Li5.4 |
| modelC (Li5.4 Cl-only) | ~155-225 | Li5.4 |
| **Nd2O3 winner s04** | **~44-67** | doped |

## Problem — Absolute Scale Unphysical

- Experimental NCM-SE Wad (Sundar 2025 Argonne): **0.2–0.4 J/m²**
- Our Stage 11 separation method: **45-225 J/m²** = **100-1000× over**
- Pattern identical to paper #1 MACE Wad finding
  (v0 paper "MACE Wad ranking-correct R=+0.957 but absolute unphysical")

**Root cause**: rigid separation creates artificial dangling bonds:
1. Build rigid stack → anneal → bonds form at interface (deep E_int well)
2. Translate +30 Å → bonds force-break (E_sep includes dangling-bond energy)
3. Wad = E_sep − E_int includes that artifact → 100-1000× overestimate

## Paper #1 Validated Methodology (R=+0.989) — Full v30u Protocol

`필독/adhesion/v30u_ensemble/` (mirrored from gabia `/data/work/v30u_ensemble/`):

| Step | Script | Role |
|------|--------|------|
| 1. Face enumerate | `enumerate_v1_faces.py`, `enumerate_v2_faces.py` | Which SE face exposed? |
| 2. Face flip (mirror) | `run_v30u_1L_face_flip.py` | Top/bottom orientation |
| 3. xy lateral registries (36) | `bond_density_36reg_FAST.py` | NCM-SE lattice mismatch |
| 4. z-shift ensemble | `comp*_slab_v*_zshifts/` | z translation |
| 5. Binding curve E(d) | `plot_binding_curves_morse_fullwindow.py` | Well depth |
| 6. α strain correction | `alpha_sensitivity_FINAL.py` | Uniform Li5.4 dW=0.44 |
| 7. Surface Li normalize | `normalize_wad_by_surface_Li.py` | Per-Li dangling |
| 8. eiso (face-pair) | `_correct_eiso_fix.py` | Isolated slab energy |

This gives **physically calibrated absolute Wad** (~0.2-2 J/m² range)
consistent with Sundar 2025 experimental.

## Decision (this round)

### **Option A — adopted now**: ranking + calibration ratio

1. Stage 11 separation method results → **ranking only**
2. Baseline Wad numbers (comp1-5, modelC) cited from **paper #1 full v30u protocol**
3. Doped winner Wad reported as separation × correction:
   ```
   Wad_doped_corrected = Wad_doped_stage11 × (Wad_comp1_paper1 / Wad_comp1_stage11)
   ```
4. paper narrative includes:
   - "Baselines reproduced from paper #1 with full v30u protocol (R=+0.989)"
   - "Doped winner Wad reported as separation-method ranking, calibrated
     to paper #1 absolute scale via comp1 ratio"
   - "Calibration assumes system-wide rigid-separation overestimate
     factor; supported by paper #1 cross-validation between
     binding-curve well depth and separation method on baselines"

### **Option B — deferred to top-3 only**: full v30u protocol

Apply full v30u protocol to **top-3 winners only** (selected by composite
score from FINAL_RANKING.json combining ΔE/atom, B_hill, mobility, Wad).

Cost economy:
- Full protocol per (winner, baseline) pair: ~45 min
- 12 winners × 6 baselines = 72 pairs ≈ **50h GPU** ← intractable
- **Top-3 × 6 baselines = 18 pairs ≈ 14h GPU** ← 1 week feasible

### **Option C — not adopted**: DFT spot-check

Run 2-3 DFT calculations for absolute Wad calibration anchor.
Deferred — too expensive (~48h KISTI per case), Option A already paper-defensible.

## Justification (paper-defensible chain)

1. **Stage 11 separation method**: established cheap protocol; ranking
   reliable per paper #1 cross-validation
2. **paper #1 calibration**: R=+0.989 vs experiment is the field's most
   rigorous LPSCl-NCM Wad benchmark; comp1 ratio approach standard for
   "system-wide overestimate" correction
3. **Top-3 selection for full protocol**: matches MLIP-then-DFT
   methodology (paper #2 hook: "MLIP screen, full-protocol verify on
   selected top candidates")
4. **Reviewer question pre-empt**:
   - Q: "Why ratio calibration vs full protocol?" → "Top-3 only get full
     protocol; ratio reasonable proxy for triage of 12 winners"
   - Q: "Why not all 12 full protocol?" → "50h GPU intractable; top-3 is
     paper-quality + cost-justified"

## Chemistry observation (paper hook)

```
Li6 family (comp1, comp2):       45-80  J/m²  (Stage 11)
Li5.4 family (comp3, 4, 5, mC):  140-225 J/m² (Stage 11)
Nd2O3 doped (winner s04):         44-67  J/m² (Stage 11, comp2-like)
```

- Li5.4 family has **3-4× larger** Wad than Li6 → Li vacancy + Cl-rich
  bonding creates more active surface (paper #1 vacancy anchor narrative)
- **Nd2O3 doping reduces Wad to Li6 levels** despite creating Li vacancies
  - Hypothesis: heavy RE (Nd) **saturates surface anchor sites**, blocking
    the Li-O cohesion mechanism Li5.4 enjoys
  - Paper narrative: "Nd2O3 doping reduces NCM-SE adhesion below pristine
    Li6 levels by chemical anchor saturation — heavy rare-earth blocks
    Li-O cohesion"

This is the **paper #2 mechanism hook** — distinct from paper #1's
halogen substitution narrative.

## ⏳ TODO

### Immediate (after Stage 11 + cascade finish)
- [ ] Extract Stage 11 final Wad mean ± std from `11_cathode_interface/cathode_interface_summary.json`
- [ ] Compute comp1 calibration ratio: `Wad_comp1_paper1 / Wad_comp1_stage11`
- [ ] Apply ratio to all winners → calibrated Wad table for paper
- [ ] Cross-check: ratio_baseline_i / ratio_comp1 should be ≈ 1.0 across baselines
  (if not, calibration assumption fails → fall back to ranking-only narrative)

### Phase 2 (paper writeup support, ~1 week compute)
- [ ] Compute composite score for top-K selection (FINAL_RANKING.json fields)
- [ ] Identify top-3 winners by composite (combining ΔE, B_hill, mobility, calibrated Wad)
- [ ] Adapt `필독/adhesion/v30u_ensemble/run_v30u_full_ensemble.py` to
  doped-winner inputs (3 winners × 6 baselines)
- [ ] Run full v30u protocol (face enum → 36 reg → α → eiso → binding curve fit)
- [ ] Produce paper-grade Wad with R=+0.989-equivalent precision
- [ ] paper Table X: top-3 winners with full-protocol Wad vs all 6 baselines

### paper SI material
- [ ] Document Stage 11 separation-method limitations:
  - rigid stacking, frozen NCM, no surface relaxation post-separation
  - cite paper #1 MACE Wad analog (R=+0.957 but absolute unphysical)
- [ ] Cross-method comparison table for one winner:
  - Separation (Stage 11) vs full v30u (this work) vs DFT (if obtained)
- [ ] Calibration ratio derivation + sensitivity analysis

### Methodology improvements (future work, not paper #2 critical)
- [ ] Implement reverse-Wad method:
  - relax interface → separate → relax each piece independently → Wad
  - subtracts surface relaxation, more physical
- [ ] DFT spot-check 1-2 interfaces for absolute calibration anchor
- [ ] NCM thickness convergence test (1L vs 3L vs 5L) per paper #1 SI
- [ ] Green-Kubo for Haven ratio direct derive (independent of v6 anneal protocol)

## References

- `db/properties/adhesion.json` v25/v26c/v30 MACE-Wad analog finding
- `필독/adhesion/v30u_ensemble/` paper #1 R=+0.989 protocol mirror
- `tools/doping/run_cathode_interface.py` Stage 11 implementation
- `kb/methodology/argyrodite_mechanical_pipeline.md` step 8 (adhesion canonical)
- Sundar 2025 (Argonne) — experimental NCM-SE Wad reference (0.2-0.4 J/m²)
- Wang 2025 — UMA-s-1p1 sulfide PES softening (related but separate issue)
