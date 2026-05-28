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

### Stage-E σ_ionic form: SAT-blend ADOPTED; 62:38 ruled out (2026-05-28)
Production fixed Stage-E/physics form is now **SAT-blend** (in
`generate_comparison_plots._sat_baselog`, used by `ionic_fit_stage_e`,
`ionic_perconfig_physics`, the outlier diag, and the global fit corpus):
`σ = C_blend(τ)·σ_grain·(φ_eff)^0.5·CN²·cov^0.5·f_p³`, with composition-
dependent threshold `φc_eff=(1−g010)·0.200 + g010·0.195` and near-0:10
saturation `φ_eff=√((φ−φc_eff)²+(0.040·g010)²)`, `g010=σ(−10·(p−0.5))`,
p=AM_P fraction. C_blend(τ) still refits live; φc_P/φc_S/δ are FROZEN.
- **Validated by nested CV** (`scripts/nested_cv_sat.py`): unbiased LOOCV
  0.9488→0.9532 (+0.0045 ≈ 2.8× noise SE) — real, not selection bias
  (naive full-data LOOCV 0.958 had +0.0046 bias). Replaces bare √(φ−0.19).
- **62:38 / 0:10 outliers are INTRINSIC — do NOT re-try size/GB terms.**
  Nested CV rejected both candidates OVER SAT-blend: log r_SE size Δ=−0.0010,
  sub-µm GB penalty (Cronau-mirror, sigmoid r_SE<0.5µm) Δ=−0.0008 (β=−0.106,
  right sign but sub-noise). Synthetic proves the GB arm WOULD catch a clean
  sub-µm drop (Δ=+0.074), so the real 62:38 3× spread at fixed (62:38, r_SE)
  is NOT a clean deterministic sub-µm effect — packing/stochastic. Only levers
  left: MORE 62:38×packing data, or probabilistic (±band) prediction.
- **Cronau σ_grain factor ADOPTED (2026-05-28).** Per Stage-E itself
  (`run_network_full_corrections.py:88`), σ_grain depends on r_SE: 1.0 ≥0.5µm,
  0.90 at 0.3–0.5, 0.65 at 0.1–0.3, smooth to 0.33 ≤30nm. This is an SE
  MATERIAL property (amorphization at sub-µm), NOT a GB/geometric correction.
  Applied as a FIXED literature factor (no fit, no DoF) to the production
  σ_grain: `σ_grain_eff = 3.0 × Cronau(r_SE)` in `_sat_baselog`. LOOCV (frozen
  φc/δ) 0.9579 → 0.9622 (Δ=+0.0043, even with only 1/91 sub-0.5µm in the
  current corpus). This is why every geometric/coverage/size correction TERM
  failed — wrong location: the missing physics was in the σ_grain prefactor,
  not a multiplicative correction term. exp_S scan: 91/91 folds pick 0.5
  (mean-field) — percolation exponent is fine as-is.
- **CONTACT-QUALITY hypothesis ALSO rejected (2026-05-28).** The resid diagnostic
  (`scripts/resid_diag_62_38.py`) showed am_se_cn (AM-SE contact COUNT) corr
  **−0.81** and coverage_AM_S **+0.79** in the 62:38 subset (n=15) — looked like
  the missing physics (contact quality vs quantity). But nested CV rejected ALL
  of: am_se_cn surf-wt ungated (Δ=−0.0015) AND g_010-gated (Δ=−0.0023, WORSE),
  coverage_AM Hertz/physics/Δ% (Δ=−0.0008/−0.0036/−0.0015), r_SE/r_AM size ratio
  (Δ=−0.0008). The −0.81 was small-sample (n=15) overfitting — does NOT
  generalize; gating to 0:10 makes it worse. DO NOT re-try am_se_cn / coverage /
  size-ratio / GB / size terms for 62:38 — the whole contact-quality+size
  hypothesis space is rigorously exhausted. 62:38 is intrinsic; SAT-blend
  (0.9488→0.9532) is the ceiling. Levers: data, or probabilistic ±band.

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
