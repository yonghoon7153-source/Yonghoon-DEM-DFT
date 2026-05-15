# Yonghoon-DEM-DFT

DEM compaction + 8-stage post-processing pipeline for ASSB
(All-Solid-State Battery) sulfide-cathode design rules. Combines
LIGGGHTS quasi-static compaction at strain-faithful 1000× softened
moduli, an Auerbach + Lawn fracture classifier, a 7-layer Kirchhoff
solver with Bruggeman EMT fallback, and Stage-E literature-grounded
grain corrections (Cronau 2022, Trevisanello 2021, Wang 2022).

## Quick links

- **Paper draft** — `docs/paper/main.tex` (compiles to `main.pdf`)
- **ASR / Stage-E reader's guide** — `STAGE_E_ASR_GUIDE.md`
- **Reviewer-defence Q&A** — `docs/Reviewer_Defence_Notes.md`
- **Reproducibility checklist** — `docs/TODO_post_stage_e_rerun.md`
- **Webapp** — `webapp/app.py` (Flask; case browser + 3D viewer)

## Pipeline overview

```
LIGGGHTS DEM compaction (dem_scripts/*.liggghts)
        │  atoms.csv, contacts.csv (real-units force / overlap)
        ▼
network_conductivity.py   ── σ_ionic, σ_e, κ baselines (Kirchhoff)
        │
        ▼
run_network_full_corrections.py    ── Stage E (Lawn fracture × grain)
        │  fracture_classify_force_sim, Bruggeman fallback,
        │  validation_flags self-report card
        ▼
full_metrics.json  ←  the single source of truth per case
        │
        ▼
audit_validation_flags.py + pca_ensemble_variance.py
        │  trust audit (145/167), variance decomposition
        ▼
docs/paper/main.tex      Results §5 + Discussion §6 caveats
```

## Reproducing the 167-case analysis

Assumes archive cases already exist under `webapp/archive/<campaign>/`
with `atoms.csv` + `contacts.csv` per case.

```bash
# 1.  Stage E on every case that needs it (skip size-invariant cases)
python3 scripts/find_and_rerun_stage_e.py --all

# 2.  Stamp trust-flag self-report cards onto every full_metrics.json
python3 scripts/backfill_validation_flags.py

# 3.  Audit + LaTeX summary
python3 scripts/audit_validation_flags.py
# outputs:
#   docs/db/case_audit.csv           — all cases, all gates
#   docs/db/case_audit_fails.csv     — fails only + failed_gates
#   docs/db/case_audit_summary.tex   — booktabs table for paper §5

# 4.  Variance decomposition + PCA biplot
python3 scripts/pca_ensemble_variance.py
# outputs:
#   docs/db/pca_variance_decomposition.csv
#   docs/db/pca_components.csv
#   docs/db/pca_multivariate_R2.csv
#   docs/figures/pca_biplot.png

# 5.  Porosity validation 4-panel (with outlier red-star markers)
python3 scripts/plot_porosity_4panel.py
# outputs:  porosity_4panel.png

# 6.  Build the paper PDF (re-includes case_audit_summary.tex + figures)
cd docs/paper && pdflatex main.tex && bibtex main \
                 && pdflatex main.tex && pdflatex main.tex
```

## Key scripts (post-processing)

| Script | Purpose |
|---|---|
| `scripts/run_network_full_corrections.py` | Stage E worker; writes σ_*_stage_e and `validation_flags` into `full_metrics.json` |
| `scripts/find_and_rerun_stage_e.py` | Driver that picks Stage-E-needing cases (Cronau factor < 1) and dispatches the worker |
| `scripts/backfill_validation_flags.py` | Stamps the self-report card onto pre-existing Stage-E outputs without re-running the solver |
| `scripts/audit_validation_flags.py` | Walks the corpus → `case_audit.csv` + `case_audit_fails.csv` + LaTeX summary table |
| `scripts/pca_ensemble_variance.py` | Pearson r + univariate R² + multivariate lstsq + PCA biplot on the ensemble |
| `scripts/plot_porosity_4panel.py` | 4-panel ε_pred vs ε_meas validation; red stars flag the §A-trust mechanistic outliers |
| `scripts/plot_brittle_z_distribution.py` | Per-case z-profile of Lawn fracture stages with AM-AM pair-type breakdown |
| `scripts/plot_stress_z_distribution.py` | Per-case z-profile of per-particle max contact pressure (MPa) |
| `scripts/plot_coverage_z_distribution.py` | Per-case z-profile of per-AM SE-coverage %, ColorBrewer RdYlGn bands |
| `scripts/plot_combined_z_distribution.py` | 4-panel brittle + stress overlay (Pearson r reported) |
| `scripts/diag_se_percolation_threshold.py` | Direct measurement of SE stress-bearing percolation threshold (validates f_perc = 0.65 vs Liu & Yin 2025) — Radjai strong-network filter with SE-SE-only / SE-SE+AM-SE bridge twin definitions |
| `scripts/fracture_model.py` | Auerbach P_c + Lawn force-ratio classifier (single source of truth) |

## Webapp

```bash
cd webapp && python3 app.py   # http://localhost:5000
```

Features:
- Case browser with the same Stage-E + ASR rendering as the paper
- 3D Three.js viewer (Brittle Hotspots view mode with surface-gradient
  cap patches per Lawn stage, ColorBrewer YlOrRd palette)
- Brittle z-profile modal — sortable table + PNG/CSV download with
  per-pair-type filter (AM_P–AM_P / AM_P–AM_S / AM_S–AM_S)

## Repository conventions

- All DEM forces / lengths are stored in *sim* units; helpers in
  `scripts/fracture_model.py::fracture_classify_force_sim` and
  `scripts/run_network_full_corrections.py` convert to real SI
  (real = sim / scale, scale = 1000) before applying Auerbach.
- `full_metrics.json` is the per-case single source of truth — the
  webapp, paper rebuild, and audit scripts all read from it and never
  re-derive from the raw `atoms.csv` / `contacts.csv` unless
  explicitly invoked.
- File-viewing on WSL goes through `/mnt/c/Users/안용훈/Downloads/`;
  see `CLAUDE.md` for the `cp … "$DL/"` convention before
  `explorer.exe`.
