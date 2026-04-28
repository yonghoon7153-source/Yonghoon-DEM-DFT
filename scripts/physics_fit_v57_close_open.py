#!/usr/bin/env python3
"""Physics-mode fit v57 — close all 4 open conclusions from v56.

Open items after v56:
  A. Per-batch γ varies (0.9–1.2) — why? φ·CN dependence?
  B. (φ-φc)·CN explains only 57% of penalty variance — other 43%?
  C. sigma_constr_only metric extraction (need raw network re-solve)
  D. Multi-mode joint fit — universality quantification

This script tackles A, B, D (C requires expensive re-solve, deferred).

  PART A — Per-batch γ analysis
      For each batch fit σ_P = C·σ_H^γ. Then regress γ on batch-mean
      (φ-φc)·CN. Verdict: is γ a function of regime? If yes, we have
      a unified scaling: σ_P = C(features)·σ_H^γ(features).

  PART B — Penalty drivers beyond (φ-φc)·CN
      LassoCV on log(σ_P/σ_bulk_H) with FULL feature library. Beyond
      the dominant interaction, what else carries signal? Top 5
      drivers ranked.

  PART C — sigma_constr_only availability check
      Verify that raw network dumps (network_conductivity_dual.json)
      contain σ_constr or whether re-solve is needed. Print sample
      keys.

  PART D — Multi-mode joint fit
      Stack σ_P, σ_H, σ_bulk_H predictions in a single regression with
      shared structural features. Mode indicators capture mode-specific
      shift. Tests universality quantitatively: if R² doesn't drop vs
      independent fits, modes share form.
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


def part_A_per_batch_gamma(df):
    """For each batch fit log σ_P = γ·log σ_H + b. Regress γ on
    batch-mean (φ-φc)·CN.
    """
    print('\n' + '=' * 80, flush=True)
    print('PART A — Per-batch γ regression on batch-mean (φ-φc)·CN', flush=True)
    print('=' * 80, flush=True)
    log_P = np.log(np.maximum(df['sigma'].values, 1e-12))
    log_H = np.log(np.maximum(df['sigma_H'].values, 1e-6))
    name = df['name'].astype(str)

    batches = ['1mAh', '6mAh', '8mAh', 'particulate']
    rows = []
    print(f'\n  {"batch":14s}  {"n":>3s}  {"γ":>8s}  {"R²":>8s}  '
          f'{"<(φ-φc)·CN>":>14s}  {"<τ>":>6s}', flush=True)
    for b in batches:
        m = name.str.contains(b, case=False, na=False).values
        if m.sum() < 5: continue
        x = log_H[m]; y = log_P[m]
        gam = float(np.sum((x - x.mean()) * (y - y.mean())) /
                    np.sum((x - x.mean()) ** 2))
        intc = y.mean() - gam * x.mean()
        pred = gam * x + intc
        r2 = 1 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2)
        sub = df[m]
        excess = np.maximum(sub['phi'].values - 0.20, 1e-6)
        cn_excess = np.log(excess) * np.log(np.maximum(sub['cn'].values, 1e-3))
        mean_x = float(np.mean(cn_excess))
        mean_tau = float(np.mean(sub['tau']))
        rows.append({'batch': b, 'n': int(m.sum()), 'gamma': gam,
                      'r2': r2, 'phi_cn_mean': mean_x, 'tau_mean': mean_tau})
        print(f'  {b:14s}  {m.sum():>3d}  {gam:+8.4f}  {r2:8.4f}  '
              f'{mean_x:14.3f}  {mean_tau:6.3f}', flush=True)

    # Regress γ on batch-mean (φ-φc)·CN feature
    gam_arr = np.array([r['gamma'] for r in rows])
    fea_arr = np.array([r['phi_cn_mean'] for r in rows])
    if len(rows) >= 3:
        slope = float(np.sum((fea_arr - fea_arr.mean()) *
                              (gam_arr - gam_arr.mean())) /
                       np.sum((fea_arr - fea_arr.mean()) ** 2))
        intc = float(gam_arr.mean() - slope * fea_arr.mean())
        pred = slope * fea_arr + intc
        r2 = 1 - np.sum((gam_arr - pred) ** 2) / \
                np.sum((gam_arr - gam_arr.mean()) ** 2)
        print(f'\n  γ regression on <(φ-φc)·CN>:', flush=True)
        print(f'    γ = {slope:+.4f} · <(φ-φc)·CN> + {intc:+.4f}', flush=True)
        print(f'    R² = {r2:.4f}', flush=True)
        if r2 > 0.7:
            print('    ⭐ γ is well-explained by batch-mean (φ-φc)·CN — '
                  'unified scaling possible.', flush=True)
        elif r2 > 0.4:
            print('    ~ γ moderately follows (φ-φc)·CN.', flush=True)
        else:
            print('    γ NOT explained by (φ-φc)·CN — different physics across '
                  'batches.', flush=True)
    return rows


def part_B_penalty_full_drivers(df):
    """Lasso on log(σ_P/σ_bulk_H) with full feature library."""
    print('\n' + '=' * 80, flush=True)
    print('PART B — Penalty (σ_P/σ_bulk_H) drivers beyond (φ-φc)·CN', flush=True)
    print('=' * 80, flush=True)
    sig_P = np.maximum(df['sigma'].values, 1e-12)
    sig_bulk_H = np.maximum(df['sigma_bulk_H'].values, 1e-6)
    y = np.log(sig_P / sig_bulk_H)

    # Full feature library (from v55)
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
    sig_H = np.maximum(df['sigma_H'].values, 1e-6)
    log_sig_H = np.log(sig_H)
    log_tau_eff_H = 0.5 * np.log(df['phi'].values * 3.0 / sig_H)

    feats = {
        'log_excess': log_excess, 'log_CN': log_CN,
        'log_cov': log_cov, 'log_f_perc': log_f_p, 'log_tau': log_tau,
        'log_thickness': log_thick, 'log_gb': log_gb,
        'porosity': porosity, 'p_frac': p_frac, 'is_thin': is_thin,
        'b_tabor': b_T, 'b_geom': b_G, 'b_hertzian': b_H, 'b_liggghts': b_L,
        'log_sigma_H': log_sig_H, 'log_tau_eff_H': log_tau_eff_H,
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
    X = np.column_stack(list(feats.values()))
    names = list(feats.keys())
    Xs = (X - X.mean(0)) / (X.std(0) + 1e-9)

    from sklearn.linear_model import LassoCV, Lasso
    from sklearn.model_selection import LeaveOneOut
    lcv = LassoCV(cv=10, max_iter=20000, n_alphas=120,
                  fit_intercept=True, random_state=42)
    lcv.fit(Xs, y)
    alpha = lcv.alpha_; coef = lcv.coef_; intc = lcv.intercept_
    pred = Xs @ coef + intc
    r2_in = 1 - np.sum((y - pred) ** 2) / np.sum((y - y.mean()) ** 2)
    print(f'\n  in-sample R² = {r2_in:.4f}  α = {alpha:.5f}', flush=True)
    nz = [(names[i], float(coef[i])) for i in range(len(coef))
          if abs(coef[i]) > 1e-9]
    nz.sort(key=lambda t: -abs(t[1]))
    print(f'  survivors ({len(nz)}/{len(names)}):', flush=True)
    for n_, g_ in nz[:12]:
        print(f'    {n_:30s}  γ = {g_:+.4f}', flush=True)

    # LOOCV
    n = len(y); pred_loo = np.empty(n)
    for tr, te in LeaveOneOut().split(Xs):
        m = Lasso(alpha=alpha, max_iter=20000, fit_intercept=True)
        m.fit(Xs[tr], y[tr])
        pred_loo[te] = m.predict(Xs[te])[0]
    ss_res = np.sum((y - pred_loo) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2_loo = 1 - ss_res / ss_tot
    print(f'\n  LOOCV R² = {r2_loo:.4f}', flush=True)
    print(f'  Single-feature ((φ-φc)·CN) R² (v56) was 0.57', flush=True)
    print(f'  Improvement with full Lasso: ΔR² = {r2_loo - 0.57:+.3f}',
          flush=True)
    return {'r2_in': r2_in, 'r2_loo': r2_loo, 'alpha': alpha,
            'survivors': nz, 'k_active': len(nz)}


def part_C_constr_availability():
    """Check if sigma_constr_only is recoverable from raw dumps or
    network_conductivity_dual.json files."""
    print('\n' + '=' * 80, flush=True)
    print('PART C — sigma_constr_only availability check', flush=True)
    print('=' * 80, flush=True)
    paths = (list(Path('webapp/results').rglob('network_conductivity*.json')) +
             list(Path('webapp/archive').rglob('network_conductivity*.json')))
    print(f'  found {len(paths)} network_conductivity*.json files', flush=True)
    if not paths:
        print('  ⚠ no per-case network outputs — re-solve required',
              flush=True)
        return {}
    sample = json.load(open(paths[0]))
    print(f'  sample file: {paths[0].name}', flush=True)
    print(f'  sample keys: {list(sample.keys())[:20]}', flush=True)
    if 'hertzian' in sample and isinstance(sample['hertzian'], dict):
        print(f'  hertzian sub-keys: {list(sample["hertzian"].keys())}',
              flush=True)
    return {'n_files': len(paths),
            'sample_keys': list(sample.keys())[:20] if sample else []}


def part_D_multi_mode_joint(df):
    """Joint fit on σ_P, σ_H, σ_bulk_H using shared base + mode indicators."""
    print('\n' + '=' * 80, flush=True)
    print('PART D — Multi-mode joint fit (universality quantification)',
          flush=True)
    print('=' * 80, flush=True)
    log_P = np.log(np.maximum(df['sigma'].values, 1e-12))
    log_H = np.log(np.maximum(df['sigma_H'].values, 1e-6))
    log_bH = np.log(np.maximum(df['sigma_bulk_H'].values, 1e-6))

    # Build common feature matrix
    excess = np.maximum(df['phi'].values - 0.20, 1e-6)
    log_excess = np.log(excess)
    log_CN     = np.log(np.maximum(df['cn'].values, 1e-3))
    log_cov    = np.log(np.maximum(df['cov_phys'].values, 1e-3))
    log_f_p    = np.log(np.maximum(df['f_perc'].values, 1e-3))
    log_tau    = np.log(np.maximum(df['tau'].values, 1e-3))
    log_thick  = np.log(np.maximum(df['thickness'].values, 1.0))
    porosity   = df['porosity'].values / 100.0
    feats = {
        'log_excess': log_excess, 'log_CN': log_CN,
        'log_cov': log_cov, 'log_f_perc': log_f_p, 'log_tau': log_tau,
        'log_thickness': log_thick, 'porosity': porosity,
        'log_excess__log_CN': log_excess * log_CN,
        'log_tau__log_thickness': log_tau * log_thick,
        'log_tau_sq': log_tau ** 2,
    }
    X_common = np.column_stack(list(feats.values()))
    names = list(feats.keys())
    n_feat = X_common.shape[1]

    # Stack: each case appears 3× (one per mode)
    n = len(df)
    X_stack_list = []
    y_stack = []
    mode_idx = []
    for mode_id, target in [(0, log_P), (1, log_H), (2, log_bH)]:
        mode_dummies = np.zeros((n, 3))
        mode_dummies[:, mode_id] = 1.0
        X_stack_list.append(np.column_stack([X_common, mode_dummies]))
        y_stack.append(target)
        mode_idx.extend([mode_id] * n)
    X_stack = np.vstack(X_stack_list)
    y_stack = np.concatenate(y_stack)
    mode_idx = np.array(mode_idx)

    Xs = (X_stack - X_stack.mean(0)) / (X_stack.std(0) + 1e-9)

    from sklearn.linear_model import LassoCV, Lasso
    from sklearn.model_selection import KFold
    lcv = LassoCV(cv=5, max_iter=20000, n_alphas=80,
                  fit_intercept=True, random_state=42)
    lcv.fit(Xs, y_stack)
    alpha = lcv.alpha_; coef = lcv.coef_; intc = lcv.intercept_
    pred = Xs @ coef + intc
    r2_in = 1 - np.sum((y_stack - pred) ** 2) / \
                np.sum((y_stack - y_stack.mean()) ** 2)
    print(f'\n  Joint in-sample R² (3 modes stacked): {r2_in:.4f}', flush=True)

    # Per-mode R² with this joint fit
    print(f'  Per-mode R²:', flush=True)
    for mid, label in [(0, 'σ_P'), (1, 'σ_H'), (2, 'σ_bulk_H')]:
        m = (mode_idx == mid)
        ss_r = np.sum((y_stack[m] - pred[m]) ** 2)
        ss_t = np.sum((y_stack[m] - y_stack[m].mean()) ** 2)
        r2 = 1 - ss_r / ss_t if ss_t > 0 else 0
        print(f'    {label:8s}: R² = {r2:.4f}', flush=True)

    # Show coefficients
    feat_names_ext = names + ['mode_P', 'mode_H', 'mode_bH']
    nz = [(feat_names_ext[i], float(coef[i])) for i in range(len(coef))
          if abs(coef[i]) > 1e-9]
    nz.sort(key=lambda t: -abs(t[1]))
    print(f'\n  Joint-fit survivors ({len(nz)}/{len(feat_names_ext)}):',
          flush=True)
    for n_, g_ in nz[:12]:
        marker = ' (mode shift)' if n_.startswith('mode_') else ''
        print(f'    {n_:30s}  γ = {g_:+.4f}{marker}', flush=True)

    # Mode-shift comparison
    print(f'\n  Mode-shift constants (intercepts per mode):', flush=True)
    for n_, g_ in nz:
        if n_.startswith('mode_'):
            print(f'    {n_}: {g_:+.4f}', flush=True)

    # 5-fold CV
    rng = KFold(n_splits=5, shuffle=True, random_state=42)
    pred_cv = np.empty(len(y_stack))
    for tr, te in rng.split(Xs):
        m = Lasso(alpha=alpha, max_iter=20000, fit_intercept=True)
        m.fit(Xs[tr], y_stack[tr])
        pred_cv[te] = m.predict(Xs[te])
    ss_r = np.sum((y_stack - pred_cv) ** 2)
    ss_t = np.sum((y_stack - y_stack.mean()) ** 2)
    r2_cv = 1 - ss_r / ss_t
    print(f'\n  Joint 5-fold CV R²: {r2_cv:.4f}', flush=True)

    return {'r2_joint_in': float(r2_in), 'r2_joint_cv': float(r2_cv),
            'alpha': float(alpha), 'survivors': nz}


def main():
    cases = load_cases()
    rows = enrich_full(load_phys_rows(cases))
    df = pd.DataFrame(rows)
    print(f'Loaded {len(df)} cases.', flush=True)

    A = part_A_per_batch_gamma(df)
    B = part_B_penalty_full_drivers(df)
    C = part_C_constr_availability()
    D = part_D_multi_mode_joint(df)

    # Final summary
    print('\n' + '=' * 80, flush=True)
    print('=== FINAL SUMMARY (close all open conclusions) ===', flush=True)
    print('=' * 80, flush=True)
    print(f'  A. Per-batch γ:', flush=True)
    for r in A:
        print(f'    {r["batch"]:14s}  γ={r["gamma"]:+.3f}  '
              f'<(φ-φc)·CN>={r["phi_cn_mean"]:+.2f}', flush=True)
    print(f'  B. Penalty Lasso LOOCV: {B["r2_loo"]:.4f} '
          f'(vs single-feat 0.57 → +{B["r2_loo"] - 0.57:.3f})', flush=True)
    print(f'  C. {C.get("n_files", 0)} network_conductivity files available',
          flush=True)
    print(f'  D. Multi-mode joint fit:', flush=True)
    print(f'    in-sample R² = {D["r2_joint_in"]:.4f}', flush=True)
    print(f'    5-fold CV R² = {D["r2_joint_cv"]:.4f}', flush=True)

    out = Path('docs/figures/physics_regime')
    out.mkdir(parents=True, exist_ok=True)
    save = {'A_per_batch_gamma': A, 'B_penalty_drivers': B,
            'C_constr_availability': C, 'D_multimode_joint': D}
    with open(out / 'physics_fit_v57_close_open.json', 'w') as f:
        json.dump(save, f, indent=2, default=str)
    print(f'\n→ {out}/physics_fit_v57_close_open.json', flush=True)


if __name__ == '__main__':
    main()
