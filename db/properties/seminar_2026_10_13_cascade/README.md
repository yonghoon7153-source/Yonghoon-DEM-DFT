# Origin CSVs — Research Seminar 2026-10-13 (cascade progress briefing)

Deck: `kb/seminars/Research_Seminar_2026_10_13_cascade_progress.pptx` (18 slides).
Made by `kb/seminars/export_cascade_briefing_csvs_2026_10.py` — rerun it after the source files change.
Every CSV starts with `#` comment lines (source, units, cautions); Origin: Import → skip comment lines.

| page | slide | CSV | what to plot |
|---|---|---|---|
| 6 | Candidate set | `p06_candidate_set_by_anion_family.csv` | bars: n_planned vs n_computed per anion family |
| 8 | Configuration sampling | `p08_configurations_per_site_pair_long.csv` · `_matrix.csv` | heat map: cation site × anion site → configurations |
| 9 | DFT EOS | `p09_eos_bm3_fit_curves.csv` | lines: E − E0 vs V per f.u. (fit curves; raw points not in repo) |
| 10 | Stability window | `p10_stability_window_host.csv` · `p10_stability_window_host_segments.csv` | bar segments on a voltage axis (host Li6PS5Cl) |
| 12 | MD status | `p12_md_campaign_progress.csv` · `p12_md_campaign_runs.csv` | progress bars; run roster (status, wall-clock GPU-h) |
| 17 | Backup: site preference | `p17_site_preference_vs_ionic_radius.csv` | ΔE vs Shannon radius, three loadings per element |

Pages without a CSV:
- 2 (previous DFT work): figure boxes left empty on purpose — fill per tile on request.
- 3, 7, 11, 13, 14 (cards and tables), 5–6 tables (text in the slide).
- 4 (Kang 2026), 10 right (Sundar 2025 Fig. 2), 12 right (Jung 2026 Fig. 5b): literature figures — not digitized; literature values never go on the same plot as ours.
- 18 (bond-valence landscape): volumetric data (.cube) — not converted.

Value discipline: no transport value (D, ratio, Ea) is in any file here; the stability window is the corrected definition only;
B0 values are canonical DFT (compare per f.u. only).
