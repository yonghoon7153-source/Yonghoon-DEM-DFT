# Project conventions for Claude Code sessions

## Viewing figures / PDFs on this WSL machine

WSL paths (`/home/yonghoon/...`) cannot be opened directly with
`explorer.exe`.  Always **copy the file to the Windows Downloads
folder first**, then launch explorer from there.

**Path:** `/mnt/c/Users/안용훈/Downloads/`
(Windows: `C:\Users\안용훈\Downloads\`)

### Single file

```bash
DL="/mnt/c/Users/안용훈/Downloads"
cp <path/to/file.png> "$DL/" && explorer.exe "$(wslpath -w "$DL/<file.png>")"
```

### Multiple files (open Downloads folder once)

```bash
DL="/mnt/c/Users/안용훈/Downloads"
cp docs/figures/<glob>.png "$DL/" && explorer.exe "$(wslpath -w "$DL")"
```

### Concrete example (the brittle z-distribution plots)

```bash
DL="/mnt/c/Users/안용훈/Downloads"
cp docs/figures/brittle_z_*.png "$DL/" && explorer.exe "$(wslpath -w "$DL")"
```

This convention applies to PNGs, PDFs, STL files, and any other output
the user wants to view through Windows.  When suggesting view commands,
always use this `cp … "$DL/"` pattern — never call `explorer.exe` on a
raw `/home/...` WSL path because Windows can't resolve it.

---

## Current roadmap & open tasks (updated 2026-05-27)

Working branch: `claude/debug-fracture-solver-DQE6G`. Commit footer:
`https://claude.ai/code/session_01AE6H8brQNyGYQLfq4X8Yq7`. Never put the
model identifier in commits/PRs. sklearn is NOT installed in the cloud
container → predictor (GPR/RF) training can only be statically checked
here; real training verified on the user's WSL machine.

### Big goal (user's vision)
Given input design numbers → ML predicts the full metric set → draw a 2D
microstructure matching those numbers → eventually stack different
configs as natural LAYERS inside one composite cathode.

### 5-phase plan (agreed order: sequential 1→5)
- **Phase 1 — DONE** (commit 9785bbf): expose grade_engine's ~30 derived
  metrics (Q_gravimetric, ASR_*, τ_Laplace, cycle-stable, 분극 η …) as
  `grade:<label>` params in the group-compare tool. Helpers:
  `grade_engine.axis_values()` + `map_input_params()`.
- **Phase 2 — single data layer**: per-case unified vector =
  full_metrics ∪ grade-axis ∪ fracture ∪ viewer_aux; make it the single
  source for ML training matrix + plot pool + predict targets. Extend
  `webapp/predictor_engine.py` `load_training_data` to include the
  grade/aux derived targets.
- **Phase 3 — ML predictor learns the full metric set** (design knobs →
  all metrics), per-target CV R².
- **Phase 4 — predicted numbers → 2D image**: add a "targets-only" entry
  point to `scripts/extract_2d_microstructure.py synthesize_microstructure`
  (no atoms.csv needed) so predictor output drives the 2D synth.
- **Phase 5 — layered composite cathode**: per-layer config synth +
  z-stacking with smooth interfaces (synth already does z-bands).

### Ionic-conductivity scaling-law reconciliation — RESOLVED (2026-05-27)
**There is effectively ONE current-best model under three names.**
- `v12-clean v3` **≡** `v29_FINAL` — IDENTICAL math, verified at
  `scripts/fit_v29_physics.py:102-103` and `generate_comparison_plots.py:1144-1162`:
  `σ_ionic = C_blend(τ) · σ_grain · √(φ−0.2) · CN^(3/2) · cov^(2/5) · f_p³`
  (σ_grain=3.0, φc=0.20). `v32` = v29 + 4 extra correction terms (LIGG_LB,
  w_thin·GEOM, p50δR, r_SE/r_AM) that all refit to ≈0 ⇒ v32 ≡ v29.
- **FORM X (v4++)** `C·σ_grain·(φ−0.185)^¾·CN·√cov/√τ` (R²≈0.96) is the
  OLDER, inferior model — kept only as a legacy toggle / predictor fallback.
- Performance: R²≈0.975, LOOCV≈0.968 on **n=92** (was 0.9813 / 0.9791 on
  n=57 — the small drop is just more diverse cases, normal).
- Consumers ALREADY consistent + auto-refit live on the current corpus:
  predictor_engine (`fit_ionic_v12`, primary) and the group plots both
  fit C_blend(τ) live on whatever cases exist → no stale n=57 coefficients.
- **Cannot meaningfully fit better**: at the noise-floor ceiling (LOOCV SE
  ≈0.0045). v32 extra terms → 0; v59/v60 real-resistance τ (τ_Dijkstra_R)
  gave NO improvement (inconclusive). The only real lever is MORE DATA in
  structural gaps (CN≥7, intermediate thickness) — already growing 57→92.
- Ground-truth network solver `scripts/network_conductivity.py` (Kirchhoff,
  Holm 1967) is current/unchanged — it was never the thing in question.
- REMAINING (cosmetic, optional): plot titles still say "FORM X v32 /
  v29_FINAL" while docs/predictor say "v12-clean v3" — same model, 3 names.
  Unify the label to stop confusion. Docs: `docs/ionic_scaling_law_experiments.md`
  (line 122 declares v12-clean v3 FINAL), `docs/Scaling_Law_Report_Full.md`.

### Recently completed (this session)
- Group-compare "save selected cases to archive"; full MD/PDF report
  mirroring the dashboard; honest "—" for uncomputed base σ_e/κ; v12-clean
  v3 wired into predictor + phi_ex clamp fix (0.001→1e-4); per-case grade
  rubric guide PDF (`/results/<id>/grade-guide`) with plain-language
  "쉽게 말하면" for all 54 axes; dynamic grade corpus (static 82 ∪ live
  viewer-loaded cases); generic parameter comparison (scatter/bar/corr) +
  fracture comparison charts in the group view; grade:<label> params.
