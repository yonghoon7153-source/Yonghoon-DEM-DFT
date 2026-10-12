# Origin CSVs — Research Seminar 2026-10-13 (cascade progress briefing)

Decks: `kb/seminars/Research_Seminar_2026_10_13_cascade_progress.pptx` (19 slides) and the lean variant
`…_progress_lean.pptx` (same 19 slides, same order, same page numbers — every CSV below fits both).
Made by `kb/seminars/export_cascade_briefing_csvs_2026_10.py` — rerun it after the source files change.
Every CSV starts with `#` comment lines (source, units, cautions); Origin: Import → skip comment lines.
2026-10-12 update: the September-audit slide became page 11, so the MD-status CSV is now p13 and the
site-preference backup p18 (old p12 / p17 files are removed by the script). p06 and p07 count from the ledgers.

| page | slide | CSV | what to plot |
|---|---|---|---|
| 6 | Candidate set | `p06_candidate_set_by_anion_family.csv` | bars: n_planned vs n_relaxed vs n_gate_evaluation per anion family |
| 7 | Stage-1 coverage | `p07_stage1_coverage_by_ledger.csv` · `p07_structures_by_anion_family.csv` | bars: precursors held by each Stage-1 table (As2S3 / AlI3 flags); the per-family structure counts (relaxed 3,675 vs annealed 693) are a text line on the slim deck since 10-13 |
| 8 | Configuration sampling | `p08_configurations_per_site_pair_long.csv` · `_matrix.csv` | heat map: cation site × anion site → configurations (main batch 3,615) |
| 9 | DFT EOS | `p09_eos_bm3_fit_curves.csv` | lines: E − E0 vs V per f.u. (fit curves; raw points not in repo) |
| 10 | Stability window | `p10_stability_window_host.csv` · `p10_stability_window_host_segments.csv` | bar segments on a voltage axis (host Li6PS5Cl) |
| 13 | MD status | `p13_md_campaign_progress.csv` · `p13_md_campaign_runs.csv` | progress bars; run roster (status, wall-clock GPU-h) |
| 18 | Backup: site preference | `p18_site_preference_vs_ionic_radius.csv` | ΔE vs Shannon radius, three loadings per element (June batch, not Stage 1) |

Slim-deck figures (`--figures`) in `kb/seminars/assets_2026_10_13/`: plain previews drawn from the CSVs here (`fig_p06_candidates_by_family.png` · `fig_p07_stage1_coverage.png` · `fig_p10_host_window.png` · `fig_p13_run_roster.png`; p06 and p07 are drawn at the size they take on the slide, so their font sizes are the slide's) — replace them with the Origin versions — and literature figures cropped from the litdb crops as the reason for a method choice (`lit_jung2026_sio2_fig3d.png` p06 · `lit_schwietert2021_fig1.png` p10 · `lit_he2018_fig3.png` p12 · `lit_phuthi2026_fig1a.png` p14; never redrawn, never on the same plot as our numbers).

Pages without a CSV:
- 2 (previous DFT work): figure boxes left empty on purpose — fill per tile on request.
- 3, 11, 14, 15 (cards) · 5, 12 (tables, text in the slide) · 1, 16, 17 (title, thanks, references).
- 4 (Kang 2026), 10 right (Sundar 2025 Fig. 2), 13 right (Jung 2026 Fig. 5b): literature figures — not digitized; literature values never go on the same plot as ours.
- 19 (bond-valence landscape): volumetric data (.cube) — not converted.

Value discipline: no transport value (D, ratio, Ea) is in any file here; the stability window is the corrected definition only;
B0 values are canonical DFT (compare per f.u. only); Stage-1 counts are exploratory-data coverage, not a ranking.
