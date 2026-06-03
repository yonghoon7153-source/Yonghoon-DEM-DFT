#!/usr/bin/env python3
"""σ_thermal form screen — Stage T1 v2 (corrected after V1 fail).

V1 failure diagnosis: LOCKED literature endpoints (κ_S=4 W/m·K etc.) in
W/m·K scale conflict with thermal_sigma_full_mScm output (equivalent mScm,
Kirchhoff-normalized).  Bruggeman φ⁴ also too aggressive for two-phase
heat conduction (both AM and SE conduct).

V2 approach: ALL endpoints LIVE-fit (discover scale from data).  Locked
exponents only where strong literature anchor (Wang(r) ratio, Holm 0.5).
Build form bottom-up — add features one at a time, see what adds signal.

Variants:
  V0: intercept only
  V1: + log(φ_AM), log(φ_SE)             (2-phase volume fractions)
  V2: V1 + (1-p)·log_κ_S + p·log_κ_P     (AM endpoint mix, LIVE)
  V3: V2 + log(A_total) Holm-like        (contact area)
  V4: V3 + C(τ)                          (tortuosity logpoly2)
  V5: V4 + β_T·log(T/d)                  (thickness)
  V6: V5 + β_Fe·log(f_intact)            (fracture)
  V7: V6 + Wang(r_AM_P)                  (P-side size effect)
  V8: V7 + log(r_SE)                     (SE size)

Run:  python3 scripts/thermal_form_screen.py
"""
from __future__ import annotations
import sys, json, glob
from pathlib import Path
import numpy as np
from numpy.linalg import lstsq

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
import generate_comparison_plots as gcp


def _ps_fraction(d):
    fn = getattr(gcp, '_ps_fraction', None)
    if fn:
        v = fn(d)
        if v is not None: return v
    am_p = d.get('AM_P_mass_pct') or 0
    am_s = d.get('AM_S_mass_pct') or 0
    if am_p + am_s <= 0: return 0
    return am_p / (am_p + am_s)


def _r_am_sizes(d):
    fn = getattr(gcp, '_r_am_sizes', None)
    if fn:
        v = fn(d)
        if v: return v
    return d.get('r_AM_S', 2.5), d.get('r_AM_P', 5.5)


def load_corpus():
    rows = []
    for f in sorted(glob.glob('webapp/archive/**/full_metrics.json', recursive=True)):
        nm = Path(f).parent.name
        if not nm.startswith('input_'): continue
        try: d = json.load(open(f))
        except: continue
        kappa = (d.get('thermal_sigma_full_mScm_stage_e') or
                 d.get('thermal_sigma_full_mScm') or 0)
        if not (kappa and kappa > 0): continue
        phi_am = d.get('phi_am', 0) or 0
        phi_se = d.get('phi_se', 0) or 0
        if phi_am <= 0 or phi_se <= 0: continue
        tau = (d.get('tortuosity_recommended') or d.get('tortuosity_mean') or 0)
        if tau <= 0: continue
        A_am_am = d.get('am_am_mean_area', 0) or 0
        A_am_se_t = d.get('area_AM전체_SE_total', 0) or 0
        A_se_se_t = d.get('area_SE_SE_total', 0) or 0
        A_total = A_am_am + A_am_se_t + A_se_se_t
        if A_total <= 0: continue
        p = _ps_fraction(d) or 0
        ras, rap = _r_am_sizes(d)
        ras = float(ras) if (ras and np.isfinite(ras)) else 2.5
        rap = float(rap) if (rap and np.isfinite(rap)) else 5.5
        rse = d.get('r_SE', 0.5) or 0.5
        T = d.get('thickness_um', 100) or 100
        d_AM = 2.0 * ((1-p)*ras + p*rap)
        f_severe = (d.get('frac_severe_force_pct') or 0) / 100
        f_intact = max(1.0 - f_severe, 0.05)
        rows.append({
            'name': nm, 'kappa': float(kappa),
            'p': float(p), 'phi_am': float(phi_am), 'phi_se': float(phi_se),
            'ras': ras, 'rap': rap, 'rse': float(rse),
            'A_total': float(A_total), 'tau': float(tau),
            'T_d': float(T) / max(d_AM, 1.0),
            'f_intact': float(f_intact),
        })
    return rows


def fit_variant(rows, feature_cols):
    """Fit log κ = sum(coef · X_col) + intercept (always included).
    feature_cols = list of (label, fn(row)) tuples.  intercept added automatically.
    Returns (R², LOOCV, med_err%, coefs, labels)."""
    n = len(rows)
    y = np.array([np.log(r['kappa']) for r in rows])
    cols = [np.ones(n)]   # intercept
    labels = ['intercept']
    for lbl, fn in feature_cols:
        cols.append(np.array([fn(r) for r in rows]))
        labels.append(lbl)
    X = np.column_stack(cols)
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
    err_pct = (np.exp(pred) - np.array([r['kappa'] for r in rows])) / \
               np.array([r['kappa'] for r in rows]) * 100
    return {'k': k, 'r2': r2, 'loocv': loocv,
            'med_err': float(np.median(np.abs(err_pct))),
            'coef': coef, 'labels': labels}


def main():
    rows = load_corpus()
    n = len(rows)
    print(f"\n  Loaded {n} cases with valid thermal data.\n")
    if n < 20:
        print(f"[ABORT] too few cases (n={n}<20)"); return

    # κ statistics
    kappas = np.array([r['kappa'] for r in rows])
    print(f"  κ stats: min={kappas.min():.2f}, median={np.median(kappas):.2f}, "
          f"max={kappas.max():.2f} mScm-equiv")
    print(f"  log(κ) stats: min={np.log(kappas).min():.2f}, "
          f"median={np.log(np.median(kappas)):.2f}, max={np.log(kappas).max():.2f}")

    # ─── Variants — incremental feature addition ─────────────────────
    f_log_phi_am = ('log(φ_AM)',     lambda r: np.log(r['phi_am']))
    f_log_phi_se = ('log(φ_SE)',     lambda r: np.log(r['phi_se']))
    f_endpt_S    = ('(1-p)·log_κS',  lambda r: 1.0 - r['p'])
    f_endpt_P    = ('p·log_κP',      lambda r: r['p'])
    f_log_A      = ('log(A_total)',  lambda r: np.log(max(r['A_total'], 1e-12)))
    f_p_tau      = ('p_τ',           lambda r: 1.0)  # constant — combined with intercept; will be merged
    f_q_tau      = ('q_τ·lnτ',       lambda r: np.log(max(r['tau'], 0.1)))
    f_r_tau      = ('r_τ·ln²τ',      lambda r: np.log(max(r['tau'], 0.1))**2)
    f_log_Td     = ('β_T·log(T/d)',  lambda r: np.log(max(r['T_d'], 0.1)))
    f_log_fint   = ('β_Fe·log f_int', lambda r: np.log(max(r['f_intact'], 0.05)))
    # Wang-style AM_P size penalty
    f_wang_P     = ('log Wang_P',    lambda r: -np.log(1.0 + (r['rap']/2.0)**1.5))
    f_log_rse    = ('log r_SE',      lambda r: np.log(max(r['rse'], 0.05)))

    variants = [
        ("V0: intercept only",                            []),
        ("V1: + φ_AM, φ_SE",                              [f_log_phi_am, f_log_phi_se]),
        ("V2: V1 + AM endpoint mix (κ_S, κ_P live)",     [f_log_phi_am, f_log_phi_se, f_endpt_S, f_endpt_P]),
        ("V3: V2 + Holm log(A_total)",                    [f_log_phi_am, f_log_phi_se, f_endpt_S, f_endpt_P, f_log_A]),
        ("V4: V3 + C(τ) ln+ln²",                          [f_log_phi_am, f_log_phi_se, f_endpt_S, f_endpt_P, f_log_A, f_q_tau, f_r_tau]),
        ("V5: V4 + β_T·log(T/d)",                         [f_log_phi_am, f_log_phi_se, f_endpt_S, f_endpt_P, f_log_A, f_q_tau, f_r_tau, f_log_Td]),
        ("V6: V5 + β_Fe·log(f_intact)",                   [f_log_phi_am, f_log_phi_se, f_endpt_S, f_endpt_P, f_log_A, f_q_tau, f_r_tau, f_log_Td, f_log_fint]),
        ("V7: V6 + log Wang(r_AM_P)",                     [f_log_phi_am, f_log_phi_se, f_endpt_S, f_endpt_P, f_log_A, f_q_tau, f_r_tau, f_log_Td, f_log_fint, f_wang_P]),
        ("V8: V7 + log r_SE",                             [f_log_phi_am, f_log_phi_se, f_endpt_S, f_endpt_P, f_log_A, f_q_tau, f_r_tau, f_log_Td, f_log_fint, f_wang_P, f_log_rse]),
    ]

    print()
    print("=" * 100)
    print(f"  σ_thermal incremental screen (LIVE-fit endpoints)  n={n}")
    print("=" * 100)
    print(f"  {'Variant':50s} {'k':>3s} {'n/k':>6s} {'R²':>7s} {'LOOCV':>7s} {'med|err|':>9s} {'ΔLOOCV':>9s}")

    prev_loo = -np.inf
    best_loo = -np.inf
    best_res = None; best_label = None
    for label, feats in variants:
        res = fit_variant(rows, feats)
        dloo = res['loocv'] - prev_loo if prev_loo != -np.inf else float('nan')
        marker = ' ★' if res['loocv'] > best_loo else ''
        if res['loocv'] > best_loo:
            best_loo = res['loocv']; best_res = res; best_label = label
        n_over_k = n / res['k']
        print(f"  {label:50s} {res['k']:>3d} {n_over_k:>6.1f} "
              f"{res['r2']:>6.3f} {res['loocv']:>6.3f} {res['med_err']:>8.1f}% "
              f"{dloo:>+8.4f}{marker}")
        prev_loo = res['loocv']

    print()
    print("=" * 100)
    print(f"  BEST: {best_label}")
    print("=" * 100)
    for lbl, c in zip(best_res['labels'], best_res['coef']):
        print(f"    {lbl:25s}  {c:+.4f}")
    print(f"\n  LOOCV {best_res['loocv']:.4f}  R² {best_res['r2']:.4f}  "
          f"med|err| {best_res['med_err']:.1f}%  k={best_res['k']}  n/k={n/best_res['k']:.1f}")
    # Translate endpoint coefs to κ_S, κ_P scale
    labels = best_res['labels']
    if '(1-p)·log_κS' in labels:
        i_s = labels.index('(1-p)·log_κS')
        i_p = labels.index('p·log_κP')
        log_kS = best_res['coef'][i_s]
        log_kP = best_res['coef'][i_p]
        print(f"\n  Discovered endpoints (LIVE-fit, mScm-equiv units):")
        print(f"    κ_S = {np.exp(log_kS):.2f}   κ_P = {np.exp(log_kP):.2f}")
        print(f"    ratio κ_S/κ_P = {np.exp(log_kS - log_kP):.2f}× "
              f"(literature W/m·K ratio ≈ 4/3 = 1.33×)")


if __name__ == '__main__':
    main()
