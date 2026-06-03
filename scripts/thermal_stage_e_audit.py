#!/usr/bin/env python3
"""σ_thermal — audit Stage E and try multiple targets.

Hypothesis: thermal_sigma_full_mScm_stage_e may be noisy/wrong due to
kappa_grain_factor_AM step function (0.65/0.50/0.40/0.30 by r_AM_P) or
Bruggeman-weighting in Stage E thermal channel.  If Stage E adds noise,
no form will fit it well — fitting RAW solver output might work better.

Tests:
  1. Audit Stage E factor distribution (per-case κ_stage_e / κ_raw)
  2. Identify extreme corrections (potential bug indicators)
  3. Fit form against RAW thermal (thermal_sigma_full_mScm)
  4. Fit form against PHYSICS thermal (thermal_sigma_full_mScm_physics)
  5. Fit form against κ_raw × manual Wang correction (bypass Stage E)
  6. Compare LOOCV across all 4 targets

If RAW fits well but Stage E doesn't → Stage E formula bug.
If neither fits well → genuine multi-pathway noise.
"""
from __future__ import annotations
import sys, json, glob
from pathlib import Path
import numpy as np
from numpy.linalg import lstsq

sys.path.insert(0, str(Path(__file__).parent))


def load_full():
    cases = []
    for f in sorted(glob.glob('webapp/archive/**/full_metrics.json', recursive=True)):
        nm = Path(f).parent.name
        if not nm.startswith('input_'): continue
        try: d = json.load(open(f))
        except: continue
        rows = {'_name': nm}
        # Targets
        rows['k_raw_H']    = d.get('thermal_sigma_full_mScm') or 0
        rows['k_stage_H']  = d.get('thermal_sigma_full_mScm_stage_e') or 0
        rows['k_raw_P']    = d.get('thermal_sigma_full_mScm_physics') or 0
        rows['k_stage_P']  = d.get('thermal_sigma_full_mScm_stage_e_physics') or 0
        # Structural features
        rows['phi_am']     = d.get('phi_am') or 0
        rows['phi_se']     = d.get('phi_se') or 0
        rows['r_AM_P']     = d.get('r_AM_P') or 5.5
        rows['r_AM_S']     = d.get('r_AM_S') or 2.5
        rows['r_SE']       = d.get('r_SE') or 0.5
        rows['tau']        = (d.get('tortuosity_recommended') or
                              d.get('tortuosity_mean') or 0)
        rows['am_se_cn']   = d.get('am_se_cn_mean') or 0
        rows['cov_am']     = max(d.get('coverage_AM_P_mean') or 0,
                                  d.get('coverage_AM_S_mean') or 0)
        rows['A_total']    = ((d.get('am_am_mean_area') or 0) +
                              (d.get('area_AM전체_SE_total') or 0) +
                              (d.get('area_SE_SE_total') or 0))
        # AM_P ratio for p
        am_p_pct = d.get('AM_P_mass_pct') or 0
        am_s_pct = d.get('AM_S_mass_pct') or 0
        rows['p'] = am_p_pct / (am_p_pct + am_s_pct) if (am_p_pct + am_s_pct) > 0 else 0.5
        cases.append(rows)
    return cases


def kappa_grain_factor_AM(r_AM_P_um):
    """Replicate run_network_full_corrections step function."""
    if r_AM_P_um <= 3.0: return 0.65
    if r_AM_P_um <= 7.0: return 0.50
    if r_AM_P_um <= 12.0: return 0.40
    return 0.30


def fit_simple(cases, target_key, valid_mask):
    """Fit log(κ) = intercept + α·log(φ_AM) + β·log(am_se_cn) + γ·log(cov_AM)
    + δ·log(τ) + ε·log²(τ).  Same minimal feature set across all targets."""
    rows = [c for i, c in enumerate(cases) if valid_mask[i]]
    n = len(rows)
    if n < 20: return None
    y = np.array([np.log(max(r[target_key], 1e-6)) for r in rows])
    X = np.column_stack([
        np.ones(n),
        np.array([np.log(max(r['phi_am'], 1e-3)) for r in rows]),
        np.array([np.log(max(r['phi_se'], 1e-3)) for r in rows]),
        np.array([np.log(max(r['am_se_cn'], 0.1)) for r in rows]),
        np.array([np.log(max(r['cov_am'], 0.01)) for r in rows]),
        np.array([np.log(max(r['tau'], 0.1)) for r in rows]),
        np.array([np.log(max(r['tau'], 0.1))**2 for r in rows]),
        np.array([np.log(max(r['A_total'], 1e-12)) for r in rows]),
    ])
    k = X.shape[1]
    coef, *_ = lstsq(X, y, rcond=None)
    pred = X @ coef
    sse_fit = float(np.sum((y - pred)**2))
    ss_tot = float(np.sum((y - y.mean())**2))
    r2 = 1 - sse_fit/ss_tot if ss_tot > 0 else 0
    sse_loo = 0.0
    for j in range(n):
        m = np.ones(n, bool); m[j] = False
        try:
            c, *_ = lstsq(X[m], y[m], rcond=None)
            sse_loo += (y[j] - X[j] @ c)**2
        except: pass
    loocv = 1 - sse_loo/ss_tot if ss_tot > 0 else 0
    return {'n': n, 'k': k, 'r2': r2, 'loocv': loocv, 'y_log': y, 'pred': pred}


def main():
    cases = load_full()
    print(f"\n  Loaded {len(cases)} cases\n")

    # ─── Audit: Stage E factor distribution per case ───
    print("=" * 95)
    print("  AUDIT 1: Stage E correction factor κ_stage_e / κ_raw (Hertz mode)")
    print("=" * 95)
    factors = []
    extreme_cases = []
    for c in cases:
        raw, stage = c['k_raw_H'], c['k_stage_H']
        if raw > 0 and stage > 0:
            f = stage / raw
            factors.append(f)
            if f < 0.10 or f > 1.5:
                extreme_cases.append((c['_name'], raw, stage, f, c['r_AM_P']))
    if factors:
        factors = np.array(factors)
        print(f"  Stage E factors (n={len(factors)}):")
        print(f"    range = [{factors.min():.3f}, {factors.max():.3f}]")
        print(f"    mean  = {factors.mean():.3f}")
        print(f"    median = {np.median(factors):.3f}")
        print(f"    std   = {factors.std():.3f}")
        print(f"  Expected: 0.30 ~ 1.00 (Wang step function 0.30/0.40/0.50/0.65 + Bruggeman + fracture)")
    print()

    if extreme_cases:
        print(f"  ⚠ {len(extreme_cases)} cases with EXTREME Stage E factor (< 0.10 or > 1.5):")
        for nm, raw, stage, f, r_AM_P in sorted(extreme_cases, key=lambda t: t[3])[:15]:
            wang_expected = kappa_grain_factor_AM(r_AM_P)
            tag = '⚠' if abs(f - wang_expected) > 0.3 else ''
            print(f"    {nm:30s}  raw={raw:>8.2f}  stage={stage:>8.2f}  f={f:>6.3f}  "
                  f"Wang_expected(r_AM_P={r_AM_P:.1f})={wang_expected:.2f} {tag}")
    print()

    # ─── Audit: kappa value distribution per target ───
    print("=" * 95)
    print("  AUDIT 2: κ value distribution per target")
    print("=" * 95)
    print(f"  {'Target':40s} {'n>0':>6s} {'min':>10s} {'median':>10s} {'max':>12s}")
    for key, label in [('k_raw_H',   'Hertz raw'),
                       ('k_stage_H', 'Hertz Stage E'),
                       ('k_raw_P',   'Physics raw'),
                       ('k_stage_P', 'Physics Stage E')]:
        vals = np.array([c[key] for c in cases if c[key] > 0])
        if len(vals) > 0:
            print(f"  {label:40s} {len(vals):>6d} {vals.min():>10.3f} "
                  f"{np.median(vals):>10.3f} {vals.max():>12.2f}")
    print()

    # ─── Fit on 4 different targets ───
    print("=" * 95)
    print("  Fit minimal form on 4 target choices (n_features=8 each)")
    print("=" * 95)
    print(f"  {'Target':40s} {'n':>5s} {'R²':>7s} {'LOOCV':>7s}")
    for key, label, max_sane in [
        ('k_raw_H',   'Hertz raw (no Stage E)',     50.0),
        ('k_stage_H', 'Hertz Stage E (current target)', 50.0),
        ('k_raw_P',   'Physics raw (no Stage E)',   50.0),
        ('k_stage_P', 'Physics Stage E',            50.0),
    ]:
        mask = np.array([0.01 < c[key] < max_sane for c in cases])
        if mask.sum() < 20: continue
        res = fit_simple(cases, key, mask)
        if res is None: continue
        flag = ' ⭐' if res['loocv'] >= 0.9 else (' ★' if res['loocv'] > 0.5 else '')
        print(f"  {label:40s} {res['n']:>5d} {res['r2']:>6.3f} {res['loocv']:>6.3f}{flag}")
    print()

    # ─── Try: raw × manual Wang correction (bypass Stage E completely) ───
    print("=" * 95)
    print("  Manual Wang correction (bypass Stage E entirely)")
    print("=" * 95)
    print(f"  κ_target = κ_raw_Hertz × Wang(r_AM_P)  (composition-weighted)")
    # Set κ_manual = κ_raw_H × kappa_grain_factor (composition-weighted average)
    for c in cases:
        if c['k_raw_H'] <= 0:
            c['k_manual'] = 0; continue
        # Bruggeman-weighted: f_AM = (1-p)·1.0 + p·Wang(r_AM_P)
        f_AM = (1 - c['p']) * 1.0 + c['p'] * kappa_grain_factor_AM(c['r_AM_P'])
        c['k_manual'] = c['k_raw_H'] * f_AM
    mask = np.array([0.01 < c.get('k_manual', 0) < 50 for c in cases])
    if mask.sum() >= 20:
        res = fit_simple(cases, 'k_manual', mask)
        if res:
            flag = ' ⭐' if res['loocv'] >= 0.9 else (' ★' if res['loocv'] > 0.5 else '')
            print(f"  {'manual Wang':40s} {res['n']:>5d} {res['r2']:>6.3f} "
                  f"{res['loocv']:>6.3f}{flag}")
    print()

    print("=" * 95)
    print("  INTERPRETATION")
    print("=" * 95)
    print("  - If RAW target LOOCV > Stage E LOOCV → Stage E adds noise/bug")
    print("  - If Physics > Hertz on RAW → solver Hertz mode has noise (use Physics)")
    print("  - If MANUAL Wang > Stage E → Stage E formula has bug")
    print("  - If all targets ~same low LOOCV → genuine multi-pathway data noise")


if __name__ == '__main__':
    main()
