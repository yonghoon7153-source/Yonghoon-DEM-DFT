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

## ⚠ Units / caveats (read before anchoring)
1. **Raw impedances are in Ω, NOT Ω·cm².**  The `.mps` `Electrode surface area` is a
   placeholder (`0.001 cm2`), so no area normalization was applied.  To compare with
   manuscript R_int (Ω·cm²) multiply by the **true electrode area** (⌀ / cm²) — *pending
   from the user.*  (A ⌀10 mm ≈ 0.785 cm² would map No.1 full 78 Ω → ~61 Ω·cm², matching
   Fig S20 pristine ~60–90 Ω·cm² — plausible but unconfirmed.)
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
