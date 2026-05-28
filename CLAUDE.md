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

### σ_ionic form FINALIZED — logpoly2 C_blend + smooth label-free f_small (2026-05-28)
**The production σ_ionic form has a complete physics derivation and is the
minimal-parameter form that the data supports.**  See
`docs/sigma_ionic_physics_derivation.md` for term-by-term derivation;
`scripts/final_form_status.py` for the equation + error landscape;
`scripts/test_threshold_form.py` for form-A-vs-alternatives comparison;
`scripts/audit_ps_label_convention.py` for the AM_P/AM_S size-convention
audit (n=183, 0 violations); `scripts/screen_form_simplifications.py` for
the term-by-term simplification screen.

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

### σ_ionic outlier landscape (after logpoly2 + 1mAh_9 exclusion, 2026-05-28)
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
