#!/usr/bin/env python3
"""σ_thermal — push to 0.9+ LOOCV (final attempt).

After V0-V24 screen capped at LOOCV 0.11, user requires 0.9+ to adopt.
This script tries 3 aggressive new approaches:

  Approach A: σ_ionic + σ_e as PRIMARY features (not supplements).
              Minimal form, no structural redundancy.
  Approach B: Aggressive sanity filter (require valid σ_ionic AND σ_e
              AND κ in narrow plausible range).  Remove anything that
              could be solver noise.
  Approach C: Bruggeman EMT baseline + form fits log(κ_actual / κ_baseline).
              Baseline absorbs main variance; form fits correction.

If best LOOCV < 0.9 → conclude: thermal form fundamentally cannot reach
the σ_ionic / σ_e rigor with current corpus.  Production = solver direct.

Run:  python3 scripts/thermal_form_push_09.py
"""
from __future__ import annotations
import sys, json, glob
from pathlib import Path
import numpy as np
from numpy.linalg import lstsq

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
import generate_comparison_plots as gcp

KAPPA_MAX = 50.0; KAPPA_MIN = 0.05
ION_MIN = 0.01; ION_MAX = 5.0
E_MIN = 0.1; E_MAX = 30.0


def _ps_fraction(d):
    fn = getattr(gcp, '_ps_fraction', None)
    if fn:
        v = fn(d)
        if v is not None: return v
    am_p = d.get('AM_P_mass_pct') or 0
    am_s = d.get('AM_S_mass_pct') or 0
    if am_p + am_s <= 0: return 0
    return am_p / (am_p + am_s)


def load_corpus(aggressive=False):
    rows = []
    skipped = {'no_kappa': 0, 'kappa_out': 0, 'no_phi': 0, 'no_tau': 0,
               'no_area': 0, 'sigma_ion_out': 0, 'sigma_e_out': 0}
    for f in sorted(glob.glob('webapp/archive/**/full_metrics.json', recursive=True)):
        nm = Path(f).parent.name
        if not nm.startswith('input_'): continue
        try: d = json.load(open(f))
        except: continue
        kappa = (d.get('thermal_sigma_full_mScm_stage_e') or
                 d.get('thermal_sigma_full_mScm') or 0)
        if not (kappa and kappa > 0): skipped['no_kappa'] += 1; continue
        if kappa > KAPPA_MAX or kappa < KAPPA_MIN: skipped['kappa_out'] += 1; continue
        sigma_ion = (d.get('sigma_full_mScm_stage_e') or
                     d.get('sigma_full_mScm') or 0)
        sigma_e = (d.get('electronic_sigma_full_mScm_stage_e') or
                   d.get('electronic_sigma_full_mScm') or 0)
        if aggressive:
            if not (ION_MIN <= sigma_ion <= ION_MAX): skipped['sigma_ion_out'] += 1; continue
            if not (E_MIN <= sigma_e <= E_MAX): skipped['sigma_e_out'] += 1; continue
        else:
            if sigma_ion <= 0: sigma_ion = 0.1
            if sigma_e <= 0: sigma_e = 0.1
        phi_am = d.get('phi_am', 0) or 0
        phi_se = d.get('phi_se', 0) or 0
        if phi_am <= 0 or phi_se <= 0: skipped['no_phi'] += 1; continue
        tau = (d.get('tortuosity_recommended') or d.get('tortuosity_mean') or 0)
        if tau <= 0: skipped['no_tau'] += 1; continue
        A_total = (d.get('am_am_mean_area', 0) or 0) + \
                  (d.get('area_AM전체_SE_total', 0) or 0) + \
                  (d.get('area_SE_SE_total', 0) or 0)
        if A_total <= 0: skipped['no_area'] += 1; continue
        p = _ps_fraction(d) or 0
        am_se_cn = d.get('am_se_cn_mean', 0) or 0
        cov_am = max(d.get('coverage_AM_P_mean', 0) or 0,
                     d.get('coverage_AM_S_mean', 0) or 0)
        perc = d.get('percolation_pct', 0) or 0
        rows.append({
            'name': nm, 'kappa': float(kappa),
            'sigma_ion': float(sigma_ion), 'sigma_e': float(sigma_e),
            'p': float(p), 'phi_am': float(phi_am), 'phi_se': float(phi_se),
            'A_total': float(A_total), 'tau': float(tau),
            'am_se_cn': float(am_se_cn) if am_se_cn > 0 else 1.0,
            'cov_am': float(cov_am) if cov_am > 0 else 1.0,
            'perc': float(perc)/100 if perc > 0 else 0.5,
        })
    return rows, skipped


def fit_loocv(rows, feature_cols, target_fn=None):
    n = len(rows)
    if target_fn is None:
        y = np.array([np.log(r['kappa']) for r in rows])
    else:
        y = np.array([target_fn(r) for r in rows])
    cols = [np.ones(n)]; labels = ['intercept']
    for lbl, fn in feature_cols:
        cols.append(np.array([fn(r) for r in rows]))
        labels.append(lbl)
    X = np.column_stack(cols); k = X.shape[1]
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
    return {'k': k, 'r2': r2, 'loocv': loocv, 'coef': coef, 'labels': labels}


def main():
    print("\n  ─── Approach A: σ_ionic + σ_e as PRIMARY (minimal form) ───")
    rows, sk = load_corpus(aggressive=False)
    print(f"  Loaded {len(rows)} cases (lenient filter). Skipped: {sk}\n")

    f_ion = ('log(σ_ionic)',  lambda r: np.log(max(r['sigma_ion'], 0.01)))
    f_e   = ('log(σ_e)',      lambda r: np.log(max(r['sigma_e'], 0.01)))
    f_phi_am = ('log(φ_AM)',  lambda r: np.log(r['phi_am']))
    f_phi_se = ('log(φ_SE)',  lambda r: np.log(r['phi_se']))
    f_A   = ('log(A_total)',  lambda r: np.log(max(r['A_total'], 1e-12)))
    f_amse = ('log(am_se_cn)', lambda r: np.log(max(r['am_se_cn'], 0.1)))
    f_cov = ('log(cov_AM)',   lambda r: np.log(max(r['cov_am'], 0.01)))
    f_perc = ('log(perc)',    lambda r: np.log(max(r['perc'], 0.05)))
    f_tau = ('q_τ·lnτ',       lambda r: np.log(max(r['tau'], 0.1)))
    f_tau2 = ('r_τ·ln²τ',     lambda r: np.log(max(r['tau'], 0.1))**2)

    minimal_variants = [
        ("A1: σ_ionic only",                    [f_ion]),
        ("A2: σ_e only",                        [f_e]),
        ("A3: σ_ionic + σ_e",                   [f_ion, f_e]),
        ("A4: σ_ionic + σ_e + φ_AM",            [f_ion, f_e, f_phi_am]),
        ("A5: A4 + am_se_cn",                   [f_ion, f_e, f_phi_am, f_amse]),
        ("A6: A5 + cov_AM",                     [f_ion, f_e, f_phi_am, f_amse, f_cov]),
        ("A7: A6 + perc",                       [f_ion, f_e, f_phi_am, f_amse, f_cov, f_perc]),
        ("A8: A7 + C(τ)",                       [f_ion, f_e, f_phi_am, f_amse, f_cov, f_perc, f_tau, f_tau2]),
    ]
    print(f"  {'Variant':40s} {'k':>3s}  {'R²':>7s} {'LOOCV':>7s}")
    for label, feats in minimal_variants:
        res = fit_loocv(rows, feats)
        flag = ' ⭐' if res['loocv'] >= 0.9 else (' ★' if res['loocv'] > 0.5 else '')
        print(f"  {label:40s} {res['k']:>3d}  {res['r2']:>6.3f} {res['loocv']:>6.3f}{flag}")
    print()

    print("  ─── Approach B: AGGRESSIVE sanity filter ───")
    rows_b, sk_b = load_corpus(aggressive=True)
    print(f"  Loaded {len(rows_b)} cases (aggressive filter). Skipped: {sk_b}\n")
    if len(rows_b) >= 20:
        print(f"  {'Variant':40s} {'k':>3s}  {'R²':>7s} {'LOOCV':>7s}")
        for label, feats in minimal_variants:
            res = fit_loocv(rows_b, feats)
            flag = ' ⭐' if res['loocv'] >= 0.9 else (' ★' if res['loocv'] > 0.5 else '')
            print(f"  {label:40s} {res['k']:>3d}  {res['r2']:>6.3f} {res['loocv']:>6.3f}{flag}")
    else:
        print(f"  [SKIP] aggressive filter too strict (n<20)")
    print()

    print("  ─── Approach C: Bruggeman EMT baseline + residual form ───")
    # Bruggeman 2-phase EMT (geometric mean): κ_baseline = κ_AM^φ_AM × κ_SE^φ_SE
    # Use LIVE-fit endpoints to discover κ_AM_eff, κ_SE_eff in mScm-equiv units
    # First: pure baseline (just κ_AM × κ_SE geometric mean with LIVE endpoints)
    f_endpt_AM = ('φ_AM·log κ_AM',  lambda r: r['phi_am'])
    f_endpt_SE = ('φ_SE·log κ_SE',  lambda r: r['phi_se'])
    baseline_feats = [f_endpt_AM, f_endpt_SE]
    res_base = fit_loocv(rows, baseline_feats)
    print(f"  Bruggeman baseline alone: k={res_base['k']}, R²={res_base['r2']:.3f}, "
          f"LOOCV={res_base['loocv']:.3f}")
    # κ_AM = exp(coef[1]), κ_SE = exp(coef[2])
    log_kAM, log_kSE = res_base['coef'][1], res_base['coef'][2]
    print(f"    discovered κ_AM = {np.exp(log_kAM):.3f}, κ_SE = {np.exp(log_kSE):.3f}")
    # Now form fits log(κ_actual / κ_baseline) = residual
    # Use coef from baseline as fixed offset
    def kappa_baseline(r):
        return np.exp(r['phi_am'] * log_kAM + r['phi_se'] * log_kSE)
    target_resid = lambda r: np.log(r['kappa'] / kappa_baseline(r))
    residual_variants = [
        ("C1: residual + σ_ionic",         [f_ion]),
        ("C2: residual + σ_ionic + σ_e",   [f_ion, f_e]),
        ("C3: residual + am_se_cn + cov",  [f_amse, f_cov]),
        ("C4: residual + all primary",     [f_ion, f_e, f_amse, f_cov, f_perc]),
        ("C5: residual + C(τ)",            [f_tau, f_tau2]),
        ("C6: residual + everything",      [f_ion, f_e, f_amse, f_cov, f_perc, f_tau, f_tau2]),
    ]
    print()
    print(f"  Residual form (target = log(κ_actual / κ_baseline)):")
    print(f"  {'Variant':40s} {'k':>3s}  {'R²_res':>7s} {'LOOCV_res':>9s}")
    for label, feats in residual_variants:
        res = fit_loocv(rows, feats, target_fn=target_resid)
        flag = ' ⭐' if res['loocv'] >= 0.9 else (' ★' if res['loocv'] > 0.5 else '')
        print(f"  {label:40s} {res['k']:>3d}  {res['r2']:>6.3f} {res['loocv']:>8.3f}{flag}")
    print()

    # ─── Verdict ───
    print("=" * 80)
    print("  VERDICT")
    print("=" * 80)
    print("  ⭐ = LOOCV ≥ 0.9 (user adoption threshold)")
    print("  ★  = LOOCV > 0.5 (interesting but below threshold)")
    print()
    print("  If NO ⭐ anywhere → σ_thermal form genuinely cannot reach 0.9 with")
    print("  current corpus + metrics.  Production = solver direct, document limit.")


if __name__ == '__main__':
    main()
