# EIS measurement archive (BioLogic EC-Lab, user lab)

Raw electrochemical-impedance-spectroscopy data for the **소립(小粒, 4 µm single-crystal)**
cathode program (No.1 / No.2) and its **5:5 poly:small bimodal** blend, plus the tidy
CSVs and a catalog.  Instrument: **BioLogic VSP-300** (EC-Lab v11.63).

```
raw/         original .mpr (binary data) + .mps (settings), uuid prefix stripped
extracted/   one tidy CSV per .mpr  (freq_Hz, ReZ_ohm, negImZ_ohm, absZ_ohm, phase_deg, Ewe_V, I_mA, cycle)
eis_catalog.csv   one row per measurement — metadata parsed from filename + quick descriptors
```

Regenerate / ingest new files:  `python3 scripts/eis_archive.py`
(needs the **galvani** .mpr parser — see *Parser* below; the committed CSVs make the
archive fully usable without it.)

## Filename taxonomy  `date_sample_blend_cell_...`
| token | meaning |
|---|---|
| `260715` / `260719` | date 2026-07-15 / -19 |
| `No1` / `No2` | sample — **소립 4 µm single-crystal** (two batches/cells) |
| `only` | **pure small-particle** electrode |
| `55_70um` | **5:5 poly:small** blend, **70 µm** thick |
| `full` / `sym` | **full cell** (NCM‖Li-In) / **symmetric cell** |
| `1cyc` | after 1 cycle |
| `C01`/`C02`/`C06` | EC-Lab technique/loop index |
| `1.3V` | EIS taken at 1.3 V cell state (else OCV) |

## Two measurement families → two model axes
- **full cell** (`only_full_1cyc`) → **R_int** (reaction + collector interface) — anchors **STEP4**
  (V_term = V − I·R_int).  Nyquist: R_s (bulk/series) + interfacial arc.
- **symmetric cell** (`sym`) → **σ_ion / σ_e transport** of the composite electrode — the
  **EIS-TLM method** (Siroma/Minnmann 2021) our σ_ionic calibration references.  Lets us
  compare **pure-small vs bimodal(5:5)** transport directly → validates **STEP3** σ network.

## Cell fabrication (lab notes 2026-06-25 → 07-19)
- **Composition** AM:SE:VGCF:PTFE = **80:18:1:1**.  Recipe: vortex 10 min → add PTFE →
  ball-mill 1 h → Thinky 2000 rpm 5 min → hot-plate rolling → roll-press onto **primer-coated
  SUS** collector.  **Areal capacity target = 3 mAh cm⁻²**.
- **AM**: No.1 / No.2 = **소립 4 µm single-crystal**; **Poly** = large polycrystalline.
  **5:5** = poly:small = 5:5 wt%.  Specific capacity (5:5): No.1 = 202.95, No.2 = 206.5 mAh g⁻¹.
- **Cells**: Li-In anode, 60 °C, 0.1C 2 cyc → 0.2C main.  **대칭셀(symmetric) = 10pi (⌀10 mm)**,
  **율특셀(rate)·수명셀(life, EIS source) = 13pi (⌀13 mm)**.
- **Thickness** (primer-SUS ~15 µm excluded where noted): 5:5 sym = **70 µm** (in filename);
  pure-small 면용량2 sym ≈ 50 µm.  ⚠ per-cell thickness for the 260715 pure-small sym is not
  in the notes — **needed to convert a symmetric-cell arc to σ** (σ = L / (R·3) for a blocking TLM).

## ⚠ Units / caveats (read before anchoring)
1. **Area normalization — RESOLVED (Ω·cm² now in catalog).**  Areas inferred from disk
   geometry (lab notes): **symmetric 10pi → 0.7854 cm²**, **full 13pi → 1.3273 cm²**;
   `*_ohmcm2 = *_ohm × area`.  (The `.mps` `Electrode surface area` 0.001 cm² is a placeholder
   and was ignored.)  Areas are inferred from cell type, not measured per file.
2. **`R_s / Re_LF / arc` in the catalog are quick descriptors, not a circuit fit.**
   `R_s` = high-freq real-axis intercept (bulk+series); `arc` = `Re_LF − R_s`
   (interfacial **+** diffusion, not yet separated).  Proper **R_ion/R_int/R_w** needs a
   CNLS equivalent-circuit fit (manuscript Fig S19: r_i + r_e + r_int‖cpe + Z_w).
3. **Symmetric-cell blocking condition** (ion- vs electron-blocking) is not encoded in the
   files — it determines whether the arc is R_ion or R_e.  Confirm with the user before
   converting a sym-cell arc to a σ.
4. **Run reproducibility**: most measurements have 2 runs that agree; **`No2_only_full` run02
   (arc 89 Ω) diverges from run01 (arc 43 Ω)** — flagged, treat as re-measure/cell issue.

## Parser (external, not vendored)
`.mpr` is decoded with **[galvani](https://github.com/echemdata/galvani)** (GPL-3.0).  We
deliberately do **not** copy galvani into this repo (license hygiene); `scripts/eis_archive.py`
imports it lazily:
1. `from galvani import BioLogic`  (`pip install galvani`)
2. env `GALVANI_SRC=/path/to/galvani`  (dir with `BioLogic.py`)
3. else: catalog from existing `extracted/*.csv` (no re-extract).

## Provenance
User lab (Hanyang, 이종원 group) — BioLogic VSP-300, EC-Lab v11.63, 7 MHz→10 mHz, 10 pts/dec,
5 mV a.c., 2026-07-15 & -19.  Full-cell = NCM‖Li-In.  Areal capacity ~3 mAh cm⁻², ~70 µm electrode.
