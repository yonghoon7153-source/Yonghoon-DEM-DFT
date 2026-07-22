# 이종기술 (heterogeneous-technology) cathode project

**Separate experimental line from SDCP.**  소립(小粒, 4 µm single-crystal) NCM cathode
program (samples **No.1 / No.2**) and its **poly:small = 5:5 bimodal** blend, on a
**primer-coated SUS** current collector.  Hanyang (이종원 group), BioLogic VSP-300.

## Contents
```
이종기술/
  README.md          ← this file (project index)
  eis/               ← EIS measurement archive (BioLogic .mpr → tidy CSV + catalog + fits)
    raw/  extracted/  eis_catalog.csv  eis_overview.png  README.md
    fits/            ← CNLS equivalent-circuit fits (R_s / R_int / R_w / R_ion)
```

## Materials & cells (lab notes 2026-06-25 → 07-19)
- **Composition** AM:SE:VGCF:PTFE = **80:18:1:1**.  Recipe: vortex 10 min → PTFE →
  ball-mill 1 h → Thinky 2000 rpm 5 min → hot-plate rolling → roll-press on primer-SUS.
- **AM**: No.1 / No.2 = 소립 4 µm single-crystal; **Poly** = large polycrystalline.
  **5:5** = poly:small wt%.  Specific cap (5:5): No.1 202.95 / No.2 206.5 mAh g⁻¹.
- **Areal capacity target 3 mAh cm⁻²**; Li-In anode, 60 °C, 0.1C 2 cyc → 0.2C main.
- **Cells**: 대칭셀(symmetric) 10pi ⌀10 mm (0.785 cm²); 율특셀(rate)·수명셀(life) 13pi
  ⌀13 mm (1.327 cm²).  Full-cell EIS taken on a life cell after charge.

## How this feeds the DEM/MPM model
- **full-cell EIS → R_int** (reaction + primer-SUS collector) — real anchor for **STEP4**
  (V_term = V − I·R_int).  These are the project's OWN measured R_int (vs the SDCP
  manuscript's SBE/DBE/C-SUS panel-e values).
- **symmetric-cell EIS → σ_ion / σ_e transport** — the EIS-TLM method (Minnmann 2021)
  that our σ_ionic calibration references → **validates STEP3** σ network, and the
  **pure-small vs 5:5 bimodal** contrast is the core project comparison.

## Status / open items
- ✅ 24 raw files archived, 12 tidy CSVs, catalog (Ω + Ω·cm²), first-pass CNLS fits.
- ⚠ pure-small symmetric-cell thickness not in notes → needed to turn a transport arc into σ.
- ⚠ symmetric-cell blocking condition (ion- vs electron-) unconfirmed → sets R_ion vs R_e label.
- ⚠ `No2_only_full` run2 diverges from run1 (re-measure / cell issue).
- Next: TLM refit of symmetric cells (lower CPE_a = transport dispersion the R-CPE only
  approximates); wire measured R_int into the STEP4 anchor CSV once labels are confirmed.
