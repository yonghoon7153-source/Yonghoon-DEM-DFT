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
- **Excluded case (per-seed sim anomaly, 2026-05-28).** `input_particulate_12_S3`
  filtered from the analysis corpus (`nested_cv_sat._EXCLUDED_NAMES`). At the
  same design point (φ=0.275, CN=3.3, r_SE=1.5µm) the 5 sibling seeds (base, S1,
  S2, S4, S5) cluster σ_act 0.030–0.045 (median 0.038); S3=0.020 is half the
  sibling median → isolated seed anomaly, not a form failure. The audit
  family-check (`scripts/audit_outliers_factors.py`) found it via meta.json
  sibling lookup.  Production form predicted ~0.034 (matching the sibling
  range), so the +74% "outlier" was the case, not the model.
- **POST-Cronau extras ALL rejected; ablation shows form is balanced (2026-05-28).**
  Re-running the residual diagnostic AFTER Cronau adoption surfaced new strong
  signals in the D1/D1.5 62:38 subset (path_hop_area +0.82, se_cn_eff_area +0.80,
  stress_cv −0.82) — but all three failed LOOCV-with-feat (Δ between −0.0015 and
  −0.0019, β≈0) because the strong signal is concentrated in ~4 cases (62:38
  large-SE) and dilutes globally. SAME pattern as the rejected contact-quality
  family. Term-by-term ablation (`section 8` of nested_cv_sat.py) on the full
  base (LOOCV 0.9622) shows: CN²=−0.307, (φ_eff)^0.5=−0.134, cov^0.5=−0.033,
  f_p³=−0.015, C_blend(τ)=−0.0057, Cronau=−0.0043. CN² and the percolation φ
  term carry ~90% of the fit; nothing redundant. ionic σ work is COMPLETE.
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

### σ_ionic form FINALIZED — T1 production (power gate + cov_Hertz + f_intact) (2026-05-28)
**The production σ_ionic form has 5 live OLS coefficients, all terms
have physical meaning (HIGH/MED-HIGH/MED, NO LOW), and is at the data
noise ceiling.**  Docs in `docs/sigma_ionic_physics_derivation.md`;
status in `scripts/final_form_status.py`; key supporting scripts:
`bidir_62_38_test.py` (C4 leave-corner-out), `test_threshold_form.py`,
`audit_ps_label_convention.py` (n=183, 0 violations), `screen_form_simplifications.py`,
`scan_smooth_f_small.py` (power gate ★ vs sigmoid), `integrate_betacov.py`
(T1 cov_Hertz ★ vs cov_physics+Δcov), `final_pushes.py` (Spearman narrative
verify + per-composition LOOCV + Huber robust).

⚠ T1 ADOPTION HAD A "FALSE-REVERT" MOMENT (2026-05-28).
First T1 commit (5c617a2) only switched the GLOBAL FIT base + extras to
cov_Hertz but missed FOUR plot callsites that compute their own per-case
base for prediction (`plot_ionic_perconfig_physics` line 4226,
`plot_ionic_outliers_stage_e` 4503/4533, `plot_ionic_decomp_physics`
line 2279).  Those plot sites kept calling `_cov_frac(d, physics=True)`,
so the dashboard's `_sat_baselog(..., cov=cov_physics)` was being added
to T1-Hertz-calibrated logpoly2 coefficients → systematic ~1.4×
over-prediction across ALL 91 cases (cov_phys ≈ 2× cov_Hertz, so the
0.5·log(2) ≈ +0.35 base shift was amplified by the Hertz-fit `a`).  This
LOOKED like "T1 intrinsic over-prediction" and triggered a temporary
revert (b97674c → DOC) before user-flagged "91 outliers" diagnosis
identified the missing patches.  Re-adoption commit re-applies T1 to
`_stage_e_base_arrays` + `production_extras` AND patches all 4 plot
callsites for full consistency.  Lesson: when changing a base-form
ingredient, GREP every `_cov_frac` / `_sat_baselog` callsite — the form
lives in ≥4 plot functions, not just `_stage_e_global_fit`.

THE FINAL EQUATION:
  σ = σ_grain · Cronau(r_SE) · (φ_eff)^½ · CN² · cov_Hertz^½ · f_p^3
      · exp[a + b·ln τ + c·(ln τ)² + β_P2·P2 + β_F·log f_intact]

Sub-definitions (all FROZEN):
  φ_eff      = √[(φ − φc_eff)² + (δ·g_phys)²]
  φc_eff     = (1 − g_phys)·φc_P + g_phys·φc_S
  g_phys     = (min(r_cut / r_AM_eff, 1))^α        [POWER GATE]
  r_AM_eff   = (1 − p)·r_AM_S + p·r_AM_P            (composition-weighted)
  P2         = g_phys · (φ − φc_S)² · (r_SE − 0.5)+ [P2 corner correction]
  f_intact   = 1 − fracture_aware_excluded_pct/100
  Cronau(r)  = 0.33 + 0.32·σ(50(r−0.10)) + 0.25·σ(50(r−0.30)) + 0.10·σ(50(r−0.50))
                                                    [smooth 3-sigmoid]
Constants:
  σ_grain = 3.0 mS/cm     (Cronau 2022 Li6PS5Cl single-crystal)
  φc_P = 0.200            (P-heavy threshold, FROZEN)
  φc_S = 0.195            (S-heavy threshold, FROZEN)
  δ = 0.040               (disorder rounding, FROZEN)
  r_cut = 3.5 µm          (power-gate cutoff = audit-derived AM_S/AM_P midpoint)
  α = 2                   (power-gate exponent = inverse-square scaling)

5 LIVE-fit params: (a, b, c, β_P2, β_F).  n=90/k=5 = 18:1 (safe).

Per-term meaning & confidence:
  σ_grain               HIGH      Cronau 2022 single-crystal literature
  Cronau(r_SE)          HIGH      Cronau 2022 piecewise smoothed (3-sigmoid)
  (φ_eff)^½             MED-HIGH  mean-field 3D percolation; data-locked 91/91
  CN²                   MED-HIGH  Kirchhoff #paths × bond-strength; locked 91/91
  cov_Hertz^½           HIGH      Holm 1967 + effective Li⁺ conduction area
                                  (Spearman: cov_H vs σ 0.697 > cov_P 0.476;
                                   Tabor adhesion creates mechanical contact area
                                   but vdW gap interferes with ionic transport)
  f_p^3                 MED       3D isotropy P(percolate-x ∧ -y ∧ -z) = f_p³
  C(τ) = a+b·lnτ+c·(lnτ)² MED    logpoly2, beats dual-branch by ΔAIC=-10.6
  β_P2·P2               MED       Cronau super-µm arm: bulk-grain regime at
                                  62:38 D1+ corner; PASSED leave-corner-out
  β_F·log f_intact      MED       fracture-aware Holm; β=+0.19 partial-conduction
                                  (broken contacts retain ~60% via micro-asperity)
  g_phys (power gate)   MED-HIGH  inverse-square small-AM dominance, label-free

Adoption history (full chain, each step separately validated):
  • Baseline (bare √φ−0.19)                          LOOCV 0.9499
  • + SAT-blend (φc_eff, δ disorder rounding)        LOOCV 0.9578  Δ+0.0049
  • × Cronau(r_SE) σ_grain factor (literature)       LOOCV 0.9640  Δ+0.0062
  • C_blend → logpoly2 (3 params, dual-branch 6)     LOOCV 0.9660  Δ+0.0020 (+ΔAIC -10.6)
  • smooth Cronau (3-sigmoid, fully differentiable)  no LOOCV change
  • smooth f_small → power gate (Alt-C, α=2)         LOOCV 0.9670  Δ+0.0010
  • + β_P2·P2 (g_phys-gated, 62:38 corner)           LOOCV 0.9687  Δ+0.0017
  • + β_F·log f_intact (fracture-aware Holm)         LOOCV 0.9710  Δ+0.0023
  • T1: cov_physics → cov_Hertz (drop Δcov term)     LOOCV 0.9712  Δ+0.0002 (k 6→5)
        [+ 4 plot callsite patches for consistency]

FINAL production: LOOCV ≈ 0.971, 5 fit params.

CLOSE-OUT (2026-05-28) — Bayesian Laplace + form-vs-solver decomposition:
  • Form-vs-solver: Stage E σ ≈ network solver output (Cronau-multiplied).
    Decomposition shows solver↔DEM gap is ~0% for all cases except
    sub-µm Cronau-region (D0.25 only).  All other gap is form↔solver.
    → form is the bottleneck, and it's a 5-param OLS compression of the
    solver's output.  At info-theoretic ceiling for this representation.
  • Bayesian Laplace (physics priors: β_F~N(0.19, 0.05) literature,
    β_P2~N(3.5, 1.5)): empirical 90% PI coverage = 94.4% (well-calibrated).
    Of 17 cases with |err|>15%:
      − 12 INSIDE 90% PI → form correctly states uncertainty; NOT real outliers
      − 5 OUTSIDE PI    → genuine model failures, ALL data-resolution issues

THE 5 GENUINE σ_ionic OUTLIERS (post-Bayesian classification):
  | # | Case                       | err%   | P:S  | Resolution path                         |
  |---|----------------------------|--------|------|-----------------------------------------|
  | 1 | input_1mAh_9_S5            | +46.5  | 7:3  | sibling tail; family median≈0.033, S5  |
  |   |                            |        |      | the outlying seed → use sibling median  |
  |   |                            |        |      | in dashboard (no new sim needed)        |
  | 2 | input_1mAh_8               | +40.3  | 5:5  | isolated single; user running           |
  |   |                            |        |      | input_72_seed1..5 multi-seed sim        |
  | 3 | input_8mAh_real_10         | -30.0  | 10:0 | isolated; near-φc + τ_Laplace ratio     |
  |   |                            |        |      | 2.73×; 8mAh sim slow, separate review   |
  | 4 | input_8mAh_8_AMP           | -26.7  | 10:0 | isolated thick 10:0 (D_P/T=0.07,        |
  |   |                            |        |      | NOT single-layer); needs 8mAh multi-seed|
  | 5 | input_particulate_12_S2    | -25.0  | 0:10 | sibling tail; particulate_12_S1..S5    |
  |   |                            |        |      | family exists → use sibling median      |

  All 5 are PER-SEED OR ISOLATED — NONE are systematic regime failures.
  Form has zero residual systematic bias.

Dashboard / production code updates (2026-05-28):
  • plot_ionic_perconfig_physics: bootstrap-derived per-case 68% PI band
    replaces hard-coded ±22% band.  Wide where form is uncertain
    (extrapolation), tight where well-fit.
  • Cache: _BOOTSTRAP_CACHE (B=500 resampling, MAP residual SE for
    aleatoric noise).  Computed once per session.

Methodology scripts added:
  • scripts/form_vs_solver_decomp.py — verdicts each outlier as FORM- or
    SOLVER-limited.  15/16 outliers classified FORM-limited.
  • scripts/bayesian_laplace.py — closed-form Laplace posterior (no PyMC);
    physics priors; per-outlier PI inside/outside verdict.
  • scripts/active_learning_suggest.py — Laplace-based next-sim recommender.
    Top suggestions converge to degenerate (r_AM_S=r_AM_P=4µm, r_SE=1.5µm)
    corner — realistic-region corpus is well covered.

Performance summary (n=90):
  median |err| ≈ 7%, mean ≈ 10%, 90th pctile ≈ 20%
  |err|>30%: 2 (1mAh_8, 1mAh_9_S5)   |err|>50%: 0
  After Bayesian PI: only 5 cases classified as GENUINE failures
  (all addressable by sibling-median display or pending multi-seed sim).

⚠ DO NOT add more form terms.  The form is at the joint info-theoretic
ceiling of:
  (a) what 5 OLS coefficients can compress from the solver's output, AND
  (b) what per-seed/isolated stochasticity in DEM allows the data to anchor.
Any further term will overfit on the 5 genuine outliers, ALL of which
are data-resolution problems (not form representation problems).

Production performance (n=90):
  median |err| ≈ 7%, mean ≈ 10%, 90th pctile ≈ 20%
  |err|≤30%: 97%   |err|>30%: 2-3 cases   |err|>50%: 0

(Legacy outlier landscape from before Bayesian reclassification — see
the close-out section above for the current 5-genuine-outlier list.)

Multi-seed averaging would clean these up further (+0.0041 LOOCV) but
PRODUCTION USES RAW n=90 — averaging is data-side preprocessing, not
form change.  Documented in `scripts/final_pushes.py` for reference.

⚠ NEVER re-screen φc.  φc_P, φc_S, δ stay FROZEN at (0.200, 0.195, 0.040).
With logpoly2 the selection-bias from re-screening is larger (gap +0.0095
vs +0.0048 with dual-branch).  Production never re-selects → not a problem.

NARRATIVE NOTE on T1 adoption (2026-05-28): Spearman signal supports
cov_Hertz: ρ(σ, cov_Hertz)=+0.697 vs ρ(σ, cov_physics)=+0.476.
Interpretation: "Li⁺ effective conduction area" (Hertz native) not
"mechanical bottleneck" (cov_physics inflated by Tabor adhesion).  Tabor
adhesion creates physical contact area but the vdW gap layer interferes
with ionic transport → effective conduction area < mechanical area.
First T1 commit looked like it caused dashboard over-prediction; that was
NOT the form — it was 4 plot callsites still using cov_physics for
per-case base prediction while the global fit used cov_Hertz (see
warning box).  When ALL callsites use cov_Hertz consistently, the form
predicts σ_act well AND tracks the network solver line on the dashboard.
β_cov·Δcov was dropped — the empirical Tabor-correction is unnecessary
once the base operates at the elastic-Hertz area where Holm 1967 was
derived.
Lesson: when changing a base-form ingredient, grep EVERY callsite of the
shared compute helper (`_cov_frac`, `_sat_baselog`) before adopting —
mismatched plot paths look like form regressions and can trigger spurious
reverts.

  σ = σ_grain · Cronau(r_SE) · (φ_eff)^½ · CN² · cov^½ · f_p³ · C_blend(τ)

with smooth label-free g_phys replacing g₀₁₀ (canonical):
  g_phys   = σ(10·(f_small − 0.5))
  f_small  = (1−p)·σ(5·(3.5 − r_AM,S)) + p·σ(5·(3.5 − r_AM,P))
  φ_eff    = √[(φ−φc_eff)² + (δ·g_phys)²]
  φc_eff   = (1−g_phys)·0.200 + g_phys·0.195
  C_blend(τ) = a + b·ln τ + c·(ln τ)²   (logpoly2, 3 OLS params live-fit)
  δ=0.040; σ_grain=3.0 mS/cm; Cronau piecewise (literature)

Adoption rationale (each change separately validated):
  • Cronau(r_SE) σ_grain factor — Cronau 2022 literature, +0.0048 LOOCV
  • f_small (smooth two-sigmoid) — replaces g₀₁₀ with size-derived gate;
    LOOCV equivalent (+0.0001) but no label-convention dependency
  • C_blend → logpoly2 (3 params instead of dual-branch 6) — +0.0020 LOOCV,
    ΔAIC -10.6, ΔBIC -18.2.  n/k goes 15:1 → 30:1 (overfit margin doubles).

⚠ NEVER re-screen φc.  φc_P, φc_S, δ stay FROZEN at (0.200, 0.195, 0.040).
With logpoly2 the selection-bias from re-screening (φc_P, φc_S, δ) is
larger (gap +0.0095 in nested CV vs +0.0048 with dual-branch): logpoly2
has less "absorption" of φc choice than dual-branch, so re-selection over-
fits more.  Production never re-selects → not a problem.  But if the next
maintainer tries to re-screen φc after adding new data, expect inflated
LOOCV that doesn't generalize.  Always benchmark against the FROZEN-φc
LOOCV in `final_form_status.py`, not the nested-CV with re-selection.

Confidence:
  • σ_grain × Cronau(r_SE) — Cronau 2022 (HIGH literature)
  • cov^½ — Holm 1967 constriction (HIGH literature)
  • CN² and (φ_eff)^½ — data-locked 91/91, derivable physics
  • f_p³ — 3D isotropy + Stauffer-Bruggeman backbone scaling
  • C_blend(τ) logpoly2 — beats dual-branch on AIC/BIC by decisive margin
  • g_phys (smooth) — empirically validated vs 5 alternatives, all losing
    3.5–11.1× noise SE.  Audit (n=183) confirmed AM_S ≤ 4 µm AND
    AM_P ≥ 5 µm with no overlap → label and smooth form equivalent here.
  • exponents (½, 2, ½, 3) — joint screen confirms minimal; merge tests
    rejected (Q2 percolation merge fails by >0.13 LOOCV, Q3 network merge
    fails by >0.03).

### σ_ionic outlier landscape (DEPRECATED — see CLOSE-OUT 2026-05-28 for current 5-outlier list)
### (after C4 adoption, n=90, LOOCV 0.9687, 2026-05-28)
With the C4 augmented form, 3 cases remain >30% (down from 4) and 10 cases
remain >20% (down from 12).  4 particulate-corner cases (particulate_7,
_10, _5, _12_S2) which all previously sat 22-37% out are now ALL within
±20%.  The remaining 10 outliers split into three diagnostic classes:

  CLASS A — PER-SEED NOISE (6 cases, unfixable by any form term):
    input_8mAh_real_10 (-41%): isolated 10:0 r_SE=0.5, 4-edge sensitivity
    input_1mAh_9_S5    (+32%): sibling tail (within sibling spread)
    input_1mAh_9_S2    (-29%): sibling tail
    input_1mAh_8       (+22%): isolated 5:5
    input_1mAh_8_AMP   (+24%): isolated 10:0
    input_8mAh_8_AMP   (-20%): isolated 10:0
  CLASS B — r_SE = 0.5 OVER-PREDICTION (3 cases, P2=0 at r_SE=0.5):
    input_S_2          (+25%): 0:10 SE-rich
    input_1mAh_5_AMP   (+30%): 10:0 SE-rich
    input_6mAh_real_10 (+23%): 10:0 D1+
  CLASS C — MARGINAL-PERCOLATION EDGE (1 case):
    input_6mAh_real_6  (+32%): 0:10 r_SE=1.5 BUT CN=2.7 (below typical
       percolation threshold); form being asked to extrapolate near φc·CN
       boundary.

Bidirectional 0:10·SE-rich corner now PARTIALLY resolved:
  • r_SE ≥ 1µm UNDER-prediction side: FIXED (particulate_7 -24→±20%,
    particulate_10 -37→±20%) by gated P2 term
  • r_SE = 0.5  OVER-prediction side: PARTIALLY (particulate_5 +22→<20%
    via Δcov; input_S_2 stays +25% — Δcov insufficient)
  P2 is mathematically zero at r_SE=0.5 — cannot help the over-prediction
  side; would need a separate r_SE=0.5-active term but corpus has only
  3 such corner cases → cannot validate (leave-corner-out would FAIL).

⊗ DO NOT try to add more form terms.  The remaining outliers are data-
limited (per-seed simulation noise, isolated single cases, marginal-
percolation edges).  Path forward = MORE multi-seed DATA at:
  • particulate_5/S_2 design (r_SE=0.5 over-prediction) — to determine
    if the 25-30% miss is reproducible physics or per-seed noise
  • 8mAh_real_10 design (4-edge case) — to determine anomaly vs form-limit
  • 1mAh_9_Sn family — averaging clears the family from outlier list (med
    σ=0.033, form predicts 0.028 → -15% err < 20%)

### σ_ionic outlier landscape (DEPRECATED, kept for history)
Corpus n=90, LOOCV 0.9634, |err|>30% in 4 cases.  All 4 individually
analyzed; NONE are form-of-equation failures, all are data limitations:

  1. input_1mAh_9 (base, +45%) — REMOVED as per-seed anomaly (σ_act=0.020
     vs 5 _Sn siblings 0.029-0.035, sibling median 0.033, base = 61%).
     Same pattern as input_particulate_12_S3.  Now in _EXCLUDED_NAMES.

  REMAINING 4 (|err|>30%):

  2. input_8mAh_real_10 (-44%) — 4 form-sensitivity edges simultaneously:
       (i) φ−φc = 0.016 (near-threshold, amplified variance);
       (ii) τ_Laplace=3.53 vs τ_Dijkstra=1.29 (constriction overhead 2.73×,
            form uses Laplace which over-penalizes);
       (iii) Hertz→physics amplification +133% (unusual; form uses physics
             cov which inflates σ_base, then C_blend over-corrects);
       (iv) 10:0 → g_phys≈0 → no δ rounding to soften the threshold edge.
     Cumulative effect: form predicts ~half of σ_act.  Isolated case
     (no siblings) → cannot distinguish data anomaly from form-region
     limitation.  Keep as outlier; do NOT tune form to fit it.

  3. input_particulate_10 (-37%) — 62:38 D1.5 corner UNDER-prediction.
     Paired with #4 input_S_2 below (same regime, opposite r_SE end).

  4. input_S_2 (+32%) — 0:10 SE-rich r_SE=0.5µm OVER-prediction.  Same
     0:10·SE-rich regime as particulate_10, but at small r_SE.  These
     two reveal a BIDIRECTIONAL r_SE-dependent error in the 0:10·φ>0.30
     corner that the form cannot capture with a single multiplicative
     factor:
        r_SE = 0.5µm   form OVER-predicts:  input_S_2 +32%, particulate_5 +22%
        r_SE ≥ 1.0µm   form UNDER-predicts: particulate_7 -24%, particulate_10 -37%
     Actual σ varies 0.20 (r_SE=0.5) → 0.67 (r_SE=1.5) at the same
     composition (φ≈0.40, 0:10), a 3× span; form is approximately flat
     because Cronau(r_SE) saturates to 1.0 for all r_SE ≥ 0.5.
     P2 = (φ−φc)²·(r_SE−0.5)+ catches the under-prediction side (Δ
     LOOCV +0.0072) but is mathematically zero at r_SE=0.5 — so it
     CANNOT fix the over-prediction side.  This is why P2 failed the
     leave-corner-out test: bulk-only fit found β<0 to compensate the
     over-prediction at r_SE=0.5, but full-fit needs β>0 for the
     under-prediction at r_SE≥1.0.  Bidirectional bias = single
     multiplicative correction insufficient.  Must add MORE DATA on
     BOTH ends (multi-seed at particulate_5/S_2 AND particulate_7/_10).

  5. input_1mAh_9_S5 (+33%) — sibling spread tail (σ_act=0.029, 88% of
     family median 0.033).  Within sibling spread → NOT removed; logged
     as form-prediction outlier rather than data anomaly.

(Note: input_6mAh_real_6 (CN=2.7 marginal-percolation) is at +28%,
just under the 30% cutoff after the 1mAh_9 base exclusion shifted the
overall fit slightly.  Still a form-region edge case; included in the
"|err|>20%" outlier table.)

Path forward = data, not form:
  • multi-seed at 1mAh_9 design IS available (5 siblings) → if we average
    σ_act across siblings = 0.033 (med), form predicts 0.028 (-15% err)
    → averaging clears the family from the outlier list
  • multi-seed at BOTH ends of the 0:10·φ>0.30 r_SE-sweep (particulate_5
    + S_2 at r_SE=0.5, AND particulate_7/_10 at r_SE≥1.0) would tell us
    whether the 3× σ_act swing at fixed composition is a clean function
    of r_SE or per-seed noise.  ONLY then can we decide if a (φ−φc)·r_SE
    family of corrections is real physics or noise.
  • multi-seed at 8mAh_real_10 design would tell us if -44% is anomaly
    or genuine form limitation in the φ≈φc·10:0 regime

### Recently completed (this session)
- Group-compare "save selected cases to archive"; full MD/PDF report
  mirroring the dashboard; honest "—" for uncomputed base σ_e/κ; v12-clean
  v3 wired into predictor + phi_ex clamp fix (0.001→1e-4); per-case grade
  rubric guide PDF (`/results/<id>/grade-guide`) with plain-language
  "쉽게 말하면" for all 54 axes; dynamic grade corpus (static 82 ∪ live
  viewer-loaded cases); generic parameter comparison (scatter/bar/corr) +
  fracture comparison charts in the group view; grade:<label> params.
