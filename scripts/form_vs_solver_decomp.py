#!/usr/bin/env python3
"""Form-vs-Solver decomposition — separate σ_form vs σ_solver vs σ_DEM gaps.

QUESTION
--------
When σ_form (T1 production) misses σ_DEM by 30%, is it because:
  (A) form can't represent what the solver predicts  → form-limited
  (B) solver itself disagrees with σ_DEM            → solver-limited
  (C) both                                          → unsolvable without new physics

DECOMPOSITION
-------------
For each case:
  σ_DEM     = ground truth (from full DEM + Stage-E pipeline)
  σ_solver  = Kirchhoff network solver prediction
  σ_form    = T1 production form prediction

Gaps:
  GAP_form-solver  = log(σ_form) − log(σ_solver)     [form's ability to mimic solver]
  GAP_solver-DEM   = log(σ_solver) − log(σ_DEM)       [solver's accuracy on DEM]
  GAP_form-DEM     = log(σ_form) − log(σ_DEM)         [end-to-end form error]

  GAP_form-DEM = GAP_form-solver + GAP_solver-DEM

VERDICT PER CASE
----------------
  |GAP_form-solver| > |GAP_solver-DEM|  → FORM-limited (improve form)
  |GAP_solver-DEM| > |GAP_form-solver|  → SOLVER-limited (improve solver, or accept)
  both small (<10%)                     → noise ceiling, both fine

IMPLICATIONS FOR THE PROJECT
----------------------------
  • If most outliers are solver-limited → form is doing its job; further form
    tweaks are wasted.  Path forward = revisit Holm 1967 contact model OR
    accept the solver's limit.
  • If outliers are form-limited → form needs more terms (which we've largely
    exhausted) or restructure.
  • If mixed → outlier-by-outlier triage.

Run on WSL where corpus lives:
    python3 scripts/form_vs_solver_decomp.py
"""
from __future__ import annotations
import sys, json
from pathlib import Path
import numpy as np

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))

from nested_cv_sat import (load_corpus, base_log_sat, cronau_factor,
                           cblend_fit, cblend_pred, _g_phys_smooth,
                           _meta_name, _EXCLUDED_NAMES, PHIC_PROD,
                           PHICP_F, PHICS_F, DELTA_F, PHI_C0)
import generate_comparison_plots as gcp


def p2_feat(a, g):
    phi = a[:, 0]; r = a[:, 8]
    pex = np.maximum(phi - PHIC_PROD, 0.0)
    rs = np.where(np.isfinite(r) & (r > 0), r, 0.5)
    return g * pex**2 * np.maximum(rs - 0.5, 0.0)


def load_corpus_with_names_and_solver():
    """Walk corpus, return (a_array, names, sigma_solver_array).
    sigma_solver = raw Kirchhoff network solver σ (physics).
    sigma_DEM    = a[:,5] (already in load_corpus).
    """
    a = load_corpus()
    names, sigsol = [], []
    seen = set()
    for base in ('webapp/results', 'webapp/archive'):
        bp = Path(base)
        if not bp.is_dir():
            continue
        for mp in bp.rglob('full_metrics.json'):
            try:
                d = json.load(open(mp))
            except Exception:
                continue
            sig = gcp._stage_e_sigma(d)
            phi = gcp._get(d, 'phi_se'); cn = gcp._get(d, 'se_se_cn')
            cov = gcp._cov_frac(d, physics=False) or gcp._cov_frac(d, physics=True)
            fp = gcp._get(d, 'percolation_pct') / 100.0
            tau = gcp._get(d, 'tortuosity_recommended', gcp._get(d, 'tortuosity_mean', 0))
            if not (sig and sig > 0 and phi > PHI_C0 and cn > 0 and cov and cov > 0
                    and fp > 0 and tau > 0):
                continue
            nm = _meta_name(mp.parent.name, mp.parent)
            if nm in _EXCLUDED_NAMES:
                continue
            key = (round(phi, 4), round(cn, 3), round(float(sig), 5))
            if key in seen:
                continue
            seen.add(key); names.append(nm)
            # Solver σ: prefer sigma_full_mScm_physics, fall back to sigma_full_mScm
            sigsol.append(d.get('sigma_full_mScm_physics')
                          or d.get('sigma_full_mScm') or np.nan)
    return a, names, np.asarray(sigsol, float)


def main():
    print("=" * 78)
    print(" FORM-vs-SOLVER DECOMPOSITION — where do σ errors come from?")
    print("=" * 78)
    a, names, sig_solver = load_corpus_with_names_and_solver()
    n = len(a)
    if n < 8 or a.ndim < 2:
        print("[ABORT] corpus too small.")
        return
    logsf = np.log(a[:, 5]); taus = a[:, 4]   # σ_DEM
    log_solver = np.log(np.where(sig_solver > 0, sig_solver, 1e-9))
    valid_solver = np.isfinite(log_solver) & (sig_solver > 0)
    print(f"Corpus n = {n} (with σ_solver available: {valid_solver.sum()})\n")

    # Fit T1 production form on σ_DEM
    g = _g_phys_smooth(a); fi = a[:, 19] if a.shape[1] >= 20 else np.zeros(n)
    base = base_log_sat(a, PHICP_F, PHICS_F, DELTA_F) + np.log(cronau_factor(a[:, 8]))
    extras = [p2_feat(a, g), fi]
    b = cblend_fit(base, logsf, taus, extras=extras)
    pred_log = cblend_pred(base, taus, b, extras=extras)   # σ_form on σ_DEM target

    # ───── Gaps in log-space ─────
    gap_form_dem = pred_log - logsf                # form's overall error
    gap_form_solver = pred_log - log_solver        # form's ability to mimic solver
    gap_solver_dem = log_solver - logsf            # solver's accuracy on DEM

    def _pct_band(g):
        return float(np.mean(g)*100), float(np.std(g)*100), float(np.median(np.abs(g))*100)

    m, s, med_abs = _pct_band(gap_form_dem[valid_solver])
    print(f"  GAP form ↔ DEM     (form's total error):")
    print(f"     mean = {m:+6.2f}%   std = {s:5.2f}%   median |err| = {med_abs:5.2f}%")
    m, s, med_abs = _pct_band(gap_form_solver[valid_solver])
    print(f"  GAP form ↔ solver  (form's ability to mimic the solver):")
    print(f"     mean = {m:+6.2f}%   std = {s:5.2f}%   median |err| = {med_abs:5.2f}%")
    m, s, med_abs = _pct_band(gap_solver_dem[valid_solver])
    print(f"  GAP solver ↔ DEM   (solver's accuracy on DEM):")
    print(f"     mean = {m:+6.2f}%   std = {s:5.2f}%   median |err| = {med_abs:5.2f}%")
    print()

    # ───── Per-case classification ─────
    print("─" * 78)
    print(" Per-case classification (cases with |GAP form↔DEM| > 15%)")
    print("─" * 78)
    print(f"  {'case':32s}  {'σ_DEM':>7s}  {'σ_solver':>8s}  {'σ_form':>7s}  "
          f"{'GAP F-D':>7s}  {'GAP F-S':>7s}  {'GAP S-D':>7s}  {'verdict':s}")
    print("  " + "─" * 76)
    n_form, n_solver, n_both, n_noise = 0, 0, 0, 0
    for i in np.argsort(-np.abs(gap_form_dem)):
        if not valid_solver[i] or abs(gap_form_dem[i]) < 0.15:
            continue
        # log → %
        fd = (np.exp(gap_form_dem[i]) - 1) * 100
        fs = (np.exp(gap_form_solver[i]) - 1) * 100
        sd = (np.exp(gap_solver_dem[i]) - 1) * 100
        # Classify dominant gap
        afs = abs(fs); asd = abs(sd)
        if afs > 1.5 * asd and afs > 0.10:
            verdict = "FORM-limited"; n_form += 1
        elif asd > 1.5 * afs and asd > 0.10:
            verdict = "SOLVER-limited"; n_solver += 1
        elif afs > 0.10 and asd > 0.10:
            verdict = "BOTH (cumulative)"; n_both += 1
        else:
            verdict = "noise ceiling"; n_noise += 1
        nm = names[i] if i < len(names) else f"(idx{i})"
        print(f"  {nm[:32]:32s}  {a[i,5]:7.4f}  {sig_solver[i]:8.4f}  "
              f"{float(np.exp(pred_log[i])):7.4f}  "
              f"{fd:+7.1f}  {fs:+7.1f}  {sd:+7.1f}  {verdict}")
    print()

    # ───── Summary ─────
    print("=" * 78)
    print(" CLASSIFICATION SUMMARY (|form-DEM| > 15% outliers only)")
    print("=" * 78)
    total = n_form + n_solver + n_both + n_noise
    print(f"  FORM-limited       : {n_form:3d}   form can't mimic solver here → form fix lever")
    print(f"  SOLVER-limited     : {n_solver:3d}   solver disagrees with DEM → Holm/Cronau issue")
    print(f"  BOTH               : {n_both:3d}   compounding errors → hardest to fix")
    print(f"  noise ceiling      : {n_noise:3d}   small gaps, residual noise")
    print(f"  total outliers     : {total:3d}")
    print()

    if total > 0:
        print(f"  → ACTIONABLE INSIGHT:")
        if n_form > n_solver + n_both:
            print(f"     Form is the dominant constraint.  But our form is already at noise")
            print(f"     ceiling on LOOCV; any further form tweak overfits.  Bayesian/")
            print(f"     hierarchical (#2) is the only legitimate form-side lever.")
        elif n_solver > n_form + n_both:
            print(f"     SOLVER is the dominant constraint.  No amount of form tweaking will")
            print(f"     help — revisit Kirchhoff Holm 1967 assumption (cov_Hertz vs other")
            print(f"     contact area definitions) OR document & accept the ceiling.")
        else:
            print(f"     Mixed — form and solver each carry roughly equal residual.")
            print(f"     End-to-end gap is the sum; neither side dominates.")
        print()

    # ───── Bonus: correlation of GAP_form-solver with GAP_solver-DEM ─────
    if valid_solver.sum() > 10:
        corr = np.corrcoef(gap_form_solver[valid_solver],
                           gap_solver_dem[valid_solver])[0, 1]
        print(f"  cov(form-solver, solver-DEM) = ρ = {corr:+.3f}")
        if abs(corr) < 0.3:
            print(f"    → independent errors (form/solver weaknesses uncorrelated)")
        elif corr > 0.3:
            print(f"    → CORRELATED: form mimics solver AND inherits its bias")
        else:
            print(f"    → ANTI-correlated: form partially compensates for solver's bias")


if __name__ == '__main__':
    main()
