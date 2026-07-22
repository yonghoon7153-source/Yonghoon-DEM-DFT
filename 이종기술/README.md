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
- **symmetric-cell EIS (SUS|cathode|SUS = ion-blocking) → σ_e (electronic)** of the composite
  → **validates STEP3 σ_e** network.  The **pure-small vs 5:5 bimodal** σ_e contrast is the
  core project comparison (measured: No1 0.14→0.093, No2 0.115→0.152 mS/cm — opposite effects).

## ★ R_int collector convention (user, 2026-07)
- **bare-Al collector → SDCP project ONLY** (SBE 18/110, DBE 12/46 Ω·cm² — SDCP manuscript Fig6e).
  Do not use bare-Al for 이종기술.
- **이종기술 (and going forward) → SUS collector**, R_int ≈ **50 Ω·cm²** — the measured full-cell
  mean (SOC100, primer-SUS; `eis/fits/summary_means.csv` = 49.8, auto-updating as cells are added).
- **Why 50 is the "정설"**: it matches the independent ASSB full-cell R_int consensus — **Doerrer
  2021 = 40 Ω·cm²** (SC-NMC/LPSCl full cell) — so the lab's own measurement lands on the same
  tens-of-Ω·cm² full-cell scale.
- ⚠ Layer: this 50 is a **full-cell** R_int (reaction + collector at SOC100, like Doerrer 40),
  NOT the decoupled collector-contact.  Use it as the full-cell series R; if STEP4 also computes
  BV η_kin, the reaction interface is partly shared (same caveat as the Doerrer-40 slot).

## Status / open items
- ✅ 24 raw files archived, 12 tidy CSVs, catalog (Ω + Ω·cm²), CNLS fits + **σ_e** (mS/cm).
- ✅ blocking RESOLVED (SUS ion-blocking → σ_e); composite thickness RESOLVED (40–50 µm, the
  filename 70 µm includes the collector); No2 full run2 = SOC100 degradation (not error).
- Next: **TLM refit** of symmetric cells (CPE_a ≈ 0.3 = transport dispersion the R-CPE only
  approximates) for a cleaner σ_e; run **STEP3 on No.1/No.2 pure & 5:5** and compare σ_e vs the
  measured 0.09–0.15 mS/cm; wire full-cell R_int into the STEP4 anchor CSV (primer-SUS line).

## ⚠ These are REPRESENTATIVE values — re-experiment to firm up
The fits/σ_e above are single representative cells; before treating as final, re-measure:
1. **순수-소립 대칭셀 복합체 두께** (집전체 제외) — pins σ_e (now a ±11 % band from L = 40–50 µm).
2. **Full-cell R_int at a defined SOC / rested state** — the OCV vs 1.3 V arcs differ 2–3× (R_int
   79 vs 30) and `No2_full` run2 mixes in SOC100 aging → a controlled-SOC scan gives a clean R_int.
3. **poly effect direction** (No.1 σ_e ↓ vs No.2 σ_e ↑) — repeat with more cells to tell a real
   sample difference from cell-to-cell scatter.
4. **σ_ion** needs an **electron-blocking** symmetric cell (Li/In contacts) — the SUS cells give
   σ_e only.  (= the planned 3:7 / 5:5 / 7:3 이온전도도 series in the lab notes.)
