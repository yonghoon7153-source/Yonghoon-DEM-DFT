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
- **symmetric cell** (`sym`) = **SUS | cathode | SUS** = **ion-blocking** (SUS passes e⁻,
  blocks Li⁺) → the DC arc is the **ELECTRONIC** resistance → **σ_e** of the composite
  (Hebb-Wagner).  Compares **pure-small vs bimodal(5:5)** electronic transport → validates
  **STEP3 σ_e** network.  (NOT σ_ion — that needs electron-blocking Li/In contacts.)

## Cell fabrication (lab notes 2026-06-25 → 07-19)
- **Composition** AM:SE:VGCF:PTFE = **80:18:1:1**.  Recipe: vortex 10 min → add PTFE →
  ball-mill 1 h → Thinky 2000 rpm 5 min → hot-plate rolling → roll-press onto **primer-coated
  SUS** collector.  **Areal capacity target = 3 mAh cm⁻²**.
- **AM**: No.1 / No.2 = **소립 4 µm single-crystal**; **Poly** = large polycrystalline.
  **5:5** = poly:small = 5:5 wt%.  Specific capacity (5:5): No.1 = 202.95, No.2 = 206.5 mAh g⁻¹.
- **Cells**: Li-In anode, 60 °C, 0.1C 2 cyc → 0.2C main.  **대칭셀(symmetric) = 10pi (⌀10 mm)**,
  **율특셀(rate)·수명셀(life, EIS source) = 13pi (⌀13 mm)**.
- **Thickness** — the filename "70 µm" is **cathode + SUS/c-SUS collector**; the
  **cathode-electrolyte composite (transport path) = 40–50 µm** at areal-cap 3 (user 2026-07,
  both sym & full).  σ_e uses the composite L (collector excluded) → σ_e carries a ±~11 % band
  from the 40–50 µm range.

## ⚠ Units / caveats (read before anchoring)
1. **Area normalization — RESOLVED (Ω·cm² now in catalog).**  Areas inferred from disk
   geometry (lab notes): **symmetric 10pi → 0.7854 cm²**, **full 13pi → 1.3273 cm²**;
   `*_ohmcm2 = *_ohm × area`.  (The `.mps` `Electrode surface area` 0.001 cm² is a placeholder
   and was ignored.)  Areas are inferred from cell type, not measured per file.
2. **`R_s / Re_LF / arc` in the catalog are quick descriptors, not a circuit fit.**
   `R_s` = high-freq real-axis intercept (bulk+series); `arc` = `Re_LF − R_s`
   (interfacial **+** diffusion, not yet separated).  Proper **R_ion/R_int/R_w** needs a
   CNLS equivalent-circuit fit (manuscript Fig S19: r_i + r_e + r_int‖cpe + Z_w).
3. **Symmetric-cell blocking — RESOLVED: SUS | cathode | SUS = ion-blocking → σ_e** (electronic).
   The DC arc is the electronic resistance R_e; **NOT** σ_ion (that needs electron-blocking Li/In).
4. **Run reproducibility**: 2 runs agree except **`No2_only_full` run02 (R_int 66) vs run01 (24
   Ω·cm²)** — this is the **same cell scanned twice at SOC100**; the divergence is real interfacial
   **degradation between scans** at the fully-charged (reactive) state, not a measurement error.

## CNLS equivalent-circuit fits  (`fits/`, `scripts/eis_fit.py`)
First-pass fits (impedance.py), **R0 fixed to the measured HF intercept**, arc free:
- **symmetric** (SUS ion-blocking) `R0-p(R1,CPE1)` → R_s + **R1 = R_e** → **σ_e = L_composite / R1**
- **full** `R0-p(R1,CPE1)-Wo1` → R_s + **R1 = R_int** + **Wo = R_w (diffusion)**

Results (`fits/eis_fit_results.csv`, Ω·cm², 2 runs each; **σ_e at L = 45 µm composite**):

| symmetric → σ_e | R_s | R_e | **σ_e (mS/cm)** |  | full → R_int | R_s | R_int | R_w |
|---|---|---|---|---|---|---|---|---|
| No1 pure | 10.1 | 32 | **0.14** | | No1 OCV | 9.8 | 79 | 51 |
| No1 5:5 | 6.9 | 48 | **0.093 ↓** | | No1 @1.3V | 6.8 | 30 | 0 |
| No2 pure | 8.2 | 39 | **0.115** | | No2 OCV run1 | 8.4 | 24 | 73 |
| No2 5:5 | 5.6 | 30 | **0.152 ↑** | | No2 OCV run2 (SOC100 aged) | 13.8 | 66 | 136 |

**σ_e electronic (composite, 1 % VGCF, single-crystal):** poly effect is **opposite** —
No1 ↓ (0.14→0.093), No2 ↑ (0.115→0.152); each ±~11 % from L = 40–50 µm.  These are a **STEP3
σ_e validation target** (low-carbon SC composite).  ⚠ CPE_a ≈ 0.30–0.34 (transport dispersion)
→ single R-CPE is first-pass; a TLM refit would refine.  rmse 5–6 % (sym) / 2.6–13 % (full).
Figure: `fits/eis_fits.png`.

**★ Representative full-cell R_int (`fits/summary_means.csv`, auto-recomputed each run):**
all 4 full cells are **SOC100 (charged, Ewe 3.61–3.67 V)** — the filename `1.3V` is that cell's
*initial OCV* (a cell-quality flag: 1.3 V = abnormally low OCV / worse cell; normal ≈ 2.0–2.2 V),
**not** the EIS voltage.  **Mean R_int = 49.8 Ω·cm²** (range 24–79, n=4; R_s 9.7, R_w 65).  Wide
spread → representative, not final (see re-experiment note).  Adding cells + re-running
`eis_archive.py` → `eis_fit.py` updates the mean automatically ("유동적으로 열어둔" 대표값).

### ⚠ n=4 → n=6 (2026-08-07): the auto-mean now spans TWO CELL BUILDS — do not anchor it
Re-running the fits after the `260728` cells landed moved the mean **49.8 → 100.46 Ω·cm²**.
That doubling is **not scatter**; the arithmetic separates cleanly:

| group | cells | R_s (Ω·cm²) | R1 = R_int | R_w | rmse % |
|---|---|---|---|---|---|
| **A** `260719_*_only_full` | 4 | 6.8–13.8 (mean 9.7) | 24.2 / 30.4 / 65.9 / 78.7 → **49.8** | 0.0–135.8 | 2.6–**13.0** |
| **B** `260728_No2_55_70` | 2 | 96.8–147.3 (mean 122) | 200.6 / 203.0 → **201.8** | 81.0 / 90.3 | **1.4–3.3** |

`(4×49.8 + 2×201.8)/6 = 100.46` — the new mean is just B entering the average.
- **R_s differs 12.6×** between the groups ⇒ different cell builds, not repeat scatter.
- **Fit quality splits the same way**: B reproduces R1 to **1.2 %** (200.6 vs 203.0) at rmse
  1.4–3.3 %; A reaches rmse 13 % and leaves **R_w unidentified (0.0 ↔ 135.8)**, i.e. the
  arc/tail split is at a local minimum, so A's R1 spread is partly a fit artifact.
- ⇒ report **two anchors** (A ≈ 50 n=4 ⚠fit-limited, B ≈ 202 n=2 best-fit), never the pooled
  mean.  `docs/data/rint_eis_anchors.csv:lab_sus_pristine` still carries the A-only value 50
  while `summary_means.csv` now says 100.46 — the "auto-updating" note makes that silent.

### ⚠ C_dl from Brug is OUT OF DOMAIN at these CPE exponents — withdraw the anchor
`C_dl` over the 6 full cells spans **2.7 → 1460 µF/cm² (541×)** in three per-cell clusters.
This is arithmetic, not physics: Brug `C = Q^(1/α)·R^((1−α)/α)` has exponents **3.33 and 2.33**
at the measured `CPE_a ≈ 0.30–0.34`.  Back-solving two endpoint cells at α = 0.30:

```
A#01  Q≈1.70e-2  R≈22.9 Ω   → C 1422 µF/cm²
B#02  Q≈7.9e-4   R≈152.9 Ω  → C    4.3 µF/cm²
      Q  21.5× ↓ → ^3.33 = 2.7e4× ↓ ;  R 6.7× ↑ → ^2.33 = 84× ↑ ;  net 321× ↓  (obs. 331×)
```

So the spread is **how each fit split the arc between Q and R**, amplified by two large opposing
powers — not a double-layer difference.  Brug is derived for surface-distributed capacitance at
α ≳ 0.7; α ≈ 0.3 is below even Warburg (0.5) and signals **distributed transport**, so the single
R‖CPE is first-pass for **R1 itself** (hence for R_int *and* σ_e), exactly as the σ_e note above
flags.  **TLM refit is the fix.**  Until then: no C_dl number (§F1 — record the reason, not a mean).

### σ_e: the STEP3 comparison set was mismatched (carbon), not a model gap
These cells are **AM:SE:VGCF:PTFE = 80:18:1:1**; the STEP3 numbers they were compared against
(SBE 1.979 / DBE 3.002 mS/cm) come from the SDCP campaign beds at **70:27:3:1** — **3× the VGCF**.
Carbon is a percolating additive, so 1 % vs 3 % can move σ_e by an order of magnitude on its own.
The measured 0.092–0.292 mS/cm (n=9, median 0.140) is therefore **not yet a discrepancy**.
→ Valid test = run STEP3 at **80:18:1:1 with SC AM** and check it lands in that band; that would
be the first ABSOLUTE experimental validation of the σ_e law (all prior σ_e checks were trends).
⚠ Also unresolved by the n=9 set: every σ_e uses the **L = 45 µm default** (no
`thickness_overrides.json` present) → ±11 % only, so L is not the explanation either.

### Poly vs single-crystal — one new cell points AGAINST our locked direction
The new pure-**Poly** symmetric cell gives **σ_e = 0.2924 mS/cm vs 0.1278 for the 8 SC cells (2.3×)**.
Our locked endpoints are σ_S(single) = 10 > σ_P(poly) = 5 mS/cm, i.e. the opposite ordering; this
agrees instead with `Oh #266 (poly > single)` already flagged in the A1 backlog.  **n = 1 and a
different build** → too weak to act on, and the 5:5 blend effect already fails to reproduce across
batches (No1 0.14→0.093 ↓ vs No2 0.115→0.152 ↑).  **One more Poly cell would decide it.**

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
