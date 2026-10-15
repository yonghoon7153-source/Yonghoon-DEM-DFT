# Origin CSVs — Research Seminar 2026-10-13 (cascade progress briefing)

Decks: `kb/seminars/Research_Seminar_2026_10_13_cascade_progress.pptx` (19 slides) and the lean variant
`…_progress_lean.pptx` (same 19 slides, same order, same page numbers — every CSV below fits both).
**Since 2026-10-14 the audit is slide 8** (right after the Stage-1 pipeline and its score) and the three slides that were
8–10 moved down one: `p08_*` = slide 9 · `p09_*` = slide 10 · `p10_*` = slide 11 (file names kept — they are paths).
Made by `kb/seminars/export_cascade_briefing_csvs_2026_10.py` — rerun it after the source files change.
Every CSV starts with `#` comment lines (source, units, cautions); Origin: Import → skip comment lines.
2026-10-12 update: the September-audit slide became page 11, so the MD-status CSV is now p13 and the
site-preference backup p18 (old p12 / p17 files are removed by the script). p06 and p07 count from the ledgers.

| page | slide | CSV | what to plot |
|---|---|---|---|
| 6 | Candidate set | `p06_candidate_set_by_anion_family.csv` | bars: n_planned vs n_relaxed vs n_gate_evaluation per anion family |
| 7 | Stage-1 coverage | `p07_stage1_coverage_by_ledger.csv` · `p07_structures_by_anion_family.csv` | not drawn on the slim deck since 2026-10-14 (the slide shows the five-step pipeline box; the full deck keeps the step table) — kept for questions and Origin (As2S3 / AlI3 flags) |
| 7 | Stage-1 composite score | `p07_stage1_composite_score_91.csv` | horizontal bars, top 10 of 91 (slim deck, beside the pipeline box) — the August method re-run on 10-14 with As2S3 and AlI3 added; exploratory and flawed (the audit, slide 8, says why); never cite a rank as a result |
| 7 | Stage-1 composite score, Origin copy (10-15) | `p07_stage1_composite_score_top10_origin.csv` | the slide's ten bars only, copied from the 91 file · rows in Origin plotting order (rank 10 → 1, so rank 1 is on top) · tick labels plain and Origin rich text (`\-(2)` subscripts) · value labels at 2 decimals as on the slide · same caution |
| 8 | Configuration sampling | `p08_configurations_per_site_pair_long.csv` · `_matrix.csv` | heat map: cation site × anion site → configurations (main batch 3,615) |
| 8 | Short anneal (slim slide 9, 10-15) | `p08_anneal_energy_change.csv` | histogram: ΔE per structure (meV per supercell · 693 · bin 50 · −1250 … 0) — replaces the August Step-5 histogram (681) |
| 8 | Site pairs over all 3,675 (user page 10, 10-15) | `p08_structures_per_site_pair_3675_long.csv` · `…_3675_matrix.csv` | structures per (cation site, anion site), main batch + August re-run · counts runs like slide 7 (15 AlI₃ re-runs share names; 3,660 distinct) |
| 8 | Short anneal, Origin layout (user page 10, 10-15) | `p08_anneal_energy_change_origin.csv` · `p08_anneal_energy_change_bins_origin.csv` | same 693 values in meV and eV per 52-atom cell, median in the header · 50 meV bins (sum = 693) for a column plot |
| 9 | DFT EOS | `p09_eos_bm3_fit_curves.csv` | lines: E − E0 vs V per f.u. (fit curves; raw points not in repo) |
| 10 | Stability window | `p10_stability_window_host.csv` · `p10_stability_window_host_segments.csv` · `p10_stability_window_host_legacy.csv` | bar segments on a voltage axis (host Li6PS5Cl); the legacy file is the earlier lower limit (a Li-uptake step, edge until 2026-09-22) for the user's page 12 — not a window edge |
| A (appendix) | Stage-1 volume filter vs two reference volumes | `pA_volume_filter_two_references.csv` · `pA_volume_filter_two_references_bins.csv` | per-structure dV against 27.478 (Stage 1) and 19.562 Å³/atom (DFT host, same MLIP) · 5 % bins coloured by the Stage-1 decision (100 removed; 1,284 beyond 25 % against the DFT host) |
| 13 | MD status | `p13_md_campaign_progress.csv` · `p13_md_campaign_runs.csv` | progress bars; run roster (status, wall-clock GPU-h) |
| 18 | Backup: site preference | `p18_site_preference_vs_ionic_radius.csv` | ΔE vs Shannon radius, three loadings per element (June batch, not Stage 1) |

Slim-deck figures (`--figures`) in `kb/seminars/assets_2026_10_13/`: plain previews drawn from the CSVs here (`fig_p07_stage1_score_top10.png` — on the slim deck since 10-14 · `fig_p07_stage1_coverage.png` · `fig_p10_host_window.png` · `fig_p13_run_roster.png`; p07 is drawn at the size it takes on the slide, so its font sizes are the slide's — since 10-13 p06 shows the 08-18 family table (four columns, the third now 'anion vs host') instead, and `fig_p06_candidates_by_family.png` stays only as an Origin option) — replace them with the Origin versions — and literature figures cropped from the litdb crops as the reason for a method choice (`lit_schwietert2021_fig1.png` p10 · `lit_he2018_fig3.png` p12 · `lit_phuthi2026_fig1a.png` p14; never redrawn, never on the same plot as our numbers; `lit_jung2026_sio2_fig3d.png` left p06 on 10-13 and stays only as a crop).

Pages without a CSV:
- 2 (previous DFT work): figure boxes left empty on purpose — fill per tile on request.
- 3, 11, 14, 15 (cards) · 5, 12 (tables, text in the slide) · 1, 16, 17 (title, thanks, references).
- 4 (Kang 2026), 10 right (Sundar 2025 Fig. 2), 13 right (Jung 2026 Fig. 5b): literature figures — not digitized; literature values never go on the same plot as ours.
- 19 (bond-valence landscape): volumetric data (.cube) — not converted.

Value discipline: no transport value (D, ratio, Ea) is in any file here; the stability window is the corrected definition only;
B0 values are canonical DFT (compare per f.u. only); Stage-1 counts are exploratory-data coverage, not a ranking.
