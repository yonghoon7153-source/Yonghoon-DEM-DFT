#!/usr/bin/env python3
"""Physics-mode fit v55 — comprehensive deep-dive.

Four explorations after v54 revealed Lasso reaches 0.96 LOOCV with
structural-only features (vs v29's 0.90):

  Part A — Lasso form distillation
      Take v54 R3's 11 surviving features, fit them explicitly, write
      out the full equation with γ values + per-term interpretation.

  Part B — σ_P / σ_bulk_H ratio analysis (plastic-constriction penalty)
      Define penalty = σ_P / σ_bulk_H per case.
      What predicts the penalty? Lasso on (penalty target) using
      structural + binding features. Outliers in the ratio.

  Part C — Universality test (apply Lasso pipeline to Hertzian σ target)
      Predict σ_H from same 33 features via LassoCV. Do the same
      features survive? Same coefficients? Different mode, same form?

  Part D — Hertzian features individual predictive power
      Test each Hertzian-mode feature ALONE for predicting σ_P:
        log σ_H, log σ_bulk_H, log σ_constr_H, log τ_eff_H,
        log constr_share_H
      Quantifies which Hertzian-mode summary carries which signal.
"""
from __future__ import annotations
import sys, json, warnings
from pathlib import Path
import numpy as np
import pandas as pd

SCRIPTS = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS))
from physics_fit_v33_binding import load_phys_rows  # noqa: E402
from v32_exhaustive_refit import load_cases  # noqa: E402
from physics_fit_v53_lasso import enrich_full        # noqa: E402

WEBAPP = SCRIPTS.parent / 'webapp'
warnings.filterwarnings('ignore')


def loocv_lasso(Xs, y, alpha):
    from sklearn.linear_model import Lasso
    from sklearn.model_selection import LeaveOneOut
    n = len(y); pred = np.empty(n)
    for tr, te in LeaveOneOut().split(Xs):
        m = Lasso(alpha=alpha, max_iter=20000, fit_intercept=True)
        m.fit(Xs[tr], y[tr])
        pred[te] = m.predict(Xs[te])[0]
    ss_res = np.sum((y - pred) ** 2); ss_tot = np.sum((y - y.mean()) ** 2)
    return 1 - ss_res / ss_tot, pred


def run_single_lasso(X, names, y, label, do_loocv=True):
    from sklearn.linear_model import LassoCV
    Xs = (X - X.mean(0)) / (X.std(0) + 1e-9)
    if X.shape[1] >= 2:
        lcv = LassoCV(cv=10, max_iter=20000, n_alphas=120,
                      fit_intercept=True, random_state=42)
        lcv.fit(Xs, y)
        coef, alpha, intercept = lcv.coef_, lcv.alpha_, lcv.intercept_
    else:
        # 1-feature OLS
        x = Xs[:, 0]
        c = np.sum((x - x.mean()) * (y - y.mean())) / np.sum((x - x.mean()) ** 2)
        coef = np.array([c]); intercept = y.mean() - c * x.mean(); alpha = 0.0
    pred = Xs @ coef + intercept
    ss_res = np.sum((y - pred) ** 2); ss_tot = np.sum((y - y.mean()) ** 2)
    r2_in = 1 - ss_res / ss_tot
    if do_loocv:
        r2_loo, _ = loocv_lasso(Xs, y, alpha)
    else:
        r2_loo = None
    print(f'\n  {label}', flush=True)
    print(f'    R²(in)={r2_in:.4f}  '
          f'LOOCV={"%.4f" % r2_loo if r2_loo is not None else "—"}  '
          f'α={alpha:.5f}', flush=True)
    nz = [(names[i], float(coef[i])) for i in range(len(coef))
          if abs(coef[i]) > 1e-9]
    nz.sort(key=lambda t: -abs(t[1]))
    print(f'    survivors ({len(nz)}/{len(names)}):', flush=True)
    for n_, g_ in nz[:8]:
        print(f'      {n_:30s}  γ = {g_:+.4f}', flush=True)
    return {'r2_in': float(r2_in), 'r2_loo': float(r2_loo) if r2_loo else None,
            'alpha': float(alpha), 'survivors': nz, 'k_active': len(nz),
            'k_total': len(names)}


def main():
    cases = load_cases()
    rows = enrich_full(load_phys_rows(cases))
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} cases.', flush=True)
    n = len(df)

    # ── Build features once (shared across parts) ────────────
    excess = np.maximum(df['phi'].values - 0.20, 1e-6)
    log_excess = np.log(excess)
    log_CN     = np.log(np.maximum(df['cn'].values, 1e-3))
    log_cov    = np.log(np.maximum(df['cov_phys'].values, 1e-3))
    log_f_p    = np.log(np.maximum(df['f_perc'].values, 1e-3))
    log_tau    = np.log(np.maximum(df['tau'].values, 1e-3))
    log_thick  = np.log(np.maximum(df['thickness'].values, 1.0))
    log_gb     = np.log(np.maximum(df['gb_dens'].values, 1e-6))
    porosity   = df['porosity'].values / 100.0
    p_frac     = df['p_frac'].values
    is_thin    = (df['thickness'].values < 50).astype(float)
    b_T = df['b_tabor'].values / 100.0
    b_G = df['b_geom'].values / 100.0
    b_H = df['b_hertzian'].values / 100.0
    b_L = df['b_liggghts'].values / 100.0

    sig_H      = np.maximum(df['sigma_H'].values, 1e-6)
    sig_bulk_H = np.maximum(df['sigma_bulk_H'].values, 1e-6)
    sig_cf_H   = np.maximum(df['sigma_cf_H'].values, 1e-6)
    log_sig_H      = np.log(sig_H)
    log_sig_bulk_H = np.log(sig_bulk_H)
    log_sig_cf_H   = np.log(sig_cf_H)
    tau_eff_H = np.sqrt(np.maximum(df['phi'].values * 3.0 / sig_H, 1e-6))
    log_tau_eff_H = np.log(tau_eff_H)
    log_constr_share_H = np.log(sig_H / sig_bulk_H + 1e-9)

    y_P = np.log(np.maximum(df['sigma'].values, 1e-12))
    y_H = log_sig_H

    # ─────────────────────────────────────────────────────────
    # PART A — Lasso form distillation
    # ─────────────────────────────────────────────────────────
    print('\n' + '=' * 80, flush=True)
    print('PART A — Lasso form (structural-only, no Hertzian) distillation', flush=True)
    print('=' * 80, flush=True)
    feats_A = {
        'log_excess': log_excess,
        'log_CN': log_CN,
        'log_cov': log_cov,
        'log_f_perc': log_f_p,
        'log_tau': log_tau,
        'log_thickness': log_thick,
        'log_gb': log_gb,
        'porosity': porosity,
        'p_frac': p_frac,
        'is_thin': is_thin,
        'b_tabor': b_T, 'b_geom': b_G, 'b_hertzian': b_H, 'b_liggghts': b_L,
        'log_excess__log_CN': log_excess * log_CN,
        'log_cov__log_f_perc': log_cov * log_f_p,
        'log_tau__log_CN': log_tau * log_CN,
        'log_tau__b_tabor': log_tau * b_T,
        'log_tau__log_thickness': log_tau * log_thick,
        'p_frac__b_tabor': p_frac * b_T,
        'log_excess_sq': log_excess ** 2,
        'log_tau_sq': log_tau ** 2,
        'log_CN_sq': log_CN ** 2,
        'b_tabor_sq': b_T ** 2,
    }
    XA = np.column_stack(list(feats_A.values()))
    nA = list(feats_A.keys())
    A = run_single_lasso(XA, nA, y_P, 'A: structural-only (24 candidates)')

    # ─────────────────────────────────────────────────────────
    # PART B — σ_P / σ_bulk_H ratio analysis
    # ─────────────────────────────────────────────────────────
    print('\n' + '=' * 80, flush=True)
    print('PART B — σ_P / σ_bulk_H ratio (plastic-constriction penalty)', flush=True)
    print('=' * 80, flush=True)
    sig_P = np.maximum(df['sigma'].values, 1e-12)
    ratio = sig_P / sig_bulk_H
    print(f'  ratio σ_P / σ_bulk_H stats:', flush=True)
    print(f'    min    = {ratio.min():.4f}', flush=True)
    print(f'    median = {np.median(ratio):.4f}', flush=True)
    print(f'    max    = {ratio.max():.4f}', flush=True)
    print(f'    geomean= {np.exp(np.mean(np.log(ratio))):.4f}', flush=True)

    # Top-5 high-penalty cases (low ratio = strong constriction loss)
    idx_low = np.argsort(ratio)[:5]
    print(f'\n  Top-5 high-penalty cases (low σ_P/σ_bulk_H ratio):', flush=True)
    for i in idx_low:
        nm = df.iloc[i].get('name', '')
        print(f'    {str(nm)[:30]:30s}  ratio={ratio[i]:.3f}  '
              f'τ={df.iloc[i]["tau"]:.2f}  φ={df.iloc[i]["phi"]:.3f}  '
              f'b_T={b_T[i]*100:.1f}%', flush=True)
    idx_high = np.argsort(-ratio)[:5]
    print(f'\n  Top-5 low-penalty cases (high σ_P/σ_bulk_H ratio):', flush=True)
    for i in idx_high:
        nm = df.iloc[i].get('name', '')
        print(f'    {str(nm)[:30]:30s}  ratio={ratio[i]:.3f}  '
              f'τ={df.iloc[i]["tau"]:.2f}  φ={df.iloc[i]["phi"]:.3f}  '
              f'b_T={b_T[i]*100:.1f}%', flush=True)

    # Predict log(ratio) from structural features (find what controls penalty)
    y_ratio = np.log(ratio)
    B = run_single_lasso(XA, nA, y_ratio,
                         'B: log(σ_P/σ_bulk_H) ~ structural features')

    # ─────────────────────────────────────────────────────────
    # PART C — Universality test (predict σ_H with same form)
    # ─────────────────────────────────────────────────────────
    print('\n' + '=' * 80, flush=True)
    print('PART C — Universality: same structural Lasso for Hertzian σ', flush=True)
    print('=' * 80, flush=True)
    C = run_single_lasso(XA, nA, y_H, 'C: predict σ_H from structural features')
    # Compare survivors with PART A
    surv_A = {n_ for n_, _ in A['survivors']}
    surv_C = {n_ for n_, _ in C['survivors']}
    overlap = surv_A & surv_C
    only_A = surv_A - surv_C
    only_C = surv_C - surv_A
    print(f'\n  Survivor overlap σ_P vs σ_H:', flush=True)
    print(f'    common  ({len(overlap)}): {sorted(overlap)}', flush=True)
    print(f'    only σ_P({len(only_A)}): {sorted(only_A)}', flush=True)
    print(f'    only σ_H({len(only_C)}): {sorted(only_C)}', flush=True)

    # ─────────────────────────────────────────────────────────
    # PART D — Hertzian features individual predictive power
    # ─────────────────────────────────────────────────────────
    print('\n' + '=' * 80, flush=True)
    print('PART D — Hertzian features individual predictive power for σ_P', flush=True)
    print('=' * 80, flush=True)
    hertzian_feats = {
        'log_sigma_H':         log_sig_H,
        'log_sigma_bulk_H':    log_sig_bulk_H,
        'log_sigma_constr_H':  log_sig_cf_H,
        'log_tau_eff_H':       log_tau_eff_H,
        'log_constr_share_H':  log_constr_share_H,
    }
    D_results = {}
    for name_, feat in hertzian_feats.items():
        Xd = feat.reshape(-1, 1)
        D_results[name_] = run_single_lasso(Xd, [name_], y_P,
                                             f'D-{name_} (alone)')

    # All 5 Hertzian features together
    XD_all = np.column_stack(list(hertzian_feats.values()))
    nD_all = list(hertzian_feats.keys())
    D_all = run_single_lasso(XD_all, nD_all, y_P,
                             'D: all 5 Hertzian features (LassoCV)')

    # ─────────────────────────────────────────────────────────
    # SUMMARY
    # ─────────────────────────────────────────────────────────
    print('\n' + '=' * 80, flush=True)
    print('=== COMPREHENSIVE SUMMARY ===', flush=True)
    print('=' * 80, flush=True)
    print(f'  v29 baseline:                         LOOCV = 0.8977', flush=True)
    print(f'  PART A (structural-only Lasso):      LOOCV = {A["r2_loo"]:.4f}',
          flush=True)
    print(f'  PART D-bulk_H alone:                  LOOCV = {D_results["log_sigma_bulk_H"]["r2_loo"]:.4f}',
          flush=True)
    print(f'  PART D-sigma_H alone:                 LOOCV = {D_results["log_sigma_H"]["r2_loo"]:.4f}',
          flush=True)
    print(f'  PART D-tau_eff_H alone:               LOOCV = {D_results["log_tau_eff_H"]["r2_loo"]:.4f}',
          flush=True)
    print(f'  PART D-all 5 Hertzian features:      LOOCV = {D_all["r2_loo"]:.4f}',
          flush=True)
    print(f'  PART C (structural for σ_H):          LOOCV = {C["r2_loo"]:.4f}',
          flush=True)
    print(f'  PART B (predict σ_P/σ_bulk_H ratio):  LOOCV = {B["r2_loo"]:.4f}',
          flush=True)

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    save = {'A_structural_lasso': A, 'B_ratio_lasso': B,
            'C_universality_sigmaH': C,
            'D_individual_hertzian': D_results, 'D_all_hertzian': D_all,
            'ratio_stats': {
                'min': float(ratio.min()),
                'median': float(np.median(ratio)),
                'max': float(ratio.max()),
                'geomean': float(np.exp(np.mean(np.log(ratio)))),
            }}
    with open(out / 'physics_fit_v55_comprehensive.json', 'w') as f:
        json.dump(save, f, indent=2, default=str)
    print(f'\n→ {out}/physics_fit_v55_comprehensive.json', flush=True)


if __name__ == '__main__':
    main()
